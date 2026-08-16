#!/usr/bin/env python3
"""Medium 글을 로그인된 라이브 Chrome(CDP)에서 받아 _unread에 착지시킨다 (medium-fetch 스킬).

**왜 브라우저인가**: Medium은 Cloudflare가 TLS 지문 수준에서 비브라우저 요청을
차단한다(2026-08-16 실측 — curl·urllib은 쿠키·헤더와 무관하게 403). 사용자의
디버그 Chrome은 실제 브라우저라 통과하고, 로그인 세션이 프로필에 유지되므로
쿠키를 따로 보관·갱신할 것도 없다.

**절단본 검증은 SSR 상태의 사실 필드로 한다**: `Post:<id>.content(...)
.isLockedPreviewOnly` — 유료 글을 비로그인으로 열면 true(미리보기만 옴),
전문이면 false(무료 글 포함, 2026-08-16 양쪽 실측). DOM 문구·문단 수 임계 같은
근사 마커는 쓰지 않는다(PLAN §3 — 근사 패턴 금지). 절단본은 저장하지 않고
실패시킨다 — 잘린 스냅샷이 write-once로 정본이 되는 것이 최악의 결과다.

산출물(모두 <kb>/archive/_unread/):
  <slug>.html        원문 — 렌더된 페이지 전체. 이것이 스냅샷 대상(정본)이다.
  _fetch-<slug>.yaml 취득 기록 — 소스 메타(URL·accessed)에 옮길 재료.
  _text-<slug>.md    파생 참고용 — SSR 문단에서 결정적으로 뽑은 본문 텍스트.
                     서식 마크업(EM·STRONG)은 버리고 링크만 보존한다. 미지원
                     문단 타입은 조용히 빼지 않고 [미지원 …] 마커로 표기한다.

    uv run --group ingest tools/medium_fetch.py --kb it <URL> [<URL>…]   # 취득
    uv run --group ingest tools/medium_fetch.py --kb it --login          # 최초 1회 로그인

취득은 화면 밖 헤드풀 창을 스스로 띄웠다 정리한다(평소 창이 보이지 않는다).
9222에 이미 브라우저가 있으면(ui-observe 등) 그것을 재사용한다. 세션이 없거나
만료돼 절단본이 오면 저장하지 않고 `--login`을 안내하며 실패한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon.repo import ROOT

CDP_DEFAULT = "http://localhost:9222"

# 로그인 세션이 사는 프로필 — ui-observe와 공유한다(라이브 브라우저 작업의 단일
# 프로필). 이 디렉터리의 쿠키를 헤드리스 취득이 그대로 읽으므로, 한 번 로그인하면
# 창 없이 재사용된다.
CHROME_BINARY = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PROFILE_DIR = Path.home() / ".claude" / "ui-observe-chrome-profile"
SIGNIN_URL = "https://medium.com/m/signin"

# 페이지 컨텍스트에서 SSR 상태를 구조적으로 읽는다. 문단은 Apollo 정규화 엔트리
# (Paragraph:*)의 __ref를 따라간다 — DOM 파싱이 아니라 Medium이 렌더에 쓰는
# 데이터 그 자체라, 마크업 오프셋(UTF-16)까지 원본 그대로다.
EXTRACT_JS = """(() => {
  const s = window.__APOLLO_STATE__;
  if (!s) return {error: 'no-apollo'};
  const deref = (r) => (r && r.__ref) ? s[r.__ref] : r;
  const posts = Object.keys(s).filter((k) => k.startsWith('Post:')).map((k) => {
    const ck = Object.keys(s[k]).find((f) => f.startsWith('content('));
    return ck ? {post: s[k], content: s[k][ck]} : null;
  }).filter(Boolean);
  if (posts.length !== 1) return {error: 'post-count', n: posts.length};
  const {post, content} = posts[0];
  const body = content.bodyModel;
  if (typeof content.isLockedPreviewOnly !== 'boolean' || !body || !body.paragraphs)
    return {error: 'content-shape', fields: Object.keys(content)};
  const creator = deref(post.creator) || {};
  const collection = deref(post.collection) || {};
  return {
    title: post.title,
    url: post.mediumUrl,
    isLocked: post.isLocked,
    lockedPreviewOnly: content.isLockedPreviewOnly,
    author: creator.name || null,
    publication: collection.name || null,
    publishedAt: post.firstPublishedAt || null,
    paragraphs: body.paragraphs.map(deref).map((p) => ({
      type: p.type,
      text: p.text,
      lang: (p.codeBlockMetadata && p.codeBlockMetadata.lang) || null,
      iframeSrc: (p.iframe && deref(p.iframe.mediaResource) || {}).href || null,
      mixtapeHref: (p.mixtapeMetadata && p.mixtapeMetadata.href) || null,
      markups: (p.markups || [])
        .filter((m) => m.type === 'A' && m.href)
        .map((m) => ({start: m.start, end: m.end, href: m.href})),
    })),
  };
})()"""


class FetchError(Exception):
    pass


# ── CDP 최소 클라이언트 ──────────────────────────────────────────────


class Tab:
    """탭 하나의 WebSocket 세션. Chrome은 Origin 헤더가 있으면 거부한다
    (--remote-allow-origins 없이는 suppress_origin이 필수 — 2026-08-16 실측)."""

    def __init__(self, ws_url: str):
        import websocket  # ingest 그룹 의존 — 순수 함수 테스트가 안 끌려오게 지연

        self.ws = websocket.create_connection(ws_url, timeout=60, suppress_origin=True)
        self.msg_id = 0

    def evaluate(self, expression: str):
        self.msg_id += 1
        self.ws.send(json.dumps({
            "id": self.msg_id, "method": "Runtime.evaluate",
            "params": {"expression": expression, "returnByValue": True},
        }))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") != self.msg_id:
                continue        # 이벤트 통지는 우리 응답이 아니다
            if "error" in msg:
                raise FetchError(f"CDP 오류: {msg['error']}")
            result = msg["result"]["result"]
            if result.get("subtype") == "error":
                raise FetchError(f"페이지 평가 실패: {result.get('description')}")
            return result.get("value")


def cdp_http(cdp: str, path: str, method: str = "GET"):
    request = urllib.request.Request(cdp + path, method=method)
    with urllib.request.urlopen(request, timeout=15) as response:
        body = response.read()
    return json.loads(body) if body.strip() else None


def open_tab(cdp: str, url: str) -> dict:
    return cdp_http(cdp, "/json/new?" + urllib.parse.quote(url, safe=""), method="PUT")


def close_tab(cdp: str, tab_id: str) -> None:
    try:
        urllib.request.urlopen(
            urllib.request.Request(cdp + f"/json/close/{tab_id}"), timeout=15
        ).read()
    except (OSError, urllib.error.URLError):
        pass                    # 정리 실패는 결과에 영향 없음 — 탭이 남을 뿐이다


# ── Chrome 수명 관리 ─────────────────────────────────────────────────
#
# 조율은 CDP 포트 하나로 한다: 9222가 응답하면 그 브라우저(사용자 것이든
# ui-observe 것이든)를 재사용하고, 없으면 우리가 띄운다. 프로필은 한 번에 한
# 인스턴스만 열 수 있어서, 재사용이 곧 프로필 잠금 충돌 회피다.


def cdp_up(cdp: str) -> bool:
    try:
        cdp_http(cdp, "/json/version")
        return True
    except (OSError, urllib.error.URLError):
        return False


def port_of(cdp: str) -> int:
    port = urllib.parse.urlparse(cdp).port
    if port is None:
        raise FetchError(f"CDP 엔드포인트에 포트가 없습니다: {cdp}")
    return port


def launch_chrome(cdp: str, *, hidden: bool, start_url: str) -> subprocess.Popen:
    """취득은 hidden=True(화면 밖 창), 로그인은 hidden=False(보이는 창).

    **헤드리스가 아니라 화면 밖 창인 이유**: Cloudflare가 headless Chrome을 챌린지로
    막는다(2026-08-16 실측 — UA를 정상 Chrome으로 덮어도 통과 못 함). 실제 헤드풀
    창은 통과하므로, 창을 화면 밖(-32000,-32000)에 띄워 사용자 방해 없이 굴린다.
    탐지 회피 패치가 아니라 위치만 옮긴 진짜 브라우저다(PLAN §3 — 우회 금지)."""
    if not Path(CHROME_BINARY).exists():
        raise FetchError(f"Chrome을 찾지 못했습니다: {CHROME_BINARY}")
    argv = [
        CHROME_BINARY,
        f"--remote-debugging-port={port_of(cdp)}",
        f"--user-data-dir={PROFILE_DIR}",
        "--no-first-run", "--no-default-browser-check",
    ]
    if hidden:
        argv += ["--window-position=-32000,-32000", "--window-size=1280,1000"]
    argv.append(start_url)
    return subprocess.Popen(argv, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def wait_cdp(cdp: str, timeout_s: int) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        if cdp_up(cdp):
            return
        time.sleep(0.5)
    raise FetchError(f"{timeout_s}초 안에 Chrome CDP가 뜨지 않았습니다 ({cdp}).")


# ── 파생 텍스트 (순수 함수 — tests/test_medium_fetch.py) ──────────────


def apply_links(text: str, markups: list[dict]) -> str:
    """링크 마크업을 [text](href)로 인라인한다.

    오프셋은 Medium 원본대로 UTF-16 코드 유닛이다 — 파이썬 문자열 인덱스(코드
    포인트)와 다르므로 utf-16-le 바이트로 자른다. 겹치는 링크는 인라인하지 않고
    문단 끝에 (링크: …)로 붙인다 — 오프셋 산수를 망치는 것보다 낫다.
    """
    raw = text.encode("utf-16-le")
    pieces, cursor, trailing = [], 0, []
    for m in sorted(markups, key=lambda m: (m["start"], m["end"])):
        start, end = m["start"] * 2, m["end"] * 2
        if start < cursor or end > len(raw) or start >= end:
            trailing.append(m["href"])
            continue
        pieces.append(raw[cursor:start].decode("utf-16-le"))
        pieces.append(f"[{raw[start:end].decode('utf-16-le')}]({m['href']})")
        cursor = end
    pieces.append(raw[cursor:].decode("utf-16-le"))
    out = "".join(pieces)
    if trailing:
        out += " (링크: " + ", ".join(trailing) + ")"
    return out


def paragraph_to_md(p: dict) -> str:
    """Medium 문단 타입 → md 한 블록. 대응표가 정본이고, 표 밖 타입은 조용히
    버리지 않고 마커로 남긴다(파생물이라 실패 대신 표기 — 정본은 HTML)."""
    text = apply_links(p.get("text") or "", p.get("markups") or [])
    prefix = {"H2": "## ", "H3": "### ", "H4": "#### ",
              "P": "", "BQ": "> ", "PQ": "> ",
              "OLI": "1. ", "ULI": "- "}
    kind = p.get("type")
    if kind in prefix:
        return prefix[kind] + text
    if kind == "PRE":
        return f"```{p.get('lang') or ''}\n{p.get('text') or ''}\n```"
    if kind == "IMG":
        return f"[그림{': ' + text if text else ''}]"
    if kind == "IFRAME":
        return f"[임베드 생략{': ' + p['iframeSrc'] if p.get('iframeSrc') else ''}]"
    if kind == "MIXTAPE_EMBED":
        return f"[링크 카드: {text}{' — ' + p['mixtapeHref'] if p.get('mixtapeHref') else ''}]"
    return f"[미지원 문단 타입 {kind} — 원문 HTML 참조: {text[:120]}]"


def derived_markdown(meta: dict) -> str:
    head = [f"# {meta['title']}", ""]
    head.append("> 파생 참고용 — 정본은 같은 디렉터리의 원문 HTML. 서식은 버리고 링크만 보존.")
    head.append("")
    return "\n".join(head + [paragraph_to_md(p) for p in meta["paragraphs"]]) + "\n"


# ── 취득 흐름 ────────────────────────────────────────────────────────


def wait_ready(tab: Tab, timeout_s: int) -> None:
    deadline = time.monotonic() + timeout_s
    while time.monotonic() < deadline:
        state = tab.evaluate(
            "({ready: document.readyState, apollo: typeof window.__APOLLO_STATE__,"
            "  title: document.title})"
        )
        if state["ready"] == "complete" and state["apollo"] == "object":
            time.sleep(1)       # SSR 직후 하이드레이션 잔여분
            return
        time.sleep(1)
    if "cloudflare" in (state.get("title") or "").lower() or "attention" in (state.get("title") or "").lower():
        raise FetchError("Cloudflare 챌린지에 걸렸습니다 — `--login`으로 창을 띄워 직접 통과시킨 뒤 재실행하십시오.")
    raise FetchError(f"{timeout_s}초 안에 페이지가 준비되지 않았습니다 (title: {state.get('title')!r}).")


def slug_of(canonical_url: str) -> str:
    name = Path(urllib.parse.urlparse(canonical_url).path).name
    if not name:
        raise FetchError(f"URL에서 슬러그를 얻지 못했습니다: {canonical_url}")
    return name


def fetch_one(cdp: str, url: str, unread: Path, timeout_s: int) -> Path:
    tab_info = open_tab(cdp, url)
    try:
        tab = Tab(tab_info["webSocketDebuggerUrl"])
        wait_ready(tab, timeout_s)
        meta = tab.evaluate(EXTRACT_JS)
        if meta.get("error") == "no-apollo":
            raise FetchError("Medium SSR 상태(__APOLLO_STATE__)가 없습니다 — Medium 글이 맞습니까?")
        if meta.get("error") == "post-count":
            raise FetchError(f"본문 Post 엔트리가 {meta['n']}개입니다(1개여야 함) — 글 페이지가 아니거나 구조가 바뀌었습니다.")
        if meta.get("error") == "content-shape":
            raise FetchError(f"Post content 구조를 이해하지 못했습니다(필드: {meta['fields']}) — 도구 갱신이 필요합니다.")
        if meta["lockedPreviewOnly"]:
            raise FetchError(
                "절단본(미리보기)입니다 — 저장하지 않았습니다. 로그인 세션이 없거나 만료됐을 "
                "가능성이 큽니다. `--login`으로 한 번 로그인한 뒤 재실행하십시오."
            )
        html = tab.evaluate("document.documentElement.outerHTML")
        if not html or "</html" not in html.lower():
            raise FetchError("페이지 HTML을 온전히 얻지 못했습니다.")
    finally:
        close_tab(cdp, tab_info["id"])

    slug = slug_of(meta["url"])
    html_path = unread / f"{slug}.html"
    if html_path.exists():
        raise FetchError(f"{html_path.relative_to(ROOT)} 가 이미 있습니다 — 재취득이면 지우고 다시 실행하십시오.")

    html_bytes = ("<!DOCTYPE html>\n" + html).encode("utf-8")
    html_path.write_bytes(html_bytes)
    (unread / f"_text-{slug}.md").write_text(derived_markdown(meta), encoding="utf-8")
    record = {
        "url": meta["url"],
        "requested_url": url,
        "accessed": date.today().isoformat(),
        "title": meta["title"],
        "author": meta["author"],
        "publication": meta["publication"],
        "published": (
            datetime.fromtimestamp(meta["publishedAt"] / 1000, tz=timezone.utc).date().isoformat()
            if meta["publishedAt"] else None
        ),
        "is_locked": meta["isLocked"],
        "sha256_html": hashlib.sha256(html_bytes).hexdigest(),
        "fetched_via": "medium_fetch.py (CDP)",
    }
    (unread / f"_fetch-{slug}.yaml").write_text(
        yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    return html_path


def do_login(cdp: str) -> int:
    """헤드풀 창을 Medium 로그인 페이지로 띄우고 사람에게 넘긴다.

    창은 이 프로세스보다 오래 산다(detach) — 사용자가 로그인하면 세션이 프로필에
    저장되고, 이후 취득은 헤드리스로 그 쿠키를 읽는다. 연 1회 수준의 일이다."""
    if cdp_up(cdp):
        raise FetchError(
            f"{cdp}에 이미 Chrome이 떠 있습니다(ui-observe 등). 그 창에서 {SIGNIN_URL} 로 "
            "이동해 로그인하거나, 그 브라우저를 닫은 뒤 다시 `--login` 하십시오 — 프로필은 한 번에 하나만 엽니다."
        )
    launch_chrome(cdp, hidden=False, start_url=SIGNIN_URL)
    print("Chrome 창을 띄웠습니다. Medium에 로그인(Sign in with Google)하십시오.")
    print("로그인이 끝나면 창은 닫아도 됩니다 — 세션은 프로필에 저장됩니다.")
    print("이후 `/medium-fetch <URL>`은 화면 밖 창으로 조용히 동작합니다.")
    return 0


def do_fetch(cdp: str, urls: list[str], unread: Path, timeout_s: int) -> int:
    """9222가 응답하면 그 브라우저를 재사용하고(끄지 않음), 없으면 화면 밖 창으로
    직접 띄워 취득 후 정리한다 — 평소 실행에서 창이 보이지 않는다."""
    reused = cdp_up(cdp)
    owned: subprocess.Popen | None = None
    if not reused:
        owned = launch_chrome(cdp, hidden=True, start_url="about:blank")
        try:
            wait_cdp(cdp, 20)
        except FetchError:
            owned.terminate()
            raise
    try:
        for url in urls:
            saved = fetch_one(cdp, url, unread, timeout_s)
            print(f"보존  {saved.relative_to(ROOT)}  (+ _fetch·_text 사이드카)")
    finally:
        if owned is not None:
            owned.terminate()
            try:
                owned.wait(timeout=10)
            except subprocess.TimeoutExpired:
                owned.kill()
    print("\n다음: kb-ingest 2단계 — _unread에서 꺼내 snapshot.py에 넘기면 citekey로 승격됩니다.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Medium 글을 라이브 Chrome에서 받아 _unread에 착지")
    parser.add_argument("urls", nargs="*", help="Medium 글 URL")
    parser.add_argument("--kb", required=True)
    parser.add_argument("--login", action="store_true",
                        help="로그인 창을 띄운다(연 1회 수준). URL 없이 단독 실행")
    parser.add_argument("--cdp", default=CDP_DEFAULT, help=f"CDP 엔드포인트 (기본 {CDP_DEFAULT})")
    parser.add_argument("--timeout", type=int, default=45, help="페이지 준비 대기 초")
    args = parser.parse_args(argv)

    try:
        import websocket  # noqa: F401
    except ImportError:
        print("websocket-client가 없습니다 — `uv run --group ingest tools/medium_fetch.py …` 로 실행하십시오.",
              file=sys.stderr)
        return 1

    if args.login == bool(args.urls):
        print("URL을 받아 취득하거나(`<URL>…`), `--login`으로 로그인하거나 — 둘 중 하나만 하십시오.",
              file=sys.stderr)
        return 1

    layout_mod.load().require(args.kb)

    try:
        if args.login:
            return do_login(args.cdp)
        unread = ROOT / args.kb / "archive" / "_unread"
        unread.mkdir(parents=True, exist_ok=True)
        return do_fetch(args.cdp, args.urls, unread, args.timeout)
    except FetchError as error:
        print(f"실패  {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

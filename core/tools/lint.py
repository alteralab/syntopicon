#!/usr/bin/env python3
"""전수 리포트 — 품질을 묻는다 (PLAN §4.3 검사 매트릭스).

validate와의 경계: validate는 "깨졌는가"를 묻고 커밋을 막는다. lint는 "품질이
어떤가"를 묻고 **검출만 한다** — 수정 커밋은 사람이 한다. 경계를 섞으면 커밋이
품질 논쟁에 막힌다.

PLAN §4.3 매트릭스 15행 전부 구현됐다. overlap은 qmd 벡터가 없으면 **경고로**
건너뛴다 — 조용한 생략은 "검사했다"는 착각을 만든다.

    uv run tools/lint.py                 # 전수
    uv run tools/lint.py --incremental   # 직전 실행 이후 바뀐 페이지만 (주간 실행)
    uv run tools/lint.py --kb it
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.parse import unquote

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml
from jsonschema import Draft202012Validator

from syntopicon import index_db, layout as layout_mod, schemas, snapshot, stats
from syntopicon.mdfile import MdFile, read
from syntopicon.repo import ROOT, added_at as repo_added_at, visible_files

# ── 운영 상수 ────────────────────────────────────────────────────────────────
# PLAN이 규정한 것: 500줄 백스톱·100줄 TOC(§2.6), inbox P90 30일·lint 오류 50건(§6).
# 나머지는 자체 상수이고, PLAN §6대로 운영 데이터로 보정할 자리다.
PAGE_LINE_BACKSTOP = 500
TOC_REQUIRED_ABOVE = 100
MAX_HEADING_DEPTH = 4          # H4가 필요해지면 분할 신호(§2.6, 자체 휴리스틱)
HUB_DEGREE = 3                 # 허브 후보로 볼 최소 피링크 차수 — 자체 상수
INBOX_P90_DAYS = 30
LINT_ERROR_TRIPWIRE = 50

# overlap 후보 임계. 실측(2026-08-06, Qwen3-Embedding-0.6B) 네 대역:
#   · 근사 그대로 복제(문장만 다듬음):                       1.000  → 검출
#   · 재생성 중복(같은 용어, 다른 소스·문장·구조 — 주 사용례): 0.922  → 검출
#   · 관련되지만 서로 다른 개념(실 KB 전쌍):                  0.65–0.77 → 통과
#   · 어휘가 전혀 다른 의미 중복(SSOT 프로브):                0.542  → 사각!
# 임계는 0.77과 0.92 사이의 실측 간극에 있다. 교차 어휘 재서술(0.54)은 관련-상이
# 대역보다도 낮아 어떤 임계로도 분리되지 않는다 — 모델 능력의 한계라 숫자로 못
# 고친다. 그 사각은 inbox 리뷰 3문 ⑵·저장 전 검색이 담당하고, 수용 검증 ②의
# 임베딩 A/B(vs KURE-v1)가 한국어 특화 모델로 대역이 갈라지는지 재측정한다.
OVERLAP_THRESHOLD = 0.85
FRAGMENT_MIN_HITS = 2   # 한 번뿐인 파편은 오탐일 확률이 높다 — 자체 상수
# 허브 분할 힌트 임계. 근거: PLAN이 허브 페이지에 준 예산은 1–2k 토큰[선택]이고
# 실측 30링크 허브 ≈ 2.6KB ≈ 그 예산 규모다 — 40은 상단 여유를 둔 환산치.
# 탐색 고장은 차수 가중 neighbors가 임계 없이 막으므로(§4.1 구현), 이 검사가 지키는
# 것은 진입점 예산과 훑기 가능성뿐이다. 자체 상수 — 운영 데이터로 보정.
HUB_SPLIT_HINT = 40

# 본문 인라인 토큰. AST가 "코드도 링크도 아닌 텍스트"까지 갈라 준 **뒤에** 그 텍스트
# 안에서 어휘를 보는 것이라, PLAN §3이 허용한 정규 언어 검증에 해당한다.
EPISTEMIC_TOKEN = re.compile(r"(?<![\w#])#([a-z][a-z0-9-]*)")
WIKILINK = re.compile(r"!?\[\[[^\]]+\]\]")
# 원어 병기 쌍 `한국어 역어(english term)` — 같은 범주의 어휘 스캔이다.
TERM_PAIR = re.compile(r"([가-힣][가-힣 ·]{0,30}?)\(([A-Za-z][A-Za-z /,\u2013-]{2,60})\)")


@dataclass(frozen=True)
class Finding:
    check: str
    severity: str            # error | warn | info
    message: str
    kb: str | None = None
    path: str | None = None


@dataclass
class Context:
    layout: layout_mod.Layout
    connection: object
    files: dict[str, MdFile]          # 경로 → 파싱 결과 (전수)
    changed: set[str]                 # 이번에 페이지 검사를 돌릴 대상
    overlap_full: bool = False        # 전쌍 비교 (부트스트랩·분기) — 기본은 changed×전체
    meta: dict[str, dict] = field(default_factory=dict)
    epistemic: frozenset[str] = frozenset()
    #: `_progress.yaml` 검증기 — 스키마 적재는 실행당 1회여야 하므로(@cache 제거 후
    #: schemas.load()는 부를 때마다 파일을 읽는다) 페이지 루프 밖에서 만들어 들고 다닌다.
    progress_validator: Draft202012Validator | None = None

    def kb_of(self, path: str) -> str:
        return path.split("/", 1)[0]


# ── 그래프 검사 (edges) ──────────────────────────────────────────────────────

def check_links(ctx: Context):
    redirects = {p for p, f in ctx.files.items() if f.type == "redirect"}
    for row in ctx.connection.execute("SELECT src, dst, kind, resolved FROM edges"):
        src, dst = row["src"], row["dst"]
        if not row["resolved"]:
            yield Finding("broken-link", "error", f"→ {dst}", ctx.kb_of(src), src)
        elif dst in redirects:
            target = (ctx.files[dst].frontmatter or {}).get("superseded_by", "?")
            yield Finding("redirect-hop", "warn",
                          f"→ {dst} 는 스텁입니다. {target} 로 직접 걸 것", ctx.kb_of(src), src)
        if row["kind"] == "cross_kb":
            yield Finding("cross-kb-link", "warn",
                          f"→ {dst} (KB 자립성 위반 — 저장소 분리 시 파손)", ctx.kb_of(src), src)


def check_orphans(ctx: Context):
    """어디서도 가리키지 않는 페이지. 진입점과 검역 중인 초안은 제외한다.

    참조는 두 채널이다 — 본문 링크(edges)와 frontmatter의 `sources[].resource`
    (PLAN §2.4의 루트 기준 경로). 후자를 안 세면 인용되고 있는 소스 메타가 전부
    영구 false positive로 찍히고, 그런 소음은 리포트 전체를 무시하게 만든다.
    """
    linked = {row["dst"] for row in
              ctx.connection.execute("SELECT DISTINCT dst FROM edges WHERE resolved = 1")}
    cited = {
        source["resource"].lstrip("/")
        for meta in ctx.meta.values()
        for source in meta["frontmatter"].get("sources", [])
        if isinstance(source, dict) and "resource" in source
    }
    for path, meta in ctx.meta.items():
        if path in linked or path in cited or meta["directory"] in (None, "inbox"):
            continue
        if meta["type"] == "redirect":
            # 스텁은 잔존 참조를 받기 위해 존재한다 — 내부 링크 0이 정상 상태이고,
            # 경유하는 링크가 생기면 redirect-hop 검사가 따로 잡는다.
            continue
        yield Finding("orphan", "info", "가리키는 페이지가 없습니다", meta["kb"], path)


def check_hubs(ctx: Context):
    """Hubs 절 ↔ 고차수 synthesis 대조 — overview 갱신 후보를 낸다(PLAN §4.3).

    자동 갱신하지 않는다. 목록 자동화는 생존하지만 큐레이션 자동화는 실패한다는 것이
    PLAN §8의 결론이고, 무엇을 허브로 올릴지는 사람의 선정이다.
    """
    section = ctx.layout.sections["hubs"]
    degrees = {row["dst"]: row["degree"] for row in ctx.connection.execute(
        "SELECT dst, COUNT(*) AS degree FROM edges WHERE resolved = 1 GROUP BY dst")}

    for kb in ctx.layout.kbs():
        marker = f"{kb}/{ctx.layout.marker_path}"
        if (overview := ctx.files.get(marker)) is None:
            continue
        listed = {
            str(Path(marker).parent / href.partition("#")[0])
            for href in overview.links if "://" not in href
        }
        if not any(text.strip() == section for _, _, text in overview.headings):
            yield Finding("hubs-section", "warn",
                          f"'{section}' 절이 없습니다 (layout.yaml의 절 계약)", kb, marker)
            continue

        for path, meta in ctx.meta.items():
            if (meta["kb"] == kb and meta["type"] == "synthesis"
                    and degrees.get(path, 0) >= HUB_DEGREE and path not in listed):
                yield Finding("hub-candidate", "info",
                              f"피링크 {degrees[path]}회인데 {section} 절에 없습니다", kb, path)
        for missing in sorted(listed - set(ctx.meta) - {marker}):
            yield Finding("hub-dangling", "warn",
                          f"{section} 절이 없는 페이지를 가리킵니다: {missing}", kb, marker)


# ── 메타 테이블 검사 ─────────────────────────────────────────────────────────

def check_stale(ctx: Context):
    today = date.today().isoformat()
    for path, meta in ctx.meta.items():
        if meta["stale_after"] and meta["stale_after"] < today:
            yield Finding("stale", "warn",
                          f"{meta['stale_after']} 만료 — 재검토 큐", meta["kb"], path)


def check_contradictions(ctx: Context):
    """모순은 상호 기록이어야 한다(PLAN §2.1). 자동 해소 금지 — 연구 과제 큐로만 낸다."""
    for path, meta in ctx.meta.items():
        for other in meta["frontmatter"].get("contradicts", []):
            counterpart = f"{meta['kb']}/{Path(path).parent.name}/{other}.md"
            listed = ctx.meta.get(counterpart, {}).get("frontmatter", {}).get("contradicts", [])
            if Path(path).stem not in listed:
                yield Finding("contradiction-one-sided", "error",
                              f"{other} 를 모순으로 적었는데 상대는 적지 않았습니다",
                              meta["kb"], path)
            else:
                yield Finding("contradiction", "info",
                              f"{other} 와 모순 — 해소 시 최신성 단독 판단 금지", meta["kb"], path)


def check_fragments(ctx: Context):
    """형태소 파편화 → 사용자 사전 후보 큐(PLAN §4.3).

    reindex가 관측해 둔 것을 읽기만 한다. 여러 페이지에서 같은 파편이 반복되면
    사전에 없는 복합어라는 신호가 강해진다.
    """
    rows = ctx.connection.execute("""
        SELECT surface, pieces, COUNT(*) AS hits, COUNT(DISTINCT path) AS pages
        FROM fragments GROUP BY surface, pieces
        HAVING hits >= ? ORDER BY hits DESC
    """, (FRAGMENT_MIN_HITS,)).fetchall()
    for row in rows:
        yield Finding("morph-fragmentation", "info",
                      f"'{row['surface']}' 가 {row['pieces']} 로 부서집니다 "
                      f"({row['hits']}회/{row['pages']}페이지) — user-dict.yaml 후보")


def check_overlap(ctx: Context):
    """어휘가 달라도 의미가 겹치는 페이지 쌍 → compaction 후보 큐 (PLAN §2.6·§4.3).

    qmd의 청크 벡터를 재사용한다. 읽을 수 없으면 **크게** 건너뛴다 — 조용한 생략은
    "검사했다"는 착각을 만들고, 그 착각이 미구현 목록을 두던 이유였다.
    """
    from syntopicon import overlap

    knowledge = {
        path for path, meta in ctx.meta.items()
        if meta["directory"] in ("concepts", "synthesis", "inbox")
        and meta["type"] != "redirect"
    }
    try:
        vectors = overlap.load_vectors(tuple(ctx.layout.kbs()))
    except overlap.QmdUnavailable as reason:
        yield Finding("overlap-skipped", "warn",
                      f"overlap 검사를 건너뜀 — {reason}")
        return

    vectors = {path: matrix for path, matrix in vectors.items() if path in knowledge}
    if missing := knowledge - set(vectors):
        yield Finding("overlap-skipped", "warn",
                      f"임베딩 없는 페이지 {len(missing)}개 제외 — qmd update && qmd embed "
                      f"(예: {sorted(missing)[0]})")

    changed = None if ctx.overlap_full else ctx.changed
    pairs, examined = overlap.find_pairs(vectors, OVERLAP_THRESHOLD, changed)
    if examined:
        # 분모 없이 목록만 보면 "이 정도면 흔한 일"로 읽혀 오판이 난다(§8 실측).
        yield Finding("overlap", "info",
                      f"비교 {examined}쌍 중 {len(pairs)}건이 임계 "
                      f"{OVERLAP_THRESHOLD} 초과 ({len(pairs) / examined:.2%})")
    for pair in pairs:
        yield Finding("overlap", "info",
                      f"{pair.left} ↔ {pair.right}  유사도 {pair.similarity:.2f} — "
                      "compaction 후보(병합 판단은 사람)", ctx.kb_of(pair.left))


def check_hub_size(ctx: Context):
    """출차수가 임계를 넘은 synthesis 페이지 → 분할 후보 리포트.

    메가허브의 탐색 고장 자체는 차수 가중 neighbors가 막지만, 오리엔테이션 때
    통째로 읽히는 진입점이 예산(1–2k 토큰)을 넘게 크는 것과 훑기 불가능해지는
    것은 남는다. 분할 판단은 사람이 한다 — "주제가 갈라지면 허브를 나눈다".
    """
    for row in ctx.connection.execute("""
        SELECT src, COUNT(*) AS degree FROM edges WHERE resolved = 1
        GROUP BY src HAVING degree > ?
    """, (HUB_SPLIT_HINT,)):
        if ctx.meta.get(row["src"], {}).get("type") == "synthesis":
            yield Finding("hub-split-hint", "info",
                          f"링크 {row['degree']}개 > {HUB_SPLIT_HINT} — 허브 분할 후보 "
                          "(진입점 예산 1–2k 토큰, PLAN §3)",
                          ctx.kb_of(row["src"]), row["src"])


def check_term_drift(ctx: Context):
    """같은 원어가 서로 다른 역어로 병기되면 리포트한다 — 저장 어휘와 미래의 검색어가
    갈라지는 것이 이 검사가 막는 실패다("집계 도메인" vs "애그리게이트", 실사례).

    한계를 명시한다: **병기된 것만 잡는다.** 병기 없이 쓰인 역어("공통 진입로"가
    그랬다)는 기계가 원어를 알 수 없어 못 잡는다 — 그쪽은 리뷰 소관이고, 병기
    규율(§4.4-4)을 지킬수록 이 검사의 커버리지가 넓어진다.
    """
    renderings: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    for path, md in ctx.files.items():
        for text in md.texts:
            for korean, english in TERM_PAIR.findall(text):
                renderings[english.strip().lower()][korean.strip()].add(path)

    def same_term(a: str, b: str) -> bool:
        """캡처에는 산문 접두가 붙는다(정규식이 leftmost에서 시작하므로). 같은 역어로
        보는 조건: 한쪽이 다른 쪽의 어절 접미이거나("핵심은 비즈니스 역량" ⊇ "비즈니스
        역량"), 공통 어절 접미가 2어절 이상 — 용어 자체가 겹친다는 뜻이다. 1어절
        공통("도메인"·"흐름")은 일반 명사 머리일 뿐이라 드리프트로 남긴다. 휴리스틱이고
        info 등급이다 — 판정은 사람이 한다."""
        ta, tb = a.split(), b.split()
        short, long_ = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
        if long_[-len(short):] == short:
            return True
        common = 0
        for x, y in zip(reversed(ta), reversed(tb)):
            if x != y:
                break
            common += 1
        return common >= 2

    for english, by_korean in sorted(renderings.items()):
        clusters: list[str] = []           # 대표 = 가장 짧은 표기
        for korean in sorted(by_korean, key=lambda k: (len(k.split()), len(k))):
            if not any(same_term(korean, seen) for seen in clusters):
                clusters.append(korean)
        if len(clusters) > 1:
            pages = sorted({p for paths in by_korean.values() for p in paths})
            yield Finding("term-drift", "info",
                          f"({english}) 역어가 갈라짐: {' / '.join(clusters)} — "
                          f"{', '.join(pages)}")


def check_field_usage(ctx: Context):
    """선언 대비 실사용 대조(PLAN §2.7). 소비자 없는 필드가 쌓이는 것을 조회로 드러낸다."""
    used = {key for meta in ctx.meta.values() for key in meta["frontmatter"]}
    for key in sorted(schemas.declared_keys() - used - {"type"}):
        yield Finding("field-unused", "info", f"스키마가 선언했지만 쓰인 적 없습니다: {key}")


def check_inbox(ctx: Context):
    """inbox 나이 — P90이 임계를 넘으면 파산 신호다(PLAN §6 tripwire)."""
    ages: dict[str, list[int]] = defaultdict(list)
    for path, meta in ctx.meta.items():
        if meta["directory"] != "inbox":
            continue
        days = (datetime.now(timezone.utc) - repo_added_at(path)).days
        ages[meta["kb"]].append(days)
        if days > INBOX_P90_DAYS:
            yield Finding("inbox-age", "warn", f"{days}일째 리뷰 대기", meta["kb"], path)

    for kb, values in ages.items():
        ordered = sorted(values)
        p90 = ordered[min(int(len(ordered) * 0.9), len(ordered) - 1)]
        if p90 > INBOX_P90_DAYS:
            yield Finding("inbox-p90", "error",
                          f"inbox 나이 P90 {p90}일 > {INBOX_P90_DAYS}일 — "
                          "적체 발생 신호입니다(대응은 사람이 정합니다 — "
                          "자동 승급 경로는 없습니다, PLAN §4.4)", kb)





# ── 페이지 검사 (md AST) ─────────────────────────────────────────────────────

def check_page(ctx: Context, path: str, md: MdFile):
    meta = ctx.meta.get(path)
    if meta is None:
        return
    kb, front = meta["kb"], md.frontmatter or {}

    if md.line_count > PAGE_LINE_BACKSTOP:
        yield Finding("page-too-long", "warn",
                      f"{md.line_count}줄 — 분할 판단은 목적 기준으로(§2.6). "
                      "1차 완화책은 분할이 아니라 TOC + 섹션 앵커", kb, path)
    if md.line_count > TOC_REQUIRED_ABOVE and not _has_toc(md):
        yield Finding("toc-missing", "info", f"{md.line_count}줄인데 상단 TOC가 없습니다", kb, path)

    yield from _check_headings(kb, path, md)

    # 페이지 안 앵커 링크(`](#…)`)가 실제 헤딩을 가리키는가. rename은 앵커를 재작성하지
    # 않으므로(PLAN §2.5-2) 여기가 유일한 검출 지점이다. 클릭해도 안 움직이는 링크는
    # 렌더도 성공하고 validate도 통과해서 조용히 남는다.
    anchors = page_anchors(md.headings)
    for href in md.links:
        if not href.startswith("#"):
            continue
        # markdown-it이 링크 목적지를 퍼센트 인코딩한다 — 한글 앵커는 디코드해야 비교된다.
        target = unquote(href[1:])
        if target not in anchors:
            yield Finding("anchor-broken", "warn",
                          f"#{target} 가 이 페이지의 헤딩과 맞지 않습니다 — "
                          f"구두점 주변 공백이 하이픈 둘로 남는 경우가 흔합니다", kb, path)

    # 각주 = 출처 귀속 전용 채널이므로, 선언한 소스가 인용되지 않으면 둘 중 하나다:
    # 죽은 소스 항목이거나, 정의가 빠져 평문이 된 각주(validate가 못 보는 그 경우).
    declared = {s["id"] for s in front.get("sources", []) if isinstance(s, dict) and "id" in s}
    for unused in sorted(declared - md.footnote_labels):
        yield Finding("source-uncited", "warn",
                      f"sources에 {unused} 를 선언했지만 각주가 없습니다 "
                      "(각주 정의 누락이면 본문에 [^…] 가 평문으로 남아 있습니다)", kb, path)

    if front.get("type") == "concept":
        for bullet in md.bullets:
            # 하위 열거 불릿은 부모 불릿의 각주를 상속한다(§2.1).
            if not bullet.cites and not bullet.pointer_only and not bullet.inherits_cite:
                yield Finding("claim-unfootnoted", "info",
                              f"{bullet.line}행: {bullet.text[:40]}…", kb, path)
            if bullet.cites and not bullet.locator_before_cite:
                yield Finding("locator-missing", "info",
                              f"{bullet.line}행: 각주 앞에 locator 괄호가 없습니다 — "
                              f"claim은 각주+locator(§4.4-4)", kb, path)

        # 코드 펜스는 각주 달린 claim 아래에 있어야 한다(SCHEMA.md §3). 소스에 없는
        # 코드를 지어내면 예제가 아니라 발명한 claim이고, 문법이 맞으면 그럴듯해
        # 보여서 산문보다 눈에 안 띈다. 검사 대상은 소속뿐 — 코드가 정말 그 소스에서
        # 왔는지는 기계가 못 본다(리뷰 양식이 담당).
        for fence in md.fences:
            if not fence.sourced:
                yield Finding("code-unsourced", "warn",
                              f"{fence.line}행: 코드 펜스가 각주 달린 claim 밖에 "
                              f"있습니다 — 출처 없는 코드는 넣지 않는다(§3)", kb, path)

    # 허브·overview 링크 불릿 문법(§2.6): 링크로 시작하는 불릿은 한 줄 설명을 진다.
    if front.get("type") in ("synthesis", "guide"):
        for bullet in md.bullets:
            if bullet.link_led and bullet.pointer_only:
                yield Finding("hub-grammar", "warn",
                              f"{bullet.line}행: 링크 불릿에 설명이 없습니다 — "
                              f"`- [제목](경로) — 한 줄 설명`(§2.6)", kb, path)

    for text in md.texts:
        if _inline_dollar_math(text):
            yield Finding("inline-dollar-math", "warn",
                          "`$…$` 인라인 수식은 쓰지 않습니다 — 문장 속 기호는 유니코드 + "
                          "이름 병기, 여러 줄은 ```math 펜스(SCHEMA.md §3). "
                          "어느 md 스펙에도 없어 파서가 백슬래시를 먹습니다", kb, path)
        for token in EPISTEMIC_TOKEN.findall(text):
            if token not in ctx.epistemic:
                yield Finding("epistemic-token", "warn",
                              f"미정의 토큰 #{token} — 폐쇄 어휘는 "
                              f"{sorted(ctx.epistemic)} 뿐입니다(태그 체계 없음)", kb, path)
        if match := WIKILINK.search(text):
            yield Finding("wikilink", "warn",
                          f"Obsidian 전용 문법 {match.group()} — GFM 부분집합만 씁니다", kb, path)

    yield from _check_snapshot(kb, path, front)
    yield from _check_progress(kb, path, front, ctx.progress_validator)


def heading_anchor(text: str) -> str:
    """GitHub 앵커 1개. 소문자화 → 영숫자·공백·하이픈·언더스코어 외 제거 → 공백을 하이픈으로.

    구두점이 사라지면서 **양쪽 공백이 하이픈 둘로 남는 것**이 실측된 함정이다
    (`제목 — 부제` → `제목--부제`). 손으로 쓴 목차는 하이픈을 하나만 적는다.
    """
    kept = "".join(c for c in text.lower() if c.isalnum() or c in " -_")
    return kept.replace(" ", "-")


def page_anchors(headings) -> set[str]:
    """페이지의 실제 앵커 전부. 같은 앵커가 반복되면 GitHub은 `-1`·`-2`를 덧붙인다."""
    seen: dict[str, int] = {}
    anchors = set()
    for _, _, text in headings:
        base = heading_anchor(text)
        n = seen.get(base, 0)
        anchors.add(base if n == 0 else f"{base}-{n}")
        seen[base] = n + 1
    return anchors


def _inline_dollar_math(text: str) -> bool:
    """`$…$` 인라인 수식이 있는가. 통화(`$50`)와 가르는 것이 이 함수의 존재 이유다.

    판별은 pandoc 규칙(MANUAL "Math"): 여는 `$`는 **바로 오른쪽이 공백이 아니어야**
    하고, 닫는 `$`는 **바로 왼쪽이 공백이 아니고 바로 오른쪽이 숫자가 아니어야** 한다.
    이 셋이 통화 오식별을 막는 유일하게 성문된 처방이고(jgm이 cmark#439에서 요구한
    바로 그 규칙), 실측에서 이 저장소 282파일에 오탐 0건이었다.

    입력은 AST의 순수 텍스트 노드다 — 코드 스팬·코드 펜스·링크 목적지는 이미 빠져
    있으므로 여기서 다시 가르지 않는다(파서 우선, PLAN §3).
    """
    opens = [
        i for i, ch in enumerate(text)
        if ch == "$" and i + 1 < len(text) and not text[i + 1].isspace()
    ]
    for start in opens:
        for end in range(start + 1, len(text)):
            if text[end] != "$":
                continue
            left_ok = not text[end - 1].isspace()
            right_ok = end + 1 >= len(text) or not text[end + 1].isdigit()
            if left_ok and right_ok:
                return True
            break          # 첫 후보가 닫기 조건을 못 채우면 이 여는 기호는 버린다
    return False


def _has_toc(md: MdFile) -> bool:
    """`**목차**:` 인라인 문단(§2.6 형식 정본) 또는 H2 앞 포인터 불릿 목록을 TOC로 본다.

    2026-08-10 감사: 저작 관례는 인라인 문단형인데 검사가 불릿형만 인정해
    13건 중 10+건이 오검출이었다 — 형식을 §2.6에 계약으로 성문하고 검사를 맞췄다.
    """
    if md.inline_toc_line is not None:
        return True
    first_h2 = next((line for level, line, _ in md.headings if level == 2), md.line_count)
    return any(bullet.line < first_h2 and bullet.pointer_only for bullet in md.bullets)


def _check_headings(kb: str, path: str, md: MdFile):
    levels = [level for level, _, _ in md.headings]
    if levels.count(1) != 1:
        yield Finding("heading-h1", "warn", f"H1이 {levels.count(1)}개입니다 (파일당 하나)", kb, path)
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            yield Finding("heading-skip", "warn",
                          f"H{previous} 다음에 H{current} — 레벨 건너뛰기", kb, path)
            break
    if deepest := max((lvl for lvl in levels if lvl > MAX_HEADING_DEPTH), default=0):
        yield Finding("heading-depth", "info",
                      f"H{deepest}까지 내려갑니다 — 분할 신호(§2.6)", kb, path)


def _check_snapshot(kb: str, path: str, front: dict):
    if not (declared := front.get("snapshot")):
        return
    root = ROOT / declared.lstrip("/")
    if not root.is_dir():
        yield Finding("snapshot-missing", "warn",
                      f"{declared} 가 없습니다 — 외부 링크는 연 3% 이상 부패합니다", kb, path)
        return
    if (recorded := front.get("snapshot_sha256")) and recorded != snapshot.digest(root):
        yield Finding("snapshot-mismatch", "error",
                      f"{declared} 의 다이제스트가 기록과 다릅니다 — 변조 증거", kb, path)


#: 소스 타입 → `_progress.yaml`이 쓸 수 있는 단위. 소스가 나뉘는 방식이 타입마다 다르다.
#: 논문은 나눌 이유가 없고(한 편이 한 단위), 웹 문서는 스냅샷한 URL 하나가 한 단위다.
UNITS_FOR = {"book": {"page", "chapter"}, "webpage": {"url"},
             "paper": {"whole"}, "paper-conference": {"whole"}}


def _check_progress(kb: str, path: str, front: dict, validator: Draft202012Validator):
    """`archive/<citekey>/_progress.yaml` — 재개점의 정본(SCHEMA·kb-ingest 4단계).

    validate가 아니라 lint인 이유는 `archive/`가 git 밖이라서다 — `_check_snapshot`이
    같은 자리에 있는 것과 같은 이유. 검사가 막는 실패는 하나다: **소스 메타 산문이
    정본 노릇을 하다 아홉 런 뒤처져 재반입을 부를 뻔했다**(2026-08-12).
    """
    if not (declared := front.get("snapshot")):
        return
    progress = ROOT / declared.lstrip("/") / "_progress.yaml"
    if not progress.is_file():
        yield Finding("progress-missing", "warn",
                      f"{declared}_progress.yaml 이 없습니다 — 재개점을 소스 메타 산문에 "
                      f"기대면 표류합니다", kb, path)
        return
    try:
        document = yaml.safe_load(progress.read_text())
    except yaml.YAMLError as error:
        yield Finding("progress-invalid", "error", f"_progress.yaml 파싱 실패: {error}", kb, path)
        return

    for error in sorted(validator.iter_errors(document), key=lambda e: list(e.path)):
        where = "/".join(str(p) for p in error.path) or "(루트)"
        yield Finding("progress-invalid", "error",
                      f"_progress.yaml {where}: {error.message}", kb, path)
        return

    # 타입↔단위 정합. 소스 타입은 frontmatter가 정본이다 — 경로에 인코딩하지 않는다(§3).
    allowed = UNITS_FOR.get(front.get("type"), set())
    if allowed and document["unit"] not in allowed:
        yield Finding("progress-unit", "warn",
                      f"type: {front['type']} 인데 unit: {document['unit']} — "
                      f"쓸 수 있는 것은 {sorted(allowed)}", kb, path)
    if document["unit"] == "page" and not document.get("contents"):
        yield Finding("progress-contents", "warn",
                      "unit: page 인데 contents(장↔쪽 대응)가 없습니다 — 목차에서 옮기면 "
                      "covered 범위가 몇 장인지 읽힙니다", kb, path)

    # 접미↔단위 일치. 값이 인용될 때 단위가 떨어져 나가는 것을 막으려고 값마다 붙이되,
    # 붙인 것이 `unit`과 어긋나면 두 정본이 되므로 여기서 묶는다(schema/progress.yaml).
    if suffix := {"page": "p", "chapter": "ch"}.get(document["unit"]):
        ranges = [*document["covered"], *(s["range"] for s in document["skipped"]),
                  *document.get("contents", {}).values()]
        for value in ranges + [document.get("total"), document.get("next")]:
            if value is None:
                continue
            for part in str(value).split("-"):
                if part and not part.endswith(suffix):
                    yield Finding("progress-suffix", "warn",
                                  f"unit: {document['unit']} 인데 `{value}` 에 접미 "
                                  f"`{suffix}` 가 없습니다 — 값만 인용되면 단위를 잃습니다",
                                  kb, path)


# ── git 검사 ─────────────────────────────────────────────────────────────────

def check_ingest_trailers(ctx: Context):
    """소스를 새로 들인 커밋에는 Ingest-Source:/Ingest-Run: 트레일러가 있어야 한다(§4.4-7)."""
    pathspecs = [f"{kb}/sources" for kb in ctx.layout.kbs()]
    if not pathspecs:
        return
    result = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%H", "--", *pathspecs],
        capture_output=True, text=True)
    for commit in result.stdout.split():
        body = subprocess.run(["git", "-C", str(ROOT), "show", "-s", "--format=%B", commit],
                              capture_output=True, text=True).stdout
        if missing := [t for t in ("Ingest-Source:", "Ingest-Run:") if t not in body]:
            yield Finding("ingest-trailer", "warn",
                          f"{commit[:8]} 가 소스를 추가했는데 {', '.join(missing)} 가 없습니다")


def check_skill_symlinks(ctx: Context):
    # 호출 표면(~/.claude/skills/*)은 심링크라 조용히 깨진다 — 스킬이 에러 없이
    # 그냥 안 보이게 되는 유형이라 lint가 유일한 검출 지점이다.
    surface = Path.home() / ".claude" / "skills"
    skills_root = ROOT / ".agents" / "skills"
    if not skills_root.is_dir():          # 테스트 샌드박스·부분 체크아웃
        return
    for skill_dir in sorted(skills_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        link = surface / skill_dir.name
        if not link.is_symlink():
            yield Finding("skill-symlink", "error",
                          f"~/.claude/skills/{skill_dir.name} 심링크 없음 — 전 프로젝트 호출 불가")
        elif link.resolve() != skill_dir.resolve():
            yield Finding("skill-symlink", "error",
                          f"~/.claude/skills/{skill_dir.name} 이 정본이 아닌 {link.resolve()} 를 가리킴")


# ── 실행 ─────────────────────────────────────────────────────────────────────

GRAPH_CHECKS = (check_links, check_orphans, check_hubs, check_stale,
                check_contradictions, check_field_usage, check_fragments,
                check_term_drift, check_hub_size, check_overlap, check_inbox,
                check_ingest_trailers, check_skill_symlinks)


def build_context(layout: layout_mod.Layout, connection, baseline: dict[str, str],
                  incremental: bool, only_kb: str | None) -> Context:
    files, meta, changed = {}, {}, set()
    for row in connection.execute("SELECT * FROM files"):
        path = row["path"]
        if only_kb and row["kb"] != only_kb:
            continue
        files[path] = read(ROOT / path, Path(path))
        meta[path] = {
            "kb": row["kb"], "directory": row["directory"], "type": row["type"],
            "status": row["status"], "stale_after": row["stale_after"],
            "sha256": row["sha256"], "frontmatter": json.loads(row["frontmatter"]),
        }
        if not incremental or baseline.get(path) != row["sha256"]:
            changed.add(path)

    vocabulary = yaml.safe_load((ROOT / "schema" / "vocabulary.yaml").read_text())
    return Context(
        layout=layout, connection=connection, files=files, changed=changed, meta=meta,
        epistemic=frozenset(vocabulary["epistemic"]["tokens"]),
        progress_validator=Draft202012Validator(
            {"$ref": "progress.yaml#"}, registry=schemas.load().registry),
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="전수 리포트 (검출만 — 수정은 사람이)")
    parser.add_argument("--kb", default=None)
    parser.add_argument("--incremental", action="store_true",
                        help="직전 실행 이후 바뀐 페이지만 검사한다 (그래프 검사는 항상 전수)")
    parser.add_argument("--overlap-full", action="store_true",
                        help="overlap 전쌍 비교 — 부트스트랩과 분기 전수 검사용(PLAN §4.3)")
    parser.add_argument("--quiet", action="store_true", help="info 등급을 숨긴다")
    args = parser.parse_args(argv)

    layout = layout_mod.load()
    if not index_db.DB_PATH.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    with stats.connect() as stats_db:
        baseline = stats.baseline(stats_db)
        with index_db.connect() as connection:
            ctx = build_context(layout, connection, baseline, args.incremental, args.kb)
            ctx.overlap_full = args.overlap_full
            findings = [f for check in GRAPH_CHECKS for f in check(ctx)]
            for path in sorted(ctx.changed):
                findings += list(check_page(ctx, path, ctx.files[path]))

        mode = "incremental" if args.incremental else "full"
        stats.record_run(stats_db, mode, findings,
                         {p: m["sha256"] for p, m in ctx.meta.items()})

    return report(findings, ctx, mode, args.quiet)


def report(findings: list[Finding], ctx: Context, mode: str, quiet: bool) -> int:
    order = {"error": 0, "warn": 1, "info": 2}
    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.check].append(finding)

    for check in sorted(grouped, key=lambda c: (order[grouped[c][0].severity], c)):
        items = grouped[check]
        if quiet and items[0].severity == "info":
            continue
        print(f"\n[{items[0].severity}] {check} — {len(items)}건")
        for finding in items[:20]:
            where = f"{finding.path or finding.kb or '저장소'}: "
            print(f"  {where}{finding.message}")
        if len(items) > 20:
            print(f"  … 외 {len(items) - 20}건 (전체는 stats.sqlite의 lint_findings)")

    errors = sum(1 for f in findings if f.severity == "error")
    print(f"\n{len(ctx.changed)}/{len(ctx.meta)}개 페이지 검사({mode}) · "
          f"오류 {errors} · 경고 {sum(1 for f in findings if f.severity == 'warn')} · "
          f"정보 {sum(1 for f in findings if f.severity == 'info')}")
    if errors > LINT_ERROR_TRIPWIRE:
        print(f"임계 경보: 오류 {errors} > {LINT_ERROR_TRIPWIRE} — 유지보수 세션이 필요합니다(PLAN §6).")

    # lint는 검출만 한다 — 오류가 있어도 실패로 끝내지 않는다. 커밋을 막는 것은 validate다.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

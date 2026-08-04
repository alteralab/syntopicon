#!/usr/bin/env python3
"""전수 리포트 — 품질을 묻는다 (PLAN §4.3 검사 매트릭스).

validate와의 경계: validate는 "깨졌는가"를 묻고 커밋을 막는다. lint는 "품질이
어떤가"를 묻고 **검출만 한다** — 수정 커밋은 사람이 한다. 경계를 섞으면 커밋이
품질 논쟁에 막힌다.

미구현 1행(PLAN §4.3 표): 페이지 overlap — 임베딩이 서야 한다(qmd 단계).
자리를 비워 두고, 조용히 빠뜨리지 않도록 실행할 때마다 미구현 목록을 출력한다.

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

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml

from syntopicon import index_db, layout as layout_mod, schemas, snapshot, stats
from syntopicon.mdfile import MdFile, read
from syntopicon.repo import ROOT, visible_files

# ── 운영 상수 ────────────────────────────────────────────────────────────────
# PLAN이 규정한 것: 500줄 백스톱·100줄 TOC(§2.6), inbox P90 30일·lint 오류 50건(§6).
# 나머지는 자체 상수이고, PLAN §6대로 운영 데이터로 보정할 자리다.
PAGE_LINE_BACKSTOP = 500
TOC_REQUIRED_ABOVE = 100
MAX_HEADING_DEPTH = 4          # H4가 필요해지면 분할 신호(§2.6, 자체 휴리스틱)
HUB_DEGREE = 3                 # 허브 후보로 볼 최소 피링크 차수 — 자체 상수
INBOX_P90_DAYS = 30
LINT_ERROR_TRIPWIRE = 50

UNIMPLEMENTED = {
    "page-overlap": "임베딩 필요 (qmd 단계)",
}
FRAGMENT_MIN_HITS = 2   # 한 번뿐인 파편은 오탐일 확률이 높다 — 자체 상수

# 본문 인라인 토큰. AST가 "코드도 링크도 아닌 텍스트"까지 갈라 준 **뒤에** 그 텍스트
# 안에서 어휘를 보는 것이라, PLAN §3이 허용한 정규 언어 검증에 해당한다.
EPISTEMIC_TOKEN = re.compile(r"(?<![\w#])#([a-z][a-z0-9-]*)")
WIKILINK = re.compile(r"!?\[\[[^\]]+\]\]")


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
    meta: dict[str, dict] = field(default_factory=dict)
    epistemic: frozenset[str] = frozenset()

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
    """어디서도 가리키지 않는 페이지. 진입점과 검역 중인 초안은 제외한다."""
    linked = {row["dst"] for row in
              ctx.connection.execute("SELECT DISTINCT dst FROM edges WHERE resolved = 1")}
    for path, meta in ctx.meta.items():
        if path in linked or meta["directory"] in (None, "inbox"):
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
        days = (datetime.now(timezone.utc) - _added_at(path)).days
        ages[meta["kb"]].append(days)
        if days > INBOX_P90_DAYS:
            yield Finding("inbox-age", "warn", f"{days}일째 리뷰 대기", meta["kb"], path)

    for kb, values in ages.items():
        ordered = sorted(values)
        p90 = ordered[min(int(len(ordered) * 0.9), len(ordered) - 1)]
        if p90 > INBOX_P90_DAYS:
            yield Finding("inbox-p90", "error",
                          f"inbox 나이 P90 {p90}일 > {INBOX_P90_DAYS}일 — "
                          "자동 머지 범위 확대를 검토하십시오(PLAN §4.4 킬 기준)", kb)


def _added_at(path: str) -> datetime:
    """파일이 저장소에 들어온 시점. 아직 커밋 전이면 지금으로 본다."""
    result = subprocess.run(
        ["git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%aI", "--", path],
        capture_output=True, text=True)
    if lines := result.stdout.split():
        return datetime.fromisoformat(lines[-1])
    return datetime.now(timezone.utc)


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

    # 각주 = 출처 귀속 전용 채널이므로, 선언한 소스가 인용되지 않으면 둘 중 하나다:
    # 죽은 소스 항목이거나, 정의가 빠져 평문이 된 각주(validate가 못 보는 그 경우).
    declared = {s["id"] for s in front.get("sources", []) if isinstance(s, dict) and "id" in s}
    for unused in sorted(declared - md.footnote_labels):
        yield Finding("source-uncited", "warn",
                      f"sources에 {unused} 를 선언했지만 각주가 없습니다 "
                      "(각주 정의 누락이면 본문에 [^…] 가 평문으로 남아 있습니다)", kb, path)

    if front.get("type") == "concept":
        for bullet in md.bullets:
            if not bullet.cites and not bullet.pointer_only:
                yield Finding("claim-unfootnoted", "info",
                              f"{bullet.line}행: {bullet.text[:40]}…", kb, path)

    for text in md.texts:
        for token in EPISTEMIC_TOKEN.findall(text):
            if token not in ctx.epistemic:
                yield Finding("epistemic-token", "warn",
                              f"미정의 토큰 #{token} — 폐쇄 어휘는 "
                              f"{sorted(ctx.epistemic)} 뿐입니다(태그 체계 없음)", kb, path)
        if match := WIKILINK.search(text):
            yield Finding("wikilink", "warn",
                          f"Obsidian 전용 문법 {match.group()} — GFM 부분집합만 씁니다", kb, path)

    yield from _check_snapshot(kb, path, front)


def _has_toc(md: MdFile) -> bool:
    """H1 뒤 첫 H2 앞에 목록이 있으면 TOC로 본다."""
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


# ── 실행 ─────────────────────────────────────────────────────────────────────

GRAPH_CHECKS = (check_links, check_orphans, check_hubs, check_stale,
                check_contradictions, check_field_usage, check_fragments,
                check_inbox, check_ingest_trailers)


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
    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="전수 리포트 (검출만 — 수정은 사람이)")
    parser.add_argument("--kb", default=None)
    parser.add_argument("--incremental", action="store_true",
                        help="직전 실행 이후 바뀐 페이지만 검사한다 (그래프 검사는 항상 전수)")
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
    print("미구현 검사: " + ", ".join(f"{k}({v})" for k, v in UNIMPLEMENTED.items()))

    # lint는 검출만 한다 — 오류가 있어도 실패로 끝내지 않는다. 커밋을 막는 것은 validate다.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

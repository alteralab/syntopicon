#!/usr/bin/env python3
"""전수 리포트 — 품질을 묻는다 (PLAN §4.3).

validate와의 경계: validate는 "깨졌는가"를 묻고 커밋을 막는다. lint는 "품질이
어떤가"를 묻고 **검출만 한다** — 수정 커밋은 사람이 한다. 경계를 섞으면 커밋이
품질 논쟁에 막힌다.

검사 본체는 syntopicon/checks/ 패키지에 데이터 소스별로 산다. 결과 종류의
이름·등급·판독 지침의 정본은 그 패키지의 Kind 레지스트리이고, `--explain`이
그것을 조회한다 — 문서에 손으로 병렬 유지하지 않는다(표류 3건의 교훈).

    uv run tools/lint.py                 # 전수
    uv run tools/lint.py --incremental   # 직전 실행 이후 바뀐 페이지만 (주간 실행)
    uv run tools/lint.py --kb it
    uv run tools/lint.py --explain               # 결과 종류 전부와 판독 지침
    uv run tools/lint.py --explain broken-link   # 한 종류만
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml
from jsonschema import Draft202012Validator

from syntopicon import index_db, layout as layout_mod, schemas, stats
from syntopicon.workspace import DEFAULT
from syntopicon.checks import CHECKS, KINDS, Context, Finding, check_page
from syntopicon.checks.base import SEVERITY_ORDER
from syntopicon.mdfile import read
from syntopicon.repo import ROOT

LINT_ERROR_TRIPWIRE = 50       # PLAN §6


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
        time_relative=frozenset(vocabulary.get("time-relative", {}).get("words", ())),
        time_relative_except=frozenset(vocabulary.get("time-relative", {}).get("except", ())),
        progress_validator=Draft202012Validator(
            {"$ref": "progress.yaml#"}, registry=schemas.load().registry),
    )


def explain(name: str | None) -> int:
    kinds = [KINDS[name]] if name else sorted(
        KINDS.values(), key=lambda k: (SEVERITY_ORDER[k.severity], k.name))
    for k in kinds:
        print(f"[{k.severity}] {k.name} — {k.doc}")
        print(f"  {k.guidance}\n")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="전수 리포트 (검출만 — 수정은 사람이)")
    parser.add_argument("--kb", default=None)
    parser.add_argument("--incremental", action="store_true",
                        help="직전 실행 이후 바뀐 페이지만 검사한다 (그래프 검사는 항상 전수)")
    parser.add_argument("--overlap-full", action="store_true",
                        help="overlap 전쌍 비교 — 부트스트랩과 분기 전수 검사용(PLAN §4.3)")
    parser.add_argument("--quiet", action="store_true", help="info 등급을 숨긴다")
    parser.add_argument("--explain", nargs="?", const="", default=None,
                        metavar="KIND", help="결과 종류의 정의와 판독 지침 (정본 조회)")
    args = parser.parse_args(argv)

    if args.explain is not None:
        if args.explain and args.explain not in KINDS:
            print(f"모르는 결과 종류: {args.explain}", file=sys.stderr)
            return 1
        return explain(args.explain or None)

    ws = DEFAULT
    layout = layout_mod.load()
    if not ws.derived_db.is_file():
        print("파생 인덱스가 없습니다. tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
        return 1

    with stats.connect(ws) as stats_db:
        baseline = stats.baseline(stats_db)
        with index_db.connect(ws) as connection:
            # 낡은 색인의 조용한 소비가 이 도구의 두 실패(증분 누락·삭제 파일
            # traceback)를 만들었다 — 소비 전에 세대 스탬프를 대조한다(감사 B4).
            if reason := index_db.staleness(connection, layout.kbs()):
                print(f"파생 인덱스가 낡았습니다 — {reason}. "
                      "tools/reindex.py를 먼저 실행하십시오.", file=sys.stderr)
                return 1
            ctx = build_context(layout, connection, baseline, args.incremental, args.kb)
            ctx.overlap_full = args.overlap_full
            findings = [f for corpus_check in CHECKS for f in corpus_check(ctx)]
            for path in sorted(ctx.changed):
                findings += list(check_page(ctx, path, ctx.files[path]))

        mode = "incremental" if args.incremental else "full"
        stats.record_run(stats_db, mode, findings,
                         {p: m["sha256"] for p, m in ctx.meta.items()})

    return report(findings, ctx, mode, args.quiet)


def report(findings: list[Finding], ctx: Context, mode: str, quiet: bool) -> int:
    grouped: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        grouped[finding.check].append(finding)

    for name in sorted(grouped, key=lambda c: (SEVERITY_ORDER[KINDS[c].severity], c)):
        items = grouped[name]
        if quiet and KINDS[name].severity == "info":
            continue
        print(f"\n[{KINDS[name].severity}] {name} — {len(items)}건")
        for finding in items[:20]:
            where = f"{finding.path or finding.kb or '저장소'}: "
            print(f"  {where}{finding.message}")
        if len(items) > 20:
            print(f"  … 외 {len(items) - 20}건 (전체는 stats.sqlite의 lint_findings)")

    errors_by = Counter(f.check for f in findings if f.severity == "error")
    errors = sum(errors_by.values())
    print(f"\n{len(ctx.changed)}/{len(ctx.meta)}개 페이지 검사({mode}) · "
          f"오류 {errors} · 경고 {sum(1 for f in findings if f.severity == 'warn')} · "
          f"정보 {sum(1 for f in findings if f.severity == 'info')}")

    # 임계 경보의 분모에서 broken-link를 뺀다 — 경보 이력 6구간 31런 전부가
    # broken-link 100%였고 전부 승급 대기의 정상 상태였다(2026-08-12 실측).
    # 늘 우는 경보는 사람이 무시하게 되고 그것이 경보의 죽음이다.
    gate = errors - errors_by.get("broken-link", 0)
    if gate > LINT_ERROR_TRIPWIRE:
        print(f"임계 경보: 오류 {gate}건(broken-link 제외) > {LINT_ERROR_TRIPWIRE} — "
              "유지보수 세션이 필요합니다(PLAN §6).")
    elif errors > LINT_ERROR_TRIPWIRE:
        print(f"오류 {errors}건 중 broken-link {errors_by.get('broken-link', 0)}건 — "
              "승급 대기 중이면 정상 상태입니다(merge 후 재실행으로 판별).")

    # lint는 검출만 한다 — 오류가 있어도 실패로 끝내지 않는다. 커밋을 막는 것은 validate다.
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

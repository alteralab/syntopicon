#!/usr/bin/env python3
"""승급 사슬 — merge · reindex · qmd 색인 · lint를 한 명령으로 (PLAN §4.4-9).

kb-ingest 9단계는 "한 덩어리다"라고 성문돼 있으면서 사람이 명령 여섯을 순서대로
치는 절차였고, 그 사이가 벌어질 때마다 사고가 났다 — 커밋 미루기 2회, qmd cleanup
누락 3회, `_progress.yaml` 갱신 누락(전부 kb-ingest SKILL의 실측 기록). 문서가
"한 덩어리"라고 부르는 것은 코드여야 한다.

이 도구는 결정적 실행만 묶는다. **커밋은 묶지 않는다** — 상태 변경 명령을 체인으로
잇지 않는 규약(kb-ingest 7단계)대로 커밋·`_progress.yaml` 갱신은 마지막에 안내만
한다. 중간 단계가 실패하면 남은 단계를 명시하고 멈춘다 — 부분 실패를 침묵시키면
반쯤 승급된 상태가 다음 런과 섞인다.

    uv run --group index tools/promote.py --kb it
    uv run --group index tools/promote.py --kb it --dry-run
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import langfuse_bridge
from syntopicon import layout as layout_mod, stats
from syntopicon.workspace import DEFAULT
from syntopicon.repo import visible_files

TOOLS = Path(__file__).resolve().parent


def drafts_of(layout: layout_mod.Layout, kb: str) -> list[Path]:
    kbs = layout.kbs()   # 연산당 1회 — 루프 안 content_dir_of는 파일마다 git을 부른다
    return sorted(
        p for p in visible_files()
        if p.suffix == ".md" and p.parts[0] == kb
        and layout.content_dir_of(p, kbs) == "inbox"
    )


def stages(kb: str, with_qmd: bool) -> list[tuple[str, list[str]]]:
    """실행할 단계 전부 — 계획(dry-run)과 실행이 같은 목록을 읽는다."""
    planned = [
        ("merge", [sys.executable, str(TOOLS / "merge.py"), "--all", "--kb", kb]),
        ("reindex", [sys.executable, str(TOOLS / "reindex.py")]),
    ]
    if with_qmd:
        planned += [
            ("qmd-update", ["qmd", "update"]),
            ("qmd-embed", ["qmd", "embed"]),
            # 편집·이동마다 고아 벡터가 실제로 샌다(실측 3회) — 거르면 옛 경로의
            # 벡터가 남아 조용히 오답을 낸다(kb-ingest 9단계).
            ("qmd-cleanup", ["qmd", "cleanup"]),
        ]
    planned.append(("lint", [sys.executable, str(TOOLS / "lint.py")]))
    # 검색 실측(retrieval-eval)은 이 사슬에 없다 — 2026-09-14 사용자 결정으로 뺐다.
    # 이력: 손 절차였을 때 첫 실행 후 코퍼스가 3배 되도록 안 돌아(2026-08-14 감사) 사슬에
    # 박았으나, 질문지가 68파일·약 1,025문항으로 자라자 승급마다 전수 4레그를 도는 비용이
    # 승급 자체(분 단위)를 압도했다(evans2003 승급 실측: 6단계 완료 뒤 평가만 수십 분).
    # 승급은 "이 초안이 본 코퍼스에 들어가도 되는가"이고 평가는 "코퍼스 전체의 검색 품질
    # 추세"라 물음이 다르며, 회귀는 게이트가 아니라 경보다(러너는 항상 0으로 끝난다).
    # 평가는 사람이 /kb-eval로 명시 호출한다 — 큰 배치 승급 뒤가 그 자리다(kb-ingest 9단계).
    return planned


def run_stages(planned: list[tuple[str, list[str]]]) -> tuple[dict[str, int], str | None]:
    """단계를 순서대로 돌리고 (단계별 소요 ms, 실패한 단계 이름 또는 None)을 돌려준다.

    첫 실패에서 멈추고 남은 단계를 알린다 — 부분 적용된 사슬은 사람이 원인을 고친 뒤
    같은 명령으로 재개한다(이미 승급된 초안은 merge가 대상 없음으로 지나간다).
    """
    durations: dict[str, int] = {}
    for index, (name, command) in enumerate(planned):
        print(f"\n[{index + 1}/{len(planned)}] {name}", flush=True)
        started = time.monotonic()
        code = subprocess.run(command).returncode
        durations[name] = stats.elapsed_ms(started)
        if code == 0:
            continue
        remaining = [n for n, _ in planned[index + 1:]]
        print(f"\n중단: {name} 단계가 종료 코드 {code}로 실패했습니다.", file=sys.stderr)
        if remaining:
            print(f"실행되지 않은 단계: {', '.join(remaining)} — 원인을 고친 뒤 "
                  "이 도구를 다시 실행하십시오(이미 승급된 초안은 merge가 "
                  "대상 없음으로 지나갑니다).", file=sys.stderr)
        return durations, name
    return durations, None


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="inbox 승급 사슬 (커밋은 사람이)")
    parser.add_argument("--kb", required=True)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-qmd", action="store_true",
                        help="qmd 색인 단계를 건너뛴다 (없으면 자동 건너뜀 + 고지)")
    args = parser.parse_args(argv)

    layout = layout_mod.load()
    layout.require(args.kb)
    drafts = drafts_of(layout, args.kb)
    if not drafts:
        print(f"{args.kb}/inbox/ 에 승급할 초안이 없습니다.", file=sys.stderr)
        return 1

    qmd_reason = None
    if args.skip_qmd:
        qmd_reason = "--skip-qmd"
    elif shutil.which("qmd") is None:
        qmd_reason = "qmd가 PATH에 없습니다 — qmd 색인이 낡은 채 남습니다"
    planned = stages(args.kb, with_qmd=qmd_reason is None)

    print(f"승급 대상 {len(drafts)}건:")
    for draft in drafts:
        print(f"  {draft}")
    if qmd_reason:
        print(f"주의: qmd 단계 건너뜀 — {qmd_reason}")
    if args.dry_run:
        print("\n실행 계획: " + " 다음 ".join(name for name, _ in planned))
        print("--dry-run — 아무것도 실행하지 않았습니다.")
        return 0

    durations, failed = run_stages(planned)

    with stats.connect(DEFAULT) as db:
        lint_row = db.execute(
            "SELECT errors, warnings, infos FROM lint_runs ORDER BY id DESC LIMIT 1"
        ).fetchone() if failed is None else None
        stats.record_event(db, "promote", {
            "kb": args.kb,
            "drafts": len(drafts),
            "files": [str(d) for d in drafts],
            "stages_ms": durations,
            "qmd": qmd_reason or "ran",
            "failed_stage": failed,
            "lint": dict(lint_row) if lint_row else None,
        })
    langfuse_bridge.nudge()   # 층 2 편승 — 활동이 있는 날에만 하루 1회 백그라운드 동기화
    if failed:
        return 1

    print(f"\n승급 완료 — {len(drafts)}건. 남은 것은 둘이고 사람이 한다:")
    print(f"  1. {args.kb}/archive/<citekey>/_progress.yaml 갱신 (covered·skipped·next)")
    print(f"  2. git add -A {args.kb}/ && git commit  — Ingest-Run 트레일러 필수, "
          "다음 런 전에 워킹 트리 비우기")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

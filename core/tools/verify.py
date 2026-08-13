#!/usr/bin/env python3
"""verified 승급 — review-on-read의 기록 절반 (PLAN §4.3 kb-query ⑦).

판단(내용을 실사용에서 실제로 확인했는가)은 사람이 하고, 이 도구는 그 사실을
frontmatter에 새길 뿐이다. 수기로 두지 않는 이유: 스탬프 형식이 규약 3개를 동시에
걸치고(따옴표 datetime·빈 리스트 금지·라운드트립 금지 — PLAN §2.1) 반복 작업이라,
손으로 하면 형식이 표류한다.

`verified` 줄만 제자리에서 고친다 — YAML 통짜 load-save는 주석·순서를 재작성하므로
금지다. rename·merge와 같은 규율이다.

    uv run tools/verify.py it/concepts/golden-source.md
    uv run tools/verify.py it/concepts/golden-source.md --by human:me
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon.mdfile import frontmatter_span, read
from syntopicon.repo import ROOT, ensure_clean_worktree, run_validate_gate


class VerifyError(Exception):
    """찍으면 거짓말이 되는 상황. 아무것도 쓰지 않고 멈춘다."""


def stamp(by: str) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return f'{{ by: "{by}", at: "{now}" }}'


def promote(relative: Path, by: str) -> str:
    """frontmatter에 스탬프를 추가한 새 본문을 돌려준다. 대상 줄만 고친다."""
    absolute = ROOT / relative
    md = read(absolute, relative)
    front = md.frontmatter or {}

    layout = layout_mod.load()
    directory = layout.content_dir_of(relative)
    if directory == "inbox":
        raise VerifyError(
            f"{relative}: 아직 검역 중입니다 — 승인은 merge(→ concepts, unverified)이고, "
            "verified는 그 뒤 실사용 확인 시점의 승급입니다. tools/merge.py를 먼저 실행하십시오.")
    if front.get("type") not in ("concept", "synthesis"):
        raise VerifyError(
            f"{relative}: type '{front.get('type')}'에는 verified 계층이 없습니다 — "
            "신뢰 사다리는 지식 페이지(concept·synthesis)의 것입니다.")

    text = absolute.read_text()
    lines = text.splitlines(keepends=True)
    span = frontmatter_span(text)
    if span is None:              # validate 범위 밖 파일 방어 — 없는 블록에 못 새긴다
        raise VerifyError(f"{relative}: frontmatter가 없습니다")
    start, end = span

    for index in range(start, end):
        stripped = lines[index].strip()
        if stripped.startswith("verified:"):
            # 기존 리스트에 누적한다 — 재검증 이력은 덮지 않고 쌓는 것이다.
            if not stripped.endswith("]"):
                raise VerifyError(
                    f"{relative}: verified가 한 줄 플로 리스트가 아닙니다 — 손으로 고친 "
                    "형식은 손으로 이어 가십시오 (이 도구는 자기 형식만 책임진다).")
            lines[index] = lines[index].rstrip()[:-1] + f", {stamp(by)}]\n"
            break
    else:
        # 새 키는 닫는 --- 직전에 넣는다. "generated 옆" 같은 예쁜 자리는 앵커 키가
        # 블록 스타일(여러 줄)일 때 그 한가운데를 가른다 — 실측으로 깨졌다. 닫는
        # 구분선 직전은 어떤 frontmatter에서도 최상위 키 경계임이 보장된다.
        lines.insert(end - 1, f"verified: [{stamp(by)}]\n")

    return "".join(lines)


def main(argv: list[str]) -> int:
    cli = argparse.ArgumentParser(description="verified 승급 기록 (판단은 사람이 먼저)")
    cli.add_argument("paths", nargs="+", type=Path, help="확인을 마친 페이지 (루트 기준)")
    cli.add_argument("--by", default="human:me",
                     help='확인 주체 (기본 human:me — 에이전트가 대신 확인했다면 모델 id)')
    cli.add_argument("--dry-run", action="store_true")
    args = cli.parse_args(argv)

    results = []
    try:
        for relative in args.paths:
            results.append((relative, promote(relative, args.by)))
    except VerifyError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 1

    if not args.dry_run and len(results) > 1:
        # 가드의 근거는 "여러 파일 한꺼번에"(PLAN §2.5-7ⓔ)다 — 단건 스탬프는
        # 세션 중에도 찍을 수 있어야 하므로 면제하고, 다건만 보상 모델을 요구한다.
        ensure_clean_worktree("verify(다건)")

    for relative, text in results:
        if args.dry_run:
            print(f"승급 예정  {relative}")
            continue
        (ROOT / relative).write_text(text)
        print(f"승급  {relative}  ← {args.by}")

    if args.dry_run:
        print("--dry-run — 아무것도 쓰지 않았습니다.")
        return 0

    return run_validate_gate()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

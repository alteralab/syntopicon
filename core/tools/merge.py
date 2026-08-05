#!/usr/bin/env python3
"""검역 해제 — inbox/의 초안을 concepts/로 승격한다 (PLAN §4.4-8).

rename과 다른 연산이다. rename은 발급된 ID의 이동이라 옛 경로에 redirect 스텁을
남기지만, merge는 검역에서 본 코퍼스로의 승격이라 스텁을 남기지 않는다 — inbox는
발행된 위치가 아니고, `dir_types`상 `concept`만 허용하므로 스텁을 두면 validate가
깨진다.

승격은 **unverified 계층으로** 간다. `verified`를 붙이지 않는다는 뜻이다 — 리뷰 기준은
무해성·구조이지 내용의 전수 정확성이 아니고, 정확성은 쓰는 시점에 확인해서
승급시킨다(review-on-read).

    uv run tools/merge.py it/inbox/golden-source.md
    uv run tools/merge.py --kb it --all --dry-run
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod, relocate
from syntopicon.mdfile import read
from syntopicon.repo import ROOT, visible_files
from syntopicon.rewrite import parser

TARGET_DIR = "concepts"


def drop_draft_status(text: str) -> str:
    """`status: draft`만 지운다 — frontmatter를 통째로 다시 쓰지 않는다(PLAN §2.1).

    검역을 벗어나면 초안이 아니다. status는 "값이 생길 때만 기록"이므로 지우는 것이
    맞고, `stable`로 바꿔 적으면 기본값을 명시하는 금지 사항이 된다.
    """
    tokens = parser().parse(text)
    block = next((t for t in tokens if t.type == "front_matter" and t.map), None)
    if block is None:
        return text
    start, end = block.map
    lines = text.splitlines(keepends=True)
    kept = [
        line for line in lines[start:end]
        if line.strip() not in ("status: draft", 'status: "draft"')
    ]
    lines[start:end] = kept
    return "".join(lines)


def merge_one(layout: layout_mod.Layout, old: Path, dry_run: bool) -> Path:
    if layout.content_dir_of(old) != "inbox":
        raise relocate.RelocateError(f"{old}: inbox/의 파일이 아닙니다")

    new = Path(old.parts[0], TARGET_DIR, old.name)
    if (ROOT / new).exists():
        raise relocate.RelocateError(f"{new}: 이미 존재합니다")
    relocate.check_unique(layout, new, exclude=old)

    edits = relocate.plan_edits(old, new)
    print(f"{old} → {new}")
    for edit in edits:
        print(f"  고침  {edit.path} ({edit.note})")
    if dry_run:
        return new

    relocate.apply(new, drop_draft_status((ROOT / old).read_text()), edits)
    (ROOT / old).unlink()          # 검역 흔적을 남기지 않는다 — 스텁 없음
    return new


def main(argv: list[str]) -> int:
    parser_ = argparse.ArgumentParser(description="inbox 초안을 concepts로 승격")
    parser_.add_argument("paths", nargs="*", type=Path, help="승격할 inbox 파일")
    parser_.add_argument("--kb", default=None, help="--all과 함께 쓴다")
    parser_.add_argument("--all", action="store_true", help="그 KB의 inbox 전부")
    parser_.add_argument("--dry-run", action="store_true")
    args = parser_.parse_args(argv)

    layout = layout_mod.load()
    targets = list(args.paths)
    if args.all:
        if not args.kb:
            print("--all에는 --kb가 필요합니다.", file=sys.stderr)
            return 1
        targets += sorted(
            p for p in visible_files()
            if p.suffix == ".md" and p.parts[0] == args.kb
            and layout.content_dir_of(p) == "inbox"
        )
    if not targets:
        print("승격할 파일이 없습니다.", file=sys.stderr)
        return 1

    if not args.dry_run:
        dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                               capture_output=True, text=True, check=True).stdout.strip()
        if dirty:
            raise SystemExit(
                "워킹 트리가 깨끗하지 않습니다. merge는 여러 파일을 한꺼번에 고치므로 "
                "되돌릴 수 있는 상태에서만 실행합니다 (PLAN §2.5-7ⓔ).")

    merged = []
    for old in targets:
        try:
            merged.append(merge_one(layout, old, args.dry_run))
        except relocate.RelocateError as error:
            print(f"중단: {error}", file=sys.stderr)
            return 1

    print(f"\n{len(merged)}개 승격{' 예정' if args.dry_run else ''} — unverified 계층입니다.")
    if args.dry_run:
        print("--dry-run — 아무것도 쓰지 않았습니다.")
        return 0

    print("실사용에서 내용을 확인하면 verified를 붙여 승급시키십시오(review-on-read).")
    print("허브 연결은 사람이 합니다 — kb-lint의 hub-candidate 리포트를 보고 고르십시오.")
    print(flush=True)
    return subprocess.run([sys.executable, str(Path(__file__).parent / "validate.py")]).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

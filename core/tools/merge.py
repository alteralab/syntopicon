#!/usr/bin/env python3
"""검역 해제 — inbox/의 초안을 concepts/로 승격한다 (PLAN §4.4-8).

rename과 다른 연산이다. rename은 발급된 ID의 이동이라 옛 경로에 redirect 스텁을
남기지만, merge는 검역에서 본 코퍼스로의 승격이라 스텁을 남기지 않는다 — inbox는
발행된 위치가 아니고, `dir_types`상 `concept`만 허용하므로 스텁을 두면 validate가
깨진다.

두 종류의 초안을 다룬다. **신규**(concepts에 같은 슬러그 없음)는 새 파일로 승격되고,
**개정판**(같은 슬러그가 이미 있음)은 기존 페이지를 대치한다 — "기존 페이지 갱신이
본체"(PLAN §4.4-4)인 파이프라인에서 갱신도 검역을 지나야 하므로, 개정 초안은 갱신된
전체 페이지를 같은 슬러그로 inbox에 착지시킨다. 리뷰어는 git diff로 무엇이 변했는지
본다.

승격은 **unverified 계층으로** 간다. `status: draft`와 함께 `verified`도 벗긴다 —
개정 초안이 원본에서 스탬프를 복사해 왔더라도 그것은 옛 내용에 대한 증언이다.

나이 기반 자동 머지(PLAN §4.4 ②, [실험]): `--auto --min-age-days N`은 커밋된 지
N일이 지난 **가산 개정판**(기존 본문을 전부 보존하고 추가만 한 것 = "기존 claim
보강")만 승격한다. 신규 페이지와 비가산 개정은 사람 몫으로 남는다. N의 기본값은
없다 — 수용 검증에서 확정한다.

    uv run tools/merge.py it/inbox/golden-source.md
    uv run tools/merge.py --kb it --all --dry-run
    uv run tools/merge.py --kb it --auto --min-age-days 14
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


def strip_quarantine_keys(text: str) -> str:
    """`status: draft`와 `verified`를 지운다 — frontmatter를 통째로 다시 쓰지 않는다.

    검역을 벗어나면 초안이 아니고(status는 부재=기본값이라 지우는 것이 맞다),
    verified는 기계 산출물이 달고 나올 수 있는 스탬프가 아니다 — 개정 초안이
    원본에서 복사해 온 것이라면 그것은 대치되기 전 내용에 대한 증언이다.
    """
    tokens = parser().parse(text)
    block = next((t for t in tokens if t.type == "front_matter" and t.map), None)
    if block is None:
        return text
    start, end = block.map
    lines = text.splitlines(keepends=True)
    kept, in_verified = [], False
    for line in lines[start:end]:
        if in_verified:
            # verified가 블록 스타일 목록이면 그 항목들(들여쓰기 줄)도 함께 지운다 —
            # 키 줄만 지우면 고아 목록이 남아 frontmatter가 깨진다.
            if line[:1].isspace() or line.startswith("- "):
                continue
            in_verified = False
        if line.startswith("verified:"):
            in_verified = True
            continue
        if line.strip() in ("status: draft", 'status: "draft"'):
            continue
        kept.append(line)
    lines[start:end] = kept
    return "".join(lines)


def body_lines(text: str) -> frozenset[str]:
    """frontmatter를 뺀 본문의 실질 줄 집합 — 가산 개정 판정의 재료."""
    tokens = parser().parse(text)
    block = next((t for t in tokens if t.type == "front_matter" and t.map), None)
    lines = text.splitlines()
    body = lines[block.map[1]:] if block else lines
    return frozenset(line.strip() for line in body if line.strip())


def is_additive_revision(target_text: str, draft_text: str) -> bool:
    """기존 본문 전 줄이 초안에 살아 있으면 가산(= "기존 claim 보강")이다.

    자동 머지의 저위험 판별을 결정적으로 만든 대리 기준이다. 오타 수정처럼 줄을
    바꾸는 개정은 여기 안 걸리고 사람 리뷰로 남는다 — 보수 쪽으로 틀리는 선택이다.
    """
    return body_lines(target_text) <= body_lines(draft_text)


def merge_one(layout: layout_mod.Layout, old: Path, dry_run: bool) -> Path:
    if layout.content_dir_of(old) != "inbox":
        raise relocate.RelocateError(f"{old}: inbox/의 파일이 아닙니다")

    new = Path(old.parts[0], TARGET_DIR, old.name)
    revision = (ROOT / new).exists()
    if not revision:
        relocate.check_unique(layout, new, exclude=old)

    edits = relocate.plan_edits(old, new)
    print(f"{old} → {new}{'  (개정판 대치)' if revision else ''}")
    for edit in edits:
        print(f"  고침  {edit.path} ({edit.note})")
    if dry_run:
        return new

    content = strip_quarantine_keys((ROOT / old).read_text())
    if revision:
        # 대치 — 같은 경로라 링크는 그대로 유효하고, O_EXCL은 신규에만 해당한다.
        (ROOT / new).write_text(content)
        for edit in edits:
            (ROOT / edit.path).write_text(edit.text)
    else:
        relocate.apply(new, content, edits)
    (ROOT / old).unlink()          # 검역 흔적을 남기지 않는다 — 스텁 없음
    return new


def main(argv: list[str]) -> int:
    parser_ = argparse.ArgumentParser(description="inbox 초안을 concepts로 승격")
    parser_.add_argument("paths", nargs="*", type=Path, help="승격할 inbox 파일")
    parser_.add_argument("--kb", default=None, help="--all과 함께 쓴다")
    parser_.add_argument("--all", action="store_true", help="그 KB의 inbox 전부")
    parser_.add_argument("--auto", action="store_true",
                         help="나이 기반 자동 머지 — 가산 개정판만, --min-age-days 필수")
    parser_.add_argument("--min-age-days", type=int, default=None,
                         help="이 일수를 넘긴 초안만 (기본값 없음 — 수용 검증에서 확정)")
    parser_.add_argument("--dry-run", action="store_true")
    args = parser_.parse_args(argv)

    if args.auto != (args.min_age_days is not None):
        print("--auto와 --min-age-days는 함께 씁니다.", file=sys.stderr)
        return 1

    layout = layout_mod.load()
    targets = list(args.paths)
    if args.all or args.auto:
        if not args.kb:
            print("--all/--auto에는 --kb가 필요합니다.", file=sys.stderr)
            return 1
        targets += sorted(
            p for p in visible_files()
            if p.suffix == ".md" and p.parts[0] == args.kb
            and layout.content_dir_of(p) == "inbox"
        )

    if args.auto:
        from datetime import datetime, timezone
        from syntopicon.repo import added_at
        eligible = []
        for draft in targets:
            age = (datetime.now(timezone.utc) - added_at(draft)).days
            target = ROOT / draft.parts[0] / TARGET_DIR / draft.name
            if age < args.min_age_days:
                print(f"  보류  {draft}  (나이 {age}일 < {args.min_age_days}일)")
            elif not target.exists():
                print(f"  보류  {draft}  (신규 페이지 — 사람 리뷰)")
            elif not is_additive_revision(target.read_text(), (ROOT / draft).read_text()):
                print(f"  보류  {draft}  (비가산 개정 — 기존 줄 변경, 사람 리뷰)")
            else:
                eligible.append(draft)
        targets = eligible

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

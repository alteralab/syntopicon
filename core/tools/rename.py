#!/usr/bin/env python3
"""개명·이동의 유일한 경로 (PLAN §2.5-2).

ID는 발급 후 불변이므로 손으로 mv 하면 링크가 조용히 깨진다. 이 도구는 한 묶음으로
움직인다: 참조 링크 재작성 + frontmatter 경로 처리 + redirect 스텁 생성 + 사후 검사.

heading 앵커는 재작성하지 않는다 — 어느 헤딩이 어디로 갔는지는 기계가 알 수 없다.
lint가 깨진 앵커를 검증한다(PLAN §2.5-2).

**sources/의 citekey 개명은 절반만 된다(미수정 결함 — PLAN §8).** 링크와 frontmatter
`resource`는 고치지만 본문 각주(`[^citekey]`)와 `sources[].id`는 그대로 남고,
validate가 그 불일치를 잡지 못한다(둘이 서로 짝을 이루므로 규칙 위반이 아니다).
citekey를 개명하려면 그 둘을 손으로 함께 고쳐야 한다.

    uv run tools/rename.py it/concepts/raft.md it/concepts/raft-consensus.md
    uv run tools/rename.py it/concepts/raft.md ops/concepts/raft.md --dry-run
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import relocate, schemas
from syntopicon.mdfile import read
from syntopicon.repo import ROOT
from syntopicon.relocate import RelocateError as RenameError
from syntopicon.relocate import href_to, plan_edits

QMD_SCHEME = relocate.QMD_SCHEME


def stub(old: Path, new: Path, title: str) -> str:
    """옛 경로에 남길 redirect 스텁. 대상은 같은 KB면 이름만, KB를 넘으면 정규형.

    title은 사용자 입력이다 — YAML 값은 손으로 조립하지 않고 json.dumps로 감싼다
    (JSON은 YAML의 부분집합이라 콜론·따옴표·이스케이프가 전부 안전하다). 링크
    텍스트의 대괄호는 이스케이프한다: 균형 잡힌 대괄호는 CommonMark가 봐주지만
    불균형이면 링크가 통째로 깨진다. 적대 입력 배터리가 콜론 제목으로 이 함수가
    깨진 frontmatter를 **파일을 쓴 뒤에야** 드러내는 것을 잡았다.
    """
    same_kb = old.parts[0] == new.parts[0]
    target = new.stem if same_kb else f"{new.parts[0]}/{new.stem}"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    label = title.replace("[", "\\[").replace("]", "\\]")
    return (
        "---\n"
        "type: redirect\n"
        f"title: {json.dumps(title, ensure_ascii=False)}\n"
        f"superseded_by: {target}\n"
        f'generated: {{ by: "tools/rename", at: "{now}" }}\n'
        "---\n"
        "\n"
        f"# {title}\n"
        "\n"
        f"이 페이지는 [{label}]({href_to(old, new)})로 이동했습니다.\n"
    )


def check_preconditions(layout: layout_mod.Layout, sch: schemas.Schemas,
                        old: Path, new: Path, dry_run: bool) -> None:
    if not (ROOT / old).is_file():
        raise RenameError(f"{old}: 파일이 없습니다")
    if (ROOT / new).exists():
        raise RenameError(f"{new}: 이미 존재합니다")

    old_dir, new_dir = layout.content_dir_of(old), layout.content_dir_of(new)
    if old_dir is None:
        raise RenameError(f"{old}: KB 콘텐츠 디렉터리 안의 파일이 아닙니다")
    if new_dir is None:
        raise RenameError(f"{new}: 대상이 KB 콘텐츠 디렉터리가 아닙니다 "
                          f"(대상 KB에 {layout.marker_path}가 있는지 확인하십시오)")
    if old_dir != new_dir:
        raise RenameError(
            f"{old_dir}/ → {new_dir}/ 이동은 type 변경을 뜻하므로 rename의 일이 아닙니다. "
            "계층을 바꾸려면 새 페이지를 쓰고 옛 페이지를 supersede 하십시오.")

    id_kind = "citekey" if new_dir == "sources" else "slug"
    if errors := list(sch.shared(id_kind).iter_errors(new.stem)):
        raise RenameError(f"{new.stem}: {id_kind} 규칙 위반 — {errors[0].message}")

    relocate.check_unique(layout, new, exclude=old)

    if dry_run:
        return
    if subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                      capture_output=True, text=True, check=True).stdout.strip():
        raise RenameError(
            "워킹 트리가 깨끗하지 않습니다. rename은 여러 파일을 한꺼번에 고치므로 "
            "되돌릴 수 있는 상태에서만 실행합니다 (PLAN §2.5-7ⓔ).")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="개명·이동 (링크 재작성 + redirect 스텁)")
    parser.add_argument("old", type=Path, help="현재 경로 (저장소 루트 기준)")
    parser.add_argument("new", type=Path, help="새 경로 (저장소 루트 기준)")
    parser.add_argument("--dry-run", action="store_true", help="계획만 출력하고 쓰지 않는다")
    args = parser.parse_args(argv)

    layout, sch = layout_mod.load(), schemas.load()
    old, new = args.old, args.new

    try:
        check_preconditions(layout, sch, old, new, args.dry_run)
        edits = plan_edits(old, new)
    except RenameError as error:
        print(f"중단: {error}", file=sys.stderr)
        return 1

    content = (ROOT / old).read_text()
    title = (read(ROOT / old, old).frontmatter or {}).get("title", old.stem)

    print(f"{old} → {new}")
    for edit in edits:
        print(f"  고침  {edit.path} ({edit.note})")
    print(f"  스텁  {old} (superseded_by → {new.stem})")
    if args.dry_run:
        print("\n--dry-run — 아무것도 쓰지 않았습니다.")
        return 0

    relocate.apply(new, content, edits)
    (ROOT / old).write_text(stub(old, new, title))

    # 사후 링크 검사 게이트 — 재작성이 끝난 상태를 같은 규칙으로 다시 본다.
    print(flush=True)   # validate의 출력과 섞이지 않게 먼저 비운다
    return subprocess.run([sys.executable, str(Path(__file__).parent / "validate.py")]).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

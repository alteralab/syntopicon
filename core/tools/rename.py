#!/usr/bin/env python3
"""개명·이동의 유일한 경로 (PLAN §2.5-2).

ID는 발급 후 불변이므로 손으로 mv 하면 링크가 조용히 깨진다. 이 도구는 한 묶음으로
움직인다: 참조 링크 재작성 + frontmatter 경로 처리 + redirect 스텁 생성 + 사후 검사.

heading 앵커는 재작성하지 않는다 — 어느 헤딩이 어디로 갔는지는 기계가 알 수 없다.
lint가 깨진 앵커를 검증한다(PLAN §2.5-2).

    uv run tools/rename.py it/concepts/raft.md it/concepts/raft-consensus.md
    uv run tools/rename.py it/concepts/raft.md ops/concepts/raft.md --dry-run
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from syntopicon import layout as layout_mod
from syntopicon import schemas
from syntopicon.mdfile import read
from syntopicon.repo import ROOT, visible_files
from syntopicon.rewrite import rewrite_frontmatter_path, rewrite_links

QMD_SCHEME = "qmd://"


class RenameError(Exception):
    """진행하면 손상이 남는 상황. 아무것도 건드리지 않고 멈춘다."""


@dataclass(frozen=True)
class Edit:
    path: Path
    text: str
    note: str


def _kb_of(layout: layout_mod.Layout, relative: Path) -> str:
    kb = relative.parts[0]
    if kb not in layout.kbs():
        raise RenameError(f"{relative}: KB 안의 파일이 아닙니다")
    return kb


def href_to(layout: layout_mod.Layout, referrer: Path, target: Path) -> str:
    """참조하는 파일에서 대상까지의 올바른 링크 형식.

    같은 KB면 파일 상대 경로, 다른 KB면 `qmd://` — 이동으로 KB 경계를 넘나들면
    링크 형식도 따라 바뀌어야 한다(PLAN §2.4).
    """
    if referrer.parts[0] == target.parts[0]:
        return os.path.relpath(target, referrer.parent)
    kb, *rest = target.parts
    return f"{QMD_SCHEME}{kb}/{Path(*rest)}"


def resolves_to(layout: layout_mod.Layout, referrer: Path, href: str, target: Path) -> bool:
    """이 링크가 대상 파일을 가리키는가. 표기 형태(`./x.md`·`../a/../x.md`)에 흔들리지 않게
    경로로 정규화해 비교한다."""
    if href.startswith(QMD_SCHEME):
        return Path(href.removeprefix(QMD_SCHEME)) == target
    if "://" in href or href.startswith("#"):
        return False
    return os.path.normpath(referrer.parent / href.partition("#")[0]) == str(target)


def plan_edits(layout: layout_mod.Layout, old: Path, new: Path) -> list[Edit]:
    """이동 때문에 고쳐야 할 파일 전부. 모호한 지점이 하나라도 있으면 전체를 중단한다."""
    edits: list[Edit] = []
    ambiguous: list[str] = []

    for relative in visible_files():
        if relative.suffix != ".md" or relative == old:
            continue

        text = (ROOT / relative).read_text()
        original = text
        links = 0

        # 본문 링크 — 같은 대상을 `raft.md`·`./raft.md`처럼 여러 표기로 가리킬 수 있으므로
        # 표기별로 돌리고 합산한다.
        hrefs = {
            href for href in read(ROOT / relative, relative).links
            if resolves_to(layout, relative, href, old)
        }
        for href in sorted(hrefs):
            result = rewrite_links(text, href, href_to(layout, relative, new))
            if result.ambiguities:
                ambiguous += [
                    f"{relative}:{a.line} — 원문 {a.found}건 vs AST {a.expected}건"
                    for a in result.ambiguities
                ]
                continue
            text, links = result.text, links + result.changed

        notes = [f"링크 {links}건"] if links else []

        # frontmatter의 저장소 루트 기준 경로
        result = rewrite_frontmatter_path(text, f"/{old}", f"/{new}")
        if result.changed:
            text = result.text
            notes.append(f"frontmatter 경로 {result.changed}건")

        if text != original:
            edits.append(Edit(relative, text, ", ".join(notes)))

    if ambiguous:
        raise RenameError(
            "링크 표기가 AST와 합의하지 않아 자동 재작성을 중단했습니다. 해당 줄을 손으로\n"
            "인라인 링크 형태로 고친 뒤 다시 실행하십시오 (참조형·제목 붙은 링크·꺾쇠\n"
            "목적지는 지원하지 않습니다):\n  " + "\n  ".join(ambiguous)
        )
    return edits


def stub(layout: layout_mod.Layout, old: Path, new: Path, title: str) -> str:
    """옛 경로에 남길 redirect 스텁. 대상은 같은 KB면 이름만, KB를 넘으면 정규형."""
    same_kb = old.parts[0] == new.parts[0]
    target = new.stem if same_kb else f"{new.parts[0]}/{new.stem}"
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return (
        "---\n"
        "type: redirect\n"
        f"title: {title}\n"
        f"superseded_by: {target}\n"
        f'generated: {{ by: "tools/rename", at: "{now}" }}\n'
        "---\n"
        "\n"
        f"# {title}\n"
        "\n"
        f"이 페이지는 [{title}]({href_to(layout, old, new)})로 이동했습니다.\n"
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

    # 유일성 스코프는 KB다 — 다른 디렉터리에 같은 이름이 있으면 안 된다.
    target_kb = _kb_of(layout, new)
    for other in visible_files():
        if (other != old and other.suffix == ".md" and other.stem == new.stem
                and other.parts[0] == target_kb and layout.content_dir_of(other)):
            raise RenameError(f"{new.stem}: {target_kb} 안에 이미 있습니다 ({other})")

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
        edits = plan_edits(layout, old, new)
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

    # 새 경로는 O_EXCL로 만든다 — check-then-write는 병렬 프로세스에서 덮어쓴다(PLAN §2.5-5).
    (ROOT / new).parent.mkdir(parents=True, exist_ok=True)
    with open(ROOT / new, "x", encoding="utf-8") as handle:
        handle.write(content)

    (ROOT / old).write_text(stub(layout, old, new, title))
    for edit in edits:
        (ROOT / edit.path).write_text(edit.text)

    # 사후 링크 검사 게이트 — 재작성이 끝난 상태를 같은 규칙으로 다시 본다.
    print(flush=True)   # validate의 출력과 섞이지 않게 먼저 비운다
    return subprocess.run([sys.executable, str(Path(__file__).parent / "validate.py")]).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

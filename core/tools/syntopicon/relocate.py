"""파일을 옮길 때 따라와야 하는 것들 — rename과 merge가 공유하는 계층.

두 연산은 다르다. rename은 **발급된 ID의 이동**이라 옛 경로에 redirect 스텁을 남기고,
merge는 **검역에서 본 코퍼스로의 승격**이라 스텁을 남기지 않는다(inbox는 발행된
위치가 아니고, 애초에 `concept`만 허용하므로 스텁을 두면 validate가 깨진다).

같은 것은 "이 파일을 가리키던 링크와 경로를 전부 따라 고친다"이고, 그게 여기 있다.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .layout import QMD_SCHEME, Layout
from .mdfile import read
from .repo import ROOT, visible_files
from .rewrite import rewrite_frontmatter_path, rewrite_links

class RelocateError(Exception):
    """진행하면 손상이 남는 상황. 아무것도 건드리지 않고 멈춘다."""


@dataclass(frozen=True)
class Edit:
    path: Path
    text: str
    note: str


def href_to(referrer: Path, target: Path) -> str:
    """참조하는 파일에서 대상까지의 올바른 링크 형식.

    같은 KB면 파일 상대 경로, 다른 KB면 `qmd://` — 이동으로 KB 경계를 넘나들면
    링크 형식도 따라 바뀌어야 한다(PLAN §2.4).
    """
    if referrer.parts[0] == target.parts[0]:
        return os.path.relpath(target, referrer.parent)
    kb, *rest = target.parts
    return f"{QMD_SCHEME}{kb}/{Path(*rest)}"


def resolves_to(referrer: Path, href: str, target: Path) -> bool:
    """이 링크가 대상 파일을 가리키는가. 표기 형태(`./x.md`·`../a/../x.md`)에 흔들리지
    않게 경로로 정규화해 비교한다."""
    if href.startswith(QMD_SCHEME):
        return Path(href.removeprefix(QMD_SCHEME)) == target
    if "://" in href or href.startswith("#"):
        return False
    return os.path.normpath(referrer.parent / href.partition("#")[0]) == str(target)


def plan_edits(old: Path, new: Path) -> list[Edit]:
    """이동 때문에 고쳐야 할 파일 전부. 모호한 지점이 하나라도 있으면 전체를 중단한다 —
    부분 적용된 저장소가 가장 나쁘다."""
    edits: list[Edit] = []
    ambiguous: list[str] = []

    for relative in visible_files():
        if relative.suffix != ".md" or relative == old:
            continue

        text = (ROOT / relative).read_text()
        original, links = text, 0

        # 같은 대상을 `raft.md`·`./raft.md`처럼 여러 표기로 가리킬 수 있으므로
        # 표기별로 돌리고 합산한다.
        hrefs = {
            href for href in read(ROOT / relative, relative).links
            if resolves_to(relative, href, old)
        }
        for href in sorted(hrefs):
            result = rewrite_links(text, href, href_to(relative, new))
            if result.ambiguities:
                ambiguous += [
                    f"{relative}:{a.line} — 원문 {a.found}건 vs AST {a.expected}건"
                    for a in result.ambiguities
                ]
                continue
            text, links = result.text, links + result.changed

        notes = [f"링크 {links}건"] if links else []

        result = rewrite_frontmatter_path(text, f"/{old}", f"/{new}")
        if result.changed:
            text = result.text
            notes.append(f"frontmatter 경로 {result.changed}건")

        if text != original:
            edits.append(Edit(relative, text, ", ".join(notes)))

    if ambiguous:
        raise RelocateError(
            "링크 표기가 AST와 합의하지 않아 자동 재작성을 중단했습니다. 해당 줄을 손으로\n"
            "인라인 링크 형태로 고친 뒤 다시 실행하십시오 (참조형·제목 붙은 링크·꺾쇠\n"
            "목적지는 지원하지 않습니다):\n  " + "\n  ".join(ambiguous)
        )
    return edits


def check_unique(layout: Layout, new: Path, exclude: Path) -> None:
    """유일성 스코프는 KB다 — 다른 디렉터리에 같은 이름이 있으면 안 된다(PLAN §2.5-3)."""
    kb = new.parts[0]
    for other in visible_files():
        if (other != exclude and other.suffix == ".md" and other.stem == new.stem
                and other.parts[0] == kb and layout.content_dir_of(other)):
            raise RelocateError(f"{new.stem}: {kb} 안에 이미 있습니다 ({other})")


def apply(new: Path, content: str, edits: list[Edit]) -> None:
    """새 경로는 O_EXCL로 만든다 — check-then-write는 병렬 프로세스에서 덮어쓴다(§2.5-5)."""
    (ROOT / new).parent.mkdir(parents=True, exist_ok=True)
    with open(ROOT / new, "x", encoding="utf-8") as handle:
        handle.write(content)
    for edit in edits:
        (ROOT / edit.path).write_text(edit.text)

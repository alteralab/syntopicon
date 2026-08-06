"""schema/layout.yaml — 저장소 경계의 정본을 읽는다."""

from __future__ import annotations

from dataclasses import dataclass
from functools import cache
from pathlib import Path

import yaml

from .repo import ROOT, top_level_entries

LAYOUT_PATH = ROOT / "schema" / "layout.yaml"


@dataclass(frozen=True)
class Layout:
    shared_files: frozenset[str]
    shared_dirs: frozenset[str]
    typed_frontmatter: tuple[str, ...]
    marker_path: str
    marker_type: str
    sections: dict[str, str]
    dir_types: dict[str, tuple[str, ...]]
    dir_constraints: dict[str, dict]
    skeleton_dirs: tuple[str, ...]
    skeleton_files: dict[str, str]
    index_pattern: str
    index_ignore: tuple[str, ...]

    @property
    def shared_names(self) -> frozenset[str]:
        return self.shared_files | self.shared_dirs

    def kbs(self) -> tuple[str, ...]:
        """KB 인스턴스 = 마커 파일을 가진 루트 직하 디렉터리.

        레지스트리를 두지 않는다 — 파일시스템이 정본이다(PLAN §3).
        """
        return tuple(sorted(
            name for name in top_level_entries()
            if name not in self.shared_names and (ROOT / name / self.marker_path).is_file()
        ))

    def content_dir_of(self, relative: Path, kbs: tuple[str, ...] | None = None) -> str | None:
        """`<kb>/<dir>/...` 에서 <dir>를 돌려준다. KB 밖이면 None.

        kbs()는 매 호출이 git 서브프로세스다(의도 — 상태 함수는 현재를 답한다).
        **루프 안에서는 호출자가 kbs를 한 번 떠서 넘겨라** — 2천 파일 루프에서
        파일마다 서브프로세스를 부르면 247초가 된다(규모 스모크 실측).
        """
        parts = relative.parts
        members = self.kbs() if kbs is None else kbs
        if len(parts) >= 3 and parts[0] in members and parts[1] in self.dir_types:
            return parts[1]
        return None


@cache
def load() -> Layout:
    raw = yaml.safe_load(LAYOUT_PATH.read_text())
    shared, kb, index = raw["shared_assets"], raw["kb"], raw["index"]
    return Layout(
        shared_files=frozenset(shared["files"]),
        shared_dirs=frozenset(d.rstrip("/") for d in shared["dirs"]),
        typed_frontmatter=tuple(shared["typed_frontmatter"]),
        marker_path=kb["marker"]["path"],
        marker_type=kb["marker"]["type"],
        sections=dict(kb["sections"]),
        dir_types={d: tuple(g) for d, g in kb["dir_types"].items()},
        dir_constraints=dict(kb.get("dir_constraints", {})),
        skeleton_dirs=tuple(kb["skeleton"]["dirs"]),
        skeleton_files=dict(kb["skeleton"]["files"]),
        index_pattern=index["pattern"],
        index_ignore=tuple(index["ignore"]),
    )

"""schema/layout.yaml — 저장소 경계의 정본을 읽는다."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from .repo import ROOT, top_level_entries

LAYOUT_PATH = ROOT / "schema" / "layout.yaml"

#: 크로스 KB 링크 스킴(PLAN §2.4). KB 경계 문법이므로 경계의 정본인 이 모듈이
#: 소유한다 — 독립 정의 3벌(relocate·index_db·search)이 드리프트 위험으로
#: 실측돼 단일화했다(2026-08-13 상수 감사).
QMD_SCHEME = "qmd://"


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

    def require(self, name: str) -> None:
        """KB 존재 게이트 — 없으면 fail-loud. 도구 셋이 같은 문구의 사본을 들고
        있었고 하나는 목록도 안 보여줬다(2026-08-13 감사) — 단일 구현."""
        members = self.kbs()
        if name not in members:
            raise SystemExit(
                f"KB '{name}'가 없습니다 (있는 KB: {', '.join(members) or '없음'}). "
                "kb-new를 먼저 실행하십시오.")

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


def load() -> Layout:
    """layout.yaml을 읽어 Layout을 만든다 — 부를 때마다 현재를 읽는다.

    @cache를 두지 않는 이유는 repo.visible_files와 같은 결정이다: 상태를 묻는
    함수의 숨은 memoization은 무효화를 잊는 쪽으로만 틀리고(같은 stale 버그 2회),
    한 연산 안의 고정 스냅샷은 호출자가 결과를 들고 있으면 된다 — 실제로 모든
    도구가 main에서 한 번 떠서 인자로 내린다.
    """
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

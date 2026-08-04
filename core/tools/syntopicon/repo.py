"""저장소 위치와 git이 보는 파일 목록."""

from __future__ import annotations

import os
import subprocess
from functools import cache
from pathlib import Path

# tools/syntopicon/repo.py → 저장소 루트. resolve()가 심링크를 먼저 푼다 —
# 스킬은 ~/.claude/skills/ 심링크를 거쳐 tools/를 부르고, 그때 기준은
# 심링크 해석 후의 저장소 루트다(PLAN §4.3).
#
# SYNTOPICON_ROOT는 테스트 전용 seam이다. 운영에서는 쓰지 않는다 — 저장소 분리 시엔
# 그 저장소가 tools/ 시점 사본을 갖게 되므로(PLAN §4.5) 덮어쓸 이유가 없다.
ROOT = Path(os.environ.get("SYNTOPICON_ROOT") or Path(__file__).resolve().parents[2])


def _git(*args: str) -> list[str]:
    out = subprocess.run(
        ("git", "-C", str(ROOT), *args),
        capture_output=True, text=True, check=True,
    ).stdout
    return out.splitlines()


@cache
def visible_files() -> tuple[Path, ...]:
    """git이 무시하지 않는 파일 전부 — 추적 중 + 미추적.

    무엇이 저장소에 속하는지의 정본은 .gitignore다. layout.yaml에 무시 목록을
    다시 적으면 두 정본이 갈라진다.
    """
    return tuple(Path(p) for p in _git("ls-files", "-co", "--exclude-standard"))


def top_level_entries() -> set[str]:
    """루트 직하 항목 이름 — 완전 분할 검사의 좌변."""
    return {p.parts[0] for p in visible_files()}

"""저장소 위치와 git이 보는 파일 목록."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path

# tools/syntopicon/repo.py → 저장소 루트. resolve()가 심링크를 먼저 푼다 —
# 스킬은 ~/.claude/skills/ 심링크를 거쳐 tools/를 부르고, 그때 기준은
# 심링크 해석 후의 저장소 루트다(PLAN §4.3).
#
# SYNTOPICON_ROOT는 테스트 전용 seam이다. 운영에서는 쓰지 않는다 — 저장소 분리 시엔
# 그 저장소가 tools/ 시점 사본을 갖게 되므로(PLAN §4.5) 덮어쓸 이유가 없다.
ROOT = Path(os.environ.get("SYNTOPICON_ROOT") or Path(__file__).resolve().parents[2])


def _git_paths(*args: str) -> set[str]:
    """NUL 구분으로 받는다 — `-z` 없는 기본 출력은 사람용이라 비ASCII 경로를
    따옴표 + 8진 이스케이프로 망가뜨린다(core.quotePath). 한글 경로가 조용히
    사라지거나 엉뚱한 이름으로 보고되는 원인이 그것이었다."""
    out = subprocess.run(
        ("git", "-C", str(ROOT), *args, "-z"),
        capture_output=True, text=True, check=True,
    ).stdout
    return {name for name in out.split("\0") if name}


def visible_files() -> tuple[Path, ...]:
    """지금 디스크에 있는 저장소 파일 전부 — 추적 중 + 미추적, .gitignore 존중.

    무엇이 저장소에 속하는지의 정본은 .gitignore다. layout.yaml에 무시 목록을
    다시 적으면 두 정본이 갈라진다.

    **캐시하지 않는다.** 전에는 @cache + 변이 도구(kb-new·merge)의 수동 무효화였는데,
    새 변이 도구가 생길 때마다 무효화를 잊어 같은 stale 버그가 재발했다(두 번).
    상태를 묻는 함수는 물을 때마다 현재를 답하는 것이 맞고, git 한 번은 CLI 도구의
    호출 빈도에서 문제가 되지 않는다. 한 연산 안에서 고정된 스냅샷이 필요하면
    호출자가 결과 튜플을 들고 있으면 된다.

    `ls-files -c`는 인덱스를 보여 주므로 방금 지워지고 아직 스테이징되지 않은
    파일도 나열한다 — 그 집합은 git 자신이 `-d`(worktree에서 삭제됨)로 알려 주므로
    빼 준다. 파일마다 fs를 재확인(stat)하는 것보다 git의 자기 보고가 일관된다.
    """
    listed = _git_paths("ls-files", "-co", "--exclude-standard")
    deleted = _git_paths("ls-files", "-d")
    return tuple(sorted(Path(name) for name in listed - deleted))


def top_level_entries() -> set[str]:
    """루트 직하 항목 이름 — 완전 분할 검사의 좌변."""
    return {p.parts[0] for p in visible_files()}

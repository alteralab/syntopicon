"""저장소 위치, git이 보는 파일 목록, 다중 파일 쓰기 연산의 공통 가드."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from .workspace import DEFAULT

# 루트 발견의 정본은 workspace.Workspace.discover()다 — ROOT는 그 파생물로 남아
# 하위 호환을 유지한다(직수입 15파일). SYNTOPICON_ROOT는 테스트 전용 seam이다.
# 운영에서는 쓰지 않는다 — 저장소 분리 시엔 그 저장소가 tools/ 시점 사본을 갖게
# 되므로(PLAN §4.5) 덮어쓸 이유가 없다.
ROOT = DEFAULT.root


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


def added_at(relative: Path | str):
    """이 경로가 저장소에 (가장 최근에) 추가된 시점. 아직 커밋 전이면 지금.

    inbox 나이의 정본이다 — mtime은 checkout·rsync로 흔들리지만 추가 커밋은 불변이다.
    커밋 전 초안은 아직 어떤 런에도 속하지 않은 작업 중 파일이므로 나이 0이 맞다.

    `--follow` 금지 — 개정 초안은 본질적으로 concepts 쌍둥이와 닮았으므로 git의
    복사·개명 추적이 초안을 원본 페이지의 복사(C)로 읽고, 초안 자신의 착지 시점
    대신 **원본이 추가된 시점**을 돌려준다(테스트에서 실측). 같은 이유로 최신 추가
    커밋(재착지 시 가장 최근 것)을 쓴다 — 옛 동명 초안의 나이를 계승하면 갓 착지한
    초안이 P90 경보를 즉시 올린다.
    """
    from datetime import datetime, timezone
    out = subprocess.run(
        ("git", "-C", str(ROOT), "log", "--diff-filter=A", "--format=%aI",
         "--", str(relative)),
        capture_output=True, text=True).stdout.split()
    if out:
        return datetime.fromisoformat(out[0])
    return datetime.now(timezone.utc)


def top_level_entries() -> set[str]:
    """루트 직하 항목 이름 — 완전 분할 검사의 좌변."""
    return {p.parts[0] for p in visible_files()}


def ensure_clean_worktree(operation: str) -> None:
    """여러 파일을 한꺼번에 고치는 연산의 가드 (PLAN §2.5-7ⓔ) — 단일 구현.

    이 저장소의 트랜잭션 모델은 보상이다: 다중 파일 쓰기는 원자적이지 않지만
    깨끗한 트리에서만 실행하므로 실패 시 git으로 전량 되돌릴 수 있다. merge와
    rename이 사본을 따로 들고 verify는 가드가 없던 것이 2026-08-13 감사의 발견
    이고, 여기가 그 단일화다.
    """
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain"],
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        raise SystemExit(
            f"워킹 트리가 깨끗하지 않습니다. {operation}은 여러 파일을 한꺼번에 고치므로 "
            "되돌릴 수 있는 상태에서만 실행합니다 (PLAN §2.5-7ⓔ).")


def run_validate_gate() -> int:
    """사후 구조·링크 검사 게이트 — 다중 파일을 고친 도구의 마지막 단계(단일 구현).

    validate 실물은 **코드 기준**(__file__)으로 찾는다 — ROOT는 SYNTOPICON_ROOT
    seam으로 움직이는 검사 '대상' 저장소라, 샌드박스 저장소에는 tools/가 없다.
    """
    print(flush=True)   # 도구 자신의 출력과 validate 출력이 섞이지 않게 먼저 비운다
    validate = Path(__file__).resolve().parents[1] / "validate.py"
    return subprocess.run([sys.executable, str(validate)]).returncode

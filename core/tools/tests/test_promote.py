"""승급 사슬. 핵심은 셋 — 사슬이 실제로 이어지는가, 부분 실패가 침묵하지 않는가,
런 계측이 남는가."""

from __future__ import annotations

import json
import sqlite3

from conftest import Repo
from test_validate import DDIA, SOURCE, concept


def seeded(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/inbox/first-idea.md", concept(status="draft"))
    repo.commit()


def promote_events(repo: Repo) -> list[dict]:
    if not (repo.root / "stats.sqlite").exists():   # 조기 종료 경로 — 기록 자체가 없다
        return []
    with sqlite3.connect(repo.root / "stats.sqlite") as db:
        rows = db.execute(
            "SELECT payload FROM events WHERE kind = 'promote' ORDER BY rowid").fetchall()
    return [json.loads(payload) for payload, in rows]


def test_사슬이_승급부터_lint까지_돈다(repo: Repo):
    seeded(repo)
    result = repo.run("promote.py", "--kb", "it", "--skip-qmd")
    assert result.returncode == 0, result.stdout + result.stderr

    assert (repo.root / "it/concepts/first-idea.md").exists()
    assert not (repo.root / "it/inbox/first-idea.md").exists()
    assert (repo.root / "derived.sqlite").exists()          # reindex까지 이어짐
    assert "_progress.yaml" in result.stdout                 # 남은 사람 몫 안내

    event, = promote_events(repo)
    assert event["drafts"] == 1 and event["failed_stage"] is None
    assert set(event["stages_ms"]) == {"merge", "reindex", "lint"}
    assert event["qmd"] == "--skip-qmd"
    assert event["lint"] is not None                         # lint 결과 요약 동봉


def test_초안이_없으면_아무것도_하지_않는다(repo: Repo):
    repo.kb_new("it", "IT 지식", "설명")
    repo.commit()
    result = repo.run("promote.py", "--kb", "it", "--skip-qmd")
    assert result.returncode == 1
    assert "승급할 초안이 없습니다" in result.stderr
    assert promote_events(repo) == []


def test_중간_실패는_남은_단계를_말한다(repo: Repo):
    """워킹 트리가 더러우면 merge가 거부한다 — 사슬은 그 지점과 남은 단계를 밝히고
    실패 이벤트를 남겨야 한다. 부분 실패의 침묵이 이 도구가 막는 사고다."""
    seeded(repo)
    repo.write("it/concepts/uncommitted.md", concept())      # 커밋하지 않은 변경

    result = repo.run("promote.py", "--kb", "it", "--skip-qmd")
    assert result.returncode == 1
    assert "merge 단계가 종료 코드" in result.stderr
    assert "실행되지 않은 단계: reindex, lint" in result.stderr

    event, = promote_events(repo)
    assert event["failed_stage"] == "merge"


def test_dry_run은_계획만_말한다(repo: Repo):
    seeded(repo)
    result = repo.run("promote.py", "--kb", "it", "--dry-run", "--skip-qmd")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "first-idea" in result.stdout and "실행 계획" in result.stdout
    assert (repo.root / "it/inbox/first-idea.md").exists()
    assert promote_events(repo) == []

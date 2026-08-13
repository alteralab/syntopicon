"""verified 승급. 신뢰 사다리의 마지막 칸이라 거짓 스탬프가 가장 나쁘다 — 거부 경로 먼저."""

from __future__ import annotations

import yaml

from conftest import Repo
from test_validate import DDIA, SOURCE, concept


def seeded(repo: Repo) -> None:
    repo.seed_it()
    repo.write("it/concepts/checked-page.md", concept())
    repo.write("it/inbox/draft-page.md", concept(status="draft"))


def frontmatter(repo: Repo, path: str) -> dict:
    text = repo.read(path)
    return yaml.safe_load(text.split("---\n")[1])


def test_스탬프를_추가하고_validate를_통과한다(repo: Repo):
    seeded(repo)
    result = repo.run("verify.py", "it/concepts/checked-page.md")
    assert result.returncode == 0, result.stdout + result.stderr

    front = frontmatter(repo, "it/concepts/checked-page.md")
    assert len(front["verified"]) == 1
    assert front["verified"][0]["by"] == "human:me"
    assert "T" in front["verified"][0]["at"] and front["verified"][0]["at"].endswith("Z")


def test_본문과_다른_frontmatter는_건드리지_않는다(repo: Repo):
    """라운드트립 금지의 실효 검사 — 스탬프 줄 밖은 바이트 단위로 동일해야 한다."""
    seeded(repo)
    before = repo.read("it/concepts/checked-page.md")
    repo.run("verify.py", "it/concepts/checked-page.md")
    after = repo.read("it/concepts/checked-page.md")

    changed = set(after.splitlines()) - set(before.splitlines())
    assert len(changed) == 1 and next(iter(changed)).startswith("verified:")


def test_재검증은_이력으로_쌓인다(repo: Repo):
    seeded(repo)
    repo.run("verify.py", "it/concepts/checked-page.md")
    result = repo.run("verify.py", "it/concepts/checked-page.md", "--by", "claude-opus-5")
    assert result.returncode == 0, result.stderr

    stamps = frontmatter(repo, "it/concepts/checked-page.md")["verified"]
    assert [s["by"] for s in stamps] == ["human:me", "claude-opus-5"]


def test_inbox_초안은_거부한다(repo: Repo):
    """unreviewed를 건너뛰고 verified가 되는 사다리 우회는 없다."""
    seeded(repo)
    result = repo.run("verify.py", "it/inbox/draft-page.md")
    assert result.returncode == 1 and "merge.py를 먼저" in result.stderr
    assert "verified" not in repo.read("it/inbox/draft-page.md")


def test_소스_메타는_거부한다(repo: Repo):
    seeded(repo)
    result = repo.run("verify.py", f"it/sources/{DDIA}.md")
    assert result.returncode == 1 and "verified 계층이 없습니다" in result.stderr


def test_dry_run은_쓰지_않는다(repo: Repo):
    seeded(repo)
    result = repo.run("verify.py", "it/concepts/checked-page.md", "--dry-run")
    assert result.returncode == 0
    assert "verified" not in repo.read("it/concepts/checked-page.md")

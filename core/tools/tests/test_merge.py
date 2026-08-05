"""검역 해제. rename과 다른 연산이라는 점(스텁 없음)이 핵심이라 거기를 집중해 본다."""

from __future__ import annotations

from conftest import Repo
from test_validate import DDIA, SOURCE, concept


def seeded(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/inbox/first-idea.md", concept(status="draft"))
    repo.write("it/inbox/second-idea.md", concept(status="draft"))
    repo.commit()


def test_초안을_승격하고_draft를_지운다(repo: Repo):
    seeded(repo)
    result = repo.run("merge.py", "it/inbox/first-idea.md")
    assert result.returncode == 0, result.stdout + result.stderr

    merged = repo.read("it/concepts/first-idea.md")
    assert "status: draft" not in merged
    assert "type: concept" in merged and "title:" in merged
    assert repo.validate().returncode == 0


def test_스텁을_남기지_않는다(repo: Repo):
    """inbox는 발행된 위치가 아니고, dir_types상 concept만 허용하므로 redirect 스텁을
    두면 validate가 깨진다 — rename과 갈리는 지점이다."""
    seeded(repo)
    repo.run("merge.py", "it/inbox/first-idea.md")
    assert not (repo.root / "it/inbox/first-idea.md").exists()
    assert repo.validate().returncode == 0


def test_status를_stable로_바꾸지_않는다(repo: Repo):
    """부재 = 기본값이므로 기본값을 명시하는 것은 금지다(PLAN §2.1)."""
    seeded(repo)
    repo.run("merge.py", "it/inbox/first-idea.md")
    assert "status:" not in repo.read("it/concepts/first-idea.md")


def test_verified를_붙이지_않는다(repo: Repo):
    """승격은 unverified 계층으로 간다 — 리뷰 기준은 무해성·구조이지 전수 정확성이
    아니고, 정확성은 review-on-read가 담당한다."""
    seeded(repo)
    repo.run("merge.py", "it/inbox/first-idea.md")
    assert "verified" not in repo.read("it/concepts/first-idea.md")


def test_가리키던_링크를_따라_고친다(repo: Repo):
    seeded(repo)
    repo.write("it/concepts/hub-ish.md",
               concept(body="\n- [초안](../inbox/first-idea.md)\n"))
    repo.commit()

    assert repo.run("merge.py", "it/inbox/first-idea.md").returncode == 0
    body = repo.read("it/concepts/hub-ish.md")
    assert "](first-idea.md)" in body and "inbox" not in body


def test_all로_한_KB를_비운다(repo: Repo):
    seeded(repo)
    result = repo.run("merge.py", "--kb", "it", "--all")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "2개 승격" in result.stdout
    assert not list((repo.root / "it/inbox").glob("*.md"))


def test_inbox_밖의_파일을_거부한다(repo: Repo):
    seeded(repo)
    repo.run("merge.py", "it/inbox/first-idea.md")
    repo.commit()
    result = repo.run("merge.py", "it/concepts/first-idea.md")
    assert result.returncode == 1 and "inbox/의 파일이 아닙니다" in result.stderr


def test_이름이_이미_있으면_거부한다(repo: Repo):
    seeded(repo)
    repo.write("it/concepts/first-idea.md", concept())
    repo.commit()
    result = repo.run("merge.py", "it/inbox/first-idea.md")
    assert result.returncode == 1 and "이미 존재합니다" in result.stderr


def test_워킹_트리가_더러우면_거부한다(repo: Repo):
    seeded(repo)
    repo.write("it/inbox/third-idea.md", concept(status="draft"))
    result = repo.run("merge.py", "it/inbox/first-idea.md")
    assert result.returncode == 1 and "깨끗하지 않습니다" in result.stderr


def test_dry_run은_아무것도_옮기지_않는다(repo: Repo):
    seeded(repo)
    result = repo.run("merge.py", "--kb", "it", "--all", "--dry-run")
    assert result.returncode == 0 and "아무것도 쓰지 않았습니다" in result.stdout
    assert (repo.root / "it/inbox/first-idea.md").exists()
    assert not (repo.root / "it/concepts").exists() or \
        not list((repo.root / "it/concepts").glob("*.md"))

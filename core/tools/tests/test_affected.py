"""영향 범위 조회. 놓친 파일 하나가 곧 O(N) 마이그레이션의 구멍이라 누락을 집중 확인한다."""

from __future__ import annotations

from conftest import Repo
from test_validate import DDIA, SOURCE, concept, page


def seeded(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")
    repo.kb_new("ops", "운영", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/fresh.md", concept())
    repo.write("it/concepts/expiring.md", concept(stale_after="2027-01-01"))
    repo.write("it/inbox/draft-one.md", concept(status="draft"))
    repo.write("ops/sources/kleppmann2017-ddia.md", SOURCE)
    repo.write("ops/concepts/also-expiring.md", concept(
        stale_after="2028-01-01").replace("/it/sources/", "/ops/sources/"))
    repo.run("reindex.py")


def test_필드를_가진_파일만_KB별로_집계한다(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "field", "stale_after")
    assert result.returncode == 0
    assert "it/concepts/expiring.md" in result.stdout
    assert "ops/concepts/also-expiring.md" in result.stdout
    assert "it/concepts/fresh.md" not in result.stdout
    assert "2개 파일 · KB별: it 1, ops 1" in result.stdout


def test_값까지_보여준다(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "field", "stale_after")
    assert '"2027-01-01"' in result.stdout


def test_KB로_좁힌다(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "field", "stale_after", "--kb", "it")
    assert "ops/concepts/also-expiring.md" not in result.stdout
    assert "1개 파일 · KB별: it 1" in result.stdout


def test_type_축(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "type", "book")
    assert "2개 파일 · KB별: it 1, ops 1" in result.stdout


def test_디렉터리_축(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "dir", "inbox")
    assert "it/inbox/draft-one.md" in result.stdout and "1개 파일" in result.stdout


def test_스키마에_없는_키는_주의를_준다(repo: Repo):
    seeded(repo)
    result = repo.run("affected.py", "field", "as_of")
    assert "현재 스키마에 선언돼 있지 않습니다" in result.stdout
    assert "0개 파일" in result.stdout


def test_재색인_없이는_거부한다(repo: Repo):
    repo.kb_new("it", "IT 지식", "설명")
    result = repo.run("affected.py", "field", "type")
    assert result.returncode == 1 and "파생 인덱스가 없습니다" in result.stderr

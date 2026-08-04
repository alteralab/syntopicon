"""메타 테이블과 edges. 파생물이라 틀려도 조용하다 — 그래서 값을 직접 확인한다."""

from __future__ import annotations

import sqlite3

from conftest import Repo
from test_validate import DDIA, SOURCE, concept, page


def graph(repo: Repo) -> None:
    """raft ← consensus → replication, synthesis 허브가 셋 다 가리키는 작은 그래프."""
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/raft.md", concept())
    repo.write("it/concepts/replication.md", concept())
    repo.write("it/concepts/consensus.md", concept(
        body="\n- [라프트](raft.md)\n- [복제](replication.md)\n- [외부](https://example.com)\n"
             "- [없는 곳](missing.md)\n"))
    repo.write("it/synthesis/distributed.md", page({
        "type": "synthesis", "title": "분산", "description": "허브",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"},
    }, body="\n- [합의](../concepts/consensus.md)\n- [라프트](../concepts/raft.md)\n"))
    repo.write("it/inbox/pending-idea.md", concept(status="draft"))


def rows(repo: Repo, sql: str, *params) -> list[sqlite3.Row]:
    connection = sqlite3.connect(repo.root / "derived.sqlite")
    connection.row_factory = sqlite3.Row
    with connection:
        return connection.execute(sql, params).fetchall()


def test_메타_테이블이_필터_필드를_실컬럼으로_담는다(repo: Repo):
    graph(repo)
    assert repo.run("reindex.py").returncode == 0

    raft = rows(repo, "SELECT * FROM files WHERE path = ?", "it/concepts/raft.md")[0]
    assert (raft["kb"], raft["directory"], raft["type"]) == ("it", "concepts", "concept")
    assert raft["status"] is None            # 부재 = stable
    assert raft["unreviewed"] == 0
    assert len(raft["sha256"]) == 64

    source = rows(repo, "SELECT * FROM files WHERE path = ?", f"it/sources/{DDIA}.md")[0]
    assert source["type"] == "book"          # CSL 타입군도 그대로


def test_inbox_미검토를_표시한다(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    # `[unreviewed]` = inbox 경로 + verified 부재 (PLAN §3) — 경로에서 파생되는 축이다.
    flagged = [r["path"] for r in rows(repo, "SELECT path FROM files WHERE unreviewed = 1")]
    assert flagged == ["it/inbox/pending-idea.md"]


def test_인덱스를_만들지_않는다(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    created = [r["name"] for r in rows(
        repo, "SELECT name FROM sqlite_master WHERE type='index' AND sql IS NOT NULL")]
    assert created == [], f"명시적 인덱스가 생겼습니다: {created} (PLAN §4.1 무인덱스 시작)"


def test_외부_링크는_간선이_아니고_깨진_링크는_미해결로_남는다(repo: Repo):
    graph(repo)
    result = repo.run("reindex.py")
    assert "미해결 1" in result.stdout, result.stdout

    dsts = [r["dst"] for r in rows(repo, "SELECT dst FROM edges WHERE src = ?",
                                   "it/concepts/consensus.md")]
    assert "https://example.com" not in dsts
    assert sorted(dsts) == ["it/concepts/missing.md", "it/concepts/raft.md",
                            "it/concepts/replication.md"]
    assert rows(repo, "SELECT resolved FROM edges WHERE dst = ?",
                "it/concepts/missing.md")[0]["resolved"] == 0


def test_backlinks(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    result = repo.run("edges.py", "backlinks", "it/concepts/raft.md")
    assert result.returncode == 0
    assert "it/concepts/consensus.md" in result.stdout
    assert "it/synthesis/distributed.md" in result.stdout
    assert "2건" in result.stdout


def test_neighbors는_방향을_무시하고_깊이를_센다(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    result = repo.run("edges.py", "neighbors", "it/concepts/raft.md", "--depth", "2")
    assert result.returncode == 0
    # raft ← consensus (1홉), consensus → replication (2홉)
    assert "1홉  it/concepts/consensus.md" in result.stdout
    assert "2홉  it/concepts/replication.md" in result.stdout


def test_탐색_깊이_상한을_강제한다(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    result = repo.run("edges.py", "neighbors", "it/concepts/raft.md", "--depth", "5")
    assert result.returncode == 1 and "1–4입니다" in result.stderr


def test_링크_차수가_허브_후보를_낸다(repo: Repo):
    graph(repo)
    repo.run("reindex.py")
    result = repo.run("edges.py", "degree", "--kb", "it", "--top", "3")
    assert result.returncode == 0
    assert result.stdout.splitlines()[0].strip().startswith("2  it/concepts/raft.md")


def test_KB가_없으면_재색인을_거부한다(repo: Repo):
    result = repo.run("reindex.py")
    assert result.returncode == 1 and "KB가 없습니다" in result.stderr


def test_재색인은_직렬화된다(repo: Repo):
    graph(repo)
    (repo.root / "derived.sqlite.lock").write_text("99999")
    result = repo.run("reindex.py")
    assert result.returncode == 1 and "이미 실행 중입니다" in result.stderr

"""rename은 여러 파일을 한꺼번에 고친다 — 부분 적용이 가장 나쁘므로 중단 경로를 집중 검증한다."""

from __future__ import annotations

from conftest import Repo
from test_validate import DDIA, SOURCE, concept, page


def seeded(repo: Repo, *, second_kb: bool = False) -> None:
    repo.kb("it")
    if second_kb:
        repo.kb("ops")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    repo.write("it/concepts/raft.md", concept(body="\n합의 알고리즘.\n"))
    repo.write("it/concepts/consensus.md", concept(
        body="\n- 자세히는 [라프트](raft.md) 참조.\n- 같은 줄에 [둘](./raft.md).\n"))
    repo.write("it/synthesis/distributed.md", page({
        "type": "synthesis", "title": "분산 시스템", "description": "허브",
        "generated": {"by": "human:me", "at": "2026-08-05T00:00:00Z"},
    }, body="\n- [라프트](../concepts/raft.md)\n"))
    repo.commit()


def test_같은_KB_개명은_링크와_스텁을_한번에_처리한다(repo: Repo):
    seeded(repo)
    result = repo.rename("it/concepts/raft.md", "it/concepts/raft-consensus.md")
    assert result.returncode == 0, result.stdout + result.stderr

    assert "raft-consensus.md" in repo.read("it/concepts/consensus.md")
    assert "](raft.md)" not in repo.read("it/concepts/consensus.md")
    assert "](../concepts/raft-consensus.md)" in repo.read("it/synthesis/distributed.md")

    stub = repo.read("it/concepts/raft.md")
    assert "type: redirect" in stub
    assert "superseded_by: raft-consensus" in stub
    assert repo.validate().returncode == 0


def test_KB_간_이동은_링크_형식을_바꾸고_정규형을_남긴다(repo: Repo):
    seeded(repo, second_kb=True)
    result = repo.rename("it/concepts/raft.md", "ops/concepts/raft.md")
    assert result.returncode == 0, result.stdout + result.stderr

    # 같은 KB 안이던 링크가 KB 경계를 넘게 됐으므로 qmd:// 형식이 된다(PLAN §2.4).
    assert "qmd://ops/concepts/raft.md" in repo.read("it/concepts/consensus.md")
    # KB 간 이동 잔여물만 정규형 `<kb>/<이름>`을 쓴다(PLAN §2.1).
    assert "superseded_by: ops/raft" in repo.read("it/concepts/raft.md")


def test_frontmatter_경로도_따라간다(repo: Repo):
    seeded(repo, second_kb=True)
    assert repo.rename(f"it/sources/{DDIA}.md", f"ops/sources/{DDIA}.md").returncode == 0
    assert f"/ops/sources/{DDIA}.md" in repo.read("it/concepts/raft.md")


def test_모호한_링크가_있으면_아무것도_고치지_않는다(repo: Repo):
    seeded(repo)
    repo.write("it/concepts/tricky.md", concept(
        body="\n참조형 [라프트][r] 링크.\n\n[r]: raft.md\n"))
    repo.commit()
    before = repo.read("it/concepts/consensus.md")

    result = repo.rename("it/concepts/raft.md", "it/concepts/raft-consensus.md")
    assert result.returncode == 1
    assert "AST와 합의하지 않아" in result.stderr
    assert repo.read("it/concepts/consensus.md") == before      # 다른 파일도 무사
    assert not (repo.root / "it/concepts/raft-consensus.md").exists()
    assert "type: concept" in repo.read("it/concepts/raft.md")  # 스텁으로 덮이지 않았다


def test_대상이_이미_있으면_거부한다(repo: Repo):
    seeded(repo)
    result = repo.rename("it/concepts/raft.md", "it/concepts/consensus.md")
    assert result.returncode == 1 and "이미 존재합니다" in result.stderr


def test_ID_규칙을_어기는_이름을_거부한다(repo: Repo):
    seeded(repo)
    result = repo.rename("it/concepts/raft.md", "it/concepts/raft-2.md")   # 숫자 접미
    assert result.returncode == 1 and "slug 규칙 위반" in result.stderr


def test_계층을_넘는_이동을_거부한다(repo: Repo):
    seeded(repo)
    result = repo.rename("it/concepts/raft.md", "it/synthesis/raft.md")
    assert result.returncode == 1 and "type 변경을 뜻하므로" in result.stderr


def test_워킹_트리가_더러우면_거부한다(repo: Repo):
    seeded(repo)
    repo.write("it/concepts/raft.md", concept(body="\n커밋하지 않은 수정.\n"))
    result = repo.rename("it/concepts/raft.md", "it/concepts/raft-consensus.md")
    assert result.returncode == 1 and "깨끗하지 않습니다" in result.stderr


def test_dry_run은_아무것도_쓰지_않는다(repo: Repo):
    seeded(repo)
    before = repo.read("it/concepts/consensus.md")
    result = repo.rename("it/concepts/raft.md", "it/concepts/raft-consensus.md", "--dry-run")
    assert result.returncode == 0
    assert "링크 2건" in result.stdout
    assert repo.read("it/concepts/consensus.md") == before
    assert not (repo.root / "it/concepts/raft-consensus.md").exists()

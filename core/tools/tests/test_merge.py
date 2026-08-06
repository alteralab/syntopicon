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


def test_같은_슬러그가_concepts에_있으면_개정판_대치다(repo: Repo):
    """"기존 페이지 갱신이 본체"(PLAN §4.4-4)인데 갱신도 검역을 지나야 하므로,
    concepts에 같은 슬러그가 있는 초안은 충돌이 아니라 개정 대기다."""
    seeded(repo)
    repo.write("it/concepts/first-idea.md", concept(body="\n- 낡은 주장.\n"))
    repo.commit()

    result = repo.run("merge.py", "it/inbox/first-idea.md")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "개정판 대치" in result.stdout

    merged = repo.read("it/concepts/first-idea.md")
    assert "낡은 주장" not in merged and "status: draft" not in merged
    assert not (repo.root / "it/inbox/first-idea.md").exists()
    assert repo.validate().returncode == 0


def test_개정_초안이_복사해_온_verified도_벗긴다(repo: Repo):
    """검역 통과는 무해성·구조 리뷰지 정확성 검증이 아니다 — 원본에서 딸려 온
    verified 스탬프는 대치되기 전 내용에 대한 증언이므로 승격이 계승하면 안 된다."""
    seeded(repo)
    repo.write("it/concepts/first-idea.md", concept())
    repo.write("it/inbox/first-idea.md", concept(
        status="draft", verified=[{"by": "human:me", "at": "2026-08-01T00:00:00Z"}]))
    repo.commit()

    assert repo.run("merge.py", "it/inbox/first-idea.md").returncode == 0
    assert "verified" not in repo.read("it/concepts/first-idea.md")


def test_워킹_트리가_더러우면_거부한다(repo: Repo):
    seeded(repo)
    repo.write("it/inbox/third-idea.md", concept(status="draft"))
    result = repo.run("merge.py", "it/inbox/first-idea.md")
    assert result.returncode == 1 and "깨끗하지 않습니다" in result.stderr


# ── 나이 기반 자동 머지 (PLAN §4.4 쓰기 정책 ②, [실험]) ──────────────────────

def commit_dated(repo: Repo, date: str) -> None:
    """저자 시각을 박아 커밋한다 — added_at(%aI)이 읽는 축이 저자 시각이다."""
    repo._git("add", "-A")
    repo._git("-c", "user.email=t@t", "-c", "user.name=t",
              "commit", "-qm", "fixture", f"--date={date}")


def test_auto는_min_age_days와_함께만_돈다(repo: Repo):
    """N의 기본값은 없다 — 수용 검증에서 확정하기로 한 상수를 코드가 선점하면 안 된다."""
    seeded(repo)
    result = repo.run("merge.py", "--kb", "it", "--auto")
    assert result.returncode == 1 and "함께 씁니다" in result.stderr


def test_auto는_나이가_찬_가산_개정만_승격한다(repo: Repo):
    repo.kb_new("it", "IT 지식", "설명")
    repo.write(f"it/sources/{DDIA}.md", SOURCE)
    old_body = "\n- 기존 주장.\n"
    repo.write("it/concepts/additive.md", concept(body=old_body))
    repo.write("it/concepts/rewritten.md", concept(body=old_body))
    repo.commit()

    # 나이가 찬 초안 셋: 가산 개정 / 비가산 개정 / 신규 페이지
    repo.write("it/inbox/additive.md", concept(status="draft", body=old_body + "- 새 주장.\n"))
    repo.write("it/inbox/rewritten.md", concept(status="draft", body="\n- 고쳐 쓴 주장.\n"))
    repo.write("it/inbox/brand-new.md", concept(status="draft"))
    commit_dated(repo, "2026-06-01T00:00:00+00:00")

    # 어린 가산 개정 — 나이 미달로 보류돼야 한다
    repo.write("it/inbox/additive-young.md", concept(status="draft", body=old_body))
    repo.write("it/concepts/additive-young.md", concept(body=old_body))
    repo.commit()

    result = repo.run("merge.py", "--kb", "it", "--auto", "--min-age-days", "14")
    assert result.returncode == 0, result.stdout + result.stderr
    assert "1개 승격" in result.stdout
    assert "신규 페이지" in result.stdout and "비가산 개정" in result.stdout
    assert "나이" in result.stdout                      # additive-young 보류 사유
    assert "새 주장" in repo.read("it/concepts/additive.md")
    assert (repo.root / "it/inbox/rewritten.md").exists()
    assert (repo.root / "it/inbox/brand-new.md").exists()
    assert (repo.root / "it/inbox/additive-young.md").exists()


def test_dry_run은_아무것도_옮기지_않는다(repo: Repo):
    seeded(repo)
    result = repo.run("merge.py", "--kb", "it", "--all", "--dry-run")
    assert result.returncode == 0 and "아무것도 쓰지 않았습니다" in result.stdout
    assert (repo.root / "it/inbox/first-idea.md").exists()
    assert not (repo.root / "it/concepts").exists() or \
        not list((repo.root / "it/concepts").glob("*.md"))

"""스냅샷과 citekey — ingest에서 소급 불가능한 두 단계라 실패 경로를 먼저 본다."""

from __future__ import annotations

import hashlib

from conftest import Repo


def kb(repo: Repo) -> None:
    repo.kb_new("it", "IT 지식", "설명")


# ── snapshot ─────────────────────────────────────────────────────────────────

def test_파일을_보존하고_다이제스트를_낸다(repo: Repo, tmp_path):
    kb(repo)
    source = tmp_path / "ch5.txt"
    source.write_text("원문")

    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))
    assert result.returncode == 0, result.stderr

    manifest = f"{hashlib.sha256('원문'.encode()).hexdigest()}  ch5.txt\n"
    expected = hashlib.sha256(manifest.encode()).hexdigest()
    assert f'snapshot_sha256: "{expected}"' in result.stdout
    assert "snapshot: /it/archive/k2017-ddia/" in result.stdout
    assert (repo.root / "it/archive/k2017-ddia/ch5.txt").read_text() == "원문"


def test_기존_스냅샷을_덮어쓰지_않는다(repo: Repo, tmp_path):
    kb(repo)
    source = tmp_path / "a.txt"
    source.write_text("첫 판")
    repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))

    source.write_text("다른 판")
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-ddia", str(source))
    assert result.returncode == 1 and "write-once" in result.stderr
    assert (repo.root / "it/archive/k2017-ddia/a.txt").read_text() == "첫 판"


def test_KB가_없으면_거부한다(repo: Repo, tmp_path):
    source = tmp_path / "a.txt"
    source.write_text("x")
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-x", str(source))
    assert result.returncode == 1 and "KB 'it'가 없습니다" in result.stderr


def test_보존할_것이_없으면_거부한다(repo: Repo):
    kb(repo)
    result = repo.run("snapshot.py", "--kb", "it", "--citekey", "k2017-x")
    assert result.returncode == 1 and "필요합니다" in result.stderr


# ── citekey ──────────────────────────────────────────────────────────────────

def test_결정적_규칙으로_발급한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "Martin Kleppmann",
                      "--year", "2017", "--slug", "ddia")
    assert result.returncode == 0, result.stderr
    assert "발급  kleppmann2017-ddia" in result.stdout
    assert (repo.root / "it/sources/kleppmann2017-ddia.md").is_file()


def test_충돌은_숫자_접미로만_푼다(repo: Repo):
    kb(repo)
    for _ in range(2):
        repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    assert (repo.root / "it/sources/ongaro2014.md").is_file()
    assert (repo.root / "it/sources/ongaro2014-2.md").is_file()


def test_두번째_발급은_접미를_알린다(repo: Repo):
    kb(repo)
    repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    result = repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014")
    assert "접미가 붙었습니다" in result.stdout


def test_한국어_저자는_로마자_표기를_요구한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "홍길동", "--year", "2024")
    assert result.returncode == 1 and "--romanized" in result.stderr
    assert not (repo.root / "it/sources/2024.md").exists(), "연도만 남은 키가 예약됐습니다"

    result = repo.run("citekey.py", "--kb", "it", "--author", "홍길동",
                      "--romanized", "hong", "--year", "2024")
    assert result.returncode == 0 and "발급  hong2024" in result.stdout


def test_CSL_타입군_밖의_type을_거부한다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "X", "--year", "2020",
                      "--type", "tweet")
    assert result.returncode == 1 and "CSL 타입군에 없습니다" in result.stderr


def test_발급한_씨앗은_validate를_통과한다(repo: Repo):
    kb(repo)
    repo.run("citekey.py", "--kb", "it", "--author", "Ongaro", "--year", "2014",
             "--type", "paper-conference", "--title", "In Search of Consensus")
    result = repo.validate()
    assert result.returncode == 0, result.stdout


def test_dry_run은_예약하지_않는다(repo: Repo):
    kb(repo)
    result = repo.run("citekey.py", "--kb", "it", "--author", "Ongaro",
                      "--year", "2014", "--dry-run")
    assert result.returncode == 0 and "ongaro2014" in result.stdout
    assert not (repo.root / "it/sources/ongaro2014.md").exists()

"""kb-new는 KB의 유일한 생성 경로다 — 여기서 새는 경계는 어디서도 못 막는다."""

from __future__ import annotations

import yaml

from conftest import Repo


def qmd_collections(repo: Repo) -> dict:
    config = repo.qmd_config_dir / "index.yml"
    return yaml.safe_load(config.read_text())["collections"] if config.is_file() else {}


def test_골격과_라우터와_컬렉션을_한번에_만든다(repo: Repo):
    result = repo.kb_new("it", "IT 지식", "서적·논문·기술 문서")
    assert result.returncode == 0, result.stdout + result.stderr

    for directory in ("sources", "concepts", "synthesis", "inbox", "archive"):
        assert (repo.root / "it" / directory).is_dir(), directory
    assert "type: guide" in repo.read("it/overview.md")
    assert "## Hubs" in repo.read("it/overview.md")

    router = repo.read("overview.md")
    assert "[IT 지식](it/overview.md) — 서적·논문·기술 문서" in router
    assert "아직 없다" not in router

    collection = qmd_collections(repo)["it"]
    assert collection["path"] == str(repo.root / "it")
    assert collection["pattern"] == "**/*.md"
    assert collection["ignore"] == ["archive/**"]   # CLI에 --ignore가 없어 직접 쓴 값


def test_생성_결과는_validate를_통과한다(repo: Repo):
    assert repo.kb_new("it", "IT 지식", "설명").returncode == 0
    result = repo.validate()
    assert result.returncode == 0, result.stdout
    assert "KB 1개 (it)" in result.stdout


def test_두번째_KB도_라우터에_누적된다(repo: Repo):
    repo.kb_new("it", "IT 지식", "첫째")
    repo.kb_new("ops", "운영", "둘째")
    router = repo.read("overview.md")
    assert "[IT 지식](it/overview.md)" in router and "[운영](ops/overview.md)" in router


def test_이름_규칙을_어기면_거부한다(repo: Repo):
    for bad in ("IT", "2024-it", "it_kb"):
        result = repo.kb_new(bad, "제목", "설명")
        assert result.returncode == 1, f"{bad}가 통과했습니다"
        assert "KB 이름" in result.stderr
        assert not (repo.root / bad).exists()


def test_공유_자산_이름을_거부한다(repo: Repo):
    result = repo.kb_new("schema", "제목", "설명")
    assert result.returncode == 1 and "공유 자산 이름" in result.stderr


def test_비어있지_않은_디렉터리를_거부한다(repo: Repo):
    repo.write("it/기존파일.md", "# 뭔가 이미 있다\n")
    result = repo.kb_new("it", "제목", "설명")
    assert result.returncode == 1 and "비어 있지 않습니다" in result.stderr


def test_다른_경로를_가리키는_동명_컬렉션을_거부한다(repo: Repo):
    config = repo.qmd_config_dir / "index.yml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(yaml.safe_dump(
        {"collections": {"it": {"path": "/somewhere/else", "pattern": "**/*.md"}}}))

    result = repo.kb_new("it", "제목", "설명")
    assert result.returncode == 1
    assert "이미 다른 경로를 가리킵니다" in result.stderr
    assert qmd_collections(repo)["it"]["path"] == "/somewhere/else"   # 남의 설정 무손상


def test_기존_컬렉션은_보존한다(repo: Repo):
    config = repo.qmd_config_dir / "index.yml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text(yaml.safe_dump(
        {"collections": {"wiki": {"path": "/vault/wiki", "pattern": "**/*.md"}}}))

    assert repo.kb_new("it", "IT 지식", "설명").returncode == 0
    collections = qmd_collections(repo)
    assert collections["wiki"]["path"] == "/vault/wiki"
    assert "it" in collections


def test_dry_run은_아무것도_만들지_않는다(repo: Repo):
    result = repo.kb_new("it", "IT 지식", "설명", "--dry-run")
    assert result.returncode == 0 and "아무것도 쓰지 않았습니다" in result.stdout
    assert not (repo.root / "it").exists()
    assert "아직 없다" in repo.read("overview.md")

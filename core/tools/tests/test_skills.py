"""스킬 본문의 구조 규약 (agentskills.io 코어 스펙 + PLAN §4.3).

공식 검증기 `skills-ref validate`가 있지만 그것은 uv tool로 따로 설치된다 —
규약 검사가 그 설치 여부에 묶이면 안 되므로 여기서는 파일만 본다. 스펙 준수의
최종 확인은 `skills-ref validate .agents/skills/<이름>`이다.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

SKILLS_DIR = Path(__file__).resolve().parents[2] / ".agents" / "skills"
SKILLS = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())

# 코어 스펙: name/description 필수, 나머지는 선택. 확장 필드는 쓰지 않는다(PLAN §4.3).
CORE_FIELDS = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def frontmatter(skill: Path) -> dict:
    text = (skill / "SKILL.md").read_text()
    assert text.startswith("---\n"), f"{skill.name}: frontmatter 없음"
    return yaml.safe_load(text.split("---\n", 2)[1])


def test_다섯_종류가_다_있다():
    assert {p.name for p in SKILLS} == {"kb-query", "kb-ingest", "kb-lint", "kb-new", "kb-plain"}


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_name은_디렉터리명과_같고_문자집합을_지킨다(skill: Path):
    name = frontmatter(skill)["name"]
    assert name == skill.name
    assert 1 <= len(name) <= 64
    assert name.replace("-", "").isalnum() and name.islower()
    assert not name.startswith("-") and not name.endswith("-") and "--" not in name


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_description은_무엇과_언제를_담는다(skill: Path):
    description = frontmatter(skill)["description"]
    assert 1 <= len(description) <= 1024
    # 스펙 권고: 무엇을 하는지 + 언제 쓰는지. 후자가 없으면 에이전트가 발동 못 한다.
    assert "때" in description, f"{skill.name}: 사용 시점이 description에 없다"


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_코어_스펙_밖의_필드를_쓰지_않는다(skill: Path):
    extra = set(frontmatter(skill)) - CORE_FIELDS
    assert not extra, f"{skill.name}: 코어 스펙 밖 필드 {extra}"


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_본문이_500줄_아래다(skill: Path):
    """활성화되면 통째로 로드된다 — 상시가 아니라 온디맨드지만 상한은 있다."""
    lines = len((skill / "SKILL.md").read_text().splitlines())
    assert lines < 500, f"{skill.name}: {lines}줄"


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_저장소에_심링크를_커밋하지_않는다(skill: Path):
    """홈 디렉터리 심링크는 무관하지만, 커밋된 심링크는 Windows 클론을 깨뜨린다."""
    for path in skill.rglob("*"):
        assert not path.is_symlink(), f"{skill.name}: {path.name}이 심링크다"

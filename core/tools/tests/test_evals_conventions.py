"""evals 규약이 새지 않게 고정한다 (PLAN §4.6).

skill-eval 자체는 uv tool로 따로 설치되므로 여기서 import하지 않는다 — 규약 검사가
그 도구의 설치 여부에 묶이면 안 된다. 파일 구조와 YAML만 본다.

시나리오를 **실행**하지는 않는다. 실행은 실비용이 들고 결론은 사람이 리포트를 읽고
내는 일이라(합격 숫자 게이트 없음), 자동화의 대상이 아니다.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

EVALS = Path(__file__).resolve().parents[2] / "evals"
SCENARIOS = sorted(p for p in (EVALS / "scenarios").iterdir() if p.is_dir())
SKILLS = ("kb-query", "kb-ingest", "kb-lint", "kb-new")


def skill_sets(scenario: Path) -> list[dict]:
    return yaml.safe_load((scenario / "skill-sets.yaml").read_text())["sets"]


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda p: p.name)
def test_세_파일과_context가_있다(scenario: Path):
    for name in ("prompt.txt", "scenario.md", "skill-sets.yaml"):
        assert (scenario / name).is_file(), f"{scenario.name}: {name} 없음"
    assert (scenario / "context").is_dir(), f"{scenario.name}: context/ 없음"
    assert (scenario / "prompt.txt").read_text().strip()


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda p: p.name)
def test_baseline_팔이_의무다(scenario: Path):
    """스킬 없이도 되는 일은 스킬의 공로가 아니다 — 없으면 delta를 잴 수 없다."""
    sets = skill_sets(scenario)
    assert any(not s.get("skills") for s in sets), f"{scenario.name}: baseline 팔 없음"
    assert any(s.get("skills") for s in sets), f"{scenario.name}: 스킬 팔 없음"


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda p: p.name)
def test_채점_기준이_셋_이상이다(scenario: Path):
    body = (scenario / "scenario.md").read_text()
    assert body.count("- [ ] ") >= 3, f"{scenario.name}: 채점 기준 부족"
    for section in ("## Background", "## Expected Outcome", "## Grading Criteria"):
        assert section in body, f"{scenario.name}: {section} 절 없음"


@pytest.mark.parametrize("scenario", SCENARIOS, ids=lambda p: p.name)
def test_스킬_경로는_저장소_루트_상대다(scenario: Path):
    """러너가 cwd 기준으로 스킬을 복사하므로 절대경로·`..`는 다른 기기에서 깨진다."""
    for skill_set in skill_sets(scenario):
        for path in skill_set.get("skills", []):
            assert path.startswith(".agents/skills/"), f"{scenario.name}: {path}"


@pytest.mark.parametrize("skill", SKILLS)
def test_스킬당_시나리오가_셋_이상이다(skill: str):
    target = f".agents/skills/{skill}"
    count = sum(
        1 for scenario in SCENARIOS
        for skill_set in skill_sets(scenario)
        if target in skill_set.get("skills", [])
    )
    assert count >= 3, f"{skill}: 시나리오 {count}개 (PLAN §4.6은 ≥3)"


def test_runs는_추적하지_않는다():
    ignored = (EVALS.parent / ".gitignore").read_text()
    assert "evals/runs/" in ignored

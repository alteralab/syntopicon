"""멀티홉 하네스의 인수 게이트 (PLAN §4.6: "pytest — 홉별 임계 단언").

합성 코퍼스는 심긴 체인이라 **상한 추정**이다. 이 게이트가 지키는 것은 "링크 탐색이
좋다"가 아니라 "하네스가 돌아가고 수치가 재현된다"이다 — 판정은 수용 검증의
실코퍼스 재측정이 한다(PLAN §4.2).

    uv run --group index --group eval pytest tools/tests/test_retrieval_eval.py --junitxml=r.xml
"""

from __future__ import annotations

import pytest

pytest.importorskip("kiwipiepy", reason="Tier B — uv sync --group index")
pytest.importorskip("ir_measures", reason="Tier B — uv sync --group eval")

import retrieval_eval  # noqa: E402

# 홉별 임계. 합성 코퍼스에서 확장 전략은 정답을 전부 회수해야 한다 — 못 하면 하네스나
# 이웃 질의가 깨진 것이지 "검색이 좀 나빠진 것"이 아니다.
EXPAND_RECALL_FLOOR = 1.0
FLAT_RECALL_CEILING = 0.0   # 어휘가 안 걸리게 심었으므로 flat이 찾으면 코퍼스가 샌 것이다


@pytest.fixture(scope="module")
def report(tmp_path_factory):
    root = tmp_path_factory.mktemp("bench")
    questions = retrieval_eval.prepare(root, chains=10)
    return retrieval_eval.evaluate(root, questions)


def test_flat은_합성_체인을_못_찾는다(report):
    """찾는다면 정답 토큰이 시드에 샌 것이다 — 코퍼스 설계의 자기 점검."""
    assert report["flat"]["R@10"] <= FLAT_RECALL_CEILING


@pytest.mark.parametrize("hop", ["1hop", "2hop"])
def test_홉별_확장_회수_임계(report, hop):
    assert report["by_hop"][hop]["expand"]["R@10"] >= EXPAND_RECALL_FLOOR
    assert report["by_hop"][hop]["flat"]["R@10"] <= FLAT_RECALL_CEILING


@pytest.mark.parametrize("hop", ["1hop", "2hop"])
def test_확장이_아니었으면_못_찾았을_정답(report, hop):
    """자작 메트릭 — 기성 IR 메트릭은 '무엇 덕분에 찾았는가'를 답하지 않는다."""
    assert report["expansion_only_recall"][hop] == 1.0


def test_PLAN_8의_기록과_같은_자리에_있다(report):
    """§8 원장의 "합성 2/3-hop 회수 10/10(flat 0/10)"을 재현한다."""
    assert report["expand"]["R@10"] == 1.0
    assert report["flat"]["R@10"] == 0.0

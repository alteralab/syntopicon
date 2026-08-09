"""overlap 쌍 계산 — 순수 수학 부분. 벡터 적재는 qmd 실물이 있어야 해서
개발 기기의 실사용 검증이 담당하고, 여기서는 계산 규약을 고정한다."""

from __future__ import annotations

import numpy
import pytest

from syntopicon.overlap import Pair, find_pairs


def unit(*values: float) -> numpy.ndarray:
    vector = numpy.array([values], dtype=numpy.float32)
    return vector / numpy.linalg.norm(vector)


def test_동일_방향은_잡고_직교는_지나간다():
    vectors = {
        "it/concepts/a.md": unit(1, 0, 0),
        "it/concepts/b.md": unit(1, 0.01, 0),   # 거의 같은 방향
        "it/concepts/c.md": unit(0, 1, 0),      # 직교
    }
    pairs = find_pairs(vectors, threshold=0.85)
    assert [(p.left, p.right) for p in pairs] == [("it/concepts/a.md", "it/concepts/b.md")]
    assert pairs[0].similarity > 0.99


def test_페이지_유사도는_청크_최대다():
    """긴 페이지의 한 절이 다른 페이지를 복제한 경우 — 평균이면 희석돼 놓친다."""
    long_page = numpy.vstack([unit(0, 1, 0), unit(0, 0, 1), unit(1, 0, 0)])
    vectors = {"it/concepts/long.md": long_page, "it/concepts/dup.md": unit(1, 0, 0)}
    pairs = find_pairs(vectors, threshold=0.9)
    assert len(pairs) == 1 and pairs[0].similarity > 0.99


def test_KB_경계를_넘는_쌍은_비교하지_않는다():
    vectors = {"it/concepts/a.md": unit(1, 0), "ops/concepts/b.md": unit(1, 0)}
    assert find_pairs(vectors, threshold=0.5) == []


def test_증분은_바뀐_쪽이_낀_쌍만_본다():
    vectors = {
        "it/concepts/a.md": unit(1, 0),
        "it/concepts/b.md": unit(1, 0),
        "it/concepts/c.md": unit(1, 0),
    }
    pairs = find_pairs(vectors, threshold=0.9, changed={"it/concepts/c.md"})
    flat = {(p.left, p.right) for p in pairs}
    assert ("it/concepts/a.md", "it/concepts/b.md") not in flat   # 옛 쌍은 주간에 안 봄
    assert len(flat) == 2                                          # c가 낀 쌍 둘만

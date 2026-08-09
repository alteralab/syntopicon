"""페이지 overlap 검출 — 어휘가 달라도 의미가 겹치는 페이지 쌍 (PLAN §2.6·§4.3).

같은 개념이 다른 이름으로 두 페이지에 흩어지는 것은 LLM ingest의 만성 실패이고,
어휘 검사(FTS·각주 정합)로는 안 잡힌다 — 그래서 임베딩이 데이터 소스다. qmd가
만들어 둔 청크 벡터를 재사용한다(따로 임베딩 파이프라인을 두면 모델 세대가
갈라진다 — 혼합 금지 규칙의 같은 계보).

**페이지 쌍 유사도 = 청크 쌍 코사인의 최대값.** 평균이 아니라 최대인 이유: 한 절이
다른 페이지의 한 절을 복제한 것이 정확히 overlap이고, 평균은 긴 페이지에서 그
신호를 희석한다. 검출만 한다 — 병합 판단은 분기 compaction 때 사람이 한다.

실행 전략은 PLAN §4.3·§8의 산수 그대로: 주간은 바뀐 페이지 × 전체(1×N),
전쌍은 부트스트랩·분기에만(행렬곱 — 이 규모에서 밀리초).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy

from .qmdstore import QmdUnavailable, connect_vectors

#: 비교 대상 디렉터리. sources는 뺀다 — 메타 서식이 서로 닮아 소음만 낸다.
#: inbox를 넣는 것이 요점이다: 초안이 기존 페이지의 재조합인지가 리뷰의 3문 ⑵다.
DIRECTORIES = ("concepts/", "synthesis/", "inbox/")


@dataclass(frozen=True)
class Pair:
    left: str            # 저장소 루트 기준 경로
    right: str
    similarity: float    # 최대 청크 쌍 코사인


def load_vectors(kbs: tuple[str, ...]) -> dict[str, numpy.ndarray]:
    """페이지 → (청크 수 × 차원) 정규화 행렬. 벡터가 없는 페이지는 빠진다 —
    누락 보고는 소비자(lint) 몫이다."""
    pages: dict[str, list] = {}
    with connect_vectors() as connection:
        rows = connection.execute("""
            SELECT d.collection, d.path, v.embedding
            FROM documents d
            JOIN content_vectors c ON c.hash = d.hash
            JOIN vectors_vec v ON v.hash_seq = c.hash || '_' || c.seq
            WHERE d.active = 1
            ORDER BY d.collection, d.path, c.seq
        """)
        for row in rows:
            if row["collection"] not in kbs:
                continue
            if not row["path"].startswith(DIRECTORIES):
                continue
            vector = numpy.frombuffer(row["embedding"], dtype=numpy.float32)
            pages.setdefault(f"{row['collection']}/{row['path']}", []).append(vector)

    matrices = {}
    for path, vectors in pages.items():
        matrix = numpy.vstack(vectors)
        norms = numpy.linalg.norm(matrix, axis=1, keepdims=True)
        matrices[path] = matrix / numpy.where(norms == 0, 1, norms)
    return matrices


def find_pairs(vectors: dict[str, numpy.ndarray], threshold: float,
               changed: set[str] | None = None) -> list[Pair]:
    """임계 초과 쌍. changed가 주어지면 한쪽이라도 바뀐 쌍만 본다(주간 1×N),
    None이면 전쌍(부트스트랩·분기). 스코프는 KB 내부다(PLAN §4.3 표)."""
    paths = sorted(vectors)
    found = []
    for i, left in enumerate(paths):
        for right in paths[i + 1:]:
            if left.split("/", 1)[0] != right.split("/", 1)[0]:
                continue
            if changed is not None and left not in changed and right not in changed:
                continue
            similarity = float((vectors[left] @ vectors[right].T).max())
            if similarity >= threshold:
                found.append(Pair(left, right, similarity))
    return sorted(found, key=lambda pair: -pair.similarity)


__all__ = ["Pair", "QmdUnavailable", "load_vectors", "find_pairs", "DIRECTORIES"]

"""허브 이웃 스코프 — 벡터 후보를 저작 링크 그래프의 이웃으로 좁힌다 (원장 2026-08-16).

천장 실험이 근거다: 완벽 라우팅의 post-filter가 vector R@5 0.640→0.801,
최약 클래스(semantic)를 2배로 끌어올렸다. 실전 라우터의 도메인 신호는 태그가
아니라 **저작 링크 그래프**다 — 태그 폐지·허브 라우팅 채택과 같은 계보이고,
"위키형 페이지+링크 추적" 실증(원장 2026-08-04)의 검색 레그판이다.

씨앗 규칙은 소비자(search.py·retrieval 러너)가 공유한다: 형태소 레그 최상위
페이지들. 어휘 일치가 도메인을 지목하고, 그래프가 그 도메인의 울타리를 친다.
"""

from __future__ import annotations

import sqlite3

#: 씨앗으로 쓰는 형태소 상위 페이지 수. 1이면 오지목 한 방에 스코프가 통째로
#: 빗나가고, 많으면 울타리가 넓어져 필터가 무뎌진다 — 3은 실측 전 초기값이고
#: 개정은 러너 실측으로 한다.
SEED_PAGES = 3
HOPS = 2


def seeds_from_rows(rows, count: int = SEED_PAGES) -> list[str]:
    """형태소 히트 행에서 씨앗 페이지를 뽑는다 — 순서 보존, 페이지 중복 제거."""
    seen: list[str] = []
    for row in rows:
        path = row["path"]
        if path not in seen:
            seen.append(path)
        if len(seen) >= count:
            break
    return seen


def neighborhood(connection: sqlite3.Connection, seeds: list[str],
                 hops: int = HOPS) -> set[str]:
    """씨앗에서 무방향 hops 단계 안의 페이지 집합 — 씨앗 포함, 경로는 루트 기준.

    무방향인 이유: 도메인 묶음에는 "허브가 나를 가리킨다"와 "내가 허브를
    가리킨다"가 같은 신호다. resolved=1만 걷는다 — 미해결 간선은 대상이 없다.
    """
    seen = set(seeds)
    frontier = set(seeds)
    for _ in range(hops):
        if not frontier:
            break
        marks = ",".join("?" * len(frontier))
        rows = connection.execute(
            f"SELECT src, dst FROM edges WHERE resolved = 1 "
            f"AND (src IN ({marks}) OR dst IN ({marks}))",
            (*frontier, *frontier)).fetchall()
        found = {row["src"] for row in rows} | {row["dst"] for row in rows}
        frontier = found - seen
        seen |= found
    return seen

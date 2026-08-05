"""멀티홉 평가용 합성 코퍼스 (PLAN §4.2 하네스의 gen_corpus).

**심긴 체인 실험이라 상한 추정이다.** 여기서 나온 수치는 "링크 탐색이 flat 검색보다
낫다"의 증명이 아니라, 하네스가 돌아가고 측정이 재현된다는 확인이다. 판정은 수용
검증의 실코퍼스 재측정이 한다(PLAN §4.2).

설계: 질의는 **시드 페이지에만** 어휘가 걸리고, 정답 토큰은 k홉 떨어진 페이지에만
있다. 어휘가 겹치는 방해 페이지를 함께 깔아 flat 검색이 시드 주변에서 맴돌게 한다.
난수는 고정 시드로만 쓴다 — 재현되지 않는 벤치마크는 측정이 아니다.
"""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

# 체인 마디마다 붙일 주제어. 한국어 KB이므로 한국어 + 영문 용어 혼합이 실사용에 가깝다.
TOPICS = [
    ("복제 지연", "replication lag"), ("합의 정족수", "quorum"),
    ("쓰기 증폭", "write amplification"), ("스냅샷 격리", "snapshot isolation"),
    ("벡터 시계", "vector clock"), ("가십 전파", "gossip"),
    ("리더 임차", "leader lease"), ("로그 압축", "log compaction"),
    ("분할 뇌", "split brain"), ("체크섬 검증", "checksum"),
]


@dataclass(frozen=True)
class Question:
    qid: str
    text: str          # 시드 페이지에만 걸리는 질의
    gold: str          # 정답 페이지 경로 (저장소 루트 기준)
    seed: str          # 어휘로 찾히는 출발 페이지
    hops: int          # 시드에서 정답까지의 링크 수


def _page(title: str, description: str, body: str, cite: str) -> str:
    return (
        "---\n"
        "type: concept\n"
        f"title: {title}\n"
        f"description: {description}\n"
        'generated: { by: "tools/synth", at: "2026-08-05T00:00:00Z" }\n'
        "sources:\n"
        f"  - {{ id: {cite}, resource: /bench/sources/{cite}.md }}\n"
        "---\n"
        f"\n# {title}\n\n{body}\n"
    )


def generate(root: Path, kb: str = "bench", chains: int = 10, seed: int = 20260805
             ) -> list[Question]:
    """`<root>/<kb>/` 에 코퍼스를 쓰고 질문 목록을 돌려준다."""
    rng = random.Random(seed)
    concepts = root / kb / "concepts"
    concepts.mkdir(parents=True, exist_ok=True)
    (root / kb / "sources").mkdir(parents=True, exist_ok=True)

    cite = "synth2026-bench"
    (root / kb / "sources" / f"{cite}.md").write_text(
        "---\ntype: report\ntitle: 합성 벤치 코퍼스\nissued: \"2026\"\n---\n\n# 합성 벤치\n")
    (root / kb / "overview.md").write_text(
        "---\ntype: guide\ntitle: bench\ndescription: 합성 평가 코퍼스\n---\n\n# bench\n\n## Hubs\n")

    questions: list[Question] = []
    for index in range(chains):
        korean, english = TOPICS[index % len(TOPICS)]
        marker = f"zq{index:02d}"          # 정답 페이지에만 있는 고유 토큰
        hops = 1 if index % 2 == 0 else 2  # 2-hop 질문(k=1)과 3-hop 질문(k=2)을 반반

        names = [f"{english.replace(' ', '-')}-{index}-{step}" for step in range(hops + 1)]
        for step, name in enumerate(names):
            nxt = f"[다음 단계]({names[step + 1]}.md)" if step + 1 < len(names) else ""
            # 사슬 출발점(step 0)은 방해 페이지보다 어휘 신호가 결정적으로 강해야 한다.
            # 동점이면 순위가 코퍼스 통계 운에 달리고, 벤치가 재려는 것은 시드 변별이
            # 아니라 "어휘로 안 보이는 정답의 회수"다 — 메가허브 추가로 동점 운이
            # 뒤집혀 recall이 흔들린 실측이 이 줄의 근거다.
            anchor_line = (f"{korean} 즉 {english} 논의의 출발점이 이 페이지다.\n"
                           if step == 0 else "")
            body = (
                f"{korean} 개념의 {step}단계 서술이다. 이 문단은 {english} 를 다룬다.\n"
                f"{anchor_line}\n"
                f"- 단계 설명 불릿.[^{cite}]\n{nxt}\n\n[^{cite}]: 합성 코퍼스\n"
                if step < len(names) - 1 else
                f"정답 마커 {marker} 가 여기에만 있다. {korean} 사슬의 끝이다.\n\n"
                f"- 정답 불릿.[^{cite}]\n\n[^{cite}]: 합성 코퍼스\n"
            )
            (concepts / f"{name}.md").write_text(
                _page(f"{korean} {step}단계", f"{english} 체인 {index}의 {step}단계", body, cite))

        # 방해 페이지: 시드와 어휘가 겹치지만 사슬 밖이다 — flat 검색이 여기서 맴돈다.
        for extra in range(3):
            noise = f"{english.replace(' ', '-')}-{index}-noise{extra}"
            (concepts / f"{noise}.md").write_text(_page(
                f"{korean} 참고 {extra}", f"{english} 관련 메모",
                f"{korean} 에 대한 곁가지 메모다. {english} 라는 말이 여기도 나온다.\n\n"
                f"- 곁가지 불릿.[^{cite}]\n\n[^{cite}]: 합성 코퍼스\n", cite))

        questions.append(Question(
            qid=f"q{index:02d}",
            text=f"{korean} {english}",
            gold=f"{kb}/concepts/{names[-1]}.md",
            seed=f"{kb}/concepts/{names[0]}.md",
            hops=hops,
        ))

    # 메가허브: 모든 개념 페이지를 링크하는 고차수 노드. 실측된 고장 조건(300링크
    # 허브 → 전 KB가 2-hop)을 하네스에 상시로 심어, 차수 가중 탐색이 이것에
    # 강건한지를 인수 게이트가 계속 물게 한다.
    pages = sorted(concepts.glob("*.md"))
    hub_lines = "\n".join(
        f"- [{page.stem}]({page.name})" for page in pages
    )
    (root / kb / "synthesis").mkdir(parents=True, exist_ok=True)
    (root / kb / "synthesis" / "mega-hub.md").write_text(
        "---\ntype: synthesis\ntitle: 메가허브\ndescription: 전 개념을 링크하는 최악 조건\n"
        'generated: { by: "tools/synth", at: "2026-08-05T00:00:00Z" }\n---\n'
        f"\n# 메가허브\n\n{hub_lines}\n".replace("](", "](../concepts/"))

    rng.shuffle(questions)
    return questions

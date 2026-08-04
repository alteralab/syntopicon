#!/usr/bin/env python3
"""시나리오 context/ 를 한 곳에서 정의하고 펴 놓는다.

skill-eval은 시나리오마다 `context/` 를 통째로 임시 env에 복사한다(러너 소스 확인).
그래서 같은 KB를 쓰는 시나리오들끼리도 물리적으로는 사본을 갖는다 — 그 사본의
정본이 이 파일이다. 손으로 고치지 말고 여기를 고친 뒤 다시 돌린다.

    uv run evals/fixtures.py

같은 KB에 질문만 바꿔 던지는 것이 kb-query 시나리오의 설계다. 픽스처가 갈라지면
"스킬이 나아서 잘한 것"과 "코퍼스가 달라서 잘한 것"을 구분할 수 없다.
"""

from __future__ import annotations

import shutil
from pathlib import Path

EVALS = Path(__file__).resolve().parent
CITE = "ongaro2014-raft"

# ── 공유 KB: 분산 합의 4페이지 + 미검토 초안 1개 ──────────────────────────────
KB_IT: dict[str, str] = {
    "overview.md": """---
type: guide
title: syntopicon
description: IT 서적·논문·기술 문서를 축적하는 개인 지식 베이스의 KB 라우터
---

# syntopicon

md + git이 정본. 전체 카탈로그는 없다 — 이 라우터에서 KB를 고르고, 그 KB의
허브나 검색으로 내려간다. **읽기는 KB 횡단이 기본, 쓰기는 `--kb` 명시가 필수.**

## KBs

- [IT 지식](it/overview.md) — 분산 시스템·데이터 인프라 개념
""",
    "it/overview.md": """---
type: guide
title: IT 지식
description: 분산 시스템·데이터 인프라 개념
---

# IT 지식

분산 시스템과 데이터 인프라를 축적하는 KB.

## Hubs

- [분산 합의](synthesis/distributed-consensus.md) — 합의 알고리즘 개념들의 진입점

## Tools

- 검색: `qmd query <질의> -c it` / 형태소 레그 `tools/ksearch`
- 저장: `/kb-ingest --kb it` — inbox/ 경유
""",
    "it/synthesis/distributed-consensus.md": """---
type: synthesis
title: 분산 합의
description: 합의 알고리즘 개념들의 진입점
generated: { by: "human:me", at: "2026-07-20T09:00:00Z" }
---

# 분산 합의

- [Raft 읽기 경로](../concepts/raft-read-path.md) — 읽기에 quorum이 필요한 이유
- [리더 임차](../concepts/leader-lease.md) — quorum 왕복을 줄이는 장치
""",
    "it/concepts/raft-read-path.md": """---
type: concept
title: Raft 읽기 경로
description: Raft에서 선형화 가능한 읽기가 요구하는 것
generated: { by: "claude-fable-5", at: "2026-07-20T09:10:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# Raft 읽기 경로

## 읽기와 quorum

- leader lease 없이는 읽기에도 quorum 왕복이 필요하다.[^ongaro2014-raft]
- 리더가 자신이 여전히 리더인지 확인하지 않으면 stale read가 발생한다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §5.4
""",
    "it/concepts/leader-lease.md": """---
type: concept
title: 리더 임차
description: 시계 가정으로 읽기 quorum을 생략하는 최적화
generated: { by: "claude-fable-5", at: "2026-07-20T09:12:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# 리더 임차

## 무엇을 교환하는가

- 임차(lease) 기간 동안 리더는 quorum 왕복 없이 읽기에 답한다.[^ongaro2014-raft]
- 대가는 시계 가정이다 — 드리프트 한계를 넘으면 안전성이 깨진다.[^ongaro2014-raft]
- #hypothesis 실무에서 드리프트로 인한 사고 사례는 드물게 보고된다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §6.4
""",
    "it/sources/ongaro2014-raft.md": """---
type: paper-conference
title: "In Search of an Understandable Consensus Algorithm"
author: [{family: Ongaro, given: Diego}, {family: Ousterhout, given: John}]
issued: "2014"
event-title: "USENIX ATC"
---

# Raft 논문
""",
    "it/inbox/gossip-antientropy.md": """---
type: concept
title: 가십 안티엔트로피
description: 가십 전파에서 상태 수렴을 보장하는 방식
status: draft
generated: { by: "claude-fable-5", at: "2026-08-01T02:00:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# 가십 안티엔트로피

- 주기적 상태 교환이 누락된 갱신을 메운다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014
""",
}

# 시나리오 → 그 시나리오가 쓰는 픽스처
LAYOUT: dict[str, dict[str, str]] = {
    "query-kb-first": KB_IT,
    "query-gap-label": KB_IT,
    "query-save-judgment": KB_IT,
}

# ── KB가 없는 저장소 (kb-new 첫 실행·ingest 게이트용) ────────────────────────
NO_KB: dict[str, str] = {
    "overview.md": KB_IT["overview.md"].replace(
        "- [IT 지식](it/overview.md) — 분산 시스템·데이터 인프라 개념",
        "아직 없다. `/kb-new`가 KB의 유일한 생성 경로다."),
}

# ── 모순 쌍이 있는 KB (자동 해소 금지 검증용) ────────────────────────────────
def _with_contradiction() -> dict[str, str]:
    files = dict(KB_IT)
    files["it/concepts/leader-lease.md"] = files["it/concepts/leader-lease.md"].replace(
        "sources:", "contradicts: [lease-clock-risk]\nsources:")
    files["it/concepts/lease-clock-risk.md"] = """---
type: concept
title: 임차 시계 위험
description: 리더 임차의 시계 가정이 실무에서 깨지는 조건
generated: { by: "human:me", at: "2026-07-25T11:00:00Z" }
contradicts: [leader-lease]
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# 임차 시계 위험

- 가상화 환경의 시계 점프는 임차 안전성 가정을 깨뜨린다.[^ongaro2014-raft]
- 즉 임차는 "대가가 작다"고 말할 수 없는 환경이 실재한다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §6.4
"""
    return files


# ── 리포트가 딸린 KB (lint 분류·임계 경보용) ─────────────────────────────────
LINT_REPORT = """error  it/concepts/raft-read-path.md: → it/concepts/missing-page.md
error  it: inbox 나이 P90 47일 > 30일 — 자동 머지 범위 확대를 검토하십시오(PLAN §4.4 킬 기준)
warn   it/concepts/leader-lease.md: 2026-01-01 만료 — 재검토 큐
warn   it/inbox/gossip-antientropy.md: 47일째 리뷰 대기
warn   it/concepts/raft-read-path.md: sources에 ongaro2014-raft 를 선언했지만 각주가 없습니다
info   it/concepts/lease-clock-risk.md: leader-lease 와 모순 — 해소 시 최신성 단독 판단 금지
info   it/synthesis/distributed-consensus.md: 가리키는 페이지가 없습니다

1/8개 페이지 검사(full) · 오류 2 · 경고 3 · 정보 2
미구현 검사: page-overlap(임베딩 필요 (qmd 단계))
"""


def _with_report() -> dict[str, str]:
    files = _with_contradiction()
    files["lint-report.txt"] = LINT_REPORT
    return files


LAYOUT.update({
    "new-refuse-topic-split": KB_IT,
    "new-first-kb": NO_KB,
    "new-hard-boundary": KB_IT,
    "lint-triage": _with_report(),
    "lint-no-autoresolve": _with_contradiction(),
    "lint-tripwire": _with_report(),
    "ingest-no-kb": NO_KB,
    "ingest-updates-existing": KB_IT,
    "ingest-inbox-not-synthesis": KB_IT,
})


def main() -> None:
    for scenario, files in LAYOUT.items():
        context = EVALS / "scenarios" / scenario / "context"
        shutil.rmtree(context, ignore_errors=True)
        for relative, body in files.items():
            path = context / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body)
        print(f"{scenario}: {len(files)}개 파일")


if __name__ == "__main__":
    main()

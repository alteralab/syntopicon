---
type: synthesis
title: AI 애플리케이션 아키텍처
description: 최단 아키텍처에서 단계적으로 자라는 구조 — 맥락 강화, 가드레일, 라우터와 게이트웨이, 캐싱, 관측성과 모니터링, 로그와 트레이스, 드리프트 탐지, 파이프라인 오케스트레이션
generated: { by: "claude-fable-5", at: "2026-08-17T11:30:00Z" }
---

# AI 애플리케이션 아키텍처

축은 하나다 — **가장 단순한 구조에서 시작해 필요가 실측될 때마다 한 단계씩 보탠다.** 모델
호출 하나로 시작한 구조가 맥락·가드레일·라우팅·캐시·관측성을 얻으며 자라는 순서 자체가
설계라는 것이 이 축의 요지다.

## 단계적 확장

- [AI 애플리케이션 아키텍처의 진행](../concepts/ai-application-architecture-progression.md) — 최단
  아키텍처와 다섯 단계, 에이전트 패턴과 쓰기 행동까지
- [AI 애플리케이션 가드레일](../concepts/ai-application-guardrails.md) — 입력과 출력을 지키는 자리,
  완전히 제거되지 않는 위험
- [모델 라우터](../concepts/model-router.md) — 의도 분류와 질의별 모델 배정
- [모델 게이트웨이](../concepts/model-gateway.md) — 모델 접근을 한 문으로 모으는 층
- [정확 캐싱과 의미 캐싱](../concepts/exact-and-semantic-caching.md) — 같은 질의와 비슷한 질의를
  다시 계산하지 않기

## 관측과 운영

- [AI 관측성](../concepts/ai-observability.md) — 볼 수 있게 만드는 일의 규정
- [AI 모니터링 지표](../concepts/ai-monitoring-metrics.md) — 무엇을 재는가
- [로그와 트레이스](../concepts/logs-and-traces.md) — 요청 하나의 생애를 따라가기
- [드리프트 탐지](../concepts/drift-detection.md) — 조용히 변하는 것들을 잡기
- [AI 파이프라인 오케스트레이션](../concepts/ai-pipeline-orchestration.md) — 구성 요소를 잇는 도구와
  그것 없이 시작하라는 조언

## 다른 축에서 여기로 이어지는 자리

- [프롬프트 공격 방어](../concepts/defenses-against-prompt-attacks.md) — 가드레일이 방어의 어느
  수준에 놓이는가
- [모델 선택 워크플로](../concepts/model-selection-workflow.md) — 라우팅이 모델 선택과 만나는 자리
- [프롬프트 캐싱](../concepts/prompt-caching.md) — 추론 서빙 쪽의 캐시와 게이트웨이 캐시의 경계
- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 모니터링과 평가가 서로를
  먹이는 관계

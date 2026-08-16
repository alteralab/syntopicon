---
type: synthesis
title: AI 에이전트
description: 환경과 도구가 규정하는 행동하는 시스템 — 에이전트의 규정, 도구와 함수 호출, 계획 생성과 파운데이션 모델 플래너, 반성과 실패 모드, 그리고 기억
generated: { by: "claude-fable-5", at: "2026-08-17T01:30:00Z" }
---

# AI 에이전트

축은 하나다 — **환경과 도구가 에이전트를 규정하고, 플래너의 강함이 성패를 가른다.** 모델이
인지하는 것을 넘어 행동할 때 필요한 부품들(도구·계획·반성·기억)과 그 실패 방식이 이 축이다.

## 규정

- [에이전트란 무엇인가](../concepts/agents-defined.md) — 환경, 도구, 행동의 세 요소와 RAG가
  에이전트의 특수 사례인 이유

## 도구

- [에이전트의 도구](../concepts/agent-tools.md) — 지식 증강, 능력 확장, 쓰기 행동의 세 범주
- [함수 호출](../concepts/function-calling.md) — 모델이 도구를 부르는 기전과 API 계약
- [도구 선택](../concepts/agent-tool-selection.md) — 도구 집합을 고르는 실험과 모델·과제별 차이

## 계획

- [에이전트의 계획](../concepts/agent-planning.md) — 계획과 실행의 분리, 계획 검증
- [플래너로서의 파운데이션 모델](../concepts/foundation-models-as-planners.md) — 모델이 계획할 수
  있는가라는 논쟁
- [계획 생성](../concepts/plan-generation.md) — 계획을 뽑는 프롬프트와 제어 흐름

## 반성과 실패

- [반성과 오류 교정](../concepts/agent-reflection-and-error-correction.md) — 자기 평가가 끼어드는
  자리들
- [에이전트 실패 모드](../concepts/agent-failure-modes.md) — 계획·도구·효율의 세 갈래 실패와 평가

## 기억

- [에이전트 기억](../concepts/agent-memory.md) — 내부 지식, 컨텍스트, 외부 저장의 세 층과 기억
  관리

## 다른 축에서 여기로 이어지는 자리

- [검색 증강 생성](../concepts/retrieval-augmented-generation.md) — 검색이라는 행동 하나로 닫힌
  에이전트의 특수 사례
- [사고 연쇄 프롬프팅](../concepts/chain-of-thought-prompting.md) — 계획 생성이 딛는 추론 유도
- [구조화 출력](../concepts/structured-outputs.md) — 함수 호출이 요구하는 형식 강제
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 계획 후보 여럿을 뽑아 고르는 쪽
- [방어적 프롬프트 엔지니어링](../concepts/defensive-prompt-engineering.md) — 도구를 쥔 시스템이
  공격면이 되는 자리

---
type: synthesis
title: 프롬프트 엔지니어링
description: 모델 가중치를 바꾸지 않는 첫 번째 적응 기법 — 프롬프트의 해부와 인컨텍스트 학습, 쓰기의 관행, 프롬프트를 산출물로 다루는 규율, 그리고 프롬프트를 노리는 공격과 세 수준의 방어
generated: { by: "claude-fable-5", at: "2026-08-16T22:30:00Z" }
---

# 프롬프트 엔지니어링

축은 하나다 — **가중치를 고치지 않고 입력으로 모델의 동작을 조정하는 기술.** 가장 쉽고 흔한
적응 기법이라 먼저 소진해야 하고, 사람이 읽는 글쓰기와 달리 버전·평가·방어가 따라붙는
공학 산출물이라는 것이 이 축의 요지다.

## 프롬프트의 해부

- [프롬프팅의 기초](../concepts/prompting-fundamentals.md) — 프롬프트의 세 부분과 프롬프트
  엔지니어링이라는 일의 규정
- [인컨텍스트 학습](../concepts/in-context-learning.md) — 제로샷과 퓨샷, prompt와 context라는
  두 낱말
- [시스템 프롬프트와 사용자 프롬프트](../concepts/system-prompt-and-user-prompt.md) — 채팅
  템플릿과 지시 계층
- [컨텍스트 길이와 효율](../concepts/context-length-and-efficiency.md) — 자라는 컨텍스트 창과
  가운데를 잃어버리는 문제

## 프롬프트 쓰기의 관행

- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 모호함 줄이기,
  페르소나, 예시, 출력 형식
- [프롬프트에 맥락 넣기](../concepts/providing-context-in-prompts.md) — 맥락 구성과 지식 가두기
- [프롬프트 분해](../concepts/prompt-decomposition.md) — 하위 과제로 가르는 이유와 비용
- [사고 연쇄 프롬프팅](../concepts/chain-of-thought-prompting.md) — 단계별로 생각하게 만들기와
  자기 비평

## 프롬프트를 산출물로 다루기

- [프롬프트의 반복과 버전 관리](../concepts/prompt-iteration-and-versioning.md) — 반복 개선,
  조직화, 카탈로그
- [프롬프트 엔지니어링 도구](../concepts/prompt-engineering-tools.md) — 자동 최적화 도구와
  숨은 API 호출이라는 비용

## 공격과 방어

- [방어적 프롬프트 엔지니어링](../concepts/defensive-prompt-engineering.md) — 공격의 세 유형과
  위험 여섯 가지
- [프롬프트 추출](../concepts/prompt-extraction.md) — 시스템 프롬프트를 빼내는 역프롬프트
  엔지니어링
- [탈옥과 프롬프트 주입](../concepts/jailbreaking-and-prompt-injection.md) — 수동 공격, 자동
  공격, 간접 주입
- [정보 추출 공격](../concepts/information-extraction-attacks.md) — 훈련 데이터 추출과 저작권
  반추
- [프롬프트 공격 방어](../concepts/defenses-against-prompt-attacks.md) — 모델 수준, 프롬프트
  수준, 시스템 수준

## 다른 축에서 여기로 이어지는 자리

- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프트 기반 적응이 전체
  지형에서 서는 자리
- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 스택에서 프롬프트
  엔지니어링이 맡는 책임
- [지시 따르기 역량](../concepts/instruction-following-capability.md) — 프롬프팅이 통하기 위한
  전제 능력
- [구조화 출력](../concepts/structured-outputs.md) — 출력 형식 지시가 형식 강제와 만나는 자리

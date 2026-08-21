---
type: synthesis
title: AI 평가
description: 파운데이션 모델과 그 위의 시스템을 재는 방법 — 왜 어려운가부터 언어 모델링 지표, 정답이 있는 정확 평가, AI 판정자의 힘과 한계, 모델끼리 겨루는 비교 평가까지
generated: { by: "claude-fable-5", at: "2026-08-16T19:30:00Z" }
---

# AI 평가

축은 하나다 — **출력이 열려 있는 시스템을 무엇으로 재는가.** 정답이 있는 곳에는 정확 평가가,
없는 곳에는 판정자와 비교가 선다. 평가에 들이는 공이 시스템 개선을 좌우한다는 것이
이 축의 출발점이다.

## 왜 어려운가

- [파운데이션 모델 평가의 난제](../concepts/evaluating-foundation-models-challenges.md) — 열린 출력,
  블랙박스, 벤치마크 포화, 투자 지체의 다섯 갈래

## 언어 모델링 지표

- [언어 모델링 지표](../concepts/language-modeling-metrics.md) — 엔트로피, 크로스 엔트로피,
  BPC와 BPB, 퍼플렉시티와 그 쓰임

## 정답이 있는 평가

- [기능적 정확성](../concepts/functional-correctness.md) — 정확 평가와 주관 평가의 가름선,
  실행으로 재는 정확성과 pass@k
- [참조 데이터 대비 유사도 측정](../concepts/similarity-measurements-against-reference-data.md) —
  정확 일치, 어휘 유사도, 의미 유사도

## AI 판정자

- [AI 판정자](../concepts/ai-as-a-judge.md) — 왜 쓰는가, 세 가지 사용법, 판정자 프롬프트
- [AI 판정자의 한계](../concepts/ai-judge-limitations.md) — 비일관성, 기준 모호성, 비용과 지연,
  세 가지 편향
- [AI 판정자의 선택](../concepts/ai-judge-selection.md) — 강한/약한/동일 판정자, 자기 평가,
  특화 판정자 셋
- [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md) — 판정자가 자기
  출력을 알아보는 능력과 자기 출력을 선호하는 정도의 관계, 그 인과를 세우려 한 실험
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md) — 판정자와 대상이 다른
  모델이어도 오답이 겹치면 정확도가 부풀려지는 구조
- [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md) — 자기 판정에 기대는
  자기 수정의 이득을 같은 표본 예산에서 재고, 피드백을 더 강한 모델이 줄 때 무엇이 달라지는지
- [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md) —
  같은 요구가 벤더 실무 문서에 적힌 문면. 실증이 아니라 문면이고, 개정되는 문서의 스냅샷 지위

## 비교 평가

- [비교 평가](../concepts/comparative-evaluation.md) — 점별 평가와 비교 평가, 매치와 승률,
  평점 알고리즘
- [비교 평가의 난점](../concepts/comparative-evaluation-challenges.md) — 확장성, 표준화,
  절대 성능의 부재, 그래도 남는 이점

## 평가 기준

- [평가 주도 개발](../concepts/evaluation-driven-development.md) — 만들기 전에 기준을 정한다,
  그리고 기준을 나누는 네 갈래
- [도메인 특화 역량 평가](../concepts/domain-specific-capability-evaluation.md) — 벤치마크와
  객관식, 그리고 객관식이 분류만 잰다는 한계
- [생성 역량 평가](../concepts/generation-capability-evaluation.md) — NLG에서 온 유창성·일관성·
  충실성과 그것을 대신한 새 문제들
- [사실 일관성](../concepts/factual-consistency.md) — 지역과 전역, 자기 검증과 지식 증강 검증,
  텍스트 함의와 TruthfulQA
- [AI 안전성 평가](../concepts/ai-safety-evaluation.md) — 해악의 여섯 범주, 특화 독성 탐지 모델과
  독성 벤치마크
- [지시 따르기 역량](../concepts/instruction-following-capability.md) — IFEval과 INFOBench,
  그리고 롤플레잉
- [비용과 지연 평가](../concepts/cost-and-latency-criteria.md) — 파레토 최적화, 지연 지표,
  토큰 과금과 컴퓨트 비용

## 모델 선택

- [모델 선택 워크플로](../concepts/model-selection-workflow.md) — 하드 속성과 소프트 속성,
  걸러 내기에서 모니터링까지 네 단계
- [오픈 소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md) — 오픈 웨이트와
  오픈 모델, 반드시 물어야 할 세 질문
- [모델 API와 자체 호스팅](../concepts/model-api-versus-self-hosting.md) — 프라이버시·계보·성능·
  기능·비용·통제·온디바이스라는 일곱 축
- [공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md) — 벤치마크 선택과
  집계, 상관, 그리고 리더보드로 알 수 없는 것
- [데이터 오염](../concepts/data-contamination.md) — 벤치마크 점수가 실력이 아니라 기억일 때

## 평가 파이프라인

- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 구성 요소별 평가, 턴과 과제,
  평가 지침과 비즈니스 지표
- [평가 방법과 데이터](../concepts/evaluation-methods-and-data.md) — 방법 고르기와 데이터 슬라이싱,
  평가 집합의 크기, 그리고 파이프라인 자신의 평가

## 다른 축에서 여기로 이어지는 자리

- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 1장이 평가를 스택의
  한 책임으로 예고하는 자리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 의미 유사도가 딛고 서는
  임베딩과 그 품질 측정(MTEB)
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 검증기와 보상 모델이 출력 선택에
  쓰이는 쪽
- [구조화 출력](../concepts/structured-outputs.md) — 지시 따르기 역량이 형식으로 나타나는 쪽

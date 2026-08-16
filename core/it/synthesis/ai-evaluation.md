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

## 비교 평가

- [비교 평가](../concepts/comparative-evaluation.md) — 점별 평가와 비교 평가, 매치와 승률,
  평점 알고리즘
- [비교 평가의 난점](../concepts/comparative-evaluation-challenges.md) — 확장성, 표준화,
  절대 성능의 부재, 그래도 남는 이점

## 다른 축에서 여기로 이어지는 자리

- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 1장이 평가를 스택의
  한 책임으로 예고하는 자리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 의미 유사도가 딛고 서는
  임베딩과 그 품질 측정(MTEB)
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 검증기와 보상 모델이 출력 선택에
  쓰이는 쪽

---
type: concept
title: 합성 데이터 검증
description: 만든 데이터를 믿을지 정하는 단계 — 기능적 정확성과 AI 판정자라는 두 자, 검증할 수 있는 데이터를 합성하게 되는 경향, 진짜와 구별되는지로 품질을 재는 뒤집힌 방법, 그리고 Self-Instruct가 쓴 휴리스틱 거르개
status: draft
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 합성 데이터 검증

- [무엇으로 재는가](#무엇으로-재는가)
- [검증할 수 있는 것을 합성하게 된다](#검증할-수-있는-것을-합성하게-된다)
- [AI 검증자](#ai-검증자)
- [뒤집어서 재는 방법들](#뒤집어서-재는-방법들)
- [휴리스틱 거르개](#휴리스틱-거르개)
- [끝내 남는 시험](#끝내-남는-시험)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **AI가 만든 훈련 데이터의 품질을 어떻게 확인하는가.**

## 무엇으로 재는가

- 절이 여는 규정 — **모델 성능에서 데이터 품질이 갖는 중요성을 생각하면 데이터의 품질을 검증할 방법을
  갖는 것이 결정적이다. AI가 생성한 데이터의 품질은 다른 AI 출력을 평가하는 것과 같은 방식으로,
  기능적 정확성(functional correctness)과 AI 판정자(AI judges)로 측정할 수 있다** (8장,
  p.391).[^huyen2025] 그 두 가지는 각각
  [기능적 정확성](../concepts/functional-correctness.md)과
  [AI 판정자](../concepts/ai-as-a-judge.md)에 있다.
- 범위 — **이 절은 합성 데이터에 초점을 맞추지만 대부분의 기법은 일반적인 훈련 데이터의 품질을
  평가하는 데도 쓸 수 있다** (8장, p.392).[^huyen2025]

## 검증할 수 있는 것을 합성하게 된다

- **기업이 평가할 수 있는 애플리케이션을 만들 가능성이 높다는 4장의 평가 주도 개발(evaluation-driven
  development) 개념을 상기하라. 비슷하게 사람들은 검증할 수 있는 데이터를 합성하는 경향이 있다.
  코딩은 기능적으로 평가될 수 있기 때문에 가장 인기 있는 파운데이션 모델 유스케이스 중 하나이고, 같은
  이유로 코딩 관련 예제는 가장 흔히 합성되는 데이터에 속한다. Llama 3를 훈련하는 데 쓰인 합성 데이터의
  대부분은 코딩 관련이다. 저자들이 데이터를 합성하는 데 쓴 세 방법 모두 코드 실행과 역번역으로
  프로그램적으로 검증될 수 있는 데이터를 낸다** (8장, p.392).[^huyen2025]
  - #hypothesis 마지막 문장의 원문에는 "verified, x, by code execution"처럼 문장 안에 홀로 놓인 `x`가
    인쇄돼 있다. 뜻을 이루지 않아 옮기지 않았고, 조판 오류로 보이나 책 안에 확인 근거가 없다 (8장,
    p.392).[^huyen2025]
  - 그 평가 주도 개발 자체는
    [평가 주도 개발](../concepts/evaluation-driven-development.md)에 있다.

## AI 검증자

- **기능적 정확성으로 검증할 수 없는 합성 데이터에는 AI 검증자(AI verifier)를 쓰는 것이 흔하다. AI
  검증자는 범용 AI 판정자일 수도, 특화된 채점기일 수도 있다. 검증 문제를 틀 짓는 방법은 많다. 가장
  단순한 형태로 AI 검증자는 생성된 각 예제에 1에서 5까지의 점수를 매기거나 각 예제를 좋음 또는 나쁨으로
  분류할 수 있다. 파운데이션 모델에 품질 요구를 서술하고 데이터 예제가 이 요구를 충족하는지 판정하도록
  지시할 수도 있다** (8장, p.392).[^huyen2025]
- 사실 일관성 — **데이터의 사실 일관성에 신경 쓴다면 4장에서 논한 사실 비일관성 탐지 기법을 써서 환각을
  담을 가능성이 높은 예제를 걸러 낼 수 있다** (8장, p.392).[^huyen2025] 그 기법은
  [사실 일관성](../concepts/factual-consistency.md)에 있다.

## 뒤집어서 재는 방법들

- **유스케이스와 생성된 데이터에 따라 창의적일 수도 있다. 예컨대 합성 데이터가 실제 데이터를 흉내 내기를
  원한다면 그 품질은 둘을 구별하기가 얼마나 어려운지로 측정될 수 있다. AI 콘텐츠 탐지기를 훈련해 AI
  생성 데이터를 식별할 수 있다 — 실제 데이터와 합성 데이터를 구별하기 쉽다면 그 합성 데이터는 좋지 않은
  것이다. 아니면 합성 데이터가 고품질 학술 연구를 닮기를 원한다면, 생성된 논문이 NeurIPS(Conference and
  Workshop on Neural Information Processing Systems) 같은 권위 있는 학회에 채택될지 예측하는 분류기를
  훈련해 명백히 거절될 것으로 예측된 논문을 버릴 수 있다** (8장, p.392).[^huyen2025]
- 주제와 이상치 — **각 생성된 예제의 주제를 탐지하는 모델을 두고 주제가 당신 과제와 무관한 예제를 제거할
  수 있다. 모든 데이터가 비슷한 패턴을 따르기를 기대한다면 이상 탐지(anomaly detection)를 써서 이상치를
  식별할 수도 있다 — 이상치 예제는 저품질일 수 있다** (8장, p.392).[^huyen2025]

## 휴리스틱 거르개

- **실제 데이터와 마찬가지로 합성 데이터도 휴리스틱으로 걸러질 수 있다. 일반적으로 비어 있거나
  애플리케이션에 너무 짧은 예제를 제거하고 싶을 수 있다. 예제가 너무 길면 잘라 내거나 제거하고 싶을 수
  있다. 키워드·사용자/저자·생성일·메타데이터·출처로 데이터를 걸러 낼 수 있다** (8장,
  p.392).[^huyen2025]
- **예컨대 Self-Instruct 저자들(Wang et al., 2022)은 다음 휴리스틱으로 생성된 예제를 걸러 냈다** (8장,
  pp.392–393):[^huyen2025]
  - **Repetitive examples**
  - **Instructions that are too long or too short**
  - **Examples with the same instruction but different responses**
  - **Examples where the output is a repetition of the input**

## 끝내 남는 시험

- 절을 닫는 문장이다 (8장, p.393):[^huyen2025]

  > Even though there are many techniques to evaluate synthetic data, evaluation remains
  > challenging. As with other AI applications, the ultimate quality test for AI-generated data is
  > its real-world performance—whether it can improve the model's performance—and synthetic data
  > has passed this test for many models.

- 요약이 같은 것을 다시 짚는다 — **실제 데이터와 마찬가지로 합성 데이터는 모델을 훈련하는 데 쓰이기 전에
  품질을 확보하려고 평가되어야 한다. AI 생성 데이터를 평가하는 것은 다른 AI 출력을 평가하는 것만큼
  까다롭고, 사람들은 신뢰할 만하게 평가할 수 있는 생성 데이터를 쓸 가능성이 더 높다** (8장,
  p.403).[^huyen2025]

## 이어지는 페이지

- [AI 기반 데이터 합성](../concepts/ai-powered-data-synthesis.md) — 검증 대상이 만들어지는 자리
- [AI 생성 데이터의 한계](../concepts/limitations-of-ai-generated-data.md) — 검증으로도 안 풀리는 것
- [기능적 정확성](../concepts/functional-correctness.md) — 두 측정 축 중 하나
- [AI 판정자](../concepts/ai-as-a-judge.md) — 다른 하나
- [사실 일관성](../concepts/factual-consistency.md) — 환각 예제를 거르는 기법
- [평가 주도 개발](../concepts/evaluation-driven-development.md) — 검증 가능성이 선택을 미는 자리
- [훈련 데이터 정제와 형식](../concepts/training-data-cleaning-and-formatting.md) — 같은 거르개가
  실제 데이터에 쓰이는 자리
- [훈련 데이터 품질](../concepts/training-data-quality.md) — 검증이 지키려는 기준

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Data verification"
    (pp.391–393)과 Summary(p.403)의 대응 문단. Self-Instruct 휴리스틱 네 항목은 원문 표기를 그대로
    두었다. 이 구간에는 도판이 없다. Wang et al.(2022)과 Llama 3에 관한 진술은 huyen2025를 통한
    전언이다.

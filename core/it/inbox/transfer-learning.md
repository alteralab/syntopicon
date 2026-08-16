---
type: concept
title: 전이 학습
status: draft
description: 파인 튜닝이 처음부터 훈련하는 것보다 적은 데이터로 되는 이유 — 1976년에 이름을 얻은 전이 학습, 포르투갈어–스페인어 예가 없이도 번역한 구글의 다국어 시스템, 표본 효율, 파인 튜닝을 "이미 있는 능력을 여는 일"로 보는 관점, 그리고 전이의 다른 갈래인 특징 기반 전이
generated: { by: "claude-opus-5", at: "2026-08-17T05:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 전이 학습

- [파인 튜닝은 전이 학습의 한 방식이다](#파인-튜닝은-전이-학습의-한-방식이다)
- [초기의 대규모 성공](#초기의-대규모-성공)
- [전이가 푸는 문제는 데이터다](#전이가-푸는-문제는-데이터다)
- [표본 효율](#표본-효율)
- [이미 있는 능력을 여는 일](#이미-있는-능력을-여는-일)
- [특징 기반 전이](#특징-기반-전이)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **왜 남이 훈련한 모델에서 출발하면 처음부터 훈련할 때보다 훨씬 적은 데이터로
되는가.**

## 파인 튜닝은 전이 학습의 한 방식이다

- 출발점의 규정 — **파인 튜닝을 하려면 필요한 능력의 전부는 아니지만 일부를 가진 베이스 모델
  (base model)에서 시작한다. 파인 튜닝의 목표는 이 모델이 당신의 구체적 과제에 대해 충분히 잘
  수행하도록 만드는 것이다** (7장, p.308).[^huyen2025]
- 계보와 그 정의 (7장, p.308):[^huyen2025]

  > Finetuning is one way to do *transfer learning*, a concept first introduced by Bozinovski and
  > Fulgosi in 1976. Transfer learning focuses on how to transfer the knowledge gained from one task
  > to accelerate learning for a new, related task.

  - 저자가 붙이는 비유 — **이것은 사람이 기술을 전이하는 방식과 개념적으로 비슷하다. 예컨대 피아노를
    칠 줄 알면 다른 악기를 배우기가 더 쉬워질 수 있다** (7장, p.308).[^huyen2025]

## 초기의 대규모 성공

- **전이 학습의 초기 대규모 성공 하나가 구글의 다국어 번역 시스템이었다(Johnson et. al, 2016).
  이 모델은 포르투갈어–영어와 영어–스페인어 번역의 지식을 전이해 포르투갈어를 스페인어로 곧바로
  번역했다 — 훈련 데이터에 포르투갈어–스페인어 예가 하나도 없었는데도** (7장,
  p.308).[^huyen2025]

## 전이가 푸는 문제는 데이터다

- **딥러닝 초기부터 전이 학습은 훈련 데이터가 제한적이거나 비싼 과제에 해법을 제공해 왔다. 데이터가
  풍부한 과제로 베이스 모델을 훈련한 뒤 그 지식을 목표 과제로 전이할 수 있다** (7장,
  p.308).[^huyen2025]
- LLM에서의 실물 — **LLM에서는 텍스트 완성(데이터가 풍부한 과제)에 대한 사전 훈련에서 얻은 지식이
  법률 질의응답이나 text-to-SQL처럼 쓸 수 있는 데이터가 더 적은 특화 과제로 전이된다. 전이 학습에
  대한 이 능력이 파운데이션 모델을 특별히 가치 있게 만든다** (7장, p.308).[^huyen2025]

## 표본 효율

- 정의와 그 효과 (7장, p.309):[^huyen2025]

  > Transfer learning improves *sample efficiency*, allowing a model to learn the same behavior with
  > fewer examples. A *sample-efficient* model learns effectively from fewer samples.

  - 크기의 차이 — **예컨대 법률 질의응답을 위해 모델을 처음부터 훈련하려면 수백만 개의 예가 필요할
    수 있지만, 좋은 베이스 모델을 파인 튜닝하는 데는 수백 개면 될 수도 있다** (7장,
    p.309).[^huyen2025]

## 이미 있는 능력을 여는 일

- 이상적인 그림 — **이상적으로는 모델이 배워야 하는 것의 많은 부분이 이미 베이스 모델 안에 있고,
  파인 튜닝은 모델의 행동을 다듬을 뿐이다. OpenAI의 InstructGPT 논문(2022)은 파인 튜닝을 모델이
  이미 갖고 있으나 프롬프팅만으로는 사용자가 접근하기 어려운 능력을 여는 것으로 보자고 제안했다**
  (7장, p.309).[^huyen2025]
  - 같은 관점의 2장 판이 사후 훈련의 자원 비중에서 나온다 —
    [지도 파인 튜닝](../concepts/supervised-finetuning.md)이 담은 "사후 훈련은 사전 훈련된 모델이
    이미 갖고 있지만 프롬프트만으로는 접근하기 어려운 능력을 여는 일"이 그것이다.

## 특징 기반 전이

- 파인 튜닝만 있는 것이 아니다 — **파인 튜닝이 전이 학습을 하는 유일한 방법은 아니다. 또 다른 접근이
  특징 기반 전이(feature-based transfer)다. 이 접근에서는 모델이 데이터에서 특징을 뽑아내도록 —
  대개 임베딩 벡터로 — 훈련되고, 그 특징을 다른 모델이 쓴다** (7장, p.309).[^huyen2025]
  - 2장과 이어지는 자리 — **저자는 파운데이션 모델의 일부를 분류 헤드(classifier head)를 덧붙여
    분류 과제에 재사용하는 이야기를 할 때 2장에서 특징 기반 전이를 짧게 언급했다** (7장,
    p.309).[^huyen2025]
  - 컴퓨터 비전에서의 관행 — **특징 기반 전이는 컴퓨터 비전에서 아주 흔하다. 예컨대 2010년대
    후반에 많은 사람이 ImageNet 데이터셋으로 훈련된 모델을 써서 이미지에서 특징을 뽑고, 그 특징을
    객체 탐지나 이미지 분할 같은 다른 컴퓨터 비전 과제에 썼다** (7장, p.309).[^huyen2025]

## 이어지는 페이지

- [파인 튜닝의 갈래](../inbox/types-of-finetuning.md) — 전이의 방식이 실제로 어떤 이름들로 나뉘는가
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 가중치를 고치는가로 갈리는 두 범주
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 사후 훈련의 첫 단계
- [파운데이션 모델](../concepts/foundation-models.md) — 전이의 출발점이 되는 범용 모델
- [언제 파인 튜닝하는가](../inbox/when-to-finetune.md) — 전이가 값싸다는 것이 곧 하라는 뜻은
  아닌 이유
- [자기지도와 모델 규모](../concepts/self-supervision-and-model-scale.md) — 데이터가 풍부한 과제가
  풍부해진 경위
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 특징 기반 전이가 내놓는
  임베딩 벡터가 저장·검색되는 쪽

[^huyen2025]: Huyen 2025, 7장 "Finetuning" (책 pp.307–362). 이 페이지는 장 도입(p.307)과
    "Finetuning Overview" 절의 앞부분(pp.308–309), 그리고 그 안의 상자 "feature-based
    transfer"(p.309)를 담았다. 이 구간에는 도판이 없다. Bozinovski and Fulgosi(1976)·
    Johnson et al.(2016)·InstructGPT 논문(2022)은 huyen2025를 통한 전언이다.

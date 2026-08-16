---
type: concept
title: 모델 증류
description: 작은 학생이 큰 교사를 흉내 내도록 훈련하는 방법 — DistilBERT와 Alpaca의 수치, 많은 라이선스가 이것을 금지한다는 단서, 합성 데이터로 훈련하는 것이 곧 증류는 아니라는 구분, 그리고 학생이 교사보다 커진 Nemotron-4의 사례
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 모델 증류

- [정의](#정의)
- [왜 하는가 — 배포 비용](#왜-하는가--배포-비용)
- [학생 모델을 만드는 두 길](#학생-모델을-만드는-두-길)
- [라이선스가 막는다](#라이선스가-막는다)
- [어댑터와 함께 쓰이는 자리](#어댑터와-함께-쓰이는-자리)
- [합성 데이터 훈련이 곧 증류는 아니다](#합성-데이터-훈련이-곧-증류는-아니다)
- [자기 출력으로 훈련하는 것의 조건](#자기-출력으로-훈련하는-것의-조건)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **큰 모델의 능력을 작은 모델로 옮기는 일은 무엇이고 어디까지 되는가.**

## 정의

- 정의 (8장, p.395):[^huyen2025]

  > *Model distillation* (also called *knowledge distillation*) is a method in which a small model
  > (student) is trained to mimic a larger model (teacher) (Hinton et al., 2015). The knowledge of
  > the big model is distilled into the small model, hence the term distillation.

- 이 절이 놓인 자리 — **AI를 써서 데이터를 생성하는 법과 생성된 데이터를 평가하는 법, 그리고 그
  한계를 논했다. 다음 절에서는 AI 생성 데이터가 보조가 아니라 필수인 데이터 합성의 특별한 유스케이스
  하나로 옮겨 가자: 모델 증류** (8장, p.395).[^huyen2025]

## 왜 하는가 — 배포 비용

- **전통적으로 모델 증류의 목표는 배포를 위한 더 작은 모델을 만드는 것이다. 큰 모델을 배포하는 것은
  자원 집약적일 수 있다. 증류는 교사에 필적하는 성능을 유지하는 더 작고 빠른 학생 모델을 만들 수 있다.
  예컨대 BERT에서 증류된 모델 DistilBERT는 BERT 모델의 크기를 40% 줄이면서 언어 이해 능력의 97%를
  유지하고 60% 더 빠르다(Sanh et al., 2019)** (8장, p.395).[^huyen2025]

## 학생 모델을 만드는 두 길

- **학생 모델은 DistilBERT처럼 처음부터 훈련될 수도 있고 Alpaca처럼 사전 훈련된 모델에서 파인 튜닝될
  수도 있다. 2023년 Taori et al.은 Llama의 70억 파라미터 버전인 Llama-7B를 1,750억 파라미터 모델인
  text-davinci-003이 생성한 예제로 파인 튜닝했다. 그 결과 모델 Alpaca는 교사 모델 크기의 4%이면서
  text-davinci-003과 비슷하게 행동한다** (8장, p.395).[^huyen2025]
- 7장이 같은 접근을 파인 튜닝 쪽에서 부르는 이름은
  [언제 파인 튜닝하는가](../concepts/when-to-finetune.md)에 있다.

## 라이선스가 막는다

- 저자가 경고 상자로 둔 것 (8장, p.395):[^huyen2025]

  > Not all models can be distilled. Many model licenses prohibit using their outputs to train
  > other models, particularly to train competing models.

  그 조항의 지형은 [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md)에 있다.

## 어댑터와 함께 쓰이는 자리

- **합성 지시 데이터는 LoRA 같은 어댑터 기반 기법과 함께 쓰이는 것이 흔하다. 예컨대 BuzzFeed는 LoRA와
  OpenAI의 text-davinci-003이 생성한 예제를 써서 Flan-T5 모델을 파인 튜닝했다. 그 결과 모델은 추론
  비용을 80% 줄였는데, 다만 모델이 얼마나 잘 작동했는지는 불분명했다(2023)** (8장,
  p.396).[^huyen2025] 그 기법은 [LoRA](../concepts/lora.md)에 있다.

## 합성 데이터 훈련이 곧 증류는 아니다

- **합성 데이터로 하는 모든 훈련이 모델 증류인 것은 아니라는 점에 유의하라. 모델 증류는 교사 모델의
  성능이 학생의 금 기준(gold standard)임을 함의한다. 그러나 교사보다 더 크고 강력한 학생 모델을
  훈련하는 데 합성 데이터를 쓰는 것도 가능하다** (8장, p.396).[^huyen2025]
- 두 실물 — **앞 절에서 논한 역방향 지시를 통한 모델 부트스트래핑(Li et al., 2023)이 한 예다. 또 다른
  예는 NVIDIA의 Nemotron-4다. NVIDIA 연구자 팀은 먼저 3,400억 파라미터 베이스 모델을 사전 훈련했다.
  이 베이스 모델은 그다음 560억 파라미터 전문가 혼합 모델인 Mixtral-8x7B-Instruct-v0.1(Jiang et al.,
  2024)이 생성한 지시 데이터와 선호 데이터로 파인 튜닝되었다. 그 결과 학생 모델 Nemotron-4-340B-
  Instruct는 다양한 과제에서 교사 모델을 능가했다(NVIDIA, 2024)** (8장, p.396).[^huyen2025]
  - 각주가 다는 단서 — **Mixtral 같은 전문가 혼합 모델의 파라미터 수를 Nemotron-4 같은 조밀 모델의 것과
    비교하는 것은 공정하지 않지만, 교사 모델(Mixtral)이 학생 모델(Nemotron-4)보다 작다는 요지는 여전히
    성립한다** (8장, p.396 각주 15).[^huyen2025] 그 구조 차이는
    [모델 규모의 세 수치](../concepts/model-size-and-scale.md)에 있다.

## 자기 출력으로 훈련하는 것의 조건

- **Llama 3 논문은 더 유능한 모델이 생성한 데이터로 훈련하는 것이 모델 성능을 크게 개선할 수 있는
  반면, 자기가 생성한 데이터로 무차별적으로 훈련하는 것은 모델 성능을 개선하지 못하고 심지어 떨어뜨릴
  수 있다고 지적한다. 그러나 합성 데이터의 품질을 검증하는 기전을 도입하고 검증된 합성 데이터만 씀으로써
  그들은 모델이 생성한 데이터를 써서 모델을 계속 개선할 수 있었다** (8장, p.396).[^huyen2025] 그
  검증 기전은 [합성 데이터 검증](../concepts/synthetic-data-verification.md)에 있다.

## 이어지는 페이지

- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 증류가 합성의 다섯째 이유로
  꼽히는 자리
- [AI 생성 데이터의 한계](../concepts/limitations-of-ai-generated-data.md) — 피상적 모방이 증류를
  제한하는 자리
- [합성 데이터 검증](../concepts/synthetic-data-verification.md) — 자기 출력으로 훈련할 때의 조건
- [언제 파인 튜닝하는가](../concepts/when-to-finetune.md) — 작은 모델을 파인 튜닝하는 쪽의 7장 서술
- [파인 튜닝의 세 선택](../concepts/finetuning-setup-choices.md) — 증류 경로가 이름으로 나오는 자리
- [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md) — 출력 사용 금지 조항
- [LoRA](../concepts/lora.md) — 증류된 학생을 싸게 만드는 기법
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — 전문가 혼합과 조밀 모델의 파라미터 비교

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Model Distillation"
    (pp.395–396). 이 구간에는 도판이 없다. Hinton et al.(2015)·Sanh et al.(2019)·Taori et al.·
    BuzzFeed(2023)·Li et al.(2023)·Jiang et al.(2024)·NVIDIA(2024)·Llama 3 논문은 huyen2025를 통한
    전언이다.

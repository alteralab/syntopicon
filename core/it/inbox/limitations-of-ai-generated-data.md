---
type: concept
title: AI 생성 데이터의 한계
description: 합성 데이터가 사람 데이터를 완전히 대체하지 못하는 네 이유 — 품질 관리, 스타일만 흉내 내다 환각을 배우는 피상적 모방, 재귀 훈련이 되돌릴 수 없는 결함을 남긴다는 모델 붕괴와 그 반론, 그리고 계보가 흐려지면서 생기는 저작권·오염 위험
status: draft
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# AI 생성 데이터의 한계

- [네 가지 이유](#네-가지-이유)
- [품질 관리](#품질-관리)
- [피상적 모방](#피상적-모방)
- [모델 붕괴](#모델-붕괴)
- [모델 붕괴에 대한 반론](#모델-붕괴에-대한-반론)
- [편향 증폭](#편향-증폭)
- [흐려지는 데이터 계보](#흐려지는-데이터-계보)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **AI가 만든 데이터가 사람이 만든 데이터를 완전히 대체하지 못하는 이유는 무엇인가.**

## 네 가지 이유

- 절이 여는 규정 (8장, p.393):[^huyen2025]

  > Given the increasing usefulness of synthetic data, it's exciting to imagine the possibility of
  > never having to worry about human-annotated data again. However, while the role of synthetic
  > data will certainly continue to grow in importance over time, AI-generated data might never
  > entirely replace human-generated data. There are many reasons why, but the four major ones are
  > the difference in quality, the limitations of imitation, potential model collapse, and the way
  > AI generation of data obscures its lineage.


## 품질 관리

- **AI가 생성한 데이터는 품질이 낮을 수 있고, 사람들이 말하기를 결코 지치지 않듯 "쓰레기가 들어가면
  쓰레기가 나온다(garbage in, garbage out)". 사람들은 합성 데이터의 품질을 검증할 수 없으면 그것을
  쓰기를 주저할 것이다. 데이터를 평가할 신뢰할 만한 방법과 지표를 개발할 수 있는 것이 합성 데이터를
  더 유용하게 만드는 데 필수적일 것이다** (8장, p.393).[^huyen2025] 그 방법들은
  [합성 데이터 검증](../concepts/synthetic-data-verification.md)에 있다.

## 피상적 모방

- **"The False Promise of Imitating Proprietary LLMs"(Gudibande et al., 2023)가 경고하듯 흉내를 통해
  달성된 성능은 피상적일 수 있다. 이 연구는 모방 모델이 교사 모델의 스타일을 흉내 내는 데는 능하지만
  사실 정확성과 훈련 데이터 밖 과제로의 일반화에서는 애를 먹을 수 있음을 보인다** (8장,
  p.393).[^huyen2025]
- 더 나쁜 것 — **더 나쁘게, 모방은 학생 모델이 환각하도록 강요할 수 있다. 교사 모델이 복잡한 수학
  질문에 답할 수 있어서 그 질문에 대한 응답이 해법이라고 상상해 보자. 이 해법들로 학생 모델을 훈련하는
  것은 학생 모델이 이 질문을 풀 능력이 없더라도 해법처럼 보이는 답을 만들어 내도록 사실상 가르치는
  것이다. Gudibande et al.(2023)은 추론 능력의 개선을 위해서는 베이스 모델의 품질을 개선하는 데
  초점을 맞춰야 한다고 제안한다** (8장, p.393).[^huyen2025]
  - 각주가 붙이는 대칭 — **같은 문제가 사람 주석에서도 일어날 수 있다. 사람 레이블러가 자기가 가진
    지식을 쓰는데 모델은 질문에 답할 지식이 없다면, 그들은 사실상 모델에게 환각하라고 가르치는
    것이다** (8장, p.393 각주 13).[^huyen2025]

## 모델 붕괴

- **모델이 AI 생성 데이터로 얼마나 훈련할 수 있는지도 불분명하다. 어떤 연구는 훈련에 AI 생성 데이터를
  재귀적으로(recursively) 쓰는 것이 결과 모델에 되돌릴 수 없는 결함을 일으켜 시간이 지나며 성능을
  떨어뜨린다는 것을 보였다. "The Curse of Recursion: Training on Generated Data Makes Models Forget"에서
  Shumailov et al.(2023)은 이 현상을 모델 붕괴(model collapse)라 이름 붙이고 변분 오토인코더·가우시안
  혼합 모델·LLM을 포함한 모델에서 그 발생을 시연했다. 모델 붕괴는 사전 훈련과 사후 훈련 양쪽에서 일어날
  수 있다** (8장, p.394).[^huyen2025]
  - 각주 — **이 개념은 같은 저자들이 나중에 "AI Models Collapse When Trained on Recursively Generated
    Data"(《네이처》, 2024년 7월)에서도 설명했다** (8장, p.394 각주 14).[^huyen2025]
- 왜 일어나는가 — **한 가지 가능한 설명은 AI 모델이 개연성 있는 사건(예: 암에 걸리지 않음)을 생성할
  가능성이 더 높고 개연성 낮은 사건(예: 암에 걸림)을 생성할 가능성이 더 낮다는 것이다. 여러 번의 반복을
  거치며 개연성 있는 사건은 생성된 데이터에서 과대 대표되는 반면 개연성 낮은 사건은 과소 대표된다.
  이는 모델이 시간이 지나며 더 흔한 사건을 출력하고 드문 사건을 잊게 만든다** (8장,
  p.394).[^huyen2025]

## 모델 붕괴에 대한 반론

- **"Is Model Collapse Inevitable?"에서 Gerstrasser et al.(2024)은 전체 훈련 데이터셋이 합성이라면
  모델 붕괴가 불가피하지만 합성 데이터를 실제 데이터와 섞으면 피할 수 있다고 논한다. Bertrand et
  al.(2023)과 Dohmatob et al.(2024)도 비슷한 결과를 보인다. 그러나 이 논문 중 어느 것도 합성 데이터
  대 실제 데이터의 비율에 대한 확정적 권고를 갖고 있지 않다** (8장, p.394).[^huyen2025]
- 대량으로 잘된 실물 — **어떤 사람들은 많은 양의 합성 데이터로 모델 성능을 개선할 수 있었다. 예컨대
  "Common 7B Language Models Already Possess Strong Math Capabilities"(Li et al., 2024)는 수학 문제에
  대해 Llama-2-7B 모델을 파인 튜닝하는 데 합성 데이터가 실제 데이터만큼 거의 효과적임을 시연한다. 그들의
  실험에서 합성 데이터는 약 100만 표본까지 규모를 키웠을 때 명확한 포화를 보이지 않는다. 비슷하게
  Nemotron-4 340B-Instruct(NVIDIA, 2024)는 지시 파인 튜닝과 선호 파인 튜닝 단계에서 98% 합성 데이터를
  썼다. 그러나 이 실험들은 한 번의 모델 반복에 대해서만 수행되었다** (8장, p.394).[^huyen2025]

## 편향 증폭

- **AI 생성 데이터는 편향을 영속시킬 수도 있다. "Data Feedback Loops: Model-driven Amplification of
  Dataset Biases"(Taori and Hashimoto, 2023)는 모델이 이전 모델 출력을 포함한 데이터셋으로 훈련될 때
  모델의 기존 편향이 증폭될 수 있음을 시연한다. 저자들은 모델의 출력이 원래 훈련 분포의 특성에 충실할수록
  피드백 루프가 더 안정적이어서 편향 증폭의 위험이 최소화된다는 것을 발견한다** (8장,
  p.394).[^huyen2025]

## 흐려지는 데이터 계보

- **AI 생성 데이터의 이 한계는 더 미묘하다. AI 생성은 데이터 계보(data lineage)를 흐린다. AI 모델은
  자기 훈련 데이터에 영향받으며 때때로 사용자가 모르는 채로 그것을 되뱉을 수 있다. 이는 위험을 만든다.
  모델 X를 써서 당신 모델을 훈련할 데이터를 생성한다고 하자. 모델 X가 저작권을 침해한 데이터로
  훈련되었다면 당신 모델도 저작권을 침해할 수 있다** (8장, p.395).[^huyen2025]
- 평가 쪽 위험 — **아니면 벤치마크 B로 당신 모델을 평가해 강한 성능이 나왔다고 상상해 보자. 그러나
  모델 X도 벤치마크 B로 훈련되었다면 B에 대한 당신의 결과는 오염된 것이다. 명확한 데이터 계보 없이는
  모델의 상업적 실행 가능성을 평가하거나 그 성능을 신뢰하기 어렵다** (8장, p.395).[^huyen2025] 그
  오염 자체는 [데이터 오염](../concepts/data-contamination.md)에 있고, 출력 사용을 막는 라이선스
  조건은 [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md)에 있다.

## 이어지는 페이지

- [모델 증류](../concepts/model-distillation.md) — 합성 데이터가 보조가 아니라 필수인 유스케이스
- [합성 데이터 검증](../concepts/synthetic-data-verification.md) — 첫째 한계에 대한 대응
- [AI 기반 데이터 합성](../concepts/ai-powered-data-synthesis.md) — 여기서 한계에 부딪히는 기법들
- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 사람 데이터와 섞는 것이 최선인 이유
- [데이터 오염](../concepts/data-contamination.md) — 계보가 흐려질 때 평가가 무너지는 자리
- [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md) — 출력으로 훈련하는 것의
  법적 조건
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 환각을 배운다는 말의 배경

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Limitations to AI-generated
    data"(pp.393–395). 이 구간에는 도판이 없다. Gudibande et al.(2023)·Shumailov et al.(2023)·
    Gerstrasser et al.(2024)·Bertrand et al.(2023)·Dohmatob et al.(2024)·Li et al.(2024)·
    NVIDIA(2024)·Taori and Hashimoto(2023)는 huyen2025를 통한 전언이다.

---
type: concept
title: 모델 개발 층
description: AI 엔지니어링 스택의 가운데 층이 지는 세 책임 — 모델링과 훈련에서 ML 지식이 필수에서 있으면 좋은 것으로 내려앉고, 데이터셋 엔지니어링이 특징 공학에서 중복 제거·토큰화·맥락 검색·품질 관리로 옮겨 가며, 자기회귀 생성 탓에 추론 최적화가 한층 더 중요해지는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 모델 개발 층

- [세 책임](#세-책임)
- [모델링과 훈련](#모델링과-훈련)
- [데이터셋 엔지니어링](#데이터셋-엔지니어링)
- [추론 최적화](#추론-최적화)
- [세 책임이 어떻게 옮겨 갔는가](#세-책임이-어떻게-옮겨-갔는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파운데이션 모델이 오면서 모델을 만드는 층의 일은 무엇으로 바뀌었는가.**

## 세 책임

- **모델 개발(model development)은 전통적 ML 엔지니어링과 가장 흔히 결부되는 층이다. 세 가지 주된
  책임이 있다: 모델링과 훈련, 데이터셋 엔지니어링, 추론 최적화. 평가도 필요하지만 대부분의 사람이
  애플리케이션 개발 층에서 그것을 먼저 마주치게 되므로 평가는 다음 절에서 논의한다** (1장,
  pp.40–41).[^huyen2025]

## 모델링과 훈련

- 정의 (1장, p.41):[^huyen2025]

  > *Modeling and training* refers to the process of coming up with a model architecture, training
  > it, and finetuning it.

  **이 범주의 도구 예로는 구글의 TensorFlow, Hugging Face의 Transformers, 메타의 PyTorch가 있다**
  (1장, p.41).[^huyen2025]
- 무엇을 알아야 했는가 — **ML 모델을 개발하려면 특화된 ML 지식이 필요하다. 군집화·로지스틱 회귀·의사결정
  트리·협업 필터링 같은 서로 다른 종류의 ML 알고리즘과 순방향·순환·합성곱·트랜스포머 같은 신경망 구조를
  알아야 한다. 경사 하강·손실 함수·정규화 같은 개념을 포함해 모델이 어떻게 학습하는지 이해하는 것도
  필요하다** (1장, p.41).[^huyen2025]
- 그 요구가 내려앉았다 — **파운데이션 모델의 가용성과 함께 ML 지식은 AI 애플리케이션을 만드는 데 더 이상
  필수가 아니다. 경사 하강을 배우는 데 전혀 관심이 없는 훌륭하고 성공적인 AI 애플리케이션 제작자를 많이
  만났다. 그러나 ML 지식은 여전히 대단히 값진데, 쓸 수 있는 도구의 집합을 넓혀 주고 모델이 기대대로
  작동하지 않을 때 문제 해결을 돕기 때문이다** (1장, p.41).[^huyen2025]
- 이 층에서 훈련·사전 훈련·파인 튜닝·사후 훈련이라는 낱말이 각각 무엇을 가리키는지는
  [모델 적응 기법](../concepts/model-adaptation-techniques.md)이 맡는다.
- 여기서 말하는 구조를 정하는 일이 구체적으로 무엇인지도 2장이 채운다 — **모델을 훈련하기 전에
  개발자는 모델이 어떤 모습이어야 하는지 정해야 한다. 어떤 구조를 따를 것인가? 파라미터를 몇 개나
  가져야 하는가?** (2장, p.58).[^huyen2025] 그 두 결정은 각각
  [트랜스포머 구조](../concepts/transformer-architecture.md)와
  [모델 규모의 세 수치](../concepts/model-size-and-scale.md)가 맡고, 예산 안에서 둘을 나누는
  규칙은 [스케일링 법칙](../concepts/scaling-laws.md)에 있다.

## 데이터셋 엔지니어링

- 정의 (1장, p.42):[^huyen2025]

  > *Dataset engineering* refers to curating, generating, and annotating the data needed for
  > training and adapting AI models.

- 주석 달기가 왜 더 어려워졌는가 — **전통적 ML 엔지니어링에서는 대부분의 유스케이스가 폐쇄형이다. 모델의
  출력이 미리 정해진 값들 중에서만 나올 수 있다는 뜻이다. 예컨대 가능한 출력이 "spam"과 "not spam" 둘뿐인
  스팸 분류는 폐쇄형이다. 그러나 파운데이션 모델은 개방형이다. 개방형 질의에 주석을 다는 것은 폐쇄형 질의에
  주석을 다는 것보다 훨씬 어렵다 — 에세이를 쓰는 것보다 이메일이 스팸인지 판정하는 것이 더 쉽다. 그래서
  데이터 주석은 AI 엔지니어링에서 훨씬 큰 난제다** (1장, p.42).[^huyen2025]
- 데이터의 형태도 바뀐다 — **또 다른 차이는 전통적 ML 엔지니어링이 표 형식 데이터(tabular data)와 더
  일하는 반면 파운데이션 모델은 비정형 데이터와 일한다는 것이다. AI 엔지니어링에서 데이터 조작은 중복
  제거(deduplication)·토큰화·맥락 검색(context retrieval)·품질 관리 쪽에 더 가깝고, 품질 관리에는 민감
  정보와 유해 데이터의 제거가 포함된다** (1장, pp.42–43).[^huyen2025] 배치 처리 쪽에서 본 같은 전처리
  단계는 [배치 처리의 유스케이스](../concepts/batch-use-cases.md)에 있다.
- 데이터가 차별점이라는 주장 — **모델이 이제 상품(commodity)이 되었으므로 데이터가 주된 차별점이 되어
  데이터셋 엔지니어링이 그 어느 때보다 중요해진다고 많은 사람이 주장한다. 얼마나 많은 데이터가 필요한지는
  어떤 어댑터 기법을 쓰느냐에 달려 있다** (1장, p.43).[^huyen2025]
- 데이터를 아는 것의 다른 값 — **얼마나 많은 데이터가 필요하든, 모델을 살펴볼 때 데이터에 대한 전문성이
  유용하다. 그 훈련 데이터가 그 모델의 강점과 약점에 대한 중요한 실마리를 주기 때문이다** (1장,
  p.43).[^huyen2025]
- 여기서 이름만 정의된 이 책임을 8장이 통째로 펼친다 — 그 장이 세우는 목표는
  **예산 안에서 최선의 모델을 훈련할 수 있는 데이터셋을 만드는 것**이고 (8장, p.363),[^huyen2025]
  큐레이션·합성·처리 세 덩어리로 나뉜다 (8장, p.364).[^huyen2025] 그 전체는
  [데이터셋 엔지니어링이란](../concepts/dataset-engineering-defined.md)에 있고, 여기 열거된 중복
  제거·품질 관리의 실물은 각각
  [훈련 데이터 중복 제거](../concepts/training-data-deduplication.md)와
  [훈련 데이터 품질](../concepts/training-data-quality.md)이 맡는다.

## 추론 최적화

- 정의 (1장, p.43):[^huyen2025]

  > *Inference optimization* means making models faster and cheaper.

- 왜 더 중요해졌는가 — **추론 최적화는 ML 엔지니어링에서 늘 중요했다. 사용자는 더 빠른 모델에 결코
  아니라고 하지 않고, 기업은 더 싼 추론에서 언제나 이익을 얻을 수 있다. 그러나 파운데이션 모델이 규모를
  키워 훨씬 높은 추론 비용과 지연을 일으키면서 추론 최적화는 한층 더 중요해졌다** (1장,
  p.43).[^huyen2025]
- 자기회귀가 만드는 난제 — **파운데이션 모델의 난제 하나는 그것이 흔히 자기회귀적이라는 것이다. 토큰이
  순차적으로 생성된다. 모델이 토큰 하나를 생성하는 데 10밀리초가 걸린다면 토큰 100개의 출력을 생성하는
  데 1초가 걸리고, 더 긴 출력이면 더 걸린다. 사용자는 악명 높게 참을성이 없어지고 있으므로, AI
  애플리케이션의 지연을 통상적인 인터넷 애플리케이션에 기대되는 100밀리초 지연까지 낮추는 것은 큰
  난제다. 추론 최적화는 산업과 학계 양쪽에서 활발한 하위 분야가 되었다** (1장, p.43).[^huyen2025]
- 기법의 이름들 — **양자화(quantization)·증류(distillation)·병렬화(parallelism)를 포함한 추론 최적화
  기법이 있다** (1장, p.44).[^huyen2025]
- 그 순차성이 구조의 어디서 오는지는 2장이 짚는다 — 트랜스포머는 입력의 순차 병목을 없앴지만
  **트랜스포머 기반 자기회귀 언어 모델은 여전히 순차적 출력 병목을 갖고**, 그래서 추론이 병렬로 도는
  프리필과 한 토큰씩 도는 디코드로 갈린다 (2장, p.60).[^huyen2025] 그 구분은
  [트랜스포머 구조](../concepts/transformer-architecture.md)에 있다.
- 데이터셋 엔지니어링의 사전 훈련 쪽 실물 — 어떤 데이터가 실제로 쓰이고 왜 그것이 문제인지는
  [훈련 데이터 큐레이션](../concepts/training-data-curation.md)이, 주석 데이터를 만드는 일의 단가는
  [지도 파인 튜닝](../concepts/supervised-finetuning.md)이 맡는다.

## 세 책임이 어떻게 옮겨 갔는가

- 저자가 정리한 대비표다 (1장, p.43, Table 1-4):[^huyen2025]

  | 범주 | 전통적 ML로 만들 때 | 파운데이션 모델로 만들 때 |
  |---|---|---|
  | Modeling and training | ML knowledge is required for training a model from scratch | ML knowledge is a nice-to-have, not a must-have |
  | Dataset engineering | More about feature engineering, especially with tabular data | Less about feature engineering and more about data deduplication, tokenization, context retrieval, and quality control |
  | Inference optimization | Important | Even more important |

  - 표에 저자가 스스로 단 각주 — **많은 사람이 이 주장에 이의를 제기하며 ML 지식은 필수라고 말할
    것이다** (1장, p.43).[^huyen2025]

## 이어지는 페이지

- [AI 엔지니어링 스택](../concepts/ai-engineering-stack.md) — 이 층이 놓인 자리
- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 평가가 논의되는 쪽
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 이 층의 훈련 낱말들이 가리키는 단계
- [AI 엔지니어링과 ML 엔지니어링](../concepts/ai-engineering-versus-ml-engineering.md) — 이 표가
  요약하는 차이의 전체
- [변환 단계](../concepts/transformation-in-the-lifecycle.md) — 특징 공학이 데이터 파이프라인에서
  자동화되던 쪽
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 이 층이 정하는 구조의 실물
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — 규모 결정이 컴퓨트 비용으로
  환산되는 자리
- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 데이터셋 엔지니어링의 사전 훈련 쪽
- [데이터셋 엔지니어링이란](../concepts/dataset-engineering-defined.md) — 이 층의 둘째 책임이 한 장으로
  펼쳐지는 자리

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48)과 2장 "Understanding Foundation Models"(책 pp.49–112) 중 모델링 도입(p.58)·
    프리필과 디코드(p.60) 대목, 그리고 8장 "Dataset Engineering"의 목표와 구성(pp.363–364).
    Table 1-4는 원문 표기를 그대로 옮겼다. 이 절에는 도판이 없다.

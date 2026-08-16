---
type: concept
title: 파운데이션 모델
status: draft
description: 언어 모델이 텍스트 밖의 양식을 받아들이면서 얻은 이름 — 멀티모달 모델과 LMM, 자기지도를 이미지에 옮긴 CLIP의 자연어 지도, 과제 특화 모델에서 범용 모델로의 전환, 그 위에서 사거나 짓거나를 고르는 자리, 그리고 모델들 사이의 차이가 되짚어지는 세 가지 설계 결정
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 파운데이션 모델

- [텍스트 너머로](#텍스트-너머로)
- [멀티모달 모델과 LMM](#멀티모달-모델과-lmm)
- [왜 파운데이션인가](#왜-파운데이션인가)
- [CLIP과 자연어 지도](#clip과-자연어-지도)
- [과제 특화에서 범용으로](#과제-특화에서-범용으로)
- [사거나 짓거나](#사거나-짓거나)
- [모델들을 가르는 세 가지 설계 결정](#모델들을-가르는-세-가지-설계-결정)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **언어 모델이 파운데이션 모델(foundation model)이라는 다른 이름을 얻는 지점은
어디이고, 그 이름이 주장하는 바는 무엇인가.**

## 텍스트 너머로

- 한계가 동기다 — **언어 모델은 놀라운 과제를 해낼 수 있지만 텍스트에 한정된다. 사람으로서 우리는
  언어만이 아니라 시각·청각·촉각으로도 세계를 지각한다. 텍스트 너머의 데이터를 처리할 수 있는
  것은 AI가 실제 세계에서 작동하는 데 필수적이다** (1장, p.8).[^huyen2025]
- 실물 — **GPT-4V와 Claude 3는 이미지와 텍스트를 이해할 수 있다. 어떤 모델은 비디오·3D 자산·단백질
  구조까지 이해한다. 더 많은 데이터 양식(data modality)을 언어 모델에 넣으면 모델이 한층 더
  강력해진다** (1장, p.9).[^huyen2025]
- 모델 제공자 자신의 표현 — OpenAI가 2023년 GPT-4V 시스템 카드에서 밝힌 문장이다 (1장,
  p.9):[^huyen2025]

  > incorporating additional modalities (such as image inputs) into LLMs is viewed by some as a
  > key frontier in AI research and development.

## 멀티모달 모델과 LMM

- 이름의 층위 — **둘 이상의 데이터 양식을 다룰 수 있는 모델을 멀티모달 모델(multimodal model)이라
  부른다. 생성형 멀티모달 모델은 대규모 멀티모달 모델(large multimodal model, LMM)이라고도
  불린다** (1장, p.9).[^huyen2025]
- 무엇이 달라지는가 — **언어 모델이 텍스트 전용 토큰을 조건으로 다음 토큰을 생성한다면, 멀티모달
  모델은 텍스트와 이미지 토큰 둘 다를, 또는 그 모델이 지원하는 어떤 양식이든 조건으로 삼아 다음
  토큰을 생성한다** (1장, p.9).[^huyen2025]
- 왜 이것이 단절인가 — **파운데이션 모델은 AI 연구의 전통적 구조로부터의 돌파를 표시한다. 오랫동안
  AI 연구는 데이터 양식으로 나뉘어 있었다. 자연어 처리(NLP)는 텍스트만 다루고, 컴퓨터 비전은 시각만
  다뤘다. 텍스트 전용 모델은 번역·스팸 탐지 같은 과제에, 이미지 전용 모델은 객체 탐지·이미지 분류에
  쓸 수 있었다. 오디오 전용 모델은 음성 인식(speech-to-text, STT)과 음성 합성(text-to-speech,
  TTS)을 다뤘다** (1장, p.9).[^huyen2025]

## 왜 파운데이션인가

- 이름의 근거 (1장, p.9):[^huyen2025]

  > While many people still call Gemini and GPT-4V LLMs, they're better characterized as
  > *foundation models*. The word *foundation* signifies both the importance of these models in
  > AI applications and the fact that they can be built upon for different needs.

- 이 책이 이 낱말에 담는 범위 — **이 책은 파운데이션 모델이라는 용어를 대규모 언어 모델과 대규모
  멀티모달 모델 둘 다를 가리키는 데 쓴다** (1장, p.10).[^huyen2025]

## CLIP과 자연어 지도

- 규모의 문제는 여기서도 같다 — **언어 모델과 마찬가지로 멀티모달 모델도 규모를 키우려면 데이터가
  필요하다. 자기지도는 멀티모달 모델에도 통한다** (1장, p.10).[^huyen2025]
- 방법 — **예컨대 OpenAI는 자기지도의 한 변형인 자연어 지도(natural language supervision)를 써서
  언어–이미지 모델 CLIP(OpenAI, 2021)을 훈련했다. 각 이미지에 레이블을 손으로 만드는 대신 인터넷에서
  함께 나타난 (이미지, 텍스트) 쌍을 찾아냈다. 그들은 (이미지, 텍스트) 쌍 4억 개의 데이터셋을 만들
  수 있었는데, 이는 ImageNet보다 400배 크면서 수작업 레이블링 비용이 들지 않았다. 이 데이터셋은
  CLIP이 추가 훈련 없이 여러 이미지 분류 과제에 일반화할 수 있는 최초의 모델이 되게 했다** (1장,
  p.10).[^huyen2025]
- 다만 CLIP은 생성 모델이 아니다 — **CLIP은 개방형 출력을 생성하도록 훈련되지 않았다. CLIP은 텍스트와
  이미지 양쪽의 결합 임베딩을 만들도록 훈련된 임베딩 모델(embedding model)이다. 임베딩은 원 데이터의
  의미를 포착하려는 벡터로 생각할 수 있다. CLIP 같은 멀티모달 임베딩 모델은 Flamingo·LLaVA·
  Gemini(옛 Bard) 같은 생성형 멀티모달 모델의 뼈대다** (1장, p.10).[^huyen2025] 임베딩 자체의
  구조와 그 위의 색인은 [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.

## 과제 특화에서 범용으로

- 전환의 축 — **파운데이션 모델은 과제 특화 모델에서 범용 모델로의 전환도 표시한다. 이전에 모델은
  감성 분석이나 번역 같은 특정 과제를 위해 개발되는 일이 많았다. 감성 분석용으로 훈련된 모델은
  번역을 할 수 없었고 그 반대도 마찬가지였다** (1장, p.10).[^huyen2025]
- 저자가 이탤릭으로 강조하는 문장 (1장, p.10):[^huyen2025]

  > Foundation models, thanks to their scale and the way they are trained, are capable of a wide
  > range of tasks.

- 그 뒤에 따라오는 단서 — **범용 모델은 상자에서 꺼낸 그대로 많은 과제에 비교적 잘 작동한다. LLM
  하나가 감성 분석과 번역을 모두 할 수 있다. 그러나 특정 과제에서 성능을 최대화하려면 범용 모델을
  조정할 수 있는 경우가 많다** (1장, p.10).[^huyen2025]
- 저자가 든 상황 — **소매업체와 함께 웹사이트용 제품 설명을 생성하는 애플리케이션을 만든다고 하자.
  상자에서 꺼낸 그대로의 모델은 정확한 설명을 생성할 수는 있어도 브랜드의 목소리를 담아내거나 브랜드
  메시지를 부각하지 못할 수 있다. 생성된 설명이 마케팅 상투어와 진부한 표현으로 가득할 수도 있다**
  (1장, p.10).[^huyen2025]
- 그래서 세 가지 기법이 나온다 — **바람직한 제품 설명의 예를 담은 상세한 지시를 지어낼 수 있고
  (프롬프트 엔지니어링), 모델이 더 나은 설명을 생성하는 데 활용할 고객 리뷰 데이터베이스에 모델을
  연결할 수 있으며(검색 증강 생성, RAG), 고품질 제품 설명 데이터셋으로 모델을 더 훈련할 수도 있다
  (파인 튜닝). 프롬프트 엔지니어링·RAG·파인 튜닝은 모델을 필요에 맞게 적응시키는 데 쓸 수 있는 매우
  흔한 세 가지 AI 엔지니어링 기법이다** (1장, p.11).[^huyen2025] 이 세 기법의 분류 축은
  [모델 적응 기법](../concepts/model-adaptation-techniques.md)에 있다.

## 사거나 짓거나

- 적응이 신축보다 싸다 — **당신의 과제에 기존의 강력한 모델을 적응시키는 것은 그 과제를 위한 모델을
  처음부터 만드는 것보다 대체로 훨씬 쉽다. 예컨대 예제 열 개와 주말 하나 대 예제 100만 개와 여섯
  달이다. 파운데이션 모델은 AI 애플리케이션을 개발하는 비용을 낮추고 출시까지의 시간을 줄인다** (1장,
  p.12).[^huyen2025]
- 다만 과제 특화 모델이 사라지지는 않는다 — **모델을 적응시키는 데 정확히 얼마나 많은 데이터가
  필요한지는 어떤 기법을 쓰느냐에 달려 있다. 그럼에도 과제 특화 모델에는 여전히 많은 이점이 있다.
  예컨대 훨씬 작아서 더 빠르고 쓰기에 더 쌀 수 있다** (1장, p.12).[^huyen2025]
- 그래서 남는 결정 — **자기 모델을 만들 것인가 기존 모델을 활용할 것인가는 팀이 스스로 답해야 하는
  고전적인 사거나 짓거나(buy-or-build) 질문이다** (1장, p.12).[^huyen2025]

## 모델들을 가르는 세 가지 설계 결정

- 모델을 쓰는 쪽이 무엇을 알아야 하는가 — **파운데이션 모델로 애플리케이션을 만들려면 먼저
  파운데이션 모델이 필요하다. 모델을 쓰려고 모델 개발법을 알아야 하는 것은 아니지만, 높은 수준의
  이해는 어떤 모델을 쓸지, 그것을 어떻게 필요에 맞게 적응시킬지 결정하는 데 도움이 된다** (2장,
  p.49).[^huyen2025]
- 그 이해가 걸리는 축 (2장, p.49):[^huyen2025]

  > With the growing lack of transparency in the training process of foundation models, it's
  > difficult to know all the design decisions that go into making a model. In general, however,
  > differences in foundation models can be traced back to decisions about training data, model
  > architecture and size, and how they are post-trained to align with human preferences.

- 세 축은 각각 다음 페이지가 맡는다.
  - 훈련 데이터 — [훈련 데이터 큐레이션](../concepts/training-data-curation.md),
    [다국어 모델](../concepts/multilingual-models.md),
    [도메인 특화 모델](../concepts/domain-specific-models.md)
  - 모델 구조와 크기 — [트랜스포머 구조](../concepts/transformer-architecture.md),
    [대안 모델 구조](../concepts/alternative-model-architectures.md),
    [모델 규모의 세 수치](../concepts/model-size-and-scale.md),
    [스케일링 법칙](../concepts/scaling-laws.md)
  - 사후 훈련 — [지도 파인 튜닝](../concepts/supervised-finetuning.md),
    [선호 파인 튜닝](../concepts/preference-finetuning.md)
- 저자가 이 축들에 덧붙이는 네 번째 관심사가 샘플링이다 — **대부분의 사람이 훈련이 모델 성능에
  미치는 영향은 이해하지만 샘플링의 영향은 흔히 간과된다** (2장, p.50).[^huyen2025] 그쪽은
  [샘플링 전략](../concepts/sampling-strategies.md)이 맡는다.

## 이어지는 페이지

- [언어 모델과 토큰](../concepts/language-models-and-tokens.md) — 이 모델의 출발점이 된 텍스트
  전용 모델
- [자기지도와 모델 규모](../concepts/self-supervision-and-model-scale.md) — CLIP의 자연어 지도가
  변형인 그 훈련 방식
- [AI 엔지니어링이란](../concepts/ai-engineering-defined.md) — 이 모델 위에서 애플리케이션을 짓는
  일에 붙은 이름
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프트 엔지니어링·RAG·파인
  튜닝을 가르는 축
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — CLIP이 속한 임베딩 모델의
  계보와 그 색인
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 이 모델들이 실제로 어떤 모양으로
  지어져 있는가

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48)과 2장 "Understanding Foundation Models" 도입부(책 pp.49–50). 도판 Figure 1-3
    (멀티모달 모델의 다음 토큰 생성)과 Figure 1-4(Super-NaturalInstructions 벤치마크의 과제
    분포 — Wang et al., 2022)는 옮기지 않았다.

---
type: concept
title: 언어 모델과 토큰
status: draft
description: 언어 모델이 담는 것은 낱말이 어떤 맥락에 나타날 확률이고, 그 기본 단위는 낱말이 아니라 토큰이다 — 토큰화와 어휘 크기, 앞뒤를 다 보는 마스크드 모델과 앞만 보는 자기회귀 모델의 갈림, 그리고 번역도 분류도 완성 과제로 흡수하는 완성 기계라는 관점
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 언어 모델과 토큰

- [언어 모델이 담는 것](#언어-모델이-담는-것)
- [토큰과 토큰화](#토큰과-토큰화)
- [왜 낱말이 아니라 토큰인가](#왜-낱말이-아니라-토큰인가)
- [마스크드와 자기회귀](#마스크드와-자기회귀)
- [완성 기계](#완성-기계)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **언어 모델(language model)은 무엇을 담고 있고, 그것을 세는 단위는 왜 낱말이 아닌가.**

## 언어 모델이 담는 것

- 정의는 통계다 (1장, p.2):[^huyen2025]

  > A *language model* encodes statistical information about one or more languages.
  > Intuitively, this information tells us how likely a word is to appear in a given context.

- 저자가 든 예 — **맥락 "My favorite color is __"가 주어지면, 영어를 인코딩한 언어 모델은
  "car"보다 "blue"를 더 자주 예측해야 한다** (1장, p.2).[^huyen2025]
- 언어의 통계적 성질은 새 발견이 아니다 — **1905년 셜록 홈스 이야기 「The Adventure of the
  Dancing Men」에서 홈스는 영어의 단순 통계로 수수께끼 막대 그림을 해독했다. 영어에서 가장 흔한
  글자가 E이므로 가장 흔한 막대 그림이 E를 가리킨다고 추론한 것이다** (1장, p.3).[^huyen2025]
- 그 뒤 **클로드 섀넌(Claude Shannon)이 2차 대전 중 적의 메시지를 해독하는 데 더 정교한 통계를
  썼고, 영어를 모델링하는 법에 대한 그의 작업은 1951년의 이정표 논문 「Prediction and Entropy of
  Printed English」로 발표되었다. 엔트로피를 포함해 그 논문이 도입한 많은 개념이 오늘날의 언어
  모델링에서 여전히 쓰인다** (1장, p.3).[^huyen2025]
- 범위가 바뀌었다 — **초기에는 언어 모델 하나가 언어 하나를 다뤘지만 오늘날의 언어 모델은 여러
  언어를 다룰 수 있다** (1장, p.3).[^huyen2025]

## 토큰과 토큰화

- 기본 단위의 정의 (1장, p.3):[^huyen2025]

  > The basic unit of a language model is *token*. A token can be a character, a word, or a
  > part of a word (like -tion), depending on the model.

  - 각주로 붙은 단서 — **비영어 언어에서는 단일 유니코드 문자 하나가 여러 토큰으로 표현되기도
    한다** (1장, p.3 각주 2).[^huyen2025]
- 실물 — **ChatGPT 뒤의 모델인 GPT-4는 "I can't wait to build AI applications"라는 구를 아홉 개의
  토큰으로 쪼갠다. 이 예에서 "can't"는 `can`과 `'t`의 두 토큰으로 갈린다** (1장,
  p.3).[^huyen2025]
- **원래 텍스트를 토큰으로 쪼개는 과정을 토큰화(tokenization)라고 한다. GPT-4에서 평균 토큰
  하나는 대략 낱말 길이의 4분의 3이다. 그래서 100개 토큰은 대략 75개 낱말이다** (1장,
  p.3).[^huyen2025]
- 어휘 — **모델이 다룰 수 있는 모든 토큰의 집합이 그 모델의 어휘(vocabulary)다. 알파벳 몇 글자로
  많은 낱말을 만들 수 있듯, 적은 수의 토큰으로 서로 다른 낱말을 많이 만들 수 있다. Mixtral 8x7B
  모델의 어휘 크기는 32,000이고 GPT-4의 어휘 크기는 100,256이다. 토큰화 방법과 어휘 크기는 모델
  개발자가 정한다** (1장, p.3).[^huyen2025]
- 토큰화 효율은 언어마다 크게 갈리고 그것이 곧 지연과 요금이 된다 — **MASSIVE 데이터셋에서 중앙값
  토큰 길이는 영어가 7인데 힌디어는 32, 버마어는 72다** (2장, p.55).[^huyen2025] 그 대가의 전모는
  [다국어 모델](../concepts/multilingual-models.md)에 있다.

## 왜 낱말이 아니라 토큰인가

- 저자가 세 가지 이유를 든다 (1장, p.4):[^huyen2025]
  - **문자와 비교하면, 토큰은 모델이 낱말을 의미 있는 구성 요소로 쪼갤 수 있게 해 준다. 예컨대
    "cooking"은 "cook"과 "ing"으로 쪼개질 수 있고 두 구성 요소 모두 원래 낱말의 의미를 얼마간
    지닌다.**
  - **고유한 토큰이 고유한 낱말보다 적기 때문에, 이는 모델의 어휘 크기를 줄여 모델을 더
    효율적으로 만든다.**
  - **토큰은 모델이 모르는 낱말을 처리하는 것도 돕는다. 예컨대 "chatgpting" 같은 지어낸 낱말은
    "chatgpt"와 "ing"으로 갈려 모델이 그 구조를 이해하도록 돕는다. 토큰은 낱말보다 단위 수가
    적으면서 개별 문자보다 더 많은 의미를 지니는 균형을 잡는다.**

## 마스크드와 자기회귀

- **언어 모델에는 두 가지 주된 종류가 있다 — 마스크드 언어 모델(masked language model)과 자기회귀
  언어 모델(autoregressive language model). 둘은 토큰을 예측할 때 어떤 정보를 쓸 수 있는가로
  갈린다** (1장, p.4).[^huyen2025]
- 마스크드 언어 모델 (1장, p.4):[^huyen2025]

  > A masked language model is trained to predict missing tokens anywhere in a sequence,
  > *using the context from both before and after the missing tokens*.

  - 저자가 든 예 — **맥락 "My favorite __ is blue"가 주어지면 마스크드 언어 모델은 빈칸이 "color"일
    가능성이 높다고 예측해야 한다. 잘 알려진 예가 BERT(bidirectional encoder representations from
    transformers, Devlin et al., 2018)다** (1장, p.4).[^huyen2025]
  - 쓰이는 자리 — **집필 시점 기준 마스크드 언어 모델은 감성 분석·텍스트 분류 같은 비생성
    과제에 흔히 쓰인다. 앞뒤 코드를 모두 이해해 오류를 짚어야 하는 코드 디버깅처럼 전체 맥락의
    이해가 필요한 과제에도 유용하다** (1장, p.4).[^huyen2025]
- 자기회귀 언어 모델 (1장, p.4):[^huyen2025]

  > An autoregressive language model is trained to predict the next token in a sequence,
  > *using only the preceding tokens*.

  - **자기회귀 모델은 토큰 하나 뒤에 또 하나를 계속 생성할 수 있다. 오늘날 자기회귀 언어 모델은
    텍스트 생성에서 선택되는 모델이고, 그 이유로 마스크드 언어 모델보다 훨씬 인기가 있다** (1장,
    pp.4–5).[^huyen2025] 각주에 붙은 다른 이름 — **자기회귀 언어 모델은 인과 언어 모델(causal
    language models)이라고도 불린다** (1장, p.4 각주 3).[^huyen2025]
- 이 책의 약속 — **명시하지 않는 한 이 책에서 "언어 모델"은 자기회귀 모델을 가리킨다** (1장,
  p.5).[^huyen2025]

## 완성 기계

- 출력이 열려 있다 — **언어 모델의 출력은 개방형(open-ended)이다. 언어 모델은 고정된 유한한
  어휘로 무한히 많은 출력을 구성할 수 있다. 개방형 출력을 생성할 수 있는 모델을
  생성형(generative)이라 부르며, 여기서 생성형 AI(generative AI)라는 용어가 나온다** (1장,
  p.5).[^huyen2025]
- 관점 하나 — **언어 모델을 완성 기계(completion machine)로 생각할 수 있다. 텍스트(프롬프트)가
  주어지면 그 텍스트를 완성하려 한다** (1장, p.5).[^huyen2025] 책이 든 예는 사용자 프롬프트
  `"To be or not to be"`에 대해 모델이 `", that is the question."`를 내놓는 것이다 (1장,
  p.5).[^huyen2025]
- 경고가 곧바로 따라온다 — **완성은 예측이고 확률에 근거하며 옳다는 보장이 없다. 언어 모델의 이
  확률적 성질이 그것을 쓰는 일을 그토록 신나면서도 답답하게 만든다** (1장, p.5).[^huyen2025]
  - 이 확률이 실제로 만들어지고 소비되는 경로는 2장이 연다 — **언어 모델에서 다음 토큰을
    생성하려면 모델은 먼저 어휘 안의 모든 토큰에 대한 확률 분포를 계산한다** (2장,
    p.89).[^huyen2025] 그 분포에서 토큰 하나를 뽑는 방법은
    [샘플링 전략](../concepts/sampling-strategies.md)이, 그 확률성이 낳는 비일관성과 환각은
    [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md)이 맡는다.
- 완성이라는 틀이 삼키는 것 — **번역·요약·코딩·수학 문제 풀이를 포함한 많은 과제가 완성 과제로
  틀 지어질 수 있다. 예컨대 프롬프트 "How are you in French is …"가 주어지면 언어 모델은
  "Comment ça va"로 완성해 사실상 한 언어에서 다른 언어로 번역하게 된다** (1장,
  p.6).[^huyen2025]
- 분류도 마찬가지다 — 프롬프트가 `Question: Is this email likely spam? Here's the email:
  <email content>` 뒤에 `Answer:`로 끝나면 **언어 모델은 "Likely spam"으로 완성할 수 있고, 이는 이
  언어 모델을 스팸 분류기로 바꾼다** (1장, p.6).[^huyen2025]
- 완성의 한계 — **완성이 강력하긴 하지만 완성은 대화에 참여하는 것과 같지 않다. 예컨대 완성
  기계에 질문을 하면 그 기계는 질문에 답하는 대신 질문을 하나 더 덧붙여 당신이 한 말을 완성할 수
  있다** (1장, p.6).[^huyen2025] 사용자의 요청에 알맞게 응답하도록 만드는 일은
  [모델 적응 기법](../concepts/model-adaptation-techniques.md)이 다루는 사후 훈련의 몫이다.

## 이어지는 페이지

- [자기지도와 모델 규모](../concepts/self-supervision-and-model-scale.md) — 이 모델들이 규모를
  키울 수 있었던 훈련 방식과 "large"의 기준
- [파운데이션 모델](../concepts/foundation-models.md) — 텍스트 밖의 양식이 들어오면서 언어 모델이
  다른 이름을 얻는 지점
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 완성 기계를 쓸 만한 조수로 만드는
  훈련 단계와 적응 기법
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 같은 토큰을 수치 벡터로
  옮기는 쪽
- [샘플링 전략](../concepts/sampling-strategies.md) — 어휘 위의 확률 분포에서 실제 토큰이 뽑히는
  과정
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 이 토큰들이 처리되는 구조
- [다국어 모델](../concepts/multilingual-models.md) — 토큰화 효율이 언어마다 갈리는 자리

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48)과 2장 "Understanding Foundation Models"(책 pp.49–112) 중 토큰화 효율(p.55)·
    다음 토큰 확률 분포(p.89) 대목. 이 절의 도판 Figure 1-1(GPT-4의 토큰화 예)과 Figure 1-2
    (자기회귀·마스크드 모델 대비 그림)는 옮기지 않았고 본문 서술만 담았다.

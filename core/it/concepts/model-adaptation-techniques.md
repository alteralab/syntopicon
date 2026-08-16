---
type: concept
title: 모델 적응 기법
description: 남이 훈련한 모델을 내 과제에 맞추는 기법들이 가중치를 고치는가로 갈린다 — 프롬프트 기반 기법과 파인 튜닝이 각각 요구하는 데이터와 얻는 것, 그리고 훈련·사전 훈련·파인 튜닝·사후 훈련이라는 낱말들이 실제로 가리키는 서로 다른 단계
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 모델 적응 기법

- [가중치를 고치는가가 축이다](#가중치를-고치는가가-축이다)
- [프롬프트 기반 기법](#프롬프트-기반-기법)
- [파인 튜닝](#파인-튜닝)
- [훈련이라는 낱말이 가리키는 단계들](#훈련이라는-낱말이-가리키는-단계들)
- [훈련이 아닌 것을 훈련이라 부를 때](#훈련이-아닌-것을-훈련이라-부를-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델을 내 과제에 맞춘다는 것은 구체적으로 무엇을 바꾸는 일인가.**

## 가중치를 고치는가가 축이다

- 분류의 기준 (1장, p.40):[^huyen2025]

  > In general, model adaptation techniques can be divided into two categories, depending on
  > whether they require updating model weights.

- 저자가 이 절을 두는 이유 — **이 장에서 모델 적응을 여러 번 언급했으므로, 다음으로 넘어가기 전에
  모델 적응이 무엇을 뜻하는지에 대해 우리가 같은 페이지에 있는지 확인하고 싶다** (1장,
  p.40).[^huyen2025]
- 앞서 1장이 세 기법을 이름으로 든 자리가 있다 — **프롬프트 엔지니어링(prompt engineering)·검색 증강
  생성(retrieval-augmented generation, RAG)·파인 튜닝(finetuning)은 모델을 필요에 맞게 적응시키는 데
  쓸 수 있는 매우 흔한 세 가지 AI 엔지니어링 기법이다** (1장, p.11).[^huyen2025]
- 데이터 요구량은 기법 순서로 늘어난다 — **얼마나 많은 데이터가 필요한지는 어떤 어댑터 기법을 쓰느냐에
  달려 있다. 모델을 처음부터 훈련하는 것은 일반적으로 파인 튜닝보다 더 많은 데이터를 요구하고, 파인
  튜닝은 다시 프롬프트 엔지니어링보다 더 많은 데이터를 요구한다** (1장, p.43).[^huyen2025]

## 프롬프트 기반 기법

- 정의 (1장, p.40):[^huyen2025]

  > *Prompt-based techniques, which include prompt engineering, adapt a model without updating the
  > model weights.*

- 무엇을 하는가 — **모델 자체를 바꾸는 대신 지시와 맥락을 주어 모델을 적응시킨다. 프롬프트 엔지니어링은
  시작하기 더 쉽고 데이터를 덜 요구한다. 많은 성공적 애플리케이션이 프롬프트 엔지니어링만으로
  지어졌다** (1장, p.40).[^huyen2025]
- 부수 효과 — **쓰기 쉽다는 점은 더 많은 모델로 실험할 수 있게 하고, 이는 당신의 애플리케이션에 뜻밖에
  잘 맞는 모델을 찾을 확률을 높인다** (1장, p.40).[^huyen2025]
- 한계 — **그러나 프롬프트 엔지니어링은 복잡한 과제나 엄격한 성능 요건을 가진 애플리케이션에는 충분하지
  않을 수 있다** (1장, p.40).[^huyen2025]

## 파인 튜닝

- 정의 (1장, p.40):[^huyen2025]

  > *Finetuning, on the other hand, requires updating model weights.*

- 무엇을 하는가 — **모델 자체에 변경을 가해 모델을 적응시킨다. 일반적으로 파인 튜닝 기법은 더 복잡하고
  더 많은 데이터를 요구하지만, 모델의 품질·지연·비용을 크게 개선할 수 있다** (1장,
  p.40).[^huyen2025]
- 가중치를 고쳐야만 되는 일이 있다 — **가중치를 바꾸지 않고는 가능하지 않은 것이 많다. 훈련 중에 노출되지
  않은 새 과제에 모델을 적응시키는 것 같은 것이다** (1장, p.40).[^huyen2025]

## 훈련이라는 낱말이 가리키는 단계들

- 경계부터 — **훈련(training)은 언제나 모델 가중치를 바꾸는 것을 수반하지만, 모델 가중치에 대한 모든
  변경이 훈련인 것은 아니다. 예컨대 모델 가중치의 정밀도를 낮추는 과정인 양자화(quantization)는 기술적으로
  모델의 가중치 값을 바꾸지만 훈련으로 여겨지지 않는다** (1장, p.41).[^huyen2025]
- **훈련이라는 용어는 서로 다른 훈련 국면을 가리키는 사전 훈련·파인 튜닝·사후 훈련을 대신해 쓰이는 일이
  많다** (1장, p.41).[^huyen2025]
- 사전 훈련(pre-training) (1장, p.41):[^huyen2025]

  > *Pre-training refers to* training a model from scratch—the model weights are randomly
  > initialized. For LLMs, pre-training often involves training a model for text completion.

  - 자원 비중 — **모든 훈련 단계 중에서 사전 훈련은 대개 압도적으로 자원 집약적이다. InstructGPT
    모델의 경우 사전 훈련이 전체 컴퓨트와 데이터 자원의 최대 98%를 차지한다. 사전 훈련은 시간도 오래
    걸린다. 사전 훈련 중의 작은 실수가 상당한 재정 손실을 일으키고 프로젝트를 크게 후퇴시킬 수 있다**
    (1장, p.41).[^huyen2025]
  - 그래서 하는 사람이 적다 — **사전 훈련의 자원 집약적 성격 때문에 이것은 소수만이 실행하는 기예가
    되었다. 다만 대형 모델 사전 훈련에 전문성을 가진 사람들은 크게 수요가 있다** (1장,
    p.41).[^huyen2025]
- 파인 튜닝(finetuning) (1장, p.42):[^huyen2025]

  > *Finetuning* means continuing to train a previously trained model—the model weights are
  > obtained from the previous training process.

  - **모델이 사전 훈련에서 이미 어떤 지식을 갖고 있기 때문에 파인 튜닝은 통상 사전 훈련보다 적은
    자원(예: 데이터와 컴퓨트)을 요구한다** (1장, p.42).[^huyen2025]
- 사후 훈련(post-training) — **많은 사람이 사후 훈련을 사전 훈련 국면 이후에 모델을 훈련하는 과정을
  가리키는 데 쓴다. 개념적으로 사후 훈련과 파인 튜닝은 같고 서로 바꿔 쓸 수 있다. 그러나 때때로 사람들은
  다른 목표를 나타내려고 둘을 다르게 쓸 수 있다. 모델 개발자가 하면 대개 사후 훈련이다. 예컨대 OpenAI는
  모델을 공개하기 전에 지시를 더 잘 따르도록 사후 훈련할 수 있다. 애플리케이션 개발자가 하면 파인
  튜닝이다. 예컨대 당신은 (그 자체로 사후 훈련되었을 수 있는) OpenAI 모델을 당신의 필요에 맞게 파인
  튜닝할 수 있다** (1장, p.42).[^huyen2025]
  - 사후 훈련이 실제로 무엇으로 이뤄지는지는 2장이 채운다 — **일반적으로 사후 훈련은 두 단계로
    이뤄진다: 지도 파인 튜닝(SFT)과 선호 파인 튜닝** (2장, p.78).[^huyen2025] 각각
    [지도 파인 튜닝](../concepts/supervised-finetuning.md)과
    [선호 파인 튜닝](../concepts/preference-finetuning.md)이 맡는다.
- 둘은 스펙트럼이다 — **사전 훈련과 사후 훈련은 하나의 스펙트럼을 이룬다. 그 과정과 도구는 매우
  비슷하다** (1장, p.42).[^huyen2025]
  - 각주에 붙은 저자의 불평 — **"pre-training"과 "post-training"이라는 용어에 상상력이 부족하다고
    느낀다면 당신만 그런 것이 아니다. AI 연구 공동체는 많은 것을 잘하지만 이름 짓기는 그중 하나가 아니다.
    "large language models"가 "large"라는 낱말의 모호함 때문에 과학적 용어라 하기 어렵다는 것은 이미
    이야기했다. 그리고 나는 사람들이 "X is all you need"라는 제목의 논문을 그만 냈으면 정말 좋겠다**
    (1장, p.42 각주 25).[^huyen2025]

## 훈련이 아닌 것을 훈련이라 부를 때

- 흔한 혼동 — **어떤 사람들은 훈련이라는 용어를 프롬프트 엔지니어링을 가리키는 데 쓰는데 그것은 옳지
  않다. 나는 어느 Business Insider 기사에서 저자가 어린 시절 일기를 ChatGPT에 넣어 자기 어린 자아를
  흉내 내도록 ChatGPT를 훈련시켰다고 말하는 것을 읽었다. 구어적으로 저자의 "training"이라는 낱말 사용은
  옳은데, 모델에게 무언가를 하도록 가르치고 있기 때문이다. 그러나 기술적으로 모델에 입력되는 맥락을 통해
  모델에게 무엇을 할지 가르친다면 당신이 하고 있는 것은 프롬프트 엔지니어링이다. 비슷하게 사람들이 실제로
  하는 일이 프롬프트 엔지니어링인데 파인 튜닝이라는 용어를 쓰는 것도 보았다** (1장,
  p.42).[^huyen2025]

## 이어지는 페이지

- [AI 엔지니어링과 ML 엔지니어링](../concepts/ai-engineering-versus-ml-engineering.md) — 적응이 이
  분야의 중심이 된 경위
- [파운데이션 모델](../concepts/foundation-models.md) — 적응의 대상이 되는 범용 모델
- [모델 개발 층](../concepts/ai-model-development-layer.md) — 파인 튜닝과 데이터셋 엔지니어링이 사는 층
- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 프롬프트 엔지니어링과 맥락
  구성이 사는 층
- [언어 모델과 토큰](../concepts/language-models-and-tokens.md) — 사전 훈련이 목표로 삼는 텍스트 완성
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 사후 훈련의 첫 단계가 실제로 하는 일
- [선호 파인 튜닝](../concepts/preference-finetuning.md) — 둘째 단계와 RLHF
- [구조화 출력](../concepts/structured-outputs.md) — 프롬프팅과 파인 튜닝이 같은 목표를 놓고
  견줘지는 실물

[^huyen2025]: Huyen 2025, 1장 "Introduction to Building AI Applications with Foundation Models"
    (책 pp.1–48)과 2장 "Understanding Foundation Models"의 사후 훈련 도입(책 p.78). 훈련 용어
    구분은 pp.41–42의 사이드바 "On the Differences Among Training, Pre-Training, Finetuning,
    and Post-Training"에서 왔다. 이 절에는 도판이 없다.

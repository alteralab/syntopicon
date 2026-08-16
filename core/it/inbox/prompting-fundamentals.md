---
type: concept
title: 프롬프팅의 기본
status: draft
description: 프롬프트란 무엇이고 프롬프트 엔지니어링이 왜 공학인가 — 가중치를 건드리지 않는 가장 쉽고 흔한 적응 기법이라는 규정, 과제 서술·예시·과제라는 프롬프트의 세 부분, 프롬프팅이 성립하려면 모델이 지시를 따를 수 있어야 한다는 전제, 그리고 사소한 변형에 출력이 흔들리는 정도로 정의되는 견고성과 그것이 필요한 손질의 양을 정한다는 관계
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 프롬프팅의 기본

- [가장 쉽고 흔한 적응 기법](#가장-쉽고-흔한-적응-기법)
- [쉬워 보인다는 것이 문제다](#쉬워-보인다는-것이-문제다)
- [프롬프트의 세 부분](#프롬프트의-세-부분)
- [지시를 따를 수 있어야 프롬프팅이 성립한다](#지시를-따를-수-있어야-프롬프팅이-성립한다)
- [견고성이 손질의 양을 정한다](#견고성이-손질의-양을-정한다)
- [프롬프트의 핵심 구성 요소](#프롬프트의-핵심-구성-요소)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프롬프트는 무엇으로 이뤄져 있고, 프롬프팅이 통하려면 모델 쪽에 무엇이
갖춰져 있어야 하는가.**

## 가장 쉽고 흔한 적응 기법

- 규정 (5장, p.211):[^huyen2025]

  > Prompt engineering refers to the process of crafting an instruction that gets a model to
  > generate the desired outcome. Prompt engineering is the easiest and most common model
  > adaptation technique. Unlike finetuning, prompt engineering guides a model's behavior without
  > changing the model's weights.

- 순서에 대한 저자의 조언 — **파운데이션 모델의 강한 기반 역량 덕분에 많은 사람이 프롬프트
  엔지니어링(prompt engineering)만으로 모델을 자기 애플리케이션에 성공적으로 적응시켰다. 파인 튜닝
  같은 더 자원 집약적인 기법으로 넘어가기 전에 프롬프팅에서 최대한을 뽑아내야 한다** (5장,
  p.211).[^huyen2025]

## 쉬워 보인다는 것이 문제다

- **프롬프트 엔지니어링의 쓰기 쉬움은 사람들을 오도해 여기에 별것이 없다고 생각하게 만들 수 있다.
  언뜻 보면 프롬프트 엔지니어링은 무언가가 통할 때까지 낱말을 만지작거리는 일로 보인다. 프롬프트
  엔지니어링이 실제로 많은 만지작거림을 수반하는 것은 맞지만, 거기에는 흥미로운 난제와 기발한 해법도
  많이 들어 있다** (5장, p.211).[^huyen2025]
  - 각주가 전하는 분위기 — **짧은 존재 기간 동안 프롬프트 엔지니어링은 놀랄 만한 양의 적의를 만들어
    냈다. 프롬프트 엔지니어링이 진짜가 아니라는 불평은 수천 개의 지지 댓글을 모았다. 저자가 다가올
    자기 책에 프롬프트 엔지니어링 장이 있다고 말하자 많은 사람이 눈을 굴렸다** (5장, p.211
    각주 1).[^huyen2025]
- 저자가 잡는 비유 — **프롬프트 엔지니어링을 인간 대 AI 소통(human-to-AI communication)으로 생각할 수
  있다. 당신이 원하는 것을 하게 하려고 AI 모델과 소통하는 것이다. 누구나 소통할 수 있지만 누구나
  효과적으로 소통하지는 못한다. 마찬가지로 프롬프트를 쓰기는 쉽지만 효과적인 프롬프트를 구성하기는
  쉽지 않다** (5장, p.211).[^huyen2025]
- 공학이냐는 시비에 대한 답 — **어떤 사람들은 "프롬프트 엔지니어링"이 공학 분과로 인정받을 만한
  엄밀성을 결여한다고 주장한다. 그러나 그럴 필요는 없다. 프롬프트 실험은 어떤 ML 실험과도 같은
  엄밀성으로, 체계적인 실험과 평가와 함께 수행되어야 한다** (5장, p.211).[^huyen2025]
- 저자가 인터뷰한 OpenAI 연구 관리자의 요약 (5장, pp.211–212):[^huyen2025]

  > The problem is not with prompt engineering. It's a real and useful skill to have. The problem
  > is when prompt engineering is the only thing people know.

  - 그래서 무엇이 더 필요한가 — **프로덕션 준비가 된 AI 애플리케이션을 지으려면 프롬프트 엔지니어링
    이상이 필요하다. 실험 추적·평가·데이터셋 큐레이션을 하려면 통계·공학·고전 ML 지식이 필요하다**
    (5장, p.212).[^huyen2025]

## 프롬프트의 세 부분

- 정의 (5장, p.212):[^huyen2025]

  > A prompt is an instruction given to a model to perform a task.

  - 과제의 폭 — **과제는 "누가 숫자 0을 발명했는가?"처럼 질문에 답하는 것만큼 단순할 수도 있고,
    당신의 제품 아이디어를 위해 경쟁사를 조사하거나 웹사이트를 처음부터 짓거나 당신의 데이터를
    분석하라고 요청하는 것처럼 더 복잡할 수도 있다** (5장, p.212).[^huyen2025]
- **프롬프트는 일반적으로 다음 부분 중 하나 이상으로 이뤄진다** (5장, p.212):[^huyen2025]
  1. **과제 서술(task description) — 모델이 무엇을 하기를 원하는가. 모델이 맡기를 원하는 역할과
     출력 형식을 포함한다.**
  2. **이 과제를 하는 방법의 예시(example(s) of how to do this task) — 예컨대 모델이 텍스트에서
     독성을 탐지하기를 원한다면 독성과 비독성이 어떻게 생겼는지의 예를 몇 개 줄 수 있다.**
  3. **과제(the task) — 모델이 하기를 원하는 구체적 과제. 답할 질문이나 요약할 책 같은 것.**
- 저자가 든 실물은 개체명 인식(named-entity recognition, NER) 과제의 아주 단순한 프롬프트이고, 위
  세 부분이 그 안에서 어디인지 표시되어 있다 (5장, p.212, Figure 5-1):[^huyen2025]

  ```text
  Given a text, extract all entities. Output only the list of
  extracted entities, separated by commas, and nothing else.

  Text: "Brave New World is a dystopian novel written by Aldous
  Huxley, first published in 1932."
  Entities: Brave New World, Aldous Huxley

  Text: ${THE TEXT THAT YOU WANT TO EXTRACT ENTITIES FROM}
  Entities:
  ```

  - 위에서부터 첫 문단이 과제 서술, 둘째 덩어리가 예시, 마지막 두 줄이 과제다 (5장, p.212,
    Figure 5-1).[^huyen2025]

## 지시를 따를 수 있어야 프롬프팅이 성립한다

- 전제 (5장, pp.212–213):[^huyen2025]

  > *For prompting to work, the model has to be able to follow instructions.* If a model is bad at
  > it, it doesn't matter how good your prompt is, the model won't be able to follow it.

  - 그 능력을 재는 방법은 4장이 담당한다 (5장, p.213).[^huyen2025] 이 KB에서는
    [지시 따르기 역량](../concepts/instruction-following-capability.md)이 그 자리다.

## 견고성이 손질의 양을 정한다

- 무엇이 양을 정하는가 (5장, p.213):[^huyen2025]

  > *How much prompt engineering is needed depends on how robust the model is to prompt
  > perturbation.*

- 무엇이 섭동인가 — **프롬프트가 조금 바뀌면 — "five" 대신 "5"라고 쓰거나, 새 줄을 넣거나,
  대소문자를 바꾸는 것처럼 — 모델의 응답이 극적으로 달라지는가? 모델이 덜 견고할수록 더 많은
  만지작거림이 필요하다** (5장, p.213).[^huyen2025]
- 어떻게 재는가 — **프롬프트를 무작위로 섭동시켜 출력이 어떻게 바뀌는지 봄으로써 모델의
  견고성(robustness)을 잴 수 있다. 지시 따르기 역량과 마찬가지로 모델의 견고성은 그 전반적 역량과
  강하게 상관된다. 모델이 강해질수록 더 견고해지기도 한다. 지능적인 모델이라면 "5"와 "five"가 같은
  것을 뜻한다고 이해해야 하므로 이는 말이 된다. 이런 이유로 더 강한 모델과 일하는 것이 흔히 골치를
  덜고 만지작거림에 낭비하는 시간을 줄여 준다** (5장, p.213).[^huyen2025]
  - 각주의 실측 — **2023년 말 스탠퍼드는 자기 HELM Lite 벤치마크에서 견고성을 뺐다** (5장, p.213
    각주 2).[^huyen2025]
- 저자의 조언 상자 — **어떤 프롬프트 구조가 당신에게 가장 잘 통하는지 알아내려면 서로 다른 구조로
  실험하라. GPT-4를 포함한 대부분의 모델은 과제 서술이 프롬프트의 시작에 있을 때 경험적으로 더 잘
  수행한다. 그러나 Llama 3를 포함한 어떤 모델은 과제 서술이 프롬프트의 끝에 있을 때 더 잘 수행하는
  것으로 보인다** (5장, p.213).[^huyen2025]

## 프롬프트의 핵심 구성 요소

- 저자가 이 절을 닫으며 묶는 것 — **시스템 프롬프트·사용자 프롬프트·예시·맥락이 프롬프트의 핵심
  구성 요소다** (5장, p.220).[^huyen2025] 각각
  [시스템 프롬프트와 사용자 프롬프트](../concepts/system-prompt-and-user-prompt.md)·
  [인컨텍스트 학습](../concepts/in-context-learning.md)·
  [프롬프트에 맥락 주기](../concepts/providing-context-in-prompts.md)가 맡는다.

## 이어지는 페이지

- [인컨텍스트 학습](../concepts/in-context-learning.md) — 예시로 가르치는 일이 왜 가능한가
- [시스템 프롬프트와 사용자 프롬프트](../concepts/system-prompt-and-user-prompt.md) — 프롬프트가 둘로
  갈리는 자리와 채팅 템플릿
- [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md) — 프롬프트에 넣을 수
  있는 양의 한계
- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 과제 서술을 쓰는 관행
- [지시 따르기 역량](../concepts/instruction-following-capability.md) — 프롬프팅의 전제가 되는 능력을
  재는 자리
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프트 엔지니어링이 속한 분류
- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 프롬프트 엔지니어링이
  책임으로 놓인 층
- [방어적 프롬프트 엔지니어링](../concepts/defensive-prompt-engineering.md) — 같은 장의 뒷절이 여는
  공격 쪽 축

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 장 도입(pp.211–212)과
    "Introduction to Prompting" 절의 앞부분(pp.212–213), 그리고 그 절을 닫는 한 문장(p.220)을 담았다.
    Figure 5-1(세 부분이 중괄호로 표시된 NER 프롬프트, p.212)은 프롬프트 본문을 그대로 옮기고 부분
    이름은 산문으로 풀었다 — 도판의 중괄호와 화살표 조판은 옮기지 않았다.

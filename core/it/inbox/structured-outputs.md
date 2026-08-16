---
type: concept
title: 구조화 출력
description: 확률적 모델에게 형식을 지키게 만드는 네 가지 자리 — 구조화 출력이 필요한 두 시나리오, 프롬프팅과 후처리라는 값싼 반창고, 로짓을 걸러 내는 제약 샘플링과 그 문법 비용, 분류기 헤드를 붙이는 파인 튜닝, 그리고 이 기법들이 언젠가 덜 중요해질 것이라는 저자의 예상
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 구조화 출력

- [구조화 출력이 필요한 두 시나리오](#구조화-출력이-필요한-두-시나리오)
- [네 자리에서 손댈 수 있다](#네-자리에서-손댈-수-있다)
- [프롬프팅](#프롬프팅)
- [후처리](#후처리)
- [제약 샘플링](#제약-샘플링)
- [파인 튜닝](#파인-튜닝)
- [이 기법들이 덜 중요해질 것이라는 예상](#이-기법들이-덜-중요해질-것이라는-예상)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **확률적으로 토큰을 뽑는 모델에게 정해진 형식을 반드시 지키게 하려면 어디에
손을 대야 하는가.**

## 구조화 출력이 필요한 두 시나리오

- **프로덕션에서는 모델이 특정 형식을 따르는 출력을 생성하게 해야 하는 일이 많다. 구조화 출력은
  다음 두 시나리오에 결정적이다** (2장, p.99):[^huyen2025]
  1. **구조화 출력을 요구하는 과제 — 이 시나리오에서 가장 흔한 범주는 의미 파싱(semantic
     parsing)이다. 의미 파싱은 자연어를 구조화된 기계 판독 형식으로 변환하는 것을 포함한다.
     text-to-SQL이 의미 파싱의 한 예로, 출력이 유효한 SQL 질의여야 한다. 의미 파싱은 사용자가
     자연어(예: 영어)로 API와 상호작용할 수 있게 한다. 예컨대 text-to-PostgreSQL은 사용자가
     PostgreSQL로 쓰는 대신 "What's the average monthly revenue over the last 6 months" 같은
     영어 질의로 Postgres 데이터베이스에 질의할 수 있게 한다. 이 시나리오의 다른 범주에는 출력이
     유효한 클래스여야 하는 분류가 있다** (2장, pp.99–100).[^huyen2025]
  2. **출력이 하류 애플리케이션에 쓰이는 과제 — 이 시나리오에서 과제 자체는 출력이 구조화될 것을
     요구하지 않지만, 출력이 다른 애플리케이션에 쓰이기 때문에 그 애플리케이션이 파싱할 수 있어야
     한다. 예컨대 AI 모델로 이메일을 쓴다면 이메일 자체는 구조화될 필요가 없다. 그러나 이 이메일을
     쓰는 하류 애플리케이션은 특정 형식을 요구할 수 있다 — 예컨대 `{"title": [TITLE], "body":
     [EMAIL BODY]}` 같은 특정 키를 가진 JSON 문서. 이는 모델의 출력이 흔히 모델이 쓸 수 있는
     도구의 입력으로 넘겨지는 에이전트 워크플로에서 특히 중요하다** (2장, p.100).[^huyen2025]
- 저자가 실은 실물이다. GPT-4o에게 text-to-regex를 시키는 프롬프트이고 출력은 GPT-4o가 실제로
  생성한 것이다 (2장, p.100):[^huyen2025]

  ```
  System prompt
  Given an item, create a regex that represents all the ways the item
  can be written. Return only the regex.

  Example:
  US phone number -> \+?1?\s?(\()?(\d{3})(?(1)\))[-.\s]?(\d{3})[-.\s]?
  (\d{4})

  User prompt
  Email address ->

  GPT-4o
  [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}

  User prompt
  Dates ->

  GTP-4o
  (?:\d{1,2}[\/\-\.])(?:\d{1,2}[\/\-\.])?\d{2,4}
  ```

- 도구와 제공자의 대응 — **구조화 출력을 지원하는 프레임워크에는 guidance·outlines·instructor·
  llama.cpp가 있다. 각 모델 제공자도 구조화 출력 생성 능력을 개선하려고 자기 기법을 쓸 수 있다.
  OpenAI는 텍스트 생성 API에 JSON 모드를 도입한 첫 모델 제공자였다. API의 JSON 모드는 통상 출력이
  유효한 JSON임만 보장하고 JSON 객체의 내용은 보장하지 않는다는 점에 유의하라. 그밖에 유효한
  생성된 JSON도 최대 출력 토큰 길이에 도달하는 등 생성이 너무 일찍 멈추면 잘려서 파싱 불가능해질
  수 있다. 그러나 최대 토큰 길이를 너무 높게 잡으면 모델의 응답이 너무 느리고 비싸진다** (2장,
  p.101).[^huyen2025]

## 네 자리에서 손댈 수 있다

- 저자가 잡는 지형 (2장, p.101):[^huyen2025]

  > You can guide a model to generate structured outputs at different layers of the AI stack:
  > prompting, post-processing, test time compute, constrained sampling, and finetuning. The first
  > three are more like bandages. They work best if the model is already pretty good at generating
  > structured outputs and just needs a little nudge. For intensive treatment, you need constrained
  > sampling and finetuning.

- 테스트 시점 컴퓨트 쪽은 앞 절이 이미 다뤘다 — **기대 형식에 맞는 것이 나올 때까지 계속 출력을
  생성한다** (2장, p.101).[^huyen2025] 그 기법 자체는
  [테스트 시점 컴퓨트](../concepts/test-time-compute.md)에 있다.

## 프롬프팅

- 첫 수 — **프롬프팅은 구조화 출력의 첫 행동 노선이다. 모델에게 어떤 형식으로든 출력을 생성하라고
  지시할 수 있다. 그러나 모델이 이 지시를 따를 수 있는지는 모델의 지시 따르기 능력과 지시의
  명확성에 달려 있다. 모델이 지시를 따르는 데 점점 좋아지고는 있지만 언제나 당신의 지시를 따를
  것이라는 보장은 없다. 몇 퍼센트포인트의 무효한 모델 출력도 많은 애플리케이션에서 여전히 받아들일
  수 없다** (2장, p.102).[^huyen2025]
  - 각주의 실측 — **집필 시점 기준 애플리케이션과 모델에 따라 올바르게 생성된 JSON 객체의 비율이
    0%에서 90%대 후반까지 걸치는 것을 저자는 보아 왔다** (2장, p.102 각주 33).[^huyen2025]
- 5장이 이 자리에 붙이는 관행 — JSON을 원하면 키가 무엇이어야 하는지 지정하고, 구조화 출력을 기대하는
  과제에는 입력의 끝을 표시하는 마커를 두라는 것이다 (5장, p.223).[^huyen2025] 그 관행의 자리는
  [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md)다.
- AI로 AI를 검사하기 — **유효한 출력의 비율을 높이려고 어떤 사람은 AI를 써서 원래 프롬프트의
  출력을 검증하거나 교정한다. 이는 AI 심판(AI as a judge) 접근의 한 예다. 이는 출력마다 최소 두
  번의 모델 질의가 있다는 뜻이다: 하나는 출력을 생성하고 하나는 검증한다. 추가된 검증 층이 출력의
  유효성을 크게 개선할 수 있지만, 추가 검증 질의가 유발하는 여분의 비용과 지연은 어떤 사람들에게
  이 접근을 너무 비싸게 만들 수 있다** (2장, p.102).[^huyen2025]

## 후처리

- 왜 통하는가 — **후처리는 단순하고 싸지만 놀랍도록 잘 통할 수 있다. 가르치던 시절 저자는 학생들이
  매우 비슷한 실수를 하는 경향이 있음을 알아챘다. 파운데이션 모델로 일하기 시작하면서 같은 것을
  알아챘다. 모델은 질의를 가로질러 비슷한 실수를 반복하는 경향이 있다. 이는 모델이 저지르는 흔한
  실수를 찾아내면 잠재적으로 그것을 교정하는 스크립트를 쓸 수 있다는 뜻이다. 예컨대 생성된 JSON
  객체가 닫는 괄호를 빠뜨리면 그 괄호를 손으로 더한다** (2장, p.102).[^huyen2025]
- 실물 — **링크드인의 방어적 YAML 파서는 올바른 YAML 출력의 비율을 90%에서 99.99%로 올렸다
  (Bottaro and Ramgopal, 2020)** (2장, p.102).[^huyen2025]
- 형식 선택의 실물 — **JSON과 YAML은 흔한 텍스트 형식이다. 링크드인은 자기 기반 모델 GPT-4가 둘
  다와 잘 작동함을 발견했지만 YAML을 출력 형식으로 택했는데, 덜 장황해 JSON보다 적은 출력 토큰을
  요구하기 때문이다(Bottaro and Ramgopal, 2020)** (2장, p.102).[^huyen2025]
- 한계 — **후처리는 실수를 고치기 쉬울 때만 통한다. 이는 보통 모델의 출력이 이미 대체로 올바르게
  형식화되어 있고 가끔 작은 오류가 있을 때 일어난다** (2장, p.102).[^huyen2025]

## 제약 샘플링

- 정의 — **제약 샘플링(constraint sampling)은 텍스트 생성을 특정 제약으로 유도하는 기법이다.
  통상 구조화 출력 도구가 따른다** (2장, p.103).[^huyen2025]
- 기제 — **높은 수준에서 토큰을 생성하려면 모델은 제약을 만족하는 값 중에서 샘플링한다. 토큰
  하나를 생성하려고 모델이 먼저 로짓 벡터를 출력하고 각 로짓이 하나의 가능한 토큰에 대응한다는
  것을 기억하라. 제약 샘플링은 이 로짓 벡터를 걸러 제약을 만족하는 토큰만 남긴다. 그러고 나서 이
  유효한 토큰들에서 샘플링한다** (2장, p.103).[^huyen2025]
- 어려운 이유 — **간단한 예에서는 제약을 걸러 내기 쉽다. 그러나 대부분의 경우는 그렇게 간단하지
  않다. 각 단계에서 무엇이 허용되고 무엇이 허용되지 않는지 지정하는 문법이 있어야 한다. 예컨대
  JSON 문법은 `{` 다음에 문자열의 일부가 아닌 한 또 다른 `{`가 올 수 없다고 규정한다 —
  `{"key": "{{string}}"}`처럼 되어야 한다** (2장, p.103).[^huyen2025]
- 비용 — **그 문법을 만들어 내고 샘플링 과정에 넣는 것은 간단하지 않다. 각 출력 형식 — JSON·YAML·
  정규 표현식·CSV 등 — 이 자기 문법을 필요로 하므로 제약 샘플링은 일반화가 덜 된다. 그 사용은
  외부 도구나 당신의 팀이 문법을 지원하는 형식에 한정된다. 문법 검증은 생성 지연을 늘릴 수도
  있다(Brandon T. Willard, 2024)** (2장, p.103).[^huyen2025]
- 반대 의견 — **어떤 사람은 제약 샘플링에 필요한 자원이 지시를 더 잘 따르도록 모델을 훈련하는 데
  투자되는 편이 낫다고 믿기 때문에 제약 샘플링에 반대한다** (2장, p.103).[^huyen2025]

## 파인 튜닝

- 가장 효과적인 접근 — **당신이 원하는 형식을 따르는 예로 모델을 파인 튜닝하는 것이 이 형식으로
  출력을 생성하게 만드는 가장 효과적이고 일반적인 접근이다. 어떤 기대 형식과도 작동할 수 있다.
  단순한 파인 튜닝이 모델이 언제나 기대 형식을 출력할 것을 보장하지는 않지만 프롬프팅보다 훨씬
  신뢰할 만하다** (2장, p.104).[^huyen2025]
  - 각주의 대안 — **원하는 형식을 따르는 데이터로 모델을 처음부터 훈련하는 것도 통하지만 이 책은
    모델을 처음부터 개발하는 것에 대한 책이 아니다** (2장, p.104 각주 34).[^huyen2025]
- 구조까지 바꾸는 길 — **어떤 과제에서는 파인 튜닝 전에 모델의 구조를 변경해 출력 형식을 보장할 수
  있다. 예컨대 분류에서는 파운데이션 모델의 구조에 분류기 층(classifier layer)을 덧붙여 모델이 미리
  지정된 클래스 중 하나만 출력하게 할 수 있다. 이 접근은 특징 기반 전이(feature-based transfer)
  라고도 불린다** (2장, p.104).[^huyen2025]
  - 각주 — **어떤 파인 튜닝 서비스는 이것을 자동으로 해 준다. OpenAI의 파인 튜닝 서비스는 예전에
    훈련 시 분류기 헤드를 더할 수 있게 해 주었으나 집필 시점에는 이 기능이 비활성화되었다** (2장,
    p.104 각주 35).[^huyen2025]
- 어디까지 다시 훈련하는가 — **파인 튜닝 중에는 모델 전체를 종단 간으로 재훈련하거나 이 분류기
  헤드 같은 모델의 일부만 재훈련할 수 있다. 종단 간 훈련은 더 많은 자원을 요구하지만 더 나은
  성능을 약속한다** (2장, p.104).[^huyen2025]

## 이 기법들이 덜 중요해질 것이라는 예상

- 저자의 전망 (2장, p.104):[^huyen2025]

  > We need techniques for structured outputs because of the assumption that the model, by itself,
  > isn't capable of generating structured outputs. However, as models become more powerful, we can
  > expect them to get better at following instructions. I suspect that in the future, it'll be
  > easier to get models to output exactly what we need with minimal prompting, and these techniques
  > will become less important.

## 이어지는 페이지

- [샘플링 전략](../concepts/sampling-strategies.md) — 제약 샘플링이 걸러 내는 그 로짓과 정지 조건
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 형식에 맞을 때까지 다시 생성하는 접근
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프팅과 파인 튜닝을 가르는 축
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 형식을 가르치는 데이터가 만들어지는 쪽
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 형식이 흔들리는 근본 원인
- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 프롬프팅 층에서 형식을
  지정하는 관행
- [프롬프트 엔지니어링 도구](../concepts/prompt-engineering-tools.md) — Guidance·Outlines·Instructor가
  다시 등장하는 자리

[^huyen2025]: Huyen 2025, 2장 "Understanding Foundation Models" (책 pp.49–112). 이 페이지는
    "Structured Outputs" 절(pp.99–104)을 담았다. text-to-regex 예(p.100)는 원문 표기를 그대로
    옮겼고, GPT-4o를 "GTP-4o"로 쓴 마지막 라벨의 오식도 원문 그대로다. 도판 Figure 2-20
    (guidance로 제약 출력을 생성하는 코드 예 두 개, p.101)·Figure 2-21(제약 샘플링의 로짓 필터,
    p.103)·Figure 2-22(분류기 헤드를 붙인 구조, p.104)는 옮기지 않았다. 프롬프팅 절에 더해진 한
    줄은 5장 "Prompt Engineering"의 "Specify the output format"(책 p.223)에서 왔다. Bottaro and
    Ramgopal(2020)·Brandon T. Willard(2024)는 huyen2025를 통한 전언이다.

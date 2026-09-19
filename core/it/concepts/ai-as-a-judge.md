---
type: concept
title: AI 판정자
description: AI로 AI를 평가하는 접근이 무엇이고 왜 프로덕션의 표준이 되어 가는가 — 참조 데이터 없이 어떤 기준으로든 물을 수 있다는 이점과 인간 일치도 85%라는 실측, 응답 하나·참조 대비·둘 중 하나라는 세 가지 사용법, 도구마다 다른 내장 기준, 판정자 프롬프트가 담아야 하는 과제·기준·채점 체계, 점수를 그냥 물어보는 대신 답을 진술로 쪼개 하나씩 검증하게 하면 사람과의 일치도가 오른다는 실측, 그리고 판정자는 모델이 아니라 모델과 프롬프트로 된 시스템이라는 규정
generated: { by: "claude-opus-5", at: "2026-08-17T11:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: es2024-ragas, resource: /it/sources/es2024-ragas.md }
---

# AI 판정자

- [AI로 AI를 평가한다](#ai로-ai를-평가한다)
- [언제부터 실용이 되었나](#언제부터-실용이-되었나)
- [왜 AI 판정자인가](#왜-ai-판정자인가)
- [사람과 얼마나 일치하는가](#사람과-얼마나-일치하는가)
- [쓰는 방식 세 가지](#쓰는-방식-세-가지)
- [도구마다 다른 내장 기준](#도구마다-다른-내장-기준)
- [판정자 프롬프트가 담아야 하는 것](#판정자-프롬프트가-담아야-하는-것)
- [점수를 묻는 대신 쪼개어 검증하게 하기](#점수를-묻는-대신-쪼개어-검증하게-하기)
- [원전이 밝힌 조건과 한계](#원전이-밝힌-조건과-한계)
- [판정자는 모델이 아니라 시스템이다](#판정자는-모델이-아니라-시스템이다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **AI가 AI의 응답을 판정하게 하면 무엇을 얻고, 그 판정을 무엇으로 규정해야
재현할 수 있는가.**

## AI로 AI를 평가한다

- 어디서 나온 접근인가 — **개방형 응답을 평가하는 난제 때문에 많은 팀이 사람 평가로 되돌아갔다. AI가
  많은 어려운 과제를 자동화하는 데 성공적으로 쓰여 왔으니 AI가 평가도 자동화할 수 있을까? AI를 써서
  AI를 평가하는 접근을 AI 판정자(AI as a judge) 또는 LLM 판정자(LLM as a judge)라고 부른다. 다른 AI
  모델을 평가하는 데 쓰이는 AI 모델을 AI 판정자(AI judge)라고 부른다** (3장, p.136).[^huyen2025]
  - 각주가 미리 막는 오해 — **AI 판정자라는 용어는 AI가 법정에서 판사로 쓰이는 유스케이스와 혼동해서는
    안 된다** (3장, p.136 각주 15).[^huyen2025]

## 언제부터 실용이 되었나

- 발상은 오래되었으나 — **AI를 써서 평가를 자동화한다는 발상은 오랫동안 있어 왔지만, AI 모델이 그것을
  할 능력을 갖추었을 때에야 실용이 되었고 그 시점은 GPT-3가 출시된 2020년 무렵이었다** (3장,
  p.137).[^huyen2025]
  - 각주가 밝히는 저자 자신의 이력 — **2017년 저자는 NeurIPS 워크숍에서 MEWR(Machine translation
    Evaluation metric Without Reference text)를 발표했는데, 더 강한 언어 모델을 활용해 기계 번역을
    자동으로 평가하는 평가 방법이었다. 안타깝게도 삶이 끼어들어 이 연구 방향을 계속 추구하지
    못했다** (3장, p.137 각주 16).[^huyen2025]
- 지금의 위치 — **집필 시점 기준 AI 판정자는 프로덕션에서 AI 모델을 평가하는 가장 흔한 방법 중
  하나가, 어쩌면 가장 흔한 방법이 되었다. 저자가 2023년과 2024년에 본 AI 평가 스타트업 데모의 대부분이
  어떤 식으로든 AI 판정자를 활용했다. LangChain의 2023년 State of AI 리포트는 자기 플랫폼에서 이뤄진
  평가의 58%가 AI 판정자에 의해 수행되었다고 밝혔다. AI 판정자는 활발한 연구 영역이기도 하다** (3장,
  p.137).[^huyen2025]

## 왜 AI 판정자인가

- 세 가지 이점 — **AI 판정자는 사람 평가자에 비해 빠르고, 쓰기 쉽고, 상대적으로 싸다. 참조 데이터
  없이도 작동할 수 있는데, 이는 참조 데이터가 없는 프로덕션 환경에서도 쓸 수 있다는 뜻이다** (3장,
  p.137).[^huyen2025]
- 무엇이든 물을 수 있다 — **정확성·반복성·독성·건전성·환각 등 어떤 기준으로든 출력을 판정하라고 AI
  모델에게 요청할 수 있다. 이는 사람에게 무엇에 대해서든 의견을 달라고 요청할 수 있는 것과 비슷하다.
  "그렇지만 사람의 의견을 늘 믿을 수는 없잖아"라고 생각할 수 있다. 맞는 말이고, AI의 판단도 늘 믿을 수는
  없다. 그러나 각 AI 모델이 다수의 집합체이므로 AI 모델이 다수를 대표하는 판단을 내리는 것이 가능하다.
  올바른 모델에 올바른 프롬프트를 쓰면 넓은 범위의 주제에 대해 꽤 좋은 판단을 얻을 수 있다** (3장,
  p.137).[^huyen2025]
- 설명까지 낸다 — **AI는 응답을 평가할 수 있을 뿐 아니라 자기 결정을 설명할 수도 있는데, 이는 평가
  결과를 감사(audit)하고 싶을 때 특히 유용할 수 있다** (3장, p.137, Figure 3-7이 GPT-4가 자기 판정을
  설명하는 예를 보인다).[^huyen2025]
- 유일한 선택지일 때도 있다 — **그 유연성 덕에 AI는 넓은 범위의 애플리케이션에 유용하며, 어떤
  애플리케이션에는 유일한 자동 평가 선택지다. AI의 판단이 사람의 판단만큼 좋지 않을 때조차, 애플리케이션의
  개발을 이끌고 프로젝트를 띄울 충분한 확신을 주기에는 충분히 좋을 수 있다** (3장,
  p.137).[^huyen2025]

## 사람과 얼마나 일치하는가

- 실측 둘 — **어떤 AI 판정자는 사람 평가자와 강하게 상관됨을 연구들이 보였다. 2023년 Zheng et al.은
  자기 평가 벤치마크 MT-Bench에서 GPT-4와 사람 사이의 일치도가 85%에 이르렀음을 발견했는데, 이는 사람들
  사이의 일치도(81%)보다도 높다. AlpacaEval 저자들(Dubois et al., 2023)도 자기 AI 판정자가 사람이
  평가하는 LMSYS의 Chat Arena 리더보드와 거의 완벽한(0.98) 상관을 가짐을 발견했다** (3장,
  p.137).[^huyen2025]

## 쓰는 방식 세 가지

- **AI로 판단을 내리는 방법은 여럿이다. 예컨대 AI를 써서 응답 자체의 품질을 평가하거나, 그 응답을
  참조 데이터와 비교하거나, 그 응답을 다른 응답과 비교할 수 있다. 이 세 접근의 소박한 예시 프롬프트가
  다음과 같다** (3장, pp.138–139):[^huyen2025]
  1. **원래 질문이 주어졌을 때 응답 자체의 품질을 평가한다:**

     ```
     "Given the following question and answer, evaluate how good the answer is
     for the question. Use the score from 1 to 5.
     - 1 means very bad.
     - 5 means very good.
     Question: [QUESTION]
     Answer: [ANSWER]
     Score:"
     ```

  2. **생성 응답을 참조 응답과 비교해 생성 응답이 참조 응답과 같은지 평가한다. 이는 손으로 설계한
     유사도 측정의 대안 접근이 될 수 있다:**

     ```
     "Given the following question, reference answer, and generated answer,
     evaluate whether this generated answer is the same as the reference answer.
     Output True or False.
     Question: [QUESTION]
     Reference answer: [REFERENCE ANSWER]
     Generated answer: [GENERATED ANSWER]"
     ```

  3. **생성된 두 응답을 비교해 어느 쪽이 더 나은지 판정하거나 사용자가 어느 쪽을 선호할 가능성이 높은지
     예측한다. 이는 사후 훈련 정렬을 위한 선호 데이터 생성, 테스트 시점 컴퓨트, 그리고 다음 절의
     비교 평가를 이용한 모델 순위 매기기에 유용하다:**

     ```
     "Given the following question and two answers, evaluate which answer is
     better. Output A or B.
     Question: [QUESTION]
     A: [FIRST ANSWER]
     B: [SECOND ANSWER]
     The better answer is:"
     ```

- 기준은 애플리케이션이 정한다 — **범용 AI 판정자에게는 어떤 기준으로든 응답을 평가하라고 요청할 수
  있다. 롤플레잉 챗봇을 만든다면 챗봇의 응답이 사용자가 원하는 역할과 일관되는지 평가하고 싶을 수 있다.
  "Does this response sound like something Gandalf would say?" 같은 것이다. 홍보용 제품 사진을 생성하는
  애플리케이션을 만든다면 "From 1 to 5, how would you rate the trustworthiness of the product in this
  image?"라고 묻고 싶을 수 있다** (3장, p.139).[^huyen2025]

## 도구마다 다른 내장 기준

- 어떤 AI 도구들이 제공하는 내장 AI 판정자 기준의 예다. 2024년 9월 기준이며, **이 도구들이 진화하면서
  이 내장 기준도 바뀔 것이라는 데 유의하라** (3장, p.139, Table 3-3):[^huyen2025]

  | AI 도구 | 내장 기준 |
  |---|---|
  | Azure AI Studio | Groundedness, relevance, coherence, fluency, similarity |
  | MLflow.metrics | Faithfulness, relevance |
  | LangChain Criteria Evaluation | Conciseness, relevance, correctness, coherence, harmfulness, maliciousness, helpfulness, controversiality, misogyny, insensitivity, criminality |
  | Ragas | Faithfulness, answer relevance |

- 표준이 아니다 — **AI 판정자 기준이 표준화되어 있지 않다는 것을 기억하는 것이 필수다. Azure AI
  Studio의 relevance 점수는 MLflow의 relevance 점수와 아주 다를 수 있다. 이 점수들은 판정자의 밑에 깔린
  모델과 프롬프트에 달려 있다** (3장, p.139).[^huyen2025]

## 판정자 프롬프트가 담아야 하는 것

- **AI 판정자에게 프롬프트하는 법은 어떤 AI 애플리케이션에 프롬프트하는 법과 비슷하다. 일반적으로
  판정자의 프롬프트는 다음을 명확히 설명해야 한다** (3장, p.140):[^huyen2025]
  1. **모델이 수행할 과제.** 예컨대 **생성된 답과 질문 사이의 관련성을 평가하는 것.**
  2. **모델이 평가할 때 따라야 하는 기준.** 예컨대 **"Your primary focus should be on determining
     whether the generated answer contains sufficient information to address the given question
     according to the ground truth answer". 지시가 더 상세할수록 좋다.**
  3. **채점 체계. 다음 중 하나일 수 있다:**
     - **분류. 좋음/나쁨, 또는 관련 있음/관련 없음/중립 같은 것.**
     - **이산 수치 값. 1에서 5 같은 것. 이산 수치 값은 각 클래스가 의미적 해석 대신 수치적 해석을
       갖는 분류의 특수 사례로 볼 수 있다.**
     - **연속 수치 값. 0과 1 사이 같은 것. 예컨대 유사도의 정도를 평가하고 싶을 때다.**
- 저자의 조언 상자 — **언어 모델은 일반적으로 숫자보다 텍스트를 더 잘 다룬다. AI 판정자가 수치 채점
  체계보다 분류에서 더 잘 작동한다고 보고되어 왔다. 수치 채점 체계에서는 연속 채점보다 이산 채점이 더
  잘 작동하는 것으로 보인다. 경험적으로 이산 채점의 범위가 넓을수록 모델이 나빠지는 것으로 보인다.
  전형적인 이산 채점 체계는 1과 5 사이다** (3장, p.140).[^huyen2025]
- 예시를 넣어라 — **예시가 있는 프롬프트가 더 잘 수행하는 것으로 나타났다. 1과 5 사이의 채점 체계를
  쓴다면 1·2·3·4·5점을 받는 응답이 각각 어떻게 생겼는지, 가능하다면 왜 어떤 응답이 특정 점수를 받는지의
  예시를 포함하라** (3장, p.140).[^huyen2025]
- 실물 하나 — Azure AI Studio가 relevance 기준에 쓰는 프롬프트의 일부다. **과제·기준·채점 체계, 낮은
  점수를 받는 입력의 예, 그리고 이 입력이 왜 낮은 점수를 받는지의 근거를 설명한다. 간결함을 위해
  프롬프트의 일부가 제거되었다** (3장, pp.140–141):[^huyen2025]

  ```
  Your task is to score the relevance between a generated answer and the
  question based on the ground truth answer in the range between 1 and 5,
  and please also provide the scoring reason.

  Your primary focus should be on determining whether the generated answer
  contains sufficient information to address the given question according
  to the ground truth answer. …

  If the generated answer contradicts the ground truth answer, it will
  receive a low score of 1-2.

  For example, for the question "Is the sky blue?" the ground truth answer
  is "Yes, the sky is blue." and the generated answer is "No, the sky is
  not blue."

  In this example, the generated answer contradicts the ground truth answer
  by stating that the sky is not blue, when in fact it is blue.

  This inconsistency would result in a low score of 1-2, and the reason for
  the low score would reflect the contradiction between the generated
  answer and the ground truth answer.
  ```

## 점수를 묻는 대신 쪼개어 검증하게 하기

> **심사 조건**: 이 절과 다음 절의 claim은 위 표에 Ragas로 실린 도구의 원전에서 오는데, 그것은
> EACL 2024 **System Demonstrations** 트랙 논문이다. 본 학회 트랙보다 심사가 가볍고 도구 시연이
> 목적인 트랙이므로 아래 수치는 그 조건에서 읽는다.

- 위 표에서 Ragas의 내장 기준으로 적힌 것은 둘이지만 (3장, p.139, Table 3-3),[^huyen2025] 그
  원전이 제안하는 것은 셋이다 — **충실성(Faithfulness)·답 관련성(Answer Relevance)·맥락
  관련성(Context Relevance)** (3절, p.152).[^es2024-ragas] 세 지표의 정의와 계산은
  [검색 품질 평가](../concepts/retrieval-evaluation.md)에 있다.
- 이 페이지에 걸리는 것은 그 **프롬프트 설계**다. 위에서 저자가 든 "소박한 예시 프롬프트" 세
  가지는 모두 판정자에게 **점수나 참·거짓을 곧바로 물어본다** (3장, pp.138–139).[^huyen2025]
  원전은 그것을 기준선으로 삼고 자기 설계와 견준다 — **GPT Score는 ChatGPT에게 세 품질 차원에
  0에서 10 사이의 점수를 매기게 하고, GPT Ranking은 대신 선호하는 답이나 맥락을 고르게 한다. 두
  경우 모두 프롬프트에 해당 품질 지표의 정의를 포함한다** (5절, p.154).[^es2024-ragas]
- 원전의 설계는 한 번 묻지 않고 두 단계로 나눈다 — **충실성을 추정하려고 먼저 LLM으로 진술 집합을
  뽑는다. 이 단계의 목적은 긴 문장을 더 짧고 초점이 맞은 단언으로 분해하는 것이다.** 그다음 진술
  하나하나에 대해 **그것이 맥락에서 추론될 수 있는지 판정한다** (3절, p.152).[^es2024-ragas]
- 그 차이가 사람과의 일치도로 나타난다. 원문 표기를 그대로 옮겼다 (5절, p.154,
  Table 4):[^es2024-ragas]

  | | Faith. | Ans. Rel. | Cont. Rel. |
  |---|---|---|---|
  | RAGAS | 0.95 | 0.78 | 0.70 |
  | GPT Score | 0.72 | 0.52 | 0.63 |
  | GPT Ranking | 0.54 | 0.40 | 0.52 |

  **제안한 지표들이 두 기준선의 예측보다 사람 판단에 훨씬 가깝게 정렬된다** (5절,
  p.154).[^es2024-ragas] 곧 같은 모델·같은 기준이라도 **묻는 방식**이 판정 품질을 가른다 —
  이 페이지가 마지막 절에서 세우는 "판정자는 모델과 프롬프트로 된 시스템"이라는 규정의 실측이다.
- 저자가 조언 상자에서 "언어 모델은 숫자보다 텍스트를 더 잘 다룬다"고 적은 것과도 같은
  방향이다 (3장, p.140)[^huyen2025] — 원전에서 가장 잘 맞은 충실성은 **점수를 매기는 대신
  진술마다 Yes/No 판정을 내리게 하고 그 비율을 사람이 계산하는** 방식이다 (3절,
  p.152).[^es2024-ragas]
- 저자들이 형식에 대해 따로 남긴 것 — **우리는 LLM이 구조화된 JSON 형식으로 출력을 생성하도록
  요구한다. 이것이 RAGAS를 다른 LLM과 대체로 호환되게 만들고, 궁극적으로 LLM 생성 텍스트를 소비할
  때의 오류율을 낮춘다** (5.1절, pp.154–155).[^es2024-ragas]

## 원전이 밝힌 조건과 한계

- 판정자를 무엇으로 돌리는가에 전부 걸린다 — **이 논문은 툴킷을 소개하며, 그것은 서로 다른 구성
  요소를 평가하는 데 쓰인 LLM의 성능에 크게 의존한다. 2024년 저술 시점의 실험 집합이 이 지표들과 사람 판단의
  높은 상관을 보이지만, LLM에 기대는 것에 알려진 한계가 따라옴을 인정한다** (8절 Limitations,
  p.156).[^es2024-ragas]
- 저자들이 붙인 처방 — **따라서 LLM의 적합성을 신중히 검토하는 것이 RAGAS와 이 공간의 다른
  기여들에 결정적이며, 이상적으로는 유료 API 뒤의 완제품보다 열린 모델을 우선해야 한다** (8절
  Limitations, p.156).[^es2024-ragas] 이는 위에서 든 "판정자가 바뀌면 다른 판정자가 된다"는
  규정을 도구 선택의 기준으로 되돌린 것이다.
- 실험이 실제로 돌린 모델은 하나다 — **우리 구현과 실험에서 모든 프롬프트는 OpenAI API로 이용
  가능한 `gpt-3.5-turbo-16k` 모델로 평가된다** (3절, p.152).[^es2024-ragas] 곧 위 표의 0.95는
  이 모델·이 프롬프트·이 데이터셋의 값이며 다른 판정자로 옮겨 갈 수 있다는 근거는 논문에 없다.

## 판정자는 모델이 아니라 시스템이다

- 저자의 규정 (3장, p.141):[^huyen2025]

  > An AI judge is not just a model—it's a system that includes both a model and a prompt.
  > Altering the model, the prompt, or the model's sampling parameters results in a different
  > judge.

  이 규정이 [AI 판정자의 한계](../concepts/ai-judge-limitations.md)에서 기준 모호성과 재현 불가의
  근거가 된다.

## 이어지는 페이지

- [AI 판정자의 한계](../concepts/ai-judge-limitations.md) — 비일관성·기준 모호성·비용과 지연·편향
- [판정자 모델 고르기](../concepts/ai-judge-selection.md) — 더 강한 판정자와 더 약한 판정자, 그리고
  특화 판정자 세 종류
- [비교 평가](../concepts/comparative-evaluation.md) — 셋째 사용법이 모델 순위로 이어지는 자리
- [참조 데이터 대비 유사도 측정](../concepts/similarity-measurements-against-reference-data.md) —
  둘째 사용법이 대체하려는 손 설계 지표
- [기능적 정확성](../concepts/functional-correctness.md) — AI 판정자가 "주관적"으로 분류되는 기준
- [선호 파인 튜닝](../concepts/preference-finetuning.md) — 선호 데이터 생성이 쓰이는 자리
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 여러 출력 중 고르는 데 판정이 쓰이는 자리
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 판정자 자신도 확률적이라는 사실의
  출처
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — 위 세 지표의 정의와 계산이 서는 자리

[^es2024-ragas]: Es et al. 2024, "RAGAs: Automated Evaluation of Retrieval Augmented Generation",
    EACL 2024 **System Demonstrations**, pp.150–158. 본 학회 트랙이 아니라 시연 트랙이므로
    심사가 가볍다 — 이 페이지의 claim은 그 조건에서 읽는다. 쪽 번호는 학회 논문집 인쇄 쪽이다.
    이 페이지는 3절 Evaluation Strategies의 프롬프트 설계·5절 Experiments·5.1절
    Reproducibility·8절 Limitations을 담았다. Table 4는 원문 표기를 그대로 옮겼다. 지표의 정의와
    식, WikiEval 데이터셋 구성은 [검색 품질 평가](../concepts/retrieval-evaluation.md)가 담는다.
    Figure 1(JSON 형식 유무별 점수 일관성 산점도, p.155)은 옮기지 않았고 본문이 서술한 결론만
    담았다. 6절 Python API의 코드는 옮기지 않았다.

[^huyen2025]: Huyen 2025, 3장 "Evaluation Methodology" (책 pp.113–158). 이 페이지는
    "AI as a Judge" 절의 도입부(pp.136–137)와 하위 절 "Why AI as a Judge?"(p.137)·"How to Use AI
    as a Judge"(pp.138–141)를 담았다. 예시 프롬프트와 Azure AI Studio 프롬프트 발췌, Table 3-3은
    원문에 실린 것을 그대로 옮겼다. 도판 Figure 3-7(GPT-4가 문단에 4.5/5를 주고 근거를 설명하는
    화면, p.138)·Figure 3-8(AI 판정자의 구성 도식, p.141)은 옮기지 않았고 본문이 서술한 내용만
    담았다. Zheng et al.(2023) MT-Bench·Dubois et al.(2023) AlpacaEval·LangChain State of AI
    2023·Azure AI Studio·MLflow·LangChain Criteria Evaluation·Ragas는 huyen2025를 통한 전언이다.

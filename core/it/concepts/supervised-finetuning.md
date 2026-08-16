---
type: concept
title: 지도 파인 튜닝
description: 사후 훈련의 첫 단계가 완성 기계를 대화 상대로 바꾸는 방식 — 사후 훈련이 푸는 두 문제와 그 두 단계, 시연 데이터와 행동 복제, 좋은 레이블러가 비싼 이유와 실제 단가, 자원봉사·휴리스틱·합성 데이터라는 대안, 그리고 사전 훈련을 건너뛰지 않는 이유
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 지도 파인 튜닝

- [사후 훈련이 푸는 두 문제](#사후-훈련이-푸는-두-문제)
- [사후 훈련의 두 단계](#사후-훈련의-두-단계)
- [토큰 수준에서 응답 수준으로](#토큰-수준에서-응답-수준으로)
- [완성이 아니라 응답](#완성이-아니라-응답)
- [시연 데이터와 행동 복제](#시연-데이터와-행동-복제)
- [좋은 레이블러는 비싸다](#좋은-레이블러는-비싸다)
- [비싼 주석을 피하는 길들](#비싼-주석을-피하는-길들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **사전 훈련이 끝난 완성 기계를 사용자의 요청에 응답하는 모델로 바꾸는 첫 단계는
무엇을 하는가.**

## 사후 훈련이 푸는 두 문제

- 출발점 — **사후 훈련(post-training)은 사전 훈련된 모델에서 시작한다. 자기지도로 파운데이션
  모델을 사전 훈련했다고 하자. 오늘날 사전 훈련이 작동하는 방식 때문에 사전 훈련된 모델에는
  통상 두 가지 문제가 있다** (2장, p.78).[^huyen2025]
  - **첫째, 자기지도는 대화가 아니라 텍스트 완성에 대해 모델을 최적화한다.**
  - **둘째, 인터넷에서 무차별적으로 긁어 온 데이터로 사전 훈련되면 그 출력이 인종차별적이거나
    성차별적이거나 무례하거나 그냥 틀릴 수 있다.**
  - **사후 훈련의 목표는 이 두 문제를 다루는 것이다** (2장, p.78).[^huyen2025]
  - 각주에 실린 비유 — **한 친구가 이 비유를 썼다: 사전 훈련된 모델은 사람이 아니라 웹 페이지처럼
    말한다** (2장, p.78 각주 21).[^huyen2025]

## 사후 훈련의 두 단계

- **모델마다 사후 훈련은 다르다. 그러나 일반적으로 사후 훈련은 두 단계로 이뤄진다** (2장,
  p.78):[^huyen2025]
  1. **지도 파인 튜닝(supervised finetuning, SFT) — 완성 대신 대화를 위해 고품질 지시 데이터로
     사전 훈련된 모델을 파인 튜닝한다.**
  2. **선호 파인 튜닝(preference finetuning) — 인간 선호에 정렬된 응답을 출력하도록 모델을 더
     파인 튜닝한다. 선호 파인 튜닝은 통상 강화 학습(reinforcement learning, RL)으로 이뤄진다.
     선호 파인 튜닝 기법에는 GPT-3.5와 Llama 2가 쓴 인간 피드백 강화 학습(reinforcement learning
     from human feedback, RLHF), Llama 3가 쓴 DPO(Direct Preference Optimization), 그리고 Claude가
     잠재적으로 쓰는 AI 피드백 강화 학습(RLAIF)이 있다.**
  - 각주 — **강화 학습의 기초는 이 책의 범위 밖이지만 요점은 강화 학습이 인간 선호처럼 어려운
    목적에 대해 최적화하게 해 준다는 것이다** (2장, p.78 각주 22).[^huyen2025]
- 조합이 필수는 아니다 — **사전 훈련·SFT·선호 파인 튜닝의 조합이 오늘날 파운데이션 모델을 만드는
  인기 있는 해법이지만 유일한 해법은 아니다. 어느 단계든 건너뛸 수 있다** (2장,
  p.80).[^huyen2025]

## 토큰 수준에서 응답 수준으로

- 저자가 다르게 말한 차이 — **언어 기반 파운데이션 모델에서 사전 훈련은 토큰 수준 품질을
  최적화하며, 모델은 다음 토큰을 정확히 예측하도록 훈련된다. 그러나 사용자는 토큰 수준 품질에
  신경 쓰지 않는다 — 응답 전체의 품질에 신경 쓴다. 사후 훈련은 일반적으로 사용자가 선호하는
  응답을 생성하도록 모델을 최적화한다. 어떤 사람은 사전 훈련을 지식을 얻기 위한 독서에, 사후
  훈련을 그 지식을 쓰는 법을 배우는 것에 비유한다** (2장, p.78).[^huyen2025]
- 용어 경고 — **어떤 사람은 지도 파인 튜닝을 가리키는 데 지시 파인 튜닝(instruction finetuning)
  이라는 용어를 쓰고, 어떤 사람은 지도 파인 튜닝과 선호 파인 튜닝 둘 다를 가리키는 데 쓴다.
  모호함을 피하려고 이 책은 지시 파인 튜닝이라는 용어를 피한다** (2장, p.78).[^huyen2025]
- 자원 비중과 그 함의 — **사후 훈련이 사전 훈련에 비해 자원의 작은 부분만 소비하므로(InstructGPT는
  사후 훈련에 컴퓨트의 2%만, 사전 훈련에 98%를 썼다), 사후 훈련은 사전 훈련된 모델이 이미 갖고
  있지만 프롬프트만으로는 접근하기 어려운 능력을 여는 일로 생각할 수 있다** (2장,
  pp.78–79).[^huyen2025]
- 저자가 든 그림 하나 — **전체 훈련 워크플로가 스마일 얼굴을 단 괴물 쇼고스(Shoggoth) 밈과 아주
  비슷해 보인다** (2장, p.79):[^huyen2025]
  1. **자기지도 사전 훈련은 인터넷의 무차별적 데이터를 쓰기 때문에 길들여지지 않은 괴물로 여길 수
     있는 불량 모델을 낳는다.**
  2. **이 괴물은 더 높은 품질의 데이터 — 스택 오버플로·쿼라·사람의 주석 — 로 지도 파인 튜닝되어
     사회적으로 더 받아들일 만해진다.**
  3. **이 파인 튜닝된 모델은 선호 파인 튜닝으로 더 다듬어져 고객에게 적합해지는데, 이는 스마일
     얼굴을 붙여 주는 것과 같다.**

## 완성이 아니라 응답

- 문제의 실물 — **사전 훈련된 모델은 대화가 아니라 완성에 최적화되어 있을 가능성이 높다. 모델에
  "How to make pizza"를 입력하면 모델은 이것이 대화여야 한다는 개념이 없으므로 이 문장을 계속
  완성할 것이다. 다음 세 가지 중 어느 것도 유효한 완성일 수 있다** (2장, p.80):[^huyen2025]
  1. **질문에 맥락 더하기: "for a family of six?"**
  2. **후속 질문 덧붙이기: "What ingredients do I need? How much time would it take?"**
  3. **피자 만드는 법에 대한 지시 주기.**
  - **목표가 사용자에게 알맞게 응답하는 것이라면 옳은 선택지는 3이다** (2장, p.80).[^huyen2025]

## 시연 데이터와 행동 복제

- 기제와 두 이름 (2장, p.81):[^huyen2025]

  > We know that a model mimics its training data. To encourage a model to generate the appropriate
  > responses, you can show examples of appropriate responses. Such examples follow the format
  > (*prompt, response*) and are called *demonstration data*. Some people refer to this process as
  > *behavior cloning*: you demonstrate how the model should behave, and the model clones this
  > behavior.
- 무엇을 담아야 하는가 — **서로 다른 종류의 요청은 서로 다른 종류의 응답을 요구하므로, 시연
  데이터는 모델이 다루기를 원하는 요청의 범위를 담아야 한다. 질의응답·요약·번역 같은 것이다**
  (2장, p.81).[^huyen2025]
- OpenAI가 InstructGPT를 파인 튜닝하는 데 쓴 프롬프트의 과제별 분포다. 저자가 도판으로 실은
  것을 수치만 옮겼다. **InstructGPT가 텍스트 전용 모델이므로 이 분포에는 멀티모달 과제가 없다**
  (2장, p.81, Figure 2-12):[^huyen2025]

  | 과제 유형 | 비율 |
  |---|---|
  | Generation | 45.6% |
  | Open QA | 12.4% |
  | Brainstorming | 11.2% |
  | Chat | 8.4% |
  | Rewrite | 6.6% |
  | Summarization | 4.2% |
  | Classification | 3.5% |
  | Other | 3.5% |
  | Closed QA | 2.6% |
  | Extract | 1.9% |

## 좋은 레이블러는 비싸다

- 왜 어려운가 — **사람이 배우는 데 좋은 교사가 중요하듯, AI가 지적인 대화를 이끄는 법을 배우는 데
  좋은 레이블러가 중요하다. 도메인 전문성이 거의 또는 전혀 없이도 흔히 가능한 전통적 데이터
  레이블링과 달리, 시연 데이터는 비판적 사고·정보 수집·사용자 요청의 적절성에 대한 판단을 요구하는
  응답을 가진 복잡한 프롬프트를 담을 수 있다** (2장, pp.81–82).[^huyen2025]
- InstructGPT를 위해 레이블러가 만든 (프롬프트, 응답) 쌍의 예다. 원문 표기를 그대로 옮겼고, 긴
  본문을 생략한 표기도 원문의 것이다 (2장, p.82, Table 2-6):[^huyen2025]

  | Prompt | Labeler's response |
  |---|---|
  | Serendipity means the occurrence and development of events by chance in a happy or beneficial way. Use the word in a sentence. | Running into Margaret and being introduced to Tom was a fortunate stroke of serendipity. |
  | Read the following text and answer the three questions at the end.<br><br>[OMITTED FOR LENGTH - Article about Justice Ruth Bader Ginsburg, Champion Of Gender Equality, Dies At 87]<br><br>1. …<br>2. …<br>3. Why will Ginsburg's death have profound consequences for the court and the country? | 1. …<br>2. …<br>3. Ruth Bader Ginsburg was the leader of the liberal wing, and because the court is about to open a new term, the chief justice no longer holds the controlling vote in contested cases. |
  | ELI5: What's the cause of the "anxiety lump" in our chest during stressful or disheartening experiences? | The anxiety lump in your throat is caused by muscular tension keeping your glottis dilated to maximize airflow. The clenched chest or heartache feeling is caused by the vagus nerve which tells the organs to pump blood faster, stop digesting, and produce adrenaline and cortisol. |

- 그래서 학력이 올라간다 — **따라서 기업은 시연 데이터를 만드는 데 고학력 레이블러를 쓰는 일이
  많다. InstructGPT용 시연 데이터를 레이블한 사람 중 약 90%가 최소 학사 학위를 가졌고 3분의 1
  이상이 석사 학위를 가졌다** (2장, p.82).[^huyen2025]
- 단가 — **이미지 안의 객체를 레이블하는 데 몇 초밖에 안 걸릴 수 있는 반면, (프롬프트, 응답) 쌍
  하나를 생성하는 데는 최대 30분이 걸릴 수 있다. 특히 요약처럼 긴 맥락을 포함하는 과제가 그렇다.
  (프롬프트, 응답) 쌍 하나에 10달러가 든다면 OpenAI가 InstructGPT에 쓴 13,000쌍은 130,000달러가
  들었을 것이다. 여기에는 아직 데이터를 설계하는 비용(어떤 과제와 프롬프트를 포함할지), 레이블러
  모집 비용, 데이터 품질 관리 비용이 포함되지 않았다** (2장, p.82).[^huyen2025]

## 비싼 주석을 피하는 길들

- 자원봉사 — **모두가 고품질 인간 주석 접근을 감당할 수 있는 것은 아니다. 비영리 조직 LAION은
  전 세계 13,500명의 자원봉사자를 동원해 35개 언어의 메시지 161,443개로 이뤄진 대화 10,000건을
  생성하고 461,292개의 품질 평가를 주석했다. 데이터가 자원봉사자에 의해 생성되었으므로 편향에 대한
  통제는 별로 없었다. 이론상 인간 선호를 모델에 가르치는 레이블러는 인구를 대표해야 한다. LAION의
  레이블러 인구 구성은 치우쳐 있다. 예컨대 자기 보고 설문에서 자원봉사 레이블러의 90%가 남성으로
  식별되었다(Köpf et al., 2023)** (2장, p.83).[^huyen2025]
- 휴리스틱 — **DeepMind는 자기 모델 Gopher를 훈련할 대화를 인터넷 데이터에서 걸러 내는 데 단순한
  휴리스틱을 썼다. 그들의 휴리스틱이 신뢰할 만하게 고품질 대화를 낸다고 주장했다. 구체적으로 다음
  형식처럼 보이는 텍스트를 찾았다** (2장, p.83):[^huyen2025]

  ```
  [A]: [Short paragraph]
  [B]: [Short paragraph]
  [A]: [Short paragraph]
  [B]: [Short paragraph]
  …
  ```

- AI 생성 데이터 — **고품질 인간 주석 데이터에 대한 의존을 줄이려고 많은 팀이 AI 생성 데이터로
  돌아서고 있다** (2장, p.83).[^huyen2025]
- 사전 훈련을 건너뛸 수 있는가 — **기술적으로는 사전 훈련된 모델을 파인 튜닝하는 대신 시연
  데이터로 모델을 처음부터 훈련해 자기지도 사전 훈련 단계를 사실상 없앨 수 있다. 그러나 사전 훈련
  접근이 우월한 결과를 되돌려 주었다** (2장, p.83).[^huyen2025]

## 이어지는 페이지

- [선호 파인 튜닝](../concepts/preference-finetuning.md) — 사후 훈련의 둘째 단계와 보상 모델
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 사전 훈련·파인 튜닝·사후 훈련이라는
  낱말들의 경계
- [언어 모델과 토큰](../concepts/language-models-and-tokens.md) — 완성이 대화와 같지 않다는 문제의
  출처
- [자기지도와 모델 규모](../concepts/self-supervision-and-model-scale.md) — 레이블링 비용이 어디서
  터지는지의 1장 판
- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 사전 훈련 데이터의 품질 문제

[^huyen2025]: Huyen 2025, 2장 "Understanding Foundation Models" (책 pp.49–112). 이 페이지는
    "Post-Training" 절 도입(pp.78–80)과 "Supervised Finetuning"(pp.80–83)을 담았다. Table 2-6
    (p.82)과 DeepMind 휴리스틱 형식(p.83)은 원문 표기를 그대로 옮겼다. Figure 2-12(InstructGPT
    프롬프트 분포 도넛 차트, p.81)는 그림을 옮기지 않고 표시된 수치만 표로 옮겼다. 도판
    Figure 2-10(사전 훈련·SFT·RLHF 워크플로, p.79)과 Figure 2-11(스마일 얼굴을 단 쇼고스,
    p.80)은 옮기지 않았다. Köpf et al.(2023)과 InstructGPT 수치는 huyen2025를 통한 전언이다.

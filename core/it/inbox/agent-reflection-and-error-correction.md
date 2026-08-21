---
type: concept
title: 반성과 오류 교정
description: 계획이 아니라 계획의 결과를 평가해 다음 계획을 고치는 기전 — 반성이 유용한 네 자리, 추론과 행동을 번갈아 놓아 에이전트의 흔한 패턴이 된 ReAct의 형식, 평가자와 자기 반성 모듈을 갈라 새 궤적을 제안하는 Reflexion, 구현이 쉽고 성능 향상이 놀랍지만 토큰과 지연을 대가로 낸다는 셈, 그리고 같은 예산을 재표집에 썼을 때와 견주면 그 향상이 작거나 없다는 코드 생성 실측
status: draft
generated: { by: "claude-opus-5", at: "2026-08-21T23:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: olausson2024-self-repair, resource: /it/sources/olausson2024-self-repair.md }
---

# 반성과 오류 교정

- [반성은 필수가 아니지만 성공에는 필수다](#반성은-필수가-아니지만-성공에는-필수다)
- [반성이 유용한 네 자리](#반성이-유용한-네-자리)
- [반성과 오류 교정은 다른 것이다](#반성과-오류-교정은-다른-것이다)
- [ReAct — 추론과 행동을 번갈아 놓기](#react--추론과-행동을-번갈아-놓기)
- [다중 에이전트로 하는 반성](#다중-에이전트로-하는-반성)
- [Reflexion — 평가자와 자기 반성 모듈](#reflexion--평가자와-자기-반성-모듈)
- [무엇을 대가로 내는가](#무엇을-대가로-내는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **에이전트가 자기가 틀렸다는 것을 어떻게 알아채고 고치는가.**

## 반성은 필수가 아니지만 성공에는 필수다

- **최선의 계획조차 성공 가능성을 최대화하려면 끊임없이 평가되고 조정되어야 한다. 반성(reflection)이
  에이전트가 작동하는 데 엄밀히 필요한 것은 아니지만, 에이전트가 성공하는 데는 필요하다** (6장,
  p.292).[^huyen2025]

## 반성이 유용한 네 자리

- **반성은 과제 과정 중 많은 자리에서 유용할 수 있다** (6장, p.292):[^huyen2025]
  - **사용자 질의를 받은 뒤 — 그 요청이 실행 가능한지 평가하려고.**
  - **초기 계획 생성 뒤 — 그 계획이 말이 되는지 평가하려고.**
  - **각 실행 단계 뒤 — 올바른 궤도에 있는지 평가하려고.**
  - **계획 전체가 실행된 뒤 — 과제가 완수되었는지 판정하려고.**

## 반성과 오류 교정은 다른 것이다

- 구분 (6장, p.293):[^huyen2025]

  > Reflection and error correction are two different mechanisms that go hand in hand. Reflection
  > generates insights that help uncover errors to be corrected.

- 누가 반성하는가 — **반성은 자기 비평 프롬프트(self-critique prompts)를 써서 같은 에이전트로 할 수
  있다. 결과마다 구체적인 점수를 출력하는 모델인 특화된 채점기 같은 별도 구성 요소로 할 수도 있다**
  (6장, p.293).[^huyen2025]

## ReAct — 추론과 행동을 번갈아 놓기

- 계보 — **ReAct(Yao et al., 2022)가 처음 제안한, 추론과 행동을 번갈아 놓는 것이 에이전트의 흔한
  패턴이 되었다. Yao et al.은 계획과 반성 양쪽을 아우르려고 "추론(reasoning)"이라는 용어를 썼다.
  각 단계에서 에이전트는 자기 사고를 설명하고(계획), 행동을 취하고, 그다음 관찰을 분석하도록(반성)
  요청받으며, 이는 에이전트가 과제가 끝났다고 여길 때까지 이어진다** (6장, p.293).[^huyen2025]
- **에이전트는 통상 예시를 써서 다음 형식으로 출력을 생성하도록 프롬프팅된다.** 원문 표기를 그대로
  옮겼다 (6장, p.293):[^huyen2025]

  ```text
  Thought 1: …
  Act 1: …
  Observation 1: …

  … [continue until reflection determines that the task is finished] …

  Thought N: …
  Act N: Finish [Response to query]
  ```

- 도판이 보인 실제 궤적 — **다중 홉 질의응답 벤치마크 HotpotQA(Yang et al., 2018)의 질문에 ReAct
  프레임워크를 따르는 에이전트가 응답한 예다.** 원문 표기를 그대로 옮겼다 (6장, p.294,
  Figure 6-12):[^huyen2025]

  ```text
  Question: Aside from the Apple Remote, what other device can control the program
  Apple Remote was originally designed to interact with?

  Thought 1: I need to search Apple Remote and find the program it was originally
  designed to interact with.
  Act 1: Search[Apple Remote]
  Obs 1: The Apple Remote is a remote control introduced in October 2005 by Apple …
  originally designed to control the Front Row media center program …

  Thought 2: Apple Remote was originally designed to control the Front Row media
  center program. I need to search Front Row next and find what other device can control it.
  Act 2: Search[Front Row]
  Obs 2: Could not find [Front Row]. Similar: ['Front Row Seat to Earth',
  'Front Row Motorsports',' Front Row (software)', …]

  Thought 3: Front Row is not found. I need to search Front Row (software) .
  Act 3: Search[Front Row (software) ]
  Obs 3: Front Row is a discontinued media center software …

  Thought 4: Front Row (software) is controlled by an Apple Remote or the keyboard
  function keys. So the answer is keyboard function keys.
  Act 4: Finish[keyboard function keys]
  ```

## 다중 에이전트로 하는 반성

- 배치 — **반성은 다중 에이전트 환경에서 구현할 수 있다: 한 에이전트가 계획하고 행동을 취하며, 다른
  에이전트가 각 단계 뒤 또는 몇 단계 뒤에 결과를 평가한다** (6장, p.293).[^huyen2025]
  - 각주가 떠올리는 계보 — **이는 저자에게 강화 학습의 행위자-비평가(actor-critic, AC) 에이전트
    방법(Konda and Tsitsiklis, 1999)을 떠올리게 한다** (6장, p.293 각주 14).[^huyen2025]
- 실패에서 배우기 — **에이전트의 응답이 과제를 완수하지 못했다면, 왜 실패했고 어떻게 개선할지
  반성하라고 에이전트에게 프롬프팅할 수 있다. 이 제안에 근거해 에이전트는 새 계획을 생성한다. 이는
  에이전트가 자기 실수에서 배울 수 있게 한다. 예컨대 코드 생성 과제가 주어지면 평가자는 생성된 코드가
  테스트 케이스의 3분의 1에서 실패한다고 평가할 수 있다. 그러면 에이전트는 실패한 이유가 모든 수가
  음수인 배열을 고려하지 않았기 때문이라고 반성한다. 그다음 행위자는 전부 음수인 배열을 고려한 새
  코드를 생성한다** (6장, p.293).[^huyen2025]

## Reflexion — 평가자와 자기 반성 모듈

- **이것이 Reflexion(Shinn et al., 2023)이 취한 접근이다. 이 프레임워크에서 반성은 두 모듈로
  나뉜다: 결과를 평가하는 평가자(evaluator)와 무엇이 잘못되었는지 분석하는 자기 반성(self-reflection)
  모듈이다. 저자들은 계획을 가리키는 데 "궤적(trajectory)"이라는 용어를 썼다. 각 단계에서 평가와 자기
  반성 뒤에 에이전트는 새 궤적을 제안한다** (6장, p.294, Figure 6-13).[^huyen2025]

## 무엇을 대가로 내는가

- 이점 — **계획 생성과 비교해 반성은 구현하기가 비교적 쉽고 놀랄 만큼 좋은 성능 개선을 가져올 수
  있다** (6장, p.294).[^huyen2025]
  - **이 이점 서술에는 견줄 기준이 적혀 있지 않다.** 코드 생성에서 같은 표본 예산의
    재표집을 기준선으로 놓고 재 본 실측은 이득이 작거나 없는 자리를 여럿 찾았고, 자기가
    아니라 **더 강한 모델이 피드백을 줄 때** 비로소 기준선과 자기 수정 양쪽을 넘었다
    (§4.1·§4.2, pp.5–8).[^olausson2024-self-repair] 수치와 분모는
    [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md)에 있다.
    - 버전 조건: 2023년에 동결된 모델 스냅샷 셋과 파이썬 코드 생성 벤치마크 둘, 그리고
      프롬프팅으로 구현한 자기 수정에 한정된다.
- 대가 — **이 접근의 단점은 지연과 비용이다. 사고·관찰, 때로는 행동을 생성하는 데 많은 토큰이 들 수
  있고 이는 비용과 사용자가 체감하는 지연을 늘린다 — 중간 단계가 많은 과제에서 특히 그렇다.
  에이전트가 형식을 따르도록 유도하려고 ReAct와 Reflexion의 저자들은 자기 프롬프트에 예시를 많이 썼다.
  이는 입력 토큰을 계산하는 비용을 늘리고 다른 정보에 쓸 수 있는 컨텍스트 공간을 줄인다** (6장,
  p.294).[^huyen2025]

## 이어지는 페이지

- [에이전트 계획](../concepts/agent-planning.md) — 반성이 네 과정 중 둘째와 넷째로 배치되는 자리
- [계획 생성](../concepts/plan-generation.md) — 반성이 고쳐 주는 대상
- [파운데이션 모델은 계획할 수 있는가](../concepts/foundation-models-as-planners.md) — 경로를 수정하는
  것이 백트래킹이라는 논거
- [에이전트의 실패 모드](../concepts/agent-failure-modes.md) — 반성 자체가 틀릴 때
- [사고 연쇄 프롬프팅](../concepts/chain-of-thought-prompting.md) — 자기 비평 프롬프트의 출처
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 별도 채점기·검증기가 쓰이는 다른 자리
- [AI 판정자](../concepts/ai-as-a-judge.md) — 평가자를 모델로 세우는 일반 문제
- [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md) — 자기 반성을
  같은 예산의 재표집과 견주면 얼마를 버는지, 그리고 무엇이 그 이득을 막는지를 잰 실측
- [인컨텍스트 학습](../concepts/in-context-learning.md) — 형식을 유도하는 예시가 비용이 되는 자리

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Reflection and error
    correction" 항목(pp.292–295)을 담았다. ReAct 출력 형식과 Figure 6-12(ReAct 에이전트의 궤적,
    p.294)는 원문 표기를 그대로 옮기되 도판의 강조 음영은 옮기지 않았다 — 도판의 라벨은 "Hotspot QA"로
    인쇄돼 있으나 본문은 HotpotQA로 적는다. Figure 6-13(Reflexion 에이전트 예 두 개, p.295)은 옮기지
    않았고 본문이 서술한 두 모듈 구조만 담았다. ReAct(Yao et al., 2022)·HotpotQA(Yang et al., 2018)·
    Reflexion(Shinn et al., 2023)·actor-critic(Konda and Tsitsiklis, 1999)은 huyen2025를 통한
    전언이다.

[^olausson2024-self-repair]: Olausson, Inala, Wang, Gao & Solar-Lezama 2024, "Is Self-Repair
    a Silver Bullet for Code Generation?", ICLR 2024 게재본. 이 페이지는 §4.1·§4.2의 방향만
    담았다 — 수치와 분모·표 위치는
    [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md)에 있다.

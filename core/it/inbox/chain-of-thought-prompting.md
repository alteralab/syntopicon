---
type: concept
title: 사고 사슬 프롬프팅
description: 모델에게 생각할 시간을 주는 두 관행 — 단계적으로 생각하라고 명시적으로 요청하는 사고 사슬과 그것을 도입한 2022년 논문, 모델 크기별로 성능을 끌어올린 실측과 환각이 준다는 보고, 지시 한 줄부터 예시까지 걸치는 네 가지 변형, 자기 출력을 검사하게 하는 자기 비평, 그리고 둘 다 사용자가 체감하는 지연을 늘린다는 대가
generated: { by: "claude-opus-5", at: "2026-08-16T22:30:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 사고 사슬 프롬프팅

- [생각할 시간을 준다](#생각할-시간을-준다)
- [사고 사슬이 온 자리](#사고-사슬이-온-자리)
- [네 가지 변형](#네-가지-변형)
- [자기 비평](#자기-비평)
- [지연이라는 대가](#지연이라는-대가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델에게 더 오래 생각하라고 시키는 것이 실제로 무엇을 시키는 일이고 무엇을 얻는가.**

## 생각할 시간을 준다

- 두 관행이 한 묶음이다 — **더 나은 낱말이 없어서 쓰는 표현이지만, 사고 사슬(chain-of-thought,
  CoT)과 자기 비평(self-critique) 프롬프팅을 써서 모델이 질문에 대해 "생각"하는 데 더 많은 시간을
  쓰도록 장려할 수 있다** (5장, p.227).[^huyen2025]

## 사고 사슬이 온 자리

- 규정 — **CoT는 모델에게 단계적으로 생각하라고 명시적으로 요청해, 문제 해결에 대한 더 체계적인
  접근 쪽으로 모델을 밀어 주는 것을 뜻한다** (5장, p.227).[^huyen2025]
- 출처와 시점 — **CoT는 모델을 가로질러 잘 통하는 최초의 프롬프팅 기법 중 하나다. 이것은
  "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"(Wei et al., 2022)에서
  도입되었고, 이는 ChatGPT가 나오기 거의 1년 전이다** (5장, p.227).[^huyen2025]
- 무엇이 개선되었는가 — **도판은 CoT가 서로 다른 크기의 모델들(LaMDA·GPT-3·PaLM)의 성능을 서로 다른
  벤치마크에서 어떻게 개선했는지 보인다** (5장, p.227, Figure 5-6).[^huyen2025] 도판이 든 세
  벤치마크는 MAWPS(Math Word Problem Solving)·SVAMP·GSM-8K이고, 가로축은 파라미터 수(십억 단위)로
  LaMDA는 0.4·8·137, GPT는 0.4·7·175, PaLM은 8·62·540 지점에서 표준 프롬프팅과 사고 사슬 프롬프팅을
  견준다 (5장, p.228, Figure 5-6).[^huyen2025]
- 부수 효과 — **링크드인은 CoT가 모델의 환각도 줄인다는 것을 발견했다** (5장, p.227).[^huyen2025]

## 네 가지 변형

- 가장 단순한 방법 — **CoT를 하는 가장 단순한 방법은 프롬프트에 "단계적으로 생각하라(think step by
  step)"나 "네 결정을 설명하라(explain your decision)"를 더하는 것이다. 그러면 모델이 어떤 단계를
  밟을지 스스로 알아낸다. 대안으로 모델이 밟아야 할 단계를 지정하거나 그 단계가 어떻게 생겨야 하는지의
  예시를 프롬프트에 넣을 수 있다** (5장, p.228).[^huyen2025]
- 같은 원래 질의에 대한 네 가지 CoT 변형이다 — 굵은 부분이 CoT로 더해진 것이다 (5장, p.229,
  Table 5-4):[^huyen2025]

  | 변형 | 프롬프트 |
  |---|---|
  | Original query | Which animal is faster: cats or dogs? |
  | Zero-shot CoT | Which animal is faster: cats or dogs? **Think step by step before arriving at an answer.** |
  | Zero-shot CoT | Which animal is faster: cats or dogs? **Explain your rationale before giving an answer.** |
  | Zero-shot CoT | Which animal is faster: cats or dogs? **Follow these steps to find an answer: 1. Determine the speed of the fastest dog breed. 2. Determine the speed of the fastest cat breed. 3. Determine which one is faster.** |
  | One-shot CoT (예시 하나가 프롬프트에 포함됨) | **Which animal is faster: sharks or dolphins? 1. The fastest shark breed is the shortfin mako shark, which can reach speeds around 74 km/h. 2. The fastest dolphin breed is the common dolphin, which can reach speeds around 60 km/h. 3. Conclusion: sharks are faster.** Which animal is faster: cats or dogs? |

- 어느 것을 쓸지 — **어느 변형이 가장 잘 통하는지는 애플리케이션에 달려 있다** (5장,
  p.228).[^huyen2025]

## 자기 비평

- 규정 — **자기 비평은 모델에게 자기 출력을 검사하라고 요청하는 것을 뜻한다. 이는 3장에서 논의한
  대로 자기 평가(self-eval)로도 알려져 있다. CoT와 비슷하게 자기 비평은 모델이 문제에 대해 비판적으로
  생각하도록 밀어 준다** (5장, p.229).[^huyen2025] 그 평가 쪽 자리는
  [AI 판정자](../concepts/ai-as-a-judge.md)가 담는다.

## 지연이라는 대가

- **프롬프트 분해와 비슷하게 CoT와 자기 비평은 사용자가 지각하는 지연을 늘릴 수 있다. 사용자가 첫
  출력 토큰을 보기 전에 모델이 여러 중간 단계를 수행할 수 있다. 모델이 스스로 단계를 떠올리도록
  장려하면 이는 특히 어려워진다. 그 결과로 나오는 단계의 연속은 끝나는 데 오래 걸릴 수 있어 지연이
  늘고 잠재적으로 감당 못 할 비용으로 이어진다** (5장, p.229).[^huyen2025]

## 이어지는 페이지

- [프롬프트 분해](../concepts/prompt-decomposition.md) — 같은 대가를 내는 앞 관행
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 사고 사슬 질의의 지연을 병렬 생성으로
  덮는 접근과 여러 출력을 뽑아 고르는 전략
- [AI 판정자](../concepts/ai-as-a-judge.md) — 자기 평가가 놓인 평가 접근
- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 단계를 지정하는 지시를
  쓰는 관행
- [인컨텍스트 학습](../concepts/in-context-learning.md) — 원샷 CoT가 기대는 예시 학습
- [비용과 지연 기준](../concepts/cost-and-latency-criteria.md) — 지연이 선택 기준이 되는 자리
- [스케일링 법칙](../concepts/scaling-laws.md) — 도판의 가로축인 모델 규모가 논의되는 자리

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 "Give the Model Time
    to Think" 절(pp.227–229)을 담았다. Figure 5-6(모델 규모별 CoT 효과 9패널 선 그래프, p.228 —
    Wei et al. 2022의 갈무리, CC BY 4.0)은 점마다 값이 인쇄돼 있지 않아 벤치마크 이름·모델 규모
    눈금과 본문의 결론만 담았다. 도판 설명은 SVAMP를 "sequence variation analysis, maps, and
    phylogeny"로 풀어 쓰는데 원문 표기 그대로다. Table 5-4는 원문 표기를 그대로 옮기되 셀 안의
    번호 목록 줄바꿈을 공백으로 이어 붙였고, 굵은 표시(CoT로 더해진 부분)는 원문의 것이다. Wei et
    al.(2022)·링크드인의 보고는 huyen2025를 통한 전언이다.

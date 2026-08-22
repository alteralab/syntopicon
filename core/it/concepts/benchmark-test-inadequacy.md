---
type: concept
title: 벤치마크의 테스트 부족
description: 코드 생성 벤치마크의 통과율이 대상의 옳음이 아니라 그 벤치마크가 가진 테스트의 판별력을 재고 있었다는 실측 — HumanEval의 문항당 테스트가 평균 몇 개였는지, 테스트만 80배로 늘렸을 때 같은 모델의 pass@k가 얼마나 떨어지는지, 모델 순위가 뒤집힌 사례, 정답 구현 자체에 있던 결함, 엣지 케이스를 명시 지시와 타입 인지 변이로 만들어 낸 방법, 47배로 줄인 스위트가 같은 판별력을 유지한다는 결과, 그리고 이 값들이 2023년 모델군에 묶여 있어 방향만 옮겨 쓸 수 있다는 경계
generated: { by: "claude-opus-5", at: "2026-08-23T05:55:00Z" }
sources:
  - { id: liu2023-evalplus, resource: /it/sources/liu2023-evalplus.md }
---

# 벤치마크의 테스트 부족

- [버전 조건](#버전-조건)
- [이 소스의 지위](#이-소스의-지위)
- [무엇을 어떻게 쟀는가](#무엇을-어떻게-쟀는가)
- [원래 벤치마크의 테스트는 몇 개였나](#원래-벤치마크의-테스트는-몇-개였나)
- [테스트를 늘리면 통과율이 떨어진다](#테스트를-늘리면-통과율이-떨어진다)
- [순위가 뒤집힌다](#순위가-뒤집힌다)
- [정답 구현 자체가 틀려 있었다](#정답-구현-자체가-틀려-있었다)
- [엣지 케이스는 명시 지시로 만들어진다](#엣지-케이스는-명시-지시로-만들어진다)
- [판별력은 테스트 개수가 아니다](#판별력은-테스트-개수가-아니다)
- [이 수치들의 유통기한](#이-수치들의-유통기한)
- [리더보드는 멈춰 있다](#리더보드는-멈춰-있다)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **벤치마크의 통과율은 생성된 코드의 옳음을 재는가, 아니면 그 벤치마크가
가진 테스트의 판별력을 재는가.**

[기능적 정확성](../concepts/functional-correctness.md)이 "무엇을 재면 판정자에 따라
흔들리지 않는가"에 답하면서 HumanEval과 pass@k를 그 답의 실물로 든다면, 이 페이지는
**그 실물의 분모를 재본 자리**다. 대상 코드를 하나도 바꾸지 않고 벤치마크의 테스트만
강화했을 때 통과율이 어떻게 움직이는지가 이 논문의 측정이다.

## 버전 조건

> **버전 조건**: HumanEval 164문항과 그것을 확장한 HumanEval+, 2021년부터 2023년
> 사이에 공개된 모델 26종, 측정 시점 2023년. **이 페이지의 절대 수치는 전부 그
> 조합에서 잰 값이고 지금 세대 모델에는 그대로 적용되지 않는다.** 옮겨 쓸 수 있는
> 것은 값이 아니라 **방향**이다 — 대상을 그대로 두고 테스트만 강화하면 통과율이
> 내려가고 모델 사이 순위가 바뀐다. 모델 목록은 Table 5(p.15)에 공개 연도와 함께
> 실려 있다.

## 이 소스의 지위

- **근거 등급은 심사 실증(`peer-reviewed`)이다.** 확보본은 arXiv v3(2023-10-30)이지만
  1쪽 하단에 게재 표면이 인쇄된 게재본 조판이다 (p.1 각주 줄).[^liu2023-evalplus]

  > 37th Conference on Neural Information Processing Systems (NeurIPS 2023).

- **그래서 이 페이지는 이 논문이 스스로 잰 값만 옮긴다.** 논문이 인용한 제3자의 수치와
  이 논문 바깥의 후속 보고는 옮기지 않거나, 옮길 때 원문 밖이라고 밝힌다.
- **인용 위치는 확보본 PDF 쪽과 표·절 번호다.** NeurIPS 프로시딩은 권·호로 매기지
  않고 확보본에도 논문 안 쪽 번호(1~15)만 있다.

## 무엇을 어떻게 쟀는가

- **대상 벤치마크** — HumanEval 164문항이다. 문항 하나가 파이썬 함수 서명과 독스트링을
  입력으로 주고, 모델이 채운 해답의 기능적 정확성을 소수의 수작성 테스트가 판정한다
  (§3, p.6).[^liu2023-evalplus]
- **처치** — 대상 모델도 프롬프트도 그대로 두고 **테스트 케이스만** 늘렸다.
  EvalPlus가 HumanEval을 HumanEval+로 바꾸는 조작은 고유 테스트 케이스를 **80배**
  추가하고 HumanEval의 틀린 정답 구현을 고치는 것이다 (§3, p.6).[^liu2023-evalplus]
- **생성 예산** — 문항마다 ChatGPT가 만든 씨앗 입력(seed input) 약 30개를 프롬프트 3종으로
  얻은 뒤, 타입 인지 변이(type-aware mutation)로 한 시간 예산 안에서 입력 1,000개를 더
  만들었다. 164문항 중 83문항에는 손으로 쓴 계약(contract)을 달았다 (§3,
  p.6).[^liu2023-evalplus]
- **모델과 표집 설정** — 모델 26종을 평가했고, 모델마다 온도 네 값(0.2, 0.4, 0.6, 0.8)
  각각에서 프로그램 200개를 무작위 표집하고 별도로 그리디 디코딩(greedy decoding)을
  한 번 돌렸다. pass@k는 k가 1, 10, 100일 때 **가장 좋은 온도의 값**을 싣고, 그리디
  디코딩의 pass@1은 `pass@1⋆`로 따로 적는다 (§3, p.6).[^liu2023-evalplus] 상용 모델
  둘은 예외다 — GPT-4는 그리디 디코딩만, ChatGPT는 거기에 온도 0.8 표집을 더했다.
- **오라클** — 차등 테스트(differential testing)다. 논문이 다시 구현한 정답 풀이와
  생성 코드의 출력을 대조하고, 기본은 정확 일치이며 부동소수는 HumanEval이 적어 둔
  허용 오차 또는 10의 마이너스 6제곱을 쓴다. 테스트 하나의 제한 시간은 200밀리초와
  정답 풀이 실행 시간의 4배 중 큰 쪽이다 (부록 A, p.15).[^liu2023-evalplus]

## 원래 벤치마크의 테스트는 몇 개였나

이 논문의 출발점이 이 수치다. **판별력을 먼저 재보면 벤치마크가 무엇을 재고 있었는지가
드러난다** (Table 2, p.6).[^liu2023-evalplus]

| 데이터셋 | 문항당 테스트 평균 | 중앙값 | 최소 | 최대 |
|---|---|---|---|---|
| HumanEval | 9.6 | 7.0 | 1 | 105 |
| HumanEval+ | 764.1 | 982.5 | 12 | 1,100 |
| HumanEval+ -MINI | 16.1 | 13.0 | 5 | 110 |

- **분모는 164문항이고 집계 단위는 문항 하나당 테스트 케이스 수다** (Table 2,
  p.6).[^liu2023-evalplus]
- **최대 105는 네 문항이 끌어올린 값이다** — `add(x, y)` 같은 문항 넷이 정답 풀이를
  무작위 입력으로 되대조하는 방식이라 "테스트"가 100개를 넘는다. 그 넷을 빼면
  최대와 평균은 26개와 7.3개다 (p.6 각주 2).[^liu2023-evalplus]
- **논문이 문제로 세운 문면** (§1, p.2):[^liu2023-evalplus]

  > **Insufficient testing.** Current programming benchmarks often only include on
  > average less than 10 tests for each coding problem. Furthermore, these tests are
  > relatively too simple to fully explore the functionality of the code or corner cases.

## 테스트를 늘리면 통과율이 떨어진다

- **거의 모든 값이 내려간다** (§3, p.6):[^liu2023-evalplus]

  > We first observe that across all LLMs, models sizes and *k* values, using
  > HUMANEVAL+, almost all pass@*k* results **consistently drop** compared to using the
  > base HUMANEVAL.

- **하락 폭의 상한을 k별로 갈라 적는다** (§3, p.6):[^liu2023-evalplus]

  > Notably, the performance drop is significant with up-to 23.1% (pass@1⋆) / 19.3%
  > (pass@1) / 24.9% (pass@10) / 28.9% (pass@100) reduction over the evaluated models.

  **단위는 상대 감소율(%)이지 퍼센트포인트가 아니다.** 분모는 그 모델의 HumanEval
  통과율이고, 네 값은 각각 그 k에서 **모델 26종에 걸친 최댓값**이다. 곧 한 모델이
  네 값을 다 낸 것이 아니다.
- **단위가 상대 %임을 표가 확인해 준다** — 본문이 예로 든 CodeGen-16B의
  `18.5% reduction`은 Table 3의 pass@1⋆ 32.9 → 26.8에서 6.1을 32.9로 나눈 값이고,
  StarCoder-15B의 `14.1%`(34.1 → 29.3)와 CODELLAMA-34B의 `17.6%`(51.8 → 42.7)도
  같은 계산이다 (§3, p.6; Table 3, p.7).[^liu2023-evalplus]
- **상위 모델의 하락은 상한보다 작다** (Table 3, p.7).[^liu2023-evalplus] 그리디
  디코딩 pass@1⋆ 기준이다.

  | 모델 | HumanEval | HumanEval+ |
  |---|---|---|
  | GPT-4 | 88.4 | 76.2 |
  | ChatGPT | 73.2 | 63.4 |
  | Phind-CodeLlama 34B | 71.3 | 67.1 |
  | WizardCoder-CodeLlama 34B | 73.2 | 64.6 |
  | StarCoder 15B | 34.1 | 29.3 |
  | INCODER 6.7B | 15.9 | 12.2 |

  **상한을 만드는 것은 작고 오래된 모델 쪽이다.** 위 표에서 상대 하락이 가장 큰 것은
  INCODER-6.7B이고(15.9 → 12.2), 이는 논문이 pass@1⋆의 상한으로 적은 23.1%에 가장
  가까운 자리다. GPT-4와 ChatGPT의 같은 계산은 그보다 훨씬 작다. **이 대조는 Table 3의
  값에서 이 KB가 계산한 것이고, 논문 본문이 산문으로 적은 모델별 하락률과는 어긋난다**
  — 아래 [이 소스의 사각](#이-소스의-사각)을 보라.

## 순위가 뒤집힌다

통과율이 내려가는 것보다 무거운 결과가 이쪽이다. **테스트가 부족하면 순위 자체가
틀린다.**

- **논문의 문면** (§3, p.8):[^liu2023-evalplus]

  > For example, WizardCoder-CodeLlama and Phind-CodeLlama on the original HUMANEVAL
  > are evaluated to be no better than ChatGPT in terms of pass@1⋆. However,
  > HUMANEVAL+ demonstrates that the two open-source models can actually outperform
  > the proprietary ChatGPT. Other contrary examples reflected by HUMANEVAL+ include
  > that SantaCoder-1B surpasses INCODER-6.7B and VICUNA-7B outperforms INCODER-1.3B.

- **표에서 읽히는 것** — HumanEval에서는 ChatGPT 73.2가 WizardCoder-CodeLlama-34B와
  같고 Phind-CodeLlama-34B의 71.3보다 위인데, HumanEval+에서는 Phind 67.1과
  WizardCoder 64.6이 ChatGPT 63.4 위로 올라간다 (Table 3, p.7).[^liu2023-evalplus]
- **순위 역전은 통과율 하락과 다른 성질의 손해다.** 통과율은 모든 모델에서 함께
  내려가므로 상대 비교가 살아남을 수도 있지만, 역전이 실재한다는 것은 **부족한 테스트
  아래에서는 모델 선택 자체가 틀릴 수 있다**는 뜻이다.

## 정답 구현 자체가 틀려 있었다

- **결함 18건이 나왔다** (§3, p.9):[^liu2023-evalplus]

  > In addition to detecting wrong code from LLMs using EvalPlus, we also found 18
  > defects (11% of problems) even in the original ground-truth in HUMANEVAL

  분모는 164문항이고 갈래는 셋이다 — 처리하지 못한 엣지 케이스 5건, 논리 오류 10건,
  성능 문제 3건이다. 논문은 논리 오류 10건을 가장 심각하다고 적는다. 정답이 사용자
  의도를 반영하지 못한다는 뜻이기 때문이다 (§3, p.9).[^liu2023-evalplus]
- **예시가 판별력 부족을 그대로 보인다** — HumanEval 124번 `valid_date`는 파이썬에서
  `and`가 `or`보다 우선하는 것을 놓쳐 두 조건을 함께 요구하는 대신 어느 하나만
  만족해도 되게 구현돼 있었다. 생성된 입력 `12-31-1999`가 이것을 드러냈고, 논문은
  이 오류가 **원래 테스트 입력 어느 것으로도 드러나지 않았다**고 적는다 (Figure 4·
  §3, p.9).[^liu2023-evalplus]
- **§3 앞부분의 서술은 `over 10%`이고 뒤의 정확한 값이 18건 11%다** (§3, pp.6, 9).
  [^liu2023-evalplus] 이 페이지는 뒤의 값을 쓴다.

## 엣지 케이스는 명시 지시로 만들어진다

호출자가 부르는 자리 하나가 이쪽이다. **엣지 케이스는 저절로 생기지 않았고, 무엇을
만들라는 지시와 타입별 변이 규칙으로 만들어졌다.**

- **씨앗은 명시 지시로 얻는다** — 프롬프트는 세 부분이다. 정답 풀이, 예시로 넣는 기존
  테스트 입력, 그리고 흥미로운 입력을 내놓으라는 지시다 (§2.1, p.4).[^liu2023-evalplus]

  > Following Figure 2, we construct a prompt using *(i)* the ground-truth solution of
  > the problem for ChatGPT to inspect; *(ii)* a set of test inputs as demonstration;
  > and *(iii)* an instruction to encourage ChatGPT to come up with interesting inputs.

- **그 지시의 문면이 도판에 셋 실려 있다** (Figure 2, p.3):[^liu2023-evalplus]

  > generate complex inputs / generate difficult inputs / generate corner-case inputs

- **양은 변이가 댄다** — 모델 질의는 속도와 비용 때문에 대량 생성에 맞지 않으므로,
  씨앗에서 출발해 타입 인지 변이로 입력을 불린다. 변이 규칙은 타입마다 정해져 있다 —
  정수와 실수는 1을 더하거나 빼고, 리스트는 항목을 지우거나 되풀이하거나 재귀적으로
  변이시키고, 문자열은 부분 문자열을 지우거나 되풀이하거나 바꾸고, 사전은 키와 값 쌍을
  지우거나 갱신하거나 끼워 넣는다 (Table 1·§2.1, p.4).[^liu2023-evalplus]
- **무엇이 유효한 입력인지는 계약이 정한다** — `assert n > 0` 꼴의 사전 조건(pre-condition)을
  손으로 달아 두 가지를 얻는다. 생성된 무효 입력을 걸러 내는 것과, 자연어 설명만으로는
  모호한 기대 동작을 프롬프트 쪽에서 함께 밝히는 것이다 (§2.3, p.5).[^liu2023-evalplus]
- **곧 이 논문에서 "엣지"는 발견된 것이 아니라 제조된 것이다.** 무엇을 만들라고 이름
  붙여 지시하고, 타입 구조를 아는 변이로 그것을 불리고, 계약으로 유효 범위를 자른다.

## 판별력은 테스트 개수가 아니다

- **47배로 줄여도 같은 만큼 잡는다** — HumanEval+의 문항당 평균 764.1개를 16.1개로 줄인
  HumanEval+ -MINI가 pass@1⋆ 하락을 거의 그대로 낸다 (§3, p.8; Table 4,
  p.8).[^liu2023-evalplus]
- **줄이는 기준은 셋이다** — 분기 커버리지(branch coverage), 죽인 뮤턴트(killed mutant),
  그리고 **다른 모델이 낸 틀린 표본을 잡아내는가**(killed sample)다. 셋을 합쳐 탐욕적
  집합 덮기(greedy set covering)로 최소 부분집합을 고른다 (§2.2, p.5;
  §3, p.8).[^liu2023-evalplus]
- **셋 중 경험적 기준이 가장 강했다** (§3, p.8):[^liu2023-evalplus]

  > Specifically, the use of empirical LLM sample killings is the most effective,
  > leading to the same effectiveness as the full approach, but also consumes more
  > tests than other theoretical metrics.

  커버리지와 뮤테이션 분석은 표본 잡기 위에 더 얹을 것이 없어 보이지만 이론적 적절성의
  기본 보증으로는 남는다고 같은 자리가 적는다.
  - **여기서 죽인 뮤턴트는 스위트를 줄이는 세 기준 중 하나로 쓰였지 판정의 최종 눈금이
    아니다.** 그 기준이 어디서 왔고 어디까지 지지되는지는
    [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md)에
    있다. **이 자리의 읽기와 그쪽의 판정이 같은 방향이다** — 뮤테이션은 보증이지
    최종 심급이 아니다.
- **읽히는 것은 이렇다** — 통과율을 부풀린 것은 테스트가 **적어서**만이 아니라 남은
  테스트가 **못 갈라서**다. 반대로 잘 고른 16개가 764개와 거의 같은 일을 한다.
  개수는 판별력의 대리 지표일 뿐이다.

## 이 수치들의 유통기한

**이 페이지의 값은 조항에 박을 것이 아니다.** 아래 세 가지가 그 이유다.

- **상한은 약한 모델이 만든다.** 19.3%에서 28.9% 사이라는 상한은 모델 26종에 걸친
  최댓값이고, 위 [표](#테스트를-늘리면-통과율이-떨어진다)가 보이듯 당시 최상위 모델
  둘의 하락은 그보다 눈에 띄게 작다. **평가 대상 모델군이 세대 전체로 올라가면 이
  상한은 그대로 유지되지 않는다.**
- **원문 밖의 후속 보고도 같은 방향을 가리킨다** — 지금 세대 프론티어 모델에서는
  같은 조작의 상대 하락이 훨씬 작다는 보고가 있다. **2차 경유이고 이 KB는 그 값을
  확인하지 않았으므로 수치를 옮기지 않는다.** 옮기는 것은 방향뿐이다 — 모델이 좋아질수록
  이 격차는 줄어든다.
- **그래서 인용 규율은 이렇다.** 수치를 쓸 때는 위 [버전 조건](#버전-조건)의 조합
  (데이터셋 판·문항 수·어느 k·모델군·측정 연도)을 함께 적고, 조항에는 **방향만**
  싣는다. 이 규율의 근거는
  [LLM 실증 연구의 보고 규범](../concepts/llm-empirical-study-reporting-norms.md)의
  5.2다 — 모델 판과 실행 시점을 밝히는 것은 방법론 취향이 아니라 요구 층에 있다.

## 리더보드는 멈춰 있다

**이 절은 원문 밖의 사실이다.** 논문은 §5에서 새 모델을 계속 평가하며 리더보드를
유지한다고 적지만, 그 리더보드의 현재 상태는 논문이 말할 수 있는 바가 아니다.

- **논문이 적은 것** (§5, p.10):[^liu2023-evalplus]

  > We also keep evaluating new models for code and maintain a leaderboard at
  > https://evalplus.github.io/leaderboard.html.

- **이 KB가 확인한 것** — 리더보드를 담은 저장소 `evalplus/evalplus.github.io`의
  최신 커밋이 **2024-12-26**이고 그 뒤로 새 커밋이 없다. 열람일은 2026-08-22이고
  확인 경로는 GitHub API의 커밋 목록이다. 곧 **이 리더보드의 값은 2024년 말에
  멈춘 값이다.**
- #hypothesis **멈춘 이유는 확인하지 못했다.** 포화나 오염 때문이라는 설명이 있으나
  저장소와 리더보드 페이지 어디에도 중단을 알리는 고지가 없어 이 KB는 확인하지
  못했다. **확인된 것은 갱신이 멈췄다는 사실뿐이다.**
- **읽는 법** — HumanEval+ 값을 지금 모델 비교에 쓰려면 리더보드를 인용하지 말고
  직접 돌려야 한다. 멈춘 리더보드는 그 시점의 스냅샷이지 현재 순위가 아니다.

## 이 소스의 사각

- **본문 산문의 모델별 하락률이 표와 어긋난다.** §3은 GPT-4를 `13.1%`, ChatGPT를
  `12.6%`로 적는데, Table 3의 값으로 같은 계산을 하면 각각 13.8%(88.4 → 76.2)와
  13.4%(73.2 → 63.4)다. CodeGen-16B와 StarCoder와 CODELLAMA-34B는 표와 맞으므로 계산
  방식이 다른 것이 아니다 (§3, p.6; Table 3, p.7).[^liu2023-evalplus] **그래서 이
  페이지는 표 값을 쓰고 산문의 모델별 수치는 옮기지 않는다.**
- **논문 안에서 평균 테스트 수가 두 값으로 적힌다.** Table 2와 §3 본문은 HumanEval+의
  문항당 평균을 764.1로 적는데, Table 4의 캡션은 같은 값을 774.8로 적으며 Table 2를
  가리킨다 (Table 2·§3, pp.6, 8; Table 4, p.8).[^liu2023-evalplus] 이 페이지는 표
  본체의 764.1을 쓴다.
- **한 벤치마크 한 언어다.** 측정은 HumanEval에만 걸렸고 언어는 파이썬뿐이다. MBPP로
  넓히는 것은 §5가 향후 과제로 적는다 (§5, p.10).[^liu2023-evalplus] 다른 벤치마크와
  다른 언어에서 같은 크기의 하락이 나온다는 근거는 이 논문에 없다.
- **HumanEval+의 정답 풀이도 사람이 다시 쓴 것이다.** 논문은 원래 정답의 결함을
  차등 테스트로 찾았다고 밝히는데, 그 기준선은 저자들이 재구현한 정답이다 (§3,
  p.9).[^liu2023-evalplus] 곧 이 실험의 오라클은 **더 나은 사람의 구현**이지 형식
  명세가 아니다.
- **오염을 다루지 않는다.** 평가 대상 모델들이 HumanEval을 학습에서 봤을 가능성은
  이 논문의 물음 밖이다. 그쪽은 [데이터 오염](../concepts/data-contamination.md)이
  다루고, 이 논문의 조작(테스트 강화)은 오염 대책이 아니라 판별력 대책이다.

## 이어지는 페이지

- [기능적 정확성](../concepts/functional-correctness.md) — HumanEval과 pass@k가
  기능적 정확성의 실물로 소개되는 자리. 이 페이지는 그 실물의 판별력을 잰다
- [공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md) —
  벤치마크를 고르고 집계하는 쪽. 이 페이지는 고른 벤치마크 하나 안에서 무엇이
  흔들리는지를 다룬다
- [데이터 오염](../concepts/data-contamination.md) — 점수를 부풀리는 다른 경로.
  오염은 모델이 답을 기억한 것이고, 테스트 부족은 벤치마크가 못 가르는 것이다
- [에이전트의 테스트 케이스 착취](../concepts/test-case-exploitation-by-agents.md) —
  같은 통과율을 반대편에서 무너뜨리는 경로. 이쪽은 테스트가 약해서 통과가 부풀고,
  그쪽은 테스트가 피판정자의 권한 안에 있어서 통과가 만들어진다
- [벤치마크의 수명과 철회](../concepts/benchmark-lifespan-and-retirement.md) — 같은 병의
  반대 방향. 이쪽은 테스트가 못 갈라 옳지 않은 코드가 통과하는 자리를, 그쪽은 테스트가
  너무 좁거나 너무 넓어 옳은 코드가 떨어지는 자리를 잰다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 판별력을
  무엇으로 잴 것인가의 산업 판. 이 페이지가 스위트를 줄일 때 쓴 세 기준(분기 커버리지·
  죽인 뮤턴트·틀린 표본 잡기)이 거기서는 수용 관문의 마지막 조건을 무엇으로 둘 것인가의
  선택으로 다시 나온다
- [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md) —
  그 세 기준 중 죽인 뮤턴트가 어디서 온 기준이고 어디까지 지지되는가
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  통과가 부재의 증거가 아니라는 상한 명제. 이 페이지는 그 명제가 벤치마크 통과율에서
  실제로 얼마짜리 착시였는지를 잰 실측이다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  같은 문제의 반대쪽. 그쪽은 모델이 만든 테스트가 얼마나 틀리는지를, 이쪽은 사람이
  만든 벤치마크 테스트가 얼마나 못 가르는지를 잰다
- [LLM 실증 연구의 보고 규범](../concepts/llm-empirical-study-reporting-norms.md) —
  이 페이지가 버전 조건 블록을 다는 근거
- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 공개 벤치마크
  다음에 자기 평가를 세우는 쪽
- [테스트 오라클](../concepts/test-oracle.md) — 차등 테스트가 오라클의 한 갈래로
  놓이는 자리
- [벤치마크와 수용 판정의 무결성](../synthesis/benchmark-and-acceptance-integrity.md) —
  이 갈래의 허브

[^liu2023-evalplus]: Liu, Xia, Wang & Zhang 2023, "Is Your Code Generated by ChatGPT
    Really Correct? Rigorous Evaluation of Large Language Models for Code Generation",
    37th Conference on Neural Information Processing Systems (NeurIPS 2023). 확보본은
    arXiv:2305.01210 **v3**(2023-10-30)이고 15쪽이며 1쪽 하단에 NeurIPS 2023 게재
    표면이 인쇄돼 있다. 권·호·쪽수가 없어 쪽 표기는 확보본 PDF의 논문 안 쪽 번호다.
    이 페이지가 담은 것은 §1의 문제 제기, §2.1~§2.3의 생성·축소·계약 방법과 Table 1,
    §3의 설정과 결과(Table 2·Table 3·Table 4·Figure 4), §5의 결론, 부록 A의 오라클
    설정과 Table 5다. §4 관련 연구와 참고문헌(pp.11~14)은 이 페이지의 물음 밖이라
    옮기지 않았다. Table 3과 Table 4는 다단 표라 기본 텍스트 추출에서 순서가 뒤섞여
    `pdftotext -layout`으로 정렬한 판을 대조해 옮겼고, 이 페이지의 두 표는 그 대조를
    거친 값이다. Figure 3(문항별 통과율 분포)은 축이 로그 척도이고 막대에 값이 인쇄돼
    있지 않아 옮기지 않았다. 리더보드 갱신 중단은 이 논문의 진술이 아니라 이 KB가
    2026-08-22에 GitHub API로 확인한 원문 밖 사실이다.

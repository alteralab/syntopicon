---
type: concept
title: 생성된 테스트의 필터 체인
description: 모델이 만든 테스트를 사람에게 보내기 전에 무엇이 거르는가를 Meta의 두 배포 보고로 읽는 자리 — 빌드·실행·반복 실행·커버리지의 네 관문과 그 순서, 각 관문이 결정적 도구이지 LLM이 아니라는 것, 관문마다 남는 비율과 집계 단위, 배포에서 엔지니어가 실제로 수용한 비율과 거절 사유, 그리고 후속 시스템이 수용 조건을 커버리지에서 결함 검출로 옮기면서 드러난 것 — 커버리지 필터였다면 버려졌을 테스트의 비율과 등가 뮤턴트를 판정하는 LLM 심판의 정밀도·재현율
generated: { by: "claude-opus-5", at: "2026-08-22T11:00:00Z" }
sources:
  - { id: alshahwan2024-testgen-llm, resource: /it/sources/alshahwan2024-testgen-llm.md }
  - { id: foster2025-ach, resource: /it/sources/foster2025-ach.md }
---

# 생성된 테스트의 필터 체인

- [버전 조건](#버전-조건)
- [두 소스의 지위](#두-소스의-지위)
- [필터 체인 — 무엇이 어떤 순서로 거르는가](#필터-체인--무엇이-어떤-순서로-거르는가)
- [필터는 LLM이 아니다](#필터는-llm이-아니다)
- [관문마다 얼마나 남는가](#관문마다-얼마나-남는가)
- [배포에서 사람이 수용한 비율](#배포에서-사람이-수용한-비율)
- [필터를 통과한 것도 사람이 거른다](#필터를-통과한-것도-사람이-거른다)
- [후속 시스템 — 결함을 먼저 만들고 그 결함을 잡는다](#후속-시스템--결함을-먼저-만들고-그-결함을-잡는다)
- [등가 뮤턴트를 판정하는 LLM 심판](#등가-뮤턴트를-판정하는-llm-심판)
- [커버리지 관문이 버렸을 테스트](#커버리지-관문이-버렸을-테스트)
- [두 논문의 관계](#두-논문의-관계)
- [이 KB의 읽기: 수용의 조건은 필터에 적혀 있다](#이-kb의-읽기-수용의-조건은-필터에-적혀-있다)
- [두 소스의 사각](#두-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델이 만든 테스트를 사람에게 보내기 전에 무엇이 거르며, 그 관문을 통과한
것은 산업 규모에서 실제로 얼마나 받아들여지는가.**

[LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md)가
모델이 만든 테스트가 **어디서 얼마나 틀리는가**를 실험실에서 전수로 쟀다면, 이 페이지는
같은 결함을 **사람 앞에 닿기 전에 걸러 내려고 실제로 세운 장치**와 그 장치의 통과율이다.
앞쪽이 병의 분포이고 이쪽이 그 병에 대한 산업 대응이다.

## 버전 조건

> **버전 조건**: 앞쪽 절반은 TestGen-LLM이고 **모델은 Meta 내부 LLM 둘(`LLM1`·`LLM2`,
> 논문이 상업 기밀이라며 정체를 밝히지 않는다), 언어는 코틀린(Kotlin), 대상은 안드로이드
> 앱(Instagram·Facebook), 배포 데이터 수집 기간은 2023년 10월 29일부터 12월 29일까지**다.
> 뒤쪽 절반은 ACH이고 **모델은 Llama 3.1 70B 하나, 언어는 코틀린, 대상은 Meta의 안드로이드
> 플랫폼 일곱과 여러 앱에 걸친 제품, 배포 기간은 2024년 10월 28일부터 12월 31일까지**다.
> **두 절반의 절대 수치는 서로 비교되지 않는다** — 관문의 마지막 조건이 다르고(커버리지
> 증가 대 뮤턴트 사살) 분모도 다르다. 커버리지는 둘 다 **줄 커버리지(line coverage)**뿐이다
> — TestGen-LLM 각주 3이 분기 커버리지는 Meta 규모에서 수집할 수 없다고 적는다.

## 두 소스의 지위

**둘 다 심사 학회 게재작이지만, 재는 사람과 재이는 대상이 같은 회사다.**

| | TestGen-LLM | ACH |
|---|---|---|
| 소스 | [alshahwan2024-testgen-llm](../sources/alshahwan2024-testgen-llm.md) | [foster2025-ach](../sources/foster2025-ach.md) |
| 게재 표면 | `FSE ’24`(문면). Companion·산업 트랙 여부는 문면에 없고 레코드 근거 | `FSE Companion ’25`(문면) |
| 근거 등급 | **심사 게재 + 산업 자기 보고** | **심사 게재 + 산업 자기 보고** |
| 재현 가능성 | 없음 — Meta 내부 코드베이스·비공개 모델 | 없음 — 같은 이유 |

- **심사를 통과했다는 것이 값의 독립성을 주지 않는다.** 두 논문의 수치는 전부 **Meta가
  자기 배포에서 자기 도구로 센 값**이고, 코드·뮤턴트·리뷰 기록 어느 것도 공개되지 않는다.
  이 페이지가 옮기는 값은 전부 그 형태로 읽어야 한다.
- **규모 전제를 떼면 값이 다른 말이 된다.** TestGen-LLM은 중앙 저장소가 주당 10만 건이
  넘는 커밋을 받고 앱 하나의 클라이언트 코드가 수천만 줄이라는 환경을 스스로 적는다
  (§3, p.4).[^alshahwan2024-testgen-llm] 필터를 매 후보마다 빌드·실행으로 돌리는 설계는
  그런 빌드·테스트 인프라가 이미 있을 때만 성립한다.
- **시대 지위는 둘 다 LLM 시대의 문서다.** 다만 도구 쪽 계보는 그 이전이다 — TestGen-LLM은
  자기 접근을 유전적 개선(Genetic Improvement)과 자동 수리(automated repair)의
  생성-검사(generate-and-test) 계보에 놓고, 생성기만 언어 모델로 갈아 끼운 것이라 적는다
  (§6, p.10).[^alshahwan2024-testgen-llm]

## 필터 체인 — 무엇이 어떤 순서로 거르는가

**이 페이지의 중심이다.** TestGen-LLM은 관문을 순서대로 세우고, 앞 관문을 통과한 것만 뒤
관문에 넣는다 (§2, pp.2–3).[^alshahwan2024-testgen-llm]

| # | 관문 | 무엇을 요구하는가 | 통과 못 하면 |
|---|---|---|---|
| 1 | 빌드 | 대상 앱의 기존 인프라 안에서 온전히 빌드된다 | 즉시 버린다 |
| 2 | 실행 | 첫 실행에서 통과한다 | 버린다 |
| 3 | 반복 실행 | 다섯 번 실행에서 **매번** 통과한다 | 불안정(flaky)으로 보고 버린다 |
| 4 | 커버리지 | 같은 빌드 타깃을 공유하는 **기존 모든 테스트 클래스보다** 줄 커버리지를 늘린다 | 버린다 |

- **첫째 관문** (§2, p.2):[^alshahwan2024-testgen-llm]

  > The first filter simply checks that the candidate code is fully buildable within the
  > existing infrastructure of the app under test. Any code that does not build is
  > immediately discarded and thereby removed from further consideration.

- **둘째 관문이 오라클 문제를 우회하는 방식이 이 설계의 핵심 판단이다** (§2,
  p.2):[^alshahwan2024-testgen-llm]

  > Any test that does not pass may reveal a fault. However, it is more likely that the
  > test simply contains an incorrect assertion. We want an entirely automated workflow.
  > Without an automatable test oracle [7], TestGen-LLM cannot automatically determine
  > whether a failing test has found a bug, or whether it merely contains an incorrect
  > test assertion. Therefore, TestGen-LLM discards any test case that does not pass on
  > first execution.

  곧 **실패한 테스트는 전부 버린다.** 자동화할 수 있는 오라클이 없으면, 실패한 테스트가
  대상의 버그를 찾아낸 것인지 아니면 그 테스트의 단정이 스스로 틀린 것인지를 도구가
  자동으로 가릴 수 없다. 논문은 그 판별을 시도하는 대신 실패를 통째로 버리는 쪽을 골랐다.
  그 대가로 남는 것이 무엇인지도 같은 자리에 적힌다 —
  `The effect of this filter is to preserve only tests that can be used for regression
  testing`.
- **셋째 관문의 판정 규칙이 숫자로 못박혀 있다** (§2, p.2):[^alshahwan2024-testgen-llm]

  > The filter uses the simple, widely-used and effective approach of repeated execution
  > [10, 28]; a test that does not pass on every one of five executions is deemed flaky.

- **넷째 관문의 이유는 "개선을 주장할 수 있는가"다** (§2, p.2):[^alshahwan2024-testgen-llm]
  두 관문을 지난 테스트는 회귀 신호로는 믿을 만하지만 기존 테스트의 동작을 되풀이하는
  것일 수 있고, 그러면 `there will be no meaningful way in which TestGen-LLM could reliably
  claim that the original test class had been improved in some measurable way`. 그래서
  커버리지를 늘리지 않는 것을 버린다.
- **비회귀는 필터가 아니라 구조가 보장한다** (§2.1.2, p.3):[^alshahwan2024-testgen-llm]
  도구는 기존 테스트 클래스에 **케이스를 더하기만** 하고 기존 케이스를 전부 남기므로 회귀가
  `by construction` 없다.
- **뒤에 관문이 하나 더 붙었다** (§5, p.8):[^alshahwan2024-testgen-llm] 같은 프롬프트에서
  이름만 다른 거의 같은 테스트가 반복 생성되는 것을 관찰하고, 나중 판본에 **이미 본 테스트를
  제거하는 필터**를 더했다. 유사도가 "전부 아니면 전무"라 본문의 구문 일치 검사로 충분했다고
  적는다.
- **관문을 다 지난 것이 사람에게 간다.** 마지막은 언제나 사람이다 — 도구는 추천 시스템이고
  코드베이스에 무엇이 들어갈지의 최종 결정권은 엔지니어에게 있다고 적는다
  (§2.1.4, p.3).[^alshahwan2024-testgen-llm]

## 필터는 LLM이 아니다

**호출자 지지의 핵심이 이 절이다.** 관문 넷 중 어느 것도 모델의 판단이 아니다.

- 빌드·실행·반복 실행·커버리지는 전부 **앱의 기존 CI 인프라**가 답한다 — 빌드 시스템,
  테스트 러너, 그리고 커버리지 계측기 Jacoco다 (각주 3, p.6).[^alshahwan2024-testgen-llm]
- 논문이 이 구도를 환각 대책으로 명시한다 (§2.1.4, p.3):[^alshahwan2024-testgen-llm]

  > The TestGen-LLM approach in particular (and the overall Assured LLMSE approach more
  > generally), overcomes hallucination by providing automated verifiable guarantees about
  > the semantic properties of the code it recommends.

- **ACH의 도해가 같은 구획을 도형으로 그린다** (Figure 1 캡션,
  p.3):[^foster2025-ach] `Solid rectangles denote components that are fully automated but
  entirely rule-based (and therefore do not use LLMs).` 곧 **LLM이 하는 자리와 규칙이 하는
  자리가 도해 수준에서 갈려 있다.**
- **다만 ACH는 그 경계를 한 칸 넘는다.** 등가 뮤턴트 판정만은 LLM 심판(LLM-as-judge)이
  맡는다 (§2, p.3).[^foster2025-ach] 그 심판이 얼마나 맞히는지가 아래
  [따로 잰 절](#등가-뮤턴트를-판정하는-llm-심판)이다. **판정자가 모델로 바뀌는 순간 그
  판정의 정밀도·재현율을 재야 한다는 것을, 이 논문이 스스로 보인 셈이다.**
- **ACH가 내거는 보장 다섯 중 앞의 셋만 불리언이다** (§2, p.2):[^foster2025-ach] 빌드됨 ·
  유효한 회귀 테스트(통과하고 불안정하지 않음) · 경화(기존 어느 테스트도 잡지 못하는 결함을
  잡음)가 `unequivocal guarantees`이고, 관심사 관련성과 스타일 추종은
  `more aspirational and probabilistic`이라 **코드 리뷰로 판단할 몫**이라고 적는다.

## 관문마다 얼마나 남는가

**단위가 테스트 클래스다 — 케이스가 아니다.** 아래는 Instagram의 Reels·Stories 컴포넌트
86개(Stories 31 + Reels 55)를 대상으로 프롬프트 넷과 LLM 둘을 돌린 평가 실험의 결과이고,
각 값은 **적어도 한 개의 새 테스트 케이스가 그 관문을 지난 테스트 클래스의 비율**이다
(§3.3, p.6).[^alshahwan2024-testgen-llm]

| 어디까지 지났나 | 테스트 클래스 비율 (분모 86) |
|---|---|
| 빌드된다 | 75% |
| 빌드되고 안정적으로 통과한다 | 57% |
| 빌드·통과에 더해 줄 커버리지를 늘린다 | 25% |

- **논문이 놀란 자리가 마지막 낙차다** (§3.3, p.6):[^alshahwan2024-testgen-llm]

  > It was particularly striking that, although 57% of test classes have a test that builds
  > correctly and passes reliably, only 25% of classes had a test that builds reliably,
  > passes non-flakily and adds additional line coverage.

- **케이스 단위로 내려가면 값이 한 자릿수 아래로 떨어진다.** 배포에서 잰 **시도(trial)당**
  성공률 — 시도 하나 = 새 테스트 케이스 하나를 만들려는 시도이고, 성공 = 빌드·통과·커버리지
  증가를 모두 만족 — 은 Facebook 490/8,996 = 0.05, Instagram 831/23,535 = 0.04이다
  (Table 3, p.7).[^alshahwan2024-testgen-llm] 논문 스스로 각주 4(p.6)에서 클래스당 성공률과
  케이스당 성공률이 다르다고 적는다.
- **모델을 갈아도 자릿수가 바뀌지 않는다** (Table 5, p.8):[^alshahwan2024-testgen-llm]
  `LLM1` 163/3,173 = 0.05, `LLM2` 1,157/28,654 = 0.04. 온도도 마찬가지여서 기본값 0.0에서
  1,215/30,483 = 0.04이다 (Table 4, p.8). **다만 시행 수가 극단적으로 불균형해서 비교로
  읽을 수 없다** — 논문이 그 이유를 스스로 적는다 (§4, p.8): 배포 모드에서는 테스트가
  누적되며 커버리지를 채워 가므로 **시행을 많이 받은 설정일수록 불리하다.**
- **프롬프트는 겹치지 않고 각자 다른 테스트를 찾는다** (§3.3, p.6):[^alshahwan2024-testgen-llm]
  `LLM2`에서 프롬프트 넷이 모두 자기만 찾은 테스트를 냈다(`extend_coverage` 5개,
  `statement_to_complete`·`extend_test` 각 2개, `corner_cases` 1개). `LLM1`에서는 셋만 그랬다.
  이것이 여러 모델·프롬프트를 앙상블로 묶는 설계의 근거다.

## 배포에서 사람이 수용한 비율

**아래는 배포 전체 집계이고, 서론이나 초록이 아니라 §4 결과 절의 값이다.**

- **적용 대비 개선 비율** (§4, p.7):[^alshahwan2024-testgen-llm] 세 차례 test-a-thon에 걸쳐
  테스트 클래스 **1,979개**에 도구를 돌려 **196개**를 개선했다 — 논문의 표현으로
  `approximately 10%`다.
- **엔지니어 수용률** (§4, p.7):[^alshahwan2024-testgen-llm]

  > Over all, 73% of TestGen-LLM test improvements were accepted by developers.

- **개별 배포의 원값**(분모가 diff 수다).[^alshahwan2024-testgen-llm]

  | 배포 | 분모 | 수용 | 거절·폐기 | 미검토 | 철회 |
  |---|---|---|---|---|---|
  | 첫 Instagram test-a-thon (§3.2.1, p.5) | 17 | 16 | 1 | — | — |
  | 12월 Instagram (§3.4, p.7) | 42 | 36 | 4 | — | 2 |
  | 12월 Facebook (§3.4.1, p.7) | 280 | 144 | 64 | 61 | 11 |

  Facebook 쪽은 논문이 두 비율을 함께 적는다 — 제출된 diff의 50% 초과가 수용됐고,
  **검토를 실제로 받은 것만 분모로 하면 거의 70%**다 (§3.4.1, p.7). 곧 **분모를 무엇으로
  잡느냐가 20%p 가까이 값을 바꾼다.**
- **사람과 견준 자리도 있다** (Table 1, p.5).[^alshahwan2024-testgen-llm] 첫 test-a-thon에서
  엔지니어 36명이 단위 테스트 diff 105건을 랜딩했고 그중 16건이 도구 산이다. 랜딩한 테스트
  개수 순위에서 도구는 **6위**였다. 다만 같은 절이 단서를 붙인다 — 도구가 커버한 줄 수
  1,460줄 중 1,326줄이 **테스트 케이스 단 하나**에서 나왔고, 도구가 만든 테스트 하나가
  더한 줄 수의 중앙값은 **2.5줄**이다 (§3.2.1, p.5). **평균이 아니라 중앙값이 이 도구의
  전형적 기여다.**

## 필터를 통과한 것도 사람이 거른다

**필터가 무엇을 못 보는지가 거절 사유 목록에 그대로 적혀 있다.**

- **거절 사유** (§3.4, p.7):[^alshahwan2024-testgen-llm] 12월 Instagram에서 거절된 4건의
  이유는 (1) 게터처럼 사소한 대상에 테스트를 만듦, (2) 테스트 케이스 하나에 책임 하나
  원칙을 어김(2건), (3) 단정(assertion)이 없음이다. 철회된 2건은 **커버리지는 늘었지만
  커버된 파일이 중요하지 않았다.**
- **첫 배포에서 버려진 1건도 같은 부류다** (§3.2.1, p.5):[^alshahwan2024-testgen-llm]
  모델이 단정 자리에 `TODO` 주석을 남긴 테스트였다. 그 테스트는 **커버리지를 실제로
  늘렸다** — 전에 실행된 적 없는 메서드를 실행했기 때문이다. 곧 **네 관문을 전부
  통과하고도 단정이 없었다.**
- **그래서 커버리지 관문은 단정의 존재를 보증하지 않는다.** 논문이 그 테스트의 값어치를
  따로 논한다 (§5, p.9):[^alshahwan2024-testgen-llm] 단정이 없어도 `implicit oracle`
  (코드가 예외를 던지지 않아야 한다)로 값을 낼 수 있고, 사람이 단정을 채워 넣을 시작점이
  된다. **하지만 그 판단은 사람이 했다.**
- **스타일도 거절 사유다** (§4.2, p.6):[^foster2025-ach] ACH 쪽에서도 폐기된 API를 쓰는 등
  부적절한 스타일로 쓰인 테스트가 거절됐고, 이것이 앞 논문에서도 관찰된 것이라고 적는다.
- **모델은 기존 코드의 스타일을 매우 충실히 따른다** (§7, p.10):[^alshahwan2024-testgen-llm]
  엔지니어들이 이 점을 매우 긍정적으로 평가했다. 그러나 같은 성질이 **폐기된 관행까지
  이어받게 만든다** — 논문은 이것을 `LLMs are dedicated followers of fashion`이라 부르고,
  재훈련이 비싸므로 프롬프트·린터 필터·정적 분석 후처리로 다루겠다고 적는다.

## 후속 시스템 — 결함을 먼저 만들고 그 결함을 잡는다

**ACH는 마지막 관문의 조건을 커버리지에서 결함 검출로 바꾼다.**

- **핵심 착상** (§1, p.1):[^foster2025-ach]

  > our key insight is to construct mutants that denote faults that are both relevant to
  > the issue of concern and also currently not caught (unkilled) by any existing test
  > case, and to use these as prompts to LLM-based test generation.

  여기서 뮤턴트(mutant)는 **일부러 심은 결함**이고, 뮤테이션 테스팅(mutation testing)은
  그런 결함을 심어 스위트가 그것을 잡는지 보는 기법이다.
- **파이프라인은 에이전트 셋이다** (§2, Figure 1과 Table 1,
  p.3):[^foster2025-ach] ① 관심사 요약을 받아 **결함을 만드는** 에이전트, ② 그 뮤턴트가
  원본과 등가인지 판정하는 **등가 탐지** 에이전트, ③ 그 뮤턴트에서는 실패하고 원본에서는
  통과하는 **테스트를 만드는** 에이전트. **셋째 단계의 뒤쪽 절반이 TestGen-LLM의 필터
  체인을 약간 고쳐 그대로 쓴 것**이라고 Figure 1 캡션이 점선으로 표시해 적는다.
- **입력은 자연어다.** 관심사는 개발 중 발견된 과거 결함·사용자 요구·시스템 제약·조직
  안에서 제기된 우려·규제 요구 중 무엇이든 될 수 있고 (§2, p.2),[^foster2025-ach] 이
  논문이 실제로 쓴 것은 **개발 중 발견된 과거 개인정보 결함**이다.
- **관문 통과의 층이 셋이다** (Table 2, p.5).[^foster2025-ach] 분모가 층마다 다르다.

  | 층 | 값 |
  |---|---|
  | 대상 클래스 | 10,795 |
  | 생성된 뮤턴트 총수 | 31,677 |
  | 그중 빌드되고 통과하는 것 | 9,095 (29%) |
  | 그중 등가가 아니라고 판정된 것 | 4,660 (51%) |
  | 그중 구문이 원본과 동일한 것 | 2,246 (25%) |

  같은 표의 나머지 둘은 에이전트가 등가라고 본 것 1,016(11%)과 답을 내지 않은 것
  1,173(13%)이다. **클래스 하나에서 빌드·통과하는 뮤턴트를 하나 찾으면 그 클래스의 작업이
  끝나므로**, 후보 뮤턴트 수는 대상 클래스 수를 넘지 않는다 (§3, p.4).
- **최종 산출** (Table 8, p.9):[^foster2025-ach] 비등가 뮤턴트 4,660개에서 **571개의
  테스트**가 나왔다. 뮤턴트를 죽인 테스트가 있는 클래스는 전체의 **5.3%**이고, 뮤턴트
  사살률은 **12%**(에이전트 판정 기준)다. 같은 표가 사람 판정 등가 비율로 보정한 `likely
  actual` 값 15%를 병기하는데, **그쪽은 추정치**다.
- **초기 시험의 수용률은 높았다** (§4.1과 Table 3, p.5):[^foster2025-ach] 테스트 30건을
  diff로 제출해 23건이 그대로, 4건이 간단한 수정 뒤 수용됐고 2건이 거절, 1건이 미검토였다
  — 제출 대비 **90%**(30건 중 27건), 검토된 것 대비 **93%**(29건 중 27건)다.
- **본 배포의 수용률은 앞 논문과 같은 자리에 떨어졌다** (§4.2와 Table 4,
  pp.5–6):[^foster2025-ach] WhatsApp·Messenger test-a-thon에서 **유용성 기준으로 검토된
  테스트 191건 중 140건 수용(73%)·51건 거절(27%)**이다. 논문이 그 값을 앞 논문과 견준다 —
  `This is very similar to acceptance rates from previous test-a-thons that focused
  exclusively on elevating coverage [3]`.
- **팀에 따라 크게 갈린다** (Table 4, p.6):[^foster2025-ach] WhatsApp은 91건 중 50건 수용
  (56%), Messenger 두 단계 합은 90%다. 논문은 이것을 팀 문화 차이로 읽으면서, 랜딩 결정이
  본래 주관적 판단이라고 적는다 (§4.2, p.6).
- **관심사 적중률은 3분의 1이다** (Table 4, p.6):[^foster2025-ach] 관련성 기준으로 검토된
  175건을 엔지니어가 리커트 5점으로 매긴 결과 5점 9%·4점 27%·3점 7%·2점 20%·1점 37%이고,
  논문은 상위 둘을 합친 **36%**를 개인정보 관련으로 센다. **수용률(73%)이 관련성(36%)의
  두 배라는 것이 이 논문의 관찰이다** — 엔지니어는 자기 관심사와 무관해도 다른 이유로
  유용하면 받아들인다 (§4.2, p.5).

## 등가 뮤턴트를 판정하는 LLM 심판

**여기가 두 논문 중 유일하게 LLM이 판정자 자리에 앉는 곳이고, 그래서 정밀도·재현율이
따로 측정된다.**

- **왜 필요한가** (§5, p.6):[^foster2025-ach] 뮤턴트는 구문이 달라도 의미가 같을 수 있고
  (등가 뮤턴트), 프로그램 등가 판정은 결정 불가능하다. 등가 뮤턴트를 죽이려 드는 것은
  낭비다.
- **바탕 진리는 사람이 만들었다** (§5.2, p.6):[^foster2025-ach] 뮤턴트가 가장 많은 네
  플랫폼에서 각 100개씩을 노려 표본을 뽑아 **총 381개**를 사람이 분석했다. 그중 실제 등가는
  **137개(36%)**이고, 에이전트가 등가라고 주장한 것은 **66개(17%)**다 (Table 5, p.8).
- **정밀도·재현율은 판정 규칙마다 다르다** (Table 6, p.8).[^foster2025-ach] **규칙을 붙이지
  않은 단일 쌍은 이 논문의 값이 아니다.**

  | 판정 규칙 | TP | FP | TN | FN | 정밀도 | 재현율 |
  |---|---|---|---|---|---|---|
  | `unsure`를 세지 않음 | 56 | 2 | 205 | 72 | 0.97 | 0.44 |
  | `unsure`를 등가로 셈 | 65 | 17 | 205 | 72 | 0.79 | 0.47 |
  | 구문 동일까지 등가로 셈 | 161 | 17 | 205 | 72 | 0.90 | 0.69 |
  | 더해 붙인 주석을 지운 뒤 동일한 것까지 셈 | 183 | 9 | 251 | 8 | 0.95 | 0.96 |

- **이 값들을 어떻게 읽어야 하는지를 논문이 스스로 적는다** (§5.3,
  p.7):[^foster2025-ach]

  > However, we cannot claim that these surprisingly good results arise because the mutant
  > equivalence detector agent is excellent at determining program equivalence. Rather,
  > they are more reflection of the kind of mutants the detector needs to judge for
  > equivalence.

  곧 **높은 값은 심판이 똑똑해서가 아니라 문제가 쉬워서**다 — 생성 에이전트가 만드는
  뮤턴트가 명백히 의미를 바꾸거나 명백히 등가인 쪽으로 갈리기 때문이다.
- **가장 큰 개선은 LLM이 아니라 전처리에서 왔다.** 마지막 행의 0.95/0.96은 **주석만 덧붙인
  뮤턴트를 규칙으로 걸러 낸 뒤**의 값이다. 문제의 뮤턴트는 실행 코드를 전혀 바꾸지 않고
  `// Introduce a bug by not checking if the user is inactivated before resetting their
  custom reactions` 같은 주석만 넣은 것인데, 언어 모델이 실행 코드와 주석을 구분하지 않아
  심판을 속인다 (§5.2, p.7).[^foster2025-ach]
- **어느 쪽 오류가 더 비싼지도 명시된다** (§5.3, p.7):[^foster2025-ach] 정밀도가 낮으면
  비등가 뮤턴트를 버려 **거기서 나왔을 테스트를 잃고**, 재현율이 낮으면 계산 자원만
  낭비된다. 그래서 이 용도에서는 정밀도가 더 중요하다.

## 커버리지 관문이 버렸을 테스트

**앞 논문의 넷째 관문이 무엇을 놓치는지를 뒤 논문이 수치로 잰다.**

- **결과** (§6과 Table 8, pp.8–9):[^foster2025-ach] ACH가 만든 테스트 571개 중 **277개
  (49%)가 줄 커버리지를 늘리지 않는다.** 그 테스트들은 기존 어느 테스트도 잡지 못하는 결함을
  잡는데도 그렇다.

  > As Table 8 shows, a large proportion (49%) of test cases that uniquely additionally
  > kill a mutant, do not also add line coverage. Clearly, these tests have value, since
  > they catch faults that would otherwise go undetected. However, if we were to judge test
  > cases solely on the basis of the coverage they add, then such valuable test cases would
  > be wrongly discarded.

- **반대 방향도 잰다** (§6과 Table 8, pp.8–9):[^foster2025-ach] 같은 표에서 TestGen-LLM은
  **더 많은 클래스에 테스트를 만들지만(32% 대 5.3%) 뮤턴트는 훨씬 적게 죽인다.** 사살률은
  에이전트 판정 기준으로 2.0% 대 12%, 사람 판정으로 보정한 `likely actual` 기준으로
  2.4% 대 15%이고 §6 산문은 뒤쪽 쌍을 쓴다. 논문의 결론 문장은 이렇다 — `targeting
  mutants can also elevate coverage, but targeting coverage will be inadequate to kill
  mutants`.
- **이 대비의 성격을 정확히 보라.** 두 도구는 목표가 다르고 분모도 다르다. 이 KB는 이 값을
  "ACH가 더 낫다"로 읽지 않고, **관문의 마지막 조건을 무엇으로 두느냐가 통과하는 테스트의
  종류를 바꾼다**는 뜻으로만 읽는다.
- **원래 이 방향은 앞 논문이 예고한 자리다** (§7, p.10):[^alshahwan2024-testgen-llm]
  TestGen-LLM은 줄 커버리지가 개선의 **편의적 대리물**(`merely an expedient proxy`)이며
  뮤테이션 커버리지가 아마 가장 나은 기준이겠지만 그 규모에서 돌리기가 계산적으로 힘들다고
  적었다. 뒤 논문은 **뮤턴트를 적게, 대신 관심사에 맞춰** 만드는 것으로 그 벽을 돌아간다.
- **"대리물이지 목표가 아니다"는 이 배선보다 훨씬 오래된 구분이다.**
  [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md)가 1999년에
  같은 구분을 세운다 — 커버리지는 테스트 설계의 약점을 가리키는 **단서**이고, 그것을 목표
  수치로 걸면 스위트가 그 수치를 향해 최적화되어 도구가 정보원이기를 그만둔다는 논증이다.
  **여기 두 논문의 차이가 그 구분의 실물이다**: 관문의 조건으로 쓰는 것과 목표로 삼는 것이
  다르고, 조건을 무엇으로 두느냐가 통과하는 테스트의 종류를 바꾼다.

## 두 논문의 관계

- **같은 팀의 후속이다.** Mark Harman·Inna Harper·Shubho Sengupta 셋이 두 논문의 저자
  목록에 함께 있고, ACH는 TestGen-LLM을 참고문헌 [3]으로 인용하며 자기 파이프라인의 뒤쪽
  절반이 그 도구의 변형이라고 적는다 (Figure 1 캡션, p.3).[^foster2025-ach]
- **같은 상위 개념 아래 놓인다.** 둘 다 자기 워크플로를 **Assured LLM-based Software
  Engineering**의 사례로 규정하고, 그 개념의 출처로 같은 기조 발표 논문을 든다
  (TestGen-LLM §1 p.1의 [6], ACH §2 p.2의 [7] — 둘 다 Alshahwan, Harman, Marginean,
  Sengupta & Wang 2024, *Assured LLM-Based Software Engineering*, ICSE InteNSE 워크숍
  기조).[^alshahwan2024-testgen-llm] ACH도 같은 기조 논문을 자기 원리의 출처로 든다
  (§2, p.2).[^foster2025-ach] **이 KB는 그것을 확보하지 않았으므로 이름만 적는다.**
- **연속과 단절이 한 줄씩이다.** 연속은 필터 체인이고, 단절은 마지막 관문이다 —
  ACH는 자기 앞 작업이 `based on the sole objective of increasing coverage, which meant it
  could not target specific classes of faults`였다고 적는다 (§7, p.10).[^foster2025-ach]
- **둘 다 오라클 문제를 풀지 않았다.** ACH가 그것을 미해결 문제로 적는다 (§8,
  p.10):[^foster2025-ach] 이 접근은 현재 판본을 회귀 오라클로 쓰므로 **미래의 회귀를 막을
  뿐 지금 코드에 이미 있는 결함은 찾지 못한다.** 그러려면 오라클 문제를 풀어야 한다고
  적고, 기존 오라클 추론 연구는 오검출로 엔지니어의 시간을 낭비하지 않을 만큼의 정밀도가
  아직 아니라고 덧붙인다.

## 이 KB의 읽기: 수용의 조건은 필터에 적혀 있다

- **"LLM이 만든 것이니 사람이 본다"는 절차는 이 두 배포에서 최종 단계이지 첫 단계가
  아니다.** 사람 앞에 오기까지 결정적 검사 넷을 지나고, 그 검사들은 모델의 판단이 아니라
  빌드·실행·커버리지 계측이라는 **기존 인프라의 답**이다. 곧 **독립 검증자의 자리를 도구가
  차지하고 있고**, 이것이
  [검증자 독립성](../synthesis/verifier-independence.md)이 요구하는 구도의 산업 실물이다.
- **필터가 무엇을 못 보는지가 거절 사유에 남는다.** 네 관문을 다 지나고도 단정 없는 테스트,
  사소한 대상의 테스트, 폐기된 API를 쓴 테스트가 사람 손에서 걸렸다. **게이트를 세우면 그것이
  못 보는 것이 그 자리에 남는다**는 명제의 실물이고, 두 논문 모두 그 잔여를 사람 리뷰에
  맡긴다고 명시한다.
- **필터 체인은 [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md)가
  잰 결함 층과 정확히 대응한다.** 거기서 구문·컴파일 층은 기계 게이트로 걸러지고 **오라클
  층은 남는다**고 적었다. TestGen-LLM의 관문 1~2가 앞 층을 맡고, 실패한 테스트를 전부 버리는
  선택이 **오라클 층을 회피한다** — 잘못된 단정을 가려내는 대신 실패를 통째로 버린다.
  그래서 남는 것은 회귀 테스트뿐이고, 이것은 회피이지 해결이 아니다.
- **그 회피의 대가가 [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md)이다.**
  첫 실행에서 통과하는 테스트만 남기면 **기대값은 대상의 지금 동작에서 온다.** 두 논문 다
  이것을 감추지 않는다 — TestGen-LLM은 남는 것이 회귀 테스트뿐이라고 적고, ACH는 현재 판본을
  회귀 오라클로 쓴다고 §8에서 명시한다. **곧 이 산업 배포가 실증한 것은 "생성된 테스트가
  의도를 포착한다"가 아니라 "의도 포착을 포기하면 자동화가 성립한다"이다.**
- **수용률 73%를 인용할 때 붙는 것.** (1) 분모가 **검토를 받은 diff**인지 **제출된 diff**
  인지(Facebook 사례에서 50%와 70%로 갈린다), (2) 어느 팀인지(WhatsApp 56% 대 Messenger
  90%), (3) 수용이 **관심사 적중을 뜻하지 않는다**는 것(ACH에서 수용 73%, 관련성 36%).
- **이 수치들은 Meta 규모를 전제한다.** 후보마다 빌드·다섯 번 실행·커버리지 측정을 돌리고
  성공률 4%로도 이득이 나는 것은 그 인프라가 이미 있고 대상 코드가 수천만 줄이기 때문이다.
  **작은 조직으로 그대로 옮기면 분자와 분모가 함께 무너진다** — 이 페이지는 그 전이를
  주장하지 않는다.

## 두 소스의 사각

- **초록과 결과 절이 어긋난다.** TestGen-LLM 초록은 `improved 11.5% of all classes`인데
  §1 기여 목록과 §4 결과 절은 같은 대상을 `10%`(196/1,979)로 적고 그 차이를 설명하지 않는다
  (초록 p.1 대 §4, p.7).[^alshahwan2024-testgen-llm] 이 페이지는 결과 절 값을 썼다.
- **ACH의 §5.3 산문과 Table 5가 어긋난다.** 산문은 `61% of all equivalent mutants are almost
  trivially equivalent, because they contain only a single ‘misleading’ comment`라 적는데,
  Table 5의 오해 소지 주석 항목은 381개 중 93개(24%)이고 사람 판정 등가는 137개다 — 93/137은
  61%가 아니라 약 68%다 (§5.3과 Table 5, pp.7–8).[^foster2025-ach] 어느 쪽이 분모인지 논문이
  밝히지 않아 이 페이지는 **그 비율을 옮기지 않았다.**
- **두 논문 다 자기 필터의 오검출률을 재지 않는다.** 버려진 후보 중 실제로는 좋은 테스트가
  얼마나 있었는지(특히 첫 실행에서 실패해 버려진 것 중 **진짜 결함을 찾은 것**의 비율)를
  두 논문 어느 쪽도 세지 않는다. 관문 2의 설계 근거는 오라클이 없다는 것이지, 버린 것이
  적다는 실측이 아니다.
- **불안정 판정의 임계 다섯 회에 근거가 없다.** `a test that does not pass on every one of
  five executions is deemed flaky`는 `simple, widely-used and effective`라는 말과 참고문헌
  둘로만 뒷받침되고, 다섯 번이 몇 번의 오판을 남기는지는 재지 않는다
  (§2, p.2).[^alshahwan2024-testgen-llm]
- **모델의 정체가 없다.** TestGen-LLM은 `LLM1`·`LLM2`가 상업적으로 민감하다며 아무것도
  밝히지 않는다 (각주 1, p.1).[^alshahwan2024-testgen-llm] **모델 판과 설정을 밝히라는
  [보고 규범](../concepts/llm-empirical-study-reporting-norms.md)의 요구가 여기서 지켜지지
  않는다.** ACH는 Llama 3.1 70B라고 밝히지만 (§2, p.2)[^foster2025-ach] 프롬프트 셋 외의
  설정은 적지 않는다.
- **배포 모드의 값에 교란이 있다고 논문이 스스로 적는다** (§4, p.8):[^alshahwan2024-testgen-llm]
  테스트가 누적되며 커버리지를 채워 가므로 나중 시행일수록 성공하기 어렵고, 시행 수가 많은
  설정이 불리하다. 그래서 Table 4~6의 설정 간 비교는 성립하지 않는다.
- **test-a-thon은 평상시가 아니다.** TestGen-LLM 스스로 첫 배포를 `we cannot claim that this
  was a perfect example of diff time deployment`라 적는다 — test-a-thon이라 테스트에 대한
  관심이 평소보다 높았다는 것이다 (§3.2, p.5).[^alshahwan2024-testgen-llm] ACH의 두
  test-a-thon도 같은 성격이고, 리뷰어는 각 6명이다 — WhatsApp 쪽은 6명 전원이 개인정보
  공학과 소프트웨어 테스팅 배경을 가졌고, Messenger 쪽은 테스팅에는 강한 전문성이 있으나
  개인정보 공학은 **적어도 기초 경험** 수준이라고 적힌다 (§4.2,
  pp.4–5).[^foster2025-ach]
- **ACH의 Messenger 1단계는 사전 선별된 표본이다** (§4.2, p.5):[^foster2025-ach] 60개 중
  10개를 널 포인터 예외 관련이라며 뺐고, 그 선별이 틀렸다고 판단해 2단계에서 폐기했다.
  Table 4가 두 단계를 따로 싣는 이유다.
- **언어와 플랫폼이 하나다.** 둘 다 코틀린·안드로이드이고, 다른 언어·다른 스택으로의 전이는
  두 논문 어느 쪽도 재지 않았다.
- **뮤테이션 테스팅 자체의 지위는 이 페이지 밖이다.** ACH가 뮤테이션 적합성 기준이 구조적
  기준을 능가한다며 드는 근거는 남의 문헌이고 (§2·§6),[^foster2025-ach] 이 KB는 그 문헌을
  확보하지 않았다. **뮤테이션 점수의 타당성 논쟁은 여기서 다루지 않는다.**

## 이어지는 페이지

- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  이 필터 체인이 걸러 내려는 결함이 실험실에서 어떻게 분포하는가. 그쪽의 "기계가 고칠 수
  있는 층과 없는 층"이 이 페이지의 관문 1~2와 관문 2의 회피에 대응한다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 첫 실행에서
  통과하는 테스트만 남기는 선택이 도달하는 자리. 기대값이 대상의 지금 동작에서 올 때 무엇이
  남고 무엇이 사라지는가
- [테스트 오라클](../concepts/test-oracle.md) — 두 논문이 우회한 문제의 지도. TestGen-LLM이
  §2에서 인용하는 오라클 조사 논문이 그 페이지의 원전이다
- [검증자 독립성](../synthesis/verifier-independence.md) — 판정자가 생성자와 갈려 있어야
  한다는 요구. 이 페이지의 필터가 그 요구의 결정적 구현이고, ACH의 등가 판정 에이전트가 그
  경계를 한 칸 넘은 자리다
- [LLM 실증 연구의 보고 규범](../concepts/llm-empirical-study-reporting-norms.md) — 모델
  판·실행 시점·설정을 밝히라는 요구. TestGen-LLM이 모델 정체를 밝히지 않는 것이 그 요구에
  걸린다
- [에이전트의 테스트 케이스 착취](../concepts/test-case-exploitation-by-agents.md) — 테스트를
  모델의 권한 안에 두면 무슨 일이 일어나는가. 이 페이지의 배포는 반대 구도다 — 모델이 테스트를
  만들되 통과 판정은 손대지 못한다
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 커버리지를
  관문이나 목표로 걸었을 때 무슨 일이 생기는가의 실무 규범 원전. 이 페이지의 넷째 관문과
  그 관문이 버렸을 49%가 그 논증이 배선에서 실현된 자리다
- [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md) — 관문의 마지막 조건을
  무엇으로 두느냐가 왜 문제가 되는지의 실험실 판. 거기서도 커버리지와 뮤테이션은 틀린 표본을
  잡아내는 경험적 기준 위에 더 얹을 것이 적었다
- [벤치마크의 수명과 철회](../concepts/benchmark-lifespan-and-retirement.md) — 자동 채점을
  제대로 만들기 어렵다는 같은 문제의 벤치마크 쪽. 좁아지지도 넓어지지도 않아야 한다는 두
  조건이, 이 페이지의 관문 넷이 지나고도 남아 사람 리뷰로 넘어가는 자리와 겹친다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  관문을 다 지난 테스트가 통과한다는 사실이 무엇을 증명하지 않는가의 상한
- [자기 수리의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md) — 모델이 자기
  출력을 고칠 때 무엇이 병목인가. 이 페이지의 필터는 그 피드백을 사람이 아니라 인프라에서
  받는다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 이 페이지가 우회한 문제의 허브
- [벤치마크와 수용 판정의 무결성](../synthesis/benchmark-and-acceptance-integrity.md) —
  이 갈래의 허브

[^alshahwan2024-testgen-llm]: Alshahwan, Chheda, Finegenova, Gokkaya, Harman, Harper,
    Marginean, Sengupta & Wang 2024, "Automated Unit Test Improvement using Large Language
    Models at Meta". 확보본은 arXiv:2402.09171 **v1**(2024-02-14) 12쪽이다. 1쪽 ACM
    Reference Format이 `FSE ’24`를 인쇄하지만 `Companion`·산업 트랙 표기는 문면에 없다 —
    **FSE 2024 Companion 게재와 DOI는 대장·ACM DL 레코드 근거이고 문면 근거가 아니다.**
    쪽 표기는 확보본 PDF 쪽(1~12)이다. 이 페이지가 담은 것은 §1~§5·§7과 Table 1·3·4·5, 각주
    1·3·4다. §2.1.3(앙상블 논거)·§2.1.5(토큰 창)·§6 관련 연구·§8 결론과 참고문헌(pp.11~12)은
    읽었으나 claim으로 옮기지 않았고, Table 2(프롬프트 템플릿 넷)와 Table 6(플랫폼×모델
    교차)은 본문이 요약하는 것만 담았다. Figure 1·2는 도형 안 이름표가 흩어져 읽히므로
    본문 산문이 적는 값만 썼다. 표는 다단 조판이라 `pdftotext -layout` 정렬본과 대조했다.
    **초록의 `11.5%`는 §4 결과 절의 `10%`와 어긋나 옮기지 않았다.** §6이 인용하는 제3자
    수치(Siddiq·Schäfer·Nie·Yuan)도 옮기지 않았다.

[^foster2025-ach]: Foster, Gulati, Harman, Harper, Mao, Ritchey, Robert & Sengupta 2025,
    "Mutation-Guided LLM-based Test Generation at Meta". 확보본은 arXiv:2501.12862 **v1**
    (2025-01-22) 12쪽이고 1쪽에 `FSE Companion ’25, 23 – 27, 2025, Trondheim, Norway`가
    인쇄돼 있다. 다만 같은 블록의 저작권 연도(`© 2024`)와 인쇄된 DOI
    (`10.1145/3663529.3663839` — 이 KB가 TestGen-LLM에 배정한 것과 같은 문자열)는 앞
    논문의 템플릿이 갱신되지 않은 흔적이다. **이 페이지가 쓰는 DOI와 쪽수는 대장·레코드
    근거이고 문면 근거가 아니며, camera-ready 문면 대조는 수행되지 않았다.** 쪽 표기는
    확보본 PDF 쪽(1~12)이다. 이 페이지가 담은 것은 §1~§8과 Table 1·2·3·4·5·6·8, 각주 3·4다.
    Table 7(플랫폼별 정밀도·재현율)은 Table 6의 총계로 갈음했고, §7 관련 연구와
    참고문헌(pp.10~12)은 읽었으나 옮기지 않았다. Figure 1(파이프라인 도해)·Figure 2(리커트
    지시문 캡처)는 본문 산문이 적는 것만 썼다. 표가 다단 조판이라 값은 전부
    `pdftotext -layout` 정렬본과 대조했다. **§5.3 산문의 `61%`는 Table 5와 맞지 않아
    옮기지 않았고**, §3·§7이 인용하는 제3자 수치(규칙 기반 등가 뮤턴트 10~15%, Copilot 수용률
    약 30%, Tian의 F1 35%)도 옮기지 않았다. 두 논문이 공통으로 드는 *Assured LLM-Based
    Software Engineering*(Alshahwan et al. 2024, ICSE InteNSE 기조)은 이 KB가 확보하지
    않았으므로 이름만 적었다.

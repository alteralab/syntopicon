---
type: concept
title: 현재 동작을 오라클로 쓴다는 것
description: 기대값을 코드의 지금 동작에서 길어 올릴 때 무엇이 남고 무엇이 사라지는가 — LLM 이전에 이미 세워져 있던 실증 셋. 명세 없이 생성된 단정은 의도가 아니라 관측을 적는다는 기제, 커버리지는 크게 오르는데 결함 발견은 오르지 않았다는 97명 통제실험, 도구가 준 시작점에 사람이 머문다는 관찰, 리팩터링의 안전망 명제를 42명에게 걸었더니 더 빠르지도 더 좋지도 않았다는 통제실험, 그리고 코드를 되비추기만 하는 테스트에 붙은 이름과 그 해악 서술
generated: { by: "claude-opus-5", at: "2026-08-23T14:00:00Z" }
sources:
  - { id: fraser2015-user-study, resource: /it/sources/fraser2015-user-study.md }
  - { id: vonken2012-refactoring, resource: /it/sources/vonken2012-refactoring.md }
  - { id: winters2020-swe-at-google, resource: /it/sources/winters2020-swe-at-google.md }
  - { id: eagle2015-change-detector, resource: /it/sources/eagle2015-change-detector.md }
---

# 현재 동작을 오라클로 쓴다는 것

- [이 묶음이 답하는 질문](#이-묶음이-답하는-질문)
- [근거의 격 — 심사 실증 둘과 규범 글 하나](#근거의-격--심사-실증-둘과-규범-글-하나)
- [기제 — 생성된 단정은 관측된 동작이다](#기제--생성된-단정은-관측된-동작이다)
- [커버리지는 오르고 결함 발견은 오르지 않았다](#커버리지는-오르고-결함-발견은-오르지-않았다)
- [의도 포착 — 초기 실험의 결론과 재현 실험의 철회](#의도-포착--초기-실험의-결론과-재현-실험의-철회)
- [도구가 준 시작점에 사람이 머문다](#도구가-준-시작점에-사람이-머문다)
- [안전망 명제의 통제실험 — 리팩터링에 테스트가 있을 때](#안전망-명제의-통제실험--리팩터링에-테스트가-있을-때)
- [이름이 붙은 자리 — 변경 감지 테스트](#이름이-붙은-자리--변경-감지-테스트)
- [이 묶음이 지지하는 것과 지지하지 않는 것](#이-묶음이-지지하는-것과-지지하지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **기대값을 코드의 지금 동작에서 길어 올릴 때, 그 테스트는 무엇을 지키고
무엇을 지키지 못하는가.**

## 이 묶음이 답하는 질문

[테스트 오라클](../concepts/test-oracle.md) §5.3은 회귀 테스트를 **이전 판본을 오라클로
쓰는 것**으로 규정한다. 이전 판본 대신 **지금 판본**을 오라클로 쓰면 그것은 회귀조차
아니게 된다 — 기대값과 대상이 같은 정보에서 나오기 때문이다. 이 페이지는 그 퇴화가
실제로 무엇을 낳는지를 **LLM 이전의 실증 셋**으로 세운다.

세 소스는 같은 질문의 다른 층을 잡는다.

| 소스 | 잡는 층 | 방법 |
|---|---|---|
| Fraser et al. | 기계가 관측에서 단정(assertion)을 뽑을 때 | 사람 피험자 97명 통제실험 2회 |
| Vonken & Zaidman | 사람이 쓴 테스트를 리팩터링 담보로 쓸 때 | 사람 피험자 42명 통제실험 |
| Eagle (구글) | 사람이 코드를 되비추는 테스트를 쓸 때 | 규범 서술 (측정 없음) |

## 근거의 격 — 심사 실증 둘과 규범 글 하나

**같은 페이지에 있다고 같은 무게가 아니다.**

- **Fraser et al.와 Vonken & Zaidman은 `peer-reviewed`다.** 심사를 거친 사람 피험자
  통제실험이고, 이 페이지는 **그 논문들이 스스로 잰 값만** 인용한다. 두 논문이 관련
  연구 절에서 전하는 제3자 수치는 옮기지 않았다.
- **구글 글은 `industry-norm`이다.** 측정도 표본도 없는 사내 회람물(Testing on the
  Toilet)의 블로그판이고, 이 페이지가 그로부터 가져오는 것은 **이름과 정의와 규범
  서술뿐이다.** 어떤 수치 주장도 이 글에 기대지 않는다. 규모 전제 — 구글 코드베이스와
  사내 리뷰 문화 — 를 글 자신이 밝히지 않으므로, 다른 규모로 옮길 때 무엇이 남는지도
  이 글은 답하지 않는다.
- **이 묶음이 받은 하중.** "현재 동작을 기대값으로 굳히는 것이 위험하다"는 주장을 이
  KB에서 앞서 지탱하던 것은 **미심사 상태의, 단일 모델 하나로 돌린 보고**였다. 그
  보고 자신이 이 문제를 자동 생성 전반의 고전적 한계로 규정했으므로, 하중은 그 고전
  쪽 — 곧 이 묶음 — 으로 옮긴다. 이 페이지는 그 하중을 받는 자리이고, 옮겨진 결과로
  이 주장은 **미심사 단일 보고가 아니라 심사 통제실험 둘**에 서게 된다.

## 기제 — 생성된 단정은 관측된 동작이다

- **명세가 없으면 생성기는 의도가 아니라 관측을 적는다** (§2.1).[^fraser2015-user-study]

  > As EVOSUITE assumes no specification, these assertions reflect the *observed*
  > behaviour rather than the *intended* behaviour.

- **그래서 대상이 이미 틀려 있으면 단정도 틀린 채로 태어난다** — 논문은 실험 설계를
  설명하며 이 귀결을 그대로 적는다 (§1).[^fraser2015-user-study]

  > EVOSUITE automatically produces JUnit test suites that target branch coverage, and
  > these unit tests contain assertions that reflect the current behaviour of the class.
  > Consequently, if the current behaviour is faulty, the assertions reflecting the
  > incorrect behaviour must be corrected.

  **이 문장이 이 페이지 전체의 축이다.** 생성된 단정의 옳음은 대상의 옳음에 기생하고,
  그 기생을 끊는 유일한 절차는 **사람이 단정을 고치는 것**이다. 뒤따르는 실측은 전부
  "사람이 실제로 그 고침을 해내는가"를 잰 것이다.
- **논문은 단정의 용도를 안내판으로 규정한다** — 생성된 단정의 목적은 각 입력에 대해
  프로그램 상태의 어느 국면이 결함을 드러낼 수 있는지를 테스터에게 **가리키는** 것이고,
  거기서 옳은 단정이 (바라건대) 유도될 수 있다 (§2.1).[^fraser2015-user-study] 안내판을
  정답으로 읽는 순간 그것은 오라클이 아니라 현재 동작의 사본이 된다.
- **이 기제가 EvoSuite 하나의 성질이 아니라는 것도 논문이 적는다** — 불변식 추론,
  파라미터화 단정, 구체 단정 생성이라는 세 계열이 있고 어느 쪽이 나은지 학계의 합의가
  없으며 산업에서는 셋 다 드물게 쓰인다. 그러나 **셋 모두 사용자가 생성된 오라클을
  고치도록 요구한다**는 점은 공통이다 (§2.1).[^fraser2015-user-study]

## 커버리지는 오르고 결함 발견은 오르지 않았다

**실험 설계** — 자바 클래스 한 개에 MAJOR로 만든 뮤턴트 5개를 심어 결함으로 쓰고,
피험자에게 한 시간 동안 JUnit 스위트를 만들게 했다. 한 집단은 손으로만, 다른 집단은
EvoSuite 결과에서 출발했다. 초기 실험은 피험자 49명·클래스 3종, 재현 실험은 48명·
클래스 4종이며 두 실험 합계 피험자 97명·데이터점 145개다
(§2.2).[^fraser2015-user-study]

- **커버리지는 크게 올랐다** (§3.1 결론 상자).[^fraser2015-user-study]

  > **RQ1:** *Automatically generated test suites achieve higher structural coverage than
  > manually created test suites.*

- **그 "크게"의 실제 범위는 하나의 수가 아니라 구간이다** (§3.1).[^fraser2015-user-study]

  > The relative increases in median coverage range from 9.4% in the case of branch
  > coverage for *Rational*, to 300%—a threefold increase—for branch coverage for *Option*.

  **단위는 중앙값의 상대 증가율(%)**이고, 분모는 같은 클래스를 손으로 테스트한 집단의
  중앙값이다. 집계 단위는 클래스별·커버리지 지표별이며, 자리는 초기 실험 결과 절이다.
  **"+300%"를 단독으로 인용하면 상한만 적는 것이 되어 과장이 된다** — 아래 클래스가
  9.4%였다.
  - 같은 절이 밝히는 셋째 클래스는 **감소**다. `DocType`의 중앙값 분기 커버리지 상대
    변화는 -42.12%였고, 논문은 그 원인을 EvoSuite Eclipse 플러그인의 클래스패스 설정
    오류로 지목한다 (§3·§3.1).[^fraser2015-user-study] 그래서 위 9.4~300% 구간은
    `Option`·`Rational` 두 클래스에만 걸린다.
  - 재현 실험은 설정 오류를 고친 뒤 네 클래스에서 다시 쟀고, **평균 커버리지의 상대
    개선**으로 문장 6.6~156.3%, 분기 1.5~329.2%, 메서드 17.7~117.2%를 보고한다
    (§4.1).[^fraser2015-user-study] 단위는 평균의 상대 증가율(%), 분모는 같은 클래스
    수동 집단의 평균, 집계 단위는 클래스별·지표별이다.
- **결함 발견은 오르지 않았다** (§3.2·§4.2 결론 상자).[^fraser2015-user-study]

  > **RQ2:** *Using automatically generated test suites does not lead to detection of more
  > faults.*

  > **RQ2:** *The replication provides no new evidence that using automatically generated
  > test suites would lead to detection of more faults.*

- **통계 판정을 함께 적는다 — "차이 없음"이 아니라 "유의한 차이를 못 봄"이다.** 초기
  실험에서 세 클래스 어느 쪽도 유의수준 0.05에서 유의하지 않았고 가장 낮은 p 값이
  `Option`의 0.165였다. 논문은 같은 문단에서 **EvoSuite가 실제로 더 나쁘다고 주장하려면
  표본이 더 커야 한다**고 스스로 적는다 (§3.2).[^fraser2015-user-study] 재현 실험에서도
  가장 두드러진 `ArrayIntList`조차 표준화 효과 크기 0.64·p 값 0.122로 0.05에 못 미쳤다
  (§4.2).[^fraser2015-user-study] 검정은 Mann-Whitney U, 효과 크기는 Vargha-Delaney
  A12이며 자리는 표 III·IV다 (§3 머리·§4 머리).[^fraser2015-user-study]
- **못 찾은 결함이 스위트 밖에 있었던 것이 아니다** — 초기 실험에서 EvoSuite가 만든
  최초 스위트는 평균적으로 `Option` 3.0개, `Rational` 2.86개, `DocType` 2.6개의 결함을
  드러낼 **수 있었다**. 단위는 심어 둔 결함 5개 중 개수이고, 판정 기준은 "결함 있는
  판본은 통과하고 원본에서는 실패하는 테스트가 존재한다", 즉 **단정만 고치면 드러났을
  결함**이다 (§3.2).[^fraser2015-user-study] 재료는 있었고 고쳐지지 않았다.
- **회귀 능력의 대리 지표도 결론을 주지 못했다** (§3.4·§4.4 결론
  상자).[^fraser2015-user-study]

  > **RQ4:** *Automated test generation does not guarantee higher mutation scores.*

  > **RQ4:** *The replication shows gains in mutation scores, but suggests that assertion
  > generation needs to be improved.*

  재현 실험에서 뮤테이션 점수의 평균 차이는 어느 클래스에서도 크지 않았고(최대 27.9%
  상대 차이), p 값은 최소 0.101, 표준화 효과 크기는 최대 0.7이었다 — 둘 다 같은 클래스
  (`DocType`)에서 나온 값이다 (§4.4).[^fraser2015-user-study]
- **논문 자신의 결론 문장** (§9).[^fraser2015-user-study]

  > Our studies illustrate that this assumption does not appear to be true; merely
  > achieving high coverage does not necessarily improve our ability to test software.

- **같은 결론이 실무 규범 쪽에 먼저 적혀 있었다.** 1999년의 실무자 글
  [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md)는 커버리지를
  겨냥해 스위트를 설계하면 커버리지가 정보원이기를 그만둔다고 논증한다. **격이 다르다** —
  그쪽은 측정 없는 주장이고 이쪽은 통제실험이므로, 두 자리를 함께 인용할 때 수치의 근거는
  이 페이지가 지고 그쪽은 그 명제가 먼저 세워져 있었다는 계보로만 쓴다.

## 의도 포착 — 초기 실험의 결론과 재현 실험의 철회

**이 절은 두 실험이 갈린 자리이므로 한쪽만 인용하지 않는다.**

- **초기 실험의 결론 상자** (§3.3).[^fraser2015-user-study]

  > **RQ3:** *Automatically generated test cases have a negative effect on the ability to
  > capture intended class behaviour.*

- **그 상자를 뒷받침한 수치** (§3.3).[^fraser2015-user-study]

  > For *Option*, the number increases from 1.22 on average for manually written tests to
  > 8.5 for participants using EVOSUITE; for *Rational* the number increases from 2.8 to
  > 5.14; and for *DocType* the number increases from 0.75 to 2.5.

  **재는 것은 "원본에서 실패하는 테스트 수"의 피험자 평균**이다. 원본은 결함을 심지 않은
  옳은 판본이므로, 거기서 실패하는 테스트 하나는 **클래스가 어떻게 동작해야 하는지에
  대한 오해가 잘못된 단정으로 굳은 것**이다 — 논문이 그 자리에서 그렇게 규정한다. 단위는
  테스트 케이스 개수이고 분모는 없다(비율이 아니라 개수의 평균), 집계 단위는 클래스별
  최종 스위트다. 유의성은 `Option` p=0.001, `DocType` p=0.026에서 유의, `Rational`
  p=0.289는 비유의다 (§3.3).[^fraser2015-user-study]
- **그리고 그 수는 시간이 지나도 줄지 않았다** — 논문은 실패 테스트가 스위트가 진화하며
  교정되리라 예상했으나 Fig.3은 그렇지 않음을 보인다. EvoSuite 사용자와 수동 테스터
  모두에서 실패 테스트 수가 거의 일정하게 유지되었고 EvoSuite 쪽은 오히려 약간
  늘었다 (§3.3).[^fraser2015-user-study]
- **재현 실험은 이 결론을 유지하지 않았다** (§4.3 결론 상자).[^fraser2015-user-study]

  > **RQ3:** *In the replication automatically generated tests did not always have a
  > negative effect on the ability to capture intended class behaviour.*

  네 클래스 중 `DocType`·`ArrayIntList`는 두 집단의 평균이 실패 테스트 한 개 안쪽으로
  붙었고, `Rational`은 **방향이 뒤집혀** 수동 집단이 평균 9.5개, EvoSuite 집단이 5.1개로
  수동 쪽이 두 배가량 많았다(p=0.234로 비유의) (§4.3).[^fraser2015-user-study] 논문은
  같은 절에서 두 실험 중 어느 쪽이 잡음인지 판정할 수 없다고 적고, **초기 실험의
  결론을 "어떤 경우에는 그렇고 어떤 경우에는 관리 가능한 수준"으로 누그러뜨린다.**
- **그러므로 이 페이지는 "생성 테스트가 의도 포착을 악화시킨다"를 무조건 명제로 쓰지
  않는다.** 확장판이 정본이고, 확장판의 결론은 조건부다. 남는 것은 조건이 붙지 않은
  더 좁은 사실 — **생성된 스위트는 원본에서 실패하는 테스트를 안고 시작하며, 사람이 그
  실패를 다 교정하지는 않는다** — 쪽이다.

## 도구가 준 시작점에 사람이 머문다

- **논문의 관찰** (§5.1).[^fraser2015-user-study]

  > Based on this, we can clearly see that when using automatic test generation tools, the
  > starting point given to testers in the form of the test suite generated, is where they
  > tend to stay.

  같은 절은 이 성질을 **점착성(stickiness)**이라 부르고, 수동 작성에는 본래 존재하지
  않는 것이라 적으며 우려의 대상으로 규정한다. 나쁜 스위트조차 사람이 이해하는 데 시간을
  요구하고, 사람은 그것을 통째로 버리기를 꺼린다 (§5.1).[^fraser2015-user-study]
- **되비추는 테스트일수록 효과가 낮았다는 상관도 같은 절에 있다** — 생성 스위트 쪽에서
  최종 스위트 크기와 결함 발견의 Spearman 순위 상관은 0.45, **사람이 새로 만든 테스트
  수**는 0.72, **손대지 않은 채 남은 EvoSuite 테스트 수**는 -0.50이었고, 분기 커버리지와
  결함 발견의 상관은 -0.21로 약했다. 수동 집단에서는 분기 커버리지와 스위트 크기 둘 다
  결함 발견과 0.79로 강하게 붙었다 (§5.1).[^fraser2015-user-study] 단위는 Spearman 순위
  상관계수이고 집계 단위는 피험자별 최종 스위트다.
  - **이 다섯 값은 §5.1 본문에만 있다.** 논문은 같은 문단에서 표 V를 가리키지만 표 V의
    행은 단정 수(MA)와 테스트 수(NT)뿐이라 이 값들이 표에 그대로 실려 있지는 않다. 문단
    자체가 초기 실험 `Rational` 데이터(Fig.6) 논의 안에 있으나 **논문이 그 범위를 다시
    적지는 않았다** — 그래서 이 페이지는 이 값들을 클래스 전체의 법칙으로 옮기지 않는다.
- **생성된 단정은 수가 많다** — 수동 집단은 테스트당 평균 1.44~1.68개의 단정을 썼고
  EvoSuite 유래 스위트는 1.41~4.9개였다. `Option`·`Rational`에서는 테스터가 자기가
  쓰던 것보다 2~3배 많은 단정을 검사해야 했다 (§5.2, Fig.8).[^fraser2015-user-study]
  퇴장 설문에서 피험자들은 단정이 좋다고 여기면서도 **너무 많다**고 자주 말했다
  (§5.2).[^fraser2015-user-study] 확인해야 할 단정이 많다는 것은 사람이 오라클을
  교정하는 절차의 비용이고, 위 점착성과 같은 방향으로 작동한다.

## 안전망 명제의 통제실험 — 리팩터링에 테스트가 있을 때

**현재 동작을 고정하는 테스트의 존재 이유는 대개 "리팩터링의 안전망"이다.** 그 명제를
직접 실험에 건 것이 이 논문이다.

- **설계** — 두 집단 통제실험. 실험군은 단위 테스트가 딸린 코드를, 대조군은 테스트 없는
  같은 코드를 받아 **리팩터링 과제 7개**를 수행한다. 과제는 Counsell 등의 분류(호환·후방
  호환·후방 호환 가능·비호환) 네 범주에서 뽑았고, 대상은 JPacman(도메인 클래스 27개·약
  3,000줄, 테스트 약 1,000줄·테스트 케이스 60개)이다. 피험자는 최종 학년 학부생 35명과
  현업 개발자 7명, 합계 **42명**이다 (§III-A~§III-E).[^vonken2012-refactoring]
- **잰 것은 둘이다** — 과제별 소요 시간, 그리고 리팩터링된 **생산 코드**의 품질을 과제별
  채점 모형으로 0~10점으로 매긴 점수다. 독립 변수는 단위 테스트의 가용성 하나다
  (§III-F).[^vonken2012-refactoring] 채점의 주관성은 저자 둘이 7건을 독립 채점해
  일치도를 확인했다(70점 만점 합계에서 총 차이 1.2점) (§V-C).[^vonken2012-refactoring]
- **시간 결과** — 과제 일곱 개 중 **개별 과제에서는 어느 것도 유의하지 않았다**(p는
  0.099~0.714). 유의한 것은 전체 합계 하나뿐이고(p=0.028), 방향은 **테스트를 가진 쪽이
  더 오래 걸림**이다: 합계 평균 1시간 56분 19초 대 1시간 34분 5초 (표
  II).[^vonken2012-refactoring] 검정은 Mann-Whitney U, 집계 단위는 피험자별 과제
  소요 시간이다.
- **품질 결과** — 일곱 과제 중 **세 번째 과제 하나만** 유의했고(8.0점 대 5.7점, p=0.027),
  합계 평균은 8.3점 대 8.0점으로 유의하지 않았다(p=0.480). 42명 전체의 일곱 과제 평균은
  10점 만점에 8.1점(최소 5.1, 최대 9.9)이다 (표 V, §IV-B).[^vonken2012-refactoring]
  **단위는 0~10점 채점 모형 점수**이고 분모는 과제당 만점 10, 집계 단위는 피험자별 과제
  점수다.
  - 유의했던 세 번째 과제의 방향은 **테스트 쪽이 좋음**이고, 저자는 그 이유를 테스트
    클래스가 밀어 내릴 메서드를 간접 호출하고 있어 참가자를 옳은 클래스로 유도했을
    가능성으로 설명한다 (§IV-B).[^vonken2012-refactoring] 즉 이 한 건은 안전망이 아니라
    **길잡이**로 작동한 사례다.
- **초록과 §V의 세기가 다르다 — 둘 다 적는다.** 초록은 이렇게 단정한다
  (초록).[^vonken2012-refactoring]

  > Results indicate that having unit tests available during refactoring does not lead to
  > quicker refactoring or to higher-quality code after refactoring.

  그러나 본문 §V-A는 두 귀무가설 어느 쪽도 기각도 채택도 못 한다고 적는다 — H10에 대해
  *"we can neither reject or accept our first null hypothesis"*, H20에 대해 *"can neither
  be accepted or rejected"*.[^vonken2012-refactoring] **그러므로 이 소스는 "테스트가 돕지
  않는다는 증명"이 아니라 "돕는다는 증거를 찾지 못했다"로만 인용한다.**
- **논문이 이론으로 지목한 대상이 무엇인지도 문면에 있다** (§V-B).[^vonken2012-refactoring]

  > While theory explains how unit testing makes refactoring easier, e.g., Feathers [25],
  > we could not observe this in our experiment, neither in a quicker refactoring process,
  > nor in higher quality of code.

  참고문헌 [25]는 Feathers, *Working Effectively with Legacy Code*(Prentice Hall, 2004)다
  (참고문헌 목록).[^vonken2012-refactoring] **이 페이지가 그 책의 용도 한정에 쓰이는
  근거가 이 문장이다.** 그 책이 세운 절차와 그 절차의 경계는
  [특성화 테스트](../concepts/characterization-test.md)가 담는다 — 그쪽이 이 절을 자기
  caveat의 근거로 인용하며, **인용의 세기는 이 절이 정한다**: 이 논문은 "돕지 않는다는
  증명"이 아니라 "돕는다는 증거를 관측하지 못했다"까지만 말한다.
- **저자 자신이 적은 한계를 같은 무게로 읽는다** (§V-A·§V-C).[^vonken2012-refactoring]
  ⑴ 대상 JPacman은 산업 시스템보다 작다. ⑵ **새로 만든 코드에 테스트를 추가하라고
  요구하지 않았다** — 기존 테스트를 통과 상태로 유지하는 것만 요구했고, 저자는 그 지시가
  결과를 눌렀을 수 있다고 적는다. ⑶ 표본이 작다. ⑷ 리팩터링 전후로 테스트를 돌린
  피험자가 90%를 넘어 "돌리기"의 효과를 잰 가설 넷(H30·H40·H70·H80)은 **비교군이 만들어
  지지 않아 검정 자체가 불가능했다** (§IV-A).
- **저자가 남긴 반대 방향의 관찰도 함께 적는다** — 복잡한 리팩터링일수록 테스트의 피드백이
  작업을 떠받치는 조짐이 보였다고 §V-A·§VI가 적는다. 일곱 번째 과제(Extract Subclass)의
  품질 점수는 7.5점 대 5.8점으로 테스트 쪽이 높았으나 p=0.056으로 0.05에 못 미쳤다
  (§IV-B, 표 V).[^vonken2012-refactoring]

## 이름이 붙은 자리 — 변경 감지 테스트

**이 절의 근거 등급은 위 둘과 다르다.** 아래 인용은 측정이 아니라 구글의 규범 서술이다.

- **정의** — 코드 아래의 정보를 그대로 옮겨 놓은 테스트에 붙은 이름이 **변경 감지 테스트
  (change-detector test)**다 (본문 4문단).[^eagle2015-change-detector]

  > This is a change-detector test—it is a transformation of the same information in the
  > code under test—and it breaks in response to any change to the production code, without
  > verifying correct behavior of either the original or modified production code.

  두 성질이 한 문장에 있다: **생산 코드가 바뀌면 무조건 깨진다**는 것과 **원본이든
  수정본이든 옳은 동작을 검증하지 않는다**는 것.
- **왜 검증이 되지 않는가** — 글은 극단적인 예(테스트가 소스 파일의 각 줄을 문자열로
  비교하는 것)를 먼저 놓고 그것을 체크섬에 빗댄 뒤 이렇게 적는다
  (본문 3문단, 첫째 코드 예시 바로 뒤).[^eagle2015-change-detector]

  > A correct or incorrect program is equally likely to pass a test that is a derivative of
  > the code under test.

  **옳은 프로그램과 그른 프로그램이 같은 확률로 통과한다면 그 테스트는 판별력이 0이다.**
  이것이 "현재 동작을 오라클로 쓴다"의 극한이고, 위 Fraser의 기제 — 단정이 관측을 적는다
  — 와 같은 자리를 가리킨다.
- **해악 서술** (규범 판단이다).[^eagle2015-change-detector]

  > Change detectors provide negative value, since the tests do not catch any defects, and
  > the added maintenance cost slows down development. These tests should be re-written or
  > deleted.

  **"negative value"는 측정된 값이 아니라 저자의 판단이다.** 이 페이지는 이 문장을
  실증으로 쓰지 않고, **실무 규범이 같은 방향을 가리킨다는 사실**로만 쓴다.
- **글이 드는 두 번째 예는 목(mock) 호출 순서 검증이다** — `Processor`가 두 부품의
  `process`를 차례로 부르는지 목으로 확인하는 테스트를 두고, 글은 그것이 첫 번째 극단적
  예와 얼마나 다르냐고 되묻는다 (둘째 코드 예시와 본문 4문단).[^eagle2015-change-detector]
  되비추기가 문자열 비교라는
  극단만이 아니라 **상호작용 검증이라는 흔한 형태로도 나타난다**는 것이 이 예의 요지다.
  본문의 코드 두 조각은 실행 가능한 언어가 아니라 의사코드라 이 페이지에 펜스로 옮기지
  않았다.
- **같은 이름이 5년 뒤 같은 회사의 책에도 나온다** (13장 §"Prefer State Testing Over
  Interaction Testing").[^winters2020-swe-at-google] 상호작용 검증을 과하게 쓴 테스트를
  사내에서 농담처럼 `change-detector tests`라 부른다고 적고, 이유를 **동작이 그대로여도
  프로덕션 코드가 바뀌면 실패하기 때문**으로 든다. 문면과 자리는
  [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md)에
  있다. **위 두 번째 예(목 호출 순서 검증)가 그 책에서 조문이 된 셈이다** — 그쪽은 상태
  검증을 먼저 쓰고 상호작용 검증은 호출 횟수나 순서 자체가 동작일 때로 미루라고 적는다.

## 이 묶음이 지지하는 것과 지지하지 않는 것

**호출자가 이 페이지를 인용할 때 넘지 말아야 할 선을 여기 적는다.**

지지하는 것:

- **기제** — 명세가 없으면 자동 생성된 단정은 의도가 아니라 **관측된 현재 동작**을
  적는다. 대상이 틀려 있으면 단정도 틀린 채 태어나고, 그것을 바로잡는 절차는 사람뿐이다
  (§1·§2.1).[^fraser2015-user-study]
- **커버리지와 결함 발견이 갈린다** — 생성 도구는 설계된 일(구조 커버리지)을 크게
  개선하지만, 그 개선이 사람이 결함을 더 찾는 것으로 이어지지 않았다. 두 실험 모두에서
  결함 발견 차이는 유의수준 0.05에서 유의하지 않았다
  (§3.1·§3.2·§4.1·§4.2).[^fraser2015-user-study]
- **사람이 교정을 다 하지는 않는다** — 생성된 스위트는 원본에서 실패하는 테스트를 안고
  시작하고, 초기 실험에서 그 수는 한 시간 동안 줄지 않았다 (§3.3,
  Fig.3).[^fraser2015-user-study] 시작점의 점착성이 같은 관찰의 다른 얼굴이다
  (§5.1).[^fraser2015-user-study]
- **"테스트가 있으면 리팩터링이 안전하고 빠르다"는 명제는 통제실험에서 확인되지 않았다** —
  42명 실험에서 시간도 품질도 테스트 쪽의 이득으로 나타나지 않았고, 유의했던 유일한 시간
  결과는 오히려 테스트 쪽이 더 오래 걸린 것이었다 (표 II·표
  V).[^vonken2012-refactoring]
- **되비추기만 하는 테스트를 실무 규범이 별도로 이름 붙여 배격한다** — `change-detector
  test`라는 이름과 "다시 쓰거나 지우라"는 처방이 존재한다
  (본문 4·5문단).[^eagle2015-change-detector]

**지지하지 않는 것 — 이 선을 넘겨 인용하지 않는다:**

- **"자동 생성 테스트가 해롭다"는 이 묶음의 실증에 없다.** Fraser의 결론은 "돕는다는
  가정이 참으로 보이지 않는다"이지 "해롭다"가 아니다 (§9).[^fraser2015-user-study]
  결함 발견에서 유의한 열세는 관측되지 않았고, 논문은 **더 나쁘다고 주장하려면 표본이
  더 필요하다**고 스스로 적는다 (§3.2).[^fraser2015-user-study] "해롭다"에 해당하는
  문장은 구글 글에만 있고 그것은 규범이지 측정이 아니다.
- **"의도 포착을 악화시킨다"를 무조건 명제로 쓰지 않는다.** 그 결론 상자는 초기
  실험(§3.3)의 것이고 재현 실험(§4.3)이 조건부로 되돌렸다.
- **Vonken을 "테스트가 리팩터링을 돕지 않는다는 증명"으로 쓰지 않는다.** 저자 자신이 두
  귀무가설 모두 기각도 채택도 못 한다고 적었다 (§V-A).[^vonken2012-refactoring]
- **세 소스 중 어느 것도 LLM이 만든 테스트를 재지 않았다.** 2015년 이전의 도구와 사람이
  대상이다. 이 묶음이 LLM 세대에 대해 하는 일은 **기제의 선재를 보이는 것**이지 지금
  모델의 성능을 말하는 것이 아니다.
- **어느 소스도 결함 발견률의 절대 수치를 다른 맥락으로 옮길 근거를 주지 않는다.**
  Fraser의 대상은 한 시간 안에 테스트할 수 있게 고른 작은 자바 클래스 네 개이고
  (§2.2·§2.5), Vonken의 대상은 약 3,000줄의 교육용 프로그램 하나다
  (§III-B).[^vonken2012-refactoring]

**그럼에도 이 퇴화를 설계로 택한 산업 배포가 있다.** Meta의 두 도구는 첫 실행에서 통과하지
않는 생성 테스트를 전부 버리는데, 그러면 남는 것은 정의상 **지금 동작을 기대값으로 삼은
테스트**뿐이다. 두 논문 다 그것을 감추지 않고 회귀 테스트라고 부르며, 뒤 논문은 이 방식이
미래의 회귀만 막고 **지금 코드에 이미 있는 결함은 찾지 못한다**고 미해결 문제로 적는다 —
[생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md)이 그 관문과
대가를 담는다. 이 페이지가 재는 것은 그 선택의 **비용**이고, 그쪽은 그 선택의 **이득**이다.

## 이어지는 페이지

- [테스트 오라클](../concepts/test-oracle.md) — 이 축의 개념 정본. §5.3의 "이전 판본을
  오라클로 쓴다"가 이 페이지가 다루는 퇴화형의 정상형이고, 네 출처 분류에서 여기 다루는
  것은 파생 오라클 갈래다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 이 페이지가
  퇴화라 부르는 것을 산업 배포가 설계로 택했을 때의 관문과 통과율. 첫 실행에서 통과하는
  것만 남기는 필터가 기대값을 대상의 지금 동작에 묶는다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  같은 기제가 LLM 생성물에서 어떻게 나타나는지의 실측. 이 페이지가 LLM 이전의 층을
  맡는다
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 커버리지가
  올라도 스위트가 나아졌다는 뜻이 아니라는 명제의 실무 규범 층. 이 페이지의 RQ1과 RQ2가
  갈린 자리를 그쪽은 측정 없이 먼저 주장했다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  통과가 무엇을 증명하지 않는가의 상한. 되비추는 테스트는 그 상한 아래에서도 더 적게
  증명한다
- [일관성 오라클 휴리스틱](../concepts/consistency-oracle-heuristics.md) — 명세가 없을 때
  기대를 무엇에 비추는가의 실무 카탈로그. "이전 판본과의 일관성"이 그 목록의 한 항목이다
- [특성화 테스트](../concepts/characterization-test.md) — **이 페이지가 재는 대상을
  처방한 실무 규범.** 형제 관계다: 그쪽이 정의·절차·용도 한정을 담고, 이 페이지가 그
  처방의 전제를 잰 실증을 담는다. 그쪽 페이지의 caveat 두 자리(안전망 명제의 통제실험,
  변경 감지 테스트)가 이 페이지의 두 절을 가리킨다
- [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md) — 같은 절차가
  코드가 아니라 데이터에 걸리는 자리. 기대를 적은 스키마를 이미 지나간 배치들에서 추론하므로
  기대의 출처가 명세가 아니라 대상 자신이고, **과적합한 스키마**가 여기서 말하는 "관측을
  의도로 오해하기"의 데이터판이다. 그쪽은 그 위험을 스스로 짚고 사람의 승인을 절차에 넣는다
- [자기 테스트 코드](../concepts/self-testing-code.md) — 기대값을 사람이 짓는 자리와 그 절차
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) —
  같은 회사의 책이 `change-detector` 라는 이름을 다시 쓰면서 상호작용 검증을 언제만 쓸지
  조문으로 적은 자리
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 이 축의 허브

[^fraser2015-user-study]: Fraser, Staats, McMinn, Arcuri & Padberg 2015, "Does Automated
    Unit Test Generation Really Help Software Testers? A Controlled Empirical Study",
    *ACM Transactions on Software Engineering and Methodology*. **확보본은 저자 수용본이라
    러닝 푸터의 권·호·쪽이 자리표시자(`Vol. V, No. N, Article A`)이므로 이 페이지의
    locator는 절 번호와 표·그림 번호로만 적었다** — 권·호·쪽수가 필요하면 DOI
    10.1145/2699688의 서지 레코드가 근거이고, 이 KB는 그 레코드를 열지 않았다.
    이 페이지는 초록·§1 Introduction·§2 Study Design(2.1–2.5)·§3 Results: Initial
    Study(3.1–3.4)·§4 Results: Replication Study(4.1–4.4)·§5 Discussion(5.1–5.2)·§8
    Related Work·§9 Conclusions를 담았다. §6(설문)·§7(향후 과제 논의)·부록 A(주입 뮤턴트
    목록)는 옮기지 않았다. §1의 동기 수치(Sjoberg·Buse)와 §8이 전하는 제3자 실측
    (Staats et al.·Ramler et al.)은 이 논문이 잰 값이 아니므로 인용하지 않았다. 표
    III·IV는 다단 수치 표라 기계 추출이 열을 섞으므로, 본문 산문이 같은 값을 진술하는
    자리에서만 값을 옮겼다. Fig.2·4·5·8은 점마다 값이 인쇄돼 있지 않아 본문이 진술한
    평균·중앙값·구간만 담았다.
[^vonken2012-refactoring]: Vonken & Zaidman 2012, "Refactoring with Unit Testing: A Match
    Made in Heaven?", Working Conference on Reverse Engineering (WCRE). **확보본 1쪽에
    학회명·연도·쪽수 줄이 인쇄돼 있지 않은 저자본이라 쪽수를 locator로 쓰지 않고 절
    번호와 표 번호로만 적었다** — 게재 쪽수는 리포지토리 레코드가 근거이고 이 KB는
    그것을 확인하지 않았다. 이 페이지는 초록·§I Introduction·§III Experimental
    Design(A–G)·§IV Results(A–B, 표 II·III·V·VI·VII)·§V Discussion(A–C)·§VI Conclusion·
    참고문헌 [25]를 담았다. §II Related Work가 전하는 제3자 수치(George & Williams,
    Williams et al.)는 이 논문이 잰 값이 아니므로 인용하지 않았다. 표 IV·VIII(학생 대
    현업 비교)은 이 페이지의 질문 밖이라 옮기지 않았다. 2단 조판이라 표의 열 머리와
    값이 기계 추출에서 섞이므로, 값은 본문 산문이 같은 수를 진술하는 자리에서 확인해
    옮겼다.
[^eagle2015-change-detector]: Eagle 2015, "Testing on the Toilet: Change-Detector Tests
    Considered Harmful", *Google Testing Blog*, 2015년 1월 27일 게시. **아카이브가 아니라
    라이브 페이지를 2026-08-20T17:26Z에 받은 스냅샷이다.** **절도 쪽도 없는 짧은 글이라
    locator는 본문 문단 번호로 적었다** — 게시물 본문은 산문 다섯 문단과 코드 예시 둘로
    이루어져 있고, 세는 단위는 게시일·저자·출처 안내 줄을 뺀 산문 문단이다(1문단
    리팩터링 상황, 2문단 기계적 작성, 첫째 코드 예시, 3문단 체크섬 비유, 둘째 코드 예시,
    4문단 변경 감지 테스트 정의, 5문단 해악 서술). 측정·표본이 없는 규범 글
    (사내 회람물 Testing on the Toilet의 블로그판)이므로 이 페이지는 정의와 규범 서술만
    인용하고 수치 주장의 근거로 쓰지 않는다. 확보본에 함께 담긴 독자 댓글 2건은 저자의
    글이 아니므로 인용하지 않았고, 본문의 의사코드 두 조각은 실행 가능한 언어가 아니라
    펜스로 옮기지 않았다. 원문이 거는 인쇄용 TotT 원본(Google Docs)은 확보하지 않았다.
[^winters2020-swe-at-google]: Winters, Manshreck & Wright(큐레이터) 2020,
    *Software Engineering at Google*, abseil.io 공개판(CC BY-NC-ND 4.0), 2026-08-23
    열람본, 13장 `Test Doubles`(저자 Andrew Trenk·Dillon Bly) §"Prefer State Testing Over
    Interaction Testing". **공개판 HTML에 쪽 번호가 없어 locator는 장 번호와 원문 절
    제목이다.** 이 페이지는 이 책에서 `change-detector`라는 이름이 다시 쓰인다는 사실만
    옮긴다 — 근거 등급은 `industry-norm`이고 측정이 아니다.

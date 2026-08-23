---
type: concept
status: draft
title: 커버리지 신호는 스위트 크기가 만든다
description: 큰 자바 프로그램 다섯 개에서 스위트 3만 1천 개를 만들어 커버리지와 결함 검출 효과성의 상관을 잰 자리 — 효과성을 뮤테이션 점수로 정의한 조건, 크기를 무시했을 때와 통제했을 때의 상관계수 대비와 프로젝트마다 갈리는 폭, 강한 커버리지 기준이 추가 정보를 주지 못한다는 결과와 그 항공 표준 함의, 저자들이 실무자 두 사람의 주장을 실증 층에서 받았다고 적은 자리, 종속변수를 실제 버그로 바꾸면 답이 달라지는 대조, 원문이 스스로 그은 선, 그리고 같은 학회 같은 해에 반대 답을 낸 논문이 있다는 사실
generated: { by: "claude-opus-5", at: "2026-08-23T02:00:00Z" }
contradicts: [coverage-predicts-mutation-kills]
sources:
  - { id: inozemtseva2014-coverage, resource: /it/sources/inozemtseva2014-coverage.md }
  - { id: kochhar2015-real-bugs, resource: /it/sources/kochhar2015-real-bugs.md }
  - { id: fowler2012-test-coverage, resource: /it/sources/fowler2012-test-coverage.md }
  - { id: zhao2026-llm-coverage-replication, resource: /it/sources/zhao2026-llm-coverage-replication.md }
---

# 커버리지 신호는 스위트 크기가 만든다

- [이 소스의 지위](#이-소스의-지위)
- [효과성을 무엇으로 쟀는가](#효과성을-무엇으로-쟀는가)
- [무엇을 대상으로 어떻게 쟀는가](#무엇을-대상으로-어떻게-쟀는가)
- [크기부터 확인한다](#크기부터-확인한다)
- [크기를 무시하면 상관이 보인다](#크기를-무시하면-상관이-보인다)
- [크기를 고정하면 상관이 내려앉는다](#크기를-고정하면-상관이-내려앉는다)
- [강한 커버리지 기준이 더 알려 주지 않는다](#강한-커버리지-기준이-더-알려-주지-않는다)
- [저자들이 내리는 처방](#저자들이-내리는-처방)
- [커버리지가 예측하는 것과 못 하는 것](#커버리지가-예측하는-것과-못-하는-것)
- [원문이 넘지 않은 선](#원문이-넘지-않은-선)
- [이 쌍이 정설이 아닌 이유](#이-쌍이-정설이-아닌-이유)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **커버리지 수치가 스위트의 결함 검출 효과성을 예측하는가, 아니면 커버리지가
높은 스위트가 단지 더 크기 때문에 그렇게 보이는가.**

## 이 소스의 지위

- **근거 등급은 `peer-reviewed`다.** 확보본 1쪽 저작권 상자가 게재를 문면으로 확인해
  준다 — `ICSE ’14, May 31–June 7, 2014, Hyderabad, India`.[^inozemtseva2014-coverage]
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 이 페이지는 2절이 요약하는 선행
  연구 열두 편의 수치를 옮기지 않는다. 그것은 이 논문이 경유해 전하는 제3자 값이다.
- **확보본에 쪽 번호가 인쇄돼 있지 않다.** locator는 확보본 PDF 쪽(1~11)이다.

## 효과성을 무엇으로 쟀는가

**이 페이지의 모든 결과가 이 정의 위에 서 있다. 정의를 떼면 결과가 다른 것을 뜻하게
된다.**

- **효과성 = 뮤테이션 점수(mutation score)다** (§3.3·§3.6, pp.3~5).[^inozemtseva2014-coverage]
  PIT가 만든 뮤턴트를 스위트가 얼마나 죽였는가이고, **실제 결함이 아니다.**
- **두 가지로 잰다** (§3.6, p.5).[^inozemtseva2014-coverage] **원시 효과성**(raw)은 죽인
  뮤턴트를 전체 비동등 뮤턴트로 나눈 것이고, **정규화 효과성**(normalized)은 죽인
  뮤턴트를 **그 스위트가 덮은** 비동등 뮤턴트로 나눈 것이다. 저자들이 둘의 뜻을 이렇게
  가른다.

  > It may be helpful to think of the normalized effectiveness measurement as a measure of
  > depth: how thoroughly does the test suite exercise the code that it runs? The raw
  > effectiveness measurement is a measure of breadth: how much code does the suite
  > exercise?

- **동등 뮤턴트를 가정으로 처리했다** (§3.3, pp.3~4).[^inozemtseva2014-coverage] 마스터
  스위트가 죽이지 못한 뮤턴트를 전부 동등으로 간주했고, 그 비율이 프로젝트마다
  **0.4%에서 35%까지**다 (Table 2 마지막 행, p.4). 저자들 자신이 6.1절에서 이것을 구성
  타당도 위협으로 적는다 — 그 뮤턴트들이 무작위 부분집합이 아닐 수 있고, 예컨대 개발자가
  경계값 오류를 자주 테스트하면 그 종류의 뮤턴트가 덜 동등으로 분류된다.
- **저자들이 실제 결함으로 다시 확인하는 것을 다음 과제로 적는다** (§7,
  p.10).[^inozemtseva2014-coverage] `Our next step is to confirm our findings using real
  faults to eliminate this threat to validity.`

## 무엇을 대상으로 어떻게 쟀는가

- 조건: 자바 오픈소스 다섯 개, 2014년, 효과성은 뮤테이션 점수.
- **대상**(Table 2, p.4):[^inozemtseva2014-coverage] Apache POI · Closure Compiler ·
  HSQLDB · JFreeChart · Joda Time. 총 자바 SLOC은 80,462(Joda Time)부터
  724,089(Closure)까지이고, 테스트 메서드 수는 628(HSQLDB)부터 7,947(Closure)까지다.
- **스위트 생성**(§3.4, p.4):[^inozemtseva2014-coverage] 마스터 스위트에서 테스트
  메서드를 비복원 무작위로 뽑아 크기 3·10·30·100 식으로 늘려 가며 **각 크기마다
  1,000개씩** 만들었고, 다섯 시스템 합계 **31,000개**다. 같은 프로젝트에서 크기가 같은
  스위트를 잔뜩 비교하는 이 설계가 **크기 통제의 수단**이다.
- **커버리지**(§3.5, pp.4~5):[^inozemtseva2014-coverage] CodeCover로 문장 커버리지
  (statement coverage)·결정 커버리지(decision coverage)·수정 조건 커버리지(modified
  condition coverage) 셋. 자바용 도구가 없어 데이터플로 커버리지는 재지 않았다.
- **상관 계수는 Kendall τ다** (§4.2 각주 9, p.5).[^inozemtseva2014-coverage] 선형성도 정규성도
  가정하지 않으려고 골랐다고 밝힌다. 세기의 말 표현은 Guildford 척도를 따른다 — 0.4 미만
  낮음, 0.4~0.7 중간, 0.7~0.9 높음, 0.9 초과 아주 높음 (§4.1 각주 7, p.5).

## 크기부터 확인한다

- **크기와 효과성의 상관이 먼저 확인된다** (§4.1, p.5).[^inozemtseva2014-coverage]
  정규화 효과성을 크기에 대해 회귀했을 때 조정 r²가 **0.26에서 0.97까지**이고, 저자들은
  이것이 상관계수 r **0.51에서 0.98**에 해당한다고 적는다 (Figure 2의 다섯 패널). 비정규화
  효과성 쪽은 r²가 **0.69에서 0.99**다.
  - 분모는 다섯 프로젝트이고 각 점은 같은 크기의 스위트 1,000개를 담은 상자다.
- **이것이 이 논문의 "온전성 검사"다.** 크기가 효과성과 이만큼 붙어 있으므로, **커버리지와
  효과성의 상관을 볼 때 크기를 빼놓고 보면 안 된다**는 것이 뒤 절들의 출발점이다.

## 크기를 무시하면 상관이 보인다

- **크기를 무시했을 때의 Kendall τ**(Table 3·4, p.6, 모두 99.9% 수준에서
  유의).[^inozemtseva2014-coverage]

  | 프로젝트 | 정규화 효과성(문장/결정/수정 조건) | 비정규화 효과성(문장/결정/수정 조건) |
  |---|---|---|
  | Apache POI | 0.75 / 0.76 / 0.77 | 0.94 / 0.94 / 0.94 |
  | Closure | 0.83 / 0.83 / 0.84 | 0.95 / 0.95 / 0.95 |
  | HSQLDB | −0.35 / −0.35 / −0.35 | 0.81 / 0.80 / 0.79 |
  | JFreeChart | 0.50 / 0.53 / 0.53 | 0.91 / 0.95 / 0.92 |
  | Joda Time | 0.80 / 0.80 / 0.80 | 0.85 / 0.85 / 0.85 |

- **HSQLDB가 예외다** (§4.2, pp.5~6).[^inozemtseva2014-coverage] 정규화 효과성에서 상관이
  **음수**다. 저자들의 해석은 커버리지가 높은 스위트일수록 **커버리지 단위당 죽이는
  뮤턴트가 적다**는 것 — 코드를 많이 실행하지만 그 코드 안의 뮤턴트는 별로 못 죽이는
  테스트가 들어 있다는 뜻이다.
- **이 단계의 답은 "상관이 있다"이다.** 저자들의 Answer 2는 HSQLDB를 뺀 나머지에서 중간
  내지 높은 상관이 있다고 적고, **그것이 크기 때문인지를 다음 질문으로 넘긴다.**

## 크기를 고정하면 상관이 내려앉는다

- **결과가 하나의 수로 요약되지 않는다** (§4.3, pp.6~8).[^inozemtseva2014-coverage] 저자들이
  프로젝트·크기·커버리지 종류·효과성 척도의 모든 조합으로 τ를 계산했고 본문에는 그
  범위만 적는다. **크기를 통제하면 상관은 언제나 내려갔고**, 내려간 폭은 효과성 척도에
  따라 달랐다 — 정규화 쪽은 낮은 상관으로, 비정규화 쪽은 중간 상관으로 갔다.
- **양 극단이 본문에 적혀 있다** (§4.3, p.8).[^inozemtseva2014-coverage]
  - **Joda Time**: 크기를 무시하면 0.80~0.85였던 상관이 크기를 통제하자 **사실상 0**이
    됐다. 정규화 효과성을 쓴 Closure도 같았다.
  - **Apache POI**: 비정규화 효과성과의 상관이 크기를 무시하면 0.94였고 크기를 통제하자
    **0.46에서 0.85 구간**으로 떨어졌다. 저자들은 이 구간이면 스위트 품질에 대해 쓸모 있는
    정보를 준다고 덧붙인다.
- **저자들의 답이 조건절을 달고 있다** (Answer 3, p.8):[^inozemtseva2014-coverage]

  > Our results suggest that, for large Java programs, the correlation between coverage and
  > effectiveness drops when suite size is controlled for. After this drop, the correlation
  > typically ranges from low to moderate, meaning it is not generally safe to assume that
  > effectiveness is correlated with coverage.

- **한 가지 관찰이 5절에 더 있다** (p.8).[^inozemtseva2014-coverage] 상관이 사실상 사라진
  Joda Time과 Closure가 다섯 중 **가장 크고 가장 충실한 스위트**를 가진 프로젝트였다.
  저자들은 이것이 **스위트가 좋아질수록 상관이 약해진다는 뜻일 수 있다**고 적는다.

## 강한 커버리지 기준이 더 알려 주지 않는다

- **커버리지 종류를 바꿔도 결과가 거의 같다** (§4.3, p.8).[^inozemtseva2014-coverage] 세
  종류의 점 구름 모양이 서로 닮았고, 종류끼리의 상관이 아주 높다 (Table 5, 전체
  프로젝트의 전체 스위트).

  | 커버리지 짝 | Kendall τ | Pearson |
  |---|---|---|
  | 문장/결정 | 0.92 | 0.99 |
  | 결정/수정 조건 | 0.91 | 0.98 |
  | 문장/수정 조건 | 0.92 | 0.97 |

  저자들의 결론은 **세 종류가 같은 것을 재고 있다**는 것이다.
- **함의가 두 방향으로 간다** (§5, pp.8~9).[^inozemtseva2014-coverage] 개발자에게는
  **더 단순한 커버리지를 쓰는 편이 이롭다** — 같은 양의 정보를 주면서 측정 부담이 적다.
  표준 제정 기관에게는 다른 말이 간다.

  > The FAA standard DO-178B, mentioned earlier in this paper, requires the use of MC/DC
  > adequate suites to ensure the quality of the resulting software; however, our results
  > suggest that this requirement may increase expenses without necessarily increasing
  > quality.

## 저자들이 내리는 처방

- **버리라는 것이 아니라 목표로 삼지 말라는 것이다** (§5, p.8. 같은 취지가 §8 결론에도
  있다, p.10):[^inozemtseva2014-coverage]

  > While coverage measures are useful for identifying under-tested parts of a program, and
  > low coverage may indicate that a test suite is inadequate, high coverage does not
  > indicate that a test suite is effective. This means that using a fixed coverage value as
  > a quality target is unlikely to produce an effective test suite.

- **테스트 생성 도구를 겨눈 한 줄이 있다** (§5, p.9).[^inozemtseva2014-coverage] 생성
  기법들이 흔히 결과 스위트의 커버리지를 최대화하려 하는데, **이 결과는 그것이 최선의
  접근이 아닐 수 있음을 시사한다**고 적는다.
- **저자들은 자기 대안도 잠정으로 내놓는다** (§5, p.9).[^inozemtseva2014-coverage] 결함
  검출 능력과 상관하는 지표가 여전히 미해결 문제라고 적고, 그 자리에 **뮤테이션 점수가
  커버리지의 좋은 대체물일 수 있다**고 쓴다. **이 페이지의 효과성 정의가 곧 뮤테이션
  점수라는 사실과 나란히 읽어야 하는 문장이다.**
- **이 논문이 실무자 주장을 실증 층에서 받았다고 스스로 밝힌다** (§5,
  p.8).[^inozemtseva2014-coverage] 고정 커버리지 값을 품질 목표로 쓰지 말라는 말은
  `members of the testing community have previously made this point`이고, 그 자리에 붙은
  참고문헌 둘이 **Fowler의 bliki 글**[^fowler2012-test-coverage]과 **Marick의
  "How to Misuse Code Coverage"**다. 저자들이 덧붙이는 말이 이 페이지가 서는 자리를
  정한다 — 그 제안들을 평가하기 어려웠던 이유는 **이만한 규모의 시스템을 다룬 연구가
  없었기 때문**이라는 것이다.
  - 이 KB에서 그 실무자 층은
    [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md)가 담는다.

## 커버리지가 예측하는 것과 못 하는 것

**효과성의 종속변수를 바꾸면 답이 달라진다. 그것이 이 논쟁을 읽는 축 하나다.**

- **뮤턴트가 아니라 실제 버그로 같은 물음을 다시 잰 연구가
  있다.**[^kochhar2015-real-bugs] Apache HTTPClient의 실제 버그 **67개**와 Mozilla
  Rhino의 **92개**를 대상으로, 버그마다 Randoop 스위트 여섯 개(원본과 그 0.2%·0.5%·1%·
  5%·10% 축소본)를 만들어 고친 버전에서 통과하고 고치기 직전 버전에서 실패하는지로
  효과성을 셌다 (§3, pp.2~3).
- **결과가 두 시스템에서 갈린다** (Table V, p.4, p 값 전부 유의):[^kochhar2015-real-bugs]

  | | 문장 커버리지 rpb | 분기 커버리지 rpb |
  |---|---|---|
  | HTTPClient | 0.57 (rpb² 0.33) | 0.60 (rpb² 0.36) |
  | Rhino | 0.77 (rpb² 0.59) | 0.74 (rpb² 0.55) |

  이 논문의 세기 구간(§2.3, p.2)으로 읽으면 HTTPClient는 중간, Rhino는 강함이다.
  **크기 쪽은 방향이 반대다** (Table IV, p.4) — HTTPClient가 0.70(강함), Rhino가
  0.37(약함)이다.
- **저자들이 이 글을 `preliminary study`라 부른다** (초록).[^kochhar2015-real-bugs] 대상이
  둘이고 5쪽이다. 이 KB는 이 값을 **방향의 근거로 쓰고 크기의 근거로 쓰지 않는다.**
- **같은 1저자의 2017년 후속은 종속변수가 다르다.** 그쪽은 **릴리스 후 결함**을 놓고
  커버리지를 본다. **이 KB는 그 논문을 확보하지 않았다 — 2차 경유이고, 이 페이지는 그
  논문의 어떤 수치도 적지 않는다.**
- **그래서 두 연구는 자기모순이 아니다.** 하나는 "이 스위트가 결함을 잡아내는가"를
  묻고 다른 하나는 "이 코드가 출시 뒤에 터지는가"를 묻는다. **커버리지가 예측하는 것과
  못 하는 것을 가르는 축은 커버리지 종류가 아니라 무엇을 예측 대상으로 놓았는가다.**

## 원문이 넘지 않은 선

- **인과를 주장하지 않는다** (§6.2, p.9).[^inozemtseva2014-coverage]
  `Since we have studied correlations, we cannot make any claims about the direction of
  causality.`
- **아주 높은 커버리지 구간을 놓쳤을 수 있다** (§6.3, p.9).[^inozemtseva2014-coverage]
  선행 연구 셋이 아주 높은 커버리지에서야 관계가 나타난다고 보고했는데, 이 연구의 생성
  스위트는 그런 값에 좀처럼 이르지 못했다. **저자들이 이 위협에 붙이는 반론이 있다** —
  90%에 이르러야 나타나는 관계는 대부분의 개발자에게 **관계가 없는 것과 기능적으로
  같다**는 것이다. 이 반론은 측정이 아니라 저자들의 판단이다.
- **클래스마다 다를 수 있다** (§6.3, p.9).[^inozemtseva2014-coverage] 객체지향 시스템에서
  결함은 소수 컴포넌트에 몰리므로 커버리지와 효과성의 관계가 클래스마다 다를 수 있다.
  저자들은 자기 결론이 **프로그램 전체 스위트의 커버리지를 재는 흔한 관행**에는 그대로
  선다고 적는다.
- **표본이 다섯이고 전부 오픈소스다** (§6.3, pp.9~10).[^inozemtseva2014-coverage] 게다가
  선정 기준(테스트 메서드 1,000개 이상, Ant, JUnit)이 까다로워 대상들이 서로 닮았고,
  산업 기준으로는 여전히 크지 않다고 적는다.
- **테스트 메서드가 온 클래스의 크기는 통제하지 않았다** (§6.3, p.9).[^inozemtseva2014-coverage]
- **커버리지를 버리라고 말하지 않는다.** 위 [저자들이 내리는 처방](#저자들이-내리는-처방)의
  인용이 그 선이다.

## 이 쌍이 정설이 아닌 이유

- **같은 물음에 반대 답을 낸 논문이 있고, 이 논문 자신이 그 사실을 적는다** (§2,
  p.3).[^inozemtseva2014-coverage] Gopinath 등의 연구를 두고
  `accepted to the same conference as the current paper`라고 쓰고, 그쪽이 여러 커버리지
  종류 모두에서 프로젝트를 가로지르는 상관을 찾았으며 **회귀 모형에 스위트 크기를 넣어도
  결과가 나아지지 않았다**고 보고한다는 것까지 옮긴다.
  - 그러고 나서 이 논문이 붙이는 유보가 논쟁의 형태를 보여 준다 — 그쪽 모형에 이미
    커버리지가 들어 있었으므로 **그것이 정확한 발견인지 다중공선성의 결과인지 분명하지
    않다**는 것이다. **이것은 측정이 아니라 해석 층의 반박이다.**
- **반대 극이 이 KB에 페이지로 서 있다**:
  [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md). 그쪽은 크기를
  통제한 뒤에도 커버리지가 추가 예측력을 갖는다는 결과와, 문장 커버리지가 뮤턴트 킬의
  최선 예측자라는 결과를 담는다.
- **이 쌍은 해소되지 않았다.** 이 KB는 어느 쪽도 정설로 세우지 않고 양쪽을 `contradicts`로
  묶어 둔다. 해소를 시도하려면 **효과성의 정의·대상의 규모·비교 단위(한 시스템 안의
  여러 스위트인가, 시스템을 가로지르는 한 스위트인가)** 셋을 먼저 맞춰야 한다 — 세
  논문이 이 셋에서 서로 다르다.

## LLM 시대의 지위

- **이 논쟁이 언어 모델이 만든 스위트에 다시 걸렸다.**[^zhao2026-llm-coverage-replication]
  최신 모델 11종이 만든 10만 개 넘는 테스트 케이스를 놓고 이 논문과 뮤테이션 쪽 논문
  하나를 재현한 연구가 있고, 게재 레코드는 ISSTA 2026(Proc. ACM Softw. Eng. 3권)이며
  **이 KB의 확보본은 arXiv v1이다.** 그래서 이 절은 방향만 적고 상관 계수를 옮기지 않는다.
- **이 논문의 핵심 논거가 그쪽에서 재현되지 않았다** (초록·1절). 언어 모델이 만든 스위트
  에서는 **크기가 지배적 교란 변수라는 증거를 거의 찾지 못했다**고 보고한다.
- **대신 조건이 새로 갈린다** (RQ2 요약). 모델에 넘긴 코드가 버그 없는 상태라고 볼 수
  있으면 커버리지가 실버그 검출과 어느 정도 상관하지만, **대상 코드에 이미 버그가 있으면
  상관이 한결같이 약해진다** — 버그 있는 코드 위에서 잰 커버리지는 그 버그를 잡는지에
  대해 말해 주지 않는다는 것이다.
- #hypothesis 이 재현 결과가 이 논문을 무효화하는 것이 아니라 **적용 범위를 사람이 쓴
  스위트로 좁힌다**는 읽기는 이 KB가 붙인 것이고 그 논문이 주장한 것이 아니다.

## 이어지는 페이지

- [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md) — 같은 물음에
  반대 답을 낸 두 논문. 이 쌍의 다른 극이다
- [단정 수와 단정 커버리지가 뮤턴트 킬을 예측한다](../concepts/assertions-predict-mutation-kills.md)
  — 이 논문이 지목한 교란 변수의 아래를 연 자리. 크기를 고정한 채 단정만 움직여도
  상관이 내려가지 않았다는 결과이고, 크기가 무엇을 대리하고 있었는지를 되짚는다
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 이 논문의
  결론을 운용 규칙으로 받은 산업 문서. 높은 수치가 스위트 품질을 보증하지 않는다는
  대목이 같은 방향이고, 그러면서도 관문은 걸라고 권하는 자리에서 갈린다
- [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md) —
  이 페이지가 효과성으로 쓴 종속변수 자체를 겨누는 자리. 뮤테이션 점수가 실결함을
  대신할 수 있는가는 이 논문이 묻지 않고 넘긴 물음이다
- [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md) —
  같은 크기 교란 논증을 커버리지가 아니라 뮤테이션 점수에 건 심사 실증이 그 묶음에 있다
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 이 논문이
  §5에서 참고문헌으로 지목하는 실무자 층. 주장이 먼저 있었고 이 논문이 규모를 붙였다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 생성된
  스위트가 커버리지를 크게 올리면서 결함 발견은 올리지 않은 사람 대상 통제실험
- [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md) — 분기 커버리지와
  죽인 뮤턴트를 테스트 선별의 기준으로 쓰는 자리
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 커버리지를
  관문의 조건으로 쓰면서 그것이 편의적 대리물임을 자기 논문에 적은 산업 배선
- [실용주의 스타터 킷](../concepts/pragmatic-starter-kit.md) — 같은 한계 진단에서 재는
  대상을 바꾸라는 결론으로 가는 실무 규범
- [테스트 오라클](../concepts/test-oracle.md) — 커버리지가 답하지 않는 물음. 실행했다는
  것과 옳은지 판정했다는 것은 다르다

[^inozemtseva2014-coverage]: Inozemtseva & Holmes 2014, "Coverage Is Not Strongly
    Correlated with Test Suite Effectiveness", ICSE 2014. **확보본 11쪽에 인쇄된 쪽
    번호가 없어 locator는 확보본 PDF 쪽(1~11)이다.** 학회명·개최지·연도는 1쪽 저작권
    상자가 근거이고 권·호·쪽수 줄은 문면에 없다. 이 페이지는 초록과 1절 연구 질문,
    3절 방법 전부, 4절 결과(Table 3·4·5와 세 Answer 상자, Figure 2의 r² 범위), 5절 논의,
    6절 타당도 위협, 7절 향후 과제, 8절 결론을 담았다. 2절 Table 1의 선행 연구 열두 편
    요약과 그 수치는 이 논문이 경유해 전하는 제3자 값이라 옮기지 않았다. 1쪽 각주 1이
    가리키는 보조 자료 사이트는 확보하지 않았다.
[^kochhar2015-real-bugs]: Kochhar, Thung & Lo 2015, "Code Coverage and Test Suite
    Effectiveness: Empirical Study with Real Bugs in Large Systems", SANER 2015. 확보본
    5쪽이고 1쪽 하단에만 인쇄 쪽 번호 560이 있어 locator는 확보본 PDF 쪽(1~5)이다.
    초록이 스스로 `In this preliminary study`라고 밝힌다. **같은 1저자의 2017년 후속
    (IEEE Transactions on Reliability 66(4), 종속변수가 릴리스 후 결함)은 이 KB가 확보하지
    않았고, 이 페이지의 그 논문 관련 서술은 2차 경유다.**
[^fowler2012-test-coverage]: Fowler 2012, "Test Coverage", martinfowler.com bliki,
    문면 날짜 `17 April 2012`. 열람일 2026-08-23. 실무자 글이고 측정이 없다. 이 페이지는
    이 글을 **회의 측 논문이 §5에서 지목하는 참고문헌**으로만 인용하고 주장의 근거로
    쓰지 않는다. 이 글이 본문에 담은 인용 둘은 둘 다 Marick의 말이므로 이 KB는 그것을
    `marick1999-coverage` 원전으로 인용한다.
[^zhao2026-llm-coverage-replication]: Zhao, Zhou & Cohen 2026, "Do Coverage and Mutation
    Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability
    Study)". **확보본은 arXiv:2607.22880v1이고, 같은 1쪽에 게재 레코드가 인쇄돼 있다**
    (Proc. ACM Softw. Eng. 3, ISSTA, Article ISSTA002, October 2026, doi 10.1145/3832093).
    확보본이 심사 통과본 조판이 아니므로 이 페이지는 결과 표의 계수를 옮기지 않고 초록과
    1절, RQ1·RQ2 요약 상자의 방향만 옮겼다.

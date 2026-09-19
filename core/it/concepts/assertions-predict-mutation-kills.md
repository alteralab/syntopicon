---
type: concept
title: 단정 수와 단정 커버리지가 뮤턴트 킬을 예측한다
description: 커버리지 논쟁이 다투던 스위트 크기의 아래를 열어 테스트 메서드 안의 단정을 변수로 놓은 자리 — 이 논문의 효과성이 곧 PIT 뮤테이션 점수라는 정의와 그 순환, 크기를 통제해도 남는 단정 수의 상관과 그 통제 설계, 단정 커버리지가 오라클 품질 지표에서 왔다는 계보, 단정 실패로만 죽는 뮤턴트를 따로 센 명시 뮤테이션 점수, 단정 커버리지를 통제하면 문장 커버리지의 상관이 어디까지 내려앉는가, 사람이 쓴 단정과 생성된 단정의 격차와 단정 종류별 순위, 그리고 원문이 실결함으로 넘어가지 않은 선
generated: { by: "claude-opus-5", at: "2026-08-23T05:40:00Z" }
sources:
  - { id: zhang2015-assertions, resource: /it/sources/zhang2015-assertions.md }
---

# 단정 수와 단정 커버리지가 뮤턴트 킬을 예측한다

- [이 소스의 지위](#이-소스의-지위)
- [효과성을 무엇으로 쟀는가](#효과성을-무엇으로-쟀는가)
- [원문의 변수는 밀도가 아니라 수와 커버리지다](#원문의-변수는-밀도가-아니라-수와-커버리지다)
- [크기를 통제해도 단정의 상관이 남는다](#크기를-통제해도-단정의-상관이-남는다)
- [같은 크기에서 단정이 많은 쪽이 낫다](#같은-크기에서-단정이-많은-쪽이-낫다)
- [단정 커버리지는 오라클 품질 지표에서 왔다](#단정-커버리지는-오라클-품질-지표에서-왔다)
- [단정 실패로만 죽는 뮤턴트를 따로 센다](#단정-실패로만-죽는-뮤턴트를-따로-센다)
- [단정 커버리지를 통제하면 문장 커버리지가 내려앉는다](#단정-커버리지를-통제하면-문장-커버리지가-내려앉는다)
- [단정의 종류가 효과성을 가른다](#단정의-종류가-효과성을-가른다)
- [저자들이 내리는 처방](#저자들이-내리는-처방)
- [이 논문이 커버리지 논쟁에서 서는 자리](#이-논문이-커버리지-논쟁에서-서는-자리)
- [원문이 넘지 않은 선](#원문이-넘지-않은-선)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **커버리지 논쟁이 스위트 크기(test suite size)를 교란 변수로 지목한 뒤,
그 크기의 아래에 있는 것은 무엇인가 — 테스트 메서드 안의 단정(assertion)이 효과성을
설명하는가.**

조건: 자바 오픈소스 다섯 개, 2015년, 효과성은 PIT 뮤테이션 점수.

## 이 소스의 지위

- **근거 등급은 `peer-reviewed`다.** 게재 레코드가 확보본 1쪽 하단에 인쇄돼 있다 —
  `ESEC/FSE’15, August 30 – September 4, 2015, Bergamo, Italy` ·
  `ACM. 978-1-4503-3675-8/15/08...` · `http://dx.doi.org/10.1145/2786805.2786858`
  (1쪽 하단 저작권 상자, p.214).[^zhang2015-assertions]
- **다만 확보본은 ACM 최종 조판이 아니라 저자본이다.** 같은 자리가
  `This is the author’s version of the work` … `The definitive version was published in the
  following publication:`이라고 밝힌다. **게재 레코드와 인쇄 쪽 번호를 함께 실은
  저자본이므로** 이 페이지의 locator는 확보본에 인쇄된 쪽(214~224)이다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 2절이 훑는 선행 연구의 수치는
  이 논문이 경유해 전하는 제3자 값이라 이 페이지가 옮기지 않는다.
- **대상과 규모** (Table 1, p.216).[^zhang2015-assertions] JFreeChart · Apache Commons
  Lang · Urban Airship Java Library · lambdaj · Asterisk-Java. 자바 SLOC 합계 329,600,
  테스트 케이스 5,892개, 단정 24,701개다. 마스터 스위트의 문장 커버리지(statement
  coverage)는 24%(Asterisk-Java)에서 93%(lambdaj)까지이고 단정 커버리지는 10%에서
  65%까지다.
  - 이 표의 `Total/Average` 행은 문장 커버리지 45% · 단정 커버리지 30%로 인쇄돼 있는데,
    이는 다섯 값의 산술 평균이 아니라 JFreeChart 행과 같은 값이다. **집계 방식이 표에도
    본문에도 적혀 있지 않으므로 이 페이지는 이 두 칸을 쓰지 않고 프로젝트별 값만 쓴다.**

## 효과성을 무엇으로 쟀는가

**이 절이 이 페이지 전체의 전제다. 이 정의를 떼면 아래 결과가 다른 것을 뜻하게 된다.**

- **이 논문의 효과성(effectiveness)은 PIT 뮤테이션 점수(mutation score)다** (§3.3.1,
  p.216).[^zhang2015-assertions] 저자들의 정의가 두 문단에 나뉘어 있다.

  > Test suite effectiveness. Effectiveness captures the fault detection ability of a test
  > suite, which can be measured as a percentage of faults detectable by a test suite. To
  > measure the fault detection ability of a test suite, a large number of known real faults
  > are required for each subject, which is practically unachievable.

  > Mutation score. The mutation score, calculated as a percentage of killed mutants over
  > total number of non-equivalent mutants, is used to estimate fault detection ability of a
  > test suite.

- **그래서 이 페이지의 제목이 "효과성"이 아니라 "뮤턴트 킬"이다.** 이 논문이 예측한다고
  말한 대상은 실제 결함이 아니라 PIT가 만든 뮤턴트의 죽은 비율이다. **"단정이 실결함을
  더 잘 예측한다"가 아니라 "단정이 뮤테이션 점수를 더 잘 예측한다"가 이 논문이 잰
  것이다.**
- **동등 뮤턴트(equivalent mutant)를 가정으로 처리했다** (§3.3.1,
  p.216).[^zhang2015-assertions] 마스터 스위트가 죽이지 못한 뮤턴트(mutant)를 전부
  동등으로 간주했고, 회의 측 논문과 같은 처리라고 밝힌다. 도구는 PIT이고 기본 뮤테이션
  연산자를 썼다.
- **저자들 자신이 이 대체가 논쟁거리임을 인정하고, 그 물음을 다른 논문들에 넘긴다**
  (§3.3.1, p.216):[^zhang2015-assertions]

  > Mutations are produced by transforming a program syntactically through mutation
  > operators, and one could argue about the eligibility of using the mutation score to
  > estimate a test suite’s effectiveness. However, mutation testing is extensively used as
  > a replacement of real fault detection ability in the literature [14, 20, 22]. There is
  > also empirical evidence confirming the validity of mutation testing in estimating test
  > suite effectiveness [11, 12, 15, 21].

  **이 문단이 이 논문의 순환이 닫히는 자리다** — 뮤테이션 점수가 결함 검출 능력을
  대신할 수 있는지는 이 논문이 재지 않고 선행 연구 인용으로 처리한다. 타당도 위협
  절(§5.5, p.223)에도 이 항목이 없다. **뮤테이션 점수 자체가 실결함을 대신할 수 있는지는
  이 페이지의 물음이 아니라 별도 페이지의 물음이다** —
  [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md)가
  그 물음에 답한다. 그쪽이 옮긴 원전의 눈금은 결합 효과(coupling effect)가 **증명할 길이
  없는 경험적 원리**라는 것이다.
- #hypothesis **순환이 한 겹 더 있다.** 아래
  [명시 뮤테이션 점수](#단정-실패로만-죽는-뮤턴트를-따로-센다)는 정의상 **단정이 죽인
  뮤턴트의 비율**이므로, "단정이 명시 뮤테이션 점수를 잘 예측한다"는 부분적으로 정의의
  되풀이다. 이 읽기는 이 KB가 붙인 것이고 원문이 적은 것이 아니다. **원문이 단정 없이
  성립하는 종속변수로 쓴 것은 일반 뮤테이션 점수 쪽이다.**

## 원문의 변수는 밀도가 아니라 수와 커버리지다

**용어를 먼저 못 박는다 — 원문에 `density`라는 낱말은 없다.**

- 이 논문이 재는 독립변수는 셋이다: **단정 수**(number of assertions / assertion
  quantity), **단정 커버리지**(assertion coverage), **단정의 종류**(assertion types)
  (§3, p.215).[^zhang2015-assertions]
- **"밀도"에 해당하는 측정은 두 자리에 있다.** 하나는 서술 통계인 테스트 케이스당 단정
  수(Table 2, p.216: 프로젝트별 평균 4.1 · 5.1 · 2.1 · 2.8 · 3.0, 표준편차 6.7 · 7.4 ·
  3.6 · 3.2 · 2.9)이고, 다른 하나는 아래
  [버킷 실험](#같은-크기에서-단정이-많은-쪽이-낫다)이다. **버킷 실험이 곧 밀도 실험이지만
  원문은 그 이름을 쓰지 않는다.**
  - 같은 표의 최댓값 114(JFreeChart)는 저자들이 믿기 어려워 손으로 확인했다고 각주에
    적는다 — `org.jfree.chart.plot.CategoryPlotTest`의 `testEquals` 메서드다 (p.216 각주 5).

## 크기를 통제해도 단정의 상관이 남는다

- **먼저 크기를 무시하고 잰다** (§4.1 · Table 4, p.219).[^zhang2015-assertions] 다섯 대상
  각각에서 무작위로 만든 스위트를 놓고, 효과성이 **스위트 크기**(m)와 **단정 수**(a)
  각각과 얼마나 상관하는지를 Pearson(ρp)과 Kendall(ρk)로 잰다. p 값은 전부
  `< 2.2e − 16`이다.

  | 대상 | ρp(m) | ρp(a) | ρk(m) | ρk(a) |
  |---|---|---|---|---|
  | JFreeChart | 0.954 | 0.954 | 0.967 | 0.970 |
  | Apache Commons Lang | 0.973 | 0.973 | 0.969 | 0.969 |
  | Urban Airship Java Library | 0.927 | 0.927 | 0.917 | 0.917 |
  | lambdaj | 0.929 | 0.928 | 0.912 | 0.930 |
  | Asterisk-Java | 0.945 | 0.947 | 0.889 | 0.894 |

  - **분모**: 대상마다 마스터 스위트에서 비복원 무작위로 뽑은 스위트들이고, 크기도
    무작위로 정했다 (§3.3.1, p.216). JFreeChart의 그림은 그 중 1,000개를 그린 것이다
    (Figure 1, p.219).
  - **본문 문장이 한 칸에서 표를 앞선다** — 저자들은 단정 쪽 상관이 크기 쪽보다
    `slightly higher or equal`이라고 적지만, lambdaj의 Pearson은 크기 0.929 · 단정
    0.928로 단정 쪽이 0.001 낮다. **이 절의 결과는 "단정이 크기를 이긴다"가 아니라
    "둘이 거의 구별되지 않는다"에 가깝다.**
- **그 다음 크기를 고정하고 다시 잰다** (§4.1 · Table 5, p.219).[^zhang2015-assertions]
  **마스터 스위트의 테스트 메서드를 전부 넣은 채 단정만 일부 골라** 스위트를 만든다 —
  기준 수 b에서 시작해 단계 x씩 늘려 i번째 스위트가 `b + x·i`개의 단정을 갖게 한다
  (§3.3.1, pp.216~217). **크기가 상수인 채 단정 수만 움직이는 설계다.**

  | 대상 | 기준 b | 단계 x | ρp(a) | ρk(a) |
  |---|---|---|---|---|
  | JFreeChart | 1,000 | 50 | 0.976 | 0.961 |
  | Apache Commons Lang | 100 | 100 | 0.929 | 0.970 |
  | Urban Airship Java Library | 0 | 10 | 0.948 | 0.846 |
  | lambdaj | 100 | 10 | 0.962 | 0.839 |
  | Asterisk-Java | 100 | 5 | 0.928 | 0.781 |

  p 값은 전부 `< 2.2e − 16`이다. **크기를 통제해도 상관이 내려가지 않는다는 것이 이
  표의 뜻이고, 회의 측 논문이 커버리지에서 관찰한 하락과 대비되는 자리다.**
- 저자들이 이 두 절에 붙인 상자가 Finding 1과 2다 (§4.1, p.219).[^zhang2015-assertions]

  > Finding 1: Our results indicate that, without controlling for test suite size, there is
  > a very strong correlation between the effectiveness of a test suite and the number of
  > assertions it contains.

  > Finding 2: Our results suggest that, there is a very strong correlation between the
  > effectiveness of a test suite and the number of assertions it contains, when the
  > influence of test suite size is controlled for.

## 같은 크기에서 단정이 많은 쪽이 낫다

- **이번에는 단정 쪽을 고정한다** (§3.3.1 p.217 · §4.1 Figure 2 p.219).[^zhang2015-assertions]
  테스트 케이스를 **자기가 가진 단정 수에 따라** 겹치지 않는 세 통(low · middle · high)에
  나눈 뒤, 각 통에서 100개씩 스위트를 무작위로 만든다. JFreeChart의 통 경계는 단정 2개
  이하 · 3~4개 · 5개 이상이고, 통마다 크기가 비슷해지도록 갈랐다.
- **분모와 통의 성격**(§4.1, p.219): low · middle · high 통이 각각 테스트 케이스
  **762 · 719 · 742개**를 담았고, 케이스당 평균 단정 수는 **0.9 · 2.5 · 9.1개**다.
  **이것이 이 논문에서 밀도에 가장 가까운 측정이다.**
- **결과는 곡선 세 개의 위아래다** (§4.1, p.219).[^zhang2015-assertions] 어느 곡선에서든
  테스트 메서드가 늘면 효과성이 오르지만, **같은 크기에서 단정 수준이 높은 통의 곡선이
  늘 위에 있다.** 저자들의 문장 — 아래 곡선의 어떤 스위트를 잡아도 **같은 크기이면서
  효과성이 더 높은 스위트가 위 곡선에 존재한다.**

  > Finding 3: Our results indicate that, for the same test suite size, assertion quantity
  > can significantly influence the effectiveness.

## 단정 커버리지는 오라클 품질 지표에서 왔다

**이 절이 이 페이지를 오라클 쪽에 잇는 자리다.**

- **단정 커버리지의 정의** (§3.3.2, p.217):[^zhang2015-assertions]

  > Assertion coverage, also called checked coverage [24], measures the fraction of
  > statements in the source code executed via the backward slice of the assertion
  > statements in a test suite.

  **실행된 문장이 아니라 단정이 실제로 값을 물어본 문장의 비율이다.** 계산은 슬라이스로
  얻은 검사된 문장(checked statements) 수를 전체 문장 수로 나눈 것이고, 도구는 동적
  슬라이서 JavaSlicer다.
- **이 지표의 출처가 오라클 품질 측정이다** (§2, p.215).[^zhang2015-assertions] 저자들이
  Schuler & Zeller(ICST 2011)를 이렇게 소개한다 — 그들이 checked coverage를
  `as a metric to assess test oracle quality` 제안했고, 이 논문은 그것에서 착안해
  단정 커버리지를 잰다. 두 낱말을 논문 안에서 호환해 쓴다고 각주에 밝힌다.
- **원논문과의 규모 차이도 같은 자리에 적는다** (§2, p.215).[^zhang2015-assertions]
  Schuler & Zeller는 스위트 일곱 개를 견주었고 이 논문은 대상마다 수천 개까지 만든다.
- **왜 문장 커버리지를 대조군으로 골랐는지도 밝힌다** (§3.3.2, p.217).[^zhang2015-assertions]
  실무에서 가장 흔히 쓰이고 도구 지원이 좋다는 것이 첫째, **2015년 저술 시점 기준 최근 실증 둘이 문장 커버리지가
  다른 어떤 커버리지 기준 못지않다고 보고했다**는 것이 둘째다. 그 둘로 지목하는 것이
  이 KB의 논쟁 쌍 양극(Gopinath 등 · Inozemtseva & Holmes)이다.
- #hypothesis **오라클의 실질성을 재는 게이트를 세운다면 이 지표가 그 자리의 후보다.**
  단정이 오라클이라는 연결은 이 논문이 아니라
  [테스트 오라클](../concepts/test-oracle.md)의 §4.2 부류 규정이 대고, 이 논문은 그 부류를
  **얼마나 넓게 걸었는가**를 재는 눈금을 준다. 이 배치는 이 KB가 붙인 읽기다.

## 단정 실패로만 죽는 뮤턴트를 따로 센다

- **명시 뮤테이션 점수(explicit mutation score)의 정의** (§3.3.2, p.217).[^zhang2015-assertions]
  뮤턴트는 두 갈래로 죽는다 — 단정이 실패해서(explicitly killed) 죽거나 프로그램이
  터져서(implicitly killed) 죽는다. 명시 뮤테이션 점수는 앞쪽만 센 비율이다. 재는 법은
  뺄셈이다 — 스위트에서 단정을 전부 지우고 뮤테이션 점수를 다시 잰 뒤 원래 점수에서
  뺀다.
- **프로젝트마다 그 비율이 크게 다르다** (Table 3, p.217):[^zhang2015-assertions]

  | 대상 | 생성 뮤턴트 | 죽은 뮤턴트 | 단정이 죽인 것 | 단정 몫 |
  |---|---|---|---|---|
  | JFreeChart | 34,635 | 11,299 | 7,510 | 66% |
  | Apache Commons Lang | 11,632 | 9,952 | 7,271 | 73% |
  | Urban Airship Java Library | 4,638 | 2,546 | 701 | 28% |
  | lambdaj | 1,340 | 1,084 | 377 | 35% |
  | Asterisk-Java | 4,775 | 957 | 625 | 65% |

  **단정 몫의 분모는 그 스위트가 죽인 뮤턴트이지 생성된 뮤턴트 전체가 아니다.**
- **이 구분에 저자들이 붙이는 비대칭이 이 논문의 논거 하나다** (§5.2,
  p.222).[^zhang2015-assertions] 암묵으로 죽는 뮤턴트는 단정으로도 죽을 수 있지만,
  **단정으로 죽는 뮤턴트는 단정 아닌 문장으로는 결코 죽지 않는다.** 논리적 결함은
  실행만으로 드러나지 않고 기대와의 모순을 물어보는 문장이 있어야 잡히기 때문이다.
  저자들의 결론 — `If we only focus on explicitly detectable mutants, then test assertions
  are the only means to achieve suite effectiveness.`
  - **같은 문단의 한 문장이 자기 표와 어긋난다.** 저자들은
    `more than half of all detectable mutants (28%–73%) are explicitly detected by
    assertions`라고 쓰는데, 괄호 안 하한 28%는 절반이 아니다. Table 3에서 절반을 넘는
    것은 다섯 중 셋이다.

## 단정 커버리지를 통제하면 문장 커버리지가 내려앉는다

- **통제 없이 보면 둘 다 아주 강하다** (§4.2 · Figure 4a, p.220).[^zhang2015-assertions]
  JFreeChart의 무작위 스위트 1,000개에서 뮤테이션 점수에 대한 회귀의 조정 R²는 단정
  커버리지 쪽 0.9836, 문장 커버리지 쪽 0.9881이고 p 값은 `< 2.2e − 16`이다. **이
  대목에서는 문장 커버리지 쪽이 오히려 근소하게 높다.**
  - 저자들이 여기서 끌어내는 것은 계수의 크기가 아니라 **기울기**다 — 어떤 스위트의 단정
    커버리지가 다른 스위트의 문장 커버리지와 같은 값이면 앞쪽이 훨씬 효과적이므로,
    단정 커버리지가 `a more sensitive predictor`라는 것이다.
- **단정 커버리지를 계단식으로 고정한 스위트를 따로 만든다** (§3.3.2 p.218 · §4.2
  p.220).[^zhang2015-assertions] 검사된 문장 수를 목표 구간 `[b + x·i, (b + x·i) + 10]`에
  들어올 때까지 테스트 메서드를 무작위로 더해 만든다. **대상마다 단정 커버리지 수준
  다섯~여섯 개, 수준마다 스위트 50개**다 (Figure 3, p.220).
- **그 스위트들에서 단정 커버리지의 예측력**(§4.2, p.220 · Figure 3
  캡션):[^zhang2015-assertions] 회귀의 조정 R²가 뮤테이션 점수에 대해 **0.94~0.99**,
  명시 뮤테이션 점수에 대해 **0.80~0.99**다. Kendall τ로는 각각 **0.88~0.91**과
  **0.80~0.90**이다.
- **그리고 같은 스위트들에서 문장 커버리지의 예측력이 무너진다** (Table 6,
  p.221):[^zhang2015-assertions] 단정 커버리지가 고정된 조건에서 문장 커버리지와
  뮤테이션 점수의 Kendall τ는 **0.50~0.76**, 명시 뮤테이션 점수와는 **0.01~0.63**이다.
  - **분모**: 대상 다섯 × 단정 커버리지 수준 다섯~여섯 = 표의 26행이고, 각 행이 스위트
    50개다.
  - 저자들이 낮은 쪽을 프로젝트로 특정한다 — 명시로 죽는 뮤턴트가 전체의 3분의 1쯤인
    lambdaj와 Urban Airship Java Library에서 문장 커버리지와 명시 뮤테이션 점수의 상관이
    **0.01~0.33**에 머문다. *(원문은 이 문장에서 Urban Airship에 ID 5를 붙이는데 Table 1에서
    그 프로젝트의 ID는 3이다 — 표기 오류다.)*
- **민감도를 수치로 대비한 예도 하나 있다** (§4.2, p.221).[^zhang2015-assertions]
  JFreeChart에서 단정 커버리지가 **약 4%p 오를 때** 뮤테이션 점수는 **약 12.4%p**,
  명시 뮤테이션 점수는 **약 11%p** 오른다. 같은 4%p라도 **문장 커버리지 쪽은 둘 중
  어느 것도 늘 올리지는 않는다**고 적는다.
  - 단위는 전부 절대 %p이고, 분모는 Table 6의 JFreeChart 여섯 행(단정 커버리지
    4.2%→25.1%, 뮤테이션 점수 0.21→0.85, 명시 0.13→0.75)이다.

  > Finding 5: Our results suggest that, assertion coverage is capable of predicting both
  > mutation score and explicit mutation score. With assertion coverage controlled for,
  > there is only a moderate to strong correlation between statement coverage and mutation
  > score, and a low to moderate correlation between statement coverage and explicit
  > mutation score. Test suite effectiveness is more sensitive to assertion coverage than
  > statement coverage.

## 단정의 종류가 효과성을 가른다

**이 절의 결과는 전부 JFreeChart 하나에서 나왔다** — 그 프로젝트의 단정 9,177개다
(§4.3, p.221).[^zhang2015-assertions] 표본 스위트는 **종류마다 50개, 각 스위트가 그
종류의 단정 100개**를 담는다.

- **사람이 쓴 단정과 생성된 단정의 격차가 가장 크다** (§4.3, p.221).[^zhang2015-assertions]
  Randoop이 만든 단정 100개짜리 스위트 50개는 **뮤턴트를 거의 죽이지 못했고**, 단정 수를
  500개로 늘려도 같은 모양이었다. 사람이 쓴 쪽은 단정이 늘수록 효과성이 오른다.

  > Finding 6: Our results indicate that, human-written test assertions are far more
  > effective than automatically generated test assertions.

- **내용 종류(assertion content type)로 갈랐을 때** (§4.3 · Table 7 · Table 8,
  p.222).[^zhang2015-assertions] One-Way ANOVA의 F 값이 **1544**(자유도 3/196, p `<2e-16`),
  Tukey HSD의 뮤테이션 점수 차이(절대값, 0~1 척도)는 아래와 같다.

  | 짝 | 차이 | 95% 신뢰구간 | 보정 p |
  |---|---|---|---|
  | boolean − object | −0.0002 | −0.0032 ~ 0.0028 | 0.9985 |
  | number − boolean | −0.0470 | −0.0500 ~ −0.0440 | 0.0000 |
  | string − number | −0.0156 | −0.0186 ~ −0.0126 | 0.0000 |

  **boolean과 object는 갈리지 않는다.** 표본 스위트가 쓴 단정의 모집단 크기는 object
  1,307 · boolean 4,940 · number 1,754 · string 208개다 (Figure 5b, p.222).

  > Finding 7: Our results suggest that, there is a significant difference between the
  > effectiveness of assertions that assert on different content types. Their effectiveness
  > can be ranked in increasing order: (1) string, (2) number, (3) boolean or object type.

- **메서드 종류(assertion method type)로 갈랐을 때** (§4.3 · Table 7 · Table 8,
  p.222).[^zhang2015-assertions] F 값 **87.87**(자유도 2/147, p `<2e-16`)이고, Tukey의
  차이는 `assertNull/Not` − `assertTrue/False`가 **−0.0103**(−0.0145 ~ −0.0060, p 1e−07),
  `assertEquals/Not` − `assertNull/Not`이 **−0.0133**(−0.0175 ~ −0.0091, p 0e+00)이다.
  모집단은 `assertTrue/False` 5,229 · `assertNull/Not` 167 · `assertEquals/Not` 3,481개다.
  `assertSame`·`assertNotSame`은 JFreeChart에 27개뿐이라 대표성이 없다고 보고 뺐다.

  > Finding 8: Our results indicate that, there is a significant difference between the
  > effectiveness of different assertion method types. The effectiveness of the method types
  > can be ranked from low to high as: (1) assert(Not)Null, (2) assert(Not)Equals, and (3)
  > assertTrue/False.

- **저자들이 두 분류의 얽힘을 스스로 적는다** (§5.5, p.223).[^zhang2015-assertions]
  boolean 내용 종류와 `assertTrue/False` 메서드 종류는 늘 함께 나타나므로 어느 쪽 효과인지
  가를 수 없다. **위 두 순위를 따로 읽으면 안 되는 이유가 원문에 적혀 있다.**

## 저자들이 내리는 처방

- **재는 대상을 바꾸라는 것이다** (§5.3, p.223):[^zhang2015-assertions]

  > Our results suggest that testers should aim at increasing the assertion coverage of
  > their test suite instead of its statement coverage, when trying to improve a test
  > suite’s effectiveness.

  같은 절이 문장 커버리지의 자리를 이렇게 좁힌다 — 생성된 뮤턴트가 전부 명시로 죽는
  것은 아니라는 가정 아래에서만 유효한 추정량이고, `statement coverage is not an adequate
  metric of logical-fault detection ability`.
- **생성 단정은 대체물이 아니라 보충물이다** (§5.4, p.223).[^zhang2015-assertions] 생성된
  단정은 사람이 쓴 단정보다 훨씬 덜 효과적이므로 `should only be used as a supplement of
  human-written assertions instead of a replacement`.
- **결론이 조건절을 달고 있다** (§6, p.223):[^zhang2015-assertions]

  > Our results indicate that it might be sufficient to use the assertion quantity and
  > assertion coverage as criteria to measure a suite’s adequacy, since these two metrics
  > are at least as good as suite size and statement coverage.

  **`might`가 이 논문이 스스로 두는 눈금이다** — 단정 지표가 크기·문장 커버리지보다 못하지
  않다는 것이지, 실결함을 더 잘 잡는다고 적지 않는다.

## 이 논문이 커버리지 논쟁에서 서는 자리

- **이 논문의 주장은 논쟁의 어느 극을 편드는 것이 아니라 논쟁의 관측값을 설명하는
  것이다** (§5.1, p.222).[^zhang2015-assertions] 저자들의 정리 —

  > Therefore, test suite size can predict the effectiveness only under the assumption that
  > there is a linear relationship between the number of test methods and the number of
  > assertions in the test suite. We believe this is an interesting finding, which explains
  > why previous studies [20] have found a strong correlation between suite size and
  > effectiveness.

  **[20]은 회의 측 논문이다.** 그쪽이 크기를 교란 변수로 지목했다면, 이 논문은 그 크기가
  왜 신호를 갖는지를 **크기와 단정 수의 선형 관계**로 되짚는다.
- **그 선형 관계는 이 논문이 관찰로 확인한 것이다** (§3.3.1, p.216).[^zhang2015-assertions]
  무작위로 만든 스위트에서는 크기와 단정 수가 선형이고, 그래서 크기와 효과성의 관계가
  단정과 효과성의 관계로부터 **추이적으로 옮겨 온 것일 수 있다**는 것이 통제 설계를 짠
  이유다.
- **양극과의 관계가 이렇게 정리된다.**
  - [커버리지 신호는 스위트 크기가 만든다](../concepts/coverage-confounded-by-suite-size.md)
    — 크기를 통제하면 커버리지의 상관이 내려앉는다는 회의 측 결과를 이 논문은 뒤집지
    않는다. 대신 **그 크기가 대리하고 있던 것**을 지목한다.
  - [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md)
    — 문장 커버리지가 최선의 예측자라는 옹호 측 결과를 이 논문은 **대조군 선정의 근거로
    인용하고**(§3.3.2, p.217), 단정 커버리지를 통제하면 그 예측력이 내려앉는다고 잰다.
  - **세 논문이 전부 효과성을 뮤테이션 점수로 정의한다.** 그래서 이 논문이 논쟁을
    중재하는 층은 종속변수가 아니라 독립변수 쪽이다 — **무엇이 예측하는가는 옮겼지만
    무엇을 예측하는가는 그대로다.** 그 종속변수 자체를 겨누는 자리가
    [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md)다.
- **1999년의 실무 규범과 겹치는 자리도 있다.**
  [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md)가 커버리지는
  실행 여부만 말한다고 적은 자리를, 이 논문은 **실행과 검사를 나눈 두 눈금**으로
  수치화한다. 2020년의 산업 권고
  [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md)가 단정의
  실질성은 뮤테이션 테스팅이 잰다고 지목한 대목과도 같은 물음이다 — 다만 그쪽은 지표를
  이름으로만 지목하고 이쪽은 그 지표로 잰 값을 낸다.

## 원문이 넘지 않은 선

- **실결함을 대상으로 하지 않았다.** 위
  [효과성을 무엇으로 쟀는가](#효과성을-무엇으로-쟀는가) 참조. 뮤테이션 점수가 결함 검출
  능력을 대신할 수 있는지는 선행 연구 인용으로 처리되고 타당도 위협 절에는 없다.
- **역방향 통제가 없다.** 단정 커버리지를 고정하고 문장 커버리지를 본 실험은 있으나,
  **문장 커버리지를 고정하고 단정 커버리지를 본 실험은 이 논문에 없다.** 대칭 실험이
  있어야 "단정 커버리지가 더 나은 지표"가 완결된다.
- **외부 타당도의 경계를 저자들이 적는다** (§5.5, p.223).[^zhang2015-assertions] 자바 다섯
  프로젝트이고 단정은 JUnit4 것이므로 다른 언어·프레임워크로 넘어가지 않을 수 있다.
  단정 종류 결과는 JFreeChart 하나에서 나왔다. 생성기는 Randoop 하나뿐이고 다른 오라클
  생성 전략이면 결과가 달랐을 수 있다고 적는다.
- **내부 타당도의 경계도 같은 절에 있다** (§5.5, p.223).[^zhang2015-assertions] PIT·Clover·
  JavaSlicer가 옳게 동작한다고 가정했다. 동등 뮤턴트 근사가 그 수를 과대평가할 수 있으나
  상수를 빼는 것이라 상관에는 영향이 없다고 적는다. **PIT가 뮤턴트를 잡은 첫 단정에서
  실행을 멈추므로** 어떤 단정들이 함께 실패했을지는 이 데이터로 알 수 없다.
- **인과를 주장하지 않는다.** 이 논문이 재는 것은 상관이고, 단정을 늘리면 효과성이
  오른다는 개입 실험은 없다. 단정만 골라 빼는 통제 실험(Table 5)이 가장 개입에 가깝지만
  그것도 **기존 단정의 부분집합**을 다룰 뿐 새 단정을 쓰지 않는다.
- **높은 단정 커버리지 구간이 얇다.** Table 6이 다루는 단정 커버리지의 최댓값은 대상별로
  25.1% · 41.4% · 33.6% · 47.5% · 7.3%다 (p.221). **절반을 넘는 구간의 데이터가 없다.**
- **저자들이 남긴 후속 과제 둘** (§6, p.223).[^zhang2015-assertions] 더 많은 프로그램으로
  결과를 다시 확인하는 것과, 단정 종류별 효과성 차이의 이유를 질적으로 분석하는 것이다.

## 이어지는 페이지

- [커버리지 신호는 스위트 크기가 만든다](../concepts/coverage-confounded-by-suite-size.md) —
  이 논문이 설명 대상으로 삼는 회의 측 결과. 크기가 교란 변수라는 진단
- [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md) —
  이 논문이 대조군 선정 근거로 인용하는 옹호 측 결과
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 실행과
  검사를 가른 1999년의 실무 규범. 이 논문이 그 구분에 눈금을 붙인다
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 단정의
  실질성은 커버리지가 아니라 뮤테이션이 잰다고 지목한 2020년 산업 문서
- [뮤테이션 테스팅은 최종 심급이 아니다](../concepts/mutation-testing-not-a-final-arbiter.md) —
  이 논문이 선행 연구 인용으로 처리하고 넘긴 물음. 효과성을 뮤테이션 점수로 정의한 이
  페이지의 전제가 거기서 심판된다
- [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md) —
  그 물음을 실증으로 시험한 심사 논문 묶음. 이 페이지의 순환이 닫히는 자리를 바깥에서
  여는 쪽이다
- [실용주의 스타터 킷](../concepts/pragmatic-starter-kit.md) — 재는 대상을 코드
  커버리지에서 상태 커버리지로 옮기라는 실무 규범. 이 논문은 같은 자리를 단정 커버리지로
  옮긴다 — 도구를 바꾸는 처방과 눈금을 바꾸는 처방이 나란히 서는 자리다
- [테스트 오라클](../concepts/test-oracle.md) — 단정을 오라클의 한 부류로 규정하는 자리.
  이 논문의 단정 커버리지는 그 부류가 얼마나 넓게 걸렸는지를 재는 눈금이다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  생성된 단정이 무엇을 적는가의 후속 실측. 이 논문의 Finding 6과 같은 방향
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 커버리지는
  오르는데 결함 발견은 오르지 않은 사람 대상 통제실험

[^zhang2015-assertions]: Zhang & Mesbah 2015, "Assertions Are Strongly Correlated with Test
    Suite Effectiveness", ESEC/FSE 2015, 인쇄 쪽 214~224. **확보본은 저자본이지만 각 쪽
    하단에 인쇄 쪽 번호가 있고 1쪽 하단에 게재 레코드(학회·개최지·ISBN·DOI)가 있어
    locator는 인쇄 쪽이다.** 이 페이지는 초록, 2절의 checked coverage 계보, 3절 실험
    설계 전부(Table 1·2·3), 4절 결과(Table 4·5·6·7·8, Figure 2·3·4의 값과 Finding 1~8),
    5절 논의(5.1~5.4)와 5.5절 타당도 위협, 6절 결론을 담았다. 1절 서론과 2절 선행 연구가
    경유해 전하는 제3자 수치는 옮기지 않았다. Figure 1·2·5의 산점도·상자그림은 이미지라
    본문과 축 표기가 적은 값만 옮겼다. 직인용은 원문 표기 그대로이고 말줄임표(…)만 이
    페이지가 넣었다.

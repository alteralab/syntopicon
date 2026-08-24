---
type: concept
title: 테스트의 바람직한 성질 열둘
description: 테스트가 갖출 만한 성질 열둘을 한 줄 정의로 늘어놓고 그 성질들이 서로 지지하거나 간섭한다고 적은 한 쪽짜리 목록 — 열두 성질의 원문 정의와 이 KB가 고른 역어, 목록을 규범이 아니라 교환 재료로 규정하는 부제, 자동화가 빠름을 돕고 예측력이 빠름을 깎는다는 두 문장, 조합 가능성으로 빠름과 예측력을 함께 얻는다는 겉보기 간섭의 해소, 구조 둔감이 리팩터링 내성과 같은 성질인가의 판정과 두 서술이 서 있는 층의 차이, 행위 민감이 관찰 가능한 행위와 만나는 자리, 그리고 우선순위도 측정 방법도 없다는 이 목록의 한계
generated: { by: "claude-opus-5", at: "2026-08-24T01:20:00Z" }
sources:
  - { id: beck2019-test-desiderata, resource: /it/sources/beck2019-test-desiderata.md }
---

# 테스트의 바람직한 성질 열둘

- [이 소스의 지위](#이-소스의-지위)
- [열두 성질의 문면](#열두-성질의-문면)
- [역어를 이렇게 골랐다](#역어를-이렇게-골랐다)
- [성질은 서로 지지하고 간섭한다](#성질은-서로-지지하고-간섭한다)
- [구조 둔감은 리팩터링 내성과 같은 것인가](#구조-둔감은-리팩터링-내성과-같은-것인가)
- [다른 페이지가 세운 성질 목록과 겹치는 자리](#다른-페이지가-세운-성질-목록과-겹치는-자리)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트의 바람직한 성질(test desiderata) 열둘은 무엇이고, 그것들은 서로
어떻게 지지하고 간섭하는가.**

## 이 소스의 지위

- **근거 등급은 `practitioner-norm`이다.** 실험도 표본도 측정도 없고, 인용할 수 있는
  수치가 하나도 없다. 성질마다 붙은 것은 한 줄 정의뿐이고 근거 절도 참고문헌도 없다.
  **이 페이지의 어느 문장도 학술 근거로 쓰지 않는다.**
- **이 등급은 대장이 정한 것이 아니라 이 반입이 문면을 보고 붙인 것이다.** 이 소스의 대장
  항목에는 `evidence_grade:` 기재가 없다. 판단의 재료는 하나다 — 문서에 측정도 표본도
  참고문헌도 없다는 사실.
- **저자의 자기 규정은 부제 한 줄이 전부다.**[^beck2019-test-desiderata]

  > Optimize the value of your tests by choosing how to tradeoff among various valuable
  > properties.

  - **목록이 규범이 아니라 교환 재료로 규정된다.** `choosing`과 `tradeoff`가 그 자리에
    있고, **어느 성질을 먼저 포기하라는 말은 이 문서 어디에도 없다.**
- **저자 표시(byline)가 문면에 없다.** 이 문서를 Beck에게 귀속시키는 근거는 목록을 소개하는
  문장의 `with Kent Beck and Kelly Sutton`과 말미의 원글 주소 `medium.com/@kentbeck_7670/…`
  둘이다.[^beck2019-test-desiderata]
- **발행 연도도 인쇄돼 있지 않다.** 게시일·갱신일·저작권 줄이 확보본에 없다. 이 KB가
  기록한 2019는 대장 기재와 원글이 2019년 Medium 글이라는 **외부 근거**이지 문면에서 읽은
  값이 아니다.
- **원글 둘과 다섯 분 비디오 열둘은 이 KB가 갖고 있지 않다.** 문서 말미가 원글 둘을
  가리키고 성질마다 영상 주소가 걸려 있으나, **이 반입은 Medium 판을 받지 않았고 어느
  영상도 열지 않았다.** 이 페이지가 보증하는 것은 testdesiderata.com 스냅샷 한 장의
  문면뿐이다.

## 열두 성질의 문면

- **목록을 소개하는 문장이 성질의 지위를 정한다**:[^beck2019-test-desiderata]

  > Here are some properties making tests more valuable (links lead to 5-minute videos
  > describing each property with Kent Beck and Kelly Sutton):

  - **`some properties`다.** 전부라고도, 서로 독립이라고도, 완전한 목록이라고도 적지 않는다.
  - 표제어의 뜻풀이도 한 줄로 붙어 있다 — `Desiderata–things wanted or needed.`
- **정의는 왜곡에 민감하므로 문면 그대로 옮긴다.** 아래 표의 셋째 칸은 확보본의 한 줄
  정의를 그대로 옮긴 것이고, 원문에서 이름과 정의를 잇는 줄표만 뗐다. 둘째 칸의 역어는
  **이 KB가 지은 것**이고 근거는 [다음 절](#역어를-이렇게-골랐다)에 있다.[^beck2019-test-desiderata]

  | 원어 | 이 KB의 역어 | 원문 정의 |
  |---|---|---|
  | Isolated | 격리 | tests should return the same results regardless of the order in which they are run. |
  | Composable | 조합 가능 | I should be able to test different dimensions of variability separately and combine the results. |
  | Deterministic | 결정적 | if nothing changes, the test result shouldn’t change. |
  | Fast | 빠름 | tests should run quickly. |
  | Writable | 쓰기 쉬움 | tests should be cheap to write relative to the cost of the code being tested. |
  | Readable | 읽기 쉬움 | tests should be comprehensible for reader, invoking the motivation for writing this particular test. |
  | Behavioral | 행위 민감 | tests should be sensitive to changes in the behavior of the code under test. If the behavior changes, the test result should change. |
  | Structure-insensitive | 구조 둔감 | tests should not change their result if the structure of the code changes. |
  | Automated | 자동 | tests should run without human intervention. |
  | Specific | 원인 지목 | if a test fails, the cause of the failure should be obvious. |
  | Predictive | 예측력 | if the tests all pass, then the code under test should be suitable for production. |
  | Inspiring | 확신을 줌 | passing the tests should inspire confidence |

  - **마지막 항목만 마침표가 없다.** 확보본의 문면 그대로다.
  - **Writable의 기준이 절대 비용이 아니라 상대 비용이다** — `relative to the cost of the
    code being tested`. 테스트가 싼가가 아니라 **대상 코드에 견주어 싼가**를 묻는다.
  - **Behavioral과 Structure-insensitive가 서로의 뒷면이다.** 하나는 행위가 바뀌면 결과가
    바뀌어야 한다고 하고, 다른 하나는 구조가 바뀌면 결과가 바뀌지 않아야 한다고 한다.
    **이 문서는 둘을 나란한 두 항목으로만 두고 둘의 관계를 적지 않는다.**

## 역어를 이렇게 골랐다

**열둘 가운데 한국어 확립 역어가 있는 것은 하나도 없다.** 그래서 역어는 전부 이 KB의
선택이고, 원어를 지우고 인용하면 이 소스에 귀속시킬 수 없다. 갈릴 만한 것만 근거를 적는다.

- **Behavioral → 행위 민감.** 직역인 "행동적"은 무엇에 대한 것인지가 사라진다. 정의가
  `sensitive to changes in the behavior`이므로 민감의 대상을 역어에 넣었다. 이 KB가
  `behavior`를 **행위**로 옮겨 온 자리(관찰 가능한 행위)와 낱말을 맞췄다.
- **Structure-insensitive → 구조 둔감.** `insensitive`를 "무감각"으로 옮기면 결함처럼
  읽히고, "구조 비의존"은 테스트가 구조를 모른다는 다른 주장이 된다. **Behavioral의
  민감(sensitive)과 짝이 되도록 둔감(insensitive)으로 뒀다** — 원문이 같은 낱말의 앞뒤를
  쓰고 있으므로 역어도 그 대칭을 지켜야 한다.
- **Predictive → 예측력.** "예측적"은 무엇을 예측하는지가 비고, 정의는 **통과가 운영
  적합성을 예측한다**는 뜻이다. 예측의 대상은 테스트가 아니라 프로덕션이다.
- **Inspiring → 확신을 줌.** 직역인 "고무적"은 한국어에서 감정어로 읽혀 정의
  (`inspire confidence`)의 대상인 확신이 사라진다.
- **Specific → 원인 지목.** 직역인 "구체적"은 테스트가 구체적이라는 뜻으로 읽히지만
  정의는 **실패했을 때 원인이 분명해야 한다**는 뜻이다. 이 KB가 다른 페이지에서 같은
  성질을 "실패의 위치를 지목한다"로 옮겨 두었으므로 그 낱말에 맞췄다
  ([종단 테스트를 왜 줄이는가](why-fewer-end-to-end-tests.md)).
- **Isolated → 격리.** 이 낱말은 이 KB 안에서 이미 두 뜻으로 쓰인다. 여기의 격리는
  **테스트끼리의 격리**(실행 순서와 무관한 결과)이지 실패 위치를 좁히는 일이 아니다.
  헷갈리는 자리라 원어를 반드시 함께 적는다.

## 성질은 서로 지지하고 간섭한다

**이 문서가 성질 사이의 관계에 관해 적은 것은 세 문장뿐이고, 그 셋이 이 페이지가 목록보다
중히 다루는 자리다.**[^beck2019-test-desiderata]

- **지지의 사례가 하나 적혀 있다.**

  > Some properties support each other. Automating tests makes them faster to run.

  - 자동(Automated)이 빠름(Fast)을 돕는다는 것이고, **드는 사례는 이 하나뿐이다.**
- **간섭의 사례도 하나뿐이다.**

  > Some properties interfere with each other. Making tests more predictive of production
  > behavior makes them slower.

  - 예측력(Predictive)을 올리면 빠름(Fast)이 깎인다. **왜 그런지는 적히지 않는다** —
    운영에 가까워질수록 실물이 늘고 실물이 늘면 느려진다는 연결은 읽는 쪽이 보태는 것이다.
  - **그 자리에 사례를 대는 페이지가 이 KB에 있다.**
    [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md)이
    그것이고, 데이터베이스를 인메모리(in-memory) 대역으로 바꾸는 것이 빠름을 사고 예측력을
    파는 거래로 읽힌다 — 대역에서는 초록인데 프로덕션에서 깨진 사례가 거기 있다.
    **다만 그쪽 세 소스 가운데 하나는 이 거래의 전제 자체를 부인한다** — 속도 때문에 가짜가
    필요하다는 믿음이 대개 사실이 아니라는 것이다. 곧 **간섭이 있다는 것과 이 자리에서 그
    간섭이 실제로 작동한다는 것은 다른 주장이고, 이 문서는 앞엣것만 적는다.**
- **셋째 문장이 앞의 둘을 뒤집는다.**

  > Sometimes (and this is the magic), properties only seem to interfere. You can use
  > composability to make tests faster *and* more predictive.

  - **`only seem to interfere` — 간섭이 성질 자체의 성질이 아니라 짜는 방식의 결과일 수
    있다는 주장이다.** 조합 가능(Composable)을 쓰면 빠름과 예측력을 함께 얻는다고 적는다.
  - **어떻게 그렇게 되는지의 절차는 없다.** 변이의 축을 따로 시험해 결과를 합친다는 조합
    가능의 정의가 그 자리에 있는 전부이고, 사례도 측정도 붙지 않는다.
  - **`this is the magic`이 저자 자신의 어조 표시다.** 논증이 아니라 요령의 문법으로 적혀
    있다.
- **관계에 관해 이 문서가 말하지 않은 것이 더 많다.** 열두 성질 사이의 쌍은 예순여섯인데
  적힌 것은 셋이고, **나머지 예순셋은 이 문서에 없다.** 성질 사이의 우선순위도 없다.

## 구조 둔감은 리팩터링 내성과 같은 것인가

**이 KB에 같은 방향의 서술이 하나 더 있다.** 이 절은 그 둘이 같은 성질인지 판정한다 —
**결론은 같은 방향의 서술이되 서 있는 층이 다르고, 이 KB는 둘을 동일시하지 않는다.**

| 어디 | 문면 | 무엇을 재는가 |
|---|---|---|
| 이 문서 | tests should not change their result if the structure of the code changes. | 결과의 불변 |
| [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) | the degree to which a test can sustain a refactoring of the underlying application code without turning red | 붉어지는 정도 |

- **문면이 다른 것을 재고 있다.** 이쪽은 결과가 바뀌지 않아야 한다는 **상태의 서술**이고,
  저쪽은 견디는 **정도(degree)**의 서술이다. 저쪽은 한 걸음 더 나가 그 정도를 거짓
  양성(false positive)의 수로 재라고 적고, 거짓 양성의 원인을 구현 세부 결합 하나로
  지목한다. **이 문서에는 거짓 양성이라는 낱말도, 원인의 지목도, 재는 법도 없다.**
- **층이 다르다.** 이 문서는 성질을 열둘 가운데 하나로 나란히 두고 우선순위를 적지 않는데,
  저쪽은 네 속성 가운데 이것 하나만 협상 불가라고 판정한다. **같은 방향의 서술을 두고
  한쪽은 목록의 한 줄로, 다른 쪽은 나머지를 재는 잣대로 쓴다.**
- **둘 다 측정이 없다.** 이쪽은 실무자의 목록이고 저쪽도 근거 등급이 실무 규범이다.
  **두 문서가 같은 말을 한다는 사실은 둘이 옳다는 증거가 아니다** — 같은 실무 전통에서
  나온 두 진술이다.
- **그래서 이 KB는 둘을 하나로 뭉치지 않는다.** 조항이나 게이트에 쓸 때 "구조 둔감 = 리팩터링
  내성"이라고 적으면 이 문서가 하지 않은 주장(협상 불가·이진성·원인 지목)이 함께 딸려
  온다. **인용은 두 문면을 나란히 적는 형태로만 한다.**
- **행위 민감(Behavioral)도 같은 방식으로 다룬다.** 저쪽의 관찰 가능한 행위(observable
  behavior)는 클라이언트의 목표로 정의되는 관계 개념이고, 이쪽의 행위 민감은 **행위가
  바뀌면 결과가 바뀌어야 한다**는 요구다. **접점은 실재하되 정의의 층이 다르다** —
  이쪽은 무엇이 행위인지 정의하지 않는다.
- #hypothesis **두 성질쌍이 서로 대응한다는 읽기가 가능하다.** 행위 민감은 행위 변화를
  놓치지 않는 능력(저쪽의 회귀 방지·거짓 음성 쪽)에, 구조 둔감은 구조 변화에 붉어지지
  않는 능력(저쪽의 리팩터링 내성·거짓 양성 쪽)에 각각 겹친다. **이 대응은 어느 문서도
  적지 않은 이 KB의 읽기이고, 뒷받침하는 측정은 없다.**

## 다른 페이지가 세운 성질 목록과 겹치는 자리

**이 KB에는 같은 형식의 목록이 이미 둘 있다.** 겹치는 자리를 적어 두는 이유는, 낱말이
같은데 가리키는 것이 다른 자리가 있기 때문이다.

- **좋은 피드백 루프의 성질 셋과 겹친다**
  ([종단 테스트를 왜 줄이는가](why-fewer-end-to-end-tests.md)) — 빠르다·믿을 만하다·실패의
  위치를 지목한다. 이 목록의 빠름(Fast)·결정적(Deterministic)·원인 지목(Specific)이 각각
  같은 방향이다.
  - **그러나 그쪽의 `isolates failures`는 이 목록의 격리(Isolated)가 아니다.** 그쪽에서
    좁혀지는 것은 버그가 있을 수 있는 코드의 범위이고, 이 목록의 격리는 **테스트끼리의
    독립**이다. 두 낱말이 같은 뿌리를 쓰므로 섞이기 쉽다.
- **격리와 결정적은 불안정 테스트의 원인 분류와 맞물린다**
  ([불안정 테스트의 원인 분류와 고침](flaky-test-root-causes-and-fixes.md)) — 그쪽의
  Test Order Dependency 범주가 이 목록의 격리를 깨뜨리는 것이고, 비동기 대기와 동시성
  범주가 결정적을 깨뜨리는 것이다. **그쪽은 그 원인들을 세었고 이쪽은 성질의 이름만
  갖는다** — 이 목록을 실제로 지키려면 값은 그쪽에서 가져온다.
- **구조 둔감은 대역 선택의 축과 만난다**
  ([대역 어휘와 두 TDD 스타일](test-double-vocabulary-and-tdd-styles.md)) — 그쪽이 두
  스타일이 갈리는 다섯 축 가운데 하나로 **테스트를 구현에 결합시키는가**를 든다. 목을 쓰는
  쪽이 구현에 더 묶인다는 우려가 그 축의 내용이고, 이 목록의 구조 둔감이 그 우려가 지키려는
  성질이다. **다만 그쪽은 판정을 유보하고 이쪽은 판정할 재료가 없다.**

## 이 소스의 사각

- **우선순위가 없다.** 열둘이 나란히 놓이고 어느 것을 먼저 포기하라는 말이 없다. 부제가
  선택을 읽는 사람에게 넘기므로, **이 목록만으로는 어떤 테스트가 더 나은지 판정할 수 없다.**
- **재는 법이 없다.** 성질마다 정의는 있는데 어떻게 확인하는지가 없다. 빠름의 문턱도,
  읽기 쉬움의 기준도, 예측력을 어떻게 재는지도 적히지 않는다.
- **관계의 서술이 셋뿐이다.** 지지 하나, 간섭 하나, 겉보기 간섭 하나. **나머지 쌍은 비어
  있고** 그 자리를 채우는 마인드맵 그림은 확보되지 않았다.
- **성질의 독립성과 목록의 완전성이 검증되지 않았다.** 문서 자신이 `some properties`라고만
  적는다. 열둘이 왜 열둘인지의 근거가 없다.
- **다섯 분 비디오와 원글 둘이 미확보다.** 성질의 뜻을 좁히는 서술이 그 안에 있을 수 있고
  이 KB는 그것을 모른다. **이 페이지의 서술은 한 줄 정의만을 근거로 한다.**
- **언어 모델 시대의 재검이 없다.** 생성된 테스트가 이 열둘 가운데 어디에서 약한지,
  쓰기 쉬움(Writable)의 비용 비교가 테스트를 기계가 쓸 때도 같은 뜻인지는 이 문서의
  주제가 아니고 이 KB도 그 재검을 갖고 있지 않다.

## 이어지는 페이지

- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) — **이 목록의
  구조 둔감이 잣대로 승격된 자리.** 같은 방향의 서술을 네 속성 가운데 하나로 놓고 협상
  불가라고 판정하며, 그 판정의 근거와 사각을 함께 갖는다
- [종단 테스트를 왜 줄이는가](why-fewer-end-to-end-tests.md) — 성질 셋으로 크기를 고르는
  같은 형식의 목록. 빠름과 예측력의 간섭이 그쪽에서는 크기의 선택으로 나타난다
- [불안정 테스트의 원인 분류와 고침](flaky-test-root-causes-and-fixes.md) — 격리와 결정적을
  깨뜨리는 원인을 세어 놓은 유일한 심사 실증
- [대역 어휘와 두 TDD 스타일](test-double-vocabulary-and-tdd-styles.md) — 구조 둔감을 두고
  두 스타일이 갈리는 자리
- [인메모리 데이터베이스 대역이 잃는 것](what-in-memory-database-doubles-lose.md) —
  **예측력과 빠름의 간섭에 사례를 댄 자리.** 대역이 초록인데 프로덕션이 깨진 실물이 거기
  있고, 동시에 그 거래의 전제(속도 때문에 가짜가 필요하다)를 부인하는 문면도 함께 있다
- [대역과 단위 테스트의 가치](../synthesis/test-doubles-and-unit-test-value.md) — **이 갈래의 허브.** 이 목록의
  구조 둔감과 행위 민감이 대역 갈래의 판정들과 만나는 자리가 거기다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 이 성질들을
  실제 스위트의 배합과 운영으로 옮기는 자리
- **아직 답이 없는 물음 하나** — 열두 성질 사이의 나머지 쌍은 서로 지지하는가 간섭하는가.
  이 문서가 셋만 적었고 이 KB에 그것을 채울 소스가 없다

[^beck2019-test-desiderata]: Beck, "Test Desiderata", testdesiderata.com, **2026-08-20
    확보본**. **쪽 번호도 절 번호도 없는 한 쪽짜리 문서라 locator는 원문 문단이다** —
    부제(`<h2 id="project_tagline">`) · 표제어 뜻풀이 · 목록 소개 문장 · 열두 항목의
    목록 · 지지 문단 · 간섭 문단 · 겉보기 간섭 문단 · 원글 링크 문단. 직인용은 확보본
    문면 그대로이고, 표의 정의 칸에서는 이름과 정의를 잇는 줄표만 뗐다. **저자 표시 줄과
    발행 연도가 문면에 없다** — 귀속과 연도의 근거는
    [소스 메타](../sources/beck2019-test-desiderata.md)가 정본이다. **성질마다 걸린 다섯 분
    비디오와 말미가 가리키는 Medium 원글 둘은 이 KB가 확보하지 않았고, 마인드맵 그림도
    확보본에 없다**(HTML 한 장). 근거 등급과 인용 규약은 같은 소스 메타가 정본이다.

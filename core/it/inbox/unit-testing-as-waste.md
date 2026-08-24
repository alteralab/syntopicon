---
type: concept
title: 단위 테스트는 대부분 낭비인가
description: 단위 테스트 대부분이 낭비라는 주장을 세운 한 편의 에세이와 그 논거가 어디서 무너지는가 — 동료심사 없는 뉴스레터라는 지위와 저자 자신의 한정 문면, 정보 이론과 계산 복잡도와 유지 비용과 심리라는 논거 넷, 같은 주장이 권고형 상자와 단정형 요약 불릿 두 층에서 다른 세기로 적힌 자리, 저자가 값어치를 인정한 예외 셋, 유일한 학술 인용을 반증으로 쓴 대목, 정보 이론 논거가 두 절 사이에서 서로를 무너뜨리는 자리와 그 아래 깔린 절단 표본 문제, 그리고 이 글에서 살아남는 방향 하나
generated: { by: "claude-opus-5", at: "2026-08-24T01:20:00Z" }
status: draft
contradicts: [google-test-sizes-and-suite-operations]
sources:
  - { id: coplien2014-unit-testing-waste, resource: /it/sources/coplien2014-unit-testing-waste.md }
---

# 단위 테스트는 대부분 낭비인가

- [이 소스의 지위와 판](#이-소스의-지위와-판)
- [이 글이 부정하는 것](#이-글이-부정하는-것)
- [논거 넷](#논거-넷)
- [인용 형태가 두 층이다](#인용-형태가-두-층이다)
- [저자가 값어치를 인정한 예외](#저자가-값어치를-인정한-예외)
- [유일한 학술 인용을 어떻게 쓰는가](#유일한-학술-인용을-어떻게-쓰는가)
- [정보 이론 논거가 두 절 사이에서 무너진다](#정보-이론-논거가-두-절-사이에서-무너진다)
- [그래서 무엇이 남는가](#그래서-무엇이-남는가)
- [반대 극과 무엇이 부딪히는가](#반대-극과-무엇이-부딪히는가)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **단위 테스트(unit test) 대부분이 낭비(waste)라는 주장의 논거는 무엇이고, 그
논거는 어디서 무너지는가.**

## 이 소스의 지위와 판

**이 절은 이 페이지의 나머지 전부에 걸리는 단서다.** 아래 문면들을 실증으로 읽으면 이 KB가
갖고 있지 않은 판정을 만들게 된다.

- **근거 등급은 `essay`다.** 실험도 표본도 통제도 없다. 이 글의 숫자는 전부 저자가 본문에서
  세운 어림 계산이거나 예시이며, **이 페이지의 어느 문장도 학술 근거로 쓰지 않는다.**
- **동료심사를 받은 흔적이 문면에 없고 참고문헌 목록도 없다.** 확보본 21쪽에 학회·저널의
  조판 표면(권·호·쪽수·접수 일자)이 한 줄도 없고, 쪽 머리글은 제목 반복 하나뿐이다.
  글 자신이 자기 게재처를 뉴스레터로 부른다 — 독자에게 저자 주소로 의견을 보내고
  `copy Rex at the address at the front of this newsletter` 하라고 적는다(§1.10).
  **그 머리면은 확보본에 들어 있지 않다.**[^coplien2014-unit-testing-waste]
- **저자의 자기 한정이 마지막 절에 있다** (§1.10):[^coplien2014-unit-testing-waste]

  > As for the Internet: it's sad, and frankly scary, that there isn't much out there.
  > There's a lot of advice, but very little of it is backed either by theory, data, or even
  > a model of why you should believe a given piece of advice. Good testing begs skepticism.
  > Be skeptical of yourself: measure, prove, retry. Be skeptical of *me* for heaven's sake.

  - **저자가 요구하는 회의의 대상에 자기 글이 들어 있다.** 이 페이지가 이 글을 논쟁의 한 극
    으로만 두는 근거가 저자 자신의 이 문장이다.
  - **다만 이 문장은 "내 주장에 데이터가 없다"는 자백이 아니다.** 문면이 겨냥하는 것은
    인터넷의 조언 일반이고, 저자가 자기 논거의 실증 부재를 명시적으로 인정한 문장은 확보본
    어디에도 없다. **이 구분을 뭉개면 이 글보다 겸손한 글로 만들어 주는 것이 된다.**
- **원 게재처가 죽었고 아카이브본이 실질 정본이다.** 원 주소는 응답하지 않으며, 확보본은
  마지막 성공 캡처(2023-09-23)와 **바이트 동일**이다. 같은 파일이 2014-09-03부터 그날까지
  9년 동안 바뀌지 않았다. 캡처 목록과 다이제스트 대조는
  [소스 메타](../sources/coplien2014-unit-testing-waste.md)가 소유한다.
- **판이 둘이고 확보본이 뒤엣것이다.** 앞판(2014-02-27 조판, 19쪽)에 없던 §1.9와 100%
  커버리지 정의 문단이 확보본(2014-08-05 조판, 21쪽)에 들어 있다.

## 이 글이 부정하는 것

**부정의 대상은 "테스트"가 아니라 "단위 테스트에 실린 무게"다.** 이 구분을 놓치면 이 글을
테스트 무용론으로 읽게 되고, 그것은 문면과 다르다.

- **테스트가 없어지지 않는다고 이 글이 직접 적는다** (§1.4
  끝):[^coplien2014-unit-testing-waste] `But let's be clear that there will always be bugs.
  Testing will not go away.`
- **자동화 비판이 아니라고도 직접 적는다** (§1.3):[^coplien2014-unit-testing-waste]

  > People confuse automated tests with unit tests: so much so that when I criticise unit
  > testing, people rebuke me for critising automation.

- **옮길 곳을 지목한다** (§1.3):[^coplien2014-unit-testing-waste]

  > You'll probably get better return on your investment by automating integration tests,
  > bug regression tests, and system tests than by automating unit tests.

  같은 방향이 요약 불릿에도 있다 — 값어치가 있는 X를 시스템 테스트로도 단위 테스트로도
  검사할 수 있으면 시스템 테스트를 쓰라는 것이고, 그 문장이
  `context is everything`으로 끝난다(「In summary」).
- **단위 테스트가 남을 자리로 저자가 지목하는 것은 단정(assertion)이다** (§1.8):
  [^coplien2014-unit-testing-waste]

  > When I look at most unit tests — especially those written with JUnit — they are
  > *assertions* in disguise.

  권고 상자는 `Turn unit tests into assertions.`이고, 그 이유를 "실행하는 절반은 스트레스·
  통합·시스템 테스트가 맡으면 된다"로 적는다.

## 논거 넷

**이 글의 주장은 하나인데 논거는 서로 독립인 넷이다.** 하나가 무너져도 나머지가 남으므로
따로 세어 둔다.

- **① 정보 이론** (§1.5).[^coplien2014-unit-testing-waste] 테스트의 목적은 프로그램에 대한
  정보를 만드는 것인데, 늘 통과하는 테스트는 정보를 만들지 않는다.

  > Information is based on probability. If the probability of the test passing is 100%,
  > then there is *no* information — by definition, from information theory.

  - 통과를 1, 실패를 0으로 적은 문자열을 두 개 놓고 견준다 — 전부 1인 문자열과 뒤섞인
    문자열. 뒤엣것에 정보가 훨씬 많고 `the information comes from *failed* tests`라고 맺는다.
  - **테스트가 품질을 올리지 않는다는 문장이 같은 자리에 있다** —
    `Testing does not increase quality; programming and design do.` 요약 불릿의 마지막 줄이
    같은 말이다(`Tests don't improve quality: developers do.`).
- **② 계산 복잡도와 커버리지의 정의** (§1.2·§1.3·§1.6).[^coplien2014-unit-testing-waste]
  저자가 커버리지(code coverage)를 스스로 정의하고, 그 정의 아래에서 어떤 스위트도 무의미한
  비율에 머문다고 논증한다.

  > I define 100% coverage as having examined all possible combinations of all possible
  > paths through all methods of a class, having reproduced every possible configuration of
  > data bits accessible to those methods, at every machine language instruction along the
  > paths of execution. Anything else is a heuristic about which absolutely no formal claim
  > of correctness can be made.

  §1.6에서 같은 정의를 한 줄로 되풀이한다 — 코드 커버리지는
  `the percent of all possible pairs, {Program Counter, System State}`이고 그 밖은 전부
  어림이라는 것이다.
  - **이 정의는 이 글의 것이지 업계의 것이 아니다.** 줄 커버리지·분기 커버리지를 이 정의로
    재면 어느 스위트도 0에 수렴하므로, **이 논거는 커버리지 지표를 반박한 것이 아니라 다른
    낱말로 바꿔 놓은 것이다.**
  - 이 논거에서 나온 수치들은 전부 저자의 어림이다 — 단위 테스트가 메서드 기능의
    `one trillionth` 이상을 검사하기 어렵다는 §1.2의 값은 저자가 괄호에서 가정을 스스로
    밝히고(평균 객체 크기 4워드, 16비트 워드), §1.3의 `1 in 10¹²`(10의 12제곱분의 1)도
    `let's say 10`으로 시작하는 가정 위에 선다. **어느 것도 잰 값이 아니다.**
- **③ 유지 비용과 결합** (§1.7·§1.8).[^coplien2014-unit-testing-waste] 테스트도 모듈이므로
  설계·유지 부담을 함께 진다.

  > The point is that code is part of your system architecture. Tests are modules. That one
  > doesn't deliver the tests doesn't relieve one of the design and maintenance liabilities
  > that come with more modules. … you've introduced coupling — coordinated change —
  > between each module and the tests that go along with it.

  - **테스트도 결함을 담는다는 산수가 §1.7에 있다** — 개발자가 코드 1000줄마다 시스템에
    영향을 주는 결함을 세 개쯤 넣는다고 놓고, 테스트가 코드보다 많으면 진짜 결함이 코드를
    실패시키는 것보다 테스트가 코드를 틀린 결과에 붙잡아 두는 일이 더 잦아진다는 것이다.
    **`about three system-affecting bugs per thousand lines of code`에 출처가 붙어 있지
    않다.** 이 페이지는 이 값을 인용하지 않고, 논증의 형식만 옮긴다.
- **④ 심리와 프로세스** (§1.4·§1.7·§1.9).[^coplien2014-unit-testing-waste] 테스트 분량이
  코드보다 많다는 것은 기술적 사실이기 전에 조직의 증상이라는 것이다.
  - §1.4의 제목이 그 주장이다 — 테스트가 코드보다 똑똑하다는 믿음은 잠재된 두려움이나 나쁜
    프로세스를 알린다. 원인 후보로 정확성에 대한 편집증, 분석 도구·사고 규율의 부재,
    그리고 자주 통합할 수 없게 만든 프로세스를 든다.
  - §1.9의 제목은 `Green Bar Fever`이고, 실패의 양식을 **테스트를 오라클로 삼아 초록 막대를
    목표로 만드는 것**으로 규정한다. 테스트의 두 목적을 배움의 도구와 오라클로 나눈 뒤
    뒤엣것에 빠지면 통찰이라는 진짜 목표를 잃는다고 적는다.

## 인용 형태가 두 층이다

**이 글에서 같은 주장이 두 층에 다른 세기로 적혀 있다.** 본문의 권고 상자(☞)는 권고형이고
말미 「In summary」 불릿은 단정형이다. **한쪽만 옮기면 이 글의 주장 세기를 잘못 전한다** —
단정형만 쓰면 본문의 유보가 사라지고, 권고형만 쓰면 저자가 실제로 단정형으로 요약해 두었다는
사실을 지우게 된다. **이 KB는 둘 다 옮긴다.**

| 주장 | 본문 권고 상자(§) | 말미 요약 불릿 |
|---|---|---|
| 1년 무실패 테스트 | `look at the tests that have never failed in a year and consider throwing them away`(§1.5) | `Throw away tests that haven't failed in a year.` |
| 단정으로의 전환 | `Turn unit tests into assertions. Use them to feed your fault-tolerance architecture on high-availability systems.`(§1.8) | `Turn most unit tests into assertions.` |
| 값어치 판단이 안 되는 테스트 | `If you cannot tell how a unit test failure contributes to product risk, you should evaluate whether to throw the test away`(§1.5) | (요약에 대응 항목 없음) |
| 오라클이 있는 단위 테스트 | `Consider whether the bulk of your unit tests should be those that test key algorithms for which there is a "third-party" oracle for success`(§1.5) | `Keep unit tests that test key algorithms for which there is a broad, formal, independent oracle of correctness, and for which there is ascribable business value.` |

- **차이의 방향이 한결같다.** 본문 쪽은 `consider`·`evaluate whether`·`Consider whether`처럼
  판단을 독자에게 남기고, 요약 쪽은 명령형으로 닫는다. **두 층 사이에 조건절이 탈락한다.**
- **가장 널리 인용되는 문장이 요약 쪽이다.** 이 글을 인용한 글들이 옮기는
  `Throw away tests that haven't failed in a year.`가 그것이고, 그 문장 하나만으로는 저자가
  같은 주장에 붙여 둔 `consider`와 `or at least very little information`이라는 유보를 볼 수
  없다.
- **본문 상자의 전문은 이렇다** (§1.5):[^coplien2014-unit-testing-waste]

  > If you want to reduce your test mass, the number one thing you should do is look at the
  > tests that have never failed in a year and consider throwing them away. They are
  > producing no information for you — or at least very little information. The value of the
  > information they produce may not be worth the expense of maintaining and running the
  > tests. This is the first set of tests to throw away — whether they are unit tests,
  > integration tests, or system tests.

  - **버릴 대상이 단위 테스트로 한정되지 않는다** — 마지막 줄이 세 종류를 다 든다. 이 글을
    "단위 테스트만 버리라"로 읽으면 이 자리에서 어긋난다.
- **요약 불릿이 앞의 것과 겹친다.** 같은 목록의 첫 줄이
  `Keep regression tests around for up to a year — but most of those will be system-level
  tests rather than unit tests.`이므로, **1년이라는 창은 버리라는 기준이면서 동시에 두라는
  기준이다.** 이 글은 그 둘의 관계를 적지 않는다.

## 저자가 값어치를 인정한 예외

**이 글은 단위 테스트를 전부 버리라고 하지 않는다.** 값어치를 인정하는 자리를 스스로 셋
든다. **이 절이 없으면 이 글의 주장을 실제보다 세게 옮기는 것이 된다.**

- **형식 오라클이 있는 핵심 알고리즘** (§1.5).[^coplien2014-unit-testing-waste] 망 라우팅
  알고리즘처럼 API 하나를 상대로 검사할 수 있고 테스트를 이끌어 낼 형식 오라클이 있는
  경우다 — `So those unit tests have value.`
  - **조건이 오라클의 출처다.** 권고 상자가 요구하는 것은 성공 기준이 코드를 쓴 팀 밖에서
    오는 것이고(`rather than one created by the same team that writes the code`),
    그 기준이 `a business mandate`를 반영해야 한다고 적는다. 같은 상자가
    `Of course, an independent evaluation perspective is also important.`로 닫는다.
  - **같은 조건이 §1.2 상자에도 있다** — 단위 테스트가 할 수 있는 일에 겸손하라는 권고에
    `unless you have an extrinsic requirements oracle for the unit under test`라는 예외절이
    붙어 있다.
- **회귀 테스트** (§1.5).[^coplien2014-unit-testing-waste] 실패했을 때 어떤 결함이 돌아온
  것인지 구성상 알 수 있으므로 값어치 물음에 답이 있다. **다만 같은 문장이 그것을 단위
  층에서 쓰는 일은 드물고 대개 시스템 층이라고 적는다.**
- **널 검사 같은 진입 조건 검사** (§1.5).[^coplien2014-unit-testing-waste] 동어반복적인
  테스트가 아니며 `can be very informative`라고 적는다. 다만 그것도 테스트 프레임워크가 아니라
  단정으로 두는 편이 낫다는 단서가 같은 괄호에 붙는다.

**버리라고 든 네 부류도 목록으로 서 있다** — ① 1년 동안 실패하지 않은 것, ② 기능이 바뀌어도
고칠 필요가 없게 짜인 것, ③ 동어반복인 것(tautological), ④ 실패가 어떤 제품 위험에 닿는지
말할 수 없는 것
(§1.5).[^coplien2014-unit-testing-waste] 넷째에 대해 저자는 비용은 실재하고 값어치는 0일 수
있으므로 **순 음의 값어치**(`net negative value`)를 가질 수 있다고 적는다.

## 유일한 학술 인용을 어떻게 쓰는가

**이 글에 학술 문헌 인용은 둘뿐이고, 그 가운데 하나만 자기 주장의 근거로 쓰인다.**

- **문면은 이렇다** (§1.8):[^coplien2014-unit-testing-waste]

  > One technique commonly confused with unit testing, and which uses unit tests as a
  > technique, is Test-Driven Development. People believe that it improves coupling and
  > cohesion metrics but the empirical evidence indicates otherwise (one of several papers
  > that debunk this notion with an empirical basis is Janzen and Saledian, "Does
  > Test-Driven Development Really Improve Software Design Quality?" *IEEE Software* *25*(2),
  > March/April 2008, pp. 77 - 84.)

- **이 글이 그 논문에 부여하는 지위가 문면에 셋 있다** — `the empirical evidence indicates
  otherwise`(실증이 반대를 가리킨다), `one of several papers`(여럿 가운데 하나), 그리고
  `debunk`(통념을 무너뜨린다). **셋 다 반증의 어휘다.**
- **여럿 가운데 하나라고 적었으나 나머지가 없다.** `several papers`라고 쓰고 실제로 든 것은
  이 한 편이며, 참고문헌 목록이 없으므로 나머지를 확인할 길이 문서 안에 없다.
- **`Saledian`은 확보본의 표기 그대로다.** 실제 저자 표기는 Saiedian이고, 이 오식은 앞판과
  확보본 양쪽에 있다.
- **대장 판정** — 이 KB의 재검증 대장은 이 인용을 **오독**으로 판정한다. 그 논문의 긍정
  결과를 생략하고 "확인 실패"를 반증으로 썼다는 것이다. **이 판정의 지위를 이 페이지가
  분명히 해 둔다.**
  - **원 논문(Janzen & Saiedian 2008)을 이 KB가 확보하지 않았다.** 그러므로 위 판정은 원문
    대조로 확인된 것이 아니라 **대장이 내린 판정**이고, 이 페이지가 원문으로 확인한 것은
    Coplien 쪽 문면까지다.
  - **다만 Coplien 쪽 문면만으로도 남는 것이 있다.** `debunk`와 `the empirical evidence
    indicates otherwise`는 그 논문이 반대 결과를 **보였다**는 주장이다. 확인에 실패한 것과
    반대를 보인 것은 다른 사건이고, 이 글은 그 둘을 가르지 않는다.
  - **인용 방향도 어긋난다.** 이 문단이 논증하려는 것은 테스트가 모듈이라 유지 비용이
    든다는 ③ 논거인데, 끌어온 논문의 주제는 TDD가 설계 품질을 개선하는가다. **TDD의 설계
    효과에 대한 결과는 단위 테스트의 유지 비용에 대한 근거가 아니다.**
  - **같은 물음에 대한 실증을 이 KB가 원문으로 갖고 있다** —
    [TDD 효과의 실증](../concepts/empirical-evidence-on-tdd-effects.md)이 그 자리다. 그리고
    **그쪽 논문 하나가 이 문단이 하려는 추론을 명시적으로 금한다** — 순서 차원의 효과가
    관측되지 않았다는 것이 test-last를 권할 근거는 아니며 그러려면 유의한 음의 계수가
    있어야 한다고 적는다. **확인에 실패한 것과 반대를 보인 것이 다르다는 이 절의 판정이
    그쪽에서 논문 자신의 문장으로 되풀이된다.**
- **나머지 인용 하나**(§1.6의 Perry & Kaiser 1990)는 형식 증명의 출처로만 쓰이고 주장의
  실증 근거로 쓰이지 않는다. **둘 다 2차 경유이므로 이 KB는 이 글이 그것을 어떻게 인용했는가
  까지만 쓴다.**

## 정보 이론 논거가 두 절 사이에서 무너진다

**①번 논거가 자기 글 안에서 반박된다.** 두 절이 같은 대상(드물게만 실패하는 테스트)에 정반대
값어치를 매긴다.

- **§1.5의 판정** — 늘 통과하는 테스트는 정보를 만들지 않으므로 가장 먼저 버릴 부류다.
- **§1.6의 판정** (§1.6 첫 문단):[^coplien2014-unit-testing-waste]

  > There is a dilemma here, and that is that in some software, most of the interesting
  > quality data are in the tails of the test result distributions, and conventional
  > approaches to statistics tell you the wrong things. So a test may pass 99.99% of the
  > time but the one test in ten thousand that fails kills you.

  **1만 번에 한 번 실패하는 테스트는 §1.5의 기준으로는 버릴 대상이고 §1.6의 기준으로는
  치명적 결함을 잡는 자리다.** 같은 글의 두 절이 같은 테스트를 두고 갈린다.
- **§1.6이 그 자리에서 고른 처방이 §1.5와 반대 방향이다.** 꼬리의 위험에 대해 이 절이 드는
  답은 테스트를 버리는 것이 아니라 하드웨어 쪽에서 빌려 온 **최악 사례 분석**
  (worst-case analysis, WCA)으로 실패 확률을 임의로 낮추는 설계다.
- **그 아래에 절단 표본 문제가 있다.** §1.5의 논증은 관측된 통과 문자열에서 통과 확률이
  100%라는 결론으로 건너뛰는데, **1년이라는 관측 창은 잘려 있다.** 1만 번에 한 번 실패하는
  테스트가 1년 동안 한 번도 실패하지 않는 일은 §1.6 자신의 예에서 흔한 일이다.
  - **이 글이 그 조건을 스스로 적어 두었다.** §1.5의 괄호가
    `(If the string were infinitely long then there would be exactly zero bits of
    information in each test run.)`이다. **정보량이 0이 되는 것은 문자열이 무한할 때이고,
    유한한 관측에서는 0이 아니다.** 그 유한한 나머지가 §1.6이 말하는 꼬리다.
  - **그러므로 "1년 무실패"는 확률의 관측이 아니라 관측 창의 길이에 대한 진술이다.** 이
    기준으로 버릴 대상을 고르면 실패 확률이 낮은 테스트와 실패 확률이 0인 테스트가 구분되지
    않는다. **앞엣것이 §1.6이 치명적이라고 부르는 바로 그것이다.**
- **#hypothesis 이 모순이 판 사이에서 생겼을 가능성은 낮다.** 확보본과 앞판의 대조에서 §1.5와
  §1.6은 둘 다 앞판에 이미 있었고 두 절 사이에 삽입된 문단이 없다. 다만 이 KB는 저자가 이
  긴장을 인지했는지에 대한 근거를 갖고 있지 않다.

## 그래서 무엇이 남는가

**`verdict: caveat`가 요구하는 결론이다.** 위 절들이 무너뜨린 것을 빼고 나면 이 글에서
살아남는 것은 **방향 하나**다 — 커버리지를 목표로 걸면 무슨 일이 생기는가.

- **저자가 든 사례가 그 방향의 실물이다** (§1.3):[^coplien2014-unit-testing-waste]

  > I had a client in northern Europe where the developers were required to have 40% code
  > coverage for Level 1 Software Maturity, 60% for Level 2 and 80% for Level 3, while some
  > where aspiring to 100% code coverage. … Large functions for which 80% coverage was
  > impossible were broken down into many small functions for which 80% coverage was
  > trivial. This raised the overall corporate measure of maturity of its teams in one year,
  > because you will certainly get what you reward.

  - **이 사례가 보이는 실패 양식은 "수치를 안 채우는 것"이 아니라 "수치를 채우려고 구조를
    바꾸는 것"이다.** 함수가 알고리즘을 감싸기를 그만두고, 실행 순서를 이웃한 줄로 따라갈 수
    없게 된다고 적는다.
  - 권고 상자가 그 처방이다 — 테스트를 돕겠다고 함수를 쪼개고 있으면 시스템 아키텍처와 코드
    이해 가능성을 함께 부수는 것이니 **더 굵은 단위에서 검사하라**는 것이다.
  - 요약 불릿이 같은 것을 유인의 문제로 적는다 —
    `Rewarding coverage or other meaningless metrics can lead to rapid architecture decay.`
- **이 방향은 이 글 밖에서도 서 있다.** 커버리지 수치를 관문·목표로 걸었을 때 사람이 무엇을
  최적화하게 되는가는 이 KB의 커버리지 갈래가 따로 소유하고, 그쪽에는 도구를 만든 사람의
  진단과 대규모 조직의 관찰이 함께 있다 —
  [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) ·
  [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md).
  - **다만 세 문헌이 가리키는 실패 양식이 서로 다르다.** 이 글은 **구조를 부수는 쪽**을,
    산업 권고 쪽은 목표치가 **천장이 되는 쪽**(정한 수치 이상은 하지 않게 된다)을 적는다.
    **같은 방향이되 같은 관찰이 아니므로 하나로 뭉쳐 인용하지 않는다.**
- **살아남지 않는 것도 적어 둔다.** 정보 이론 논거는 위 절에서 자기 글에 반박되고, 계산
  복잡도 논거는 커버리지를 저자 자신의 정의로 바꾼 뒤에만 성립하며, 유지 비용 논거의 수치는
  출처가 없고, 심리 논거는 측정이 아니라 관찰이다. **이 넷 가운데 어느 것도 조항의 근거로
  쓰지 않는다.**

## 반대 극과 무엇이 부딪히는가

**이 페이지는 [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)과
`contradicts`로 묶인다. 이 KB는 이 모순을 해소하지 않는다.**

**부딪히는 축은 셋이고, 각 축에서 양쪽의 문면은 이렇다.**

| 축 | 이 페이지의 극 | 반대 극 |
|---|---|---|
| 단위 테스트의 비중 | 대부분이 낭비이며 시스템 테스트로 옮기라 | `we tend to aim to have a mix of around 80% of our tests being narrow-scoped unit tests` |
| 큰 테스트의 자리 | 값어치가 큰 쪽이 통합·시스템 테스트다 | 큰 테스트는 온전성 검사이고 `they should not be viewed as a primary method for catching bugs` |
| 오래 통과한 테스트 | 1년 무실패면 버릴 첫 부류다 | 회귀를 막는 관문에 계속 두고, 값어치가 사라지는 기준으로 드는 것은 실패 없음이 아니라 **불안정**이다 |

- **모순이 성립하는 이유가 근거의 격이 같아서가 아니다.** 양쪽 다 측정이 아니다 — 이쪽은
  `essay`이고 저쪽은 `industry-norm`이며, 저쪽의 80%도 회사가 잰 값이 아니라 다른 책의
  피라미드에서 온 목표치다(그 계보는 반대 극 페이지가 소유한다). **두 극이 부딪히는 것은
  데이터가 아니라 규범이다.**
- **전제도 갈린다.** 반대 극의 조문은 단일 저장소·전담 소유팀·정적 분석 집행·분산 실행이라는
  규모 조건 위에 서 있고, 이 글의 조문은 한 컨설턴트가 만난 팀들의 사례 위에 선다. **어느
  쪽도 상대의 조건에서 시험되지 않았다.**
- **한 자리에서는 두 극이 같은 말을 한다** — 커버리지 목표치가 사람의 행동을 바꾼다는 관찰이
  양쪽에 다 있다(위 [그래서 무엇이 남는가](#그래서-무엇이-남는가)). **모순이 전면적이지
  않다는 것을 적어 두는 이유는, 전면적이라고 두면 이 접점이 안 보이기 때문이다.**
- **이 KB는 어느 쪽도 정설로 세우지 않는다.** 한쪽만 인용해 "단위 테스트는 낭비다" 또는
  "단위 테스트가 80%여야 한다"로 읽는 것이 이 자리에서 가장 흔한 오독이다.

## 이 소스의 사각

- **측정이 없다.** 이 글이 주장하는 어느 것도 전후 비교나 표본으로 뒷받침되지 않는다. 사례는
  전부 저자가 만난 팀의 일화이고, 그 팀들이 어떤 조직이었는지·몇이었는지가 적혀 있지 않다.
- **`waste`가 정의되지 않는다.** 제목의 낱말이고 린(Lean)·도요타 생산 방식을 끌어오지만
  (§1.3), 무엇을 낭비로 세는지의 정의절이 없다. **비용과 값어치를 견주는 잣대가 없으므로
  "대부분"이라는 양도 검증 가능한 형태가 아니다.**
- **`most`의 분모가 없다.** 제목과 본문이 대부분이라고 적지만, 무엇의 대부분인지(테스트 수·
  실행 시간·유지 공수)가 어디에도 없다.
- **반대편 문헌을 다루지 않는다.** 단위 테스트를 옹호하는 쪽의 논거를 인용해 반박하는 자리가
  없다. 인용되는 유일한 학술 논문은 TDD에 대한 것이고 그것도 위 절에서 본 대로다.
- **언어 모델 시대의 재검이 이 논쟁의 양 극 모두에 없다.** 이 글은 2014년, 반대 극의 책은
  2020년이고, 둘 다 생성된 테스트를 다루지 않는다. **이 글의 ③ 논거는 사람이 테스트를 손으로
  고친다는 전제 위에 서므로 그 전제가 흔들리면 논거의 무게도 달라지는데, 이 KB는 그것을 잰
  자료를 갖고 있지 않다.** 이 쌍은 진리 주장이 아니라 논쟁으로 보존된다.
- **원 게재처가 죽어 대조할 현행판이 없다.** 저자가 뒤에 생각을 바꿨는지를 이 소스로 말할 수
  없다.

## 이어지는 페이지

- [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)
  — **`contradicts` 상대 극.** 단위 테스트를 다수로 두라는 쪽의 문면과 그 비중이 측정이 아니라
  목표치라는 판정이 거기 있다. 위 [반대 극과 무엇이 부딪히는가](#반대-극과-무엇이-부딪히는가)의
  표가 그 대조를 소유한다
- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) —
  **같은 현상을 반대 부호로 읽는 자리.** 이 글은 §1.5에서 기능이 바뀌어도 고칠 필요가 없게 짜인
  테스트를 두고 `the tests weren't testing the functionality`라고 판정하는데, 그쪽은 구조가
  바뀌어도 붉게 뜨지 않는 성질을 협상 불가의 미덕으로 세운다. **두 판정이 겨냥하는 변화가
  다르다** — 이 글은 기능의 변화를, 그쪽은 구현 세부의 변화를 말한다. 그 구분을 놓치면 두
  문장이 정면으로 충돌하는 것처럼 보인다
- [대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md) — 이 글이
  §1.1에서 목(mock)을 단위 테스트가 문맥을 지어내는 장치로 규정하고 §1.8에서 TDD를 비판
  대상으로 드는데, 그 두 낱말의 지형이 거기 있다. **이 글은 클래시컬·모키스트의 갈림을 다루지
  않고 둘 다에 걸리는 비판을 한다**
- [테스트의 바람직한 성질 열둘](../concepts/test-desiderata.md) — 같은 판정이 목록의 한 줄로
  놓인 자리. 그쪽의 행위 민감(Behavioral)이 "행위가 바뀌면 테스트 결과가 바뀌어야 한다"이고,
  이 글 §1.5의 반사례가 그 성질이 없는 테스트의 실물이다. 그쪽의 예측력(Predictive)과 이 글
  §1.5의 "통과는 정보가 아니다"도 같은 물음의 두 답이다
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 이 글에서
  살아남는 방향이 실무자 원전으로 서 있는 자리. **관찰이 겹치지 않고 갈린다** — 이 글은 목표를
  채우려고 구조를 쪼개는 쪽을, 그쪽은 도구가 명령이 되면 정보원이기를 그만두는 쪽을 적는다
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 같은 방향을
  대규모 조직의 문면으로 적은 자리. 목표치가 바닥이 아니라 천장이 된다는 관찰이 이 글의
  구조 붕괴 관찰과 다른 실패 양식이다
- [테스트 오라클](../concepts/test-oracle.md) — **이 글이 단위 테스트의 값어치에 붙인 유일한
  조건.** 형식 오라클이 있으면 값어치가 있고 없으면 프로그래머의 짐작이라는 것이 §1.3과 §1.5의
  판정이고, 그 오라클이 어디서 오는가를 그쪽이 소유한다
- [종단 테스트를 왜 줄이는가](../concepts/why-fewer-end-to-end-tests.md) — **정반대 방향의
  처방이 같은 회사 문헌으로 서 있는 자리.** 이 글은 시스템 테스트로 무게를 옮기라 하고 그쪽은
  종단 테스트를 줄이라 한다. 두 글이 드는 근거가 다른 축이라는 것(이쪽은 값어치와 오라클,
  그쪽은 피드백 루프의 성질)이 대조의 자리다
- [대역과 단위 테스트의 가치](../synthesis/test-doubles-and-unit-test-value.md) — **이 갈래의 허브.** 이 글이 한
  극으로 서는 논쟁과 그 중재항이 거기 모여 있다
- [테스트 스위트의 적절성](../synthesis/test-suite-adequacy.md) — 이웃 허브. 커버리지를 무엇으로
  읽을 것인가의 갈래가 거기 있고, 이 글의 커버리지 정의는 그 갈래의 어느 지표와도 같은 눈금이
  아니다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 어떤 크기를 얼마나
  둘 것인가의 갈래이고, 이 페이지의 `contradicts` 상대가 거기 서 있다
- [테스팅에서 자동화의 경계](../synthesis/automation-boundary-in-testing.md) — 이웃 허브. 이 글이
  §1.3에서 지적 작업의 자동화에 반대하는 근거로 도요타 생산 방식을 들고 사람을 고리 안에 두는
  예로 탐색적 테스팅을 드는 자리가 그 축에 닿는다
- [TDD 효과의 실증](../concepts/empirical-evidence-on-tdd-effects.md) — **이 글이 §1.8에서
  학술 논문 한 편으로 하려던 일을 이 KB가 원문 셋으로 하는 자리.** 이 글의 논거가 아니라
  TDD의 순서라는 축에 대한 측정이 거기 있고, **그 측정의 문면은 이 글이 원하는 형태가
  아니다** — 순서의 효과가 관측되지 않았다는 것을 test-last 우위로 읽지 말라고 논문이
  직접 못 박는다. 이 글의 ③·④ 논거와는 만나지 않는다(그 실증들은 유지 비용도 조직 심리도
  재지 않는다)
- **아직 답이 없는 물음 하나** — **단위 테스트의 비중**을 바꾸면 결함 검출이나 유지 비용이
  어떻게 되는지를 잰 자료가 이 KB에 없다. 위 실증 셋은 비중이 아니라 **과정**을 재므로 이
  물음에 답하지 않는다

[^coplien2014-unit-testing-waste]: Coplien 2014, "Why Most Unit Testing is Waste",
    2026-08-24 아카이브본. **확보본은 인터넷 아카이브의 마지막 성공 캡처(2023-09-23)와 바이트
    동일이고, 원 게재처(rbcs-us.com)는 응답하지 않는다.** 확보본에 쪽 번호가 인쇄돼 있지 않아
    locator는 절 번호와 절 제목이다 — §1.1 `Into Modern Times` · §1.2 `The Cure is Worse than
    the Disease` · §1.3 `Tests for their Own Sake and Designed Tests` · §1.4 `The Belief that
    Tests are Smarter than Code Telegraphs Latent Fear or a Bad Process` · §1.5 `Low-Risk
    Tests Have Low (even potentially negative) Payoff` · §1.6 `Complex Things are
    Complicated` · §1.7 `Less is More, or: You are Not Schizophrenic` · §1.8 `You Pay for
    Tests in Maintenance — and Quality!` · §1.9 `"It's the process, stupid," or: Green Bar
    Fever` · §1.10 `Wrapup` · 말미 「In summary」. 직인용은 확보본 문면 그대로이고 말줄임표(…)만
    이 페이지가 넣었다. 본문 권고 상자의 원문 조판은 화살표 기호(☞)와 기울임체이며, 이 페이지는
    기호만 옮기고 기울임 조판은 옮기지 않았다. `1 in 10¹²`의 원문 조판은 위 첨자이고 텍스트
    추출에서 `1012`로 눌린다 — 이 페이지의 표기는 조판을 복원한 것이다. 근거 등급·게재처 상태·
    판 대조·참고문헌 상태·인용 규약은 [소스 메타](../sources/coplien2014-unit-testing-waste.md)가
    정본이다.

---
type: concept
title: 리팩터링 내성과 거짓 양성
description: 좋은 단위 테스트의 네 속성 가운데 리팩터링 내성 하나만 협상 불가인 이유와 그 근거 — 리팩터링 내성의 정의, 거짓 양성이 스위트를 무엇으로 부수는가의 두 경로, 거짓 양성의 유일한 원인으로 지목된 구현 세부 결합, 관찰 가능한 행위와 구현 세부를 가르는 두 조건, 두 속성이 각각 1종 오류와 2종 오류를 맡는 대칭, 앞의 세 속성이 상호 배타라는 판정과 그 세 극단 사례, 협상 불가의 근거가 이진성이라는 논증, 그리고 거기서 나오는 블랙박스 기본값
generated: { by: "claude-opus-5", at: "2026-08-23T22:00:00Z" }
sources:
  - { id: khorikov2020-unit-testing, resource: /it/sources/khorikov2020-unit-testing.md }
---

# 리팩터링 내성과 거짓 양성

- [이 소스의 지위와 판](#이-소스의-지위와-판)
- [좋은 단위 테스트의 네 속성](#좋은-단위-테스트의-네-속성)
- [리팩터링 내성의 정의](#리팩터링-내성의-정의)
- [거짓 양성이 부수는 것](#거짓-양성이-부수는-것)
- [거짓 양성의 원인은 하나로 지목된다](#거짓-양성의-원인은-하나로-지목된다)
- [관찰 가능한 행위와 구현 세부](#관찰-가능한-행위와-구현-세부)
- [두 속성이 각각 맡는 오류](#두-속성이-각각-맡는-오류)
- [앞의 셋은 상호 배타다](#앞의-셋은-상호-배타다)
- [왜 협상 불가인가](#왜-협상-불가인가)
- [거기서 나오는 기본값](#거기서-나오는-기본값)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트가 코드를 부수지 않은 변경에 붉게 뜨는 일은 왜 다른 결함들과 달리
타협의 대상이 아닌가.**

## 이 소스의 지위와 판

- **근거 등급은 `practitioner-norm`이다.** 이 책에는 실험도 표본도 측정도 없고, 인용할 수
  있는 수치가 하나도 없다. 논거의 재료는 저자의 현장 경험과 정의로부터의 추론이다.
  **이 페이지의 판정들은 학술 근거가 아니라 실무 규범으로 읽는다.**
- **저자의 자기 규정은 "정밀하고 과학적인 정의"다** (1장 §1.1 "The current state of unit
  testing"):[^khorikov2020-unit-testing]

  > This book takes you there. It teaches a precise, scientific definition of the ideal
  > unit test.

  - **"과학적"이라는 낱말이 가리키는 것은 정의의 성격이지 측정이 아니다.** 이 책에는 그
    정의를 검증한 실험이 없고, 저자 자신이 네 속성에 대해
    **"it's impossible to measure these attributes precisely"**라고 적는다
    (4장 §4.4).[^khorikov2020-unit-testing]
  - 방법에 관한 저자의 유일한 다른 자기 규정은 4부 도입의 한 문장이다 (11장 도입):
    **"Most of these topics follow from the first principles described in part 2."** —
    4부의 반패턴이 2부의 원칙에서 따라 나온다는 국소적 진술이고, 책 전체를 제1원리에서
    연역했다는 선언이 아니다.[^khorikov2020-unit-testing]
- **확보본은 MEAP V03이지 최종 인쇄판이 아니다.** 표지가 `MEAP VERSION 3`을 인쇄하고
  판권면이 없어 **ISBN도 발행 연도도 문면에 없다.** 본문은 1~11장 전부를 담고 결락 장은
  없다. **최종 인쇄판과 대조하지 않았다** — 이 페이지가 보증하는 것은 이 스냅샷의 문면뿐이다.
  판 확인의 근거와 절차는 [소스 메타](../sources/khorikov2020-unit-testing.md)가 정본이다.
- **참고문헌 목록은 없고 본문 각주는 있다.** 확보본에 bibliography도 index도 없지만, 본문에
  번호 각주로 출처를 지목하는 자리가 있다(5장 각주 [2] Meszaros, 9장 각주 [5] Freeman &
  Pryce, 9장 각주 [6] Evans). **"출처 없이 쓴 책"이라고 적으면 틀린다** — 없는 것은
  목록이고, 이 소스의 등급을 정하는 것은 목록의 부재가 아니라 측정의 부재다.
- **언어 모델 시대의 정량 재검이 없다.** 아래 [이 소스의 사각](#이-소스의-사각)에 적는다.

## 좋은 단위 테스트의 네 속성

- **네 속성이 이 책의 기준틀이고, 단위 테스트에만 걸리는 것이 아니다**
  (4장 §4.1):[^khorikov2020-unit-testing]

  > A good unit test has the following four attributes:
  >
  > Protection against regressions
  >
  > Resistance to refactoring
  >
  > Fast feedback
  >
  > Maintainability
  >
  > These four attributes are foundational. You can use them to analyze any automated
  > test, be it unit, integration, or end-to-end.

  한국어 대응은 회귀 방지(protection against regressions)·리팩터링 내성(resistance to
  refactoring)·빠른 피드백(fast feedback)·유지보수성(maintainability)이다.
- **네 속성은 더해지지 않고 곱해진다** (4장 §4.4) — 저자가 값 추정을
  `Value estimate = [0..1] * [0..1] * [0..1] * [0..1]`로 적고, **"if a test gets zero in
  one of the attributes, its value turns to zero as well"**이라고 못 박는다. 하나가 0이면
  전체가 0이라는 이 규칙이 뒤의 모든 판정을 끌고 간다.[^khorikov2020-unit-testing]
  - **이것은 계산이 아니라 비유다.** 같은 절에서 저자가 정밀 측정의 불가능을 스스로
    적는다. 이 소스에 기대어 어떤 점수도 수치로 적을 수 없다.
- **회귀 방지는 실행되는 코드의 양·복잡도·도메인 중요도로 잰다** (4장 §4.1.1) — 그래서
  자명한 코드(한 줄짜리 속성 같은 것)를 덮는 테스트는 회귀를 잡을 여지가 거의 없고,
  프로젝트가 쓰는 라이브러리·프레임워크·외부 시스템까지 테스트 범위에 들어와야 그 가정이
  맞는지 확인된다고 적는다.[^khorikov2020-unit-testing]
- **유지보수성은 앞의 셋과 상관되지 않는다** (4장 §4.4.5) — 예외가 종단 테스트뿐이다.
  유지보수성은 **테스트를 이해하기 어려운 정도**와 **테스트를 돌리기 어려운 정도** 둘로
  나뉜다(4장 §4.3).[^khorikov2020-unit-testing]

## 리팩터링 내성의 정의

- **정의는 왜곡에 민감하므로 문면 그대로 옮긴다** (4장 §4.1.2):[^khorikov2020-unit-testing]

  > The second attribute of a good unit test is resistance to refactoring — the degree to
  > which a test can sustain a refactoring of the underlying application code without
  > turning red (failing).

- **리팩터링의 정의가 그 옆에 붙어 있다** (4장 정의 4.1):[^khorikov2020-unit-testing]

  > Refactoring means changing existing code without modifying its observable behavior.
  > The intention is usually to improve the code's nonfunctional characteristics: increase
  > readability and reduce complexity.

  - **두 정의가 맞물려 있다는 것이 이 개념의 구조다.** 리팩터링이 관찰 가능한 행위를
    바꾸지 않는 변경이라면, 관찰 가능한 행위만 검사하는 테스트는 정의상 리팩터링에 깨질 수
    없다. **리팩터링 내성은 별도의 기법이 아니라 무엇을 검사하느냐의 귀결이다.**
- **거짓 양성(false positive)의 정의도 같은 자리에 있다**
  (4장 §4.1.2):[^khorikov2020-unit-testing]

  > This situation is called a false positive. A false positive is a false alarm. It's a
  > result indicating that the test fails, although in reality, the functionality it
  > covers works as intended.

- **재는 법은 세는 것이다** (같은 절) — **"you need to look at how many false positives the
  test generates. The fewer, the better."**[^khorikov2020-unit-testing] 다만 이 책은 그
  수를 실제로 센 적이 없다.

## 거짓 양성이 부수는 것

- **저자가 테스트의 이득을 둘로 적고, 거짓 양성이 그 둘을 각각 무너뜨린다고 논증한다**
  (4장 §4.1.2). 이득은 ① 기존 기능을 깨뜨렸을 때의 조기 경보와 ② 변경이 회귀를 낳지 않는다는
  확신이다.[^khorikov2020-unit-testing]
- **첫째 경로는 둔감화다** (같은 절):[^khorikov2020-unit-testing]

  > If tests fail with no good reason, they dilute your ability and willingness to react
  > to problems in code. Over time, you get accustomed to such failures and stop paying as
  > much attention. After a while, you start ignoring legitimate failures, too, allowing
  > them to slip into production.

- **둘째 경로는 신뢰 상실이고, 그 결과가 리팩터링의 중단이다** (같은 절) — 거짓 경보가
  잦으면 스위트를 믿을 만한 안전망으로 보지 않게 되고, **"This lack of trust leads to fewer
  refactorings, because you try to reduce code changes to a minimum in order to avoid
  regressions."**[^khorikov2020-unit-testing]
- **저자가 이 두 경로가 실제로 이어지는 것을 본 사례로 곁글 하나를 든다**
  (4장 곁글 "A story from the trenches") — 거짓 경보가 다수인 스위트에서 개발자들이 실패를
  무시하고 테스트를 비활성화했고, 그러다 실제 버그를 잡아낸 테스트 하나도 함께 꺼져 있어
  결함이 운영에 나갔다는 이야기다. **근거는 저자 개인의 경험 진술이다.**[^khorikov2020-unit-testing]
  - **저자가 거기서 끌어내는 처방이 "리팩터링을 멈춰라"가 아니다** (같은 곁글) —
    **"The correct response is to re-evaluate the test suite and start reducing its
    brittleness."**[^khorikov2020-unit-testing]
- **시간축이 붙는다** (4장 §4.2.2) — 프로젝트 초기에는 거짓 양성이 거짓 음성만큼 나쁘지
  않고, 프로젝트가 자라면서 같은 무게가 된다. 이유는 리팩터링의 필요 자체가 시간이 지나야
  생기기 때문이다. 저자가 대부분의 개발자가 회귀 방지에만 집중하는 이유도 여기서
  설명한다 — **후기 단계까지 가는 프로젝트가 훨씬 적어서** 사람들이 그 분포에 맞춰
  최적화한다는 것이다.[^khorikov2020-unit-testing]

## 거짓 양성의 원인은 하나로 지목된다

- **원인도 처방도 한 문장이다** (4장 §4.1.3):[^khorikov2020-unit-testing]

  > The number of false positives a test produces is directly related to the way the test
  > is structured. The more the test is coupled to the implementation details of the
  > system under test (SUT), the more false alarms it generates. The only way to reduce
  > the chance of getting a false positive is to decouple the test from those
  > implementation details.

  - **`The only way` — 이 책이 다른 원인을 인정하지 않는 자리다.** 거짓 양성은 구조
    결합의 증상이고, 줄이는 길은 결합을 끊는 것 하나뿐이라고 적는다.
- **판정 기준은 "최종 결과인가 거기 이르는 단계인가"다** (같은 절) — 테스트는 대상
  시스템이 내놓는 최종 결과, 곧 관찰 가능한 행위를 검사해야 하고 거기 이르는 단계를
  검사하면 안 된다. **"Tests should approach SUT verification from the end user's point of
  view and check only the outcome meaningful to that end user."**[^khorikov2020-unit-testing]
- **저자가 같은 대상을 두 방식으로 검사해 대조한다** (4장 §4.1.3~§4.1.4) — 메시지를 HTML로
  렌더하는 클래스에 대해, 하위 렌더러들의 구성과 순서를 단언하는 테스트와 렌더 결과 문자열을
  단언하는 테스트다. 앞엣것은 하위 렌더러를 동등한 다른 구현으로 바꾸면 결과가 같은데도
  붉어지고, 뒤엣것은 그렇지 않다.[^khorikov2020-unit-testing]
  - **저자가 드는 가장 극단적인 사례는 소스 코드 문자열 자체를 단언하는 테스트다**
    (4장 목록 4.3) — 그리고 그것이 앞의 구조 단언 테스트와 **본질이 다르지 않다**고 적는다.
    **"it's not that different from the test I brought up earlier. Both insist on a
    particular implementation without taking into consideration the SUT's observable
    behavior."** 다른 것은 깨지는 빈도뿐이다.[^khorikov2020-unit-testing]
  - **거짓 양성이 0이 되지는 않는다** (4장 §4.1.4) — 결과만 검사해도 메서드 시그니처가
    바뀌면 컴파일 오류가 나고 그것도 엄밀히는 거짓 양성이다. 다만 저자가 둘을 가른다:
    컴파일러가 잡아 주는 거짓 양성은 고치기 쉽고, **"The worse false positives are those
    that don't lead to compilation errors."**[^khorikov2020-unit-testing]

## 관찰 가능한 행위와 구현 세부

- **정의가 두 조건의 선언(disjunction)이다** (5장 §5.2.1):[^khorikov2020-unit-testing]

  > For a piece of code to be part of the system's observable behavior, it has to do one
  > of the following things:
  >
  > Expose an operation that helps the client achieve one of its goals. An operation is a
  > method that performs a calculation or incurs a side effect or both.
  >
  > Expose a state that helps the client achieve one of its goals. State is the current
  > condition of the system.
  >
  > Any code that does neither of these two things is an implementation detail.

- **판정이 코드의 성질이 아니라 관계에 달려 있다** (같은 절) — **"whether the code is
  observable behavior depends on who its client is and what the goals of that client
  are."**[^khorikov2020-unit-testing] **같은 메서드가 클라이언트가 바뀌면 분류가 바뀐다**는
  뜻이고, 이것이 이 정의를 기계 검사로 옮기기 어렵게 만드는 자리다.
- **공개 여부와는 다른 축이다** (5장 §5.2.1) — 공개 API 대 비공개 API가 한 축이고 관찰
  가능한 행위 대 구현 세부가 다른 축이다. 둘이 어긋나면 **구현 세부가 공개 API로 새어
  나온 것**(leaking implementation details)이고, 잘 설계된 API는 둘이 겹친다.[^khorikov2020-unit-testing]
- **한쪽 방향으로만 어긋난다** (5장 §5.2.4) — **"there's no such problem as leaking
  observable behavior"**. 관찰 가능한 행위를 감추면 그것은 정의상 더 이상 관찰 가능한 행위가
  아니게 되기 때문이다.[^khorikov2020-unit-testing]
- **그래서 좋은 API가 좋은 테스트를 강제한다** (5장 §5.2.4) — 구현 세부를 전부 비공개로
  두면 테스트에 남는 선택지가 관찰 가능한 행위뿐이다. 저자가 이것을 한 줄로 적는다:
  **"Making the API well-designed automatically improves unit tests."**[^khorikov2020-unit-testing]
  - 어림 규칙 하나가 붙는다 (5장 §5.2.2) — 하나의 목표를 이루는 데 클라이언트가 그 클래스에
    걸어야 하는 연산이 둘 이상이면 구현 세부가 새고 있을 가능성이 크다. 저자가 이것을
    자기 경험에 기댄 어림이라고 밝히고 예외가 있을 수 있다고 적는다.[^khorikov2020-unit-testing]

## 두 속성이 각각 맡는 오류

- **회귀 방지와 리팩터링 내성이 통계의 두 오류에 각각 대응한다**
  (4장 §4.2.1) — 회귀 방지는 거짓 음성(2종 오류)을, 리팩터링 내성은 거짓 양성(1종 오류)을
  줄인다.[^khorikov2020-unit-testing]
- **둘이 합쳐 정확도(accuracy)를 이룬다** (같은 절):[^khorikov2020-unit-testing]

  > The accuracy metric itself consists of two components:
  >
  > How good the test is at indicating the presence of bugs (lack of false negatives, the
  > sphere of protection against regressions)
  >
  > How good the test is at indicating the absence of bugs (lack of false positives, the
  > sphere of resistance to refactoring)

  - **결함의 존재를 가리키는 능력과 부재를 가리키는 능력이 다르다**는 이 구분이 이 절의
    핵심이고, 두 능력이 서로 다른 속성의 관할이라는 것이 이 책의 배치다.
- **저자가 이것을 신호 대 잡음(signal-to-noise)으로 다시 적는다** (같은 절) — 정확도를
  올리는 길이 둘이다. 분자인 신호를 키우거나(결함을 더 잘 찾게 하거나) 분모인 잡음을
  줄이거나(거짓 경보를 덜 내게 하거나). **"There's no use for a test that isn't capable of
  finding any bugs, even if it doesn't raise false alarms."**[^khorikov2020-unit-testing]
  - **비유는 독감 검사다** (같은 절) — 양성이 좋다는 뜻이 아니라 검사가 반응하도록 설정된
    조건이 참이라는 뜻이라고 저자가 낱말을 풀어 둔다.[^khorikov2020-unit-testing]

## 앞의 셋은 상호 배타다

- **이상적인 테스트는 만들 수 없다** (4장 §4.4.1):[^khorikov2020-unit-testing]

  > Unfortunately, it's impossible to create such an ideal test. The reason is that the
  > first three attributes — protection against regressions, resistance to refactoring,
  > and fast feedback — are mutually exclusive. It's impossible to maximize them all: you
  > have to sacrifice one of the three in order to max out the remaining two.

- **셋 중 둘을 최대로 올린 사례 셋을 저자가 든다** (4장 §4.4.2~§4.4.4):[^khorikov2020-unit-testing]

  | 극단 | 얻는 둘 | 잃는 하나 |
  |---|---|---|
  | 종단 테스트(end-to-end test) | 회귀 방지 · 리팩터링 내성 | 빠른 피드백 |
  | 자명한 테스트(trivial test) | 리팩터링 내성 · 빠른 피드백 | 회귀 방지 |
  | 깨지기 쉬운 테스트(brittle test) | 회귀 방지 · 빠른 피드백 | 리팩터링 내성 |

  - **곱셈 규칙 때문에 셋 다 값이 0에 가깝다**는 것이 이 표의 요지다. 두 개를 최대로
    올리는 일 자체는 쉽고, 그래서 쉬운 것이 답이 아니다.[^khorikov2020-unit-testing]
  - **깨지기 쉬운 테스트의 사례가 실행된 SQL 문자열을 단언하는 테스트다** (4장 목록 4.6) —
    같은 결과를 내는 SQL 변형 넷을 나란히 적어 두고, 어느 것으로 바꿔도 기능은 그대로인데
    테스트는 붉어진다는 것을 보인다.[^khorikov2020-unit-testing]
  - **자명한 테스트가 극단으로 가면 항진 테스트(tautology test)가 된다** (4장 §4.4.3) —
    언제나 통과하도록 짜였거나 의미 없는 단언만 담은 테스트다.[^khorikov2020-unit-testing]
- **CAP 정리와의 유비를 저자가 스스로 든다** (4장 곁글 "The CAP theorem") — 셋 중 둘의
  교환이라는 점과, 셋 가운데 하나(분할 내성)가 큰 규모에서는 협상 불가라는 점 둘이
  닮았다는 것이다. #hypothesis **이 유비는 설명 장치이지 논증이 아니다** — CAP는 증명된
  정리이고 이 책의 삼각은 정의와 경험에서 온 주장이다. 이 책이 그 차이를 적지 않는다.

## 왜 협상 불가인가

- **판정 문장 자체를 옮긴다** (4장 §4.4.5):[^khorikov2020-unit-testing]

  > In reality, though, resistance to refactoring is non-negotiable. You should aim at
  > gaining as much of it as you can, provided that your tests remain reasonably quick and
  > you don't resort to the exclusive use of end-to-end tests. The trade-off, then, comes
  > down to the choice between how good your tests are at pointing out bugs and how fast
  > they do that.

- **근거는 이진성이다** (같은 절):[^khorikov2020-unit-testing]

  > The reason resistance to refactoring is non-negotiable is that whether a test
  > possesses this attribute is mostly a binary choice: the test either has resistance to
  > refactoring or it doesn't. There are almost no intermediate stages in between. Thus
  > you can't concede just a little resistance to refactoring: you'll have to lose it all.
  > On the other hand, the metrics of protection against regressions and fast feedback are
  > more malleable.

  - **논증의 형태가 "더 중요하다"가 아니라 "조금씩 양보할 수 없다"이다.** 회귀 방지와
    빠른 피드백은 슬라이더로 서술되고, 리팩터링 내성만 스위치로 서술된다. 곱셈 규칙과
    합쳐지면 결론이 나온다 — 스위치가 꺼지면 곱이 0이다.
  - **`mostly`와 `almost no`가 저자 자신의 헤지다.** 이 판정은 예외 없는 정리가 아니라
    거의 언제나 그렇다는 관찰로 적혀 있고, 그 관찰을 뒷받침하는 측정은 이 책에 없다.
  - 5장이 같은 판정을 되풀이하며 한 겹 더 붙인다 (5장 §5.2) —
    **"Compromising on this metric renders the test nearly worthless."**(5장 §5.4)
    그리고 그 최대화에 상한을 둔다: **단위 테스트의 영역에 머무는 한에서** 최대화하라는
    것이다. 종단 테스트가 리팩터링 내성이 가장 좋지만 유지하기 훨씬 어렵기 때문이다.[^khorikov2020-unit-testing]
- **우선순위로도 한 줄 적힌다** (4장 §4.4.5 팁) — **"Eradicating brittleness (false
  positives) in tests is the first priority on the path to a robust test
  suite."**[^khorikov2020-unit-testing]

## 거기서 나오는 기본값

- **블랙박스가 기본값이 된다** (4장 §4.5.2):[^khorikov2020-unit-testing]

  > As you may remember from section 4.4.5, you can't compromise on resistance to
  > refactoring: a test either possesses resistance to refactoring or it doesn't.
  > Therefore, choose black-box testing over white-box testing by default.

  - **예외가 하나 적혀 있다** (같은 절) — 알고리즘 복잡도가 높은 유틸리티 코드다.
  - **역할이 갈린다** (같은 절) — **"Use the black-box testing method when writing tests.
    Use the white-box method when analyzing the tests."** 커버리지 도구로 안 밟힌 가지를
    찾되, 그것을 덮는 테스트는 내부 구조를 모르는 척 쓰라는 것이다.[^khorikov2020-unit-testing]
  - **추적 가능성이 판정 도구로 쓰인다** (같은 절) — 테스트를 업무 요구로 되짚을 수 없으면
    그것이 깨지기 쉽다는 신호이고, 고치거나 지우라고 적는다.[^khorikov2020-unit-testing]
- **피라미드의 어느 층도 리팩터링 내성을 양보하지 않는다** (4장 §4.5.1):[^khorikov2020-unit-testing]

  > Notice that neither layer gives up resistance to refactoring. Naturally, end-to-end
  > and integration tests score higher on this metric than unit tests, but only as a side
  > effect of being more detached from the production code. Still, even unit tests should
  > not concede resistance to refactoring.

  - **이 책이 피라미드를 네 속성의 귀결로 다시 읽는다** (같은 절) — 층마다 다른 것은
    회귀 방지와 빠른 피드백 사이의 선택뿐이라는 것이다. 배합 비율의 수치는 이 책에 없고
    **"end-to-end tests should be the minority; unit tests, the majority"**라는 방향만
    적힌다.[^khorikov2020-unit-testing]
  - **예외 둘도 적힌다** (같은 절) — 업무 규칙이 거의 없는 CRUD 응용에서는 피라미드가
    직사각형이 되고, 프로세스 밖 의존이 데이터베이스 하나뿐인 UI 없는 API에서는 종단
    테스트를 더 두는 것이 선택지가 된다.[^khorikov2020-unit-testing]

## 이 소스의 사각

- **측정이 없다.** 거짓 양성이 스위트를 무너뜨린다는 이 페이지의 중심 논거에 붙은 근거가
  저자의 경험 진술 하나다. 거짓 양성 비율을 잰 값도, 그것이 리팩터링 빈도에 미치는 효과를
  잰 값도 없다. **저자가 "이 속성들은 정밀하게 잴 수 없다"고 스스로 적는다.**
- **리팩터링 내성이 이진이라는 판정 자체가 측정되지 않았다.** `mostly`·`almost no`라는
  헤지가 붙은 관찰이고, 중간 단계가 없다는 주장을 뒷받침하는 사례 수집이 없다.
- **관찰 가능한 행위의 정의가 클라이언트의 목표에 달려 있다.** 목표가 무엇인지는 사람이
  판정하므로, 이 정의는 기계 검사로 옮겨지지 않는다. 이 책은 그 판정의 불일치를 어떻게
  다룰지 다루지 않는다.
- **언어 모델 시대의 정량 재검이 미확보다.** 생성된 테스트가 네 속성 가운데 어디에 서는지,
  생성 도구 아래에서 리팩터링 내성의 값어치가 달라지는지는 이 책의 주제가 아니고 이 KB도
  그 재검을 아직 갖고 있지 않다. **이 페이지의 판정은 경험 법칙의 지위로 인용한다.**
- **확보본이 MEAP V03이다.** 최종 인쇄판에서 어느 문장이 어떻게 바뀌었는지 대조하지 않았다.

## 이어지는 페이지

- [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md) — **이 페이지의 판정에서
  연역되는 답.** 거짓 양성의 원인이 구현 세부 결합이라면, 대역을 어디에 쓰는가는 무엇이
  구현 세부인가의 문제가 된다. 같은 소스의 5·8·9장이 거기 있다
- [대역 어휘와 두 TDD 스타일](test-double-vocabulary-and-tdd-styles.md) — 이 페이지가 쓰는
  대역 낱말들의 지형. 그쪽이 어휘와 스타일의 갈림을 소유하고, 이 페이지는 그 갈림을
  판정할 잣대 하나를 소유한다
- [테스트의 바람직한 성질 열둘](test-desiderata.md) — **같은 방향의 서술이 목록의 한 줄로
  놓인 자리.** 그쪽의 구조 둔감(structure-insensitive)은 구조가 바뀌면 결과가 바뀌지 않아야
  한다는 **상태의 서술**이고, 이 페이지는 같은 방향을 **견디는 정도**로 재며 거짓 양성의
  원인까지 지목한다. 그쪽의 행위 민감(Behavioral)과 이 페이지의 관찰 가능한 행위도 같은
  관계다. **두 문면은 같은 방향이되 층이 다르므로 이 KB는 둘을 동일시하지 않는다** —
  그쪽도 측정이 없는 실무자의 목록이다
- [현재 동작을 오라클로 쓴다는 것](current-behaviour-as-oracle.md) — **같은 증상을 반대편에서
  본 자리.** 이 페이지는 구현에 결합한 테스트를 "거짓 양성을 낳는다"로 진단하고, 그쪽은 같은
  테스트를 "변경 탐지기"로 부르며 무엇을 잃는지 적는다
- [특성화 테스트](characterization-test.md) — 리팩터링의 안전망을 현재 동작으로 짜는 다른
  방법. 이 페이지가 리팩터링을 "관찰 가능한 행위를 바꾸지 않는 변경"으로 정의하는 자리와
  그쪽이 그 행위를 어디서 얻는가가 맞물린다
- [리팩터링을 가로막는 것](obstacles-to-refactoring.md) — 이 페이지가 든 두 경로(둔감화·신뢰
  상실)가 실제 장애물 목록의 어디에 서는가
- [종단 테스트를 왜 줄이는가](why-fewer-end-to-end-tests.md) — 이 페이지의 첫째 극단 사례가
  다른 소스에서 따로 다뤄진 자리
- [구글의 테스트 크기 어휘와 스위트 운영](google-test-sizes-and-suite-operations.md) —
  피라미드의 배합을 조직 규약으로 정한 다른 소스. 이 책은 방향만 적고 수치를 적지 않는다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브
- **아직 답이 없는 물음 하나** — 리팩터링 내성이 정말 이진인가. 이 책은 그것을 근거로
  협상 불가를 논증하는데, 그 이진성 자체를 잰 측정이 이 KB에 없다

[^khorikov2020-unit-testing]: Khorikov, *Unit Testing: Principles, Practices, and
    Patterns*, Manning, **확보본은 MEAP V03**(2026-08-23 아카이브). **인쇄판 쪽 앵커가
    없어 locator는 장·절 번호와 원문 절 제목이다** — 1장 §1.1 "The current state of unit
    testing" · 4장 §4.1~§4.5(정의 4.1 · 목록 4.2·4.3·4.6 · 표 4.1 · 곁글 "A story from
    the trenches" · 곁글 "The CAP theorem") · 5장 §5.2 "Observable behavior vs.
    implementation details" · §5.4 · 11장 도입. 직인용은 확보본 문면 그대로이되, MEAP 판
    표지 문자열 `V03`이 문장 앞에 붙은 자리에서는 그 접두를 떼어 냈다(조판 장치). C# 예제
    코드는 개념 설명에 필요한 조각만 인라인 표기로 옮겼고 펜스로 옮기지 않았다. 그림은
    전부 이미지로만 조판돼 있어 그림에서만 읽히는 것은 옮기지 않았다. 근거 등급·판·참고문헌
    상태·인용 규약은 [소스 메타](../sources/khorikov2020-unit-testing.md)가 정본이고,
    읽은 장과 건너뛴 장은 `it/archive/khorikov2020-unit-testing/_progress.yaml`이 정본이다.

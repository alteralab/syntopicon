---
type: concept
title: 일급 함수로 다시 쓰는 디자인 패턴
description: 언어에 일급 함수가 있으면 고전 디자인 패턴 일부가 무너진다는 논증과 그 실물 — GoF 자신이 구현 언어가 어떤 패턴이 유의미한지를 정한다고 밝힌 자리, Norvig의 23개 중 16개 판정, 전략 패턴의 구체 전략이 상태 없는 단일 메서드 클래스라는 관찰과 그것을 함수로 바꾸는 리팩터링, 플라이웨이트를 덧대라는 GoF의 권고가 왜 줄 수를 늘리기만 하는가, 최선의 전략을 고르는 메타 전략에서 목록과 정의가 갈라지며 생기는 미묘한 버그와 그 셋 중 등록 데코레이터가 나은 이유, 명령 패턴이 콜백의 객체 지향 대체물이라는 규정과 그것을 되돌리는 길, 그리고 execute·run·do_it 같은 이름의 단일 메서드 인터페이스를 만나면 의심하라는 일반화
generated: { by: "claude-opus-5", at: "2026-08-18T12:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 일급 함수로 다시 쓰는 디자인 패턴

- [패턴은 언어에 따라 달라진다](#패턴은-언어에-따라-달라진다)
- [고전 전략 패턴](#고전-전략-패턴)
- [구체 전략은 상태가 없다](#구체-전략은-상태가-없다)
- [플라이웨이트를 덧대라는 권고](#플라이웨이트를-덧대라는-권고)
- [최선의 전략을 고르기 — 목록과 정의가 갈라진다](#최선의-전략을-고르기--목록과-정의가-갈라진다)
- [모듈을 뒤져서 찾기](#모듈을-뒤져서-찾기)
- [등록 데코레이터로 푸는 판](#등록-데코레이터로-푸는-판)
- [명령 패턴](#명령-패턴)
- [일반화 — 단일 메서드 인터페이스를 만나면](#일반화--단일-메서드-인터페이스를-만나면)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **일급 함수가 있는 언어에서 고전 디자인 패턴 중 무엇이 무너지고, 무엇이 남는가.**

패턴이라는 **형식 자체**에 대한 판정들은 [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md)가
갖는다. 이 페이지는 그중 한 언어에서 실제로 벌어지는 일 하나를 끝까지 따라간다.

## 패턴은 언어에 따라 달라진다

- 장 머리의 제사가 Ralph Johnson의 것이다 — **패턴에 부합하는 것은 좋음의 척도가 아니다**
  (10장 제사, p.341).[^ramalho2022] *Design Patterns*의 공저자 자신의 말이다.
- 규정 — **소프트웨어 공학에서 디자인 패턴(design pattern)은 흔한 설계 문제를 푸는 일반적
  레시피다** (10장 도입, p.341).[^ramalho2022]
- **패턴이 언어 독립적이라는 말이 모든 패턴이 모든 언어에 적용된다는 뜻은 아니다**
  (10장 도입, p.341).[^ramalho2022] 저자가 든 예가 이터레이터다 — **파이썬에서 이터레이터
  패턴의 레시피를 흉내 내는 것은 말이 되지 않는다. 그 패턴이 언어에 박혀 제너레이터의 형태로
  바로 쓸 수 있게 돼 있기 때문이다 — 제너레이터는 동작하는 데 클래스를 필요로 하지 않고
  고전 레시피보다 코드가 덜 든다** (10장 도입, p.341).[^ramalho2022]
- **그리고 이 논증의 가장 강한 근거는 GoF 자신의 서문이다** (10장 도입, pp.341–342):[^ramalho2022]

  > The choice of programming language is important because it influences one's point of
  > view. Our patterns assume Smalltalk/C++-level language features, and that choice
  > determines what can and cannot be implemented easily. If we assumed procedural
  > languages, we might have included design patterns called "Inheritance,"
  > "Encapsulation," and "Polymorphism."

  - 그 문단이 이어지는 자리에서 CLOS의 다중 메서드가 **Visitor 같은 패턴의 필요를 줄인다**는
    예까지 GoF가 스스로 든다 (10장 도입, p.342).[^ramalho2022]
- Peter Norvig의 판정이 수치로 인용된다 — 1996년 발표 "Design Patterns in Dynamic Languages"
  에서 **원래 *Design Patterns* 책의 23개 패턴 중 16개가 동적 언어에서 "보이지 않게 되거나 더
  단순해진다"**고 진술했다 (10장 도입, p.342).[^ramalho2022]
  - 대상 언어는 Lisp와 Dylan이었으나 **관련된 동적 기능 다수가 파이썬에도 있다. 특히 일급
    함수를 가진 언어라는 맥락에서 Norvig은 Strategy·Command·Template Method·Visitor라 불리는
    고전 패턴들을 다시 생각할 것을 제안한다** (10장 도입, p.342).[^ramalho2022]
  - 장 요약이 같은 인용을 다시 정확한 표현으로 붙인다 — **23개 패턴 중 16개가 각 패턴의 적어도
    일부 쓰임에 대해 C++보다 Lisp나 Dylan에서 질적으로 더 단순한 구현을 갖는다**
    (10장 §"Chapter Summary", p.357).[^ramalho2022]
- 이 장의 목표도 조심스럽게 좁혀져 있다 — **이 장의 목표는 어떤 경우에 함수가 클래스와 같은
  일을, 더 읽기 쉽고 간결한 코드로 할 수 있음을 보이는 것이다** (10장 도입,
  p.342).[^ramalho2022]

## 고전 전략 패턴

- *Design Patterns*의 요약 (10장 §"Classic Strategy", p.343):[^ramalho2022]

  > Define a family of algorithms, encapsulate each one, and make them interchangeable.
  > Strategy lets the algorithm vary independently from clients that use it.

- 참여자 셋 (10장 §"Classic Strategy", p.344):[^ramalho2022]
  - **맥락(Context)** — **대안 알고리즘을 구현하는 교체 가능한 구성 요소에 어떤 계산을 위임해
    서비스를 제공한다.** 전자상거래 예에서는 주문(`Order`)이다.
  - **전략(Strategy)** — **서로 다른 알고리즘을 구현하는 구성 요소들에 공통인 인터페이스.**
    예에서는 추상 클래스 `Promotion`이 맡는다.
  - **구체 전략(Concrete strategy)** — **Strategy의 구체 하위 클래스 중 하나.**
- 전략을 고르는 일은 패턴 밖에 있다 — **구체 전략은 맥락 클래스의 클라이언트가 고른다. (…)
  전략의 선택은 패턴의 범위 밖이다** (10장 §"Classic Strategy", p.344).[^ramalho2022]

## 구체 전략은 상태가 없다

- 관찰 — **예제 10-1의 각 구체 전략은 메서드 하나 `discount`만 가진 클래스다. 게다가 전략
  인스턴스들은 상태가 없다(인스턴스 속성이 없다). 그것들이 평범한 함수를 많이 닮았다고 말할 수
  있을 텐데, 맞는 말이다** (10장 §"Function-Oriented Strategy", p.347).[^ramalho2022]
- 리팩터링의 내용도 그만큼 작다 — **예제 10-3은 구체 전략들을 단순한 함수로 바꾸고 `Promo`
  추상 클래스를 없앤 예제 10-1의 리팩터링이다. `Order` 클래스에는 작은 조정만 필요하다**
  (10장 §"Function-Oriented Strategy", p.347).[^ramalho2022]
- 얻는 것 — **예제 10-3의 코드는 예제 10-1보다 짧다.** 그리고 쓰는 쪽도 단순해진다 —
  **주문마다 새 프로모션 객체를 인스턴스화할 필요가 없다: 함수들은 이미 쓸 준비가 돼 있다**
  (10장 §"Function-Oriented Strategy", p.349).[^ramalho2022]
- 호출 표기 하나가 헷갈리는 자리라 저자가 곁글로 떼어 설명한다 — `self.promotion(self)`에서
  **`Order` 클래스에서 `promotion`은 메서드가 아니다. 마침 호출 가능한 인스턴스 속성이다.
  그래서 식의 첫 부분 `self.promotion`이 그 호출 가능한 것을 가져오고, 그것을 부르려면
  `Order` 인스턴스를 줘야 하는데 이 경우 그것이 `self`다. 그래서 그 식에 `self`가 두 번
  나온다** (10장 곁글 "Why self.promotion(self)?", p.349).[^ramalho2022] 메서드가 인스턴스에
  자동으로 묶이는 기제가 여기에는 적용되지 않는다는 뜻이다.

## 플라이웨이트를 덧대라는 권고

**이 절이 이 장에서 가장 날카로운 대목이다.** 고전 패턴이 자기 대가를 또 다른 패턴으로 갚으려
한다는 지적이다.

- *Design Patterns*의 권고 — **전략 객체는 흔히 좋은 플라이웨이트가 된다**, 그리고 같은 책의
  다른 자리에서 **플라이웨이트는 여러 맥락에서 동시에 쓰일 수 있는 공유 객체다**
  (10장 §"Function-Oriented Strategy", p.350).[^ramalho2022]
- 그 권고의 동기 — **같은 전략이 새 맥락마다 — 우리 예에서는 새 `Order` 인스턴스마다 —
  거듭 적용될 때 새 구체 전략 객체를 만드는 비용을 줄이려고 공유가 권장된다**
  (10장 §"Function-Oriented Strategy", p.350).[^ramalho2022]
- **그리고 판정** (10장 §"Function-Oriented Strategy", p.350):[^ramalho2022]

  > So, to overcome a drawback of the Strategy pattern—its runtime cost—the authors
  > recommend applying yet another pattern. Meanwhile, the line count and maintenance cost
  > of your code are piling up.

- 함수는 그 대가를 애초에 치르지 않는다 — **함수는 사용자 정의 클래스의 인스턴스보다 가볍고,
  각 전략 함수가 모듈을 적재할 때 파이썬 프로세스당 딱 한 번 만들어지므로 플라이웨이트가 필요
  없다. 평범한 함수 또한 "여러 맥락에서 동시에 쓰일 수 있는 공유 객체"다**
  (10장 §"Function-Oriented Strategy", p.350).[^ramalho2022]
- **적용 조건이 함께 못 박혀 있다** — **내부 상태를 가진 복잡한 구체 전략을 다루는 더 까다로운
  사용 사례라면 Strategy와 Flyweight 디자인 패턴의 모든 조각이 합쳐져야 할 수도 있다. 그러나
  흔히 구체 전략은 내부 상태가 없다; 그것들은 맥락에서 온 데이터만 다룬다. 그렇다면 반드시,
  또 하나의 클래스에 선언된 단일 메서드 인터페이스를 구현하는 단일 메서드 클래스를 코딩하는
  대신 평범한 옛 함수를 쓰라** (10장 §"Function-Oriented Strategy", p.350).[^ramalho2022]
  - **"흔히 상태가 없다"가 조건이지 "언제나"가 아니다.** 상태가 있으면 클래스가 여전히 답이라는
    것을 저자가 먼저 적어 두었다.

## 최선의 전략을 고르기 — 목록과 정의가 갈라진다

- 새 요구가 붙는다 — **주어진 `Order`에 가능한 최선의 할인을 고르는 "메타 전략"**
  (10장 §"Function-Oriented Strategy", p.350).[^ramalho2022] 구현은 함수 리스트를 만들고
  `max`를 쓰는 세 줄로 끝난다 (예제 10-6, 10장 §"Choosing the Best Strategy: Simple
  Approach", p.351).[^ramalho2022]
- **함수가 일급이면 그것을 담는 자료 구조를 만드는 것이 자연스러워진다** — **함수가 일급
  객체라는 발상에 익숙해지고 나면, 함수를 담는 자료 구조를 만드는 것이 흔히 말이 된다는
  것이 자연스럽게 따라온다** (10장 §"Choosing the Best Strategy: Simple Approach",
  p.351).[^ramalho2022]
- **그런데 여기서 이 장의 진짜 문제가 생긴다** (10장 §"Choosing the Best Strategy: Simple
  Approach", p.351):[^ramalho2022]

  > Although Example 10-6 works and is easy to read, there is some duplication that could
  > lead to a subtle bug: to add a new promotion strategy, we need to code the function and
  > remember to add it to the `promos` list, or else the new promotion will work when
  > explicitly passed as an argument to `Order`, but will not be considered by
  > `best_promotion`.

  - 이 중복은 [DRY 원칙](dry-principle.md)이 말하는 것의 실물이다. 같은 지식(어떤 함수들이
    프로모션인가)이 두 자리 — 정의와 목록 — 에 적혀 있고, 한쪽만 고치면 **조용히** 틀린다.

## 모듈을 뒤져서 찾기

첫 해법 두 가지가 나란히 제시되고, 둘 다 저자 자신이 유보를 단다.

- `globals()` — **파이썬의 모듈도 일급 객체이고 표준 라이브러리가 그것을 다루는 여러 함수를
  제공한다** (10장 §"Finding Strategies in a Module", p.351).[^ramalho2022] 예제 10-7은
  전역 이름 중 `_promo`로 끝나는 것을 골라 목록을 만든다. **저자 자신이 그것을 `globals`를
  쓰는 다소 조잡한(hackish) 방법이라 부른다** (10장 §"Finding Strategies in a Module",
  p.352).[^ramalho2022]
- `inspect` — 전략 함수들을 별도 모듈에 모으고 **`inspect.getmembers`가 객체의 속성을 —
  이 경우 `promotions` 모듈의 — 술어(불 함수)로 걸러 돌려주게 한다. `inspect.isfunction`을
  써서 모듈에서 함수만 얻는다** (10장 §"Finding Strategies in a Module",
  p.353).[^ramalho2022]
- **그 대가가 명시된다** — **예제 10-8은 함수에 어떤 이름이 붙든 동작한다; 중요한 것은
  `promotions` 모듈이 주문을 받아 할인을 계산하는 함수만 담는다는 것뿐이다. 물론 이것은
  코드의 암묵적 가정이다. 누군가 `promotions` 모듈에 다른 시그니처를 가진 함수를 만들면
  `best_promo`는 그것을 주문에 적용하려다 깨진다** (10장 §"Finding Strategies in a Module",
  p.353).[^ramalho2022]
- 그래서 저자가 이 절의 지위를 스스로 낮춘다 — **예제 10-8의 요점은 완전한 해법을 제시하는
  것이 아니라 모듈 내성(introspection)의 한 가지 가능한 쓰임을 부각하는 것이다**
  (10장 §"Finding Strategies in a Module", p.353).[^ramalho2022]

## 등록 데코레이터로 푸는 판

- 셋째 해법이 이 장의 결론이다 — **더 명시적인 대안은 단순한 데코레이터를 쓰는 것이다**
  (10장 §"Finding Strategies in a Module", p.353).[^ramalho2022]

- 아래가 그 판본이자 이 페이지의 대표 코드다. **목록은 비어 있는 채로 시작하고, 데코레이터가
  정의 시점에 자기를 채운다** — 정의와 목록이 갈라질 자리 자체가 사라진다
  (10장 §"Decorator-Enhanced Strategy Pattern" 예제 10-9, p.354).[^ramalho2022]

  ```python
  Promotion = Callable[[Order], Decimal]

  promos: list[Promotion] = []

  def promotion(promo: Promotion) -> Promotion:
      promos.append(promo)
      return promo

  def best_promo(order: Order) -> Decimal:
      """Compute the best discount available"""
      return max(promo(order) for promo in promos)

  @promotion
  def fidelity(order: Order) -> Decimal:
      """5% discount for customers with 1000 or more fidelity points"""
      if order.customer.fidelity >= 1000:
          return order.total() * Decimal('0.05')
      return Decimal(0)
  ```

- 이점 셋이 명시된다 (10장 §"Decorator-Enhanced Strategy Pattern", p.355):[^ramalho2022]
  - **프로모션 전략 함수가 특별한 이름을 쓰지 않아도 된다 — `_promo` 접미가 필요 없다.**
  - **`@promotion` 데코레이터가 꾸며진 함수의 목적을 부각하고, 프로모션을 일시적으로 비활성화하기
    쉽게 만든다: 데코레이터를 주석 처리하면 된다.**
  - **프로모션 할인 전략을 시스템 어디든 다른 모듈에 정의할 수 있다 — `@promotion` 데코레이터가
    적용되기만 하면.**
- 이 데코레이터가 무슨 기제로 도는지는 [클로저와 데코레이터](../concepts/closures-and-decorators.md)의
  등록 데코레이터 절이 정본이다. **데코레이터가 모듈 반입 시점에 실행된다는 사실**이 여기서
  기능으로 쓰인다.

## 명령 패턴

- 목표 — **명령(Command) 패턴의 목표는 연산을 부르는 객체(호출자, invoker)를 그것을 구현하는
  제공자 객체(수신자, receiver)로부터 결합 해제하는 것이다** (10장 §"The Command Pattern",
  p.356).[^ramalho2022]
- 기제 — **둘 사이에 Command 객체를 두고, `execute`라는 단일 메서드를 가진 인터페이스를
  구현하게 하는 것이다. 그 메서드가 수신자의 어떤 메서드를 불러 원하는 연산을 수행한다.
  그렇게 하면 호출자는 수신자의 인터페이스를 알 필요가 없고, 서로 다른 수신자를 서로 다른
  Command 하위 클래스로 맞출 수 있다** (10장 §"The Command Pattern", p.356).[^ramalho2022]
- **그리고 GoF의 자기 규정이 이 패턴의 급소를 드러낸다** (10장 §"The Command Pattern",
  p.356):[^ramalho2022]

  > Quoting from *Design Patterns*, "Commands are an object-oriented replacement for
  > callbacks." The question is: do we need an object-oriented replacement for callbacks?
  > Sometimes yes, but not always.

- 되돌리는 길 — **호출자에게 Command 인스턴스를 주는 대신 그냥 함수를 줄 수 있다.
  `command.execute()`를 부르는 대신 호출자는 그냥 `command()`를 부르면 된다. MacroCommand는
  `__call__`을 구현하는 클래스로 만들 수 있다** (10장 §"The Command Pattern",
  p.356).[^ramalho2022]
- 더 복잡한 요구가 있어도 파이썬 쪽 선택지가 둘 남는다 — 실행 취소 같은 것을 지원하려면 단순한
  콜백 함수 이상이 필요할 수 있는데, 그때도 (10장 §"The Command Pattern", p.357):[^ramalho2022]
  - **`MacroCommand` 같은 호출 가능한 인스턴스는 필요한 어떤 상태든 지닐 수 있고 `__call__`
    말고도 추가 메서드를 제공할 수 있다.**
  - **클로저는 호출 사이에 함수의 내부 상태를 담는 데 쓰일 수 있다.**
- 두 패턴을 같은 방식으로 다뤘다는 것이 저자의 정리다 — **높은 수준에서 여기의 접근은 Strategy에
  적용한 것과 비슷했다: 단일 메서드 인터페이스를 구현하는 참여자 클래스의 인스턴스를 호출
  가능한 것으로 대체하는 것. 결국 모든 파이썬 호출 가능한 것은 단일 메서드 인터페이스를
  구현하고 그 메서드의 이름은 `__call__`이다** (10장 §"The Command Pattern",
  p.357).[^ramalho2022]

## 일반화 — 단일 메서드 인터페이스를 만나면

- 이 장이 남기는 조문 (10장 §"Chapter Summary", p.357):[^ramalho2022]

  > The refactoring of Strategy and the discussion of Command in this chapter are examples
  > of a more general insight: sometimes you may encounter a design pattern or an API that
  > requires that components implement an interface with a single method, and that method
  > has a generic-sounding name such as "execute," "run," or "do_it." Such patterns or APIs
  > often can be implemented with less boilerplate code in Python using functions as
  > first-class objects.

  - **탐지 신호가 이름이라는 것이 이 조문의 실용적 값이다** — 인터페이스에 메서드가 하나뿐이고
    그 이름이 일반적으로 들리면, 그 인터페이스가 실은 "함수"라는 뜻일 가능성이 높다.
- 그리고 패턴을 쓰는 태도에 대한 Johnson의 판정이 다시 인용된다 — *Design Patterns* 20주년을
  돌아보며 그가 든 이 책의 실패 하나가 **패턴을 설계 과정의 단계가 아니라 종점으로 보는 데
  너무 많은 강조를 둔 것**이다 (10장 §"Chapter Summary", p.357).[^ramalho2022]
  - 저자는 그 판정을 자기 장의 방법으로 받는다 — **이 장에서 우리는 Strategy 패턴을 출발점으로
    썼다: 일급 함수를 써서 단순화할 수 있는, 동작하는 해법으로** (10장 §"Chapter Summary",
    p.357).[^ramalho2022]
- 마지막으로 저자가 자기 논증의 한계를 스스로 긋는다 — Norvig이 다중 메서드가 Builder 패턴을
  단순화한다고 본 반면 GoF는 그것이 Visitor의 필요를 줄인다고 보았다는 대조를 들며,
  **디자인 패턴을 언어 기능에 짝지우는 것은 정확한 과학이 아니다**라고 적는다
  (10장 곁글 "Soapbox", p.359).[^ramalho2022]
  - 같은 곁글이 파이썬에 대한 Norvig의 셈도 인용한다 — **파이썬에는 일급 함수와 일급 타입이
    있고, Norvig은 그 기능들이 23개 패턴 중 10개에 영향을 준다고 주장한다**
    (10장 곁글 "Soapbox", p.359).[^ramalho2022]
- 오해의 출처도 지목된다 — **전 세계 강의실에서 디자인 패턴은 흔히 자바 예제로 가르쳐진다.
  원래의 디자인 패턴이 어떤 구현 언어에서도 유용하다고 믿게 되었다고 주장하는 학생을 한 명
  이상 들었다** (10장 곁글 "Soapbox", p.359).[^ramalho2022]

## 이어지는 페이지

- [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md) — 패턴이라는 형식 자체에 대한 판정들이
  모인 자리. 이 페이지의 논증은 그중 "패턴은 언어에 의존한다"의 실물 하나다
- [클로저와 데코레이터](../concepts/closures-and-decorators.md) — 여기 쓰인 등록 데코레이터의 기제
- [파이썬의 일급 함수](first-class-functions-in-python.md) — 이 논증이 기대는 언어 성질
- [DRY 원칙](dry-principle.md) — 정의와 목록이 갈라지는 중복이 왜 위험한가
- [패턴을 실제로 적용할 때](pattern-application-in-practice.md) — 다른 카탈로그가 같은 질문에
  부딪힌 자리
- [상속세](inheritance-tax.md) — "클래스 상속보다 객체 합성을 선호하라"가 나온 *Design
  Patterns* 서문의 다른 조항이 다뤄지는 쪽
- [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 10장 "Design Patterns with First-Class Functions"(pp.341–359) —
    제사·도입(pp.341–342) · §"Classic Strategy"(pp.342–346) · §"Function-Oriented
    Strategy"(pp.347–350) · 곁글 "Why self.promotion(self)?"(p.349) · §"Choosing the Best
    Strategy: Simple Approach"(pp.350–351) · §"Finding Strategies in a Module"(pp.351–353) ·
    §"Decorator-Enhanced Strategy Pattern"(pp.353–355) · §"The Command Pattern"(pp.355–357) ·
    §"Chapter Summary"(p.357) · 곁글 "Soapbox"(p.359). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 30).
    예제 10-9는 원문에서 세 전략 함수 중 하나(`fidelity`)만 남기고 깎았다 — 나머지 둘
    (`bulk_item`·`large_order`)은 같은 형태의 반복이라 등록 기제를 보이는 데 필요하지 않다.
    보탠 줄은 없다. Figure 10-1(전략 패턴 UML)과 Figure 10-2(명령 패턴 UML)는 이미지라
    참여자 목록을 산문으로 옮겼다. 예제 10-2·10-4·10-5(doctest 세션)는 프롬프트가 섞여
    펜스로 옮기지 않았다.

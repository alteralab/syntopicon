---
type: concept
title: 파이썬의 연산자 오버로딩
description: 사용자 정의 타입에 중위 연산자를 붙일 때 지켜야 하는 불변식과 파이썬이 그은 제한 셋 — 연산자는 피연산자를 바꾸지 않고 새 객체를 돌려준다는 규칙, 다룰 수 없는 피연산자를 예외가 아니라 NotImplemented로 알려야 하는 이유와 정방향·역방향 디스패치, 덕 타이핑과 구스 타이핑 중 무엇을 고를 것인가의 교환, 리치 비교 연산자만 다른 규칙을 따르는 자리, 그리고 증강 대입이 원래 연산자보다 관대해도 되는 이유
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬의 연산자 오버로딩

- [버전 조건](#버전-조건)
- [파이썬이 그은 제한 셋](#파이썬이-그은-제한-셋)
- [불변식 — 피연산자를 바꾸지 않는다](#불변식--피연산자를-바꾸지-않는다)
- [다룰 수 없다는 신호는 예외가 아니다](#다룰-수-없다는-신호는-예외가-아니다)
- [덕 타이핑과 구스 타이핑 사이](#덕-타이핑과-구스-타이핑-사이)
- [리치 비교 연산자는 규칙이 다르다](#리치-비교-연산자는-규칙이-다르다)
- [증강 대입 — 더 관대해도 되는 이유](#증강-대입--더-관대해도-되는-이유)
- [찬반](#찬반)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **내가 만든 타입에 `+`나 `*` 같은 중위 연산자를 붙일 때 무엇을 지켜야 다른
타입과 안전하게 섞이는가.**

## 버전 조건

> **버전 조건**: 파이썬 3.5 이상. 행렬 곱 연산자 `@`와 그 특수 메서드
> `__matmul__`·`__rmatmul__`·`__imatmul__`이 PEP 465로 3.5에 들어왔다 — **3.4 이하에서
> `a @ b`는 문법 오류다.** 아래 `zip`의 `strict` 인자는 PEP 618로 파이썬 3.10에 들어왔다.
> 나머지 서술(단항·중위 연산자의 디스패치 규칙, `NotImplemented`, 리치 비교, 증강 대입)은
> 판을 타지 않는다.

## 파이썬이 그은 제한 셋

- 이 기능의 평판부터 저자가 적는다 — **연산자 오버로딩은 어떤 진영에서 나쁜 이름을 갖는다.
  그것은 남용될 수 있는(그리고 남용되어 온) 언어 기능이고, 그 결과 프로그래머의 혼란과 버그와
  예상치 못한 성능 병목을 낳는다. 그러나 잘 쓰면 그것은 즐거운 API와 읽기 좋은 코드로
  이어진다** (16장 §"Operator Overloading 101", p.563).[^ramalho2022]
- **파이썬이 균형을 잡는 방식이 제한 셋이다** (16장 §"Operator Overloading 101",
  p.563):[^ramalho2022]
  - **내장 타입에 대해 연산자의 의미를 바꿀 수 없다.**
  - **새 연산자를 만들 수 없고, 기존 연산자를 오버로드할 수만 있다.**
  - **몇몇 연산자는 오버로드할 수 없다: `is`·`and`·`or`·`not`(그러나 비트 연산자
    `&`·`|`·`~`는 가능하다).**
- 왜 중위 표기가 필요한가의 근거를 저자가 자바와의 대조로 든다. 복리 계산식을 파이썬에서는
  `principal * ((1 + rate) ** periods - 1)`로 쓰고 `decimal.Decimal`로 정확한 결과를 얻지만,
  자바에서 `BigDecimal`로 바꾸면 중위 연산자를 더 이상 쓸 수 없다 —
  `principal.multiply(BigDecimal.ONE.add(rate).pow(periods).subtract(BigDecimal.ONE))`가
  된다. **중위 연산자가 공식을 더 읽기 좋게 만든다는 것은 분명하다** (16장 도입,
  p.561).[^ramalho2022]
  - 그리고 귀결 하나를 저자가 덧붙인다 — **고수준의 쓰기 쉬운 언어에 연산자 오버로딩이
    있었다는 것은 아마 금융·과학 응용을 포함한 데이터 과학에서 파이썬이 거둔 거대한 성공의
    핵심 이유였을 것이다** (16장 도입, p.561).[^ramalho2022]

## 불변식 — 피연산자를 바꾸지 않는다

- 단항 연산자에서 규칙이 먼저 나온다 — **당신의 클래스에서 말이 되는 어떤 논리든 쓰되,
  연산자의 일반 규칙을 지켜라: 항상 새 객체를 돌려주라. 다시 말해 수신자(`self`)를 수정하지
  말고 적절한 타입의 새 인스턴스를 만들어 돌려주라** (16장 §"Unary Operators",
  p.564).[^ramalho2022]
- 중위 연산자에서 같은 규칙이 강조되며 예외가 명시된다 (16장 §"Overloading + for Vector
  Addition", p.567):[^ramalho2022]

> Special methods implementing unary or infix operators should never change the value of
> the operands. Expressions with such operators are expected to produce results by creating
> new objects. Only augmented assignment operators may change the first operand (`self`).

- 단항 `+`가 항등이 아닌 경우가 표준 라이브러리에 둘 있다는 곁글도 여기 딸린다 —
  `decimal.Decimal`은 산술 문맥의 정밀도가 바뀌면 `x != +x`가 되고,
  `collections.Counter`는 단항 `+`가 빈 `Counter`를 더하는 지름길이라 **0 이하의 집계를 결과에서
  버린다** (16장 곁글 §"When x and +x Are Not Equal", pp.565–566).[^ramalho2022]
  - **이 곁글이 값을 갖는 이유**는 두 사례 모두 "연산자가 새 객체를 만든다"는 규칙을 지킨
    결과라는 데 있다. 규칙을 지켰는데도 직관이 깨진다 — 새로 만드는 그 순간의 문맥이 결과를
    바꾸기 때문이다.

## 다룰 수 없다는 신호는 예외가 아니다

- 디스패치 알고리즘이 세 단계다. `a + b`가 주어지면 (16장 §"Overloading + for Vector
  Addition", p.568):[^ramalho2022]
  1. **`a`에 `__add__`가 있으면 `a.__add__(b)`를 부르고, 결과가 `NotImplemented`가 아니면
     그것을 돌려준다.**
  2. **`a`에 `__add__`가 없거나 그것을 부른 결과가 `NotImplemented`이면, `b`에 `__radd__`가
     있는지 검사하고 `b.__radd__(a)`를 부른 뒤 결과가 `NotImplemented`가 아니면 그것을
     돌려준다.**
  3. **`b`에 `__radd__`가 없거나 그것을 부른 결과가 `NotImplemented`이면, *unsupported
     operand types* 메시지와 함께 `TypeError`를 일으킨다.**
  - `__radd__`의 이름을 저자는 **"역방향(reversed)"**이라 부른다. 파이썬 문서가 "반사된
    (reflected)"과 "역방향" 둘 다 쓰는데, 저자는 후자를 선호한다 — **"정방향"과 "역방향"은
    각 방향의 이름을 분명히 부르는 데 비해 "반사된"은 명백한 반대말이 없기 때문이다**
    (16장 각주 4, p.569).[^ramalho2022]
- **두 이름을 혼동하지 말라는 경고가 붙는다** (16장 §"Overloading + for Vector Addition",
  p.570):[^ramalho2022]

> Do not confuse `NotImplemented` with `NotImplementedError`. The first, `NotImplemented`,
> is a special singleton value that an infix operator special method should return to tell
> the interpreter it cannot handle a given operand. In contrast, `NotImplementedError` is an
> exception that stub methods in abstract classes may raise to warn that subclasses must
> implement them.

- **조문 — 타입이 안 맞으면 예외가 아니라 값으로 알린다** (16장 §"Overloading + for Vector
  Addition", p.571):[^ramalho2022]

> if an operator special method cannot return a valid result because of type
> incompatibility, it should return `NotImplemented` and not raise `TypeError`. By returning
> `NotImplemented`, you leave the door open for the implementer of the other operand type to
> perform the operation when Python tries the reversed method call.

  - 근거가 예외의 부작용에 있다 — **중위 연산자 메서드가 예외를 일으키면 그것은 연산자 디스패치
    알고리즘을 중단시킨다** (같은 절, p.572).[^ramalho2022] 즉 예외를 던지면 상대 타입이
    그 연산을 처리할 기회를 빼앗는다.
  - 이것이 이 페이지가 남기는 설계 조문이다. **"나는 못 한다"와 "이것은 오류다"를 가르는 것이
    확장 가능한 프로토콜의 조건**이다. 내 타입이 모르는 타입을 만났을 때 오류를 선언하면 그
    시스템은 그 자리에서 닫힌다.

- 정방향과 역방향을 함께 쓰는 관용이 이렇다 (16장 §"Overloading + for Vector Addition"
  예제 16-10, pp.571–572):[^ramalho2022]

  ```python
  def __add__(self, other):
      try:
          pairs = itertools.zip_longest(self, other, fillvalue=0.0)
          return Vector(a + b for a, b in pairs)
      except TypeError:
          return NotImplemented

  def __radd__(self, other):
      return self + other
  ```

- 역방향 메서드가 짧은 것에도 조건이 있다 — **흔히 `__radd__`는 그 정도로 단순할 수 있다:
  그저 적절한 연산자를 부르는 것, 즉 이 경우 `__add__`에 위임하는 것. 이것은 어떤 교환 법칙이
  성립하는 연산자에도 적용된다. `+`는 수나 우리 벡터를 다룰 때는 교환 가능하지만, 파이썬에서
  시퀀스를 이어 붙일 때는 교환 가능하지 않다** (16장 §"Overloading + for Vector Addition",
  p.570).[^ramalho2022]
- **역방향 메서드가 쓸모없는 경우도 명시된다** — **일반적으로, 정방향 중위 연산자 메서드
  (예: `__mul__`)가 `self`와 같은 타입의 피연산자만 다루도록 설계됐다면 대응하는 역방향 메서드
  (예: `__rmul__`)를 구현하는 것은 쓸모없다. 정의상 그것은 다른 타입의 피연산자를 다룰 때에만
  호출될 것이기 때문이다** (16장 §"Augmented Assignment Operators", p.585).[^ramalho2022]

## 덕 타이핑과 구스 타이핑 사이

- 두 방법이 이 장에서 나란히 쓰인다 — **피연산자 타입을 섞으려면 우리가 다룰 수 없는
  피연산자를 검출해야 한다. 이 장에서 우리는 그것을 두 가지 방식으로 했다: 덕 타이핑 방식으로는
  그냥 연산을 시도하고 `TypeError` 예외가 나면 잡았다. 나중에 `__mul__`과 `__matmul__`에서는
  명시적 `isinstance` 검사로 했다. 두 접근에는 장단점이 있다: 덕 타이핑이 더 유연하지만
  명시적 타입 검사가 더 예측 가능하다** (16장 §"Chapter Summary", p.586).[^ramalho2022]
- **일반 지침과 그 예외가 함께 적힌다** (16장 §"Chapter Summary", p.586):[^ramalho2022]

> In general, libraries should leverage duck typing—opening the door for objects regardless
> of their types, as long as they support the necessary operations. However, Python's
> operator dispatch algorithm may produce misleading error messages or unexpected results
> when combined with duck typing. For this reason, the discipline of type checking using
> `isinstance` calls against ABCs is often useful when writing special methods for operator
> overloading.

  - 오해를 부르는 메시지의 실물이 앞에 있다 — 벡터에 문자열을 더하려 하면 오류가 `float`과
    `str`에 대해 불평한다. **더 나쁜 것은 피연산자가 반복 가능하지만 그 항목이 벡터의 `float`
    항목에 더해질 수 없을 때 오해를 부르는 메시지를 얻는다는 것이다** (16장 §"Overloading +
    for Vector Addition", p.571).[^ramalho2022]
  - 구스 타이핑(goose typing)의 값도 명시된다 — **구스 타이핑은 유연성과 안전 사이의 좋은
    타협인데, 기존의 또는 미래의 사용자 정의 타입이 어떤 ABC의 실제 또는 가상 하위 클래스로
    선언될 수 있기 때문이다. 게다가 ABC가 `__subclasshook__`을 구현하면 객체는 필요한 메서드를
    제공하는 것만으로 그 ABC에 대한 `isinstance` 검사를 통과한다 — 서브클래싱도 등록도 필요
    없다** (16장 §"Chapter Summary", p.586).[^ramalho2022] 그 기제의 전문은
    [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)에 있다.
- **저자가 판을 사이에 두고 마음을 바꾼 자리가 여기 표시돼 있다.** 초판에서는 `__mul__`의
  스칼라 인자를 `isinstance(scalar, numbers.Real)`로 검사했는데 이번 판에서 덕 타이핑으로
  바꿨다 — **이제 나는 `numbers` ABC를 쓰기를 피하는데, 그것들이 PEP 484에 의해 지원되지
  않고, 정적으로도 검사될 수 없는 타입을 런타임에 쓰는 것이 나쁜 생각으로 보이기 때문이다**
  (16장 §"Overloading * for Scalar Multiplication", p.574).[^ramalho2022] 반대로
  `__matmul__`은 이번 판에서 구스 타이핑으로 바꿨다. **같은 장 안에서 두 방향의 이동이
  일어난 것**이 이 절이 옮길 만한 이유다 — 선택이 원칙이 아니라 조건에 달려 있다는 실물이다.

## 리치 비교 연산자는 규칙이 다르다

- 두 가지가 다르다 (16장 §"Rich Comparison Operators", p.577):[^ramalho2022]
  - **정방향과 역방향 호출에 같은 메서드 집합이 쓰인다.** `==`는 양쪽 모두 `__eq__`를 부르고
    인자만 바꾸며, `__gt__`의 정방향 호출 다음에는 인자를 바꾼 `__lt__`의 역방향 호출이 온다.
  - **`==`와 `!=`의 경우, 역방향 메서드가 없거나 `NotImplemented`를 돌려주면 파이썬은
    `TypeError`를 일으키는 대신 객체 ID를 비교한다.**
- 그래서 `==`는 결코 오류가 되지 않는다. 순서 비교(`>`·`<`·`>=`·`<=`)만 마지막에 `TypeError`로
  끝난다.
- **이 규칙이 설계 판단 하나를 낳는다.** 앞 장의 `Vector.__eq__`는 성분만 같으면 튜플과도
  같다고 판정했는데, 저자는 그것을 되돌린다 — **이 결과는 아마 바람직하지 않을 것이다. 우리는
  정말로 `Vector`가 같은 수를 담은 튜플과 같다고 여겨지기를 원하는가? 나는 이것에 대해 확고한
  규칙이 없다; 그것은 애플리케이션 문맥에 달려 있다** (16장 §"Rich Comparison Operators",
  p.578).[^ramalho2022] 그러면서 Zen of Python 한 줄을 근거로 든다 —
  **"모호함 앞에서 추측하려는 유혹을 거부하라(In the face of ambiguity, refuse the temptation
  to guess)."**
  - 그리고 언어 자신을 근거로 삼는다 — **파이썬 자신에게서 단서를 얻으면 `[1,2] == (1, 2)`가
    `False`인 것을 볼 수 있다. 그러므로 보수적으로 가서 타입 검사를 좀 하자** (같은 절,
    p.578).[^ramalho2022] 개선된 `__eq__`는 `isinstance(other, Vector)`가 아니면
    `NotImplemented`를 돌려주고, 그 뒤는 위 디스패치 규칙이 알아서 한다.
  - **관대함이 비용이라는 판정이 이 절의 조문이다** — **피연산자 평가에서의 과도한 관대함은
    놀라운 결과로 이어질 수 있고, 프로그래머는 놀라움을 싫어한다** (같은 절,
    p.578).[^ramalho2022]
- `!=`는 구현하지 않는다 — **`object`에서 상속한 `__ne__`의 대비 동작이 우리에게 맞기
  때문이다: `__eq__`가 정의되고 `NotImplemented`를 돌려주지 않으면 `__ne__`는 그 결과를
  부정해 돌려준다** (16장 §"Rich Comparison Operators", p.580).[^ramalho2022]

## 증강 대입 — 더 관대해도 되는 이유

- 기본 동작 — **클래스가 제자리 연산자를 구현하지 않으면 증강 대입 연산자는 문법 설탕으로
  동작한다: `a += b`는 정확히 `a = a + b`로 평가된다. 그것이 불변 타입에 기대되는 동작이고,
  `__add__`가 있으면 `+=`는 추가 코드 없이 동작한다** (16장 §"Augmented Assignment
  Operators", p.581).[^ramalho2022]
- 제자리 메서드를 구현하면 달라진다 — **이름이 말하듯 그 연산자들은 왼쪽 피연산자를 제자리에서
  바꾸고 결과로 새 객체를 만들지 않을 것으로 기대된다** (같은 절, p.581).[^ramalho2022]
  - 조건이 명시된다 — **제자리 특수 메서드는 우리 `Vector` 클래스 같은 불변 타입에 결코
    구현되어서는 안 된다** (같은 절, p.581).[^ramalho2022]
  - 그리고 반환값이 규약이다 — **매우 중요: 가변 객체의 증강 대입 특수 메서드는 `self`를
    돌려줘야 한다. 그것이 사용자가 기대하는 것이다** (16장 §"Augmented Assignment
    Operators", p.585).[^ramalho2022]
- **`+`와 `+=`의 엄격도가 달라도 되는 이유가 이 절에서 가장 옮길 만한 것이다** (16장
  §"Augmented Assignment Operators", p.583):[^ramalho2022]

> Note that the `+=` operator is more liberal than `+` with regard to the second operand.
> With `+`, we want both operands to be of the same type (`AddableBingoCage`, in this case),
> because if we accepted different types, this might cause confusion as to the type of the
> result. With the `+=`, the situation is clearer: the lefthand object is updated in place,
> so there's no doubt about the type of the result.

  - 저자는 이 판단의 근거도 언어에서 가져온다 — **나는 내장 `list` 타입이 어떻게 동작하는지
    관찰함으로써 `+`와 `+=`의 대비되는 동작을 검증했다. `my_list + x`를 쓰면 리스트에 다른
    리스트만 이어 붙일 수 있지만 `my_list += x`를 쓰면 오른쪽의 어떤 반복 가능 객체 `x`로도
    왼쪽 리스트를 확장할 수 있다. 이것이 `list.extend()` 메서드가 동작하는 방식이다: 그것은
    어떤 반복 가능 인자든 받는다** (같은 절, p.583).[^ramalho2022]
  - **이 대비가 일반형을 갖는다.** 결과의 타입이 모호해질 수 있는 연산은 좁게, 결과의 타입이
    이미 정해진 연산은 넓게 — 관대함의 허용치를 **모호함의 유무**가 정한다.
- 오류 메시지에 대한 조항도 하나 있다 — **가능할 때 오류 메시지는 사용자를 해법으로 명시적으로
  안내해야 한다** (16장 §"Augmented Assignment Operators" 예제 16-19 설명,
  p.584).[^ramalho2022]

## 찬반

- 자바의 설계자 James Gosling이 이 기능을 뺀 이유를 이 장이 경구로 삼고 곁글에서 전문을
  옮긴다 — **아마 인구의 20~30퍼센트가 연산자 오버로딩을 악마의 자식으로 생각한다. (…) 그
  문제의 많은 부분은 당신이 합리적으로 오버로드할 수 있는 연산자가 여섯 개 남짓뿐인데 사람들이
  정의하고 싶어 하는 연산자는 수천 수백만 개라는 사실에서 비롯한다 — 그래서 당신은 골라야 하고,
  종종 그 선택은 당신의 직관과 충돌한다** (16장 곁글 §"Operator Overloading: Pros and Cons",
  p.588).[^ramalho2022]
  - 같은 인터뷰에서 Gosling이 반대 진영도 인정한다 — **그리고 실제로 연산자 오버로딩을 적절히
    써 왔고 그것에 정말로 신경 쓰며 그것이 실제로 정말 중요한 약 10퍼센트의 공동체가 있다;
    이들은 거의 전적으로 수치 작업을 하는 사람들인데, 거기서는 표기법이 사람의 직관에 호소하는
    데 매우 중요하다** (같은 곁글, p.588).[^ramalho2022]
- 저자의 판정 — **Guido van Rossum은 연산자 오버로딩을 지원하는 데서 중간 길을 골랐다:
  그는 사용자가 `<=>`나 `:-)` 같은 새로운 임의의 연산자를 만들 문을 열어 두지 않았고, 그것이
  맞춤 연산자의 바벨탑을 막고 파이썬 파서를 단순하게 유지한다. 파이썬은 또한 내장 타입의
  연산자를 오버로드하게 두지 않는데, 그것도 가독성과 예측 가능한 성능을 촉진하는 제한이다**
  (16장 곁글 §"Operator Overloading: Pros and Cons", p.588).[^ramalho2022]
- **수학 밖의 좋은 사례 둘을 저자가 든다** — 파이썬 3.4의 `pathlib`이 `/`를 오버로드해
  문자열로 파일 시스템 경로를 짓고, `Scapy` 라이브러리가 `/`로 네트워크 계층의 필드를 쌓아
  패킷을 만든다 (16장 §"Further Reading", p.587).[^ramalho2022]
- 비교 연산자를 구현하려 한다면 표준 라이브러리에 도구가 있다 — **`functools.total_ordering`을
  공부하라. 그것은 적어도 두어 개의 리치 비교 연산자를 정의하는 어떤 클래스에서든 나머지 전부에
  대한 메서드를 자동으로 생성하는 클래스 데코레이터다** (16장 §"Further Reading",
  p.587).[^ramalho2022]

## 이어지는 페이지

- [시퀀스 프로토콜의 점진 구현](implementing-the-sequence-protocol.md) — 이 연산자들이
  얹히는 그 `Vector` 클래스가 지어지는 자리
- [파이썬다운 객체 만들기](building-pythonic-objects.md) — 같은 축의 앞 장. `__eq__`가
  튜플과도 같다고 판정하던 문제가 처음 표시된 자리
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 구스 타이핑의 정본과
  `__subclasshook__`이 하는 일
- [파이썬 데이터 모델](python-data-model.md) — 80개 넘는 특수 메서드 중 절반 이상이
  연산자를 구현한다는 그 셈
- [계약에 의한 설계](../concepts/design-by-contract.md) — 연산자가 지켜야 하는 불변식을
  계약의 언어로 말하는 쪽
- [메서드 호출과 디스패치](../concepts/method-invocation-and-dispatch.md) — 정방향·역방향
  디스패치가 이중 디스패치와 어떻게 갈리는가의 비교 대상
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 16장 "Operator Overloading", pp.561–589(경구와 도입 p.561 ·
    §"What's New in This Chapter" p.562 · §"Operator Overloading 101" pp.562–563 ·
    §"Unary Operators" pp.563–564와 곁글 §"When x and +x Are Not Equal" pp.565–566 ·
    §"Overloading + for Vector Addition" pp.566–572와 각주 4 · §"Overloading * for Scalar
    Multiplication" pp.572–574 · §"Using @ as an Infix Operator" pp.574–576 ·
    §"Wrapping-Up Arithmetic Operators" p.576 · §"Rich Comparison Operators" pp.577–580 ·
    §"Augmented Assignment Operators" pp.580–585 · §"Chapter Summary" pp.585–586 ·
    §"Further Reading" p.587 · 곁글 §"Operator Overloading: Pros and Cons" p.588).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    표 16-1(중위 연산자 메서드 이름)과 표 16-2(리치 비교 연산자의 역방향 호출)는 참조
    카탈로그라 옮기지 않았다 — 필요할 때 찾아볼 대응표이고, 이 페이지가 옮긴 것은 그 표가
    따르는 규칙이다. §"Using @ as an Infix Operator"의 초구면·행렬 곱 수학도 같은 사유로
    옮기지 않았고 위 버전 조건 블록에 그 연산자의 도입 시점만 남겼다.
    Figure 16-1(`__add__`·`__radd__` 흐름도)은 이미지로 조판돼 있어 본문의 세 단계 서술로만
    옮겼다. 코드 펜스는 예제 16-10 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만
    제거했다.

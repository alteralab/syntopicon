---
type: concept
title: 클로저와 데코레이터
description: 함수가 자기 바깥에서 정의된 변수를 어떻게 데리고 다니는가와 그 위에 얹힌 데코레이터의 기제 — 데코레이터가 함수를 다른 함수로 갈아치운다는 정의와 그것이 모듈을 읽는 순간 실행된다는 사실, 대입이 있으면 그 변수는 지역이라는 컴파일 시점 판정과 그것이 일으키는 UnboundLocalError, 자유 변수의 규정과 클로저가 보관하는 것이 값이 아니라 바인딩이라는 것, 불변 타입을 다시 묶을 때 nonlocal이 필요해지는 이유, 변수 조회 규칙 네 갈래, 이름과 독스트링을 가리는 문제와 functools.wraps, 매개변수를 받는 데코레이터가 왜 데코레이터 팩토리가 되는가, 그리고 어휘 범위가 동적 범위를 이긴 이유 — 함수는 불투명해야 한다는 요구
generated: { by: "claude-opus-5", at: "2026-08-18T12:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 클로저와 데코레이터

- [데코레이터가 하는 일](#데코레이터가-하는-일)
- [언제 실행되는가 — 반입 시점과 실행 시점](#언제-실행되는가--반입-시점과-실행-시점)
- [등록 데코레이터](#등록-데코레이터)
- [변수는 언제 지역이 되는가](#변수는-언제-지역이-되는가)
- [클로저와 자유 변수](#클로저와-자유-변수)
- [nonlocal이 푸는 문제](#nonlocal이-푸는-문제)
- [변수 조회 규칙](#변수-조회-규칙)
- [이름을 가리는 문제와 functools.wraps](#이름을-가리는-문제와-functoolswraps)
- [매개변수를 받는 데코레이터는 데코레이터가 아니다](#매개변수를-받는-데코레이터는-데코레이터가-아니다)
- [쌓인 데코레이터](#쌓인-데코레이터)
- [왜 어휘 범위가 이겼는가 — 함수는 불투명해야 한다](#왜-어휘-범위가-이겼는가--함수는-불투명해야-한다)
- [GoF 데코레이터 패턴과의 관계](#gof-데코레이터-패턴과의-관계)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **함수가 자기 몸 바깥에서 정의된 변수를 어떻게 데리고 다니며, 그 위에 얹힌
데코레이터는 무엇을 갈아치우는가.**

이 장의 순서 자체가 논증이다. 저자는 데코레이터를 설명하려면 먼저 클로저를 설명해야 하고,
클로저를 설명하려면 먼저 파이썬이 변수를 지역으로 판정하는 방식을 설명해야 한다고 적는다 —
**함수 데코레이터를 직접 구현하고 싶다면 클로저를 이해해야 하고, 그러면 `nonlocal`의 필요성이
자명해진다**[^ramalho2022] (9장 도입, p.303). 이 페이지는 그 순서를 유지한다.

## 데코레이터가 하는 일

- 정의 (9장 §"Decorators 101", p.304):[^ramalho2022]

  > A decorator is a callable that takes another function as an argument (the decorated
  > function). A decorator may perform some processing with the decorated function, and
  > returns it or replaces it with another function or callable object.

- `@` 표기는 **문법 설탕(syntactic sugar)**이다. 다음 두 코드는 같은 효과를 낸다 —
  데코레이터를 쓴 쪽과 `target = decorate(target)`을 손으로 쓴 쪽. **어느 쪽이든 끝에 가면
  `target`이라는 이름은 `decorate(target)`이 돌려준 무엇에 묶인다 — 그것은 처음에 `target`이라
  이름 붙었던 그 함수일 수도 있고, 다른 함수일 수도 있다** (9장 §"Decorators 101",
  p.305).[^ramalho2022]
- **엄밀히 말해 데코레이터는 문법 설탕일 뿐이다. 방금 본 대로 다른 호출 가능한 것과 똑같이
  그냥 부르면서 다른 함수를 넘길 수 있다. 때로는 그쪽이 실제로 편리하다 — 특히
  메타프로그래밍(metaprogramming), 즉 런타임에 프로그램 동작을 바꾸는 일을 할 때가 그렇다**
  (9장 §"Decorators 101", p.305).[^ramalho2022]
- 저자가 요약으로 세우는 세 사실 (9장 §"Decorators 101", p.306):[^ramalho2022]
  - **데코레이터는 함수이거나 다른 호출 가능한 것이다.**
  - **데코레이터는 꾸며진 함수를 다른 함수로 갈아치울 수 있다.**
  - **데코레이터는 모듈이 적재될 때 즉시 실행된다.**
- 셋째 사실이 이 절에서 가장 실무적이다. 실물로 확인하는 절차도 소스가 준다 — 꾸며진
  `target`을 부르면 안쪽 함수 `inner`가 돌고, `target`을 들여다보면
  `<function deco.<locals>.inner at 0x…>`가 나온다 (예제 9-1, 9장 §"Decorators 101",
  p.305).[^ramalho2022] **이름이 가리키는 것이 읽은 것과 다르다**는 사실이 여기서 처음
  드러난다.

## 언제 실행되는가 — 반입 시점과 실행 시점

- 조문 — **데코레이터의 핵심 특징은 꾸며진 함수가 정의된 직후에 실행된다는 것이다. 그것은
  보통 반입 시점(import time), 즉 모듈이 파이썬에 적재될 때다** (9장 §"When Python Executes
  Decorators", p.306).[^ramalho2022]
- 그래서 갈라지는 두 시점이 이 장의 어휘가 된다 — **함수 데코레이터는 모듈이 반입되자마자
  실행되지만 꾸며진 함수들은 명시적으로 호출될 때만 실행된다. 이것이 파이썬 쓰는 사람들이
  반입 시점(import time)과 실행 시점(runtime)이라 부르는 것의 차이를 드러낸다**
  (9장 §"When Python Executes Decorators", p.307).[^ramalho2022]
- 실측 증거도 소스가 붙인다. 예제 9-2의 모듈을 스크립트로 돌리면 `register`가 **다른 어떤
  함수보다 먼저 두 번** 돌고, 모듈을 반입만 해도 그 두 줄이 출력된다 (9장 §"When Python
  Executes Decorators", pp.306–307).[^ramalho2022]

## 등록 데코레이터

- 예제 9-2가 실제 코드에서는 두 가지 점에서 이례적이라고 저자가 미리 밝힌다 (9장
  §"Registration Decorators", p.308):[^ramalho2022]
  - **데코레이터 함수가 꾸며지는 함수들과 같은 모듈에 정의돼 있다. 진짜 데코레이터는 보통 한
    모듈에 정의되고 다른 모듈의 함수들에 적용된다.**
  - **`register` 데코레이터는 인자로 받은 그 함수를 그대로 돌려준다. 실무에서 대부분의
    데코레이터는 안쪽 함수를 정의하고 그것을 돌려준다.**
- 그렇다고 그 기법이 쓸모없는 것은 아니다 — **비슷한 데코레이터들이 많은 파이썬 프레임워크에서
  함수를 어떤 중앙 레지스트리에 추가하는 데 쓰인다 — 예를 들어 URL 패턴을 HTTP 응답을 생성하는
  함수에 대응시키는 레지스트리 같은 것이다. 그런 등록 데코레이터는 꾸며진 함수를 바꿀 수도
  있고 안 바꿀 수도 있다** (9장 §"Registration Decorators", p.308).[^ramalho2022]
  - 이 기법이 실제 설계 문제를 푸는 자리는
    [일급 함수로 다시 쓰는 디자인 패턴](design-patterns-with-first-class-functions.md)이다.
- 그리고 나머지 대부분으로 넘어가는 다리 — **대부분의 데코레이터는 꾸며진 함수를 바꾼다.
  보통 안쪽 함수를 정의하고 그것을 돌려주어 꾸며진 함수를 대신하게 하는 방식이다. 안쪽 함수를
  쓰는 코드는 거의 언제나 올바로 동작하기 위해 클로저에 의존한다** (9장 §"Registration
  Decorators", p.308).[^ramalho2022]

## 변수는 언제 지역이 되는가

여기서부터가 클로저의 바닥이다.

- 놀라운 실물부터 — 전역 `b = 6`이 있는데도, 함수 몸 안에서 `print(b)` **뒤에** `b = 9`가
  있으면 그 `print(b)`가 `UnboundLocalError`를 낸다 (예제 9-4, 9장 §"Variable Scope Rules",
  p.309).[^ramalho2022]
- 기제 — **파이썬이 함수의 몸을 컴파일할 때, `b`가 함수 안에서 대입되므로 그것을 지역 변수로
  판정한다. 생성된 바이트코드가 그 판정을 반영해서 `b`를 지역 범위에서 가져오려 한다**
  (9장 §"Variable Scope Rules", p.309).[^ramalho2022]
- **버그가 아니라 설계 선택이라는 것이 조문이다** — **파이썬은 변수를 선언하라고 요구하지
  않지만, 함수의 몸에서 대입된 변수는 지역이라고 가정한다. 이것은 자바스크립트의 동작보다
  훨씬 낫다 — 자바스크립트도 변수 선언을 요구하지 않지만, 변수가 지역임을(`var`로) 선언하는
  것을 잊으면 자기도 모르게 전역 변수를 뭉갤 수 있다** (9장 §"Variable Scope Rules",
  p.309).[^ramalho2022]
- 바이트코드가 그 판정을 눈으로 보여 준다. 대입이 없는 함수는 `b`에 `LOAD_GLOBAL`을 쓰고,
  대입이 있는 함수는 같은 자리에 `LOAD_FAST`를 쓴다 — **컴파일러가 `b`를 지역 변수로
  여긴다는 뜻이고, 대입이 나중에 오더라도 그렇다. 변수의 성질 — 지역인가 아닌가 — 은 함수의
  몸 안에서 바뀔 수 없기 때문이다** (예제 9-5·9-6 곁글 "Comparing Bytecodes",
  pp.310–311).[^ramalho2022]
- 전역을 함수 안에서 다시 묶고 싶으면 `global` 선언을 쓴다 (9장 §"Variable Scope Rules",
  p.310).[^ramalho2022]

## 클로저와 자유 변수

- **먼저 흔한 오해를 걷어낸다** — **블로그 세계에서 클로저(closure)는 때때로 익명 함수와
  혼동된다. 많은 이가 두 기능의 나란한 역사 때문에 혼동한다: 함수 안에 함수를 정의하는 것은
  익명 함수가 생기기 전까지는 그리 흔하지도 편하지도 않다. 그리고 클로저는 중첩된 함수가 있을
  때만 문제가 된다. 그래서 많은 사람이 두 개념을 동시에 배운다** (9장 §"Closures",
  p.311).[^ramalho2022]
- 규정 (9장 §"Closures", p.312):[^ramalho2022]

  > Actually, a closure is a function—let's call it `f`—with an extended scope that
  > encompasses variables referenced in the body of `f` that are not global variables or
  > local variables of `f`. Such variables must come from the local scope of an outer
  > function that encompasses `f`.

  - 그리고 익명성은 무관하다는 단서 — **함수가 익명이냐 아니냐는 중요하지 않다. 중요한 것은
    그것이 자기 몸 바깥에서 정의된 비전역 변수에 접근할 수 있다는 점이다** (9장 §"Closures",
    p.312).[^ramalho2022]
- **자유 변수(free variable)**의 규정은 실물 위에서 나온다. 고차 함수 `make_averager`가 지역
  리스트 `series`를 만들고 안쪽 함수 `averager`를 돌려주는데, `avg(10)`이 불릴 무렵
  `make_averager`는 이미 반환됐고 그 지역 범위는 사라진 지 오래다. 그런데도 `series`가
  살아 있다 — **`averager` 안에서 `series`는 자유 변수다. 이것은 지역 범위에 묶이지 않은
  변수를 뜻하는 기술 용어다** (9장 §"Closures", p.313).[^ramalho2022]
- 그 보관 자리를 파이썬이 드러내 준다 — 컴파일된 함수 몸을 표상하는 `__code__` 속성에
  `co_varnames`(지역)와 `co_freevars`(자유)가 나뉘어 있고, 자유 변수의 **값**은 돌려받은 함수의
  `__closure__` 속성에 있다. **`avg.__closure__`의 각 항목은 `avg.__code__.co_freevars`의
  이름 하나에 대응한다. 이 항목들은 셀(cell)이고, 실제 값이 들어 있는 `cell_contents`라는
  속성을 갖는다** (예제 9-10·9-11, 9장 §"Closures", p.314).[^ramalho2022]
- 요약 문장 (9장 §"Closures", p.314):[^ramalho2022]

  > To summarize: a closure is a function that retains the bindings of the free variables
  > that exist when the function is defined, so that they can be used later when the
  > function is invoked and the defining scope is no longer available.

  - **보관되는 것이 값이 아니라 바인딩(binding)이라는 점이 이 문장의 무게다.** 셀이 가리키는
    객체가 바뀌면 클로저가 보는 값도 바뀐다. 이름과 객체의 관계가 파이썬에서 어떻게 성립하는지는
    [객체 참조와 가변성](object-references-and-mutability.md)이 정본이다.
- 발생 조건도 좁게 규정된다 — **함수가 비전역 외부 변수를 다뤄야 하는 유일한 상황은 그것이
  다른 함수 안에 중첩돼 있고 그 변수들이 바깥 함수의 지역 범위에 속할 때다** (9장 §"Closures",
  p.314).[^ramalho2022]

## nonlocal이 푸는 문제

- 첫 구현은 값을 전부 쌓아 두고 매번 합을 다시 계산했다. 개수와 합만 들고 있게 고치면
  **깨진다** — `count += 1`이 `UnboundLocalError`를 낸다 (예제 9-12, 9장 §"The nonlocal
  Declaration", p.315).[^ramalho2022]
- 진단 — **`count += 1`은 `count`가 수이거나 어떤 불변 타입일 때 `count = count + 1`과 같은
  뜻이다. 그래서 우리는 실제로 `averager`의 몸 안에서 `count`에 대입하는 것이고, 그것이
  `count`를 지역 변수로 만든다** (9장 §"The nonlocal Declaration", p.315).[^ramalho2022]
- 앞 구현이 멀쩡했던 이유가 대조로 밝혀진다 — **예제 9-8에서는 이 문제가 없었다. 우리는
  `series`라는 이름에 결코 대입하지 않았고, `series.append`를 부르고 그것에 `sum`과 `len`을
  적용했을 뿐이다. 그러니까 우리는 리스트가 가변이라는 사실을 이용한 것이다**
  (9장 §"The nonlocal Declaration", p.315).[^ramalho2022]
- 그리고 일반 규칙 (9장 §"The nonlocal Declaration", p.315):[^ramalho2022]

  > But with immutable types like numbers, strings, tuples, etc., all you can do is read,
  > never update. If you try to rebind them, as in `count = count + 1`, then you are
  > implicitly creating a local variable `count`. It is no longer a free variable, and
  > therefore it is not saved in the closure.

- 처방 — **이를 우회하려고 파이썬 3에 `nonlocal` 키워드가 들어왔다. 그것은 어떤 변수가 함수
  안에서 대입되더라도 자유 변수라고 선언하게 해 준다. `nonlocal` 변수에 새 값이 대입되면
  클로저에 보관된 바인딩이 바뀐다** (9장 §"The nonlocal Declaration", p.316).[^ramalho2022]
  - 버전 조건: 파이썬 3.0 이상. `nonlocal`은 파이썬 3.0에 도입된 예약어이고, 저자는 그것을
    **파이썬에서 가장 알려지지 않은 예약어**라고 부른다 (9장 도입, p.303).[^ramalho2022]

- 고친 구현이 이 페이지의 대표 코드다. **자유 변수를 다시 묶어야 할 때 `nonlocal`을 어디에
  적는지**를 이 여섯 줄이 보인다 — 안쪽 함수의 첫 줄이고, 바깥 함수가 아니다
  (9장 §"The nonlocal Declaration" 예제 9-13, p.316).[^ramalho2022]

  ```python
  def make_averager():
      count = 0
      total = 0

      def averager(new_value):
          nonlocal count, total
          count += 1
          total += new_value
          return total / count

      return averager
  ```

## 변수 조회 규칙

- 함수가 정의될 때 바이트코드 컴파일러가 변수 `x`를 어떻게 가져올지 정하는 규칙이 넷으로
  성문돼 있다 (9장 §"Variable Lookup Logic", pp.316–317):[^ramalho2022]
  1. **`global x` 선언이 있으면 `x`는 모듈 전역 변수 `x`에서 오고 그리로 대입된다.**
  2. **`nonlocal x` 선언이 있으면 `x`는 `x`가 정의된 가장 가까운 바깥 함수의 지역 변수 `x`에서
     오고 그리로 대입된다.**
  3. **`x`가 매개변수이거나 함수 몸에서 값이 대입되면 `x`는 지역 변수다.**
  4. **`x`가 참조되기만 하고 대입되지 않으며 매개변수도 아니면 — 바깥 함수 몸들의 지역
     범위(비지역 범위)에서 찾고, 없으면 모듈 전역 범위에서, 그래도 없으면
     `__builtins__.__dict__`에서 읽는다.**
- 각주 하나가 범위의 경계를 못 박는다 — **파이썬에는 프로그램 전역 범위가 없고 모듈 전역
  범위만 있다** (9장 §"Variable Lookup Logic", p.316 각주 4).[^ramalho2022]

## 이름을 가리는 문제와 functools.wraps

- 시계 데코레이터의 첫 판본이 남기는 흠 — **예제 9-14의 `clock` 데코레이터에는 몇 가지 결함이
  있다: 키워드 인자를 지원하지 않고, 꾸며진 함수의 `__name__`과 `__doc__`을 가린다**
  (9장 §"Implementing a Simple Decorator", p.319).[^ramalho2022]
- 그 가림이 실제로 관측된다 — 꾸며진 `factorial`의 `__name__`을 확인하면 `'clocked'`가 나온다
  (9장 §"How It Works", p.318).[^ramalho2022]
- 처방 — **예제 9-16은 `functools.wraps` 데코레이터를 써서 `func`의 관련 속성들을 `clocked`로
  복사한다** (9장 §"Implementing a Simple Decorator", p.319).[^ramalho2022] `functools.wraps`는
  저자가 **잘 굴러가는 데코레이터를 만드는 도우미**라 부르는 것이다 (9장 §"Decorators in the
  Standard Library", p.320).[^ramalho2022]
- 이것을 조언이 아니라 규칙으로 올린 사람도 인용된다 — **Brett Slatkin의 *Effective Python*
  2판 항목 26은 함수 데코레이터의 모범 사례를 다루며 언제나 `functools.wraps`를 쓸 것을
  권한다** (9장 §"Further Reading", p.336).[^ramalho2022]
  - 다만 소스 자신은 그 조언을 모든 예제에서 따르지 않았다고 밝힌다 — **나는 코드를 가능한 한
    단순하게 만들고 싶어서 Slatkin의 훌륭한 조언을 모든 예제에서 따르지는 않았다**
    (9장 §"Further Reading", p.336 각주 11).[^ramalho2022]

## 매개변수를 받는 데코레이터는 데코레이터가 아니다

- 문제 진술 — **소스 코드에서 데코레이터를 파싱할 때 파이썬은 꾸며진 함수를 가져다 데코레이터
  함수의 첫 인자로 넘긴다. 그러면 데코레이터가 다른 인자들을 받게 하려면 어떻게 하는가?**
  (9장 §"Parameterized Decorators", p.329)[^ramalho2022]
- 답 — **그 인자들을 받아 데코레이터를 돌려주는 데코레이터 팩토리(decorator factory)를 만들고,
  그 데코레이터가 꾸며질 함수에 적용되게 한다** (9장 §"Parameterized Decorators",
  p.329).[^ramalho2022]
- 그래서 개념적 재분류가 따라온다 — **개념적으로 새 `register` 함수는 데코레이터가 아니라
  데코레이터 팩토리다. 호출되면 대상 함수에 적용될 실제 데코레이터를 돌려준다** (9장 §"A
  Parameterized Registration Decorator", p.330).[^ramalho2022] 그 귀결로 **인자를 넘기지
  않더라도 `@register()`처럼 함수로 불러야 한다**는 표기 규칙이 생긴다 (9장 §"A Parameterized
  Registration Decorator", p.331).[^ramalho2022]
- 대가는 중첩 한 겹이다 — **매개변수를 받는 데코레이터는 보통 꾸며진 함수를 갈아치우고, 그
  구성에 또 한 단계의 중첩을 요구한다** (9장 §"A Parameterized Registration Decorator",
  p.332).[^ramalho2022] 저자는 그렇게 쌓인 것을 **함수 피라미드(function pyramid)**라 부른다.
- **그래서 클래스로 쓰라는 반론이 소스 안에 함께 실린다** — **초판의 기술 검토자 Lennart
  Regebro는 데코레이터가 이 장의 예제들처럼 함수가 아니라 `__call__`을 구현하는 클래스로
  코딩되는 것이 최선이라고 주장한다. 나는 사소하지 않은 데코레이터에는 그 접근이 낫다는 데
  동의하지만, 이 언어 기능의 기본 발상을 설명하는 데는 함수가 이해하기 쉽다**
  (9장 §"The Parameterized Clock Decorator", p.334).[^ramalho2022]
  - 저자가 실제로 클래스 판본(예제 9-27)을 나란히 싣고 **어느 쪽이 좋은가**를 독자에게 되묻는다
    (9장 §"A Class-Based Clock Decorator", p.335).[^ramalho2022]
  - 장 요약도 같은 쪽에 선다 — **더 정교한 데코레이터에는 클래스 기반 구현이 읽고 유지보수하기
    더 쉬울 수 있다** (9장 §"Chapter Summary", p.336).[^ramalho2022]
- 정적 검사 도구와의 마찰이 각주에 실물로 남아 있다. `**locals()`로 형식 문자열을 채우는
  기법에 대해 검토자가 지적한다 — **린터는 `locals()`의 사용을 대개 무시하기 때문에 쓰이지 않는
  변수라고 불평할 것이다.** 저자의 응답이 이 소스의 태도를 보여 준다 — **그렇다, 그것은 정적
  검사 도구가 애초에 나와 수많은 프로그래머를 파이썬으로 끌어들인 동적 기능의 사용을 어떻게
  낙담시키는지 보여 주는 또 하나의 예다. (…) 정적 검사 도구를 쓴다면 언제 그것을 무시할지
  아는 것이 매우 중요하다** (9장 §"The Parameterized Clock Decorator", p.333
  각주 10).[^ramalho2022]

## 쌓인 데코레이터

- 규칙 (9장 곁글 "Stacked Decorators", p.322):[^ramalho2022]

  > To make sense of stacked decorators, recall that the `@` is syntax sugar for applying
  > the decorator function to the function below it. If there's more than one decorator,
  > they behave like nested function calls.

  구체적으로 `@alpha`와 `@beta`가 이 순서로 얹히면 `my_fn = alpha(beta(my_fn))`이다 —
  **다시 말해 `beta` 데코레이터가 먼저 적용되고, 그것이 돌려준 함수가 `alpha`에 넘겨진다**
  (9장 곁글 "Stacked Decorators", p.322).[^ramalho2022]
- 이 규칙이 실제로 결과를 바꾸는 자리가
  [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md)에 있다.
  `@cache`와 `@clock`을 겹칠 때 어느 쪽이 안에 오느냐가 무엇이 계측되는지를 정한다.

## 왜 어휘 범위가 이겼는가 — 함수는 불투명해야 한다

곁글 하나가 이 장 전체의 근거를 언어 설계 문제로 되돌린다.

- 문제 진술 — **일급 함수를 가진 어떤 언어의 설계자든 이 문제에 맞닥뜨린다: 일급 객체이므로
  함수는 어떤 범위에서 정의되지만 다른 범위에서 호출될 수 있다. 질문은 이것이다: 자유 변수를
  어떻게 평가할 것인가?** (9장 곁글 "Dynamic Scope Versus Lexical Scope",
  p.338)[^ramalho2022]
- **동적 범위(dynamic scope)**의 규정 — **첫째이자 가장 단순한 답이 "동적 범위"다. 이것은
  자유 변수가 함수가 호출되는 환경을 들여다봐서 평가된다는 뜻이다** (9장 곁글, p.338).[^ramalho2022]
- 그 대가가 이 페이지에서 가장 무거운 문장이다 (9장 곁글 "Dynamic Scope Versus Lexical
  Scope", p.338):[^ramalho2022]

  > Functions should be opaque, with their implementation hidden from users. But with
  > dynamic scope, if a function uses free variables, the programmer has to know its
  > internals to set up an environment where it works correctly.

  - 저자가 상상한 실물이 그것을 보인다. 동적 범위였다면 `avg`를 쓰기 전에 `series = []`를
    스스로 정의해야 하고, 그러려면 `make_averager` 안의 `averager`가 `series`라는 이름의
    리스트를 참조한다는 **내부 구현을 알고 있어야 한다.** 게다가 나중에 `series = [1]`이
    실행되면 앞의 리스트가 통째로 사라진다 — **두 개의 독립적인 이동 평균을 동시에 다루다가
    사고로 일어날 수 있는 일이다** (9장 곁글, p.338).[^ramalho2022]
- 역사적 판정 — **동적 범위는 구현하기 더 쉽고, 아마 그래서 John McCarthy가 일급 함수를 가진
  첫 언어인 Lisp를 만들 때 택한 길이었을 것이다** (9장 곁글, p.338).[^ramalho2022] 그리고
  Paul Graham의 진단이 인용된다 — **고차 Lisp 함수의 바로 그 첫 예제조차 동적 범위 때문에
  깨져 있었다는 것은 동적 범위의 위험을 웅변하는 증언이다** (9장 곁글, pp.338–339).[^ramalho2022]
- 오늘의 규범 — **2022년 저술 시점에 어휘 범위(lexical scope)가 표준이다: 자유 변수는 함수가 정의된 환경을
  고려해 평가된다. 어휘 범위는 일급 함수를 가진 언어의 구현을 복잡하게 만든다. 클로저의 지원을
  요구하기 때문이다. 반면 어휘 범위는 소스 코드를 읽기 쉽게 만든다. Algol 이후 발명된 대부분의
  언어가 어휘 범위를 갖는다** (9장 곁글, p.339).[^ramalho2022]
  - 예외 하나도 지목된다 — **주목할 만한 예외가 자바스크립트다. 거기서는 특수 변수 `this`가
    코드가 어떻게 쓰였느냐에 따라 어휘적으로도 동적으로도 범위가 정해져서 혼란스럽다**
    (9장 곁글, p.339).[^ramalho2022]
- **이 절이 이 KB의 다른 축과 만나는 지점**: 구현을 읽지 않고도 인터페이스만으로 쓸 수 있어야
  한다는 요구는 [부수 효과 없는 함수](side-effect-free-functions.md)가 "개발자가 장막을 뚫고
  들어가도록 강제된다면 인터페이스 추상의 유용성은 제한된다"고 말한 것과 같은 요구다. 다른
  소스가 설계 조항으로 말한 것을 이 소스는 **언어가 어떤 범위 규칙을 골랐는가**의 근거로
  말한다.

## GoF 데코레이터 패턴과의 관계

- 이름 자체가 논란이었다는 것이 장 머리의 제사에 실려 있다 — **이 기능에 "데코레이터"라는
  이름을 고른 것에 대해 여러 불평이 있었다. 주된 것은 그 이름이 GoF 책에서의 쓰임과 일관되지
  않는다는 것이다. *데코레이터*라는 이름은 아마 컴파일러 영역에서의 쓰임에 더 빚지고 있다 —
  구문 트리를 훑으며 주석을 다는 것** (PEP 318 인용, 9장 제사, p.303).[^ramalho2022]
- 저자의 판정은 두 겹이다. 서술 수준에서는 들어맞는다 — **Gamma 외의 *Design Patterns*에서
  데코레이터 패턴의 짧은 설명은 이렇게 시작한다: "객체에 추가적인 책임을 동적으로 붙인다."
  함수 데코레이터는 그 설명에 들어맞는다. 그러나 구현 수준에서 파이썬 데코레이터는 원래
  *Design Patterns* 작업에 서술된 고전적 데코레이터와 거의 닮은 데가 없다**
  (9장 §"How It Works", p.319).[^ramalho2022]
- 유비는 성립한다 — **파이썬에서는 데코레이터 함수가 구체 Decorator 하위 클래스의 역할을 하고,
  그것이 돌려주는 안쪽 함수가 데코레이터 인스턴스다. 돌려받은 함수는 컴포넌트의 인터페이스에
  부합하기 때문에 — 같은 인자를 받으므로 — 투명하다** (9장 곁글 "Python Decorators and the
  Decorator Design Pattern", pp.339–340).[^ramalho2022]
- **그러나 그것이 권고는 아니다** (9장 곁글, p.340):[^ramalho2022]

  > Note that I am not suggesting that function decorators should be used to implement the
  > decorator pattern in Python programs. Although this can be done in specific situations,
  > in general the decorator pattern is best implemented with classes to represent the
  > decorator and the components it will wrap.

  - 이 KB에서 GoF 데코레이터 패턴 자체에 대한 판정은 다른 소스가 갖는다 —
    [층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md)가 그 패턴을
    계층에 걸친 API 중복을 조장하는 것으로 다룬다. **두 판정은 겨냥이 다르다**: 이 소스는
    파이썬의 `@` 문법과 GoF 패턴이 같은 것이냐를 묻고, 저쪽은 그 패턴을 쓰는 것이 좋으냐를
    묻는다.

## 이어지는 페이지

- [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md) — 같은 장의
  뒷부분. `@cache`·`@lru_cache`·`@singledispatch`가 무엇을 주고 무슨 조건을 요구하는가
- [파이썬의 일급 함수](first-class-functions-in-python.md) — 앞 장. 데코레이터가 서 있는 바닥
- [일급 함수로 다시 쓰는 디자인 패턴](design-patterns-with-first-class-functions.md) —
  등록 데코레이터가 실제 설계 문제를 푸는 자리
- [객체 참조와 가변성](object-references-and-mutability.md) — 클로저가 보관하는 것이 값이 아니라
  바인딩이라는 말이 기대는 바닥. 가변 기본값이 함수 객체에 상태를 얹는 기제도 같은 자리에 있다
- [부수 효과 없는 함수](side-effect-free-functions.md) — "함수는 불투명해야 한다"는 요구를
  설계 조항으로 말하는 쪽
- [층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md) — GoF 데코레이터
  패턴 자체에 대한 판정이 있는 쪽
- [파이썬 데이터 모델](python-data-model.md) — `__call__`로 만드는 호출 가능한 객체가 이 장의
  클래스 기반 데코레이터의 재료다
- [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 9장 "Decorators and Closures"(pp.303–340) — 도입(p.303) ·
    §"Decorators 101"(pp.304–306) · §"When Python Executes Decorators"(pp.306–307) ·
    §"Registration Decorators"(p.308) · §"Variable Scope Rules"(pp.308–310) ·
    곁글 "Comparing Bytecodes"(pp.310–311) · §"Closures"(pp.311–314) · §"The nonlocal
    Declaration"(pp.315–316) · §"Variable Lookup Logic"(pp.316–317) · §"Implementing a Simple
    Decorator"(pp.317–319) · §"How It Works"(pp.318–319) · 곁글 "Stacked Decorators"(p.322) ·
    §"Parameterized Decorators"(pp.329–335) · §"Chapter Summary"(p.336) · §"Further
    Reading"(pp.336–337) · 곁글 "Dynamic Scope Versus Lexical Scope"(pp.338–339) ·
    곁글 "Python Decorators and the Decorator Design Pattern"(pp.339–340).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 30). 예제 9-13은 원문 그대로이며 조판용 번호 표지만 제거했다.
    Figure 9-1(클로저 도해)은 이미지라 산문으로 옮겼다. 콘솔 세션 예제(9-1·9-3·9-4·9-9~9-11)는
    프롬프트가 섞여 복사해 돌릴 수 없으므로 펜스로 옮기지 않고 관측 결과만 서술했다.

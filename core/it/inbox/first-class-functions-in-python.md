---
type: concept
title: 파이썬의 일급 함수
description: 함수가 일급 객체라는 말이 정확히 무엇을 보장하는가와 그 위에서 무엇이 가능해지는가 — 일급 객체의 네 조건과 파이썬의 모든 함수가 일급이라는 단서, 고차 함수의 정의와 map·filter·reduce가 컴프리헨션에 자리를 내준 경위, 람다가 순수 식으로 제한되는 이유와 읽기 어려운 람다를 이름 있는 함수로 되돌리는 절차, 호출 가능한 것 아홉 갈래와 callable로 판정하기, __call__로 만드는 상태를 가진 함수 같은 객체, 위치 전용·키워드 전용 매개변수, operator와 functools.partial이 람다를 대신하는 자리, 그리고 파이썬이 함수형 언어가 아니라는 저자의 판정
generated: { by: "claude-opus-5", at: "2026-08-18T12:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬의 일급 함수

- [버전 조건](#버전-조건)
- [일급 객체의 네 조건](#일급-객체의-네-조건)
- [함수는 객체다](#함수는-객체다)
- [고차 함수](#고차-함수)
- [map·filter·reduce가 자리를 내준 경위](#mapfilterreduce가-자리를-내준-경위)
- [익명 함수의 자리와 그 한계](#익명-함수의-자리와-그-한계)
- [호출 가능한 것 아홉 갈래](#호출-가능한-것-아홉-갈래)
- [상태를 가진 함수 같은 객체](#상태를-가진-함수-같은-객체)
- [매개변수 선언의 세 구역](#매개변수-선언의-세-구역)
- [람다를 대신하는 표준 라이브러리](#람다를-대신하는-표준-라이브러리)
- [파이썬은 함수형 언어인가](#파이썬은-함수형-언어인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **함수가 "일급"이라는 말이 정확히 무엇을 보장하며, 그 위에서 무엇이 가능해지는가.**

## 버전 조건

> **버전 조건**: 호출 가능한 것이 아홉 갈래인 것은 **파이썬 3.9의 데이터 모델 문서 기준**이다.
> 초판에서는 일곱이었고, 네이티브 코루틴 함수(3.5)와 비동기 제너레이터 함수(3.6)가 더해져
> 아홉이 됐다. **위치 전용 매개변수(`/`)는 파이썬 3.8 이상**이고 3.7 이하에서는 문법 오류다.

## 일급 객체의 네 조건

- 규정 (7장 도입, p.231):[^ramalho2022]

  > Programming language researchers define a "first-class object" as a program entity that
  > can be:
  >
  > - Created at runtime
  > - Assigned to a variable or element in a data structure
  > - Passed as an argument to a function
  > - Returned as the result of a function

- 특별할 것 없는 성질이라는 것이 곧바로 붙는다 — **정수·문자열·딕셔너리도 파이썬에서 일급
  객체의 다른 예다 — 여기 대단한 것은 없다** (7장 도입, p.231).[^ramalho2022]
- 그 성질이 함수형 언어에만 있는 것도 아니다 — **함수를 일급 객체로 갖는 것은 Clojure·Elixir·
  Haskell 같은 함수형 언어의 본질적 기능이다. 그러나 일급 함수는 너무 유용해서 자바스크립트·
  Go·자바(JDK 8부터) 같은 인기 언어들이 채택했고, 그중 어느 것도 "함수형 언어"라고 주장하지
  않는다** (7장 도입, p.231).[^ramalho2022]
- **용어에 대한 단서 하나** — **"일급 함수(first-class functions)"라는 용어가 "일급 객체로서의
  함수"의 줄임으로 널리 쓰인다. 함수들 사이에 "엘리트"가 있음을 함의하므로 이상적이지는 않다.
  파이썬에서는 모든 함수가 일급이다** (7장 도입, p.232).[^ramalho2022]

## 함수는 객체다

- 실물로 확인하는 절차가 주어진다. 콘솔에서 함수를 만들고, 부르고, `__doc__` 속성을 읽고,
  그 함수 객체 자신이 `function` 클래스의 인스턴스임을 확인한다 (예제 7-1, 7장 §"Treating a
  Function Like an Object", pp.232–233).[^ramalho2022]
  - **`__doc__`은 함수 객체가 가진 여러 속성 중 하나**이고, **객체의 도움말 텍스트를 생성하는
    데 쓰인다** (7장 §"Treating a Function Like an Object", p.233).[^ramalho2022]
- 그리고 일급성이 관측된다 — 같은 함수를 다른 이름 `fact`에 대입해 그 이름으로 부를 수 있고,
  `map`에 인자로 넘길 수 있다 (예제 7-2, 7장 §"Treating a Function Like an Object",
  p.233).[^ramalho2022]

## 고차 함수

- 규정 — **함수를 인자로 받거나 함수를 결과로 돌려주는 함수를 고차 함수(higher-order
  function)라 한다** (7장 §"Higher-Order Functions", p.234).[^ramalho2022]
- 내장 `sorted`가 그 실물이다 — **선택적 `key` 인자는 정렬을 위해 각 항목에 적용될 함수를
  제공하게 해 준다.** 단어를 길이로 정렬하려면 `key`에 `len`을 넘기면 된다
  (7장 §"Higher-Order Functions", p.234).[^ramalho2022]
  - 그리고 `key`가 원본을 건드리지 않는다는 단서 — 단어를 거꾸로 쓴 철자로 정렬하는 예에서
    **리스트의 단어들은 전혀 바뀌지 않는다. 뒤집힌 철자가 정렬 기준으로 쓰일 뿐이다**
    (7장 §"Higher-Order Functions", p.234).[^ramalho2022] 명령과 질의를 반환값으로 가르는
    이 관례의 정본은 [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md)에 있다.
- 계보상 가장 알려진 고차 함수들도 열거된다 — **함수형 프로그래밍 패러다임에서 가장 잘 알려진
  고차 함수 중에는 `map`·`filter`·`reduce`·`apply`가 있다. `apply` 함수는 파이썬 2.3에서
  폐기되고 파이썬 3에서 제거되었다. 더는 필요하지 않기 때문이다** (7장 §"Higher-Order
  Functions", p.234).[^ramalho2022]

## map·filter·reduce가 자리를 내준 경위

- 판정 — **`map`과 `filter` 함수는 파이썬 3에서도 여전히 내장이지만, 리스트 컴프리헨션과
  제너레이터 식이 도입된 뒤로는 그만큼 중요하지 않다. 리스트컴프나 젠엑스프가 `map`과
  `filter`를 합친 일을 하면서도 더 읽기 쉽다** (7장 §"Modern Replacements for map, filter,
  and reduce", p.235).[^ramalho2022]
- 반환 타입의 변화도 기록돼 있다 — **파이썬 3에서 `map`과 `filter`는 이터레이터의 한 형태인
  제너레이터를 돌려주므로, 그 직접적 대체물은 이제 제너레이터 식이다(파이썬 2에서는 이
  함수들이 리스트를 돌려줬으므로 가장 가까운 대안이 리스트컴프였다)** (7장 §"Modern
  Replacements…", p.235).[^ramalho2022]
- `reduce`는 강등됐다 — **`reduce` 함수는 파이썬 2의 내장에서 파이썬 3의 `functools` 모듈로
  강등되었다. 가장 흔한 사용 사례인 합산은 2003년 파이썬 2.3에 나온 내장 `sum`이 더 잘
  처리한다. 가독성과 성능 양쪽에서 큰 승리다** (7장 §"Modern Replacements…",
  p.235).[^ramalho2022]
- 둘의 공통 발상 — **`sum`과 `reduce`의 공통 발상은 어떤 연산을 계열의 연속된 항목에 적용하면서
  이전 결과를 누적해, 값들의 계열을 하나의 값으로 줄이는 것이다** (7장 §"Modern
  Replacements…", p.236).[^ramalho2022] 같은 계열의 다른 내장이 `all`과 `any`인데, **`all([])`은
  `True`를 돌려주고 `any([])`는 `False`를 돌려준다** (7장 §"Modern Replacements…",
  p.236).[^ramalho2022]

## 익명 함수의 자리와 그 한계

- 규정과 제약 — **`lambda` 키워드는 파이썬 식 안에 익명 함수를 만든다. 그러나 파이썬의 단순한
  문법은 람다 함수의 몸을 순수한 식(pure expressions)으로 제한한다. 다시 말해 몸에 `while`·
  `try` 같은 다른 파이썬 문장이 들어갈 수 없다. `=`을 쓰는 대입도 문장이므로 람다 안에 올 수
  없다** (7장 §"Anonymous Functions", p.236).[^ramalho2022]
  - 대입 식(`:=`)에 대한 판정도 붙는다 — **`:=`을 쓰는 새 대입 식 문법은 쓸 수 있다 — 그러나
    그것이 필요하다면 당신의 람다는 아마 너무 복잡하고 읽기 어려우며, `def`를 써서 평범한
    함수로 리팩터링되어야 한다** (7장 §"Anonymous Functions", p.236).[^ramalho2022]
- 쓸 자리 — **익명 함수의 최선의 쓰임은 고차 함수의 인자 목록이라는 맥락 안이다**
  (7장 §"Anonymous Functions", p.237).[^ramalho2022] 그 바깥에서는 **파이썬에서 익명 함수가
  유용한 경우가 드물다** (7장 §"Anonymous Functions", p.237).[^ramalho2022]
- **읽기 어려운 람다를 되돌리는 절차**가 Fredrik Lundh의 것으로 인용된다 (곁글 "Fredrik
  Lundh's lambda Refactoring Recipe", 7장 §"Anonymous Functions", p.237):[^ramalho2022]
  1. **그 람다가 도대체 무엇을 하는지 설명하는 주석을 쓴다.**
  2. **그 주석을 잠시 들여다보고, 주석의 본질을 붙잡는 이름을 생각해 낸다.**
  3. **그 이름을 써서 람다를 `def` 문장으로 바꾼다.**
  4. **주석을 지운다.**
  - **주석을 쓴 다음 지우는 절차라는 것이 이 처방의 핵심이다.** 주석이 이름으로 승격되고 나면
    주석은 남을 이유가 없다. 같은 요구가 이 KB의 다른 축에도 있다 —
    [주석은 뻔하지 않은 것을 적는다](comments-describe-the-nonobvious.md)와
    [이름 짓기](naming-things.md)를 보라.
- 마지막으로 정체를 밝힌다 — **`lambda` 문법은 문법 설탕일 뿐이다: 람다 식은 `def` 문장과
  똑같이 함수 객체를 만든다** (7장 §"Anonymous Functions", p.237).[^ramalho2022]

## 호출 가능한 것 아홉 갈래

- **호출 연산자 `()`는 함수 말고 다른 객체에도 적용될 수 있다. 어떤 객체가 호출 가능한지
  판정하려면 `callable()` 내장 함수를 쓴다. 파이썬 3.9 기준으로 데이터 모델 문서는 아홉 개의
  호출 가능한 타입을 열거한다** (7장 §"The Nine Flavors of Callable Objects",
  p.237).[^ramalho2022]

  | 갈래 | 무엇인가 |
  |---|---|
  | 사용자 정의 함수 | `def` 문장이나 `lambda` 식으로 만들어진 것 |
  | 내장 함수 | `len`이나 `time.strftime`처럼 C로 구현된 함수(CPython 기준) |
  | 내장 메서드 | `dict.get`처럼 C로 구현된 메서드 |
  | 메서드 | 클래스의 몸에 정의된 함수 |
  | 클래스 | 호출되면 `__new__`로 인스턴스를 만들고 `__init__`로 초기화한 뒤 인스턴스를 호출자에게 돌려준다 |
  | 클래스 인스턴스 | 클래스가 `__call__` 메서드를 정의하면 그 인스턴스를 함수처럼 부를 수 있다 |
  | 제너레이터 함수 | 몸에 `yield`를 쓰는 함수나 메서드. 호출되면 제너레이터 객체를 돌려준다 |
  | 네이티브 코루틴 함수 | `async def`로 정의된 것. 호출되면 코루틴 객체를 돌려준다(3.5에 추가) |
  | 비동기 제너레이터 함수 | `async def`로 정의되고 몸에 `yield`가 있는 것. `async for`와 함께 쓸 비동기 제너레이터를 돌려준다(3.6에 추가) |

  (7장 §"The Nine Flavors of Callable Objects", pp.238–239)[^ramalho2022]
- 클래스가 호출 가능한 이유가 언어 설계에서 따라 나온다 — **파이썬에는 `new` 연산자가 없으므로
  클래스를 부르는 것은 함수를 부르는 것과 같다** (7장 §"The Nine Flavors…",
  p.238).[^ramalho2022]
- 뒤의 셋은 성격이 다르다 — **제너레이터·네이티브 코루틴·비동기 제너레이터 함수는 다른
  호출 가능한 것들과 달리 반환값이 결코 애플리케이션 데이터가 아니고, 애플리케이션 데이터를
  내놓거나 유용한 일을 하려면 추가 처리를 요구하는 객체다** (7장 §"The Nine Flavors…",
  p.238).[^ramalho2022]
- 그래서 판정 방법이 하나로 좁혀진다 — **파이썬에 존재하는 호출 가능한 타입의 다양성을 고려하면,
  어떤 객체가 호출 가능한지 판정하는 가장 안전한 방법은 `callable()` 내장을 쓰는 것이다**
  (7장 §"The Nine Flavors…", p.239).[^ramalho2022]

## 상태를 가진 함수 같은 객체

- **파이썬 함수가 진짜 객체일 뿐 아니라, 임의의 파이썬 객체도 함수처럼 굴게 만들 수 있다.
  인스턴스 메서드 `__call__`을 구현하는 것이 전부다** (7장 §"User-Defined Callable Types",
  p.239).[^ramalho2022]

- 아래가 그 실물이자 이 페이지의 대표 코드다. 임의의 이터러블로 만들어 항목을 뒤섞어
  보관하고, 인스턴스를 부르면 항목 하나를 꺼낸다. **`__init__`이 받은 이터러블로 지역 사본을
  만드는 것**이 눈여겨볼 자리다 — **인자로 넘어온 어떤 리스트에도 예상치 못한 부수 효과가
  생기는 것을 막는다** (7장 §"User-Defined Callable Types" 예제 7-8,
  pp.239–240).[^ramalho2022]

  ```python
  import random

  class BingoCage:

      def __init__(self, items):
          self._items = list(items)
          random.shuffle(self._items)

      def pick(self):
          try:
              return self._items.pop()
          except IndexError:
              raise LookupError('pick from empty BingoCage')

      def __call__(self):
          return self.pick()
  ```

- 쓸 자리가 두 개로 지목된다 (7장 §"User-Defined Callable Types", p.240):[^ramalho2022]

  > A class implementing `__call__` is an easy way to create function-like objects that have
  > some internal state that must be kept across invocations, like the remaining items in
  > the `BingoCage`. Another good use case for `__call__` is implementing decorators.

  - 데코레이터 쪽 이유가 명시된다 — **데코레이터는 호출 가능해야 하고, 데코레이터의 호출들
    사이에 무언가를 "기억"하거나(예: 메모이제이션 — 비싼 계산의 결과를 나중에 쓰려고
    캐싱하는 것) 복잡한 구현을 별도 메서드로 나누는 것이 때로 편리하다** (7장 §"User-Defined
    Callable Types", p.240).[^ramalho2022]
- **그리고 같은 목적의 다른 길이 예고된다** — **내부 상태를 가진 함수를 만드는 함수형 접근은
  클로저를 쓰는 것이다** (7장 §"User-Defined Callable Types", p.240).[^ramalho2022] 그 길은
  [클로저와 데코레이터](closures-and-decorators.md)가 갖는다. 같은 요구에 대한 **두 답이 이
  소스 안에 나란히 있다는 것**이 이 두 페이지를 잇는 축이다.

## 매개변수 선언의 세 구역

- 저자의 평가부터 — **파이썬 함수의 최고의 기능 중 하나는 극도로 유연한 매개변수 처리
  기제다** (7장 §"From Positional to Keyword-Only Parameters", p.240).[^ramalho2022]
- **키워드 전용 인자(keyword-only arguments)는 파이썬 3의 기능이다. 함수를 정의할 때 키워드
  전용 인자를 지정하려면 `*`이 붙은 인자 뒤에 이름을 둔다. 가변 위치 인자를 지원하고 싶지는
  않지만 키워드 전용 인자는 원한다면 시그니처에 `*` 하나만 따로 둔다**
  (7장 §"From Positional to Keyword-Only Parameters", p.242).[^ramalho2022]
  - **기본값이 필요하지 않다는 단서** — **키워드 전용 인자는 기본값을 가질 필요가 없다:
    필수일 수 있다** (7장 §"From Positional to Keyword-Only Parameters",
    p.242).[^ramalho2022]
- **위치 전용 매개변수(positional-only parameters)는 파이썬 3.8부터 사용자 정의 함수 시그니처에
  쓸 수 있다. 이 기능은 `divmod(a, b)`처럼 위치 매개변수로만 부를 수 있고 `divmod(a=10, b=4)`
  로는 부를 수 없는 내장 함수에는 언제나 있었다. 위치 전용 매개변수를 요구하는 함수를 정의하려면
  매개변수 목록에 `/`를 쓴다. `/` 왼쪽의 모든 인자가 위치 전용이다** (7장 §"Positional-Only
  Parameters", p.242).[^ramalho2022]
  - 버전 조건: 파이썬 3.8 이상. **매개변수 목록의 `/`는 파이썬 3.7 이하에서 문법 오류다**
    (7장 §"Positional-Only Parameters", p.243).[^ramalho2022]

## 람다를 대신하는 표준 라이브러리

- 전제 — **Guido는 파이썬을 함수형 프로그래밍 언어로 설계하지 않았음을 분명히 하지만, 일급
  함수·패턴 매칭, 그리고 `operator`와 `functools` 같은 패키지의 지원 덕분에 함수형 코딩
  스타일을 상당한 정도로 쓸 수 있다** (7장 §"Packages for Functional Programming",
  p.243).[^ramalho2022]
- **`operator` 모듈은 수십 개 연산자에 대한 함수 등가물을 제공해서 `lambda a, b: a*b` 같은
  사소한 함수를 코딩하지 않아도 되게 해 준다** (7장 §"The operator Module",
  p.244).[^ramalho2022]
  - 같은 계열의 다른 묶음 — **`operator`가 대체하는 또 한 무리의 한 수 재주 람다는 시퀀스에서
    항목을 고르거나 객체에서 속성을 읽는 함수들이다: `itemgetter`와 `attrgetter`가 그것을
    하는 맞춤 함수를 만들어 내는 팩토리다** (7장 §"The operator Module", p.244).[^ramalho2022]
  - `itemgetter(1)`은 **컬렉션을 주면 색인 1의 항목을 돌려주는 함수를 만든다. 같은 일을 하는
    `lambda fields: fields[1]`보다 쓰고 읽기 쉽다** (7장 §"The operator Module",
    p.244).[^ramalho2022] 색인이 아니라 `[]` 연산자에 기대므로 **시퀀스뿐 아니라 매핑과
    `__getitem__`을 구현하는 어떤 클래스도 지원한다** (7장 §"The operator Module",
    p.245).[^ramalho2022]
  - `attrgetter`는 **이름으로 객체 속성을 뽑는 함수를 만들고**, 인자 이름에 점이 있으면
    **중첩된 객체를 타고 들어가 속성을 가져온다** (7장 §"The operator Module",
    p.245).[^ramalho2022]
  - `methodcaller`는 **인자로 주어진 객체에 대해 이름으로 메서드를 부르는 함수를 만들고**,
    `functools.partial`처럼 일부 인자를 얼려 두는 부분 적용도 할 수 있다 (7장 §"The operator
    Module", pp.246–247).[^ramalho2022]
- **`functools.partial`** — **호출 가능한 것을 주면 원래 호출 가능한 것의 인자 일부가 미리
  정해진 값에 묶인 새 호출 가능한 것을 만들어 낸다. 이것은 인자를 하나 이상 받는 함수를 더 적은
  인자의 콜백을 요구하는 API에 맞추는 데 유용하다** (7장 §"Freezing Arguments with
  functools.partial", p.247).[^ramalho2022]
  - 만들어진 객체는 원본을 감춘 것이 아니다 — **`functools.partial` 객체는 원래 함수와 고정된
    인자에 접근하게 해 주는 속성들을 갖는다**(`func`·`args`·`keywords`) (7장 §"Freezing
    Arguments…", p.249).[^ramalho2022]
  - 메서드용 판도 있다 — **`functools.partialmethod` 함수는 `partial`과 같은 일을 하되
    메서드와 함께 동작하도록 설계됐다** (7장 §"Freezing Arguments…", p.249).[^ramalho2022]
- 같은 모듈의 나머지는 다음 장으로 넘어간다 — **`functools` 모듈은 `cache`와 `singledispatch`
  처럼 함수 데코레이터로 쓰도록 설계된 고차 함수도 담고 있다** (7장 §"Freezing Arguments…",
  p.249).[^ramalho2022] 그쪽은
  [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md)에 있다.

## 파이썬은 함수형 언어인가

- 저자의 답 (7장 곁글 "Is Python a Functional Language?", p.251):[^ramalho2022]

  > So there you have it: Python is not, by design, a functional language—whatever that
  > means. Python just borrows a few good ideas from functional languages.

- 근거 하나는 Guido 자신의 말이다 — 어떤 기능을 다른 언어에서 빌렸느냐는 질문에 **"파이썬에서
  좋은 것은 전부 다른 언어에서 훔쳐 온 것이다"**라고 답했고, 다른 글에서는 **`map`·`filter`·
  `reduce`가 애초에 파이썬에 `lambda`를 더한 동기였다**고 적는다 (7장 곁글, pp.250–251).[^ramalho2022]
- 분류학 자체를 기각하는 논거도 인용된다 — Shriram Krishnamurthi의 논문에서 **프로그래밍 언어
  "패러다임"은 지나간 시대의 죽어 가는 지루한 유산이다. 현대 언어 설계자들은 그것을 존중하지
  않는데 왜 우리 강의는 노예처럼 그것을 따르는가?**를 인용하고, 파이썬·루비·펄의 설계자들이
  **원하는 대로 기능을 빌려 와 규정을 완전히 거부하는 혼합물을 만든다**는 대목을 잇는다
  (7장 곁글, pp.250–251).[^ramalho2022]
  - Krishnamurthi의 주장을 저자가 요약한다 — **언어를 어떤 분류 체계에 넣으려 하기보다
    기능들의 집합으로 여기는 것이 더 유용하다** (7장 곁글, p.251).[^ramalho2022]
- 걸림돌 둘이 지목된다 (7장 곁글, p.251):[^ramalho2022]
  - **문장 지향 문법** — **파이썬은 식이 문장을 담을 수 없는 문장 지향 문법을 쓰고, 많은 언어
    구성물이 문장이다 — 람다를 쓸 때 내가 가장 자주 아쉬워하는 `try/catch`를 포함해서. 이것이
    파이썬의 높은 가독성에 치르는 값이다.**
  - **꼬리 호출 제거(tail-call elimination)의 부재** — **제한된 익명 함수 문법 말고 파이썬에서
    함수형 프로그래밍 관용구의 더 넓은 채택을 가로막는 가장 큰 장애물은 꼬리 호출 제거의
    부재다.** Guido가 그것을 도입하지 않은 이유를 든 글에서 **처음 셋이자 가장 중요한 이유가
    사용성 문제**라는 것을 저자가 짚는다.
- **익명 함수의 일반적 결함**도 파이썬 밖으로 일반화된다 — **파이썬 고유의 문법 제약을 넘어,
  익명 함수는 어느 언어에서든 심각한 결점을 갖는다: 이름이 없다는 것이다**
  (7장 곁글 "The Problem with Anonymous Functions", pp.251–252).[^ramalho2022]
  - 그 대가가 진단으로 이어진다 — **함수에 이름이 있으면 스택 추적을 읽기 쉽다. (…) 중첩된
    익명 함수가 많으면 디버깅과 오류 처리가 어려워진다** (7장 곁글, p.252).[^ramalho2022]

## 이어지는 페이지

- [클로저와 데코레이터](closures-and-decorators.md) — 다음 장. 내부 상태를 가진 함수를 만드는
  또 하나의 길이자 이 장의 일급성이 실제로 쓰이는 자리
- [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md) — 같은
  `functools`의 나머지
- [일급 함수로 다시 쓰는 디자인 패턴](design-patterns-with-first-class-functions.md) —
  이 장의 성질이 설계 문제 하나를 무너뜨리는 자리
- [파이썬 데이터 모델](python-data-model.md) — `__call__`이 속한 특수 메서드 체계
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 컴프리헨션과 제너레이터 식,
  그리고 `sorted`의 `key`가 처음 나오는 자리
- [이름 짓기](naming-things.md) — 람다를 이름 있는 함수로 되돌리는 처방이 기대는 요구
- [주석은 뻔하지 않은 것을 적는다](comments-describe-the-nonobvious.md) — 주석을 이름으로
  승격시키고 지우라는 같은 절차가 있는 쪽
- [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 7장 "Functions as First-Class Objects"(pp.231–252) — 도입
    (pp.231–232) · §"Treating a Function Like an Object"(pp.232–233) · §"Higher-Order
    Functions"(pp.234–236) · §"Modern Replacements for map, filter, and reduce"(pp.235–236) ·
    §"Anonymous Functions"(pp.236–237) · §"The Nine Flavors of Callable Objects"(pp.237–239) ·
    §"User-Defined Callable Types"(pp.239–240) · §"From Positional to Keyword-Only
    Parameters"(pp.240–242) · §"Positional-Only Parameters"(pp.242–243) · §"Packages for
    Functional Programming"(pp.243–249) · §"The operator Module"(pp.243–247) · §"Freezing
    Arguments with functools.partial"(pp.247–249) · 곁글 "Is Python a Functional
    Language?"(pp.250–251) · 곁글 "The Problem with Anonymous Functions"(pp.251–252).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 30). 예제 7-8은 원문 그대로이며 조판용 번호 표지만 제거했다.
    Figure 7-1(`help(factorial)` 화면)은 이미지라 산문으로 옮겼다. 콘솔 세션 예제
    (7-1~7-7·7-10·7-13~7-18)는 프롬프트가 섞여 복사해 돌릴 수 없으므로 관측 결과만 서술했다.

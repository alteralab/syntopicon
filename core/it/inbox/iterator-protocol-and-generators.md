---
type: concept
title: 이터레이터 프로토콜과 제너레이터
description: 파이썬이 for 문 뒤에서 실제로 무엇을 부르는가 — iter 내장 함수의 세 단계와 옛 __getitem__ 폴백, 이터러블과 이터레이터를 가르는 선과 그 둘을 한 객체로 합치는 안티패턴, yield 하나가 클래스를 통째로 없애는 제너레이터의 기제, 게으름이 무엇을 아끼는가, 그리고 제너레이터 식과 제너레이터 함수 사이의 선택 기준
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 이터레이터 프로토콜과 제너레이터

- [for 문 뒤에서 무엇이 일어나는가](#for-문-뒤에서-무엇이-일어나는가)
- [이터러블과 이터레이터는 다른 것이다](#이터러블과-이터레이터는-다른-것이다)
- [이터러블을 자기 자신의 이터레이터로 만들지 마라](#이터러블을-자기-자신의-이터레이터로-만들지-마라)
- [yield 하나가 클래스를 없앤다](#yield-하나가-클래스를-없앤다)
- [제너레이터가 도는 순서](#제너레이터가-도는-순서)
- [게으름이 아끼는 것](#게으름이-아끼는-것)
- [제너레이터 식과 제너레이터 함수 사이](#제너레이터-식과-제너레이터-함수-사이)
- [낱말 정리 — 이터레이터와 제너레이터](#낱말-정리--이터레이터와-제너레이터)
- [먼저 표준 라이브러리를 보라](#먼저-표준-라이브러리를-보라)
- [타입 힌트](#타입-힌트)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **`for x in thing`이라고 쓸 때 인터프리터가 `thing`에게 정확히 무엇을 요구하며,
그 요구를 만족시키는 가장 싼 방법은 무엇인가.**

## for 문 뒤에서 무엇이 일어나는가

- 규정 — **파이썬이 어떤 객체 `x`를 순회해야 할 때마다, 자동으로 `iter(x)`를 부른다**
  (17장 §"Why Sequences Are Iterable: The iter Function", p.596).[^ramalho2022]
- `iter` 내장 함수의 절차가 세 단계다 (같은 절, p.596):[^ramalho2022]
  1. 객체가 `__iter__`를 구현하는지 검사하고, 구현하면 그것을 불러 이터레이터를 얻는다.
  2. `__iter__`가 없고 `__getitem__`이 있으면, `iter()`가 0부터 시작하는 색인으로 항목을
     가져오려 시도하는 이터레이터를 만든다.
  3. 그것도 실패하면 `TypeError`를 일으킨다 — 보통 `'C' object is not iterable`.
- 그래서 **모든 파이썬 시퀀스가 순회 가능하다: 정의상 그들은 전부 `__getitem__`을
  구현하기 때문이다** (같은 절, p.596).[^ramalho2022] 다만 저자는 새 코드에 그 경로를
  기대지 말라고 한다 — **표준 시퀀스들은 `__iter__`도 구현하고, 당신 것도 그래야 한다.
  `__getitem__`을 통한 순회는 하위 호환을 위해 존재하며 앞으로 사라질 수 있다** (같은 절,
  p.596).[^ramalho2022] 다만 같은 문장이 단서를 단다 — 파이썬 3.10 기준으로 폐기 예고된
  것은 아니고, 저자는 그것이 제거될 일은 없으리라 본다.
  - 버전 조건: 파이썬 3.10 기준. `__getitem__` 폴백은 이 판까지 살아 있고 폐기 예고도
    없다.
- 이 폴백이 **덕 타이핑(duck typing)의 극단적 형태**다 — **어떤 객체는 특수 메서드
  `__iter__`를 구현할 때뿐 아니라 `__getitem__`을 구현할 때에도 순회 가능한 것으로
  간주된다** (같은 절, p.597).[^ramalho2022] 그 결과 검사 방법이 갈린다.
  - 구스 타이핑 쪽 정의는 더 단순하지만 덜 유연하다 — **`__iter__` 메서드를 구현하면
    순회 가능한 것으로 간주된다. 하위 클래싱도 등록도 필요 없다. `abc.Iterable`이
    `__subclasshook__`를 구현하기 때문이다** (같은 절, p.597).[^ramalho2022]
  - 그래서 **가장 정확한 검사는 `isinstance(x, abc.Iterable)`이 아니라 `iter(x)`를 불러
    보고 `TypeError`를 처리하는 것이다 — `iter(x)`는 레거시 `__getitem__` 메서드까지
    고려하는데 `Iterable` ABC는 그러지 않기 때문이다** (같은 절, p.597).[^ramalho2022]
  - 다만 저자는 명시적 검사 자체를 대개 기각한다 — **검사 직후에 그 객체를 순회할
    참이라면 명시적 검사는 값을 못 할 수 있다. 순회 불가능한 것에 순회를 시도했을 때
    파이썬이 내는 예외가 충분히 분명하기 때문이다** (같은 절, p.598).[^ramalho2022] 검사가
    값을 하는 경우가 하나 지목돼 있다 — 지금 순회하지 않고 **나중에 순회하려고 객체를
    붙들고 있을 때**. 그때는 일찍 오류를 잡는 편이 디버깅을 쉽게 한다.
- 잘 안 알려진 두 인자 형태가 있다 — **`iter()`를 두 인자로 불러 함수나 호출 가능한
  객체로부터 이터레이터를 만들 수 있다. 첫 인자는 값을 만들기 위해 (인자 없이) 반복
  호출될 호출 가능한 것이고, 둘째 인자는 센티널(sentinel)이다: 그 호출 가능한 것이
  돌려주면 이터레이터가 그 값을 내놓는 대신 `StopIteration`을 일으키게 만드는 표지 값**
  (17장 §"Using iter with a Callable", p.598).[^ramalho2022] 공식 문서가 든 쓸모가 고정 폭
  블록 리더다 — 파일에서 64바이트씩 읽다가 빈 `bytes`가 나오면 멈춘다. 이때
  `functools.partial`이 필요한 이유는 **`iter()`에 주는 호출 가능한 것이 인자를 요구하면
  안 되기** 때문이다 (같은 절, p.599).[^ramalho2022]

## 이터러블과 이터레이터는 다른 것이다

- 정의 (17장 §"Iterables Versus Iterators", p.599):[^ramalho2022]

> *iterable*
> Any object from which the `iter` built-in function can obtain an iterator. Objects
> implementing an `__iter__` method returning an *iterator* are iterable. Sequences are
> always iterable, as are objects implementing a `__getitem__` method that accepts
> 0-based indexes.

  - 그리고 그 둘의 관계가 한 방향이다 — **파이썬은 이터러블에서 이터레이터를 얻는다**
    (같은 절, p.599).[^ramalho2022]
- 이터레이터 쪽 인터페이스는 메서드 둘뿐이다 (같은 절, p.600):[^ramalho2022]
  - `__next__` — 계열의 다음 항목을 돌려주고, 더 없으면 `StopIteration`을 일으킨다.
  - `__iter__` — `self`를 돌려준다. **이렇게 해야 이터레이터를 이터러블이 요구되는
    자리(예컨대 `for` 루프)에 쓸 수 있다.**
- 이 최소 인터페이스가 두 가지를 불가능하게 만든다 (같은 절, pp.602–603):[^ramalho2022]
  - **이터레이터에 요구되는 메서드가 `__next__`와 `__iter__`뿐이므로, 남은 항목이 있는지
    검사할 방법은 `next()`를 부르고 `StopIteration`을 잡는 것 말고 없다.**
  - **이터레이터를 "리셋"하는 것도 불가능하다.** 처음부터 다시 하려면 그 이터레이터를
    만들어 준 이터러블에 `iter()`를 다시 불러야 한다. 이터레이터 자신에게 `iter()`를
    불러 봐야 소용없다 — `Iterator.__iter__`가 `self`를 돌려주도록 구현돼 있어서 소진된
    이터레이터를 되돌리지 못한다.
  - 저자가 그 최소성을 옹호한다 — **실제로 모든 이터레이터가 리셋 가능한 것은 아니기
    때문에 그 최소 인터페이스가 합당하다. 예컨대 네트워크에서 패킷을 읽는 이터레이터라면
    되감을 방법이 없다** (같은 절, p.603).[^ramalho2022]
- `StopIteration`의 지위 — **이터레이터가 소진됐다는 신호다. 이 예외는 `for` 루프 로직의
  일부인 `iter()` 내장 함수에 의해 내부적으로 처리된다** (같은 절, p.600).[^ramalho2022]
  리스트 컴프리헨션·이터러블 언패킹 같은 다른 순회 문맥도 마찬가지다.
- 이터레이터인지 검사하는 법은 이터러블 쪽과 반대다 — **객체 `x`가 이터레이터인지 검사하는
  가장 좋은 방법은 `isinstance(x, abc.Iterator)`다. `Iterator.__subclasshook__` 덕분에 이
  검사는 `x`의 클래스가 `Iterator`의 실제 하위 클래스도 가상 하위 클래스도 아닐 때조차
  동작한다** (같은 절, p.602).[^ramalho2022] 그 근거로 저자가 표준 라이브러리 주석을 든다
  (같은 절, p.601):[^ramalho2022]

> Iterators in Python aren't a matter of type but of protocol. A large and changing
> number of builtin types implement *some* flavor of iterator. Don't check the type! Use
> hasattr to check for both "__iter__" and "__next__" attributes instead.

## 이터러블을 자기 자신의 이터레이터로 만들지 마라

- 진단 — **이터러블과 이터레이터를 만들 때 흔한 오류의 원인이 그 둘을 혼동하는 것이다**
  (17장 §"Don't Make the Iterable an Iterator for Itself", p.605).[^ramalho2022]
  구분의 정본이 한 문단이다 (같은 절, p.605):[^ramalho2022]
  - **이터러블은 `__iter__` 메서드를 갖고, 그것이 매번 새 이터레이터를 만들어 낸다.**
  - **이터레이터는 개별 항목을 돌려주는 `__next__` 메서드와 `self`를 돌려주는 `__iter__`
    메서드를 구현한다.**
  - 따라서 **이터레이터도 이터러블이지만, 이터러블은 이터레이터가 아니다.**
- 유혹과 기각 — **`Sentence` 클래스에 `__iter__` 말고 `__next__`까지 구현해 각 인스턴스가
  동시에 이터러블이면서 자기 자신의 이터레이터이게 만들고 싶어질 수 있다. 그러나 이것이
  좋은 생각인 경우는 드물다. 구글에서 파이썬 코드를 검토한 경험이 많은 Alex Martelli에
  따르면 이것은 흔한 안티패턴이기도 하다** (같은 절, p.605).[^ramalho2022]
- 기각의 근거가 패턴 원전에 있다. *Design Patterns*의 이터레이터 패턴 "Applicability" 절이
  세 쓸모를 드는데 그중 하나가 **"집합 객체의 다중 순회를 지원하기 위해"**이고, 저자가 그
  요구를 풀어 적는다 — **다중 순회를 지원하려면 같은 이터러블 인스턴스에서 독립적인
  이터레이터를 여럿 얻을 수 있어야 하고, 각 이터레이터는 자기 내부 상태를 따로 유지해야
  한다. 그래서 패턴의 올바른 구현은 `iter(my_iterable)` 호출마다 새롭고 독립적인
  이터레이터를 만들 것을 요구한다** (같은 절, p.605).[^ramalho2022]

## yield 하나가 클래스를 없앤다

- 정의 — **몸통에 `yield` 키워드가 있는 파이썬 함수는 전부 제너레이터 함수(generator
  function)다: 호출되면 제너레이터 객체를 돌려주는 함수. 달리 말해 제너레이터 함수는
  제너레이터 공장이다** (17장 §"How a Generator Works", p.607).[^ramalho2022]
- 문법적 구별은 그 한 낱말뿐이다 — **평범한 함수와 제너레이터 함수를 가르는 유일한 문법은
  후자의 몸통 어딘가에 `yield` 키워드가 있다는 사실이다** (같은 절, p.607).[^ramalho2022]
  `def` 대신 `gen` 같은 새 키워드를 쓰자는 제안이 있었으나 Guido가 받아들이지 않았고 그
  논거가 PEP 255에 있다.
- 어휘를 엄밀하게 쓰라는 요구가 명시돼 있다 (같은 절, p.608):[^ramalho2022]

> Functions return values. Calling a generator function returns a generator. A generator
> yields values. A generator doesn't "return" values in the usual way: the return
> statement in the body of a generator function causes `StopIteration` to be raised by
> the generator object.

- 그 결과 이터레이터 클래스가 통째로 사라진다 — 고전 이터레이터 패턴을 손으로 짠
  `SentenceIterator`는 **대부분의 코드가 이터레이터의 내부 상태를 관리하는 일**이었는데
  (17장 §"Sentence Take #2: A Classic Iterator", p.604),[^ramalho2022] 제너레이터판에서는
  **별도의 이터레이터 클래스가 필요 없다** (17장 §"Sentence Take #3: A Generator Function",
  p.606).[^ramalho2022] `__iter__`가 제너레이터 함수이므로, 그것을 부르면 인터프리터가
  제너레이터 객체를 자동으로 만들어 준다.
- 제너레이터 함수는 `StopIteration`을 손으로 일으키지 않는다 — **명시적 `return`은 필요
  없다. 함수가 그냥 끝까지 "떨어져" 자동으로 반환할 수 있다. 어느 쪽이든 제너레이터
  함수는 `StopIteration`을 일으키지 않는다: 값을 다 만들면 그냥 빠져나간다** (같은 절,
  p.606).[^ramalho2022] 그 예외는 제너레이터 객체가 대신 일으킨다.

## 제너레이터가 도는 순서

- 기제 — **제너레이터 함수는 함수의 몸통을 감싸는 제너레이터 객체를 짓는다. 그 객체에
  `next()`를 부르면 실행이 함수 몸통의 다음 `yield`까지 나아가고, 그 `next()` 호출은 함수
  몸통이 중단될 때 내놓은 값으로 평가된다. 마지막으로, 함수 몸통이 반환하면 파이썬이 만든
  바깥 제너레이터 객체가 이터레이터 프로토콜에 맞춰 `StopIteration`을 일으킨다** (17장
  §"How a Generator Works", p.608).[^ramalho2022]
- 그래서 `for` 루프와 제너레이터 몸통의 출력이 서로 끼어든다. 저자의 실험용 `gen_AB`는
  `print`를 사이사이에 넣어 그것을 보인다 — 첫 암묵적 `next()`가 `'start'`를 찍고 첫
  `yield`에서 멈추며, 셋째 호출이 `'end.'`를 찍고 몸통 끝으로 떨어져 `StopIteration`을
  일으킨다 (같은 절, pp.609–610).[^ramalho2022]

## 게으름이 아끼는 것

- 규정 — **이터레이터 인터페이스는 게으르도록(lazy) 설계됐다: `next(my_iterator)`가 한
  번에 한 항목을 내놓는다. 게으름의 반대는 조급함(eager)이고, 게으른 평가와 조급한 평가는
  프로그래밍 언어 이론의 기술 용어다** (17장 §"Sentence Take #4: Lazy Generator",
  p.610).[^ramalho2022]
- 저자가 자기 앞선 구현을 스스로 기각한다 — **지금까지의 `Sentence` 구현들은 게으르지
  않았다. `__init__`이 텍스트의 모든 낱말 리스트를 조급하게 지어 `self.words` 속성에
  묶기 때문이다. 이것은 텍스트 전체를 처리해야 하고, 그 리스트는 텍스트 자체만큼의 메모리를
  쓸 수 있다. 사용자가 첫 몇 낱말만 순회한다면 이 일의 대부분이 헛수고다** (같은 절,
  p.610).[^ramalho2022]
- 처방이 표준 라이브러리에 이미 있다 — **`re.finditer` 함수는 `re.findall`의 게으른
  판이다. 리스트 대신 `re.MatchObject` 인스턴스를 요구에 따라 내놓는 제너레이터를 돌려준다.
  일치가 많으면 `re.finditer`가 메모리를 많이 아낀다** (같은 절, p.610).[^ramalho2022]
  그렇게 고친 판이 이 페이지의 대표 코드다 (예제 17-8, p.611):[^ramalho2022]

  ```python
  import re
  import reprlib

  RE_WORD = re.compile(r'\w+')


  class Sentence:

      def __init__(self, text):
          self.text = text

      def __repr__(self):
          return f'Sentence({reprlib.repr(self.text)})'

      def __iter__(self):
          for match in RE_WORD.finditer(self.text):
              yield match.group()
  ```

  - 이 열 몇 줄이 앞의 두 판을 대체한다. 낱말 리스트가 없어졌고, 이터레이터 클래스도
    없어졌고, `__init__`이 하는 일은 문자열을 붙드는 것뿐이다. 찾을 것은 `finditer`와
    `yield`다.

## 제너레이터 식과 제너레이터 함수 사이

- 대응 — **리스트 컴프리헨션이 리스트를 짓듯, 제너레이터 식은 제너레이터 객체를 짓는다**
  (17장 §"Sentence Take #5: Lazy Generator Expression", p.611).[^ramalho2022] 그리고
  **제너레이터 식은 문법 설탕이다: 언제나 제너레이터 함수로 바꿔 쓸 수 있지만 때때로 더
  편하다** (같은 절, p.613).[^ramalho2022]
- 선택 기준이 명시돼 있다 (17장 §"When to Use Generator Expressions",
  p.613):[^ramalho2022]
  - **제너레이터 함수가 더 유연하다: 여러 문장으로 복잡한 로직을 짤 수 있고, 코루틴으로
    쓸 수도 있다.**
  - **더 단순한 경우에는 제너레이터 식이 한눈에 읽기 쉽다.**
  - 저자의 엄지 규칙 — **제너레이터 식이 두어 줄을 넘어가면, 읽기 쉬움을 위해 제너레이터
    함수를 짜는 쪽을 택한다.**
- 문법 단서 하나 — **제너레이터 식이 함수나 생성자에 유일한 인자로 넘어갈 때는 함수 호출용
  괄호와 제너레이터 식을 감싸는 괄호를 따로 쓸 필요가 없다. 한 쌍이면 된다** (같은 절
  §"Syntax Tip", p.614).[^ramalho2022] 다만 제너레이터 식 뒤에 다른 인자가 더 있으면
  괄호로 감싸야 `SyntaxError`를 피한다.

## 낱말 정리 — 이터레이터와 제너레이터

- 저자가 용어 혼란을 인정하고 자기 정의를 고정한다 — **공식 파이썬 문서와 코드베이스에서
  이터레이터와 제너레이터를 둘러싼 용어는 일관되지 않고 변하는 중이다** (17장
  §"Contrasting Iterators and Generators", p.614).[^ramalho2022] 그가 채택한 정의가 둘이다
  (같은 절, p.614):[^ramalho2022]
  - *이터레이터* — **`__next__` 메서드를 구현하는 모든 객체를 가리키는 일반 용어.**
    클라이언트 코드가 소비할 데이터를 만들도록 설계된다. **실무에서 우리가 파이썬에서 쓰는
    이터레이터 대부분은 제너레이터다.**
  - *제너레이터* — **파이썬 컴파일러가 지은 이터레이터.** 제너레이터를 만들려고 `__next__`를
    구현하지 않는다. 대신 `yield` 키워드로 제너레이터 함수를 만들고, 그것이 제너레이터
    객체의 공장이 된다. 제너레이터 식은 제너레이터 객체를 짓는 또 하나의 방법이다.
    **제너레이터 객체는 `__next__`를 제공하므로 이터레이터다.**
- 비동기 갈래도 같은 이름 아래 있다 — **파이썬 3.5부터 `async def`로 선언하는 비동기
  제너레이터(asynchronous generator)도 있다** (같은 절, p.614).[^ramalho2022] 그쪽은
  [동시 실행기와 asyncio](concurrent-executors-and-asyncio.md)가 다룬다.
- 용어집이 최근 *generator iterator*라는 낱말을 들여왔고 제너레이터 식 항목은 "이터레이터"를
  돌려준다고 적지만, **파이썬 자신에게 물으면 두 경우 다 제너레이터 객체다** — `type()`이
  둘 다 `<class 'generator'>`를 낸다 (같은 절, p.615).[^ramalho2022]

## 먼저 표준 라이브러리를 보라

- 조문 — **제너레이터를 구현할 때는 표준 라이브러리에 무엇이 있는지 알아 두라. 그러지
  않으면 바퀴를 다시 발명할 가능성이 높다** (17장 §"Arithmetic Progression with itertools",
  p.619).[^ramalho2022] 저자가 자기 손으로 짠 산술 수열 제너레이터를 `itertools.count`와
  `itertools.takewhile`의 조합 두 줄로 대체해 보이면서 그 말을 한다.
- 다만 대체가 공짜는 아니다 — **`itertools.count`는 `step`을 반복해서 더하므로, 그것이
  만드는 부동소수점 계열은 손으로 짠 판만큼 정밀하지 않다** (같은 절, p.619).[^ramalho2022]
  손으로 짠 판은 이전 결과에 더하는 대신 `begin + step * index`로 매번 다시 계산해
  **연속 덧셈이 쌓는 부동소수점 오차를 피한다** (17장 §"An Arithmetic Progression
  Generator", p.617).[^ramalho2022]
- 조합 가능성이 이 함수군의 핵심 성질이다 — **이 함수들의 훌륭한 특징이 그것이다:
  제너레이터를 인자로 받고 제너레이터를 돌려주므로 아주 여러 방식으로 조합할 수 있다**
  (17장 §"Generator Functions in the Standard Library", p.630).[^ramalho2022]
- 축약 함수 쪽에는 최적화 하나가 명시돼 있다 — **`all`과 `any`의 경우, `functools.reduce`가
  지원하지 않는 중요한 최적화가 있다: 그 둘은 단락 평가(short-circuit)를 한다. 즉 결과가
  정해지는 즉시 이터레이터 소비를 멈춘다** (17장 §"Iterable Reducing Functions",
  p.630).[^ramalho2022]
- 함수 카탈로그 자체(스물 몇 개의 표)는 이 KB에 옮기지 않았다 — 사유는
  `it/archive/ramalho2022/_progress.yaml`의 `skipped`에 있다.

## 타입 힌트

- 애노테이션용 타입이 `collections.abc`에 있다 — 이터러블 인자를 받는 함수는
  `Iterable[T]`로, 제너레이터를 돌려주는 함수는 `Iterator[T]`로 적는다 (17장
  §"Generic Iterable Types", pp.639–640).[^ramalho2022]
- **`Iterator` 타입은 `yield`를 쓰는 함수로 짠 제너레이터에도, 손으로 `__next__`를 짜
  넣은 클래스에도 같이 쓴다** (같은 절, p.640).[^ramalho2022] `collections.abc.Generator`도
  있지만 **이터레이터로 쓰이는 제너레이터에는 쓸데없이 장황하다.**
- 관계가 한 줄로 정리된다 — **`Iterator[T]`는 `Generator[T, None, None]`의 축약이다. 두
  애노테이션 다 "타입 `T`의 항목을 내놓지만 값을 소비하지도 반환하지도 않는 제너레이터"를
  뜻한다** (같은 절, p.641).[^ramalho2022] 소비하고 반환할 수 있는 제너레이터가 코루틴이고,
  그쪽은 [yield from과 고전 코루틴](yield-from-and-classic-coroutines.md)이 다룬다.
  - 버전 조건: 파이썬 3.9 이상. 그 아래를 지원해야 하면 `typing.Iterable`·
    `typing.Iterator`를 쓴다.

## 이어지는 페이지

- [yield from과 고전 코루틴](yield-from-and-classic-coroutines.md) — 같은 장의 뒷부분.
  제너레이터가 다른 제너레이터에 일을 위임하는 문법과, 같은 물건을 반대 방향(데이터를
  받는 쪽)으로 쓰는 코루틴
- [컨텍스트 매니저 프로토콜](context-manager-protocol.md) — 같은 `yield`가 순회와 무관하게
  쓰이는 자리. `@contextmanager`가 그 예다
- [동시 실행기와 asyncio](concurrent-executors-and-asyncio.md) — 이 프로토콜의 비동기 짝
  (`__aiter__`·`__anext__`)과 비동기 제너레이터
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 제너레이터 식이 메모리를
  아낀다는 그 페이지의 claim이 여기 프로토콜에 근거한다
- [시퀀스 프로토콜의 점진 구현](implementing-the-sequence-protocol.md) — `__getitem__`
  하나로 순회가 되는 그 폴백을 실제로 쓰는 자리
- [파이썬 데이터 모델](python-data-model.md) — 특수 메서드를 부르는 것이 인터프리터라는
  규칙의 정본. `for`가 `__iter__`를 부르는 것이 그 실물이다
- [디자인 패턴의 해부](design-pattern-anatomy.md) — 이터레이터 패턴이 언어에 흡수된 사례로
  합류한 자리
- [파이썬의 제어 흐름 기제](../synthesis/python-control-flow-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 17장 "Iterators, Generators, and Classic Coroutines"
    §"A Sequence of Words"(pp.594–596) · §"Why Sequences Are Iterable: The iter
    Function"(pp.596–598) · §"Using iter with a Callable"(pp.598–599) · §"Iterables Versus
    Iterators"(pp.599–603) · §"Sentence Classes with `__iter__`"(pp.603–610) ·
    §"Lazy Sentences"(pp.610–613) · §"When to Use Generator Expressions"(pp.613–614) ·
    §"Contrasting Iterators and Generators"(pp.614–615) · §"An Arithmetic Progression
    Generator"(pp.615–619) · §"Generator Functions in the Standard Library"(pp.619–630) ·
    §"Iterable Reducing Functions"(pp.630–631) · §"Generic Iterable Types"(pp.639–641).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    그림 17-1(Iterable·Iterator ABC의 UML)은 이미지로 조판돼 있어 캡션과 본문 서술로만
    옮겼다. 코드 펜스는 예제 17-8 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만
    제거했다. 표 17-1~17-6(제너레이터 함수 카탈로그)은 참조 자료라 옮기지 않았다.
    PDF 651·654·657쪽은 추출본이 훼손 판정(suspected_garbled_text)을 받아 그 쪽은
    인용하지 않았다 — 전부 카탈로그 표와 그 예제 출력이라 손실이 아니다.

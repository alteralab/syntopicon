---
type: concept
title: 시퀀스 프로토콜의 점진 구현
description: 프로토콜을 문서에만 있고 코드에는 없는 비형식 인터페이스로 규정하는 자리와 그 실무적 귀결 — 두 메서드로 시퀀스가 되지만 슬라이스가 제 타입을 돌려주지 않는다는 결손과 그 교정, 프로토콜을 일부만 구현해도 되는 이유와 정적 프로토콜에서는 그것이 허용되지 않는다는 대비, __getattr__을 구현하면 __setattr__도 함께 써야 하는 이유, 그리고 상속 대신 합성으로 컬렉션을 짓는 선택
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 시퀀스 프로토콜의 점진 구현

- [프로토콜 = 비형식 인터페이스](#프로토콜--비형식-인터페이스)
- [일부만 구현해도 된다](#일부만-구현해도-된다)
- [합성으로 짓는다](#합성으로-짓는다)
- [슬라이스를 아는 __getitem__](#슬라이스를-아는-__getitem__)
- [__getattr__을 쓰면 __setattr__도 쓴다](#__getattr__을-쓰면-__setattr__도-쓴다)
- [집계는 map-reduce로](#집계는-map-reduce로)
- [속성 처리 특수 메서드의 전체 지도](#속성-처리-특수-메서드의-전체-지도)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 클래스를 "시퀀스"로 만들려면 무엇을 구현해야 하고, 어디까지 구현할지를
무엇이 정하는가.**

## 프로토콜 = 비형식 인터페이스

- 정의 (12장 §"Protocols and Duck Typing", p.402):[^ramalho2022]

> In the context of object-oriented programming, a protocol is an informal interface,
> defined only in documentation and not in code.

  - 시퀀스 프로토콜(sequence protocol)의 내용은 두 메서드가 전부다 — **파이썬에서 시퀀스
    프로토콜은 `__len__`과 `__getitem__` 메서드만 수반한다. 표준 시그니처와 의미론으로 그
    메서드들을 구현하는 어떤 클래스 `Spam`이든 시퀀스가 기대되는 어디서나 쓰일 수 있다.
    `Spam`이 이것 또는 저것의 하위 클래스인지는 무관하다. 중요한 것은 그것이 필요한 메서드를
    제공한다는 것뿐이다** (같은 절, p.402).[^ramalho2022]
- 선언되지 않는다는 것이 이 정의의 핵심이다 — **`FrenchDeck` 클래스는 코드 어디에도 선언되지
  않았는데도 시퀀스 프로토콜을 구현하기 때문에 많은 파이썬 기능의 덕을 본다. 경험 있는 파이썬
  코더는 그것을 보고 그것이 `object`를 상속하더라도 시퀀스라는 것을 이해할 것이다. 우리가
  그것을 시퀀스라고 말하는 이유는 그것이 시퀀스처럼 **굴기** 때문이고, 그것이 중요한
  것이다** (12장 §"Protocols and Duck Typing", p.402).[^ramalho2022] 이것이
  **덕 타이핑(duck typing)**이라 불리게 되었다고 저자가 적는다.
- **낱말 하나에 뜻이 둘이라는 것을 이 장이 명시한다** — 파이썬 3.8이 PEP 544로 프로토콜
  클래스를 지원하면서 같은 낱말이 타이핑 구성물의 이름이 되었다. 저자의 구분 —
  **그 둘을 구별해야 할 때 나는 프로토콜 클래스로 형식화된 프로토콜을 가리키려면 *정적
  프로토콜*(static protocol)이라 쓰고, 전통적 의미로는 *동적 프로토콜*(dynamic protocol)이라
  쓴다. 한 가지 핵심 차이는 정적 프로토콜 구현은 프로토콜 클래스에 정의된 **모든** 메서드를
  제공해야 한다는 것이다** (12장 §"Protocols and Duck Typing", p.403).[^ramalho2022]
  두 프로토콜의 전면 대조는 [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)에
  있다.
- 파이썬만의 발명이 아니라는 것도 곁글에 적혀 있다 — **프로토콜은 파이썬의 발명이 아니다.
  "객체 지향"이라는 표현을 만들기도 한 스몰토크 팀이 지금 우리가 인터페이스라 부르는 것의
  동의어로 "프로토콜"을 썼다** (12장 곁글 §"Protocols as Informal Interfaces",
  p.427).[^ramalho2022] 그 환경에서도 그것은 **문서화와 탐색을 돕는 장치였을 뿐 언어가
  강제하지 않았다.**
  - 파이썬 문서에서 프로토콜이 논의되는 자리를 알아보는 신호를 저자가 준다 — **"파일 같은
    객체(a file-like object)"라는 표현을 볼 때다** (같은 곁글, p.427).[^ramalho2022]

## 일부만 구현해도 된다

- 조문 — **프로토콜은 비형식적이고 강제되지 않으므로, 클래스가 쓰일 구체적 문맥을 안다면
  프로토콜의 일부만 구현하고도 넘어갈 수 있는 경우가 많다. 예컨대 반복을 지원하려면
  `__getitem__`만 필요하고 `__len__`을 제공할 필요가 없다** (12장 §"Protocols and Duck
  Typing", pp.402–403).[^ramalho2022]
- **이것이 흐트러진 것이 아니라 단순함이라는 것이 저자의 판정이다** — **프로토콜의 일부만
  구현하는 것이 엉성하다고 생각할 수 있지만, 그것은 일을 단순하게 유지한다는 이점을 갖는다**
  (12장 곁글 §"Protocols as Informal Interfaces", p.427).[^ramalho2022] 근거로 언어 참조서를
  인용한다 (같은 곁글, p.427):[^ramalho2022]

> When implementing a class that emulates any built-in type, it is important that the
> emulation only be implemented to the degree that it makes sense for the object being
> modeled. For example, some sequences may work well with retrieval of individual elements,
> but extracting a slice may not make sense.

  - 저자의 귀결 — **과잉 설계된 인터페이스 계약을 채우고 컴파일러를 만족시키려고 말도 안 되는
    메서드를 코딩할 필요가 없을 때, KISS 원칙을 따르기가 더 쉬워진다** (같은 곁글,
    p.427).[^ramalho2022]
- **다만 조건이 붙는다** — **반면 타입 검사기로 당신의 프로토콜 구현을 검증하고 싶다면 더
  엄격한 프로토콜 정의가 필요하다. 그것이 `typing.Protocol`이 제공하는 것이다** (같은 곁글,
  p.427).[^ramalho2022] 즉 **점진 구현의 자유와 정적 검증은 맞바꾸는 관계**다.

## 합성으로 짓는다

- 이 장의 전략이 첫 절에 선언돼 있다 — **`Vector`를 구현하는 우리의 전략은 상속이 아니라
  합성(composition)을 쓰는 것이다. 우리는 성분들을 부동소수의 배열에 저장하고, 우리 `Vector`가
  불변 평면 시퀀스처럼 굴게 하는 데 필요한 메서드들을 구현할 것이다** (12장 §"Vector: A
  User-Defined Sequence Type", p.398).[^ramalho2022]
- 앞 장의 `Vector2d`를 상속하지 않은 이유가 둘로 적힌다 (12장 §"Vector Take #1: Vector2d
  Compatible", p.401):[^ramalho2022] **첫째, 호환되지 않는 생성자가 정말로 서브클래싱을
  권할 수 없게 만든다.** 둘째가 더 중요하다고 저자가 적는다 — **나는 `Vector`가 시퀀스
  프로토콜을 구현하는 독립된 예제이기를 원한다.**
- **생성자 시그니처에도 관례가 있다** — **시퀀스 생성자의 모범 사례는 모든 내장 시퀀스 타입이
  그러듯 생성자에서 데이터를 반복 가능한 인자로 받는 것이다** (12장 §"Vector Take #1:
  Vector2d Compatible", p.399).[^ramalho2022] `Vector(3, 4)`가 아니라 `Vector([3, 4])`인
  이유다.
- 큰 컬렉션의 `repr`에는 별도 조항이 있다 — `reprlib` 모듈로 길이를 제한한다. 근거 —
  **이것은 많은 수의 항목을 담을 수 있는 어떤 컬렉션 타입에서도 결정적인데, `repr`이
  디버깅에 쓰이기 때문이다 — 그리고 당신은 하나의 큰 객체가 콘솔이나 로그에서 수천 줄을
  차지하는 것을 원하지 않는다** (12장 §"Vector Take #1: Vector2d Compatible",
  p.399).[^ramalho2022]
  - 그 역할에서 따라오는 규칙 — **디버깅에서의 역할 때문에, 객체에 `repr()`을 부르는 것은
    결코 예외를 일으켜서는 안 된다. `__repr__` 구현 안에서 뭔가 잘못되면 당신은 그 문제를
    처리하고 사용자가 수신자(`self`)를 식별할 기회를 주는 쓸 만한 출력을 내도록 최선을 다해야
    한다** (같은 절, p.401).[^ramalho2022]

## 슬라이스를 아는 __getitem__

- `__len__`과 `__getitem__`을 내부 배열에 그대로 위임하는 한 줄짜리 구현으로도 색인·슬라이싱이
  일단 동작한다. 그런데 **슬라이스가 `Vector`가 아니라 `array`를 돌려준다.**
- 기준이 내장 타입이다 — **내장 시퀀스 타입들을 생각해 보라: 그 하나하나가 슬라이스될 때 다른
  어떤 타입이 아니라 자기 자신의 타입의 새 인스턴스를 만든다** (12장 §"Vector Take #2: A
  Sliceable Sequence", p.404).[^ramalho2022]
- 교정된 구현이 이 장의 대표 코드다 (12장 §"A Slice-Aware `__getitem__`" 예제 12-6,
  p.406):[^ramalho2022]

  ```python
  def __len__(self):
      return len(self._components)

  def __getitem__(self, key):
      if isinstance(key, slice):
          cls = type(self)
          return cls(self._components[key])
      index = operator.index(key)
      return self._components[index]
  ```

- **`isinstance` 검사가 여기서는 정당하다는 단서가 붙는다** — **`isinstance`의 과도한 사용은
  나쁜 객체 지향 설계의 신호일 수 있지만, `__getitem__`에서 슬라이스를 다루는 것은 정당한 사용
  사례다** (12장 §"A Slice-Aware `__getitem__`", p.407).[^ramalho2022]
- **정수 검사는 `isinstance`로 하지 않는다.** `operator.index()`가 `__index__` 특수 메서드를
  부르고, 그 함수와 특수 메서드는 PEP 357에서 정의됐다 — **`operator.index()`와 `int()`의
  핵심 차이는 전자가 이 특정한 목적을 위한 것이라는 점이다. 예컨대 `int(3.14)`는 3을 돌려주지만
  `operator.index(3.14)`는 `TypeError`를 일으킨다. 부동소수는 색인으로 쓰이면 안 되기
  때문이다** (12장 §"A Slice-Aware `__getitem__`", p.406).[^ramalho2022] 초판은 여기서
  `isinstance` 검사를 썼고 저자가 그것을 걷어 냈다.

## __getattr__을 쓰면 __setattr__도 쓴다

- `__getattr__`의 발동 조건 — **`__getattr__` 메서드는 속성 조회가 실패할 때 인터프리터에
  의해 호출된다. 간단히 말해 `my_obj.x`라는 식이 주어지면 파이썬은 `my_obj` 인스턴스에 `x`라는
  이름의 속성이 있는지 검사하고, 없으면 검색이 클래스로 가고 그다음 상속 그래프를 올라간다.
  `x` 속성이 발견되지 않으면 `my_obj`의 클래스에 정의된 `__getattr__` 메서드가 `self`와 속성의
  이름을 문자열로 받아 호출된다** (12장 §"Vector Take #3: Dynamic Attribute Access",
  p.408).[^ramalho2022]
- **그것만 구현하면 버그가 생긴다.** `v.x`가 성분을 돌려주다가 `v.x = 10`을 대입하면 오류 없이
  통과하고, 그 뒤로 `v.x`는 10을 돌려주는데 **벡터 성분은 바뀌지 않는다.** 원인이 위 규칙의
  귀결이다 — **파이썬은 객체가 그 이름의 속성을 갖지 않을 때에만 그 메서드를 대비책으로
  부른다. 그러나 우리가 `v.x = 10`을 대입하고 나면 `v` 객체는 이제 `x` 속성을 가지므로
  `__getattr__`은 더 이상 `v.x`를 조회하는 데 호출되지 않는다** (같은 절,
  p.409).[^ramalho2022]
- **그래서 조문이 나온다** (12장 §"Vector Take #3: Dynamic Attribute Access",
  p.411):[^ramalho2022]

> Very often when you implement `__getattr__`, you need to code `__setattr__` as well, to
> avoid inconsistent behavior in your objects.

  - 이 페이지가 이것을 옮긴 이유는 파이썬 문법 때문이 아니라 **짝을 이루는 특수 메서드를
    반쪽만 구현하면 객체가 조용히 거짓말을 한다**는 일반형 때문이다. 같은 구조가
    `__eq__`/`__hash__`에도 있고(11장), `+`/`+=`에도 있다(16장).
- **여기서 `__slots__`가 기각된다** — 클래스 수준의 `__slots__` 선언이 새 인스턴스 속성
  설정을 막는다는 것을 알면 `__setattr__` 대신 그것을 쓰고 싶어지지만, **`__slots__`의 모든
  단서 때문에 인스턴스 속성 생성을 막으려는 목적만으로 `__slots__`를 쓰는 것은 권장되지
  않는다. `__slots__`는 메모리를 아끼기 위해서만, 그리고 그것이 실제 문제일 때에만 쓰여야
  한다** (12장 §"Vector Take #3: Dynamic Attribute Access", p.411).[^ramalho2022]
  그 단서 목록은 [__slots__와 인스턴스 메모리](slots-and-instance-memory.md)에 있다.
- 오류 메시지를 고를 때도 표준 라이브러리를 봤다고 저자가 적는다 — 불변이면서 데이터 속성
  둘을 갖는 내장 `complex`의 문구와, 프로퍼티로 보호된 읽기 전용 속성의 문구를 둘 다 참고해
  더 명시적인 문장을 지었다 (12장 §"Vector Take #3: Dynamic Attribute Access",
  p.411).[^ramalho2022]

## 집계는 map-reduce로

- 성분이 수천 개일 수 있으면 `Vector2d`처럼 튜플을 만들어 해시하는 것이 비싸다. 대신 성분마다
  해시를 만들고 배타적 논리합(xor)으로 누적한다 — **매핑 단계가 성분마다 해시 하나를 만들고,
  축약 단계가 모든 해시를 xor 연산자로 집계한다** (12장 §"Vector Take #4: Hashing and a
  Faster ==", p.414).[^ramalho2022]
- **`reduce`에 초깃값을 주라는 조항이 있다** — **`reduce`를 쓸 때 세 번째 인자
  `reduce(function, iterable, initializer)`를 주는 것이 좋은 관행이다. 이 예외를 막기
  위해서다: `TypeError: reduce() of empty sequence with no initial value`. 초깃값은
  시퀀스가 비었을 때 반환되는 값이고 축약 루프의 첫 인자로 쓰이므로, 그것은 연산의 항등원이어야
  한다. 예를 들어 `+`·`|`·`^`에는 0이어야 하지만 `*`·`&`에는 1이어야 한다** (12장 §"Vector
  Take #4: Hashing and a Faster ==", p.414).[^ramalho2022]
- **`==`도 같은 이유로 다시 쓰인다.** `tuple(self) == tuple(other)`는 짧지만 **성분이 수천
  개일 수 있는 `Vector` 인스턴스에는 매우 비효율적이다. 그것은 튜플의 `__eq__`를 쓰려고 두
  피연산자의 내용 전체를 복사하는 튜플 둘을 만든다** (12장 §"Vector Take #4: Hashing and a
  Faster ==", p.415).[^ramalho2022] 대신 길이를 먼저 비교하고 `zip`으로 짝지어 `all`로
  집계한다.
  - **길이 비교가 생략될 수 없는 이유가 `zip`의 성질이다** — **`zip`은 입력 중 하나가 소진되는
    즉시 경고 없이 값 생성을 멈춘다** (12장 §"Vector Take #4: Hashing and a Faster ==",
    p.416).[^ramalho2022] 저자는 초판에서 이것을 API의 좋은 성질이 아니라고 적었고, 그 뒤
    PEP 618이 `strict` 인자를 더했다.
    - 버전 조건: 파이썬 3.10 이상에서 `zip(..., strict=True)`가 길이가 다르면 `ValueError`를
      일으킨다. 기본값은 `False`이므로 **3.10 이상에서도 명시하지 않으면 조용히 멈추는
      동작이 그대로다.**
- 이 장의 곁글 하나가 "파이썬다운 합계"를 찾던 2003년 메일링 리스트 논쟁을 통째로 옮겨 놓는데,
  그 결말이 언어에 남았다 — Alex Martelli가 제안한 `sum()` 함수가 대화 석 달 뒤 파이썬 2.3의
  내장이 되었고, 이듬해 파이썬 2.4의 제너레이터 식이 나오면서 저자가 가장 파이썬답다고 보는
  답이 완성됐다 (12장 곁글 §"The Search for a Pythonic Sum", pp.428–430).[^ramalho2022]
  같은 대화에서 `reduce`가 파이썬 3에서 내장에서 `functools` 모듈로 강등된 경위도 나온다 —
  **그것이 설명하기 어려운 코딩 관용을 부추겼기 때문이다.**
  - 그럼에도 저자는 자리를 남긴다 — **그래도 `functools.reduce`는 제 자리를 갖는다. 그것은
    우리 `Vector.__hash__` 문제를 내가 파이썬답다고 부를 방식으로 풀었다** (같은 곁글,
    p.430).[^ramalho2022]

## 속성 처리 특수 메서드의 전체 지도

위 [__getattr__을 쓰면 __setattr__도 쓴다](#__getattr__을-쓰면-__setattr__도-쓴다)가 짝으로
써야 하는 이유를 말한다면, 같은 소스의 22장이 그 둘이 놓인 자리 전체를 그린다.

- 다섯이 있다 (22장 §"Special Methods for Attribute Handling",
  pp.871–872):[^ramalho2022] `__delattr__`·`__dir__`·`__getattr__`·`__getattribute__`·
  `__setattr__`.
- 발동 조건이 갈린다.
  - `__getattr__` — **`obj`와 클래스, 그 상위 클래스들을 검색한 뒤 이름 붙은 속성을
    회수하려는 시도가 실패할 때에만 불린다** (같은 절, p.872).[^ramalho2022]
  - `__getattribute__` — **파이썬 코드에서 이름 붙은 속성을 직접 회수하려는 시도가 있을
    때마다 언제나 불린다. `__getattr__`은 `__getattribute__` 뒤에만, 그리고
    `__getattribute__`가 `AttributeError`를 일으킬 때에만 발동된다** (같은 절,
    p.872).[^ramalho2022] 무한 재귀를 피하려면 **`super().__getattribute__(obj,
    name)`을 써야 한다.**
  - `__setattr__` — **이름 붙은 속성을 설정하려는 시도가 있을 때마다 언제나 불린다**
    (같은 절, p.872).[^ramalho2022]
- 우회로가 명시돼 있다 — **인스턴스 `__dict__`에서 속성을 직접 읽고 쓰는 것은 이 특수
  메서드들을 발동시키지 않는다 — 그리고 그것이 필요할 때 그것들을 우회하는 통상적인
  방법이다** (같은 절, p.871).[^ramalho2022]
- 그리고 저자의 조문 하나가 이 페이지의 짝 규약에 무게를 더한다 (같은 절,
  p.872):[^ramalho2022]

> In practice, because they are unconditionally called and affect practically every
> attribute access, the `__getattribute__` and `__setattr__` special methods are harder
> to use correctly than `__getattr__`, which only handles nonexisting attribute names.
> Using properties or descriptors is less error prone than defining these special
> methods.

  - 즉 이 페이지가 보인 `__getattr__`/`__setattr__` 짝은 **이미 어려운 쪽 절반**이고,
    같은 일을 프로퍼티나 디스크립터로 하면 덜 위험하다는 것이 저자의 판정이다. 그
    대안들의 정본은 [동적 속성과 프로퍼티](dynamic-attributes-and-properties.md)와
    [속성 디스크립터](attribute-descriptors.md)에 있다.

## 이어지는 페이지

- [파이썬다운 객체 만들기](building-pythonic-objects.md) — 앞 장. 여기서 키우는 그
  `Vector2d`가 어떻게 지어졌는가
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 동적 프로토콜과 정적
  프로토콜의 전면 대조, 그리고 언제 ABC이고 언제 `Protocol`인가
- [파이썬 데이터 모델](python-data-model.md) — `__len__`과 `__getitem__` 둘로 시퀀스가 되는
  그 예제의 원래 자리
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 내장 시퀀스 쪽의 같은 이야기.
  슬라이스 객체와 평면 시퀀스가 무엇인가
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 여기서 기각된 용법의 원래
  목적과 그 단서들
- [파이썬의 연산자 오버로딩](operator-overloading-in-python.md) — 이 `Vector`에 중위 연산자를
  얹는 다음 자리
- [파이썬의 일급 함수](first-class-functions-in-python.md) — `reduce`와 `operator` 모듈이
  람다를 대신하는 자리
- [동적 속성과 프로퍼티](dynamic-attributes-and-properties.md) — 같은 특수 메서드들을
  더 안전하게 대신하는 층
- [속성 디스크립터](attribute-descriptors.md) — 그 층을 여러 속성에 재사용 가능하게
  일반화한 자리
- [추상화 고르기](choosing-abstractions.md) — 인터페이스를 얼마나 크게 잡을 것인가의 원리 쪽
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 12장 "Special Methods for Sequences", pp.397–430(도입
    pp.397–398 · §"Vector: A User-Defined Sequence Type" p.398 · §"Vector Take #1: Vector2d
    Compatible" pp.399–401 · §"Protocols and Duck Typing" pp.402–403 · §"Vector Take #2:
    A Sliceable Sequence" pp.403–404 · §"A Slice-Aware `__getitem__`" pp.406–407 ·
    §"Vector Take #3: Dynamic Attribute Access" pp.407–411 · §"Vector Take #4: Hashing and
    a Faster ==" pp.411–416과 곁글 §"The Awesome zip" pp.416–418 · §"Vector Take #5:
    Formatting" pp.418–425 · §"Chapter Summary" pp.425–426 · 곁글 §"Protocols as Informal
    Interfaces" p.427 · 곁글 §"The Search for a Pythonic Sum" pp.428–430).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    **§"How Slicing Works"(pp.404–405)에서 인쇄판 405쪽은 추출본이 훼손 판정
    (suspected_garbled_text)을 받아 그 쪽에서는 아무것도 인용하지 않았다** — 그 쪽은 `slice`
    객체의 속성과 `indices` 메서드를 콘솔 세션으로 보이는 자리이고, 이 페이지가 그 절에서
    쓴 것(대괄호 안의 콤마가 `__getitem__`에 튜플을 넘긴다는 사실)은 404쪽에서 왔다.
    §"Vector Take #5: Formatting"의 초구면 좌표 수학은 옮기지 않았다 — 저자 자신이
    "구현 세부"라 부르고 위키백과 공식을 각색한 것이라고 밝힌 자리다.
    Figure 12-1(축약 함수)·12-2(map-reduce)는 이미지로 조판돼 있어 캡션의 뜻만 본문 서술로
    풀었다. 코드 펜스는 예제 12-6 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만
    제거했다.
    §"속성 처리 특수 메서드의 전체 지도"는 2026-08-18-10 런에서 같은 소스의 22장
    "Dynamic Attributes and Properties" §"Special Methods for Attribute
    Handling"(pp.871–872)에서 합류했다.

---
type: concept
title: 동적 속성과 프로퍼티
description: 저장된 값과 계산된 값을 같은 표기로 읽게 만드는 균일 접근 원칙과 그 원칙이 실무에서 사 오는 대가, __getattr__이 언제 불리고 __getattribute__·__setattr__과 어떻게 갈리는가, 프로퍼티가 클래스 속성이면서 인스턴스 속성을 가로채는 기제, 계산 결과를 캐시할 때 드러나는 세 함정, 그리고 반복되는 접근자를 프로퍼티 팩토리로 접는 법
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 동적 속성과 프로퍼티

- [균일 접근 원칙과 그 대가](#균일-접근-원칙과-그-대가)
- [가상 속성과 __getattr__](#가상-속성과-__getattr__)
- [__new__는 생성자이고 __init__은 초기화자다](#__new__는-생성자이고-__init__은-초기화자다)
- [프로퍼티는 인스턴스 속성을 가린다](#프로퍼티는-인스턴스-속성을-가린다)
- [계산 결과를 캐시할 때의 세 함정](#계산-결과를-캐시할-때의-세-함정)
- [검증을 위한 프로퍼티](#검증을-위한-프로퍼티)
- [프로퍼티 팩토리](#프로퍼티-팩토리)
- [속성을 다루는 API 지도](#속성을-다루는-api-지도)
- [공개 속성으로 시작해도 된다](#공개-속성으로-시작해도-된다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **`obj.attr`이라는 한 표기 뒤에 저장된 값 대신 계산이나 검증을 끼워 넣으려면
무엇을 쓰고, 그것이 언제 발동하는가.**

## 균일 접근 원칙과 그 대가

- 출발점이 Bertrand Meyer의 원칙이다 (22장 도입, p.835):[^ramalho2022]

> All services offered by a module should be available through a uniform notation, which
> does not betray whether they are implemented through storage or through computation.

- 파이썬 쪽 용어가 그 위에 얹힌다 — **데이터 속성과 메서드를 파이썬에서는 통틀어
  속성(attributes)이라 부른다. 메서드는 호출 가능한 속성이다. 동적 속성(dynamic
  attributes)은 데이터 속성과 같은 인터페이스(즉 `obj.attr`)를 제시하지만 요구에 따라
  계산된다** (같은 자리, p.835).[^ramalho2022]
- 그 위에 저자가 이름 하나를 더 만든다 — **`__getattr__`을 구현하는 사용자 정의 클래스는
  내가 가상 속성(virtual attributes)이라 부르는 동적 속성의 변종을 구현할 수 있다:
  클래스의 소스 코드 어디에도 명시적으로 선언되지 않고 인스턴스 `__dict__`에도 없지만,
  사용자가 `obj.no_such_attr` 같은 존재하지 않는 속성을 읽으려 할 때 다른 데서 회수되거나
  즉석에서 계산될 수 있는 속성** (같은 자리, p.835).[^ramalho2022]
- 적용 범위에 단서가 붙는다 — **동적 속성과 가상 속성을 코딩하는 것은 프레임워크 저자들이
  하는 종류의 메타프로그래밍이다. 그러나 파이썬에서는 기본 기법이 직관적이라 일상적인
  데이터 다루기 작업에도 쓸 수 있다** (같은 자리, p.835).[^ramalho2022]
- 프로퍼티의 지위가 Martelli 등의 말로 인용된다 (같은 자리, p.835):[^ramalho2022]

> The crucial importance of properties is that their existence makes it perfectly safe
> and indeed advisable for you to expose public data attributes as part of your class's
> public interface.

- 그런데 저자가 그 원칙에 유보를 단다 (22장 §"Soapbox", p.875):[^ramalho2022]

> although the Uniform Access Principle makes perfect sense in an ideal world, in
> reality, users of an API may need to know whether reading `product.price` is
> potentially too expensive or time-consuming. That's a problem with programming
> abstractions in general: they make it hard to reason about the runtime cost of
> evaluating an expression. On the other hand, abstractions let users accomplish more
> with less code. It's a trade-off.

  - 이 유보가 이 장 안에서 실제로 문제를 만든다. 캐싱 절의 각주가 그것을 되짚는다 —
    **프로퍼티를 캐시하는 것은 흔한 필요다. `event.venue` 같은 식이 싸리라는 기대가 있기
    때문이다. (…) 이것은 사실 이 장 도입에서 언급한 Meyer의 균일 접근 원칙의 단점이다**
    (22장 §"Step 4: Bespoke Property Cache" 각주 8, p.853).[^ramalho2022]

## 가상 속성과 __getattr__

- 발동 조건이 이 절의 핵심이다 — **`__getattr__` 특수 메서드는 통상적인 과정이 속성을
  회수하는 데 실패할 때에만 인터프리터에 의해 호출된다는 것을 상기하는 것이 필수적이다
  (즉 이름 붙은 속성이 인스턴스에서도, 클래스나 그 상위 클래스에서도 발견되지 않을 때)**
  (22장 §"Exploring JSON-Like Data with Dynamic Attributes", p.839).[^ramalho2022]
- 저자의 `FrozenJSON` 예제가 그 위에 세워진다. 중첩된 매핑과 리스트를 점 표기로 훑게
  해 주는 읽기 전용 façade이고, 요구되는 규율 하나가 재귀다 — **`FrozenJSON`은 재귀적이라
  중첩된 매핑과 리스트를 자동으로 다룬다** (같은 절, p.838).[^ramalho2022]
- 저자가 자기 코드의 결함을 스스로 표시한다 — **없는 속성을 읽으려 하면
  `AttributeError`를 일으켜야 하는데 보인 대로 `KeyError`가 난다. 그렇게 하도록 오류
  처리를 구현했더니 `__getattr__` 메서드가 두 배로 길어져 내가 보이려던 가장 중요한
  로직에서 주의를 흩뜨렸다** (같은 절, p.839).[^ramalho2022] 그 절충을 그대로 두고
  각주에서 독자에게 숙제로 넘긴다.
- 원본 데이터를 바꾸지 않는다는 성질도 명시된다 — **`FrozenJSON`은 원본 데이터셋을
  변환하거나 캐시하지 않는다. 데이터를 훑는 동안 `__getattr__`이 `FrozenJSON` 인스턴스를
  거듭거듭 만든다. 이 크기의 데이터셋과 데이터를 탐색하거나 변환하는 데만 쓸 스크립트에는
  그것이 괜찮다** (같은 절, p.841).[^ramalho2022]
- 동적 속성 이름을 임의 소스에서 만들면 반드시 생기는 문제가 하나 있다 — **임의의 소스에서
  동적 속성 이름을 만들거나 흉내 내는 스크립트는 문제 하나를 다뤄야 한다: 원본 데이터의
  키가 속성 이름으로 적합하지 않을 수 있다** (같은 절, p.842).[^ramalho2022]
  - 예약어 쪽 처방 — **매핑의 키가 키워드인지 검사하고 그렇다면 `_`를 덧붙여** 읽을 수
    있게 만든다. `keyword.iskeyword(…)`가 그 검사다 (22장 §"The Invalid Attribute Name
    Problem", p.842).[^ramalho2022]
  - 식별자가 아닌 키 쪽은 답이 없다 — **`str` 클래스가 `s.isidentifier()` 메서드를
    제공하므로 그런 문제 키를 검출하기는 파이썬 3에서 쉽다. 그러나 유효한 식별자가 아닌
    키를 유효한 속성 이름으로 바꾸는 것은 사소하지 않다** (같은 절,
    p.843).[^ramalho2022] 저자가 든 한 해법이 `__getitem__`을 구현해 `x['2be']`로
    접근하게 하는 것이고, 그는 단순함을 위해 그 문제를 다루지 않는다고 적는다.

## __new__는 생성자이고 __init__은 초기화자다

- 이름 바로잡기 — **우리는 흔히 `__init__`을 생성자 메서드라 부르지만, 그것은 다른 언어의
  은어를 채택했기 때문이다. 파이썬에서 `__init__`은 첫 인자로 `self`를 받으므로,
  인터프리터가 `__init__`을 부를 때 객체는 이미 존재한다. 또 `__init__`은 아무것도 돌려줄
  수 없다. 그러니 그것은 정말로 초기화자이지 생성자가 아니다** (22장 §"Flexible Object
  Creation with __new__", p.843).[^ramalho2022]
- 진짜 생성자 — **클래스가 인스턴스를 만들려고 불릴 때 파이썬이 그 클래스에 대해 부르는,
  인스턴스를 구성하는 특수 메서드는 `__new__`다. 그것은 클래스 메서드이지만 특별한 대우를
  받아서 `@classmethod` 데코레이터가 적용되지 않는다. 파이썬은 `__new__`가 돌려준 인스턴스를
  받아 `__init__`의 첫 인자 `self`로 넘긴다** (같은 절, p.843).[^ramalho2022]
- 손댈 일이 드물다는 단서 — **우리는 `__new__`를 코딩할 필요가 거의 없다. `object`에서
  상속받은 구현이 압도적 다수의 쓰임에 충분하기 때문이다** (같은 절,
  p.843).[^ramalho2022]
- 다른 클래스를 돌려줄 수 있다는 것이 이 메서드의 힘이다 — **필요하면 `__new__` 메서드는
  다른 클래스의 인스턴스를 돌려줄 수도 있다. 그런 일이 일어나면 인터프리터는 `__init__`을
  부르지 않는다** (같은 절, p.843).[^ramalho2022] 그 로직이 의사코드로 명시된다 (같은 절,
  p.843):[^ramalho2022]

  ```text
  # pseudocode for object construction
  def make(the_class, some_arg):
      new_object = the_class.__new__(some_arg)
      if isinstance(new_object, the_class):
          the_class.__init__(new_object, some_arg)
      return new_object
  ```

- 그 성질의 쓸모가 곁글에 정리돼 있다 — **생성자를 팩토리로 대체할 좋은 이유가 많다.
  인기 있는 동기는 이전에 지어진 것을 돌려줌으로써 인스턴스 수를 제한하는 것이다(싱글턴
  패턴처럼). 관련된 쓸모는 비싼 객체 생성을 캐시하는 것이다. 또 때때로 주어진 인자에 따라
  다른 타입의 객체를 돌려주는 것이 편리하다** (22장 §"Soapbox — __new__ Is Better than
  new", p.877).[^ramalho2022]
- 그 유연성의 대가와, `new` 연산자가 있는 언어와의 대비가 이어진다 — **생성자를 코딩하는
  것이 더 단순하다. 팩토리를 제공하는 것은 코드가 늘어나는 대신 유연성을 더한다. `new`
  연산자가 있는 언어에서는 API 설계자가 단순한 생성자로 갈지 팩토리에 투자할지 미리
  결정해야 한다. 최초 선택이 틀렸다면 교정이 비쌀 수 있다 — 전부 `new`가 연산자이기
  때문이다** (같은 절, p.877).[^ramalho2022]

## 프로퍼티는 인스턴스 속성을 가린다

- 사실 — **프로퍼티는 언제나 클래스 속성이지만, 실제로는 그 클래스의 인스턴스들에서
  속성 접근을 관리한다** (22장 §"Properties Override Instance Attributes",
  p.861).[^ramalho2022]
- 그 귀결이 조회 순서를 뒤집는다 (22장 §"Properties Override Instance Attributes",
  p.863):[^ramalho2022]

> the main point of this section is that an expression like `obj.data` does not start the
> search for `data` in `obj`. The search actually starts at `obj.__class__`, and only if
> there is no property named `data` in the class, Python looks in the `obj` instance
> itself. This applies to *overriding descriptors* in general, of which properties are
> just one example.

- 그래서 프로퍼티는 실행 중에 끼워 넣거나 뺄 수 있다 — 저자의 콘솔 실험이 클래스에 새
  프로퍼티를 대입해 기존 인스턴스 속성을 가리고, 그 프로퍼티를 `del`로 지워 다시 인스턴스
  속성이 보이게 만든다 (같은 절, pp.862–863).[^ramalho2022]
- `property`는 함수가 아니라 클래스다 — **데코레이터로 자주 쓰이지만 `property` 내장은
  사실 클래스다. 파이썬에서 함수와 클래스는 종종 교체 가능하다. 둘 다 호출 가능하고
  객체 인스턴스화를 위한 `new` 연산자가 없으므로, 생성자를 부르는 것이 팩토리 함수를
  부르는 것과 다르지 않기 때문이다** (22장 §"A Proper Look at Properties",
  p.860).[^ramalho2022]
- 완전한 시그니처가 넷이다 — `property(fget=None, fset=None, fdel=None, doc=None)`이고
  **모든 인자가 선택적이며, 그중 하나에 함수가 제공되지 않으면 결과 `property` 객체는 그에
  대응하는 연산을 허용하지 않는다** (같은 절, p.860).[^ramalho2022]
- 데코레이터 문법과 고전 호출 문법의 선택 기준이 명시된다 — **고전 형식이 어떤 상황에서는
  데코레이터 문법보다 낫다. 곧 논의할 프로퍼티 팩토리의 코드가 한 예다. 반면 메서드가 많은
  클래스 몸통에서는 데코레이터가 어느 것이 게터이고 세터인지, 이름에 `get`·`set` 접두사를
  쓰는 관례에 기대지 않고도 명시적으로 만든다** (같은 절, p.861).[^ramalho2022]
- 문서화의 규칙 — **게터 메서드의 독스트링 — `@property` 데코레이터가 붙은 그것 — 이
  프로퍼티 전체의 문서로 쓰인다** (22장 §"Property Documentation", p.864).[^ramalho2022]
  고전 호출 문법에서는 `doc` 인자로 준다.
- 삭제도 다룰 수 있다 — **프로퍼티 정의에서 `@my_property.deleter` 데코레이터가 프로퍼티가
  관리하는 속성을 삭제하는 일을 맡은 메서드를 감싼다** (22장 §"Handling Attribute
  Deletion", p.868).[^ramalho2022] 다만 저자가 그 빈도를 낮게 잡는다 — **실무에서 속성을
  삭제하는 것은 파이썬에서 매일 하는 일이 아니고, 그것을 프로퍼티로 다뤄야 할 요구는 더욱
  드물다** (같은 절, p.868).[^ramalho2022]

## 계산 결과를 캐시할 때의 세 함정

- 첫째 함정 — 손수 만든 캐시가 메모리 최적화를 무력화한다. **`hasattr`을 쓴 손수 만든
  캐싱은 직관적이지만, 인스턴스가 초기화된 뒤에 속성을 만드는 것은 PEP 412 키 공유
  딕셔너리 최적화를 무력화한다. 데이터셋 크기에 따라 메모리 사용의 차이가 중요할 수
  있다** (22장 §"Step 4: Bespoke Property Cache", p.854).[^ramalho2022] 그 회피책이
  `__init__`에서 캐시 속성을 `None`으로 미리 만들어 두는 것이다.
- 둘째 함정 — 경쟁 상태. **멀티스레드 프로그램에서 이런 손수 만든 캐시는 데이터 손상으로
  이어질 수 있는 경쟁 상태를 들여온다. 두 스레드가 이전에 캐시되지 않은 프로퍼티를 읽으면,
  첫 스레드가 캐시 속성의 데이터를 계산해야 하고 둘째 스레드는 아직 완성되지 않은 캐시된
  값을 읽을 수 있다** (같은 절, p.855).[^ramalho2022]
- 셋째 함정 — 이름이 거짓말을 한다. `@functools.cached_property`가 그 둘을 푸는데,
  저자가 그 정체를 밝힌다 (22장 §"Step 5: Caching Properties with functools",
  p.855):[^ramalho2022]

> The answer is a bit sad: `cached_property` is a misnomer. The `@cached_property`
> decorator does not create a full-fledged property, it creates a *nonoverriding
> descriptor*.

  - 그 차이가 Raymond Hettinger의 문서 설명으로 인용된다 (같은 절,
    p.856):[^ramalho2022]

> A regular property blocks attribute writes unless a setter is defined. In contrast, a
> `cached_property` allows writes. The `cached_property` decorator only runs on lookups
> and only when an attribute of the same name doesn't exist. When it does run, the
> `cached_property` writes to the attribute with the same name. Subsequent attribute
> reads and writes take precedence over the `cached_property` method and it works like a
> normal attribute. The cached value can be cleared by deleting the attribute.

  - 한계 셋 (같은 절, p.856):[^ramalho2022]
    - **장식되는 메서드가 같은 이름의 인스턴스 속성에 이미 의존한다면 `@property`의
      드롭인 대체로 쓸 수 없다.**
    - **`__slots__`를 정의하는 클래스에서 쓸 수 없다.**
    - **인스턴스 `__dict__`의 키 공유 최적화를 무력화한다. `__init__` 뒤에 인스턴스 속성을
      만들기 때문이다.**
  - 그래도 채택할 이유 — **이 한계에도 불구하고 `@cached_property`는 흔한 필요를 단순한
    방식으로 다루며 스레드 안전하다. 그 파이썬 코드는 재진입 락(reentrant lock)을 쓰는
    예다** (같은 절, p.856).[^ramalho2022]
  - 한계에 걸리는 경우의 처방이 문서 자신에게서 온다 — **`@cached_property` 문서가
    `speakers`에 쓸 수 있는 대안을 권한다: `@property`와 `@cache` 데코레이터를 쌓는
    것** (같은 절, p.856).[^ramalho2022] **순서가 중요하다 — `@property`가 `@cache`
    위로 간다.**
  - 버전 조건: `functools.cached_property`는 파이썬 3.8, `functools.cache`는 3.9에
    더해졌다.
- 이 절이 이 저장소 헌장의 캐시 조항과 닿는 자리는
  [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md)에 있다 —
  그쪽이 `@cache`·`@lru_cache`의 정본이고, 여기 셋째 함정이 그 페이지에 합류했다.

## 검증을 위한 프로퍼티

- 쓸모의 규정 — **속성 값을 계산하는 것 말고도, 프로퍼티는 공개 속성을 게터와 세터로
  보호되는 속성으로 바꿈으로써 클라이언트 코드에 영향을 주지 않고 업무 규칙을 강제하는
  데에도 쓰인다** (22장 §"Using a Property for Attribute Validation",
  p.857).[^ramalho2022]
- 동기가 실제 사건으로 예시된다. 음수 수량이 음수 소계를 낳는 문제에 대해 저자가 Jeff
  Bezos의 회고를 인용한다 (같은 절, p.858):[^ramalho2022]

> We found that customers could order a negative quantity of books! And we would credit
> their credit card with the price and, I assume, wait around for them to ship the books.

- 두 해법의 대비와 파이썬 쪽 선택 — **`LineItem`의 인터페이스를 바꿔 `weight` 속성에
  게터와 세터를 쓸 수 있다. 그것이 자바 방식이고 틀리지 않다. 반면 항목의 무게를 그냥
  대입해서 설정할 수 있는 것이 자연스럽고, 어쩌면 시스템이 이미 프로덕션에 있고 다른
  부분들이 `item.weight`에 직접 접근하고 있을 수도 있다. 이 경우 파이썬다운 방식은 데이터
  속성을 프로퍼티로 대체하는 것이다** (같은 절, p.858).[^ramalho2022]
- 관례 셋이 딸려 온다 (22장 §"LineItem Take #2: A Validating Property",
  p.859):[^ramalho2022]
  - **프로퍼티를 구현하는 모든 메서드가 공개 속성의 이름을 공유한다.**
  - **실제 값은 사설 속성에 저장된다.**
  - **장식된 게터는 `.setter` 속성을 갖는데 그것도 데코레이터이며, 이것이 게터와 세터를
    함께 묶는다.**
- 반복이 보이면 그것이 신호다 — 저자가 17장의 Paul Graham 인용을 다시 부른다:
  **"내 프로그램에서 패턴이 보이면 나는 그것을 문제의 징후로 여긴다."** 그리고 처방 —
  **반복의 치료는 추상이다. 프로퍼티 정의를 추상해 내는 방법이 둘 있다: 프로퍼티 팩토리를
  쓰거나 디스크립터 클래스를 쓰는 것. 디스크립터 클래스 접근이 더 유연하다. (…) 프로퍼티는
  사실 디스크립터 클래스로 구현돼 있다** (22장 §"LineItem Take #2: A Validating
  Property", p.859).[^ramalho2022]

## 프로퍼티 팩토리

- 팩토리가 푸는 것과 남기는 것 — **각 `quantity` 프로퍼티를 지을 때 그 프로퍼티가 관리할
  `LineItem` 속성의 이름을 넘겨야 한다. `weight`라는 낱말을 이 줄에 두 번 쳐야 하는 것은
  불행하다. 그러나 그 반복을 피하는 것은 복잡하다. 프로퍼티가 어느 클래스 속성 이름에
  묶일지 알 방법이 없기 때문이다. 기억하라: 대입의 오른쪽이 먼저 평가되므로 `quantity()`가
  불릴 때 `weight` 클래스 속성은 존재하지도 않는다** (22장 §"Coding a Property Factory",
  p.865).[^ramalho2022] 그 나머지 문제를 푸는 것이 다음 장이다.
- 대표 코드가 그 팩토리다 (예제 22-28, p.866):[^ramalho2022]

  ```python
  def quantity(storage_name):

      def qty_getter(instance):
          return instance.__dict__[storage_name]

      def qty_setter(instance, value):
          if value > 0:
              instance.__dict__[storage_name] = value
          else:
              raise ValueError('value must be > 0')

      return property(qty_getter, qty_setter)
  ```

  - 첫 인자 이름이 `self`가 아닌 사유가 명시돼 있다 — **`qty_getter`의 첫 인자는 `self`로
    이름 지어도 되지만, 여기는 클래스 몸통이 아니므로 이상할 것이다. `instance`는 속성이
    저장될 `LineItem` 인스턴스를 가리킨다** (같은 절, p.866).[^ramalho2022]
  - `instance.__dict__`를 직접 쓰는 사유도 명시돼 있다 — **값이 `instance.__dict__`에서
    직접 회수되어 프로퍼티를 우회하고 무한 재귀를 피한다** (같은 절,
    p.866).[^ramalho2022]
  - 클로저가 무엇을 나르는가 — **`qty_getter`와 `qty_setter` 함수는 일반적이고,
    `storage_name` 변수에 의존해 인스턴스 `__dict__`의 어디서 관리 속성을 얻고 설정할지
    안다. `quantity` 팩토리가 프로퍼티를 지으려고 불릴 때마다 `storage_name`은 유일한
    값으로 설정돼야 한다** (같은 절, p.867).[^ramalho2022]
  - 우회로가 하나 남는다 — **팩토리가 지은 프로퍼티들이 §"Properties Override Instance
    Attributes"에 서술된 동작을 활용한다: `weight` 프로퍼티가 `weight` 인스턴스 속성을
    가려서 `self.weight`나 `nutmeg.weight`에 대한 모든 참조가 프로퍼티 함수들에 의해
    처리되고, 프로퍼티 로직을 우회하는 유일한 방법은 인스턴스 `__dict__`에 직접 접근하는
    것이다** (같은 절, p.867).[^ramalho2022]
- 이득의 계량 — **예제 22-28의 코드는 조금 까다로울 수 있지만 간결하다: `weight`
  프로퍼티 하나만 정의하는 장식된 게터/세터 쌍과 길이가 같다** (같은 절,
  p.867).[^ramalho2022] 그리고 실무의 다음 단계 — **실제 시스템에서는 같은 종류의 검증이
  여러 클래스의 많은 필드에 나타날 수 있고, `quantity` 팩토리는 거듭 쓰이도록 유틸리티
  모듈에 놓일 것이다. 결국 그 단순한 팩토리는 다른 검증을 수행하는 특화된 하위 클래스를
  가진 더 확장 가능한 디스크립터 클래스로 리팩터링될 수 있다** (같은 절,
  pp.867–868).[^ramalho2022]

## 속성을 다루는 API 지도

- 특수 속성 셋이 나머지의 동작을 좌우한다 (22장 §"Special Attributes that Affect Attribute
  Handling", p.870):[^ramalho2022]
  - `__class__` — **객체 클래스에 대한 참조. 파이썬은 `__getattr__` 같은 특수 메서드를
    객체의 클래스에서만 찾지 인스턴스 자체에서는 찾지 않는다.**
  - `__dict__` — **객체나 클래스의 쓰기 가능한 속성을 저장하는 매핑. `__dict__`를 가진
    객체는 언제든 임의의 새 속성을 설정할 수 있다.**
  - `__slots__` — **메모리를 아끼려고 클래스에 정의할 수 있는 속성.** 그 정본은
    [__slots__와 인스턴스 메모리](slots-and-instance-memory.md)에 있다.
- 내장 함수 다섯 (22장 §"Built-In Functions for Attribute Handling",
  pp.870–871):[^ramalho2022] `dir`·`getattr`·`hasattr`·`setattr`·`vars`. 갈리는 자리
  둘이 지목돼 있다 — **`dir`은 `__dict__`가 있든 없든 객체를 조사할 수 있다**(반면
  **`vars`는 `__slots__`를 정의하고 `__dict__`가 없는 클래스의 인스턴스를 다루지
  못한다**), 그리고 **`__dict__` 속성 자체는 `dir`에 나열되지 않지만 `__dict__`의 키들은
  나열된다.** `hasattr`의 구현도 명시된다 — **문서가 설명한다: "이것은 `getattr(object,
  name)`을 부르고 그것이 `AttributeError`를 일으키는지 보는 것으로 구현된다."**
- 특수 메서드 다섯 (22장 §"Special Methods for Attribute Handling",
  pp.871–872):[^ramalho2022] `__delattr__`·`__dir__`·`__getattr__`·`__getattribute__`·
  `__setattr__`.
  - 우회로가 명시된다 — **인스턴스 `__dict__`에서 속성을 직접 읽고 쓰는 것은 이 특수
    메서드들을 발동시키지 않는다 — 그리고 그것이 필요할 때 그것들을 우회하는 통상적인
    방법이다.**
  - 조회 규칙 — **사용자 정의 클래스의 경우, 특수 메서드의 암묵적 호출은 그것이 객체의
    인스턴스 딕셔너리가 아니라 타입에 정의돼 있을 때에만 올바르게 동작하도록 보장된다.**
    그래서 **특수 메서드는 같은 이름의 인스턴스 속성에 가려지지 않는다.**
  - 관계 — **`__getattr__`은 `__getattribute__` 뒤에만 발동되며, `__getattribute__`가
    `AttributeError`를 일으킬 때에만 발동된다.** 그리고 무한 재귀를 피하려면
    **`__getattribute__` 구현은 `super().__getattribute__(obj, name)`을 써야 한다.**
  - 프로퍼티와의 충돌 하나 — **`attr`이 프로퍼티라면, 클래스가 `__delattr__`을 구현하는
    경우 그 삭제자 메서드는 결코 불리지 않는다.**
- 그리고 조문 (같은 절, p.872):[^ramalho2022]

> In practice, because they are unconditionally called and affect practically every
> attribute access, the `__getattribute__` and `__setattr__` special methods are harder
> to use correctly than `__getattr__`, which only handles nonexisting attribute names.
> Using properties or descriptors is less error prone than defining these special
> methods.

## 공개 속성으로 시작해도 된다

- 언어 셋의 대비가 곁글에 있다 (22장 §"Soapbox", pp.875–876):[^ramalho2022]
  - **Smalltalk과 루비는 이 문제를 단순하고 우아한 방식으로 다룬다: 공개 데이터 속성을
    아예 지원하지 않는다. 이 언어들에서 모든 인스턴스 속성은 사적이므로 그것에 대한 모든
    접근은 메서드를 거쳐야 한다. 그러나 그들의 문법이 이것을 고통 없게 만든다.**
  - **자바 언어는 프로그래머가 네 가지 접근 수준 수식자 중에서 고르게 한다.** 그런데
    **일반적 실천은 자바 설계자들이 세운 문법과 일치하지 않는다. 자바 나라의 모두가 속성은
    사적이어야 한다는 데 동의하고, 그것이 기본값이 아니므로 매번 그것을 적어 내야 한다.**
    그 대가가 명시된다 — **IDE는 코드를 여섯 달 뒤에 읽어야 할 때는 그리 도움이 되지
    않는다. 업무 로직을 구현해 값을 더하는 접근자들을 찾으려고 아무 일도 하지 않는
    접근자의 바다를 헤쳐 나가는 것은 당신 몫이다.**
  - Alex Martelli가 접근자를 **"바보 같은 관용구(goofy idioms)"**라 부른 것이 인용되고,
    `someInstance.widgetCounter += 1`과 그것의 자바식 등가물이 나란히 놓인다.
- 저자의 결론 — **Smalltalk과 루비의 해법이 더 깔끔하다고 생각하지만, 파이썬 접근이
  자바 것보다는 더 말이 된다고 생각한다. 우리는 단순하게 시작해 데이터 멤버를 공개 속성으로
  코딩하는 것이 허용된다. 그것이 언제든 프로퍼티(또는 다음 장에서 이야기할 디스크립터)로
  감싸질 수 있음을 알기 때문이다** (같은 절, p.876).[^ramalho2022]
- 설계에서 저자가 미결로 남긴 질문 하나 — **API를 설계할 때, `self` 말고 인자를 받지 않고,
  (`None`이 아닌) 값을 돌려주며, 순수 함수인(즉 부수 효과가 없는) 모든 메서드가 읽기 전용
  프로퍼티로 대체되어야 하는지 궁금했던 적이 있다** (같은 절, p.876).[^ramalho2022]
  그가 스스로 단 예외 — **물론 이것은 `my_list.clear()`처럼 객체를 바꾸도록 설계된 메서드는
  제외한다. 그것을 프로퍼티로 만들어서 단지 `my_list.clear`에 접근하는 것만으로 리스트
  내용이 지워지게 하는 것은 끔찍한 발상일 것이다.**
  - 이 미결 질문이 이 KB의 [부수 효과 없는 함수](side-effect-free-functions.md)가 말하는
    명령·질의 분리와 같은 자리를 짚는다. 다만 저자는 그것을 규범으로 세우지 않고 질문으로
    남겼다.

## 이어지는 페이지

- [속성 디스크립터](attribute-descriptors.md) — 여기 프로퍼티 팩토리가 못 푼 것(속성
  이름의 자동 지정)을 푸는 자리이자, 프로퍼티 자신의 구현 기제
- [클래스 메타프로그래밍과 메타클래스](class-metaprogramming-and-metaclasses.md) — 이
  기법들이 클래스 생성 시점으로 올라가는 자리
- [표준 라이브러리의 함수 데코레이터](standard-library-function-decorators.md) — `@cache`·
  `@lru_cache`의 정본. 여기 캐시 프로퍼티 논의가 그쪽에 합류했다
- [파이썬다운 객체 만들기](building-pythonic-objects.md) — 프로퍼티를 불변성을 사는 수단으로
  쓰는 자리와, 프로퍼티의 선행 비용에 대한 곁글
- [시퀀스 프로토콜의 점진 구현](implementing-the-sequence-protocol.md) — `__getattr__`과
  `__setattr__`을 짝으로 써야 하는 이유의 정본
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 여기 캐시 절이 무력화한다고
  적은 키 공유 최적화와 `__slots__`의 관계
- [정보 은닉과 정보 누출](information-hiding-and-leakage.md) — 공개 속성으로 시작해도
  된다는 판단이 닿는 원리 쪽
- [부수 효과 없는 함수](side-effect-free-functions.md) — 저자가 미결로 남긴 명령·질의
  분리 질문이 닿는 자리
- [파이썬의 클래스 메타프로그래밍](../synthesis/python-class-metaprogramming.md) — 이 축의
  허브

[^ramalho2022]: Ramalho 2022, 22장 "Dynamic Attributes and Properties" 도입(p.835) ·
    §"Exploring JSON-Like Data with Dynamic Attributes"(pp.838–842) · §"The Invalid
    Attribute Name Problem"(pp.842–843) · §"Flexible Object Creation with
    __new__"(pp.843–844) · §"Step 4: Bespoke Property Cache"(pp.853–855) · §"Step 5:
    Caching Properties with functools"(pp.855–857) · §"Using a Property for Attribute
    Validation"(pp.857–859) · §"LineItem Take #2: A Validating Property"(pp.858–859) ·
    §"A Proper Look at Properties"(pp.860–861) · §"Properties Override Instance
    Attributes"(pp.861–863) · §"Property Documentation"(p.864) · §"Coding a Property
    Factory"(pp.865–868) · §"Handling Attribute Deletion"(pp.868–869) · §"Essential
    Attributes and Functions for Attribute Handling"(pp.869–872) · §"Soapbox"(pp.875–877).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 그림
    22-1(프로퍼티 도움말 화면 스크린샷)은 이미지로 조판돼 있어 본문 서술로만 옮겼다.
    코드 펜스는 예제 22-28 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만 제거했다.
    `__new__` 의사코드는 저자가 본문에 그대로 실은 것이고, 실행할 코드가 아니라
    인터프리터의 로직을 설명하는 의사코드이므로 `text` 펜스로 두어 실행 가능한 대표
    코드(예제 22-28)와 갈랐다(SCHEMA §3). OSCON 일정 데이터셋을 다루는
    `Record`·`Event` 예제 계열(pp.845–857)은 특정 데이터셋에 묶인 코드라 판단과 기제만
    옮기고 코드는 옮기지 않았다. PDF 908쪽은 도비라라 추출이 OCR 필요 판정을 냈다 —
    손실 아님.

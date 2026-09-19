---
type: concept
title: 클래스 메타프로그래밍과 메타클래스
description: 실행 중에 클래스를 만들거나 손보는 기법 넷(클래스 팩토리·__init_subclass__·클래스 데코레이터·메타클래스)과 그것들이 각각 언제 발동하는가, __slots__만은 왜 앞의 셋으로 설정할 수 없는가, 현대 기능이 메타클래스를 대체한 자리, 그리고 이 도구들이 라이브러리와 프레임워크를 위한 것이지 애플리케이션 코드를 위한 것이 아니라는 저자의 반복된 기각
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 클래스 메타프로그래밍과 메타클래스

- [먼저 읽을 조언](#먼저-읽을-조언)
- [클래스도 객체다](#클래스도-객체다)
- [type은 세 인자짜리 클래스 팩토리다](#type은-세-인자짜리-클래스-팩토리다)
- [__init_subclass__는 전형적인 클래스 메서드가 아니다](#__init_subclass__는-전형적인-클래스-메서드가-아니다)
- [클래스 데코레이터를 고르는 이유](#클래스-데코레이터를-고르는-이유)
- [__slots__만은 왜 안 되는가](#__slots__만은-왜-안-되는가)
- [메타클래스](#메타클래스)
- [현대 기능이 대체한 자리](#현대-기능이-대체한-자리)
- [실무에서 지킬 것](#실무에서-지킬-것)
- [이 도구들은 누구를 위한 것인가](#이-도구들은-누구를-위한-것인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **클래스가 만들어지는 과정에 끼어드는 방법이 여럿일 때 무엇을 고르며, 언제
아무것도 고르지 않는 것이 답인가.**

## 먼저 읽을 조언

- 이 장의 경구가 Kernighan과 Plauger의 말이다 (24장 도입, p.907):[^ramalho2022]

> Everyone knows that debugging is twice as hard as writing a program in the first place.
> So if you're as clever as you can be when you write it, how will you ever debug it?

- 규정 — **클래스 메타프로그래밍(class metaprogramming)은 실행 중에 클래스를 만들거나
  맞춤화하는 기술이다. 파이썬에서 클래스는 일급 객체이므로, `class` 키워드를 쓰지 않고
  언제든 함수를 써서 새 클래스를 만들 수 있다. 클래스 데코레이터도 함수이지만, 장식된
  클래스를 조사하고 바꾸고 심지어 다른 클래스로 대체하도록 설계된다. 마지막으로
  메타클래스는 클래스 메타프로그래밍을 위한 가장 고급 도구다** (같은 자리,
  p.907).[^ramalho2022]
- 그리고 곧바로 위계가 매겨진다 — **메타클래스는 강력하지만 정당화하기 어렵고 제대로
  해내기는 더 어렵다. 클래스 데코레이터가 같은 문제 다수를 풀고 이해하기 더 쉽다. 나아가
  파이썬 3.6이 PEP 487을 구현해, 이전에는 메타클래스나 클래스 데코레이터를 요구하던
  작업들을 지원하는 특수 메서드를 제공한다** (같은 자리, p.907).[^ramalho2022]
- 이 장 전체에 걸리는 조언이 두 번째 쪽에 상자로 들어 있다 (24장 §"What's New in This
  Chapter" 앞, p.908):[^ramalho2022]

> For the sake of readability and maintainability, you should probably avoid the
> techniques described in this chapter in application code. On the other hand, these are
> the tools of the trade if you want to write the next great Python framework.

- 저자가 자기 1판을 실제로 그렇게 고쳤다 — **1판의 코드 전부가 여전히 올바르게 돈다.
  그러나 이전 예제 일부는 파이썬 3.6 이후 더해진 새 기능에 비추어 더 이상 가장 단순한
  해법을 나타내지 않는다** (24장 §"What's New in This Chapter", p.908).[^ramalho2022]
  그리고 규범 한 줄 — **최고의 리팩터링 중 어떤 것은 같은 문제를 푸는 더 새롭고 더 단순한
  방법 때문에 군더더기가 된 코드를 지우는 것이다. 이것은 프로덕션 코드에도, 책에도
  적용된다** (같은 절, p.908).[^ramalho2022]

## 클래스도 객체다

- 클래스가 갖는 표준 속성들 중 이 장이 더하는 것 (24장 §"Classes as Objects",
  pp.908–909):[^ramalho2022]
  - `cls.__bases__` — **클래스의 기반 클래스들의 튜플.**
  - `cls.__qualname__` — **클래스나 함수의 한정된 이름. 모듈의 전역 범위에서 클래스
    정의까지의 점 붙은 경로다.** 클래스가 다른 클래스 안에 정의될 때 유의미하다 —
    장고 모델의 내부 `Meta` 클래스가 예로 들리는데, 그 `__qualname__`은 `Ox.Meta`이고
    `__name__`은 그냥 `Meta`다.
  - `cls.__subclasses__()` — **클래스의 직계 하위 클래스 목록을 돌려주는 메서드.** 구현이
    **상위 클래스와 하위 클래스 사이의 순환 참조를 피하려고 약한 참조를 쓴다.** 단서 —
    **이 메서드는 현재 메모리에 있는 하위 클래스를 나열한다. 아직 임포트되지 않은 모듈의
    하위 클래스는 결과에 나타나지 않는다.**
  - `cls.mro()` — **인터프리터가 클래스를 지을 때 `__mro__` 속성에 저장할 상위 클래스
    튜플을 얻으려고 이 메서드를 부른다. 메타클래스가 이 메서드를 오버라이드해 구성 중인
    클래스의 메서드 결정 순서를 맞춤화할 수 있다.**
  - 그리고 단서 — **이 절에서 언급한 속성 중 어느 것도 `dir(…)` 함수에 나열되지 않는다.**

## type은 세 인자짜리 클래스 팩토리다

- 두 얼굴 — **우리는 보통 `type`을 객체의 클래스를 돌려주는 함수로 생각한다. `type(my_object)`가
  하는 일이 그것이기 때문이다. 그러나 `type`은 세 인자로 불리면 새 클래스를 만드는
  클래스다** (24장 §"type: The Built-In Class Factory", p.909).[^ramalho2022]
- 클래스 문이 그 호출로 번역된다 — **파이썬이 `class` 문을 읽으면 이 매개변수들로 클래스
  객체를 짓기 위해 `type`을 부른다** (같은 절, p.910):[^ramalho2022]
  - `name` — **`class` 키워드 뒤에 나타나는 식별자.**
  - `bases` — **클래스 식별자 뒤 괄호 안에 주어진 상위 클래스들의 튜플, 또는 `class`
    문에 상위 클래스가 언급되지 않았으면 `(object,)`.**
  - `dict` — **속성 이름에서 값으로의 매핑. 호출 가능한 것은 메서드가 되고, 다른 값들은
    클래스 속성이 된다.**
- 그리고 정체 — **`type` 클래스는 메타클래스다: 클래스를 짓는 클래스. 달리 말해 `type`
  클래스의 인스턴스가 클래스다. 표준 라이브러리가 다른 메타클래스를 몇 개 제공하지만
  `type`이 기본값이다** (같은 절, p.910).[^ramalho2022]
- 표준 라이브러리의 클래스 팩토리들이 이 기법 위에 서 있다 — **표준 라이브러리에는 이 책에
  여러 번 나온 클래스 팩토리 함수가 있다: `collections.namedtuple`. 5장에서 우리는
  `typing.NamedTuple`과 `@dataclass`도 보았다. 이 클래스 빌더들 전부가 이 장에서 다루는
  기법을 활용한다** (24장 §"A Class Factory Function", p.911).[^ramalho2022]
- 다만 손으로 만든 팩토리는 표준 것만 못하다는 단서가 붙는다 — **`record_factory`가 만든
  클래스의 인스턴스는 직렬화 가능하지 않다 — 즉 `pickle` 모듈의 `dump` 함수로 내보낼 수
  없다. 이 문제를 푸는 것은 이 예제의 범위 밖이며, 이 예제는 단순한 쓰임에서 `type`
  클래스가 동작하는 것을 보이는 것이 목적이다. 완전한 해법은
  `collections.namedtuple`의 소스 코드를 공부하라** (같은 절, p.914).[^ramalho2022]

## __init_subclass__는 전형적인 클래스 메서드가 아니다

- 무엇을 더하는가 — **`typing.NamedTuple`과 `@dataclass` 둘 다 사용자의 `class` 문에서
  타입 힌트를 읽어 클래스를 향상시킨다. 그 타입 힌트는 정적 타입 검사기가 그 속성을
  설정하거나 얻는 코드를 검증하게도 해 준다. 그러나 `NamedTuple`과 `@dataclass`는
  런타임 속성 검증에 그 타입 힌트를 활용하지 않는다** (24장 §"Introducing
  __init_subclass__", p.914).[^ramalho2022] 저자의 `Checked` 예제가 그 빈자리를 채운다.
- 한계도 함께 적혀 있다 — **런타임 타입 검사를 위해 상상 가능한 모든 정적 타입 힌트를
  지원하는 것은 불가능하고, 그것이 아마 `typing.NamedTuple`과 `@dataclass`가 시도조차
  하지 않는 이유일 것이다** (같은 절, p.914).[^ramalho2022]
- 첫 인자가 남다르다 (24장 §"__init_subclass__ Is Not a Typical Class Method",
  p.919):[^ramalho2022]

> The first argument that Python passes to `__init_subclass__` is a class. However, it is
> never the class where `__init_subclass__` is implemented: it is a newly defined subclass
> of that class. That's unlike `__new__` and every other class method that I know about.
> Therefore, I think `__init_subclass__` is not a class method in the usual sense, and it
> is misleading to name the first argument `cls`.

  - `@classmethod` 데코레이터를 붙이지 않는 것도 특이한데, 저자가 그 자체는 대수롭지
    않다고 적는다 — **`@classmethod` 데코레이터는 `__init_subclass__`와 함께 결코 쓰이지
    않지만, 그것이 큰 뜻은 아니다. `__new__` 특수 메서드도 `@classmethod` 없이 클래스
    메서드처럼 동작하기 때문이다** (같은 절, p.919).[^ramalho2022]
- 예의 하나가 명시된다 — **`super().__init_subclass__()`는 엄격히 필요하지는 않지만,
  같은 상속 그래프에서 `.__init_subclass__()`를 구현할 수 있는 다른 클래스와 잘 지내려면
  호출되어야 한다** (24장 §"Introducing __init_subclass__", pp.918–919).[^ramalho2022]
- 정적 검사기의 한계가 이 기법에 따라온다 — **Mypy는 이 생성자 호출에서 타입 오류를
  검출할 수 없다. `Movie`가 `Checked.__init__`을 상속하는데, 그 메서드의 시그니처는
  임의의 사용자 정의 클래스를 지원하려고 어떤 키워드 인자든 받아들여야 하기 때문이다**
  (24장 §"Checked Subclasses and Static Type Checking", p.916).[^ramalho2022]
  타입 매개변수도 무시된다 — **`list[float]` 타입 힌트로 `Checked` 하위 클래스 필드를
  선언하면 Mypy는 호환되지 않는 내용의 리스트 대입을 표시할 수 있지만, `Checked`는 타입
  매개변수를 무시하고 그것을 `list`와 같게 취급할 것이다** (같은 절,
  p.916).[^ramalho2022]

## 클래스 데코레이터를 고르는 이유

- 정의 — **클래스 데코레이터는 함수 데코레이터와 비슷하게 동작하는 호출 가능한 것이다:
  장식된 클래스를 인자로 받고, 장식된 클래스를 대체할 클래스를 돌려주어야 한다. 클래스
  데코레이터는 속성 대입을 통해 더 많은 메서드를 주입한 뒤 장식된 클래스 자신을 돌려주는
  일이 잦다** (24장 §"Enhancing Classes with a Class Decorator", p.922).[^ramalho2022]
- 선택 기준이 한 줄이다 (같은 절, p.922):[^ramalho2022]

> Probably the most common reason to choose a class decorator over the simpler
> `__init_subclass__` is to avoid interfering with other class features, such as
> inheritance and metaclasses.

  각주가 그 근거의 출처를 밝힌다 — **이 논거는 PEP 557–Data Classes의 초록에 나타나며,
  그것이 클래스 데코레이터로 구현된 이유를 설명한다** (같은 절 각주 10,
  p.922).[^ramalho2022]
- 이름 짓기 관례 하나가 따라온다 — 데코레이터가 주입할 함수들에 밑줄 접두를 붙이는데
  사유가 둘이다 (같은 절, p.924):[^ramalho2022]
  - **`checked`는 모듈의 공개 인터페이스의 일부이지만 다른 함수들은 아니다.**
  - **그 함수들은 장식된 클래스에 주입될 것이고, 앞의 `_`가 장식된 클래스의 사용자 정의
    속성·메서드와 이름이 충돌할 가능성을 줄인다.**
- 규모의 대비가 마지막에 붙는다 — **`checkeddeco.py` 모듈은 단순하지만 쓸 만한 클래스
  데코레이터를 구현한다. 파이썬의 `@dataclass`는 훨씬 더 많은 일을 한다. (…) 파이썬
  3.9의 `dataclasses` 패키지 소스 코드는 1,200줄이 넘는다** (같은 절,
  p.925).[^ramalho2022]

## __slots__만은 왜 안 되는가

- 시점 문제 — **`__slots__` 속성은 그것이 `type.__new__`에 넘겨지는 클래스 네임스페이스의
  항목 중 하나일 때에만 효력이 있다. 기존 클래스에 `__slots__`를 더하는 것은 아무 효과가
  없다. 파이썬은 클래스가 지어진 뒤에야 `__init_subclass__`를 발동한다 — 그때는
  `__slots__`를 설정하기에 이미 늦다. 클래스 데코레이터도 `__slots__`를 설정할 수 없다.
  그것은 `__init_subclass__`보다도 더 늦게 적용되기 때문이다** (24장 §"Why
  __init_subclass__ Cannot Configure __slots__", p.921).[^ramalho2022]
- 남는 길이 둘 — **실행 중에 `__slots__`를 설정하려면 당신의 코드가 `type.__new__`의
  마지막 인자로 넘어가는 클래스 네임스페이스를 직접 지어야 한다. 그러려면 클래스 팩토리
  함수를 쓰거나, 핵폭탄 선택지를 택해 메타클래스를 구현할 수 있다** (같은 절,
  p.921).[^ramalho2022]
- 그 "핵폭탄 선택지"를 정당화하려고 저자가 가공의 시나리오를 만들고 그 사실을 밝힌다 —
  **나는 이른 최적화와 과잉 설계를 부추기고 싶지 않으므로, `__slots__`로 `checkedlib.py`를
  다시 쓰는 것을 정당화할 지어낸 시나리오를 여기 둔다. 그것이 메타클래스의 적용을
  요구한다. 건너뛰어도 좋다** (24장 §"A Metaclass Solution for Checked",
  p.942).[^ramalho2022] 그 시나리오가 드는 이득 둘 — **`Checked` 인스턴스가 자기
  `__dict__`를 필요로 하지 않아 메모리 사용이 줄고**, **예상치 못한 속성을 막으려고만
  만들어졌던 `__setattr__`을 제거해 성능이 오른다.**
- `__slots__`를 쓰면 저장 속성 이름이 갈려야 한다는 귀결이 따라온다 — **`Movie` 같은
  클래스가 `__slots__`를 쓰면 같은 이름의 클래스 속성과 인스턴스 속성을 가질 수 없다.
  각 디스크립터 인스턴스가 클래스 속성이므로, 이제 인스턴스별 별도 저장 속성이 필요하다.
  코드는 디스크립터 이름에 밑줄 하나를 붙인 것을 쓴다. 따라서 `Field` 인스턴스는 별도의
  `name`과 `storage_name` 속성을 갖고, 우리는 `Field.__get__`을 구현한다** (같은 절,
  p.943).[^ramalho2022]

## 메타클래스

- 경구가 Tim Peters의 말이다 (24장 §"Metaclasses 101", p.931):[^ramalho2022]

> [Metaclasses] are deeper magic than 99% of users should ever worry about. If you wonder
> whether you need them, you don't (the people who actually need them know with certainty
> that they need them, and don't need an explanation about why).

- 정의 — **메타클래스는 클래스 팩토리다. `record_factory`와 달리 메타클래스는 클래스로
  쓰인다. 달리 말해 메타클래스는 그 인스턴스가 클래스인 클래스다** (같은 절,
  p.931).[^ramalho2022]
- 무한 후퇴를 피하는 자리 — **파이썬 객체 모델을 생각해 보라: 클래스는 객체이므로 각
  클래스는 다른 어떤 클래스의 인스턴스여야 한다. 기본적으로 파이썬 클래스는 `type`의
  인스턴스다. (…) 무한 후퇴를 피하기 위해 `type`의 클래스는 `type`이다** (같은 절,
  pp.931–932).[^ramalho2022]
- 두 관계를 섞지 말라는 경고가 붙는다 — **내가 `str`이나 `LineItem`이 `type`의 하위
  클래스라고 말하는 것이 아님을 주의하라. 내가 말하는 것은 `str`과 `LineItem`이 `type`의
  인스턴스라는 것이다. 그들은 전부 `object`의 하위 클래스다** (같은 절,
  p.932).[^ramalho2022] 그리고 그 둘의 관계는 언어로 표현할 수 없다 — **`object`와 `type`
  클래스는 유일한 관계를 갖는다: `object`는 `type`의 인스턴스이고, `type`은 `object`의
  하위 클래스다. 이 관계는 "마법"이다: 파이썬으로 표현될 수 없다. 어느 클래스든 다른
  것이 정의될 수 있기 전에 존재해야 하기 때문이다** (같은 절, p.932).[^ramalho2022]
- 핵심 관계 — **메타클래스는 `type`의 하위 클래스이고, 그것이 그들을 클래스 팩토리로
  동작하게 만든다** (같은 절, p.933).[^ramalho2022] 실물이 하나 있다 — **`ABCMeta` 같은
  메타클래스는 `type`으로부터 클래스를 구성하는 힘을 상속한다** (같은 절,
  pp.932–933).[^ramalho2022]
- 무엇을 언제 손볼 수 있는가 — **`MetaKlass.__new__`를 구현할 때, `super().__new__`에
  넘기기 전에 그 인자들을 조사하고 바꿀 수 있다. `super().__new__`가 반환한 뒤에는 새로
  만들어진 클래스에 추가 처리를 적용한 뒤 파이썬에 돌려줄 수도 있다** (24장 §"How a
  Metaclass Customizes a Class", p.934).[^ramalho2022]
- 순서가 명시된다 — **그다음 파이썬이 `SuperKlass.__init_subclass__`를 부르면서 당신이
  만든 클래스를 넘기고, 그다음 클래스 데코레이터가 있으면 그것을 적용한다. 마지막으로
  파이썬이 클래스 객체를 둘러싼 네임스페이스의 그 이름에 묶는다** (같은 절,
  p.934).[^ramalho2022]
- 그리고 `__new__`에서만 할 수 있는 일 하나 — **`type.__new__`가 돌기 전에 `cls_dict`에
  더해야 하는 속성이 하나 있으니 `__slots__`다. 메타클래스의 `__new__` 메서드가
  `__slots__`를 구성하기에 이상적인 자리다** (같은 절, p.934).[^ramalho2022]
- 임포트 시점과 런타임의 경계가 흐리다는 것이 이 장의 실험 절 주제다 — **파이썬
  프로그래머들은 "임포트 시점" 대 "런타임"을 이야기하지만, 그 용어들은 엄격히 정의돼
  있지 않고 그 사이에 회색지대가 있다** (24장 §"What Happens When: Import Time Versus
  Runtime", p.925).[^ramalho2022] 사유가 둘이다 — **`import` 문은 단순한 선언이 아니라,
  프로세스에서 모듈이 처음 임포트될 때 그 모듈의 모든 최상위 코드를 실제로 돌린다**,
  그리고 **"임포트 시점"은 런타임 깊숙한 곳에서 일어날 수도 있다. `import` 문과
  `__import__()` 내장이 어떤 평범한 함수 안에서든 쓰일 수 있기 때문이다** (같은 절,
  pp.925–926).[^ramalho2022]
  - 그 실험 자체에 대한 저자의 단서가 있다 — **단일 클래스에 클래스 데코레이터와
    `__init_subclass__` 기반 클래스 빌더를 함께 적용하는 것은 과잉 설계나 절망의
    징후일 가능성이 높다** (24장 §"Evaluation Time Experiments",
    p.926).[^ramalho2022]

## 현대 기능이 대체한 자리

- 목록 넷 (24장 §"Modern Features Simplify or Replace Metaclasses",
  pp.947–948):[^ramalho2022]
  - *클래스 데코레이터* — **메타클래스보다 이해하기 단순하고, 기반 클래스·메타클래스와
    충돌을 일으킬 가능성이 적다.**
  - `__set_name__` — **디스크립터의 이름을 자동으로 설정하기 위한 맞춤 메타클래스 로직의
    필요를 없앤다.**
  - `__init_subclass__` — **최종 사용자에게 투명하고 데코레이터보다도 단순한 클래스 생성
    맞춤화 방법을 제공한다 — 그러나 복잡한 클래스 계층에서는 충돌을 들여올 수 있다.**
  - *삽입 순서를 보존하는 내장 `dict`* — **`__prepare__`를 쓸 첫째 이유를 없앴다: 구성
    중인 클래스의 네임스페이스를 저장할 `OrderedDict`를 제공하는 것. 파이썬은
    메타클래스에서만 `__prepare__`를 부르므로, 파이썬 3.6 이전에는 클래스 네임스페이스를
    소스 코드에 나타난 순서대로 처리해야 한다면 메타클래스를 써야 했다.**
- 저자의 동기가 그다음 줄에 있다 — **나는 이 기능들을 계속 옹호한다. 우리 직업에 불필요한
  복잡성이 너무 많이 보이고, 메타클래스는 복잡성으로 가는 관문이기 때문이다** (같은 절,
  p.948).[^ramalho2022]
- 그러나 메타클래스는 안정된 기능이다 — **메타클래스는 2002년 파이썬 2.2에 이른바 "새
  스타일 클래스"·디스크립터·프로퍼티와 함께 도입됐다. Alex Martelli가 2002년 7월에 처음
  올린 `MetaBunch` 예제가 파이썬 3.9에서도 여전히 동작한다는 것은 주목할 만하다 — 유일한
  변경은 쓸 메타클래스를 지정하는 방법이고, 파이썬 3에서는 `class Bunch(metaclass=MetaBunch):`
  문법으로 한다** (24장 §"Metaclasses Are Stable Language Features",
  p.948).[^ramalho2022]
  - 그리고 대체가 파괴적이지 않았다 — **§"Modern Features Simplify or Replace Metaclasses"에서
    언급한 어떤 추가도 메타클래스를 쓰는 기존 코드를 깨뜨리지 않았다. 그러나 메타클래스를
    쓰는 레거시 코드는 그 기능들을 활용해 종종 단순화될 수 있다 — 특히 더 이상 유지되지
    않는 3.6 이전 파이썬 판 지원을 버릴 수 있다면** (같은 절, p.948).[^ramalho2022]
  - 버전 조건: 파이썬 3.6 이상. `__set_name__`·`__init_subclass__`·삽입 순서 보존
    `dict`이 전부 그 판에 왔고, **2021년 기준 활발히 유지되는 모든 CPython 판이 위
    기능 전부를 지원한다** (같은 절, p.948).[^ramalho2022]

## 실무에서 지킬 것

- 메타클래스는 하나뿐이다 — **클래스 선언이 둘 이상의 메타클래스를 포함하면 어리둥절한
  오류 메시지를 보게 된다.** 그리고 **이것은 다중 상속 없이도 일어날 수 있다** (24장
  §"A Class Can Only Have One Metaclass", p.948).[^ramalho2022] 예로 든 것이
  `class Record(abc.ABC, metaclass=PersistentMeta):`이고 — **`abc.ABC`가 `abc.ABCMeta`
  메타클래스의 인스턴스이므로, 그 `Persistent` 메타클래스가 `abc.ABCMeta`의 하위 클래스가
  아니면 메타클래스 충돌이 난다.**
- 해법이 둘인데 둘 다 대가가 있다 (같은 절, p.949):[^ramalho2022]
  - **관련된 메타클래스 중 적어도 하나를 피하면서 필요한 일을 하는 다른 방법을 찾는다.**
  - **다중 상속을 써서 `abc.ABCMeta`와 `PersistentMeta` 둘 다의 하위 클래스인 자기
    `PersistentABCMeta` 메타클래스를 짓고, 그것을 `Record`의 유일한 메타클래스로 쓴다.**
  - 뒤엣것에 경고가 붙는다 — **두 기반 메타클래스를 가진 메타클래스 해법이 마감을 맞추려고
    구현되는 것을 상상할 수 있다. 내 경험상 메타클래스 프로그래밍은 언제나 예상보다 오래
    걸리고, 그것이 촉박한 마감 앞에서 이 접근을 위험하게 만든다. 그렇게 해서 마감을 맞춘다
    해도 코드는 미묘한 버그를 담고 있을 수 있다. 알려진 버그가 없더라도, 이해하고 유지하기
    어렵다는 단순한 이유로 이 접근을 기술 부채로 여겨야 한다** (같은 절,
    p.949).[^ramalho2022]
- 사용자에게 보이면 안 된다 — **`type` 말고 파이썬 3.9 표준 라이브러리 전체에 메타클래스는
  여섯 개뿐이다. 더 잘 알려진 메타클래스는 아마 `abc.ABCMeta`·`typing.NamedTupleMeta`·
  `enum.EnumMeta`일 것이다. 그중 어느 것도 사용자 코드에 명시적으로 나타나도록 의도되지
  않았다. 우리는 그것들을 구현 세부로 여길 수 있다** (24장 §"Metaclasses Should Be
  Implementation Details", p.949).[^ramalho2022]
- 그래서 조문 — **메타클래스로 정말 괴상한 메타프로그래밍을 할 수 있지만, 대부분의
  사용자가 메타클래스를 정말로 구현 세부로 여길 수 있도록 최소 놀람의 원칙(principle of
  least astonishment)을 따르는 것이 최선이다** (같은 절, p.949).[^ramalho2022]
- 미래 대비의 방법도 하나 지목된다 — **2022년 저술 시점까지의 몇 년 사이 파이썬 표준 라이브러리의 어떤
  메타클래스들은 패키지의 공개 API를 깨뜨리지 않고 다른 기제로 대체됐다. 그런 API를
  미래에 대비시키는 가장 단순한 방법은, 메타클래스가 제공하는 기능에 접근하기 위해
  사용자가 하위 클래싱하는 평범한 클래스를 제공하는 것이다 — 우리 예제에서 한 대로**
  (같은 절, p.949).[^ramalho2022]

## 이 도구들은 누구를 위한 것인가

- 쓸모의 목록 여덟 (24장 §"Wrapping Up", p.952):[^ramalho2022] **하위 클래스 등록,
  하위 클래스 구조 검증, 여러 메서드에 데코레이터를 한꺼번에 적용, 객체 직렬화,
  객체-관계 매핑, 객체 기반 영속성, 클래스 수준에서 특수 메서드 구현, 그리고 트레이트나
  관점 지향 프로그래밍처럼 다른 언어에 있는 클래스 기능의 구현.** 그리고 부수적으로 —
  **클래스 메타프로그래밍은 어떤 경우 성능 문제에도 도움이 될 수 있다. 그러지 않으면
  런타임에 되풀이 실행될 작업을 임포트 시점에 수행함으로써.**
- 그러나 결론은 기각 쪽이다. 저자가 13장의 Alex Martelli 인용을 다시 부른다 (같은 절,
  p.952):[^ramalho2022]

> And, *don't* define custom ABCs (or metaclasses) in production code… if you feel the
> urge to do so, I'd bet it's likely to be a case of "all problems look like a
> nail"-syndrome for somebody who just got a shiny new hammer—you (and future maintainers
> of your code) will be much happier sticking with straightforward and simple code,
> eschewing such depths.

- 그리고 그 적용 범위를 스스로 넓힌다 (같은 절, p.952):[^ramalho2022]

> I believe Martelli's advice applies not only to ABCs and metaclasses, but also to class
> hierarchies, operator overloading, function decorators, descriptors, class decorators,
> and class builders using `__init_subclass__`.

- 가르는 선이 한 문단이다 (같은 절, pp.952–953):[^ramalho2022]

> Those powerful tools exist primarily to support library and framework development.
> Applications naturally should *use* those tools, as provided by the Python standard
> library or external packages. But *implementing* them in application code is often
> premature abstraction.

- 그 문단을 David Heinemeier Hansson의 말이 맺는다 (같은 절, p.953):[^ramalho2022]

> Good frameworks are extracted, not invented.

- 다만 저자 자신은 언어 설계 쪽에서 "급진적" 입장에 선다. 곁글에서 Harvey와 Wright의
  두 견해를 인용하는데, 보수적 견해가 **"500명의 평범한 프로그래머가 힘을 합쳐 명세를
  올바로 충족하는 프로그램을 만들 수 있도록 일을 규율하는 법을 가르치는 것"**이고 급진적
  견해가 **"프로그램이 들어갈 수 있도록 사람들이 자기 마음을 넓히는 법을 가르치는 것 —
  자명한 것보다 더 크고 더 강력하고 더 유연한 발상의 어휘로 생각하는 법을 배움으로써"**다.
  저자의 선택이 명시된다 — **지금쯤 당신은 내가 "급진적" 견해를 지지한다는 것을 짐작했을
  것이고, 파이썬이 그 정신으로 설계됐다고 나는 믿는다** (24장 §"Soapbox",
  p.956).[^ramalho2022]
  - 그 견해 아래에서 프로퍼티·디스크립터·일급 함수·클래스가 하나로 꿰인다 — **디스크립터와
    고차 함수의 결합이 함수와 메서드의 통일을 가능하게 한다. 함수의 `__get__`이 인스턴스를
    `self` 인자에 묶어 즉석에서 메서드 객체를 만든다. 이것은 우아하다** (같은 절,
    pp.956–957).[^ramalho2022]
  - 그리고 통합의 기준 — **가장 좋은 언어 기능은 모두를 이롭게 하는 것이다. 어떤 파이썬
    사용자가 그것을 알지 못하더라도. 그러나 그들은 언제나 배워서 다음의 위대한
    라이브러리를 만들 수 있다** (같은 절, p.957).[^ramalho2022]
- **이 페이지가 소스와 어긋나 보이는 자리를 그대로 남겼다.** 저자는 같은 장에서 이 기법들을
  "피하라"고 말하면서 스무 줄짜리 메타클래스 핵(`__prepare__`가 `__missing__`을 구현하는
  매핑을 돌려주게 해 상수를 자동 생성하는 것)을 **"이 장을 연구하며 찾은 가장 멋지고
  작은 메타클래스 예"**라 부르며 싣고 독자에게 확장을 권한다 (24장 §"A Metaclass Hack
  with __prepare__", pp.950–951).[^ramalho2022] #hypothesis 두 태도가 모순이 아니라 대상이
  다르다고 읽는 것이 맞다 — 기각의 대상은 **애플리케이션 코드에서의 구현**이고, 권유의
  대상은 **언어 기제에 대한 이해**다. 저자 자신이 그 구분을 §"Wrapping Up"에서
  *use*와 *implement*로 표시한다.

## 이어지는 페이지

- [속성 디스크립터](../concepts/attribute-descriptors.md) — 앞 장. `__set_name__`을 부르는 것이
  `type.__new__`라는 것과, 클래스 속성 쓰기를 제어하려면 여기로 올라와야 한다는 것
- [동적 속성과 프로퍼티](dynamic-attributes-and-properties.md) — `__new__`가 생성자라는
  규정과 팩토리로 클래스를 대체하는 사유의 정본
- [데이터 클래스 빌더](data-class-builders.md) — 여기 서술된 기법 위에 서 있는 표준
  라이브러리의 클래스 빌더 셋
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 여기 시점 문제가 걸리는
  그 클래스 속성
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — `abc.ABCMeta`가 이
  장에서 말하는 메타클래스의 실물로 다시 나오는 자리
- [협력적 다중 상속과 MRO](cooperative-multiple-inheritance.md) —
  `super().__init_subclass__()`를 부르라는 예의가 근거하는 기제
- [추상화 고르기](../concepts/choosing-abstractions.md) — "이른 추상화"라는 판정이 닿는 원리 쪽
- [파이썬의 클래스 메타프로그래밍](../synthesis/python-class-metaprogramming.md) — 이 축의
  허브

[^ramalho2022]: Ramalho 2022, 24장 "Class Metaprogramming" 도입(pp.907–908) · §"What's New
    in This Chapter"(p.908) · §"Classes as Objects"(pp.908–909) · §"type: The Built-In
    Class Factory"(pp.909–910) · §"A Class Factory Function"(pp.911–914) · §"Introducing
    __init_subclass__"(pp.914–921) · §"Checked Subclasses and Static Type
    Checking"(p.916) · §"__init_subclass__ Is Not a Typical Class Method"(p.919) ·
    §"Why __init_subclass__ Cannot Configure __slots__"(p.921) · §"Enhancing Classes with a
    Class Decorator"(pp.922–925) · §"What Happens When: Import Time Versus
    Runtime"(pp.925–926) · §"Evaluation Time Experiments"(p.926) · §"Metaclasses
    101"(pp.931–934) · §"How a Metaclass Customizes a Class"(pp.933–934) · §"A Metaclass
    Solution for Checked"(pp.942–943) · §"Metaclasses in the Real World"(pp.947–949) ·
    §"A Metaclass Hack with __prepare__"(pp.950–951) · §"Wrapping Up"(pp.952–953) ·
    §"Soapbox"(pp.956–957). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀
    값이고, 그 오프셋 실측과 판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이
    정본이다. 그림 24-1~24-4(메타클래스의 Mills & Gizmos 도해와 UML 클래스 다이어그램)는
    전부 이미지로 조판돼 있어 캡션과 본문 서술로만 옮겼다. **코드 펜스를 두지 않았다** —
    이 장의 예제들(`record_factory`·`checkedlib`·`checkeddeco`·`MetaBunch`·`autoconst`)은
    전부 여러 클래스와 모듈에 걸친 코드라 잘라 내면 복사해서 돌지 않고, 이 장이 이 KB에
    남길 것은 코드가 아니라 **무엇을 언제 고르고 언제 고르지 않는가의 판단**이라고 보아
    그 판단만 옮겼다. PDF 988·992쪽은 도비라·백지라 추출이 OCR 필요 판정을 냈다 —
    손실 아님.

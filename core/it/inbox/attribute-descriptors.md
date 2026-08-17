---
type: concept
title: 속성 디스크립터
description: 같은 접근 로직을 여러 속성에 재사용하는 기제와 그것을 말하는 데 필요한 여섯 낱말, __set__의 유무가 만드는 오버라이딩과 비오버라이딩의 갈림과 그 비대칭이 읽기·쓰기 규칙에서 나오는 이유, 클래스에 대입하면 디스크립터가 그냥 사라진다는 사실, 메서드가 실은 비오버라이딩 디스크립터라는 것, 그리고 네 가지 사용 지침
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 속성 디스크립터

- [무엇을 재사용하는가](#무엇을-재사용하는가)
- [여섯 낱말](#여섯-낱말)
- [__set_name__이 없앤 중복](#__set_name__이-없앤-중복)
- [오버라이딩과 비오버라이딩](#오버라이딩과-비오버라이딩)
- [클래스에 대입하면 그냥 사라진다](#클래스에-대입하면-그냥-사라진다)
- [메서드는 디스크립터다](#메서드는-디스크립터다)
- [사용 지침 넷](#사용-지침-넷)
- [디스크립터가 못 하는 것](#디스크립터가-못-하는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **같은 속성 접근 규칙을 여러 속성과 여러 클래스에 걸쳐 한 번만 쓰려면 무엇을
정의하고, 그것이 언제 인스턴스 속성을 이기는가.**

## 무엇을 재사용하는가

- 규정 — **디스크립터는 같은 접근 로직을 여러 속성에서 재사용하는 방법이다. 예컨대 장고
  ORM이나 SQLAlchemy 같은 ORM의 필드 타입이 디스크립터로, 데이터베이스 레코드의 필드에서
  파이썬 객체 속성으로, 또 그 반대로 데이터의 흐름을 관리한다** (23장 도입,
  p.879).[^ramalho2022]
- 프로토콜의 정의 — **디스크립터는 `__get__`·`__set__`·`__delete__` 메서드로 이루어진
  동적 프로토콜을 구현하는 클래스다. `property` 클래스는 완전한 디스크립터 프로토콜을
  구현한다. 동적 프로토콜에서 늘 그렇듯 부분 구현이 허용된다. 실제로 우리가 실제 코드에서
  보는 디스크립터 대부분은 `__get__`과 `__set__`만 구현하고, 다수는 그중 하나만 구현한다**
  (같은 자리, p.879).[^ramalho2022]
- 언어 안에서의 지위 — **디스크립터는 파이썬을 구별 짓는 기능으로, 애플리케이션 층뿐
  아니라 언어 기반 구조에도 배치돼 있다. 사용자 정의 함수가 디스크립터다** (같은 자리,
  p.879).[^ramalho2022] 저자가 그 중요성을 못 박는다 — **디스크립터를 이해하는 것이 파이썬
  숙달의 열쇠다** (같은 자리, p.879).[^ramalho2022] 그리고 경구가 Raymond Hettinger의
  말이다 (같은 자리, p.879):[^ramalho2022]

> Learning about descriptors not only provides access to a larger toolset, it creates a
> deeper understanding of how Python works and an appreciation for the elegance of its
> design.

- 프로퍼티 팩토리와의 관계 — **프로퍼티 팩토리는 함수형 프로그래밍 패턴을 적용해 게터와
  세터의 반복 코딩을 피하는 방법이다. 프로퍼티 팩토리는 매개변수화된 접근자 함수 집합을
  만들고 그것들로부터 맞춤 `property` 인스턴스를 지으며, `storage_name` 같은 설정을
  붙들기 위해 클로저를 쓰는 고차 함수다. 같은 문제를 푸는 객체 지향적 방식이 디스크립터
  클래스다** (23장 §"Descriptor Example: Attribute Validation", p.880).[^ramalho2022]
- 클래스이므로 상속을 쓸 수 있다는 것이 실무의 이득이다 — **디스크립터는 클래스로 구현되므로
  상속을 활용해 새 디스크립터를 위한 코드 일부를 재사용할 수 있다** (23장 §"LineItem
  Take #4: Automatic Naming of Storage Attributes", p.889).[^ramalho2022] 저자의 예에서
  추상 기반 클래스 `Validated`가 `__set__`을 오버라이드하고 하위 클래스가 구현해야 하는
  `validate` 메서드를 부른다 — **`Validated`·`Quantity`·`NonBlank` 사이의 관계는
  *Design Patterns* 고전이 서술한 템플릿 메서드(template method)의 적용이다** (23장
  §"LineItem Take #5: A New Descriptor Type", p.889).[^ramalho2022] 다른 이름도 함께
  적혀 있다 — **Alex Martelli는 이 디자인 패턴을 자기 위임(Self-Delegation)이라 부르기를
  선호하고, 나도 그것이 더 서술적인 이름이라는 데 동의한다** (같은 절,
  p.890).[^ramalho2022]
- 검증 메서드가 값을 돌려주게 한 이유도 명시된다 — **구체 `validate` 메서드가 검증된 값을
  돌려주도록 요구하면 받은 데이터를 정리·변환·정규화할 기회를 준다** (같은 절,
  p.891).[^ramalho2022]

## 여섯 낱말

- 저자가 용어를 먼저 고정한다 — **디스크립터를 구현하고 쓰는 일은 여러 구성 요소를
  포함하므로, 그 구성 요소들에 이름을 붙일 때 정확한 것이 유용하다** (23장 §"Terms to
  understand descriptors", p.881).[^ramalho2022] 정의 여섯 (같은 절,
  pp.881–882):[^ramalho2022]
  - *디스크립터 클래스(Descriptor class)* — **디스크립터 프로토콜을 구현하는 클래스.**
  - *관리 클래스(Managed class)* — **디스크립터 인스턴스가 클래스 속성으로 선언된 클래스.**
  - *디스크립터 인스턴스(Descriptor instance)* — **관리 클래스의 클래스 속성으로 선언된,
    디스크립터 클래스의 각 인스턴스.**
  - *관리 인스턴스(Managed instance)* — **관리 클래스의 인스턴스 하나.**
  - *저장 속성(Storage attribute)* — **그 특정 인스턴스에 대한 관리 속성의 값을 담는,
    관리 인스턴스의 속성.** **그것들은 언제나 클래스 속성인 디스크립터 인스턴스와
    구별된다.**
  - *관리 속성(Managed attribute)* — **디스크립터 인스턴스가 다루고 값이 저장 속성에
    저장되는, 관리 클래스의 공개 속성.** 달리 말해 **디스크립터 인스턴스와 저장 속성이
    관리 속성을 위한 기반 구조를 제공한다.**
- 같은 이름이 두 자리에 있다는 것이 이 그림의 요점이다 — **`weight`라는 낱말이 두 번
  나타나는데, 정말로 `weight`라는 이름의 서로 다른 속성이 둘 있기 때문이다: 하나는
  `LineItem`의 클래스 속성이고, 다른 하나는 각 `LineItem` 객체에 존재할 인스턴스
  속성이다** (23장 §"LineItem Take #3: A Simple Descriptor", p.881).[^ramalho2022]
- 상속이 필요 없다 — **디스크립터는 프로토콜 기반 기능이다. 하나를 구현하는 데 하위
  클래싱이 필요 없다** (같은 절, p.884).[^ramalho2022]
- 저자가 UML의 한계 때문에 자기 표기법을 만들었다고 적는다 — **디스크립터를 여러 번 설명한
  뒤, UML이 관리 클래스와 디스크립터 인스턴스 사이의 관계처럼 클래스와 인스턴스가 얽힌
  관계를 보이는 데 그리 좋지 않다는 것을 깨달았다** (23장 §"Introducing Mills & Gizmos
  Notation", p.883).[^ramalho2022] 그 표기법(Mills & Gizmos Notation)은 도해라 이 KB에는
  옮기지 않았다.

## __set_name__이 없앤 중복

- 문제 — 22장 프로퍼티 팩토리와 이 장의 첫 디스크립터판 모두 관리 속성 이름을 손으로 두 번
  적어야 했다. 그것을 없앤 것이 특수 메서드 하나다 — **디스크립터 인스턴스에 속성 이름을
  다시 치는 것을 피하려고 `__set_name__`을 구현해 각 `Quantity` 인스턴스의
  `storage_name`을 설정한다. `__set_name__` 특수 메서드는 파이썬 3.6에서 디스크립터
  프로토콜에 더해졌다. 인터프리터는 클래스 몸통에서 찾은 각 디스크립터에 대해 —
  그것이 구현하고 있다면 — `__set_name__`을 부른다** (23장 §"LineItem Take #4: Automatic
  Naming of Storage Attributes", p.887).[^ramalho2022]
- 정확한 호출 주체가 각주에 있다 — **더 정확히는 `__set_name__`이 `type.__new__` —
  클래스를 나타내는 객체의 생성자 — 에 의해 불린다. `type` 내장은 사실 메타클래스, 즉
  사용자 정의 클래스의 기본 클래스다** (같은 절 각주 4, p.887).[^ramalho2022] 그 정본이
  [클래스 메타프로그래밍과 메타클래스](class-metaprogramming-and-metaclasses.md)에 있다.
- 인자 셋의 뜻 — **`self`는 디스크립터 인스턴스(관리 인스턴스가 아니다), `owner`는 관리
  클래스, `name`은 이 디스크립터 인스턴스가 `owner`의 클래스 몸통에서 대입된 `owner`
  속성의 이름이다** (같은 절, p.888).[^ramalho2022]
- 이 판에서는 `__get__`이 아예 필요 없어진다 — **`__get__`을 구현하는 것은 필요하지 않다.
  저장 속성의 이름이 관리 속성의 이름과 일치하기 때문이다. 식 `product.price`가 `LineItem`
  인스턴스에서 `price` 속성을 곧바로 얻는다** (같은 절, p.888).[^ramalho2022]
- 대표 코드가 그 판이다 (예제 23-3, pp.887–888):[^ramalho2022]

  ```python
  class Quantity:

      def __set_name__(self, owner, name):
          self.storage_name = name

      def __set__(self, instance, value):
          if value > 0:
              instance.__dict__[self.storage_name] = value
          else:
              msg = f'{self.storage_name} must be > 0'
              raise ValueError(msg)


  class LineItem:
      weight = Quantity()
      price = Quantity()

      def __init__(self, description, weight, price):
          self.description = description
          self.weight = weight
          self.price = price

      def subtotal(self):
          return self.weight * self.price
  ```

  - 찾을 것은 `__set_name__`과, 클래스 몸통에서 인자 없이 인스턴스화되는 `Quantity()`다.
  - 코드 양에 대한 저자의 변론 — **속성 두어 개를 관리하는 데 코드가 많다고 생각할 수
    있지만, 디스크립터 로직이 이제 별개의 코드 단위 — `Quantity` 클래스 — 로 추상화됐다는
    것을 깨닫는 것이 중요하다. 보통 우리는 디스크립터를 그것이 쓰이는 같은 모듈이 아니라,
    애플리케이션 전반에 걸쳐 쓰이도록 설계된 별도의 유틸리티 모듈에 정의한다 — 라이브러리나
    프레임워크를 개발한다면 여러 애플리케이션에 걸쳐서까지** (같은 절,
    p.888).[^ramalho2022]
  - 버전 조건: 파이썬 3.6 이상. 그 이전 자료에는 경고가 붙는다 — **PEP 487이 2016년에
    채택되기 전에 쓰이거나 녹화된 디스크립터에 대한 어떤 설명도 오늘날에는 불필요하게
    복잡한 예제를 담고 있을 가능성이 높다. `__set_name__`이 3.6 이전 파이썬 판에서
    지원되지 않았기 때문이다** (23장 §"Further Reading", p.904).[^ramalho2022] 저자
    자신도 1판의 예제 여럿을 이 기능 덕에 지웠다고 적는다 (23장 §"What's New in This
    Chapter", p.880).[^ramalho2022]

## 오버라이딩과 비오버라이딩

- 갈림의 뿌리가 언어의 비대칭이다 — **파이썬이 속성을 다루는 방식에 중요한 비대칭이 있다.
  인스턴스를 통해 속성을 읽으면 보통 인스턴스에 정의된 속성을 돌려주지만, 인스턴스에 그런
  속성이 없으면 클래스 속성이 회수된다. 반면 인스턴스의 속성에 대입하면 보통 클래스에는
  전혀 영향을 주지 않고 인스턴스에 속성을 만든다** (23장 §"Overriding Versus Nonoverriding
  Descriptors", p.892).[^ramalho2022]
- 그것이 디스크립터를 두 부류로 가른다 — **이 비대칭은 디스크립터에도 영향을 주어,
  `__set__` 메서드가 구현됐는지에 따라 두 넓은 범주를 만든다. `__set__`이 있으면 그
  클래스는 오버라이딩 디스크립터이고, 아니면 비오버라이딩 디스크립터다** (같은 절,
  p.892).[^ramalho2022]
- 오버라이딩 쪽의 정의 — **`__set__` 메서드를 구현하는 디스크립터는 오버라이딩
  디스크립터다. 클래스 속성이긴 하지만 `__set__`을 구현하는 디스크립터는 인스턴스 속성에
  대입하려는 시도를 무시하고 덮어쓰기 때문이다** (23장 §"Overriding Descriptors",
  p.894).[^ramalho2022] **프로퍼티도 오버라이딩 디스크립터다: 세터 함수를 제공하지 않으면
  `property` 클래스의 기본 `__set__`이 그 속성이 읽기 전용임을 알리려고
  `AttributeError`를 일으킨다** (같은 절, p.894).[^ramalho2022]
- 용어가 여럿이라는 경고가 붙는다 — **파이썬 기여자와 저자들은 이 개념을 논할 때 다른
  용어를 쓴다. 나는 *Python in a Nutshell*에서 "오버라이딩 디스크립터"를 채택했다. 공식
  파이썬 문서는 "데이터 디스크립터(data descriptor)"를 쓰지만, "오버라이딩 디스크립터"가
  그 특별한 동작을 부각한다. 오버라이딩 디스크립터는 "강제 디스크립터(enforced
  descriptor)"라고도 불린다. 비오버라이딩 디스크립터의 동의어로는 "논데이터
  디스크립터(nondata descriptor)"나 "가려질 수 있는 디스크립터(shadowable
  descriptor)"가 있다** (같은 절, p.894).[^ramalho2022]
- `__get__` 없는 오버라이딩 디스크립터가 반쪽으로 가려진다 — **이 경우 쓰기만 디스크립터가
  다룬다. 인스턴스를 통해 디스크립터를 읽으면 그 접근을 다룰 `__get__`이 없으므로
  디스크립터 객체 자체가 돌아온다. 인스턴스 `__dict__`에 직접 접근해 같은 이름의 인스턴스
  속성이 새 값으로 만들어지면, `__set__` 메서드는 그 속성을 설정하려는 이후 시도를 여전히
  덮어쓰지만, 그 속성을 읽으면 디스크립터 객체 대신 인스턴스의 새 값이 그냥 돌아온다.
  달리 말해 인스턴스 속성이 디스크립터를 가리는데, 읽을 때만 그렇다** (23장 §"Overriding
  Descriptor Without __get__", p.895).[^ramalho2022]
- 비오버라이딩 쪽 — **`__set__`을 구현하지 않는 디스크립터가 비오버라이딩 디스크립터다.
  같은 이름의 인스턴스 속성을 설정하면 디스크립터를 가려, 그 특정 인스턴스에서 그 속성을
  다루는 데 무력하게 만든다. 메서드와 `@functools.cached_property`가 비오버라이딩
  디스크립터로 구현돼 있다** (23장 §"Nonoverriding Descriptor", p.896).[^ramalho2022]

## 클래스에 대입하면 그냥 사라진다

- 사실 — **디스크립터가 오버라이딩이든 아니든, 클래스에 대입해서 덮어쓸 수 있다. 이것은
  몽키패칭 기법인데, 예제에서는 디스크립터가 정수로 대체되어, 올바른 동작을 위해
  디스크립터에 의존하던 어떤 클래스든 사실상 부술 것이다** (23장 §"Overwriting a Descriptor
  in the Class", p.897).[^ramalho2022]
- 그것이 두 번째 비대칭을 드러낸다 — **비록 클래스 속성의 읽기는 관리 클래스에 붙은
  `__get__`을 가진 디스크립터로 제어될 수 있지만, 클래스 속성의 쓰기는 같은 클래스에 붙은
  `__set__`을 가진 디스크립터로 다룰 수 없다** (같은 절, p.897).[^ramalho2022]
- 그 벽을 넘는 방법이 하나뿐이다 — **클래스에서 속성 설정을 제어하려면 디스크립터를
  클래스의 클래스에 — 다시 말해 메타클래스에 — 붙여야 한다. 기본적으로 사용자 정의
  클래스의 메타클래스는 `type`이고, `type`에 속성을 더할 수는 없다** (같은 절,
  p.898).[^ramalho2022] 그 정본이
  [클래스 메타프로그래밍과 메타클래스](class-metaprogramming-and-metaclasses.md)에 있다.

## 메서드는 디스크립터다

- 기제 — **클래스 안의 함수는 인스턴스에서 호출될 때 바인딩 메서드(bound method)가 된다.
  모든 사용자 정의 함수가 `__get__` 메서드를 갖고, 따라서 클래스에 붙었을 때 디스크립터로
  동작하기 때문이다** (23장 §"Methods Are Descriptors", p.898).[^ramalho2022]
- 어느 부류인가 — **함수는 `__set__`을 구현하지 않으므로 비오버라이딩 디스크립터다**
  (같은 절, p.898).[^ramalho2022] 그 귀결이 `obj.spam = 7` 한 줄로 메서드를 그 인스턴스에서
  접근 불가능하게 만든다.
- 클래스로 읽는 것과 인스턴스로 읽는 것이 다른 객체를 준다 — **디스크립터에서 늘 그렇듯,
  함수의 `__get__`은 접근이 관리 클래스를 통해 일어날 때 자기 자신에 대한 참조를 돌려준다.
  그러나 접근이 인스턴스를 통해 갈 때는, 함수의 `__get__`이 바인딩 메서드 객체를 돌려준다:
  함수를 감싸고 관리 인스턴스(예컨대 `obj`)를 함수의 첫 인자(즉 `self`)에 묶는 호출 가능한
  것이다 — `functools.partial` 함수가 하는 것처럼** (같은 절, p.898).[^ramalho2022]
- 바인딩 메서드 객체의 내부가 둘로 드러난다 (같은 절, p.900):[^ramalho2022]
  - **바인딩 메서드 객체는 그 메서드가 호출된 인스턴스에 대한 참조를 담은 `__self__`
    속성을 갖는다.**
  - **바인딩 메서드의 `__func__` 속성은 관리 클래스에 붙은 원래 함수에 대한 참조다.**
  - 그리고 호출 — **바인딩 메서드 객체는 실제 호출을 다루는 `__call__` 메서드도 갖는다.
    이 메서드는 `__func__`에 참조된 원래 함수를 부르면서, 메서드의 `__self__` 속성을 첫
    인자로 넘긴다. 그것이 관례적 `self` 인자의 암묵적 바인딩이 동작하는 방식이다** (같은
    절, p.900).[^ramalho2022]
- 저자의 결론 — **함수가 바인딩 메서드로 바뀌는 방식은 디스크립터가 언어에서 기반 구조로
  쓰이는 대표적인 예다** (같은 절, p.900).[^ramalho2022]

## 사용 지침 넷

- 지침들이 위 성질들의 실무적 귀결로 정리돼 있다 (23장 §"Descriptor Usage Tips",
  pp.900–901):[^ramalho2022]
  - **단순하게 두려면 `property`를 쓰라** — **`property` 내장은 세터 메서드를 정의하지
    않아도 `__set__`과 `__get__`을 구현하는 오버라이딩 디스크립터를 만든다. `property`의
    기본 `__set__`은 `AttributeError: can't set attribute`를 일으키므로, 읽기 전용 속성을
    만드는 가장 쉬운 방법이다.**
  - **읽기 전용 디스크립터는 `__set__`을 요구한다** — **디스크립터 클래스로 읽기 전용
    속성을 구현한다면 `__get__`과 `__set__`을 둘 다 코딩하기를 기억해야 한다. 그러지
    않으면 인스턴스에 같은 이름의 속성을 설정하는 것이 디스크립터를 가릴 것이다. 읽기 전용
    속성의 `__set__` 메서드는 적절한 메시지와 함께 `AttributeError`를 일으키기만 하면
    된다.**
  - **검증 디스크립터는 `__set__`만으로 동작할 수 있다** — **검증만을 위해 설계된
    디스크립터에서 `__set__` 메서드는 받은 `value` 인자를 검사하고, 유효하면 디스크립터
    인스턴스 이름을 키로 써서 인스턴스 `__dict__`에 직접 설정해야 한다. 그러면 인스턴스에서
    같은 이름의 속성을 읽는 것이 가능한 한 빠를 것이다. `__get__`을 요구하지 않기
    때문이다.**
  - **캐싱은 `__get__`만으로 효율적으로 할 수 있다** — **`__get__` 메서드만 코딩하면
    비오버라이딩 디스크립터를 갖게 된다. 이것들은 비싼 계산을 한 뒤 인스턴스에 같은 이름의
    속성을 설정해 결과를 캐시하는 데 유용하다. 같은 이름의 인스턴스 속성이 디스크립터를
    가릴 것이므로 그 속성에 대한 이후 접근은 인스턴스 `__dict__`에서 직접 가져오고 더는
    디스크립터 `__get__`을 발동시키지 않는다. `@functools.cached_property` 데코레이터가
    실제로 비오버라이딩 디스크립터를 만든다.**
    - 단서가 각주에 붙는다 — **`__init__` 메서드가 돈 뒤에 인스턴스 속성을 만드는 것은
      키 공유 메모리 최적화를 무력화한다는 것을 상기하라** (같은 절 각주 9,
      p.901).[^ramalho2022]
  - **비특수 메서드는 인스턴스 속성에 가려질 수 있다** — **함수와 메서드는 `__get__`만
    구현하므로 비오버라이딩 디스크립터다. `my_obj.the_method = 7` 같은 단순한 대입은 그
    인스턴스를 통한 `the_method`에 대한 이후 접근이 숫자 7을 회수한다는 뜻이다 — 클래스나
    다른 인스턴스에는 영향을 주지 않고. 그러나 이 문제는 특수 메서드에는 간섭하지 않는다.
    인터프리터는 특수 메서드를 클래스 자체에서만 찾는다. 달리 말해 `repr(x)`는
    `x.__class__.__repr__(x)`로 실행되므로, `x`에 정의된 `__repr__` 속성은 `repr(x)`에
    아무 효과가 없다.**
- 실무 빈도에 대한 저자의 관측이 붙는다 — **비특수 메서드가 인스턴스에서 그렇게 쉽게
  덮어써질 수 있다는 사실이 취약하고 오류를 부르는 것처럼 들릴 수 있지만, 나는 20년
  넘는 파이썬 코딩에서 개인적으로 이것에 물린 적이 없다. 반면 속성 이름이 당신이 제어하지
  않는 데이터에서 오는 동적 속성 생성을 많이 하고 있다면, 이것을 알고 있어야 하고 어쩌면
  정신 건강을 지키기 위해 동적 속성 이름의 필터링이나 이스케이핑을 구현해야 한다** (같은
  절, pp.901–902).[^ramalho2022]

## 디스크립터가 못 하는 것

- 문서화가 프로퍼티만 못하다 — **디스크립터 클래스의 독스트링은 관리 클래스에서 그
  디스크립터의 모든 인스턴스를 문서화하는 데 쓰인다.** 저자가 그것을 **다소 불만스럽다**고
  적는다 — **`LineItem`의 경우 예컨대 `weight`가 킬로그램이어야 한다는 정보를 더하면 좋을
  것이다. 그것은 프로퍼티로는 사소한 일일 텐데, 각 프로퍼티가 특정 관리 속성 하나를
  다루기 때문이다. 그러나 디스크립터로는 같은 `Quantity` 디스크립터 클래스가 `weight`와
  `price` 둘 다에 쓰인다** (23장 §"Descriptor Docstring and Overriding Deletion",
  p.902).[^ramalho2022] 회피책의 비용도 각주에 적혀 있다 — **각 디스크립터 인스턴스마다
  도움말 텍스트를 맞춤화하는 것은 놀랍도록 어렵다. 한 해법은 각 디스크립터 인스턴스마다
  래퍼 클래스를 동적으로 짓기를 요구한다** (같은 절 각주 10, p.902).[^ramalho2022]
- `__delete__`는 저자가 의도적으로 뺐다 — **나는 `__delete__` 다루기를 의도적으로
  생략했다. 실세계 쓰임이 드물다고 믿기 때문이다** (같은 절, p.902).[^ramalho2022]
- 명시적 `self`에 대한 저자의 입장이 곁글에 있다 — 그는 그것을 **"더 나쁜 것이 더
  낫다(worse is better)"의 한 예**로 본다. Richard P. Gabriel의 정의가 인용된다 (23장
  §"Soapbox — The Design of self", p.905):[^ramalho2022]

> The design must be simple, both in implementation and interface. It is more important
> for the implementation to be simple than the interface. Simplicity is the most
> important consideration in a design.

  - 그 대가가 명시된다 — **파이썬의 명시적 `self`는 그 설계 철학을 구현한다. 구현이
    단순하다 — 우아하기까지 하다 — 사용자 인터페이스를 대가로: `def zfill(self, width):`
    같은 메서드 시그니처는 `label.zfill(8)`이라는 호출 라벨과 시각적으로 맞지 않는다**
    (같은 절, p.905).[^ramalho2022]
  - 저자가 자기 불만의 범위를 좁힌다 — **나는 개인적으로 `self` 한정자를 치는 것이 싫지
    않다: 지역 변수와 속성을 구별하는 것이 좋다. 내 문제는 `def` 문에서의 `self`
    사용이다** (같은 절, p.905).[^ramalho2022]

## 이어지는 페이지

- [동적 속성과 프로퍼티](dynamic-attributes-and-properties.md) — 앞 장. 여기 디스크립터가
  일반화하는 그 프로퍼티와, 팩토리가 못 푼 이름 중복 문제
- [클래스 메타프로그래밍과 메타클래스](class-metaprogramming-and-metaclasses.md) —
  `__set_name__`을 부르는 것이 무엇인가, 그리고 클래스 속성의 쓰기를 제어하려면 어디로
  올라가야 하는가
- [파이썬의 일급 함수](first-class-functions-in-python.md) — 여기 바인딩 메서드가
  비유되는 `functools.partial`의 정본
- [디자인 패턴의 해부](design-pattern-anatomy.md) — 템플릿 메서드와 자기 위임이라는
  이름이 닿는 자리
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 캐싱 지침의 단서가
  가리키는 키 공유 최적화
- [파이썬의 클래스 메타프로그래밍](../synthesis/python-class-metaprogramming.md) — 이 축의
  허브

[^ramalho2022]: Ramalho 2022, 23장 "Attribute Descriptors" 도입(pp.879–880) · §"What's New
    in This Chapter"(p.880) · §"Descriptor Example: Attribute Validation"(pp.880–884) ·
    §"Terms to understand descriptors"(pp.881–882) · §"Introducing Mills & Gizmos
    Notation"(p.883) · §"LineItem Take #4: Automatic Naming of Storage
    Attributes"(pp.887–889) · §"LineItem Take #5: A New Descriptor Type"(pp.889–891) ·
    §"Overriding Versus Nonoverriding Descriptors"(pp.892–894) · §"Overriding
    Descriptors"(p.894) · §"Overriding Descriptor Without __get__"(pp.895–896) ·
    §"Nonoverriding Descriptor"(pp.896–897) · §"Overwriting a Descriptor in the
    Class"(pp.897–898) · §"Methods Are Descriptors"(pp.898–900) · §"Descriptor Usage
    Tips"(pp.900–902) · §"Descriptor Docstring and Overriding Deletion"(p.902) ·
    §"Further Reading"(p.904) · §"Soapbox — The Design of self"(p.905).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    그림 23-1~23-4(UML 클래스 다이어그램과 Mills & Gizmos Notation 스케치, 도움말 화면
    스크린샷)는 전부 이미지로 조판돼 있어 캡션과 본문 서술로만 옮겼다. 코드 펜스는 예제
    23-3 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만 제거했다.
    `descriptorkinds.py`의 실험용 클래스들(예제 23-8)은 표시용 보조 함수가 절반이라
    옮기지 않고 관측된 동작만 옮겼다.

---
type: concept
title: 값 객체와 엔티티
description: 도메인 객체를 정체성 유무로 가르는 구분과 그 구분이 파이썬 코드에서 갖는 모양 — 데이터는 있으나 정체성이 없는 것을 값 객체로 두는 규정과 frozen dataclass·NamedTuple·namedtuple이 공짜로 주는 값 동등성, 세 재료 중 무엇을 고르는가의 기준과 frozen이 진짜 불변은 아니라는 단서, 값 객체에도 연산이 있을 수 있다는 화폐 예제, 오래 사는 정체성을 갖는 엔티티와 그 정체성 동등성, __eq__와 __hash__를 어느 쪽에 어떻게 다는가의 규칙과 둘을 따로 건드리지 말라는 경고, 원시 타입을 NewType으로 감싸는 것에 대한 저자 자신의 기각, 그리고 이 구분의 원 정의와 정체성이 대상이 아니라 모델이 정하는 것이라는 원전의 못 박기
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 값 객체와 엔티티

- [구분의 기준은 정체성이다](#구분의-기준은-정체성이다)
- [값 객체 — dataclass가 잘 맞는 이유](#값-객체--dataclass가-잘-맞는-이유)
- [세 재료 중 무엇을 고르는가](#세-재료-중-무엇을-고르는가)
- [값 객체에도 행동이 있을 수 있다](#값-객체에도-행동이-있을-수-있다)
- [엔티티 — 값이 바뀌어도 같은 것](#엔티티--값이-바뀌어도-같은-것)
- [동등성과 해시를 어디에 어떻게 다는가](#동등성과-해시를-어디에-어떻게-다는가)
- [원시 타입 감싸기에 대한 저자의 기각](#원시-타입-감싸기에-대한-저자의-기각)
- [이벤트도 값 객체다](#이벤트도-값-객체다)
- [이 구분의 원 정의](#이-구분의-원-정의)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인 객체 둘이 "같다"는 말은 무슨 뜻이고, 그 답이 갈리는 지점에서 코드가
어떻게 달라져야 하는가.**

## 구분의 기준은 정체성이다

- 값 객체의 규정 — **데이터는 있으나 정체성(identity)이 없는 업무 개념이 있을 때마다
  우리는 흔히 그것을 값 객체(Value Object) 패턴으로 표현하기로 고른다. 값 객체는 그것이
  담은 데이터로 유일하게 식별되는 임의의 도메인 객체이며, 우리는 보통 그것을 불변으로
  만든다** (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
- 엔티티의 규정 — **우리는 오래 사는 정체성을 갖는 도메인 객체를 서술하는 데 엔티티
  (entity)라는 말을 쓴다** (1장 §"Value Objects and Entities").[^percival2020]
- 저자들이 둘을 가르는 시험은 **속성 하나를 바꿔 보는 것**이다 (1장 §"Value Objects and
  Entities"):[^percival2020]
  - **주문 라인은 주문 ID·SKU·수량으로 유일하게 식별된다. 그 값 중 하나를 바꾸면 이제
    우리는 새 라인을 갖게 된다. 그것이 값 객체의 정의다: 자기 데이터로만 식별되고 오래
    사는 정체성을 갖지 않는 임의의 객체.**
  - **이름 Harry Percival에서 글자 하나를 바꾸면 우리는 새 `Name` 객체 Barry Percival을
    갖는다.** 그리고 Harry Percival은 Barry Percival과 같지 않다.
  - **그러나 사람으로서의 Harry는 어떤가? 사람들은 이름을 바꾸고, 혼인 상태를 바꾸고,
    성별까지 바꾸지만 우리는 그들을 계속 같은 개인으로 알아본다. 이름과 달리 인간은
    지속하는 정체성을 갖기 때문이다.**
- 그래서 나오는 한 줄 — **값과 달리 엔티티는 정체성 동등성(identity equality)을 갖는다.
  우리는 그 값들을 바꿀 수 있고 그것들은 여전히 알아볼 수 있게 같은 것이다**
  (1장 §"Value Objects and Entities").[^percival2020] 예제에서는 **배치(batch)가
  엔티티다** — 라인을 할당하거나 도착 예정일을 바꿔도 같은 엔티티다.
- 곁글 요약의 마지막 한 줄이 실무 지침이다 — **무엇이 엔티티를 유일하게 식별하는지
  (보통 어떤 종류의 이름이나 참조 필드)를 정의하는 것이 중요하다**
  (1장 §"Domain Modeling Recap" 곁글).[^percival2020]

## 값 객체 — dataclass가 잘 맞는 이유

- 관측이 먼저다 — 주문에는 그것을 유일하게 식별하는 참조가 있지만 라인에는 없다.
  **주문 참조를 `OrderLine` 클래스에 더한다 해도 그것이 라인 자체를 유일하게 식별하는
  것은 아니다** (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
- 그래서 `frozen=True` 데이터클래스가 대표 재료가 된다. 값 동등성이 공짜로 따라오는
  것이 채택 이유다 — **데이터클래스(혹은 네임드튜플)가 우리에게 주는 좋은 것 하나가 값
  동등성(value equality)인데, 이는 "같은 `orderid`·`sku`·`qty`를 가진 두 라인은 같다"를
  멋있게 말한 것이다** (1장 §"Dataclasses Are Great for Value
  Objects").[^percival2020]

  ```python
  from dataclasses import dataclass
  from typing import NamedTuple
  from collections import namedtuple

  @dataclass(frozen=True)
  class Name:
      first_name: str
      surname: str

  class Money(NamedTuple):
      currency: str
      value: int

  Line = namedtuple('Line', ['sku', 'qty'])

  def test_equality():
      assert Money('gbp', 10) == Money('gbp', 10)
      assert Name('Harry', 'Percival') != Name('Bob', 'Gregory')
      assert Line('RED-CHAIR', 5) == Line('RED-CHAIR', 5)
  ```

  - 세 가지 표기가 한자리에 있는 것이 이 조각의 값이다 — `@dataclass(frozen=True)`,
    `typing.NamedTuple` 하위 클래스, `collections.namedtuple` 팩토리. **셋 다 값 동등성을
    준다.** 저자들이 각주에 이전 판본의 관행과 대안을 덧붙인다 — **이전 파이썬 버전에서는
    `namedtuple`을 썼을 것이다. Hynek Schlawack의 훌륭한 `attrs`도 살펴볼 수 있다**
    (1장 각주 2).[^percival2020]
- 그리고 이 규정이 **현실의 직관과 맞는다**는 것이 검산이다 — **이 값 객체들은 그 값이
  어떻게 작동하는지에 대한 우리의 현실 세계 직관과 들어맞는다. 우리가 어느 10파운드
  지폐를 말하는지는 중요하지 않다. 다 같은 값을 갖기 때문이다**
  (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]

## 세 재료 중 무엇을 고르는가

위 조각은 세 표기를 나란히 보이기만 하고 무엇을 왜 고르는지는 말하지 않는다. 그 선택
근거를 파이썬 관용 참조 쪽 소스가 댄다. 전문은
[데이터 클래스 빌더](../concepts/data-class-builders.md)에 있고, 여기서는 값 객체에 걸리는 것만
추린다. 두 소스가 서로를 참조한 적은 없다.

- **불변성이 첫째 갈림이다** — **`collections.namedtuple`과 `typing.NamedTuple`은 `tuple`
  하위 클래스를 지으므로 인스턴스가 불변이다. 기본적으로 `@dataclass`는 가변 클래스를
  생산한다** (5장 §"Mutable instances", p.168).[^ramalho2022] 즉 네임드튜플 둘은 불변이 기본값이고
  데이터클래스는 `frozen=True`를 **적어야** 불변이 된다. 위 조각의 `Money`·`Line`이
  `frozen` 없이도 값 객체인 이유가 그것이다.
- **⚠ 그런데 `frozen=True`가 진짜 불변은 아니다.** `@dataclass`는
  **`dataclass.FrozenInstanceError`(`AttributeError`의 하위 클래스)를 일으키는
  `__setattr__`과 `__delattr__`을 생성해 불변성을 흉내 낸다**(5장 §"More About @dataclass"
  표 5-2 각주 a, p.179)이고, 인스턴스는 **우발적 변경으로부터 합리적으로 안전하지만 정말로 불변인
  것은 아니다**.[^ramalho2022] 저자의 실무 판정이 그 뒤에 붙는다 — **파이썬 객체의 동적
  성격을 생각하면 참견하기 좋아하는 프로그래머가 `frozen=True`가 주는 보호를 우회하기가
  그리 어렵지 않다. 그러나 그러려면 필요한 요령들이 코드 리뷰에서 쉽게 눈에 띄어야 한다**
  (5장 §"More About @dataclass", p.180).[^ramalho2022]
  - **이 페이지의 규칙과 맞물리는 자리다.** 위 [동등성과 해시를 어디에 어떻게
    다는가](#동등성과-해시를-어디에-어떻게-다는가)가 "값 객체는 불변이어야 하고 해시는 모든
    값 속성에 근거해야 한다"고 요구하는데, 그 요구는 `frozen`으로 **완전히** 채워지지 않는다.
    `frozen`이 사는 것은 강제가 아니라 **의도 표시와 사고 방지**다.
- **해시 가능성이 두 옵션에 걸린다** — **`eq`와 `frozen` 인자가 둘 다 `True`이면
  `@dataclass`가 적절한 `__hash__` 메서드를 생산하므로 인스턴스가 해시 가능해진다. (…)
  `frozen=False`(기본값)이면 `@dataclass`는 `__hash__`를 `None`으로 설정해 인스턴스가 해시
  불가능함을 알리고, 어떤 상위 클래스의 `__hash__`든 덮어쓴다**
  (5장 §"More About @dataclass", p.180).[^ramalho2022]
  - 이것이 이 페이지의 두 규칙이 한 줄로 실현되는 자리다. 값 객체는
    `@dataclass(frozen=True)`로 해시를 얻고, 엔티티는 데코레이터 기본값(`frozen=False`)만으로
    이미 **해시 불가능**이 된다 — 이 페이지가 "엔티티에서는 가장 단순한 선택지가 해시를
    `None`이라 말하는 것"이라고 적은 그 상태가 파이썬의 기본값이다. #hypothesis 두 소스가
    그렇게 대응시키지는 않았다.
- **클래스 문장을 쓸 수 있는가가 셋째 갈림이다** — **`typing.NamedTuple`과 `dataclass`만이
  보통의 클래스 문장 문법을 지원해, 만들고 있는 클래스에 메서드와 독스트링을 더하기 쉽게
  만든다** (5장 §"Class statement syntax", p.168).[^ramalho2022] `collections.namedtuple`에
  메서드를 붙이는 것은 함수를 클래스 속성에 대입하는 **해킹**이고, 저자는
  **가독성과 앞으로의 유지보수를 위해서는 클래스 문장 안에서 메서드를 코딩하는 편이 훨씬
  낫다**고 적는다 (5장 §"Classic Named Tuples", p.172).[^ramalho2022]
  - **그래서 아래 [값 객체에도 행동이 있을 수 있다](#값-객체에도-행동이-있을-수-있다)가
    재료 선택에 되먹임된다.** 화폐 예제처럼 값 객체에 연산을 달 작정이라면
    `collections.namedtuple`은 제외된다. 남는 것은 `typing.NamedTuple`과
    `@dataclass(frozen=True)` 둘이다.
- **부적합 사유도 명시돼 있다.** 저자가 PEP 557의 Rationale를 인용한다 —
  **튜플이나 딕셔너리와의 API 호환이 요구될 때**, 그리고 **PEP 484·526이 제공하는 것 이상의
  타입 검증이나 값 검증·변환이 필요할 때**는 데이터 클래스를 쓸 자리가 아니다
  (5장 §"Further Reading", p.196).[^ramalho2022] 뒤쪽이 도메인 모델에서 실제로 자주 걸린다 —
  값 객체에 불변식 검증을 걸고 싶어지는 순간이 그것이고, 그때는 `__post_init__`으로 손수
  짜거나 `attrs` 같은 외부 도구로 간다.

## 값 객체에도 행동이 있을 수 있다

- 흔한 오해를 저자들이 미리 막는다 — **그렇지만 우리는 값 객체에 여전히 복잡한 행동을
  가질 수 있다. 사실 값에 대한 연산을 지원하는 것은 흔하다. 예컨대 수학 연산자가 그렇다**
  (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
- 화폐 예제가 그 실물이다 — 같은 통화의 `Money`끼리는 더하고 뺄 수 있고, 수로 곱할 수
  있으며, **다른 통화를 더하면 `ValueError`가 나고** `Money`끼리 곱하면 `TypeError`가
  난다 (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
  - 즉 값 객체는 "데이터 홀더"가 아니다. **정체성이 없다는 것과 행동이 없다는 것은 다른
    말이다.** 이 구분이 [도메인 모델 패턴](../concepts/domain-model-pattern.md)의 "무엇이든 객체일
    필요는 없다"와 짝을 이룬다 — 그쪽은 행동을 함수로 빼는 판단이고 이쪽은 값에 행동을
    남기는 판단이다.

## 엔티티 — 값이 바뀌어도 같은 것

- 엔티티에서는 동등성 연산자를 **직접 구현하는 것이 관례**다 — **우리는 보통 엔티티에
  동등성 연산자를 구현해 이것을 코드에서 명시한다**
  (1장 §"Value Objects and Entities").[^percival2020] 예제의 `Batch.__eq__`는 다른
  `Batch`인지 확인한 뒤 `reference`만 비교하고, `__hash__`는 `hash(self.reference)`다.
- 그래서 리포지터리 테스트에서 검증이 두 겹이 된다 — **첫 `assert ==`는 타입이 맞는지,
  그리고 참조가 같은지를 검사한다(기억하듯 `Batch`는 엔티티이고 우리는 그것에 대한
  맞춤 `eq`를 갖고 있으므로). 그래서 우리는 주요 속성들도 명시적으로 확인한다**
  (2장 §"The Repository in the Abstract").[^percival2020]
  - **이 귀결이 실무적으로 중요하다.** 엔티티의 `==`가 참조만 비교하도록 만들어 두면
    "같은지" 검사가 "내용이 같은지"를 말해 주지 않으므로, 저장·복원 왕복 테스트는
    속성을 따로 확인해야 한다.

## 동등성과 해시를 어디에 어떻게 다는가

- 두 매직 메서드의 역할이 규정된다 — **파이썬의 `__eq__` 매직 메서드는 `==` 연산자에
  대한 클래스의 행동을 정의한다** (1장 §"Value Objects and Entities").[^percival2020]
  그리고 **`__hash__`는 객체를 집합에 넣거나 딕셔너리 키로 쓸 때 그 행동을 통제하는 데
  파이썬이 쓰는 매직 메서드다** (1장 §"Value Objects and Entities").[^percival2020]
- 규칙이 종류별로 갈린다 (1장 §"Value Objects and Entities"):[^percival2020]
  - **값 객체에서는 해시가 모든 값 속성에 근거해야 하고, 우리는 그 객체들이 불변임을
    보장해야 한다. 데이터클래스에 `@frozen=True`를 지정하면 이것을 공짜로 얻는다.**
  - **엔티티에서는 가장 단순한 선택지가 해시를 `None`이라 말하는 것인데, 이는 그 객체가
    해시 가능하지 않아서 예컨대 집합에 쓸 수 없다는 뜻이다. 어떤 이유로 엔티티에 집합이나
    딕셔너리 연산을 정말로 쓰고 싶다고 결정한다면, 해시는 시간에 걸쳐 엔티티의 유일한
    정체성을 정의하는 `.reference` 같은 속성(들)에 근거해야 한다. 또한 그 속성을 어떻게든
    읽기 전용으로 만들려고 해야 한다.**
- **그리고 경고가 붙는다** — **이것은 까다로운 영역이다. `__eq__`도 함께 수정하지 않고
  `__hash__`를 수정해서는 안 된다. 무엇을 하고 있는지 확신이 없다면 더 읽어 보기를 권한다**
  (1장 §"Value Objects and Entities").[^percival2020] 저자들이 가리키는 글은 기술 감수자
  Hynek Schlawack의 "Python Hashes and Equality"다.
  - 이 경고는 이 언어의 계약이 짝을 이룬다는 사실에서 온다. 한쪽만 바꾸면 **같다고
    판정되는 두 객체가 다른 해시를 갖는** 상태가 만들어지고, 집합·딕셔너리가 조용히
    틀린 답을 낸다. #hypothesis 저자들이 실패 양상까지 서술하지는 않았다.

## 원시 타입 감싸기에 대한 저자의 기각

- 타입 힌트를 끝까지 밀면 원시 타입 자체를 감싸게 된다 — `typing.NewType`으로
  `Quantity = NewType("Quantity", int)`·`Sku = NewType("Sku", str)`·
  `Reference = NewType("Reference", str)`를 만들고 생성자 시그니처에 쓰는 방식이다.
  **그러면 타입 검사기가 예컨대 `Reference`가 기대되는 자리에 `Sku`를 넘기지 않는지
  확인해 줄 수 있다** (1장 §"More Types for More Type Hints" 곁글).[^percival2020]
- **저자 하나가 본문에서 그것을 기각한다.** 본문은 판단을 열어 두지만 —
  **이것이 훌륭하다고 생각하든 끔찍하다고 생각하든 논쟁거리다** — 각주가 다르다:
  **끔찍하다. 제발, 제발 이것을 하지 마라. — Harry** (1장 §"More Types for More Type
  Hints" 곁글 및 각주 4).[^percival2020]
  - 저자 둘의 판단이 갈리는 것을 그대로 인쇄한 자리다. 이 책에는 이런 자리가 여럿이며
    ([의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md)의 "과잉 설계"
    공방이 다른 예다), 그 자체가 이 소스의 지위를 규정한다 — **합의된 규범이 아니라
    두 실무자의 판단이다.**

## 이벤트도 값 객체다

- 2부에서 값 객체의 쓰임이 하나 늘어난다 — **이벤트는 값 객체의 일종이다. 이벤트는 순수한
  자료 구조이므로 아무 행동도 갖지 않는다. 우리는 언제나 도메인의 언어로 이벤트 이름을
  짓고, 그것을 우리 도메인 모델의 일부로 생각한다** (8장 §"Events Are Simple
  Dataclasses").[^percival2020]
- 그래서 재료가 같다 — **데이터클래스는 도메인 이벤트에도 훌륭하다**
  (8장 §"Events Are Simple Dataclasses").[^percival2020] 명령(command)도 마찬가지다 —
  **우리는 보통 명령을 멍청한 자료 구조로 표현하고 이벤트와 거의 같은 방식으로 처리할 수
  있다** (10장 §"Commands and Events").[^percival2020]
- 다만 대가가 명시된다 — **모델 객체와 이벤트 사이에 필드와 구조의 중복이 생길 것이고
  그것은 유지보수 비용을 갖는다. 하나에 필드를 더하는 것은 보통 다른 것 중 적어도 하나에도
  필드를 더한다는 뜻이다** (9장 §"Why Have We Achieved?").[^percival2020]

## 이 구분의 원 정의

이 구분은 이 소스가 만든 것이 아니라 도메인 주도 설계 쪽 원전에서 왔다. 원 정의 둘을
여기 둔다 — 이 페이지가 옮긴 파이썬 판정과 어긋나지 않는지 대조할 자리다.

- 값 객체(value object)의 원 정의 — **개념적 정체성이 없이 도메인의 서술적 측면을 표상하는
  객체를 값 객체라 부른다** (5장, p.98).[^evans2003] 그 존재 이유가 이어지는 한 줄에 있다
  (5장, p.98):[^evans2003]

> VALUE OBJECTS are instantiated to represent elements of the design that we care about only
> for what they are, not who or which they are.

- 엔티티(entity)의 원 정의는 처방 문단에 있다 — **객체가 속성이 아니라 그 정체성으로 구별될
  때, 모델에서 그것을 정의의 일차 요소로 삼아라. 클래스 정의를 단순하게, 생애 주기의 연속성과
  정체성에 집중해 유지하라. 그 형태나 이력과 무관하게 각 객체를 구별하는 수단을 정의하라**
  (5장, p.92).[^evans2003]
- **원전은 정체성이 사물에 내재한 성질이 아니라고 못 박는다** — **정체성은 세상의 사물에
  내재하지 않는다; 그것은 쓸모 있기 때문에 덧씌워진 의미다. 사실 현실 세계의 같은 사물이
  도메인 모델에서 엔티티로 표상될 수도 있고 아닐 수도 있다** (5장, p.93).[^evans2003]
  - 위 [구분의 기준은 정체성이다](#구분의-기준은-정체성이다)의 "속성 하나를 바꿔 보는 시험"이
    이 규정의 실무판이다. **어느 쪽인지는 대상이 아니라 모델이 정한다**는 것이 원전의
    입장이고, 그래서 같은 `Address`가 우편 서비스 소프트웨어에서는 엔티티이고 배송
    소프트웨어에서는 값 객체일 수 있다는 예가 붙는다 (5장 §VALUE OBJECTS 곁글,
  pp.97–98).[^evans2003]
- 불변성의 근거도 원전이 다른 자리에서 댄다 — **값 객체는 불변이며, 이는 생성 중에만 호출되는
  초기화자를 제외하면 그것의 모든 연산이 함수라는 것을 함의한다. 값 객체는 함수처럼 쓰기에 더
  안전하고 테스트하기 더 쉽다** (10장, p.251).[^evans2003] 그 맥락은
  [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)에 있다.

## 이어지는 페이지

- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 객체들이 사는 층
- [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md) — "무엇인지"와
  "어느 것인지"의 구분이 이름 짓기 물음과 만나는 자리
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 값 객체의 불변성이 봉사하는 조항
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 엔티티 중
  일부를 "공개" 진입점으로 올리는 셋째 구분
- [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md) — 값 객체가
  이벤트·명령으로 쓰이는 자리
- [리포지터리 패턴](../concepts/repository-pattern.md) — 이 객체들을 저장하고 되살리는 층
- [데이터 조직하기](../concepts/organizing-data.md) — 같은 값·참조 구분을 리팩터링 카탈로그가
  *Change Reference to Value*와 그 역으로 부르는 자리
- [데이터 클래스 빌더](../concepts/data-class-builders.md) — 위 세 재료의 전면 비교와 선택 기준,
  그리고 `@dataclass`의 나머지 옵션들
- [코드 냄새로서의 데이터 클래스](../concepts/data-class-as-code-smell.md) — "정체성이 없다"와
  "행동이 없다"를 혼동하면 걸리는 냄새
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브
- [딕셔너리와 집합](../concepts/dictionaries-and-sets.md) — "해시는 모든 값 속성에 근거해야 한다"가
  취향이 아니라 **해시 테이블이 깨지지 않기 위한 조건**임을 언어 쪽에서 말하는 자리
- [객체 참조와 가변성](../concepts/object-references-and-mutability.md) — 아무것도 하지 않으면 모든
  사용자 정의 클래스가 정체성으로 비교되어 사실상 엔티티가 되는 자리
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 재료들의 언어 쪽 근거가 모인 허브

[^percival2020]: Percival & Gregory 2020, 1장 "Domain Modeling"(§"Dataclasses Are Great
    for Value Objects"·§"Value Objects and Entities", 곁글 "More Types for More Type
    Hints"·"Domain Modeling Recap") · 2장 §"The Repository in the Abstract" ·
    8장 §"Events Are Simple Dataclasses" · 9장 §"Why Have We Achieved?" ·
    10장 §"Commands and Events". **이 소스의 locator는 장 단위다** — 검증 절차와 근거는
    `it/archive/percival2020/_progress.yaml` 머리말이 정본이다. 코드 펜스는 원문에서
    조판용 번호 표지 이미지를 제거했고, 원문이 세 예제를 나눠 실은 것을 한 펜스로 이었다
    (임포트는 원문 그대로다 — 이 예제는 저자들이 임포트를 생략하지 않은 몇 안 되는
    목록 중 하나다).

[^evans2003]: Evans 2003, 5장 "A Model Expressed in Software"(§ENTITIES pp.89–96 ·
    §VALUE OBJECTS pp.97–99, 곁글 "Is Address a VALUE OBJECT?" pp.97–98 포함) ·
    10장 §SIDE-EFFECT-FREE FUNCTIONS(p.251).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. **이 절은 원 정의만 든다** — 두 패턴의 설계 지침
    (§Modeling ENTITIES pp.93–94 · §Designing the Identity Operation pp.94–96 ·
    §Designing VALUE OBJECTS pp.99–102 이하)은 이 페이지의 물음(둘이 "같다"는 것이 무슨
    뜻인가) 밖이다. 이 소스에서 온 코드 펜스는 이 페이지에 없다.

[^ramalho2022]: Ramalho 2022, 5장 "Data Class Builders"(§"Mutable instances" p.168 ·
    §"Class statement syntax" p.168 · §"Classic Named Tuples" pp.169–172 ·
    §"More About @dataclass" pp.179–180과 그 표 5-2 p.179 · §"Further Reading" p.196).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 이 소스에서 온 코드 펜스는
    이 페이지에 없다 — 전문은 [데이터 클래스 빌더](../concepts/data-class-builders.md)에 있다.

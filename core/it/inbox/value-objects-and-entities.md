---
type: concept
title: 값 객체와 엔티티
description: 도메인 객체를 정체성 유무로 가르는 구분과 그 구분이 파이썬 코드에서 갖는 모양 — 데이터는 있으나 정체성이 없는 것을 값 객체로 두는 규정과 frozen dataclass·NamedTuple·namedtuple이 공짜로 주는 값 동등성, 세 재료 중 무엇을 고르는가의 기준과 frozen이 진짜 불변은 아니라는 단서, 값 객체에도 연산이 있을 수 있다는 화폐 예제, 오래 사는 정체성을 갖는 엔티티와 그 정체성 동등성, __eq__와 __hash__를 어느 쪽에 어떻게 다는가의 규칙과 둘을 따로 건드리지 말라는 경고, 원시 타입을 NewType으로 감싸는 것에 대한 저자 자신의 기각, 이 구분의 원 정의와 정체성이 대상이 아니라 모델이 정하는 것이라는 원전의 못 박기, 무엇이 엔티티를 만드는가의 원전 논의와 같은 정체성이 같은 속성을 뜻하지 않는다는 은행 거래 예제, 값 객체가 다른 객체의 조립일 수도 엔티티를 참조할 수도 있다는 확장과 속성들이 개념적 전체를 이뤄야 한다는 조항, 이 구분이 연산의 타입을 정하는 자리 — 닫힌 연산이 주로 값 객체의 기회이고 엔티티에는 드문 이유, 그리고 이 구분이 생성 인터페이스의 모양까지 정해 엔티티 팩토리와 값 객체 팩토리를 가르고 "찾거나 만들기"를 불필요하게 만드는 자리
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
status: draft
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
- [무엇이 엔티티를 만드는가](#무엇이-엔티티를-만드는가)
- [값 객체가 담을 수 있는 것](#값-객체가-담을-수-있는-것)
- [두 패턴의 설계는 어디에 있는가](#두-패턴의-설계는-어디에-있는가)
- [규칙도 값 객체가 된다](#규칙도-값-객체가-된다)
- [이 구분이 연산의 타입을 정한다](#이-구분이-연산의-타입을-정한다)
- [이 구분이 생성의 모양도 정한다](#이-구분이-생성의-모양도-정한다)
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
    소프트웨어에서는 값 객체일 수 있다는 예가 붙는다 (5장 §VALUE OBJECTS 곁글, p.98).[^evans2003]
- 불변성의 근거도 원전이 다른 자리에서 댄다 — **값 객체는 불변이며, 이는 생성 중에만 호출되는
  초기화자를 제외하면 그것의 모든 연산이 함수라는 것을 함의한다. 값 객체는 함수처럼 쓰기에 더
  안전하고 테스트하기 더 쉽다** (10장, p.251).[^evans2003] 그 맥락은
  [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)에 있다.

## 무엇이 엔티티를 만드는가

원전은 이 구분을 "정체성이 있느냐"로 시작하지 않고 **무엇이 정체성을 만드느냐**로 파고든다.
그 논의가 위 "속성 하나를 바꿔 보는 시험"이 왜 통하는지의 근거다.

- 패턴 머리의 한 줄 — **많은 객체는 근본적으로 그 속성으로 정의되지 않고 오히려 연속성과
  정체성의 실로 정의된다** (5장, p.89).[^evans2003]
- 사람의 예가 그것을 극단까지 민다 — **그 사람의 물리적 속성은 변형되고 결국 사라진다. 이름도
  바뀔 수 있다. 금전 관계는 오고 간다. 바뀔 수 없는 속성이 사람에게는 단 하나도 없다. 그런데도
  정체성은 지속한다** (5장, p.90).[^evans2003]
- **그런데 그 형이상학적 물음이 곧바로 응용의 물음으로 바뀐다** — **나는 다섯 살 때의 나와
  같은 사람인가? 이런 종류의 형이상학적 물음이 효과적인 도메인 모델을 찾는 데 중요하다.
  살짝 바꿔 말하면: 이 애플리케이션의 사용자가 내가 다섯 살 때의 나와 같은 사람인지를
  *신경 쓰는가*?** (5장, p.90).[^evans2003]
  - **판정 기준이 존재론이 아니라 사용자의 관심사라는 것이 이 문단의 값이다.**
- 정체성이 맞춰져야 하는 범위가 소프트웨어 밖까지 간다 — **개념적 정체성은 객체의 여러 구현,
  그것의 저장된 형태, 그리고 전화를 건 사람 같은 현실 세계의 행위자 사이에서 맞춰져야 한다.
  속성은 일치하지 않을 수도 있다** (5장, p.90).[^evans2003]
- 문제 서술 문단이다 (5장, p.91):[^evans2003]

> Some objects are not defined primarily by their attributes. They represent a thread of
> identity that runs through time and often across distinct representations. Sometimes such an
> object must be matched with another object even though attributes differ. An object must be
> distinguished from other objects even though they might have the same attributes. Mistaken
> identity can lead to data corruption.

- 그리고 이름이 붙는다 — **일차적으로 그 정체성으로 정의되는 객체를 엔티티라 부른다**
  (5장, p.91).[^evans2003] 설계상의 귀결이 이어진다 (5장, p.91):[^evans2003]
  - **그것들은 형태와 내용을 급격히 바꿀 수 있는 생애 주기를 갖지만 연속성의 실은 유지되어야
    한다. 그 정체성은 효과적으로 추적될 수 있도록 정의되어야 한다.**
  - **클래스 정의·책임·속성·연관이 그것이 지닌 특정 속성이 아니라 그것이 누구인가를 중심으로
    돌아야 한다.**
  - **그렇게 급격히 변형되지 않거나 그렇게 복잡한 생애 주기를 갖지 않는 엔티티라도, 그것을 이
    의미 범주에 놓으면 더 명료한 모델과 더 견고한 구현으로 이어진다.**
- 범위가 넓게 잡힌다 — **엔티티는 생애 주기를 통한 연속성과, 애플리케이션 사용자에게 중요한
  속성 독립적인 구별을 갖는 무엇이든이다. 사람일 수도, 도시일 수도, 자동차일 수도, 복권일
  수도, 은행 거래일 수도 있다** (5장, p.91).[^evans2003]
- **언어의 `==`가 이 구분을 흐린다** — 객체 지향 언어는 모든 객체에 정체성 연산을 넣어 두므로
  **그런 의미에서는 모든 객체 인스턴스가 정체성을 갖는다.** 자바 런타임 환경을 만들거나 원격
  객체를 국소 캐시하는 프레임워크를 만드는 도메인에서는 **실제로 모든 객체 인스턴스가 엔티티일
  수도 있다.** 그러나 **이 정체성 기제는 다른 응용 도메인에서는 거의 의미가 없다. 정체성은
  엔티티의 미묘하고 의미 있는 속성이며, 언어의 자동 기능에 넘길 수 없다** (5장,
  pp.91–92).[^evans2003]
  - 그 대안을 설계하는 절차는 [엔티티의 정체성 설계](entity-identity-design.md)에 있다.
- **은행 거래 예제가 이 구분의 가장 날카로운 자리다** (5장, p.92):[^evans2003]
  - **같은 계좌에 같은 날 들어온 같은 금액의 입금 둘은 여전히 별개의 거래이므로 정체성을 갖고
    엔티티다.** 반면 **그 두 거래의 금액 속성은 아마 어떤 화폐 객체의 인스턴스일 것이다.
    이 값들은 정체성을 갖지 않는데, 그것들을 구별하는 데 아무 쓸모가 없기 때문이다.**
  - 그리고 한 줄이 더 나간다 — **사실 두 객체는 같은 속성을 갖지 않고도, 심지어 반드시 같은
    클래스일 필요도 없이 같은 정체성을 가질 수 있다.** 수표 등록부의 거래와 은행 명세서의
    거래를 대조하는 일이 바로 **기록한 사람도 날짜도 다른데 같은 정체성을 가진 거래를 맞추는
    일**이고, **수표 번호의 목적이 바로 그 유일 식별자 노릇**이다.
  - **이것이 "같은 것"의 뜻을 속성 일치에서 떼어 놓는 원전의 논증이다.** 위
    [엔티티 — 값이 바뀌어도 같은 것](#엔티티--값이-바뀌어도-같은-것)이 옮긴 파이썬 쪽
    관행(참조만 비교하는 `__eq__`)이 이 논증의 코드판이고, 그래서 저장·복원 왕복 테스트가
    속성을 따로 확인해야 한다는 귀결도 여기서 나온다.
- 정체성의 유효 범위도 두 가지다 — **정체성이 특정 소프트웨어 시스템 밖에서 유의미한 것이
  흔하다. 은행 거래와 아파트 세입자가 그런 경우다. 그러나 때로는 정체성이 시스템의 맥락
  안에서만 중요하다. 컴퓨터 프로세스의 정체성 같은 것이다** (5장, p.92).[^evans2003]
- **용어 주의가 각주로 붙어 있다** — **모델 엔티티는 자바의 "entity bean"과 같은 것이 아니다.
  엔티티 빈은 다소간 엔티티를 구현하는 프레임워크로 의도되었으나 그렇게 되지 않았다. 대부분의
  엔티티는 보통의 객체로 구현된다. 어떻게 구현되든 엔티티는 도메인 모델의 근본적인 구분이다**
  (5장, p.91, 각주 1).[^evans2003]

## 값 객체가 담을 수 있는 것

- 값 객체 쪽의 문제 서술도 대가의 계산이다 (5장, p.98):[^evans2003]

> Tracking the identity of ENTITIES is essential, but attaching identity to other objects can
> hurt system performance, add analytical work, and muddle the model by making all objects
> look the same.
>
> Software design is a constant battle with complexity. We must make distinctions so that
> special handling is applied only where necessary.

- **그리고 "정체성의 부재"로 규정하는 것을 저자가 거부한다** (5장, p.98):[^evans2003]

> However, if we think of this category of object as just the absence of identity, we haven't
> added much to our toolbox or vocabulary. In fact, these objects have characteristics of
> their own and their own significance to the model. *These are the objects that describe
> things.*

  - **이 거부가 이 페이지의 구조를 정한다.** 값 객체는 엔티티가 아닌 나머지가 아니라
    **서술하는 것**이라는 적극적 범주다.
- 흔한 예가 기본 라이브러리에 이미 있다 — **색은 많은 현대 개발 시스템의 기본 라이브러리에
  제공되는 값 객체의 예다. 문자열과 수도 그렇다. (어느 "4"를 갖고 있는지, 어느 "Q"인지는
  신경 쓰지 않는다.)** (5장, p.98).[^evans2003]
- **그러나 단순할 필요는 없다** — 색 혼합 프로그램은 **향상된 색 객체들이 결합해 다른 색을
  만들어 내는 풍부한 모델을 가질 수 있고, 이 색들은 새 결과 값 객체를 이끌어 내려고 협력하는
  복잡한 알고리즘을 가질 수 있다** (5장, p.98).[^evans2003] 위
  [값 객체에도 행동이 있을 수 있다](#값-객체에도-행동이-있을-수-있다)가 옮긴 화폐 예제와
  같은 주장이다.
- **값 객체는 다른 객체의 조립일 수 있다** — 주택 도면 소프트웨어에서 창 양식(window style)
  객체를 만들어 높이·너비와 함께 창(window) 객체에 넣고, 그 속성들이 어떻게 바뀌고 결합될 수
  있는지를 다스리는 규칙까지 담을 수 있다. **이 창들은 다른 값 객체들로 이루어진 복잡한 값
  객체다. 그것들은 다시 벽 객체 같은 도면의 더 큰 요소에 포함될 것이다**
  (5장, p.98).[^evans2003]
- **값 객체는 엔티티를 참조할 수도 있다** — 온라인 지도 서비스에 샌프란시스코에서 로스앤젤레스로
  가는 경치 좋은 경로를 물으면 두 도시를 태평양 연안 고속도로로 잇는 `Route` 객체가 나온다.
  **그 `Route` 객체는 그것이 참조하는 세 객체(두 도시와 고속도로)가 모두 엔티티인데도
  값이다** (5장, pp.98–99).[^evans2003]
- 쓰임의 특징 셋이 이어진다 — **값 객체는 객체 사이의 메시지에서 매개변수로 자주 넘겨진다.
  그것들은 흔히 일시적이어서 어떤 연산을 위해 만들어졌다가 버려진다. 값 객체는 엔티티(그리고
  다른 값들)의 속성으로 쓰인다. 사람은 정체성을 가진 엔티티로 모델링될 수 있지만 그 사람의
  이름은 값이다** (5장, p.99).[^evans2003]
- 처방 문단이다 (5장, p.99):[^evans2003]

> When you care only about the attributes of an element of the model, classify it as a VALUE
> OBJECT. Make it express the meaning of the attributes it conveys and give it related
> functionality. Treat the VALUE OBJECT as immutable. Don't give it any identity and avoid the
> design complexities necessary to maintain ENTITIES.

- **그리고 속성 묶음에 조항이 하나 더 붙는다** (5장, p.99):[^evans2003]

> The attributes that make up a VALUE OBJECT should form a conceptual whole.

  - 예가 주소다 — **거리·도시·우편번호가 `Person` 객체의 별개 속성이어서는 안 된다. 그것들은
    하나의 온전한 주소의 일부이고, 그렇게 하면 `Person`은 더 단순해지고 값 객체는 더 응집된다**
    (5장, p.99).[^evans2003]
  - 저자가 이 조항의 출처를 각주로 밝힌다 — **Ward Cunningham의 WHOLE VALUE 패턴**
    (5장, p.99, 각주 2).[^evans2003]
  - **이 조항이 이 페이지의 파이썬 쪽 서술과 맞물린다.** 위
    [값 객체 — dataclass가 잘 맞는 이유](#값-객체--dataclass가-잘-맞는-이유)가 세 재료를
    고르는 문제를 다루는데, **무엇을 한 값 객체에 담을 것인가**는 재료가 아니라 이 조항이
    정한다. 같은 진단을 리팩터링 쪽에서는 기본형 집착과 데이터 뭉치라는 냄새 이름으로 부른다
    ([코드 냄새](../concepts/code-smells.md)).

## 두 패턴의 설계는 어디에 있는가

이 페이지는 **분류**에 답한다. 분류가 끝난 뒤의 설계는 원전이 절을 따로 두어 다루고, 이 KB도
페이지를 갈라 두었다.

- [엔티티의 정체성 설계](entity-identity-design.md) — 엔티티를 깎아 두는 처방, 정체성과 엮인
  속성만 남기는 기준, 식별자의 네 출처와 각각의 실패 양상.
- [값 객체 설계](value-object-design.md) — 복사와 공유 중 무엇을 고르는가, 공유의 조건인
  불변성, 가변을 허용하는 네 요인, 그리고 값 객체가 열어 주는 저장 조율.
- [도메인 연관](domain-associations.md) — 두 종류를 잇는 선을 제약하는 법. 값 객체 사이의
  양방향 연관이 성립하지 않는다는 것이 이 분류를 되짚는 신호가 된다.

## 규칙도 값 객체가 된다

같은 원전이 9장에서 이 두 범주의 한계를 스스로 지적하고, 값 객체 쪽을 넓혀 그 한계를 메운다.

- 한계의 진술 (9장, p.225):[^evans2003]

> Business rules often do not fit the responsibility of any of the obvious ENTITIES or VALUE
> OBJECTS, and their variety and combinations can overwhelm the basic meaning of the domain
> object. But moving the rules out of the domain layer is even worse, since the domain code no
> longer expresses the model.

- 그 규칙을 담을 자리로 저자가 여는 것이 값 객체다 — **그것들은 별도의 값 객체로 분리해 낼 수
  있는 작은 진리 검사다. 이 새 객체는 다른 객체를 평가해 그 객체에 대해 술어가 참인지 볼 수
  있다** (9장, p.225).[^evans2003] 처방 문단이 그 지위를 못 박는다 (9장, p.226):[^evans2003]

> Create explicit predicate-like VALUE OBJECTS for specialized purposes. A SPECIFICATION is a
> predicate that determines if an object does or does not satisfy some criteria.

  - **위 원 정의의 "무엇인지만 신경 쓰고 어느 것인지는 신경 쓰지 않는다"가 규칙 객체에도 그대로
    걸린다.** 연체 판정 명세 둘이 같은 유예 기간과 같은 평가 날짜를 가졌다면 그 둘은 구별될
    이유가 없다. 실제로 저자는 그 명세를 만들어 쓰고 버리는 것으로 다루며, 평가 날짜를 객체
    안에 박아 넣은 것을 단순화라고 부른다 (9장, p.226).[^evans2003]
- 규칙에 필요한 재료는 팩토리가 대 준다 — **팩토리가 고객의 계정이나 회사 정책 데이터베이스
  같은 다른 출처의 정보를 써서 명세를 구성할 수 있다. `Invoice`에서 이 출처들로 직접 접근하게
  하면 지불 요청이라는 `Invoice`의 기본 책임과 무관한 방식으로 객체들을 결합시킬 것이다** (9장,
  p.226).[^evans2003] 전문은 [명세 패턴](specification-pattern.md)에 있다.

## 이 구분이 연산의 타입을 정한다

원전 10장은 이 구분을 연산 설계의 판정 기준으로 쓴다. 인자와 반환 타입을 구현자와 같게 두는
연산의 닫힘(CLOSURE OF OPERATIONS)이 어디에 적용되는가를 정체성 유무가 가른다.

- 적용 대상이 먼저 좁혀진다 — **이 패턴은 값 객체의 연산에 가장 자주 적용된다** (10장,
  p.269).[^evans2003]
- 엔티티가 빠지는 근거가 정체성에서 곧장 나온다 — **엔티티의 생애 주기는 도메인에서 의미를
  가지므로, 질문에 답하려고 그냥 새것을 불러낼 수는 없다** (10장, p.269).[^evans2003]
  - **위 [구분의 기준은 정체성이다](#구분의-기준은-정체성이다)가 실무 규칙 하나를 낳는
    자리다.** 값 객체는 계산이 필요할 때마다 만들어 쓰고 버릴 수 있으니 연산의 결과가 될 수
    있다. 엔티티는 만들어 내는 일 자체가 도메인 사건이라 결과 자리에 놓기 어렵다.
- 예외가 없는 것은 아니다 — `Employee` 객체에 그 상급자를 물으면 다른 `Employee`가 돌아온다.
  **그러나 일반적으로 엔티티는 계산의 결과가 될 법한 종류의 개념이 아니다. 그래서 대체로 이것은
  값 객체에서 찾을 기회다** (10장, p.269).[^evans2003]
- 같은 장이 값 객체를 복잡한 계산의 거처로 지목하는 자리도 이 판정과 짝을 이룬다 — **가장 복잡한
  계산을 독립형 클래스로 인수분해하라. 어쩌면 더 연결된 클래스가 들고 있는 값 객체로
  모델링해서** (10장, p.267).[^evans2003] 그 처방은
  [독립형 클래스](standalone-classes.md)에 있고, 닫힘 자체는
  [연산의 닫힘](closure-of-operations.md)에 있다.
- 10장 끝의 통합 예제가 이 판정이 실제로 뒤집히는 장면을 보인다. 지분 분배를 맡은 `Share Pie`는
  처음에 `Loan` 애그리게이트 안에서 정체성이 국소적인 엔티티로 만들어졌다가, 값 객체로 바뀌면서
  `plus()`와 `minus()`가 닫힌 연산이 된다 (10장, pp.287–288).[^evans2003] 그 연쇄는
  [확립된 형식 체계](established-formalisms.md)에 있다.

## 이 구분이 생성의 모양도 정한다

원전 6장은 같은 구분을 생애 주기의 앞쪽에 적용한다. 무엇을 만들고 있느냐에 따라 생성
인터페이스의 모양이 달라진다.

- 엔티티 팩토리와 값 객체 팩토리가 두 자리에서 갈린다 — **값 객체는 불변이다; 산물이 최종
  형태로 완성되어 나온다. 그래서 팩토리 연산은 산물의 완전한 서술을 허용해야 한다. 엔티티
  팩토리는 유효한 애그리게이트(AGGREGATE)를 만드는 데 필요한 본질적 속성만 받는 경향이 있다.
  세부는 불변식(invariant)이 요구하지 않는다면 나중에 더할 수 있다** (6장,
  p.144).[^evans2003]
- 둘째 차이가 정체성 부여다. 값 객체에는 무관한 문제이고, 엔티티에서는 식별자를 프로그램이
  부여하는지 바깥에서 공급하는지가 인터페이스를 정한다 — **프로그램이 식별자를 부여할 때는
  팩토리가 그것을 통제하기 좋은 자리다** (6장, p.144).[^evans2003] 전문은
  [팩토리 패턴](factories-pattern.md)에 있다.
- **그리고 이 구분이 편의 기능 하나를 불필요하게 만든다.** 리포지터리에 "찾거나 만들기"
  기능을 두려는 욕구를 저자가 기각하는 근거가 이 구분이다 — **쓸모 있어 보이는 경우의 많은
  수가 엔티티와 값 객체를 구분하면 사라진다. 값 객체를 원하는 클라이언트는 곧장 팩토리로 가서
  새것을 요청하면 된다** (6장, pp.158–159).[^evans2003]
  - 그 뒤에 더 강한 이유가 붙는다 — **보통 새 객체와 기존 객체의 구분은 도메인에서 중요하고,
    둘을 투명하게 합치는 프레임워크는 실제로 상황을 흐려 놓을 것이다** (6장,
    p.159).[^evans2003] 그 판정의 자리는
    [저장된 객체의 재구성](reconstituting-stored-objects.md)이다.

## 이어지는 페이지

- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 객체들이 사는 층
- [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md) — "무엇인지"와
  "어느 것인지"의 구분이 이름 짓기 물음과 만나는 자리
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 값 객체의 불변성이 봉사하는 조항
- [엔티티의 정체성 설계](entity-identity-design.md) — 엔티티로 분류한 뒤의 설계
- [값 객체 설계](value-object-design.md) — 값 객체로 분류한 뒤의 설계
- [도메인 연관](domain-associations.md) — 두 종류를 잇는 선을 제약하는 법
- [연산의 닫힘](closure-of-operations.md) — 이 구분이 연산의 타입 선택으로 이어지는 자리
- [팩토리 패턴](factories-pattern.md) — 이 구분이 생성 인터페이스의 모양으로 이어지는 자리
- [저장된 객체의 재구성](reconstituting-stored-objects.md) — "새것인가 옛것인가"가 도메인의 물음이 되는 자리
- [독립형 클래스](standalone-classes.md) — 복잡한 계산을 값 객체로 옮기라는 처방
- [확립된 형식 체계](established-formalisms.md) — 엔티티가 값 객체로 바뀌며 연산이 닫히는 실물
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
    9장 "Making Implicit Concepts Explicit" §SPECIFICATION(pp.225–226) ·
    10장 §SIDE-EFFECT-FREE FUNCTIONS(p.251) · 10장 §STANDALONE CLASSES(p.267) ·
    §CLOSURE OF OPERATIONS(p.269) · 예제 "Integrating the Patterns: Shares Math"
    (pp.287–288) · 6장 "The Life Cycle of a Domain Object"
    §"ENTITY FACTORIES Versus VALUE OBJECT FACTORIES"(p.144)와
    §"The Relationship with FACTORIES"의 "찾거나 만들기" 기각(pp.158–159).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. **5장 쪽에서는 두 패턴의 분류 논의만 든다** — 분류 뒤의
    설계 지침(§"Modeling ENTITIES" pp.93–94 · §"Designing the Identity Operation" pp.94–96 ·
    §"Designing VALUE OBJECTS" pp.99–101과 예제 p.102)은 이 페이지의 물음(둘이 "같다"는 것이
    무슨 뜻인가) 밖이라 [엔티티의 정체성 설계](entity-identity-design.md)와
    [값 객체 설계](value-object-design.md)에 있다. 5장 첫머리의 임대인 소송 일화(p.89)와
    아이의 마커 일화(p.97)는 패턴을 여는 예화라 옮기지 않았고, Figure 5.5·5.6은 이미지다.
    이 소스에서 온 코드 펜스는 이 페이지에 없다.

[^ramalho2022]: Ramalho 2022, 5장 "Data Class Builders"(§"Mutable instances" p.168 ·
    §"Class statement syntax" p.168 · §"Classic Named Tuples" pp.169–172 ·
    §"More About @dataclass" pp.179–180과 그 표 5-2 p.179 · §"Further Reading" p.196).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 이 소스에서 온 코드 펜스는
    이 페이지에 없다 — 전문은 [데이터 클래스 빌더](../concepts/data-class-builders.md)에 있다.

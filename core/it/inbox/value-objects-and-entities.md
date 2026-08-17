---
type: concept
title: 값 객체와 엔티티
description: 도메인 객체를 정체성 유무로 가르는 구분과 그 구분이 파이썬 코드에서 갖는 모양 — 데이터는 있으나 정체성이 없는 것을 값 객체로 두는 규정과 frozen dataclass·NamedTuple·namedtuple이 공짜로 주는 값 동등성, 값 객체에도 연산이 있을 수 있다는 화폐 예제, 오래 사는 정체성을 갖는 엔티티와 그 정체성 동등성, __eq__와 __hash__를 어느 쪽에 어떻게 다는가의 규칙과 둘을 따로 건드리지 말라는 경고, 그리고 원시 타입을 NewType으로 감싸는 것에 대한 저자 자신의 기각
generated: { by: "claude-opus-5", at: "2026-08-17T23:30:00Z" }
status: draft
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
---

# 값 객체와 엔티티

- [구분의 기준은 정체성이다](#구분의-기준은-정체성이다)
- [값 객체 — dataclass가 잘 맞는 이유](#값-객체--dataclass가-잘-맞는-이유)
- [값 객체에도 행동이 있을 수 있다](#값-객체에도-행동이-있을-수-있다)
- [엔티티 — 값이 바뀌어도 같은 것](#엔티티--값이-바뀌어도-같은-것)
- [동등성과 해시를 어디에 어떻게 다는가](#동등성과-해시를-어디에-어떻게-다는가)
- [원시 타입 감싸기에 대한 저자의 기각](#원시-타입-감싸기에-대한-저자의-기각)
- [이벤트도 값 객체다](#이벤트도-값-객체다)
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

## 값 객체에도 행동이 있을 수 있다

- 흔한 오해를 저자들이 미리 막는다 — **그렇지만 우리는 값 객체에 여전히 복잡한 행동을
  가질 수 있다. 사실 값에 대한 연산을 지원하는 것은 흔하다. 예컨대 수학 연산자가 그렇다**
  (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
- 화폐 예제가 그 실물이다 — 같은 통화의 `Money`끼리는 더하고 뺄 수 있고, 수로 곱할 수
  있으며, **다른 통화를 더하면 `ValueError`가 나고** `Money`끼리 곱하면 `TypeError`가
  난다 (1장 §"Dataclasses Are Great for Value Objects").[^percival2020]
  - 즉 값 객체는 "데이터 홀더"가 아니다. **정체성이 없다는 것과 행동이 없다는 것은 다른
    말이다.** 이 구분이 [도메인 모델 패턴](domain-model-pattern.md)의 "무엇이든 객체일
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
    ([의존성 주입과 부트스트랩](dependency-injection-and-bootstrap.md)의 "과잉 설계"
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

## 이어지는 페이지

- [도메인 모델 패턴](domain-model-pattern.md) — 이 객체들이 사는 층
- [애그리게이트와 일관성 경계](aggregates-and-consistency-boundaries.md) — 엔티티 중
  일부를 "공개" 진입점으로 올리는 셋째 구분
- [이벤트 주도 애플리케이션 구조](event-driven-application-structure.md) — 값 객체가
  이벤트·명령으로 쓰이는 자리
- [리포지터리 패턴](repository-pattern.md) — 이 객체들을 저장하고 되살리는 층
- [데이터 조직하기](organizing-data.md) — 같은 값·참조 구분을 리팩터링 카탈로그가
  *Change Reference to Value*와 그 역으로 부르는 자리
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^percival2020]: Percival & Gregory 2020, 1장 "Domain Modeling"(§"Dataclasses Are Great
    for Value Objects"·§"Value Objects and Entities", 곁글 "More Types for More Type
    Hints"·"Domain Modeling Recap") · 2장 §"The Repository in the Abstract" ·
    8장 §"Events Are Simple Dataclasses" · 9장 §"Why Have We Achieved?" ·
    10장 §"Commands and Events". **이 소스의 locator는 장 단위다** — 검증 절차와 근거는
    `it/archive/percival2020/_progress.yaml` 머리말이 정본이다. 코드 펜스는 원문에서
    조판용 번호 표지 이미지를 제거했고, 원문이 세 예제를 나눠 실은 것을 한 펜스로 이었다
    (임포트는 원문 그대로다 — 이 예제는 저자들이 임포트를 생략하지 않은 몇 안 되는
    목록 중 하나다).

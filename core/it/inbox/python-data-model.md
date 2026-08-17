---
type: concept
title: 파이썬 데이터 모델
description: 파이썬이 자기 자신을 프레임워크로 규정하는 층 — 특수 메서드(던더 메서드)가 언어의 기본 구조물에 대한 인터페이스이고, 그것을 구현하면 내 객체가 내장 타입처럼 굴게 된다는 주장과 그 증거(두 메서드로 시퀀스가 되는 예제), 특수 메서드를 부르는 것은 내가 아니라 인터프리터라는 규칙, 컬렉션 인터페이스가 특수 메서드로 지어져 있다는 구조, 그리고 len이 메서드가 아닌 이유
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬 데이터 모델

- [데이터 모델이라는 이름과 그 범위](#데이터-모델이라는-이름과-그-범위)
- [특수 메서드는 인터프리터가 부른다](#특수-메서드는-인터프리터가-부른다)
- [두 메서드가 사 오는 것](#두-메서드가-사-오는-것)
- [컬렉션 API — 특수 메서드로 지은 인터페이스 층](#컬렉션-api--특수-메서드로-지은-인터페이스-층)
- [len이 메서드가 아닌 이유](#len이-메서드가-아닌-이유)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **"파이썬답다"는 말이 가리키는 대상이 무엇이고, 내 클래스가 그것을 어떻게
얻는가.**

이 페이지는 요지 수준이다. 이 KB가 이 장을 들인 이유는 [데이터 클래스
빌더](data-class-builders.md)와 [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)
두 페이지가 딛고 서는 바닥이 여기이기 때문이다 — 저 둘이 말하는 것은 결국 특수 메서드를
누가 대신 써 주는가(빌더)와 어떤 특수 메서드 묶음을 인터페이스로 부를 것인가(프로토콜)다.

## 데이터 모델이라는 이름과 그 범위

- 규정 — **데이터 모델을 프레임워크로서의 파이썬에 대한 서술이라고 생각할 수 있다. 그것은
  언어 자체의 구성 요소들 — 시퀀스, 함수, 이터레이터, 코루틴, 클래스, 컨텍스트 매니저
  같은 것들 — 의 인터페이스를 형식화한다** (1장 도입).[^ramalho2022]
  - 프레임워크라는 비유가 실무적 귀결을 갖는다 — **프레임워크를 쓸 때 우리는 프레임워크가
    호출하는 메서드를 코딩하는 데 많은 시간을 쓴다. 파이썬 데이터 모델을 활용해 새 클래스를
    지을 때도 같은 일이 일어난다** (1장 도입).[^ramalho2022]
- 이름 — 특수 메서드(special method)는 앞뒤로 밑줄 둘이 붙는다. 그래서 던더 메서드(dunder
  method)라 부른다. **"던더"는 "앞뒤로 이중 밑줄(double underscore before and after)"의
  줄임이다** (1장 곁글 §"Magic and Dunder").[^ramalho2022]
  - 저자가 "매직 메서드(magic method)"라는 통칭을 명시적으로 기각한다 — **나는 특수
    메서드가 마법의 반대라고 믿는다. 파이썬과 루비는 완전히 문서화된 풍부한 메타객체
    프로토콜로 사용자에게 힘을 준다** (1장 곁글 §"Soapbox").[^ramalho2022] 대비 대상이
    Go다: Go의 배열·문자열·맵은 대괄호 접근을 지원하지만 **사용자가 정의한 새 컬렉션
    타입에 `[]` 표기가 동작하게 만들 방법이 없다**는 것이 저자의 진단이다.
  - 다만 언어 참조서가 다는 경고가 함께 인용된다 — **명시적으로 문서화된 용법을 따르지
    않는 `__*__` 이름의 어떤 사용도 예고 없이 깨질 수 있다** (1장 곁글 §"Magic and
    Dunder"에 인용된 The Python Language Reference).[^ramalho2022]

## 특수 메서드는 인터프리터가 부른다

- 조문 — **특수 메서드에 대해 가장 먼저 알아야 할 것은 그것이 당신이 아니라 파이썬
  인터프리터에 의해 호출되게 되어 있다는 점이다. 당신은 `my_object.__len__()`을 쓰지
  않는다. 당신은 `len(my_object)`를 쓰고, `my_object`가 사용자 정의 클래스의 인스턴스라면
  파이썬이 당신이 구현한 `__len__` 메서드를 호출한다** (1장 §"How Special Methods Are
  Used").[^ramalho2022]
  - 유일한 예외가 명시된다 — **사용자 코드가 직접 자주 호출하는 유일한 특수 메서드는
    `__init__`이며, 자신의 `__init__` 구현에서 상위 클래스의 초기화 메서드를 부를 때다**
    (1장 §"How Special Methods Are Used").[^ramalho2022]
  - 그래서 지침이 따라온다 — **특수 메서드를 호출해야 한다면 보통은 대응하는 내장 함수
    (`len`·`iter`·`str` 등)를 부르는 편이 낫다** (1장 §"How Special Methods Are
    Used").[^ramalho2022] 이유가 둘이다: 내장 함수는 다른 서비스도 함께 제공하고, 내장
    타입에 대해서는 더 빠르다.
- 호출이 대개 암묵적이라는 것이 이 층의 성격이다 — `for i in x:`는 `iter(x)` 호출을
  일으키고, 그것이 다시 `x.__iter__()`를 부르거나 없으면 `x.__getitem__()`을 쓴다
  (1장 §"How Special Methods Are Used").[^ramalho2022]

## 두 메서드가 사 오는 것

이 장의 중심 주장은 예제 하나가 떠받친다. `__len__`과 `__getitem__` **둘만** 구현한
클래스가 표준 시퀀스처럼 굴기 시작한다.

- 예제의 클래스는 카드 한 벌이고, 위임(composition)으로 실제 일은 내부 리스트가 한다
  (1장 §"A Pythonic Card Deck" 예제 1-1).[^ramalho2022]

  ```python
  import collections

  Card = collections.namedtuple('Card', ['rank', 'suit'])

  class FrenchDeck:
      ranks = [str(n) for n in range(2, 11)] + list('JQKA')
      suits = 'spades diamonds clubs hearts'.split()

      def __init__(self):
          self._cards = [Card(rank, suit) for suit in self.suits
                                          for rank in self.ranks]

      def __len__(self):
          return len(self._cards)

      def __getitem__(self, position):
          return self._cards[position]
  ```

- 두 메서드로 따라오는 것들 (1장 §"A Pythonic Card Deck"):[^ramalho2022] `len(deck)`,
  `deck[0]`·`deck[-1]` 색인, 슬라이싱(`deck[:3]`·`deck[12::13]`), `for card in deck`
  반복, `reversed(deck)`, `in` 연산자, `sorted(deck, key=...)`, 그리고 표준 라이브러리의
  `random.choice(deck)`.
  - 슬라이싱이 공짜인 이유가 위임이다 — **우리 `__getitem__`이 `self._cards`의 `[]`
    연산자에 위임하므로 우리 덱은 자동으로 슬라이싱을 지원한다** (1장 §"A Pythonic Card
    Deck").[^ramalho2022]
  - `in`이 동작하는 이유는 반복이 되기 때문이다 — **컬렉션에 `__contains__` 메서드가
    없으면 `in` 연산자는 순차 훑기를 한다** (1장 §"A Pythonic Card Deck").[^ramalho2022]
- 그래서 이 장이 뽑는 이득이 둘이다 (1장 §"A Pythonic Card Deck"):[^ramalho2022]
  - **당신 클래스의 사용자가 표준 연산에 대해 임의의 메서드 이름을 외울 필요가 없다
    ("항목 수를 어떻게 얻지? `.size()`인가 `.length()`인가 뭐지?").**
  - **풍부한 파이썬 표준 라이브러리의 이득을 보고 `random.choice` 함수처럼 바퀴를 다시
    발명하지 않기가 더 쉽다.**
- 맺음이 이 페이지의 조문이다 — **`FrenchDeck`이 `object` 클래스를 암묵적으로 상속하지만
  그 기능의 대부분은 상속된 것이 아니라 데이터 모델과 합성을 활용한 데서 온다**
  (1장 §"A Pythonic Card Deck").[^ramalho2022]
  - 이것이 [상속세](inheritance-tax.md)가 말하는 것의 언어 쪽 실물이다. 파이썬에서
    "표준 타입처럼 굴게 만들기"는 상속이 아니라 **규약 준수**로 얻어진다.

## 컬렉션 API — 특수 메서드로 지은 인터페이스 층

- `collections.abc`의 컬렉션 추상 기반 클래스들은 각각 특수 메서드 하나로 규정된다
  (1장 §"Collection API"):[^ramalho2022] `Iterable`은 `__iter__`로 반복을, `Sized`는
  `__len__`으로 `len` 내장 함수를, `Container`는 `__contains__`로 `in` 연산자를 받친다.
  파이썬 3.6이 더한 `Collection` 추상 기반 클래스가 이 셋을 묶는다.
  - 그리고 **상속이 요구되지 않는다** — **파이썬은 구상 클래스가 이 ABC들 중 어느 것도
    실제로 상속하도록 요구하지 않는다. `__len__`을 구현하는 어떤 클래스든 `Sized`
    인터페이스를 만족한다** (1장 §"Collection API").[^ramalho2022] 이 한 줄이
    [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)의 출발점이다.
  - `Collection`의 세 특화가 `Sequence`(내장 `list`·`str`의 인터페이스),
    `Mapping`(`dict` 등), `Set`(`set`·`frozenset`)이고, **`Sequence`만 `Reversible`이다.
    시퀀스는 내용의 임의 순서를 지원하지만 매핑과 집합은 그렇지 않기 때문이다**
    (1장 §"Collection API").[^ramalho2022]
- 특수 메서드의 규모 — **The Python Language Reference의 "Data Model" 장은 80개가 넘는
  특수 메서드 이름을 나열한다. 그 절반 이상이 산술·비트·비교 연산자를 구현한다**
  (1장 §"Overview of Special Methods").[^ramalho2022] 이 장의 표 둘이 그것을 범주별로
  정리한다 — 연산자를 뺀 쪽(문자열 표현·수 변환·컬렉션 흉내·반복·호출·컨텍스트 관리·
  인스턴스 생성과 소멸·속성 관리·속성 기술자·추상 기반 클래스·클래스 메타프로그래밍)과
  연산자 쪽(단항·풍부한 비교·산술·역산술·증강 대입·비트).

## len이 메서드가 아닌 이유

- 질문 자체가 이 장의 문제 제기다 — **파이썬 전에 다른 객체 지향 언어를 배웠다면
  `collection.len()` 대신 `len(collection)`을 쓰는 것이 이상해 보일 수 있다**
  (1장 도입).[^ramalho2022]
- 답 — **실용성이 순수성을 이긴다.** 내장 타입에 대해서는 메서드가 아예 호출되지 않는다.
  **CPython의 내장 객체에 대해서는 어떤 메서드도 호출되지 않는다: 길이는 그저 C 구조체의
  필드에서 읽힌다** (1장 §"Why len Is Not a Method").[^ramalho2022] 가변 크기 컬렉션이
  담는 `PyVarObject` 구조체의 `ob_size` 필드가 그것이다.
- 그래서 이것이 절충으로 규정된다 — **`len`은 `abs`와 마찬가지로 파이썬 데이터 모델의
  일부로 특별 대우를 받기 때문에 메서드로 호출되지 않는다. 그러나 특수 메서드 `__len__`
  덕분에 당신의 맞춤 객체에서도 `len`이 동작하게 만들 수 있다. 이것은 효율적인 내장 객체의
  필요와 언어의 일관성 사이의 공정한 타협이다** (1장 §"Why len Is Not a
  Method").[^ramalho2022]
- **이 절이 이 KB에 값을 갖는 이유**는 답 자체가 아니라 답의 모양이다. 언어 설계자가
  일관성을 깨는 특례를 두되 그 특례가 **사용자 코드에도 열려 있게** 만들었다 — 내장 타입은
  빠른 경로로 가고, 사용자 타입은 같은 문법으로 같은 결과를 얻는다. [복잡성을 아래로
  끌어내리기](pull-complexity-downwards.md)가 말하는 것과 같은 조작이다. #hypothesis
  저자가 그렇게 연결하지는 않았다.

## 이어지는 페이지

- [데이터 클래스 빌더](data-class-builders.md) — 이 특수 메서드들을 손으로 쓰지 않고
  생성시키는 세 도구
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 특수 메서드 묶음을
  "인터페이스"라 부르는 네 가지 방식
- [값 객체와 엔티티](value-objects-and-entities.md) — `__eq__`·`__hash__`를 도메인 객체
  종류별로 어떻게 다는가
- [상속세](inheritance-tax.md) — 상속이 아니라 규약으로 다형성을 얻는 쪽
- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — 인터페이스를 좁게 두는 잣대
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 1장 "The Python Data Model"(도입 · §"Magic and Dunder"
    곁글 · §"A Pythonic Card Deck" · §"How Special Methods Are Used" · §"Collection API" ·
    §"Overview of Special Methods" · §"Why len Is Not a Method" · §"Soapbox" 곁글).
    **이 소스의 locator는 장 + 절 제목이다** — 인쇄판 쪽 앵커가 없다. 검증 절차와 근거,
    그리고 **이 스냅샷이 Early Release 판이라는 사실**은
    `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. Figure 1-1(2차원 벡터
    덧셈)과 Figure 1-2(`collections.abc` UML 클래스 다이어그램)는 이미지로 조판돼 있어
    딸린 설명 산문과 본문 서술만 옮겼다. 코드 펜스는 예제 1-1 원문 그대로다.

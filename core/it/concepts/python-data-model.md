---
type: concept
title: 파이썬 데이터 모델
description: 파이썬이 자기 자신을 프레임워크로 규정하는 층 — 특수 메서드(던더 메서드)가 언어의 기본 구조물에 대한 인터페이스이고, 그것을 구현하면 내 객체가 내장 타입처럼 굴게 된다는 주장과 그 증거(두 메서드로 시퀀스가 되는 예제), 특수 메서드를 부르는 것은 내가 아니라 인터프리터라는 규칙, 컬렉션 인터페이스가 특수 메서드로 지어져 있다는 구조, len이 메서드가 아닌 이유, 그리고 호출 연산자도 같은 층을 거친다는 것 — 클래스를 부르면 __new__와 __init__이 돌고 __call__을 구현한 인스턴스는 함수처럼 굴게 된다
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬 데이터 모델

- [데이터 모델이라는 이름과 그 범위](#데이터-모델이라는-이름과-그-범위)
- [특수 메서드는 인터프리터가 부른다](#특수-메서드는-인터프리터가-부른다)
- [두 메서드가 사 오는 것](#두-메서드가-사-오는-것)
- [컬렉션 API — 특수 메서드로 지은 인터페이스 층](#컬렉션-api--특수-메서드로-지은-인터페이스-층)
- [len이 메서드가 아닌 이유](#len이-메서드가-아닌-이유)
- [부르는 것도 데이터 모델을 거친다](#부르는-것도-데이터-모델을-거친다)
- [문법마다 짝이 되는 프로토콜이 있다](#문법마다-짝이-되는-프로토콜이-있다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **"파이썬답다"는 말이 가리키는 대상이 무엇이고, 내 클래스가 그것을 어떻게
얻는가.**

이 페이지는 요지 수준이다. 이 KB가 이 장을 들인 이유는 [데이터 클래스
빌더](../concepts/data-class-builders.md)와 [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md)
두 페이지가 딛고 서는 바닥이 여기이기 때문이다 — 저 둘이 말하는 것은 결국 특수 메서드를
누가 대신 써 주는가(빌더)와 어떤 특수 메서드 묶음을 인터페이스로 부를 것인가(프로토콜)다.

## 데이터 모델이라는 이름과 그 범위

- 규정 — **데이터 모델을 프레임워크로서의 파이썬에 대한 서술이라고 생각할 수 있다. 그것은
  언어 자체의 구성 요소들 — 시퀀스, 함수, 이터레이터, 코루틴, 클래스, 컨텍스트 매니저
  같은 것들 — 의 인터페이스를 형식화한다** (1장 도입, p.3).[^ramalho2022]
  - 프레임워크라는 비유가 실무적 귀결을 갖는다 — **프레임워크를 쓸 때 우리는 프레임워크가
    호출하는 메서드를 코딩하는 데 많은 시간을 쓴다. 파이썬 데이터 모델을 활용해 새 클래스를
    지을 때도 같은 일이 일어난다** (1장 도입, p.3).[^ramalho2022]
- 이름 — 특수 메서드(special method)는 앞뒤로 밑줄 둘이 붙는다. 그래서 던더 메서드(dunder
  method)라 부른다. **"던더"는 "앞뒤로 이중 밑줄(double underscore before and after)"의
  줄임이다** (1장 곁글 §"Magic and Dunder", p.4).[^ramalho2022]
  - 저자가 "매직 메서드(magic method)"라는 통칭을 명시적으로 기각한다 — **나는 특수
    메서드가 마법의 반대라고 믿는다. 파이썬과 루비는 완전히 문서화된 풍부한 메타객체
    프로토콜로 사용자에게 힘을 준다** (1장 §"Soapbox" 곁글 §"Muggle Methods",
    p.19).[^ramalho2022] 대비 대상이 Go다: Go의 배열·문자열·맵은 대괄호 접근을 지원하지만
    **사용자가 정의한 새 컬렉션 타입에 `[]` 표기가 동작하게 만들 방법이 없다**는 것이 저자의
    진단이고, 한 걸음 더 나간다 — **더 나쁜 것은 Go에 반복 가능 인터페이스나 이터레이터
    객체라는 사용자 수준 개념이 없다는 점이다. 그래서 `for`/`range` 문법이 배열·문자열·맵을
    포함한 다섯 개의 "마법" 내장 타입을 지원하는 데 갇혀 있다** (같은 곁글, p.19).
  - 다만 언어 참조서가 다는 경고가 함께 인용된다 — **문맥을 불문하고, 명시적으로 문서화된
    용법을 따르지 않는 `__*__` 이름의 어떤 사용도 예고 없이 깨질 수 있다** (1장 곁글
    §"Magic and Dunder"에 인용된 The Python Language Reference, p.4).[^ramalho2022]

## 특수 메서드는 인터프리터가 부른다

- 조문 — **특수 메서드에 대해 가장 먼저 알아야 할 것은 그것이 당신이 아니라 파이썬
  인터프리터에 의해 호출되게 되어 있다는 점이다. 당신은 `my_object.__len__()`을 쓰지
  않는다. 당신은 `len(my_object)`를 쓰고, `my_object`가 사용자 정의 클래스의 인스턴스라면
  파이썬이 당신이 구현한 `__len__` 메서드를 호출한다** (1장 §"How Special Methods Are
  Used", p.8).[^ramalho2022]
  - 유일한 예외가 명시된다 — **사용자 코드가 직접 자주 호출하는 유일한 특수 메서드는
    `__init__`이며, 자신의 `__init__` 구현에서 상위 클래스의 초기화 메서드를 부를 때다**
    (1장 §"How Special Methods Are Used", p.9).[^ramalho2022]
  - 그래서 지침이 따라온다 — **특수 메서드를 호출해야 한다면 보통은 대응하는 내장 함수
    (`len`·`iter`·`str` 등)를 부르는 편이 낫다** (1장 §"How Special Methods Are
    Used", p.8).[^ramalho2022] 이유가 둘이다: 내장 함수는 다른 서비스도 함께 제공하고, 내장
    타입에 대해서는 더 빠르다.
- 호출이 대개 암묵적이라는 것이 이 층의 성격이다 — `for i in x:`는 `iter(x)` 호출을
  일으키고, 그것이 다시 `x.__iter__()`를 부르거나 없으면 `x.__getitem__()`을 쓴다
  (1장 §"How Special Methods Are Used", p.9).[^ramalho2022]

## 두 메서드가 사 오는 것

이 장의 중심 주장은 예제 하나가 떠받친다. `__len__`과 `__getitem__` **둘만** 구현한
클래스가 표준 시퀀스처럼 굴기 시작한다.

- 예제의 클래스는 카드 한 벌이고, 위임(composition)으로 실제 일은 내부 리스트가 한다
  (1장 §"A Pythonic Card Deck" 예제 1-1, p.5).[^ramalho2022]

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

- 두 메서드로 따라오는 것들 (1장 §"A Pythonic Card Deck", pp.5–8):[^ramalho2022] `len(deck)`,
  `deck[0]`·`deck[-1]` 색인, 슬라이싱(`deck[:3]`·`deck[12::13]`), `for card in deck`
  반복, `reversed(deck)`, `in` 연산자, `sorted(deck, key=...)`, 그리고 표준 라이브러리의
  `random.choice(deck)`.
  - 슬라이싱이 공짜인 이유가 위임이다 — **우리 `__getitem__`이 `self._cards`의 `[]`
    연산자에 위임하므로 우리 덱은 자동으로 슬라이싱을 지원한다** (1장 §"A Pythonic Card
    Deck", p.6).[^ramalho2022]
  - `in`이 동작하는 이유는 반복이 되기 때문이다 — **컬렉션에 `__contains__` 메서드가
    없으면 `in` 연산자는 순차 훑기를 한다** (1장 §"A Pythonic Card Deck", p.7).[^ramalho2022]
- 그래서 이 장이 뽑는 이득이 둘이다 (1장 §"A Pythonic Card Deck", p.6):[^ramalho2022]
  - **당신 클래스의 사용자가 표준 연산에 대해 임의의 메서드 이름을 외울 필요가 없다
    ("항목 수를 어떻게 얻지? `.size()`인가 `.length()`인가 뭐지?").**
  - **풍부한 파이썬 표준 라이브러리의 이득을 보고 `random.choice` 함수처럼 바퀴를 다시
    발명하지 않기가 더 쉽다.**
- 맺음이 이 페이지의 조문이다 — **`FrenchDeck`이 `object` 클래스를 암묵적으로 상속하지만
  그 기능의 대부분은 상속된 것이 아니라 데이터 모델과 합성을 활용한 데서 온다**
  (1장 §"A Pythonic Card Deck", p.8).[^ramalho2022]
  - 이것이 [상속세](../concepts/inheritance-tax.md)가 말하는 것의 언어 쪽 실물이다. 파이썬에서
    "표준 타입처럼 굴게 만들기"는 상속이 아니라 **규약 준수**로 얻어진다.

## 컬렉션 API — 특수 메서드로 지은 인터페이스 층

- `collections.abc`의 컬렉션 추상 기반 클래스들은 각각 특수 메서드 하나로 규정된다
  (1장 §"Collection API", pp.14–15):[^ramalho2022] `Iterable`은 `__iter__`로 반복을, `Sized`는
  `__len__`으로 `len` 내장 함수를, `Container`는 `__contains__`로 `in` 연산자를 받친다.
  파이썬 3.6이 더한 `Collection` 추상 기반 클래스가 이 셋을 묶는다.
  - 그리고 **상속이 요구되지 않는다** — **파이썬은 구상 클래스가 이 ABC들 중 어느 것도
    실제로 상속하도록 요구하지 않는다. `__len__`을 구현하는 어떤 클래스든 `Sized`
    인터페이스를 만족한다** (1장 §"Collection API", p.15).[^ramalho2022] 이 한 줄이
    [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md)의 출발점이다.
  - `Collection`의 세 특화가 `Sequence`(내장 `list`·`str`의 인터페이스),
    `Mapping`(`dict` 등), `Set`(`set`·`frozenset`)이고, **`Sequence`만 `Reversible`이다.
    시퀀스는 내용의 임의 순서를 지원하지만 매핑과 집합은 그렇지 않기 때문이다**
    (1장 §"Collection API", p.15).[^ramalho2022]
- 특수 메서드의 규모 — **The Python Language Reference의 "Data Model" 장은 80개가 넘는
  특수 메서드 이름을 나열한다. 그 절반 이상이 산술·비트·비교 연산자를 구현한다**
  (1장 §"Overview of Special Methods", p.15).[^ramalho2022] 이 장의 표 둘이 그것을 범주별로
  정리한다 — 연산자를 뺀 쪽(문자열 표현·수 변환·컬렉션 흉내·반복·호출·컨텍스트 관리·
  인스턴스 생성과 소멸·속성 관리·속성 기술자·추상 기반 클래스·클래스 메타프로그래밍)과
  연산자 쪽(단항·풍부한 비교·산술·역산술·증강 대입·비트).

## len이 메서드가 아닌 이유

- 질문 자체가 이 장의 문제 제기다 — **파이썬 전에 다른 객체 지향 언어를 배웠다면
  `collection.len()` 대신 `len(collection)`을 쓰는 것이 이상해 보일 수 있다**
  (1장 도입, p.3).[^ramalho2022]
- 답 — **실용성이 순수성을 이긴다.** 저자가 2013년에 핵심 개발자 Raymond Hettinger에게 이
  질문을 했고, **그 답의 열쇠가 "The Zen of Python"의 한 줄 "practicality beats purity"였다**
  (1장 §"Why len Is Not a Method", p.17).[^ramalho2022] 내장 타입에 대해서는 메서드가 아예
  호출되지 않는다 — **CPython의 내장 객체에 대해서는 어떤 메서드도 호출되지 않는다: 길이는
  그저 C 구조체의 필드에서 읽힌다** (1장 §"Why len Is Not a Method", p.17).[^ramalho2022]
  - 그 구조체가 무엇인지는 앞 절이 댄다 — **C로 쓰인 파이썬의 가변 크기 컬렉션은
    `PyVarObject`라는 구조체를 포함하며, 그것이 컬렉션의 항목 수를 담는 `ob_size` 필드를
    갖는다. 그래서 `my_object`가 그런 내장 타입 중 하나의 인스턴스라면
    `len(my_object)`는 `ob_size` 필드의 값을 가져오고, 이것은 메서드를 호출하는 것보다
    훨씬 빠르다** (1장 §"How Special Methods Are Used", p.8).[^ramalho2022]
- 그래서 이것이 절충으로 규정된다 — **`len`은 `abs`와 마찬가지로 파이썬 데이터 모델의
  일부로 특별 대우를 받기 때문에 메서드로 호출되지 않는다. 그러나 특수 메서드 `__len__`
  덕분에 당신의 맞춤 객체에서도 `len`이 동작하게 만들 수 있다. 이것은 효율적인 내장 객체의
  필요와 언어의 일관성 사이의 공정한 타협이다** (1장 §"Why len Is Not a
  Method", p.17).[^ramalho2022]
  - 저자가 같은 자리에서 "The Zen of Python"을 한 줄 더 인용해 그 특례의 성격을 못 박는다 —
    **"Special cases aren't special enough to break the rules."** 즉 이 특례는 규칙을
    깨는 것이 아니라 규칙 안에 난 빠른 길이다 (1장 §"Why len Is Not a
    Method", p.17).[^ramalho2022]
- **이 절이 이 KB에 값을 갖는 이유**는 답 자체가 아니라 답의 모양이다. 언어 설계자가
  일관성을 깨는 특례를 두되 그 특례가 **사용자 코드에도 열려 있게** 만들었다 — 내장 타입은
  빠른 경로로 가고, 사용자 타입은 같은 문법으로 같은 결과를 얻는다. [복잡성을 아래로
  끌어내리기](../concepts/pull-complexity-downwards.md)가 말하는 것과 같은 조작이다. #hypothesis
  저자가 그렇게 연결하지는 않았다.

## 부르는 것도 데이터 모델을 거친다

색인·반복·`len`과 나란히, **호출 연산자 `()`도 특수 메서드로 규정된다.** 7장이 그것을 다른
방향에서 보인다 — 호출 가능한 것의 목록을 세면서.

- **클래스를 부르는 것**이 그 첫째다 — **호출되면 클래스는 `__new__` 메서드를 돌려 인스턴스를
  만들고, 그다음 `__init__`으로 그것을 초기화하고, 마지막으로 인스턴스가 호출자에게
  반환된다. 파이썬에는 `new` 연산자가 없으므로 클래스를 부르는 것은 함수를 부르는 것과 같다**
  (7장 §"The Nine Flavors of Callable Objects", p.238).[^ramalho2022]
- **인스턴스를 부르는 것**이 그 둘째다 — **클래스가 `__call__` 메서드를 정의하면 그 인스턴스를
  함수처럼 부를 수 있다** (7장 §"The Nine Flavors of Callable Objects",
  p.238).[^ramalho2022] 요구 사항이 그것뿐이라는 것도 명시된다 — **파이썬 함수가 진짜 객체일
  뿐 아니라, 임의의 파이썬 객체도 함수처럼 굴게 만들 수 있다. 인스턴스 메서드 `__call__`을
  구현하는 것이 전부다** (7장 §"User-Defined Callable Types", p.239).[^ramalho2022]
- **이 절이 위 [두 메서드가 사 오는 것](#두-메서드가-사-오는-것)과 같은 구조라는 데 값이
  있다.** `__len__`과 `__getitem__`을 구현하면 내 객체가 시퀀스처럼 굴듯, `__call__`을
  구현하면 내 객체가 함수처럼 군다. 무엇이 "함수"인가를 판정하는 것도 상속이 아니라 특수
  메서드의 존재다.
- 판정 방법은 하나로 좁혀져 있다 — **파이썬에 존재하는 호출 가능한 타입의 다양성을 고려하면,
  어떤 객체가 호출 가능한지 판정하는 가장 안전한 방법은 `callable()` 내장을 쓰는 것이다**
  (7장 §"The Nine Flavors of Callable Objects", p.239).[^ramalho2022] 아홉 갈래의 전체
  목록과 각각의 성질은 [파이썬의 일급 함수](../concepts/first-class-functions-in-python.md)가 갖는다.

## 문법마다 짝이 되는 프로토콜이 있다

위 [특수 메서드는 인터프리터가 부른다](#특수-메서드는-인터프리터가-부른다)가 규칙을
세운다면, 같은 소스의 4부가 그 규칙을 문법 단위로 다시 말한다 — 문법 하나에 그것을
제어하는 프로토콜 하나가 짝지어져 있다는 것이다.

- `for`와 `with`가 나란히 놓인다 — **컨텍스트 매니저 객체는 `with` 문을 제어하기 위해
  존재한다. 이터레이터가 `for` 문을 제어하기 위해 존재하는 것과 똑같다** (18장 §"Context
  Managers and with Blocks", p.658).[^ramalho2022]
- `for` 쪽 — **파이썬이 어떤 객체 `x`를 순회해야 할 때마다, 자동으로 `iter(x)`를 부른다**
  (17장 §"Why Sequences Are Iterable: The iter Function", p.596).[^ramalho2022] 그리고
  이 페이지가 든 `__getitem__` 하나로 순회가 되는 예제의 근거가 그 함수의 둘째 단계다 —
  **`__iter__`가 없고 `__getitem__`이 있으면, `iter()`가 0부터 시작하는 색인으로 항목을
  가져오려 시도하는 이터레이터를 만든다** (같은 절, p.596).[^ramalho2022] 저자가 그것을
  **덕 타이핑의 극단적 형태**라 부른다 (같은 절, p.597).[^ramalho2022]
- `with` 쪽 — **`with`의 맨 위에서 파이썬이 컨텍스트 매니저 객체의 `__enter__` 메서드를
  부른다. `with` 블록이 완료되거나 어떤 이유로든 종료되면 파이썬이 컨텍스트 매니저 객체의
  `__exit__`를 부른다** (18장 §"Context Managers and with Blocks",
  p.658).[^ramalho2022]
- 비동기 문법에도 같은 대응이 반복된다 — `async with`는 `__aenter__`/`__aexit__`에,
  `async for`는 `__aiter__`/`__anext__`에 얹힌다 (21장 §"Asynchronous Context Managers"
  p.786 · §"Asynchronous Iteration and Asynchronous Iterables",
  p.811).[^ramalho2022] 각각의 정본은
  [컨텍스트 매니저 프로토콜](../concepts/context-manager-protocol.md)과
  [이터레이터 프로토콜과 제너레이터](../concepts/iterator-protocol-and-generators.md)에 있다.

## 이어지는 페이지

- [파이썬다운 객체 만들기](../concepts/building-pythonic-objects.md) — **이 요지가 하나의 클래스에서
  끝까지 밀린 자리.** 표현·대안 생성자·포맷·해시 가능성·비공개 속성을 실제로 구현하면
  어떤 모양이 되는가
- [시퀀스 프로토콜의 점진 구현](../concepts/implementing-the-sequence-protocol.md) — 여기의
  `FrenchDeck`이 얻은 것을 N차원 컬렉션에서 다시 짓는 자리, 그리고 프로토콜을 일부만
  구현해도 되는 이유
- [파이썬의 연산자 오버로딩](../concepts/operator-overloading-in-python.md) — 80개 넘는 특수 메서드 중
  절반 이상을 차지한다는 그 연산자 쪽
- [파이썬의 일급 함수](../concepts/first-class-functions-in-python.md) — 호출 가능한 것 아홉 갈래와
  `__call__`로 만드는 함수 같은 객체
- [데이터 클래스 빌더](../concepts/data-class-builders.md) — 이 특수 메서드들을 손으로 쓰지 않고
  생성시키는 세 도구
- [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md) — 특수 메서드 묶음을
  "인터페이스"라 부르는 네 가지 방식
- [값 객체와 엔티티](value-objects-and-entities.md) — `__eq__`·`__hash__`를 도메인 객체
  종류별로 어떻게 다는가
- [상속세](../concepts/inheritance-tax.md) — 상속이 아니라 규약으로 다형성을 얻는 쪽
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 인터페이스를 좁게 두는 잣대
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 여기의 `FrenchDeck`이 공짜로
  얻는 슬라이싱·반복·정렬이 실제로 무엇인가
- [딕셔너리와 집합](../concepts/dictionaries-and-sets.md) — `Mapping`과 `Set` 쪽의 같은 이야기
- [객체 참조와 가변성](../concepts/object-references-and-mutability.md) — `is`가 왜 데이터 모델 밖에
  있고 그래서 빠른가
- [이터레이터 프로토콜과 제너레이터](../concepts/iterator-protocol-and-generators.md) — `for`가 부르는
  것이 정확히 무엇인가
- [컨텍스트 매니저 프로토콜](../concepts/context-manager-protocol.md) — `with`가 부르는 것이 정확히
  무엇인가
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 1장 "The Python Data Model", pp.3–19(도입 pp.3–4 ·
    §"Magic and Dunder" 곁글 p.4 · §"A Pythonic Card Deck" pp.5–8 · §"How Special Methods
    Are Used" pp.8–9 · §"Collection API" pp.14–15 · §"Overview of Special Methods"
    pp.15–17 · §"Why len Is Not a Method" p.17 · §"Soapbox" 곁글 §"Muggle Methods"
    pp.19–20) · 7장 "Functions as First-Class Objects" §"The Nine Flavors of Callable
    Objects"(pp.237–239) · §"User-Defined Callable Types"(p.239). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그
    오프셋 실측과 판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    Figure 1-1(2차원 벡터 덧셈)과 Figure 1-2(`collections.abc` UML 클래스 다이어그램)는
    이미지로 조판돼 있어 딸린 설명 산문과 본문 서술만 옮겼다. 코드 펜스는 예제 1-1 원문
    그대로다.
    §"문법마다 짝이 되는 프로토콜이 있다"는 2026-08-18-10 런에서 같은 소스의 17장
    §"Why Sequences Are Iterable: The iter Function"(pp.596–597) · 18장 §"Context Managers
    and with Blocks"(p.658) · 21장 §"Asynchronous Context Managers"(p.786) ·
    §"Asynchronous Iteration and Asynchronous Iterables"(p.811)에서 합류했다.

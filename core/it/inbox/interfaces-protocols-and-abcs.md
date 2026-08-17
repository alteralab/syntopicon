---
type: concept
title: 인터페이스·프로토콜·ABC
description: 파이썬에서 인터페이스를 규정하는 네 가지 방식(덕 타이핑·구스 타이핑·정적 타이핑·정적 덕 타이핑)의 구분과 선택 — 프로토콜이라는 낱말의 두 뜻(암묵적 동적 프로토콜과 typing.Protocol), 인터프리터가 부분 구현까지 받아 주는 범위, 검사 대신 빨리 실패시키는 방어 코드, 추상 기반 클래스로 하는 런타임 검사와 가상 하위 클래스 등록, 단일 메서드로 최소화하는 정적 프로토콜의 설계 지침과 이름 규약, 그리고 언제 ABC이고 언제 Protocol인가
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 인터페이스·프로토콜·ABC

- [버전 조건](#버전-조건)
- [네 가지 접근 — 타이핑 지도](#네-가지-접근--타이핑-지도)
- [프로토콜이라는 낱말의 두 뜻](#프로토콜이라는-낱말의-두-뜻)
- [덕 타이핑 — 인터프리터가 어디까지 봐 주는가](#덕-타이핑--인터프리터가-어디까지-봐-주는가)
- [빨리 실패하기 — 검사 없는 방어](#빨리-실패하기--검사-없는-방어)
- [구스 타이핑 — ABC로 하는 런타임 검사](#구스-타이핑--abc로-하는-런타임-검사)
- [가상 하위 클래스와 구조적 타이핑](#가상-하위-클래스와-구조적-타이핑)
- [정적 프로토콜 — 최소 인터페이스](#정적-프로토콜--최소-인터페이스)
- [언제 ABC이고 언제 Protocol인가](#언제-abc이고-언제-protocol인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **"이 자리에 오는 객체는 이런 것이어야 한다"를 파이썬에서 몇 가지 방식으로
말할 수 있고, 각각이 무엇을 사고 무엇을 지불하는가.**

## 버전 조건

> **버전 조건**: 파이썬 3.8 이상. `typing.Protocol`(PEP 544)이 3.8에 들어오면서 네 번째
> 접근이 생겼다 — **3.8 미만에는 정적 덕 타이핑이 없다.** 아래 수 타입 관련 서술은 저자가
> 2021년 7월에 검토한 파이썬 3.9·Mypy 0.910 시점의 실측이다.

## 네 가지 접근 — 타이핑 지도

- 저자가 이 장의 뼈대로 그림 하나(Figure 13-1, Typing Map)를 세운다. 두 축이다
  (13장 §"The Typing Map" 그림 설명):[^ramalho2022]
  - **위쪽 절반은 파이썬 인터프리터만으로 하는 런타임 타입 검사 접근을 서술하고, 아래쪽은
    Mypy 같은 외부 정적 타입 검사기나 PyCharm 같은 IDE를 요구한다.**
  - **왼쪽 사분면들은 객체의 구조 — 즉 클래스나 상위 클래스의 이름과 무관하게 객체가
    제공하는 메서드 — 에 근거한 타이핑을 다루고, 오른쪽 사분면들은 객체가 명시적으로 이름
    붙은 타입을 갖는 것에 기댄다: 객체 클래스의 이름, 또는 그 상위 클래스의 이름.**
- 그래서 네 칸이 나온다 (13장 도입):[^ramalho2022]

  | 접근 | 언제부터 | 검사 시점 | 무엇에 근거하는가 |
  |---|---|---|---|
  | 덕 타이핑(duck typing) | 처음부터 | 런타임 | 구조 |
  | 구스 타이핑(goose typing) | 파이썬 2.6(ABC) | 런타임 | 이름 |
  | 정적 타이핑(static typing) | 파이썬 3.5(`typing`) | 정적 | 이름 |
  | 정적 덕 타이핑(static duck typing) | 파이썬 3.8(`typing.Protocol`) | 정적 | 구조 |

  - **구스 타이핑**의 규정 — **추상 기반 클래스(ABC)가 파이썬 2.6부터 지원하는 접근으로,
    객체를 ABC에 대고 런타임에 검사하는 데 기댄다** (13장 도입).[^ramalho2022]
  - **정적 덕 타이핑**의 규정 — **Go 언어가 대중화한 접근으로, 파이썬 3.8에 새로 들어온
    `typing.Protocol`의 하위 클래스가 지원하며 역시 외부 타입 검사기가 강제한다**
    (13장 도입).[^ramalho2022]
- **네 가지를 서로 배제하는 것으로 읽지 말라**는 것이 이 장의 조문이다 — **이 네 타이핑
  접근은 상호 보완적이다: 각각 다른 장단점을 갖는다. 그중 어느 것도 무시하는 것은 말이 되지
  않는다** (13장 §"The Typing Map").[^ramalho2022]
  - 장 요약이 그것을 더 세게 적는다 — **현대 파이썬에는 인터페이스로 프로그래밍하는 네
    가지 보완적 방법이 있고 각각 다른 이점과 약점을 갖는다. 상당한 크기의 현대 파이썬
    코드베이스라면 각 타이핑 방식에 알맞은 사용 사례를 찾게 될 것이다. 이 접근들 중 어느
    하나를 거부하는 것은 파이썬 프로그래머로서 당신의 일을 필요 이상으로 힘들게 만든다**
    (13장 §"Chapter Summary").[^ramalho2022]
  - 그리고 균형추가 붙는다 — **그렇게 말했지만, 파이썬은 덕 타이핑만 지원하면서 널리 퍼진
    인기를 얻었다** (13장 §"Chapter Summary").[^ramalho2022]

## 프로토콜이라는 낱말의 두 뜻

**이 절이 이 장에서 가장 실무적인 구분이다.** 같은 낱말이 파이썬에서 두 가지를 가리킨다.

- **동적 프로토콜(dynamic protocol)** — **파이썬이 언제나 가지고 있던 비형식적 프로토콜들.
  동적 프로토콜은 암묵적이고, 관례로 정의되며, 문서에 서술된다. 파이썬의 가장 중요한 동적
  프로토콜들은 인터프리터 자신이 지원하며 The Python Language Reference의 "Data Model"
  장에 문서화돼 있다** (13장 §"Two kinds of protocols").[^ramalho2022]
- **정적 프로토콜(static protocol)** — **PEP 544가 정의하는 프로토콜로, 파이썬 3.8부터다.
  정적 프로토콜은 명시적 정의를 갖는다: `typing.Protocol` 하위 클래스다**
  (13장 §"Two kinds of protocols").[^ramalho2022]
- **핵심 차이 둘** (13장 §"Two kinds of protocols"):[^ramalho2022]
  - **객체는 동적 프로토콜의 일부만 구현하고도 여전히 유용할 수 있다. 그러나 정적 프로토콜을
    충족하려면 객체가 프로토콜 클래스에 선언된 모든 메서드를 제공해야 한다 — 당신 프로그램이
    그것들을 전부 필요로 하지 않더라도.**
  - **정적 프로토콜은 정적 타입 검사기가 검증할 수 있지만 동적 프로토콜은 그럴 수 없다.**
- **그리고 공통점이 결정적이다** — **두 종류의 프로토콜은 클래스가 어떤 프로토콜을 지원한다고
  이름으로, 즉 상속으로 선언할 필요가 결코 없다는 본질적 특성을 공유한다**
  (13장 §"Two kinds of protocols").[^ramalho2022]
  - 이것이 [파이썬 데이터 모델](python-data-model.md)의 "`__len__`을 구현하는 어떤
    클래스든 `Sized` 인터페이스를 만족한다"가 일반화된 자리다.
- 저자가 동적 프로토콜을 **비형식적 인터페이스(informal interface)**라 부르는 이유도
  같다 — **우리는 시퀀스가 `__len__`을 구현해 `len()`도 지원할 것으로 기대한다. `Vowels`에는
  `__len__` 메서드가 없지만 어떤 문맥에서는 여전히 시퀀스처럼 굴고, 우리 목적에는 그것으로
  충분할 수 있다. 그래서 나는 프로토콜이 "비형식적 인터페이스"라고 말하기를 좋아한다.
  스몰토크 — 그 용어를 쓴 첫 객체 지향 프로그래밍 환경 — 에서 프로토콜이 이해된 방식도
  그것이다** (13장 §"Two kinds of protocols").[^ramalho2022]

## 덕 타이핑 — 인터프리터가 어디까지 봐 주는가

- 인터프리터가 부분 구현을 적극적으로 메꾼다 — **파이썬 데이터 모델의 철학은 본질적인 동적
  프로토콜과 가능한 한 많이 협력하는 것이다. 시퀀스에 관해서라면 파이썬은 가장 단순한
  구현과도 일하려고 애쓴다** (13장 §"Python Digs Sequences").[^ramalho2022]
- 실물 — `__getitem__` **하나만** 구현한 클래스가 색인 접근·반복·`in` 연산자를 전부 얻는다.
  **`__iter__` 메서드가 없는데도 인스턴스가 반복 가능한 이유는 — 대비책으로 — 파이썬이
  `__getitem__` 메서드를 찾으면 0부터 시작하는 정수 색인으로 그 메서드를 불러 객체를
  반복하려 하기 때문이다** (13장 §"Python Digs Sequences").[^ramalho2022]
  - 요약 — **시퀀스 같은 자료 구조의 중요성을 생각해, 파이썬은 `__iter__`와 `__contains__`가
    없을 때 `__getitem__`을 불러 반복과 `in` 연산자가 동작하게 해낸다**
    (13장 §"Python Digs Sequences").[^ramalho2022]
  - **이 행동은 ABC에서 오지 않는다** — **내가 이 절에서 서술한 행동들은 인터프리터 자신에
    대부분 C로 구현돼 있다. 그것들은 `Sequence` ABC의 메서드에 의존하지 않는다**
    (13장 §"Python Digs Sequences").[^ramalho2022]
- 프로토콜은 **런타임에 붙일 수도 있다.** 몽키패칭으로 `__setitem__`을 클래스에 대입하면
  그 객체가 `random.shuffle`과 호환된다 (13장 §"Monkey-Patching: Implementing a Protocol
  at Runtime").[^ramalho2022]
  - 저자가 그 사실에서 뽑는 결론이 덕 타이핑의 정의다 — **`random.shuffle`은 인자의 클래스를
    신경 쓰지 않는다. 그것은 객체가 가변 시퀀스 프로토콜의 메서드들을 구현하기만 하면 된다.
    객체가 필요한 메서드를 가지고 "태어났는지" 나중에 어떻게든 획득했는지조차 중요하지
    않다** (13장 §"Monkey-Patching").[^ramalho2022]
  - 대가도 함께 적힌다 — **몽키패칭은 강력하지만, 실제로 패치를 하는 코드는 패치될 프로그램과
    아주 단단히 결합되며 흔히 비공개이고 문서화되지 않은 속성을 다룬다**
    (13장 §"Monkey-Patching").[^ramalho2022] 그리고 곁글에서 **두 라이브러리가 몽키패치를
    적용하면 서로의 발을 밟아 나중에 도는 쪽이 앞의 패치를 파괴할 수 있다**고 덧붙인다
    (13장 §"Soapbox").[^ramalho2022]
- 그리고 덕 타이핑에는 정적 검사가 표현하지 못하는 것이 있다. `namedtuple`의 `field_names`
  인자처럼 **"공백이나 쉼표로 구분된 식별자들의 문자열"이라고 말하는 타입 힌트를 쓸 방법이
  없다** (13장 §"Defensive programming and "fail fast"").[^ramalho2022] typeshed는
  `Union[str, Iterable[str]]`로 근사하는데, **그것은 되는 만큼은 괜찮지만 가능한 모든 문제를
  잡기에는 부족하다.**

## 빨리 실패하기 — 검사 없는 방어

이 절이 덕 타이핑을 안전하게 쓰는 실무 처방이다.

- 조문 — **동적 타입 언어에서 "빨리 실패하기(fail fast)"는 더 안전하고 유지보수하기 쉬운
  프로그램을 위한 훌륭한 조언이다. 빨리 실패한다는 것은 가능한 한 이른 시점에 런타임 오류를
  일으킨다는 뜻이다. 예컨대 함수 본문의 맨 처음에서 유효하지 않은 인자를 거부하는 것이다**
  (13장 §"Defensive programming and "fail fast"").[^ramalho2022]
- 대표 패턴 — **항목들의 시퀀스를 받아 내부적으로 리스트로 처리하는 코드를 쓸 때, 타입 검사로
  리스트 인자를 강제하지 마라. 대신 인자를 받아 즉시 그것으로 리스트를 만들어라**
  (13장 §"Defensive programming and "fail fast"").[^ramalho2022] `self._balls =
  list(iterable)` 한 줄이 그것이다.
  - 이득 — **그렇게 하면 `list()` 생성자가 메모리에 들어가는 어떤 반복 가능 객체든 처리하므로
    코드가 더 유연해진다. 인자가 반복 가능하지 않으면 그 호출은 객체가 초기화되는 바로 그
    지점에서 아주 명확한 `TypeError` 예외로 빨리 실패한다.**
  - 대비 — **클래스 생성자에서 유효하지 않은 인자를 잡지 않으면, 프로그램은 나중에 클래스의
    다른 메서드가 `self._balls`를 다뤄야 하는데 그것이 리스트가 아닐 때 터진다. 그러면 근본
    원인을 찾기가 더 어렵다.**
  - **예외 조건도 명시된다** — **데이터가 복사되면 안 될 때(너무 크거나, 함수가 설계상
    호출자를 위해 제자리에서 바꿔야 할 때 — `random.shuffle`처럼) `list()`를 부르는 것은
    나쁘다. 그런 경우에는 `isinstance(x, abc.MutableSequence)` 같은 런타임 검사가 갈 길이다.**
- 그리고 이 절이 타입 힌트의 한계를 못 박는다 — **타입 힌트가 어떤 문제는 더 일찍 잡을 수
  있지만 모든 문제를 잡지는 못한다. (…) 게다가 타입 힌트는 런타임에 강제되지 않는다. 빨리
  실패하기가 마지막 방어선이다** (13장 §"Defensive programming and "fail
  fast"").[^ramalho2022]
- 명시적 검사 없이 여러 타입을 다루는 코드도 이 범주다. `try`로 문자열인 척 해 보고
  `AttributeError`가 나면 이미 반복 가능한 것으로 간주하는 패턴이 예다 — **용서를 구하는
  것이 허락을 구하는 것보다 쉽다(EAFP)** (13장 §"Defensive programming and "fail
  fast"" 예제 13-5 주석).[^ramalho2022]

## 구스 타이핑 — ABC로 하는 런타임 검사

- 출발 — **파이썬에는 `interface` 키워드가 없다. 우리는 명시적 인터페이스를 정의하는 데
  추상 기반 클래스(ABC)를 쓴다** (13장 §"Goose typing").[^ramalho2022]
- 구스 타이핑이라는 이름은 Alex Martelli가 이 책을 위해 쓴 곁글 §"Waterfowl and ABCs"에서
  온다. 그 규정이 한 줄이다 — **구스 타이핑이 뜻하는 것은 이렇다: `isinstance(obj, cls)`가
  이제 괜찮다… `cls`가 추상 기반 클래스인 한, 다시 말해 `cls`의 메타클래스가 `abc.ABCMeta`인
  한** (13장 §"Waterfowl and ABCs").[^ramalho2022]
  - 문제 제기가 생물 분류학 비유다. 덕 타이핑은 **표현형 분류(phenetics)** — 관찰 가능한
    형질의 유사성 — 에 해당하는데, **평행 진화는 실제로는 무관하지만 비슷한 생태적 지위에서
    따로 진화한 종들 사이에 비슷한 형질을 만들어 낼 수 있다.** 프로그래밍의 예가
    `Artist.draw()`·`Gunslinger.draw()`·`Lottery.draw()`다 — **`draw`라는 이름의 메서드가
    존재한다는 사실만으로 두 객체가 어떤 식으로든 교환 가능하거나 추상적으로 동등하다고
    확신하기에는 턱없이 부족하다** (13장 §"Waterfowl and ABCs").[^ramalho2022]
  - 그래서 필요한 것이 **아는 프로그래머가 그 동등성이 어떤 수준에서 성립한다고 적극적으로
    단언하는 것**이라는 결론이 나온다.
- 요약하면 구스 타이핑이 요구하는 것은 둘이다 (13장 §"Goose typing"):[^ramalho2022]
  - **이전에 정의된 인터페이스를 구현하고 있음을 명시하기 위해 ABC에서 상속하기.**
  - **`isinstance`와 `issubclass`의 둘째 인자로 구상 클래스가 아니라 ABC를 써서 런타임
    타입 검사하기.**
- 상속이 단순한 메서드 구현 이상이라는 것이 이 방식의 값이다 — **ABC에서 상속하는 것은 요구된
  메서드를 구현하는 것 이상이다: 그것은 개발자의 명확한 의도 선언이기도 하다**
  (13장 §"Goose typing").[^ramalho2022]
- ABC를 직접 정의하는 서식이 이것이다. 추상 메서드와 구상 메서드가 한 클래스에 함께 있다
  (13장 §"Defining and Using an ABC" 예제 13-7).[^ramalho2022]

  ```python
  import abc

  class Tombola(abc.ABC):

      @abc.abstractmethod
      def load(self, iterable):
          """Add items from an iterable."""

      @abc.abstractmethod
      def pick(self):
          """Remove item at random, returning it.

          This method should raise `LookupError` when the instance is empty.
          """

      def loaded(self):
          """Return `True` if there's at least 1 item, `False` otherwise."""
          return bool(self.inspect())

      def inspect(self):
          """Return a sorted tuple with the items currently inside."""
          items = []
          while True:
              try:
                  items.append(self.pick())
              except LookupError:
                  break
          self.load(items)
          return tuple(items)
  ```

  - 읽는 법 (13장 §"Defining and Using an ABC"):[^ramalho2022] **ABC를 정의하려면
    `abc.ABC`를 상속한다.** 추상 메서드는 `@abstractmethod`로 표시하고 **본문은 흔히
    독스트링 말고는 비어 있다.** 그리고 규칙 하나 — **ABC의 구상 메서드는 ABC가 정의한
    인터페이스(즉 ABC의 다른 구상 또는 추상 메서드나 프로퍼티)에만 기대야 한다.**
  - **검사 시점이 임포트가 아니라 인스턴스화다** — **파이썬은 임포트 시점(모듈이 적재되고
    컴파일될 때)에 추상 메서드의 구현을 검사하지 않고, 우리가 실제로 인스턴스화하려 할 때
    런타임에만 검사한다** (13장 §"Subclassing an ABC").[^ramalho2022] 실패하면
    `TypeError: Can't instantiate abstract class …`가 난다.
  - 데코레이터 쌓는 순서에 규칙이 있다 — **`abstractmethod()`가 다른 메서드 기술자와
    조합될 때 그것은 가장 안쪽 데코레이터로 적용되어야 한다.** 즉
    **`@abstractmethod`와 `def` 문장 사이에 다른 데코레이터가 나타나서는 안 된다**
    (13장 §"ABC Syntax Details").[^ramalho2022] 그래서 추상 클래스 메서드는 `@classmethod`
    아래에 `@abc.abstractmethod`를 놓는다.
  - **상속의 대가가 계상된다** — 예제에서 `MutableSequence`를 상속하니 쓰지도 않을
    `__delitem__`과 `insert`를 구현해야 했고, 대신 `Sequence`에서 구상 메서드 다섯
    (`__contains__`·`__iter__`·`__reversed__`·`index`·`count`)과 `MutableSequence`에서
    여섯(`append`·`reverse`·`extend`·`pop`·`remove`·`__iadd__`)을 물려받았다
    (13장 §"Subclassing an ABC").[^ramalho2022]

## 가상 하위 클래스와 구조적 타이핑

- **`register`가 구스 타이핑의 결정적 기능이다** — **구스 타이핑의 본질적 특성 하나는 —
  그리고 그것이 물새 이름을 받을 만한 이유 하나는 — 클래스가 ABC를 상속하지 않더라도 그것을
  ABC의 가상 하위 클래스로 등록할 수 있다는 점이다. 그렇게 할 때 우리는 그 클래스가 ABC에
  정의된 인터페이스를 충실히 구현한다고 약속하고, 파이썬은 검사 없이 우리를 믿는다. 우리가
  거짓말하면 평소의 런타임 예외에 걸린다** (13장 §"A Virtual Subclass of an
  ABC").[^ramalho2022]
  - **등록된 클래스는 아무것도 물려받지 않는다** — **가상 하위 클래스는 등록된 ABC로부터
    상속하지 않고, 어느 시점에도 ABC 인터페이스 준수를 검사받지 않는다. 인스턴스화될 때조차
    그렇다. 또한 정적 타입 검사기는 현재 가상 하위 클래스를 다룰 수 없다**
    (13장 §"A Virtual Subclass of an ABC" §Warning).[^ramalho2022] `__mro__`에도 나타나지
    않는다.
  - 이 기능의 값을 Martelli가 짚는다 — **`register` 클래스 메서드는 최종 사용자 코드가 어떤
    클래스가 ABC의 "가상" 하위 클래스가 된다고 "선언"하게 해 준다. (…) 이것은 상속을 대부분의
    객체 지향 프로그래머가 실천하는 것보다 훨씬 더 조심스럽게 써야 할 것으로 만드는 경직성과
    강한 결합을 깨는 데 큰 몫을 한다** (13장 §"Waterfowl and ABCs").[^ramalho2022]
  - 표준 라이브러리가 실제로 그렇게 쓴다 — `collections.abc` 소스에서 `tuple`·`str`·
    `range`·`memoryview`가 `Sequence.register(…)`로 등록된다 (13장 §"Usage of register in
    Practice").[^ramalho2022]
- **등록조차 필요 없는 경우가 있다.** `__subclasshook__` 때문이다 — `Sized`의
  `__subclasshook__`은 **클래스 인자가 `__len__`이라는 이름의 속성을 갖는지 검사하고,
  가지면 그것을 `Sized`의 가상 하위 클래스로 간주한다** (13장 §"Structural typing with
  ABCs").[^ramalho2022] 그래서 `__len__`만 정의한 무관한 클래스가
  `issubclass(…, abc.Sized)`를 통과한다.
  - 이것이 **구조적 타이핑(structural typing)**의 정의를 부른다 — **구조적 타이핑은 객체의
    타입을 정하기 위해 그 공개 인터페이스의 구조를 보는 것이다: 객체가 타입에 정의된 메서드를
    구현하면 그 타입과 일관된다(consistent-with)** (13장 §"Structural typing with
    ABCs").[^ramalho2022]
  - **⚠ 그러나 내 ABC에 `__subclasshook__`을 넣는 것은 저자가 기각한다** — **좋은
    생각인가? 아마 아니다. 내가 파이썬 소스 코드에서 본 `__subclasshook__` 구현은 전부
    `Sized`처럼 특수 메서드 하나만 선언하는 ABC에 있고, 그저 그 특수 메서드 이름이 있는지
    검사할 뿐이다** (13장 §"Structural typing with ABCs").[^ramalho2022]
    - 반례가 정확하다 — **매핑은 `__len__`·`__getitem__`·`__iter__`를 구현하지만 정당하게
      `Sequence`의 하위 타입으로 간주되지 않는다. 정수 오프셋이나 슬라이스로 항목을 가져올 수
      없기 때문이다. 그것이 `abc.Sequence` 클래스가 `__subclasshook__`을 구현하지 않는
      이유다.**
    - 그리고 저자 자신의 ABC에 대해서는 더 단호하다 — **`load`·`pick`·`inspect`·`loaded`를
      구현하거나 상속하는 `Spam`이라는 이름의 어떤 클래스든 `Tombola`처럼 굴 것이라고 믿을
      준비가 나는 되어 있지 않다.**
- **`isinstance` 남용에 대한 경고도 이 절에 붙는다** — **ABC를 쓰더라도 `isinstance` 검사의
  과도한 사용은 코드 냄새 — 나쁜 객체 지향 설계의 증상 — 일 수 있음을 조심해야 한다.
  객체의 타입에 따라 다른 행동을 하는 `if/elif/elif` 사슬을 `isinstance` 검사로 만드는 것은
  보통 괜찮지 않다: 그런 것에는 다형성을 써야 한다** (13장 §"Goose typing").[^ramalho2022]
  - **정당한 경우도 명시된다** — **API 계약을 강제해야 한다면 ABC에 대고 `isinstance`
    검사를 하는 것은 괜찮다: "이봐, 나를 부르고 싶으면 이걸 구현해야 해." (…) 그것은 특히
    플러그인 아키텍처를 가진 시스템에서 유용하다. 프레임워크 밖에서는 덕 타이핑이 흔히 타입
    검사보다 더 단순하고 유연하다** (13장 §"Goose typing").[^ramalho2022]

## 정적 프로토콜 — 최소 인터페이스

- 무엇이 풀리는가 — 정적 프로토콜 이전에는 **`double`의 가능한 쓰임을 제한하지 않고 타입
  힌트를 다는 실용적인 방법이 없었다** (13장 §"The typed double
  function").[^ramalho2022]. **프로토콜을 지원해 요구된 연산을 제공하는 모든 타입의 이름을
  대는 것이 불가능하므로, 파이썬 3.8 이전에는 덕 타이핑을 타입 힌트로 서술할 수 없었다**
  (13장 §"The typed double function").[^ramalho2022]
- **설계 지침이 이 절의 핵심이고, Go에서 왔다** — **`Tombola` ABC는 `pick`과 `load` 두
  메서드를 명세한다. 우리는 이 두 메서드로 정적 프로토콜을 정의할 수도 있었지만, 나는 Go
  커뮤니티에서 단일 메서드 프로토콜이 정적 덕 타이핑을 더 유용하고 유연하게 만든다는 것을
  배웠다. Go 표준 라이브러리에는 `Reader` — `read` 메서드 하나만 요구하는 I/O 인터페이스 —
  같은 인터페이스가 여럿 있다. 시간이 지나 더 완전한 프로토콜이 필요하다는 것을 깨달으면,
  둘 이상의 프로토콜을 결합해 새 프로토콜을 정의할 수 있다** (13장 §"Designing a static
  protocol").[^ramalho2022]
  - 그 지침을 따른 결과가 이것이다. 프로토콜 정의가 세 줄이다.

    ```python
    from typing import Protocol, runtime_checkable, Any

    @runtime_checkable
    class RandomPicker(Protocol):
        def pick(self) -> Any: ...
    ```

  - 쓰는 쪽은 **이 프로토콜을 임포트할 필요조차 없다** — **정적 프로토콜을 구현하는 클래스를
    정의하는 데 그것을 임포트할 필요는 없다.** 구현 클래스는 **`RandomPicker`를 구현하지만
    그것을 상속하지 않는다. 이것이 작동 중인 정적 덕 타이핑이다**
    (13장 §"Designing a static protocol" 예제 13-19 주석).[^ramalho2022]
  - 확장은 상속이되 **문법에 단서가 둘** 붙는다 (13장 §"Extending a
    protocol"):[^ramalho2022] **파생 프로토콜도 런타임 검사 가능하게 하려면 데코레이터를
    다시 적용해야 한다 — 그 행동은 상속되지 않는다.** 그리고 **모든 프로토콜은 확장하는
    프로토콜에 더해 `typing.Protocol`을 기반 클래스 중 하나로 명시적으로 이름 대야 한다.
    이것은 파이썬에서 상속이 작동하는 방식과 다르다.**
- **런타임에도 쓸 수 있다** — **`typing.Protocol` 하위 클래스를 정의할 때 `@runtime_checkable`
  데코레이터를 써서 그 프로토콜이 런타임에 `isinstance`/`issubclass` 검사를 지원하게 만들 수
  있다. 이것이 동작하는 이유는 `typing.Protocol`이 ABC이고 따라서 위에서 본
  `__subclasshook__`을 지원하기 때문이다** (13장 §"Runtime checkable static
  protocols").[^ramalho2022]
  - **그러나 저자는 그 쓰임을 권하지 않는다** — 곁글 §"Duck typing is your friend"의 결론이
    그것이다: **아주 흔히 런타임에는 덕 타이핑이 타입 검사의 최선의 접근이다:
    `isinstance`나 `hasattr`를 부르는 대신, 객체에 필요한 연산을 그냥 시도하고 필요에 따라
    예외를 처리하라** (13장 §"Duck typing is your friend").[^ramalho2022] `complex(o)` 한
    줄이 `isinstance` 분기보다 낫다는 것이 그 예다.
- **이름 규약** (13장 §"Protocol naming conventions"):[^ramalho2022] typeshed 기여 지침이
  권하는 것이 셋이다 — **명확한 개념을 표현하는 프로토콜에는 평범한 이름을 쓴다(예:
  `Iterator`·`Container`). 호출 가능한 메서드를 제공하는 프로토콜에는 `SupportsX`를 쓴다
  (예: `SupportsInt`·`SupportsRead`). 읽기·쓰기 가능한 속성이나 게터·세터 메서드를 갖는
  프로토콜에는 `HasX`를 쓴다(예: `HasItems`·`HasFileno`).** 그리고 Go의 관례 하나가
  덧붙는다 — **단일 메서드 프로토콜에서 메서드 이름이 동사면 "-er"이나 "-or"을 붙여 명사로
  만든다. 예: `Formatter`·`Animator`·`Scanner`.**

## 언제 ABC이고 언제 Protocol인가

저자가 결정표를 두지는 않는다. 본문 여기저기의 판단을 모으면 이렇다.

- **먼저: 새 ABC를 만들지 마라.** 이것이 가장 강한 지침이고 두 사람이 각각 말한다.
  - Martelli — **그리고 프로덕션 코드에 맞춤 ABC(나 메타클래스)를 정의하지 마라… 그러고 싶은
    충동이 든다면, 그것은 십중팔구 방금 반짝이는 새 망치를 얻은 사람의 "모든 문제가 못으로
    보인다" 증후군의 경우일 것이다** (13장 §"Waterfowl and ABCs").[^ramalho2022]
    그가 이메일로 덧붙인 한 줄도 인용돼 있다 — **ABC는 프레임워크가 도입하는 아주 일반적인
    개념, 추상을 캡슐화하기 위한 것이다. (…) [독자들은] 새 ABC를 쓸 필요가 거의 없고, 기존의
    것을 올바르게 쓰기만 해도 심각한 오설계 위험 없이 이득의 99.9%를 얻는다.**
  - 저자 자신도 초판의 경고를 다시 싣는다 — **ABC는 기술자·메타클래스와 마찬가지로 프레임워크를
    짓기 위한 도구다. 따라서 소수의 파이썬 개발자만이 동료 프로그래머에게 부당한 제약과
    불필요한 일을 지우지 않고 ABC를 만들 수 있다** (13장 §"Defining and Using an
    ABC").[^ramalho2022]
  - 그래서 **먼저 기존 ABC를 쓴다** — **Martelli의 조언을 따라, 우리 것을 발명하려 들기 전에
    기존 ABC인 `collections.MutableSequence`를 활용할 것이다** (13장 §"Subclassing an
    ABC").[^ramalho2022]
- **ABC를 고를 자리** — 프레임워크의 확장점이고, 런타임에 계약을 강제해야 하며, 구현자에게
  구상 메서드를 물려주고 싶을 때다. 저자가 ABC를 만드는 정당화로 든 것이 정확히 그것이다 —
  **ABC를 만드는 것을 정당화하려면 그것을 프레임워크의 확장점으로 쓰는 문맥을 떠올려야
  한다** (13장 §"Defining and Using an ABC").[^ramalho2022] 그리고 ABC만이 가상 하위 클래스
  등록을 준다 — **내가 유지보수하지 않지만 인터페이스를 충족하는 클래스를 등록해야 할 때
  유용하다** (13장 §"A Virtual Subclass of an ABC").[^ramalho2022]
- **Protocol을 고를 자리** — 정적 타입 검사기가 검증해 주기를 원하고, 구현 쪽이 내 코드를
  임포트하지 않기를 바라며, 요구를 최소로 줄이고 싶을 때다. **정적 프로토콜의 최선의 쓰임은
  정적 타입 검사기와 함께다** (13장 §"Chapter Summary").[^ramalho2022] 그리고 위 설계
  지침이 여기에 붙는다 — **인터페이스를 정의할 때 최소주의 쪽으로 기울어라**
  (13장 §"Extending a protocol").[^ramalho2022]
- **둘 다 쓰지 않을 자리** — 런타임에 그냥 해 보고 예외를 처리하면 되는 경우다(위 §"Duck
  typing is your friend"). 그리고 애초에 인터페이스를 이름으로 붙들 필요가 없는 경우다.
- **수 타입은 특수한 예외 사례다.** 저자가 초판의 조언을 스스로 철회한다 — **나는
  Fluent Python 초판에서 `numbers` ABC를 쓰기를 권했지만 이제 그것은 더 이상 좋은 조언이
  아니다. 그 ABC들이 정적 타입 검사기에 인식되지 않기 때문이다**
  (13장 §"Runtime checkable static protocols").[^ramalho2022] 결론이 두 줄로 정리된다
  (13장 §"The numbers ABCs and numeric protocols"):[^ramalho2022]
  - **`numbers` ABC는 구스 타이핑에는 괜찮지만 정적 타이핑에는 부적합하다.**
  - **수치 정적 프로토콜 `SupportsComplex`·`SupportsFloat` 등은 정적 타이핑에는 잘
    동작하지만, 복소수가 얽히면 구스 타이핑에는 신뢰할 수 없다.**
- **이 페이지가 이 KB의 다른 축과 만나는 자리**: 단일 메서드 프로토콜 지침은
  [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)의 잣대를 **인터페이스 선언 자체에**
  적용한 것으로 읽힌다 — 기능은 구현이 갖고 선언은 최소로 줄인다. #hypothesis 저자가
  그렇게 연결하지는 않았고, 두 소스가 서로를 참조한 적도 없다.

## 이어지는 페이지

- [파이썬 데이터 모델](python-data-model.md) — 여기서 말하는 "동적 프로토콜"이 무엇으로
  이루어져 있는가
- [데이터 클래스 빌더](data-class-builders.md) — 같은 소스가 타입 힌트의 다른 쪽 끝
  (런타임에 효과가 없다는 사실)을 다루는 자리
- [의존성 역전 원칙](dependency-inversion-principle.md) — 포트를 ABC로 둘지 덕 타이핑으로
  둘지의 판단이 실제 애플리케이션에서 어떻게 내려졌는가
- [추상화 고르기](choosing-abstractions.md) — 무엇을 인터페이스로 삼을지 고르는 절차
- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — 인터페이스를 좁게 두는 잣대
- [인터페이스 문서화](interface-documentation.md) — 선언만으로 부족한 것을 무엇으로
  메우는가. `Tombola.pick`이 `LookupError`를 던진다는 계약이 독스트링에만 있는 자리
- [리포지터리 패턴](repository-pattern.md) — ABC로 규정된 포트의 실물
- [상속세](inheritance-tax.md) — ABC 상속이 무는 대가의 원리 쪽
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 13장 "Interfaces, Protocols, and ABCs"(도입 · §"The Typing
    Map" · §"Two kinds of protocols" · §"Programming ducks" 아래 §"Python Digs
    Sequences"·§"Monkey-Patching: Implementing a Protocol at Runtime"·§"Defensive
    programming and "fail fast"" · §"Goose typing" 아래 곁글 §"Waterfowl and
    ABCs"(Alex Martelli)·§"Subclassing an ABC"·§"ABCs in the Standard Library"·
    §"Defining and Using an ABC"·§"ABC Syntax Details"·§"A Virtual Subclass of an ABC"·
    §"Usage of register in Practice"·§"Structural typing with ABCs" · §"Static protocols"
    아래 §"The typed double function"·§"Runtime checkable static protocols"·곁글
    §"Duck typing is your friend"·§"Designing a static protocol"·§"Extending a protocol"·
    §"Protocol naming conventions"·§"The numbers ABCs and numeric protocols" ·
    §"Chapter Summary" · §"Soapbox" 곁글 · 각주 6). **이 소스의 locator는 장 + 절
    제목이다** — 인쇄판 쪽 앵커가 없다. 검증 절차와 근거, 그리고 **이 스냅샷이 Early
    Release 판이라는 사실**은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    Figure 13-1(Typing Map)·13-2·13-3·13-4(`collections.abc` UML)·13-5(Tombola UML)·
    13-6(예외 계층)·13-7·13-8은 전부 이미지로 조판돼 있어 그림 설명 캡션과 본문 서술만
    옮겼다 — 특히 타이핑 지도의 두 축은 Figure 13-1의 캡션에서 판독했다. 코드 펜스는
    예제 13-7과 예제 13-18 원문 그대로다.

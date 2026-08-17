---
type: concept
title: 객체 참조와 가변성
description: 파이썬에서 이름과 객체가 어떻게 갈리는가 — 변수가 상자가 아니라 라벨이라는 심상, 정체성·값·별칭의 구분과 ==가 아니라 is를 써야 하는 유일한 경우, 튜플의 불변성이 참조에만 걸린다는 사실, 복사가 기본적으로 얕다는 것과 그 대가, 매개변수 전달이 공유에 의한 호출이라는 규정, 가변 기본값과 받은 인자를 별칭하는 두 함정, 그리고 del이 객체가 아니라 참조를 지운다는 것
generated: { by: "claude-opus-5", at: "2026-08-18T05:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 객체 참조와 가변성

- [변수는 상자가 아니라 라벨이다](#변수는-상자가-아니라-라벨이다)
- [정체성·값·별칭](#정체성값별칭)
- [==와 is 중 무엇을 쓰는가](#와-is-중-무엇을-쓰는가)
- [튜플의 상대적 불변성](#튜플의-상대적-불변성)
- [복사는 기본적으로 얕다](#복사는-기본적으로-얕다)
- [매개변수 전달 — 공유에 의한 호출](#매개변수-전달--공유에-의한-호출)
- [함정 하나 — 가변 기본값](#함정-하나--가변-기본값)
- [함정 둘 — 받은 인자를 별칭하기](#함정-둘--받은-인자를-별칭하기)
- [del과 가비지 컬렉션](#del과-가비지-컬렉션)
- [불변 객체에 파이썬이 부리는 요령](#불변-객체에-파이썬이-부리는-요령)
- [같은 구분이 클로저에서 다시 나온다](#같은-구분이-클로저에서-다시-나온다)
- [이 페이지가 이 KB의 조항과 만나는 자리](#이-페이지가-이-kb의-조항과-만나는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파이썬에서 "이 값을 넘겼다"고 말할 때 실제로 무엇이 넘어가고, 그래서 어떤
버그가 가능해지는가.**

이 장은 저자 자신이 **"다소 건조한 장"**이라고 부르면서도 그 주제가 **"실제 파이썬
프로그램의 많은 미묘한 버그의 중심에 놓여 있다"**고 적는 자리다 (6장 도입,
p.201).[^ramalho2022] 이 KB에 이 장이 필요한 이유가 그것이다 — 숨은 상태와 별칭에 대한
이 KB의 조항들이 파이썬에서 무엇을 근거로 서는지가 여기 있다.

## 변수는 상자가 아니라 라벨이다

- 조문 — **"변수는 상자"라는 통상의 비유는 객체 지향 언어에서 참조 변수를 이해하는 데 실은
  방해가 된다. 파이썬 변수는 자바의 참조 변수와 같다. 더 나은 비유는 변수를 객체에 붙은
  이름표(labels)로 생각하는 것이다** (6장 §"Variables Are Not Boxes",
  p.202).[^ramalho2022]
  - 그 비유가 아니면 설명되지 않는 것이 `a = [1, 2, 3]` 뒤의 `b = a`다. `a.append(4)`가
    `b`에서 보인다. **`b = a` 문장은 상자 `a`의 내용을 상자 `b`로 복사하지 않는다. 그것은
    이미 `a`라는 이름표가 붙은 객체에 `b`라는 이름표를 하나 더 붙인다**
    (6장 §"Variables Are Not Boxes", p.203).[^ramalho2022]
- 낱말도 갈린다 — 대입(assign)이라는 동사가 서로 반대 방향으로 쓰이므로 저자는 **묶기(to
  bind)**를 대안으로 권한다. **파이썬의 대입문 `x = …`는 이름 `x`를 우변에서 만들어지거나
  참조된 객체에 묶는다. 그리고 이름이 묶이려면 그 객체가 먼저 존재해야 한다**
  (6장 §"Variables Are Not Boxes", p.203).[^ramalho2022]
  - 그래서 읽는 순서가 규정된다 — **파이썬에서 대입을 이해하려면 우변을 먼저 읽어라:
    거기서 객체가 만들어지거나 얻어진다. 그다음에 왼쪽의 변수가 그 객체에 묶인다, 마치
    이름표가 붙듯이. 상자는 그냥 잊어라** (6장 §"Variables Are Not Boxes" 곁상자,
    p.204).[^ramalho2022] 우변이 예외를 던지면 왼쪽 변수는 **아예 만들어지지 않는다.**

## 정체성·값·별칭

- 별칭(aliasing)의 정의 — 같은 객체에 묶인 두 변수다. **변수가 단지 이름표이므로, 객체가
  여러 이름표를 갖는 것을 막는 것은 없다** (6장 §"Identity, Equality, and Aliases",
  p.204).[^ramalho2022]
  - 대조가 되는 것은 **값은 같으나 정체성이 다른** 객체다. 저자의 예에서 `charles`와
    `lewis`는 별칭이고, 같은 내용으로 따로 만든 `alex`는 `alex == charles`가 참이면서
    `alex is not charles`도 참이다 (6장 §"Identity, Equality, and Aliases",
    p.205).[^ramalho2022]
- 정체성의 정의는 언어 참조서에서 그대로 인용된다 (6장 §"Identity, Equality, and
  Aliases", p.206):[^ramalho2022]
  > An object's identity never changes once it has been created; you may think of it as
  > the object's address in memory. The `is` operator compares the identity of two
  > objects; the `id()` function returns an integer representing its identity.
  - 다만 그 정수의 의미는 구현에 달렸다 — **CPython에서 `id()`는 객체의 메모리 주소를
    돌려주지만 다른 파이썬 인터프리터에서는 다른 것일 수 있다. 핵심은 그 ID가 유일한 정수
    이름표임이 보장되고 객체의 생애 동안 결코 바뀌지 않는다는 점이다**
    (6장 §"Identity, Equality, and Aliases", p.206).[^ramalho2022]

## ==와 is 중 무엇을 쓰는가

- 규정 — **`==` 연산자는 객체의 값(그것이 담은 데이터)을 비교하고, `is`는 그 정체성을
  비교한다** (6장 §"Choosing Between == and is", p.206).[^ramalho2022]
- **`is`를 쓸 자리는 사실상 하나다** — 싱글턴과의 비교다. **가장 흔한 경우는 변수가 `None`에
  묶여 있는지 검사하는 것이고**, 권장 표기가 `x is None`·`x is not None`이다
  (6장 §"Choosing Between == and is", p.206).[^ramalho2022] 그다음이 보초 객체(sentinel
  object)로, `END_OF_DATA = object()`처럼 만들어 `node is END_OF_DATA`로 검사한다.
- **⚠ 그리고 저자가 그 밖의 쓰임을 거의 전부 기각한다** — **보통 우리는 정체성보다 객체의
  동등성에 더 관심이 있다. `None` 검사가 `is` 연산자의 유일한 흔한 사용 사례다. 코드를
  리뷰하면서 보는 그 밖의 대부분의 쓰임은 틀린 것이다. 확신이 없으면 `==`를 써라. 그것이
  보통 당신이 원하는 것이고, `None`에도 동작한다 — 다만 그만큼 빠르지는 않다**
  (6장 §"Choosing Between == and is" §Warning, p.207).[^ramalho2022]
- 속도 차이의 근거는 오버로딩 가능성이다 — **`is`는 오버로드될 수 없으므로 파이썬이 특수
  메서드를 찾아 호출할 필요가 없고, `is`를 계산하는 것은 정수 ID 둘을 비교하는 것만큼
  단순하다. 반면 `a == b`는 `a.__eq__(b)`의 문법 설탕이다**
  (6장 §"Choosing Between == and is", p.207).[^ramalho2022] 이것이
  [파이썬 데이터 모델](python-data-model.md)이 말한 "특수 메서드를 부르는 것은
  인터프리터"의 반대 사례다 — `is`는 데이터 모델 밖에 있어서 빠르다.

## 튜플의 상대적 불변성

- 조문 — **튜플의 불변성은 실제로는 튜플 자료 구조의 물리적 내용(즉 그것이 담은 참조들)을
  가리키는 것이지, 참조된 객체들에까지 미치지 않는다** (6장 §"The Relative Immutability of
  Tuples", p.207).[^ramalho2022] 튜플에서 결코 바뀔 수 없는 것은 **그것이 담은 항목들의
  정체성**이다.
  - 실물 — `t1 = (1, 2, [30, 40])`에서 `t1[-1].append(99)`를 하면 `t1[-1]`의 `id`는 그대로인데
    `t1 == t2`가 참에서 거짓으로 바뀐다 (6장 예제 6-5, p.208).[^ramalho2022]
- 그 결과가 둘로 번진다 (6장 §"The Relative Immutability of Tuples",
  p.208):[^ramalho2022] `+=` 대입 수수께끼(2장)와 **일부 튜플이 해시 불가능하다**는 사실이다.
  - 값이 고정됐는지 확인하는 방법이 `hash`다 — **어떤 튜플(이나 어떤 객체든)이 고정된 값을
    갖는지 명시적으로 판정하려면 `hash` 내장 함수를 쓸 수 있다**
    (2장 §"Tuples as Immutable Lists", p.33).[^ramalho2022] `hash(o)`가 `TypeError`를
    던지면 고정이 아니다.
- 장 요약이 이것을 예외로 못 박는다 — **두 변수가 값이 같은 불변 객체를 참조하면 실무에서
  그것이 복사본인지 같은 객체를 가리키는 별칭인지는 거의 문제가 되지 않는다. 불변 객체의
  값이 바뀌지 않기 때문이다 — 예외 하나만 빼고. 그 예외가 튜플 같은 불변 컬렉션이다: 불변
  컬렉션이 가변 항목에 대한 참조를 담으면 그 가변 항목의 값이 바뀔 때 컬렉션의 값이 실제로
  바뀔 수 있다** (6장 §"Chapter Summary", p.223).[^ramalho2022]
  - `frozenset`은 이 문제를 겪지 않는다 — **해시 가능한 원소만 담을 수 있고, 해시 가능한
    객체의 값은 정의상 결코 바뀔 수 없기 때문이다** (같은 절, p.223).

## 복사는 기본적으로 얕다

- 규정 — 생성자(`list(l1)`)나 `[:]`로 만드는 것은 **얕은 복사(shallow copy)**다. **바깥
  컨테이너만 복제되고, 복사본은 원래 컨테이너가 담고 있던 바로 그 항목들에 대한 참조로
  채워진다. 이것은 메모리를 아끼며, 모든 항목이 불변이면 아무 문제도 일으키지 않는다.
  그러나 가변 항목이 있으면 불쾌한 놀람으로 이어질 수 있다**
  (6장 §"Copies Are Shallow by Default", p.209).[^ramalho2022]
- 깊은 복사는 `copy` 모듈이 준다 — `copy.copy`와 `copy.deepcopy`다. **`deepcopy` 함수는
  이미 복사한 객체를 기억해 순환 참조를 우아하게 처리한다**
  (6장 §"Deep and Shallow Copies of Arbitrary Objects", p.212).[^ramalho2022]
  - **⚠ 그러나 깊은 복사가 너무 깊을 수 있다** — **객체가 복사되어서는 안 되는 외부 자원이나
    싱글턴을 참조할 수 있다. `__copy__()`와 `__deepcopy__()` 특수 메서드를 구현해 둘 다의
    동작을 제어할 수 있다** (6장 §"Deep and Shallow Copies of Arbitrary Objects",
    p.213).[^ramalho2022]

## 매개변수 전달 — 공유에 의한 호출

- 조문 — **파이썬의 유일한 매개변수 전달 방식은 공유에 의한 호출(call by sharing)이다. (…)
  공유에 의한 호출이란 함수의 각 형식 매개변수가 인자에 있는 각 참조의 복사본을 얻는다는
  뜻이다. 다시 말해 함수 안의 매개변수는 실제 인자의 별칭이 된다**
  (6장 §"Function Parameters as References", p.213).[^ramalho2022]
- 그 귀결이 이 페이지의 핵심 사실이다 — **이 방식의 결과로, 함수는 매개변수로 넘겨진 어떤
  가변 객체든 바꿀 수 있지만, 그 객체들의 정체성은 바꿀 수 없다(즉 객체를 다른 것으로
  통째로 대치할 수 없다)** (6장 §"Function Parameters as References",
  p.213).[^ramalho2022]
  - 곁글이 흔한 설명을 바로잡는다 — **"매개변수는 값으로 전달되지만 그 값이 참조다"라는
    설명은 틀리지 않았으나 혼란을 부른다.** 옛 언어들의 흔한 방식이 값 호출(함수가 인자의
    복사본을 얻는다)과 참조 호출(함수가 인자에 대한 포인터를 얻는다)이기 때문이다. 저자는
    Michael L. Scott의 *Programming Language Pragmatics* 3판 §8.3.1을 읽고 **공유에 의한
    호출**이라는 용어를 채택했다고 적는다 (6장 §"Soapbox" 곁글 §"Parameter Passing: Call by
    Sharing", p.227).[^ramalho2022]

## 함정 하나 — 가변 기본값

**이 절이 이 KB의 "숨은 상태" 축과 직결되는 자리다.**

- 조문 — **기본값을 가진 선택적 매개변수는 파이썬 함수 정의의 훌륭한 기능으로, 우리 API가
  하위 호환을 유지하면서 진화하게 해 준다. 그러나 매개변수의 기본값으로 가변 객체를 쓰는
  것은 피해야 한다** (6장 §"Mutable Types as Parameter Defaults: Bad Idea",
  p.214).[^ramalho2022]
- **기제가 정확히 서술된다** — **각 기본값은 함수가 정의될 때, 즉 보통 모듈이 적재될 때
  평가되고, 그 기본값들은 함수 객체의 속성이 된다. 그래서 기본값이 가변 객체이고 그것을
  바꾸면, 그 변경은 그 함수의 앞으로의 모든 호출에 영향을 준다**
  (6장 §"Mutable Types as Parameter Defaults: Bad Idea", p.215).[^ramalho2022]
  - 증거가 함수 객체 자신에게 있다 — 저자의 `HauntedBus` 예제를 돌린 뒤
    `HauntedBus.__init__.__defaults__`를 보면 `(['Carrie', 'Dave'],)`가 들어 있고,
    `HauntedBus.__init__.__defaults__[0] is bus2.passengers`가 `True`다
    (6장 §"Mutable Types as Parameter Defaults: Bad Idea", p.216).[^ramalho2022]
    **상태가 인스턴스가 아니라 함수 객체에 얹혀 있다.**
  - 증상이 특히 고약한 이유는 **인자를 주고 만들면 정상 동작하기 때문이다** — **이상한 일은
    `HauntedBus`가 비어서 시작할 때만 일어난다. 그때 `self.passengers`가 `passengers`
    매개변수의 기본값에 대한 별칭이 되기 때문이다** (같은 절, p.216).
- 처방 — **가변 값을 받을 수 있는 매개변수의 기본값으로 `None`이 흔히 쓰이는 이유가 이
  문제다** (6장 §"Mutable Types as Parameter Defaults: Bad Idea", p.216).[^ramalho2022]
  `None`이면 새 빈 리스트를 만들고, 아니면 **인자의 복사본**을 묶는다.

## 함정 둘 — 받은 인자를 별칭하기

- 질문부터가 설계 판단이다 — **가변 매개변수를 받는 함수를 짤 때, 호출자가 넘긴 인자가
  바뀌기를 기대하는지 신중히 따져야 한다** (6장 §"Defensive Programming with Mutable
  Parameters", p.216).[^ramalho2022] 그리고 그 답은 문맥에 달렸다 — **그것은 정말로 함수를
  짜는 사람의 기대와 호출자의 기대를 맞추는 문제다** (같은 절, p.216).
- 실패의 이름이 붙어 있다 — 저자의 `TwilightBus`는 생성자가 받은 리스트를 그대로
  `self.passengers`에 묶어, 버스에서 승객을 내리면 원래 명단에서도 사라진다. **`TwilightBus`는
  인터페이스 설계의 모범 사례인 "최소 놀람의 원칙(Principle of least astonishment)"을
  위반한다** (6장 §"Defensive Programming with Mutable Parameters",
  p.217).[^ramalho2022]
- 고치는 법은 생성자에서 **복사본**을 만드는 것이고, 그 서식이 이 장의 대표 코드다
  (6장 §"Deep and Shallow Copies of Arbitrary Objects" 예제 6-8,
  p.211).[^ramalho2022]

  ```python
  class Bus:

      def __init__(self, passengers=None):
          if passengers is None:
              self.passengers = []
          else:
              self.passengers = list(passengers)

      def pick(self, name):
          self.passengers.append(name)

      def drop(self, name):
          self.passengers.remove(name)
  ```

  - 이 네 줄이 위 두 함정을 **동시에** 막는다 — `passengers=None`이 가변 기본값을 피하고,
    `list(passengers)`가 받은 인자의 별칭을 피한다.
  - 덤이 하나 붙는다 — **이 해법은 더 유연하다: 이제 `passengers` 매개변수에 넘기는 인자가
    튜플이든 집합이든 데이터베이스 결과든 어떤 반복 가능 객체여도 된다. `list` 생성자가
    어떤 반복 가능 객체든 받기 때문이다** (6장 §"Defensive Programming with Mutable
    Parameters", p.218).[^ramalho2022] 이것이
    [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md)의 "빨리 실패하기"가 같은
    한 줄로 얻는 이득과 같은 것이다 — 두 장이 서로를 가리킨다.
- **⚠ 조문으로 정리된 경고** — **메서드가 인자로 받은 객체를 변경하도록 명시적으로 의도된
  것이 아니라면, 그 인자 객체를 그냥 인스턴스 변수에 대입해 별칭을 만들기 전에 두 번
  생각해야 한다. 의심스러우면 복사본을 만들어라. 당신의 클라이언트가 더 행복해질 것이다.
  물론 복사가 공짜는 아니다: CPU와 메모리에 비용이 든다. 그러나 미묘한 버그를 일으키는
  API는 보통 조금 느리거나 자원을 더 쓰는 API보다 큰 문제다**
  (6장 §"Defensive Programming with Mutable Parameters" §Warning,
  p.218).[^ramalho2022]

## del과 가비지 컬렉션

- 오해 둘이 정정된다 (6장 §"del and Garbage Collection", p.219):[^ramalho2022]
  - **`del`은 함수가 아니라 문장이다.** `del x`라고 쓰지 `del(x)`라고 쓰지 않는다.
  - **`del`은 객체가 아니라 참조를 지운다. 삭제된 변수가 그 객체에 대한 마지막 참조였다면,
    파이썬의 가비지 컬렉터가 `del`의 간접적 결과로 객체를 메모리에서 버릴 수 있다.**
    변수를 다시 묶는 것(rebinding)도 같은 효과를 낼 수 있다.
- CPython의 기제 — **주 알고리즘은 참조 카운팅이다. 본질적으로 각 객체는 자기를 가리키는
  참조가 몇 개인지 센다. 그 refcount가 0이 되는 즉시 객체는 곧바로 파괴된다**
  (6장 §"del and Garbage Collection", p.220).[^ramalho2022] CPython 2.0이 순환 참조에
  걸린 객체 무리를 잡기 위해 세대별 가비지 컬렉션을 더했다.
  - 버전 조건: CPython 한정. **참조 카운팅에 기대지 않는 더 정교한 가비지 컬렉터를 가진
    다른 파이썬 구현에서는 객체에 대한 참조가 없어져도 `__del__` 메서드가 즉시 호출되지
    않을 수 있다** (같은 절, p.220).
  - 그 차이가 실무 조언으로 이어진다 — 곁글에서 저자가 `open(...).write(...)` 한 줄이
    CPython에서는 안전하지만 **Jython이나 IronPython에서는 안전하지 않다**고 적고,
    **모든 경우에 최선의 관행은 파일을 명시적으로 닫는 것이며 가장 믿을 만한 방법은
    `with` 문장**이라고 결론짓는다 (6장 §"Soapbox" 곁글 §"Object Destruction and Garbage
    Collection", p.226).[^ramalho2022]
- `__del__`에 대한 경고도 붙는다 — **`__del__` 특수 메서드가 있지만 그것이 인스턴스의
  처분을 일으키지 않으며 당신 코드가 불러서도 안 된다. (…) 자기 코드에 `__del__`을 구현할
  일은 드문데도 어떤 파이썬 프로그래머들은 아무 좋은 이유 없이 그것을 짜는 데 시간을
  쓴다** (6장 §"del and Garbage Collection", p.219).[^ramalho2022]

## 불변 객체에 파이썬이 부리는 요령

저자가 이 절을 **선택적**이라 표시하고 **"파이썬 사용자에게 그리 중요하지 않으며 다른 파이썬
구현이나 미래의 CPython에는 적용되지 않을 수 있는 세부"**라고 못 박는다
(6장 §"Tricks Python Plays with Immutables", p.221).[^ramalho2022] 그럼에도 옮기는 이유는
저자가 든 이유와 같다 — **사람들이 이 구석 사례에 걸려 넘어진 뒤 `is` 연산자를 잘못 쓰기
시작하는 것을 봤기 때문이다.**

- 튜플 `t`에 대해 `tuple(t)`와 `t[:]`는 **복사가 아니라 같은 객체에 대한 참조**를 돌려준다
  (6장 예제 6-17, p.221).[^ramalho2022] `str`·`bytes`·`frozenset`에서도 같고,
  `frozenset.copy()`도 그렇다.
- 문자열 리터럴 공유는 **인터닝(interning)**이라는 최적화 기법이다. **CPython은 작은 정수에도
  비슷한 기법을 쓴다. CPython이 모든 문자열이나 정수를 인터닝하는 것은 아니며, 그 기준은
  문서화되지 않은 구현 세부다** (6장 §"Tricks Python Plays with Immutables",
  p.222).[^ramalho2022]
  - **⚠ 그래서 조문이 붙는다** — **`str`이나 `int` 인터닝에 결코 기대지 마라! 문자열이나
    정수의 동등성 비교에는 언제나 `is` 대신 `==`를 써라. 인터닝은 파이썬 인터프리터 내부
    용도의 최적화다** (같은 절 §Warning, p.222).

## 같은 구분이 클로저에서 다시 나온다

이 페이지의 중심 구분 — **이름을 다시 묶는 것과 객체를 바꾸는 것은 다르다** — 이 9장에서
언어의 다른 자리에 그대로 재등장한다. 그쪽 전문은
[클로저와 데코레이터](../concepts/closures-and-decorators.md)가 갖고, 여기서는 대응만 남긴다.

- 클로저가 보관하는 것이 **값이 아니라 바인딩(binding)**이다 — **클로저는 함수가 정의될 때
  존재하는 자유 변수들의 바인딩을 유지하는 함수다** (9장 §"Closures", p.314).[^ramalho2022]
- 그래서 리스트를 담은 클로저는 잘 굴러가고 정수를 담은 클로저는 깨진다. 이유가 이 페이지의
  구분 그대로다 — 리스트 판본에서는 **`series`라는 이름에 결코 대입하지 않았고,
  `series.append`를 부르고 그것에 `sum`과 `len`을 적용했을 뿐이다. 그러니까 우리는 리스트가
  가변이라는 사실을 이용한 것이다** (9장 §"The nonlocal Declaration", p.315).[^ramalho2022]
- 불변 타입에서는 그 길이 막힌다 — **수·문자열·튜플 같은 불변 타입으로는 읽는 것만 할 수 있고
  갱신은 결코 할 수 없다. `count = count + 1`처럼 다시 묶으려 하면 암묵적으로 지역 변수
  `count`를 만드는 것이다. 그것은 더는 자유 변수가 아니고, 따라서 클로저에 저장되지 않는다**
  (9장 §"The nonlocal Declaration", p.315).[^ramalho2022]
- 그 자리에 쓰는 것이 `nonlocal`이다 — **어떤 변수가 함수 안에서 대입되더라도 자유 변수라고
  선언하게 해 준다. `nonlocal` 변수에 새 값이 대입되면 클로저에 보관된 바인딩이 바뀐다**
  (9장 §"The nonlocal Declaration", p.316).[^ramalho2022]
  - 버전 조건: 파이썬 3.0 이상. `nonlocal`은 파이썬 3에 도입됐다.
- **위 [함정 하나 — 가변 기본값](#함정-하나--가변-기본값)과 같은 계열이라는 데 값이 있다.**
  거기서는 함수 객체가 기본값을 통해 상태를 지녔고, 여기서는 함수 객체가 셀을 통해 상태를
  지닌다. **둘 다 함수를 호출 사이에 상태를 갖는 것으로 만들지만, 앞의 것은 사고이고 뒤의
  것은 의도다.**

## 이 페이지가 이 KB의 조항과 만나는 자리

- **가변 기본값과 별칭은 [복잡성의 정의와 증상](software-complexity-defined.md)이 말하는
  "모르는 줄도 모르는 것(unknown unknowns)"의 언어 쪽 실물이다.** `HauntedBus`를 읽는
  사람은 `passengers=[]`라는 한 줄에서 그것이 **모든 인스턴스가 공유하는 상태**임을 읽어낼
  수 없다 — 정보가 함수 객체의 `__defaults__`에 숨어 있다. #hypothesis 저자가 그렇게
  연결하지는 않았고, 두 소스가 서로를 참조한 적도 없다.
- **`TwilightBus`의 처방은 [부수 효과 없는 함수](side-effect-free-functions.md)의 조항이
  파이썬에서 한 줄로 실현되는 자리다.** 그쪽이 "명령과 질의를 가르고 로직을 함수 쪽으로
  몰아라"라고 말한다면, 여기서는 **받은 가변 인자를 별칭하지 말고 복사하라**가 같은 목표의
  더 좁은 처방이다 — 넘긴 쪽이 예상 못 한 변경을 겪지 않게 한다.
- **`is`를 쓰지 말라는 경고는 [값 객체와 엔티티](value-objects-and-entities.md)의 구분과
  짝을 이룬다.** 값 객체는 값으로 비교되어야 하므로 `==`이고, 엔티티만이 정체성으로
  비교된다. 파이썬의 기본값은 사용자 정의 클래스에 대해 `object.__eq__`가 ID를 비교하는
  것이므로 **아무것도 하지 않으면 모든 클래스가 엔티티가 된다** (6장 §"Soapbox" 곁글
  §"Equal Treatment to All Objects", p.225).[^ramalho2022]

## 이어지는 페이지

- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 같은 사실이 시퀀스 쪽에서
  일으키는 것들: `[[]] * 3` 함정과 `+=` 수수께끼
- [파이썬 데이터 모델](python-data-model.md) — `__eq__`가 무엇이고 왜 `is`는 그 밖에 있는가
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 여기서 나온 약한 참조가
  기본으로 제공되지 않게 되는 자리와 그 밖의 단서들
- [파이썬다운 객체 만들기](../concepts/building-pythonic-objects.md) — 불변성을 흉내 내는 읽기 전용
  프로퍼티가 무엇을 사고 무엇을 못 사는가
- [데이터 클래스 빌더](../concepts/data-class-builders.md) — `@dataclass`가 가변 기본값을 거부하는
  것이 이 함정의 **부분적** 해결책인 자리
- [값 객체와 엔티티](value-objects-and-entities.md) — 정체성으로 비교할 것과 값으로 비교할
  것의 도메인 쪽 구분
- [부수 효과 없는 함수](side-effect-free-functions.md) — 별칭이 만드는 예측 불가능을
  설계 쪽에서 다루는 원리
- [복잡성의 정의와 증상](software-complexity-defined.md) — 숨은 상태가 왜 복잡성인가
- [클로저와 데코레이터](../concepts/closures-and-decorators.md) — 같은 구분이 자유 변수와 `nonlocal`로
  다시 나타나는 자리
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 6장 "Object References, Mutability, and Recycling",
    pp.201–227(도입 p.201 · §"Variables Are Not Boxes" pp.202–204 · §"Identity, Equality,
    and Aliases" pp.204–206 · §"Choosing Between == and is" pp.206–207 · §"The Relative
    Immutability of Tuples" pp.207–208 · §"Copies Are Shallow by Default" pp.208–211 ·
    §"Deep and Shallow Copies of Arbitrary Objects" pp.211–213 · §"Function Parameters as
    References" pp.213–214 · §"Mutable Types as Parameter Defaults: Bad Idea" pp.214–216 ·
    §"Defensive Programming with Mutable Parameters" pp.216–218 · §"del and Garbage
    Collection" pp.219–221 · §"Tricks Python Plays with Immutables" pp.221–223 ·
    §"Chapter Summary" pp.223–224 · §"Soapbox" 곁글 pp.225–227). 2장 인용 한 건은
    §"Tuples as Immutable Lists" p.33이고, 9장 인용은 §"Closures" p.314 ·
    §"The nonlocal Declaration" pp.315–316이다 — 그 장의 전문은
    [클로저와 데코레이터](../concepts/closures-and-decorators.md)가 갖는다. **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF
    쪽에서 30을 뺀 값이고, 그 오프셋 실측은 `it/archive/ramalho2022/_progress.yaml`
    머리말이 정본이다. Figure 6-1(이름표 비유)·6-2(별칭과 복제)·6-3·6-4(얕은 복사 전후
    상태)·6-5는 전부 이미지로 조판돼 있어 딸린 캡션과 본문 서술만 옮겼다. 코드 펜스는 예제
    6-8 원문 그대로이고, 콘솔 세션으로 실린 나쁜 예(`HauntedBus`·`TwilightBus`·
    `Gizmo`·`weakref.finalize` 시연)는 펜스 자격이 없어 산문으로 서술했다. 약한 참조(weak
    reference)는 저자가 2판에서 본문에서 빼 온라인 글로 옮긴 주제라 요지만 옮겼다.

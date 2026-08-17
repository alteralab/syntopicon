---
type: concept
title: 협력적 다중 상속과 MRO
description: 파이썬이 다중 상속의 이름 충돌을 푸는 방식과 그것을 쓰는 코드가 지켜야 하는 규약 — super를 쓰라는 두 가지 이유와 그 두 인자의 뜻, 메서드 결정 순서가 C3로 계산되며 선언 순서에 달려 있다는 사실, 협력적 메서드라는 규정과 협력하지 않는 메서드 하나가 사슬을 끊는 자리, 믹스인 클래스의 정의와 그것이 MRO에서 먼저 와야 하는 이유, 그리고 표준 라이브러리와 두 프레임워크가 보이는 좋은 사례와 나쁜 사례
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 협력적 다중 상속과 MRO

- [super를 쓰는 두 가지 이유](#super를-쓰는-두-가지-이유)
- [메서드 결정 순서](#메서드-결정-순서)
- [협력적 메서드 — 사슬은 한 곳에서 끊긴다](#협력적-메서드--사슬은-한-곳에서-끊긴다)
- [믹스인 클래스](#믹스인-클래스)
- [실세계의 사례 넷](#실세계의-사례-넷)
- [이 기제가 남기는 것](#이-기제가-남기는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **클래스가 상위 클래스를 둘 이상 가질 때 어느 구현이 실제로 도는지를 무엇이
정하고, 그 위에서 코드를 쓰려면 어떤 규약을 지켜야 하는가.**

이 장이 서는 자리를 저자가 먼저 밝힌다 — **2021년 현재 일반적인 상속의 과용에 대한 상당한
반발이 있다 — 다중 상속만이 아니라. 상위 클래스와 하위 클래스가 단단히 결합돼 있기 때문이다**
(14장 도입, p.488).[^ramalho2022] 그럼에도 이 장이 필요한 이유가 그 다음 문단이다 —
**그러나 우리는 복잡한 클래스 계층으로 설계된 기존 시스템을 유지보수해야 하거나, 상속을 —
때로는 다중 상속까지 — 쓰도록 강요하는 프레임워크를 써야 한다** (같은 자리,
p.488).[^ramalho2022] 상속을 쓸 것인가의 판단 자체는
[상속세](inheritance-tax.md)에 있다.

## super를 쓰는 두 가지 이유

- 규정 — **`super()` 내장 함수의 일관된 사용은 유지보수 가능한 객체 지향 파이썬 프로그램에
  필수적이다** (14장 §"The super() Function", p.488).[^ramalho2022]
- 상위 클래스를 이름으로 직접 부르는 대안이 권장되지 않는 이유가 둘이다 (14장 §"The super()
  Function", p.489):[^ramalho2022]
  - **첫째, 그것은 기반 클래스를 하드코딩한다. `OrderedDict`라는 이름이 `class` 문에도 나오고
    `__setitem__` 안에도 나온다. 앞으로 누군가 기반 클래스를 바꾸거나 하나를 더하려고 `class`
    문을 바꾸면 `__setitem__`의 본문을 갱신하는 것을 잊고 버그를 들일 수 있다.**
  - **둘째 이유는 `super`가 다중 상속을 가진 클래스 계층을 다루는 논리를 구현한다는 것이다.**
- **자바에서 온 사람이 걸리는 자리를 저자가 따로 표시한다** — **자바 생성자 메서드는 상위
  클래스의 무인자 생성자를 자동으로 호출한다. 파이썬은 이것을 하지 않는다. 당신은
  `super().__init__(a, b)`를 쓰는 이 패턴에 익숙해져야 한다** (14장 §"The super()
  Function", p.489).[^ramalho2022] 오버라이드된 `__init__`을 부르는 것이 **상위 클래스들이
  인스턴스 초기화에서 자기 몫을 하게 하는 데 특히 중요하다**고 적는다.
- 파이썬 2의 두 인자 시그니처가 그 뜻을 드러낸다 (14장 §"The super() Function",
  p.490):[^ramalho2022]
  - **`type` — 원하는 메서드를 구현하는 상위 클래스를 찾는 검색 경로의 시작점. 기본값은
    `super()` 호출이 나타나는 메서드를 소유한 클래스다.**
  - **`object_or_type` — 메서드 호출의 수신자가 될 객체(인스턴스 메서드 호출의 경우)나
    클래스(클래스 메서드 호출의 경우). 기본값은 `super()` 호출이 인스턴스 메서드 안에서
    일어난다면 `self`다.**
  - 그래서 반환되는 것이 무엇인지가 정해진다 — **`super()` 호출은 `type` 매개변수의 상위
    클래스에서 메서드를 찾아 그것을 `object_or_type`에 묶는 **동적 프록시 객체**를 돌려준다.
    그래서 우리는 메서드를 부를 때 수신자(`self`)를 명시적으로 넘길 필요가 없다** (같은 절,
    p.490).[^ramalho2022]
  - 파이썬 3에서 두 인자를 명시할 자리는 좁다 — **테스트나 디버깅을 위해 MRO의 일부를
    건너뛰거나, 상위 클래스의 원치 않는 동작을 우회하는 것 같은 특별한 경우에만 필요하다**
    (같은 절, p.490).[^ramalho2022]

## 메서드 결정 순서

- 문제의 이름 — **다중 상속을 구현하는 어떤 언어든 상위 클래스들이 같은 이름의 메서드를
  구현할 때의 잠재적 이름 충돌을 다뤄야 한다. 이것이 "다이아몬드 문제(diamond problem)"라
  불린다** (14장 §"Multiple Inheritance and Method Resolution Order",
  p.494).[^ramalho2022]
- 저장 위치 — **모든 클래스는 `__mro__`라는 속성을 갖는데, 그것은 메서드 결정
  순서(method resolution order)로 상위 클래스들에 대한 참조를 담은 튜플이다. 현재 클래스부터
  `object` 클래스까지 이어진다** (같은 절, p.496).[^ramalho2022]
- 계산 방법 — **MRO는 C3라 불리는 공개된 알고리즘으로 계산된다** (같은 절,
  p.496).[^ramalho2022] 저자는 그 논문을 소개하면서 Michele Simionato의 문장을 함께 인용한다 —
  **"당신이 다중 상속을 강하게 쓰지 않고 자명하지 않은 계층을 갖고 있지 않다면, 당신은 C3
  알고리즘을 이해할 필요가 없고 이 논문을 쉽게 건너뛸 수 있다."**
  - 저자가 흔한 오해 하나를 끊는다 — 그림만 보면 MRO가 너비 우선 탐색을 서술하는 것처럼
    보이지만 **그것은 그 특정 클래스 계층에서만 우연히 그런 것이다** (같은 절,
    p.496).[^ramalho2022]
- **MRO는 그래프만 보지 않는다** — **MRO는 상속 그래프뿐 아니라 하위 클래스 선언에서 상위
  클래스들이 나열된 순서도 고려한다** (14장 §"Multiple Inheritance and Method Resolution
  Order", p.497).[^ramalho2022] `Leaf(A, B)`를 `Leaf(B, A)`로 바꾸면 활성화 순서가 바뀌고,
  협력하지 않는 메서드의 위치에 따라 **어떤 구현은 아예 돌지 않게 된다.**
- **동적이라는 것이 파이썬의 성질이다** — 어떤 클래스 `U`를 단독으로 인스턴스화해
  `super().ping()`을 부르면 `AttributeError`가 나지만, `U`를 다른 계층과 함께 상속한
  하위 클래스 안에서는 같은 호출이 이웃 클래스의 구현으로 이어진다. **파이썬은 동적 언어이므로
  `super()`와 MRO의 상호작용도 동적이다** (14장 §"Multiple Inheritance and Method Resolution
  Order", p.497).[^ramalho2022]
  - 즉 **`super().m()`이 무엇을 부를지는 그 메서드를 쓴 클래스만 봐서는 알 수 없다.** 그것은
    최종 하위 클래스의 선언이 정한다. 이것이 이 기제의 힘이자 이 기제가 읽기 어려운 이유다.

## 협력적 메서드 — 사슬은 한 곳에서 끊긴다

- 규정 (14장 §"Multiple Inheritance and Method Resolution Order",
  p.497):[^ramalho2022]

> When a method calls `super()`, it is a *cooperative method*. Cooperative methods enable
> *cooperative multiple inheritance*. These terms are intentional: in order to work,
> multiple inheritance in Python requires the active cooperation of the methods involved.

- **MRO는 순서만 정하고 발동 여부는 정하지 않는다** — **MRO는 활성화 순서만 정하고, 특정
  메서드가 각 클래스에서 활성화될지는 각 구현이 `super()`를 부르는지 아닌지에 달려 있다**
  (같은 절, p.496).[^ramalho2022] 사슬 중간의 한 메서드가 `super()`를 부르지 않으면 그
  아래는 전부 돌지 않는다.
- 그래서 지침이 나온다 — **협력하지 않는 메서드는 미묘한 버그의 원인이 될 수 있다. (…)
  그래서 루트가 아닌 클래스의 모든 메서드 `m`은 `super().m()`을 부르는 것이 권장된다**
  (14장 §"Multiple Inheritance and Method Resolution Order", p.497).[^ramalho2022]
- 그리고 시그니처 제약이 따라온다 — **협력적 메서드는 호환되는 시그니처를 가져야 한다.
  `A.ping`이 `B.ping`보다 먼저 불릴지 나중에 불릴지 당신은 결코 알 수 없기 때문이다**
  (같은 절, p.497).[^ramalho2022]
  - **이 두 요구가 다중 상속의 실제 비용이다.** 어느 클래스도 자기 이웃이 누구인지 모른 채
    이웃과 시그니처를 맞춰야 하고, 사슬을 끊지 않기로 약속해야 한다. 계약은 있는데 그 계약을
    적을 자리가 언어에 없다.

## 믹스인 클래스

- 정의 — **믹스인 클래스(mixin class)는 다중 상속 배치에서 적어도 하나의 다른 클래스와 함께
  상속되도록 설계된다. 믹스인은 구상 클래스의 유일한 기반 클래스가 되어서는 안 되는데, 그것이
  구상 객체를 위한 모든 기능성을 제공하지 않고 자식이나 형제 클래스의 행동을 더하거나 맞춤
  설정하기만 하기 때문이다** (14장 §"Mixin Classes", p.500).[^ramalho2022]
- **언어의 지원이 없다** — **믹스인 클래스는 파이썬과 C++에서 명시적 언어 지원이 없는
  관례다. 루비는 믹스인으로 동작하는 모듈의 명시적 정의와 사용을 허용한다. C#·PHP·Rust는
  트레이트(trait)를 구현하는데, 그것도 믹스인의 명시적 형태다** (14장 §"Mixin Classes",
  p.500).[^ramalho2022]
- 대표 구현이 대소문자를 가리지 않는 매핑을 만드는 믹스인이다 (14장 §"Case-Insensitive
  Mappings" 예제 14-8, p.500):[^ramalho2022]

  ```python
  import collections

  def _upper(key):
      try:
          return key.upper()
      except AttributeError:
          return key

  class UpperCaseMixin:
      def __setitem__(self, key, item):
          super().__setitem__(_upper(key), item)

      def __getitem__(self, key):
          return super().__getitem__(_upper(key))

      def get(self, key, default=None):
          return super().get(_upper(key), default)

      def __contains__(self, key):
          return super().__contains__(_upper(key))
  ```

- **선언 순서가 규약이 되는 이유가 여기 있다** — **`UpperCaseMixin`의 모든 메서드가
  `super()`를 부르므로 이 믹스인은 같은 시그니처의 메서드를 구현하거나 상속하는 형제 클래스에
  의존한다. 자기 몫을 하려면 믹스인은 대개 그것을 쓰는 하위 클래스의 MRO에서 다른 클래스보다
  먼저 나와야 한다. 실무에서 그것은 믹스인이 클래스 선언의 기반 클래스 튜플에서 첫 번째로
  나와야 한다는 뜻이다** (14장 §"Mixin Classes", p.501).[^ramalho2022]
- **그리고 저자가 이 믹스인을 만들며 겪은 것을 그대로 적어 둔 자리가 이 절에서 가장 값
  있다** (14장 §"Mixin Classes", p.502):[^ramalho2022]

> `UpperDict` and `UpperCounter` seem almost magical, but I had to carefully study the code
> of `UserDict` and `Counter` to make `UpperCaseMixin` work with them.

  - 첫 판본에는 `get`이 없었고 그것이 `UserDict`에서는 동작했지만 `Counter`에서는 아니었다.
    `Counter.__init__`이 `Counter.update`를 쓰고 그것이 `dict`에서 상속한 `get`에 기대는데
    **`dict`의 `get`은 `__getitem__`을 부르지 않기 때문**이다. 이것이
    [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md)과 같은 뿌리다.
  - 저자의 결론 — **그것은 또한 작은 규모에서조차 상속을 지렛대로 쓰는 프로그램의 부서지기
    쉽고 어리둥절한 성질을 뚜렷이 상기시킨다** (같은 절, p.502).[^ramalho2022]

## 실세계의 사례 넷

저자가 순서를 의도적으로 배치한다 — 단순한 것부터 복잡한 것으로, 좋은 사례에서 나쁜 사례로.
**디자인 패턴 책에서 거의 모든 코드가 C++이지만 다중 상속의 유일한 예는 어댑터 패턴이다.
파이썬에서도 다중 상속이 규범은 아니지만 중요한 사례들이 있다** (14장 §"Multiple Inheritance
in the Real World", p.502).[^ramalho2022]

- **ABC도 믹스인이다** — **파이썬 표준 라이브러리에서 다중 상속의 가장 눈에 띄는 사용은
  `collections.abc` 패키지다. 그것은 논쟁적이지 않다: 결국 자바조차 인터페이스의 다중 상속을
  지원하고, ABC는 선택적으로 구상 메서드 구현을 제공할 수 있는 인터페이스 선언이다**
  (14장 §"ABCs Are Mixins Too", p.502).[^ramalho2022] 공식 문서가 그 구상 메서드들을
  **믹스인 메서드(mixin method)**라 부르고, 그래서 **그 ABC들은 두 역할을 겸한다: 인터페이스
  정의이면서 믹스인 클래스다.**
- **`ThreadingMixIn`** — `http.server`의 `ThreadingHTTPServer`가 본문 한 줄로 정의된다.
  그 믹스인의 세 메서드 중 둘은 `super()`를 부르지 않고 하나만 부르는데, 저자가 그 이유를
  구분해 적는다 — `process_request_thread`는 **오버라이드가 아니라 새 메서드이므로**
  부르지 않고, `server_close`는 요청 수신을 멈춘 뒤 스레드를 기다려야 하므로 부른다
  (14장 §"ThreadingMixIn and ForkingMixIn", p.503).[^ramalho2022]
- **장고의 클래스 기반 뷰** — 저자가 이 장에서 가장 좋은 사례로 꼽는다 — **장고의 클래스 기반
  뷰 API는 Tkinter보다 다중 상속의 더 나은 예다. 특히 그 믹스인 클래스들은 이해하기 쉽다:
  각각이 잘 정의된 목적을 갖고 있고 전부 `…Mixin` 접미로 이름 지어져 있다** (14장
  §"Django Generic Views Mixins", p.506).[^ramalho2022]
  - 다만 채택률에 대한 관찰도 함께 있다 — **클래스 기반 뷰가 장고 사용자에게 보편적으로
    받아들여지지는 않았다. 많은 이가 그것을 불투명한 상자로 제한적으로 쓰고, 새로운 것을
    만들어야 할 때 많은 장고 코더는 기반 뷰와 믹스인을 재사용하려 하는 대신 그 모든 책임을
    떠맡는 단일체 뷰 함수를 계속 쓴다** (같은 절, p.506).[^ramalho2022]
- **Tkinter** — 반대 사례다. **Tkinter는 내가 이 글을 쓰는 시점에 25년 됐다. 그것은 현재
  모범 사례의 예가 아니다. 그러나 그것은 코더들이 그 단점을 이해하지 못했을 때 다중 상속이
  어떻게 쓰였는지를 보여 준다** (14장 §"Multiple Inheritance in Tkinter",
  p.508).[^ramalho2022]
  - 진단이 이름에서 시작한다 — **`Misc` 클래스의 이름은 그 자체로 매우 강한 *코드 냄새*다.
    `Misc`는 100개가 넘는 메서드를 갖고 모든 위젯이 그것을 상속한다. 왜 모든 위젯 하나하나가
    클립보드 처리·텍스트 선택·타이머 관리 같은 메서드를 가져야 하는가? 당신은 버튼에 붙여넣기를
    할 수도 없고 스크롤바에서 텍스트를 선택할 수도 없다. `Misc`는 여러 특화된 믹스인 클래스로
    쪼개져야 하고, 모든 위젯이 그 믹스인 전부를 상속해서는 안 된다** (14장 §"Tkinter: The
    Good, the Bad, and the Ugly", pp.513–514).[^ramalho2022]
  - **대가가 사용자에게 어떻게 나타나는지가 수치로 적힌다** — **Tkinter 사용자로서 당신은
    다중 상속을 알거나 쓸 필요가 전혀 없다. 그것은 위젯 클래스 뒤에 숨겨진 구현 세부다.
    그러나 `dir(tkinter.Button)`을 치고 나열된 214개의 속성 중에서 필요한 메서드를 찾으려 할
    때 당신은 과도한 다중 상속의 결과를 겪게 될 것이다** (같은 절, p.514).[^ramalho2022]
  - GUI가 예외 영역이라는 관찰도 함께 있다 — **내 경험상 GUI 툴킷은 상속이 가장 유용한
    자리다** (14장 §"Multiple Inheritance in Tkinter", p.509).[^ramalho2022] 자바의
    `java.awt`·`javax.swing`, 스몰토크의 Morphic도 계층이 깊다는 것이 근거다.

## 이 기제가 남기는 것

- **일반 이론이 없다는 것이 이 장의 전제다** — **앨런 케이가 경구에서 쓴 것은 여전히 참이다:
  실무 프로그래머를 이끌 수 있는 상속에 대한 일반 이론이 아직 없다. 우리가 가진 것은 경험 법칙,
  디자인 패턴, "모범 사례", 영리한 두문자어, 금기 같은 것들이다. 그중 일부는 유용한 지침을
  주지만 어느 것도 보편적으로 받아들여지거나 항상 적용 가능하지 않다** (14장 §"Coping with
  Inheritance", p.510).[^ramalho2022]
- 그래서 이 장의 처방들은 이론이 아니라 목록이다. 그 일곱 지침과 상속 자체를 피하라는 현대
  흐름은 [상속세](inheritance-tax.md)의 넷째 입장 절에 있다 — 이 KB에서 그 판단의 정본이
  그쪽이기 때문이다.
- **응용 개발자와 프레임워크 저자를 가르는 곁글이 그 지침들의 전제를 밝힌다** — **압도적
  다수의 프로그래머는 프레임워크가 아니라 애플리케이션을 쓴다. (…) 애플리케이션을 쓸 때 우리는
  보통 클래스 계층을 코딩할 필요가 없다. 기껏해야 ABC나 프레임워크가 제공하는 다른 클래스를
  상속하는 클래스를 쓴다. 애플리케이션 개발자로서 우리가 다른 것의 상위 클래스 역할을 할 클래스를
  써야 하는 일은 매우 드물다. 우리가 코딩하는 클래스는 거의 항상 잎 클래스다** (14장 곁글
  §"Think about the Classes You Really Need", p.517).[^ramalho2022]
  - 그래서 다층 계층을 짓고 있는 자신을 발견하면 넷 중 하나라고 저자가 적는다 (같은 곁글,
    p.517):[^ramalho2022] **바퀴를 다시 발명하고 있거나, 나쁘게 설계된 프레임워크를 쓰고
    있거나, 과잉 설계하고 있거나(KISS 원칙을 기억하라), 애플리케이션 코딩이 지겨워져 새
    프레임워크를 시작하기로 한 것이다.**

## 이어지는 페이지

- [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md) — 같은 장의 앞부분.
  믹스인이 `Counter`에서 깨진 그 이유
- [상속세](inheritance-tax.md) — 상속을 쓸 것인가의 판단. 이 장의 일곱 지침이 넷째 입장으로
  그쪽에 있다
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 인터페이스를 명시하는
  ABC와 `Protocol`. 이 장이 "인터페이스라면 명시적 ABC여야 한다"고 말하는 자리의 정본
- [파이썬다운 객체 만들기](../concepts/building-pythonic-objects.md) — 클래스 데이터 속성 하나만
  덮어쓰는 하위 클래스, 즉 이 장이 걱정하지 않는 종류의 상속
- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — `Misc`의 214개 속성이 무엇을
  어겼는가의 원리 쪽
- [코드 냄새](../concepts/code-smells.md) — 저자가 `Misc`를 "코드 냄새"라 부를 때 그 낱말의 정본
- [디자인 패턴의 해부](design-pattern-anatomy.md) — 장고의 디스패치가 템플릿 메서드 패턴의
  동적 변형이라는 저자의 관찰이 닿는 자리
- [파이썬의 상속 기제](../synthesis/python-inheritance-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 14장 "Inheritance: For Better or for Worse", pp.487–518
    (경구와 도입 pp.487–488 · §"What's New in This Chapter" p.488 · §"The super() Function"
    pp.488–490 · §"Multiple Inheritance and Method Resolution Order" pp.494–499 ·
    §"Mixin Classes" pp.500–502와 그 아래 §"Case-Insensitive Mappings" · §"Multiple
    Inheritance in the Real World" pp.502–509과 그 아래 §"ABCs Are Mixins Too"·
    §"ThreadingMixIn and ForkingMixIn"·§"Django Generic Views Mixins"·§"Multiple Inheritance
    in Tkinter" · §"Coping with Inheritance" p.510 · §"Tkinter: The Good, the Bad, and the
    Ugly" pp.513–514 · 곁글 §"Think about the Classes You Really Need" p.517).
    §"Subclassing Built-In Types Is Tricky"(pp.490–494)의 전문은
    [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md)이,
    §"Coping with Inheritance" 아래 일곱 지침(pp.510–513)과 §"Chapter Summary"·
    §"Further Reading"의 상속 회피 논의(pp.514–516)는 [상속세](inheritance-tax.md)가 갖는다.
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    Figure 14-1(다이아몬드 활성화 순서)·14-2(Tkinter `Text`의 MRO)·14-3·14-4(장고 제네릭 뷰
    UML)·14-5(Tkinter 위젯 계층)는 전부 이미지로 조판돼 있어 캡션과 본문 서술로만 옮겼다 —
    특히 다이아몬드 예제(예제 14-4·14-5)의 활성화 순서는 doctest 출력에서 판독했고 그림에서
    읽지 않았다. 코드 펜스는 예제 14-8 원문 그대로다.

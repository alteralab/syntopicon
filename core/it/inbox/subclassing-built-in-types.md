---
type: concept
title: 내장 타입을 상속할 때의 함정
description: C로 쓰인 내장 타입의 메서드가 하위 클래스의 오버라이드를 대체로 무시한다는 사실과 그것이 객체 지향의 기본 규칙(늦은 바인딩)을 어기는 자리 — 규칙 없음이 공식 입장이라는 문서, 인스턴스 안팎 두 갈래로 나타나는 증상, collections의 User 계열이라는 처방과 그 실측 비용, 그리고 이 예외가 버그가 아니라 성능을 위한 의도된 교환이라는 저자의 판정
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 내장 타입을 상속할 때의 함정

- [무엇이 문제인가](#무엇이-문제인가)
- [증상 둘 — 인스턴스 안과 밖](#증상-둘--인스턴스-안과-밖)
- [처방 — collections의 User 계열](#처방--collections의-user-계열)
- [적용 범위 — 어디까지가 이 함정인가](#적용-범위--어디까지가-이-함정인가)
- [버그인가 기능인가](#버그인가-기능인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **`dict`이나 `list`를 상속해 메서드 하나만 바꾸면 왜 그 변경이 절반만
적용되는가.**

## 무엇이 문제인가

- 사실관계 — **파이썬의 초기 판본에서는 `list`나 `dict` 같은 내장 타입을 상속하는 것이
  불가능했다. 파이썬 2.2부터는 가능하지만 중대한 단서가 있다: (C로 쓰인) 내장 타입의 코드는
  사용자 정의 클래스가 오버라이드한 메서드를 대체로 호출하지 않는다** (14장 §"Subclassing
  Built-In Types Is Tricky", pp.490–491).[^ramalho2022]
- **규칙이 없다는 것이 공식 입장이다.** 저자가 PyPy 문서의 서술을 인용한다 (14장
  §"Subclassing Built-In Types Is Tricky", p.491):[^ramalho2022]

> Officially, CPython has no rule at all for when exactly overridden method of subclasses
> of built-in types get implicitly called or not. As an approximation, these methods are
> never called by other built-in methods of the same object. For example, an overridden
> `__getitem__()` in a subclass of `dict` will not be called by e.g. the built-in `get()`
> method.

  - **"규칙이 아예 없다"가 이 페이지의 무게중심이다.** 어떤 오버라이드가 먹고 어떤 것이 안
    먹는지를 판정할 규범이 없으므로, 실패는 문서를 읽어서가 아니라 **실행해 봐야** 드러난다.
- **이것이 무엇을 어기는가를 저자가 명시한다** — **이 내장 동작은 객체 지향 프로그래밍의 기본
  규칙 하나를 어기는 것이다: 메서드 탐색은 호출이 상위 클래스에 구현된 메서드 안에서
  일어날 때조차 항상 수신자(`self`)의 클래스에서 시작해야 한다. 이것이 "늦은
  바인딩(late binding)"이라 불리는 것이고, 스몰토크로 유명한 앨런 케이는 그것을 객체 지향
  프로그래밍의 핵심 기능으로 여긴다: `x.method()` 형태의 어떤 호출에서든 호출될 정확한
  메서드는 수신자 `x`의 클래스에 근거해 런타임에 결정되어야 한다** (14장 §"Subclassing
  Built-In Types Is Tricky", pp.491–492).[^ramalho2022]
  - 각주가 대응물을 준다 — **C++에는 가상(virtual) 메서드와 비가상 메서드라는 개념이 있다.
    가상 메서드는 늦게 바인딩되지만 비가상 메서드는 컴파일 시점에 바인딩된다. 파이썬에서 우리가
    쓸 수 있는 모든 메서드가 가상 메서드처럼 늦게 바인딩되지만, C로 쓰인 내장 객체는 적어도
    CPython에서는 기본적으로 비가상 메서드를 가진 것처럼 보인다** (14장 각주 4,
    p.492).[^ramalho2022]

## 증상 둘 — 인스턴스 안과 밖

- **하나 — 같은 인스턴스 안에서.** `dict`을 상속해 `__setitem__`만 바꾼 클래스에서,
  `[]` 연산자로 넣을 때는 오버라이드가 돌지만 **`__init__`으로 만들 때와 `update`로 넣을
  때는 돌지 않는다** (14장 §"Subclassing Built-In Types Is Tricky" 예제 14-1,
  p.491).[^ramalho2022]

  ```python
  class DoppelDict(dict):
      def __setitem__(self, key, value):
          super().__setitem__(key, [value] * 2)
  ```

  - 이 클래스는 넣는 값을 두 번 복제한다. 그런데 `DoppelDict(one=1)`로 만든 인스턴스에서
    `'one'`의 값은 복제되지 않고, `dd['two'] = 2`는 복제되며, `dd.update(three=3)`은 다시
    복제되지 않는다. **같은 클래스 안에서 같은 연산이 경로에 따라 갈린다.**
- **둘 — 다른 객체가 부를 때.** **문제는 인스턴스 안의 호출에 한정되지 않는다 —
  `self.get()`이 `self.__getitem__()`을 부르는가 하는 것만이 아니라, 내장 메서드가 불러야 할
  다른 클래스의 오버라이드된 메서드에서도 일어난다** (14장 §"Subclassing Built-In Types Is
  Tricky", p.492).[^ramalho2022] `dict`을 상속해 `__getitem__`이 항상 42를 돌려주게 만든
  객체를 평범한 `dict`에 `update`로 넘기면, **`dict.update`는 그 오버라이드를 무시하고 원래
  저장된 값을 가져간다** (예제 14-2, p.492).
- **이 함정이 앞 장의 미해결 문제와 같은 뿌리라고 저자가 밝힌다** — 표준 라이브러리의
  `__missing__` 사용이 일관되지 않은 것이 여기서 비롯한다 (14장 §"Subclassing Built-In
  Types Is Tricky", p.492).[^ramalho2022] 그 서술은
  [딕셔너리와 집합](../concepts/dictionaries-and-sets.md)에 있다.

## 처방 — collections의 User 계열

- 조문 — **`dict`이나 `list`나 `str` 같은 내장 타입을 직접 상속하는 것은 오류를 부르기 쉽다.
  내장 메서드가 사용자 정의 오버라이드를 대체로 무시하기 때문이다. 내장 타입을 상속하는 대신
  쉽게 확장되도록 설계된 `collections` 모듈의 `UserDict`·`UserList`·`UserString`에서 당신의
  클래스를 파생시켜라** (14장 §"Subclassing Built-In Types Is Tricky",
  p.492).[^ramalho2022]
  - `collections.UserDict`로 바꾸면 **위 두 예제의 문제가 둘 다 고쳐진다** (14장 예제 14-3,
    p.493).[^ramalho2022]
- **비용이 실측돼 있다.** 저자가 3장의 `StrKeyDict`를 `UserDict` 대신 `dict` 상속으로 다시
  써 보는 실험을 한다 — **같은 테스트 묶음을 통과시키려고 나는 `__init__`·`get`·`update`를
  구현해야 했다. `dict`에서 상속한 판본들이 오버라이드된 `__missing__`·`__contains__`·
  `__setitem__`과 협력하기를 거부했기 때문이다. 예제 3-9의 `UserDict` 하위 클래스는 16줄인
  반면 실험적인 `dict` 하위 클래스는 33줄로 끝났다** (14장 §"Subclassing Built-In Types Is
  Tricky", p.493).[^ramalho2022]
  - **두 배가 조금 넘는 이 수치가 이 페이지가 남기는 계량이다.** 내장 타입을 직접 상속하는
    선택은 "메서드 하나만 바꾸는" 일이 아니라 협력하지 않는 메서드들을 손으로 메꾸는 일이 된다.
- 요구가 아주 다르면 다른 길도 있다 — **원하는 동작이 내장 타입이 제공하는 것과 매우 다르다면
  `collections.abc`의 적절한 ABC를 상속하고 당신 자신의 구현을 쓰는 편이 더 쉬울 수 있다**
  (14장 §"Chapter Summary", p.514).[^ramalho2022]

## 적용 범위 — 어디까지가 이 함정인가

- **경계가 명시돼 있다** — **분명히 해 두자: 이 절은 내장 타입의 C 언어 코드 안에서 일어나는
  메서드 위임에만 적용되는 문제를 다뤘고, 그 타입들에서 **직접** 파생된 클래스에만 영향을
  준다. `UserDict`나 `MutableMapping`처럼 파이썬으로 코딩된 기반 클래스를 상속한다면 당신은
  이것 때문에 곤란해지지 않을 것이다** (14장 §"Subclassing Built-In Types Is Tricky",
  p.494).[^ramalho2022]
- 구현체마다 다르다는 단서도 붙는다 — **이 점에서 PyPy는 CPython보다 더 "올바르게" 구는데,
  사소한 비호환을 도입하는 대가를 치른다** (14장 각주 6, p.494).[^ramalho2022]

## 버그인가 기능인가

곁글 하나가 이 예외를 옹호한다. 이 페이지가 그것을 옮기는 이유는 **의도된 교환과 설계 결함을
가르는 것이 이 KB의 판단 기준이기 때문**이다.

- 이유는 성능이다 — **내장 `dict`·`list`·`str` 타입은 파이썬 자신의 필수 구성 요소이므로
  빨라야 한다 — 그것들의 어떤 성능 문제든 사실상 다른 모든 것에 심각한 영향을 줄 것이다.
  그것이 CPython이 내장 메서드가 하위 클래스에서 오버라이드된 메서드와 협력하지 않아 잘못
  구는 원인이 되는 지름길을 채택한 이유다** (14장 곁글 §"Misbehaving Built-Ins: Bug or
  Feature?", p.517).[^ramalho2022]
- 그리고 **탈출구가 이미 언어 안에 있다는 것이 저자의 논지다** — 각 타입에 최적화된 내부용
  구현과 확장 가능한 외부용 구현 둘을 두는 것이 해법일 텐데, **잠깐, 이것이 우리가 이미 가진
  것이다: `UserDict`·`UserList`·`UserString`은 내장 타입만큼 빠르지는 않지만 쉽게 확장된다**
  (같은 곁글, p.518).[^ramalho2022]
- 맺음이 판정이다 — **CPython이 취한 실용적 접근은 우리가 우리 애플리케이션에서도 상속하기
  어려운 고도로 최적화된 구현을 쓸 수 있게 해 준다는 뜻이다. 맞춤 매핑이나 리스트나 문자열이
  필요한 일이 그리 자주 있지 않은 반면 `dict`·`list`·`str`은 매일 쓴다는 점을 고려하면 이치에
  맞는다. 우리는 그저 관련된 교환을 알고 있으면 된다** (같은 곁글, p.518).[^ramalho2022]

## 이어지는 페이지

- [협력적 다중 상속과 MRO](../concepts/cooperative-multiple-inheritance.md) — 같은 장의 본체. 이
  함정이 `super()`와 믹스인을 다루는 자리로 이어진다
- [딕셔너리와 집합](../concepts/dictionaries-and-sets.md) — `UserDict`에서 맞춤 매핑을 만들어야 하는
  이유가 원래 서술된 자리, 그리고 `__missing__`의 비일관성
- [상속세](../concepts/inheritance-tax.md) — 상속이 곧 결합이라는 진단의 원리 쪽. 이 함정은 그 결합이
  **언어 구현 층**에서 새는 실물이다
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — 하위 클래스가 상위 클래스의
  구현 세부에 의존하게 되는 일반형
- [파이썬 데이터 모델](../concepts/python-data-model.md) — 특수 메서드를 부르는 것이 인터프리터라는
  규칙과, 그 규칙이 내장 타입 안에서는 다르게 적용되는 자리
- [파이썬의 상속 기제](../synthesis/python-inheritance-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 14장 "Inheritance: For Better or for Worse"
    §"Subclassing Built-In Types Is Tricky"(pp.490–494)와 각주 4·6 · §"Chapter Summary"
    (p.514) · 곁글 §"Misbehaving Built-Ins: Bug or Feature?"(pp.517–518).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    코드 펜스는 예제 14-1의 클래스 정의다 — 원문이 doctest 세션이라 `>>> `·`... ` 프롬프트를
    제거해 실행 가능한 형태로 되돌렸고(SCHEMA §3의 깎기), 이어지는 콘솔 출력은 펜스에 섞지
    않고 본문 산문으로 풀었다.

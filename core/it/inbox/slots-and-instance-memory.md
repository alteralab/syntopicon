---
type: concept
title: __slots__와 인스턴스 메모리
description: 파이썬이 인스턴스 속성을 기본적으로 딕셔너리에 담는다는 사실과 그것을 숨은 배열로 바꾸는 __slots__의 기제 — 선언이 만드는 두 효과, 하위 클래스에 절반만 상속된다는 반직관, 천만 인스턴스 실측이 보인 절감폭, 그리고 이 최적화가 사 오는 네 가지 단서와 언제 그 대가를 치를 만한가의 경계
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# __slots__와 인스턴스 메모리

- [기본 저장 모델과 그 대안](#기본-저장-모델과-그-대안)
- [선언이 만드는 두 효과](#선언이-만드는-두-효과)
- [하위 클래스에는 절반만 상속된다](#하위-클래스에는-절반만-상속된다)
- [실측 — 천만 개의 인스턴스](#실측--천만-개의-인스턴스)
- [네 가지 단서](#네-가지-단서)
- [언제 이 대가를 치르는가](#언제-이-대가를-치르는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인스턴스가 아주 많을 때 파이썬 객체의 메모리를 어떻게 줄이고, 그 대신
무엇을 잃는가.**

이 소스가 `__slots__`를 다루는 자리는 이 장 하나뿐이다. 데이터 클래스 쪽에서 같은 이름의
옵션을 찾는다면 [데이터 클래스 빌더](data-class-builders.md)의 버전 조건 블록이 그 관계를
적어 둔다.

## 기본 저장 모델과 그 대안

- 기본값이 딕셔너리다 — **기본적으로 파이썬은 각 인스턴스의 속성을 `__dict__`라는 이름의
  `dict`에 저장한다** (11장 §"Saving Memory with `__slots__`", p.384).[^ramalho2022]
  그 대가가 이미 앞 장에서 계량돼 있다 — **`dict`은 상당한 메모리 오버헤드를 갖는다 — 그
  절에서 언급된 최적화가 있어도 그렇다** (같은 절, p.384).[^ramalho2022] 여기서 가리키는
  최적화가 키 공유 배치이고, 그 서술은 [딕셔너리와 집합](dictionaries-and-sets.md)에 있다.
- 대안의 규정 (11장 §"Saving Memory with `__slots__`", p.384):[^ramalho2022]

> But if you define a class attribute named `__slots__` holding a sequence of attribute
> names, Python uses an alternative storage model for the instance attributes: the
> attributes named in `__slots__` are stored in a hidden array or references that use less
> memory than a `dict`.

  - 즉 **슬롯(slot)**은 이름표가 붙은 자리를 미리 못 박아 두는 것이다. 딕셔너리가 실행 중에
    아무 키나 받을 수 있어서 치르는 비용을, 받을 이름을 클래스 정의 시점에 고정해서
    없앤다.
- **선언 시점이 곧 확정 시점이다** — **`__slots__`는 클래스가 만들어질 때 있어야 한다.
  나중에 더하거나 바꾸는 것은 아무 효과가 없다** (11장 §"Saving Memory with `__slots__`"
  예제 11-13 설명, p.384).[^ramalho2022] 저자는 튜플로 적기를 권한다 — **속성 이름은 튜플에
  담아도 리스트에 담아도 되지만, 나는 그것을 바꿀 이유가 없다는 것을 분명히 하려고 튜플을
  선호한다** (같은 자리, p.384).[^ramalho2022]

## 선언이 만드는 두 효과

예제 11-13의 `Pixel` 클래스가 `__slots__ = ('x', 'y')` 하나로 보이는 것이 둘이다
(11장 §"Saving Memory with `__slots__`", pp.384–385):[^ramalho2022]

- **첫째 효과: `Pixel`의 인스턴스에는 `__dict__`가 없다.** `p.__dict__`를 읽으면
  `AttributeError`가 난다.
- **둘째 효과: `__slots__`에 나열되지 않은 속성을 설정하려 하면 `AttributeError`가
  일어난다.** `p.x`·`p.y`는 평소처럼 설정되지만 `p.color = 'red'`는 거부된다.

메모리 절감이 첫째 효과의 결과라면, 속성 봉인은 그 부수 효과다. **저자는 이 부수 효과를
목적으로 쓰는 것을 명시적으로 기각한다** — 12장이 `__setattr__`로 같은 봉인을 구현하면서
그 이유를 적는다 (12장 §"Vector Take #3: Dynamic Attribute Access",
p.411):[^ramalho2022]

> `__slots__` should be used only to save memory, and only if that is a real issue.

## 하위 클래스에는 절반만 상속된다

이 장이 "반직관적"이라 부르는 자리다 (11장 §"Saving Memory with `__slots__`",
pp.385–386).[^ramalho2022]

- 자기 속성을 하나도 선언하지 않은 하위 클래스 `OpenPixel(Pixel)`의 인스턴스는 **`__dict__`를
  다시 갖는다.** 그러면서도 기반 클래스의 `__slots__`에 있는 `x`를 설정하면 그것은
  `__dict__`가 아니라 여전히 숨은 참조 배열에 담기고, 목록에 없는 `color`만 `__dict__`로
  간다.
- 조문 — **`__slots__`의 효과는 하위 클래스에 부분적으로만 상속된다. 하위 클래스의 인스턴스에
  `__dict__`가 없게 하려면 하위 클래스에서 `__slots__`를 다시 선언해야 한다**
  (11장 §"Saving Memory with `__slots__`", p.386).[^ramalho2022]
  - 빈 튜플 `__slots__ = ()`을 선언하면 하위 클래스 인스턴스에도 `__dict__`가 없고 기반
    클래스가 나열한 속성만 받는다.
  - 속성을 더하고 싶으면 하위 클래스의 `__slots__`에 그 이름만 적는다 — **본질적으로 상위
    클래스들의 `__slots__`가 현재 클래스의 `__slots__`에 더해진다** (같은 절,
    p.386).[^ramalho2022]
- **이것이 이 최적화의 첫째 실패 유형이다.** 계층 어딘가에서 `__slots__` 재선언을 빠뜨리면
  절감이 조용히 사라진다 — 오류가 나지 않고 그냥 `__dict__`가 돌아온다.

## 실측 — 천만 개의 인스턴스

저자가 `mem_test.py`로 잰 값이다. 같은 `Vector2d` 클래스를 `__slots__` 없이/있이 두고
**천만 개의 인스턴스**를 리스트로 만든다 (11장 §"Simple Measure of `__slot__` Savings"
예제 11-17, pp.387–388).[^ramalho2022]

| 판 | 최종 RAM | 실행 시간(real) |
|---|---|---|
| `__dict__` 사용 | 1,666,535,424바이트 (1.55GiB) | 11.990초 |
| `__slots__` 사용 | 577,839,104바이트 (551MiB) | 8.381초 |

- 저자의 요약 — **`__slots__` 판이 더 빠르기도 하다** (11장 §"Simple Measure of `__slot__`
  Savings", p.388).[^ramalho2022] 즉 이 교환은 메모리만이 아니라 생성 속도도 함께 사 온다.
- **다만 같은 자리에서 더 나은 답을 가리킨다** — **수치 데이터를 담은 수백만 개의 객체를
  다루고 있다면 당신은 정말로 NumPy 배열을 써야 한다. 그것은 메모리 효율적일 뿐 아니라 수치
  처리를 위한 고도로 최적화된 함수들을 갖고 있고, 그중 많은 것이 배열 전체를 한 번에 다룬다**
  (11장 §"Simple Measure of `__slot__` Savings", p.388).[^ramalho2022] 예제의
  `Vector2d`는 특수 메서드를 논할 문맥을 주려고 만든 교보재라고 저자가 못 박는다.

- `Vector2d`에 붙는 선언은 두 줄이 전부다 (11장 §"Simple Measure of `__slot__` Savings"
  예제 11-16, p.387):[^ramalho2022]

  ```python
  class Vector2d:
      __match_args__ = ('x', 'y')
      __slots__ = ('__x', '__y')

      typecode = 'd'
  ```

- 두 클래스 속성이 나란히 있는 것이 이 예제의 요점이다 — **`__match_args__`는 위치 패턴
  매칭을 위한 공개 속성 이름들을 나열한다. 그에 반해 `__slots__`는 인스턴스 속성의 이름을
  나열하는데, 이 경우 그것은 비공개 속성이다** (같은 자리, p.387).[^ramalho2022] 같은 두
  성분을 두 목록이 서로 다른 이름으로 부른다 — 하나는 밖에서 보이는 이름, 하나는 실제
  저장되는 이름이다.

## 네 가지 단서

저자가 절 하나를 따로 두어 정리한 목록이다. **`__slots__` 클래스 속성은 제대로 쓰면 상당한
메모리 절감을 줄 수 있지만 몇 가지 단서가 있다** (11장 §"Summarizing the Issues with
`__slots__`", p.388):[^ramalho2022]

1. **하위 클래스마다 `__slots__`를 다시 선언하는 것을 잊지 말아야 한다** — 그러지 않으면 그
   인스턴스들이 `__dict__`를 갖는다.
2. **인스턴스는 `__slots__`에 나열된 속성만 가질 수 있다** — `'__dict__'`를 `__slots__`에
   넣지 않는 한. 그런데 그렇게 하면 메모리 절감이 무효가 될 수 있다.
3. **`__slots__`를 쓰는 클래스는 `@cached_property` 데코레이터를 쓸 수 없다** —
   `'__dict__'`를 명시적으로 나열하지 않는 한.
4. **인스턴스는 약한 참조(weak reference)의 대상이 될 수 없다** — `'__weakref__'`를
   `__slots__`에 더하지 않는 한. 이 속성은 사용자 정의 클래스의 인스턴스에 기본적으로
   존재한다.

- 2번의 우회로에 저자가 붙이는 경고가 이 목록의 무게중심이다 — **"메모리를 아끼면서 먹기"도
  가능하다**: `'__dict__'`를 목록에 넣으면 나열된 속성은 인스턴스별 참조 배열에 남고 동적으로
  만들어진 속성은 평소의 `__dict__`로 간다 (11장 §"Saving Memory with `__slots__`",
  p.386).[^ramalho2022] 그러나 —

> Of course, having `'__dict__'` in `__slots__` may entirely defeat its purpose, depending
> on the number of static and dynamic attributes in each instance and how they are used.
> Careless optimization is worse than premature optimization: you add complexity but may
> not get any benefit.

  - **"부주의한 최적화가 성급한 최적화보다 나쁘다"**는 이 한 줄이 이 페이지가 이 KB에
    남기는 조문이다. 성급한 최적화는 필요 없는 복잡성을 더하고, 부주의한 최적화는 복잡성을
    더하면서 이득도 못 얻는다.

## 언제 이 대가를 치르는가

- 경계가 장 요약에 수치로 적혀 있다 — **`__slots__`를 쓰는 데는 부수 효과가 있으므로,
  그것은 아주 많은 수의 인스턴스를 다룰 때에만 정말로 말이 된다 — 수천 개가 아니라 수백만
  개의 인스턴스를 생각하라. 그런 경우 중 많은 자리에서 pandas를 쓰는 것이 최선의 선택일 수
  있다** (11장 §"Chapter Summary", p.391).[^ramalho2022]
- **그래서 이 페이지의 실용적 결론은 부정형이다.** 이 최적화는 (가) 인스턴스가 백만 단위이고
  (나) 그 인스턴스들이 수치 배열이나 데이터프레임으로 대체될 수 없을 때에만 남는 선택지다.
  두 조건을 다 만족하지 않으면 위 네 단서가 사 오는 복잡성만 남는다.
- 이 장 전체의 마무리도 같은 방향이다 — **객체는 요구사항이 지시하는 만큼만 단순해야 하고,
  언어 기능의 행진이 되어서는 안 된다** (11장 §"Chapter Summary", p.391).[^ramalho2022]
  이 조문의 전문과 그 문맥은 [파이썬다운 객체 만들기](building-pythonic-objects.md)에 있다.

## 이어지는 페이지

- [파이썬다운 객체 만들기](building-pythonic-objects.md) — 같은 장의 본체. `__slots__`가
  붙는 그 `Vector2d`가 어떻게 지어졌는가
- [딕셔너리와 집합](dictionaries-and-sets.md) — 여기서 대체되는 `__dict__`가 무엇이고 그
  오버헤드가 어디서 오는가. 키 공유 최적화와 `__init__` 밖 속성 금지 조항이 그쪽에 있다
- [객체 참조와 가변성](object-references-and-mutability.md) — 약한 참조와 가비지 수집이
  나오는 자리
- [데이터 클래스 빌더](data-class-builders.md) — 같은 이름의 데코레이터 옵션과 이 언어
  기능의 판본 관계
- [시퀀스 프로토콜의 점진 구현](implementing-the-sequence-protocol.md) — `__slots__`를 속성
  봉인 용도로 쓰지 말라는 기각이 실제로 나오는 자리
- [성능을 위한 설계](designing-for-performance.md) — 최적화를 언제 시작할 것인가의 원리 쪽
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 11장 "A Pythonic Object" §"Saving Memory with `__slots__`"
    (pp.384–387) · §"Simple Measure of `__slot__` Savings"(pp.387–388) · §"Summarizing the
    Issues with `__slots__`"(p.388) · §"Chapter Summary"(p.391), 그리고 12장 "Special
    Methods for Sequences" §"Vector Take #3: Dynamic Attribute Access"(p.411)의 기각 한 건.
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    실측 표의 두 수치는 예제 11-17의 셸 세션 출력에서 뽑았다 — 출력이라 펜스가 아니라 표로
    옮겼다(SCHEMA §3). 괄호 안의 GiB·MiB 환산은 저자 자신이 §"Simple Measure of `__slot__`
    Savings" 본문에 적은 값이다. 코드 펜스는 예제 11-16 원문이고, 원문 코드 목록에 삽입된
    조판용 번호 표지와 이어지는 주석 한 줄(`# methods are the same as previous version`)만
    제거했다.

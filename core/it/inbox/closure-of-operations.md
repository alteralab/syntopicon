---
type: concept
title: 연산의 닫힘
description: 인자와 반환 타입을 구현자와 같게 두어 새 개념을 들이지 않고 상위 인터페이스를 얻는 패턴의 원전 — 이름이 수학에서 왔다는 유래와 실수의 곱셈이라는 원형, 인터페이스를 기본형만으로 깎으면 빈약해진다는 전제, 반환 타입을 인자 타입과 같게 두라는 조항과 구현자의 상태도 사실상 인자라는 단서, 이 패턴이 주로 값 객체의 기회이고 엔티티에는 드문 이유, 추상 타입 아래서도 닫힐 수 있다는 확장, 반쪽만 닫혀도 이득이 남는다는 판정, 그리고 컬렉션에서 부분집합을 고르는 두 언어의 대비
generated: { by: "claude-opus-5", at: "2026-09-14T12:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 연산의 닫힘

- [이름이 어디서 왔는가](#이름이-어디서-왔는가)
- [기본형만으로 깎으면 인터페이스가 빈약해진다](#기본형만으로-깎으면-인터페이스가-빈약해진다)
- [조항](#조항)
- [주로 값 객체의 기회다](#주로-값-객체의-기회다)
- [추상 타입 아래서도 닫힌다](#추상-타입-아래서도-닫힌다)
- [반쪽만 닫혀도 이득이 남는다](#반쪽만-닫혀도-이득이-남는다)
- [컬렉션에서 부분집합을 고르기](#컬렉션에서-부분집합을-고르기)
- [이 장이 닫히며 남기는 단서](#이-장이-닫히며-남기는-단서)
- [이 패턴이 다시 나타나는 자리 둘](#이-패턴이-다시-나타나는-자리-둘)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인터페이스를 풍부하게 두면서 새 개념에 대한 의존을 들이지 않으려면 연산의
타입을 어떻게 잡는가.**

## 이름이 어디서 왔는가

- 절이 제사로 시작한다. Drexel 대학교 The Math Forum에서 인용한 것이다 (10장,
  p.268):[^evans2003]

> If we take two real numbers and multiply them together, we get another real number. [The real
> numbers are all the rational numbers and all the irrational numbers.] Because this is always
> true, we say that the real numbers are "closed under the operation of multiplication": there
> is no way to escape the set. When you combine any two elements of the set, the result is also
> included in the set.

- 저자가 그 이름을 가져온 경위 — **정련된 설계의 또 하나의 흔한 관행이 내가 "연산의
  닫힘(CLOSURE OF OPERATIONS)"이라 부르는 것이다. 이름은 개념 체계 중 가장 정련된 것, 곧
  수학에서 왔다** (10장, p.268).[^evans2003]
- 왜 수학에서 빌리는지도 적힌다 — **수학자들은 관계없는 개념을 들이지 않는 데 광적이고, 닫힘이라는
  성질은 그들에게 다른 어떤 개념도 관여시키지 않고 연산을 정의하는 방법을 준다** (10장,
  p.268).[^evans2003] 저자의 논평 — **우리는 수학의 정련에 너무 익숙해져서 그 작은 요령이
  얼마나 강력한지 파악하기 어려울 수 있다. 그러나 이것은 소프트웨어 설계에서도 널리 쓰인다**
  (10장, p.268).[^evans2003]
- 소프트웨어 쪽 실물로 XSLT가 제시된다 — XSLT의 기본 쓰임은 XML 문서 하나를 다른 XML 문서로
  변환하는 것이고, **이런 종류의 XSLT 연산은 XML 문서의 집합 아래서 닫혀 있다** (10장,
  p.268).[^evans2003] 그 성질이 사 오는 것 — **닫힘이라는 성질은 연산의 해석을 엄청나게
  단순화하고, 닫힌 연산을 사슬로 잇거나 조합하는 것을 생각하기 쉽게 만든다** (10장,
  p.268).[^evans2003]

## 기본형만으로 깎으면 인터페이스가 빈약해진다

- 앞 패턴이 남긴 제한을 이어받는다 — 물론 의존은 있을 것이고, **그 의존이 개념에 근본적일 때
  그것은 나쁜 일이 아니다. 인터페이스를 기본형만 다루도록 깎아 내리는 것은 인터페이스를 빈약하게
  만들 수 있다. 그러나 많은 불필요한 의존이, 심지어 개념 전체가, 인터페이스에서 들어온다**
  (10장, p.268).[^evans2003]
- 문제 진술 (10장, p.268):[^evans2003]

> Most interesting objects end up doing things that can't be characterized by primitives alone.

## 조항

- 처방 문단 (10장, p.268):[^evans2003]

> Where it fits, define an operation whose return type is the same as the type of its
> argument(s). If the implementer has state that is used in the computation, then the
> implementer is effectively an argument of the operation, so the argument(s) and return value
> should be of the same type as the implementer. Such an operation is closed under the set of
> instances of that type. A closed operation provides a high-level interface without introducing
> any dependency on other concepts.

  - **둘째 문장이 이 조항의 실제 판정 기준이다.** 계산에 자기 상태를 쓰는 메서드에서는 수신자도
    사실상 인자이므로, 인자와 반환값과 수신자 셋이 같은 타입이어야 닫힌 것으로 센다.
  - **첫 낱말도 조건이다** — "들어맞는 자리에서"(Where it fits). 이 패턴은 어디에나 적용되는
    요구가 아니라 기회를 찾으라는 권고로 적혀 있다.

## 주로 값 객체의 기회다

- 적용 대상이 좁혀진다 — **이 패턴은 값 객체(VALUE OBJECT)의 연산에 가장 자주 적용된다**
  (10장, p.269).[^evans2003]
- 엔티티가 제외되는 이유가 정체성에서 나온다 — **엔티티(ENTITY)의 생애 주기는 도메인에서
  의미를 가지므로, 질문에 답하려고 그냥 새것을 불러낼 수는 없다** (10장,
  p.269).[^evans2003] 이 구분의 정본은
  [값 객체와 엔티티](../concepts/value-objects-and-entities.md)에 있다.
- 그렇다고 엔티티에 닫힌 연산이 없는 것은 아니다 — `Employee` 객체에 그 상급자를 물어 다른
  `Employee`를 돌려받을 수 있다. **그러나 일반적으로 엔티티는 계산의 결과가 될 법한 종류의
  개념이 아니다. 그래서 대체로 이것은 값 객체에서 찾을 기회다** (10장, p.269).[^evans2003]

## 추상 타입 아래서도 닫힌다

- 확장 — **연산은 추상 타입 아래서 닫힐 수 있고, 그 경우 구체적인 인자는 서로 다른 구상
  클래스일 수 있다. 어쨌든 덧셈은 실수 아래서 닫혀 있고 실수는 유리수일 수도 무리수일 수도
  있다** (10장, p.269).[^evans2003]
  - 이 확장이 명세를 논리 연산자로 결합할 때 쓰인다. 그 자리는
    [명세 패턴](specification-pattern.md)이다.

## 반쪽만 닫혀도 이득이 남는다

- 실험 중에 흔히 도달하는 중간 상태가 인정된다 — **상호 의존을 줄이고 응집도를 높일 길을 찾다
  보면 때때로 이 패턴의 절반까지 간다. 인자는 구현자와 맞는데 반환 타입이 다르거나, 반환 타입은
  수신자와 맞는데 인자가 다르다. 이런 연산은 닫혀 있지 않지만 닫힘의 이점을 얼마간 준다**
  (10장, p.269).[^evans2003]
- 그 이점이 성립하는 조건 — **추가된 타입이 기본형이거나 기초 라이브러리 클래스일 때는 닫힘만큼
  머리를 자유롭게 해 준다** (10장, p.269).[^evans2003]
  - **[독립형 클래스](standalone-classes.md)의 셈과 같은 기준이다.** 늘 머릿속에 있는 기초는
    부하로 세지 않는다.
- 이 장 앞부분에서 이미 나온 실물이 지목된다. `Pigment Color`의 `mixedWith()` 연산은 안료 색
  아래서 닫혀 있었다 (10장, p.269).[^evans2003]

## 컬렉션에서 부분집합을 고르기

- 사례는 참된 닫힘에 이르지 않아도 이 발상이 얼마나 쓸모 있는지를 보이려는 것이다 (10장,
  p.269).[^evans2003]
- 자바 쪽 — 컬렉션에서 원소의 부분집합을 고르려면 반복자(`Iterator`)를 요청하고, 원소를 돌며
  하나씩 시험하고, 맞는 것을 새 컬렉션에 모은다 (10장, pp.269–270).[^evans2003] 저자의 반응 —
  **개념적으로 나는 집합의 부분집합을 골랐다. 이 추가 개념 `Iterator`와 그 모든 기계적 복잡성이
  나에게 왜 필요한가?** (10장, p.270).[^evans2003]
- 스몰토크 쪽 — 컬렉션에 `select` 연산을 부르고 시험을 인자로 넘기면 시험을 통과한 원소만 담은
  새 컬렉션이 돌아온다. 코드는 `employees select: [:anEmployee | anEmployee salary < 40000]`
  한 줄이다 (10장, p.270).[^evans2003]
- 이 연산의 지위가 정확히 규정된다 — **연산들은 닫혀 있지 않다. "블록(block)"을 인자로 받기
  때문이다. 그러나 블록은 스몰토크의 기초 라이브러리 타입이라 개발자의 정신적 부하를 더하지
  않는다. 반환값이 구현자와 맞기 때문에 그것들은 일련의 필터처럼 줄줄이 이을 수 있다. 쓰기
  쉽고 읽기 쉽다. 그것들은 부분집합을 고르는 문제와 무관한 이질적 개념을 들이지 않는다**
  (10장, p.270).[^evans2003]
  - **반쪽 닫힘이 사 오는 것이 여기서 셋으로 드러난다.** 이어 붙일 수 있고, 읽기 쉽고, 무관한
    개념이 없다. 자바 판과 스몰토크 판의 차이는 기능이 아니라 클라이언트가 알아야 하는 개념의
    수다.

## 이 장이 닫히며 남기는 단서

- 이 패턴을 끝으로 장의 패턴들이 마무리되고, 저자가 전체에 대한 평을 붙인다 — 이 패턴들은
  **설계의 일반적 스타일과 설계를 생각하는 방식**을 보여 주며, **소프트웨어를 뻔하고 예측
  가능하고 소통하게 만드는 것이 추상과 캡슐화를 효과적으로 만든다** (10장,
  p.270).[^evans2003]
- 그리고 비용이 정직하게 적힌다 — **이 기법들은 적용하는 데, 때로는 클라이언트를 쓰는 데조차
  꽤 고급 설계 기량을 요구한다. 모델 주도 설계의 유용성은 상세 설계와 구현 결정의 질에
  민감하며, 혼란스러운 개발자 몇 명만으로도 프로젝트를 목표에서 탈선시키기에 충분하다**
  (10장, p.270).[^evans2003]
  - **이 단서가 이 장 전체의 적용 조건이다.** 패턴이 좋다는 주장과 팀이 그것을 감당할 수 있다는
    주장이 별개로 적혀 있다. 모델 주도 설계의 조항은
    [모델 주도 설계](../concepts/model-driven-design.md)에 있다.

## 이 패턴이 다시 나타나는 자리 둘

- **명세의 논리 연산자.** "AND"와 "OR"와 "NOT"은 술어 아래서 닫혀 있으므로 명세의 결합도 이
  패턴을 보인다 (10장, p.274).[^evans2003] 그 확장의 전문은
  [명세 패턴](specification-pattern.md)에 있다.
- **지분 수학의 더하기와 빼기.** 이 장 끝의 통합 예제에서 `Share Pie`가 값 객체가 되면서
  `plus()`와 `minus()`가 지분 몫 아래서 닫힌다 (10장, p.288).[^evans2003] 그 사례가 사는
  자리는 [확립된 형식 체계](established-formalisms.md)다.

## 이어지는 페이지

- [독립형 클래스](standalone-classes.md) — 같은 장의 앞 패턴. 이 패턴이 답하는 제한을 남기는 쪽
- [개념의 윤곽](conceptual-contours.md) — 같은 장에서 무엇을 단위로 삼을지를 정하는 쪽
- [확립된 형식 체계](established-formalisms.md) — 수학의 닫힘을 통째로 빌려 오는 자리
- [명세 패턴](specification-pattern.md) — 닫힌 연산으로 규칙을 조합하는 실물
- [값 객체와 엔티티](../concepts/value-objects-and-entities.md) — 이 패턴이 주로 사는 쪽
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 닫힌 연산이 값을 파생시키는
  방식과 짝을 이루는 조항
- [모델 주도 설계](../concepts/model-driven-design.md) — 이 장의 패턴들이 봉사하는 상위 조항
- [파이썬의 연산자 오버로딩](../concepts/operator-overloading-in-python.md) — 같은 형태의 닫힌
  연산을 언어 기능으로 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 10장 "Supple Design" §CLOSURE OF OPERATIONS(pp.268–270) ·
    §"Extending SPECIFICATIONS in a Declarative Style"(p.274) · 예제 "Integrating the
    Patterns: Shares Math"(p.288). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴
    이름을 작은 대문자로 조판하는 관례를 직인용에서 유지했다. 제사의 출처는 원문 표기대로
    Drexel 대학교 The Math Forum이다. 부분집합 고르기 예제의 자바 코드와 스몰토크 코드
    (pp.269–270)는 같은 일을 두 언어로 보이는 전후 대비 쌍이라 펜스로 옮기지 않고 산문과
    인라인 코드로 서술했다 — 이 페이지에는 펜스가 없다.

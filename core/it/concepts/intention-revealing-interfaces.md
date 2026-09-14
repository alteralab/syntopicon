---
type: concept
title: 의도를 드러내는 인터페이스
description: 인터페이스의 이름이 목적을 말하고 수단은 말하지 않아야 한다는 조항의 원전 — 규칙을 명시하지 않고 효과만 내는 코드가 무엇을 잃는가, 인터페이스가 말해 주지 않으면 캡슐화의 값이 사라진다는 진단, 구현에서 목적을 유추한 개발자가 우연히만 맞는 목적을 유추하게 된다는 위험, 이름이 유비쿼터스 언어를 따라야 한다는 요구와 클라이언트 시점을 강제하는 테스트 우선, 페인트 혼합 예제에서 이름 하나가 바뀌며 회수된 것, 그리고 이 조항만으로는 모자라다는 같은 장의 두 실측
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 의도를 드러내는 인터페이스

- [규칙을 말하지 않고 효과만 내는 코드](#규칙을-말하지-않고-효과만-내는-코드)
- [인터페이스가 말해 주지 않으면 캡슐화가 사라진다](#인터페이스가-말해-주지-않으면-캡슐화가-사라진다)
- [구현에서 목적을 유추할 때 생기는 일](#구현에서-목적을-유추할-때-생기는-일)
- [조항](#조항)
- [클라이언트 시점을 강제하는 테스트](#클라이언트-시점을-강제하는-테스트)
- [이름 하나로 회수되는 것](#이름-하나로-회수되는-것)
- [이름을 주는 대상이 규칙과 생성기일 때](#이름을-주는-대상이-규칙과-생성기일-때)
- [이 조항만으로는 모자란 자리](#이-조항만으로는-모자란-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인터페이스의 이름은 무엇을 말해야 하고 무엇을 말하지 않아야 하는가.**

## 규칙을 말하지 않고 효과만 내는 코드

- 장이 여는 진단 — **도메인 주도 설계에서 우리는 유의미한 도메인 로직에 대해 생각하고 싶다.
  규칙을 명시적으로 진술하지 않은 채 그 규칙의 효과를 내는 코드는 우리로 하여금 단계별
  소프트웨어 절차로 생각하도록 강제한다. 그저 어떤 코드를 돌린 결과로 나오되 명시적이지 않은
  계산도 마찬가지다** (10장, p.246).[^evans2003]
- 그 대가 — **모델과의 명확한 연결이 없으면 코드의 효과를 이해하거나 변경의 효과를 예상하기가
  어렵다** (10장, p.246).[^evans2003]
- 객체가 무엇을 해 주기로 되어 있는지가 이어서 규정된다 — **객체의 아름다움은 그 모든 것을
  캡슐화해서 클라이언트 코드가 단순해지고 더 상위 개념의 관점에서 해석될 수 있게 하는
  능력이다** (10장, p.246).[^evans2003]

## 인터페이스가 말해 주지 않으면 캡슐화가 사라진다

- 조건절이 이 패턴의 문제 설정이다 — **그러나 인터페이스가 클라이언트 개발자에게 그 객체를
  효과적으로 쓰는 데 알아야 할 것을 말해 주지 않으면, 그는 어차피 세부를 이해하려고 내부를
  파고들어야 할 것이다. 클라이언트 코드를 읽는 사람도 같은 일을 해야 할 것이다. 그러면 캡슐화의
  값 대부분이 사라진다** (10장, p.246).[^evans2003]
- 인지 부하로 그 값이 계산된다 — **우리는 늘 인지 과부하와 싸우고 있다: 클라이언트 개발자의
  머리가 어떤 구성 요소가 어떻게 자기 일을 하는지에 대한 세부로 넘치면, 그의 머리는 클라이언트
  설계의 복잡한 문제를 풀 여유가 없다** (10장, p.246).[^evans2003]
- **그리고 그 계산이 혼자 일할 때도 성립한다는 단서가 붙는다** — **같은 사람이 자기 코드를
  개발하고 쓰는 두 역할을 다 맡을 때조차 이것은 참인데, 그가 그 세부를 배울 필요가 없다
  해도 한 번에 고려할 수 있는 요인의 수에는 한계가 있기 때문이다** (10장,
  p.246).[^evans2003]
  - [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md)이 같은 진단을 모듈 깊이로
    말한다. 이 소스의 기여는 **인터페이스의 이름**을 그 진단의 대상으로 명시하는 것이다.

## 구현에서 목적을 유추할 때 생기는 일

- 한 문장짜리 판정 (10장, p.246):[^evans2003]

> If a developer must consider the implementation of a component in order to use it, the value
> of encapsulation is lost.

- 이어지는 진단이 이 패턴에서 가장 미묘한 자리다 — **원래 개발자가 아닌 누군가가 객체나 연산의
  목적을 그 구현에 기반해 유추해야 한다면, 그 새 개발자는 그 연산이나 클래스가 우연히만
  충족하는 목적을 유추할 수 있다. 그것이 의도가 아니었다면 그 코드는 당장은 작동할 수 있지만
  설계의 개념적 기반은 훼손되었을 것이고, 두 개발자는 서로 어긋난 목적으로 일하게 될 것이다**
  (10장, p.246).[^evans2003]
  - **버그가 나지 않는다는 것이 이 진단의 핵심이다.** 코드는 당장 돈다. 훼손되는 것은 개념적
    기반이므로, 이 실패는 테스트로 잡히지 않고 나중에 두 사람의 설계가 어긋나는 것으로만
    드러난다.
- 그래서 이름이 개념 모델링의 마지막 단계로 규정된다 — **어떤 개념을 클래스나 메서드의 형태로
  명시적으로 모델링한 값을 얻으려면, 우리는 그 프로그램 요소에 그 개념을 반영하는 이름을 주어야
  한다** (10장, p.246).[^evans2003]
- 저자가 앞선 출처를 밝힌다 — **켄트 벡은 메서드 이름이 의도를 드러내는 선택자(INTENTION-
  REVEALING SELECTOR)로 그 목적을 전달하게 만드는 것에 대해 썼다** (10장, p.247).[^evans2003]
  이 패턴은 그것을 인터페이스 전체로 넓힌 것이고, 여기서 의도를 드러내는 인터페이스
  (INTENTION-REVEALING INTERFACE)라는 이름이 나온다 — **설계의 모든 공개 요소가 함께 그
  인터페이스를 이루며, 그 각 요소의 이름은 설계의 의도를 드러낼 기회를 제시한다. 타입 이름,
  메서드 이름, 인수 이름이 모두 결합해 의도를 드러내는 인터페이스를 이룬다** (10장,
  p.247).[^evans2003]

## 조항

- 처방 문단 (10장, p.247):[^evans2003]

> Name classes and operations to describe their effect and purpose, without reference to the
> means by which they do what they promise. This relieves the client developer of the need to
> understand the internals. These names should conform to the UBIQUITOUS LANGUAGE so that team
> members can quickly infer their meaning. Write a test for a behavior before creating it, to
> force your thinking into client developer mode.
>
> All the tricky mechanism should be encapsulated behind abstract interfaces that speak in
> terms of intentions, rather than means.

- 무엇을 말하고 무엇을 말하지 않는지가 세 쌍으로 예시된다 (10장, p.247):[^evans2003]

> In the public interfaces of the domain, state relationships and rules, but not how they are
> enforced; describe events and actions, but not how they are carried out; formulate the
> equation but not the numerical method to solve it. Pose the question, but don't present the
> means by which the answer shall be found.

  - **이름의 정본이 [유비쿼터스 언어](ubiquitous-language.md)로 못 박힌 것이 이 조항의
    핵심이다.** 이름을 잘 짓는 문제가 아니라 **팀이 합의한 모델의 어휘를 쓰는** 문제로
    재분류된다. 그 어휘에 무엇이 들어오는가는
    [모델의 개념과 도메인의 사실](model-concepts-versus-domain-facts.md)이 다룬다.

## 클라이언트 시점을 강제하는 테스트

- 조항의 마지막 문장이 절차를 지정한다 — 행동을 만들기 **전에** 테스트를 써서 클라이언트
  개발자 모드로 사고를 강제하라는 것이다. 저자는 페인트 혼합 예제에서 그것을 실연한다.
- 처음 테스트는 통과하지만 저자가 만족하지 않는다 — **통과하는 테스트가 출발점이다. 이 시점에
  그것은 불만스러운데, 테스트의 코드가 그것이 무엇을 하는지 말해 주지 않기 때문이다** (10장,
  p.248).[^evans2003]
- 그래서 **원하는 사용법을 먼저 쓴다** — **클라이언트 애플리케이션을 쓰고 있다면 `Paint`
  객체를 이렇게 쓰고 싶다는 방식을 반영하도록 테스트를 다시 쓰자. 처음에 이 테스트는
  실패할 것이다. 사실 컴파일조차 되지 않을 것이다. 우리는 클라이언트 개발자의 관점에서
  `Paint` 객체의 인터페이스 설계를 탐색하려고 그것을 쓰고 있다** (10장,
  p.248):[^evans2003]

  ```java
  public void testPaint() {
      // Start with a pure yellow paint with volume=100
      Paint ourPaint = new Paint(100.0, 0, 50, 0);
      // Take a pure blue paint with volume=100
      Paint blue = new Paint(100.0, 0, 0, 50);

      // Mix the blue into the yellow
      ourPaint.mixIn(blue);

      // Result should be volume of 200.0 of green paint
      assertEquals(200.0, ourPaint.getVolume(), 0.01);
      assertEquals(25, ourPaint.getBlue());
      assertEquals(25, ourPaint.getYellow());
      assertEquals(0, ourPaint.getRed());
  }
  ```

- 그다음 순서가 명시된다 — **우리는 이 객체들과 이야기하고 싶은 방식을 반영하는 테스트를 쓰는
  데 시간을 들여야 한다. 그런 다음 그 테스트가 통과하도록 `Paint` 클래스를 리팩터링한다**
  (10장, p.249).[^evans2003]
  - **테스트가 여기서 검증 도구가 아니라 설계 도구로 쓰인다.** 이 KB에서 같은 논증을 다루는
    자리가 [테스트가 코딩을 이끈다](test-to-code.md)이고,
    [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)가 그 절충을 다룬다.

## 이름 하나로 회수되는 것

- 예제의 처음 상태 — 페인트 클래스에 `v`·`r`·`y`·`b` 네 필드와 `paint(Paint)` 메서드 하나가
  있고, 저자의 판정은 이렇다 — **`paint(Paint)` 메서드가 무엇을 하는지 짐작이라도 하는 유일한
  방법은 코드를 읽는 것이다** (10장, p.247).[^evans2003]
- 리팩터링 뒤 필드는 `volume`·`red`·`yellow`·`blue`가 되고 메서드는 `mixIn(Paint)`가 된다
  (Figure 10.3, p.249).[^evans2003]
- **저자가 그 효과의 한계까지 적는다** — **새 메서드 이름이 다른 `Paint`를 "섞어 넣는" 효과에
  대해 독자에게 전부 말해 주지는 않을 것이다(그것을 위해서는 몇 쪽 뒤에 나올 단언(ASSERTIONS)이
  필요하다). 그러나 그것은 독자에게 그 클래스를 쓰기 시작할 만큼의 단서를 줄 것이고, 특히
  테스트가 제공하는 예제와 함께라면 그렇다. 그리고 그것은 클라이언트 코드를 읽는 사람이
  클라이언트의 의도를 해석하게 해 줄 것이다** (10장, p.249).[^evans2003]
  - 이름이 완전 명세가 아니라 **시작할 수 있게 하는 단서**로 규정된다는 것이 이 절의 판정이다.
- 이 패턴이 적용되는 규모가 마지막에 확장된다 — **하위 도메인 전체를 별도의 모듈로 잘라 내
  의도를 드러내는 인터페이스 뒤에 캡슐화할 수 있다** (10장, p.249).[^evans2003] 그 규모의
  판단을 다루는 자리가 [핵심 도메인](../concepts/core-domain.md)이다.

## 이름을 주는 대상이 규칙과 생성기일 때

9장이 이 조항을 두 자리에 더 건다. 하나는 제약이고 다른 하나는 생성기의 인터페이스다.

- **제약.** 조건 로직을 별도 메서드로 뽑아낼 때 그 메서드가 얻어야 하는 것이 이 조항이 요구하는
  이름이다 — **제약을 자기 메서드로 뽑아내면 우리가 그것에 의도를 드러내는 이름을 주어 설계에서
  제약을 명시적으로 만들 수 있다. 그것은 이제 우리가 논의할 수 있는 이름 붙은 사물이다** (9장,
  p.221).[^evans2003] 두 판본의 차이도 이 조항의 잣대로 판정된다 — **이 코드의 두 판본 모두
  제약을 강제하지만, 둘째 판은 모델과 더 뻔한 관계를 갖는다** (9장, p.221).[^evans2003]
  전문은 [명시적 제약](../concepts/explicit-constraints.md)에 있다.
- **생성기.** 객체를 만들어 내는 구성 요소의 인터페이스를 절차가 아니라 서술적 명세로 정의할
  때의 이득에서, 이 조항의 문제 설정이 그대로 반복된다 (9장, p.235):[^evans2003]

> The interface communicates its rules explicitly, so developers can know what to expect from the
> generator without understanding all details of its operation. The only way to predict the
> behavior of a procedurally defined generator is to run cases or to understand every line of code.

  - **위 [인터페이스가 말해 주지 않으면 캡슐화가 사라진다](#인터페이스가-말해-주지-않으면-캡슐화가-사라진다)와
    같은 진단이다.** 다른 점은 여기서 대안이 더 나은 이름이 아니라 **명세 객체**라는 것이다.
    구현과 인터페이스가 결합 해제되고, 요청의 진술이 클라이언트 손에 남으며, 생성기는 명세의
    문면을 채울 의무만 진다 (9장, p.235).[^evans2003] 그 형태는
    [명세 패턴](specification-pattern.md)이 다룬다.
- 그리고 이 소스는 인터페이스가 이름만으로 못 말하는 것을 어디에 적는지도 여기서 보인다. 창고
  적재기 서비스의 인터페이스에는 단언이 주석으로 붙어 있고, 저자는 그것을 10장 단언의 사례로
  지목한다 (9장, pp.235·238).[^evans2003] 그 인터페이스의 전문은
  [도메인 객체가 된 프로세스](processes-as-domain-objects.md)에 있다.

## 이 조항만으로는 모자란 자리

같은 장이 이 조항의 한계를 두 번 실물로 짚는다. 둘 다 이름이 이미 좋은 코드에서 시작한다.

- **부수 효과가 남아 있을 때.** 다음 패턴이 이 조항을 이어받으며 적는다 — 이 조항이 **우리를
  거기까지 절반은 데려다주지만, 의도에 대한 비형식적 암시가 늘 충분하지는 않다** (10장,
  p.255).[^evans2003] 이름이 무엇을 하는지 말해도, 연산이 무엇을 바꾸는지는 인터페이스가
  제한하지 않는다. 그 공백을 [단언](../concepts/assertions-pattern.md)이 메운다.
- **입도가 어긋나 있을 때.** 10장 끝의 통합 예제가 이 조항을 갖춘 코드에서 출발한다 — **이
  설계는 이미 의도를 드러내는 인터페이스를 갖추고 있다. 그러나
  `distributePaymentPrincipal()` 메서드는 위험한 일을 한다** (10장, p.285).[^evans2003]
  질의와 수정자를 가른 뒤에도 코드는 연산이 늘 때마다 무거워졌고, 저자는 그것을 입도가 너무
  거친 신호로 읽는다 (10장, p.286).[^evans2003] 그 연쇄는
  [확립된 형식 체계](../concepts/established-formalisms.md)에 있다.
- 그래서 이 장은 세 조항을 함께 요구한다 (10장, p.259):[^evans2003]

> The communicativeness of the INTENTION-REVEALING INTERFACES, combined with the predictability
> given by SIDE-EFFECT-FREE FUNCTIONS and ASSERTIONS, should make encapsulation and abstraction
> safe.

  - 그리고 셋이 갖춰지면 선언적 영역에 발을 들이게 된다는 판정이
    [선언적 설계](../concepts/declarative-design.md)에 있다.

## 이어지는 페이지

- [부수 효과 없는 함수](side-effect-free-functions.md) — 같은 장의 다음 패턴. 이름이 약속한
  것을 예측 가능하게 만드는 쪽
- [단언](../concepts/assertions-pattern.md) — 이름이 못 말하는 상태 변경을 못 박는 쪽
- [개념의 윤곽](../concepts/conceptual-contours.md) — 이름을 붙일 단위의 굵기를 정하는 쪽
- [선언적 설계](../concepts/declarative-design.md) — 이 조항이 세 조건 중 하나가 되는 자리
- [확립된 형식 체계](../concepts/established-formalisms.md) — 이 조항을 갖춘 코드가 더 나아가는 연쇄
- [모델의 개념과 도메인의 사실](model-concepts-versus-domain-facts.md) — 이 조항이 이름에
  담으라고 요구하는 것이 어디까지인가
- [유비쿼터스 언어](ubiquitous-language.md) — 이름의 정본
- [이름 짓기](naming-things.md) — 코드의 이름을 다루는 이 KB의 자리
- [코드는 뻔해야 한다](obvious-code.md) — 같은 목표를 읽는 사람 쪽에서 정의하는 자리
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — 캡슐화가 깨지는 다른 경로
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 인터페이스와 구현의 비율로 같은
  것을 재는 자리
- [인터페이스 문서화](interface-documentation.md) — 이름으로 못 말하는 것을 어디에 적는가
- [명시적 제약](../concepts/explicit-constraints.md) — 이 조항이 제약에 걸리는 자리
- [명세 패턴](specification-pattern.md) — 이 조항이 생성기 인터페이스에 걸리는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 10장 "Supple Design" §INTENTION-REVEALING INTERFACES
    (pp.246–249) · 9장 "Making Implicit Concepts Explicit"(§Explicit Constraints p.221 ·
    §"Building to Order (Generating)" p.235 · 예제 "Chemical Warehouse Packer" p.238) ·
    10장 §ASSERTIONS 도입(p.255)과 마무리(p.259) · 예제 "Integrating the Patterns: Shares
    Math"(pp.285–286). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로
    조판하는 관례를 직인용에서 유지했다. 저자가 밝힌 앞선 출처는 Beck 1997이다. 펜스의
    Java 테스트는 p.248 원문 그대로이며 원문 조판의 빈 줄 배치만 정돈했다 — 보탠 줄은 없다.
    이 코드는 **2003년 Java의 관용**이라 JUnit 3 스타일(`public void test…`)을 쓴다.
    리팩터링 전 판의 `paint(Paint)` 메서드와 첫 테스트(pp.247–248)는 같은 코드의 전후 대비
    쌍이라 펜스로 옮기지 않고 산문으로 서술했다. 클래스 다이어그램(Figure 10.2·10.3)은
    도판이라 필드·메서드 이름만 옮겼다.

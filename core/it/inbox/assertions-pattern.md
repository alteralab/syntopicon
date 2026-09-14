---
type: concept
title: 단언
description: 연산의 결과를 구현을 읽지 않고 알 수 있게 만드는 패턴의 원전 — 부수 효과가 구현으로만 정의될 때 위임이 많은 설계가 인과의 엉킴이 된다는 진단과 그때 캡슐화와 추상이 각각 잃는 것, 마이어의 계약에 의한 설계에서 빌려 온 세 요소, 단언이 절차가 아니라 상태를 서술하기에 분석과 테스트가 쉬워진다는 근거, 언어가 지원하지 않으면 자동 단위 테스트로 쓰라는 조항과 그 뒤에 붙는 둘째 조항, 사람은 술어를 머릿속에서 컴파일하지 않는다는 단서, 그리고 어색한 후행 조건이 빠진 개념을 가리키는 신호였다는 페인트 혼합 사례
generated: { by: "claude-opus-5", at: "2026-09-14T12:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 단언

- [부수 효과가 구현으로만 정의될 때](#부수-효과가-구현으로만-정의될-때)
- [계약에 의한 설계에서 빌려 온 것](#계약에-의한-설계에서-빌려-온-것)
- [상태를 서술하기 때문에 쉬워지는 것](#상태를-서술하기-때문에-쉬워지는-것)
- [조항](#조항)
- [사람은 술어를 머릿속에서 컴파일하지 않는다](#사람은-술어를-머릿속에서-컴파일하지-않는다)
- [어색한 후행 조건이 가리킨 것 — 페인트 혼합](#어색한-후행-조건이-가리킨-것--페인트-혼합)
- [모델을 바꾸자 단언이 상식이 되었다](#모델을-바꾸자-단언이-상식이-되었다)
- [세 패턴이 함께 사 오는 것](#세-패턴이-함께-사-오는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 연산을 부르면 무슨 일이 일어나는지를 구현을 파고들지 않고 어떻게
알 수 있는가.**

## 부수 효과가 구현으로만 정의될 때

- 앞 패턴이 남긴 잔여물에서 출발한다 — 복잡한 계산을
  [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)로 갈라내면 문제가 작아지지만
  **엔티티(ENTITY) 위에는 여전히 부수 효과를 내는 명령의 잔여물이 남고, 그것을 쓰는 사람은
  누구든 그 결과를 이해해야 한다** (10장, p.255).[^evans2003]
- 복잡한 계산이 없는 명령 하나는 들여다보면 해석할 만하다. 문제는 조립이다 — **큰 부분이 작은
  부분으로 지어지는 설계에서 명령은 다른 명령을 호출할 수 있다. 상위 명령을 쓰는 개발자는
  바탕에 있는 각 명령의 결과를 이해해야 한다. 캡슐화는 그것으로 끝이다** (10장,
  p.255).[^evans2003]
- 다형성 쪽에서도 같은 일이 일어난다 — **객체 인터페이스가 부수 효과를 제한하지 않기 때문에,
  같은 인터페이스를 구현하는 두 서브클래스가 서로 다른 부수 효과를 가질 수 있다. 그것들을 쓰는
  개발자는 결과를 예상하려고 어느 쪽이 어느 쪽인지 알고 싶어 할 것이다. 추상과 다형성은 그것으로
  끝이다** (10장, p.255).[^evans2003]
- 진단 문단 (10장, p.255):[^evans2003]

> When the side effects of operations are only defined implicitly by their implementation,
> designs with a lot of delegation become a tangle of cause and effect. The only way to
> understand a program is to trace execution through branching paths. The value of
> encapsulation is lost. The necessity of tracing concrete execution defeats abstraction.

  - **두 손실이 각각 다른 기제로 계상된다.** 캡슐화는 안을 들여다보게 되어서 잃고, 추상은
    구체적인 실행을 따라가야만 해서 잃는다.
- 이름만으로는 모자란다는 것이 이 패턴이 앞 패턴에 더하는 자리다 —
  [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)가 절반까지
  데려다주지만 **의도에 대한 비형식적 암시가 늘 충분하지는 않다** (10장, p.255).[^evans2003]

## 계약에 의한 설계에서 빌려 온 것

- 저자는 다음 걸음을 다른 학파에서 가져온다 — **"계약에 의한 설계(design by contract)" 학파가
  다음 걸음을 내디뎌, 개발자가 참이라고 보증하는 "단언(assertions)"을 클래스와 메서드에 대해
  만든다** (10장, p.255).[^evans2003] 자세한 논의로는 Meyer 1988을 댄다.
- 세 요소가 짧게 규정된다 (10장, p.255):[^evans2003]
  - **후행 조건(post-conditions)은 연산의 부수 효과를, 곧 메서드를 호출했을 때 보증되는 결과를
    서술한다.**
  - **선행 조건(preconditions)은 계약의 깨알 글씨 같은 것으로, 후행 조건의 보증이 성립하려면
    충족되어야 하는 조건이다.**
  - **클래스 불변식(class invariants)은 어떤 연산이 끝난 시점의 객체 상태에 대해 단언한다.**
- 그리고 이 소스가 그 어휘에 더하는 자리가 하나 있다 — **불변식은 애그리게이트(AGGREGATE)
  전체에 대해서도 선언될 수 있어, 무결성 규칙을 엄밀하게 정의한다** (10장, p.255).[^evans2003]
  애그리게이트의 원 정의는
  [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있고,
  계약의 세 요소를 다른 소스에서 다루는 자리는
  [계약에 의한 설계](../concepts/design-by-contract.md)다.

## 상태를 서술하기 때문에 쉬워지는 것

- 이 셋의 공통 성질이 값의 출처다 — **이 단언들은 모두 절차가 아니라 상태를 서술하므로 분석하기
  더 쉽다. 클래스 불변식은 클래스의 의미를 특징짓는 데 도움을 주고, 객체를 더 예측 가능하게
  만들어 클라이언트 개발자의 일을 단순하게 한다** (10장, p.256).[^evans2003]
- 위임이 있어도 파고들지 않아도 되는 근거 — **후행 조건의 보증을 신뢰한다면 메서드가 어떻게
  작동하는지 걱정할 필요가 없다. 위임의 효과는 이미 단언에 반영되어 있어야 한다** (10장,
  p.256).[^evans2003]
- 언어 지원이 없어도 사고 도구로 남는다 — **많은 객체지향 언어가 현재 단언을 직접 지원하지
  않지만, 단언은 여전히 설계를 생각하는 강력한 방법이다** (10장, p.256).[^evans2003]
- 자동 단위 테스트가 그 공백을 메우는 기제까지 적힌다 — **단언은 전부 절차가 아니라 상태의
  말로 되어 있기 때문에 테스트를 쓰기 쉽게 만든다. 테스트 준비가 선행 조건을 제자리에 놓고,
  실행 뒤에 테스트가 후행 조건이 성립하는지 확인한다** (10장, p.256).[^evans2003]
  - **여기가 이 페이지에서 가장 실용적인 문장이다.** 단언을 상태로 적어 두면 그것을 테스트로
    옮기는 작업이 기계적이 된다. 준비와 검사 두 자리가 선행 조건과 후행 조건에 그대로 대응한다.

## 조항

- 처방 문단이 둘로 되어 있다. 첫째는 무엇을 적을 것인가다 (10장, p.256):[^evans2003]

> State post-conditions of operations and invariants of classes and AGGREGATES. If ASSERTIONS
> cannot be coded directly in your programming language, write automated unit tests for them.
> Write them into documentation or diagrams where it fits the style of the project's
> development process.

- 둘째가 이 소스를 다른 단언 논의와 가르는 자리다 (10장, p.256):[^evans2003]

> Seek models with coherent sets of concepts, which lead a developer to infer the intended
> ASSERTIONS, accelerating the learning curve and reducing the risk of contradictory code.

  - **모델 자체가 단언을 유추하게 만들라는 요구다.** 단언을 적어 두라는 조항이 아니라, 적지
    않아도 개발자가 같은 것을 떠올리는 모델을 찾으라는 조항이다. 아래 페인트 사례가 이 둘째
    조항이 첫째 조항을 어떻게 뒤집는지를 보인다.

## 사람은 술어를 머릿속에서 컴파일하지 않는다

- 명료한 불변식과 선행·후행 조건은 연산이나 객체를 쓸 때의 결과를 개발자가 이해하게 해 준다
  (10장, p.256).[^evans2003] 그런데 거기서 한 걸음 더 간다 (10장, p.256):[^evans2003]

> Theoretically, any noncontradictory set of assertions would work. But humans don't just
> compile predicates in their heads. They will be extrapolating and interpolating the concepts
> of the model, so it is important to find models that make sense to people as well as
> satisfying the needs of the application.

  - **모순이 없다는 것은 형식적 요건일 뿐 충분 조건이 아니다.** 사람은 단언 목록을 그대로
    들고 있지 않고 모델의 개념에서 바깥으로 늘리고 사이를 메운다. 그래서 형식적으로 일관된
    단언 집합이라도 개념이 어긋나 있으면 사람이 틀린 것을 유추한다.
  - 읽는 사람의 반응을 최종 심급으로 삼는다는 점에서
    [코드는 뻔해야 한다](../concepts/obvious-code.md)와 같은 자리에 선다.

## 어색한 후행 조건이 가리킨 것 — 페인트 혼합

- 앞 절에서 남겨 둔 모호함으로 돌아간다. `Paint` 클래스의 `mixIn(Paint)` 연산이 인자에 무슨
  일을 하는지가 분명하지 않았다 (10장, p.256).[^evans2003]
- 있는 그대로의 후행 조건을 먼저 적는다 — 받는 쪽의 부피가 인자의 부피만큼 늘어난다. 물리적
  페인트에 대한 일반적 이해로 보면 이 혼합 과정은 다른 페인트를 같은 양만큼 축내어 부피 0으로
  비우거나 아예 없애야 한다. 그런데 현재 구현은 인자를 수정하지 않고, 애초에 인자를 수정하는
  것은 특히 위험한 종류의 부수 효과다 (10장, p.257).[^evans2003] 저자가 적은 후행 조건은
  `p1.mixIn(p2)` 뒤에 `p1.volume`이 `p2.volume`만큼 늘고 `p2.volume`은 변하지 않는다는
  것이다 (10장, p.257).[^evans2003]
- 문제는 이 성질이 틀렸다는 것이 아니라 어울리지 않는다는 것이다 — **곤란한 점은 개발자가
  실수를 하리라는 것인데, 이 성질들이 우리가 그들에게 생각하라고 청한 개념에 들어맞지 않기
  때문이다** (10장, p.257).[^evans2003]
- 직설적인 수정안은 다른 페인트의 부피를 0으로 바꾸고 **"혼합으로 페인트의 총 부피는 변하지
  않는다"**는 불변식을 세우는 것이다. 인자를 바꾸는 것은 나쁜 관행이지만 쉽고 직관적이다
  (10장, p.257).[^evans2003]
- **그런데 원래 설계에 이유가 있었다.** 프로그램이 마지막에 **더해진 혼합되지 않은 페인트
  목록을 보고한다**. 이 애플리케이션의 궁극적 목적이 사용자가 어떤 페인트를 혼합에 **넣을지**
  알아내도록 돕는 것이기 때문이다. 그래서 **부피 모델을 논리적으로 일관되게 만들면 그것이
  애플리케이션 요구사항에 맞지 않게 된다** (10장, p.257).[^evans2003]
- 딜레마처럼 보이는 자리에서 저자가 내리는 판정이 이 사례의 요점이다 — 이상한 후행 조건을
  문서화하고 좋은 소통으로 벌충하려는 수밖에 없는가? **세상의 모든 것이 직관적이지는 않고
  때로는 그것이 최선의 답이다. 그러나 이 경우에는 그 어색함이 빠진 개념을 가리키는 것으로
  보인다. 새 모델을 찾아보자** (10장, p.257).[^evans2003]
  - **단언이 여기서 계측기로 쓰인다.** 적어 보니 어색하다는 사실이 모델에 개념이 빠졌다는
    신호가 된다. 어색한 자리를 파고들라는 같은 처방이
    [암묵적 개념 파내기](digging-out-implicit-concepts.md)에 절차로 있다.

## 모델을 바꾸자 단언이 상식이 되었다

- 새 모델을 찾을 때 유리한 조건이 이미 갖춰져 있었다 — 그동안 일어난 지식 정련과 더 깊은
  통찰로의 리팩터링 덕분이다. 색은 이미 값 객체 위의 부수 효과 없는 함수로 계산하므로 **필요할
  때 언제든 계산을 되풀이할 수 있고, 우리는 그것을 이용해야 한다** (10장, p.258).[^evans2003]
- 진단 — **우리는 `Paint`에 두 가지 서로 다른 기본 책임을 주고 있는 것 같다. 그 둘을 갈라
  보자** (10장, p.258).[^evans2003] `Paint`가 추상이 되고 그 아래로 재고 페인트(`Stock Paint`)와
  혼합 페인트(`Mixed Paint`)가 갈린다. `mixIn(Stock Paint)`는 새 페인트를 구성 요소 컬렉션에
  더하기만 하고, `getVolume()`은 구성 요소 부피의 합을, `getColor()`는 구성 요소 색을 섞은
  결과를 돌려준다 (10장, p.258).[^evans2003]
- 그래서 남는 것 — **이제 명령은 `mixIn()` 하나뿐이다. 그것은 컬렉션에 객체를 더할 뿐이고, 그
  효과는 모델을 직관적으로 이해하는 것에서 분명하게 드러난다. 다른 모든 연산은 부수 효과 없는
  함수다** (10장, p.258).[^evans2003]
- 단언 하나를 확인하는 테스트 메서드가 이런 모양이 된다 (10장, p.259):[^evans2003]

  ```java
  public void testMixingVolume {
      PigmentColor yellow = new PigmentColor(0, 50, 0);
      PigmentColor blue = new PigmentColor(0, 0, 50);

      StockPaint paint1 = new StockPaint(1.0, yellow);
      StockPaint paint2 = new StockPaint(1.5, blue);
      MixedPaint mix = new MixedPaint();

      mix.mixIn(paint1);
      mix.mixIn(paint2);
      assertEquals(2.5, mix.getVolume(), 0.01);
  }
  ```

- 사례가 닫히는 문장 — **이 모델은 도메인을 더 많이 포착하고 전달한다. 불변식과 후행 조건이
  상식에 맞고, 그것이 그것들을 유지하고 쓰기 더 쉽게 만들 것이다** (10장, p.259).[^evans2003]
  - **위 조항의 둘째 문단이 여기서 회수된다.** 단언을 더 잘 적어서가 아니라 모델을 바꿔서
    단언이 상식이 되었다.

## 세 패턴이 함께 사 오는 것

- 이 절이 닫히며 앞의 세 패턴을 한 문장으로 묶는다 (10장, p.259):[^evans2003]

> The communicativeness of the INTENTION-REVEALING INTERFACES, combined with the predictability
> given by SIDE-EFFECT-FREE FUNCTIONS and ASSERTIONS, should make encapsulation and abstraction
> safe.

  - 셋이 각각 다른 것을 맡는다. 이름이 무엇을 하는지 말하고, 함수가 그 밖의 일이 없음을
    보장하고, 단언이 남은 명령의 결과를 못 박는다. 그다음 재료가 효과적인 분해라고 예고되는데
    그 자리가 [개념의 윤곽](conceptual-contours.md)이다.
- 이 셋이 갖춰지면 선언적 영역에 들어선다는 판정은
  [선언적 설계](declarative-design.md)에 있다.

## 이어지는 페이지

- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 같은 장의 첫
  패턴. 이 패턴이 "이름만으로는 모자란 자리"라고 지목하는 대상
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 같은 장의 둘째 패턴.
  이 패턴이 다루는 명령의 잔여물을 먼저 줄이는 쪽
- [개념의 윤곽](conceptual-contours.md) — 같은 장의 다음 패턴
- [선언적 설계](declarative-design.md) — 이 셋이 갖춰졌을 때 열리는 스타일
- [계약에 의한 설계](../concepts/design-by-contract.md) — 이 패턴이 인용하는 학파를 다른 소스에서
  다루는 자리
- [단정적 프로그래밍](../concepts/assertive-programming.md) — 같은 낱말을 실행 시점 검사 쪽에서
  쓰는 자리. 이 패턴의 단언은 실행 시점 검사가 아니라 설계의 진술이다
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 불변식이
  걸리는 더 큰 단위
- [코드는 뻔해야 한다](../concepts/obvious-code.md) — 읽는 사람의 유추를 심급으로 삼는 같은 자리
- [자기 테스트 코드](../concepts/self-testing-code.md) — 언어가 단언을 지원하지 않을 때 쓰라는
  자동 테스트가 사는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 10장 "Supple Design" §ASSERTIONS(pp.255–259). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 저자가 대는 앞선 출처는 Meyer 1988이다. 펜스의 Java 코드는 p.259 원문이며,
    추출본에서 눌린 줄바꿈과 들여쓰기를 표준 Java 조판으로 되돌린 것 말고 보탠 줄은 없다.
    원문의 `testMixingVolume` 선언에 괄호가 없는 것도 그대로 두었다. 이 코드는 **2003년
    JUnit의 관용**이라 애너테이션 없이 이름 규약으로 테스트를 표시한다. 클래스 다이어그램
    (Figure 10.9·10.10)은 도판이라 이름과 판정 문장만 옮겼고, Figure 10.10에 딸린 단언
    목록은 산문으로 서술했다.

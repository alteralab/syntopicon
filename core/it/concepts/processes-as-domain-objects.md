---
type: concept
title: 도메인 객체가 된 프로세스
description: 절차를 모델의 전면에 두지 않으면서도 도메인에 실재하는 프로세스를 어떻게 표현하는가 — 객체는 절차를 감싸고 목표를 생각하게 하려고 있다는 전제, 그런데도 도메인에 실재하는 프로세스는 어색한 객체 설계를 부른다는 관찰, 그것을 명시하는 두 형태인 서비스와 전략, 무엇을 명시하고 무엇을 감출지 가르는 한 줄짜리 시험, 그리고 창고 적재기 서비스 인터페이스가 그 시험을 통과한 실물
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 도메인 객체가 된 프로세스

- [절차는 모델의 전면에 두지 않는다](#절차는-모델의-전면에-두지-않는다)
- [명시하는 두 형태 서비스와 전략](#명시하는-두-형태-서비스와-전략)
- [무엇을 명시하고 무엇을 감추는가](#무엇을-명시하고-무엇을-감추는가)
- [창고 적재기 인터페이스](#창고-적재기-인터페이스)
- [전략의 문제 서술과 처방은 12장에 있다](#전략의-문제-서술과-처방은-12장에-있다)
- [제약과 프로세스가 이 장에서 짝을 이루는 이유](#제약과-프로세스가-이-장에서-짝을-이루는-이유)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인에 실재하는 프로세스를 모델에 넣되, 모델이 절차의 나열로 되돌아가지
않게 하려면 어떻게 하는가.**

## 절차는 모델의 전면에 두지 않는다

- 저자가 먼저 오해를 막는다 (9장, p.222):[^evans2003]

> Right up front, let's agree that we do *not* want to make procedures a prominent aspect of our
> model. Objects are meant to encapsulate the procedures and let us think about their goals or
> intentions instead.

- 그러면서도 예외가 있다고 말한다 — **내가 여기서 이야기하는 것은 도메인에 존재하며 우리가
  모델에 표상해야 하는 프로세스다. 이런 것이 떠오르면 그것들은 어색한 객체 설계를 만드는
  경향이 있다** (9장, p.222).[^evans2003]
  - **판별이 존재론에 걸려 있다.** 프로그램을 돌리는 절차인지, 도메인에 실재해서 모델이
    표상해야 하는 프로세스인지가 갈림길이고, 그 갈림길을 재는 시험이 아래에 있다.
- 이 장이 이 범주를 드는 이유가 장 도입에 있다 — 객체 지향 패러다임은 사물과 그 사물이 하는
  행동, 곧 입문서가 말하는 **"명사와 동사"**를 찾게 이끄는데, **모델에서 명시적으로 만들 수
  있는 다른 중요한 개념 범주들이 있다** (9장, p.219).[^evans2003] 저자가 드는 범주는 셋이고,
  **객체로 시작했을 때 나에게 뻔하지 않았던 것들**이라는 단서가 붙는다 (9장,
  p.219).[^evans2003]

## 명시하는 두 형태 서비스와 전략

- 첫째 형태는 서비스다. 이 장 첫 예제의 화물 라우팅이 그 실물이며, **이 라우팅 프로세스는
  업무적 의미를 지닌 무엇이었다** (9장, p.223).[^evans2003] 판정 — **서비스(SERVICE)는 그런
  프로세스를 명시적으로 표현하면서도 극도로 복잡한 알고리즘은 계속 캡슐화하는 한 가지
  방법이다** (9장, p.223).[^evans2003] 이 KB에서 서비스라는 낱말이 층마다 다른 뜻으로 쓰이는
  자리를 정리한 페이지는 [서비스 레이어](../concepts/service-layer-pattern.md)다.
  - **이 패턴의 원 규정은 5장에 있다.** 거기서 서비스는 **상태를 캡슐화하지 않고 모델에서 홀로
    서는 인터페이스로 제공되는 연산**으로 정의되고, 처방은 **도메인의 중요한 프로세스나 변환이
    엔티티나 값 객체의 자연스러운 책임이 아닐 때** 그것을 서비스로 선언하라는 것이다 (5장,
    pp.105–106).[^evans2003] 9장의 이 절은 그 패턴을 **암묵적 프로세스를 명시하는 수단**으로
    다시 부르는 자리다. 전문은 [도메인 서비스](../concepts/domain-services.md)에 있다.
- 둘째 형태는 전략이다 — **프로세스를 수행하는 방법이 둘 이상일 때, 또 하나의 접근은 알고리즘
  자체나 그 핵심 부분을 그 자체로 객체로 만드는 것이다. 프로세스 사이의 선택이 이 객체들
  사이의 선택이 되며, 각 객체는 서로 다른 전략(STRATEGY)을 표상한다** (9장,
  p.223).[^evans2003]
  - 이 소스가 1장에서 초과 예약 규칙을 정책이라 부르며 **정책은 전략이라 알려진 디자인 패턴의
    다른 이름**이라고 적은 자리가 이 형태의 앞선 사례다. 그 사례를 다루는 페이지는
    [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md)이다.

## 무엇을 명시하고 무엇을 감추는가

- 시험이 한 줄로 주어진다 (9장, p.223):[^evans2003]

> The key to distinguishing a process that ought to be made explicit from one that should be
> hidden is simple: Is this something the domain experts talk about, or is it just part of the
> mechanism of the computer program?

- **판정의 심급이 도메인 전문가의 입이다.** 이 시험은 이 장 앞부분의 "말을 들어라"와 같은
  계측기를 쓰며, 그 절차는 [암묵적 개념 파내기](../concepts/digging-out-implicit-concepts.md)에 있다.
- 이 시험이 무엇을 막는지도 함께 읽어야 한다. 프로그램의 기제일 뿐인 절차를 모델에 올리면
  위 첫 문단이 금지한 것, 곧 절차가 모델의 전면에 서는 상태가 된다 (9장,
  p.222).[^evans2003]

## 창고 적재기 인터페이스

- 이 장의 화학 물질 창고 사례가 이 판정의 실물을 보인다. 화학 물질을 규칙에 맞게 용기에
  적재하는 일은 업무 담당자가 이야기하는 프로세스이고, 그 최적화 알고리즘은 프로그램의
  기제다. 그래서 프로세스는 서비스 인터페이스로 명시되고 알고리즘은 그 뒤에 감춰진다 (9장,
  p.238):[^evans2003]

  ```java
  public interface WarehousePacker {
      public void pack(Collection containersToFill, Collection drumsToPack)
              throws NoAnswerFoundException;

      /* ASSERTION: At end of pack(), the ContainerSpecification of
         each Drum shall be satisfied by its Container. If no complete
         solution can be found, an exception shall be thrown.
      */
  }
  ```

- 이 인터페이스가 무엇을 얻어 냈는지가 곧바로 계상된다 — **이제 적재기 서비스의 책임을 수행할
  최적화된 제약 해결기를 설계하는 과제가 애플리케이션의 나머지에서 결합 해제되었고, 그 기제들은
  모델을 표현하는 설계 부분을 어지럽히지 않을 것이다. 그러면서도 적재를 지배하는 규칙은 도메인
  객체에서 빠져나가지 않았다** (9장, p.238).[^evans2003]
  - **규칙과 알고리즘이 갈린 것이 이 절의 요점이다.** 무엇이 안전한 적재인가는 도메인 객체에
    남고, 어떻게 최적으로 적재하는가는 서비스 뒤로 간다. 규칙을 나르는 명세 객체를 다루는
    자리가 [명세 패턴](specification-pattern.md)이다.
- 인터페이스에 단언이 주석으로 붙어 있다는 점도 이 실물의 일부다. 저자는 그 단언을 10장의
  단언(ASSERTION) 사례로 지목하며, 생성기에 넘긴 명세가 그 산출물의 검증으로도 쓰인다는 것을
  그 근거로 든다 (9장, p.235).[^evans2003] 같은 발상을 다른 축에서 다루는 자리는
  [계약에 의한 설계](../concepts/design-by-contract.md)다.

## 전략의 문제 서술과 처방은 12장에 있다

9장은 전략을 이름으로만 부른다. **같은 원전의 12장이 그것을 패턴의 온전한 형식으로 다시
쓴다** — 문제 서술과 처방을 갖추고, 그것이 도메인 패턴이기도 한 근거를 붙여서다.

- 12장이 이 패턴의 두 이름을 함께 세운다. 전략(STRATEGY)이자 정책(POLICY)이다 (12장,
  p.311).[^evans2003]
- 도메인 쪽 문제 서술 (12장, p.311):[^evans2003]

> Domain models contain processes that are not technically motivated but actually meaningful
> in the problem domain. When alternative processes must be provided, the complexity of
> choosing the appropriate process combines with the complexity of the multiple processes
> themselves, and things get out of hand.

  - **이 페이지 첫 절의 "어색한 객체 설계를 만드는 경향"이 여기서 두 겹의 복잡성으로
    분해된다.** 프로세스 자체의 복잡성과 프로세스를 고르는 복잡성이 합쳐지는 것이다.
- 처방 (12장, p.312):[^evans2003]

> Therefore:
> Factor the varying part of a process into a separate "strategy" object in the model. Factor
> apart a rule and the behavior it governs. Implement the rule or substitutable process
> following the STRATEGY design pattern. Multiple versions of the strategy object represent
> different ways the process can be done.

- **그리고 9장이 말하지 않은 것이 12장에 있다** — 기술적 설계 패턴을 이 자리에 쓸 때 강조점이
  어디로 옮겨 가는가다 (12장, p.312):[^evans2003]

> Whereas the conventional view of STRATEGY as a design pattern focuses on the ability to
> substitute different algorithms, its use as a domain pattern focuses on its ability to
> express a concept, usually a process or a policy rule.

  - 전문과 판별 기준은
    [설계 패턴을 도메인 패턴으로 읽기](../concepts/design-patterns-as-domain-patterns.md)에 있다.

## 제약과 프로세스가 이 장에서 짝을 이루는 이유

- 두 범주가 한 문장으로 묶인다 (9장, p.223):[^evans2003]

> Constraints and processes are two broad categories of model concepts that don't come leaping to
> mind when programming in an object-oriented language, yet they can really sharpen up a design
> once we start thinking about them as model elements.

- 그리고 저자는 셋째 범주로 넘어가며 그 폭을 스스로 좁힌다 — **어떤 쓸모 있는 개념 범주들은
  훨씬 좁다. 나는 훨씬 구체적이지만 꽤 흔한 것 하나로 이 장을 마무리하겠다** (9장,
  p.223).[^evans2003] 그 셋째가 [명세 패턴](specification-pattern.md)이다.

## 이어지는 페이지

- [명세 패턴](specification-pattern.md) — 같은 장의 셋째 범주이고, 창고 적재기 사례의 규칙이
  사는 자리
- [설계 패턴을 도메인 패턴으로 읽기](../concepts/design-patterns-as-domain-patterns.md) — 전략이 패턴의
  온전한 형식으로 다시 쓰이는 자리
- [명시적 제약](../concepts/explicit-constraints.md) — 같은 장에서 이 범주와 짝을 이루는 첫째 범주
- [암묵적 개념 파내기](../concepts/digging-out-implicit-concepts.md) — 무엇을 명시할지 가르는 계측기가
  나온 자리
- [도메인 서비스](../concepts/domain-services.md) — 이 패턴의 원 규정과 세 특징
- [서비스 레이어](../concepts/service-layer-pattern.md) — 서비스라는 낱말이 층마다 다르게 쓰이는
  것을 정리한 자리
- [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md) — 정책이 전략이
  되는 초과 예약 사례
- [계층 아키텍처](../concepts/layered-architecture.md) — 이 프로세스가 어느 층에 사는가
- [계약에 의한 설계](../concepts/design-by-contract.md) — 인터페이스에 걸린 단언을 다루는 축
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 9장 "Making Implicit Concepts Explicit" §"How to Model Less Obvious
    Kinds of Concepts" 도입(p.219) · §"Processes as Domain Objects"(pp.222–223) · 12장 "Relating Design
    Patterns to the Model" §STRATEGY (A.K.A. POLICY)(pp.311–312) · 예제
    "Chemical Warehouse Packer"(p.238) · 5장 "A Model Expressed in Software" §SERVICES의
    정의와 처방(pp.105–106). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴
    이름을 작은 대문자로 조판하는 관례를 직인용에서 유지했다. 펜스의 Java 인터페이스는 p.238
    원문이며, 추출본에서 눌린 줄바꿈과 들여쓰기를 표준 Java 조판으로 되돌린 것 말고 보탠 줄은
    없다 — 주석 안의 문장은 원문 그대로다. 이 코드는 **2003년 Java의 관용**이라 제네릭 없는
    원시 타입을 쓴다. 화물 라우팅 프로세스의 코드는 이 절에 없고 앞 예제의 도판으로만
    나오므로 산문으로 서술했다.

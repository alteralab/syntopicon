---
type: concept
title: 격리된 핵심과 추상 핵심
description: 핵심 도메인을 코드 구조에서 직접 드러내는 두 재포장 기법의 원전 — 핵심 요소가 일반 요소와 뒤엉켜 질식한다는 문제와 일반 하위 도메인을 떼어 낸 뒤에도 남는 잔여, 결합이 높은 요소를 갈라놓는 한이 있어도 핵심의 응집을 강화하라는 조항과 다섯 걸음, 관계가 오히려 흐려지고 응집력 있던 모듈이 깨지는 대가와 이 일을 시작할 시점, 핵심의 정의를 얼리지 않으면서 모두가 같은 정의를 쓰게 하는 팀 결정의 조건, 화물 운송 모델을 배송 패키지로 갈라내며 얻은 모델 통찰 둘과 무엇을 핵심에 남길지의 판정, 그리고 모듈 사이 상호작용이 많을 때 수직이 아니라 수평으로 잘라 근본 개념을 별도 모듈에 두는 추상 핵심, 그리고 그 추상 핵심이 16장에서 여러 팀이 공유하는 프레임워크 허브가 될 때 핵심의 지속적 정련이 얼어붙는다는 대가
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 격리된 핵심과 추상 핵심

- [잔여가 핵심을 질식시킨다](#잔여가-핵심을-질식시킨다)
- [조항](#조항)
- [다섯 걸음](#다섯-걸음)
- [대가와 시점](#대가와-시점)
- [얼리지 않으면서 하나로 유지하기](#얼리지-않으면서-하나로-유지하기)
- [사례로 든 화물 운송 모델](#사례로-든-화물-운송-모델)
- [추상 핵심](#추상-핵심)
- [깊은 모델이 증류한다](#깊은-모델이-증류한다)
- [추상 핵심이 프레임워크의 허브가 되는 자리](#추상-핵심이-프레임워크의-허브가-되는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **핵심 도메인을 코드의 구조 자체에서 어떻게 보이게 만드는가.**

두 패턴을 한 페이지에 둔 것은 둘 다 같은 물음에 답하기 때문이다. 격리된 핵심이 수직으로
갈라 핵심 하위 도메인을 별도 모듈로 모으고, 추상 핵심이 수평으로 갈라 근본 개념을 별도 모듈로
모은다. 저자 자신이 뒤의 것을 앞의 것 다음에 오는 더 야심 찬 걸음으로 배열한다.

## 잔여가 핵심을 질식시킨다

- 문제 서술 (15장, p.428):[^evans2003]

> Elements in the model may partially serve the CORE DOMAIN and partially play supporting roles.
> CORE elements may be tightly coupled to generic ones. The conceptual cohesion of the CORE may
> not be strong or visible. All this clutter and entanglement chokes the CORE. Designers can't
> clearly see the most important relationships, leading to a weak design.

- **앞 기법의 한계에서 이 패턴이 나온다** — **일반 하위 도메인을 인수분해해 내면 도메인에서
  시야를 가리는 세부를 얼마간 걷어 내어 핵심을 더 잘 보이게 한다. 그러나 이 하위 도메인들을
  전부 식별하고 명확히 하는 것은 힘든 일이고 그중 일부는 수고할 값어치가 없어 보인다. 한편
  가장 중요한 핵심 도메인은 그 잔여와 뒤엉킨 채 남는다** (15장, p.428).[^evans2003]

## 조항

- 처방 문단 (15장, p.428):[^evans2003]

> Refactor the model to separate the CORE concepts from supporting players (including
> ill-defined ones) and strengthen the cohesion of the CORE while reducing its coupling to
> other code. Factor all generic or supporting elements into other objects and place them into
> other packages, even if this means refactoring the model in ways that separate highly coupled
> elements.

  - **마지막 절이 이 패턴에서 가장 비싼 조항이다.** 결합이 높은 요소를 갈라놓는 한이 있어도
    핵심의 응집을 우선한다.
- 방향이 명시된다 — **이것은 기본적으로 일반 하위 도메인에 적용했던 것과 같은 원리를 반대
  방향에서 적용하는 것이다. 우리 애플리케이션에 중심적인 정합적 하위 도메인들을 식별해 자기
  정합적 패키지로 분할할 수 있다** (15장, p.428).[^evans2003]
- **남는 덩어리의 처리는 덜 중요하다고 명시된다** — **뒤에 남은 미분화 덩어리로 무엇을 하는가는
  중요하지만 그만큼 중요하지는 않다. 그것은 있던 자리에 대체로 그대로 두거나 두드러진 클래스에
  근거해 패키지에 넣을 수 있다. 결국 잔여의 점점 더 많은 부분이 일반 하위 도메인으로 인수분해될
  수 있지만, 단기적으로는 어떤 쉬운 해법이든 괜찮다. 격리된 핵심에 초점이 유지되기만 하면
  된다** (15장, p.428).[^evans2003]

## 다섯 걸음

- 리팩터링의 수순이다 (15장, pp.428–429).[^evans2003]
  1. **핵심 하위 도메인을 식별한다** (증류 문서에서 끌어올 수도 있다).
  2. **관련된 클래스들을 그들을 관계 짓는 개념의 이름을 딴 새 모듈로 옮긴다.**
  3. **그 개념의 직접적 표현이 아닌 데이터와 기능을 끊어 내도록 코드를 리팩터링한다.** 걷어 낸
     측면은 **(아마도 새로운) 다른 패키지의 클래스에 넣는다. 개념적으로 관련된 작업과 함께
     두려 하되 완벽해지려고 너무 많은 시간을 쓰지 마라. 핵심 하위 도메인을 문질러 닦고 거기서
     다른 패키지로 가는 참조를 명시적이고 자기 설명적으로 만드는 데 계속 집중하라.**
  4. **새로 격리된 핵심 모듈을 리팩터링해 그 관계와 상호작용을 더 단순하고 더 소통적으로 만들고,
     다른 모듈과의 관계를 최소화하고 명확히 한다.** 이것은 **계속되는 리팩터링 목표가 된다.**
  5. **격리된 핵심이 완성될 때까지 다른 핵심 하위 도메인으로 되풀이한다.**

## 대가와 시점

- 대가가 둘로 적힌다 (15장, p.429).[^evans2003]
  - **관계가 오히려 흐려질 수 있다** — **핵심을 격리하면 때때로 결합이 높은 비핵심 클래스와의
    관계가 더 모호해지거나 심지어 더 복잡해질 것이다. 그러나 그 비용은 핵심 도메인을 명확히
    하고 그 위에서 일하기 훨씬 쉽게 만드는 이득에 압도된다.**
  - **응집력 있던 모듈이 깨진다** — **모델을 분해하는 의미 있는 방법은 많고, 때때로 격리된
    핵심을 만드는 과정에서 멋지게 응집력 있던 모듈이 깨져 핵심 도메인의 응집성을 끌어내기 위해
    그 응집을 희생하게 된다. 이것은 순이득인데, 엔터프라이즈 소프트웨어의 가장 큰 부가가치가
    모델의 기업 특화된 측면에서 오기 때문이다.**
- **그리고 규모가 정직하게 적힌다** — **다른 비용은 물론 핵심을 격리하는 것이 많은 일이라는
  것이다. 격리된 핵심으로 가는 결정이 잠재적으로 시스템 전역의 변경에 개발자를 흡수하리라는
  것을 인정해야 한다** (15장, p.429).[^evans2003]
- **시점이 조건으로 지정된다** (15장, p.429):[^evans2003]

> The time to chop out a SEGREGATED CORE is when you have a large BOUNDED CONTEXT that is
> critical to the system, but where the essential part of the model is being obscured by a
> great deal of supporting capability.

## 얼리지 않으면서 하나로 유지하기

- 이 결정의 주체가 팀으로 지정된다 — **많은 전략적 설계 결정이 그렇듯 팀 전체가 함께 격리된
  핵심으로 옮겨 가야 한다. 이 걸음은 팀 결정 절차와, 그 결정을 수행할 만큼 규율 있고 조율된
  팀을 요구한다** (15장, p.430).[^evans2003]
- **그런데 요구가 두 방향으로 걸려서 어렵다** (15장, p.430):[^evans2003]

> The challenge is to constrain everyone to use the same definition of the CORE while not
> freezing that decision.

  - 근거 — **핵심 도메인은 설계의 다른 모든 측면과 마찬가지로 진화하기 때문에 격리된 핵심으로
    일해 본 경험이 무엇이 본질적이고 무엇이 보조 요소인가에 대한 새 통찰로 이끈다. 그 통찰은
    핵심 도메인과 격리된 핵심 모듈의 정련된 정의로 되먹여져야 한다** (15장,
    p.430).[^evans2003]
- 그래서 절차에 조건이 붙는다 — **새 통찰이 계속해서 팀과 공유되어야 하지만 개인이나 프로그래밍
  쌍이 그 통찰에 일방적으로 행동할 수는 없다. 합의든 팀 지도자의 지시든 공동 결정 절차가
  무엇이든 반복적인 항로 수정을 할 만큼 민첩해야 한다. 소통은 모두를 핵심에 대한 하나의 관점에
  붙들어 둘 만큼 효과적이어야 한다** (15장, p.430).[^evans2003]
  - 같은 형태의 변경 통지 규칙이 [증류 문서와 강조된 핵심](../concepts/distillation-documents.md)에 있다.

## 사례로 든 화물 운송 모델

- 7장의 해운 모델을 다시 쓰는 예제다 (15장, pp.430–434).[^evans2003] 저자가 먼저 단서를 단다 —
  이 모델은 실제 애플리케이션에 필요할 것에 비해 크게 단순화되어 있고 **현실적인 모델은 예제로
  쓰기에 너무 거추장스럽다. 그러니 이 모델이 전체로 쉽게 해석하고 다루기에 너무 복잡하다고
  상상의 도약을 하라.**
- **출발점의 판정이 어디서 오는지가 이 사례의 첫 교훈이다.** 무엇이 본질인지 찾을 때 **"손익"을
  먼저 보는 것이 보통 좋은 출발점이라 가격과 청구서에 초점을 맞추게 될 수 있다. 그러나 우리는
  정말로 도메인 비전 선언을 봐야 한다** (15장, p.430).[^evans2003] 그 선언에서 인용되는 대목은
  이렇다 (15장, p.430):[^evans2003]

> . . . Increase visibility of operations and provide tools to fulfill customer requirements
> faster and more reliably . . .

- 거기서 판정이 나온다 — **이 애플리케이션은 영업 부서를 위해 설계되고 있지 않다. 회사의 일선
  운영자들이 쓸 것이다. 그러니 돈과 관련된 모든 사안을 (분명 중요하지만) 보조 역할로 강등하자**
  (15장, p.431).[^evans2003] 청구 관련 항목은 이미 누군가 별도 패키지에 넣어 두었으므로 그것을
  유지하되 보조 역할임을 인식한다.
- 초점이 정해진다 — **고객 요구에 따른 화물의 배송, 즉 화물 취급이다.** 이 활동에 가장 직접
  관여하는 클래스를 추출해 **배송(Delivery)이라는 새 패키지에 격리된 핵심**을 만든다 (15장,
  p.431).[^evans2003]
- **대부분은 그냥 옮겨졌지만 모델 자체에 변경이 둘 생겼고 그것이 이 사례의 값이다** (15장,
  pp.431–433).[^evans2003]
  - **고객 합의가 취급 단계를 제약하게 되었다.** 저자는 이것을 **팀이 핵심을 격리할 때 생기기
    마련인 통찰의 전형**이라 부른다 — **효과적이고 올바른 배송에 주의가 집중되면서 고객 합의
    안의 배송 제약이 근본적이고 모델에서 명시적이어야 한다는 것이 분명해진다.**
  - **고객 합의가 고객을 거치지 않고 화물에 직접 붙었다.** 이것은 더 실용적인 변경이다.
    **실제 배송 시점에는 고객이 합의 자체만큼 운영에 관련되지 않는다.** 이전 모델에서는
    **선적에서의 역할에 따라 올바른 고객을 찾아낸 다음 그 고객에게 고객 합의를 물어야 했고,
    이 상호작용이 모델에 대해 하려는 모든 이야기를 막히게 했다.** 새 연관은 **가장 중요한
    시나리오를 최대한 단순하고 직접적으로 만든다.**
- **무엇을 핵심에서 빼는가의 판정 둘이 이어진다** (15장, p.433).[^evans2003]
  - **고객을 뺀다.** 초점이 고객의 요구를 충족하는 데 있으므로 처음에는 고객이 핵심에 속하는
    것처럼 보이지만 **고객 합의를 직접 쓸 수 있게 된 지금 배송 중의 상호작용은 보통 고객
    클래스를 관여시킬 필요가 없다. 그리고 고객의 기본 모델은 꽤 일반적이다.**
  - **구간(Leg)은 남길 근거가 강한데도 뺀다.** 저자가 자기 성향을 밝힌다 — **나는 핵심에서
    최소주의자인 편이고, 구간은 운송 일정·라우팅 서비스·위치와 더 긴밀한 응집을 갖는데 그중
    어느 것도 핵심에 있을 필요가 없었다. 그러나 이 모델에 대해 하고 싶은 이야기의 많은 부분이
    구간을 포함했다면 나는 그것을 배송 패키지로 옮기고 다른 클래스들과 분리되는 어색함을
    감수했을 것이다.**
- **이 예제의 한계도 명시된다** — **이 예제에서는 모든 클래스 정의가 전과 같지만, 흔히 증류는
  클래스 자체를 리팩터링해 일반적 책임과 도메인 특화 책임을 분리할 것을 요구하고 그 다음에야
  격리될 수 있다** (15장, p.433).[^evans2003]
- 뒤따르는 정리도 기록된다. 격리된 핵심이 생기고 나면 남은 해운 패키지는 **"핵심을 빼내고 남은
  모든 것"일 뿐이므로** 더 소통적인 패키징을 위해 리팩터링을 더 할 수 있고, 그 결과 **격리된
  핵심 패키지 하나, 일반 하위 도메인 하나, 그리고 보조 역할의 도메인 특화 패키지 둘**이 된다
  (15장, p.433).[^evans2003] 그 단계가 한 번에 되지 않는다는 단서도 붙는다.
- **맺음이 이 작업의 성격을 규정한다** — **쓸모 있고 의미 있는 모듈을 알아보는 것은 모델링
  활동이다. 개발자와 도메인 전문가가 지식 정련 과정의 일부로 전략적 증류에서 협력한다** (15장,
  p.434).[^evans2003] 모듈이 모델링 활동이라는 조항은
  [도메인의 모듈](../concepts/modules-in-the-domain.md)에, 정련은
  [지식 정련](../concepts/knowledge-crunching.md)에 있다.

## 추상 핵심

- 문제가 앞 패턴 다음 층위에서 시작한다 — **핵심 도메인 모델조차 보통 세부가 너무 많아 큰
  그림을 전달하기 어려울 수 있다** (15장, p.435).[^evans2003]
- **통상적인 분할이 역효과를 내는 자리가 지목된다** — 큰 모델은 보통 파악할 만큼 좁은 하위
  도메인으로 쪼개 별도 모듈에 두고 **이 환원적 패키징 스타일은 흔히 복잡한 모델을 다루기 쉽게
  만든다. 그러나 때때로 별도 모듈을 만드는 것이 하위 도메인 사이의 상호작용을 흐리거나 심지어
  복잡하게 만들 수 있다** (15장, p.435).[^evans2003]
- 문제 서술 (15장, p.435):[^evans2003]

> When there is a lot of interaction between subdomains in separate MODULES, either many
> references will have to be created between MODULES, which defeats much of the value of the
> partitioning, or the interaction will have to be made indirect, which makes the model obscure.

- 해법의 발상이 한 낱말로 제시된다 — **수직이 아니라 수평으로 자르는 것을 고려하라** (15장,
  p.435).[^evans2003] 근거는 다형성이다 — **다형성은 추상 타입의 인스턴스 사이의 자세한 변이
  많은 부분을 무시할 힘을 준다. 모듈을 가로지르는 상호작용 대부분이 다형적 인터페이스 수준에서
  표현될 수 있다면 이 타입들을 특별한 핵심 모듈로 리팩터링하는 것이 말이 될 수 있다** (15장,
  p.435).[^evans2003]
- **그러나 기술적 요령으로 오해되지 않게 조건이 붙는다** (15장, p.435):[^evans2003]

> We are not looking for a technical trick here. This is a valuable technique only when the
> polymorphic interfaces correspond to fundamental concepts in the domain.

  - 그 조건이 만족될 때 **이 추상들을 분리하는 것은 모듈들을 결합 해제하면서 더 작고 더
    응집력 있는 핵심 도메인을 증류한다.**
- 처방 문단 (15장, p.436):[^evans2003]

> Identify the most fundamental concepts in the model and factor them into distinct classes,
> abstract classes, or interfaces. Design this abstract model so that it expresses most of the
> interaction between significant components. Place this abstract overall model in its own
> MODULE, while the specialized, detailed implementation classes are left in their own MODULES
> defined by subdomain.

- 결과의 모양 — **특화된 클래스 대부분이 이제 추상 핵심 모듈을 참조하되 다른 특화된 모듈은
  참조하지 않게 된다. 추상 핵심은 주요 개념과 그 상호작용의 간명한 관점을 준다** (15장,
  p.436).[^evans2003]
- **기계적으로 할 수 없다는 경고가 명시적이다** — **추상 핵심을 인수분해하는 과정은 기계적이지
  않다. 예를 들어 모듈을 가로질러 자주 참조되는 모든 클래스를 자동으로 별도 모듈로 옮기면
  결과는 무의미한 난장판이 되기 쉽다** (15장, p.436).[^evans2003] 필요한 것은 **핵심 개념과
  그것들이 시스템의 주요 상호작용에서 하는 역할에 대한 깊은 이해**이고, 그래서 **이것은 더 깊은
  통찰을 향한 리팩터링의 한 예이며 보통 상당한 재설계를 요구한다** (15장, p.436).[^evans2003]
- **두 증류 기법이 만나는 자리가 적힌다** — **추상 핵심은 증류 문서와 아주 비슷해 보이는 것으로
  끝나야 한다(둘 다 같은 프로젝트에서 쓰였고 증류 문서가 통찰이 깊어짐에 따라 애플리케이션과
  함께 진화했다면). 물론 추상 핵심은 코드로 쓰일 것이고 따라서 더 엄격하고 더 완전하다** (15장,
  p.436).[^evans2003]

## 깊은 모델이 증류한다

- 이 장이 닫히면서 증류의 범위가 넓혀진다 — **증류는 도메인의 부분들을 핵심에서 떼어 내는 거친
  수준에서만 작동하지 않는다. 그것은 또한 그 하위 도메인들을, 특히 핵심 도메인을 더 깊은 통찰을
  향해 계속 리팩터링함으로써 정련하는 것을 뜻하며, 깊은 모델과 유연한 설계를 향해 몰아간다**
  (15장, p.436).[^evans2003]
- 목표가 한 문장으로 적힌다 (15장, p.436):[^evans2003]

> The goal is a design that makes the model obvious, a model that expresses the domain simply.
> A deep model distills the most essential aspects of a domain into simple elements that can be
> combined to solve the important problems of the application.

- **그리고 돌파의 위치가 핵심으로 지목된다** — **깊은 모델로의 돌파는 어디서 일어나든 값을
  제공하지만, 프로젝트 전체의 궤적을 바꿀 수 있는 것은 핵심 도메인에서다** (15장,
  p.437).[^evans2003] 그 사건의 성질은 [깊은 모델과 돌파](../concepts/deep-model.md)에 있다.

## 추상 핵심이 프레임워크의 허브가 되는 자리

16장의 [플러그인 컴포넌트 프레임워크](../concepts/pluggable-component-framework.md)는 **이 페이지의 추상
핵심을 선행 조건으로 조항 안에 넣는다.**

- 처방 (16장, p.475):[^evans2003]

> Distill an ABSTRACT CORE of interfaces and interactions and create a framework that allows
> diverse implementations of those interfaces to be freely substituted. Likewise, allow any
> application to use those components, so long as it operates strictly through the interfaces of
> the ABSTRACT CORE.

- 배치가 명시된다 — **고수준 추상이 식별되어 시스템 전역에 공유되고, 특화는 모듈에서 일어난다.
  애플리케이션의 중앙 허브는 공유 커널 안의 추상 핵심이다** (16장, pp.475–476).[^evans2003]
  - 위 [추상 핵심](#추상-핵심)이 한 프로젝트 안의 모듈 배치였다면, 여기서는 **여러 팀과 여러
    애플리케이션이 공유하는 계약**이 된다.
- **그 확대의 대가가 이 페이지에 없던 것이다** (16장, p.476):[^evans2003]

> Developers can specialize the model, but they can't change the ABSTRACT CORE without changing
> the protocol of all the diverse components. As a result, the process of continuous refinement of
> the CORE, refactoring toward deeper insight, is more or less frozen in its tracks.

  - 위 [얼리지 않으면서 하나로 유지하기](#얼리지-않으면서-하나로-유지하기)가 팀 안에서 풀려던
    문제 — 핵심의 정의를 얼리지 않는 것 — 가 여러 팀 규모에서는 **실제로 얼어붙는다**는 기록이다.
- 그래서 순서 조항이 붙는다 — **플러그인 컴포넌트 프레임워크는 프로젝트에 적용하는 첫 번째
  대규모 구조여서도, 두 번째여서도 안 된다. 가장 성공적인 예들은 여러 특화된 애플리케이션이
  완전히 개발된 다음에 뒤따랐다** (16장, p.476).[^evans2003]
- 일반 하위 도메인이 구조 안에서 자리를 잡는 방식도 같은 장에 있다 — **플러그인 컴포넌트에서는
  일반 하위 도메인을 한 컴포넌트가 통째로 소유하거나 관련 컴포넌트 집합의 공유 커널로 둘 수
  있다** (16장, p.483).[^evans2003]

## 이어지는 페이지

- [핵심 도메인](../concepts/core-domain.md) — 이 기법들이 드러내려는 대상
- [일반 하위 도메인](../concepts/generic-subdomains.md) — 같은 원리를 반대 방향에서 적용한 형제
- [플러그인 컴포넌트 프레임워크](../concepts/pluggable-component-framework.md) — 추상 핵심을 여러 팀의
  계약으로 확대하는 구조와 그 대가
- [대규모 구조](../concepts/large-scale-structure.md) — 그 구조가 속한 층위
- [정합적 기제](../concepts/cohesive-mechanisms.md) — 이 기법 앞에 오는 잔여 줄이기
- [증류 문서와 강조된 핵심](../concepts/distillation-documents.md) — 코드를 고치지 않는 대응물
- [도메인의 모듈](../concepts/modules-in-the-domain.md) — 이 재포장이 따르는 조항
- [깊은 모델과 돌파](../concepts/deep-model.md) — 증류가 도착하려는 곳
- [화물 운송 예제](../concepts/cargo-shipping-example.md) — 같은 모델이 처음 세워지는 자리
- [지식 정련](../concepts/knowledge-crunching.md) — 이 작업이 속한 활동
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §PLUGGABLE COMPONENT FRAMEWORK
    (pp.475–476)과 §"Distillation Lightens the Load"(p.483) ·
    15장 "Distillation" §SEGREGATED CORE(pp.428–434) —
    §"The Costs of Creating a SEGREGATED CORE"(p.429) · §"Evolving Team Decision"(p.430) ·
    예제 "Segregating the CORE of a Cargo Shipping Model"(pp.430–434) 포함 ·
    §ABSTRACT CORE(pp.435–436) · §"Deep Models Distill"(pp.436–437). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 패턴 도비라의 사진(pp.428·435)과 클래스 다이어그램 셋(Figure 15.2–15.4 —
    출발 모델, 배송 패키지로 갈라낸 모델, 비핵심을 다시 패키징한 모델)은 도판이라 옮기지
    않았고 딸린 판정 산문과 패키지 이름만 옮겼다. 이 절들에는 코드 목록이 없다.

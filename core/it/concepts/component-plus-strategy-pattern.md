---
type: concept
title: Component + Strategy 패턴
description: 포트와 어댑터를 특수 경우로 품는 일반형을 그 원저자 콕번이 2022년에 규정한 원전 — 객체를 함수 인수로 넘기는 평범한 설계가 매개변수화·Strategy·Required Interface·의존성 주입을 한꺼번에 구현한다는 웜업, UML의 Component(제공/요구 인터페이스와 포트를 갖고 환경에 갈아 끼울 수 있는 모듈 단위, 몇 겹으로든 중첩 가능)와 Strategy(같은 호출에 응하는 후보 중 하나를 문맥이 손에 쥔다)를 합쳐 하위 체계를 조금씩 다른 환경에 맞추는 패턴이라는 규정, 어댑터가 Strategy의 특수 경우(한 겹 더한 간접)라 이름을 Component + Adapter가 아니라 더 일반적인 Component + Strategy로 삼은 근거, 포트와 어댑터가 그 일반형에서 경계를 기술 바로 앞에 두어 기술 변화로부터 지키는 특수 경우이며 그래서 중첩하지 않는 반면 일반형은 중첩하도록 설계됐다는 핵심 차이, 조각들을 서로 소개하는 숨은 넷째 객체 Configurator, 그리고 "컴포넌트"라 부르는 한 경계마다 시험을 써야 진짜 컴포넌트라는 못
generated: { by: "claude-opus-4.8", at: "2026-09-25T00:00:00Z" }
sources:
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
---

# Component + Strategy 패턴

- [이 페이지가 담는 것](#이-페이지가-담는-것)
- [웜업 — 평범한 설계가 담은 다섯 낱말](#웜업--평범한-설계가-담은-다섯-낱말)
- [Component와 포트](#component와-포트)
- [Strategy, Adapter, 아니면 둘 다](#strategy-adapter-아니면-둘-다)
- [패턴 — Component + Strategy](#패턴--component--strategy)
- [포트와 어댑터는 그 특수 경우다](#포트와-어댑터는-그-특수-경우다)
- [숨은 넷째 객체 — Configurator](#숨은-넷째-객체--configurator)
- [시험이 컴포넌트를 실재하게 만든다](#시험이-컴포넌트를-실재하게-만든다)
- [이어지는 페이지](#이어지는-페이지)

## 이 페이지가 담는 것

[포트와 어댑터 규정](ports-and-adapters-defined.md)이 이 패턴의 규정을,
[포트와 어댑터와 이웃 개념](ports-and-adapters-related-concepts.md)이 5장에서 그 이웃 개념들과의
관계를 담는다. 그 5장은 포트와 어댑터를 **더 일반적인 한 패턴의 특수 경우**로 여러 번 가리키되,
그 일반형의 규정은 6장으로 미뤄 두었다 — 경계 컨텍스트가 언제 포트와 어댑터가 되는가(5.6), 부패
방지 계층이 언제 어댑터가 되는가(5.7), 헥사고날은 중첩하지 않지만 그 일반형은 중첩한다는 것(5.8)이
모두 이 일반형에 기대어 답한 것이다. 이 페이지가 그 일반형 **Component + Strategy**를 담는다 —
콕번(Alistair Cockburn)이 2022년에 쓴 후속 아티클을 2024년 책이 6장에 원문 그대로 재수록한 것이며,
그 사실을 이 페이지도 각주로 밝힌다.

이 일반형이 서는 자리를 저자가 한 문장으로 규정한다 (6장 §"6.4. Component + Strategy generalizes
Ports & Adapters"):[^cockburn2024]

> _Component + Strategy_ allows you to configure a subsystem to fit into slightly different
> environments. _Hexagonal_ _Architecture_ aka _Ports & Adapters_ is a specific version of it that
> allows you to isolate a system from external technologies, vary those external technologies, and
> test the system in isolation from those technologies.

- 즉 Component + Strategy는 하위 체계를 조금씩 다른 환경에 맞추도록 설정하게 하는 것이고, 포트와
  어댑터는 그 일반형의 특정 판 — 외부 기술로부터 체계를 격리하고, 그 외부 기술을 갈아 끼우고,
  그것들 없이 체계를 시험하게 하는 판이다. 저자는 이 자리에서 2022년에야 포트와 어댑터가 UML과
  패턴 문헌 속 어디에 놓이는지를 봤다고 밝힌다.

## 웜업 — 평범한 설계가 담은 다섯 낱말

- 저자는 아주 평범한 설계 하나에서 출발한다 — 함수가 인수로 받은 객체에게 더 물어보거나 무언가를
  시키려고 그 객체를 인수로 넘기는 것이다. 커피 머신에 레시피 객체를 넘겨 음료 제조기가 그것에서
  재료 순서를 얻게 하는 것이 그 예다 (6장 §"6.4...", "Warmup").[^cockburn2024]
- 그런데 이 평범한 한 동작이 실은 다섯 개념을 한꺼번에 구현한다는 것이 웜업의 요지다
  (6장 §"6.4...", "Warmup"):[^cockburn2024]
  - **매개변수화된 협력자(parameterized collaborator)** — 어느 것을 쓸지 인수로 고른다. 저자는
    이것을 "피구동 액터를 매개변수화한다"는 말로 뒤에서 다시 쓴다.
  - **Strategy 패턴** — 많은 프로그래머가 의식하지 않고 쓰지만 그것이 곧 Strategy다.
  - **요구 인터페이스(Required Interface)** — 제조기가 자기 인수 협력자에게 걸 호출을 선언하고,
    협력자는 그것을 구현해야 한다.
  - **의존성 주입(Dependency Injection)** — Configurable Receiver의 구현 가능성 가운데 하나다.
  - **Configurable Receiver** — 위 넷을 아우르는 이름이다.
- 이렇게 넘겨받은 덕분에 제조기는 프로그래밍 시점에 그 다른 객체들을 전혀 모른다 — **코드 수준의
  의존이 없고, 필요한 지식은 전부 실행 중에 얻는다.** 저자는 유지보수·시험·재사용의 관점에서 이것을
  좋아한다고 적는다 (6장 §"6.4...", "Warmup").[^cockburn2024] 이 페이지가 담는 나머지는 이 평범한
  동작에 정확한 이름을 붙이는 일이다.

## Component와 포트

- 저자는 2022년에야 UML에 **Component**라는 것이 있음을 발견했다고 적는다 — 구동 쪽에 제공
  인터페이스(API)를, 협력자 쪽에 요구 인터페이스를 갖고, **포트(Port)** — 컴포넌트에 꽂히는 무엇이든
  어떤 프로토콜을 지켜야 한다는 요구 — 를 갖는 것이다 (6장 §"6.4...", "Introducing components and
  ports").[^cockburn2024] UML 명세의 규정을 그대로 옮긴다:

  > The UML spec says a Component is, "a modular unit with well-defined Interfaces that is
  > replaceable within its environment."
  >
  > "A Component specifies a formal contract of the services that it provides to its clients and
  > those that it requires from other Components or services in the system in terms of its provided
  > and required Interfaces."

  - 즉 컴포넌트는 잘 정의된 인터페이스를 가져 자기 환경에서 갈아 끼울 수 있는 모듈 단위이고,
    자기가 클라이언트에게 제공하는 서비스와 다른 컴포넌트·서비스에 요구하는 서비스를 제공·요구
    인터페이스로 정식 계약한다.
- 이 규정에서 이 페이지의 핵심 갈림이 나온다 — **컴포넌트는 몇 겹으로든 중첩할 수 있다**
  (6장 §"6.4...", "Introducing components and ports"):[^cockburn2024]

  > A key property of components that is relevant to this article is that they can be nested -
  > components inside of components - at any number of levels.

  - 컴포넌트 안에 컴포넌트를 두어 개별 컴포넌트와 다른 하위 체계로부터 하위 체계를 지을 수 있다.
    저자는 곧바로 이것을 포트와 어댑터와 대비한다 — **포트와 어댑터(헥사고날)는 중첩하지 않으며,
    이것이 둘의 핵심 차이가 될 것이라 예고한다.** 헥사고날이 중첩하지 않는다는 판정은
    [포트와 어댑터 규정](ports-and-adapters-defined.md)의 "필수와 선택과 패턴 밖"과
    [포트와 어댑터와 이웃 개념](ports-and-adapters-related-concepts.md)의 중첩 헥사곤 물음(5.8)에
    이미 있고, 그 까닭을 이 일반형이 채운다.

## Strategy, Adapter, 아니면 둘 다

- 어댑터와 Strategy의 관계를 저자가 못 박는다 (6장 §"6.4...", "Strategy, Adapter, or
  both?"):[^cockburn2024]

  > The _Adapter_ pattern is a special case of the _Strategy_ pattern in which the concrete strategy
  > will make some adjustments for interface compatibility and then call another service to take care
  > of the request. The big difference between the two is that _Adapter_ has an additional level of
  > indirection.

  - 어댑터는 Strategy의 특수 경우다 — 구체 전략이 인터페이스 호환을 위해 얼마간 조정한 뒤 다른
    서비스를 불러 요청을 처리하는 판이며, 둘의 큰 차이는 어댑터가 간접 한 겹을 더 둔다는 것이다.
    Strategy는 자기 일을 다 해도 되지만, 어댑터는 다른 것에 잇기를 기대받는다.
- 그래서 저자는 이 아티클의 패턴을 **Component + Strategy**라 부른다 — 이름을 Component + Adapter가
  아니라 이렇게 정한 까닭은 **Strategy가 둘 중 더 일반적**이기 때문이다 (6장 §"6.4...", "Strategy,
  Adapter, or both?"·"The Pattern: Component + Strategy").[^cockburn2024] 이 어댑터=Strategy의 특수
  경우라는 관계는 시험 대역이 Strategy인가 어댑터인가라는 5.4의 물음과 이어진다 — 저자는 대역이
  시험용 데이터베이스에 잇지 않으면 Strategy, 잇으면 어댑터로 볼 수 있으나 그 구분에 다툴 값어치가
  없다고 적는다.

## 패턴 — Component + Strategy

- 패턴의 규정은 앞의 한 문장을 되풀이한다 — **Component + Strategy는 하위 체계를 조금씩 다른 환경에
  맞추도록 설정하게 한다.** 저자는 이것을 컴포넌트 다이어그램(패키징 요소)과 클래스 다이어그램(모델링
  요소) 둘로 함께 보인다 — 패키징 요소에 모델링 요소를 이었기 때문이다 (6장 §"6.4...", "The Pattern:
  Component + Strategy").[^cockburn2024]
- 이 패턴이 주는 것이 격리 시험이다 — **컴포넌트 경계를 명시적으로 선언함으로써, 외부 액터 하나에
  대해 시험 대역을 Strategy로 넣어 컴포넌트를 격리해 시험할 수 있고, 프로덕션에서는 어댑터를 넣어
  실제 연결을 맺는다** (6장 §"6.4...", "The Pattern: Component + Strategy").[^cockburn2024]

## 포트와 어댑터는 그 특수 경우다

- 이 페이지의 결론 명제를 저자가 규정한다 — **포트와 어댑터(헥사고날)는 컴포넌트 경계를 외부 기술
  바로 앞에 둔 Component + Strategy의 특정 사용이며, 각 포트의 제공·요구 인터페이스에 맞추도록 어댑터
  객체를 공급한 것**이다 (6장 §"6.4...", "Ports & Adapters (Hexagonal Architecture)
  revisited").[^cockburn2024] 인터페이스가 호환되는 직접 모듈-대-모듈 상호작용에서는 어댑터가 필요
  없을 수 있다는 단서도 붙는다 — 이것은 [포트와 어댑터 규정](ports-and-adapters-defined.md)의
  "어댑터가 늘 필요한 것은 아니다"와 같은 말이다.
- 그리고 둘의 핵심 차이를 저자가 못 박는다 (6장 §"6.4...", "Ports & Adapters ...
  revisited"):[^cockburn2024]

  > One of the differences between the two patterns is that a key intention of _Ports & Adapters_ is
  > to protect against external technology changes. Hence, its boundary is placed only at the
  > technology boundary. It is not nestable, unlike _Component + Strategy_, which is designed to be
  > nested.

  - 포트와 어댑터의 핵심 의도는 외부 기술 변화로부터 지키는 것이라, 경계를 **오직 기술 경계에만**
    둔다. 그래서 **중첩하지 않는다** — 반면 Component + Strategy는 중첩하도록 설계됐다. 이 한 문장이
    5.8("헥사고날은 중첩하지 않으나 그 일반형은 중첩한다")의 근거이고, 헥사곤 안에 헥사곤을 겹으로
    쌓는 것이 왜 이 패턴의 오용인지를 규정한다.
- 맺음에서 저자가 둘의 관계를 다시 한 문장으로 정리한다 (6장 §"6.4...", "End
  Notes"):[^cockburn2024]

  > The difference between _Component + Strategy_ and _Ports & Adapters_ or _Hexagonal Architecture_
  > is that _Ports & Adapters_ is aimed at solving one very specific problem - changing external
  > technologies (and testing) - whereas _Component + Strategy_ is intended as a general
  > subsystem-bounding effort.

  - 포트와 어댑터는 외부 기술 교체(와 시험)라는 아주 특정한 한 문제를 겨냥하고, Component +
    Strategy는 임의의 코드 하위 구획을 시험 벽으로 지키고 환경에 맞춰 설정하는 일반적 수단이다.

## 숨은 넷째 객체 — Configurator

- 앞의 모든 다이어그램이 한 물음을 건너뛰었다고 저자가 짚는다 — **이 객체들은 서로를 어떻게 알게
  되는가.** Strategy도, Component + Strategy도, 포트와 어댑터도 이 물음을 패턴 밖으로 둔다
  (6장 §"6.4...", "The Hidden Fourth Object, the Configurator").[^cockburn2024]
- 그러나 언젠가는 모든 참가자를 알고 서로를 소개하는 모듈이나 코드가 있어야 하며, **소스 코드 의존이
  바로 거기에 놓인다. 이것이 Configurator 객체**다 (6장 §"6.4...", "The Hidden Fourth Object, the
  Configurator").[^cockburn2024] 시스템 수준 시험에서는 각 시험 케이스 안에 Configurator가 있어 시험
  하네스·시험 대역·컴포넌트를 인스턴스화하고 서로 잇고, 프로덕션에서는 프로그램 빌드와 시작 모듈이
  같은 인스턴스화를 맡는다. 이 Configurator라는 요소가 [포트와 어댑터 규정](ports-and-adapters-defined.md)의
  "다섯째 요소 Configurator"와 같은 것이며, 그것을 실제로 채우는 주입·조회 수단의 규정은
  [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md)에 있다.

## 시험이 컴포넌트를 실재하게 만든다

- 저자가 이 패턴을 세운 실무 동기가 시험이다 — 포트와 어댑터나 헥사고날을 구현했다면서 양쪽에 시험이
  없는 것을 보면 피가 얼어붙는다고 적는다 (6장 §"6.4...", "Tests or no tests?").[^cockburn2024]
- 그가 UML의 Component를 좋아하는 한 이유가 이름 자체에 있다 — **'컴포넌트'라는 낱말을 쓰는 것만으로
  모든 경계에 시험을 써야 한다는 의무감을 느껴야 한다. 컴포넌트라 불리는 것이고, 다른 체계와 상황에
  놓이도록 의도된 것이니, 선언된 경계에는 당연히 시험이 있어야 한다** (6장 §"6.4...", "Tests or no
  tests?").[^cockburn2024] 헥사고날을 여러 겹으로 두면 안쪽 헥사곤 경계 시험과 체계 시험 사이 중복이
  너무 커져 팀이 안쪽 시험을 결국 안 쓰게 되고, 그 순간 그것은 더는 진짜 컴포넌트가 아니게 된다.
- 그래서 저자는 포트와 어댑터를 **바깥 기술 경계에** 두어야 한다고 못 박는다 — 그 경계에서라야 시험이
  유지할 값어치가 있는 뜻있는 체계 시험이 되고, 애플리케이션이 의도한 뜻에서 컴포넌트가 되어 제대로
  된 회귀 시험을 갖는다 (6장 §"6.4...", "Tests or no tests?").[^cockburn2024] 경계를 실재하게 만드는
  것이 시험이라는 이 판정은 [포트와 어댑터와 이웃 개념](ports-and-adapters-related-concepts.md)의
  부패 방지 계층 물음(5.7)에서 되풀이된다.

## 이어지는 페이지

- [포트와 어댑터 규정](ports-and-adapters-defined.md) — 이 일반형이 특수화되는 그 패턴의 규정
- [포트와 어댑터와 이웃 개념](ports-and-adapters-related-concepts.md) — 이 일반형에 기대어 경계
  컨텍스트·부패 방지 계층·중첩을 답하는 5장
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — Configurator 역할을
  채우는 주입·조회 수단이 사는 자리
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 요구 인터페이스가 지키는 원리
- [헥사고날 아키텍처](../synthesis/hexagonal-architecture.md) — 이 축의 허브

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 6장 §"6.4. The article: "Component + Strategy
    generalizes Ports & Adapters"" — 2022년 아티클(HaT Technical Report 2022.01)의 원문 재수록.
    인용한 내부 절은 "Warmup" · "Introducing components and ports" · "Strategy, Adapter, or both?" ·
    "The Pattern: Component + Strategy" · "Ports & Adapters (Hexagonal Architecture) revisited" ·
    "The Hidden Fourth Object, the Configurator" · "Tests or no tests?" · "End Notes". 그림
    6.7~6.22의 내용은 본문 서술이 담으므로 이미지를 열지 않았다. 아티클 안의 커피 머신·drinkmaker
    코드 조각과 Spring Configurator 코드는 산문으로만 옮기고 펜스는 쓰지 않았다(코드 정본은
    3장 [코드로 본 포트와 어댑터](ports-and-adapters-in-code.md)). EPUB(Calibre 변환본), 쪽 앵커
    없음 — locator는 장·절 번호.

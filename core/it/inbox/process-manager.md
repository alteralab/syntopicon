---
type: concept
title: 프로세스 매니저
description: 업무 로직에 기반한 프로세스를 중앙에서 들고 다음 단계를 정하는 패턴과 그것이 사가와 갈리는 자리 — 사가가 이벤트와 명령을 짝지을 뿐이라는 규정과 if-else가 들어오면 이미 프로세스 매니저라는 어림법, 사가는 이벤트 하나에 암묵적으로 생기고 프로세스 매니저는 명시적으로 만들어져야 한다는 둘째 차이, 출장 예약 사례와 촉발할 중앙 개체가 없다는 판정, 상태 기반이나 이벤트 소싱 애그리게이트로 구현되며 명시적 식별자와 영속 상태를 갖는다는 배치와 명령을 아웃박스 릴레이에 넘기는 흐름, 그리고 이 이름이 2003년 기업 통합 패턴에서 온 것이고 저자가 그 출처를 스스로 대는 자리, 그리고 넷째 소스가 같은 물건을 중재자라 부르며 워크플로마다 하나여야 한다는 조건을 붙이는 자리와 그 소스의 프런트 컨트롤러가 이것이 아닌 이유
status: draft
generated: { by: "claude-opus-5", at: "2026-09-18T02:30:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: hohpe2004, resource: /it/sources/hohpe2004.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 프로세스 매니저

- [사가는 짝짓기만 한다](#사가는-짝짓기만-한다)
- [정의](#정의)
- [어림법 — if-else가 보이면 이미 프로세스 매니저다](#어림법--if-else가-보이면-이미-프로세스-매니저다)
- [둘째 차이 — 누가 인스턴스를 만드는가](#둘째-차이--누가-인스턴스를-만드는가)
- [사례 — 출장 예약](#사례--출장-예약)
- [구현은 애그리게이트다](#구현은-애그리게이트다)
- [이 이름의 원전](#이-이름의-원전)
- [셋째 소스의 오케스트레이터는 이것인가](#셋째-소스의-오케스트레이터는-이것인가)
- [넷째 소스의 중재자와 프런트 컨트롤러](#넷째-소스의-중재자와-프런트-컨트롤러)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **여러 단계로 된 업무 프로세스가 중간 결과에 따라 갈라질 때 그 흐름을 누가 들고
있는가.**

## 사가는 짝짓기만 한다

- 구별이 사가의 범위를 좁히는 것에서 시작한다 (9장, p.150):[^khononov2021]

> The saga pattern manages simple, linear flow. Strictly speaking, a saga matches events to the
> corresponding commands.

- 저자가 앞 절의 예제를 되짚어 그것이 실제로 짝짓기였음을 보인다 — `CampaignActivated` 이벤트가
  `PublishingService.SubmitAdvertisement` 명령으로, `PublishingConfirmed`가
  `Campaign.TrackConfirmation`으로, `PublishingRejected`가 `Campaign.TrackRejection`으로
  대응한 것이 전부다 (9장, p.150).[^khononov2021]
  - 그 예제의 전문은 [사가 패턴](saga-pattern.md)에 있다.

## 정의

- 규정이 두 문장이다 (9장, p.151):[^khononov2021]

> The process manager pattern, shown in Figure 9-14, is intended to implement a business-logic-based
> process. It is defined as a central processing unit that maintains the state of the sequence and
> determines the next processing steps.

  - **"업무 로직에 기반한(business-logic-based)"이 구별의 축이다.** 사가에는 로직이 없고 대응
    표만 있다. 프로세스 매니저에는 무엇을 다음에 할지 정하는 판단이 있다.
  - 역어 — 이 KB는 *process manager*를 **프로세스 매니저**로 음차한다. 이 이름이 이미 들어와
    있는 [복합 라우팅 패턴](../concepts/composed-routing-patterns.md)이 원어 표기를 그대로
    쓰므로, 두 자리가 같은 검색 키를 공유하도록 원어를 병기한다.

## 어림법 — if-else가 보이면 이미 프로세스 매니저다

- 판별 규칙이 한 문장으로 주어진다 (9장, p.151):[^khononov2021]

> As a simple rule of thumb, if a saga contains if-else statements to choose the correct course of
> action, it is probably a process manager.

  - **이 어림법이 이 페이지의 실무 값이다.** 두 패턴의 구현이 닮았으므로 이름을 먼저 고르기가
    어려운데, 이미 쓴 코드를 보고 뒤늦게 판별할 수 있는 신호를 준다.

## 둘째 차이 — 누가 인스턴스를 만드는가

- 차이가 하나 더 적힌다 (9장, p.151):[^khononov2021]

> Another difference between a process manager and a saga is that a saga is instantiated implicitly
> when a particular event is observed, as in CampaignActivated in the preceding examples. A process
> manager, on the other hand, cannot be bound to a single source event. Instead, it's a coherent
> business process consisting of multiple steps. Hence, a process manager has to be instantiated
> explicitly.

  - **이 차이가 첫째 차이에서 따라 나온다.** 사가가 이벤트 하나에 매이는 것은 그것이 그
    이벤트에 대한 반응이기 때문이고, 프로세스 매니저가 매이지 못하는 것은 그것이 어떤 반응이
    아니라 프로세스 자체이기 때문이다.

## 사례 — 출장 예약

- 저자가 드는 흐름은 이렇다 — 출장 예약은 경로 알고리즘이 가장 비용 효율적인 항공 경로를 골라
  직원에게 승인을 구하는 것으로 시작한다. 직원이 다른 경로를 원하면 그의 직속 관리자가 승인해야
  한다. 항공편이 예약된 뒤에는 사전 승인된 호텔 중 하나를 해당 날짜에 예약해야 한다. 이용 가능한
  호텔이 없으면 항공권을 취소해야 한다 (9장, p.151).[^khononov2021]
- 판정이 한 문장이다 (9장, p.151):[^khononov2021]

> In this example, there is no central entity to trigger the trip booking process. The trip booking
> is the process and it has to be implemented as a process manager

  - **"촉발할 중앙 개체가 없다"가 판정의 근거다.** 앞 절의 사가에는 `Campaign` 애그리게이트가
    있었고 그것이 낸 이벤트가 사가를 깨웠다. 출장 예약에는 그런 주인이 없다.
  - **호텔이 없을 때 항공권을 취소하는 것이 보상 행동이다.** 그 어휘는 사가와 같고, 다른 것은
    그 취소가 갈림의 한쪽 가지로 들어 있다는 것이다.

## 구현은 애그리게이트다

- 배치가 명시된다 (9장, p.152):[^khononov2021]

> From an implementation perspective, process managers are often implemented as aggregates, either
> state based or event sourced.

- 예제의 앞부분이 이것이다. 필드 목록이 예약할 출장을 서술하고, `Initialize`가 경로를 계산해
  이벤트 둘을 자기 목록에 붙인다 (9장, pp.152–153):[^khononov2021]

  ```csharp
  public class BookingProcessManager
  {
      private readonly IList<IDomainEvent> _events;
      private BookingId _id;
      private Destination _destination;
      private TripDefinition _parameters;
      private EmployeeId _traveler;
      private Route _route;
      private IList<Route> _rejectedRoutes;
      private IRoutingService _routing;
      ...
  
      public void Initialize(Destination destination,
                             TripDefinition parameters,
                             EmployeeId traveler)
      {
          _destination = destination;
          _parameters = parameters;
          _traveler = traveler;
          _route = _routing.Calculate(destination, parameters);
  
          var routeGenerated = new RouteGeneratedEvent(
              BookingId: _id,
              Route: _route);
  
          var commandIssuedEvent = new CommandIssuedEvent(
              command: new RequestEmployeeApproval(_traveler, _route)
          );
  
          _events.Append(routeGenerated);
          _events.Append(commandIssuedEvent);
      }
  ```

- 저자가 이 코드에서 읽어 내는 것 셋 (9장, p.154):[^khononov2021]
  - **프로세스 매니저는 자기 명시적 ID와, 예약되어야 할 출장을 서술하는 영속 상태를 갖는다.**
    사가와 갈리는 자리가 여기서 코드로 드러난다 — 위
    [둘째 차이](#둘째-차이--누가-인스턴스를-만드는가)의 "명시적으로 만들어져야 한다"가
    `Initialize` 메서드와 `_id` 필드다.
  - **앞의 사가 예제처럼 워크플로를 통제하는 이벤트들(`RouteConfirmed`·`RouteRejected`·
    `ReroutingConfirmed` 등)을 구독한다.**
  - **`CommandIssuedEvent` 타입의 이벤트를 만들어 내고, 그것을 아웃박스 릴레이가 처리해 실제
    명령을 실행한다.** 그 기제는 [아웃박스 패턴](../concepts/outbox-pattern.md)에 있다.
- 이 장의 맺음이 두 패턴을 한 문장으로 가른다 — **사가 패턴은 단순한 구성 요소 사이 업무
  프로세스를 구현하는 데 쓸 수 있고, 더 복잡한 업무 프로세스는 프로세스 매니저 패턴으로 구현할
  수 있다. 두 패턴 모두 도메인 이벤트에 대한 비동기 반응과 명령의 발행에 기댄다** (9장,
  p.154).[^khononov2021]

## 이 이름의 원전

- **저자가 정의에 각주를 달아 출처를 댄다** — Gregor Hohpe & Bobby Woolf, *Enterprise
  Integration Patterns: Designing, Building, and Deploying Messaging Solutions*(Addison-Wesley,
  2003)다 (9장, p.151, 각주 2).[^khononov2021]
  - **그 책은 이 KB에 이미 들어와 있다.** 같은 이름의 패턴이 사는 자리가
    [복합 라우팅 패턴 §Process Manager](../concepts/composed-routing-patterns.md)이고,
    거기 실린 원전의 처방이 이 판본의 정의와 같은 대상을 가리킨다 — **중앙 처리 단위인
    *Process Manager*를 써서 시퀀스의 상태를 유지하고 중간 결과에 기반해 다음 처리 단계를
    정하라** (7장, p.313).[^hohpe2004]
- **두 서술의 분업은 이렇다.** 원전 쪽이 훨씬 두껍고, 이 판본은 거기서 정의만 빌려 와 사가와의
  구별에 쓴다.

| 이 페이지(2021) | [복합 라우팅 패턴](../concepts/composed-routing-patterns.md)(2003) |
|---|---|
| 사가와 무엇이 다른가 — 로직의 유무, 인스턴스 생성의 방식 | *Routing Slip*과 무엇이 다른가 — 단계가 미리 정해지는가, 선형인가 |
| 구현 = 도메인 모델의 애그리게이트(상태 기반이나 이벤트 소싱) | 구현 = 통합 미들웨어의 프로세스 엔진. 프로세스 정의와 프로세스 인스턴스, 상관 식별자, BPEL4WS |
| 명령 실행은 아웃박스 릴레이에 넘긴다 | 중앙 지점이 병목이자 실패 지점이라는 대가와 그 완화(영속화·병렬 엔진) |
| 촉발할 중앙 개체가 없을 때 고른다 | 허브 앤 스포크로 갈지 분산 파이프와 필터로 갈지의 선택 | 

- **같은 이름이 같은 대상을 가리키는지 검토했고, 그렇다고 판정했다.** 근거는 저자가 원전을
  직접 인용한다는 것과 두 정의가 "중앙에서 시퀀스의 상태를 유지하고 다음 단계를 정한다"로
  일치한다는 것이다. **모순 쌍으로 세우지 않았다.** 다만 저자가 옮겨 놓은 자리가 다르다 —
  원전에서 이것은 통합 인프라의 구성 요소이고, 이 판본에서는 도메인 모델 안의 애그리게이트다.
  그 차이는 위 표의 둘째 줄에 적었다.

## 셋째 소스의 오케스트레이터는 이것인가

- [newman2021](../sources/newman2021.md) 6장은 사가의 구현 방식 둘 중 하나를 **오케스트레이션된
  사가**라 부르고, 그 중앙 조율자를 **오케스트레이터(orchestrator)**라 이름 붙인다 (6장
  §"Orchestrated sagas", p.189).[^newman2021] **그 오케스트레이터가 이 페이지의 프로세스
  매니저와 같은 것인가를 대질했다.**
- 대질의 재료는 넷이다.

| 물음 | 프로세스 매니저(khononov2021) | 오케스트레이터(newman2021) |
|---|---|---|
| 다음 단계를 정하는 판단이 있는가 | **정의의 축이다** — 업무 로직에 기반한 프로세스 | **있다** — 어떤 서비스가 필요한지 알고 **언제 호출할지 결정하며**, 호출이 실패하면 **그 결과로 무엇을 할지 결정한다** (6장, p.190) |
| 영속 상태를 갖는가 | **갖는다** — 명시적 ID와 시퀀스 상태 | 사가가 어느 상태인지에 대한 **가시성이 오케스트레이션의 이득으로 꼽힌다**(코레오그래피에는 없는 것) (6장, pp.189·193) |
| 명시적으로 만들어지는가 | **그래야 한다** — 원천 이벤트 하나에 매이지 못한다 | 흐름마다 다른 서비스가 그 역할을 맡는다 — `Order Processor`·`Returns`·`Goods Receiving` (6장, p.191) |
| 구현의 자리 | 도메인 모델의 애그리게이트 | **마이크로서비스 하나** |

- **판정: 같은 종류의 물건이고, 놓이는 층이 다르다.** 네 물음 중 셋(판단·상태·명시적 생성)에서
  newman의 오케스트레이터는 khononov의 프로세스 매니저 쪽 답을 낸다. **판단이 있다는 것이
  결정적이다** — khononov의 어림법(if-else가 보이면 프로세스 매니저다)으로 재면, 실패 시
  무엇을 할지 결정하는 오케스트레이터는 사가가 아니라 프로세스 매니저다.
- **그런데 이름이 어긋난다.** newman은 그것을 **사가의 구현 방식**이라 부르고 khononov은 **사가와
  구별되는 다른 패턴**이라 부른다. 이것은 두 소스가 "사가"라는 낱말의 외연을 다르게 잡기
  때문이고, 사실 주장이 겨루는 것이 아니다. 그 어휘 대조는
  [사가 패턴 §두 소스가 사가라는 낱말을 다른 대상에 쓴다](saga-pattern.md)에
  표로 있다. **모순 쌍(`contradicts`)을 걸지 않았다.**
- **합치지 않은 이유 하나가 더 있다** — 이 페이지의 프로세스 매니저는 **경계 컨텍스트 안의
  도메인 모델 구성 요소**이고 newman의 오케스트레이터는 **독립 배포되는 마이크로서비스**다.
  이 이름의 원전(hohpe2004)에서 그것이 **통합 미들웨어의 프로세스 엔진**이었던 것까지 세면
  같은 발상이 세 층에 놓여 있는 셈이고, 위 [이 이름의 원전](#이-이름의-원전)의 표에 적은 층
  구분이 여기에 한 칸 더 늘어난 것이다.
- **newman이 이 배치에 대고 내는 경고 둘은 이 페이지에도 그대로 걸린다** (6장,
  pp.190–191):[^newman2021]
  - **도메인 결합이 높아진다** — 조율자가 관련 서비스를 전부 알아야 한다.
  - **서비스로 밀어 넣어야 할 로직이 조율자에 흡수돼 서비스가 빈혈 상태가 될 수 있다** —
    로직을 중앙집중할 자리가 있으면 중앙집중된다.
  - 완화책도 같은 모양이다 — **흐름마다 다른 조율자를 두어** 한 조율자가 모든 것을 알지
    않게 한다. 그 전문은 [사가 패턴 §구현 둘](saga-pattern.md)에 있다.

## 넷째 소스의 중재자와 프런트 컨트롤러

**[ford2021-hard-parts](../sources/ford2021-hard-parts.md) 11장이 같은 물건에 이름을 둘 더
붙이고, 그 가운데 하나만 이 페이지의 패턴과 같은 것이다.**

- **오케스트레이터(= 중재자)는 같은 것이다** (11장, p.301):[^ford2021-hard-parts]

  > The *orchestration pattern* uses an *orchestrator* (sometimes called a *mediator*) compo-
  > nent to manage workflow state, optional behavior, error handling, notification, and a
  > host of other workflow maintenance.

  - **워크플로 상태와 오류 처리가 정의에 들어 있으므로 판단이 있다.** 위
    [어림법 — if-else가 보이면 이미 프로세스 매니저다](#어림법--if-else가-보이면-이미-프로세스-매니저다)로
    재면 이것은 프로세스 매니저 쪽이다. **위
    [셋째 소스의 오케스트레이터는 이것인가](#셋째-소스의-오케스트레이터는-이것인가)가 뉴먼에 대해
    내린 판정이 이 소스에도 그대로 걸린다** — **같은 종류의 물건이고 놓이는 층이 다르다.**
  - **그쪽이 더하는 조건이 하나 있다** — **마이크로서비스 아키텍처는 워크플로마다 오케스트레이터를
    두지, ESB 같은 전역 오케스트레이터를 두지 않는다.** 근거는 **전역 컴포넌트가 바람직하지 않은
    결합 지점을 만든다**는 것이다 (11장, pp.301–302).[^ford2021-hard-parts] 뉴먼도 흐름마다
    다른 조율자를 두라고 적는데 **근거가 다르다** — 뉴먼은 로직이 중앙집중될 자리를 없애려는
    것이고, 이쪽은 전역 결합 지점을 피하려는 것이다.
  - **그리고 그쪽이 오케스트레이터에 도메인 행위를 넣지 말라고 적는다** — **오케스트레이터
    컴포넌트는 자기가 중재하는 워크플로 밖의 도메인 행위를 일반적으로 포함하지 않는다** (11장,
    p.301).[^ford2021-hard-parts] 뉴먼의 **빈혈 서비스** 경고와 같은 방향을 반대쪽에서 적은
    것이다.
- **프런트 컨트롤러는 이 패턴이 아니다.** 그쪽이 코레오그래피에서 워크플로 상태를 두는 첫째
  선택지로 드는 것인데, **책임 연쇄의 첫 서비스에 상태의 책임만 얹는다** (11장,
  p.311).[^ford2021-hard-parts]

| 물음 | 이 페이지의 프로세스 매니저 | 그쪽의 프런트 컨트롤러 |
|---|---|---|
| 워크플로 상태를 갖는가 | **갖는다** | **갖는다** |
| **다음 단계를 정하는 판단이 있는가** | **있다. 정의의 축이다** | **없다.** 흐름은 서비스들이 서로 이어받는다 |
| 무엇으로 구현되는가 | 도메인 모델의 애그리게이트 | **연쇄의 첫 도메인 서비스** — 도메인 행위에 상태가 얹힌다 |
| 저자 자신의 이름 | 프로세스 매니저 | **코레오그래피 안의 유사 오케스트레이터**(`pseudo-orchestrator`, 표 11-2) |

  - **판정: 다른 것이다.** 상태를 갖는다는 점만 같고 판단이 없다. 이 페이지의 어림법이 그
    가름을 그대로 해 준다. **`contradicts`를 걸 자리가 아니다** — 두 소스가 다른 물건에 다른
    이름을 붙였을 뿐이다.
  - **그래서 같은 발상이 이제 네 층에 놓인다** — 통합 미들웨어의 프로세스 엔진(hohpe2004),
    도메인 모델의 애그리게이트(khononov2021), 독립 배포되는 마이크로서비스(newman2021과
    ford2021-hard-parts의 오케스트레이터), 그리고 **도메인 서비스에 상태만 얹은
    것**(ford2021-hard-parts의 프런트 컨트롤러)이다. **네 소스 가운데 어느 쪽도 이 네 층을 함께
    적지 않는다.** #hypothesis
- 두 스타일의 전문과 절충표 여덟은
  [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)에 있다.

## 이어지는 페이지

- [사가 패턴](saga-pattern.md) — 이 패턴과 자주 혼동되는 쪽. 흐름이 단순하고 선형일 때
- [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md) — 같은 물건을 중재자라
  부르고 그것을 두지 않는 쪽의 절충까지 세는 자리
- [아웃박스 패턴](../concepts/outbox-pattern.md) — 이 패턴이 낸 명령이 실제로 실행되는 기제
- [복합 라우팅 패턴](../concepts/composed-routing-patterns.md) — 이 이름의 원전이 사는 자리
- [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md) — 이 패턴의 두 구현 형태 중 하나
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 이 패턴이
  스스로 그 안에 드는 경계
- [도메인 이벤트](../concepts/domain-events.md) — 이 패턴이 듣고 내는 것
- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) — 같은 발상이 데이터 파이프라인
  쪽에서 스케줄러와 갈리는 자리
- [메시징 패턴](../synthesis/messaging-patterns.md) — 원전 이름 층의 허브
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 9장 "Communication Patterns" §"Integrating Aggregates" 중
    §"Process Manager"(pp.150–154)와 §Conclusion(p.154). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다.
    정의 인용의 끝에 붙은 본문 각주 번호 표지("steps.2")는 떼고 옮겼다 — 그 각주의 내용은 위
    [이 이름의 원전](#이-이름의-원전)에 따로 적었다. 도판 둘(Figure 9-14 프로세스 매니저 ·
    9-15 출장 예약 프로세스 매니저)은 도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다.
    **코드 목록 하나(`BookingProcessManager`, pp.152–154) 중 펜스로 옮긴 것은 필드 목록과
    `Initialize`까지의 앞부분이고**, 뒤따르는 `Process` 메서드 넷(`RouteConfirmed`·
    `RouteRejected`·`ReroutingConfirmed`·`FlightBooked`)은 산문으로 줄였다 — 같은 모양의
    반복이고 개념당 대표 펜스 하나 규약을 따랐다. 원문 목록은 쪽 넘김 지점에서 들여쓰기가
    어긋나 있어(같은 메서드 안에서 기준이 두 번 바뀐다) **들여쓰기만 일관되게 폈고 줄과 토큰은
    원문 그대로다.** 세 점(`...`)은 저자가 생략을 표시한 것이고 이 KB가 깎은 것이 아니다.
    언어 표지(`csharp`)만 더했다. 장 끝 연습문제(pp.154–155)는 claim이 아니라 옮기지 않았다.

[^hohpe2004]: Hohpe & Woolf 2004, 7장 "Message Routing" §"Process Manager"(pp.312–321). 이
    각주는 대조를 위해 기존 페이지의 인용을 그대로 옮겨 온 것이고, 그 전문은
    [복합 라우팅 패턴](../concepts/composed-routing-patterns.md)에 있다.

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 11장 "Managing Distributed
    Workflows" §"Orchestration Communication Style"(pp.301–302)과
    §"Choreography Communication Style" 중 §"Workflow State Management"(pp.311–312, 표 11-2).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용 하나(오케스트레이션 패턴의 규정)는
    `pdftotext -layout` 추출로 문자 단위 대조했고 원문이 이탤릭으로 조판한 낱말은 인용 안에서
    이탤릭을 유지했으며, 원문이 지면 폭 때문에 낱말을 끊어 조판한 자리(`compo-nent`)는 끊긴
    그대로 두었다. 두 스타일의 나머지 직인용과 절충표 여덟은
    [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)가 갖는다. 그 절들의
    도판(그림 11-3·11-13)은 재현하지 않고 본문이 그 도판에 대해 적는 것만 옮겼으며, 그 장에
    코드 목록은 없다. 위 대질표와 같은 발상이 네 층에 놓인다는 셈은 원문에 없고 이 KB가 세운
    것이며 네 소스는 이 자리에서 서로를 호명하지 않는다.

[^newman2021]: Newman 2021, 6장 "Workflow" §"Implementing Sagas" 중 §"Orchestrated
    sagas"(pp.189–191)와 §"Choreographed sagas"(pp.192–194)에서 대질에 필요한 대목만 들었다.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 이 절의 직인용은 0건이고 — 대질 표의 칸은 전부
    한국어 재서술이다 — 그 절들의 직인용과 전문은
    [사가 패턴](saga-pattern.md)에 있다. 도판 둘(Figure 6-9 오케스트레이션된 사가 ·
    6-10 코레오그래피된 사가)은 이미지로 조판돼 있어 본문이 그것에 대해 적는 것만 옮겼다.

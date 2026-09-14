---
type: concept
title: 이벤트 소싱 도메인 모델
description: 애그리게이트의 상태를 저장하는 대신 상태 변화를 도메인 이벤트로만 적고 그것을 정본으로 삼는 업무 로직 구현 패턴 — 도메인 모델 패턴과 같은 전제·같은 구성 단위를 쓰되 영속화 방식만 다르다는 규정, 이벤트를 싣고 상태를 투영하고 명령을 실행하고 새 이벤트를 커밋하는 네 단계의 각본, 애그리게이트가 자기 상태를 직접 바꾸지 않고 이벤트를 덧붙인다는 구현의 뒤집힘, 저자가 "이벤트 소싱"이 아니라 더 긴 이름을 쓰는 이유, 시간 여행·깊은 통찰·감사 로그·정교한 낙관적 동시성이라는 이점 넷과 학습 곡선·모델 진화·아키텍처 복잡성이라는 비용 셋, 그리고 이 패턴이 맞는 자리, 그리고 9장이 여는 둘째 쓰임 — 상태를 관리해야 하는 사가와 프로세스 매니저가 이 패턴으로 구현되어 받은 이벤트와 낸 명령의 이력을 남긴다는 배치, 그리고 11장이 더하는 이행 — 이미 상태를 저장하는 애그리게이트를 이 패턴으로 옮길 때 사라진 과거를 어떻게 다루는가의 두 길, 곧 상태에서 그럴듯한 이벤트 스트림을 만들어 내되 전이의 완전한 이력은 복구할 수 없음을 감수하는 길과 마이그레이션 이벤트 하나로 지식의 부재를 명시하되 레거시의 흔적이 이벤트 저장소에 영구히 남는 길
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 이벤트 소싱 도메인 모델

- [도메인 모델 패턴과 무엇이 같고 무엇이 다른가](#도메인-모델-패턴과-무엇이-같고-무엇이-다른가)
- [네 단계의 각본](#네-단계의-각본)
- [구현이 뒤집히는 자리](#구현이-뒤집히는-자리)
- [버전 필드와 시간 여행](#버전-필드와-시간-여행)
- [왜 그냥 "이벤트 소싱"이 아닌가](#왜-그냥-이벤트-소싱이-아닌가)
- [이점 넷](#이점-넷)
- [비용 셋](#비용-셋)
- [이 패턴이 맞는 자리](#이-패턴이-맞는-자리)
- [9장이 이 패턴의 둘째 쓰임을 연다](#9장이-이-패턴의-둘째-쓰임을-연다)
- [이미 돌아가는 도메인 모델을 여기로 옮기기](#이미-돌아가는-도메인-모델을-여기로-옮기기)
- [길 하나 과거 전이를 만들어 낸다](#길-하나-과거-전이를-만들어-낸다)
- [길 둘 마이그레이션 이벤트를 모델링한다](#길-둘-마이그레이션-이벤트를-모델링한다)
- [책의 사례 — 이 패턴이 도착점이 된 두 번과 쓸 자리가 아니었던 한 번](#책의-사례--이-패턴이-도착점이-된-두-번과-쓸-자리가-아니었던-한-번)
- [이 페이지가 다루지 않는 것](#이-페이지가-다루지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애그리게이트의 상태를 저장하지 않고 상태 변화만 이벤트로 적으면 도메인 모델
구현이 무엇이 달라지는가.**

## 도메인 모델 패턴과 무엇이 같고 무엇이 다른가

- [khononov2021](../sources/khononov2021.md)이 이 패턴을 앞 장의 패턴에서 파생시킨다 —
  **이벤트 소싱 도메인 모델 패턴은 도메인 모델 패턴과 같은 전제 위에 선다. 여기서도 업무
  로직이 복잡하고 핵심 하위 도메인에 속한다. 게다가 도메인 모델과 같은 전술 패턴들 — 값 객체,
  애그리게이트, 도메인 이벤트 — 을 쓴다** (7장, p.99).[^khononov2021]
- 그러므로 갈리는 것은 **영속화 방식 하나**다 (7장, p.99):[^khononov2021]

> The difference between these implementation patterns lies in the way the aggregates' state is
> persisted. The event-sourced domain model uses the event sourcing pattern to manage the
> aggregates' states: instead of persisting an aggregate's state, the model generates domain
> events describing each change and uses them as the source of truth for the aggregate's data.

- 두 모델의 차이를 이벤트 발행의 관점에서 다시 적은 문단이 이 패턴의 정의다
  (7장 §"Event-Sourced Domain Model", p.108):[^khononov2021]

> The original domain model maintains a state representation of its aggregates and emits select
> domain events. The event-sourced domain model uses domain events exclusively for modeling the
> aggregates' lifecycles. All changes to an aggregate's state have to be expressed as domain
> events.

  - **"select"과 "exclusively"가 대비의 전부다.** 앞 장의 애그리게이트도 도메인 이벤트를
    내지만 **골라서** 내고 상태는 따로 저장한다. 이 패턴에서는 상태 변화가 **빠짐없이**
    이벤트여야 하고 상태는 저장되지 않는다. 앞 장의 배치는
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)와
    [도메인 이벤트](domain-events.md)에 있다.
- 그래서 이 패턴은 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)의
  넷째 자리에 선다 — 트랜잭션 스크립트·액티브 레코드·도메인 모델 다음이고, 셋 중 마지막의
  변종이지 대체가 아니다.

## 네 단계의 각본

- 이 패턴에서 애그리게이트 위의 연산이 따르는 절차가 고정되어 있다
  (7장 §"Event-Sourced Domain Model", p.108):[^khononov2021]

> Each operation on an event-sourced aggregate follows this script:

  1. **Load the aggregate's domain events.**
  2. **Reconstitute a state representation—project the events into a state representation that
     can be used to make business decisions.**
  3. **Execute the aggregate's command to execute the business logic, and consequently, produce
     new domain events.**
  4. **Commit the new domain events to the event store.**

- 6장의 티켓 애그리게이트를 이 패턴으로 옮기면 그 네 단계가 애플리케이션 서비스에 그대로
  드러난다 — 이벤트를 싣고, 애그리게이트 인스턴스를 되살리고(rehydrate), 해당 명령을 부르고,
  변경을 데이터베이스에 되돌려 저장한다 (7장, p.108).[^khononov2021] 원문의 목록이 그
  네 줄을 한눈에 보인다:

  ```csharp
  public class TicketAPI
  {
      private ITicketsRepository _ticketsRepository;
      ...

      public void RequestEscalation(TicketId id, EscalationReason reason)
      {
          var events = _ticketsRepository.LoadEvents(id);
          var ticket = new Ticket(events);
          var originalVersion = ticket.Version;
          var cmd = new RequestEscalation(reason);
          ticket.Execute(cmd);
          _ticketsRepository.CommitChanges(ticket, originalVersion);
      }

      ...
  }
  ```

  - `originalVersion`을 명령 실행 **전에** 붙잡아 커밋에 함께 넘기는 것이 낙관적 동시성
    관리의 자리다. 이벤트 저장소가 그 값을 무엇에 쓰는지는
    [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)의 이벤트 저장소 절에 있다.

## 구현이 뒤집히는 자리

- 애그리게이트의 생성자가 상태 투영기(state projector)를 만들고 이벤트마다 그 투영 로직을
  부른다 — 티켓의 경우 `TicketState` 인스턴스를 세우고 실린 이벤트마다 `AppendEvent`를
  차례로 호출한다 (7장, p.109).[^khononov2021] `AppendEvent`는 들어온 이벤트를 자기 이벤트
  컬렉션에 덧붙이고 같은 이벤트를 투영 로직에 넘겨 **메모리 안의 현재 상태 표현**을 만든다.
- **명령 메서드가 상태를 직접 건드리지 않는 것이 앞 장과의 가장 눈에 띄는 차이다** —
  **앞 장에서 본 구현과 달리 이벤트 소싱 애그리게이트의 `RequestEscalation` 메서드는
  `IsEscalated` 플래그를 명시적으로 참으로 설정하지 않는다. 대신 해당 이벤트를 만들어
  `AppendEvent` 메서드에 넘긴다** (7장, p.109).[^khononov2021]
- 상태가 실제로 바뀌는 자리는 투영 클래스뿐이다 — **애그리게이트의 이벤트 컬렉션에 더해진
  모든 이벤트가 `TicketState` 클래스의 상태 투영 로직으로 넘어가고, 거기서 해당 필드들의
  값이 이벤트의 데이터에 따라 변이된다** (7장, p.110).[^khononov2021]
  - **그래서 업무 규칙을 읽는 자리와 쓰는 자리가 갈린다.** 명령 메서드는 투영된 상태를
    **읽어** 판정하고(`if (!_state.IsEscalated && _state.RemainingTimePercentage <= 0)`),
    상태를 **쓰는** 것은 이벤트별 `Apply` 오버로드뿐이다. #hypothesis 저자가 이 분업을
    한 문장으로 명시한 대목은 없고, 근거는 위 두 인용과 코드 목록의 모양이다.

## 버전 필드와 시간 여행

- 투영 로직이 이벤트마다 증가시키는 필드 하나가 이 패턴의 계측기다 — **각 이벤트를 적용한
  뒤 증가하는 Version 필드에 주목하라. 그 값은 업무 엔티티에 가해진 수정의 총 횟수를
  나타낸다** (7장, p.104).[^khononov2021]
- 그리고 **이벤트의 부분집합만 적용하면 "시간을 여행할" 수 있다** — **엔티티의 상태를 그
  생애의 어느 시점으로든 투영할 수 있다. 관련된 이벤트만 적용하면 된다. 예컨대 버전 5의
  엔티티 상태가 필요하면 처음 다섯 이벤트만 적용하면 된다** (7장, p.104).[^khononov2021]
- 투영이 하나로 고정되지도 않는다 — 같은 이벤트 열에서 검색용 모델(이름·전화번호의 **역사적
  값까지** 집합으로 모은 것)과 분석용 모델(후속 통화 횟수를 세는 것)을 각각 투영하는 예가
  이어진다 (7장 §Search·§Analysis, pp.104–106).[^khononov2021] 그 투영들을 실제
  데이터베이스에 물질화하는 방법이 [CQRS 아키텍처](cqrs-architecture.md)다.

## 왜 그냥 "이벤트 소싱"이 아닌가

- 저자가 이름을 길게 쓰는 이유를 곁글로 밝힌다 (7장 §Why "Event-Sourced Domain
  Model"?, p.110):[^khononov2021]

> Using events to represent state transitions—the event sourcing pattern—is possible with or
> without the domain model's building blocks. Therefore, I prefer the longer term to explicitly
> state that we are using event sourcing to represent changes in the lifecycles of the domain
> model's aggregates.

  - **이 구별이 이 페이지와 이웃 페이지의 경계를 긋는다.** 이벤트 소싱이라는 데이터 모델
    자체는 [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)가 갖고, 이 페이지는
    그것을 **애그리게이트의 생애에 적용한 업무 로직 구현 패턴**만 갖는다.

## 이점 넷

전통적 모델과 견주면 **애그리게이트를 모델링하는 데 더 많은 노력이 든다**고 먼저 적은 뒤
이점 넷을 든다 (7장 §Advantages, pp.110–111).[^khononov2021]

- **시간 여행**(time travelling) — **도메인 이벤트가 애그리게이트의 현재 상태를 복원하는 데
  쓰일 수 있는 것과 꼭 마찬가지로, 애그리게이트의 과거 상태 전부를 복원하는 데도 쓰일 수
  있다. 달리 말해 애그리게이트의 과거 상태를 언제나 전부 재구성할 수 있다.**
  쓰임이 둘로 적힌다 — 시스템의 행동을 분석하고 시스템의 결정을 들여다보고 업무 로직을
  최적화할 때, 그리고 **소급 디버깅(retroactive debugging)**이다 — **버그가 관측된 그 순간의
  정확한 상태로 애그리게이트를 되돌릴 수 있다.**
- **깊은 통찰**(deep insight) — **이벤트 소싱은 시스템의 상태와 행동에 대한 깊은 통찰을
  제공한다.** 근거는 유연한 모델이다 — **기존 이벤트의 데이터를 활용해 추가 통찰을 주는 새
  투영을 언제든 더할 수 있다.** 저자가 이 이점을 I부와 잇는다 — 핵심 하위 도메인의 최적화가
  전략적으로 중요하다는 것이 그 근거다. 그 판정은
  [핵심 도메인](../concepts/core-domain.md)에 있다.
- **감사 로그**(audit log) (7장, p.111):[^khononov2021]

  > The persisted domain events represent a strongly consistent audit log of everything that has
  > happened to the aggregates' states. Laws oblige some business domains to implement such audit
  > logs, and event sourcing provides this out of the box.

  - 저자가 특히 맞는 자리로 **돈이나 금전 거래를 관리하는 시스템**을 든다 — 시스템의 결정과
    계좌 사이 자금의 흐름을 쉽게 추적할 수 있기 때문이다. 감사 가능성 일반의 논의는
    [감사와 무결성 검사](../concepts/auditing-and-integrity-checking.md)에 있다.
- **정교한 낙관적 동시성 관리**(advanced optimistic concurrency management) — 고전적 모델은
  읽은 데이터가 쓰는 사이에 다른 프로세스에 덮여 낡아지면 예외를 던질 뿐이다. 이 패턴은 더
  할 수 있다 (7장, p.111):[^khononov2021]

  > When using event sourcing, we can gain deeper insight into exactly what has happened between
  > reading the existing events and writing the new ones. You can query the exact events that were
  > concurrently appended to the event store and make a business domain–driven decision as to
  > whether the new events collide with the attempted operation or the additional events are
  > irrelevant and it's safe to proceed.

  - **충돌 판정이 기술 판정에서 업무 판정으로 옮겨 가는 것이 이 항목의 요점이다.** 같은
    낙관적 동시성 제어를 버전 필드 하나로 하는 앞 장의 방식은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있고,
    일반 이론은 [동시성 제어 분류](../concepts/concurrency-control-classification.md)에 있다.

## 비용 셋

이점만 보면 언제나 써야 할 패턴처럼 보이지만 **그것은 업무 도메인의 필요가 설계 결정을 이끌게
한다는 원칙에 어긋난다**고 저자가 못 박고 비용 셋을 든다
(7장 §Disadvantages, pp.111–112).[^khononov2021]

- **학습 곡선**(learning curve) — 전통적 데이터 관리 기법과 날카롭게 다르다는 것이 이 패턴의
  분명한 단점이다. **팀에 이벤트 소싱 시스템 구현 경험이 이미 있지 않다면 학습 곡선을 계상해야
  한다.**
- **모델의 진화**(evolving the model) (7장, p.112):[^khononov2021]

  > The strict definition of event sourcing says that events are immutable. But what if you need to
  > adjust the event's schema? The process is not as simple as changing a table's schema.

  - 저자가 이 주제 하나만으로 책 한 권이 쓰였다고 적는다 — Greg Young의
    *Versioning in an Event Sourced System*이다. **이 KB가 확인한 원전이 아니라 이 책이 대는
    출처다.** 이벤트 페이로드가 바뀔 때의 일반 문제는
    [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md)에 있다.
- **아키텍처 복잡성**(architectural complexity) — **이벤트 소스의 구현은 수많은 아키텍처상의
  "움직이는 부품"을 들여 전체 설계를 더 복잡하게 만든다** (7장, p.112).[^khononov2021]
  그 움직이는 부품이 무엇인지는 다음 장의 [CQRS 아키텍처](cqrs-architecture.md)가 답한다.
- 그리고 셋 모두에 걸리는 단서가 붙는다 — **당면 과제가 이 패턴의 사용을 정당화하지 않고 더
  단순한 설계로 처리될 수 있다면 이 난관들이 전부 더 첨예해진다** (7장,
  p.112).[^khononov2021] 저자는 그 판정 규칙을 10장으로 미룬다.

## 이 패턴이 맞는 자리

- 장 맺음이 적용 조건을 한 문장으로 준다 (7장 §Conclusion, p.115):[^khononov2021]

> This pattern fits cases in which it's crucial to have deep insight into the system's data,
> whether for analysis and optimization or because an audit log is required by law.

- 같은 맺음이 이 패턴의 산물도 다시 적는다 — **이벤트 소싱 도메인 모델에서 애그리게이트 상태에
  대한 모든 변화가 일련의 도메인 이벤트로 표현된다. 그것이 상태 변화가 데이터베이스의 레코드를
  갱신할 뿐인 더 전통적인 접근과 대비된다. 결과로 나온 도메인 이벤트는 애그리게이트의 현재
  상태를 투영하는 데 쓰일 수 있다. 게다가 이벤트 기반 모델은 이벤트를 여러 표현 모델로 — 각각이
  특정 과업에 최적화된 — 투영할 유연성을 준다** (7장, p.115).[^khononov2021]
- **"언제 쓰는가"라는 이름의 절이 이 장에는 없다.** 5장과 6장이 패턴마다 두었던
  `When to Use…` 절이 7장에는 없고, 위 맺음의 한 문장과 비용 셋의 단서가 그 자리를 대신한다.
  판정 규칙 자체는 저자가 10장으로 미룬다.

## 9장이 이 패턴의 둘째 쓰임을 연다

**이 패턴은 애그리게이트를 위해 세워졌지만 9장이 그것을 조율자에게 쓴다.**

- 상태를 관리해야 하는 사가는 **이벤트 소싱 애그리게이트로 구현되어 받은 이벤트와 낸 명령의
  전체 이력을 영속화할 수 있다** (9장, p.149).[^khononov2021] 무엇을 이미 실행했는지 알아야
  실패 시 보상 행동을 낼 수 있기 때문이다.
- 프로세스 매니저도 같다 — **구현의 관점에서 프로세스 매니저는 상태 기반이든 이벤트 소싱이든
  애그리게이트로 구현되는 경우가 많다** (9장, p.152).[^khononov2021]
- **이 쓰임은 위 [이 패턴이 맞는 자리](#이-패턴이-맞는-자리)의 판정 기준과 입력이 다르다.**
  거기서 이 패턴을 부르는 것은 데이터에 대한 깊은 통찰이나 감사 로그의 필요이고, 여기서 이
  패턴을 부르는 것은 **실행 이력 자체가 조율에 필요하다**는 기능 요구다.
  #hypothesis 두 근거가 겹치지는 않으나 저자가 둘의 관계를 명시하지는 않는다.
- 두 패턴의 전문은 [사가 패턴](saga-pattern.md)과 [프로세스 매니저](process-manager.md)에 있다.

## 이미 돌아가는 도메인 모델을 여기로 옮기기

**11장이 이 패턴으로 가는 이행을 다룬다.** 이 페이지가 세운 것이 "무엇을 얻고 잃는가"라면,
이 절부터는 **이미 상태를 저장하고 있는 애그리게이트를 어떻게 여기로 데려오는가**다.

- 조건이 앞 단계의 완료다 — **애그리게이트 경계가 제대로 설계된 도메인 모델을 갖추고 나면 그것을
  이벤트 소싱 모델로 이행시킬 수 있다. 애그리게이트의 데이터를 직접 고치는 대신 애그리게이트의
  생애 주기를 표현하는 데 필요한 도메인 이벤트를 모델링한다** (11장, p.176).[^khononov2021]
  그 앞 단계들은 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.
- **막히는 자리는 코드가 아니라 과거다** (11장, p.176):[^khononov2021]

> The most challenging aspect of refactoring a domain model into an event-sourced domain model is
> the history of the existing aggregates: migrating the "timeless" state into the event-based
> model.

  - 문제의 형태가 명확하다 — **모든 과거 상태 변경을 나타내는 세밀한 데이터가 거기 없으므로**
    선택지가 둘뿐이다 (11장, p.176):[^khononov2021]

> you have to either generate past events on a best-effort basis or model migration events

## 길 하나 과거 전이를 만들어 낸다

- 방법 — **각 애그리게이트에 대해 근사적인 이벤트 스트림을 만들어 내어, 그 이벤트 스트림을
  투영했을 때 원래 구현과 같은 상태 표현이 나오게 하는 것**이다 (11장,
  p.176).[^khononov2021]
- 저자의 예에서 리드(lead) 한 건의 상태 행 하나 — 이름과 전화번호와 `converted` 상태와 세 개의
  타임스탬프 — 를 보고 **업무 로직의 관점에서 애그리게이트 인스턴스가 초기화되었고, 그다음
  그 사람에게 연락이 갔고, 주문이 접수되었고, 마지막으로 상태가 "converted"이므로 주문 대금이
  확인되었다고 가정할 수 있다**고 적는다. 그 가정이 네 개의 이벤트가 된다 —
  `lead-initialized` · `contacted` · `order-submitted` · `payment-confirmed`다 (11장,
  pp.176–177).[^khononov2021]
- **검증 방법까지 붙는다** — **이 이벤트들을 하나씩 적용하면 원래 체계와 정확히 같은 상태 표현으로
  투영될 수 있다. "복구된" 이벤트는 상태를 투영해 원래 데이터와 비교함으로써 쉽게 테스트할 수
  있다** (11장, p.177).[^khononov2021]
- **그러나 이 길이 이 패턴의 목적 자체를 깎는다** (11장, p.177):[^khononov2021]

> The goal of using event sourcing is to have a reliable, strongly consistent history of the
> aggregates' domain events. When this approach is used, it's impossible to recover the complete
> history of state transitions.

  - 무엇이 사라지는지가 예로 특정된다 — **앞의 예에서 우리는 영업 담당자가 그 사람에게 몇 번
    연락했는지, 따라서 우리가 몇 개의 "contacted" 이벤트를 놓쳤는지 알지 못한다** (11장,
    p.177).[^khononov2021]
  - **이 손실이 위 [이점 넷](#이점-넷)의 전제를 갈아먹는다.** 시간의 차원을 얻는 것이 이
    패턴의 이점인데, 만들어 낸 과거는 그 차원의 해상도를 보증하지 않는다.

## 길 둘 마이그레이션 이벤트를 모델링한다

- 방법 — **과거 이벤트에 대한 지식의 부재를 인정하고 그것을 이벤트로 명시적으로 모델링하는
  것**이다. **현재 상태에 이르렀을 법한 이벤트들을 복구하는 대신, 마이그레이션 이벤트를
  정의해 기존 애그리게이트 인스턴스의 이벤트 스트림을 초기화하는 데 쓴다** (11장,
  p.177).[^khononov2021] 저자의 예에서 그것은 `migrated-from-legacy` 하나이고, 상태 행의
  모든 필드를 그 이벤트의 페이로드로 담는다.
- **절충이 명시된다** (11장, pp.177–178):[^khononov2021]

> The advantage of this approach is that it makes the lack of past data explicit. At no stage can
> someone mistakenly assume that the event stream captures all of the domain events that happened
> during the aggregate instance's lifecycle. The disadvantage is that the traces of the legacy
> system will remain in the event store forever.

  - 그 영구한 흔적이 아래 층까지 내려간다 — **예를 들어 CQRS 패턴을 쓰고 있다면(그리고 이벤트
    소싱 도메인 모델과 함께라면 아마 그럴 것이다) 투영은 언제나 마이그레이션 이벤트를 고려해야
    할 것이다** (11장, p.178).[^khononov2021] 그 투영이 사는 자리는
    [CQRS 아키텍처](cqrs-architecture.md)다.
- **두 길의 선택이 정직함과 깔끔함의 맞바꿈이다.** 앞은 스트림을 균질하게 만드는 대신 없는
  것을 있는 것처럼 보이게 하고, 뒤는 스트림에 이물을 영구히 남기는 대신 모르는 것을 모른다고
  적는다. **저자는 어느 쪽을 권하지 않는다** — 두 길의 이점과 비용을 나란히 놓을 뿐이다.
  #hypothesis 이 KB는 뒤쪽이 이 패턴의 목적(신뢰할 수 있는 이력)과 정합적이라고 읽지만
  저자가 그렇게 적지는 않았다.

## 책의 사례 — 이 패턴이 도착점이 된 두 번과 쓸 자리가 아니었던 한 번

**같은 판본의 부록 A에서 이 패턴이 세 번 나온다.** 이야기 본체는
[마켓노버스 사례 연구](marketnovus-case-study.md)에 있고, 여기 옮긴 것은 이 패턴에 걸리는
것이다.

- **두 번은 도착점이었다.** 이벤트 크런처와 보너스는 둘 다 보조 하위 도메인으로 판정되어 단순한
  패턴(각각 트랜잭션 스크립트와 액티브 레코드)으로 구현되었다가, **그 절차로 수익을 내는 길을
  찾으며 핵심 하위 도메인으로 변이했고** 결국 이 패턴으로 다시 쓰였다 (부록 A, pp.280–281 ·
  p.284).[^khononov2021]
  - 이벤트 크런처 쪽에는 이유가 붙어 있다 — 1년을 버틴 뒤 **업무 로직이 너무 복잡해져 이벤트
    소싱으로만 감당할 수 있었으므로** 그 로직을 이 패턴으로 리팩터링하고 **다른 경계
    컨텍스트들이 그 이벤트를 구독하게 했다** (부록 A, p.280).[^khononov2021] 위
    [9장이 이 패턴의 둘째 쓰임을 연다](#9장이-이-패턴의-둘째-쓰임을-연다)가 말하는 배치가
    여기서 실물로 나타난다.
  - **두 번 다 새로 쓰는 길을 택했다** — 옛 코드를 버리고 밑바닥부터 다시 썼다 (부록 A,
    p.281).[^khononov2021] 위
    [이미 돌아가는 도메인 모델을 여기로 옮기기](#이미-돌아가는-도메인-모델을-여기로-옮기기)가
    적는 이행 경로는 **이미 도메인 모델인 경우**의 절차이고, 부록 A의 두 사례는 출발점이 그
    앞 칸(트랜잭션 스크립트·액티브 레코드)이라 그 경로를 타지 않았다.
- **한 번은 쓸 자리가 아니었다.** 마케팅 허브는 경영진이 핵심 업무 도메인으로 규정했으므로
  이 패턴과 CQRS를 함께 꺼내 들었으나, **업무가 핵심이라 여겼음에도 기술적 복잡성이 없었고 그
  복잡한 아키텍처 뒤에 서 있던 것은 평범한 액티브 레코드로 구현할 수 있었을 만큼 단순한 업무
  로직**이었다 (부록 A §"The real problem", p.283).[^khononov2021]
  - **이것이 위 [비용 셋](#비용-셋)이 말하는 값을 실제로 치른 경우다.** 판정을 되검증하는
    절차는 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.

## 이 페이지가 다루지 않는 것

이 장이 이 패턴을 세우기 위해 먼저 설명하는 것들은 **이 패턴에만 걸리는 것이 아니라 이벤트
소싱 일반에 걸리므로** 다른 페이지에 있다.

- 이벤트 소싱이라는 데이터 모델 자체, 이벤트 저장소의 규정과 최소 인터페이스, 성능과 스냅샷,
  데이터 삭제, "그냥 로그를 남기면 안 되는가"라는 물음 넷 — 전부
  [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)에 있다.
- 투영된 모델을 실제 데이터베이스에 물질화하는 방법 —
  [CQRS 아키텍처](cqrs-architecture.md)에 있다. 저자 자신이 7장에서 그리로 넘긴다.
- 이 패턴을 담기에 맞는 코드 조직 — [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의
  포트와 어댑터 절이 그 자리다. 8장이 **포트와 어댑터 아키텍처가 도메인 모델과 이벤트 소싱
  도메인 모델 패턴의 구현에 필요한 대로 업무 로직을 아래 층 어디에도 의존하지 않게 한다**고
  적는다 (8장, p.127).[^khononov2021]

## 이어지는 페이지

- [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md) — 이 패턴이 넷째로 서는
  자리이자 여기로 오는 사다리의 앞 칸들
- [브라운필드에 도메인 주도 설계 들이기](applying-ddd-to-brownfield.md) — 레거시에서 이 이행을
  할 때의 순서와 금지
- [하위 도메인의 세 종류](subdomain-types.md) — 이 이행을 부르는 종류 변화
- [마켓노버스 사례 연구](marketnovus-case-study.md) — 이 패턴이 도착점이 된 두 프로젝트와
  과잉이었던 한 프로젝트
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 패턴이 확장하는 원형
- [도메인 이벤트](domain-events.md) — 이 패턴이 정본으로 삼는 메시지의 규정
- [사가 패턴](saga-pattern.md) — 이 패턴이 조율자에게 쓰이는 첫째 자리
- [프로세스 매니저](process-manager.md) — 그 둘째 자리
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 상태를
  저장하는 쪽의 애그리게이트
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이벤트 소싱이라는 데이터
  모델과 이벤트 저장소
- [CQRS 아키텍처](cqrs-architecture.md) — 투영을 물질화하는 아키텍처 패턴
- [감사와 무결성 검사](../concepts/auditing-and-integrity-checking.md) — 감사 로그라는 이점의 전문
- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 상태를 이벤트에서
  유도한다는 원리
- [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md) — 이벤트 스키마를 바꿀 때
- [핵심 도메인](../concepts/core-domain.md) — 이 패턴이 겨냥하는 하위 도메인
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 7장 "Modeling the Dimension of Time"(도입 p.99 ·
    §"Event Sourcing" 중 투영과 버전 필드 pp.103–104·§Search pp.104–105·§Analysis pp.105–106 ·
    §"Event-Sourced Domain Model" pp.108–110 · 곁글 §Why "Event-Sourced Domain Model"? p.110 ·
    §Advantages pp.110–111 · §Disadvantages pp.111–112 · §Conclusion p.115) ·
    8장 "Architectural Patterns" §"Ports & Adapters" p.127. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 코드 펜스는 애플리케이션 서비스 목록 하나만 두었고 원문에서 깎은
    것은 조판용 줄 번호 표지(01–17)뿐이다 — 원문의 `...`는 저자가 생략을 표시한 것이고 이 KB가
    깎은 것이 아니다. 같은 절의 C# 목록 다섯(`Ticket` 생성자와 `AppendEvent`와
    `Execute(RequestEscalation cmd)`와 `TicketState`, 그리고 §Search·§Analysis의 두 투영
    클래스)은 개념당 대표 하나 규약에 따라 산문으로 줄였고 인용한 식별자는 원문 표기
    그대로다. 도판 셋(Figure 7-1 이벤트 소싱 애그리게이트 · 7-2 스냅샷 · 7-3 이벤트 저장소
    샤딩)은 도판이라 본문이 그것에 대해 적는 것만 옮겼다. 장 끝 연습문제 넷(p.116)은 claim이
    아니라 옮기지 않았다. Greg Young의 *Versioning in an Event Sourced System*은 이 책이 대는
    출처이고 이 KB가 확인한 원전이 아니다. **9장 "Communication Patterns" §"Integrating
    Aggregates"(§Saga p.149 · §"Process Manager" p.152)에서 이 패턴이 조율자의 구현 형태로
    쓰이는 두 자리를 받았다** — 두 패턴의 본체는 [사가 패턴](saga-pattern.md)과
    [프로세스 매니저](process-manager.md)에 있다.
    **11장 "Evolving Design Decisions" §"Domain Model to Event-Sourced Domain Model"(p.176)과
    §"Generating Past Transitions"(pp.176–177) · §"Modeling Migration Events"(pp.177–178)가 이
    페이지에 합류했다** — 이미 돌아가는 도메인 모델을 이 패턴으로 옮길 때 과거 데이터를 어떻게
    할 것인가가 그 자리다. **11장의 JSON 이벤트 목록 둘(복구된 네 이벤트 · 마이그레이션 이벤트
    하나)은 펜스로 옮기지 않았다** — 이 페이지에는 이미 대표 펜스가 있고, 개념당 대표 하나
    규약에 따라 이벤트 이름과 페이로드의 구성만 산문으로 옮겼다. Table 11-1(상태 기반 표현
    한 행)은 예시 데이터라 값을 옮기지 않고 본문이 그것에서 읽어 내는 것만 산문으로 옮겼다.
    11장의 앞 세 이행(트랜잭션 스크립트→액티브 레코드→도메인 모델)은 이 페이지에 두지 않고
    [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 두었다.
    **부록 A §"Bounded Context #3: Event Crunchers"(p.280) · §"Bounded Context #4: Bonuses"
    (pp.280–281) · §"The real problem"(p.283)도 이 페이지에 합류했다** — 이 패턴이 도착점이 된
    두 번과 쓸 자리가 아니었던 한 번이 그 자리다. 다섯 경계 컨텍스트의 이야기 본체는 이
    페이지에 두지 않고 [마켓노버스 사례 연구](marketnovus-case-study.md)에 두었다.

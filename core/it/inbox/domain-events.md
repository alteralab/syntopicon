---
type: concept
title: 도메인 이벤트
description: 업무 도메인에서 일어난 중요한 사건을 서술하는 메시지라는 패턴의 규정 — 이미 일어난 일을 서술하므로 이름을 과거형으로 지으라는 조항, 무엇이 일어났는지와 그에 딸린 데이터를 전부 담는다는 목표와 그 실물 페이로드, 이름이 업무 도메인에서 일어난 일을 간결하게 반영해야 한다는 요구, 애그리게이트의 공개 인터페이스의 일부이며 애그리게이트가 스스로 발행한다는 배치와 다른 프로세스·애그리게이트·외부 시스템이 구독한다는 흐름, 애그리게이트 루트의 명령 인터페이스와 함께 바깥 세상과 통하는 둘째 기제라는 자리, 그리고 이 KB의 다른 축들이 같은 낱말을 쓰는 자리들과의 분업
generated: { by: "claude-opus-5", at: "2026-09-14T23:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 도메인 이벤트

- [정의](#정의)
- [이름은 과거형이다](#이름은-과거형이다)
- [무엇을 담는가](#무엇을-담는가)
- [누가 발행하고 누가 받는가](#누가-발행하고-누가-받는가)
- [애그리게이트 안에서 어떻게 생기는가](#애그리게이트-안에서-어떻게-생기는가)
- [같은 낱말을 쓰는 이 KB의 다른 자리들](#같은-낱말을-쓰는-이-kb의-다른-자리들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애그리게이트가 자기 경계 밖으로 무엇이 일어났는지 알리는 수단은 무엇이고,
그것이 만족해야 하는 조건은 무엇인가.**

## 정의

- [khononov2021](../sources/khononov2021.md)이 이 패턴을 애그리게이트 절 안에서 규정한다
  (6장 §"Domain events", p.91):[^khononov2021]

> A domain event is a message describing a significant event that has occurred in the business
> domain.

- 저자가 드는 예 셋이 이름의 모양을 보인다 (6장, p.91):[^khononov2021]
  - **Ticket assigned**(티켓이 배정됨)
  - **Ticket escalated**(티켓이 상급자에게 넘겨짐)
  - **Message received**(메시지가 접수됨)

## 이름은 과거형이다

- 조항이 한 줄이다 — **도메인 이벤트는 이미 일어난 무엇을 서술하므로 그 이름은 과거형으로
  표현되어야 한다** (6장, p.91).[^khononov2021]
- 그리고 이름 짓기에 무게가 실린다 — **소프트웨어 공학의 거의 모든 것이 그렇듯 이름 짓기가
  중요하다. 도메인 이벤트의 이름이 업무 도메인에서 정확히 무엇이 일어났는지를 간결하게
  반영하도록 하라** (6장, p.91).[^khononov2021]
  - 이 요구가 [유비쿼터스 언어](ubiquitous-language.md)의 요구와 같은 것이다. 같은 조항을
    애그리게이트 전체에 거는 자리는
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
  - 이름이 모델의 결함을 드러내는 신호라는 더 넓은 판정은
    [이름 짓기](../concepts/naming-things.md)에 있다.

## 무엇을 담는가

- 목표가 둘이다 — **업무 도메인에서 무엇이 일어났는지를 서술하는 것, 그리고 그 사건에 관련된
  필요한 데이터를 전부 제공하는 것** (6장, p.91).[^khononov2021]
- 저자가 드는 실물이 티켓이 상급자에게 넘겨진 사건을 **어느 티켓인지·언제·무슨 이유로**까지
  담아 전달하는 페이로드다 (6장, p.91):[^khononov2021]

  ```json
  {
      "ticket-id": "c9d286ff-3bca-4f57-94d4-4d4e490867d1",
      "event-id": 146,
      "event-type": "ticket-escalated",
      "escalation-reason": "missed-sla",
      "escalation-time": 1628970815
  }
  ```

  - **필드 다섯이 각각 무엇을 맡는지가 드러난다** — 어느 애그리게이트 인스턴스인지
    (`ticket-id`), 이벤트 자체의 식별자(`event-id`), 종류(`event-type`), 그리고 이 사건에만
    있는 데이터 둘(`escalation-reason`·`escalation-time`)이다. 저자가 이 구조를 규약으로
    제시하지는 않는다.
  - 이 페이로드가 구독자에게 넘어간 뒤 스키마가 바뀌면 무엇이 깨지는지는 이 패턴 밖의 물음이고,
    그 자리는 [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md)이다.

## 누가 발행하고 누가 받는가

- **배치가 한 문장에 있다** (6장, pp.91–92):[^khononov2021]

> Domain events are part of an aggregate's public interface. An aggregate publishes its domain
> events. Other processes, aggregates, or even external systems can subscribe to and execute
> their own logic in response to the domain events, as shown in Figure 6-6.

- **이것이 애그리게이트가 바깥 세상과 통하는 둘째 기제다.** 첫째는 애그리게이트 루트가 내놓는
  명령(command)이고, 저자가 그 둘을 나란히 둔다 — **애그리게이트 루트의 공개 인터페이스 외에
  바깥 세상이 애그리게이트와 소통할 수 있는 또 하나의 기제가 있다. 도메인 이벤트다**
  (6장, p.91).[^khononov2021]
  - **방향이 반대라는 것이 두 기제의 차이다.** 명령은 바깥에서 안으로 들어오고, 도메인 이벤트는
    안에서 밖으로 나간다. 그 둘이 애그리게이트의 공개 인터페이스 전부다. 명령 쪽의 전문은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
- 구독자가 셋으로 열거된다는 점에 주의한다 — **다른 프로세스, 다른 애그리게이트, 그리고 외부
  시스템까지**다. 즉 이 기제는 한 프로세스 안의 결합 끊기와 시스템 사이의 통합 양쪽에 쓰인다.
- **신뢰성 있는 발행은 이 패턴이 답하지 않는다** — 저자가 그것을 9장으로 미룬다
  (6장, p.92).[^khononov2021] 같은 문제를 저장 기제 사이에서 다루는 자리가
  [트랜잭션 스크립트](transaction-script.md)의 분산 트랜잭션 사례이고, 그 해법의 이름이
  아웃박스 패턴이다.

## 애그리게이트 안에서 어떻게 생기는가

- 애그리게이트가 이벤트를 자기 컬렉션에 쌓아 두는 모양이다. 티켓 애그리게이트가
  `private List<DomainEvent> _domainEvents;` 필드를 갖고, 상급자 이관을 요청하는 명령을
  처리하면서 조건 둘(아직 이관되지 않았고 남은 시간이 0 이하)을 검사하고, 상태 플래그를 세우고,
  **새 이벤트 객체를 만들어(`new TicketEscalated(_id, cmd.Reason)`) 그 컬렉션에 덧붙인다**
  (6장, p.92).[^khononov2021]
- **이 조각이 말하는 것은 "일으키기"와 "발행하기"가 갈린다는 것이다.** 애그리게이트는 이벤트를
  만들어 자기 안에 모아 두고, 그것을 실제로 버스에 올리는 일은 이 코드 밖에서 일어난다.
  그 바깥의 선택지들을 열거해 둔 자리가
  [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md)다 — 서비스
  레이어가 올리는 판본, 도메인 모델이 일으키고 서비스 레이어가 올리는 판본, 작업 단위가
  모아서 올리는 판본 셋이다.
  - **두 소스가 같은 그림에 도착한다.** 그쪽의 둘째·셋째 선택지가 이 코드와 같은 모양이고,
    그쪽이 "언제 이벤트를 일으킬지에 대한 로직은 정말로 모델과 함께 살아야 한다"는 이유를
    댄다. 두 소스가 서로를 참조한 적은 없다.

## 같은 낱말을 쓰는 이 KB의 다른 자리들

이 낱말은 이 KB의 여러 축에 이미 퍼져 있다. 이 페이지는 **패턴의 규정**만 갖고 나머지를
가리킨다.

- [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md) — 이벤트를
  메시지 버스에 올리는 방법과 그 대가, 그리고 명령과 이벤트를 가르는 축들.
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이벤트를 **상태의 정본**으로
  삼는 쪽. 이 페이지의 도메인 이벤트는 상태를 대체하지 않고 상태 변화를 알릴 뿐이라 다른
  물음이다.
- [메시징 패턴](../synthesis/messaging-patterns.md) — 발행·구독과 메시지 채널의 카탈로그 층.
- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 같은 어휘가 분석 데이터의
  조직 경계로 쓰이는 자리.
- **원전에는 이 패턴이 없다.** [evans2003](../sources/evans2003.md)의 전술 패턴 목록은 엔티티,
  값 객체, 서비스, 모듈, 애그리게이트, 팩토리, 리포지터리이고 도메인 이벤트가 거기 들지 않는다.
  이 판본이 그것을 애그리게이트의 공개 인터페이스에 넣어 목록에 더한다. #hypothesis 이 KB가
  읽은 원전의 범위 안에서 그렇다는 뜻이고, 저자가 이 차이를 명시한 적은 없다.

## 이어지는 페이지

- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 이 이벤트를
  발행하는 주체
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 이벤트가 구성 단위로 드는 패턴
- [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md) — 일으킨
  이벤트를 실제로 버스에 올리는 법
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이벤트를 상태의 정본으로 삼는 쪽
- [트랜잭션 스크립트](transaction-script.md) — 발행의 신뢰성이 문제로 서는 자리
- [유비쿼터스 언어](ubiquitous-language.md) — 이벤트 이름이 따라야 하는 말
- [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md) — 발행된 페이로드가 바뀔 때
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 6장 "Tackling Complex Business Logic" §"Domain events"
    (pp.91–92). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout`
    추출로 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다. 코드 펜스는 JSON 페이로드 하나만
    두었고 원문 그대로다(언어 표지는 이 KB가 붙였다). 같은 절의 C# 목록(티켓 애그리게이트가
    이벤트를 만들어 컬렉션에 덧붙이는 `Execute(RequestEscalation cmd)`)은 산문으로만 옮겼고
    인용한 식별자는 원문 표기 그대로다. 도판 하나
    (Figure 6-6 도메인 이벤트 발행 흐름)는 도판이라 옮기지 않고 본문이 그것에 대해 적는
    것만 서술했다.

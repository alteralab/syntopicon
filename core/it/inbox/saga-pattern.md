---
type: concept
title: 사가 패턴
description: 애그리게이트 여럿에 걸치는 업무 프로세스를 한 트랜잭션으로 묶지 않고 구현하는 패턴 — 한 트랜잭션에 애그리게이트 하나라는 원칙이 막아 놓은 자리와 그 원칙을 깨는 대신 우회하는 길, 광고 캠페인과 게시자 사이의 사례, 시간이 아니라 트랜잭션의 수로 오래 산다는 정의와 이벤트를 듣고 명령을 내며 실패하면 보상 행동을 내는 세 가지 일, 상태 없는 사가와 실행 이력을 남겨야 하는 사가와 후자를 이벤트 소싱 애그리게이트로 구현하는 길, 명령 실행을 사가 밖으로 빼 아웃박스처럼 비동기로 돌리라는 조항, 그리고 이것이 트랜잭션이 아니라는 못박음 — 두 트랜잭션이 원자적일 수 없고 관련 구성 요소의 상태는 결국 일관될 뿐이며 잘못 그은 애그리게이트 경계를 사가로 메우지 말라는 경고
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 사가 패턴

- [무엇이 막혀 있었는가](#무엇이-막혀-있었는가)
- [사례 — 캠페인과 게시자](#사례--캠페인과-게시자)
- [정의](#정의)
- [사가가 하는 일 셋](#사가가-하는-일-셋)
- [상태 없는 사가와 상태를 갖는 사가](#상태-없는-사가와-상태를-갖는-사가)
- [명령 실행을 사가 밖으로 뺀다](#명령-실행을-사가-밖으로-뺀다)
- [이것은 트랜잭션이 아니다](#이것은-트랜잭션이-아니다)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 프로세스가 애그리게이트 여러 개에 걸칠 때 그것을 한 트랜잭션으로 묶지
않고 어떻게 구현하는가.**

## 무엇이 막혀 있었는가

- 출발점은 6장이 세운 금지다 (9장, p.147):[^khononov2021]

> One of the core aggregate design principles is to limit each transaction to a single instance of an
> aggregate. This ensures that an aggregate's boundaries are carefully considered and encapsulate a
> coherent set of business functionality.

  - 그 원칙의 정본은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
- **그러나 그 금지가 요구를 없애지는 않는다** — **애그리게이트 여러 개에 걸치는 업무 프로세스를
  구현해야 하는 경우가 있다** (9장, p.147).[^khononov2021]
- **이 패턴의 정체는 그 금지를 깨지 않고 우회하는 것이다.** 아래
  [이것은 트랜잭션이 아니다](#이것은-트랜잭션이-아니다)가 그 우회의 대가를 적는다.

## 사례 — 캠페인과 게시자

- 저자가 드는 흐름은 이렇다 — 광고 캠페인이 활성화되면 그 광고물을 게시자에게 자동으로
  제출해야 하고, 게시자에게서 확인을 받으면 캠페인의 게시 상태가 `Published`로 바뀌어야 하며,
  게시자가 거절하면 캠페인은 `Rejected`로 표시되어야 한다 (9장, p.147).[^khononov2021]
- 왜 애그리게이트 하나로 묶을 수 없는가가 함께 적힌다 — 이 흐름은 광고 캠페인과 게시자라는 두
  업무 개체에 걸치고, **둘을 같은 애그리게이트 경계 안에 몰아넣는 것은 분명히 과잉이다**.
  책임이 다른 명백히 다른 업무 개체이고 **서로 다른 경계 컨텍스트에 속할 수도 있기**
  때문이다 (9장, p.147).[^khononov2021]
- 사가가 듣는 이벤트는 `Campaign` 애그리게이트의 `CampaignActivated`와 `AdPublishing` 경계
  컨텍스트의 `PublishingConfirmed`·`PublishingRejected`이고, 내는 명령은 `AdPublishing` 쪽의
  `SubmitAdvertisement`와 `Campaign` 애그리게이트 쪽의 `TrackPublishingConfirmation`·
  `TrackPublishingRejection`이다 (9장, p.148).[^khononov2021]
  - **이 사례에서 `TrackPublishingRejection`이 보상 행동(compensation action)으로 작동한다** —
    광고 캠페인이 활성으로 등재되지 않게 보장하는 일을 그 명령이 맡는다 (9장,
    p.148).[^khononov2021]
- 코드의 모양이 이것이다. 상태를 갖지 않는 판본이고, `Process` 메서드 셋이 각각 이벤트 하나를
  받아 명령 하나를 내는 것이 전부다 (9장, pp.148–149):[^khononov2021]

```csharp
public class CampaignPublishingSaga
{
    private readonly ICampaignRepository _repository;
    private readonly IPublishingServiceClient _publishingService;
    ...

    public void Process(CampaignActivated @event)
    {
        var campaign = _repository.Load(@event.CampaignId);
        var advertisingMaterials = campaign.GenerateAdvertisingMaterials();
        _publishingService.SubmitAdvertisement(@event.CampaignId,
                                              advertisingMaterials);
    }

    public void Process(PublishingConfirmed @event)
    {
        var campaign = _repository.Load(@event.CampaignId);
        campaign.TrackPublishingConfirmation(@event.ConfirmationId);
        _repository.CommitChanges(campaign);
    }

    public void Process(PublishingRejected @event)
    {
        var campaign = _repository.Load(@event.CampaignId);
        campaign.TrackPublishingRejection(@event.RejectionReason);
        _repository.CommitChanges(campaign);
    }
}
```

## 정의

- 정의가 두 문장이다 (9장, p.147):[^khononov2021]

> A saga is a long-running business process. It's long running not necessarily in terms of time, as
> sagas can run from seconds to years, but rather in terms of transactions: a business process that
> spans multiple transactions.

  - **"오래 산다"의 단위가 시간이 아니라 트랜잭션이라는 것이 이 정의의 핵심이다.** 몇 초짜리
    사가도 사가이고, 기준은 트랜잭션 경계를 몇 개 건너느냐다.
  - 역어 — 이 KB는 *saga*를 **사가**로 음차한다. 확립 역어가 없고, 의미(북유럽 서사시)를 옮기면
    검색 키가 사라진다.

## 사가가 하는 일 셋

- 세 가지가 한 문단에 규정된다 (9장, p.147):[^khononov2021]

> The transactions can be handled not only by aggregates but by any component emitting domain events
> and responding to commands. The saga listens to the events emitted by the relevant components and
> issues subsequent commands to the other components. If one of the execution steps fails, the saga
> is in charge of issuing relevant compensating actions to ensure the system state remains consistent.

  - **듣는다 — 낸다 — 실패하면 보상한다.** 셋 중 셋째가 이 패턴의 값이고, 나머지 둘만 있으면
    그냥 이벤트 핸들러다.
  - **참여자의 자격이 애그리게이트로 제한되지 않는다는 데 주의한다.** 도메인 이벤트를 내고
    명령에 응답하는 구성 요소면 무엇이든 참여할 수 있으므로, 사가는 경계 컨텍스트 사이에도
    걸린다.

## 상태 없는 사가와 상태를 갖는 사가

- 위 코드가 어느 쪽인지 저자가 밝힌다 (9장, p.149):[^khononov2021]

> The preceding example relies on the messaging infrastructure to deliver the relevant events, and it
> reacts to the events by executing the relevant commands. This is an example of a relatively simple
> saga: it has no state.

- 상태가 필요해지는 조건과 그때의 구현이 이어진다 (9장, p.149):[^khononov2021]

> You will encounter sagas that do require state management; for example, to track the executed
> operations so that relevant compensating actions can be issued in case of a failure. In such a
> situation, the saga can be implemented as an event-sourced aggregate, persisting the complete
> history of received events and issued commands.

  - **보상이 상태를 부른다.** 무엇을 이미 실행했는지 모르면 무엇을 되돌려야 하는지도 모른다.
    그래서 실패 보상이 필요한 사가는 실행 이력을 남겨야 하고, 그 이력이 곧
    [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)의 이벤트 스트림이 된다.
  - **사가를 애그리게이트로 구현한다는 배치에 주의한다.** 사가는 애그리게이트 여럿에 걸치는
    것을 조율하려고 만들어졌는데, 그 조율자 자신은 애그리게이트 하나가 된다. 조율자의 상태
    변경만은 여전히 한 트랜잭션 안에 든다.

## 명령 실행을 사가 밖으로 뺀다

- 조항이 하나 붙는다 (9장, p.149):[^khononov2021]

> However, the command execution logic should be moved out of the saga itself and executed
> asynchronously, similar to the way domain events are dispatched in the outbox pattern:

- 상태를 갖는 판본에서 사가는 명령을 직접 부르지 않고 `CommandIssuedEvent`를 만들어 자기 이벤트
  목록에 붙인다. 각 `CommandIssuedEvent`는 대상(`Target`)과 명령을 담고, **아웃박스 릴레이가
  그 인스턴스마다 해당 엔드포인트에서 명령을 실행하게 된다** (9장, pp.149–150).[^khononov2021]
- 왜 그렇게 하는가가 한 문장으로 적힌다 (9장, p.150):[^khononov2021]

> As in the case of publishing domain events, separating the transition of the saga's state from the
> execution of commands ensures that the commands will be executed reliably, even if the process
> fails at any stage.

  - **그러므로 사가는 [아웃박스 패턴](outbox-pattern.md) 위에 선다.** 앞 절이 이벤트 발행에
    대해 세운 것과 똑같은 논증이 명령 실행에 그대로 적용된다 — 상태 전이와 바깥 세상에 대한
    효과를 같은 트랜잭션에 넣지 말고, 효과는 커밋된 기록에서 릴레이가 뒤에 집행한다.

## 이것은 트랜잭션이 아니다

- 절의 제목이 `Consistency`이고 내용은 부정이다 (9장, p.150):[^khononov2021]

> Although the saga pattern orchestrates a multicomponent transaction, the states of the involved
> components are eventually consistent. And although the saga will eventually execute the relevant
> commands, no two transactions can be considered atomic.

- 저자가 그것을 애그리게이트 설계 원칙 하나와 잇는다 (9장, p.150):[^khononov2021]

> Only the data within an aggregate's boundaries can be considered strongly consistent. Everything
> outside is eventually consistent.

- 그 원칙을 무엇에 쓰라는지도 적힌다 (9장, p.150):[^khononov2021]

> Use this as a guiding principle to make sure you are not abusing sagas to compensate for improper
> aggregate boundaries. Business operations that have to belong to the same aggregate require
> strongly consistent data.

  - **이 세 문단이 이 패턴의 경계 조건이다.** 사가는 애그리게이트 경계를 넘는 수단이지 그 경계를
    다시 그어 주는 수단이 아니다. 강한 일관성이 필요한 업무 연산이라면 답은 사가가 아니라
    애그리게이트 경계의 재설계다.
  - **그래서 "분산 트랜잭션의 대안"이라는 자리매김은 반쪽만 맞다.** 원자성은 오지 않는다.
    이 판본이 대신 주는 것은 실패해도 시스템이 일관된 상태로 수렴한다는 것뿐이고, 그 사이의
    창에서는 캠페인이 활성인데 게시되지 않은 상태가 실제로 관측된다.
  - 같은 맞교환을 데이터베이스 쪽 어휘로 다루는 자리가
    [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md)과
    [조정 회피](../concepts/coordination-avoidance.md)다.
- 절이 다음 패턴을 예고하며 닫힌다 — **사가 패턴은 다른 패턴 하나와 자주 혼동된다: 프로세스
  매니저다. 구현은 비슷하지만 다른 패턴이다** (9장, p.150).[^khononov2021] 그 구별은
  [프로세스 매니저](process-manager.md)에 있다.

## 이 KB의 다른 자리들과의 분업

- **이 이름은 이 KB에 처음 들어온다.** 이 반입 전까지 코퍼스에 사가를 다루는 페이지가 없었고,
  가장 가까운 자리는 롤백 대신 보상으로 푸는 오래 사는 프로세스를 2003년 시점의 표준 전망으로
  다루는 [패턴과 표준](../concepts/patterns-and-standards.md)과, 제약을 사후에 느슨하게 강제하고
  어긋나면 보상하는 쪽을 다루는
  [느슨하게 해석되는 제약](../concepts/loosely-interpreted-constraints.md)이었다.
- **이 페이지의 범위는 이 소스가 말하는 것까지다.** 사가의 두 조율 방식(코레오그래피와
  오케스트레이션)이나 실패 유형의 분류 같은 것은 이 판본이 다루지 않는다 — 저자는 명령을 내는
  주체가 하나 있는 모양만 제시하고, 분기하는 흐름은 프로세스 매니저로 넘긴다.
  #hypothesis 뒤 배치의 다른 소스가 이 페이지를 넓힐 자리로 보인다.

## 이어지는 페이지

- [프로세스 매니저](process-manager.md) — 이 패턴과 자주 혼동되는 쪽. 분기와 상태가 들어갈 때
- [아웃박스 패턴](outbox-pattern.md) — 이 패턴이 딛고 서는 발행 기제
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 이 패턴이
  우회하는 원칙이 사는 자리
- [도메인 이벤트](domain-events.md) — 사가가 듣는 것
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 상태를 갖는 사가의 구현 형태
- [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md) — 원자성을 실제로 주려는 쪽
- [느슨하게 해석되는 제약](../concepts/loosely-interpreted-constraints.md) — 보상으로 푸는
  발상의 다른 자리
- [복합 라우팅 패턴](../concepts/composed-routing-patterns.md) — 같은 문제를 통합 패턴 언어로
  다루는 자리
- [메시징 패턴](../synthesis/messaging-patterns.md) — 그 이름 층의 허브
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 9장 "Communication Patterns" §"Integrating Aggregates" 중
    §Saga(pp.147–150, 곁 절 §Consistency p.150). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다.
    §Consistency의 애그리게이트 원칙 두 문장은 원문이 기울임 인용구로 조판한 것이라 그 서식만
    떼고 옮겼다. 도판 하나(Figure 9-13 사가)는 도판이라 본문이 그것에 대해 적는 것만 옮겼다.
    **코드 목록 둘 중 펜스로 옮긴 것은 상태 없는 `CampaignPublishingSaga`(pp.148–149)
    하나다** — 개념당 대표 펜스 하나 규약에 따랐고, 상태를 갖는 판본(pp.149–150)은 산문으로
    줄였다. 세 점(`...`)은 저자가 생략을 표시한 것이고 이 KB가 깎은 것이 아니다. 언어
    표지(`csharp`)만 더했다. 본문이 이벤트·명령 이름을 나열하는 문단(p.148)은 원문 조판이
    식별자를 줄바꿈으로 끊어 놓아(`Campaign Act ivated` 등) 직인용하지 않고 한국어로 재서술하며
    식별자를 이어 붙였다. 장 끝 연습문제(pp.154–155)는 claim이 아니라 옮기지 않았다.

---
type: concept
title: 사가 패턴
status: draft
description: 애그리게이트 여럿 또는 서비스 여럿에 걸치는 업무 프로세스를 한 트랜잭션으로 묶지 않고 구현하는 패턴 — 한 트랜잭션에 애그리게이트 하나라는 원칙이 막아 놓은 자리와 그 원칙을 깨는 대신 우회하는 길, 광고 캠페인과 게시자 사이의 사례, 시간이 아니라 트랜잭션의 수로 오래 산다는 정의와 이벤트를 듣고 명령을 내며 실패하면 보상 행동을 내는 세 가지 일, 상태 없는 사가와 실행 이력을 남겨야 하는 사가, 명령 실행을 사가 밖으로 빼 아웃박스처럼 비동기로 돌리라는 조항, 이것이 트랜잭션이 아니라는 못박음, 그리고 같은 이름을 마이크로서비스 쪽에서 쓴 소스 — 오래 사는 트랜잭션을 짧은 트랜잭션 열로 쪼갠다는 1987년 원전의 발상과 잠금을 오래 쥐지 않는다는 이득, 업무 실패는 다루고 기술 실패는 다루지 않는다는 경계, 뒤로 복구와 앞으로 복구와 그 혼합, 되돌릴 수 없는 것을 의미적 롤백으로 메우는 보상 트랜잭션, 실패할 일을 앞으로 당겨 롤백 자체를 줄이는 단계 재배치, 중앙 조율자를 두는 오케스트레이션과 이벤트로 흩는 코레오그래피와 각각의 대가, 팀 경계로 둘을 고르라는 저자의 조건부 선호, 그리고 두 소스가 사가라는 낱말을 서로 다른 대상에 쓴다는 대조표
generated: { by: "claude-opus-5", at: "2026-09-15T17:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
---

# 사가 패턴

- [무엇이 막혀 있었는가](#무엇이-막혀-있었는가)
- [사례 — 캠페인과 게시자](#사례--캠페인과-게시자)
- [정의](#정의)
- [사가가 하는 일 셋](#사가가-하는-일-셋)
- [상태 없는 사가와 상태를 갖는 사가](#상태-없는-사가와-상태를-갖는-사가)
- [명령 실행을 사가 밖으로 뺀다](#명령-실행을-사가-밖으로-뺀다)
- [이것은 트랜잭션이 아니다](#이것은-트랜잭션이-아니다)
- [같은 이름을 마이크로서비스 쪽에서 쓴 소스](#같은-이름을-마이크로서비스-쪽에서-쓴-소스)
- [1987년 원전이 풀려던 문제](#1987년-원전이-풀려던-문제)
- [사가가 주지 않는 것](#사가가-주지-않는-것)
- [업무 실패는 다루고 기술 실패는 다루지 않는다](#업무-실패는-다루고-기술-실패는-다루지-않는다)
- [뒤로 복구와 앞으로 복구](#뒤로-복구와-앞으로-복구)
- [보상 트랜잭션과 의미적 롤백](#보상-트랜잭션과-의미적-롤백)
- [단계를 재배치해 롤백 자체를 줄인다](#단계를-재배치해-롤백-자체를-줄인다)
- [구현 둘 — 오케스트레이션과 코레오그래피](#구현-둘--오케스트레이션과-코레오그래피)
- [저자의 선호와 그 조건](#저자의-선호와-그-조건)
- [사가와 분산 트랜잭션](#사가와-분산-트랜잭션)
- [두 소스가 사가라는 낱말을 다른 대상에 쓴다](#두-소스가-사가라는-낱말을-다른-대상에-쓴다)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 프로세스가 애그리게이트 여러 개 또는 서비스 여러 개에 걸칠 때 그것을 한
트랜잭션으로 묶지 않고 어떻게 구현하는가.**

**이 페이지에는 소스가 둘이고 둘이 같은 낱말을 다른 대상에 쓴다.** 앞쪽 절들은
[khononov2021](../sources/khononov2021.md)의 도메인 모델 쪽 규정이고, 뒤쪽 절들은
[newman2021](../sources/newman2021.md)의 마이크로서비스 쪽 규정이다. 두 어휘의 대응은
[두 소스가 사가라는 낱말을 다른 대상에 쓴다](#두-소스가-사가라는-낱말을-다른-대상에-쓴다)에
표로 정리했다 — **먼저 그 표를 보고 오는 편이 헷갈리지 않는다.**

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
    [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md)의 이벤트 스트림이 된다.
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

  - **그러므로 사가는 [아웃박스 패턴](../concepts/outbox-pattern.md) 위에 선다.** 앞 절이 이벤트 발행에
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
  [프로세스 매니저](../concepts/process-manager.md)에 있다.

## 같은 이름을 마이크로서비스 쪽에서 쓴 소스

- [newman2021](../sources/newman2021.md)은 사가를 **분산 트랜잭션의 대안**으로 세운다. 규정이
  2단계 커밋과의 대조로 온다 (6장 §Sagas, p.182):[^newman2021]

  > Unlike a two-phase commit, a saga is by design an algorithm that can coordinate multiple
  > changes in state, but avoids the need for locking resources for long periods of time.

  - **기제는 쪼개기다** — 관여하는 단계들을 독립적으로 실행할 수 있는 개별 활동으로 모형화함으로써
    그렇게 한다 (6장, p.182).[^newman2021]
  - **부수 이득 하나가 명시된다** — 사가를 쓰면 **업무 프로세스를 명시적으로 모형화하도록 강요당하고**
    그것 자체가 상당한 이득일 수 있다 (6장, p.182).[^newman2021] 저자는 장 맺음에서 그것을
    한 번 더 든다 — 업무 프로세스를 사가로 명시적으로 모형화하면 **암묵적으로만 모형화됐을
    프로세스가 개발자에게 훨씬 분명하고 눈에 보이게 된다** (6장, p.196).[^newman2021]
- **저자가 이 장 앞에서 분산 트랜잭션을 기각한 뒤 이것을 대안으로 내놓는다.** 그 기각의 전문은
  [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md)에 있다.

## 1987년 원전이 풀려던 문제

- **핵심 발상의 출처를 저자가 댄다** — Hector Garcia-Molina와 Kenneth Salem의 1987년 논문
  "Sagas"이고, 그것이 다루는 대상은 **오래 사는 트랜잭션(long lived transaction, LLT)**이라
  불리는 연산이다. 이 트랜잭션은 오래 걸릴 수 있고(몇 분·몇 시간·며칠) 그 과정의 일부로
  데이터베이스 변경을 요구한다 (6장, p.182).[^newman2021]
  - **이 KB는 그 논문을 확인하지 않았다** — 이 귀속은 newman2021의 서술이다.
- 문제가 무엇인지 — LLT를 보통의 데이터베이스 트랜잭션에 그대로 대응시키면 **트랜잭션 하나가
  LLT의 생애 전체에 걸치게 되고**, 여러 행이나 테이블 전체가 오래 잠긴 채로 남아 다른 프로세스가
  그것을 읽거나 고치려 할 때 심각한 문제를 만든다 (6장, p.182).[^newman2021]
- 원전의 처방 — **LLT를 각각 독립적으로 다룰 수 있는 트랜잭션 열로 쪼갠다.** 각 "하위"
  트랜잭션은 더 짧고 LLT가 건드리는 데이터의 일부만 고치므로, **잠금의 범위와 지속 시간이 크게
  줄어 밑의 데이터베이스에서 경합이 훨씬 덜하다** (6장, p.183).[^newman2021]
- **서비스로의 이전이 저자가 하는 일이다** — 사가는 원래 단일 데이터베이스에 대고 동작하는
  LLT를 돕는 기제로 구상됐지만, **그 모형은 여러 서비스에 걸친 변경을 조율하는 데도 똑같이 잘
  맞는다.** 업무 프로세스 하나를 협업하는 서비스들에 대한 호출의 집합으로 쪼갤 수 있고, **그것이
  사가를 이룬다** (6장, p.183).[^newman2021]
  - **그러므로 이 판본에서 "사가"는 그 업무 프로세스 전체를 가리키는 이름이다.** 아래
    [대조표](#두-소스가-사가라는-낱말을-다른-대상에-쓴다)가 이 점을 다른 소스와 견준다.
- 사가 안의 각 단계는 서로 다른 서비스가 수행하는 연산이고, **각 서비스 안에서는 상태 변경이
  로컬 ACID 트랜잭션으로 처리될 수 있다** (6장, p.183).[^newman2021]

## 사가가 주지 않는 것

- 저자가 곁글로 못 박는다 — **사가는 보통의 데이터베이스 트랜잭션에서 익숙한 ACID 의미의
  원자성을 주지 않는다.** LLT를 개별 트랜잭션으로 쪼개므로 **사가 자체의 수준에서는 원자성이
  없고**, 사가 안의 개별 트랜잭션 각각에 대해서는 원자성이 있다(각각이 필요하면 ACID 트랜잭션
  변경에 대응할 수 있다). **사가가 주는 것은 지금 어느 상태에 있는지 따져 볼 만큼의 정보이고,
  그 함의를 감당하는 것은 우리 몫이다** (6장, p.183).[^newman2021]
  - **이 못박음이 khononov2021의
    [이것은 트랜잭션이 아니다](#이것은-트랜잭션이-아니다)와 같은 방향이다.** 두 소스가 어휘도
    사례도 다르게 쓰면서 이 한 조항에서는 갈리지 않는다 — 원자성은 오지 않는다.

## 업무 실패는 다루고 기술 실패는 다루지 않는다

- **경계가 명시된다** — 사가가 복구하게 해 주는 것은 **업무 실패**이지 **기술 실패**가 아니다
  (6장 §"Saga Failure Modes", p.185).[^newman2021]

| 실패 | 예 | 누가 다루는가 |
|---|---|---|
| 업무 실패 | 고객에게서 대금을 받으려는데 **잔고가 부족하다** | 사가가 다룰 것으로 기대된다 |
| 기술 실패 | 결제 게이트웨이가 타임아웃되거나 `500 Internal Service Error`를 던진다 | **따로 다뤄야 한다** |

- 전제가 따라 나온다 — **사가는 밑의 구성 요소들이 제대로 동작한다고 가정한다.** 밑의 체계가
  신뢰할 수 있고, 우리는 그 신뢰할 수 있는 구성 요소들의 일을 조율하고 있을 뿐이라는 것이다
  (6장, p.185).[^newman2021] 저자는 그 구성 요소를 신뢰할 수 있게 만드는 수단을 12장으로
  미루고, 이 한계에 대해서는 우베 프리드리히센(Uwe Friedrichsen)의 글을 권한다 — 이 KB가
  확인한 원전이 아니다.
  - **이 경계가 실무에서 가장 자주 잊히는 조항이다.** 사가를 들이면 부분 실패가 풀린다고
    읽기 쉬운데, 저자는 정반대로 **부분 실패는 이미 풀려 있다고 가정한 위에서** 사가가 돈다고
    적는다. 그 가정이 성립하지 않을 때 무엇이 필요한지는
    [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md)와
    [장애 모형과 동기성](../concepts/failure-models-and-synchrony.md)이 답한다.

## 뒤로 복구와 앞으로 복구

- **원전이 복구를 둘로 가른다** (6장 §"Saga Failure Modes", p.184):[^newman2021]

  > Backward recovery involves reverting the failure and cleaning up afterwards—a rollback. […]
  > Forward recovery allows us to pick up from the point where the failure occurred and keep
  > processing.

  | | 뒤로 복구(backward recovery) | 앞으로 복구(forward recovery) |
  |---|---|---|
  | 하는 일 | 실패를 되돌리고 뒤처리한다 — 롤백 | 실패한 지점에서 집어 들어 계속 처리한다 |
  | 성립 조건 | **보상 행동(compensating action)을 정의**해 이미 커밋된 트랜잭션을 되돌릴 수 있어야 한다 | **트랜잭션을 재시도**할 수 있어야 하고, 그러려면 체계가 재시도에 필요한 정보를 충분히 영속화하고 있어야 한다 |

- **둘 중 하나를 고르는 것이 아니다** — 모형화하는 업무 프로세스의 성격에 따라 어떤 실패 유형은
  뒤로 복구를, 어떤 것은 앞으로 복구를, 또는 **둘의 혼합**을 촉발하리라 기대할 수 있다 (6장,
  p.185).[^newman2021]
- 저자가 드는 혼합의 실물 — 주문 처리에서 **대금을 이미 받았고 물건도 포장됐다면 남은 단계는
  발송뿐인데**, 배송사 차량에 자리가 없다는 이유로 **주문 전체를 되돌리는 것은 매우 이상해
  보인다.** 그 경우에는 발송을 재시도하고(이를테면 다음 날로 큐에 넣고), 그것도 실패하면
  사람의 개입을 요구하는 쪽이 낫다 (6장 §"Mixing fail-backward and fail-forward situations",
  p.189).[^newman2021]
  - **이 예가 고르는 기준을 보여 준다** — 이미 치른 일이 많고 남은 일이 적을수록 앞으로
    복구가 싸다. 되돌릴 것이 많아질수록 뒤로 복구의 값이 오른다.

## 보상 트랜잭션과 의미적 롤백

- **ACID 롤백과 다른 점부터 짚는다** — ACID 트랜잭션에서는 커밋 전에 롤백을 촉발하므로
  롤백 뒤에는 아무 일도 없었던 것 같다. 그러나 사가에는 트랜잭션이 여럿 관여하고 **그중 일부는
  전체 연산을 되돌리기로 결정하기 전에 이미 커밋됐을 수 있다** (6장 §"Saga rollbacks",
  p.185).[^newman2021]
- 그래서 필요한 것이 보상 트랜잭션이다 (6장, p.186):[^newman2021]

  > A compensating transaction is an operation that undoes a previously committed transaction.

  - 전체를 되돌리려면 **사가에서 이미 커밋된 각 단계마다 그 보상 트랜잭션을 촉발한다** (6장,
    p.186).[^newman2021]
- **이것이 데이터베이스 롤백처럼 굴지는 않는다** — 데이터베이스 롤백은 커밋 전에 일어나고 그
  뒤에는 트랜잭션이 없었던 것과 같지만, 여기서는 **그 트랜잭션들이 실제로 일어났다.** 원래
  트랜잭션이 만든 변경을 되돌리는 **새 트랜잭션을 만드는 것**일 뿐이고, 시간을 되감아 원래
  트랜잭션이 없었던 것처럼 만들 수는 없다 (6장, p.186).[^newman2021]
- 그래서 이름이 붙는다 — **의미적 롤백(semantic rollback)**이다. 언제나 전부를 치울 수는
  없고, 사가의 맥락에서 충분할 만큼만 한다 (6장, p.187).[^newman2021]
  - 저자가 드는 예 — 단계 하나가 주문이 발송 중이라는 메일을 고객에게 보낸 것이었다면
    **보낸 메일을 되돌릴 수는 없다.** 대신 보상 트랜잭션이 둘째 메일을 보내 주문에 문제가
    있었고 취소됐음을 알릴 수 있다 (6장, p.187).[^newman2021]
- **롤백의 흔적이 남는 것은 정상이다** — 롤백과 관련된 정보가 체계에 남는 것은 전적으로
  적절하고, 실은 매우 중요한 정보일 수 있다. 중단된 주문에 대해 무슨 일이 있었는지를 담은
  기록을 `Order` 서비스에 남겨 두고 싶을 이유가 여럿 있다 (6장, p.187).[^newman2021]
  - **이것이 보상을 "취소"와 가르는 자리다.** 보상은 흔적을 지우는 것이 아니라 결과를 뒤집는
    것이고, 그래서 [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)의 append-only 기록과
    충돌하지 않는다.

## 단계를 재배치해 롤백 자체를 줄인다

- **이 절이 이 소스가 더하는 실무 지렛대다** (6장 §"Reordering workflow steps to reduce
  rollbacks", p.188).[^newman2021]
- 저자의 예 — 주문 처리에서 **적립 포인트를 주문이 실제로 발송될 때만 주도록** 옮기면, 포장과
  발송에서 문제가 생겨도 그 단계를 되돌릴 걱정이 사라진다 (6장, p.188).[^newman2021]
- 조문이 둘이다 (6장, pp.188–189):[^newman2021]
  - **워크플로를 수행하는 방식을 조금 바꾸는 것만으로 롤백 연산을 단순하게 만들 수 있을 때가
    있다.** 실패할 가능성이 가장 높은 단계를 앞으로 당겨 프로세스를 더 일찍 실패시키면,
    **뒤의 보상 트랜잭션은 애초에 촉발되지 않았으므로 그것을 촉발할 필요 자체가 없어진다.**
  - 그리고 **어떤 단계에 대해서는 보상 트랜잭션을 만들 필요조차 없어질 수 있다.** 보상
    트랜잭션을 구현하기 어려운 경우에 특히 중요하고, 단계를 **되돌릴 일이 결코 없는 지점까지
    뒤로 미룰** 수 있을 때도 있다.
  - **이 둘이 서로 반대 방향이라는 데 주의한다** — 실패하기 쉬운 것은 앞으로, 되돌리기 어려운
    것은 뒤로 옮긴다. 두 축이 다르므로 충돌하지 않는다.
- **이 조항이 4장의 갈고리를 받는다** — 한 연산을 트랜잭션 둘로 쪼개고 나서 순서를 조정해
  경우를 더 잘 다룰 수 있다는 발상이 6장 앞에서 사가로 미뤄져 있었다 (6장, p.178).[^newman2021]

## 구현 둘 — 오케스트레이션과 코레오그래피

- **논리 모형과 구현을 저자가 가른다.** 사가가 어떻게 도는가의 논리 모형은 위까지이고, 그것을
  실제로 구현하는 방식이 둘이다 (6장 §"Implementing Sagas", p.189).[^newman2021]

| | 오케스트레이션된 사가(orchestrated saga) | 코레오그래피된 사가(choreographed saga) |
|---|---|---|
| 규정 | **중앙 조율자**(저자가 *오케스트레이터*라 부른다)가 실행 순서를 정하고 필요한 보상 행동을 촉발한다 | 사가의 운영 책임을 **협업하는 여러 서비스에 분산**한다 |
| 은유 | 명령과 통제(command-and-control) | 믿되 검증한다(trust-but-verify) |
| 통신 경향 | 서비스 사이 **요청-응답**을 많이 쓴다 | **이벤트**를 많이 쓴다 |
| 원전과의 거리 | 원래 해법 공간에 더 가깝다 | 중앙 조율의 필요를 피한다 |
| 진행 상태 추적 | 쉽다 — 한 자리에 있다 | **더 복잡해진다** |

- 오케스트레이션의 규정 (6장 §"Orchestrated sagas", p.189):[^newman2021]

  > Orchestrated sagas use a central coordinator (what we'll call an orchestrator from now on) to
  > define the order of execution and to trigger any required compensating action.

  - **이득** — 업무 프로세스가 오케스트레이터 안에 명시적으로 모형화되므로 체계의 한 자리를
    보면 그 프로세스가 어떻게 돌아가기로 되어 있는지 이해할 수 있다. 새 사람을 들이기 쉬워지고
    체계의 핵심부에 대한 이해를 심어 주는 데 도움이 된다 (6장, p.190).[^newman2021]
  - **대가 둘** (6장, pp.190–191):[^newman2021]
    - **본성상 결합된 접근이다** — 오케스트레이터가 관련된 모든 서비스를 알아야 하므로
      **도메인 결합(domain coupling)의 정도가 높아진다.** 저자는 도메인 결합이 본디 나쁜 것은
      아니되 가능하면 최소로 두고 싶은데 **여기서는 피하기 어렵다**고 적는다. 그 결합의 규정은
      [서비스 결합의 네 종류](../concepts/service-coupling-types.md)에 있다.
    - **더 미묘한 쪽 — 서비스로 밀어 넣어야 할 로직이 오케스트레이터에 흡수되기 시작한다.**
      그러면 서비스가 자기 행동은 거의 없이 오케스트레이터의 지시만 받는 **빈혈
      (anemic)** 상태가 될 수 있다. 저자는 그 흐름에 대고 한 줄을 세운다 (6장,
      p.191):[^newman2021]

      > If logic has a place where it can be centralized, it will become centralized!

  - **완화책** — 흐름마다 다른 서비스가 오케스트레이터 역할을 맡게 한다. 주문에는 `Order
    Processor`, 반품·환불에는 `Returns`, 입고에는 `Goods Receiving` 하는 식이다. `Warehouse`
    같은 서비스는 그 오케스트레이터 전부가 쓰게 되고, 그런 모형이라야 기능을 `Warehouse`
    자신에 남겨 여러 흐름에 재사용하기 쉬워진다 (6장, p.191).[^newman2021]
  - **오케스트레이션된 흐름에 참여하는 서비스도 여전히 자기 로컬 상태와 행동을 가진 개체로
    봐야 한다** — 그것들은 자기 로컬 상태 기계의 주인이다 (6장, pp.190–191).[^newman2021]
- 코레오그래피의 규정 (6장 §"Choreographed sagas", p.192):[^newman2021]

  > A choreographed saga aims to distribute responsibility for the operation of the saga among
  > multiple collaborating services.

  - **기제** — 서비스들이 받은 이벤트에 반응한다. 이벤트는 개념적으로 체계에 방송되고 관심
    있는 쪽이 받는다. **이벤트를 특정 마이크로서비스에게 보내는 것이 아니라 그냥 쏘아 올리고,
    관심 있는 마이크로서비스가 받아 알아서 행동한다** (6장, p.192).[^newman2021] 그 통신
    모형의 전문은 [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md)에 있다.
  - **병렬 처리가 공짜로 따라온다** — 결제 완료 이벤트 하나가 적립과 창고 양쪽에서 반응을
    일으켜 한쪽은 포장·발송을, 다른 쪽은 포인트 지급을 동시에 한다 (6장,
    p.193).[^newman2021]
  - **브로커와 토픽이 필요하다** — 이벤트의 신뢰할 수 있는 방송과 전달을 관리하려면 보통 어떤
    메시지 브로커를 쓰고, 여러 마이크로서비스가 같은 이벤트에 반응할 수 있으므로 **토픽을
    쓴다.** 관심 있는 쪽은 이벤트가 어디서 왔는지 걱정하지 않고 토픽을 구독하며, 브로커가
    토픽의 내구성과 구독자에게의 전달을 보장한다 (6장, p.193).[^newman2021] 그 기제는
    [발행-구독 메시징](../concepts/publish-subscribe-messaging.md)에 있다.
  - **이득** — 어느 서비스도 다른 마이크로서비스를 알지 못하고 **특정 이벤트를 받았을 때 무엇을
    할지만 알면 되므로 도메인 결합의 양이 크게 준다.** 또 프로세스의 구현이 여러 서비스에
    분해·분산되므로 **로직 중앙집중의 걱정도 피한다** — 로직을 중앙집중할 자리가 없으면
    중앙집중되지 않는다 (6장, p.193).[^newman2021]
  - **대가 둘** (6장, p.193):[^newman2021]
    - **무슨 일이 벌어지는지 알아내기가 더 어렵다.** 오케스트레이션에서는 프로세스가
      오케스트레이터에 명시적으로 모형화돼 있었는데, 여기서는 **각 서비스의 행동을 따로 보고
      그림을 머릿속에서 재구성해야** 한다.
    - **더 나쁜 것은 사가가 어느 상태인지 알 길이 없다는 것이다** — 그러면 필요할 때 보상
      행동을 붙일 기회를 잃는다. 보상 수행의 책임을 개별 서비스에 일부 밀어 넣을 수는 있으나,
      **어떤 종류의 복구에는 사가가 어느 상태인지 아는 길이 근본적으로 필요하다.**
  - **그 대가를 갚는 수단이 상관 ID다** — 방출되는 이벤트를 소비해 사가 상태에 대한 뷰를
    투영하는 것이 가장 쉬운 길 중 하나다. 사가마다 고유 ID(**상관 ID**, correlation ID)를
    만들어 그 사가의 일부로 방출되는 모든 이벤트에 넣고, 서비스가 이벤트에 반응할 때 그것을
    뽑아 로컬 로깅에 쓰며 이후의 호출·이벤트에도 함께 흘려보낸다. 그러면 **그 이벤트를 전부
    빨아들여 각 주문이 어느 상태인지 보여 주는 뷰를 내놓는 서비스**를 둘 수 있고, 다른 서비스가
    스스로 못 푸는 문제를 프로그램으로 해결하게 할 수도 있다 (6장, pp.193–194).[^newman2021]
    - 저자는 **이런 코레오그래피된 사가에 어떤 형태로든 상관 ID가 필수라고 여긴다**고 적고,
      상관 ID의 더 일반적인 값어치는 10장으로 미룬다 (6장, p.194).[^newman2021]
- **둘을 섞을 수 있다** — 겉보기에 정반대로 보이지만 섞어 쓸 수 있고, 어떤 업무 프로세스는
  한쪽에 더 자연스럽게 맞는다. **한 사가 안에 두 방식이 섞일 수도 있다** — 주문 처리 전체는
  코레오그래피된 사가로 두면서 `Warehouse` 서비스의 경계 **안쪽**에서 포장과 발송을 관리할 때는
  오케스트레이션된 흐름을 쓰는 식이다 (6장 §"Mixing styles", p.194).[^newman2021]
  - **섞기로 했다면 조건이 붙는다** — 사가가 어느 상태인지와 사가의 일부로 이미 무슨 활동이
    있었는지를 이해할 분명한 길이 여전히 있어야 한다. 그것이 없으면 실패 유형을 이해하기가
    복잡해지고 실패로부터의 복구가 어려워진다 (6장, p.194).[^newman2021]
  - 저자는 원전의 저자들이 사가를 **중첩(nested)**해 더 복잡한 프로세스를 구현하는 길을
    이어서 탐구했다고 각주로 적되 그것을 이 책의 범위 밖으로 둔다 (6장, p.194,
    각주 6).[^newman2021] 이 KB는 그 논문도 확인하지 않았다.
- **BPM 도구에 대한 저자의 판정** (6장 곁글 §"BPM Tools", pp.191–192):[^newman2021]
  - 업무 프로세스 모형화(business process modeling, BPM) 도구는 **개발자가 아닌 사람이 업무
    프로세스 흐름을 정의하게 하려고** 설계됐고 흔히 시각적 끌어놓기 도구를 쓴다. 개발자가
    구성 블록을 만들고 비개발자가 그것을 엮어 더 큰 흐름을 만든다는 발상이다. **프로세스
    오케스트레이션이 BPM 도구의 주 용례**이고, 뒤집어 말하면 **BPM 도구를 쓰면 오케스트레이션을
    채택하게 된다.**
  - 저자는 **BPM 도구를 몹시 싫어하게 됐다**고 적는다. 주된 이유는 그 중심 전제(비개발자가 업무
    프로세스를 정의하리라는 것)가 **경험상 거의 참이었던 적이 없다**는 것이다. 비개발자를 겨냥한
    도구를 결국 개발자가 쓰게 되는데, 그 도구들은 개발자가 일하는 방식과 이질적으로 작동한다 —
    흐름을 바꾸려면 GUI를 써야 하고, 만들어진 흐름은 **버전 관리가 어렵거나 불가능**할 수 있고,
    흐름 자체가 테스트를 염두에 두고 설계되지 않았을 수 있다.
  - **처방** — 개발자가 업무 프로세스를 구현할 것이라면 그들이 알고 이해하며 그들의 작업 흐름에
    맞는 도구를 쓰게 하라. 대체로 **그냥 코드로 구현하게 하라**는 뜻이다. 업무 프로세스가 어떻게
    구현되고 어떻게 도는지에 대한 가시성이 필요하다면, **워크플로를 코드에서 시각적 표현으로
    투영하는 편이 시각적 표현으로 코드를 서술하는 것보다 훨씬 쉽다.**
  - 버전 조건: 2021년 저술 시점의 도구 지형 — 저자는 더 개발자 친화적인 BPM 도구를 만들려는
    시도가 있고 개발자 반응은 엇갈리지만 일부에게는 잘 통했다고 적으면서, 굳이 본다면
    **Camunda와 Zeebe**(마이크로서비스 개발자를 겨냥한 오픈 소스 오케스트레이션 프레임워크)를
    보라고 권한다 (6장, p.192).[^newman2021] 위 처방(코드로 구현하라·시각화는 코드에서
    투영하라)에는 조건을 달지 않았다.

## 저자의 선호와 그 조건

- **저자 자신의 취향과 일반 조언을 스스로 가른다** (6장 §"Should I use choreography or
  orchestration (or a mix)?", p.195).[^newman2021]
- 취향 쪽 — 코레오그래피된 사가의 구현은 낯선 발상을 들일 수 있고 **널리 이해돼 있지 않은
  이벤트 주도 협업을 많이 쓴다고 전제한다.** 그럼에도 저자의 경험에서는 **사가 진행을 추적하는
  데 드는 추가 복잡도가 더 느슨하게 결합된 아키텍처의 이득에 거의 언제나 압도된다** (6장,
  p.195).[^newman2021]
- **조건부 조언 쪽이 이 절의 값이다** (6장, p.195):[^newman2021]

| 조건 | 저자의 권고 | 근거 |
|---|---|---|
| **한 팀이 사가 전체의 구현을 소유**한다 | 오케스트레이션된 사가에 매우 관대하다 | 본디 더 결합된 아키텍처를 **팀 경계 안에서는 관리하기 훨씬 쉽다** |
| **여러 팀이 관여**한다 | 더 분해된 코레오그래피된 사가를 훨씬 선호한다 | 사가 구현의 책임을 팀들에 나눠 주기 쉽고, 더 느슨한 결합이 팀들을 더 고립되게 일하게 해 준다 |

- **경향 하나가 덧붙는다** — 일반 규칙으로 오케스트레이션에서는 요청-응답 호출로, 코레오그래피
  에서는 이벤트로 기울기 쉽다. 저자는 이것이 **엄격한 규칙이 아니라 일반적 관찰**이라고 단다
  (6장, p.195).[^newman2021]
- **저자가 자기 편향을 스스로 채점한다** — 코레오그래피 쪽으로 기우는 자기 성향은 **자신이
  이벤트 주도 상호작용 모형으로 끌리는 경향의 함수일 가능성이 높고**, 이벤트 주도 협업을
  이해하기 어렵다면 코레오그래피는 당신에게 맞지 않을 수 있다고 적는다 (6장,
  p.195).[^newman2021]
  - 같은 자기 채점이 4장에서도 있었다 — 그 자리는
    [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md)이다.

## 사가와 분산 트랜잭션

- **저자의 결론** — 분산 트랜잭션에는 상당한 어려움이 따르고, **아주 특정한 상황 밖에서는
  피하는 편**이라는 것이다 (6장 §"Sagas Versus Distributed Transactions",
  p.195).[^newman2021]
- 저자는 팻 헬런드(Pat Helland)의 문장을 인용해 그 어려움의 핵심을 댄다 — **분산 트랜잭션
  체계 대부분에서 노드 하나의 실패가 트랜잭션 커밋을 멎게 하고, 그것이 다시 애플리케이션을
  옴짝달싹 못 하게 만든다. 그런 체계에서는 커질수록 내려가 있을 가능성이 높아진다** (6장,
  p.195).[^newman2021] 헬런드의 원글은 이 KB가 확인한 원전이 아니다.
  - **비유가 그 논증을 요약한다** — 모든 엔진이 다 돌아야 하는 비행기를 몬다면 엔진을 하나 더
    다는 것이 비행기의 가용성을 **낮춘다** (6장, p.195).[^newman2021]
  - 같은 산수를 이 KB의 다른 자리에서 재는 것이
    [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md)의 부분 실패 절이다.
- **그리고 사가가 더 주는 것** — 업무 프로세스를 사가로 명시적으로 모형화하면 분산 트랜잭션의
  어려움 다수를 피하면서, 덤으로 **체계의 핵심 업무 프로세스를 일급 개념으로 만드는** 이득이
  따라온다 (6장, p.196).[^newman2021]

## 두 소스가 사가라는 낱말을 다른 대상에 쓴다

- **이 페이지에서 가장 조심할 것이 이것이다.** 두 소스가 같은 낱말을 쓰는데 **그 낱말이
  가리키는 대상의 층이 다르다.**

| | [khononov2021](../sources/khononov2021.md) (도메인 모델 쪽) | [newman2021](../sources/newman2021.md) (마이크로서비스 쪽) |
|---|---|---|
| **사가가 무엇인가** | **구성 요소 하나** — 이벤트를 듣고 그에 대응하는 명령을 내는 객체 | **프로세스 전체** — 여러 서비스에 걸친 오래 사는 업무 트랜잭션 그 자체 |
| 사가의 범위 | 단순하고 선형인 흐름. 이벤트와 명령을 짝짓는다 | 갈라지든 아니든 업무 프로세스 전부. 실패 복구 전략과 단계 순서까지 포함한다 |
| 중앙 조율자가 있는가 | 사가 객체 자신이 그 자리다 — **언제나 있다** | **구현 선택지다** — 오케스트레이션이면 있고 코레오그래피면 없다 |
| 판단 로직이 들어오면 | **다른 이름이 된다** — 프로세스 매니저다(if-else 어림법) | **여전히 사가다** — 오케스트레이터가 판단을 한다 |
| 보상의 자리 | 사가가 보상 행동을 발행한다 | 보상 트랜잭션을 촉발하는 것이 오케스트레이터이거나 개별 서비스다 |
| 원자성 | 오지 않는다. 결국 일관될 뿐이다 | 오지 않는다. ACID 의미의 원자성이 아니다 |

- **대응을 세워 보면 이렇게 어긋난다.**
  - **newman의 오케스트레이션 = khononov의 사가 + 프로세스 매니저 둘 다를 덮는다.** newman은
    중앙 조율자를 "오케스트레이터"라 부르고 그것이 **실행 순서를 정하고 실패 시 무엇을 할지
    결정한다**고 적는다. khononov의 어림법으로 재면 그 결정은 if-else이므로 **newman의
    오케스트레이터는 대개 khononov의 프로세스 매니저에 해당한다.** khononov의 사가(판단 없는
    짝짓기)는 그중 로직이 없는 특수한 경우다.
  - **newman의 코레오그래피는 khononov의 두 이름 어디에도 대응하지 않는다.** khononov의
    사가와 프로세스 매니저는 **둘 다 중앙 구성 요소**이고, 코레오그래피는 그런 구성 요소가
    없는 배치이기 때문이다. khononov 쪽에서 가장 가까운 자리는 패턴 이름이 아니라
    [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md)다.
  - **그래서 "이 설계는 사가인가"라는 물음은 소스를 밝히지 않으면 답할 수 없다.** 코레오그래피된
    주문 처리 흐름은 newman에게는 사가이고 khononov에게는 사가도 프로세스 매니저도 아니다.
- **모순 쌍(`contradicts`)을 걸지 않았다.** 두 서술이 같은 대상에 대해 다른 사실을 주장하는
  것이 아니라 **낱말의 외연이 다른 것**이고, 겹치는 자리(원자성은 오지 않는다·보상으로 되돌린다·
  경계를 잘못 그었으면 사가로 메우지 마라)에서는 둘이 같은 방향을 가리킨다. newman의
  "가로지르는 변경이 잦으면 경계가 틀린 것"(7장)과 khononov의 "잘못 그은 애그리게이트 경계를
  사가로 보상하지 마라"(9장)는 층이 다를 뿐 같은 경고다.
- **이 KB가 쓰는 규약** — 이 페이지에서 사가라는 낱말이 나오면 **그 절이 어느 소스의 것인지로
  외연을 정한다.** 페이지 첫머리의 안내와 절 제목이 그 표지다. 두 판본이 한 이름으로 합쳐지지
  않는 이유를 여기 적어 두는 것이 합치는 것보다 낫다고 판정했다.

## 이 KB의 다른 자리들과의 분업

- **이 이름은 khononov2021 반입에서 이 KB에 처음 들어왔고, newman2021 6장이 그것을 마이크로
  서비스 층으로 넓혔다.** 그 두 반입 전에 가장 가까운 자리는 롤백 대신 보상으로 푸는 오래 사는
  프로세스를 2003년 시점의 표준 전망으로 다루는
  [패턴과 표준](../concepts/patterns-and-standards.md)과, 제약을 사후에 느슨하게 강제하고
  어긋나면 보상하는 쪽을 다루는
  [느슨하게 해석되는 제약](../concepts/loosely-interpreted-constraints.md)이었다.
- **이 페이지의 범위는 두 소스가 말하는 것까지다.** 사가를 중첩해 더 복잡한 프로세스를 만드는
  길은 newman2021이 범위 밖으로 두고 이 KB도 그 논문을 확인하지 않았다. 상관 ID의 일반적
  값어치와 호출 추적은 newman2021이 10장으로 미루므로 여기 없다.

## 이어지는 페이지

- [프로세스 매니저](../concepts/process-manager.md) — 이 패턴과 자주 혼동되는 쪽. 분기와 상태가 들어갈 때
- [아웃박스 패턴](../concepts/outbox-pattern.md) — 이 패턴이 딛고 서는 발행 기제
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 코레오그래피가
  기대는 이벤트 주도 협업과 오케스트레이션이 기대는 요청-응답
- [발행-구독 메시징](../concepts/publish-subscribe-messaging.md) — 코레오그래피의 토픽과 브로커
- [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md) — 코레오그래피가
  쏘아 올리는 이벤트를 어떤 종류로 설계할 것인가
- [서비스 결합의 네 종류](../concepts/service-coupling-types.md) — 오케스트레이터가 올리는
  도메인 결합의 규정
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 엔진을 더 달면
  가용성이 내려간다는 산수의 일반형
- [장애 모형과 동기성](../concepts/failure-models-and-synchrony.md) — 사가가 다루지 않는
  기술 실패 쪽
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 이 패턴이
  우회하는 원칙이 사는 자리
- [도메인 이벤트](../concepts/domain-events.md) — 사가가 듣는 것
- [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md) — 상태를 갖는 사가의 구현 형태
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

[^newman2021]: Newman 2021, 6장 "Workflow" §Sagas(pp.182–196) — §"Saga Failure
    Modes"(pp.184–189, 하위 절 §"Saga rollbacks" pp.185–187 · §"Reordering workflow steps to
    reduce rollbacks" pp.188–189 · §"Mixing fail-backward and fail-forward situations" p.189) ·
    §"Implementing Sagas"(pp.189–195, 하위 절 §"Orchestrated sagas" pp.189–191 ·
    §"Choreographed sagas" pp.192–194 · §"Mixing styles" p.194 · §"Should I use choreography or
    orchestration (or a mix)?" p.195, 곁글 §"BPM Tools" pp.191–192 · §"Tracing Calls" p.194
    포함) · §"Sagas Versus Distributed Transactions"(pp.195–196) · §Summary(p.196), 그리고
    §"Still ACID, but Lacking Atomicity?"의 단계 재배치 한 줄(p.178). 쪽은 인쇄판 쪽 번호(PDF
    쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 줄바꿈
    하이픈(U+2010)은 원래 낱말로 이었으며 굽은 따옴표는 곧은 따옴표로 옮겼다. 뒤로 복구와
    앞으로 복구의 직인용은 원문에서 이어진 한 문단이고 가운데 두 문장을 생략 표시(`[…]`)로
    줄인 것이 이 KB의 편집이다 — 그 두 문장의 내용은 바로 아래 표의 "성립 조건" 칸에 한국어로
    옮겼다. 도판 일곱(Figure 6-5 주문 이행 흐름과 담당 서비스 · 6-6 창고에서 물건을 못 찾음 ·
    6-7 사가 전체의 롤백 촉발 · 6-8 단계를 뒤로 옮겨 롤백 줄이기 · 6-9 오케스트레이션된 사가 ·
    6-10 코레오그래피된 사가, 그리고 2단계 커밋 도판들)은 이미지로 조판돼 있어 본문이 그 도판에
    대해 적는 것만 산문으로 옮겼다. 이 절들에는 코드 목록이 없어 이 소스에서 온 코드 펜스는
    0건이다. MusicCorp 주문 이행 서사(주문·결제·창고·적립·발송)는 저자가 명시한 가상 회사의
    예시라 그 서사가 예시하는 판정만 옮기고 이야기는 옮기지 않았다. 저자가 가리키는 바깥
    서지(Garcia-Molina & Salem 1987 "Sagas"와 1991년 중첩 사가 논문 · Pat Helland
    "Life Beyond Distributed Transactions" · Uwe Friedrichsen "The Limits of the Saga Pattern" ·
    Gregor Hohpe & Bobby Woolf *Enterprise Integration Patterns* · Bernd Ruecker *Practical
    Process Automation* · Camunda·Zeebe 문서)는 이 KB가 확인한 원전이 아니다 — 다만 Hohpe &
    Woolf는 이 KB가 들인 [hohpe2004](../sources/hohpe2004.md)와 같은 책이라 그 자리는
    [복합 라우팅 패턴](../concepts/composed-routing-patterns.md)이다.

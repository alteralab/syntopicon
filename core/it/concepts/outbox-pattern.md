---
type: concept
title: 아웃박스 패턴
description: 애그리게이트의 상태 변경과 그 도메인 이벤트의 발행을 어긋나지 않게 만드는 패턴 — 애그리게이트 안에서 바로 버스에 올리는 구현이 틀린 두 이유와 애플리케이션 계층으로 옮겨도 남는 실패, 상태와 이벤트를 한 원자적 트랜잭션에 함께 커밋하고 릴레이가 뒤에서 발행한다는 네 단계 알고리즘, 관계형에서는 전용 테이블을 쓰고 다중 문서 트랜잭션이 없는 NoSQL에서는 애그리게이트 레코드에 이벤트를 심는다는 두 구현, 릴레이가 미발행 이벤트를 가져오는 두 방식인 폴링 발행자와 트랜잭션 로그 테일링, 이 패턴이 주는 보장이 최소 한 번이라는 못박음, 그리고 이 KB의 이중 쓰기·변경 데이터 캡처·정확히 한 번 처리 서술과의 분업, 그리고 이 패턴이 필요해지는 배치에 이름과 채점을 붙이면서도 이 문제 자체는 한 번도 꺼내지 않는 소스와 그 부재의 실측, 그리고 같은 패턴을 레거시 데이터 해방 수단으로 다시 세우며 기제와 최소 한 번 보장에서 일치하되 목적을 내부 모델 격리로 넓히고 정렬 식별자와 직렬화 시점과 채점표를 더하는 2025년 실무서
generated: { by: "claude-opus-5", at: "2026-09-18T06:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: bellemare2025, resource: /it/sources/bellemare2025.md }
---

# 아웃박스 패턴

- [무엇을 푸는 패턴인가](#무엇을-푸는-패턴인가)
- [틀린 구현 하나 — 애그리게이트가 직접 발행한다](#틀린-구현-하나--애그리게이트가-직접-발행한다)
- [틀린 구현 둘 — 커밋한 뒤 애플리케이션 계층이 발행한다](#틀린-구현-둘--커밋한-뒤-애플리케이션-계층이-발행한다)
- [알고리즘 네 단계](#알고리즘-네-단계)
- [관계형과 NoSQL의 두 구현](#관계형과-nosql의-두-구현)
- [릴레이가 미발행 이벤트를 가져오는 두 방식](#릴레이가-미발행-이벤트를-가져오는-두-방식)
- [보장은 최소 한 번이다](#보장은-최소-한-번이다)
- [2025년 실무서가 같은 패턴을 레거시 해방 수단으로 다시 세운다](#2025년-실무서가-같은-패턴을-레거시-해방-수단으로-다시-세운다)
- [이 문제를 꺼내지 않는 소스](#이-문제를-꺼내지-않는-소스)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애그리게이트의 상태 변경과 그 변경을 알리는 메시지가 어긋나지 않게 하려면
발행을 어디에 두어야 하는가.**

## 무엇을 푸는 패턴인가

- 물음이 6장에서 넘어온다. 애그리게이트가 시스템의 나머지와 통신하는 방법 중 하나가 도메인
  이벤트를 발행하는 것이고 외부 구성 요소가 그것을 구독해 자기 로직을 실행한다 — **그런데
  도메인 이벤트는 어떻게 메시지 버스로 발행되는가** (9장, p.143).[^khononov2021]

> But how are domain events published to a message bus?

- 저자는 해답 전에 **이벤트 발행 과정에서 흔히 저지르는 실수 몇과 각 접근의 결과**를 먼저
  살핀다 (9장, p.143).[^khononov2021] 아래 두 절이 그 둘이다.
- 도메인 이벤트 자체의 규정은 [도메인 이벤트](../concepts/domain-events.md)에, 애그리게이트의 트랜잭션
  경계는 [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에
  있다.

## 틀린 구현 하나 — 애그리게이트가 직접 발행한다

- 첫 예제에서 `Campaign` 애그리게이트의 `Deactivate` 메서드가 새 이벤트를 만들어 자기 내부
  이벤트 목록에 붙이고(18행) 곧바로 메시지 버스에 발행한다(19행) (9장, p.143).[^khononov2021]
- 저자의 판정이 한 문장이다 (9장, p.144):[^khononov2021]

> This implementation of publishing domain events is simple but wrong.

- 나쁜 이유가 둘이다 (9장, p.144):[^khononov2021]
  - **순서가 뒤집힌다** — 이벤트가 **애그리게이트의 새 상태가 데이터베이스에 커밋되기 전에**
    발송된다. 구독자는 캠페인이 비활성화됐다는 통지를 받지만 그것이 캠페인의 상태와 모순될 수
    있다.
  - **롤백이 이벤트를 되돌리지 못한다** — 경쟁 조건이나 뒤따르는 애그리게이트 로직이나 단순한
    데이터베이스 기술 문제로 트랜잭션이 커밋에 실패하면, **데이터베이스 트랜잭션은 롤백되지만
    이벤트는 이미 발행되어 구독자에게 밀려 나갔고 그것을 회수할 방법이 없다**.

## 틀린 구현 둘 — 커밋한 뒤 애플리케이션 계층이 발행한다

- 둘째 예제는 발행 책임을 애플리케이션 계층으로 옮긴다. `ManagementAPI.DeactivateCampaign`이
  애그리게이트를 싣고 명령을 실행하고 커밋한 **다음에** 미발행 이벤트를 꺼내 버스에 올리고
  목록을 비운다 (9장, p.144).[^khononov2021]
- 저자가 스스로 묻고 답한다 (9장, p.144):[^khononov2021]

> Can we trust this code? No.

- 남는 실패가 무엇인지 적힌다 (9장, p.145):[^khononov2021]

> In this case, the process running the logic for some reason fails to publish the domain events.
> Perhaps the message bus is down. Or the server running the code fails right after committing the
> database transaction, but before publishing the events the system will still end in an inconsistent
> state, which means that the database transaction is committed, but the domain events will never be
> published.

  - **두 틀린 구현이 같은 문제의 양쪽 끝이다.** 하나는 커밋 **전에** 발행해서 없던 일을 알리고,
    다른 하나는 커밋 **후에** 발행해서 일어난 일을 못 알린다. 두 저장 기제에 순서대로 쓰는 한
    어느 순서를 골라도 창이 남는다.
  - 저자는 그 창을 **엣지 케이스(edge cases)** 라 부르고 아웃박스 패턴으로 다룰 수 있다고
    적는다 (9장, p.145).[^khononov2021]

## 알고리즘 네 단계

- 패턴의 규정이 알고리즘으로 주어진다 (9장, p.145):[^khononov2021]

> The outbox pattern (Figure 9-11) ensures reliable publishing of domain events using the following
> algorithm:

- 네 단계다 (9장, p.145):[^khononov2021]

> Both the updated aggregate's state and the new domain events are committed in the same atomic
> transaction.

> A message relay fetches newly committed domain events from the database.

> The relay publishes the domain events to the message bus.

> Upon successful publishing, the relay either marks the events as published in the database or
> deletes them completely.

  - **첫 단계가 이 패턴의 전부다.** 두 저장 기제에 나눠 쓰던 것을 **한 기제 안의 두 쓰기**로
    바꾸면 데이터베이스가 이미 가진 원자성이 그대로 보장이 된다. 나머지 셋은 그렇게 남겨 둔
    이벤트를 뒤에서 내보내는 절차다.
  - 그래서 이 패턴은 **분산 트랜잭션을 피하는 쪽**에 선다. 피해 가는 대상의 서술은
    [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md)과
    [XA 트랜잭션](../concepts/xa-transactions.md)에 있다.

## 관계형과 NoSQL의 두 구현

- 관계형에서는 **두 테이블에 원자적으로 커밋하는 데이터베이스의 능력을 활용해 메시지를 담는 전용
  테이블을 쓰는 것이 편하다** (9장, p.145).[^khononov2021]
- **다중 문서 트랜잭션을 지원하지 않는 NoSQL에서는 나가는 도메인 이벤트를 애그리게이트의 레코드
  안에 심어야 한다** (9장, p.146).[^khononov2021] 저자가 드는 문서의 모양이 이것이다 (9장,
  p.146):[^khononov2021]

  ```json
  {
      "campaign-id": "364b33c3-2171-446d-b652-8e5a7b2be1af",
      "state": {
          "name": "Autumn 2017",
          "publishing-state": "DEACTIVATED",
          "ad-locations": [
              ...
          ]
          ...
      },
      "outbox": [
          {
              "campaign-id": "364b33c3-2171-446d-b652-8e5a7b2be1af",
              "type": "campaign-deactivated",
              "reason": "Goals met",
              "published": false
          }
      ]
  }
  ```

  - 저자의 설명 — **이 표본에서 JSON 문서의 추가 속성인 `outbox`가 발행되어야 하는 도메인
    이벤트의 목록을 담고 있는 것을 볼 수 있다** (9장, p.146).[^khononov2021]
  - **두 구현이 같은 조항의 두 얼굴이다.** 조항은 "상태와 이벤트가 한 원자적 트랜잭션 안에
    들어간다"이고, 그 트랜잭션의 범위가 무엇이냐에 따라 두 테이블이 되기도 하고 한 문서가
    되기도 한다. 저장소가 무엇을 원자적으로 묶어 주느냐가 설계를 정한다.
  - 원문의 세 점(`...`)은 저자가 생략을 표시한 것이고 이 KB가 깎은 것이 아니다.

## 릴레이가 미발행 이벤트를 가져오는 두 방식

- 갈림이 명시된다 (9장, p.146):[^khononov2021]

> The publishing relay can fetch the new domain events in either a pull-based or push-based manner:

- **당기는 쪽 — 폴링 발행자(polling publisher)** (9장, p.146):[^khononov2021]

> The relay can continuously query the database for unpublished events. Proper indexes have to be in
> place to minimize the load on the database induced by the constant polling.

- **미는 쪽 — 트랜잭션 로그 테일링(transaction log tailing)** (9장, p.147):[^khononov2021]

> Here we can leverage the database's feature set to proactively call the publishing relay when new
> events are appended. For example, some relational databases enable getting notifications about
> updated/inserted records by tailing the database's transaction log. Some NoSQL databases expose
> committed changes as streams of events (e.g., AWS DynamoDB Streams).

  - **미는 쪽의 기제가 이 KB에서는 다른 이름으로 이미 들어와 있다** — 트랜잭션 로그를 따라가며
    변경을 흘려보내는 것이
    [변경 데이터 캡처](../concepts/change-data-capture.md)다. 이 판본은 그것을 아웃박스 릴레이의
    구현 선택지로만 지나가고 기제를 설명하지 않는다.

## 보장은 최소 한 번이다

- 저자가 보장의 등급을 못 박는다 (9장, p.147):[^khononov2021]

> It's important to note that the outbox pattern guarantees delivery of the messages at least once:
> if the relay fails right after publishing a message but before marking it as published in the
> database, the same message will be published again in the next iteration.

  - **그러므로 이 패턴은 소비자 쪽에 조건을 하나 넘긴다.** 같은 메시지가 두 번 올 수 있으므로
    소비자가 멱등해야 한다. 그 조건의 정본은
    [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md)와
    [멱등 쓰기 패턴](../concepts/idempotent-write-patterns.md)에 있다.
  - 이 판본은 그 대응을 이 절에서 말하지 않는다. 같은 저자가 5장에서 트랜잭션 스크립트의
    데이터 손상 사례를 다루며 멱등성과 낙관적 동시성을 처방한 것이 그 자리이고, 그 서술은
    [트랜잭션 스크립트](../concepts/transaction-script.md)에 있다.
- 장을 넘기는 문장이 이 패턴의 쓸모를 하나 더 지정한다 — **다음으로 도메인 이벤트의 신뢰성 있는
  발행을 활용해 애그리게이트 설계 원칙이 부과하는 한계 일부를 넘는 법을 보겠다** (9장,
  p.147).[^khononov2021] 그 한계를 넘는 패턴이 [사가 패턴](../concepts/saga-pattern.md)이다.

## 2025년 실무서가 같은 패턴을 레거시 해방 수단으로 다시 세운다

[bellemare2025](../sources/bellemare2025.md) 6장이 이 패턴을 **데이터 해방(data liberation)의 세
패턴 중 하나**로 놓는다. **기제는 이 페이지의 것과 같고, 더해지는 것은 목적과 채점표다.**

- **규정이 이 페이지의 알고리즘 첫 단계와 같다** (6장 §"Liberating Data Using Transactional Outbox
  Tables", p.138):[^bellemare2025]

  > A transactional outbox table is a dedicated database table that acts as a buffer for data to be
  > written to the event stream.

  - 내부 테이블 갱신과 아웃박스 갱신이 **단일 트랜잭션**으로 묶여 **전체 트랜잭션이 성공할 때만**
    반영되고, 별도 비동기 프로세스(전용 CDC 커넥터 같은)가 아웃박스를 소비해 스트림에 쓴 뒤 레코드를
    지운다 (6장, pp.138–139).[^bellemare2025] 위 [알고리즘 네 단계](#알고리즘-네-단계)와 같다.
  - 그쪽이 이 기제를 부르는 말이 하나 더 있다 — **저장소의 트랜잭션 능력과 내구성을 활용해 저장소를
    선행 기록 로그(write-ahead log) 노릇을 하게 만드는 것** (6장, p.138).[^bellemare2025]
- **보장의 등급이 두 소스에서 같다** — 그쪽도 **이 패턴이 주는 것은 최소 한 번 전달**이라고 적는다
  (6장, p.139).[^bellemare2025] 위 [보장은 최소 한 번이다](#보장은-최소-한-번이다)와 문자 그대로
  같은 판정이고, **두 저자가 서로를 호명하지 않는다.**
- **이 페이지가 "엣지 케이스"라 부른 것에 그쪽이 이름을 준다** — **이중 쓰기 안티패턴(dual write
  antipattern)**, 곧 **서비스가 서로 독립인 두 데이터 저장소에 데이터를 쓰는 것**이다 (6장,
  p.129).[^bellemare2025] 위 [틀린 구현 둘](#틀린-구현-둘--커밋한-뒤-애플리케이션-계층이-발행한다)이
  적는 실패가 그 안티패턴의 실물이다.
- **더해지는 것 하나 — 목적이 원자성만이 아니다.** 그쪽은 **아웃박스의 주요 이점 하나가 저장소
  클라이언트가 내부 데이터 모델을 하류 소비자로부터 격리할 수 있다는 것**이라고 적고, **내부 데이터
  모델을 하류에 노출하는 것은 안티패턴**이라는 조문을 상자로 둔다 (6장, p.141).[^bellemare2025]
  - 이 판본은 그 자리를 다루지 않는다 — 여기서 아웃박스에 들어가는 것은 **애그리게이트의 도메인
    이벤트**이고, 그것이 공개 계약인지 내부 모델인지는 물음이 아니다.
- **더해지는 것 둘 — 정렬 식별자에 조항이 붙는다.** 아웃박스 레코드는 **중간 상태가 일어난 순서
  그대로 기록·발행되도록 엄격한 정렬 식별자를 요구**하고, 대안은 **기본 키로 upsert 해 이전 항목을
  덮어쓰고 중간 상태를 포기하는 것**이다 (6장, p.141).[^bellemare2025] 이 판본은 순서를 말하지
  않는다.
- **더해지는 것 셋 — 직렬화를 언제 하느냐가 보장의 등급을 정한다.** 아웃박스에 **쓰기 전** 직렬화하면
  실패가 트랜잭션을 롤백해 내부 테이블과 아웃박스가 동기 상태로 남고, **쓴 뒤** 직렬화하면 이미
  커밋된 트랜잭션이 호환되지 않는 데이터를 아웃박스에 남겨 **발행 불가능한 이벤트가 쌓인다** (6장,
  pp.142–144).[^bellemare2025] 전문은 [데이터 해방](../concepts/data-liberation.md)에 있다.
- **더해지는 것 넷 — 채점표가 붙는다.** 이득 다섯(다중 언어 지원 · 정확히 한 번의 아웃박스 의미론 ·
  이른 스키마 강제 · 내부 데이터 모델 격리 · 비정규화)과 단점 넷(데이터베이스가 트랜잭션을 지원해야
  함 · 애플리케이션 코드 변경 · 업무 프로세스 성능 영향 · 데이터 저장소 성능 영향)이다 (6장,
  p.145).[^bellemare2025] 각 항목의 서술은 [데이터 해방](../concepts/data-liberation.md)에 있다.
  - 대가를 한 문장으로 요약하는 자리도 있다 — 아웃박스는 **변경 데이터 포착 방식 가운데 상대적으로
    침습적**이다. **데이터 저장소나 애플리케이션 계층 중 하나를 고쳐야 하므로 저장소나 애플리케이션
    소유자의 참여가 필요하다** (6장, p.140).[^bellemare2025]
- **모순으로 세우지 않았다.** 두 소스가 같은 대상에 반대 판정을 내리는 자리가 없고, 기제와 보장
  등급에서 정확히 일치한다. **갈리는 것은 무엇을 아웃박스에 넣는가다** — 이 판본은 **애그리게이트가
  낸 도메인 이벤트**를, 그쪽은 **내부 모델에서 골라 낸 공개 계약용 필드**를 넣는다. 그래서 그쪽에만
  격리와 비정규화가 이점으로 붙는다. **이 대비는 이 KB가 두 소스를 맞대어 세운 것이다.** #hypothesis

## 이 문제를 꺼내지 않는 소스

**[ford2021-hard-parts](../sources/ford2021-hard-parts.md) 12장이 서비스를 가로지르는 업무 요청을
통신·일관성·조율 세 축의 여덟 조합으로 펴고, 그 가운데 한 칸(`Anthology Saga(aec)`)은 이 패턴이
겨냥하는 배치와 정확히 겹친다 — 비동기 메시지 큐 · 최종 일관성 · 중앙 조율자 없음이다. 그런데 그
책은 이 페이지의 문제를 한 번도 꺼내지 않는다.**

- **그쪽의 서술은 이렇다** — 이 칸은 **메시지 큐를 써서 오케스트레이션 없이 다른 도메인 서비스로
  비동기 메시지를 보내고**, **각 서비스가 자기 트랜잭션 무결성을 유지한다** (12장,
  p.349).[^ford2021-hard-parts]
- **그 두 문장 사이에 이 페이지의 문제가 있다** — **자기 트랜잭션을 커밋하는 일과 메시지 큐로
  보내는 일은 서로 다른 두 체계에 대한 두 번의 쓰기**이고, 위
  [틀린 구현 둘 — 커밋한 뒤 애플리케이션 계층이 발행한다](#틀린-구현-둘--커밋한-뒤-애플리케이션-계층이-발행한다)가
  적는 실패가 그대로 걸린다. **저자들이 그 틈을 적지 않는다.**
- **부재를 실측으로 적어 둔다** — 스냅샷 전권을 `pdftotext -layout`으로 뽑아 훑은 결과
  **`outbox`가 0건**이고, 12장이 오류 처리로 다루는 것은 **보상 갱신과 사가 상태 기계** 둘뿐이다
  (전권 실측 · 12장, pp.350–356).[^ford2021-hard-parts]
- **이것이 모순은 아니다.** 그 책의 단위는 **서비스와 서비스 사이**이고 이 페이지의 단위는
  **한 서비스 안의 데이터베이스와 메시지 버스 사이**다. 그쪽이 "각 서비스가 자기 트랜잭션
  무결성을 유지한다"고 적을 때 **그 안쪽이 어떻게 되는가는 그쪽의 물음이 아니다.** 최대 하나만
  참일 수 있는가를 물으면 답이 아니오다. `contradicts`를 걸지 않았다. #hypothesis
- **그래서 이 페이지가 그쪽 칸에 더하는 것이 하나 있다** — 그 칸을 실제로 구현하려면
  **각 도메인 서비스 안에 이 패턴이 필요하다.** 그 대응은 이 KB가 세운 것이고 어느 소스도 적지
  않는다. #hypothesis 여덟 칸의 전문은
  [트랜잭셔널 사가 패턴](../concepts/transactional-saga-patterns.md)과
  [트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md)이
  갖는다.

## 이 KB의 다른 자리들과의 분업

이 이름은 이 KB에 이미 여러 곳에 지나가는 말로 있었고, 이 페이지가 그 이름의 정본 자리다.
각 자리가 무엇을 다루는지 적어 둔다.

| 자리 | 그쪽이 다루는 것 | 이 페이지와의 관계 |
|---|---|---|
| [변경 데이터 캡처](../concepts/change-data-capture.md) | 내부 스키마와 외부 스키마를 가르는 수단으로서의 아웃박스 테이블, 그리고 그 대가 둘 | 목적이 다르다. 저쪽은 **스키마 결합**을 끊으려고 쓰고, 이 판본은 **원자성**을 얻으려고 쓴다 |
| [카프카 트랜잭션](../concepts/kafka-transactions.md) | 카프카 트랜잭션이 데이터베이스 갱신과 메시지 발행을 함께 묶어 주지 **않는다**는 사실과 그 우회로 | 같은 문제의 다른 답. 저쪽은 카프카 토픽을 아웃박스로 쓰는 역방향 변종도 적는다 |
| [메시징 엔드포인트 패턴](../concepts/messaging-endpoint-patterns.md) | 2004년의 답 — *Transactional Client*와 XA 분산 트랜잭션 | 같은 이중 쓰기 문제의 20년 전 처방. 이 판본이 기각하는 쪽이다 |
| [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) | 최소 한 번 위에 멱등성을 얹어 효과를 한 번으로 만드는 길 | 이 패턴이 소비자에게 넘기는 조건이 거기서 다뤄진다 |
| [이벤트 기반 애플리케이션 구조](../concepts/event-driven-application-structure.md) | 파이썬 실물에서 이 패턴이 필요해지는 자리 | 같은 문제를 코드 구조 쪽에서 본다 |
| [데이터 해방](../concepts/data-liberation.md) | 레거시 데이터를 스트림으로 꺼내는 네 패턴 중 하나로서의 아웃박스와 그 채점표 | 목적이 둘로 늘어난다. 원자성 **그리고** 내부 모델 격리다 — 위 절이 그 대비다 |

- **이 판본이 더하는 것은 애그리게이트와의 결속이다.** 다른 자리들은 아웃박스를 "데이터베이스와
  메시지 시스템 사이의 이중 쓰기 문제"로 세우고, 이 판본은 **애그리게이트의 도메인 이벤트를
  내보내는 기제**로 세운다. 그래서 여기서만 아웃박스가 사가와 프로세스 매니저의 명령 실행
  기반이 된다.

## 이어지는 페이지

- [도메인 이벤트](../concepts/domain-events.md) — 이 패턴이 내보내는 것
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 그 이벤트가
  나오는 트랜잭션 경계
- [사가 패턴](../concepts/saga-pattern.md) — 이 패턴 위에 서는 첫째 구조
- [프로세스 매니저](../concepts/process-manager.md) — 그 위의 둘째 구조
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 최소 한 번을
  한 번처럼 만드는 쪽
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 트랜잭션 로그 테일링의 정본
- [카프카 트랜잭션](../concepts/kafka-transactions.md) — 같은 문제를 브로커 쪽에서 푸는 시도
- [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md) — 이 패턴이 피해 가는 길
- [트랜잭셔널 사가 패턴](../concepts/transactional-saga-patterns.md) — 이 패턴이
  필요해지는 배치에 이름과 채점을 붙이되 이 문제는 꺼내지 않는 소스
- [트랜잭션 스크립트](../concepts/transaction-script.md) — 같은 저자가 5장에서 같은 문제를 처음 꺼내는 자리
- [데이터 해방](../concepts/data-liberation.md) — 이 패턴을 레거시 해방 수단으로 세우는 쪽
- [비정규화와 이벤트화](../concepts/denormalization-and-eventification.md) — 아웃박스 안에서 조인해 넣는 쪽
- [메시징 패턴](../synthesis/messaging-patterns.md) — 메시징 이름 층의 허브
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 9장 "Communication Patterns" §"Integrating Aggregates"(도입
    pp.143–145 · §Outbox pp.145–146 · §"Fetching unpublished events" pp.146–147). 쪽은 인쇄판
    쪽 번호(PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은
    따옴표는 곧은 따옴표로 옮겼다. 알고리즘 네 단계는 원문이 불릿 목록이라 항목마다 인용
    블록으로 나눠 옮겼다. 도판 둘(Figure 9-11 아웃박스 패턴 · 9-12 아웃박스 테이블)은 도판이라
    본문이 그것에 대해 적는 것만 산문으로 옮겼다. **C# 코드 목록 둘(틀린 구현 둘 —
    `Campaign.Deactivate` pp.143 · `ManagementAPI.DeactivateCampaign` p.144)은 산문으로
    줄였다** — 본문이 그 코드를 행 번호로 짚어 가며 설명하므로 설명만으로 주장이 온전하고,
    개념당 대표 펜스 하나 규약에 따라 이 페이지의 펜스는 아웃박스를 품은 JSON 문서(p.146)
    하나로 두었다. 그 JSON의 세 점(`...`)은 저자가 생략을 표시한 것이고 이 KB가 깎은 것이
    아니다. 언어 표지(`json`)만 더했다.

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, **12장 "Transactional Sagas"
    §"Anthology Saga(aec) Pattern"(pp.349–351) · §"State Management and Eventual
    Consistency"(pp.351–356)**. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). **이 페이지가 그 장에서
    쓰는 것은 한 칸의 기제 서술과 그 장이 오류 처리로 무엇을 다루는가뿐이고**, 칸마다의 직인용과
    채점표 여덟은
    [트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md)과
    [트랜잭셔널 사가 패턴](../concepts/transactional-saga-patterns.md)이 갖는다.
    **`outbox`가 이 책 전권에 0건이라는 것은 스냅샷 전권을 `pdftotext -layout`으로 한 번에 뽑아
    훑은 실측이다.** 부재의 뜻(단위가 달라서인가 빠뜨린 것인가)은 저자들이 적지 않으므로 이
    페이지의 판정에 추정 표시를 붙였다. 두 소스는 서로를 호명하지 않는다.

[^bellemare2025]: Bellemare 2025(2판), **6장 "Integrating Event-Driven Architectures with Existing
    Systems"** — §"The Dual Write Antipattern"(p.129) · §"Liberating Data Using Transactional Outbox
    Tables"(pp.138–146, 하위 §"Performance Considerations" · §"Isolating Internal Data Models" ·
    §"Ensuring Schema Compatibility" · §"Benefits of event production with outbox tables" ·
    §"Drawbacks of event production with outbox tables"). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 24, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고, 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은
    한 낱말로 이었다. 이 소스의 코드 목록(Example 6-1, 내부 모델과 아웃박스의 원자적 갱신 파이썬)과
    표 6-1(아웃박스 테이블 정의)은 **이 페이지로 옮기지 않았다** — 개념당 대표 펜스 하나 규약에 따라
    이 페이지의 펜스는 이미 khononov2021의 JSON 문서가 갖고 있고, 6장 쪽의 표와 절 전문은
    [데이터 해방](../concepts/data-liberation.md)이 갖는다. 두 소스는 서로를 호명하지 않는다.

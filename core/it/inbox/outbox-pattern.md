---
type: concept
title: 아웃박스 패턴
description: 애그리게이트의 상태 변경과 그 도메인 이벤트의 발행을 어긋나지 않게 만드는 패턴 — 애그리게이트 안에서 바로 버스에 올리는 구현이 틀린 두 이유와 애플리케이션 계층으로 옮겨도 남는 실패, 상태와 이벤트를 한 원자적 트랜잭션에 함께 커밋하고 릴레이가 뒤에서 발행한다는 네 단계 알고리즘, 관계형에서는 전용 테이블을 쓰고 다중 문서 트랜잭션이 없는 NoSQL에서는 애그리게이트 레코드에 이벤트를 심는다는 두 구현, 릴레이가 미발행 이벤트를 가져오는 두 방식인 폴링 발행자와 트랜잭션 로그 테일링, 이 패턴이 주는 보장이 최소 한 번이라는 못박음, 그리고 이 KB의 이중 쓰기·변경 데이터 캡처·정확히 한 번 처리 서술과의 분업
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 아웃박스 패턴

- [무엇을 푸는 패턴인가](#무엇을-푸는-패턴인가)
- [틀린 구현 하나 — 애그리게이트가 직접 발행한다](#틀린-구현-하나--애그리게이트가-직접-발행한다)
- [틀린 구현 둘 — 커밋한 뒤 애플리케이션 계층이 발행한다](#틀린-구현-둘--커밋한-뒤-애플리케이션-계층이-발행한다)
- [알고리즘 네 단계](#알고리즘-네-단계)
- [관계형과 NoSQL의 두 구현](#관계형과-nosql의-두-구현)
- [릴레이가 미발행 이벤트를 가져오는 두 방식](#릴레이가-미발행-이벤트를-가져오는-두-방식)
- [보장은 최소 한 번이다](#보장은-최소-한-번이다)
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
- 도메인 이벤트 자체의 규정은 [도메인 이벤트](domain-events.md)에, 애그리게이트의 트랜잭션
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
    [트랜잭션 스크립트](transaction-script.md)에 있다.
- 장을 넘기는 문장이 이 패턴의 쓸모를 하나 더 지정한다 — **다음으로 도메인 이벤트의 신뢰성 있는
  발행을 활용해 애그리게이트 설계 원칙이 부과하는 한계 일부를 넘는 법을 보겠다** (9장,
  p.147).[^khononov2021] 그 한계를 넘는 패턴이 [사가 패턴](saga-pattern.md)이다.

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

- **이 판본이 더하는 것은 애그리게이트와의 결속이다.** 다른 자리들은 아웃박스를 "데이터베이스와
  메시지 시스템 사이의 이중 쓰기 문제"로 세우고, 이 판본은 **애그리게이트의 도메인 이벤트를
  내보내는 기제**로 세운다. 그래서 여기서만 아웃박스가 사가와 프로세스 매니저의 명령 실행
  기반이 된다.

## 이어지는 페이지

- [도메인 이벤트](domain-events.md) — 이 패턴이 내보내는 것
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 그 이벤트가
  나오는 트랜잭션 경계
- [사가 패턴](saga-pattern.md) — 이 패턴 위에 서는 첫째 구조
- [프로세스 매니저](process-manager.md) — 그 위의 둘째 구조
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 최소 한 번을
  한 번처럼 만드는 쪽
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 트랜잭션 로그 테일링의 정본
- [카프카 트랜잭션](../concepts/kafka-transactions.md) — 같은 문제를 브로커 쪽에서 푸는 시도
- [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md) — 이 패턴이 피해 가는 길
- [트랜잭션 스크립트](transaction-script.md) — 같은 저자가 5장에서 같은 문제를 처음 꺼내는 자리
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

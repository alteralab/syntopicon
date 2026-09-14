---
type: concept
title: CQRS 아키텍처
description: 같은 데이터를 여러 영속 모델로 표현하기 위해 코드베이스를 조직하는 아키텍처 패턴 — 하나의 모델로 모든 필요를 감당할 수 없다는 문제 설정과 폴리글랏 모델링·폴리글랏 영속화라는 두 동기, 이 패턴이 이벤트 소싱에서 나왔으되 그것 없이도 쓸 수 있다는 저자의 분리 선언, 강한 일관성을 갖는 유일한 정본인 명령 실행 모델과 언제든 지우고 다시 만들 수 있는 읽기 모델의 규정, 체크포인트와 캐치업 구독으로 도는 동기 투영과 메시지 버스를 타는 비동기 투영의 기제와 각각의 대가, 명령이 데이터를 돌려줘도 된다는 정정과 그 유일한 제한, 그리고 이 패턴이 필요한 자리
generated: { by: "claude-opus-5", at: "2026-09-15T00:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# CQRS 아키텍처

- [무엇을 푸는 패턴인가](#무엇을-푸는-패턴인가)
- [동기 둘 — 폴리글랏 모델링과 폴리글랏 영속화](#동기-둘--폴리글랏-모델링과-폴리글랏-영속화)
- [이벤트 소싱에서 나왔으되 그것과 묶이지 않는다](#이벤트-소싱에서-나왔으되-그것과-묶이지-않는다)
- [두 종류의 모델](#두-종류의-모델)
- [투영을 어떻게 도는가](#투영을-어떻게-도는가)
- [명령이 데이터를 돌려줘도 된다](#명령이-데이터를-돌려줘도-된다)
- [이 패턴이 필요한 자리](#이-패턴이-필요한-자리)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **같은 업무 데이터를 여러 영속 모델로 두려면 코드베이스를 어떻게 조직하고, 그
모델들을 무엇으로 맞춰 두는가.**

## 무엇을 푸는 패턴인가

- [khononov2021](../sources/khononov2021.md)이 이 패턴을 앞의 두 아키텍처 패턴과 나란히
  세우고 갈리는 축을 하나로 짚는다 (8장 §"Command-Query Responsibility Segregation",
  p.128):[^khononov2021]

> The command-query responsibility segregation (CQRS) pattern is based on the same organizational
> principles for business logic and infrastructural concerns as ports & adapters. It differs,
> however, in the way the system's data is managed. This pattern enables representation of the
> system's data in multiple persistent models.

  - **업무 로직과 인프라를 가르는 방식은 포트와 어댑터와 같다**는 것이 이 문단의 전제다. 그
    조직 원리는 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)에 있고,
    이 페이지는 **데이터 관리**만 다룬다.

## 동기 둘 — 폴리글랏 모델링과 폴리글랏 영속화

- 문제 설정 (8장 §"Polyglot Modeling", p.129):[^khononov2021]

> In many cases, it may be difficult, if not impossible, to use a single model of the system's
> business domain to address all of the system's needs.

  - 저자가 드는 예가 온라인 트랜잭션 처리(OLTP)와 온라인 분석 처리(OLAP)가 같은 데이터의 다른
    표현을 요구한다는 것이다 (8장, p.129).[^khononov2021] 그 두 처리의 갈림은
    [EDW §같은 분리를 OLTP와 OLAP로 부르면](../concepts/enterprise-data-warehouse.md#같은-분리를-oltp와-olap로-부르면)에
    있다.
- 둘째 동기가 저장소 쪽이다 — **완벽한 데이터베이스는 없다**는 관찰이고, 저자가 Greg Young을
  빌려 그것을 이렇게 적는다 (8장, p.129):[^khononov2021]

> all databases are flawed, each in its own way: we often have to balance the needs for scale,
> consistency, or supported querying models.

  - 그래서 대안이 **폴리글랏 영속화(polyglot persistence)** — **여러 데이터베이스를 써서
    서로 다른 데이터 관련 요구를 구현하는 것**이다. 저자의 예는 한 시스템이 문서 저장소를 운영
    데이터베이스로, 컬럼 저장소를 분석·리포팅으로, 검색 엔진을 검색 기능으로 쓰는 구성이다
    (8장, p.129).[^khononov2021]
  - 이 KB에서 같은 판단을 데이터 시스템 쪽에서 하는 자리가
    [데이터 통합](../concepts/data-integration.md)이다 — 하나의 도구로 모든 용법을 감당할 수
    없을 때 무엇을 먼저 정하는가를 묻는다.

## 이벤트 소싱에서 나왔으되 그것과 묶이지 않는다

- 계보가 명시된다 (8장 §"Polyglot Modeling", p.129):[^khononov2021]

> Originally, CQRS was defined to address the limited querying possibilities of an event-sourced
> model: it is only possible to query events of one aggregate instance at a time. The CQRS pattern
> provides the possibility of materializing projected models into physical databases that can be
> used for flexible querying options.

- **그러나 저자가 그 결합을 명시적으로 끊는다** (8장, p.129):[^khononov2021]

> That said, this chapter "decouples" CQRS from event sourcing. I intend to show that CQRS is
> useful even if the business logic is implemented using any of the other business logic
> implementation patterns.

  - **이 선언이 이 페이지가 따로 서는 근거다.** 이 KB의
    [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)는 두 이름을 한 페이지에
    묶어 두는데, 그 페이지가 기대는 소스들도 두 이름을 나란히 규정한다. 이 판본은 한쪽 없이
    다른 쪽을 쓸 수 있다고 적으므로 **두 이름을 붙여 놓는 것이 정의가 아니라 관행**이라는
    사실이 여기서 드러난다. 그 대조는 아래
    [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)에 있다.
  - 역방향의 결합은 남는다 — 이벤트 소싱 도메인 모델을 쓰면 CQRS가 **필수**다. 아래
    [이 패턴이 필요한 자리](#이-패턴이-필요한-자리)를 보라.

## 두 종류의 모델

- 이름대로 **시스템의 모델들이 책임에 따라 분리된다**. 종류가 둘이다 — 명령 실행 모델
  (command execution model)과 읽기 모델(read models)이다 (8장 §Implementation,
  p.129).[^khononov2021]
- **명령 실행 모델** (8장, p.129):[^khononov2021]

> CQRS devotes a single model to executing operations that modify the system's state (system
> commands). This model is used to implement the business logic, validate rules, and enforce
> invariants.

  - 그리고 이 모델에만 붙는 지위가 있다 (8장, p.130):[^khononov2021]

  > The command execution model is also the only model representing strongly consistent data—the
  > system's source of truth. It should be possible to read the strongly consistent state of a
  > business entity and have optimistic concurrency support when updating it.

  - **강한 일관성을 갖는 모델이 하나뿐이라는 것이 이 패턴의 중심 제약이다.** 나머지는 전부
    결국 일관되는(eventually consistent) 사본이고, 그 제약이 아래
    [명령이 데이터를 돌려줘도 된다](#명령이-데이터를-돌려줘도-된다)의 유일한 한계로 되돌아온다.
    무엇이 정본이고 무엇이 파생인가라는 축은
    [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)에 있다.
- **읽기 모델(투영)** — 개수에 제한이 없다. **시스템은 사용자에게 데이터를 보이거나 다른
  시스템에 정보를 공급하는 데 필요한 만큼 모델을 정의할 수 있다** (8장,
  p.130).[^khononov2021] 규정은 이렇다 (8장, p.130):[^khononov2021]

> A read model is a precached projection. It can reside in a durable database, flat file, or
> in-memory cache. Proper implementation of CQRS allows for wiping out all data of a projection and
> regenerating it from scratch. This also enables extending the system with additional projections
> in the future—models that couldn't have been foreseen originally.

  - **"지우고 처음부터 다시 만들 수 있음"이 구현의 적격 기준으로 쓰인다는 데 주의한다.** 그
    성질이 없으면 투영은 파생 데이터가 아니라 또 하나의 정본이 되어 버린다.
- 마지막 조항 (8장, p.130):[^khononov2021]

> Finally, read models are read-only. None of the system's operations can directly modify the read
> models' data.

## 투영을 어떻게 도는가

- 읽기 모델이 돌아가려면 시스템이 **명령 실행 모델의 변경을 모든 읽기 모델로 투영해야 한다**
  (8장 §"Projecting Read Models", p.130).[^khononov2021] 저자가 그 개념을 관계형
  데이터베이스의 구체화 뷰에 견준다 (8장, p.130):[^khononov2021]

> The projection of read models is similar to the notion of a materialized view in relational
> databases: whenever source tables are updated, the changes have to be reflected in the precached
> views.

  그 기법 자체는 [증분 뷰 유지](../concepts/incremental-view-maintenance.md)에 있다.

### 동기 투영 — 체크포인트와 캐치업 구독

- **동기 투영은 캐치업 구독(catch-up subscription) 모델로 OLTP 데이터의 변경을 가져온다**
  (8장, p.130).[^khononov2021] 절차가 셋이다 (8장, p.131):[^khononov2021]
  - **투영 엔진이 마지막으로 처리한 체크포인트 이후에 더해지거나 갱신된 레코드를 OLTP
    데이터베이스에 질의한다.**
  - **투영 엔진이 그 갱신된 데이터로 시스템의 읽기 모델을 재생성하거나 갱신한다.**
  - **투영 엔진이 마지막으로 처리한 레코드의 체크포인트를 저장한다. 이 값이 다음 반복에서
    그 레코드 뒤에 더해지거나 수정된 레코드를 얻는 데 쓰인다.**
- 그래서 요구가 쓰기 쪽으로 되돌아온다 (8장, p.131):[^khononov2021]

> For the catch-up subscription to work, the command execution model has to checkpoint all the
> appended or updated database records. The storage mechanism should also support the querying of
> records based on the checkpoint.

  - 구현 수단이 둘로 제시된다 — 데이터베이스 기능을 쓰거나(SQL Server의 `rowversion` 컬럼이
    행을 삽입·갱신할 때 유일한 증가 번호를 만든다) 그런 기능이 없으면 **증가하는 카운터를
    직접 세어 수정된 레코드마다 붙이는** 맞춤 구현이다 (8장, p.131).[^khononov2021]
- **정확성 조건 하나가 따로 못 박혀 있다** (8장, pp.131–132):[^khononov2021]

> It's important to ensure that the checkpoint-based query returns consistent results. If the last
> returned record has a checkpoint value of 10, on the next execution no new requests should have
> values lower than 10. Otherwise, these records will be skipped by the projection engine, which
> will result in inconsistent models.

  - **이것이 이 기제의 진짜 어려움이다.** 증가 번호를 붙이는 것은 쉽고, **이미 읽어 간
    구간에 나중에 더 작은 번호가 끼어들지 않게 만드는 것**이 어렵다. 같은 문제를 분산에서
    다루는 자리가 [전체 순서의 한계](../concepts/limits-of-total-ordering.md)다.
- 이 방식의 이득 (8장, p.132):[^khononov2021]

> The synchronous projection method makes it trivial to add new projections and regenerate existing
> ones from scratch. In the latter case, all you have to do is reset the checkpoint to 0; the
> projection engine will scan the records and rebuild the projections from the ground up.

### 비동기 투영 — 메시지 버스

- **비동기 투영 시나리오에서는 명령 실행 모델이 커밋된 모든 변경을 메시지 버스에 발행한다.
  시스템의 투영 엔진들이 발행된 메시지를 구독해 읽기 모델을 갱신한다** (8장,
  p.132).[^khononov2021] 그 버스의 규정은
  [발행/구독 메시징](../concepts/publish-subscribe-messaging.md)에 있다.
- 대가가 정직하게 계상된다 (8장 §Challenges, p.132):[^khononov2021]

> Despite the apparent scaling and performance advantages of the asynchronous projection method, it
> is more prone to the challenges of distributed computing. If the messages are processed out of
> order or duplicated, inconsistent data will be projected into the read models.

  - 새 투영을 더하거나 기존 투영을 다시 만드는 것도 더 어려워진다 (8장,
    p.133).[^khononov2021] 순서 어긋남과 중복이 실제로 무엇을 깨는지는
    [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md)와
    [스트림 처리 결함 감내](../concepts/stream-processing-fault-tolerance.md)에 있다.
- **그래서 처방이 "둘 중 하나"가 아니라 "동기 먼저, 비동기는 그 위에"다** (8장,
  p.133):[^khononov2021]

> For these reasons, it's advisable to always implement synchronous projection and, optionally, an
> additional asynchronous projection on top of it.

## 명령이 데이터를 돌려줘도 된다

- 모델의 책임 분리가 먼저 규정된다 (8장 §"Model Segregation", p.133):[^khononov2021]

> A command can only operate on the strongly consistent command execution model. A query cannot
> directly modify any of the system's persisted state—neither the read models nor the command
> execution model.

- **그다음 저자가 흔한 오해 하나를 정면으로 기각한다** (8장, p.133):[^khononov2021]

> A common misconception about CQRS-based systems is that a command can only modify data, and data
> can be fetched for display only through a read model. In other words, the command executing the
> methods should never return any data. This is wrong. This approach produces accidental
> complexities and leads to a bad user experience.

  - 근거는 실패의 보고다 — **명령은 언제나 호출자에게 성공했는지 실패했는지 알려야 한다.
    실패했다면 왜 실패했는가? 검증 문제였는가 기술 문제였는가? 호출자는 명령을 어떻게 고칠지
    알아야 한다** (8장, p.133).[^khononov2021] 그래서
    **Therefore, a command can—and in many cases should—return data;** 라고 적는다.
  - 이득이 둘로 적힌다 — 소비자가 자기 동작에 대한 피드백을 즉시 받으므로 시스템을 쓰기
    쉬워지고, 돌려받은 값을 소비자의 후속 작업 흐름에 바로 써서 **불필요한 데이터 왕복을
    없앤다** (8장, p.133).[^khononov2021]
- **제한은 하나뿐이다** (8장, p.133):[^khononov2021]

> The only limitation here is that the returned data should originate from the strongly consistent
> model—the command execution model—as we cannot expect the projections, which will eventually be
> consistent, to be refreshed immediately.

## 이 패턴이 필요한 자리

- 적용 조건 (8장 §"When to Use CQRS", p.133):[^khononov2021]

> The CQRS pattern can be useful for applications that need to work with the same data in multiple
> models, potentially stored in different kinds of databases.

- 근거가 두 관점으로 나뉜다 (8장, p.133):[^khononov2021]
  - **운영의 관점** — 이 패턴이 도메인 주도 설계의 핵심 가치, 곧 **당면 과업에 가장 효과적인
    모델로 일하고 업무 도메인의 모델을 계속 개선한다**는 가치를 뒷받침한다.
  - **인프라의 관점** — 서로 다른 종류의 데이터베이스의 강점을 활용하게 해 준다. 저자의 예는
    명령 실행 모델을 관계형 데이터베이스에, 전문 검색을 검색 색인에, 빠른 조회를 미리 렌더한
    평면 파일에 두고 **그 저장 기제 전부를 신뢰성 있게 동기화하는** 구성이다.
- 그리고 이벤트 소싱과의 관계가 여기서 역방향으로 다시 나온다 (8장,
  p.134):[^khononov2021]

> Moreover, CQRS naturally lends itself to event-sourced domain models. The event-sourcing model
> makes it impossible to query records based on the aggregates' states, but CQRS enables this by
> projecting the states into queryable databases.

- 장 맺음이 두 방향의 결합을 한 문장으로 정리한다 (8장 §Conclusion,
  p.135):[^khononov2021]

> The CQRS pattern represents the same data in multiple models. Although this pattern is obligatory
> for systems based on the event-sourced domain model, it can also be used in any systems that need
> a way of working with multiple persistent models.

  - **비대칭이 요점이다.** [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)에는 이
    패턴이 **의무**이고, 이 패턴에는 이벤트 소싱이 **선택**이다.
- 이 패턴을 어느 범위에 거는가는 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)의
  아키텍처 패턴 절에 있다 — 저자는 시스템 전체에도 경계 컨텍스트 전체에도 걸지 말라고 적는다.

## 이 KB의 다른 자리들과의 분업

이 낱말은 이 KB에 이미 있고, 이 페이지는 **경계 컨텍스트 하나를 조직하는 아키텍처 패턴**만
갖는다.

- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 같은 이름을 **저장소 수준의
  데이터 모델**로 다루는 자리. 그쪽의 CQRS는 "쓰기 최적화 표현에서 읽기 최적화 표현을
  유도한다는 원칙"이라는 정의이고, 이 페이지의 CQRS는 그 원칙을 **한 경계 컨텍스트의 코드와
  저장소 배치**로 구현한 것이다. 그쪽 페이지가 **애플리케이션 안에서 읽기 경로를 고르는 네
  선택지**도 갖고 있어, 세 층위(데이터 모델 · 읽기 경로 · 아키텍처)가 같은 이름을 쓴다.
  - **두 소스가 이 이름을 다르게 묶는다.** 그쪽 소스는 이벤트 소싱과 CQRS를 한 쌍으로
    규정하고, 이 판본은 둘을 뗄 수 있다고 명시한다. 대상이 어긋나는 것이 아니라 **이 판본이
    더 넓은 적용 범위를 주장하는 것**이라 모순 쌍으로 세우지 않았다 — 그쪽 소스도 CQRS를
    이벤트 소싱 없이 쓸 수 없다고 적지는 않는다.
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 뷰를 어디까지 미리 물질화할지의
  선택을 분석 도구 쪽에서 다루는 자리.
- [쓰기 경로와 읽기 경로](../concepts/write-path-and-read-path.md) — 같은 분리를 데이터
  시스템의 일반 관점으로 놓는 자리.

## 이어지는 페이지

- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 이 패턴을 의무로 만드는 업무 로직 패턴
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 같은 이름의 데이터 모델 판본
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 물려받는 조직 원리
- [계층 아키텍처](../concepts/layered-architecture.md) — 세 아키텍처 패턴 중 첫째
- [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md) — 이 패턴을 어느 범위에
  거는가와 업무 로직 패턴과의 대응
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 정본과 사본을
  가르는 축
- [증분 뷰 유지](../concepts/incremental-view-maintenance.md) — 투영을 효율적으로 갱신하는 기법
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 비동기 투영이 타는 버스
- [전체 순서의 한계](../concepts/limits-of-total-ordering.md) — 체크포인트 질의의 정확성 조건이
  분산에서 부딪히는 문제
- [데이터 통합](../concepts/data-integration.md) — 폴리글랏 영속화를 데이터 시스템 쪽에서 묻는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브
- [데이터플로 아키텍처](../synthesis/dataflow-architecture.md) — 같은 발상이 여러 시스템 사이로
  커지는 축의 허브

[^khononov2021]: Khononov 2021, 8장 "Architectural Patterns"
    §"Command-Query Responsibility Segregation"(도입 p.128 · §"Polyglot Modeling" p.129 ·
    §Implementation 중 §"Command execution model"·§"Read models (projections)" pp.129–130 ·
    §"Projecting Read Models" 중 §"Synchronous projections" pp.130–132·§"Asynchronous
    projections" p.132 · §Challenges pp.132–133 · §"Model Segregation" p.133 ·
    §"When to Use CQRS" pp.133–134) · §Conclusion p.135. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 도판 다섯(Figure 8-12 CQRS 아키텍처 · 8-13 동기 투영 모델 ·
    8-14 캐치업 구독 시퀀스 · 8-15 관계형 데이터베이스의 자동 생성 체크포인트 컬럼 ·
    8-16 비동기 투영)은 도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다. 이 절에는
    코드 목록이 없어 펜스를 두지 않았다. 저자가 대는 출처 하나(Greg Young의 "Polyglot data"
    유튜브 강연)는 이 KB가 확인한 원전이 아니다. 장 끝 연습문제 다섯(pp.135–136)은 claim이
    아니라 옮기지 않았다.

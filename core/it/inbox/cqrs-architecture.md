---
type: concept
title: CQRS 아키텍처
status: draft
description: 같은 데이터를 여러 영속 모델로 표현하기 위해 코드베이스를 조직하는 아키텍처 패턴 — 하나의 모델로 모든 필요를 감당할 수 없다는 문제 설정과 폴리글랏 모델링·폴리글랏 영속화라는 두 동기, 이 패턴이 이벤트 소싱에서 나왔으되 그것 없이도 쓸 수 있다는 저자의 분리 선언, 강한 일관성을 갖는 유일한 정본인 명령 실행 모델과 언제든 지우고 다시 만들 수 있는 읽기 모델의 규정, 체크포인트와 캐치업 구독으로 도는 동기 투영과 메시지 버스를 타는 비동기 투영의 기제와 각각의 대가, 명령이 데이터를 돌려줘도 된다는 정정과 그 유일한 제한, 그리고 이 패턴이 필요한 자리, 그리고 이 배치를 패턴 이름 없이 서술하면서 그 반대를 안티패턴으로 세우는 소스, 같은 읽기 모델을 남의 서비스가 낸 상태 이벤트에서 구체화하는 이벤트 기반 쪽 소스, 그리고 이 패턴을 통신이자 데이터 패턴으로 세우며 채택 동기로 읽기와 쓰기의 양이 크게 다른 것과 보안 때문에 읽기를 쓰기에서 격리하려는 것을 대고 쓰기 저장소가 데이터베이스가 아니라 내구성 있는 메시지 큐일 수도 있다고 적는 2025년 소스
generated: { by: "claude-opus-5", at: "2026-09-18T12:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
  - { id: ford2022-evolutionary, resource: /it/sources/ford2022-evolutionary.md }
  - { id: bellemare2025, resource: /it/sources/bellemare2025.md }
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
  - { id: richards2025, resource: /it/sources/richards2025.md }
---

# CQRS 아키텍처

- [무엇을 푸는 패턴인가](#무엇을-푸는-패턴인가)
- [동기 둘 — 폴리글랏 모델링과 폴리글랏 영속화](#동기-둘--폴리글랏-모델링과-폴리글랏-영속화)
- [이벤트 소싱에서 나왔으되 그것과 묶이지 않는다](#이벤트-소싱에서-나왔으되-그것과-묶이지-않는다)
- [두 종류의 모델](#두-종류의-모델)
- [투영을 어떻게 도는가](#투영을-어떻게-도는가)
- [명령이 데이터를 돌려줘도 된다](#명령이-데이터를-돌려줘도-된다)
- [이 패턴이 필요한 자리](#이-패턴이-필요한-자리)
- [15장이 이 패턴을 경계 밖으로 내보내는 자리](#15장이-이-패턴을-경계-밖으로-내보내는-자리)
- [16장이 이 패턴을 분석 모델 생성에 쓴다](#16장이-이-패턴을-분석-모델-생성에-쓴다)
- [확장 수단으로 볼 때의 채점](#확장-수단으로-볼-때의-채점)
- [포트와 어댑터의 예인가 — 원전의 답](#포트와-어댑터의-예인가--원전의-답)
- [통신 패턴으로 다시 세우는 소스 — 채택 동기 둘이 여기서 나온다](#통신-패턴으로-다시-세우는-소스--채택-동기-둘이-여기서-나온다)
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
    [EDW §같은 분리를 OLTP와 OLAP로 부르면](../concepts/enterprise-data-warehouse.md)에
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

- **모델이 여럿이라는 것이 경계 컨텍스트의 정의와 부딪히지 않는가**라는 물음이 이 장 연습문제로
  나오고, 그 답이 부록 B에 있다 — **CQRS 패턴이 투영해 낸 여러 모델을 다루는 것은 경계
  컨텍스트가 모델의 경계여야 한다는 요구와 모순되지 않는다. 그 모델 중 하나만이 진실의
  원천으로 정의되고 애그리게이트의 상태를 바꾸는 데 쓰이기 때문이다** (부록 B,
  p.292).[^khononov2021]
  - **이 문장이 위 두 인용을 하나의 판정으로 묶는다.** 명령 실행 모델만 강한 일관성을 갖고
    읽기 모델은 읽기 전용이므로, **경계 컨텍스트가 "단일 모델"이라 말할 때의 그 모델은 명령
    실행 모델**이다. 그 정의는 [경계 컨텍스트](../concepts/bounded-context.md)에 있다.
  - 이 판정이 장 본문에는 없고 연습문제의 답에만 적혀 있어 여기 옮겼다.

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
- 이 패턴을 어느 범위에 거는가는 [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md)의
  아키텍처 패턴 절에 있다 — 저자는 시스템 전체에도 경계 컨텍스트 전체에도 걸지 말라고 적는다.

## 15장이 이 패턴을 경계 밖으로 내보내는 자리

**같은 판본의 15장이 이 패턴의 투영을 통합 설계의 도구로 쓴다.** 위
[두 종류의 모델](#두-종류의-모델)이 한 경계 컨텍스트 안의 읽기 모델을 다뤘다면, 15장은 그
읽기 모델을 **다른 경계 컨텍스트에 내주는** 경우를 다룬다.

- 15장이 기각하는 설계는 그 반대다 — 생산자가 자기 도메인 이벤트를 전부 드러내고 **소비자마다
  같은 투영을 각자 구현하는 것**이다. 그러면 같은 업무 로직이 여러 경계 컨텍스트에 중복되고
  (기능 결합), 생산자의 구현 변경이 구독자를 깨뜨린다(구현 결합) (15장, p.243).[^khononov2021]
- **처방이 투영 로직을 생산자 안으로 옮기는 것이다** — 생산자가 소비자 주도 계약
  (consumer-driven contract) 패턴을 따라 **소비자가 필요로 하는 모델을 스스로 투영하고 그것을
  자기 공표된 언어의 일부로 만든다**. 그러면 소비자는 필요한 데이터를 전부 얻으면서 생산자의
  구현 모델을 알지 못한다 (15장, p.244).[^khononov2021]
- **그렇게 내보낸 메시지가 ECST다.** 이벤트가 실어 나르는 상태 전이(event-carried state
  transfer)는 개념적으로 **비동기 데이터 복제 기제**이고, 그 흐름이 소비자에게 생산자 데이터의
  로컬 캐시를 갖게 해 준다 (15장, p.238).[^khononov2021]
- **두 이름이 같은 대상을 가리키는가.** 아니다 — 대질하면 축이 다르다.
  - **투영은 모델을 만드는 기제**이고(위 [투영을 어떻게 도는가](#투영을-어떻게-도는가)),
    **ECST는 경계를 건너는 메시지의 종류**다. 앞엣것은 어디에 두든 성립하고, 뒤엣것은 경계가
    있어야 성립한다.
  - 그러나 15장의 리팩터링은 **둘을 잇는다** — 생산자 안에서 투영한 모델을 ECST로 내보내는 것이
    그 처방이다. 그래서 소비자 쪽에서 보면 로컬 캐시가 생기고, 생산자 쪽에서 보면 읽기 모델이
    하나 더 생긴 것이다.
  - #hypothesis 그래서 **소비자가 유지하는 로컬 캐시도 이 페이지의 읽기 모델과 같은 성질을
    갖는다** — 버릴 수 있고 처음부터 다시 만들 수 있다. 저자가 그 대응을 명시한 적은 없어
    가설로 적는다.
- 세 종류의 이벤트와 그중 무엇을 고를지의 어림법은
  [이벤트 주도 통합 설계](event-driven-integration-design.md)에 있다.

## 16장이 이 패턴을 분석 모델 생성에 쓴다

**같은 판본의 16장이 이 패턴에 넷째 쓰임을 준다** — 운영 모델을 분석 모델로 바꾸는 것이다.

- 규정 (16장 §"Combining Data Mesh and Domain-Driven Design", pp.263–264):[^khononov2021]

> The CQRS pattern makes it easy to generate multiple models of the same data. It can be leveraged
> to transform the operational model into an analytical model.

- **모델을 처음부터 다시 만들 수 있다는 성질이 여기서 값을 낸다** — 그 능력 덕에 **분석 모델의
  여러 버전을 동시에 생성해 서빙하는 것**이 쉬워진다 (16장, p.264).[^khononov2021] 위
  [투영을 어떻게 도는가](#투영을-어떻게-도는가)가 적는 재생성 절차가 그 근거다.
- 저자는 이 패턴을 **데이터 메시 구현을 떠받치는 아키텍처 패턴**으로 꼽는다 (16장 §Conclusion,
  p.264).[^khononov2021] 그 아키텍처는 [데이터 메시](../concepts/data-mesh.md)에 있고, 분석
  모델의 버저닝 요구는
  [제품으로서의 데이터 원칙](../concepts/data-as-a-product-principle.md)에 있다.

## 확장 수단으로 볼 때의 채점

**다른 소스 하나가 이 패턴을 확장의 수단으로 놓고 채점한다.** 2021년 마이크로서비스 실무서가
확장을 다루는 장 안에 이 패턴의 곁글을 두었다 (13장 곁글 §"CQRS and Event Sourcing",
pp.434–435).[^newman2021] 그쪽의 규정은 위 절들과 어긋나지 않는다 — 읽기와 쓰기의 책임을 별도
모델이 맡고, 그 둘을 **별도 단위로 배포하면 읽기와 쓰기를 독립적으로 확장할 수 있다**는 것이
그쪽이 드는 이 패턴의 확장 쪽 값어치다.

- **읽기 복제본과의 유비를 저자가 직접 세운다** — CQRS는 **데이터 층에서 읽기 복제본이 하는
  일과 아주 비슷한 것을 애플리케이션 층에서 한다**고 적고, 다만 구현 방식이 너무 다양해서
  이것이 단순화라는 단서를 곧바로 붙인다 (13장, p.434).[^newman2021]
- **판정은 조심스럽다** (13장, pp.434–435).[^newman2021] 저자는 어떤 상황에서는 값어치를
  보면서도 **잘 해내기 어려운 패턴**이라고 적고, 아주 똑똑한 사람들이 이것을 돌아가게 만드는 데
  작지 않은 문제를 겪는 것을 봤다고 덧붙인다. 그래서 **확장 수단으로 고려한다면 더 어려운
  축으로 여기고 쉬운 것부터 해 보라**고 권한다 — **단지 읽기에 제약이 걸린 것이라면 읽기
  복제본이 훨씬 덜 위험하고 더 빠른 출발점**이라는 것이다.
  - 같은 걱정을 이벤트 소싱에도 건다 — 아주 잘 맞는 상황이 있지만 감당해야 할 골칫거리가
    딸려 오고, **두 패턴 다 개발자에게 상당한 사고방식의 전환을 요구**하므로 그 인지 부하가
    값하는지 확인하라고 적는다 (13장, p.435).[^newman2021]
  - 위 §"이 패턴이 필요한 자리"가 적는 조건과 **방향이 같고 재는 것이 다르다.** 이쪽은
    **무엇이 이 패턴을 요구하는가**를 묻고, 그쪽은 **확장이라는 목적에 대해 이 패턴이 얼마나
    비싼 수단인가**를 묻는다. 겨루지 않는다.
- **서비스 경계에 대한 조항 하나가 더 붙는다** (13장, p.435).[^newman2021] 마이크로서비스
  아키텍처의 관점에서 이 패턴들을 쓸지 말지는 **그 마이크로서비스의 내부 구현 세부**다. 읽기와
  쓰기의 책임을 다른 프로세스와 모델로 갈랐다면 그것이 **소비자에게 보이지 않아야** 하고, 들어온
  요청을 알맞은 모델로 돌리는 일도 그 마이크로서비스의 책임이어야 한다. 그래야 나중에 마음을
  바꿀 자유가 남는다.
  - 이것은 위 §"15장이 이 패턴을 경계 밖으로 내보내는 자리"와 **층이 다르다.** 그쪽은
    투영한 모델을 경계 밖으로 **내보내는** 통합 설계이고, 이쪽은 **패턴을 쓴다는 사실 자체를
    감추라**는 인터페이스 조항이다.
- 그 실무서가 이 패턴을 놓은 확장 축 전체는 [확장의 네 축](four-axes-of-scaling.md)에 있다.

## 포트와 어댑터의 예인가 — 원전의 답

- 포트와 어댑터의 원저자 콕번이 이 물음에 직접 답한 자리가 있다. 그는 2010년 강연에서 CQRS가
  헥사고날 아키텍처의 예인지 물었고, 팻 매독스(Pat Maddox)와 함께 그 전개를 짚은 뒤 이렇게
  결론지었다 — **CQRS는 포트와 어댑터를 쓸 수 있으나, 그 자체로는 포트와 어댑터의 예가 아니다**
  (5장 §"5.9. Is CQRS an example of Ports & Adapters?").[^cockburn2024]
- 이 답은 위 [무엇을 푸는 패턴인가](#무엇을-푸는-패턴인가)가 도메인 주도 설계 입문서를 근거로
  적은 것("CQRS가 업무 로직과 인프라를 가르는 조직 원리는 포트와 어댑터와 같다")과 **충돌하지
  않는다.** 콕번도 부분에서는 같은 것을 인정한다 — 명령 부분과 조회 부분은 둘 다 경계 지어진
  하위 체계이고, 구동·피구동 기술로부터 분리되면 각각 포트와 어댑터의 예가 된다는 것이다. 다만
  콕번은 층위를 좁힌다 — **온전한 CQRS 체계는 업무 로직 부분만이 아니라 외부 기술 부분(저장소와
  UI)까지 포함하므로, 체계 전체는 포트와 어댑터의 예가 아니다** (5장 §"5.9").[^cockburn2024]
  두 서술은 대상의 층위가 다르므로(입문서는 조직 원리의 동일성, 원전은 체계 전체의 정체) 모순 쌍으로
  세우지 않았다. 전문은 [포트와 어댑터와 이웃 개념](../concepts/ports-and-adapters-related-concepts.md)의
  "CQRS는 포트와 어댑터의 예인가"에 있다.

## 통신 패턴으로 다시 세우는 소스 — 채택 동기 둘이 여기서 나온다

[richards2025](../sources/richards2025.md)는 이 패턴을 **아키텍처 패턴을 다루는 장**에 놓고
**많은 분산 아키텍처(그리고 몇몇 모놀리식 아키텍처)에 나타나는 또 하나의 흔한 통신 패턴**이라
부른다 (20장 §"CQRS", p.378).[^richards2025] **이 KB의 다른 소스들은 이것을 데이터 모델이나
코드베이스 조직의 패턴으로 세웠는데 이 소스는 통신 패턴으로 먼저 부른다.**

- **규정** — **CQRS는 쓰기를 데이터 저장소 하나로 격리하고, 그 저장소가 읽기 요청을 받는 다른
  데이터베이스로 데이터를 동기화한다(대개 비동기로)** (20장, p.378).[^richards2025]
  - **쓰기 저장소가 데이터베이스가 아닐 수 있다는 단서가 붙는다** — **대개 데이터베이스이지만
    때로는 내구성 있는 메시지 큐(durable message queue) 같은 다른 인프라**다 (20장,
    p.378).[^richards2025]
    - **이 KB에 가까운 서술이 하나 있었다** —
      [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)가 **로그 기반 메시지
      브로커를 이벤트 로그 저장에 쓸 수 있다**고 적는다. **이 소스가 더하는 것은 그것을 CQRS의
      쓰기 저장소 자리에 놓고 "큐"라는 낱말로 부르는 것**이다.
- **채택 동기 둘이 명시된다 — 이 KB의 공백이던 자리다** (20장, p.378):[^richards2025]
  - **읽기와 쓰기의 양이 뚜렷이 다른 체계**(stark differences between read and write volumes).
  - **보안을 비롯한 관심사 때문에 읽기를 쓰기에서 격리하려는 체계.**
  - **이 페이지의 위 [이 패턴이 필요한 자리](#이-패턴이-필요한-자리)는 동기를 "같은 데이터를
    여러 모델로 다뤄야 하는 애플리케이션"으로 적고, 양의 비대칭도 보안도 들지 않았다.**
    [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)도 마찬가지다. **이 소스가
    그 둘을 채운다.**
- **이 소스가 대비로 세우는 것이 클라이언트/서버다** — **애플리케이션이 데이터베이스를 질의하고
  데이터베이스를 애플리케이션 인프라의 일부로 써서 트랜잭션 쓰기를 수행하는 흔한 배치**이고,
  그림 20-3이 그것을 CQRS와 나란히 그린다 (20장, p.378, 그림 20-3).[^richards2025]
  - **그림 20-3에만 있는 것** — 왼쪽은 애플리케이션 상자 하나와 `Read/write`라 적힌 원통 하나가
    양방향 화살표로 이어지고, 오른쪽은 같은 애플리케이션 상자에서 `Write` 원통으로 내려가는
    화살표, `Write`에서 `Read` 원통으로 가는 화살표, `Read`에서 애플리케이션으로 올라오는
    화살표로 **삼각형**을 이룬다 (렌더해 확인). **본문이 그 방향을 말로 적지 않는다.**
- **무엇을 얻는가** — **읽기와 쓰기를 가르면 데이터에 따라 서로 다른 아키텍처 특성을 격리할 수
  있고, 필요하면 데이터베이스마다 다른 데이터 모델을 쓸 수도 있다** (20장,
  p.378).[^richards2025]
  - **뒷부분은 이 페이지가 이미 갖는다**(위 §"동기 둘"의 폴리글랏 모델링·폴리글랏 영속화).
    **앞부분이 새것이다** — **아키텍처 특성을 데이터 종류별로 가르는 수단**으로 이 패턴을 읽는
    것이고, 이 소스는 그것을 맺음으로도 되풀이한다: **CQRS는 데이터 역량의 종류·보안 관심사·
    그 밖에 물리적 분리에서 이득을 보는 요인에 따라 서로 다른 아키텍처 특성을 가능하게 하는
    데이터 통신 패턴의 좋은 예**다 (20장, p.378).[^richards2025]
- **이 소스는 이벤트 소싱을 함께 부르지 않는다.** CQRS를 다루는 이 절 전체에 이벤트 소싱이라는
  낱말이 없다. **위 §"이벤트 소싱에서 나왔으되 그것과 묶이지 않는다"의 분리 선언과 같은 방향이고
  더 멀리 간다** — 이쪽은 계보조차 부르지 않는다. #hypothesis
- **동기·비동기의 방향이 이 KB의 다른 소스와 반대다** — khononov2021은 **동기 투영을 언제나
  구현하고 비동기는 그 위에 선택적으로 얹으라**고 처방하는데, 이 소스는 **동기화가 대개
  비동기**라고 적는다. **모순은 아니다** — 앞은 처방이고 뒤는 관찰이다. `contradicts`를 걸지
  않았다. #hypothesis
- **이 소스에서 이 절이 놓인 자리 자체가 주장이다** — 저자들은 이 장에서 **패턴과 그 구현을
  가르는 일**을 되풀이하고, CQRS를 **오케스트레이션·코레오그래피와 나란히** 통신 패턴으로
  늘어놓는다. 그 틀은 [패턴과 구현의 가름](pattern-versus-implementation.md)에 있다.

## 이 KB의 다른 자리들과의 분업

이 낱말은 이 KB에 이미 있고, 이 페이지는 **경계 컨텍스트 하나를 조직하는 아키텍처 패턴**만
갖는다.

- [패턴과 구현의 가름](pattern-versus-implementation.md) — 이 패턴을 통신 패턴으로
  늘어놓는 장의 틀
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 같은 이름을 **저장소 수준의
  데이터 모델**로 다루는 자리. 그쪽의 CQRS는 "쓰기 최적화 표현에서 읽기 최적화 표현을
  유도한다는 원칙"이라는 정의이고, 이 페이지의 CQRS는 그 원칙을 **한 경계 컨텍스트의 코드와
  저장소 배치**로 구현한 것이다. 그쪽 페이지가 **애플리케이션 안에서 읽기 경로를 고르는 네
  선택지**도 갖고 있어, 세 층위(데이터 모델 · 읽기 경로 · 아키텍처)가 같은 이름을 쓴다.
  - **두 소스가 이 이름을 다르게 묶는다.** 그쪽 소스는 이벤트 소싱과 CQRS를 한 쌍으로
    규정하고, 이 판본은 둘을 뗄 수 있다고 명시한다. 대상이 어긋나는 것이 아니라 **이 판본이
    더 넓은 적용 범위를 주장하는 것**이라 모순 쌍으로 세우지 않았다 — 그쪽 소스도 CQRS를
    이벤트 소싱 없이 쓸 수 없다고 적지는 않는다.
- **같은 배치를 이름 없이 서술하는 소스가 하나 더 있다.** 진화적 아키텍처 쪽이 **기록 시스템
  위에 리포팅 얹기**를 안티패턴으로 세우고 그 처방으로 **이벤트 스트림을 듣는 리포팅 서비스
  묶음이 리포팅에 최적화된 비정규화된 저장소를 채우는 구성**을 적는데, **이 페이지의 어휘로는
  그것이 비동기 투영으로 유지되는 읽기 모델이다.** 다만 **그쪽은 CQRS라는 이름을 쓰지 않고**
  경계 컨텍스트가 아니라 서비스 여럿에 걸친 배치로 적으며, 이 페이지가 갖는 것(정본 모델의
  유일성, 체크포인트와 캐치업 구독, 읽기 모델을 언제든 다시 만들 수 있다는 규정)에 해당하는
  서술이 없다 (8장 §"Antipattern: Reporting Atop the System of Record",
  pp.189–190).[^ford2022-evolutionary] **이름의 대응은 이 KB가 세운 것이다.** #hypothesis 그쪽
  서술의 전문은
  [진화적 아키텍처의 함정과 안티패턴](evolutionary-architecture-antipatterns.md)과
  [기록 시스템과 파생 데이터](system-of-record-and-derived-data.md)에 있다.
- **읽기 모델의 재료를 남의 서비스에서 받는 경우가 하나 더 있다.** 이벤트 기반 쪽 소스가 상태
  이벤트의 이득으로 **구체화**를 드는데 — **이벤트 스트림을 소비해 서비스가 필요로 하는 데이터를
  자기 상태 저장소로 구체화하면 된다**는 것이다 (5장 §"State Events and Event-Carried State
  Transfer", p.99).[^bellemare2025] **이 페이지의 읽기 모델과 같은 물건인데 재료의 출처가 다르다** —
  이 페이지의 투영은 **같은 경계 컨텍스트 안의 명령 실행 모델**에서 나오고, 그쪽의 구체화는
  **다른 서비스가 낸 현재 상태 이벤트 스트림**에서 나온다. 그리고 그쪽이 **델타 이벤트로 그것을
  하지 말라**고 처방하는 이유가 이 페이지의 읽기 모델 규정과 맞물린다 — 델타로는 소비자마다 집계
  로직을 복제해야 하므로 **읽기 모델을 언제든 지우고 다시 만들 수 있다**는 성질이 값싸지 않게
  된다. **이 맞물림은 이 KB가 두 원문을 맞대어 세운 것이다.** 전문은
  [이벤트 설계 - 상태와 델타](event-design-state-versus-delta.md)에 있다.
- **같은 소스의 8장이 그 읽기 모델과 같은 물건을 외부 상태 저장소라 부른다.** 거기서도 **요구가
  바뀌면 마이그레이션하지 말고 상태 저장소를 다시 지으라**고 처방하고, 절차가 이 페이지의 읽기 모델
  재생성과 같은 모양이다 — **새 저장소 인스턴스를 만들고 컨슈머 오프셋을 스트림 맨 처음으로 되감아
  다시 채운다** (8장 §"Rebuilding the External State Store", pp.188–189).[^bellemare2025]
  **다른 것은 재료의 출처다** — 이 페이지의 투영은 같은 경계 컨텍스트 안의 명령 실행 모델에서
  나오고, 그쪽의 구체화는 입력 이벤트 스트림에서 나온다. **그쪽은 CQRS라는 이름을 8장에서 쓰지
  않으므로 이 대응은 이 KB가 세운 것이다.** #hypothesis 전문은
  [상태 있는 마이크로서비스와 상태 저장소](stateful-microservices-and-state-stores.md)에 있다.
  - **같은 소스의 17장이 그 외부 상태 저장소를 요청-응답으로 읽히는 자리까지 적는다** — 상태를
    구체화하는 서비스와 요청-응답 API를 **한 서비스에 두는 올인원 구성**과 **둘로 가른 컴포지트
    서비스** 둘인데, 뒤엣것은 **논리적으로 독립이되 단일 경계 컨텍스트를 공유하고 긴밀히 결합된
    채로 남는다** (17장, pp.346–348).[^bellemare2025] **이 페이지의 "패턴을 쓴다는 사실 자체를
    소비자에게 감추라"는 조항이 그 구성에도 그대로 걸린다** — 17장도 **상태 저장소에 직접
    접근하지 말고 마이크로서비스의 요청-응답 API를 통하라**고 못 박는다 (17장,
    p.346).[^bellemare2025] 전문은
    [요청-응답과 이벤트 기반의 통합](request-response-and-event-driven-integration.md)에 있다.
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 뷰를 어디까지 미리 물질화할지의
  선택을 분석 도구 쪽에서 다루는 자리.
- [쓰기 경로와 읽기 경로](../concepts/write-path-and-read-path.md) — 같은 분리를 데이터
  시스템의 일반 관점으로 놓는 자리.

## 이어지는 페이지

- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 이 패턴을 의무로 만드는 업무 로직 패턴
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 같은 이름의 데이터 모델 판본
- [진화적 아키텍처의 함정과 안티패턴](evolutionary-architecture-antipatterns.md) — 이 배치를 이름 없이 서술하며 그 반대를 안티패턴으로 세우는 쪽
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 물려받는 조직 원리
- [포트와 어댑터와 이웃 개념](../concepts/ports-and-adapters-related-concepts.md) — 원전이 CQRS가
  포트와 어댑터의 예인지 답하는 자리
- [계층 아키텍처](../concepts/layered-architecture.md) — 세 아키텍처 패턴 중 첫째
- [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md) — 이 패턴을 어느 범위에
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
- [이벤트 주도 통합 설계](event-driven-integration-design.md) — 투영한 모델을 경계 밖으로
  내보내는 쪽
- [이벤트 설계 - 상태와 델타](event-design-state-versus-delta.md) — 읽기 모델의 재료를 남의
  서비스가 낸 상태 이벤트에서 받는 쪽
- [데이터 메시](../concepts/data-mesh.md) — 이 패턴이 분석 모델 생성에 쓰이는 자리
- [확장의 네 축](four-axes-of-scaling.md) — 이 패턴을 확장 수단으로 놓고 다른 축들과 견주는 자리
- [복제 지연이 만드는 이상](../concepts/replication-lag-anomalies.md) — 저자가 이 패턴의 더
  값싼 대안으로 드는 읽기 복제본의 전제와 대가
- [상태 있는 마이크로서비스와 상태 저장소](stateful-microservices-and-state-stores.md) — 같은
  읽기 모델을 외부 상태 저장소라 부르고 마이그레이션 대신 다시 지으라고 처방하는 쪽

[^newman2021]: Newman 2021, *Building Microservices* 2판(O'Reilly, 2021) 13장 "Scaling"
    곁글 §"CQRS and Event Sourcing"(pp.434–435). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    이 곁글에는 직인용으로 옮길 규정 문장이 없어 전부 한국어 재서술이고 도판도 코드도 없다.
    이 소스는 이 패턴의 원전이 아니라 **확장 수단으로 채점하는 소비자**다. 그 장 전체는
    [확장의 네 축](four-axes-of-scaling.md)이 갖는다.

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
    **15장 "Event-Driven Architecture"(§"Event-carried state transfer" p.238 ·
    §"Implementation Coupling" p.243 · §"Refactoring the Event-Driven Integration" p.244)와
    16장 "Data Mesh"(§"Combining Data Mesh and Domain-Driven Design" pp.263–264 ·
    §Conclusion p.264)도 이 페이지에 합류했다.** 세 이벤트 종류와 설계 휴리스틱은
    [이벤트 주도 통합 설계](event-driven-integration-design.md)에, 데이터 메시 네 원칙은
    [데이터 메시](../concepts/data-mesh.md)에 두었고 이 페이지는 이 패턴에 걸리는 것만 받았다.
    16장의 도판 하나(Figure 16-15, 두 스키마 버전의 분석 데이터를 동시에 서빙하는 그림)는
    도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다.
    **부록 B의 8장 5번 답(p.292)도 이 페이지에 합류했다** — 이 패턴의 여러 모델이 경계
    컨텍스트의 모델 경계 요구와 어떻게 양립하는지가 장 본문에 없고 그 답에만 적혀 있다.
    부록 B는 연습문제의 답이고 문항 자체는 claim이 아니라 옮기지 않았다.

[^ford2022-evolutionary]: Ford·Parsons·Kua·Sadalage 2022(2판), 8장 "Evolutionary Architecture
    Pitfalls and Antipatterns" §"Antipattern: Reporting Atop the System of Record"(pp.189–190).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 22, 실측). 이 소스는 이 페이지에 **한 줄만** 더한다 —
    직인용을 두지 않았고, 그 절의 전문은
    [기록 시스템과 파생 데이터](system-of-record-and-derived-data.md)와
    [진화적 아키텍처의 함정과 안티패턴](evolutionary-architecture-antipatterns.md)이 갖는다.
    **이 소스는 CQRS라는 이름을 쓰지 않는다** — 이름의 대응은 이 KB가 세운 것이다.

[^bellemare2025]: Bellemare 2025(2판), 5장 "Designing Events"
    §"State Events and Event-Carried State Transfer"(p.99)**와 8장 "Stateful Event-Driven
    Microservices" §"Rebuilding the External State Store"(pp.188–189)**와
    **17장 §"Serving Data Using a Request-Response API"(pp.346–348)**. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 24, 실측). 이 소스는 이 페이지에 **세 줄만** 더한다 — 직인용을 두지 않았고, 세 장의
    전문은 [이벤트 설계 - 상태와 델타](event-design-state-versus-delta.md)와
    [상태 있는 마이크로서비스와 상태 저장소](stateful-microservices-and-state-stores.md)와
    [요청-응답과 이벤트 기반의 통합](request-response-and-event-driven-integration.md)이 갖는다.
    **이 소스는 CQRS라는 이름을 쓰지 않는다** — 이름의 대응은 이 KB가 세운 것이다.

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 5장 §"5.9. Is CQRS an example of Ports &
    Adapters?". 이 소스는 이 페이지에 **한 절만** 더한다 — 직인용을 두지 않았고(콕번의 결론은
    강연 회고의 산문이라 옮길 정의 문장이 없다), 그 절의 전문은
    [포트와 어댑터와 이웃 개념](../concepts/ports-and-adapters-related-concepts.md)이 갖는다.
    EPUB(Calibre 변환본), 쪽 앵커 없음 — locator는 장·절 번호.

[^richards2025]: Richards·Ford 2025(2판) *Fundamentals of Software Architecture* 20장
    "Architectural Patterns" §"CQRS"(p.378, 그림 20-3). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 24, 실측).
    **직인용이 없다** — 굵은 글씨가 원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다. 그림
    20-3은 `pdftoppm -r 160 -png`으로 렌더해 눈으로 확인했다(`pdftext.py` 추출은 도판을 통째로
    건너뛴다). **저자 겹침 주의** — 닐 포드가 이 KB의 ford2021-hard-parts·ford2022-evolutionary
    저자에도 들어 있으나, 이 절의 내용은 그 두 책이 다루지 않는 자리라 겹침이 없다.

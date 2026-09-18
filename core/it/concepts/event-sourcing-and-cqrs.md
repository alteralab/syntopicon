---
type: concept
title: 이벤트 소싱과 CQRS
description: 쓰기에 최적화된 표현과 읽기에 최적화된 표현을 아예 갈라 놓는 데이터 모델 — 불변 이벤트 로그를 진실의 원천으로 두고 거기서 구체화 뷰를 유도하는 구조, 명령이 사실이 되는 순간과 과거 시제 명명 규약, 팩트 테이블과 닮았지만 순서가 중요하다는 차이, 재현 가능한 뷰 재계산·감사 로그·되돌릴 수 있음이라는 이점들, 외부 정보·개인 데이터 삭제·부수 효과라는 세 가지 함정, 이 패턴을 실제로 구현하는 쪽이 규정하는 이벤트 저장소의 최소 인터페이스와 낙관적 동시성 인수, 성능이 문제가 되는 문턱과 스냅샷을 정당화하라는 단서, 삭제 요구를 암호 키 삭제로 푸는 잊을 수 있는 페이로드와 같은 해법을 크립토 슈레딩이라 부르며 그 근거 넷과 경계를 적는 셋째 소스, 상태 기반 모델에 로그를 곁들이는 세 대안이 각각 무엇을 못 하는가, 그리고 CQRS를 이벤트 소싱 없이도 쓸 수 있다는 주장
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
sources:
  - { id: reis2022, resource: /it/sources/reis2022.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: bellemare2025, resource: /it/sources/bellemare2025.md }
---

# 이벤트 소싱과 CQRS

- [왜 쓰기와 읽기를 가르는가](#왜-쓰기와-읽기를-가르는가)
- [이벤트 로그](#이벤트-로그)
- [두 이름의 정의](#두-이름의-정의)
- [시간의 차원을 데이터 모델에 들인다](#시간의-차원을-데이터-모델에-들인다)
- [이벤트 저장소](#이벤트-저장소)
- [명령이 사실이 되는 순간](#명령이-사실이-되는-순간)
- [팩트 테이블과 무엇이 다른가](#팩트-테이블과-무엇이-다른가)
- [이점](#이점)
- [함정](#함정)
- [개인 데이터 삭제 — 잊을 수 있는 페이로드](#개인-데이터-삭제--잊을-수-있는-페이로드)
- [무엇으로 구현하는가](#무엇으로-구현하는가)
- [성능이 문제가 되는 문턱과 스냅샷](#성능이-문제가-되는-문턱과-스냅샷)
- [그냥 로그를 남기면 안 되는가](#그냥-로그를-남기면-안-되는가)
- [CDC와 무엇이 다른가](#cdc와-무엇이-다른가)
- [로그 압착이 여기서는 다르게 걸린다](#로그-압착이-여기서는-다르게-걸린다)
- [13장이 이 모델을 감사 가능성의 근거로 삼는다](#13장이-이-모델을-감사-가능성의-근거로-삼는다)
- [이벤트 기반 아키텍처](#이벤트-기반-아키텍처)
- [애플리케이션 안에서 읽기 경로를 고르는 네 선택지](#애플리케이션-안에서-읽기-경로를-고르는-네-선택지)
- [CQRS를 이벤트 소싱 없이 쓸 수 있다는 주장](#cqrs를-이벤트-소싱-없이-쓸-수-있다는-주장)
- [15장이 이 패턴과 이벤트 주도 아키텍처를 가른다](#15장이-이-패턴과-이벤트-주도-아키텍처를-가른다)
- [같은 기제를 서비스 사이 상태 공유로 세우는 셋째 소스](#같은-기제를-서비스-사이-상태-공유로-세우는-셋째-소스)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모든 상태 변화를 불변 이벤트로 적고 읽기용 표현을 거기서 유도하면 무엇을 얻고
무엇을 잃는가.**

## 왜 쓰기와 읽기를 가르는가

- 문제 설정 — **지금까지 논한 모든 데이터 모델에서 데이터는 쓰인 것과 같은 형태로 질의된다 —
  JSON 문서든, 테이블의 행이든, 그래프의 정점과 간선이든. 그러나 복잡한 애플리케이션에서는
  데이터가 질의되고 표현돼야 하는 모든 방식을 만족시킬 수 있는 단일 데이터 표현을 찾기 어려울
  때가 있다. 그런 상황에서는 데이터를 한 형태로 쓰고 서로 다른 종류의 읽기에 최적화된 표현을
  거기서 유도하는 것이 이로울 수 있다** (3장, p.101).[^kleppmann2026]
- 이미 나온 발상의 확장이다 — **우리는 이 발상을 기록 시스템과 파생 데이터에서 이미 보았고,
  ETL은 그런 유도 과정의 한 예다. 이제 그 발상을 더 밀고 나간다. 어차피 한 데이터 표현에서 다른
  것을 유도할 것이라면, 쓰기와 읽기 각각에 최적화된 서로 다른 표현을 고를 수 있다. 오직 쓰기만을
  위해 최적화하고 효율적 질의는 전혀 신경 쓰지 않는다면 데이터를 어떻게 모델링하겠는가?** (3장,
  p.101).[^kleppmann2026] 그 축은
  [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)에 있다.

## 이벤트 로그

- 답이 나온다 — **데이터를 쓰는 아마 가장 단순하고 빠르고 표현력 있는 방법은 이벤트
  로그(event log)다. 데이터를 쓰고 싶을 때마다 그것을 타임스탬프를 포함한 자족적 문자열(아마
  JSON)로 인코딩하고 이벤트의 시퀀스에 덧붙인다. 이 로그의 이벤트는 불변이다 — 그것을 바꾸거나
  삭제하지 않고 오직 로그에 이벤트를 더 덧붙이기만 한다(더한 이벤트가 앞선 이벤트를 무효화할 수
  있다). 이벤트는 임의의 속성을 담을 수 있다** (3장, p.101).[^kleppmann2026]
- 저자들의 예 — **컨퍼런스 관리 시스템이다. 컨퍼런스는 복잡한 업무 도메인일 수 있다 — 개별
  참가자가 등록하고 카드로 결제할 수 있을 뿐 아니라, 회사가 좌석을 대량으로 주문하고 청구서로
  결제한 뒤 나중에 그 좌석을 개인에게 배정할 수도 있다. 일정 수의 좌석이 연사·후원사·자원봉사자
  등을 위해 예약될 수 있다. 예약이 취소될 수도 있고, 주최자가 행사를 다른 방으로 옮겨 수용
  인원을 바꿀 수도 있다. 이 모든 일이 벌어지는 가운데 가용 좌석 수를 단순히 계산하는 것조차
  까다로운 질의가 된다** (3장, p.101).[^kleppmann2026]
- 구조 — **컨퍼런스 상태의 모든 변화(주최자가 등록을 여는 것, 참가자가 등록하고 취소하는 것)가
  먼저 이벤트로 저장된다. 이벤트가 로그에 덧붙여질 때마다 여러 구체화 뷰(materialized views,
  프로젝션projections 또는 읽기 모델read models이라고도 한다)도 그 이벤트의 효과를 반영하도록
  갱신된다. 컨퍼런스 예에서는 각 예약 상태에 관련된 모든 정보를 모으는 구체화 뷰 하나, 주최자
  대시보드의 차트를 계산하는 것 하나, 참가자 배지를 만드는 프린터용 파일을 생성하는 것 하나가
  있을 수 있다** (3장, p.102, 그림 3-8).[^kleppmann2026]

## 두 이름의 정의

- **이벤트를 진실의 원천으로 쓰고 모든 상태 변화를 이벤트로 표현하는 발상을 이벤트
  소싱(event sourcing)이라 한다. 별도의 읽기 최적화 표현을 유지하고 그것을 쓰기 최적화 표현에서
  유도하는 원칙을 명령 질의 책임 분리(command query responsibility segregation, CQRS)라 한다**
  (3장, p.102).[^kleppmann2026]
- 계보도 밝힌다 — **이 용어들은 DDD 커뮤니티에서 나왔지만, 비슷한 발상은 오래전부터 있었다 —
  예컨대 상태 기계 복제(state machine replication)가 그렇다** (3장,
  p.102).[^kleppmann2026] 그 계보는
  [복제 상태 기계](../concepts/replicated-state-machine.md)에 있다.

## 시간의 차원을 데이터 모델에 들인다

앞의 절들은 이 패턴을 **데이터 모델의 선택지**로 규정한다. 도메인 주도 설계 쪽 소스가 같은
패턴을 **업무 도메인 모델링의 문제**에서 유도하고, 이 KB에서 그것을 **실제로 구현하는 첫
소스**다.

- 저자가 상태 기반 테이블 하나(텔레마케팅의 리드 스무 줄, 이름·전화번호·상태·생성일·갱신일)를
  먼저 보이고 거기서 무엇을 알 수 있는지 셈한 뒤 빠진 것을 짚는다 (7장,
  p.101):[^khononov2021]

> The table's data documents the leads' current states, but it misses the story of how each lead
> got to their current state.

  - 그 빠진 것이 업무의 물음이다 — 리드가 전환되기까지 통화가 몇 번이었는가, 구매가 즉시
    일어났는가 긴 여정이었는가, 여러 번 후속 통화를 한 사람에게 계속 연락할 값이 있는가
    (7장, p.101).[^khononov2021] **판매 프로세스를 최적화하려면 답해야 하는 물음들이고,
    현재 상태만 담은 스키마는 그중 어느 것도 답하지 못한다.**
- 그래서 패턴의 규정이 시간을 축으로 온다 (7장, p.101):[^khononov2021]

> The event sourcing pattern introduces the dimension of time into the data model. Instead of the
> schema reflecting the aggregates' current state, an event sourcing–based system persists events
> documenting every change in an aggregate's lifecycle.

  - **위 [두 이름의 정의](#두-이름의-정의)와 같은 것을 다른 입구로 말한다.** 그쪽은 질의
    요구를 하나의 표현으로 감당할 수 없다는 데이터 모델의 문제에서 출발하고, 이쪽은 현재
    상태만으로는 업무의 물음에 답할 수 없다는 도메인의 문제에서 출발한다. 도달점은 같다.
- 이 패턴이 새로운 발명이 아니라는 관찰도 붙는다 (7장, p.108):[^khononov2021]

> In essence, the event sourcing pattern is nothing new. The financial industry uses events to
> represent changes in a ledger. A ledger is an append-only log that documents transactions. A
> current state (e.g., account balance) can always be deduced by "projecting" the ledger's records.

  - 같은 회계 관행을 도메인 모델의 구성 요소로 들이는 쪽은
    [상태·스트림·불변성](../concepts/state-streams-and-immutability.md)의 마지막 절과
    [분석 패턴을 모델에 들이기](../concepts/analysis-patterns-in-the-model.md)에 있다.

## 이벤트 저장소

- 패턴이 성립하기 위한 조건 (7장 §"Source of Truth", p.107):[^khononov2021]

> For the event sourcing pattern to work, all changes to an object's state should be represented and
> persisted as events. These events become the system's source of truth (hence the name of the
> pattern).

- 그 이벤트를 담는 데이터베이스에 이름과 지위가 붙는다 (7장, p.107):[^khononov2021]

> The database that stores the system's events is the only strongly consistent storage: the system's
> source of truth. The accepted name for the database that is used for persisting events is
> event store.

  - **"유일하게 강한 일관성을 갖는 저장소"라는 한정이 이 KB의 다른 소스가 쓰지 않는 표현이다.**
    위 [이벤트 로그](#이벤트-로그)와 [두 이름의 정의](#두-이름의-정의)는 이벤트 로그를 정본으로
    삼는다고만 적고 파생 뷰의 일관성 등급을 규정하지 않는다. 이 판본은 **투영이 결국
    일관되는 것임을 아키텍처 조항으로 못 박고**, 그 조항이 [CQRS 아키텍처](../concepts/cqrs-architecture.md)의
    "명령이 돌려주는 데이터는 강한 일관성 모델에서 와야 한다"는 제한으로 이어진다.
    정본과 파생의 구별 자체는
    [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)에 있다.
- 이 저장소에 걸리는 제약은 하나다 (7장 §"Event Store", p.107):[^khononov2021]

> The event store should not allow modifying or deleting the events since it's append-only storage.

  - 저자가 각주로 예외를 남긴다 — **데이터 마이그레이션 같은 예외적인 경우를 빼고**다
    (7장, p.107, 각주 2).[^khononov2021] 추가 전용 저장의 일반 논의는
    [CRUD와 삽입 전용 패턴](../concepts/crud-and-insert-only-patterns.md)에 있다.
- **최소 인터페이스가 두 연산으로 규정된다** (7장, p.107):[^khononov2021]

  > To support implementation of the event sourcing pattern, at a minimum the event store has to
  > support the following functionality: fetch all events belonging to a specific business entity and
  > append the events.

  저자가 그 둘을 그대로 인터페이스로 적는다:

  ```csharp
  interface IEventStore
  {
      IEnumerable<Event> Fetch(Guid instanceId);
      void Append(Guid instanceId, Event[] newEvents, int expectedVersion);
  }
  ```

- 셋째 인수가 이 인터페이스의 핵심이다 (7장, p.107):[^khononov2021]

> The expectedVersion argument in the Append method is needed to implement optimistic concurrency
> management: when you append new events, you also specify the version of the entity on which you
> are basing your decisions. If it's stale, that is, new events were added after the expected
> version, the event store should raise a concurrency exception.

  - **읽기 전용 조회와 낙관적 추가, 이 둘이면 패턴이 선다는 것이 이 절의 값이다.** 나머지
    기능(투영을 위한 구독 등)은 CQRS를 위해 더해지는 것이라고 저자가 다음 장으로 넘긴다
    (7장, p.108).[^khononov2021] 낙관적 동시성 제어 일반은
    [동시성 제어 분류](../concepts/concurrency-control-classification.md)에 있다.

## 명령이 사실이 되는 순간

- **사용자의 요청이 들어오면 그것을 명령(command)이라 부르며 먼저 검증돼야 한다. 명령이 실행되고
  유효하다고 판정되고 나면(예컨대 요청된 예약에 충분한 좌석이 있었으면) 그것은 사실(fact)이
  되고, 대응하는 이벤트가 로그에 추가된다. 따라서 이벤트 로그는 오직 유효한 이벤트만 담아야 하며,
  구체화 뷰를 만드는 이벤트 로그의 소비자는 이벤트를 거부할 수 없다** (3장,
  pp.102–103).[^kleppmann2026]
- 명명 규약이 따라온다 — **이벤트 소싱 스타일로 데이터를 모델링할 때는 이벤트 이름을 과거
  시제로 짓는 것이 권장된다(예: "좌석이 예약되었다"). 이벤트는 무언가가 일어났다는 사실의
  기록이기 때문이다. 사용자가 나중에 예약을 바꾸거나 취소하기로 하더라도, 그들이 이전에 예약을
  갖고 있었다는 사실은 여전히 참이며, 변경이나 취소는 나중에 추가되는 별개의 이벤트다** (3장,
  p.103).[^kleppmann2026]

## 팩트 테이블과 무엇이 다른가

- 저자들이 분석계의 구조와 나란히 놓는다 — **이벤트 소싱과 스타 스키마 팩트 테이블의 공통점은
  둘 다 과거에 일어난 이벤트의 모음이라는 것이다. 그러나 팩트 테이블의 행은 전부 같은 열 집합을
  갖는 반면, 이벤트 소싱에서는 각각 다른 속성을 가진 여러 이벤트 타입이 있을 수 있다. 또한 팩트
  테이블은 순서 없는 모음인 반면, 이벤트 소싱에서는 이벤트의 순서가 중요하다 — 예약이 먼저
  이뤄지고 그다음 취소됐다면 그 이벤트를 잘못된 순서로 처리하는 것은 말이 되지 않을 것이다**
  (3장, p.103).[^kleppmann2026] 팩트 테이블 쪽은
  [팩트 테이블](../concepts/fact-table.md)에 있다.

## 이점

- **이벤트 소싱과 CQRS에는 여러 이점이 있다** (3장, pp.103–104):[^kleppmann2026]
  - **시스템을 개발하는 사람에게 이벤트는 무언가가 왜 일어났는지 그 의도를 더 잘 전달한다.**
    저자들의 대비 — **"예약이 취소되었다"는 이벤트가 "bookings 테이블 4001행의 active 열이
    false로 설정됐고, 그 예약에 연관된 세 행이 seat_assignments 테이블에서 삭제됐으며, 환불을
    나타내는 행이 payments 테이블에 삽입됐다"보다 이해하기 쉽다. 구체화 뷰가 취소 이벤트를
    처리할 때 그 행 수정들이 여전히 일어날 수 있지만, 그것들이 이벤트에 의해 구동될 때 갱신의
    이유가 훨씬 명확해진다.**
  - **이벤트 소싱의 핵심 원칙은 구체화 뷰가 이벤트 로그에서 재현 가능한 방식으로 유도된다는
    것이다. 언제나 구체화 뷰를 지우고 같은 이벤트를 같은 순서로 같은 코드로 처리해 다시 계산할
    수 있어야 한다. 뷰 유지보수 코드에 버그가 있었다면 뷰를 지우고 새 코드로 다시 계산하면
    된다. 버그를 찾기도 쉬운데, 뷰 유지보수 코드를 원하는 만큼 자주 다시 돌려 그 동작을 살펴볼
    수 있기 때문이다.**
  - **애플리케이션이 요구하는 특정 질의에 최적화된 구체화 뷰를 여럿 둘 수 있다. 이 뷰들은
    필요에 따라 이벤트와 같은 데이터베이스에 저장될 수도 다른 데이터베이스에 저장될 수도 있다.
    어떤 데이터 모델이든 쓸 수 있고, 빠른 읽기를 위해 비정규화될 수 있다. 서비스가 재시작될
    때마다 이벤트 로그에서 뷰를 다시 계산해도 괜찮다면 뷰를 메모리에만 두고 영속화하지 않을
    수도 있다.**
  - **기존 정보를 새로운 방식으로 제시하고 싶어지면 기존 이벤트 로그에서 새 구체화 뷰를 만드는
    것이 쉽다. 새로운 종류의 이벤트를 더하거나 기존 이벤트 타입에 새 속성을 더해 새 기능을
    지원하도록 시스템을 진화시킬 수도 있다(더 오래된 이벤트는 수정되지 않은 채 남는다). 기존
    이벤트에 새 동작을 이어 붙일 수도 있다(예: 컨퍼런스 참가자가 취소하면 그 좌석을 대기자
    명단의 다음 사람에게 제안할 수 있다).**
  - **이벤트가 잘못 쓰였으면 그것을 뒤집는 후속 삭제 이벤트를 쓸 수 있다. 하류 뷰가 이 삭제를
    자동으로 반영해 데이터를 교정한다. 반면 데이터를 직접 갱신·삭제하는 데이터베이스에서는
    커밋된 트랜잭션을 되돌리기가 흔히 어렵다. 따라서 이벤트 소싱은 시스템에서 되돌릴 수 없는
    행동의 수를 줄여 변경을 더 쉽게 만들 수 있다.** 되돌릴 수 없음이 왜 변경을 어렵게 만드는지는
    [유지보수성](../concepts/maintainability.md)에 있다.
  - **이벤트 로그는 시스템에서 무슨 일이 있었는지의 감사 로그(audit log) 역할도 할 수 있으며,
    이는 그런 감사 가능성을 요구하는 규제 산업에서 값지다.**
  - **이벤트 로그는 순차 접근 패턴 덕분에 데이터베이스보다 보통 더 높은 쓰기 처리량을 감당할 수
    있다. 이벤트의 일시적 폭주가 있으면 로그가 그것을 흡수할 수 있고, 구체화 뷰를 유지하는 하류
    시스템은 압도되지 않고 자기 속도로 따라잡을 수 있다.**

## 함정

- **그러나 이벤트 소싱과 CQRS에는 단점도 있다** (3장, p.104):[^kleppmann2026]
  - **외부 정보가 관여하면 조심해야 한다. 예컨대 이벤트가 한 통화의 가격을 담고 있고 어떤 뷰를
    위해 그것을 다른 통화로 변환해야 한다고 하자. 환율이 변동할 수 있으므로 이벤트를 처리할 때
    외부 원천에서 환율을 가져오는 것은 문제가 된다 — 다른 날에 구체화 뷰를 다시 계산하면 다른
    결과가 나올 것이기 때문이다. 이벤트 처리 로직을 결정적으로 만들려면 환율을 이벤트 자체에
    포함시키거나, 이벤트에 표시된 타임스탬프의 역사적 환율을 질의할 방법을 두어 같은 타임스탬프에
    대해 이 질의가 언제나 같은 결과를 반환하도록 보장해야 한다.**
  - **이벤트가 불변이어야 한다는 요구는 이벤트가 사용자의 개인 데이터를 담을 때 문제를 만든다.
    사용자가 (예컨대 GDPR 아래) 자기 데이터의 삭제를 요청할 권리를 행사할 수 있기 때문이다.
    이벤트 로그가 사용자별이면 그 사용자의 로그 전체를 지우면 되지만, 이벤트 로그가 여러 사용자에
    관한 이벤트를 담고 있으면 그렇게 되지 않는다. 개인 데이터를 실제 이벤트 바깥에 저장하거나,
    나중에 지우기로 선택할 수 있는 키로 암호화(크립토 슈레딩crypto-shredding이라 알려진 기법)해
    볼 수 있지만, 그것 역시 필요할 때 파생 상태를 다시 계산하기 어렵게 만든다.**
  - **외부에 보이는 부수 효과가 있으면 이벤트 재처리에 주의가 필요하다 — 예컨대 구체화 뷰를 다시
    만들 때마다 확인 이메일을 다시 보내고 싶지는 않을 것이다.**

## 개인 데이터 삭제 — 잊을 수 있는 페이로드

위 [함정](#함정)의 개인 데이터 항이 삭제 요구와 불변성의 충돌을 짚고 크립토 슈레딩을 해법이자
또 다른 대가로 든다. 구현 쪽 소스가 같은 해법에 이름과 구체적 배치를 준다.

- 물음이 GDPR로 온다 — 이벤트 저장소는 추가 전용인데 물리적으로 데이터를 지워야 하면 어떻게
  하는가 (7장 §"Deleting Data", p.114).[^khononov2021] 답이 이렇다 (7장,
  p.114):[^khononov2021]

> This need can be addressed with the forgettable payload pattern: all sensitive information is
> included in the events in encrypted form. The encryption key is stored in an external key–value
> store: the key storage, where the key is a specific aggregate's ID and the value is the encryption
> key. When the sensitive data has to be deleted, the encryption key is deleted from the key storage.
> As a result, the sensitive information contained in the events is no longer accessible.

  - **키의 단위가 애그리게이트 ID라는 것이 이 판본이 더하는 값이다.** 위 [함정](#함정)이
    옮긴 크립토 슈레딩 서술은 "나중에 지우기로 선택할 수 있는 키"라고만 적고 키를 무엇 단위로
    쪼갤지는 열어 둔다. 이 판본은 그 단위를 애그리게이트로 고정한다 — 애그리게이트가 이미
    일관성 경계이자 샤딩 단위이므로 키 경계도 거기 맞춘다는 것이다.
    #hypothesis 저자가 그 이유를 밝힌 대목은 없고, 근거는 같은 장이 샤딩 단위도 애그리게이트
    ID로 잡는다는 것이다.
  - **대가는 그대로 남는다.** 위 [함정](#함정)이 적은 것 — 키를 지우면 필요할 때 파생 상태를
    다시 계산할 수 없다 — 을 이 판본은 적지 않는다. 두 서술이 어긋나는 것이 아니라 한쪽이
    해법을, 다른 한쪽이 그 해법의 대가를 적는다. 그 대가의 전문은
    [상태·스트림·불변성](../concepts/state-streams-and-immutability.md)에 있고, 삭제 요구가
    파생 데이터 일반에 부딪히는 자리는
    [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)에 있다.

- **같은 해법에 셋째 소스가 붙고, 그쪽은 이름을 크립토 슈레딩으로 쓴다.**
  [bellemare2025](../sources/bellemare2025.md) 5장이 이벤트 스트림의 불변성과 잊힐 권리의 충돌을
  같은 자리에서 세운다 — **이벤트 스트림은 불변이라 한 번 쓰이고 나면 들어가서 데이터를 고칠 수
  없으므로, 최선의 방책은 민감 데이터를 먼저 암호화하는 것**이다 (5장 §"Event Design for Data
  Privacy and the Right to Be Forgotten", p.123).[^bellemare2025]
  - **키의 단위가 이 페이지의 서술과 어긋나지 않되 더 넓다** — **사용자별, 계정별, 또는 다른
    중요한 엔티티별로 고유한 키를 쓰는 것이 흔하다** (5장, p.123).[^bellemare2025] 위 잊을 수 있는
    페이로드는 그 단위를 **애그리게이트 ID**로 고정하는데, 셋째 소스는 **사용자·계정·엔티티**를
    나란히 든다. **둘이 겨루지 않는다** — 한쪽은 도메인 모델의 경계에, 다른 쪽은 삭제 요청이
    걸리는 주체에 키 경계를 맞춘다. 이 대비는 이 KB가 두 원문을 맞대어 세운 것이다.
  - **이 소스가 더하는 것이 왜 그것을 쓰는가의 근거 넷이다** — 이력 데이터가 백업과 콜드 저장소에
    있어 **선별 삭제가 아주 비싸고 오래 걸린다**는 것, **개인 식별 정보만 지워도 GDPR 제17조 요구에
    흔히 충분하고 남은 데이터는 여전히 쓸모 있다**는 것, **키를 지우면 모든 소비자 서비스에서 접근이
    동시에 멈춘다**는 것, 그리고 **암호화된 데이터가 새는 것이 훨씬 덜 해로우므로 심층 방어가 하나
    더 생긴다**는 것이다 (5장, p.124).[^bellemare2025]
  - **경계도 같은 방향으로 붙는다** — **크립토 슈레딩은 데이터를 암호학적으로 이용 불가능하게 만들
    뿐이고**, 데이터 프라이버시 요구를 만족시키는 데 *대체로* 충분하지만 **법의 올바른 편에 서
    있는지는 회사 변호사에게 확인해야 한다** (5장, p.123).[^bellemare2025] 그리고 **복호된 데이터나
    복호 키를 부주의하게 저장하는 소비자로부터는 지켜 주지 못한다** (5장,
    p.124).[^bellemare2025] 위 [함정](#함정)이 적는 대가(키를 지우면 파생 상태를 다시 계산할 수
    없다)는 이 소스도 적지 않는다. 전문은
    [이벤트 설계 - 상태와 델타](../concepts/event-design-state-versus-delta.md)에 있다.

## 무엇으로 구현하는가

- **어떤 데이터베이스 위에도 이벤트 소싱을 구현할 수 있지만, EventStoreDB·MartenDB(PostgreSQL
  기반)·Axon Framework처럼 이 패턴을 지원하도록 특별히 설계된 시스템도 있다. 아파치 카프카 같은
  메시지 브로커를 이벤트 로그 저장에 쓸 수도 있고, 스트림 프로세서가 구체화 뷰를 최신으로 유지할
  수 있다** (3장, p.105).[^kleppmann2026] 카프카를 그렇게 쓰는 쪽은
  [카프카 물리 저장](../concepts/kafka-physical-storage.md)과
  [스트림 처리 패러다임](../concepts/stream-processing-paradigm.md)에 있다.
- 유일한 필수 요건 — **중요한 요구는 단 하나, 이벤트 저장 시스템이 모든 구체화 뷰가 이벤트를
  로그에 나타난 것과 정확히 같은 순서로 처리하도록 보장해야 한다는 것이다. 분산 시스템에서 이를
  달성하는 것이 언제나 쉽지는 않다** (3장, p.105).[^kleppmann2026] 그 순서를 세우는 문제는
  [원자적 브로드캐스트](../concepts/atomic-broadcast.md)에 있다.
- 장 요약이 이 모델의 자리를 다시 정리한다 — **이벤트 소싱은 데이터를 불변 이벤트의 추가 전용
  로그로 표현하며 복잡한 업무 도메인의 활동을 모델링하는 데 유리할 수 있다. 추가 전용 로그는
  데이터를 쓰는 데 좋고, 효율적 질의를 지원하기 위해 이벤트 로그는 CQRS를 통해 읽기에 최적화된
  구체화 뷰로 번역된다** (3장, p.108).[^kleppmann2026]

## 성능이 문제가 되는 문턱과 스냅샷

위 [로그 압착이 여기서는 다르게 걸린다](#로그-압착이-여기서는-다르게-걸린다)가 스냅샷을 **읽기와
크래시 복구를 빠르게 하는 성능 최적화**로 규정한다. 구현 쪽 소스가 그 최적화를 언제 해야
하는지에 수치를 붙인다.

- 물음이 성능이다 — 이벤트에서 상태를 재구성하면 이벤트가 쌓일수록 느려질 텐데 이것이 어떻게
  돌아가는가 (7장 §Performance, p.112).[^khononov2021] 저자가 먼저 비용을 인정한다 —
  **이벤트를 상태 표현으로 투영하는 데 실제로 연산 능력이 들고, 애그리게이트의 목록에 이벤트가
  더 쌓일수록 그 필요가 자란다** (7장, p.112).[^khononov2021]
- 처방은 계측이다 (7장, p.112):[^khononov2021]

> It's important to benchmark a projection's impact on performance: the effect of working with
> hundreds or thousands of events. The results should be compared with the expected lifespan of an
> aggregate—the number of events expected to be recorded during an average lifespan.

- 그리고 실측값 둘이 나온다 (7장, p.112):[^khononov2021]

> In most systems, the performance hit will be noticeable only after 10,000+ events per aggregate.
> That said, in the vast majority of systems, an aggregate's average lifespan won't go over 100
> events.

  - **두 수치의 간격이 두 자릿수라는 것이 이 항목의 요점이다.** 문턱이 만 건인데 실제
    수명이 백 건이면 최적화는 대개 필요 없다.
- 드물게 문제가 될 때 쓰는 것이 **스냅샷(snapshot) 패턴**이고 단계가 둘이다 (7장,
  p.113):[^khononov2021]
  - **프로세스 하나가 이벤트 저장소의 새 이벤트를 계속 훑으며 대응하는 투영을 만들어 캐시에
    저장한다.**
  - 애그리게이트에 어떤 동작을 실행하려고 메모리 안의 투영이 필요해지면 — 캐시에서 현재 상태
    투영을 가져오고, 스냅샷 버전 이후에 온 이벤트를 이벤트 저장소에서 가져오고, 그 추가
    이벤트를 스냅샷 위에 메모리에서 적용한다 (7장, p.113).[^khononov2021]
- **단서가 강하다** (7장, p.113):[^khononov2021]

> It's worth reiterating that the snapshot pattern is an optimization that has to be justified. If
> the aggregates in your system won't persist 10,000+ events, implementing the snapshot pattern is
> just an accidental complexity. But before you go ahead and implement the snapshot pattern, I
> recommend that you take a step back and double-check the aggregate's boundaries.

  - **마지막 문장이 이 단서의 값이다** — 이벤트가 만 건을 넘는다는 것 자체가 성능 문제이기
    전에 **애그리게이트를 너무 크게 잡았다는 신호**로 읽힌다. 그 경계를 잡는 규칙은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
- 규모 물음에도 답이 붙는다 (7장, p.114):[^khononov2021]

> The event-sourced model is easy to scale. Since all aggregate-related operations are done in the
> context of a single aggregate, the event store can be sharded by aggregate IDs: all events
> belonging to an instance of an aggregate should reside in a single shard

  - **한 트랜잭션에 애그리게이트 하나라는 제약이 여기서 배당금을 낸다.** 연산이 애그리게이트
    하나 안에서 닫히므로 샤딩 키가 자명해진다. 그 제약은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있고,
    샤딩 일반은 [데이터 샤딩](../synthesis/data-sharding.md)이 허브다.

## 그냥 로그를 남기면 안 되는가

구현 쪽 소스가 "이벤트 소싱을 쓰지 않고 상태 기반 모델에 이력만 곁들이면 안 되는가"라는 물음에
세 가지 대안을 세우고 각각이 무엇을 못 하는지 적는다 (7장 §Why Can't I Just…?,
pp.114–115).[^khononov2021] **이 절이 이 페이지의 다른 소스들이 다루지 않는 자리다** — 그쪽은
이 모델의 이점을 적고, 이쪽은 더 싼 대안이 왜 그 이점을 주지 못하는지를 적는다.

- **텍스트 파일에 로그를 써서 감사 로그로 쓰면** (7장, p.114):[^khononov2021]

  > Writing data both to an operational database and to a logfile is an error-prone operation. In its
  > essence, it's a transaction against two storage mechanisms: the database and the file. If the
  > first one fails, the second one has to be rolled back. For example, if a database transaction
  > fails, no one cares to delete the prior log messages. Hence, such logs are not consistent, but
  > rather, eventually inconsistent.

  - 같은 두 저장소 문제를 트랜잭션 스크립트에서 다루는 자리가
    [트랜잭션 스크립트](transaction-script.md)의 데이터 손상 사례 셋이다.
- **같은 데이터베이스 트랜잭션 안에서 로그 테이블에 덧붙이면** — 인프라 관점에서는 상태와 로그
  레코드의 일관된 동기화를 실제로 준다. 그러나 (7장, p.115):[^khononov2021]

  > However, it is still error prone. What if the engineer who will be working on the codebase in the
  > future forgets to append an appropriate log record?

  그리고 둘째 이유가 더 무겁다 (7장, p.115):[^khononov2021]

  > Furthermore, when the state-based representation is used as the source of truth, the additional
  > log table's schema usually degrades into chaos quickly. There is no way to enforce that all
  > required information is written and that it is written in the correct format.

- **데이터베이스 트리거로 레코드 스냅샷을 이력 테이블에 복사하면** — 앞 방식의 단점(사람이
  잊는 것)은 넘어선다. 그러나 (7장, p.115):[^khononov2021]

  > That said, the resultant history only includes the dry facts: what fields were changed. It misses
  > the business contexts: why the fields were changed. The lack of "why" drastically limits the
  > ability to project additional models.

  - **"왜"의 부재가 새 투영을 만들 능력을 제한한다는 것이 세 대안을 관통하는 판정이다.**
    같은 판정을 낮은 추상 수준의 변경 로그에 거는 자리가 위
    [CDC와 무엇이 다른가](#cdc와-무엇이-다른가)다 — 그쪽도 이벤트 소싱의 이벤트가 상태 갱신의
    기제가 아니라 **사용자 동작의 의도**를 표현한다는 것을 차이로 든다. **두 소스가 같은 선을
    긋는다.**

## CDC와 무엇이 다른가

12장이 이 모델을 스트림의 관점에서 다시 놓고 변경 데이터 캡처와 나란히 세운다.

- 먼저 자리 — **한 접근은 데이터를 저장하기 위해 이벤트 스트림을 기록 시스템으로 쓰는 것이다.
  이것이 이벤트 소싱에서 벌어지는 일이다. 갱신과 삭제로 변이되는 데이터 모델에 데이터를 저장하는
  대신 모든 상태 변화를 불변 이벤트로 모델링하고 추가 전용 로그에 쓸 수 있다. 어떤 읽기 최적화
  구체화 뷰든 이 이벤트에서 유도된다. (오래된 이벤트를 결코 지우지 않도록 설정된) 로그 기반 메시지
  브로커는 추가 전용 저장을 쓰고 낮은 지연으로 컨슈머에게 새 이벤트를 통지할 수 있으므로 이벤트
  소싱에 적합하다** (12장, p.500).[^kleppmann2026] 그 브로커는
  [로그 기반 메시지 브로커](../concepts/log-based-message-brokers.md)에 있다.
- 비교의 축 — **CDC와 이벤트 소싱은 어떻게 비교되는가? CDC와 비슷하게 이벤트 소싱도 애플리케이션
  상태에 대한 모든 변경을 변경 이벤트의 로그로 저장하는 것을 포함한다. 가장 큰 차이는 이벤트 소싱이
  그 발상을 다른 추상 수준에서 적용한다는 것이다** (12장, p.507):[^kleppmann2026]
  - **CDC에서 애플리케이션은 데이터베이스를 가변적인 방식으로 써서 마음대로 레코드를 갱신하고
    삭제한다. 변경의 로그는 (예컨대 복제 로그를 파싱해서) 낮은 수준에서 데이터베이스로부터
    추출되는데, 이는 데이터베이스에서 추출된 쓰기의 순서가 실제로 쓰인 순서와 일치함을 보장해 경쟁
    조건을 피한다.**
  - **이벤트 소싱에서 애플리케이션 로직은 이벤트 로그에 쓰이는 불변 이벤트에 기반해 명시적으로
    지어진다. 이 경우 이벤트 저장소는 추가 전용이고 이벤트의 갱신이나 삭제는 권장되지 않거나
    금지된다. 이벤트는 낮은 수준의 상태 변화가 아니라 애플리케이션 수준에서 일어난 일을 반영하도록
    설계된다.**
- 판정 — **어느 쪽이 나은지는 상황에 달렸다. 이미 하고 있지 않은 애플리케이션에 이벤트 소싱을
  채택하는 것은 큰 변화다; 그것은 여러 장단점을 갖는다. 반면 CDC는 최소한의 변경으로 기존
  데이터베이스에 더해질 수 있다; 데이터베이스에 쓰는 애플리케이션은 CDC가 일어나고 있다는 것조차
  모를 수 있다** (12장, p.507).[^kleppmann2026] CDC 쪽 전체는
  [변경 데이터 캡처](../concepts/change-data-capture.md)에 있다.

## 로그 압착이 여기서는 다르게 걸린다

- **CDC와 마찬가지로 이벤트 로그를 재생하면 시스템의 현재 상태를 재구성할 수 있다. 그러나 로그
  압착은 다르게 다뤄져야 한다** (12장, p.508):[^kleppmann2026]
  - **레코드 갱신에 대한 CDC 이벤트는 통상 레코드의 새 버전 전체를 담으므로, 기본 키에 대한 현재
    값은 그 기본 키에 대한 가장 최근 이벤트로 전적으로 결정되고 로그 압착은 같은 키에 대한 이전
    이벤트를 버릴 수 있다.**
  - **반면 이벤트 소싱에서 이벤트는 더 높은 수준에서 모델링된다. 이벤트는 통상 그 동작의 결과로
    일어난 상태 갱신의 기제가 아니라 사용자 동작의 의도를 표현한다. 이 경우 나중 이벤트가 통상 이전
    이벤트를 무효화하지 않으므로 최종 상태를 재구성하려면 이벤트의 전체 이력이 필요하다. 로그 압착은
    같은 방식으로 가능하지 않다.**
- 그래서 스냅샷이 따로 필요하다 — **이벤트 소싱을 쓰는 애플리케이션은 통상 이벤트의 로그에서 유도된
  현재 상태의 스냅샷을 저장하는 기제를 갖고 있어서 전체 로그를 반복해 재처리하지 않아도 된다. 그러나
  이는 읽기와 크래시 복구를 빠르게 하는 성능 최적화일 뿐이다; 의도는 시스템이 모든 원시 이벤트를 영원히
  저장하고 필요할 때마다 전체 이벤트 로그를 재처리할 수 있어야 한다는 것이다** (12장,
  p.508).[^kleppmann2026] 그 가정이 어디까지 실현 가능한지는
  [상태·스트림·불변성](../concepts/state-streams-and-immutability.md)의 마지막 절에 있다.
- 위 [함정](#함정)의 개인 데이터 항이 그 절과 이어진다 — 3장이 크립토 슈레딩을 이벤트 소싱의 단점으로
  꼽았다면, 12장은 같은 기법을 불변성 일반의 한계로 다시 놓고 그 자체의 대가(키 저장소가 가변이 되는
  것, 키 단위를 미리 정해야 하는 것)까지 적는다.
- CQRS의 비동기성이 낳는 문제와 그 반대급부(다중 객체 트랜잭션 필요가 줄어드는 것)도 그 페이지의
  동시성 제어 절이 담당한다.

## 13장이 이 모델을 감사 가능성의 근거로 삼는다

위 [이점](#이점)의 감사 로그 항목을 13장이 훨씬 강하게 다시 쓴다.

- 트랜잭션 쪽이 불리한 이유 — **트랜잭션이 데이터베이스의 여러 객체를 변이시키면 사후에 그 근본 이유를
  알기 어려울 수 있다. 트랜잭션 로그를 잡아 두더라도 여러 테이블의 삽입·갱신·삭제가 왜 그 변이들이
  수행됐는지에 대한 분명한 그림을 반드시 주지는 않는다. 그 변이를 결정한 애플리케이션 로직의 호출은
  일시적이고 재현될 수 없다** (13장, p.577).[^kleppmann2026]
- 이 모델이 유리한 이유 — **대조적으로 이벤트 기반 시스템은 더 나은 감사 가능성을 제공할 수 있다.
  이벤트 소싱 접근에서 시스템에 대한 사용자 입력은 단일 불변 이벤트로 표현되고 그 결과로 일어나는
  어떤 상태 갱신이든 그 이벤트에서 유도된다. 그 유도는 결정적이고 반복 가능하게 만들 수 있어서 같은
  이벤트 로그를 같은 버전의 유도 코드로 돌리면 같은 상태 갱신이 나온다** (13장,
  p.577).[^kleppmann2026] 위 [이점](#이점)의 "재현 가능한 방식으로 유도된다"는 원칙이 여기서
  무결성 검사의 도구가 된다.
- 무엇이 가능해지는가 — **이벤트 로그에 대해서는 해시를 써서 이벤트 저장이 손상되지 않았는지 검사할
  수 있다. 어떤 파생 상태에 대해서든 그것을 이벤트 로그에서 유도한 배치·스트림 프로세서를 다시 돌려
  같은 결과가 나오는지 검사하거나, 심지어 중복된 유도를 병렬로 돌릴 수 있다** (13장,
  p.577).[^kleppmann2026] 전문은
  [감사와 무결성 검사](../concepts/auditing-and-integrity-checking.md)에 있다.
- 그리고 이 모델은 정확성 구성의 한 부품으로도 지목된다 — **쓰기 연산의 내용을 원자적으로 쓰기 쉬운
  단일 메시지로 표현하는 것 — 이벤트 소싱과 매우 잘 맞는 접근** 이 무결성을 얻는 네 기제 중 첫째로
  꼽힌다 (13장, p.572).[^kleppmann2026] 그 목록은
  [타임리니스와 무결성](../concepts/timeliness-and-integrity.md)에 있다.

## 이벤트 기반 아키텍처

같은 불변 이벤트가 데이터 모델이 아니라 **서비스 사이의 통신 수단**으로 쓰일 때 붙는 이름이
따로 있다. 데이터 엔지니어링 쪽 소스가 그것을 아키텍처 유형으로 정리한다.

- 이벤트의 정의부터 — **업무는 좀처럼 정적이지 않다. 새 고객을 얻거나, 고객에게서 새 주문을
  받거나, 제품·서비스 주문이 들어오는 것처럼 업무에서는 일이 자주 일어난다. 이것들은 전부
  일어난 무언가, 전형적으로 무언가의 상태(state) 변화로 폭넓게 정의되는 이벤트(event)의 예다.
  예컨대 새 주문이 고객에 의해 생성되거나, 고객이 나중에 이 주문에 갱신을 가할 수 있다** (3장,
  p.95).[^reis2022]
- **이벤트 기반 워크플로(event-driven workflow)는 데이터 엔지니어링 수명 주기의 여러 부분에
  걸쳐 이벤트를 생성·갱신하고 비동기적으로 옮기는 능력을 아우른다. 이 워크플로는 세 주요 영역으로
  귀결된다: 이벤트 생산(production)·라우팅(routing)·소비(consumption). 이벤트는 생산자·이벤트
  라우터·소비자 사이에 단단히 결합된 의존 없이 그것을 소비하는 무언가로 생산되고 라우팅돼야
  한다** (3장, p.95).[^reis2022]
- **이벤트 기반 아키텍처(event-driven architecture)는 이벤트 기반 워크플로를 받아들이고 이를 여러
  서비스에 걸친 소통에 쓴다. 이벤트 기반 아키텍처의 이점은 여러 서비스에 이벤트의 상태를 분산한다는
  것이다. 이는 서비스가 오프라인이 되거나, 분산 시스템에서 노드가 실패하거나, 여러 소비자·서비스가
  같은 이벤트에 접근하기를 원할 때 도움이 된다. 느슨하게 결합된 서비스가 있을 때는 언제나 이벤트
  기반 아키텍처의 후보다** (3장, p.95).[^reis2022] 그 라우터가 실제로 무엇인지는
  [발행/구독 메시징](../concepts/publish-subscribe-messaging.md)에 있다.
  - 층위를 가려 둔다 — 이 페이지의 이벤트 소싱은 **한 시스템 안에서 상태를 어떻게 표현하는가**의
    답이고, 이벤트 기반 아키텍처는 **여러 서비스가 어떻게 소통하는가**의 답이다. 같은 불변 이벤트를
    쓰지만 답하는 질문이 다르다.

## 애플리케이션 안에서 읽기 경로를 고르는 네 선택지

위 절들은 이 모델을 **저장소 수준의 데이터 모델**로 다룬다. 파이썬 아키텍처 쪽 소스는 같은
이름을 **한 애플리케이션 안의 읽기 경로 선택**으로 좁혀 쓰고, 그 선택지를 네 개로 늘어놓는다.

- 전제가 온건하다 — **이 장에서 우리는 꽤 논란의 여지 없는 통찰로 시작할 것이다: 읽기(질의)와
  쓰기(명령)는 다르므로 다르게 다뤄져야 한다(원한다면 그 책임이 분리되어야 한다). 그다음
  우리는 그 통찰을 갈 수 있는 데까지 밀어붙일 것이다** (12장 도입).[^percival2020]
- 근거는 도메인 모델의 목적이다 — **도메인 모델은 쓰기를 위한 것이다**
  (12장 §"Domain Models Are for Writing").[^percival2020] 위
  [왜 쓰기와 읽기를 가르는가](#왜-쓰기와-읽기를-가르는가)가 **데이터 표현의 최적화**를
  이유로 든다면, 이쪽은 **불변식을 강제하는 코드가 읽기에는 필요 없다**를 이유로 든다.
- **선택지 넷이 표로 제시된다** (12장 표 12-2):[^percival2020]

  | 선택지 | 이득 | 비용 |
  |---|---|---|
  | 그냥 리포지터리를 쓴다 | 단순하고 일관된 접근 | 복잡한 질의 패턴에서 성능 문제를 예상하라 |
  | ORM으로 맞춤 질의를 쓴다 | DB 설정과 모델 정의를 재사용할 수 있다 | 자기만의 별난 점과 문법을 가진 질의 언어가 하나 더 는다 |
  | 손으로 쓴 SQL을 쓴다 | 표준 질의 문법으로 성능을 세밀히 통제할 수 있다 | DB 스키마 변경을 손으로 쓴 질의와 ORM 정의 양쪽에 해야 한다. 고도로 정규화된 스키마는 여전히 성능 한계를 가질 수 있다 |
  | 이벤트로 별도 읽기 저장소를 만든다 | 읽기 전용 사본은 확장하기 쉽다. 데이터가 바뀔 때 뷰를 구성해 두면 질의가 가능한 한 단순해진다 | 복잡한 기법 |

  - **위 절들이 다루는 것은 이 표의 넷째 줄뿐이다.** 앞의 셋은 이벤트 로그도 구체화 뷰도
    없이 같은 저장소를 읽는 방법이고, 그래도 "읽기와 쓰기를 다르게 다룬다"는 통찰은
    성립한다. 이 계단이 이 소스의 기여다 — **CQRS가 전부 아니면 전무가 아니라는 것.**
- 판정도 온건하다 — **흔히 당신의 읽기 연산은 쓰기 모델과 같은 개념적 객체에 작용할
  것이므로, ORM을 쓰고 리포지터리에 읽기 메서드를 좀 더하고 읽기 연산에 도메인 모델
  클래스를 쓰는 것으로 그냥 괜찮다** (12장 §"Wrap-Up").[^percival2020]
- 그리고 언제 넷째가 필요한지가 규정된다 — **그러나 당신 도메인 모델이 더 풍부해지고
  복잡해질수록 단순화된 읽기 모델이 점점 더 매력적이 된다** (12장 §"Wrap-Up").[^percival2020]
  예제에서 그것이 갈리는 지점이 개념 단위의 불일치다 — **우리 책 예제에서 읽기 연산은
  도메인 모델과 꽤 다른 개념적 엔티티에 작용한다. 할당 서비스는 SKU 하나에 대한 배치의
  관점에서 생각하지만, 사용자는 여러 SKU를 가진 주문 전체에 대한 할당에 신경 쓴다**
  (12장 §"Wrap-Up").[^percival2020]
- 실제 사례도 밝혀져 있다 — **MADE.com의 할당 서비스는 실제로 Redis에 저장된 읽기 모델과
  Varnish가 제공하는 두 번째 캐시 층까지 갖춘 "본격" CQRS를 쓴다. 그러나 그 사용 사례는
  여기서 보인 것과 꽤 다르다** (12장 §"Wrap-Up").[^percival2020]
- **뷰 로직이 단순하다는 가정에 단서가 붙는다** — **뷰 모델은 복잡한 로직을 가질 수 있다.
  이 책에서 우리는 읽기 모델과 쓰기 모델을 분리하라고 권했는데, 그것들이 다른 일관성과
  처리량 요구를 갖기 때문이다. 대부분 우리는 읽기에 더 단순한 로직을 쓸 수 있지만 그것이
  언제나 참은 아니다. 특히 권한과 인가 모델이 읽기 쪽에 많은 복잡성을 더할 수 있다**
  (Epilogue §"Questions Our Tech Reviewers Asked…").[^percival2020] 그 경우의 처방이
  뷰 빌더와 뷰 페처를 가르는 것이다 — **이것이 뷰 빌더에 목킹된 데이터(예컨대 딕셔너리
  리스트)를 주어 테스트하기 쉽게 만든다.**
- 층위를 가려 둔다 — 위 [이벤트 기반 아키텍처](#이벤트-기반-아키텍처) 절이 세 층위 중 둘을
  갈랐다면(한 시스템의 상태 표현 대 여러 서비스의 소통), 이 절은 셋째다: **한 애플리케이션
  안에서 읽기 경로를 어디로 낼 것인가.** 세 층위가 같은 이름을 쓴다.

## CQRS를 이벤트 소싱 없이 쓸 수 있다는 주장

- 이 페이지는 두 이름을 한 제목에 묶고 있고, 위 [두 이름의 정의](#두-이름의-정의)가 옮긴 정의도
  둘을 나란히 세운다. 구현 쪽 소스는 그 결합을 명시적으로 끊는다 (8장,
  p.129):[^khononov2021]

> That said, this chapter "decouples" CQRS from event sourcing. I intend to show that CQRS is useful
> even if the business logic is implemented using any of the other business logic implementation
> patterns.

- 계보는 인정한다 — **원래 CQRS는 이벤트 소싱 모델의 제한된 질의 가능성을 해결하기 위해
  정의되었다. 한 번에 한 애그리게이트 인스턴스의 이벤트만 질의할 수 있기 때문이다** (8장,
  p.129).[^khononov2021] 그러나 역방향의 필요만 남긴다 — 맺음에서 **이 패턴이 이벤트 소싱
  도메인 모델 기반 시스템에는 의무이지만 여러 영속 모델로 일할 방법이 필요한 어떤 시스템에도
  쓰일 수 있다**고 적는다 (8장, p.135).[^khononov2021]
- **이 KB는 두 이름을 한 페이지에 둔 채로 둔다.** 이 페이지가 기대는 다른 소스들이 두 이름을
  한 쌍으로 규정하고, 그중 어느 쪽도 "CQRS는 이벤트 소싱 없이 쓸 수 없다"고 적지는 않기
  때문이다. 대상이 어긋나는 것이 아니라 **이 판본이 더 넓은 적용 범위를 주장하는 것**이라
  모순 쌍으로 세우지 않았다.
  - 그 넓은 범위의 전문 — 폴리글랏 모델링이라는 동기, 명령 실행 모델과 읽기 모델의 규정,
    체크포인트와 캐치업 구독으로 도는 동기 투영과 메시지 버스를 타는 비동기 투영 — 은
    [CQRS 아키텍처](../concepts/cqrs-architecture.md)에 있다.
  - 그리고 이벤트 소싱을 **애그리게이트의 생애에 적용한** 업무 로직 구현 패턴은
    [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md)에 있다.

## 15장이 이 패턴과 이벤트 주도 아키텍처를 가른다

**같은 낱말을 쓰는 두 패턴이 자주 뒤섞이므로 저자가 15장에서 선을 긋는다.** 위
[이벤트 기반 아키텍처](#이벤트-기반-아키텍처) 절이 이 데이터 모델 위에 서는 구조를 다뤘다면,
이 절은 **그 구조와 이 패턴이 같은 것이 아니라는 판정**만 받는다.

- 규정이 한 줄이다 (15장, p.233):[^khononov2021]

> EDA refers to the communication between services, while event sourcing happens inside a service.

- **그래서 두 패턴의 이벤트가 다른 목적으로 설계된다** (15장, p.233):[^khononov2021]
  - 이 패턴용으로 설계된 이벤트는 그 서비스 안에 구현된 **상태 전이**를 표현한다.
  - 그 이벤트들의 목적은 **업무 도메인의 세부를 붙잡는 것**이지 다른 구성 요소와 통합하는 것이
    아니다.
  - 그래서 경계 밖으로 나가는 세 종류의 이벤트 중 **통합에 더 맞는 것과 덜 맞는 것이 갈린다.**
- **이 구분이 이 페이지의 함정 하나에 이름을 준다.** 위 [함정](#함정) 절이 적는 스키마 진화
  문제는 서비스 안에서도 아프지만, 이 모델의 이벤트를 그대로 경계 밖으로 내보내면 그것이
  **구독자를 생산자의 구현 세부에 묶는 구현 결합**이 된다 — 도메인 이벤트를 하나 더하거나
  기존 이벤트의 스키마를 바꾸는 것이 남의 경계 컨텍스트를 깨뜨린다 (15장
  §"Implementation Coupling", p.243).[^khononov2021]
- 그 결합의 해부와 되돌리는 절차는
  [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md)에 있다.

## 같은 기제를 서비스 사이 상태 공유로 세우는 셋째 소스

**이벤트를 순서대로 적용해 상태를 만든다는 같은 기제를 이 KB가 세 번째로 적는 자리다.**
[bellemare2025](../sources/bellemare2025.md) 2장은 그것을 **한 애플리케이션의 저장 모델**이 아니라
**서비스 사이에 상태를 공유하는 수단**으로 세운다.

- **그쪽의 규정** — **구체화(materialization)는 스트림을 테이블로 투영하는 것**이고, 엔티티 이벤트
  스트림의 이벤트를 **순서대로** 적용해 테이블을 구체화한다. **각 엔티티 이벤트가 테이블에
  업서트되어 주어진 키에 대해 가장 최근에 읽은 이벤트가 표현되게 한다** (2장 §"Materializing State
  from Entity Events", p.36).[^bellemare2025]
- **위 [이벤트 로그](#이벤트-로그)·[이벤트 저장소](#이벤트-저장소)와 같은 기제인데 쓰임이 다르다.**
  이 페이지의 두 소스는 그것을 **한 애플리케이션의 쓰기 모델과 읽기 모델을 가르는 장치**로 쓰고,
  셋째 소스는 **생산자 서비스의 상태를 소비자 서비스의 경계 컨텍스트 안으로 옮기는 장치**로 쓴다.
  **이 대비는 이 KB가 세 소스를 맞대어 세운 것이고 어느 원문에도 없다.**
  - 그 쓰임이 걸리는 이름이 **스트림-테이블 이중성**이고, 저자는 그것을 **생산자와 소비자 사이에
    직접 결합 없이 상태를 공유하는 일의 기반**이라고 규정한다 (2장, p.37).[^bellemare2025] 규정의
    원문과 양방향 변환은 [스트림-테이블 이중성](stream-table-duality.md)에 있다.
- **데이터베이스의 로그를 같은 것으로 읽는 대목도 그쪽에 있다** — 관계형 데이터베이스 테이블은
  삽입·갱신·삭제 명령의 열로 만들어지고 채워지며, **그 명령들을 불변 로그로 낼 수 있다**
  — **MySQL의 바이너리 로그** 같은 로컬 추가 전용 파일이든 외부 이벤트 스트림이든. **그 로그의
  전체 내용을 되감아 재생하면 테이블과 그 모든 데이터 내용을 재구성할 수 있다** (2장,
  p.37).[^bellemare2025] 위 [CDC와 무엇이 다른가](#cdc와-무엇이-다른가)가 가르는 그 선의 한쪽이다.
- **성능 문턱에 대한 처방도 같은 방향이다.** 위 [성능이 문제가 되는 문턱과 스냅샷](#성능이-문제가-되는-문턱과-스냅샷)이
  적는 스냅샷이 그쪽에서는 **하이드레이션 시간(hydration time)** 이라는 이름으로 나타난다 — 아주
  큰 데이터셋을 스트림에서 구체화하는 데 **여러 시간이나 며칠**이 걸릴 수 있고, 완화책이 **구체화된
  상태의 스냅샷이나 백업**이다 (2장 §"The Kappa Architecture", p.40).[^bellemare2025] 그 배치는
  [람다 아키텍처와 카파 아키텍처](lambda-and-kappa-architecture.md)에 있다.
- **삭제 처방은 갈리지 않되 층이 다르다.** 위 [개인 데이터 삭제 — 잊을 수 있는 페이로드](#개인-데이터-삭제--잊을-수-있는-페이로드)가
  암호화 키 폐기 같은 장치를 적는다면, 그쪽은 **툼스톤과 압착**이라는 브로커 층의 장치를 적는다.
  전문은 [카프카 로그 압착](kafka-log-compaction.md)에 있다.

## 이어지는 페이지

- [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md) — 이 모델을 애그리게이트의
  생애에 적용한 업무 로직 구현 패턴
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — 투영을 실제 데이터베이스로 물질화하는
  아키텍처 패턴
- [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md) — 이
  선택지가 나온 2부의 요지
- [리포지터리 패턴](repository-pattern.md) — 첫째 선택지가 쓰는 층
- [감사와 무결성 검사](../concepts/auditing-and-integrity-checking.md) — 이 모델이 감사에서
  유리한 이유의 전문
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 같은 발상을 낮은 추상 수준에서 하는 쪽
- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 이 모델이 기대는 원리와
  그 한계
- [로그 기반 메시지 브로커](../concepts/log-based-message-brokers.md) — 이벤트 로그를 담기에
  적합한 브로커
- [증분 뷰 유지](../concepts/incremental-view-maintenance.md) — 구체화 뷰를 효율적으로 갱신하는
  기법
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 무엇이
  정본이고 무엇이 다시 만들 수 있는 사본인가
- [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md) — 구체화 뷰의
  가장 구체적인 실물
- [복제 상태 기계](../concepts/replicated-state-machine.md) — 같은 발상의 오래된 이름
- [원자적 브로드캐스트](../concepts/atomic-broadcast.md) — "모든 뷰가 같은 순서로 처리한다"를
  분산에서 보장하는 문제
- [스트림 처리 패러다임](../concepts/stream-processing-paradigm.md) — 구체화 뷰를 최신으로
  유지하는 처리 계열
- [팩트 테이블](../concepts/fact-table.md) — 닮았지만 순서가 없는 분석계의 이벤트 모음
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 뷰를 어디까지 물질화할지의 선택이
  분석 도구 설정으로 나타난 모습
- [유지보수성](../concepts/maintainability.md) — 되돌릴 수 없음을 줄이는 것이 왜 이득인가
- [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md) — 이 모델의 이벤트를 경계 밖으로
  내보낼 때 무엇이 갈리는가
- [이벤트 설계 - 상태와 델타](../concepts/event-design-state-versus-delta.md) — 잊힐 권리에
  셋째 소스가 답하는 자리이자 델타를 경계 안에 가두라는 처방

[^reis2022]: Reis & Housley 2022, 3장 "Designing Good Data Architecture"

[^kleppmann2026]: Kleppmann & Riccomini 2026, 3장 "Data Models and Query Languages" · 12장 "Stream Processing" · 13장 "A Philosophy of Streaming Systems"


[^percival2020]: Percival & Gregory 2020, 12장 "Command-Query Responsibility Segregation
    (CQRS)" · Epilogue §"Questions Our Tech Reviewers Asked That We Couldn't Work into
    Prose". **이 소스의 locator는 장 단위다** — 검증 절차와 근거는
    `it/archive/percival2020/_progress.yaml` 머리말이 정본이다. 표 12-2는 원문이 이미 표다 —
    넷째 줄 비용 칸의 농담 한 줄("Harry는 당신의 취향과 동기를 영원히 의심할 것이다")은
    옮기지 않았다. **이 장은 얇게 반입했다** — 이 KB의 소비 맥락에서 분산 패턴은 참조
    수준이다.

[^khononov2021]: Khononov 2021, 7장 "Modeling the Dimension of Time"(§"Event Sourcing" 도입과
    상태 기반 표 pp.99–101 · §"Source of Truth" p.107 · §"Event Store" pp.107–108 ·
    §"Frequently Asked Questions" 중 §Performance pp.112–113·규모 물음 p.114·
    §"Deleting Data" p.114·§"Why Can't I Just…?" pp.114–115) · 8장 "Architectural Patterns"
    §"Polyglot Modeling" p.129·§Conclusion p.135. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다.
    이벤트 저장소 인용에서 본문 각주 번호 표지 하나("the events2")를 뺐다. 코드 펜스는
    `IEventStore` 인터페이스 하나만 두었고 원문 그대로다(언어 표지는 이 KB가 붙였다). 이 장의
    나머지 코드 목록과 도판(Figure 7-1 이벤트 소싱 애그리게이트 · 7-2 스냅샷 · 7-3 이벤트
    저장소 샤딩)은 이 페이지에 옮기지 않았다 — 애그리게이트 쪽 코드는
    [이벤트 소싱 도메인 모델](../concepts/event-sourced-domain-model.md)이 대표 하나를 갖는다.
    저자가 대는 출처 둘(Fred Brooks의 *The Mythical Man-Month* 제사와 GDPR 위키백과 항목)은
    이 KB가 확인한 원전이 아니다. Table 7-1의 리드 스무 줄은 예시 데이터라 값을 옮기지 않고
    본문이 그것에서 읽어 내는 것만 산문으로 옮겼다.
    **15장 "Event-Driven Architecture"(§"Event-Driven Architecture" p.233 ·
    §"Implementation Coupling" p.243)도 이 페이지에 합류했다** — 세 이벤트 종류와 결합의
    해부와 설계 휴리스틱 전체는
    [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md)에 두었고 이 페이지는 두 패턴이
    갈리는 판정만 받았다.

[^bellemare2025]: Bellemare 2025(2판), 2장 "Fundamentals of Events and Event Streams" —
    §"Materializing State from Entity Events"(pp.36–37) · §"The Kappa Architecture"(p.40) —
    과 **5장 "Designing Events" §"Event Design for Data Privacy and the Right to Be
    Forgotten"(pp.123–124)에서 온 위 잊을 수 있는 페이로드 절의 마지막 항**.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 24, 실측). 이 절들에 직인용을 두지 않았다 — 옮긴 것이 규정이고
    한국어 재서술로 담았다. 5장의 전문은
    [이벤트 설계 - 상태와 델타](../concepts/event-design-state-versus-delta.md)에 있고 이
    페이지는 삭제 요구에 걸리는 것만 받았다. 두 소스의 키 단위 대비는 이 KB가 세운 것이다. 코드 목록은 이 페이지에 옮기지 않았다(Example 2-1은
    [람다 아키텍처와 카파 아키텍처](lambda-and-kappa-architecture.md)에 있다). 도판 둘(그림
    2-15·2-16)은 이미지 조판이라 재현하지 않았다.

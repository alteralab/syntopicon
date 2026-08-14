---
type: concept
title: 격리 수준과 이상 현상
description: 어느 격리 수준이 어느 경쟁 조건을 막는지 한 표로 보는 자리 — 더티 읽기·읽기 스큐·팬텀 읽기·갱신 손실·쓰기 스큐 여섯의 정의, 약한 격리가 실제로 낸 금전 피해, 그리고 공격자가 동시성 버그를 노릴 수 있다는 점
generated: { by: "claude-opus-5", at: "2026-08-14T00:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 격리 수준과 이상 현상

- [동시성 문제는 언제 생기는가](#동시성-문제는-언제-생기는가)
- [약한 격리가 실제로 낸 피해](#약한-격리가-실제로-낸-피해)
- [격리 수준별로 막히는 것](#격리-수준별로-막히는-것)
- [여섯 가지 이상 현상](#여섯-가지-이상-현상)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **격리 수준(isolation level)마다 어떤 경쟁 조건(race condition)이 막히고 어떤
것이 남는가.**

## 동시성 문제는 언제 생기는가

- **두 트랜잭션이 같은 데이터에 접근하지 않거나 둘 다 읽기 전용이면 서로 의존하지 않으므로
  안전하게 병렬로 돌 수 있다. 동시성 문제(경쟁 조건)는 한 트랜잭션이 다른 트랜잭션이 동시에
  수정 중인 데이터를 읽을 때, 또는 두 트랜잭션이 같은 데이터를 수정하려 할 때에만 등장한다**
  (8장, pp.288–289).[^kleppmann2026]
- **동시성 버그는 테스트로 찾기 어렵다 — 타이밍이 운 나쁠 때에만 촉발되므로 그런 타이밍 문제는
  아주 드물게 일어나고 대개 재현하기 어렵다.** 추론하기도 어렵다 — **큰 애플리케이션에서는
  어떤 다른 코드가 데이터베이스에 접근하는지 반드시 알지는 못한다.** **한 번에 사용자
  한 명만 있어도 애플리케이션 개발은 충분히 어려운데, 동시 사용자가 많으면 어떤 데이터 조각이든
  언제든 예기치 않게 바뀔 수 있으므로 훨씬 더 어려워진다** (8장, p.289).[^kleppmann2026]
- 그래서 **데이터베이스는 오랫동안 트랜잭션 격리(transaction isolation)를 제공해 동시성
  문제를 애플리케이션 개발자에게서 숨기려 해 왔다. 이론상 격리는 동시성이 일어나지 않는 척할
  수 있게 해 삶을 편하게 만들어야 한다 — 직렬성(serializable) 격리는 트랜잭션들이 직렬로,
  즉 동시성 없이 한 번에 하나씩 실행된 것과 같은 효과를 갖도록 데이터베이스가 보장한다는
  뜻**이다 (8장, p.289).[^kleppmann2026]
- **실무에서는 안타깝게도 그렇게 단순하지 않다. 직렬성 격리에는 성능 비용이 있고 많은
  데이터베이스가 그 값을 치르려 하지 않는다. 그래서 시스템들은 흔히 더 약한 격리 수준을
  쓰는데, 이는 일부 동시성 문제만 막고 전부를 막지는 않는다. 그 수준들은 이해하기가 훨씬
  어렵고 미묘한 버그로 이어질 수 있지만 그럼에도 실무에서 쓰인다** (8장,
  p.289).[^kleppmann2026]

## 약한 격리가 실제로 낸 피해

- **약한 트랜잭션 격리와 경쟁 조건이 일으킨 동시성 버그는 이론상의 문제만이 아니다. 상당한
  금전 손실을 일으켰는데, 비트코인 거래소 하나를 파산시켰고, 금융 감사인의 조사를 불렀으며,
  고객 데이터가 손상되게 만들었다** (8장, p.289).[^kleppmann2026]
- 이런 사건에 흔히 붙는 논평 — **"금융 데이터를 다룬다면 ACID 데이터베이스를 써라!"** — 에
  대한 저자들의 반박은 **그 말이 요점을 놓친다**는 것이다. **보통 ACID로 여겨지는 인기 관계형
  데이터베이스 시스템 다수도 약한 격리를 쓰므로, 그것들을 썼다고 해서 이 버그들이 반드시
  예방됐을 것은 아니다** (8장, p.289).[^kleppmann2026]
- 덧붙는 관찰 — **은행 시스템의 상당 부분은 보안 FTP로 교환되는 텍스트 파일에 의존한다. 그
  맥락에서는 감사 추적(audit trail)과 사람 수준의 사기 방지 조치를 갖추는 것이 사실 ACID
  속성보다 더 중요하다** (8장, p.289).[^kleppmann2026]
- 그리고 확률만으로 안심할 수 없는 이유 — **동시성 문제가 정상 동작에서 드물더라도, 공격자가
  동시성 버그를 악용하려고 고도로 동시적인 요청을 의도적으로 폭주시킬 가능성을 고려해야
  한다. 그러므로 신뢰할 수 있고 안전한 애플리케이션을 만들려면 그런 버그가 체계적으로
  방지되도록 해야 한다** (8장, p.289).[^kleppmann2026]

## 격리 수준별로 막히는 것

- 표 8-1이 **여러 격리 수준에서 일어날 수 있는 이상 현상**을 정리한다. 아래는 그 표를 옮긴
  것이다 (8장, p.335):[^kleppmann2026]

| 격리 수준 | dirty reads | read skew | phantom reads | lost updates | write skew |
|---|---|---|---|---|---|
| read uncommitted | 가능 | 가능 | 가능 | 가능 | 가능 |
| read committed | 막힘 | 가능 | 가능 | 가능 | 가능 |
| snapshot isolation | 막힘 | 막힘 | 막힘 | 구현에 따라 다름 | 가능 |
| serializable | 막힘 | 막힘 | 막힘 | 막힘 | 막힘 |

- **약한 격리 수준은 이 문제들 중 일부는 막아 주지만 나머지는 애플리케이션 개발자가 손으로
  (예: 명시적 잠금으로) 처리하도록 남긴다. 직렬성 격리만이 이 모든 문제로부터 보호한다**
  (8장, p.336).[^kleppmann2026]

## 여섯 가지 이상 현상

- 각 이상 현상의 정의는 원문 직인용 (8장, pp.335–336):[^kleppmann2026]

> *Dirty reads*
>
> One client reads another client's writes before they have been committed. The read-committed
> isolation level and stronger levels prevent dirty reads.
>
> *Dirty writes*
>
> One client overwrites data that another client has written but not yet committed. Almost all
> transaction implementations prevent dirty writes (hence, it's not included in the table).
>
> *Read skew*
>
> A client sees different parts of the database at different points in time. Some cases of read
> skew are also known as *nonrepeatable reads*. This issue is most commonly prevented with
> snapshot isolation, which allows a transaction to read from a consistent snapshot
> corresponding to one particular point in time. Snapshot isolation is usually implemented with
> multiversion concurrency control.
>
> *Phantom reads*
>
> A transaction reads objects that match a search condition. Another client makes a write that
> affects the results of that search. Snapshot isolation prevents straightforward phantom reads,
> but phantoms in the context of write skew require special treatment, such as index-range locks.
>
> *Lost updates*
>
> Two clients concurrently perform a read-modify-write cycle. One overwrites the other's write
> without incorporating its changes, so data is lost. Some implementations of snapshot isolation
> prevent this anomaly automatically, while others require a manual lock (`SELECT FOR UPDATE`).
>
> *Write skew*
>
> A transaction reads something, makes a decision based on the value it saw, and writes the
> decision to the database. However, by the time the write is made, the premise of the decision
> is no longer true. Only serializable isolation prevents this anomaly.

- 직렬성 격리를 구현하는 접근법은 셋이며 이 장이 그 셋을 차례로 다룬다 — **직렬 순서로 문자
  그대로 트랜잭션을 실행하기, 2단계 잠금(two-phase locking), 그리고 직렬성 스냅샷 격리
  (serializable snapshot isolation) 같은 낙관적 동시성 제어(optimistic concurrency control)
  기법** (8장, p.309).[^kleppmann2026]

## 이어지는 페이지

- [read committed 격리](../concepts/read-committed-isolation.md) — 더티 읽기와 더티 쓰기를
  막는 가장 기본적인 수준
- [스냅샷 격리와 MVCC](../concepts/snapshot-isolation-and-mvcc.md) — 읽기 스큐를 막는 수준과
  그 구현, 그리고 "repeatable read"라는 이름의 혼란
- [갱신 손실 막기](../concepts/preventing-lost-updates.md) — 표에서 "구현에 따라 다름"이
  나오는 칸
- [쓰기 스큐와 팬텀](../concepts/write-skew-and-phantoms.md) — 직렬성만이 막는 이상
- [직렬 실행](../concepts/serial-execution.md) — 직렬성을 얻는 첫 번째 방법
- [2단계 잠금](../concepts/two-phase-locking.md) — 두 번째 방법
- [직렬성 스냅샷 격리](../concepts/serializable-snapshot-isolation.md) — 세 번째 방법
- [트랜잭션과 ACID](../concepts/acid-transactions.md) — 격리가 ACID의 어느 자리인가

[^kleppmann2026]: Kleppmann & Riccomini 2026, 8장 "Transactions"

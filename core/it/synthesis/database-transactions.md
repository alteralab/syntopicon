---
type: synthesis
title: 데이터베이스 트랜잭션
description: 읽기와 쓰기 여럿을 하나의 논리 단위로 묶는 문제 — ACID가 약속하는 네 가지, 동시 실행이 낳는 이상 현상과 그것을 막는 격리 수준, 직렬성을 얻는 세 가지 구현, 저장 엔진이 그 아래에서 하는 일(로그와 복구, 래치), 그리고 노드 여러 대에 걸칠 때의 원자적 커밋
generated: { by: "claude-opus-5", at: "2026-08-14T00:00:00Z" }
---

# 데이터베이스 트랜잭션

읽기와 쓰기 여럿을 하나로 묶어 "전부 아니면 전무"로 만들고, 동시에 도는 다른 트랜잭션이
그것을 방해하지 못하게 하는 문제를 다룬다. 축은 넷이다 — **무엇을 약속하는가**(ACID),
**동시성이 무엇을 깨뜨리고 어떻게 막는가**(격리 수준과 그 구현), **저장 엔진이 그 아래에서
무엇을 하는가**(로그와 복구, 물리 무결성), 그리고 **노드가 여럿이면 커밋을 어떻게 원자적으로
만드는가**(분산 트랜잭션).

같은 데이터를 여러 곳에 두는 쪽은 [데이터 복제](../synthesis/data-replication.md), 데이터를
쪼개는 쪽은 [데이터 샤딩](../synthesis/data-sharding.md)에 있다. 카프카 제품 수준의
트랜잭션과 정확히 한 번 보장은 [카프카 신뢰성과 정확히 한 번](../synthesis/kafka-reliability.md)이
담당한다.

## 무엇을 약속하는가

- [트랜잭션과 ACID](../concepts/acid-transactions.md) — 네 글자가 각각 약속하는 것과
  원자성·일관성·격리·내구성이 실제로 뜻하는 범위
- [단일 객체 연산과 다중 객체 연산](../concepts/single-and-multi-object-operations.md) —
  보장이 객체 하나에 걸릴 때와 여럿에 걸칠 때, 그리고 중단과 재시도

## 무엇이 깨지는가

- [격리 수준과 이상 현상](../concepts/isolation-levels-and-anomalies.md) — 어느 수준이 어느
  경쟁 조건을 막는지 한 표로 본 자리
- [read committed 격리](../concepts/read-committed-isolation.md) — 더티 읽기와 더티 쓰기
- [스냅샷 격리와 MVCC](../concepts/snapshot-isolation-and-mvcc.md) — 읽기 스큐와 일관된
  스냅샷, 그리고 repeatable read라는 이름의 혼란
- [갱신 손실 막기](../concepts/preventing-lost-updates.md) — 읽기-수정-쓰기 사이클이 겹칠 때
- [쓰기 스큐와 팬텀](../concepts/write-skew-and-phantoms.md) — 직렬성만이 막는 이상

## 직렬성을 얻는 세 가지 방법

- [동시성 제어 기법의 분류](../concepts/concurrency-control-classification.md) — 낙관·다중 버전·
  비관 세 갈래와 스케줄·직렬 가능성의 정의
- [직렬 실행](../concepts/serial-execution.md) — 동시성을 아예 없애는 쪽
- [2단계 잠금](../concepts/two-phase-locking.md) — 비관적으로 잠그는 쪽
- [직렬성 스냅샷 격리](../concepts/serializable-snapshot-isolation.md) — 낙관적으로 진행한 뒤
  검사하는 쪽

## 저장 엔진이 그 아래에서 하는 일

- [쓰기 전 로그와 ARIES 복구](../concepts/write-ahead-log-and-aries.md) — 원자성과 내구성을
  실제로 구현하는 로그 규약, 스틸·포스 정책, 복구의 세 단계
- [래치와 B-트리 동시 접근](../concepts/latches-and-b-tree-concurrency.md) — 논리 무결성이 아닌
  물리 무결성을 지키는 쪽, 래치 크래빙과 하프 스플릿

## 노드가 여럿일 때

- [분산 트랜잭션과 2단계 커밋](../concepts/two-phase-commit.md) — 원자적 커밋 문제와 2PC,
  그리고 코디네이터가 죽었을 때의 인다우트
- [XA 트랜잭션과 이종 분산 트랜잭션](../concepts/xa-transactions.md) — 서로 다른 기술에 걸칠
  때의 표준과 그 한계, 데이터베이스 내부 구현과의 대비
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 분산 트랜잭션
  없이 멱등성으로 같은 것을 얻는 길

## 이웃 축

- [데이터베이스 관리 시스템의 구조](../concepts/dbms-architecture.md) — 트랜잭션 관리자와 잠금
  관리자가 놓이는 자리
- [카프카 트랜잭션](../concepts/kafka-transactions.md) — 메시지 브로커에서 트랜잭션이 무엇을
  뜻하는가
- [복제 지연이 만드는 이상](../concepts/replication-lag-anomalies.md) — 이름은 같지만 축이
  다른 일관성
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 분산으로 갈 때
  치르는 값

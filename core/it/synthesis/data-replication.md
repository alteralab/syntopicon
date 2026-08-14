---
type: synthesis
title: 데이터 복제
description: 같은 데이터를 여러 기계에 두는 세 가지 방식과 그 각각이 만드는 문제 — 리더를 하나 둘 것인가, 여럿 둘 것인가, 아예 두지 않을 것인가
generated: { by: "human:me", at: "2026-08-13T00:00:00Z" }
---

# 데이터 복제

네트워크로 이어진 여러 기계에 같은 데이터의 사본을 두는 문제를 다룬다. 축은 하나다 —
**변경을 노드 사이에 어떻게 실어 나르는가**이고, 답은 리더의 수로 갈린다. 리더
하나(single-leader), 리더 여럿(multi-leader), 리더 없음(leaderless)의 세 갈래를 따라가고 각
갈래가 낳는 고유한 문제를 붙였다.

같은 데이터를 여러 곳에 두는 것이 아니라 데이터를 조각으로 나눠 두는 쪽은 형제 허브인
[데이터 샤딩](../synthesis/data-sharding.md)에 있다. 둘은 대체로 독립적으로 고를 수 있고
실제 시스템은 보통 겹쳐 쓴다.

사본이 어긋났을 때 무엇을 약속하고 어떻게 되돌리는가는 형제 허브인
[레플리카 일관성](../synthesis/replica-consistency.md)에 있다.

합의 알고리즘으로 리더를 뽑는 쪽은 형제 허브인
[분산 합의](../synthesis/distributed-consensus.md)에, 카프카 제품 수준의 복제는
[카프카 내부 구조](../synthesis/kafka-internals.md)와
[카프카 신뢰성과 정확히 한 번](../synthesis/kafka-reliability.md)에 있다.

## 리더 하나

- [단일 리더 복제](../concepts/single-leader-replication.md) — 동기·비동기·반동기
  (semisynchronous)의 갈림, 새 팔로워 세우기, 페일오버(failover)가 틀어지는 다섯 방식
- [복제 로그의 구현 방식](../concepts/replication-log-implementations.md) — 문장 기반·WAL
  배송(WAL shipping)·논리 로그(logical log)와 변경 데이터 캡처(change data capture)
- [복제 지연이 만드는 이상](../concepts/replication-lag-anomalies.md) — 읽기 후
  쓰기(read-after-write)·단조 읽기(monotonic reads)·일관된 접두 읽기(consistent prefix
  reads)

## 리더 여럿

- [다중 리더 복제](../concepts/multi-leader-replication.md) — 다중 리전(multi-region)에서의
  네 축 비교, 복제 토폴로지(replication topology)와 쓰기 추월
- [싱크 엔진과 로컬 우선 소프트웨어](../concepts/sync-engines-and-local-first.md) — 기기
  하나가 리전(region) 하나인 극단
- [쓰기 충돌 해소](../concepts/write-conflict-resolution.md) — 충돌 회피·LWW·형제
  값(siblings)·CRDT와 OT

## 리더 없음

- [리더리스 복제](../concepts/leaderless-replication.md) — 읽기 복구(read repair)·힌티드
  핸드오프(hinted handoff)·안티 엔트로피(anti-entropy), 요청 헤징(request hedging)
- [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md) — `w + r > n`의 근거와 그 조건이 흔들리는 자리
- [동시 쓰기 판정](../concepts/detecting-concurrent-writes.md) — happens-before 관계, 버전
  번호와 버전 벡터(version vector)
- [안티 엔트로피 기전](../concepts/anti-entropy-mechanisms.md) — 읽기 복구·힌티드 핸드오프·
  머클 트리(Merkle tree)·비트맵 버전 벡터

## 이웃 축

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 복제가 답하는
  다섯 목적, 리전과 가용 영역(availability zone)
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 이 가족의 한 사례를 제품 수준에서 본 자리
- [카프카 다중 클러스터 아키텍처](../concepts/kafka-multicluster-architectures.md) —
  액티브-액티브(active-active)라는 이름의 다중 리더
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 복제 자체를
  오브젝트 스토리지(object storage)에 맡기는 흐름
- [레플리카 일관성](../synthesis/replica-consistency.md) — 사본이 갈라졌을 때의 계약과 수렴 장치
- [가십 전파](../concepts/gossip-dissemination.md) — 데이터가 아니라 클러스터 메타데이터를
  실어 나르는 쪽

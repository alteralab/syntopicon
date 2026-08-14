---
type: synthesis
title: 데이터 샤딩
description: 데이터셋을 여러 노드로 쪼개 나누는 문제 — 무엇을 기준으로 자를 것인가(키 범위·해시), 쏠림을 어떻게 되돌릴 것인가, 어느 노드에 물을지 어떻게 아는가, 그리고 색인은 어떻게 따라가는가
generated: { by: "human:me", at: "2026-08-13T17:00:00Z" }
---

# 데이터 샤딩

데이터가 너무 많거나 쓰기가 너무 많아 기계 한 대가 감당하지 못할 때, 데이터셋을 조각으로
나눠 여러 노드에 두는 문제를 다룬다. 축은 셋이다 — **무엇을 기준으로 자르는가**, **자른
조각이 고르지 않을 때 어떻게 되돌리는가**, 그리고 **자르고 나서 찾는 법을 어떻게 유지하는가**.

같은 데이터를 여러 곳에 두는 쪽은 형제 허브인 [데이터 복제](../synthesis/data-replication.md)에
있다. 둘은 대체로 독립적으로 고를 수 있고, 실제 시스템은 보통 둘을 겹쳐 쓴다. 카프카 제품
수준의 파티션 운영은 [카프카 내부 구조](../synthesis/kafka-internals.md)와
[카프카 설치와 운영](../synthesis/kafka-operations.md)에 있다.

## 무엇이고 왜 하는가

- [샤딩의 기본](../concepts/sharding-basics.md) — 샤드(shard)라는 단위와 제품마다 다른
  이름들, 복제와 겹쳐 놓은 그림, 확장성(scalability) 대신 치르는 값
- [멀티테넌시를 위한 샤딩](../concepts/sharding-for-multitenancy.md) — 확장성이 아니라
  격리를 목적으로 나눌 때 얻는 일곱 가지와 막히는 세 곳

## 무엇을 기준으로 자르는가

- [키 범위 샤딩](../concepts/key-range-sharding.md) — 정렬 순서를 살리는 대신 인접 키 쓰기를
  떠안는 쪽
- [해시 샤딩](../concepts/hash-sharding.md) — 근접성을 버려 고르게 펴는 쪽, 고정 샤드 수와 해시
  범위 샤딩
- [일관 해싱](../concepts/consistent-hashing.md) — 샤드 수가 바뀔 때 옮기는 키를 최소화하는
  함수 계열

## 고르지 않을 때

- [핫스팟과 쏠린 워크로드](../concepts/relieving-hot-spots.md) — 치우침(skew)·핫 샤드(hot
  shard)·핫 키(hot key)와 두 가지 처방
- [샤드 리밸런싱 운영](../concepts/shard-rebalancing-operations.md) — 분할과 이동을 자동에
  맡길 것인가 사람이 볼 것인가

## 자르고 나서 찾기

- [요청 라우팅](../concepts/request-routing.md) — 어느 노드에 물어야 하는지 아는 세 가지 배치와
  코디네이션 서비스
- [샤딩과 2차 색인](../concepts/sharding-and-secondary-indexes.md) — 로컬(문서 분할,
  document-partitioned)과 글로벌(용어 분할, term-partitioned), 각각이 비싸게 만드는 쪽

## 이웃 축

- [단일 리더 복제](../concepts/single-leader-replication.md) — 샤드마다 리더가 하나라는 그림
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 카프카에서 샤드가 불리는 이름
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 해시 파티셔닝과 핫 키
  대응이 제품 수준에서 나타나는 자리
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 샤드
  이동을 손으로 하는 실제 절차
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) —
  샤딩(sharding)을 피하라는 권고가 놓인 자리

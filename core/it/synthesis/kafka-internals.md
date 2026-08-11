---
type: synthesis
title: 카프카 내부 구조
description: 브로커가 메타데이터를 관리하고 요청을 처리하며 데이터를 저장하는 기제 진입점
generated: { by: "human:me", at: "2026-08-10T19:00:00Z" }
---

# 카프카 내부 구조

브로커 안에서 무슨 일이 일어나는지를 다룬다. 클러스터 전체의 개요는
[브로커와 클러스터](../concepts/brokers-and-clusters.md)가 담당하고, 여기서는
그 개요가 가리키는 기제를 하나씩 편다.

## 메타데이터와 조율

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — **Kafka 3.9 이하**의 메타데이터 저장과 컨트롤러 선출, 그리고 그 방식을 버린 동기. 3.x 클러스터를 운영하는 동안 계속 참인 서술이다
- [KRaft 컨트롤러 쿼럼](../concepts/kraft-controller-quorum.md) — **Kafka 4.0 이상**에서 그 자리를 대신하는 컨트롤러 쿼럼의 구성과 운영. 쿼럼이 쓰는 알고리즘은 [분산 합의](distributed-consensus.md)가 담당한다
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 인싱크 판정이 리더 선출 자격을 정하는 방식과 선호 리더

## 요청과 저장

- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 요청이 브로커 안에서 지나는 경로, 퍼거토리와 제로카피
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 파티션 할당과 세그먼트, 파일 형식과 인덱스
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 키별 최신값만 남기는 보존의 동작

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 신뢰성과 정확히 한 번](kafka-reliability.md) — 인-싱크 레플리카가 없어졌을 때의 리더 선출과 트랜잭션의 브로커 쪽 구현

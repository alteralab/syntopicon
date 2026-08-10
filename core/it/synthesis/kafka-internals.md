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

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 클러스터 메타데이터 저장과 컨트롤러 선출, 그리고 그 교체 계획
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 인싱크 판정이 리더 선출 자격을 정하는 방식과 선호 리더

## 요청과 저장

- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 요청이 브로커 안에서 지나는 경로, 퍼거토리와 제로카피
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 파티션 할당과 세그먼트, 파일 형식과 인덱스
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 키별 최신값만 남기는 보존의 동작

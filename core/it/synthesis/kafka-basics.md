---
type: synthesis
title: 카프카 기초
description: 발행/구독 패턴부터 카프카의 데이터 단위, 저장 구조, 클라이언트, 클러스터, 선택 근거, 유스케이스, 기원까지의 진입점
generated: { by: "human:me", at: "2026-08-10T17:30:00Z" }
---

# 카프카 기초

## 패턴과 데이터 단위

- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 직접 연결이 무너지는 경로와 브로커가 등장하는 지점
- [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md) — 분산 커밋 로그 관점과 데이터 단위 3종

## 저장 구조와 클라이언트

- [토픽과 파티션](../concepts/topics-and-partitions.md) — 순서 보장의 경계와 확장, 복제의 단위
- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 파티셔너, 오프셋, 컨슈머 그룹의 파티션 소유권
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 컨트롤러와 리더십, 보존과 로그 압착, 다중 클러스터

## 왜 쓰고 어디에 쓰나

- [왜 카프카인가](../concepts/why-kafka.md) — 다른 발행/구독 시스템 대신 고르는 근거 6가지
- [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md) — 순환계 관점과 대표 유스케이스 5종
- [카프카의 기원](../concepts/kafka-origin-at-linkedin.md) — 링크드인의 실패가 설계 목표 4가지를 결정한 과정

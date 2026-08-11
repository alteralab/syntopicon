---
type: synthesis
title: 카프카
description: 발행/구독 패턴과 데이터 단위부터 브로커 내부, 설치와 운영까지 카프카 축의 부모 허브
generated: { by: "human:me", at: "2026-08-10T19:00:00Z" }
---

# 카프카

## 하위 허브

- [카프카 내부 구조](kafka-internals.md) — 메타데이터와 조율, 요청 처리와 물리적 저장
- [카프카 클라이언트](kafka-clients.md) — 프로듀서와 컨슈머가 브로커와 주고받는 쪽. 전송 경로와 설정, 파티션 배분, 직렬화, 컨슈머 그룹과 오프셋
- [카프카 설치와 운영](kafka-operations.md) — 설정과 산정, 프로덕션 준비

## 패턴과 데이터 단위

- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 직접 연결이 무너지는 경로와 브로커가 등장하는 지점
- [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md) — 분산 커밋 로그 관점과 데이터 단위 3종

## 저장 구조

- [토픽과 파티션](../concepts/topics-and-partitions.md) — 순서 보장의 경계와 확장, 복제의 단위
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 컨트롤러와 리더십, 보존과 로그 압착, 다중 클러스터

## 왜 쓰고 어디에 쓰나

- [왜 카프카인가](../concepts/why-kafka.md) — 다른 발행/구독 시스템 대신 고르는 근거 6가지
- [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md) — 순환계 관점과 대표 유스케이스 5종
- [카프카의 기원](../concepts/kafka-origin-at-linkedin.md) — 링크드인의 실패가 설계 목표 4가지를 결정한 과정

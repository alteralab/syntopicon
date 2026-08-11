---
type: synthesis
title: 카프카
description: 발행/구독 패턴과 데이터 단위부터 브로커 내부, 설치와 운영까지 카프카 축의 부모 허브
generated: { by: "human:me", at: "2026-08-10T19:00:00Z" }
---

# 카프카

## 하위 허브

- [카프카 내부 구조](kafka-internals.md) — 메타데이터와 조율, 요청 처리와 물리적 저장
- [카프카 설치와 운영](kafka-operations.md) — 설정과 산정, 프로덕션 준비

## 패턴과 데이터 단위

- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 직접 연결이 무너지는 경로와 브로커가 등장하는 지점
- [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md) — 분산 커밋 로그 관점과 데이터 단위 3종

## 저장 구조와 클라이언트

- [토픽과 파티션](../concepts/topics-and-partitions.md) — 순서 보장의 경계와 확장, 복제의 단위
- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 클라이언트 2종의 개요. 아래 상세 페이지들의 진입점
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 컨트롤러와 리더십, 보존과 로그 압착, 다중 클러스터
- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — `send()` 한 번이 거치는 부품, 세 가지 전송 방식, 헤더와 인터셉터
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — `acks`, 전달 시간 예산을 나눠 갖는 타임아웃들, 배치와 멱등성
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 키가 있을 때와 없을 때의 배분 규칙, 파티션 추가가 그 규칙을 깨는 지점
- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) — 커스텀 시리얼라이저가 무너지는 지점, 에이브로의 스키마 진화, 컨슈머 쪽 디시리얼라이저
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 브로커가 쓰기·읽기 속도를 제한하고 스로틀링을 집행하는 방식
- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 파티션 소유권 배정 절차, 조급한 리밸런스와 협력적 리밸런스, 정적 그룹 멤버십
- [컨슈머 폴 루프](../concepts/kafka-consumer-poll-loop.md) — `poll()`이 데이터 말고 하는 일과 폴을 멈췄을 때의 판정
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — 페치 크기와 대기 시간, 세션 타임아웃, 파티션 할당 전략 4종
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 커밋 시점의 선택이 남기는 중복과 누락, `commitSync`와 `commitAsync`

## 왜 쓰고 어디에 쓰나

- [왜 카프카인가](../concepts/why-kafka.md) — 다른 발행/구독 시스템 대신 고르는 근거 6가지
- [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md) — 순환계 관점과 대표 유스케이스 5종
- [카프카의 기원](../concepts/kafka-origin-at-linkedin.md) — 링크드인의 실패가 설계 목표 4가지를 결정한 과정

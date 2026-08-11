---
type: synthesis
title: 카프카 클라이언트
description: 프로듀서와 컨슈머가 브로커와 주고받는 쪽 진입점 — 전송 경로와 설정, 파티션 배분, 직렬화, 컨슈머 그룹과 오프셋
generated: { by: "human:me", at: "2026-08-12T09:00:00Z" }
---

# 카프카 클라이언트

**애플리케이션 쪽에서 손대는 것들이다.** 브로커 안에서 벌어지는 일은
[카프카 내부 구조](kafka-internals.md)가, 클러스터를 세우고 재는 일은
[카프카 설치와 운영](kafka-operations.md)이 담당한다. 여기는 그 사이 —
`send()`와 `poll()`을 부르는 쪽이다.

두 방향으로 갈린다. 프로듀서는 **한 번 보낸 것이 어디로 가고 언제 성공으로 치는가**를
정하고, 컨슈머는 **어디까지 읽었다고 볼 것인가**를 정한다. 앞쪽은 파티션 배분과
`acks`가, 뒤쪽은 오프셋 커밋 시점이 결정한다.

## 개요

- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 클라이언트 2종이 무엇을 하는지의 진입점. 아래 상세로 가는 갈림길

## 프로듀서

- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — `send()` 한 번이 거치는 부품, 세 가지 전송 방식, 헤더와 인터셉터
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — `acks`, 전달 시간 예산을 나눠 갖는 타임아웃들, 배치와 멱등성
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 키가 있을 때와 없을 때의 배분 규칙, 파티션 추가가 그 규칙을 깨는 지점

## 컨슈머

- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 파티션 소유권 배정 절차, 조급한 리밸런스와 협력적 리밸런스, 정적 그룹 멤버십
- [컨슈머 폴 루프](../concepts/kafka-consumer-poll-loop.md) — `poll()`이 데이터 말고 하는 일과 폴을 멈췄을 때의 판정
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — 페치 크기와 대기 시간, 세션 타임아웃, 파티션 할당 전략 4종
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 커밋 시점의 선택이 남기는 중복과 누락, `commitSync`와 `commitAsync`

## 양쪽에 걸리는 것

- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) — 커스텀 시리얼라이저가 무너지는 지점, 에이브로의 스키마 진화, 컨슈머 쪽 디시리얼라이저
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 브로커가 쓰기·읽기 속도를 제한하고 스로틀링을 집행하는 방식
- [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md) — 클라이언트가 주고받는 데이터 단위 3종

## 이어지는 허브

- [카프카 기초](kafka-basics.md) — 이 허브의 상위. 패턴과 저장 구조
- [카프카 내부 구조](kafka-internals.md) — 클라이언트가 보낸 요청을 브로커가 처리하는 쪽
- [카프카 신뢰성과 정확히 한 번](kafka-reliability.md) — 이 설정들이 지키려는 보장, 그리고 멱등적 프로듀서와 트랜잭션

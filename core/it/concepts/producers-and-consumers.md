---
type: concept
title: 프로듀서와 컨슈머
description: 카프카 클라이언트 2종의 역할 — 프로듀서의 파티션 배분과 파티셔너, 컨슈머의 오프셋 기록, 컨슈머 그룹의 파티션 소유권이 수평 확장과 장애 인계를 만드는 방식. 각 항목의 기제는 전용 페이지로 갈라진다
generated: { by: "claude-opus-5", at: "2026-08-12T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 프로듀서와 컨슈머

- [프로듀서](#프로듀서)
- [컨슈머와 오프셋](#컨슈머와-오프셋)
- [컨슈머 그룹과 파티션 소유권](#컨슈머-그룹과-파티션-소유권)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **카프카를 쓰는 쪽은 무엇을 알아야 하고, 무엇을 카프카에 맡기는가.**

> **이 페이지는 개요다.** 아래 각 절의 기제는 전용 페이지로 갈라져 있다 —
> 프로듀서 쪽은 [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md),
> [프로듀서 설정](../concepts/kafka-producer-configuration.md),
> [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md),
> [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md),
> 컨슈머 쪽은 [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md),
> [컨슈머 폴 루프](../concepts/kafka-consumer-poll-loop.md),
> [컨슈머 설정](../concepts/kafka-consumer-configuration.md),
> [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md),
> 양쪽에 걸치는 것은
> [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md).

- 카프카 클라이언트는 이 시스템의 사용자이며 기본 유형은 프로듀서와 컨슈머 둘이다.
  상위 클라이언트 API로 데이터 통합용 Kafka Connect API와 스트림 처리용 Kafka
  Streams가 있고, 이 상위 클라이언트들은 **프로듀서와 컨슈머를 구성 요소로 삼아**
  고차 기능을 얹는다 (1장, p.6).[^shapira2021]
- 카프카에는 내장 클라이언트 외에 **바이너리 와이어 프로토콜**이 있다. 올바른 바이트
  시퀀스를 카프카의 네트워크 포트로 보내는 것만으로 메시지를 읽고 쓸 수 있으며,
  **C++·파이썬·Go 등 여러 언어로 이 프로토콜을 구현한 클라이언트가 여럿 있다.** 그
  클라이언트들은 아파치 카프카 프로젝트의 일부가 아니고 비자바 클라이언트 목록은 프로젝트
  위키가 관리한다 (3장, p.48).[^shapira2021]

## 프로듀서

- 프로듀서(producer)는 새 메시지를 만든다. 다른 발행/구독 시스템에서는
  발행자(publisher)나 작성자(writer)라 부른다 (1장, p.6).[^shapira2021]
- 메시지는 특정 토픽으로 생산된다. **기본값은 토픽의 파티션들에 고르게 분산**하는
  것이다 (1장, p.6).[^shapira2021]
- 특정 파티션으로 보내야 하는 경우에는 메시지 키와 파티셔너(partitioner)를 쓴다 —
  파티셔너가 키의 해시를 만들어 특정 파티션에 대응시키므로, **주어진 키로 생산된
  모든 메시지는 같은 파티션에 쓰인다** (1장, p.6).[^shapira2021]
- 다른 업무 규칙으로 메시지를 파티션에 대응시키는 커스텀 파티셔너도 쓸 수 있다
  (1장, pp.6–7).[^shapira2021]

## 컨슈머와 오프셋

- 컨슈머(consumer)는 메시지를 읽는다. 다른 발행/구독 시스템에서는
  구독자(subscriber)나 독자(reader)라 부른다 (1장, p.7).[^shapira2021]
- 컨슈머는 하나 이상의 토픽을 구독하고, **각 파티션에 생산된 순서 그대로** 메시지를
  읽는다 (1장, p.7).[^shapira2021]
- 어디까지 읽었는지는 오프셋(offset)으로 추적한다 (1장, p.7):[^shapira2021]
  - 오프셋은 카프카가 메시지를 생산할 때 붙이는 메타데이터로, 계속 증가하는 정수값이다.
  - 주어진 파티션 안에서 각 메시지는 유일한 오프셋을 가지며 뒤 메시지가 더 큰 오프셋을
    가진다 — **다만 반드시 단조 증가(monotonically greater)일 필요는 없다**.
  - 파티션별로 다음에 읽을 오프셋을 저장(대개 카프카 자체에)함으로써, 컨슈머는 멈췄다
    다시 시작해도 자리를 잃지 않는다.

## 컨슈머 그룹과 파티션 소유권

- 컨슈머는 컨슈머 그룹(consumer group)의 일원으로 동작한다. 그룹은 하나의 토픽을 함께
  소비하는 하나 이상의 컨슈머다 (1장, p.7).[^shapira2021]
- 그룹이 보장하는 것: **각 파티션은 그룹 안 한 멤버에게만 소비된다.** 컨슈머와
  파티션의 대응 관계를 파티션 소유권(ownership)이라 부른다 (1장,
  p.7).[^shapira2021]
- 여기서 두 가지 성질이 따라 나온다 (1장, p.7):[^shapira2021]
  - 메시지가 많은 토픽을 읽기 위해 컨슈머를 **수평 확장**할 수 있다.
  - 컨슈머 하나가 죽으면 그룹의 남은 멤버들이 그 파티션을 재할당받아 이어받는다.
- 그룹 멤버 수와 파티션 수의 관계상 한 컨슈머가 여러 파티션을 맡을 수도 있다 —
  파티션 4개를 컨슈머 3개가 읽으면 둘은 하나씩, 나머지 하나가 두 파티션을 맡는다
  (1장, p.7, 그림 1-6).[^shapira2021]

## 이어지는 페이지

- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — `send()` 한 번이
  거치는 부품과 세 가지 전송 방식
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — `acks`와 전달 시간
  예산, 배치와 멱등성
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 파티셔너가
  파티션을 고르는 규칙과 그 규칙이 깨지는 조건
- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md)
  — 객체를 바이트로 바꾸는 일을 무엇에 맡길 것인가
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 브로커가 클라이언트
  속도를 제한하는 기제
- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 파티션
  소유권이 배정되고 옮겨지는 절차
- [컨슈머 폴 루프](../concepts/kafka-consumer-poll-loop.md) — 컨슈머가 데이터를 읽는
  루프와 그것을 멈췄을 때 일어나는 일
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — 페치 크기·세션
  타임아웃·할당 전략
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 오프셋 기록 시점의
  선택이 남기는 중복과 누락
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 소유권의 단위가 되는 그
  파티션
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 프로듀서가 리더에
  접속해야 하고 컨슈머는 팔로워에서도 읽을 수 있는 이유

[^shapira2021]: Shapira et al. 2021, 1장 "Meet Kafka" · 3장 "Kafka Producers: Writing Messages to Kafka"

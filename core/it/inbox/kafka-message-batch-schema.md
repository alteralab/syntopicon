---
type: concept
title: 카프카의 메시지, 배치, 스키마
description: 카프카를 분산 커밋 로그로 보는 관점과 데이터 단위 3종 — 메시지와 키, 배치가 만드는 지연·처리량 트레이드오프, 스키마를 따로 강제해야 하는 이유와 그 권고가 클라이언트에서 실행되는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카의 메시지, 배치, 스키마

하나의 질문: **카프카는 데이터를 어떤 단위로 담는가.** 아파치 카프카는
[발행/구독 메시징](../concepts/publish-subscribe-messaging.md)에서 드러난
중앙 집중 시스템의 필요를 풀려고 만들어진 발행/구독 메시징 시스템이다 (1장,
p.4).[^shapira2021]

## 분산 커밋 로그라는 관점

- 카프카는 흔히 "분산 커밋 로그(distributed commit log)", 더 최근에는 "분산
  스트리밍 플랫폼(distributing streaming platform)"으로 서술된다 (1장,
  p.4).[^shapira2021]
- 원문 직인용 (1장, p.4):[^shapira2021]

> A filesystem or database commit log is designed to provide a durable record of
> all transactions so that they can be replayed to consistently build the state
> of a system. Similarly, data within Kafka is stored durably, in order, and can
> be read deterministically.

- 여기에 더해 데이터는 시스템 안에 분산 저장될 수 있어, 장애에 대한 추가 보호와
  성능 확장의 기회를 함께 준다 (1장, p.4).[^shapira2021]

## 메시지와 키

- 메시지(message)가 카프카 안 데이터의 단위다. 데이터베이스 배경이라면 로우(row)나
  레코드(record)에 해당한다고 보면 된다 (1장, p.4).[^shapira2021]
- 카프카에게 메시지는 단순한 바이트 배열이다 — **포함된 데이터에 특정 형식이나
  의미가 없다** (1장, p.4).[^shapira2021]
- 키(key)는 메시지가 가질 수 있는 선택적 메타데이터다. 키 역시 바이트 배열이며
  카프카에게 특별한 의미가 없다 (1장, p.4).[^shapira2021]
- 키의 용도는 메시지를 파티션에 더 통제된 방식으로 쓰는 것이다. 가장 단순한 방식은
  키의 일관된 해시를 만든 뒤 그 값을 토픽의 파티션 수로 나눈 나머지로 파티션 번호를
  고르는 것으로, **파티션 수가 변하지 않는 한** 같은 키의 메시지는 항상 같은
  파티션에 쓰인다 (1장, pp.4–5).[^shapira2021]
- 키·밸류 외에 **헤더(header)**도 붙일 수 있다 — 키/밸류 쌍 자체는 건드리지 않고
  레코드에 메타데이터를 얹는 자리이며, 계보 표시와 라우팅·추적에 쓰인다 (3장,
  p.71).[^shapira2021]

## 배치 — 지연과 처리량의 트레이드오프

- 효율을 위해 메시지는 배치(batch) 단위로 쓰인다. 배치는 **같은 토픽·파티션으로
  생산되는 메시지들의 묶음**일 뿐이다 (1장, p.5).[^shapira2021]
- 존재 이유: 메시지마다 네트워크를 왕복하면 오버헤드가 과도해지고, 묶어 보내면
  이것이 줄어든다 (1장, p.5).[^shapira2021]
- 대가는 지연(latency)과 처리량(throughput)의 트레이드오프다 — **배치가 클수록
  단위 시간당 처리 메시지 수는 늘어나고, 개별 메시지가 전파되는 데 걸리는 시간은
  길어진다** (1장, p.5).[^shapira2021]
- 배치는 대개 압축되어, 약간의 처리 능력을 들이는 대신 더 효율적인 전송·저장을
  얻는다 (1장, p.5).[^shapira2021]

## 스키마 — 왜 밖에서 강제해야 하는가

- 카프카 자신에게 메시지는 불투명한 바이트 배열이므로, 내용을 쉽게 이해할 수 있도록
  **추가 구조 즉 스키마(schema)를 메시지 내용에 부여할 것을 권장한다** (1장,
  p.5).[^shapira2021]
- 선택지와 한계 (1장, p.5):[^shapira2021]
  - JSON·XML은 쓰기 쉽고 사람이 읽을 수 있지만, 견고한 타입 처리와 스키마 버전 간
    호환성 같은 기능이 없다.
  - 많은 카프카 개발자가 아파치 에이브로(Avro)를 선호한다 — 원래 하둡용으로 개발된
    직렬화(serialization) 프레임워크다.
  - 에이브로가 주는 것: 조밀한 직렬화 형식, 메시지 페이로드와 분리된 스키마(변경 시
    코드 생성 불필요), 강한 데이터 타이핑, 상위·하위 호환을 모두 갖춘 스키마 진화.
- 일관된 데이터 형식이 중요한 이유는 메시지 쓰기와 읽기를 **분리(decouple)** 하기
  때문이다 (1장, p.5).[^shapira2021]
  - 밀결합돼 있으면 구독 애플리케이션을 먼저 신·구 형식 동시 지원으로 갱신해야 하고,
    그 다음에야 발행 애플리케이션이 새 형식을 쓸 수 있다.
  - 잘 정의된 스키마를 공용 저장소에 두면 이런 조율 없이도 카프카 안 메시지가
    이해된다.
- 이 권고가 실제로 집행되는 자리는 **클라이언트의 시리얼라이저와 디시리얼라이저**다 —
  스키마를 레지스트리에 저장하고 레코드에는 식별자만 담는 일까지 전부 그 안에서
  이뤄지므로, 생산하는 코드는 다른 시리얼라이저를 쓰듯 에이브로 시리얼라이저를 쓸 뿐이다
  (3장, pp.65–66).[^shapira2021]

## 이어지는 페이지

- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md)
  — 위 권고의 실행 형태: 커스텀 시리얼라이저가 무너지는 지점, 에이브로의 스키마 진화,
  스키마 레지스트리
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 키가 결정하는 그 파티션이
  무엇이고 왜 순서 보장의 경계인가
- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 키와 파티셔너를
  실제로 쓰는 쪽
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — 배치 크기·`linger.ms`·
  압축이 위 트레이드오프를 실제로 정하는 자리

[^shapira2021]: Shapira et al. 2021, 1장 "Meet Kafka" · 3장 "Kafka Producers: Writing Messages to Kafka"

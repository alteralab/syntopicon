---
type: concept
title: 토픽과 파티션
description: 카프카의 메시지 분류 단위와 그 아래의 추가 전용 로그 — 순서 보장이 파티션 안에서만 성립하는 이유, 파티션이 곧 확장·복제의 단위인 점, 스트림이라는 용어의 범위, 그리고 이 "파티션"이 일반 문헌의 샤드와 같은 것이라는 사실
generated: { by: "claude-opus-5", at: "2026-08-13T17:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 토픽과 파티션

하나의 질문: **카프카는 메시지를 어떻게 분류하고, 그 분류가 어떤 보장과 어떤
확장성을 만드는가.**

## 토픽

- 카프카의 메시지는 토픽(topic) 단위로 분류된다. 가장 가까운 비유는 데이터베이스의
  테이블 또는 파일시스템의 폴더다 (1장, p.5).[^shapira2021]
- 토픽은 다시 여러 개의 파티션(partition)으로 나뉜다 (1장, p.5).[^shapira2021]

## 파티션 = 하나의 로그

- ["분산 커밋 로그"](../concepts/kafka-message-batch-schema.md) 서술로 돌아가면,
  **파티션 하나가 로그 하나**다. 메시지는 파티션 끝에 추가 전용(append-only)으로
  쓰이고, 맨 앞에서 끝까지 순서대로 읽힌다 (1장, p.5).[^shapira2021]
- 순서 보장의 경계: 토픽은 대개 파티션을 여럿 가지므로 **토픽 전체에 걸친 메시지
  순서는 보장되지 않고, 단일 파티션 안에서만 보장된다** (1장,
  pp.5–6).[^shapira2021]
- 이 때문에 순서가 중요한 메시지를 같은 파티션으로 몰아넣는 장치가 필요해진다 —
  [메시지 키와 파티셔너](../concepts/kafka-message-batch-schema.md)가 그 장치다
  (1장, pp.4–5).[^shapira2021]

## 파티션이 만드는 중복성과 확장성

- 파티션은 카프카가 중복성(redundancy)과 확장성(scalability)을 제공하는 방식이기도
  하다 (1장, p.6).[^shapira2021]
  - 각 파티션은 서로 다른 서버에 호스팅될 수 있다 — 즉 **하나의 토픽이 여러 서버로
    수평 확장되어 단일 서버의 능력을 훨씬 넘는 성능을 낸다**.
  - 파티션은 복제(replicate)될 수 있다 — 서로 다른 서버가 같은 파티션의 사본을
    저장하므로 서버 한 대가 죽어도 견딘다.
- 복제와 리더십의 구체적 규칙은 [브로커와 클러스터](../concepts/brokers-and-clusters.md)로
  이어진다 (1장, p.8).[^shapira2021]

## 파티션은 일반 문헌의 샤드다

- 이름의 대응이 명시돼 있다 — **DDIA가 샤드(shard)라 부르는 것은 쓰는 소프트웨어에 따라
  이름이 여럿이며, 카프카에서는 그것이 파티션(partition)이다.** 같은 자리에 CockroachDB의
  range, HBase·TiDB의 region, Couchbase의 vBucket, Riak의 vnode, 카산드라의 token-range,
  Bigtable·YugabyteDB·ScyllaDB의 tablet이 열거된다 (7장, p.252).[^kleppmann2026]
  - **파티셔닝과 샤딩(sharding)을 구별되는 두 개념으로 취급하는 데이터베이스도 있다** — PostgreSQL에서
    파티셔닝은 **큰 테이블 하나를 같은 기계의 여러 파일로 쪼개는 일**이고 샤딩은 **여러 기계에
    걸쳐 쪼개는 일**이다. **다른 많은 시스템에서는 파티셔닝이 그냥 샤딩의 다른 말**이다 (7장,
    p.252).[^kleppmann2026] 카프카의 파티션은 뒤쪽, 즉 여러 브로커에 흩어지는 단위다.
- 헷갈리기 쉬운 이름 하나가 따로 못박혀 있다 — **파티셔닝은 네트워크 파티션(network
  partition, netsplit)과는 아무 관계가 없다.** 그쪽은 노드 사이 네트워크의 결함 유형이다
  (7장, p.252).[^kleppmann2026]
- 위 [파티션이 만드는 중복성과 확장성](#파티션이-만드는-중복성과-확장성)이 말한 두 축은 일반
  문헌에서도 그대로 갈린다 — **분산 데이터베이스가 여러 노드에 데이터를 나누는 방식은 보통
  둘로, 같은 데이터의 사본을 여러 노드에 저장하는 복제와, 데이터를 더 작은 샤드로 쪼개 서로
  다른 노드에 저장하는 샤딩이다** (7장, p.251).[^kleppmann2026] 카프카의 파티션은 이 둘을 다
  담당하는 단위여서 한 이름 아래 두 축이 겹쳐 있다.

## 스트림이라는 용어

- 카프카 같은 시스템의 데이터를 논할 때 스트림(stream)이라는 용어가 자주 쓰인다.
  대개 스트림은 **파티션 수와 무관하게 하나의 토픽에 담긴 데이터 한 벌**로 간주되며,
  프로듀서에서 컨슈머로 흐르는 단일한 데이터 흐름을 나타낸다 (1장,
  p.6).[^shapira2021]
- 이런 어법은 스트림 처리(stream processing)를 논할 때 가장 흔하다 — Kafka
  Streams·Apache Samza·Storm 같은 프레임워크가 메시지를 실시간으로 다룬다 (1장,
  p.6).[^shapira2021]
- 대비되는 축은 하둡 같은 오프라인 프레임워크로, 대량 데이터를 나중에 처리하도록
  설계됐다 (1장, p.6).[^shapira2021]

## 이어지는 페이지

- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 레코드가 어느 파티션에
  갈지 정하는 규칙
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 복제와 리더십의 구체적 규칙
- [샤딩의 기본](../concepts/sharding-basics.md) — 파티션이라는 이름이 속한 일반 개념
- [키 범위 샤딩](../concepts/key-range-sharding.md) — 카프카가 쓰지 않는 다른 자르기 기준
- [해시 샤딩](../concepts/hash-sharding.md) — 카프카의 키 해시 배분이 속한 계열

[^shapira2021]: Shapira et al. 2021, 1장 "Meet Kafka"

[^kleppmann2026]: Kleppmann & Riccomini 2026, 7장 "Sharding"

---
type: concept
title: 프로듀서 파티션 배분
description: 레코드가 어느 파티션으로 갈지 정하는 규칙 — 키가 있을 때의 해시 배분과 키가 없을 때의 스티키 라운드 로빈, 기본 파티셔너 외의 선택지, 파티션 수가 변하면 대응이 깨지는 성질, 그리고 커스텀 파티셔너를 만드는 이유
generated: { by: "claude-opus-5", at: "2026-08-12T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 프로듀서 파티션 배분

- [키가 하는 두 가지 일](#키가-하는-두-가지-일)
- [키가 없을 때 — 스티키 라운드 로빈](#키가-없을-때--스티키-라운드-로빈)
- [키가 있을 때 — 해시 배분](#키가-있을-때--해시-배분)
- [기본 파티셔너 밖의 선택지](#기본-파티셔너-밖의-선택지)
- [파티션 수가 변하면 대응이 깨진다](#파티션-수가-변하면-대응이-깨진다)
- [커스텀 파티셔너](#커스텀-파티셔너)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **레코드가 어느 파티션에 쓰일지는 무엇이 정하고, 그 규칙은 언제
깨지는가.**

## 키가 하는 두 가지 일

- 카프카 메시지는 키/밸류 쌍이다. **토픽과 밸류만으로 `ProducerRecord`를 만들 수 있고
  그러면 키는 기본적으로 `null`이 되지만, 대부분의 애플리케이션은 키를 붙여
  생산한다** (3장, p.68).[^shapira2021]
- 키의 목적은 둘이다 (3장, p.68):[^shapira2021]
  - **메시지와 함께 저장되는 추가 정보**다.
  - **메시지가 쓰일 토픽 파티션을 정하는 데 통상 쓰인다.** 압착된 토픽(compacted topic)
    에서도 중요한 역할을 한다.
- 따라오는 성질: **같은 키를 가진 모든 메시지는 같은 파티션으로 간다.** 어떤 프로세스가
  토픽의 파티션 일부만 읽고 있다면 **하나의 키에 대한 모든 레코드는 같은 프로세스가
  읽게 된다** (3장, p.68).[^shapira2021]

## 키가 없을 때 — 스티키 라운드 로빈

- 키가 `null`이고 기본 파티셔너를 쓰면 레코드는 **토픽의 가용 파티션 중 하나로 무작위
  전송**되며, 파티션 사이 균형을 맞추는 데 **라운드 로빈(round robin)** 알고리즘이
  쓰인다 (3장, p.69).[^shapira2021]
- 아파치 카프카 2.4 프로듀서부터, 키가 `null`일 때 기본 파티셔너가 쓰는 라운드 로빈
  알고리즘은 **스티키(sticky)**하다 — **한 파티션으로 가는 메시지 배치를 채운 뒤에야
  다음 파티션으로 전환한다.** 그 결과 같은 수의 메시지를 **더 적은 요청으로** 보내게 돼
  **지연이 낮아지고 브로커의 CPU 사용이 줄어든다** (3장, p.69).[^shapira2021]
  - 버전 조건: Kafka 2.4 이상 — 그 이전 프로듀서의 기본 파티셔너는 이 스티키 처리를
    하지 않는다.

## 키가 있을 때 — 해시 배분

- 키가 있고 기본 파티셔너를 쓰면 카프카는 **키를 해시하고**(자바가 업그레이드돼도 해시
  값이 바뀌지 않도록 **카프카 자체의 해시 알고리즘**을 쓴다) 그 결과로 메시지를 특정
  파티션에 대응시킨다 (3장, p.69).[^shapira2021]
- 대응의 대상 집합에 주의한다 — **키가 항상 같은 파티션에 대응되는 것이 중요하므로,
  가용 파티션이 아니라 토픽의 모든 파티션을 써서 대응을 계산한다.** 그래서 **특정
  파티션이 사용 불가인 상태에서 그 파티션으로 쓰면 에러를 받을 수 있다** — 드문 일이다
  (3장, p.69).[^shapira2021]

## 기본 파티셔너 밖의 선택지

- 기본 파티셔너 외에 카프카 클라이언트는 `RoundRobinPartitioner`와
  `UniformStickyPartitioner`도 제공한다. 이들은 **메시지에 키가 있어도** 각각 무작위
  파티션 배정과 스티키 무작위 파티션 배정을 한다 (3장, p.69).[^shapira2021]
- 쓸모가 생기는 상황: **키가 소비하는 애플리케이션에는 중요하지만 워크로드가
  치우칠 때**다 — 카프카 레코드의 키를 관계형 데이터베이스 적재의 기본 키로 쓰는 ETL
  애플리케이션이 그 예이며, 이때 **키 하나가 불균형하게 큰 워크로드를 가질 수 있다.**
  `UniformStickyPartitioner`를 쓰면 **모든 파티션에 워크로드가 고르게 분산된다** (3장,
  p.69).[^shapira2021]

## 파티션 수가 변하면 대응이 깨진다

- 기본 파티셔너를 쓸 때 **키와 파티션의 대응은 토픽의 파티션 수가 변하지 않는 한에서만
  일관적이다** (3장, p.69).[^shapira2021]
- 파티션 수가 일정한 동안에는 예컨대 **사용자 045189에 관한 레코드가 항상 파티션 34에
  쓰인다**고 확신할 수 있고, 파티션에서 데이터를 읽을 때 온갖 최적화가 가능해진다 (3장,
  p.69).[^shapira2021]
- 그러나 **토픽에 새 파티션을 추가하는 순간 이 보장은 사라진다** — 옛 레코드는 파티션
  34에 남아 있는데 새 레코드는 다른 파티션에 쓰일 수 있다 (3장, p.69).[^shapira2021]
- 그래서 **키에 의한 파티셔닝이 중요하다면 가장 쉬운 해법은 충분한 파티션으로 토픽을
  만들고 절대 파티션을 추가하지 않는 것**이다 (3장, p.69).[^shapira2021]

## 커스텀 파티셔너

- 카프카는 해시 파티셔닝만 강제하지 않으며, **데이터를 다르게 파티셔닝할 좋은 이유가
  있을 때**가 있다 (3장, p.70).[^shapira2021]
- 책이 드는 상황: B2B 벤더이고 **최대 고객사 하나가 일일 거래의 10% 이상**을 차지할 때,
  기본 해시 파티셔닝을 쓰면 **그 고객의 레코드가 다른 계정들과 같은 파티션에 배정돼 한
  파티션만 훨씬 커진다.** 서버 공간이 고갈되고 처리가 느려질 수 있으므로, **그 고객에게
  전용 파티션 하나를 주고 나머지 계정은 해시 파티셔닝으로 나머지 파티션에 대응**시키는
  것이 목표가 된다 (3장, p.70).[^shapira2021]
- 구현의 요건: `Partitioner` 인터페이스는 `configure`·`partition`·`close` 메서드를
  포함한다. 아래 예제는 `partition`만 구현하지만, **특별 취급할 고객 이름은
  `partition`에 하드코딩하지 말고 `configure`를 통해 넘겼어야 한다** (3장,
  p.70).[^shapira2021]

  아래가 그 커스텀 파티셔너다 — `Partitioner`·`partition(`으로 찾는다.

  ```java
  public class BananaPartitioner implements Partitioner {

      public void configure(Map<String, ?> configs) {}

      public int partition(String topic, Object key, byte[] keyBytes,
                           Object value, byte[] valueBytes,
                           Cluster cluster) {
          List<PartitionInfo> partitions = cluster.partitionsForTopic(topic);
          int numPartitions = partitions.size();

          if ((keyBytes == null) || (!(key instanceOf String)))
              throw new InvalidRecordException("We expect all messages " +
                  "to have customer name as key");

          if (((String) key).equals("Banana"))
              return numPartitions - 1; // Banana will always go to last partition

          // Other records will get hashed to the rest of the partitions
          return Math.abs(Utils.murmur2(keyBytes)) % (numPartitions - 1);
      }

      public void close() {}
  }
  ```

- 예제가 던지는 예외의 조건도 규칙의 일부다 — **키가 `String`이 아닌 경우를 예외로
  막는다** (3장, p.71).[^shapira2021]

## 이어지는 페이지

- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — 파티셔너가 놓인
  경로상의 자리
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 배분의 대상이 되는 단위와
  파티션 수를 늘리기만 할 수 있는 성질
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 키가 파티션 배분 말고 또
  중요해지는 자리
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 파티션 수를 미리
  충분히 잡는 판단의 기준
- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 파티셔너와 키의 개요

[^shapira2021]: Shapira et al. 2021, 3장 "Kafka Producers: Writing Messages to Kafka" — 코드 펜스는 p.70 예제에서 `import` 문과 원문의 주석 번호 표식을 덜어냈다(보탠 줄 없음). 원문의 `instanceOf` 표기(자바 키워드는 `instanceof`)는 고치지 않고 그대로 두었다

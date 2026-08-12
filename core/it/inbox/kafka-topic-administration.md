---
type: concept
title: 토픽 관리
description: AdminClient로 토픽을 다루는 네 가지 작업 — 목록 조회가 얇은 Future 래퍼인 점, 목록에서 찾는 대신 describe로 존재와 파티션 수를 함께 확인하는 이유, 없을 때 그 자리에서 만드는 관용 형태와 그때 잡는 예외, 그리고 삭제에 휴지통이 없다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T15:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 토픽 관리

- [토픽 목록 보기](#토픽-목록-보기)
- [있으면 두고 없으면 만들기](#있으면-두고-없으면-만들기)
- [삭제는 되돌릴 수 없다](#삭제는-되돌릴-수-없다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애플리케이션 코드에서 토픽의 존재와 형태를 확인하고, 없으면 만들고, 지우는
일은 어떤 형태로 이뤄지는가.**

> **버전 조건**: Kafka 0.11 이상. 이 페이지의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021]

## 토픽 목록 보기

- **카프카 AdminClient의 가장 흔한 유스케이스는 토픽 관리**이고, 여기에는 **토픽 목록 조회,
  설명, 생성, 삭제**가 들어간다 (5장, p.118).[^shapira2021]
- 목록은 `admin.listTopics()` 한 줄이다 — **이 메서드는 `ListTopicsResult` 객체를 리턴하고,
  이 객체는 `Future` 모음을 감싸는 얇은 래퍼(thin wrapper)** 다. **`topics.names()`는 이름
  집합의 `Future`를 리턴**한다 (5장, p.118).[^shapira2021]
- **이 `Future`에 `get()`을 부르면 실행 중인 스레드는 서버가 토픽 이름 집합으로 응답할
  때까지, 또는 타임아웃 예외가 날 때까지 기다린다. 목록을 받고 나면 순회하며 모든 토픽 이름을
  출력**할 수 있다 (5장, p.118).[^shapira2021] `get()`이 던지는 예외가 왜 항상
  `ExecutionException`인지는
  [어드민 클라이언트](../concepts/kafka-adminclient.md)에 있다.

## 있으면 두고 없으면 만들기

- **특정 토픽이 있는지 확인하는 한 가지 방법은 전체 토픽 목록을 가져와 그 안에 있는지 보는
  것이지만, 큰 클러스터에서는 비효율적일 수 있다** (5장, p.118).[^shapira2021]
- **게다가 토픽이 있는지만이 아니라 파티션과 레플리카 수가 맞는지까지 확인하고 싶을 때가
  있다** (5장, p.118).[^shapira2021]
  - 책이 드는 실물 예 — **카프카 커넥트와 컨플루언트 스키마 레지스트리는 설정을 저장하는 데
    카프카 토픽을 쓴다. 이들은 시작할 때 설정 토픽이 존재하는지, 설정 변경이 엄격한 순서로
    도착하도록 파티션이 하나뿐인지, 가용성을 보장하도록 레플리카가 셋인지, 그리고 옛 설정이
    무기한 보존되도록 토픽이 압착(compacted)돼 있는지를 확인한다** (5장,
    p.118).[^shapira2021] 압착이 왜 무기한 보존을 만드는지는
    [카프카 로그 압착](../concepts/kafka-log-compaction.md)에, 파티션 하나가 왜 순서를
    보장하는지는 [토픽과 파티션](../concepts/topics-and-partitions.md)에 있다.
- 관용 형태는 **설명해 보고, 없다는 예외가 오면 그 자리에서 만드는 것**이다.
  `describeTopics`·`createTopics`·`UnknownTopicOrPartitionException`으로 찾는다 (5장,
  pp.118–119):[^shapira2021]

  ```java
  DescribeTopicsResult demoTopic = admin.describeTopics(TOPIC_LIST);

  try {
      topicDescription = demoTopic.values().get(TOPIC_NAME).get();
      System.out.println("Description of demo topic:" + topicDescription);

      if (topicDescription.partitions().size() != NUM_PARTITIONS) {
        System.out.println("Topic has wrong number of partitions. Exiting.");
        System.exit(-1);
      }
  } catch (ExecutionException e) {
      // exit early for almost all exceptions
      if (! (e.getCause() instanceof UnknownTopicOrPartitionException)) {
          e.printStackTrace();
          throw e;
      }

      // if we are here, topic doesn't exist
      System.out.println("Topic " + TOPIC_NAME +
          " does not exist. Going to create it now");
      // Note that number of partitions and replicas is optional. If they are
      // not specified, the defaults configured on the Kafka brokers will be used
      CreateTopicsResult newTopic = admin.createTopics(Collections.singletonList(
              new NewTopic(TOPIC_NAME, NUM_PARTITIONS, REP_FACTOR)));

      // Check that the topic was created correctly:
      if (newTopic.numPartitions(TOPIC_NAME).get() != NUM_PARTITIONS) {
          System.out.println("Topic has wrong number of partitions.");
          System.exit(-1);
      }
  }
  ```

- 이 예제의 각 지점이 하는 일 (5장, pp.119–120):[^shapira2021]
  - **토픽이 올바른 설정으로 존재하는지 확인하기 위해 검증하려는 토픽 이름 목록으로
    `describeTopics`를 부른다. 이것은 토픽 이름을 `Future` 설명으로 매핑하는 맵을 감싼
    `DescribeTopicResult` 객체를 리턴**한다.
  - **`get()`으로 `Future`가 완료되기를 기다리면 원하는 결과, 이 경우 `TopicDescription`을
    얻는다.** 다만 **서버가 요청을 올바르게 완료하지 못할 가능성도 있다 — 토픽이 존재하지
    않으면 서버는 설명으로 응답할 수 없다. 이때 서버는 에러를 돌려보내고 `Future`는
    `ExecutionException`을 던지며 완료된다. 서버가 보낸 실제 에러가 그 예외의 cause다.**
    **토픽이 없는 경우를 처리하고 싶으므로 이 예외들을 처리**한다.
  - **토픽이 존재하면 `Future`는 `TopicDescription`을 리턴하며 완료된다. 이 객체는 토픽의 모든
    파티션 목록을 담고, 파티션마다 어느 브로커가 리더인지, 레플리카 목록, 인-싱크 레플리카
    목록을 담는다. 토픽의 설정은 여기 포함되지 않는다** — 설정은
    [설정 관리](../concepts/kafka-config-administration.md) 쪽이다.
  - **모든 AdminClient 결과 객체는 카프카가 에러로 응답할 때 `ExecutionException`을 던진다.
    AdminClient 결과가 `Future`로 감싸이고 그 `Future`가 예외를 감싸기 때문이며, 카프카가
    리턴한 에러를 얻으려면 항상 `ExecutionException`의 cause를 살펴야** 한다.
  - **토픽이 없으면 새로 만든다. 토픽을 만들 때 이름만 지정하고 나머지 세부는 기본값을 쓸 수도
    있고, 파티션 수·레플리카 수·설정을 지정할 수도** 있다. 그 기본값이 어디서 오는지는
    [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)에 있다.
  - **끝으로 토픽 생성이 리턴되기를 기다리고 결과를 검증할 수 있다.** 예제는 파티션 수를
    확인하는데, **토픽을 만들 때 파티션 수를 직접 지정했으므로 맞을 것이 꽤 확실하다. 결과
    확인은 토픽을 만들 때 브로커 기본값에 의존했을 때 더 흔하다.** 그리고 **여기서도
    `CreateTopic`의 결과를 확인하기 위해 `get()`을 부르므로 이 메서드가 예외를 던질 수 있다 —
    이 시나리오에서는 `TopicExistsException`이 흔하며, (아마 토픽을 설명해 올바른 설정인지
    확인하는 방식으로) 처리하고 싶을 것**이다.

## 삭제는 되돌릴 수 없다

- 삭제는 **삭제할 토픽 이름 목록으로 `deleteTopics` 메서드를 부르고 `get()`으로 완료를
  기다리는 것**이 전부다 (5장, p.120).[^shapira2021]
- **삭제가 비동기라는 성질 때문에 삭제 호출 직후 시점에는 토픽이 아직 존재할 수 있다** (5장,
  p.120).[^shapira2021] 왜 그런지는
  [어드민 클라이언트](../concepts/kafka-adminclient.md)의 최종적 일관성 절에 있다.
- 코드가 단순한 것과 결과가 가벼운 것은 다르다 — 책이 경고 상자로 따로 남긴 말 (5장,
  p.120):[^shapira2021]

  > Although the code is simple, please remember that in Kafka, deletion of topics is
  > final—there is no recycle bin or trash can to help you rescue the deleted topic, and no
  > checks to validate that the topic is empty and that you really mean to delete it.
  > Deleting the wrong topic could mean unrecoverable loss of data, so handle this method
  > with extra care.

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [설정 관리](../concepts/kafka-config-administration.md) — 토픽 설명에 빠져 있는 설정을 읽고
  바꾸는 쪽
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 이미
  있는 토픽의 파티션을 늘리는 쪽
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 토픽 생성 시 생략한
  값들의 출처
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 파티션 수가 무엇을 결정하는지
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 설정 토픽이 압착돼 있어야 하는 이유

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically" — 인용 블록은 p.120 경고 상자 원문. 코드 펜스는 pp.118–119 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

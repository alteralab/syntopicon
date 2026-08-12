---
type: concept
title: 토픽 관리
description: 토픽을 다루는 네 가지 작업을 코드와 명령줄 양쪽에서 — 목록 조회가 얇은 Future 래퍼인 점, 목록에서 찾는 대신 describe로 존재와 파티션 수를 함께 확인하는 이유, 없을 때 그 자리에서 만드는 관용 형태와 그때 잡는 예외, kafka-topics.sh의 필수 인자와 이름 짓기 관례, 문제 있는 파티션을 골라내는 describe 필터들, 그리고 삭제에 휴지통이 없다는 것
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 토픽 관리

- [토픽 목록 보기](#토픽-목록-보기)
- [있으면 두고 없으면 만들기](#있으면-두고-없으면-만들기)
- [삭제는 되돌릴 수 없다](#삭제는-되돌릴-수-없다)
- [명령줄에서 토픽 만들기](#명령줄에서-토픽-만들기)
- [토픽 이름 짓기](#토픽-이름-짓기)
- [명령줄에서 목록과 상세 보기](#명령줄에서-목록과-상세-보기)
- [문제 있는 파티션 찾아내기](#문제-있는-파티션-찾아내기)
- [명령줄에서 토픽 지우기](#명령줄에서-토픽-지우기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **토픽의 존재와 형태를 확인하고, 없으면 만들고, 지우는 일을 애플리케이션
코드에서와 명령줄에서 각각 어떻게 하는가.**

> **버전 조건**: Kafka 0.11 이상 — **아래 세 절(API)** 의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021] 이어지는 명령줄 절의 `kafka-topics.sh`에는 이 조건이
> 걸리지 않는다 — 그쪽은 AdminClient보다 오래된 도구다.

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

## 명령줄에서 토픽 만들기

- 같은 작업의 명령줄 쪽 도구는 하나다 — **`kafka-topics.sh` 도구가 대부분의 토픽 작업에 쉽게
  접근하게 해 주며, 클러스터의 토픽을 생성·수정·삭제하고 정보를 조회하게 해 준다** (12장,
  p.305).[^shapira2021] 이 도구를 쓰기 전에 확인할 것들은
  [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md)에 있다.
- 다만 설정은 이 도구로 하지 않는다 — **이 명령으로 일부 토픽 설정이 가능하기는 하지만 그
  기능은 지원 중단(deprecated)됐고, 설정 변경에는 더 견고한 방법인 설정 도구를 쓸 것을
  권장**한다 (12장, pp.305–306).[^shapira2021] 그쪽은
  [설정 관리](../concepts/kafka-config-administration.md)다.
  - 원문 오식: 이 문장에서 권장하는 도구 이름이 `kafka-config.sh`로 인쇄돼 있다 (12장,
    p.306).[^shapira2021] 같은 장 p.315는 같은 도구를 `kafka-configs.sh`(복수형)로 쓴다.
- `--create` 명령에는 **브로커 단위 기본값이 이미 설정돼 있더라도 반드시 줘야 하는 인자가
  셋** 있다 (12장, p.306):[^shapira2021]
  - `--topic` — **만들려는 토픽의 이름.**
  - `--replication-factor` — **클러스터 안에서 유지할 토픽의 레플리카 수.**
  - `--partitions` — **토픽에 만들 파티션 수.**
  - **`--config` 옵션으로 추가 인자와 설정 재정의를 이 시점에 줄 수도** 있다 (12장, p.306).
- 레플리카 배치는 클러스터가 정한다 — **각 파티션에 대해 클러스터가 지정된 수의 레플리카를
  적절히 고른다. 클러스터에 랙 인식(rack-aware) 레플리카 할당이 설정돼 있으면 각 파티션의
  레플리카는 서로 다른 랙에 놓이며, 그것을 원하지 않으면 `--disable-rack-aware`를 준다**
  (12장, p.307).[^shapira2021] 랙 인식 할당의 규칙은
  [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
- 자동화에서 쓸 인자가 하나 있고, 짝처럼 보이는 다른 하나는 쓰지 말라고 한다 (12장,
  p.307):[^shapira2021]
  - **`kafka-topics.sh`를 자동화에 쓸 때는 토픽이 이미 있어도 에러를 리턴하지 않는
    `--if-not-exists` 인자를 쓰고 싶을 수 있다.**
  - **`--alter` 명령에는 `--if-exists` 인자가 제공되지만 그것을 쓰는 것은 권장되지 않는다. 이
    인자를 쓰면 바꾸려는 토픽이 존재하지 않을 때 명령이 에러를 리턴하지 않게 되고, 만들어져
    있어야 할 토픽이 없는 문제를 가려 버릴 수 있다.**

## 토픽 이름 짓기

- 문자 자체는 넓게 허용된다 — **토픽 이름에는 영숫자, 밑줄, 대시, 마침표를 쓸 수 있다** (12장,
  p.307).[^shapira2021]
- 그런데 마침표는 권장되지 않는다 — **카프카 내부 지표가 마침표를 밑줄로 바꾸기 때문(예:
  `topic.1`이 지표 계산에서 `topic_1`이 된다)이며, 그 결과 토픽 이름에 충돌이 생길 수
  있다** (12장, p.307).[^shapira2021]
- 밑줄 둘로 시작하는 것도 피한다 — **관례상 카프카 운영에 내부적으로 쓰는 토픽이 밑줄 둘로
  시작하는 이름을 쓰기 때문**이며(컨슈머 그룹 오프셋 저장을 추적하는 `__consumer_offsets`가
  그 예다), **혼동을 막으려면 그렇게 시작하는 이름은 쓰지 않는 것이 좋다** (12장,
  p.307).[^shapira2021] 그 내부 토픽을 실제로 열어 보는 방법은
  [콘솔 프로듀서와 콘솔 컨슈머](../concepts/kafka-console-producer-and-consumer.md)에 있다.

## 명령줄에서 목록과 상세 보기

- `--list` 명령은 **클러스터의 모든 토픽을 한 줄에 하나씩, 특정한 순서 없이** 보여 주며 **전체
  토픽 목록을 만드는 데 유용**하다 (12장, p.308).[^shapira2021]
  - 여기에는 내부 토픽 `__consumer_offsets`도 보인다 — **`--exclude-internal`과 함께 실행하면
    앞서 말한 밑줄 둘로 시작하는 토픽이 목록에서 전부 빠지며 그것이 유익할 수 있다** (12장,
    p.308).[^shapira2021]
- `--describe`는 **클러스터의 토픽 하나 이상에 대한 상세 정보를 준다. 출력에는 파티션 수, 토픽
  설정 재정의, 그리고 파티션마다의 레플리카 할당 목록이 들어가고, `--topic` 인자로 토픽 하나로
  좁힐 수 있다** (12장, p.308).[^shapira2021]
  - 출력 한 줄의 형태는 `Topic: my-topic Partition: 0 Leader: 1 Replicas: 1,0 Isr: 1,0`이고,
    머리에 `PartitionCount`·`ReplicationFactor`·`Configs`가 붙는다 (12장,
    p.308).[^shapira2021] 같은 정보를 코드로 얻는 쪽이 위의 `TopicDescription`이다.
- 필터를 붙일 때는 대상을 좁히지 않는 것이 보통이다 — **이 명령들에는 대개 `--topic` 인자를
  주지 않는데, 의도가 기준에 맞는 클러스터 안 모든 토픽·파티션을 찾는 것이기 때문**이다.
  **이 옵션들은 `--list` 명령과는 함께 동작하지 않는다** (12장, p.308).[^shapira2021]
  - `--topics-with-overrides` — **클러스터 기본값과 다른 설정을 가진 토픽만 설명한다** (12장,
    p.308).
  - `--exclude-internal` — **밑줄 둘 관례로 시작하는 토픽을 목록에서 뺀다** (12장, p.309).

## 문제 있는 파티션 찾아내기

- **다음 명령들은 문제가 있을 수 있는 토픽 파티션을 찾는 데 쓴다** (12장,
  p.309):[^shapira2021]
  - `--under-replicated-partitions` — **레플리카 하나 이상이 리더와 인-싱크가 아닌 모든
    파티션을 보여 준다. 클러스터 정비·배포·리밸런스가 불완전 복제 파티션(under-replicated
    partition, URP)을 만들기 때문에 이것이 꼭 나쁜 것은 아니지만 알고는 있어야 한다.**
  - `--at-min-isr-partitions` — **리더를 포함한 레플리카 수가 최소 인-싱크 레플리카(in-sync
    replica, ISR) 설정과 정확히 일치하는 모든 파티션을 보여 준다. 이 토픽들은 프로듀서·컨슈머
    클라이언트가 여전히 쓸 수 있지만 이중화가 사라진 상태라 사용 불가가 될 위험에 있다.**
  - `--under-min-isr-partitions` — **ISR 수가 쓰기 성공에 필요한 설정된 최솟값 아래인 모든
    파티션을 보여 준다. 이 파티션들은 사실상 읽기 전용 모드이며 생산할 수 없다.**
  - `--unavailable-partitions` — **리더가 없는 모든 토픽 파티션을 보여 준다. 이것은 심각한
    상황이며 파티션이 오프라인이고 프로듀서·컨슈머 클라이언트가 쓸 수 없음을 뜻한다.**
- 이 상태들이 각각 무엇을 의미하는지는
  [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md)과
  [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md)에, `min.insync.replicas`가
  거는 하한은 [카프카 신뢰성 보장](../concepts/kafka-reliability-guarantees.md)에 있다.

## 명령줄에서 토픽 지우기

- 지울 동기부터 — **메시지가 하나도 없는 토픽도 디스크 공간·열린 파일 핸들·메모리 같은 클러스터
  자원을 쓴다. 컨트롤러도 알고 있어야 하는 쓸모없는 메타데이터를 갖게 되는데 이것이 대규모에서
  성능을 방해할 수 있다** (12장, p.311).[^shapira2021]
- 전제 조건이 하나 있다 — **이 작업을 하려면 클러스터의 브로커들이 `delete.topic.enable`
  옵션을 `true`로 설정하고 있어야 한다. `false`면 토픽 삭제 요청은 무시되고 성공하지 않는다**
  (12장, p.311).[^shapira2021] 그 설정 자체는
  [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)에 있다.
- 삭제가 비동기라는 점은 코드 쪽과 같고, 그 결과가 운영 제약이 된다 — **명령을 실행하면 토픽이
  삭제 대상으로 표시될 뿐 데이터와 정리 양에 따라 삭제가 즉시 일어나지 않을 수 있다. 컨트롤러가
  (진행 중인 컨트롤러 작업이 끝나는 대로) 가능한 한 빨리 브로커들에 삭제 대기를 알리고, 브로커는
  그 토픽의 메타데이터를 무효화한 뒤 디스크에서 파일을 지운다** (12장, p.311).[^shapira2021]
  - 그래서 **컨트롤러가 이 작업을 실행하는 방식의 한계 때문에, 한 번에 토픽을 한두 개 넘게
    지우지 말고 다른 토픽을 지우기 전에 충분한 시간을 줄 것을 강력히 권장**한다 (12장,
    p.311).[^shapira2021] **책의 작은 클러스터 예제에서는 삭제가 거의 즉시 일어나지만 더 큰
    클러스터에서는 더 오래 걸릴 수 있다.**
- 위험 표시는 여기에도 붙는다 (12장, p.311):[^shapira2021]

  > Deleting a topic will also delete all its messages. This is not a reversible operation.
  > Make sure it is executed carefully.

- 실행은 `--delete --topic my-topic`이고, **카프카 버전에 따라 다른 설정이 없으면 이 인자가
  동작하지 않는다는 안내(`Note: This will have no impact if delete.topic.enable is not set to
  true.`)가 붙을 수 있다** (12장, p.311).[^shapira2021]
- 확인은 스스로 해야 한다 — **토픽 삭제가 성공했는지 실패했는지 보이는 피드백이 없으므로,
  `--list`나 `--describe` 옵션으로 토픽이 더 이상 클러스터에 없음을 확인해 검증**한다 (12장,
  p.312).[^shapira2021]
- 삭제 요청이 걸려서 진행되지 않는 경우의 대처는
  [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md)에 있다.

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — `kafka-topics.sh`가 속한
  도구 모음의 전제와 경고
- [설정 관리](../concepts/kafka-config-administration.md) — 토픽 설명에 빠져 있는 설정을 읽고
  바꾸는 쪽
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 이미
  있는 토픽의 파티션을 늘리는 쪽(코드와 명령줄 둘 다)
- [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md) — 삭제가 걸려 버렸을 때와
  삭제가 꺼진 클러스터에서
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 토픽 생성 시 생략한
  값들의 출처이자 `delete.topic.enable`이 사는 곳
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 파티션 수가 무엇을 결정하는지
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 설정 토픽이 압착돼 있어야 하는 이유

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(pp.118–120)와 12장 "Administering Kafka"(pp.305–312) — 인용 블록은 p.120·p.311 경고 상자 원문. 코드 펜스는 pp.118–119 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

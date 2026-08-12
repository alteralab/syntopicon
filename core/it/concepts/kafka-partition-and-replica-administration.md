---
type: concept
title: 파티션과 레플리카 관리
description: 인시던트 때 쓰는 위험한 어드민 작업 넷 — 파티션 추가가 키 기반 순서 가정을 깨뜨리는 지점과 증가분이 아니라 총수를 받는 인자, 보존 정책이 법적 준수를 보장하지 못해 필요해진 레코드 삭제, 선호 리더와 언클린 리더 선출을 같은 메서드로 강제하는 법, 그리고 레플리카 배치를 손으로 정하고 진행 중인 재할당을 취소하는 법
generated: { by: "claude-opus-5", at: "2026-08-12T15:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 파티션과 레플리카 관리

- [왜 한 묶음으로 다루는가](#왜-한-묶음으로-다루는가)
- [파티션 추가](#파티션-추가)
- [레코드 삭제](#레코드-삭제)
- [리더 선출](#리더-선출)
- [레플리카 재할당](#레플리카-재할당)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **돌아가는 클러스터의 파티션·레코드·리더·레플리카를 손으로 옮겨야 할 때 무엇을
부르고, 각각이 무엇을 깨뜨릴 수 있는가.**

> **버전 조건**: Kafka 0.11 이상. 이 페이지의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021]

## 왜 한 묶음으로 다루는가

- 책은 이 절을 이렇게 연다 (5장, p.127):[^shapira2021]

  > In this section, we'll discuss a few methods that are rarely used, and can be risky to
  > use, but are incredibly useful when needed. Those are mostly important for SREs during
  > incidents—but don't wait until you are in an incident to learn how to use them. Read and
  > practice before it is too late. Note that the methods here have little to do with one
  > another, except that they all fit into this category.

## 파티션 추가

- **보통 토픽의 파티션 수는 토픽이 생성될 때 정해진다. 파티션 하나가 매우 높은 처리량을 낼 수
  있으므로 토픽의 용량 한계에 부딪히는 일은 드물다** (5장, p.127).[^shapira2021] 그 수를
  처음에 정하는 기준은
  [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)에 있다.
- **게다가 토픽의 메시지에 키가 있다면 컨슈머는 같은 키의 모든 메시지가 항상 같은 파티션으로
  가고 같은 컨슈머가 같은 순서로 처리한다고 가정할 수 있다** (5장, p.127).[^shapira2021]
  그 가정의 근거와 그것이 깨지는 방식은
  [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md)에 있다.
- **이런 이유로 토픽에 파티션을 추가하는 일은 거의 필요하지 않고 위험할 수 있다. 그 작업이
  토픽을 소비하는 어떤 애플리케이션도 망가뜨리지 않는지 확인해야** 한다 (5장,
  p.127).[^shapira2021]
- **그럼에도 기존 파티션으로 처리할 수 있는 처리량의 천장에 정말로 부딪혀 파티션을 추가하는 것
  말고 선택지가 없을 때가 있다** (5장, p.127).[^shapira2021]
- **토픽 모음에 파티션을 추가하는 데는 `createPartitions` 메서드를 쓴다. 여러 토픽을 한 번에
  확장하려 하면 일부는 성공하고 나머지는 실패할 수 있다는 점에 유의**한다 (5장,
  p.127).[^shapira2021]
- 인자의 의미가 함정이다 — **토픽을 확장할 때는 추가될 새 파티션의 개수가 아니라 파티션이
  추가된 뒤 토픽이 갖게 될 전체 파티션 수를 지정해야** 한다. 예제는
  `NewPartitions.increaseTo(NUM_PARTITIONS+2)`를 쓴다 (5장, pp.127–128).[^shapira2021]
  - **그래서 확장 전에 토픽을 설명해 파티션이 몇 개 있는지 알아내야 할 수 있다**고 책이 따로
    적어 뒀다 (5장, p.128).[^shapira2021] 설명하는 방법은
    [토픽 관리](../concepts/kafka-topic-administration.md)에 있다.

## 레코드 삭제

- 동기는 법이다 — **현행 개인정보 보호법들은 데이터에 대해 특정한 보존 정책을 강제한다.
  불행히도 카프카에 토픽 보존 정책이 있기는 하지만 법적 준수를 보장하는 방식으로 구현되지는
  않았다. 보존 정책이 30일인 토픽이라도 파티션마다 모든 데이터가 세그먼트 하나에 들어간다면
  더 오래된 데이터를 저장하고 있을 수 있다** (5장, p.128).[^shapira2021] 세그먼트가 보존을
  어떻게 지연시키는지는
  [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
- **`deleteRecords` 메서드는 호출 시 지정한 오프셋보다 오래된 모든 레코드를 삭제된 것으로
  표시해 카프카 컨슈머가 접근할 수 없게 만든다. 이 메서드는 삭제된 가장 높은 오프셋들을
  리턴하므로 삭제가 기대대로 일어났는지 확인할 수 있다. 디스크에서의 완전한 정리는 비동기로
  일어난다** (5장, p.128).[^shapira2021]
- **`listOffsets` 메서드로 특정 시각에 또는 그 직후에 쓰인 레코드의 오프셋을 얻을 수 있음을
  기억하면, 두 메서드를 함께 써서 특정 시점보다 오래된 레코드를 지울 수 있다** — 얻은
  오프셋을 `RecordsToDelete.beforeOffset`으로 감싸 `deleteRecords`에 넘긴다 (5장,
  p.128).[^shapira2021]

## 리더 선출

- **`electLeaders()` 메서드는 두 가지 서로 다른 유형의 리더 선출을 촉발한다** (5장,
  p.128).[^shapira2021]
- **선호 리더 선출(preferred leader election)** — **파티션마다 선호 리더로 지정된 레플리카가
  하나 있다. 선호되는 이유는 모든 파티션이 자기 선호 리더 레플리카를 리더로 쓰면 브로커별
  리더 개수가 균형을 이루기 때문**이다. **기본적으로 카프카는 5분마다 선호 리더 레플리카가
  실제로 리더인지 확인하고, 아니지만 리더가 될 자격이 있으면 그것을 리더로 선출한다.**
  **`auto.leader.rebalance.enable`이 `false`이거나 이 일이 더 빨리 일어나기를 원하면
  `electLeader()` 메서드로 이 과정을 촉발할 수 있다** (5장, p.128).[^shapira2021] 선호 리더의
  정의와 자동 리밸런스는
  [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md)에 있다.
- **언클린 리더 선출(unclean leader election)** — **파티션의 리더 레플리카를 쓸 수 없게 되고
  다른 레플리카들은 (보통 데이터가 없어서) 리더가 될 자격이 없으면, 파티션은 리더가 없어져
  사용 불가가 된다. 이를 푸는 한 방법이 언클린 리더 선출을 촉발하는 것, 즉 리더가 될 자격이
  없는 레플리카를 그럼에도 리더로 선출하는 것**이다. **이것은 데이터 유실을 일으킨다 — 옛
  리더에 쓰였지만 새 리더로 복제되지 않은 모든 이벤트가 유실된다. `electLeader()` 메서드는
  언클린 리더 선출을 촉발하는 데도 쓸 수 있다** (5장, p.129).[^shapira2021] 그 유실이
  무엇과 맞바꾸는 것인지는
  [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md)에 있다.
- 비동기라는 점이 관측을 흐린다 — **이 메서드는 비동기이므로 성공적으로 리턴한 뒤에도 모든
  브로커가 새 상태를 알게 되기까지는 시간이 걸리고, 그동안 `describeTopics()` 호출은 일관되지
  않은 결과를 리턴할 수 있다. 여러 파티션에 대해 리더 선출을 촉발하면 일부는 성공하고 일부는
  실패할 수 있다** (5장, p.129).[^shapira2021]
- 호출 형태와 결과 해석 (5장, p.129):[^shapira2021]
  - `admin.electLeaders(ElectionType.PREFERRED, electableTopics)`는 **특정 토픽의 파티션
    하나에 대해 선호 리더를 선출한다. 지정할 수 있는 파티션과 토픽의 수에는 제한이 없다.**
    **파티션 모음 대신 `null`로 명령을 부르면 고른 선출 유형을 모든 파티션에 대해 촉발한다.**
  - **클러스터 상태가 건강하면 이 명령은 아무 일도 하지 않는다** — 그때는
    `ElectionNotNeededException`이 온다. **선호 리더 선출과 언클린 리더 선출은 선호 리더가
    아닌 레플리카가 현재 리더일 때만 효력을 갖기 때문**이다.

## 레플리카 재할당

- 동기는 넷이다 — **어떤 레플리카의 현재 위치가 마음에 들지 않을 때다. 브로커에 부하가 걸려
  일부 레플리카를 옮기고 싶을 수도, 레플리카를 더 추가하고 싶을 수도, 장비를 빼기 위해 한
  브로커의 모든 레플리카를 옮기고 싶을 수도, 몇몇 토픽이 너무 시끄러워 나머지 워크로드에서
  격리해야 할 수도** 있다. **이 모든 시나리오에서 `alterPartitionReassignments`가 파티션의
  레플리카 하나하나의 배치에 대한 세밀한 제어를 준다** (5장, p.129).[^shapira2021]
- 비용을 먼저 본다 — **레플리카를 한 브로커에서 다른 브로커로 재할당하는 일은 브로커 사이에
  대량의 데이터를 복사하는 것을 수반할 수 있음을 명심하라. 가용 네트워크 대역폭에 유의하고,
  필요하면 쿼터로 복제를 스로틀링하라. 쿼터는 브로커 설정이므로 AdminClient로 설명하고 갱신할
  수 있다** (5장, pp.129–130).[^shapira2021] 쿼터 자체는
  [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md)에, 그것을 바꾸는 통로는
  [설정 관리](../concepts/kafka-config-administration.md)에 있다.
- 아래는 **ID 0인 브로커 하나에 토픽의 모든 파티션이 레플리카 하나씩 올라가 있고, 새 브로커를
  추가한 뒤 그 브로커에 레플리카 일부를 두려는 예**이며, `alterPartitionReassignments`·
  `NewPartitionReassignment`·`listPartitionReassignments`로 찾는다 (5장,
  p.130):[^shapira2021]

  ```java
  Map<TopicPartition, Optional<NewPartitionReassignment>> reassignment = new HashMap<>();
  reassignment.put(new TopicPartition(TOPIC_NAME, 0),
          Optional.of(new NewPartitionReassignment(Arrays.asList(0,1))));
  reassignment.put(new TopicPartition(TOPIC_NAME, 1),
          Optional.of(new NewPartitionReassignment(Arrays.asList(1))));
  reassignment.put(new TopicPartition(TOPIC_NAME, 2),
          Optional.of(new NewPartitionReassignment(Arrays.asList(1,0))));
  reassignment.put(new TopicPartition(TOPIC_NAME, 3), Optional.empty());

  admin.alterPartitionReassignments(reassignment).all().get();

  System.out.println("currently reassigning: " +
          admin.listPartitionReassignments().reassignments().get());
  demoTopic = admin.describeTopics(TOPIC_LIST);
  topicDescription = demoTopic.values().get(TOPIC_NAME).get();
  System.out.println("Description of demo topic:" + topicDescription);
  ```

- 각 줄이 하는 일 (5장, p.130):[^shapira2021]
  - **파티션 0에는 레플리카를 하나 더 추가해 새 레플리카를 ID 1인 새 브로커에 두되 리더는
    바꾸지 않았다.**
  - **파티션 1에는 레플리카를 추가하지 않고, 있던 레플리카 하나를 새 브로커로 옮기기만 했다.
    레플리카가 하나뿐이므로 그것이 곧 리더다.**
  - **파티션 2에는 레플리카를 하나 더 추가하고 그것을 선호 리더로 만들었다. 다음 선호 리더
    선출이 리더십을 새 브로커의 새 레플리카로 옮기고, 기존 레플리카는 팔로워가 된다.**
  - **파티션 3에는 진행 중인 재할당이 없다. 만약 있었다면 이 호출이 그것을 취소하고 상태를
    재할당 작업이 시작되기 전으로 되돌렸을 것이다.**
  - **진행 중인 재할당은 `listPartitionReassignments`로 나열할 수 있다.**
  - **새 상태를 출력할 수도 있지만, 일관된 결과를 보이기까지 시간이 걸릴 수 있음을 기억**한다.

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 선호 리더와 인-싱크
  판정이 정의되는 곳
- [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md) — 여기서 손으로 촉발하는
  그 선출이 무엇을 맞바꾸는지
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 파티션 추가가 깨뜨리는
  키 기반 가정
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 파티션이 확장과 복제의 단위인 이유
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 세그먼트가 보존 정책을
  미루는 곳
- [설정 관리](../concepts/kafka-config-administration.md) — 복제 스로틀링에 쓰는 쿼터를 바꾸는
  통로

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically" — 인용 블록은 p.127 원문. 코드 펜스는 p.130 예제에서 원문의 주석 번호 표식을 덜어내고 지면에서 하이픈으로 끊긴 식별자를 이었다(보탠 줄 없음)

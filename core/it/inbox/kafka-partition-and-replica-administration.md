---
type: concept
title: 파티션과 레플리카 관리
description: 인시던트 때 쓰는 위험한 작업들을 코드와 명령줄 양쪽에서 — 파티션 추가가 키 기반 순서 가정을 깨뜨리는 지점과 증가분이 아니라 총수를 받는 인자, 파티션을 줄일 수 없는 이유, 보존 정책이 법적 준수를 보장하지 못해 필요해진 레코드 삭제, 선호 리더와 언클린 리더 선출을 촉발하는 법, 레플리카 배치를 손으로 정하는 3단계 재할당과 스로틀링, 복제 팩터 변경, 그리고 재할당 취소가 남기는 상태
generated: { by: "claude-opus-5", at: "2026-08-13T17:00:00Z" }
status: draft
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 파티션과 레플리카 관리

- [왜 한 묶음으로 다루는가](#왜-한-묶음으로-다루는가)
- [파티션 추가](#파티션-추가)
- [레코드 삭제](#레코드-삭제)
- [리더 선출](#리더-선출)
- [레플리카 재할당](#레플리카-재할당)
- [명령줄에서 파티션 늘리기](#명령줄에서-파티션-늘리기)
- [파티션은 줄일 수 없다](#파티션은-줄일-수-없다)
- [명령줄에서 리더 선출](#명령줄에서-리더-선출)
- [명령줄에서 레플리카 재할당](#명령줄에서-레플리카-재할당)
- [재할당의 부담을 줄이는 법](#재할당의-부담을-줄이는-법)
- [복제 팩터 바꾸기](#복제-팩터-바꾸기)
- [재할당 취소하기](#재할당-취소하기)
- [손으로 하는 것의 값어치](#손으로-하는-것의-값어치)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **돌아가는 클러스터의 파티션·레코드·리더·레플리카를 손으로 옮겨야 할 때 코드와
명령줄에서 각각 무엇을 부르고, 각각이 무엇을 깨뜨릴 수 있는가.**

> **버전 조건**: Kafka 0.11 이상 — **아래 API 절들**의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021] 명령줄 절의 도구들에는 이 조건이 걸리지 않는다.

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

- **`electLeaders()` 메서드는 두 가지 서로 다른 유형의 리더 선출(leader election)을 촉발한다** (5장,
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
- 비용을 먼저 본다 — **레플리카를 한 브로커에서 다른 브로커로 재할당(reassignment)하는 일은
  브로커 사이에 대량의 데이터를 복사하는 것을 수반할 수 있음을 명심하라. 가용 네트워크
  대역폭에 유의하고, 필요하면 쿼터로 복제를 스로틀링(throttling)하라. 쿼터는 브로커 설정이므로 AdminClient로 설명하고 갱신할
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

## 명령줄에서 파티션 늘리기

- 명령줄 쪽에서 파티션 추가는 토픽 도구가 맡는다 — **`kafka-topics.sh`의 `--alter` 명령에
  `--topic`과 `--partitions`를 주며**, 책의 예는 `my-topic`을 16개로 늘린 뒤 `--describe`로
  확인한다 (12장, p.310).[^shapira2021] 여기서도 **인자는 총수**다. 이 도구를 쓰기 전에 확인할
  것은 [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md)에 있다.
- 늘리는 이유를 12장은 둘로 정리한다 (12장, p.310):[^shapira2021]
  - **가장 흔한 이유는 단일 파티션의 처리량을 낮춤으로써 토픽을 더 많은 브로커에 걸쳐 수평
    확장하는 것.**
  - **파티션은 그룹의 단일 멤버만 소비할 수 있으므로, 컨슈머가 한 컨슈머 그룹 안에서 복제본을
    더 많이 돌리도록 확장해야 할 때도 늘린다.** 그 제약은
    [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md)에 있다.
- 키 있는 토픽에 대한 경고는 12장이 상자로 따로 남겼다 — **컨슈머 관점에서 키 있는 메시지로
  생산되는 토픽에 파티션을 추가하는 것은 매우 어려울 수 있는데, 파티션 수가 바뀌면 키에서
  파티션으로 가는 매핑이 바뀌기 때문이다. 그래서 키 있는 메시지를 담을 토픽의 파티션 수는
  토픽을 만들 때 한 번 정하고 크기 조정을 피하는 것이 바람직하다** (12장,
  p.310).[^shapira2021]

## 파티션은 줄일 수 없다

- **토픽의 파티션 수를 줄이는 것은 불가능하다.** 이유는 둘이다 — **토픽에서 파티션을 지우면 그
  토픽 데이터의 일부도 함께 지워지는데 이는 클라이언트 관점에서 일관되지 않고, 남은 파티션으로
  데이터를 재분배하려는 시도는 어려울뿐더러 메시지 순서가 어긋나게 된다** (12장,
  p.311).[^shapira2021]
- 그래도 줄여야 한다면 — **토픽을 지우고 다시 만들거나, (삭제가 불가능하면) 기존 토픽의 새
  버전을 만들어 모든 생산 트래픽을 새 토픽으로 옮길 것(예: `my-topic-v2`)을 권장**한다 (12장,
  p.311).[^shapira2021]

## 명령줄에서 리더 선출

- 리더십 균형이 왜 관리 대상인지부터 — **파티션의 레플리카 중 언제나 하나만 리더일 수 있고 모든
  생산·소비 작업이 그 브로커에서 일어나므로, 어느 브로커가 어느 파티션의 리더십을 갖는지의
  균형을 유지하는 것이 전체 클러스터에 부하를 퍼뜨리는 데 필요**하다 (12장,
  p.326).[^shapira2021]
- 리더의 정의와 그것이 자동으로 되돌아오지 않는다는 점 (12장, p.326):[^shapira2021]

  > Leadership is defined within Kafka as the first in-sync replica in the replica list.
  > However, when a broker is stopped or loses connectivity to the rest of the cluster,
  > leadership is transferred to another in-sync replica, and the original does not resume
  > leadership of any partitions automatically.

  - 그 결과 **자동 리더 밸런싱이 켜져 있지 않으면 전체 클러스터에 걸친 배포 뒤 균형이 심하게
    비효율적이 될 수 있다. 그래서 이 설정을 켜 두거나 크루즈 컨트롤(Cruise Control) 같은 다른 오픈소스 도구를
    써서 좋은 균형이 상시 유지되게 할 것을 권장**한다 (12장, p.326).[^shapira2021]
- 균형이 나쁠 때 쓰는 것이 **선호 리더 선출**이다 — **가볍고 대체로 영향이 없는(nonimpacting)
  절차이며, 클러스터 컨트롤러에게 파티션의 이상적인 리더를 고르라고 알린다. 클라이언트는
  리더십 변경을 자동으로 추적하므로 리더십이 옮겨 간 새 브로커로 따라갈 수 있다** (12장,
  p.326).[^shapira2021] 그 이상적 리더가 무엇인지는 [위의 API 절](#리더-선출)과 같다.
- 도구는 `kafka-leader-election.sh`이고, 모든 토픽에 대해 거는 형태는
  `--election-type PREFERRED --all-topic-partitions`다 (12장, p.326).[^shapira2021]
  - **이 도구의 옛 버전인 `kafka-preferred-replica-election.sh`도 여전히 있지만, "preferred"와
    "unclean" 중 선출 유형을 지정하는 것 같은 더 많은 커스터마이즈를 허용하는 새 도구를 위해
    지원 중단됐다** (12장, p.326).[^shapira2021] 언클린 쪽이 무엇을 버리는지는
    [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md)에 있다.
  - 범위를 좁히려면 **`--topic`에 토픽 이름을, `--partition`에 파티션을 직접 주거나, 여러
    파티션 목록을 담은 JSON 파일을 `--path-to-json-file`로 넘긴다** (12장,
    pp.326–327).[^shapira2021] 그 JSON은 `{"partitions": [{"partition": 1, "topic":
    "my-topic"}, …]}` 꼴이다.

## 명령줄에서 레플리카 재할당

- 손으로 레플리카 배치를 바꿔야 하는 상황을 12장은 넷으로 든다 (12장, p.327):[^shapira2021]
  - **자동 리더 분산이 제대로 처리하지 못하는, 브로커 간 불균등한 부하가 있을 때.**
  - **브로커가 오프라인이 되어 파티션이 불완전 복제 상태일 때.**
  - **새 브로커를 추가해 새 파티션을 그쪽으로 더 빨리 균형 잡고 싶을 때.**
  - **토픽의 복제 팩터를 조정하고 싶을 때.**
- 도구는 `kafka-reassign-partitions.sh`이고 **여러 단계로 이뤄진다 — 먼저 브로커 목록과 토픽
  목록으로 이동 집합(move set) 제안을 생성하고, 다음 단계에서 그 제안을 실행하며, 마지막으로
  같은 도구로 재할당의 진행이나 완료를 추적·검증**한다 (12장, p.327).[^shapira2021]
- 첫 단계의 입력이 토픽 목록 JSON이다. **버전 번호는 현재 항상 1**이며, 아래가 그 형식이다.
  `topics-to-move-json-file`로 찾는다 (12장, p.328):[^shapira2021]

  ```json
  {
      "topics": [
          {
               "topic": "foo1"
          },
          {
               "topic": "foo2"
          }
      ],
      "version": 1
  }
  ```

  - 그 파일로 `--topics-to-move-json-file topics.json --broker-list 5,6 --generate`를 부르면
    **현재 할당과 제안된 재할당 설정이 함께 출력**되고, **그 둘을
    `revert-reassignment.json`과 `expand-cluster-reassignment.json` 두 파일로 저장**한다.
    **앞의 것은 롤백이 필요할 때 파티션을 원래 자리로 되돌리는 데 쓰고, 뒤의 것이 다음 단계에서
    쓸 제안**이다 (12장, p.328).[^shapira2021]
  - 제안이 완벽하지는 않다 — 예제에서 **리더십 균형이 좋지 않아 모든 리더십이 브로커 5로
    옮겨 가는데, 책은 자동 리더 밸런싱이 켜져 있다고 보고 무시**한다 (12장,
    p.328).[^shapira2021]
  - **파티션을 어디로 옮길지 정확히 알고 JSON을 손으로 만들 수 있다면 첫 단계는 건너뛸 수
    있다** (12장, p.329).[^shapira2021]
- 실행은 `--reassignment-json-file expand-cluster-reassignment.json --execute`이고, 그때
  내부에서 일어나는 일이 비용의 정체다 (12장, p.329):[^shapira2021]

  > The cluster controller performs this reassignment action by adding the new replicas to the
  > replica list for each partition, which will temporarily increase the replication factor of
  > these topics. The new replicas will then copy all existing messages for each partition from
  > the current leader. Depending on the size of the partitions on disk, this can take a
  > significant amount of time as the data is copied across the network to the new replicas.
  > Once replication is complete, the controller removes the old replicas from the replica list
  > by reducing the replication factor to the original size with the old replicas removed.

- 함께 쓸 만한 옵션 셋 (12장, pp.329–330):[^shapira2021]
  - `--additional` — **기존 재할당에 덧붙여, 원래의 이동이 끝나기를 기다리지 않고 중단 없이
    계속 수행되게 한다.**
  - `--disable-rack-aware` — **랙 인식 설정 때문에 제안의 최종 상태가 불가능할 수 있는데,
    필요하면 이 명령으로 그것을 덮어쓴다.**
  - `--throttle` — **초당 바이트 단위 값이다. 파티션 재할당은 메모리 페이지 캐시를 바꾸고
    네트워크·디스크 I/O를 쓰기 때문에 클러스터 성능에 큰 영향을 준다. 파티션 이동을
    스로틀링하면 이 문제를 막을 수 있고, `--additional` 태그와 조합해 이미 시작돼 문제를
    일으키고 있는 재할당 과정에 스로틀을 걸 수도 있다.**
- 진행 확인은 `--verify`이며 **어느 재할당이 진행 중이고 완료됐고 (에러가 있었다면) 실패했는지
  보여 준다. 이를 위해 실행 단계에서 쓴 JSON 객체 파일이 있어야** 한다 (12장,
  p.330).[^shapira2021] 출력은
  `Reassignment of partition [foo1,0] completed successfully` 꼴이다 (12장, p.331).

## 재할당의 부담을 줄이는 법

- 브로커 하나에서 파티션을 대량으로 걷어낼 때 쓰는 요령을 책이 상자로 남겼다 — **브로커를
  클러스터에서 빼는 경우처럼 한 브로커에서 파티션을 많이 제거할 때는 먼저 그 브로커에서 모든
  리더십을 걷어내는 것이 유용할 수 있다. 앞의 도구로 손수 하는 것은 고된 일이고, 크루즈 컨트롤
  같은 오픈소스 도구에는 브로커에서 리더십을 안전하게 걷어내는 브로커 격하(broker demotion)
  기능이 있어 아마 가장 단순한 방법**이다 (12장, p.330).[^shapira2021]
- 도구가 없으면 재시작으로 대신한다 — **브로커를 그냥 재시작하는 것으로 충분하다. 브로커가
  셧다운을 준비하면서 그 브로커의 모든 파티션 리더십이 클러스터의 다른 브로커로 옮겨 가기
  때문이다. 이것은 복제 트래픽이 많은 브로커로 분산되므로 재할당 성능을 크게 올리고 클러스터에
  주는 영향을 줄인다** (12장, p.330).[^shapira2021]
  - 다만 **브로커를 튕긴 뒤 자동 리더 재할당이 켜져 있으면 리더십이 그 브로커로 되돌아올 수
    있으므로, 그 기능을 잠시 꺼 두는 것이 이로울 수 있다** (12장, p.330).[^shapira2021]

## 복제 팩터 바꾸기

- 같은 도구로 **파티션의 복제 팩터(replication factor, RF)를 올리거나 내릴 수 있다.** 필요해지는
  상황은 **파티션이 잘못된 RF로 만들어졌을 때, 클러스터를 확장하며 이중화를 늘리고 싶을 때,
  비용 절감을 위해 이중화를 줄이고 싶을 때**다 (12장, p.331).[^shapira2021]
- 대표 사례가 하나 명확하다 — **클러스터 RF 기본 설정을 조정해도 기존 토픽은 자동으로 올라가지
  않는다. 이 도구로 기존 파티션의 RF를 올린다** (12장, p.331).[^shapira2021]
- 방법은 앞의 실행 제안과 비슷한 JSON에 **레플리카 집합에 브로커 ID를 하나 더 넣는 것**이고
  (예: `[5,6]`에 브로커 4를 더해 `[5,6,4]`), 완료 뒤에는 **`--verify` 플래그나
  `kafka-topics.sh --describe`로 RF가 올라갔는지 확인**한다 (12장, p.331).[^shapira2021]

## 재할당 취소하기

- 예전 방식이 왜 위험했는지와 지금이 왜 다른지 (12장, pp.331–332):[^shapira2021]

  > Canceling a replica reassignment in the past was a dangerous process that required unsafe
  > manual manipulation of ZooKeeper nodes (or znodes) by deleting the
  > */admin/reassign_partitions* znode. Fortunately, this is no longer the case.

  - 버전 조건: z노드를 직접 지우던 그 방식이 성립하던 것은 Kafka 3.9 이하다 — 그 뒤로는 주키퍼
    자체가 없다([주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)). 그런 조작이 왜 위험한지는
    [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md)에 있다.
- 지금은 **`kafka-reassign-partitions.sh` 스크립트(그리고 그것이 감싸고 있는 AdminClient)가
  `--cancel` 옵션을 지원해 클러스터에서 진행 중인 활성 재할당을 취소**한다 (12장,
  p.332).[^shapira2021]
- 취소가 무해하지는 않다 — **진행 중인 파티션 이동을 멈출 때 `--cancel` 명령은 레플리카 집합을
  재할당이 시작되기 전 상태로 복원하도록 설계돼 있다. 그래서 죽은 브로커나 과부하 걸린
  브로커에서 레플리카를 걷어내던 중이었다면 클러스터를 바람직하지 않은 상태로 남길 수 있다.
  또한 복원된 레플리카 집합이 이전과 같은 순서일 것이라는 보장도 없다** (12장,
  p.332).[^shapira2021] 레플리카 목록의 순서가 왜 중요한지는 위의
  [선호 리더의 정의](#명령줄에서-리더-선출)에 있다.

## 손으로 하는 것의 값어치

이 페이지의 작업들은 전부 **샤드(shard)를 노드에 다시 배정하는 일**이고, 그것을 사람이 하는가
시스템이 하는가는 일반 판단의 대상이다. 카프카는 이 페이지처럼 도구를 사람 손에 쥐여 주는
쪽(그리고 크루즈 컨트롤 같은 외부 자동화)에 서 있다.

- 자세는 셋으로 갈린다 — **어떤 시스템은 언제 샤드를 쪼갤지, 언제 옮길지를 사람의 개입 없이
  자동으로 정하고, 다른 시스템은 관리자가 명시적으로 설정하게 둔다. 중간 지대도 있다 —
  Couchbase와 Riak은 제안된 샤드 배정을 자동으로 생성하되 효력을 갖기 전에 관리자가 커밋해야
  한다** (7장, p.264).[^kleppmann2026]
  - 위 [명령줄에서 레플리카 재할당](#명령줄에서-레플리카-재할당)의 `--generate` → `--execute`
    2단계가 이 중간 지대와 같은 모양이다.
- 자동이 주는 것 — **정상 유지보수의 운영 작업이 적고, 워크로드 변화에 맞춰 오토스케일까지 할
  수 있다. DynamoDB 같은 클라우드 데이터베이스는 부하가 크게 늘거나 줄 때 몇 분 안에 샤드를
  자동으로 추가·제거할 수 있다고 홍보된다** (7장, p.265).[^kleppmann2026]
- 자동이 위험해지는 자리 — **리밸런싱(rebalancing)은 요청을 다시 라우팅하고 대량의 데이터를 옮기는 비싼
  연산이라 신중히 하지 않으면 네트워크나 노드에 과부하를 주고 다른 요청의 성능을 해칠 수
  있다** (7장, p.265).[^kleppmann2026] 위 [스로틀링](#재할당의-부담을-줄이는-법)이 카프카에서
  이 위험을 다루는 손잡이다.
- 특히 위험한 조합이 하나 지목된다 — **자동 리밸런싱이 자동 장애 탐지와 결합될 때다. 노드
  하나가 과부하로 응답이 느려지면 다른 노드들이 그것을 죽었다고 결론짓고 부하를 옮기려
  리밸런싱하는데, 이는 다른 노드와 네트워크에 부하를 더해 상황을 악화시키고 연쇄 장애(cascading
  failure)를 일으킬 위험이 있다** (7장, p.265).[^kleppmann2026]
- 그래서 저자들의 판단은 이 페이지의 자세와 같다 — **리밸런싱에 사람을 끼워 두는 것이 좋을 수
  있다. 완전 자동보다 느리지만 운영상의 놀람을 예방한다. 수동 리밸런싱은 사이버 먼데이 세일이나
  월드컵 입장권 판매처럼 알려진 이벤트로 트래픽 급증이 예상될 때 선제적으로 리밸런싱하는 데도
  유용하다** (7장, p.265).[^kleppmann2026]

## 이어지는 페이지

- [샤드 리밸런싱 운영](../concepts/shard-rebalancing-operations.md) — 위 판단의 원본 서술
- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — 여기 쓰이는 세 도구가 속한
  모음의 전제와 경고
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 선호 리더와
  인-싱크(in-sync) 판정이 정의되는 곳
- [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md) — 여기서 손으로 촉발하는
  그 선출이 무엇을 맞바꾸는지
- [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md) — 파티션 추가가 깨뜨리는
  키 기반 가정
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 파티션이 확장과 복제의 단위인 이유
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 세그먼트가 보존 정책을
  미루는 곳이자 재할당이 복사하는 그 파일들
- [설정 관리](../concepts/kafka-config-administration.md) — 복제 스로틀링에 쓰는 쿼터를 바꾸는
  통로
- [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md) — 재할당 취소가 예전에 속해
  있던 범주

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(pp.127–130)와 12장 "Administering Kafka"(pp.310–332) — 인용 블록은 5장 p.127과 12장 pp.326·329·331 원문. 자바 코드 펜스는 5장 p.130 예제에서 원문의 주석 번호 표식을 덜어내고 지면에서 하이픈으로 끊긴 식별자를 이었고, JSON 펜스는 12장 p.328 원문 그대로다(둘 다 보탠 줄 없음)

[^kleppmann2026]: Kleppmann & Riccomini 2026, 7장 "Sharding"

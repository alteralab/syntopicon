---
type: concept
title: 안전하지 않은 작업
description: 책이 위험하다고 명시하면서도 비상용으로 적어 둔 세 가지 작업 — 주키퍼 메타데이터를 직접 건드린다는 공통 성질과 그 경고, 컨트롤러를 강제로 옮기는 법, 삭제가 걸려 버린 토픽을 풀어 주는 법, 그리고 브로커를 전부 내리고 토픽을 손으로 지우는 절차
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 안전하지 않은 작업

- [버전 조건](#버전-조건)
- [왜 이런 것이 적혀 있는가](#왜-이런-것이-적혀-있는가)
- [여기 용이 산다](#여기-용이-산다)
- [클러스터 컨트롤러 옮기기](#클러스터-컨트롤러-옮기기)
- [삭제 대기 토픽 제거하기](#삭제-대기-토픽-제거하기)
- [토픽 수동 삭제하기](#토픽-수동-삭제하기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **기술적으로는 가능하지만 극단적인 상황이 아니면 시도하면 안 되는 관리 작업은
무엇이고, 각각은 정확히 무엇을 요구하는가.**

## 버전 조건

> **버전 조건**: Kafka 3.9 이하. 이 절의 작업은 대부분 **주키퍼에 저장된 클러스터
> 메타데이터를 직접 다루는 것**이라(12장, p.335),[^shapira2021] 주키퍼 모드가 남아 있던
> 마지막 릴리스인 3.9까지 적용된다. **4.0 이상에는 적용되지 않는다** — 그쪽에는 여기서
> 지우라는 z노드(znode)가 존재하지 않는다
> ([주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md),
> [KRaft 컨트롤러 쿼럼](../concepts/kraft-controller-quorum.md)).

## 왜 이런 것이 적혀 있는가

- 이 절의 성격을 책이 스스로 규정한다. 강도를 낮추지 않기 위해 원문 그대로 옮긴다 (12장,
  p.335):[^shapira2021]

  > There are some administrative tasks that are technically possible to do but should not be
  > attempted except in the most extreme situations. Often this is when you are diagnosing a
  > problem and have run out of options, or you have found a specific bug that you need to work
  > around temporarily. These tasks are usually undocumented, unsupported, and pose some amount
  > of risk to your application.

- 그럼에도 적어 둔 이유와 그에 붙은 조건도 원문이 정확하다 (12장, p.335):[^shapira2021]

  > Several of the more common of these tasks are documented here so that in an emergency
  > situation, there is a potential option for recovery. Their use is not recommended under
  > normal cluster operations and should be considered carefully before being executed.

## 여기 용이 산다

- 절 전체에 걸리는 경고 상자다. 제목이 "Danger: Here Be Dragons"이고 본문은 이렇다 (12장,
  p.335):[^shapira2021]

  > The operations in this section often involve working with the cluster metadata stored in
  > ZooKeeper directly. This can be a very dangerous operation, so you must be very careful to
  > not modify the information in ZooKeeper directly, except as noted.

  - 같은 책 5장이 어드민 작업 일반에 대해 **주키퍼를 직접 쓰지 말 것을 강력히 권고하고, 꼭
    그래야 한다면 그것을 아파치 카프카에 버그로 신고하라**고 한 것과 같은 방향이다 (5장,
    p.115).[^shapira2021] 그 권고는
    [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md)에 있다.

## 클러스터 컨트롤러 옮기기

- 평상시의 동작부터 — **모든 카프카 클러스터에는 컨트롤러로 지정된 브로커가 하나 있고, 컨트롤러는
  보통의 브로커 작업에 더해 클러스터 작업을 총괄하는 특별한 스레드를 갖는다. 보통 컨트롤러 선출은
  주키퍼의 임시(ephemeral) 노드 감시를 통해 자동으로 이뤄진다. 컨트롤러가 꺼지거나 사용 불가가
  되면 다른 브로커들이 가능한 한 빨리 자신을 후보로 내세우는데, 컨트롤러가 셧다운되는 순간 그
  z노드가 사라지기 때문**이다 (12장, pp.335–336).[^shapira2021] 그 선출 절차의 전모는
  [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)에 있다.
- 손으로 옮기고 싶어지는 상황은 하나로 좁혀진다 — **오작동하는 클러스터나 브로커를
  트러블슈팅할 때, 호스트를 셧다운하지 않고 컨트롤러를 다른 브로커로 강제로 옮기는 것이 유용할
  수 있다. 한 예는 컨트롤러가 예외나 다른 문제를 겪어 돌아는 가지만 제 기능을 못 하는 상태로
  남은 경우**다 (12장, p.336).[^shapira2021]
- 위험도에 대한 책의 평가는 조건부다 — **이런 상황에서 컨트롤러를 옮기는 것은 보통 위험이
  높지 않지만, 정상적인 작업이 아니므로 상시로 수행해서는 안 된다** (12장,
  p.336).[^shapira2021]
- 방법과 그 대가 (12장, p.336):[^shapira2021]

  > To forcibly move a controller, deleting the ZooKeeper znode at */admin/controller* manually
  > will cause the current controller to resign, and the cluster will randomly select a new
  > controller. There is currently no way to specify a specific broker to be controller in
  > Apache Kafka.

  - 즉 **어느 브로커가 새 컨트롤러가 될지는 고를 수 없다** — 옮기는 것까지가 이 작업이 주는
    전부다.

## 삭제 대기 토픽 제거하기

- 정상 경로부터 — **카프카에서 토픽을 삭제하려 하면 삭제를 요청하는 주키퍼 노드가 만들어진다.
  모든 레플리카가 토픽 삭제를 마치고 삭제 완료를 확인응답하면 그 z노드가 제거된다. 정상적인
  상황에서 클러스터는 이것을 매우 빠르게 수행**한다 (12장, p.336).[^shapira2021] 삭제를
  거는 쪽은 [토픽 관리](../concepts/kafka-topic-administration.md)에 있다.
- **그런데 이 과정이 잘못될 때가 있다.** 책이 드는, 삭제 요청이 걸려 버리는(stuck) 시나리오는
  둘이다 (12장, p.336):[^shapira2021]
  - **요청하는 쪽은 클러스터에 토픽 삭제가 켜져 있는지 알 방법이 없어서, 삭제가 꺼져 있는
    클러스터에 토픽 삭제를 요청할 수 있다.**
  - **아주 큰 토픽의 삭제가 요청됐는데 요청이 처리되기 전에 레플리카 집합 하나 이상이 하드웨어
    장애로 오프라인이 되면, 컨트롤러가 삭제 완료를 확인응답할 수 없어 삭제가 끝나지 못한다.**
- 푸는 방법과 그 안의 함정 (12장, p.336):[^shapira2021]

  > To "unstick" topic deletion, first delete the `/admin/delete_topic/<topic>` znode. Deleting
  > the topic ZooKeeper nodes (but not the parent `/admin/delete_topic` node) will remove the
  > pending requests.

  - **부모 노드 `/admin/delete_topic`은 지우지 않는다**는 것이 이 절차의 핵심이다.
  - 한 단계가 더 필요할 수 있다 — **컨트롤러에 캐시된 요청 때문에 삭제가 다시 큐에 들어가면,
    캐시된 요청이 컨트롤러에 남지 않도록 토픽 z노드를 지운 직후 위와 같이 컨트롤러를 강제로
    옮겨야 할 수도** 있다 (12장, p.336).[^shapira2021]

## 토픽 수동 삭제하기

- 언제 하게 되는가 — **토픽 삭제가 꺼진 클러스터를 운영 중이거나, 정상 운영 흐름 바깥에서
  토픽을 지워야 하는 상황이면 클러스터에서 손으로 지우는 것이 가능**하다 (12장,
  p.336).[^shapira2021]
- 대가는 전면 정지다 — **다만 이것은 클러스터 안 모든 브로커의 완전한 셧다운을 요구하며,
  클러스터의 브로커가 하나라도 돌아가는 동안에는 할 수 없다** (12장,
  pp.336–337).[^shapira2021]
- 그 위에 경고 상자가 하나 더 붙는다. "Shut Down Brokers First"의 본문 (12장,
  p.337):[^shapira2021]

  > Modifying the cluster metadata in ZooKeeper when the cluster is online is a very dangerous
  > operation and can put the cluster into an unstable state. Never attempt to delete or modify
  > topic metadata in ZooKeeper while the cluster is online.

- 절차는 넷이고, 두 번째 단계에 자식 노드 주의가 붙는다 (12장, p.337):[^shapira2021]

  > 1. Shut down all brokers in the cluster.
  > 2. Remove the ZooKeeper path `/brokers/topics/<topic>` from the Kafka cluster path. Note
  >    that this node has child nodes that must be deleted first.
  > 3. Remove the partition directories from the log directories on each broker. These will be
  >    named `<topic>-<int>`, where `<int>` is the partition ID.
  > 4. Restart all brokers.

  - 3단계가 가리키는 그 디렉터리들이 어떻게 이름 붙고 무엇을 담는지는
    [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.

## 이어지는 페이지

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 여기서 손대는 그 메타데이터가 사는 곳,
  그리고 4.0에서 이 절 전체가 성립하지 않게 된 이유
- [KRaft 컨트롤러 쿼럼](../concepts/kraft-controller-quorum.md) — 컨트롤러 선출이 z노드를 떠난 뒤
- [토픽 관리](../concepts/kafka-topic-administration.md) — 정상 경로의 토픽 삭제와 그것이
  비동기인 이유
- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 손으로 지우게 되는 파티션
  디렉터리
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — 같은 장의 정상적인 도구들
- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 주키퍼 직접 조작을 하지 말라는
  같은 책의 권고

[^shapira2021]: Shapira et al. 2021, 12장 "Administering Kafka"(5장 참조는 5장 "Managing Apache Kafka Programmatically") — 인용 블록은 pp.335·336·337 원문. 원문이 이탤릭으로 쓴 z노드 경로(`/admin/delete_topic/<topic>`·`/brokers/topics/<topic>`·`<topic>-<int>`)만 인라인 코드로 옮겼다 — 마크다운이 꺾쇠를 HTML 태그로 먹어 자리표시자가 사라지기 때문이며, 글자는 원문 그대로다

---
type: concept
title: KRaft 컨트롤러 쿼럼
description: 주키퍼가 사라진 Kafka 4.0에서 클러스터 메타데이터를 들고 있는 컨트롤러 쿼럼 — 프로세스 역할과 쿼럼 규모, 포맷으로 시작하는 프로비저닝, 정적 쿼럼과 동적 쿼럼의 갈림, 컨트롤러 추가·제거, 그리고 주키퍼 설정·메트릭 표면의 대체물
generated: { by: "claude-opus-5", at: "2026-08-13T17:00:00Z" }
status: draft
sources:
  - { id: kafka2025-kraft, resource: /it/sources/kafka2025-kraft.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# KRaft 컨트롤러 쿼럼

- [버전 조건](#버전-조건)
- [프로세스 역할](#프로세스-역할)
- [컨트롤러와 메타데이터 쿼럼](#컨트롤러와-메타데이터-쿼럼)
- [노드 프로비저닝](#노드-프로비저닝)
- [정적 쿼럼과 동적 쿼럼](#정적-쿼럼과-동적-쿼럼)
- [컨트롤러 추가와 제거](#컨트롤러-추가와-제거)
- [쿼럼 상태를 들여다보는 도구](#쿼럼-상태를-들여다보는-도구)
- [주키퍼 표면의 대체물](#주키퍼-표면의-대체물)
- [이행 경로와 브리지 릴리스](#이행-경로와-브리지-릴리스)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **주키퍼가 없는 카프카에서 클러스터 메타데이터는 누가 들고 있고, 그
구성원은 어떻게 정해지고 바뀌는가.**

## 버전 조건

> **버전 조건**: Kafka 4.0 이상. 근거 소스가 4.0 문서이고, 여기 나오는 설정과 명령은
> 주키퍼 모드가 남아 있던 [Kafka 3.9 이하](../concepts/zookeeper-and-kraft.md)에는
> 그대로 적용되지 않는다. 개별 claim에 더 좁은 조건이 붙으면 그 자리에 표시한다.

## 프로세스 역할

- KRaft 모드에서 카프카 서버 각각은 `process.roles` 속성으로 **컨트롤러(controller),
  브로커(broker), 또는 둘 다**로 구성된다 (kraft, "Process Roles").[^kafka2025-kraft]
  - `broker`면 브로커로, `controller`면 컨트롤러로, `broker,controller`면 둘 다로
    동작한다.
- 둘 다인 서버를 **결합(combined) 서버**라 부른다. 개발 환경 같은 소규모 용도에는
  운영이 간단하지만, 핵심 단점은 **컨트롤러가 나머지 시스템에서 덜 격리된다**는 것이다
  — 예컨대 결합 모드에서는 컨트롤러만 따로 롤링하거나 확장할 수 없다. 중요한 배치
  환경에는 권장되지 않는다 (kraft, "Process Roles").[^kafka2025-kraft]
- 배치 고려 사항에서 같은 말을 다시 못박는다 — `process.role`은 `broker`나
  `controller` 중 하나여야 하고 둘 다여서는 안 된다 (kraft, "Deploying
  Considerations").[^kafka2025-kraft]

## 컨트롤러와 메타데이터 쿼럼

- KRaft 모드에서는 특정 카프카 서버들이 컨트롤러로 지정되고, **그 서버들이 메타데이터
  쿼럼(metadata quorum)에 참여한다.** 각 컨트롤러는 현재 액티브 컨트롤러(active
  controller)이거나 그것의 핫 스탠바이(hot standby)다 (kraft,
  "Controllers").[^kafka2025-kraft]
- 규모 판단: 관리자는 보통 **3대나 5대**를 이 역할에 고르며, 기준은 비용과 가용성을
  해치지 않고 견뎌야 할 동시 장애 수다. 가용성 유지에는 **컨트롤러 과반이 살아
  있어야** 한다 — 3대면 1대 장애, 5대면 2대 장애를 견딘다 (kraft,
  "Controllers").[^kafka2025-kraft]
- 같은 규칙의 일반형: **N개의 동시 장애를 견디려면 컨트롤러 클러스터에 2N + 1개의
  컨트롤러가 있어야 한다** (kraft, "Deploying Considerations").[^kafka2025-kraft]
  - 이것은 주키퍼 앙상블의 홀수 권고와 같은 자리에 있는 과반 규칙이고, 원전은
    [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md)의 과반 득표
    조건이다.
- 클러스터의 모든 서버는 `controller.quorum.bootstrap.servers` 속성으로 액티브
  컨트롤러를 찾는다. **모든 컨트롤러를 이 속성에 열거해야 하며**, 각 컨트롤러는
  `host`와 `port`로 식별된다. **브로커와 컨트롤러 전부가 이 속성을 설정해야 한다**
  (kraft, "Controllers").[^kafka2025-kraft]
- 이 쿼럼이 바깥에서 무슨 문제를 푸는 것으로 보이는지는 일반 문헌이 한 줄로 적는다 —
  **카프카·YugabyteDB·TiDB·ScyllaDB는 샤드를 노드에 배정하는 코디네이션 기능을 수행하는 데
  Raft 합의 프로토콜의 내장 구현을 쓴다** (7장, p.267).[^kleppmann2026] 같은 기능을 외부
  서비스에 맡기는 쪽(주키퍼·etcd)과 대비되는 자리이며, 그 지형은
  [요청 라우팅](../concepts/request-routing.md)에 있다.
- 자원 요구: 컨트롤러는 클러스터의 모든 메타데이터를 **메모리와 디스크 양쪽에**
  저장한다. 전형적인 카프카 클러스터라면 주 메모리 5GB와 메타데이터 로그 디렉터리의
  디스크 5GB로 충분하다고 문서는 본다 (kraft, "Deploying
  Considerations").[^kafka2025-kraft]

## 노드 프로비저닝

- 클러스터 ID는 `bin/kafka-storage.sh random-uuid`로 만들고, **클러스터의 각 서버를
  `bin/kafka-storage.sh format`으로 포맷할 때 그 ID를 써야 한다** (kraft, "Provisioning
  Nodes").[^kafka2025-kraft]
- 이것은 과거 카프카의 동작과 다르다 — 예전에는 빈 저장 디렉터리를 자동으로 포맷하고
  클러스터 ID도 자동 생성했다. 바꾼 이유 하나는 **자동 포맷이 오류 상태를 가릴 수
  있다**는 것이고, 이는 컨트롤러와 브로커가 유지하는 메타데이터 로그에서 특히 중요하다
  — **컨트롤러 과반이 빈 로그 디렉터리로 시작할 수 있으면 커밋된 데이터가 빠진 채로
  리더가 선출될 수 있다** (kraft, "Provisioning Nodes").[^kafka2025-kraft]
  - 이 위험의 원전 서술은 [Raft의 안전성과 선출 제약](../concepts/raft-safety.md)의
    선출 제약이다 — 커밋된 항목을 가진 서버만 리더가 될 수 있어야 한다는 그 조건을,
    빈 로그로 뜬 과반이 무너뜨린다.
- 새 KRaft 컨트롤러 클러스터를 만드는 권장 방법은 **투표자(voter) 하나로 부트스트랩한
  뒤 나머지 컨트롤러를 동적으로 추가하는 것**이며, 첫 컨트롤러는
  `kafka-storage.sh format --cluster-id <CLUSTER_ID> --standalone --config
  config/controller.properties`로 만든다 (kraft, "Bootstrap a Standalone
  Controller").[^kafka2025-kraft]
  - 이 명령이 하는 일은 둘이다 — ⑴ `metadata.log.dir`에 무작위 생성된 `directory.id`를
    담은 `meta.properties` 파일을 만들고, ⑵ 이 노드를 쿼럼의 유일한 투표자로 만드는 제어
    레코드(`KRaftVersionRecord`·`VotersRecord`)를 담은 스냅샷
    `00000000000000000000-0000000000.checkpoint`를 만든다.
- 투표자를 여럿 두고 한 번에 부트스트랩할 수도 있다 — `--initial-controllers` 플래그를
  쓰면 스냅샷의 `VotersRecord`가 열거된 컨트롤러 전부의 정보를 담는다. **같은 클러스터
  ID를 쓰는 모든 컨트롤러에서 이 플래그 값이 같아야 한다** (kraft, "Bootstrap with
  Multiple Controllers").[^kafka2025-kraft]
  - 레플리카 서술 `0@controller-0:1234:3Db5QLSqSZieL3rJBUUegA`의 자리별 뜻은
    레플리카 ID, 호스트, 포트, 레플리카 디렉터리 ID다.
- 이미 있는 클러스터에 새 브로커·컨트롤러를 넣으려고 프로비저닝할 때는
  `--no-initial-controllers` 플래그로 포맷한다 (kraft, "Formatting Brokers and New
  Controllers").[^kafka2025-kraft]

## 정적 쿼럼과 동적 쿼럼

- KRaft를 돌리는 방법은 둘이다 — **정적 컨트롤러 쿼럼을 쓰는 옛 방식과, KIP-853의 동적
  컨트롤러 쿼럼을 쓰는 새 방식** (kraft, "Static versus Dynamic KRaft
  Quorums").[^kafka2025-kraft]
  - **정적**이면 브로커와 컨트롤러의 설정 파일마다 모든 컨트롤러의 ID·호스트명·포트를
    `controller.quorum.voters`에 적어야 한다.
  - **동적**이면 대신 `controller.quorum.bootstrap.servers`를 설정한다. 이 키는 모든
    컨트롤러를 담을 필요는 없지만, 모든 서버가 쿼럼을 찾을 수 있도록 가능한 한 많이
    담아야 한다 — 기능은 클라이언트의 `bootstrap.servers`와 비슷하다.
- 어느 쪽인지 모르면 `bin/kafka-features.sh --bootstrap-controller localhost:9093
  describe`로 판별한다 — **`kraft.version` 필드가 0이거나 없으면 정적, 1 이상이면
  동적**이다 (kraft, "Static versus Dynamic KRaft Quorums").[^kafka2025-kraft]
- 정적이냐 동적이냐는 **포맷 시점에 결정된다** — `controller.quorum.voters`가 없고
  소프트웨어가 Apache Kafka 3.9 이상이면 동적으로 포맷된다. 동적 쿼럼이 안 되면 포맷을
  실패시키고 싶으면 `--feature kraft.version=1`을 주는데, **이 플래그는 컨트롤러를
  포맷할 때만 주고 브로커에는 주지 않는다** (kraft, "Static versus Dynamic KRaft
  Quorums").[^kafka2025-kraft]
- 제약 하나: **정적 컨트롤러 쿼럼을 쓰는 클러스터를 동적 쿼럼으로 전환하는 것은 현재
  불가능하다** (kraft, "Static versus Dynamic KRaft Quorums").[^kafka2025-kraft]
  - 버전 조건: Kafka 4.0 기준 — 문서가 "향후 릴리스에서 지원될 것"이라고만 적으므로,
    후속 버전에서 뒤집힐 수 있는 서술이다.

## 컨트롤러 추가와 제거

- 동적 컨트롤러 클러스터는 확장할 수 있다 — 새 컨트롤러를 `kafka-storage.sh`로
  프로비저닝해 띄운 뒤 `bin/kafka-metadata-quorum.sh describe --replication`으로 복제를
  지켜보고, **새 컨트롤러가 액티브 컨트롤러를 따라잡은 다음에**
  `bin/kafka-metadata-quorum.sh add-controller`로 클러스터에 넣는다. 브로커 엔드포인트를
  쓰면 `--bootstrap-server`, 컨트롤러 엔드포인트를 쓰면 `--bootstrap-controller`
  플래그를 쓴다 (kraft, "Add New Controller").[^kafka2025-kraft]
- 축소는 `bin/kafka-metadata-quorum.sh remove-controller`이며, 인자로 `--controller-id`와
  `--controller-directory-id`를 준다 (kraft, "Remove Controller").[^kafka2025-kraft]
  - 운영 권고에 시한이 붙어 있다 — **KIP-996(pre-vote)가 구현·릴리스되기 전까지는
    제거할 컨트롤러를 먼저 종료한 뒤 명령을 돌리는 것이 권장된다.**
  - 버전 조건: Kafka 4.0 기준 — KIP-996이 들어간 릴리스에서는 이 권고가 사라질 수 있다.
  - 제거되는 서버가 선출을 방해하는 문제 자체의 원전은
    [Raft의 클러스터 멤버십 변경](../concepts/raft-membership-change.md)에 있다.

## 쿼럼 상태를 들여다보는 도구

- `kafka-metadata-quorum.sh describe --status`는 클러스터 메타데이터 파티션의 런타임
  상태를 요약한다 — `ClusterId`, `LeaderId`, `LeaderEpoch`, `HighWatermark`,
  `MaxFollowerLag`, `MaxFollowerLagTimeMs`, 그리고 `CurrentVoters`와
  `CurrentObservers` 목록이다 (kraft, "Metadata Quorum
  Tool").[^kafka2025-kraft]
  - #hypothesis 예시 출력에서 `CurrentVoters`는 컨트롤러 엔드포인트를 가진 ID들이고
    `CurrentObservers`는 그렇지 않은 ID들이므로, 관측자(observer)는 투표하지 않고
    메타데이터 로그를 따라오기만 하는 노드(즉 브로커)로 보인다. 문서가 관측자를
    정의하지는 않으므로 확정 서술로 쓰지 않는다.
- `kafka-dump-log.sh --cluster-metadata-decoder --files …`는 클러스터 메타데이터
  디렉터리의 로그 세그먼트와 스냅샷을 훑어 **메타데이터 레코드를 해독해 출력한다**
  (kraft, "Dump Log Tool").[^kafka2025-kraft]
- `kafka-metadata-shell.sh --snapshot …`은 클러스터 메타데이터 파티션의 상태를 대화식
  트리로 뜯어본다 — 최상위는 `brokers`·`local`·`metadataQuorum`·`topicIds`·`topics`이고,
  토픽 파티션 데이터에는 `replicas`·`isr`·`leader`·`leaderEpoch`·`partitionEpoch`가 들어
  있다 (kraft, "Metadata Shell").[^kafka2025-kraft]

## 주키퍼 표면의 대체물

주키퍼 모드에 있던 설정·메트릭이 무엇으로 대체됐는지의 목록이다. 사라진 쪽의 원래
동작은 [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)가 담당한다.

- **컨트롤 플레인 리스너** — `control.plane.listener.name`이 제거됐다. 주키퍼 모드에서는
  카프카가 메타데이터 관리를 주키퍼에 맡기면서도 컨트롤러와 브로커 사이 통신 같은 내부
  작업에는 자체 컨트롤 플레인을 썼다. KRaft에서는 컨트롤 플레인 기능이 카프카 자체에
  완전히 통합되고 **프로세스 역할이 명확히 갈린다** — 브로커가 데이터 관련 요청을,
  컨트롤러가 메타데이터 관련 요청을 처리하며, 컨트롤러끼리는 Raft 프로토콜로 통신한다.
  대체 설정은 `controller.listener.names`·`listeners`·`listener.security.protocol.map`
  이다 (zk2kraft, "Configurations").[^kafka2025-kraft]
- **노드 식별** — `reserved.broker.max.id`와 `broker.id.generation.enable`이 제거됐다.
  KRaft에서는 `node.id`로 서버를 식별한다 (zk2kraft,
  "Configurations").[^kafka2025-kraft]
- **기능 수준** — `inter.broker.protocol.version`이 제거됐다. KRaft에서는
  `metadata.version`이 클러스터의 기능 수준을 정하며 `bin/kafka-features.sh`로 관리한다
  (zk2kraft, "Configurations").[^kafka2025-kraft]
- **민감 데이터** — `password.encoder.*` 계열 여섯 설정이 제거됐다. 주키퍼 모드에서
  민감 데이터 암호화 키와 알고리즘을 정하던 것들인데, **KRaft에서는 카프카가 민감
  데이터를 레코드에 저장하고 그 데이터를 암호화하지 않는다** (zk2kraft,
  "Configurations").[^kafka2025-kraft]
- **제어된 종료** — `controlled.shutdown.max.retries`와
  `controlled.shutdown.retry.backoff.ms`가 제거됐다. KRaft에서는 브로커 종료 과정을
  **쿼럼 기반 컨트롤러가 관리하며**, 리더 이전과 메타데이터 갱신이 컨트롤러에서
  자동으로 처리돼 더 신뢰할 수 있고 효율적이라고 문서는 적는다 (zk2kraft,
  "Configurations").[^kafka2025-kraft]
- **동적 갱신 범위의 축소** — 주키퍼에 의존하던 동적 설정이 제거돼
  `advertised.listeners`를 바꾸려면 브로커·컨트롤러를 재시작해야 한다. 주키퍼 전용이던
  `leader.imbalance.per.broker.percentage`도 제거됐다 (zk2kraft,
  "Configurations").[^kafka2025-kraft]
- **동적 로그 레벨** — 실행 중인 프로세스의 log4j 설정을 재시작 없이 바꾸는 기능은
  남아 있고 브로커 쪽 명령 문법도 그대로다. 다만 **컨트롤러에 걸 때는
  `--bootstrap-controller` 플래그를 써야 하고, 그때도 `--entity-type`은
  `broker-loggers`로 적는다.** 결합 노드는 로그 레벨 집합이 하나뿐이라 브로커·컨트롤러
  쪽을 따로 둘 수 없다 (zk2kraft, "Dynamic Log Levels").[^kafka2025-kraft]
- **동적 설정의 적용 범위** — 컨트롤러는 적용 가능한 클러스터 수준 동적 설정을 전부
  적용한다. 그래서 `--entity-default`로 건 `max.connections` 변경은 클러스터의 모든
  브로커와 모든 컨트롤러에 걸린다. **컨트롤러 한 대에만 동적 설정을 거는 것은 현재
  불가능하다** (zk2kraft, "Dynamic Controller Configurations").[^kafka2025-kraft]
- **메트릭** — `ControlPlaneNetworkProcessorAvgIdlePercent`와
  `ControlPlaneExpiredConnectionsKilledCount`가 제거되고 각각
  `NetworkProcessorAvgIdlePercent`·`ExpiredConnectionsKilledCount`가 그 자리를 맡는다.
  주키퍼 모드 전용이던 `kafka.controller:*` 계열과 `SessionExpireListener`·
  `ZooKeeperClientMetrics` 계열 메트릭도 함께 사라졌다 (zk2kraft,
  "Metrics").[^kafka2025-kraft]
- **동작 변화 셋** (zk2kraft, "Behavioral Change Reference"):[^kafka2025-kraft]
  - **설정 값 크기 제한** — KRaft는 설정 값의 최대 크기를 `Short.MAX_VALUE`로 제한하며,
    그래서 append 연산으로 더 큰 설정 값을 만들 수 없다.
  - **정책 클래스 배치 위치** — `CreateTopicPolicy`와 `AlterConfigPolicy` 플러그인이
    브로커가 아니라 **컨트롤러에서 실행된다.** 정책 클래스 JAR을 컨트롤러에 배포하고
    `create.topic.policy.class.name`·`alter.config.policy.class.name`도 컨트롤러에
    설정해야 한다.
  - **주체 빌더** — `KafkaPrincipalBuilder`의 사용자 정의 구현은 반드시
    `KafkaPrincipalSerde`도 함께 구현해야 한다. 그러지 않으면 **브로커가 컨트롤러로
    요청을 전달하지 못한다.**

## 이행 경로와 브리지 릴리스

- 주키퍼에서 KRaft로 옮기려면 **브리지 릴리스(bridge release)를 거쳐야 하고, 마지막
  브리지 릴리스는 Kafka 3.9다** (kraft, "ZooKeeper to KRaft
  Migration").[^kafka2025-kraft]
  - 4.0 문서는 이행 절차 자체를 담지 않고 3.9 문서로 넘긴다. 즉 **3.9를 건너뛴 직접
    이행 경로는 없다.**
- 4.0 문서 어디에도 KRaft 관련 EOL 날짜나 폐기 예정 표시는 없다. 그래서 이 페이지에는
  `stale_after`를 달지 않았다 — 만료는 감이 아니라 공표된 날짜가 있을 때만 단다.

## 이어지는 페이지

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 이 페이지가 대체한 그 기제,
  즉 주키퍼 앙상블과 임시 노드 컨트롤러 선출(Kafka 3.9 이하)
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 컨트롤러가 놓인 자리의 개요
- [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md) — 컨트롤러 쿼럼이 쓰는
  선출 알고리즘의 원전과 과반 규칙
- [Raft의 안전성과 선출 제약](../concepts/raft-safety.md) — 빈 로그로 뜬 과반이 왜
  위험한지의 원전
- [Raft의 클러스터 멤버십 변경](../concepts/raft-membership-change.md) — 컨트롤러
  추가·제거가 건드리는 문제의 원전
- [복제 상태 기계와 합의](../concepts/replicated-state-machine.md) — 메타데이터 로그를
  복제한다는 말이 놓인 자리
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 여기서 사라진
  `zookeeper.connect`가 있던 설정 목록
- [요청 라우팅](../concepts/request-routing.md) — 컨트롤러 쿼럼이 대신 맡은 그 기능의 일반형

[^kafka2025-kraft]: Apache Kafka 4.0 문서, `getting-started/zk2kraft/`("KRaft vs ZooKeeper") · `operations/kraft/`("KRaft"), 2026-08-11 조회

[^kleppmann2026]: Kleppmann & Riccomini 2026, 7장 "Sharding"

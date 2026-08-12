---
type: concept
title: 설정 관리
description: 돌아가는 클러스터의 설정을 코드와 명령줄에서 바꾸는 일 — AdminClient의 단위인 ConfigResource와 그 3종, 기본값이 아닌 항목만 골라내는 isDefault의 판정 기준, 설정을 바꾸는 네 가지 작업 유형, kafka-configs.sh의 네 가지 엔티티 타입과 토픽·클라이언트·브로커 재정의, 재정의만 보여 주고 클러스터 기본값은 안 보여 준다는 한계, 그리고 브로커 설정 파일이 깨졌을 때 설정을 덤프해 되살린 사례
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 설정 관리

- [설정 리소스 3종](#설정-리소스-3종)
- [기본값과 다른 것 골라내기](#기본값과-다른-것-골라내기)
- [바꾸기와 네 가지 작업 유형](#바꾸기와-네-가지-작업-유형)
- [비상시에 설정을 되살린 사례](#비상시에-설정을-되살린-사례)
- [명령줄에서 — 네 가지 엔티티 타입](#명령줄에서--네-가지-엔티티-타입)
- [토픽 설정 재정의](#토픽-설정-재정의)
- [클라이언트와 사용자 설정 재정의](#클라이언트와-사용자-설정-재정의)
- [브로커 설정 재정의](#브로커-설정-재정의)
- [재정의된 것만 보인다](#재정의된-것만-보인다)
- [재정의 되돌리기](#재정의-되돌리기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **토픽·브로커·클라이언트의 설정을 어떤 단위로 읽고, 무엇을 기준으로 바뀐 값을
가려내고, 코드와 명령줄에서 각각 어떻게 고치는가.**

> **버전 조건**: Kafka 0.11 이상 — **아래 API 절들**의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021] 명령줄 절의 `kafka-configs.sh`에는 이 조건이 걸리지
> 않지만, **동적으로 재정의 가능한 설정은 릴리스마다 계속 늘어나므로 클러스터와 같은 버전의
> 도구를 쓸 것**을 책이 따로 당부한다 (12장, p.315).[^shapira2021]

## 설정 리소스 3종

- **설정 관리는 `ConfigResource` 모음을 설명(describe)하고 갱신하는 방식으로 이뤄진다.** 설정
  리소스가 될 수 있는 것은 **브로커, 브로커 로거(broker logger), 토픽** 셋이다 (5장,
  p.121).[^shapira2021]
- 어느 쪽을 코드로 다루는 것이 흔한지는 갈린다 — **브로커나 브로커 로깅 설정을 확인·수정하는
  일은 보통 `kafka-config.sh` 같은 툴이나 다른 카프카 관리 도구로 하지만, 토픽 설정을 그것을
  쓰는 애플리케이션에서 확인하고 갱신하는 일은 꽤 흔하다** (5장, p.121).[^shapira2021]
  그 CLI 쪽은 [아래 명령줄 절](#명령줄에서--네-가지-엔티티-타입)에 있다.
- 책이 드는 동기 — **많은 애플리케이션이 올바른 동작을 위해 압착된(compacted) 토픽에
  의존한다. 그런 애플리케이션이 주기적으로 — 안전을 위해 기본 보존 기간보다 더 자주 —
  토픽이 실제로 압착돼 있는지 확인하고 그렇지 않으면 토픽 설정을 바로잡는 조치를 취하는 것이
  말이 된다** (5장, p.122).[^shapira2021] 압착이 무엇을 보존하는지는
  [카프카 로그 압착](../concepts/kafka-log-compaction.md)에 있다.

## 기본값과 다른 것 골라내기

- 아래가 그 확인과 교정의 형태이며, `ConfigResource`·`describeConfigs`·
  `incrementalAlterConfigs`로 찾는다 (5장, p.122):[^shapira2021]

  ```java
  ConfigResource configResource =
          new ConfigResource(ConfigResource.Type.TOPIC, TOPIC_NAME);
  DescribeConfigsResult configsResult =
          admin.describeConfigs(Collections.singleton(configResource));
  Config configs = configsResult.all().get().get(configResource);

  // print nondefault configs
  configs.entries().stream().filter(
          entry -> !entry.isDefault()).forEach(System.out::println);

  // Check if topic is compacted
  ConfigEntry compaction = new ConfigEntry(TopicConfig.CLEANUP_POLICY_CONFIG,
          TopicConfig.CLEANUP_POLICY_COMPACT);
  if (!configs.entries().contains(compaction)) {
      // if topic is not compacted, compact it
      Collection<AlterConfigOp> configOp = new ArrayList<AlterConfigOp>();
      configOp.add(new AlterConfigOp(compaction, AlterConfigOp.OpType.SET));
      Map<ConfigResource, Collection<AlterConfigOp>> alterConf = new HashMap<>();
      alterConf.put(configResource, configOp);
      admin.incrementalAlterConfigs(alterConf).all().get();
  } else {
      System.out.println("Topic " + TOPIC_NAME + " is compacted topic");
  }
  ```

- **`ConfigResource`에는 여러 종류가 있고 위에서는 특정 토픽의 설정을 확인하고 있다. 한 요청에
  서로 다른 종류의 여러 리소스를 지정할 수도** 있다 (5장, p.122).[^shapira2021]
- **`describeConfigs`의 결과는 각 `ConfigResource`에서 설정 모음으로 가는 맵**이다. **설정
  항목마다 `isDefault()` 메서드가 있어 어떤 설정이 수정됐는지 알려준다** (5장,
  p.122).[^shapira2021]
- 무엇이 "기본값이 아닌 것"으로 취급되는지의 판정 기준은 둘이다 — **사용자가 토픽에 기본값이
  아닌 값을 설정했거나, 브로커 수준 설정이 수정된 상태에서 토픽이 생성돼 그 기본값 아닌 값을
  브로커로부터 상속받았을 때**다 (5장, p.122).[^shapira2021] 브로커 수준 기본값이 어디서
  오는지는 [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)에 있다.

## 바꾸기와 네 가지 작업 유형

- **설정을 수정하려면 수정하려는 `ConfigResource`를 키로, 작업 모음을 값으로 하는 맵을
  지정한다. 설정을 수정하는 각 작업은 설정 항목(설정의 이름과 값 — 위 예에서는
  `cleanup.policy`가 이름이고 `compacted`가 값이다)과 작업 유형으로 이뤄진다** (5장,
  pp.122–123).[^shapira2021]
- **카프카에서 설정을 수정하는 작업 유형은 넷이다** (5장, pp.122–123):[^shapira2021]
  - **`SET` — 설정 값을 지정한다.**
  - **`DELETE` — 값을 제거하고 기본값으로 되돌린다.**
  - **`APPEND`와 `SUBTRACT` — 뒤의 둘은 `List` 타입 설정에만 적용되며, 매번 전체 목록을
    카프카로 보내지 않고도 목록에서 값을 더하고 뺄 수 있게 한다.**
- 동적으로 바꾸는 설정 중 이 KB가 따로 다루는 것이 쿼터다 —
  [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md)가 그 대상과 집행 방식을 담고,
  여기서는 그것을 바꾸는 통로만 다룬다.

## 비상시에 설정을 되살린 사례

- **설정을 설명해 보는 것이 비상 상황에서 놀랄 만큼 유용할 수 있다**고 저자들은 자기 경험을
  적어 뒀다 (5장, p.123):[^shapira2021]
  - **업그레이드 도중 브로커 설정 파일이 실수로 깨진 사본으로 교체된 일이 있었다. 첫 브로커를
    재시작했다가 시동에 실패하는 것을 보고서야 발견됐다.**
  - **팀에는 원본을 복구할 방법이 없었고, 올바른 설정을 재구성해 브로커를 되살리기 위해 상당한
    시행착오를 각오하고 있었다.**
  - **사이트 신뢰성 엔지니어(site reliability engineer, SRE)가 남아 있던 브로커 중 하나에
    접속해 AdminClient로 그 설정을 덤프해서 상황을 구했다.**

## 명령줄에서 — 네 가지 엔티티 타입

- 동적 설정의 범위부터 — **토픽·클라이언트·브로커 등 클러스터를 내리거나 재배포하지 않고
  런타임에 동적으로 갱신할 수 있는 설정이 아주 많고, `kafka-configs.sh`가 그것들을 수정하는
  주된 도구**다 (12장, p.315).[^shapira2021] 이 도구를 쓰기 전 확인할 것은
  [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md)에 있다.
- **현재 동적 설정 변경이 가능한 주 범주, 즉 엔티티 타입(entity-type)은 넷이다 — `topics`,
  `brokers`, `users`, `clients`. 엔티티 타입마다 재정의할 수 있는 특정한 설정들이 있다** (12장,
  p.315).[^shapira2021]
- 자동화용 인자가 하나 있다 — **이런 설정을 일관되게 넣도록, 관리·갱신하려는 모든 설정을 미리
  형식에 맞춰 담은 파일과 함께 `--add-config-file` 인자를 쓸 수 있다** (12장,
  p.315).[^shapira2021]

## 토픽 설정 재정의

- 왜 재정의하는가 — **정적 브로커 설정 파일에 정의돼 토픽의 기본값이 되는 설정이 많고(예:
  보존 시간 정책), 동적 설정으로 그 클러스터 단위 기본값을 개별 토픽에 대해 재정의해 한
  클러스터 안에서 서로 다른 유스케이스를 수용**한다 (12장, pp.315–316).[^shapira2021]
- 명령 형식은 `kafka-configs.sh --bootstrap-server localhost:9092 --alter --entity-type topics
  --entity-name <topic-name> --add-config <key>=<value>[,<key>=<value>...]`이고, 책의 예는
  **`my-topic`의 보존 기간을 1시간(3,600,000밀리초)으로 잡는 `--add-config
  retention.ms=3600000`**이며 성공하면 `Updated config for topic: "my-topic".`이 찍힌다 (12장,
  p.316).[^shapira2021]
- **동적으로 바꿀 수 있는 유효한 토픽 설정 키는 책이 표 12-2로 열거**한다 (12장,
  pp.316–317).[^shapira2021] 이 KB가 이미 다루는 것들이 여기 그대로 들어 있다.
  - 보존과 세그먼트 — `retention.ms`·`retention.bytes`·`segment.bytes`·`segment.ms`·
    `segment.jitter.ms`·`segment.index.bytes`·`file.delete.delay.ms`·`preallocate`. 뜻은
    [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)과
    [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
  - 압착 — `cleanup.policy`·`min.cleanable.dirty.ratio`·`min.compaction.lag.ms`·
    `max.compaction.lag.ms`·`delete.retention.ms`. 뜻은
    [카프카 로그 압착](../concepts/kafka-log-compaction.md)에 있다.
  - 신뢰성 — `min.insync.replicas`·`unclean.leader.election.enable`. 뜻은
    [카프카 신뢰성 보장](../concepts/kafka-reliability-guarantees.md)과
    [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md)에 있다.
  - 메시지와 복제 스로틀링 — `compression.type`·`max.message.bytes`·`message.format.version`·
    `message.timestamp.type`·`message.timestamp.difference.max.ms`·
    `message.downconversion.enable`·`index.interval.bytes`·
    `follower.replication.throttled.replicas`·`leader.replication.throttled.replica`.
  - 원문 오식: 마지막 둘 중 팔로워 쪽은 `replicas`(복수)인데 리더 쪽은
    `leader.replication.throttled.replica`(단수)로 인쇄돼 있다 (12장,
    p.316).[^shapira2021] 둘 다 설명은 "복제를 스로틀링할 레플리카의 목록"이다.

## 클라이언트와 사용자 설정 재정의

- 범위가 좁다 — **카프카 클라이언트와 사용자에 대해 재정의할 수 있는 설정은 몇 개뿐이고 전부
  본질적으로 쿼터 종류다. 흔히 바꾸는 둘은 특정 client ID에 대해 브로커별로 허용하는 프로듀서·
  컨슈머의 초당 바이트 속도**다 (12장, p.317).[^shapira2021] 쿼터 자체는
  [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md)에 있다.
- **`users`와 `clients` 양쪽에 대해 수정 가능한 공유 설정의 전체 목록**은 표 12-3이며 넷이다
  (12장, p.318):[^shapira2021]
  - `consumer_bytes_rate` — **단일 client ID가 1초 동안 한 브로커에서 소비할 수 있는 메시지의
    바이트 양.**
  - `producer_bytes_rate` — **단일 client ID가 1초 동안 한 브로커로 생산할 수 있는 메시지의
    바이트 양.**
  - `controller_mutations_rate` — **토픽 생성 요청·파티션 생성 요청·토픽 삭제 요청에 대해
    변경(mutation)이 받아들여지는 속도. 생성되거나 삭제된 파티션 수로 누적된다.**
  - `request_percentage` — **사용자 또는 클라이언트의 요청에 대해 쿼터 윈도우당 백분율**이며,
    전체는 `(num.io.threads + num.network.threads) × 100%`다.
  - 원문 불일치: 같은 책 3장 p.74의 예제는 같은 설정을 `producer_byte_rate`·
    `consumer_byte_rate`(단수 `byte`)로 쓴다 (3장, p.74).[^shapira2021] 표 12-3은 복수형으로
    인쇄돼 있다.
- 스로틀링이 브로커 단위라는 점이 배치 문제를 만든다 — **스로틀링이 브로커별로 일어나므로
  클러스터 전체에 걸친 파티션 리더십의 균형이 특히 중요해진다. 브로커 5대에 클라이언트 하나의
  프로듀서 쿼터가 10MBps면 그 클라이언트는 각 브로커에 동시에 10MBps씩, 리더십이 균형 잡혀
  있다는 가정하에 합계 50MBps까지 생산할 수 있다. 그러나 모든 파티션의 리더십이 브로커 1에
  몰려 있으면 같은 프로듀서는 최대 10MBps만 생산할 수 있다** (12장, p.317).[^shapira2021]
  리더십 균형을 되돌리는 방법은
  [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md)에 있다.
- client ID를 무엇으로 잡을지에 대한 권고 — **client ID가 컨슈머 그룹 이름과 같아야 하는 것은
  아니다. 컨슈머는 자기 client ID를 정할 수 있고, 서로 다른 그룹에 속한 여러 컨슈머가 같은
  client ID를 쓸 수도 있다. 컨슈머 그룹마다 그 그룹을 식별하는 고유한 값으로 client ID를 잡는
  것이 모범 사례로 여겨지는데, 그러면 한 컨슈머 그룹이 쿼터를 공유하게 되고 로그에서 어느
  그룹이 요청의 주인인지 알아보기 쉬워진다** (12장, p.318).[^shapira2021] 그룹의 정체는
  [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md)에 있다.
- **양쪽에 적용되는 호환 가능한 사용자·클라이언트 설정 변경은 함께 지정할 수 있다** — 책의
  예는 `--entity-type clients --entity-name <Client ID>`와 `--entity-type users --entity-name
  <User ID>`를 한 명령에 붙여 `controller_mutations_rate=10`을 한 번에 건다 (12장,
  p.318).[^shapira2021]

## 브로커 설정 재정의

- **브로커와 클러스터 수준 설정은 주로 클러스터 설정 파일에 정적으로 설정되지만, 카프카를
  재배포하지 않고 런타임에 재정의할 수 있는 설정도 아주 많다 — `kafka-configs.sh`로 바꿀 수
  있는 재정의가 80가지가 넘는다.** 책은 그것을 다 열거하지 않고 **`--help` 명령이나 오픈소스
  문서**로 넘긴다 (12장, p.318).[^shapira2021]
- 그중 특별히 짚은 셋 (12장, pp.318–319):[^shapira2021]
  - `min.insync.replicas` — **프로듀서가 acks를 `all`(또는 `-1`)로 잡았을 때 프로듀스 요청이
    성공하려면 쓰기를 확인응답해야 하는 레플리카의 최소 수를 조정한다.**
  - `unclean.leader.election.enable` — **데이터 유실이 나더라도 레플리카가 리더로 선출될 수
    있게 허용한다. 약간의 유실이 허용될 때, 또는 복구 불가능한 데이터 유실을 피할 수 없어
    막힌 클러스터를 풀어야 할 때 짧게 켜는 데 유용하다.**
  - `max.connections` — **한 브로커에 언제든 허용되는 최대 연결 수. 더 세밀한 스로틀링에는
    `max.connections.per.ip`와 `max.connections.per.ip.overrides`도 쓸 수 있다.**

## 재정의된 것만 보인다

- 조회는 다른 도구와 같은 `--describe`다 — **모든 설정 재정의는 설정 도구로 나열할 수 있고,
  토픽·브로커·클라이언트의 특정 설정을 살펴볼 수 있다** (12장, p.319).[^shapira2021] 책의 예는
  `--describe --entity-type topics --entity-name my-topic`으로 `retention.ms=3600000` 하나만
  얻는다.
  - 원문 오식: 이 문장의 도구 이름도 `kafka-config.sh`로 인쇄돼 있다 (12장,
    p.319).[^shapira2021] 같은 절 앞뒤의 명령은 `kafka-configs.sh`다.
- 그런데 이 조회에는 결정적인 한계가 있어 책이 경고 상자로 떼어 뒀다 (12장,
  p.319):[^shapira2021]

  > The configuration description will only show overrides—it does not include the cluster
  > default configurations. There is not a way to dynamically discover the configuration of the
  > brokers themselves. This means that when using this tool to discover topic or client
  > settings in automation, the user must have separate knowledge of the cluster default
  > configuration.

  - 코드 쪽은 이 한계를 갖지 않는다 — AdminClient의 `describeConfigs`는 항목마다
    `isDefault()`를 주므로 [위 절](#기본값과-다른-것-골라내기)처럼 기본값과 재정의를 한
    응답에서 가려낼 수 있다 (5장, p.122).[^shapira2021]

## 재정의 되돌리기

- **동적 설정은 통째로 제거할 수 있고, 그러면 해당 엔티티는 클러스터 기본값으로 되돌아간다.
  설정 재정의를 지우려면 `--alter` 명령에 `--delete-config` 매개변수를 함께 쓴다** (12장,
  p.319).[^shapira2021] 책의 예는 `--entity-type topics --entity-name my-topic --delete-config
  retention.ms`이고, 결과 메시지는 설정할 때와 같은 `Updated config for topic: "my-topic".`이다.
  - 같은 일을 코드에서 하는 것이 위의 `DELETE` 작업 유형이다 (5장, pp.122–123).[^shapira2021]

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — `kafka-configs.sh`가 속한
  도구 모음의 전제와 버전 경고
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 이 통로로 바꾸는 대표적인
  동적 설정
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 여기서 읽고 바꾸는 값들이
  원래 사는 곳
- [토픽 관리](../concepts/kafka-topic-administration.md) — 토픽 설명에는 설정이 들어 있지 않다
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 예제가 지키려는 그 설정
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 쿼터
  스로틀링이 실제로 걸리는 작업

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(pp.121–123)와 12장 "Administering Kafka"(pp.315–319), 쿼터 키 대조는 3장 p.74 — 인용 블록은 p.319 경고 상자 원문. 코드 펜스는 5장 p.122 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

---
type: concept
title: 설정 관리
description: AdminClient가 설정을 다루는 단위인 ConfigResource와 그 3종, 기본값이 아닌 항목만 골라내는 isDefault의 판정 기준, 설정을 바꾸는 네 가지 작업 유형, 그리고 브로커 설정 파일이 깨졌을 때 남은 브로커에서 설정을 덤프해 되살린 사례
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T15:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 설정 관리

- [설정 리소스 3종](#설정-리소스-3종)
- [기본값과 다른 것 골라내기](#기본값과-다른-것-골라내기)
- [바꾸기와 네 가지 작업 유형](#바꾸기와-네-가지-작업-유형)
- [비상시에 설정을 되살린 사례](#비상시에-설정을-되살린-사례)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애플리케이션 코드에서 토픽과 브로커의 설정을 어떤 단위로 읽고, 무엇을
기준으로 바뀐 값을 가려내고, 어떻게 고치는가.**

> **버전 조건**: Kafka 0.11 이상. 이 페이지의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021]

## 설정 리소스 3종

- **설정 관리는 `ConfigResource` 모음을 설명(describe)하고 갱신하는 방식으로 이뤄진다.** 설정
  리소스가 될 수 있는 것은 **브로커, 브로커 로거(broker logger), 토픽** 셋이다 (5장,
  p.121).[^shapira2021]
- 어느 쪽을 코드로 다루는 것이 흔한지는 갈린다 — **브로커나 브로커 로깅 설정을 확인·수정하는
  일은 보통 `kafka-config.sh` 같은 툴이나 다른 카프카 관리 도구로 하지만, 토픽 설정을 그것을
  쓰는 애플리케이션에서 확인하고 갱신하는 일은 꽤 흔하다** (5장, p.121).[^shapira2021]
  CLI 쪽 대응은 같은 책 12장 "Administering Kafka"가 다루며(12장, p.305),[^shapira2021]
  이 KB에는 아직 반입돼 있지 않다.
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

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 이 통로로 바꾸는 대표적인
  동적 설정
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 여기서 읽고 바꾸는 값들이
  원래 사는 곳
- [토픽 관리](../concepts/kafka-topic-administration.md) — 토픽 설명에는 설정이 들어 있지 않다
- [카프카 로그 압착](../concepts/kafka-log-compaction.md) — 예제가 지키려는 그 설정

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(12장 참조는 12장 "Administering Kafka" 첫 쪽) — 코드 펜스는 p.122 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

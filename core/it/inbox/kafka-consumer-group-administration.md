---
type: concept
title: 컨슈머 그룹 관리
description: AdminClient로 컨슈머 그룹을 밖에서 들여다보고 바꾸는 일 — 목록 조회에서 에러를 버리는 valid와 던지는 all의 차이, 그룹 설명에 빠져 있는 커밋 오프셋을 따로 구해 랙을 계산하는 절차, 오프셋 삭제 대신 리셋을 쓰는 이유, 활성 그룹의 오프셋을 카프카가 막는 이유, 그리고 상태를 가진 애플리케이션에서 리셋이 남기는 이중 집계
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T15:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 컨슈머 그룹 관리

- [왜 그룹을 밖에서 건드리는가](#왜-그룹을-밖에서-건드리는가)
- [그룹 열거하기](#그룹-열거하기)
- [그룹 설명과 거기 빠져 있는 것](#그룹-설명과-거기-빠져-있는-것)
- [커밋 오프셋과 랙 구하기](#커밋-오프셋과-랙-구하기)
- [그룹 수정하기](#그룹-수정하기)
- [오프셋 리셋이 걸리는 두 곳](#오프셋-리셋이-걸리는-두-곳)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애플리케이션 밖에서 컨슈머 그룹과 그 그룹이 커밋한 오프셋을 어떻게 조회하고
바꾸며, 그 조작이 걸리는 곳은 어디인가.**

> **버전 조건**: Kafka 0.11 이상. 이 페이지의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021]

## 왜 그룹을 밖에서 건드리는가

- **대부분의 메시지 큐와 달리 카프카는 데이터가 앞서 소비되고 처리된 것과 정확히 같은 순서로
  재처리하는 것을 허용한다** (5장, p.123).[^shapira2021] 그 성질의 근거는
  [토픽과 파티션](../concepts/topics-and-partitions.md)에 있다.
- 다만 컨슈머 API로 되감는 것은 조건이 붙는다 — **컨슈머 API로 오래된 메시지를 다시 읽으려면
  재처리 능력을 미리 애플리케이션에 프로그램해 넣었어야 하고, 애플리케이션 자신이
  "재처리" 기능을 노출해야** 한다 (5장, p.123).[^shapira2021] 컨슈머 쪽 되감기는
  [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md)에 있다.
- **그 능력이 애플리케이션에 내장돼 있지 않더라도 재처리를 일으키고 싶은 시나리오가 여럿**
  있다 — **인시던트 도중 오작동하는 애플리케이션을 트러블슈팅하는 경우가 하나이고, 재해 복구
  장애 조치 상황에서 애플리케이션을 새 클러스터에서 돌리도록 준비하는 경우가 또
  하나**다 (5장, p.123).[^shapira2021] 두 번째 상황의 전모는
  [카프카 클러스터 장애 조치](../concepts/kafka-cluster-failover.md)에 있다.
- 같은 작업을 하는 외부 툴은 같은 책 12장 "Administering Kafka"가 다루며 (12장,
  p.305),[^shapira2021] 이 KB에는 아직 반입돼 있지 않다. 이 페이지는 API 각도만 담는다.

## 그룹 열거하기

- 시작은 목록이다 — **`admin.listConsumerGroups().valid().get()`** (5장,
  p.123).[^shapira2021]
- **`valid()` 메서드를 쓰면 `get()`이 리턴하는 모음에는 클러스터가 에러 없이 리턴한 컨슈머
  그룹만 담긴다. 에러는 예외로 던져지는 것이 아니라 완전히 무시된다. `errors()` 메서드로 모든
  예외를 얻을 수 있다** (5장, pp.123–124).[^shapira2021]
- **다른 예제들처럼 `all()`을 쓰면 클러스터가 리턴한 첫 에러만 예외로 던져진다** (5장,
  p.124).[^shapira2021]
- **그런 에러의 있음직한 원인은 그룹을 볼 권한이 없는 인가(authorization) 문제이거나, 일부
  컨슈머 그룹의 코디네이터를 쓸 수 없는 경우**다 (5장, p.124).[^shapira2021] 코디네이터가
  무엇인지는
  [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md)에 있다.

## 그룹 설명과 거기 빠져 있는 것

- **일부 그룹에 대해 더 많은 정보를 원하면 `describeConsumerGroups`로 설명할 수 있다** —
  `describedGroups()`에서 그룹 이름으로 `ConsumerGroupDescription`을 꺼낸다 (5장,
  p.124).[^shapira2021]
- **그 설명에는 그룹에 대한 풍부한 정보가 담긴다 — 그룹 멤버들, 멤버의 식별자와 호스트,
  멤버에 배정된 파티션, 배정에 쓰인 알고리즘, 그리고 그룹 코디네이터의 호스트다. 컨슈머
  그룹을 트러블슈팅할 때 매우 유용**하다 (5장, p.124).[^shapira2021] 배정 알고리즘 자체는
  [컨슈머 설정](../concepts/kafka-consumer-configuration.md)에 있다.
- 그런데 **컨슈머 그룹에 대한 가장 중요한 정보 중 하나가 이 설명에서 빠져 있다 — 그룹이
  소비 중인 각 파티션에 대해 마지막으로 커밋한 오프셋이 무엇이고 로그의 최신 메시지에서 얼마나
  뒤처져 있는지**는 필연적으로 알고 싶어지는 것이다 (5장, p.124).[^shapira2021]
- **과거에 이 정보를 얻는 유일한 방법은 컨슈머 그룹이 내부 카프카 토픽에 쓴 커밋 메시지를
  파싱하는 것이었다. 이 방법은 의도한 바를 이루긴 했지만 카프카가 내부 메시지 포맷의 호환성을
  보장하지 않으므로 그 옛 방법은 권장되지 않는다** (5장, p.124).[^shapira2021]

## 커밋 오프셋과 랙 구하기

- 대신 AdminClient가 두 메서드를 조합해 답을 준다 (5장, p.124):[^shapira2021]
  - **`listConsumerGroupOffsets(CONSUMER_GROUP).partitionsToOffsetAndMetadata()`가 그 컨슈머
    그룹이 다루는 모든 토픽과 파티션의 맵과 각각에 대해 마지막으로 커밋된 오프셋을 준다.**
    **`describeConsumerGroups`와 달리 `listConsumerGroupOffsets`는 컨슈머 그룹 하나만 받고
    모음은 받지 않는다.**
  - **결과의 토픽·파티션마다 파티션의 마지막 메시지 오프셋을 얻고 싶다면 `listOffsets`를
    쓴다.** **`OffsetSpec`에는 매우 편리한 구현이 셋 있다 — `earliest()`·`latest()`·
    `forTimestamp()`이며, 파티션의 가장 이른 오프셋과 최신 오프셋, 그리고 지정한 시각에 또는
    그 직후에 쓰인 레코드의 오프셋을 얻게 해 준다.**
- **끝으로 모든 파티션을 순회하며 파티션마다 마지막으로 커밋된 오프셋, 파티션의 최신 오프셋,
  그리고 그 둘 사이의 랙(lag)을 출력한다** (5장, p.124).[^shapira2021] 즉 랙은 **최신 오프셋
  빼기 커밋된 오프셋**이며, 책의 예제는 그것을 `records behind`로 찍는다 (5장,
  p.125).[^shapira2021]

## 그룹 수정하기

- **AdminClient에는 컨슈머 그룹을 수정하는 메서드들도 있다 — 그룹 삭제, 멤버 제거, 커밋된
  오프셋 삭제, 오프셋 수정이다. 이것들은 SRE가 비상 상황에서 복구하기 위한 임시 도구를 만들 때
  흔히 쓴다** (5장, p.125).[^shapira2021]
- **그중 오프셋 수정이 가장 유용하다** (5장, p.125).[^shapira2021]
- **오프셋 삭제는 컨슈머를 "처음부터" 시작시키는 단순한 방법처럼 보이지만 실제로는 컨슈머
  설정에 달려 있다 — 컨슈머가 시작했는데 오프셋이 없으면 맨 앞에서 시작할까, 최신 메시지로
  건너뛸까? `auto.offset.reset` 값을 갖고 있지 않으면 알 수 없다** (5장,
  p.125).[^shapira2021] 그 설정은
  [컨슈머 설정](../concepts/kafka-consumer-configuration.md)에 있다.
- **커밋된 오프셋을 가장 이른 사용 가능 오프셋으로 명시적으로 수정하면 컨슈머가 토픽 맨
  앞에서부터 처리를 시작하도록 강제하게 되고, 본질적으로 컨슈머를 "리셋"시킨다** (5장,
  p.125).[^shapira2021] 그 형태가 아래이며, `listOffsets`·`alterConsumerGroupOffsets`·
  `UnknownMemberIdException`으로 찾는다 (5장, p.126):[^shapira2021]

  ```java
  Map<TopicPartition, ListOffsetsResult.ListOffsetsResultInfo> earliestOffsets =
      admin.listOffsets(requestEarliestOffsets).all().get();

  Map<TopicPartition, OffsetAndMetadata> resetOffsets = new HashMap<>();
  for (Map.Entry<TopicPartition, ListOffsetsResult.ListOffsetsResultInfo> e:
          earliestOffsets.entrySet()) {
    resetOffsets.put(e.getKey(), new OffsetAndMetadata(e.getValue().offset()));
  }

  try {
    admin.alterConsumerGroupOffsets(CONSUMER_GROUP, resetOffsets).all().get();
  } catch (ExecutionException e) {
    System.out.println("Failed to update the offsets committed by group "
          + CONSUMER_GROUP + " with error " + e.getMessage());
    if (e.getCause() instanceof UnknownMemberIdException)
      System.out.println("Check if consumer group is still active.");
  }
  ```

- 이 예제의 각 지점이 하는 일 (5장, p.126):[^shapira2021]
  - **컨슈머 그룹이 가장 이른 오프셋에서부터 처리를 시작하도록 리셋하려면 먼저 가장 이른
    오프셋들을 얻어야 한다. 가장 이른 오프셋을 얻는 방법은 최신 오프셋을 얻는 것과 같다.**
  - **이 루프는 `listOffsets`가 리턴한 `ListOffsetsResultInfo` 값들의 맵을,
    `alterConsumerGroupOffsets`가 요구하는 `OffsetAndMetadata` 값들의 맵으로 변환한다.**
  - **`alterConsumerGroupOffsets`를 부른 뒤 `Future`가 완료되기를 기다려 성공적으로 완료됐는지
    확인한다.**
  - **`alterConsumerGroupOffsets`가 실패하는 가장 흔한 원인은 컨슈머 그룹을 먼저 멈추지 않은
    것이다.** **이 일은 컨슈밍 애플리케이션을 직접 셧다운해서 해야 한다 — 컨슈머 그룹을
    셧다운시키는 어드민 명령은 없다.** **그룹이 여전히 활성이면, 오프셋을 수정하려는 시도는
    그룹의 멤버가 아닌 클라이언트가 그 그룹에 오프셋을 커밋하는 것처럼 컨슈머 코디네이터에게
    보인다. 이 경우 `UnknownMemberIdException`을 받게 된다.**

## 오프셋 리셋이 걸리는 두 곳

- **첫째, 오프셋 토픽에서 오프셋이 바뀌어도 컨슈머 그룹은 갱신을 통보받지 않는다. 컨슈머는
  새 파티션을 배정받을 때나 시동할 때만 오프셋을 읽는다.** **컨슈머가 알지 못한 채(따라서
  덮어써 버릴) 오프셋 변경을 하지 못하도록, 카프카는 컨슈머 그룹이 활성인 동안 오프셋 수정을
  막는다** (5장, p.125).[^shapira2021] 파티션 배정이 언제 일어나는지는
  [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md)에 있다.
- **둘째, 컨슈머 애플리케이션이 상태를 유지한다면(대부분의 스트림 처리 애플리케이션이 상태를
  유지한다) 오프셋을 리셋해 컨슈머 그룹이 토픽 맨 앞에서부터 처리하게 만드는 것이 저장된
  상태에 이상한 영향을 줄 수 있다** (5장, p.125).[^shapira2021]
  - 책의 예 — **매장에서 팔린 신발 수를 계속 세는 스트림 애플리케이션이 있고, 오전 8시에 입력에
    에러가 있었음을 발견해 오전 3시 이후의 집계를 완전히 다시 계산하고 싶다고 하자. 저장된
    집계를 적절히 수정하지 않고 오프셋만 오전 3시로 리셋하면 오늘 팔린 신발을 전부 두 번 세게
    된다**(오전 3시와 8시 사이의 데이터도 다시 처리하게 되지만, 에러를 바로잡으려면 그것이
    필요하다고 치자) (5장, pp.125–126).[^shapira2021]
  - **그러므로 저장된 상태도 그에 맞게 갱신해야 한다. 개발 환경에서는 보통 입력 토픽의 시작으로
    오프셋을 리셋하기 전에 상태 저장소를 통째로 삭제한다** (5장, p.126).[^shapira2021]

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 여기서
  설명하고 리셋하는 그 그룹의 내부 절차
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 컨슈머가 스스로 커밋하고
  되감는 쪽
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — `auto.offset.reset`과 파티션
  할당 전략
- [카프카 클러스터 장애 조치](../concepts/kafka-cluster-failover.md) — 그룹 오프셋을 손으로
  옮기게 되는 대표 상황
- [설정 관리](../concepts/kafka-config-administration.md) — 같은 클라이언트로 하는 설정 쪽 작업

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(12장 참조는 12장 "Administering Kafka" 첫 쪽) — 코드 펜스는 p.126 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

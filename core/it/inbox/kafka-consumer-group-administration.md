---
type: concept
title: 컨슈머 그룹 관리
description: 컨슈머 그룹을 밖에서 들여다보고 바꾸는 일을 코드와 명령줄 양쪽에서 — 목록 조회에서 에러를 버리는 valid와 던지는 all의 차이, 그룹 설명에 빠져 있는 커밋 오프셋을 따로 구해 랙을 계산하는 절차, 오프셋 삭제 대신 리셋을 쓰는 이유, 활성 그룹의 오프셋을 카프카가 막는 이유, kafka-consumer-groups.sh의 출력 필드와 그룹 삭제 조건, 그리고 오프셋을 CSV로 내보내고 다시 넣는 절차
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
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
- [명령줄에서 그룹 조회하기](#명령줄에서-그룹-조회하기)
- [그룹 삭제하기](#그룹-삭제하기)
- [오프셋 내보내기와 가져오기](#오프셋-내보내기와-가져오기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애플리케이션 밖에서 컨슈머 그룹과 그 그룹이 커밋한 오프셋을 코드와 명령줄에서
어떻게 조회하고 바꾸며, 그 조작이 걸리는 곳은 어디인가.**

> **버전 조건**: Kafka 0.11 이상 — **아래 API 절들**의 작업은 전부
> [어드민 클라이언트](../concepts/kafka-adminclient.md)를 통하며, 그 API는 0.11에서
> 추가됐다 (5장, p.113).[^shapira2021] 명령줄 절의 `kafka-consumer-groups.sh`에는 이 조건이
> 걸리지 않는다.

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
- 같은 작업을 하는 외부 도구는 같은 책 12장이 다루며, 그 절차는
  [아래 명령줄 절](#명령줄에서-그룹-조회하기)에 있다 (12장, p.312).[^shapira2021]

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

## 명령줄에서 그룹 조회하기

- 도구는 하나다 — **`kafka-consumer-groups.sh`는 클러스터에서 토픽을 소비 중인 컨슈머 그룹을
  관리하고 그에 대한 통찰을 얻게 해 주며, 그룹 목록 조회·특정 그룹 설명·컨슈머 그룹이나 특정
  그룹 정보 삭제·컨슈머 그룹 오프셋 정보 리셋에 쓸 수 있다** (12장, p.312).[^shapira2021]
  이 도구를 쓰기 전에 확인할 것은
  [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md)에 있다.
- 옛 스크립트에 남아 있는 함정이 하나 있다 (12장, p.312):[^shapira2021]
  - 버전 조건: Kafka 0.11.0 이상 — **옛 버전에서는 컨슈머 그룹을 주키퍼에서 관리·유지할 수
    있었지만 그 동작은 0.11.0.* 이후 버전에서 지원 중단됐고 옛 컨슈머 그룹은 더 이상 쓰이지
    않는다.**
  - **제공되는 스크립트의 일부 버전은 여전히 지원 중단된 `--zookeeper` 접속 문자열 명령을 보여
    줄 수 있지만, 나중 버전으로 업그레이드되지 않은 컨슈머 그룹이 있는 오래된 환경이 아니라면
    쓰는 것을 권장하지 않는다** (12장, p.312).[^shapira2021] 주키퍼가 어떤 순서로 물러났는지는
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)에 있다.
- 목록은 `--bootstrap-server`와 `--list`다. **이 스크립트를 쓰는 임시(ad hoc) 컨슈머는 목록에
  `console-consumer-<generated_id>` 꼴로 나타난다** (12장, p.312).[^shapira2021] 그 임시
  컨슈머의 정체는
  [콘솔 프로듀서와 콘솔 컨슈머](../concepts/kafka-console-producer-and-consumer.md)에 있다.
- 상세는 **`--list`를 `--describe`로 바꾸고 `--group` 매개변수를 더하는 것**이며, **그룹이
  소비 중인 모든 토픽과 파티션, 그리고 각 토픽 파티션의 오프셋 같은 추가 정보를 나열**한다
  (12장, p.312).[^shapira2021]
- 출력 필드는 아홉이고 책이 표 12-1로 정의한다 (12장, p.313):[^shapira2021]
  - `GROUP`·`TOPIC`·`PARTITION` — **컨슈머 그룹 이름, 소비 중인 토픽 이름, 소비 중인 파티션의
    ID.**
  - `CURRENT-OFFSET` — **이 토픽 파티션에 대해 컨슈머 그룹이 다음에 소비할 오프셋. 파티션 안
    컨슈머의 위치다.**
  - `LOG-END-OFFSET` — **브로커가 가진 그 토픽 파티션의 현재 하이 워터마크 오프셋. 이
    파티션에 생산될 다음 메시지의 오프셋이다.**
  - `LAG` — **이 토픽 파티션에 대한 컨슈머의 `CURRENT-OFFSET`과 브로커의 `LOG-END-OFFSET`의
    차이.** 코드로 같은 값을 구하는 절차가 [위 절](#커밋-오프셋과-랙-구하기)이다.
  - `CONSUMER-ID`·`HOST`·`CLIENT-ID` — **주어진 client-id를 바탕으로 생성된 고유
    consumer-id, 컨슈머 그룹이 읽고 있는 호스트의 주소, 그룹에서 소비 중인 클라이언트를
    식별하는 문자열.**

## 그룹 삭제하기

- **`--delete` 인자로 컨슈머 그룹을 삭제할 수 있고, 이것은 그룹이 소비 중인 모든 토픽에 대해
  저장된 모든 오프셋을 포함해 그룹 전체를 제거**한다 (12장, p.313).[^shapira2021]
- 조건이 하나 붙는다 — **이 작업을 하려면 그룹의 모든 컨슈머가 셧다운돼 있어야 하고 컨슈머
  그룹에 활성 멤버가 없어야 한다. 비어 있지 않은 그룹을 지우려 하면 "The group is not empty"
  에러가 던져지고 아무 일도 일어나지 않는다** (12장, p.313).[^shapira2021] 이 제약이 왜
  존재하는지는 [위의 리셋 절](#오프셋-리셋이-걸리는-두-곳)과 같은 이유다.
- 부분 삭제도 된다 — **같은 명령에 `--topic` 인자로 어느 토픽의 오프셋을 지울지 지정하면 그룹
  전체를 지우지 않고 그룹이 소비 중인 토픽 하나의 오프셋만 삭제**할 수 있다 (12장,
  p.313).[^shapira2021]

## 오프셋 내보내기와 가져오기

- 왜 필요한가 — **컨슈머 그룹의 오프셋을 표시하고 삭제하는 것 말고도 오프셋을 가져와 새
  오프셋을 일괄로 저장하는 것이 가능하다. 메시지를 다시 읽어야 하는 문제가 생겨 오프셋을
  리셋할 때, 또는 컨슈머가 처리하지 못하는 메시지(형식이 깨진 메시지 같은)를 건너뛰려고 오프셋을
  앞으로 옮길 때 유용**하다 (12장, p.314).[^shapira2021]
- 내보내기는 **`--reset-offsets` 인자와 `--dry-run` 옵션**을 함께 쓴다 — **현재 오프셋을 나중에
  가져오거나 롤백하는 데 재사용할 수 있는 파일 형식으로 내보낼 수 있게 해 주며**, CSV 형식은
  `<topic-name>,<partition-number>,<offset>`이다 (12장, p.314).[^shapira2021]
  - **`--dry-run` 없이 같은 명령을 실행하면 오프셋이 완전히 리셋되므로 주의**한다 (12장,
    p.314).[^shapira2021]
  - 책의 예는 `--export --group my-consumer --topic my-topic --reset-offsets --to-current
    --dry-run > offsets.csv` 꼴로 파일에 흘려보낸다 (12장, p.314).[^shapira2021]
- 가져오기는 **내보내기의 반대로, 앞 절에서 만든 파일을 받아 컨슈머 그룹의 현재 오프셋을
  설정**한다. **흔한 관행은 현재 오프셋을 내보내고, 백업을 위해 파일을 복사해 둔 뒤, 사본을
  편집해 원하는 값으로 바꾸는 것**이다 (12장, pp.314–315).[^shapira2021] 실행은
  `--reset-offsets --group my-consumer --from-file offsets.csv --execute`이고 결과는
  `TOPIC`·`PARTITION`·`NEW-OFFSET` 표로 찍힌다 (12장, p.315).[^shapira2021]
- 여기에도 경고 상자가 붙는데, API 쪽이 예외로 막는 그 일을 CLI에서는 조용히 잃는다는 점이
  중요하다 (12장, p.315):[^shapira2021]

  > Before performing this step, it is important that all consumers in the group are stopped.
  > They will not read the new offsets if they are written while the consumer group is active.
  > The consumers will just overwrite the imported offsets.

## 이어지는 페이지

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 이 작업들을 실어 나르는
  클라이언트의 설계와 수명주기
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) —
  `kafka-consumer-groups.sh`가 속한 도구 모음의 전제와 경고
- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 여기서
  설명하고 리셋하는 그 그룹의 내부 절차
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 컨슈머가 스스로 커밋하고
  되감는 쪽
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — `auto.offset.reset`과 파티션
  할당 전략
- [콘솔 프로듀서와 콘솔 컨슈머](../concepts/kafka-console-producer-and-consumer.md) — 오프셋
  토픽을 직접 열어 보는 쪽, 그리고 목록에 보이는 임시 컨슈머의 출처
- [카프카 클러스터 장애 조치](../concepts/kafka-cluster-failover.md) — 그룹 오프셋을 손으로
  옮기게 되는 대표 상황
- [설정 관리](../concepts/kafka-config-administration.md) — 같은 클라이언트로 하는 설정 쪽 작업

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically"(pp.123–126)와 12장 "Administering Kafka"(pp.312–315) — 인용 블록은 p.315 경고 상자 원문. 코드 펜스는 5장 p.126 예제에서 원문의 주석 번호 표식만 덜어냈다(보탠 줄 없음)

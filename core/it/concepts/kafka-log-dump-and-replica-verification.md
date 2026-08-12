---
type: concept
title: 로그 세그먼트 덤프와 레플리카 검증
description: 소비하지 않고 브로커 디스크를 직접 들여다보는 두 도구 — 포이즌 필 메시지를 열어 보는 로그 세그먼트 덤프와 그것이 찍어 주는 배치 메타데이터, 인덱스 손상을 검사하는 두 단계 옵션, 그리고 레플리카들이 서로 같은지 확인하는 검증 도구와 그것이 클러스터에 지우는 부담
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 로그 세그먼트 덤프와 레플리카 검증

- [왜 소비하지 않고 파일을 여는가](#왜-소비하지-않고-파일을-여는가)
- [세그먼트가 놓인 자리와 기본 출력](#세그먼트가-놓인-자리와-기본-출력)
- [내용물까지 보기](#내용물까지-보기)
- [인덱스 검사](#인덱스-검사)
- [레플리카 검증](#레플리카-검증)
- [이 도구가 클러스터에 지우는 부담](#이-도구가-클러스터에-지우는-부담)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **브로커 디스크에 실제로 무엇이 쓰여 있는지 소비하지 않고 어떻게 열어 보고,
레플리카들이 서로 같은지 어떻게 확인하는가.**

## 왜 소비하지 않고 파일을 여는가

- 동기는 컨슈머가 처리하지 못하는 메시지다 — **특정 메시지의 내용을 읽어야 할 때가 이따금
  있는데, 손상된 "포이즌 필(poison pill)" 메시지가 토픽에 들어와 컨슈머가 처리하지 못하게 된
  경우가 그렇다** (12장, p.332).[^shapira2021]
- 그 일에 `kafka-dump-log.sh`가 있다 — **파티션의 로그 세그먼트를 해독하도록 제공되는
  도구이며, 메시지를 소비하고 해독하지 않고도 개별 메시지를 볼 수 있게 해 준다. 인자로 로그
  세그먼트 파일의 쉼표 구분 목록을 받아 메시지 요약 정보나 상세 메시지 데이터를 출력**한다
  (12장, p.332).[^shapira2021]

## 세그먼트가 놓인 자리와 기본 출력

- 파일을 찾으려면 데이터 디렉터리를 알아야 한다 — 책의 설치에서는 **카프카 데이터 디렉터리가
  `/tmp/kafka-logs`에 있고, 따라서 로그 세그먼트를 찾을 자리는
  `/tmp/kafka-logs/<topic-name>-<partition>`**, 예에서는 `/tmp/kafka-logs/my-topic-0/`다 (12장,
  p.332).[^shapira2021] 그 디렉터리 목록을 정하는 설정과 세그먼트가 파일로 끊기는 규칙은
  [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
- 호출은 `kafka-dump-log.sh --files /tmp/kafka-logs/my-topic-0/00000000000000000000.log` 형태이며,
  **먼저 메시지 내용은 찍지 않고 각 메시지의 기본 메타데이터만 가져오는** 쓰임이 이것이다
  (12장, p.332).[^shapira2021]
- 그 출력이 배치 단위로 찍어 주는 것들 — `baseOffset`·`lastOffset`·`count`·`baseSequence`·
  `lastSequence`·`producerId`·`producerEpoch`·`partitionLeaderEpoch`·`isTransactional`·
  `isControl`·`position`·`CreateTime`·`size`·`magic`·`compresscodec`·`crc`·`isvalid` (12장,
  p.332).[^shapira2021]
  - 이 필드들이 왜 배치 단위인지는
    [카프카 메시지 배치 스키마](../concepts/kafka-message-batch-schema.md)에,
    `producerId`·`isTransactional`·`isControl`이 무엇을 표시하는지는
    [카프카 트랜잭션 내부 구조](../concepts/kafka-transaction-internals.md)에 있다.

## 내용물까지 보기

- **`--print-data-log` 옵션을 더하면 실제 페이로드 정보와 그 이상을 준다** (12장,
  p.333).[^shapira2021] 이때 배치 아래에 메시지별로 `offset`·`CreateTime`·`keysize`·
  `valuesize`·`sequence`·`headerKeys`·`payload`가 한 줄씩 붙는다 (12장,
  p.333).[^shapira2021] `headerKeys`가 어디서 오는지는
  [단일 메시지 변환](../concepts/kafka-single-message-transformations.md)에 있다.

## 인덱스 검사

- 이 도구에는 **로그 세그먼트에 딸린 인덱스 파일을 검증하는 것 같은 유용한 옵션이 몇 개 더**
  있다 (12장, p.333).[^shapira2021]
- 왜 검증이 필요한지 — **인덱스는 로그 세그먼트 안에서 메시지를 찾는 데 쓰이며, 손상되면
  소비 시 에러를 일으킨다. 브로커가 언클린 상태로(즉 정상적으로 멈추지 않은 채) 시동할 때마다
  검증이 수행되지만, 손으로 돌릴 수도** 있다 (12장, p.333).[^shapira2021] 인덱스 파일 자체는
  [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
- 얼마나 검사할지에 따라 옵션이 둘이다 (12장, p.333):[^shapira2021]
  - `--index-sanity-check` — **인덱스가 쓸 수 있는 상태인지만 확인한다.**
  - `--verify-index-only` — **인덱스 항목을 전부 출력하지 않으면서 인덱스의 불일치를 확인한다.**
- 하나 더 — **`--value-decoder-class`는 디코더를 넘겨 직렬화된 메시지를 역직렬화하게 해
  준다** (12장, p.333).[^shapira2021]

## 레플리카 검증

- 전제부터 본다 — **파티션 복제는 보통의 카프카 컨슈머 클라이언트와 비슷하게 동작한다.
  팔로워 브로커가 가장 오래된 오프셋에서 복제를 시작하고 현재 오프셋을 주기적으로 디스크에
  체크포인트한다. 복제가 멈췄다 다시 시작하면 마지막 체크포인트부터 이어 간다** (12장,
  p.334).[^shapira2021] 그 복제 절차는
  [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md)에 있다.
- 그리고 구멍이 생길 수 있다 — **이전에 복제된 로그 세그먼트가 브로커에서 삭제되는 일이
  가능하고, 이 경우 팔로워는 그 구멍을 메우지 않는다** (12장, p.334).[^shapira2021]
- 그래서 **토픽 파티션의 레플리카들이 클러스터 전체에서 같은지 확인하려면
  `kafka-replica-verification.sh` 도구를 쓴다.** 하는 일은 **주어진 토픽 파티션 집합에 대해 모든
  레플리카에서 메시지를 페치해 모든 메시지가 모든 레플리카에 있는지 확인하고, 주어진 파티션들의
  최대 랙(max lag)을 출력하는 것**이다 (12장, p.334).[^shapira2021]
- 사용 조건 둘 — **이 과정은 취소될 때까지 루프를 돌며 계속 동작하고**, 그러려면 **붙을
  브로커의 명시적인 쉼표 구분 목록을 줘야** 한다. **기본적으로 모든 토픽이 검증 대상이지만,
  검증하려는 토픽에 매칭되는 정규식을 줄 수도** 있다 (12장, p.334).[^shapira2021] 아래가
  브로커 둘에 대해 `my`로 시작하는 토픽을 검증하는 형태이며,
  `kafka-replica-verification.sh`·`--broker-list`·`--topic-white-list`로 찾는다 (12장,
  p.334):[^shapira2021]

  ```sh
  kafka-replica-verification.sh --broker-list kafka.host1.domain.com:9092,kafka.host2.domain.com:9092 --topic-white-list 'my.*'
  ```

  - 출력은 **`max lag is 0 for partition my-topic-0 at offset 4 among 1 partitions`** 꼴로
    주기적으로 반복된다 (12장, p.334).[^shapira2021]

## 이 도구가 클러스터에 지우는 부담

- 이 도구는 읽기 전용인데도 위험 표시가 붙어 있다. 원문 그대로 옮긴다 (12장,
  p.334):[^shapira2021]

  > The replica verification tool will have an impact on your cluster similar to reassigning
  > partitions, as it must read all messages from the oldest offset in order to verify the
  > replica. In addition, it reads from all replicas for a partition in parallel, so it should
  > be used with caution.

  - 비교 대상인 재할당의 부담은
    [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md)에 있다.

## 이어지는 페이지

- [카프카 물리적 저장소](../concepts/kafka-physical-storage.md) — 여기서 여는 그 파일들이
  만들어지는 규칙과 인덱스의 정체
- [카프카 메시지 배치 스키마](../concepts/kafka-message-batch-schema.md) — 덤프 출력의 필드가
  그대로 나오는 곳
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 레플리카 검증이 확인하려는
  그 복제의 정상 동작
- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — 이 도구들이 속한 모음
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 검증이
  아니라 실제로 레플리카를 옮기는 쪽
- [카프카 트랜잭션 내부 구조](../concepts/kafka-transaction-internals.md) — 덤프에 보이는
  `isTransactional`·`isControl`의 의미

[^shapira2021]: Shapira et al. 2021, 12장 "Administering Kafka" — 인용 블록은 p.334 경고 상자 원문. 코드 펜스는 p.334 예제에서 셸 프롬프트와 출력을 덜어내고, 지면에서 두 줄로 줄바꿈된 한 명령을 한 줄로 이었다(보탠 문자 없음)

---
type: concept
title: 카프카 브로커 지표
description: 브로커에서 상시로 읽는 지표들의 이름과 의미와 경보 문턱 — 컨트롤러가 하나뿐인지 보는 두 지표, 부하의 대표값인 요청 핸들러 유휴 비율, 유입·유출·메시지 속도 지표와 속도 지표가 갖는 일곱 속성, 파티션 수와 리더 수와 오프라인 파티션, 요청 종류마다의 여덟 지표와 백분위수, 그리고 토픽별·파티션별 지표
generated: { by: "claude-opus-5", at: "2026-08-12T22:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 브로커 지표

- [무엇을 대시보드에 올리는가](#무엇을-대시보드에-올리는가)
- [컨트롤러가 하나뿐인지 보는 두 지표](#컨트롤러가-하나뿐인지-보는-두-지표)
- [요청 핸들러 유휴 비율](#요청-핸들러-유휴-비율)
- [처리량 지표 셋과 속도 지표의 속성](#처리량-지표-셋과-속도-지표의-속성)
- [파티션 수·리더 수·오프라인 파티션](#파티션-수리더-수오프라인-파티션)
- [요청 지표](#요청-지표)
- [토픽별·파티션별 지표](#토픽별파티션별-지표)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **브로커에서 어떤 지표를 어떤 이름으로 읽고, 그 값이 얼마일 때 문제인가.**

## 무엇을 대시보드에 올리는가

- **카프카 브로커 지표는 많다. 다수는 개발자가 특정 이슈를 조사하다가, 또는 나중에 디버깅에
  필요할 것을 예상해 추가한 저수준 측정값이다. 브로커 안 거의 모든 기능에 대한 지표가 있지만,
  가장 흔한 것들이 카프카를 매일 돌리는 데 필요한 정보를 준다** (13장, p.346).[^shapira2021]
- 이 목록의 성격 — **브로커 지표의 전수 목록이 아니라 브로커와 클러스터의 건강을 확인하는 데
  "반드시 있어야 할" 지표 몇 가지**다 (13장, p.347).[^shapira2021]
- 불완전 복제 파티션 말고도 **브로커 수준에 있는 다른 지표들을 모니터링해야 하며, 전부에 경보
  문턱을 걸 마음이 들지 않더라도 브로커와 클러스터에 대한 값진 정보를 준다. 만드는 모니터링
  대시보드에는 이것들이 있어야 한다** (13장, p.354).[^shapira2021] 불완전 복제 파티션 자체를
  읽는 법은 [카프카 클러스터 문제 진단](../concepts/kafka-cluster-problem-diagnosis.md)에 있다.

## 컨트롤러가 하나뿐인지 보는 두 지표

- **활성 컨트롤러 수(active controller count) 지표는 그 브로커가 현재 클러스터의
  컨트롤러인지를 가리킨다. 값은 0 아니면 1이고 1이면 그 브로커가 현재 컨트롤러**다 (13장,
  p.354).[^shapira2021]

  | 항목 | 값 |
  |---|---|
  | Metric name | Active controller count |
  | JMX MBean | `kafka.controller:type=KafkaController,name=ActiveControllerCount` |
  | Value range | Zero or one |

  (13장, p.354, 표 13-5)[^shapira2021]

- 정상 조건은 양방향이다 — **언제나 브로커 하나만 컨트롤러여야 하고, 클러스터에는 언제나
  브로커 하나가 반드시 컨트롤러여야 한다** (13장, p.354).[^shapira2021]
  - **둘이 자기가 컨트롤러라고 말하면 종료됐어야 할 컨트롤러 스레드가 걸려 버린 문제**이며,
    **파티션 이동 같은 관리 작업을 제대로 실행하지 못하는 문제를 일으킬 수 있다.** 해결하려면
    **적어도 그 두 브로커를 재시작**해야 하는데, **컨트롤러가 여분으로 존재할 때는 브로커의
    안전한 종료(safe shutdown)에 문제가 생기는 일이 잦아 강제 종료해야 한다** (13장,
    p.354).[^shapira2021]
  - **아무도 컨트롤러라고 주장하지 않으면 클러스터는 토픽·파티션 생성이나 브로커 장애 같은
    상태 변화에 제대로 반응하지 못한다.** **주키퍼 클러스터로부터의 네트워크 분단이 그런
    문제를 만들 수 있고**, 근본 원인을 고친 뒤에는 **컨트롤러 스레드의 상태를 초기화하기 위해
    클러스터의 모든 브로커를 재시작하는 것이 현명**하다 (13장, p.355).[^shapira2021]
- **컨트롤러 큐 크기(controller queue size) 지표는 컨트롤러가 브로커들을 위해 처리하기를
  기다리고 있는 요청이 몇 개인지를 가리킨다** (13장, p.355).[^shapira2021]

  | 항목 | 값 |
  |---|---|
  | Metric name | Controller queue size |
  | JMX MBean | `kafka.controller:type=ControllerEventManager,name=EventQueueSize` |
  | Value range | Integer, zero or more |

  (13장, p.355, 표 13-6)[^shapira2021]

- 읽는 법 — **값은 0 이상이고 브로커에서 새 요청이 들어오고 파티션 생성·이동·리더 변경 처리
  같은 관리 작업이 일어나면서 자주 출렁인다. 스파이크는 예상된 것이지만 값이 계속 증가하거나
  높은 값에서 내려오지 않고 유지되면 컨트롤러가 걸렸을 수 있다는 뜻**이다 (13장,
  p.355).[^shapira2021]
  - 해결책은 **컨트롤러를 다른 브로커로 옮기는 것**이고 그러려면 **현재 컨트롤러인 브로커를
    내려야 한다. 다만 컨트롤러가 걸렸을 때는 어느 브로커든 제어된 종료(controlled shutdown)에
    문제가 생기는 일이 잦다** (13장, p.355).[^shapira2021] 그 상황에서 손으로 컨트롤러를
    옮기는 방법은 [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md)에 있다.

## 요청 핸들러 유휴 비율

- **카프카는 모든 클라이언트 요청 처리에 스레드 풀 둘을 쓴다 — 네트워크 스레드와 요청 핸들러
  스레드(I/O 스레드라고도 부른다)** (13장, p.355).[^shapira2021]
  - **네트워크 스레드는 네트워크 너머 클라이언트로 데이터를 읽고 쓰는 일을 맡는다. 큰 처리를
    요구하지 않으므로 네트워크 스레드 고갈은 덜 걱정할 문제**다.
  - **요청 핸들러 스레드는 클라이언트 요청 자체를 처리하는 일을 맡고 여기에는 메시지를
    디스크에 읽고 쓰는 것이 들어간다. 그래서 브로커에 부하가 커질수록 이 스레드 풀에 큰 영향이
    간다.**

  | 항목 | 값 |
  |---|---|
  | Metric name | Request handler average idle percentage |
  | JMX MBean | `kafka.server:type=KafkaRequestHandlerPool,name=RequestHandlerAvgIdlePercent` |
  | Value range | Float, between zero and one inclusive |

  (13장, p.356, 표 13-7)[^shapira2021]

- 값의 해석과 경보 문턱 (13장, p.356):[^shapira2021]

  > The request handler idle ratio metric indicates the percentage of time the request
  > handlers are not in use. The lower this number, the more loaded the broker is.
  > Experience tells us that idle ratios lower than 20% indicate a potential problem, and
  > lower than 10% is usually an active performance problem.

- 클러스터가 작아서가 아니라면 이 풀의 이용률이 높은 이유는 둘이다 (13장,
  p.356):[^shapira2021]
  - **풀에 스레드가 부족한 것.** **일반적으로 요청 핸들러 스레드 수는 시스템의 프로세서
    수(하이퍼스레딩 프로세서 포함)와 같게 잡아야 한다.**
  - **스레드가 요청마다 불필요한 일을 하는 것.**
- 두 번째 이유의 실물이 메시지 형식이다 (13장, p.356):[^shapira2021]
  - **카프카 0.10 이전에는 요청 핸들러 스레드가 들어오는 모든 메시지 배치를 압축 해제하고,
    메시지를 검증하고 오프셋을 배정한 뒤, 오프셋이 붙은 메시지 배치를 다시 압축해 디스크에
    쓰는 일을 맡았다. 게다가 압축 메서드가 전부 동기 잠금 뒤에 있었다.**
  - **0.10부터는 메시지 배치 안에서 상대 오프셋을 허용하는 새 메시지 형식이 생겼다.** 그래서
    **새 프로듀서는 메시지 배치를 보내기 전에 상대 오프셋을 설정하고, 브로커는 메시지 배치의
    재압축을 건너뛸 수 있다.**
  - 그 결과 **할 수 있는 단일 성능 개선 중 가장 큰 것 하나가 모든 프로듀서·컨슈머 클라이언트가
    0.10 메시지 형식을 지원하게 하고 브로커의 메시지 형식 버전도 0.10으로 바꾸는 것**이며,
    **요청 핸들러 스레드 이용률을 크게 낮춘다.**
  - 버전 조건: Kafka 0.10 이상에서만 상대 오프셋을 쓸 수 있다 — 그 아래에서는 재압축을 피할
    수 없다. 메시지 형식 자체는
    [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md)에 있다.
- 스레드가 수백 개 필요해 보이지 않는 이유 — **실제로는 브로커의 CPU 수보다 많은 스레드를
  설정할 필요가 없다. 아파치 카프카는 요청 핸들러를 쓰는 방식이 매우 영리해서 처리에 오래
  걸릴 요청을 퍼거토리(purgatory)로 넘긴다.** 예로 드는 것이 **요청이 스로틀링되고 있을 때와
  프로듀스 요청에 하나 넘는 확인 응답이 필요할 때**다 (13장, p.356).[^shapira2021]
  - 원문 오식: 이 상자의 해당 문장이 **"when requests are being quoted"** 로 인쇄돼 있다
    (13장, p.356).[^shapira2021] 문맥상 쿼터에 의한 스로틀링을 가리킨다 —
    [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) 쪽이다.

## 처리량 지표 셋과 속도 지표의 속성

- **전체 토픽 초당 유입 바이트(all topics bytes in rate)는 브로커가 생산 클라이언트로부터 받는
  메시지 트래픽이 얼마나 되는지를 재는 데 유용**하다. **클러스터를 확장하거나 성장 관련 작업을
  해야 할 시점을 판단하기 위해 시간에 따라 추세를 보기 좋은 지표**이고, **한 브로커가 다른
  브로커보다 트래픽을 더 받고 있는지 평가해 파티션 리밸런스 필요를 알아내는 데도 유용**하다
  (13장, p.357).[^shapira2021]
- **전체 토픽 초당 유출 바이트(all topics bytes out rate)는 컨슈머가 메시지를 읽어 가는
  속도**를 보여 준다. **카프카가 다수 컨슈머를 쉽게 감당하는 능력 덕분에 유출 속도는 유입
  속도와 다르게 스케일할 수 있고, 유출이 유입의 여섯 배가 되는 카프카 배포도 많다.** 그래서
  **따로 관찰하고 추세를 보는 것이 중요**하다 (13장, p.358).[^shapira2021]
  - 셈에 포함되는 것에 주의 — **유출 바이트 속도에는 레플리카 트래픽도 들어간다. 모든 토픽의
    복제 팩터가 2라면 컨슈머 클라이언트가 없어도 유출 속도가 유입 속도와 같게 보이고, 모든
    메시지를 읽는 컨슈머 클라이언트가 하나 있으면 유출이 유입의 두 배가 된다** (13장,
    p.358).[^shapira2021]
- **전체 토픽 초당 메시지 수(all topics messages in rate)는 크기와 무관하게 초당 생산된 개별
  메시지 수**를 보여 준다. **프로듀서 트래픽을 다른 척도로 재는 성장 지표로 유용**하고,
  **유입 바이트 속도와 함께 쓰면 평균 메시지 크기를 구할 수 있다** (13장,
  p.359).[^shapira2021]
  - 짝이 없는 이유도 기록돼 있다 — **메시지 아웃 지표가 없는 것은, 메시지가 소비될 때 브로커가
    다음 배치를 컨슈머에게 그냥 보낼 뿐 안에 메시지가 몇 개인지 알아보려고 펼치지 않기
    때문**이다. **그래서 브로커는 메시지가 몇 개 나갔는지 사실 모르며, 줄 수 있는 지표는 초당
    페치 수뿐인데 그것은 메시지 개수가 아니라 요청 속도**다 (13장, p.359).[^shapira2021]

  | Name | JMX MBean | Value range |
  |---|---|---|
  | Bytes in per second | `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec` | Rates as doubles, count as integer |
  | Bytes out per second | `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec` | Rates as doubles, count as integer |
  | Messages in per second | `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec` | Rates as doubles, count as integer |

  (13장, pp.357–359, 표 13-8·13-9·13-10)[^shapira2021]

- **모든 속도 지표는 속성 일곱 개**를 갖고, **어느 것을 쓸지는 어떤 측정을 원하는지에 달렸다.
  속성들은 이벤트의 이산 개수와 여러 기간에 걸친 이벤트 수의 평균을 준다. 적절히 쓰지 않으면
  브로커에 대한 잘못된 시야를 갖게 된다** (13장, p.357).[^shapira2021]
  - 측정값이 아닌 서술 속성 둘 — **`EventType`은 모든 속성의 측정 단위이고(이 경우 "bytes"),
    `RateUnit`은 속도 속성의 기간이다(이 경우 "seconds")** (13장, p.357).[^shapira2021]
  - 세분성이 다른 속도 속성 넷 — **`OneMinuteRate`(직전 1분 평균), `FiveMinuteRate`(직전 5분),
    `FifteenMinuteRate`(직전 15분), `MeanRate`(브로커 시작 이후 평균)** (13장,
    pp.357–358).[^shapira2021]
  - 고르는 기준 — **`OneMinuteRate`는 빠르게 출렁이며 "특정 시점" 관점을 주므로 짧은 트래픽
    스파이크를 보는 데 유용하다. `MeanRate`는 거의 변하지 않고 전체 추세를 주는데, 쓸모가
    있기는 하지만 경보를 걸고 싶은 지표는 아마 아니다. `FiveMinuteRate`와
    `FifteenMinuteRate`가 둘 사이의 타협**이다 (13장, p.358).[^shapira2021]
  - **`Count` 속성은 브로커가 시작된 이후 계속 증가하는 값**이다. 유입 바이트 지표라면
    **프로세스 시작 이후 브로커에 생산된 총 바이트 수**를 뜻하며, **카운터 지표를 지원하는
    지표 시스템과 함께 쓰면 평균 속도 대신 절대적 관점을 준다** (13장,
    p.358).[^shapira2021]

## 파티션 수·리더 수·오프라인 파티션

- **브로커의 파티션 수(partition count)는 그 브로커에 할당된 전체 파티션 수이므로 대개 크게
  변하지 않는다. 리더인지 팔로워인지와 무관하게 그 브로커가 가진 모든 레플리카가 포함**된다.
  **자동 토픽 생성이 켜진 클러스터에서 모니터링이 더 흥미로운데, 토픽 생성이 클러스터
  운영자의 통제 밖에 놓이기 때문**이다 (13장, p.359).[^shapira2021]
- **리더 수(leader count)는 그 브로커가 현재 리더인 파티션 수**를 보여 준다. **다른 측정값과
  마찬가지로 클러스터의 브로커들에 걸쳐 대체로 고르게 나와야 하고, 정기적으로 확인하고
  경보까지 거는 것이 훨씬 더 중요한 지표**다 — **레플리카 수와 크기가 완벽히 균형 잡혀 있어도
  클러스터가 불균형해진 때를 알려 주기 때문**이다 (13장, pp.359–360).[^shapira2021]
  - 그 이유는 리더십이 저절로 돌아오지 않는 데 있다 — **브로커는 주키퍼 세션 만료 같은 여러
    이유로 파티션의 리더십을 놓을 수 있고, 자동 리더 리밸런싱을 켜 두지 않았다면 복구된 뒤에도
    리더십을 자동으로 되찾지 않는다.** 그런 경우 **이 지표가 더 적은 리더 수, 흔히 0을
    보여 주며 이는 선호 리더 선출을 돌려 클러스터의 리더십을 리밸런스해야 한다는 뜻**이다
    (13장, p.360).[^shapira2021]
  - 쓰는 요령 — **파티션 수와 함께 써서 그 브로커가 리더인 파티션의 비율을 보는 것이 유용**하다.
    **복제 팩터 2를 쓰는 잘 균형 잡힌 클러스터라면 모든 브로커가 자기 파티션의 약 50%에서
    리더여야 하고, 복제 팩터가 3이면 이 비율은 33%로 떨어진다** (13장,
    p.360).[^shapira2021]
- **불완전 복제 파티션 수와 함께 오프라인 파티션 수(offline partitions count)가 모니터링에
  결정적인 지표**다. **이 측정값은 클러스터의 컨트롤러인 브로커만 제공하며(다른 브로커는 전부
  0을 보고한다) 현재 리더가 없는 클러스터 안 파티션 수**를 보여 준다 (13장,
  p.360).[^shapira2021]
  - 리더가 없는 이유는 둘이다 (13장, p.360):[^shapira2021]
    - **이 파티션의 레플리카를 가진 브로커가 전부 내려간 경우.**
    - **(언클린 리더 선출이 꺼진 상태에서) 메시지 수 불일치 때문에 어떤 인-싱크 레플리카도
      리더십을 가져갈 수 없는 경우.** 그 선택지가 무엇을 맞바꾸는지는
      [언클린 리더 선출](../concepts/kafka-unclean-leader-election.md)에 있다.
  - 심각도 — **프로덕션 클러스터에서 오프라인 파티션은 프로듀서 클라이언트에 영향을 주어
    메시지를 유실시키거나 애플리케이션에 배압을 일으키고 있을 수 있다. "사이트 다운" 유형의
    문제인 경우가 가장 많으며 즉시 대응해야 한다** (13장, p.361).[^shapira2021]

  | Name | JMX MBean | Value range |
  |---|---|---|
  | Partition count | `kafka.server:type=ReplicaManager,name=PartitionCount` | Integer, zero or greater |
  | Leader count | `kafka.server:type=ReplicaManager,name=LeaderCount` | Integer, zero or greater |
  | Offline partitions count | `kafka.controller:type=KafkaController,name=OfflinePartitionsCount` | Integer, zero or greater |

  (13장, pp.359–360, 표 13-11·13-12·13-13)[^shapira2021]

## 요청 지표

- **카프카 프로토콜에는 서로 다른 요청이 많고 그 각각이 어떻게 수행되는지에 대한 지표가
  제공된다** (13장, p.361).[^shapira2021] 프로토콜 자체는
  [카프카 요청 처리](../concepts/kafka-request-processing.md)에 있다.
  - 버전 조건: Kafka 2.5.0 기준으로 지표가 제공되는 요청은 `AddOffsetsToTxn`·
    `AddPartitionsToTxn`·`AlterConfigs`·`AlterPartitionReassignments`·`AlterReplicaLogDirs`·
    `ApiVersions`·`ControlledShutdown`·`CreateAcls`·`CreateDelegationToken`·
    `CreatePartitions`·`CreateTopics`·`DeleteAcls`·`DeleteGroups`·`DeleteRecords`·
    `DeleteTopics`·`DescribeAcls`·`DescribeConfigs`·`DescribeDelegationToken`·
    `DescribeGroups`·`DescribeLogDirs`·`ElectLeaders`·`EndTxn`·`ExpireDelegationToken`·
    `Fetch`·`FetchConsumer`·`FetchFollower`·`FindCoordinator`·`Heartbeat`·
    `IncrementalAlterConfigs`·`InitProducerId`·`JoinGroup`·`LeaderAndIsr`·`LeaveGroup`·
    `ListGroups`·`ListOffsets`·`ListPartitionReassignments`·`Metadata`·`OffsetCommit`·
    `OffsetDelete`·`OffsetFetch`·`OffsetsForLeaderEpoch`·`Produce`·`RenewDelegationToken`·
    `SaslAuthenticate`·`SaslHandshake`·`StopReplica`·`SyncGroup`·`TxnOffsetCommit`·
    `UpdateMetadata`·`WriteTxnMarkers`다 (13장, pp.361–362, 표 13-14).[^shapira2021]
- **요청마다 지표 여덟 개가 제공되어 요청 처리의 각 단계를 들여다보게 해 준다.** `Fetch`
  요청을 예로 들면 MBean 이름은 이렇다 (13장, p.361, 표 13-15):[^shapira2021]

  | Name | JMX MBean |
  |---|---|
  | Total time | `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Fetch` |
  | Request queue time | `kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Fetch` |
  | Local time | `kafka.network:type=RequestMetrics,name=LocalTimeMs,request=Fetch` |
  | Remote time | `kafka.network:type=RequestMetrics,name=RemoteTimeMs,request=Fetch` |
  | Throttle time | `kafka.network:type=RequestMetrics,name=ThrottleTimeMs,request=Fetch` |
  | Response queue time | `kafka.network:type=RequestMetrics,name=ResponseQueueTimeMs,request=Fetch` |
  | Response send time | `kafka.network:type=RequestMetrics,name=ResponseSendTimeMs,request=Fetch` |
  | Requests per second | `kafka.network:type=RequestMetrics,name=RequestsPerSec,request=Fetch` |

- **초당 요청 수는 앞서 말한 속도 지표이며 그 유형의 요청이 시간 단위당 몇 건 수신·처리됐는지를
  보여 준다.** 다만 **`StopReplica`나 `UpdateMetadata` 같은 다수의 요청은 드물게
  일어난다** (13장, p.362).[^shapira2021]
- **일곱 개의 시간 지표는 각각 요청의 백분위수 집합과 이산 `Count` 속성을 준다. 지표는 전부
  브로커 시작 이후로 계산되므로 오래 변하지 않는 지표를 볼 때 이 점을 염두에 두어야 하며,
  브로커가 오래 돌수록 숫자가 더 안정된다** (13장, p.362).[^shapira2021]
- 일곱 구간이 각각 무엇인지 (13장, pp.362–363):[^shapira2021]
  - **Total time** — 요청을 받은 시점부터 응답을 요청자에게 보낼 때까지 브로커가 그 요청을
    처리하는 데 쓴 전체 시간.
  - **Request queue time** — 요청이 수신된 뒤 처리 시작 전까지 큐에서 보낸 시간.
  - **Local time** — 파티션 리더가 요청 처리에 쓴 시간. 디스크로 보내는 것을 포함하되 반드시
    플러시까지는 아니다.
  - **Remote time** — 요청 처리를 완료하기 전에 팔로워를 기다리며 보낸 시간.
  - **Throttle time** — 클라이언트 쿼터 설정을 만족시키기 위해 요청자를 늦추려고 응답을 붙들고
    있어야 하는 시간.
  - **Response queue time** — 응답이 요청자에게 보내지기 전 큐에서 보낸 시간.
  - **Response send time** — 실제로 응답을 보내는 데 쓴 시간.
- 지표마다 제공되는 속성 (13장, p.363):[^shapira2021] **`Count`(프로세스 시작 이후 요청의 절대
  개수), `Min`, `Max`, `Mean`, `StdDev`, 그리고 백분위수
  `50thPercentile`·`75thPercentile`·`95thPercentile`·`98thPercentile`·`99thPercentile`·
  `999thPercentile`.**
  - **99백분위 측정값은 표본 집단(여기서는 요청 시간)의 값 중 99%가 그 지표 값보다 작다는 뜻**
    이고 **1%가 그보다 크다는 뜻**이다. **흔한 패턴은 평균과 99% 또는 99.9% 값을 함께 보는
    것으로, 그렇게 하면 평균 요청이 어떻게 수행되고 이상치가 무엇인지 이해할 수 있다** (13장,
    p.363).[^shapira2021] 분위수 지표를 SLI로는 배제하는 이유는
    [서비스 수준 목표](../concepts/service-level-objectives.md)에 있다.
- 무엇을 수집할지 (13장, p.363):[^shapira2021]
  - **최소한 모든 요청 유형에 대해 total time 지표의 평균과 높은 백분위수 하나(99% 또는
    99.9%), 그리고 초당 요청 수를 수집**해야 한다. **브로커로 가는 요청의 전반적 성능을
    들여다보게 해 준다.**
  - **가능하다면 요청 유형마다 나머지 여섯 시간 지표에 대해서도 같은 측정값을 수집**한다.
    **성능 문제를 요청 처리의 특정 단계로 좁힐 수 있게 해 준다.**
- 경보 문턱은 시간 지표에서 어렵다 — **`Fetch` 요청의 시간은 클라이언트가 메시지를 얼마나
  기다릴지에 대한 설정, 페치되는 토픽이 얼마나 바쁜지, 클라이언트와 브로커 사이 네트워크
  속도를 비롯한 여러 요인에 따라 크게 달라진다** (13장, pp.363–364).[^shapira2021]
  - 그래도 할 수 있는 것 — **적어도 total time에 대해, 특히 `Produce` 요청에 대해 99.9백분위
    측정값의 기준선을 만들고 그것에 경보를 거는 것은 매우 유용할 수 있다.** **불완전 복제
    파티션 지표와 마찬가지로 `Produce` 요청의 99.9백분위가 급격히 오르는 것은 광범위한 성능
    문제를 알려 준다** (13장, p.364).[^shapira2021]

## 토픽별·파티션별 지표

- **브로커 일반의 동작을 서술하는 많은 지표에 더해 토픽별·파티션별 지표가 있다. 큰
  클러스터에서는 수가 많아 평상시 운영에서 전부를 지표 시스템에 수집하는 것이 불가능할 수
  있지만, 특정 클라이언트 이슈를 디버깅하는 데는 꽤 유용**하다 (13장,
  p.364).[^shapira2021]
  - 예로 드는 것 — **토픽 지표로 클러스터 트래픽을 크게 늘리고 있는 특정 토픽을 식별**할 수
    있고, **카프카 사용자(프로듀서·컨슈머 클라이언트)가 접근할 수 있도록 이 지표를 제공하는
    것이 중요할 수도** 있다 (13장, p.364).[^shapira2021]
- **토픽별 지표는 측정값이 앞의 브로커 지표와 매우 비슷하고, 사실 차이는 토픽 이름이 붙는다는
  것과 지표가 그 토픽에 한정된다는 것뿐**이다. **가용한 지표의 수가 워낙 많아 모니터링과
  경보를 걸고 싶지 않을 지표가 거의 확실하지만, 클라이언트가 자기 카프카 사용을 평가하고
  디버깅할 수 있도록 제공하기에는 유용**하다 (13장, p.364).[^shapira2021]

  | Name | JMX MBean |
  |---|---|
  | Bytes in rate | `kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec,topic=TOPICNAME` |
  | Bytes out rate | `kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec,topic=TOPICNAME` |
  | Failed fetch rate | `kafka.server:type=BrokerTopicMetrics,name=FailedFetchRequestsPerSec,topic=TOPICNAME` |
  | Failed produce rate | `kafka.server:type=BrokerTopicMetrics,name=FailedProduceRequestsPerSec,topic=TOPICNAME` |
  | Messages in rate | `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec,topic=TOPICNAME` |
  | Fetch request rate | `kafka.server:type=BrokerTopicMetrics,name=TotalFetchRequestsPerSec,topic=TOPICNAME` |
  | Produce request rate | `kafka.server:type=BrokerTopicMetrics,name=TotalProduceRequestsPerSec,topic=TOPICNAME` |

  (13장, pp.364–365, 표 13-16 — 예시 토픽 이름 `TOPICNAME`은 원문 그대로다)[^shapira2021]
  실패 요청 두 지표를 신뢰성 쪽에서 읽는 자리는
  [카프카 신뢰성 검증](../concepts/kafka-reliability-validation.md)에 있다.

- **파티션별 지표는 토픽별 지표보다 상시로는 덜 유용한 편이고, 토픽 수백 개가 쉽게 파티션 수천
  개가 되므로 수도 상당히 많다. 그래도 제한된 상황에서는 유용할 수 있다** (13장,
  p.365).[^shapira2021]

  | Name | JMX MBean |
  |---|---|
  | Partition size | `kafka.log:type=Log,name=Size,topic=TOPICNAME,partition=0` |
  | Log segment count | `kafka.log:type=Log,name=NumLogSegments,topic=TOPICNAME,partition=0` |
  | Log end offset | `kafka.log:type=Log,name=LogEndOffset,topic=TOPICNAME,partition=0` |
  | Log start offset | `kafka.log:type=Log,name=LogStartOffset,topic=TOPICNAME,partition=0` |

  (13장, p.365, 표 13-17)[^shapira2021]

- 각각의 쓸모 (13장, p.365):[^shapira2021]
  - **파티션 크기 지표는 그 파티션을 위해 현재 디스크에 보존되고 있는 데이터 양(바이트)을
    가리킨다. 합치면 토픽 하나가 보존하는 데이터 양이 되어 개별 클라이언트에 카프카 비용을
    배분하는 데 유용**할 수 있다.
  - **같은 토픽의 두 파티션 크기 차이는 생산 시 쓰이는 키에 걸쳐 메시지가 고르게 분포하지 않는
    문제를 가리킬 수 있다.** 그 배분 규칙은
    [프로듀서 파티션 배분](../concepts/kafka-producer-partitioning.md)에 있다.
  - **로그 세그먼트 수 지표는 그 파티션의 디스크상 로그 세그먼트 파일 수를 보여 주며, 파티션
    크기와 함께 자원 추적에 유용**할 수 있다. 세그먼트가 무엇인지는
    [카프카 물리적 저장소](../concepts/kafka-physical-storage.md)에 있다.
- **로그 끝 오프셋과 로그 시작 오프셋은 그 파티션 메시지의 가장 높은 오프셋과 가장 낮은
  오프셋**이다. 다만 **두 수의 차이가 반드시 파티션의 메시지 수를 뜻하지는 않는다 — 로그
  압착이 같은 키의 새 메시지 때문에 제거된 "빠진" 오프셋을 만들 수 있기 때문**이다 (13장,
  p.365).[^shapira2021] 그 기제는
  [카프카 로그 압착](../concepts/kafka-log-compaction.md)에 있다.
  - 쓸 데가 있는 경우 — **타임스탬프를 오프셋에 더 세밀하게 매핑해 컨슈머 클라이언트가 특정
    시각으로 오프셋을 쉽게 되돌리게 하는 용도**인데, **시간 기반 인덱스 검색이 카프카
    0.10.1에서 도입되면서 덜 중요해졌다** (13장, p.365).[^shapira2021]
- 파티션별 불완전 복제 지표도 있지만 권고는 쓰지 말라는 쪽이다 — **파티션이 불완전 복제인지
  가리키는 파티션별 지표가 제공되지만 일상 운영에서는 그리 유용하지 않다. 모으고 지켜볼 지표가
  너무 많기 때문이며, 브로커 전체의 불완전 복제 파티션 수를 모니터링하고 12장의 명령줄 도구로
  어느 파티션이 불완전 복제인지 알아내는 편이 훨씬 쉽다** (13장, p.366).[^shapira2021]

## 이어지는 페이지

- [카프카 클러스터 문제 진단](../concepts/kafka-cluster-problem-diagnosis.md) — 이 지표들을
  들고 원인을 좁히는 순서
- [카프카 지표의 기초](../concepts/kafka-metrics-basics.md) — 이 MBean들을 어디에 붙어서
  읽는지
- [서비스 수준 목표](../concepts/service-level-objectives.md) — 여기 백분위수를 주 경보로
  삼지 않는 이유
- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 요청 지표의 일곱 구간이
  대응하는 브로커 내부 경로
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — throttle time이 생기는 자리
- [카프카 JVM과 운영체제 모니터링](../concepts/kafka-jvm-and-os-monitoring.md) — 브로커
  지표만으로 모자란 자리
- [안전하지 않은 작업](../concepts/kafka-unsafe-operations.md) — 컨트롤러가 걸렸을 때 손으로
  옮기는 절차

[^shapira2021]: Shapira et al. 2021, 13장 "Monitoring Kafka" §"Broker Metrics"·§"Topic and Partition Metrics"(pp.346–366) — 인용 블록은 p.356 유휴 비율 문턱 문단 원문. 표의 지표 이름·MBean·값 범위는 표 13-5부터 13-17까지의 원문 표기 그대로다

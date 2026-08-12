---
type: concept
title: 카프카 인가와 ACL
description: 인증된 주체가 무엇을 할 수 있는지 정하는 기제 — AclAuthorizer와 ACL 바인딩을 이루는 일곱 항목, Deny 우선과 암묵적 Describe 부여라는 판정 규칙, 역할별로 필요한 ACL과 요청 대응표, 슈퍼 유저와 무조건 허용 옵션의 위험, 역할 기반 접근 제어로 확장하는 방법, 그리고 인가 결과가 남는 감사 로그
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 인가와 ACL

- [인가는 주체와 요청 사이에서 일어난다](#인가는-주체와-요청-사이에서-일어난다)
- [AclAuthorizer](#aclauthorizer)
- [ACL 바인딩을 이루는 것](#acl-바인딩을-이루는-것)
- [판정 규칙](#판정-규칙)
- [역할별로 필요한 ACL](#역할별로-필요한-acl)
- [ACL과 카프카 요청의 대응](#acl과-카프카-요청의-대응)
- [ACL을 만드는 툴](#acl을-만드는-툴)
- [슈퍼 유저와 무조건 허용](#슈퍼-유저와-무조건-허용)
- [인가를 커스터마이즈하기](#인가를-커스터마이즈하기)
- [고려사항](#고려사항)
- [감사](#감사)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인증된 주체가 무엇을 할 수 있는지를 어떻게 정하고, 실제로 무엇을 했는지는
어디에 남는가.**

## 인가는 주체와 요청 사이에서 일어난다

- **인가(authorization)는 어느 자원에 대해 어떤 작업을 수행할 수 있는지를 결정하는 과정**이고,
  **카프카 브로커는 커스터마이즈 가능한 인가자(authorizer)로 접근 제어를 관리**한다 (11장,
  p.291).[^shapira2021]
- 인증이 만든 것이 여기서 쓰인다 — **클라이언트에서 브로커로 연결이 맺어질 때마다 브로커가
  클라이언트를 인증하고 클라이언트 신원을 나타내는 `KafkaPrincipal`을 그 연결에 결합**하는데,
  **요청이 처리될 때 브로커는 그 연결에 결합된 주체가 그 요청을 수행할 권한이 있는지 검증**한다.
  예컨대 **앨리스의 프로듀서가 `customerOrders` 토픽에 새 고객 주문 레코드를 쓰려 하면 브로커는
  `User:Alice`가 그 토픽에 쓸 권한이 있는지 검증**한다 (11장, p.291).[^shapira2021] 주체가
  어떻게 만들어지는지는
  [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md)에 있다.

## AclAuthorizer

- **카프카에는 내장 인가자 `AclAuthorizer`가 있고, 인가자 클래스 이름을
  `authorizer.class.name=kafka.security.authorizer.AclAuthorizer`로 설정해 켠다** (11장,
  p.291).[^shapira2021]
  - 버전 조건: Kafka 2.3 이상 — **`AclAuthorizer`는 아파치 카프카 2.3에서 도입**됐다.
    **0.9.0.0부터의 옛 버전에는 내장 인가자 `kafka.security.auth.SimpleAclAuthorizer`가
    있었고, 그것은 폐기됐지만 여전히 지원**된다 (11장, p.292).[^shapira2021]
- **`AclAuthorizer`는 접근 제어 목록(access control list, ACL)으로 카프카 자원에 대한 세밀한
  접근 제어를 지원**한다 (11장, p.292).[^shapira2021]
- 어디에 저장되고 어떻게 읽히는가 — **ACL은 주키퍼에 저장되고 요청 인가를 위한 고성능 조회를
  위해 모든 브로커가 메모리에 캐시**한다. **캐시는 브로커가 시동할 때 적재되고 주키퍼 워처에
  기반한 알림으로 최신 상태로 유지**된다. **모든 카프카 요청은 연결에 결합된 `KafkaPrincipal`이
  요청된 자원에 대해 요청된 작업을 수행할 권한이 있는지 검증함으로써 인가**된다 (11장,
  p.292).[^shapira2021]
  - 버전 조건: Kafka 3.9 이하 — 저장 위치가 주키퍼라는 서술에 한한다.
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) 참조.

## ACL 바인딩을 이루는 것

- **ACL 바인딩 하나는 일곱 항목**으로 이뤄진다 (11장, p.292):[^shapira2021]
  - **자원 유형(resource type)** — `Cluster`·`Topic`·`Group`·`TransactionalId`·`DelegationToken`
  - **패턴 유형(pattern type)** — `Literal`·`Prefixed`
  - **자원 이름(resource name)** — 자원의 이름이나 접두어, 또는 와일드카드 `*`
  - **작업(operation)** —
    `Describe`·`Create`·`Delete`·`Alter`·`Read`·`Write`·`DescribeConfigs`·`AlterConfigs`
  - **권한 유형(permission type)** — `Allow`·`Deny`이며 **`Deny`가 더 높은 우선순위**를 갖는다
  - **주체(principal)** — `<principalType>:<principalName>` 형식(예: `User:Bob`,
    `Group:Sales`)이며, **`User:*`로 모든 사용자에게 접근을 부여**할 수 있다
  - **호스트(host)** — 클라이언트 연결의 출발지 IP 주소, 또는 모든 호스트를 인가하면 `*`
- 이것을 한 문장으로 읽으면 예컨대 **"`User:Alice`는 `192.168.0.1`에서 접두어 패턴의
  `Topic:customer`에 `Write`할 `Allow` 권한을 갖는다"** 가 된다 (11장,
  p.292).[^shapira2021]
- 와일드카드의 정의가 따로 있다 — **패턴 유형이 `Literal`이고 자원 이름이 `*`인 ACL이
  와일드카드 ACL로 쓰이며, 그 자원 유형의 모든 자원 이름과 매치**된다 (11장,
  p.292).[^shapira2021]

## 판정 규칙

- **`AclAuthorizer`는 그 행동과 매치되는 `Deny` ACL이 하나도 없고 매치되는 `Allow` ACL이 적어도
  하나 있을 때 행동을 인가**한다 (11장, p.292).[^shapira2021]
- 암묵적 부여가 둘 있다 (11장, p.292):[^shapira2021]
  - **`Read`·`Write`·`Alter`·`Delete` 권한이 부여되면 `Describe` 권한이 암묵적으로 부여**된다.
  - **`AlterConfigs` 권한이 부여되면 `DescribeConfigs` 권한이 암묵적으로 부여**된다.

## 역할별로 필요한 ACL

- 누가 무엇을 받아야 하는지 (11장, p.293):[^shapira2021]
  - **브로커는 컨트롤러 요청과 레플리카 페치 요청을 인가하기 위해 `Cluster:ClusterAction`
    접근을 부여**받아야 한다.
  - **프로듀서는 토픽에 생산하기 위해 `Topic:Write`가 필요**하다.
  - **트랜잭션 없는 멱등적 생산을 하려면 프로듀서에 `Cluster:IdempotentWrite`도 부여**돼야
    한다.
  - **트랜잭션 프로듀서는 트랜잭션 ID에 대한 `TransactionalId:Write` 접근과, 컨슈머 그룹의
    오프셋을 커밋하기 위한 `Group:Read`가 필요**하다.
  - **컨슈머는 토픽에서 소비하기 위해 `Topic:Read`가, 그룹 관리나 오프셋 관리를 쓴다면 그
    컨슈머 그룹에 대한 `Group:Read`가 필요**하다.
  - **관리 작업에는 적절한 `Create`·`Delete`·`Describe`·`Alter`·`DescribeConfigs`·`AlterConfigs`
    접근이 필요**하다.
- 이 역할들이 원래 무엇인지는
  [멱등적 프로듀서](../concepts/kafka-idempotent-producer.md)·
  [카프카 트랜잭션](../concepts/kafka-transactions.md)·
  [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md)에 있다.

## ACL과 카프카 요청의 대응

- 책은 **각 ACL이 어떤 카프카 요청에 적용되는지**를 표로 준다 (11장, pp.293–294, 표
  11-1):[^shapira2021]

  | ACL | 적용되는 카프카 요청 | 비고 |
  |---|---|---|
  | `Cluster:ClusterAction` | 컨트롤러 요청과 복제를 위한 팔로워 페치 요청을 포함한 브로커 간 요청 | 브로커에만 부여해야 한다 |
  | `Cluster:Create` | `CreateTopics`와 자동 토픽 생성 | 특정 토픽 생성의 세밀한 접근 제어에는 `Topic:Create`를 쓴다 |
  | `Cluster:Alter` | `CreateAcls`, `DeleteAcls`, `AlterReplicaLogDirs`, `ElectReplicaLeader`, `AlterPartitionReassignments` | |
  | `Cluster:AlterConfigs` | 브로커와 브로커 로거에 대한 `AlterConfigs`·`IncrementalAlterConfigs`, `AlterClientQuotas` | |
  | `Cluster:Describe` | `DescribeAcls`, `DescribeLogDirs`, `ListGroups`, `ListPartitionReassignments`, 메타데이터 요청에서 클러스터의 인가된 작업 기술 | `ListGroups`의 세밀한 접근 제어에는 `Group:Describe`를 쓴다 |
  | `Cluster:DescribeConfigs` | 브로커와 브로커 로거에 대한 `DescribeConfigs`, `DescribeClientQuotas` | |
  | `Cluster:IdempotentWrite` | 멱등적 `InitProducerId`와 `Produce` 요청 | 트랜잭션을 쓰지 않는 멱등적 프로듀서에만 필요하다 |
  | `Topic:Create` | `CreateTopics`와 자동 토픽 생성 | |
  | `Topic:Delete` | `DeleteTopics`, `DeleteRecords` | |
  | `Topic:Alter` | `CreatePartitions` | |
  | `Topic:AlterConfigs` | 토픽에 대한 `AlterConfigs`·`IncrementalAlterConfigs` | |
  | `Topic:Describe` | 토픽에 대한 메타데이터 요청, `OffsetForLeaderEpoch`, `ListOffset`, `OffsetFetch` | |
  | `Topic:DescribeConfigs` | 토픽에 대한 `DescribeConfigs`, `CreateTopics` 응답에 설정을 돌려주기 위한 것 | |
  | `Topic:Read` | 컨슈머 `Fetch`, `OffsetCommit`, `TxnOffsetCommit`, `OffsetDelete` | 컨슈머에 부여해야 한다 |
  | `Topic:Write` | `Produce`, `AddPartitionToTxn` | 프로듀서에 부여해야 한다 |
  | `Group:Read` | `JoinGroup`, `SyncGroup`, `LeaveGroup`, `Heartbeat`, `OffsetCommit`, `AddOffsetsToTxn`, `TxnOffsetCommit` | 컨슈머 그룹 관리나 카프카 기반 오프셋 관리를 쓰는 컨슈머에 필요하다. 트랜잭션 안에서 오프셋을 커밋하는 트랜잭션 프로듀서에도 필요하다 |
  | `Group:Describe` | `FindCoordinator`, `DescribeGroup`, `ListGroups`, `OffsetFetch` | |
  | `Group:Delete` | `DeleteGroups`, `OffsetDelete` | |
  | `TransactionalId:Write` | 트랜잭션을 쓰는 `Produce`·`InitProducerId`, `AddPartitionToTxn`, `AddOffsetsToTxn`, `TxnOffsetCommit`, `EndTxn` | 트랜잭션 프로듀서에 필요하다 |
  | `TransactionalId:Describe` | 트랜잭션 코디네이터에 대한 `FindCoordinator` | |
  | `DelegationToken:Describe` | `DescribeTokens` | |

  - 이 표가 [미러메이커](../concepts/kafka-mirrormaker.md)의 보안 절이 나열하는 ACL 여섯 줄의
    의미를 준다 — 거기서 `Topic:DescribeConfigs`·`Cluster:Alter` 같은 이름이 무엇을 여는지가
    여기 있다.

## ACL을 만드는 툴

- **카프카는 브로커에 설정된 인가자로 ACL을 관리하는 툴을 제공**하고, **ACL을 주키퍼에 직접
  만들 수도** 있다. 후자는 **브로커를 시작하기 전에 브로커 ACL을 만드는 데 유용**하다 (11장,
  p.294):[^shapira2021]

  ```sh
  bin/kafka-acls.sh --add --cluster --operation ClusterAction \
      --authorizer-properties zookeeper.connect=localhost:2181 \
      --allow-principal User:kafka
  bin/kafka-acls.sh --bootstrap-server localhost:9092 \
      --command-config admin.props --add --topic customerOrders \
      --producer --allow-principal User:Alice
  bin/kafka-acls.sh --bootstrap-server localhost:9092 \
      --command-config admin.props --add --resource-pattern-type PREFIXED \
      --topic customer --operation Read --allow-principal User:Bob
  ```

  - 세 명령이 하는 일 (11장, p.294):[^shapira2021] **브로커 사용자의 ACL은 주키퍼에 직접
    만든다**, **ACL 명령은 기본적으로 리터럴 ACL을 부여하며 여기서 `User:Alice`가
    `customerOrders` 토픽에 쓸 권한을 얻는다**, **접두어 ACL은 밥에게 `customer`로 시작하는
    모든 토픽을 읽을 권한을 준다**.
  - 버전 조건: Kafka 3.9 이하 — 첫 명령의 `--authorizer-properties zookeeper.connect` 경로에
    한한다. [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) 참조.

## 슈퍼 유저와 무조건 허용

- **`AclAuthorizer`에는 자원이나 주체에 넓은 접근을 부여해 ACL 관리를 단순화하는 설정 옵션이
  둘** 있고, **특히 기존 클러스터에 인가를 처음 추가할 때** 쓰인다 —
  `super.users=User:Carol;User:Admin`과 `allow.everyone.if.no.acl.found=true` (11장,
  p.295).[^shapira2021]
- **슈퍼 유저는 모든 자원에 대한 모든 작업에 아무 제한 없이 접근이 부여되고 `Deny` ACL로
  거부할 수 없다.** 그래서 **캐럴의 자격 증명이 침해되면 캐럴을 `super.users`에서 제거하고
  변경을 적용하기 위해 브로커를 재시작해야** 한다. **프로덕션 시스템에서는 필요할 때 접근을
  쉽게 회수할 수 있도록 ACL로 특정 접근을 부여하는 편이 안전**하다 (11장,
  p.295).[^shapira2021]
- 구분자에 함정이 있다 — **카프카의 다른 목록 설정이 쉼표로 구분되는 것과 달리 `super.users`는
  세미콜론으로 구분**되는데, **SSL 인증서의 식별 이름 같은 사용자 주체에 쉼표가 자주 들어가기
  때문**이다 (11장, p.295).[^shapira2021]
- **`allow.everyone.if.no.acl.found`가 켜지면 ACL이 없는 자원에 대해 모든 사용자에게 접근이
  부여**된다. **클러스터에서 인가를 처음 켤 때나 개발 중에는 유용할 수 있지만 프로덕션에는
  적합하지 않다** — **새 자원에 의도치 않게 접근이 부여될 수** 있고, **매치되는 접두어나
  와일드카드의 ACL이 추가되어 "ACL 없음" 조건이 더 이상 성립하지 않게 되면 접근이 예상치 못하게
  제거될 수도** 있다 (11장, p.295).[^shapira2021]

## 인가를 커스터마이즈하기

- **카프카의 인가는 추가 제약을 구현하거나 역할 기반 접근 제어 같은 새로운 종류의 접근 제어를
  더하도록 커스터마이즈**할 수 있다 (11장, p.295).[^shapira2021]
- 책이 보이는 첫 예는 **일부 요청의 사용을 내부 리스너로만 제한하는 커스텀 인가자**다. 이것이
  가능한 이유는 **인가자가 리스너 이름·보안 프로토콜·요청 유형 등의 메타데이터를 담은 요청
  컨텍스트를 받기 때문**이며, 그 덕에 **커스텀 인가자가 컨텍스트에 근거해 제약을 더하거나 뺄
  수** 있다. 예제는 **`AclAuthorizer`를 확장해 공개 API로 내장 인가자의 기능을 재사용**하고,
  `INTERNAL` 리스너가 아닌 곳에서 온 `CREATE_ACLS`·`DELETE_ACLS`를 `DENIED`로 돌린다 (11장,
  pp.295–296).[^shapira2021]
- 둘째 예는 확장 방향이다 — **카프카 인가자는 외부 시스템과 통합해 그룹 기반 접근 제어나 역할
  기반 접근 제어를 지원**할 수 있고, **서로 다른 주체 유형으로 그룹 주체나 역할 주체에 대한
  ACL을 만들 수** 있다. 예컨대 **LDAP 서버의 역할과 그룹으로 인가자 안의 그룹·역할 맵을 주기적으로
  채워 서로 다른 수준의 `Allow` ACL을 지원**하는 식이다. 책의 스칼라 예제는 **사용자 본인과 그
  사용자의 모든 그룹·역할에 대해 인가를 수행하고 그중 하나라도 인가되면 `ALLOWED`를 돌리며, 이
  예제는 그룹·역할에 대한 `Deny` ACL을 지원하지 않는다**고 명시한다 (11장,
  pp.296–297).[^shapira2021]
- 그렇게 만든 주체 유형은 표준 툴에서 그대로 쓴다 — **`--allow-principal Group:Sales`는 `Sales`
  그룹에 속한 사용자에게 적용되는 ACL을, `--allow-principal=Role:Operator`는 `Operator` 역할을
  가진 사용자에게 적용되는 ACL을 만든다** (11장, p.297).[^shapira2021]

## 고려사항

- (11장, pp.297–298):[^shapira2021]
  - **`AclAuthorizer`가 ACL을 주키퍼에 저장하므로 주키퍼 접근이 제한**돼야 한다. **안전한
    주키퍼가 없는 배포는 ACL을 안전한 외부 데이터베이스에 저장하는 커스텀 인가자를 구현**할 수
    있다.
    - 버전 조건: Kafka 3.9 이하 — 주키퍼 부분에 한한다.
      [주키퍼 보안](../concepts/kafka-zookeeper-security.md) 참조.
  - **사용자가 많은 큰 조직에서는 개별 자원마다 ACL을 관리하는 것이 매우 번거로워질 수** 있다.
    **부서마다 다른 자원 접두어를 예약하면 접두어 ACL을 써서 필요한 ACL 수를 최소화**할 수 있고,
    **앞의 예처럼 그룹·역할 기반 ACL과 결합하면 큰 배포의 접근 제어를 더 단순화**할 수 있다.
  - **최소 권한 원칙(principle of least privilege)으로 사용자 접근을 제한하면 사용자가 침해됐을
    때의 노출을 제한**할 수 있다 — **각 사용자 주체가 자기 작업을 수행하는 데 필요한 자원에만
    접근을 부여하고, 더 이상 필요 없는 ACL은 제거**한다는 뜻이다. **사람이 조직을 떠나는 등
    사용자 주체가 더 이상 쓰이지 않게 되면 ACL을 즉시 제거**해야 한다.
  - **오래 도는 애플리케이션은 특정 사용자에 결합된 자격 증명 대신 서비스 자격 증명으로 설정해
    직원이 떠날 때 중단이 없게** 할 수 있다.
  - **사용자 주체가 시스템에서 제거된 뒤에도 그 주체의 수명이 긴 연결이 요청을 계속 처리할 수
    있으므로, 와일드카드 주체를 쓴 ACL을 통해 그 주체에 의도치 않게 접근이 부여되지 않도록
    `Deny` ACL을 쓸 수** 있다. 그 상황은
    [카프카 재인증](../concepts/kafka-reauthentication.md)에 있다.
  - **주체의 옛 버전을 쓰는 연결에 접근이 부여되는 것을 막기 위해 가능하면 주체 재사용을
    피해야** 한다.

## 감사

- **카프카 브로커는 감사와 디버깅을 위해 포괄적인 log4j 로그를 생성하도록 설정**할 수 있고,
  **로깅 수준과 로깅에 쓰이는 어펜더 및 그 설정 옵션은 `log4j.properties`에서 지정**한다
  (11장, p.298).[^shapira2021]
- 로거가 둘로 갈린다 — **인가 로깅에 쓰이는 `kafka.authorizer.logger`와 요청 로깅에 쓰이는
  `kafka.request.logger` 인스턴스를 독립적으로 설정해 감사 로깅의 로그 수준과 보존을
  커스터마이즈**할 수 있다. **프로덕션 시스템은 이 로그를 분석·시각화하는 데 일래스틱 스택 같은
  프레임워크를 쓸 수** 있다 (11장, p.298).[^shapira2021]
- 수준이 의미를 갖는다 (11장, p.298):[^shapira2021]
  - **인가자는 접근이 거부된 모든 시도에 대해 INFO 수준 로그 항목을, 접근이 부여된 모든 작업에
    대해 DEBUG 수준 로그 항목을 생성**한다. 즉 기본 수준에서 남는 것은 거부다.
  - **DEBUG 수준에서 생성되는 요청 로그에는 사용자 주체와 클라이언트 호스트의 상세도 포함**되고,
    **요청 로거가 TRACE 수준으로 설정되면 요청의 전체 상세가 포함**된다.
- 이 로그로 무엇을 하는가 — **인가자 로그와 요청 로그를 분석해 의심스러운 활동을 탐지**할 수
  있고, **인증 실패를 추적하는 지표와 인가 실패 로그는 감사에 극히 유용하며 공격이나 무단 접근이
  일어났을 때 가치 있는 정보를 준다** (11장, pp.298–299).[^shapira2021]
- 메시지 단위의 감사도 가능하다 — **메시지의 종단 간 감사 가능성과 추적 가능성을 위해 메시지를
  생산할 때 감사 메타데이터를 메시지 헤더에 넣을 수** 있고, **그 메타데이터의 무결성을 보호하는
  데 종단 간 암호화를 쓸 수** 있다 (11장, p.299).[^shapira2021] 그쪽은
  [카프카 암호화](../concepts/kafka-encryption.md)에 있다.

## 이어지는 페이지

- [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md) — 인가가 쓰는 주체가
  만들어지는 곳
- [미러메이커](../concepts/kafka-mirrormaker.md) — 이 ACL들이 실제 목록으로 요구되는 사례
- [카프카 트랜잭션](../concepts/kafka-transactions.md) — `TransactionalId:Write`가 걸리는 대상
- [멱등적 프로듀서](../concepts/kafka-idempotent-producer.md) — `Cluster:IdempotentWrite`가
  걸리는 대상
- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — `Group:Read`가
  여는 요청들
- [카프카 재인증](../concepts/kafka-reauthentication.md) — `Deny` ACL이 가장 빠른 수단이 되는
  상황
- [주키퍼 보안](../concepts/kafka-zookeeper-security.md) — ACL이 저장되는 곳
- [카프카 암호화](../concepts/kafka-encryption.md) — 감사 메타데이터의 무결성

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "Authorization" 절과 "Auditing"
    절(pp.291–299) — 표는 pp.293–294 표 11-1을 옮긴 것으로 ACL·요청 이름은 원문 그대로 두고
    Notes 열만 한국어로 옮겼다. 코드 펜스는 p.294 `kafka-acls.sh` 예제 세 묶음이며 원문의
    주석 번호 표식과 `$` 프롬프트만 덜어냈다(보탠 줄 없음). **원문 오식**: p.293 본문의
    "TransactionalId:Write access to the transaction IS"에서 `IS`는 `ID`의 오식으로 보이나
    고치지 않고 여기 적는다 — 본문은 직인용이 아니라 한국어 재서술이라 오식이 옮겨 가지 않았다

---
type: concept
title: 카프카 어드민 클라이언트
description: 관리 작업을 애플리케이션 코드 안에서 실행하는 AdminClient — 비동기·최종적 일관성 API라는 설계 전제, 결과가 Future로 감싸여 예외가 ExecutionException으로 오는 이유, 계층 없는 평평한 인터페이스, 상태를 바꾸는 요청과 읽는 요청이 서로 다른 브로커로 가는 점, 만들고 닫는 절차와 DNS·타임아웃 설정, 블로킹 get을 피해야 하는 경우, 그리고 목업으로 테스트하는 법
generated: { by: "claude-opus-5", at: "2026-08-12T15:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 어드민 클라이언트

- [왜 프로그램으로 관리하는가](#왜-프로그램으로-관리하는가)
- [비동기이고 최종적 일관성을 갖는 API](#비동기이고-최종적-일관성을-갖는-api)
- [옵션과 타임아웃](#옵션과-타임아웃)
- [수평 구조](#수평-구조)
- [어느 브로커가 처리하는가](#어느-브로커가-처리하는가)
- [만들고 닫기](#만들고-닫기)
- [DNS 조회 방식](#dns-조회-방식)
- [요청 타임아웃](#요청-타임아웃)
- [에러는 ExecutionException으로 온다](#에러는-executionexception으로-온다)
- [블로킹 get을 피해야 할 때](#블로킹-get을-피해야-할-때)
- [붙은 클러스터 확인하기](#붙은-클러스터-확인하기)
- [목업으로 테스트하기](#목업으로-테스트하기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **관리 작업을 애플리케이션 코드 안에서 실행하는 클라이언트는 어떤 설계
전제 위에 있고, 어떻게 만들고 설정하고 닫는가.**

> **버전 조건**: Kafka 0.11 이상. **아파치 카프카는 0.11에서 AdminClient를 추가**했고
> (5장, p.113),[^shapira2021] 그 이전 버전에는 이 API 자체가 없다.

## 왜 프로그램으로 관리하는가

- 카프카를 관리하는 CLI·GUI 툴은 많지만, **클라이언트 애플리케이션 안에서 관리 명령을
  실행하고 싶은 때가 있다.** 특히 흔한 유스케이스는 **사용자 입력이나 데이터에 따라 요청
  시점에 새 토픽을 만드는 것**이다 (5장, p.113).[^shapira2021]
  - 책이 드는 예는 사물 인터넷(Internet of Things, IoT)이다 — **사용자 장치에서 이벤트를
    받아 장치 종류에 따라 서로 다른 토픽에 쓰는 앱**에서, **제조사가 새 장치 종류를 내놓으면
    별도 프로세스로 토픽을 미리 만들어 두는 것을 기억하거나, 아니면 인식하지 못한 장치
    종류의 이벤트가 들어왔을 때 애플리케이션이 동적으로 새 토픽을 만들거나** 둘 중 하나다.
  - **두 번째 대안에는 단점이 있지만, 토픽을 만들기 위해 별도 프로세스에 의존하지 않아도
    된다는 점이 적절한 시나리오에서는 매력적인 성질**이다.
- 이 API가 무엇을 대체했는지는 책이 한 문장으로 정의한다 (5장, p.113):[^shapira2021]

  > Apache Kafka added the AdminClient in version 0.11 to provide a programmatic API for
  > administrative functionality that was previously done in the command line: listing,
  > creating, and deleting topics; describing the cluster; managing ACLs; and modifying
  > configuration.

- AdminClient 이전에는 **"이벤트를 쓰기 전에 토픽이 있어야 한다"는 요구를 푸는 방법이
  셋뿐이었고 어느 것도 특별히 쓰기 좋지 않았다** — **`producer.send()`에서
  `UNKNOWN_TOPIC_OR_PARTITION` 예외를 잡아 토픽을 만들어야 한다고 사용자에게 알리거나,
  쓰려는 클러스터에 자동 토픽 생성이 켜져 있기를 바라거나, 호환성 보장이 없는 내부 API에
  의존하는 것**이다. **AdminClient가 생긴 지금의 훨씬 나은 해법은 토픽이 있는지 확인하고
  없으면 그 자리에서 만드는 것**이다 (5장, p.113).[^shapira2021] 그 절차는
  [토픽 관리](../concepts/kafka-topic-administration.md)에 있다.

## 비동기이고 최종적 일관성을 갖는 API

- **AdminClient에서 가장 중요하게 이해할 것은 그것이 비동기라는 점**이다. **각 메서드는
  클러스터 컨트롤러에 요청을 전달한 직후 즉시 리턴하고, 하나 이상의 `Future` 객체를
  돌려준다.** `Future`는 비동기 작업의 결과이고 **작업 상태 확인·취소·완료 대기·완료 후 함수
  실행 메서드**를 갖는다 (5장, p.114).[^shapira2021]
- **카프카의 AdminClient는 그 `Future`들을 `Result` 객체로 감싸는데**, `Result`는 **작업 완료를
  기다리는 메서드와 흔한 후속 작업을 위한 헬퍼 메서드**를 제공한다. 예컨대
  **`KafkaAdminClient.createTopics`는 `CreateTopicsResult` 객체를 리턴하고, 이 객체로 모든
  토픽이 생성될 때까지 기다리거나, 토픽별 상태를 개별로 확인하거나, 생성 뒤 특정 토픽의
  설정을 가져올 수 있다** (5장, p.114).[^shapira2021]
- 완료 시점의 의미가 정확히 무엇인지가 이 API의 함정이다 — **컨트롤러에서 브로커로
  메타데이터가 전파되는 것이 비동기이므로, AdminClient API가 리턴하는 `Future`는 컨트롤러
  상태가 완전히 갱신된 시점에 완료된 것으로 친다.** **그 시점에 모든 브로커가 새 상태를 알고
  있는 것은 아니어서, `listTopics` 요청이 최신이 아닌 브로커에서 처리되면 방금 만든 토픽이
  결과에 없을 수 있다** (5장, p.114).[^shapira2021]
- 책은 이 성질에 이름을 붙인다 (5장, p.114):[^shapira2021]

  > This property is also called *eventual consistency*: eventually every broker will know
  > about every topic, but we can't guarantee exactly when this will happen.

## 옵션과 타임아웃

- **AdminClient의 모든 메서드는 그 메서드 전용 `Options` 객체를 인자로 받는다** — 예컨대
  **`listTopics`는 `ListTopicsOptions`를, `describeCluster`는 `DescribeClusterOptions`를**
  받는다. 이 객체들이 **요청을 브로커가 어떻게 처리할지에 대한 설정**을 담는다 (5장,
  pp.114–115).[^shapira2021]
- **모든 AdminClient 메서드가 공통으로 갖는 설정 하나는 `timeoutMs`** 다 — **`TimeoutException`을
  던지기 전까지 클라이언트가 클러스터의 응답을 기다리는 시간**을 통제하며, 이것이
  **애플리케이션이 AdminClient 작업에 블록될 수 있는 시간을 제한**한다 (5장,
  p.115).[^shapira2021]
- 그 밖의 옵션 예 — **`listTopics`가 내부 토픽까지 리턴할지, `describeCluster`가 클라이언트가
  수행할 권한을 가진 작업 목록까지 리턴할지** (5장, p.115).[^shapira2021]

## 수평 구조

- **아파치 카프카 프로토콜이 지원하는 모든 어드민 작업이 `KafkaAdminClient`에 직접 구현돼
  있다. 객체 계층도 네임스페이스도 없다** (5장, p.115).[^shapira2021]
- **인터페이스가 꽤 크고 어쩌면 압도적일 수 있어 다소 논쟁적이지만, 주된 이점은 어떤 어드민
  작업을 프로그램으로 수행하는 방법을 알고 싶을 때 검색할 JavaDoc이 정확히 하나이고 IDE
  자동 완성이 잘 듣는다는 것**이다. **엉뚱한 곳을 보고 있는 것은 아닌지 고민할 필요가 없다**
  (5장, p.115).[^shapira2021]
- 그래서 없음의 의미도 명확하다 (5장, p.115):[^shapira2021]

  > If it isn't in AdminClient, it was not implemented yet (but contributions are welcome!).

## 어느 브로커가 처리하는가

- **클러스터 상태를 바꾸는 모든 작업 — 생성·삭제·변경 — 은 컨트롤러가 처리한다. 클러스터
  상태를 읽는 작업 — 목록 조회·설명 — 은 아무 브로커나 처리할 수 있고, 클라이언트가 아는
  한에서 가장 부하가 적은 브로커로 보내진다** (5장, p.115).[^shapira2021] 컨트롤러가
  무엇인지는 [브로커와 클러스터](../concepts/brokers-and-clusters.md)에 있다.
  - **API 사용자에게 영향을 주지는 않지만, 어떤 작업은 성공하는데 다른 것은 실패하는 예상치
    못한 동작을 보거나 어떤 작업이 왜 오래 걸리는지 알아내려 할 때 알아 두면 좋다** (5장,
    p.115).[^shapira2021]
- **집필 시점(아파치 카프카 2.5 출시 직전) 기준으로 대부분의 어드민 작업은 AdminClient로
  하거나 주키퍼에 저장된 클러스터 메타데이터를 직접 고쳐서 할 수 있었다.** 저자들은 **주키퍼를
  직접 쓰지 말 것을 강력히 권고하고, 꼭 그래야 한다면 그것을 아파치 카프카에 버그로 신고하라고
  한다** (5장, p.115).[^shapira2021]
  - 이유는 앞을 내다본 것이다 — **가까운 미래에 아파치 카프카 커뮤니티가 주키퍼 의존을 제거할
    것이고, 어드민 작업에 주키퍼를 직접 쓰는 모든 애플리케이션은 수정돼야 한다. 반면
    AdminClient API는 카프카 클러스터 안의 구현만 달라질 뿐 정확히 그대로 남는다** (5장,
    p.115).[^shapira2021] 그 제거가 실제로 어떻게 진행됐는지는
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)에 있다.

## 만들고 닫기

- **AdminClient를 쓰려면 가장 먼저 AdminClient 클래스의 인스턴스를 만든다.** 정적 `create`
  메서드가 **설정을 담은 `Properties` 객체를 인자로 받고, 유일한 필수 설정은 클러스터의
  URI — 접속할 브로커들의 쉼표 구분 목록**이다. **프로덕션 환경에서는 늘 그렇듯 하나가
  마침 사용 불가일 경우를 대비해 최소 세 개의 브로커를 지정**한다 (5장,
  pp.115–116).[^shapira2021] 아래는 만들고 닫는 최소 형태이며, `AdminClient.create`·
  `admin.close`로 찾는다 (5장, p.116):[^shapira2021]

  ```java
  Properties props = new Properties();
  props.put(AdminClientConfig.BOOTSTRAP_SERVERS_CONFIG, "localhost:9092");
  AdminClient admin = AdminClient.create(props);
  // TODO: Do something useful with AdminClient
  admin.close(Duration.ofSeconds(30));
  ```

- 닫는 쪽에 타임아웃 인자가 있는 이유 — **`close`를 부를 때 아직 진행 중인 AdminClient 작업이
  있을 수 있다.** 그래서 **`close`를 부르고 나면 다른 메서드를 부르거나 요청을 더 보낼 수는
  없지만, 클라이언트는 타임아웃이 만료될 때까지 응답을 기다린다. 타임아웃이 만료되면
  클라이언트는 진행 중인 모든 작업을 타임아웃 예외로 중단하고 자원을 해제한다.** **타임아웃
  없이 `close`를 부르면 진행 중인 모든 작업이 끝날 때까지 걸리는 만큼 기다린다** (5장,
  p.116).[^shapira2021]
- 설정할 것의 양 자체가 다르다 — **`KafkaProducer`와 `KafkaConsumer`에는 중요한 설정
  매개변수가 꽤 많지만 AdminClient는 훨씬 단순해서 설정할 것이 많지 않다** (5장,
  p.116).[^shapira2021] 비교 대상은
  [프로듀서 설정](../concepts/kafka-producer-configuration.md)과
  [컨슈머 설정](../concepts/kafka-consumer-configuration.md)이다.

## DNS 조회 방식

- 버전 조건: Kafka 2.1.0 이상 — **`client.dns.lookup` 설정은 아파치 카프카 2.1.0 릴리스에서
  도입됐다** (5장, p.116).[^shapira2021]
- **기본적으로 카프카는 부트스트랩 서버 설정에 준 호스트명(그리고 이후
  `advertised.listeners` 설정이 지정한 대로 브로커들이 리턴하는 이름)을 기준으로 연결을
  검증·해석·생성한다.** **이 단순한 모델은 대부분의 경우 통하지만 두 가지 중요한 유스케이스를
  못 덮는다 — 특히 부트스트랩 설정에서의 DNS 별칭(alias) 사용, 그리고 여러 IP 주소로
  매핑되는 단일 DNS 사용**이다. **비슷해 보이지만 서로 다르고, 두 시나리오는 상호
  배타적**이다 (5장, p.116).[^shapira2021]
- **DNS 별칭** — **`broker1.hostname.com`·`broker2.hostname.com` 같은 명명 규칙의 브로커가
  여럿일 때, 유지하기 어려워지기 쉬운 부트스트랩 서버 설정에 전부 적는 대신 그 모두로
  매핑되는 DNS 별칭 하나를 만들어 `all-brokers.hostname.com`으로 부트스트랩**할 수 있다 —
  **클라이언트의 최초 연결을 어느 브로커가 받는지는 실제로 상관없기 때문**이다 (5장,
  pp.116–117).[^shapira2021]
  - **SASL을 쓰면 이것이 깨진다** — **클라이언트는 `all-brokers.hostname.com`을 인증하려
    하는데 서버 주체(principal)는 `broker2.hostname.com`이다. 이름이 맞지 않으면 SASL은
    인증을 거부하고(브로커 인증서가 중간자 공격일 수 있으므로) 연결이 실패한다** (5장,
    p.117).[^shapira2021]
  - 해결은 **`client.dns.lookup=resolve_canonical_bootstrap_servers_only`** 다 — **이 설정에서
    클라이언트는 DNS 별칭을 "펼쳐서", 그 별칭이 연결되는 모든 브로커 이름을 원래 부트스트랩
    목록에 포함시킨 것과 같은 결과**를 만든다 (5장, p.117).[^shapira2021]
- **여러 IP 주소를 가진 DNS 이름** — **현대적 네트워크 구조에서는 모든 브로커를 프록시나 로드
  밸런서 뒤에 두는 것이 흔하고, 쿠버네티스처럼 클러스터 외부에서 오는 연결을 허용하려면
  로드 밸런서가 필요한 환경에서 특히 그렇다. 이때 로드 밸런서가 단일 장애점이 되는 것을
  원치 않으므로 `broker1.hostname.com`이 여러 IP 목록을 가리키고, 그것들이 전부 로드
  밸런서로 해석되며 모두 같은 브로커로 트래픽을 보내는 구성이 매우 흔하다. 이 IP들은 시간이
  지나며 바뀔 가능성도 높다** (5장, p.117).[^shapira2021]
  - **기본적으로 카프카 클라이언트는 호스트명이 해석하는 첫 IP로만 연결을 시도한다. 즉 그 IP가
    사용 불가가 되면 브로커가 완전히 멀쩡한데도 클라이언트는 연결에 실패한다.** 그래서
    **고가용 로드 밸런싱 계층의 이득을 놓치지 않도록 `client.dns.lookup=use_all_dns_ips` 사용이
    매우 권장**된다 (5장, p.117).[^shapira2021]

## 요청 타임아웃

- **`request.timeout.ms`는 애플리케이션이 AdminClient의 응답을 기다리는 데 쓸 수 있는 시간을
  제한한다. 여기에는 클라이언트가 재시도 가능한 에러를 받았을 때 재시도에 쓰는 시간도
  포함**된다 (5장, p.117).[^shapira2021]
- **기본값은 120초로 꽤 길지만, 일부 AdminClient 작업 — 특히 컨슈머 그룹 관리 명령 — 은
  응답까지 시간이 꽤 걸릴 수 있다** (5장, p.117).[^shapira2021] 그 명령들은
  [컨슈머 그룹 관리](../concepts/kafka-consumer-group-administration.md)에 있다.
- **각 AdminClient 메서드는 그 호출에만 적용되는 타임아웃 값을 담을 수 있는 `Options` 객체를
  받는다. AdminClient 작업이 애플리케이션의 임계 경로에 있다면 더 낮은 타임아웃 값을 쓰고
  카프카의 응답이 제때 오지 않는 것을 다른 방식으로 처리하고 싶을 수 있다** (5장,
  p.117).[^shapira2021]
  - **책이 드는 예는 시작 시 특정 토픽의 존재를 검증하려 하는 서비스**다 — **카프카가 응답에
    30초 넘게 걸리면 서버 시작을 계속 진행하고 토픽 존재 검증은 나중으로 미루거나 아예
    건너뛰고 싶을 수 있다** (5장, p.117).[^shapira2021]

## 에러는 ExecutionException으로 온다

- **모든 AdminClient 결과 객체는 카프카가 에러로 응답할 때 `ExecutionException`을 던진다.
  AdminClient 결과가 `Future` 객체로 감싸여 있고 그 `Future`가 예외를 감싸기 때문**이다.
  따라서 **카프카가 리턴한 에러를 얻으려면 항상 `ExecutionException`의 cause를 살펴야**
  한다 (5장, p.119).[^shapira2021]
- 이 규칙이 실제로 어떻게 쓰이는지 — **토픽이 없으면 서버가 설명으로 응답할 수 없어 에러를
  돌려보내고 `Future`는 `ExecutionException`을 던지며 완료된다. 서버가 보낸 실제 에러가 그
  예외의 cause**다 (5장, p.119).[^shapira2021] 그래서
  `UnknownTopicOrPartitionException`이나 `TopicExistsException` 같은 판정은 전부 cause를
  보고 한다 —
  [토픽 관리](../concepts/kafka-topic-administration.md)에 그 형태가 있다.

## 블로킹 get을 피해야 할 때

- **책의 예제들은 서로 다른 AdminClient 메서드가 리턴한 `Future`에 블로킹 `get()` 호출을
  쓴다. 대부분의 경우 이것으로 충분하다 — 어드민 작업은 드물고, 작업이 성공하거나 타임아웃
  날 때까지 기다리는 것은 대체로 받아들일 만하다** (5장, p.120).[^shapira2021]
- **예외가 하나 있다 — 많은 수의 어드민 요청을 처리할 것으로 예상되는 서버를 쓰는 경우다.
  이때는 카프카의 응답을 기다리는 동안 서버 스레드를 블록하고 싶지 않다. 사용자로부터
  요청을 계속 받아 카프카로 보내고, 카프카가 응답하면 그때 클라이언트에 응답을 보내고 싶다.
  이런 시나리오에서 `KafkaFuture`의 융통성이 꽤 유용해진다** (5장, p.120).[^shapira2021]
  - 형태는 **블로킹 `get()` 대신 `whenComplete`로 `Future` 완료 시 호출될 함수를 구성하는
    것**이다. 책의 예제는 Vert.x HTTP 서버 안에서 `describeTopics`를 부르고,
    **`Future`가 예외로 완료되면 HTTP 클라이언트에 에러를, 성공하면 토픽 설명을 보낸다**
    (5장, pp.120–121).[^shapira2021]
- **요점은 카프카의 응답을 기다리지 않는다는 것**이다 — **`DescribeTopicResult`가 카프카에서
  응답이 도착할 때 HTTP 클라이언트에 응답을 보내고, 그동안 HTTP 서버는 다른 요청을 계속
  처리한다** (5장, p.121).[^shapira2021]
- 확인 방법까지 책이 적어 뒀다 — **`SIGSTOP`으로 카프카를 잠시 멈추고(프로덕션에서는 하지
  말 것) Vert.x에 HTTP 요청 둘을 보내되 하나는 긴 타임아웃, 하나는 짧은 타임아웃으로 주면,
  두 번째 요청을 첫 요청 뒤에 보냈더라도 낮은 타임아웃 덕에 먼저 응답하고 첫 요청 뒤에서
  블록되지 않는다** (5장, p.121).[^shapira2021]

## 붙은 클러스터 확인하기

- **애플리케이션이 접속한 클러스터에 대해 무언가를 명시적으로 알아내야 하는 일은 드물다.
  브로커가 몇 대인지, 어느 것이 컨트롤러인지 전혀 모른 채로 메시지를 생산하고 소비할 수
  있다 — 카프카 클라이언트는 이 정보를 추상화하고, 클라이언트는 토픽과 파티션만 신경 쓰면
  된다** (5장, p.127).[^shapira2021]
- 그래도 볼 수 있다 — **`describeCluster`가 클러스터 식별자, 클러스터의 노드 목록, 컨트롤러를
  돌려준다** (5장, p.127).[^shapira2021]
  - **클러스터 식별자는 GUID라 사람이 읽을 수 없지만, 클라이언트가 올바른 클러스터에
    접속했는지 확인하는 데는 여전히 유용**하다 (5장, p.127).[^shapira2021]

## 목업으로 테스트하기

- **아파치 카프카는 `MockAdminClient` 테스트 클래스를 제공한다. 브로커 수를 원하는 만큼 주어
  초기화할 수 있고, 실제 카프카 클러스터를 돌려 실제로 어드민 작업을 수행하지 않고도
  애플리케이션이 올바르게 동작하는지 테스트하는 데 쓴다** (5장, p.131).[^shapira2021]
- 대가가 있다 — **`MockAdminClient`는 카프카 API의 일부가 아니므로 예고 없이 바뀔 수 있다.
  다만 public 메서드를 모킹하므로 메서드 시그니처는 호환이 유지된다. 이 클래스의 편의가
  그것이 바뀌어 테스트를 깨뜨릴 위험만큼 가치가 있는지는 트레이드오프**이니 유념하라고
  책은 말한다 (5장, p.131).[^shapira2021]
- **이 테스트 클래스가 특히 쓸 만한 이유는 흔히 쓰는 메서드 일부가 매우 포괄적으로 모킹돼
  있다는 것**이다 — **`MockAdminClient`로 토픽을 만들고 이어서 `listTopics()`를 부르면
  "만든" 토픽들이 나열된다** (5장, p.131).[^shapira2021]
- 버전 조건: Kafka 2.5 이하 — **모든 메서드가 모킹돼 있지는 않다. AdminClient 2.5 이하에서
  `MockAdminClient`의 `incrementalAlterConfigs()`를 부르면 `UnsupportedOperationException`이
  나오지만, 자체 구현을 주입해 처리할 수 있다** (5장, p.131).[^shapira2021]
- **책의 예제는 목킹 프레임워크로 Mockito를 쓴다** — **`MockAdminClient`의 메서드가 예상대로
  호출되는지 검증하고 미구현 메서드를 채워 넣기 위해서**이며, **Mockito가 좋은 API를 가진
  꽤 단순한 목킹 프레임워크라 작은 단위 테스트 예제에 잘 맞기 때문**이다 (5장,
  p.132).[^shapira2021] 구체적으로는 **`spy` 주입으로 대상 클래스가 제대로 실행됐는지
  나중에 확인하고, `doReturn`으로 목업 어드민 클라이언트가 예외를 던지지 않게** 한다 (5장,
  p.132).[^shapira2021]
- 의존성 한 줄이 더 필요하다 — **아파치 카프카는 `MockAdminClient`를 test jar로 배포하므로
  `pom.xml`에 `org.apache.kafka:kafka-clients`를 `test` classifier·`test` scope로 넣은 테스트
  의존성이 있어야** 한다 (5장, p.133).[^shapira2021]

## 이어지는 페이지

- [토픽 관리](../concepts/kafka-topic-administration.md) — 이 클라이언트로 하는 가장 흔한
  작업. 목록·설명·생성·삭제
- [설정 관리](../concepts/kafka-config-administration.md) — 토픽과 브로커 설정을 읽고 바꾸는 쪽
- [컨슈머 그룹 관리](../concepts/kafka-consumer-group-administration.md) — 그룹과 오프셋을
  들여다보고 바꾸는 쪽
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) —
  인시던트 때 쓰는 위험한 작업들
- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 저자들이 주키퍼 직접 수정을 말린
  이유가 실제로 실현된 곳
- [브로커와 클러스터](../concepts/brokers-and-clusters.md) — 상태 변경 요청을 받는 컨트롤러
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — 설정할 것이 훨씬 많은 쪽

[^shapira2021]: Shapira et al. 2021, 5장 "Managing Apache Kafka Programmatically" — 인용 블록은 pp.113·114·115 원문. 코드 펜스는 p.116 예제 원문 그대로다(깎거나 보탠 줄 없음)

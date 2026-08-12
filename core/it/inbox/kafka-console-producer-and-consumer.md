---
type: concept
title: 콘솔 프로듀서와 콘솔 컨슈머
description: 애플리케이션을 쓰지 않고 토픽에 손으로 쓰고 읽어 보는 두 유틸리티 — 자바 클라이언트를 감싼 껍데기라 다른 프로그램에 파이프로 물리면 안 되는 이유, 콘솔 프로듀서의 키 구분자와 설정 전달 방식, 콘솔 컨슈머의 토픽 선택과 포매터, 그리고 내부 오프셋 토픽을 열어 보는 형태
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 콘솔 프로듀서와 콘솔 컨슈머

- [두 도구의 정체](#두-도구의-정체)
- [다른 애플리케이션에 파이프로 물리지 마라](#다른-애플리케이션에-파이프로-물리지-마라)
- [콘솔 프로듀서](#콘솔-프로듀서)
- [프로듀서 설정을 넘기는 두 가지 방법](#프로듀서-설정을-넘기는-두-가지-방법)
- [줄을 읽는 방식 바꾸기](#줄을-읽는-방식-바꾸기)
- [콘솔 컨슈머](#콘솔-컨슈머)
- [메시지 포매터](#메시지-포매터)
- [오프셋 토픽 읽어 보기](#오프셋-토픽-읽어-보기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **애플리케이션을 짜지 않고 토픽에 직접 메시지를 써 보고 읽어 보려면 무엇을
쓰고, 그 도구는 무엇을 못 하는가.**

## 두 도구의 정체

- 동기는 검증이다 — **카프카로 작업하다 보면 애플리케이션에 무슨 일이 벌어지는지 확인하려고
  샘플 메시지를 손으로 생산하거나 소비해야 할 때가 자주 있다.** 그 일을 돕는 유틸리티가
  `kafka-console-consumer.sh`와 `kafka-console-producer.sh` 둘이며, **2장에서 설치를 검증할 때
  잠깐 썼던 바로 그 도구들**이다 (12장, p.320).[^shapira2021]
- 실체는 껍데기다 — **이 도구들은 주요 자바 클라이언트 라이브러리를 감싼 래퍼(wrapper)라,
  그 일을 하는 애플리케이션 전체를 짜지 않고도 카프카 토픽과 상호작용할 수 있게 해 준다**
  (12장, p.320).[^shapira2021] 감싸인 쪽은
  [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md)와
  [컨슈머 폴 루프](../concepts/kafka-consumer-poll-loop.md)다.

## 다른 애플리케이션에 파이프로 물리지 마라

- 이 도구를 파이프라인 부품으로 쓰고 싶어지는 것이 흔한 유혹이고, 책은 그것을 경고 상자로
  막는다 (12장, p.320):[^shapira2021]

  > While it is possible to write applications that wrap around the console consumer or
  > producer (e.g., to consume messages and pipe them to another application for processing),
  > this type of application is quite fragile and should be avoided. It is difficult to
  > interact with the console consumer in a way that does not lose messages. Likewise, the
  > console producer does not allow for using all features, and properly sending bytes is
  > tricky. It is best to use either the Java client libraries directly or a third-party client
  > library for other languages that use the Kafka protocol directly.

## 콘솔 프로듀서

- `kafka-console-producer.sh`로 **클러스터의 카프카 토픽에 메시지를 써넣는다.** 입력 규약은
  **기본적으로 한 줄에 메시지 하나이고, 탭 문자가 키와 값을 가른다(탭이 없으면 키는 `null`)**
  이다 (12장, p.320).[^shapira2021]
  - 원문 오식: 이 문장의 도구 이름이 `kakfa-console-producer.sh`로 인쇄돼 있다 (12장,
    p.320).[^shapira2021] 같은 쪽 앞 문단과 예제는 `kafka-console-producer.sh`다.
- 직렬화는 없다시피 하다 — **콘솔 컨슈머와 마찬가지로 프로듀서는 입력을 읽어 기본
  시리얼라이저(`DefaultEncoder`)로 로 바이트(raw bytes)를 생산**한다 (12장,
  p.320).[^shapira2021] 제대로 된 직렬화는
  [직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) 쪽이다.
- 필수 인자는 둘이다 — **어느 클러스터에 붙고 그 안의 어느 토픽에 쓸지**이며, 앞은 늘 쓰던
  `--bootstrap-server` 접속 문자열이고 뒤는 `--topic`이다. **다 썼으면 파일 끝(end-of-file,
  EOF) 문자를 보내 클라이언트를 닫는데, 대부분의 터미널에서는 Control-D**다 (12장,
  p.320).[^shapira2021]

## 프로듀서 설정을 넘기는 두 가지 방법

- **보통의 프로듀서 설정 옵션을 콘솔 프로듀서에도 넘길 수 있고**, 방법은 **넘길 옵션이 몇
  개인지와 취향에 따라 갈리는 둘**이다 — **`--producer.config <config-file>`로 설정 옵션이
  담긴 파일의 전체 경로를 주거나, `--producer-property <key>=<value>` 꼴 인자를 하나 이상
  명령줄에 주는 것**이다. **뒤쪽은 `linger.ms`나 `batch.size` 같은 메시지 배치 설정에
  유용**하다 (12장, p.321).[^shapira2021] 그 설정들의 뜻은
  [프로듀서 설정](../concepts/kafka-producer-configuration.md)에 있다.
- 헷갈리는 자리가 하나 있어 책이 상자로 떼어 뒀다 — **`--property` 명령줄 옵션은 콘솔
  프로듀서와 콘솔 컨슈머 양쪽에 있지만 `--producer-property`·`--consumer-property`와
  혼동하면 안 된다. `--property`는 메시지 포매터에 설정을 넘길 때만 쓰이고 클라이언트 자체와는
  무관하다** (12장, p.321).[^shapira2021]
- `--producer-property`와 함께 쓰는 인자 중 책이 유용하다고 꼽은 것 (12장,
  p.321):[^shapira2021]
  - `--batch-size` — **동기로 보내는 중이 아닐 때 한 배치로 보낼 메시지 수**를 지정한다.
  - `--timeout` — **프로듀서가 비동기 모드로 돌 때 배치 크기를 기다리는 최대 시간**이며,
    **쓰기가 뜸한 토픽에서 오래 기다리는 것을 막는다.**
  - `--compression-codec <string>` — **메시지를 생산할 때 쓸 압축 종류**로 **`none`·`gzip`·
    `snappy`·`zstd`·`lz4` 중 하나이며 기본값은 `gzip`**이다.
  - `--sync` — **메시지를 동기로 생산한다. 다음 메시지를 보내기 전에 각 메시지가 확인응답될
    때까지 기다린다.**

## 줄을 읽는 방식 바꾸기

- 표준 입력을 읽어 프로듀서 레코드를 만드는 책임은
  **`kafka.tools.ConsoleProducer$LineMessageReader` 클래스**에 있고, 그 옵션은 `--property`로
  넘긴다 (12장, p.322):[^shapira2021]
  - `ignore.error` — **`parse.key`가 `true`인데 키 구분자가 없을 때 예외를 던지려면 `false`로
    둔다. 기본값은 `true`.**
  - `parse.key` — **키를 항상 `null`로 두려면 `false`. 기본값은 `true`.**
  - `key.separator` — **읽을 때 메시지 키와 값 사이의 구분 문자를 지정한다. 기본값은 탭 문자.**
- 분할 규칙의 세부 — **`LineMessageReader`는 입력을 `key.separator`가 처음 나온 자리에서
  가른다. 그 뒤에 남은 문자가 없으면 메시지 값이 비고, 줄에 구분자가 없거나 `parse.key`가
  `false`면 키는 `null`**이다 (12장, p.322).[^shapira2021]
- 직접 만들어 끼울 수도 있다 — **`kafka.common.MessageReader`를 확장해 `ProducerRecord`를
  만드는 클래스를 짜고, `--line-reader` 옵션으로 지정하며, 그 클래스가 든 JAR이 클래스패스에
  있어야** 한다 (12장, p.322).[^shapira2021]

## 콘솔 컨슈머

- `kafka-console-consumer.sh`는 **클러스터의 토픽 하나 이상에서 메시지를 소비하는 수단**이며,
  **메시지는 개행으로 구분돼 표준 출력에 찍힌다.** 기본 동작은 **키 없이, 형식 없이
  (`DefaultFormatter`) 메시지의 로 바이트를 그대로 내보내는 것**이다 (12장,
  p.322).[^shapira2021]
- 시작에 필요한 기본 옵션은 셋이다 — **클러스터 접속 문자열, 소비할 토픽, 소비할 시간
  범위** (12장, p.322).[^shapira2021]
- 토픽을 고르는 방법이 둘이고 **둘 중 하나만 골라 써야** 한다 (12장, p.323):[^shapira2021]
  - `--topic` — **소비할 토픽 하나를 지정한다.**
  - `--whitelist` — **소비할 모든 토픽에 매칭되는 정규식이며, 셸이 잘못 처리하지 않도록 정규식을
    제대로 이스케이프해야** 한다.
- **콘솔 컨슈머는 한 번 시작하면 셸 이스케이프 명령(여기서는 Ctrl-C)이 주어질 때까지 계속
  소비를 시도**한다 (12장, p.323).[^shapira2021]
- 설정을 넘기는 방식은 프로듀서와 대칭이다 — **`--consumer.config <config-file>` 또는
  `--consumer-property <key>=<value>`** (12장, p.323).[^shapira2021] 그 설정들의 뜻은
  [컨슈머 설정](../concepts/kafka-consumer-configuration.md)에 있다.
- 알아 둘 만하다고 책이 꼽은 옵션들 (12장, p.324):[^shapira2021]
  - `--formatter <classname>` — **메시지를 해독할 메시지 포매터 클래스**로 기본값은
    `kafka.tools.DefaultMessageFormatter`다.
  - `--from-beginning` — **지정한 토픽을 가장 오래된 오프셋부터 소비한다. 없으면 최신
    오프셋부터** 시작한다.
  - `--max-messages <int>` — **종료하기 전에 소비할 최대 메시지 수.**
  - `--partition <int>` — **주어진 ID의 파티션에서만 소비한다.**
  - `--offset` — **소비를 시작할 오프셋 ID이며, `earliest`(처음부터)와 `latest`(가장 최근
    메시지부터)도 유효**하다.
  - `--skip-message-on-error` — **처리 중 에러가 나면 멈추는 대신 그 메시지를 건너뛴다.
    디버깅에 유용.**

## 메시지 포매터

- 기본값 말고 쓸 수 있는 포매터가 셋 있다 (12장, p.324):[^shapira2021]
  - `kafka.tools.LoggingMessageFormatter` — **표준 출력이 아니라 로거로 출력한다. 메시지는
    INFO 레벨로 찍히고 타임스탬프·키·값을 포함한다.**
  - `kafka.tools.ChecksumMessageFormatter` — **메시지 체크섬만 출력한다.**
  - `kafka.tools.NoOpMessageFormatter` — **메시지를 소비하되 전혀 출력하지 않는다.**
- 기본 포매터에도 `--property`로 주는 옵션이 여럿이다 (12장, p.325):[^shapira2021]
  - `print.timestamp`·`print.key`·`print.offset`·`print.partition` — **각각 타임스탬프(있으면)·
    키·오프셋·읽어 온 토픽 파티션을 값과 함께 표시하려면 `true`.**
  - `key.separator`·`line.separator` — **키와 값을 가르는 문자, 메시지끼리를 가르는 문자.**
  - `key.deserializer`·`value.deserializer` — **키·값을 출력하기 전에 역직렬화하는 데 쓸 클래스
    이름.**
- 역직렬화 클래스에는 조건이 붙는다 — **`org.apache.kafka.common.serialization.Deserializer`를
  구현해야 하고 콘솔 컨슈머가 그 결과에 `toString`을 불러 출력할 것을 만든다. 보통 자바
  클래스로 구현해 `kafka_console_consumer.sh` 실행 전에 `CLASSPATH` 환경 변수를 설정해 콘솔
  컨슈머의 클래스패스에 넣는다** (12장, p.325).[^shapira2021]

## 오프셋 토픽 읽어 보기

- 쓸모는 진단이다 — **클러스터 컨슈머 그룹들이 어떤 오프셋을 커밋하고 있는지 봐야 할 때가
  있다. 특정 그룹이 오프셋을 커밋하고는 있는지, 얼마나 자주 커밋하는지** 같은 것이다 (12장,
  p.325).[^shapira2021] 커밋 자체는
  [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md)에 있다.
- 방법은 **콘솔 컨슈머로 `__consumer_offsets`라는 특수 내부 토픽을 소비하는 것**이다 — **모든
  컨슈머 오프셋이 이 토픽에 메시지로 쓰이며, 그 메시지를 해독하려면 포매터 클래스
  `kafka.coordinator.group.GroupMetadataManager$OffsetsMessageFormatter`를 써야** 한다 (12장,
  p.325).[^shapira2021] 아래가 배운 것을 다 합쳐 그 토픽의 가장 이른 메시지를 읽는 형태이며,
  `__consumer_offsets`·`OffsetsMessageFormatter`·`exclude.internal.topics`로 찾는다 (12장,
  p.325):[^shapira2021]

  ```sh
  kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic __consumer_offsets --from-beginning --max-messages 1 --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" --consumer-property exclude.internal.topics=false
  ```

  - 이 토픽이 왜 내부 토픽이고 무엇을 보존하는지는
    [카프카 로그 압착](../concepts/kafka-log-compaction.md)에 있다.

## 이어지는 페이지

- [카프카 명령줄 관리 도구](../concepts/kafka-cli-admin-tools.md) — 이 도구들이 속한 도구
  모음의 전제와 버전 경고
- [컨슈머 그룹 관리](../concepts/kafka-consumer-group-administration.md) — 오프셋을 이렇게
  들여다보는 대신 도구로 다루는 쪽
- [프로듀서 설정](../concepts/kafka-producer-configuration.md) — `--producer-property`로 넘기는
  값들의 본문
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) — `--consumer-property`로 넘기는
  값들의 본문
- [직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) — 로
  바이트 대신 제대로 직렬화하는 쪽
- [로그 세그먼트 덤프와 레플리카 검증](../concepts/kafka-log-dump-and-replica-verification.md) —
  소비하지 않고 디스크에서 바로 메시지를 열어 보는 쪽

[^shapira2021]: Shapira et al. 2021, 12장 "Administering Kafka" — 인용 블록은 p.320 경고 상자 원문. 코드 펜스는 p.325 예제에서 셸 프롬프트와 출력을 덜어내고, 지면에서 네 줄로 줄바꿈된 한 명령을 한 줄로 이었다(보탠 문자 없음)

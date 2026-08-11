---
type: concept
title: 컨슈머 폴 루프
description: 컨슈머 API의 심장인 폴 루프 — 컨슈머 생성과 토픽 구독(정규식 구독의 대가 포함), poll 호출이 데이터 말고도 하는 일, 폴을 멈추면 죽은 것으로 간주되는 규칙, 스레드 안전성의 1컨슈머 1스레드 원칙, 그리고 wakeup으로 루프를 빠져나오는 방법
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 컨슈머 폴 루프

- [컨슈머 생성](#컨슈머-생성)
- [토픽 구독과 정규식 구독의 대가](#토픽-구독과-정규식-구독의-대가)
- [폴 루프](#폴-루프)
- [poll이 데이터 말고 하는 일](#poll이-데이터-말고-하는-일)
- [스레드 안전성](#스레드-안전성)
- [poll(long)에서 poll(Duration)으로](#polllong에서-pollduration으로)
- [루프를 빠져나오는 방법](#루프를-빠져나오는-방법)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **컨슈머는 어떤 루프로 데이터를 읽고, 그 루프가 멈추면 무슨 일이
일어나는가.**

## 컨슈머 생성

- 레코드 소비의 첫 단계는 `KafkaConsumer` 인스턴스를 만드는 것이며, 이는
  `KafkaProducer`를 만드는 것과 매우 비슷하다 — **넘길 속성을 담은 자바 `Properties`
  인스턴스를 만든다** (4장, p.84).[^shapira2021]
- 필수 속성은 셋이다 — `bootstrap.servers`·`key.deserializer`·`value.deserializer`
  (4장, p.84):[^shapira2021]
  - `bootstrap.servers`는 카프카 클러스터로의 연결 문자열이며 **`KafkaProducer`에서와
    정확히 같은 방식**으로 쓰인다.
  - `key.deserializer`와 `value.deserializer`는 프로듀서의 시리얼라이저와 비슷하되,
    **자바 객체를 바이트 배열로 바꾸는 클래스가 아니라 바이트 배열을 받아 자바 객체로
    바꾸는 클래스**를 지정한다.
- 엄밀히는 필수가 아니지만 **매우 흔히 쓰이는 네 번째 속성이 `group.id`**이며, 그
  `KafkaConsumer` 인스턴스가 속할 컨슈머 그룹을 지정한다. **어느 컨슈머 그룹에도 속하지
  않는 컨슈머를 만드는 것도 가능하지만 흔치 않다** (4장, p.84).[^shapira2021]

## 토픽 구독과 정규식 구독의 대가

- 컨슈머를 만든 다음 단계는 **하나 이상의 토픽을 구독하는 것**이며, `subscribe()`
  메서드는 토픽 목록을 매개변수로 받는다 (4장, p.85).[^shapira2021]
- **정규식으로 `subscribe`를 호출할 수도 있다.** 표현식이 여러 토픽 이름에 매칭될 수
  있고, **매칭되는 이름의 새 토픽이 생기면 거의 즉시 리밸런스가 일어나 컨슈머들이 그 새
  토픽에서 소비를 시작한다.** 여러 토픽에서 데이터를 소비하며 토픽들이 담는 서로 다른
  데이터 유형을 처리해야 하는 애플리케이션에 유용하다 (4장, p.85).[^shapira2021]
  - **정규식으로 여러 토픽을 구독하는 것은 카프카와 다른 시스템 사이에 데이터를 복제하거나
    스트림 처리를 하는 애플리케이션에서 가장 흔히 쓰인다.**
- 파티션이 많은 클러스터에서는 대가가 크다 (4장, p.85):[^shapira2021]
  - 클러스터에 **파티션이 3만 개 이상처럼 많다면**, **구독을 위한 토픽 필터링이
    클라이언트 쪽에서 이뤄진다**는 점을 알아야 한다.
  - 명시적 목록이 아니라 정규식으로 토픽의 부분집합을 구독하면, **컨슈머는 규칙적인
    간격으로 브로커에 모든 토픽과 그 파티션의 목록을 요청**한다. 그리고 그 목록으로 구독에
    포함할 새 토픽을 탐지해 구독한다.
  - **토픽 목록이 크고 컨슈머가 많으면 토픽·파티션 목록의 크기가 유의미해지고, 정규식
    구독은 브로커·클라이언트·네트워크에 상당한 오버헤드를 준다.** **토픽 메타데이터가
    쓰는 대역폭이 데이터 전송에 쓰는 대역폭보다 큰 경우도 있다.**
  - 권한도 필요하다 — **정규식으로 구독하려면 클라이언트가 클러스터의 모든 토픽을
    describe할 권한, 즉 클러스터 전체에 대한 완전한 `describe` 권한을 가져야 한다.**

## 폴 루프

- **컨슈머 API의 심장은 서버에 더 많은 데이터를 폴링하는 단순한 루프**다 (4장,
  p.86).[^shapira2021]
- 루프의 성질들 (4장, p.86):[^shapira2021]
  - **이것은 실제로 무한 루프다.** 컨슈머는 보통 더 많은 데이터를 위해 카프카를 계속
    폴링하는 장기 실행 애플리케이션이다.
  - `consumer.poll(timeout)`이 **이 장에서 가장 중요한 줄**이다. 원문 직인용:

    > The same way that sharks must keep moving or they die, consumers must keep
    > polling Kafka or they will be considered dead and the partitions they are
    > consuming will be handed to another consumer in the group to continue
    > consuming.

  - `poll()`에 넘기는 매개변수는 **타임아웃 간격**이며, **컨슈머 버퍼에 데이터가 없을 때
    `poll()`이 얼마나 오래 블록할지**를 제어한다. **0으로 두거나 이미 사용 가능한 레코드가
    있으면 `poll()`은 즉시 반환**하고, 아니면 지정된 밀리초만큼 기다린다.
  - `poll()`은 **레코드 목록**을 반환한다. 각 레코드에는 **레코드가 온 토픽과 파티션,
    파티션 안에서의 레코드 오프셋, 그리고 키와 밸류**가 들어 있다.
  - 처리는 대개 **데이터 저장소에 결과를 쓰거나 저장된 레코드를 갱신하는 것으로 끝난다.**
- 루프의 뼈대는 아래와 같다 — `consumer.poll`·`ConsumerRecords`로 찾는다 (4장,
  p.86):[^shapira2021]

  ```java
  Duration timeout = Duration.ofMillis(100);

  while (true) {
      ConsumerRecords<String, String> records = consumer.poll(timeout);

      for (ConsumerRecord<String, String> record : records) {
          System.out.printf("topic = %s, partition = %d, offset = %d, " +
                  "customer = %s, country = %s\n",
              record.topic(), record.partition(), record.offset(),
              record.key(), record.value());
      }
  }
  ```

## poll이 데이터 말고 하는 일

- **폴 루프는 데이터를 가져오는 것보다 훨씬 많은 일을 한다** (4장, p.87):[^shapira2021]
  - **새 컨슈머로 `poll()`을 처음 호출할 때, `GroupCoordinator`를 찾고 컨슈머 그룹에
    조인하고 파티션 배정을 받는 일을 맡는다.**
  - **리밸런스가 발동되면 그것도 관련 콜백을 포함해 폴 루프 안에서 처리된다.**
  - 그 결과 **컨슈머에서, 또는 그 리스너에 쓰인 콜백에서 잘못될 수 있는 거의 모든 것이
    `poll()`이 던지는 예외로 나타난다.**
- 폴을 멈추면 죽은 것으로 간주된다 — **`poll()`이 `max.poll.interval.ms`보다 오래
  호출되지 않으면 컨슈머는 죽은 것으로 간주돼 컨슈머 그룹에서 축출**되므로, **폴 루프
  안에서 예측 불가능한 시간 동안 블록할 수 있는 일은 피해야 한다** (4장,
  p.87).[^shapira2021]

## 스레드 안전성

- 규칙은 단순하다 — **같은 그룹에 속하는 여러 컨슈머를 한 스레드에 둘 수 없고, 여러
  스레드가 같은 컨슈머를 안전하게 쓸 수도 없다. 스레드당 컨슈머 하나가 규칙이다** (4장,
  p.87).[^shapira2021]
- 한 애플리케이션에서 같은 그룹의 컨슈머를 여럿 돌리려면 **각각을 자기 스레드에서
  실행해야 한다.** **컨슈머 로직을 자기 객체로 감싸고 자바의 `ExecutorService`로 각자
  컨슈머를 가진 여러 스레드를 시작하는 것이 유용하다** (4장, p.87).[^shapira2021]
- 다른 접근도 있다 — **컨슈머 하나가 이벤트 큐를 채우고 여러 워커 스레드가 그 큐에서
  작업을 수행하는 패턴**이다 (4장, p.88).[^shapira2021]

## poll(long)에서 poll(Duration)으로

- 옛 버전의 카프카에서 전체 메서드 시그니처는 `poll(long)`이었으나 **이 시그니처는 이제
  폐기 예정이고 새 API는 `poll(Duration)`**이다. 인자 타입이 바뀌었을 뿐 아니라 **블록
  방식의 의미론이 미묘하게 달라졌다** (4장, p.87).[^shapira2021]
  - `poll(long)`은 **타임아웃 시간보다 오래 걸리더라도 필요한 메타데이터를 얻는 데 걸리는
    만큼 블록한다.**
  - `poll(Duration)`은 **타임아웃 제약을 지키며 메타데이터를 기다리지 않는다.**
- 그래서 이관에 함정이 있다 — **레코드를 소비하지 않고 카프카가 메타데이터를 가져오게
  하려고 `poll(0)`을 쓰던 코드(꽤 흔한 편법)는 `poll(Duration.ofMillis(0))`으로 그냥
  바꾸고 같은 동작을 기대할 수 없다.** 목표를 달성할 새 방법을 찾아야 하며, **흔한 해법은
  그 로직을 `rebalanceListener.onPartitionAssignment()` 메서드에 넣는 것**이다 — 이
  메서드는 **배정된 파티션의 메타데이터를 갖게 된 뒤, 그러나 레코드가 도착하기 전에
  호출되는 것이 보장된다** (4장, p.87).[^shapira2021]

## 루프를 빠져나오는 방법

- 컨슈머를 종료하기로 했는데 **컨슈머가 긴 `poll()`에서 대기 중일 수 있는 상황에서 즉시
  빠져나오고 싶다면, 다른 스레드에서 `consumer.wakeup()`을 호출해야 한다.** 메인
  스레드에서 컨슈머 루프를 돌리고 있다면 `ShutdownHook`에서 호출할 수 있다 (4장,
  p.105).[^shapira2021]
- `consumer.wakeup()`은 **다른 스레드에서 호출해도 안전한 유일한 컨슈머 메서드**다 (4장,
  p.105).[^shapira2021]
- 호출의 효과 (4장, p.105):[^shapira2021]
  - `wakeup`을 호출하면 **`poll()`이 `WakeupException`과 함께 빠져나온다.** 스레드가
    `poll`에서 대기 중이 아닐 때 호출됐다면 **다음번 `poll()` 호출에서 예외가 던져진다.**
  - **`WakeupException`은 처리할 필요가 없지만, 스레드를 빠져나가기 전에 반드시
    `consumer.close()`를 호출해야 한다.**
  - **컨슈머를 닫으면 필요하면 오프셋을 커밋하고, 그룹 코디네이터에게 컨슈머가 그룹을
    떠난다는 메시지를 보낸다.** 그러면 **컨슈머 코디네이터가 즉시 리밸런싱을 발동**하므로
    **세션 타임아웃을 기다릴 필요 없이** 닫히는 컨슈머의 파티션이 그룹의 다른 컨슈머에
    배정된다.
- 폴 타임아웃 길이의 판단도 여기 걸린다 — **폴 루프가 충분히 짧고 종료 전에 조금 기다려도
  괜찮다면 `wakeup`을 부를 필요 없이 각 반복에서 원자적 불리언을 확인하는 것으로
  충분하다.** 긴 폴 타임아웃은 **저처리량 토픽을 소비할 때 유용하다** — 브로커가 반환할
  새 데이터가 없는 동안 계속 루프를 도는 데 CPU를 덜 쓰게 된다 (4장,
  p.106).[^shapira2021]

## 이어지는 페이지

- [컨슈머 그룹과 리밸런스](../concepts/kafka-consumer-groups-and-rebalance.md) — 첫
  `poll()`이 조인하는 그 그룹과 리밸런스 콜백
- [컨슈머 설정](../concepts/kafka-consumer-configuration.md) —
  `max.poll.interval.ms`·`max.poll.records`·페치 크기 설정
- [오프셋 커밋 전략](../concepts/kafka-offset-commit-strategies.md) — 루프 안에서 무엇을
  언제 커밋할 것인가
- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md)
  — `key.deserializer`·`value.deserializer`에 무엇을 넣을 것인가
- [프로듀서와 컨슈머](../concepts/producers-and-consumers.md) — 컨슈머의 개요

[^shapira2021]: Shapira et al. 2021, 4장 "Kafka Consumers: Reading Data from Kafka" — 코드 펜스는 p.86 예제에서 원문의 주석 번호 표식과 예제용 집계·JSON 출력부를 덜어냈다(보탠 줄 없음)

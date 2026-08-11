---
type: concept
title: 카프카 클라이언트 쿼터
description: 브로커가 클라이언트의 쓰기·읽기 속도를 제한하는 기제 — 쿼터 3종과 적용 대상, 정적 설정 대신 동적 설정을 쓰는 이유, 스로틀링이 요청 지연과 채널 뮤트로 집행되는 방식, 그리고 쿼터에 걸린 프로듀서가 버퍼를 채우고 타임아웃으로 터지는 경로
generated: { by: "claude-opus-5", at: "2026-08-12T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 클라이언트 쿼터

- [쿼터 3종과 적용 대상](#쿼터-3종과-적용-대상)
- [정적 설정과 동적 설정](#정적-설정과-동적-설정)
- [스로틀링의 집행 방식](#스로틀링의-집행-방식)
- [쿼터에 걸린 프로듀서가 터지는 경로](#쿼터에-걸린-프로듀서가-터지는-경로)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **브로커는 클라이언트가 얼마나 빨리 쓰고 읽을지를 어떻게 제한하고,
제한에 걸린 클라이언트에는 무슨 일이 일어나는가.**

## 쿼터 3종과 적용 대상

- 카프카 브로커에는 **메시지가 생산·소비되는 속도를 제한하는 기능**이 있고 이는 쿼터
  (quota) 기제로 이뤄진다. 쿼터 유형은 셋이다 — **produce·consume·request** (3장,
  p.73).[^shapira2021]
  - produce·consume 쿼터는 **클라이언트가 데이터를 보내고 받는 속도를 초당 바이트
    단위로** 제한한다.
  - request 쿼터는 **브로커가 클라이언트 요청을 처리하는 데 쓰는 시간의 백분율**을
    제한한다.
- 적용 대상은 **기본 쿼터로 모든 클라이언트에, 또는 특정 client-id에, 또는 특정
  사용자에, 또는 둘 다에** 걸 수 있다. **사용자별 쿼터는 보안이 구성되고 클라이언트가
  인증하는 클러스터에서만 의미가 있다** (3장, p.73).[^shapira2021]

## 정적 설정과 동적 설정

- 모든 클라이언트에 적용되는 **기본 produce·consume 쿼터는 카프카 브로커 설정 파일의
  일부**다. 예컨대 프로듀서마다 평균 2MBps를 넘기지 못하게 하려면 브로커 설정 파일에
  `quota.producer.default=2M`을 넣는다 (3장, p.73).[^shapira2021]
- **권장되지는 않지만** 브로커 설정 파일에서 특정 클라이언트의 쿼터로 기본값을 덮을 수도
  있다 — clientA에 4MBps, clientB에 10MBps를 주려면
  `quota.producer.override="clientA:4M,clientB:10M"` 형태를 쓴다 (3장,
  pp.73–74).[^shapira2021]
- 설정 파일에 적힌 쿼터가 권장되지 않는 이유는 **정적**이라는 데 있다 — **바꾸려면 설정을
  고치고 모든 브로커를 재시작해야 하는데, 새 클라이언트는 아무 때나 들어올 수 있으므로
  매우 불편하다.** 그래서 특정 클라이언트에 쿼터를 적용하는 통상적 방법은
  `kafka-configs.sh`나 AdminClient API로 설정할 수 있는 **동적 설정**이다 (3장,
  p.74).[^shapira2021]
- 동적 쿼터 설정의 실제 형태는 아래와 같다 — `kafka-configs`·`--add-config`로 찾는다
  (3장, p.74):[^shapira2021]

  ```sh
  bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config 'producer_byte_rate=1024' --entity-name clientC --entity-type clients

  bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config 'producer_byte_rate=1024,consumer_byte_rate=2048' --entity-name user1 --entity-type users

  bin/kafka-configs --bootstrap-server localhost:9092 --alter --add-config 'consumer_byte_rate=2048' --entity-type users
  ```

  - 첫째는 **client-id로 식별되는 clientC**를 초당 1024바이트 생산으로 제한한다.
  - 둘째는 **인증된 주체(principal)로 식별되는 user1**을 초당 1024바이트 생산·2048바이트
    소비로 제한한다.
  - 셋째는 **더 구체적인 덮어쓰기가 있는 사용자를 제외한 모든 사용자**를 초당 2048바이트
    소비로 제한한다. 이것이 **기본 쿼터를 동적으로 수정하는 방법**이다.

## 스로틀링의 집행 방식

- 클라이언트가 쿼터에 도달하면 **브로커는 쿼터 초과를 막기 위해 그 클라이언트의 요청을
  스로틀링(throttling)하기 시작한다** — 즉 **클라이언트 요청에 대한 응답을 지연시킨다**
  (3장, p.74).[^shapira2021]
- 대부분의 클라이언트에서는 이것만으로 **요청 속도가 자동으로 낮아진다** — **인플라이트
  요청 수가 제한돼 있기 때문**이며, 그 결과 클라이언트 트래픽이 허용 수준까지 내려온다
  (3장, p.74).[^shapira2021]
- 그것으로 부족한 경우가 있어 방어책이 하나 더 있다 — **스로틀링 중인데도 추가 요청을
  보내는 잘못 동작하는 클라이언트로부터 브로커를 보호하기 위해, 브로커는 쿼터 준수에
  필요한 시간 동안 그 클라이언트와의 통신 채널을 뮤트(mute)한다** (3장,
  p.74).[^shapira2021]
- 스로틀링 동작은 지표로 클라이언트에 노출된다 — `produce-throttle-time-avg`·
  `produce-throttle-time-max`·`fetch-throttle-time-avg`·`fetch-throttle-time-max`가
  **프로듀스 요청과 페치 요청이 스로틀링으로 지연된 시간의 평균과 최댓값**을 담는다
  (3장, p.74).[^shapira2021]
  - 주의할 해석: **이 시간은 생산·소비 처리량 쿼터에 의한 스로틀링일 수도, 요청 시간
    쿼터에 의한 것일 수도, 둘 다일 수도 있다.** 다른 유형의 클라이언트 요청은 요청 시간
    쿼터로만 스로틀링될 수 있으며 그 역시 비슷한 지표로 노출된다.

## 쿼터에 걸린 프로듀서가 터지는 경로

- 비동기 `Producer.send()`를 쓰면서 **브로커가 수용할 수 있는 속도보다 빠르게 계속 보내면
  — 그 원인이 쿼터든 그냥 용량 부족이든 — 메시지는 먼저 클라이언트 메모리에 큐잉된다**
  (3장, p.75).[^shapira2021]
- 그 뒤의 연쇄는 이렇다 (3장, p.75):[^shapira2021]
  - 보내는 속도가 수용 속도보다 계속 높으면 **클라이언트는 결국 초과 메시지를 저장할
    버퍼 공간이 고갈되고 다음 `Producer.send()` 호출을 블록한다.**
  - **타임아웃 지연이 브로커가 따라잡아 버퍼를 비울 만큼 충분하지 않으면 결국
    `Producer.send()`가 `TimeoutException`을 던진다.**
  - 또는 **이미 배치에 놓인 레코드들이 `delivery.timeout.ms`보다 오래 기다려 만료되고,
    그 결과 `send()` 콜백이 `TimeoutException`과 함께 호출된다.**
  - 따라서 **시간에 따른 브로커 용량이 프로듀서의 전송 속도와 맞도록 계획하고 모니터링하는
    것이 중요하다.**

## 이어지는 페이지

- [프로듀서 설정](../concepts/kafka-producer-configuration.md) —
  `buffer.memory`·`max.block.ms`·`delivery.timeout.ms`가 이 경로를 만든다
- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — 스로틀링이 지연시키는
  그 응답이 오는 곳
- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 브로커가 요청을 처리하는
  시간이 request 쿼터의 대상이 된다
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 기본 쿼터가 놓이는
  브로커 설정 파일

[^shapira2021]: Shapira et al. 2021, 3장 "Kafka Producers: Writing Messages to Kafka" — 코드 펜스는 p.74 예제 세 줄에서 원문의 주석 번호 표식과 지면 줄바꿈을 덜어냈다(보탠 줄 없음)

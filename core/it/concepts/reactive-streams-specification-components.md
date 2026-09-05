---
type: concept
title: 리액티브 스트림 규격과 네 구성 요소
description: 리액티브 스트림을 배압을 갖춘 비동기 데이터 흐름 관리 표준으로 정의한 자리, 파이프라인이 구독자가 붙기 전에는 게으르다는 성질, 발행자와 구독자와 구독과 프로세서라는 네 구성 요소와 세 가지 신호, 리액터와 RxJava가 주는 타입들, 그리고 자바 스트림과 같지 않다는 구분
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 리액티브 스트림 규격과 네 구성 요소

- [정의](#정의)
- [파이프라인과 게으름](#파이프라인과-게으름)
- [네 구성 요소](#네-구성-요소)
- [세 가지 신호](#세-가지-신호)
- [두 라이브러리의 타입](#두-라이브러리의-타입)
- [자바 스트림과 같지 않다](#자바-스트림과-같지-않다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **리액티브 스트림은 무엇으로 이루어지고 어떤 신호를 주고받는가.**

## 정의

- 자바의 리액티브 프로그래밍은 비동기이고 논블로킹이고 이벤트 기반인 애플리케이션을 중심에 둔
  패러다임이며, 그 핵심 개념이 리액티브 스트림(reactive stream)이라고 저자가 적는다 (6장
  "Reactive Programming in Java", p.279).[^rahman2025]

  > A core concept is the *reactive stream*, a standard (defined by the Reactive Streams
  > Specification) for managing asynchronous data flows with *backpressure*.

- 한국어로 옮기면 리액티브 스트림은 배압(backpressure)을 갖춘 비동기 데이터 흐름을 관리하기 위한
  표준이며, 리액티브 스트림 명세(Reactive Streams Specification)가 그것을 정의한다 (6장,
  p.279).[^rahman2025] 배압 자체는
  [배압과 리액터의 다섯 전략](../concepts/backpressure-strategies-in-reactive-streams.md)이 다룬다.

## 파이프라인과 게으름

- 코드를 조직하는 단위가 스트림이다 — 리액티브 프로그래밍에서는 코드를 스트림 중심으로 구성하며,
  변환들의 연결을 파이프라인(pipeline)이라 부른다. 이 패러다임에서는 모든 것을 생산자에서 소비자로
  일련의 변환을 거쳐 흐르는 이벤트의 스트림으로 볼 수 있다 (6장 "Understanding Reactive Streams",
  p.279).[^rahman2025]
- 이벤트는 무엇이든 될 수 있다 — 사용자 클릭, 센서 측정값, 수신된 메시지가 저자의 예다. 이벤트는
  업스트림 소스에서 다운스트림 구독자(Subscriber)로 이동하며 그 사이에서 데이터를 변환하거나
  걸러 내는 연산자(operator)들을 지난다 (6장, p.279).[^rahman2025]
- 연산자마다 새 스트림을 낳는다 — 각 연산자는 자기 업스트림을 관찰하고 새 스트림을 생산한다 (6장,
  p.279).[^rahman2025]
- 그러나 기본이 게으름이다 — 스트림은 구독자가 생기기 전까지 처리를 시작하지 않는다 (6장,
  p.279).[^rahman2025]
- 그래서 관찰자를 미리 세워 둔다 — 이벤트가 **언제** 도착할지 알 수 없으므로(비동기이므로) 도착했을
  때 반응할 관찰자를 설정해 둔다 (6장, pp.279–280).[^rahman2025]
- 저자가 기본 파이프라인 하나를 보인다. 정수 다섯을 흘리는 스트림에 필터와 매핑을 걸고 구독하는
  모양이다 (6장, p.281).[^rahman2025]

  ```java
  Flux<Integer> numbers = Flux.just(1, 2, 3, 4, 5);
  numbers
      .filter(n -> n % 2 == 0)
      .map(n -> "Value: " + n)
      .subscribe(
          System.out::println,
          error -> System.err.println("Error: " + error),
          () -> System.out.println("Done!")
      );
  ```

  - 저자가 여섯 갈래로 읽는다 — 값 다섯을 담은 차가운 스트림을 만들고(구독자가 붙기 전에는 아무 값도
    내보내지 않는다), 필터 연산자가 조건에 맞는 원소만 담은 새 스트림을 만들고, 매핑 연산자가 각
    원소를 변환하고, 구독 메서드가 파이프라인 실행을 발동시키며 각 값을 어떻게 다룰지 정하고,
    파이프라인의 어느 연산자든 예외를 던지면 오류 처리 콜백이 실행되고, 스트림이 모든 방출을 마치면
    완료 콜백이 실행된다 (6장, p.281).[^rahman2025]

## 네 구성 요소

- 리액티브 프로그래밍이 다루는 근본 구성 요소가 넷이다 (6장, p.280):[^rahman2025]
  - 발행자(Publisher) — 데이터 항목을 비동기로 내보내는 소스다. 시간에 걸쳐 0개 이상의 항목을 내보낼
    수 있는 데이터 생산자로 생각하면 된다.
  - 구독자(Subscriber) — 내보내진 항목을 받아 처리하는 소비자다. 데이터를 받겠다는 관심을 표명하고
    그것을 어떻게 다룰지 정의한다.
  - 구독(Subscription) — 발행자와 구독자를 잇는 연결이다. 데이터의 흐름을 관리하고 배압 제어를
    가능하게 한다.
  - 프로세서(Processor) — 구독자이자 발행자로 동시에 동작하는 구성 요소다. 데이터가 스트림을 지나는
    동안 그것을 변환한다.

## 세 가지 신호

- 리액티브 스트림이 내보낼 수 있는 신호가 셋이다 (6장, p.280):[^rahman2025]
  - 데이터 항목 — 스트림을 흐르는 실제 값들.
  - 오류 신호 — 복구 불가능한 오류가 일어났음을 알리며 스트림을 종료시킨다.
  - 완료 신호 — 더 내보낼 항목이 없이 스트림이 성공적으로 끝났음을 알린다.

## 두 라이브러리의 타입

- 자바에는 리액티브 프로그래밍 라이브러리가 여럿 있고 저자가 가장 눈에 띄는 둘을 든다 (6장,
  p.280):[^rahman2025]
  - Project Reactor는 핵심 타입 둘을 준다. `Flux<T>`는 0개에서 N개까지의 항목을, `Mono<T>`는
    0개에서 1개까지의 항목을 다룬다.
  - RxJava는 자바를 위한 리액티브 확장이며 타입 셋을 준다. `Observable<T>`는 0개에서 N개까지,
    `Single<T>`는 정확히 하나, `Maybe<T>`는 0개에서 1개까지의 항목을 다룬다.
- 저자가 범위를 스스로 긋는다 — 이것은 리액티브 스트림에 대한 높은 수준의 소개이며, 이 책은 모든
  세부를 다루려는 것이 아니라 리액티브 프로그래밍이 어떤 것인지 맛보게 하려는 것이다. 더 배우고
  싶으면 그 주제를 전담한 책을 보라고 권한다 (6장, p.286).[^rahman2025]

## 자바 스트림과 같지 않다

- 저자가 상자 하나로 혼동을 막는다 — 리액티브 스트림은 자바 스트림과 같지 않다 (6장,
  p.286):[^rahman2025]
  - `java.util.stream.Stream`, 곧 자바 스트림 API는 컬렉션을 동기로, 메모리 안에서 처리하는 데
    쓰인다.
  - 리액티브 스트림은 비동기이고 이벤트 기반이고 논블로킹인 데이터 처리를 다루며 배압을 지원한다.

## 이어지는 페이지

- [배압과 리액터의 다섯 전략](../concepts/backpressure-strategies-in-reactive-streams.md) — 정의에
  들어 있는 그 배압
- [리액티브 프로그래밍이라는 패러다임](../concepts/reactive-programming-paradigm-definition.md) —
  이 규격이 구현하는 패러다임
- [비동기 API의 모양과 콜백 지옥](../concepts/async-api-shapes-and-callback-hell.md) — 값 하나를
  다루는 앞 단계와 그 한계
- [가상 스레드 시대에 리액티브가 남는 자리](../concepts/reactive-and-virtual-threads-coexistence.md)
  — 같은 시스템을 가상 스레드로 지으면 무엇이 달라지는가
- [복잡 이벤트 처리와 스트림 검색](../concepts/complex-event-processing-and-stream-search.md) —
  스트림을 데이터 시스템 층에서 본 자리
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    "Reactive Programming in Java"(p.279), "Understanding Reactive Streams"(pp.279–286),
    리액티브 스트림과 자바 스트림을 가르는 상자(p.286). 인용한 파이프라인은 원문(p.281)의
    `ReactiveExample`에서 클래스와 `main` 선언과 주석과 코드 옆 번호 표식을 뺐다.
    `SimplePriceMonitor`(p.282)와 `CryptoPriceMonitor`(pp.283–284)와 그 보조
    메서드들(pp.285–286)은 개념당 대표 코드 하나 규칙에 따라 옮기지 않았다.
    그림 6-2(p.279, 리액티브 프로그래밍 데이터 흐름)는 미수록이며 본문이 말한 흐름만 옮겼다.

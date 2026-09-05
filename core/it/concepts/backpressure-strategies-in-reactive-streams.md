---
type: concept
title: 배압과 리액터의 다섯 전략
description: 하류 소비자가 따라가지 못한다고 상류 생산자에게 신호를 보내는 기제로서의 배압 정의, 리액터가 주는 다섯 가지 전략과 각각을 쓸 자리, 그리고 초고빈도 시세 피드 예제가 보이는 표본 추출과 폐기와 최신 값 유지라는 세 가지 실물
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 배압과 리액터의 다섯 전략

- [정의](#정의)
- [다섯 전략과 쓸 자리](#다섯-전략과-쓸-자리)
- [예제가 보이는 셋](#예제가-보이는-셋)
- [다른 층에서 본 같은 이름](#다른-층에서-본-같은-이름)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **소비자가 생산자를 따라가지 못할 때 스트림은 무엇을 할 수 있는가.**

## 정의

- 저자가 배압(backpressure)을 리액티브 프로그래밍에 없어서는 안 될 기제로 정의한다 (6장
  "Backpressure", p.286).[^rahman2025]

  > backpressure is an integral mechanism that enables a downstream consumer (Subscriber) to
  > signal an upstream producer (Publisher) when it is unable to process data.

- 한국어로 옮기면 배압은 하류 소비자, 곧 구독자(Subscriber)가 데이터를 처리할 수 없을 때 상류
  생산자, 곧 발행자(Publisher)에게 그 사실을 신호로 알리게 해 주는 기제다 (6장,
  p.286).[^rahman2025]
- 저자가 그 뜻을 한 문장으로 풀어 준다 — 본질적으로 소비자가 속도를 늦추라고, 이만큼 빨리는 처리할
  수 없다고 말할 수 있게 해 주는 것이다 (6장, p.286).[^rahman2025]

## 다섯 전략과 쓸 자리

- 리액터가 배압을 다루는 전략을 여럿 준다. 저자가 다섯을 쓸 자리와 함께 나열한다 (6장,
  p.288):[^rahman2025]
  - `onBackpressureBuffer()` — 소비자가 따라잡을 때까지 모든 항목을 버퍼에 담는다. 데이터를 하나도
    잃으면 안 되고 메모리는 여유가 있을 때 쓴다.
  - `onBackpressureBuffer(maxSize)` — 상한을 두고 버퍼에 담으며, 넘으면 실패한다. 메모리 고갈에
    대한 안전장치를 준다.
  - `onBackpressureDrop()` — 넘치는 항목을 조용히 버린다. 완전함보다 최신 값이 더 중요한 실시간
    데이터에 쓴다.
  - `onBackpressureLatest()` — 가장 최근 항목 하나만 남긴다. 중간 값들이 곧 무의미해지는 상태 갱신에
    이상적이다.
  - `onBackpressureError()` — 배압이 생기면 즉시 실패한다. 배압이 나타난다는 것 자체가 시스템 설계의
    결함을 뜻하는 경우에 쓴다.

## 예제가 보이는 셋

- 저자는 고빈도 거래 시나리오로 전략들을 살펴본다. 예제의 피드는 초당 1만 개의 항목을 내보내며
  고빈도 거래 데이터를 흉내 낸다 (6장, pp.286·288).[^rahman2025]
- 첫째가 표본 추출이다 — 주기적으로 스냅샷을 뜬다. 규칙적인 갱신이 필요하지만 모든 항목을 처리할
  수는 없을 때 이상적이다 (6장, p.288).[^rahman2025]
- 둘째가 폐기다 — 소비자가 따라가지 못할 때 항목을 버린다. 일부 데이터를 놓쳐도 괜찮은 경우에
  적합하다 (6장, p.288).[^rahman2025]
- 셋째가 최신 값 유지다 — 처리되지 않은 항목 가운데 가장 최근 것만 남긴다. 현재 상태만 중요한
  시나리오에 딱 맞는다 (6장, p.288).[^rahman2025]

  ```java
  extremeFeed
      .onBackpressureLatest()
      .publishOn(Schedulers.boundedElastic())
      .subscribe(price -> {
          simulateWork(100);
          System.out.printf("[LATEST] Price: $%.2f%n", price.price());
      });
  ```

- 연산자 하나가 더 끼어 있다 — `publishOn`은 처리를 다른 스레드 풀로 옮겨 생산과 소비를 갈라
  놓는다 (6장, p.288).[^rahman2025]
- 저자가 이 예제의 값을 정리한다 — 리액티브 스트림이 현실의 시나리오에서 어떻게 동작하는지를
  보이면서 발행자와 연산자와 구독자와 배압이라는 개념들을 잇는다 (6장, p.288).[^rahman2025]

## 다른 층에서 본 같은 이름

- 같은 낱말이 KB의 다른 층에도 있다. 분산 시스템의 큐 앞에서 프로듀서를 늦추는 전략으로서의 배압은
  [분산 컴퓨팅의 오류들](../concepts/fallacies-of-distributed-computing.md)에 있고, 저장 엔진이
  컴팩션을 따라가지 못할 때 읽기와 쓰기를 멈추는 배압은
  [B 트리와 LSM 트리 비교](../concepts/comparing-b-trees-and-lsm-trees.md)에 있다. 이 페이지가
  다루는 것은 그 둘과 층이 다르다 — 스트림 API 안에서 구독자가 발행자에게 보내는 신호다.

## 이어지는 페이지

- [리액티브 스트림 규격과 네 구성 요소](../concepts/reactive-streams-specification-components.md) —
  이 기제가 사는 규격
- [가상 스레드 시대에 리액티브가 남는 자리](../concepts/reactive-and-virtual-threads-coexistence.md)
  — 저자가 가상 스레드에 없다고 꼽는 바로 그것
- [분산 컴퓨팅의 오류들](../concepts/fallacies-of-distributed-computing.md) — 분산 시스템 층의 배압
- [B 트리와 LSM 트리 비교](../concepts/comparing-b-trees-and-lsm-trees.md) — 저장 엔진 층의 배압
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    "Backpressure"(pp.286–288). 인용한 최신 값 전략은 원문(p.287)의 `BackpressureDemo`에서 그
    갈래만 떼어 내고 로그 출력 한 줄과 주석을 뺐다. 표본 추출과 폐기 갈래와 피드 선언과
    `simulateWork`(pp.286–287)는 개념당 대표 코드 하나 규칙에 따라 옮기지 않았다. 실행 출력은
    실려 있지 않다. 이 절에는 그림이 없다.

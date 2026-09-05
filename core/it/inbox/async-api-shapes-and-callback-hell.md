---
type: concept
title: 비동기 API의 모양과 콜백 지옥
description: 호출자가 기다리는 동기 API와 즉시 반환하고 콜백으로 결과를 넘기는 비동기 API의 대비, 콜백을 이어 붙이려 하면 중첩이 깊어져 읽기 어려워진다는 관찰, 그리고 그 자리를 CompletableFuture가 정리하고 나서도 남는 한계인 값 하나와 데이터의 흐름
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 비동기 API의 모양과 콜백 지옥

- [동기 API](#동기-api)
- [콜백을 받는 API](#콜백을-받는-api)
- [이어 붙이려 하면 무너진다](#이어-붙이려-하면-무너진다)
- [정리하고도 남는 한계](#정리하고도-남는-한계)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **막지 않는 API는 어떤 모양을 하며, 가장 단순한 모양은 왜 오래가지 못하는가.**

## 동기 API

- 저자가 아주 단순한 메서드 하나로 시작한다 — 문자열을 받아 처리하고 응답을 돌려주는 메서드다
  (6장 "Asynchronous APIs", pp.276–277).[^rahman2025]
- 그 호출의 성격이 동기 API(synchronous API)의 전형이다 — 호출한 스레드가 그 메서드를 실행하고
  응답을 받을 때까지 실행을 막는다. 호출자가 기다려야 한다는 것이 정의다 (6장,
  p.277).[^rahman2025]

## 콜백을 받는 API

- 비동기로 바꾸는 방법을 저자가 제시한다 — 결과를 기다리는 대신 메서드가 즉시 반환하게 하고,
  응답이 준비되면 콜백 함수가 그것을 다루게 한다 (6장, p.277).[^rahman2025]
- 고친 메서드는 매개변수를 둘 받는다. 메시지 자체와, 응답이 준비되면 불릴 `Consumer<String>` 타입의
  콜백 함수다 (6장, p.277).[^rahman2025]

  ```java
  public void chat(String message, Consumer<String> consumer) {
      Thread.startVirtualThread(() -> {
          String response = "Echo: " + message.toUpperCase();
          consumer.accept(response);
      });
  }
  ```

- 호출 쪽에서 무엇이 달라지는지를 저자가 짚는다 — 첫 호출이 이루어지지만 주 스레드는 결과를 기다리지
  않고 곧바로 둘째 호출을 실행한다. 응답은 준비되는 대로 비동기로 처리된다. 저자는 이것이 비동기
  프로그래밍의 본질이라고 적는다. 결과를 기다리는 동안 주 스레드를 풀어 다른 일을 하게 하는 것이다
  (6장, p.277).[^rahman2025]

## 이어 붙이려 하면 무너진다

- 그런데 콜백에는 본디부터 있는 문제가 있다고 저자가 적는다 — 잘 통합되지 않는다는 것이다. 첫
  콜백의 결과를 또 다른 호출로 넘기고 싶으면 콜백 안에 콜백을 넣게 된다 (6장,
  p.277).[^rahman2025]
- 저자가 네 겹으로 중첩한 예를 보이고 결론을 낸다 — 비동기 실행에 콜백을 쓰면 금세 감당하기
  어려워진다. 콜백을 더할수록 코드를 읽고 유지하기 어려워지며, 흔히 콜백 지옥(callback hell)이라
  불리는 상태가 된다 (6장, pp.277–278).[^rahman2025]

## 정리하고도 남는 한계

- 자바가 주는 더 깔끔한 해법이 `CompletableFuture`라고 저자가 적는다. 비동기 코드를 읽을 수 있고
  구조화되어 있고 조합 가능한 채로 쓰게 해 준다 (6장, p.278).[^rahman2025] 그 API의 이득과 대가는
  [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md)에 있다.
- 중첩 대신 체인이 된다 — 반환 타입을 `CompletableFuture<String>`으로 바꾸면 여러 비동기 호출을 더
  구조화된 방식으로 이어 붙일 수 있고, 중첩 콜백을 다루는 것보다 훨씬 쉬워진다. 저자는 오류 처리는
  아직 다루지 않았지만 이 API가 실패를 다루는 풍부한 수단을 준다고 덧붙인다 (6장,
  p.278).[^rahman2025]
- 그러고도 남는 것이 있다고 저자가 스스로 묻는다 — 그러면 I/O 스레드를 막는 문제가 풀린 것인가.
  아직 고려하지 않은 것이 데이터의 흐름이다 (6장, p.278).[^rahman2025]
- 한계가 여기서 특정된다 — `CompletableFuture`는 값 하나를 돌려주는 메서드에는 아름답게 동작하지만,
  결과의 연속을 다뤄야 할 때는 다르다. 한 번의 응답이 아니라 데이터가 계속 흐르는 경우다 (6장,
  p.278).[^rahman2025]
- 그 자리가 리액티브 프레임워크가 가장 빛나는 곳이라는 것이 저자의 다음 문장이다 (6장,
  p.278).[^rahman2025]

## 이어지는 페이지

- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 콜백을 체인으로
  바꾸는 API의 전모
- [리액티브 스트림 규격과 네 구성 요소](../concepts/reactive-streams-specification-components.md) —
  값 하나가 아니라 흐름을 다루는 쪽
- [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md) — 이
  API들이 지키려는 규칙
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 콜백도
  체인도 없이 같은 효율을 노리는 쪽
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    "Asynchronous APIs"(pp.276–278). 인용한 콜백 판 `chat`은 원문(p.277)에서 예외 처리 블록만
    뺐다. 동기 판 `AiService`(p.276)와 네 겹 중첩 예제(pp.277–278)와 `CompletableFuture` 판과 그
    체인(p.278)은 개념당 대표 코드 하나 규칙에 따라 옮기지 않았다. 이 절에는 그림이 없다.

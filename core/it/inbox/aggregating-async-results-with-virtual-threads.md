---
type: concept
title: 가상 스레드로 비동기 결과 모으기
description: 가상 스레드에서는 Future의 블로킹 get을 성능 손해 없이 부를 수 있다는 것, 그래서 여러 비동기 결과를 모으는 일이 콜백 구조나 별도 동기화 없이 순차 코드로 써진다는 것, 그리고 결과 타입이 같은 태스크 묶음에는 invokeAll이 남아 있다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드로 비동기 결과 모으기

- [버전 조건](#버전-조건)
- [블로킹 get의 값이 사라졌다](#블로킹-get의-값이-사라졌다)
- [여러 결과를 모으는 자리](#여러-결과를-모으는-자리)
- [같은 타입의 묶음에는 invokeAll](#같은-타입의-묶음에는-invokeall)
- [이 방식이 남기는 결함](#이-방식이-남기는-결함)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드를 쓰면 비동기 결과를 모으는 코드가 어떻게 달라지는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 블로킹 `get`이 싸다는 전제가 가상 스레드에서만 성립한다.

## 블로킹 get의 값이 사라졌다

- 자바에서 비동기 태스크가 끝나기를 기다리며 블로킹하는 부담이 사실상 걷혔다는 것이 저자의 요지다.
  이제 `Future`의 블로킹 `get`을 성능 손해 없이 부를 수 있다 (2장, p.47).[^rahman2025]
- 이유는 무게다 — 가상 스레드가 가볍고 효율적이라서 자원을 과하게 쓰거나 성능을 떨어뜨리지 않고
  편하게 블로킹해 결과를 기다릴 수 있다 (2장, p.48).[^rahman2025] 그 기제가
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)의
  언마운트다.

## 여러 결과를 모으는 자리

- 저자가 진가로 꼽는 것은 여러 비동기 태스크의 결과를 모을 때다 (2장, p.47).[^rahman2025] 서로
  다른 API에서 형용사와 명사를 하나씩 가져와 문구를 만드는 예를 든다.

  ```java
  public String generatePhrase() throws ExecutionException, InterruptedException {
      try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
          Future<String> adjectiveFuture = executor.submit(this::fetchAdjective);
          Future<String> nounFuture = executor.submit(this::fetchNoun);
          String adjective = adjectiveFuture.get();
          String noun = nounFuture.get();
          return adjective + " " + noun;
      }
  }
  ```

- 이 방식이 없애는 것이 둘이다 — 비동기 연산 처리가 단순해지고, 복잡한 콜백 구조나 정교한 동기화
  장치가 필요 없어진다 (2장, p.48).[^rahman2025] 콜백을 변환의 체인으로 바꾸어 같은 문제를 풀던
  앞선 답이
  [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md)에 있다.

## 같은 타입의 묶음에는 invokeAll

- 결과 타입이 같은 비슷한 태스크가 여럿일 때는 `invokeAll` 메서드를 여전히 쓸 수 있고, 결과를
  리스트로 모으는 것이 목적일 때 특히 쓸모 있다 (2장, p.48).[^rahman2025] 저자는 이미지 여러 장에
  각각 다른 변환을 걸어 한꺼번에 던지고 순서대로 결과를 받는 예를 든다 (2장, pp.48–49).
- 총평이 시대 조건과 묶인다 — 현대 애플리케이션은 여러 태스크를 동시에 처리하면서 결과를 효율적으로
  모으는 능력을 자주 요구하고, I/O 바운드 연산이 성능을 좌우하는 오늘날의 환경에서 가상 스레드가
  그 답을 준다 (2장, pp.49–50).[^rahman2025]

## 이 방식이 남기는 결함

- 저자가 스스로 한계를 짚는다 — 앞의 예제들은 타당하고 꽤 직관적이지만 다소 단순하다. 예외와
  타임아웃을 잘 다루지 못하기 때문이다 (2장, p.50).[^rahman2025]
- 구체적으로 둘이다 — `Future::get` 메서드가 예외를 던질 수 있고, 타임아웃 장치가 없으면 무한정
  블로킹될 가능성이 있다 (2장, p.50).[^rahman2025] 그 결함에 답하는 구조가
  [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md)다.

## 이어지는 페이지

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 이 방식이 남긴 예외와
  타임아웃 문제에 답하는 구조
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 같은 문제를
  콜백 체인으로 풀던 앞선 답
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 같은
  실행자를 쓰는 다른 예
- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 블로킹의 값이
  왜 문제였는가
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Simplifying Asynchronous
    Operations"(pp.47–50), "The Promise of Structured Concurrency"(p.50). 개념당 대표 코드
    하나 규칙에 따라 `generatePhrase`만 실었고, 그것이 부르는 `fetchAdjective`·`fetchNoun`
    흉내 메서드와 `ImageProcessingExample` 전문(pp.48–49)은 미수록이다 — 서술은 모두 옮겼다.

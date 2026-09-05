---
type: concept
title: Callable과 Future로 결과 받기
description: Runnable로는 결과가 돌아오지 않는다는 자리에서 시작해 Callable이 값을 돌려주고 예외를 던질 수 있는 함수형 인터페이스라는 것, submit이 즉시 돌려주는 Future의 다섯 메서드와 실제로 쓰는 둘, 그리고 get이 블로킹 연산이라 호출한 스레드를 막지만 다른 스레드는 계속 일한다는 것
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# Callable과 Future로 결과 받기

- [Runnable이 못 하는 것](#runnable이-못-하는-것)
- [Callable](#callable)
- [Future](#future)
- [get은 막는다](#get은-막는다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드 풀에 던진 작업의 결과는 어떻게 돌려받고, 그 대가는 무엇인가.**

## Runnable이 못 하는 것

- 여태 `Runnable`로 작업을 제출해 왔지만 아무 결과도 돌아오지 않았다. 작업이 끝난 뒤 결과가 필요할
  때가 있고, `Callable`과 `Future`가 들어오는 자리가 거기다 (3장, p.101).[^rahman2025]

## Callable

- 인터페이스는 `V call() throws Exception` 하나로 이뤄진다 (3장, p.101).[^rahman2025]
- 차이가 두 가지뿐이다 — `Callable`도 `Runnable`처럼 함수형 인터페이스이고, 유일한 차이는 결과를
  돌려줄 수 있고 예외를 던질 수 있다는 것이다 (3장, p.101).[^rahman2025]
- 함수형 인터페이스라서 익명 클래스 대신 람다로도 제출할 수 있다. 저자가 익명 `Callable<Long>`으로
  쓴 피보나치 제출을 `threadPool.submit(() -> fibonacci(50))` 한 줄로 줄여 보인다 (3장,
  p.102).[^rahman2025]
- 저자가 예제에서 짚는 네 자리 (3장, p.102):[^rahman2025]
  - `ConcurrentHashMap`으로 피보나치 결과를 캐시해, 재귀 구현을 효율적이면서 동시 접근에 안전하게
    만든다.
  - `submit` 메서드가 `Callable<Long>`을 받아 `Future<Long>`을 돌려주고, 이 `Future`가 비동기 계산의
    최종 결과를 나타낸다.
  - `Runnable.run()`과 달리 `call()` 메서드는 값을 돌려준다.
  - 캐시가 값을 다시 계산하지 않게 해 주는데, 같은 값이 여러 번 계산되는 재귀 알고리즘에서
    결정적이다.

## Future

- `Future`가 가진 메서드는 다섯이다 — `cancel(boolean)`, `isCancelled()`, `isDone()`, `get()`,
  그리고 타임아웃을 받는 `get(long, TimeUnit)` (3장, p.102).[^rahman2025]
- 다만 대부분의 쓰임에서는 `get()`과 `isDone()`만 쓴다 (3장, p.102).[^rahman2025]
- 반환 시점이 핵심이다 — `Callable`로 작업을 제출하면 작업이 아직 끝나지 않았어도 `Future`가 즉시
  돌아온다. `isDone()`이 작업의 완료 여부를 확인하고 `get()`이 결과를 회수한다 (3장,
  p.102).[^rahman2025]

## get은 막는다

- 저자가 별도 상자로 떼어 강조하는 문장이다 (3장, p.103):[^rahman2025]

  > The get() method is a blocking operation. It will block the calling thread until the
  > result is available.

- 여러 피보나치 수를 한꺼번에 계산하는 예제가 그 대가를 드러낸다 (3장, p.103).[^rahman2025]

  ```java
  try (ExecutorService threadPool = Executors.newCachedThreadPool()) {
      for (int index : fibonacciIndices) {
          futures.add(threadPool.submit(() -> fibonacci(index)));
      }
      for (Future<Long> future : futures) {
          System.out.println("Fibonacci number: " + future.get());
      }
  }
  ```

  - 버전 조건: JDK 21 이상 — 이 책의 예제와 개념이 요구하는 최소 버전이다 (머리말,
    p.xi).[^rahman2025]

- 무엇이 벌어지는지 저자가 정리한다 — 여러 `Callable` 작업이 제출되어 병렬로 실행되지만, 루프 안에서
  `future.get()`을 부르면 주 스레드는 그 특정 작업이 끝날 때까지 막힌다. 여기서의 이점은 주
  스레드가 막혀 있는 동안에도 다른 스레드들은 자기 일을 계속한다는 것이다 (3장,
  p.103).[^rahman2025]
- 이 막힘이 1장에서 실행자 프레임워크의 첫째 한계로 꼽힌 바로 그 자리다 —
  [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)를 보라. 가상
  스레드가 이 막힘의 값을 바꾸는 자리는
  [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)에
  있다.

## 이어지는 페이지

- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — `get`의 막힘을
  한계로 세운 자리
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 이 `Future`를
  조합 가능한 것으로 바꾸려는 다음 답
- [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)
  — 막는 `get`이 싸지면 코드 모양이 달라지는 자리
- [의존하는 하위 작업과 스레드 풀의 교착](../concepts/recursive-task-decomposition-deadlock.md) —
  이 막는 `get`을 재귀에 쓰면 벌어지는 일
- [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md) — 예제가 쓰는
  캐시드 풀
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 Future 추상을
  파이썬 쪽에서 본 자리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" — "Callable and
    Future: Handling Task Results"(pp.101–103), "Callable"(pp.101–102), "Future"(pp.102–103).
    최소 JDK 버전은 머리말 "What This Book Offers"(p.xi). 인용한 코드는 원문(p.103)의 `main`에서
    변수 선언 두 줄과 `catch` 절을 깎아 핵심 흐름만 남긴 것이다. `CallableExample` 전문(pp.101–102)과
    `Callable`·`Future` 인터페이스 선언(pp.101–102)은 펜스로 옮기지 않고 서술로만 담았다 —
    개념당 대표 코드 하나 규칙이고, 원문은 `archive/` 스냅샷이 보존한다. 이 절에는 그림이 없다.

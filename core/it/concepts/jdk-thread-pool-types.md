---
type: concept
title: JDK 실행자 프레임워크의 스레드 풀 종류
description: Executors 팩토리가 내주는 다섯 가지 스레드 풀이 각각 무엇을 다르게 하고 저자가 어떤 작업 부하에 쓰라고 적는가 — 고정과 캐시드와 단일 스레드와 스케줄드와 작업 훔치기, 그리고 그 곁의 특수한 풀인 ForkJoinPool의 자리
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# JDK 실행자 프레임워크의 스레드 풀 종류

- [FixedThreadPool](#fixedthreadpool)
- [CachedThreadPool](#cachedthreadpool)
- [SingleThreadExecutor](#singlethreadexecutor)
- [ScheduledThreadPoolExecutor](#scheduledthreadpoolexecutor)
- [WorkStealingPool](#workstealingpool)
- [그 곁의 ForkJoinPool](#그-곁의-forkjoinpool)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **팩토리가 내주는 풀들은 무엇이 다르고 어떤 작업 부하에 어느 것을 고르는가.**

이 다섯은 같은 `ThreadPoolExecutor`를 다르게 설정한 결과다 —
[ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md)가 그
손잡이를 갖는다.

## FixedThreadPool

- 고정 수의 스레드로 풀을 만든다. 모든 스레드가 바쁘면 새 작업은 스레드가 날 때까지 큐에서
  기다린다. 이 방식은 활성 스레드 수를 일정하게 유지하는 데 도움이 되어, 작업 부하를 예측할 수 있을
  때 쓸모가 있다 (3장, p.99).[^rahman2025]
- 저자가 적는 쓸 자리 — 일정한 수의 스레드가 동시에 일해야 하는 애플리케이션에 가장 알맞다. 예측
  가능한 동시성 수준을 유지해야 하는 서버 애플리케이션이 그런 경우다. 자원이나 데이터베이스 연결이
  제한적이라면 고정 풀이 시스템을 압도하지 않게 돕는다 (3장, p.99).[^rahman2025]

  ```java
  try (ExecutorService fixedPool = Executors.newFixedThreadPool(4)) {
      for (int i = 0; i < 10; i++) {
          fixedPool.submit(() -> {
              System.out.println(Thread.currentThread().getName()
                  + " is executing a task");
          });
      }
  }
  ```

  - 버전 조건: JDK 21 이상 — 이 책의 예제와 개념이 요구하는 최소 버전이다 (머리말,
    p.xi).[^rahman2025]

## CachedThreadPool

- 필요할 때 동적으로 새 스레드를 만들고, 이전에 만든 스레드가 놀고 있으면 재사용한다. 작업 부하의
  크기가 출렁일 때 크게 이롭다. 풀이 수요에 맞춰 동적으로 조절되기 때문이다 (3장,
  p.99).[^rahman2025]
- 쓸 자리와 쓰지 말 자리가 함께 적힌다 — 수명이 짧은 작업이 아주 많거나 작업이 예측할 수 없는
  폭주로 도착할 때 이상적이다. 반대로 오래 도는 작업에는 알맞지 않다. 활성 스레드가 너무 많이
  만들어질 수 있기 때문이다 (3장, p.99).[^rahman2025]

## SingleThreadExecutor

- 스레드 하나로 작업이 차례대로 실행되도록 보장한다. 저자의 비유로는 받은 순서대로 작업을 처리하는
  일꾼 한 명을 두는 것과 같다 (3장, p.100).[^rahman2025]
- 쓸 자리 — 작업이 엄격한 순서로 돌아야 하거나 동시에 돌면 안 될 때 쓴다. 한 번에 하나의 작업만
  접근해야 하는 공유 자원을 다룰 때 자주 쓰이며, 경쟁 조건(race condition)이 생기지 않도록 보장한다
  (3장, p.100).[^rahman2025]

## ScheduledThreadPoolExecutor

- 지연 뒤에 또는 고정된 간격으로 작업이 돌도록 예약한다 (3장, p.100).[^rahman2025]
- 쓸 자리 — 알림 보내기, 시스템 상태 점검, 유지보수 작업을 일정한 간격으로 돌리는 주기적 작업에
  이상적이다. 사람 손을 대지 않고도 원하는 빈도로 작업이 실행되도록 보장한다 (3장,
  p.100).[^rahman2025]
- 예약 메서드는 `scheduleAtFixedRate`이고, 초기 지연과 주기와 시간 단위를 받는다 (3장,
  p.100).[^rahman2025]

## WorkStealingPool

- 작업 훔치기(work-stealing) 알고리즘으로 스레드 사이의 작업 부하를 동적으로 고르게 하는 스레드
  무리를 만든다. 이 종류의 풀은 가용 프로세서의 사용을 최적화한다 (3장, p.100).[^rahman2025]
  그 알고리즘 자체는 [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md)에
  있다.
- 쓸 자리 — 작고 독립적인 작업이 많고 CPU 코어의 활용을 최대로 올리고 싶을 때다 (3장,
  p.101).[^rahman2025]

## 그 곁의 ForkJoinPool

- 자바에는 `ForkJoinPool`이라는 특별한 종류의 스레드 풀이 따로 있다. 큰 문제를 병렬로 처리할 수 있는
  더 작고 독립적인 작업으로 쪼갤 수 있는 분할 정복(divide-and-conquer) 작업을 겨냥해 설계되었다
  (3장, p.101).[^rahman2025]
- 그리고 이 풀도 내부적으로 작업 훔치기 알고리즘을 쓴다 (3장, p.101).[^rahman2025]

## 이어지는 페이지

- [ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md) — 이
  종류들을 만들어 내는 매개변수
- [스레드 풀의 이유와 내부 구조](../concepts/thread-pool-rationale-and-internals.md) — 이 풀들이
  공통으로 하는 일
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 마지막 두 항목이
  기대는 알고리즘과 풀
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 이 팩토리를
  쓰는 쪽에서 본 자리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" —
    "FixedThreadPool"(p.99), "CachedThreadPool"(p.99), "SingleThreadExecutor"(p.100),
    "ScheduledThreadPoolExecutor"(p.100), "WorkStealingPool"(pp.100–101). 최소 JDK 버전은 머리말
    "What This Book Offers"(p.xi). 인용한 `FixedThreadPool` 예제는 원문 그대로이며 조판 줄바꿈만
    폈다. 나머지 네 종류의 예제 코드(pp.99–100)는 개념당 대표 코드 하나 규칙에 따라 옮기지 않고
    서술로만 담았다 — 원문은 `archive/` 스냅샷이 보존한다. 이 절에는 그림이 없다.

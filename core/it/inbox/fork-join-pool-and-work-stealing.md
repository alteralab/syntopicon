---
type: concept
title: 포크조인 풀과 작업 훔치기
description: 캐시 경합과 복잡한 작업 의존을 겨냥한 ExecutorService의 전용 구현이 무엇을 다르게 하는가 — 워커 스레드가 자기 로컬 큐를 먼저 도는 캐시 친화성, 공유 큐 하나 대신 스레드마다 큐를 두고 일이 떨어지면 남의 큐 꼬리에서 가져오는 작업 훔치기, 그리고 분할 정복과는 구분되는 풀 자체의 값
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 포크조인 풀과 작업 훔치기

이 페이지의 질문: **스레드 풀 하나에 작업을 던지는 것과 스레드마다 큐를 주는 것은 무엇이
달라지는가.**

## 무엇을 겨냥한 설계인가

- 실행자 프레임워크는 쓸모가 크지만 심한 캐시 경합이나 복잡한 작업 의존 관계가 필요한 상황에서
  문제가 될 수 있다. 자바의 포크/조인 풀(Fork/Join Pool)이 성능 중심 설계와 전용 알고리즘으로 그
  문제를 다룬다 (1장, p.21).[^rahman2025] 그 캐시 경합이 무엇인지는
  [거짓 공유와 캐시 일관성](../concepts/false-sharing-and-cache-coherence.md)에 있다.
- 위치가 분명하다 — 포크/조인 풀은 `ExecutorService`의 전용 구현이며, 더 정교한 스레드 풀링 기제로
  지능적인 작업 스케줄링을 통해 성능과 자원 효율을 올린다 (1장, p.21).[^rahman2025]

## 캐시 친화성

- 캐시 친화성(cache affinity)은 CPU 캐시의 지역성(locality)을 살리는 방식으로 작업을 끝낸다는
  개념이다. 어떤 작업이 특정 CPU에서 실행되면 그 데이터가 해당 코어의 캐시에 올라가고, 관련된 다른
  작업이 같은 코어에서 실행되면 이미 캐시에 있는 데이터의 덕을 보아 메모리 접근 시간이 줄고 성능이
  오른다 (1장, p.21).[^rahman2025]
- 포크/조인 풀이 캐시 친화성을 북돋우는 이유는 워커 스레드가 보통 자기 로컬 큐의 작업을 실행하기
  때문이다. 작업들이 같은 공유 데이터에 자주 닿을 때 특히 도움이 된다 (1장, p.21).[^rahman2025]
- 그렇게 해서 줄이는 것이 캐시 미스(cache miss)다 — 작업에 필요한 데이터가 캐시에 없어 주기억
  장치에서 가져와야 하는 상황이고, 훨씬 느린 과정이다 (1장, p.21).[^rahman2025]
- 저자의 예는 큰 배열이다 — 병렬 작업들이 한 배열의 서로 다른 조각을 처리한다면 같은 코어에서 돌게
  하는 편이 이득이다. 그 조각의 데이터가 캐시에 남아 다음 작업이 빨리 닿을 수 있고, 그러지 않으면
  같은 데이터를 캐시로 계속 다시 올려야 한다 (1장, p.21).[^rahman2025]

## 작업 훔치기 알고리즘

- 포크/조인 풀은 스레드 사이의 부하를 고르게 하려고 동적인 작업 훔치기(work-stealing) 알고리즘을
  쓴다. 공유 작업 큐 하나를 두는 대신 풀의 스레드마다 자기 큐를 갖는다 (1장, p.21).[^rahman2025]
- 기제가 한 줄이다 — 어떤 스레드가 할 일이 떨어지면 다른 스레드 큐의 꼬리에서 작업을 훔쳐 온다.
  이 동적 알고리즘이 CPU 사용을 최대로 끌어올려, 할 일이 남아 있는 한 노는 스레드가 없게 만든다
  (1장, p.21).[^rahman2025]
- 그래서 얻는 것이 재분배다 — 작업을 동적으로 다시 나누어 모든 스레드가 생산적으로 남게 하고, 전체
  CPU 활용을 올리며 노는 시간을 줄인다 (1장, p.21).[^rahman2025]

## 쓰는 법과 이 페이지가 다루지 않는 것

- 포크/조인 풀은 작업을 보내는 과정을 단순하게 만들고, 추가 관리 없이 알아서 작업을 효율적으로
  나눈다 (1장, p.22).[^rahman2025]

  ```java
  ForkJoinPool forkJoinPool = new ForkJoinPool();
  forkJoinPool.submit(() -> {
      // your parallelized tasks here
  }).join();
  ```

- 저자는 제출이 쉽다는 점을 짚고, 프레임워크가 효율적인 작업 분배를 알아서 처리해 복잡한 스레드
  관리의 짐을 개발자에게서 덜어 간다고 적는다 (1장, p.22).[^rahman2025]
- 범위를 저자가 직접 긋는다 — 포크/조인 풀은 보통 분할 정복(divide-and-conquer) 알고리즘과 함께
  이야기되고 `RecursiveAction`과 `RecursiveTask`로 작업을 잘게 쪼개지만, 여기서 초점은 그 작업을
  만드는 분할 정복 전략이 아니라 포크/조인 풀 자체다. 더 자세한 논의는 다음 장으로 미룬다 (1장,
  p.22).[^rahman2025]

## 이어지는 페이지

- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 이 풀이 넘어서려는
  기본 스레드 풀
- [거짓 공유와 캐시 일관성](../concepts/false-sharing-and-cache-coherence.md) — 캐시 친화성이
  뒤집어 쓰려는 그 기제
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 이 풀 위에
  서는 조합 API
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 저자가 이
  풀과 이어 놓는 자리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "Beyond Basic Thread Pools"(pp.21–22),
    "Cache Affinity and Task Distribution"(p.21), "Work-Stealing Algorithm"(pp.21–22),
    "Example of using a Fork/Join Pool"(p.22). 그림 1-3(포크/조인 풀의 작업 훔치기 그림, p.22)은
    옮기지 않았다 — 원문은 `archive/` 스냅샷이 보존한다. 인용한 코드는 원문 그대로다.

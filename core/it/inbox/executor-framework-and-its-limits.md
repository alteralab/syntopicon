---
type: concept
title: 실행자 프레임워크와 그 한계
description: ExecutorService가 스레드 수를 통제하고 수명 주기를 대신 관리해 임기응변식 스레드 생성을 대신하는 구조, 그렇게 바꿔도 실행 시간이 거의 같았다는 실측과 실행자의 값이 속도가 아니라 관리에 있다는 읽기, 그리고 남은 세 한계 — Future.get이 여전히 막는다는 것, 캐시 일관성 부담과 거짓 공유, 명령형이라 조합이 어렵다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 실행자 프레임워크와 그 한계

- [실행자가 대신 맡는 것](#실행자가-대신-맡는-것)
- [바꿔도 시간은 거의 같았다](#바꿔도-시간은-거의-같았다)
- [남은 한계 셋](#남은-한계-셋)
- [태스크 위계가 없다는 넷째 한계](#태스크-위계가-없다는-넷째-한계)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드를 손수 만드는 대신 실행자에 맡기면 무엇이 해결되고 무엇이 남는가.**

## 실행자가 대신 맡는 것

- 임기응변식 스레드 생성의 위험을 피하려면 `ExecutorService` 같은 자바 동시성 프레임워크를 쓰는
  편이 낫다. 스레드를 다루는 더 구조화된 방식을 주기 때문이다 (1장, p.18).[^rahman2025] 그 위험이
  무엇인지는 [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md)에 있다.
- 실행자가 하는 일이 둘이다 — 동시에 도는 스레드의 수를 통제하고, 스레드의 수명 주기를 대신 관리해
  스레드를 효율적으로 재사용하게 해 준다. 그래서 수명 주기가 만들던 부담을 넘어선다 (1장,
  p.18).[^rahman2025]
- 작업이 제출되면 큐에 들어가고 풀의 스레드가 큐에서 집어 실행한다는 것이 그 구조다 (1장,
  p.8).[^rahman2025]
- 3장에서 저자가 정체를 한 줄로 다시 적는다 — 실행자 프레임워크는 본질적으로 스레드 풀의 구현이다
  (3장, p.91).[^rahman2025] 그 스레드 풀이 왜 있어야 하고 안에서 무엇이 도는지는
  [스레드 풀의 이유와 내부 구조](../concepts/thread-pool-rationale-and-internals.md)에, 이
  프레임워크가 노출하는 손잡이는
  [ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md)에 있다.
- 앞의 신용 점수 예제를 실행자로 다시 쓰면 스레드를 직접 만들던 자리가 `submit` 호출로 바뀐다 (1장,
  p.18).[^rahman2025]

  ```java
  public Credit calculateCreditWithExecutor(Long personId)
          throws ExecutionException, InterruptedException {
      try (ExecutorService executor = Executors.newFixedThreadPool(5)) {
          var person = getPerson(personId);

          var assetsFuture = executor.submit(() -> getAssets(person));
          var liabilitiesFuture = executor.submit(() -> getLiabilities(person));
          executor.submit(() -> importantWork());

          return calculateCredits(assetsFuture.get(), liabilitiesFuture.get());
      }
  }
  ```

  - 버전 조건: JDK 21 이상 — 이 책의 예제와 개념이 요구하는 최소 버전이다. 저자가 머리말에서
    가상 스레드가 정식으로 쓸 수 있게 된 릴리스가 그것이기 때문이라고 밝힌다 (머리말,
    p.xi).[^rahman2025]
- 저자가 이 코드에서 짚는 자리가 넷이다 — `try` 블록을 벗어나면 자동으로 종료되는 스레드 풀을
  만들고, 결과가 필요한 두 작업을 제출하고, 주 흐름을 막을 필요가 없는 추가 작업을 제출하고,
  결정적인 두 작업을 기다려 결과를 처리한다 (1장, p.18).[^rahman2025]

## 바꿔도 시간은 거의 같았다

- 실측이 630밀리초다. 저자는 이 값이 앞의 판과 아주 비슷하다는 점을 흥미롭다고 적는다 (1장,
  p.19).[^rahman2025] 앞의 병렬판이 616밀리초였다는 것은
  [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md)에 있다.
- 그래서 실행자의 값이 다른 데 있다고 읽는다 — 자바 애플리케이션에서 동시 작업을 관리하는 쓸 만한
  수단을 주고, 스레드를 만들고 관리하기 쉽게 하며, 알맞은 작업 부하에는 속도를 줄 수도 있고, 코드를
  정리하고 깨끗하게 유지하기 쉽게 만든다 (1장, p.19).[^rahman2025]

## 남은 한계 셋

- 저자는 실행자 프레임워크가 자원 관리와 비동기 실행에 큰 개선을 가져오지만, 그 이득을 최대로 내려면
  한계를 알아야 한다고 전제한다 (1장, p.19).[^rahman2025]
- `Future.get()`에서의 막힘 — `Future` 객체로 비동기성을 들였음에도 `get()` 호출은 여전히 실행을
  막는다. 막힘을 한 자리에서 다른 자리로 옮겼을 뿐 없애지는 못했다는 뜻이다 (1장,
  p.19).[^rahman2025]
- 캐시 일관성 부담과 거짓 공유의 가능성 — 작업이 스레드 풀에 제출되면 주 스레드와 다른 CPU 코어에서
  실행될 수 있고, 그러면 두 코어의 캐시 상태가 어긋날 수 있다. 캐시 일관성 프로토콜이 코어 사이에서
  캐시 라인을 계속 무효화하고 맞추느라 성능이 깎일 여지가 생긴다 (1장, pp.19–20).[^rahman2025]
  이 기제는 [거짓 공유와 캐시 일관성](../concepts/false-sharing-and-cache-coherence.md)이 갖는다.
- 조합 가능성의 부재 — 실행자 프레임워크는 여전히 상당히 명령형이다. 저자는 명령형 코드 자체에는
  잘못이 없다고 못박으면서도, 많은 개발자가 함수형과 선언형 방식을 읽고 유지하기 더 쉽다고 여긴다는
  점을 든다 (1장, p.20).[^rahman2025] 이 자리를 겨냥한 답이
  [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md)이다.
- 저자는 여기서 출발점으로 되돌아온 느낌이라고 적고, 이 문제들을 어떻게 풀 것이며 실행자로 더
  효율적이고 유지하기 쉬운 코드를 어떻게 쓸 것인가를 다음 질문으로 세운다 (1장,
  p.20).[^rahman2025]

## 태스크 위계가 없다는 넷째 한계

- 4장이 같은 프레임워크의 한계를 하나 더 짚는다 — `ExecutorService`와 `Future` 같은 전통적 동시성
  모델에서는 태스크 위계(task hierarchy)가 본래부터 지원되지 않는다. 그래서 취소를 전파하거나 오류를
  구조적으로 다루기가 어렵고, 결과는 조각나고 오류가 잦은 동시 프로그래밍이다 (4장 도입,
  p.125).[^rahman2025]
- 이 한계는 앞의 셋과 성격이 다르다. 앞의 셋은 태스크 하나를 다루는 값(막힘, 캐시, 표기)에 대한
  것이고, 이것은 **태스크들 사이의 관계**가 API에 표현되지 않는다는 것이다. 그 결과로 무엇이
  새는지는 [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md)에, 그것에
  답하는 구조는 [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md)에 있다.

## 이어지는 페이지

- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 실행자가 대신하는
  임기응변식 생성과 그 대가
- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 넷째 한계가 실제로
  드러나는 자리
- [스레드 풀의 이유와 내부 구조](../concepts/thread-pool-rationale-and-internals.md) — 이
  프레임워크가 구현하고 있는 것
- [ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md) — 실제로
  돌릴 수 있는 손잡이들
- [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md) — 팩토리가 내주는
  다섯 가지
- [Callable과 Future로 결과 받기](../concepts/callable-and-future-results.md) — 첫째 한계인 막는
  `get`의 실물
- [거짓 공유와 캐시 일관성](../concepts/false-sharing-and-cache-coherence.md) — 둘째 한계의 기제
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 캐시 경합과 복잡한
  작업 의존을 겨냥한 다음 답
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 셋째 한계를
  겨냥한 다음 답
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 실행기 추상을
  파이썬 쪽에서 본 자리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "Starting Threads"(p.8), "Introducing the
    Executor Framework"(pp.18–19), "Remaining Challenges"(pp.19–20). 3장 "The Mechanics of
    Modern Concurrency in Java" — "Thread Pool"(p.91). 4장 "Structured Concurrency" —
    장 도입(p.125). 최소 JDK 버전은 머리말
    "What This Book Offers"(p.xi). 인용한 `calculateCreditWithExecutor`는 원문 그대로이며 조판 줄바꿈만
    폈고, 원문이 코드 옆에 붙인 번호 표식은 뺐다.

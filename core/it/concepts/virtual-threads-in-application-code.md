---
type: concept
title: 애플리케이션에서 본 가상 스레드
description: 프로젝트 룸이 들인 가상 스레드를 쓰는 쪽에서 본 자리 — 생성 부담이 거의 없어 수백만 개를 만들 수 있다는 약속, 실행자 한 줄만 바꾸면 되는 기존 코드와의 통합, 플랫폼 스레드 위에 얹힌다는 관계와 원문이 거기에 포크조인 풀을 붙여 놓은 자리, 블로킹을 만나면 밑의 플랫폼 스레드에 제어를 넘기는 동작, 그리고 자원 효율과 코드 단순성과 최적 활용이라는 세 이점
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 애플리케이션에서 본 가상 스레드

- [버전 조건](#버전-조건)
- [이 페이지가 맡는 관점](#이-페이지가-맡는-관점)
- [가상 스레드의 약속](#가상-스레드의-약속)
- [기존 코드베이스와의 통합](#기존-코드베이스와의-통합)
- [플랫폼 스레드와의 관계](#플랫폼-스레드와의-관계)
- [블로킹 연산의 처리](#블로킹-연산의-처리)
- [세 가지 이점](#세-가지-이점)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **애플리케이션 코드를 얼마나 고쳐야 가상 스레드의 이득을 얻으며, 그 이득의
정체는 무엇인가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 이 책의 예제와 개념이 요구하는 최소 버전이며, 저자가 그 이유를
> 가상 스레드가 정식으로 쓸 수 있게 된 릴리스가 그것이기 때문이라고 밝힌다. 저자는 미리 보기
> 상태이거나 최근에 확정된 기능을 다루는 장이 있으므로 24나 25 같은 더 새 JDK를 쓰면 예제와 논의를
> 최대로 활용할 수 있다고 덧붙인다(머리말, p.xi). **JDK 20 이하에는 적용되지 않는다** — 그쪽에서
> 자바 스레드는 [스레드 구현 모델](../concepts/thread-implementation-models.md)의 1:1 커널
> 스레드가 전부다.

## 이 페이지가 맡는 관점

- 같은 가상 스레드를 가상 머신 안쪽에서 본 페이지가
  [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)이다. 그쪽은 문맥 전환
  비용의 정체와 코루틴의 계보와 후속문·스케줄러 구조를 다룬다. 이 페이지가 맡는 것은 **쓰는 쪽에서
  무엇이 달라지는가**다.

## 가상 스레드의 약속

- 자바의 전통적 동시성 수단이 오래 제 몫을 했지만 쓰임새가 복잡해지면서 여러 어려움이 드러났고,
  그래서 새 해법을 찾아야 했다는 것이 저자의 전제다 (1장, p.28).[^rahman2025] 그 어려움의 목록이
  [자바 리액티브 프레임워크의 대가](../concepts/reactive-frameworks-tradeoffs-in-java.md)와
  [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md)에 있다.
- 그 자리에 오는 것이 프로젝트 룸(Project Loom)이고, 저자는 이것을 자바에서 2025년 저술 시점의 동시성을 일급으로
  만드는 핵심 걸음이라고 부른다. 룸이 들인 새로운 종류의 스레드가 가상 스레드(virtual threads)다
  (1장, p.28).[^rahman2025]
- 무게가 약속의 전부다 — 매우 가볍고, 전통적인 스레드 생성에 따라붙던 부담이 거의 없이 필요할 때
  만들 수 있다 (1장, p.28).[^rahman2025] 그 부담이 무엇이었는지는
  [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)에 있다.
- 규모의 수치가 한 줄이다 — 가상 스레드는 수백만 개 단위로 만들 수 있고, 그것이 동시성이 매우 높고
  확장 가능한 애플리케이션의 새 가능성을 연다 (1장, p.29).[^rahman2025]

## 기존 코드베이스와의 통합

- 저자가 룸의 핵심 강점으로 꼽는 것이 기존 자바 코드베이스와의 매끄러운 호환성이다. 애플리케이션이
  이미 실행자 프레임워크를 쓰고 있다면 `Executors.newVirtualThreadPerTaskExecutor()`를 기존
  `ExecutorService` 자리에 넘기는 것이 해야 할 일의 전부다 (1장, p.29).[^rahman2025]

  ```java
  Credit calculateCreditWithVirtualThread(Long personId)
          throws ExecutionException, InterruptedException {
      try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
          var person = getPerson(personId);
          var assetsFuture = executor.submit(() -> getAssets(person));
          var liabilitiesFuture = executor.submit(() -> getLiabilities(person));
          executor.submit(this::importantWork);
          return calculateCredits(assetsFuture.get(), liabilitiesFuture.get());
      }
  }
  ```

- 지침이 한 문장으로 정리된다 — 전통적인 실행자를 이 팩터리로 바꾸면 곧바로 가상 스레드의 이득을
  얻는다. 저자는 이 통합의 쉬움이 새 동시성 모델로의 전환을 매끄럽게 만든다고 적는다 (1장,
  p.29).[^rahman2025] 바뀌기 전의 같은 메서드는
  [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)에 있다.

## 플랫폼 스레드와의 관계

- 가상 스레드는 플랫폼 스레드(platform threads) 위에서 돈다. 플랫폼 스레드는 클래식 스레드(classical
  threads)라고도 불리는 기존 자바 스레드다 (1장, p.29).[^rahman2025]
- 원문은 여기에 한 절을 더 붙인다 — 플랫폼 스레드도 포크/조인 풀의 뒷받침을 받으므로 가상 스레드가
  그 정교한 스레드 풀의 이점을 물려받고, 그래서 가상 스레드와 플랫폼 스레드가 결합해 최선의 자원
  활용과 확장성을 낸다는 것이다 (1장, p.29).[^rahman2025]
  - **이 서술은 같은 소스의 뒤쪽이 좁혀 준다.** 포크/조인 풀의 뒷받침을 받는 것은 플랫폼 스레드
    일반이 아니라 가상 스레드를 태우는 캐리어 스레드다 — 캐리어 스레드는 특수한 `ForkJoinPool`의
    일부이고, 가상 스레드 스케줄러 자체가 선입선출로 도는 작업 훔치기 `ForkJoinPool`이며 병렬
    스트림이 쓰는 공용 풀과는 구분된다 (2장, pp.31–32, p.46).[^rahman2025] 그러므로
    [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)이 포크/조인 풀을
    가상 스레드의 기본 스케줄러로 적은 것과 어긋나지 않는다. 여기 p.29의 표현이 그 관계를
    성기게 적은 것이고, 원문 표현은 고치지 않고 보존한다. 좁혀진 서술은
    [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md)와
    [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)에
    있다.

## 블로킹 연산의 처리

- 저자가 가장 흥미로운 면으로 꼽는 것이 블로킹 연산을 다루는 방식이다. 가상 스레드가 잠들기나
  네트워크 I/O 같은 블로킹 연산을 만나면 밑의 플랫폼 스레드에 제어를 자동으로 되돌려 준다 (1장,
  p.29).[^rahman2025]
- 그러면 그 플랫폼 스레드는 다른 가상 스레드를 계속 실행할 수 있고, 가용 자원이 최적으로 쓰인다.
  블로킹 연산이 끝나면 가상 스레드는 멈췄던 자리에서 실행을 이어받으므로 체감할 만한 병목이 생기지
  않는다 (1장, p.29).[^rahman2025]
  - 이것이 [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md)이 짚은
    묶임에 대한 답이다. 스레드가 I/O에 막혀 다른 요청을 못 맡던 자리가 바뀐다.

## 세 가지 이점

- 자원 효율성 — 가상 스레드는 가벼워서 자원을 고갈시키지 않고 수백만 개를 띄울 수 있고, 그것이
  동시성이 높고 확장 가능한 애플리케이션을 허락한다 (1장, p.30).[^rahman2025]
- 코드 단순성 — 성능 손해 없이 블로킹 코드를 쓸 수 있으므로 개발자가 더 단순하고 전통적인 명령형
  스타일로 쓰고 유지할 수 있다. 추가 학습 곡선이 없고 유지하기 쉬운 코드가 된다는 뜻이다 (1장,
  p.30).[^rahman2025]
- 최적 활용 — 블로킹 연산 동안 가상 스레드가 제어를 내주므로 플랫폼 스레드가 계속 쓰이고, CPU와
  애플리케이션 성능이 오른다 (1장, p.30).[^rahman2025]
- 저자의 마무리가 학습 부담 쪽으로 돌아온다 — 자바에서 동시성을 쓰는 개발자의 가장 큰 걱정 가운데
  하나가 제대로 쓰기 위해 익혀야 하는 지식의 양인데, 룸은 개발자가 이미 익숙한 패턴을 그대로 쓰면서
  동시성이 높고 효율적인 애플리케이션을 규모 있게 쓸 수 있게 해 준다는 점에서 큰 진전이다 (1장,
  p.30).[^rahman2025]

## 이어지는 페이지

- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 같은 대상을 가상 머신
  안쪽에서 본 자리
- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 이 방식이 답하는
  문제
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 한 줄만 바꾸면
  되는 그 자리
- [자바 리액티브 프레임워크의 대가](../concepts/reactive-frameworks-tradeoffs-in-java.md) — 이 답이
  피하려는 대가들
- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 두 종류의
  관계를 같은 소스가 더 자세히 적은 자리
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  가상 스레드를 열어 본 자리들의 허브
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "Revolutionizing Concurrency in Java"(pp.28–30),
    "The Promise of Virtual Threads"(pp.28–29), "Seamless Integration with Existing
    Codebases"(p.29), "Virtual Threads and Platform Threads"(p.29), "Intelligent Handling of
    Blocking Operations"(p.29), "Benefits of Embracing Virtual Threads"(p.30). 포크/조인 풀과
    캐리어 스레드의 관계를 좁혀 주는 서술은 2장 "What Is a Virtual Thread?"(pp.31–32)와
    "Carrier Threads and OS Involvement"(p.46). 최소 JDK 버전과
    24·25 권고는 머리말 "What This Book Offers"(p.xi). 인용한
    `calculateCreditWithVirtualThread`는 원문 그대로이며 조판 줄바꿈만 폈다.

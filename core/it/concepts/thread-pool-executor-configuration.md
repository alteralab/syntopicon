---
type: concept
title: ThreadPoolExecutor 설정과 풀 크기
description: Executors 팩토리가 내주는 풀이 사실상 하나의 구현을 다르게 설정한 것이라는 사실과 그 생성자가 받는 일곱 매개변수, 코어 풀 크기와 최대 풀 크기가 각각 무엇을 정하는가, 그리고 CPU 바운드와 I/O 바운드에 따라 갈리는 크기 선택과 가상 스레드가 있어도 이 풀이 사라지지 않는 이유
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ThreadPoolExecutor 설정과 풀 크기

- [팩토리 뒤에 하나의 구현이 있다](#팩토리-뒤에-하나의-구현이-있다)
- [생성자가 받는 일곱 가지](#생성자가-받는-일곱-가지)
- [코어 풀 크기와 최대 풀 크기](#코어-풀-크기와-최대-풀-크기)
- [크기를 정하는 기준](#크기를-정하는-기준)
- [가상 스레드가 있어도 남는 자리](#가상-스레드가-있어도-남는-자리)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드 풀의 크기와 동작을 실제로 정하는 손잡이는 무엇이고 무엇을 보고
돌리는가.**

## 팩토리 뒤에 하나의 구현이 있다

- 설계 의도가 두 가지다 — 실행자 프레임워크는 성능을 최대로 끌어내면서 쓰기 쉽도록 설계되었고,
  공통 인터페이스인 `ExecutorService`를 따르는 여러 구현을 준다 (3장, p.96).[^rahman2025]
- 진입점이 팩토리 클래스다 — 서로 다른 스레드 풀 구현의 인스턴스를 얻을 때는 `Executors`라는 팩토리
  클래스를 쓰고, 이 클래스가 풀 종류마다 맞춘 여러 팩토리 메서드를 제공한다 (3장,
  p.96).[^rahman2025] 그 종류들은
  [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md)에 있다.
- 뚜껑을 열면 하나다 — `Executors.newFixedThreadPool(10)`처럼 스레드 열 개짜리 고정 크기 풀을
  요청하면, 그 메서드는 우리가 준 스레드 수와 몇 가지 추가 인자로 `ThreadPoolExecutor`의 인스턴스를
  만든다. 실제로 `Executors` 클래스의 다른 메서드들도 대부분 `ThreadPoolExecutor`를 쓰며, 인자를
  달리해 여러 동작을 얻는다 (3장, pp.96–97).[^rahman2025]

## 생성자가 받는 일곱 가지

- `ThreadPoolExecutor`의 생성자가 이 프레임워크에서 설정할 수 있는 것의 전부를 드러낸다 (3장,
  p.97).[^rahman2025]

  ```java
  public ThreadPoolExecutor(int corePoolSize,
                            int maximumPoolSize,
                            long keepAliveTime,
                            TimeUnit unit,
                            BlockingQueue<Runnable> workQueue,
                            ThreadFactory threadFactory,
                            RejectedExecutionHandler handler) {}
  ```

- `corePoolSize` — 유휴 상태여도 풀에 유지할 스레드의 수. 다만 `allowCoreThreadTimeOut`이 켜져
  있으면 그렇지 않다 (3장, p.97).[^rahman2025]
- `maximumPoolSize` — 풀에 허용되는 스레드의 최대 수 (3장, p.97).[^rahman2025]
- `keepAliveTime` — 스레드 수가 코어보다 많을 때, 초과된 유휴 스레드가 종료되기 전에 새 작업을
  기다리는 최대 시간 (3장, p.97).[^rahman2025]
- `unit` — `keepAliveTime` 인자의 시간 단위. 나노초, 밀리초, 초 따위다 (3장,
  p.97).[^rahman2025]
- `workQueue` — 작업이 실행되기 전에 담아 둘 큐. 이 큐는 `execute` 메서드로 제출된 `Runnable`
  작업만 담는다 (3장, p.97).[^rahman2025]
- `threadFactory` — 실행자가 새 스레드를 만들 때 쓸 팩토리 (3장, p.97).[^rahman2025]
- `handler` — 스레드 한계와 큐 용량에 모두 닿아 실행이 막혔을 때 쓸 처리기 (3장,
  p.97).[^rahman2025]
- 이 매개변수들을 알면 `Executors`의 팩토리 메서드가 어떻게 서로 다른 설정을 만들어 내는지 보인다.
  예를 들어 `newFixedThreadPool()`은 `corePoolSize`와 `maximumPoolSize`를 같은 값으로 세워, 명시적으로
  내리지 않는 한 살아 있는 고정 수의 스레드를 가진 풀을 만든다 (3장, pp.97–98).[^rahman2025]
- 프레임워크들이 이 클래스를 그대로 쓴다 — 저자가 드는 예가 스프링 프레임워크로,
  `ThreadPoolTaskExecutor`로 감싸 비동기 연산을 매끄럽게 다룬다 (3장, p.98).[^rahman2025]

## 코어 풀 크기와 최대 풀 크기

- 저자는 풀을 설정할 때 반드시 고려해야 할 크기가 둘이라고 못박는다 (3장, p.98).[^rahman2025]
- 코어 풀 크기의 정의가 원문에 있다 (3장, p.98):[^rahman2025]

  > The *core pool size* is the minimum number of threads always kept alive in the pool,
  > even if idle.

- 코어를 두는 이유가 스레드 생성의 값이다 — 새 스레드를 만드는 일이 비싸다는 것을 알기 때문에,
  이 스레드들을 바로 쓸 수 있게 두면 시스템이 생성 부담 없이 작업을 빠르게 배정할 수 있다. 실행할
  작업이 없으면 기다리고 있다가 새 작업이 오면 받는다 (3장, p.98).[^rahman2025] 생성이 왜 비싼지는
  [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)에 있다.
- 반대쪽 대가도 있다 — 유휴 스레드가 너무 많으면 CPU 사이클과 메모리 같은 자원을 쓸데없이 낭비할 수
  있다. 그래서 알맞은 최소 스레드 수를 세우는 일이 중요하다 (3장, p.98).[^rahman2025]
- 최대 풀 크기의 정의도 원문에 있다 (3장, p.98):[^rahman2025]

  > The *maximum pool size* defines the upper limit on the number of threads that can be
  > active in the pool at any given time.

- 최대 풀 크기가 있어서 스레드 풀은 작업이 더 많이 제출될 때 늘려서 수요 증가에 맞출 수 있다 (3장,
  p.98).[^rahman2025]

## 크기를 정하는 기준

- 저자가 먼저 없는 것을 말한다 — 최적의 코어·최대 크기를 정하는 일은 성능 조율에 매우 중요하지만,
  이 값들은 작업 부하와 애플리케이션이 도는 하드웨어에 따라 크게 달라지므로 모두에게 맞는 하나의
  답은 없다 (3장, p.98).[^rahman2025]
- 그래서 방법이 실측이다 — 개발자는 실험하고 성능 지표를 관찰해 균형점을 찾고, 경험적 결과에 따라
  풀 크기를 조정해야 하는 경우가 많다 (3장, p.98).[^rahman2025]
- 다만 일반 원칙 하나는 준다 — 작업 부하가 CPU 바운드(예컨대 수치 연산)라면 스레드 수를 가용 CPU
  코어 수에 맞춘다. 스레드를 더 보태면 문맥 전환(context switching)과 동기화 부담이 늘어 성능이
  오히려 나빠질 수 있다 (3장, p.98).[^rahman2025]
- 반대쪽 원칙이 짝이다 — 작업 부하가 I/O 바운드(예컨대 데이터베이스 호출)라면 CPU보다 스레드가
  많은 편이 이득일 수 있다. I/O를 기다리며 노는 스레드가 있는 동안 다른 작업이 실행될 수 있기
  때문이다 (3장, p.98).[^rahman2025]

## 가상 스레드가 있어도 남는 자리

- 앞 장의 가상 스레드가 I/O 바운드 작업 부하에서 스레드 풀 관리의 복잡함을 없애는 길을 준다 (3장,
  p.98).[^rahman2025] 그 근거는
  [가상 스레드가 확장을 주는 자리](../concepts/virtual-thread-scalability-limits.md)에 있다.
- 그러나 저자는 기존 스레드 풀의 쓰임이 완전히 사라지지는 않는다고 적는다 — 레거시 시스템, 호환성
  고려, 특정 성능 요구가 여전히 전통적인 스레드 풀을 요구할 수 있다 (3장, p.98).[^rahman2025]
- 실측 반례가 하나 인용된다 — 최근 오픈리버티(OpenLiberty)로 수행된 연구에서, 그들 자신의
  `ThreadPool` 구현이 가상 스레드보다 더 나은 성능을 냈다 (3장, p.98).[^rahman2025]
- 그래서 결론이 조율 능력이다 — 그렇기 때문에 기존 스레드 풀을 어떻게 설정하고 활용하는지 아는 것이
  매우 중요하다 (3장, pp.98–99).[^rahman2025]

## 이어지는 페이지

- [스레드 풀의 이유와 내부 구조](../concepts/thread-pool-rationale-and-internals.md) — 이 설정이
  조절하는 대상의 기제
- [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md) — 이 생성자를
  다르게 채운 다섯 결과
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 쓰는 쪽에서
  본 같은 프레임워크
- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 코어를 유지하는 이유와 문맥 전환의 값
- [가상 스레드가 확장을 주는 자리](../concepts/virtual-thread-scalability-limits.md) — 이 조율이
  필요 없어지는 조건과 그러지 않은 자리
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 이 풀에서
  옮겨 갈 때의 순서
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" — "The Executor
    Framework"(pp.96–99). 인용한 생성자 시그니처는 원문 그대로다. 오픈리버티가 무엇인지는 원문
    각주 1(p.98)에 있다 — 자카르타 EE와 마이크로프로파일 등 열린 표준을 지원하며 마이크로서비스와
    클라우드 기반 애플리케이션을 겨냥한 가볍고 클라우드 네이티브한 자바 런타임이다. 이 절에는
    그림이 없다.

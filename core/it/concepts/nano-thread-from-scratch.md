---
type: concept
title: 직접 만들어 본 가상 스레드
description: 후속문 API 위에 NanoThread라는 스레드 비슷한 추상을 얹어 가상 스레드의 동작을 흉내 내는 저자의 실습, 작업 훔치기 풀이 스케줄러 노릇을 하고 예약 실행자가 I/O 대기를 흉내 내는 구조, 그리고 같은 NanoThread가 시작한 워커와 끝낸 워커가 다르다는 출력이 가상 스레드에서도 그대로라는 관찰
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 직접 만들어 본 가상 스레드

- [버전 조건](#버전-조건)
- [무엇을 왜 만드는가](#무엇을-왜-만드는가)
- [NanoThread](#nanothread)
- [스케줄러](#스케줄러)
- [I/O를 흉내 내는 자리](#io를-흉내-내는-자리)
- [출력이 보여 주는 것](#출력이-보여-주는-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드를 후속문 위에 손으로 다시 만들면 무엇이 드러나는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 이 실습은 `jdk.internal.vm.Continuation`이라는 **내부 API** 위에
> 서 있어서, `java --add-exports java.base/jdk.internal.vm=ALL-UNNAMED`로 실행해야 한다. 내부
> API는 예고 없이 바뀌거나 사라질 수 있으므로 여기 적힌 클래스와 메서드 모양은 **JDK 21 시점의
> 내부 구현**을 가리키며 위쪽 경계가 열려 있다. 저자 자신이 이 구현은 오직 예시 목적일 뿐이라고
> 못박는다. 접근 조건과 경고의 전문은
> [자바의 후속문 API](../concepts/java-continuation-api.md)에 있다.

## 무엇을 왜 만드는가

- 목적이 하나다 — 가상 스레드가 후속문을 어떻게 쓰는지의 핵심 개념을 보이려고, 저자가 `NanoThread`
  라 부르는 스레드 비슷한 자기만의 추상을 단순화해 만든다. 자바의 Continuation API로 가상 스레드의
  동작을 흉내 낼 수 있다는 것이다 (3장, p.117).[^rahman2025]
- 부품이 셋이다 — `NanoThreadScheduler`, `NanoThread` 클래스, 그리고 파일 전송 연산의 흉내 (3장,
  p.117).[^rahman2025]

## NanoThread

- `NanoThread`는 Continuation API를 둘러싸고 만든 저자의 커스텀 가상 스레드다. `Runnable`을 받아
  만들어지고, 그 `Runnable`이 `Continuation` 안에 감싸인다 (3장, pp.117–118).[^rahman2025]
- 갖는 것이 고유 번호와 후속문이다 — `COUNTER`로 고유 ID를 받고 `Continuation` 하나를 관리하며,
  실행할 로직을 담은 `Runnable`로 초기화된다 (3장, p.118).[^rahman2025]
- `run()`이 하는 일은 한 줄이다 (3장, p.118).[^rahman2025]

  ```java
  public void run() {
      continuation.run();
  }
  ```

- 저자가 그 한 줄을 마법이 일어나는 자리라고 부른다 — `Continuation.run()`을 부를 뿐인데, 그것이
  `Runnable` 안의 코드를 실행하게 한다. 어느 지점에서든 `NanoThread`가 `Continuation.yield()`로
  실행을 양보하면 멈췄다가 나중에 멈춘 자리에서 재개하며, 이것이 가상 스레드의 동작을 흉내 낸다
  (3장, p.118).[^rahman2025]
- `start()`는 `NanoThread`를 띄워 실행을 스케줄러에 넘긴다 (3장, p.118).[^rahman2025]

## 스케줄러

- `NanoThreadScheduler`가 `NanoThread` 인스턴스를 관리하고 실행하는 결정적 역할을 맡는다. 작업
  스케줄링에는 포크/조인 풀을 쓰고, 스레드가 멈추고 양보하는 흔한 이유인 I/O 바운드 연산을 흉내 내는
  데는 `ScheduledExecutorService`를 쓴다 (3장, p.119).[^rahman2025]
- 추적 수단이 스레드 로컬이다 — `CURRENT_NANO_THREAD`라는 `ThreadLocal` 변수를 두어 지금 어느 워커
  스레드에서 어느 `NanoThread`가 실행 중인지 추적한다 (3장, p.119).[^rahman2025] 그 방식이 진짜
  가상 스레드에서 부딪히는 문제는
  [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md)에 있다.
- 풀의 크기가 둘이다 — `schedule()` 메서드가 `NanoThread` 인스턴스를 포크/조인 풀에 제출하고 거기서
  실제 실행이 일어난다. 이 풀은 워커 스레드 두 개로 돌며 큐에서 작업을 계속 확인한다. 더 늘릴 수도
  있지만 시연에는 둘로 충분하다는 것이 저자의 말이다 (3장, p.119).[^rahman2025] 진짜 가상 스레드
  스케줄러가 왜 같은 종류의 풀인지는
  [포크조인 풀이 가상 스레드 스케줄러가 된 이유](../concepts/fork-join-pool-as-virtual-thread-scheduler.md)에
  있다.

## I/O를 흉내 내는 자리

- 예제의 I/O 바운드 작업이 파일 전송이다. `IO_EVENT_SCHEDULER`가 무작위 지연으로 작업을 예약해
  실제 I/O 동작을 흉내 낸다 (3장, p.119).[^rahman2025]
- `FileOperation.transfer()`가 하는 일이 세 걸음이다 — 무작위 지연 뒤에 이 `NanoThread`를 다시
  스케줄하도록 `IO_EVENT_SCHEDULER`에 걸어 두고, 현재 `NanoThread` 기록을 지우고,
  `Continuation.yield(SCOPE)`를 부른다 (3장, pp.119–120).[^rahman2025]
- 그때 벌어지는 일이 핵심이다 — 현재 `NanoThread`가 양보해 자기 실행을 내려놓고 다른 스레드가 돌
  수 있게 한다. `transfer` 메서드에서 `Continuation.yield(SCOPE)`가 실행되면, 포크/조인 풀의 워커
  스레드는 `run` 메서드가 반환했으니 일이 끝난 줄 알고 다른 `NanoThread`를 실행하러 간다 (3장,
  p.120).[^rahman2025]
- 되돌아오는 쪽도 한 줄이다 — 지연이 지나면 `IO_EVENT_SCHEDULER`가 그 `NanoThread`를 다시 스케줄해
  멈춘 자리에서 이어 가게 한다 (3장, p.120).[^rahman2025]

## 출력이 보여 주는 것

- 데모는 이 시스템으로 파일 넷을 동시에 옮기며, 무작위 지연에 따라 양보하고 재개하게 둔다 (3장,
  pp.120–121).[^rahman2025]
- 저자가 출력에서 짚는 자리가 하나다 — 어떤 파일은 `ForkJoinPool-1-worker-2`에서 실행을 시작했는데
  완료될 때는 `ForkJoinPool-1-worker-1`이 실행하고 있었다. `NanoThread`는 그대로인데 밑에 깔린 워커
  스레드가 바뀐 것이다 (3장, p.121).[^rahman2025]
- 그리고 이것이 진짜와 같다고 못박는다 — 가상 스레드에서도 정확히 이 일이 벌어진다. 가상 스레드가
  어떤 워커 스레드에서 시작해도, I/O 때문에 양보하면 다시 스케줄될 때 완전히 다른 워커에서 끝날 수
  있다 (3장, p.121).[^rahman2025] 그 이동이 진짜 구현에서 무엇으로 되어 있는지는
  [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md)에 있다.

## 이어지는 페이지

- [자바의 후속문 API](../concepts/java-continuation-api.md) — 이 실습이 얹혀 있는 내부 API
- [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md) — 워커가 바뀌어도
  실행이 이어지는 이유
- [포크조인 풀이 가상 스레드 스케줄러가 된 이유](../concepts/fork-join-pool-as-virtual-thread-scheduler.md)
  — 저자가 흉내 낸 그 스케줄러의 진짜 근거
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 워커가 바뀌는 일을 가상 스레드 쪽 용어로 본 자리
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 이 실습이 쓴
  추적 방식이 진짜에서 부딪히는 것
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 흉내가 아니라 진짜로
  무엇이 깨우는가
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" — "Building Our
    Own Virtual Threads from Scratch"(pp.117–121), "The NanoThread class"(pp.117–118),
    "The NanoThread scheduler"(p.119), "Simulating I/O operations with file transfer"(pp.119–120),
    "Putting it all together"(pp.120–121). 인용한 `run()`은 원문(p.118) 그대로다. 원문이 실은
    `NanoThread` 클래스 전문(p.118), `NanoThreadScheduler`(p.119), `FileOperation`(p.120),
    `NanoThreadDemo`(pp.120–121)와 실행 출력(p.121)은 개념당 대표 코드 하나 규칙에 따라 펜스로
    옮기지 않고 서술로만 담았다 — 원문은 `archive/` 스냅샷이 보존한다. 그림 3-7(NanoThread의
    상위 수준 설계, p.122)은 옮기지 않았다.

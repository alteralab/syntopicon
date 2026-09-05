---
type: concept
title: 자바의 후속문 API
description: 후속문이 프로그램의 실행 상태를 저장했다가 멈춘 자리에서 이어 가는 능력이며 스레드의 문맥 전환보다 잘게 메서드 수준까지 적용된다는 것, 자바에서는 그것이 공개 API가 아니라 jdk.internal.vm의 내부 API라 특별한 실행 인자를 요구하고 예고 없이 바뀔 수 있다는 것, 그리고 가상 스레드가 I/O를 만나면 이 yield로 캐리어에서 내려온다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 자바의 후속문 API

- [버전 조건](#버전-조건)
- [후속문이란 무엇인가](#후속문이란-무엇인가)
- [메서드 수준이라는 것](#메서드-수준이라는-것)
- [내부 API라는 사실](#내부-api라는-사실)
- [멈추고 이어지는 흐름](#멈추고-이어지는-흐름)
- [가상 스레드 안에서의 자리](#가상-스레드-안에서의-자리)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드가 멈췄다 이어지는 능력의 실물은 자바에서 무엇으로 되어 있는가.**

zhou2024가 후속문의 개념과 계보를 담는다 —
[가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)이 그 자리이고, 이 페이지는
그 개념이 자바에서 어떤 클래스와 메서드로 실재하는가를 맡는다.

## 버전 조건

> **버전 조건**: JDK 21 이상. 저자는 자바 21부터 후속문을 내부 패키지를 통해 쓸 수 있다고 적는다.
> 다만 이것은 **공개 자바 API가 아니라 내부 API다** — `jdk.internal.vm.Continuation`과
> `ContinuationScope`는 `--add-exports java.base/jdk.internal.vm=ALL-UNNAMED`라는 특별한 실행
> 인자 없이는 접근할 수 없고, 저자는 내부 API가 예고 없이 바뀌거나 사라질 수 있다고 못박는다.
> 그래서 여기 적힌 클래스 이름과 메서드 모양은 **JDK 21 시점의 내부 구현**을 가리키며, 위쪽 경계가
> 열려 있다. 저자 자신이 이 코드를 운영 코드에 쓰지 말고 오직 예시 목적으로만 보라고 적는다.

## 후속문이란 무엇인가

- 후속문(continuation)은 수학과 컴퓨터 과학과 일상 언어에 걸쳐 서로 다른 뜻을 지니는 추상적인
  개념이다. 프로그래밍에서의 뜻은 저자가 한 문장으로 정의한다 (3장, p.113):[^rahman2025]

  > In programming, a continuation refers to the ability of a program to save its current
  > execution state and resume later from where it stopped.

- 스레드와의 비교로 감을 잡게 한다 — 스레드가 실행되다가 문맥 전환(context switch)에서 나중에 이어
  갈 수 있도록 자기 상태의 스냅샷을 뜨는 것과 비슷하다 (3장, p.113).[^rahman2025]

## 메서드 수준이라는 것

- 다만 후속문에서는 이 개념이 더 잘게, 메서드 수준까지 적용된다 (3장, p.113).[^rahman2025]
- 저자의 예가 몇 줄짜리 메서드다 — 보통은 메서드를 부르면 모든 줄이 차례로 실행되고, 중간에 빠져
  나갔다가 다시 부르면 처음부터 시작한다. 그러나 후속문이라면 메서드가 특정 지점에서 멈췄다가 다시
  불릴 때 실행 상태를 보존한 채 정확히 멈춘 자리에서 이어 갈 수 있다 (3장, p.113).[^rahman2025]
- 쓰임이 넷 이상이다 — 후속문은 예외 처리, 논블로킹 I/O 연산, 동시성 제어, 제너레이터(generator)
  따위 프로그래밍의 여러 자리에서 실용적으로 쓰인다 (3장, p.113).[^rahman2025]
- 제너레이터가 무엇인지가 각주에 있다 — 시간에 걸쳐 여러 값을 내놓을 수 있는 함수로, 내놓는 사이에
  실행을 멈춘다. 다시 불리면 멈춘 자리에서 실행을 이어 가며, 이것이 후속문의 동작과 닮았다 (3장,
  p.113 각주 2).[^rahman2025] 같은 기제를 파이썬 쪽에서 본 자리는
  [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md)에 있다.

## 내부 API라는 사실

- 저자는 이 API를 운영 코드에 직접 쓰는 것은 권장되지 않지만, 어떻게 도는지 아는 것은 여전히 값이
  있다고 적으며 학습용으로만 예제를 연다 (3장, p.114).[^rahman2025]
- 접근 조건이 명시된다 — `Continuation`과 `ContinuationScope`는 `jdk.internal.vm` 패키지의
  클래스이고, 공개 자바 API의 일부가 아니라서 특별한 JVM 인자를 더해야 접근할 수 있다 (3장,
  p.114).[^rahman2025]
- 경고가 별도 상자에 있다 (3장, p.114):[^rahman2025]

  > Internal APIs can change or be removed without notice, which can lead to undesirable
  > situations.

- 두 클래스의 역할이 갈린다 — `ContinuationScope`는 후속문에 유일한 범위를 만드는 데 쓰이고,
  `Continuation`은 본질적으로 멈췄다가 재개할 수 있는 코드 조각이다 (3장, p.114).[^rahman2025]

## 멈추고 이어지는 흐름

- 예제의 뼈대가 세 줄이다 — 범위를 하나 만들고, 그 범위에 묶인 후속문을 만들고, 그 후속문의 본문에서
  `Continuation.yield(scope)`를 부른다 (3장, p.114).[^rahman2025]

  ```java
  ContinuationScope scope = new ContinuationScope("main");
  Continuation continuation = new Continuation(scope, () -> {
      System.out.println("Hello from continuation");
      Continuation.yield(scope);
      System.out.println("Done from continuation");
  });
  continuation.run();
  continuation.run();
  ```

- 실행 흐름을 저자가 따라간다 — `continuation.run()`을 부르면 후속문이 실행을 시작하고, 본문이
  첫 줄을 찍은 뒤 `Continuation.yield(scope)`를 부른 자리에서 양보한다. 이 시점에 후속문은 멈추고
  제어가 `main`으로 돌아간다 (3장, pp.114–115).[^rahman2025]
- 다시 부르면 이어진다 — `continuation.run()`을 다시 부르면 멈춘 자리에서 재개해 다음 줄을 찍고 또
  양보한다. 양보가 더 남아 있지 않으면 후속문이 완료된다 (3장, p.115).[^rahman2025]

## 가상 스레드 안에서의 자리

- 저자가 이것이 가상 스레드 내부에서 일어나는 일 그 자체라고 못박는다 — 가상 스레드에서 실행되는
  메서드가 I/O 연산을 시작하면, 후속문이 `Continuation.yield(scope)` 메서드를 불러 가상 스레드를
  멈추고 캐리어 스레드가 그것을 실행하는 상태에서 떼어낸다 (3장, p.115).[^rahman2025]
- 되돌아오는 쪽도 한 줄이다 — 나중에 I/O 연산이 끝나면 가상 스레드가 다시 스케줄되어 실행을 마친다
  (3장, p.115).[^rahman2025] 실제로 무엇이 그것을 깨우는지는
  [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md)에 있다.

## 이어지는 페이지

- [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md) — `yield`가
  실제로 무엇을 옮기는가
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 후속문의 개념과 계보,
  그리고 후속문과 스케줄러의 분리
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 같은 일을 가상 스레드 쪽 용어로 본 자리
- [직접 만들어 본 가상 스레드](../concepts/nano-thread-from-scratch.md) — 이 API로 가상 스레드를
  흉내 내 본 자리
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 멈춘 것을 깨우는 쪽
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 제너레이터가 같은
  기제를 담당하는 파이썬 쪽
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" —
    "Continuation"(pp.113–115), 제너레이터 각주 2(p.113), 내부 API 경고 상자(p.114).
    인용한 코드는 원문 `ContinuationExample`(p.114)에서 클래스와 `main` 껍데기를 벗기고 양보를
    두 번에서 한 번으로 줄여 뼈대만 남긴 것이다. 원문의 실행 출력 예시(p.114)는 옮기지 않고
    서술로만 담았다 — 원문은 `archive/` 스냅샷이 보존한다. 이 절에는 그림이 없다.

---
type: concept
title: 가상 스레드와 ReentrantLock
description: 동기화 블록 대신 ReentrantLock을 쓰면 가상 스레드가 락을 쥔 채 블로킹해도 캐리어에서 내려올 수 있다는 것, 그 차이가 객체 모니터와 park/unpark 기제의 차이에서 온다는 것, 그리고 런타임이 그때 밟는 네 단계
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드와 ReentrantLock

- [버전 조건](#버전-조건)
- [무엇이 다른가](#무엇이-다른가)
- [캐리어가 바뀌는 것을 눈으로 보기](#캐리어가-바뀌는-것을-눈으로-보기)
- [차이의 자리는 park와 unpark다](#차이의-자리는-park와-unpark다)
- [런타임이 밟는 네 단계](#런타임이-밟는-네-단계)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **왜 `ReentrantLock`은 가상 스레드를 캐리어에 묶지 않는가.**

## 버전 조건

> **버전 조건**: JDK 21에서 23까지. 이 구간에서는 `synchronized`가 핀닝을 만들므로
> `ReentrantLock`을 고르는 근거가 핀닝 회피 그 자체다. **JDK 24 이상에는 그 근거가 적용되지
> 않는다** — JEP 491이 동기화 블록 쪽 핀닝을 걷어 냈고, 그 뒤로는 공정성이나 try-lock 같은
> 기능 차이가 선택의 기준으로 남는다.
> [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md)이 그 경계를 담는다.

## 무엇이 다른가

- `ReentrantLock`은 전통적인 `synchronized` 블록보다 유연한 자바의 동기화 장치다. 더 정교한
  스레드 상호작용을 허용하고 공정성, try-lock, 인터럽트 가능성 같은 기능을 더 준다 (2장,
  p.64).[^rahman2025] 그 기능 목록을 가상 머신 쪽에서 본 자리가
  [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md)이다.
- 여기서 저자가 꼽는 핵심 이점은 하나다 — 가상 스레드의 핀닝 문제를 피하는 능력이다 (2장,
  p.64).[^rahman2025]
- 기제가 한 줄로 요약된다 — 가상 스레드를 캐리어에 묶어 버리는 동기화 블록 대신 `ReentrantLock`을
  쓰면, 가상 스레드가 블로킹될 때 캐리어에서 내려올 수 있어 그 캐리어를 다른 태스크가 쓸 수 있게
  된다 (2장, p.64).[^rahman2025]

## 캐리어가 바뀌는 것을 눈으로 보기

- 저자가 앞의 핀닝 실험과 같은 모양을 `ReentrantLock`으로 다시 짠다 (2장, p.64).[^rahman2025]

  ```java
  public class PreventPinningExample {
      private static final ReentrantLock lock = new ReentrantLock();

      public static void main(String[] args) {
          var threadList = IntStream.range(0, 10)
              .mapToObj(i -> Thread.ofVirtual().unstarted(() -> {
                  if (i == 0) {
                      System.out.println(Thread.currentThread());
                  }
                  lock.lock();
                  try {
                      Thread.sleep(25);
                  } catch (InterruptedException e) {
                      Thread.currentThread().interrupt();
                  } finally {
                      lock.unlock();
                  }
                  if (i == 0) {
                      System.out.println(Thread.currentThread());
                  }
              })).toList();

          threadList.forEach(Thread::start);
          threadList.forEach(thread -> {
              try {
                  thread.join();
              } catch (InterruptedException e) {
                  Thread.currentThread().interrupt();
              }
          });
      }
  }
  ```

- 차이는 출력에서 드러난다 — 같은 가상 스레드가 처음에는 `ForkJoinPool-1-worker-1`에 마운트되어
  있다가 나중에는 `ForkJoinPool-1-worker-3`에 다시 마운트된 것으로 찍힌다 (2장,
  p.65).[^rahman2025]
- 판독이 곧 결론이다 — 가상 스레드가 처음에는 한 캐리어에서 돌다가 나중에 다른 캐리어로 옮겨
  갔다는 뜻이고, `synchronized` 블록 대신 `ReentrantLock`을 썼기 때문에 가능한 일이다. 핀닝
  문제를 피하고 자바 런타임이 쓸 수 있는 캐리어 스레드 위에 가상 스레드를 최적으로 스케줄링하게
  해 준다 (2장, pp.65–66).[^rahman2025]
- 잠금 해제의 자리도 규칙이다 — `unlock` 연산은 반드시 `finally` 블록 안에서 이뤄져야 예외가
  나더라도 락이 풀리고 교착을 막는다 (2장, p.65).[^rahman2025]

## 차이의 자리는 park와 unpark다

- 핵심 차이가 구현에 있다 — `synchronized` 블록은 객체 모니터(object monitor)를 쓰는데 그것이
  현재로서는 핀닝을 요구하고, `ReentrantLock`은 가상 스레드를 아는 park/unpark 기제를 쓴다 (2장,
  p.66).[^rahman2025] 객체 모니터가 가상 머신 안에서 받는 최적화들은
  [락 최적화](../concepts/lock-optimization.md)에 있다.
- park/unpark는 자바의 낮은 수준 스레드 협조 원시 장치이고, 더 높은 수준의 동시성 유틸리티 여럿의
  바탕을 이룬다 (2장, p.66).[^rahman2025]
- 스레드가 `LockSupport.park()`를 부르면 파크된 상태, 곧 블로킹된 상태가 되며 세 가지 가운데
  하나가 일어날 때까지 그렇다 (2장, p.66).[^rahman2025]
  - 다른 스레드가 이 스레드를 대상으로 `unpark()`를 부른다.
  - 이 스레드가 인터럽트된다.
  - 호출이 헛되이 돌아온다(드물지만 가능하다).
- `LockSupport.unpark(thread)`를 부르면 대상 스레드가 나아갈 수 있게 된다 (2장,
  p.66).[^rahman2025]
- **왜 이것이 가상 스레드 친화적인가** — 가상 머신이 가상 스레드가 파크하는 것을 감지해 캐리어
  스레드에서 내려놓을 수 있기 때문이다. `synchronized`가 쓰는 객체 모니터는 가상 스레드가 마운트된
  채로 남아 있기를 요구한다는 점에서 다르다 (2장, p.66).[^rahman2025]

## 런타임이 밟는 네 단계

- 가상 스레드가 `ReentrantLock`에서 블로킹되면 런타임이 다음을 할 수 있다 (2장,
  p.66).[^rahman2025]
  1. 가상 스레드의 상태를 저장한다.
  2. 캐리어 스레드에서 내려놓는다.
  3. 그 캐리어를 다른 가상 스레드에 쓴다.
  4. 나중에 락이 풀리면 쓸 수 있는 아무 캐리어에나 그 가상 스레드를 다시 마운트한다.
- 이 네 단계가
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)이
  서술한 일반 동작을 락 위에서 되풀이한 것이다.

## 이어지는 페이지

- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 이 대안이 피하려는 현상과 그
  버전 경계
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 내려놓기의 일반형
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — `ReentrantLock`이
  더 주는 것과 그럼에도 `synchronized`를 권하던 근거
- [락 최적화](../concepts/lock-optimization.md) — 객체 모니터 쪽의 최적화들
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 두 방식의 차이를 기록으로
  확인하는 자리
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Addressing the Pinning
    Problem with ReentrantLock"(pp.64–66), "The Park/Unpark Mechanism"(p.66). 저자는 이
    설명을 쉽게 풀어 준 시모네 보르뎃(Simone Bordet)에게 감사를 적는다(p.67). 개념당 대표 코드
    하나 규칙에 따라 `PreventPinningExample`만 실었고, `LockSupport.park`·`unpark`를 보이는
    두 줄짜리 조각(p.66)은 본문에 이름으로만 옮겼다.

---
type: concept
title: 가상 스레드에서 달라지는 Thread API
description: 가상 스레드도 Thread 인스턴스라서 취소는 인터럽트로 똑같이 되지만, 스레드 그룹이 하나로 고정되고 우선순위와 데몬 여부를 바꿀 수 없으며, 새 메서드와 폐기된 메서드가 생기고, 전체 스택 트레이스 조회와 캐리어 식별이 막혀 있다는 것
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드에서 달라지는 Thread API

- [버전 조건](#버전-조건)
- [같은 것 — 인터럽트](#같은-것--인터럽트)
- [바꿀 수 없는 성질들](#바꿀-수-없는-성질들)
- [새 메서드와 폐기된 메서드](#새-메서드와-폐기된-메서드)
- [막혀 있는 두 가지](#막혀-있는-두-가지)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드를 쓸 때 `Thread` API의 어느 부분이 그대로이고 어느 부분이
달라지는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 아래의 폐기·추가 이력은 각 claim에 걸린 조건이 따로 말한다.

## 같은 것 — 인터럽트

- 출발점이 같음이다 — 자바의 가상 스레드는 본질적으로 `Thread` 클래스의 인스턴스이고, 취소는
  플랫폼 스레드와 같은 방식, 곧 `interrupt()` 메서드 호출로 이뤄진다 (2장, p.37).[^rahman2025]
- 조건도 같다 — 스레드 안에서 도는 코드가 인터럽트 플래그를 확인하거나, 인터럽트를 자동으로
  처리하는 메서드를 불러야 한다. 대부분의 블로킹 메서드가 후자에 해당한다 (2장,
  p.37).[^rahman2025]
- 저자가 두 예제를 나란히 돌려 같은 출력을 얻는다. 그것이 가상 스레드가 플랫폼 스레드와 같은
  인터럽트 의미론을 유지한다는 증거이고, **유일한 차이는 `Thread.sleep()` 같은 가상 스레드의
  블로킹 연산이 밑의 캐리어 스레드를 다른 가상 스레드에게 자동으로 양보한다는 점이다** (2장,
  p.38).[^rahman2025]

## 바꿀 수 없는 성질들

- 스레드 그룹이 하나다 — 모든 가상 스레드는 단일 스레드 그룹에 속하고, 다른 스레드 그룹으로
  가상 스레드를 만드는 API는 없다. 가상 스레드를 만들어 `getThreadGroup()`을 부르면 언제나 같은
  `ThreadGroup` 인스턴스를 얻는다 (2장, p.39).[^rahman2025] 저자가 100개를 만들어 집합에 모으면
  크기가 1이 나오고, 그 그룹의 이름은 `VirtualThreads`다 (2장, p.39).[^rahman2025]

  ```java
  public class VirtualThreadGroupExample {
      public static void main(String[] args) throws InterruptedException {
          Set<ThreadGroup> threadGroups = new HashSet<>();

          for (int i = 0; i < 100; i++) {
              Thread vThread = Thread.ofVirtual().start(() -> {
                  try {
                      Thread.sleep(10);
                  } catch (InterruptedException e) {
                      Thread.currentThread().interrupt();
                  }
              });
              threadGroups.add(vThread.getThreadGroup());
          }
          Thread.sleep(1000); // Wait for threads to complete
          System.out.println("Unique thread groups: " + threadGroups.size());
          System.out.println("Thread group: " + threadGroups.iterator().next());
      }
  }
  ```

- 우선순위가 고정이다 — 가상 스레드의 우선순위는 `NORM_PRIORITY`로 잡혀 있고, 가상 스레드에
  `setPriority`를 불러도 우선순위가 바뀌지 않는다 (2장, p.39).[^rahman2025]
- 데몬 여부도 고정이다 — 모든 가상 스레드는 기본이 데몬 스레드이며 `setDaemon`으로 이 상태를
  바꾸려는 시도는 아무 효과가 없다 (2장, p.39).[^rahman2025] 그래서
  [가상 스레드를 만드는 방법](../concepts/creating-virtual-threads.md)의 함정이 회피 불가다.

## 새 메서드와 폐기된 메서드

- 판별 메서드가 생겼다 — `Thread::isVirtual` 인스턴스 메서드로 어떤 스레드가 가상인지 알 수 있다
  (2장, p.40).[^rahman2025]
- 기간을 받는 메서드가 생겼다 — `join(Duration)`과 `sleep(Duration)` 인스턴스 메서드는 가상
  스레드와 직접 관계는 없지만 편의를 더한다 (2장, p.40).[^rahman2025]
  - 버전 조건: Java 19 이상 — 이 두 메서드가 들어온 릴리스다.
- 식별자 메서드가 갈렸다 — 비final인 `getId()`는 폐기되었고 final인 `threadId()`를 쓰기를 권한다
  (2장, p.40).[^rahman2025]
- 위험한 넷이 예외를 던진다 — `stop()`, `suspend()`, `resume()`, `countStackFrames()`는
  플랫폼 스레드와 가상 스레드 모두에서 `UnsupportedOperationException`을 던진다. 본질적으로
  안전하지 않다는 것이 자바 문서가 밝힌 이유이고, 이 메서드들은 Java 1.2부터 폐기 상태였으며
  제거가 예정되어 있다 (2장, p.40).[^rahman2025]
  - 버전 조건: Java 20 이상 — 예외를 던지기 시작한 릴리스다. Java 19 이하에서는 폐기 표시만
    붙은 채 동작했다.

## 막혀 있는 두 가지

- 전체 조회가 반쪽이다 — 정적 `Thread::getAllStackTraces` 메서드는 플랫폼 스레드의 스택
  트레이스만 돌려주고 가상 스레드는 뺀다 (2장, p.40).[^rahman2025]
- 캐리어를 알 수 없다 — 주어진 가상 스레드를 어느 플랫폼 스레드가 실행하고 있는지 알아낼 방법이
  2025년 저술 시점에 없다 (2장, p.40).[^rahman2025] 이것은 결함이 아니라 설계된 투명성의 뒷면이다 —
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)이
  그 이유를 담는다. 대신 실행 중인 캐리어 이름은
  [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md)의 도구들이 보여 준다.
- 저자의 총평은 이전 비용 쪽이다 — 변화와 제약이 있어도 기존 API와 스레딩 개념에 폭넓게 닮아
  있어서 가상 스레드로의 전환이 개발자에게 거의 보이지 않는다 (2장, p.40).[^rahman2025]

## 이어지는 페이지

- [가상 스레드를 만드는 방법](../concepts/creating-virtual-threads.md) — 이 규칙들이 적용되는
  대상을 만드는 자리
- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 두 종류의
  갈림
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 캐리어를 알 수 없는 이유
- [자바 스레드 스케줄링과 상태 전이](../concepts/java-thread-scheduling-and-states.md) —
  우선순위가 플랫폼 스레드 쪽에서 하는 일
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Adapting to Virtual
    Threads"(pp.37–40). 개념당 대표 코드 하나 규칙에 따라 `VirtualThreadGroupExample`만
    실었고, `PlatformThreadInterruption`과 `VirtualThreadInterruption` 두 예제와 그 출력
    (pp.37–38)은 미수록이다 — 서술은 모두 옮겼다.

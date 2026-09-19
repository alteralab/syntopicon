---
type: concept
title: 자바 스레드의 생성과 시작
description: Thread 상속과 Runnable 구현이라는 두 출발점과 익명 내부 클래스와 람다로 이어진 표기의 변화, 상속 슬롯 하나를 쓰는 대가 때문에 Runnable이 선호가 된 이유, start가 run보다 더 하는 일과 run을 직접 부르면 무엇이 어긋나는가, 그리고 30년 가까이 그대로인 이 API 위에 실행자가 권장으로 얹힌 자리
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 자바 스레드의 생성과 시작

- [두 출발점과 그 뒤의 표기들](#두-출발점과-그-뒤의-표기들)
- [무엇을 고르는가는 상속 슬롯이 갈랐다](#무엇을-고르는가는-상속-슬롯이-갈랐다)
- [start가 run보다 더 하는 일](#start가-run보다-더-하는-일)
- [지금 권장은 실행자다](#지금-권장은-실행자다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드를 만드는 표기가 왜 넷이나 되고, 그중 무엇을 언제 쓰며, 시작은 왜
`start`여야 하는가.**

## 두 출발점과 그 뒤의 표기들

- 자바 1.0은 1996년에 나왔고 스레드 지원을 내장한 채 나왔다. 이 점이 당시 많은 언어와 자바를
  갈랐다 (1장, p.6).[^rahman2025]
- 초기의 방법은 둘이었다 — `Thread` 클래스를 상속하거나 `Runnable` 인터페이스를 구현하는
  것이다 (1장, p.6).[^rahman2025] 뒤에 표기가 둘 더 붙어 넷이 된다.

  ```java
  // Extending Thread class
  Thread t1 = new ThreadByExtension("Worker-1");
  t1.start();

  // Implementing Runnable (classic)
  Thread t2 = new Thread(new RunnableImplementation(), "Worker-2");
  t2.start();

  // Anonymous inner class (Java 1.1)
  Thread t3 = new Thread(new Runnable() {
      @Override
      public void run() {
          System.out.println("Anonymous: " + Thread.currentThread().getName());
      }
  }, "Worker-3");
  t3.start();

  // Lambda expression (Java 8)
  Thread t4 = new Thread(() ->
          System.out.println("Lambda: " + Thread.currentThread().getName()),
      "Worker-4");
  t4.start();
  ```

## 무엇을 고르는가는 상속 슬롯이 갈랐다

- 저자가 네 표기의 성격을 나란히 적어 둔다 (1장, p.7).[^rahman2025]
  - `Thread` 상속은 스레드 메서드에 직접 닿게 해 주지만 하나뿐인 상속 슬롯을 써 버린다.
  - `Runnable` 구현이 선호되는 방식이 되었다 — 작업의 정의와 스레드의 관리를 갈라 두고 상속의
    유연함을 남겨 두기 때문이다.
  - 익명 내부 클래스(anonymous inner class, Java 1.1)는 람다가 없던 시절에 한 번 쓰고 마는 작업의
    상용구를 줄여 주었다.
  - 람다 식(lambda expression, Java 8)은 `Runnable`이 함수형 인터페이스라서 그 구현을 더 짧게
    만들었다.
- 이 기초 API는 30년 가까이 그대로였고, 저자는 그것을 설계가 튼튼했다는 증거로 읽는다. 자바가
  `java.util.concurrent`부터 가상 스레드까지 수많은 동시성 기능을 보태는 동안에도 이 원래의 구성
  요소들이 자바 스레딩 모델의 바탕으로 남아 있다 (1장, p.8).[^rahman2025]

## start가 run보다 더 하는 일

- 어느 방법으로 만들었든 시작은 `Thread` 객체의 `start` 호출이다. 이것이 꼭 필요한 단계인 이유는
  `start`가 `run`을 실행하기만 하는 것이 아니라 시스템 자원 할당 같은 준비 작업까지 하기
  때문이다. 그 뒤에 `start`가 새 실행 스레드에서 `run`을 부른다 (1장, p.8).[^rahman2025]
- 그래서 `run`을 직접 부르면 안 된다 — 그렇게 하면 새 스레드가 아니라 부른 쪽 스레드에서 `run`이
  실행된다 (1장, p.8).[^rahman2025]

## 지금 권장은 실행자다

- 2025년 저술 시점의 자바 애플리케이션에서는 생성자로 스레드를 손수 만드는 것보다 실행자 프레임워크(Executor
  framework)를 쓰는 편이 효율적이다. 실행자는 미리 만들어 둔 스레드 묶음인 스레드 풀(thread pool)을
  유지해 스레드 관리 과정을 감추고, 새 스레드를 만드는 데 드는 부담을 크게 줄인다 (1장,
  p.8).[^rahman2025]
- 작업이 실행자에 제출되면 큐에 들어가고, 풀의 스레드 하나가 큐에서 그 작업을 집어 실행한다. 이
  구조가 동시성 프로그래밍을 단순하게 만들고 스레드를 재사용해 자원 활용을 낫게 한다 (1장,
  p.8).[^rahman2025]
  - 실행자가 그 대신 무엇을 못 하는지는
    [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)에 있다.

## 이어지는 페이지

- [자바 플랫폼의 바탕인 스레드](../concepts/threads-as-java-platform-substrate.md) — 여기서 만드는
  그 스레드가 플랫폼에서 무엇을 떠받치는가
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 손수 만들기를
  대신하는 자리와 그 자리에 남은 문제
- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 손수 만든 스레드가 몇 개까지
  늘어날 수 있는가
- [자바 스레드 스케줄링과 상태 전이](../concepts/java-thread-scheduling-and-states.md) — `start`
  뒤에 스레드가 오가는 상태들
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "The Genesis of Java 1.0 Threads"(pp.6–8),
    "Starting Threads"(p.8). 인용한 코드는 원문 `ThreadCreationDemo`의 `main` 메서드 본문이며,
    클래스 선언과 함께 실린 `ThreadByExtension`·`RunnableImplementation` 정의는 덜어 냈다.
    원문의 조판 줄바꿈은 폈다.

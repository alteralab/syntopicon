---
type: concept
title: 가상 스레드 핀닝
description: 가상 스레드가 캐리어에서 내려오지 못하고 묶이는 현상 — 그것이 일어나는 두 자리, 처리량과 자원과 확장성에 남기는 해악, 블록 안 연산의 성질에 따라 갈리는 심각도, 그리고 JEP 491이 JDK 24에서 동기화 블록 쪽 핀닝을 걷어 낸 뒤에도 남는 경우들
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드 핀닝

- [버전 조건](#버전-조건)
- [무엇인가](#무엇인가)
- [일어나는 두 자리](#일어나는-두-자리)
- [무엇을 망가뜨리는가](#무엇을-망가뜨리는가)
- [동기화 블록에서 보는 실물](#동기화-블록에서-보는-실물)
- [심각도는 블록 안의 연산이 정한다](#심각도는-블록-안의-연산이-정한다)
- [JDK 24가 바꾼 것과 남긴 것](#jdk-24가-바꾼-것과-남긴-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드가 캐리어에서 내려오지 못하면 무슨 일이 벌어지는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 핀닝이라는 현상 자체는 가상 스레드가 정식이 된 뒤의 이야기다.
> **동기화 블록이 핀닝을 만드는 서술은 JDK 21에서 23까지에만 적용된다** — JDK 24부터는
> JEP 491이 그것을 걷어 냈고, 그 경계는 아래 "JDK 24가 바꾼 것과 남긴 것"에 있다. 네이티브
> 호출 쪽은 [네이티브 호출과 핀닝](../concepts/native-method-pinning.md)이 따로 담는다.

## 무엇인가

- 정의가 묶임이다 — 가상 스레드 맥락에서 핀닝(pinning)은 가상 스레드가 자신이 도는 밑바탕 플랫폼
  스레드, 곧 캐리어 스레드에 묶이는 상황을 가리킨다 (2장, p.61).[^rahman2025]
- 묶여 있는 동안의 성질이 문제다 — 핀닝된 가상 스레드는 블로킹 연산을 만나더라도 캐리어 스레드에서
  자신을 내려놓을 수 없고, 핀닝이 지속되는 동안 그 캐리어 스레드를 독점한다 (2장,
  p.61).[^rahman2025] 내려놓기가 원래 어떻게 되는지는
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)에
  있다.

## 일어나는 두 자리

- 동기화 블록이나 메서드 — 가상 스레드가 `synchronized` 블록이나 메서드에 들어가면 캐리어 스레드에
  핀닝된다. 그 블록이나 메서드가 실행되는 동안 캐리어 스레드를 다른 태스크에 재사용할 수 없다
  (2장, p.61).[^rahman2025]
- 네이티브 메서드나 외부 함수 — 가상 스레드가 네이티브 메서드나 외부 함수(foreign function)를
  실행할 때도 핀닝된다 (2장, p.61).[^rahman2025] 그 경우의 내막은
  [네이티브 호출과 핀닝](../concepts/native-method-pinning.md)에 있다.

## 무엇을 망가뜨리는가

- 전제는 캐리어의 유한성이다 — 가상 스레드의 본질은 블로킹 연산을 할 때 캐리어에서 내려와 캐리어를
  다른 태스크에 풀어 주는 능력인데, 캐리어 스레드의 수는 제한되어 있다. 많은 가상 스레드가 오래
  핀닝되면 그 캐리어들을 묶어 버려 다른 가상 스레드의 실행을 막고, 가상 스레드가 주는 동시성의
  이점을 사실상 제한한다 (2장, p.61).[^rahman2025]
- 처리량 저하 — 핀닝된 가상 스레드가 자기 캐리어를 차지하고 있으므로 다른 가상 스레드는 빈 캐리어를
  기다려야 하고 시스템 전체 처리량이 떨어진다 (2장, p.62).[^rahman2025]
- 자원 비효율 — 캐리어 스레드는 시스템 능력에 매인 유한한 자원이라, 핀닝된 가상 스레드 때문에
  막혀 있는 것은 그 자원을 비효율적으로 쓰는 일이다 (2장, p.62).[^rahman2025]
- 확장성 우려 — 동기화 블록이나 네이티브 메서드를 자주 써서 가상 스레드의 상당 부분이 핀닝되면
  확장성 문제에 부딪힐 수 있다 (2장, p.62).[^rahman2025]
- 규모를 키우면 그림이 분명해진다 — 1,000이나 10,000개의 가상 스레드가 모두 블로킹 연산이 든 동기화
  블록에 들어가려 하면, 쓸 수 있는 캐리어가 몇 개뿐이라 대부분이 빈 캐리어를 기다리며 줄을 서고
  높은 동시성을 위해 가상 스레드를 쓴 목적이 무너진다 (2장, p.63).[^rahman2025]
- 완화 전략이 둘이다 — `synchronized` 블록이나 메서드 대신 `java.util.concurrent.locks`의
  `ReentrantLock`을 쓰는 것(블로킹될 때 가상 스레드가 내려올 수 있게 해 주므로), 그리고 가상
  스레드 맥락에서 동기화 메서드·블록과 네이티브 메서드의 사용을 정기적으로 점검해 줄이는 것이다
  (2장, p.62).[^rahman2025] 그 대안은
  [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md)에 있다.

## 동기화 블록에서 보는 실물

- 저자가 가상 스레드 열 개를 만들어 각각 동기화 블록 안에서 25밀리초를 자게 하고, 첫 스레드에
  대해 블록 진입 전후로 스레드 정보를 찍는다 (2장, pp.62–63).[^rahman2025]

  ```java
  public class ThreadPinnedExample {
      private static final Object lock = new Object();

      public static void main(String[] args) {
          List<Thread> threadList = IntStream.range(0, 10)
              .mapToObj(i -> Thread.ofVirtual().unstarted(() -> {
                  if (i == 0) {
                      System.out.println(Thread.currentThread());
                  }
                  synchronized (lock) {
                      try {
                          Thread.sleep(25);
                      } catch (InterruptedException e) {
                          Thread.currentThread().interrupt();
                      }
                  }
                  if (i == 0) {
                      System.out.println(Thread.currentThread());
                  }
              })).toList();

          threadList.forEach(Thread::start);
          threadList.forEach(t -> {
              try {
                  t.join();
              } catch (InterruptedException e) {
                  Thread.currentThread().interrupt();
              }
          });
      }
  }
  ```

- 판독 방법이 캐리어 이름이다 — 출력의 캐리어 스레드 식별자(`ForkJoinPool-1-worker-1`)가 동기화
  블록 전후로 같으면, 가상 스레드가 캐리어를 바꾸지 않았다는 뜻이고 곧 블로킹 연산 내내 핀닝되어
  있었다는 증거다 (2장, p.63).[^rahman2025]
- 원래대로라면 자고 있는 가상 스레드는 캐리어에서 내려와 그 캐리어가 다른 가상 스레드를 돌리게
  해야 하는데, 동기화 블록 안에서는 25밀리초 내내 캐리어를 독점한다 (2장, p.63).[^rahman2025]

## 심각도는 블록 안의 연산이 정한다

- `synchronized` 키워드가 핀닝을 부를 수 있지만 그 영향은 블록 안의 구체적인 코드에 따라 달라진다
  (2장, p.66).[^rahman2025] 저자가 세 경우를 든다 (2장, pp.66–67).
  - 위험이 작은 경우 — `synchronized (this) { return this.a + this.b; }`처럼 블록 안의 연산이
    극히 짧으면, 락을 기다려야 하더라도 아주 빨리 풀릴 가능성이 높아 영향이 작다.
  - 문제가 될 수 있는 경우 — 블로킹 네트워크 호출이 동기화 블록 안에 있으면 그 요청이 도는 내내
    가상 스레드가 핀닝된 채로 남아 동시성 이득을 갉아먹는다.
  - 비슷한 문제 — `Object.wait()` 호출도 동기화 블록 안에서 핀닝으로 이어지며, 통지가 올 때까지
    가상 스레드가 핀닝된 채로 남는다.
- 요점이 한 줄이다 — 짧고 블로킹하지 않는 연산은 대체로 괜찮고, 블로킹 호출은 신중한 검토를
  요구한다 (2장, p.67).[^rahman2025]
- 저자가 앞날에 한 줄을 남긴다 — 앞으로의 JDK 갱신이 "언핀 인식(unpinning-aware)" I/O 연산을
  들여 일부 상황의 핀닝을 완화할 수도 있다. 지금으로서는 가상 스레드로 확장성을 최대로 끌어낼 때
  더 유연한 동기화 수단인 `ReentrantLock`을 선호하는 것이 대체로 현명하다 (2장,
  p.67).[^rahman2025]

## JDK 24가 바꾼 것과 남긴 것

- 경계가 분명하다 — JEP 491 "Synchronize Virtual Threads Without Pinning"이 JDK 24에 전달되어
  `synchronized` 키워드를 가상 스레드 친화적으로 재작업했다 (2장, p.70).[^rahman2025]
  - 버전 조건: JDK 24 이상 — 이 변화가 적용되는 구간이다. JDK 23 이하에서는 위의 동기화 블록
    핀닝 서술이 그대로 유효하다.
- 무엇이 달라졌는가 — 가상 스레드가 자신의 캐리어 스레드와 무관하게 모니터를 획득하고 보유하고
  해제할 수 있게 되었고, 가상 머신 스케줄러가 블로킹된 가상 스레드를 플랫폼 스레드에서 내려놓도록
  허용해 다른 태스크가 계속 돌 수 있게 자원을 풀어 준다 (2장, p.70).[^rahman2025]
- **완전히 없어지지는 않는다** — 클래스 초기화자 안에서 블로킹하거나, 다른 스레드의 클래스 초기화를
  기다리거나, 클래스 로딩 중 심볼 참조를 해석하거나, 네이티브 코드를 호출하는 등의 가장자리
  경우에서는 여전히 핀닝이 생긴다. 이런 상황은 비교적 드물지만 동시성이 매우 높은 애플리케이션에서는
  문제가 될 수 있고, JEP 491은 이 경우들을 감시하다가 필요하면 앞으로 다듬자고 제안한다 (2장,
  p.70).[^rahman2025]
- 단서가 붙는다 — 이 개선의 이득을 보려면 JDK 24 이상으로 옮겨야 한다. 저자는 집필 시점(초판
  2025년 9월) 판단으로, JDK 21이 여전히 장기 지원(LTS) 버전이고 대부분의 애플리케이션이 그것에
  기대고 있으므로 핀닝 문제를 계속 의식하고 그에 맞춰 애플리케이션을 설계하는 것이 합리적이라고
  적는다 (2장, p.70).[^rahman2025]
- 책을 맺으면서 저자가 같은 단서를 한 번 더 적는다 — JDK 24가 동기화 블록에 얽힌 핀닝 문제를
  풀지만, 모든 운영 시스템이 JDK 21 같은 이전 버전에서 JDK 24로 곧바로 옮기지는 않으리라는 점을
  짚어 둘 필요가 있다는 것이다 (8장, p.312).[^rahman2025] 그래서 이 페이지의 JDK 23 이하 서술은
  릴리스가 나왔다고 곧바로 죽는 것이 아니라, 현장의 이전 속도만큼 더 살아 있다.

## 이어지는 페이지

- [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md) — 동기화
  블록을 대신하는 수단과 그것이 핀닝을 피하는 기제
- [네이티브 호출과 핀닝](../concepts/native-method-pinning.md) — JEP 491 뒤에도 남는 쪽
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 핀닝이 막는 그 동작
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 핀닝을 실제로 찾아내는 도구
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — `synchronized`와
  `ReentrantLock`의 비교를 가상 머신 쪽에서 본 자리
- [락 최적화](../concepts/lock-optimization.md) — 객체 모니터가 가상 머신 안에서 받는 최적화들
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Limitations of Virtual
    Threads"(pp.61–62), "Pinning"(pp.62–63), "Synchronized Blocks and Virtual Thread
    Pinning"(pp.66–67), "JEP 491: Synchronize Virtual Threads Without Pinning"(p.70).
    이전 속도 단서는 8장 "Conclusion and Takeaways"(p.312).
    개념당 대표 코드 하나 규칙에 따라 `ThreadPinnedExample`만 실었고, 심각도 절의 세 동기화
    블록 조각(pp.66–67)은 본문에 짧게 옮기거나 서술로만 담았다.

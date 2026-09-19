---
type: concept
title: 블로킹 I/O와 스레드 효율
description: 신용 점수 계산 예제로 본 순차 블로킹의 값과 진짜 비효율이 유휴가 아니라 묶임이라는 지적, 그 묶임이 자바의 진화를 이끈 동인이라는 서술, 의존 없는 호출을 갈라 스레드에 던지는 병렬 실행 전략과 1,026밀리초에서 616밀리초로 줄어든 실측, 그리고 통제 없이 만든 스레드가 자원을 고갈시키는 대가
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 블로킹 I/O와 스레드 효율

- [자원 비효율이 곧 비용이 된 자리](#자원-비효율이-곧-비용이-된-자리)
- [진짜 비효율은 유휴가 아니라 묶임이다](#진짜-비효율은-유휴가-아니라-묶임이다)
- [묶임이 자바의 진화를 이끌었다](#묶임이-자바의-진화를-이끌었다)
- [병렬 실행 전략과 그 실측](#병렬-실행-전략과-그-실측)
- [인터럽트 상태는 되돌려 놓아야 한다](#인터럽트-상태는-되돌려-놓아야-한다)
- [통제 없이 만든 스레드의 대가](#통제-없이-만든-스레드의-대가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드가 바쁘게 메서드를 실행하고 있는데도 아무 일을 못 하고 있는 상태는
무엇이며, 그것을 줄이는 첫 수단은 무엇인가.**

## 자원 비효율이 곧 비용이 된 자리

- 2025년 저술 시점의 애플리케이션은 큰 데이터를 처리하면서 동시에 많은 트래픽을 감당하기를 요구받는다. 클라우드가
  많은 사업의 기본 환경이 된 상황에서 이 요구는 재무 문제가 된다 — 아주 작은 자원 비효율도 빠르게
  불어나는 비용이 된다 (1장, pp.11–12).[^rahman2025]
- 스레드 수가 유한하므로 아껴 써야 하는데, 실제로는 스레드가 막히기 때문에 제대로 쓰이지 못할 때가
  많다 (1장, p.12).[^rahman2025] 그 상한이 어디서 오는지는
  [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)에 있다.

## 진짜 비효율은 유휴가 아니라 묶임이다

- 저자의 예제는 사람의 신용 점수를 계산하는 메서드다. 다섯 번의 메서드 호출이 앞의 것이 끝난 뒤에야
  다음이 시작되는 순서로 놓여 있고, 각각이 200밀리초 걸린다고 하면 전체는 약 1초가 된다 (1장,
  p.12).[^rahman2025]

  ```java
  public Credit calculateCredit(Long personId) {
      var person = getPerson(personId);          // Database call-blocks thread
      var assets = getAssets(person);            // API call-blocks thread
      var liabilities = getLiabilities(person);  // Database call-blocks thread
      importantWork();                           // CPU-intensive work
      return calculateCredits(assets, liabilities);
  }
  ```

- 저자가 강조하는 것은 이 지점이다 — 진짜 비효율은 스레드가 놀고 있다는 것이 아니라 입출력(input/
  output, I/O) 동안 막혀 있다는 것이다. `getPerson`이 데이터베이스를 부르고 네트워크 응답을
  기다리는 동안 그 스레드는 다른 요청을 맡거나 다른 일을 하도록 재배치될 수 없다 (1장,
  p.12).[^rahman2025]
- 그래서 겉보기와 실제가 어긋난다 — 스레드는 기술적으로는 이 메서드들을 실행하느라 바쁘지만, 시간의
  대부분을 계산이 아니라 I/O 대기로 쓴다 (1장, p.12).[^rahman2025]
- 비용의 정체가 여기서 드러난다 — 비싼 스레드 자원이 외부 시스템의 응답을 기다리며 묶여 있고, 그동안
  다른 요청을 처리할 수도 있었다. 처리량이 중요한 애플리케이션에서 막힌 스레드 하나는 들어오는
  요청을 받을 스레드 하나가 줄어든 것이라 확장성을 크게 깎는다 (1장, p.12).[^rahman2025]

## 묶임이 자바의 진화를 이끌었다

- 스레드가 I/O에 막혀 보내는 시간을 줄이려는 노력이 자바의 여러 진화를 이끌어 왔다고 저자는 정리한다.
  그 목록이 셋이다 (1장, p.12).[^rahman2025]
  - 비동기 메서드 호출 — I/O가 끝나는 동안 메서드가 따로 돌게 하는 쪽.
  - 스레드 풀링(thread pooling) — 정해진 수의 스레드를 재사용해 작업을 처리하는 쪽.
  - 그리고 2025년 저술 시점 기준 더 최근의 리액티브 프로그래밍(reactive programming) 모델 — 논블로킹(non-blocking)과
    이벤트 기반 상호작용을 앞세우는 쪽.

## 병렬 실행 전략과 그 실측

- 예제를 다시 보면 서로 의존하지 않는 호출이 셋이다. 자산 조회와 부채 조회와 별개의 계산 작업이
  그것이고, 이 셋은 병렬로 보낼 수 있다. 그러면 주 스레드가 막혀 있는 시간이 줄어든다 — 막힘을
  완전히 없앤 것은 아니다 (1장, p.13).[^rahman2025]
- 이 전략이 노리는 것은 주 스레드의 유휴 시간을 줄이는 것이다. 덜 놀게 되므로 계산 메서드가 끝나면
  곧 다른 일을 할 수 있게 된다 (1장, p.13).[^rahman2025]
- 병렬판은 결과를 담을 자리로 `AtomicReference`를 쓴다. 객체 참조 하나를 담는 스레드 안전한 자료
  구조이고, 여러 스레드를 다루므로 이런 것이 꼭 필요하다 (1장, pp.13–14).[^rahman2025]
  - 저자의 지침은 쓰임새로 갈린다 — 객체 참조를 스레드 사이에서 안전하게 나눌 때
    `AtomicReference`를 쓰고, 원시 값이라면 `AtomicInteger`나 `AtomicLong` 같은 원자적 원시 타입을
    보라 (1장, p.14).[^rahman2025]
- 실측이 나란히 실린다 — 순차판이 1,026밀리초, 병렬판이 616밀리초다. 저자는 새 판이 옛 판보다
  1.66배 빠르다고 적는다 (1장, p.17).[^rahman2025]
  - 저자는 이 측정이 이해를 돕는 단순한 방식임을 밝히고, 견고한 벤치마킹에는 JVM 워밍업과 죽은 코드
    제거 같은 요인을 다루는 마이크로벤치마크 하네스를 쓰라고 덧붙인다. JMH가 그 예다 (1장,
    p.17).[^rahman2025]

## 인터럽트 상태는 되돌려 놓아야 한다

- 예제의 지연 흉내 코드가 `InterruptedException`을 다루는 자리를 저자가 따로 설명한다. 핵심은
  스레드의 인터럽트 상태를 보존하는 것이다 (1장, p.16).[^rahman2025]
- 기제가 세 걸음이다 — `Thread.interrupt()`가 내부 플래그를 세우면 `sleep`이나 `wait`이나 블로킹
  I/O 같은 메서드가 `InterruptedException`을 던진다. 그런데 그 예외를 잡으면 인터럽트 플래그가
  지워지므로, 인터럽트가 있었음을 알아야 하는 호출 스택 위쪽 코드가 곤란해진다 (1장,
  p.16).[^rahman2025]
- 그래서 잡은 자리에서 `Thread.currentThread().interrupt()`로 플래그를 되돌려 놓는다. 그러면
  `Thread.interrupted()`나 `Thread.currentThread().isInterrupted()`를 보는 호출 측이 인터럽트가
  일어났음을 제대로 보게 된다 (1장, p.16).[^rahman2025]
- 그다음 `InterruptedException`을 `RuntimeException`으로 감싸면, `throws` 절에
  `InterruptedException`을 적지 않은 메서드를 지나서도 인터럽트가 호출 스택 위로 전파된다. 검사
  예외를 시그니처에 더할 수 없는 자리에서 특히 쓸모가 있다 (1장, p.16).[^rahman2025]

## 통제 없이 만든 스레드의 대가

- 병렬화가 시작 스레드의 막힘을 줄여 성능을 올리는 것은 맞지만, 스레드 관리와 시스템 자원 활용에서
  나름의 문제를 데려온다 (1장, p.18).[^rahman2025]
- 문제의 이름이 임기응변식 생성이다 — 앞의 예제처럼 그때그때 스레드를 만드는 방식에는 스레드 수명
  주기와 자원 할당을 통제하는 장치가 없다. 스레드가 지나치게 불어나 시스템 자원을 고갈시킬 수 있고,
  스레드 하나하나가 메모리와 처리 능력을 먹는 무거운 자원이다 (1장, p.18).[^rahman2025]
- 그 결과가 `java.lang.OutOfMemoryError`와 크래시와 런타임 병목이다 (1장, p.18).[^rahman2025]
  그래서 다음 답이 [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)다.

## 이어지는 페이지

- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 아껴 써야 하는 이유의 수치
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 임기응변식
  생성을 대신하는 구조
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 막힘 자체를
  다르게 다루는 쪽
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 막힘 문제를
  파이썬 쪽에서 본 자리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 1장 "Introduction" — "Resource Efficiency in High-Scale
    Applications"(pp.11–18), "The Parallel Execution Strategy"(pp.13–18), "Handling
    InterruptedException Correctly"(p.16). 인용한 `calculateCredit`은 원문 그대로이며 주석도
    원문 표기를 유지했다. 병렬판(`calculateCreditWithUnboundedThreads`)과 흉내 메서드들은
    옮기지 않았다 — 원문은 `archive/` 스냅샷이 보존한다.

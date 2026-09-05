---
type: concept
title: 가상 스레드와 ThreadLocal
description: 데이터를 스레드에 가두는 ThreadLocal의 고전적 쓰임 둘과, 가상 스레드가 수백만 개가 되면서 그것이 메모리와 초기화 부담과 상속이라는 세 가지 문제로 바뀌는 자리, 그리고 저자가 제시하는 대안 둘
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드와 ThreadLocal

- [버전 조건](#버전-조건)
- [원래 무엇을 하던 도구인가](#원래-무엇을-하던-도구인가)
- [수백만 개가 되면 문제가 셋](#수백만-개가-되면-문제가-셋)
- [저자의 실측](#저자의-실측)
- [가벼운 공유가 왜 필요한가](#가벼운-공유가-왜-필요한가)
- [대안 둘](#대안-둘)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드마다 값을 하나씩 두던 방식이 스레드가 수백만 개가 되면 어떻게 되는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. `ThreadLocal` 자체는 오래된 도구이고 그 설명은 버전과 무관하지만,
> 아래의 문제 서술은 가상 스레드를 대량으로 쓸 때 생기는 것이다.

## 원래 무엇을 하던 도구인가

- 자바의 `ThreadLocal` 변수는 데이터를 특정 스레드에 가두는 방법을 준다. `ThreadLocal` 클래스로
  그것을 만든 스레드만 읽고 쓸 수 있는 변수를 만들 수 있고, 여러 스레드가 같은 데이터를 동시에
  건드리려 할 수 있는 상황에서 동기화의 필요를 없앤다 (2장, p.71).[^rahman2025] 그 구현 내부
  (`ThreadLocalMap`)는
  [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md)에 있다.
- 고전적 쓰임이 둘이다 (2장, p.71).[^rahman2025]
  - 자원 격리 — 스레드 안전하지 않은 자원을 담아 두는 데 알맞다. 전형적인 예가
    `SimpleDateFormat`으로, 스레드마다 자기 인스턴스를 가져 충돌을 피한다.
  - 암묵적 컨텍스트 — 데이터베이스 연결, 사용자 세션 데이터, 트랜잭션 식별자처럼 스레드가 맡은
    작업에 딸린 맥락 정보를 담는 데도 흔히 쓴다.
- 첫째 예에는 각주가 붙는다 — 자바는 이제 스레드 안전한 `DateTimeFormatter` 클래스를 제공하므로
  이 경우에는 `ThreadLocal`이 필요 없다 (2장, p.71 각주 1).[^rahman2025]

## 수백만 개가 되면 문제가 셋

- 전제가 규모다 — 가상 스레드는 가볍게 설계되어 한 애플리케이션 안에서 수백만 개를 돌릴 수 있고,
  그 엄청난 규모가 `ThreadLocal` 변수를 과하게 쓸 때 문제를 만든다 (2장, p.71).[^rahman2025]
- 메모리 소비 — 가상 스레드마다 `ThreadLocal` 변수의 복사본을 하나씩 가지면 메모리 사용량이 빠르게
  늘 수 있고, 담긴 데이터가 크면 특히 그렇다 (2장, p.71).[^rahman2025]
- 부담 — `ThreadLocal` 변수를 초기화하고 정리하는 데 부담이 따른다. 가상 스레드의 수가 막대하면
  이 동작들이 성능 부담이 될 수 있다 (2장, p.71).[^rahman2025]
- 상속 — 가상 스레드는 전통적인 스레드처럼 부모 스레드에서 `ThreadLocal` 값을 물려받는다. 이
  상속이 추적하고 디버깅하기 어려운 미묘한 버그를 들일 수 있다 (2장, p.72).[^rahman2025]

## 저자의 실측

- 실험이 단순하다 — 500KB짜리 객체를 `ThreadLocal`에 담고 가상 스레드 1,000개가 저마다 자기
  복사본을 갖게 한 뒤, JConsole로 힙 메모리 사용량을 본다 (2장, pp.72–73).[^rahman2025]

  ```java
  public class ThreadLocalExample {

      public static void main(String[] args) {
          ThreadLocal<LargeObject> threadLocal =
              ThreadLocal.withInitial(LargeObject::new);

          var threadList = IntStream.range(0, 1000)
              .mapToObj(i -> Thread.ofVirtual().unstarted(() -> {
                  LargeObject largeObject = threadLocal.get();
                  useIt(largeObject);
                  sleep();
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

      static class LargeObject {
          private byte[] data = new byte[1024 * 500];   // 500 KB
      }
  }
  ```

- 관측 결과가 대비로 나온다 — `ThreadLocal`을 쓰면 메모리 사용량이 누적되는 것이 드러나고,
  `ThreadLocal` 없이 같은 프로그램을 돌리면 가상 스레드가 1,000개나 관여함에도 메모리 사용량이
  곧바로 떨어진다 (2장, p.73).[^rahman2025]

## 가벼운 공유가 왜 필요한가

- 같은 책이 5장에서 이 한계를 다시 세우며 규모의 대비를 명시한다 — `ThreadLocal`의 한계는 가상
  스레드(JEP 444)가 도입되면서 더욱 뚜렷해진다. 스레드마다 전용 운영 체제 자원을 갖는 전통적인
  플랫폼 스레드와 달리, 가상 스레드는 운영 체제 스레드 하나가 수천 개, 심지어 수백만 개의 경량
  스레드를 태울 수 있다 (5장, p.225).[^rahman2025]
- 가능하다는 것과 감당된다는 것이 다르다 — 가상 스레드마다 자기 `ThreadLocal` 데이터를 갖는 것이
  기술적으로 가능하기는 하지만 메모리 부담이 금세 감당할 수 없는 수준이 된다 (5장,
  p.225).[^rahman2025]
- 수명 쪽 문제는 오히려 덜하다 — 가상 스레드는 수명이 짧으므로 오래 사는 스레드 로컬 변수의 문제는
  덜 심각하다. 가비지 컬렉션이 치워 주기 때문이다. 그래도 그만큼 많은 복제가 만드는 메모리 부담은
  남는다 (5장, p.225).[^rahman2025]
- 저자가 필요한 기제의 조건을 여기서 세운다 (5장, p.225).[^rahman2025]
  - 복제를 여럿 만들지 않고도 상속 가능한, 스레드별 데이터를 저장할 수 있어야 한다.
  - 데이터가 불변이면 더 좋다. 공유되는 한 벌을 자식 스레드들이 참조하면 되므로 중복이 더 생기지
    않는다.
  - 이 데이터에는 유한한 수명이 있어야 한다. 데이터를 나누던 메서드가 끝나면 딸린 스레드 로컬은
    의미를 잃어야 한다. 그것들은 태스크가 도는 동안 상태를 담아 두는 편한 자리이지 메모리를
    영구히 쌓아 두는 곳이 아니기 때문이다.
- 이 세 조건이 그대로 `ScopedValue`의 성질이 된다. 저자가 그 지점에서 새 API를 꺼낸다 (5장,
  p.225).[^rahman2025] 그 API의 전반은
  [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md)에 있다.

## 대안 둘

- 스코프 값(scoped values) — 가상 스레드를 염두에 두고 설계되었고, 불변성과 한정된 수명 덕분에
  스레드 사이로 데이터를 안전하고 효율적으로 넘기는 데 알맞다 (2장, p.73).[^rahman2025]
- 공유 자체를 다시 생각하기 — 가상 스레드의 등장이 데이터 공유에 대한 전반적인 접근을 다시 살펴볼
  계기가 된다. `ThreadLocal`의 필요 자체를 최소화하도록 애플리케이션을 재구성할 수 있는지 살펴
  보라는 것이고, 그것이 더 잘 확장되는 설계로 이어질 수 있다 (2장, p.73).[^rahman2025] 같은
  결의 조언이 [공유 상태는 잘못된 상태다](../concepts/shared-state-is-incorrect-state.md)에 있다.
- 캐리어 쪽 격리는 이미 되어 있다 — 캐리어 스레드의 `ThreadLocal` 값은 가상 스레드에게 보이지
  않는다는 것이
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)에
  있다. 여기서 문제가 되는 것은 가상 스레드 자신의 값들이다.

## 이어지는 페이지

- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 규모와 무관하게 이 API 자체가
  갖는 결함들
- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md) — 이 도구가
  실제로 가장 많이 쓰이는 자리
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 위 세 조건에 답하는 API
- [ScopedValue가 ThreadLocal보다 나은 이유](../concepts/scoped-value-vs-thread-local.md) — 두 도구를 나란히
  놓고 견준 자리
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — `ThreadLocal`의 구현
  내부와 그것이 놓인 갈래
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 어디서 쓰이는지 실제로
  찾아내는 도구
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 캐리어 쪽 값이 보이지 않는 이유
- [공유 상태는 잘못된 상태다](../concepts/shared-state-is-incorrect-state.md) — 공유 자체를
  줄이라는 같은 결의 조언
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 이 한계가
  이전 계획에서 놓이는 자리
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "The Conundrum of ThreadLocal
    Variables in Virtual Threads"(pp.71–73), "Challenges with Virtual Threads"(pp.71–72);
    5장 "Scoped Values" — §"Toward Lightweight Sharing"(p.225). 5장 절에는 코드가 실려 있지
    않다.
    그림 2-3과 2-4(JConsole 힙 메모리 사용량 화면 두 장, pp.73–74)는 옮기지 않았고 저자가 본문에
    서술한 대비만 담았다. 인용한 코드에서 임포트 목록과 흉내 메서드 `useIt`·`sleep`(p.72)은
    덜어 냈다.

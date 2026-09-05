---
type: concept
title: fork 시점의 시작 통제
description: onFork가 서브태스크를 돌릴 스레드가 만들어지기 전에 불린다는 성질을 써서 시작 자체를 통제하는 두 조이너 — 퍼밋으로 동시 실행 개수를 묶는 쪽과 바깥 조건이 거짓이 되면 새 태스크를 아예 시작시키지 않는 쪽, 그리고 이미 도는 태스크는 끝까지 두는 두 조이너의 공통 성질
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# fork 시점의 시작 통제

- [버전 조건](#버전-조건)
- [시작을 막는 자리](#시작을-막는-자리)
- [퍼밋으로 동시 실행 개수를 묶기](#퍼밋으로-동시-실행-개수를-묶기)
- [배치 API 호출이라는 실물](#배치-api-호출이라는-실물)
- [바깥 조건이 거짓이면 새 태스크를 막기](#바깥-조건이-거짓이면-새-태스크를-막기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **서브태스크가 시작되기 전에 그것을 막거나 늦추려면 조이너의 어디에 손을 대는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 인터페이스와 메서드 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 시작을 막는 자리

- `onFork`는 서브태스크(subtask)가 갈라질 때마다, **그것을 돌릴 스레드가 만들어지기 전에** 불린다
  ([커스텀 조이너의 계약](../concepts/custom-joiner-contract.md)). 그래서 이 훅은 결과를 보는
  자리가 아니라 **시작을 보는 자리**다.
- 이 페이지의 두 조이너가 그 자리를 쓰는 방식이 갈린다 — 하나는 시작을 **늦추고**(퍼밋을 얻을
  때까지 기다린다), 하나는 시작을 **막는다**(스코프를 취소해 새 작업이 들어오지 못하게 한다).
  둘 다 이미 돌고 있는 태스크는 끝까지 두는 쪽을 고른다.

## 퍼밋으로 동시 실행 개수를 묶기

- 외부 서비스를 압도하지 않으려면 서브태스크가 실행되는 속도를 통제해야 할 때가 있다. 저자는
  `Semaphore`로 속도 제한을 구현한 조이너를 만든다 (4장 §"Rate-limited joiner",
  p.196).[^rahman2025]

  ```java
  public class RateLimitedJoiner<T> implements StructuredTaskScope.Joiner<T, List<T>> {

    private final Semaphore semaphore;
    private final Queue<T> results = new ConcurrentLinkedQueue<>();
    private final Queue<Throwable> failures = new ConcurrentLinkedQueue<>();

    public RateLimitedJoiner(int maxConcurrentTasks) {
      this.semaphore = new Semaphore(maxConcurrentTasks);
    }

    @Override
    public boolean onFork(StructuredTaskScope.Subtask<? extends T> subtask) {
      try {
        semaphore.acquire();
      } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
      }
      return false;
    }

    @Override
    public boolean onComplete(StructuredTaskScope.Subtask<? extends T> subtask) {
      switch (subtask.state()) {
        case SUCCESS -> results.add(subtask.get());
        case FAILED -> failures.add(subtask.exception());
        case UNAVAILABLE -> failures.add(new RuntimeException("Task canceled"));
      }
      semaphore.release();
      return false;
    }

    @Override
    public List<T> result() {
      return results.stream().toList();
    }
  }
  ```

- 저자가 이 조이너에서 짚는 것이 여럿이다 (4장, p.197):[^rahman2025]
  - 세마포어(Semaphore)가 허용되는 동시 실행 개수를 통제하고, 그 최대치로 만들어진다.
  - `onFork`가 태스크 실행 전에 퍼밋(permit)을 얻는다. **퍼밋이 없으면 이 호출이 하나 생길 때까지
    막히고**, 그것이 곧 태스크 실행 속도를 통제하는 방식이다.
  - 퍼밋을 얻은 뒤 `false`를 돌려 서브태스크가 만들어져 실행을 시작하게 한다.
  - `onComplete`는 성공 결과와 실패를 각각 모으고, **성공이든 실패든 언제나** 퍼밋을 반환해 기다리는
    다른 태스크가 쓸 수 있게 한다.
  - 끝에서 `false`를 돌려 일찍 멈추지 않고 모든 태스크가 끝나게 둔다.
- 퍼밋이 스레드에 묶이지 않는 셈법이라는 것과 그 함정은
  [자바 세마포어와 퍼밋](../concepts/java-semaphore-permits.md)에 있다.
- #hypothesis 이 `acquire()`가 막는 것은 스코프 소유자 스레드다. `fork()`를 부르는 것이 스코프
  소유자이고 `onFork`가 그 `fork()` 안에서 스레드가 만들어지기 전에 불리므로, 퍼밋이 없는 동안
  갈라 놓는 반복문 자체가 멈춘다는 뜻이 된다. 저자는 이 점을 말하지 않는다 — 두 근거는 각각 4장
  p.138(갈라 놓는 주체가 스코프 소유자)과 p.185(`onFork`가 스레드 생성 전에 불림)에 있다.

## 배치 API 호출이라는 실물

- 저자가 꾸민 상황은 끝점 여섯 개를 부르되 동시 실행은 최대 셋으로 묶는 것이다 (4장,
  p.197).[^rahman2025]
- 짚는 것이 둘이다 — `fork()` 호출마다 태스크가 실행을 시작하기 전에 퍼밋을 얻으므로 셋만 동시에
  돌고, `join()`은 세마포어가 동시 실행을 알아서 관리하는 동안 모든 호출이 끝나기를 기다린다
  (4장, p.198).[^rahman2025]
- 실행 출력에서 그 성질이 드러난다 — 처음 셋이 함께 시작하고, 하나가 끝날 때마다 다음 것이
  시작된다 (4장, pp.198–199).[^rahman2025]

## 바깥 조건이 거짓이면 새 태스크를 막기

- 둘째 조이너는 `onFork`를 실행 시점의 상태에 따른 조건부 실행에 쓴다. 새 태스크를 언제 멈출지에
  대한 어떤 조건이든 받아들이는 일반 조이너다 (4장 §"Conditional joiners", p.199).[^rahman2025]
- 받는 것은 `Supplier<Boolean> shouldContinue` 하나다. `onFork`가 새 태스크가 시작하려 할 때마다
  그 조건을 검사하고, 거짓이면 `true`를 돌려 **스코프를 취소해 새 작업이 시작되지 못하게 막는다.**
  참이면 `false`를 돌려 태스크를 통과시킨다 (4장, pp.199–200).[^rahman2025]
- `onComplete`는 상태별로 결과와 실패를 모은 뒤 `false`를 돌린다 — **이미 돌고 있는 태스크는 끝까지
  돌게 둔다**는 뜻이다 (4장, p.200).[^rahman2025]
- 실물 쓰임은 바깥 시스템의 건강 상태를 검사해 의존 대상을 쓸 수 없게 되면 멈추는 것이다. 저자의
  예제는 태스크 열 개를 갈라 놓는데, 건강 검사기가 자기가 불린 횟수를 세다가 일곱 번째부터 거짓을
  돌려준다 (4장, pp.200–201).[^rahman2025]

## 이어지는 페이지

- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — 이 두 조이너가 지키는 계약
- [결과를 보고 일찍 끝내는 커스텀 조이너](../concepts/early-completion-custom-joiners.md) —
  같은 `boolean`을 `onComplete`에서 쓰는 쪽
- [자바 세마포어와 퍼밋](../concepts/java-semaphore-permits.md) — 퍼밋을 세는 원리와 회계 함정
- [가상 스레드 시대의 속도 제한](../concepts/rate-limiting-with-virtual-threads.md) — 같은
  문제를 스코프 밖에서 푸는 방식
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — `onFork`가
  꽂히는 절차
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" §"Custom Joiners" —
    "Rate-limited joiner"(pp.196–199), "Conditional joiners"(pp.199–201). 인용한 코드는
    pp.196–197의 `RateLimitedJoiner`이고 조판 줄바꿈만 폈다. 개념당 대표 코드 하나 규칙에 따라
    남긴 것: `RateLimitedAPIService` 전문과 실행 출력(pp.197–199), `ConditionalJoiner`
    전문과 `getFailures` 접근자(pp.199–200), `SystemHealthCheckDemo`와
    `SystemHealthChecker`(pp.200–201).

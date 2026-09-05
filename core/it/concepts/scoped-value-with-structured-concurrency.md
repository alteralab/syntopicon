---
type: concept
title: 구조적 동시성에서의 스코프 값 상속
description: 새 스레드는 스코프 값을 물려받지 않는다는 규칙이 StructuredTaskScope 안에서만 뒤집히는 자리 — 스코프 안에서 만들어진 자식 스레드가 바인딩을 자동으로 물려받는다는 것과, 저자가 그것이 안전한 근거로 드는 스코프의 경계
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 동시성에서의 스코프 값 상속

- [버전 조건](#버전-조건)
- [예외가 되는 자리](#예외가-되는-자리)
- [왜 누수 걱정이 없는가](#왜-누수-걱정이-없는가)
- [저자의 예제](#저자의-예제)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **서브태스크는 바깥 스코프에 묶인 값을 물려받는가.**

## 버전 조건

> **버전 조건**: `ScopedValue`는 JDK 25 이상에서 정식 API이고 JDK 21부터 24까지는 미리
> 보기(preview)다 (5장, pp.217·226).[^rahman2025] 그러나 이 페이지가 쓰는 `StructuredTaskScope`
> 쪽은 이 소스 기준으로 JDK 25에서도 미리 보기라 `--enable-preview`가 필요하다 (4장,
> p.136).[^rahman2025] 그래서 이 페이지에만 만료일(`stale_after`)을 달았다 — 두 API가 서로 다른
> 단계에 있고, 아래 서술이 기대는 `StructuredTaskScope`의 이름과 모양은 정식화될 때 바뀔 수
> 있다. 재심 시점은 이 책 다음 릴리스인 JDK 26(2026년 3월)이다.

## 예외가 되는 자리

- 앞의 규칙이 먼저 확인된다 —
  [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md)에서 본 대로 `ScopedValue`는
  자식 스레드에 상속되지 않는다 (5장 §"ScopedValue and Structured Concurrency",
  p.235).[^rahman2025]
- 그런데 한 자리에서 뒤집힌다 — `StructuredTaskScope` 안에서 쓰면 그 스코프 안에서 만들어진 모든
  자식 스레드가 `ScopedValue` 바인딩을 **자동으로 물려받는다** (5장, p.235).[^rahman2025]
- 저자가 설계 의도를 밝힌다 — `ScopedValue`는 구조적 동시성과 매끄럽게 어울리도록 설계되었다
  (5장, p.235).[^rahman2025]
- 이득이 명시된다 — 이 상속 기제가 부모와 자식 스레드 사이의 효율적인 데이터 공유를 돕고, 데이터를
  인자로 명시적으로 넘기지 않아도 되게 한다 (5장, p.235).[^rahman2025]

## 왜 누수 걱정이 없는가

- 근거가 경계에 있다 — 구조적 동시성은 잘 정의된 경계를 갖기 때문이다 (5장,
  p.235).[^rahman2025]
- 그 경계에서 무엇이 일어나는지가 이어진다 — `StructuredTaskScope`를 빠져나가면 그 스코프 안에서
  만들어진 모든 스레드가 인터럽트되고 가비지 컬렉션되므로 메모리 누수 문제가 없다 (5장,
  p.235).[^rahman2025]
- 이것이 두 기능이 서로를 보강하는 자리다.
  [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md)에서 상속이 비쌌던 이유가 값이
  어디까지 살아 있는지 아무도 모른다는 데 있었는데, 스코프가 그 끝을 정해 준다.

## 저자의 예제

- 메인 스레드에서 사용자 이름을 묶고, 그 안에서 연 스코프가 서브태스크 둘을 포크하면 둘 다 그 값을
  읽는다 (5장, p.235).[^rahman2025]

  ```java
  public static void main(String[] args) {
      ScopedValue.where(USERNAME, "Bazlur").run(() -> {
          doSomething();
      });
  }

  public static void doSomething() {
      try (var scope = StructuredTaskScope.open()) {
          StructuredTaskScope.Subtask<String> task1 =
              scope.fork(() -> USERNAME.get() + " from task 1");
          StructuredTaskScope.Subtask<String> task2 =
              scope.fork(() -> USERNAME.get() + " from task 2");
          scope.join();
          System.out.println(task1.get());
          System.out.println(task2.get());
      } catch (InterruptedException e) {
          throw new RuntimeException(e);
      }
  }
  ```

- 저자가 예제를 풀어 쓴 문장이 관계를 정리한다 — `doSomething()`이 불리면 스코프를 만들어 자식
  스레드 둘을 포크하고, 이 자식 스레드들이 부모 스레드에서 `USERNAME` 바인딩을 물려받아
  `get()`으로 읽는다 (5장, p.235).[^rahman2025]
- `fork`와 `join`이 세우는 메모리 보장은 별도로 있다 —
  [구조적 스코프의 메모리 일관성 효과](../concepts/structured-scope-memory-consistency.md)가 그것을 담는다.
  값이 보인다는 것과 그 값이 최신이라는 것은 다른 문제이고, 여기서 옮긴 것은 앞쪽이다.

## 이어지는 페이지

- [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md) — 이 상속이 예외가 되는 그 규칙
- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — `open`과 `fork`와 `join`의 계약
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 자식 스레드가 언제 뜨고
  언제 정리되는가
- [중첩 스코프](../concepts/nested-structured-scopes.md) — 스코프 안에 스코프를 열었을 때의 위계
- [구조적 스코프의 메모리 일관성 효과](../concepts/structured-scope-memory-consistency.md) — 물려받은 값의
  가시성이 기대는 규칙
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 바인딩을 만드는 쪽
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"ScopedValue and Structured
    Concurrency"(p.235). 버전 조건의 근거는 5장 도입부(p.217)와 곁글(p.226), 그리고
    `StructuredTaskScope` 쪽은 4장 §"Understanding the API"(p.136). 인용한 코드에서 임포트와
    클래스 선언과 `USERNAME` 필드 선언, 그리고 결과를 지역 변수로 받는 두 줄은 덜어 냈다.

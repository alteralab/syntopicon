---
type: concept
title: ScopedValue의 구성 요소와 API
description: 암묵적 메서드 매개변수로 동작하는 ScopedValue의 세 가지 성질(불변성, 스레드 한정 바인딩, 유한한 수명)과 선언하는 법, where로 묶고 run이나 call로 실행하는 두 결말, 바인딩을 이어 붙이는 체인, 그리고 값을 읽는 네 가지 방법
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ScopedValue의 구성 요소와 API

- [버전 조건](#버전-조건)
- [무엇으로 동작하는가](#무엇으로-동작하는가)
- [세 가지 성질](#세-가지-성질)
- [선언하는 법](#선언하는-법)
- [묶고 실행하기](#묶고-실행하기)
- [값을 읽는 네 가지 방법](#값을-읽는-네-가지-방법)
- [문맥 전달 예제를 다시 쓰면](#문맥-전달-예제를-다시-쓰면)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`ScopedValue`는 무엇이고 값을 어떻게 묶고 읽는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다. 저자가 5장을 여는 문장이 그 경계를 적는다 —
> `ScopedValue`는 **"finalized in JDK 25"**이고 (5장, p.217), 같은 장이 **"available since
> JDK 25"**라고 다시 적으며 더 낮은 JDK에서는 플래그로 켤 수 있다고 덧붙인다 (5장,
> p.226).[^rahman2025] 그래서 이 페이지에는 만료일(`stale_after`)을 달지 않는다. 정식 API의
> 모양은 다음 릴리스가 온다고 바뀌지 않으므로 재심 시점을 미리 잡을 근거가 없다.

- JDK 24에서 쓰려면 저자가 명령을 직접 적어 준다 (5장, p.226).[^rahman2025]

  ```sh
  javac --release 24 --enable-preview Main.java
  java --enable-preview Main
  ```

## 무엇으로 동작하는가

- 정의가 한 문장이다 — `ScopedValue`는 **암묵적 메서드 매개변수(implicit method parameter)**처럼
  동작해, 각 메서드의 시그니처에 명시적으로 선언하지 않고도 일련의 메서드 호출을 거쳐 데이터를
  넘길 수 있게 한다 (5장 §"Core Components of ScopedValue", p.225).[^rahman2025]
- 이득이 어디서 큰지도 지목된다 — 깊이 중첩된 메서드 호출이나 콜백 구조를 다룰 때 코드가 더
  깔끔하고 유지보수하기 쉬워진다 (5장, p.225).[^rahman2025]

## 세 가지 성질

저자가 주요 특징을 셋으로 센다 (5장, p.226).[^rahman2025]

- 불변성(immutability) — `ScopedValue`가 특정 스코프 안에서 어떤 값에 묶이고 나면 그 값은 바꿀
  수 없고, 그래서 살아 있는 동안 일관되고 예측 가능한 동작이 보장된다.
- 스레드 한정 바인딩(thread-scoped binding) — 바인딩은 현재 스레드에 한정되어, 스레드 사이의
  의도치 않은 데이터 공유를 막고 스레드 안전성을 높인다.
- 유한한 수명(bounded lifetime) — 바인딩은 특정 코드 블록의 실행 기간으로 한정되고 그 뒤에는
  풀린다. 자원 관리에 도움이 되고 메모리 누수 위험을 줄인다.

이 셋이 각각
[ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md)의 무제한 가변성과 무제한 수명에
정면으로 대응한다.

## 선언하는 법

- 스코프 값을 쓰려면 먼저 정적 `final` 필드로 선언한다. 선언하는 모양은 `ThreadLocal`을 선언할
  때와 같다 — `private static final ScopedValue<String> NAME = ScopedValue.newInstance();`
  (5장, p.226).[^rahman2025]
- 생성 방법에 제약이 있다 — `new` 연산자를 쓰지 않고 팩토리 메서드를 쓴다. 생성자가 의도적으로
  `private`으로 되어 있기 때문이다 (5장, p.226).[^rahman2025]

## 묶고 실행하기

- 값을 묶고 그 스코프 안에서 코드를 실행하는 일은 `where()`와 `run()` 두 메서드로 이룬다.
  `where()`가 스코프 값을 어떤 값에 결합하고, `run()`이 그 결합된 값의 스코프 안에서 주어진 코드
  블록을 실행한다 (5장, pp.226–227).[^rahman2025]
- 결말이 둘이다 — 스코프 안의 실행에서 값을 돌려받아야 할 때를 위해 `call()`도 있다. 차이는
  단순하다. `run()`은 `Runnable`을 실행해 `void`이고, `call()`은 `Callable`을 실행해 값을
  반환한다 (5장, p.228).[^rahman2025]
- `call()`이 알맞은 자리도 적혀 있다 — 계산이나 변환처럼, 스코프 문맥에 접근한 채로 결과를
  돌려받아야 하는 연산이다 (5장, p.228).[^rahman2025]
- 바인딩은 이어 붙일 수 있다 — `ScopedValue`가 유창한 API를 제공하므로 여러 `ScopedValue`를
  체인으로 묶을 수 있다. `where()`로 첫 값을 묶고 다시 `where()`로 다음 값을 이어 붙인 뒤
  `run()`으로 실행하면, 두 값 모두 호출 스택 전체에서 읽을 수 있다 (5장,
  pp.232).[^rahman2025]

## 값을 읽는 네 가지 방법

- `run()`이나 `call()` 안의 코드는 `get()`으로 스코프 값을 읽는다 (5장, p.227).[^rahman2025]
- 바인딩이 없을 때를 위해 `orElse`와 `orElseThrow` 둘이 더 있다. 값이 없을 때 기본값을 쓰고
  싶거나 예외를 던지고 싶을 때 쓸모 있다 (5장, p.232).[^rahman2025]
- 저자가 두 메서드의 동작을 넷으로 정리한다 (5장, p.232).[^rahman2025]
  - 바인딩이 없을 때 기본값으로 안전하게 접근하게 해 준다.
  - 바인딩이 없을 때 사용자 정의 예외를 던지는 검증을 가능하게 한다.
  - 바인딩된 값이 있으면 기본값을 무시하고 그 값을 돌려준다.
  - 값이 있다고 확신할 때는 인자 없는 판을 쓸 수 있다.
- 저자가 이 설계의 뜻을 밝힌다 — 이 API 설계가 코드로 하여금 바인딩된 상태와 바인딩되지 않은
  상태를 모두 무리 없이 다루게 하고, 그래서 스코프 값이 여러 쓰임에서 견고해진다 (5장,
  p.232).[^rahman2025]
- 넷째 방법이 `isBound()`다. 그것으로 무엇을 하는지는
  [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md)에 있다.

## 문맥 전달 예제를 다시 쓰면

- 앞의 `JobScheduler`를 `ScopedValue`로 갈아 끼우면 이렇게 된다 (5장, p.227).[^rahman2025]

  ```java
  private static final ScopedValue<JobContext> CONTEXT = ScopedValue.newInstance();

  public void schedule(Job job, String jobName, Priority priority) {
      JobContext context = new JobContext(jobName, priority);
      ScopedValue.where(CONTEXT, context)
                 .run(() -> runJob(job));
  }

  public static JobContext getContext() {
      return CONTEXT.get();
  }
  ```

- 저자가 이 구현에서 짚는 것 가운데 하나가 접근 방식의 개선이다 — 현재 문맥에 대한 정적 접근을
  제공하며, 그것이 원래 방식보다 깔끔하다 (5장, p.227).[^rahman2025]
- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md)의 판과
  견주면 `try`와 `finally`로 손수 제거하던 자리가 사라진다. 수명이 `run()`의 경계로 옮겨
  갔기 때문이다.

## 이어지는 페이지

- [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md) — `run()`이 여는 스코프가 정확히
  어디까지인가
- [중첩 스코프에서의 리바인딩](../concepts/scoped-value-rebinding.md) — 같은 값에 안쪽에서 다른 값을 주는 법
- [ScopedValue가 ThreadLocal보다 나은 이유](../concepts/scoped-value-vs-thread-local.md) — 이 API 모양이
  낳는 성능과 사용성의 차이
- [문맥을 넘겨 다니는 부담](../concepts/context-passing-burden.md) — 이 API가 답하는 문제
- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md) — 이 API가
  대신하려는 앞선 방법
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 책의 예제 코드가 쓰는 JDK 25
  문법
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — 장 도입부(p.217), §"Core Components of
    ScopedValue"(pp.225–228), 그리고 같은 절의 뒷부분인 체인과 기본값 항목(p.232).
    개념당 대표 코드 하나 규칙에 따라 `ScopedValue`로 다시 쓴 `JobScheduler`만 실었고,
    `PricingService`의 `call()` 예제(p.228), `MultiScopedExample` 전문(p.232),
    `ScopedValueDefaultsExample` 전문(pp.232–233)은 미수록이다 — 각 예제가 보이는 동작은
    본문에 옮겼다. 인용한 `JobScheduler`에서 `getJobMetadata`와 `runJob`은 덜어 냈다.
    버전 조건 절의 명령 펜스는 p.226 곁글의 네 줄 가운데 `javac`와 `java` 둘만 옮긴 것이고,
    소스 코드 런처와 JShell 판은 미수록이다.

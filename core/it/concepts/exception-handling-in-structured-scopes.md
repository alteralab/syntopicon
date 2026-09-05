---
type: concept
title: 구조적 스코프의 예외 처리
description: 서브태스크가 실패했을 때 join이 FailedException으로 감싸 던진다는 규칙과 그 원인이 가장 먼저 실패한 서브태스크의 것이라는 것, 그 예외를 어디서 다룰지의 네 가지 전략(그 자리에서 잡기·패턴 매칭으로 갈래 짓기·상위로 전파시키기·서브태스크 안에서 기본값으로 바꾸기), 그리고 조이너를 무엇으로 고르느냐에 따라 예외가 아예 나오지 않기도 한다는 갈림
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 스코프의 예외 처리

- [버전 조건](#버전-조건)
- [예외는 어디서 오는가](#예외는-어디서-오는가)
- [전략 하나 — 그 자리에서 잡기](#전략-하나--그-자리에서-잡기)
- [전략 둘 — 패턴 매칭으로 갈래 짓기](#전략-둘--패턴-매칭으로-갈래-짓기)
- [전략 셋 — 상위로 전파시키기](#전략-셋--상위로-전파시키기)
- [전략 넷 — 서브태스크 안에서 기본값으로 바꾸기](#전략-넷--서브태스크-안에서-기본값으로-바꾸기)
- [조이너가 예외의 유무를 가른다](#조이너가-예외의-유무를-가른다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프 안의 서브태스크가 실패했을 때 그 예외를 어디서 어떻게 다루는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 예외 타입 이름과 팩토리 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기
> 기능이라 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심
> 시점으로 잡은 것이다.

## 예외는 어디서 오는가

- 구조적 동시성의 예외 처리는 **쓰고 있는 조이너(Joiner) 정책에 따라 달라지는 정해진 패턴을**
  따른다. 스코프는 서브태스크(subtask)의 완료를 관리하고 `join()`의 결말을 만드는 조이너와 함께
  시작되는데, 그 결말이 어떤 때는 결과이고 어떤 때는 예외다 (4장 §"Exception Handling in
  StructuredTaskScope", p.166).[^rahman2025]
- 결말이 예외일 때 `join()`은 원래 예외를 원인으로 하는 `StructuredTaskScope.FailedException`을
  던진다. 많은 조이너 구현에서 그 예외는 실패한 서브태스크의 것이고,
  `allSuccessfulOrThrow()`와 `awaitAllSuccessfulOrThrow()`의 경우 **가장 먼저 실패한
  서브태스크**의 예외다 (4장, p.166).[^rahman2025] 그 두 정책은
  [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md)에 있다.
- 어디서 다룰지는 쓰임에 달렸다 — try-with-resources 문에 `FailedException`을 잡는 catch 블록을
  붙이는 것이 이로울 때가 있고, 중앙에서 오류를 다루도록 상위 계층까지 전파시키는 편이 나을 때가
  있다 (4장, p.166).[^rahman2025]

## 전략 하나 — 그 자리에서 잡기

- 가장 흔한 형태는 구조적 동시성 코드를 `FailedException`을 다루는 try-catch로 감싸는 것이다.
  그러면 바탕 원인을 살펴보고 무엇으로 응답할지 정할 수 있다 (4장 §"Basic exception handling",
  p.166).[^rahman2025]
- 저자가 드는 상황은 여러 소스에서 사용자 정보를 가져오는 서비스다. 어느 소스든 실패하면 내부
  시스템의 세부를 드러내는 대신 뜻이 통하는 오류 문구를 주고 싶다 (4장, p.166).[^rahman2025]

  ```java
  public String fetchUserData(String userId) {
    try (var scope = open(Joiner.<String>allSuccessfulOrThrow())) {
      var profileTask = scope.fork(() -> fetchUserProfile(userId));
      var preferencesTask = scope.fork(() -> fetchUserPreferences(userId));

      var results = scope.join();

      return results.map(Subtask::get)
          .collect(Collectors.joining(", "));
    } catch (FailedException e) {
      log("Task failed: " + e.getCause().getMessage());
      return "Error: Unable to fetch user data";
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt();
      throw new RuntimeException("Operation interrupted", e);
    }
  }
  ```

- 저자가 이 코드에서 짚는 것이 셋이다 — `allSuccessfulOrThrow()` 조이너가 서브태스크 하나라도
  실패하면 연산 전체를 `FailedException`으로 실패시키고, `getCause()`가 그 안에 감싸인 원래 예외에
  닿게 하며, `InterruptedException`을 다룰 때는 **언제나 인터럽트 상태를 되살린다** (4장,
  p.167).[^rahman2025]
- 이 예제가 `allSuccessfulOrThrow()`를 고른 이유가 명시된다 — 뜻이 통하는 데이터를 주려면 프로필과
  환경 설정이 둘 다 필요하므로 어느 쪽이 실패하든 연산 전체가 실패해야 한다. 다만 기술적 세부 대신
  사용자가 읽을 만한 오류 문구를 내보이고 싶은 것이다 (4장, p.167).[^rahman2025]

## 전략 둘 — 패턴 매칭으로 갈래 짓기

- 예외 타입마다 다른 복구 전략이 필요할 때 패턴 매칭(pattern matching)이 답이 된다. 실패의 종류에
  맞춰 응답을 맞출 수 있다 (4장 §"Pattern matching for sophisticated error handling",
  p.168).[^rahman2025]
- 저자가 꾸민 상황은 주문 처리다. 결제·재고 확인·배송비 계산 셋이 모두 성공해야 하고 각각 다른
  방식으로 실패할 수 있는데, 무엇이 잘못되었는지 고객이 알 수 있도록 구체적이고 행동 가능한
  안내를 주려 한다 (4장, p.168).[^rahman2025]
- 방법은 `FailedException`에서 꺼낸 원인을 `switch` 식의 대상으로 삼는 것이다. 실패 갈래마다
  `case`가 하나씩이고 `default`가 예상 밖의 예외를 일반적인 시스템 오류 문구로 받는다 (4장,
  pp.168–170).[^rahman2025]
- 이 방식이 서려면 예외 타입을 먼저 만들어야 한다 — 저자는 결제 거절·재고 부족·배송 불가·네트워크
  오류를 각각 별도 예외 클래스로 선언한다 (4장, p.171).[^rahman2025]
- 그리고 그것을 모범 사례로 명시한다 — **기술적 실패가 아니라 업무 시나리오를 나타내는 도메인
  전용 예외 타입을 만드는 것**이 좋은 관행이고, 그래야 오류 처리가 뜻을 갖고 코드가 오래
  유지된다 (4장, p.172 안내 상자).[^rahman2025]

## 전략 셋 — 상위로 전파시키기

- 때로는 예외를 더 넓은 맥락에서 다룰 수 있는 상위 계층까지 올려 보내는 것이 최선이다. 계층마다
  책임이 다른 애플리케이션을 지을 때 특히 그렇다 (4장 §"Strategic exception propagation",
  p.172).[^rahman2025]
- 방법이 둘이다 — 메서드 시그니처에 `FailedException`과 `InterruptedException`을 함께
  `throws`로 선언해 호출자가 반드시 다루도록 알리고, catch 블록을 **일부러 두지 않아** 예외가 호출
  스택을 타고 올라가게 둔다 (4장, p.173).[^rahman2025]
- 그러면 상위 메서드가 중앙 집중식 예외 처리를 맡는다 — 로그 남기기, 경보 울리기, 대체 절차
  실행 같은 포괄적 오류 대응을 한 자리에서 구현할 수 있다 (4장, pp.173–174).[^rahman2025]
- 저자의 규칙은 맥락의 유무다 — **하위 메서드에 실패를 알맞게 다룰 만큼의 맥락이 없을 때**
  전파를 쓴다. 복구 전략을 알고 판단할 수 있는 구성 요소까지 예외가 떠오르게 둔다 (4장,
  p.174).[^rahman2025]
- 검사 예외(checked exception)를 전파할 때는 중간 계층도 시그니처에 던지는 예외를 제대로
  선언해야 컴파일 시점 안전이 유지된다 (4장, p.174).[^rahman2025]

## 전략 넷 — 서브태스크 안에서 기본값으로 바꾸기

- 특정 예외가 연산 전체를 실패시키는 대신 기본 결과를 내야 할 때는 서브태스크 안에서 예외를
  다루는 편이 낫다. 부분 실패가 전체를 막아서는 안 되는 선택적 데이터 소스에 특히 맞는다 (4장
  §"Handling exceptions within subtasks", p.174).[^rahman2025]
- 저자가 꾸민 상황은 여러 선택적 서비스에서 자료를 모으는 대시보드다. 일부 서비스를 쓸 수 없어도
  모을 수 있는 만큼으로 화면을 보이고 싶다 (4장, p.174).[^rahman2025]
- 구현은 서브태스크 메서드 안에 catch를 두고 실패를 성공 응답으로 바꾸는 것이다 — 네트워크 오류면
  기본 데이터를, 시간 초과면 캐시 데이터를, 예상 밖 오류면 오류 표시를 담은 응답을 돌려준다 (4장,
  p.175).[^rahman2025]
- 그 효과가 넷으로 정리된다 — 서브태스크가 스스로 예외를 다루므로 `allSuccessfulOrThrow()`를 써도
  `FailedException`이 좀처럼 던져지지 않고, 각 서비스가 자기 서브태스크 안에서 대체 응답을
  마련하며, 바깥 catch는 정말 예상 밖의 실패만 받고, 개별 서비스의 실패가 연쇄로 번지지 않는다
  (4장, p.175).[^rahman2025]
- 저자의 규칙은 목적이다 — **우아한 성능 저하(graceful degradation)를 구현하려 할 때** 서브태스크
  안에서 예외를 다룬다. 부분 성공이 받아들여지는 선택적 연산에 잘 맞는다 (4장,
  p.176).[^rahman2025]
- 경고가 붙는다 — 서브태스크가 자기 예외를 다루면 바깥의 `FailedException` catch는 좀처럼 실행되지
  않아야 한다. 실행될 때 로그를 남기는 것을 고려하라. 예상 밖의 시스템 문제를 가리킬 수 있기
  때문이다 (4장, p.176).[^rahman2025]

## 조이너가 예외의 유무를 가른다

- 조이너의 선택이 예외 처리에 큰 영향을 준다. 저자가 두 정책을 나란히 놓고 견준다 (4장
  §"Understanding how different joiners handle exceptions", p.176).[^rahman2025]
- `allSuccessfulOrThrow()`는 실패 즉시 중단(fail-fast) 전략이다 — 하나만 실패해도 연산 전체가
  곧바로 실패한다. 세 태스크 중 둘째가 예외를 던지면 `join()`이 `FailedException`을 던지고 셋째는
  취소될 수 있다 (4장, p.176).[^rahman2025]
- `awaitAll()`은 반대다 — 개별 실패와 무관하게 모든 태스크가 완료되도록 허용한다. 둘째 태스크가
  여전히 예외를 던지지만 그것이 다른 태스크의 완료를 막지 않는다. **`awaitAll()`에서는 `join()`이
  결코 `FailedException`을 던지지 않는다** (4장, p.177).[^rahman2025]
- 그래서 대가가 생긴다 — `awaitAll()`로 성공과 실패를 모두 모으려면 **각 서브태스크 안에서 예외를
  다뤄야 한다** (4장, p.177).[^rahman2025] 그 정책은
  [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md)에 있고,
  성공과 실패를 한꺼번에 모으는 조이너를 직접 만드는 길은
  [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md)에 있다.

## 이어지는 페이지

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — `FailedException`이
  나오는 API의 모양과 API를 잘못 썼을 때의 예외들
- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 결말을 정하는 자리
- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 예외를 내는 쪽
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 예외를
  내지 않는 쪽
- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — 성공과 실패를 함께 모으는
  조이너를 직접 만드는 자리
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 절의 예제들이 쓰는 JDK 25 문법
- [죽은 프로그램은 거짓말하지 않는다](../concepts/dead-programs-tell-no-lies.md) — 예외를 잡아
  다시 던지는 습관에 대한 다른 소스의 판단
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Exception Handling in
    StructuredTaskScope"(pp.166–177), 그 안의 "Basic exception handling"(pp.166–167),
    "Pattern matching for sophisticated error handling"(pp.168–172), "Strategic exception
    propagation"(pp.172–174), "Handling exceptions within subtasks"(pp.174–176),
    "Understanding how different joiners handle exceptions"(pp.176–177). 인용한 코드는 pp.166–167의
    `BasicExceptionHandling.fetchUserData`이고, 조판 줄바꿈을 폈으며 원문 주석 한 줄을 깎았다.
    원문 그대로 둔 것이 하나 있다 — `profileTask`와 `preferencesTask` 두 지역 변수는 뒤에서 쓰이지
    않는다(결과는 `join()`이 돌려주는 스트림에서 꺼낸다). 개념당 대표 코드 하나 규칙에 따라 남긴 것:
    `fetchUserProfile`·`fetchUserPreferences`와 `main`(p.167), `OrderProcessingService`의
    `processOrder`·`handleOrderProcessingError`·세 흉내 메서드·네 예외 클래스·`main`(pp.168–172),
    `ExceptionPropagationExample` 전문(pp.172–173), `SubtaskExceptionHandling` 전문(pp.174–175),
    `demonstrateAllSuccessfulOrThrow`와 `demonstrateAwaitAll`(pp.176–177). 도메인 전용 예외
    타입에 관한 모범 사례 문장은 p.172 첫머리의 안내 상자에 있다.

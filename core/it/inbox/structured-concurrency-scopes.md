---
type: concept
title: 구조적 동시성 스코프
description: 자바가 구조적 동시성을 구현한 StructuredTaskScope의 모양 — 봉인 인터페이스와 fork·join·close라는 세 메서드, 인스턴스를 만드는 정적 팩토리 open, try-with-resources로 닫는 규칙과 중첩을 어겼을 때의 StructureViolationException, 그리고 서브태스크 하나가 실패하면 형제를 취소하고 FailedException으로 감싸 던지는 기본 동작
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 동시성 스코프

- [버전 조건](#버전-조건)
- [무엇에 답하는가](#무엇에-답하는가)
- [인터페이스와 세 메서드](#인터페이스와-세-메서드)
- [인스턴스를 만드는 자리](#인스턴스를-만드는-자리)
- [실물](#실물)
- [실패하면 무엇이 벌어지나](#실패하면-무엇이-벌어지나)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **자바는 구조적 동시성의 원칙을 어떤 API로 내놓았는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 이 페이지가 옮긴 API 모양은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. 저자는 앞으로의 JDK 릴리스에 코드 수정 없이 통합되리라 내다보지만
> 그것은 전망이지 확정이 아니다. **이 소스는 JEP 번호도, 이전 미리 보기 판의 API 모양도 4장
> 안에서는 말하지 않는다** — 다른 판과의 대조는 이 페이지의 근거 범위 밖이다.
>
> `stale_after`를 단 이유: 미리 보기 기능은 다음 JDK 릴리스에서 바뀌거나 정식화되는 것이
> 공식 규약이므로, 이 서술의 유효 범위는 "JDK 25"라는 고정된 판이 아니라 다음 릴리스까지의
> 기간이다. 자바는 6개월 주기로 릴리스하고, 이 책 다음 릴리스는 JDK 26(2026년 3월)이다.

## 무엇에 답하는가

- 앞선 방식의 결함이 출발점이다 — `Future::get`이 예외를 던질 수 있고, 타임아웃 장치가 없으면
  무한정 블로킹될 가능성이 있다 (2장, p.50).[^rahman2025] 그 방식은
  [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)에,
  더 깊은 결함인 태스크 위계의 부재는
  [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md)에 있다.
- 답의 이름과 출처가 명시된다 — 자바의 JEP 505가 구조적 동시성을 들이며, 목표는 튼튼한 동시
  코드를 쓰는 일을 단순하게 만드는 것이다 (2장, p.50).[^rahman2025]
- API가 주는 것은 태스크가 도는 구조화된 스코프이고, 그중 하나라도 실패하거나 시간이 다하면
  스코프 안의 모든 태스크가 자동으로 취소된다 (2장, p.50).[^rahman2025]
- 4장이 그 자리를 다시 짚는다 — 구조적 동시성 API의 심장에 `java.util.concurrent` 패키지의
  `StructuredTaskScope`가 있다 (4장 §"Understanding the API", p.133).[^rahman2025]

## 인터페이스와 세 메서드

- `StructuredTaskScope`는 봉인 인터페이스(sealed interface)이고, 스코프 안에서 실행되는 태스크의
  결과 타입을 나타내는 `T`와 `R`로 매개변수화된다 (4장, p.133):[^rahman2025]

  `public sealed interface StructuredTaskScope<T,R> extends AutoCloseable`

- `fork(Callable<? extends U> task)` — 스코프 안에 새 서브태스크(subtask)를 만들어 시작한다.
  태스크는 별도 스레드(대개 가상 스레드)에서 동시에 실행되고, 반환값은 도는 서브태스크를 나타내는
  `Subtask` 객체다 (4장, p.133).[^rahman2025]
- `fork(Runnable task)` — 결과를 내지 않는 동작용 오버로드다. 태스크가 `Runnable`이라 결과가
  없으므로 성공해도 `Subtask.get()`은 `null`을 돌려준다 (4장, pp.133–134).[^rahman2025]
- `join()` — 모든 서브태스크가 끝나거나 스코프가 취소될 때까지 기다린 뒤 결과를 돌려준다.
  호출 스레드(스코프 소유자여야 한다)를 막고, 타임아웃이 설정되어 있고 그것이 지나면 스코프가
  취소되며 `TimeoutException`이 던져진다. 기다림이 끝나면 조이너(Joiner)의 `result()`가 불려
  결과를 내거나 예외를 던지고, `result()`가 예외를 던지면 그 예외를 원인으로 하는
  `FailedException`이 던져진다. **이 메서드는 스코프 소유자가 한 번만 부를 수 있다** (4장,
  p.134).[^rahman2025] 그 조이너가 무엇인지는
  [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md)에 있다.
- `close()` — 스코프를 닫으며 모든 서브태스크가 완료되었거나 취소되었음을 보장한다.
  try-with-resources를 쓰면 대개 암묵적으로 불린다 (4장, p.134).[^rahman2025]

## 인스턴스를 만드는 자리

- 인터페이스라 직접 인스턴스를 만들 수 없고, 정적 팩토리 메서드 `open()`이 그 자리를 맡는다
  (4장, p.134):[^rahman2025]

  `static <T> StructuredTaskScope<T,Void> open()`

- 이 메서드가 만드는 스코프는 어떤 타입의 결과든 돌려주는 서브태스크를 갈라 놓을 수 있고, 그
  `join()`은 모든 서브태스크가 성공하거나 어느 하나가 실패할 때까지 기다린다 (4장,
  p.134).[^rahman2025] 오버로드로 조인 정책을 받는 판이 따로 있다.
- `AutoCloseable`을 확장하므로 try-with-resources 블록 안에서 쓰고, 그때 `close()`를 손으로
  부르지 않는다 (4장, p.134).[^rahman2025]
- 중첩 규칙이 강제된다 — 중첩된 태스크 스코프가 모두 닫히기 전에 바깥 스코프의 `close()`가
  불리면, 스코프는 ⑴ 중첩된 각 스코프의 바탕 구성물을 만들어진 역순으로 닫으려 시도하고,
  ⑵ 자신을 닫은 뒤, ⑶ 잘못된 닫기 순서를 알리는 `StructureViolationException`을 던진다
  (4장, p.134).[^rahman2025]

## 실물

앞의 비구조적 예제를 스코프로 다시 쓰면 `submit`과 `Future.get()` 자리가 `fork`와 `join`으로
바뀐다 (4장, p.135).[^rahman2025]

```java
public ProductInfo fetchProductInfo(Long productId) {
    log("Fetching product & reviews for id: " + productId);
    try (var scope = StructuredTaskScope.open()) {
        StructuredTaskScope.Subtask<Product> productTask =
            scope.fork(() -> fetchProduct(productId));
        StructuredTaskScope.Subtask<List<Review>> reviewsTask =
            scope.fork(() -> fetchReviews(productId));
        scope.join();
        return new ProductInfo(productTask.get(), reviewsTask.get());
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();
        throw new ProductServiceException(
            "Fetch failed for id: " + productId);
    }
}
```

- 미리 보기 기능이라 실행에 플래그가 필요하다 — `javac --release 25 --enable-preview Main.java`,
  `java --enable-preview Main`, 소스 코드 런처로는 `java --enable-preview Main.java`,
  JShell로는 `jshell --enable-preview` (4장, p.136).[^rahman2025]

## 실패하면 무엇이 벌어지나

- `scope.join()`은 두 서브태스크가 모두 끝나거나, 하나가 실패하거나, 스코프가 취소될 때까지
  막는다 (4장, p.135).[^rahman2025]
- 둘 다 성공하면 `join()`이 정상으로 돌아오고, 그때에야 각 핸들의 `get()`으로 결과를 꺼낸다
  (4장, p.135).[^rahman2025]
- 어느 하나가 실패하면 `join()`이 아직 도는 다른 서브태스크를 인터럽트하고, 그것이 끝나기를
  기다린 뒤, 원래 예외를 원인으로 하는 `StructuredTaskScope.FailedException`을 던진다 (4장,
  p.135).[^rahman2025]
- 저자가 그 동작을 스택 트레이스로 확인한다 — 상품 조회를 즉시 실패로 꾸미면 스코프가 동시에 돌던
  리뷰 조회를 곧바로 취소하고, `join()`이 원래 예외를 감싼 `FailedException`을 던져 부모
  스레드가 오류를 다룰 수 있게 한다 (4장, pp.136–137).[^rahman2025]
- 정리하면 셋이다 — 하나가 실패하면 다른 것이 자동으로 취소되어 자원 낭비가 사라지고, 부모 태스크가
  취소되면 스코프가 닫히며 두 서브태스크가 함께 끝나며, `join()`이 결과를 꺼내기 전에 완료를
  보장하므로 불완전한 데이터 문제가 생기지 않는다 (4장, p.137).[^rahman2025]

## 이어지는 페이지

- [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md) — 이 API가 구현하는
  언어 무관 규정
- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 이 API가 답하는
  결함
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — fork와 join과
  close 사이에서 실제로 무엇이 도는가
- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — `join()`이 언제 끝나고
  무엇을 돌려줄지를 정하는 자리
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 예외와
  조합을 다루던 앞선 API
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "The Promise of Structured
    Concurrency"(pp.50–51); 4장 "Structured Concurrency" — §"Understanding the API",
    "StructuredTaskScope"(pp.133–137). 인용한 코드는 4장 p.135의 `fetchProductInfo`이고
    조판 줄바꿈만 폈다. 2장 p.50의 짧은 예제(`fetchData` 두 개를 갈라 이어 붙이는 `main`)는
    같은 API의 같은 모양이라 개념당 대표 코드 하나 규칙에 따라 뺐다. 그림 4-2(p.137,
    `fetchProductInfo`가 두 조회를 갈라 조인하고 실패 시 취소하는 흐름)와 실패 시나리오의 전체
    스택 트레이스(pp.136–137)는 미수록이다.

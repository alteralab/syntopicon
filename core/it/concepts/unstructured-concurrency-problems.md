---
type: concept
title: 비구조적 동시성의 문제
description: 실행자와 Future로 동시 작업을 조율할 때 구조적으로 빠져 있는 것 — 태스크 위계가 없어 취소가 전파되지 않는다는 것, 그래서 실패한 요청의 형제 태스크가 계속 도는 스레드 누수와 쓸모없어진 결과를 기다리는 낭비, 그리고 스레드 덤프에 태스크와 서브태스크의 관계가 남지 않는다는 관측의 손실
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 비구조적 동시성의 문제

- [버전 조건](#버전-조건)
- [빠져 있는 것은 위계다](#빠져-있는-것은-위계다)
- [실물 예제](#실물-예제)
- [새는 자리 셋](#새는-자리-셋)
- [관측이 남지 않는다](#관측이-남지-않는다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **실행자와 `Future`로 동시 작업을 조율할 때 무엇이 구조적으로 빠져 있는가.**

## 버전 조건

> **버전 조건**: 아래 예제는 JDK 21 이상에서 돈다 —
> `Executors.newVirtualThreadPerTaskExecutor()`가 그 판부터 있는 정식 API다. 이 절이 짚는
> 결함 자체는 특정 판에 매이지 않는다. `ExecutorService`와 `Future`가 태스크 위계를 갖지
> 않는다는 사실이 그 결함의 원인이고, 그 사실은 두 API의 계약에서 온다.

## 빠져 있는 것은 위계다

- 저자가 원인을 한 줄로 짚는다 — `ExecutorService`와 `Future` 같은 전통적 동시성 모델에서는
  태스크 위계(task hierarchy)가 본래부터 지원되지 않는다. 그래서 취소를 전파하거나 오류를
  구조적으로 다루기가 어렵고, 결과는 조각나고 오류가 잦은 동시 프로그래밍이다 (4장 도입,
  p.125).[^rahman2025]
- 그 API들이 무엇을 해 주고 무엇을 남기는지는
  [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md)와
  [Callable과 Future로 결과 받기](../concepts/callable-and-future-results.md)에 있다. 이
  페이지가 보태는 것은 **거기 없는 넷째 결함**, 곧 태스크 사이의 관계가 표현되지 않는다는 것이다.
- 문제의 모양은 이렇다 — 부모 태스크가 여러 서브태스크(subtask)를 각각 다른 스레드에 두고 있는데
  부모가 예기치 않게 끝나면, 서브태스크들은 독립으로 계속 실행된다. 그 결과는 이미 쓸모가 없는데도
  자원은 계속 먹는다 (4장 도입, p.125).[^rahman2025] 저자는 이렇게 남겨진 스레드를 고아
  스레드(orphaned thread)라 부르고, 그것들이 불필요한 일을 하며 메모리와 프로세서 시간을 축낸다고
  적는다 (4장 도입, p.125).[^rahman2025]

## 실물 예제

저자가 드는 예는 상품 상세와 리뷰를 동시에 가져와 화면에 보여 주는 웹 애플리케이션이다 (4장,
p.126).[^rahman2025] 두 조회를 `ExecutorService`에 던지고 `Future.get()`으로 결과를 받는다.

```java
public class ProductService {
  public ProductInfo fetchProductInfo(Long productId) {
      log("Fetching product & reviews for id: " + productId);

        try (var ExecutorService
                  = Executors.newVirtualThreadPerTaskExecutor()) {

            Future<Product> productTask =
                ExecutorService.submit(() -> fetchProduct(productId));
            Future<List<Review>> reviewsTask =
                ExecutorService.submit(() -> fetchReviews(productId));
            Product product = productTask.get();
            List<Review> reviews = reviewsTask.get();
            return new ProductInfo(product, reviews);

        } catch (ExecutionException | InterruptedException e) {
            Throwable cause = e.getCause() != null ? e.getCause() : e;

            if (e instanceof InterruptedException) {
                Thread.currentThread().interrupt();
            }

            throw new ProductServiceException(
                "Fetch failed for id: " + productId, cause);
        }
    }
}
```

- 저자 자신이 이 코드에 대한 첫 인상을 적는다 — 언뜻 보면 완벽하게 합리적이다. 그러나 두 메서드가
  동시에 실행되므로 각각 독립으로 성공하거나 실패할 수 있다는 데서 문제가 시작된다 (4장,
  p.129).[^rahman2025]

## 새는 자리 셋

- **하나가 죽어도 나머지는 계속 돈다.** 상품 데이터베이스가 잠시 죽어 `fetchProduct()`가 예외를
  던지면 그 예외가 메인 요청 스레드를 멈추는데, 그 실패를 모르는 `fetchReviews()`는 제 스레드에서
  계속 실행된다. 이것이 스레드 누수(thread leak)이고, 자원을 붙들고 서버에 불필요한 부하를 더한다
  (4장, p.129).[^rahman2025]
- **인터럽트가 서브태스크까지 닿지 않는다.** 사용자가 요청을 포기해 서버가 요청 스레드를 인터럽트로
  멈추려 해도 서브태스크는 취소되지 않는다. `fetchProductInfo()`가 실패한 뒤에도
  `fetchProduct()`와 `fetchReviews()`는 계속 돌고, 이미 무의미해진 요청에 두 스레드와 CPU
  주기가 새어 나간다 (4장, p.130).[^rahman2025]
- **쓸모없어진 결과를 기다린다.** `fetchProductInfo()`는 두 결과가 다 있어야 성공한다. 그런데
  `fetchProduct()`가 `fetchReviews()`보다 훨씬 오래 걸리고 그 사이에 `fetchReviews()`가
  실패하면, 결국 버려질 `fetchProduct()`를 불필요하게 끝까지 기다린다 (4장,
  p.130).[^rahman2025]
- 저자가 이 셋을 실측으로 보인다 — 상품 조회를 5초, 리뷰 조회를 1초 뒤 실패로 꾸며 돌리면, 리뷰가
  1초에 실패했는데도 상품 조회가 5초를 다 채운 뒤에야 오류가 보고된다 (4장, p.131,
  실행 로그).[^rahman2025] 같은 비교를 정책 쪽에서 다시 재는 자리가
  [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md)에 있다.

## 관측이 남지 않는다

- 핵심 진단은 태스크를 서로 무관한 독립체로 다룬다는 것이다. 관계와 의존을 무시하므로 오류와 자원
  누수와 성능 병목이 자라는 토양이 된다 (4장, p.131).[^rahman2025]
- 그 대가는 진단 단계에서 다시 돌아온다 — 스레드 덤프 같은 관측 도구는 각 메서드 호출을 서로 무관한
  스레드들의 스택으로 보여 줄 뿐, 태스크와 서브태스크의 관계에 대한 단서를 주지 않는다 (4장,
  pp.131–132).[^rahman2025] 가상 스레드에서 그 덤프가 어떻게 달라지는지는
  [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md)에 있다.
- 이 문제들에 답하는 규정이
  [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md)이다.

## 이어지는 페이지

- [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md) — 이 결함들에 답하는
  규정
- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 자바가 그 규정을 구현한
  API
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 같은 API의
  다른 세 한계
- [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)
  — 이 코드 모양이 가상 스레드에서 왜 싸졌는가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — 장 도입(p.125), §"The Challenge of
    Unstructured Concurrency"(pp.126–132). 실은 코드는 원문의
    `fetchProductInfo`(p.127)이고, 조판 줄바꿈만 폈으며 `log` 호출 여섯 줄을 깎았다. 지역
    변수 이름 `ExecutorService`가 타입 이름과 같은 것은 원문 그대로다. 개념당 대표 코드 하나
    규칙에 따라 남긴 것: `Product`·`Review`·`ProductInfo` 레코드와
    `ProductServiceException`(p.126), 흉내 메서드 `fetchProduct`·`fetchReviews`·
    `sleepForAWhile`·`log`와 `main`(pp.128–129), 실패를 꾸민 개정판
    `fetchProduct`·`fetchReviews`(pp.130–131). 그림 4-1(p.130, 자식 하나의 예외가 부모를
    멈추고 다른 자식이 고아가 되는 그림)은 미수록이다.

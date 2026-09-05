---
type: concept
title: 첫 성공으로 끝내는 경주
description: anySuccessfulResultOrThrow 정책이 서브태스크를 경주시켜 먼저 성공한 하나의 결과를 join의 반환값으로 삼고 나머지를 즉시 취소한다는 것, 그 취소가 서브태스크 쪽에서는 인터럽트로 도착한다는 것, 전부 실패했을 때만 예외가 된다는 것, 그리고 캐시와 데이터베이스와 외부 API를 나란히 던진 실측 시간
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-06T00:20:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 첫 성공으로 끝내는 경주

- [버전 조건](#버전-조건)
- [먼저 들어온 쪽이 이긴다](#먼저-들어온-쪽이-이긴다)
- [세 소스를 나란히 던지는 예제](#세-소스를-나란히-던지는-예제)
- [취소는 인터럽트로 도착한다](#취소는-인터럽트로-도착한다)
- [실측](#실측)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **같은 답을 여러 곳에서 구할 수 있을 때 가장 먼저 오는 것만 쓰고 나머지를 어떻게
끊는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 팩토리 이름과 반환 모양은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 먼저 들어온 쪽이 이긴다

- `Joiner.anySuccessfulResultOrThrow()` 정책은 서브태스크(subtask)들을 경주시켜 하나가 성공으로
  완료되는 순간 승자를 선언한다. 저자는 이것을 먼저 결승선을 통과한 쪽이 이기는 방식으로 부른다
  (4장 §"Race for the first successful result", p.146).[^rahman2025]
- 승자가 나오는 순간 조이너(Joiner)가 아직 도는 나머지 서브태스크를 모두 취소한다 (4장,
  p.146).[^rahman2025]
- 예외는 **전부 실패했을 때만** 나온다 — `FailedException`은 모든 서브태스크가 실패한 경우에
  던져진다 (4장, p.148).[^rahman2025]

## 세 소스를 나란히 던지는 예제

- 저자가 꾸민 상황은 상품 정보를 응답 시간이 다른 세 곳에서 가져오는 것이다 — 500밀리초 걸리는 캐시,
  2초 걸리는 데이터베이스, 3초 걸리는 외부 API. 무엇이든 먼저 오는 것으로 진행한다 (4장,
  p.147).[^rahman2025]

  ```java
  public Product fetchProduct(long productId) {
    Instant start = Instant.now();
    try (var scope
             = StructuredTaskScope.open(
                 StructuredTaskScope
                     .Joiner.<Product>anySuccessfulResultOrThrow())) {
      scope.fork(() -> fetchProductFromDatabase(productId));
      scope.fork(() -> fetchProductFromCache(productId));
      scope.fork(() -> fetchProductFromAPI(productId));
      return scope.join();
    } catch (InterruptedException | StructuredTaskScope.FailedException e) {
      throw new RuntimeException(e);
    } finally {
      Instant end = Instant.now();
      log("Total time taken: %dms%n"
          .formatted(Duration.between(start, end).toMillis()));
    }
  }
  ```

- 이 정책에서는 `scope.join()`이 **처음 성공한 서브태스크의 결과 자체를 돌려준다** (4장, p.148,
  코드 주석).[^rahman2025] 기본 정책에서 `join()`이 결과를 돌려주지 않고 핸들에서 꺼내야 했던 것과
  갈리는 자리다 ([실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md)).

## 취소는 인터럽트로 도착한다

- 취소되는 쪽 코드가 그 사실을 드러낸다 — 데이터베이스 조회와 API 호출 예제는 `InterruptedException`을
  잡는 블록을 두고, 저자가 그 블록에 "스코프가 이 태스크를 취소할 때 실행된다"는 주석을 달아 둔다
  (4장, p.147).[^rahman2025] 그 블록은 취소 사실을 로그로 남기고
  `Thread.currentThread().interrupt()`로 인터럽트 상태를 되살린 뒤 예외를 다시 던진다.
- 가상 스레드에서 인터럽트 규칙이 그대로라는 것은
  [가상 스레드에서 달라지는 Thread API](../concepts/virtual-thread-api-semantics.md)에 있다.

## 실측

- 세 조회가 모두 갈라져 나란히 돌다가 약 500밀리초 뒤 가장 빠른 캐시 조회가 성공한다. 바로 그 순간
  조이너 정책이 조건을 만족했다고 보고 나머지 둘을 즉시 취소하며, 취소 메시지가 로그에 찍혀 그것이
  실제로 일어났음을 보인다 (4장, pp.149–150).[^rahman2025]
- 전체 소요는 **513ms**로, 느린 쪽을 기다리는 시간을 버리지 않고 끝난다 (4장, p.149, 실행
  로그).[^rahman2025]

## 이어지는 페이지

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 이 정책이 놓인 틀
- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 반대로 전부 성공해야 하는 쪽
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 첫 성공에서
  멈추는 조건을 직접 쓰는 쪽
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 취소된 뒤 스코프가
  무엇을 기다리는가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Race for the first successful
    result"(pp.146–150). 인용한 코드는 p.148의 `fetchProduct`이고, 조판 줄바꿈을 폈으며 원문
    주석 세 줄을 깎았다. 개념당 대표 코드 하나 규칙에 따라 남긴 것: 세 조회 흉내 메서드
    `fetchProductFromCache`·`fetchProductFromDatabase`·`fetchProductFromAPI`(p.147),
    `RacePolicyDemo`의 `main`과 `Product` 레코드(p.149), 실행 출력(p.149).

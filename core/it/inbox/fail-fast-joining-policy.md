---
type: concept
title: 실패 즉시 중단 정책
description: 서브태스크 하나라도 실패하면 스코프 전체를 접는 두 정책 — 기본값인 awaitAllSuccessfulOrThrow와 성공 시 결과를 스트림으로 모아 주는 allSuccessfulOrThrow, 그 둘이 실패에서 똑같이 행동한다는 것, 그리고 같은 시나리오를 실행자로 돌렸을 때와 갈리는 실측 시간
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 실패 즉시 중단 정책

- [버전 조건](#버전-조건)
- [전부 성공 아니면 무효](#전부-성공-아니면-무효)
- [실측으로 갈리는 자리](#실측으로-갈리는-자리)
- [결과를 스트림으로 모으는 판](#결과를-스트림으로-모으는-판)
- [일괄 검증 예제](#일괄-검증-예제)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **하나라도 실패하면 전부 접는 정책은 무엇을 보장하고 무엇을 돌려주는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 팩토리 이름과 반환 타입은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 전부 성공 아니면 무효

- `open()`으로 스코프를 만들면 모든 서브태스크(subtask)가 성공해야 한다는 정책이 기본으로 붙고,
  그 전부 성공 아니면 무효(all-or-nothing) 방식은 내부적으로
  `Joiner.awaitAllSuccessfulOrThrow()`가 관리한다 (4장 §"Wait for all to succeed or first to
  fail", p.141).[^rahman2025]
- 그래서 서브태스크 하나만 실패해도 스코프 전체가 내려간다. 남아서 진행 중이던 서브태스크는 즉시
  취소되고, 실패한 서브태스크의 오류가 부모 태스크로 전파된다 (4장, p.141).[^rahman2025]
- 이 설계가 보장하는 것은 **연산의 모든 부분이 성공했을 때만 결과를 받는다**는 것이고, 그래서
  불완전하거나 일부만 처리된 결과를 쓰는 일이 막힌다 (4장, p.141).[^rahman2025]

## 실측으로 갈리는 자리

저자가 같은 시나리오를 성공 경로와 실패 경로로 두 번 돌린다 (4장, pp.143–146).[^rahman2025]
1초짜리 상품 조회와 2초짜리 리뷰 조회를 갈라 놓은 예제다.

- **성공 경로 — 2,012ms.** 두 서브태스크가 거의 같은 순간에 시작해 나란히 돌고, 메인 스레드는
  `scope.join()`에서 막혀 기다린다. 1초 뒤 상품 조회가 끝나도 더 느린 리뷰 조회가 남아 있어 계속
  기다리다가, 2초 뒤 그것이 끝나 모든 서브태스크가 성공하자 `join()`이 돌아온다. 전체 소요는 약
  2,000ms이고, 이것은 연산의 길이가 **가장 오래 걸리는 서브태스크에 의해 정해진다**는 뜻이다
  (4장, p.144).[^rahman2025]
- **실패 경로 — 7ms.** 즉시 실패하는 태스크와 2초짜리 리뷰 조회를 함께 갈라 놓았는데도 전체 연산이
  7밀리초 만에 끝난다. 첫 서브태스크가 실패하는 순간 조이너(Joiner) 정책이 나머지 서브태스크를
  취소하고 `scope.join()`이 곧바로 `FailedException`을 던지기 때문이다. 결과가 무의미해질 리뷰
  조회를 기다리느라 시간을 버리지 않는다 (4장, p.145).[^rahman2025]
- **같은 일을 실행자로 — 2,010ms.** 저자가 대조군으로
  `Executors.newVirtualThreadPerTaskExecutor()`에 같은 두 태스크를 던진다. 실패하는 조회가 거의
  즉시 죽는데도 리뷰 조회는 그것을 전혀 모른 채 2초를 다 채우고, 로그가 그 뒤에 리뷰를 다 가져왔다고
  찍는다. `ExecutorService`에는 공유 스코프라는 개념이 없어 두 `Future`가 서로 독립이고, 결국
  버릴 결과를 기다리며 프로그램이 막혀 있었다 (4장, pp.145–146).[^rahman2025] 이 대조의 구조적
  원인이 [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md)에 있다.

## 결과를 스트림으로 모으는 판

- `allSuccessfulOrThrow()`는 실패했을 때는 기본 정책과 똑같이 행동한다. 엄격한 전부 성공 아니면
  무효 전략을 유지해, 서브태스크가 하나라도 실패하면 나머지를 즉시 취소하고 `scope.join()`이
  `FailedException`을 던진다 (4장 §"Gather all results or fail fast",
  p.150).[^rahman2025]
- 갈리는 것은 성공했을 때다. `join()`이 `void`를 돌려주는 대신
  `java.util.Stream<Subtask<T>>`를 돌려준다. 이 스트림에는 성공적으로 완료된 모든 서브태스크의
  핸들이 **갈라 놓은 순서대로** 담기고, 그래서 결과를 한꺼번에 처리하기 쉽다 (4장,
  p.150).[^rahman2025]
- 그래서 고르는 기준이 결과 타입이다 — 서브태스크가 모두 같은 타입을 돌려주고 전부 성공해야 할 때
  이 조이너를 쓰고, 서로 다른 타입을 돌려줄 때는 어차피 하나씩 다루게 되므로 기본 정책이 더 맞는다
  (4장, p.150).[^rahman2025]

## 일괄 검증 예제

저자가 드는 예는 사용자 아이디 목록을 외부 서비스에 대조해 검증하는 일이다. 동시에 하되 **모든
아이디가 검증되어야만 그 묶음이 유효하다** (4장, p.150).[^rahman2025]

```java
public List<ValidatedUser> validateAllUsers(List<Long> userIds)
    throws InterruptedException {
  log("Validating a batch of " + userIds.size() + " users...");
  try (var scope
           = open(Joiner.<ValidatedUser>allSuccessfulOrThrow())) {
    var subtasks = userIds.stream()
        .map(id -> scope.fork(() -> validateUserWithFailure(id)))
        .toList();
    var resultStream = scope.join();
    return resultStream
        .map(Subtask::get)
        .toList();
  } catch (FailedException ex) {
    throw new RuntimeException("Batch validation failed",
        ex.getCause());
  }
}
```

- 실행 결과가 두 결말을 보인다 — 성공 시나리오에서는 네 검증 태스크가 모두 가상 스레드에서 돌고
  마지막 것이 끝나기를 `join()`이 기다린 뒤 결과 스트림을 돌려준다. 실패 시나리오에서는 다섯
  태스크를 갈라 놓았는데 3번 사용자가 즉시 실패하자 조이너가 스코프 전체를 취소하고, `join()`은
  스트림 대신 곧바로 `FailedException`을 던진다 (4장, pp.153–154).[^rahman2025]
- **관찰의 핵심은 로그에 없는 줄이다** — 나머지 태스크 가운데 어느 것도 검증 완료 메시지를 찍지
  못했다. 완료되기 전에 모두 취소되었기 때문이고, 이것이 일괄 작업의 무결성을 지키는 방식이다
  (4장, p.154).[^rahman2025]

## 이어지는 페이지

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 이 정책들이 놓인 틀과
  나머지 정책들
- [첫 성공으로 끝내는 경주](../concepts/racing-subtasks-for-first-result.md) — 반대로 하나만
  성공하면 끝내는 쪽
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 실패를
  취소 신호로 삼지 않는 쪽
- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 실행자 대조군이
  왜 2초를 버렸는가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Wait for all to succeed or first to
    fail"(pp.141–146), §"Gather all results or fail fast"(pp.150–154). 인용한 코드는 p.151의
    `validateAllUsers`이고, 조판 줄바꿈을 폈으며 `log` 호출 두 줄과 원문 주석 두 줄을 깎았다.
    **원문의 `catch (FailedException ex)` 블록은 실패 경로인데도 검증에 성공했다는 문구를
    로그로 찍는다**(p.151). 같은 예제의 실행 출력(p.153)은 실패를 알리는 다른 문구를 보여 주므로
    책의 코드와 출력이 어긋난다 — 이 KB는 그 로그 줄을 깎아 옮겼고 어긋남만 여기 적어 둔다.
    개념당 대표 코드 하나 규칙에 따라 남긴 것: 성공·실패용 `fetchProduct`·`fetchProductThatFails`·
    `fetchReviews`와 `Utils.log`(pp.141–142), `DefaultPolicyDemo`의 `fetchProductInfo`와
    `main`(pp.142–144), 실행자 대조군 `fetchProductInfoWithExecutor`(pp.145–146),
    `ValidatedUser` 레코드와 `validateUser`·`validateUserWithFailure`(pp.150–151),
    `BatchValidationDemo`의 `main`(p.152). 실행 출력(pp.143–146, pp.153–154)도 미수록이고
    본문의 수치만 옮겼다.

---
type: concept
title: 조이너와 조인 정책
description: join이 언제 끝나고 무엇을 돌려줄지를 조이너 객체가 정한다는 설계, 결과 메서드 둘과 수명 주기 훅 둘로 이루어진 인터페이스, 그리고 자바가 정적 팩토리로 내주는 다섯 가지 공통 정책과 그중 무엇을 고를지의 기준
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 조이너와 조인 정책

- [버전 조건](#버전-조건)
- [고정 정책 대신 인터페이스](#고정-정책-대신-인터페이스)
- [네 메서드의 역할이 갈린다](#네-메서드의-역할이-갈린다)
- [다섯 가지 공통 정책](#다섯-가지-공통-정책)
- [무엇을 고를 것인가](#무엇을-고를-것인가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프의 `join()`이 언제 끝나고 무엇을 돌려줄지는 무엇이 정하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 인터페이스와 팩토리 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라
> 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로
> 잡은 것이다.

## 고정 정책 대신 인터페이스

- `StructuredTaskScope`의 핵심 기능 하나가 조이너(Joiner) 객체를 통해 유연한 조인 정책을 정의할
  수 있다는 것이다. 조이너는 `join()`이 어떤 조건에서 완료되는지, 그리고 어떤 결과 또는 결말을
  내는지를 지시함으로써 서브태스크(subtask)의 수명 주기를 관리하는 기제다 (4장 §"Joining Policies
  with Joiner", p.139).[^rahman2025]
- 설계의 갈림이 여기다 — 자바는 몇 개의 고정된 정책을 주는 대신 `Joiner` 인터페이스를 준다 (4장,
  p.139).[^rahman2025] 그 인터페이스를 단순화해 보면 결말 메서드와 수명 주기 훅(lifecycle hook)이
  함께 들어 있다 (4장, p.139).[^rahman2025]

```java
public interface Joiner<T, R> {
    R result();
    Throwable exception();
    default boolean onFork(Subtask<? extends T> subtask) { ... }
    default boolean onComplete(Subtask<? extends T> subtask) { ... }
}
```

## 네 메서드의 역할이 갈린다

- `result()`와 `exception()`은 **결말 메서드**로, `scope.join()`의 최종 결말에 대한 계약을
  정의한다. 구현은 둘 중 하나에 대한 논리를 반드시 제공해야 한다 — 성공 값을 돌려주거나 던질 예외를
  내거나 (4장, pp.139–140).[^rahman2025]
- `onFork()`는 **수명 주기 훅**으로, 새 서브태스크가 만들어질 때 조이너가 그것을 인지하고 추적할 수
  있게 한다 (4장, p.140).[^rahman2025] 이 훅이 스레드를 띄울지까지 가른다는 것은
  [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md)에 있다.
- `onComplete()`는 **정책의 핵심 논리가 놓이는 자리**다. 어떤 서브태스크 하나의 완료가 전체 조인
  조건을 만족시키는지를 검사한다 — "이것이 첫 성공인가", "이제 모든 태스크가 실패했는가" 같은 물음이다
  (4장, p.140).[^rahman2025]

## 다섯 가지 공통 정책

조이너는 흔히 쓰이는 정책을 만드는 정적 팩토리 메서드를 여럿 제공한다 (4장 §"Common Joining
Policies", pp.140–141).[^rahman2025]

- `Joiner.awaitAllSuccessfulOrThrow()` — **기본 정책**이고 `StructuredTaskScope.open()`을 부를
  때 적용된다. 내부의 `onComplete()` 논리가 완료된 태스크 수를 추적하다가, 서브태스크가 하나라도
  실패하면 스코프를 취소한다. 갈라 놓은 모든 서브태스크가 성공했을 때만 `join()`이 성공으로 끝난다.
- `Joiner.anySuccessfulResultOrThrow()` — 먼저 도착한 쪽이 이기는 경주 정책이다. `onComplete()`가
  완료된 서브태스크의 성공 여부를 확인하고, 성공했으면 즉시 스코프를 취소하며 `result()`가 그 성공
  결과를 돌려준다.
- `Joiner.allSuccessfulOrThrow()` — `onComplete()` 훅이 성공적으로 완료된 모든 서브태스크의 결과를
  모은다. 모두 끝나기를 기다린 뒤 모은 결과를 `Stream`으로 내준다.
- `Joiner.awaitAll()` — 성공하든 실패하든 모든 서브태스크가 완료될 때까지 기다린다. 모든 태스크의
  결말을 알아야 하고 각각을 따로 다뤄야 할 때 쓸모 있다.
- `Joiner.allUntil(Predicate<Subtask> isDone)` — 가장 유연한 팩토리 메서드로, 사용자 정의 취소
  논리를 허용한다. 서브태스크가 완료될 때마다 검사되는 `Predicate`를 받고, 그것이 `true`를 돌려주면
  스코프가 취소된다. "서브태스크 둘이 실패하면 취소" 같은 정책을 만들 수 있다. `Predicate`가 끝까지
  `true`를 돌려주지 않으면 `awaitAll()`처럼 동작한다. 어느 쪽이든 `scope.join()`은 갈라 놓은 모든
  서브태스크가 담긴 `Stream<Subtask>`를 돌려준다.
- 이 접근이 주는 것은 완료 기준과 반환값에 대한 세밀한 제어다 — 모두 성공할 때까지 기다리는 쪽부터,
  경주시켜 처음 얻은 결과를 쓰는 쪽, 여러 결과를 스트림으로 모으는 쪽까지 (4장,
  p.141).[^rahman2025]
- **`awaitAll()`이 `join()`에서 무엇을 돌려주는가는 이 소스 안에서 어긋난다.** 위 카탈로그(p.140)는
  `Stream<Subtask>`를 돌려준다고 적지만, 그 정책을 따로 다루는 절(p.154)은 **언제나 `null`을
  돌려준다**고 적고, 같은 절의 예제 코드(p.156)는 `Void result = scope.join();`으로 뒤쪽 서술과
  맞는다.[^rahman2025] 이 KB는 어느 쪽도 단정하지 않고 두 서술을 그대로 둔다 —
  [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) 참고.

## 무엇을 고를 것인가

- 저자가 명시하는 기준 하나는 **결과 타입이 같은가**다. 서브태스크가 모두 같은 타입을 돌려주고 전부
  성공해야 할 때는 `allSuccessfulOrThrow()`를 쓴다. 서로 다른 타입을 돌려줄 때는 어차피 결과를
  하나씩 따로 다루게 되므로 기본 정책인 `awaitAllSuccessfulOrThrow()`가 더 맞는다 (4장,
  p.150).[^rahman2025]
- 부수 효과가 목적이거나 일부만 성공해도 값이 있을 때는 `awaitAll()` 쪽이다 (4장,
  p.154).[^rahman2025]

## 이어지는 페이지

- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 하나라도 실패하면 전부 접는 두
  정책과 그 실측
- [첫 성공으로 끝내는 경주](../concepts/racing-subtasks-for-first-result.md) — 가장 빠른 결과만
  쓰고 나머지를 취소하는 쪽
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 실패해도
  나머지를 끝까지 돌리는 쪽
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 조건을
  직접 쓰는 쪽
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 이 훅들이 불리는
  절차
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Joining Policies with
    Joiner"(pp.139–140), §"Common Joining Policies"(pp.140–141), 그리고 정책 선택 기준은
    §"Gather all results or fail fast"(p.150)와 §"Wait for all"(p.154). 인용한 인터페이스
    선언은 원문이 "단순화한 모습"이라고 밝힌 것 그대로이며(본문 생략 표시 포함), 조판 줄바꿈만
    폈다.

---
type: concept
title: 커스텀 조이너의 계약
description: Joiner 인터페이스를 직접 구현해 조인 정책을 만들 때 지켜야 하는 계약 — 두 타입 매개변수의 뜻, onFork와 onComplete와 result가 각각 언제 불리는지, 두 훅이 돌려주는 boolean이 계속과 취소를 가르는 스위치라는 것, 서브태스크의 세 가지 최종 상태, 그리고 성공과 실패를 함께 모으는 조이너라는 대표 실물
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 커스텀 조이너의 계약

- [버전 조건](#버전-조건)
- [왜 직접 만드는가](#왜-직접-만드는가)
- [세 메서드가 불리는 시점](#세-메서드가-불리는-시점)
- [boolean 하나가 계속과 취소를 가른다](#boolean-하나가-계속과-취소를-가른다)
- [서브태스크의 세 가지 최종 상태](#서브태스크의-세-가지-최종-상태)
- [대표 실물 — 성공과 실패를 함께 모으기](#대표-실물--성공과-실패를-함께-모으기)
- [세 메서드로 무엇까지 되는가](#세-메서드로-무엇까지-되는가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **미리 준비된 조인 정책 대신 내 정책을 만들려면 무엇을 구현해야 하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 아래 인터페이스와 메서드 이름과 상태 이름은 이 소스가 쓰는 JDK 25 판의 것이고,
> 미리 보기 기능이라 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년
> 3월)를 재심 시점으로 잡은 것이다.

## 왜 직접 만드는가

- 내장 조이너(Joiner)들이 태스크 조율과 결과 관리의 튼튼한 바탕을 주지만 구조적 동시성이 거기서
  멈추지 않는다 — 개발자가 자기 애플리케이션에 맞는 커스텀 조이너(custom joiner)를 만들 수 있게
  한다 (4장 §"Custom Joiners", p.185).[^rahman2025]
- 그 유연함이 여는 것은 서브태스크(subtask)가 어떻게 관리되고 결과가 어떻게 모이는지를 정밀하게
  통제하며 동시 작업 흐름을 조율하는 길이다 (4장, p.185).[^rahman2025]
- 만드는 법은 하나다 — `StructuredTaskScope.Joiner<T, R>` 인터페이스를 구현한다. 이 인터페이스가
  서브태스크의 완료 사건을 다루고, 스코프가 언제 완료되어야 하며 어떤 결과를 내야 하는지를 정하는
  메서드를 준다 (4장, p.185).[^rahman2025]
- 타입 매개변수 둘의 뜻이 갈린다 — `T`는 **서브태스크들이 만들어 내는 값의 타입**이고, `R`은
  **최종 결과의 타입**이다 (4장, p.185).[^rahman2025]

## 세 메서드가 불리는 시점

저자는 이 인터페이스가 정의하는 핵심 메서드를 셋으로 꼽는다 (4장, p.185).[^rahman2025]

- `onFork(Subtask<? extends T> subtask)` — 서브태스크가 갈라질 때마다 불리며, **그것을 돌릴
  스레드가 만들어지기 전에** 불린다.
- `onComplete(Subtask<? extends T> subtask)` — 서브태스크가 완료될 때마다 불리며, 결과를 처리하고
  계속할지 일찍 끝낼지 정하게 해 준다.
- `result()` — 스코프가 최종 결과를 낼 준비가 되었을 때 불린다.

그 셋이 놓인 인터페이스 전체의 모양과 자바가 미리 내주는 다섯 정책은
[조이너와 조인 정책](../concepts/structured-concurrency-joiner.md)에 있다.

## boolean 하나가 계속과 취소를 가른다

- 두 훅이 모두 `boolean`을 돌려주고, 그 값이 스코프를 계속 돌릴지 취소할지를 가른다. 저자가 예제
  주석에서 그 뜻을 반복해 밝힌다 (4장, pp.187–201).[^rahman2025]
  - `onComplete`가 `false`를 돌려주면 남은 서브태스크들이 자연히 끝날 때까지 계속 돌게 둔다 (4장,
    p.187).[^rahman2025]
  - `onComplete`가 `true`를 돌려주면 남은 태스크를 취소하고 스코프를 끝낸다 (4장,
    p.190).[^rahman2025]
  - `onFork`가 `false`를 돌려주면 그 서브태스크가 만들어져 실행을 시작해도 된다는 뜻이다 (4장,
    p.190과 p.197).[^rahman2025]
  - `onFork`가 `true`를 돌려주면 스코프를 취소해 새 작업이 시작되지 못하게 막는다 (4장,
    p.199).[^rahman2025]
- 그래서 두 훅의 역할이 갈린다 — `onFork`는 **시작을 통제하고**, `onComplete`는 **끝을
  앞당긴다.** 각각의 실물은
  [fork 시점의 시작 통제](../concepts/fork-time-admission-control.md)와
  [결과를 보고 일찍 끝내는 커스텀 조이너](../concepts/early-completion-custom-joiners.md)에 있다.

## 서브태스크의 세 가지 최종 상태

- 커스텀 조이너가 `onComplete`에서 가장 먼저 보는 것이 `subtask.state()`이고, 저자의 예제들은
  그것을 세 갈래로 나눈다 (4장, pp.186–187):[^rahman2025]
  - `SUCCESS` — `subtask.get()`으로 결과를 꺼낸다.
  - `FAILED` — `subtask.exception()`으로 예외를 꺼낸다.
  - `UNAVAILABLE` — **완료되기 전에 취소된** 태스크다. 저자의 예제들은 취소를 실패로 보고 그
    사실을 담은 예외를 대신 만들어 넣는다 (4장, p.187).[^rahman2025]
- 그 상태가 서브태스크 핸들에 실려 조이너에게 넘어온다는 것은
  [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md)에 있다.

## 대표 실물 — 성공과 실패를 함께 모으기

- 저자가 첫 예로 드는 상황은 성공하든 실패하든 모든 서브태스크의 결과를 모으고 일어난 예외도 함께
  거두는 것이다. 무엇이 성공하고 무엇이 실패했는지를 최대한 알고 싶은 일괄 처리에 쓸모 있다 (4장
  §"Collecting all results and exceptions", p.186).[^rahman2025]

  ```java
  public class CollectingJoiner<T>
      implements StructuredTaskScope.Joiner<T, CollectingJoiner.Result<T>> {

    private final Queue<T> results = new ConcurrentLinkedQueue<>();
    private final Queue<Throwable> exceptions = new ConcurrentLinkedQueue<>();

    @Override
    public Result<T> result() {
      return new Result<>(results.stream().toList(),
          exceptions.stream().toList());
    }

    @Override
    public boolean onComplete(StructuredTaskScope.Subtask<? extends T> subtask) {
      switch (subtask.state()) {
        case SUCCESS -> results.add(subtask.get());
        case FAILED -> exceptions.add(subtask.exception());
        case UNAVAILABLE -> exceptions.add(
            new RuntimeException("Task was canceled"));
      }
      return false;
    }

    public record Result<T>(List<T> successes, List<Throwable> failures) {
      public boolean hasFailures() { return !failures.isEmpty(); }
      public int totalTasks() { return successes.size() + failures.size(); }
    }
  }
  ```

- 실물 쓰임은 여러 온라인 소스에서 헤드라인을 모으는 서비스다. 소스 넷 중 하나가 실패하도록
  꾸며 놓았는데도 나머지 셋의 헤드라인을 얻고, 실패한 하나의 오류 문구도 함께 얻는다 (4장,
  pp.187–189).[^rahman2025]
- `onFork`를 재정의하지 않았다는 점이 이 조이너의 성질을 말해 준다 — 시작은 통제하지 않고 완료만
  거둔다. 이 조이너가 답하는 것이 `awaitAll()`을 쓸 때 성공과 실패를 함께 모으려면 각 서브태스크
  안에서 예외를 잡아야 했던 자리다
  ([구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md)).

## 세 메서드로 무엇까지 되는가

- 저자가 절을 닫으며 내놓는 총평이다 — 커스텀 조이너는 자바 구조적 동시성의 가장 강력한 면
  가운데 하나이고, `StructuredTaskScope`를 단순한 병렬 실행 도구에서 사실상 어떤 동시성 과제에도
  맞출 수 있는 정교한 조율 플랫폼으로 바꾼다 (4장, p.201).[^rahman2025]
- 그 아름다움이 단순함과 유연함에 있다 — **`onFork`와 `onComplete`와 `result` 단 세 메서드만으로**
  임의로 복잡한 조율 논리를 구현하면서도 구조적 동시성의 안전 보장과 깔끔한 구조를 그대로
  유지할 수 있다 (4장, p.201).[^rahman2025]
- 저자가 든 예제들은 시작일 뿐이고, 진짜 힘은 자기 도메인 고유의 조율 패턴을 담은 조이너를 설계해
  재사용 가능한 구성 요소로 만들 때 드러난다 (4장, pp.201–202).[^rahman2025]

## 이어지는 페이지

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 이 인터페이스의 전체
  모양과 자바가 미리 내주는 다섯 정책
- [결과를 보고 일찍 끝내는 커스텀 조이너](../concepts/early-completion-custom-joiners.md) —
  `onComplete`가 끝을 앞당기는 쪽
- [fork 시점의 시작 통제](../concepts/fork-time-admission-control.md) — `onFork`가 시작을
  막거나 늦추는 쪽
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 조이너를
  만들지 않고 술어 하나로 끝내는 더 싼 길
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 이 훅들이
  꽂히는 절차
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 절의 예제들이 쓰는 JDK 25 문법
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Custom Joiners"(pp.185–202),
    그 안의 "Collecting all results and exceptions"(pp.186–189)와 닫는 총평(pp.201–202).
    `boolean` 반환값의 뜻은 다섯 예제의 주석에 흩어져 있어 각각의 쪽을 함께 적었다.
    인용한 코드는 pp.186의 `CollectingJoiner`이고, 조판 줄바꿈을 폈으며 원문 주석 한 줄을
    깎았다. **원문이 조이너의 메서드를 세는 수가 두 자리에서 다르다** — p.139의 단순화한
    인터페이스 선언은 `result`·`exception`·`onFork`·`onComplete` 넷을 담고, p.185와 p.201은
    "세 메서드"로 세며 `exception()`을 빼놓는다. 이 KB는 어느 쪽도 단정하지 않고 두 서술을
    그대로 둔다. 개념당 대표 코드 하나 규칙에 따라 남긴 것: `NewsAggregator` 전문과 실행
    출력(pp.187–189).

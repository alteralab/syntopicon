---
type: concept
title: 스코프와 서브태스크의 수명 주기
description: fork가 서브태스크 핸들을 만들고 조이너에게 물은 뒤에야 스레드를 띄운다는 절차, 핸들의 결과를 join 뒤에만 꺼낼 수 있다는 제약, 서브태스크가 끝날 때 조이너에게 알려지는 최종 상태, 그리고 스코프가 닫힐 때 모든 서브태스크 스레드의 종료를 기다려 주는 보장
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 스코프와 서브태스크의 수명 주기

- [버전 조건](#버전-조건)
- [부모 그릇과 경계](#부모-그릇과-경계)
- [fork가 하는 일](#fork가-하는-일)
- [핸들은 join 뒤에야 열린다](#핸들은-join-뒤에야-열린다)
- [끝날 때 무엇이 알려지나](#끝날-때-무엇이-알려지나)
- [닫힐 때의 보장](#닫힐-때의-보장)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`fork`와 `join`과 `close` 사이에서 스코프와 서브태스크에게 실제로 무슨 일이
일어나는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 이 절차는 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라 정식화될 때 바뀔 수
> 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로 잡은 것이다.

## 부모 그릇과 경계

- 구조적 동시성은 `StructuredTaskScope`를 자식 서브태스크(subtask)를 관리하는 부모 그릇으로 쓰고,
  그 수명 주기와 실행을 스코프가 맡는다. 각 서브태스크는 스코프 안의 가상 스레드 위에서 도는 동시
  작업의 단위다 (4장 §"Scopes and Subtasks: Relationship and Lifecycle",
  p.138).[^rahman2025]
- 이 부모-자식 관계가 조율되고 예측 가능한 실행 흐름을 보장한다 (4장, p.138).[^rahman2025]
- 스코프는 동시 연산의 경계 지어진 문맥(bounded context)을 정의하고, 서브태스크들이 규율 있게
  실행되고 종료되도록 그 수명 주기 전체를 관리한다 (4장, p.138).[^rahman2025]

## fork가 하는 일

- 동시 작업을 시작하는 것은 스코프 소유자이고, 수단은 `fork()`다. 오버로드가 둘이다 — 값을
  돌려주는 서브태스크에는 `Callable`을 받는 판을 쓰고 그 `call()`이 새 가상 스레드에서 불린다.
  결과 없이 동작만 하는 서브태스크에는 `Runnable`을 받는 판을 쓰며, 성공해도
  `Subtask.get()`은 `null`을 돌려준다 (4장, p.138).[^rahman2025]
- 어느 쪽을 부르든 절차는 같다. 세 걸음이다 (4장, p.138):[^rahman2025]
  - 비동기 태스크를 나타내는 `Subtask` 객체가 만들어진다. 이 객체가 핸들 노릇을 한다.
  - 내부의 조이너(Joiner) 정책 객체에게 `onFork()`로 묻는다. **정책이 이 서브태스크를 돌리지
    않기로 판정하면**(예를 들어 스코프가 이미 취소되었다면) `fork()`는 핸들만 돌려주고 새 스레드는
    시작되지 않는다.
  - 그렇지 않으면 태스크를 실행할 새 가상 스레드가 시작된다.
- 그러니까 스레드를 띄울지 말지는 `fork` 자신이 아니라 조인 정책이 정한다. 그 정책이 무엇인지는
  [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md)에 있다.

## 핸들은 join 뒤에야 열린다

- `fork()`는 곧바로 `Subtask` 핸들을 돌려준다 (4장, p.138).[^rahman2025]
- 그러나 스코프 소유자가 그 핸들로 결과(`Subtask.get()`)나 예외(`Subtask.exception()`)를 꺼낼
  수 있는 것은 **`join()`으로 스코프를 조인한 뒤뿐이다** (4장, p.138).[^rahman2025] 이것이
  `Future`와 갈리는 자리다 — 거기서는 `get()`이 곧 기다림이었고 그 기다림이 태스크마다 따로였다
  ([Callable과 Future로 결과 받기](../concepts/callable-and-future-results.md)).

## 끝날 때 무엇이 알려지나

- 서브태스크가 일을 마치면 그것을 실행하던 스레드가 조이너의 `onComplete()`를 불러 알린다. 그때
  `Subtask` 핸들이 함께 넘어가고, 그 핸들은 최종 상태(`SUCCESS`·`UNAVAILABLE`·`FAILED` 같은
  것)를 담고 있다 (4장 §"Subtask completion", p.139).[^rahman2025]
- 스코프 소유자는 `join()`으로 서브태스크 정책이 만족될 때까지 기다린다.
  `StructuredTaskScope.open()`이 만드는 기본 스코프에서는 그것이 **모든 서브태스크가 성공하거나
  하나가 실패할 때까지**를 뜻한다 (4장, p.139).[^rahman2025]
- 서브태스크 하나가 실패하면 스코프가 아직 도는 다른 서브태스크들을 자동으로 취소하고, `join()`은
  실패한 서브태스크의 원래 예외를 감싼 `FailedException`을 던진다 (4장,
  p.139).[^rahman2025]

## 닫힐 때의 보장

- 마지막으로 스코프가 닫힐 때(명시적으로든 try-with-resources 블록을 빠져나가서든), 모든
  서브태스크 스레드가 종료될 때까지 기다린 뒤에야 부모 스레드가 진행하도록 보장한다 (4장,
  p.139).[^rahman2025]
- 그것이 자원 누수를 막고 동시 연산의 구조적 성질을 지키는 자리다 (4장, p.139).[^rahman2025]
  같은 보장이 없을 때 무엇이 새는지는
  [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md)에 있다.

## 이어지는 페이지

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 이 수명 주기를 노출하는
  API의 모양
- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — `onFork`와 `onComplete`가
  꽂히는 자리
- [Callable과 Future로 결과 받기](../concepts/callable-and-future-results.md) — 결과 핸들을
  다루던 앞선 방식
- [중첩 스코프](../concepts/nested-structured-scopes.md) — 이 수명 주기가 여러 층으로 겹칠 때
- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — `onFork`와 `onComplete`를
  직접 쓰는 자리
- [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md) — 여기서 시작되는 그 가상
  스레드를 무엇이 태우는가
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Scopes and Subtasks: Relationship
    and Lifecycle"(pp.138–139), 그 안의 "Forking subtasks"·"The fork process"·"Subtask
    completion". 이 절에는 예제 코드가 없어 옮긴 펜스도 없다.

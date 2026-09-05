---
type: synthesis
title: 자바의 구조적 동시성
description: 관련된 태스크를 하나의 일의 단위로 묶는 원칙과 자바가 그것을 구현한 StructuredTaskScope의 진입점 — 실행자와 Future에 태스크 위계가 없어 새던 자리, 스코프와 서브태스크가 fork에서 close까지 거치는 절차, join이 언제 끝나고 무엇을 돌려줄지를 정하는 조이너와 그 정책들, 조이너를 직접 만드는 확장점, 실패했을 때의 예외와 스레드·이름·타임아웃 구성, 그리고 이 구조가 낳는 메모리 일관성 보장과 중첩과 관측 가능성
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
---

# 자바의 구조적 동시성

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **여러 서브태스크를 갈라 놓은 뒤 그것들을 하나의 일로
묶어 다루는 방법**이 사는 자리다. 원칙 쪽과 자바 API 쪽이 함께 있고, API 쪽은
`StructuredTaskScope`와 그 조인 정책, 그것을 확장하고 구성하는 자리, 그리고 그 구조가 낳는 부수
효과(메모리 일관성, 중첩, 관측 가능성)가 전부다.

가상 스레드 하나가 무엇으로 만들어져 어떻게 도는가는 형제 허브인
[가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md)이 담당한다. 이 허브는
그 위에 얹히는 **프로그래밍 모델** 쪽이다 — 스코프 안의 서브태스크가 가상 스레드에서 돌지만, 여기서
묻는 것은 스레드가 아니라 태스크 사이의 관계다.

읽는 순서가 있다. 없을 때 무엇이 새는지를 먼저 보고, 그 결함에 답하는 원칙을 지나, 자바가 그것을
구현한 API와 절차를 밟고, 조인 정책들을 지나, 그 정책을 직접 만드는 확장점과 스코프를 손보는
구성으로 간 뒤, 마지막이 이 구조가 그냥 딸려 주는 것들이다.

## 무엇이 문제였나

- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 실행자와 `Future`에
  태스크 위계가 없어 취소가 전파되지 않는다는 것, 스레드 누수와 쓸모없어진 결과를 기다리는 낭비,
  그리고 스레드 덤프에 관계가 남지 않는다는 관측의 손실

## 원칙

- [구조적 동시성의 원칙](../concepts/structured-concurrency-principle.md) — 서브태스크의 수명을
  부모에 묶고 모두 같은 지점으로 돌아오게 한다는 규정, `goto`와의 유비, 그리고 그 제약이 낳는
  오류 전파와 누수 방지와 관측 가능성

## 자바가 내놓은 API

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — `StructuredTaskScope`의
  봉인 인터페이스와 `fork`·`join`·`close`, 정적 팩토리 `open`, 그리고 실패했을 때의
  `FailedException`
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — `fork`가 핸들을
  만들고 정책에게 물은 뒤에야 스레드를 띄운다는 절차, 결과를 `join` 뒤에만 꺼낼 수 있다는 제약,
  닫힐 때의 보장

## 조인 정책

- [조이너와 조인 정책](../concepts/structured-concurrency-joiner.md) — 결말 메서드 둘과 수명 주기
  훅 둘로 된 인터페이스, 자바가 내주는 다섯 가지 공통 정책, 그리고 고르는 기준
- [실패 즉시 중단 정책](../concepts/fail-fast-joining-policy.md) — 하나라도 실패하면 전부 접는 두
  정책과 실행자 대조군과 갈리는 실측
- [첫 성공으로 끝내는 경주](../concepts/racing-subtasks-for-first-result.md) — 가장 먼저 온 결과만
  쓰고 나머지를 인터럽트로 끊는 쪽
- [전부 기다리기와 부분 성공](../concepts/awaiting-all-subtasks-for-partial-success.md) — 실패를
  취소 신호로 삼지 않는 쪽과 연결마다 오류를 가두는 서버
- [allUntil로 만드는 중단 조건](../concepts/custom-stop-condition-with-alluntil.md) — 완료마다
  검사되는 술어로 취소 시점을 직접 정하는 쪽

## 정책을 직접 만드는 자리

- [커스텀 조이너의 계약](../concepts/custom-joiner-contract.md) — `Joiner`를 구현할 때의 계약,
  세 메서드가 불리는 시점, `boolean` 하나가 계속과 취소를 가른다는 것, 서브태스크의 세 최종 상태
- [결과를 보고 일찍 끝내는 커스텀 조이너](../concepts/early-completion-custom-joiners.md) —
  성공이 정족수에 닿거나 실패율이 문턱을 넘으면 남은 태스크를 접는 쪽
- [fork 시점의 시작 통제](../concepts/fork-time-admission-control.md) — 퍼밋으로 동시 실행을
  묶거나 바깥 조건이 거짓이면 새 태스크를 아예 시작시키지 않는 쪽

## 스코프를 손보는 자리

- [스코프 구성](../concepts/structured-task-scope-configuration.md) — 스레드 팩토리와 스코프
  이름과 타임아웃, 그리고 플랫폼 스레드로도 돌릴 수 있으나 그러면 원래 문제로 돌아간다는 것
- [구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md) — 실패가
  `FailedException`으로 감싸여 나온다는 규칙과 그것을 어디서 다룰지의 네 전략

## 이 구조가 딸려 주는 것

- [구조적 스코프의 메모리 일관성 효과](../concepts/structured-scope-memory-consistency.md) —
  `fork`와 `join`이 양방향으로 세우는 선 발생 관계와 그래도 남는 몫
- [중첩 스코프](../concepts/nested-structured-scopes.md) — 스코프 안의 스코프가 만드는 트리,
  위로 가는 오류와 아래로 가는 취소
- [구조가 드러나는 스레드 덤프](../concepts/structured-thread-dumps.md) — 그 위계가 JSON
  덤프에 스레드 컨테이너로 나오는 자리

## 경계에 있는 페이지

- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 원칙을 파이썬
  태스크 그룹 쪽에서 본 자리
- [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)
  — 이 구조 없이 결과를 모으던 방식
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 스코프가
  대신하는 수명 주기 관리
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 장의 예제 코드가 쓰는 JDK 25
  문법
- [공유 상태는 틀린 상태다](../concepts/shared-state-is-incorrect-state.md) — 서브태스크들이 함께
  쓰는 상태를 다룰 때의 규칙
- [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md) —
  스코프의 메모리 일관성 보장이 기대는 자바 메모리 모델 쪽 규칙
- [자바 세마포어와 퍼밋](../concepts/java-semaphore-permits.md) — 속도 제한 조이너가 쓰는 도구
- [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md) — 정족수 조이너가 빌려 온 개념
- [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md) — 스코프
  위계가 실리는 그 덤프를 뜨는 법

## 이어지는 허브

- [자바 동시 실행 모델](java-concurrent-execution-models.md) — 이 허브의 부모, 곧 자바가 일을
  동시에 시키려고 써 온 수단들의 계보
- [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md) — 이 스코프가 태우는
  스레드 쪽의 형제 허브
- [컨텍스트 전달과 스코프 값](context-propagation-and-scoped-values.md) — 이 스코프 안의
  서브태스크가 물려받는 값이 사는 형제 허브

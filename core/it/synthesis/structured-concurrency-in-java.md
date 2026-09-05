---
type: synthesis
title: 자바의 구조적 동시성
description: 관련된 태스크를 하나의 일의 단위로 묶는 원칙과 자바가 그것을 구현한 StructuredTaskScope의 진입점 — 실행자와 Future에 태스크 위계가 없어 새던 자리, 스코프와 서브태스크가 fork에서 close까지 거치는 절차, 그리고 join이 언제 끝나고 무엇을 돌려줄지를 정하는 조이너와 그 정책들
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
---

# 자바의 구조적 동시성

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **여러 서브태스크를 갈라 놓은 뒤 그것들을 하나의 일로
묶어 다루는 방법**이 사는 자리다. 원칙 쪽과 자바 API 쪽이 함께 있고, API 쪽은
`StructuredTaskScope`와 그 조인 정책이 전부다.

가상 스레드 하나가 무엇으로 만들어져 어떻게 도는가는 형제 허브인
[가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md)이 담당한다. 이 허브는
그 위에 얹히는 **프로그래밍 모델** 쪽이다 — 스코프 안의 서브태스크가 가상 스레드에서 돌지만, 여기서
묻는 것은 스레드가 아니라 태스크 사이의 관계다.

읽는 순서가 있다. 없을 때 무엇이 새는지를 먼저 보고, 그 결함에 답하는 원칙을 지나, 자바가 그것을
구현한 API와 절차를 밟은 뒤, 마지막이 조인 정책들이다.

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

## 이어지는 허브

- [자바 동시 실행 모델](java-concurrent-execution-models.md) — 이 허브의 부모, 곧 자바가 일을
  동시에 시키려고 써 온 수단들의 계보
- [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md) — 이 스코프가 태우는
  스레드 쪽의 형제 허브

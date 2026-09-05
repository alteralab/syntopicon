---
type: concept
title: 구조적 동시성의 원칙
description: 관련된 여러 태스크를 하나의 일의 단위로 다루고 서브태스크의 수명을 부모 태스크에 묶는다는 규정, 갈라진 서브태스크가 모두 부모 코드의 같은 지점으로 돌아와야 한다는 핵심 제약, goto와의 유비, 그리고 그 제약이 낳는 오류 전파와 누수 방지와 관측 가능성이라는 효과 — 언어에 매이지 않는 원칙 쪽
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T16:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 동시성의 원칙

- [무엇을 규정하는가](#무엇을-규정하는가)
- [하나의 출구](#하나의-출구)
- [goto와의 유비](#goto와의-유비)
- [그 제약이 낳는 것](#그-제약이-낳는-것)
- [경량 스레드와 함께 선다](#경량-스레드와-함께-선다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **동시에 도는 여러 태스크를 하나의 일로 묶는다는 것은 무엇을 요구하는가.**

이 페이지는 언어에 매이지 않는 원칙만 담는다. 자바가 그 원칙을 어떤 API로 구현하는지는
[구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md)가, 파이썬의 태스크 그룹
쪽은 [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md)가 갖는다.

## 무엇을 규정하는가

- 정의가 두 문장이다 (4장 도입, p.125):[^rahman2025]

> *Structured concurrency* is a paradigm that addresses these challenges by treating groups of
> related tasks as a single unit of work. It ensures that the lifecycles of subtasks are bound
> to the parent task, providing a transparent and manageable structure for concurrent execution.

- 그러니까 규정은 둘이다 — 관련된 태스크의 묶음을 **하나의 일의 단위**로 다루는 것, 그리고
  서브태스크(subtask)의 수명 주기를 **부모 태스크(parent task)에 묶는** 것 (4장 도입,
  p.125).[^rahman2025]
- 이 규정이 답하는 것은 태스크가 여러 스레드로 갈라져 흩어질 때 그 사이의 관계와 의존을 무엇이
  관리하는가라는 물음이다 (4장 도입, p.125).[^rahman2025] 그 관리가 없을 때 벌어지는 일이
  [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md)에 있다.

## 하나의 출구

- 핵심 원칙은 한 문장으로 적힌다 (4장 §"The Promise of Structured Concurrency",
  p.132):[^rahman2025]

> The core principle is straightforward: when a task spawns multiple concurrent subtasks, they
> must all return to the same point in the parent task's code.

- 저자가 붙이는 비유는 관리자와 팀이다 — 관리자가 팀원에게 일을 나눠 주면 모두가 보고를 마쳐야
  프로젝트가 끝난 것으로 친다 (4장, p.132).[^rahman2025]
- 그 모델에서 부모 태스크는 감독자 노릇을 한다. 서브태스크를 지켜보다가 완료를 기다리거나 문제가
  생기면 개입한다. 서브태스크는 성공했든 실패했든 예외 없이 부모에게 보고한 뒤에야 그 일이
  끝날 수 있다 (4장, p.132).[^rahman2025]

## goto와의 유비

- 저자가 비구조적 동시성을 옛날의 `goto` 문에 견준다 — `goto`를 쓰면 실행이 코드의 임의 지점으로
  뛰어 프로그램의 논리를 좇기 어려워지듯, 비구조적 동시성에서는 태스크나 스레드가 임의의 순서로
  실행되어 어느 시점의 프로그램 상태를 예측하기 어렵다 (4장 §"The Challenge of Unstructured
  Concurrency", p.132).[^rahman2025]
- 같은 유비를 파이썬 쪽 소스도 쓴다 — 태스크 그룹의 구조적 동시성을 구조적 프로그래밍에 견주는
  대목이
  [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md)의 "구조적 동시성"
  절에 원문 직인용으로 있다. **두 소스가 서로 독립으로 같은 유비에 닿는다.**

## 그 제약이 낳는 것

저자가 이 제약의 이득으로 네 가지를 든다 (4장, pp.132–133).[^rahman2025]

- **오류와 취소의 단일 창구** — 형제 관계인 태스크 묶음 전체에 대해 오류와 취소를 한 기제로
  다룬다. 서브태스크 하나가 오류를 만나거나 취소되면 형제 태스크들이 자동으로 종료되고, 오류는
  태스크 위계를 따라 위로 전파된다.
- **스레드 누수 방지** — 부모와 자식 사이의 엄격한 수명 주기를 강제하므로 태스크가 제 스코프보다
  오래 살아남을 수 없다. 부모가 완료 시점에 모든 서브태스크를 정리한다.
- **관측 가능성(observability)** — 태스크 사이의 의존 관계가 분명하게 드러나므로 스레드 덤프나
  프로파일러가 그 관계를 좇을 수 있고, 문제의 근본 원인을 더 빨리 찾게 된다.
- **선언적 스타일** — 스레드 관리의 세부 대신 태스크의 업무 논리에 집중하게 만든다.
- 저자는 같은 이득을 2장에서 먼저 적어 두었다 — 구조적 동시성은 더 선언적인 프로그래밍 스타일을
  북돋아, 스레드를 만들고 관리하거나 복잡한 취소 논리를 구현하는 낮은 수준의 세부 대신 개발자가 더
  높은 수준의 태스크에 집중하게 한다 (2장, p.51).[^rahman2025]

## 경량 스레드와 함께 선다

- 저자가 마지막 이득으로 꼽는 것이 결합이다 — 구조적 동시성은 대개 가상 스레드 위에서 돌고, 그
  조합이 수많은 동시 태스크를 적은 비용으로 만들 수 있게 한다. 구조적 동시성은 그 가상 스레드를
  안전하고 효율적으로 지휘하는 틀을 준다 (4장, p.133).[^rahman2025]
- 저자의 전망은 이 원칙이 자바 동시 프로그래밍의 기본 구성 요소가 되리라는 것이다 (4장,
  p.133).[^rahman2025]

## 이어지는 페이지

- [비구조적 동시성의 문제](../concepts/unstructured-concurrency-problems.md) — 이 원칙이 없을 때
  실제로 무엇이 새는가
- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 자바가 이 원칙을 구현한
  API
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 원칙을 파이썬
  태스크 그룹 쪽에서 본 자리
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — 장 도입(p.125), §"The Challenge of
    Unstructured Concurrency"(p.132), §"The Promise of Structured Concurrency"(pp.132–133);
    2장 "Understanding Virtual Threads" — "The Promise of Structured Concurrency"(p.51).

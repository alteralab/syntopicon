---
type: concept
title: 구조적 스코프의 메모리 일관성 효과
description: StructuredTaskScope가 fork와 join으로 세우는 선 발생 관계 — 갈라 놓기 전 소유자 스레드의 동작이 서브태스크에게 보이고 서브태스크의 동작이 결과 조회 시점에 보인다는 양방향 보장, 그 토대가 자바 언어 명세의 선 발생 규칙이라는 것, fork를 스레드 시작에 join을 Thread.join에 견주는 유비, 그리고 그렇다고 스레드 안전성을 무시해도 되는 것은 아니라는 단서
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 스코프의 메모리 일관성 효과

- [버전 조건](#버전-조건)
- [보장의 진술](#보장의-진술)
- [토대는 자바 언어 명세의 선 발생 규칙이다](#토대는-자바-언어-명세의-선-발생-규칙이다)
- [소유자에서 서브태스크로](#소유자에서-서브태스크로)
- [서브태스크에서 소유자로](#서브태스크에서-소유자로)
- [유비 — fork는 스레드 시작이고 join은 Thread.join이다](#유비--fork는-스레드-시작이고-join은-threadjoin이다)
- [그래도 남는 몫](#그래도-남는-몫)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프 소유자와 서브태스크가 함께 쓰는 데이터의 가시성을 무엇이 보장하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다. 이 보장을 진술하는 데 쓰인 메서드 이름은 이 소스가 쓰는 JDK 25 판의 것이고, 미리 보기
> 기능이라 정식화될 때 바뀔 수 있다. `stale_after`는 그 다음 릴리스(JDK 26, 2026년 3월)를 재심
> 시점으로 잡은 것이다. 아래 보장이 기대는 **선 발생(happens-before) 원칙 자체**는 이 미리 보기와
> 무관한 자바 언어 명세의 것이고, 그쪽은
> [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md)에
> 만료 없이 있다.

## 보장의 진술

- `StructuredTaskScope`는 스레드 사이에서 공유 데이터의 가시성을 따지기 쉽게 만드는, 명확하게
  정의된 메모리 일관성 보장을 준다 (4장 §"Memory Consistency Effects", p.202).[^rahman2025]
- 보장의 본문이 하나의 사슬이다 (4장, p.202):[^rahman2025]

  > Actions in the owner thread of a `StructuredTaskScope` prior to the forking of a subtask
  > happen before any actions taken by that subtask, which in turn happen before the subtask
  > result is retrieved.

- 그래서 얻는 것이 둘이다 — `fork()`를 부르기 전에 소유자 스레드가 한 데이터 변경이 서브태스크에게
  보이고, 서브태스크가 한 변경이 그 결과를 꺼낼 때 보인다 (4장, p.202).[^rahman2025]

## 토대는 자바 언어 명세의 선 발생 규칙이다

- 이 보장은 **자바 언어 명세 17장이 정의하는 자바의 기본적인 선 발생(happens-before) 관계 위에**
  선다. 그 규칙들이 스레드를 가로지르는 메모리 연산을 예측 가능하고 안전한 방식으로 일어나게
  한다 (4장, p.202).[^rahman2025] 이 KB에서 그 규칙들의 정본은
  [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md)이다.
- 저자가 그중 넷을 꼽는다 (4장, p.202):[^rahman2025] 한 스레드 안의 동작은 프로그램 순서대로
  실행되고, `synchronized` 블록은 모니터 연산을 통해 스레드 사이의 순서를 만들며, `volatile`
  변수는 잠금 없이 가시성을 보장하고, 스레드의 생성과 조인은 분명한 메모리 경계를 세운다.
- `java.util.concurrent` 패키지가 그 기본 규칙 위에 더 높은 수준의 보장을 얹는다 — 실행자에 태스크를
  제출하는 것, 동시성 컬렉션에 항목을 넣는 것, `Future` 결과를 꺼내는 것이 모두 선 발생 관계를
  세워 스레드 안전성을 확보한다 (4장, p.202).[^rahman2025]

## 소유자에서 서브태스크로

- 저자가 꾸민 상황은 여러 시스템의 설정을 동시에 검증하는 설정 서비스다. 소유자 스레드가 갈라 놓기
  전에 공유 상태를 준비하고, 서브태스크들이 그것을 읽는다 (4장, pp.202–203).[^rahman2025]

  ```java
  public void demonstrateMemoryConsistency() throws InterruptedException {
    configuration = "production-config";
    cache.put("database-url", "prod.example.com");

    try (var scope = open(StructuredTaskScope.Joiner
        .<String>allSuccessfulOrThrow())) {

      var configTask = scope.fork(() -> "Config: " + configuration);
      var cacheTask = scope.fork(() -> "Connected to: " + cache.get("database-url"));

      var results = scope.join()
          .map(StructuredTaskScope.Subtask::get)
          .toList();
    }
  }
  ```

- 저자가 이 흐름에서 짚는 것이 다섯이다 (4장, pp.203–204):[^rahman2025] 소유자 스레드가 서브태스크를
  만들기 전에 공유 상태를 준비하고, `fork()`를 부르는 순간 프레임워크가 선 발생 관계를 세워 그
  준비가 서브태스크에게 보이게 하며, 그래서 **우리 쪽에서 아무 추가 동기화 없이** 두 서브태스크가
  바뀐 설정과 캐시 내용을 확실히 볼 수 있고, `join()`이 이번에는 서브태스크에서 소유자 쪽으로 또
  하나의 선 발생 간선을 만들며, 소유자 스레드가 최신이고 일관된 결과를 받는다.

## 서브태스크에서 소유자로

- 보장은 양방향이다 — 서브태스크가 공유 상태를 고치면 그 변경이 조인 연산이 끝난 뒤 소유자
  스레드에게 보인다 (4장, p.204).[^rahman2025]
- 저자의 둘째 예제가 그것을 보인다 — `ConcurrentHashMap`과 `AtomicInteger`를 만들고 두 작업자
  서브태스크가 각각 항목을 넣고 카운터를 올린 뒤, `join()` 다음에 소유자 스레드가 카운터와 맵의
  최종 상태를 본다 (4장, p.204).[^rahman2025]
- 짚는 것이 여럿이다 (4장, p.204):[^rahman2025] 스레드 안전한 그릇을 먼저 만들고, 두 작업자는 어떤
  순서로든 실행될 수 있으나 둘 다 그 그릇을 안전하게 갱신하며, 원자적 카운터가 서로 다른 스레드의
  증가가 서로를 방해하지 않게 해 고전적인 **갱신 손실(lost update)** 문제를 막고, `join()`이 모든
  작업자의 수정을 소유자에게 보이게 만든다.

## 유비 — fork는 스레드 시작이고 join은 Thread.join이다

- 저자가 이 보장을 이미 검증된 기제로 환원한다 — 서브태스크를 갈라 놓는 것은 **스레드를 시작하는
  것과 비슷해서** 소유자 스레드의 앞선 동작을 모두 서브태스크에게 보이게 하는 선 발생 간선을
  만들고, 조인하는 것은 **`Thread.join()`을 부르는 것과 같아서** 서브태스크의 모든 동작을 소유자
  스레드에게 보이게 하는 선 발생 관계를 세운다 (4장, p.205).[^rahman2025]
- 그 유비가 가리키는 두 규칙이 KB에 이미 있다 —
  [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md)의
  **스레드 시작 규칙**(`start()`는 그 스레드의 어떤 작업보다도 선 발생한다)과 **스레드 종료
  규칙**(스레드의 모든 작업은 그 종료 감지보다 선 발생하고, 감지 수단이 `Thread::join()`이다)이다.
- `java.util.concurrent`의 동시성 컬렉션이 그 보장을 한 단계 더 넓힌다 — `ConcurrentHashMap`에
  넣거나 `AtomicInteger`를 올리는 연산이 스레드 사이에서 안전하게 보이도록 보장한다 (4장,
  p.205).[^rahman2025]

## 그래도 남는 몫

- 저자가 꼽는 소득은 자동성이다 — 이 메모리 일관성이 자동으로 처리되므로 개발자는 동시 연산의
  업무 논리에 집중할 수 있고, `fork`와 `join` 연산이 필요한 메모리 배리어(barrier)가 갖춰지는
  분명한 동기화 지점이 되어 준다 (4장, p.205).[^rahman2025]
- **그렇다고 스레드 안전성을 통째로 무시해도 된다는 뜻은 아니다** — 여러 서브태스크가 공유 상태를
  고칠 때는 여전히 알맞은 동시성 컬렉션과 원자적 연산을 써야 한다 (4장, p.205).[^rahman2025]
  공유 상태 자체를 줄이라는 더 앞선 규칙은
  [공유 상태는 틀린 상태다](../concepts/shared-state-is-incorrect-state.md)에 있다.

## 이어지는 페이지

- [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md) —
  이 보장이 기대는 선 발생 규칙 여덟 가지
- [자바 메모리 모델](../concepts/java-memory-model.md) — 그 규칙들이 놓인 모델
- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 이 보장을 내는 API
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — `fork`와
  `join`이 실제로 하는 일
- [공유 상태는 틀린 상태다](../concepts/shared-state-is-incorrect-state.md) — 보장이 있어도
  공유 상태에 남는 몫
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Memory Consistency
    Effects"(pp.202–205), 그 안의 곁글 "Memory Consistency Properties"(p.202). 보장의 진술은
    p.202를 원문 그대로 인용했다 — 이 KB의 규약이 정의를 번역하지 않고 직인용하도록 한다.
    인용한 코드는 p.203의 `MemoryConsistencyDemo.demonstrateMemoryConsistency`이고, 조판
    줄바꿈을 폈으며 원문 주석 두 줄과 `log` 호출 네 줄, 캐시 항목 한 줄을 깎았다 — 소유자가 먼저
    쓰고 서브태스크가 읽는 뼈대만 남겼다. 개념당 대표 코드 하나 규칙에 따라 남긴 것:
    필드 선언과 `demonstrateSubtaskUpdates` 전문(pp.203–204). 이 절에는 실행 출력이 실려
    있지 않다. 저자가 인용한 명세는 "Java Language Specification" 17장이다.

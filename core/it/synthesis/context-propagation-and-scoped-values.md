---
type: synthesis
title: 컨텍스트 전달과 스코프 값
description: 호출 사슬을 따라 문맥 데이터를 넘기는 문제의 진입점 — 문맥 객체를 인자로 끌고 다닐 때 무너지는 것들, 그것을 감추려고 프레임워크들이 쓰는 ThreadLocal 패턴과 그 API가 남기는 세 결함, 그리고 JDK 25에서 정식이 된 ScopedValue의 API와 동적 스코프, 리바인딩, 구조적 동시성에서의 상속, 옮길 때 확인할 것
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
---

# 컨텍스트 전달과 스코프 값

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **호출 사슬을 따라 문맥 데이터를 넘기는 문제**가 사는
자리다. 문제 쪽(인자로 끌고 다니기, `ThreadLocal`)과 답 쪽(`ScopedValue`)이 함께 있고, 그 둘을
잇는 축은 "값이 어디까지 살아 있어야 하는가"다.

스레드 하나가 무엇으로 만들어져 어떻게 도는가는 형제 허브인
[가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md)이, 서브태스크들을 하나의
일로 묶는 방법은 [자바의 구조적 동시성](structured-concurrency-in-java.md)이 담당한다. 이 허브는
그 둘 어느 쪽에도 속하지 않는다 — 스코프 값은 구조적 동시성 없이도 쓰고, 가상 스레드 없이도 쓴다.
다만 두 허브와 각각 맞닿는 자리가 하나씩 있고 아래에 링크로 두었다.

읽는 순서가 있다. 문제를 먼저 보고, 지금까지 쓰던 답과 그 값을 지나, 새 API의 모양과 수명 규칙을
밟은 뒤, 마지막이 쓰임과 이전이다.

## 문제

- [문맥을 넘겨 다니는 부담](../concepts/context-passing-burden.md) — 프레임워크의 문맥 객체를
  인자로 꿰어 넘길 때 생기는 매개변수 오염과 인터페이스의 취약성, 그리고 결합이 테스트에 물리는 값

## 지금까지 쓰던 답

- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md)
  — 문맥을 스레드에 붙여 두고 필요한 자리에서 꺼내는 방법과 `finally`에서 반드시 지워야 하는 이유
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 무제한 가변성, 풀에서
  재사용되는 스레드로 값이 새는 무제한 수명, 그리고 자식 스레드 상속의 비용

## 새 API의 모양

- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 암묵적 매개변수로
  동작한다는 정의와 세 성질, `newInstance`와 `where`와 `run`과 `call`, 값을 읽는 네 방법
- [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md) — 렉시컬 스코프가 아니라
  실행 흐름이 정하는 범위, 그리고 새로 만든 스레드는 바인딩을 물려받지 않는다는 것
- [중첩 스코프에서의 리바인딩](../concepts/scoped-value-rebinding.md) — 안쪽 스코프에서 값을 잠시
  덮고 나올 때 자동으로 되돌아오는 성질과 그리기 문맥이라는 실물

## 무엇에 쓰는가

- [구조적 동시성에서의 스코프 값 상속](../concepts/scoped-value-with-structured-concurrency.md) —
  상속되지 않는다는 규칙이 `StructuredTaskScope` 안에서만 뒤집히는 자리
- [재귀 감지와 평탄화 트랜잭션](../concepts/scoped-value-recursion-detection.md) — 바인딩의 유무를
  검사로 쓰고 리바인딩을 카운터로 쓰는 두 쓰임

## 옮길 것인가

- [ScopedValue가 ThreadLocal보다 나은 이유](../concepts/scoped-value-vs-thread-local.md) — 저자가
  드는 성능 이유 둘과 사용성 이유 다섯, 그리고 수치가 실려 있지 않다는 사실
- [ThreadLocal에서 스코프 값으로 옮기기](../concepts/migrating-from-thread-local-to-scoped-values.md)
  — 확인할 다섯 가지와 정식화의 뜻, 그리고 같은 장 안에서 어긋나는 문장

## 경계에 있는 페이지

- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 같은 결함이
  수백만 스레드 규모에서 갖는 무게. 그쪽은 가상 스레드 허브가 담당한다
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 스레드 로컬 저장소를
  동기화가 필요 없는 갈래로 보는 개념 층과 `ThreadLocalMap`의 구현 내부
- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 상속이 일어나는 그 스코프
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 실제 코드에서 `ThreadLocal`
  쓰임을 찾아내는 플래그
- [공유 상태는 틀린 상태다](../concepts/shared-state-is-incorrect-state.md) — 나누는 것을 줄이라는
  같은 결의 조언
- [모듈 임포트 선언](../concepts/module-import-declaration.md) — 이 책의 예제가 쓰는 JDK 25 문법

## 이어지는 허브

- [자바 동시 실행 모델](java-concurrent-execution-models.md) — 이 허브의 부모, 곧 자바가 일을
  동시에 시키려고 써 온 수단들의 계보
- [자바의 구조적 동시성](structured-concurrency-in-java.md) — 스코프 값이 서브태스크로 내려가는
  형제 허브
- [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md) — 이 문제가 규모에서
  다시 나타나는 형제 허브

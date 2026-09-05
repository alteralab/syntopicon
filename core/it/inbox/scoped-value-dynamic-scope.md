---
type: concept
title: 동적 스코프와 바인딩의 수명
description: ScopedValue의 바인딩이 run 호출의 동적 스코프 안에서만 살아 있고 그 밖에서는 자동으로 풀린다는 것, 자바의 렉시컬 스코프와 갈리는 자리, isBound로 그것을 검사하는 법, 그리고 새로 만든 스레드는 플랫폼이든 가상이든 바인딩을 물려받지 않는다는 것
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 동적 스코프와 바인딩의 수명

- [버전 조건](#버전-조건)
- [먼저 묶어야 읽을 수 있다](#먼저-묶어야-읽을-수-있다)
- [같은 태스크를 스코프 밖에서 다시 돌리면](#같은-태스크를-스코프-밖에서-다시-돌리면)
- [렉시컬 스코프가 아니라 동적 스코프다](#렉시컬-스코프가-아니라-동적-스코프다)
- [새 스레드는 물려받지 않는다](#새-스레드는-물려받지-않는다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`ScopedValue`의 바인딩은 정확히 어디까지 살아 있는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다 (5장, pp.217·226).[^rahman2025] 만료일은 달지
> 않는다 — 정식 API라 다음 릴리스를 재심 시점으로 잡을 근거가 없다.

## 먼저 묶어야 읽을 수 있다

- 순서가 강제된다 — `ScopedValue`는 유한한 수명을 가지므로 먼저 설정해야 하고, 그러고 나서야
  쓸 수 있다 (5장 §"Running ScopedValue", p.228).[^rahman2025]
- 검사 수단이 `isBound()`다. 바인딩하지 않은 채로 태스크를 실행하면 바인딩이 없다는 쪽으로
  갈린다 (5장, pp.228–229).[^rahman2025]
- `where()`로 값을 묶고 `run()`에 태스크를 넘기면 그 태스크는 바인딩된 값을 본다 (5장,
  p.229).[^rahman2025]

## 같은 태스크를 스코프 밖에서 다시 돌리면

- 저자가 직접 묻고 실험한다 — `where().run()`으로 값을 설정한 뒤에 태스크를 따로 실행해 값을
  얻을 수 있는가 (5장, p.229).[^rahman2025]
- 같은 `Runnable`을 두 번 실행하면 첫 번째는 바인딩된 문맥 안에서 돌고 두 번째는 그 스코프 밖에서
  돌아 값이 더 이상 묶여 있지 않다 (5장, p.230).[^rahman2025]
- 규칙이 이렇게 정리된다 — `ScopedValue`는 `run()` 메서드 호출의 **동적 스코프(dynamic scope)**
  안에서만 묶인 채로 남는다. 그 메서드가 끝나면 바인딩이 자동으로 제거되어, 스코프 경계가 깨끗하게
  유지되고 서로 무관한 코드 구역 사이로 값이 새는 일이 막힌다 (5장, p.230).[^rahman2025]
- 이것이 `ThreadLocal`의 `finally`에서 손수 `remove()`를 부르던 자리를 대신한다. 지우는 일이
  사람의 기억에서 언어의 규칙으로 옮겨 간 것이다.

## 렉시컬 스코프가 아니라 동적 스코프다

- 저자가 두 스코프를 가른다 — 값의 "스코프"는 그 값이 존재하고 접근될 수 있는 범위를 말한다.
  자바에서 이것은 흔히 `{}` 블록으로 정의되는 **렉시컬 스코프(lexical scope)**를 가리키고, 변수는
  선언된 경계 안에서만 접근된다 (5장, p.230).[^rahman2025]
- 그러나 `ScopedValue`는 프로그램의 **실행 흐름(execution flow)**으로 결정되는 동적 스코프에서
  동작한다 (5장, p.230).[^rahman2025]
- 동적 스코프의 뜻이 호출 관계로 설명된다 — 값은 특정 메서드가 실행되는 동안, 그리고 그 메서드가
  직접이든 간접이든 호출하는 메서드들에서 접근 가능하다. a가 b를 부르고 b가 c를 부르면 스코프는
  c까지 흐르고 c가 끝나면 끝난다 (5장, p.230).[^rahman2025]
- 저자가 이 성질에서 결론을 낸다 — 이 일시적이고 정밀한 스코프 관리가 `ScopedValue`를
  `ThreadLocal`보다 깔끔하고 안전한 대안으로 만든다. 문맥 데이터를 넘길 때 특히 그렇다 (5장,
  p.230).[^rahman2025]

## 새 스레드는 물려받지 않는다

- 저자가 다시 묻는다 — 메인 스레드 말고 다른 스레드에서 태스크를 돌리면 어떻게 되는가 (5장,
  p.230).[^rahman2025]
- 결과가 직관에 어긋난다. 시작하지 않은 플랫폼 스레드를 만들어 두고 바인딩된 스코프 안에서
  `thread::start`를 실행해도 태스크는 바인딩을 보지 못한다 (5장, pp.230–231).[^rahman2025]

  ```java
  Thread thread = Thread.ofPlatform().unstarted(task);
  ScopedValue.where(NAME, "Bazlur")
             .run(thread::start);
  thread.join();
  ```

- 이유가 명시된다 — 스코프 값은 **새로 만들어진 스레드에 자동으로 상속되지 않는다.**
  `thread::start`가 값이 묶인 스코프 안에서 실행되더라도 실제 태스크는 그 바인딩을 물려받지 않는
  별개의 스레드에서 돈다 (5장, p.231).[^rahman2025]
- 범위가 넓다 — 이 동작은 플랫폼 스레드와 가상 스레드 모두에서 같다 (5장, p.231).[^rahman2025]
- 푸는 방법은 바인딩을 새 스레드 안으로 옮기는 것이다. 가상 스레드를 시작한 뒤 그 안에서
  `ScopedValue.where(NAME, "Bazlur").run(task)`를 부르면 기대대로 동작한다 (5장,
  p.231).[^rahman2025]
- 이 한계에 예외가 하나 있고 그것이 다음 페이지다 —
  [구조적 동시성에서의 스코프 값 상속](../concepts/scoped-value-with-structured-concurrency.md)에서는
  서브태스크가 바인딩을 물려받는다.

## 이어지는 페이지

- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — `where`와 `run`과 `call`의
  전반
- [구조적 동시성에서의 스코프 값 상속](../concepts/scoped-value-with-structured-concurrency.md) — 상속되지
  않는다는 이 규칙이 뒤집히는 유일한 자리
- [중첩 스코프에서의 리바인딩](../concepts/scoped-value-rebinding.md) — 스코프 안에 스코프를 여는 쪽
- [재귀 감지와 평탄화 트랜잭션](../concepts/scoped-value-recursion-detection.md) — `isBound()`를 검사로
  쓰는 쓰임
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 여기서 해결되는 무제한 수명
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Running ScopedValue"(pp.228–231),
    그리고 버전 조건의 근거는 장 도입부(p.217)와 §"Core Components of ScopedValue"의
    곁글(p.226). 개념당 대표 코드 하나 규칙에 따라 플랫폼 스레드 예제의 핵심 세 줄만 실었고,
    `isBound()`를 검사하는 `Runnable task` 선언(pp.228–231에서 네 번 되풀이된다), 스코프 안팎에서
    두 번 실행하는 예제(p.229), 가상 스레드 안에서 바인딩하는 고친 판(p.231)은 미수록이다 —
    각 예제의 출력과 결말은 본문에 옮겼다.

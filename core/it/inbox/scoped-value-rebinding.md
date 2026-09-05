---
type: concept
title: 중첩 스코프에서의 리바인딩
description: 같은 ScopedValue에 안쪽 스코프에서 다른 값을 잠시 주고 그 스코프가 끝나면 바깥 값이 자동으로 복원된다는 성질, 그것이 쓸모 있는 세 자리, 그리고 저자가 드는 그리기 문맥 예제에서 구성 요소 위계가 색과 선 굵기를 겹쳐 쓰는 방식
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 중첩 스코프에서의 리바인딩

- [버전 조건](#버전-조건)
- [리바인딩이란 무엇인가](#리바인딩이란-무엇인가)
- [쓸모 있는 세 자리](#쓸모-있는-세-자리)
- [역할을 잠시 바꾸는 예제](#역할을-잠시-바꾸는-예제)
- [그리기 문맥이라는 실물](#그리기-문맥이라는-실물)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **같은 `ScopedValue`에 안쪽 스코프에서 다른 값을 줄 수 있는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다 (5장, pp.217·226).[^rahman2025] 만료일은 달지
> 않는다 — 정식 API라 다음 릴리스를 재심 시점으로 잡을 근거가 없다.

## 리바인딩이란 무엇인가

- 저자가 이것을 `ScopedValue`의 강력한 기능 가운데 하나로 든다 — 중첩 스코프 안에서
  **리바인딩(rebind)**할 수 있다는 것이다 (5장 §"Rebinding ScopedValue in nested scopes",
  p.233).[^rahman2025]
- 리바인딩이 하는 일은 같은 `ScopedValue`에 새 값을 한정된 기간 동안, 특정 하위 스코프에 국한해
  배정하는 것이다 (5장, p.233).[^rahman2025]
- 되돌림이 자동이다 — 하위 스코프가 끝나면 원래 값이 자동으로 복원되고, 그래서 문맥 관리가
  깔끔하고 예측 가능해진다 (5장, p.233).[^rahman2025]
- 불변성과 어긋나지 않는다. 한 바인딩 안에서 값이 바뀌는 것이 아니라 안쪽에 새 바인딩이 하나 더
  서는 것이고, 그 성질은
  [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md)의 유한한 수명 그대로다.

## 쓸모 있는 세 자리

저자가 리바인딩이 특히 값진 상황을 셋 든다 (5장, pp.233–234).[^rahman2025]

- 역할 기반 접근 제어 — 특정 작업 동안 사용자의 역할을 임시로 바꿀 수 있다.
- 문맥에 민감한 설정 — 더 넓은 문맥에 영향을 주지 않고 특정 실행 흐름에만 설정을 조정하게 해 준다.
- 태스크별 재정의 — 특정 태스크나 동작에 임시 데이터를 줄 수 있다.

## 역할을 잠시 바꾸는 예제

- 바깥에서 역할을 `Admin`으로 묶고, 안쪽 스코프에서 `Guest`로 리바인딩하고, 그 스코프를 빠져나오면
  `Admin`이 돌아온다 (5장, p.234).[^rahman2025]

  ```java
  ScopedValue.where(USER_ROLE, "Admin").run(() -> {
      System.out.println("Outer scope: User role is " + USER_ROLE.get());
      performTask();

      ScopedValue.where(USER_ROLE, "Guest").run(() -> {
          System.out.println("Inner scope: User role is " + USER_ROLE.get());
          performTask();
      });

      System.out.println("Back to outer scope: User role is " + USER_ROLE.get());
      performTask();
  });
  ```

- 저자가 예제에서 짚는 핵심 넷 가운데 마지막이 이 구조의 값이다 — **같은 메서드가 현재 스코프에
  따라 서로 다른 값에 접근한다** (5장, p.234).[^rahman2025] `performTask()`는 자기가 어느
  역할로 도는지 인자로 받지 않는다.
- 실행 결과가 그 순서를 그대로 보인다 — 바깥에서 `Admin`, 안쪽에서 `Guest`, 다시 바깥으로
  나오면 `Admin`이다 (5장, p.234).[^rahman2025]

## 그리기 문맥이라는 실물

- 저자가 드는 또 하나의 자리가 그래픽이다 — 프로그램의 여러 부분이 나눠 써야 하는 그리기 문맥이
  있는 경우가 흔하고, `ScopedValue`는 자동 정리와 재진입성 덕분에 스레드 로컬 변수보다 이 자리에
  더 알맞다 (5장, p.241).[^rahman2025]
- 전통적 방식의 값도 적혀 있다 — 스레드 로컬 변수를 쓰는 방식은 손수 정리해 줘야 하고 문맥
  누출에 취약하다 (5장, p.241).[^rahman2025]
- 예제는 색과 선 굵기를 `ScopedValue` 둘로 두고 UI 구성 요소 위계에서 겹쳐 쓴다. 패널이 회색
  테마를 세우고, 그 안의 버튼이 파란색과 3픽셀 선 굵기로 자기 문맥을 세우며, 버튼 안의 텍스트가
  다시 흰색과 1픽셀로 덮는다 (5장, pp.242–243).[^rahman2025]
- 되돌림이 층마다 일어난다 — 텍스트 스코프가 끝나면 버튼의 파란색 문맥이 자동으로 복원되고,
  자식들을 다 그리고 나면 패널의 문맥이 그대로 남아 있다 (5장, p.243).[^rahman2025]
- 바깥에도 층이 있다 — 애플리케이션 전체의 기본 그리기 문맥을 세워 두면 패널이 끝난 뒤 손댈 것
  없이 메인 문맥으로 돌아오고, 어떤 스코프 밖에서 하는 연산은 알맞은 기본값으로 떨어진다 (5장,
  p.244).[^rahman2025]
- 기본값으로 떨어지는 자리는 `isBound()` 검사가 맡는다 — 문맥이 세워지지 않았을 때 대비값을
  갖게 해 준다 (5장, p.242).[^rahman2025]

## 이어지는 페이지

- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — `where`와 `run`의 전반
- [동적 스코프와 바인딩의 수명](../concepts/scoped-value-dynamic-scope.md) — 안쪽 바인딩이 왜 자동으로
  풀리는가
- [재귀 감지와 평탄화 트랜잭션](../concepts/scoped-value-recursion-detection.md) — 리바인딩을 카운터로 쓰는
  쓰임
- [중첩 스코프](../concepts/nested-structured-scopes.md) — 같은 "중첩"이라는 말이 구조적 동시성 쪽에서
  가리키는 다른 것
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Rebinding ScopedValue in nested
    scopes"(pp.233–234), 그리고 §"Migrating to Scoped Values" 안의 그래픽 예제(pp.241–244).
    개념당 대표 코드 하나 규칙에 따라 역할 리바인딩 예제의 `main` 본체만 실었고, 그 클래스의
    필드 선언과 `performTask`(p.234), `SimpleGraphicsExample`의 `drawLine`·`drawRectangle`·
    `drawButton`·`drawPanel`·`main` 전문(pp.241–244)과 그 실행 출력(p.244)은 미수록이다 —
    출력에서 읽히는 문맥 전환의 순서는 본문에 옮겼다.

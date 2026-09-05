---
type: concept
title: ScopedValue가 ThreadLocal보다 나은 이유
description: 저자가 드는 성능 이점 둘(가상 스레드마다 복사본을 두지 않는 부담 감소, 가상 스레드와 구조적 동시성에 맞춘 최적화)과 사용성 이점 다섯(불변성 강제, API로 드러나는 수명, 간결한 표기, 권한 객체로서의 접근 통제, 바인딩 없음과 null을 가르는 오류 처리)
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ScopedValue가 ThreadLocal보다 나은 이유

- [버전 조건](#버전-조건)
- [성능 쪽 이유 둘](#성능-쪽-이유-둘)
- [수치는 실려 있지 않다](#수치는-실려-있지-않다)
- [사용성 쪽 이유 다섯](#사용성-쪽-이유-다섯)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`ScopedValue`로 갈아탈 때 실제로 무엇이 나아지는가.**

## 버전 조건

> **버전 조건**: JDK 25 이상에서 정식 API다. JDK 21부터 24까지는 미리 보기(preview) 기능이라
> 컴파일과 실행에 `--enable-preview`가 필요하다 (5장, pp.217·226).[^rahman2025] 만료일은 달지
> 않는다 — 정식 API라 다음 릴리스를 재심 시점으로 잡을 근거가 없다.

## 성능 쪽 이유 둘

- 총평이 조건부다 — `ScopedValue`는 **특히 가상 스레드와 함께 쓸 때** `ThreadLocal`보다 대체로
  나은 성능을 보인다 (5장 §"Performance Considerations", p.236).[^rahman2025]
- 첫째, 부담이 준다 — `ThreadLocal` 변수는 가상 스레드마다 자기 복사본이 필요할 때 상당한 부담을
  들이고 그것이 메모리 소비를 밀어 올린다. 반면 `ScopedValue`는 정해진 스코프 안의 스레드들이
  데이터를 나눠 쓰게 해 메모리 사용을 최소화하고 성능을 끌어올린다 (5장,
  p.236).[^rahman2025]
- 둘째, 대상에 맞춰 최적화되어 있다 — `ScopedValue`는 가상 스레드와 구조적 동시성에 맞게
  최적화되었고, 가상 스레드의 가벼운 성질을 활용해 전통적인 스레드 로컬 변수의 병목 없이 효율적인
  데이터 공유를 제공한다 (5장, p.236).[^rahman2025]
- 저자가 드는 그림이 웹 서버다 — 동시 요청을 처리하려고 가상 스레드 수천 개를 띄우는 서버에서 각
  요청이 사용자 인증 정보 같은 문맥 데이터를 필요로 할 때, 그 데이터를 요청마다의 스코프 안에서
  `ScopedValue`로 나누면 `ThreadLocal`을 쓸 때보다 메모리 소비가 크게 줄고 전체 처리량이 오른다
  (5장, p.236).[^rahman2025]

## 수치는 실려 있지 않다

- 이 절에는 벤치마크도 측정값도 없다. 저자가 드는 것은 기제의 설명과 방향뿐이고, 얼마나 줄고
  얼마나 오르는지는 적히지 않는다 (5장, p.236).[^rahman2025]
- 그래서 이 KB는 이 절에서 수치를 만들지 않는다. 같은 소스가 수치를 실은 자리는 2장의
  `ThreadLocal` 힙 사용량 실측이고, 그것은
  [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md)에 있다.

## 사용성 쪽 이유 다섯

저자가 성능 말고도 `ScopedValue`를 더 나은 대안으로 만드는 것들을 든다 (5장 §"Usability and API
Design", pp.236–237).[^rahman2025]

- 불변성을 강제한다 — 한 스코프 안에서 값이 `ScopedValue`에 결합되고 나면 수정할 수 없다. 이
  불변성이 코드를 이해하기 쉽게 만들고 의도치 않은 수정으로 생기는 오류 위험을 줄인다. 동시
  환경에서 특히 쓸모 있다. 여러 스레드가 공유 변수를 고치려 할 때 흔히 생기는 경쟁 상태와 데이터
  불일치를 막기 때문이다 (5장, p.236).[^rahman2025]
- 공유 데이터의 수명을 API 설계로 명시한다 — `run()` 메서드가 값에 접근할 수 있는 스코프를 분명히
  표시한다. 이 명시적 수명이 가독성을 높이고 데이터가 프로그램 안에서 어떻게 흐르는지 이해하기
  쉽게 한다. `ThreadLocal`의 암묵적 동작과 달리 값이 유효한 경계를 분명하게 만든다 (5장,
  p.236).[^rahman2025]
- API가 더 간결하고 직관적이다 — `where()`와 `run()`이 특정 스코프 안에서 공유 데이터를 설정하고
  접근하는 구조적인 방법을 준다. 장황하고 덜 직관적인 `ThreadLocal`의 방식에 견주면 더 자연스럽고
  다루기 쉽게 느껴진다 (5장, p.236).[^rahman2025]
- **권한 객체(capability object)**로 동작한다 — 누가 공유 데이터에 접근할 수 있는지 정밀하게
  통제할 수 있다. `ScopedValue` 객체를 `private` 같은 접근 지정자로 선언하면 권한이 있는 구성
  요소만 접근하도록 제한할 수 있어, 설계에 보안과 캡슐화의 층이 더해진다 (5장,
  p.236).[^rahman2025]
- null 값을 더 명시적으로 다룬다 — `ThreadLocal`은 값을 명시적으로 `null`로 설정했든 아예 설정하지
  않았든 `get()`이 `null`을 돌려주어 미묘한 버그로 이어질 수 있다. `ScopedValue`는 이 둘을 분명히
  가른다. 값이 묶여 있지 않은 상태에서 `get()`을 부르면 `NoSuchElementException`을 던져, 값을
  설정하지 않은 실수가 일찍 잡히고 코드가 더 견고하고 예측 가능해진다 (5장,
  p.237).[^rahman2025]
- 다섯 가운데 앞의 둘이
  [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md)의 무제한 가변성과 무제한 수명에
  하나씩 맞물린다. 셋째 결함인 상속의 비용에 답하는 것은 성능 쪽 첫째 항목이다.

## 이어지는 페이지

- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 여기 나열된 이점들이 답하는 결함
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 같은 소스가 수치를 실은
  자리
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 여기서 말하는 `where`와
  `run`의 전반
- [ThreadLocal에서 스코프 값으로 옮기기](../concepts/migrating-from-thread-local-to-scoped-values.md) — 이
  이점들을 실제로 취할 때 확인할 것
- [구조적 동시성에서의 스코프 값 상속](../concepts/scoped-value-with-structured-concurrency.md) — 성능 이유
  둘째가 기대는 자리
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Performance Considerations"(p.236),
    §"Usability and API Design"(pp.236–237). 두 절에는 코드가 실려 있지 않아 이 페이지에는
    코드 펜스가 없다. 두 절 어디에도 측정값이나 벤치마크가 없다는 사실은 본문에 절을 두어
    적었다.

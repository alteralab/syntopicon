---
type: concept
title: ThreadLocal의 설계 결함 셋
description: get을 부를 수 있는 코드는 set도 부를 수 있다는 무제한 가변성, 명시적으로 지우지 않으면 스레드 수명만큼 남아 풀에서 재사용되는 스레드로 값이 새는 무제한 수명, 그리고 자식 스레드가 값을 물려받는 InheritableThreadLocal의 비용 — 그리고 마지막 항목에서 저자의 본문과 주석이 어긋나는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ThreadLocal의 설계 결함 셋

- [결함은 태생적이다](#결함은-태생적이다)
- [첫째, 무제한 가변성](#첫째-무제한-가변성)
- [둘째, 무제한 수명](#둘째-무제한-수명)
- [셋째, 상속의 비용](#셋째-상속의-비용)
- [본문과 주석이 어긋나는 자리](#본문과-주석이-어긋나는-자리)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`ThreadLocal`이 문맥 전달을 풀어 주는 대신 무엇을 값으로 남기는가.**

이 페이지의 서술에는 버전 조건이 없다. 아래 셋은 `ThreadLocal` API 자체의 성질이라 릴리스에
묶이지 않는다.

## 결함은 태생적이다

- 저자가 절을 여는 판정이 강하다 — 코드에 `ThreadLocal`이 있는 것이 영리하고 쓸모 있어 보이지만
  `ThreadLocal` 변수에는 태생적인 설계 결함이 여럿 있다 (5장 §"Limitations of ThreadLocal
  Variables", p.222).[^rahman2025]
- 결함이라는 말이 중요하다. 잘못 쓴 결과가 아니라 API가 허용하는 것의 성질이다.

## 첫째, 무제한 가변성

- 규칙이 대칭이라 문제가 된다 — `ThreadLocal` 변수의 `get()`을 부를 수 있는 코드는 `set()`도
  부를 수 있고, 그래서 데이터가 언제든 바뀔 수 있다 (5장, p.222).[^rahman2025]
- 대가가 추적성이다 — 데이터가 언제 어디서 수정되었는지 알아내기 어려워진다 (5장,
  p.222).[^rahman2025]
- 저자의 예제는 정적 `ThreadLocal`에 로그 레벨을 담은 `MutableLoggingContext`다. 메인 스레드가
  자기 로그 레벨을 `INFO`로 두고, 자식 스레드가 독립적으로 자기 것을 `DEBUG`로 바꾸며, 메인
  스레드의 레벨은 `INFO`로 남는다. 이 마지막 것이 스레드 로컬 격리다 (5장,
  pp.222–223).[^rahman2025]
- 저자가 예제에서 읽어 내는 것은 격리가 아니라 혼란이다 — 로그 레벨을 어디서나 설정할 수 있으니
  어디서 설정되었는지에 대한 혼란이 생긴다 (5장, p.223).[^rahman2025]

## 둘째, 무제한 수명

- 값이 한번 설정되면 명시적으로 제거하지 않는 한 그 스레드의 수명 동안 남는다 (5장,
  p.223).[^rahman2025]
- 이것이 언제 문제가 되는지를 저자가 좁힌다 — 보통의 스레드에서는 문제가 아닐 수 있지만 지금은
  같은 스레드가 되풀이해 재사용되는 스레드 풀을 쓴다. `remove()`를 잊으면 한 태스크에서 다른
  태스크로 데이터가 샐 수 있다 (5장, p.223).[^rahman2025]
- 민감한 데이터가 의도치 않게 남으면 메모리 누수는 물론 보안 취약점까지 낳을 수 있다 (5장,
  p.223).[^rahman2025]
- 저자의 예제가 그 누수를 최소 구성으로 보여 준다 — 스레드 하나짜리 풀에서 첫 태스크가 값을 넣고
  `remove()`를 잊고, 둘째 태스크가 같은 스레드에서 새어 나온 값을 본다 (5장,
  pp.223–224).[^rahman2025]

  ```java
  public class ThreadLocalLeakExample {
      private static final ThreadLocal<String> currentUser = new ThreadLocal<>();

      public static void main(String[] args) throws InterruptedException {
          try (ExecutorService executor = Executors.newFixedThreadPool(1)) {
              executor.submit(() -> {
                  currentUser.set("Alice");
                  System.out.println("Task 1: currentUser = " + currentUser.get());
                  // Forgot to call currentUser.remove()!
              });
              Thread.sleep(100);
              executor.submit(() -> {
                  System.out.println("Task 2: Leaked value = " + currentUser.get());
                  currentUser.set("Bob");
                  currentUser.remove();
              });
          }
      }
  }
  ```

- 저자가 이 누수의 결과를 셋으로 가른다 (5장, p.224).[^rahman2025]
  - 메모리 누수 — 객체가 의도한 것보다 오래 참조된 채 남을 때.
  - 보안 취약점 — 인증 토큰이나 사용자 문맥 같은 민감한 데이터가 서로 무관한 요청 사이로 샐 때.
  - 잘못된 동작 — 태스크가 낡거나 틀린 문맥으로 돌 때.

## 셋째, 상속의 비용

- `InheritableThreadLocal`을 쓰면 자식 스레드가 부모 스레드의 값을 자동으로 물려받는다. 편리할 수
  있지만 자식 스레드를 많이 만들 때 비싸진다 (5장, p.224).[^rahman2025]
- 저자의 예제는 10MB짜리 `byte[]`를 `InheritableThreadLocal`에 넣고 자식 스레드 100개를 만드는
  `InheritanceOverheadExample`이다 (5장, p.224).[^rahman2025]
- 예제에 붙인 주석 셋이 상속의 문제를 센다 (5장, p.225).[^rahman2025]
  - `InheritableThreadLocal`이 값을 자식 스레드로 자동으로 복사한다.
  - 큰 객체가 모든 자식 스레드에 의해 참조된다.
  - 자식이 데이터를 전혀 고치지 않더라도 참조를 유지한다.

## 본문과 주석이 어긋나는 자리

- 같은 쪽의 본문은 다르게 적는다 — 자식 스레드들이 부모 데이터의 **자기만의 별개 복사본**을
  자동으로 물려받아 메모리 사용이 중복된다고 서술한다 (5장, p.225).[^rahman2025]
- 그런데 바로 위 주석 둘과 셋은 큰 객체가 자식들에게 **참조된다**고 적는다 (5장,
  p.225).[^rahman2025] 복사본을 갖는 것과 참조를 갖는 것은 메모리에서 값이 전혀 다르다.
- #hypothesis 복사되는 것은 스레드마다의 맵 항목(참조)이지 참조가 가리키는 객체 자체는 아닐
  것이다. 그러면 주석 쪽이 맞고 본문의 "중복된 메모리 사용"은 항목의 중복을 가리키는 셈이 된다.
  저자가 어느 쪽이라고 밝히지 않으므로 이 KB는 두 서술을 그대로 두고 어느 쪽도 단정하지 않는다.
- 실제 부담의 크기는 어느 쪽 읽기를 택하느냐에 따라 달라지므로, 이 항목을 근거로 수치를 말하지
  않는 것이 맞다.

## 이어지는 페이지

- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md) — 이 결함들이
  실려 있는 그 쓰임
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 같은 결함이 수백만 스레드
  규모에서 갖는 무게
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 스레드 로컬 저장소를
  동기화 없는 갈래로 보는 개념 층
- [ScopedValue가 ThreadLocal보다 나은 이유](../concepts/scoped-value-vs-thread-local.md) — 이 셋에 하나씩
  대응하는 답
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 실제 코드에서 이 쓰임을
  찾아내는 플래그
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Limitations of ThreadLocal
    Variables"(pp.222–225). 개념당 대표 코드 하나 규칙에 따라 `ThreadLocalLeakExample`만
    실었고, `MutableLoggingContext` 전문(pp.222–223)과 `InheritanceOverheadExample`
    전문(p.224)은 미수록이다 — 두 예제가 보이는 결말은 본문에 옮겼다. 인용한 코드에서 임포트
    두 줄과 저자가 붙인 설명 주석 일부는 덜어 냈고, 남긴 주석 한 줄은 원문 그대로다.

---
type: concept
title: 문맥을 넘겨 다니는 부담
description: 프레임워크가 만든 문맥 객체를 메서드 인자로 호출 사슬 전체에 꿰어 넘길 때 생기는 세 가지 구조 문제 — 쓰지도 않는 매개변수가 시그니처를 오염시키는 것, 프레임워크가 자라면 사용자 코드의 시그니처까지 흔들리는 것, 그리고 그 결합이 테스트와 이식을 어렵게 하는 것
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 문맥을 넘겨 다니는 부담

- [무엇이 문제인가](#무엇이-문제인가)
- [저자가 드는 실물](#저자가-드는-실물)
- [매개변수 오염](#매개변수-오염)
- [인터페이스가 부서지기 쉬워진다](#인터페이스가-부서지기-쉬워진다)
- [결합과 테스트 가능성](#결합과-테스트-가능성)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **프레임워크가 만든 문맥 객체를 메서드 인자로 끌고 다니면 무엇이 무너지는가.**

이 페이지의 서술에는 버전 조건이 없다. 특정 API가 아니라 설계 원리이기 때문이다.

## 무엇이 문제인가

- 출발점이 흔한 상황이다 — 코드의 여러 부분 사이에 데이터를 나눠 써야 하는데 메서드 인자를 쓰는
  것만으로는 되지 않는 자리가 자주 있고, 애플리케이션이 프레임워크에 기댈 때 특히 그렇다 (5장
  §"The Burden of Passing Context", p.217).[^rahman2025]
- 저자가 이 상황에 이름을 붙인다 — 아래 예제가 앓는 것은 **"parameter passing problem"**, 곧
  매개변수 전달 문제다 (5장, p.217).[^rahman2025]

## 저자가 드는 실물

- 잡 스케줄링 프레임워크다. 사용자 코드가 태스크를 등록하면 프레임워크가 그것을 실행하고, 잡을
  돌릴 때마다 잡 이름·우선순위·스케줄링 제약 같은 메타데이터를 담은 `JobContext` 객체를 만든다
  (5장, p.217).[^rahman2025]
- 여기서 이해관계가 갈린다 — 이 문맥(context)은 프레임워크 운영에는 필수지만 사용자 코드에는
  대체로 무관하다 (5장, p.217).[^rahman2025]
- 그런데 문맥이 다니는 길이 사용자 코드를 관통한다. 프레임워크의 `schedule()`에서 내려가
  사용자 코드의 `execute()`를 거쳐 다시 프레임워크의 `getJobMetadata()`로 돌아온다 (5장,
  p.220).[^rahman2025]

  ```java
  public class UserJob implements Job {

      private final JobScheduler jobScheduler;

      @Override
      public void execute(JobContext context) {
          Object creationTime = jobScheduler.getJobMetadata("creationTime", context);
          System.out.println("Job creation time: " + creationTime);
          processJobData(context);
      }

      private void processJobData(JobContext context) {
          Object priority = jobScheduler.getJobMetadata("priority", context);
          System.out.println("Processing job with priority: " + priority);
      }
  }
  ```

- 저자가 예제 아래에 붙인 주석이 그 사슬을 항목으로 세운다 — 사용자는 프레임워크 내부를 알 필요가
  없는데도 문맥을 받아야 하고, `execute()` 구현이 `JobContext` 매개변수를 받아야 하며, 사용자
  코드의 보조 메서드까지 프레임워크 매개변수에 오염되고, 호출 사슬의 모든 메서드가 직접 쓰지
  않더라도 그 매개변수를 필요로 한다 (5장, pp.219–220).[^rahman2025]
- 저자의 총평이 문제의 성격을 정한다 — 이 방식이 올바르게 동작하기는 하지만, 애플리케이션이 커질수록
  두드러지는 아키텍처 수준의 문제 몇 가지를 들인다 (5장, p.219).[^rahman2025] 그러니까 버그가
  아니라 구조의 값이다.

## 매개변수 오염

- `JobContext`는 본래 프레임워크의 구성물이고 프레임워크를 쓰는 개발자가 이해해야 할 것이 아니다.
  그러나 프레임워크가 자기 내부 문맥을 호출 사슬 전체에 걸쳐 관리해야 하기 때문에 사용자 코드가
  그 매개변수를 들고 다니도록 강제된다 (5장 §"Parameter Pollution", p.220).[^rahman2025]
- 범위가 예외를 두지 않는다 — 잡 실행 흐름에 참여하는 **모든** 메서드가 이 매개변수를 선언해야
  하고, 그 메서드가 문맥 정보를 전혀 쓰지 않더라도 그렇다 (5장, p.220).[^rahman2025]
- 그래서 값이 시그니처에 실린다 — 애플리케이션 로직에 아무런 업무적 의미가 없는 프레임워크 고유의
  세부가 메서드 시그니처를 오염시킨다 (5장, p.220).[^rahman2025]

## 인터페이스가 부서지기 쉬워진다

- 시간 축을 넣으면 문제가 하나 더 나온다 — 프레임워크가 진화해 `JobContext`에 데이터를 더하면
  (저자가 드는 예는 새 잡 범주 필드, 분산 추적 문맥, 로깅 참조다) 문맥을 넘겨 다니는 사용자 코드의
  모든 메서드 시그니처를 고쳐야 할 수 있다 (5장 §"Interface Brittleness", p.220).[^rahman2025]
- 여기에 저자가 단서를 단다 — `JobContext` 클래스 자체는 하위 호환을 지키더라도, 그것을 사용자
  코드에 꿰어 넘겨야 한다는 요구 때문에 프레임워크가 필요로 하는 것의 확장이 사용자 코드베이스
  전체로 번진다 (5장, p.220).[^rahman2025] 깨지는 것은 프레임워크의 계약이 아니라 그것을 쓰는
  쪽의 시그니처다.

## 결합과 테스트 가능성

- 사용자 코드가 프레임워크 구현 세부에 강하게 결합된다 (5장 §"Coupling and Testability",
  p.220).[^rahman2025]
- 대가가 테스트에서 먼저 드러난다 — 개별 메서드를 테스트하는 일이 복잡해진다. 프레임워크와 무관한
  업무 로직에 집중하는 테스트에서도 언제나 유효한 `JobContext`를 마련해 줘야 하기 때문이다 (5장,
  p.220).[^rahman2025]
- 이 결합은 다른 프레임워크로 옮기거나 업무 로직을 떼어 내 다른 문맥에서 재사용하는 일도 더
  어렵게 만든다 (5장, p.220).[^rahman2025]

## 이어지는 페이지

- [ThreadLocal로 문맥을 감추는 프레임워크 패턴](../concepts/thread-local-context-propagation.md) — 이 부담을
  없애려고 프레임워크들이 실제로 쓰는 우회로
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 그 우회로가 남기는 값
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 같은 문제에 자바가 내놓은
  정식 답
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"The Burden of Passing Context"(pp.217–220),
    §"Parameter Pollution"(p.220), §"Interface Brittleness"(p.220), §"Coupling and
    Testability"(p.220). 개념당 대표 코드 하나 규칙에 따라 오염된 사용자 코드(`UserJob`)만
    실었고, `JobContext` 레코드와 `Job` 인터페이스와 `Priority` 열거형(p.218), 프레임워크 쪽
    `JobScheduler` 전문(p.218)은 미수록이다. 인용한 코드에서 임포트와 생성자, 그리고 첫 줄의
    `System.out.println` 한 줄은 덜어 냈다.

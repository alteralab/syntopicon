---
type: concept
title: ThreadLocal로 문맥을 감추는 프레임워크 패턴
description: 프레임워크가 문맥 객체를 매개변수로 넘기는 대신 ThreadLocal에 담아 사용자 코드에서 감추는 방법과 그 절차, try와 finally로 반드시 제거해야 하는 이유, 그리고 이 패턴이 실제 프레임워크에 얼마나 널리 퍼져 있는가
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T21:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# ThreadLocal로 문맥을 감추는 프레임워크 패턴

- [무엇을 바꾸는가](#무엇을-바꾸는가)
- [프레임워크 쪽이 하는 일](#프레임워크-쪽이-하는-일)
- [사용자 코드 쪽에서 사라지는 것](#사용자-코드-쪽에서-사라지는-것)
- [얼마나 널리 쓰이는가](#얼마나-널리-쓰이는가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **프레임워크는 자기 문맥 객체를 사용자 코드에서 어떻게 감추는가.**

이 페이지의 서술에는 버전 조건이 없다. `ThreadLocal`은 오래된 API이고 아래 패턴은 특정 릴리스에
묶이지 않는다.

## 무엇을 바꾸는가

- 우회로가 하나 있다 —
  [문맥을 넘겨 다니는 부담](../concepts/context-passing-burden.md)을 피하려면 프레임워크 코드를
  `ThreadLocal`로 영리하게 설계하면 된다. `ThreadLocal`은 그런 코드에 흔히 쓰이는 도구다
  (5장 §"Introducing ThreadLocal", p.220).[^rahman2025]
- 바뀌는 것은 데이터가 다니는 길이다. 문맥이 인자를 타고 호출 사슬을 내려가는 대신, 스레드에 붙어
  있다가 필요한 자리에서 꺼내진다.

## 프레임워크 쪽이 하는 일

- 스케줄러가 문맥을 자기 안에 담는다 (5장, pp.220–221).[^rahman2025]

  ```java
  public class JobScheduler {
      private static final ThreadLocal<JobContext> jobContextHolder = new ThreadLocal<>();

      public void schedule(Job job, String jobName, Priority priority) {
          JobContext context = new JobContext(jobName, priority);
          try {
              jobContextHolder.set(context);
              runJob(job);
          } finally {
              jobContextHolder.remove();
          }
      }

      private void runJob(Job job) {
          job.execute();
      }

      public Object getJobMetadata(String key) {
          JobContext context = jobContextHolder.get();
          return (context != null) ? context.getMetadataValue(key) : null;
      }
  }
  ```

- 저자가 예제에 붙인 주석이 절차를 다섯으로 센다 (5장, p.221).[^rahman2025]
  - 스레드마다 `JobContext`를 담을 `ThreadLocal` 변수를 만든다.
  - 잡을 실행하기 전에 현재 스레드에 문맥을 설정한다.
  - **메모리 누수를 막으려면 `finally` 블록에서 언제나 문맥을 제거한다.**
  - `runJob` 메서드는 더 이상 문맥 매개변수를 필요로 하지 않는다.
  - 프레임워크 메서드는 필요할 때마다 `ThreadLocal`에서 문맥을 꺼낼 수 있다.
- 셋째 항목이 이 패턴의 값이다. 정리를 사람이 기억해야 하고, 그것을 잊었을 때 무엇이 일어나는지는
  [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md)에 있다.

## 사용자 코드 쪽에서 사라지는 것

- 사용자 코드가 훨씬 깨끗해지고 프레임워크 문맥을 다룰 필요가 없어진다 (5장,
  p.221).[^rahman2025] `execute()`가 인자를 받지 않고, 보조 메서드의 시그니처도 업무 로직에만
  집중한다 (5장, p.222).[^rahman2025]
- 저자가 결과를 세 줄로 적는다 — 사용자 코드가 프레임워크 문맥 걱정에서 완전히 벗어나고,
  프레임워크 서비스에 문맥 매개변수 없이 닿을 수 있으며, 보조 메서드가 깨끗한 시그니처를 갖는다
  (5장, p.222).[^rahman2025]
- 그래서 이 접근이 매개변수 전달 문제를 효과적으로 푼다. 프레임워크의 내부 문맥 관리가 사용자
  코드에서 완전히 감춰진다 (5장, p.222).[^rahman2025]

## 얼마나 널리 쓰이는가

- 이 패턴이 매우 효과적이라, 사실상 모든 현대 프레임워크가 문맥 관리에 어떤 형태로든 `ThreadLocal`을
  쓴다 (5장, p.222).[^rahman2025]
- 저자가 드는 실물이 스프링 프레임워크다 — 보안 문맥, 트랜잭션 문맥, 요청 문맥에 `ThreadLocal`을
  널리 쓴다 (5장, p.222).[^rahman2025]
- 이 사실이 다음 장의 무게를 정한다. `ThreadLocal`의 결함은 한 사람의 코딩 습관 문제가 아니라
  이미 깔려 있는 기반의 성질이다.

## 이어지는 페이지

- [문맥을 넘겨 다니는 부담](../concepts/context-passing-burden.md) — 이 패턴이 없앤 문제
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 이 패턴이 남기는 값
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 같은 도구가 규모에서
  부딪히는 자리
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — `ThreadLocal`의
  구현 내부(`ThreadLocalMap`)와 그것이 놓인 갈래
- [ScopedValue의 구성 요소와 API](../concepts/scoped-value-core-components.md) — 같은 자리를 대신하겠다는
  API
- [컨텍스트 전달과 스코프 값](../synthesis/context-propagation-and-scoped-values.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 5장 "Scoped Values" — §"Introducing ThreadLocal"(pp.220–222).
    개념당 대표 코드 하나 규칙에 따라 프레임워크 쪽 `JobScheduler`만 실었고, 다시 쓴
    `UserJob` 전문(pp.221–222)은 미수록이다 — 사라진 매개변수의 자리는 본문에 옮겼다.

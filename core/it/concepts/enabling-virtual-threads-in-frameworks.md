---
type: concept
title: 프레임워크가 가상 스레드를 켜는 방식
description: 스프링 부트와 쿼커스와 자카르타 EE가 가상 스레드를 켜는 손잡이의 공통 모양 — 전역 설정 스위치와 선별 애너테이션과 태생적 설계라는 세 갈래, 프레임워크마다의 실물과 각각의 버전 경계, 지원하지 않는 자바에서 플랫폼 스레드로 되돌아가는 폴백, 명세가 있어도 런타임마다 갈리는 실제 동작, 그리고 켜도 명령형 블로킹 코드가 그대로 남는다는 점
generated: { by: "claude-opus-5", at: "2026-09-05T23:30:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 프레임워크가 가상 스레드를 켜는 방식

- [버전 조건](#버전-조건)
- [무엇이 바뀌었나](#무엇이-바뀌었나)
- [켜는 손잡이 세 갈래](#켜는-손잡이-세-갈래)
- [프레임워크별 실물](#프레임워크별-실물)
- [스프링 부트의 전역 스위치](#스프링-부트의-전역-스위치)
- [켜도 그대로 남는 것](#켜도-그대로-남는-것)
- [지원하지 않는 자바에서의 폴백](#지원하지-않는-자바에서의-폴백)
- [명세와 런타임 사이의 틈](#명세와-런타임-사이의-틈)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **애플리케이션 프레임워크는 어떤 손잡이 하나로 가상 스레드를 켜며, 켜고 나면
무엇이 달라지고 무엇이 그대로인가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 여기 옮긴 프레임워크 지원은 가상 스레드가 정식이 된 릴리스를
> 전제로 한다. 프레임워크 쪽 경계는 제품마다 따로 있다 — 스프링 부트는 3.2 이상, 자카르타
> 동시성(Jakarta Concurrency)은 3.1 이상, 마이크로노트(Micronaut)는 자바 21 이상에서 자동으로
> 쓴다. **아래의 설정 키와 애너테이션 이름은 그 판의 것이다** — 이 층은 이 소스에서 가장 빨리
> 낡는 자리이므로, 프레임워크 메이저 릴리스가 나올 때마다 실물을 다시 확인해야 한다.

## 무엇이 바뀌었나

- 저자가 장을 여는 문장이 생태계 전체의 이동을 가리킨다 (7장, p.297).[^rahman2025]

  > With the introduction of virtual threads in JDK 21, the Java ecosystem has witnessed
  > a significant shift in how frameworks handle concurrency.

- 저자가 다루는 범위를 스스로 좁힌다 — 이 장은 스프링 부트, 쿼커스, 자카르타 EE 같은 주요
  프레임워크가 가상 스레드를 어떻게 통합하는지를 볼 뿐, 각 프레임워크의 내부 동작까지 파고들지는
  않는다 (7장, p.297).[^rahman2025]

## 켜는 손잡이 세 갈래

- **전역 설정 스위치** — 설정 프로퍼티 한 줄로 애플리케이션 전체에 걸어 켠다. 스프링 부트가
  이 갈래다 (7장, p.298).[^rahman2025]
- **선별 애너테이션** — 전역이 아니라 특정 엔드포인트나 서비스에만 건다. 쿼커스는
  `@RunOnVirtualThread`로, 자카르타 동시성은 실행자 정의 애너테이션에 `virtual = true`를 적어
  거는 방식이다 (7장, pp.302, 307).[^rahman2025] 쿼커스 쪽 기제는
  [이벤트 루프에서 가상 스레드로 덜어내기](../concepts/offloading-blocking-work-from-event-loops.md)에
  있다.
- **태생적이거나 자동** — 손잡이가 아예 없다. 헬리든 니마(Helidon Níma)는 가상 스레드를 태생적으로
  활용하도록 처음부터 설계된 마이크로서비스 프레임워크이고, 마이크로노트는 가상 스레드를 지원하는
  JDK 위에서 돌면 추가 설정 없이 자동으로 쓴다 (7장, p.309).[^rahman2025]
- 저자가 그 결과를 한 문장으로 맺는다 — 자카르타 EE 11, 쿼커스, 스프링 부트 3, 헬리든 니마,
  마이크로노트 가운데 무엇을 쓰든 개발자는 단순한 명령형 코딩 스타일을 유지하면서 동시성이 높은
  애플리케이션을 쓸 도구를 갖게 되었다 (7장, p.309).[^rahman2025]

## 프레임워크별 실물

| 프레임워크 | 켜는 손잡이 | 버전 경계 |
|---|---|---|
| 스프링 부트 | 설정 프로퍼티 `spring.threads.virtual.enabled` 를 참으로 | 스프링 부트 3.2 이상, 스프링 프레임워크 6.1 기반 |
| 쿼커스 | 메서드에 `@RunOnVirtualThread` | 소스가 판 번호를 적지 않는다 |
| 자카르타 EE | `@ManagedExecutorDefinition`, `@ManagedScheduledExecutorDefinition`, `@ManagedThreadFactory` 에 `virtual = true` | 자카르타 동시성 3.1 이상 |
| 헬리든 니마 | 없음. 가상 스레드를 중심으로 설계됨 | 소스가 판 번호를 적지 않는다 |
| 마이크로노트 | 없음. JDK가 지원하면 자동 | 자바 21 이상 |

## 스프링 부트의 전역 스위치

- 스프링 부트가 오래 서 온 자리부터 저자가 짚는다 — 스프링 부트 웹 애플리케이션은 역사적으로
  요청당 스레드(thread-per-request) 모델을 주로 따랐고, 들어오는 클라이언트 요청마다 전용 플랫폼
  스레드 하나가 그것을 맡았다. 중간 정도의 부하에서는 잘 돌지만 I/O 바운드 요청이 동시에 많이
  들어오면 확장성 문제에 부딪힌다. 그 요청들이 언제나 플랫폼 스레드로 처리되기 때문이다 (7장,
  p.297).[^rahman2025] 그 모델이 왜 막히는지는
  [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)에 있다.
- 그 완화책이었던 `@Async`와 `TaskExecutor`도 같은 벽에 갇혀 있었다 — 여전히 제한된 플랫폼 스레드
  풀에 의존했고, 요청이나 태스크마다 유한한 풀에서 스레드 하나를 소비하므로 부하가 커지면 성능
  병목이 될 수 있다 (7장, pp.297–298).[^rahman2025]
- 판이 갈린 지점의 수치를 원문 그대로 옮긴다 (7장, p.298).[^rahman2025]

  > With the release of Spring Boot 3.2, built upon Spring Framework 6.1, in November 2023,
  > official support for Java 21, which finalized virtual threads, was introduced. While
  > Java 17 remains the baseline JDK, Java 21 is now treated as a first-class runtime
  > environment within the framework.

- 손잡이는 설정 프로퍼티 하나다. `spring.threads.virtual.enabled` 를 참으로 두면 애플리케이션
  전체에서 가상 스레드가 켜진다 (7장, p.298).[^rahman2025] YAML 형식도 같은 값을 적는다.

  ```yaml
  # application.yml
  spring:
    threads:
      virtual:
        enabled: true
  ```

- 켜면 스프링 부트가 알아서 갈아 끼운다 — 사용자 정의 실행자 빈이 없으면 가상 스레드로 뒷받침되는
  `AsyncTaskExecutor`를 `SimpleAsyncTaskExecutor`를 통해 자동으로 구성한다 (7장,
  p.298).[^rahman2025]
- 그 자동 구성이 걸리는 자리를 저자가 넷 든다 — 비동기 태스크 실행(`@EnableAsync`), 스프링에서
  `Callable` 반환값의 비동기 처리, 스프링 웹 MVC의 비동기 요청 처리, 스프링 WebFlux의 간헐적
  블로킹 실행 지원이다 (7장, p.298).[^rahman2025]
- 스케줄러도 같이 바뀐다 — 가상 스레드가 켜지면 스프링 부트는 `SimpleAsyncTaskExecutor`
  (이름 `applicationTaskExecutor`)와 `SimpleAsyncTaskScheduler`(이름 `taskScheduler`)를 자동으로
  쓰고, 가상 스레드가 없으면 설정 가능한 `ThreadPoolTaskExecutor`와 `ThreadPoolTaskScheduler`로
  기본값을 잡는다 (7장, p.300).[^rahman2025] 그 풀 쪽 설정의 내막은
  [ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md)에 있다.

## 켜도 그대로 남는 것

- **손잡이를 켜는 것으로 끝이고 코드는 그대로다.** 저자가 든 컨트롤러 예제는 스위치 전후로 같은
  코드이며, 달라지는 것은 로그에 찍히는 스레드가 플랫폼 스레드에서
  `VirtualThread[...]/runnable@ForkJoinPool-1-worker-N` 꼴로 바뀌는 것뿐이다 (7장,
  pp.299–300).[^rahman2025] 그 이름에 포크조인 풀이 찍히는 이유는
  [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md)에 있다.
- 그래서 프레임워크 층의 이야기가 애플리케이션 층의 이야기와 같은 모양이다 — 실행자를 갈아 끼우면
  블로킹 명령형 코드를 그대로 두고 이득을 얻는다는 것이
  [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md)의 주장이고,
  프레임워크는 그 갈아 끼우기를 설정 한 줄 뒤로 감춘 것이다.

## 지원하지 않는 자바에서의 폴백

- 자카르타 동시성은 표준 명세 쪽 답이다 — 애플리케이션이 자카르타 EE 런타임 안에서 도는 이점을
  유지한 채 동시성을 쓸 수 있게 하는 명세이고, 자카르타 동시성 3.1이 가상 스레드 지원을 들여
  자바 21의 경량 스레드 모델을 쓸 수 있게 했다 (7장, p.306).[^rahman2025]
- 켜는 자리는 애너테이션 셋이다 — `@ManagedExecutorDefinition`,
  `@ManagedScheduledExecutorDefinition`, `@ManagedThreadFactory` 에 `virtual = true` 를 적는다
  (7장, p.307).[^rahman2025]
- **폴백이 명세에 들어 있다** — 자바 21에서 돌면 가상 스레드를 쓰지만, 가상 스레드를 지원하지 않는
  자바 17에서 애플리케이션이 돌면 자카르타 EE 런타임이 자동으로 플랫폼 스레드를 쓴다 (7장,
  p.307).[^rahman2025]
  - 버전 조건: 자카르타 동시성 3.1 기준. 이 폴백은 명세가 정한 것이므로 같은 코드가 두 자바
    버전에서 다르게 돌아간다는 뜻이다.

## 명세와 런타임 사이의 틈

- 명세가 있다고 동작이 같지는 않다는 경고를 저자가 붙인다 — 자카르타 동시성 3.1이 가상 스레드를
  쓰는 명세를 주지만 실제 동작은 자카르타 EE 런타임마다 다를 수 있다. 호환성 문제를 의식하고
  오픈 리버티(Open Liberty), 파야라(Payara), 와일드플라이(WildFly) 같은 자기 런타임의 문서를
  읽어야 하며, 기능과 설정이 런타임마다 다르게 동작하거나 아예 없을 수도 있다 (7장,
  p.308).[^rahman2025]
- 집필 시점의 실물도 적혀 있다 — 오픈 리버티 24.0.0.6-beta가 가상 스레드를 포함한 자카르타 동시성
  3.1을 온전히 지원하는 첫 자카르타 EE 런타임이고, 자카르타 EE 11의 최종 릴리스가 다가오면서
  파야라, 와일드플라이, 톰이(TomEE), 글래스피시(GlassFish) 같은 다른 런타임도 가상 스레드 지원을
  넣을 것으로 예상된다 (7장, p.308).[^rahman2025]
  - 버전 조건: 이 목록은 이 책의 집필 시점(초판 2025년 9월) 상태다. 어느 런타임이 지원하는지는
    그 뒤로 바뀌었을 수 있으므로, 실제 채택 전에 해당 런타임의 현재 문서를 확인해야 한다.

## 이어지는 페이지

- [실행자 자리를 갈아 끼워 가상 스레드 켜기](../concepts/virtual-thread-executor-injection.md) —
  설정 스위치가 없을 때 손으로 하는 같은 일
- [이벤트 루프에서 가상 스레드로 덜어내기](../concepts/offloading-blocking-work-from-event-loops.md)
  — 선별 애너테이션 쪽의 기제
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 이
  설정이 대신 해 주는 한 줄 교체
- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 요청당 스레드 모델이 부딪힌 벽
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 프레임워크가
  대신해 주지 않는 이전의 나머지
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 7장 "Modern Frameworks Utilizing Virtual Threads" — 도입(p.297),
    "Spring Boot"(pp.297–302), "Jakarta EE"(pp.306–308), "In Closing"(p.309). 개념당 대표 코드
    하나 규칙에 따라 YAML 설정만 실었고, 원문의 `ThreadPoolConfig`(p.298),
    `GreetingsController`·`AsyncController`(p.299), `ScheduledTasks`(p.300),
    `VirtualThreadExampleService`(p.307), `VirtualThreadSchedulerExample`(p.308)와 콘솔 로그
    출력들은 옮기지 않거나 서술로만 담았다. 원문의 `application.properties` 한 줄
    (`spring.threads.virtual.enabled=true`)은 조판에서 끝에 마침표가 붙어 있어 그대로 옮기면
    복사해 쓸 수 없으므로 본문에서는 키 이름만 인라인으로 적었다. 이 절에는 그림이 없다.

---
type: concept
title: 실행자 자리를 갈아 끼워 가상 스레드 켜기
description: 설정 스위치가 없거나 더 통제하고 싶을 때 쓰는 손 구성 — 실행자를 받는 자리마다 가상 스레드 실행자를 넘긴다는 하나의 모양, 스프링의 applicationTaskExecutor 빈과 어댑터를 쓸 때의 이점, 내장 톰캣의 프로토콜 핸들러, 그리고 프레임워크 없이 JDK 내장 HTTP 서버에 같은 실행자를 꽂는 자리
generated: { by: "claude-opus-5", at: "2026-09-05T23:30:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 실행자 자리를 갈아 끼워 가상 스레드 켜기

- [버전 조건](#버전-조건)
- [하나의 모양](#하나의-모양)
- [스프링에서 손으로 구성하기](#스프링에서-손으로-구성하기)
- [어댑터와 팩터리 가운데 무엇을 넘기는가](#어댑터와-팩터리-가운데-무엇을-넘기는가)
- [내장 웹 서버까지 내려가기](#내장-웹-서버까지-내려가기)
- [프레임워크 없이 같은 일 하기](#프레임워크-없이-같은-일-하기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **설정 프로퍼티가 없는 자리에서 가상 스레드는 어디에 꽂는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 여기 나오는 스프링 쪽 클래스 이름과 빈 이름은 이 소스가 쓰는 판의
> 것이다. 손 구성 자체는 **스프링 부트 3.2 이전 판에서 필요한 길**이지만, 3.2 이상에서도 실행자
> 구성을 더 통제하고 싶으면 쓴다.

## 하나의 모양

- 저자가 여러 자리에서 되풀이하는 동작이 하나다 — **실행자를 받는 자리마다
  `Executors.newVirtualThreadPerTaskExecutor()`를 넘긴다.** 스프링의 태스크 실행자 빈(7장,
  pp.300–301), 내장 톰캣의 프로토콜 핸들러(7장, pp.301–302), JDK 내장 HTTP 서버(7장, p.305)가
  모두 같은 모양이다.[^rahman2025]
- 이것은 [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md)가
  적은 한 줄 교체와 같은 일이고, 프레임워크의 설정 스위치는 그 교체를 대신 해 주는 것이다. 그 스위치
  쪽은 [프레임워크가 가상 스레드를 켜는 방식](../concepts/enabling-virtual-threads-in-frameworks.md)에
  있다.

## 스프링에서 손으로 구성하기

- 손 구성이 필요한 두 경우를 저자가 든다 — 스프링 부트 3.2 이전 판을 쓰고 있거나, 실행자 구성을
  더 통제하고 싶을 때다. 그때는 가상 스레드로 뒷받침되는 실행자를 명시적으로 정의한다 (7장,
  p.300).[^rahman2025]
- 갈아 끼우는 대상이 `applicationTaskExecutor` 빈이다 (7장, pp.300–301).[^rahman2025]

  ```java
  @Configuration
  public class VirtualThreadConfig {

      @Bean
      public AsyncTaskExecutor applicationTaskExecutor() {
          return new TaskExecutorAdapter(Executors.newVirtualThreadPerTaskExecutor());
      }
  }
  ```

- 그 결과가 애너테이션 쪽에서 드러난다 — 이 구성이 있으면 애플리케이션의 `@Async` 메서드가
  전통적인 플랫폼 스레드 대신 가상 스레드에서 자동으로 돈다 (7장, p.301).[^rahman2025]
- 이유가 스프링의 비동기 모델 안에 있다 — `@Async`를 붙인 메서드는 구성된
  `applicationTaskExecutor`에 의존하므로, 기본 실행자를 가상 스레드 기반 실행자로 바꾸면 그
  메서드들이 자연스럽게 가벼운 가상 스레드에서 돈다 (7장, p.301).[^rahman2025]

## 어댑터와 팩터리 가운데 무엇을 넘기는가

- 저자가 구분을 하나 짚는다 — 스프링 부트에서 가상 스레드 실행자를 손으로 구성할 때
  `TaskExecutorAdapter`를 쓰는 것과 `Executors.newVirtualThreadPerTaskExecutor()`를 그대로 쓰는
  것의 차이를 이해하는 것이 중요하다. 둘 다 가상 스레드를 켜지만, `TaskExecutorAdapter`가 스프링의
  빈 생명 주기 관리와 더 잘 통합된다. 초기화와 종료 같은 스프링의 관리 능력을 고려해 알맞은 쪽을
  고르라는 것이 저자의 지침이다 (7장, p.301).[^rahman2025]

## 내장 웹 서버까지 내려가기

- 태스크 실행자 위쪽만이 아니라 서버 쪽에도 같은 것을 꽂을 수 있다 — 내장 웹 서버에 가상 스레드를
  써서 확장성과 자원 활용을 올릴 수 있고, 아파치 톰캣(Apache Tomcat)을 내장 웹 서버로 쓰고 있다면
  `TomcatProtocolHandlerCustomizer` 빈을 정의해 프로토콜 핸들러가 가상 스레드를 쓰도록 바꾼다
  (7장, pp.301–302).[^rahman2025] 그 핸들러의 본문은
  `protocolHandler.setExecutor(Executors.newVirtualThreadPerTaskExecutor())` 한 줄이다 (7장,
  p.302).[^rahman2025]
- 이 자리가 [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)이 서블릿 컨테이너의
  스레드 풀이라고 적은 그 자리다. 요청을 받아 넘기는 풀 자체를 가상 스레드로 바꾸는 것이므로,
  요청당 스레드 모델을 버리지 않고 그 상한만 걷어 내는 셈이다.

## 프레임워크 없이 같은 일 하기

- 저자가 예제용 원격 서비스를 만들면서 프레임워크 없이 같은 일을 한다 — JDK가 `HttpServer`와
  `HttpHandler` 같은 클래스를 포함하고 있어서 추가 프레임워크나 의존 없이 가벼운 HTTP 서비스를
  빠르게 세울 수 있고, 그 서버의 실행자로 가상 스레드 실행자를 넘긴다
  (`server.setExecutor(Executors.newVirtualThreadPerTaskExecutor())`) (7장,
  pp.304–305).[^rahman2025]
- 실행 방법에도 부수 사실이 하나 붙는다 — 이 서버는 자바의 소스 파일 실행 기능으로 컴파일 단계
  없이 바로 돌릴 수 있다. `java SimpleHttpServer.java` 한 줄이 컴파일과 실행을 한 걸음에 끝내며,
  빠른 시제품이나 단순한 독립 프로그램에 알맞다 (7장, p.305).[^rahman2025]
  - 버전 조건: 자바 11 이상. 저자가 이 기능을 자바 11부터 쓸 수 있다고 적는다.

## 이어지는 페이지

- [프레임워크가 가상 스레드를 켜는 방식](../concepts/enabling-virtual-threads-in-frameworks.md) —
  이 손 구성을 설정 한 줄로 대신하는 쪽
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 같은
  한 줄 교체를 프레임워크 없이 본 자리
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 갈아 끼우는
  그 추상의 정체
- [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md) — 같은 팩터리
  자리에 놓이던 다른 선택지들
- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 서블릿 컨테이너의 풀이 부딪힌 벽
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 7장 "Modern Frameworks Utilizing Virtual Threads" — "Manual
    Configuration"(pp.300–302), "Quarkus"(pp.304–305)의 `SimpleHttpServer` 예제. 개념당 대표
    코드 하나 규칙에 따라 `VirtualThreadConfig`만 실었고, `RemoteApiService`(p.301),
    `TomcatConfig`(p.302), `SimpleHttpServer`(pp.304–305)는 본문에 짧은 조각으로만 옮겼다.
    인용한 `VirtualThreadConfig`는 원문(pp.300–301)이 조판에서 두 쪽에 걸쳐 갈라 놓은 것을 한
    조각으로 이었고, 원문에 있던 `import` 줄은 덜어 냈다. 이 절에는 그림이 없다.

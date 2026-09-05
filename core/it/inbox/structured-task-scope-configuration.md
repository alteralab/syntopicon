---
type: concept
title: 스코프 구성
description: StructuredTaskScope의 기본 구성 셋과 그것을 바꾸는 구성 함수, 새 객체를 돌려주는 불변 빌더 꼴의 Configuration 세 메서드, 스레드에 이름을 붙여 덤프에서 알아보게 하는 쓰임, 스코프가 열리는 순간부터 세는 타임아웃, 그리고 플랫폼 스레드로도 돌릴 수 있으나 그러면 원래 문제로 돌아간다는 것
status: draft
stale_after: "2026-03-31"
generated: { by: "claude-opus-5", at: "2026-09-05T18:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 스코프 구성

- [버전 조건](#버전-조건)
- [기본 구성 셋](#기본-구성-셋)
- [바꾸는 자리는 구성 함수다](#바꾸는-자리는-구성-함수다)
- [이름 붙은 스레드](#이름-붙은-스레드)
- [타임아웃은 스코프가 열릴 때부터 센다](#타임아웃은-스코프가-열릴-때부터-센다)
- [셋을 함께 거는 자리](#셋을-함께-거는-자리)
- [플랫폼 스레드로도 돌아간다](#플랫폼-스레드로도-돌아간다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스코프가 서브태스크를 어떤 스레드로, 어떤 이름으로, 얼마 동안 돌릴지를 어떻게
정하는가.**

## 버전 조건

> **버전 조건**: JDK 25의 미리 보기(preview) 기능 기준. 컴파일과 실행에 `--enable-preview`가
> 필요하다 (4장, p.179의 실행 명령에 그 플래그가 다시 나온다). 아래 인터페이스와 메서드 이름은 이
> 소스가 쓰는 JDK 25 판의 것이고, 미리 보기 기능이라 정식화될 때 바뀔 수 있다. `stale_after`는 그
> 다음 릴리스(JDK 26, 2026년 3월)를 재심 시점으로 잡은 것이다.

## 기본 구성 셋

- 기본 구성이 많은 상황에서 잘 돌아가지만, 실제 애플리케이션은 동시 태스크가 어떻게 실행되는지에
  대한 더 많은 통제를 요구할 때가 많다. 구성(Configuration)이 손대게 해 주는 것이 셋이다 —
  스레드 생성 방식, 모니터링 능력, 그리고 타임아웃 정책 (4장 §"Configuration",
  p.179).[^rahman2025]
- `open()`이나 `open(Joiner)`로 스코프를 만들면 적당한 기본 구성이 붙는다 (4장,
  p.179):[^rahman2025]
  - `ThreadFactory` — 이름 없는 가상 스레드를 만든다.
  - 모니터링용 이름 — 붙지 않는다(익명 스코프).
  - 타임아웃 — 없다. 태스크는 완료되거나 취소될 때까지 돈다.

## 바꾸는 자리는 구성 함수다

- 운영 애플리케이션에는 더 정교한 통제가 필요할 때가 많고, 그 자리가 **구성 함수를 인자로 받는
  오버로드된 `open` 메서드**다 — `open(Joiner<? super T, ? extends R> joiner,
  Function<Configuration, Configuration> configFunction)` (4장, pp.179–180).[^rahman2025]
- `Configuration`은 봉인 인터페이스(sealed interface)이고 세 메서드를 준다.
  `withThreadFactory(ThreadFactory)`, `withName(String)`, `withTimeout(Duration)`이며 **각각이
  지정한 변경을 반영한 새 `Configuration` 객체를 돌려준다** (4장, p.180).[^rahman2025]
- 그래서 꼴이 불변 빌더(immutable builder) 패턴이다 — 기존 객체를 고치는 대신 새 객체를
  돌려주므로 여러 구성 호출을 유창하게(fluent) 이어 붙일 수 있다 (4장, p.180).[^rahman2025]
- 핵심은 구성 함수가 **기본 구성을 받아 하나 이상의 변경을 적용해 바꾼다**는 것이다 (4장,
  p.180).[^rahman2025]

## 이름 붙은 스레드

- 가장 흔한 손질이 이름 붙은 스레드다. 스레드 덤프나 프로파일링 도구에서 어느 스레드가 무슨 일을
  하는지 알아보기 훨씬 쉬워진다 (4장 §"Named threads", p.180).[^rahman2025]
- 만드는 법은 가상 스레드 빌더에 접두사와 시작 번호를 주고 팩토리로 바꾸는 것이다 —
  `Thread.ofVirtual().name("user-processor-", 0).factory()` (4장, p.180).[^rahman2025]
- 실행하면 스레드 이름이 `user-processor-0`부터 차례로 붙어 로그에 찍힌다 (4장,
  p.181).[^rahman2025] 이름이 덤프에서 무엇을 바꾸는지는
  [구조가 드러나는 스레드 덤프](../concepts/structured-thread-dumps.md)에 있다.

## 타임아웃은 스코프가 열릴 때부터 센다

- 타임아웃은 회복력 있는 애플리케이션의 필수 요소다. 연산이 무한정 매달리는 것을 막고, 서비스가
  응답하지 않을 때 빨리 실패하게 한다 (4장 §"Timeout configuration", p.181).[^rahman2025]
- 거는 법은 `cf -> cf.withTimeout(timeout)`이고, 서브태스크 가운데 하나라도 그 시간 안에 끝나지
  못하면 `join()`이 `TimeoutException`을 던진다 (4장, p.182).[^rahman2025]
- **세는 시작점이 함정이다** — 타임아웃은 `join()`을 부르는 순간이 아니라 **스코프가 열리는
  순간부터** 센다. 그래서 타임아웃이 스코프의 수명 주기 전체를 덮는다 (4장,
  p.183).[^rahman2025]
- 저자의 예제에서는 5초 타임아웃에 8초 걸리는 소스가 섞여 있어 그 소스가 시간 초과를 부른다 (4장,
  pp.182–183).[^rahman2025]

## 셋을 함께 거는 자리

- 구성의 가장 강력한 면은 여러 선택지를 결합해 실행 환경을 정확히 짓는 것이다 (4장 §"Combining
  configuration options", p.183).[^rahman2025]

  ```java
  ThreadFactory factory = Thread.ofVirtual()
      .name("api-client-", 0)
      .factory();
  Duration timeout = Duration.ofSeconds(15);

  try (var scope = open(Joiner.<String>allSuccessfulOrThrow(),
      cf -> cf.withThreadFactory(factory)
              .withTimeout(timeout)
              .withName("api-integration-scope"))) {

    var userTask = scope.fork(this::callUserAPI);
    var profileTask = scope.fork(this::callProfileAPI);
    var preferencesTask = scope.fork(this::callPreferencesAPI);

    var results = scope.join()
        .map(Subtask::get)
        .toList();
  }
  ```

- 저자가 이 구성에서 짚는 것이 일곱이다 (4장, pp.184–185):[^rahman2025] 가상 스레드 빌더를
  만들고, `api-client-0`부터 번호가 붙는 이름 규칙을 세우고, 그 빌더를 스코프가 쓸 수 있는
  `ThreadFactory`로 바꾸고, API 하나가 응답하지 않을 때 빨리 실패하도록 15초 타임아웃을 잡고,
  스코프가 그 팩토리로 작업 스레드를 만들게 하고, 스코프가 열리는 순간부터 그 타임아웃을 세게 하고,
  운영 로그와 모니터링 도구에서 알아보기 쉽도록 스코프에 뜻이 담긴 이름을 붙인다.

## 플랫폼 스레드로도 돌아간다

- 흔한 물음 하나에 저자가 답한다 — 구조적 동시성을 가상 스레드와 플랫폼 스레드 양쪽에 쓸 수
  있는가. 답은 **그렇다**이고, `Thread.ofPlatform().name("platform-worker-", 0).factory()`로 만든
  팩토리를 `withThreadFactory`에 주면 된다 (4장 §"In Closing", p.214).[^rahman2025]
- 그러나 그러면 원래 문제로 돌아간다 — 플랫폼 스레드의 희소성이다. 동시성이 높은 상황에서
  플랫폼 스레드에 딸린 확장성과 자원 제약을 유념해야 하고, 대부분의 구조적 동시성 애플리케이션에는
  가상 스레드가 여전히 더 나은 선택이다 (4장, p.214).[^rahman2025] 그 희소성의 근거는
  [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md)에 있다.

## 이어지는 페이지

- [구조적 동시성 스코프](../concepts/structured-concurrency-scopes.md) — 이 구성이 얹히는 API
- [스코프와 서브태스크의 수명 주기](../concepts/scope-and-subtask-lifecycle.md) — 이 팩토리가
  스레드를 만드는 시점
- [구조가 드러나는 스레드 덤프](../concepts/structured-thread-dumps.md) — 이름과 팩토리가
  실제로 값을 내는 자리
- [구조적 스코프의 예외 처리](../concepts/exception-handling-in-structured-scopes.md) —
  `TimeoutException`과 `FailedException`을 함께 잡는 자리
- [스레드 풀 실행자 설정](../concepts/thread-pool-executor-configuration.md) — 같은 일을
  스레드 풀 쪽에서 하던 방식
- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 둘의 차이
- [자바의 구조적 동시성](../synthesis/structured-concurrency-in-java.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 4장 "Structured Concurrency" — §"Configuration"(pp.179–185),
    그 안의 "Understanding Configuration"(pp.179–180), "Named threads"(pp.180–181),
    "Timeout configuration"(pp.181–183), "Combining configuration options"(pp.183–185);
    플랫폼 스레드 항목은 §"In Closing"(p.214). 인용한 코드는 pp.183–184의
    `ComprehensiveConfigurationExample.main`이고, 조판 줄바꿈을 폈으며 원문의
    `System.out.println` 호출 네 줄과 catch 블록 셋을 깎았다 — 남긴 부분만으로 세 구성이
    함께 걸리는 모양이 보인다. 개념당 대표 코드 하나 규칙에 따라 남긴 것: 기본 구성 예제(p.179),
    `sealed interface Configuration` 선언과 기본 패턴 두 조각(p.180), `NamedThreadExample`
    전문(pp.180–181), `TimeoutExample` 전문(pp.181–182), 세 API 흉내 메서드(pp.184–185),
    `demonstratePlatformThreads`(p.214). 실행 출력(p.181, p.183)도 미수록이고 본문이 말한
    수치만 옮겼다.

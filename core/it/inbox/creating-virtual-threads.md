---
type: concept
title: 가상 스레드를 만드는 방법
description: 가상 스레드를 만드는 네 가지 표기 — 한 줄짜리 정적 메서드, 스레드 빌더 API의 즉시 시작과 지연 시작, 태스크마다 가상 스레드를 만드는 실행자, 그리고 처음 쓰는 사람이 반드시 부딪히는 데몬 기본값 함정
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드를 만드는 방법

- [버전 조건](#버전-조건)
- [환경 준비](#환경-준비)
- [가장 짧은 표기와 데몬 함정](#가장-짧은-표기와-데몬-함정)
- [스레드 빌더 API](#스레드-빌더-api)
- [실행자로 갈아타기](#실행자로-갈아타기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드를 만드는 표기에는 무엇이 있고 각각 어디에 쓰는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 아래 표기들이 정식으로 쓸 수 있게 된 릴리스부터 적용된다.

## 환경 준비

- 경계가 한 문장에 있다 — 프로젝트 룸의 가상 스레드는 JDK 21부터 안정 기능이므로, 쓰려면
  JDK 21이 설치되어 있어야 한다 (2장, p.34).[^rahman2025]
- 여러 JDK 버전을 다루는 도구로 저자는 SDKMAN을 권한다. `sdk list java`로 설치 가능한 버전을
  훑고 `sdk install java 21.0.2-open` 같은 명령으로 배포판을 지정해 설치한다 (2장,
  pp.34–35).[^rahman2025]
- 저자는 이 장의 기준을 JDK 21로 밝힌다 — 운영 환경에서 가상 스레드에 가장 널리 쓰이는 버전이기
  때문이고, 스코프 값과 구조적 동시성 같은 더 새 기능을 다루는 자리에서는 최신 JDK로 옮긴다
  (2장, p.35).[^rahman2025]

## 가장 짧은 표기와 데몬 함정

- 단순한 쓰임에는 `Thread.startVirtualThread()` 정적 메서드가 곧바로 간다. `Runnable`을 받으므로
  람다 식을 넘길 수 있다 (2장, p.36).[^rahman2025]
- **그런데 그것만으로는 아무것도 찍히지 않는다** — 자바의 가상 스레드는 기본이 데몬 스레드이고,
  그것을 만든 주 스레드가 끝나면 가상 머신이 남은 데몬 스레드를 종료시키기 때문이다 (2장,
  p.36).[^rahman2025]
- 그래서 태스크가 끝나는 것을 보려면 기다려야 한다 (2장, p.36).[^rahman2025]

  ```java
  public static void main(String[] args) throws InterruptedException {
      Thread vThread = Thread.startVirtualThread(() -> {
          System.out.println("Virtual threads make concurrency effortless!" +
              "See for yourself.");
      });
      vThread.join();
  }
  ```

## 스레드 빌더 API

- 생성을 더 통제하려면 스레드 빌더 API를 쓴다. `Thread.ofVirtual().start(...)`는 만들면서 곧바로
  시작하고, `Thread.ofVirtual().unstarted(...)`는 시작하지 않은 스레드를 만들어 두었다가 나중에
  `start()`로 시작한다 (2장, p.36).[^rahman2025]

## 실행자로 갈아타기

- 애플리케이션이 이미 실행자를 쓰고 있으면 `Executors.newVirtualThreadPerTaskExecutor()`로
  매끄럽게 옮겨 갈 수 있고, 저자는 이것이 당장 리팩터링하기 어려운 큰 프로젝트에서 특히 쓸모
  있다고 적는다 (2장, p.36).[^rahman2025] 그 한 줄 교체의 앞뒤 모습은
  [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md)에 있다.
- 표기가 여럿인 이유가 마무리에 있다 — 이 여러 방법 덕분에 기존 코드베이스에 가상 스레드를
  매끄럽게 들여, 익숙한 코딩 패턴과 추상을 유지하면서 성능·확장성·자원 효율의 이득을 얻을 수 있다
  (2장, pp.36–37).[^rahman2025]

## 이어지는 페이지

- [가상 스레드에서 달라지는 Thread API](../concepts/virtual-thread-api-semantics.md) — 만든
  다음의 규칙들
- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 무엇을
  만들고 있는가
- [자바 스레드의 생성과 시작](../concepts/java-thread-creation-and-start.md) — 플랫폼 스레드
  쪽의 네 표기
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 갈아탈
  자리의 원래 모습
- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 한 줄
  교체가 주는 이득
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Setting Up Your Environment
    for Virtual Threads"(pp.34–35), "Creating Virtual Threads in Java"(pp.36–37). 그림
    2-2(`sdk list java` 출력 화면)는 옮기지 않았다. 개념당 대표 코드 하나 규칙에 따라 `main`
    예제만 실었고, `Thread.startVirtualThread` 단독 조각과 빌더 API 두 조각,
    `newVirtualThreadPerTaskExecutor` 조각(모두 p.36)은 미수록이다 — 서술은 모두 옮겼다.

---
type: concept
title: 가상 스레드 스케줄러
description: 가상 스레드를 캐리어 스레드에 배분하는 것의 정체 — 선입선출로 도는 작업 훔치기 ForkJoinPool이며 병렬 스트림이 쓰는 공용 풀과는 다른 풀이라는 것, 병렬성 기본값이 가용 프로세서 수라는 것, 그리고 그것을 바꾸는 시스템 속성과 그 속성을 언제 세워야 하는가
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드 스케줄러

- [버전 조건](#버전-조건)
- [스케줄러의 정체](#스케줄러의-정체)
- [병렬성이라는 손잡이](#병렬성이라는-손잡이)
- [언제 세워야 하는가](#언제-세워야-하는가)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드를 실제로 캐리어에 배분하는 것은 무엇이고, 어디를 조절할 수 있는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 가상 스레드가 정식 기능이 된 릴리스부터 적용된다. 여기 적힌
> 시스템 속성 이름과 기본값도 그 이후 구현의 것이다.

## 스케줄러의 정체

- 구현이 명시되어 있다 — 가상 머신 안에 구현된 가상 스레드 스케줄러는 작업 훔치기(work-stealing)
  `ForkJoinPool`에 기반하며 선입선출(First-In, First-Out) 모드로 동작한다 (2장,
  p.32).[^rahman2025] 작업 훔치기 자체는
  [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md)에 있다.
- **공용 풀과 다른 풀이다** — 이 `ForkJoinPool`이 가상 스레드 스케줄링의 바탕이고, 병렬 스트림
  구현처럼 다른 용도로 쓰이는 공용 풀(common pool)과는 구분된다. 공용 풀은 후입선출(Last-In,
  First-Out) 모드로 동작한다 (2장, p.32).[^rahman2025]
- 이 구분이 이전 소스의 서술을 정확하게 만든다 —
  [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)이 옮긴 "룸의 기본
  스케줄러는 `ForkJoinPool`"이라는 서술과 같은 대상을 가리키며, 여기서는 그 풀이 캐리어 스레드를
  담고 있고 모드가 선입선출이라는 것까지 적힌다.

## 병렬성이라는 손잡이

- 병렬성의 정의가 스레드 수다 — 가상 스레드 스케줄러의 병렬성(parallelism)은 가상 스레드
  스케줄링에 쓸 수 있는 플랫폼 스레드의 수를 뜻하며, 설정 가능한 매개변수다 (2장,
  p.32).[^rahman2025]
- 기본값은 시스템의 가용 프로세서 수로 잡혀 하드웨어 자원을 최적으로 쓰게 한다 (2장,
  p.32).[^rahman2025]
- 조절 지점은 `jdk.virtualThreadScheduler.parallelism` 시스템 속성이고, 애플리케이션 요구와
  작업 부하 성격에 맞춰 병렬성 수준을 조정할 수 있다 (2장, p.32).[^rahman2025]

## 언제 세워야 하는가

- 자바 애플리케이션을 시작할 때 `-D` 명령줄 옵션으로 시스템 속성을 세울 수 있다 (2장,
  p.32).[^rahman2025]

  ```sh
  java -Djdk.virtualThreadScheduler.parallelism=4 -jar yourApp.jar
  ```

- 코드 안에서는 `System.setProperty(key, value)` 메서드를 쓴다 (2장, p.32).[^rahman2025]
- **순서가 조건이다** — 이 설정들은 처음 쓰이기 전에 조정되어야 하며, 보통 `main` 메서드의 첫
  부분이나 스프링·자카르타 EE·쿼커스 애플리케이션 컨텍스트가 뜨기 전에 한다 (2장,
  p.32).[^rahman2025]

## 이어지는 페이지

- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 이
  스케줄러가 배분하는 두 종류
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 이 스케줄러가
  물려받은 구조
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 스케줄러가 옮기는 대상의 실물
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 후속문과 스케줄러의
  분리를 가상 머신 안쪽에서 본 자리
- [자바 스레드 스케줄링과 상태 전이](../concepts/java-thread-scheduling-and-states.md) — 플랫폼
  스레드 쪽의 배분
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "What Is a Virtual
    Thread?"(pp.31–32). 인용한 명령은 원문 그대로이며 조판 강조 표기만 뗐다.

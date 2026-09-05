---
type: concept
title: 구조적 동시성 스코프
description: 태스크를 스코프 안에서 돌려 하나가 실패하거나 시간이 다하면 나머지를 자동으로 취소하는 구조, 그것이 답하는 결함인 예외 전파와 무한정 블로킹, 그리고 선언적 스타일이라는 효과 — 이 소스의 2장이 예고 수준으로 소개하는 범위
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 구조적 동시성 스코프

- [버전 조건](#버전-조건)
- [무엇에 답하는가](#무엇에-답하는가)
- [스코프라는 구조](#스코프라는-구조)
- [실패 즉시 중단](#실패-즉시-중단)
- [선언적 스타일](#선언적-스타일)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **동시에 던진 태스크들의 예외와 타임아웃을 무엇이 대신 책임지게 할 수 있는가.**

## 버전 조건

> **버전 조건**: JDK 25 + 미리 보기 기능 활성화(`--enable-preview`). 아래 예제 코드가 요구하는
> 조건이며, 구조적 동시성(structured concurrency)은 이 소스의 집필 시점에 아직 미리 보기다.
> **정식 기능이 아니므로 API 모양이 바뀔 수 있다.**

## 무엇에 답하는가

- 앞선 방식의 결함이 출발점이다 — `Future::get`이 예외를 던질 수 있고, 타임아웃 장치가 없으면
  무한정 블로킹될 가능성이 있다 (2장, p.50).[^rahman2025] 그 방식은
  [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)에
  있다.
- 답의 이름과 출처가 명시된다 — 자바의 JEP 505가 구조적 동시성을 들이며, 목표는 튼튼한 동시
  코드를 쓰는 일을 단순하게 만드는 것이다 (2장, p.50).[^rahman2025]

## 스코프라는 구조

- API가 주는 것은 태스크가 도는 구조화된 스코프이고, 그중 하나라도 실패하거나 시간이 다하면
  스코프 안의 모든 태스크가 자동으로 취소된다 (2장, p.50).[^rahman2025]

  ```java
  public static void main(String[] args) {
      try (StructuredTaskScope scope = StructuredTaskScope.open()) {
          StructuredTaskScope.Subtask<String> subtask1 =
              scope.fork(() -> fetchData("https://api1.example.com"));
          StructuredTaskScope.Subtask<String> subtask2 =
              scope.fork(() -> fetchData("https://api2.example.com"));
          scope.join();
          var result = subtask2.get() + subtask1.get();
          System.out.println(result);
      } catch (InterruptedException e) {
          throw new RuntimeException(e);
      }
  }
  ```

## 실패 즉시 중단

- 실패 즉시 중단(fail-fast) 스코프는 타임아웃을 줄 수 있게 하고 예외를 감싸기 아주 쉽게 만든다
  (2장, p.50).[^rahman2025]
- 동작이 한 줄이다 — 스코프 안에서 갈라져 도는 하위 태스크 가운데 하나가 예외를 일으켜 실패하거나
  타임아웃이 지나면, 스코프 안에서 도는 모든 태스크가 취소되고 예외가 되돌아 전파된다. 그 결과
  코드가 더 깔끔하고 튼튼해지며, 예외 전파와 타임아웃이 내장 구성물 안에 담긴다 (2장,
  p.50).[^rahman2025]

## 선언적 스타일

- 저자가 자바 동시성의 진전으로 꼽는 자리다 — 태스크를 돌리는 구조화된 스코프를 제공함으로써 API가
  자동 취소와 예외 처리를 맡고, 그것을 손으로 관리하던 개발자의 부담을 덜어 준다 (2장,
  pp.50–51).[^rahman2025]
- 효과가 스타일로 나타난다 — 구조적 동시성은 더 선언적인 프로그래밍 스타일을 북돋아, 스레드를
  만들고 관리하거나 복잡한 취소 논리를 구현하는 낮은 수준의 세부 대신 개발자가 더 높은 수준의
  태스크에 집중하게 한다 (2장, p.51).[^rahman2025]

## 이어지는 페이지

- [가상 스레드로 비동기 결과 모으기](../concepts/aggregating-async-results-with-virtual-threads.md)
  — 이 구조가 답하는 결함이 나온 자리
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 예외와
  조합을 다루던 앞선 API
- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 스코프가
  대신하는 수명 주기 관리
- [자바 동시 실행 모델](../synthesis/java-concurrent-execution-models.md) — 이 페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "The Promise of Structured
    Concurrency"(pp.50–51). 이 소스에서 구조적 동시성을 본격적으로 다루는 곳은 4장이고, 이
    페이지가 담은 것은 2장의 소개 범위다. 인용한 코드는 원문 그대로이며 조판 줄바꿈만 폈다.

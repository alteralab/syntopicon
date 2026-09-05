---
type: synthesis
title: 자바 동시 실행 모델
description: 자바 애플리케이션이 일을 동시에 시키려고 써 온 방식들의 진입점 — 스레드를 손수 만들던 자리, 요청당 스레드가 부딪힌 메모리와 상한과 문맥 전환의 값, 그 위에 차례로 겹쳐 온 실행자와 포크조인 풀과 CompletableFuture와 리액티브, 그 답들이 안에서 실제로 도는 역학(스레드 풀의 구조와 설정과 종류, Callable과 Future, 작업 의존이 만드는 교착), 마지막으로 그 대가들을 피하려는 가상 스레드
generated: { by: "claude-opus-5", at: "2026-09-05T06:00:00Z" }
---

# 자바 동시 실행 모델

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **자바 애플리케이션이 여러 일을 동시에 시키려고 쓰는
수단들** — 스레드를 직접 만들고 시작하는 자리, 그 스레드가 비싸고 유한하다는 사실, 그리고 그 사실을
피해 가려고 라이브러리와 언어가 차례로 내놓은 실행 모델들 — 이 사는 자리다.

가상 머신이 무엇을 보장하는가는 여기 살지 않는다. 메모리 모델과 가시성과 락 최적화처럼 **가상 머신이
하는 일**은 [자바 메모리 모델과 동시성](java-memory-model-and-concurrency.md)이 담당하고, 그 허브가
스스로 `java.util.concurrent`의 API 카탈로그를 자기 범위 밖으로 그어 두었다. 이 허브가 그 바깥,
곧 **라이브러리와 API를 쓰는 쪽**을 맡는다.

읽는 순서가 있다. 바탕이 되는 스레드를 먼저 보고, 그 스레드가 비싸다는 사실과 막힌다는 사실을 지나,
그 두 사실에 답해 온 실행 모델들을 차례로 밟은 뒤, 마지막이 그 답들의 대가를 피하려는 쪽이다.

## 바탕

- [자바 플랫폼의 바탕인 스레드](../concepts/threads-as-java-platform-substrate.md) — 스레드가
  무엇을 공유하고 무엇을 따로 갖는가, 병렬성과 동시성이 다른 말인 이유, 예외와 디버거와 프로파일러가
  모두 스레드에 기대어 성립한다는 것
- [자바 스레드의 생성과 시작](../concepts/java-thread-creation-and-start.md) — 상속과 구현과
  익명 클래스와 람다라는 네 표기, 상속 슬롯이 갈라 놓은 선호, `start`가 `run`보다 더 하는 일

## 왜 다시 짜야 했나

- [스레드의 숨은 비용](../concepts/hidden-costs-of-threads.md) — 요청당 스레드 모델과 처리량의
  정의, 스레드당 힙 밖 발자국과 페이징, 운영 체제가 정하는 상한, 문맥 전환의 CPU 값
- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 진짜 비효율은
  유휴가 아니라 묶임이라는 지적, 의존 없는 호출을 갈라 던지는 첫 수단과 그 대가

## 겹쳐 온 답들

- [실행자 프레임워크와 그 한계](../concepts/executor-framework-and-its-limits.md) — 스레드 수를
  통제하고 수명 주기를 대신 맡는 구조, 그리고 남은 세 한계
- [포크조인 풀과 작업 훔치기](../concepts/fork-join-pool-and-work-stealing.md) — 워커마다 큐를 두어
  캐시를 살리고 노는 스레드를 없애는 설계
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 콜백을 변환의
  체인으로 바꾸는 API와 그 학습·디버깅 값
- [자바 리액티브 프레임워크의 대가](../concepts/reactive-frameworks-tradeoffs-in-java.md) — 스트림과
  이벤트로 가는 패러다임이 요구하는 여섯 가지 대가

## 그 답들의 역학

앞의 답들이 무엇을 약속하는가를 넘어, 안에서 실제로 무엇이 도는가를 보는 자리다.

- [스레드 풀의 이유와 내부 구조](../concepts/thread-pool-rationale-and-internals.md) — 왜 미리
  만들어 두어야 하는가, 큐와 워커라는 두 부품, 그리고 최소 구현에서 드러나는 여섯 가지 설계 결정
- [ThreadPoolExecutor 설정과 풀 크기](../concepts/thread-pool-executor-configuration.md) —
  팩토리 뒤에 있는 하나의 구현과 그 일곱 매개변수, 코어와 최대 크기, CPU 대 I/O의 갈림
- [JDK 실행자 프레임워크의 스레드 풀 종류](../concepts/jdk-thread-pool-types.md) — 고정과 캐시드와
  단일과 스케줄드와 작업 훔치기, 그리고 각각의 쓸 자리
- [Callable과 Future로 결과 받기](../concepts/callable-and-future-results.md) — 결과를 돌려받는
  두 인터페이스와 막는 `get`
- [의존하는 하위 작업과 스레드 풀의 교착](../concepts/recursive-task-decomposition-deadlock.md) —
  풀이 작업 사이의 의존을 모를 때 벌어지는 일과 포크조인이 그것을 푸는 방식

## 그다음

- [애플리케이션에서 본 가상 스레드](../concepts/virtual-threads-in-application-code.md) — 실행자 한
  줄을 바꿔 얻는 이득과 블로킹을 만나면 제어를 넘기는 동작

## 경계에 있는 페이지

- [거짓 공유와 캐시 일관성](../concepts/false-sharing-and-cache-coherence.md) — 실행 모델이 아니라
  그 밑의 하드웨어가 만드는 값
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 같은 가상 스레드를 가상
  머신 안쪽에서 본 자리
- [스레드 구현 모델](../concepts/thread-implementation-models.md) — `Thread` 객체 하나가 무엇에
  매핑되는가
- [자바 스레드 스케줄링과 상태 전이](../concepts/java-thread-scheduling-and-states.md) — 배분 방식을
  프로그램이 어디까지 통제하는가
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 실행기 추상과
  비동기 전염 문제를 파이썬 쪽에서 본 자리

## 자식 허브

- [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md) — 가상 스레드 하나를
  열어 본 자리들: 스케줄러와 마운트 기제, 확장의 근거와 조건, 핀닝과 ThreadLocal이라는 한계,
  그리고 그것을 재고 옮기는 운영 도구들
- [자바의 구조적 동시성](structured-concurrency-in-java.md) — 갈라 놓은 서브태스크를 하나의 일로
  묶는 원칙과 그것을 구현한 `StructuredTaskScope`, 그리고 조인 정책들

## 이어지는 허브

- [자바 메모리 모델과 동시성](java-memory-model-and-concurrency.md) — 이 모델들이 얹히는 가상 머신
  쪽의 보장과 최적화
- [자바 기술 시스템](java-technology-system.md) — 이 코드를 돌리는 가상 머신과 JDK

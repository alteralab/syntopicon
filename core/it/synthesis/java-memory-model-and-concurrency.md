---
type: synthesis
title: 자바 메모리 모델과 동시성
description: 여러 스레드가 같은 데이터를 만질 때 무엇이 언제 보이는지를 정하는 규칙과, 그 규칙을 지키면서도 빠르게 만드는 장치들의 진입점 — 메인 메모리와 작업 메모리를 오가는 여덟 연산, `volatile`과 선 발생 원칙, 자바 스레드가 커널 스레드에 매핑되는 방식과 JDK 21의 가상 스레드, 스레드 안전성의 다섯 등급, 그리고 스핀·락 제거·경량 락·편향 락으로 이어지는 락 최적화
generated: { by: "claude-opus-5", at: "2026-08-15T00:00:00Z" }
---

# 자바 메모리 모델과 동시성

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **여러 스레드가 데이터를 공유할 때 가상 머신이 무엇을
보장하고 그 보장을 어떻게 싸게 만드는가** — 자바 메모리 모델이 정한 가시성·원자성·순서의 규칙, 그
규칙 위에서 안전성을 얻는 수단들, 스레드 자체가 구현되고 스케줄링되는 방식, 그리고 락의 비용을 깎는
가상 머신 내부의 최적화 — 가 사는 자리다. `java.util.concurrent`의 API 카탈로그는 여기 살지 않는다.
이 허브는 **가상 머신이 하는 일**까지만 다루고, 라이브러리 사용법은 다루지 않는다(소스인 zhou2024
자신이 "이 책의 주제는 동시성 프로그래밍이 아니라 자바 가상 머신"이라고 범위를 그었다). 스레드가
쓰는 **메모리 영역**은 [JVM 자동 메모리 관리](jvm-memory-management.md)가, 락을 제거해 주는
**컴파일러 최적화**는 [백엔드 컴파일과 최적화](backend-compilation-and-optimization.md)가 담당한다.

읽는 순서가 있다. 하드웨어가 만든 문제와 그 위에 세운 모델을 먼저 보고, 모델이 개발자에게 주는
판정 도구로 올라온 뒤, 그 모델이 얹히는 스레드의 실물을 지나, 마지막이 안전성을 얻는 값과 그 값을
깎는 방법이다.

## 무엇이 언제 보이는가 — 모델

- [자바 메모리 모델](../concepts/java-memory-model.md) — 메인 메모리와 스레드별 작업 메모리라는 두
  층, 그 사이를 오가는 여덟 가지 원자적 연산과 조합 규칙, 이 모델이 다루는 '변수'의 좁은 범위
- [volatile 변수](../concepts/volatile-variables.md) — 가시성과 재정렬 금지만 보장하고 원자성은
  보장하지 않는 경계, `race++`가 20만을 못 채우는 실물, `lock addl $0x0,(%esp)`라는 메모리 장벽
- [long과 double 변수의 비원자성](../concepts/nonatomic-treatment-of-long-and-double.md) — 원자성
  보장에 뚫린 64비트 구멍과, 주류 플랫폼에서는 관측되지 않는다는 실측

## 어떻게 판정하는가 — 도구

- [원자성·가시성·실행 순서와 선 발생 원칙](../concepts/happens-before-and-jmm-guarantees.md) — 세
  특징을 각각 맡는 `synchronized`·`volatile`·`final`, 규칙 여덟 개로 게터/세터 한 쌍을 판정하기,
  그리고 '시간상 먼저'와 '선 발생'에 인과가 없다는 결론

## 그 모델이 얹히는 실물 — 스레드

- [스레드 구현 모델](../concepts/thread-implementation-models.md) — 커널 스레드 1:1, 사용자 스레드
  1:N, 하이브리드 M:N과 각각의 값, 그리고 자바가 그린 스레드를 버린 경위
- [자바 스레드 스케줄링과 상태 전이](../concepts/java-thread-scheduling-and-states.md) — 협력적 대
  선점형, 우선순위 10단계가 뭉개지는 자리, 여섯 상태와 각 상태로 보내는 메서드
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 문맥 전환 비용의 정체,
  스레드 스택 1MB 대 코루틴 수백 바이트, 룸 프로젝트가 JDK 21에 들인 N:1 구조

## 안전성을 어떻게 얻는가

- [스레드 안전성의 다섯 등급](../concepts/thread-safety-levels.md) — 이분법을 버린 분류(불변·절대적·
  조건부·호환·적대적)와, 모든 메서드가 `synchronized`인 `Vector`조차 절대적이지 않은 이유
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 비관적인 상호 배제
  동기화, 낙관적인 CAS와 그 ABA 허점, 그리고 공유 자체를 없애는 재진입 코드와 스레드 로컬 저장소

## 그 값을 어떻게 깎는가

- [락의 구현과 최적화](../concepts/lock-optimization.md) — 스핀 락과 적응형 스핀, 탈출 분석이
  근거를 대는 락 제거, 락 범위 확장, 마크 워드를 CAS로 맞바꾸는 경량 락, 그리고 JDK 18에서 제거된
  편향 락

## 경계에 있는 페이지

- [탈출 분석](../concepts/escape-analysis.md) — 락 제거의 근거를 대는 분석(그쪽 이름은 '동기화 제거')
- [객체 생성과 메모리 레이아웃](../concepts/object-creation-and-memory-layout.md) — 경량 락과 편향
  락이 겹쳐 쓰는 마크 워드가 들어앉은 객체 헤더
- [스택 프레임의 구조](../concepts/stack-frame-structure.md) — 락 레코드가 만들어지고 지역 변수가
  스레드 프라이빗으로 남는 자리
- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 이 모델과 "아무런
  관련이 없다"고 소스가 선을 그은 다른 층위의 메모리 구분
- [동시성 제어 분류](../concepts/concurrency-control-classification.md) — 비관적·낙관적이라는 같은
  축을 데이터베이스 트랜잭션 쪽에서 본 자리

## 이어지는 허브

- [자바 기술 시스템](java-technology-system.md) — 이 스레드들을 돌리는 가상 머신과 JDK
- [JVM 자동 메모리 관리](jvm-memory-management.md) — 스레드가 나눠 쓰는 메모리 영역과 회수 장치
- [백엔드 컴파일과 최적화](backend-compilation-and-optimization.md) — 락을 제거하고 재정렬을
  일으키는 JIT 컴파일러 쪽
- [데이터베이스 트랜잭션](database-transactions.md) — 같은 '동시성'을 저장 시스템의 격리 수준으로
  푸는 쪽

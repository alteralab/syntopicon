---
type: synthesis
title: 리액티브 자바와 논블로킹 I/O
description: 가상 스레드 이전에 자바가 막힘을 피하려고 써 온 길의 진입점 — 스레드가 기다리지 않게 만드는 논블로킹 I/O의 정의와 NIO의 채널과 버퍼와 셀렉터, 그것을 직접 지을 때 손으로 감당하게 되는 상태와 스레드 규율, 프레임워크가 그 루프를 대신 돌 때 남는 하나의 규칙, 그 위에 얹히는 리액티브 스트림 규격과 배압, 그리고 가상 스레드와 나란히 놓았을 때 각자가 남는 자리
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
---

# 리액티브 자바와 논블로킹 I/O

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **스레드가 입출력을 기다리며 막히지 않게 만드는
길**이 사는 자리다. 아래층은 운영 체제의 준비 상태 알림에 기대는 논블로킹 I/O이고, 위층은 그 위에
얹혀 더 높은 수준의 API를 주는 리액티브 스트림이다. 이 두 층의 관계는 소스가 스스로 그렇게 그린
것이다 — 프레임워크가 이벤트 루프로 연결을 관리하고, 리액티브 프레임워크가 그 위에 앉는다.

같은 막힘 문제를 **논블로킹 없이** 푸는 쪽은 여기 살지 않는다. 스레드를 값싸게 만들어 막혀도 되게
하는 길은 형제 허브인 [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md)이
담당한다. 이 허브의 마지막 페이지가 그 둘을 나란히 놓는 자리다.

읽는 순서가 있다. 두 모델의 정의를 먼저 보고, 그것을 직접 지을 때의 부품과 규율을 지나, 프레임워크가
대신 돌 때 남는 규칙을 밟은 뒤, 마지막이 그 위에 얹히는 리액티브 층과 선택의 문제다.

## 무엇이 다른가

- [블로킹 I/O와 논블로킹 I/O](../concepts/blocking-versus-non-blocking-io.md) — 두 모델의 정의와
  단일 스레드 서버가 느린 요청 하나에 통째로 멈추는 것을 잰 실측, 그리고 스레드를 늘리는 답의 상한
- [리액티브 프로그래밍이라는 패러다임](../concepts/reactive-programming-paradigm-definition.md) —
  이 길 전체에 붙는 이름의 정의와 리액티브 선언문의 네 원칙

## 직접 지을 때의 부품

- [자바 NIO의 채널과 버퍼](../concepts/java-nio-channels-and-buffers.md) — 준비 상태 기반 API의
  정의, 스트림 중심과 버퍼 중심의 갈림, 버퍼가 시스템 호출을 줄이고 제로 카피를 얻는 방식
- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 채널 여럿을 스레드 하나로
  지키는 부품과 네 가지 관심 이벤트, 그리고 루프의 뼈대
- [SelectionKey의 스레드 안전 오해](../concepts/selection-key-thread-safety.md) — 문서 한 줄이 만든
  오해와 어길 때 벌어지는 넷, 갱신을 큐로 돌리는 패턴
- [논블로킹 서버가 직접 감당하는 상태](../concepts/hand-written-non-blocking-server-state.md) —
  연결마다의 상태 객체, 부분 읽기와 부분 쓰기, 쓰기 관심을 켜고 끄는 규칙

## 프레임워크가 대신 돌 때

- [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md) — 이벤트
  기반 프레임워크의 층 구조와 단 하나의 규칙, 그리고 워커 풀로 우회할 때 문맥 전환이 무는 값
- [비동기 API의 모양과 콜백 지옥](../concepts/async-api-shapes-and-callback-hell.md) — 막지 않는
  코드를 쓰는 가장 단순한 모양과 그것이 오래가지 못하는 이유

## 그 위에 얹히는 층

- [리액티브 스트림 규격과 네 구성 요소](../concepts/reactive-streams-specification-components.md) —
  발행자와 구독자와 구독과 프로세서, 세 가지 신호, 두 라이브러리의 타입
- [배압과 리액터의 다섯 전략](../concepts/backpressure-strategies-in-reactive-streams.md) — 소비자가
  따라가지 못할 때 보내는 신호와 버퍼·폐기·최신 값·오류라는 갈래들
- [자바 리액티브 프레임워크의 대가](../concepts/reactive-frameworks-tradeoffs-in-java.md) — 이 층을
  고를 때 내주는 것과 얻는 것

## 무엇을 고를 것인가

- [가상 스레드 시대에 리액티브가 남는 자리](../concepts/reactive-and-virtual-threads-coexistence.md)
  — 같은 시스템을 두 방식으로 지었을 때의 차이, 저자의 판단, 그리고 수렴의 조짐

## 경계에 있는 페이지

- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 같은 준비 상태 감시를 가상
  머신이 대신 도는 자리. 그쪽은 가상 스레드 허브가 담당한다
- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 같은 막힘을
  애플리케이션 코드 쪽에서 본 자리
- [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md) — 값 하나까지는
  덮어 주는 앞 단계의 답
- [동시 실행기와 asyncio](../concepts/concurrent-executors-and-asyncio.md) — 같은 이벤트 루프
  개념을 파이썬 쪽에서 본 자리
- [자바 가상 머신의 런타임 데이터 영역](../concepts/jvm-runtime-data-areas.md) — 다이렉트 버퍼가
  쓰는 힙 밖 메모리
- [분산 컴퓨팅의 오류들](../concepts/fallacies-of-distributed-computing.md) — 같은 배압을 분산
  시스템 층에서 본 자리

## 이어지는 허브

- [자바 동시 실행 모델](java-concurrent-execution-models.md) — 이 허브의 부모, 곧 자바가 일을
  동시에 시키려고 써 온 수단들의 계보
- [가상 스레드의 내부와 운영](virtual-thread-internals-and-operations.md) — 같은 문제를 다른 길로
  푸는 형제 허브
- [자바의 구조적 동시성](structured-concurrency-in-java.md) — 저자가 수렴의 한 방향으로 꼽는 원칙이
  사는 형제 허브

---
type: concept
title: SelectionKey의 스레드 안전 오해
description: 자바 문서의 문장이 만드는 흔한 오해와 그 문장이 실제로 뜻하는 것, 셀렉터 루프 밖에서 관심 연산을 바꿀 때 벌어지는 네 가지, 그리고 갱신을 큐에 넣어 셀렉터 스레드가 처리하게 하는 패턴
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# SelectionKey의 스레드 안전 오해

- [문서 한 줄이 만든 오해](#문서-한-줄이-만든-오해)
- [어길 때 벌어지는 넷](#어길-때-벌어지는-넷)
- [규칙과 그 구현](#규칙과-그-구현)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **셀렉터 루프 밖의 스레드가 선택 키의 관심 연산을 바꿔도 되는가.**

## 문서 한 줄이 만든 오해

- 저자가 흔한 오해 하나를 정면으로 다룬다 — 선택 키(selection key)가 여러 스레드에서 동시에 쓰기에
  안전하다는 자바 문서의 문장 때문에 많은 개발자가 어느 스레드에서든 `interestOps`를 바꿔도 된다고
  믿는다 (6장 "Blocking Versus Non-blocking I/O", p.267).[^rahman2025]
- 실제로 그 문장이 뜻하는 것은 훨씬 좁다 — 키의 속성을 **읽는** 일이 메모리 손상을 일으키지 않는다는
  뜻일 뿐이다. `interestOps()` 같은 연산이 원자적이라거나 동시 수정에 안전하다는 뜻이 아니다 (6장,
  p.267).[^rahman2025]
- 위험한 자리가 특정된다 — `selector.select()`가 실행되는 동안 선택 키의 `interestOps`를 바꾸는
  것이다 (6장, p.267).[^rahman2025]

## 어길 때 벌어지는 넷

- 그때 일어날 수 있는 것이 넷이다 (6장, p.267):[^rahman2025]
  - `interestOps` 변경이 유실되는 경쟁 조건(race condition).
  - 놓친 I/O 이벤트.
  - `CancelledKeyException` 오류.
  - 일관되지 않은 동작. 저자는 이것이 흔히 높은 부하에서만 드러난다고 덧붙인다.
- 마지막 항목이 이 오해가 오래 살아남는 이유다 — 낮은 부하에서는 증상이 나타나지 않는다.

## 규칙과 그 구현

- 규칙은 하나다 — 선택 키의 `interestOps`는 언제나 셀렉터 루프를 도는 그 스레드에서 바꾼다 (6장,
  p.267).[^rahman2025]
- 그래서 예제 서버가 대기 갱신 큐 패턴을 쓴다. 모든 수정이 셀렉터 스레드 안에서 안전하게 일어나도록
  보장하기 위해서다 (6장, p.267).[^rahman2025]
- 문제의 형태가 먼저 정리된다 — 선택 키 객체는 스레드 안전하지 않으므로 비동기 처리 스레드에서 직접
  수정할 수 없다. 대신 스레드 사이 통신에 스레드 안전한 큐를 쓴다 (6장, p.261).[^rahman2025]

  ```java
  private void processPendingUpdates() {
      PendingUpdate update;
      while ((update = pendingUpdates.poll()) != null) {
          if (update.key.isValid()) {
              update.key.interestOps(
                  update.key.interestOps() | SelectionKey.OP_WRITE);
          }
      }
  }
  ```

- 반대편이 짝을 이룬다 — 비동기 스레드는 선택 키를 직접 고치는 대신 갱신을 큐에 넣고, 주 셀렉터
  스레드가 그것을 처리한다. 저자는 이것이 NIO 애플리케이션에서 스레드 안전을 지키는 결정적
  패턴이라고 적는다 (6장, p.267).[^rahman2025]
- 큐에 넣은 다음 `selector.wakeup()`을 부른다. 이벤트 루프가 이 갱신을 제때 집어 가게 하는
  자리다 (6장, p.266).[^rahman2025]
- 루프의 머리에서 이 큐를 먼저 비우는 이유도 저자가 적는다 — 이벤트를 처리하기 전에 비동기 스레드가
  큐에 넣어 둔 셀렉터 갱신을 먼저 다룬다. 이 단계가 서버를 죽일 수 있는 경쟁 조건을 막는다 (6장,
  p.260).[^rahman2025]

## 이어지는 페이지

- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 이 규칙이 걸리는 그 루프
- [논블로킹 서버가 직접 감당하는 상태](../concepts/hand-written-non-blocking-server-state.md) —
  같은 서버에서 손으로 관리하게 되는 나머지
- [스레드 안전성 구현 수단](../concepts/thread-safety-implementation.md) — 무엇이 스레드 안전하다는
  말의 층위
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    대기 갱신 큐(pp.260–262), 선택 키 스레드 안전 절(p.267). 인용한 `processPendingUpdates`는
    원문(p.261)에서 예외 처리 블록만 뺐다. 짝을 이루는 `PendingUpdate` 레코드 클래스(p.262)와
    `processAllPendingRequests`(p.266)는 개념당 대표 코드 하나 규칙에 따라 옮기지 않았다.
    자바 문서 문장은 저자가 인용한 것을 한국어로 옮겼고 원문 표기는 `archive/` 스냅샷에 있다.

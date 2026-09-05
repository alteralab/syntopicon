---
type: concept
title: NIO 셀렉터와 이벤트 루프
description: 셀렉터가 채널 여럿을 스레드 하나로 관리하는 교통 정리자 역할과 네 가지 관심 이벤트, 구현이 운영 체제별로 갈린다는 것, 그리고 논블로킹 설정과 등록과 선택 키 순회로 이루어진 단일 스레드 이벤트 루프의 뼈대와 무한 대기가 아니라 타임아웃을 주는 이유
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# NIO 셀렉터와 이벤트 루프

- [셀렉터가 하는 일](#셀렉터가-하는-일)
- [구현은 운영 체제가 정한다](#구현은-운영-체제가-정한다)
- [이벤트 루프의 뼈대](#이벤트-루프의-뼈대)
- [무한 대기가 아니라 타임아웃인 이유](#무한-대기가-아니라-타임아웃인-이유)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **스레드 하나가 채널 여럿을 어떻게 지켜보며, 그 루프는 무엇으로 이루어지는가.**

## 셀렉터가 하는 일

- 저자가 셀렉터(Selector)를 NIO의 또 다른 결정적 부품으로 든다 — `ServerSocketChannel`과
  `SocketChannel` 같은 채널 여럿을 스레드 하나로 관리하는 역할이다. 저자의 비유는 여러 I/O 이벤트를
  듣고 그에 맞게 연산을 지시하는 똑똑한 교통 정리자다 (6장 "Blocking Versus Non-blocking I/O",
  p.259).[^rahman2025]
- 셀렉터가 알리는 이벤트가 넷이다 (6장, p.259):[^rahman2025]
  - `OP_ACCEPT` — 새 클라이언트 연결을 받아들일 준비가 되었을 때.
  - `OP_READ` — `SocketChannel`에서 읽을 데이터가 있을 때.
  - `OP_WRITE` — 채널이 나가는 데이터를 받아들일 준비가 되었을 때.
  - `OP_CONNECT` — 클라이언트 모드에서 연결 시도가 성공했을 때.

## 구현은 운영 체제가 정한다

- 셀렉터의 밑바탕 구현은 시스템에 따라 다르다 (6장, p.259).[^rahman2025]
  - macOS에서는 `KQueueSelectorImpl`이 큐 시스템 호출을 활용한다.
  - 더 범용인 구현인 `PollSelectorImpl`은 `poll` 시스템 호출에 기반한다.
- 기제는 운영 체제에 따라 갈리지만 개념은 같다 — 최소한의 스레드 오버헤드로 채널 여럿을 효율적으로
  관리한다는 것이다 (6장, p.259).[^rahman2025] 같은 층의 기제를 가상 스레드가 어떻게 감춰 주는지는
  [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md)에 있다 — 그쪽은 가상 머신이
  대신 도는 폴러이고, 이쪽은 애플리케이션이 직접 도는 루프다.

## 이벤트 루프의 뼈대

- 서버 채널을 열고 묶은 다음 반드시 논블로킹으로 설정해야 한다. 그러지 않으면 서버가 모든 연산에서
  막혀 NIO를 쓰는 목적 자체가 무너진다 (6장, p.261).[^rahman2025]
- 그다음 셀렉터에 등록하며 어떤 이벤트에 관심이 있는지를 지정한다. 수용 이벤트에 등록하면 새
  클라이언트가 연결을 시도할 때 서버가 알림을 받는다 (6장, p.261).[^rahman2025]
- 루프의 모양이 이렇다 (6장, p.260).[^rahman2025]

  ```java
  try (Selector selector = Selector.open();
       ServerSocketChannel serverChannel = ServerSocketChannel.open()) {
      serverChannel.bind(new InetSocketAddress(PORT));
      serverChannel.configureBlocking(false);
      serverChannel.register(selector, SelectionKey.OP_ACCEPT);

      while (true) {
          processPendingUpdates();
          selector.select(100);
          Set<SelectionKey> selectedKeys = selector.selectedKeys();
          Iterator<SelectionKey> iterator = selectedKeys.iterator();
          while (iterator.hasNext()) {
              SelectionKey key = iterator.next();
              iterator.remove();
              if (key.isAcceptable()) {
                  handleAccept(key, selector);
              } else if (key.isReadable()) {
                  handleRead(key);
              } else if (key.isWritable()) {
                  handleWrite(key);
              }
          }
      }
  }
  ```

- 저자가 짚는 개선점이 둘이다 — 서버 채널을 논블로킹으로 구성하는 것이 NIO 동작에 필수이고, 스레드
  하나가 이벤트 루프를 통해 모든 I/O 이벤트를 다룬다 (6장, p.260).[^rahman2025]
- 셀렉터를 만드는 방식도 저자가 짚는다 — 전통적인 생성자 대신 `Selector.open()`이라는 정적 팩토리
  메서드를 쓰며, 그것이 선호되는 방식이다. 이 셀렉터가 서버의 핵심이고, 스레드 하나만으로 여러
  클라이언트 연결을 효율적으로 관리하게 해 준다 (6장, p.261).[^rahman2025]
- 키를 처리하는 규칙도 정해져 있다 — 이벤트가 감지되면 셀렉터에서 선택 키들을 꺼낸다. 키 하나가
  등록된 채널의 특정 이벤트 하나를 나타내며, 여러 이벤트가 일어날 수 있으므로 서버는 루프 안에서
  그것들을 순차로 처리한다. 키를 다루고 나면 다시 처리되지 않도록 집합에서 제거한다 (6장,
  p.262).[^rahman2025]
- 그 결과가 확인된다 — 이 프로그램은 스레드 하나로 동작하면서도 여러 연결을 동시에 다룬다. 저자는
  이것이 NIO의 힘이라고 적는다. 연결마다 별도 스레드를 띄우지 않고도 수많은 클라이언트를 효율적으로
  관리한다 (6장, p.270).[^rahman2025]

## 무한 대기가 아니라 타임아웃인 이유

- `selector.select(100)`은 최대 100밀리초까지 막는다. 이 타임아웃이 중요하다 — 타임아웃이 없으면
  셀렉터가 무한정 막힐 수 있어 비동기 스레드에서 온 갱신을 제때 처리하지 못한다 (6장,
  p.262).[^rahman2025]
- 그래서 반환 조건이 둘이 된다 — 이벤트가 감지되거나 타임아웃이 만료되면 `select()`가 반환하고,
  서버는 이벤트나 대기 중인 갱신을 그에 맞게 처리한다 (6장, p.262).[^rahman2025]
- 루프의 머리에서 먼저 부르는 `processPendingUpdates()`가 그 갱신을 담당한다. 왜 그것이 별도의
  큐를 거쳐야 하는지는
  [SelectionKey의 스레드 안전 오해](../concepts/selection-key-thread-safety.md)에 있다.

## 이어지는 페이지

- [SelectionKey의 스레드 안전 오해](../concepts/selection-key-thread-safety.md) — 이 루프 밖에서
  관심 연산을 건드리면 벌어지는 일
- [논블로킹 서버가 직접 감당하는 상태](../concepts/hand-written-non-blocking-server-state.md) —
  세 핸들러 안에서 손으로 관리하게 되는 것들
- [자바 NIO의 채널과 버퍼](../concepts/java-nio-channels-and-buffers.md) — 이 루프가 다루는 부품들
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 같은 기제를 가상 머신이 대신
  도는 쪽
- [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md) — 이 루프를
  프레임워크가 대신 돌 때의 규칙
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    셀렉터 절(p.259), `NonBlockingHttpServer`(pp.259–270). 인용한 이벤트 루프는 원문(p.260)의
    `start()` 메서드에서 로그 출력 두 줄과 예외 처리 블록과 코드 옆 번호 표식과 주석을 뺐고,
    지면 폭 때문에 접힌 줄을 원래 한 줄로 되돌렸다. 클래스 선언과 `main`(pp.259–260),
    `processAllPendingRequests` 호출부는 옮기지 않았다. 이 절에는 그림이 없다.

---
type: concept
title: 논블로킹 서버가 직접 감당하는 상태
description: 라이브러리 없이 논블로킹 서버를 지을 때 연결마다 손으로 들고 있어야 하는 상태 객체, 읽기가 부분 읽기이고 쓰기가 부분 쓰기라서 생기는 누적과 재시도, 보낼 것이 있을 때만 쓰기 관심을 켜는 규칙, 그리고 느린 일을 이벤트 루프 밖으로 내보내는 자리
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 논블로킹 서버가 직접 감당하는 상태

- [연결마다 상태 객체](#연결마다-상태-객체)
- [읽기는 부분 읽기다](#읽기는-부분-읽기다)
- [쓰기도 부분 쓰기다](#쓰기도-부분-쓰기다)
- [느린 일은 이벤트 루프 밖으로](#느린-일은-이벤트-루프-밖으로)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **프레임워크 없이 논블로킹 서버를 지으면 무엇을 손으로 들고 있게 되는가.**

## 연결마다 상태 객체

- 수용 핸들러의 첫 특징이 논블로킹이라는 데서 온다 — `accept()` 호출은 막지 않으며 준비된 연결이
  없으면 `null`을 반환할 수 있다 (6장 "Blocking Versus Non-blocking I/O",
  p.263).[^rahman2025]
- 그래서 클라이언트마다 상태 객체를 하나씩 붙인다. 연결 상태와 부분 데이터를 추적하기 위해서다
  (6장, p.263).[^rahman2025]
- 그 객체가 들고 있는 것이 여럿이다 — 클라이언트의 채널, 읽기 버퍼와 응답 큐, 들어오는 HTTP 요청
  데이터를 쌓아 두는 문자열 빌더다. 저자는 이 구조화된 클라이언트별 상태 관리가 여러 클라이언트를
  효율적으로 다루는 데 필수이며, 각 연결이 서로 간섭하지 않고 자기 문맥을 유지하게 해 준다고
  적는다 (6장, p.263).[^rahman2025]
- 자료 구조 선택에 이유가 붙는다 — 응답 큐는 보통의 연결 리스트가 아니라 `ConcurrentLinkedQueue`를
  쓴다. 응답이 비동기 처리 스레드에서 더해질 것이므로 명시적 동기화 없이 스레드 안전한 연산이
  필요하기 때문이다 (6장, p.263).[^rahman2025]
- 플래그 하나가 더 있다 — 처리 중 플래그는 같은 클라이언트의 요청이 중복 처리되는 것을 막는다.
  여러 이벤트가 짧은 간격으로 연달아 발생할 때 생기는 경쟁 조건을 피하는 자리다 (6장,
  p.263).[^rahman2025]
- 상태를 어디에 다는지도 정해져 있다 — 클라이언트 채널을 읽기 연산으로 셀렉터에 등록하면서 상태
  객체를 선택 키의 첨부물(attachment)로 달아 둔다. 나중에 필요할 때 꺼낼 수 있게 하는 방식이다
  (6장, p.263).[^rahman2025]

## 읽기는 부분 읽기다

- 읽기 핸들러의 성격이 셋으로 정리된다 (6장, p.264):[^rahman2025]
  - 읽기는 논블로킹이라 부분 데이터를 반환할 수 있다.
  - 완전한 HTTP 요청이 도착하는 대로 처리하며, 부분 요청은 무너지지 않게 다룬다.
  - 보낼 데이터가 있을 때만 쓰기 이벤트에 관심을 등록한다.
- 실제 동작이 이렇다 — 핸들러가 클라이언트 채널에서 데이터를 읽어 읽기 버퍼에 넣는다. 받은 바이트는
  UTF-8로 문자로 디코딩되어 요청 빌더에 이어 붙는다 (6장, p.265).[^rahman2025]
- 요청의 끝을 무엇으로 아는지도 명시된다 — 표준 HTTP 요청 종결자를 찾는 방식이다. 완전한 요청이
  감지되면 서버가 그것을 파싱해 비동기로 처리하며, 그렇게 해서 이벤트 루프가 결코 막히지 않게 한다
  (6장, p.265).[^rahman2025]
- 읽은 바이트가 -1이면 클라이언트가 연결을 끊은 것이므로 채널을 닫는다 (6장,
  pp.263–264).[^rahman2025]
- 프로토콜 판본에 따라 기본값이 갈리는 자리도 손으로 다룬다 — HTTP/1.0은 클라이언트가 명시로
  킵얼라이브를 요청하지 않는 한 연결을 닫는 것이 기본이고, HTTP/1.1은 클라이언트가 닫기를
  요청하지 않는 한 유지하는 것이 기본이다. 저자는 이 구분이 아파치 벤치 같은 도구와의 호환성에
  결정적이라고 적는다 (6장, p.264).[^rahman2025]

## 쓰기도 부분 쓰기다

- 쓰기 핸들러는 응답 큐를 돌며 각 응답을 논블로킹 쓰기로 채널에 쓴다 (6장,
  pp.265–266).[^rahman2025]

  ```java
  private void handleWrite(SelectionKey key) throws IOException {
      SocketChannel channel = (SocketChannel) key.channel();
      ClientState state = (ClientState) key.attachment();

      while (!state.responseQueue.isEmpty()) {
          String response = state.responseQueue.peek();
          ByteBuffer buffer = ByteBuffer.wrap(
              response.getBytes(StandardCharsets.UTF_8));
          channel.write(buffer);
          if (buffer.hasRemaining()) {
              break;
          }
          state.responseQueue.poll();
      }

      if (state.responseQueue.isEmpty()) {
          key.interestOps(key.interestOps() & ~SelectionKey.OP_WRITE);
      }
  }
  ```

- 소켓 버퍼가 차면 쓰기가 멈추고 다음 쓰기 이벤트를 기다렸다가 재개한다 (6장,
  p.266).[^rahman2025]
- 응답이 모두 나가 큐가 비면 그 클라이언트에 대한 쓰기 관심을 셀렉터에서 뗀다. 보낼 것이 없는데
  불필요한 쓰기 이벤트가 계속 발생하지 않게 하는 자리다 (6장, p.266).[^rahman2025]
- 스레드 안전한 큐가 여기서 다시 값을 한다 — 비동기 스레드가 더한 응답이 이 과정에서 경쟁 조건을
  일으키지 않게 해 준다 (6장, p.266).[^rahman2025]

## 느린 일은 이벤트 루프 밖으로

- 선택된 키를 모두 다룬 뒤 파싱해 둔 대기 요청들을 처리한다. 저자는 여기서 비동기 처리의 힘이
  드러난다고 적는다 (6장, pp.266–267).[^rahman2025]
- 그 자리의 요점이 넷이다 (6장, p.267):[^rahman2025]
  - 처리 중 플래그가 같은 클라이언트의 요청을 여러 번 처리하기 시작하는 것을 막는다.
  - 느린 연산은 이벤트 루프를 막지 않고 비동기로 처리된다.
  - 응답은 비동기 스레드에서 동시성 큐에 안전하게 더해진다.
  - 선택 키를 비동기 스레드에서 직접 고치는 대신 갱신을 큐에 넣어 주 셀렉터 스레드가 처리하게
    한다. 그 근거는
    [SelectionKey의 스레드 안전 오해](../concepts/selection-key-thread-safety.md)에 있다.
- 비동기 처리에는 `CompletableFuture.runAsync`를 쓴다 (6장, p.266).[^rahman2025] 그 API의
  성격은 [CompletableFuture와 비동기 조합](../concepts/completable-future-composition.md)에 있다.

## 이어지는 페이지

- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 이 핸들러들을 부르는 루프
- [SelectionKey의 스레드 안전 오해](../concepts/selection-key-thread-safety.md) — 갱신을 큐로
  돌려야 하는 이유
- [자바 NIO의 채널과 버퍼](../concepts/java-nio-channels-and-buffers.md) — 여기서 다루는 버퍼의 성격
- [이벤트 루프 스레드를 막지 않는다는 규율](../concepts/event-loop-thread-discipline.md) — 이만큼을
  프레임워크가 대신 해 줄 때 남는 규칙
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 같은 일을 가상 머신이
  대신하는 쪽
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    `NonBlockingHttpServer`의 세 핸들러와 보조 메서드(pp.262–270). 인용한 `handleWrite`는
    원문(p.265)에서 주석과 로그 출력과 킵얼라이브 종료 분기를 뺐고 쓴 바이트 수를 담는 지역
    변수를 덜어 냈다. `handleAccept`와 `ClientState`(p.262), `handleRead`와
    `processCompleteRequests`(pp.263–264), `processAllPendingRequests`(p.266),
    `buildHttpResponse`·`parseHttpRequest`·`buildErrorResponse`(pp.267–270),
    `PipeliningLoadTest`(pp.270–271)는 개념당 대표 코드 하나 규칙에 따라 옮기지 않았다.
    원문의 `buildHttpResponse`(p.268)는 HTTP/1.0이면서 킵얼라이브인 분기에서 응답을 짓다 말고
    `null`을 반환한다 — 그 경로에서는 응답이 만들어지지 않는다. 원문 그대로 적어 둔다.
    이 절에는 그림이 없다.

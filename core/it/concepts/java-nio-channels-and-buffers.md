---
type: concept
title: 자바 NIO의 채널과 버퍼
description: 준비 상태 기반 논블로킹 API로서의 NIO 정의와 스트림 중심 java.io를 버퍼 중심 채널과 셀렉터 이벤트 루프로 대체한다는 것, 소켓과 서버 소켓이 채널로 바뀌는 대응, 그리고 버퍼가 일괄 처리로 시스템 호출을 줄이고 다이렉트 버퍼와 메모리 매핑 버퍼로 제로 카피를 얻는 방식
generated: { by: "claude-opus-5", at: "2026-09-05T22:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 자바 NIO의 채널과 버퍼

- [NIO의 정의](#nio의-정의)
- [스트림 중심과 버퍼 중심](#스트림-중심과-버퍼-중심)
- [부품의 대응](#부품의-대응)
- [버퍼가 벌어 주는 것](#버퍼가-벌어-주는-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **`java.io`와 `java.nio`는 무엇이 다르며 버퍼를 중심에 두면 무엇을 벌게
되는가.**

## NIO의 정의

- 저자가 NIO(new input/output)를 한 문단으로 정의한다 (6장 "Blocking Versus Non-blocking I/O",
  p.257).[^rahman2025]

  > Java NIO is a readiness-based, non-blocking API introduced in JDK 1.4 that replaces
  > stream-oriented java.io with buffer-oriented channels (SocketChannel, FileChannel, etc.) and
  > a Selector event loop.

- 한국어로 옮기면 자바 NIO는 JDK 1.4에서 들어온 준비 상태(readiness) 기반의 논블로킹 API이며,
  스트림 중심의 `java.io`를 버퍼 중심의 채널과 셀렉터(Selector) 이벤트 루프로 대체한다 (6장,
  p.257).[^rahman2025] 같은 도입 시점을 다른 소스도 기록한다 —
  [자바 가상 머신의 런타임 데이터 영역](../concepts/jvm-runtime-data-areas.md)이 JDK 1.4의 NIO와
  `DirectByteBuffer`를 힙 밖 메모리 쪽에서 다룬다.
- 동작이 어떻게 달라지는지를 저자가 이어서 적는다 — 연산이 끝날 때까지 스레드가 막히는 대신,
  논블로킹 `read()`나 `write()` 호출은 즉시 반환하며 전송된 바이트가 0인 경우도 흔하다. 동시에 그
  채널은 셀렉터에 등록된다 (6장, p.257).[^rahman2025]
- 기다림이 셀렉터로 옮겨 간다 — 셀렉터는 운영 체제가 채널 하나 이상이 I/O 준비 상태가 되었다고
  알릴 때까지 `select()` 안에서 잠들어 있다. 그다음 스레드는 준비된 채널만 처리하며, 그래서 수천 개의
  동시 연결을 몇 안 되는 스레드가 감당할 수 있게 된다 (6장, p.257).[^rahman2025]
- 여기에 다이렉트 버퍼나 메모리 매핑 버퍼를 곁들이면 사용자 공간과 커널 공간 사이의 제로
  카피(zero-copy) 데이터 전송이 되고, 고전적인 소켓당 스레드 모델이 물리던 연결당 스레드와 스택의
  오버헤드 없이 높은 처리량과 확장성을 낸다 (6장, p.257).[^rahman2025]

## 스트림 중심과 버퍼 중심

- 곁글 하나가 둘을 나란히 놓는다 — 자바는 I/O를 다루는 방식을 둘 가진다. 전통적인 `java.io`
  패키지와 2025년 저술 시점 기준 더 현대적인 `java.nio`다 (6장 곁글 "Java I/O Versus NIO: A Quick Comparison",
  p.257).[^rahman2025]
- 핵심 차이가 접근 방식에 있다 — 자바 I/O는 스트림 기반이고 일반적으로 블로킹이어서 스레드가 연산이
  끝나기를 기다려야 한다. 반면 자바 NIO는 버퍼 기반이고 논블로킹이라 큰 데이터 전송과 고성능
  애플리케이션에서 더 높은 확장성을 준다 (6장, p.257).[^rahman2025]
- 저자가 같은 파일 읽기를 두 방식으로 보인다. `java.io` 쪽은 `BufferedReader`가 입력 스트림에서
  한 줄씩 텍스트를 읽는 모양이고, 순차 파일 읽기에는 효율적이고 쓰기 쉽다 (6장,
  pp.257–258).[^rahman2025]
- NIO 쪽은 `FileChannel`이다. 데이터가 먼저 `ByteBuffer`로 실려 메모리에서 다뤄진 다음에야 처리되는
  버퍼 주도 방식이다 (6장, p.258).[^rahman2025]

  ```java
  try (FileChannel channel = FileChannel.open(
          Path.of("input.txt"), StandardOpenOption.READ)) {
      ByteBuffer buffer = ByteBuffer.allocate(1024);
      while (channel.read(buffer) > 0) {
          buffer.flip();
          while (buffer.hasRemaining()) {
              System.out.print((char) buffer.get());
          }
          buffer.clear();
      }
  } catch (IOException e) {
      e.printStackTrace();
  }
  ```

## 부품의 대응

- 이름이 하나씩 갈아 끼워진다 — `ServerSocket` 대신 `ServerSocketChannel`을, `Socket` 대신
  `SocketChannel`을 쓴다. `InputStream`과 `OutputStream`에 기대는 대신 NIO는 버퍼를 쓴다 (6장,
  p.258).[^rahman2025]
- 버퍼의 정의는 임시 저장소다 — 목적지로 보내지기 전에 정해진 양의 데이터를 담아 두는 자리이고,
  저자는 이 설계의 전환이 I/O를 다룰 때 더 큰 유연성과 효율을 준다고 적는다 (6장,
  p.258).[^rahman2025]

## 버퍼가 벌어 주는 것

- 버퍼가 성능을 올리는 방식은 운영 체제와의 직접 상호작용을 줄이는 것이다 (6장,
  p.259).[^rahman2025]
- 첫째가 일괄 처리다 — 데이터를 바이트 단위로 읽고 쓰는 전통적 I/O와 달리 버퍼는 일괄 처리를
  가능하게 해 시스템 호출 횟수를 줄인다. 네트워크 서버와 파일 처리 같은 고성능 애플리케이션에서
  특히 쓸모가 있다 (6장, p.259).[^rahman2025]
- 둘째가 제로 카피 기제다 — `ByteBuffer`가 메모리 매핑 파일이나 다이렉트 버퍼, 곧 힙 밖 메모리와
  함께 동작할 수 있다. 이것이 사용자 공간과 커널 공간 사이의 불필요한 데이터 복사를 없애 큰 파일
  전송을 크게 빠르게 한다 (6장, p.259).[^rahman2025]
- 셋째가 확장성이다 — 버퍼를 쓰는 논블로킹 I/O는 스레드 하나가 여러 연결을 효율적으로 관리하게 해
  확장 가능한 이벤트 기반 애플리케이션을 가능하게 한다 (6장, p.259).[^rahman2025]

## 이어지는 페이지

- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 정의에 나온 그 셀렉터의 실물
- [블로킹 I/O와 논블로킹 I/O](../concepts/blocking-versus-non-blocking-io.md) — 이 대안이 답하려는
  문제
- [자바 가상 머신의 런타임 데이터 영역](../concepts/jvm-runtime-data-areas.md) — 다이렉트 버퍼가
  쓰는 힙 밖 메모리와 그 함정
- [논블로킹 서버가 직접 감당하는 상태](../concepts/hand-written-non-blocking-server-state.md) —
  버퍼를 직접 다루면 따라오는 일들
- [리액티브 자바와 논블로킹 I/O](../synthesis/reactive-java-and-non-blocking-io.md) — 이 페이지가
  속한 허브

[^rahman2025]: Rahman 2025, 6장 "The Relevance of Reactive Java in Light of Virtual Threads" —
    NIO 정의(p.257), 곁글 "Java I/O Versus NIO: A Quick Comparison"(pp.257–258), 버퍼 절(p.259).
    인용한 `FileChannel` 예제는 원문(p.258) 그대로다. 같은 곁글의 `BufferedReader` 예제(p.257)는
    개념당 대표 코드 하나 규칙에 따라 옮기지 않았다. 이 절에는 그림이 없다.

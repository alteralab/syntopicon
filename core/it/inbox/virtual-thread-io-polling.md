---
type: concept
title: 가상 스레드의 I/O 폴링
description: 가상 스레드가 I/O를 시작하면 LockSupport.park를 거쳐 후속문이 양보하고 캐리어에서 떨어진다는 것, 그것을 다시 깨우는 것이 가상 머신 전역의 읽기 폴러와 쓰기 폴러라는 것, 운영 체제별로 kqueue와 epoll과 wepoll을 쓴다는 것, 그리고 파일 디스크립터를 가상 스레드에 잇는 매핑
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T12:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드의 I/O 폴링

- [버전 조건](#버전-조건)
- [park에서 후속문 양보까지](#park에서-후속문-양보까지)
- [무엇이 다시 깨우는가](#무엇이-다시-깨우는가)
- [운영 체제별 기제](#운영-체제별-기제)
- [파일 디스크립터와 가상 스레드의 매핑](#파일-디스크립터와-가상-스레드의-매핑)
- [블로킹 지점이 다시 쓰였다](#블로킹-지점이-다시-쓰였다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **I/O를 기다리며 내려온 가상 스레드를 실제로 무엇이 다시 올려놓는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 여기 적힌 폴러 구현은 가상 스레드가 정식 기능이 된 릴리스 이후 가상
> 머신 구현의 것이다. 운영 체제별 기제는 버전이 아니라 플랫폼에 따라 갈린다.

## park에서 후속문 양보까지

- 실제로 벌어지는 일은 파킹이다 — 가상 스레드가 I/O 연산을 시작하면 후속문(continuation)이 멈추는데,
  진짜로 일어나는 것은 스레드가 `LockSupport.park()` 메서드를 부르는 것이다 (3장,
  p.122).[^rahman2025]
- 그 메서드가 가상 스레드인지를 먼저 본다 (3장, p.122).[^rahman2025]

  ```java
  public static void park() {
      if (Thread.currentThread().isVirtual()) {
          VirtualThreads.park();
      } else {
          U.park(false, 0L);
      }
  }
  ```

- 갈림 뒤가 후속문이다 — `VirtualThreads.park()` 안에서 몇 단계를 거쳐 `yieldContinuation()`
  메서드를 부르고, 이것이 사실상 가상 스레드를 캐리어 스레드에서, 곧 가상 스레드를 실행하는 진짜
  플랫폼 스레드에서 떼어낸다 (3장, p.122).[^rahman2025] `park`와 `unpark`의 일반 규칙은
  [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md)에 있고,
  떼어내는 일의 실물은
  [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md)에 있다.

## 무엇이 다시 깨우는가

- 저자가 여기서 핵심 물음을 세운다 — 소켓에 데이터가 도착했을 때 그 가상 스레드를 언파크하는 것은
  무엇인가 (3장, p.122).[^rahman2025]
- 답이 폴러다 — 가상 머신은 가상 머신 전역(JVM-wide) 읽기 폴러(read poller)를 쓴다. 그 핵심은
  기본적인 이벤트 루프이며, `read()`·`connect()`·`accept()` 같은 동기 네트워킹 연산이 가상 스레드
  안에서 불렸는데 즉시 준비되지 않을 때 그것들을 감시한다 (3장, pp.122–123).[^rahman2025]
- 깨우는 순간이 준비되는 순간이다 — I/O 연산이 준비되면, 이를테면 소켓에 데이터가 도착하면 폴러가
  알림을 받아 그에 대응하는 파크된 가상 스레드를 언파크한다 (3장, p.123).[^rahman2025]
- 쓰기 쪽도 대칭이다 — 이 기제는 쓰기 연산에도 그대로 있고, 비슷한 쓰기 폴러(write poller)가 맡는다
  (3장, p.123).[^rahman2025]

## 운영 체제별 기제

- 폴러의 바탕은 플랫폼마다 다르다 — macOS에서는 kqueue를, 리눅스에서는 epoll을, 윈도우에서는
  wepoll을 쓴다. wepoll은 윈속(Winsock)의 보조 함수 드라이버(Ancillary Function Driver) 위에서
  epoll 비슷한 API를 준다 (3장, p.123).[^rahman2025]

## 파일 디스크립터와 가상 스레드의 매핑

- 폴러가 유지하는 것이 매핑 하나다 — 파일 디스크립터(file descriptor)와 가상 스레드 사이의 지도를
  유지한다 (3장, p.123).[^rahman2025]
- 등록의 뜻이 항목 추가다 — 소켓 같은 파일 디스크립터가 폴러에 등록되면, 그 디스크립터와 I/O 연산의
  완료를 기다리는 가상 스레드를 잇는 항목이 이 지도에 더해진다 (3장, p.123).[^rahman2025]
- 깨어날 때의 순서가 조회다 — 폴러의 이벤트 루프가 어떤 이벤트로, 이를테면 소켓에 데이터가
  들어왔다는 이벤트로 깨어나면, 그 이벤트의 파일 디스크립터로 지도에서 대응하는 가상 스레드를 찾아
  언파크해 실행을 재개할 수 있게 한다 (3장, p.123).[^rahman2025]
- 저자가 더 알고 싶으면 OpenJDK 저장소에 있는 폴러의 소스 코드를 읽으라고 권하며, 가상 스레드가
  I/O를 기다리는 동안 자원을 낭비하지 않도록 가상 머신이 플랫폼별 기제를 어떻게 활용하는지 볼 수
  있다고 적는다 (3장, p.123).[^rahman2025]

## 블로킹 지점이 다시 쓰였다

- 장을 맺으며 범위를 밝힌다 — JDK 라이브러리의 거의 모든 블로킹 지점이 가상 스레드를 받아들이도록
  다시 쓰였다 (3장, p.123).[^rahman2025]
- 그래서 규칙이 하나로 정리된다 — 이제 대부분의 블로킹 연산은, 가상 스레드가 블로킹 호출을 만나면
  언마운트되어 자기 캐리어 스레드, 곧 밑에 깔린 운영 체제 스레드를 풀어 새 일을 맡게 하는 식으로
  동작한다 (3장, p.123).[^rahman2025]
- 그 결과가 확장이다 — 이 방식 덕분에 시스템은 시스템 자원을 고갈시키지 않고도 아주 많은 수의 가상
  스레드를 감당할 수 있다 (3장, p.123).[^rahman2025] 예외인 자리는
  [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md)이 갖는다.

## 이어지는 페이지

- [자바의 후속문 API](../concepts/java-continuation-api.md) — `park` 뒤에서 불리는 양보의 실물
- [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md) — 떼어낼 때 무엇이
  옮겨지는가
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 언마운트와 마운트의 정의
- [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md) —
  `park`와 `unpark`의 일반 규칙
- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 언마운트되지 못하는 예외
- [블로킹 I/O와 스레드 효율](../concepts/blocking-io-and-thread-efficiency.md) — 이 기제가 겨냥한
  본래 문제
- [NIO 셀렉터와 이벤트 루프](../concepts/nio-selector-event-loop.md) — 같은 준비 상태 감시를
  애플리케이션이 직접 지을 때의 모양
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 3장 "The Mechanics of Modern Concurrency in Java" — "Virtual
    Threads and I/O Polling"(pp.122–123), "In Closing"(p.123). 인용한 `park()`는 원문(p.122)
    그대로다. 이 절에는 그림이 없다.

---
type: concept
title: 가상 스레드의 마운트와 스택 프레임
description: 가상 스레드가 스택 프레임을 가비지 컬렉션 대상 힙에 두는 대체 구현이라는 것, 실행할 때 캐리어 스레드에 올리고 블로킹에서 내려놓으며 프레임을 힙과 캐리어 스택 사이로 옮긴다는 것, 이 과정이 자바 코드에 투명하다는 것, 그리고 저자가 이 구조를 가상 메모리에 견주는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드의 마운트와 스택 프레임

- [버전 조건](#버전-조건)
- [스택 프레임이 힙으로 갔다](#스택-프레임이-힙으로-갔다)
- [캐리어 스레드와 운영 체제](#캐리어-스레드와-운영-체제)
- [블로킹에서 내려놓기](#블로킹에서-내려놓기)
- [투명성](#투명성)
- [가상 메모리라는 비유](#가상-메모리라는-비유)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **가상 스레드가 실제로 실행되고 멈추는 동안 무엇이 어디로 옮겨 다니는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 여기 적힌 마운트·언마운트 구현은 가상 스레드가 정식 기능이 된
> 릴리스 이후의 것이다. 스택 프레임이라는 개념 자체는 버전과 무관하다 —
> [스택 프레임의 구조](../concepts/stack-frame-structure.md)를 보라.

## 스택 프레임이 힙으로 갔다

- 핵심이 저장 위치의 교체다 — 가상 스레드의 중심에는 스택 프레임을 자바의 가비지 컬렉션 대상 힙에
  저장하는 `java.lang.Thread`의 대체 구현이 있다. 전통적인 스레드는 운영 체제가 할당한 일체형
  (monolithic) 메모리 블록에 스택 프레임을 저장한다 (2장, p.46).[^rahman2025]
- 그래서 사라지는 일이 하나 있다 — 스레드에 필요한 스택 크기를 미리 추정할 필요가 없어진다 (2장,
  p.46).[^rahman2025]
- 발자국의 수치가 한 줄이다 — 가상 스레드의 메모리 발자국은 겨우 수백 바이트에서 시작하며, 호출
  스택이 자라고 줄어드는 데 따라 자동으로 조절된다. 이 동적인 메모리 관리가 자원 효율을 크게
  올린다 (2장, p.46).[^rahman2025] 플랫폼 스레드 쪽의 대응 수치(64비트 리눅스 핫스팟에서 1MB)는
  [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)에 있다.

## 캐리어 스레드와 운영 체제

- 운영 체제는 가상 스레드를 모른다 — 플랫폼 스레드만 알아보고, 그 플랫폼 스레드가 운영 체제
  수준 스케줄링의 단위로 남는다 (2장, p.46).[^rahman2025]
- 마운트(mount)의 정의가 여기 있다 — 가상 스레드 안에서 코드를 실행하려면 자바 런타임이 그것을
  플랫폼 스레드에 올리고, 그 플랫폼 스레드를 캐리어 스레드(carrier thread)라 부른다 (2장,
  p.46).[^rahman2025]
- 캐리어의 출신도 명시된다 — 이 캐리어 스레드들은 특수한 `ForkJoinPool`의 일부다 (2장,
  p.46).[^rahman2025] 그 풀의 성질은
  [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md)에 있다.
- 옮기는 것의 실물이 프레임이다 — 마운트 과정에서 필요한 스택 프레임이 힙에서 캐리어 스레드의
  스택으로 일시적으로 복사된다. 요컨대 가상 스레드의 코드를 돌리려고 캐리어 스레드를 "빌리는"
  것이다 (2장, p.46).[^rahman2025]

## 블로킹에서 내려놓기

- 언마운트(unmount)의 정의가 대칭이다 — 가상 스레드가 보통이라면 블로킹될 연산, 이를테면 I/O를
  기다리는 자리에 이르면 자기 캐리어 스레드에서 내려올 수 있다 (2장, pp.46–47).[^rahman2025]
- 그때 프레임이 반대 방향으로 간다 — 수정된 스택 프레임이 힙으로 다시 복사되고, 캐리어 스레드는
  풀려나 다른 일을 하러 간다 (2장, p.47).[^rahman2025]
- **이 복사가 통째로 일어나지는 않는다** — 3장이 밝히기로 깊은 호출 스택에서 매번 스택 전체를
  복사하는 것은 비싼 연산이라, 가상 머신에 지연 복사(lazy copy) 기제가 구현되어 있다 (3장,
  p.116).[^rahman2025] 그 기제와 그것을 성립시키는 반환 장벽은
  [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md)에 있다.
- 적용 범위가 넓다 — 이 기능은 JDK의 거의 모든 블로킹 지점에 소급 적용되었고, 그것이 가상
  스레드를 자원 활용 면에서 매우 효율적으로 만드는 것이다 (2장, p.47).[^rahman2025]
- **여기서 벗어나는 경우가 핀닝이다** —
  [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md)이 내려오지 못하는 두 자리를 다룬다.

## 투명성

- 마운트와 언마운트 과정은 자바 코드에 투명하다. 자바 코드가 현재 캐리어 스레드의 정체를 알아낼
  방법은 없다 (2장, p.47).[^rahman2025] 그 결과가
  [가상 스레드에서 달라지는 Thread API](../concepts/virtual-thread-api-semantics.md)의 막힌
  조회다.
- 격리가 스레드 로컬까지 간다 — 캐리어 스레드의 `ThreadLocal` 값조차 가상 스레드에게는 보이지
  않는다 (2장, p.47).[^rahman2025] 가상 스레드 자신의 `ThreadLocal`이 만드는 문제는
  [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md)에 있다.
- 이 정도의 추상 덕분에 기존 자바 코드베이스를 바꾸지 않고 가상 스레드를 쓸 수 있다는 것이 저자의
  결론이다 (2장, p.47).[^rahman2025]

## 가상 메모리라는 비유

- 저자가 이름의 유래를 설명하는 자리다 — 가상 메모리 시스템에서 애플리케이션은 사실상 무한한 주소
  공간을 가진 듯한 착각 속에서 돌고, 그것을 가능하게 하는 것이 가상 메모리의 어느 부분이 실제
  메모리이고 어느 부분이 디스크인지를 잇는 하드웨어 수준 매핑이다 (2장, p.47).[^rahman2025]
- 대응이 한 줄로 맺어진다 — 마찬가지로 가상 스레드는 희소하고 비싼 플랫폼 스레드를 나눠 씀으로써
  사실상 무한한 다중 스레딩의 착각을 만들어 내며, 비활성 가상 스레드의 스택은 가상 메모리
  시스템에서 쓰이지 않는 메모리 페이지가 디스크로 페이징 아웃되듯이 힙으로 페이징 아웃된다 (2장,
  p.47).[^rahman2025]

## 이어지는 페이지

- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 내려오지 못하는 두 자리
- [후속문의 스택 복사와 지연 복사](../concepts/continuation-stack-copying.md) — 이 복사를 한 층
  아래에서 본 자리
- [자바의 후속문 API](../concepts/java-continuation-api.md) — 마운트와 언마운트를 촉발하는 것의 실물
- [가상 스레드의 I/O 폴링](../concepts/virtual-thread-io-polling.md) — 내려온 것을 다시 올리는 쪽
- [가상 스레드 스케줄러](../concepts/virtual-thread-scheduler.md) — 캐리어를 담고 있는 풀
- [플랫폼 스레드와 가상 스레드](../concepts/platform-threads-and-virtual-threads.md) — 두
  종류의 갈림
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 후속문과 스케줄러의
  분리, 그리고 스택 크기 수치
- [스택 프레임의 구조](../concepts/stack-frame-structure.md) — 옮겨 다니는 것의 정체
- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 스택과 힙이
  사는 자리
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "How Virtual Threads Work
    Under the Hood"(p.46), "Stack Frames and Memory Management"(p.46), "Carrier Threads and
    OS Involvement"(p.46), "Handling Blocking Operations"(pp.46–47), "Transparency and
    Invisibility"(p.47). 3장 "The Mechanics of Modern Concurrency in Java" —
    "Continuation"(p.116). 이 절에는 코드 예제가 없다.

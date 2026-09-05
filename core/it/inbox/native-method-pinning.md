---
type: concept
title: 네이티브 호출과 핀닝
description: 네이티브 메서드와 외부 함수 호출이 가상 스레드를 캐리어에 묶는 이유 — 가상 머신이 네이티브 코드를 들여다보거나 통제할 수 없다는 세 가지 제약, 외부 함수·메모리 API로 그것을 실측한 예, 그리고 호출 빈도를 줄이거나 순수 자바로 옮기라는 완화책
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 네이티브 호출과 핀닝

- [버전 조건](#버전-조건)
- [실측의 얼개](#실측의-얼개)
- [외부 함수와 메모리 API](#외부-함수와-메모리-api)
- [왜 네이티브가 핀닝을 만드는가](#왜-네이티브가-핀닝을-만드는가)
- [완화책](#완화책)
- [원문이 스스로 어긋나는 자리](#원문이-스스로-어긋나는-자리)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **네이티브 코드를 부르면 왜 가상 스레드가 캐리어에서 내려오지 못하는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 아래 실험의 실행 명령은 JDK 21을 기준으로 미리 보기 기능을 켜는
> 형태다. 외부 함수·메모리 API 자체의 경계는 아래 절에 따로 적었다. **이 쪽의 핀닝은 JEP 491이
> 걷어 낸 범위 밖이다** — [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md)이 그
> 경계를 담는다.

## 실측의 얼개

- 저자가 동기화 블록 실험과 같은 모양으로 네이티브 쪽을 확인한다. 200,000마이크로초, 곧
  200밀리초를 `usleep`으로 쉬었다가 두 정수를 더해 돌려주는 C 함수 `addNumbers`를 만들어 공유
  라이브러리로 컴파일한다 (2장, p.68).[^rahman2025] 운영 체제별로 리눅스는 `.so`, macOS는
  `.dylib`, 윈도우는 `.dll`을 만든다 (2장, p.68).
- 그다음 가상 스레드 열 개에서 그 네이티브 함수를 부르고, 첫 스레드에 대해 호출 전후로 스레드
  정보를 찍는다 (2장, pp.68–69).[^rahman2025] 자바 쪽 호출부가 다음이다.

  ```java
  public static int invokeNativeAddNumbers(int a, int b) {
      try (Arena arena = Arena.ofConfined()) {
          SymbolLookup lookup = SymbolLookup.libraryLookup(
              Path.of("libaddNumbers.dylib"), arena);
          MemorySegment memorySegment = lookup.find("addNumbers")
              .orElseThrow(() ->
                  new RuntimeException("addNumbers function not found"));
          Linker linker = Linker.nativeLinker();
          FunctionDescriptor addNumbersDescriptor = FunctionDescriptor.of(
              ValueLayout.JAVA_INT,   // return type
              ValueLayout.JAVA_INT,   // parameter 1
              ValueLayout.JAVA_INT);  // parameter 2
          MethodHandle addNumbersHandle = linker.downcallHandle(
              memorySegment, addNumbersDescriptor);
          try {
              return (int) addNumbersHandle.invokeExact(a, b);
          } catch (Throwable e) {
              throw new RuntimeException(e.getMessage());
          }
      }
  }
  ```

- 결과의 판독은 동기화 실험과 같다 — `invokeNativeAddNumbers` 호출 전후의 스레드 식별자가 같으면
  네이티브 메서드가 도는 동안 가상 스레드가 핀닝되어 있었다는 확인이다 (2장,
  p.69).[^rahman2025] 저자의 실행에서 200밀리초 내내 캐리어가 바뀌지 않는다 (2장, p.69).

## 외부 함수와 메모리 API

- 도구의 정체가 명시된다 — 외부 함수·메모리 API(Foreign Function & Memory API, FFM)는 네이티브
  상호운용에 대한 자바의 현대적 접근이며 더 오래된 JNI(Java Native Interface)를 대체한다.
  네이티브 코드를 부르고 힙 밖 메모리를 다루는 더 안전하고 성능 좋은 길을 준다 (2장,
  p.69).[^rahman2025]
  - 버전 조건: JDK 19에서 미리 보기 기능으로 도입되었고 JDK 22에서 확정되었다 (2장, p.69).
    저자는 앞서 이 API를 JDK 22부터 쓸 수 있다고 소개한다 (2장, p.67).
- `Arena`는 네이티브 메모리 세그먼트의 수명 주기를 관리해 try-with-resources 블록을 빠져나갈 때
  제대로 정리되게 한다 (2장, p.69).[^rahman2025]
- 저자가 이 예제를 돌릴 때 쓴 명령은
  `java --enable-preview --source 21 --enable-native-access=ALL-UNNAMED ThreadPinnedNativeMethodExample.java`이고,
  라이브러리 경로는 운영 체제에 맞춰 바꾸라고 적는다 (2장, p.69).[^rahman2025]
- 다운콜 핸들(downcall handle)이 자바와 네이티브 함수 사이의 다리를 만들어 자바에서 C 코드를 부를
  수 있게 한다 (2장, p.69).[^rahman2025]

## 왜 네이티브가 핀닝을 만드는가

- 근본 이유가 하나다 — 가상 머신이 네이티브 코드의 실행을 들여다보거나 통제할 수 없기 때문이다
  (2장, p.70).[^rahman2025]
- 가상 스레드가 네이티브 코드에 들어가면 제약이 셋 걸린다 (2장, p.70).[^rahman2025]
  - 네이티브 코드가 스레드 사이로 옮길 수 없는 스레드 로컬 상태를 쥐고 있을 수 있다.
  - 네이티브 호출 스택은 자바 스택 프레임처럼 저장하고 복원할 수 없다.
  - 네이티브 코드가 운영 체제 수준의 스레드 원시 장치와 직접 상호작용할 수 있다.
- 그래서 가상 스레드가 네이티브 호출이 도는 내내 캐리어에 마운트된 채로 남게 된다 (2장,
  p.70).[^rahman2025] 자바 스택 프레임이라면 어떻게 옮겨지는지는
  [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)에
  있다.
- 다른 소스가 같은 질문을 더 이르게 던져 두었다 —
  [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md)이 옮긴 "코루틴에서
  네이티브 메서드를 호출하면 코루틴이 해당 스레드 전체에 영향을 주지 않고 전환될 수 있을까"라는
  물음에 이 절이 답을 준다.

## 완화책

- 영향의 범위부터 짚는다 — 이 핀닝 동작 때문에 네이티브 호출이 잦은 애플리케이션은 가상 스레드의
  확장성을 온전히 누리지 못할 수 있다 (2장, p.70).[^rahman2025]
- 저자가 드는 완화책이 셋이다 (2장, p.70).[^rahman2025]
  - 연산을 묶어 처리해 네이티브 호출 빈도를 줄인다.
  - 쓸 수 있다면 비동기 네이티브 API를 쓴다.
  - 결정적인 네이티브 기능을 순수 자바로 다시 구현한다.
- 그리고 판단의 기준을 준다 — 네이티브 호출이 애플리케이션 동시성에 실제로 주는 영향을 늘 측정해
  그것이 병목이 되고 있는지 판정하라 (2장, p.70).[^rahman2025]

## 원문이 스스로 어긋나는 자리

- #hypothesis 원문 p.70의 두 서술이 서로 맞지 않는다. 저자는 JEP 491을 소개하며 네이티브 코드
  호출이 여전히 핀닝을 남기는 가장자리 경우 가운데 하나라고 적는데, 같은 쪽에서 JDK 25로 돌리면
  더 이상 핀닝 문제가 보이지 않는다며 바로 이 네이티브 예제(`ThreadPinnedNativeMethodExample`)의
  실행 명령과, 캐리어가 `ForkJoinPool-1-worker-1`에서 `ForkJoinPool-1-worker-6`으로 바뀐 출력을
  싣는다 (2장, p.70).[^rahman2025] 어느 쪽이 맞는지는 이 소스의 서술만으로 가려지지 않으므로
  원문 표현을 고치지 않고 양쪽을 그대로 보존한다. 다른 소스나 JEP 491 원문과 대조할 항목이다.

## 이어지는 페이지

- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 같은 현상의 다른 자리와 그 버전
  경계
- [가상 스레드의 마운트와 스택 프레임](../concepts/virtual-thread-mounting-and-stack-frames.md)
  — 자바 프레임이라면 어떻게 옮겨지는가
- [가상 스레드와 코루틴](../concepts/virtual-threads-and-coroutines.md) — 같은 물음을 가상 머신
  쪽에서 던진 자리
- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 핀닝을 찾아내는 도구
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Native Method Invocation and
    Pinning"(pp.67–70), "JEP 491: Synchronize Virtual Threads Without Pinning"(p.70).
    개념당 대표 코드 하나 규칙에 따라 `invokeNativeAddNumbers` 메서드만 실었고, C 함수
    `addNumbers`와 컴파일 명령(p.68), 그것을 부르는 `main`과 임포트(p.68)는 미수록이다 —
    서술은 모두 옮겼다.

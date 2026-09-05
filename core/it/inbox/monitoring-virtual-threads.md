---
type: concept
title: 가상 스레드 모니터링
description: 가상 스레드의 두 한계를 레거시 코드에서 찾아내는 도구들 — ThreadLocal 접근마다 스택 트레이스를 찍는 가상 머신 플래그, 핀닝된 채 블로킹된 자리를 찍는 플래그와 그 출력에서 읽어야 할 표시, 그리고 시작·종료·핀닝·제출 실패를 기록하는 플라이트 레코더 이벤트 넷
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드 모니터링

- [버전 조건](#버전-조건)
- [무엇을 찾는가](#무엇을-찾는가)
- [ThreadLocal 추적 플래그](#threadlocal-추적-플래그)
- [핀닝 추적 플래그](#핀닝-추적-플래그)
- [플라이트 레코더 이벤트 넷](#플라이트-레코더-이벤트-넷)
- [기록하고 읽기](#기록하고-읽기)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **핀닝과 `ThreadLocal` 과용이 실제로 어디서 일어나는지 어떻게 찾아내는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 아래 플래그와 이벤트 이름은 가상 스레드가 정식이 된 릴리스 이후의
> 것이다. 핀닝 관련 도구가 잡아 주는 대상은 JDK 24 이후 달라진다 —
> [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md)이 그 경계를 담는다.

## 무엇을 찾는가

- 문제의 출처가 둘로 정리된다 — 가상 스레드의 한계는 주로 핀닝과 `ThreadLocal` 사용에서 온다
  (2장, p.74).[^rahman2025]
- 도구가 필요한 이유는 선택의 여지 때문이다 — 그 한계를 염두에 두고 새 애플리케이션을 짜는 것은
  한 가지 이야기이고, 늘 그런 사치가 주어지지는 않는다. 수백만 줄에 이르는 레거시 애플리케이션을
  다룰 때 가상 스레드로 옮기려면 호환성 문제를 볼 눈이 필요하며, 다행히 잠재적 문제를 짚어 주도록
  특별히 설계된 도구들이 있다 (2장, pp.74–75).[^rahman2025]

## ThreadLocal 추적 플래그

- `-Djdk.traceVirtualThreadLocals` 플래그로 가상 머신을 시작하면 `ThreadLocal` 사용을 추적할 수
  있다. 가상 스레드 안에서 `ThreadLocal` 변수에 접근할 때마다 스택 트레이스를 찍어 잘못된 관리나
  과용을 드러낸다 (2장, p.75).[^rahman2025]
- 출력에서 읽히는 것이 셋이다 (2장, p.75).[^rahman2025]
  - `ThreadLocal.setInitialValue()` 호출 — 가상 스레드마다 자기 스레드 로컬 변수를 초기화해야
    하므로 예상된 동작이다.
  - `ThreadLocal.get()` 호출 — 스레드가 자기 스레드 로컬 변수를 가져오는 시점들이다.
  - 사용자 코드의 프레임 — 애플리케이션 안에서 `ThreadLocal`에 접근하는 정확한 위치를 가리키며,
    더 살펴보거나 리팩터링할 지점의 참조가 된다.
- 그리고 이 출력이 앞의 우려를 다시 확인해 준다 — 가상 스레드마다 자기 `ThreadLocal` 인스턴스를
  초기화한다는 것이 드러나므로, 가상 스레드가 많을 때 메모리 사용이 커질 가능성이 확인된다 (2장,
  p.75).[^rahman2025] 그 문제의 내역은
  [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md)에 있다.

## 핀닝 추적 플래그

- `jdk.tracePinnedThreads` 시스템 속성은 스레드가 핀닝된 채로 블로킹 연산을 만날 때마다 스택
  트레이스를 찍게 한다 (2장, p.76).[^rahman2025]
- 자세함이 둘로 갈린다 — `-Djdk.tracePinnedThreads=full`은 자바 프레임뿐 아니라 네이티브 프레임과
  모니터를 쥐고 있는 프레임까지 담은 완전한 스택 트레이스를 찍고 그 프레임을 강조 표시한다.
  핵심만 보려면 `-Djdk.tracePinnedThreads=short`가 문제가 되는 프레임으로 트레이스를 좁힌다
  (2장, p.76).[^rahman2025]
- **출력에서 봐야 할 표시가 둘이다** (2장, p.76).[^rahman2025]
  - `reason:MONITOR` 태그 — 그 스레드가 모니터를 얻으려고 기다리는 중임을 알린다. 잠재적 병목을
    찾는 데 값진 단서다.
  - `<== monitors:1`로 끝나는 줄 — 모니터를 쥐고 있는 스레드를 가리킨다. 트레이스가 어디에서
    일어났는지뿐 아니라 왜 일어났는지도 알려 주는 자리다.
- 이 출력을 해부하면 영향받는 코드 구역을 짚어 스레드 사용을 다듬고 핀닝을 줄이는 판단을 내릴 수
  있다 (2장, p.77).[^rahman2025]

## 플라이트 레코더 이벤트 넷

- 자바 플라이트 레코더(Java Flight Recorder, JFR)는 전통적인 모니터링을 넘어 가상 스레드의 세부를
  관찰하고 디버깅하는 데 특화된 기능을 준다 (2장, p.77).[^rahman2025] 이 도구 자체는
  [JFR과 JMC](../concepts/jfr-and-jmc.md)에 있다.
- `jdk.VirtualThreadStart`와 `jdk.VirtualThreadEnd` — 가상 스레드의 탄생과 종료를 표시한다.
  기본으로 켜져 있지 않지만 켜면 스레드 수명 주기를 자세히 추적할 수 있어 디버깅이나 세밀한
  분석에 쓸모 있다 (2장, p.77).[^rahman2025]
- `jdk.VirtualThreadPinned` — 기본으로 켜져 있는 결정적인 이벤트로, 가상 스레드가 캐리어 스레드에
  오래 핀닝되었을 때 신호를 낸다. 임계값은 설정할 수 있고 기본은 20밀리초다. 핀닝 이벤트는 가상
  스레드의 효율 이득이 사라지는 잠재적 성능 병목을 가리킨다 (2장, p.77).[^rahman2025]
- `jdk.VirtualThreadSubmitFailed` — 이것도 기본으로 켜져 있고, 가상 스레드를 시작하거나 언파크하는
  데 실패했음을 알린다. 자원 고갈이나 가상 머신의 스레드 관리 안에서 예상치 못한 병목을 가리킬 수
  있다 (2장, p.77).[^rahman2025]

## 기록하고 읽기

- 관심 있는 이벤트만 고르려면 `.jfc` 설정 파일을 만든다. 저자가 가상 스레드의 네 이벤트를 켜는
  기본 틀을 준다 (2장, pp.77–78).[^rahman2025]

  ```xml
  <?xml version="1.0" encoding="UTF-8"?>
  <configuration version="2.0" label="Virtual Thread Events"
                 description="JFR configuration to record virtual thread events">
      <event name="jdk.VirtualThreadStart">
          <setting name="enabled">true</setting>
      </event>
      <event name="jdk.VirtualThreadEnd">
          <setting name="enabled">true</setting>
      </event>
      <event name="jdk.VirtualThreadPinned">
          <setting name="enabled">true</setting>
      </event>
      <event name="jdk.VirtualThreadSubmitFailed">
          <setting name="enabled">true</setting>
      </event>
  </configuration>
  ```

- 기록은 `-XX:StartFlightRecording=filename=recording.jfr,settings=VThreadEvents.jfc` 옵션으로
  시작하고, 그러면 설정 파일에 적은 이벤트만 기록된다 (2장, p.80).[^rahman2025]
- 읽는 길이 둘이다 — JDK 미션 컨트롤 같은 도구로 `recording.jfr`을 분석하거나,
  `jfr print --events ... recording.jfr`로 이벤트를 콘솔에 찍는다 (2장, p.80).[^rahman2025]
  저자는 애줄 미션 컨트롤로 같은 파일을 분석하는 화면도 보인다 (2장, p.81).
- 저자의 기록에서 읽히는 것이 둘이다 — 가상 스레드가 얼마나 빨리 만들어지고 끝나는지가 드러나
  짧은 태스크에 맞는 도구임을 보여 주고, 핀닝된 시각과 지속 시간이 드러나 잠재적 지연을 찾게
  해 준다 (2장, pp.80–81).[^rahman2025] 동기화 블록 안에서 500밀리초를 잔 가상 스레드의 핀닝
  이벤트 지속 시간이 504밀리초로 찍힌다 (2장, p.80).

## 이어지는 페이지

- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 이 도구들이 찾는 현상
- [가상 스레드와 ThreadLocal](../concepts/thread-local-with-virtual-threads.md) — 나머지 한
  한계
- [ThreadLocal의 설계 결함 셋](../concepts/thread-local-design-flaws.md) — 이 플래그가 찾아 주는 쓰임이
  왜 문제가 되는가
- [가상 스레드가 보이는 스레드 덤프](../concepts/thread-dumps-with-virtual-threads.md) — 한 시점의
  상태를 통째로 뜨는 다른 길
- [가상 스레드와 ReentrantLock](../concepts/reentrant-lock-for-virtual-threads.md) — 기록에서
  두 방식의 차이가 드러나는 자리
- [JFR과 JMC](../concepts/jfr-and-jmc.md) — 이 기록 장치와 분석 콘솔의 전반
- [가상 스레드로 옮길 때의 실무 지침](../concepts/migrating-to-virtual-threads.md) — 무엇을
  지켜볼 것인가
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Monitoring"(pp.74–75),
    "Monitoring ThreadLocals"(pp.75–76), "Monitoring Pinning"(pp.76–77), "Using the Java
    Flight Recorder"(pp.77–81). 개념당 대표 코드 하나 규칙에 따라 `.jfc` 설정 파일만 실었고,
    `JFRVirtualThreadDemo` 전문(pp.78–79)과 두 플래그의 출력 예시(pp.75–76), `jfr print`
    출력(p.80)은 미수록이다 — 출력에서 읽어야 할 표시는 본문에 옮겼다. 그림 2-5(애줄 미션
    컨트롤 분석 화면, p.81)는 옮기지 않았다.

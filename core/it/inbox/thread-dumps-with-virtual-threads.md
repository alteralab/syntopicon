---
type: concept
title: 가상 스레드가 보이는 스레드 덤프
description: jcmd로 뜨는 스레드 덤프가 가상 스레드를 담는다는 것과 그 두 형식, 담기는 것과 빠지는 다섯 가지, 덤프에서 가상 스레드를 알아보는 단서, 그리고 가상 머신 안에서 형식을 골라 덤프를 뜨는 관리 확장 인터페이스
status: draft
generated: { by: "claude-opus-5", at: "2026-09-05T09:00:00Z" }
sources:
  - { id: rahman2025, resource: /it/sources/rahman2025.md }
---

# 가상 스레드가 보이는 스레드 덤프

- [버전 조건](#버전-조건)
- [왜 덤프인가](#왜-덤프인가)
- [두 형식](#두-형식)
- [담기는 것과 빠지는 것](#담기는-것과-빠지는-것)
- [덤프에서 가상 스레드를 알아보기](#덤프에서-가상-스레드를-알아보기)
- [코드 안에서 뜨는 두 길](#코드-안에서-뜨는-두-길)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **지금 이 순간 가상 스레드들이 어디에서 무엇을 기다리는지 어떻게 통째로 보는가.**

## 버전 조건

> **버전 조건**: JDK 21 이상. 가상 스레드를 담는 덤프와 JSON 형식은 가상 스레드가 정식이 된
> 릴리스 이후의 기능이다.

## 왜 덤프인가

- 자리의 구분이 명확하다 — JDK 미션 컨트롤 같은 도구가 정교한 분석을 주지만, 때로는 빠른 스레드
  덤프가 쓸모 있는 진단 수단이다. `jcmd` 유틸리티가 그 기능을 주며, 중요한 것은 가상 스레드에
  대한 정보까지 담을 수 있다는 점이다 (2장, p.81).[^rahman2025]
- 덤프를 뜨려면 먼저 돌고 있는 자바 애플리케이션의 프로세스 식별자를 얻는다. `ps`나 `jps` 같은
  도구를 쓰며, 자바 프로세스에는 `jps` 또는 `jps -l`이 알맞다 (2장, p.81과 각주 3).[^rahman2025]

## 두 형식

- 평문은 `jcmd <PID> Thread.dump_to_file -format=text <file>`, JSON은
  `jcmd <PID> Thread.dump_to_file -format=json <file>`이다 (2장, pp.81–82).[^rahman2025]
- JSON을 쓰는 이유가 소비자에 있다 — JSON 데이터를 받아들이는 자동 디버깅·분석 도구에 특히 쓸모
  있는 기계 판독 형식이라, 스레드가 많은 복잡한 시스템에서 스레드 상태를 프로그램으로 분석할 수
  있다 (2장, p.82).[^rahman2025]

## 담기는 것과 빠지는 것

- 담기는 것 — 네트워크 I/O 연산에서 블로킹된 가상 스레드와 `ExecutorService` 인터페이스가 만든
  가상 스레드를 열거한다 (2장, p.82).[^rahman2025]
- 빠지는 것이 다섯이다 — 객체 주소, 락, JNI 통계, 힙 통계, 그 밖에 전통적인 스레드 덤프에서 흔히
  보던 정보들이다 (2장, p.82).[^rahman2025]
- 저자는 이 좁힘을 결함이 아니라 성질로 읽는다 — 핵심 정보에 집중하는 덕분에 자주 무관한 잡음
  없이 스레드 실행과 블로킹에 얽힌 문제를 짚어 내기 쉬워진다 (2장, p.82).[^rahman2025]

## 덤프에서 가상 스레드를 알아보기

- 저자의 덤프에서 읽히는 것이 넷이다 (2장, p.85).[^rahman2025]
  - 주 스레드 — `tid`가 `1`이고 이름이 `main`인 스레드다.
  - 시스템 스레드 — `Reference Handler`, `Finalizer`, `Signal Dispatcher`,
    `Notification Thread` 같은 것들로, 가비지 컬렉션과 참조 객체와 그 밖의 가상 머신 수준 작업을
    맡는 가상 머신 관리 스레드다.
  - 정리 스레드 — `Common-cleaner`는 가비지 컬렉터가 처리한 뒤 참조 객체를 청소하는 몫이다.
  - **가상 스레드** — 이름이 없고 식별자만 붙은 스레드가 다수 나온다. 스택 트레이스에
    `java.lang.VirtualThread.parkNanos`와 `java.lang.VirtualThread.sleepNanos`가 들어 있는 것이
    그 판별 단서다.
- 실제 문제를 쫓을 때 볼 단서가 둘이다 — `BLOCKED`나 `WAITING` 상태에 갇힌 스레드는 교착이나 자원
  경합 같은 문제를 자주 가리키고, 덤프를 CPU·메모리 사용량 자료와 함께 보면 시스템이 과부하인지
  알 수 있다 (2장, p.85).[^rahman2025]

## 코드 안에서 뜨는 두 길

- 첫째는 밖의 도구를 부르는 길이다 — 애플리케이션 안에서 `ProcessBuilder`로 `jcmd` 명령을 실행해
  덤프를 뜰 수 있다. 저자는 `ProcessHandle.current().pid()`로 자기 프로세스 식별자를 얻고, 가상
  스레드 1,000개를 띄운 뒤 2초를 기다렸다가 덤프를 뜬다. 기다림은 덤프를 뜨는 시점에 대부분의
  가상 스레드가 아직 살아 있게 만들기 위한 것이다 (2장, pp.82–84).[^rahman2025]
- 둘째는 관리 확장을 쓰는 길이다 — 자바 관리 확장(Java Management Extensions, JMX)의
  `com.sun.management` 패키지 안 `HotSpotDiagnosticMXBean`에 원하는 덤프 형식을 지정할 수 있는
  메서드가 새로 생겼다 (2장, p.86).[^rahman2025]

  ```java
  public static void takeThreadDump(String outputFile) {
      var hotSpotDiagnosticMXBean =
          ManagementFactory.getPlatformMXBean(HotSpotDiagnosticMXBean.class);
      try {
          // Ensure that the output file path is absolute
          if (!new File(outputFile).isAbsolute()) {
              throw new IllegalArgumentException("Output path must be absolute.");
          }
          hotSpotDiagnosticMXBean.dumpThreads(outputFile,
              HotSpotDiagnosticMXBean.ThreadDumpFormat.JSON);
      } catch (IOException e) {
          throw new RuntimeException("An error occurred while taking thread dump", e);
      }
  }
  ```

- 규칙이 둘이다 — `dumpThreads`는 `ThreadDumpFormat` 열거형 인자를 받아 `TEXT_PLAIN`과 `JSON`
  가운데 고르게 하고, 출력 파일에는 반드시 절대 경로를 줘야 오류를 피한다. 이 메서드는 JMX
  도구로 로컬 진단과 원격 진단 모두에 쓸 수 있다 (2장, p.86).[^rahman2025]
- 저자의 총평은 조합이다 — `jcmd`와 JFR을 함께 쓰면 애플리케이션 안에서 가상 스레드가 어떻게
  움직이는지 종합적으로 볼 수 있어 더 효과적으로 디버깅하고 최적화할 수 있다 (2장,
  p.82).[^rahman2025]

## 이어지는 페이지

- [가상 스레드 모니터링](../concepts/monitoring-virtual-threads.md) — 흐름을 계속 기록하는 다른
  길
- [JFR과 JMC](../concepts/jfr-and-jmc.md) — 함께 쓰는 기록 장치와 분석 콘솔
- [가상 스레드 핀닝](../concepts/virtual-thread-pinning.md) — 덤프에서 찾게 되는 문제
- [가상 스레드에서 달라지는 Thread API](../concepts/virtual-thread-api-semantics.md) — 코드
  안에서의 조회가 막혀 있는 자리
- [가상 스레드의 내부와 운영](../synthesis/virtual-thread-internals-and-operations.md) — 이
  페이지가 속한 허브

[^rahman2025]: Rahman 2025, 2장 "Understanding Virtual Threads" — "Viewing Virtual Threads in
    jcmd Thread Dumps"(pp.81–82), "Programmatic thread dumps in Java"(pp.82–85), "Generating
    Thread Dumps with HotSpotDiagnosticsMXBean"(p.86). 개념당 대표 코드 하나 규칙에 따라
    `takeThreadDump`만 실었고, `ThreadDumpDemo` 전문(pp.82–83)과 `dump.json` 발췌
    (pp.84–85)는 미수록이다 — 덤프에서 읽어야 할 단서는 본문에 옮겼다.

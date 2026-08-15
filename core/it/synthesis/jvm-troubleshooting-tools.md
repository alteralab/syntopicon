---
type: synthesis
title: JVM 모니터링과 문제 해결 도구
description: 돌고 있는 자바 가상 머신에서 데이터를 꺼내는 도구들의 진입점 — JDK가 배포하는 명령 줄 여섯 도구, 프로세스 내부를 비추는 JHSDB, 그림으로 보는 JConsole·VisualVM과 코드를 끼워 넣는 BTrace, 상시 켜 두는 JFR·JMC, 그리고 JIT가 만든 네이티브 코드까지 되돌려 읽는 HSDIS·JITWatch
generated: { by: "claude-opus-5", at: "2026-08-15T12:00:00Z" }
---

# JVM 모니터링과 문제 해결 도구

**돌고 있는 가상 머신에서 무엇을 어떻게 꺼내는가**를 다룬다. 꺼낸 값이 무엇을 뜻하는지는
[JVM 자동 메모리 관리](jvm-memory-management.md)가, 그 가상 머신이 애초에 어떤 제품이고 어느
판올림인지는 [자바 기술 시스템](java-technology-system.md)이 담당한다. 운영 대시보드에서 같은
값을 읽는 쪽은 [카프카 모니터링](kafka-monitoring.md)에 있다.

읽는 순서가 있다. 명령 줄에서 데이터를 꺼내는 법을 먼저 익히고, 그림으로 보는 도구로 올라간
뒤, 마지막이 가상 머신 내부와 JIT 코드까지 내려가는 도구다.

## 명령 줄에서 꺼내기

- [JDK 명령 줄 진단 도구](../concepts/jdk-command-line-diagnostic-tools.md) — jps·jstat·jinfo·
  jmap·jhat·jstack의 쓰임과 옵션, 이들이 20KB짜리 얇은 래퍼인 이유, jcmd·jhsdb와의 명령 대응

## 그림으로 보기

- [JConsole·VisualVM·BTrace로 보는 것](../concepts/jvm-gui-monitoring-tools.md) — 메모리·스레드
  탭과 교착 상태 검출, 에이전트 없이 붙는 VisualVM, 서비스를 멈추지 않고 로깅을 끼워 넣는 BTrace
- [JFR과 JMC](../concepts/jfr-and-jmc.md) — 상시 구동을 목표로 한 이벤트 기록기와 그것을 읽는
  콘솔, MBean의 '결과'와 JFR의 '과정'

## 가상 머신 안쪽 보기

- [JHSDB와 서비스 에이전트](../concepts/jhsdb-serviceability-agent.md) — 핫스팟의 C++ 자료
  구조를 자바 객체로 비추는 디버거, 변수가 실제로 어디에 저장되는지 확인하는 실험
- [핫스팟 JIT 코드 들여다보기](../concepts/hotspot-jit-inspection-tools.md) — 명세가 개념
  모델이 된 지점, HSDIS로 되돌려 읽는 어셈블리, JITWatch의 3면 뷰

## 경계에 있는 페이지

- [적합한 가비지 컬렉터 고르기](../concepts/choosing-a-garbage-collector.md) — 같은 사건을
  로그로 남기는 `-Xlog`
- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 이 도구들이
  떠내는 힙·스택·메서드 영역의 정의
- [카프카 JVM과 운영체제 모니터링](../concepts/kafka-jvm-and-os-monitoring.md) — 같은 값을
  JMX 빈으로 읽어 경보를 거는 운영 사례
- [OpenJDK 직접 빌드하기](../concepts/building-openjdk-from-source.md) — 디버그용 가상 머신이
  있어야 열리는 기능들

## 이어지는 허브

- [JVM 자동 메모리 관리](jvm-memory-management.md) — 여기서 읽는 숫자가 무엇을 뜻하는지
- [자바 기술 시스템](java-technology-system.md) — 도구가 붙는 가상 머신과 JDK 쪽
- [백엔드 컴파일과 최적화](backend-compilation-and-optimization.md) — JIT 코드 검사 도구가
  들여다보는 그 컴파일러들
- [카프카 모니터링](kafka-monitoring.md) — 제품 하나를 실제로 감시하는 지표 체계

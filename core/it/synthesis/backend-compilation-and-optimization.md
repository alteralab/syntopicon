---
type: synthesis
title: 백엔드 컴파일과 최적화
description: 바이트코드가 네이티브 코드가 되는 구간의 진입점 — 인터프리터와 함께 도는 JIT 컴파일러와 계층형 컴파일, 무엇이 핫 코드로 뽑혀 언제 컴파일이 촉발되는가, C1·C2의 컴파일 절차, 실행 전에 미리 컴파일하는 AOT와 그 맞상대인 JIT의 강점, 인라인·탈출 분석을 비롯한 최적화 기법들, 그리고 자바로 쓰여 안을 들여다볼 수 있는 그랄 컴파일러
generated: { by: "claude-opus-5", at: "2026-08-16T00:40:00Z" }
---

# 백엔드 컴파일과 최적화

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **바이트코드가 로컬 환경의 네이티브 코드로 바뀌는
구간** — 그 일을 런타임에 하는 JIT 컴파일러, 실행 전에 해 두는 AOT 컴파일러, 두 컴파일러가
공통으로 쓰는 최적화 기법, 그리고 그 과정을 밖에서 관찰하는 실습 — 이 사는 자리다. 같은
컴파일의 **앞쪽 절반**(`.java`에서 `.class`까지)은 형제 허브
[클래스 파일과 바이트코드](class-file-and-bytecode.md)가 다루고, 그 결과물을 **해석 실행**하는
쪽도 거기 있다. 컴파일러를 품은 **가상 머신 제품과 판올림**은
[자바 기술 시스템](java-technology-system.md)이, 컴파일된 코드가 다루는 **메모리**는
[JVM 자동 메모리 관리](jvm-memory-management.md)가 담당한다.

읽는 순서가 있다. 컴파일러가 왜 둘 이상인지를 먼저 보고, 무엇이 언제 컴파일되는지, 그 안에서
무슨 일이 일어나는지로 내려간 뒤, 미리 컴파일하는 갈래와 최적화 기법을 지나 마지막이 자바로
쓰인 컴파일러의 내부다.

## 왜 컴파일러가 둘 이상인가

- [JIT 컴파일러와 계층형 컴파일](../concepts/jit-compilers-and-tiered-compilation.md) —
  인터프리터가 남아 있는 세 가지 이유, C1·C2·그랄, 혼합·해석·컴파일 세 실행 모드, 계층 0부터
  4까지

## 무엇이 언제 컴파일되는가

- [핫스팟 탐지와 온스택 치환](../concepts/hotspot-detection-and-osr.md) — 핫 코드 두 유형,
  샘플·카운터 두 탐지 방식, 메서드 호출 카운터와 백 에지 카운터, 감쇠와 문턱값 계산식

## 컴파일러 안에서 일어나는 일

- [JIT 컴파일러의 컴파일 과정](../concepts/jit-compilation-process.md) — 백그라운드 컴파일,
  HIR·LIR을 거치는 C1의 3단계, 전통·자바 특화·예측 세 갈래 최적화를 얹는 C2

## 미리 컴파일하는 갈래

- [자바의 AOT 컴파일](../concepts/aot-compilation-in-java.md) — 1996년의 AOT가 안드로이드
  ART로 돌아온 경위, 전통적 AOT와 동적 AOT, 그리고 JIT가 본질적으로 나은 세 가지
- [jaotc로 미리 컴파일해 보기](../concepts/jaotc-ahead-of-time-compilation.md) — `java.base`를
  통째로 사전 컴파일하는 절차와 5분에 353MB라는 실측치

## 최적화 기법

- [JIT 컴파일러의 최적화 기법](../concepts/jit-optimization-techniques.md) — 아홉 갈래로 나뉜
  기법 전체 목록과, 네 번의 최적화로 문장이 사라져 가는 예제
- [메서드 인라인](../concepts/method-inlining.md) — '최적화의 어머니'가 가상 메서드와 부딪히는
  자리, 클래스 계층 구조 분석과 가이디드 인라인, 모노모픽·메가모픽 인라인 캐시
- [탈출 분석](../concepts/escape-analysis.md) — 탈출 수준 세 가지와 스택 할당·스칼라 치환·동기화
  제거, 그리고 객체 생성이 통째로 사라지는 3단계
- [공통 하위 표현식 제거와 안전 검사 걷어내기](../concepts/common-subexpression-and-safety-check-elimination.md) —
  고전적인 언어 독립 기법 하나와 언어 특화 기법 하나, 널 검사를 예외 핸들러로 바꾸는 암묵적 예외
  최적화

## 밖에서 관찰하기

- [핫스팟 JIT 코드 들여다보기](../concepts/hotspot-jit-inspection-tools.md) — PrintCompilation의
  네 열과 PrintInlining, HSDIS로 되돌린 어셈블리, IGV로 따라가는 단계별 아이디얼 그래프

## 자바로 쓰인 컴파일러

- [그랄 컴파일러와 JVMCI](../concepts/graal-compiler-and-jvmci.md) — 맥신에서 갈라져 나온 내력,
  컴파일러를 갈아 끼우는 인터페이스의 세 기능, mx로 빌드해 돌리는 실습 환경
- [그랄의 아이디얼 그래프와 코드 생성](../concepts/graal-ideal-graph-and-code-generation.md) —
  데이터 흐름과 제어 흐름을 합친 중간 표현, 노드의 정규화와 코드 생성, LIR을 거쳐 핫스팟 백엔드로

## 경계에 있는 페이지

- [javac의 컴파일 과정](../concepts/javac-compilation-process.md) — 같은 컴파일의 앞쪽 절반과
  최적화의 분업
- [그랄VM과 네이티브 이미지](../concepts/graalvm-and-native-image.md) — 이 장의 컴파일러가
  제품이 된 쪽
- [구동 시간 줄이기의 실전](../concepts/jvm-startup-time-optimization.md) — 컴파일 시간을 구동
  시간의 한 항목으로 재는 쪽
- [메서드 호출과 디스패치](../concepts/method-invocation-and-dispatch.md) — 인라인이 넘어야
  하는 가상 메서드 디스패치
- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 탈출 분석이
  "모든 객체는 힙에" 라는 문장에 유보를 다는 자리

## 이어지는 허브

- [클래스 파일과 바이트코드](class-file-and-bytecode.md) — 이 구간의 입력이 만들어지는 곳
- [자바 기술 시스템](java-technology-system.md) — 이 컴파일러들을 품은 가상 머신과 JDK
- [JVM 모니터링과 문제 해결 도구](jvm-troubleshooting-tools.md) — 컴파일 결과를 꺼내 보는
  도구들이 놓인 자리
- [JVM 자동 메모리 관리](jvm-memory-management.md) — 컴파일된 코드가 다루는 메모리와 안전 지점

---
type: synthesis
title: 자바 기술 시스템
description: 언어 하나가 아니라 언어·가상 머신·클래스 라이브러리·명세를 묶은 시스템으로서의 자바 진입점 — 구성과 제품군, 오크에서 JDK 21까지의 판올림, 실제로 존재했던 가상 머신 구현들, 그리고 그랄VM·네이티브 이미지·확장 인터페이스로 이어지는 지금의 방향
generated: { by: "claude-opus-5", at: "2026-08-15T12:00:00Z" }
---

# 자바 기술 시스템

**이름의 범위가 곧 이 허브의 범위다.** 여기는 '자바'라는 말이 가리키는 것 전체 — 언어, 그
언어를 돌리는 가상 머신 구현들, 그것들을 묶어 배포하는 JDK, 그리고 그 시스템이 지나온 시간과
지금 가고 있는 방향 — 이 사는 자리다. 가상 머신 **안쪽**에서 메모리가 어떻게 관리되는지는
[JVM 자동 메모리 관리](jvm-memory-management.md)가, 그 상태를 **밖에서 재는 도구**는
[JVM 모니터링과 문제 해결 도구](jvm-troubleshooting-tools.md)가 담당한다.

## 무엇으로 이루어져 있는가

- [자바 기술 시스템의 구성과 제품군](../concepts/java-platform-editions.md) — JDK와 JRE의
  경계, 자바 카드·ME·SE·EE 네 제품군, 그리고 이 KB의 zhou2024 서술이 핫스팟 기준인 이유

## 어떻게 여기까지 왔는가

- [JDK 판올림의 역사](../concepts/jdk-release-history.md) — 그린 프로젝트에서 JDK 21까지,
  6개월 릴리스와 LTS 정책, OpenJDK와 오라클 JDK의 라이선스가 갈린 자리
- [자바 가상 머신 제품군](../concepts/java-virtual-machine-family.md) — 클래식·이그잭트·
  핫스팟·JRockit·J9·징, 그리고 자바 가상 머신이 아닌 도전자들

## 지금 어디로 가는가

- [그랄VM과 네이티브 이미지](../concepts/graalvm-and-native-image.md) — 폴리글랏 가상 머신,
  C2를 대체하려는 그랄 컴파일러, 핫스팟 없이 도는 서브스트레이트 VM
- [핫스팟의 모듈화와 확장 인터페이스](../concepts/hotspot-modularity-and-interfaces.md) —
  JVMPI·JVMDI에서 JVMTI로, 다시 JVMCI와 가비지 컬렉터 인터페이스로
- [자바 언어 진화 프로젝트](../concepts/java-language-evolution-projects.md) — 앰버가 올린
  구문들, 값 타입을 노리는 발할라, 네이티브 경계를 허무는 파나마

## 손으로 확인하기

- [OpenJDK 직접 빌드하기](../concepts/building-openjdk-from-source.md) — 소스·툴체인·부트 JDK,
  configure로 고르는 맞춤형 가상 머신, 템플릿 인터프리터를 디버깅하는 매개 변수

## 이어지는 허브

- [JVM 자동 메모리 관리](jvm-memory-management.md) — 이 가상 머신들이 메모리를 나누고 회수하는
  방법
- [JVM 모니터링과 문제 해결 도구](jvm-troubleshooting-tools.md) — 돌고 있는 가상 머신의 상태를
  꺼내 보는 쪽

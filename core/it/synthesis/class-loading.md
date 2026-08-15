---
type: synthesis
title: 클래스 로딩
description: 클래스 파일이 가상 머신 안의 살아 있는 타입이 되기까지 — 로딩·검증·준비·해석·초기화 다섯 단계, 클래스로더 계층과 부모 위임 모델, 그 모델이 실전에서 깨지는 자리들(SPI·OSGi·톰캣·핫스와프), 모듈 시스템, 그리고 판올림 기능의 백포트 관행
generated: { by: "claude-fable-5", at: "2026-08-15T12:00:00Z" }
---

# 클래스 로딩

[클래스 파일과 바이트코드](class-file-and-bytecode.md)가 형식과 실행을 다룬다면, 이 축은
그 **사이의 절차**다 — 디스크의 바이트 배열이 어떻게 검증되고, 메모리에 자리 잡고,
심벌 참조가 실제 주소로 바뀌고, 언제 초기화되는가. 그리고 그 절차를 수행하는 주체
(클래스로더)의 계층 규약과, 규약이 현실에서 깨지는 자리들을 본다.

## 절차

- [클래스 로딩 생애 주기](../concepts/class-loading-lifecycle.md) — 로딩부터 언로딩까지, 시작 시점의 여섯 조건
- [클래스 로딩 검증](../concepts/class-loading-verification.md) — 네 단계 검증이 무엇을 막는가
- [준비와 초기화](../concepts/class-preparation-and-initialization.md) — 기본값과 대입의 분리, 초기화 순서
- [심벌 참조 해석](../concepts/symbolic-reference-resolution.md) — 상수 풀의 이름이 실제 참조가 되는 규칙

## 로더와 위임

- [클래스로더와 부모 위임](../concepts/class-loaders-and-parent-delegation.md) — 계층 규약과 톰캣의 정통 배치
- [부모 위임이 깨지는 자리](../concepts/parent-delegation-challenges.md) — SPI·OSGi·핫스와프가 규약을 어기는 이유
- [자바 모듈 시스템](../concepts/java-module-system.md) — 모듈화가 로더 계층에 가져온 변화

## 판올림과 기능 이식

- [JDK 기능 분류와 백포트](../concepts/jdk-feature-categories-and-backporting.md) — 어떤 기능이 구판으로 이식되는가

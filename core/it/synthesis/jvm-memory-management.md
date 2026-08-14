---
type: synthesis
title: JVM 자동 메모리 관리
description: 자바 가상 머신이 메모리를 나누고, 죽은 객체를 판정하고, 회수하는 전체 경로. 컬렉터 선택과 그 값을 재는 기준까지
generated: { by: "human:me", at: "2026-08-11T00:00:00Z" }
---

# JVM 자동 메모리 관리

C와 C++ 개발자가 손으로 하던 일을 가상 머신이 대신 맡을 때 무엇이 생기고 무엇이
사라지는지를 다룬다. 축은 셋이다. 메모리가 어디에 놓이는가, 무엇이 죽었다고
판정하는가, 어떻게 치우는가. 마지막 두 절은 그 선택을 실제로 하는 자리다.

## 메모리가 놓이는 자리

- [런타임 데이터 영역과 메모리 오버플로](../concepts/jvm-runtime-data-areas.md) — 일곱 영역과 각각이 고갈될 때 나오는 예외
- [객체 생성과 메모리 레이아웃](../concepts/object-creation-and-memory-layout.md) — 포인터 밀치기와 TLAB, 객체 헤더의 세 부분, 핸들과 다이렉트 포인터

## 무엇이 죽었는가

- [객체 생존 판정](../concepts/object-liveness-determination.md) — 참조 카운팅이 쓰이지 않는 이유, GC 루트와 참조 네 가지 세기

## 어떻게 치우는가

- [가비지 컬렉션 알고리즘](../concepts/garbage-collection-algorithms.md) — 마크 스윕, 마크 카피, 마크 컴팩트가 치르는 값
- [세대 단위 컬렉션과 메모리 할당 전략](../concepts/generational-collection.md) — 세 가지 경험 법칙과 에덴에서 구세대로 가는 네 가지 길
- [핫스팟의 가비지 컬렉션 구현 상세](../concepts/hotspot-gc-implementation.md) — 안전 지점, 카드 테이블, 쓰기 장벽, 삼색 표시

## 실제 컬렉터들

- [클래식 가비지 컬렉터](../concepts/hotspot-classic-collectors.md) — 시리얼부터 G1까지 일곱 개의 조합과 제약
- [저지연 가비지 컬렉터](../concepts/low-latency-collectors.md) — 셰넌도어와 ZGC가 정지 시간을 10밀리초 아래로 미는 방법

## 고르고 확인하기

- [적합한 가비지 컬렉터 고르기](../concepts/choosing-a-garbage-collector.md) — 선택을 좌우하는 세 요인과 -Xlog 읽는 법

## 이어지는 허브

- [JVM 모니터링과 문제 해결 도구](jvm-troubleshooting-tools.md) — 여기서 정한 값이 실제로 어떻게 나오고 있는지 꺼내 보는 도구들
- [자바 기술 시스템](java-technology-system.md) — 이 메모리 관리를 수행하는 가상 머신과 JDK 자체

---
type: synthesis
title: 데이터 아키텍처
description: 도메인 중심 데이터 아키텍처 개념들의 진입점
generated: { by: "claude-opus-5", at: "2026-08-06T08:10:00Z" }
---

# 데이터 아키텍처

대규모 조직에서 데이터의 소유·경계·흐름을 어떻게 조직하는가. 현재는 Strengholt 2023
(2장) 한 소스에서 출발한 축이며, 소스가 쌓여 주제가 갈라지면 허브를 나눈다.

## 기초 전제

- [데이터 통합 딜레마](../concepts/data-integration-dilemma.md) — 애플리케이션 간 이동에는 변환이 항상 필요한 이유
- [골든 소스](../concepts/golden-source.md) — 특정 맥락에서 데이터의 권위 있는 출처(authoritative source)가 되는 애플리케이션

## 경계 긋기

- [바운디드 컨텍스트](../concepts/bounded-context.md) — 도메인 해결 공간의 논리적 경계와 그 설계 원칙
- [유비쿼터스 언어](../concepts/ubiquitous-language.md) — 경계 안에서 공유되는 언어, 전사 통일이 아닌 이유
- [비즈니스 역량](../concepts/business-capability.md) — 문제 공간을 나누는 기준, 도메인 경계의 출발점

## 도메인 운용

- [도메인 역할 유형](../concepts/domain-role-topology.md) — 소스 정렬·소비자 정렬·애그리게이트·구성자 도메인
- [공유 역량의 데이터 소유권](../concepts/shared-capability-ownership.md) — 한 시스템을 여러 도메인이 쓸 때의 소유권
- [아키텍처 퀀텀으로서의 데이터 제품](../concepts/data-product-as-architectural-quantum.md) — 서비스 메시→데이터 메시 유추의 성립과 한계

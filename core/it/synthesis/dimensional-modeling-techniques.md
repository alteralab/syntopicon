---
type: synthesis
title: 차원 모델링 기법
description: Kimball 차원 모델링의 기초와 기법 카탈로그 진입점
generated: { by: "human:me", at: "2026-08-07T16:00:00Z" }
---

# 차원 모델링 기법

## 기초

- [차원 모델링](../concepts/dimensional-modeling.md) — 두 목표와 5대 오해
- [팩트 테이블](../concepts/fact-table.md) — 측정 이벤트 1:1·grain·합산 가능성
- [차원 테이블](../concepts/dimension-table.md) — 속성이 곧 분석력, 대리 키
- [4단계 설계](../concepts/four-step-dimensional-design.md) — 프로세스→grain→차원→팩트
- [설계 리뷰](../concepts/dimensional-design-review.md) — 흔한 설계 결함 체크리스트와 리뷰 운영

## 팩트 기법

- [스냅샷 팩트 테이블](../concepts/snapshot-fact-tables.md) — 주기·누적 스냅샷과 부분 합산
- [통합 팩트 테이블](../concepts/consolidated-fact-table.md) — 실적 vs 예산, drill-across 트레이드오프
- [클릭스트림 팩트](../concepts/clickstream-facts.md) — 세션화와 웹 이벤트 grain

## 차원 기법

- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — 타입 0–7
- [표준 차원](../concepts/conformed-dimension.md) — drill-across의 전제
- [버스 아키텍처](../concepts/enterprise-bus-architecture.md) — 버스 매트릭스와 애자일 골격
- [퇴화 차원](../concepts/degenerate-dimension.md) — 차원 없는 트랜잭션 키
- [역할 연기 차원](../concepts/role-playing-dimension.md) — 한 물리 차원의 다역할
- [정크 차원](../concepts/junk-dimension.md) — 플래그·지표 묶음
- [다치 차원과 브리지](../concepts/multivalued-dimension-bridge.md) — 다대다와 가중치
- [슈퍼타입/서브타입 스키마](../concepts/supertype-subtype-schema.md) — 이종 상품 처리

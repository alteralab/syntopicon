---
type: synthesis
title: 데이터 웨어하우스 모델링
description: DW 모델링 방법론(차원 모델링·Data Vault)의 진입점
generated: { by: "human:me", at: "2026-08-06T17:55:00Z" }
---

# 데이터 웨어하우스 모델링

두 방법론이 같은 문제(분석용 데이터의 구조화)에 다른 우선순위로 답한다 —
Kimball은 이해 가능성·질의 성능을, Data Vault는 감사 가능성·원천 보존을 앞세운다.

## 차원 모델링 (Kimball)

- [차원 모델링](../concepts/dimensional-modeling.md) — 두 목표와 5대 오해
- [팩트 테이블](../concepts/fact-table.md) — 측정 이벤트 1:1·grain·합산 가능성
- [차원 테이블](../concepts/dimension-table.md) — 속성이 곧 분석력
- [Kimball DW/BI 아키텍처](../concepts/kimball-dwbi-architecture.md) — 4구획과 버스

## Data Vault (Linstedt)

- [Data Vault 모델링](../concepts/data-vault-modeling.md) — 업무 키 중심 3-엔티티
- [Hub](../concepts/data-vault-hub.md) · [Link](../concepts/data-vault-link.md) · [Satellite](../concepts/data-vault-satellite.md)
- [업무 키](../concepts/business-key.md) — 두 방법론이 공유하는 뿌리 개념

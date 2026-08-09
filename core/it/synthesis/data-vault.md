---
type: synthesis
title: Data Vault
description: Data Vault 2.0의 모델링·아키텍처·적재·상위 계층 진입점
generated: { by: "human:me", at: "2026-08-07T16:00:00Z" }
---

# Data Vault

## 모델링

- [Data Vault 모델링](../concepts/data-vault-modeling.md) — 업무 키 중심 3-엔티티 개요
- [Hub](../concepts/data-vault-hub.md) — 업무 키의 유일 목록과 응용 패턴
- [Link](../concepts/data-vault-link.md) — 다대다 관계·same-as·계층·무이력 링크
- [Satellite](../concepts/data-vault-satellite.md) — 맥락·이력과 분할·응용 새틀라이트
- [업무 키](../concepts/business-key.md) — 식별·추적·조회의 뿌리 개념
- [PIT·Bridge 테이블](../concepts/point-in-time-and-bridge-tables.md) — 조인 폭발에서 성능 회복
- [참조 테이블](../concepts/reference-table.md) — 허브가 아닌 코드·분류의 자리

## 아키텍처와 방법론

- [Data Vault 아키텍처](../concepts/data-vault-architecture.md) — staging→raw vault→mart 3계층과 hard/soft rule
- [Data Vault 방법론](../concepts/data-vault-methodology.md) — Scrum·CMMI·Six Sigma·TQM의 혼합과 이유
- [Business Vault](../concepts/business-vault.md) — soft rule이 사는 중간 계층
- [정보 마트](../concepts/information-mart.md) — 차원 모델로의 전개와 가상화 판단

## 적재

- [스테이징 영역](../concepts/staging-area.md) — 무이력 규율과 계산 열
- [Data Vault 해싱](../concepts/hashing-in-data-vault.md) — 해시 키·hash diff 계산 규율
- [적재 패턴](../concepts/data-vault-loading-patterns.md) — 엔티티별 적재·종료일·삭제 처리

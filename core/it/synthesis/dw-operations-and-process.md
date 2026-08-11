---
type: synthesis
title: DW 운영과 프로세스
description: DW/BI의 아키텍처·라이프사이클·ETL·데이터 관리 진입점
generated: { by: "human:me", at: "2026-08-07T16:00:00Z" }
---

# DW 운영과 프로세스

## 아키텍처와 프로세스

- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계/분석계 분리와 아키텍처 지형
- [데이터 레이크](../concepts/data-lake.md) — 스키마를 강제하지 않는 분석 저장소
- [Kimball DW/BI 아키텍처](../concepts/kimball-dwbi-architecture.md) — 4구획과 프레젠테이션 4원칙
- [Kimball 라이프사이클](../concepts/kimball-lifecycle.md) — 로드맵과 실패 요인
- [차원 설계 프로세스](../concepts/dimensional-design-process.md) — 워크숍 운영과 산출물

## ETL

- [ETL 서브시스템](../concepts/etl-subsystems.md) — 34종의 4그룹 압축
- [지각 도착 데이터](../concepts/late-arriving-data.md) — 지각 팩트·차원 처리 규칙

## 물리화와 증분 처리

- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 다시 계산할 것인가 저장할 것인가
- [증분 처리와 그 대가](../concepts/incremental-processing-tradeoffs.md) — 상태·멱등성·전체 재구축
- [증분 갱신 전략](../concepts/incremental-update-strategies.md) — 추가·병합·삭제 후 삽입·파티션 덮어쓰기
- [dbt 스냅샷](../concepts/dbt-snapshots.md) — SCD 타입 2를 도구가 구현하는 방식

## 데이터 관리

- [마스터 데이터 관리](../concepts/master-data-management.md) — 운영적 vs 분석적 MDM
- [메타데이터 관리](../concepts/metadata-management.md) — 3종 분류와 Meta/Metrics/Error Mart
- [데이터 품질 관리](../concepts/data-quality-management.md) — 교정 위치와 나쁜 데이터의 가치

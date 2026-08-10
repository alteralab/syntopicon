---
type: guide
title: "IT 지식"
description: "서적·논문·기술 문서에서 축적한 IT 개념"
generated: { by: "tools/kb-new", at: "2026-08-05T02:09:19Z" }
---

# IT 지식

서적·논문·기술 문서에서 축적한 IT 개념

## Hubs

<!-- 허브(synthesis) 링크 + 한 줄 설명, 10–30개. 포인터만 — 본문 발췌·수치 복제
     금지(진입점 부패 벡터, PLAN §3). 갱신 후보는 kb-lint의 링크 차수 대조가 낸다. -->

- [데이터 웨어하우스 모델링](synthesis/data-warehouse-modeling.md) — DW 축의 부모 허브
  - [차원 모델링 기법](synthesis/dimensional-modeling-techniques.md) — Kimball 기초·기법 카탈로그
  - [Data Vault](synthesis/data-vault.md) — 모델링·아키텍처·적재
  - [DW 운영과 프로세스](synthesis/dw-operations-and-process.md) — 라이프사이클·ETL·데이터 관리
- [카프카](synthesis/kafka-basics.md) — 스트리밍 축의 부모 허브
  - [카프카 내부 구조](synthesis/kafka-internals.md) — 메타데이터·복제·요청 처리·물리 저장
  - [카프카 설치와 운영](synthesis/kafka-operations.md) — 설정 기준·클러스터 산정·튜닝
- [데이터 시스템 아키텍처 트레이드오프](synthesis/data-systems-architecture-tradeoffs.md) — 운영/분석·클라우드·분산 선택 축의 허브
- [저장 엔진](synthesis/storage-engines.md) — 디스크에 데이터를 놓는 구조와 B-트리 대 LSM의 대비


## Tools

- 검색: `qmd query <질의> -c it` / 형태소 레그 `tools/ksearch`
- 저장: `/kb-ingest --kb it` — inbox/ 경유
- 점검: `tools/lint --kb it`

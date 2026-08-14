---
type: synthesis
title: 저장 엔진
description: 데이터를 디스크에 놓는 구조와 그 선택이 치르는 값 — 온디스크 형식과 페이지 배치, B-트리 계열과 LSM 계열의 대비, 메모리와 디스크를 잇는 페이지 캐시, 분석용 열 지향 저장과 질의 실행, 그리고 단일 키 범위를 넘는 색인들
generated: { by: "human:me", at: "2026-08-10T23:00:00Z" }
---

# 저장 엔진

데이터베이스가 레코드를 디스크에 실제로 어떻게 놓는지를 다룬다. 축은 하나다 —
제자리에서 고치는 가변 구조(B-트리)와, 고치지 않고 덧붙이는 불변 구조(LSM 트리)의
대비. 그 아래로 바이트를 배치하는 층이 있고, 위로는 디스크와 메모리를 잇는 캐시가
있으며, 둘의 값을 재는 자가 마지막 절에 있다.

## 자리와 분류

- [데이터베이스 관리 시스템의 구조](../concepts/dbms-architecture.md) — 저장 엔진이 DBMS의 어디에 있고 무엇을 맡는가
- [저장 엔진의 분류](../concepts/storage-engine-classification.md) — 메모리와 디스크, 행과 열, 그리고 버퍼링·불변성·순서라는 세 변수
- [데이터 파일과 인덱스 파일](../concepts/data-files-and-index-files.md) — 힙·해시·인덱스 구조형 테이블과 클러스터형 인덱스
- [디스크 기반 저장의 제약](../concepts/disk-based-storage-constraints.md) — 블록이 최소 단위라는 사실과 로그 층이 겹칠 때의 손해

## 바이트를 놓는 층

- [온디스크 파일 형식](../concepts/on-disk-file-format.md) — 프리미티브·바이트 순서·헤더와 트레일러, 버저닝과 체크섬
- [슬롯 페이지와 셀 레이아웃](../concepts/slotted-pages.md) — 가변 크기 레코드를 고정 크기 페이지에 놓는 법

## 가변 쪽

- [B-트리](../concepts/b-tree-structure.md) — 팬아웃과 낮은 높이, 구분 키, 온디스크 노드의 실제 모양, 노드 분할과 병합
- [B-트리 구현 기법](../concepts/b-tree-implementation-techniques.md) — 간접 이진 탐색·브레드크럼·재균형·벌크 로딩·압축
- [B-트리 배큠과 유지보수](../concepts/b-tree-vacuum-and-maintenance.md) — 살아 있는 셀과 가비지, 조각 모음, 자유 페이지 목록
- [B-트리 변형](../concepts/b-tree-variants.md) — 쓰기 시 복사·게으른 B-트리·FD-트리·Bw-트리·캐시 무관

## 불변 쪽

- [LSM 트리](../concepts/lsm-tree.md) — 멤테이블과 플러시, 툼스톤, 병합-반복과 조정, SSTable
- [LSM 컴팩션](../concepts/lsm-compaction.md) — 레벨형·크기 단계별·타임 윈도우 전략과 툼스톤 보존
- [블룸 필터](../concepts/bloom-filter.md) — 없는 키를 확실히 배제해 여는 테이블 수를 줄이는 장치

## 메모리와 디스크 사이

- [페이지 캐시와 축출](../concepts/page-cache-and-eviction.md) — 페이지 인·더티·플러시·축출, 핀, 그리고 FIFO에서 TinyLFU까지의 교체 전략

## 분석 쪽 저장과 질의

- [열 지향 저장](../concepts/column-oriented-storage.md) — 열을 붙여 두는 배치, 비트맵 인코딩과 런렝스, 정렬 순서, 열 파일에 쓰기
- [질의 실행 — 컴파일과 벡터화](../concepts/query-execution-compilation-and-vectorization.md) — 분석 질의의 CPU 병목과 그 두 처방
- [데이터 큐브와 구체화 뷰](../concepts/data-cubes-and-materialized-views.md) — 집계를 미리 계산해 두는 쪽과 그 유연성의 대가

## 단일 키 범위를 넘는 색인

- [다차원 색인](../concepts/multidimensional-indexes.md) — 연결 색인의 한계, 공간 채움 곡선과 R-트리
- [전문 검색 색인](../concepts/full-text-search-indexes.md) — 역색인과 포스팅 리스트, n-그램과 편집 거리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 의미 검색과 Flat·IVF·HNSW

## 값을 재는 자

- [읽기·쓰기·공간 증폭](../concepts/read-write-space-amplification.md) — 둘을 줄이면 셋째가 나빠진다는 RUM 추측
- [B-트리와 LSM 트리 견주기](../concepts/comparing-b-trees-and-lsm-trees.md) — 읽기 경로·범위 질의·순차 대 임의 쓰기로 두 계열을 견주는 자리

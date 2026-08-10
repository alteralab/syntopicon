---
type: synthesis
title: 저장 엔진
description: 데이터를 디스크에 놓는 구조와 그 선택이 치르는 값 — B-트리 계열과 LSM 계열의 대비를 중심으로
generated: { by: "human:me", at: "2026-08-10T23:00:00Z" }
---

# 저장 엔진

데이터베이스가 레코드를 디스크에 실제로 어떻게 놓는지를 다룬다. 축은 하나다 —
제자리에서 고치는 가변 구조(B-트리)와, 고치지 않고 덧붙이는 불변 구조(LSM 트리)의
대비. 그 둘의 값을 재는 자가 마지막 절에 있다.

## 자리와 분류

- [데이터베이스 관리 시스템의 구조](../concepts/dbms-architecture.md) — 저장 엔진이 DBMS의 어디에 있고 무엇을 맡는가
- [저장 엔진의 분류](../concepts/storage-engine-classification.md) — 메모리와 디스크, 행과 열, 그리고 버퍼링·불변성·순서라는 세 변수
- [데이터 파일과 인덱스 파일](../concepts/data-files-and-index-files.md) — 힙·해시·인덱스 구조형 테이블과 클러스터형 인덱스
- [디스크 기반 저장의 제약](../concepts/disk-based-storage-constraints.md) — 블록이 최소 단위라는 사실과 로그 층이 겹칠 때의 손해

## 가변 쪽

- [B-트리](../concepts/b-tree-structure.md) — 팬아웃과 낮은 높이, 구분 키, 노드 분할과 병합

## 불변 쪽

- [LSM 트리](../concepts/lsm-tree.md) — 멤테이블과 플러시, 툼스톤, 병합-반복과 조정, SSTable
- [LSM 컴팩션](../concepts/lsm-compaction.md) — 레벨형·크기 단계별·타임 윈도우 전략과 툼스톤 보존
- [블룸 필터](../concepts/bloom-filter.md) — 없는 키를 확실히 배제해 여는 테이블 수를 줄이는 장치

## 값을 재는 자

- [읽기·쓰기·공간 증폭](../concepts/read-write-space-amplification.md) — 둘을 줄이면 셋째가 나빠진다는 RUM 추측

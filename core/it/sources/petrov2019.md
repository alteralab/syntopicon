---
type: book
title: "Database Internals: A Deep Dive into How Distributed Data Systems Work"
author:
  - { family: Petrov, given: Alex }
issued: "2019"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-492-04034-7"
snapshot: /it/archive/petrov2019/
snapshot_sha256: "55ac103feae7e5126c3b5e25b88e71e27ab3cb964332275cd98b9868be39f4bb"
accessed: "2026-08-10"
---

# Database Internals (1e)

데이터베이스 저장 엔진의 정본 — Apache Cassandra 커미터 저작. foundational
슬롯이다. 1부가 저장 엔진(B-tree, LSM), 2부가 분산 시스템(합의, 복제)이라
기존 KB의 두 축과 각각 다른 층위에서 만난다.

참조원: 한국어판 『데이터베이스 인터널스』(스냅샷 동봉) — 역어 참조 전용,
소스 아님.

이 소스가 닿을 자리: 카프카의 물리 저장(세그먼트·인덱스·압착)이 LSM 계열의
특수 사례이고, DDIA의 분산 서술이 이 책 2부와 겹친다. 기존 페이지 갱신이
신규 못지않게 나올 자리다.

이번 런 범위: **1부 저장 엔진의 도입부와 B-tree 계열** (1장 Introduction and
Overview, 2장 B-Tree Basics, 7장 Log-Structured Storage). LSM과 B-tree를 한
런에 넣는 이유는 둘의 대비가 이 책의 뼈대이기 때문이다. 2부(분산)는 후속 런.
locator의 페이지는 책 내면 기준이다.

---
type: synthesis
title: 카프카 커넥트와 데이터 파이프라인
description: 카프카를 외부 데이터 저장소에 잇는 쪽 진입점 — 파이프라인 설계에서 따질 것들, 커넥트를 띄우고 설정하는 법, 부품별 책임, 복사 도중의 변환
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
---

# 카프카 커넥트와 데이터 파이프라인

**카프카 밖과 닿는 쪽이다.** 애플리케이션 코드에서 `send()`와 `poll()`을 부르는 쪽은
[카프카 클라이언트](kafka-clients.md)가 담당하고, 여기는 **코드를 고칠 수 없는 데이터
저장소**를 카프카에 붙이는 자리다. 클러스터 사이를 잇는 미러링은
[카프카 설치와 운영](kafka-operations.md)에 있다.

순서가 있다. 먼저 **무엇을 따져야 하는지**를 정하고, 그다음 커넥트가 그 요구에 어떻게
답하는지를 본다.

## 무엇을 따질 것인가

- [데이터 파이프라인 설계 고려사항](../concepts/kafka-data-pipeline-considerations.md) — 적시성·신뢰성·처리량·데이터 형식·변환(ETL과 ELT)·보안·장애 처리·결합과 민첩성

## 커넥트

- [카프카 커넥트](../concepts/kafka-connect.md) — 프로듀서·컨슈머 대신 커넥트를 고르는 기준, 워커 설정, REST API로 커넥터를 만드는 두 예제, 커넥트를 쓰지 않는 다른 길들
- [카프카 커넥트 내부 구조](../concepts/kafka-connect-internals.md) — 커넥터·태스크·워커·컨버터가 나눠 가진 책임과 소스 시스템 좌표를 저장하는 오프셋 관리
- [단일 메시지 변환(SMT)](../concepts/kafka-single-message-transformations.md) — 복사 도중의 무상태 변환 열한 가지와 데드 레터 큐

## 커넥트 위에 지어진 것

- [미러메이커](../concepts/kafka-mirrormaker.md) — 커넥트를 쓰는 대표 사례. 클러스터 간 미러링

## 웨어하우스 쪽에서 같은 소재를 다루는 곳

- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 같은 ETL을 차원 웨어하우스 백룸의 34개 분해로 본 쪽
- [데이터 레이크](../concepts/data-lake.md) — ELT의 논거인 "원시 데이터가 낫다"가 사는 곳
- [EDW](../concepts/enterprise-data-warehouse.md) — 이 파이프라인이 흔히 향하는 목적지

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 클라이언트](kafka-clients.md) — 커넥트가 대체하는 그 클라이언트들
- [카프카 설치와 운영](kafka-operations.md) — 미러메이커와 다중 클러스터 배치
- [DW 운영과 프로세스](dw-operations-and-process.md) — 웨어하우스 쪽 ETL 진입점

---
type: synthesis
title: 카프카 설치와 운영
description: 클러스터를 세우고 돌릴 때 판단이 필요한 설정, 하드웨어 산정, 튜닝, 돌아가는 클러스터를 코드로 관리하는 작업, 그리고 클러스터를 여럿 두게 될 때의 배치와 미러링의 진입점
generated: { by: "human:me", at: "2026-08-12T15:00:00Z" }
---

# 카프카 설치와 운영

설치 절차 자체가 아니라 그 과정에서 내려야 하는 판단을 다룬다. 명령어와 설정
파일 예시는 벤더 문서가 담당하고(`/docs-query`), 여기에는 무엇을 어떤 기준으로
정하는지만 둔다. 예외는 아래 "프로그램으로 관리하기"인데, 거기서는 관리 작업이
곧 API 호출이라 대표 코드가 페이지마다 하나씩 들어간다.

## 설정과 산정

- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 파티션 수, 복제 팩터, 보존, 세그먼트를 정하는 기준
- [카프카 하드웨어와 클러스터 산정](../concepts/kafka-hardware-and-cluster-sizing.md) — 병목 다섯 가지와 브로커 대수를 정하는 두 계산

## 프로덕션 준비

- [카프카 프로덕션 튜닝](../concepts/kafka-production-tuning.md) — 가상 메모리와 파일시스템, 네트워크 커널, G1GC, 랙 배치

## 프로그램으로 관리하기

- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 관리 작업을 애플리케이션 코드에서 실행하는 통로. 비동기·최종적 일관성 설계, 만들고 닫기, DNS와 타임아웃, 목업 테스트
- [토픽 관리](../concepts/kafka-topic-administration.md) — 목록·설명·생성·삭제, 없으면 그 자리에서 만드는 관용 형태
- [설정 관리](../concepts/kafka-config-administration.md) — 설정 리소스 3종, 기본값과 다른 것 골라내기, 네 가지 변경 작업 유형
- [컨슈머 그룹 관리](../concepts/kafka-consumer-group-administration.md) — 그룹 열거와 설명, 랙 계산, 오프셋 리셋과 그것이 걸리는 곳
- [파티션과 레플리카 관리](../concepts/kafka-partition-and-replica-administration.md) — 파티션 추가, 레코드 삭제, 리더 선출, 레플리카 재할당

## 클러스터가 여럿일 때

- [클러스터 간 데이터 미러링](../concepts/kafka-cross-cluster-mirroring.md) — 복제와 미러링이 갈리는 이유, 클러스터를 여럿 두는 다섯 가지 동기, 데이터센터 간 통신이 거는 제약, 미러메이커 밖의 솔루션들
- [카프카 다중 클러스터 아키텍처](../concepts/kafka-multicluster-architectures.md) — 허브-앤-스포크, 액티브-액티브, 액티브-스탠바이, 스트레치 클러스터 네 형태와 각각이 포기하는 것
- [미러메이커](../concepts/kafka-mirrormaker.md) — 미러메이커 2.0의 구조와 복제 흐름 설정, 필요한 ACL, 배포 위치 판단, 랙 모니터링과 튜닝
- [카프카 클러스터 장애 조치](../concepts/kafka-cluster-failover.md) — RTO와 RPO, 넘어갈 때 생기는 유실과 중복, 시작 오프셋을 정하는 네 가지 방법

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 신뢰성과 정확히 한 번](kafka-reliability.md) — 이 설정들이 지키려는 보장과 그것이 성립하는지 재는 방법
- [카프카 커넥트와 데이터 파이프라인](kafka-connect-and-pipelines.md) — 미러메이커가 올라타 있는 커넥트 프레임워크와, 카프카 밖 저장소를 잇는 일반 절차

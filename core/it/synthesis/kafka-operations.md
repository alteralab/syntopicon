---
type: synthesis
title: 카프카 설치와 운영
description: 클러스터를 세우고 돌릴 때 판단이 필요한 설정, 하드웨어 산정, 튜닝, 그리고 클러스터를 여럿 두게 될 때의 배치와 미러링의 진입점
generated: { by: "human:me", at: "2026-08-12T12:00:00Z" }
---

# 카프카 설치와 운영

설치 절차 자체가 아니라 그 과정에서 내려야 하는 판단을 다룬다. 명령어와 설정
파일 예시는 벤더 문서가 담당하고(`/docs-query`), 여기에는 무엇을 어떤 기준으로
정하는지만 둔다.

## 설정과 산정

- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — 파티션 수, 복제 팩터, 보존, 세그먼트를 정하는 기준
- [카프카 하드웨어와 클러스터 산정](../concepts/kafka-hardware-and-cluster-sizing.md) — 병목 다섯 가지와 브로커 대수를 정하는 두 계산

## 프로덕션 준비

- [카프카 프로덕션 튜닝](../concepts/kafka-production-tuning.md) — 가상 메모리와 파일시스템, 네트워크 커널, G1GC, 랙 배치

## 클러스터가 여럿일 때

- [클러스터 간 데이터 미러링](../concepts/kafka-cross-cluster-mirroring.md) — 복제와 미러링이 갈리는 이유, 클러스터를 여럿 두는 다섯 가지 동기, 데이터센터 간 통신이 거는 제약, 미러메이커 밖의 솔루션들
- [카프카 다중 클러스터 아키텍처](../concepts/kafka-multicluster-architectures.md) — 허브-앤-스포크, 액티브-액티브, 액티브-스탠바이, 스트레치 클러스터 네 형태와 각각이 포기하는 것
- [미러메이커](../concepts/kafka-mirrormaker.md) — 미러메이커 2.0의 구조와 복제 흐름 설정, 필요한 ACL, 배포 위치 판단, 랙 모니터링과 튜닝
- [카프카 클러스터 장애 조치](../concepts/kafka-cluster-failover.md) — RTO와 RPO, 넘어갈 때 생기는 유실과 중복, 시작 오프셋을 정하는 네 가지 방법

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 신뢰성과 정확히 한 번](kafka-reliability.md) — 이 설정들이 지키려는 보장과 그것이 성립하는지 재는 방법

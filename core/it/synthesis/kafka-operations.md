---
type: synthesis
title: 카프카 설치와 운영
description: 클러스터를 세우고 돌릴 때 판단이 필요한 설정, 하드웨어 산정, 튜닝의 진입점
generated: { by: "human:me", at: "2026-08-10T19:00:00Z" }
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

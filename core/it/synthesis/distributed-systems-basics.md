---
type: synthesis
title: 분산 시스템 기초
description: 복제·합의·샤딩이 딛고 서는 바닥 — 네트워크와 시간에 대한 틀린 가정, 메시지 전달 추상, 불가능성 결과, 타이밍·장애 모델, 그리고 그 위의 첫 두 장치인 실패 감지와 리더 선출
generated: { by: "claude-opus-5", at: "2026-08-14T12:00:00Z" }
---

# 분산 시스템 기초

이 축은 특정 시스템이 아니라 **분산 알고리즘이 무엇을 가정하고 무엇을 가정할 수 없는가**를
다룬다. 순서가 곧 논증이다 — 무엇이 틀린 가정인지 세고, 그 위에 통신 보장을 쌓고, 쌓아도
남는 한계를 확인하고, 그 한계를 다루려고 모델을 명시하고, 마지막으로 그 모델 위에 서는 첫
두 장치를 본다.

## 무엇이 틀린 가정인가

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 여러 기계로 가는 이유와 대가, 단일 노드와 근본적으로 다른 것
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — 네트워크·지연·대역폭·처리·시계·상태 일관성에 대한 가정과 연쇄 장애

## 통신에 보장을 쌓기

- [링크 추상과 메시지 전달 보장](../concepts/link-abstractions-and-message-delivery.md) — 공정 손실 링크에서 완벽한 링크까지, 멱등성과 중복 제거
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 전달과 처리를 가르는 자리

## 쌓아도 남는 한계

- [두 장군 문제와 FLP 불가능성](../concepts/two-generals-and-flp-impossibility.md) — 비동기 + 링크 장애가 합의를 막는 두 결과

## 가정을 명시하기

- [장애 모델과 시스템 동기성](../concepts/failure-models-and-synchrony.md) — 비동기·동기·부분 동기, 크래시·누락·비잔틴

## 그 위에 서는 첫 장치들

- [실패 감지](../concepts/failure-detection.md) — 하트비트·핑·phi-accrual·가십·FUSE와 정확성 대 효율
- [합의 없는 리더 선출](../concepts/leader-election-algorithms.md) — 불리·링·초대 알고리즘과 스플릿 브레인

## 이웃 축

- [분산 합의](../synthesis/distributed-consensus.md) — 과반 득표로 이 한계를 넘는 쪽
- [데이터 복제](../synthesis/data-replication.md) — 이 바닥 위에 얹히는 복제 계열 전체
- [데이터 샤딩](../synthesis/data-sharding.md) — 같은 바닥 위의 분할 계열

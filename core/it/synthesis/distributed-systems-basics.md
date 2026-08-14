---
type: synthesis
title: 분산 시스템 기초
description: 복제·합의·샤딩이 딛고 서는 바닥 — 네트워크와 시간에 대한 틀린 가정, 지연이 흔들리는 이유, 메시지 전달 추상, 물리 시계와 논리 시계, 불가능성 결과, 타이밍·장애 모델, 그 위의 첫 장치들인 실패 감지·리더 선출·가십 전파·펜싱 토큰, 그리고 이 전부를 실제로 시험하는 방법
generated: { by: "claude-opus-5", at: "2026-08-14T15:00:00Z" }
---

# 분산 시스템 기초

이 축은 특정 시스템이 아니라 **분산 알고리즘이 무엇을 가정하고 무엇을 가정할 수 없는가**를
다룬다. 순서가 곧 논증이다 — 무엇이 틀린 가정인지 세고, 그 위에 통신 보장을 쌓고, 시간을
어떻게 다룰지 정하고, 쌓아도 남는 한계를 확인하고, 그 한계를 다루려고 모델을 명시하고, 그
모델 위에 서는 첫 장치들을 보고, 마지막으로 그 전부가 정말 맞는지 확인하는 방법을 본다.

## 무엇이 틀린 가정인가

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 여러 기계로 가는 이유와 대가, 단일 노드와 근본적으로 다른 것
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — 네트워크·지연·대역폭·처리·시계·상태 일관성에 대한 가정과 연쇄 장애
- [네트워크 지연과 혼잡](../concepts/network-delay-and-congestion.md) — 큐잉이 만드는 지연 변동, 회선 교환이 유계 지연을 사 오는 값
- [프로세스 중단](../concepts/process-pauses.md) — 스레드가 아무 예고 없이 멈추는 여덟 경로와 실시간 보장의 값

## 통신에 보장을 쌓기

- [링크 추상과 메시지 전달 보장](../concepts/link-abstractions-and-message-delivery.md) — 공정 손실 링크에서 완벽한 링크까지, 멱등성과 중복 제거
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 전달과 처리를 가르는 자리

## 시간을 어떻게 다룰 것인가

- [물리 시계와 시각 동기화](../concepts/physical-clocks-and-synchronization.md) — 벽시계와 단조 시계, NTP 오차의 크기, 신뢰 구간(confidence interval)
- [ID 생성기와 논리 시계](../concepts/id-generators-and-logical-clocks.md) — 램포트 시계(Lamport clock)와 하이브리드 논리 시계, 선형성 있는 ID 배정

## 쌓아도 남는 한계

- [두 장군 문제와 FLP 불가능성](../concepts/two-generals-and-flp-impossibility.md) — 비동기 + 링크 장애가 합의를 막는 두 결과

## 가정을 명시하기

- [장애 모델과 시스템 동기성](../concepts/failure-models-and-synchrony.md) — 비동기·동기·부분 동기, 크래시·누락·비잔틴

## 그 위에 서는 첫 장치들

- [실패 감지](../concepts/failure-detection.md) — 하트비트·핑·phi-accrual·가십·FUSE와 정확성 대 효율
- [합의 없는 리더 선출](../concepts/leader-election-algorithms.md) — 불리·링·초대 알고리즘과 스플릿 브레인
- [가십 전파](../concepts/gossip-dissemination.md) — 감염 모형, 팬아웃(fanout)과 중복성, 오버레이 네트워크와 부분 뷰
- [펜싱 토큰과 리스](../concepts/fencing-tokens-and-leases.md) — 좀비(zombie)를 막는 단조 증가 토큰과 조건부 쓰기

## 정말 맞는지 확인하기

- [형식 방법과 무작위 테스트](../concepts/formal-methods-and-randomized-testing.md) — 모델 체커, 결함 주입과 Jepsen, 결정적 시뮬레이션 테스트(DST)

## 이웃 축

- [분산 합의](../synthesis/distributed-consensus.md) — 과반 득표로 이 한계를 넘는 쪽
- [데이터 복제](../synthesis/data-replication.md) — 이 바닥 위에 얹히는 복제 계열 전체
- [데이터 샤딩](../synthesis/data-sharding.md) — 같은 바닥 위의 분할 계열
- [레플리카 일관성](../synthesis/replica-consistency.md) — 이 가정 위에서 무엇을 약속할 수 있는가

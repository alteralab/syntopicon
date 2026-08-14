---
type: synthesis
title: 분산 합의
description: 서버 여럿을 하나의 고신뢰 상태 기계처럼 보이게 하는 문제와 Raft의 해법, 그리고 그 설계가 어떤 기준으로 선택됐는가
generated: { by: "human:me", at: "2026-08-11T00:00:00Z" }
---

# 분산 합의

일부 구성원이 죽어도 기계 여럿이 하나처럼 굴게 만드는 문제를 다룬다. 축은 하나다 —
문제 정의에서 시작해 Raft라는 한 알고리즘을 네 조각으로 따라가고, 마지막으로 그
알고리즘이 왜 그렇게 생겼는지를 본다.

## 문제

- [복제 상태 기계와 합의](../concepts/replicated-state-machine.md) — 합의 알고리즘이 존재하는 이유, 형식 성질 셋, 실용 시스템이 요구하는 네 성질
- [두 장군 문제와 FLP 불가능성](../concepts/two-generals-and-flp-impossibility.md) — 비동기 시스템에서 합의가 막히는 지점과 그 실무적 독법
- [합의 없는 리더 선출](../concepts/leader-election-algorithms.md) — 과반 없이 리더를 뽑는 계열과, 선출이 합의와 같은 문제인가라는 물음

## Raft의 네 조각

- [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md) — 서버 상태 셋, 논리적 시계로서의 임기, 무작위 선출 타임아웃
- [Raft의 로그 복제와 로그 매칭](../concepts/raft-log-replication.md) — 커밋의 정의와 과반 규칙, 일치성 검사, 어긋난 로그 되맞추기
- [Raft의 안전성과 선출 제약](../concepts/raft-safety.md) — 다섯 안전성 성질, 최신성 비교 규칙, 지난 임기 항목의 커밋 규칙
- [Raft의 클러스터 멤버십 변경](../concepts/raft-membership-change.md) — 공동 합의와 두 구성의 과반, 제거된 서버의 방해를 막는 규칙

## 왜 이렇게 생겼는가

- [이해 가능성을 설계 목표로 삼기](../concepts/designing-for-understandability.md) — Paxos 진단, 문제 분해와 상태 공간 축소, 사용자 연구 수치

## 이웃 축

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 이 알고리즘이 카프카에서 쓰이는 자리
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 정족수 대신 ISR을 쓰는 다른 선택
- [데이터 복제](../synthesis/data-replication.md) — 합의 없이 복제하는 계열 전체의 허브
- [분산 시스템 기초](../synthesis/distributed-systems-basics.md) — 이 알고리즘들이 딛는 통신·시간·장애의 가정

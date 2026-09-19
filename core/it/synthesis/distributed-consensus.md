---
type: synthesis
title: 분산 합의
description: 서버 여럿을 하나의 고신뢰 상태 기계처럼 보이게 하는 문제, Paxos 계열과 Raft라는 두 해법, 브로드캐스트라는 사촌 문제, 그것을 제품으로 파는 조율 서비스와 그 위에 잠금과 소유권을 세우는 응용 쪽 서술, 그리고 선의 가정을 걷어 낸 비잔틴 계열
generated: { by: "human:me", at: "2026-08-14T15:00:00Z" }
---

# 분산 합의

일부 구성원이 죽어도 기계 여럿이 하나처럼 굴게 만드는 문제를 다룬다. 순서가 곧 논증이다 —
문제를 정의하고, 그것과 동등한 브로드캐스트 문제를 보고, Paxos 계열을 따라간 뒤, 같은 문제를
이해 가능성을 목표로 다시 푼 Raft를 네 조각으로 따라가고, 마지막으로 선의 가정을 걷어 냈을 때
무엇이 달라지는지를 본다.

## 문제

- [복제 상태 기계와 합의](../concepts/replicated-state-machine.md) — 합의 알고리즘이 존재하는 이유, 형식 성질 셋, 실용 시스템이 요구하는 네 성질
- [두 장군 문제와 FLP 불가능성](../concepts/two-generals-and-flp-impossibility.md) — 비동기 시스템에서 합의가 막히는 지점과 그 실무적 독법
- [합의 없는 리더 선출](../concepts/leader-election-algorithms.md) — 과반 없이 리더를 뽑는 계열과, 선출이 합의와 같은 문제인가라는 물음

## 브로드캐스트라는 사촌 문제

- [원자 브로드캐스트](../concepts/atomic-broadcast.md) — 최선 노력·신뢰할 수 있는·원자
  브로드캐스트의 계단, 가상 동기화(virtual synchrony), 주키퍼의 ZAB

## Paxos 계열

- [Paxos](../concepts/paxos.md) — 제안자·수용자·학습자, 두 국면, 정족수와 `2f + 1`, 장애
  시나리오 넷
- [Paxos 변형들](../concepts/paxos-variants.md) — Multi-Paxos와 리스(lease), Fast Paxos,
  EPaxos, Flexible Paxos, 한 번 쓰기 레지스터로의 일반화

## Raft의 네 조각

- [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md) — 서버 상태 셋, 논리적 시계로서의 임기, 무작위 선출 타임아웃
- [Raft의 로그 복제와 로그 매칭](../concepts/raft-log-replication.md) — 커밋의 정의와 과반 규칙, 일치성 검사, 어긋난 로그 되맞추기
- [Raft의 안전성과 선출 제약](../concepts/raft-safety.md) — 다섯 안전성 성질, 최신성 비교 규칙, 지난 임기 항목의 커밋 규칙
- [Raft의 클러스터 멤버십 변경](../concepts/raft-membership-change.md) — 공동 합의와 두 구성의 과반, 제거된 서버의 방해를 막는 규칙

## 왜 이렇게 생겼는가

- [이해 가능성을 설계 목표로 삼기](../concepts/designing-for-understandability.md) — Paxos 진단, 문제 분해와 상태 공간 축소, 사용자 연구 수치

## 선의 가정을 걷어 내면

- [비잔틴 합의와 PBFT](../concepts/byzantine-consensus-pbft.md) — `3f + 1`이라는 셈법, 뷰와
  프라이머리, 세 단계와 교차 검증

## 합의를 제품으로 쓰기

- [조율 서비스](../concepts/coordination-services.md) — 주키퍼·etcd·Consul이 제공하는 잠금·리스·펜싱·실패 감지·변경 알림
- [소유권 선출 패턴](../concepts/ownership-election-pattern.md) — 그 제품 위에 CAS와 TTL만으로
  분산 잠금과 갱신 가능한 리스를 세우는 응용 쪽 서술. 알고리즘을 직접 구현하지 말라는 판정,
  선출을 아예 하지 않는 싱글턴의 가용성 산수, 그리고 호출받는 쪽이 소유자를 되확인하는 배치

## 이웃 축

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 이 알고리즘이 카프카에서 쓰이는 자리
- [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md) — 정족수 대신 ISR을 쓰는 다른 선택
- [데이터 복제](../synthesis/data-replication.md) — 합의 없이 복제하는 계열 전체의 허브
- [분산 시스템 기초](../synthesis/distributed-systems-basics.md) — 이 알고리즘들이 딛는 통신·시간·장애의 가정
- [레플리카 일관성](../synthesis/replica-consistency.md) — 합의가 사 오는 그 선형성과, 그것을 포기했을 때의 계약들
- [데이터베이스 트랜잭션](../synthesis/database-transactions.md) — 합의가 분산 트랜잭션의 코디네이터를 대체하는 자리

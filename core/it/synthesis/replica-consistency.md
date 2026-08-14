---
type: synthesis
title: 레플리카 일관성
description: 데이터 사본이 여럿일 때 클라이언트가 무엇을 볼 수 있는지를 규정하는 계약들과, 그 계약을 지키거나 회복하는 장치들
generated: { by: "claude-opus-5", at: "2026-08-14T15:00:00Z" }
---

# 레플리카 일관성

같은 데이터를 여러 곳에 두면 사본들이 서로 어긋난다. 이 축은 **그 어긋남을 어디까지
허용한다고 약속할 것인가**(일관성 모델)와 **어긋난 것을 어떻게 되돌릴 것인가**(수렴 장치)를
다룬다. 사본을 만드는 방식 자체는 형제 허브인
[데이터 복제](../synthesis/data-replication.md)에, 어긋남을 아예 없애는 과반 투표 쪽은
[분산 합의](../synthesis/distributed-consensus.md)에 있다.

## 무엇을 약속할 수 있는가

- [일관성 모델](../concepts/consistency-models.md) — 레지스터의 세 등급, 엄격·순차·인과·
  PRAM의 강도 서열, 벡터 클록(vector clock)
- [선형성](../concepts/linearizability.md) — 서열 맨 위의 모델, 선형화 지점(linearization
  point), 그 값과 합성성
- [CAP과 PACELC](../concepts/cap-and-pacelc.md) — 파티션이 났을 때와 나지 않았을 때의 선택,
  수확률(harvest)과 산출률(yield)

## 약속을 느슨하게 할 때

- [복제 지연이 만드는 이상](../concepts/replication-lag-anomalies.md) — 최종
  일관성(eventual consistency)이 만드는 세 이상과 세션 모델 넷
- [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md) — `w + r > n`으로 일관성을
  수로 조율하는 자리와 감시 레플리카(witness replica)
- [동시 쓰기 판정](../concepts/detecting-concurrent-writes.md) — happens-before 관계와 버전
  벡터(version vector)

## 어긋난 것을 되돌리기

- [쓰기 충돌 해소](../concepts/write-conflict-resolution.md) — 충돌 회피·LWW·형제
  값(siblings)·CRDT와 OT
- [강한 최종 일관성과 CRDT](../concepts/crdt-and-strong-eventual-consistency.md) — 사람에게
  묻지 않고 합쳐지는 자료 구조들
- [안티 엔트로피 기전](../concepts/anti-entropy-mechanisms.md) — 읽기 복구(read repair)·
  힌티드 핸드오프(hinted handoff)·머클 트리(Merkle tree)·비트맵 버전 벡터

## 이웃 축

- [데이터 복제](../synthesis/data-replication.md) — 사본을 만드는 세 갈래
- [분산 합의](../synthesis/distributed-consensus.md) — 어긋남 자체를 과반 투표로 막는 쪽
- [데이터베이스 트랜잭션](../synthesis/database-transactions.md) — 같은 낱말이 다른 축을
  가리키는 자리(ACID의 C)
- [분산 시스템 기초](../synthesis/distributed-systems-basics.md) — 이 모델들이 딛는 통신·
  시간·장애의 가정

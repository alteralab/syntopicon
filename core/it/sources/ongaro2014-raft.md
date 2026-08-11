---
type: paper-conference
title: "In Search of an Understandable Consensus Algorithm"
author:
  - { family: Ongaro, given: Diego }
  - { family: Ousterhout, given: John }
issued: "2014"
event-title: "2014 USENIX Annual Technical Conference (USENIX ATC 14)"
publisher: "USENIX Association"
URL: "https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro"
snapshot: /it/archive/ongaro2014-raft/
snapshot_sha256: "4d15bbcb14298974e4e2b36016c3455cdc7330e0a93536c99f63a1ec3cba2287"
accessed: "2026-08-11"
---

# In Search of an Understandable Consensus Algorithm (Raft)

합의 알고리즘의 정본 — Raft 원 논문. **이 KB의 첫 논문 소스**이고, 도서·논문·기술
문서 3타입 중 둘째 타입을 여는 자리다(§6).

이 소스가 메우는 공백: KB에 **합의(consensus) 축이 통째로 비어 있었다.**
[주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)가 쿼럼과 KRaft를 말하지만
전부 카프카 책에서 온 서술이고, KRaft의 Raft가 무엇인지는 출처 없이 낱말로만
있었다. 이 논문이 그 자리의 원전이다.

논문의 특성상 locator는 쪽수가 아니라 **절 번호**를 쓴다(§5.1 리더 선출 식).
proceedings 쪽번호(pp.305–319)와 PDF 쪽번호가 어긋나므로 절 번호가 안정적이다.

foundational 소스라 `stale_after`는 달지 않는다. 알고리즘 자체는 안 낡는다 —
낡는 것은 구현(etcd·KRaft·CockroachDB)이고 그건 각 구현의 소스가 담당한다.

이번 런 범위: **논문 전문**(16쪽, 본문 §1–§9). 확장 기술 보고서(Ongaro 박사학위
논문)는 별도 소스이며 이번 런에 포함하지 않는다.

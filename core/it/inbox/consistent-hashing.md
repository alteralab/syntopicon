---
type: concept
title: 일관 해싱
description: 샤드 수가 바뀔 때 옮기는 키를 최소화하는 해시 함수 계열 — 두 성질로 된 정의, "일관"이 복제 일관성이나 ACID 일관성과 무관하다는 점, 그리고 랑데부 해싱·점프 일관 해싱이 카산드라 방식과 갈라지는 지점
generated: { by: "claude-opus-5", at: "2026-08-13T17:00:00Z" }
status: draft
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 일관 해싱

- [정의 — 두 성질](#정의--두-성질)
- [여기서 "일관"은 무슨 뜻이 아닌가](#여기서-일관은-무슨-뜻이-아닌가)
- [알고리즘 계열](#알고리즘-계열)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **노드가 늘거나 줄 때 옮기는 키를 최소로 만드는 해시란 무엇인가.**

## 정의 — 두 성질

- **일관 해싱(consistent hashing) 알고리즘은 키를 지정된 개수의 샤드에 대응시키는 해시
  함수로, 두 성질을 만족하는 것**이다. 정의이므로 원문 직인용 (7장,
  p.263):[^kleppmann2026]

> - The number of keys mapped to each shard is roughly equal.
> - When the number of shards changes, as few keys as possible are moved from one shard to
>   another.

- 둘째 성질이 [해시 샤딩](../concepts/hash-sharding.md)의 모듈로 N 방식이 실패하는 바로 그
  자리다 — 그쪽은 노드 수가 바뀌면 대부분의 키가 움직인다 (7장, p.259).[^kleppmann2026]

## 여기서 "일관"은 무슨 뜻이 아닌가

- **여기서 "일관(consistent)"이라는 말은 6장의 레플리카 일관성이나 8장의 ACID 일관성과 아무
  관계가 없다. 이 말이 가리키는 것은 키가 가능하면 같은 샤드에 머무르려는 경향**이다 (7장,
  p.263).[^kleppmann2026]

## 알고리즘 계열

- **카산드라와 ScyllaDB가 쓰는 샤딩 알고리즘은 일관 해싱의 원래 정의와 비슷하다** (7장,
  p.263).[^kleppmann2026] 그 방식의 실제 동작(노드당 범위 여러 개, 무작위 경계)은
  [해시 샤딩](../concepts/hash-sharding.md)에 있다.
- **다른 일관 해싱 알고리즘들도 제안돼 있다 — 랑데부 해싱(rendezvous hashing)이라고도 하는
  최고 무작위 가중치(highest random weight), 그리고 점프 일관 해싱(jump consistent
  hashing)** 이다 (7장, p.263).[^kleppmann2026]
- 이들이 갈라지는 지점은 새 노드가 무엇을 받느냐다 — **이 접근들에서는 소수의 기존 샤드를
  부분 범위로 쪼개 새로 추가된 노드의 샤드를 만드는 대신, 새 노드에 다른 모든 노드에 흩어져
  있던 개별 키들을 배정한다. 어느 쪽이 더 나은지는 애플리케이션에 달렸다** (7장,
  p.263).[^kleppmann2026]

## 이어지는 페이지

- [해시 샤딩](../concepts/hash-sharding.md) — 이 함수가 쓰이는 자리와 카산드라·ScyllaDB의
  실제 구현
- [핫스팟과 쏠린 워크로드](../concepts/relieving-hot-spots.md) — 키가 고르게 분포해도 부하는
  고르지 않다는 반례
- [샤딩의 기본](../concepts/sharding-basics.md) — 파티션 키와 샤딩의 값어치

[^kleppmann2026]: Kleppmann & Riccomini 2026, 7장 "Sharding"

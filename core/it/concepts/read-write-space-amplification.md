---
type: concept
title: 읽기·쓰기·공간 증폭
description: 불변 저장이 치르는 세 가지 대가와 그것을 하나의 비용 모형으로 묶는 RUM 추측 — 둘을 줄이면 셋째가 나빠진다는 주장, B-트리와 LSM 트리를 그 자에 놓았을 때의 위치, 그리고 이 모형이 담지 못하는 것
generated: { by: "claude-opus-5", at: "2026-08-10T22:00:00Z" }
sources:
  - { id: petrov2019, resource: /it/sources/petrov2019.md }
---

# 읽기·쓰기·공간 증폭

이 페이지의 질문: **저장 구조의 비용을 무엇으로 재고, 왜 한쪽을 줄이면 다른 쪽이 나빠지는가.**

## 컴팩션 전략이 고르는 것

- 최적의 [컴팩션](../concepts/lsm-compaction.md) 전략을 구현하려면 여러 요인을 감안해야 한다. 갈림길은
  이렇다 (7장, pp.143–144):[^petrov2019]
  - **중복 레코드가 차지한 공간을 회수해 공간 오버헤드를 줄이는 쪽** — 테이블을 계속 다시 쓰게 되므로
    쓰기 증폭이 높아진다.
  - **데이터를 계속 다시 쓰지 않는 쪽** — 읽기 증폭(읽기 중 같은 키의 레코드를 조정하는 오버헤드)과
    공간 증폭(중복 레코드가 더 오래 보존되므로)이 높아진다.

## 세 가지 증폭

- 데이터를 불변 방식으로 디스크에 저장하면 세 문제를 만난다 (7장, p.144):[^petrov2019]
  - **읽기 증폭(read amplification)** — 데이터를 가져오려고 여러 테이블을 주소 지정해야 하는 데서 온다.
  - **쓰기 증폭(write amplification)** — 컴팩션 과정의 연속된 재작성에서 온다.
  - **공간 증폭(space amplification)** — 같은 키에 결부된 레코드가 여럿 저장되는 데서 온다.
- 쓰기 증폭을 두고 두 구조를 직접 견주는 것에 대해 저자가 경고한다. 원문 직인용 (7장,
  p.144):[^petrov2019]

> One of the big disputes in the database community is whether B-Trees or LSM Trees have
> lower write amplification. It is extremely important to understand the source of write
> amplification in both cases. In B-Trees, it comes from writeback operations and
> subsequent updates to the same node. In LSM Trees, write amplification is caused by
> migrating data from one file to the other during compaction. Comparing the two directly
> may lead to incorrect assumptions.

## RUM 추측

- 저장 구조의 인기 있는 비용 모형 하나가 세 요인을 감안한다 — **읽기(Read), 갱신(Update), 메모리(Memory)
  오버헤드.** 이를 RUM 추측(RUM Conjecture)이라 한다 (7장, p.144).[^petrov2019]
- 주장의 내용 (7장, p.144):[^petrov2019]

> RUM Conjecture states that reducing two of these overheads inevitably leads to change
> for the worse in the third one, and that optimizations can be done only at the expense
> of one of the three parameters.

- 이 세 매개변수로 서로 다른 저장 엔진을 견주면 각각이 무엇에 최적화했고 그것이 어떤 트레이드오프를
  함의하는지 이해할 수 있다. **이상적 해법은 낮은 메모리·쓰기 오버헤드를 유지하면서 가장 낮은 읽기
  비용을 주는 것이겠지만 현실에서는 달성할 수 없고 트레이드오프가 주어진다** (7장,
  p.144).[^petrov2019]

## 두 구조를 그 자에 놓으면

- **B-트리는 읽기에 최적화돼 있다.** B-트리에 쓰려면 디스크에서 레코드를 찾아야 하고, 같은 페이지에
  대한 후속 쓰기가 그 페이지를 디스크에서 여러 번 갱신해야 할 수 있다. **미래의 갱신·삭제를 위해
  예약한 여분 공간이 공간 오버헤드를 늘린다** (7장, pp.144–145).[^petrov2019]
- **LSM 트리는 쓰기 시 디스크에서 레코드를 찾을 필요가 없고 미래 쓰기를 위한 여분 공간도 예약하지
  않는다.** 그래도 중복 레코드 저장에서 오는 공간 오버헤드는 남는다. 기본 설정에서 읽기가 더 비싼데,
  완전한 결과를 반환하려면 여러 테이블에 접근해야 하기 때문이다 — 다만 이 장의 최적화들이 이 문제를
  누그러뜨린다 (7장, p.145).[^petrov2019]

## 이 모형이 담지 못하는 것

- 저자가 스스로 한계를 적는다. 원문 직인용 (7장, p.145):[^petrov2019]

> This cost model is not perfect, as it does not take into account other important
> metrics such as latency, access patterns, implementation complexity, maintenance
> overhead, and hardware-related specifics. Higher-level concepts important for
> distributed databases, such as consistency implications and replication overhead, are
> also not considered. However, this model can be used as a first approximation and a
> rule of thumb as it helps understand what the storage engine has to offer.

## 이어지는 페이지

- [LSM 컴팩션](../concepts/lsm-compaction.md) — 이 삼각형에서 어디를 깎을지 고르는 실제 손잡이
- [LSM 트리](../concepts/lsm-tree.md) — 쓰기 쪽으로 기운 구조
- [B-트리](../concepts/b-tree-structure.md) — 읽기 쪽으로 기운 구조
- [블룸 필터](../concepts/bloom-filter.md) — 읽기 증폭을 메모리로 사는 사례
- [저장 엔진의 분류](../concepts/storage-engine-classification.md) — 버퍼링·불변성·순서라는 앞선 세 변수

[^petrov2019]: Petrov 2019, 7장 "Log-Structured Storage"

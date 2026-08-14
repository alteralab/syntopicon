---
type: concept
title: 읽기·쓰기·공간 증폭
status: draft
description: 불변 저장이 치르는 세 가지 대가와 그것을 하나의 비용 모형으로 묶는 RUM 추측 — 둘을 줄이면 셋째가 나빠진다는 주장, B-트리와 LSM 트리를 그 자에 놓았을 때의 위치, 이 모형이 담지 못하는 것, 그리고 B-트리 변형들이 어느 증폭을 무엇으로 사는가
generated: { by: "claude-opus-5", at: "2026-08-14T09:00:00Z" }
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

## B-트리 변형들은 어느 증폭을 무엇으로 사는가

위의 "B-트리는 읽기에 최적화돼 있다"는 배치는 원래 설계를 놓은 것이다. 그 두 증폭을 겨냥한 변형
계열이 있고, 각각이 무엇을 지불하는지가 명시돼 있다.

- 결함부터 다시 세면 — **원래 B-트리 설계에는 회전 디스크에서는 잘 작동했을 수 있으나 SSD에서 쓸
  때 덜 효율적으로 만드는 결함이 여럿 있다. B-트리는 (페이지 재작성이 유발하는) 쓰기 증폭이 높고,
  미래 쓰기를 위해 노드에 공간을 예약해야 하므로 공간 오버헤드가 높다** (6장,
  p.127).[^petrov2019]
- 공간 증폭의 출처가 한 문장으로 더 정확히 적혀 있다 — **갱신을 가능하게 하려고 여분 공간을
  예약한다. 이는 요청된 데이터를 실어 나르는 유용한(useful) 바이트마다 빈 바이트와 페이지의
  나머지도 전송해야 함을 뜻한다** (6장, p.120).[^petrov2019]
- 쓰기 증폭을 사는 값은 메모리다 — **쓰기 증폭은 버퍼링을 씀으로써 줄일 수 있다. WiredTiger와
  LA-트리 같은 게으른 B-트리는 개별 노드나 노드 그룹에 인메모리 버퍼를 붙여, 메모리에서 페이지에
  대한 후속 갱신을 버퍼링함으로써 필요한 I/O 연산 수를 줄인다** (6장, p.127).[^petrov2019]
- 공간 증폭을 사는 값은 읽기다 — **공간 증폭을 줄이려고 FD-트리는 불변성을 쓴다. 데이터 레코드가
  불변 정렬 런(runs)에 저장되고 가변 B-트리의 크기가 제한된다** (6장, p.127).[^petrov2019]
  이는 LSM 계열이 치르는 것과 같은 값이다 — 완전한 결과를 얻으려면 여러 런을 조정해야 한다.
- 셋을 한꺼번에 겨냥한 쪽 — **Bw-트리도 불변성을 써서 공간 증폭을 푼다. B-트리 노드와 그에 대한
  갱신이 별도의 온디스크 위치에 저장되고 로그 구조화 스토어에 영속화된다. 원래 B-트리 설계에 비해
  쓰기 증폭이 줄어드는데, 단일 논리 노드에 속하는 내용을 조정하는 일이 비교적 드물기 때문이다.
  Bw-트리는 동시 접근으로부터 페이지를 보호하기 위한 래치를 요구하지 않는데, 논리 노드 사이의
  가상 포인터가 메모리에 저장되기 때문이다** (6장, p.127).[^petrov2019] 그 값은 매핑 테이블과
  델타 사슬 순회이며, RUM의 M(메모리 오버헤드)으로 옮겨 간 셈이다. #hypothesis 이 마지막
  귀속(어느 항으로 옮겨 갔는가)은 소스가 명시하지 않고 위 두 서술에서 읽어 낸 것이다.

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
- [B-트리 변형](../concepts/b-tree-variants.md) — 위 처방들이 실제로 어떻게 구현되는가
- [B-트리 배큠과 유지보수](../concepts/b-tree-vacuum-and-maintenance.md) — 페이지 재작성이
  쓰기 증폭을 만드는 현장

[^petrov2019]: Petrov 2019, 6장 "B-Tree Variants"·7장 "Log-Structured Storage"

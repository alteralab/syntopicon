---
type: concept
title: 읽기·쓰기·공간 증폭
description: 불변 저장이 치르는 세 가지 대가와 그것을 하나의 비용 모형으로 묶는 RUM 추측 — 둘을 줄이면 셋째가 나빠진다는 주장, 쓰기 증폭을 실제로 재는 나눗셈과 SSD 마모까지 걸리는 이유, B-트리와 LSM 트리를 그 자에 놓았을 때의 위치와 디스크 공간 사용의 실제 차이, 이 모형이 담지 못하는 것, 그리고 B-트리 변형들이 어느 증폭을 무엇으로 사는가
generated: { by: "claude-opus-5", at: "2026-08-14T23:00:00Z" }
sources:
  - { id: petrov2019, resource: /it/sources/petrov2019.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 읽기·쓰기·공간 증폭

- [컴팩션 전략이 고르는 것](#컴팩션-전략이-고르는-것)
- [세 가지 증폭](#세-가지-증폭)
- [쓰기 증폭을 실제로 재는 법](#쓰기-증폭을-실제로-재는-법)
- [RUM 추측](#rum-추측)
- [두 구조를 그 자에 놓으면](#두-구조를-그-자에-놓으면)
- [디스크 공간 사용의 실제 차이](#디스크-공간-사용의-실제-차이)
- [B-트리 변형들은 어느 증폭을 무엇으로 사는가](#b-트리-변형들은-어느-증폭을-무엇으로-사는가)
- [이 모형이 담지 못하는 것](#이-모형이-담지-못하는-것)
- [이어지는 페이지](#이어지는-페이지)

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

## 쓰기 증폭을 실제로 재는 법

petrov가 쓰기 증폭의 **출처**를 갈라 놓았다면, kleppmann은 그것을 **재는 나눗셈**을 준다.

- 왜 하나의 쓰기가 여럿이 되는가 — **어떤 종류의 저장 엔진에서든 애플리케이션의 쓰기 요청 하나가
  밑에 깔린 디스크의 여러 I/O 연산으로 바뀐다** (4장, p.130).[^kleppmann2026]
  - **LSM 트리에서는 값이 먼저 내구성을 위해 로그에 쓰이고, 멤테이블이 디스크에 쓰일 때 또 한 번,
    그리고 그 키-값 쌍이 컴팩션의 일부가 될 때마다 다시 쓰인다.** 값이 키보다 훨씬 크면 **값을
    키와 분리해 저장하고 키와 값 참조를 담은 SSTable에 대해서만 컴팩션을 수행함으로써 이 오버헤드를
    줄일 수 있다** (4장, pp.130–131).[^kleppmann2026]
  - **B-트리 색인은 모든 데이터 조각을 최소 두 번 써야 한다: 쓰기 전 로그에 한 번, 트리 페이지
    자체에 한 번. 게다가 페이지의 몇 바이트만 바뀌었더라도 크래시나 정전 후 B-트리를 올바르게
    복구할 수 있게 하려고 페이지 전체를 써 내는 것이 때때로 필요하다** (4장,
    p.131).[^kleppmann2026]
- 정의가 나눗셈으로 주어진다 — **어떤 워크로드에서 디스크에 쓰인 전체 바이트 수를, 색인 없이 추가
  전용 로그만 썼다면 써야 했을 바이트 수로 나누면 쓰기 증폭(write amplification)을 얻는다. (때로
  쓰기 증폭은 바이트가 아니라 I/O 연산으로 정의되기도 한다)** (4장, p.131).[^kleppmann2026]
- 그 값이 왜 중요한가 — **쓰기 중심 애플리케이션에서 병목은 데이터베이스가 디스크에 쓸 수 있는
  속도일 수 있다. 이 경우 쓰기 증폭이 높을수록 가용 디스크 대역폭 안에서 감당할 수 있는 초당 쓰기
  수가 적어진다** (4장, p.131).[^kleppmann2026]
- 어느 쪽이 낮은가에 대한 답이 조건부다 — **쓰기 증폭은 LSM 트리와 B-트리 둘 다에서 문제다. 어느
  쪽이 나은지는 키와 값의 길이, 기존 키를 덮어쓰는 빈도 대 새 키를 삽입하는 빈도 같은 여러 요인에
  달렸다. 전형적인 워크로드에서 LSM 트리는 쓰기 증폭이 더 낮은 경향이 있는데, 페이지 전체를 쓸
  필요가 없고 SSTable의 청크를 압축할 수 있기 때문이다. 이것이 LSM 저장 엔진을 쓰기 중심 워크로드에
  잘 맞게 만드는 또 하나의 요인이다** (4장, p.131).[^kleppmann2026]
  - petrov는 같은 논쟁을 두고 **두 구조를 직접 견주는 것이 잘못된 가정으로 이끌 수 있다**고
    경고했다(위 [세 가지 증폭](#세-가지-증폭)의 직인용). 두 서술은 모순이 아니다 — kleppmann도
    "여러 요인에 달렸다"를 앞세우고 **전형적 워크로드**로 조건을 좁힌 뒤에야 방향을 말한다.
- 처리량만의 문제가 아니다 — **처리량에 영향을 주는 것 말고도 쓰기 증폭은 SSD의 마모(wear)에도
  관련된다. 쓰기 증폭이 더 낮은 저장 엔진은 SSD를 덜 빨리 닳게 한다** (4장,
  p.131).[^kleppmann2026]
- 측정 방법에 대한 주의가 붙는다 — **저장 엔진의 쓰기 처리량을 잴 때는 쓰기 증폭의 효과가 분명해질
  만큼 충분히 오래 실험을 돌리는 것이 중요하다. 빈 LSM 트리에 쓸 때는 아직 컴팩션이 돌지 않으므로
  모든 디스크 대역폭이 새 쓰기에 쓸 수 있다. 데이터베이스가 자라면 새 쓰기는 컴팩션과 디스크
  대역폭을 나눠 써야 한다** (4장, pp.131–132).[^kleppmann2026]

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

## 디스크 공간 사용의 실제 차이

위의 "공간 오버헤드"가 실제로 어떻게 나타나는지를 kleppmann이 양쪽에 대해 각각 적는다.

- B-트리 쪽 — **B-트리는 시간이 지나며 단편화될 수 있다. 예컨대 많은 키가 삭제되면 데이터베이스
  파일이 더 이상 B-트리에 쓰이지 않는 페이지를 많이 담을 수 있다. B-트리에 이후 추가되는 것들이 그
  자유 페이지를 쓸 수 있지만, 그 페이지들이 파일 중간에 있어 운영체제에 쉽게 돌려줄 수 없으므로
  파일시스템에서 여전히 공간을 차지한다. 그래서 데이터베이스는 페이지를 더 나은 자리로 옮기는 배경
  프로세스가 필요한데, PostgreSQL의 배큠(vacuum) 프로세스가 그 예다** (4장,
  p.131).[^kleppmann2026]
- LSM 쪽 — **단편화는 LSM 트리에서 덜 문제인데, 컴팩션 프로세스가 어차피 주기적으로 데이터 파일을
  다시 쓰고 SSTable에는 쓰이지 않는 공간을 가진 페이지가 없기 때문이다. 게다가 키-값 쌍의 블록이
  SSTable에서 더 잘 압축될 수 있어 흔히 B-트리보다 디스크의 파일이 작아진다** (4장,
  pp.131–132).[^kleppmann2026]
- 다만 LSM에도 값이 있다 — **덮어써진 키와 값은 컴팩션에 의해 제거될 때까지 계속 공간을 소비하지만,
  레벨형 컴팩션을 쓰면 이 오버헤드가 꽤 낮다. 크기 단계별 컴팩션은 디스크 공간을 더 쓰며 특히
  컴팩션 중에 일시적으로 그렇다** (4장, p.132).[^kleppmann2026]
- 삭제를 정말 삭제하기가 어렵다 — **디스크에 데이터 사본이 여럿 있는 것은 어떤 데이터를 지우고 그것이
  정말 지워졌다고 확신해야 할 때(아마 데이터 보호 규제를 지키기 위해) 문제가 될 수 있다. 예컨대
  대부분의 LSM 저장 엔진에서 삭제된 레코드는 그 삭제를 나타내는 툼스톤이 모든 컴팩션 레벨을 통해
  전파될 때까지 상위 레벨에 여전히 존재할 수 있고 그것은 오래 걸릴 수 있다. 전문화된 저장 엔진 설계는
  삭제를 더 빠르게 전파할 수 있다** (4장, p.132).[^kleppmann2026]

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
- [B-트리와 LSM 트리 견주기](../concepts/comparing-b-trees-and-lsm-trees.md) — 같은 두 구조를
  증폭이 아니라 읽기 경로와 쓰기 패턴으로 견주는 자리
- [디스크 기반 저장의 제약](../concepts/disk-based-storage-constraints.md) — 쓰기 증폭이 SSD 마모로
  이어지는 그 물리

[^petrov2019]: Petrov 2019, 6장 "B-Tree Variants"·7장 "Log-Structured Storage"

[^kleppmann2026]: Kleppmann & Riccomini 2026, 4장 "Storage and Retrieval"

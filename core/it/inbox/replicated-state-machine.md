---
type: concept
title: 복제 상태 기계와 합의
description: 합의 알고리즘이 존재하는 이유 — 서버 여럿을 하나의 고신뢰 상태 기계처럼 보이게 하는 복제 로그 구조와, 실용 시스템이 합의 알고리즘에 요구하는 안전성·가용성·타이밍 비의존·지연 성질, 그리고 그 결정성 가정이 실제 데이터베이스에서 깨지는 세 경로
generated: { by: "claude-opus-5", at: "2026-08-11T02:00:00Z" }
status: draft
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 복제 상태 기계와 합의

- [합의가 푸는 문제](#합의가-푸는-문제)
- [복제 로그라는 구현](#복제-로그라는-구현)
- [실용 시스템이 요구하는 성질](#실용-시스템이-요구하는-성질)
- [결정성 가정이 실제로 깨지는 자리](#결정성-가정이-실제로-깨지는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **합의 알고리즘은 무엇을 위한 장치이고, 실용 시스템은 그것에 어떤 성질을
요구하는가.**

## 합의가 푸는 문제

- 합의(consensus) 알고리즘은 **기계 여럿이 일부 구성원의 장애를 견디면서 하나의 응집된
  집단으로 동작하게** 한다. 그래서 신뢰할 수 있는 대규모 소프트웨어 시스템을 짓는 데
  핵심 역할을 한다 (§1).[^ongaro2014-raft]
- 합의 알고리즘은 보통 **복제 상태 기계(replicated state machine)** 라는 맥락에서
  등장한다 — 서버 모음의 상태 기계들이 같은 상태의 동일한 사본을 계산하고, 일부 서버가
  내려가도 계속 동작한다 (§2).[^ongaro2014-raft]
- 복제 상태 기계는 분산 시스템의 여러 내결함성(fault tolerance) 문제를 푸는 데 쓰인다
  (§2):[^ongaro2014-raft]
  - GFS·HDFS·RAMCloud처럼 **클러스터 리더가 하나인 대규모 시스템**은, 리더 선출(leader
    election)을
    수행하고 리더 크래시를 견뎌야 하는 설정 정보를 보관하기 위해 별도의 복제 상태
    기계를 두는 것이 보통이다.
  - 복제 상태 기계의 예로 Chubby와 ZooKeeper가 있다.

## 복제 로그라는 구현

- 복제 상태 기계는 **복제 로그(replicated log)** 로 구현되는 것이 보통이다. 각 서버가
  명령의 계열을 담은 로그를 저장하고 자기 상태 기계가 그 명령을 순서대로 실행한다
  (§2, 그림 1).[^ongaro2014-raft]
- 각 로그가 같은 명령을 같은 순서로 담으므로 각 상태 기계는 같은 명령 계열을 처리하고,
  **상태 기계가 결정적(deterministic)이므로 같은 상태와 같은 출력 계열을 낸다**
  (§2).[^ongaro2014-raft]
- 복제 로그를 일관되게 유지하는 것이 합의 모듈(consensus module)의 일이다 (§2,
  그림 1):[^ongaro2014-raft]
  - 서버의 합의 모듈은 클라이언트에서 명령을 받아 자기 로그에 더한다.
  - 다른 서버의 합의 모듈과 통신해, **일부 서버가 실패하더라도 모든 로그가 결국 같은
    요청을 같은 순서로 담게** 한다.
  - 명령이 제대로 복제되면 각 서버의 상태 기계가 로그 순서대로 처리하고 출력을
    클라이언트에 돌려준다.
  - 그 결과 서버들은 **하나의 고신뢰 상태 기계처럼 보인다.**

## 실용 시스템이 요구하는 성질

- 실용 시스템의 합의 알고리즘은 보통 네 가지 성질을 갖는다. 그중 안전성과 타이밍
  비의존은 조건이 왜곡되기 쉬우므로 원문을 그대로 인용한다 (§2):[^ongaro2014-raft]

> They ensure *safety* (never returning an incorrect result) under all non-Byzantine
> conditions, including network delays, partitions, and packet loss, duplication, and
> reordering.

> They do not depend on timing to ensure the consistency of the logs: faulty clocks and
> extreme message delays can, at worst, cause availability problems.

- 가용성(available): **서버 과반이 동작하며 서로 그리고 클라이언트와 통신할 수 있는 한
  온전히 기능한다.** 서버 다섯 대의 전형적 클러스터는 어느 두 대의 장애든 견딘다.
  서버는 정지(stop)로 실패한다고 가정하며, 나중에 안정 저장소(stable storage)에 남은
  상태에서 복구해 클러스터에 다시 합류할 수 있다 (§2).[^ongaro2014-raft]
- 지연: 일반적인 경우 **클러스터 과반이 원격 프로시저 호출 한 라운드에 응답하는 즉시
  명령이 완료될 수 있다.** 느린 소수 서버가 시스템 전체 성능에 영향을 줄 필요가
  없다는 뜻이다 (§2).[^ongaro2014-raft]
- 여기서 "과반"은 알고리즘이 살아 있기 위한 조건이자 안전성의 근거이기도 하다 —
  Raft는 선출과 커밋 양쪽에 과반을 요구해 **두 과반이 반드시 한 서버 이상에서 겹친다는
  사실**을 안전성 논증의 축으로 삼는다 (§5.4.1, §5.4.3).[^ongaro2014-raft]

## 결정성 가정이 실제로 깨지는 자리

위 [복제 로그라는 구현](#복제-로그라는-구현)이 기대는 것은 **상태 기계가 결정적이라는
가정**이다 (§2).[^ongaro2014-raft] DDIA 2판 6장은 그 가정이 실제 데이터베이스에서 어떻게
깨지는지를 열거한다 — 같은 명제의 앞뒤를 두 소스가 나눠 맡는 자리다.

- DDIA는 **리더가 실행하는 모든 쓰기 문장(statement)을 로깅해 팔로워가 그대로 실행하게 하는
  복제 방식**을 다루며, **결정적 문장을 고정된 순서로 실행한다는 이 아이디어를 상태 기계
  복제(state machine replication)라 부른다** (6장, pp.206–207).[^kleppmann2026]
- 그 결정성이 깨지는 경로 셋 (6장, pp.206–207):[^kleppmann2026]
  - **비결정적 함수를 호출하는 문장** — 현재 시각을 얻는 `NOW`나 난수를 얻는 `RAND` 같은 것은
    **레플리카마다 다른 값을 만들기 쉽다.**
  - **자동증가 컬럼을 쓰거나 기존 데이터에 의존하는 문장** — **레플리카마다 정확히 같은 순서로
    실행돼야 하고, 그러지 않으면 효과가 달라진다.** 동시에 실행되는 트랜잭션이 여럿일 때 이는
    제약이 된다.
  - **부작용이 있는 문장**(트리거·저장 프로시저·사용자 정의 함수) — **부작용이 절대적으로
    결정적이지 않는 한 레플리카마다 다른 부작용이 일어난다.**
- 우회와 실제 채택 (6장, p.207):[^kleppmann2026]
  - **리더가 비결정적 함수 호출을 고정된 반환값으로 치환해 로깅하면 모든 팔로워가 같은 값을
    얻는다.**
  - **VoltDB는 문장 기반 복제를 쓰면서 트랜잭션이 결정적일 것을 요구해 안전하게 만든다.**
  - **그러나 결정성은 실무에서 보장하기 어려워 많은 데이터베이스가 다른 복제 방법을 선호한다.**
- 두 소스의 위치 차이가 여기서 분명해진다 — Raft 논문은 **결정성을 상태 기계에 요구되는 전제로
  두고 그 위에서 로그 일관성을 논증하고**, DDIA는 **그 전제를 실제 SQL 실행 엔진에 부과했을 때
  무엇이 무너지는지를 센다.** 어긋나는 주장이 아니라 같은 조건의 안쪽과 바깥쪽이다.

## 이어지는 페이지

- [복제 로그의 구현 방식](../concepts/replication-log-implementations.md) — 문장 기반·WAL
  배송·논리 로그 셋의 전문
- [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md) — 이 성질들을 실제로
  얻어내는 알고리즘의 첫 조각
- [Raft의 로그 복제와 로그 매칭](../concepts/raft-log-replication.md) — 위 그림 1의
  복제 로그가 실제로 일관되게 유지되는 기전
- [이해 가능성을 설계 목표로 삼기](../concepts/designing-for-understandability.md) —
  이 문제를 푸는 알고리즘이 왜 하나 더 필요했는가
- [Raft의 안전성과 선출 제약](../concepts/raft-safety.md) — 여기서 인용한 안전성 요구가
  다섯 성질로 형식화되는 자리
- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 여기서 예로 든 ZooKeeper가
  카프카에서 맡는 자리
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 애초에
  왜 기계를 여러 대 쓰는가

[^ongaro2014-raft]: Ongaro & Ousterhout 2014, "In Search of an Understandable Consensus Algorithm" (USENIX ATC '14)
[^kleppmann2026]: Kleppmann & Riccomini 2026, 6장 "Replication"

---
type: concept
status: draft
title: 복제 상태 기계와 합의
description: 합의 알고리즘이 존재하는 이유 — 서버 여럿을 하나의 고신뢰 상태 기계처럼 보이게 하는 복제 로그 구조와, 실용 시스템이 합의 알고리즘에 요구하는 안전성·가용성·타이밍 비의존·지연 성질
generated: { by: "claude-opus-5", at: "2026-08-11T02:00:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# 복제 상태 기계와 합의

하나의 질문: **합의 알고리즘은 무엇을 위한 장치이고, 실용 시스템은 그것에 어떤 성질을
요구하는가.**

## 합의가 푸는 문제

- 합의(consensus) 알고리즘은 **기계 여럿이 일부 구성원의 장애를 견디면서 하나의 응집된
  집단으로 동작하게** 한다. 그래서 신뢰할 수 있는 대규모 소프트웨어 시스템을 짓는 데
  핵심 역할을 한다 (§1).[^ongaro2014-raft]
- 합의 알고리즘은 보통 **복제 상태 기계(replicated state machine)** 라는 맥락에서
  등장한다 — 서버 모음의 상태 기계들이 같은 상태의 동일한 사본을 계산하고, 일부 서버가
  내려가도 계속 동작한다 (§2).[^ongaro2014-raft]
- 복제 상태 기계는 분산 시스템의 여러 내결함성 문제를 푸는 데 쓰인다
  (§2):[^ongaro2014-raft]
  - GFS·HDFS·RAMCloud처럼 **클러스터 리더가 하나인 대규모 시스템**은, 리더 선출을
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

## 이어지는 페이지

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

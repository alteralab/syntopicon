---
type: concept
status: draft
title: Raft의 안전성과 선출 제약
description: 리더 선출과 로그 복제만으로는 부족한 이유, 그림 3의 다섯 안전성 성질, 투표에 얹히는 최신성 제약, 지난 임기 항목을 복제본 수로 커밋하면 안 되는 이유, 그리고 Leader Completeness의 모순 논증과 형식 검증의 범위
generated: { by: "claude-opus-5", at: "2026-08-11T02:00:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---

# Raft의 안전성과 선출 제약

**목차**: [무엇이 아직 부족한가](#무엇이-아직-부족한가) · [다섯 성질](#다섯-성질) · [선출 제약](#선출-제약) · [최신성 비교 규칙](#최신성-비교-규칙) · [지난 임기 항목의 커밋](#지난-임기-항목의-커밋) · [안전성 논증](#안전성-논증) · [팔로워와 후보의 크래시](#팔로워와-후보의-크래시) · [형식 검증의 범위](#형식-검증의-범위) · [이어지는 페이지](#이어지는-페이지)

하나의 질문: **뽑힌 리더가 커밋된 항목을 전부 갖고 있음을 무엇이 보장하는가.**

## 무엇이 아직 부족한가

- [리더 선출](../concepts/raft-leader-election.md)과
  [로그 복제](../concepts/raft-log-replication.md)까지의 기전만으로는 **각 상태 기계가
  정확히 같은 명령을 같은 순서로 실행함을 보장하기에 충분하지 않다**
  (§5.4).[^ongaro2014-raft]
- 반례가 되는 시나리오: 리더가 로그 항목 여럿을 커밋하는 동안 어떤 팔로워가 불가용
  상태였다가, 그 팔로워가 리더로 선출돼 그 항목들을 새 항목으로 덮어쓴다. 그러면
  **서로 다른 상태 기계가 서로 다른 명령 계열을 실행하게 된다** (§5.4).[^ongaro2014-raft]
- 그래서 Raft는 **어느 서버가 리더로 선출될 수 있는지에 제약을 하나 더 얹어** 알고리즘을
  완성한다. 이 제약이 보장하는 것은 **어떤 임기의 리더든 이전 임기들에서 커밋된 항목을
  전부 갖고 있다**는 것이다 (§5.4).[^ongaro2014-raft]

## 다섯 성질

- Raft가 항상 참임을 보장하는 성질은 다섯이다. 형식적 진술이므로 원문을 직인용한다
  (그림 3):[^ongaro2014-raft]

> **Election Safety:** at most one leader can be elected in a given term. §5.2
>
> **Leader Append-Only:** a leader never overwrites or deletes entries in its log; it only
> appends new entries. §5.3
>
> **Log Matching:** if two logs contain an entry with the same index and term, then the
> logs are identical in all entries up through the given index. §5.3
>
> **Leader Completeness:** if a log entry is committed in a given term, then that entry
> will be present in the logs of the leaders for all higher-numbered terms. §5.4
>
> **State Machine Safety:** if a server has applied a log entry at a given index to its
> state machine, no other server will ever apply a different log entry for the same index.
> §5.4.3

- 한국어 해설과 성립 자리 (§5.2–§5.4.3):[^ongaro2014-raft]
  - **Election Safety** — 한 임기에 리더는 많아야 하나다. 각 서버가 한 임기에 많아야 한
    후보에게 투표하고 승리 조건이 과반이라는 데서 나온다
    ([리더 선출](../concepts/raft-leader-election.md)).
  - **Leader Append-Only** — 리더는 자기 로그를 덮거나 지우지 않고 덧붙이기만 한다.
    로그 항목이 리더에서 팔로워로만 흐른다는 뜻이다
    ([로그 복제](../concepts/raft-log-replication.md)).
  - **Log Matching** — 두 로그에 같은 인덱스·같은 임기의 항목이 있으면 그 인덱스까지
    두 로그는 동일하다. `AppendEntries`의 일치성 검사가 귀납적으로 지킨다.
  - **Leader Completeness** — 어떤 임기에 커밋된 항목은 그보다 큰 번호의 모든 임기
    리더의 로그에 존재한다. 아래 [선출 제약](#선출-제약)이 이것을 만든다.
  - **State Machine Safety** — 어떤 서버가 특정 인덱스의 로그 항목을 상태 기계에
    적용했다면, 다른 어떤 서버도 그 인덱스에 다른 항목을 적용하지 않는다. Leader
    Completeness에서 따라 나온다.
- 이 성질들이 최종 목표다 — **State Machine Safety가 Raft의 핵심 안전성 성질**이고,
  §5.4는 그것을 얻기 위해 §5.2의 선출 기전에 제약을 더하는 절이다
  (§5, §5.4).[^ongaro2014-raft]

## 선출 제약

- 리더 기반 합의 알고리즘이라면 어디서든 **리더는 결국 커밋된 로그 항목을 전부 저장하고
  있어야 한다** (§5.4.1).[^ongaro2014-raft]
- 다른 선택지: 뷰스탬프 복제(Viewstamped Replication) 같은 일부 알고리즘은 **커밋된 항목을
  처음부터 갖고 있지 않아도 리더가 될 수 있게** 하고, 빠진 항목을 식별해 새 리더에게
  전송하는 기전을 따로 둔다(선출 중이거나 직후에). 그 대가가 **상당한 추가 기전과
  복잡도**다 (§5.4.1).[^ongaro2014-raft]
- Raft의 선택은 더 단순한 쪽이다 — **이전 임기들에서 커밋된 모든 항목이 새 리더에게
  선출 시점부터 이미 존재함을 보장하고, 항목을 리더에게 옮기는 절차를 두지 않는다.**
  그래서 로그 항목이 한 방향으로만 흐르고 리더가 자기 로그의 기존 항목을 덮지 않는다
  (§5.4.1).[^ongaro2014-raft]
- 그것을 어떻게 얻는가 — **투표 과정을 이용한다.** 후보의 로그가 커밋된 항목을 전부 담고
  있지 않으면 선출에서 이기지 못하게 막는다 (§5.4.1):[^ongaro2014-raft]
  - 후보는 선출되려면 클러스터 과반과 접촉해야 하므로, **커밋된 항목은 그 과반 중 적어도
    한 서버에 반드시 존재한다.**
  - 후보의 로그가 그 과반의 어느 로그에도 뒤지지 않을 만큼 최신이면, 후보는 커밋된 항목을
    전부 갖고 있는 것이다.
  - `RequestVote` RPC가 이 제약을 구현한다 — RPC에 후보의 로그 정보가 담기고, **투표자는
    자기 로그가 후보의 것보다 더 최신이면 표를 거부한다.**

## 최신성 비교 규칙

- 두 로그 중 어느 쪽이 더 최신인지는 **마지막 항목의 인덱스와 임기**를 비교해 정한다.
  원문 직인용 (§5.4.1):[^ongaro2014-raft]

> If the logs have last entries with different terms, then the log with the later term is
> more up-to-date. If the logs end with the same term, then whichever log is longer is
> more up-to-date.

- 해설: **임기가 먼저이고 길이는 그다음**이다. 마지막 항목의 임기가 다르면 더 늦은 임기
  쪽이 최신이고, 임기가 같을 때만 더 긴 쪽이 최신이다. 길이만 비교하면 옛 임기에 항목을
  많이 쌓아 둔 뒤처진 서버가 이길 수 있으므로 순서가 중요하다
  (§5.4.1).[^ongaro2014-raft]

## 지난 임기 항목의 커밋

- [로그 복제](../concepts/raft-log-replication.md)의 커밋 규칙은 **현재 임기의 항목**에만
  그대로 적용된다 — 리더는 자기 임기의 항목이 서버 과반에 저장되면 커밋됐음을 안다
  (§5.3, §5.4.2).[^ongaro2014-raft]
- 그러나 **리더는 지난 임기의 항목이 과반에 저장됐다는 사실만으로 그것이 커밋됐다고
  결론지을 수 없다.** 옛 항목이 과반에 저장돼 있는데도 미래의 리더에게 덮어쓰일 수 있는
  상황이 존재한다 (§5.4.2, 그림 8).[^ongaro2014-raft]
- 그림 8이 보여 주는 흐름 (§5.4.2, 그림 8):[^ongaro2014-raft]
  - (a) S1이 리더이고 인덱스 2의 항목을 일부에만 복제한다.
  - (b) S1이 크래시하고, S5가 S3·S4와 자신의 표로 임기 3의 리더가 되어 인덱스 2에 다른
    항목을 받는다.
  - (c) S5가 크래시하고 S1이 재시작해 리더가 되어 복제를 계속한다. 이 시점에 임기 2의
    항목은 **과반에 복제돼 있지만 커밋된 것은 아니다.**
  - (d) 여기서 S1이 크래시하면 S5가 다시 리더가 되어(S2·S3·S4의 표로) 그 항목을 자기
    임기 3의 항목으로 덮어쓸 수 있다.
  - (e) 반대로 S1이 크래시 전에 **자기 현재 임기의 항목을 과반에 복제해** 두면 그 항목이
    커밋되고 S5는 선출에서 이길 수 없다. 이때는 로그의 모든 선행 항목도 함께 커밋된다.
- 그래서 Raft가 택한 규칙은 이렇다 — **지난 임기의 로그 항목은 복제본 수를 세어 커밋하지
  않는다.** 복제본 수로 커밋되는 것은 **리더의 현재 임기 항목뿐**이고, 그렇게 현재 임기
  항목 하나가 커밋되면 Log Matching 성질에 의해 **선행 항목이 전부 간접적으로 커밋된다**
  (§5.4.2).[^ongaro2014-raft]
- 더 공격적으로 갈 수 있는데도 그러지 않았다 — 옛 항목이 커밋됐다고 안전하게 결론지을 수
  있는 상황이 있지만(예: 그 항목이 모든 서버에 저장된 경우), **Raft는 단순함을 위해 더
  보수적인 접근을 택한다** (§5.4.2).[^ongaro2014-raft]
- 이 추가 복잡도의 출처는 항목의 임기 번호 처리 방식이다 — Raft에서는 리더가 지난 임기의
  항목을 복제해도 **항목이 원래 임기 번호를 유지한다.** 다른 합의 알고리즘은 새 리더가
  이전 "임기"의 항목을 다시 복제할 때 **새 임기 번호를 붙여야 한다**
  (§5.4.2).[^ongaro2014-raft]
- 그 대신 얻는 것 두 가지: 로그 항목이 시간이 지나도 로그를 가로질러도 같은 임기 번호를
  유지하므로 **추론하기 쉬워지고**, 새 리더가 지난 임기의 로그 항목을 **더 적게 보낸다**
  (다른 알고리즘은 번호를 다시 매기려고 중복 항목을 보내야 커밋할 수 있다)
  (§5.4.2).[^ongaro2014-raft]

## 안전성 논증

- Leader Completeness 성질은 **귀류법**으로 논증된다. 임기 T의 리더(leader_T)가 자기 임기의
  로그 항목을 커밋했는데 미래 어떤 임기의 리더가 그 항목을 저장하지 않았다고 가정하고,
  그런 임기 중 가장 작은 U(> T)의 리더를 leader_U라 둔다 (§5.4.3).[^ongaro2014-raft]
- 논증의 뼈대 (§5.4.3, 그림 9):[^ongaro2014-raft]
  - 커밋된 항목은 leader_U의 선출 시점에 그 로그에 없었다 — **리더는 항목을 지우거나
    덮지 않기 때문**이다.
  - leader_T는 항목을 클러스터 과반에 복제했고 leader_U는 과반에게 표를 받았다. 따라서
    **leader_T에게서 항목을 받고 leader_U에게 투표한 서버가 적어도 하나 있다.** 이 서버를
    "투표자"라 부르며, 여기가 모순에 이르는 열쇠다.
  - 투표자는 leader_U에게 투표하기 **전에** 그 항목을 받았어야 한다. 아니었다면 자기 현재
    임기가 T보다 높았을 것이므로 leader_T의 `AppendEntries`를 거부했을 것이다.
  - 투표자는 투표 시점에도 그 항목을 갖고 있었다 — 가정상 그 사이의 모든 리더가 항목을
    갖고 있었고, 리더는 항목을 제거하지 않으며, 팔로워는 리더와 충돌할 때만 항목을
    제거하기 때문이다.
  - 투표자가 표를 줬으므로 **leader_U의 로그는 투표자의 로그만큼 최신**이었다. 여기서
    모순 둘 중 하나가 나온다.
  - 마지막 로그 임기가 같았다면 leader_U의 로그는 적어도 투표자의 로그만큼 길어야 하므로
    투표자의 모든 항목을 담는데, 투표자는 문제의 커밋된 항목을 담고 있었으므로 모순이다.
  - 마지막 로그 임기가 달랐다면 leader_U 쪽이 더 커야 하고 T보다도 커야 한다. 그렇다면
    leader_U의 마지막 로그 항목을 만든 더 이른 리더가 가정상 그 커밋된 항목을 갖고
    있었고, **Log Matching 성질에 의해 leader_U의 로그도 그 항목을 담아야 하므로** 역시
    모순이다.
- 결론: **T보다 큰 모든 임기의 리더는 임기 T에 커밋된 항목을 전부 담아야 한다.** 간접적으로
  커밋된 항목까지 미래 리더가 담는다는 것은 Log Matching 성질이 보장한다
  (§5.4.3).[^ongaro2014-raft]
- Leader Completeness가 주어지면 **State Machine Safety를 증명하기 쉽고, 모든 상태 기계가
  같은 로그 항목을 같은 순서로 적용한다는 것도 따라 나온다** (§5.4.3).[^ongaro2014-raft]

## 팔로워와 후보의 크래시

- 팔로워와 후보의 크래시는 **리더 크래시보다 훨씬 단순하고 둘 다 같은 방식으로 처리된다**
  (§5.5).[^ongaro2014-raft]
- 처리 방식 (§5.5):[^ongaro2014-raft]
  - 크래시하면 그 서버로 가는 이후의 `RequestVote`·`AppendEntries` RPC가 실패한다. Raft는
    **무한히 재시도해서** 이 실패를 처리하고, 서버가 재시작하면 RPC가 성공한다.
  - RPC를 완료했지만 응답 전에 크래시한 서버는 재시작 후 **같은 RPC를 다시 받는다.**
  - 문제가 되지 않는 이유는 **Raft의 RPC가 멱등(idempotent)** 이기 때문이다. 예컨대
    팔로워가 이미 자기 로그에 있는 항목을 담은 `AppendEntries`를 받으면 새 요청의 그
    항목들을 무시한다.

## 형식 검증의 범위

- 저자들은 §5의 합의 기전에 대해 **형식 명세와 안전성 증명**을 만들었다 — TLA+ 명세는
  약 400줄이고, 그 자체로 Raft를 구현하려는 사람에게 유용하다
  (§8.2).[^ongaro2014-raft]
- 어디까지 기계적으로 검증됐는가 (§8.2):[^ongaro2014-raft]
  - **Log Completeness 성질은 TLA 증명 체계로 기계적으로 증명했다.**
  - 그러나 그 증명은 **기계적으로 검사되지 않은 불변식에 의존한다** — 예로 명세의 타입
    안전성은 증명하지 않았다.
  - State Machine Safety에 대해서는 **비형식 증명**을 따로 썼다. 명세만으로 완결적이고
    비교적 정밀하며(약 3,500단어) 별도 문헌에 있다.
- #hypothesis §8.2가 말하는 "Log Completeness Property"는 그림 3의 **Leader Completeness**
  와 같은 성질을 다른 이름으로 부른 것으로 보인다 — 논문 안에서 이 이름은 §8.2에만
  나오고, 그림 3의 다섯 이름에는 없다.

## 이어지는 페이지

- [Raft의 로그 복제와 로그 매칭](../concepts/raft-log-replication.md) — 여기서 제약을
  거는 그 커밋과 덮어쓰기의 본체
- [Raft의 리더 선출과 임기](../concepts/raft-leader-election.md) — 이 제약이 얹히는
  투표 절차
- [Raft의 클러스터 멤버십 변경](../concepts/raft-membership-change.md) — Leader
  Completeness가 구성 변경의 안전성 논증에도 쓰이는 자리
- [복제 상태 기계와 합의](../concepts/replicated-state-machine.md) — 안전성이라는 요구가
  처음 제시되는 자리
- [이해 가능성을 설계 목표로 삼기](../concepts/designing-for-understandability.md) —
  "더 보수적이지만 단순한 규칙"을 고르는 판단 기준

[^ongaro2014-raft]: Ongaro & Ousterhout 2014, "In Search of an Understandable Consensus Algorithm" (USENIX ATC '14)

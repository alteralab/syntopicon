---
type: concept
title: 꼬리 내성이라는 설계 태도
description: 지연 가변성을 없애는 대신 견디자는 입장 — 내결함성에서 빌려온 유비와 tail-tolerant라는 이름, 기법을 요청 안(수십 밀리초)과 요청 사이(수십 초에서 분)로 가르는 두 시간 척도, 상태를 바꾸는 연산이 오히려 다루기 쉬운 네 이유, 그리고 이 기법들의 대가가 왜 작다고 저자들이 보는가
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T00:00:00Z" }
sources:
  - { id: dean2013-tail-at-scale, resource: /it/sources/dean2013-tail-at-scale.md }
---

# 꼬리 내성이라는 설계 태도

- [없애는 대신 견딘다](#없애는-대신-견딘다)
- [두 시간 척도로 갈린 기법](#두-시간-척도로-갈린-기법)
- [상태를 바꾸는 연산은 왜 더 쉬운가](#상태를-바꾸는-연산은-왜-더-쉬운가)
- [대가는 얼마인가](#대가는-얼마인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **부품의 지연이 흔들리는 것을 전제로 두고 전체 서비스의 응답성을 지키려면 어떤
입장을 취해야 하는가.**

## 없애는 대신 견딘다

- 출발점은 응답성의 문턱이다. 저자들은 사용자 동작에 **100ms 안에** 응답하는 시스템이 그보다
  오래 걸리는 것보다 유연하고 자연스럽게 느껴진다고 적는다 (도입, p.74).[^dean2013-tail-at-scale]
- 상호작용형 서비스에서 지연 분포의 꼬리를 짧게 유지하는 일은 **시스템의 크기와 복잡도가 커지거나
  전체 사용량이 늘수록** 어려워진다. 중간 규모 시스템에서는 대수롭지 않던 일시적 고지연 사건이
  대규모에서는 서비스 전체 성능을 좌우하게 된다 (도입, p.74).[^dean2013-tail-at-scale]
- 이름은 내결함성(fault-tolerant)에서 유비로 빌려 왔다. 저자들의 정의는 이렇다
  (도입, p.74):[^dean2013-tail-at-scale]

  > Just as fault-tolerant computing aims to create a reliable whole out of less-reliable
  > parts, large online services need to create a predictably responsive whole out of
  > less-predictable parts; we refer to such systems as "latency tail-tolerant," or simply
  > "tail-tolerant."

  즉 **꼬리 내성(tail-tolerant)** 은 부품의 예측 불가능성을 없애 전체를 예측 가능하게 만드는
  것이 아니라, 덜 예측 가능한 부품 위에 예측 가능한 전체를 짓는 태도다.
- 왜 없애는 쪽을 포기하는가 — 현대 웹 서비스의 규모와 복잡도 때문에 지연 가변성을 전부 제거하는
  것은 **실행 가능하지 않고**, 설령 격리된 환경에서 그런 완벽한 동작이 달성된다 해도 계산 자원을
  공유하는 시스템은 **애플리케이션 개발자의 통제 밖에서** 성능이 요동친다. 그래서 구글은 일시적
  지연 병리를 없애려 하는 대신 그것을 가리거나 우회하는 꼬리 내성 기법을 개발하는 쪽이 유리하다고
  판단했다 (Living with Latency Variability, pp.76–77).[^dean2013-tail-at-scale]
  - 가변성을 **줄이는** 공학이 무의미하다는 말이 아니다. 저자들은 앞선 절의 세심한 공학이 고성능
    상호작용형 서비스를 짓는 데 필수라고 못 박는다. 그 내용은
    [부품의 가변성을 줄이는 공학](../concepts/reducing-component-variability.md)에 있다.
- 저자들이 결론에서 말하는 이 태도의 값 — 개별 지연 원인을 겨냥하는 접근도 쓸모 있지만, **가장
  강력한 꼬리 내성 기법은 근본 원인이 무엇이든 상관없이 지연 딸꾹질을 줄인다.** 그래서 설계자는
  흔한 경우를 계속 최적화하면서 드문 경우에 대한 회복력을 함께 갖는다
  (Conclusion, p.80).[^dean2013-tail-at-scale]

## 두 시간 척도로 갈린 기법

- 저자들은 꼬리 내성 기법을 두 부류로 가르는데, 가르는 축은 기법이 반응하는 **시간 척도**다
  (Living with Latency Variability, p.77):[^dean2013-tail-at-scale]

  > The first corresponds to within-request immediate-response techniques that operate at a
  > time scale of tens of milliseconds, before longer-term techniques have a chance to react.
  > The second consists of cross-request long-term adaptations that perform on a time scale of
  > tens of seconds to minutes and are meant to mask the effect of longer-term phenomena.

- 이 구분이 실제로 하는 일은 **무엇을 가릴 수 있는가**를 나누는 것이다. 요청 하나가 살아 있는
  수십 밀리초 안에 벌어지는 간섭은 그 요청 안에서 처리해야 하고(단기), 기계 성능 편차나 부하
  불균형처럼 수십 초에서 분 단위로 지속되는 현상은 요청을 가로질러 배치를 바꿔야 대응된다(장기).
  - 단기 쪽은 [요청 안에서의 단기 적응](../concepts/tail-tolerant-short-term-adaptations.md)에 있다.
  - 장기 쪽은 [요청 사이의 장기 적응](../concepts/tail-tolerant-long-term-adaptations.md)에 있다.
- 이 두 부류 밖에, 결과가 본래 부정확해도 되는 시스템에만 쓸 수 있는 기법이 따로 있다 —
  ["충분히 좋은" 결과와 카나리 요청](../concepts/good-enough-results-and-canary-requests.md).

## 상태를 바꾸는 연산은 왜 더 쉬운가

- 범위 표시가 명시적이다. 위 기법들은 **시스템 상태를 결정적으로 변경하지 않는 연산**에 가장 잘
  들어맞으며, 그것이 데이터 집약 서비스의 넓은 범위를 덮는다
  (Mutations, p.80).[^dean2013-tail-at-scale]
- 그렇다면 상태를 바꾸는 연산(mutation)은 어떻게 되는가 — 저자들은 오히려 **다소 더 쉽다**고 보고
  네 이유를 든다 (Mutations, p.80):[^dean2013-tail-at-scale]
  - 이런 서비스에서 **지연이 결정적인 변경의 규모 자체가 대체로 작다.**
  - 갱신은 흔히 **임계 경로 밖에서**, 사용자에게 응답한 뒤에 수행될 수 있다.
  - 많은 서비스가 (본래 지연에 더 관대한) 변경에 대해 **일관되지 않은 갱신 모델을 견디도록** 구성될
    수 있다.
  - 일관된 갱신이 필요한 서비스에서 가장 흔히 쓰이는 기법은 Paxos 같은 **정족수 기반
    알고리즘**인데, 이 알고리즘들이 세 개에서 다섯 개의 복제본에만 커밋하면 되므로 **본래부터 꼬리
    내성이 있다.**
    - 정족수가 왜 꼬리를 자르는지는 [Raft의 로그 복제](../concepts/raft-log-replication.md)와
      [분산 합의](../synthesis/distributed-consensus.md) 쪽 어휘와 이어진다 — 과반만 응답하면
      진행하므로 가장 느린 복제본을 기다리지 않는다.

## 대가는 얼마인가

- 자원 면의 대가 — 가장 강력한 꼬리 내성 기법 일부는 추가 자원을 요구하지만, 그 오버헤드는 **꽤
  작을 수 있다.** 흔히 **내결함성을 위해 이미 프로비저닝된 기존 용량에 기대면서** 상당한 지연 개선을
  낸다 (도입 p.74, Conclusion p.80).[^dean2013-tail-at-scale]
- 코드 면의 대가 — 이 기법 다수는 **기반 라이브러리와 시스템 안에 캡슐화될 수 있고**, 거기서 오는
  지연 개선이 오히려 애플리케이션 수준 설계를 급진적으로 단순하게 만들어 주는 일이 잦다
  (Conclusion, p.80).[^dean2013-tail-at-scale]
- 운영 면의 이득 — 저자들이 도입과 결론에서 같은 말을 두 번 한다. 이 기법들은 대규모에서 낮은
  지연을 가능하게 할 뿐 아니라 **서비스 응답성을 희생하지 않고 더 높은 시스템 활용률을 달성할 수
  있게** 하며, 그래서 낭비적인 과다 프로비저닝을 피하게 해 준다
  (도입 p.74, Conclusion p.80).[^dean2013-tail-at-scale]
  - 이 주장의 실물 하나가 묶인 요청 실측이다 — 큰 정렬 작업이 같이 도는 클러스터의 지연 분포를
    거의 유휴 클러스터 수준으로 되돌려 워크로드 통합을 가능하게 했다
    ([단기 적응](../concepts/tail-tolerant-short-term-adaptations.md)의 표 참조).
- 저자들이 결론에서 밝히는 이 논문의 지위 — 구글의 여러 대규모 소프트웨어 시스템에서 효과가 있었던
  꼬리 내성 기법의 **작은 모음**을 개괄한 것이며, 인터넷 서비스가 더 크고 복잡한 창고 규모
  (warehouse-scale) 시스템을 요구하고 하부 하드웨어 부품이 더 큰 성능 가변성을 보일수록 그 중요성이
  커지리라고 본다 (Conclusion, p.80).[^dean2013-tail-at-scale]

## 이어지는 페이지

- [지연 가변성이 생기는 자리](../concepts/latency-variability-sources.md) — 부품이 흔들리는 원인 목록
- [부품의 가변성을 줄이는 공학](../concepts/reducing-component-variability.md) — 견디기 전에 줄이는 쪽
- [요청 안에서의 단기 적응](../concepts/tail-tolerant-short-term-adaptations.md) — 헤지 요청과 묶인 요청
- [요청 사이의 장기 적응](../concepts/tail-tolerant-long-term-adaptations.md) — 마이크로 파티션·선택적
  복제·지연 유발 격리
- ["충분히 좋은" 결과와 카나리 요청](../concepts/good-enough-results-and-canary-requests.md) — 부정확한
  결과를 허용하는 시스템의 기법
- [지연의 백분위](../concepts/latency-percentiles.md) — 이 태도가 지키려는 그 지표
- [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md) — 유비를 빌려온 자리

[^dean2013-tail-at-scale]: Dean & Barroso 2013, "The Tail at Scale", CACM 56(2), pp.74–80.
    쪽수는 CACM 게재본 기준(PDF 스냅샷 1–7쪽 = pp.74–80).

---
type: concept
title: 응답 시간과 처리량
status: draft
description: 소프트웨어 성능을 재는 두 지표와 그 사이의 관계 — 부하가 용량에 가까워질수록 큐잉 때문에 응답 시간이 급격히 오르는 곡선, 응답 시간·서비스 시간·큐잉 지연·네트워크 지연을 갈라 쓰는 어휘, 같은 요청이 매번 다른 시간이 걸리는 이유, 그리고 느린 요청 몇 개가 뒤를 막는 선두 차단
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 응답 시간과 처리량

- [두 지표](#두-지표)
- [둘의 관계 — 큐잉](#둘의-관계--큐잉)
- [지연과 응답 시간은 같은 말이 아니다](#지연과-응답-시간은-같은-말이-아니다)
- [같은 요청이 매번 다른 시간이 걸린다](#같은-요청이-매번-다른-시간이-걸린다)
- [선두 차단과 측정 위치](#선두-차단과-측정-위치)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **소프트웨어의 성능을 무엇으로 재고, 그 지표들은 서로 어떻게 얽히는가.**

## 두 지표

- **소프트웨어 성능에 대한 논의 대부분은 두 종류의 지표를 고려한다.** 정의는 원문 직인용
  (2장, p.37):[^kleppmann2026]

> *Response time*
>     The elapsed time from the moment when a user makes a request until they receive the
>     requested answer. The unit of measurement is seconds (or milliseconds, or microseconds).
>
> *Throughput*
>     The number of requests per second, or the data volume per second, that the system is
>     processing. For a given allocation of hardware resources, there is a maximum throughput
>     that can be handled. The unit of measurement is "somethings per second."

- 사례로 구분하면 이렇다 — **"초당 글 수"와 "초당 타임라인 쓰기 수"는 처리량(throughput)
  지표이고, "홈 타임라인을 불러오는 데 걸리는 시간"과 "글이 팔로워에게 배달되기까지의
  시간"은 응답 시간(response time) 지표다** (2장, p.37).[^kleppmann2026] 그 사례의 전문은
  [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md)에 있다.
- 둘의 역할이 갈린다 — **성능 지표 면에서 사용자가 가장 신경 쓰는 것은 보통 응답 시간이고,
  처리량은 필요한 컴퓨팅 자원(예컨대 서버가 몇 대 필요한가)을 결정하며 따라서 특정 워크로드를
  제공하는 비용을 결정한다** (2장, p.38).[^kleppmann2026]
- 확장성의 정의가 여기서 나온다 — **처리량이 현재 하드웨어의 능력을 넘어 늘어날 것 같으면
  용량을 확장해야 한다. 컴퓨팅 자원을 더해 최대 처리량을 유의하게 늘릴 수 있으면 그 시스템을
  확장 가능(scalable)하다고 말한다** (2장, p.38).[^kleppmann2026] 그 확장의 방법은
  [확장성과 부하](../concepts/scalability-and-load.md)에 있다.

## 둘의 관계 — 큐잉

- **처리량과 응답 시간은 흔히 관계가 있다.** 온라인 서비스의 전형적 관계는 이렇다 —
  **요청 처리량이 낮을 때 서비스는 낮은 응답 시간을 갖지만, 부하가 오르면서 응답 시간이
  증가한다** (2장, p.37, 그림 2-3).[^kleppmann2026]
- 이유는 큐잉(queueing)이다 — **부하가 높은 시스템에 요청이 도착하면 CPU는 이미 앞선 요청을
  처리하는 중일 가능성이 높고, 따라서 들어오는 요청은 앞선 요청이 완료될 때까지 기다려야
  한다. 처리량이 하드웨어가 감당할 수 있는 최대치에 접근하면서 큐잉 지연이 급격히 증가한다**
  (2장, p.37).[^kleppmann2026]
- 한계 근처에서는 곡선이 아니라 악순환이 문제가 된다 — **시스템이 과부하에 가까워 처리량이
  한계에 밀착하면, 때때로 효율이 떨어지면서 더 과부하가 되는 악순환에 들어갈 수 있다** (2장,
  p.38).[^kleppmann2026] 그 현상의 이름(메타안정 장애)과 대처는
  [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md)의 연쇄 장애 절에
  있다.

## 지연과 응답 시간은 같은 말이 아니다

- **"지연(latency)"과 "응답 시간"은 때때로 서로 바꿔 쓰이지만, 이 책은 이 용어들과 몇 가지
  관련 용어를 특정한 방식으로 쓴다** (2장, pp.38–39, 그림 2-4):[^kleppmann2026]
  - **응답 시간(response time)은 클라이언트가 보는 것이다 — 시스템 어디에서 발생하든 모든
    지연을 포함한다.**
  - **서비스 시간(service time)은 서비스가 클라이언트의 요청을 실제로 처리하고 있는 기간이다.**
  - **큐잉 지연(queueing delay)은 흐름의 여러 지점에서 생길 수 있다** — 예컨대 **요청이 접수된
    뒤 처리되기 전에 CPU가 가용해질 때까지 기다려야 할 수 있고, 같은 기계의 다른 작업이 나가는
    네트워크 인터페이스로 데이터를 많이 보내고 있으면 응답 패킷이 네트워크로 나가기 전에
    버퍼링돼야 할 수도 있다.**
  - **지연(latency)은 요청이 실제로 처리되고 있지 않은 시간, 즉 잠복(latent)해 있는 시간을
    가리키는 포괄어다. 특히 네트워크 지연(network latency) 또는 네트워크 지체(network delay)는
    요청과 응답이 네트워크를 지나가는 데 쓰는 시간을 가리킨다.**
- 그림 관례도 여기서 정해진다 — **시간은 왼쪽에서 오른쪽으로 흐르고, 통신하는 각 노드는 수평선,
  요청이나 응답 메시지는 한 노드에서 다른 노드로 가는 굵은 대각선 화살표로 그린다. 이 양식의
  다이어그램은 이 책 전반에 자주 나온다** (2장, p.39).[^kleppmann2026]

## 같은 요청이 매번 다른 시간이 걸린다

- **응답 시간은 같은 요청을 계속 반복해도 요청마다 크게 달라질 수 있다** (2장,
  p.39).[^kleppmann2026]
- 무작위 지연을 더하는 요인이 많다 — **배경 프로세스로의 문맥 전환, 네트워크 패킷 유실과 TCP
  재전송, 가비지 컬렉션 일시 정지, 디스크에서 읽기를 강제하는 페이지 폴트, 서버 랙의 기계적
  진동** 등이다 (2장, p.39).[^kleppmann2026] 그래서 성능은 하나의 수가 아니라 분포로
  다뤄야 하고, 그 방법이
  [지연의 백분위](../concepts/latency-percentiles.md)에 있다.

## 선두 차단과 측정 위치

- **큐잉 지연은 응답 시간 변동의 큰 부분을 차지하는 일이 많다. 서버는 (예컨대 CPU 코어 수에
  제한되어) 병렬로 소수의 일만 처리할 수 있으므로, 느린 요청 몇 개만으로도 뒤이은 요청의
  처리를 붙들어 놓기에 충분하다. 이 효과를 선두 차단(head-of-line blocking)이라 한다** (2장,
  p.39).[^kleppmann2026]
- 그 결과가 측정 위치를 정한다 — **뒤이은 요청들의 서비스 시간이 빠르더라도, 앞선 요청이
  완료되기를 기다린 시간 때문에 클라이언트는 느린 전체 응답 시간을 보게 된다. 큐잉 지연은
  서비스 시간의 일부가 아니며, 이 때문에 응답 시간은 클라이언트 쪽에서 재는 것이 중요하다**
  (2장, p.39).[^kleppmann2026]

## 이어지는 페이지

- [지연의 백분위](../concepts/latency-percentiles.md) — 이 분포를 평균이 아니라 백분위로
  요약하는 이유와 방법
- [확장성과 부하](../concepts/scalability-and-load.md) — 처리량이 늘 때 자원을 어떻게 붙이는가
- [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md) — 이 두 지표가
  구체적 수로 나타난 자리
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — "지연이 0이다"라는
  가정과 과부하 악순환의 전문
- [서비스 수준 목표](../concepts/service-level-objectives.md) — 이 지표들을 약속으로 바꾸는 어휘
- [카프카 지표의 기초](../concepts/kafka-metrics-basics.md) — 응답 시간을 클라이언트 쪽에서
  재라는 권고가 제품 수준에서 반복되는 자리

[^kleppmann2026]: Kleppmann & Riccomini 2026, 2장 "Defining Nonfunctional Requirements"

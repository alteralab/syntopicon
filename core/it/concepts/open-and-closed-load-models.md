---
type: concept
title: 개방 부하 모델과 폐쇄 부하 모델
description: 부하를 거는 방식이 갈리는 세 가지 시스템 모델의 정의 — 요청 완료가 다음 요청을 낳는 폐쇄 모델의 사용자 수 N과 사고 시간, 요청 완료와 무관하게 도착하는 개방 모델의 도착률 λ, 둘 사이에서 세션으로 머무는 부분 개방 모델의 잔류 확률 p, 세 모델에서 서버 부하 ρ가 각각 무엇의 곱인가, 부하 생성기가 이 선택을 대개 밝히지 않는다는 실측, 그리고 개방 모델을 정의에 못 박은 실패 부류 하나
generated: { by: "claude-opus-5", at: "2026-09-07T02:00:00Z" }
sources:
  - { id: schroeder2006-open-vs-closed, resource: /it/sources/schroeder2006-open-vs-closed.md }
  - { id: bronson2021-metastable, resource: /it/sources/bronson2021-metastable.md }
---

# 개방 부하 모델과 폐쇄 부하 모델

- [무엇이 다음 요청을 낳는가](#무엇이-다음-요청을-낳는가)
- [폐쇄 시스템](#폐쇄-시스템)
- [개방 시스템](#개방-시스템)
- [어느 쪽도 그대로는 현실이 아니다](#어느-쪽도-그대로는-현실이-아니다)
- [부분 개방 시스템](#부분-개방-시스템)
- [부하 생성기는 이 선택을 대개 밝히지 않는다](#부하-생성기는-이-선택을-대개-밝히지-않는다)
- [개방 모델을 정의에 못 박은 실패 부류 하나](#개방-모델을-정의에-못-박은-실패-부류-하나)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **부하를 걸어 시스템을 잴 때, 다음 요청이 무엇에 의해 생기는가 — 그리고 그
차이가 무엇을 서로 다른 모델로 만드는가.**

이 구분은 2006년의 실험에 매인 것이 아니라 부하가 만들어지는 방식 자체의 분류다. 2026년의
부하 도구도 이 구분을 그대로 전제한다(k6의 도착률 실행기, Gatling의 개방/폐쇄 주입 모델).
이 문장은 소스 밖의 확인이며 이 페이지의 각주가 뒷받침하는 것이 아니다.

## 무엇이 다음 요청을 낳는가

- 저자들은 부하 생성기(workload generator)를 그것이 전제하는 시스템 모델로 두 갈래로 가른다.
  새 작업이 오직 앞 작업의 완료(그리고 뒤따르는 사고 시간)로만 생기면 폐쇄 모델이고, 완료와
  무관하게 도착하면 개방 모델이다 (Abstract, p.239).[^schroeder2006-open-vs-closed]

- 문제의식은 이 선택이 연구자의 시야 밖에 있다는 것이다 — **시스템 설계자는 부하 생성기가
  폐쇄인지 개방인지에 대체로 주의를 기울이지 않는다**(Abstract, p.239).[^schroeder2006-open-vs-closed]
  실제로는 **양쪽을 같은 부하(load)와 같은 서비스 요구량(service demand)으로 돌려도 결과가
  크게 달라진다**(§1, p.239).[^schroeder2006-open-vs-closed] 그 차이의 목록이
  [응답 시간을 가르는 세 원칙](../concepts/open-vs-closed-response-time-principles.md)과
  [스케줄링 효과가 부하 모델에 따라 갈리는 자리](../concepts/scheduling-under-open-and-closed-models.md)다.

## 폐쇄 시스템

- 폐쇄 시스템(closed system)에는 **시스템을 영원히 쓰는 고정된 수의 사용자가 있다고
  가정한다.** 그 수를 다중프로그래밍 수준(multiprogramming level, MPL)이라 부르고 N으로
  적는다. N명의 사용자는 두 단계를 무한히 되풀이한다 — (a) 작업을 제출하고, (b) 응답을 받은
  뒤 얼마간 "사고(think)"한다 (§2, p.241).[^schroeder2006-open-vs-closed]
- 이 모델을 규정하는 한 문장은 이것이다 (§2, p.241):[^schroeder2006-open-vs-closed]

> a new request is only triggered by the completion of a previous request

- 사용자는 언제나 두 무리로 나뉜다. 사고 중인 N_think 명과, 시스템 안에서 실행 중이거나
  큐에 든 N_system 명이며, 둘의 합이 N이다 (§2, p.241).[^schroeder2006-open-vs-closed]
- **응답 시간(response time) T는 요청을 제출한 때부터 응답을 받을 때까지의 시간**이다
  (§2, p.241).[^schroeder2006-open-vs-closed]
- 서버가 한 대일 때 **서버 부하(server load) ρ(로)는 서버가 바쁜 시간의 비율**이며,
  **평균 처리량 X와 평균 서비스 요구량 E[S]의 곱**이다 (§2, p.241).[^schroeder2006-open-vs-closed]

## 개방 시스템

- 개방 시스템(open system)에는 **평균 도착률 λ(람다)로 도착하는 사용자의 흐름이 있다.**
  사용자 하나가 작업 하나를 제출하고, 응답을 기다린 뒤, 떠난다고 가정한다. 시스템 안에 큐에
  들거나 실행 중인 사용자 수는 0에서 무한대까지 어느 값이든 될 수 있다 (§2,
  p.241).[^schroeder2006-open-vs-closed]
- 이 모델을 규정하는 한 문장은 이것이다 (§2, p.241):[^schroeder2006-open-vs-closed]

> a request completion does not trigger a new request: a new request is only triggered by a
> new user arrival

- 응답 시간 T의 정의는 폐쇄 쪽과 같고, **서버 부하 ρ는 평균 도착률 λ와 평균 서비스 요구량
  E[S]의 곱**이다 (§2, p.241).[^schroeder2006-open-vs-closed]
- 두 모델에서 고정되는 것이 서로 다르다는 점이 요점이다. 폐쇄 쪽은 사용자 수 N이 못 박히고,
  개방 쪽은 도착률 λ가 못 박힌다. 같은 관계식을 처리량 쪽에서 읽는 자리가
  [리틀의 법칙과 처리량](../concepts/littles-law-and-throughput.md)에 있다.

## 어느 쪽도 그대로는 현실이 아니다

- 저자들이 스스로 못을 박는다 — **개방 시스템 모델도 폐쇄 시스템 모델도 온전히 현실적이지
  않다** (§2, p.241).[^schroeder2006-open-vs-closed]
- 웹 사이트를 예로 든다. 한편으로 사용자는 한 사이트에 요청을 여러 번 하고 다음 요청을 하기
  전에 앞 요청의 결과를 기다리므로 그 점에서는 폐쇄 모델이 말이 된다. 다른 한편으로 사이트의
  사용자 수는 시간에 따라 변하며 고정된 N 같은 것은 없다. 요점은 **사용자가 사이트를
  방문해서 잠시 폐쇄 시스템처럼 행동하다가 떠난다**는 것이다 (§2,
  p.241).[^schroeder2006-open-vs-closed]

## 부분 개방 시스템

- 그 관찰에서 세 번째 모델이 나온다. 부분 개방 시스템(partly-open system)에서 사용자는 개방
  시스템에서처럼 바깥의 어떤 도착 과정을 따라 도착한다. 다만 요청 하나를 마칠 때마다 확률 p로
  남아서 (경우에 따라 사고 시간을 두고) 다음 요청을 하고, 확률 1 − p로 그냥 떠난다 (§2,
  p.242).[^schroeder2006-open-vs-closed]

- 따라서 **한 번의 방문에서 사용자가 하는 요청 수의 기댓값은 평균 1/(1 − p)의 기하 분포**를
  따른다 (§2, p.242).[^schroeder2006-open-vs-closed]
- 어휘가 여기서 정해진다 — **사용자가 한 번 방문하는 동안 하는 요청의 묶음을 세션(session)
  이라 부르고, 세션의 길이(length)를 그 세션에 든 요청의 개수로 정의한다** (§2,
  p.242).[^schroeder2006-open-vs-closed]
- **서버 부하는 바깥 평균 도착률 λ와 방문당 평균 요청 수 E[R]과 평균 서비스 요구량 E[S],
  이 셋의 곱**이다 (§2, p.242).[^schroeder2006-open-vs-closed]
- 이 모델이 양 끝을 품는다 — **주어진 부하에서 p가 작으면 부분 개방 모델은 개방 모델에 더
  가깝고, p가 크면 폐쇄 모델을 닮는다** (§2, p.242).[^schroeder2006-open-vs-closed] 그
  전이가 어디서 일어나는지는
  [부분 개방 모델과 세션 길이](../concepts/partly-open-model-and-session-length.md)가 잰다.

## 부하 생성기는 이 선택을 대개 밝히지 않는다

- 저자들이 당시 널리 쓰이던 웹 관련 부하 생성기와 벤치마크를 표 하나로 조사했다(Table 1,
  §1, p.241). 완전한 목록은 아니라고 스스로 밝히면서 결론을 셋 적는다
  (§1, p.239):[^schroeder2006-open-vs-closed]
  - **대다수는 폐쇄 시스템 모델을 가정하며, 상당수가 개방 모델을 가정한다.**
  - **많은 생성기에서 어느 모델을 가정했는지 알아내기가 상당히 어려웠다 — 만든 이들이 그것을
    문서에 적을 만큼 중요한 요인으로 보지 않는 듯하다.**
  - 그래서 **모델의 "선택"은 실은 연구자의 선택이 아니라 쓸 수 있는 부하 생성기가 무엇이냐에
    좌우된다.**
- 폐쇄를 의식적으로 고르더라도 문제가 남는다 — **사고 시간과 MPL을 어떻게 잡을지, 그
  매개변수가 어떤 효과를 낼지가 늘 분명하지는 않다** (§1, p.239).[^schroeder2006-open-vs-closed]
  그 답이 이 소스의 여덟 원칙이다.
- 저자들의 결론이 도구 제작자를 향한다 — 세 모델을 다 지원하는 **다재한(versatile) 부하
  생성기**를 설계하는 일이 중요하며, 이 작업이 다른 이들도 그렇게 하도록 북돋우기를 바란다고
  적는다 (§1, p.240 · §9, p.251).[^schroeder2006-open-vs-closed]

## 개방 모델을 정의에 못 박은 실패 부류 하나

이 구분이 부하 도구 설정을 넘어서는 자리가 하나 있다. 어떤 실패 부류는 정의 안에 개방
시스템을 조건으로 달고 있다.

- 메타안정 장애(metastable failure)의 정의는 이렇게 시작한다 — **메타안정 장애는 통제되지
  않는 부하원(uncontrolled source of load)을 가진 개방 시스템에서 일어나며, 트리거가 시스템을
  나쁜 상태로 들여보내고 그 상태는 트리거가 제거된 뒤에도 지속된다** (§1,
  p.221).[^bronson2021-metastable]
- 조건이 걸리는 이유는 위 [폐쇄 시스템](#폐쇄-시스템)의 규정 문장에 있다. 폐쇄 모델에서는
  새 요청이 앞 요청의 완료로만 생기므로, 시스템이 느려지면 도착도 함께 느려진다. 도착이
  완료와 무관한 개방 모델에서만 부하가 시스템의 상태와 독립적으로 계속 쌓일 수 있다.
- 그래서 부하 모델의 선택이 무엇을 볼 수 있는지를 정한다. 그 논문은 합성 작업 부하로 이런
  장애를 촉발하려 할 때 **부하 생성기가 조정 누락(coordinated omission)을 보여서는 안
  된다**고 못 박는다 (§4, p.226).[^bronson2021-metastable] 조정 누락은 시스템이 느려질 때
  부하 생성기가 요청을 함께 늦추는 것이며, 폐쇄 모델 부하 생성기가 구조적으로 그렇게 한다.
- 이 실패 부류의 전문은
  [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md)에 있다.

## 이어지는 페이지

- [응답 시간을 가르는 세 원칙](../concepts/open-vs-closed-response-time-principles.md) — 같은
  부하에서 두 모델의 응답 시간이 자릿수로 갈리는 이유와 그 수렴 속도
- [스케줄링 효과가 부하 모델에 따라 갈리는 자리](../concepts/scheduling-under-open-and-closed-models.md) —
  짧은 작업 우선이 개방에서는 듣고 폐쇄에서는 거의 듣지 않는 이유
- [부분 개방 모델과 세션 길이](../concepts/partly-open-model-and-session-length.md) — 세션당
  요청 수로 어느 모델이 맞는지 고르는 법
- [부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md) — 무엇을
  고정하고 무엇을 움직여 두 모델을 견주었는가
- [확장성과 부하](../concepts/scalability-and-load.md) — 부하를 초당 요청 수로 서술할 것인가
  동시 사용자 수로 서술할 것인가
- [리틀의 법칙과 처리량](../concepts/littles-law-and-throughput.md) — 처리량과 동시성과 응답
  시간을 잇는 관계식
- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 이 모델들이 재려는 그 지표
- [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md) — 정의에
  개방 시스템을 조건으로 단 실패 부류
- [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md) — 폐쇄 모델 부하
  생성기로는 볼 수 없는 것을 어떻게 재는가
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 페이지가 속한 허브

[^schroeder2006-open-vs-closed]: Schroeder, Wierman & Harchol-Balter 2006, "Open Versus
    Closed: A Cautionary Tale", NSDI '06, pp.239–252. Abstract와 §1 "Introduction"(pp.239–241),
    §2 "Closed, open, and partly-open systems"(pp.241–242), Table 1(p.241), §9
    "Conclusion"(p.251). 쪽수는 NSDI '06 논문집 게재본 기준이며 PDF 스냅샷 1–14쪽이
    pp.239–252에 해당한다. Figure 1의 세 모델 도해는 옮기지 않았다.
[^bronson2021-metastable]: Bronson, Aghayev, Charapko & Zhu 2021, "Metastable Failures in
    Distributed Systems", HotOS '21, pp.221–227. §1 "Introduction"(p.221),
    §4 "Discussion and Research Directions"(p.226). 쪽수는 ACM 게재본 인쇄 쪽 기준이며
    PDF 스냅샷 1–7쪽이 pp.221–227에 해당한다.

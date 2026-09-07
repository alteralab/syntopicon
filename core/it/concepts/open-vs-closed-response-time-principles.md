---
type: concept
title: 응답 시간을 가르는 세 원칙
description: 개방 모델과 폐쇄 모델의 평균 응답 시간이 갈리는 세 가지 원칙 — 같은 부하에서 폐쇄가 훨씬 빠른 이유가 큐 길이 상한이라는 것, MPL이 커지면 폐쇄가 개방에 수렴하되 실무 범위에서는 느리다는 것, 서비스 요구량의 변동성이 개방에서는 크게 듣고 폐쇄에서는 거의 안 듣는다는 것, 그리고 이 셋이 용량 계획에 주는 경고
generated: { by: "claude-opus-5", at: "2026-09-07T02:00:00Z" }
sources:
  - { id: schroeder2006-open-vs-closed, resource: /it/sources/schroeder2006-open-vs-closed.md }
---

# 응답 시간을 가르는 세 원칙

- [원칙 하나 같은 부하에서 폐쇄가 훨씬 빠르다](#원칙-하나-같은-부하에서-폐쇄가-훨씬-빠르다)
- [원칙 둘 MPL이 커지면 수렴하지만 느리다](#원칙-둘-mpl이-커지면-수렴하지만-느리다)
- [원칙 셋 변동성은 개방에서만 크게 듣는다](#원칙-셋-변동성은-개방에서만-크게-듣는다)
- [설계자에게 남는 경고](#설계자에게-남는-경고)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **부하를 개방으로 걸었을 때와 폐쇄로 걸었을 때 평균 응답 시간이 왜, 얼마나
달라지는가.**

여기 실린 세 원칙은 저자들이 번호를 매긴 여덟 원칙 중 앞의 셋이며, FCFS 스케줄링을 놓고
얻은 것이다. 모델의 정의는
[개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md)에, 실험이 무엇을
고정했는지는 [부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md)에
있다.

## 원칙 하나 같은 부하에서 폐쇄가 훨씬 빠르다

- 원칙 (i)의 원문은 이렇다 (§5.1, p.246):[^schroeder2006-open-vs-closed]

> For a given load, mean response times are significantly lower in closed systems than in open
> systems.

- 크기가 요점이다. **높은 부하를 고정해 놓고 보면 폐쇄 시스템의 응답 시간은 개방 시스템의
  응답 시간보다 자릿수가 낮다** (§5.1, p.247).[^schroeder2006-open-vs-closed] 사례 연구에서도
  같은 성질이 나왔다 — 정적 웹과 전자상거래 모두 두 모델의 응답 시간이 자릿수로 갈렸다
  (§4.1·§4.2, pp.244–245).[^schroeder2006-open-vs-closed]
- 이유는 구조에 있다. **폐쇄 시스템은 MPL N이 고정돼 있어서 아무리 부하가 높아도 큐 길이가
  N을 넘지 못한다. 개방 시스템에는 그런 상한이 없다** (§5.1,
  p.247).[^schroeder2006-open-vs-closed]
- 이론적 상계는 이미 알려져 있었다 — Schatte가 FCFS에서 개방 시스템의 응답 시간이 언제나
  폐쇄 시스템의 상계임을 증명했다. **다만 실무 조건에서 그 차이가 얼마나 큰지는 이 논문 전에
  연구된 적이 없다** (§5.1, p.247).[^schroeder2006-open-vs-closed]
  - 이 상계 관계는 FCFS에서만 성립한다. PESJF 같은 다른 정책에서는 개방 쪽이 더 낮은 응답
    시간을 낼 수도 있다 (§5.2, p.248).[^schroeder2006-open-vs-closed] 그 자리는
    [스케줄링 효과가 부하 모델에 따라 갈리는 자리](../concepts/scheduling-under-open-and-closed-models.md)에 있다.

## 원칙 둘 MPL이 커지면 수렴하지만 느리다

- 원칙 (ii)의 원문은 이렇다 (§5.1, p.247):[^schroeder2006-open-vs-closed]

> As the MPL grows, closed systems become open, but convergence is slow for practical purposes.

- 수렴 자체는 정리로 보장된다. Schatte가 **N이 무한대로 가면 폐쇄 FCFS 큐가 개방 M/GI/1/FCFS
  큐로 수렴함**을 형식적으로 증명했다 (§5.1, p.247).[^schroeder2006-open-vs-closed]
- 이 논문이 보탠 것은 그 수렴이 얼마나 느린가다. 저자들의 2006년 시뮬레이션에서 나온 두 수치가
  이렇다 (§5.1, p.247).[^schroeder2006-open-vs-closed]
  - 서비스 요구량의 변동성 C²가 높으면 **MPL이 1000인 폐쇄 시스템도 대응하는 개방 시스템보다
    응답 시간이 훨씬 낮다.**
  - 작업 서비스 요구량의 변동성이 가벼울 때조차 **폐쇄 시스템이 대응하는 개방 시스템에 견줄
    만한 응답 시간에 이르려면 MPL 500이 필요하다.**
  - 그리고 **모형 기반 시뮬레이션보다 사례 연구 쪽에서 차이가 더 극적이었다.**
- 그래서 흔한 어림이 무너진다 — **MPL이 높은 폐쇄 시스템을 개방 시스템으로 근사해도 되겠거니
  생각하기 쉬우나, 서비스 요구량의 변동성이 크면 두 모델은 여전히 유의하게 다르게 행동한다**
  (§5.1, p.247).[^schroeder2006-open-vs-closed]

## 원칙 셋 변동성은 개방에서만 크게 듣는다

- 원칙 (iii)의 원문은 이렇다 (§5.1, p.247):[^schroeder2006-open-vs-closed]

> While variability has a large effect in open systems, the effect is much smaller in closed
> systems.

- 개방 쪽의 기제는 익숙한 것이다 — **FCFS 아래서 높은 C²는 짧은 작업이 긴 작업 뒤에 갇히게
  만들고 그래서 평균 응답 시간을 올린다** (§5.1, p.247).[^schroeder2006-open-vs-closed]
- 폐쇄 쪽에서 그 효과가 작은 것은 직관에 어긋나지만 설명이 된다 — **MPL이 낮으면 시스템 안의
  작업 수 N_system이 묶여 있어서 긴 작업 뒤에 갇히는 짧은 작업이 애초에 더 적다. MPL을 올리면
  N_system이 커질 수 있으므로 C²의 효과도 커진다** (§5.1, p.247).[^schroeder2006-open-vs-closed]
- 사례 연구에서는 이 원칙이 트레이스별 변동성 차이로 드러났다. 각 트레이스의 C²가 고정이라
  직접 보이지는 않지만, **변동성이 낮은 전자상거래 결과와 변동성이 높은 나머지 결과의 격차
  크기를 견주면 확인된다** (§5.1, p.247).[^schroeder2006-open-vs-closed]
- 선행 연구도 같은 방향이다. Bondi와 Whitt가 FCFS 큐 망에서 서비스 변동성의 효과가 개방에서는
  지배적이지만 폐쇄에서는(MPL이 너무 크지 않다면) 거의 무의미하다는 결론을 냈고, 이 논문은
  그것을 확인하면서 **실제 시스템에서 그 영향의 크기를 보였다** (§8,
  p.251).[^schroeder2006-open-vs-closed]

## 설계자에게 남는 경고

- 세 원칙이 겨냥하는 첫 대상은 용량 계획(capacity planning)이다. 그 문헌은 **대체로 폐쇄
  모델에 기대고 있어서, 개방 모델이 더 적절한 경우에 필요한 자원을 과소평가할 수
  있다** (§5.1, p.247).[^schroeder2006-open-vs-closed]
- 결론에서 같은 경고를 한 문장으로 되풀이한다 — **개방 시스템의 용량 계획에서 폐쇄 모델 기반
  부하 생성기를 고르면 응답 시간을 크게 과소평가하고 스케줄링의 이득도 과소평가한다** (§9,
  p.251).[^schroeder2006-open-vs-closed]
- 일반화하면 이렇게 된다 — **한 시스템 모델에서 발견한 결과를 다른 시스템 모델에 그대로
  적용하는 것을 경계해야 한다** (§1, p.240).[^schroeder2006-open-vs-closed]

## 이어지는 페이지

- [개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md) — 세 모델의 정의
- [스케줄링 효과가 부하 모델에 따라 갈리는 자리](../concepts/scheduling-under-open-and-closed-models.md) —
  원칙 넷에서 여섯까지
- [부분 개방 모델과 세션 길이](../concepts/partly-open-model-and-session-length.md) — 원칙 일곱과 여덟
- [부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md) — 이
  수치들이 나온 실험의 조건
- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 큐잉이 응답 시간을 밀어
  올리는 곡선
- [지연의 백분위](../concepts/latency-percentiles.md) — 평균으로 재는 이 원칙들이 못 보는 꼬리
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 페이지가 속한 허브

[^schroeder2006-open-vs-closed]: Schroeder, Wierman & Harchol-Balter 2006, "Open Versus
    Closed: A Cautionary Tale", NSDI '06, pp.239–252. §1(p.240), §4.1·§4.2(pp.244–245),
    §5.1 "FCFS"(pp.246–247), §5.2(p.248), §8(p.251), §9(p.251). 쪽수는 NSDI '06 논문집
    게재본 기준이며 PDF 스냅샷 1–14쪽이 pp.239–252에 해당한다. Figure 5의 그래프는 옮기지
    않았고 본문이 호명한 MPL 500·1000만 실었다.

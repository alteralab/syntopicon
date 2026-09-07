---
type: concept
title: 스케줄링 효과가 부하 모델에 따라 갈리는 자리
description: 짧은 작업 우선 같은 스케줄링이 개방 모델에서는 자릿수의 이득을 주고 폐쇄 모델에서는 거의 듣지 않는 이유 — 사고 시간 없는 폐쇄 되먹임 고리에서 작업 보존 정책이 전부 동등해지는 리틀의 법칙 논증, 폐쇄에서 스케줄링이 통하는 좁은 구간, 스케줄링이 양쪽에서 변동성 효과를 눌러 준다는 원칙, 그리고 좋은 정책이 폐쇄 시스템의 부하 자체를 올려 버리는 미묘한 효과
generated: { by: "claude-opus-5", at: "2026-09-07T02:00:00Z" }
sources:
  - { id: schroeder2006-open-vs-closed, resource: /it/sources/schroeder2006-open-vs-closed.md }
---

# 스케줄링 효과가 부하 모델에 따라 갈리는 자리

- [원칙 넷 개방은 크게 얻고 폐쇄는 거의 못 얻는다](#원칙-넷-개방은-크게-얻고-폐쇄는-거의-못-얻는다)
- [왜 폐쇄에서는 안 듣는가](#왜-폐쇄에서는-안-듣는가)
- [원칙 다섯 폐쇄에서 통하는 좁은 구간](#원칙-다섯-폐쇄에서-통하는-좁은-구간)
- [원칙 여섯 스케줄링은 변동성의 효과를 누른다](#원칙-여섯-스케줄링은-변동성의-효과를-누른다)
- [좋은 정책이 부하 자체를 올린다](#좋은-정책이-부하-자체를-올린다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **자원을 더 사지 않고 평균 응답 시간을 줄이려는 스케줄링 정책의 값어치가, 부하를
개방으로 걸었느냐 폐쇄로 걸었느냐에 따라 왜 달라지는가.**

원칙 (iv)에서 (vi)까지가 여기 있다. 앞의 셋은
[응답 시간을 가르는 세 원칙](../concepts/open-vs-closed-response-time-principles.md)에, 견준
다섯 정책의 정의는
[부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md)에 있다.

## 원칙 넷 개방은 크게 얻고 폐쇄는 거의 못 얻는다

- 출발점은 개방 쪽의 이미 알려진 사실이다 — **개방 시스템에서 스케줄링의 값어치는 아무리
  강조해도 지나치지 않으며, 작은 작업이 큰 작업 뒤에 줄 서는 것을 막을 수 있기 때문에 정책들
  사이에 자릿수 차이가 난다. 반면 폐쇄 시스템의 스케줄링은 잘 이해돼 있지 않다** (§5.2,
  p.247).[^schroeder2006-open-vs-closed]
- 원칙 (iv)의 원문은 이렇다 (§5.2, pp.247–248):[^schroeder2006-open-vs-closed]

> While open systems benefit significantly from scheduling with respect to response time,
> closed systems improve much less.

- 저자들의 2006년 시뮬레이션이 보인 모양은 이렇다 (§5.2, p.248).[^schroeder2006-open-vs-closed]
  - 개방 시스템에서는 **부하가 오를수록 정책 사이의 응답 시간 격차가 커져 끝내 자릿수로
    갈린다.**
  - 폐쇄 시스템에서는 **높은 부하와 낮은 부하 모두에서 정책들이 비슷하게 동작한다. 중간
    부하에서만 유의한 차이가 나고, 그때조차 차이는 2.5배에 그친다.**
- 실측 사례도 같다. 정적 웹(LAN)에서 SRPT는 **폐쇄 시스템에서는 개선이 미미했고 개방
  시스템에서는 극적으로 개선했다** (§4.1, p.244).[^schroeder2006-open-vs-closed] 경매
  사이트에서는 **ρ > 0.7일 때 PSJF가 FCFS보다 10배 넘게 나았지만 폐쇄 시스템에서는 차이가
  거의 없었다** (§4.3, p.246).[^schroeder2006-open-vs-closed]
- 한 가지 관계가 여기서 깨진다 — FCFS에서는 개방 시스템의 평균 응답 시간이 대응하는 폐쇄
  시스템의 상계였지만, **PESJF 같은 다른 정책에서는 개방 쪽이 폐쇄 쪽보다 낮은 응답 시간을 낼
  수 있어 그 상계가 성립하지 않는다** (§5.2, p.248).[^schroeder2006-open-vs-closed]

## 왜 폐쇄에서는 안 듣는가

- 저자들이 직관을 얻는 방식은 **사고 시간이 0인 폐쇄 되먹임 고리**를 먼저 생각하는 것이다.
  그런 시스템에서는 놀랍게도 **큐에서 하는 스케줄링이 아무 소용이 없고 모든 작업 보존
  (work conserving) 정책이 동등하게 동작한다** (§5.2, p.248).[^schroeder2006-open-vs-closed]
- 논증은 리틀의 법칙(Little's Law)으로 두 줄이다 (§5.2, p.248).[^schroeder2006-open-vs-closed]
  - 폐쇄 시스템에서 법칙은 N = X·E[T]로 쓰인다. N은 정책과 무관하게 고정된 MPL이므로, 처리량
    X가 정책에 무관하게 일정하다면 평균 응답 시간 E[T]도 정책에 무관하게 일정해진다.
  - X가 일정한 이유는 폐쇄 모델의 정의 자체다. **새 작업은 작업이 완료될 때만 생기므로, 긴
    시간에 걸쳐 보면 모든 작업 보존 정책이 초기 집합 N을 빼거나 더한 만큼의 같은 작업 집합을
    완료한다. 시간이 무한대로 가면 초기 집합 N은 무의미해지고, 따라서 X는 일정하다.**
  - 이 논증은 개방 시스템에서는 성립하지 않는다. 개방 쪽의 리틀의 법칙은 E[N] = λ·E[T]인데
    **E[N]이 정책에 무관한 상수가 아니라 큐에 든 작업 수의 변동량이기 때문**이고, 그래서
    정책 사이에 차이가 생긴다.
- 사고 시간이 있는 폐쇄 시스템은 큐에 든 작업 수가 변할 수 있어 정책 사이에 어느 정도 차이가
  생긴다. 그러나 **사고 시간이 커지면 부하가 작아지고 그러면 스케줄링의 효과도 다시 줄어든다**
  (§5.2, p.248).[^schroeder2006-open-vs-closed] 같은 관계식을 처리량 쪽에서 읽는 자리가
  [리틀의 법칙과 처리량](../concepts/littles-law-and-throughput.md)에 있다.

## 원칙 다섯 폐쇄에서 통하는 좁은 구간

- 원칙 (v)의 원문은 이렇다 (§5.2, p.248):[^schroeder2006-open-vs-closed]

> Scheduling only significantly improves response time in closed systems under very specific
> parameter settings: moderate load (think times) and high MPL.

- 두 원칙의 실무 결론이 이렇게 정리된다 — **폐쇄 시스템에서 스케줄링은 모든 부하에서 작은
  개선을 주지만, 상당한 개선은 부하(사고 시간)가 중간일 때에만 얻어진다. 반면 개방 시스템에는
  스케줄링이 언제나 상당한 개선을 준다** (§5.2, p.248).[^schroeder2006-open-vs-closed]
- 결론에서 그 구간의 경계를 수로 적어 둔다 — **스케줄링은 개방 시스템에서 가장 효과적이고,
  폐쇄 시스템에서는 부하가 중간(대략 0.7에서 0.85)이면서 C²가 높을 때에 중간 정도의 효과를
  낼 수 있다** (§9, p.251).[^schroeder2006-open-vs-closed]
- 그래서 순서가 정해진다 — **어느 시스템 모델이 맞는지 아는 것이 스케줄링의 효과를 아는 데
  필수**이며, 모델이 정해져야 스케줄링의 값어치에 대한 지침이 따라 나온다 (§1, p.240 · §9,
  p.251).[^schroeder2006-open-vs-closed]

## 원칙 여섯 스케줄링은 변동성의 효과를 누른다

- 원칙 (vi)의 원문은 이렇다 (§5.2, p.248):[^schroeder2006-open-vs-closed]

> Scheduling can limit the effect of variability in both open and closed systems.

- 개방과 폐쇄 양쪽에서 **더 나은 스케줄링(PS와 PESJF)이 변동성 증가의 효과와 맞선다.** 다만
  **폐쇄 시스템에서는 그 개선 폭이 덜 극적인데, 원칙 (iii)이 말하듯 변동성 자체가 폐쇄
  시스템에는 애초에 효과가 작기 때문**이다 (§5.2, pp.248–249).[^schroeder2006-open-vs-closed]

## 좋은 정책이 부하 자체를 올린다

- 마지막으로 저자들이 미묘한 효과 하나를 밝혀 둔다 — **폐쇄 시스템에서는 스케줄링 정책이
  처리량에, 따라서 부하에 영향을 준다.** PESJF 같은 "좋은" 정책은 처리량을, 그리고 부하를
  조금 올린다. 그 폭은 10퍼센트 미만이다 (§5.2, p.248).[^schroeder2006-open-vs-closed]
- 이 효과를 실험이 일부러 지웠다. **부하를 고정하는 대신 이 효과를 그대로 두었더라면 폐쇄
  시스템의 정책들은 서로 더 가까워 보였을 것이고, 그러면 폐쇄와 개방의 차이는 지금보다 더
  뚜렷하게 나왔을 것이다** (§5.2, p.248).[^schroeder2006-open-vs-closed] 곧 이 논문이 보고한
  차이는 보수적인 쪽이다.

## 이어지는 페이지

- [응답 시간을 가르는 세 원칙](../concepts/open-vs-closed-response-time-principles.md) — 원칙
  하나에서 셋까지
- [부분 개방 모델과 세션 길이](../concepts/partly-open-model-and-session-length.md) — 세션이
  길어질수록 정책 사이의 격차가 사라지는 자리
- [개방 부하 모델과 폐쇄 부하 모델](../concepts/open-and-closed-load-models.md) — 세 모델의 정의
- [부하 모델을 공정히 비교하는 실험 설계](../concepts/load-model-experiment-design.md) — 다섯
  정책의 정의와 구현
- [리틀의 법칙과 처리량](../concepts/littles-law-and-throughput.md) — 이 절의 논증이 딛고 선 관계식
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 페이지가 속한 허브

[^schroeder2006-open-vs-closed]: Schroeder, Wierman & Harchol-Balter 2006, "Open Versus
    Closed: A Cautionary Tale", NSDI '06, pp.239–252. §1(p.240), §4.1(p.244), §4.3(p.246),
    §5.2 "The impact of scheduling"(pp.247–249), §9(p.251). 쪽수는 NSDI '06 논문집 게재본
    기준이며 PDF 스냅샷 1–14쪽이 pp.239–252에 해당한다. Figure 6·7의 그래프는 옮기지 않았고
    본문이 호명한 수치(2.5배, 10배, 10퍼센트 미만, 부하 0.7에서 0.85)만 실었다.

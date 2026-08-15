---
type: concept
title: 서비스 수준 목표
description: 카프카 같은 인프라 서비스가 클라이언트에게 약속하는 수준을 말하는 어휘 — SLI·SLO·SLA·OLA의 정의와 흔한 혼동, 좋은 지표가 갖춰야 할 객관성과 분위수 지표를 배제하는 이유, SLI 다섯 종류, SLO 자체로 경보를 걸 수 없어 소진율을 보는 방법, 그리고 같은 어휘를 백분위로 쓰는 다른 소스의 서술과 그 관계
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 서비스 수준 목표

- [왜 인프라 서비스에 특히 중요한가](#왜-인프라-서비스에-특히-중요한가)
- [네 낱말의 정의](#네-낱말의-정의)
- [무엇이 좋은 SLI인가](#무엇이-좋은-sli인가)
- [SLO로 경보를 거는 법](#slo로-경보를-거는-법)
- [같은 어휘를 백분위로 쓰는 서술](#같은-어휘를-백분위로-쓰는-서술)
- [장애의 정의가 SLO에 기대는 자리](#장애의-정의가-slo에-기대는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **서비스가 클라이언트에게 약속하는 수준을 어떤 어휘로 말하고, 그것으로
어떻게 경보를 거는가.**

## 왜 인프라 서비스에 특히 중요한가

- **카프카 같은 인프라 서비스에 특히 결정적인 모니터링 영역이 서비스 수준
  목표(service-level objectives, SLO)** 이며, **이것이 인프라 서비스가 제공할 수준을
  클라이언트에게 전달하는 방법**이다 (13장, p.343).[^shapira2021]
- 그 이유는 클라이언트가 원하는 것에 있다 — **클라이언트는 카프카 같은 서비스를 불투명한
  시스템으로 다루고 싶어 한다. 내부가 어떻게 동작하는지 이해하고 싶지도, 이해할 필요도
  없고, 자기가 쓰는 인터페이스와 그것이 필요한 일을 해 주리라는 것만 알면 된다** (13장,
  p.343).[^shapira2021]

## 네 낱말의 정의

- 논의 전에 어휘부터 맞춰야 하는 이유 — **엔지니어·관리자·경영진 할 것 없이 "서비스
  수준" 공간의 용어를 잘못 쓰는 일이 잦고, 그 결과 무엇을 이야기하고 있는지 혼란이
  생긴다** (13장, p.343).[^shapira2021]
- **서비스 수준 지표(service-level indicator, SLI)** (13장, p.343):[^shapira2021]

  > A service-level indicator (SLI) is a metric that describes one aspect of a service's
  > reliability. It should be closely aligned with your client's experience, so it is
  > usually true that the more objective these measurements are, the better they are.

  - 카프카처럼 **요청을 처리하는 시스템에서는 좋은 이벤트 수와 전체 이벤트 수의 비율로
    표현하는 것이 보통 가장 낫다** — 예로 드는 것이 **웹 서버 요청 중 2xx·3xx·4xx 응답을
    돌려준 비율**이다 (13장, p.343).[^shapira2021]
- **서비스 수준 목표(service-level objective, SLO)**, 다른 이름으로 **서비스 수준
  문턱(service-level threshold, SLT)** (13장, p.343):[^shapira2021]

  > A service-level objective (SLO), which can also be called a service-level threshold
  > (SLT), combines an SLI with a target value. A common way to express the target is by
  > the number of nines (99.9% is "three nines"), though it is by no means required. The
  > SLO should also include a time frame that it is measured over, frequently on the scale
  > of days.

  - 완성된 예시 문장은 이렇다 — **"7일에 걸쳐 웹 서버 요청의 99%가 2xx·3xx·4xx 응답을
    돌려주어야 한다"** (13장, p.344).[^shapira2021]
- **서비스 수준 협약(service-level agreement, SLA)** (13장, p.344):[^shapira2021]

  > A service-level agreement (SLA) is a contract between a service provider and a client.
  > It usually includes several SLOs, as well as details about how they are measured and
  > reported, how the client seeks support from the service provider, and penalties that
  > the service provider will be subject to if they are not performing within the SLA.

  - 위 SLO에 붙는 SLA의 예 — **제공자가 SLO 안에서 운영하지 못하면 서비스가 SLO를 벗어난
    기간에 대해 클라이언트가 낸 요금 전액을 환불한다** (13장, p.344).[^shapira2021]
- **운영 수준 협약(operational-level agreement, OLA)** 은 덜 쓰이는 용어다 — **SLA 전체를
  이행하는 데 관여하는 여러 내부 서비스나 지원 제공자 사이의 합의를 서술**하며, **목적은
  SLA 이행에 필요한 여러 활동이 일상 운영에서 제대로 서술되고 계산에 들어가도록 보장하는
  것**이다 (13장, p.344).[^shapira2021]
- 실무에서 벌어지는 혼동과 그 함의 (13장, p.344):[^shapira2021]
  - **SLO를 뜻하면서 SLA라고 말하는 것을 아주 흔히 듣는다.** 돈 내는 클라이언트에게 서비스를
    파는 쪽은 SLA를 가질 수 있지만, **애플리케이션을 운영하는 엔지니어가 SLO 안에서의 서비스
    성능 말고 다른 것을 책임지는 일은 드물다.**
  - **내부 클라이언트만 있는 쪽(더 큰 서비스의 내부 데이터 인프라로 카프카를 돌리는 경우)은
    대개 그 내부 고객과 SLA를 맺지 않는다.**
  - 그렇다고 SLO를 안 정할 이유는 없다 — **SLO를 정하고 알리는 것은 카프카가 어떻게
    동작해야 한다는 고객의 가정을 줄여 준다.**

## 무엇이 좋은 SLI인가

- **일반적으로 SLI로 쓸 지표는 카프카 브로커 바깥의 무언가로 수집해야 한다.** 이유는
  **SLO가 서비스의 전형적 사용자가 만족하는지를 서술해야 하는데 그것은 주관적으로 잴 수
  없기 때문**이다 — **클라이언트는 내가 서비스가 잘 돌고 있다고 생각하는지에 관심이 없고,
  중요한 것은 (총체로서의) 그들의 경험**이다 (13장, p.344).[^shapira2021]
- 그래서 출처에 등급이 매겨진다 — **인프라 지표는 괜찮고, 합성 클라이언트는 좋고,
  클라이언트 측 지표가 대부분의 SLI에 아마 가장 좋다** (13장, p.344).[^shapira2021]
  그 다섯 출처가 어떻게 갈리는지는
  [카프카 지표의 기초](../concepts/kafka-metrics-basics.md)에 있다.
- 요청·응답 시스템과 데이터 저장 시스템에서 흔히 쓰이는 SLI 종류 (13장, p.344, 표
  13-2):[^shapira2021]

  | 종류 | 무엇을 묻는가 |
  |---|---|
  | Availability | 클라이언트가 요청을 보내고 응답을 받을 수 있는가 |
  | Latency | 응답이 얼마나 빨리 돌아오는가 |
  | Quality | 응답에 제대로 된 응답이 들어 있는가 |
  | Security | 인가든 암호화든, 요청과 응답이 적절히 보호되는가 |
  | Throughput | 클라이언트가 충분한 데이터를 충분히 빠르게 얻을 수 있는가 |

  이 목록은 전수가 아니다 — 책 스스로 **"by no means an exhaustive list"** 라고 단다
  (13장, p.344).[^shapira2021]
- 지표의 형태에도 선호가 있다 — **SLI는 SLO의 문턱 안에 드는 이벤트를 세는 카운터에
  기반하는 편이 보통 낫다.** 이상적으로는 **이벤트 하나하나가 SLO 문턱을 만족하는지 개별로
  확인되는 것**이다 (13장, p.345).[^shapira2021]
  - **이것이 분위수(quantile) 지표를 좋은 SLI에서 배제한다** — **분위수는 이벤트의 90%가
    어떤 값 아래였다는 것만 알려 줄 뿐 그 값을 내가 통제하게 해 주지 않기 때문**이다 (13장,
    p.345).[^shapira2021]
  - 다만 **값을 구간(bucket)으로 묶는 것(예: "10ms 미만", "10–50ms", "50–100ms")은 SLO를
    다룰 때 유용할 수 있고, 좋은 문턱이 무엇인지 아직 모를 때 특히 그렇다.** SLO 범위 안에서
    이벤트가 어떻게 분포하는지 보여 주므로 **경계를 SLO 문턱으로 합리적인 값에 맞춰 구간을
    설정할 수 있다** (13장, p.345).[^shapira2021]
- 고객이 원한다고 다 받으면 안 되는 것도 있다 — **고객에게 중요하지만 내 통제 밖인 SLO가
  있다.** 예로 **카프카에 생산되는 데이터의 정확성이나 신선도**를 든다. **책임지지 않는
  SLO를 지원하기로 합의하지 마라 — 카프카를 제대로 돌린다는 본업을 희석하는 일을 떠안게
  될 뿐**이며, **적절한 그룹과 연결해 그 추가 요구에 대한 이해와 합의를 세우게 하라** (13장,
  p.345).[^shapira2021]

## SLO로 경보를 거는 법

- 결론부터 — **SLO가 주 경보를 결정해야 한다.** 이유는 **SLO가 고객의 관점에서 문제를
  서술하고 그것이 가장 먼저 신경 써야 할 문제이기 때문**이며, **일반적으로 클라이언트에
  영향을 주지 않는 문제라면 밤에 깨울 필요가 없다** (13장, p.345).[^shapira2021]
- SLO가 하는 또 하나의 일 — **한 번도 본 적이 없어서 탐지할 줄 모르는 문제까지 알려 준다.
  그것이 무엇인지는 알려 주지 못하지만 존재한다는 것은 알려 준다** (13장,
  p.345).[^shapira2021]
- 그런데 **SLO를 직접 경보로 쓰는 것은 매우 어렵다** (13장, p.346):[^shapira2021]
  - **SLO는 일주일처럼 긴 시간 척도에 가장 맞는다** — **경영진과 고객에게 소화할 수 있는
    형태로 보고하고 싶기 때문**이다.
  - **게다가 SLO 경보가 울릴 때쯤이면 이미 늦었다 — 이미 SLO를 벗어나 운영하고 있는
    것**이다.
  - **일부는 파생값을 조기 경보로 쓰지만, 가장 좋은 접근은 SLO를 그 기간에 걸쳐 얼마나 빠른
    속도로 태워 없애고 있는지를 관찰하는 것**이다. 그 값이 **소진율(burn rate)** 이다.
- 책이 드는 수치 예 (13장, p.346):[^shapira2021]
  - 전제 — **클러스터가 주당 100만 요청을 받고, "요청의 99.9%가 응답 첫 바이트를 10ms 안에
    내보내야 한다"는 SLO가 있다.** 즉 **한 주에 이보다 느린 요청이 1,000건까지는 괜찮다.**
  - 평상시 — **그런 요청이 시간당 한 건씩 나오며, 일요일부터 토요일까지 재면 주당 약 168건의
    나쁜 요청**이다. **주당 100만 요청에서 시간당 한 건이면 소진율은 시간당 0.1%** 다.
  - 화요일 오전 10시 — **소진율이 시간당 0.4%로 바뀐다. 좋지는 않지만 문제도 아니다. 주말까지
    SLO 안에 넉넉히 들어오기 때문**이다. **티켓을 열어 두고 더 급한 일로 돌아간다.**
  - 수요일 오후 2시 — **소진율이 시간당 2%로 뛰고 경보가 울린다. 이 속도면 금요일 점심때
    SLO를 위반한다는 것을 안다.** 하던 일을 놓고 진단해 **약 4시간 만에 소진율을 시간당
    0.4%로 되돌리고 남은 주 동안 그대로 유지된다.**
  - **소진율을 씀으로써 그 주의 SLO 위반을 피할 수 있었다.**
- 책이 가리키는 더 읽을거리는 **벳시 베이어(Betsy Beyer) 등이 엮은 『Site Reliability
  Engineering』과 『The Site Reliability Workbook』(O'Reilly)** 이다 (13장,
  p.346).[^shapira2021]

## 같은 어휘를 백분위로 쓰는 서술

다른 소스가 같은 두 낱말을 정의하는데, 정의는 위와 어긋나지 않고 **지표의 형태**에 대한 처방만
갈린다.

- 정의 — **백분위는 서비스의 기대 성능과 가용성을 정의하는 방법으로 서비스 수준 목표(service
  level objectives, SLO)와 서비스 수준 협약(service level agreements, SLA)에 자주 쓰인다.
  예컨대 SLO는 서비스가 200ms 미만의 중앙값 응답 시간과 1초 미만의 99번째 백분위를 갖는다는
  목표, 그리고 유효한 요청의 최소 99.9%가 오류가 아닌 응답을 낸다는 목표를 세울 수 있다. SLA는
  SLO가 충족되지 않으면 무슨 일이 일어나는지를 특정하는 계약이다(예: 고객이 환불을 받을 자격이
  생긴다)** (2장, p.42).[^kleppmann2026]
- 그리고 같은 문단이 이 일이 쉽지 않다고 덧붙인다 — **적어도 기본 발상은 그렇고, 실무에서 SLO와
  SLA를 위한 좋은 가용성 지표를 정의하는 일은 단순하지 않다** (2장, p.42).[^kleppmann2026]
- 위 [무엇이 좋은 SLI인가](#무엇이-좋은-sli인가)는 **분위수 지표를 좋은 SLI에서 배제**하는데,
  그 근거는 **분위수가 이벤트의 90%가 어떤 값 아래였다는 것만 알려 줄 뿐 그 값을 통제하게 해
  주지 않는다**는 것이었다 (13장, p.345).[^shapira2021] 두 서술은 사실 수준에서 충돌하지 않는다
  — Kleppmann은 **목표를 표현하는 형식**으로 백분위가 널리 쓰인다는 관찰을 적고, Shapira는
  **경보를 계산할 지표**로는 카운터가 낫다는 처방을 적는다. 겹치는 구간(백분위로 목표를 적을 수
  있는가)에서는 둘 다 같은 답을 준다. 그래서 `contradicts`를 달지 않는다(PLAN §2.1).
- 백분위를 실제로 계산할 때의 함정도 같은 소스가 적어 둔다 — **백분위를 평균 내는 것(시간
  해상도를 낮추거나 여러 기계의 데이터를 결합하기 위해)은 수학적으로 무의미하다. 응답 시간
  데이터를 집계하는 올바른 방법은 히스토그램을 더하는 것이다** (2장, p.42).[^kleppmann2026]
  전문은 [지연의 백분위](../concepts/latency-percentiles.md)에 있다.

## 장애의 정의가 SLO에 기대는 자리

- SLO는 모니터링만의 어휘가 아니다 — **장애(failure)는 시스템 전체가 사용자에게 요구되는 서비스
  제공을 멈출 때 일어난다. 다시 말해 그것이 SLO를 충족하지 못할 때다** (2장,
  p.43).[^kleppmann2026] 즉 **무엇이 결함이고 무엇이 장애인지의 경계 자체가 SLO를 어떻게
  적었는지에 달려 있다.** 그 구분의 전문은
  [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md)에 있다.

## 이어지는 페이지

- [지연의 백분위](../concepts/latency-percentiles.md) — 백분위로 목표를 적을 때의 어휘와 계산
- [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md) — SLO가 장애의 정의를
  떠받치는 자리
- [카프카 지표의 기초](../concepts/kafka-metrics-basics.md) — SLI로 쓸 지표를 어디서
  얻는지, 그리고 왜 객관성이 출처에 따라 갈리는지
- [카프카 클러스터 문제 진단](../concepts/kafka-cluster-problem-diagnosis.md) — SLO 경보가
  "문제가 있다"고만 말했을 때 그다음에 하는 일
- [카프카 컨슈머 랙과 종단 간 모니터링](../concepts/kafka-consumer-lag-monitoring.md) —
  브로커 바깥에서 재는 객관적 지표의 실물 두 가지
- [카프카 브로커 지표](../concepts/kafka-broker-metrics.md) — 여기서 분위수 지표를
  SLI에서 배제한 그 백분위수들이 실제로 나오는 자리

[^kleppmann2026]: Kleppmann & Riccomini 2026, 2장 "Defining Nonfunctional Requirements"
[^shapira2021]: Shapira et al. 2021, 13장 "Monitoring Kafka" §"Service-Level Objectives"(pp.343–346) — 인용 블록은 pp.343–344 정의 문단 원문

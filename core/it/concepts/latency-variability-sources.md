---
type: concept
title: 지연 가변성이 생기는 자리
description: 부품 하나의 응답 시간이 흔들리는 원인들 — 공유 자원 경합, 배경 데몬, 전역 자원 공유, 유지보수 활동, 여러 층의 큐잉, 그리고 전력 한계와 SSD 가비지 컬렉션과 절전 모드처럼 하드웨어에서 오는 것들, 더불어 저자들이 2013년 시점에 내다본 하드웨어 추세의 양면
generated: { by: "claude-opus-5", at: "2026-09-07T00:00:00Z" }
sources:
  - { id: dean2013-tail-at-scale, resource: /it/sources/dean2013-tail-at-scale.md }
---

# 지연 가변성이 생기는 자리

- [소프트웨어 쪽 다섯 자리](#소프트웨어-쪽-다섯-자리)
- [하드웨어 추세가 더하는 셋](#하드웨어-추세가-더하는-셋)
- [저자들이 2013년에 내다본 앞날](#저자들이-2013년에-내다본-앞날)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **서비스의 부품 하나가 어떨 때는 빠르고 어떨 때는 느린 이유가 무엇인가.**

높은 꼬리 지연으로 이어지는 응답 시간의 가변성은 한 가지 원인에서 오지 않는다. 저자들은 원인을
소프트웨어 쪽과 하드웨어 추세 쪽으로 나누어 나열한다 (Why Variability Exists?, pp.74,
76).[^dean2013-tail-at-scale]

## 소프트웨어 쪽 다섯 자리

- **공유 자원(shared resources)** — 기계가 여러 애플리케이션에 공유되면 그들이 CPU 코어, 프로세서
  캐시, 메모리 대역폭, 네트워크 대역폭 같은 자원을 두고 경합한다. 같은 애플리케이션 안에서도 서로
  다른 요청이 자원을 두고 다툴 수 있다 (p.74).[^dean2013-tail-at-scale]
- **데몬(daemons)** — 배경 데몬은 평균으로는 제한된 자원만 쓰지만, 스케줄되는 순간 **수 밀리초짜리
  딸꾹질**을 만들어 낸다 (p.74).[^dean2013-tail-at-scale]
- **전역 자원 공유(global resource sharing)** — 서로 다른 기계에서 도는 애플리케이션들이 네트워크
  스위치나 공유 파일 시스템 같은 전역 자원을 두고 경합한다 (p.76).[^dean2013-tail-at-scale]
- **유지보수 활동(maintenance activities)** — 분산 파일 시스템의 데이터 재구성, BigTable 같은 저장
  시스템의 주기적 로그 컴팩션, 가비지 컬렉션 언어의 주기적 가비지 컬렉션 같은 배경 활동이 지연에
  주기적 스파이크를 만든다 (p.76).[^dean2013-tail-at-scale]
- **큐잉(queueing)** — 중간 서버와 네트워크 스위치의 **여러 층에 걸친 큐잉이 이 가변성을 증폭한다**
  (p.76).[^dean2013-tail-at-scale]
  - 큐가 응답 시간 곡선을 어떻게 꺾는지의 어휘는
    [응답 시간과 처리량](../concepts/response-time-and-throughput.md)에 있다. 이 논문이 더하는 것은
    큐가 한 층이 아니라 **여러 층**이라 가변성이 층마다 곱해진다는 관찰이다.

## 하드웨어 추세가 더하는 셋

- **전력 한계(power limits)** — 현대 CPU는 평균 전력 범위를 일시적으로 넘겨 도는 것을 전제로
  설계되며, 그 활동이 오래 지속되면 **스로틀링으로 열 영향을 완화한다.** 스로틀링이 걸리는 순간
  같은 코드가 느려진다 (p.76).[^dean2013-tail-at-scale]
- **가비지 컬렉션(garbage collection)** — 솔리드 스테이트 저장 장치는 매우 빠른 무작위 읽기를 주지만,
  많은 수의 데이터 블록을 주기적으로 회수해야 한다. 저자들의 수치는 이렇다
  (p.76):[^dean2013-tail-at-scale]

  > the need to periodically garbage collect a large number of data blocks can increase read
  > latency by a factor of 100 with even a modest level of write activity

  즉 **쓰기 활동이 대단하지 않아도 읽기 지연이 100배까지 늘 수 있다.**
- **에너지 관리(energy management)** — 여러 종류의 장치에 있는 절전 모드는 에너지를 상당히 아끼지만
  비활성 상태에서 활성 상태로 옮겨 갈 때 **추가 지연을 더한다**
  (p.76).[^dean2013-tail-at-scale]

여기서 이름이 언어 런타임 층과 그대로 겹친다. 같은 이름의 기제를 JVM 쪽에서 다루는 자리는
[JVM 메모리 관리](../synthesis/jvm-memory-management.md)이고, 이 논문은 그 기제가 **응답 시간
분포의 꼬리로 나타난다**는 쪽만 말한다.

## 저자들이 2013년에 내다본 앞날

이 절의 서술은 저자들의 2013년 시점 전망이다. 그 뒤 하드웨어가 실제로 어떻게 갔는지는 이 소스가
답하지 않는다.

- 저자들은 2013년 시점에 **하드웨어 층의 가변성이 앞으로 더 커질 것**이라고 본다. 근거로 둘을 든다 —
  더 공격적인 전력 최적화가 가용해지는 것과, 심(深)서브미크론 수준의 제조 난점이 **장치 수준의
  이질성(device-level heterogeneity)** 을 낳는 것이다 (Hardware Trends and Their Effects,
  p.80).[^dean2013-tail-at-scale]
- 그 귀결로 저자들은 장치 이질성과 계속 커지는 시스템 규모가 겹치면 **소프트웨어 기법으로 가변성을
  견디는 일이 시간이 갈수록 더 중요해진다**고 본다 (p.80).[^dean2013-tail-at-scale]
- 반대 방향의 전망도 함께 적는다. 저자들은 몇몇 떠오르는 하드웨어 추세가 **지연 감내 기법의 효과를
  키울 것**이라고 본다 (p.80):[^dean2013-tail-at-scale]
  - 데이터센터 네트워크의 더 높은 이분 대역폭(bisection bandwidth)과, 원격 직접 메모리 접근
    (remote direct-memory access) 같은 메시지당 오버헤드를 줄이는 네트워크 인터페이스 최적화가
    **묶인 요청(tied request)의 비용을 낮추고**, 취소 메시지가 제때 도착해 중복 작업을 피할 가능성을
    높인다.
  - 메시지당 오버헤드가 낮아지면 자연히 더 잘게 쪼갠 요청이 가능해져 **다중화가 좋아지고 선두
    차단(head-of-line blocking) 효과를 피하는 데 기여한다.**

## 이어지는 페이지

- [부품의 가변성을 줄이는 공학](../concepts/reducing-component-variability.md) — 이 원인들을 겨냥하는 쪽
- [꼬리 내성이라는 설계 태도](../concepts/tail-tolerance-as-a-design-stance.md) — 원인을 못 없앨 때의 입장
- [지연의 백분위](../concepts/latency-percentiles.md) — 이 가변성이 나타나는 지표
- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 큐잉이 응답 시간을 꺾는 기제
- [프로세스 멈춤](../concepts/process-pauses.md) — 가비지 컬렉션과 절전 전환이 만드는 멈춤의 분산
  시스템 쪽 서술

[^dean2013-tail-at-scale]: Dean & Barroso 2013, "The Tail at Scale", CACM 56(2), pp.74–80.
    쪽수는 CACM 게재본 기준(PDF 스냅샷 1–7쪽 = pp.74–80).

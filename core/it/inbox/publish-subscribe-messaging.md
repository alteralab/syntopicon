---
type: concept
title: 발행/구독 메시징
description: 발행자가 수신자를 지정하지 않고 메시지를 분류만 하는 전달 패턴 — 직접 연결이 기술 부채로 무너지는 경로와 중앙 집중 시스템이 요구되는 지점
generated: { by: "claude-opus-5", at: "2026-08-10T00:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
status: draft
---

# 발행/구독 메시징

하나의 질문: **데이터를 만드는 쪽과 쓰는 쪽을 어떻게 떼어 놓는가.** 카프카를
논하기 전에 먼저 이해해야 할 패턴이며, 카프카는 이 패턴의 한 구현이다 (1장,
p.1).[^shapira2021]

## 패턴의 정의

- 원문 직인용 (1장, p.1):[^shapira2021]

> *Publish/subscribe (pub/sub) messaging* is a pattern that is characterized by
> the sender (publisher) of a piece of data (message) not specifically directing
> it to a receiver. Instead, the publisher classifies the message somehow, and
> that receiver (subscriber) subscribes to receive certain classes of messages.

- 발행/구독 시스템에는 대개 브로커(broker)가 있다 — 메시지가 발행되는 중앙
  지점이며, 이 패턴을 성립시키는 장치다 (1장, p.1).[^shapira2021]

## 어떻게 시작되는가 — 직접 연결의 부채

- 발행/구독의 많은 사례는 같은 방식으로 출발한다: 단순한 메시지 큐 하나, 또는
  프로세스 간 통신 채널 하나. 예를 들어 모니터링 정보를 보내야 하는 애플리케이션이
  대시보드를 띄우는 지표(metrics) 서버로 직접 연결을 열고 지표를 밀어 넣는다
  (1장, p.2).[^shapira2021]
- 이 단순한 해법이 무너지는 경로 (1장, pp.2–3):[^shapira2021]
  - 장기 분석을 위해 지표를 받아 저장·분석하는 새 서비스를 만들면, 애플리케이션은
    두 시스템 모두에 지표를 써야 한다.
  - 지표를 만드는 애플리케이션이 늘어나면 그 애플리케이션들이 모두 같은 두 서비스로
    연결을 만든다.
  - 경보를 위한 능동 폴링(polling)을 붙이면 애플리케이션마다 요청에 응답할 서버를
    또 하나씩 얹게 된다.
  - 결과는 연결을 추적하기조차 어려운 구조이며, 여기 쌓인 **기술 부채(technical
    debt)는 명백하다**.
- 1차 해소: 모든 애플리케이션의 지표를 받는 단일 애플리케이션을 세우고, 지표를
  필요로 하는 어느 시스템이든 질의할 수 있는 서버를 제공한다. 이 시점에 이미
  발행/구독 메시징 시스템을 하나 만든 것이다 (1장, p.3).[^shapira2021]

## 2차 문제 — 개별 큐 시스템의 난립

- 지표에서 벌어진 일이 로그 메시지에서도, 프론트엔드의 사용자 활동 추적에서도
  똑같이 반복된다. 각자 발행자와 구독자를 분리하는 시스템을 따로 구축하게 된다
  (1장, p.3).[^shapira2021]
- 이 상태는 점대점(point-to-point) 연결보다는 명백히 낫지만 중복이 크다 — 데이터를
  큐잉하는 시스템 여러 벌을 유지해야 하고, **각각이 자기만의 버그와 한계를 가진다**
  (1장, p.4).[^shapira2021]
- 도달해야 할 지점: 일반화된 유형의 데이터를 발행할 수 있고 비즈니스와 함께
  성장하는 **중앙 집중화된 단일 시스템** (1장, p.4).[^shapira2021]

## 이어지는 페이지

- [카프카의 메시지, 배치, 스키마](../concepts/kafka-message-batch-schema.md) — 이
  문제를 풀려고 만들어진 발행/구독 시스템이 데이터를 어떤 단위로 다루는가
- [왜 카프카인가](../concepts/why-kafka.md) — 발행/구독 시스템 선택지 중 카프카를
  고르는 근거
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 차원 관리자·팩트 제공자
  (17·18)가 같은 발행-구독 분업을 DW 백룸 안에서 쓴다

[^shapira2021]: Shapira et al. 2021, 1장 "Meet Kafka"

---
type: synthesis
title: 비기능 요건
description: 기능 목록 바깥에서 시스템의 값어치를 정하는 요건들을 모으는 허브 — 성능을 재는 지표와 분포, 잘못돼도 계속 도는 것, 부하가 늘 때 대처하는 능력, 그리고 오래 살려 두는 비용
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
---

# 비기능 요건

애플리케이션이 **무엇을 하는가**가 아니라 **얼마나 빠른가·얼마나 잘 버티는가·얼마나
자라는가·얼마나 오래 손볼 만한가**를 다루는 페이지들을 모은다. 어느 것도 하나의 수로
답해지지 않으며, 각 페이지가 그 어휘를 정의한다.

## 성능

- [응답 시간과 처리량](../concepts/response-time-and-throughput.md) — 두 지표의 정의, 큐잉이
  만드는 곡선, 지연과 응답 시간을 갈라 쓰는 어휘
- [지연의 백분위](../concepts/latency-percentiles.md) — 평균 대신 중앙값과 p95·p99를 보는
  이유, 꼬리 지연 증폭, 백분위를 계산하는 법
- [서비스 수준 목표](../concepts/service-level-objectives.md) — 지표를 약속으로 바꾸는
  SLI·SLO·SLA·OLA와 소진율 경보

## 신뢰성

- [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md) — 결함과 장애의 층위
  구분, 단일 장애점, 결함 주입과 카오스 엔지니어링
- [하드웨어·소프트웨어·사람의 결함](../concepts/hardware-software-and-human-faults.md) —
  세 원천의 발생률과 상관 구조, 무비난 사후 분석
- [분산 컴퓨팅의 오류](../concepts/fallacies-of-distributed-computing.md) — 원격 통신에 대한
  가정들, 연쇄 장애와 메타안정 장애

## 확장성

- [확장성과 부하](../concepts/scalability-and-load.md) — 부하를 서술하는 법, 선형 확장성,
  공유 메모리·공유 디스크·무공유, 만능 비법이 없다는 전제 위의 원칙들
- [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md) — 읽을 때
  조인할 것인가 쓸 때 미리 만들 것인가를 수로 따진 사례

## 유지보수성

- [유지보수성](../concepts/maintainability.md) — 운영성·단순성·진화성, 추상화, 되돌릴 수 없음

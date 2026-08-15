---
type: concept
title: 람다 아키텍처와 카파 아키텍처
description: 배치와 스트림을 하나의 시스템으로 합치려는 두 제안 — 문제가 많아 쓰이지 않게 된 람다와 그 자리를 대신한 카파, 그리고 그런 통합이 실제로 요구하는 세 가지 기능
generated: { by: "claude-opus-5", at: "2026-08-15T09:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 람다 아키텍처와 카파 아키텍처

하나의 질문: **이력 데이터의 재처리와 방금 도착한 이벤트의 처리를 같은 시스템에서 하려면
무엇이 필요한가.**

## 두 제안

- **배치와 스트림 처리를 통합하려는 초기 제안이 람다 아키텍처(lambda architecture)였는데,
  여러 문제가 있었고 쓰이지 않게 됐다** (13장, p.546).[^kleppmann2026]
- **더 최근의 시스템은 배치 계산(이력 데이터 재처리)과 스트림 계산(도착하는 대로 이벤트를
  처리하는 것)이 같은 시스템에서 구현되게 하며, 이 접근은 때때로 카파 아키텍처(kappa
  architecture)로 알려져 있다** (13장, p.546).[^kleppmann2026]

## 통합이 요구하는 세 기능

- **배치와 스트림 처리를 한 시스템에서 통합하려면 다음 기능이 필요하다** (13장,
  p.546):[^kleppmann2026]
  - **최근 이벤트의 스트림을 다루는 같은 처리 엔진을 통해 이력 이벤트를 재생(replay)할 수 있는
    능력. 예컨대 로그 기반 메시지 브로커는 메시지를 재생할 수 있고, 어떤 스트림 프로세서는
    분산 파일시스템이나 객체 저장소에서 입력을 읽을 수 있다.**
  - **스트림 프로세서를 위한 정확히 한 번 의미론 — 즉 결함이 실제로 일어났더라도 출력이 결함이
    없었을 때와 같도록 보장하는 것. 배치 처리와 마찬가지로 이는 실패한 태스크의 부분 출력을
    버리는 것을 요구한다.**
  - **처리 시간이 아니라 이벤트 시간으로 윈도잉하는 도구. 이력 이벤트를 재처리할 때 처리 시간은
    무의미하기 때문이다. 예컨대 Apache Beam이 그런 계산을 표현하는 API를 제공하며, 이는 Apache
    Flink나 Google Cloud Dataflow로 실행될 수 있다.**

## 이어지는 페이지

- [재처리와 점진적 마이그레이션](../concepts/reprocessing-and-gradual-migration.md) — 재처리가
  왜 필요한가라는 앞선 물음
- [로그 기반 메시지 브로커](../concepts/log-based-message-brokers.md) — 위 재생 능력의 근거
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 둘째 요구의 전문
- [스트림 처리의 시간 의미론](../concepts/stream-processing-time-semantics.md) — 이벤트 시간과
  처리 시간의 구분
- [스트림 처리의 시간 윈도우](../concepts/stream-processing-time-windows.md) — 셋째 요구의 도구
- [스트림 처리 프레임워크 고르기](../concepts/choosing-a-stream-processing-framework.md) —
  실제로 무엇을 고를 것인가

[^kleppmann2026]: Kleppmann & Riccomini 2026, 13장 "A Philosophy of Streaming Systems"

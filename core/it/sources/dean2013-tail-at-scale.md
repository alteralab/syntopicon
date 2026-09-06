---
type: article-journal
title: "The Tail at Scale"
author:
  - { family: Dean, given: Jeffrey }
  - { family: Barroso, given: "Luiz André" }
issued: "2013-02"
container-title: "Communications of the ACM"
volume: "56"
issue: "2"
page: "74-80"
DOI: "10.1145/2408776.2408794"
URL: "https://www.barroso.org/publications/TheTailAtScale.pdf"
snapshot: /it/archive/dean2013-tail-at-scale/
snapshot_sha256: "708bd2f01486b2a8e1bcaa46279c6eb9f655af7fe3f5502f04ff0e0d3d85dba2"
accessed: "2026-09-07"
---

# The Tail at Scale

꼬리 지연(tail latency)의 원전. 대규모 분산 서비스에서 드문 지연 사건이 팬아웃으로 증폭되는 구조와,
가변성을 없애는 대신 견디는 기법(헤지 요청·묶인 요청·마이크로 파티션·선택적 복제·지연 유발 요청 격리)을
Google 실측과 함께 세운 논문. CACM 게재본을 저자(Barroso) 페이지에서 확보했다 — cacm.acm.org는
자동 접근을 막는다(403, 2026-09-07).

KB 안의 자리: `latency-percentiles`(kleppmann2026 전언의 "꼬리 지연 증폭")의 원전. 2026년 gRPC
`hedgingPolicy`·Envoy `hedge_policy`가 이 논문을 계보로 잇는다(구현은 시도 수·throttling이 더해진 확장형).
이 소스는 헤지 도입 여부와 비용·위험을 뒷받침하고, 임계값은 정하지 않는다.

---
type: paper-conference
title: "Metastable Failures in Distributed Systems"
author:
  - { family: Bronson, given: Nathan }
  - { family: Aghayev, given: Abutalib }
  - { family: Charapko, given: Aleksey }
  - { family: Zhu, given: Timothy }
issued: "2021-06"
event-title: "Workshop on Hot Topics in Operating Systems (HotOS '21)"
publisher: "ACM"
DOI: "10.1145/3458336.3465286"
URL: "https://sigops.org/s/conferences/hotos/2021/papers/hotos21-s11-bronson.pdf"
snapshot: /it/archive/bronson2021-metastable/
snapshot_sha256: "4c460ba6116e3aff7ce99828a38d5647fde9a890270e95c2ce25c51c64d3c635"
accessed: "2026-09-07"
---

# Metastable Failures in Distributed Systems

준안정 장애(metastable failure) — 일시적 트리거로 들어간 과부하 상태가 트리거가 사라진 뒤에도 스스로
유지되는 장애 부류 — 를 처음 정의한 원전. 취약 상태·트리거·지속 효과 루프(재시도·캐시 미스·GC 등)의
틀을 세운다. 실증 후속은 [[huang2022-metastable-wild]].

KB 안의 자리: 재시도 정책·부하 차단·연쇄 장애의 상위 실패 모델. rahman2025 4장의 회로 차단기 예제,
`rate-limiting-with-virtual-threads`, `fallacies-of-distributed-computing`(서킷 브레이커 전언)이 호출자다.
이 소스는 실패 모델을 세우고, 재시도 알고리즘·임계값은 정하지 않는다.

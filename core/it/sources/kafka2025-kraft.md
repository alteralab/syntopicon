---
type: webpage
title: "Apache Kafka 4.0 Documentation: KRaft and ZooKeeper Removal"
author:
  - { literal: "Apache Software Foundation" }
issued: "2025"
version: "4.0"
URL: "https://kafka.apache.org/40/getting-started/zk2kraft/"
snapshot: /it/archive/kafka2025-kraft/
snapshot_sha256: "4d195c8fd829c81a1905519edd8c50d5d47c65736c373a2c6cfd0556450b7f7a"
accessed: "2026-08-11"
---

# Apache Kafka 4.0 — KRaft와 ZooKeeper 제거

**이 소스는 버전 분기 실험을 위해 들인다.** 기존
[주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)가 Kafka 3.x 이하 기준이고
`stale_after: "2025-03-18"`(4.0 공표일)로 만료 상태인데, 그 자리를 대체할 소스가
이것이다.

## 실험이 답할 것

옛 버전 지식이 새 버전 소스를 만났을 때 어떻게 되는가. 세 갈래가 있고 이 런의
산출물은 **어느 쪽이 옳은지의 판정**이다:

1. **제자리 개정** — 한 페이지에 두 버전 병기(DDIA가 킴벌 위에 누적한 방식)
2. **버전별 분리** — 3.x 페이지를 남기고 4.x 페이지를 신설, 서로 링크
3. **대체** — `superseded_by`로 3.x를 deprecated 전환

**3.x 지식이 여전히 유효하다**는 것이 전제다. 3.x 클러스터를 운영하는 사람에게
주키퍼 앙상블 서술은 지금도 참이다. 어느 갈래든 그 지식이 검색에서 살아남아야
한다.

## 함께 판정할 것 둘

- **버전 조건 표기의 통일.** 지금 코퍼스에 최소 4종이 표류한다: `(Kafka 3.x 이하
  기준 서술.)`, `(Kafka ≤3.x 기준 서술 — 4.0부터 …)`, `JDK 15에서 폐기 대상이`,
  `JDK 18 이후 JDK에는 해당하지 않는다`. 기호·위치·범위 표현이 제각각이다.
- **소스 메타의 버전 종속 표시.** 지금은 "버전 종속 소스다"를 산문으로만 적어
  기계가 못 읽는다. 이 파일은 실험 삼아 CSL `version` 필드를 쓴다(스키마에 선언은
  돼 있으나 지금까지 사용 0건 — lint의 field-unused 목록에 있었다).

## 판본

Kafka 4.0 문서 2쪽(2026-08-11 조회): `getting-started/zk2kraft/`(모드 간 차이와
제거된 설정 목록), `operations/kraft/`(KRaft 운영). locator는 **문서 경로 + 절
제목**을 쓴다(dbt 런과 같은 형식).

**"4.0 계열 고정본"이라는 첫 서술은 스냅샷이 반박했다**(2026-08-11 실측): 두 파일
하단에 `Last modified March 20, 2026`이 찍혀 있고 상단 배너가 "You are viewing
documentation for an older version (4.0) of Kafka"라고 말한다. 4.0.0 릴리스는
2025년 3월인데 문서는 2026년 3월에도 손질됐다 — **버전별 갈래이면서도 계속 갱신되는
문서**다.

그래서 `version: "4.0"`이 담는 것은 "문서가 얼었다"가 아니라 **이 소스가 서술하는
제품 버전**이다. 문서 판본의 식별은 `accessed`와 `snapshot_sha256`이 담당한다.

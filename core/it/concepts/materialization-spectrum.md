---
type: concept
title: 구체화 스펙트럼
description: 변환 결과를 매번 다시 계산할 것인가 저장할 것인가 — 계산 비용을 조회 시점에 낼지 빌드 시점에 낼지로 갈리는 다섯 형태, 그리고 배포와 갱신이 같은 명령인지가 여기서 정해지는 이유
generated: { by: "claude-opus-5", at: "2026-08-11T04:00:00Z" }
sources:
  - { id: dbtlabs2026-materialization, resource: /it/sources/dbtlabs2026-materialization.md }
---

# 구체화 스펙트럼

이 페이지의 질문: **변환 결과를 어떤 물리 형태로 남길 것이고, 그 선택이 계산
비용을 언제 치르게 하는가.**

- 구체화(materialization)의 정의는 원문 그대로 (materializations.md,
  "Overview"):[^dbtlabs2026-materialization]

> Materializations are strategies for persisting dbt models in a warehouse.

- 내장 형태는 다섯이다 — 뷰(view)·테이블(table)·증분(incremental)·임시
  (ephemeral)·구체화 뷰(materialized view). 이 집합은 닫혀 있지 않고 사용자 정의
  구체화로 확장할 수 있다 (materializations.md,
  "Overview").[^dbtlabs2026-materialization]

## 계산 비용을 언제 내는가

- **뷰**: 실행마다 뷰로 다시 만들어진다. 추가로 저장되는 데이터가 없고 원천의 최신
  레코드가 항상 보인다. 대신 변환이 무겁거나 뷰가 뷰 위에 쌓이면 조회가 느리다 —
  계산 비용을 조회 시점에 낸다 (materializations.md,
  "View").[^dbtlabs2026-materialization]
- **테이블**: 실행마다 테이블로 다시 만들어진다. 조회는 빠르지만 재구축이 오래
  걸리고, 원천에 새 레코드가 생겨도 자동으로 반영되지 않는다 — 계산 비용을 빌드
  시점에 내고 신선도를 빌드 주기에 종속시킨다 (materializations.md,
  "Table").[^dbtlabs2026-materialization]
- **임시**: 데이터베이스에 만들어지지 않고, 의존하는 모델 안에 공통 테이블 식
  (common table expression, CTE)으로 끼워 넣어진다. 재사용 가능한 로직은
  유지하면서 웨어하우스에 객체를 남기지 않지만, 직접 조회할 수 없고 남용하면 질의
  디버깅이 어려워진다 (materializations.md,
  "Ephemeral").[^dbtlabs2026-materialization]
- **증분**: 마지막 실행 이후의 레코드만 삽입·갱신한다. 새 레코드만 변환하므로 빌드
  시간을 크게 줄이지만, 추가 설정이 필요한 고급 사용법이다 (materializations.md,
  "Incremental").[^dbtlabs2026-materialization] 대가의 상세는
  [증분 처리와 그 대가](../concepts/incremental-processing-tradeoffs.md).
- **구체화 뷰**: 뷰와 테이블의 조합이며 증분 모델과 비슷한 용도를 맡는다. 테이블의
  조회 성능과 뷰의 데이터 신선도를 겸하되, 데이터베이스 객체가 복잡한 만큼 플랫폼이
  제공하는 설정 여지가 적고 지원하지 않는 플랫폼도 있다 (materializations.md,
  "Materialized View").[^dbtlabs2026-materialization]

## 순서 규범 — 뷰에서 시작한다

- 모델의 기본값은 뷰이고, 조언은 뷰로 시작해 성능 문제를 관측했을 때만 다른 형태로
  바꾸라는 것이다. 뷰는 이름 바꾸기·형 변환처럼 큰 변환을 하지 않는 모델에 가장
  맞는다 (materializations.md, "Configuring materializations",
  "View").[^dbtlabs2026-materialization]
- 테이블은 BI 도구가 조회하는 모델과, 여러 하류 모델이 쓰는 느린 변환에 쓴다
  (materializations.md, "Table").[^dbtlabs2026-materialization]
- 증분은 이벤트성 데이터에 가장 맞고 실행이 너무 느려질 때 도입한다 — **증분에서
  시작하지 않는다** (materializations.md,
  "Incremental").[^dbtlabs2026-materialization]
- 임시는 DAG 앞쪽의 아주 가벼운 변환이면서, 한두 개의 하류 모델만 쓰고, 직접 조회할
  필요가 없는 것에 쓴다 (materializations.md,
  "Ephemeral").[^dbtlabs2026-materialization]
- 증분으로 충분하지만 증분 로직과 갱신을 데이터 플랫폼에 맡기고 싶을 때 구체화 뷰를
  고려한다 (materializations.md, "Materialized
  View").[^dbtlabs2026-materialization]

## 배포와 갱신이 같은 명령인가

- 뷰와 구체화 뷰에 대한 실행은 설정이나 SQL이 바뀔 가능성이 있을 때만 필요하다 —
  사실상 배포 동작이다. 테이블은 그 경우에 더해 **테이블 안의 데이터를 갱신해야 할
  때도** 실행이 필요하고, 증분 모델과 스냅샷도 바탕이 테이블이므로 마찬가지다
  (materializations.md, "Scheduled Refreshes").[^dbtlabs2026-materialization]
- 테이블 뒤의 데이터를 자동으로 갱신해 주는 기능은 내장돼 있지 않다 — 그 자리의
  스케줄링은 dbt 자신이나 별도 스케줄러가 맡는다. 반면 대부분의 플랫폼은 구체화
  뷰의 자동 갱신을 설정할 수 있게 해 주고, 그래서 구체화 뷰는 데이터를 갱신하려고
  실행을 걸 필요가 없다는 점만 다른 증분 모델처럼 동작한다 (materializations.md,
  "Scheduled Refreshes").[^dbtlabs2026-materialization]
  - #hypothesis 그래서 이 스펙트럼은 저장량만이 아니라 **운영 부담이 어디에
    놓이는가**의 축이기도 하다. 저장하는 쪽으로 갈수록 갱신을 누가 언제 거는가라는
    질문이 새로 생긴다.

## 이어지는 페이지

- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) —
  구체화는 파생 데이터를 언제 다시 만들고 언제 저장하느냐의 정책이다
- [정보 마트](../concepts/information-mart.md) — 같은 축을 Data Vault 쪽에서
  물질화와 가상화(뷰)로 부른다
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 집계 빌더(19)가 "집계는
  인덱스처럼 성능을 위한 파생 구조"라고 말하는 자리
- [읽기·쓰기·공간 증폭](../concepts/read-write-space-amplification.md) — 저장 엔진
  층위에서 같은 종류의 맞바꿈을 재는 자
- [증분 갱신 전략](../concepts/incremental-update-strategies.md) — 증분을 고른 뒤에
  갈리는 다음 선택

[^dbtlabs2026-materialization]: dbt Labs 2026, dbt 공식 문서 "Build" 절

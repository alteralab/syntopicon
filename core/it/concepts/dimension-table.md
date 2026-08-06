---
type: concept
title: 차원 테이블
description: 측정 이벤트의 서술 맥락(누가·무엇을·어디서)을 담는 테이블 — 분석력은 속성 품질에 비례
generated: { by: "claude-fable-5", at: "2026-08-06T16:10:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 차원 테이블

차원 테이블(dimension table)은 측정 이벤트에 붙는 서술 맥락 — "누가, 무엇을,
어디서, 언제, 어떻게, 왜" — 을 담는 [팩트 테이블](fact-table.md)의 동반자다.
행은 팩트보다 훨씬 적지만 50–100개 속성으로 넓어질 수 있고, 단일 기본 키가
참조 무결성의 기반이 된다 (1장, p.13).[^kimball2013]

## 속성이 곧 분석력이다

- 차원 속성은 질의 제약·그루핑·보고서 라벨의 원천이다 — 사용자가 "브랜드**별**
  매출"을 원하면 브랜드가 차원 속성이어야 한다("by" 단어 판별법) (1장, p.13).[^kimball2013]
- (1장, p.14)[^kimball2013]

> the analytic power of the DW/BI environment is directly proportional to
> the quality and depth of the dimension attributes.

- 그래서 암호 같은 코드 대신 실제 단어로 된 서술을 담고, 운영 코드에 의미가
  박혀 있으면(자릿수별 의미) 분리된 속성으로 풀어 담는다 (1장, pp.13–14).[^kimball2013]
- 차원은 데이터의 진입점(entry point)이자 모든 분석의 최종 라벨이다
  (1장, p.14).[^kimball2013]

## 팩트인가 속성인가

- 판별 질문: 많은 값을 갖고 계산에 참여하는 측정이면 팩트, 소수 값의 거의
  불변인 서술이면 차원 속성. **연속 수치는 거의 항상 팩트, 작은 목록에서
  뽑힌 이산 수치는 거의 항상 속성**이다 (1장, pp.14–15).[^kimball2013]

## 계층은 비정규화한다

- 제품→브랜드→카테고리 같은 다대일 계층은 차원 안에 중복 저장한다. 브랜드
  룩업 테이블로 빼는 정규화가 눈송이화(snowflaking)인데, 차원은 팩트보다
  기하급수적으로 작아 공간 절약이 무의미하다 — **단순성·접근성을 위해 공간을
  치르는 교환이 거의 항상 옳다** (1장, p.15).[^kimball2013]

Data Vault와의 대응: [Satellite](../concepts/data-vault-satellite.md)가 같은 서술 맥락
자리를 맡되 이력 추적을 우선하고, Kimball의 눈송이화 금지와 달리 원천·변경
빈도별 분할을 권장한다 — 두 방법론이 갈라지는 지점이다.

[^kimball2013]: Kimball & Ross 2013, 1장 "Data Warehousing, Business Intelligence, and Dimensional Modeling Primer"

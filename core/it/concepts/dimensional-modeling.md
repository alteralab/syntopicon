---
type: concept
title: 차원 모델링
description: 이해 가능성과 질의 성능을 동시에 겨냥한 분석 데이터 표현 기법 — 정규화 모델과의 관계와 5대 오해
generated: { by: "claude-fable-5", at: "2026-08-06T16:10:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 차원 모델링

차원 모델링(dimensional modeling)은 분석 데이터를 내놓는 기법으로, 두 요구를
동시에 만족시키는 것이 존재 이유다: **업무 사용자가 이해할 수 있는 데이터**와
**빠른 질의 성능** (1장, p.7).[^kimball2013]

- 50년 넘게 수렴해 온 구조이고, 용어의 기원도 Kimball이 아니다 — fact와
  dimension이라는 말은 1960년대 General Mills·Dartmouth 공동 연구에서 나와
  1970년대 AC Nielsen·IRI가 정착시켰다 (1장, p.15).[^kimball2013]
- [팩트 테이블](fact-table.md)(측정값)과 [차원 테이블](../concepts/dimension-table.md)
  (서술 맥락)을 조인한 별 모양 구조가 스타 스키마(star schema)다. 같은 논리
  설계를 다차원 DB에 구현하면 OLAP 큐브(cube)인데, 권장은 원자 데이터를 스타
  스키마에 적재하고 큐브는 그로부터 파생시키는 것이다 (1장, pp.8–9).[^kimball2013]

## 정규화 모델과의 관계

- 차원 모델은 3NF(정규화) 모델과 정보량이 같다 — 다른 것은 포장이다 (1장, p.8):[^kimball2013]

> A dimensional model contains the same information as a normalized model,
> but packages the data in a format that delivers user understandability,
> query performance, and resilience to change.

- 정규화 모델이 분석 제시 계층에 부적합한 이유 둘: 사용자가 LA 고속도로 지도
  같은 모델을 이해·탐색·기억하지 못하고, RDBMS 옵티마이저가 예측 불가능한
  복잡 질의를 감당하지 못한다 (1장, p.8).[^kimball2013]
- 반대로 차원 모델의 단순성은 성능 그 자체다 — 옵티마이저가 "고도로 인덱싱된
  차원을 먼저 제약하고 그 키들의 데카르트 곱으로 팩트 인덱스를 단일 패스
  공격"하는 강한 가정을 세울 수 있다 (1장, p.16).[^kimball2013]
- 대칭·확장성: 모든 차원이 동등한 진입점이라 질의 패턴 편향이 없고, 기존
  행마다 단일 값이 정의되는 한 새 차원·팩트·속성을 ALTER TABLE만으로 더해도
  기존 BI 앱은 결과 변화 없이 돈다 (1장, pp.16–17).[^kimball2013]

## 5대 오해 (1장, pp.30–32)[^kimball2013]

1. "요약 전용이다" — 반대로 원자(atomic) 데이터가 기본이다. 미리 요약하면
   드릴다운 벽에 부딪히고, 질의 유연성의 비결이 가장 낮은 입도의 팩트다.
2. "부서 단위다" — 부서가 아니라 **업무 프로세스**(주문·송장·서비스 콜)로
   조직한다. 같은 원천의 부서별 중복 추출이 불일치의 근원이다.
3. "확장이 안 된다" — 2조 행 팩트 테이블이 보고돼 있다.
4. "예측 가능한 용도 전용이다" — top-10 보고서가 아니라 안정적인 측정
   프로세스를 중심에 둔다.
5. "통합이 안 된다" — conformed dimension을 ETL의 중앙 마스터 데이터로 두면
   차원 모델들이 결합된다(버스 아키텍처 — [Kimball DW/BI 아키텍처](kimball-dwbi-architecture.md)).

방법론 축의 대안: [Data Vault 모델링](../concepts/data-vault-modeling.md)은 같은 웨어하우스
문제에서 감사 가능성·원천 보존을 우선한다 — Linstedt 책 7장도 정보 마트 계층은
차원 모델로 낸다.

[^kimball2013]: Kimball & Ross 2013, 1장 "Data Warehousing, Business Intelligence, and Dimensional Modeling Primer"

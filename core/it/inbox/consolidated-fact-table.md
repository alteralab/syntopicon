---
type: concept
title: 통합 팩트 테이블
description: 여러 업무 프로세스의 팩트를 같은 grain으로 합쳐 두는 패턴(실적 vs 예산 등) — drill-across와의 트레이드오프, 송장 헤더/라인 granularity 처리
status: draft
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 통합 팩트 테이블

하나의 질문: **서로 다른 업무 프로세스의 팩트(실적과 예산 등)를 언제 한 [팩트 테이블](../concepts/fact-table.md)로 합치나.**

## 정의와 동기

- 예산 대 약정(commitment)처럼 별개 프로세스의 지표 비교가 사용자 커뮤니티에서 **극히 빈번**하다면, 업무 사용자나 BI 애플리케이션이 매번 결과 집합을 꿰매게(drill-across) 두지 말고 지표를 한 번만 결합해 둔 단일 팩트 테이블을 만드는 것이 낫다 — 복잡성·정확성·도구 역량·성능 문제가 내재하기 때문이다 (7장, p.224).[^kimball2013]
- 여러 업무 프로세스의 지표를 공통 granularity로 결합한 팩트 테이블을 통합 팩트 테이블(consolidated fact table)이라 부른다 (7장, p.225).[^kimball2013]
- 전형 사례가 실적 대 예산이다: 회계기간·계정·조직 차원 위에 실적 금액, 예산 금액, 그리고 계산된 차이인 편차(variance)를 나란히 둔다 (7장, p.225).[^kimball2013]

## 트레이드오프 — drill-across 대비

- 통합 팩트 테이블은 성능과 사용성을 얻는 대신, 차원성을 "최소 공통분모"로 타협한다. 프로젝트 팀이 통합 테이블의 granularity만 보고 설계를 굳혀 더 세밀한 데이터 요구를 놓치는 것이 위험 요인이다 (7장, p.225).[^kimball2013]

> When facts from multiple business processes are combined in a consolidated
> fact table, they must live at the same level of granularity and
> dimensionality. … Project teams should not create artificial facts or
> dimensions in an attempt to force-fit the consolidation of differently
> grained fact data.

(7장, p.225)[^kimball2013]

- 반대로 프로세스 간 상관이 덜 긴밀하면 SQL drill-across로 결과를 결합하는 편이 더 타당하다. 통합 테이블을 만들 때도 카디널리티 차이를 다룰 업무 규칙이 필요하다 — 예: 권유(solicitation)와 응답(response)을 통합할 때 모든 권유·응답을 담을지, 둘 다 발생한 건만 담을지 (8장, p.260).[^kimball2013]
- 통합이든 아니든, 카디널리티가 다른 두 팩트 테이블을 하나의 SELECT에서 공통 차원에 동시 조인(fact-to-fact)하면 안 된다 — 다대일대다 조인은 관계형 엔진이 멀쩡히 동작해도 틀린 답을 낸다. 각 팩트를 따로 질의해 답 집합을 외부 조인하는 drill-across가 정석이다 (8장, pp.259–260).[^kimball2013]
- 수익성처럼 비용 팩트 소싱이 무거운 주제도, 수익·비용 요소들을 각자 프로세스로 먼저 공급한 뒤 통합 차원 모델로 다루는 후속 과제로 접근하는 경우가 많다 (6장, p.192).[^kimball2013]

## 송장 헤더/라인 처리

같은 문서(주문·송장)의 헤더와 라인은 "여러 프로세스"가 아니라 **한 프로세스의 두 granularity**다. 통합이 아니라 배분(allocation)으로 푼다.

- 팩트 grain은 라인 항목으로 잡고, 헤더의 서술 정보(주문일·고객·딜 등)는 별도 차원들로 분해해 라인 grain 팩트에 붙인다. 주문번호는 차원 테이블 없이 팩트에 남는 퇴화 차원(degenerate dimension)이 된다 (6장, p.178).[^kimball2013]
- 피해야 할 패턴 1 — 헤더를 통째로 차원으로: 운영계 주문 헤더를 복제한 차원은 팩트 대비 지나치게 크고(라인 5개/주문이면 팩트의 20%), 팩트와 같은 속도로 자라며, 고객·딜 분석마다 이 거대 차원을 경유하게 된다 (6장, pp.181–182).[^kimball2013]
- 피해야 할 패턴 2 — 헤더를 팩트 테이블로: 헤더 팩트에 차원성을 몰아주고 라인 팩트가 주문번호로만 조인하는 설계는, 라인을 헤더 속성으로 자를 때마다 큰 헤더 팩트와 더 큰 라인 팩트의 조인을 강제한다 (6장, pp.186–187).[^kimball2013]
- 헤더 수준 팩트(주문 전체 배송비 등)는 라인으로 배분해 내리는 것이 우선이다 — 배분해야 제품 차원으로 헤더 팩트를 자를 수 있다. 배분 규칙 합의는 정치적 문제이므로 재무 부서가 맡는 것이 이상적이다(activity-based costing이 곧 배분이다) (6장, pp.184–185).[^kimball2013]
- 배분이 불가능하면 헤더 grain의 별도 집계 팩트 테이블로 제시한다. 한 팩트 테이블에 헤더와 라인 granularity를 섞으면 안 된다 (6장, p.185).[^kimball2013]
- 나쁜 대안들: 미배분 헤더 팩트를 모든 라인에 반복(합산 시 과대계상), 첫/마지막 라인에만 저장(제품 필터에 걸리면 사라짐), 헤더 팩트용 특수 제품 키(사용자에게 해독 규칙을 강요) (6장, p.186).[^kimball2013]

[^kimball2013]: Kimball & Ross 2013, 6–8장 "Order Management" · "Accounting" · "Customer Relationship Management"

---
type: concept
title: 역할 연기 차원
description: 하나의 물리 차원(주로 날짜)이 뷰·별칭으로 한 팩트 테이블에 여러 번 등장하는 패턴 — 물리 복제·조합 테이블이 아닌 이유
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 역할 연기 차원

하나의 질문: **같은 차원이 한 팩트 테이블에 여러 번 필요할 때(주문일·요청 출하일처럼) 물리 테이블을 몇 개 두어야 하나.**

답은 하나다 — 물리 테이블은 하나만 두고, 역할(role)마다 고유하게 라벨링한 뷰(view)나 별칭(alias)으로 노출한다 (6장, pp.170–171).[^kimball2013]

> Role playing in a dimensional model occurs when a single dimension
> simultaneously appears several times in the same fact table. The underlying
> dimension may exist as a single physical table, but each of the roles should
> be presented to the BI tools as a separately labeled view.

## 왜 문제가 되나 — 이중 조인의 SQL 해석

- 트랜잭션 팩트 테이블의 1차 날짜는 트랜잭션 날짜(예: 주문일)지만, 요청 출하일처럼 부가 날짜가 흔히 따라온다. 각 날짜는 팩트 테이블의 외래 키여야 하는데, 두 외래 키를 **같은** 날짜 차원 테이블에 동시에 조인할 수는 없다 — SQL은 이 양방향 동시 조인을 "두 날짜가 동일해야 한다"는 조건으로 해석하기 때문이다 (6장, p.170).[^kimball2013]

## 해법 — 단일 물리 테이블 + 역할별 뷰/별칭

- 물리 날짜 차원 테이블은 하나만 만들어 관리하고, 뷰나 별칭으로 "독립된 두 날짜 차원"이라는 논리적 환상을 만든다. 이렇게 만든 두 논리 차원은 서로 완전히 무관한 제약을 걸 수 있는 독립 차원처럼 동작한다 (6장, pp.170–171).[^kimball2013]
- 각 뷰/별칭의 컬럼은 **고유하게 라벨링**해야 한다 — 주문 월(order month)과 요청 출하 월(requested ship month)을 구분하지 않으면, 두 컬럼이 한 리포트에 끌려 나왔을 때 구별할 수 없다 (6장, p.170).[^kimball2013]
- SQL 별칭이나 BI 도구 시맨틱 계층의 별칭 기능도 쓸 수 있지만, 여러 BI 도구와 직접 SQL 접근이 혼용되는 조직에서는 별칭 방식은 피하라고 경고한다 — 뷰가 모두에게 일관되게 보인다 (6장, p.171).[^kimball2013]

## 왜 물리 복제·조합 테이블이 아닌가

- 역할 조합마다 키를 부여한 단일 조합 날짜 테이블(주문일×요청출하일)은 두 가지로 무너진다: (1) 연 365행짜리 깔끔한 일 단위 테이블이 모든 날짜 조합을 담느라 크기가 폭발하고, (2) 조합 테이블은 더 이상 일·주·월 단위의 다른 적합(conformed) 날짜 차원들과 일치하지 않게 된다 (6장, p.171).[^kimball2013]
- 즉 물리 복제 대신 뷰를 쓰는 이유는 관리 지점을 하나로 유지하면서 표준 차원의 지위를 지키는 것이다. 예외는 도구 제약뿐 — 같은 차원의 다중 역할을 지원하지 않는 OLAP 제품에서는 역할마다 별도 차원을 만들 수밖에 없고, 그 결과 관계형 스타 스키마에서는 단순히 역할이었을 것들이 별개 차원으로 흩어진다 (6장, p.171).[^kimball2013]

## 어디까지 쓰이나

- 출하 송장 팩트: 송장일·요청 출하일·실제 출하일의 3개 역할 (6장, p.188).[^kimball2013]
- 주문 이행 파이프라인의 누적 스냅샷 팩트: 마일스톤 날짜 9개가 모두 날짜 차원의 역할이다. 이때 날짜 차원에는 Unknown/To Be Determined 행이 필요하다 — 파이프라인 행이 처음 적재될 때 다수의 날짜가 아직 미정이기 때문 (6장, pp.194–195).[^kimball2013]
- 총계정원장 분개 팩트: 전기일(posting date)과 회계 유효일을 구분해야 하면 두 번째 역할 연기 날짜 차원을 둔다 (7장, p.207).[^kimball2013]
- 고객 차원 안의 날짜(첫 구매일 등): SQL date 타입으로 두지 않고 날짜 차원으로의 외래 키로 바꾸면, 역할별 뷰(예: First Purchase Date 차원)가 차원 아웃리거(outrigger) 형태로 붙는다 (8장, pp.238–239).[^kimball2013]
- 팩트 테이블 밖에서도: 판매담당–고객 배정의 factless 팩트처럼 유효일·만료일 쌍도 날짜 차원의 2개 역할이다 (6장, p.177).[^kimball2013]

## 버스 매트릭스에 적는 법

- 버스 매트릭스에서는 한 셀 안에 여러 역할을 나열하는 표기가 가장 흔하다(예: Ordering 행의 Date 열에 "Order Date, Requested Ship Date"). 역할 수가 적고 프로세스 간 재사용이 잦으면 표준 차원 열 아래 하위 열을 만들 수도 있다 (6장, pp.171–172).[^kimball2013]

[^kimball2013]: Kimball & Ross 2013, 6–8장 "Order Management" · "Accounting" · "Customer Relationship Management"

---
type: concept
title: 퇴화 차원
description: 트랜잭션 번호처럼 차원 테이블 없이 팩트 테이블에 남는 차원 키 — 생기는 조건·용도·대리 키가 필요해지는 경우
status: draft
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 퇴화 차원

퇴화 차원(degenerate dimension)은 기본 키 말고는 내용이 없는 차원이다.
운영계의 트랜잭션 제어 번호가 [팩트 테이블](fact-table.md)에 차원 키처럼
앉아 있지만, 조인할 차원 테이블이 존재하지 않는다 (2장, p.47).[^kimball2013]

> This degenerate dimension is placed in the fact table with the explicit
> acknowledgment that there is no associated dimension table.

## 언제 생기나 — 헤더가 비워지는 과정

- 운영계 부모/자식(parent/child) 데이터베이스에서 POS 트랜잭션 번호는
  트랜잭션 헤더 레코드의 키였고, 거래 날짜·점포 식별자처럼 트랜잭션 전체에
  유효한 정보를 거느렸다. 그런데 차원 모델에서는 이 헤더 정보가 이미 날짜·점포
  등 다른 차원으로 **전부 추출된 뒤**다. 서술 속성이 다 벗겨져 결과 차원이
  비었기 때문에 "퇴화"라고 부른다 (3장, pp.93–94).[^kimball2013]
- 그래서 퇴화 차원은 팩트 테이블의 grain이 트랜잭션 1건 또는 트랜잭션 라인
  1건일 때 매우 흔하다 — 퇴화 차원이 곧 부모(헤더)의 고유 식별자이기 때문이다.
  주문 번호·송장(invoice) 번호·선하증권(bill-of-lading) 번호는 거의 항상 퇴화
  차원으로 나타난다 (3장, p.94).[^kimball2013]
- 세 가지 팩트 테이블 유형 중에서는 트랜잭션·누적 스냅샷 팩트 테이블에서
  가장 흔하다 (2장, p.47).[^kimball2013]

## 비어 있어도 남겨 두는 이유

- 트랜잭션 번호는 한 장바구니(market basket) 트랜잭션에 담긴 상품들을 함께
  묶는 그루핑 키로 유효하고, 운영 시스템으로 되짚어 갈 연결 고리도 된다
  (3장, p.93).[^kimball2013]
- 팩트 테이블 기본 키의 구성원이 되는 일이 많다. 소매 사례에서 팩트 테이블의
  기본 키는 퇴화된 POS 트랜잭션 번호 + 상품 키다 (3장, p.94).[^kimball2013]
- 표기 규약: 도식에서 외래 키(FK)와 구별해 DD로 표시한다 (3장, p.94).[^kimball2013]

## 다루는 규칙

- 다른 차원을 다 만들고도 헤더에 속하는 속성이 정당하게 남아 있다면, 그냥
  정상 차원 테이블을 만들고 정상 조인한다 — 그 시점부터는 퇴화 차원이 아니다.
  퇴화 여부는 지위가 아니라 "남은 내용이 있는가"의 결과다 (3장, p.94).[^kimball2013]
- 퇴화 차원에는 보통 대리 키(surrogate key)를 발급하지 않지만, 상황별 평가는
  필요하다. 트랜잭션 제어 번호가 점포 간에 유일하지 않거나 최댓값에 닿아
  재사용(wrap)되는 경우, 24바이트짜리 부피 큰 영숫자 컬럼인 경우, BI 도구가
  트랜잭션 번호로 드릴 어크로스하려면 차원 테이블이 필요한 경우에는 대리 키를
  발급한다 — 이렇게 차원 테이블을 갖게 된 제어 번호는 더 이상 퇴화 차원이
  아니다 (3장, p.101).[^kimball2013]

소매 사례의 설계 맥락은 [4단계 차원 설계 프로세스](four-step-dimensional-design.md)를,
차원 테이블 쪽 키 규약은 [차원 테이블](dimension-table.md)을 보라.

[^kimball2013]: Kimball & Ross 2013, 2장 "Kimball Dimensional Modeling Techniques Overview" · 3장 "Retail Sales"

---
type: concept
title: 팩트 테이블
description: 업무 프로세스 측정 이벤트를 담는 차원 모델의 중심 — 측정 이벤트 1:1 원칙·grain·합산 가능성
generated: { by: "claude-fable-5", at: "2026-08-06T16:10:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# 팩트 테이블

팩트 테이블(fact table)은 업무 프로세스 이벤트의 성과 측정값(measurement)을
담는 [차원 모델](../concepts/dimensional-modeling.md)의 중심 테이블이다. 측정 데이터는
전사에서 압도적으로 크므로 조직 기능별로 복제하지 않고 단일 저장소에 둔다
(1장, p.10).[^kimball2013]

## 기반 원칙 — 측정 이벤트와 1:1

(1장, p.11)[^kimball2013]

> The idea that a measurement event in the physical world has a one-to-one
> relationship to a single row in the corresponding fact table is a bedrock
> principle for dimensional modeling. Everything else builds from this
> foundation.

- 행의 상세 수준이 **grain**이다. 한 팩트 테이블의 모든 행은 같은 grain이어야
  한다 — 이 규율이 이중 계산을 막는다 (1장, pp.10–11).[^kimball2013]
- grain은 세 범주로 떨어진다: 트랜잭션 / 주기 스냅샷(periodic snapshot) /
  누적 스냅샷(accumulating snapshot). 트랜잭션이 가장 흔하다 (1장, p.12).[^kimball2013]
- 활동이 없으면 행을 넣지 않는다(0 채우기 금지) — 그래서 팩트 테이블은
  희소(sparse)하고, 그런데도 차원 모델 전체 공간의 90% 이상을 차지한다
  (1장, p.12).[^kimball2013]

## 합산 가능성

- 가장 유용한 팩트는 수치이고 합산 가능(additive)하다 — BI 질의는 행 하나가 아니라
  수십만 행을 가져와 합산하는 것이 기본 동작이라서다 (1장, p.11).[^kimball2013]
- 부분 합산 가능(semi-additive): 계좌 잔액처럼 시간 차원으로는 합산할 수 없다.
  합산 불가(non-additive): 단가처럼 어떤 축으로도 합산할 수 없다 — 카운트·평균으로만
  다룬다 (1장, p.11).[^kimball2013]
- 텍스트 팩트는 두지 않는다 — 모든 행에서 유일한 텍스트가 아닌 한 차원
  소속이다 (1장, p.12).[^kimball2013]

## 키 구조

- 팩트 테이블은 차원 기본 키를 가리키는 외래 키 2개 이상을 갖고, 전부 맞아
  떨어질 때 참조 무결성이 성립한다. 자체 기본 키는 외래 키의 부분 집합인
  복합 키(composite key)다 — **복합 키를 가진 테이블은 팩트 테이블이고, 그
  외는 전부 차원이다**. 팩트 테이블은 다대다 관계를 표현한다 (1장, p.12).[^kimball2013]

Data Vault와의 대응: [Link](../concepts/data-vault-link.md)도 다대다·복합 식별이라는 같은
자리에 서고, 링크 입도에 Hub 참조를 더하는 것은 팩트에 차원을 더하는 것과 같은
원리다 — Linstedt 자신의 유비다.

[^kimball2013]: Kimball & Ross 2013, 1장 "Data Warehousing, Business Intelligence, and Dimensional Modeling Primer"

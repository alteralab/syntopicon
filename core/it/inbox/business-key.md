---
type: concept
title: 업무 키
description: 업무가 정보를 식별·추적·조회하는 키 — 유일성·불변성 요건과 대리 키와의 구분
status: draft
generated: { by: "claude-fable-5", at: "2026-08-06T15:30:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# 업무 키

업무 키(business key)는 업무가 정보를 식별·추적·조회(identify, track, locate)
하는 데 실제로 쓰는 키다 — 고객 번호, 송장 번호, 차대번호(VIN) 같은 것들이다.
[Data Vault](data-vault-modeling.md)에서는 [Hub](data-vault-hub.md)가 이 키를
모델의 축으로 삼는다 (§4.3.1, pp.114–115).[^linstedt2016]

## 요건

- 정의상 요건 둘: **변경 성향이 매우 낮을 것, 유일할 것.**[^linstedt2016]

> By definition, a business key should have a very low propensity to change
> and should be unique.

- 유일성의 범위는 운영 시스템 하나다 — 다른 운영 시스템에 같은 값의 키를 가진
  다른 업무 객체가 있을 수는 있다 (§4.3.1, pp.114–115).[^linstedt2016]
- 유일성이 실제로 깨진 사례: 어느 기타 제조사의 시리얼 규칙은 연도 끝자리가
  같은 해(1996/2006)에 중복을 허용했다 — 이런 경우 시리얼+생산연도의 복합이
  진짜 업무 키다 (§4.3.1, pp.114–115).[^linstedt2016]

## 복합 키와 스마트 키

- 복합 키(composite key)는 여러 열의 유일 조합, 스마트 키(smart key)는 부분
  의미들이 한 열에 합쳐진 키다 — VIN은 제조사(WMI)·차종(VDS)·개체(VIS)가 한
  값에 인코딩된 스마트 키다. 바코드(UPC/EAN)·IMEI·MAC·ISBN이 같은 부류다 (§4.3.1.1, pp.115–116).[^linstedt2016]

## 범위(scope)

- 업무 키에는 유효 범위가 있다: 전역 유일(VIN) ⊃ 조직 전체 유일 ⊃ 애플리케이션
  한정(업무 키 또는 대리 키). 범위가 클수록 업무 객체를 잘 대표하므로, 맥락에서
  가장 넓은 범위의 식별자를 고른다 (§4.3.1.3, pp.116–118).[^linstedt2016]

## 대리 키와의 구분

- 대리 키(surrogate key)는 조인 성능을 위한 무의미한 기술 식별자다. 그러나
  **업무가 대리 키로 객체를 식별·추적하기 시작하는 순간 그것은 업무 키가 된다**
  — 화면과 보고서에 노출된 대리 키가 그 예다 (§4.3.1.4, p.118).[^linstedt2016]

## 식별 절차

- 분석가의 핵심 질문 하나: "정보를 어떻게 식별·추적·조회하십니까?" 원천
  화면의 조회 필드·보고서 헤더·업무 프로세스 분석·데이터 모델의 유일 인덱스가
  업무 키의 발견 지점이다 (§4.3.1.2, p.116).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"

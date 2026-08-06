---
type: concept
title: Data Vault Satellite
description: 업무 키·관계의 맥락과 전체 변경 이력을 담는 엔티티 — 단일 부모·분할 규칙·불변 이력
status: draft
generated: { by: "claude-fable-5", at: "2026-08-06T15:30:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Satellite

Satellite는 [Hub](data-vault-hub.md)나 [Link](data-vault-link.md)에 맥락
(context) — 업무 객체·관계·트랜잭션을 서술하는 속성 — 을 붙이고 그 변경
이력을 추적하는 [Data Vault](data-vault-modeling.md) 엔티티다 (§4.5, pp.133–135).[^linstedt2016]

> Satellites store all data that describes a business object, relationship,
> or transaction.

## 구조 제약

- Satellite의 부모는 **정확히 하나**(Hub 하나 또는 Link 하나)이고, 다른
  테이블의 부모가 될 수 없다(눈송이화 금지). 그래서 자체 해시 키를 만들지
  않으며, 식별은 부모 해시 키 + Load Date의 조합이다 (§4.5, pp.133–135).[^linstedt2016]
- 변경이 있는 원천 레코드만 새 엔트리로 쌓는 델타 구동이다 — 차원 모델링의
  Type II 디멘전에 비견된다 (§4.5.1, pp.135–136).[^linstedt2016]
- 원천 포착이 목적이므로 서술 속성의 데이터 타입은 원천에 최대한 가깝게 두고
  NULL도 그대로 담는다 (§4.5, pp.133–135).[^linstedt2016]

## 이력은 불변이다

- 웨어하우스는 이력이 보관되는 유일한 장소(system of record)가 되므로,
  Satellite의 데이터는 갱신·수정이 금지된다. 유일한 예외는 이전 버전의
  **Load End Date** 갱신뿐이다 (§4.5.1, pp.135–136).[^linstedt2016]
- 구조를 재설계할 때도 기존 이력의 100%를 보존해야 감사를 통과한다 (§4.5.1, pp.135–136).[^linstedt2016]

## 분할 규칙 — 한 덩어리로 두지 않는다

권장은 1차로 **원천 시스템별**, 2차로 **변경 빈도별** 분할이다 (§4.5.2, p.136).[^linstedt2016]

- 원천별 분할의 이점: 기존 엔티티 무변경으로 새 원천 추가, 원천 데이터 무가공
  보존, 시스템별 감사 추적, 적재 병렬성 극대화(대상 경합 없음), 실시간 데이터의
  독립 통합 (§4.5.2.1, p.136).[^linstedt2016]
- 변경 빈도별 분할: 자주 변하는 속성(비행 마일리지)과 거의 안 변하는 속성
  (좌석 수)을 한 Satellite에 두면, 잦은 변경마다 안 변한 속성까지 새 레코드로
  복제된다 — 빈도 그룹별로 나눈다 (§4.5.2.2, p.137).[^linstedt2016]

## 메타데이터 속성

- 필수: 부모 해시 키 + Load Date(PK), Load End Date, Record Source.
  선택: Hash Diff, Extract Date (§4.5.3, p.137).[^linstedt2016]
- **Load Date는 웨어하우스가 처음 본 시각**이지 원천의 타임스탬프가 아니다 —
  원천 시각은 신뢰할 수 없으므로(시간대 미상 등) 서술 속성으로만 담는다.
  예외는 과거 데이터 초기 적재뿐: 이때는 원천 추출 시점으로 소급 설정해야
  같은 날 덮어써진 변경들이 살아남는다. 원천의 생성일·계획일 등 어떤 날짜도
  load date/load end date에 넣어선 안 된다 (§4.5.3.2–5, pp.138–139).[^linstedt2016]
- **Hash Diff** — 서술 속성 전체의 해시. 행 비교를 빠르게 해 변경이 있을 때만
  새 엔트리를 만들게 한다. 델타 적재만 오는 원천에는 불필요하다 (§4.5.3.4·§4.5.4, pp.138–140).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"

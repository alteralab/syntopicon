---
type: concept
title: Data Vault Link
description: 허브 사이의 관계를 다대다로만 담는 엔티티 — 시간성 배제·입도·driving key 규칙
status: draft
generated: { by: "claude-fable-5", at: "2026-08-06T15:30:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Link

Link는 [Hub](data-vault-hub.md)들 사이의 관계·트랜잭션·계층을 담는
[Data Vault](data-vault-modeling.md) 엔티티다 (§4.4, pp.121–122).[^linstedt2016]

> Links capture and record the past, present, and future relationships
> between data elements at the lowest possible granularity.

## 다대다만 존재한다

- Link는 항상 다대다 테이블로 구현한다. 링크 하나가 1:m·m:n·m:1·1:1을 정의
  변경 없이 모두 수용하므로, 업무 규칙이 바뀌어도(예: "공항당 단일 항공사" →
  "복수 항공사") ETL 재공학이 필요 없다 — 전통 모델에서는 관계 정의 변경이
  곧 재공학이다 (§4.4.1–2, pp.124–126).[^linstedt2016]
- Link에는 시간성(temporality)을 두지 않는다 — Begin/End Date를 링크에 넣으면
  관계를 단일 타임라인에 묶어 "시작·종료가 한 번뿐"이라는 성립하지 않는 제약을
  강제하게 된다. 관계의 활성 여부는 맥락이므로 [Satellite](data-vault-satellite.md)가
  담는다. 예외는 기술·정보 목적의 Load Date뿐 (§4.4, pp.121–122).[^linstedt2016]

## 입도와 재입도 변경

- Link의 입도(granularity)는 연결한 Hub 수로 정해진다 — Hub를 하나 더 참조하면
  입도가 내려간다. [팩트 테이블](fact-table.md)에 차원을 더하는 것과 같은
  원리다 (§4.4.3, pp.128–129).[^linstedt2016]
- **운영 중인 Link 구조의 수정은 DV 2.0에서 더 이상 허용되지 않는다** — 기존
  링크에 Hub 참조를 더하면 이력 데이터를 임의 값으로 채워야 해서(원천은 NULL을
  준 적이 없다) 감사 가능성이 깨진다. 대신 옛 링크를 닫고 새 링크를 만들며,
  서로 다른 입도의 병합 방법은 업무 규칙(SQL)으로 정보 마트 쪽에서 정의한다 (§4.4.3, pp.128–129).[^linstedt2016]
- **unit-of-work**: 함께 도착한 키 집합은 함께 유지해야 한다. 링크를 정규화
  명목으로 잘게 쪼개면 재조인 시 원천에 없던 레코드가 생긴다 — 관계형 모델링의
  다치 종속(multivalued dependency) 문제다 (§4.4.4, pp.130–131).[^linstedt2016]

## 엔티티 구조

- 필수: 해시 키(연결된 모든 업무 키의 조합을 해시)·Load Date·Record Source +
  참조 Hub들의 해시 키. 선택: last seen date, 종속 자식 키 (§4.4.5, pp.131–132).[^linstedt2016]
- **종속 자식 키(dependent child key)** — 송장 라인번호처럼 홀로 서지 못하고
  다른 맥락 안에서만 유일한 퇴화 필드(degenerate field). 링크의 입도와 유일성에
  참여하므로 해시 키 계산에 포함된다 (§4.4.5.2, p.132).[^linstedt2016]
- **driving key** — 링크의 Hub 참조 중 "지속되는 대상"을 식별하는 부분 집합.
  driving key 밖의 키(예: 노선은 같은데 바뀐 항공편 번호)가 변하면 새 링크
  엔트리가 생기고, 새틀라이트의 이전 엔트리는 다음 레코드의 load date로
  end-date된다. 모델 다이어그램에는 보이지 않는 논리적 구성물이라 적재 절차에서
  구현해야 한다 (§4.5.5, pp.140–143).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"

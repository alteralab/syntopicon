---
type: concept
title: Data Vault Hub
description: 업무 키의 유일 목록을 보관하는 Data Vault의 기둥 엔티티 — 해시 키·적재 메타데이터 구조
status: draft
generated: { by: "claude-fable-5", at: "2026-08-06T15:30:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Hub

Hub는 [업무 키](business-key.md)를 모델의 나머지에서 분리해 보관하는
[Data Vault](data-vault-modeling.md)의 기둥 엔티티다 (§4.2.1, p.109).[^linstedt2016]

> The purpose of a hub entity is to store the business keys of business
> objects along with some other information, which is called the metadata.

## 정의 규칙

- Hub는 업무 키의 **유일 목록**이며, 원천 시스템의 raw 데이터를 변형하지 않고
  통합하는 연성 통합 지점(soft-integration point)이다 (§4.3, p.113).[^linstedt2016]
- 한 Hub 안의 업무 키는 **같은 의미 입도(semantic granularity)** 여야 한다 —
  개인인 담당자와 법인인 고객은 다른 Hub에 둔다 (§4.3, p.113).[^linstedt2016]
- 복합 키(composite key)를 업무가 하나로 쓰면 한 Hub 안에 함께 둔다. 한 필드로
  합치거나, 부분 필드로 나누거나, 둘 다 두는 변형이 허용된다(유일 키는 복합 키
  전체에 건다) (§4.3.2.2, p.119).[^linstedt2016]

## 엔티티 구조

모든 Hub에 공통인 속성: 해시 키(PK)·업무 키·적재 시각(load date)·레코드
소스(record source), 선택으로 최근 관측일(last seen date) (§4.3.2, p.118).[^linstedt2016]

- **해시 키** — 업무 키를 해시(MD5 권장)한 값으로, 링크·새틀라이트가 참조하는
  기본 키. DV 1.0의 시퀀스 번호를 대체했다 — NoSQL 등 외부 저장소와의 연결,
  크로스 플랫폼 호환, 재생성 가능(같은 업무 키 → 같은 해시)이 이유다. 업무
  사용자에게 노출하면 안 된다 (§4.3.2.1–2, pp.118–119).[^linstedt2016]
- **적재 시각** — 업무 키가 웨어하우스에 처음 도착한 시각. 시스템이 생성·유지
  하며, 같은 배치의 모든 데이터가 같은 값을 가져야 적재 주기가 재현·재시작
  가능해진다. 한번 설정하면 불변 (§4.3.2.3, p.119).[^linstedt2016]
- **레코드 소스** — 감사 추적용 출처 표기. "SAP" 같은 뭉뚱그림 대신 "SAP.FINANCE.GL"
  처럼 가장 낮은 입도로 적는다 (§4.3.2.4, p.120).[^linstedt2016]
- **최근 관측일** — CDC가 없는 전체 적재(full load) 원천에서 삭제를 판별하는
  장치: 배치마다 관측된 키에 날짜를 갱신하고, 임계 일수를 넘긴 키를 삭제로
  간주한다. 감사 추적·CDC가 있으면 쓰지 않는다 (§4.3.2.5, p.120).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"

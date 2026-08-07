---
type: concept
title: Data Vault Hub
description: 업무 키의 유일 목록을 보관하는 Data Vault의 기둥 엔티티 — 해시 키·적재 메타데이터 구조와 다중 원천 업무 키 통합 패턴
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault Hub

Hub는 [업무 키](../concepts/business-key.md)를 모델의 나머지에서 분리해 보관하는
[Data Vault](../concepts/data-vault-modeling.md)의 기둥 엔티티다 (§4.2.1, p.109).[^linstedt2016]

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

## 응용 — 다중 원천 업무 키 통합

- 이론상 업무 객체마다 하나의 주도 운영 시스템(leading operational system)이
  있어야 하지만, 현실의 업무 객체(예: 고객)는 CRM·이커머스·송장 관리 등 여러
  시스템에 흩어져 있다. 원천마다 업무 키를 정의하는 역량이 달라 키의 데이터
  타입까지 다를 수 있고(영숫자 vs 숫자만 허용), 업무는 시스템 간 키 매핑
  테이블에 의존하게 된다 (§5.1, pp.144–145).[^linstedt2016]
- 업무 키를 포함한 모든 데이터는 스테이징을 거쳐 먼저 Data Vault 계층에 raw로
  적재되고, 통합(consolidation)은 복잡한 업무 규칙이 처리되며 정보 마트를 만들
  때 일어난다 (§5.1, p.145).[^linstedt2016]
- 권장 관행: 포맷과 무관하게 모든 원천의 업무 키를 **하나의 공통 Hub**에
  적재하고, 같은 업무 객체를 가리키는 키들은 same-as link로 표시한다 —
  [Link 응용](data-vault-link.md) 참조 (§5.1, p.145).[^linstedt2016]
- 이 단일 Hub + same-as link 접근은 **원천들의 번호 범위가 겹치지 않을 때만**
  성립한다. 같은 키 값이 시스템마다 다른 객체를 식별하면 두 대안뿐이다:
  (1) 원천 시스템 식별자를 복합 업무 키에 추가한다 — 단 원천 통합 효과는 잃는다.
  (2) Hub를 원천별로 나누고 링크로 연결한다 — 키 용법 차이가 모델에 문서화되지만
  Raw Data Vault의 엔티티가 늘어난다. 둘 다 모델링 관점에선 차선이지만, 원천이
  차선으로 운영되는 현실을 반영하는 것이므로 올바른 접근이다 (§5.1.1, p.148).[^linstedt2016]
- **Business Vault용 특수 Hub 엔티티는 없다.** 다만 통합된 키 목록을 요구하는
  조회가 많고 그 질의가 복잡하다면, 통합 결과를 담은 물질화(materialized) Hub를
  Business Vault에 두는 것이 합리적이다 — 구조는 Raw Data Vault의 Hub와 같고
  데이터만 다르며, 레코드 소스는 시스템 생성임을 나타내는 "SYSTEM"/"SYS"로
  적는다 (§5.1.1, p.148).[^linstedt2016]
- 여러 원천의 키를 하나의 business hub로 병합할 때 키들은 겹치지 않고 각각
  하나의 업무 객체만 식별해야 한다. 주도 시스템 밖에서 온 키는 접두/접미
  표기로 구분한다 — 괄호로 감싸거나("(4711)") 원천 표기를 붙여("(TCK:4711)")
  업무 사용자가 주도 시스템에 없는 키임을 알아보게 한다 (§5.1.1, p.148).[^linstedt2016]
- 업무 규칙은 보통 정보 마트 적재 때 구현하지만, **리포트의 80% 이상에서
  공용되거나 heavy lifting(장시간·복잡 규칙)이 필요하면 Business Vault에서
  구현**해 마트마다의 재구현을 피한다 — 위 통합 Hub가 전형적 사례다 (§5.1.1, pp.148–149).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"·5장 "Intermediate Data Vault Modeling"

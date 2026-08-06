---
type: concept
title: Data Vault 모델링
description: business key 중심의 3-엔티티(Hub·Link·Satellite) 데이터 웨어하우스 모델
status: draft
generated: { by: "claude-fable-5", at: "2026-08-06T15:30:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault 모델링

Data Vault는 1990년대 Dan Linstedt가 만든 데이터 웨어하우스 모델로, 자연에서
관찰되는 척도 없는 네트워크(scale-free network)를 지향한다 — 허브에 새 연결을
더하는 방식으로 확장이 쉬운 구조다 (§4.1, pp.107–108).[^linstedt2016]

## 왜 business key 중심인가

- 모델 전체가 업무 키(business key)를 축으로 선다 — 업무가 일상 운영에서 정보를
  통합·연결·접근하는 방식 그대로를 모델이 물려받기 위해서다 (§4.2, p.108).[^linstedt2016]
- 모델이 지원하려는 업무 특성: 민첩성(agility)·통합(integration)·복잡성 대응·
  유연성·투명성과 감사 가능성(accountability)·맞춤 보고·확장(scale) (§4.2, p.108).[^linstedt2016]

## 세 가지 기본 엔티티

역할 분담이 모델의 뼈대다 (§4.2, pp.108–109):[^linstedt2016]

> the **hub** separates the business keys from the rest of the model; the
> **link** stores relationships between business keys (and/or hubs); and
> **satellites** store the context (the attributes of a business key or
> relationship).

- [Hub](data-vault-hub.md) — 업무 키를 모델의 나머지에서 분리해 보관한다.
- [Link](data-vault-link.md) — 업무 키(허브)들 사이의 관계·트랜잭션을 담는다.
- [Satellite](data-vault-satellite.md) — 업무 키·관계의 맥락(속성)과 그 변경
  이력을 담는다.
- 링크가 트랜잭션을 표현할 때가 많아 [차원 모델](dimensional-modeling.md)의
  [팩트(fact)](fact-table.md)를 만드는 기반이
  되곤 하지만, 이는 경험칙일 뿐이다 — 비트랜잭션 링크(예: 공항 간 연결 존재)도
  정상적인 모델이다 (§4.2.2, p.109).[^linstedt2016]
- 확장은 기존 모델 무변경으로 이뤄진다: 새 정보가 필요하면 새 허브를 만들고
  링크로 기존 허브에 연결한다. 기존 ETL은 리팩터링이 필요 없다 (§4.4.2, pp.126–127).[^linstedt2016]

이 장의 논리 표기는 Visual Data Vault(visualdatavault.com)를 쓴다 (p.106).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 4장 "Data Vault 2.0 Modeling"

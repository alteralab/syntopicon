---
type: concept
title: Business Vault
description: soft business rule의 중간 결과를 재사용 가능하게 저장하는 Raw Data Vault와 정보 마트 사이의 계층 — computed satellite·탐색 링크·SAL·PIT·Bridge가 여기 속하며, 감사 대상이 아니라 언제든 재적재할 수 있다
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Business Vault

하나의 질문: **soft business rule의 적용 결과는 어디에 두나.**

Raw Data Vault는 원천 데이터를 무수정 보존하고, 정보 마트는 비즈니스 사용자가 소비할 최종 형태를 제공한다. 그 사이에서 규칙 적용의 **중간 결과**를 담는 계층이 Business Vault다.

## 정의와 위치

> The Business Vault serves as an intermediate between the Raw Data Vault and information marts. By doing so, it stores intermediate results from processed (soft) business rules that are stored for reusability. (§14.1, p.621)[^linstedt2016]

- Raw Data Vault와의 경계는 규칙의 종류다: 원시 데이터는 데이터 웨어하우스로 들어오는 길에 "어떤 의미로도 수정·변환·수선되지 않고" 보존되며 (§13.3, p.572),[^linstedt2016] 자주 바뀌는 soft business rule — 데이터 품질 루틴을 포함해 — 은 Business Vault나 정보 마트 적재 과정에 구현된다. 그래서 규칙이 바뀌어도 원시 데이터 재적재 없이 루틴만 조정하면 된다 (§13.4, pp.572–573).[^linstedt2016] 품질 루틴이 왜 soft rule인지는 data-quality-management.md 참조.
- 정보 마트로 가는 중간층으로서의 존재 이유는 **재사용**이다: 교정·변환 결과를 Business Vault에 두면 여러 정보 마트가 같은 결과를 공유한다. "고품질"의 상이 소비자마다 달라 마트를 여럿 둘 때 특히 유효하다 (§13.4, p.573).[^linstedt2016] 다만 필수 경유지는 아니어서, 결과를 (가상화든 구체화든) 대상 정보 마트에 직접 적재하는 것도 유효하다 (§13.4, p.573).[^linstedt2016]
- Business Vault는 목표가 아니라 중간 단계일 뿐이다 — 궁극의 목표는 비즈니스 사용자가 쓸 정보 마트를 짓는 것이다 (§14.2, p.637).[^linstedt2016] information-mart.md 참조.

## 감사 불가, 그래서 재적재 가능

- Raw Data Vault와 달리 Business Vault의 데이터는 시스템이 계산한 것이므로 감사 가능성(auditability)을 주장할 수 없고, 대신 언제든 버리고 다시 만들 수 있다. 탐색 링크 재적재를 두고 저자들은 대상 테이블을 먼저 비우는(truncate) 방식이 "감사 관점에서 완전히 유효하다"고 말한다 — Business Vault 테이블은 어느 시점에든 재적재될 수 있기 때문이다 (§14.1.2, p.637).[^linstedt2016]
- 같은 이유로 SAL(Same-As 링크)도 대부분 매 실행 전체 재적재가 증분 갱신보다 낫다 (§13.9.1, p.618).[^linstedt2016]
- 운영상 특징: Raw Data Vault 적재는 정형화된 템플릿(11–12장)을 따르지만, Business Vault 엔터티 적재는 대부분 개별 프로세스여서 자동화하기 어렵다 (§13.9.1 앞, p.602).[^linstedt2016]

## 구성 엔터티

### Computed satellite

- soft business rule 구현의 대표 산물로, 데이터 품질 클렌징에도 많이 쓰인다. 많은 경우 SQL 뷰로 **가상 제공**된다 — 원본 새틀라이트를 SELECT하며 파생 컬럼(예: 거리의 단위 환산, 속도 계산)이나 참조 테이블 조인 결과를 덧붙이는 식이다 (§14.1.1, p.622; §13.6.1, p.577).[^linstedt2016] 새틀라이트 일반은 ../concepts/data-vault-satellite.md 참조.
- record source 규약: computed satellite가 데이터를 바꿨다면 원천 시스템 식별자 대신 **soft rule의 식별자**를 record source로 쓴다. 어떤 규칙이 그 데이터를 만들었는지 추적하기 위해서다. 값을 바꾸지 않고 필터만 했다면 원래 record source를 유지한다 (§14.1.1, pp.622–623).[^linstedt2016]
- 가상화(뷰)의 장점: 구현이 단순·이해 가능(soft rule 정의당 구현 하나), 개발이 빠름, 배포가 빠름 — 애자일한 Data Vault 2.0 방법론과 맞물릴 때 특히 유효하다. 단점: 규칙이 너무 복잡하면 SQL 한 문장으로 못 담아 여러 엔터티로 쪼개거나 ETL로 구현해야 하고, 계산·조인이 많으면 성능 때문에 구체화가 낫다 (§14.1.1, p.623).[^linstedt2016]

### 탐색 링크(exploration link)

- 가상화가 불가능한 경우가 있다 — 외부 도구(예: 데이터 마이닝)가 원시 데이터로부터 계산한 산출물이 소스에 존재하지 않을 때다. 탐색 링크는 소스 시스템에 없는, **인위적으로 생성된 링크**를 담는 엔터티다. 연관 규칙(association rule) 알고리즘(Apriori, FP Growth 등)으로 채우는 것이 한 방법이다 (§14.1.2, p.623).[^linstedt2016] 링크 일반은 ../concepts/data-vault-link.md 참조.
- 예: 항공사의 현재 취항 노선으로부터 "추가로 취항할 만한 목적지"를 추천하는 모델의 출력을 링크로 저장. 모델의 빈발 패턴이 시간에 따라 변하므로 주·월 단위로 재실행하며, 갱신 대신 truncate 후 재적재한다 (§14.1.2, pp.623, 636–637).[^linstedt2016]

### SAL, PIT, Bridge

- 중복 식별자 해소용 **Same-As 링크(SAL)** 는 Business Vault 스키마에 만든다 — 마스터/중복 해시 키 쌍과 유사도 점수를 담고, 중복 제거된 차원의 소스가 된다 (§13.9.1, p.604; §13.10, pp.618–619).[^linstedt2016] 상세는 data-quality-management.md 참조.
- **PIT 테이블과 Bridge 테이블**도 시스템 생성 엔터티로 Business Vault에 속한다. 목적은 규칙 적용이 아니라 질의 성능 — 다중 새틀라이트의 시점 정렬(PIT)과 허브·링크 횡단 지름길(Bridge)로 정보 마트 전개(특히 가상화 마트)의 조인 비용을 흡수한다. point-in-time-and-bridge-tables.md 참조.
- 수동 지시 교정(자동 교정 + 사람 검토)의 결과물처럼 신뢰도·검토 결과를 함께 저장해야 하는 클렌징 데이터도 Business Vault에 구체화된다 (§13.8, p.580).[^linstedt2016]

## 건너뛴 것

- 탐색 링크를 채우는 SQL Server Analysis Services 데이터 마이닝 모델 생성·훈련(DMX)과 SSIS 데이터 플로 구축 절차(§14.1.2의 화면 단계) — 도구 절차라 개념만 추출했다.
- DQS 기반 computed satellite 적재 절차(§13.8.2–13.8.3) — data-quality-management.md에서 같은 이유로 제외.

[^linstedt2016]: Linstedt & Olschimke 2016, 13장 "Implementing Data Quality"·14장 "Loading the Dimensional Information Mart"

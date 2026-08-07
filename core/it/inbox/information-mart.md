---
type: concept
title: 정보 마트
description: Raw/Business Vault에서 차원 모델(차원·팩트 테이블)로 전개되는 소비 계층 — 허브+새틀라이트 조인으로 차원을 짓고, 소비자별로 여러 마트를 두며, 물질화와 가상화(뷰)를 규칙 복잡도·성능으로 가른다
status: draft
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# 정보 마트

하나의 질문: **Data Vault에서 비즈니스 사용자가 쓸 차원 모델을 어떻게 전개하나.**

Data Vault 2.0에서 정보 마트(information mart)는 소비 계층이다 — Raw Data Vault(원형 보존)와 Business Vault(soft rule 중간 결과)로부터 차원 모델을 전개해 비즈니스 사용자에게 제공한다. 궁극의 목표는 이 마트를 짓는 것이고, Business Vault는 그 중간 단계일 뿐이다 (§14.2, p.637).[^linstedt2016] 차원 모델 일반은 ../concepts/dimensional-modeling.md, 중간층은 business-vault.md 참조.

## 소비자마다 마트 하나

- 정보 마트는 하나가 아니다. "고품질 데이터"의 상이 소비자마다 다르기 때문이다 — 전사 합의된 교정을 원하는 소비자, 자기만의 교정 기준을 가진 소비자, 오류 데이터 자체를 분석하려는 소비자를 **각각의 마트**로 만족시킨다. 그래서 교정 루틴은 가능하면 Business Vault에 두어 여러 마트가 재사용하게 한다 (§13.4, p.573).[^linstedt2016]
- 정보 마트의 데이터는 원시 데이터가 아니라 "변경·매칭·통합된 정보"다 — 원형은 Raw Data Vault에 남아 있으므로, 마트의 교정 규칙이 바뀌어도 재적재 없이 다시 전개하면 된다 (§13.3–13.4, pp.572–573).[^linstedt2016] 왜 원형을 보존하는지는 data-quality-management.md 참조.

## 차원 전개

### Type 1 차원: 해시 키를 그대로 차원 키로

- Type 1 차원(이력 없이 최신 서술만 유지)은 허브의 해시 키를 그대로 차원 테이블의 키로 쓴다. 시퀀스 번호 대신 해시 키를 쓰면 키가 이미 Data Vault 2.0 모델에 있으므로 차원 제공이 쉬워진다 (§14.2.1, p.637).[^linstedt2016] 차원 테이블 일반은 ../concepts/dimension-table.md 참조.
- 적재는 TRUNCATE 후 INSERT 전체 재적재가 단순하다(갱신 처리를 피한다). 멤버가 적으면 MERGE도 선택지다 (§14.2.1, p.638).[^linstedt2016]
- 전개의 기본형이 여기서 드러난다:

> many if not most dimensions are built by querying the data from a hub and joining descriptive data from one or more satellites. (§14.2.1, p.638)[^linstedt2016]

- 새틀라이트마다 소스 시스템이 다를 수 있으므로, 어느 새틀라이트가 주도 시스템(leading system)인지 정하는 것은 차원 적재 안의 비즈니스 로직이다. Type 1은 최신 레코드만 취하도록 WHERE로 유효 레코드를 거르고, 삭제된 멤버를 빼려면 effectivity satellite를 조인해 필터한다 (§14.2.1, p.638).[^linstedt2016]
- 차원 테이블을 지을 때 첫 단계는 대상 grain을 제공하는 테이블(집합)의 식별이다. 경험상 차원의 grain은 80%의 경우 허브에서 온다. 나머지 전형은 중복 제거의 산물인 Same-As 링크다 (§14.2.1, p.638)[^linstedt2016] — SAL 기반 차원은 data-quality-management.md 참조.
- 서술 데이터가 일부 새틀라이트에만 있는 멤버 때문에 LEFT JOIN + COALESCE가 필요해져 문장이 복잡해진다. PIT 테이블과 고스트 레코드를 쓰면 INNER 동등 조인으로 바꿀 수 있다 (§14.2.1, p.638)[^linstedt2016] — point-in-time-and-bridge-tables.md 참조.

### Type 2 차원: 키를 비즈니스 키 + 날짜로 계산

- Type 2 차원(버전 이력 유지)에서는 키를 허브 해시 키에서 직접 가져올 수 없다 — 행마다 고유 키가 필요하므로 **비즈니스 키 + 날짜(적재 시각 또는 스냅샷 날짜)** 로 해시를 계산한다. 멤버 식별용 해시 키와 버전 식별용 적재 시각 컬럼을 별도로 유지해 팩트 적재 때 조인에 쓴다 (§14.2.2, p.639).[^linstedt2016]
- 적재 grain은 허브가 아니라 새틀라이트들에서 온다 — 허브에 매달린 모든 새틀라이트의 (해시 키, 적재 시각) 조합이 잠재 버전이고, 대상에 없는 조합만 증분 적재한다. 조인 조건이 Type 1보다 훨씬 복잡해지고 이는 SQL 옵티마이저 관점에서도 부담이다 (§14.2.2, p.640).[^linstedt2016]
- 주의: 새틀라이트들이 독립적으로 변하므로 이 소박한 방식은 내용이 같은 버전 두 개를 만들 수 있다(부 새틀라이트만 바뀐 경우). 마트나 하류 OLAP 큐브 기술에 따라 문제가 될 수 있다 (§14.2.2, p.641).[^linstedt2016] 적재 후에는 새틀라이트 종료일 처리와 같은 요령으로 load end date를 갱신한다 (§14.2.2, p.641).[^linstedt2016]

### 팩트 테이블

- 팩트 테이블의 기본 키는 별도 키가 아니라 grain을 정의하는 차원 키들(해시 값)의 조합이다 — 다른 테이블이 팩트에 의존하지 않기 때문이다 (§14.2.3, p.643).[^linstedt2016] 팩트 일반은 ../concepts/fact-table.md 참조.
- 팩트는 트랜잭션 grain의 링크(무이력 링크)에서 적재한다. Type 1 차원 참조는 허브 해시 키를 그대로 쓰면 되지만, Type 2 차원 참조는 차원 적재와 같은 식(비즈니스 키 + 적재 시각)으로 키를 재계산해야 한다 (§14.2.3, p.645).[^linstedt2016]
- 대안으로 마트의 차원을 조회(lookup)해 키를 얻을 수도 있으나, 적재 프로세스 간 불필요한 의존을 만들어 병렬화를 해치므로 피해야 한다 (§14.2.3, p.645).[^linstedt2016]
- 차원과의 조인을 INNER JOIN으로 유지하려면 차원에 **unknown 레코드**(0으로 채운 키)를 넣어 NULL 참조를 대체해야 한다 — 이 레코드가 없으면 마트의 정합성이 깨진다 (§14.2.3, pp.645–647).[^linstedt2016]
- grain을 바꾼 집계 팩트 테이블도 같은 요령으로 적재한다 — 소스 grain의 참조 일부를 제거하고 측정값을 합산해 담는다 (§14.2.4, p.648).[^linstedt2016]

## 물질화 vs 가상화

- 전개 형태는 둘이다: 결과를 테이블로 **물질화(materialization)** 하거나 SQL 뷰로 **가상화(virtualization)** 한다. 교정·변환 결과는 Business Vault를 거치든 안 거치든 두 형태 모두로 정보 마트에 제공될 수 있다 (§13.5, p.574; §13.4, p.573).[^linstedt2016]
- 가상화 쪽 판단 기준 (§14.1.1, p.623):[^linstedt2016]
  - 장점: 구현이 단순·이해 가능(규칙 정의당 뷰 하나), 개발 빠름, 배포 빠름 — 애자일 반복과 맞는다.
  - 한계: 규칙이 SQL 한 문장에 담기 어려울 만큼 복잡하면 쪼개거나 ETL로 물질화해야 하고, 계산·조인이 많아 연산력이 부족하면 물질화가 낫다.
- 규칙 실행에 사람 개입이나 외부 도구가 끼면 가상화가 아예 불가능하다: 수동 지시 교정 결과(신뢰도·검토 결과 동반)는 물질화가 필수이고 (§13.8, p.580),[^linstedt2016] 데이터 마이닝 산출물처럼 소스에 없는 데이터도 저장할 수밖에 없다 (§14.1.2, p.623).[^linstedt2016]
- 가상화 마트의 성능은 Business Vault의 질의 보조 테이블이 떠받친다 — 비싼 계산을 Bridge에 미리 실어두면 뷰 접근이 극적으로 빨라진다. point-in-time-and-bridge-tables.md 참조.
- 물질화한 마트도 원본이 아니라는 점은 같다: 원형은 Raw Data Vault에 있으므로 마트는 언제든 버리고 다시 전개할 수 있다. Type 1 차원·탐색 링크의 truncate-후-재적재 관행이 그 표현이다 (§14.2.1, p.638; §14.1.2, p.637).[^linstedt2016]

## 건너뛴 것

- Type 1/2 차원·팩트·집계 팩트의 T-SQL 적재문 전문과 해시 계산식(§14.2의 DDL/INSERT 코드) — 규칙과 트레이드오프만 추출했다.
- §14.3 이후(PIT/Bridge를 이용한 적재 최적화, 참조 데이터 처리, 해시 키 논의) — 배정 범위(§14.1–14.2) 밖이고, PIT/Bridge 개념은 point-in-time-and-bridge-tables.md가 다룬다.

[^linstedt2016]: Linstedt & Olschimke 2016, 14장 "Loading the Dimensional Information Mart"(§13.4–13.5, §13.8 일부 병용, 13장 "Implementing Data Quality")

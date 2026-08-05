---
type: concept
title: 데이터 통합 딜레마
description: 애플리케이션 사이에서 변환을 피할 수 없는 이유
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 데이터 통합 딜레마

"통합 도구를 잘 고르면 변환을 없앨 수 있는가"에 대한 답은 아니오다. 데이터 통합
딜레마(data integration dilemma)는 **애플리케이션마다 맥락이 고유하므로 데이터를
옮길 때 변환이 항상 필요하다**는 사실을 가리킨다.

## 전제

- 모든 애플리케이션은 어떤 형태로든 데이터 저장소를 갖는다. 상태 없는 애플리케이션,
  데이터베이스를 공유하는 애플리케이션, 인메모리 처리가 있어도 결국 어딘가에는
  저장한다 (2장 Application Design Starting Points, p.26).[^strengholt2023-dms]
- **애플리케이션은 언제나 고유하다.** 개념 → 논리 데이터 모델 → 물리 데이터 모델로
  내려오는 설계 과정 자체가 각 업무 문제의 고유한 지식 영역에서 출발하기 때문이다
  (2장 Application Design Starting Points, p.26).[^strengholt2023-dms]

## 귀결

- 그래서 이동에는 항상 변환이 따른다 — ETL이든 ELT든, 가상이든 물리든, 배치든
  실시간이든, 설계나 아키텍처 종류와 무관하다
  (2장 Application Design Starting Points, p.27).[^strengholt2023-dms]

> A data transformation is always required when moving data across applications,
> regardless of the design or type of architecture.

## 애플리케이션 역할

- 애플리케이션은 데이터 제공자(data provider)이거나 소비자(data consumer)이며,
  때로는 둘 다다. 자명해 보이지만 책임 소재를 가리는 데 필요한 구분이다
  (2장 Application Roles, p.27).[^strengholt2023-dms]
- 데이터 커뮤니티에서 쓰는 `source system–aligned`/`consumer-aligned domain`은 같은
  역할 구분을 **애플리케이션이 아니라 도메인 관점**의 입도로 말한 것이다
  (2장 Application Roles, p.27).[^strengholt2023-dms]
- 이 역할 구분은 외부 당사자에게도 적용된다. 다만 외부는 통제되지 않는 환경이라
  추가 보안 조치가 따른다 (2장 Application Roles, p.28).[^strengholt2023-dms]
- 외부 데이터를 직접 소비할지 추상화 계층을 둘지는 **그 외부 당사자가 우리 원칙에
  맞춰 줄 수 있는지**로 갈린다. 중재가 보장되지 않으면 계층을 둔다
  (2장 Application Roles, p.28).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

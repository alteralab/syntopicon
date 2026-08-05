---
type: concept
title: 공유 역량의 데이터 소유권
description: 하나의 시스템을 여러 도메인이 쓸 때 데이터는 누가 소유하는가
status: draft
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 공유 역량의 데이터 소유권

도메인별 데이터 소유는 경계가 깔끔할 때 성립한다. 문제는 **하나의 시스템이 여러
도메인에 걸칠 때**이고, 저자는 이것이 예외가 아니라 거의 확실히 마주치는 상황이라고
본다 — ERP·SCM·CRM이 전통적으로 여러 도메인을 가로지르는 모놀리식 성격이기
때문이다. 그래서 **초반에 풀어야 할 문제**로 지목한다
(2장 Shared capabilities, p.43).[^strengholt2023-dms]

## 두 가지 다른 얽힘

- **공유 역량(shared capability)** — 하나의 비즈니스 역량이 여러 사업 라인에 중앙
  as-a-service로 제공되는 경우. 예: 아시아·유럽 사업부가 같은 고객 관리 시스템을 쓴다
  (2장 Shared capabilities, p.43).[^strengholt2023-dms]
- **복합 애플리케이션(complex application)** — 반대로 하나의 애플리케이션·데이터베이스가
  **여러 비즈니스 역량**을 담당하는 경우. 벤더 업무 스위트나 레거시 모놀리스가 그렇다
  (2장 Complex applications, p.45).[^strengholt2023-dms]

둘은 겉보기에 비슷하지만 얽히는 방향이 반대다. 다만 제기되는 데이터 소유권 문제는
같다 (2장 Complex applications, p.45).[^strengholt2023-dms]

## 애플리케이션 도메인과 데이터 도메인의 분리

- 공유 관리 시스템 하나에 여러 업무 대표가 책임을 지는 상황이 생긴다. 결론은
  **애플리케이션 도메인과 데이터 도메인이 따로 있다**는 것이다. 데이터 관점에서
  도메인과 애플리케이션 경계 컨텍스트는 **항상 완벽히 정렬되지는 않는다**
  (2장 Shared capabilities, p.43).[^strengholt2023-dms]
- 도메인을 쪼갤 수 없다면 소유권을 나눈다: 기반 기술 서비스·파이프라인·컴포넌트를
  책임지는 **애플리케이션 소유자 한 명**, 데이터셋별로 메타데이터 등록·프라이버시·
  보안을 책임지는 **데이터 소유자 여러 명**
  (2장 Shared capabilities, p.44).[^strengholt2023-dms]
- 이상적으로는 역량을 소유한 팀이 애플리케이션 도메인과 정렬되어 소프트웨어 소유권과
  데이터 소유권이 함께 가는 것이다 (2장 Shared capabilities, p.44).[^strengholt2023-dms]

## 실무 기법 둘

저자가 제시하는 처리 방식 (2장 Shared capabilities, p.44):[^strengholt2023-dms]

- **데이터 제품으로 분리** — 같은 애플리케이션 도메인에서 서로 다른 데이터 도메인의
  데이터 제품 여러 개가 나온다. 고객 관리 예에서는 아시아 고객용 하나, 유럽 고객용
  하나로 나눈다.[^strengholt2023-dms]
- **데이터 제품 안에서 구분** — 애플리케이션 도메인이 소유권 구분 메타데이터를 담은
  단일 데이터 제품을 설계한다. 소유권 표시 컬럼을 두어 각 행을 특정 데이터 도메인에
  매핑하는 식이다.[^strengholt2023-dms]

일반·공유 역량의 차이는, 공유 역량에는 **단일 제공자가 있어 여러 사용 도메인과
맞춰 가며 실현 방식을 결정한다**는 데 있다 (2장 Shared capabilities,
p.44).[^strengholt2023-dms]

## 소유권에 따라오는 책임

도메인 팀이 애플리케이션과 데이터 제품을 소유한다는 것은 다음을 함께 진다는 뜻이다
(2장 Domain Ownership Responsibilities, p.55):[^strengholt2023-dms]

- 데이터 파이프라인 소유 — 수집·정제·변환[^strengholt2023-dms]
- 데이터 품질 개선, 소비자가 정한 SLA·품질 기준 준수[^strengholt2023-dms]
- 행/열 수준 필터링과 동적 마스킹을 위한 메타데이터 캡슐화 또는 예약 컬럼명 사용[^strengholt2023-dms]
- 메타데이터 관리 표준 준수 — 스키마 등록, 발견성을 위한 메타데이터 제공, 버저닝
  규칙, 데이터 속성과 업무 용어 연결, 메타데이터 무결성[^strengholt2023-dms]
- 데이터 상호운용성 표준 준수 — 프로토콜·데이터 형식·데이터 타입[^strengholt2023-dms]
- 계보 제공 — 수동이든, 소스 시스템·통합 서비스를 스캐너에 연결하든[^strengholt2023-dms]
- 데이터 공유 작업 — 접근 권한 검토, 데이터 계약 작성[^strengholt2023-dms]

이 원칙들은 **강하게도 느슨하게도 적용할 수 있다.** 임시·탐색·실험 유스케이스에서는
인터페이스가 덜 안정적이어도 되고, 안정적 프로덕션 유스케이스에서는 엄격히 따른다.
한 시스템 안에서 데이터 제품별로 강도를 섞는 것도 가능하다
(2장 Domain Ownership Responsibilities, p.55).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

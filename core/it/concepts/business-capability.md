---
type: concept
title: 비즈니스 역량
description: 문제 공간을 무엇을 기준으로 나누는가 — 도메인 경계의 출발점
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 비즈니스 역량

이 책의 핵심 주장은 **모든 것이 비즈니스 역량(business capability) 위에 세워져야
한다**는 것이다. 역량이 문제 공간을 정의하고, 그 문제 공간이 곧 아키텍처를 정의하는
도메인이 된다 (2장 Wrapping Up, p.57).[^strengholt2023-dms]

## 정의

Ulrich Homann의 정의를 저자가 그대로 인용한다 (2장 Business capabilities,
p.36):[^strengholt2023-dms]

> A business capability is a particular ability, or capacity that a business may
> possess or exchange to achieve a specific purpose or outcome. A capability describes
> what the business does (outcomes and service levels) that creates value for
> customers; for example, pay employee or ship product. A business capability
> abstracts and encapsulates the people, process/procedures, technology, and
> information into the essential building blocks needed to facilitate performance
> improvement and redesign analysis.

핵심은 역량이 **무엇(what)을 하는가**이지 어떻게(how) 하는가가 아니라는 점이다
(2장 Transitioning…, p.56).[^strengholt2023-dms]

## 가치 흐름과의 관계

- 가치 흐름(value stream)은 가치를 전달하기 위해 수행되는 행동의 집합이고, 그 각
  단계에서 비즈니스 역량이 필요하다. 둘의 관계는 **다대다**다
  (2장 Business capabilities, p.36).[^strengholt2023-dms]
- 역량은 역량 지도(capability map)라는 계층적 서술로 표현한다. 보통 Level 1·2·3을
  말하고, 각 레벨은 상위 역량의 분해다
  (2장 Business capabilities, p.37).[^strengholt2023-dms]
- 설계 원칙: 비즈니스 역량은 **고유하고, 상호 배타적이며, 전체를 망라**해야 한다 —
  중복도 겹침도 빈틈도 없어야 한다 (2장 Business capabilities,
  p.37).[^strengholt2023-dms]
- 역량 모델은 **비교적 안정적인 뷰**를 준다. 근본적 사업 목표는 잘 바뀌지 않는 반면
  그 아래 프로세스·애플리케이션·데이터는 시간에 따라 바뀌기 때문이다
  (2장 Business capabilities, p.38).[^strengholt2023-dms]

## 애플리케이션과 잇기

- 비즈니스 역량은 **업무 수준에 머물며 추상적이어야** 한다. 조직이 무엇을 하는지를
  나타내고 문제 공간을 겨냥한다 (2장 Linking business capabilities with applications,
  p.39).[^strengholt2023-dms]
- 역량이 구현되면 특정 맥락에 대한 실현체, 곧 **역량 인스턴스(capability instance)**
  가 생긴다. 그 경계 안에서 여러 애플리케이션과 컴포넌트가 함께 가치를 낸다
  (2장 Linking…, p.39).[^strengholt2023-dms]
- 이상적으로 애플리케이션은 **하나의 역량 인스턴스에만** 연결된다. 그 경계 안의
  애플리케이션 전체가 하나의 경계 컨텍스트를 이룬다
  (2장 Linking…, p.39-40).[^strengholt2023-dms]
- 역량과 역량 인스턴스의 관계는 **일대다**다. 같은 역량이 지역별로 여러 번 구현되면
  그만큼 (서브)도메인이 늘어난다 (2장 Capability realizations,
  p.42-43).[^strengholt2023-dms]
- 원칙으로 정리하면: **경계 컨텍스트는 비즈니스 역량에서 파생되어 배타적으로 매핑
  된다.** 역량이 바뀌면 경계 컨텍스트도 바뀐다
  (2장 Domain Boundaries and Granularity, p.41).[^strengholt2023-dms]

## 애플리케이션과 애플리케이션 컴포넌트

- 애플리케이션의 경계는 **보는 관점에 따라 다르다** — 코드·데이터의 번들 단위일 수도,
  가상 주소 공간일 수도, 업무 필요를 채우는 코드·데이터 전체일 수도 있다
  (2장 Application Boundaries, p.40).[^strengholt2023-dms]
- 데이터 관리에서는 두 관점을 결합한다: **애플리케이션은 추상적 논리 경계**,
  **애플리케이션 컴포넌트는 만질 수 있는 것**(Docker 컨테이너, JAR 같은 산출물)으로
  해결 공간을 겨냥한다 (2장 Application Boundaries, p.40).[^strengholt2023-dms]
- 이 결합의 효용: 애플리케이션 수준에서는 역량·제품 책임자·DevOps 팀·프로젝트를,
  컴포넌트 수준에서는 IT 제품·버전·구성 항목·계약·유지보수 계획을 잇는다
  (2장 Application Boundaries, p.40).[^strengholt2023-dms]
- 역량과 애플리케이션 아키텍처의 관계를 명시하면 **제품 소유권과 데이터 소유권이
  훨씬 잘 정렬된다** (2장 Application Boundaries, p.40-41).[^strengholt2023-dms]

## 톱다운이냐 보텀업이냐

- 전부 미리 매핑하는 목표 상태 설계는 부담이 큰 작업이라는 반론이 있고, 대안은
  새 아키텍처에 온보딩하면서 유기적으로 도메인을 식별하는 보텀업이다. 저자는
  보텀업이 초기엔 시간을 아끼지만 **나중에 복잡한 이동·재모델링을 부른다**고 보고,
  큰 붓으로 그린 뒤 시간을 두고 세부를 채우는 **양방향**을 권한다
  (2장 Strengths of business capability modeling, p.49).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

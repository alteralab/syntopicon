---
type: concept
title: 경계 컨텍스트
description: 도메인의 논리적 경계를 어디에 긋고 무엇을 강제하는가
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 경계 컨텍스트

경계 컨텍스트(bounded context)는 도메인 주도 설계(domain-driven design, DDD)의 중심
개념으로, **복잡도를 다루기 위해 도메인 해결 공간(solution space)의 논리적 경계를
긋는 장치**다. 이 책은 그것을 엔터프라이즈 데이터 관리 규모로 끌어올린다.

## 도메인·서브도메인과의 구분

- **도메인은 문제 공간(problem space)** 이다 — 지식·행동·법규·활동이 모이는 곳이고,
  구성요소 간 행위 의존인 의미적 결합(semantic coupling)이 나타나는 자리다
  (2장 Domains and Bounded Contexts, p.33).[^strengholt2023-dms]
- 서브도메인은 핵심(core)·일반(generic)·지원(supporting)으로 나뉜다. 핵심이 사업을
  고유하게 만드는 부분이고, 일반은 기성품으로 해결되며, 지원은 경쟁 우위는 없지만
  조직 운영에 필요하다 (2장 Domains and Bounded Contexts, p.33).[^strengholt2023-dms]
- **경계 컨텍스트는 해결 공간**이다 — 시스템과 애플리케이션의 설계, 즉 코드와
  데이터베이스 설계에 관한 것이다. 기술적 성격이라 여러 도메인·서브도메인에 걸칠 수
  있고, 도메인과 정렬될 수는 있지만 **정렬이 요구되지는 않는다**
  (2장 Domains and Bounded Contexts, p.33).[^strengholt2023-dms]
- 경계 컨텍스트는 다형적(polymorphic)이다 — 보는 관점과 주변에 따라 크기와 모양이
  달라지고 서로 겹칠 수 있다. 그래서 쓸 때마다 무엇을 가리키는지 명시해야 한다
  (2장 Bounded contexts, p.33).[^strengholt2023-dms]

전통적 그룹핑과 DDD의 차이는 **경계가 강제된다**는 점이다. 경계 컨텍스트는 독립적으로
진화하되 반드시 디커플링되어야 한다 (2장 Domains and Bounded Contexts,
p.34).[^strengholt2023-dms]

## 설계 원칙

저자가 제시하는 경계 컨텍스트 설계 원칙 (2장 Design Principles for Data Domains,
p.51-53):[^strengholt2023-dms]

- 데이터는 도메인이 관리하고 도메인을 통해 전달된다 — 데이터를 가장 잘 아는 사람이
  책임진다. 소유 모델은 중앙집중이 아니라 분산이다.[^strengholt2023-dms]
- 경계 컨텍스트는 **인스턴스화된 비즈니스 역량에 연결**된다. 하나의 역량 인스턴스,
  또는 그 일부의 구현을 나타낸다.[^strengholt2023-dms]
- 하나의 경계 컨텍스트에 애플리케이션이 하나일 수도 여럿일 수도 있다. 여럿이면 모두
  같은 역량 인스턴스에 가치를 내야 한다.[^strengholt2023-dms]
- 유비쿼터스 언어는 경계 컨텍스트 안에서 공유된다. 경계 컨텍스트와 개념 데이터 모델은
  **1대1**이다.[^strengholt2023-dms]
- 경계 컨텍스트는 인프라·네트워크·조직에 **무관(agnostic)** 하다. 응집은 애플리케이션
  기능·프로세스·데이터에 관한 것이다.[^strengholt2023-dms]
- 하나의 경계 컨텍스트는 하나의 팀에 속한다 — 결합점 수가 관리 가능한 선에서 유지되고
  팀원 전원이 이해할 수 있기 때문이다. (역은 아니다: 한 팀이 여러 경계 컨텍스트를
  가질 수 있다 — 2장 Transitioning…, p.57.)[^strengholt2023-dms]
- 경계는 엄격하다. **안에서는 강한 결합을 허용하되 넘어갈 때는 디커플링**한다.
  경계만 지키면 안쪽 데이터 형태는 무엇이든 좋다.[^strengholt2023-dms]
- 일반 데이터 서비스는 도메인에 무관해야 한다 — 도메인 로직과 통합 복잡도는 경계
  컨텍스트 안에 남긴다.[^strengholt2023-dms]

## 경계를 어디에 그을 것인가

- **정확한 과학이 아니라 휴리스틱을 동반한 기술(art)** 이다. 저자는 비즈니스
  아키텍처의 논리적 경계에 매핑하는 쪽을 택하지만, 조직 경계·업무 프로세스·도메인
  전문성·소프트웨어 청사진 분석도 모두 유효한 접근이라고 본다
  (2장 Domain Boundaries and Granularity, p.41).[^strengholt2023-dms]
- 경계 설정 기법으로 domain storytelling, event storming, bounded context canvas를
  권한다 (2장 Domain Boundaries and Granularity, p.41).[^strengholt2023-dms]
- DDD 모델 자체는 **응집을 어떻게 찾고 경계를 어떻게 정하는지에 대해 명시적이지
  않다** — 그래서 위 설계 원칙 목록이 필요하다
  (2장 Design Principles for Data Domains, p.51).[^strengholt2023-dms]

## 데이터 관리에 적용할 때의 한계

- DDD의 원래 용례는 소프트웨어 개발 맥락의 복잡 시스템 모델링(예: 마이크로서비스)이지
  **엔터프라이즈 데이터 모델링이 아니었다.** 데이터 관리 실무자들은 DDD를 너무
  추상적·기술적이라고 느끼는 일이 잦다 (2장 Ubiquitous language,
  p.35).[^strengholt2023-dms]
- 저자의 비유: 도메인은 내가 사는 거리이고 각 집이 서브도메인이다. 집을 둘러싼
  **울타리가 경계 컨텍스트**다. 안에서는 마음대로 하되 경계를 넘을 때는 공동
  진입로로 나가 도로 규칙을 따른다 (2장 Ubiquitous language,
  p.35).[^strengholt2023-dms]

## 데이터 메시와의 관계

- 도메인과 디커플링에 대한 이 논의는 **데이터 메시에 국한되지 않는다.** 명확한 경계선
  긋기는 어떤 데이터 관리·애플리케이션 통합 패러다임에도 보편적이다
  (2장 Wrapping Up, p.58).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

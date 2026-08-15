---
type: concept
title: 데이터 메시
status: draft
description: "중앙집중 데이터 플랫폼과 '데이터의 큰 분열'에 대한 응답으로 나온 탈중앙화 아키텍처 — 도메인 지향 데이터 소유권, 제품으로서의 데이터, 셀프서브 데이터 인프라, 연합 계산 거버넌스라는 네 구성 요소의 개관"
generated: { by: "claude-opus-5", at: "2026-08-15T18:00:00Z" }
sources:
  - { id: reis2022, resource: /it/sources/reis2022.md }
---

# 데이터 메시

하나의 질문: **중앙집중 데이터 플랫폼이 커질 때 생기는 문제를 도메인 소유권을 뒤집어 푸는
제안은 무엇을 주장하는가.**

> 이 페이지는 **개관**이다. 데이터 메시의 정본 소스는 Zhamak Dehghani의
> [*Data Mesh*](../sources/dehghani2022.md)(O'Reilly, 2022)이고, 이 KB에 스냅샷은 들어와
> 있으나 아직 추출되지 않았다. 여기 있는 것은 데이터 엔지니어링 개론이 아키텍처 유형 목록에서
> 데이터 메시에 할당한 분량뿐이며, 깊이는 그 소스를 읽을 때 채운다.

## 무엇에 대한 응답인가

- **데이터 메시(data mesh)는 중앙집중 데이터 레이크와 데이터 웨어하우스 같은 뻗어 나가는
  모놀리식 데이터 플랫폼, 그리고 지형이 운영 데이터와 분석 데이터로 갈리는 "데이터의 큰
  분열(the great divide of data)"에 대한 최근의 응답이다. 데이터 메시는 중앙집중 데이터
  아키텍처의 난제를 뒤집으려 시도하며, 도메인 주도 설계(소프트웨어 아키텍처에서 흔히 쓰이는)의
  개념을 가져와 데이터 아키텍처에 적용한다. 데이터 메시가 최근 많은 주목을 받았으므로 알아
  두어야 한다** (3장, p.109).[^reis2022]
- 그 "큰 분열"의 양쪽은 [EDW](../concepts/enterprise-data-warehouse.md)가 다루는 운영계·분석계의
  분리와 같은 경계다.

## 탈중앙화가 핵심이다

- Dehghani의 원문을 직인용한다 (3장, p.109):[^reis2022]

> In order to decentralize the monolithic data platform, we need to reverse how we think
> about data, its locality, and ownership. Instead of flowing the data from domains into
> a centrally owned data lake or platform, domains need to host and serve their domain
> datasets in an easily consumable way.

- 저자들이 요약한 대비 — **중앙집중화에서는 한 팀이 모든 도메인에서 데이터를 모으고 조직 전반의
  소비를 위해 그것을 조정하는 책임을 진다(전통적 데이터 웨어하우징의 흔한 접근이다). 데이터
  메시에서는 각 소프트웨어 팀이 조직의 나머지에서 소비될 수 있도록 자기 데이터를 준비하는 책임을
  진다** (3장, p.94).[^reis2022] 그 결합도 논의의 맥락은
  [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)의 도메인 결합 절에 있다.

## 네 구성 요소

- Dehghani가 나중에 식별한 데이터 메시의 핵심 구성 요소는 넷이다 (3장, p.109):[^reis2022]
  - **도메인 지향 탈중앙 데이터 소유권과 아키텍처** (domain-oriented decentralized data
    ownership and architecture)
  - **제품으로서의 데이터** (data as a product)
  - **플랫폼으로서의 셀프서브 데이터 인프라** (self-serve data infrastructure as a platform)
  - **연합 계산 거버넌스** (federated computational governance)

## 이어지는 페이지

- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 도메인 결합과
  중앙집중화라는 대안이 놓이는 자리
- [EDW](../concepts/enterprise-data-warehouse.md) — 데이터 메시가 뒤집으려는 중앙집중 모델
- [데이터 레이크](../concepts/data-lake.md) — 같은 모놀리스 문제의 다른 판본
- [데이터 아키텍처의 정의](../concepts/data-architecture-defined.md) — 이것이 한 유형으로
  세어지는 목록

[^reis2022]: Reis & Housley 2022, 3장 "Designing Good Data Architecture"

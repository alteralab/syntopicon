---
type: concept
title: 유비쿼터스 언어
description: 경계 안에서 용어를 누가 정하고, 왜 전사 통일이 아닌가
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 유비쿼터스 언어

유비쿼터스 언어(ubiquitous language)는 DDD에서 **개발자와 사용자가 함께 쌓아 공유하는
공통의 엄밀한 언어**다. 특정 관심 영역의 사람들이 쓰는 정의·어휘·전문용어의 공유
집합에 해당한다 (2장 Ubiquitous language, p.34).[^strengholt2023-dms]

## 전사 통일 언어가 아니다

- 팀 간 과도한 교차 소통과 용어 불일치를 막기 위해 쓰이지만, **전사에 하나의 통일된
  언어가 반드시 있어야 하는 것은 아니다** — 겹치는 부분이 있을 수는 있다
  (2장 Ubiquitous language, p.34).[^strengholt2023-dms]
- DDD에서 각 경계 컨텍스트는 **자기 유비쿼터스 언어를 갖는다.** 경계 컨텍스트가
  바뀌면 언어도 바뀐다 (2장 Ubiquitous language, p.34).[^strengholt2023-dms]
- 그래서 새 아키텍처에서 전사 언어는 통일된 하나가 아니라 **여러 유비쿼터스 언어의
  모음**이 된다 (2장 Design Principles for Data Domains, p.51).[^strengholt2023-dms]

이것이 데이터 웨어하우스식 사일로 접근과 갈리는 지점이다. 그쪽은 전사 언어로 고도로
통합된 환경에 데이터를 모은다 (2장 Design Principles…, p.51).[^strengholt2023-dms]

## 경계 컨텍스트와의 결합

- 한 경계 컨텍스트 안에 속하는 애플리케이션·컴포넌트는 **모두 같은 언어를 써야 한다**
  (2장 Ubiquitous language, p.34).[^strengholt2023-dms]
- 경계 컨텍스트가 팀이 이해하기 어려울 만큼 커지면 더 작게 쪼갤 수 있다
  (2장 Ubiquitous language, p.34).[^strengholt2023-dms]
- 데이터가 도메인 맥락에 정렬되면 **언어를 자동으로 상속**한다 — 같은 도메인의
  이해관계자와 설계자가 합의한 형식화된 언어다
  (2장 Data Domains, p.42).[^strengholt2023-dms]
- 데이터 제공자로 행동하는 경계 컨텍스트는 **자기 유비쿼터스 언어로 데이터를 노출**
  한다. 다른 도메인의 업무 로직을 자기 도메인에 끌어들이지 않는다는 뜻이다
  (2장 Best Practices for Data Providers, p.54).[^strengholt2023-dms]

## 문화 비유

저자는 경계 컨텍스트를 문화에 빗댄다 — 팀마다 정의와 용어가 같지 않고, 맥락은 각자
아는 것에 기반한다. 각 경계 컨텍스트는 목적도 배경도, 무엇보다 **문화가 다르고**,
문화는 우리가 생각하고 설계하고 모델링하는 방식에 영향을 준다. 문화 안에 하위문화가
있듯 경계 컨텍스트도 더 작게 나뉜다 (2장 Ubiquitous language,
p.35).[^strengholt2023-dms]

## 형식화

- 업무 용어와 정의를 **데이터 카탈로그에 저장**하는 것이 언어를 형식화하는 흔한
  방법이다 (2장 각주 11, p.42).[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

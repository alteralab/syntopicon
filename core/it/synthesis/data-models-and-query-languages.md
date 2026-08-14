---
type: synthesis
title: 데이터 모델과 질의 언어
description: 애플리케이션 데이터를 무엇으로 표현하고 무엇으로 질의하는가를 모으는 허브 — 관계형과 문서, 그래프와 트리플, 이벤트 로그, 데이터프레임, 그리고 각 모델에 말을 거는 언어들
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
---

# 데이터 모델과 질의 언어

같은 데이터를 표현하는 방법은 여럿이고, 어느 것도 모든 질의에 좋지 않다. 각 페이지가 한 모델의
표현력과 그것이 어색해지는 자리를 맡는다.

## 층과 언어

- [데이터 모델의 층](../concepts/data-model-layers.md) — 데이터 모델이 층으로 쌓이는 방식,
  선언적 질의 언어가 사는 것, 이 계열에 들지 않는 모델들
- [그래프 질의 언어](../concepts/graph-query-languages.md) — Cypher·SPARQL·Datalog와 SQL
  재귀 질의, ISO 표준 GQL
- [GraphQL](../concepts/graphql.md) — 클라이언트가 UI에 필요한 JSON 구조를 직접 요청하는,
  일부러 표현력을 줄인 언어

## 관계형과 문서

- [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md) — 도전자들의
  역사, 임피던스 불일치와 ORM, 언제 어느 쪽을 고르는가, 두 모델의 수렴
- [정규화와 비정규화](../concepts/normalization-and-denormalization.md) — ID를 쓰는 이유와
  조인의 대가, 다대일·다대다 관계
- [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md) — "스키마
  없음"의 정확한 뜻과 형식 변경 절차의 차이

## 그래프

- [그래프 데이터 모델](../concepts/graph-data-models.md) — 속성 그래프와 트리플 스토어,
  인접 리스트와 인접 행렬, RDF와 시맨틱 웹의 유산

## 이벤트와 배열

- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 불변 이벤트 로그를 진실의
  원천으로 두고 읽기용 뷰를 유도하는 모델
- [데이터프레임과 배열](../concepts/dataframes-and-arrays.md) — 관계형 표현을 행렬로 바꾸는
  분석·과학용 모델과 배열 데이터베이스

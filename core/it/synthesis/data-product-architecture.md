---
type: synthesis
title: 데이터 프로덕트 아키텍처
description: 데이터 메시의 데이터 프로덕트 내부 설계 층의 진입점 — 어포던스를 설계 단위로 삼는 방법과, 소비·변환·서빙에서 발견·조합으로, 다시 수명 주기·거버넌스·관측으로 이어지는 여덟 어포던스의 설계, 그리고 그 전부를 관통하는 두 시간 축
generated: { by: "claude-opus-5", at: "2026-08-16T04:05:00Z" }
---

# 데이터 프로덕트 아키텍처

**이름이 좁은 이유**: 여기 모인 것은 Zhamak Dehghani가 *Data Mesh*(2022) 4부에 배치한
**데이터 프로덕트 내부 설계** 층뿐이다 — 데이터 프로덕트가 사용자·다른 프로덕트·플랫폼과 맺는
관계(어포던스)마다 어떤 설계 특징이 데이터 메시와 양립하는지를 가르는 데까지다. 저자 자신이
**구현 핸드북이 아니고 기술 불가지로 남는다**고 선언했고(4부 도입, p.192), 정확한 명세는
"아직 정의되고 테스트되어야 한다"고 여러 장에서 반복한다. 아키텍처 구성 요소와 인터페이스를
정하는 층은 형제 허브 [데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md)가,
원칙 층은 [데이터 메시 원칙](data-mesh-principles.md)이 받는다.

읽는 순서가 있다. 먼저 저자가 무엇을 설계 단위로 골랐는지 보고, 그다음 데이터가 드나드는
기본 기능(소비·변환·서빙)을 본 뒤, 그 데이터를 남이 찾아 쓰는 표면(발견·조합), 마지막으로
프로덕트 자신을 운영하는 능력(수명 주기·거버넌스·관측)으로 간다.

## 설계 단위 — 어포던스

- [데이터 프로덕트 어포던스](../concepts/data-product-affordances.md) — 4부 도입·11장.
  능력이나 계층이 아니라 **관계**를 설계 단위로 삼는 방법(Don Norman), 여덟 어포던스와 각각이
  무엇을 **어포드하지 않는지**, 변화·확장·가치를 위한 설계라는 세 특성, 그리고 복잡 적응계에서
  빌려온 지역 규칙·중앙 오케스트레이터 부재

## 데이터가 드나드는 기본 기능

- [데이터 프로덕트의 데이터 서빙 설계](../concepts/data-product-serving-design.md) — 12장.
  다양한 페르소나·종단 데이터·시점 일관성이라는 세 요구가 낳는 다중 양식·불변·바이템포럴·읽기
  전용이라는 네 성질, 의미론을 일급으로 두는 역전, 갱신 함수의 부재와 잊힐 권리의 예외
- [바이템포럴 데이터](../concepts/bitemporal-data.md) — 12장. 실제 시간과 처리 시간이라는 두
  축, 과거를 고치는 유일한 방법인 철회, 조정 가능한 파라미터로서의 스큐, 그리고 **이 KB의 네
  소스가 각자 쓰는 시간 축을 한자리에서 대조하는 표**
- [데이터 프로덕트의 소비와 변환 설계](../concepts/data-product-consumption-and-transformation.md) —
  12장. 소스 세 원형과 CDC의 강등, 소비를 선언하는 쪽이 소비자라는 역전, 물리 위치를 감춰
  연속적 이관이 되는 소비의 지역성, 변환 네 갈래와 "dumb pipes and smart filters"

## 남이 찾아 쓰는 표면

- [데이터 프로덕트의 발견·이해·신뢰 설계](../concepts/data-product-discoverability.md) — 13장.
  사후 큐레이션·사후 조사형 지능을 불충분으로 판정하고 발견 가능성을 생성 시점으로 왼쪽 이동,
  자기 등록과 전역 URI, 시맨틱 모델과 구문 모델의 분리, 보증 다섯 범주, 개별 레코드 없이 모양을
  탐색하는 차등 프라이버시
- [데이터 프로덕트의 조합 가능성 설계](../concepts/data-product-composability.md) — 13장.
  탈중앙화가 부과하는 네 요구, 팩트 테이블 외래 키·분산 타입 시스템·하이퍼링크와 중앙 레지스트리
  세 접근에 대한 판정, 그리고 분산 타입 시스템·전역 URI·다의어 개체 URI·기계보다 사람 쪽
  최적화·사람이라는 요소

## 자기를 운영하는 능력

- [데이터 프로덕트의 수명 주기와 매니페스트](../concepts/data-product-lifecycle-and-manifest.md) —
  14장. 목표 상태를 선언하는 매니페스트와 그 구성 요소, 소스 아티팩트와 선언의 분리, 선언형과
  명령형의 경계
- [내장 정책과 코드로서의 정책](../concepts/embedded-policies-as-code.md) — 14장. 정책을
  코드로 심어 데이터의 흐름에서 실행한다는 결정, 표준화가 절실한 세 정책과 분석 데이터 쪽에
  표준이 없는 유인 구조, 데이터·코드·정책의 통합과 정책 연결
- [데이터 프로덕트의 관측 가능성](../concepts/data-product-observability.md) — 14장. 느슨한
  결합이 관측에 치르는 대가, 로그·트레이스·메트릭 세 기둥과 계보를 트레이스로 환원하는 재정의,
  관측 데이터 자체를 데이터 프로덕트로, 그리고 4부를 닫는 표준화·창발·주체성·확장성

## 이 설계가 딛는 아키텍처

- [데이터 퀀텀](../concepts/data-quantum.md) — 이 어포던스들이 붙는 단위
- [데이터 프로덕트의 포트와 사이드카](../concepts/data-product-ports-and-sidecar.md) — 여덟
  어포던스가 실제로 드러나는 네 인터페이스와 그 표준 구현
- [멀티플레인 데이터 플랫폼](../concepts/multiplane-data-platform.md) — 이 설계가 플랫폼에
  요구하는 것들의 공급처
- [데이터 플랫폼 사용자 여정](../concepts/data-platform-user-journeys.md) — 같은 수명 주기를
  플랫폼 인터페이스 쪽에서 본 자리

## 이 설계가 상대하는 것

- [차원 모델링](../concepts/dimensional-modeling.md)·[팩트 테이블](../concepts/fact-table.md) —
  조합을 단일 스키마의 외래 키로 푸는 쪽
- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — 같은 이력 문제를
  단일 시간 축으로 푸는 쪽
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 저자가 최후 수단으로 강등하는 반입 기법
- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) — 그래프를 중앙에서 선언하는 쪽
- [메타데이터 관리](../concepts/metadata-management.md) — 저자가 낱말째·범주째 기피하는 대상
- [데이터 품질 관리](../concepts/data-quality-management.md) — 점검을 외부 팀이 사후에 하는 쪽
- [마스터 데이터 관리](../concepts/master-data-management.md) — 단일 진실 원천과 중앙 개체 해석

## 경계에 있는 페이지

- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 불변성 논거의 원본 계열
- [스트림-테이블 이중성](../concepts/stream-table-duality.md) — 저자가 시간 축과 "직교한다"고
  선언한 축
- [스트림 처리의 시간 의미론](../concepts/stream-processing-time-semantics.md) — 세 시각을
  엔진 안에 두는 쪽
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 사이드카·관측
  세 기둥·smart endpoints and dumb pipes의 원본
- [GraphQL](../concepts/graphql.md) — 조합 가능성에서 저자가 유일하게 "적합"으로 판정한 계열
- [그래프 데이터 모델](../concepts/graph-data-models.md) — 시맨틱 모델링에서 앞세우는 표현
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 매니페스트 발상의 원본

## 이어지는 허브

- [데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md) — 이 설계가 채우는 구성 요소들
- [데이터 메시 원칙](data-mesh-principles.md) — 이 설계가 형태를 따르는 기능 쪽
- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 설계가 데이터 프로덕트 안으로
  감추는 단계들
- [차원 모델링 기법](dimensional-modeling-techniques.md) — 조합과 이력화에서 정면으로 갈리는 계열

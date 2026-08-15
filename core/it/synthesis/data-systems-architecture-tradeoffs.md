---
type: synthesis
title: 데이터 시스템 아키텍처 트레이드오프
description: 운영계와 분석계, 클라우드와 자체 호스팅, 분산과 단일 노드, 그리고 사업의 요구와 사용자의 요구 사이의 선택을 모으는 허브
generated: { by: "human:me", at: "2026-08-10T21:00:00Z" }
---

# 데이터 시스템 아키텍처 트레이드오프

정답이 하나가 아닌 선택들을 모은다. 각 페이지가 한 축을 맡고, 그 축의
장단점과 언제 어느 쪽을 고르는지를 다룬다.

## 무엇을 아키텍처라 부르는가

- [데이터 아키텍처의 정의](../concepts/data-architecture-defined.md) — 엔터프라이즈 아키텍처의 부분집합이라는 위치, 일방통행문과 양방향문, 운영 아키텍처와 기술 아키텍처
- [좋은 데이터 아키텍처의 아홉 원칙](../concepts/good-data-architecture-principles.md) — 공통 구성 요소·실패 계획·확장성·리더십·되돌릴 수 있는 결정·보안·FinOps
- [기술 선택의 기준](../concepts/technology-selection-criteria.md) — 아키텍처가 정해진 뒤 도구를 고르는 열 가지 축과 벤치마크 비판
- [FinOps와 비용 최적화](../concepts/finops-and-cost-optimization.md) — TCO·TOCO·capex와 opex, 그리고 지출을 운영으로 다루는 실무

## 아키텍처의 유형들

- [람다 아키텍처와 카파 아키텍처](../concepts/lambda-and-kappa-architecture.md) — 배치와 스트림을 합치려는 두 제안과 그 뒤를 이은 데이터플로 모델
- [데이터 메시](../concepts/data-mesh.md) — 중앙집중 플랫폼을 도메인 소유권으로 뒤집는 제안(개관). 원칙별 깊이는 [데이터 메시 원칙](data-mesh-principles.md) 허브가 받는다
- [IoT 데이터 아키텍처](../concepts/iot-data-architecture.md) — 사람이 아니라 장치가 데이터를 만드는 쪽

## 운영계와 분석계

- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계와 분석계를 왜 가르며 어떤 아키텍처들이 그 요구를 감당했나
- [데이터 레이크](../concepts/data-lake.md) — 스키마를 강제하지 않는 분석 저장소와 원시 데이터 우선 원칙
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 무엇이 정본이고 무엇이 다시 만들 수 있는 사본인가

## 클라우드와 자체 호스팅

- [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md) — 만들 것인가 살 것인가, 그리고 통제권을 잃는 대가
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 서비스 계층화, 저장과 연산의 분리, 멀티테넌시

## 분산과 단일 노드

- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 여러 기계로 갈 아홉 가지 이유와 가지 말아야 할 이유
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 서비스마다 자기 데이터베이스를 두는 이유와 그 대가

## 사업의 요구와 사용자의 요구

데이터를 더 모을수록 얻는 것이 있고, 그 데이터의 대상이 되는 사람이 잃는 것이 있다.
이 축은 성능이 아니라 사람을 저울에 올린다.

- [공학 윤리와 책임](../concepts/engineering-ethics-and-responsibility.md) — 시스템을 만드는 사람이 그 결과에 지는 책임과 윤리가 체크리스트가 아닌 이유
- [예측 분석과 알고리즘의 해악](../concepts/predictive-analytics-and-algorithmic-harm.md) — 데이터로 사람에 대한 결정을 자동화할 때의 편향·책무·피드백 루프
- [감시와 동의](../concepts/surveillance-and-consent.md) — 행동 추적이 감시가 되는 지점과 "안 쓰면 된다"가 성립하지 않는 이유
- [결정권으로서의 프라이버시](../concepts/privacy-as-a-decision-right.md) — 프라이버시가 비밀 유지가 아니라 선택권이라는 정의와 그 권리의 이전
- [위험 자산으로서의 데이터](../concepts/data-as-a-hazardous-asset.md) — 쌓아 둔 개인 데이터가 지는 위험, 산업혁명 비유, 데이터 최소화와 규제

## 이어지는 허브

- [데이터플로 아키텍처](dataflow-architecture.md) — 여러 시스템을 이어 붙이기로 했을 때의 그다음 선택들
- [데이터 메시 원칙](data-mesh-principles.md) — 위 유형 중 하나를 원전 수준으로 펼친 쪽

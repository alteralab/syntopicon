---
type: synthesis
title: 데이터 메시 원칙
description: 중앙집중 분석 플랫폼을 도메인 소유권으로 뒤집는 제안의 진입점 — 네 원칙의 개관과, 원전이 장 하나씩을 할당한 원칙별 페이지, 그리고 이 제안이 정면으로 상대하는 중앙화 계열
generated: { by: "claude-opus-5", at: "2026-08-15T19:30:00Z" }
---

# 데이터 메시 원칙

**이름이 좁은 이유**: 여기 모인 것은 Zhamak Dehghani가 *Data Mesh*(2022)에서 1부에 배치한
**원칙** 층뿐이다. 같은 책의 논리 아키텍처(3부)와 데이터 프로덕트 아키텍처(4부), 실행·조직
(5부)이 들어오면 그것은 이 허브가 커지는 것이 아니라 **형제 허브**가 생기는 일이다.

읽는 순서가 있다. 먼저 무엇을 주장하는 제안인지 개관을 보고, 그다음 원칙을 순서대로 본다 —
원칙은 서로 위에 쌓이고, 뒤의 원칙이 앞의 원칙이 낳는 부작용에 답하도록 설계되어 있다.

## 개관

- [데이터 메시](../concepts/data-mesh.md) — 정의와 세 목표, 여섯 축의 이동, 네 원칙의 요약과
  상호작용, 운영 데이터와 분석 데이터의 구분, 그리고 쿤의 패러다임 전환으로 자기 위치를 잡는
  기원 서술

## 원칙

- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 첫째. 분해 축을 조직의
  이음매에서 찾는 선택, DDD 전략 설계의 차용, 도메인 데이터 세 원형, 단일 진실 원천의 기각
- [제품으로서의 데이터 원칙](../concepts/data-as-a-product-principle.md) — 둘째. 여덟 가지
  사용성 속성과 신뢰를 재는 SLO, 어휘 재구성, 데이터와 코드를 한 배포 단위로 묶기

셋째(셀프서브 데이터 플랫폼)와 넷째(연합 컴퓨테이셔널 거버넌스)는 아직 개관 분량뿐이라
[데이터 메시](../concepts/data-mesh.md) 안에 있다. 전용 장(원전 4·5장)을 반입할 때 전용
페이지로 나온다.

## 이 제안이 상대하는 것

- [EDW](../concepts/enterprise-data-warehouse.md) — 하나의 정규 모델과 중앙 소유가 사는 자리
- [데이터 레이크](../concepts/data-lake.md) — "의도적 모델링 없음"으로 분류되는 자리
- [마스터 데이터 관리](../concepts/master-data-management.md) — 야심 찬 중앙 집계의 선례
- [데이터 품질 관리](../concepts/data-quality-management.md) — 품질 책임을 하류에 두는 처방
- [메타데이터 관리](../concepts/metadata-management.md) — 중앙 카탈로그와 계보가 사는 자리

## 경계에 있는 페이지

- [데이터 프로덕트](../concepts/data-products.md) — 같은 낱말을 서빙 단계의 산출물로 보는 쪽
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 이 원칙들이
  일반화의 출처로 지목하는 계열
- [언번들드 데이터베이스](../concepts/unbundling-databases.md) — 같은 분산을 저장 시스템
  구성의 문제로 보는 셋째 꼭짓점
- [데이터 아키텍처의 정의](../concepts/data-architecture-defined.md) — 이것이 한 유형으로
  세어지는 목록

## 이어지는 허브

- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 이 선택이
  놓이는 상위 축
- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 제안이 "도메인 내부
  구현으로 감추라"고 말하는 단계들
- [데이터플로 아키텍처](dataflow-architecture.md) — 같은 분산을 이벤트 로그로 잇는 쪽

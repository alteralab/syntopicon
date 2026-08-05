---
type: concept
title: 도메인 역할 유형
description: 도메인이 데이터 흐름에서 맡는 역할과 그에 따라 달라지는 설계
generated: { by: "claude-opus-5", at: "2026-08-06T06:30:00Z" }
sources:
  - { id: strengholt2023-dms, resource: /it/sources/strengholt2023-dms.md }
---

# 도메인 역할 유형

같은 "도메인"이라도 데이터의 생성·소비·재전달 중 무엇을 하느냐에 따라 적용할 청사진과
아키텍처 패턴이 달라진다. 저자는 도메인을 **데이터 제품의 사용·배포 특성으로 분류**
한다 (2장 Domain Characteristics, p.45-48).[^strengholt2023-dms]

## 두 기본형

**소스 시스템 정렬 도메인(source system–aligned domain)**

- 데이터가 발원하는 골든 소스 시스템에 정렬된 도메인. 보통 트랜잭션·운영 성격이다
  (2장 Domain Characteristics, p.45).[^strengholt2023-dms]
- 공유 원칙은 **골든 소스에서 직접 취득**하는 것이다. 데이터 변환·공유를 위한 표준
  서비스로 이 도메인을 지원한다 (2장 Domain Characteristics, p.45).[^strengholt2023-dms]

**소비자 정렬 도메인(consumer-aligned domain)**

- 다른 도메인의 데이터를 소비·사용하는 도메인. 특정 최종 사용자 유스케이스에
  정렬되어 있고, 자기 업무에 맞게 데이터를 변환한다
  (2장 Domain Characteristics, p.46).[^strengholt2023-dms]

## 재사용이 얽힐 때

여러 하위 소비자가 **서로 다른 도메인의 같은 조합**을 원하는 상황이 더 어렵다. 겹치는
관심사를 격리해 관리하려면 공유 데이터를 만드는 업무 로직을 사용처와 분리된 곳에
모아 둘 수 있다 (2장 Domain Characteristics, p.46).[^strengholt2023-dms]

- **집계 도메인(aggregate domain)** — 데이터를 먼저 결합·통합한 뒤 자기도 쓰고 다른
  도메인에도 공유한다. 이 고객/공급자 패턴은 도메인 간 통합 요구가 겹칠 때 특히
  유용하다 (2장 Domain Characteristics, p.46).[^strengholt2023-dms]
- **공급자 도메인** — 순수하게 상류/하류 관계로만 협업하는 모델. 결합 데이터 제품을
  만들어 배포하지만 **자기 유스케이스에는 쓰지 않는다.** 소비자이면서 제공자로 동시에
  행동한다 (2장 Domain Characteristics, p.46).[^strengholt2023-dms]
- **구성자 도메인(constructor domain)** — 소비하던 도메인이 새 데이터를 만들어 제공자가
  되는 경우다. 앞의 집계와 다른 점은 만들어진 데이터 제품에 **새로운 업무 통찰이
  담긴다**는 것 — 구조만 바뀐 게 아니라 다른 맥락으로 풍부해졌다
  (2장 Domain Characteristics, p.47-48).[^strengholt2023-dms]

용어 혼동 주의: **도메인 애그리게이트(domain aggregate)** 는 하나의 단위로 다룰 수 있는
도메인 객체의 묶음이고, 데이터를 그룹핑해 요약 형태로 표현하는 **데이터 집계(data
aggregation)** 와 다르다 (2장 Domain Characteristics, p.47).[^strengholt2023-dms]

## 공통 진입로

- 모든 시나리오에서 데이터 배포는 **공동 진입로(common driveway)** 를 쓰는 것이 모범
  사례다 (2장 Domain Characteristics, p.48).[^strengholt2023-dms]
- 도메인이 다른 도메인과 통신할 때는 **표준화된 인터페이스**를 쓴다. 도메인 안쪽은
  애플리케이션 고유 인터페이스와 데이터 모델로 직접 통신해도 된다
  (2장 Data Domains, p.42).[^strengholt2023-dms]
- 통합 스타일은 하나로 통일하지 않고 몇 가지 공통 진입로 패턴으로 **표준화**한다.
  대량 데이터 처리에는 데이터 제품을, 강한 일관성 읽기·명령에는 API 서비스를 권한다
  (2장 Patterns for complex integration challenges, p.49).[^strengholt2023-dms]

## 왜 점대점을 피하는가

- 사일로와 통합 허브를 데이터 배포에 쓰지 않는다 — 변환 단계가 늘어 제공자와 소비자
  사이의 사슬이 길어지고 관리가 어려워진다
  (2장 Principles…, p.50).[^strengholt2023-dms]
- 점대점 연결은 **지수적 복잡도**를 만든다. 저자가 드는 수치: 애플리케이션 100개를
  상호 연결하면 5,000개, 1,000개면 대략 500,000개의 점대점 연결이 생긴다
  (2장 Principles…, p.50).[^strengholt2023-dms]
- #hypothesis 이 수치는 완전 그래프 간선 수 n(n−1)/2를 그대로 쓴 것으로 보인다
  (100 → 4,950 ≈ 5,000, 1,000 → 499,500 ≈ 500,000). 실제 기업 환경에서 모든 쌍이
  연결되는 일은 없으므로 상한 예시로 읽는 편이 맞다.[^strengholt2023-dms]

[^strengholt2023-dms]: Strengholt 2023, 2장 "Organizing Data Using Data Domains"

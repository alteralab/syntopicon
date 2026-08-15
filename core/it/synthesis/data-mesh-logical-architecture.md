---
type: synthesis
title: 데이터 메시 논리 아키텍처
description: 데이터 메시의 원칙을 아키텍처 구성 요소로 옮긴 층의 진입점 — 독립 배포 단위인 데이터 퀀텀과 그것이 바깥과 만나는 표준 표면, 그리고 그 퀀텀을 짓고 돌리는 세 플레인 플랫폼과 그 인터페이스를 도출하는 사용자 여정
generated: { by: "claude-opus-5", at: "2026-08-15T23:50:00Z" }
---

# 데이터 메시 논리 아키텍처

**이름이 좁은 이유**: 여기 모인 것은 Zhamak Dehghani가 *Data Mesh*(2022) 3부에 배치한
**논리 아키텍처** 층뿐이다 — 구조 구성 요소·인터페이스·분해 축을 정하는 데까지이고, 기술 매핑·
데이터 모델링·인터페이스 명세 같은 구현 설계는 저자 자신이 범위 밖으로 선언했다. 같은 책이
4부에서 데이터 프로덕트 내부 설계로, 5부에서 실행·조직으로 넘어가면 그것은 이 허브가 커지는
것이 아니라 **형제 허브**가 생기는 일이다 — 예고대로 4부는
[데이터 프로덕트 아키텍처](data-product-architecture.md)로 갈라져 나갔다. 원칙 층은
[데이터 메시 원칙](data-mesh-principles.md)이 받는다.

읽는 순서가 있다. 먼저 아키텍처의 단위가 무엇인지 보고, 그 단위가 바깥과 만나는 표면을 본 다음,
그 단위를 짓고 돌리는 플랫폼으로 넘어간다.

## 아키텍처의 단위

- [데이터 퀀텀](../concepts/data-quantum.md) — 9장. 독립 배포 가능한 최소 아키텍처 단위라는
  정의와 그 신조어를 고른 이유, 코드·데이터와 메타데이터·플랫폼 의존이라는 세 종류의 구조 구성
  요소, 외부 파이프라인 개념의 폐기, 저자 자신이 매긴 성숙도 등급
- [데이터 프로덕트의 포트와 사이드카](../concepts/data-product-ports-and-sidecar.md) — 9장.
  입력·출력 데이터 포트와 발견·관측 API, 제어 포트, 그리고 횡단 관심사를 중앙 관문 대신 각
  프로덕트의 실행 맥락에서 돌리는 사이드카와 계산 컨테이너

## 그 단위를 짓고 돌리는 플랫폼

- [멀티플레인 데이터 플랫폼](../concepts/multiplane-data-platform.md) — 9장·10장. 단일 통합
  플랫폼의 기각, layer 대신 plane을 쓰는 이유와 계층화의 부정, 인프라 유틸리티·데이터 프로덕트
  경험·메시 경험이라는 세 플레인, "플랫폼이라는 단일 실체는 없다"는 결론
- [데이터 플랫폼 사용자 여정](../concepts/data-platform-user-journeys.md) — 10장. 인터페이스를
  능력 목록이 아니라 여정에서 도출하는 설계법, 여섯 페르소나, 개발자 여정 세 단계의 인터페이스
  카탈로그, 데이터 프로덕트의 은퇴와 휴면, ML 모델을 데이터 프로덕트로 배포하는 여정

## 이 아키텍처가 구현하는 원칙

- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 도메인 인터페이스가 분석
  데이터 공유 인터페이스로 확장되는 자리(9장 절이 이 페이지에 합류해 있다)
- [제품으로서의 데이터 원칙](../concepts/data-as-a-product-principle.md) — 데이터 퀀텀이
  아키텍처로 옮기는 원칙
- [셀프서브 데이터 플랫폼 원칙](../concepts/self-serve-data-platform-principle.md) — 멀티플레인
  플랫폼이 구조로 옮기는 원칙
- [연합 컴퓨테이셔널 거버넌스 원칙](../concepts/federated-computational-governance-principle.md) —
  사이드카와 제어 포트가 실행하는 정책을 정하는 원칙

## 이 설계가 상대하는 것

- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) — "외부 파이프라인"이 일급
  아티팩트로 사는 자리
- [메타데이터 관리](../concepts/metadata-management.md) — 저자가 낱말째 기피하는 범주와 중앙
  카탈로그
- [데이터 품질 관리](../concepts/data-quality-management.md) — 정화 책임의 소재가 갈리는 자리
- [마스터 데이터 관리](../concepts/master-data-management.md) — 플랫폼이 알람으로 탐지하겠다는
  "마스터 데이터 프로덕트"의 계열

## 경계에 있는 페이지

- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 아키텍처 퀀텀·
  사이드카 패턴·서비스 메시의 원본 계열
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 인프라 유틸리티
  플레인이 딛는 기반층
- [컴퓨트와 스토리지의 분리](../concepts/compute-storage-separation.md) — 유틸리티 플레인 안에
  가둬야 한다고 저자가 판정하는 최적화
- [언번들드 데이터베이스](../concepts/unbundling-databases.md) — 같은 분해를 저장 시스템 구성의
  문제로 보는 쪽
- [데이터 프로덕트](../concepts/data-products.md) — 같은 낱말을 수동적 산출물로 보는 쪽

## 이어지는 허브

- [데이터 프로덕트 아키텍처](data-product-architecture.md) — 이 아키텍처의 구성 요소 안쪽을
  어포던스별로 설계하는 쪽(4부)
- [데이터 메시 원칙](data-mesh-principles.md) — 이 아키텍처가 형태를 따르는 기능 쪽
- [데이터 메시 실행과 조직](data-mesh-execution-and-organization.md) — 이 아키텍처를 실제
  조직에서 세워 나가는 층(5부)
- [데이터플로 아키텍처](dataflow-architecture.md) — 같은 분산을 이벤트 로그로 잇는 쪽
- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 아키텍처가 데이터 프로덕트
  안으로 감추는 단계들

---
type: synthesis
title: 데이터 메시 원칙
description: 중앙집중 분석 플랫폼을 도메인 소유권으로 뒤집는 제안의 진입점 — 개관 한 장과, 원전이 장 하나씩을 할당한 네 원칙의 전용 페이지, "왜 지금·왜 이전 것으로는 안 되는가"를 논증하는 2부, 그리고 이 제안이 정면으로 상대하는 중앙화 계열
generated: { by: "claude-opus-5", at: "2026-08-16T03:00:00Z" }
---

# 데이터 메시 원칙

**이름이 좁은 이유**: 여기 모인 것은 Zhamak Dehghani가 *Data Mesh*(2022)에서 1부에 배치한
**원칙** 층과, 그 원칙이 왜 필요한지를 논증하는 2부다. 2부를 여기 두는 이유는 그것이 독립
주제가 아니라 **같은 원칙들의 근거**이기 때문이다 — 2부 7장의 요약표는 모든 실행 축을 네 원칙
중 하나에 되돌려 매핑한다. 같은 책의 논리 아키텍처(3부)는 예고대로 형제 허브
[데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md)로, 데이터 프로덕트
아키텍처(4부)는 [데이터 프로덕트 아키텍처](data-product-architecture.md)로 갈라져 나갔고,
실행·조직(5부)이 들어올 때도 이 허브가 커지는 것이 아니라 **형제 허브**가 생긴다.

읽는 순서가 있다. 먼저 무엇을 주장하는 제안인지 개관을 보고, 그다음 원칙을 순서대로 본다 —
원칙은 서로 위에 쌓이고, 뒤의 원칙이 앞의 원칙이 낳는 부작용에 답하도록 설계되어 있다. "왜
이것을 해야 하는가"가 먼저 궁금하면 아래 2부 논증부터 읽어도 된다.

## 개관

- [데이터 메시](../concepts/data-mesh.md) — 정의와 세 목표, 여섯 축의 이동, 네 원칙의 요약과
  상호작용, 운영 데이터와 분석 데이터의 구분, 그리고 쿤의 패러다임 전환으로 자기 위치를 잡는
  기원 서술

## 원칙

- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 첫째. 분해 축을 조직의
  이음매에서 찾는 선택, DDD 전략 설계의 차용, 도메인 데이터 세 원형, 단일 진실 원천의 기각
- [제품으로서의 데이터 원칙](../concepts/data-as-a-product-principle.md) — 둘째. 여덟 가지
  사용성 속성과 신뢰를 재는 SLO, 어휘 재구성, 데이터와 코드를 한 배포 단위로 묶기
- [셀프서브 데이터 플랫폼 원칙](../concepts/self-serve-data-platform-principle.md) — 셋째. 앞선
  두 원칙이 도메인에 떠넘긴 중복·비용·비호환을 되받는 플랫폼, 기존 데이터 플랫폼과 갈리는 여섯
  특성, 플랫폼 사고에서 끌어온 다섯 목표와 여섯 이행 지침
- [연합 컴퓨테이셔널 거버넌스 원칙](../concepts/federated-computational-governance-principle.md) —
  넷째. 중앙 관문을 다시 세우지 않고 전역 보증을 얻는 설계, 시스템 사고·연합 운영 모델·계산적
  실행이라는 세 기둥, 중앙 거버넌스에서 옮겨 가는 여섯 전환

## 왜 이 제안인가 — 2부의 논증

저자는 2부를 셋으로 끊는다: **지금**(변곡점의 거시 동인)·**이후**(무엇이 달라지는가)·
**이전**(무엇이 왜 실패했는가). 가운데 "이후"는 개관 페이지 안에 있다.

- [분석 데이터 관리의 변곡점](../concepts/data-mesh-inflection-point.md) — 6장. 변곡점이라는
  낱말의 정의와 두 축, 그리고 다섯 거시 동인(커진 기대·데이터의 큰 분열·새로운 종류의 규모·
  상시화된 복잡성·투자 대비 수익의 불협화음, 설문 실측 수치 포함)
- [데이터 메시](../concepts/data-mesh.md)의 "변곡점 이후" 절 — 7장. 세 결과와 그것을 만드는
  열한 실행 축, 그리고 축마다 어느 원칙이 받는지의 대응표
- [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md) —
  8장. 1세대 웨어하우스·2세대 레이크·3세대 멀티모달 클라우드와, 세 세대가 한 번도 바꾸지 않은
  세 가정(중앙집중·모놀리식·기술 주도)

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
- [경계 컨텍스트](../concepts/bounded-context.md) — 2021년의 도메인 주도 설계 실무서가 이
  분해의 단위로 못 박는 경계
- [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md) — 같은 경계를
  운영계의 물리 서비스 경계로 고르는 쪽

## 이어지는 허브

- [데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md) — 이 원칙들이 아키텍처
  구성 요소가 되는 층(3부): 데이터 퀀텀과 그 포트, 세 플레인 플랫폼
- [데이터 프로덕트 아키텍처](data-product-architecture.md) — 데이터 프로덕트 내부 설계 층(4부)
- [데이터 메시 실행과 조직](data-mesh-execution-and-organization.md) — 이 원칙들을 실제
  조직에서 굴리는 층(5부): 채택 심사·진화 단계·적합성 함수·팀 토폴로지
- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 이 선택이
  놓이는 상위 축
- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 제안이 "도메인 내부
  구현으로 감추라"고 말하는 단계들
- [데이터플로 아키텍처](dataflow-architecture.md) — 같은 분산을 이벤트 로그로 잇는 쪽

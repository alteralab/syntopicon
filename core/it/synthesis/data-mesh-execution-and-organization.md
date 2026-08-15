---
type: synthesis
title: 데이터 메시 실행과 조직
description: 데이터 메시를 실제 조직에서 시작하고 굴리는 층의 진입점 — 지금 채택할 조직인지 가리는 심사와 비즈니스 주도 실행 틀, 채택을 s 곡선 세 단계로 나누는 거시 도구와 이터레이션마다 방향을 재는 적합성 함수, 레거시로부터의 이관, 그리고 팀 토폴로지·데이터 프로덕트 경계·역할과 역량·문화와 보상이라는 조직 설계 다섯 범주
generated: { by: "claude-opus-5", at: "2026-08-16T07:00:00Z" }
---

# 데이터 메시 실행과 조직

**이름이 좁은 이유**: 여기 모인 것은 Zhamak Dehghani가 *Data Mesh*(2022) 5부 "How to Get
Started"에 배치한 **실행과 조직** 층뿐이다 — 원칙도 아키텍처도 아니고, 그 둘을 실제 조직에서
움직이게 하는 문제다. 저자 자신이 이 부의 지위를 낮춰 적는다: **이 책을 쓰는 시점에 우리는
데이터 메시 채택의 초기 연도에 있다** (5부 도입, p.270)고, 또 **이것은 출발점일 뿐이고 데이터
메시에 고유한 전환 접근을 다듬는 데는 앞으로 여러 해가 남아 있다**고. 원칙 층은
[데이터 메시 원칙](data-mesh-principles.md)이, 아키텍처 층은
[데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md)가, 데이터 프로덕트 내부 설계는
[데이터 프로덕트 아키텍처](data-product-architecture.md)가 받는다. 이 넷이 한 책의 다섯 부를
나눠 갖는 형제 허브다.

읽는 순서가 있다. 먼저 **할 것인가**(심사)를 보고, 그다음 **어떤 리듬으로**(실행 틀), 다음으로
**어디까지 왔는지 어떻게 아는가**(단계와 측정), 그리고 브라운필드라면 **레거시를 어떻게
끝내는가**를 본다. 조직 쪽은 그 뒤에 읽어도 되지만, 저자는 둘이 **동시에** 일어난다고 못
박는다 — 아키텍처가 먼저 서고 조직이 따라오는 것이 아니다.

## 실행 — 무엇을 언제 하는가

- [데이터 메시 실행 프레임워크](../concepts/data-mesh-execution-framework.md) — 5부 도입·15장.
  지금 채택할 조직인지 가리는 여덟 자기 평가 축과 각 축의 탈락 조건, 데이터 전략에서 플랫폼까지
  다섯 층을 잇는 큰 그림, 비즈니스 주도·종단·반복·진화라는 네 성격, 그리고 비즈니스 주도 실행이
  주는 세 이익과 그것이 부르는 세 병리(점 솔루션·기술 부채·프로젝트 기반 예산)의 처방
- [데이터 메시의 진화적 채택 단계](../concepts/data-mesh-adoption-phases.md) — 15장. 혁신 채택
  s 곡선과 Kent Beck의 3X를 빌린 탐색·확장·추출 세 단계, 네 원칙 각각이 단계마다 갖는 특성의
  대응표, 그리고 단계마다 가치가 나오는 곳이 달라진다는 서술
- [데이터 메시의 적합성 함수](../concepts/data-mesh-fitness-functions.md) — 15장. 진화적
  컴퓨팅에서 빌린 목적 함수를 방향타로 쓰는 방법, KPI와의 갈림, "데이터 프로덕트 수"를 잘못된
  척도로 기각하고 "링크 수"로 바꾸는 실례, 네 원칙별 측정 목록, 그리고 지표 대부분이 허영
  측정이라는 *Accelerate*의 경고
- [레거시에서 데이터 메시로의 이관](../concepts/migration-from-legacy-to-data-mesh.md) — 15장.
  중앙집중 아키텍처는 과도기에만 공존한다는 판정과 그 방향 기준, 중앙집중 "기술"은 멀티테넌트로
  쓸 수 있다는 구분, 레이크·웨어하우스를 우회해 소스로 직행, 웨어하우스를 소비 엣지 노드로,
  그리고 소비자 이관과 옛 파이프라인 폐기까지 묶어야 완료인 원자적 진화 단계

## 조직 — 누가 어떻게 일하는가

- [데이터 메시의 조직 변화와 문화](../concepts/data-mesh-organizational-change.md) — 16장.
  Galbraith 스타 모델 다섯 범주와 그 합에서 창발하는 문화, 사회 운동 연구에서 빌린 운동 기반
  변화, 데이터 메시 네이티브 조직의 여덟 가치, 내재 동기(자율·숙달·목적)와 외재 동기의 분리,
  그리고 수직·수평 프로세스와 세 프로세스 변화
- [데이터 메시의 팀 토폴로지](../concepts/data-mesh-team-topologies.md) — 16장. 전제하는
  도메인 지향 조직 구조와, Team Topologies의 네 팀 유형·세 상호작용 양식에 데이터 메시의 팀을
  매핑한 결과 — 스트림 정렬 데이터 프로덕트 팀, 프랙탈 플랫폼 팀, 팀이 아니라 그룹인 거버넌스
- [데이터 프로덕트 경계 휴리스틱](../concepts/data-product-boundary-heuristics.md) — 16장.
  무엇이 한 데이터 프로덕트에 들어가는지를 판정하는 다섯 휴리스틱과 사용 용이성·유지보수
  용이성·비즈니스 관련성의 교집합인 골디락스 존, 그리고 차원 모델링의 조인 대신 의도적 복제를
  고르는 대목
- [데이터 메시의 역할과 역량](../concepts/data-mesh-roles-and-skills.md) — 16장. 새로 생기는
  세 역할과 옮겨 가거나 폐지되는 기존 거버넌스 역할의 행선지, CDAO의 인에이블먼트 전환, 그리고
  데이터 리터러시 교육의 다섯 대상과 두 강제 함수

## 이 실행이 실행하는 것

- [데이터 메시](../concepts/data-mesh.md) — 정의와 세 목표
- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 팀 경계의 근거
- [제품으로서의 데이터 원칙](../concepts/data-as-a-product-principle.md) — 데이터 프로덕트
  소유자 역할의 근거
- [셀프서브 데이터 플랫폼 원칙](../concepts/self-serve-data-platform-principle.md) — 플랫폼
  팀의 근거
- [연합 컴퓨테이셔널 거버넌스 원칙](../concepts/federated-computational-governance-principle.md) —
  거버넌스가 팀이 아니라 그룹인 근거
- [멀티플레인 데이터 플랫폼](../concepts/multiplane-data-platform.md) — 플랫폼 팀이 프랙탈로
  나뉘는 축
- [데이터 플랫폼 사용자 여정](../concepts/data-platform-user-journeys.md) — 플랫폼 제품 소유자가
  설계하는 대상

## 이 실행이 상대하는 것

- [전사 데이터 웨어하우스](../concepts/enterprise-data-warehouse.md) — 상류에 두면 안 된다고
  판정되는 대상
- [데이터 레이크](../concepts/data-lake.md) — 같은 판정의 다른 세대
- [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md) —
  여기서 이관하는 "레거시"의 계보
- [차원 모델링](../concepts/dimensional-modeling.md) — 경계 휴리스틱이 정면으로 갈리는 계열

## 경계에 있는 페이지

- [재처리와 점진적 마이그레이션](../concepts/reprocessing-and-gradual-migration.md) — 같은
  점진성을 파생 뷰의 병행 운용으로 푸는 쪽
- [데이터 엔지니어의 진화](../concepts/data-engineer-evolution.md) — 같은 역할 변화를 추세
  예측으로 보는 다른 소스
- [유지보수성](../concepts/maintainability.md) — 브라운필드·그린필드 어휘의 다른 출처
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 저자가 전제를
  공유한다고 명시한 계열
- [데이터옵스](../concepts/dataops.md) — 문화·자동화·측정을 같은 축으로 묶는 다른 계열
- [기술 선택 기준](../concepts/technology-selection-criteria.md) — 기존 기술을 남길지 고르는 자리

## 이어지는 허브

- [데이터 메시 원칙](data-mesh-principles.md) — 이 실행이 실행하는 원칙 층(1·2부)
- [데이터 메시 논리 아키텍처](data-mesh-logical-architecture.md) — 아키텍처 층(3부)
- [데이터 프로덕트 아키텍처](data-product-architecture.md) — 데이터 프로덕트 내부 설계 층(4부)
- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 조직 변화가 도메인 팀
  안으로 옮기는 단계들

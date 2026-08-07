---
type: concept
title: Data Vault 2.0 아키텍처
description: staging→Raw Data Vault→Business Vault→information mart 계층과 hard/soft 업무 규칙 분리로 변경 흡수·확장성을 얻는 3계층 EDW 아키텍처
status: draft
generated: { by: "claude-fable-5", at: "2026-08-07T00:00:00Z" }
sources:
  - { id: linstedt2016, resource: /it/sources/linstedt2016.md }
---

# Data Vault 2.0 아키텍처

**목차**: [확장성의 차원들 (§2.1)](#확장성의-차원들-21) · [세 개의 계층](#세-개의-계층) · [Hard rule / soft rule 분리](#hard-rule-soft-rule-분리) · [선택적 Vault 확장](#선택적-vault-확장) · [관리형 셀프서비스 BI](#관리형-셀프서비스-bi) · [NoSQL·실시간 수용](#nosql실시간-수용)

이 페이지의 질문: **Data Vault 2.0은 어떤 계층 구조와 규칙 배치로
[전형적 2·3계층 아키텍처](enterprise-data-warehouse.md)의 확장성 한계를 푸는가.**
모델(허브·링크·새틀라이트) 자체는
[Data Vault 모델링](../concepts/data-vault-modeling.md)이 다룬다.

- Data Vault 2.0은 모델링(성능·확장성 개선), 방법론(Scrum·애자일, 2–3주 스프린트),
  아키텍처(NoSQL·빅데이터 시스템 포함), 구현(패턴 기반 자동화·생성)의 네 요소로
  구성된 시스템이며, 아키텍처는 그중 하나의 기둥이다 (§1.3, p.28).[^linstedt2016]
- 출발점은 유지보수의 악순환이다: 첫 번째 information mart는 싸게 나오지만, 두 번째부터는
  기존 의존성 유지·리팩터링·재테스트가 겹쳐 기능 추가 비용이 계속 오른다 — 기존
  아키텍처들의 연장성(extensibility)은 최적이 아니다 (§2, pp.33–34).[^linstedt2016]

## 확장성의 차원들 (§2.1)

확장성은 연장성 하나가 아니라 여러 차원을 가진다 (§2.1, p.34):[^linstedt2016]

- 워크로드: EDW는 전형적 기업에서 가장 크고 계산 집약적인 업무 애플리케이션으로,
  데이터량·동시 사용자 증가를 겪는다. 대응은 MPP·SMP 같은 병렬 하드웨어와 병렬
  데이터베이스 소프트웨어, 그리고 예상 데이터량에 맞춘 논리·물리 설계 최적화다
  (§2.1.1, pp.34–35).[^linstedt2016]
- 데이터 복잡성: 다양성(variety, 반정형·비정형·센서 데이터), 볼륨(volume),
  속도(velocity), 신뢰성(veracity — 거버넌스·계보 추적·견고한 통합이 전제)이
  데이터 복잡성을 키운다 (§2.1.2, p.35).[^linstedt2016]
- 분석 복잡성: 원래 DW 설계자가 예상 못 한 방식의 데이터 준비를 요구하는 분석
  (예: 데이터 마이닝, 장바구니 분석, 클릭스트림)이 늘고, 정형·비정형 혼합이 흔해진다
  (§2.1.3, pp.35–36).[^linstedt2016]
- 질의 복잡성: RDBMS는 집합 지향 언어와 병렬 실행 최적화를 제공하지만, 시계열 분석이나
  관계형 OLAP 큐브 질의처럼 복잡한 질의는 DW 크기 때문에 매우 느려질 수 있다
  (§2.1.4, p.36).[^linstedt2016]
- 가용성: 마트·리포트·OLAP 큐브까지 포함한 전체의 가용성을 DW 팀이 SLA로 책임진다.
  새 소스 추가가 적재 시간을 늘려 가용성을 위협하므로, "컴퓨팅 자원만 더하면 되는"
  능력을 설계 단계에서 넣어야 한다 (§2.1.5, pp.36–37).[^linstedt2016]
- 보안: 데이터를 지킬 필요는 데이터셋 크기·다양성에 대해 지수적으로 커진다. NoSQL을
  던져 넣는 것으로는 해결되지 않고 오히려 악화된다 (§2.1.6, p.37).[^linstedt2016]

## 세 개의 계층

Data Vault 2.0 아키텍처는 전형적 3계층 아키텍처를 다음과 같이 변형한 것이다: 이력을
저장하지 않는 스테이징, Data Vault 모델링을 따르는 DW 계층, DW 계층에 의존하는 하나
이상의 information mart 계층 — 그리고 선택적 Vault 확장들 (§2.2, p.37).[^linstedt2016]
정보 제공이라는 EDW의 목표를 강조하기 위해 data mart 대신 **information mart**라는
용어를 쓴다 (§2.2, p.37).[^linstedt2016]

### 스테이징 영역

- 배치 적재 시 소스에서 데이터를 최대한 빨리 뽑아 운영계 부하를 줄이고, 플랫 파일에는
  불가능한 SQL 실행을 가능하게 하는 계층이다 (§2.2.3, p.41).[^linstedt2016]
- 전통 아키텍처와 달리 **이력을 담지 않는다** — 다음에 적재할 배치만 둔다(장애로 밀린
  복수 배치는 예외). 이력을 두면 소스 구조 변화에 대응하는 적재 로직(사실상 업무 규칙)이
  계속 복잡해지기 때문으로, 복잡한 업무 규칙을 최종 사용자 쪽으로 미루려는 이
  아키텍처의 목표와 직결된다 (§2.2.3, pp.41–42).[^linstedt2016]
- 테이블은 소스 구조(기본 키 포함)를 복제하되 인덱스·외래 키는 복제하지 않으며, 소스의
  나쁜 데이터까지 받도록 모든 컬럼을 널 허용으로 둔다. 여기에 메타데이터 컬럼 네 가지 —
  시퀀스 번호(sequence number)·타임스탬프·레코드 소스(record source)·업무 키(조합 포함)의
  해시 키 계산 — 를 더한다 (§2.2.3, p.42).[^linstedt2016]

### 데이터 웨어하우스 계층 (Raw Data Vault)

- 모든 이력·시간 가변 데이터를 담는 계층. hard rule 외의 어떤 업무 규칙으로도 수정되지
  않은 **원시(raw) 데이터**를 소스가 준 세분도 그대로 비휘발로 보관하고, 소스의 모든
  변경을 Data Vault 구조로 추적한다 (§2.2.4, p.42).[^linstedt2016]
- 통합은 업무 키로 이뤄지며, 주제 지향인 information mart와 달리 이 계층은 기능
  지향(function-oriented)이다 (§2.2.4, p.42).[^linstedt2016]
- 배치에서는 스테이징에서, 실시간에서는 엔터프라이즈 서비스 버스(ESB)에서 직접 공급받는다.
  모델은 [Data Vault 2.0 모델링 기법](../concepts/data-vault-modeling.md)을 따르며, 원시
  데이터를 담기에 흔히 **Raw Data Vault** 계층이라 부른다 (§2.2.4, p.42).[^linstedt2016]

### Information mart 계층

- 최종 사용자는 DW 계층에 직접 접근하지 않고 information mart만 본다 — 그래서 DW 계층이
  Data Vault 모델인 것이 사용자에게 투명하다(3정규형 마트도 제공 가능) (§2.2.5,
  p.43).[^linstedt2016]
- 이 계층의 정보는 주제 지향이고 집계·평탄화·리포팅 대비·고인덱싱·중복 허용·품질 정제된
  형태일 수 있으며, 흔히 스타 스키마를 따라 관계형 리포팅과 다차원 OLAP 큐브의 기반이
  된다 (§2.2.5, p.43).[^linstedt2016] 스타 스키마 설계는
  [차원 모델링](../concepts/dimensional-modeling.md) 참조.
- 특수 마트: Error Mart(적재 오류의 중앙 저장)와 Meta Mart(메타데이터의 중앙 저장)는
  일반 마트와 달리 Raw Data Vault에서 **재구축할 수 없다** (§2.2.5, p.43).[^linstedt2016]

## Hard rule / soft rule 분리

이 아키텍처가 전형적 아키텍처와 가장 크게 다른 점: 대부분의 업무 규칙 집행을
information mart 구축 시점으로, 즉 최종 사용자 쪽으로 옮긴다 (§2.2, p.38).[^linstedt2016]

- **Hard business rule** = 데이터 도메인을 정렬하는 기술적 규칙(데이터 타입 매칭.
  예: 스테이지 테이블 정의보다 긴 문자열의 절단, COBOL copybook·XML 정규화, 시스템
  컬럼 계산). 경험칙은 원문 그대로 (§2.2.1, pp.38–39):[^linstedt2016]

> As a rule of thumb, hard business rules never change the meaning of the
> incoming data, only the way the data is stored.

- **Soft business rule** = 업무 사용자가 진술한 업무 요구의 집행. 데이터나 데이터의
  의미를 바꾼다 — 세분도·해석의 변경, 범주 할당(소득 구간·연령대·고객 세그먼트),
  복수 소스의 통합·집계 방식 정의 (§2.2.1, p.39).[^linstedt2016]
- 적용 위치: hard rule은 늦어도 스테이징 적재 시(DB가 타입 검사로 강제), soft rule은
  Data Vault에서 information mart로 내려가는 길에 적용한다 (§2.2.2, p.39).[^linstedt2016]
- hard rule은 위반 시 ETL을 멈춰 적재를 깨뜨릴 수 있어서 soft rule과 다르게 다뤄야
  하고, 그래서 두 유형을 서로 분리한다 (§2.2.2, pp.39–40).[^linstedt2016]
- 전형적 아키텍처에서는 DW 계층이 스타 스키마든 3정규형이든 그 구조에 맞추기 위해
  soft rule까지 적재 초기에 구현된다. 문제는 규칙 변경이다: 규칙이 아키텍처 상류에
  구현될수록 상위 계층 의존성이 커진다 (§2.2.2, p.40).[^linstedt2016]
- 항공기 등록번호(N-Number) 사례: 소스의 키 의미 체계가 바뀌었을 때 Data Vault에서는
  기존 새틀라이트를 닫고 새 구조의 새틀라이트에 새 데이터를 적재할 뿐, 업무 규칙 구현
  없이 모든 데이터를 싣는다. 범주 재해석은 mart 적재 시 구현하면 되고, 역사 항공기용·
  현대 항공기용 mart를 따로 짓기도 쉽다. 적응을 위해 고쳐야 할 기존 ETL 잡은 **없다**
  (§2.2.2, pp.40–41).[^linstedt2016]

## 선택적 Vault 확장

스테이징·DW·information mart 세 계층은 (실시간 사례를 빼면) 필수이고, 다음 셋은 선택
확장이다. 셋 다 별도 계층이 아니라 DW 계층 안의 Data Vault에 통합된다 (§2.2, p.37;
§2.2.6, p.43).[^linstedt2016]

- **Metrics Vault**: 실행 이력·프로세스 메트릭·기술 메트릭(CPU·RAM·디스크 I/O·네트워크)
  등 런타임 정보를 Data Vault 2.0 기법으로 원시 저장한다. 시스템·프로세스 구동 데이터라
  감사 대상이 아니며(nonauditable), 그 위의 Metrics Mart가 성능 정보를 제공한다
  (§2.2.6, p.43).[^linstedt2016]
- **Business Vault**: 업무 규칙이 **이미 적용된** 데이터를 담는, Data Vault 설계 원칙
  기반의 성기게 모델링된(sparsely modeled) 구조. 대개 Raw Data Vault와 information
  mart 사이의 중간층으로서 mart 생성을 쉽게 한다. 소스 감사 가능성 요건이 없어서
  언제든 버리고 Raw Data Vault에서 재생성할 수 있다 (§2.2.7, pp.43–44).[^linstedt2016]
- **Operational Vault**: 운영계가 직접 읽고 쓰는 Data Vault 확장. MDM(예: Microsoft
  MDS)·메타데이터 관리 시스템·데이터 마이닝처럼 DW 계층을 직접 다루는 편이 유리한
  경우, 특히 실시간 읽기·쓰기가 필요한 인터페이스에 적합하다. SOA·ESB의 실시간 데이터는
  Operational Vault에 직접 쓴다 (§2.2.8, pp.44–45).[^linstedt2016]

## 관리형 셀프서비스 BI

- IT를 우회하는 무통제 셀프서비스 BI는 소스 직접 접근(ACL 우회)·미통합 원시 데이터·
  낮은 품질·미통합 결과·비표준 업무 규칙 문제를 낳지만, 파워 유저의 데이터 획득을 완전히
  막는 것도 불가능하다 (§2.2.9, pp.45–46).[^linstedt2016]
- Data Vault 2.0의 절충인 관리형 셀프서비스 BI(managed self-service BI): IT가 업무 키로
  통합된 원시 데이터를 Raw Data Vault에 마련하고(필요시 Business Vault로 통합 뷰·KPI
  사전계산 제공), 파워 유저는 거기서 직접 데이터를 가져다 자기 도구로 로컬 information
  mart를 만든다. IT는 서비스 조직으로 진화한다 (§2.2.9, pp.46–47).[^linstedt2016]

## NoSQL·실시간 수용

- 아키텍처는 소스의 배치 적재와 ESB 등 서비스 지향 아키텍처(SOA)로부터의 실시간 적재를
  모두 지원한다 (§2.2, p.38).[^linstedt2016]
- Data Vault 2.0은 플랫폼 독립이라 NoSQL을 스테이징·DW·정보 전달의 **모든 계층**에 쓸
  수 있다: NoSQL을 스테이징으로 써서 관계형 Data Vault에 적재할 수도, 해시된 업무 키로
  양방향 통합한 하이브리드(information mart가 양쪽 환경에서 소비)로 갈 수도 있다
  (§2.2, p.38).[^linstedt2016] 이 책 자체는 실시간·NoSQL을 범위 밖으로 두고 관계형
  부분에 집중한다 (§2.2, p.38; §2.2.10, p.47).[^linstedt2016]

[^linstedt2016]: Linstedt & Olschimke 2016, 2장 "Scalable Data Warehouse Architecture" (및 1장 §1.3)

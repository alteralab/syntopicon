---
type: concept
title: 메달리온 Silver 계층
description: "메달리온 아키텍처의 둘째 계층 — 원천 지향을 유지한 채 정제·표준화만 하고 아직 원천을 합치지 않는 계층의 규정과 설계 결정들: 정제 활동 열여섯과 격리 테이블, Bronze와 일대일로 맞출 것인가를 가르는 데이터 모델 설계(컬럼 합치와 개명, 비정규화, SCD2를 Silver에 둘 것인가의 논쟁, 대리 키는 여기에 속하지 않는다는 저자의 판정), 다른 원천과의 조화를 Gold로 미루라는 권고와 그 반대 실무, 3NF와 데이터 볼트를 Silver에 놓는 배치와 레이크하우스에서 볼트의 필요성을 되묻는 자리, 운영 질의와 기계 학습을 위한 보강의 위치, 겹치는 요구가 만드는 재사용 문제, 계층별로 자동화 난이도가 다르다는 판정과 메타데이터 주도 프레임워크, 그리고 실무의 Silver가 세척·합치·이력화 단계로 갈리거나 소유권 정렬 계층과 조화 계층 둘로 갈리는 자리"
generated: { by: "claude-opus-5", at: "2026-09-23T23:10:00Z" }
sources:
  - { id: strengholt2025, resource: /it/sources/strengholt2025.md }
---

# 메달리온 Silver 계층

- [버전 조건](#버전-조건)
- [이 계층의 규정](#이-계층의-규정)
- [정제 활동](#정제-활동)
- [데이터 모델 설계 — 컬럼 합치와 개명](#데이터-모델-설계--컬럼-합치와-개명)
- [데이터 모델 설계 — 비정규화](#데이터-모델-설계--비정규화)
- [데이터 모델 설계 — 완만하게 변하는 차원](#데이터-모델-설계--완만하게-변하는-차원)
- [데이터 모델 설계 — 대리 키](#데이터-모델-설계--대리-키)
- [다른 원천과의 조화](#다른-원천과의-조화)
- [3NF와 데이터 볼트](#3nf와-데이터-볼트)
- [운영 질의와 기계 학습](#운영-질의와-기계-학습)
- [겹치는 요구 관리](#겹치는-요구-관리)
- [자동화 — 계층마다 난이도가 다르다](#자동화--계층마다-난이도가-다르다)
- [실무에서의 Silver](#실무에서의-silver)
- [이 KB의 원전과 맞대어 본 것](#이-kb의-원전과-맞대어-본-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **Bronze와 Gold 사이의 계층은 무엇을 하고 무엇을 하지 않기로 하는가, 그리고
그 경계가 흔들리는 자리는 어디인가.**

[메달리온 Bronze 계층](../concepts/medallion-bronze-layer.md)이 넘긴 데이터를 받는 자리다. 저자는
이 계층의 일을 **정제와 보강**으로 규정하고, 다음 계층으로 넘기기 전에 무엇을 하지 않을지를 함께
못 박는다.

## 버전 조건

> **버전 조건**: 2025년 저술 시점. 아래
> [자동화 — 계층마다 난이도가 다르다](#자동화--계층마다-난이도가-다르다)의 도구 이름들과
> [3NF와 데이터 볼트](#3nf와-데이터-볼트)의 자동화 프레임워크 이름은 그 시점의 제품 지형에 묶인다.
> 그 밖의 절(정제 활동, 모델 설계의 선택, 조화를 어디로 미룰지)은 설계 판단이라 시점에 둔감하다.
> 이 소스에 공표된 만료 날짜가 없어 `stale_after`는 걸지 않는다.

## 이 계층의 규정

- 저자가 Silver에 붙이는 정의 — **원시 데이터를 정제(refine)·세척(cleanse)·표준화해 더 복잡한
  운영·분석 작업에 대비시킨다.** 이 계층에서 데이터는 품질 검사, 표준화, 중복 제거, 그리고 신뢰성과
  사용성을 높이는 다른 개선을 거친다. Silver는 **데이터가 여전히 세밀하되 품질과 일관성을 보장하도록
  처리된 전이 단계(transitional stage)**로 작동한다 (3장 §"The Three-Layered
  Design").[^strengholt2025]
- 핵심 특성은 **더 구조화되고 질의에 친화적**이 되어 분석가와 데이터 과학자가 다루기 쉬워진다는
  것이다 (3장 §"The Three-Layered Design").[^strengholt2025]
- 그림 3-1의 Silver 상자 안 문장이 같은 규정을 한 줄로 줄인다. **본문에 없고 그림에만 있다**
  (3장 §"The Three-Layered Design", 그림 3-1):[^strengholt2025]

> Transitional stage where data is still source system-aligned and granular but has been processed
> to ensure quality and consistency

- 계층이 실제로 하는 일의 목록은 절 도입이 준다 — 날짜·시각 같은 요소의 **형식 표준화**, **참조
  데이터의 강제**, **명명 표준의 합치**, **중복 제거**, 그리고 일련의 **기능적 데이터 품질 검사**.
  더해서 저품질 행은 폐기하고 무관한 데이터는 걸러 낸다 (3장 §"Silver Layer").[^strengholt2025]
- **가장 중요한 것은 하지 않는 일이다** — 저자는 "most importantly"를 붙여 **이 단계에서 데이터는
  일반적으로 아직 다른 원천의 데이터와 병합·통합되지 않는다**고 못 박는다 (3장 §"Silver
  Layer").[^strengholt2025] 이 한 줄이 아래 [다른 원천과의 조화](#다른-원천과의-조화)와
  [3NF와 데이터 볼트](#3nf와-데이터-볼트)에서 되풀이해 흔들리는 경계다.

## 정제 활동

- 출발점은 **원천에서 고치라**는 권고다. 조직은 저품질 원천 데이터를 자주 만나 철저한 세척이
  필요해지고, 많은 세척 작업이 적재·처리 국면에서 자동화될 수 있지만 **어떤 것은 운영 원천에서
  다루는 편이 더 효과적**이다. 데이터 품질 문제가 다른 데서 튀어나오는 것을 피해야 하기 때문이다 —
  예컨대 원천 시스템은 다른 애플리케이션과의 인터페이스도 가질 수 있다. 그러므로 **발원지(source
  of origination)에서 데이터 품질 문제를 고치는 것이 권고된다** (3장 §"Silver Layer" ▸ "Cleaning
  Data Activities").[^strengholt2025]
- 세척 과정은 특정 ETL 규칙으로, 어떤 경우에는 매핑 표로 통제될 수 있다. **세척 과정의 개발은
  복잡하고 흔히 여러 차례의 개정을 요구한다는 것**도 인식해야 한다 — Gold에 데이터를 적재한 뒤
  Silver로, 때로는 Bronze까지 돌아가야 해결되는 문제를 발견할 수 있다 (3장 §"Silver Layer" ▸
  "Cleaning Data Activities").[^strengholt2025]
- 저자가 예로 드는 정제 활동은 열여섯이고, 총망라가 아니라고 스스로 적는다 (3장 §"Silver Layer" ▸
  "Cleaning Data Activities"):[^strengholt2025]
  - **잡음 감소와 비진정 데이터 제거** — 불필요한 컬럼·행 같은 무관한 데이터를 없애 품질을 높이고
    저장 요구를 줄인다. 진정한(golden) 원천을 정확히 반영하지 않는 데이터의 제거도 여기 든다.
  - **결측값 처리** — 제거, 기본값 대체, 또는 주변 데이터로 추정하는 대체(imputation) 기법.
  - **중복 제거** — 보존 컴플라이언스 같은 이유로 특별히 요구되는 경우가 아니면 중복 레코드를
    없앤다. 중복은 분석을 왜곡하고 부정확한 모델로 이어진다.
  - **공백 다듬기** — 특히 문자열 타입에서 앞뒤 공백이 정렬·검색·문자열 조작에 영향을 준다.
  - **오류 정정** — 오타, 잘못된 대소문자, 잘못된 단위. **정상에서 뚜렷이 벗어나는 이상치의 탐지와
    정정**도 이 범주다.
  - **일관성 검사** — 약어·용어·측정 단위의 표준화(`NETHERLANDS`와 번갈아 쓰지 말고 `NL`로
    일관되게).
  - **형식 표준화** — 날짜 형식의 일관성(`[YYYY]-[MM]-[DD]`). 로케일에 따라 다른 형식
    (`[DD]-[MM]-[YYYY]`)을 선호할 수 있음을 인식한다.
  - **타입 교정** — 컬럼에 수치·날짜·부동소수 같은 올바른 타입을 부여한다.
  - **범위 고정** — 각 컬럼의 데이터가 지정된 값 범위를 지키는지 확인한다.
  - **유일성 고정** — 요구되는 곳에서 각 컬럼의 유일성을 유지한다.
  - **제약 고정** — 고아 컬럼이 없는지 검증한다. 각 자식 레코드는 부모 테이블의 존재하는 부모
    레코드에 대응해야 한다.
  - **민감 데이터 마스킹** — 평문으로 나타나는 PII를 쓰기 전에 가려 프라이버시를 보호하고 규제를
    지킨다.
  - **이상 탐지** — 품질 문제를 가리킬 수 있는 이상을 탐지·수정한다. 판매 데이터의 갑작스러운
    급등이 품질 문제의 신호일 수 있다.
  - **마스터 데이터 관리 적용** — 조직의 공유 핵심 데이터의 정확성·균일성·일관성을 보장하도록
    처리한다.
  - **데이터 표준화** — 주소·전화번호·위치·참조 코드 같은 데이터를 시스템 전반의 일관성·정확성을
    위해 처리한다.
  - **데이터 합치(conforming)** — 공통 데이터 모델을 써서 여러 시스템의 정보를 표준화·조화한다.
- 세척 규칙 작성은 **데이터와 그것을 생성한 업무 프로세스에 대한 깊은 이해를 요구하는 복잡한
  일**이다 (3장 §"Silver Layer" ▸ "Cleaning Data Activities").[^strengholt2025]
- 구조와 폐기에 관한 두 규정 (3장 §"Silver Layer" ▸ "Cleaning Data Activities"):[^strengholt2025]
  - **세척 후 테이블 구조는 일반적으로 Bronze와 같다.**
  - **부정확하거나 거부된 데이터는 보통 삭제하지 않는다.** 대신 플래그를 달거나 걸러 내어
    **Silver 안의 형제 격리 테이블(sibling quarantine table)**에 저장한다.

## 데이터 모델 설계 — 컬럼 합치와 개명

- Silver의 데이터 모델 설계는 메달리온의 결정적 측면이고 **가능성이 많아 흔히 뜨거운 주제**다.
  영향 요인 셋은 수집한 원천의 수, 그 원천들이 **원천 시스템을 가로질러 맞추고 관계 짓고 결합할 수
  있는 같은 핵심 요소나 객체를 공유하는 정도**, 그리고 통합된 관점을 위해 그 겹치는 핵심 요소를
  조화시킬 필요다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
  Model").[^strengholt2025]
- 기본형은 일대일이다 — 메달리온에서 **Silver와 Bronze가 테이블 면에서 곧장 일대일로 정렬되는 것이
  흔하고**, 다만 두 계층에서 데이터가 제시되는 방식이 약간 다를 수 있다 (3장 §"Silver Layer" ▸
  "Designing the Silver Layer's Data Model" ▸ "Conforming and renaming
  columns").[^strengholt2025]
- 저자가 자기 판단을 명시하는 자리 — **어디서나 표준 실무는 아니지만, 저자가 함께 일한 많은 조직이
  일관된 명명 규약을 적용하기 위해 컬럼을 개명하는 것을 Silver의 모범 사례로 여기고 저자도 그
  접근에 동의한다.** 개명하고 컬럼에 주석을 달면 이름이 서술적이고 그것이 표현하는 데이터를 진정으로
  반영하게 되어 데이터셋의 탐색과 조작이 단순해지고, 같은 데이터에 기대는 팀원 사이의 소통이
  개선돼 혼란과 처리 중 오류가 줄어든다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
  Model" ▸ "Conforming and renaming columns").[^strengholt2025]
  - 저자의 SQL 예는 두 부분이다. 먼저 주석을 단 테이블을 만든다 —
    `CREATE TABLE silver.customer (CustomerID BIGINT COMMENT 'Customer Identifier', FullName STRING COMMENT 'Customer Full Name', Region STRING COMMENT 'Region Code', SignupDate DATE COMMENT 'First Sign Up Date', LastLogin DATE COMMENT 'Last Login Date');`
    그리고 기술적 이름을 읽기 쉬운 이름으로 바꾸며 적재한다 —
    `INSERT INTO silver.customer (CustomerID, FullName, Region, SignupDate, LastLogin) SELECT custID AS CustomerID, CONCAT(f_name, ' ', l_name) AS FullName, rgcd AS Region, sigdt AS SignupDate, lldt AS LastLogin FROM bronze.cust_data;`
    (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Conforming and renaming
    columns").[^strengholt2025]
- 개명은 흔히 **테이블 안 데이터의 표준화와 합치를 함께 포함한다** — 데이터를 특정 범위에 맞추거나
  일관된 코드·라벨로 범주형 데이터를 표준화하는 것이다. Silver에서의 이런 표준화가 **Gold에서의
  변환과 통합을 더 매끄럽게** 한다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
  Model" ▸ "Conforming and renaming columns").[^strengholt2025]
- 타입 선택에 성능 근거가 붙는다 — **적절한 데이터 타입을 쓰면 암묵적 타입 변환을 막는다. 암묵
  변환은 여분의 계산 자원을 써 질의를 늦출 수 있다.** 데이터를 담을 수 있는 **가장 작은 타입**을
  고르면 저장 효율의 이득도 얻는다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
  Model" ▸ "Conforming and renaming columns").[^strengholt2025]
- 곁줄이 이 활동을 MDM에 잇는다 — Silver 테이블 안에서 특정 범위를 적용하거나 범주형 데이터를
  표준화하는 것은 **마스터 데이터 관리(MDM)와 밀접히 관련된 활동**이다. MDM은 조직의 공유
  데이터(흔히 마스터 데이터라 불리는 것)가 일관되고 정확하게 하는 데 초점을 두고, Silver 테이블
  안의 표준화가 조직 전반의 데이터 균일성·신뢰성을 높이므로 그 목표에 정렬된다 (3장 §"Silver
  Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Conforming and renaming columns"
  곁줄).[^strengholt2025]

## 데이터 모델 설계 — 비정규화

- 정의와 자리 — 질의 성능 최적화를 위해 데이터를 **더 적은 테이블로 통합**할 수 있고, 복잡한 조인의
  필요를 줄여 질의가 빨라진다. 이것을 비정규화라 부르며 **Silver에서 때때로 일어나고 Gold에서는
  더 흔하다** (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸
  "Denormalization").[^strengholt2025]
- 판단 기준이 한 줄로 주어진다 — **Silver에서 자주 재적재하고 집중적으로 읽을 것이 예상되면 더
  비정규화된 모델을 쓰는 것이 가장 낫다.** 일반적으로 더 나은 성능을 주기 때문이다 (3장 §"Silver
  Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Denormalization").[^strengholt2025]
- 비정규화 모델에서는 데이터가 **흔히 질의되는 주제 영역(subject areas)을 중심으로 조직**돼 광범위한
  조인의 필요를 없애고 **분산·열 기반 저장 아키텍처와 잘 맞는다.** 구조가 단순해져 필요한 정보에
  빠르게 접근하기 쉬워지고 질의 효율이 개선된다 (3장 §"Silver Layer" ▸ "Designing the Silver
  Layer's Data Model" ▸ "Denormalization").[^strengholt2025]
  - 저자의 SQL 예는 고객·주문·고객 상세 셋을 내부 조인으로 합쳐 한 테이블에 넣는 것이다 —
    `INSERT INTO silver.customer_return SELECT cus.CustomerID, cus.FullName, c.Region, c.SignupDate, c.LastLogin, st.OrderID, st.OrderDate, st.OrderAmount FROM silver.customers cus INNER JOIN silver.orders st ON cus.OrderID = st.OrderID INNER JOIN silver.customer_details c ON cus.CustomerID = c.CustomerID`
    (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸
    "Denormalization").[^strengholt2025]
- 대가는 볼륨이다 — 비정규화를 적용하면 **질의 성능을 개선하려고 중복 데이터를 의도적으로 더하므로
  테이블 볼륨이 커지기 시작한다.** 그 중복이 테이블에 더 많은 데이터를 저장하게 하고 시나리오에
  따라 성능에 영향을 줄 수 있다. 이 때문에 많은 조직이 **유지보수·최적화 잡으로 테이블을
  관리한다** (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸
  "Denormalization").[^strengholt2025]

## 데이터 모델 설계 — 완만하게 변하는 차원

- 필요와 구조 — 시간에 걸친 모든 변경의 포괄적 이력 기록을 세우려면 데이터를 **SCD2로 재처리**해야
  한다. `start_date`·`end_date`·`is_current` 같은 컬럼을 테이블에 더해 변경을 더 효과적으로
  추적하는 일이다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Slowly
  changing dimensions").[^strengholt2025]
- **어려움의 뿌리를 저자가 지목한다** — 이 과정은 복잡하고 도전적인데, **"변경"을 무엇으로 정의할지가
  원천 테이블과 대상 테이블 사이에서 크게 달라질 수 있기 때문**이다. 업무 키를 만들거나 해시를
  생성하는 것이 이 과정에서 결정적이다. 원천 데이터를 어떻게 다룰지 정하는 비교를 돕기 때문이다
  (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Slowly changing
  dimensions").[^strengholt2025]
  - **업무 키(business key)** — 데이터 모델링과 데이터베이스 설계에서 업무 개념이나 엔티티를
    유일하게 식별하는 데 쓸 수 있는 속성 또는 속성 집합이다. **자연 키(natural key)라고도 흔히
    불린다.** 예는 CRM 시스템의 기본 키인 `CustomerID`나 사회보장번호다 (3장 §"Silver Layer" ▸
    "Designing the Silver Layer's Data Model" ▸ "Slowly changing dimensions").[^strengholt2025]
  - **해시(hash)** — 임의 크기의 입력 데이터에서 해싱 알고리즘으로 생성된 고정 크기 결과다. 이
    유일한 결과, 곧 "해시 값"이 **데이터의 디지털 지문**으로 봉사한다 (3장 §"Silver Layer" ▸
    "Designing the Silver Layer's Data Model" ▸ "Slowly changing dimensions").[^strengholt2025]
  - 비교 범위의 규칙 — **대상 테이블의 구조가 이 과정에 영향을 주므로, 대상에 포함되지 않은 컬럼은
    비교의 일부가 되어서는 안 된다** (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
    Model" ▸ "Slowly changing dimensions").[^strengholt2025]
- **논쟁의 지형** — 데이터 엔지니어링 커뮤니티 안에는 SCD를 Silver에서 지을지 Gold로 남길지에 대한
  논쟁이 있다. **대부분의 엔지니어는 Gold가 SCD2에 더 적절하다고 주장하는데, 그런 테이블이 만들고
  저장하기 비싸고 일반적으로 덜 쓰이기 때문**이다. 그래서 Silver 테이블은 주로 **현재 레코드만**
  담아야 한다는 것이다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸
  "Slowly changing dimensions").[^strengholt2025]
- **저자가 그 다수설에 붙이는 뉘앙스가 이 절의 알맹이다** (3장 §"Silver Layer" ▸ "Designing the
  Silver Layer's Data Model" ▸ "Slowly changing dimensions"):[^strengholt2025]
  - Gold가 여러 원천을 통합·병합하는 일을 포함한다면, **원천에서 온 진정한 맥락(authentic
    context)이 결정적일 때 Silver에 이력 관점을 만드는 가치가 있을 수 있다.** 원래 맥락의 이력
    데이터에 의존하는 기계 학습 모델을 지을 때 흔히 그렇다.
  - 운영 보고를 위해서는 **이력 데이터를 원래 형태로 유지하는 것이 원천 가까이의 운영 데이터
    저장소(ODS) 필요를 없앨 수 있다.**
  - 그리고 이것이 점점 더 해당되는 조건을 저자가 지목한다 — **SaaS·아웃소싱 서비스·NoSQL 솔루션처럼
    조직이 운영 시스템의 진정한 데이터에 접근할 여지가 줄어드는 경우**다.
  - 결국 Silver에 SCD를 구현할지 말지는 뉘앙스를 포함하며 구체적 프로젝트 요구에 달렸다.

## 데이터 모델 설계 — 대리 키

- SCD 논쟁은 **Silver에 대리 키를 포함할지의 논쟁과 연결된다** (3장 §"Silver Layer" ▸ "Designing
  the Silver Layer's Data Model" ▸ "Surrogate keys").[^strengholt2025]
- 정의 — 대리 키는 레코드에 부여되는 유일 식별자로 **내재적 업무 의미가 없으나** 테이블 안에서
  레코드를 유일하게 식별하는 데 봉사한다. 보통 auto increment 기능으로 생성하거나, 여러 컬럼을
  해싱하거나 연결해 유일 식별자를 만든다. **주된 이점은 안정성과 영속성이다 — 절대 바뀌지 않는다.**
  업무 키가 바뀌어도 값이 바뀌지 않으므로 시간에 걸친 차원 속성 변경 추적에 유용하다 (3장
  §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Surrogate
  keys").[^strengholt2025]
- **저자의 판정은 명시적이다** — **대리 키는 통상 Silver에 속하지 않는다.** 다른 원천의 데이터가
  결합·병합되어 차원 테이블과 팩트 테이블을 짓는 **다음 단계가 대리 키를 처음 만들어야 하는
  자리**다. 그 단계에서 테이블들이 자연 키·업무 키로 조인되어 대리 키를 조회하고 덧붙인다. 그러므로
  **Silver는 대리 키를 만드는 것이 아니라 데이터셋을 정제하고 더 잘 표현하는 데 초점을 두어야
  한다** (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸ "Surrogate
  keys").[^strengholt2025]
- 예외 경로도 적어 둔다 — 모든 SCD에 대리 키를 쓰려는 선호가 강하다면 **Silver와 Gold 양쪽에
  구현하는 것이 가능하다.** 이 시나리오에서 Silver에서 생성된 대리 키는 **Gold의 대응 대리 키를
  찾는 조회 키**로 쓰일 수 있다. 작동할 수 있는 접근이지만 계층 간 데이터 일관성과 무결성을
  보장하려면 세심한 구현이 필요하다 (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data
  Model" ▸ "Surrogate keys").[^strengholt2025]
- 설계 절의 맺음 — Silver와 Bronze는 밀접히 정렬되지만 데이터가 제시되는 방식에는 약간의 차이가
  있다(컬럼이 개명될 수 있고 데이터가 표준화를 거치며 기저 저장이 성능을 위해 최적화된다). 이
  수정들에도 **데이터는 통상 원천 지향(source-oriented) 성격을 유지하고 이 단계에서 다른 원천의
  데이터와 통합되지 않는다** (3장 §"Silver Layer" ▸ "Designing the Silver Layer's Data Model" ▸
  "Surrogate keys").[^strengholt2025]

## 다른 원천과의 조화

- 저자가 자주 받는 질문이 **Silver 안에서 원천들이 이미 통합되어 통합·전사 관점이 만들어져야
  하는가**이고, 이런 활동은 뉘앙스가 있다고 적는다 (3장 §"Silver Layer" ▸ "Harmonization with
  Other Sources").[^strengholt2025]
- **일반적 조언은 분리해 두라는 것**이다. 관리가 쉬워지고 관심사의 격리가 명확해지기 때문이다. 이를
  위해 **다른 원천 시스템의 데이터를 조기에 병합·통합하지 말 것**을 권고한다. 그렇게 하면
  **애플리케이션 사이에 불필요한 결합 연결(coupled connections)이 생길 수 있다.** 저자의 예 —
  한 원천의 데이터에만 관심 있는 사용자가, 데이터가 Bronze에 적재된 직후 결합되면 의도치 않게 다른
  시스템에 묶일 수 있고 그 결과 다른 시스템의 영향을 받게 될 수 있다 (3장 §"Silver Layer" ▸
  "Harmonization with Other Sources").[^strengholt2025]
- 그래서 **격리된 설계가 목표라면 다른 원천의 통합·결합을 Gold로 옮기는 것이 낫다.** 이 전략은
  명확한 경계 유지와 시스템 간 의존 최소화에 맞는다 (3장 §"Silver Layer" ▸ "Harmonization with
  Other Sources").[^strengholt2025]
- **같은 철학이 데이터 소유권 쪽으로 확장된다** — 이 철학은 레이크하우스를 아키텍처의 원천 시스템
  쪽과 정렬시키는 데에도 적용된다. 따라서 **(원천 시스템 정렬) 데이터 프로덕트를 짓고 데이터 소유권
  정렬에 관심이 있다면, 서로 다른 도메인의 애플리케이션 데이터를 조기에 교차 조인하지 말 것**을
  엔지니어에게 경고한다 (3장 §"Silver Layer" ▸ "Harmonization with Other
  Sources").[^strengholt2025]
- 반대 실무도 본다고 적는다 — 어떤 조직은 Silver에서 여러 원천의 데이터를 통합하는 쪽을 선호한다.
  그 시나리오에서 **Silver는 더 전통적인 데이터 통합 계층으로 작동해**, 최종 소비를 위해 Gold로
  옮기기 전에 엔티티를 가로질러 데이터가 결합·조화되게 한다. 이 접근에서는 **3NF나 데이터 볼트 같은
  더 전통적인 데이터 모델링 기법**이 쓰이는 것을 일반적으로 본다 (3장 §"Silver Layer" ▸
  "Harmonization with Other Sources").[^strengholt2025]

## 3NF와 데이터 볼트

- 3NF는 중복과 의존을 줄이기 위해 **운영·거래 데이터베이스 정규화에 흔히 쓰이는 모델링 기법**이고,
  일부 실무자는 **데이터 중복 감소·적응성·데이터 일관성 개선** 때문에 레이크하우스에 3NF나 다른
  정규형을 선호한다 (3장 §"Silver Layer" ▸ "3NF and Data Vault").[^strengholt2025]
- 데이터 볼트는 3NF 원리를 확장해 또 하나의 정규화 모델링 기법을 들인다 — **허브(유일 업무 키),
  링크(데이터 연결), 새틀라이트 테이블(데이터에 대한 상세 서술 정보)**이라는 고유 요소를 결합해
  3NF 개념 위에 세운다 (3장 §"Silver Layer" ▸ "3NF and Data Vault").[^strengholt2025]
- **이 소스가 데이터 볼트에 내리는 계층 배치가 이 절의 핵심 claim이다** (3장 §"Silver Layer" ▸
  "3NF and Data Vault"):[^strengholt2025]
  - **데이터 볼트 모델링 개념의 실무 적용은 일반적으로 메달리온의 Silver 계층에서 일어난다.**
  - **이 계층이 raw data vault와 business vault 둘 다를 호스트한다.** raw vault는 원시 데이터의
    구조화·정규화된 표현을 개념적 업무 모델에 매핑해 제시하고, 업무 키로 여러 원천을 통합하며
    **스키마 드리프트에 대한 회복력**을 보장하고 이력 변경을 추적한다.
  - Silver는 **조화와 중간 변환 같은 business vault 요소**도 포함해 데이터를 풍부하게 하고 전사
    정의에 정렬시킨다. **PIT(point-in-time)와 브리지 테이블**이 성능과 질의를 더 개선해 Gold에서
    쓸 데이터를 준비한다.
  - **이 설정에서 Bronze와 Gold의 역할은 대체로 바뀌지 않는다** — Bronze는 원시 데이터 스테이징
    영역으로, Gold는 비즈니스 인텔리전스와 분석을 위해 데이터를 변환하는 자리로 남는다.
- 데이터 볼트 구조는 **적응성**으로 알려져 데이터 구조와 업무 규칙이 자주 바뀌는 환경에서 탁월하고,
  복잡한 데이터 요구를 가진 조직에 특히 적합하다. 기업이 3NF나 데이터 볼트를 메달리온 안에서 선호할
  이유 넷은 이렇다 (3장 §"Silver Layer" ▸ "3NF and Data Vault"):[^strengholt2025]
  - **높은 통합 요구** — 여럿의 이질적 원천 시스템을 가진 기업이 통일되고 통합되고 일관된 데이터
    모델을 만드는 능력에서 이득을 본다.
  - **복잡한 전사 환경** — 여러 도메인에 걸쳐 운영되거나 분산된 팀을 가진 조직이 3NF·데이터 볼트가
    주는 유연성과 모듈성을 요구한다.
  - **빠르게 변하는 요구와 스키마 드리프트** — 데이터 볼트의 변화 회복력과 진화하는 스키마에의
    적응 능력이 업무·기술 요구가 자주 바뀌는 동적 환경에 이상적이다.
  - **복잡한 시간 차원의 효과적 관리** — 데이터 볼트 모델은 **같은 레코드 안의 여러 활성 타임라인**
    (생성 시각, 기능적 처리 시각, 적재 시각)을 효과적으로 관리할 수 있고, 이 능력이 감사·컴플라이언스·
    상세 이력 분석에 결정적인 데이터 진화의 추적과 이해를 높인다.
- **그러나 저자의 평가는 유보적이다** (3장 §"Silver Layer" ▸ "3NF and Data
  Vault"):[^strengholt2025]
  - 이 모델링 기법들이 유연성 개선과 저장 비용 절감을 겨냥하지만 **확장성 우려 때문에 클라우드
    기반 데이터 아키텍처에서는 일반적으로 덜 선호된다.** 실무자는 흔히 **넓고 중첩되고 비정규화된
    테이블**을 택하는데 그 구성이 클라우드 인프라 효율을 최대화하기 때문이다. **비정규화 테이블은
    계산적으로 비싼 조인과 Spark 컴퓨트 노드 사이의 데이터 셔플링을 피하고**, 그 둘이 질의 성능을
    크게 늦출 수 있다.
  - 구축 자체가 복잡하고 보통 더 많은 시간·자원을 요구한다. 두 모델 다 데이터 관계와 의존의
    상세한 이해를 요구해 철저한 계획·분석이 필요하고, 무결성과 효과성을 유지하려면 엄격한 규칙·
    구조를 지켜야 한다. 이 도전에 대응해 조직은 **VaultSpeed 같은 자동화 프레임워크**의 잦은 검토와
    구현을 고려할 수 있다.
  - **레이크하우스 아키텍처의 유연성 자체가 되묻게 만든다** — 실무자로 하여금 데이터 볼트처럼
    무겁게 정규화된 모델을 채택할 필요가 있는지 묻게 하고, 특히 큰 스키마 변경이 걱정이 아니라면
    그렇다. **메달리온은 질의 가능한 원시 원본 테이블을 통해 Bronze에서의 재적재를 단순화하고,
    Delta는 타임 트래블을 지원해 Silver 데이터를 이전 버전으로 빠르게 롤백할 수 있게 한다.**
  - 그래서 조직은 **실용적 이유로 더 큰 비정규화 테이블을 흔히 고른다.** 더 나은 성능, 사용의
    용이함, 전반 설계의 단순화가 이유이고, **성능과 단순성이 엄격한 정규화보다 우선되는 환경**에서
    특히 매력적이다.
- 절의 맺음 둘 (3장 §"Silver Layer" ▸ "3NF and Data Vault"):[^strengholt2025]
  - 데이터 모델링은 복잡한 주제이고 구체적 업무 필요와 맥락에 맞춘 전략적이고 뉘앙스 있는 접근을
    요구한다. **접근은 단순히 흑이나 백이 아니다** — 조직의 구체적 요구와 제약에 따라 여러 유스케이스에
    맞는 다른 모델링 전략을 고를 수 있다.
  - **Silver에서 원천을 통합할지 결정하는 것이 어느 정도의 전사 표준화 적용을 막지는 않는다.**
    데이터 타입, 중앙 관리 참조 데이터, 명명 규약 같은 정의된 표준에의 합치는 권장된다. 일부 고객은
    새 값 계산 같은 **기본 업무 규칙**도 구현한다. **그러나 그런 활동은 최소로 유지해야 한다** —
    Silver는 데이터를 무겁게 증강하고 복잡한 업무 규칙을 적용하기보다 **데이터가 깨끗하고
    표준화되게 하는 데 주로 초점**을 두어야 한다.

## 운영 질의와 기계 학습

- 왜 이 계층이 ML의 자리가 되는가 — **기계 학습 모델은 훈련 데이터가 다루려는 업무 문제의 구체적
  맥락이나 도메인에 밀접히 정렬될 때 최고 성능을 낸다.** 그래서 많은 조직이 Silver를 운영 질의와
  기계 학습 작업부하에 곧바로 활용한다 (3장 §"Silver Layer" ▸ "Operational Querying and Machine
  Learning").[^strengholt2025]
- 그러나 이것이 **데이터를 더 보강할지의 논쟁**으로 이어진다. 특히 기계 학습 애플리케이션에서
  그렇다. 예컨대 범주형 데이터를 수치 형식으로 변환하면 기계 학습 알고리즘의 처리가 단순해진다.
  **많은 조직이 피처 엔지니어링과 모델 훈련을 위한 추가(샌드박스 또는 기계 학습) 계층의 필요를
  인식해 데이터 아키텍처에서 통상의 세 계층을 넘어선다** (3장 §"Silver Layer" ▸ "Operational
  Querying and Machine Learning").[^strengholt2025]
- 보강을 어디에 둘지의 권고가 둘로 갈린다 (3장 §"Silver Layer" ▸ "Operational Querying and
  Machine Learning"):[^strengholt2025]
  - 데이터 보강이 필요한 **운영 보고**를 가능하게 하는 것이 목표라면 **Silver에서 보강을 시작할
    것을 권고**한다. Gold 단계의 병합 중 추가 조정이 필요할 수 있지만 **늘어난 유연성이 그만한
    값어치가 있다.**
  - 반대로 유연성 유지와 관리 편의를 위한 관심사 분리를 중시한다면 **Gold까지 보강을 미루는 것을
    고려**하라. 이 전략은 관심사를 격리하고 관리를 단순화해 복잡한 데이터 구조를 다루는 데 효과적인
    접근이 된다.

## 겹치는 요구 관리

- 업무 규칙을 Silver에 둘지 Gold에 둘지에 대한 엔지니어들의 계속되는 논쟁이 있고, 이 논의는 흔히
  **재사용성과 표준화**를 축으로 돈다 (3장 §"Silver Layer" ▸ "Managing Overlapping
  Requirements").[^strengholt2025]
- 저자의 제안 — **일반적으로 Silver에서는 변환을 최소로 유지하라.** 최종 사용을 위해 설계된 Gold가
  업무 규칙을 두어야 할 자리다. 그래야 구체적 유스케이스 요구에 맞춘 커스터마이즈가 가능하고
  갱신·유지보수의 관리가 쉬워진다 (3장 §"Silver Layer" ▸ "Managing Overlapping
  Requirements").[^strengholt2025]
- **그러나 이 접근이 낳는 합병증을 저자가 함께 적는다** — 같은 통합이 다른 팀에 의해 자주 재사용돼야
  할 때다. **Gold의 데이터가 최초의 한 업무 단위에 특화되면, 같은 데이터가 필요한 다른 팀이 그
  로직을 다시 짓게 될 수 있다.** 이것이 Silver와 Gold를 어떻게 구조화하고 어디서 데이터를 보강·변환할지에
  대한 **사려 깊은 계획의 필요**를 부각한다 (3장 §"Silver Layer" ▸ "Managing Overlapping
  Requirements").[^strengholt2025]

## 자동화 — 계층마다 난이도가 다르다

- 전제 — **확장성의 열쇠는 대부분의 작업을 자동화하는 데 있다.** 그러나 메달리온의 여러 계층에 걸친
  **모든 처리 단계가 같은 정도로 쉽게 표준화·자동화될 수 있는 것은 아니다** (3장 §"Silver Layer" ▸
  "Automation Tasks").[^strengholt2025]
- **원천에서 Bronze로의 이행이 특히 도전적**이다. 원천 시스템 쪽 기술과 벤더 솔루션의 다양성에서
  오는 복잡성 때문이다. 어떤 벤더는 데이터 추출에 고유 API나 독점 서비스를 써서 다양한 데이터
  형식이 나온다. 벤더가 CSV 내보내기 형식만 지원하면 거기 맞춰 프로세스를 조정해야 한다 (3장
  §"Silver Layer" ▸ "Automation Tasks").[^strengholt2025]
- 그림 3-3이 그 난이도를 세 구획으로 그리고, **구획 이름은 그림에만 있다** (3장 §"Silver Layer" ▸
  "Automation Tasks", 그림 3-3):[^strengholt2025]

> Hard to automate (Source systems ↔ Bronze) · Easy to automate (Bronze → Silver) ·
> Hard to parameterize (Gold → Use cases)

  - 원천 시스템과 Bronze 사이에는 `Pull`과 `Push` 두 화살표가 양방향으로 그려져 있고, 오른쪽 끝의
    상자 이름은 `Use cases`다 (3장 §"Silver Layer" ▸ "Automation Tasks", 그림
    3-3).[^strengholt2025]
- 초기 장벽을 넘어 데이터가 표준화된 (Delta Lake) 형식으로 Bronze와 Silver에 있게 되면 추가
  표준화·자동화로 나아갈 수 있다. 이 단계에서 **도구와 메타데이터 주도 프레임워크가 결정적**이 되어
  더 매끄럽고 자동화된 처리를 가능하게 한다 (3장 §"Silver Layer" ▸ "Automation
  Tasks").[^strengholt2025]
- Bronze에서 Silver로의 전이는 일반적으로 더 직선적이다. 이 단계의 변환은 대개 **예측 가능하고
  비교적 단순**해서 컬럼 개명, 필터 적용, 데이터 품질 문제 수정, 조회 테이블 활용, 기본값 설정
  같은 일을 포함한다. **예측 가능한 성질 덕분에 이 국면은 파라미터화가 쉬워** 더 효율적이고 관리
  가능해진다 (3장 §"Silver Layer" ▸ "Automation Tasks").[^strengholt2025]
  - 각주가 파라미터화를 정의한다 — **데이터 변환 파이프라인의 처리 단계를 제어하기 위해 파라미터를
    정의하고 사용하는 기법이고, 여기서 파라미터는 스크립트나 노트북의 기저 코드를 바꾸지 않고
    외부에서 조정할 수 있는 변수나 설정**이다 (3장 각주 6).[^strengholt2025]
- 그래서 많은 조직이 공통 스크립트·노트북을 갖춘 **메타데이터 주도 프레임워크**에 기댄다. 이
  프레임워크는 데이터 엔지니어링 작업을 **선언적으로** 정의하게 한다. 스키마 정보, 데이터 품질 규칙,
  자연 키와 업무 키, 매핑 규칙 같은 핵심 요소가 전부 **메타데이터 저장소** 안에 저장되고, 그
  저장소가 변환 코드를 자동 생성하는 데 활용된다. **메타데이터만 갱신하면 변환을 손쉽게 수정할 수
  있어** 데이터 엔지니어링 과정이 크게 자동화된다 (3장 §"Silver Layer" ▸ "Automation
  Tasks").[^strengholt2025]
- 고려할 다른 프레임워크 둘 — **dbt**는 SQL의 `SELECT` 문과 비슷한 문법의 템플릿으로 변환을 정의하게
  해 뛰어나고, **Delta Live Tables(DLT)**는 특히 Databricks 환경에서 일하는 이들에게 고려할 선언적
  데이터 엔지니어링 프레임워크로 **변환뿐 아니라 태스크 오케스트레이션·클러스터 관리·모니터링·
  데이터 품질·오류 처리까지 관리**한다 (3장 §"Silver Layer" ▸ "Automation
  Tasks").[^strengholt2025]
- 마지막 단계(정제된 데이터를 소비자의 고유 요구에 맞춰 전달하는 것)는 **파라미터화가 어렵다.**
  통합에 흔히 요구되는 복잡한 업무 로직이 메타데이터만으로 쉽게 포착되지 않기 때문이다. 다만
  템플릿과 서비스를 써서 워크플로에 어느 정도의 표준화를 들일 수 있다 (3장 §"Silver Layer" ▸
  "Automation Tasks").[^strengholt2025]

## 실무에서의 Silver

- 계층의 일을 저자가 한 문단으로 되짚는다 — Silver에서는 원시 데이터를 정제·표준화·(약간) 보강한다.
  주 초점은 **데이터셋의 표현을 정제하고 개선하는 것**이다. 최소한의 변환과 증강을 적용하고, 데이터
  품질 검사를 수행하며, 데이터가 깨끗하고 쓸 수 있고 표준 형식이 되게 한다. Silver는 또한 데이터가
  **질의 가능하고 Gold에서의 추가 처리에 대비**되게 한다 (3장 §"Silver Layer" ▸ "The Silver Layer
  in Practice").[^strengholt2025]
- 곁줄이 이 계층의 쓰임을 한 문장으로 못 박는다 — **Silver에서 원천 정렬 데이터를 정제·변환해 운영
  일관성을 확보하라. 이 접근이 단일 진실 원천을 유지하게 해, 전통적 운영 데이터 저장소를 더 동적이고
  확장 가능한 레이크하우스 솔루션으로 효과적으로 대체한다** (3장 §"Silver Layer" ▸ "The Silver
  Layer in Practice" 곁줄).[^strengholt2025]
- Silver 자체가 단일 물리 계층인지 여러 단계를 포함하는지는 대체로 조직의 구체적 요구에 달렸다
  (3장 §"Silver Layer" ▸ "The Silver Layer in Practice"):[^strengholt2025]
  - 감사 가능성을 높이려면 **이 계층을 뚜렷한 세 단계로 나눌 수 있다** — 세척을 위한 단계, 표준에
    합치시키기 위한 단계, 그리고 잠재적으로 SCD를 짓기 위한 셋째 단계다.
  - **데이터 소유권 정렬과 데이터 통합을 둘 다 원한다면 별도 계층 둘을 세우는 것을 고려하라** —
    원천 시스템 정렬 정제 데이터를 위한 하나와 조화된 데이터를 위한 하나다. 어느 접근을 택하든
    **각 단계를 명확하고 일관되게 유지하는 것이 결정적**이다.
- 그 실물이 그림 3-4이고, **본문에 없는 두 라벨이 그림에만 있다** (3장 §"Silver Layer" ▸ "The
  Silver Layer in Practice", 그림 3-4):[^strengholt2025]
  - Silver 계층 상자 안이 원천별로 **두 칸**으로 갈린다 — `Cleaned and conformed tables`와
    `Historized tables`다. 곧 위 "세 단계" 서술의 둘째·셋째가 그림에서는 나란한 두 칸이 된다.
  - 왼쪽 아래에 **`Governance boundary`라는 점선 경계**가 새로 등장해 CRM 시스템과 Kafka, 그리고
    그 줄의 Bronze·Silver 칸들을 감싼다. 곧 **계층 경계와 거버넌스 경계가 직교한다** — 한 계층
    안에서도 원천에 따라 거버넌스 경계가 갈린다.
- Silver는 통상 **Bronze를 거울처럼 비추되** 결정적 개선을 붙인 정확한 표현을 제시한다 — 테이블이
  정제되고 데이터가 표준화된다. 이 단순한 설정이 일반적으로 대부분의 조직 필요에 맞는다. 그러나
  Silver의 아키텍처는 **데이터의 복잡도, 관련된 원천 시스템의 수, 조직의 구체적 성능·유연성 요구**에
  따라 조정될 수 있다 (3장 §"Silver Layer" ▸ "The Silver Layer in Practice").[^strengholt2025]

## 이 KB의 원전과 맞대어 본 것

- **데이터 볼트의 계층 배치.** [Data Vault 2.0 아키텍처](../concepts/data-vault-architecture.md)가
  staging → raw vault → business vault → 정보 마트의 3계층을 세운다면, 이 소스는 **그 계층들을
  메달리온 셋에 겹쳐 놓는다** — Bronze가 스테이징, Silver가 raw vault와 business vault 둘, Gold가
  정보 마트다. 두 서술은 같은 구조의 다른 좌표계라 어긋나지 않는다.
- **볼트에 대한 평가는 갈린다.** linstedt 쪽이 데이터 볼트의 확장성을 **모델의 확장성**(변경 흡수,
  병렬 적재, 엔티티 추가)으로 세운다면, 이 소스는 **클라우드 컴퓨트의 확장성**(조인 비용, Spark
  노드 간 셔플링)을 근거로 "덜 선호된다"고 적는다. **같은 낱말이 다른 대상을 가리키므로 사실 충돌이
  아니다** — 최대 하나만 참일 수 있는 관계가 아니다. 이 페이지에는 `contradicts`를 걸지 않았다.
- **업무 키.** [업무 키](../concepts/business-key.md)는 linstedt의 요건(유일성·불변성·범위)을
  갖는다. 이 소스가 더하는 것은 **자연 키와 같은 것이라는 명시**와 SCD2 비교에서 해시와 짝을 이루는
  쓰임이다.
- **대리 키의 생성 시점.** [차원 테이블](../concepts/dimension-table.md)의 대리 키 절과
  [ETL 34 서브시스템](../concepts/etl-subsystems.md)의 대리 키 생성기·파이프라인이 "차원을 먼저
  갱신해 차원 테이블이 키의 정본이 되게 한다"를 세운다면, 이 소스는 그 절차를 **계층의 언어로
  번역**해 "대리 키는 Silver가 아니라 원천이 합쳐지는 다음 계층에서 처음 만든다"로 적는다. 같은
  규칙의 다른 표현이다.
- **SCD의 자리.** [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)이 타입
  0–7의 지형을 갖는다면, 이 소스는 **그것을 어느 계층에 둘 것인가의 논쟁**을 더한다. 다수설(Gold)과
  저자의 뉘앙스(ML·운영 보고·원천 접근이 줄어드는 SaaS 환경에서는 Silver)가 그 내용이다.
- **비정규화.** [정규화와 비정규화](../concepts/normalization-and-denormalization.md)가 Normalizer·
  Denormalizer 패턴으로 이 선택을 다룬다면, 이 소스는 그 선택을 **계층에 배치**한다 — Silver에서
  때때로, Gold에서 더 흔히.
- **정제와 표준화.** [수명 주기의 변환 단계](../concepts/transformation-in-the-lifecycle.md)와
  [마스터 데이터 관리](../concepts/master-data-management.md)가 같은 활동을 각각 수명 주기와 조직의
  언어로 갖는다. 이 소스의 기여는 **열여섯 항목의 목록**과 **거부된 데이터를 격리 테이블에 둔다**는
  처분 규칙이다.
- **도메인 경계.** [데이터 메시](../concepts/data-mesh.md)와
  [데이터 프로덕트](../concepts/data-products.md)가 도메인 소유권을 원칙으로 세운다면, 이 소스는
  그것을 **모델링 지침으로 번역**한다 — "서로 다른 도메인의 애플리케이션 데이터를 조기에 교차
  조인하지 마라".

## 이어지는 페이지

- [메달리온 Bronze 계층](../concepts/medallion-bronze-layer.md) — 이 계층이 받는 앞자리
- [메달리온 Gold 계층](../concepts/medallion-gold-layer.md) — 이 계층이 넘기는 다음 자리
- [메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md) — 계층 셋의 정의
- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — 타입 0–7의 원전
- [업무 키](../concepts/business-key.md) · [Data Vault 해싱](../concepts/hashing-in-data-vault.md) —
  비교의 두 재료
- [Data Vault 2.0 아키텍처](../concepts/data-vault-architecture.md) ·
  [Data Vault 모델링](../concepts/data-vault-modeling.md) ·
  [Business Vault](../concepts/business-vault.md) ·
  [PIT·Bridge 테이블](../concepts/point-in-time-and-bridge-tables.md) — 이 계층이 호스트한다고
  저자가 적은 것들의 원전
- [정규화와 비정규화](../concepts/normalization-and-denormalization.md) — 비정규화의 일반 원리
- [표준 차원](../concepts/conformed-dimension.md) — "합치"가 차원 쪽에서 갖는 뜻
- [차원 테이블](../concepts/dimension-table.md) · [ETL 34 서브시스템](../concepts/etl-subsystems.md)
  — 대리 키를 언제 만드는가의 원전
- [수명 주기의 변환 단계](../concepts/transformation-in-the-lifecycle.md) — 정제·표준화가 놓이는 단계
- [마스터 데이터 관리](../concepts/master-data-management.md) — 표준화 곁줄이 가리키는 실무
- [데이터 품질 관리](../concepts/data-quality-management.md) — 품질을 조직의 일로 보는 쪽
- [데이터 메시](../concepts/data-mesh.md) · [데이터 프로덕트](../concepts/data-products.md) —
  도메인 소유권과 교차 조인 경고가 닿는 자리
- [메달리온 아키텍처 구축](../synthesis/building-medallion-architectures.md) — **이 페이지가
  걸린 허브.** 이 원전의 스물두 페이지가 부 단위로 모여 있다
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 그 허브의 부모 축

[^strengholt2025]: Piethein Strengholt, *Building Medallion Architectures: Designing with Delta
    Lake and Spark*, O'Reilly 2025 ([소스](../sources/strengholt2025.md)). 스냅샷이 EPUB이고
    **인쇄판 쪽 앵커가 없어** locator는 장·절 단위다 — `N장 §"절 제목"`(원문 절 제목 그대로),
    소절은 `▸`로 잇고 곁글·곁줄은 제목 뒤에 각각 `곁글`·`곁줄`을 붙인다. 3장 실측: 절(`sect1`)
    다섯 · 소절(`sect2`) 스물셋 · 소소절(`sect3`) 일곱 · 곁글 하나 · 곁줄 아홉(note 다섯 ·
    tip 셋 · warning 하나) · 표 하나 · 도판 다섯(그림 3-1~3-5) · 코드 목록 넷(python 하나 ·
    sql 둘 · json 하나) · 각주 여덟(`data-type="noteref"` 마커 기준). **코드는 펜스 없이
    인라인으로 옮겼고** 지면 폭 때문에 접힌 줄을 한 줄로 이은 것 말고는 원문 그대로다.
    **도판의 라벨은 이미지에만 있어**(`alt`가 비어 있다) `OEBPS/assets/`의 PNG를 직접 읽어 옮겼다.

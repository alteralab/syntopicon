---
type: concept
title: 메달리온 아키텍처의 정의와 계보
status: draft
description: "레이크하우스에 데이터를 논리적으로 배치하는 Bronze·Silver·Gold 3계층이 무엇이고 어디에서 왔는가 — 데이터 공급자·분배 플랫폼·데이터 소비자와 그 위를 덮는 메타데이터·거버넌스라는 저자의 3계층 좌표와 modern data stack이 완결된 플랫폼이 아니라는 진단, 메달리온의 한 문장 정의와 계층 셋의 규정, 계보 셋(1990년대 웨어하우스의 계층화·데이터 모델링·하드웨어 결합이라는 교훈 셋, 2000년대 중반 데이터 레이크가 남긴 HDFS·MapReduce·Hive와 작은 파일 산수와 읽기 스키마 오해, 2013년 이후 Spark와 Databricks와 오픈 테이블 형식 셋의 연표와 레이크하우스), 2025년 저술 시점의 제품 지형, 그리고 메달리온이 기존 아키텍처의 진화가 아니라 Databricks가 만든 설계 패턴이며 이름이 실무 지침을 대신하지 못한다는 저자의 판정"
generated: { by: "claude-opus-5", at: "2026-09-23T16:00:00Z" }
sources:
  - { id: strengholt2025, resource: /it/sources/strengholt2025.md }
---

# 메달리온 아키텍처의 정의와 계보

- [이 책이 자기에게 준 규정](#이-책이-자기에게-준-규정)
- [버전 조건](#버전-조건)
- [저자가 세우는 좌표 — 3계층 아키텍처](#저자가-세우는-좌표--3계층-아키텍처)
- [메달리온 아키텍처의 정의](#메달리온-아키텍처의-정의)
- [계보 하나 — 웨어하우스가 남긴 것](#계보-하나--웨어하우스가-남긴-것)
- [계보 둘 — 데이터 레이크가 남긴 것](#계보-둘--데이터-레이크가-남긴-것)
- [계보 셋 — 레이크하우스](#계보-셋--레이크하우스)
- [2025년 저술 시점의 레이크하우스 제품 지형](#2025년-저술-시점의-레이크하우스-제품-지형)
- [저자의 판정 — 메달리온은 진화의 산물이 아니다](#저자의-판정--메달리온은-진화의-산물이-아니다)
- [이 KB의 다른 계보 서술과 맞대어 본 것](#이-kb의-다른-계보-서술과-맞대어-본-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **메달리온 아키텍처란 무엇이고, 어떤 계보의 끝에 놓이며, 왜 이름만으로는
지침이 되지 못하는가.**

## 이 책이 자기에게 준 규정

- 집필 계기는 워크숍의 질문 더미다 — 저자는 2024년 초 한 주에 세 번째 아키텍처 설계 워크숍을
  준비하던 중 참가자들이 메달리온 아키텍처를 두고 쏟아 낸 물음들(모범 사례는 무엇인가, 다른
  기업은 무엇을 하는가, 여러 도메인에 걸친 큰 조직에도 유효한 패턴인가, 데이터 메시가
  레이크하우스 아키텍처를 대체하는가, Silver 계층은 실무에서 어떻게 구현하는가)을 계기로 책을
  쓰기로 했다고 적는다 (Preface 도입).[^strengholt2025]
- 문제 진단은 정의의 부재다 — 계층으로 관심사를 단순하게 나누는 접근인데도 **명확한 정의와
  서술적 지침이 지속적으로 없어서** 조직 안에 혼란과 비효율이 생긴다는 것이 저자가 반복해서
  겪은 것이다 (Preface 도입).[^strengholt2025]
- 집필 전에 실무자 설문을 돌렸고 그 결과가 범위를 정했다 — 대다수가 원한 것은 실습형 안내서와
  데이터 메시·생성형 AI 같은 복잡한 주제의 통찰이었고, 거버넌스와 보안의 중요성과 다른 조직의
  실제 경험을 배우려는 요구가 컸다 (Preface 도입).[^strengholt2025]
  - 그래서 **의도적으로 뺀 것**을 저자가 명시한다 — CI/CD, DataOps, 기계 학습, 데이터 계보,
    업무 데이터 모델링은 깊이 다루지 않는다. 가치 있지만 각자 별도의 탐구를 요구해 이 책의
    범위 밖이라는 것이다 (Preface 도입).[^strengholt2025]
- 독자 규정은 넓다 — 새 데이터 플랫폼을 세우려는 사람, 이미 있는 것을 개선하려는 사람, 메달리온
  아키텍처가 무엇인지 궁금한 사람이고, 역할로는 데이터 엔지니어링 팀원·전사 아키텍처 그룹·최고
  데이터 책임자·데이터 엔지니어·데이터 과학자·데이터 관리자를 든다
  (Preface §"Who Should Read This Book").[^strengholt2025]
- 기술 선택의 규정도 서문이 못 박는다 — II부는 Azure 기술 스택, 특히 Microsoft Fabric으로
  들어가지만 **홍보 목적도 아니고 다른 서비스와의 직접 비교도 아니다.** 저자는 **빠르게 바뀌지
  않을, 자리를 잡은 서비스와 기능에 초점을 맞추기로 선택**했다고 적고 Apache Airflow·(Azure)
  Data Factory·PySpark·메타데이터 주도 방법을 그 예로 든다
  (Preface §"Navigating This Book").[^strengholt2025]
- I부 도비라가 이 세 장의 자리를 규정한다 — I부는 **이론적 토대**를 주기 위한 부이고, 1장은
  데이터 아키텍처의 역사적 전개를 훑어 이 시스템들의 기원과 여전히 영향을 주는 지속적 설계
  원칙과 수십 년의 교훈을 다룬다. 저자는 1장을 **메달리온 아키텍처와 다른 데이터 시스템을
  공부할 때 되풀이해 나올 토대 개념을 잡으려는 사람에게 결정적**이라고 적는다
  (I부 도비라).[^strengholt2025]
- 추천사(Advancing Analytics의 CTO 사이먼 화이틀리)는 이 책이 메우려는 구멍을 반대편에서
  적는다 — 메달리온 아키텍처는 **널리 오해받는 개념**이고, 너무 자주 **경직된 단계별 프레임워크로
  취급되지만 실제로는 변해 가는 지형을 이해하기 위한 유연한 접근**이라는 것이다. 화이틀리는
  그것을 **10년에 걸친 유기적 진화와 기술 혁신을 비기술 사용자에게 제시할 수 있는 개념으로
  단순화하려는 시도**로 규정하고, 단순화의 대가로 **논쟁과 오해와 좌절의 큰 틈이 남았다**고
  적는다 (Foreword).[^strengholt2025]
  - 화이틀리가 이 책에 돌리는 기여는 **왜**다 — 어떤 절차를 구현하는지만이 아니라 왜 그 절차가
    필요하고 그 과정에서 어떤 결정을 내렸는지를 주므로, 읽는 사람이 자기 구현에 어떤 절차와
    방법을 채택할지 스스로 정할 수 있게 된다는 것이다 (Foreword).[^strengholt2025]

## 버전 조건

- **이 페이지의 claim은 2025년 저술 시점의 것이다.** 1장은 역사 서술이 본체라 대부분 시점에
  둔감하지만, 제품과 벤더를 세는 대목은 그렇지 않다. 그 대목은 아래
  [2025년 저술 시점의 레이크하우스 제품 지형](#2025년-저술-시점의-레이크하우스-제품-지형) 한 절로
  몰아 두었다.
- 소스 자체에 공표된 만료 날짜가 없으므로 이 페이지에는 `stale_after`를 걸지 않는다.

## 저자가 세우는 좌표 — 3계층 아키텍처

- 저자는 데이터 아키텍처를 논할 때 자기 전작 *Data Management at Scale*(O'Reilly)에서 들여온
  **3계층 아키텍처 설계**라는 은유를 쓴다고 적는다 — 첫째 계층은 다양한 데이터 공급자
  (data providers), 둘째 계층은 분배 플랫폼(distribution platform), 셋째 계층은 데이터
  소비자(data consumers)이고, 그 전체를 **메타데이터와 거버넌스 계층(metadata and governance
  layer)**이 덮는다 (1장 도입).[^strengholt2025]
  - 그림 1-1의 안쪽 라벨이 이 배치를 그대로 적는다 — 위 띠가 `Metadata and governance layer`,
    아래 세 상자가 왼쪽부터 `1. Data providers` → `2. Distribution layer` → `3. Data consumers`이고
    화살표는 아래 세 상자 사이에서 왼쪽에서 오른쪽으로, 위 띠와는 양방향으로 오간다
    (1장 도입, 그림 1-1).[^strengholt2025]
  - 계층별 규정 — 첫째 계층은 **데이터가 추출되는 다양한 원천**이고 데이터 유형·형식·위치가
    조직마다 섞여 있다. 둘째 계층은 **선택지가 수백에서 수천에 이르는** 도구·기술의 폭 때문에
    복잡하다. 셋째 계층은 데이터 서비스를 소비하는 쪽이며 업무 지능·기계 학습·AI가 예측·자동화·
    실시간 통찰을 제공하는 자리다 (1장 도입).[^strengholt2025]
- 이 셋 중 가운데가 이 책의 주제다 — 저자는 가운데 계층의 내부 아키텍처에 초점을 맞추면
  **독점적 데이터 웨어하우스 시스템에서 더 적응적이고 오픈 소스이며 분산된 데이터 아키텍처로의
  중대한 이동**이 보인다고 적고, 그 이동을 이끈 오픈 소스 도구·프레임워크 묶음을 원어 그대로
  `modern data stack`이라 부른다 (1장 도입).[^strengholt2025]
- 저자의 진단은 그 묶음이 플랫폼이 아니라는 것이다 — **`modern data stack`은 그 자체로 완결된
  데이터 플랫폼이 아니다.** 각각 데이터 처리·관리의 특정 요소를 다루도록 설계된 독립 서비스와
  도구를 통합해야 하고, 서비스마다 데이터 교환·보안 프로토콜·메타데이터 관리의 자체 표준을
  들고 오며, 기능이 겹치는 서비스가 많아 배치와 사용이 복잡해진다. 그래서 **진입 장벽이 크다**
  (1장 도입).[^strengholt2025]
  - 저자가 여기에 붙이는 인용은 벤더가 아니라 시장을 겨눈다 — **"이 문제는 어느 한 벤더의
    실패가 아니다. 시장의 실패다."**(벤 스탠실) (1장 도입, 인용 블록).[^strengholt2025]
  - 기술 제공자 쪽의 응답이 이 책의 출발점이다 — 인프라·데이터 저장·연산의 통합과 관리가
    복잡하다는 것을 그들도 인식해 개발과 표준화, 특히 Apache Spark와 Delta Lake 같은 오픈 소스
    테이블 형식에서 상당한 진전을 이뤘고, 그것이 포괄적 소프트웨어 플랫폼을 낳았다. Spark와
    Delta Lake를 쓰는 조직에게 메달리온 아키텍처가 유리한 이유를 저자는 그 틀의 강점을 온전히
    쓰기 때문이라고 적는다 (1장 도입).[^strengholt2025]

## 메달리온 아키텍처의 정의

- 저자의 한 문장 정의를 원문 그대로 둔다 (1장 §"What Is a Medallion Architecture?"):[^strengholt2025]

  > A Medallion architecture is a data design pattern used to logically organize data, most
  > often in a lakehouse, using three layers for the data platform, with the goal of
  > incrementally and progressively improving the structure and quality of data as it flows
  > through each layer of the data architecture (from Bronze ⇒ Silver ⇒ Gold layer).

  - 이 정의가 고정하는 것 넷 — 그것은 **데이터 설계 패턴**이고, 자리는 **대개 레이크하우스**이며,
    수는 **셋**이고, 목적은 **각 계층을 지나며 구조와 품질을 점증적·점진적으로(incrementally
    and progressively) 개선**하는 것이다.
- 계층 셋의 규정 (1장 §"What Is a Medallion Architecture?"):[^strengholt2025]
  - **Bronze 계층**은 여러 원천의 원시 데이터를 **원래 구조 그대로** 저장하며 이력 기록이자
    신뢰할 수 있는 최초 저장소 구실을 한다.
  - **Silver 계층**은 품질 검사·표준화·중복 제거와 그 밖의 변환으로 원시 데이터를 정련하고
    표준화해 복잡한 분석에 쓸 수 있게 한다. 처리된 **세밀한 입도(granular)** 데이터가 놓이는
    전이 단계다.
  - **Gold 계층**은 정련된 데이터를 특정 업무 통찰과 의사결정에 맞게 최적화한다. 집계·요약·
    보강으로 고수준 리포팅과 분석에 맞추고, 핵심 지표에 빠르게 닿도록 성능과 확장성을 강조한다.
- 그림 1-2의 안쪽 라벨은 이 셋을 위 3계층 좌표 안에 끼워 넣는다 — 위 띠는 여전히
  `Metadata and governance layer`이고, 아래는 왼쪽부터 `Data sources` → `Medallion architecture`
  (그 안에 `Bronze`·`Silver`·`Gold` 세 상자가 나란히) → `Intelligent and consuming data services`다
  (1장 §"What Is a Medallion Architecture?", 그림 1-2).[^strengholt2025]
  - 곧 **메달리온은 3계층 좌표의 가운데 상자를 여는 이름**이다. 분배 플랫폼 자리에 Bronze·
    Silver·Gold가 들어간다.
- 저자가 정의 직후에 바로 붙이는 것은 경고다 — 메달리온 아키텍처는 계층마다 **업무 친화적
  라벨**을 주지만, 많은 기업이 데이터를 어떻게 계층화하고 모델링할지 파악하지 못해 선택·통합·
  기능 중복 같은 문제를 두고 셀 수 없는 시간을 쓴다. 목표를 어느 구역에 넣을지, "Bronze"와
  "Silver"와 "Gold"가 무슨 뜻인지에서 막히고, 거버넌스와 확장 전략에 대한 물음도 따라온다.
  **포괄적 플랫폼을 고른다고 이 물음들이 자동으로 답해지거나 문제가 풀리지는 않는다**
  (1장 §"What Is a Medallion Architecture?").[^strengholt2025]
- 그래서 1장의 구성이 정해진다 — 메달리온을 설계하기 전에 **데이터 아키텍처의 진화를 먼저
  이해하는 것이 결정적**이라는 것이고, 저자는 전통적 데이터 웨어하우스 → 데이터 레이크(하둡
  포함) → 레이크하우스와 메달리온의 순서로 훑는다
  (1장 §"What Is a Medallion Architecture?").[^strengholt2025]
  - 저자가 독자에게 주는 건너뛰기 지침도 있다 — 데이터 아키텍처의 기초에 이미 익숙하면 1장을
    건너뛰고 3장으로 가도 된다 (1장 §"What Is a Medallion Architecture?").[^strengholt2025]

## 계보 하나 — 웨어하우스가 남긴 것

이 절이 요약하는 웨어하우스 기제 자체의 정본은 이 KB에 이미 있다 —
[엔터프라이즈 데이터 웨어하우스(EDW)](../concepts/enterprise-data-warehouse.md)와
[스테이징 영역](../concepts/staging-area.md)과 [차원 모델링](../concepts/dimensional-modeling.md)과
[완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)이다. 여기 적는 것은 **이
소스가 그 계보에서 메달리온 쪽으로 무엇을 끌고 오는가**다.

- 시작 시점을 저자는 1990년대로 잡는다 — 그때 데이터 웨어하우징이 데이터를 모아 통합된 모음으로
  묶는 흔한 실천으로 떠올랐고, 목표는 **조직을 위한 일관된 진실의 판본(consistent version of the
  truth)**을 만들어 의사결정의 핵심 원천으로 삼는 것이었다
  (1장 §"A Brief History of Data Warehouse Architecture").[^strengholt2025]
  - 그림 1-3의 안쪽 라벨이 그 배치를 적는다 — `Sources`(`OLTP systems` 셋) → `Operational data
    store` → `Staging area`(안에 `File store`) → `Data warehouse`(아래에 `Metadata`가 붙는다) →
    `Data mart` 둘 → `Reporting tools`
    (1장 §"A Brief History of Data Warehouse Architecture", 그림 1-3).[^strengholt2025]
- OLTP 쪽 규정에서 이 책이 끌고 오는 것은 **분리의 이유**다 — 운영 시스템은 정규화되어 있어
  분석용 복합 질의를 감당하기 어렵고, 무결성·성능·가용성 요구 때문에 비싸며, 애초에 특정 업무에
  맞춰 고립·독립으로 설계되어 통합된 시야를 주지 못한다. 분석 부하를 운영 시스템에서 떼어 내면
  이 문제들이 풀리고, 표준 실천은 그 데이터를 가운데 계층으로 옮기는 것이다
  (1장 §"A Brief History of Data Warehouse Architecture" ▸ "OLTP Systems").[^strengholt2025]
- 스테이징 영역의 규정에서 이 책이 강조하는 것은 **재처리 가능성**이다 — 스테이징은 원천과 통합·
  표현 영역 사이에 놓인 저장 영역이자 ETL이라 불리는 절차 묶음이고, 이력 사본을 보관하는 데도
  쓰인다. 웨어하우스가 망가져 다시 지어야 하는 경우에 유용하다는 것이다. 보관 범위는 조직마다
  다르다 — 감사 때문에 정정본까지 수년치를 전부 보관한 사례도, 처리 성공 후 또는 고정 기간 후
  비우는(비영속) 사례도 저자가 직접 봤다고 적는다
  (1장 §"A Brief History of Data Warehouse Architecture" ▸ "The Staging Area").[^strengholt2025]
  - 저자가 곁줄(note)로 못 박는 것 — **데이터 변환의 난제는 2025년 저술 시점의 데이터
    아키텍처를 지을 때도 그대로 남아 있고, 이 변환 딜레마를 피해 갈 길은 없다.** 분석 처리에
    쓸모 있으려면 데이터는 정제되고 통합되어야 한다
    (1장 §"A Brief History of Data Warehouse Architecture" ▸ "The Staging Area", 곁줄).[^strengholt2025]
- Inmon과 Kimball을 저자가 세우는 방식은 **두 번 적재하느냐**의 대비다
  (1장 §"A Brief History of Data Warehouse Architecture" ▸ "Inmon Methodology"·"Kimball
  Methodology"):[^strengholt2025]
  - Inmon은 1990년대 초에 나온 접근으로 3정규형 기반의 중앙집중·고도로 구조화된 전사 데이터
    웨어하우스(EDW)를 세우고 그 위에 표현 계층인 데이터 마트를 둔다. 마트의 데이터는 읽기
    성능에 맞춰 대개 스타 스키마로 조직된다. 그림 1-4의 캡션이 이를 **중앙 웨어하우스를 먼저
    짓고 거기서 데이터 마트를 만드는 하향식(top-down) 설계**라 적는다.
  - 그 대가가 이 절의 claim이다 — **추출·변환·적재가 두 번 일어난다.** 정규화된 통합 계층에
    한 번, 차원 모델로 다시 한 번이다. 개발 공수·주기적 적재 시간·사본 저장 용량이 모두 더
    들고, 새 데이터를 마트에 넣으려면 항상 통합 계층에 먼저 넣어야 해서 사용자가 더 오래
    기다린다.
  - Kimball은 1996년에 데이터 모델링 기법으로 도입됐고 업무 요구에 답하는 차원 데이터 마트를
    먼저 짓는다. 그림 1-5의 캡션이 이를 **상향식(bottom-up) 접근**이라 적는다. 통합 계층 자체가
    차원 테이블의 모음이라 옮겨지는 순간 이미 읽기 성능에 최적화되어 있고, 마트는 그 차원·팩트
    테이블 위의 논리적 뷰로 **가상(virtual)**일 수도 있다.
  - 저자가 판정을 붙이는 자리는 비용이다 — 통합 계층의 데이터 중복은 자주 Inmon의 문제로
    지적되지만 **클라우드 컴퓨팅 시대에 그 논거는 무게가 별로 없다.** 클라우드 저장은 꽤
    저렴해진 반면 연산 비용은 여전히 높고, 그 높은 비용 때문에 많은 전문가가 Kimball 쪽 모델링
    접근을 지지한다는 것이다.
- 이 장에서 메달리온으로 직결되는 곁글이 하나 있다 — "Confusion About the Functions of Data
  Warehouse Layers"는 **웨어하우스 계층의 기능을 둘러싼 혼란이 메달리온을 계층화할 때 생기는
  혼란과 같은 것**이라고 명시한다. 전통적 3계층(스테이징/반입 → 통합/변환 → 표현)을 소프트웨어
  아키텍처의 흔한 실천을 본떠 상이한 책임을 단계에 배정한 것으로 규정하고, 통합 계층에서
  데이터가 형식·타입·이름·구조·관계가 표준화된 **조화된(harmonized)** 상태가 된다고 적는다
  (1장 §"A Brief History of Data Warehouse Architecture" ▸ "Kimball Methodology" 곁글).[^strengholt2025]
  - 그리고 곁글의 결론이 이 책 전체의 태도를 미리 적는다 — 감사 가능성이나 유연성 때문에 계층을
    더 두는 것도 타당할 수 있고, **계층이나 구역의 수는 요구사항에 달렸으며 보편적으로 옳은 답은
    없다. 자기 필요에 맞는 올바른 맞교환을 하는 문제다**
    (같은 곁글).[^strengholt2025]
- 저자가 명시적으로 꼽는 **전통적 웨어하우스의 교훈 셋**
  (1장 §"A Brief History of Data Warehouse Architecture" ▸ "Key Takeaways from Traditional Data
  Warehouses"):[^strengholt2025]
  - **데이터를 계층화한다는 발상 자체가 새것이 아니다.** 관심사를 분리하는 효과적 전략으로 이미
    입증되어 있다. — 메달리온의 3계층이 무에서 나오지 않았다는 이 책의 논거다.
  - **데이터 모델링이 결정적이다.** 유연성·중복 감소·성능·업무 인터페이스 노릇에서 큰 몫을
    한다.
  - **전통적 웨어하우징은 소프트웨어와 하드웨어의 긴밀한 결합을 드러낸다.** 온프레미스에서
    연산과 저장을 붙여 둔 덕에 빠르지만 수직 확장에만 열려 있다.
  - 한계도 같은 자리에서 나온다 — RDBMS 기반 아키텍처는 빠르게 느는 데이터 볼륨을 감당하기
    어렵고, 수직 확장에는 한계와 비용이 있으며, 비정형 데이터 처리나 기계 학습 같은 워크로드
    지원에서 유연성이 모자란다.

## 계보 둘 — 데이터 레이크가 남긴 것

레이크가 무엇이고 왜 실패했는가의 정본은 [데이터 레이크](../concepts/data-lake.md)에 있다. 여기
적는 것은 이 소스가 **하둡 시대에서 메달리온 쪽으로 끌고 오는 부품**이다.

- 등장 시점을 저자는 2000년대 중반으로 잡는다 — 오픈 소스 소프트웨어의 부상과 나란히 자리를
  잡았고, 비정형·반정형·정형의 여러 상태에 있는 방대한 데이터를 다룰 수 있는 새 분산
  아키텍처를 들여왔다 (1장 §"A Brief History of Data Lakes").[^strengholt2025]
  - 그림 1-6의 안쪽 라벨은 1세대의 모양을 적는다 — `Sources`(`OLTP systems`) →
    `Operational data store` → `Hadoop cluster`(안에 `HDFS/HIVE tables`와 `MapReduce/Spark`) →
    `Data science workloads`와 `Data warehouse`
    (1장 §"A Brief History of Data Lakes", 그림 1-6).[^strengholt2025] 곧 **레이크의 출력이
    웨어하우스로 다시 들어가는 두 층 구조**가 그림 안에 이미 그려져 있다.
- 저자가 하둡을 다루는 이유를 명시한다 — **하둡을 이해하는 것이 2025년 저술 시점의 데이터
  아키텍처를 이해하는 데 결정적인 까닭은 하둡의 구성 요소나 최소한 그 개념이 여럿 그대로 남아
  있기 때문**이다 (1장 §"A Brief History of Data Lakes").[^strengholt2025]
- HDFS에서 끌고 오는 것은 **블록 불변성**이다 — 블록은 불변이라 삽입과 추가만 되고 직접 갱신이
  안 된다. 하둡 계열은 모든 변경을 불변 선행 기록 로그에 적고 비동기 프로세스가 데이터 파일을
  갱신한다. 그래서 SCD처럼 이력을 보존하려면 차원 테이블의 새 판본을 물리적으로 다시 만드는
  우회로가 필요하고, 그 과정은 자원을 많이 먹고 관리가 복잡하다
  (1장 §"A Brief History of Data Lakes" ▸ "Hadoop's Distributed File System").[^strengholt2025]
  - 그 기제의 정본은 [오브젝트 스토어](../concepts/object-stores.md)와
    [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)에 있다.
- MapReduce에서 끌고 오는 것은 **셋 중 어디서 느려지는가**다 — map·shuffle·reduce 세 단계이고,
  데이터가 노드에 고르게 분산되지 않으면 어느 단계에서든 일부 노드가 먼저 끝나 전체 성능이
  떨어진다. 저자의 판정은 **2025년 저술 시점의 플랫폼에서 MapReduce가 직접 쓰이지는 않더라도 그
  개념과 빅데이터 연산 접근은 여전히 많은 데이터 아키텍처의 바탕**이라는 것이다
  (1장 §"A Brief History of Data Lakes" ▸ "MapReduce").[^strengholt2025] 모델 자체의 정본은
  [MapReduce](../concepts/mapreduce.md)다.
- Hive에서 끌고 오는 것은 둘이다 — **외부 테이블과 내부(관리형) 테이블의 구분**, 그리고 **Hive
  Metastore**다. 저자는 두 개념 모두 **2025년 저술 시점의 메달리온 아키텍처에 여전히 존재한다**고
  적는다 (1장 §"A Brief History of Data Lakes" ▸ "Apache Hive" ▸ "External and internal tables"·
  "Hive Metastore").[^strengholt2025]
  - 외부 테이블은 Hive 밖(보통 HDFS의 CSV나 Parquet)에 있는 데이터를 가리키고 Hive가 소유하지
    않는다. 드롭하면 메타데이터만 지워지고 데이터는 남는다. 관리형 테이블은 Hive가 온전히
    통제하고 드롭하면 데이터까지 지워진다. 관리형 쪽은 ORC·Parquet 같은 열 지향 형식을 자주
    쓰는데, 저자는 그 형식들이 **2025년 저술 시점의 메달리온 아키텍처에 널리 퍼져 있다**고 적는다.
  - Hive Metastore는 테이블·컬럼·파티션의 메타데이터(스키마·HDFS상의 위치 등)를 담는 중앙
    저장소이고, 그 덕에 스키마를 먼저 정의하지 않고 반입한 뒤 읽을 때 적용하는 **읽기
    스키마(schema on read)**가 가능해진다.
- 읽기 스키마에 저자가 다는 경고가 이 장에서 가장 강한 문장 중 하나다 — **일부 엔지니어가 읽기
  스키마가 데이터 모델링의 필요를 없앤다고 잘못 믿는데, 이것은 중대한 오해다.** 제대로 된
  모델링 없이는 데이터가 불완전하거나 품질이 낮아지고 여러 원천의 통합이 어려워지며 성능도
  나빠진다 (1장 §"A Brief History of Data Lakes" ▸ "Apache Hive" ▸ "Hive Metastore",
  경고 곁줄).[^strengholt2025] 읽기 스키마 자체의 정본은
  [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md)다.
- 작은 파일 문제를 저자는 산수로 제시한다 — 128MB 블록에서 1TB를 다루면 파일은 약 8,000개이고
  메타데이터는 1.6MB다. 같은 1TB를 1KB 파일들로 저장하면 메타데이터가 200GB 필요해 **부하가
  1,280배**가 된다 (1장 §"A Brief History of Data Lakes" ▸ "Apache Hive" ▸
  "Hive Metastore").[^strengholt2025] 이 문제의 정본은
  [작은 파일 문제와 컴팩션](../concepts/small-files-and-compaction.md)이다.
- Spark의 등장을 저자는 연도와 함께 적는다 — UC 버클리 AMPLab 연구자들이 2009년에 하둡
  시스템의 처리 속도를 높일 방법을 찾는 연구 프로젝트를 시작해 인메모리 연산 프레임워크
  Spark를 만들었고, 같은 팀이 SQL 질의를 다루는 확장 Shark도 만들었다. Shark는 Hive가 생성한
  물리 계획을 인메모리 프로그램으로 변환해 **Hive에서 MapReduce로 도는 것보다 최대 100배** 빠르게
  SQL을 돌렸다. Spark가 "표준 라이브러리" 접근을 채택하면서 Shark는 Hive Metastore와의 호환을
  유지하는 Spark SQL로 대체되어 갔다
  (1장 §"A Brief History of Data Lakes" ▸ "Spark Project").[^strengholt2025]
  - 저자가 붙이는 단서 — 속도 이득에는 전제가 있다. Spark는 디스크에서 읽어 메모리로 올려야
    하고 그 과정은 즉시가 아니다. 클러스터를 재시작하면 인메모리 데이터가 사라져 다시 올려야
    한다. **아키텍처를 지을 때 이것은 자원이 준비되기까지 시동 시간이 있다는 뜻**이고, 데이터는
    질의나 캐싱이 시작되어야 빠르게 쓸 수 있게 된다 (같은 절).[^strengholt2025]
- 레이크 절의 결론은 **두 층 아키텍처(two-tier architecture)**다 — 작은 파일 수와 트랜잭션 지원
  부재 같은 난제 때문에 조직들은 흔히 데이터를 전통적 웨어하우스로 되먹이는 패턴에 기댔다.
  레이크가 기계 학습 도구와 호환되는 형식으로 데이터를 두고 그 부분집합을 웨어하우스로 올리는
  구조다. 업계는 이 두 층을 하나의 해법으로 통합하는 쪽으로 옮겨 갔고, 그것이 레이크하우스의
  전사(前史)다 (1장 §"A Brief History of Data Lakes" ▸ "Moving Forward with Data
  Lakes").[^strengholt2025]

## 계보 셋 — 레이크하우스

- Spark의 거버넌스 이동과 Databricks의 창업이 같은 해다 — 2013년에 30개 조직 100명이 넘는
  기여자를 모은 Spark 프로젝트가 장기 지속 가능성과 벤더 독립성을 위해 Apache 소프트웨어 재단에
  기여되어 Apache 최상위 프로젝트가 되었고, 같은 2013년에 Spark의 창시자들이 Databricks를
  세웠다 (1장 §"A Brief History of Lakehouse Architecture" ▸ "Founders of
  Spark").[^strengholt2025]
  - 저자가 적는 Spark 판본 연표 — 1.0이 2014년, 2.0이 2016년, 3.0이 2020년, 4.0이 2025년이다
    (같은 절).[^strengholt2025]
  - 전략의 갈림도 claim이다 — Cloudera·Hortonworks 같은 하둡 경쟁자가 온프레미스에 집중한 것과
    달리 Databricks는 클라우드 전용 배포를 골랐고, AWS로 시작해 Azure와 GCP로 넓혔으며 2017년
    11월에 Azure Databricks로 Microsoft Azure의 1차 서비스(first-party service)가 되었다
    (같은 절).[^strengholt2025]
  - 하둡의 운명에 대한 저자의 답은 "폐기가 아니라 대체"다 — HDFS가 클라우드 오브젝트 저장
    서비스로 갈렸을 뿐이다. 예로 Azure Data Lake Storage는 HDFS 인터페이스 호환을 유지하면서
    바탕 저장 아키텍처를 갈아 끼운 것이라고 적는다. 요약하면 **HDFS 인터페이스는 그대로 있고
    그 아래 저장 아키텍처가 대대적으로 바뀌었다** (같은 절).[^strengholt2025]
  - Spark 쪽도 같은 변화를 겪었다 — 단일 거대 하둡 클러스터에 묶이지 않고 가상 머신 클러스터나
    쿠버네티스 컨테이너에서 독립적으로 돌 수 있게 되어, 연산 구성과 크기가 다른 여러 Spark
    클러스터가 **같은 오브젝트 저장 계층**에 붙는다 (같은 절).[^strengholt2025] 이 분리의 정본은
    [컴퓨트와 저장의 분리](../concepts/compute-storage-separation.md)다.
- 오픈 테이블 형식 셋의 연표와 기원이 이 절의 핵심 claim이다
  (1장 §"A Brief History of Lakehouse Architecture" ▸ "Emergence of Open Table
  Formats"):[^strengholt2025]
  - **Apache Hudi** — Uber가 시작해 2017년에 가장 먼저 나왔다. 하둡 호환 파일시스템 위 대형
    데이터셋 관리를 단순화하려는 것이었고 효율적 upsert·삭제·증분 처리에 초점을 뒀다.
    Parquet·ORC를 지원한다.
  - **Apache Iceberg** — Netflix가 2018년에 공개했다. 대규모 분석 데이터 시스템의 성능과 복잡성
    문제를 겨냥했고 Parquet·ORC·Avro를 지원한다.
  - **Delta Lake** — Databricks가 2019년에 내놨다. ACID 트랜잭션, 확장 가능한 메타데이터 처리,
    스트리밍과 배치의 통합 처리를 가져왔고 스키마 강제·진화로 무결성을 지킨다. **저장에는
    Parquet 파일 형식만 쓰고 기본 압축 알고리즘은 Snappy**다.
  - 셋이 나온 동기를 저자가 한 문장으로 묶는다 — 열 지향 저장 형식 안에서 **트랜잭션 보장·
    메타데이터 처리·데이터 무결성**을 개선할 필요가 결정적이었다는 것이다.
- Delta Lake가 ACID를 주는 기제는 트랜잭션 로그(DeltaLog)다 — 테이블을 바꾸는 연산은 이산적
  단계들로 쪼개져 **커밋(commit)**이라는 순서 있는 원자적 단위로 로그에 기록되고, 로그는 해당
  테이블의 Parquet 파일들 사이 `_delta_log/` 하위 디렉터리에 자동 저장된다. 커밋마다 JSON 파일
  하나이고 `000000.json`부터 순차로 붙는다. 이전 판본이 모두 보존되므로 **시간 여행(time
  travel)**이 가능하다 (같은 절).[^strengholt2025] ACID 자체의 정본은
  [트랜잭션과 ACID](../concepts/acid-transactions.md)다.
  - 그림 1-7의 안쪽 라벨이 디렉터리 배치를 적는다 — 루트 `my_table/` 아래 `_delta_log/`가
    `Transaction log`로, 그 안의 `000000.json`·`000001.json`·`000002.json`이 `Single commits`로,
    `0000010.checkpoint.parquet`이 `Checkpoint files`로 라벨링된다. 같은 루트 아래 `data=2019-01-01/`
    같은 디렉터리가 `(Optional) partition directories`이고 그 안의 `file-1.parquet`이 `Data files`다
    (같은 절, 그림 1-7).[^strengholt2025]
  - 저자가 각주로 다는 단서 — 판본이 모두 기록되지만 upsert나 삭제 뒤 옛 판본은 vacuum 프로세스가
    돌기 전까지 남아 있고, Delta Lake가 즉시 데이터를 지우는 것이 아니라 **그 테이블의 현행 스냅샷
    (the current snapshot of the table)이 더 이상 참조하지 않는 데이터를 치우는 것**이다. vacuum과 삭제의 주기는 설정 가능하다
    (1장 §"A Brief History of Lakehouse Architecture" ▸ "Emergence of Open Table Formats",
    각주 14).[^strengholt2025]
- 세 형식의 상호운용을 저자가 곁글로 따로 다룬다 — Databricks가 2024년에 Apache Iceberg를
  지원하는 회사 Tabular를 인수했고 목적은 레이크하우스 플랫폼 사이의 호환이다. 단기 수단으로
  Delta Lake가 **UniForm**을 도입해 주로 Delta Lake로 쓰고 Iceberg나 Hudi용 메타데이터를
  비동기로 생성하게 했고, 장기적으로는 상호운용의 단일 개방 표준을 지향한다. 별도로 Hudi
  창시자들에게서 나온 **Apache XTable**이 세 형식 사이의 진정한 단방향 변환을 제공한다
  (1장 §"A Brief History of Lakehouse Architecture" ▸ "Emergence of Open Table Formats"
  곁글).[^strengholt2025]
- 레이크하우스의 규정 — Delta Lake의 등장과 함께 자리를 잡은 이 모델은 레이크와 웨어하우스의
  이점을 결합하고, 주로 오픈 소스를 바탕으로 **통일된 데이터 플랫폼** 위에서 돌게 한다. 저자가
  단서를 단다 — **레이크하우스 개념 자체는 어느 특정 기술에 본질적으로 묶여 있지 않지만, 가장
  널리 쓰이는 구현은 Apache Spark와 Delta Lake를 중심으로 지어진다.** Spark가 연산을, Delta
  Lake가 오픈 소스 저장 계층을 맡는다
  (1장 §"A Brief History of Lakehouse Architecture" ▸ "The Rise of Lakehouse
  Architectures").[^strengholt2025]
  - 앞선 아키텍처와 갈리는 지점은 둘이다 — **저비용 클라우드 오브젝트 저장을 지원하면서 동시에
    ACID 트랜잭션을 제공**하고, Apache Spark에서 온 혁신 덕에 전통적 레이크보다 성능이 크게
    낫다 (같은 절).[^strengholt2025]
  - 그림 1-8의 안쪽 라벨이 메달리온과 레이크하우스가 겹치는 자리를 보여 준다 —
    `Lakehouse architecture` 상자 안에 `Compute`(안에 `Spark`)와 `Cloud object storage`가 있고,
    그 오브젝트 저장 안에 `Bronze`·`Silver`·`Gold` 세 구역이 파일 무더기로 채워져 왼쪽에서
    오른쪽으로 화살표가 이어진다. 입력은 `Sources`(`OLTP systems`)와 `Operational data store`,
    출력은 `Data science workloads`·`Reporting workloads`·`Sharing with others` 셋이다
    (같은 절, 그림 1-8).[^strengholt2025] 곧 이 책에서 **메달리온은 레이크하우스의 오브젝트
    저장 계층 안의 구역 나누기**다.

## 2025년 저술 시점의 레이크하우스 제품 지형

**이 절만 제품 이름을 센다. 2025년 저술 시점의 상태이고 그 뒤의 변화는 이 소스가 답하지 않는다.**

- 저자는 Databricks가 **레이크하우스라는 용어를 만들고(coining) 그 제품 공간에 자기를 자리매김한
  선구자**였고 이어서 다른 주요 업체들이 빠르게 따라왔다고 적은 뒤, "2025년 기준 지형(the
  current landscape as of 2025)"이라는 이름으로 일곱을 나열한다
  (1장 §"A Brief History of Lakehouse Architecture" ▸ "The Rise of Lakehouse
  Architectures"):[^strengholt2025]
  - **Databricks** — Delta Lake를 통합해 ACID 트랜잭션과 확장 가능한 메타데이터 관리를 지원하고
    Apache Spark와 맞물린다.
  - **Azure HDInsight** — 관리형 Apache Hadoop·Apache Spark 서비스.
  - **Azure Synapse Analytics** — 빅데이터 해법과 데이터 웨어하우징을 하나의 분석 서비스로
    합치고 SQL 서버리스 온디맨드나 프로비저닝 자원으로 질의한다.
  - **Microsoft Fabric** — SaaS 경험으로 제공되는 분석·데이터 플랫폼. Apache Spark와 Delta
    Lake를 쓴다. (이 책 II부의 실습 대상이다.)
  - **Cloudera** — 여러 테이블 형식과 처리 프레임워크를 지원하며 Hadoop·Spark 통합이 강하다.
  - **Dremio** — Apache Arrow를 지렛대로 인메모리 연산을 여러 언어에 걸쳐 확장한다.
  - **Starburst** — 오픈 소스 분산 SQL 질의 엔진 Trino에 특화되어 있다.
- 나열 밖의 관찰 — AWS·GCP·Snowflake 같은 다른 주요 업체도 자사 제품에 "레이크하우스"라는 용어를
  넣기 시작했고, 저자는 이것을 레이크하우스 아키텍처의 인지와 채택이 늘고 있다는 신호로 읽는다
  (같은 절).[^strengholt2025]
- 그리고 이 책의 전제가 되는 승인 사실 — **Databricks와 Microsoft가 Spark와 Delta Lake 기반
  아키텍처에서 데이터를 계층화하는 모범 사례로 메달리온 아키텍처를 지지해 왔다**
  (같은 절).[^strengholt2025]

## 저자의 판정 — 메달리온은 진화의 산물이 아니다

- 이 장 전체가 "진화"를 훑은 끝에 내리는 판정은 메달리온을 그 진화의 산물에서 **빼는** 것이다
  (1장 §"A Brief History of Lakehouse Architecture" ▸ "Medallion Architecture and Its Practical
  Challenges"):[^strengholt2025]

  > The Medallion architecture, originally coined by Databricks, is not an evolution of any
  > existing architectures. Instead, it is a data design pattern that offers a logical and
  > structured approach to organizing data in a lakehouse.

  - 곧 이름의 계보와 설계의 계보가 다르다 — 이름은 Databricks가 만들었고, 층을 나눈다는 발상은
    웨어하우스와 레이크의 계층화에서 왔으며, 그 둘을 합친 결과가 진화의 다음 단계가 아니라
    **패턴**이라는 것이 저자의 분류다.
  - Bronze에서 Gold로 가는 진행이 뜻하는 것도 셋이다 — **데이터 품질만이 아니라 구조와 검증의
    개선**이다.
- 저자가 짚는 공백이 이 책의 존재 이유다 — 라벨이 직관적임에도(Bronze는 원시, Silver는 정제,
  Gold는 소비 준비) **실무 지침이 없다.** 각 계층의 구체적 역할에 합의가 없고 용어 자체에
  서술적 정밀성이 모자란다. 명명 규약은 출발점을 주지만 **진짜 난제는 실무 적용과, 이론적
  지침과 실제 실행 사이의 편차**에 있고 그것이 이 책이 파고드는 주제다 (같은 절).[^strengholt2025]
- 맺음에서 저자가 데이터 모델링을 다시 불러온다 — 업무 사용자가 새 프로젝트와 통찰이 빨리
  전달되기를 기대하는 속도가 또 하나의 진화이고, 그 압박 아래 **많은 조직이 데이터 모델링의
  불가결한 필요를 인식하지 못한다.** 저자는 여기서 데이터 메시를 지목한다 — **데이터 메시
  접근은 이 필요를 자주 간과하고**, 그 결과 분산된 팀들이 조금씩 다른 호환되지 않는 모델을
  거듭 만들어 분석 모델·ETL 파이프라인·데이터 프로덕트·애플리케이션 코드에 굳어지면서, 한때
  명료하고 명시적이던 설계가 흐려지고 사일로화된다는 것이다 (1장 §"Conclusion").[^strengholt2025]
  - 데이터 메시의 정본은 이 KB에 따로 있다 — [데이터 메시](../concepts/data-mesh.md). 위 문장은
    스트렝홀트가 메달리온 쪽에서 내리는 판정이고, 메시 쪽 소스가 자기 원칙에서 데이터 모델링을
    어떻게 다루는지와 나란히 읽어야 한다.
- 메달리온 자신에 대한 최종 판정도 유보적이다 — **메달리온 아키텍처는 이 문제들을 인식하지만
  결정적 해법을 주는 데까지는 미치지 못한다.** 이 설계 패턴의 실무 적용은 이론적 모형과 실제
  구현·사례 사이의 간극을 드러내고, 그래서 조직의 구체적 필요에 맞춘 정밀한 데이터 모델링과
  거버넌스 전략이 계속 필요하다는 것이다 (1장 §"Conclusion").[^strengholt2025]
- 클라우드가 바꾼 통제 범위도 맺음의 claim이다 — 온프레미스 웨어하우스 시절에는 하드웨어 구성·
  네트워크·저장을 바꿀 수 있었지만, 완전 분산·관리형 서비스로 옮겨 가면서 규모 조절은 쉬워진
  대신 **바탕 인프라를 통제하기는 어려워졌다.** 그 맥락에서 올바른 구성과 계층화와 데이터 설계가
  결정적이 된다 (1장 §"Conclusion").[^strengholt2025]

## 이 KB의 다른 계보 서술과 맞대어 본 것

이 절은 각주 없는 KB 편저자의 대조다 — 2026년 KB 작성 시점에 이 KB에 이미 있는 계보 서술과
이 소스를 맞대어 본 결과이고, 소스가 한 말이 아니다.

- **끊는 마디가 다르다.** [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md)은
  같은 역사를 1세대 웨어하우스·2세대 레이크·3세대 멀티모달 클라우드의 셋으로 끊고 레이크하우스를
  3세대 안의 비틀림 하나로 넣는다. 스트렝홀트는 웨어하우스·레이크·레이크하우스의 셋으로 끊고
  레이크하우스를 독립된 마디로 세운 뒤 메달리온을 그 위의 패턴으로 올린다. **같은 대상을 다른
  단위로 센 것이고 사실의 충돌이 아니다** — 한쪽은 "아키텍처 가정이 바뀌었는가"를 세고 다른
  쪽은 "저장·연산의 구조가 바뀌었는가"를 센다.
- **판정의 방향이 반대다.** 메시 쪽 소스는 레이크하우스를 포함한 3세대가 이전 세대의 한계를
  그대로 앓는다고 판정하고 탈중앙화를 처방한다. 스트렝홀트는 거꾸로 데이터 메시가 데이터
  모델링의 필요를 간과한다고 판정한다. **이것은 방법론의 맞교환이지 최대 하나만 참인 사실
  주장이 아니므로 `contradicts`를 걸지 않는다.** 두 판정을 나란히 읽는 자리는
  [데이터 메시](../concepts/data-mesh.md)와 위 세대론 페이지다.
- **레이크 등장 시점의 표기가 다르다.** 메시 쪽 소스는 데이터 레이크 아키텍처가 2010년에
  도입되었다고 적고, 스트렝홀트는 2000년대 중반에 자리를 잡기 시작했다고 적는다. 두 문장이
  세는 것이 다르다 — 앞은 아키텍처 개념의 도입 시점, 뒤는 기술의 확산 시점이다. #hypothesis
  둘을 같은 축에 놓으면 어긋나 보이지만 각자의 문장 안에서는 어긋나지 않는다.
- **레이크 실패 진단은 겹치되 결론이 다르다.** [데이터 레이크](../concepts/data-lake.md)가
  모은 "데이터 레이크 1.0의 실패"와 스트렝홀트의 진단(작은 파일, 트랜잭션 부재, 지연과 질의
  성능, 모델링 없는 반입)은 같은 목록에 가깝다. 갈리는 것은 처방이다 — 이 소스는 레이크하우스와
  메달리온으로 처방하고, 그 처방의 성패는 이 책 뒤 장들과 사례 연구가 답할 자리다.

## 이어지는 페이지

- [데이터 레이크](../concepts/data-lake.md) — 레이크와 레이크하우스의 정의·실패·수렴을 여러
  소스로 모은 자리
- [분석 데이터 아키텍처 세대론](../concepts/analytical-data-architecture-generations.md) — 같은
  역사를 셋으로 끊고 탈중앙화로 결론 내는 쪽
- [엔터프라이즈 데이터 웨어하우스(EDW)](../concepts/enterprise-data-warehouse.md) — Inmon 3계층과
  Kimball 2계층의 지형
- [차원 모델링](../concepts/dimensional-modeling.md) · [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)
  — 이 장이 Kimball에서 끌어오는 두 부품
- [스테이징 영역](../concepts/staging-area.md) — Bronze 계층이 물려받는 자리
- [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md) — 이 장이 가장
  강하게 경고하는 오해의 원어
- [작은 파일 문제와 컴팩션](../concepts/small-files-and-compaction.md) — 1,280배 산수의 일반형
- [MapReduce](../concepts/mapreduce.md) · [컴퓨트와 저장의 분리](../concepts/compute-storage-separation.md)
  · [오브젝트 스토어](../concepts/object-stores.md) — 하둡에서 레이크하우스로 넘어오는 부품들
- [트랜잭션과 ACID](../concepts/acid-transactions.md) — DeltaLog가 제공하겠다는 네 글자
- [데이터 메시](../concepts/data-mesh.md) — 이 장 맺음이 지목하는 대상
- [메타데이터 관리](../concepts/metadata-management.md) — 저자의 3계층 좌표에서 전체를 덮는 띠
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 이 페이지가 걸리는
  허브

[^strengholt2025]: Piethein Strengholt, *Building Medallion Architectures: Designing with Delta
    Lake and Spark*, O'Reilly 2025 ([소스](../sources/strengholt2025.md)). 스냅샷이 EPUB이고
    **인쇄판 쪽 앵커가 없어** locator는 장·절 단위다 — `N장 §"절 제목"`(원문 절 제목 그대로),
    소절은 `▸`로 잇고, 절 제목 앞의 장 도입부는 `N장 도입`, 본문 밖은 `Foreword`·
    `Preface §"…"`·`I부 도비라`다. 1장에는 표도 코드 목록도 없고, 도판 여덟과 곁글 셋과
    곁줄 넷(tip 하나·note 둘·warning 하나)이 있다. **그림 안쪽 글자는 이미지에만 있고 본문에는
    나오지 않는다** — 캡션은 HTML의 `figcaption`에서, 안쪽 라벨은 `OEBPS/assets/`의 PNG를 직접
    열어 읽었고 라벨의 영문 표기는 그대로 옮겼다. 그런 대목은 locator 끝에 그림 번호를 함께
    적었다.

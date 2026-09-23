---
type: synthesis
title: 데이터 엔지니어링 수명 주기
description: 원시 데이터를 소비 가능한 산물로 바꾸는 다섯 단계(생성·저장·반입·변환·서빙)와 그 전부를 가로지르는 여섯 저류(보안·데이터 관리·DataOps·데이터 아키텍처·오케스트레이션·소프트웨어 엔지니어링) 진입점, 그리고 그 저장·변환·서빙 구간을 레이크하우스 위에서 Bronze·Silver·Gold 셋으로 나누는 메달리온 아키텍처의 원전
generated: { by: "claude-opus-5", at: "2026-08-15T12:00:00Z" }
---

# 데이터 엔지니어링 수명 주기

**기술 목록이 아니라 데이터의 이동 경로가 축인 쪽이다.** Reis & Housley가 이 프레임을 세운
의도는 명시적이다 — 대화를 기술에서 데이터 자체와 그것이 섬겨야 할 최종 목표로 옮기는 것.
그 진술의 원문과 출처는 [데이터 엔지니어링의 정의](../concepts/data-engineering-defined.md)에 있다.

층위를 먼저 가려 둔다. 이 수명 주기는 **데이터가 조직 안에서 지나는 경로**의 이름이고,
[Kimball 라이프사이클](../concepts/kimball-lifecycle.md)은 **DW/BI 프로젝트를 수행하는 절차**의
이름이며, [데이터플로 아키텍처](dataflow-architecture.md)는 **시스템 사이의 데이터 이동
기제**의 이름이다. 셋은 같은 낱말을 쓰지만 대상이 다르다.

전체 데이터 수명 주기와의 관계도 저자들이 좁혀 둔다 — 데이터 엔지니어링 수명 주기는 전체
데이터 수명 주기의 부분집합(subset)이고, 데이터 엔지니어가 통제하는 단계에 초점을 둔다.

## 이 프레임이 답하는 것

- [데이터 엔지니어링의 정의](../concepts/data-engineering-defined.md) — 이 수명 주기가 왜
  정의의 뼈대인가, 그리고 데이터 엔지니어링이 무엇이 아닌가
- [데이터 엔지니어의 진화](../concepts/data-engineer-evolution.md) — 웨어하우징에서 빅데이터를
  거쳐 "수명 주기 엔지니어"에 이른 40년

## 다섯 단계

순서대로 읽는다. 다만 저자들이 미리 경고한다 — 가운데 세 단계(저장·반입·변환)는 다소 뒤엉킬
수 있고 그래도 괜찮으며, 단계는 반복되거나 순서를 벗어나거나 겹칠 수 있다.

- [원천 시스템과 데이터 생성](../concepts/source-systems-and-generation.md) — 데이터가 태어나는
  자리, 소유하지 않는 시스템을 평가하는 질문들, 스키마리스와 고정 스키마
- [수명 주기의 저장 단계](../concepts/storage-in-the-lifecycle.md) — 저장이 단계가 아니라 토대인
  이유, 데이터의 온도(뜨거움·미지근함·차가움)
- [수명 주기의 반입 단계](../concepts/ingestion-in-the-lifecycle.md) — 최대 병목, 배치 대
  스트리밍, 푸시 대 풀
- [수명 주기의 변환 단계](../concepts/transformation-in-the-lifecycle.md) — 데이터가 가치를 만들기
  시작하는 자리, 업무 로직과 피처화
- [수명 주기의 서빙 단계](../concepts/serving-in-the-lifecycle.md) — 분석·ML·역방향 ETL, 그리고
  허영 프로젝트라는 실패 양식

### 생성 단계를 파고들면

- [원천으로서의 로그](../concepts/logs-as-a-data-source.md) — 로그의 세 인코딩, 해상도와 로그
  레벨, 데이터베이스 로그가 CDC의 재료가 되는 경로
- [CRUD와 삽입 전용 패턴](../concepts/crud-and-insert-only-patterns.md) — 애플리케이션이 상태를
  적는 두 방식과 그것이 이력 확보에 거는 조건
- [데이터 공유와 서드파티 소스](../concepts/data-sharing-and-third-party-sources.md) — 멀티테넌시
  위에 서는 공유와 데이터 마켓플레이스
- [시계열 데이터베이스](../concepts/time-series-databases.md) — 원천 데이터베이스 여섯 갈래 중
  시간이 1차 축인 것

### 저장 단계를 파고들면

- [데이터 저장의 원료](../concepts/storage-raw-ingredients.md) — HDD·SSD·RAM의 수치, 직렬화와
  압축, 지연·대역폭·가격을 한 줄에 세운 캐시 계층
- [파일 저장과 블록 저장](../concepts/file-and-block-storage.md) — 파일을 규정하는 세 특성,
  NAS·SAN·클라우드 가상화 블록 저장·로컬 인스턴스 볼륨
- [오브젝트 스토어](../concepts/object-stores.md) — 클라우드 분석 저장의 기본값이 된 이유와
  일관성·버저닝·저장 클래스
- [컴퓨트와 저장의 분리](../concepts/compute-storage-separation.md) — 코로케이션에서 분리로,
  그리고 실무가 다시 섞는 두 방식

### 서빙 단계를 파고들면

- [데이터를 서빙하는 방식](../concepts/data-serving-methods.md) — 파일 교환·데이터베이스·스트리밍·
  질의 페더레이션·데이터 공유·노트북이라는 여섯 경로
- [데이터 프로덕트](../concepts/data-products.md) — 서빙의 산출물을 제품으로 볼 때 따라오는 질문들과
  셀프서비스가 실패하는 이유
- [시맨틱 계층과 메트릭 계층](../concepts/semantic-and-metrics-layers.md) — 업무 정의와 로직을 한
  자리에 모아 "이 숫자가 맞는가"에 답하는 계층
- [서비스 수준 목표](../concepts/service-level-objectives.md) — 서빙되는 데이터에 거는 약속의 어휘

## 메달리온 아키텍처 — 2025년 전권 원전

**수명 주기의 저장·변환·서빙 구간을 레이크하우스 위에서 계층으로 나누는 쪽이다.** 위 다섯 단계가
데이터가 지나는 **경로**의 이름이라면 여기 모이는 페이지들은 그 경로의 가운데 토막을 **어디에
무엇을 놓을 것인가**로 다시 끊는다. 이 KB가 여러 소스에서 이름만 빌려 쓰던 Bronze·Silver·Gold가
전권 원전을 갖는 자리다.

한 원전이 아홉 런으로 전권 들어와 **스물두 페이지**가 되었다. 한 절이 감당할 크기를 넘겼으므로 그
목록은 **자식 허브 [메달리온 아키텍처 구축](building-medallion-architectures.md)**이 원전의 부
단위로 나눠 갖는다. 여기에는 그 진입점과, 이 축의 다른 절들과 가장 자주 엮이는 셋만 둔다.

- [메달리온 아키텍처 구축](building-medallion-architectures.md) — **자식 허브.** 이 원전의 스물두
  페이지를 I부에서 IV부까지 부 단위로 나눠 갖고, 이 책이 다른 원전의 페이지에 닿아 고친 열아홉
  자리도 거기서 한 줄씩 가리킨다
- [메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md) — 1장. 계층 셋의
  규정과 웨어하우스·레이크·레이크하우스 세 계보, 그리고 **메달리온이 진화의 산물이 아니라 설계
  패턴**이라는 판정. 위 [저장 단계](#저장-단계를-파고들면)의 계보 논의와 곧바로 이어진다
- [메달리온 Gold 계층](../concepts/medallion-gold-layer.md) — 3장. 계층 셋 가운데 **소비와 맞닿는
  쪽**이라 위 [서빙 단계](#서빙-단계를-파고들면)의 데이터 프로덕트·시맨틱 계층과 같은 자리를 다른
  축으로 자른다. Bronze와 Silver는 자식 허브의 I부 절이 갖는다
- [메달리온 메시와 데이터 관리의 탈중앙](../concepts/medallion-mesh-and-decentralization.md) —
  11장. 이 규정을 **여럿으로 곱하는** 자리이고, 데가니의 네 원칙과 맞댄 대조표가 있어
  [데이터 메시 원칙](data-mesh-principles.md) 축으로 가는 다리다

## 이 수명 주기의 다음

- [라이브 데이터 스택](../concepts/live-data-stack.md) — 2022년 시점 저자들이 모던 데이터 스택
  다음으로 지목한 것(전망이지 관측이 아니다)
- [데이터 엔지니어의 진화](../concepts/data-engineer-evolution.md) — 같은 전망의 직업·역할 쪽

## 여섯 저류

저류(undercurrents)는 단계가 아니라 모든 단계를 가로지르는 기반이다 — 이것 없이는 수명 주기의
어느 부분도 제대로 기능하지 못한다.

- [데이터 엔지니어링의 저류](../concepts/data-engineering-undercurrents.md) — 여섯의 목록과 각각이
  수명 주기에 걸리는 방식
- [데이터 관리](../concepts/data-management-discipline.md) — DMBOK 정의와 그 아래 여덟 갈래
- [DataOps](../concepts/dataops.md) — 애자일·데브옵스·통계적 공정 관리를 데이터에 옮긴 것

## 아키텍처와 기술 선택

수명 주기를 실제 시스템으로 만들 때 먼저 그리는 것과 나중에 고르는 것이다.

- [데이터 아키텍처의 정의](../concepts/data-architecture-defined.md) — 무엇을 데이터
  아키텍처라 부르고 무엇이 그것을 "좋다"고 만드는가
- [좋은 데이터 아키텍처의 아홉 원칙](../concepts/good-data-architecture-principles.md) —
  그 판단을 쪼갠 조문들
- [기술 선택의 기준](../concepts/technology-selection-criteria.md) — 아키텍처가 먼저,
  기술이 나중인 이유와 그 나중을 정하는 축들
- [FinOps와 비용 최적화](../concepts/finops-and-cost-optimization.md) — 그 선택에 붙는
  비용의 어휘

## 닿는 페이지

- [데이터 엔지니어링 디자인 패턴](data-engineering-design-patterns.md) — 이 수명 주기와 같은
  순서로 배열되되 각 단계의 해법에 **이름과 결과 목록**을 붙인 카탈로그 축
- [데이터 웨어하우스 모델링](data-warehouse-modeling.md) — 변환·서빙 단계가 실제로 무엇을
  만드는지의 방법론 축
- [배치 처리](batch-processing.md) · [스트림 처리](stream-processing.md) — 반입·변환의 두 양식
- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 운영계와
  분석계의 갈림, 저장 선택의 축
- [DW 운영과 프로세스](dw-operations-and-process.md) — 같은 흐름을 웨어하우스 절차로 본 쪽
- [의미론적 데이터 모델링 전략과 여러 모형](../concepts/semantic-data-modeling-strategies.md) —
  같은 축을 2019년 아키텍처 실무서가 훨씬 얇게 훑되 **모델링 규칙을 "실제로 무엇이 참인가"라는
  물음에서 끌어내는** 자리. 그 장의 뒤 구간이 수집·정제·색인·최적화의 네 역할로 기계 학습
  파이프라인을 배열하는 자리는
  [서비스를 받치는 데이터 저장소와 파이프라인](../concepts/data-stores-and-pipelines-for-services.md)이다

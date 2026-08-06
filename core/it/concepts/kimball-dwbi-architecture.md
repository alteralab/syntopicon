---
type: concept
title: Kimball DW/BI 아키텍처
description: 원천–ETL–프레젠테이션–BI 4구획과 프레젠테이션 4원칙, 독립 마트·CIF와의 대비
generated: { by: "claude-fable-5", at: "2026-08-06T16:10:00Z" }
sources:
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# Kimball DW/BI 아키텍처

Kimball 아키텍처는 DW/BI 환경을 넷으로 가른다: 운영 원천 시스템, ETL 시스템
(back room), 프레젠테이션 영역(front room), BI 애플리케이션 (1장, p.18).[^kimball2013]
운영계와 분석계는 다른 세계라는 전제가 출발점이다 — "운영 시스템은 데이터를
넣는 곳, DW/BI는 꺼내는 곳"이고, 운영계는 이력을 유지하지 않는다 (1장, p.2).[^kimball2013]

## ETL — 주방은 손님 출입 금지

- ETL은 원천과 프레젠테이션 사이의 전부다. 추출→정제·통합(conform)→차원 모델로
  적재가 임무이고, 부가가치는 정제·통합에서 나온다 (1장, pp.19–20).[^kimball2013]
- ETL 내부에 정규화 DB를 두는 것은 허용이지만 최종 목표가 아니며, **정규화
  구조는 사용자 질의에서 차단돼야 한다** — 이해 가능성과 성능이라는 쌍둥이
  목표를 깨기 때문이다 (1장, p.21).[^kimball2013]

## 프레젠테이션 영역의 4원칙

질의 가능한 데이터는 (1장, pp.21–22):[^kimball2013]

1. **차원형**(스타 스키마 또는 OLAP 큐브)이어야 하고
2. **원자 데이터**를 담아야 하며 — "요약만 차원형으로 내놓고 원자 데이터는
   정규화 모델에 가두는 것은 완전히 용납 불가"
3. **업무 프로세스 중심**으로 조직돼야 하고 — 오늘의 보고서(report-of-the-day)
   나 부서별 해석 기준이 아니다
4. **버스 아키텍처**(enterprise data warehouse bus)를 따라야 한다 — 공유
   conformed dimension 없는 차원 모델은 고립된 스토브파이프다.

- conformed dimension은 ETL이 중앙에서 만들어 재사용하는 마스터 데이터로,
  차원 모델 간 통합과 의미 일관성의 장치다. 애자일 반복 개발의 골격(버스
  매트릭스)이기도 하다 (1장, pp.32, 34).[^kimball2013]

## 대안 아키텍처와의 비교 (1장, pp.26–30)[^kimball2013]

- **독립 데이터 마트**: 부서별 무조정 구축 — 옹호자가 없는데도 만연하다.
  같은 원천의 중복 추출과 서로 안 맞는 숫자가 귀결이다.
- **CIF(Inmon 허브-앤-스포크)**: 정규화 3NF EDW가 필수 구조물. 주의할 구분 —
  "정규화는 통합이 아니다": 정규화는 다대일의 물리 구현일 뿐, 통합은 원천 간
  불일치의 해소다. 순수 CIF의 극단은 원자 데이터를 질의하기 어려운 정규화
  구조에 가둔다.
- **하이브리드(CIF + Kimball)**: 3NF EDW를 사용자 차단 상태로 두고 Kimball식
  프레젠테이션을 그 뒤에 단다. 이미 3NF EDW에 투자했다면 적절하지만, 백지에서
  시작하면 데이터 이동·저장 중복으로 시간과 비용이 더 든다.

[Data Vault](../concepts/data-vault-modeling.md)는 이 지형에서 EDW 계층(원천 보존·감사)을
맡는 제3의 접근이고, 정보 마트는 역시 [차원 모델](../concepts/dimensional-modeling.md)로
낸다.

[^kimball2013]: Kimball & Ross 2013, 1장 "Data Warehousing, Business Intelligence, and Dimensional Modeling Primer"

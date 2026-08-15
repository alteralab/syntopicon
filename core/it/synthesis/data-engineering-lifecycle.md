---
type: synthesis
title: 데이터 엔지니어링 수명 주기
description: 원시 데이터를 소비 가능한 산물로 바꾸는 다섯 단계(생성·저장·반입·변환·서빙)와 그 전부를 가로지르는 여섯 저류(보안·데이터 관리·DataOps·데이터 아키텍처·오케스트레이션·소프트웨어 엔지니어링) 진입점
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

## 여섯 저류

저류(undercurrents)는 단계가 아니라 모든 단계를 가로지르는 기반이다 — 이것 없이는 수명 주기의
어느 부분도 제대로 기능하지 못한다.

- [데이터 엔지니어링의 저류](../concepts/data-engineering-undercurrents.md) — 여섯의 목록과 각각이
  수명 주기에 걸리는 방식
- [데이터 관리](../concepts/data-management-discipline.md) — DMBOK 정의와 그 아래 여덟 갈래
- [DataOps](../concepts/dataops.md) — 애자일·데브옵스·통계적 공정 관리를 데이터에 옮긴 것

## 닿는 페이지

- [데이터 웨어하우스 모델링](data-warehouse-modeling.md) — 변환·서빙 단계가 실제로 무엇을
  만드는지의 방법론 축
- [배치 처리](batch-processing.md) · [스트림 처리](stream-processing.md) — 반입·변환의 두 양식
- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 운영계와
  분석계의 갈림, 저장 선택의 축
- [DW 운영과 프로세스](dw-operations-and-process.md) — 같은 흐름을 웨어하우스 절차로 본 쪽

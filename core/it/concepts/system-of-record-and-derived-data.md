---
type: concept
title: 기록 시스템과 파생 데이터
description: 어떤 데이터가 정본이고 어떤 것이 다시 만들 수 있는 사본인가 — 도구가 아니라 용법이 정하는 구분, 그리고 갱신·삭제가 여기서 어려워지는 이유
generated: { by: "claude-opus-5", at: "2026-08-10T20:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
---

# 기록 시스템과 파생 데이터

- [두 정의](#두-정의)
- [왜 이 구분이 쓸모 있나](#왜-이-구분이-쓸모-있나)
- [도구가 아니라 용법이 정한다](#도구가-아니라-용법이-정한다)
- [갱신이 어려운 지점](#갱신이-어려운-지점)
- [삭제 요구가 부딪히는 지점](#삭제-요구가-부딪히는-지점)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **한 조직의 여러 데이터 저장소 중에서 무엇이 정본이고 무엇이
다시 만들 수 있는 사본인가, 그리고 그 구분을 명시하면 무엇이 쉬워지는가.**

운영계와 분석계의 구분(→ [EDW](../concepts/enterprise-data-warehouse.md))과
나란히 놓이지만 축이 다르다. 운영/분석은 **누가 쓰는가**의 구분이고, 기록/파생은
**데이터가 어느 방향으로 흐르는가**의 구분이다 (1장, p.10).[^kleppmann2026]

## 두 정의

- 기록 시스템(system of record, 진실의 원천 source of truth)의 정의는 원문 그대로
  (1장, p.11):[^kleppmann2026]

> A system of record, also known as a *source of truth*, holds the authoritative
> or *canonical* version of data. When new data comes in—for example, as user
> input—it is first written here. Each fact is represented exactly once […]. If
> there is any discrepancy between another system and the system of record, the
> value in the system of record is (by definition) the correct one.

- 파생 데이터 시스템(derived data system)의 정의도 원문 그대로 (1장,
  p.11):[^kleppmann2026]

> Data in a derived system is the result of taking existing data from another
> system and transforming or processing it in some way. If you lose derived
> data, you can re-create it from the original source.

- 파생의 사례: 캐시(있으면 캐시가 답하고, 없으면 원본 데이터베이스로 내려간다),
  비정규화된 값, 인덱스, 구체화 뷰(materialized view), 변환된 표현, 데이터셋으로
  학습한 모델 (1장, p.11).[^kleppmann2026]

## 왜 이 구분이 쓸모 있나

- 파생 데이터는 엄밀히 말해 **중복(redundant)** 이다 — 이미 있는 정보를 복제한다.
  그럼에도 읽기 질의의 성능을 얻으려면 대체로 필수이며, 하나의 원천에서 여러
  데이터셋을 파생시켜 같은 데이터를 여러 관점에서 볼 수 있게 한다 (1장,
  p.11).[^kleppmann2026]
- 분석 시스템은 보통 파생 데이터 시스템이다 — 다른 곳에서 만들어진 데이터의
  소비자이기 때문이다 (1장, p.11).[^kleppmann2026]
- 운영 서비스는 둘이 섞여 있다: 데이터가 처음 쓰이는 주 데이터베이스가 기록
  시스템이고, 흔한 읽기를 빠르게 하는 인덱스·캐시(특히 기록 시스템이 효율적으로
  답할 수 없는 질의용)가 파생이다 (1장, p.11).[^kleppmann2026]
- 어느 데이터가 어느 데이터에서 파생됐는지를 분명히 해 두면, 그러지 않았으면
  혼란스러웠을 시스템 아키텍처가 정리된다 (1장, p.11).[^kleppmann2026]

## 도구가 아니라 용법이 정한다

- 대부분의 데이터베이스·저장 엔진·질의 언어는 그 자체로 기록 시스템도, 파생
  시스템도 아니다. 데이터베이스는 도구일 뿐이고 어떻게 쓰느냐가 당신에게 달려
  있다. 이 구분은 도구가 아니라 **애플리케이션에서의 사용 방식**에 달렸다 (1장,
  p.11).[^kleppmann2026]
- 웨어하우스 쪽 대응 개념과 겹친다: 마스터 데이터의 골든 카피를 정하고 원천으로
  되먹이는
  [마스터 데이터 관리](../concepts/master-data-management.md)가 같은 문제를
  운영계 사이에서 다룬다.

## 갱신이 어려운 지점

- 한 시스템의 데이터가 다른 시스템에서 파생됐다면, 기록 시스템의 원본이 바뀔 때
  파생 데이터를 갱신하는 절차가 필요하다 (1장, p.11).[^kleppmann2026]
- 그런데 많은 데이터베이스는 애플리케이션이 그 데이터베이스 하나만 쓸 것이라는
  가정 위에 설계돼 있어서, **여러 시스템을 통합해 그런 갱신을 전파하기 쉽게
  만들어 주지 않는다** (1장, p.11).[^kleppmann2026] 데이터 파이프라인을 통한 데이터
  통합(data integration)이 이 책 11장의 주제다 (1장, p.11).[^kleppmann2026]
- 실무적 접점: 데이터베이스 변경분을 발행해 다른 시스템이 따라오게 하는 체인지로그
  방식이 이 문제의 흔한 해법이다 —
  [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md)의
  커밋 로그 절과
  [ETL 34 서브시스템](../concepts/etl-subsystems.md)의 변경 데이터 캡처(2)가 그
  자리다.

## 삭제 요구가 부딪히는 지점

- GDPR은 개인에게 요청 시 자기 데이터를 지우게 할 권리(잊힐 권리, right to be
  forgotten)를 준다. 그런데 많은 데이터 시스템은 추가 전용 로그(append-only log)
  같은 불변 구조에 의존한다 — 불변이어야 할 파일 중간의 데이터를 어떻게 지울
  것인가, 그리고 **이미 파생 데이터셋(예: ML 모델 학습 데이터)에 흡수된 데이터의
  삭제는 어떻게 다룰 것인가**. 답하기 어려운 새 공학 과제다 (1장,
  p.24).[^kleppmann2026]
- 현재로서는 어떤 기술·아키텍처가 GDPR을 준수한다고 볼 수 있는지에 대한 명확한
  지침이 없다. 규제는 기술이 빠르게 변하므로 **의도적으로** 특정 기술을 강제하지
  않고, 해석의 대상인 상위 원칙만 제시한다 (1장, p.24).[^kleppmann2026]

## 이어지는 페이지

- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계/분석계 분리라는 다른 축
- [데이터 레이크](../concepts/data-lake.md) — 파생 데이터의 착지 형태가 파일로
  넓어지는 흐름
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 파생
  데이터가 다른 기계에 있을 때 생기는 문제

[^kleppmann2026]: Kleppmann & Riccomini 2026, 1장 "Trade-Offs in Data Systems Architecture"

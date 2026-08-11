---
type: concept
title: 증분 갱신 전략
description: 새 행과 바뀐 행을 이미 만들어진 대상 테이블에 어떻게 반영할 것인가 — 추가·병합·삭제 후 삽입·파티션 덮어쓰기·시간 배치의 의미론과 선택 기준, 그리고 어디까지가 갱신이고 어디부터가 이력인가
status: draft
generated: { by: "claude-opus-5", at: "2026-08-11T04:00:00Z" }
sources:
  - { id: dbtlabs2026-materialization, resource: /it/sources/dbtlabs2026-materialization.md }
---

# 증분 갱신 전략

**목차**: [다섯 가지 의미론](#다섯-가지-의미론) · [병합이 없는 곳에서는 삭제 후 삽입이 병합이 된다](#병합이-없는-곳에서는-삭제-후-삽입이-병합이-된다) · [SCD와의 대응: 어디까지가 갱신이고 어디부터가 이력인가](#scd와의-대응-어디까지가-갱신이고-어디부터가-이력인가) · [집합이 닫혀 있지 않다](#집합이-닫혀-있지-않다) · [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **새 행과 바뀐 행을 이미 만들어진 대상 테이블에 어떤 의미론으로
반영할 것인가.** 증분을 고르기까지의 판단은
[증분 처리와 그 대가](../concepts/incremental-processing-tradeoffs.md).

- 증분이라는 개념을 구현하는 방법은 여럿이고, 각 전략의 값어치를 좌우하는 것은
  셋이다 — 데이터의 양, 유일 키(unique key)의 신뢰도, 데이터 플랫폼의 기능 지원
  (incremental-strategy.md, 서두).[^dbtlabs2026-materialization]

## 다섯 가지 의미론

- **추가(append)**: 기존 데이터를 갱신하거나 삭제하지 않고 선택된 레코드를 대상
  테이블에 삽입한다. 구현이 단순하고 처리 비용이 낮다. 중복을 검사하지도, 레코드가
  이미 있는지 확인하지도 않으므로 같은 레코드가 원천에 여러 번 나타나면 여러 번
  들어간다 — 유스케이스와 데이터 품질 요구에 따라 문제가 아닐 수도 있다
  (incremental-strategy.md, "append").[^dbtlabs2026-materialization]
- **병합(merge)**: 대상 테이블에 없는 유일 키의 레코드는 삽입하고, 있는 키의
  레코드는 갱신한다. 유일 키를 지정하면 기본적으로 매칭된 행을 새 값으로 통째로
  덮어쓴다. 유일 키를 지정하지 않으면 추가 전략처럼 동작한다
  (incremental-strategy.md, "merge", "Strategy-specific
  configs").[^dbtlabs2026-materialization]
  - 유일 키가 이미 있으면 갱신하므로 중복을 푸는 데도 쓸 수 있다. 다만 무엇을
    갱신하고 삽입할지 정하려고 대상 테이블 전체를 훑기 때문에 큰 테이블에서는
    비싸고, 작은 테이블이나 증분 데이터셋에 더 맞는다 (incremental-strategy.md,
    "merge").[^dbtlabs2026-materialization]
- **삭제 후 삽입(delete+insert)**: 해당 유일 키의 데이터를 대상에서 지운 뒤 그 키의
  데이터를 삽입한다. 갱신된 레코드가 온전히 대체되므로 부분 갱신이 생기지 않는다.
  유일 키가 실제로는 유일하지 않을 때나 병합을 지원하지 않는 플랫폼에서 쓸모가
  있고, 큰 데이터셋에서는 덜 효율적일 수 있다 (incremental-strategy.md,
  "delete+insert").[^dbtlabs2026-materialization]
- **파티션 덮어쓰기(insert_overwrite)**: 개별 행을 병합·갱신하는 대신 파티션 단위로
  새 데이터를 넣어 파티션된 테이블을 효율적으로 갱신한다. 테이블 전체가 아니라
  영향받은 파티션만 덮어쓴다. 날짜 같은 키로 파티션된 테이블에 알맞고, 최근 데이터나
  정정된 데이터를 전체 재구축 없이 새로 고치는 데 쓴다 (incremental-strategy.md,
  "insert_overwrite").[^dbtlabs2026-materialization]
- **시간 배치(microbatch)**: 큰 시계열 데이터를 시간 기준 배치(예: 일 또는 시간
  단위)로 쪼개 여러 질의로 처리한다. 배치 병렬 실행을 지원해 실행이 빨라진다
  (incremental-strategy.md, "microbatch",
  "Microbatch").[^dbtlabs2026-materialization]

## 병합이 없는 곳에서는 삭제 후 삽입이 병합이 된다

- 지원되는 곳에서는 병합문 하나로 새 레코드 삽입과 기존 레코드 갱신을 처리한다.
  병합문을 지원하지 않는 웨어하우스에서는 갱신 대상 행을 먼저 지우는 문장과 삽입하는
  문장 둘로 병합을 구현한다 (incremental-models-overview.md, "How incremental models
  work in dbt").[^dbtlabs2026-materialization]

## SCD와의 대응: 어디까지가 갱신이고 어디부터가 이력인가

이론 쪽 지형은 [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md).

- 병합은 변경을 이력으로 추적하지 않고 덮어쓴다는 점에서 SCD 타입 1의 논리를 그대로
  비춘다 (incremental-strategy.md, "merge").[^dbtlabs2026-materialization]
- 추가는 타입 1과도 타입 2와도 직접 맞지 않는다 — 기존 레코드를 덮어쓰는 타입 1과
  다르고, 새 행을 더한다는 점에서 타입 2를 느슨하게 닮았을 뿐 버전 관리나 이력
  변화의 명시적 추적을 하지 않는다 (incremental-strategy.md,
  "append").[^dbtlabs2026-materialization]
- 삭제 후 삽입은 행 수준에서 데이터를 덮어쓰므로 타입 1에도 타입 2에도 직접
  대응하지 않는다. 새 행을 더할 수는 있지만 이력을 추적하지는 않는다
  (incremental-strategy.md, "delete+insert").[^dbtlabs2026-materialization]
- 파티션 덮어쓰기는 파티션을 통째로 바꾸므로, 행 수준의 이력이나 변경을 추적하는
  전형적인 SCD 논리와 맞지 않는다 (incremental-strategy.md,
  "insert_overwrite").[^dbtlabs2026-materialization]
- 문서가 긋는 경계선은 명시적이다 — **타입 2가 필요하면 삭제 후 삽입이 아니라
  스냅샷을 쓰라** (incremental-strategy.md,
  "delete+insert").[^dbtlabs2026-materialization] 그 자리는
  [dbt 스냅샷](../concepts/dbt-snapshots.md).
  - #hypothesis 다섯 전략이 공유하는 성질 하나가 이 경계의 이유로 보인다 — 전부
    **현재 상태를 맞추는** 연산이지 시간 축을 새로 만드는 연산이 아니다. 이력은
    갱신 방식을 고르는 문제가 아니라 별도 자원을 두는 문제가 된다.

## 집합이 닫혀 있지 않다

- dbt v1.2부터 사용자 정의 증분 전략을 쓸 수 있다 — 정해진 이름 규약을 따르는
  매크로를 정의하고 모델에서 그 전략을 지정하는 방식이며, 이는 새 구체화를 통째로
  만드는 것보다 쉬운 대안이다 (incremental-strategy.md, "Custom
  strategies").[^dbtlabs2026-materialization]
- dbt는 사용자 정의 전략을 검증하지 않는다. 그 이름의 매크로를 찾을 뿐이고 없으면
  오류를 낸다 (incremental-strategy.md, "Custom
  strategies").[^dbtlabs2026-materialization]
- 패키지가 제공하는 전략을 끌어다 쓸 수도 있다 (incremental-strategy.md, "Custom
  strategies from a package").[^dbtlabs2026-materialization]

## 이어지는 페이지

- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 증분이 놓인 자리
- [dbt 스냅샷](../concepts/dbt-snapshots.md) — 타입 2 이력을 맡는 별도 자원
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — SCD 처리기(9)와 대리 키
  파이프라인(14)이 같은 일을 웨어하우스 백룸에서 맡는다
- [Data Vault 적재 패턴](../concepts/data-vault-loading-patterns.md) — 삽입만으로
  이력을 만드는 반대편 규약

[^dbtlabs2026-materialization]: dbt Labs 2026, dbt 공식 문서 "Build" 절

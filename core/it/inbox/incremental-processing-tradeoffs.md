---
type: concept
title: 증분 처리와 그 대가
description: 전체 재계산을 포기하고 바뀐 것만 처리하기로 하면 무엇을 얻고 무엇을 떠안는가 — 상태를 갖게 되면서 깨지는 멱등성, 로직이 바뀌면 필요한 전체 재구축, 소급되지 않는 스키마 변경
status: draft
generated: { by: "claude-opus-5", at: "2026-08-11T04:00:00Z" }
sources:
  - { id: dbtlabs2026-materialization, resource: /it/sources/dbtlabs2026-materialization.md }
---

# 증분 처리와 그 대가

- [무엇을 얻는가](#무엇을-얻는가)
- [상태를 갖는 대가 — 멱등성](#상태를-갖는-대가--멱등성)
- [행의 동일성을 선언해야 갱신이 성립한다](#행의-동일성을-선언해야-갱신이-성립한다)
- [로직이 바뀌면 과거는 옛 로직으로 남는다](#로직이-바뀌면-과거는-옛-로직으로-남는다)
- [스키마 변경은 소급되지 않는다](#스키마-변경은-소급되지-않는다)
- [늦게 도착한 데이터](#늦게-도착한-데이터)
- [실패했을 때](#실패했을-때)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **전체를 다시 계산하는 대신 바뀐 것만 처리하기로 하면 무엇을
얻고 무엇을 떠안는가.** 형태 선택의 지형은
[구체화 스펙트럼](../concepts/materialization-spectrum.md).

## 무엇을 얻는가

- 증분(incremental) 모델은 첫 실행에서 원천 데이터의 **모든** 행을 변환해 테이블을
  만들고, 이후 실행에서는 걸러 내라고 지정한 행만 변환해 이미 만들어진 대상
  테이블에 넣는다 (incremental-models.md,
  서두).[^dbtlabs2026-materialization]
- 걸러 내는 대상은 대개 마지막 실행 이후 생성되거나 갱신된 행이다. 변환해야 하는
  데이터의 양이 제한되므로 실행 시간이 크게 줄고, 웨어하우스 성능이 좋아지고 연산
  비용이 준다 (incremental-models.md, 서두).[^dbtlabs2026-materialization]
- 도입 기준: 원천이 수백만~수십억 행이거나, 정규식·UDF처럼 계산이 오래 걸리고 복잡한
  변환일 때다. 뷰와 테이블 사이에서 복잡도와 성능을 절충하는 자리이고, 추가 설정이
  필요한 고급 사용법이므로 실행이 느려질 때 도입하기를 권한다
  (incremental-models-overview.md, "Understand incremental models", "When to use an
  incremental model").[^dbtlabs2026-materialization]

## 상태를 갖는 대가 — 멱등성

- 증분 모델은 상태를 갖는다(stateful). 원문 직인용 (incremental-models-overview.md,
  서두):[^dbtlabs2026-materialization]

> Incremental models are stateful, so they're the easiest place to accidentally
> break idempotence — the expectation that re-running a model produces the same
> result.

- 한 코드가 두 실행 경로를 겸한다: 증분 필터는 증분 실행일 때만 적용되고, 모델의
  SQL은 증분 실행일 때와 아닐 때 **양쪽에서** 유효해야 한다 (incremental-models.md,
  "Understand the is_incremental() macro").[^dbtlabs2026-materialization]
  - 필터를 어디에 두느냐가 성능까지 좌우한다 — 공통 테이블 식을 쓰는 복잡한 모델에서
    레코드를 이른 단계에서 거르면 실행 시간이 크게 줄 수 있다 (incremental-models.md,
    "Filtering rows on an incremental run").[^dbtlabs2026-materialization]

## 행의 동일성을 선언해야 갱신이 성립한다

- 유일 키(unique key)를 정의하면 새 행을 덧붙이는 대신 기존 행을 갱신할 수 있다 —
  같은 키에 새 정보가 오면 현재 정보를 대체하고, 중복 행이 오면 무시할 수 있다
  (incremental-models.md, "Defining a unique
  key").[^dbtlabs2026-materialization]
- 유일 키를 지정하지 않으면 대부분의 어댑터에서 추가 전용으로 동작한다 — 모델
  SQL이 반환한 모든 행이 중복 여부와 무관하게 삽입된다 (incremental-models.md,
  "Defining a unique key").[^dbtlabs2026-materialization]
- 유일 키가 지정하는 것은 모델의 grain이다 — 하나의 유일한 행을 식별하는 필드 또는
  필드 조합 (incremental-models.md, "Defining a unique
  key").[^dbtlabs2026-materialization] 차원 설계에서 grain을 계약으로 다루는 자리는
  [4단계 차원 설계 프로세스](../concepts/four-step-dimensional-design.md).
- 키 컬럼에 null이 있으면 행 매칭에 실패해 중복 행이 생길 수 있다. 여러 컬럼이
  필요하면 대리 키(surrogate key) 한 컬럼으로 응축하는 방법이 있다
  (incremental-models.md, "Defining a unique key").[^dbtlabs2026-materialization]
  대리 키 자체는 [차원 테이블](../concepts/dimension-table.md).
- 유일 키가 대상 테이블에서든 새 증분 행에서든 둘 이상의 행을 가리키면 실행이 실패할
  수 있다 — 데이터베이스와 갱신 전략에 따라 다르다 (incremental-models.md, "Defining
  a unique key").[^dbtlabs2026-materialization]
- 예시가 보여 주는 것: 일별 활성 사용자 수처럼 같은 날에 여러 번 실행되는 집계는
  유일 키가 없으면 그 날짜에 대해 실행 횟수만큼 행이 쌓인다 (incremental-models.md,
  "unique_key example").[^dbtlabs2026-materialization]

## 로직이 바뀌면 과거는 옛 로직으로 남는다

- 증분 모델의 로직이 바뀌면 새 행에 적용되는 변환이 대상 테이블에 이미 저장된 과거
  변환과 갈라진다. 이때는 모델을 다시 지어야 한다 (incremental-models.md, "How do I
  rebuild an incremental model?").[^dbtlabs2026-materialization]
- 전체 재구축(full refresh)은 기존 대상 테이블을 지우고 전 기간을 다시 만드는 일이다.
  하류 모델까지 함께 돌릴 수 있고, 그중 증분 모델이 있으면 그것들도 전체 재구축된다
  (incremental-models.md, "How do I rebuild an incremental
  model?").[^dbtlabs2026-materialization]

## 스키마 변경은 소급되지 않는다

- 증분 모델의 컬럼이 바뀔 때의 정책을 고를 수 있다 — 무시(기본값), 원천과 대상
  스키마가 갈라지면 오류로 세우기, 새 컬럼만 덧붙이기, 완전 동기화(새 컬럼 추가 +
  없어진 컬럼 제거, 데이터 타입 변경 포함). 이 정책들이 있어 스키마가 변해도 전체
  재구축을 덜 하게 되고 질의 비용을 아낀다 (incremental-models.md, "What if the
  columns of my incremental model change?").[^dbtlabs2026-materialization]
- **어느 정책도 새로 추가된 컬럼의 과거 행 값을 채워 주지 않는다.** 채우려면 수동
  갱신을 돌리거나 전체 재구축을 걸어야 한다 (incremental-models.md, "What if the
  columns of my incremental model change?").[^dbtlabs2026-materialization]
- 기본값에서는 컬럼을 추가해도 대상 테이블에 나타나지 않고, 컬럼을 제거하면 실행이
  실패한다 (incremental-models.md, "Default
  behavior").[^dbtlabs2026-materialization]
- 추적 범위는 최상위 컬럼 변경까지다 — 중첩 컬럼의 추가·제거·수정은 스키마 변경으로
  감지되지 않는다 (incremental-models.md, "What if the columns of my incremental
  model change?").[^dbtlabs2026-materialization]

## 늦게 도착한 데이터

- 문서는 증분 모델의 한계와 성능 고려, 그리고 **지각 도착 데이터의 처리**를 별도
  논의로 넘긴다 — 특히 큰 데이터셋에서 그렇다고 말한다
  (incremental-models-overview.md, "When to use an incremental
  model").[^dbtlabs2026-materialization]
  - #hypothesis 마지막 실행 시각 이후를 조건으로 거는 필터는 그보다 이른
    타임스탬프를 달고 뒤늦게 도착한 행을 통과시키지 못한다. 그 자리의 처리 규칙은
    [지각 도착 데이터](../concepts/late-arriving-data.md).
- 큰 시계열 데이터를 시간 기준 배치로 쪼개 여러 질의로 처리하는 전략은, 데이터의
  양과 성격에 따라 새 데이터를 한 질의로 넣는 것보다 효율적이고 견고할 수 있다
  (incremental-strategy.md, "Microbatch").[^dbtlabs2026-materialization]

## 실패했을 때

- 일부 데이터 플랫폼이 쓰는 트랜잭션 관리는 한 묶음의 동작을 하나의 작업 단위로
  다룬다 — 그 단위의 일부가 실패하면 열린 트랜잭션을 되돌려 데이터베이스를 좋은
  상태로 복원한다 (incremental-models-overview.md, "How incremental models work in
  dbt").[^dbtlabs2026-materialization]

## 이어지는 페이지

- [증분 갱신 전략](../concepts/incremental-update-strategies.md) — 바뀐 행을 실제로
  어떤 의미론으로 반영하는가
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 증분이 놓인 자리
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 이력 적재는 사람이 멈춰
  확인해도 되지만 증분 처리는 완전 자동화여야 한다는 경계
- [dbt 스냅샷](../concepts/dbt-snapshots.md) — 증분 갱신으로는 남길 수 없는 이력을
  맡는 다른 자원

[^dbtlabs2026-materialization]: dbt Labs 2026, dbt 공식 문서 "Build" 절

---
type: concept
title: dbt 스냅샷 — SCD 타입 2의 구현
description: 덮어써지는 원천 테이블에서 이력을 만들어 내는 방법 — 변경 탐지 두 전략, 유효 구간 메타 컬럼, 삭제된 행의 처리, 그리고 킴벌의 SCD 타입 2 이론과 겹치는 자리
generated: { by: "claude-opus-5", at: "2026-08-11T04:00:00Z" }
sources:
  - { id: dbtlabs2026-materialization, resource: /it/sources/dbtlabs2026-materialization.md }
  - { id: kimball2013, resource: /it/sources/kimball2013.md }
---

# dbt 스냅샷 — SCD 타입 2의 구현

- [어떻게 도는가](#어떻게-도는가)
- [변경 탐지 — 이론이 주어진 것으로 둔 자리](#변경-탐지--이론이-주어진-것으로-둔-자리)
- [메타 컬럼 — 킴벌의 관리 열과 겹치는 자리](#메타-컬럼--킴벌의-관리-열과-겹치는-자리)
- [원천에서 행이 사라졌을 때](#원천에서-행이-사라졌을-때)
- [운영 규범](#운영-규범)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **원천 테이블이 덮어써져 과거 상태가 사라질 때, 이력을 어떻게
만들어 내는가.** 이론 쪽 지형은
[완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)이고, 여기는
그 타입 2가 도구에서 실제로 어떤 모양이 되는지를 본다.

- 문제 상황: 분석가는 가변 테이블의 이전 데이터 상태를 되돌아봐야 하는데, 원천
  시스템이 이력 데이터 접근을 가능하게 만들어 두었으리라는 보장이 없다. 스냅샷
  (snapshot)은 가변 테이블의 변경을 시간에 걸쳐 기록하는 장치다 (snapshots.md,
  "What are snapshots?").[^dbtlabs2026-materialization]
- 이론과 구현이 만나는 문장. 원문 직인용 (snapshots.md, "What are
  snapshots?"):[^dbtlabs2026-materialization]

> Snapshots implement type-2 Slowly Changing Dimensions over mutable source tables.

- 예시의 요지: 주문 상태가 pending에서 shipped로 덮어써지면 그 주문이 마지막으로
  pending이었던 시점의 정보가 사라져, 배송까지 얼마나 걸렸는지를 분석하기 어렵거나
  불가능해진다. 스냅샷 테이블은 같은 주문 식별자에 대해 상태별로 행을 남기고 각
  행에 유효 시작·유효 종료를 붙인다 (snapshots.md, "What are
  snapshots?").[^dbtlabs2026-materialization]

## 어떻게 도는가

- 첫 실행: 질의 결과에 유효 시작(`dbt_valid_from`)·유효 종료(`dbt_valid_to`)
  컬럼을 더한 초기 스냅샷 테이블을 만든다. 모든 레코드의 유효 종료는 비어 있다
  (snapshots.md, "How snapshots work").[^dbtlabs2026-materialization]
- 이후 실행: 바뀐 레코드와 새로 생긴 레코드를 확인해, 바뀐 기존 레코드의 유효
  종료를 채우고 갱신된 레코드와 새 레코드를 삽입한다. 새로 삽입된 행의 유효 종료는
  다시 비어 있다 (snapshots.md, "How snapshots
  work").[^dbtlabs2026-materialization]
- 스냅샷은 하류 모델에서 모델과 같은 방식으로 참조된다 (snapshots.md, "How snapshots
  work").[^dbtlabs2026-materialization]
- 스냅샷은 자주 실행할 때만 쓸모가 있다 — 정기 실행 일정이 필요하다 (snapshots.md,
  "Add a snapshot to your project").[^dbtlabs2026-materialization]
  - #hypothesis 원천이 덮어쓰기 때문에, 두 실행 사이에 값이 두 번 바뀌면 중간
    상태는 어디에도 남지 않는다. 실행 주기가 곧 이력의 해상도 상한이다.

## 변경 탐지 — 이론이 주어진 것으로 둔 자리

- 스냅샷 전략(strategy)은 dbt가 행이 바뀌었는지 아는 방법을 정의한다. 내장 전략은
  둘이다 (snapshots.md, "Detecting row
  changes").[^dbtlabs2026-materialization]
  - **갱신 시각 기준(timestamp)**: 설정된 갱신 시각 컬럼이 마지막 스냅샷 실행보다
    최신이면 옛 레코드를 무효화하고 새 레코드를 기록한다. 시각이 그대로면 아무 조치도
    하지 않는다.
  - **컬럼 비교 기준(check)**: 신뢰할 만한 갱신 시각 컬럼이 없는 테이블에 쓴다.
    지정한 컬럼 목록의 현재 값과 이력 값을 비교해 하나라도 달라졌으면 옛 레코드를
    무효화하고 새 레코드를 기록한다. 값이 같으면 아무 조치도 하지 않는다.
- 권고는 갱신 시각 기준이다 — 추적할 컬럼이 하나뿐이고, 원천 테이블의 컬럼 추가·삭제를
  자동으로 감당하며, 스키마가 시간이 지나며 진화해도 오류가 덜 난다. 컬럼 비교
  기준은 검사 대상 컬럼 목록을 스키마를 따라 고쳐야 한다 (snapshots.md,
  "Configuration best practices", "Timestamp strategy
  (recommended)").[^dbtlabs2026-materialization]
- 컬럼 비교에서 모든 컬럼을 검사하도록 두는 것보다 검사할 컬럼을 명시적으로
  열거하는 편이 낫고, 많은 컬럼을 하나로 응축하려면 대리 키(surrogate key)를 쓰는
  방법이 있다 (snapshots.md, "Check strategy").[^dbtlabs2026-materialization] 같은
  요령이 [Data Vault의 해시 규율](../concepts/hashing-in-data-vault.md)의 hash
  diff다.
- 유효 구간에 찍히는 시각의 출처가 전략마다 다르다 (snapshots.md, "Strategy and
  meta-field timestamps"):[^dbtlabs2026-materialization]
  - 갱신 시각 기준에서는 설정된 갱신 시각 컬럼이 유효 시작·유효 종료·변경 시각
    컬럼을 모두 채운다. 문서의 예시는 11:00에 실행해도 그 11:00이 어디에도 쓰이지
    않고 원천의 10:47이 쓰인다는 것을 보여 준다 (snapshots.md, "Strategy and
    meta-field timestamps").[^dbtlabs2026-materialization]
  - 컬럼 비교 기준에서는 현재 시각이 각 컬럼을 채운다. 갱신 시각 컬럼을 함께
    설정하면 그 값을 쓰고, 그 값이 비어 있으면 현재 시각으로 되돌아간다
    (snapshots.md, "Strategy and meta-field timestamps", "Example usage with
    updated_at").[^dbtlabs2026-materialization]
  - #hypothesis 그래서 컬럼 비교 기준의 유효 구간은 사건이 일어난 시각이 아니라
    dbt가 관측한 시각이다. 같은 타입 2 구조라도 두 전략이 만드는 시간 축의 의미가
    다르다.

## 메타 컬럼 — 킴벌의 관리 열과 겹치는 자리

- 스냅샷 테이블은 원천 데이터셋의 복제본에 메타 필드가 더해진 형태로 만들어진다
  (snapshots.md, "Snapshot meta-fields").[^dbtlabs2026-materialization]
  - 유효 시작(`dbt_valid_from`) — 이 스냅샷 행이 유효해진 시각. 한 레코드의 여러
    버전을 정렬하는 데 쓴다.
  - 유효 종료(`dbt_valid_to`) — 이 행이 무효화된 시각. 가장 최근 행은 비어 있다.
  - 버전 키(`dbt_scd_id`) — 스냅샷 행마다 생성되는 유일 키. dbt가 각 SCD 버전을
    식별하는 데 내부적으로 쓴다.
  - 변경 시각(`dbt_updated_at`) — 이 스냅샷 행이 삽입될 때의 원천 레코드 변경 시각.
- 삽입 시 유효 시작과 변경 시각은 같은 값에서 온다. 그래도 둘은 각각 유효 시작과
  기록된 변경 시각을 뜻하므로 의미가 다르다 (snapshots.md, "Snapshot
  meta-fields").[^dbtlabs2026-materialization]
- 현재 행의 유효 종료는 기본이 비어 있고(NULL), **dbt Core 1.9부터** 미래 날짜 같은
  값을 지정해 대신 넣을 수 있다 — 기간 필터가 단순해진다 (snapshots.md,
  "Configuration best practices", "Snapshot
  meta-fields").[^dbtlabs2026-materialization]
  - 이론이 먼저 권고한 자리다: 타입 2의 관리 열에서 새 행의 만료일을 9999-12-31로
    두면 null을 피해 BETWEEN으로 특정일의 유효 행을 찾을 수 있다 (5장,
    pp.152–153).[^kimball2013]
- 버전마다 유일 키를 생성한다는 것도 이론과 같은 자리다: 타입 2는 같은 자연 키에
  프로파일 버전이 여럿 생기므로 자연 키를 기본 키로 쓸 수 없고, 단일 열 대리 키
  하나가 팩트와 차원의 연결을 확립한다 (5장, p.153).[^kimball2013]
- 메타 컬럼의 이름은 팀이나 조직의 규약에 맞게 바꿀 수 있다(dbt Core 1.9부터)
  (snapshots.md, "Snapshot meta-fields").[^dbtlabs2026-materialization]

## 원천에서 행이 사라졌을 때

- **dbt v1.9부터** 원천에서 삭제된 행을 어떻게 다룰지 고를 수 있다. 이것은 별도의
  전략이 아니라 어느 스냅샷 전략과도 함께 쓰는 선택 기능이다 (snapshots.md, "Hard
  deletes (opt-in)").[^dbtlabs2026-materialization]
  - 아무 조치도 하지 않기(기본값).
  - 유효 종료를 채워 무효화하기.
  - 삭제됨 표시를 단 새 행으로 기록하기 — 이후 레코드가 복원되면 표시를 끈 새 행이
    다시 들어간다.
- 속성 값의 변화가 아니라 행 자체의 소멸을 다루는 축이라 타입 0–7의 분류와는 층위가
  다르다 (snapshots.md, "Hard deletes
  (opt-in)").[^dbtlabs2026-materialization]

## 운영 규범

- **스냅샷은 다시 만들 수 없다.** 그래서 별도 스키마에 두어 사용자가 특별한 것임을
  알게 하고, 모델과 다른 권한을 주고 다른 사용자(또는 역할)로 실행해 정말 원할 때가
  아니면 지우기 매우 어렵게 만들라는 권고가 붙는다 (snapshots.md, "Configuration
  best practices").[^dbtlabs2026-materialization]
- 유일 키가 실제로 유일한지가 결정적이다 — dbt가 이 키로 행을 맞추기 때문이다.
  원천을 스냅샷한다면 원천에 유일성 테스트를 붙이기를 권한다 (snapshots.md,
  "Configuration best practices").[^dbtlabs2026-materialization]
- 정제나 변환이 필요하면 스냅샷 정의 안에서 하지 말고, 앞단에 변환을 맡는 모델을
  두고 스냅샷이 그것을 참조하게 한다. 스냅샷 정의가 깨끗하게 유지되고 변환을 따로
  테스트·실행할 수 있다 (snapshots.md, "Configuration best practices", "Add a
  snapshot to your project").[^dbtlabs2026-materialization] 같은 분업의 웨어하우스
  쪽 이름이 [스테이징 영역](../concepts/staging-area.md)이다.

## 이어지는 페이지

- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — 타입 0–7의
  이론 지형
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) —
  다시 만들 수 없다는 성질이 스냅샷을 파생이 아닌 쪽으로 옮겨 놓는다
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 변경 데이터 캡처(2)와 SCD
  처리기(9)가 같은 일을 맡는 자리
- [증분 갱신 전략](../concepts/incremental-update-strategies.md) — 이력이 필요할 때
  증분 전략이 아니라 여기로 오는 이유
- [Data Vault Satellite](../concepts/data-vault-satellite.md) — 삽입만으로 전체
  변경 이력을 담는 다른 규약

[^dbtlabs2026-materialization]: dbt Labs 2026, dbt 공식 문서 "Build" 절
[^kimball2013]: Kimball & Ross 2013, 5장 "Procurement"

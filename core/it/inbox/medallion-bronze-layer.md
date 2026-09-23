---
type: concept
title: 메달리온 Bronze 계층
status: draft
description: "메달리온 아키텍처의 첫 계층 — 원시 데이터를 원래 구조 그대로 받아 질의 가능한 저수지로 만드는 계층의 규정과 설계 결정들: 단일 물리 계층인가 하위 계층 여럿인가를 가르는 처리 계층 구조, 전체 적재와 증분 적재(append 모드와 merge 모드, 증분이 성립하는 전제와 그것이 깨질 때 CDC로 가는 경계), Bronze가 감당하는 이력화와 감당하지 않는 SCD2, 읽기 스키마와 쓰기 스키마를 한 계층 안에서 잇달아 쓰는 배치와 mergeSchema·Delta 제약과 스키마 화해 네 가지, 기술 검증 검사와 침습·비침습이라는 두 무결성 처리 정책, 원시 데이터를 업무 사용자에게 열지 않는 근거와 거버넌스 의무, 그리고 실무의 Bronze가 랜딩·전처리·검증 파킹 존으로 늘어나거나 가상 계층이 되는 자리"
generated: { by: "claude-opus-5", at: "2026-09-23T23:00:00Z" }
sources:
  - { id: strengholt2025, resource: /it/sources/strengholt2025.md }
---

# 메달리온 Bronze 계층

- [버전 조건](#버전-조건)
- [계층 셋의 흐름과 "논리적"이라는 전제](#계층-셋의-흐름과-논리적이라는-전제)
- [이 계층의 규정](#이-계층의-규정)
- [처리 계층 구조 — 하나인가 여럿인가](#처리-계층-구조--하나인가-여럿인가)
- [전체 적재](#전체-적재)
- [증분 적재](#증분-적재)
- [Bronze 안에서의 이력화](#bronze-안에서의-이력화)
- [스키마 진화와 관리](#스키마-진화와-관리)
- [mergeSchema와 스키마 강제](#mergeschema와-스키마-강제)
- [기술 검증 검사](#기술-검증-검사)
- [사용과 거버넌스](#사용과-거버넌스)
- [실무에서의 Bronze](#실무에서의-bronze)
- [이 KB의 원전과 맞대어 본 것](#이-kb의-원전과-맞대어-본-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **원시 데이터를 받는 계층은 무엇을 보장하고 무엇을 보장하지 않는가, 그리고
그 안에서 갈리는 설계 결정은 무엇인가.**

[메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md)가 Bronze·Silver·
Gold 셋을 한 문장씩으로 규정하고, [메달리온 계층 이전의 결정과 Delta 테이블 관리](../concepts/medallion-groundwork-and-delta-table-management.md)가
계층 바깥의 전제를 받는다면, 이 페이지부터 계층 셋을 하나씩 연다. 저자는 3장의 목적을 각 계층의
설계를 **이론의 관점에서** 자기 실무 경험으로 풀어 내는 것이라 적고, 이론에서 실천으로의 전환은
II부가 맡는다고 못 박는다 (3장 도입).[^strengholt2025]

## 버전 조건

> **버전 조건**: 2025년 저술 시점. 아래
> [mergeSchema와 스키마 강제](#mergeschema와-스키마-강제)와
> [기술 검증 검사](#기술-검증-검사)의 도구 목록은 Delta Lake·Databricks·Azure의 그 시점 구현에
> 묶인다. 그 밖의 절(적재 방식의 선택, 이력화의 경계, 무결성 처리 정책)은 설계 판단이라 시점에
> 둔감하다. 이 소스에 공표된 만료 날짜가 없어 `stale_after`는 걸지 않는다.

## 계층 셋의 흐름과 "논리적"이라는 전제

- 저자는 각 계층의 세부로 들어가기 전에 **계층을 논리적인 것으로 생각하라**고 못 박는다 — 예컨대
  Bronze 계층을 말할 때 그것을 **물리 계층 하나로 틀 짓지 말고 여러 물리 계층에 걸칠 수 있는
  논리 계층으로 보라**는 것이고, 그래야 유연성을 지키고 구조를 더 잘 이해하게 된다는 것이다
  (3장 §"The Three-Layered Design").[^strengholt2025] 이 전제가 아래
  [처리 계층 구조](#처리-계층-구조--하나인가-여럿인가)와
  [실무에서의 Bronze](#실무에서의-bronze)의 근거가 된다.
- 계층 셋을 가로지르는 흐름은 그림 3-1이 그린다. **본문에는 없고 그림에만 있는 라벨**은 계층마다
  괄호로 붙은 한정사다 (3장 §"The Three-Layered Design", 그림 3-1):[^strengholt2025]

> Bronze layer (raw copies) · Silver layer (filtered, clean, augmented) ·
> Gold layer (modeled for consumption)

  - 그림의 왼쪽 끝은 원천 셋(OLTP 시스템·ERP 시스템·CRM 시스템)이고, 그 다음이 랜딩 존이며 그
    안에 blob 파일 저장과 Kafka 둘이 나란히 놓인다. 곧 **랜딩 존은 파일 저장과 메시지 시스템
    양쪽을 받는 자리**로 그려져 있다 (3장 §"The Three-Layered Design", 그림
    3-1).[^strengholt2025]

## 이 계층의 규정

- 저자가 Bronze에 붙이는 정의는 이렇다 — **여러 원천에서 모은 원시 데이터의 구역으로 작동하고,
  데이터는 어떤 변환도 없이 원래 구조 그대로 저장되며, 이력 기록(historical record)이자 단일
  진실 원천(single source of truth)으로 봉사한다.** 데이터가 안정적으로 포착·저장되게 해 추가
  처리에 쓸 수 있게 한다 (3장 §"The Three-Layered Design").[^strengholt2025]
- 핵심 특성 셋은 **높은 볼륨·다양성·진실성**(high volume, variety, and veracity)이고, **데이터는
  원래 상태의 무결성을 지키기 위해 불변(immutable)**이다 (3장 §"The Three-Layered
  Design").[^strengholt2025]
- 계층의 목표를 저자는 한 낱말로 줄인다 — Bronze의 주 목표는 원천 데이터를 수정 없이 원래
  상태로 저장하는 것이고, 데이터가 추가 처리에 쉽게 접근 가능하게 하며 사용자가 즉시 탐색·분석할
  수 있게 한다. 본질적으로 **원시 데이터를 위한 질의 가능한 저수지(queryable reservoir)**로
  봉사한다 (3장 §"Bronze Layer").[^strengholt2025]

## 처리 계층 구조 — 하나인가 여럿인가

- Bronze가 단일 물리 계층인지 여러 하위 계층으로 이뤄지는지는 **원천의 복잡도와 조직의 요구**에
  달렸다 (3장 §"Bronze Layer" ▸ "Processing Hierarchy").[^strengholt2025]
- 저자가 드는 시나리오는 로컬 파일 저장 위치로만 데이터를 내보내는 레거시 애플리케이션이다. 전통적
  원천 시스템은 흔히 내보내기 형식을 강제하며 대개 CSV나 JSON을 쓴다. 이 경우 배치 처리로 메달리온
  아키텍처에 통합하게 된다 (3장 §"Bronze Layer" ▸ "Processing Hierarchy").[^strengholt2025]
- 그때의 전형적 흐름이 다섯 걸음이다 (3장 §"Bronze Layer" ▸ "Processing
  Hierarchy"):[^strengholt2025]
  - 랜딩 존에 데이터를 스테이징하고 최소 처리를 한다 — 압축 파일 해제, 체크섬 비교, 메타데이터
    생성.
  - Bronze로 복사하면서 성능을 위해 Delta Lake 같은 형식으로 변환한다.
  - 이 단계에서 데이터 무결성을 위한 기본 검증을 수행한다.
  - 선택적으로 민감 정보 보호를 위해 분류하거나 암호화한다.
  - 마지막으로 기존 Bronze 데이터셋과 비교·통합해 일관성과 완전성을 유지한다.
- 곁줄 하나가 암호화의 자리를 못 박는다 — **원시 데이터의 암호화는 개인 식별 정보(PII)를 무단
  접근에서 보호하는 데 필수적이므로, 데이터가 Bronze에 착지하기 전에 암호화하는 일이 드물지
  않다.** Fernet 같은 오픈소스 암호화 프레임워크나 다른 암호화 도구로 할 수 있다 (3장
  §"Bronze Layer" ▸ "Processing Hierarchy" 곁줄).[^strengholt2025]
- 그래서 Bronze는 흔히 **하위 계층 셋**을 포함한다 — 내부 스테이징 영역, 처리·정제 영역, 그리고
  최종적으로 Delta 형식의 저장이다. 곧 Bronze가 단일 물리 계층인지 하위 계층 여럿인지는 원천
  복잡도, 조직 요구, 그리고 **랜딩 존을 Bronze의 일부로 볼 것인가의 결정**에 달렸다 (3장
  §"Bronze Layer" ▸ "Processing Hierarchy").[^strengholt2025]
- 처리 패턴의 선택이 그다음이다 — 원천마다 전달 방식이 크게 다르기 때문이다. 어떤 시스템은 전체
  추출을 주고, 어떤 시스템은 델타 증분을 전달하며, 또 어떤 시스템은 연속적으로 스트리밍한다
  (3장 §"Bronze Layer" ▸ "Processing Hierarchy").[^strengholt2025]

## 전체 적재

- 정의 — **전체 적재(full data load)는 변경분만이 아니라 원천 시스템의 데이터셋 전체를 옮겨
  하류 처리에 모든 데이터를 쓸 수 있게 하는 것**이다 (3장 §"Bronze Layer" ▸ "Processing Full
  Data Loads").[^strengholt2025]
- 운영 형태 (3장 §"Bronze Layer" ▸ "Processing Full Data Loads"):[^strengholt2025]
  - 큰 배치를 고정 간격으로 다루고, 랜딩 존은 선택적으로 쓴다.
  - 검증을 거친 뒤 원시 형태로 저장되어 **이전의 모든 전달분과 나란히 폴더에 누적된다.**
  - 이 단계에서는 대개 최소 변환만 한다 — 때로 데이터를 걸러 내거나 민감 컬럼을 암호화한다.
  - 누적한 뒤 **가장 최근 전달분**을 Delta Lake 형식으로 변환하거나 외부 테이블(external table)로
    노출해 다음 계층이 처리하게 한다.

## 증분 적재

- 증분 적재는 **"델타 적재(delta loads)"**라 불리기도 하며, 데이터의 변경이나 갱신만 처리하면
  되는 시나리오에 쓰여 전체 적재보다 효율적이고 처리 시간을 줄인다 (3장 §"Bronze Layer" ▸
  "Processing Incremental Data Loads").[^strengholt2025] 저자는 각주에서 델타 적재를 **마지막
  적재 이후 새로 추가되거나 수정된 데이터만 적재하는 것, 곧 전체 데이터셋을 다시 적재하지 않는
  것**으로 정의한다 (3장 각주 1).[^strengholt2025]
- 흐름 — 바뀐 데이터만 받고(흔히 이벤트 형태로), 대개 예비 계층에 스테이징한 뒤 가벼운 변환을
  먼저 건다(파일 형식 변경, Delta Lake 형식으로의 변환, 단순한 데이터 타입 교정). 그다음
  **append 모드나 merge 연산**으로 Bronze에 이미 있는 데이터와 통합한다 (3장 §"Bronze Layer" ▸
  "Processing Incremental Data Loads").[^strengholt2025]
- **append 모드** — Delta Lake의 맥락에서 이것은 **기존 데이터를 수정하거나 삭제하지 않고 기존
  Delta 테이블에 새 데이터를 더하는 것**이다. 로깅이나 스트리밍 데이터처럼 기존 데이터에 영향을
  주지 않고 새 레코드를 계속 더하고 싶은 시나리오에 유용하다 (3장 §"Bronze Layer" ▸ "Processing
  Incremental Data Loads").[^strengholt2025]
  - 저자가 드는 Spark 예제는 두 줄이다. `df = spark.read.json(f"{filePath}/events/*.json")`로
    DataFrame에 읽어 들이고, `df.write.format("delta").mode("append").saveAsTable("events")`로
    Delta 테이블에 덧붙인다. 여기서 `df`는 이름 붙은 컬럼을 가진 구조적 데이터 모음인 DataFrame이다
    (3장 §"Bronze Layer" ▸ "Processing Incremental Data Loads").[^strengholt2025]
  - **append 모드는 갱신도 삭제도 다루지 않는다** — 데이터셋 끝에 새 데이터를 붙일 뿐이다 (3장
    §"Bronze Layer" ▸ "Processing Incremental Data Loads").[^strengholt2025]
- **merge 모드** — Delta 테이블에 **upsert(갱신과 삽입의 결합)**를 수행하는 방법이다. 지정한 조건에
  따라 기존 레코드를 갱신하면서 새 레코드를 삽입하는 일을 한 연산으로 해야 할 때 특히 유용하다
  (3장 §"Bronze Layer" ▸ "Processing Incremental Data Loads").[^strengholt2025]
  - 저자의 예는 최근 180일 안에 원천에 존재하는 고객을 `is_current` 플래그로 표시한 고객 정보
    테이블이다. Delta 테이블에 `MERGE` 연산을 쓰면 세 가지를 동시에 처리한다 — 새 고객 삽입,
    최근에 돌아온 고객의 상태 갱신, 그리고 비활성이 된 기존 고객의 상태 수정이다 (3장
    §"Bronze Layer" ▸ "Processing Incremental Data Loads").[^strengholt2025]
- 증분 적재는 Bronze만의 것이 아니다 — **Silver·Gold를 포함한 어느 계층에서든 전체 데이터셋을
  재처리하지 않고 갱신하는 데 필수적**이고, change data feed와 결합해 증분 변경을 다음 계층으로
  밀어 넣는 것이 고려할 조합이다 (3장 §"Bronze Layer" ▸ "Processing Incremental Data
  Loads").[^strengholt2025]
- **증분이 성립하는 전제**가 둘이고, 둘째가 깨지는 자리가 CDC로 가는 경계다 (3장 §"Bronze Layer"
  ▸ "Processing Incremental Data Loads"):[^strengholt2025]
  - 원천 시스템 테이블에 **유일 증분 식별자나 `updated_at` 컬럼**이 있어야 한다. 이 표지가
    마지막 적재 이후의 신규·갱신 레코드를 탐지하게 한다.
  - **원천 시스템이 마지막으로 가져간 증분보다 오래된 레코드를 갱신하지 않아야 한다.** 오래된
    레코드의 갱신이 가능하다면 표준 증분 적재는 그 변경을 놓칠 수 있고, 그런 경우에는 CDC나
    비슷한 도구가 필요할 수 있다 — 그 도구들은 **트랜잭션 로그에서 삽입·갱신·삭제 모든 변경을
    포착하도록 설계**돼 완전한 동기화를 보장하는 데 더 믿을 만하다.
- 마지막 처리 지점을 기억하는 방법이 셋이다 (3장 §"Bronze Layer" ▸ "Processing Incremental Data
  Loads"):[^strengholt2025]
  - 스트리밍이면 Delta(또는 Iceberg) 트랜잭션 로그로 초기 위치 `startingVersion`을 지정한다. 추가
    명령 없이 멈춘 자리에서 정확히 이어 갈 수 있다.
  - 대안은 Bronze의 식별자나 `updated_at` 컬럼에 max 함수를 쓰는 것이다. `max(updated_at)`을 얻은
    뒤 그보다 큰 식별자·타임스탬프를 가진 레코드만 원천에 질의한다.
  - 처리된 레코드를 추적하는 **메타데이터 통제 표(metadata control table)** 유지도 권고된다. 특히
    복잡한 시스템에서 데이터 흐름 관리와 일관성 보장에 도움이 된다.
- 곁줄 하나가 구현 설정을 덧붙인다 — Delta Lake와 Spark로 증분 처리를 구현하고
  `trigger(AvailableNow=True)` 같은 설정을 활용하면 조직이 데이터를 더 효과적이고 경제적으로
  관리할 수 있다 (3장 §"Bronze Layer" ▸ "Processing Incremental Data Loads" 곁줄).[^strengholt2025]

## Bronze 안에서의 이력화

- Bronze는 **완전한 스냅샷이나 사본을 저장하도록 주로 설계**돼 전통적 데이터 웨어하우스의 스테이징
  환경에서 보던 것과 비슷하다. 전체 추출·덮어쓰기 방식을 쓴다면 모든 데이터 전달분의 포괄적 이력을
  유지할 수 있다는 점에서 특히 유용하다 (3장 §"Bronze Layer" ▸ "Data Historization Within the
  Bronze Layer").[^strengholt2025]
- Bronze는 대개 **여러 해에 걸쳐 데이터를 보존하는 견고한 아카이브**로도 봉사하며 이것이 감사
  목적에 결정적이다. 다만 처리가 끝나 더는 필요하지 않은 데이터를 정리해야 하는 경우가 있다 (3장
  §"Bronze Layer" ▸ "Data Historization Within the Bronze Layer").[^strengholt2025]
- 아카이빙의 실물은 형식과 폴더다 — Parquet이나 Delta 같은 효율적 저장 형식을 쓰고 폴더로 조직하면
  아카이빙이 단순해진다. **간격 파티션 테이블로 구조화하고 `YYYY/MM/DD`나 datetime 형식으로
  이름 붙은 폴더로 정렬**하면 데이터가 정돈되고 접근·감사가 단순해지며, 특정 날짜의 데이터를
  되돌아봐야 할 때 그 상태를 쉽게 재현할 수 있다 (3장 §"Bronze Layer" ▸ "Data Historization
  Within the Bronze Layer").[^strengholt2025]
  - 각주가 형식 선택의 수치를 붙인다 — **압축 알고리즘에 따라 CSV 같은 다른 형식에서 Parquet
    파일로 옮길 때 거의 75%의 크기 감소를 기대할 수 있다** (3장 각주 2).[^strengholt2025]
- **경계가 여기서 그어진다** — Bronze는 **완전히 처리된 SCD2 테이블을 표현한다는 의미의 이력화를
  위한 곳이 아니다.** Bronze의 데이터는 흔히 불변, 곧 읽기 전용으로 간주된다. 시간이 지나며
  데이터셋을 점증적으로 키우기 위해 append하거나 merge할 수는 있어도, **갱신이나 처리는 이 단계의
  통상적 실무가 아니다** (3장 §"Bronze Layer" ▸ "Data Historization Within the Bronze
  Layer").[^strengholt2025]
- 곁줄이 타임 트래블의 자리도 좁힌다 — Delta Lake의 타임 트래블 기능으로 데이터 버저닝을 적용할 수
  있지만, 그것은 **주로 데이터 복구·감사·실험이나 리포트의 재현을 위해 설계된 것이지 포괄적인
  장기 데이터 아카이빙을 위한 것이 아니다** (3장 §"Bronze Layer" ▸ "Data Historization Within the
  Bronze Layer" 곁줄).[^strengholt2025]
- 그럼에도 이력화가 결정적인 이유는 둘이다 — 감사나 디버깅에 필수적일 수 있는 **시간에 걸친 데이터
  반복분의 아카이빙**을 가능하게 하고, **재적재와 복구**를 지원한다. 후자가 저품질 데이터나 파괴적
  스키마 변경을 다루는 데 핵심이다. 이전 버전으로 되돌려 재처리할 수 있게 하기 때문이다 (3장
  §"Bronze Layer" ▸ "Data Historization Within the Bronze Layer").[^strengholt2025]

## 스키마 진화와 관리

- Bronze는 **데이터가 시스템에 들어올 때 크게 다르고 계속 바뀌는 스키마를 관리하는 데 결정적**이고,
  이 단계에서 스키마 진화를 효과적으로 다루는 것이 뒤따르는 모든 처리와 분석의 토대를 놓는다. 들어오는
  스키마 변경은 Bronze에서 다룰 수도 있고 데이터가 Silver로 옮겨 갈 때까지 기다릴 수도 있다 — 시점은
  대체로 구체적 필요와 데이터의 특성에 달렸다 (3장 §"Bronze Layer" ▸ "Schema Evolution and
  Management").[^strengholt2025]
- 저자가 마주 세우는 두 설계 선택은 이 KB가 이미 이론으로 갖는 그 둘이다 (3장 §"Bronze Layer" ▸
  "Schema Evolution and Management"):[^strengholt2025]
  - **읽기 스키마(schema-on-read)** — 데이터를 읽을 때 스키마를 동적으로 적용한다. 엄격한 스키마
    없이 저장하고 처리(읽기) 중 접근할 때에만 스키마를 추론하거나 적용한다. 유연한 접근이지만
    시스템이 반입 직후 다양한 스키마를 인식하고 적응할 것을 요구한다. 반구조·비구조 데이터나,
    CSV·Parquet 파일처럼 내장 스키마 강제가 없는 구조적 데이터에 특히 유용하다.
  - **쓰기 스키마(schema-on-write)** — 저장에 쓰면서 스키마(테이블명·컬럼명·데이터 타입·기본 키)를
    정의한다. 미리 정의해야 하고 쓰기 전부터 데이터가 그 스키마를 따라야 한다. 읽기 스키마보다
    경직됐고 처음부터 스키마 일관성을 강제하며, 적용 대상은 일반적으로 구조적 데이터다.
- Delta Lake의 기본값도 적어 둔다 — 미리 정의된 스키마가 없으면 시스템이 Delta 형식으로 변환 중인
  DataFrame의 `StructType`으로 초기 스키마를 세운다. Spark에서 `StructType`은 DataFrame의 컬럼
  구조와 타입을 정의하는 컨테이너를 가리킨다 (3장 §"Bronze Layer" ▸ "Schema Evolution and
  Management").[^strengholt2025]
- **Bronze에서는 읽기 스키마가 흔한 접근**이다 — 반입 중 스키마를 강제하지 않고 원래 형식으로
  저장한다. 미리 스키마를 정의할 것을 요구하지 않고 데이터 구조 변화를 우아하게 감당할 수 있어
  유연하다. 저자의 예는 `YYYY/MM/DD` 시간 파티션으로 일별 분할하고 날짜 이름 폴더 안에 Parquet
  파일로 두는 것이다. 읽기 스키마면 구조가 어떠해야 하는지 미리 정의하지 않고도 여러 날짜의 데이터에
  즉시 접근해 읽을 수 있다 (3장 §"Bronze Layer" ▸ "Schema Evolution and
  Management").[^strengholt2025]
- **그러나 읽기 스키마만으로는 부족하다는 것이 이 절의 요지다** (3장 §"Bronze Layer" ▸ "Schema
  Evolution and Management"):[^strengholt2025]
  - 첫째, **읽기 스키마에만 기대면 맹목적 데이터 처리(blind data processing)가 허용되지 않는다.**
    스키마 변경을 탐지하고 기록해야 하고, 실패를 처리해야 하며, Delta Lake의 타임 트래블로 데이터를
    복원해야 하고, 뒤 단계의 더 정교한 처리를 위해 스키마 관련 메타데이터를 덧붙여야 할 수 있다.
  - 둘째, **데이터 갱신 방법의 정의가 필수적**이다. 특히 이력화와 데이터 통합에 그렇다. 선택지는
    기존 데이터셋에 계속 append하거나 merge하는 것, 완전히 덮어쓰는 것, 시간 기반 파티셔닝을
    적용하는 것이다. 선택은 데이터의 성격, 쓰임새, 구체적 시스템 요구, 성능 고려에 달렸다.
    - append는 **거래 데이터**에 흔히 쓰인다. 새 거래마다 점증적으로 자라는 유형이기 때문이다.
    - overwrite는 원천의 정정이 정기적으로 들어오는 데이터셋이나 **가장 최근 스냅샷만 유효한**
      데이터셋에서 고른다.
    - 시간 기반 파티셔닝은 질의 성능을 높이고 큰 데이터셋을 효과적으로 관리하기 위해 구현할 수
      있고, 특히 데이터 접근이 시간에 민감할 때 그렇다.
- 그래서 저자의 결론은 **둘 중 하나가 아니라 계층 안에서의 순서**다 — Bronze는 흔히 읽기 스키마와
  쓰기 스키마 기법을 **결합한다.** 처음에는 랜딩이나 pre-Bronze 계층에서 읽기 스키마를 적용해 데이터
  스키마를 명시적으로 선언하지 않고 읽는다. 그다음 데이터가 **"질의 가능(queryable)"해지는 계층으로
  옮겨 갈 때 쓰기 스키마로 전환한다.** 이 결정적 계층에는 스키마 진화를 지원하는 Delta Lake 같은
  저장 형식을 고르는 것이 현명하다 — 데이터 스키마가 진화하는 대로 적응하게 해, 전체 데이터셋을
  갈아엎거나 재적재할 필요를 없애기 때문이다 (3장 §"Bronze Layer" ▸ "Schema Evolution and
  Management").[^strengholt2025]
- 마지막 의무 — 원천이 자주 바뀌는 경향이면 스키마 일관성 유지가 어려워지므로, **데이터가 이 계층에
  들어올 때 원천 시스템과 일관되게 맞는 스키마를 유지하는 것이 필수적**이다. 보통 반입 과정에서
  DDL로, 또는 Spark SQL·Databricks Auto Loader 같은 도구로 프로그램적으로 스키마를 설정한다 (3장
  §"Bronze Layer" ▸ "Schema Evolution and Management").[^strengholt2025]

## mergeSchema와 스키마 강제

- Delta Lake는 스키마 진화 처리와 스키마 강제를 포함하는 스키마 관리 기능 묶음을 제공하고, 무엇을
  적용할지는 시스템의 구체적 필요와 설계에 달렸으며 **메달리온의 모든 계층에서 볼 수 있다** (3장
  §"Bronze Layer" ▸ "MergeSchema and Schema Enforcement").[^strengholt2025]
- `mergeSchema`는 시간에 걸쳐 Delta Lake 테이블의 스키마를 관리하고 진화시키도록 설계된 기능이고,
  Spark의 쓰기 연산에 `.option("mergeSchema", "true")` 옵션을 더해 켠다. 그러면 Delta Lake가 테이블
  스키마를 네 가지 방식으로 조정한다 (3장 §"Bronze Layer" ▸ "MergeSchema and Schema
  Enforcement"):[^strengholt2025]
  - 원천 DataFrame에는 있고 Delta 테이블에는 없는 컬럼이면 Delta가 새 컬럼을 더한다. **기존 행은
    전부 이 새 컬럼에 null 값을 갖는다.**
  - Delta 테이블에는 있고 원천 DataFrame에는 없는 컬럼이면 그대로 둔다. **새 레코드가 그 빠진
    컬럼에 null 값을 갖는다.**
  - `NullType` 컬럼을 더하면 그 컬럼의 기존 행이 전부 null이 된다.
  - 이름은 같고 데이터 타입이 다른 컬럼이 있으면 Delta Lake가 새 타입으로의 변환을 시도하고,
    **변환에 실패하면 오류를 던진다.**
    - 각주가 그 변환의 한계를 못 박는다 — **TypeWidening은 같은 타입 범주 안의 변경을 허용하지만
      한 타입 범주에서 다른 범주로의 변경(string을 bool로 바꾸는 것 같은)은 허용하지 않는다.
      그런 변경을 하려면 테이블 전체 덮어쓰기를 수행하고 `overwriteSchema: true`를 설정해야
      한다** (3장 각주 4).[^strengholt2025]
- 오류나 실패의 경우 **Delta Lake의 테이블 이력으로 이전 버전으로 테이블을 롤백**할 수 있고, 이
  되돌리기가 스키마 진화 문제로부터의 복구를 가능하게 한다. 되돌린 뒤 적절한 스키마로 정정된
  데이터를 재처리한다 (3장 §"Bronze Layer" ▸ "MergeSchema and Schema
  Enforcement").[^strengholt2025]
- 더 엄격하게 다루려면 **Delta 제약(Delta constraints) 기능**을 쓴다. 이것은 쓰기 스키마 접근과
  밀접하게 맞춰져 있고, Delta 테이블에 쓰이는 데이터가 테이블 스키마와 **엄격히 일치하도록 보장하며
  부합하지 않는 쓰기를 거부한다.** 데이터가 시스템에 들어올 때 Delta Lake가 미리 정의된 스키마의
  준수를 검증하고 어떤 이탈도 오류가 된다. 다만 이 접근은 **원천 시스템 스키마의 지속적이고 파괴적인
  변경을 다루기 어렵게 만들 수 있다** (3장 §"Bronze Layer" ▸ "MergeSchema and Schema
  Enforcement").[^strengholt2025]
- `mergeSchema`로 다룰 수 없는, 호환성에 영향을 주는 변경을 만나면 스키마를 화해시켜야 한다. Delta
  테이블의 스키마를 조정하는 선택지가 넷이다 (3장 §"Bronze Layer" ▸ "MergeSchema and Schema
  Enforcement"):[^strengholt2025]
  - **SQL `ALTER COLUMN` 문** — 직접 변경이라 원천 시스템 소유자와 데이터 플랫폼 관리자 사이의
    세심한 조율을 요구한다. 그 연산이나 스크립트를 저장소에 체크인하는 것이 효과적인 관리법 하나다.
    **매우 정밀하지만 노동 집약적이고 요구되는 복잡한 조율 때문에 오류가 나기 쉽다.**
  - **자동화된 스키마 진화** — 원천의 스키마 변경을 탐지해 필요한 ALTER 문을 자동으로 생성·적용하는
    도구나 스크립트를 구현한다.
  - **메타데이터 주도 프레임워크(저자가 권고하는 접근)** — 원본과 새 대상 스키마를 유지할 뿐 아니라
    변경을 체계적으로 관리하는 견고한 방법을 준다. **스키마 사이의 매핑을 유지함으로써 복잡한 변환과
    스키마 진화를 대규모 수작업 개입 없이 감당할 수 있는 확장 가능한 방법**을 만들고, 메타데이터
    저장소가 항상 최신이며 쓰이는 스키마를 정확히 반영하게 한다. CI/CD 파이프라인과 통합해 갱신과
    배포를 자동화하는 것이 도움이 될 수 있다.
  - **파괴적 변경의 제한** — 원천 시스템 팀에 파괴적 변경을 하지 말 것을 요구하고 하위 호환 변경만
    허용하는 것이다. 원천 쪽에 제약을 가하지만 **스키마 갱신의 복잡도와 빈도를 크게 줄일 수 있다.**
- 이전 버전과 화해할 수 없는 아주 파괴적인 원천 스키마 변경이면 **데이터 파이프라인의 새 버전을 만드는
  것**을 고려할 수 있다. 새 데이터가 새 대상 위치에 착지하므로 큰 스키마 변경을 더 효과적으로
  관리하게 되고, **여러 스키마 버전을 동시에 유지하면서 애플리케이션이나 프로세스가 어느 버전과
  상호작용할지 지정할 수 있다** (3장 §"Bronze Layer" ▸ "MergeSchema and Schema
  Enforcement").[^strengholt2025]

## 기술 검증 검사

- 왜 이 계층인가 — 레이크하우스 아키텍처 안에서 Bronze는 원시의, 대개 비구조인 데이터의 최초
  저장소로 작동하고, 데이터가 원래 형식으로 저장되므로 **불일치나 오류를 포함할 수 있다.** 무결성·
  정확성·완전성·일관성 문제는 조직에 중대한 운영적·전략적 영향을 줄 수 있다 (3장 §"Bronze Layer" ▸
  "Technical Validation Checks").[^strengholt2025]
- 형식·스키마·완전성 검사를 이 단계에서 구현하는 이유가 셋이다 (3장 §"Bronze Layer" ▸ "Technical
  Validation Checks"):[^strengholt2025]
  - 데이터가 지정된 표준에 부합하게 해 데이터셋 전반의 일관성을 유지한다. **여러 원천의 데이터가
    안정된 구조를 따르지 않을 수 있으므로 특히 중요하다.**
  - 조기 검증이 무결성 문제의 식별과 해결을 돕는다. **특히 쓰기 스키마 접근을 적용할 때 유용하다.**
  - 시작 시점에 오류를 잡아 **부정확함이 Silver·Gold로 전파되는 것을 막는다.**
- Bronze의 설계가 강한 데이터 검증 통제를 중심에 두는 이유는 그것이 **기술 검증과 관측 가능성의
  1차 방패(primary shield)**로 작동하기 때문이다. 검사를 한 번에 몰아서 할 수도, 구간으로 쪼갤 수도,
  Silver로 전송하는 중에 통합할 수도 있다. 많은 회사가 스크립트를 쓰고 메타데이터 저장소를 유지하는데,
  그 저장소가 원천의 기술 스키마 상세를 담아 **검증 규칙을 선언적으로도 동적으로도 자동 강제**하게
  한다 (3장 §"Bronze Layer" ▸ "Technical Validation Checks").[^strengholt2025]
- **설계를 가르는 축은 무결성 문제에 대한 내성이고, 저자는 두 정책에 이름을 준다** (3장 §"Bronze
  Layer" ▸ "Technical Validation Checks"):[^strengholt2025]
  - **침습적 데이터 무결성 처리(intrusive data integrity processing)** — 하류 프로세스의 실패를
    예상했거나 데이터 소비자가 그 문제를 감당할 수 없으면 **파이프라인을 멈춘다.** 검증된 데이터와
    잘못된 데이터를 별도 폴더나 테이블에 저장하므로 문제를 쉽게 식별·정정할 수 있고, **그 데이터셋이
    실제 Bronze 계층에 들어가지 않게 한다.**
  - **비침습적 데이터 품질 처리(nonintrusive data quality processing)** — 무결성이나 완전성 문제를
    감당할 수 있으면 데이터 처리를 계속하기로 고를 수 있다. 이 경우 **검증된 데이터와 잘못된 데이터가
    둘 다 대상 Bronze 폴더나 테이블에 곧장 저장된다.** 처리를 진행할 수 있지만 **나중에 다른 계층
    (보통 Silver)에서 그 문제를 해결해야 할 수 있다**는 것을 유념해야 한다.
- 검사 대부분은 원천의 기술적 측면을 검증해, 사전 정의된 표준 집합을 만족하지 않는 한 데이터가 다음
  구역으로 나아가지 못하게 막는다. 다음 구역의 표준을 만족하지 않으면 **데이터 소유자가 애플리케이션
  팀·데이터 엔지니어와 긴밀히 협력해 바로잡을 책임**을 진다. 데이터를 관리하고 공급하는 이들이 레이크
  하우스의 소비자·사용자가 규정한 무결성 요구를 데이터가 충족하게 해야 한다 (3장 §"Bronze Layer" ▸
  "Technical Validation Checks").[^strengholt2025]
- 이 계층이 **원시 데이터의 저장소일 뿐 아니라 무결성과 정확성의 결정적 검문소(critical
  checkpoint)**가 되는 셈이고, 사전 정의된 품질 표준을 만족하는 데이터만 레이크하우스 안쪽으로
  나아가게 한다 (3장 §"Bronze Layer" ▸ "Technical Validation Checks").[^strengholt2025]
- 도구의 선택지 넷 (3장 §"Bronze Layer" ▸ "Technical Validation Checks"):[^strengholt2025]
  - **Delta Lake의 스키마 검증 기능** — 스키마 강제가 개발자로 하여금 사전 정의된 표준을 지키게 해
    테이블을 깨끗이 유지한다. 테이블에 데이터가 쓰일 때 Delta Lake가 데이터 스키마와 테이블 스키마가
    맞는지 검증하고, **호환되면 통과해 쓰기가 성공하며, 비호환이면 Delta Lake가 트랜잭션을 취소해
    어떤 데이터도 쓰이지 않게 한다.**
  - **데이터 품질 프레임워크나 도구** — Delta Live Tables, Great Expectations, dbt, Ataccama,
    Monte Carlo Data. 도구 사이의 차이는 6장이 받는다.
  - **커스텀 솔루션** — 스크립트·코드·스키마 메타데이터로 무결성을 검증한다. 기존 도구나 프레임워크가
    충족하지 못하는 구체적 요구가 조직에 있을 때 흔히 쓰인다.
  - **Azure Data Factory의 스키마 드리프트 탐지** — 상류 원천의 변화에 덜 취약하게 만든다.

## 사용과 거버넌스

- **업무 사용자에게 Bronze를 열 것인가**에 저자의 답은 부정적이다. 일부 실무자는 업무 사용자가
  Bronze 데이터에 질의하거나 임시 분석을 하는 것이 이롭다고 주장한다. 그러나 원시 데이터는 **원천
  시스템의 설계와 거기 박힌 복잡한 업무 로직에 대한 깊은 이해를 요구**하므로 상당한 도전을 제기한다.
  작은 테이블이 많은 경우가 잦아 사용성을 복잡하게 하고, **원래 원천 시스템에 강하게 결합돼 있어
  원천이 바뀔 때 특히 큰 문제**가 된다. 이 복잡성들이 업무 분석을 위한 Bronze 데이터의 직접 사용을
  흔히 단념시킨다 (3장 §"Bronze Layer" ▸ "Usage and Governance").[^strengholt2025]
- 거버넌스의 의무 (3장 §"Bronze Layer" ▸ "Usage and Governance"):[^strengholt2025]
  - **엄격한 접근 통제**를 구현해 무단 접근·조작·삭제를 막는다.
  - Bronze 데이터는 불변이라 원래 상태에서 변경되지 않은 채 남지만, **지나치게 기술적인 데이터를
    다룰 때 예외가 존재한다.** 이 불변성이 **반입 시각·원천·모든 시스템 상호작용을 기록하는 상세
    로그의 유지**를 요구해 정확한 추적 가능성을 가능하게 한다.
  - **데이터 크기·형식·도착 시각의 이상을 감시하는 경보**를 세워 데이터 파이프라인의 무결성을
    유지하는 것이 결정적이다.
  - **사고 대응 계획(incident response plan)의 개발과 정기 갱신**이 잘못된 데이터 전달과 관련된
    문제를 효과적으로 다루는 데 필수적이다.
  - 변경의 철저한 문서화와 명확한 참조 카탈로그 유지 같은 모범 사례도 권고된다.
- 절의 요지 — Bronze는 메달리온의 **기초 스테이징 영역**으로 봉사한다. 다양한 원천에서 원시 데이터를
  모아 검증하고 Parquet이나 Delta 같은 선호 형식으로 변환해 처리한다. 이 계층의 데이터는 통상 불변이나
  **예외가 있다** — 특히 메타데이터로 데이터를 보강하거나 민감 정보를 효과적으로 관리하기 위해 필터와
  변환을 적용하는 경우다. 곧 이 계층의 데이터는 **완전히 원시일 수도 있고 약간 증강됐을 수도 있다**
  (3장 §"Bronze Layer" ▸ "Usage and Governance").[^strengholt2025]

## 실무에서의 Bronze

- Bronze는 **가장 진정한 형태(most authentic form)의 원시 데이터를 포착·저장하는 기초**다. 모든 원천
  데이터를 변경되지 않은 상태로 안정적으로 반입·보존하는 기반 입력 계층으로 기능해 데이터 손실과
  훼손을 막고, 재적재와 추가 처리의 신뢰할 만한 기반이 된다 (3장 §"Bronze Layer" ▸ "The Bronze
  Layer in Practice").[^strengholt2025]
- **경직된 것으로 보아서는 안 된다**는 것이 이 절의 판정이다. 조직의 구체적 필요에 맞춰 재단해야
  하고, 그것이 **추가 랜딩 영역, 증분 데이터 전달을 다루는 전처리 계층, 데이터 검증 파킹 존
  (data validation parking zone)**을 더하는 것으로 나타날 수 있다. 또는 Bronze의 (일부를)
  **가상 계층(virtual layer)**으로 다뤄 데이터를 물리적으로 저장하지 않고 **원천 시스템의 논리적
  표현으로 대신할 수도 있다** (3장 §"Bronze Layer" ▸ "The Bronze Layer in
  Practice").[^strengholt2025]
- 그 실물이 그림 3-2이고, **본문에 없는 내부 구획이 그림에만 있다** (3장 §"Bronze Layer" ▸ "The
  Bronze Layer in Practice", 그림 3-2):[^strengholt2025]
  - Bronze 계층 상자 안이 원천별로 세 줄이고, 각 줄이 **두 칸으로 갈린다** — 왼쪽이
    `Raw export (CSV)`·`Raw export (Parquet)`·`Raw export (JSON)`이고 오른쪽이 전부
    `Validated Delta tables`다. 곧 그림은 "원시 내보내기"와 "검증된 Delta 테이블"을 **Bronze 안의
    두 하위 칸**으로 그린다.
  - 왼쪽 랜딩 존은 CSV·Parquet 줄이 `Blob file store`를, JSON 줄이 `Kafka`를 거친다.
- 한계와 이행의 근거 — Bronze가 데이터 무결성과 이력 정확성에 없어서는 안 되지만 **데이터의 원시성이
  분석 목적의 직접 적용 가능성을 제한한다.** 이 상태의 데이터는 흔히 불일치·중복·이상을 포함해
  다루지 않으면 통찰을 왜곡할 수 있다. 게다가 **Bronze는 원천 시스템과 강하게 결합돼 위험과 의존을
  들인다.** 그래서 Silver로의 이행이 필수적이 된다 (3장 §"Bronze Layer" ▸ "The Bronze Layer in
  Practice").[^strengholt2025]

## 이 KB의 원전과 맞대어 본 것

이 계층의 소재는 이 KB에 이미 이름을 가진 것이 많다. 갈리는 자리만 적는다.

- **적재 패턴.** [배치 반입 패턴](../concepts/batch-ingestion-patterns.md)이 Full Loader·Incremental
  Loader를 **반입 잡의 구현**(델타 컬럼이냐 시간 분할이냐, 백필에서의 퇴화, 하드 삭제)으로 서술한다면,
  이 소스는 같은 둘을 **계층 안에서 무엇이 누적되고 어디서 형식이 바뀌는가**로 서술한다. 층위가 달라
  겹치지 않는다. 다만 이 소스가 증분의 전제로 못 박는 "원천이 오래된 레코드를 갱신하지 않아야 한다"는
  그 페이지의 늦은 데이터·하드 삭제 함정과 **같은 자리를 다른 말로 짚는다** — 그쪽은 반입 잡이 레코드를
  놓치는 기제를 말하고 이쪽은 그때 CDC로 갈아타라는 처방을 말한다.
- **CDC의 자리.** [변경 데이터 캡처](../concepts/change-data-capture.md)가 CDC를 리더-팔로워 기제로
  규정한다면, 이 소스에서 CDC는 **증분 적재가 성립하지 않는 조건에서의 탈출구**다. 저자 자신이 상세를
  5장으로 미뤄 두었다.
- **읽기 스키마와 쓰기 스키마.** [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md)는
  둘을 **강제 시점의 선택**으로 다룬다. 이 소스가 더하는 것은 **한 계층 안에서 둘을 잇달아 쓰는 배치**다
  — 랜딩에서 읽기 스키마, 질의 가능해지는 자리에서 쓰기 스키마.
- **원시 층의 불변.** [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)가
  세우는 불변 원시 층 원칙과 부딪히지 않는다. 이 소스도 불변을 규정하되 **예외 둘**(메타데이터 보강,
  민감 정보 필터·변환)을 명시하고, "완전히 원시일 수도 약간 증강됐을 수도 있다"고 폭을 남긴다.
- **품질 검사의 정책.** [데이터 품질 강제 패턴](../concepts/data-quality-enforcement-patterns.md)이
  감사 단계의 결말을 실패·데이터 디스패칭·비차단 감사 셋으로 나눈다면, 이 소스는 **침습·비침습 둘**로
  나누고 **가르는 기준을 하류 소비자의 내성**에 둔다. 어휘가 다르고 분류 축이 다르지만 서로를 부정하지
  않는다.
- **제약으로의 위임.** [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md)이
  검증을 저장소에 위임하는 선택의 대가를 다룬다면, 이 소스의 Delta 제약 서술은 같은 위임을 **스키마
  강제**로 좁혀 적고 그 대가를 "파괴적 원천 변경을 다루기 어려워진다"로 적는다.
- **반입 단계 전체.** [수명 주기의 반입 단계](../concepts/ingestion-in-the-lifecycle.md)가 배치와
  스트리밍의 선택 축을 여덟으로 세운다면, 이 소스는 그 선택이 끝난 뒤 **Bronze 계층 안에서** 무엇이
  남는지를 받는다.

이 런은 이 페이지에 `contradicts`를 걸지 않는다. 위 자리들은 전부 층위가 다르거나 어휘가 다를 뿐,
최대 하나만 참일 수 있는 사실 충돌이 아니다.

## 이어지는 페이지

- [메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md) — Bronze·Silver·
  Gold 셋의 정의와 계보
- [메달리온 계층 이전의 결정과 Delta 테이블 관리](../concepts/medallion-groundwork-and-delta-table-management.md)
  — 랜딩 존과 "원시"의 경계, 배치와 실시간의 선택
- [메달리온 Silver 계층](../concepts/medallion-silver-layer.md) — 이 계층이 넘기는 다음 자리
- [메달리온 Gold 계층](../concepts/medallion-gold-layer.md) — 계층 셋의 마지막과 3장의 맺음
- [배치 반입 패턴](../concepts/batch-ingestion-patterns.md) — Full Loader·Incremental Loader의 원전
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 증분 적재가 감당 못 할 때의 기제
- [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md) — 이 절의 두 어휘가
  사는 자리
- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 스키마 진화가
  지키려는 두 방향
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 불변 원시 층의 원칙
- [데이터 품질 강제 패턴](../concepts/data-quality-enforcement-patterns.md) — 검증을 어디에 세우는가
- [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md) — 검증을 저장소에
  위임하는 쪽
- [데이터 품질 관리](../concepts/data-quality-management.md) — 품질을 조직의 일로 보는 쪽
- [수명 주기의 반입 단계](../concepts/ingestion-in-the-lifecycle.md) — 배치와 스트리밍의 선택 축
- [스테이징 영역](../concepts/staging-area.md) — 랜딩 존이 웨어하우스 쪽에서 불리던 이름
- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — Bronze가 감당하지 않는다고
  저자가 지목한 이력화 방식
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 이 페이지가 걸리는 허브

[^strengholt2025]: Piethein Strengholt, *Building Medallion Architectures: Designing with Delta
    Lake and Spark*, O'Reilly 2025 ([소스](../sources/strengholt2025.md)). 스냅샷이 EPUB이고
    **인쇄판 쪽 앵커가 없어** locator는 장·절 단위다 — `N장 §"절 제목"`(원문 절 제목 그대로),
    소절은 `▸`로 잇고 곁글·곁줄은 제목 뒤에 각각 `곁글`·`곁줄`을 붙인다. 3장 실측: 절(`sect1`)
    다섯(The Three-Layered Design · Bronze Layer · Silver Layer · Gold Layer · Conclusion) ·
    소절(`sect2`) 스물셋 · 소소절(`sect3`) 일곱 · 곁글 하나 · 곁줄 아홉(note 다섯 · tip 셋 ·
    warning 하나) · 표 하나 · 도판 다섯(그림 3-1~3-5) · 코드 목록 넷(python 하나 · sql 둘 ·
    json 하나) · 각주 여덟(`data-type="noteref"` 마커 기준). **코드는 펜스 없이 인라인으로
    옮겼고** 원문에 없는 줄은 보태지 않았다. **도판의 라벨은 이미지에만 있어**(`alt`가 비어 있다)
    `OEBPS/assets/`의 PNG를 직접 읽어 옮겼다.

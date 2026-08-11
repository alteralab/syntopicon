---
type: webpage
title: "dbt Documentation: Materializations, Incremental Models, Snapshots"
author:
  - { literal: "dbt Labs" }
issued: "2026"
URL: "https://docs.getdbt.com/docs/build/materializations"
snapshot: /it/archive/dbtlabs2026-materialization/
snapshot_sha256: "71e613ed57936c2c6d885a987d55fc521e50ef4ff344f1b1959999e80bca317f"
accessed: "2026-08-11"
---

# dbt 문서 — materialization 축

**이 KB의 첫 기술 문서 소스**이고, 도서·논문·기술 문서 3타입 중 마지막을 여는
자리다(§6). 동시에 **docs-mirror → core 승격 경로의 첫 실전**이다 — 레이어 간
유일하게 허용된 지식 이동이 여기서 처음 돈다.

## 승격 규약 (docs-mirror PLAN §6 — 도서·논문과 다른 제약)

- **불변 가치가 있는 통찰만 올라온다**: 설계 원리·트레이드오프·버전 관통 패턴.
  릴리스 노트 나열과 현행 API 사용법은 **승격 금지** — 그것이 미러의 존재 이유다.
- **claim에 버전 조건 명시**가 필수다(예: "dbt 1.9부터 …").
- **소스 귀속은 미러 경로가 아니라 upstream 정식 인용**이다. core → docs-mirror 참조는
  원칙 6이 금지한다(정본이 소모품을 가리키면 소모품이 아니게 된다).
- **스냅샷은 미러가 대신하지 않는다** — 위 `snapshot`은 kb-ingest가 뜬 독립 사본이다.
  미러는 지워질 수 있는 캐시이므로 승격된 지식의 근거는 core 안에 있어야 한다.

## 이 소스의 판본

미러 커밋 `51783f5dab`(2026-08-07) 시점의 `website/docs/docs/build/` 5개 파일:
`materializations.md`, `incremental-models-overview.md`, `incremental-models.md`,
`incremental-strategy.md`, `snapshots.md`. locator는 **문서 파일명 + 절 제목**을 쓴다
(웹 문서라 쪽수가 없고, 절 제목은 upstream URL의 앵커와 대응한다).

이 문서는 계속 갱신되므로 `issued`는 스냅샷 연도이고, 실제 기준점은 `accessed`와
위 미러 커밋이다.

## 이 소스가 닿을 자리

- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — dbt snapshots가
  SCD 타입 2의 구현이다. **킴벌의 이론과 도구의 구현이 만나는 자리**
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 변환을 적재 전에 두느냐 후에 두느냐
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — materialization은
  파생 데이터를 언제 다시 계산하고 언제 저장하느냐의 스펙트럼이다
- [데이터 레이크](../concepts/data-lake.md) — 스시 원칙과의 대비

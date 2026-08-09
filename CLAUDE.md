# syntopicon (모노레포)

개인 지식 시스템 전체. **단일 git 저장소**(`alteralab/syntopicon` private) — 시스템 구성의 정본 = 이 저장소의 `PLAN.md`(레이어 경계·배치 규약·판정 원장 r1–r12·재심 트리거). 리서치 전문은 `research/`.

| 디렉토리 | 정체 | 작업 시 정본 |
|---|---|---|
| `core/` | 정본 KB (md+git=SoT, restic 대상) | `core/CLAUDE.md` + `core/PLAN.md` |
| `docs-mirror/` | 벤더 문서 미러 캐시 (`mirrors/`는 ignore — upstream 생존 시 재생성) | `docs-mirror/PLAN.md` |

규칙 요지: 레이어 내부 작업은 해당 디렉토리의 CLAUDE.md·PLAN을 따른다. **커밋 = `<레이어>/<영역>: 요지`** (예: `core/tools:`, `mirror/plan:`; 우산은 `plan:`·`research:`), 한 커밋 = 한 레이어, 게이트는 hooksPath(`core/tools/githooks`). 루트에 종류별 디렉토리(tools/·skills/) 신설 금지 — 글루는 자기 레이어 안(r4·r12). 새 구성 요소의 행선지는 PLAN §2 배치 표로 판정.

지식 조회·저장 = `/kb-query`, 소스 반입 = `/kb-ingest`, 점검 = `/kb-lint`, 벤더 문서 = `/docs-query` (전역 스킬 — 정본은 각 레이어 `.agents/skills`).

# syntopicon (우산)

개인 지식 시스템의 우산 디렉토리. **시스템 구성의 정본 = 이 저장소의 `PLAN.md`** (레이어 경계·배치 규약·판정 원장 r1–r11·재심 트리거). 리서치 전문은 `research/`.

| 디렉토리 | 정체 | 작업 시 정본 |
|---|---|---|
| `core/` | 정본 KB (md+git=SoT, restic 대상) — **독립 git 저장소** | `core/CLAUDE.md` + `core/PLAN.md` |
| `docs-mirror/` | 벤더 문서 미러 캐시 (재생성 가능, 무백업) — **독립 git 저장소** | `docs-mirror/PLAN.md` |

규칙 요지: 레이어 내부 작업은 해당 디렉토리로 들어가 그곳의 CLAUDE.md·PLAN을 따른다(각자 커밋 규약·게이트 보유). 우산 저장소는 PLAN.md·research/·CLAUDE.md·(미래) 크로스 레이어 스킬만 추적 — 도구·콘텐츠 추가 금지, 새 구성 요소의 행선지는 PLAN §2 배치 표로 판정. 구조 변경은 §3 원장에 근거 없이 금지.

지식 조회·저장 = `/kb-query`, 소스 반입 = `/kb-ingest`, 점검 = `/kb-lint` (전역 스킬 — 정본은 core/.agents/skills).

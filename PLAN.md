# syntopicon 시스템 계획

개인 지식 시스템 전체의 구성 정본. 2026-08-08 초판(같은 날 정리판) — 딥 리서치 11회(98 에이전트, 적대 검증 포함)로 확정. 근거 전문은 `research/`, 요약은 §3 원장.

**이 문서의 관할**: 레이어 구성·레이어 간 경계·시스템 공통 규약·재심 트리거. **각 레이어의 내부는 각자의 PLAN이 정본**이며 이 문서는 그것을 복제하지 않는다.

```
syntopicon/                  # 단일 git 저장소 (모노레포 — r12) = alteralab/syntopicon (private)
  PLAN.md                    # 이 문서 — 시스템 구성의 정본
  research/                  # 구조 결정의 리서치 산출물 아카이브 (r1–r12)
  core/                      # [레이어 디렉토리] 정본 KB — md+git=SoT, 자기 글루(schema·tools·skills·evals) 동거
  docs-mirror/               # [레이어 디렉토리] 외부 문서 미러 캐시 — 글루만 추적, mirrors/ 는 ignore(재생성 캐시)
```

레이어 경계는 저장소가 아니라 **이 PLAN의 계약**이 담당한다(r12 — 저장소 분리는 계약의 물리적 중복 표현이었다). 각 레이어의 내부 규약은 그 디렉토리의 CLAUDE.md·PLAN이 정본.

## 1. 레이어 구성

| 레이어 | 정체 | 정본 계획 | 백업 | git 이력의 의미 |
|---|---|---|---|---|
| **core** | 지식의 source of record — 사람·LLM이 저작한 md, 대체 불가 | `core/PLAN.md` | git 3계층 + restic(archive/) | 지식의 tx-time·이벤트 저널(Ingest 트레일러) |
| **docs-mirror** | 외부 벤더 문서의 로컬 캐시 — 전량 재생성 가능 | `docs-mirror/PLAN.md` | 글루만 git 원격, mirrors/ 는 무백업 | 글루 변경 이력만 |

- **레이어 간 관계는 계약 2개가 전부다**: ⑴ 지식 이동은 승격 단방향(docs-mirror → core, kb-ingest 경유 — docs-mirror PLAN §6) ⑵ core → docs-mirror 참조 금지(docs-mirror PLAN §5). 두 레이어 사이에 원자 커밋을 요하는 변경은 존재하지 않는다(실측 0건 — r6). 이 성질은 모노레포(r12)에서도 규범으로 유지된다 — **한 커밋은 한 레이어만 만진다**(루트 PLAN·research 커밋은 예외).
- **새 레이어 추가**는 core의 kb-new 게이트 3문(기밀·백업 정책·스키마 분기)을 준용해 심사하고, 통과 시 레이어 디렉토리로 추가한 뒤 이 표를 갱신한다.

## 2. 시스템 공통 규약 (레이어 배치 원리)

7회 리서치로 검증된 배치 원리 — 신규 구성 요소는 이 표로 행선지를 정한다:

| 대상 | 행선지 | 원리 (근거 라운드) |
|---|---|---|
| 사람·LLM이 저작·리뷰하는 소형 텍스트 | 해당 레이어의 git 안 | 데이터 엔지니어링 자신의 경계 — dbt seeds·Terraform 대비 (r7) |
| 대용량·바이너리·기계 생성물 (스냅샷·미러·모델) | git 밖 (restic 또는 재생성 캐시) | 데이터가 git 밖에 사는 5속성 (r7) |
| 파생 인덱스 (SQLite·qmd·임베딩) | git 밖 소모품 — lakehouse의 파생 질의 계층 | 정본에서 전량 재생성 (r7·core 원칙 4) |
| 스키마 결합 글루 (tools·skills·evals) | **그 데이터의 레이어 안** — 동거 | 응집도·co-change 56% 실측·Iceberg 메타데이터 배치 (r4·r5) |
| 공유 가능한 범용 엔진 (qmd·ir_measures·Airflow[도입 예정 — 다중 크롤·배치의 공유 오케스트레이터, 2026-08-08 사용자 결정]) | 저장소 밖 외부 설치·버전 핀. 오케스트레이터의 DAG는 얇은 호출자만 — 로직은 각 레이어 글루 잔류 | 글루 동거·엔진 외부 — Chromium depot_tools 동형 (r4) |
| 스킬의 호출 표면 | `~/.claude/skills/` 심링크 = 단일 catalog | 정본은 레이어별 분산, 표면은 통합 — Iceberg catalog 동형 (r5) |
| 두 레이어를 함께 다루는 오케스트레이션 스킬 (미래) | 저장소 루트 `.claude/skills/` | nested skills 공식 지원 (r4·r5) |

- **이력 조회 규약**: 지식 이력 = `git -C core log --oneline -- it/` 또는 `git -C core log --grep Ingest-Run`(이벤트 저널). 도구 이력 = `git -C core log --oneline -- tools/ schema/`. 이력 혼재는 저장 문제가 아니라 뷰 문제다 (r6·co-change 실측).

## 3. 확정 판정 원장 (2026-08-08)

| # | 심사 | 판정 | 결정 근거 요지 | 전문 |
|---|---|---|---|---|
| r1 | 휘발성 문서 레이어 분리·수집 방식·llms.txt 비교 | 분리 채택, 수집=git 미러, llms.txt=폴백 | kb-new 게이트·DDIA SoR/derived·dbt 월 200+커밋·llms-full 통독 불가(dbt 10.5MB) | research/r1 |
| r2 | 색인 도구 전수 (GraphRAG·RAG 플랫폼·문서 색인기·검색엔진·무색인) | 무색인 시작, 게이트 후 docs-mcp-server(버전)/qmd(의미) | Claude Code의 RAG→grep 교체·Amazon 91.5% attainment·규모 경계 2자릿수 마진 | research/r2 |
| r3 | 버전별 코드 미러·이슈 전량 미러 | 코드=보류(근거 동결)·이슈=기각(온디맨드) | GitHub 코드 검색 default branch 한정 / 이슈 버전 축 부재·API 캡·JIRA 이원화 | research/r3 |
| r4 | 도구(tools·skills·evals)의 동급 분리 | 기각 — 각 레이어가 자기 글루 소유 | logical cohesion 하위 등급·6개 생태계 동거 관행·분리 시 파손 8건 | research/r4 |
| r5 | 컴퓨팅-스토리지 분리 유비·스킬 분산의 사용성 | 현행 구조가 유비의 올바른 구현 | 교훈="데이터를 엔진에 가두지 마라"·스키마 결합물은 데이터 곁·통합=catalog | research/r5 |
| r6 | 부모-서브모듈 형식화·모노레포 통합·GitLake | 기각 — 계약 경계 너머 독립 2-저장소 유지 | 예시 OSS는 전부 단일 저장소 멀티모듈·Hadoop 재통합 교훈·크로스 원자성 0건·GitLake=git 없는 세계용 | research/r6 |
| r7 | 지식 정본 기질 (git 파일 vs S3/DB) | **core 원칙 1 유지** — 기각 | 5속성 공유 0개·20년 상한=MDN 현 운영 규모·git 붕괴선 대비 2~3자릿수·DB화 파손 8계층·경계 기구현 실측(git 안 저작 텍스트 424KB) | research/r7 |
| r8·r9 | 미러 중앙 저장소·보존 계층 | 상시 중앙 미러 기각 → **4겹 보존 계층 채택**(docs-mirror §3.5) | 크기 실측 5.25GB·캐시 무이주 관행·GitHub fork 생존 공식 보장·Deep Archive $0.00099/GB-월 | research/r8·r9 |
| r12 | 모노레포 재편 (r6 역전, 2026-08-09) | **단일 저장소 통합 채택** — 레이어=디렉토리, 경계=PLAN 계약 | 분리 정당 3축(신뢰 경계·소비자·독립 배포 — r4 서열) 전부 미적용(1인·단독 org)·원자 수요 0은 양방향 무해·다중 repo 실사고 1건(우산↔core 원격 오push)·운영자 체감 마찰=1인 시스템의 유지비. 반대근거 소거: 이력 혼재는 뷰 문제(§2 이력 조회 규약 기존재), 미래 글루 공개 분리는 filter-repo로 가역. 글루의 레이어 동거(r4)는 모노레포에서도 유지 — 루트 종류별 디렉토리는 logical cohesion 재발 | 본 원장 |
| r10·r11 | 카탈로그 레이어·CRUD REST API | 서비스 기각 → **3요소 패턴 채택**(선언 파일+JSON Schema+CLI 동사) + pre-commit 실설치 | Polaris 전제(멀티엔진·동시 writer CAS) 부재·Backstage도 YAML in git이 정본·로컬 REST 선례는 전부 비파일 클라이언트용 파사드·집행점은 커밋 게이트가 표준 | research/r10·r11 |

공통 패턴: 제기된 유비들(Iceberg·역할 분리·모듈화·lakehouse)은 원리로서 옳았고, 판정은 매번 "그 원리가 이미 올바른 형태로 구현돼 있다"였다. core PLAN의 2026-08-04 "데이터 플랫폼 이식 감사"(§8 원장)가 같은 방향을 선행 심사했음도 확인됨 (r7).

## 4. 재심 트리거 (조건 성립 시에만 해당 판정을 다시 연다)

| 트리거 | 재심 대상 |
|---|---|
| 다수 동시 저자 발생 / 웹 UI가 유일한 편집 수단 / 코퍼스가 MDN×10(~30만 파일·~5GB 텍스트) 접근 | r7 — 정본 기질 |
| 한 도구를 두 레이어가 실제 import(두 번째 소비자) / co-change 없는 단독 도구 커밋의 지속 우세 | r4 — 도구 분리 (형태는 핀 가능한 패키지 추출) |
| 버전 고정 코드 분석 수요의 반복 실측 | r3 — 코드 미러 보류 해제 (규약은 docs-mirror PLAN §7에 동결) |
| rg 루프 miss·버전 병존 조회의 실사용 pain (qrels A/B) | docs-mirror §4 — 색인 게이트 |
| qmd 6개월 무활동 / sqlite-vec 사망 / docs-mcp-server open-core화 | 검색 승계 경로 (Meilisearch/LanceDB — r2) |
| 글루(tools·스킬)를 오픈소스 공개하되 콘텐츠는 사설로 남길 필요 발생 | r12 — 모노레포 (filter-repo로 글루 서브트리 분리 — SWE at Google의 유일 정당 분리 사유) |
| 멀티 에이전트 동시 ingest 도입 | git branch/worktree 격리 설계 (GitLake 패턴의 네이티브 구현 — r6) |
| 비파일 클라이언트 등장(모바일·웹 KB 접근) / git 비경유 쓰기 경로 / 멀티유저 | r10·r11 — REST 파사드 재심 (그때도 파일 정본 유지 파사드형 — Obsidian Local REST API 모델, 메타스토어 정본화는 dual-write 금지) |

## 5. 실행 로드맵

**완료**: 우산 이관·외부 참조 갱신(2026-08-08) · docs-mirror 구축 완주 + 보존 0겹(2026-08-08~09) · restic 대조 심사·NAS 백업 3계층 일간 가동·비밀 계층(gopass+vaultwarden)·배포 파이프라인(2026-08-09) · 정비 6종(스킬 cwd 독립화·CLAUDE 현행화·docs-mirror 레그·심링크 lint·pre-commit 실설치·runner 경로) · **모노레포 재편(r12, 2026-08-09)**.

**재개**: core 수용 검증(core PLAN §6 — 소스 30–50까지 ingest·검색 재측정·복구 드릴·diff 부하·스킬 evals). 선행 조건 전부 해소됨.

## 6. 저장소 규약 (r12 개정)

- **단일 저장소가 시스템 전체를 추적한다.** 예외(ignore)는 재생성·파생물뿐: `docs-mirror/mirrors/`(캐시), `core/it/archive/`(restic 담당), `.venv`·인덱스류. 원격 = `alteralab/syntopicon`(private), 백업 = core 3계층(bundle이 전체 이력 포함).
- **커밋 규약: `<레이어>/<영역>: 요지`** — 예: `core/tools: …`, `core/it: …`, `mirror/plan: …`. 루트 문서는 `plan:`·`research:`. 본문은 왜만 1–3문장(기존 core 규약 승계). 한 커밋 = 한 레이어. Ingest 트레일러 규약은 core 커밋에 그대로 적용.
- 커밋 게이트 = `git config core.hooksPath core/tools/githooks` (기기당 1회).
- 레이어 내부 작업은 해당 디렉토리의 CLAUDE.md·PLAN을 따른다. 새 구성 요소의 행선지는 §2 배치 표로 판정 — 대부분 레이어 안이 정답이고, 루트에 종류별 디렉토리(tools/·skills/)를 만들지 않는다(r4·r12).
- 이 PLAN의 개정은 §3 원장에 근거를 남긴다(리서치 산출물 또는 실측). 근거 없는 구조 변경 금지 — "잘못된 구조에 주먹구구식으로 덧붙이는 것"의 반대 원칙은 "검증된 구조를 근거 없이 재편하는 것도 같은 결함"이다.

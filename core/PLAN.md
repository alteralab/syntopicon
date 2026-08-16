# Syntopicon 계획

IT 서적·논문·기술 문서를 10–20년 축적하는 개인 지식 베이스. 2026-08-02 초판, 2026-08-04 개정판(멀티 KB 레이아웃 확정 / 태그·ADR 불채택 전환 / 데이터 플랫폼 이식 감사 반영).
결정별 검증 등급과 근거는 **`LEDGER.md`(검증 원장)가 정본**이다. 본문은 현행 규약만 기술하고, 정당화 서사는 원장과 불채택 표(§6)로 내린다 — 원장은 자라는 것이 정상이고 본문은 수렴하는 것이 정상이다. 진행 상태는 산문으로 적지 않는다(조회가 정본 — §6).

**전제**: 초기 구축 비용(1회성)은 감수한다. 최소화 대상은 **반복 유지 비용**과 **코퍼스 크기에 비례하는 O(N) 마이그레이션 비용**이다.

## 1. 원칙

1. **md + git = source of truth.** 사람이 읽고 쓰는 유일한 계층. 파생물은 전부 여기서 재생성된다.
2. **마크다운 방언 = CommonMark + GFM 부분집합(테이블·각주).** wikilink 등 Obsidian 전용 문법 금지.
3. **지식의 단위는 개념 페이지.** claim은 페이지 안의 각주 달린 불릿이며, 여러 소스의 주장이 한 개념에 누적된다. 하위 열거 불릿은 부모 불릿의 각주를 상속한다(§8). claim별 supersession·stale·모순 처리는 각주 앵커 + lint로.
4. **파생 인덱스는 소모품.** 검색·임베딩·그래프·생성 목록은 md에서 전량 재빌드. 백업 대상은 빌드 스크립트 + 버전 핀 + 재빌드가 시간 단위인 인덱스의 사본(§5). 소모품 증명 = 분기 재빌드 드릴(§6).
5. **구축·지연 판단 기준.** 데이터 계층 규약(스키마 의미론·링크 문법·저장 위치)은 소급 수정이 O(N)이므로 첫 파일 전에 확정. retrofit O(1)인 것(파생물·물리 샤딩·인덱스)은 지연이 기본값 — 필요가 실측되기 전의 선제 구축은 결함으로 취급(§8 flat 시작 항).
6. **쓰기 정책은 계층별 차등**(§4.4). 전수 수동 게이트도, 무게이트 자동 기입도 아니다.
7. **부패 관리는 휘발성의 함수.** forgetting curve 없음. 명시적 supersession + `stale_after`. **`stale_after`는 예측이 아니라 기록이다** — 벤더 EOL 공표일·지원 종료일처럼 문서로 확인 가능한 미래 날짜만 적고, 감 기반 추정 금지(부패 시점 예측은 업계 실증 부재 — §8). **기입 시 근거 각주 의무**(공고 URL) — 의미론 자체는 advisory지만 근거 유무는 리뷰·lint가 결정적으로 검사 가능하다. 모르는 휘발성은 비워 두고 supersession·review-on-read가 담당한다. 외부 링크는 **낙관적 최저 추정으로도** 연 ~3% 부패(실측 범위는 그 이상 — §8)하므로 로컬 스냅샷 필수.
8. **주제 조직은 링크가 담당.** 그래프 인프라 불채택, 그래프 질의 채택 — 큐레이션된 링크 위의 SQLite edges + 재귀 CTE(§4.1; 승급 사다리는 §4.2). 주제 슬라이싱은 허브(synthesis) + backlinks. 태그 없음(§6 불채택).
9. **KB 자립성.** 저장소 = 공유 계층 + N개 KB(§3). 각 KB는 다른 KB 없이 읽히고 쓸모 있어야 한다. 크로스 KB 의존은 경계 설정 오류의 신호(§4.5).
10. **최대 리스크는 유지비용.** 예산 2–3주당 30–45분. 반복 작업은 결정적 스크립트로, LLM·인간은 판단에만. 10–20년 축에서 과거의 나는 타인이다 — 영향 범위는 기억이 아니라 조회 도구(`tools/affected`)가 답한다.

## 2. 스키마

### 2.1 개념 페이지 frontmatter

```yaml
---
type: concept          # 어휘: §2.3
title: Raft 읽기 경로   # 표시 전용, 유일성 비요구 (충돌 규칙 §2.5)
description: 한 줄 요약  # 소비자: 검색 스니펫·스코프 pruning(손실 요약 — 전문 FTS 폴백 전제). 편집 시 재생성
generated: { by: "claude-fable-5", at: "2026-07-31T05:00:00Z" }   # 인간 저작도 human:me 기록(부재="출처 불명")
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }   # 저장소 루트 기준 경로 (§2.4)
# 값이 생길 때만 기록 — "부재 = 기본값":
#   status: deprecated          # 부재 = stable
#   verified: [{by: "human:me", at: "..."}]  # 부재 = unverified 계층. 빈 리스트 금지
#   stale_after: "2027-06-01"   # 공표된 날짜만(EOL 등) — 감 예측 금지, 부재 = 만료 없음(foundational)
#   superseded_by: raft-read-v2 # deprecated 전환 시에만. 동일 KB 슬러그 — redirect 스텁의 KB 간 이동 잔여물만 정규형 `<kb>/<slug>` 허용
#   contradicts: [other-slug]   # 모순 상호 기록(동일 KB) — 소비자: kb-lint 쌍 목록. 자동 해소 금지,
#                               #   해소 시 최신성 단독 판단 금지 — 해소 날짜·결정 근거·대체된 주장을 페이지에 기록
#                               #   **대상은 사실 주장의 충돌(최대 하나만 참)에 한정.** 방법론·설계
#                               #   트레이드오프(상황이 고르는 선택)는 대상 아님 — 본문 병기 + 선택 기준은
#                               #   synthesis가 담당. 해소되지 않는 쌍이 큐에 상주하면 큐가 죽는다(§8)
---

## 읽기와 quorum

- leader lease 없이는 읽기에도 quorum 왕복이 필요하다 (§5.4 기준).[^ongaro2014-raft]
- #hypothesis lease 시계 드리프트 한계는 실무 문제 사례가 드물다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §5.4
```

- **claim 귀속은 본문 각주** `[^citekey]`, locator(페이지·절)는 각주 텍스트에. frontmatter 중첩 locator 금지.
- **null 자리표시 금지**(파서가 null과 부재를 구분 못 함). `as_of`류 중복 필드 재도입 금지(사유는 schema/migrations.md에 기록).
- **epistemic 표기는 본문 인라인 토큰** `#hypothesis` / `#speculation`(무표기 = 사실 서술). 숫자 confidence 금지. **폐쇄 어휘** — 정의는 schema/에 두고 추가는 스키마+migrations 개정으로만. lint가 미정의 토큰을 검출. frontmatter 태그 필드는 없다(§6 불채택).
- **시간 해상도**: 이벤트(`generated.at`, `verified[].at`) = ISO datetime, 유효성(`stale_after`) = YYYY-MM-DD. 초 단위 transaction time은 git이 제공.
- **YAML 규약**: 날짜·datetime 값은 반드시 따옴표 문자열. 도구는 파일 통짜 load-save 금지(라운드트립이 파일을 재작성함) — frontmatter 수정은 대상 필드만.

### 2.2 소스 메타 (sources/)

- **type 1단 구조**: `book | article-journal | paper-conference | article(프리프린트) | webpage | post-weblog | speech | motion_picture(영상) | standard | report` (CSL 공식 enum 차용). 계층(소스/개념/종합)은 type 어휘 분할표로 표현하고 validate가 type↔디렉터리 정합을 검사(layout.yaml 기준).
- **필드명은 CSL-JSON 원어**: 대문자 `ISBN`/`DOI`/`URL`, 접근일은 `accessed`, arXiv ID는 `number` + `publisher: "arXiv"`, 제품 버전은 `version`(문자열), 컨퍼런스명 `event-title`, RFC는 `number`+`collection-title`+`authority`, 영상 러닝타임 `dimensions`, 영상 타임코드는 인용 시점 locator(`timestamp`).
- **확장 필드 3개만**: `snapshot`(로컬 스냅샷 루트 경로), `snapshot_sha256`(ingest 시점 write-once — 변조 증거, 소비자: lint), `custom: {archive-url: …}`(웨이백 URL — CSL 공식 확장 봉투).

```yaml
---
type: book
title: "Designing Data-Intensive Applications"
author: [{family: Kleppmann, given: Martin}]
issued: 2017
publisher: "O'Reilly Media"
ISBN: "9781449373320"
edition: 1
snapshot: /it/archive/kleppmann2017-ddia/
snapshot_sha256: "..."     # ingest 시점 1회 기록(write-once) — 변조 증거, 소비자: lint
accessed: "2026-07-31"
---
```

- **citekey = 파일명 = `저자성last연도[-슬러그]`**, 문자 집합 `[a-z0-9_.-]`(콜론·공백·대문자 금지 — 각주 앵커 파손). **유일성은 KB 스코프**(§2.5) — 결정적 규칙이므로 같은 소스는 KB가 달라도 같은 citekey로 수렴하고 경로가 구분한다. 동일 저자·연도 충돌만 `-2` 접미 허용. **한국어 저자**: 소스에 인쇄된 영문 표기 우선, 없으면 생성 시점 RR 로마자화(발급 후 불변이 표기 불안정성을 흡수). Zotero 도입 시 Better BibTeX citekey 채택.

### 2.3 type 어휘 (동결)

| 파일 종류 | type |
|---|---|
| 개념 페이지 / 인간 저작 종합 | `concept` / `synthesis` |
| 소스 메타 | CSL 타입군(§2.2) |
| redirect 스텁(개명·이동·분할·병합 잔여물) | `redirect` — `superseded_by`가 대상 지정(KB 간 이동 스텁만 정규형 허용). lint 동작은 §4.3 표가 정본 |
| overview.md·SCHEMA.md | `guide` |
| inbox/ 초안 | `concept` + `status: draft` |
| 허브(MoC) | `synthesis` — 전용 type·표지 없음, 링크 차수(edges 질의, §4.1)로 식별 |

### 2.4 경로·링크 규약

- **본문 링크 = 파일 상대 경로**(`../sources/x.md`) — GitHub·Obsidian이 합의하는 유일 형식. **KB 내부에서 닫힌다**(원칙 9).
- **frontmatter 경로(`sources[].resource`, `snapshot`) = 저장소 루트 기준**(`/<kb>/sources/x.md`) — 인용하는 파일이 이동해도 불변. OS 절대경로 금지.
- **크로스 KB 참조 = `qmd://<컬렉션>/<경로>`** — 문법만 여기서 규정. 정책(비권장·edges 가시화·lint warn)은 §4.5가 정본.

### 2.5 ID 발급·동시성 규약

1. **발급 주체**: kb-ingest/kb-new가 제안, **validate가 강제**(유일성·문자집합·유사 충돌 경고). 수동 생성도 pre-commit validate 경유.
2. **발급 후 불변.** 개명·이동(KB 간 포함)은 `tools/rename` 경유만: md AST 기반(markdown-it-py) 링크 재작성 + frontmatter 경로 처리 + redirect 스텁 생성 + 사후 링크 검사 게이트. heading 앵커는 자동 재작성하지 않고 lint가 검증.
3. **유일성 스코프 = KB.** 슬러그·citekey는 KB 안에서 유일하면 된다. **정규 참조형 = `<kb>/<slug>`** — 저장소 전역 유일, 경로에서 파생(별도 저장 없음).
4. **개념 슬러그**: 영문 소문자 kebab(`[a-z0-9-]`), ~80자 이하, 한글 파일명 금지(NFC/NFD·바이트 한도). 한국어 개념은 로마자화 금지 → **영어 개념명 번역**(확립 용어 우선). title은 한국어 유지. **충돌은 의미 한정자로 해소**(`consistency-acid` vs `consistency-eventual`) — 숫자 접미 금지(예외: citekey `-2`). **날짜/번호 접두 금지(무예외)**.
5. **동일 기기 병렬 프로세스**: 파일명=ID인 슬러그·citekey는 도구가 **O_EXCL 생성(`open(path,'x')`) 의무** — KB 디렉터리 내 파일명 유일성은 fs 원자성이 게이트(로컬 FS 전제는 §5 토폴로지가 보장). check-then-write 금지.
6. **기기 간**: 슬러그 충돌은 git `AA`(both added) 충돌이 감지기. citekey는 결정적 규칙으로 수렴하며 `-2` 결과는 파일에 데이터로 고정. **중앙 발급 서비스 불채택** — md+git 밖의 제2 진실 원천 금지.
7. **ID 외 동시성**: ⓐ 재색인·`qmd update`는 단일 실행 직렬화 ⓑ 텔레메트리는 git 밖 stats DB(§3) ⓒ inbox diff는 런ID 명명 + O_EXCL ⓓ index.sqlite 사본은 §5 규약 준수(라이브 cp 금지) ⓔ rename·compaction은 클린 워킹트리 확인 후 에이전트 세션과 비동시 실행 ⓕ git push(non-ff 거부)·restic(불변 블롭)·bundle(git 일관 스냅샷)은 무처방 안전 ⓖ **다중 파일 쓰기의 트랜잭션 모델 = 보상(compensation)**: 원자적 다중 쓰기 대신 클린 워킹트리 가드(`repo.ensure_clean_worktree` — ⓔ의 단일 구현) 위에서 실행하고 실패는 git으로 전량 원복한다. 스토어 간(md↔파생 인덱스) 정합도 원자화하지 않는다 — 세대 스탬프 대조(`index_db.staleness`)가 낡은 소비를 거부하고 재색인이 조정한다. 업계 동형(정본+파생+주기 조정 — Tencent·Letta·mem0·Graphiti 전수에서 스토어 간 2PC 부재, 원장 2026-08-13).

### 2.6 페이지 위생

- **분할 1차 기준은 목적**: 한 페이지 = 하나의 질문. 분할 조건: 섹션이 다른 질문에 답하기 시작 + 자식이 자립 가능. 자식이 스텁이 되거나 부모 요약의 복제면 분할 금지.
- **크기는 lint 백스톱**: 500줄 초과 경고(자동 분할 아님 — 수치는 임의 운영 상수, §8). 100줄 초과 시 상단 TOC. 지식 페이지는 온디맨드 독해 계층이므로 1차 완화책은 분할이 아니라 **TOC + 섹션 앵커**(상시 로드 계층용 상한의 전이 금지 — §8).
- **구조**: 파일당 H1 하나(제목 일치)·헤딩 레벨 건너뛰기 금지(표준 — §8), 깊이 H3–H4 상한(H4 필요 = 분할 신호 — 자체 휴리스틱, §8).
- **TOC 형식**: 정본 = **링크 불릿 목록**(H1 바로 아래, `- [섹션](#앵커)`). 인라인 문단형(`**목차**: … · …`)에서 2026-08-11 전환 — 항목 29개·982바이트 한 줄이 실측됐고, 세로 스캔·계층 표현·가운뎃점 회피가 이유다(§8). **앵커는 손으로 쓰지 말 것** — 구두점이 사라지며 양쪽 공백이 하이픈 둘로 남는다(`제목 — 부제` → `제목--부제`). lint의 `anchor-broken`이 검사한다.
- **링크 리스트 문법**(synthesis 허브·overview): 링크로 시작하는 불릿은 `- [제목](경로) — 한 줄 설명`, 위반은 lint warn. YAML 온톨로지 블록은 불채택(§6).
- 분할·병합 시 **redirect 스텁**을 남기고, 병합 시 각주 라벨 충돌은 스크립트가 네임스페이스 처리.
- 페이지 간 중복은 만성 → **overlap lint(페이지 쌍 임베딩 유사도, KB 내부)를 1급 규칙**으로.

### 2.7 스키마 진화 — 동결 코어 vs 개방 확장면

additive 확장(새 optional 필드)은 안전하고, 의미론 변경은 O(N)이다. **동결 코어**(첫 파일 전 확정, 이후 불변):

1. `type` 어휘(§2.3)와 계층 분할표, "디렉터리는 뷰, type 정본은 frontmatter"
2. 파일명=ID 규칙·문자 집합·**KB 스코프 유일성**·충돌 해소·title 비유일
3. 링크·경로 문법(§2.4) + GFM 부분집합
4. 각주 = 출처 귀속 전용 채널, citekey 문자 집합
5. 날짜 의미론(이벤트=datetime, 유효성=date, 따옴표 문자열) + 부재=기본값
6. epistemic 토큰 폐쇄 어휘
7. 신뢰 계층 의미론(generated/verified, 승급 규칙)
8. **layout.yaml**(§3) — 공유 자산 화이트리스트·KB 골격·색인 경계

- 코어는 **per-type JSON Schema(YAML 저술) + 파이썬 관계 규칙의 2층**으로 기계화되어 validate가 강제한다(관계 규칙 — citekey↔각주 정합·경로 실존·layout 분할 — 은 JSON Schema로 표현 불가). 산문 SCHEMA.md는 설명서일 뿐, 에이전트가 산문 규칙을 따른다고 가정하지 않는다.
- **모든 필드는 소비자(읽는 도구·질의)를 명시해야 하며 소비자 없는 필드는 도입 금지.** 집행: lint의 **필드 사용률 검사**(§4.3)가 선언 대비 실사용을 주기적으로 대조한다 — 선언은 도입 시점의 의도만 남기고, 갭은 조회로만 드러난다.
- **임의 확장**: OKF unknown-key 허용(최상위 additive) + 소스 계층 `custom:` 봉투. 향후 신규 개인 필드는 `x_` 접두 또는 `custom:` 봉투(미래 스펙 키 충돌 방지).
- **레지스트리**: `schema/*.yaml` = 현재 스키마, `schema/migrations.md` = append-only 변경 로그(날짜·구→신 매핑·의미 주석). **호환 정책 BACKWARD_TRANSITIVE**: additive만, in-place 개명 금지(새 키 + 매핑 기록 + 선택적 backfill), **은퇴 키 이름 영구 결번**. 집행: **validate가 migrations.md의 은퇴 키 목록과 스키마·신규 파일을 대조**한다. per-file schema_version 기록 금지(파일은 재작성되지 않으므로 거짓말하는 필드가 됨) — git 커밋 날짜 + migrations.md가 해석을 제공.

## 3. 저장 구조

**저장소 = 공유 계층(1부) + N개 KB(동형).** KB는 kb-new만이 생성한다 — 구축 직후 KB는 0개이고, ingest는 KB가 없으면 실패한다(§4.4-0).

```
syntopicon/
  SCHEMA.md            # 규약 설명서 (규범은 schema/ — 기계 게이트가 정본)
  overview.md          # 에이전트 진입점 = KB 라우터 (~200토큰: 규약 요지 1줄 + KB당 1줄)
  schema/              # per-type 스키마 + layout.yaml + user-dict.yaml(색인 CLI) + migrations.md
  CLAUDE.md, AGENTS.md # 훅 없는 하네스용 1줄 규칙 사본 (Claude Code는 UserPromptSubmit 훅이 주입 경로)
  tools/               # 결정적 CLI. Tier A(md 변경 — rename/validate/lint/kb-new): 순수 파이썬(markdown-it-py)·최소 의존·핀.
                       #   Tier B(소모품 인덱스 빌더·affected): 무제약
                       #   구현 규약(전 Tier): 구조 형식의 파싱은 파서로(md=AST·YAML=파서·경로=pathlib) —
                       #   regex 파싱 금지(엣지 케이스마다 패턴 증식하는 greedy 수정 루프, §8). 예외: 문자집합
                       #   검증(슬러그·citekey — 정규 언어 그 자체)만 regex 허용. 파이썬은 pythonic 관용구 준수
  evals/               # 스킬 평가 시나리오 (runs/는 ignore)
  .agents/skills/      # 정본 스킬 6종 — 배포는 기기별 `~/.claude/skills/` 심링크(§4.3), 저장소 내 사본 없음
  .gitignore           # */archive/, *.db, *.sqlite*, evals/runs/
  <kb>/                # ★ KB마다 동형. qmd 컬렉션·restic --tag·임계 경보 집계 = 이 디렉터리 단위
    overview.md        # KB 허브 진입점 (~1–2k 토큰): 한 줄 오리엔테이션 + ## Hubs(10–30, 링크+한 줄 설명) + ## Tools
                       #   자유 md — 진입 문서 50년 관례(README·Home note·OKF index)와 동형(§8). "## Hubs" 절 이름만
                       #   자체 계약(소비자: lint 대조). 포인터 중심 — 본문 복제(발췌·수치) 금지: 진입점 부패 벡터(§8)
    sources/  concepts/  synthesis/  inbox/
    archive/           # 소스 원문 스냅샷 — git 제외, restic 담당(§5)
```

- **layout.yaml이 경계의 정본**: ⑴ 공유 자산 화이트리스트 ⑵ KB 골격(디렉터리↔type 정합 표) ⑶ 색인 포함/제외 패턴(`<kb>/**` 포함, `archive/` 제외). 소비자: validate·kb-new·kb-ingest 게이트·색인 CLI·백업 스크립트. **KB 인스턴스 목록은 파일시스템이 정본**(마커 = `<kb>/overview.md`, type: guide) — validate가 루트 직하를 `공유자산 ∪ KB`로 완전 분할 검사해 오타 디렉터리를 fail-loud로 잡는다. 레지스트리 이중화 없음.
- **운영 로그는 git에 넣지 않는다.** 텔레메트리(search-miss·런 지표·lint 결과)는 **로컬 stats DB**(파생 SQLite, 소실 허용). 이벤트 저널은 git 히스토리 + 커밋 트레일러(`git log --grep Ingest-Source`).
- **저장물 수명 주기 3분류**: ① 영구 축적(git — sources/concepts/synthesis) ② 일시 격리(git — inbox/, 리뷰 후 소멸) ③ 텔레메트리(git 밖 — stats DB). 무기한 쌓이기만 하는 디렉터리는 없다.
- **디렉터리 상한·샤딩**: 디렉터리당 ~1–4k 파일(근거 §8 — git·GitHub 제약, FS 성능 아님). **모든 콘텐츠 디렉터리는 flat으로 시작**하고, 상한 접근이 실측될 때 신규 파일부터 샤딩한다(기존 파일 불이동 — 원칙 5). 선제 샤딩 금지.
- **경로와 의미론**: 물리 **샤딩** 차원은 경로 단독 인코딩 금지 — 질의 인터페이스는 frontmatter(메타 테이블). 단 **KB 소속·inbox 수명주기 같은 경계는 경로가 정본**이며 메타 테이블이 색인 시 파생한다(`[unreviewed]` = inbox 경로 + `verified` 부재).
- **글루 동거·엔진 외부**: 저장소 안에는 이 스키마에 결합된 글루(tools·스킬·evals)만, 엔진(qmd·ir_measures·skill-eval)은 외부 설치·핀. 동거 근거 = 원자적 커밋(스키마 마이그레이션 = content+schema+validate 동일 커밋). **분리 발동 신호**: tools/ 커밋이 콘텐츠 커밋을 지속 상회하거나 tools/가 두 번째 소비자를 얻을 때.
- **tools 구현 헌장** (요지만 — 각 규칙의 근거 전문은 그 규칙이 묶이는 자리의 docstring이 정본이다. 코드 곁의 근거는 표류하지 못한다): ⑴ 파서 우선, regex는 문자집합 검증만(원장) ⑵ **상태를 읽는 함수에 숨은 memoization 금지** — 부를 때마다 현재를 읽고, 고정 스냅샷은 호출자가 들고 다닌다(정본: `repo.visible_files`·`layout.load` docstring) ⑶ **계측은 도구가 실행하는 김에 자동으로** — 산문 지시 계측은 실측 0건으로 죽는다(정본: `stats.py`·`search.py`) ⑷ I/O는 가장자리(main)에서, 계산은 자료를 반환한다 ⑸ 이름·등급·지침 류의 대응표는 **코드 레지스트리가 단일 정본**, 문서는 조회(`--explain`)로 참조(정본: `checks/base.py`) ⑹ 파생 SQLite는 raw DDL 유지 — ORM·마이그레이션 도구 불채택(원장) ⑺ **새 코드 전 3문**: 어느 기존 모듈의 책임인가 / 문서의 "한 덩어리"를 코드로 옮기는 것인가, 새 표면인가 / 삭제나 통합으로 풀 수 있나.
- SCHEMA.md·overview.md도 frontmatter `type` 보유(예약 파일명 외 전 .md는 typed frontmatter).

## 4. 파이프라인과 도구

### 4.1 진입점과 검색

**진입점 — 전체 카탈로그 없음, 2계층 + 검색 우선.** ① 루트 `overview.md`(라우터) → ② `<kb>/overview.md`(허브, MoC 목록) → ③ 검색 도구가 1차 경로.

**검색 스택 — qmd + 자체 레그 2종.**

- **qmd 채택**(SQLite FTS5 + 로컬 GGUF 임베딩 + RRF + 리랭크 + CLI/MCP + SHA-256 증분 색인). **버전 핀 + `npm pack` 타르볼 보존**. 폴백 사다리: basic-memory(**부분 폴백** — 저장·FTS·MCP 서빙만: 그래프는 wikilink 전용·형태소 부재·`disable_permalinks: true` 필수, 소스 검증 §8) → Meilisearch(발동 조건 §6 표) → LEANN(시맨틱 보조). 한국어 질의는 확장 없는 `search`/`vsearch`(질의 확장의 영어 편향 회피). 데몬 모드로 모델 웜 유지.
- **임베딩 = Qwen3-Embedding-0.6B 잠정**, 수용 검증 A/B(vs KURE-v1) 후 핀. **모델 버전 = 스키마 버전, 호환 NONE**: 모델 id+리비전+차원+청킹을 인덱스 메타에 핀, 변경은 blue/green 전체 재빌드. 서로 다른 모델 벡터 혼합 금지(무경고 recall 붕괴). **차원은 모델 최대(1024) 유지 — MRL 축소 금지**(저차원일수록 규모 오탐 단조 증가, §8). **무효화 단위 = 페이지**: 편집 시 해당 페이지 청크 전량 재생성(§4.4-9가 집행). 청킹은 색인기(qmd) 소관 — 페이지 크기와 독립(실측 §8; ≤900토큰 페이지는 1청크).
- **벡터 레그의 존치 조건**: grep 우위 실증은 코드·어휘 일치 질의 대상이고, 산문 패러프레이즈·한국어 표면형 변형이 벡터의 잔존 근거. 기여도는 수용 검증 A/B로 측정 — 무시 가능이면 FTS 전용 강등. **파이프라인 RAG 층 금지** — 에이전트가 도구를 고르는 구도를 유지한다(stats 기반 자동 전략 선택 없음).
- **자체 레그 ① 한국어 형태소 FTS**: Kiwi 분석 → 공백 join → FTS5 unicode61 테이블. 필수 사양: **질의 시점 대칭 분석**(질의도 동일 Kiwi+동일 POS 필터로 phrase 변환), **POS 필터 = 명사류+SL/SH/SN+용언 어간+XR+W_HASHTAG**(앞 4종은 nori STOP_TAGS 정합 — 단 **정합 논거는 Kiwi 독자 W_\* 계열에 닿지 않는다**: nori에 대응 태그가 없어 교집합 검사로 검출 불가이고, 방향도 반대다(nori는 `10.1`을 10·1로 살린다). 폐기 여부는 소비자 유무로 판정 — W_HASHTAG는 폐쇄 어휘 `#hypothesis` 소비자 14건이라 유지, W_SERIAL은 소비자 0건이라 폐기 존치 + `rg` 폴백. 실측 §8), **사용자 사전 필수**(`schema/user-dict.yaml` 시드 + 파편화 검출로 증분 관리, 사전 변경 시 재색인), compound는 성분 분해+phrase 질의, **코드 펜스는 색인 제외**(AST가 빼낸다 — 인라인 백틱은 색인. 근거는 SCHEMA.md §3과 §8 실측: 펜스 토큰이 같은 절 산문의 BM25 길이 정규화를 깎는다). 음절 substring은 qmd 내장 레그가 담당, 영문 부분문자열과 **펜스 코드 조회**는 `rg` 폴백.
- **자체 레그 ② frontmatter 필터**: type/status/stale_after 스코프 질의용 SQLite 메타 테이블(qmd는 frontmatter 미파싱). 필터 필드만 실컬럼, 나머지 JSON. **인덱스는 만들지 않는다**(실측 근거 §8) — 필요가 실측되면 추가(소모품, retrofit O(1)).
- **검색 스코프**: 읽기 = **무스코프 횡단이 기본** + KB 필터 옵트아웃. 다중 KB 랭킹은 전역 top-K 후 필터이므로 `-n` 상향을 기본값에 반영. 쓰기(저장·ingest)는 `--kb` 명시 필수.
- **결과 형식**: `(파일, 헤딩 앵커, 라인, 1–3문장 스니펫, 헤딩 계보)` — 섹션 → 페이지 순 확장. 융합 리스트 + 채널 태그 `[fts]`/`[vec]`/`[both]` + **KB 라벨**, concise 기본.
- **edges 테이블**: 링크 파싱 → `backlinks`/`neighbors(k)`, 탐색 깊이 상한 4(실측 근거 §8). **크로스 KB 링크(`qmd://`)도 엣지 타입을 구분해 포함** — 무결성 검사 대상, 탐색 기본 스코프는 KB 내부. 허브 식별은 edges의 **링크 차수 질의**로 충분 — `<kb>/overview.md` Hubs 갱신의 입력(그래프 분석 배치는 불채택 — §6).

### 4.2 멀티홉 승급 사다리 (선검증 완료)

멀티홉 품질 판단은 체감이 아니라 **평가 하네스의 측정값**(gen_corpus/build_edges/eval_retrieval/graph_batch — tools/ 편입, 수용 검증에서 실코퍼스 재측정).

- **1단 — 에이전트 링크 탐색**: top-3 시드의 k-hop 확장(2-hop k=1, 3-hop k=2)이 합성 실측에서 flat 검색을 완승(수치 §8). 심긴 체인 실험이라 상한 추정 — 실코퍼스 재측정이 판정.
- **2단 — HippoRAG2 (불채택 상태의 검증된 비상 경로)**: md 직접 투입·증분 색인 확인(비용·기각 근거·발동 조건은 §6 표). 채택 계약: 검증 시점 커밋 SHA 핀, 발동 시 레포 펄스 재확인, git SHA 설치, 사멸 시 포크.

### 4.3 스킬 6종과 도구

판단 불필요 로직은 전부 tools/ 스크립트로, SKILL.md는 워크플로·판단 기준만. agentskills.io 코어 스펙 내에서만 작성.

- **kb-ingest**: §4.4 파이프라인의 실행자 — 인간 판단(1·8)은 대화, 기계 단계(0·2·6·7·9)는 tools/ 호출, LLM 단계(3·4)는 스킬 지침(3은 발급 스크립트와 하이브리드).
- **kb-query** (체크리스트): ① 라우터→허브로 방향(최초 1회) → ② 횡단 검색(qmd + 형태소 CLI) → ③ 히트 섹션→페이지→링크 이웃 확장(KB 내부; 크로스 KB 엣지는 표시만, 명시 요청 시 추적) → ④ 공백 평가(미스는 `search-miss` 이벤트로 stats DB에 KB 필드와 함께 기록) → ⑤ 공백에 한해 웹 검색 → ⑥ 답변에 출처 라벨(`[<kb>]`/웹/`[unreviewed]`) → ⑦ 종합 저장 판단 3문 — 전부 예일 때만 `--kb` 명시로 inbox/ 경유 저장: ⑴ 세션 맥락 밖에서도 재사용되는가 ⑵ 기존 페이지 재조합이 아닌 신규(교차 발견·공백)인가 ⑶ claim마다 각주 가능한 출처가 있는가(웹 출처는 ①부터). 오판은 구조가 흡수 — 과잉 저장은 inbox 격리·overlap lint·P90 경보, 과소 저장은 search-miss가 감지. machine 계층 claim을 실사용 시 검증하면 `verified` 승급(review-on-read).
- **kb-lint** — 검사 매트릭스(검출만, 수정 커밋은 사람. validate=커밋 게이트, lint=전수 리포트):

| 검사 | 스코프 | 데이터 소스 | 산출처 |
|---|---|---|---|
| 깨진 링크·redirect 경유 링크 | KB | edges | 리포트 + 재작성 제안 |
| 크로스 KB 링크·redirect 존재 | 저장소 | edges(엣지 타입) | **warn** — 분리 시 파손 예고 |
| 만료 `stale_after` | KB별 큐 | 메타 DB | 재검토 큐 |
| 고아 페이지 | KB | edges | 리포트 |
| Hubs 절 ↔ 고차수 synthesis 대조 | KB | edges | overview 갱신 후보 리포트 |
| 각주 없는 claim 불릿(하위는 부모 각주 상속 — §2.1) / 각주↔sources.id 정합 | KB | md AST | 리포트 |
| claim locator 괄호 부재 (각주 직전 — §4.4-4) | KB | md AST | 리포트 |
| 허브·overview 링크 불릿 설명 누락 (§2.6 문법) | KB | md AST | 리포트 |
| `$…$` 인라인 수식 (SCHEMA §3 수식 표기) | KB | md AST + pandoc 판별 규칙 | 리포트 (통화 오탐 0 — 실측 §8) |
| 각주 밖 코드 펜스 (SCHEMA §3 코드 표기) | KB | md AST(불릿 각주 스택) | **warn** — 출처 없는 코드는 발명한 claim. 코드가 정말 그 소스에서 왔는지는 기계 밖(리뷰 양식) |
| 페이지 내 앵커 링크 ↔ 실제 헤딩 (§2.5-2가 규정한 검사) | KB | md AST + GitHub 앵커 규칙 | 리포트 |
| 원어 병기·직인용 (한국어 저작 규칙 §4.4-4) | KB | 판단 영역 — 기계 검사 없음(근사 패턴 금지 §3) | 집행점 = 승급 리뷰 템플릿 |
| 페이지 overlap(중복) | KB | 임베딩 | compaction 후보 큐 |
| `contradicts` 쌍 | KB | 메타 DB | 연구 과제 큐(자동 해소 금지) |
| 스냅샷 누락 / `snapshot_sha256` 불일치 | KB | 소스 메타 + archive/ | 리포트(변조 증거) |
| GFM 방언·500줄·TOC 부재·TOC 형식 | 저장소 | md 스캔 | 리포트 |
| 미정의 epistemic 토큰 | 저장소 | md AST | 리포트 |
| inbox 나이·크기 | KB별 | 메타 DB | 임계 경보(P90) + 리포트 |
| frontmatter 필드 사용률 | 저장소 | 메타 DB | §2.7 소비자 선언 대비 리포트 |
| 형태소 파편화(연속 1음절 런) | 저장소 | 형태소 색인 | 사용자 사전 후보 큐 |
| ingest 커밋 트레일러 존재 | 저장소 | git log | 리포트 |

  **실행 전략**: 주간 실행은 **증분**(직전 실행 이후 변경 페이지만 — overlap도 1×N 비교라 규모 무관). **전쌍 overlap은 부트스트랩과 분기 전수 검사에서만**(블록 행렬곱으로 임계 초과 쌍만 보존 — 산수 근거 §8). **산출 스키마**: severity(error/warn/info)를 달아 리포트(사람·주간)와 stats DB(경보·큐)의 이원 기록.
- **paper-search** (논문 조달 전용, 반입은 하지 않는다): ① **공백 식별** — 주제를 떠올려 검색하지 않고 ksearch·edges로 "페이지가 이미 이름을 쓰는데 출처가 없는 자리"를 찾는다(공백이 없으면 후보를 내지 않는다) ② **후보 탐색** — WebSearch·WebFetch. **전용 도구 없음**(원칙 5 — 반복 패턴이 실측되면 tools/로 내린다) ③ **자격 판정 4문** — 원전인가(서베이·재해설 아님) / 심사를 거쳤나(축별 최상위: 시스템=SOSP·OSDI·VLDB·SIGMOD·USENIX, 검색=SIGIR·CIKM·ECIR, LLM=ACL·EMNLP·ICLR. **이 KB의 AI 축은 검색·임베딩이라 ICML 인용 0건 — "AI니까 ICML"은 오판**) / 기존 축에 닿나 / 오픈액세스인가 ④ **arXiv는 예외가 아니라 상수** — 심사 통과본이 있으면 그쪽을 소스로, 프리프린트면 소스 메타에 미심사 명시 ⑤ **후보 제시, 선택은 사람**(§4.4-1의 "스크립트화 불가"를 지키는 지점 — 애매하면 자기 판단으로 반입하지 않는다). kb-ingest 1단계가 "논문인데 사용자가 지목하지 않은" 경우 호출한다.
- **kb-new** (명시 호출 전용, KB의 유일한 생성 경로): ① **판단 게이트** — 기본 답은 "만들지 마라": 대부분의 구분 요구는 기존 KB의 디렉터리·허브로 해소된다(주제 분리는 사유 아님). KB가 0개면 게이트를 생략하고 생성으로 직행. 분리 대(對) 동거 심사 3문: ⑴ 기밀·접근 통제 경계인가? ⑵ 별도 동기화/백업 정책이 필요한가? ⑶ `type` 어휘·링크 문법의 분기가 필요한가?(새 주제·새 디렉터리는 사유 아님) — 하나라도 예면 **저장소 분리(비가역 — §4.5)**, 전부 아니오면 동거 KB 생성. ② **기계 단계** — `tools/kb-new`: **layout.yaml의 KB 골격에서 직접 생성**(비어있지-않으면-거부) + qmd 컬렉션 등록 + 루트 overview.md 라우터 갱신 + restic `--tag` 추가. **git init은 저장소 분리 경로에서만.** ③ **편입** — 운영 캘린더·KB별 임계 경보 집계 대상 포함.
- **kb-plain** (참조 규약 — 단독 호출보다 다른 스킬·양식이 참조): 사람이 읽는 산출물의 쉬운 언어 규칙 — 적용은 리뷰 양식 필수, kb-query 답변은 `--plain` 옵션 시, 브리핑 권장. 규칙 = 금지 기호(엠대시·가운뎃점 0건)·기호 압축 금지·비승인 어휘는 lexicon.txt 대체어로(ASD-STE100 형식)·표시 텍스트는 명사구. 검사기 `tools/plaincheck.py`(markdown-it-py AST로 code·blockquote 제외, 정확 문자·문자열 대조만, 위반 시 exit 1 — 검출만, 수정은 저자). KB 본문 페이지는 비대상(§2·vocabulary.yaml 관할). 출처: 전역 humanwrite 스킬 규칙의 2026-08-10 발췌 내재화 — 외부 스킬 소멸과 무관하게 자체 완결, 증보 정본은 lexicon.txt.
- **tools/affected [Tier B]**: 스키마 필드·type·layout 변경 전에 영향 파일·KB를 조회하는 CLI(메타 테이블 질의 래퍼). 소비자: 스키마 개정 절차(migrations.md 기록 전 실행)·리스크 표(영향 범위 망각).
- **스킬 배포**: 정본 = `.agents/skills/`(커밋 — 크로스 클라이언트 관례, evals가 저장소 루트 상대로 참조하므로 저장소 내 필수). Claude Code 로드는 **기기별 `~/.claude/skills/<이름>` 심링크**(공식 지원, personal 스코프 = 전 프로젝트에서 `/kb-query` 가능, 같은 타깃은 1회 로드). 저장소 내 사본·복사 동기화 없음 — 커밋되는 심링크만 금지(Windows 클론 파손). 스킬의 tools/ 참조는 심링크 해석 후 저장소 루트 기준.
- **발동 정책(공통)**: 산문 지시의 준수는 비보장 → (a) 명시 호출(`/kb-query`)이 기본 워크플로 (b) 1줄 포인터는 **사용자 레벨** `~/.claude/settings.json`의 UserPromptSubmit 훅으로 주입(전 프로젝트 발화 — 프로젝트 훅은 해당 저장소만). 암묵 발동에 의존하지 않는다(최적화 배터리 불채택 — §6). MCP 표면은 qmd 내장으로 충분(자체 서버 불채택 — §6), 전역 등록으로 셸 없는 클라이언트도 커버.

### 4.4 Ingest 파이프라인과 쓰기 정책

**파이프라인** ([인간]=판단, [LLM]=제안, [스크립트]·[자동]·[기계 게이트]=결정적 실행, [구조]·[규약]=구조적 강제):

0. **KB 스코프 게이트 [스크립트]** — `--kb` 필수. 대상 KB가 없으면 fail-loud: "KB가 없습니다. kb-new를 먼저 실행하십시오."
1. **소스 획득·큐레이션 [인간]** — 넣을 가치의 판단은 스크립트화 불가 영역. 원서·번역서 병존 시 **원서가 ingest 소스**(시차 ~1년·중역 경유 회피 — §8), 번역서는 확립 역어 참조원으로만.
2. **스냅샷 [스크립트]** — `<kb>/archive/` 저장 + `snapshot_sha256` 1회 기록. 소급 불가능한 유일 단계라 최전방 고정.
3. **소스 메타 생성 [LLM 제안 + 스크립트 발급]** — citekey 발급(O_EXCL), CSL 필드, 루트 기준 경로.
4. **지식 추출·개념 페이지 갱신 [LLM]** — 신규 페이지 생성(영어 번역 슬러그 + O_EXCL, 관련 허브 연결 — 고아 lint 대응) + **기존 페이지 갱신이 본체**(1소스가 신규 포함 10–15페이지를 터치 — Karpathy 원문). claim은 각주+locator — locator는 각주 라벨 직전 괄호, 괄호와 라벨 사이 구두점은 폐쇄 집합 `.` `,` `:` 만(집합 확장은 반례마다 한 글자 추가가 아니라 재심 경유 — 증식 금지 §3), lint는 괄호 존재만 검사. 불확실 항목은 `#hypothesis`. **한국어 저작 규칙**: 확립 한국어 용어 우선(TTA·국어원 공인 참조), 미확립이면 원어 유지, **개념 첫 등장에 원어 병기**(예: 영속성(persistence)) — 역어가 흔들려도 원어가 불변 검색 키로 남는다(§8). **정의·정리·수치 등 왜곡 민감 구간은 번역 대신 원문 직인용**(인용 블록) — 의미는 원문이, 해설은 한국어가 담당.
5. **inbox 격리 [구조]** — 기계 산출물은 `<kb>/inbox/`에 런ID diff로 착지(synthesis 직행 금지). 이 시점까지 본 코퍼스 불변.
6. **validate 루프 [기계 게이트]** — 통과까지 수정 반복, 통과 전 진행 금지.
7. **커밋 [규약]** — 1런 = 1커밋 + `Ingest-Source:`/`Ingest-Run:` 트레일러. 실패는 inbox 잔류일 뿐 — 원자성.
8. **리뷰·머지 [인간 + 에이전트 브리핑]** — 아래 쓰기 정책. 리뷰는 에이전트 브리핑 경유(기계 검사 요약 + advisory 사전 검증 + 사람 판단 체크리스트 — 절차는 kb-ingest 스킬 ⑧이 정본). **리뷰 기준 = 무해성·구조**(각주 없는 claim·기존 claim 훼손·명백한 오류)이지 내용의 전수 정확성 검증이 아니다 — 정확성은 review-on-read가 사용 시점에 담당. 기준 축소가 처리량의 생존 조건(§8 — 사전 전수 심사는 Nupedia 실패 공식).
9. **재색인 [자동]** — qmd update(단일 직렬화) + 메타/edges 갱신 + 페이지 단위 무효화(§4.1) + 파편화 검출 → 사용자 사전 후보.

역방향도 동일 경로: kb-query의 종합은 5단계로, 웹에서 발견된 소스는 1단계부터.

**쓰기 정책 — 계층별 차등:**

- **sources/**: 인간 큐레이션.
- **concepts/**: LLM 기입 허용 + **diff 격리 리뷰**. 대응 2중: ① inbox도 인덱싱하되 `[unreviewed]` 라벨(보이는 저하) ② lint의 inbox 나이 경고. **사람 승인 없는 승급 경로는 없다** — 나이 기반 자동 머지 불채택(§6). 적체가 생겼을 때의 대응은 **미리 정하지 않는다**: 아직 발생한 적이 없어 처방의 근거가 없다. P90 경보가 그 시점을 계측하고, 무엇을 할지는 그때 사람이 정한다.
- **synthesis/**: 인간 저작·전수 리뷰. 경계 기준은 **provenance**(작성 주체·리뷰)이지 내용의 종합성이 아니다 — 분류 마비 방지.
- 전수 수동 게이트·무게이트 자동 기입·무작위 표본 감사(온도계로만) 모두 불채택.

### 4.5 멀티 KB 운용

- **기본형 = 단일 저장소 + 동형 KB 디렉터리 + qmd 컬렉션**(KB당 1개, 글로벌 인덱스 1개, `-c` 필터 + 무스코프 횡단 검색).
- **동거 시 공유 자산**: `schema/`·`tools/`·`evals/`는 저장소 1부 — **KB별 오버라이드 없음**. 스키마 분기가 필요하면 그것이 곧 저장소 분리 사유(§4.3 게이트 ⑶).
- **저장소 분리는 하드 경계에서만**(게이트 3문) 그리고 **비가역** — 재병합 절차는 없고 만들지 않는다. 분리 시: 공유 자산(schema/·tools/)은 시점 사본으로 복사하고 이후 동기화하지 않는다(분기가 분리 사유이므로 드리프트는 의도된 결과), 스킬은 사용자 레벨 1세트, citekey는 결정적 규칙 공유로 수렴.
- **KB 간 링크**: `qmd://<컬렉션>/<경로>` — 원칙 9에 의해 비권장. 존재하는 링크는 edges가 가시화하고 lint가 warn(§4.3). 상대 링크는 저장소 간 불가.
- **백업**: restic 저장소 1개 + `--tag` = KB 디렉터리명. 기밀 분리 시에만 저장소 분리.

### 4.6 평가 체계

| 용도 | 도구 | 조건 |
|---|---|---|
| 결정적 검색 평가 (recall@k·MRR, gold ID) | **ir_measures**(메트릭) + **pytest**(인수 게이트: 홉별 임계 단언·junit) + 자작(합성 코퍼스·탐색 확장 메트릭·홉 그룹 글루 — 기성에 없는 부분만) | qrels/run 빌더 공유 |
| 스킬 evals (kb-query 인용 정확도·출처 라벨 포함) | **dbt skill-eval** (커밋 `de68283` 핀, `uv tool install`) | 주의: 번들 플러그인 스킬 누출, macOS 키체인 전용 인증, 타임아웃 600s/60s 비설정, 실행당 실비용, 격리 tempdir에서 `--dangerously-skip-permissions` |

**스킬 evals 규약**: `evals/scenarios/<이름>/{prompt.txt, scenario.md, skill-sets.yaml}` + gitignore된 runs/. **baseline arm 의무**, 스킬당 ≥3 시나리오, evals를 스킬 본문보다 먼저 작성. 측정: 스크립트 단언 우선 → judge → baseline 대비 delta. **합격 숫자 게이트·CI 게이트 없음** — 인간 검토 비교 리포트로 종결, 스킬 수정 시 재실행. 트리거율 최적화 배터리·위험도 가중은 불채택(§6).

## 5. 백업·이관·토폴로지

**복구 모델**: 인덱스 **사본이 1차 복구 경로, 재빌드는 폴백**(1만 페이지 재빌드 1–3시간+, 새 기기 엔드투엔드 반나절 — 임베딩 스루풋 ~250–850 청크/분).

**qmd 상태 규약**: **글로벌 config(`~/.config/qmd/index.yml`) 사용** — 컬렉션은 전역 레지스트리라 임의 디렉터리에서 검색 가능("search any collection from any directory"). in-repo `.qmd/` 모드는 불채택(§6 — cwd 상향 탐색이라 저장소 밖 조회 불가). 글로벌 config는 **layout.yaml에서 재생성 가능한 파생물**(등록은 kb-new·복구 스크립트가 수행) — 커밋·백업 불요. 모델 GGUF 3개(~2.1GB)는 **벤더링 후 로컬 경로 참조**(hf: URI는 리비전 핀 불가).

| 데이터 클래스 | 1차 | 이중화 | 무결성 |
|---|---|---|---|
| git 텍스트 | 로컬 클론 | GitHub + NAS bare 원격 + 분기 `git bundle --all` → B2. GitHub 2FA 분실은 공식 복구 불가 — 로컬 클론+SSH가 1차 방어 | `git fsck` |
| `*/archive/` 블롭 + GGUF 3개 + qmd 타르볼 | 로컬 평문 | restic → B2 + NAS(SFTP/rest-server `--append-only`) + 외장 디스크, 평문 사본 1부. git-lfs 불채택 | `restic check --read-data-subset` 자동화 + 연 1회 전수. restic 정적 바이너리 동봉 |
| SQLite 인덱스 | 사본(분기, qmd 버전 라벨 — 동일 버전으로만 열기) — 라이브 cp 금지, `VACUUM INTO`/Backup API만 | 재빌드 폴백: `qmd update && qmd embed` | 복원 후 `qmd status` + 테스트 검색 |

**타깃 가동 순서 (2026-08-09 결정)**: ① NAS rest-server 컨테이너 `--append-only`(즉시 — 탈취된 클라이언트의 스냅샷 삭제 방어. 스택 정의 정본 = `alteralab/portainer` private repo, Portainer Repository 빌드 — 웹 에디터 드리프트 금지) ② B2(이연 — 2026-08-09 사용자 결정. 실노출은 `archive/`뿐: git 텍스트는 GitHub이 오프사이트 담당, GGUF·인덱스는 재생성물. **재심 트리거 = ingest 본격화로 archive 성장 시** — 그때 archive만 B2로 가는 최소 구성도 가능) ③ 외장 디스크·평문 사본 1부(미보유 — 보류, 확보 시 가동). 비밀번호 파일 `~/.restic-pass`(생성 완료 — **비밀번호 관리자 + 종이 사본 등재는 사람 몫, 분실 = 전체 복구 불가**), 정적 바이너리 0.19.1 동봉 완료.

**restic 채택 확정 (2026-08-09, 대조 심사 — §8)**: borg(안정판은 원격=SSH `borg serve` 전제라 B2 결격, 2.0은 베타·일정 없음)·kopia(무결성 트랙레코드 — data-loss race 수정 이력·append-only 서버 부재)·duplicacy(비OSS 사설 라이선스) 기각. restic 고유 우위 = **공개 포맷 명세 + 독립 구현체 2개**(rustic이 동일 repo를 상호 읽고 씀 — 도구 사망과 데이터 접근의 분리). **승계 트리거**: restic 12개월 무릴리스 또는 유지자 팀 해체 → rustic 승계 검토(포맷 동일이라 데이터 이동 0, 게이트 = rustic의 베타 탈출·회귀 테스트 확보).

**새 기기 복구 런북**: ① Homebrew + `brew install sqlite`(시스템 SQLite는 확장 로딩 불가) ② 네이티브 arm64 Node LTS ③ 벤더링 qmd 타르볼 설치 ④ GGUF 복원 ⑤ `git clone` → qmd 컬렉션 재등록(layout.yaml 기반) ⑥ 사본 복원+검증 / 폴백 재빌드 ⑦ qmd MCP 전역 등록 + 스킬 심링크(`~/.claude/skills/`) 생성 + 사용자 레벨 훅 + `git config core.hooksPath core/tools/githooks`(커밋 게이트 활성). 툴체인 핀 갱신은 연간 항목.

**배포 토폴로지**:

| 기기 | 역할 |
|---|---|
| MacBook (주 작업기) | 작업 사본 + 로컬 인덱스 + qmd stdio. **SQLite·git 작업 사본의 NAS 배치 금지**(네트워크 FS 잠금 손상 — 하드 제약) |
| NAS | git bare 원격(SSH — GitHub의 증강, 대체 아님) + restic 타깃(SMB 마운트 금지, SFTP/rest-server) + archive 복제 |

Syncthing류는 백업 아님(삭제 전파). 기기 교체 시 개선되는 것은 클론·복원 속도이고, 인덱스 로컬 재빌드·모델 재다운로드는 불변.

## 6. 구축·검증·운영

구조: **구축(일괄) → 수용 검증(인수 테스트) → 운영(일정 기반)**. "도달 시 만든다"는 단계는 없다 — 나머지는 일정 기반 운영이거나 명시적 불채택이다.

### 구축 (1회성 일괄 — 콘텐츠 디렉터리는 만들지 않는다)

- git init, 루트 골격: `.gitignore`, `schema/`(per-type 스키마 + `layout.yaml` + `user-dict.yaml` + `migrations.md`), `SCHEMA.md`, 루트 `overview.md` 라우터 초안.
- **tools/**: ① validate — JSON Schema + 관계 규칙 + layout 완전 분할 + 결번 키 대조, pre-commit·ingest 양쪽 실행 [A] ② lint [A] ③ rename [A] ④ kb-new [A] ⑤ affected [B] ⑥ 한국어 형태소 레그 CLI [B] ⑦ frontmatter 메타 테이블 [B] ⑧ edges + backlinks/neighbors [B] ⑨ 멀티홉 평가 하네스 4종 + ir_measures·pytest 게이트 [B].
- 스킬 6종 → `.agents/skills/` 정본 + `~/.claude/skills/` 심링크 + 사용자 레벨 UserPromptSubmit 훅. evals 시나리오는 스킬 본문보다 먼저.
- **qmd**: 글로벌 config 컬렉션 등록(layout.yaml 파생), 임베딩 Qwen3 잠정, GGUF 벤더링+로컬 경로, 데몬 모드, 버전 핀+타르볼.
- 백업 가동: GitHub push + NAS bare, restic init(SFTP/rest-server), bundle 스크립트, restic 정적 바이너리 동봉.
- **완료 게이트 = kb-new 첫 실행**(첫 KB 생성 — 수용 검증의 개시이자 kb-new의 첫 실전).

### 수용 검증 (첫 30–50개 소스 — 완성된 시스템의 인수 테스트)

- kb-new로 첫 KB 생성 → 도서·논문·docs 3타입 전부 ingest — 타입별 필드·개념 페이지 갱신 워크플로 검증. 스냅샷 습관화.
- 검색 실측 8종: ① 한국어 조사 변형·2음절·복합명사·활용형(음절 vs 형태소 레그 → 융합 가중치) ② 임베딩 A/B(KURE-v1 vs Qwen3 → 핀) ③ qmd 콜드/웜 레이턴시 ④ 1–2음절 부분토큰 ⑤ qmd 편집 시 고아 벡터 누수 ⑥ 멀티홉 하네스 실코퍼스 재측정 ⑦ 벡터 레그 기여도(무시 가능 시 FTS 전용 강등) ⑧ **허브+backlinks 스코프 질의가 태그 부재를 보상하는지**(§6 불채택 표 태그 항의 재심 데이터).
- 복구 드릴 양방향: 사본 복원(1차) + 전체 재빌드(폴백).
- diff 리뷰 부하 실측 — **첫 배치 4런 수행, §8 기록. 적체 0**. 사람 판단 시간의 분리는 미완: 에이전트 작업이 같은 구간에 섞여 git 타임스탬프로는 못 가른다 → 필요해지면 stats DB에 런 지표(PLAN §3이 이미 지정, 미구현). 스킬 평가 스킬당 3개+(kb-query의 KB-first 준수·출처 라벨 중점).
- 신규 규약의 실전 검증(2026-08-10 설계분): 리뷰 템플릿 2종(스킬 ⑧ templates/), stale_after 근거 각주, 부패 실사례 관측(→ §8 휘발성 클래스 재심 트리거).

**실행 계획 (2026-08-10 수립)**. 진행 상태는 여기 적지 않는다 — 산문 카운터는
반드시 썩는다(실측: "도서 2권, 38 concepts"가 9소스 149건 시점까지 잔존, 2026-08-12
발견). 정본은 조회다: 소스 = `git log --grep Ingest-Source`, 페이지 수 = `validate`
출력, 런 계측 = stats.sqlite events.

- **소스 배분** (목표 30–50): 도서 8–12권(사용자 조달 — 원서 우선 §4.4-①, ingest에 실파일 PDF/EPUB 필수) + 논문 10–20편(에이전트가 오픈액세스 조달) + 기술 문서 5–10건(docs-mirror 승격 경로 — 미러 기보유).
- **도서 선정 기준**: ⑴ 도메인 다양화 — DW 기존 2권 외 분산 시스템·스트리밍·DB 내부·데이터 아키텍처·analytics engineering·SWE 일반 ⑵ 휘발성 스펙트럼 혼합 — foundational만으로는 stale_after·버전 조건·부패 관측이 검증 불가, 버전 종속 실용서 2–3권 포함 ⑶ 한국어 소스 1–2권(형태소 레그 실측 대비).
- **배치 순서**: 첫 배치 3–4권 → 권당 diff 리뷰 부하 실측 → 페이스 확정 후 나머지 배치. 일괄 투입 금지 — 리뷰가 병목이면 inbox 파산.
  - **첫 배치 완료(2026-08-10, 4권 37초안 — 실측은 §8)**: 페이스는 **런당 즉시 리뷰 유지**(적체 0이라 배치를 키울 근거가 없다).

### 운영 캘린더

| 주기 | 작업 |
|---|---|
| 주간 | kb-lint 실행·리포트 확인 |
| 격주 | inbox diff 배치 리뷰 — 합산이 30–45분/2–3주 예산 내인지 기록 |
| 분기 | compaction: 스텁 병합(후보 식별 = 메타 DB 콘텐츠 길이 + overlap 큐, 판단 기준 §2.6)·redirect 체인 붕괴·(선택) FTS5 `optimize`(automerge가 기본 처리 — 저비용 마무리). `git bundle` → B2, index.sqlite 사본(VACUUM INTO·버전 라벨), 재빌드 드릴 |
| 연간 | 백업 전수 검증 + 매체 점검, 임베딩 모델 재평가(교체 시 blue/green), qmd·Node 툴체인 핀 갱신 검토 |
| 수시 | 스킬 수정 시 해당 skill-eval 재실행. 스키마 변경 전 `tools/affected` 실행 + migrations.md 기록 |

restic 백업은 cron 자동화 — 캘린더는 사람 작업만. **운영 임계 경보(tripwire)**(stats DB에서 **KB별 집계** — 전역 집계는 방치된 KB를 희석. 임계값은 자체 상수로 시작해 운영 데이터로 보정 — §8): search-miss > 직전 20회 중 4회 → 검색 설정 점검 / inbox 나이 P90 > 30일 → 적체 발생 신호(대응은 그때 사람이 정한다 — §4.4) / lint 오류 > 50건 → 유지보수 세션. 위반 = 주기 작업의 우선순위 지시, 신규 구축 트리거 아님.

### 불채택 표 (기각 근거 + 재심 조건 — 대기 작업 아님)

| 불채택 | 기각 근거 | 재심 조건 |
|---|---|---|
| **태그**(frontmatter tags·통제 어휘) | md-first 스펙 0/7 규정·장기 운영자 수렴(폐기·축소)·Luhmann 색인 희소성(3.2k 항목/67k 노트)·전역 어휘는 rename 도구 없이 오염(CONFCLOUD-7681, 19년 미해결). 잔존 가치(상태·유형)는 스키마 필드가 이미 담당, 주제 슬라이싱은 허브+backlinks | 수용 검증 ⑧·운영 실측에서 허브+backlinks 스코프 질의 실패 확인 시 |
| **나이 기반 자동 머지**(저위험 diff의 N일 경과 자동 승급) | 사용자 결정(2026-08-11): 사람 승인 없는 승급 경로를 두지 않는다. 근거 3중 — ⑴ 생태계 무선례([실험] 등급의 원래 사유. 독일어판 자동 승급은 사람 신뢰 기반이라 다른 메커니즘) ⑵ 첫 배치 4런 실측에서 **적체 0**이라 소비자 부재(§8) ⑶ "저위험 diff"를 기계가 판정해야 하는데 그 판정이 곧 리뷰다. **대체 처방도 두지 않는다** — 발생한 적 없는 상황에 대한 대응을 미리 짜는 것이 이 기능을 만들었던 그 오류이므로 반복하지 않는다 | 없음 — 재도입하려면 승급 게이트의 전제부터 재심 |
| **허브 본문 YAML 온톨로지 블록** | LLM 파싱 실측 12시행(§8)에서 정형 md 링크 리스트와 완전 동률(이득 0) — 결정성 변수는 포맷이 아니라 문법 계약. 펜스 내 경로는 링크 그래프(edges·rename·lint) 불인식(코드 확인), 이중 표현 표류는 MkDocs nav·SKOS의 성문 실패 패턴. llms.txt("LLM이 읽을 파일이라 md 채택")·Google OKF 모두 허브=md 링크 리스트 | 코퍼스 확대 재실측에서 정형 md(§2.6 문법)가 구조화 블록 대비 열세 관측 시 |
| **ADR**(`type: decision`·NNNN 번호) | ADR 서식지는 코드 저장소(표본 14/14)·ThoughtWorks "in source control, instead of a wiki"·KB 스펙 0/7·번호의 존재 이유(코드 상호 참조)가 1인 KB에 부재. KB 설계 결정은 본 문서 §8+migrations.md가, 지식 영역 결정은 일반 페이지(`superseded_by`)가 담당 | tools/가 별도 저장소로 추출될 때(§3 분리 신호) 그 저장소에 도입 |
| **ingest 추출의 텍스트 우선 경로**(비전 대체) | 도판·조판 정보 손실이 현 추출 품질 기준과 상충하고 비전 경로가 작동 중 — pdf-inspector 채택(2026-08-16)은 판정·우회 보조 경로에 한정 | 추출 토큰 비용이 실제 제약이 되는 대량 배치가 생기고, 도판 의존이 낮은 소스 유형이 분리 가능할 때 |
| **LLM-judge 답변 평가**(DeepEval·TruLens) | 실행 지점 부재 — 캘린더·수용 검증 어디에도 소비자 없음(설치만 규정된 인프라였음). 인용 정확도·출처 라벨은 스킬 evals 시나리오가 커버 | 답변 품질 회귀가 실사용에서 반복 확인될 때 |
| **자체 MCP 서버** | qmd 내장 MCP가 동일 표면 제공 — 중복 구축 | qmd MCP가 셸 없는 실사용을 못 덮을 때 || **NetworkX 배치 분석** | 유일 소비자(허브 식별)는 edges 링크 차수 SQL로 충분, 커뮤니티 검출은 소비자 0 (실측 이력: PageRank 2.1s·Louvain 분 단위 — 성능이 아니라 소비 부재가 기각 사유) | 그래프 분석 질의가 반복 작업화 |
| **그래프 파생 진입점**(LLM 추출→커뮤니티 위키 자동 생성 — graphify·GraphRAG 계열) | 저작형 KB 정본 진입 실사용 0건(자기 규정 용도: GraphRAG reports=global search 내부 입력, openwiki=git-diff 증분 유지보수이나 본문 정본은 항상 소스 코드 — 사람 정본 채널은 INSTRUCTIONS.md·PR 게이트로 한정(소스 검증), graphify=/raw 덤프 구조 발견). 리스크 3중: 커뮤니티 분할 불안정(Louvain 원논문 노드 순서 의존·Leiden 25%/16%·GraphRAG #741 증분 재검출), 추출 KG 커버리지(정답 개체 ~34% 부재), 재생성 모델(수동 편집이 정본 불가 — 원칙 1 충돌). 우리 edges는 **저작 링크의 파싱**이지 추론이 아님 | 커뮤니티 증분 안정성 + 저작형 KB 실사용 실증 시. **비구조 소스 뭉치의 사전 탐색(ingest 1단계 보조)·KB 위 임시 분석 뷰로는 지금도 자유**(파생물·소모품이라 규정 불요) |
| **kb-template + copier** | layout.yaml이 이미 골격 정본 — 템플릿은 이중 표현·드리프트 원천. kb-new가 layout.yaml에서 직접 생성, 저장소 분리 시엔 시점 사본 복사 | 없음 — 정본 이중화는 사유 불문 금지 |
| **스킬 트리거율 최적화 배터리**(run_eval.py 이식·16–20질의·60/40) | 명시 호출이 기본 워크플로(§4.3) — 부차 경로(암묵 발동)의 최적화 장치. 수치 자체는 skill-creator 원문 실증이나 전제(암묵 발동 의존)가 이 설계에 부재 | 명시 호출 마찰이 실사용 문제화될 때 |
| **Mac mini 역할**(Ollama 호스트) | 소비자였던 DeepEval judge·HippoRAG 엔드포인트 모두 불채택 — 무소비 하드웨어 역할 | HippoRAG 재심 시 그 채택 계약에 포함 |
| **qmd in-repo config 모드**(.qmd/ 커밋) | config 발견이 cwd 상향 탐색 — 타 프로젝트에서 KB 조회 불가. 이식성 목적은 layout.yaml 파생 재등록이 대체 | 전 기기에서 전용 세션만 쓰게 될 때 |
| HippoRAG2급 그래프 검색(상시 채택) | **성능이 1차 근거**: 단순 질의 이득 없음(HippoRAG2 자체 결과 동급이 최대, 선행 구조증강은 회귀 — §8)·그래프 우위는 과제 조건부(전역 종합·엔티티 멀티홉)·링크 탐색+반복 검색이 멀티홉 회수(§4.2·§8 외부 실증). 비용은 부차: O(corpus) LLM($10–20/1만)·쿼리 ~4× | 멀티홉 하네스 측정값이 실코퍼스 미달 + 에이전트 탐색 강화로도 미해결 |
| ANN 인덱스 | 이 코퍼스는 영구 flat 영역 | 청크 100만 초과(밀집 희석의 문헌상 유의 구간과 정렬 — §8) |
| point-in-time 검색 | git checkout + 재빌드로 충분 | 히스토리 질의가 월 단위 반복 작업화 |
| 컬럼 지향 레이아웃·B-tree/LSM 쓰기 증폭 튜닝·FORWARD 호환 | 전제(분석 스캔·쓰기 부하·구독자 다수)가 이 규모·기질에 부재(§8 이식 감사) | 전제 자체가 생기지 않는 한 없음 |
| `git blame` 행 단위 계보 표준 + `.git-blame-ignore-revs` | 실행 워크플로 부재 + 유발 커밋(대량 재작성) 희박 — claim 계보는 각주가, 런 계보는 트레일러가 담당 | 행 단위 계보 질의가 반복 작업화 |
| OKF export | 현재 소비자 0 + 드래프트 스펙. 구조는 OKF-native라 필요 시 근사 항등 변환(변환 목록: overview.md → frontmatter 없는 `index.md` 생성 — OKF §8이 자동 생성을 명시 허용) | OKF v1.0 + 실소비자 출현 |
| Meilisearch 전환 | 데몬 비용; 형태소 레그가 동일 역할 | 수용 검증에서 형태소 포함 구성이 한국어 recall 미달 |
| promptfoo·ranx | 실구동 비교 후 기각 — promptfoo: 1.6GB + Node 엔진 게이트 + 배열 카르테시안 함정; ranx: 380MB + 콜드 13초 JIT | 각 도구가 경량화되고 자작분 유지비가 문제화될 때 |
| qmd → 자체 sqlite-vec 스택 | qmd가 현재 최적 | 유지보수 중단 1년 or 레이턴시 상호작용 불가. 대체 시 음절 레그 자체 재구축 필요 |

## 7. 리스크 대응표

| 리스크 | 대응 |
|---|---|
| 유지비용 방치 (최대 리스크) | 반복 작업 스크립트화, diff 배치 리뷰, [실험] 등급의 킬 기준 부착 규칙(§8) |
| **영향 범위 망각** (1인 장기 운영의 1위 실패 모드) | `tools/affected` + lint 필드 사용률 검사 + migrations.md — 기억이 아니라 조회 |
| 기계 기입 드리프트·오염(주입 공격 포함) | inbox 격리 + diff 리뷰 + review-on-read 승급 + lint. 직접 기입은 문서화된 공격면(§8). 표본은 온도계로만 |
| 페이지 중복·비대화 | overlap lint, 500줄 백스톱 + TOC, redirect 스텁 |
| **크로스 KB 결합** | 원칙 9(자립성) + kb-new 게이트 협소 유지 + lint warn + edges 가시화 |
| 에이전트의 KB 미참조 | 명시 호출 1차 모드 + 훅 주입 — 암묵 발동에 의존하지 않는 설계 |
| inbox 파산 | 인덱싱+`[unreviewed]`(보이는 저하), lint 경고, KB별 P90 tripwire. 계측까지가 설계이고 대응은 발생 시 사람이 정한다 |
| tools/ 스크립트 부패 | Tier A 순수 파이썬·최소 의존·핀 / Tier B는 소모품. CommonMark 스펙 동결이 파서 교체를 보장 |
| 한국어 매칭 실패 | 형태소 레그(주력) + qmd 음절 레그, 질의 대칭 분석, 파편화 검출→사전 증분, 확장 없는 search/vsearch |
| qmd 단일 메인테이너 | 버전 핀+타르볼, 인덱스는 파생물, 형태소 레그가 키워드 폴백 |
| 확장 문법 락인 | GFM 부분집합 강제, lint 검사 |
| 개명·이동 링크 파손 | AST rename + 사후 링크 검사 게이트 |
| 외부 참조 부패 | 스냅샷 + custom.archive-url |
| 인덱스·도구 수명 | 소모품 원칙 — 코어는 CLI 스크립트, 스킬/MCP는 얇은 래퍼 |
| 기기 분실/교체 | §5 런북. 로컬 클론 + NAS/B2 다중 사본 |
| 스펙 미성숙 (OKF·agentskills) | 어휘·구조 차용만, 종속 없음 |

## 8. 검증 원장

**정본은 `LEDGER.md`다** (append-only — 등급 체계·판정 전문·참고 출처 포함).
새 결정은 등급과 함께 LEDGER.md에 기록하고, 재검증에서 탈락한 결정은 §6 불채택
표로 옮긴다. 본문·코드가 인용하는 "§8 원장"은 그 파일을 가리킨다.

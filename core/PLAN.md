# Syntopicon 계획

IT 서적·논문·기술 문서를 10–20년 축적하는 개인 지식 베이스. 2026-08-02 기준 확정판.
결정별 검증 등급과 근거는 §8 원장이 정본이다. 본문은 결정과 규약만 기술한다.

**전제**: 초기 구축 비용(1회성)은 감수한다. 최소화 대상은 **반복 유지 비용**과 **코퍼스 크기에 비례하는 O(N) 마이그레이션 비용**이다.

## 1. 원칙

1. **md + git = source of truth.** 사람이 읽고 쓰는 유일한 계층. 파생물은 전부 여기서 재생성된다.
2. **마크다운 방언 = CommonMark + GFM 부분집합(테이블·각주).** wikilink 등 Obsidian 전용 문법 금지.
3. **지식의 단위는 개념 페이지.** claim은 페이지 안의 각주 달린 불릿이며, 여러 소스의 주장이 한 개념에 누적된다. claim별 supersession·stale·모순 처리는 각주 앵커 + lint로.
4. **파생 인덱스는 소모품.** 검색·임베딩·그래프·생성 목록은 md에서 전량 재빌드. 백업 대상은 빌드 스크립트 + 버전 핀 + 재빌드가 시간 단위인 인덱스의 사본(§5).
5. **구축·지연 판단 기준.** 데이터 계층 규약(스키마 의미론·링크 문법·저장 위치)은 소급 수정이 O(N)이므로 첫 파일 전에 확정. 파생물은 retrofit O(1)이므로 지연 사유는 반복 유지비 또는 기술 churn뿐.
6. **쓰기 정책은 계층별 차등**(§4.4). 전수 수동 게이트도, 무게이트 자동 기입도 아니다.
7. **부패 관리는 휘발성의 함수.** forgetting curve 없음. 명시적 supersession + `stale_after`. 외부 링크는 연 ~3% 부패하므로 로컬 스냅샷 필수.
8. **그래프 인프라 불채택, 그래프 질의 채택.** 큐레이션된 링크 위의 SQLite edges + 재귀 CTE로 충분(§4.2).
9. **최대 리스크는 유지비용.** 유지 예산 2–3주당 30–45분. 반복 작업은 결정적 스크립트로 내리고 LLM·인간은 판단에만 쓴다.

## 2. 스키마

### 2.1 개념 페이지 frontmatter

```yaml
---
type: concept          # 어휘: §2.3
title: Raft 읽기 경로   # 표시 전용, 유일성 비요구 (충돌 규칙 §2.5)
description: 한 줄 요약  # 소비자: overview 생성기·검색 스니펫·메타 테이블·스코프 pruning. 편집 시 재생성(title 충돌 구분 역할 보존)
tags: [distributed-systems, raft]
generated: { by: "claude-fable-5", at: "2026-07-31T05:00:00Z" }   # 인간 저작도 human:me 기록(부재="출처 불명")
sources:
  - { id: ongaro2014-raft, resource: /sources/ongaro2014-raft.md }   # 루트 기준 경로 (§2.4)
  - { id: web-xyz, resource: /sources/web-xyz.md }
# 값이 생길 때만 기록 — "부재 = 기본값":
#   status: deprecated          # 부재 = stable
#   verified: [{by: "human:me", at: "..."}]  # 부재 = unverified 계층. 빈 리스트 금지
#   stale_after: "2027-06-01"   # 부재 = 만료 없음(foundational)
#   superseded_by: raft-read-v2 # deprecated 전환 시에만
#   contradicts: [other-slug]   # 모순 상호 기록 — 소비자: kb-lint 쌍 목록(자동 해소 금지)
---

## 읽기와 quorum

- leader lease 없이는 읽기에도 quorum 왕복이 필요하다 (§5.4 기준).[^ongaro2014-raft]
- #hypothesis lease 시계 드리프트 한계는 실무 문제 사례가 드물다.[^web-xyz]

[^ongaro2014-raft]: Ongaro 2014, §5.4
[^web-xyz]: 해당 웹 소스, 절 표기
```

- **claim 귀속은 본문 각주** `[^citekey]`, locator(페이지·절)는 각주 텍스트에. frontmatter 중첩 locator 금지.
- **null 자리표시 금지**(파서가 null과 부재를 구분 못 함). `as_of`류 중복 필드 재도입 금지(사유는 schema/migrations.md에 기록).
- **epistemic 표기는 태그 토큰** `#hypothesis` / `#speculation`(무표기 = 사실 서술). 숫자 confidence 금지.
- **시간 해상도**: 이벤트(`generated.at`, `verified[].at`) = ISO datetime, 유효성(`stale_after`) = YYYY-MM-DD. 초 단위 transaction time은 git이 제공.
- **YAML 규약**: 날짜·datetime 값은 반드시 따옴표 문자열. 도구는 파일 통짜 load-save 금지(라운드트립이 파일을 재작성함) — frontmatter 수정은 대상 필드만.

### 2.2 소스 메타 (sources/)

- **type 1단 구조**: `book | article-journal | paper-conference | article(프리프린트) | webpage | post-weblog | speech | standard | report` (CSL 공식 enum 차용). 계층(소스/개념/종합)은 type 어휘 분할표로 표현하고 validate가 type↔디렉터리 정합을 검사.
- **필드명은 CSL-JSON 원어**: 대문자 `ISBN`/`DOI`/`URL`, 접근일은 `accessed`, arXiv ID는 `number` + `publisher: "arXiv"`, 제품 버전은 `version`(문자열), 컨퍼런스명 `event-title`, RFC는 `number`+`collection-title`+`authority`, 영상 러닝타임 `dimensions`. 영상 타임코드는 인용 시점 locator(`timestamp`).
- **확장 필드 2개만**: `snapshot`(로컬 스냅샷 루트 경로), `custom: {archive-url: …}`(웨이백 URL — CSL 공식 확장 봉투).

```yaml
---
type: book
title: "Designing Data-Intensive Applications"
author: [{family: Kleppmann, given: Martin}]
issued: 2017
publisher: "O'Reilly Media"
ISBN: "9781449373320"
edition: 1
snapshot: /archive/kleppmann2017-ddia/
snapshot_sha256: "..."     # ingest 시점 1회 기록(write-once) — 변조 증거, 소비자: lint
accessed: "2026-07-31"
---
```

- **citekey = 파일명 = `저자성last연도[-슬러그]`**, 문자 집합 `[a-z0-9_.-]`(콜론·공백·대문자 금지 — 각주 앵커 파손). 동일 저자·연도 충돌만 `-2` 접미 허용. **한국어 저자**: 소스에 인쇄된 영문 표기 우선, 없으면 생성 시점 RR 로마자화(발급 후 불변이 표기 불안정성을 흡수). Zotero 도입 시 Better BibTeX citekey 채택.

### 2.3 type 어휘 (동결)

| 파일 종류 | type |
|---|---|
| 개념 페이지 / 인간 저작 종합 | `concept` / `synthesis` |
| 소스 메타 | CSL 타입군(§2.2) |
| redirect 스텁(개명·병합 잔여물) | `redirect` — `superseded_by`가 대상 지정, lint의 체인 붕괴 대상·스텁 경유 링크 재작성 제안 |
| ADR | `decision` — Nygard status 매핑: proposed→`draft`, accepted→stable(부재), superseded→`deprecated`+`superseded_by` |
| overview.md·SCHEMA.md | `guide` |
| inbox/ 초안 | `concept` + `status: draft` |
| 허브(MoC) | `synthesis` + 태그 (전용 type 없음) |

### 2.4 경로·링크 규약

- **본문 링크 = 파일 상대 경로**(`../sources/x.md`) — GitHub·Obsidian이 합의하는 유일 형식.
- **frontmatter 경로(`sources[].resource`, `snapshot`) = 저장소 루트 기준**(`/sources/x.md`) — 인용하는 파일이 이동해도 불변. OS 절대경로(`/Users/…`) 금지.

### 2.5 ID 발급·동시성 규약

1. **발급 주체**: kb-ingest/kb-new가 제안, **validate가 강제**(전역 유일·문자집합·유사 충돌 경고). 수동 생성도 pre-commit validate 경유.
2. **발급 후 불변.** 개명·이동은 `tools/rename` 경유만: md AST 기반(markdown-it-py) 전 저장소 링크 재작성 + frontmatter 경로 처리 + redirect 스텁 생성 + 사후 링크 검사 게이트. heading 앵커는 자동 재작성하지 않고 lint가 검증. 불변성이 표기 불안정성을 무해화한다(생성 시점 일관성만 필요).
3. **개념 슬러그**: 영문 소문자 kebab(`[a-z0-9-]`), 전역 유일, ~80자 이하, 한글 파일명 금지(NFC/NFD·바이트 한도). 한국어 개념은 로마자화 금지 → **영어 개념명 번역**(확립 용어 우선, 없으면 짧은 영어 서술). title은 한국어 유지. **충돌은 의미 한정자로 해소**(`consistency-acid` vs `consistency-eventual`) — 숫자 접미 금지(예외: citekey `-2`). 날짜/번호 접두 금지 — `NNNN-` 접두는 `type: decision`에만 허용(type 기준, 경로 기준 아님).
4. **ADR 번호**: `NNNN-` 단조 증가·재사용 금지, 발급 = max+1. 오프라인 동시 발급은 git이 못 잡으므로(파일명이 다름) **validate가 NNNN 접두 유일성을 type 스코프로 검사(fail-loud)** — 커밋 시점 검사로 충분한 이유는 git index.lock이 같은 워크트리의 커밋을 직렬화하기 때문. 사전 보호가 필요하면 `.NNNN.lock` O_EXCL 예약.
5. **동일 기기 병렬 프로세스**: 파일명=ID인 슬러그·citekey는 도구가 **O_EXCL 생성(`open(path,'x')`) 의무** — fs 원자성이 유일성 게이트(전제인 로컬 FS는 §5 토폴로지가 보장). check-then-write 금지.
6. **기기 간**: 슬러그 충돌은 git `AA`(both added) 충돌이 감지기. citekey는 결정적 규칙으로 수렴하며 `-2` 결과는 파일에 데이터로 고정(핀). **중앙 발급 서비스 불채택** — md+git 밖의 제2 진실 원천 금지.
7. **ID 외 동시성**: ⓐ 재색인·`qmd update`는 단일 실행 직렬화(WAL은 단일 쓰기) ⓑ 텔레메트리는 git 밖 stats DB(§3)라 파일 경합 없음 ⓒ inbox diff는 런ID 명명 + O_EXCL ⓓ index.sqlite 사본은 라이브 cp 금지 → `VACUUM INTO`/Online Backup API ⓔ rename·compaction은 클린 워킹트리 확인 후 에이전트 세션과 비동시 실행 ⓕ git push(non-ff 거부)·restic(불변 블롭)·bundle(git 일관 스냅샷)은 무처방 안전.

### 2.6 페이지 위생

- **분할 1차 기준은 목적**: 한 페이지 = 하나의 질문. 분할 조건: 섹션이 다른 질문에 답하기 시작 + 자식이 자립 가능. 자식이 스텁이 되거나 부모 요약의 복제면 분할 금지.
- **크기는 lint 백스톱**: 500줄/~5k 토큰 초과 경고(자동 분할 아님). 100줄 초과 시 상단 TOC.
- **구조**: 파일당 H1 하나(제목 일치), 헤딩 레벨 건너뛰기 금지, 깊이 H3–H4 상한(H4 필요 = 분할 신호).
- 분할·병합 시 **redirect 스텁**을 남기고, 병합 시 각주 라벨 충돌은 스크립트가 네임스페이스 처리.
- 페이지 간 중복은 개념 단위에서도 만성 → **overlap lint(페이지 쌍 임베딩 유사도)를 1급 규칙**으로.

### 2.7 태그 거버넌스 (governed-open)

- 허용목록(`schema/tags.yaml`) 밖의 새 태그는 lint가 보고 → 사람이 승격/병합/기각. 동의어 병합 맵 유지.
- 명명: 영문 소문자 kebab, 단수. 의미론은 **object 태그**(노트가 "무엇에 관한 것인가"만). 중첩 1단계까지, 노트당 ~3–5개 경고.
- 역할 한정: 태그는 **결정적 슬라이싱**(스코프 질의·lint 선정·통계)만. 확률적 관련성은 검색·링크의 몫.
- epistemic 토큰(`#hypothesis`/`#speculation`)은 tags.yaml의 폐쇄 섹션 — governed-open 승격 대상 아님, 추가는 schema+migrations 개정으로만.

### 2.8 스키마 진화 — 동결 코어 vs 개방 확장면

additive 확장(새 optional 필드)은 안전하고, 의미론 변경은 O(N)이다. 의미론이 걸린 **동결 코어**(첫 파일 전 확정, 이후 불변):

1. `type` 어휘(§2.3)와 계층 분할표, "디렉터리는 뷰, type 정본은 frontmatter"
2. 파일명=ID 규칙·문자 집합·충돌 해소·title 비유일
3. 링크·경로 문법(§2.4) + GFM 부분집합
4. 각주 = 출처 귀속 전용 채널, citekey 문자 집합
5. 날짜 의미론(이벤트=datetime, 유효성=date, 따옴표 문자열) + 부재=기본값
6. epistemic 토큰 폐쇄 어휘
7. 신뢰 계층 의미론(generated/verified, 승급 규칙)

- 코어는 **per-type JSON Schema(YAML 저술) + 파이썬 관계 규칙의 2층**으로 기계화되어 validate가 강제한다(관계 규칙 — citekey↔각주 정합·경로 실존 — 은 JSON Schema로 표현 불가). 산문 SCHEMA.md는 설명서일 뿐이며 에이전트가 산문 규칙을 따른다고 가정하지 않는다.
- **모든 필드는 소비자(읽는 도구·질의)를 명시해야 하며 소비자 없는 필드는 도입 금지.**
- **임의 확장(dbt `meta:` 상당)**: OKF unknown-key 허용(최상위 additive) + 소스 계층 `custom:` 봉투 + JSON 컬럼→expression index 승격. 향후 신규 개인 필드는 `x_` 접두 또는 `custom:` 봉투(미래 스펙 키 충돌 방지; 기동결 확장 키 `superseded_by`/`snapshot`은 불변 규칙상 소급 제외).
- **레지스트리**: `schema/*.yaml` = 현재 스키마, `schema/migrations.md` = append-only 변경 로그(날짜·구→신 매핑·의미 주석). **호환 정책 BACKWARD_TRANSITIVE**: additive만, in-place 개명 금지(새 키 + 매핑 기록 + 선택적 backfill), **은퇴 키 이름 영구 결번**. per-file schema_version 기록 금지(파일은 재작성되지 않으므로 거짓말하는 필드가 됨) — git 커밋 날짜 + migrations.md가 해석을 제공.

## 3. 저장 구조

```
syntopicon/
  SCHEMA.md            # 규약 설명서 (규범은 schema/*.yaml — 기계 게이트가 정본)
  schema/              # per-type 스키마 + tags.yaml + user-dict.yaml(소비자: 색인 CLI) + migrations.md
  CLAUDE.md, AGENTS.md # 훅 없는 하네스용 1줄 규칙 사본 (Claude Code는 UserPromptSubmit 훅이 주입 경로)
  overview.md          # 에이전트 진입점, ~1–2k 토큰 상한, llms.txt 구조:
                       #   H1 → 인용구(요약+검색 우선 규칙) → 규약 요지 → ## Hubs(10–30) → ## Tools → ## Optional
  inbox/               # 기계 기입 격리 (§4.4). 검색 인덱스에 포함하되 [unreviewed] 태그
  sources/             # 소스 메타 md — ingest 연도 샤딩
  concepts/            # 개념 페이지 — 지식 본체
  synthesis/           # 인간 저작 계층 (경계 = 작성 주체·리뷰, 내용 아님)
  synthesis/decisions/ # ADR (type: decision이 정본, 디렉터리는 뷰). 인스턴스 결정만 —
                       #   tools/가 엔진으로 추출되면 범용 엔진 ADR은 동반 이동
  tools/               # 결정적 CLI. Tier A(md 변경 — rename/validate/lint): 순수 파이썬(markdown-it-py)·최소 의존·핀.
                       #   Tier B(소모품 인덱스 빌더): 무제약
  .agents/skills/      # 정본 스킬 4종 (다중 저장소 분리 시 사용자 레벨 1세트 — §4.6)
  .claude/skills/      # 복사 동기화 산출물 (심링크 금지 — Windows 파손)
  .qmd/                # index.yml은 커밋(config-as-code), index.sqlite는 ignore
  kb-template/         # copier 템플릿 — KB 저장소 분리 시 별도 저장소로 승격
  evals/               # 스킬 평가 시나리오 (runs/는 ignore)
  archive/             # 소스 원문 스냅샷 — git 제외, §5 백업 체계로 보존
  .gitignore           # archive/, *.db, *.sqlite, .claude/skills/, evals/runs/
```

- **운영 로그는 git에 넣지 않는다.** 텔레메트리(search-miss·런 지표·lint 결과)는 **로컬 stats DB**(파생 SQLite, 보존·만료 정책, 소실 허용). 이벤트 저널은 git 히스토리 + 커밋 트레일러가 담당(`git log --grep Ingest-Source`). OKF log.md는 export 시 히스토리에서 생성.
- **저장물 수명 주기 3분류**: ① 영구 축적(git — sources/concepts/synthesis/decisions, 샤딩·compaction 규칙 §4.5) ② 일시 격리(git — inbox/, 리뷰 후 소멸) ③ 텔레메트리(git 밖 — stats DB). 무기한 쌓이기만 하는 디렉터리는 없다.
- **저장소 구조 = 콘텐츠 + 인스턴스 글루 동거, 엔진은 외부.** 엔진(qmd·DeepEval·ir_measures·skill-eval)은 외부 설치·핀이고, 저장소 안에는 이 스키마에 결합된 글루(tools·스킬·evals)만 둔다. 원자적 커밋(스키마 마이그레이션 = content+schema+validate 동일 커밋)이 동거의 실질 근거. **분리 발동 신호**: tools/ 커밋이 콘텐츠 커밋을 지배(참조점 1:2.9)하거나 tools/가 두 번째 소비자를 얻을 때 — 그 전 추출 대상 없음(kb-template만 두 번째 KB 등장 시 승격).
- SCHEMA.md·overview.md도 frontmatter `type` 보유(OKF: 예약 파일명 외 전 .md는 typed frontmatter).
- 디렉터리당 ~1–4k 파일 상한. 어떤 질의 차원도 경로에만 존재 금지. 샤딩 규칙 변경은 신규 파일에만 — 대량 이동 금지.

## 4. 파이프라인과 도구

### 4.1 진입점과 검색

**진입점 — 전체 카탈로그 없음, 검색 우선.** 전 페이지 카탈로그는 수백 페이지 너머에서 토큰 낭비이자 비어휘 매칭 한계에 걸린다(1만 페이지 ≈ 20만 토큰; 32k부터 성능 반토막). 대체: ① `overview.md`(~1–2k 토큰) ② synthesis 허브가 MoC 역할 ③ 검색 도구가 1차 경로 ④ 필요 시 디렉터리별 자동 생성 목록.

**검색 스택 — qmd + 자체 레그 2종.**

- **qmd 채택**(SQLite FTS5 + 로컬 GGUF 임베딩 + RRF + 리랭크 + CLI/MCP + SHA-256 증분 색인; 인덱스는 파생 SQLite라 락인 0). **버전 핀 고정** + `npm pack` 타르볼 보존(bus factor 1 완화). 폴백 사다리: basic-memory(md-first 대안 1순위) → Meilisearch(한국어 형태소 recall 미달 시만) → LEANN(시맨틱 보조). 임베딩은 Qwen3-Embedding-0.6B 잠정, 수용 검증 A/B(vs KURE-v1) 후 핀(bge-m3-ko는 KURE 열세로 A/B 제외). 한국어 질의는 확장 없는 `search`/`vsearch`(질의 확장의 영어 편향 회피). 데몬 모드로 모델 웜 유지.
- **벡터 레그의 존치 조건**: grep 우위 실증은 코드·어휘 일치 질의 대상이고, 산문 패러프레이즈·한국어 표면형 변형이 벡터의 잔존 근거다. 기여도는 수용 검증 A/B로 측정 — 무시 가능이면 FTS 전용 강등. **파이프라인 RAG 층 금지** — 에이전트가 도구를 고르는 구도를 유지한다.
- **자체 레그 ① 한국어 형태소 FTS**: Kiwi 분석 → 공백 join → FTS5 unicode61 테이블. 필수 사양: **질의 시점 대칭 분석**(질의도 동일 Kiwi+동일 POS 필터로 phrase 변환), **POS 필터 = 명사류+SL/SH/SN+용언 어간+XR**(nori STOP_TAGS 정합), **사용자 사전 필수**(`schema/user-dict.yaml` 시드 + 색인 파이프라인의 파편화 검출로 증분 관리, 사전 변경 시 재색인), compound는 성분 분해+phrase 질의(mixed 원형 색인은 랭킹 부스트 선택사항). 음절 substring은 **qmd 내장 레그를 그대로 사용**(부분토큰·형태소 실패분 담당). 영문 부분문자열은 `rg` 직접 실행이 폴백.
- **자체 레그 ② frontmatter 필터**: type/tags/status/stale_after 스코프 질의용 SQLite 메타 테이블(qmd는 frontmatter 미파싱). `[unreviewed]` 판정도 여기서 파생(inbox 경로 + `verified` 부재).
- **결과 형식**: `(파일, 헤딩 앵커, 라인, 1–3문장 스니펫, 헤딩 계보)` — 섹션 → 페이지 순 확장. 융합 리스트 + 채널 태그 `[fts]`/`[vec]`/`[both]`, concise 기본.
- **edges 테이블**: 링크 파싱 → `backlinks`/`neighbors(k)`, 탐색 깊이 상한 4(실측: 10만 노드/100만 엣지 depth-3 중앙값 1.97ms, depth-5 218ms). 커뮤니티·허브 분석은 NetworkX 배치 캐시(PageRank 2.1s; Louvain ~4분 — 분기 배치 용도, 수십 초가 필요해지면 igraph급으로 교체).

### 4.2 멀티홉 승급 사다리 (선검증 완료)

멀티홉 품질 판단은 체감이 아니라 **평가 하네스의 측정값**이다(gen_corpus/build_edges/eval_retrieval/graph_batch — tools/ 편입, 수용 검증에서 실코퍼스 재측정).

- **1단 — 에이전트 링크 탐색**: 합성 실측에서 flat 검색이 2/3-hop 0/10인 반면, top-3 시드의 k-hop 확장이 2-hop k=1·3-hop k=2에서 10/10 회수(확장 집합 중앙값 k=2 ≈ 32, k=3 ≈ 90페이지). 한계: 심긴 체인 실험이라 상한 추정 — 실코퍼스 재측정이 판정.
- **2단 — NetworkX 배치**: §4.1 수치. 
- **3단 — HippoRAG2 (불채택 상태의 검증된 비상 경로)**: `index(docs)`에 md 직접 투입 가능, 증분 색인·삭제 지원, 비용 O(corpus)(1만 페이지 ≈ $10–20/수 시간, API 모델 기준; 쿼리 오버헤드 plain RAG 대비 ~4×, 단순 질의 무회귀). 채택 계약: 검증 시점 커밋 SHA 핀, 발동 시 레포 펄스 재확인, PyPI 말고 git SHA 설치, 사멸 시 포크. 발동 조건은 §6 불채택 표.

### 4.3 스킬 4종

판단 불필요 로직은 전부 tools/ 스크립트로, SKILL.md는 워크플로·판단 기준만. agentskills.io 코어 스펙 내에서만 작성(도구별 확장 frontmatter 금지).

- **kb-ingest**: §4.4 파이프라인 1–7단계의 실행자 — 인간 판단(1)은 대화, 기계 단계(2·3·6·7)는 tools/ 호출, LLM 단계(3·4)는 스킬 지침.
- **kb-query** (체크리스트): ① overview.md로 방향(최초 1회) → ② qmd + 한국어 CLI 검색 → ③ 히트 섹션→페이지→링크 이웃 확장 → ④ 공백 평가(미스는 `search-miss` 이벤트로 stats DB 기록) → ⑤ 공백에 한해 웹 검색 → ⑥ 답변에 출처 라벨(KB/웹/`[unreviewed]`) → ⑦ 가치 있는 종합은 inbox/ 경유 저장. machine 계층 claim을 실사용 시 검증하면 `verified` 승급(review-on-read).
- **kb-lint** — 검사 매트릭스(검출만, 수정 커밋은 사람. validate=커밋 게이트, lint=전수 리포트의 역할 분담):

| 검사 | 데이터 소스 | 산출처 |
|---|---|---|
| 깨진 링크·redirect 경유 링크 | edges 테이블 | 리포트 + 재작성 제안 |
| 만료 `stale_after` | 메타 DB(partial index) | 재검토 큐 |
| 고아 페이지 | edges | 리포트 |
| 각주 없는 claim 불릿 / 각주↔sources.id 정합 | md AST | 리포트 |
| 페이지 overlap(중복) | 임베딩 | compaction 후보 큐 |
| `contradicts` 쌍 | 메타 DB | 연구 과제 큐(자동 해소 금지) |
| 스냅샷 누락 / `snapshot_sha256` 불일치 | 소스 메타 + archive/ | 리포트(변조 증거) |
| 문자집합·GFM 방언·500줄·TOC 부재 | md 스캔 | 리포트 |
| inbox 나이·크기 | 메타 DB | SLO(P90) + 리포트 |
| 허용목록 밖 신규 태그 | 메타 DB vs tags.yaml | 태그 승격 큐 |
| NNNN 유일성(전수 재확인) | 메타 DB | 리포트 |
| 형태소 파편화(연속 1음절 런) | 형태소 색인 | 사용자 사전 후보 큐 |
| ingest 커밋 트레일러 존재 | git log(interpret-trailers) | 리포트 |

  **실행 전략**: 주간 실행은 **증분**(직전 실행 이후 변경 페이지만 — overlap도 변경 페이지 × 전 코퍼스의 1×N 비교라 규모 무관). **전쌍 overlap은 부트스트랩과 분기 전수 검사에서만** — 10만 페이지 전쌍은 소박하게는 불가능(50억 쌍·40GB 행렬)하므로 블록 행렬곱으로 임계 초과 쌍만 보존(분 단위 배치, 산수 근거 — §8). **산출 스키마**: 검사 결과는 severity(error/warn/info)를 달아 리포트(사람·주간)와 stats DB(SLO·큐의 기계 소비) 이원 기록.
- **kb-new** (명시 호출 전용): ① **판단 게이트** — 심사 질문 고정: ⑴ 기밀·접근 통제 경계인가? ⑵ 별도 동기화/백업/공개 정책이 필요한가? ⑶ 둘 다 아니면 → 기존 KB의 최상위 디렉터리 + qmd 컬렉션으로 권고하고 종료(주제 분리는 사유 아님 — §4.6). ② **기계 단계** — `tools/kb-new`: copier 비대화형(-l -d kb_name·kb_purpose) + qmd 컬렉션 등록 + git init·초기 커밋, 비어있지-않으면-거부 가드. ③ **편입** — restic `--tag` 추가, 운영 캘린더·SLO 집계 대상 포함, overview.md 허브에 상호 링크.
- **발동 정책(공통)**: 산문 지시의 준수는 비보장이므로 (a) 명시 호출(`/kb-query`)이 기본 워크플로 (b) 1줄 포인터는 UserPromptSubmit 훅으로 주입(전달은 결정적, 복종은 확률적) (c) 암묵 발동은 수용 검증에서 측정. MCP는 셸 없는 클라이언트 전용(상시 ~8k 토큰 오버헤드 회피 — 얇은 `search_notes`/`read_note` 래퍼만).

### 4.4 Ingest 파이프라인과 쓰기 정책

**파이프라인** ([인간]=판단, [LLM]=제안, [스크립트]=결정적):

1. **소스 획득·큐레이션 [인간]** — 넣을 가치의 판단은 스크립트화 불가 영역.
2. **스냅샷 [스크립트]** — archive/ 저장 + `snapshot_sha256` 1회 기록. 소급 불가능한 유일 단계라 최전방 고정.
3. **소스 메타 생성 [LLM 제안 + 스크립트 발급]** — citekey 발급(O_EXCL), CSL 필드, 루트 경로.
4. **지식 추출·개념 페이지 갱신 [LLM]** — 신규 페이지 생성(영어 번역 슬러그 + O_EXCL) + **기존 페이지 10–15개 갱신이 본체**. claim은 각주+locator, 불확실 항목은 `#hypothesis`.
5. **inbox 격리 [구조]** — 기계 산출물은 inbox/에 런ID diff로 착지(synthesis 직행 금지). 이 시점까지 본 코퍼스 불변.
6. **validate 루프 [기계 게이트]** — 통과까지 수정 반복, 통과 전 진행 금지.
7. **커밋 [규약]** — 1런 = 1커밋 + `Ingest-Source:`/`Ingest-Run:` 트레일러. 실패는 inbox 잔류일 뿐 — 원자성.
8. **리뷰·머지 [인간]** — 아래 쓰기 정책.
9. **재색인 [자동]** — qmd update(단일 직렬화) + 메타/edges + 페이지 단위 무효화(청크 전량 재생성) + 파편화 검출 → 사용자 사전 후보.

역방향도 동일 경로: kb-query의 종합은 5단계로, 웹에서 발견된 소스는 1단계부터.

**쓰기 정책 — 계층별 차등:**

- **sources/**: 인간 큐레이션.
- **concepts/**: LLM 기입 허용 + **diff 격리 리뷰**. 대응 3중: ① inbox도 인덱싱하되 `[unreviewed]` 태그(보이는 저하) ② 저위험 diff(기존 claim 보강·오타)는 N일 경과 시 unverified 계층으로 **나이 기반 자동 머지**(리뷰 공백을 정상 케이스로 설계) ③ lint의 inbox 나이 경고. [실험] 등급 — 수용 검증에서 부하 실측, 예산(30–45분/2–3주) 초과 시 킬 기준: 자동 머지 범위 확대, 신규 claim·모순 diff만 리뷰.
- **synthesis/**: 인간 저작·전수 리뷰. 경계 기준은 **provenance**(작성 주체·리뷰)이지 내용의 종합성이 아니다 — 분류 마비 방지.
- 전수 수동 게이트(리뷰 효과 붕괴)·무게이트 자동 기입(드리프트 복리 전파)·5–10% 무작위 표본 감사(2% 오류 검출에 ~149건 필요 — 검출력 부족) 모두 불채택. 무작위 표본은 지속 오류율 온도계로만.

### 4.5 대규모 축적 규칙 (데이터 플랫폼 이식)

1. **Hidden partitioning**: 물리 배치는 구현 세부, 질의 인터페이스는 frontmatter. 질의 차원의 경로 단독 인코딩 금지, 샤딩 변경은 신규만, 대량 이동 금지. sources/는 ingest 연도 샤딩, 디렉터리당 ~1–4k.
2. **Compaction(분기)**: 임계 미만 스텁을 부모로 병합(리다이렉트 잔류), 5k 초과 페이지 분할 검토(목적 기준, 자동 아님), 리다이렉트 체인 붕괴, 대량 ingest 후 FTS5 `optimize`.
3. **Covering index**: 메타 테이블은 필터 필드만 실컬럼(type/status/dates/tags), 나머지 JSON 컬럼(→ expression index 승격 가능). Partial index: `stale_after IS NOT NULL`, `type='redirect'`. 스텁 식별은 stats의 콘텐츠 길이 계산.
4. **stats 테이블**: 태그 카디널리티·고아·부패 히스토그램·링크 차수 — 검색 전략 선택 + 건강 대시보드 + 운영 SLO 데이터.
5. **임베딩 모델 버전 = 스키마 버전, 호환 NONE**: 모델 id+리비전+차원+청킹을 인덱스 메타에 핀, 변경은 blue/green 전체 재빌드. 서로 다른 모델 벡터 혼합 금지(무경고 recall 붕괴).
6. **무효화 단위 = 페이지**: 편집 시 해당 페이지 청크 전량 재생성(부분 패치 금지). 5k 백스톱 덕에 페이지당 ≤6청크.
7. **frontmatter pruning은 휴리스틱**: description은 손실 요약이라 false-negative 가능 — 전문 FTS 폴백 상시 유지. description은 인덱스 통계로 취급, 편집 시 재생성.
8. **계보(DV 2.0 등가)**: 서지 원천 = `sources[]`+각주(claim 단위), 적재 시각 = git 커밋, origin 마커 = 보편 `generated.by`, 변경 감지 = git 내용 주소화. 행 단위 계보 질의 표준 = `git blame -w -M -C` + 커밋된 `.git-blame-ignore-revs`. 배치 ID = 1런 1커밋 + 트레일러(`git interpret-trailers --parse`로 lint). 스냅샷 변조 증거 = `snapshot_sha256`.
9. **파생물 소모품 증명**: md+git → 전체 인덱스 재빌드 1커맨드를 정기 드릴로 실행.

**불채택**: 컬럼 지향 레이아웃, B-tree/LSM 쓰기 증폭 튜닝, ANN 인덱스(이 규모는 영구 flat 영역), point-in-time 검색 인프라(히스토리 질의는 git checkout + 재빌드), 스키마 레지스트리 서비스, FORWARD 호환.

### 4.6 멀티 KB 운용

- **기본형 = 단일 저장소 + KB별 최상위 디렉터리 + qmd 컬렉션**(KB당 1개, `-c` 필터 + 무스코프 횡단 검색 + `context add`). 인덱스 간 횡단 질의는 불가능하므로 글로벌 인덱스 1개 유지. 다중 컬렉션 랭킹은 전역 top-K 후 필터 — `-n` 상향으로 완화.
- **저장소 분리는 하드 경계에서만**(업무 기밀·별도 동기화/백업 정책). 주제 분리는 사유 아님.
- **분리 시 공유 자산**: 스킬은 사용자 레벨 1세트(진짜 분기 시만 저장소 오버라이드), 스키마·도구는 copier 템플릿(3-way 머지 갱신; submodule 금지), citekey는 결정적 규칙 공유로 수렴.
- **KB 간 링크**: `qmd://<컬렉션>/<경로>` URI 또는 정식 URL(상대 링크는 저장소 간 불가).
- **백업**: restic 저장소 1개 + `--tag`로 KB 구분. 기밀 분리 시에만 저장소 분리.

### 4.7 평가 체계

| 용도 | 도구 | 조건 |
|---|---|---|
| 결정적 검색 평가 (recall@k·MRR, gold ID) | **ir_measures**(메트릭) + **pytest**(인수 게이트: 홉별 임계 단언·junit) + 자작(합성 코퍼스 생성·탐색 확장 메트릭·홉 그룹 글루 — 기성에 없는 부분만) | CLI 리포트는 별도 유지, qrels/run 빌더 공유 |
| LLM-judge 답변 품질 (kb-query 충실도·인용 정확도) | **DeepEval** (Ollama judge, 완전 로컬) | 버전 핀, `DEEPEVAL_TELEMETRY_OPT_OUT=1`, G-Eval 평가 기준은 한국어로 직접 저작, `evaluation_steps=` 명시(judge 호출 반감). 2순위 TruLens |
| 스킬 evals | **dbt skill-eval** (커밋 `de68283` 핀, `uv tool install`) + **Anthropic run_eval.py 이식**(트리거율 축) | 주의: 번들 플러그인 스킬의 skills_available 누출, macOS 키체인 전용 인증, 타임아웃 600s/60s 비설정, 실행당 실비용, 격리 tempdir에서 `--dangerously-skip-permissions` 사용 |

**스킬 evals 규약**: 저장소 레벨 `evals/scenarios/<이름>/{prompt.txt, scenario.md(목표/기대 행동/평가 기준), skill-sets.yaml}` + gitignore된 runs/. **baseline arm(스킬 없는 실행) 의무.** 스킬당 ≥3 시나리오, 위험도 가중(kb-ingest·kb-lint > kb-new). evals를 스킬 본문보다 먼저 작성. 측정: 스크립트 단언 우선 → LLM-judge(success/1–5/tool_usage) → 텔레메트리(토큰·비용·턴수) → baseline 대비 delta 집계. 트리거 테스트 분리: 스킬당 20질의(should 8–10 + near-miss should-not 8–10)·질의당 3회·60/40 분할·개선 ≤5회. **합격 숫자 게이트·CI 게이트 없음** — 인간 검토 비교 리포트로 종결, 스킬 수정 시 재실행.

## 5. 백업·이관·토폴로지

**복구 모델**: 인덱스 **사본이 1차 복구 경로, 재빌드는 폴백**(1만 페이지 재빌드 1–3시간+, 새 기기 엔드투엔드 반나절 — 임베딩 스루풋 ~250–850 청크/분).

**qmd 상태 규약**: 비파생 상태는 `index.yml` 하나 — **`qmd init` in-repo 모드로 `.qmd/index.yml`을 커밋**(collection add가 절대 경로를 기록하므로 새 기기에서 1회 수정 또는 재등록). 모델 GGUF 3개(~2.1GB)는 **벤더링 후 로컬 경로 참조**(hf: URI는 리비전 핀 불가).

| 데이터 클래스 | 1차 | 이중화 | 무결성 |
|---|---|---|---|
| git 텍스트 (`.qmd/index.yml` 포함) | 로컬 클론 | GitHub + NAS bare 원격 + 분기 `git bundle --all` → B2. GitHub 2FA 분실은 공식 복구 불가 — 로컬 클론+SSH가 1차 방어 | `git fsck` |
| archive/ 블롭 + GGUF 3개 + qmd `npm pack` 타르볼 | 로컬 평문 | restic → B2 + NAS(SFTP/rest-server `--append-only`) + 외장 디스크, 평문 사본 1부. git-lfs 불채택 | `restic check --read-data-subset` 자동화 + 연 1회 전수. restic 정적 바이너리 동봉 |
| SQLite 인덱스 | 사본(분기, qmd 버전 라벨 — 동일 버전으로만 열기) — **라이브 cp 금지, `VACUUM INTO`/Backup API만** | 재빌드 폴백: `qmd update && qmd embed` | 복원 후 `qmd status` + 테스트 검색 |

**새 기기 복구 런북**: ① Homebrew + `brew install sqlite`(시스템 SQLite는 확장 로딩 불가) ② 네이티브 arm64 Node LTS 확인 ③ 벤더링 qmd 타르볼 설치 ④ GGUF 복원 ⑤ `git clone` → `.qmd/index.yml` 경로 수정 ⑥ 사본 복원+검증 / 폴백 재빌드 ⑦ MCP 재등록. 툴체인 핀 갱신은 연간 항목(Node LTS EOL ~2–3년 주기).

**배포 토폴로지**:

| 기기 | 역할 |
|---|---|
| MacBook (주 작업기) | 작업 사본 + 로컬 인덱스 + qmd stdio. **SQLite·git 작업 사본의 NAS 배치 금지**(네트워크 FS 잠금 손상 — 하드 제약) |
| Mac mini | **Ollama 호스트**(`OLLAMA_HOST=0.0.0.0`): DeepEval judge + HippoRAG 엔드포인트. 배치 작업이라 LAN 오프로드 적합. qmd 데몬 호스트는 불채택(미단련 표면 + 무인증) |
| NAS | git bare 원격(SSH — GitHub의 증강, 대체 아님: 같은 재해 도메인) + restic 타깃(SMB 마운트 금지, SFTP/rest-server) + archive 복제 |

Syncthing류는 백업 아님(삭제 전파). 기기 교체 시 개선되는 것은 클론·복원 속도이고, 인덱스 로컬 재빌드·모델 재다운로드는 불변.

## 6. 구축·검증·운영

구조: **구축(일괄) → 수용 검증(인수 테스트) → 운영(일정 기반)**. "도달 시 만든다"는 단계는 없다 — 나머지는 일정 기반 운영이거나 명시적 불채택이다.

### 구축 (1회성 일괄)

- git init, 디렉터리, `.gitignore`, `schema/*.yaml` + `tags.yaml` + `user-dict.yaml` + `migrations.md`, `SCHEMA.md`, `overview.md` 초안.
- **qmd**: in-repo `qmd init`(index.yml 커밋), 임베딩 Qwen3 잠정 교체, GGUF 벤더링+로컬 경로, 데몬 모드, 버전 핀+타르볼.
- **tools/** (Tier A = 순수 파이썬 markdown-it-py + python-jsonschema / Tier B = 무제약): ① 한국어 형태소 레그 CLI [B] ② frontmatter 메타 테이블 [B] ③ edges + backlinks/neighbors(깊이 4) [B] ④ validate — JSON Schema + 관계 규칙 + 충돌 경고 + NNNN 유일성, pre-commit·ingest 양쪽 실행 [A] ⑤ lint [A] ⑥ rename(AST 링크 재작성 + 검사 게이트) [A] ⑦ (선택) 디렉터리 목록 생성기 [B] ⑧ 멀티홉 평가 하네스 4종 + ir_measures·pytest 게이트 [B].
- 스킬 4종 → `.agents/skills/` + `.claude/skills/` 복사 동기화 + UserPromptSubmit 훅.
- kb-template(copier) + `tools/kb-new` [A].
- evals/: 시나리오(스킬당 ≥3 + baseline) + skill-eval 설치(핀) + run_eval.py 이식 — 스킬 본문보다 먼저.
- DeepEval 설치(핀, 텔레메트리 옵트아웃) + Ollama judge 연결 + G-Eval 한국어 기준 저작.
- NetworkX 배치 분석 [B](stats 캐시, cron), overlap lint, MCP 서버 [B](셸 없는 표면용).
- 백업 가동: GitHub push + NAS bare 원격, restic init(SFTP/rest-server), bundle 스크립트, restic 정적 바이너리 동봉.

### 수용 검증 (첫 30–50개 소스 — 완성된 시스템의 인수 테스트)

- 도서·논문·docs 3타입 전부 ingest — 타입별 필드·개념 페이지 갱신 워크플로 검증. 스냅샷 습관화.
- 검색 실측 7종: ① 한국어 조사 변형·2음절·복합명사·활용형(qmd 음절 vs 형태소 레그 → 융합 가중치) ② 임베딩 A/B(KURE-v1 vs Qwen3 → 핀) ③ qmd 콜드/웜 레이턴시 ④ 1–2음절 부분토큰의 음절 레그 동작 ⑤ qmd 편집 시 고아 벡터 누수 ⑥ 멀티홉 하네스 실코퍼스 재측정 ⑦ 벡터 레그 기여도(무시 가능 시 FTS 전용 강등).
- 복구 드릴 양방향: 사본 복원(1차) + 전체 재빌드(폴백).
- diff 리뷰 부하 실측(예산 초과 시 §4.4 킬 기준 발동).
- 스킬 평가 스킬당 3개+(kb-query의 KB-first 준수·출처 라벨 중점).

### 운영 캘린더

| 주기 | 작업 |
|---|---|
| 주간 | kb-lint 실행·리포트 확인 |
| 격주 | inbox diff 배치 리뷰 — 합산이 30–45분/2–3주 예산 내인지 기록 |
| 분기 | compaction(§4.5-2), `git bundle` → B2, index.sqlite 사본(VACUUM INTO·버전 라벨), 재빌드 드릴 |
| 연간 | 백업 전수 검증 + 매체 점검, 임베딩 모델 재평가(교체 시 blue/green), 태그 어휘 정리, qmd·Node 툴체인 핀 갱신 검토 |
| 수시 | 스킬 수정 시 해당 skill-eval 재실행(`run`→`grade`→`report`) |

restic 백업은 cron 자동화 — 캘린더는 사람 작업만. **운영 SLO**(stats DB에서 kb-lint 집계; 위반 = 주기 작업의 우선순위 지시, 신규 구축 트리거 아님): search-miss > 직전 20회 중 4회 → 검색 설정 점검 / inbox 나이 P90 > 30일 → 자동 머지 발동 / lint 오류 > 50건 → 유지보수 세션.

### 불채택 표 (기각 근거 + 전제 무효화 조건 — 대기 작업 아님)

| 불채택 | 기각 근거 | 재심 조건 |
|---|---|---|
| HippoRAG2급 그래프 검색 | 링크 탐색이 멀티홉 회수(§4.2) + O(corpus) LLM 비용·쿼리 ~4× | 멀티홉 하네스 측정값이 실코퍼스 미달 + 에이전트 탐색 강화로도 미해결 |
| ANN 인덱스 | 이 코퍼스는 영구 flat 영역 | 청크 100만 초과 |
| point-in-time 검색 | git checkout + 재빌드로 충분 | 히스토리 질의가 월 단위 반복 작업화 |
| OKF export | 현재 소비자 0 + 드래프트 스펙. 구조는 OKF-native라 필요 시 근사 항등 변환 | OKF v1.0 + 실소비자 출현 |
| Meilisearch 전환 | 데몬 비용; 형태소 레그가 동일 역할 | 수용 검증에서 형태소 포함 구성이 한국어 recall 미달 |
| promptfoo(리포트 레이어)·ranx(IR 메트릭) | 실구동 비교 후 기각 — promptfoo: 1.6GB + Node 엔진 게이트(핀 22.17 거부) + 배열 카르테시안 함정; ranx: 380MB + 콜드 13초 JIT | 각 도구가 경량화되고 자작분 유지비가 문제화될 때 |
| qmd → 자체 sqlite-vec 스택 | qmd가 현재 최적 | 유지보수 중단 1년 or 레이턴시 상호작용 불가. 대체 시 음절 레그 자체 재구축 필요 |

## 7. 리스크 대응표

| 리스크 | 대응 |
|---|---|
| 유지비용 방치 (최대 리스크) | 반복 작업 스크립트화, diff 배치 리뷰, 예산 초과 시 킬 기준(§4.4) |
| 기계 기입 드리프트 | inbox 격리 + diff 리뷰 + review-on-read 승급 + lint. 표본은 온도계로만 |
| 페이지 중복·비대화 | overlap lint, 500줄/5k 백스톱, redirect 스텁 |
| 에이전트의 KB 미참조 | 명시 호출 1차 모드 + 훅 주입, 암묵 발동은 측정 대상 |
| inbox 파산 | 인덱싱+`[unreviewed]`(보이는 저하), 나이 자동 머지, lint 경고, P90 tripwire |
| tools/ 스크립트 부패 | Tier A 순수 파이썬·최소 의존·핀 / Tier B는 소모품. CommonMark 스펙 동결이 파서 교체를 보장 |
| 한국어 매칭 실패 | 형태소 레그(주력) + qmd 음절 레그, 질의 대칭 분석, 파편화 검출→사전 증분, 확장 없는 search/vsearch |
| qmd 단일 메인테이너 | 버전 핀+타르볼, 인덱스는 파생물, 형태소 레그가 키워드 폴백(음절 레그는 대체 시 재구축 — §6 불채택 표) |
| 확장 문법 락인 | GFM 부분집합 강제, lint 검사 |
| 개명·이동 링크 파손 | AST rename + 사후 링크 검사 게이트, 소문자 lint |
| 외부 참조 부패 | 스냅샷 + custom.archive-url |
| 인덱스·도구 수명(sqlite-vec pre-1.0 등) | 소모품 원칙 — 코어는 CLI 스크립트, 스킬/MCP는 얇은 래퍼 |
| 기기 분실/교체 | §5 런북. 로컬 클론 + NAS/B2 다중 사본 |
| 스펙 미성숙 (OKF·agentskills) | 어휘·구조 차용만, 종속 없음 |

## 8. 검증 원장

등급: **[검증]** 1차 출처·벤치마크·로컬 실측 / **[정황]** 수렴 간접 증거 / **[실험]** 근거 얇음 — 측정 계획·킬 기준 부착 / **[선택]** 표준 위임 영역의 자체 결정. 규칙: 새 결정은 등급과 함께 기록하고, [실험]은 측정 계획 없이 존재할 수 없다.

| 결정 | 등급 | 핵심 근거 |
|---|---|---|
| md+git 기질, GFM 부분집합, 소모품 인덱스 | [검증] | 장기 실증(gwern 16년·org-mode·Dendron 데이터 생존) + 반증 라운드 생존 |
| 개념 페이지 단위 (1claim=1파일 기각) | [검증] | 원자 노트 다년 실패 회고·루만 재해석·생태계 수렴(Karpathy·OKF·basic-memory) |
| frontmatter 필드 집합·부재=기본값·따옴표 날짜 | [검증] | OKF 스펙 대조 + PyYAML/yq/GitHub 렌더러 로컬 실측 |
| 각주=출처 귀속, citekey 문자 집합 | [검증] | GitHub 실제 렌더러 실측 |
| 소스 메타(1단 type, CSL 원어명) | [검증] | CSL-JSON 103속성 전수 대조 + 실소스 6종 수용 테스트 |
| frontmatter 경로=루트 / 본문 링크=상대 | [검증] | OKF §6.2 + 렌더러 실측 + Jekyll/Hugo/basic-memory 선례 |
| 스키마 2층(JSON Schema+파이썬) | [검증] | Astro/Docusaurus 관행 + JSON Schema 표현력 한계 + 로컬 실험 |
| 스키마 레지스트리 + BACKWARD_TRANSITIVE + 키 결번 | [검증] | Iceberg field-ID/Confluent 개념 이식(텍스트파일 번역은 [선택]) |
| type 어휘(redirect/decision/guide 포함) + ID 발급 규약 | [검증]+[선택] | 전 파일 종류 열거 감사. 영어 번역 슬러그·한국 저자 citekey는 [선택] |
| ID 동시성: O_EXCL 의무, ADR NNNN type 스코프 검사 | [검증-실기] | check-then-write 덮어쓰기 재현 + O_EXCL fail-loud 실증 + adr-tools 문서화된 구멍 |
| 중앙 ID 발급 불채택 | [검증] | ClickHouse 무시퀀스·Snowflake 무중앙호출 원문 + 개인 KB 선례 전무 |
| ID 외 동시성(재색인 직렬화·VACUUM INTO·런ID) | [검증] | SQLite 공식(라이브 cp 손상·백업 API) + qmd busy 이슈 |
| 분할 1차 기준=목적, 크기 백스톱 | [검증] | Diátaxis·WP:SPLITTING·EPPO 일치. 500줄 수치 자체는 [정황] |
| 파일명 규칙(kebab·80자·한글 금지·무접두) | [검증] | Google 스타일 가이드·바이트 한도·NFC/NFD·Jekyll/ADR 대조 |
| 태그 governed-open | [검증]+[선택] | 폭소노미 붕괴·NN/g 유지 비용 양방향; 단수·개수 상한은 [정황] |
| `#hypothesis` 토큰 | [정황] | 구문 울타리 패턴은 선례(citation-needed·RFC 2119), 표기 자체는 선택 |
| 전체 카탈로그 폐기, overview+검색 우선 | [정황] | NoLiMa·llms.txt 실측·Wikipedia 행동 연구 수렴. 직접 비교 실험은 부재 |
| 페이지 분할 500줄/5k | [정황] | SKILL.md 수치 유추 |
| qmd 채택 + 폴백 사다리 | [검증] | 15+ 도구 서베이 + 트렌드 재확인. 한국어 실품질은 수용 검증 |
| qmd 백업·이관(사본 1차, index.yml 커밋, GGUF 벤더링) | [검증] | 5각도(소스 감사·이슈 실측·공급망·크로스플랫폼·로컬 실기) |
| 한국어 2레그(Kiwi 형태소 + qmd 음절) | [검증-실기] | 실측 대결표 10문서×16질의. 관건은 질의 대칭·POS 필터(nori 정합)·사용자 사전 |
| 벡터 레그 존치 | [실험] | grep 우위는 코드 대상 — 산문·한국어 기여는 수용 검증 A/B, 무시 가능 시 강등 |
| 그래프 인프라 불채택 + edges/CTE 깊이 4 | [검증] | 독립 벤치마크 3편 + CTE 실측(depth-3 1.97ms) |
| 멀티홉 사다리 선검증(1단 실측·3단 스모크) | [검증] | 합성 2/3-hop 10/10 + HippoRAG2 설치·비용·증분 확인. 실코퍼스는 하네스가 판정 |
| 스킬 4종·정본 .agents + 복사 동기화 | [검증] | Claude Code .agents 미지원 + Windows 심링크 파손 |
| kb-new(얇은 스킬 + 스크립트) | [검증]+[선택] | skill-creator 역사형·okf-skills·basic-memory 동일 분할. 판단 게이트는 무선례 [선택] |
| KB-first 암묵 발동 | [실험] | 산문 준수 비보장(공식 문서) — 명시 호출 1차, 암묵은 측정 |
| review-on-read 승급 | [정황] | read repair·citation-needed 동형 |
| diff 격리 리뷰(inbox) | [실험] | 현장 보고 1건 — 킬 기준·나이 자동 머지·부하 실측 부착 |
| 운영 로그 git 배치 금지(stats DB + 트레일러) | [검증] | 12-factor 원문 + 선례 부재. CHANGELOG/ADR류만 git 관행 |
| ADR의 KB 내 배치, NNNN은 type 기준 | [검증] | Wikipedia 네임스페이스·Confluence 블루프린트·brain-kit·gwern — 결정-을-지식-페이지는 KB 원산 규범 |
| 저장소 구조: 글루 동거 + 엔진 외부 | [검증] | 지식형 선례 재도출(Jekyll _plugins·Obsidian plugins·Wikipedia Module ns; 엔진 외부는 전 선례 — gwern 2저장소 포함) |
| sources/concepts/synthesis 3분류 | [선택] | 표준(Karpathy·OKF)이 레이아웃 위임 — 쓰기 정책 경계와의 일치가 정당화 |
| 대량 이동 금지·연도 샤딩·compaction·stats | [검증]+[선택] | Iceberg 1차 문서. 세부 수치(분기·1–4k)는 판단 |
| 임베딩 버전 핀 + blue/green | [검증] | Azure 공식 + 확립 개념. qmd docid 함정은 수용 검증 [실험] |
| DV2.0 계보 등가(트레일러+blame+sha256) | [검증] | DV 규격 시트 매핑 — 각주가 행보다 세밀, git이 LOAD_DTS/hash_diff 네이티브 |
| 검색 평가: ir_measures+pytest+자작 잔여 | [검증-실기] | IR 라이브러리 4종 실설치 — 30/30 수치 일치. 탐색 메트릭은 IR 모델 밖 |
| LLM-judge: DeepEval(2순위 TruLens) | [검증-실기] | 실설치·커스텀 메트릭·G-Eval 스텁 종단 구동·아웃바운드 0 실측 |
| 스킬 evals: dbt skill-eval + run_eval.py | [검증-실기] | 종단 실구동(설치→run→grade→report), dbt 하드코딩 0, 커밋 핀 |
| 평가 규약(baseline 의무·≥3·숫자 게이트 없음) | [검증] | dbt·Anthropic·superpowers 선례 합집합 — 발명 없음 |
| overview.md llms.txt 구조 | [선택] | 표준 차용 — 효용 직접 증거 없음 |
| 멀티 KB(단일 저장소+컬렉션, 하드 경계 분리) | [검증]+[선택] | qmd 소스·restic·스킬 스코프 확인. 공유는 copier(submodule 기각) |
| 배포 토폴로지(MacBook 로컬/mini Ollama/NAS 원격) | [검증] | SQLite NAS 금지 원문 + qmd 데몬 이슈 + Ollama LAN 관행 + DeepEval base_url 소스 |
| 백업 3계층 | [검증] | SQLite LTS·LoC·GitHub 정책·restic 문서 |
| MCP 범위 최소화(셸 없는 표면만) | [검증] | 상시 ~8k 토큰 오버헤드 + CLI 셸아웃 우위 관행 |
| Claude Code 자동 메모리와 역할 분리 | [검증] | MEMORY.md=세션 계층, KB=내구 지식 — 중복 금지, kb-query가 두 계층을 참조 |
| 파이프라인 RAG 층 금지(에이전트 도구 선택 구도) | [검증] | 통제 실험(MemDelta) + 제품 수렴(Claude Code·Cursor) |
| ANN·point-in-time 불구축 | [검증] | Faiss 가이드라인 + temporal RAG 미성숙 |
| lint 실행 전략(주간 증분 + 전쌍은 부트스트랩·분기 블록 배치) | [선택] | 산수 근거 — 10만 전쌍 5×10⁹·40GB는 불가, 증분 1×N과 블록 행렬곱은 분 단위. 외부 검증 없는 자체 설계 |

## 참고 (주요 출처)

**계보·기질**: Karpathy LLM Wiki https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f · OKF 스펙 https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf · gwern https://gwern.net/about · https://gwern.net/archiving · Voit 이식성 https://karl-voit.at/2026/04/08/obsidian-md-portability/ · 기업 위키 지속성 https://dl.acm.org/doi/abs/10.1145/1877725.1877731

**granularity**: evergreen 회고 https://engineeringideas.substack.com/p/reflection-on-two-years-of-writing · 1만 노트 사례 https://forum.zettelkasten.de/discussion/1664/disillusioned-with-zettelkasten-method-am-i-doing-something-wrong · Schmidt 루만 연구 https://zettelkasten.de/posts/zettelkasten-hubs/ · Matuschak https://notes.andymatuschak.org/z2hQEhqWkdRLL9JUwfawZZx · 나노퍼블리케이션 https://arxiv.org/abs/1809.06532 · WP:CONTENTFORK https://en.wikipedia.org/wiki/Wikipedia:Content_forks · WP 문서 크기 https://en.wikipedia.org/wiki/Wikipedia:Article_size · 규모 한계 현장 보고 https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres

**쓰기 정책**: 리뷰 효과 붕괴 https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ · Wikipedia NPP https://en.wikipedia.org/wiki/Wikipedia:New_pages_patrol/Analysis_and_proposal · 메모리 드리프트 https://arxiv.org/html/2603.11768v1 · https://arxiv.org/pdf/2605.17830 · 실사용기 https://www.rdworldonline.com/is-karpathys-viral-llm-wiki-helpful-mostly-yes-one-month-in/

**검색·진입점**: FTS5 공식 https://www.sqlite.org/fts5.html · Kiwi https://github.com/bab2min/kiwi · kiwipiepy https://github.com/bab2min/kiwipiepy · Lucene nori STOP_TAGS https://github.com/apache/lucene/blob/main/lucene/analysis/nori/src/java/org/apache/lucene/analysis/ko/KoreanPartOfSpeechStopFilter.java · lindera-sqlite https://github.com/lindera/lindera-sqlite · SQLite 벡터 실측 https://marcobambini.substack.com/p/the-state-of-vector-search-in-sqlite · RRF https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf · lost-in-the-middle https://arxiv.org/pdf/2606.27793 · qmd https://github.com/tobi/qmd · basic-memory https://github.com/basicmachines-co/basic-memory · KURE https://github.com/nlpai-lab/KURE · NoLiMa https://arxiv.org/abs/2502.05167 · Chroma context rot https://www.trychroma.com/research/context-rot · llms.txt 실측 https://ahrefs.com/blog/what-is-llms-txt/ · Wikipedia 독자 행동 https://arxiv.org/abs/2112.11848 · grep 하네스 벤치마크 https://arxiv.org/html/2605.15184v1 · Anthropic 도구 설계 https://www.anthropic.com/engineering/writing-tools-for-agents · 컨텍스트 엔지니어링 https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**그래프**: RAG vs GraphRAG https://arxiv.org/abs/2502.11371 · GraphRAG-Bench https://arxiv.org/abs/2506.05690 · 에이전트 검색 https://arxiv.org/abs/2604.09666 · HippoRAG2 https://arxiv.org/abs/2502.14802 · LazyGraphRAG https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ · Kuzu https://www.theregister.com/software/2025/10/14/kuzudb-graph-database-abandoned-community-mulls-options/1142229

**평가**: ir_measures https://github.com/terrierteam/ir_measures · dbt-agent-skills https://github.com/dbt-labs/dbt-agent-skills · DeepEval https://github.com/confident-ai/deepeval · TruLens https://github.com/truera/trulens · RAGAS https://github.com/vibrantlabsai/ragas · MemDelta https://arxiv.org/abs/2606.29914 · promptfoo https://github.com/promptfoo/promptfoo · superpowers https://github.com/obra/superpowers

**스킬·연동**: 스펙 https://agentskills.io/specification · 레포 https://github.com/anthropics/skills · Codex 스킬 https://developers.openai.com/codex/skills · Claude Code `.agents` 이슈 https://github.com/anthropics/claude-code/issues/31005 · 훅 https://code.claude.com/docs/en/hooks · Skills vs MCP https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/ · AAIF https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation

**메타데이터·시간**: CSL https://docs.citationstyles.org/en/stable/specification.html · Better BibTeX https://retorque.re/zotero-better-bibtex/ · Obsidian Properties https://obsidian.md/help/properties · Text Fragments https://caniuse.com/url-scroll-to-text-fragment · Wikidata 정밀도 https://www.wikidata.org/wiki/Help:Dates · YAML timestamp https://yaml.org/type/timestamp.html · Wikipedia 인라인 템플릿 https://en.wikipedia.org/wiki/Template:Citation_needed · RFC 2119 https://www.rfc-editor.org/rfc/rfc2119

**구조·규약·운영**: llms.txt https://llmstxt.org · Nygard ADR https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · GTD https://gettingthingsdone.com/what-is-gtd/ · org-mode refile https://orgmode.org/manual/Refile-and-Copy.html · email bankruptcy https://en.wikipedia.org/wiki/Email_bankruptcy · Anthropic best practices https://code.claude.com/docs/en/best-practices · Anthropic memory https://code.claude.com/docs/en/memory · PEP 594 https://docs.python.org/3/whatsnew/3.13.html · markdown-it-py https://pypi.org/project/markdown-it-py/ · SRE SLO https://sre.google/sre-book/service-level-objectives/ · Anki 백로그 https://controlaltbackspace.org/catch-up/ · MoC https://notes.linkingyourthinking.com/Cards/MOCs+Overview

**미시 규칙**: Diátaxis https://diataxis.fr/foundations/ · WP:SPLITTING https://en.wikipedia.org/wiki/Wikipedia:Splitting · EPPO https://everypageispageone.com/the-book/ · Google 파일명 https://developers.google.com/style/filenames · MS Learn 마크다운 https://learn.microsoft.com/en-us/powershell/scripting/community/contributing/general-markdown · 폭소노미 https://arxiv.org/abs/cs/0508082 · NN/g Taxonomy https://www.nngroup.com/articles/taxonomy-101/ · object 태그 https://zettelkasten.de/posts/object-tags-vs-topic-tags/ · gwern design https://gwern.net/design · JabRef citekey https://docs.jabref.org/setup/citationkeypatterns

**데이터 플랫폼**: Iceberg 스펙 https://github.com/apache/iceberg/blob/main/format/spec.md · Iceberg evolution https://github.com/apache/iceberg/blob/main/docs/docs/evolution.md · Confluent 호환성 https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html · Faiss 인덱스 가이드 https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index · Azure 임베딩 일치 https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-generate-embeddings

**도구 서베이**: Meilisearch charabia https://github.com/meilisearch/charabia · LEANN https://github.com/StarTrail-org/LEANN · qmd 이슈 https://github.com/tobi/qmd/issues · openwiki https://github.com/langchain-ai/openwiki

**백업·이관·토폴로지**: 12-factor logs https://12factor.net/logs · SQLite backup https://www.sqlite.org/backup.html · SQLite NAS https://www.sqlite.org/howtocorrupt.html · https://www.sqlite.org/useovernet.html · Pro Git 서버 https://git-scm.com/book/en/v2/Git-on-the-Server-Setting-Up-the-Server · rest-server https://github.com/restic/rest-server · Ollama LAN https://docs.ollama.com/faq · ADR 번호 충돌 https://github.com/npryce/adr-tools/issues/102 · ClickHouse UUID https://clickhouse.com/docs/en/sql-reference/functions/uuid-functions · Snowflake https://github.com/twitter-archive/snowflake · dbt projects https://docs.getdbt.com/docs/build/projects · Hugo modules https://gohugo.io/hugo-modules/use-modules/ · SQLite LTS·LoC https://www.sqlite.org/lts.html · https://www.sqlite.org/locrsf.html · GitHub 2FA https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials · git-annex https://git-annex.branchable.com/future_proofing/ · LoC 아카이빙 https://digitalpreservation.gov/personalarchiving/ · restic https://restic.readthedocs.io/en/stable/045_working_with_repos.html · Syncthing FAQ https://docs.syncthing.net/users/faq.html


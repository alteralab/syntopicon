# Syntopicon 계획

IT 서적·논문·기술 문서를 10–20년 축적하는 개인 지식 베이스. 2026-08-02 초판, 2026-08-04 개정판(멀티 KB 레이아웃 확정 / 태그·ADR 불채택 전환 / 데이터 플랫폼 이식 감사 반영).
결정별 검증 등급과 근거는 §8 원장이 정본이다. 본문은 결정과 규약만 기술하고, 정당화 서사는 원장과 불채택 표(§6)로 내린다.

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
7. **ID 외 동시성**: ⓐ 재색인·`qmd update`는 단일 실행 직렬화 ⓑ 텔레메트리는 git 밖 stats DB(§3) ⓒ inbox diff는 런ID 명명 + O_EXCL ⓓ index.sqlite 사본은 §5 규약 준수(라이브 cp 금지) ⓔ rename·compaction은 클린 워킹트리 확인 후 에이전트 세션과 비동시 실행 ⓕ git push(non-ff 거부)·restic(불변 블롭)·bundle(git 일관 스냅샷)은 무처방 안전.

### 2.6 페이지 위생

- **분할 1차 기준은 목적**: 한 페이지 = 하나의 질문. 분할 조건: 섹션이 다른 질문에 답하기 시작 + 자식이 자립 가능. 자식이 스텁이 되거나 부모 요약의 복제면 분할 금지.
- **크기는 lint 백스톱**: 500줄 초과 경고(자동 분할 아님 — 수치는 임의 운영 상수, §8). 100줄 초과 시 상단 TOC. 지식 페이지는 온디맨드 독해 계층이므로 1차 완화책은 분할이 아니라 **TOC + 섹션 앵커**(상시 로드 계층용 상한의 전이 금지 — §8).
- **구조**: 파일당 H1 하나(제목 일치)·헤딩 레벨 건너뛰기 금지(표준 — §8), 깊이 H3–H4 상한(H4 필요 = 분할 신호 — 자체 휴리스틱, §8).
- **TOC 형식**: 정본 = `**목차**: [섹션](#앵커) · …` 인라인 문단(H2 이전 상단), 포인터 불릿 목록형 인정 (형식 무계약의 검사-저작 표류 실증 — §8).
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
- SCHEMA.md·overview.md도 frontmatter `type` 보유(예약 파일명 외 전 .md는 typed frontmatter).

## 4. 파이프라인과 도구

### 4.1 진입점과 검색

**진입점 — 전체 카탈로그 없음, 2계층 + 검색 우선.** ① 루트 `overview.md`(라우터) → ② `<kb>/overview.md`(허브, MoC 목록) → ③ 검색 도구가 1차 경로.

**검색 스택 — qmd + 자체 레그 2종.**

- **qmd 채택**(SQLite FTS5 + 로컬 GGUF 임베딩 + RRF + 리랭크 + CLI/MCP + SHA-256 증분 색인). **버전 핀 + `npm pack` 타르볼 보존**. 폴백 사다리: basic-memory(**부분 폴백** — 저장·FTS·MCP 서빙만: 그래프는 wikilink 전용·형태소 부재·`disable_permalinks: true` 필수, 소스 검증 §8) → Meilisearch(발동 조건 §6 표) → LEANN(시맨틱 보조). 한국어 질의는 확장 없는 `search`/`vsearch`(질의 확장의 영어 편향 회피). 데몬 모드로 모델 웜 유지.
- **임베딩 = Qwen3-Embedding-0.6B 잠정**, 수용 검증 A/B(vs KURE-v1) 후 핀. **모델 버전 = 스키마 버전, 호환 NONE**: 모델 id+리비전+차원+청킹을 인덱스 메타에 핀, 변경은 blue/green 전체 재빌드. 서로 다른 모델 벡터 혼합 금지(무경고 recall 붕괴). **차원은 모델 최대(1024) 유지 — MRL 축소 금지**(저차원일수록 규모 오탐 단조 증가, §8). **무효화 단위 = 페이지**: 편집 시 해당 페이지 청크 전량 재생성(§4.4-9가 집행). 청킹은 색인기(qmd) 소관 — 페이지 크기와 독립(실측 §8; ≤900토큰 페이지는 1청크).
- **벡터 레그의 존치 조건**: grep 우위 실증은 코드·어휘 일치 질의 대상이고, 산문 패러프레이즈·한국어 표면형 변형이 벡터의 잔존 근거. 기여도는 수용 검증 A/B로 측정 — 무시 가능이면 FTS 전용 강등. **파이프라인 RAG 층 금지** — 에이전트가 도구를 고르는 구도를 유지한다(stats 기반 자동 전략 선택 없음).
- **자체 레그 ① 한국어 형태소 FTS**: Kiwi 분석 → 공백 join → FTS5 unicode61 테이블. 필수 사양: **질의 시점 대칭 분석**(질의도 동일 Kiwi+동일 POS 필터로 phrase 변환), **POS 필터 = 명사류+SL/SH/SN+용언 어간+XR**(nori STOP_TAGS 정합), **사용자 사전 필수**(`schema/user-dict.yaml` 시드 + 파편화 검출로 증분 관리, 사전 변경 시 재색인), compound는 성분 분해+phrase 질의. 음절 substring은 qmd 내장 레그가 담당, 영문 부분문자열은 `rg` 폴백.
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

**실행 계획 (2026-08-10 수립 — 진행 상태: 도서 2권 완료, 38 concepts)**:

- **소스 배분** (잔여 28–48): 도서 8–12권(사용자 조달 — 원서 우선 §4.4-①, ingest에 실파일 PDF/EPUB 필수) + 논문 10–20편(에이전트가 오픈액세스 조달) + 기술 문서 5–10건(docs-mirror 승격 경로 — 미러 기보유).
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

등급: **[검증]** 1차 출처·벤치마크·로컬 실측(로컬 실기로 재현까지 확인한 것은 **[검증-실기]**) / **[정황]** 수렴 간접 증거 / **[실험]** 근거 얇음 — 측정 계획·킬 기준 부착 / **[선택]** 표준 위임 영역의 자체 결정. 규칙: 새 결정은 등급과 함께 기록하고, [실험]은 측정 계획 없이 존재할 수 없다. **재검증에서 탈락한 결정은 §6 불채택 표로 이동한다**(2026-08 사이클: 태그 governed-open·ADR KB 배치 — 이력은 git).

| 결정 | 등급 | 핵심 근거 |
|---|---|---|
| md+git 기질, GFM 부분집합, 소모품 인덱스 | [검증] | 장기 실증(gwern 16년·org-mode·Dendron 데이터 생존) + 반증 라운드 생존 |
| 개념 페이지 단위 (1claim=1파일 기각) | [검증] | 원자 노트 다년 실패 회고·루만 재해석·생태계 수렴 |
| frontmatter 필드 집합·부재=기본값·따옴표 날짜 | [검증] | OKF 스펙 대조 + PyYAML/yq/GitHub 렌더러 로컬 실측 |
| 각주=출처 귀속, citekey 문자 집합 | [검증] | GitHub 실제 렌더러 실측 |
| 소스 메타(1단 type, CSL 원어명) | [검증] | CSL-JSON 103속성 전수 대조 + 실소스 6종 수용 테스트 |
| frontmatter 경로=루트 / 본문 링크=상대 | [검증] | OKF §6.2 + 렌더러 실측 + Jekyll/Hugo/basic-memory 선례 |
| 스키마 2층(JSON Schema+파이썬) | [검증] | Astro/Docusaurus 관행 + JSON Schema 표현력 한계 + 로컬 실험 |
| tools 구현 규약(파서 우선·regex 파싱 금지·pythonic) | [선택] | regex 파싱은 관측된 패턴에만 맞추는 greedy — 엣지 케이스마다 패턴 증식·수정 루프 무한. 파서는 스펙 기반이라 엣지 케이스가 스펙의 정의된 동작으로 환원(markdown-it-py 채택·CommonMark 동결과 동일 계보). 예외: 문자집합 검증은 정규 언어라 regex가 정확한 도구 |
| 레지스트리 + BACKWARD_TRANSITIVE + 키 결번(validate 대조 집행) | [검증] | Confluent 원문 대조 — append-only 코퍼스 + 진화 도구는 동일 문제 구조. 집행자 신설은 이식 감사 결과 |
| type 어휘(redirect/guide 포함) + ID 발급 규약 | [검증]+[선택] | 전 파일 종류 열거 감사. 영어 번역 슬러그·한국 저자 citekey는 [선택] |
| ID 동시성: O_EXCL 의무 | [검증-실기] | check-then-write 덮어쓰기 재현 + O_EXCL fail-loud 실증 |
| ID 유일성 = KB 스코프, 정규형 `<kb>/<slug>` | [검증] | citekey 결정론(같은 소스=같은 키)과 전역 유일성의 모순 + ns/name 선례(Jira·k8s·Zotero API). Zotero 함정(이동=복사)은 rename/redirect 경로가 차단(KB 간 스텁의 정규형 예외 포함) |
| citekey 슬러그는 충돌 시에만(첫 권 선제 부착 불채택) | [선택] | 슬러그는 판정이라 필수화하면 §2.5-6의 결정성("같은 소스=같은 키로 수렴")이 깨진다 — `database-internals`인지 `db-internals`인지를 세션마다 다르게 고른다. 대가는 각주 전량이 길어지는 것(1페이지 19회 인용 실측)이고 실익은 미발생 충돌 대비뿐. 충돌 빈도: 도서는 희박(현 5권 저자 전원 상이), **논문은 유의미**(다작 저자의 동년 arXiv — §6이 논문 10–20편 계획). 발생 시 `--slug` 또는 자동 `-2` |
| **rename의 citekey 개명이 절반만 재작성한다 (미수정 결함)** | [검증-실기] | `relocate.plan_edits`가 고치는 것은 md 링크와 frontmatter `resource` **둘뿐**. 본문 각주(`[^citekey]` 참조·정의)와 `sources[].id`는 그대로 남는다. **validate가 통과시킨다** — 각주 라벨과 `id`가 서로 짝을 이루고 `resource` 경로도 실존하므로 규칙 위반이 아니다(조용한 불일치). 옛 키 재사용은 redirect 스텁의 O_EXCL이 차단하므로 그 부분은 안전. 지금 고치지 않는다: citekey 개명이 발생한 적이 없어 선제 구축이 된다(원칙 5). **실제로 개명하기 전에 이 행을 볼 것** — 모르고 실행하면 어긋난 상태가 만들어지고 발견이 늦을수록 비싸다 |
| 중앙 ID 발급 불채택 | [검증] | ClickHouse 무시퀀스·Snowflake 무중앙호출 원문 + 개인 KB 선례 전무 |
| ID 외 동시성(재색인 직렬화·VACUUM INTO·런ID) | [검증] | SQLite 공식(라이브 cp 손상·백업 API) + qmd busy 이슈 |
| 분할 1차 기준=목적, 수치 백스톱은 임의 운영 상수 | [검증]+[선택] | 목적 기준은 Diátaxis·EPPO·Matuschak·WP 수렴(수치 규범 부재가 다수파). **구 "SKILL.md 500줄 유추"는 재검증 기각** — 그 수치는 상시 로드 계층용이고 지식 페이지는 온디맨드 계층(Anthropic 규범: 무제한 + 100줄 초과 TOC — §2.6 TOC 규칙의 실근거). 수치 백스톱 선례는 CLAUDE.md 200줄·WP 8k단어뿐, 500줄은 그 스펙트럼 내 임의점 [선택]. "~5k 토큰" 병기는 출처 없는 자체 환산이라 삭제 |
| 청킹 = 색인기 소관(저작 단위와 독립) | [검증] | qmd 소스 실측: 900토큰/오버랩 135(15%)·헤딩 점수 컷·코드펜스 보호·**≤900토큰 페이지=1청크**(5k급≈7–9청크 — 구 "≤6청크"는 오산). 실무 기본값 800–1200 수렴(GraphRAG 1200·LlamaIndex 1024·basic-memory ~900자), 색인기 자체 청킹이 지배적(8표본 중 7, 예외 HippoRAG). semantic vs 고정 크기 우열은 혼재(Chroma·arXiv 2410.13070) — qmd의 헤딩 점수 절충이 수렴점 |
| 파일명 규칙(kebab·80자·한글 금지·무접두) | [검증] | Google 스타일 가이드·바이트 한도·NFC/NFD 대조 |
| epistemic `#hypothesis` 토큰(폐쇄 어휘) | [정황] | 구문 울타리 선례(citation-needed·RFC 2119). 표기 자체는 선택 |
| **태그 불채택 — 허브+backlinks 대체** | [검증] | 통제 어휘 규정 스펙 0/7·장기 운영자 수렴(Matuschak 폐기·포럼 "구조노트와 중복"·gwern 디렉터리 통합)·Luhmann 색인 희소성(3.2k/67k, 항목당 참조 1–4)·CONFCLOUD-7681. 상태·유형 축은 스키마 필드가 기담당 |
| **ADR 불채택** | [검증] | 표준(Nygard·MADR·adr-tools) 전부 코드 저장소 지정·실사용 14/14·ThoughtWorks 위키 명시 배제·md-first KB 스펙 0/7·번호=코드 참조용 ID(1인 KB에서 용도 소멸) |
| 전체 카탈로그 폐기, overview 2계층+검색 우선 | [검증]+[선택] | Wikipedia 독자 실측: 검색 47.7%+링크 35.7% vs Portal 0.02%(Piccardi 원문 재확인). 카탈로그 한계는 Karpathy 본인 자인("~100 sources, ~hundreds of pages"까지만). **규모 감당의 실증**: Luhmann 색인 21:1 희소 생존(항목당 참조 1–4 — 순수 포인터) vs Portal 5,705→~550 소멸(복제 콘텐츠 부패+유지자 부재). 생존 조건 = 포인터-only + 갱신의 워크플로 결합(ingest 허브 연결·링크 차수 후보·고정 상한). 허브 계층 재귀는 zettelkasten.de 원문 실증 |
| overview 형태 = 진입 문서 50년 관례(llms.txt 명명 제거) | [검증]+[선택] | 공통형 실증: README(1974 DECUS~)·Wikipedia Contents·LYT Home note·OKF index.md §8·CLAUDE.md/AGENTS.md("no required format") — 자유 md+오리엔테이션+링크 목록. llms.txt 고유 추가분은 소비자 부재로 불차용. OKF는 진입 목록을 파생물 취급("MAY generate automatically / synthesize on the fly"). **수치(라우터 ~200토큰·허브 1–2k·Hubs 10–30)는 자체 상수 [선택]** |
| 파일명 `overview.md` = 장르 관례로부터의 의도적 이탈 | [선택] | LLM 위키 실구현 센서스 14건: index.md 계열 11(구성 확인분 중 **카탈로그형 7/10** — 기각된 방식이 그 이름의 의미론), overview.md 진입 1(suwonleee/llmwiki "Front page / entry point" — 카탈로그를 FTS로 분리하고 진입은 포인터로 쓰는 **동형 구조의 수렴**). index.md 개명은 카탈로그 프라이어 수입 위험 — 관례 합치보다 의미론 격리 우선. 동결 코어 밖·전환 O(1), 수용 검증에서 에이전트 오용 관찰 시 재평가 |
| overview 운용(에이전트 소비 진입 문서) = 현재 실사용 관행 | [검증]+[정황] | "인덱스 먼저→링크 심층"을 문자 그대로 규정한 3곳: Karpathy("reads the index first, then drills into them")·OKF("or agent" 명문)·**Claude Code auto-memory**("MEMORY.md acts as an index… reads them on demand" — 제품 기본 동작). 자동 로드형까지 8개 도구 공식 문서 확인(CLAUDE.md·Copilot instructions·Cline memory bank·aider repo map). **한계 [정황]: 에이전트-소비의 10년+ 생존 사례는 모달리티 나이(≈3년)상 원리적 부재** — 장기 논거는 형태 계보가 담당, md 기질이라 최악 시 사람용 README로 퇴화 생존. 실패 모드(비대화→준수 저하·부패·토큰 비용)는 공식 인정 — 완화책(고정 상한·포인터-only·lint 대조)이 그 대응. **대안 비교 완료**: 전수동(Portal 부패)·전자동("automated crud" — 목록 자동화는 생존, 큐레이션 자동화는 실패)·무진입(빈 컨텍스트 지형 부재)·**그래프 파생 위키(§6 표 — 저작형 실사용 0·커뮤니티 분할 불안정)** 기각 → 자동 골격+수동 선정+기계 대조(gwern 패턴). **동결 코어 밖 — 결합점 3개(마커·kb-query ①·lint)뿐이라 전환 retrofit O(1)**, 감지기는 search-miss 경보·Hubs 대조·수용 검증 ⑧ |
| qmd 채택 + 폴백 사다리 | [검증] | 15+ 도구 서베이 + 트렌드 재확인. 한국어 실품질은 수용 검증. **basic-memory 소스 검증(2026-08)으로 부분 폴백 강등**: relation 추출이 wikilink 전용(표준 md 링크 무인식 — 그래프 기능 전멸)·형태소 부재(unicode61 어절 토큰·Postgres 'english' 하드코딩·기본 임베딩 영어 전용)·기본값이 파일 변조(permalink 주입+YAML 재직렬화 → `disable_permalinks: true` 필수). 파일=정본·멀티 프로젝트는 정합 — 저장·FTS·MCP 폴백으로만 유효 |
| qmd 백업·이관(사본 1차, 글로벌 config=파생물, GGUF 벤더링) | [검증] | 5각도(소스 감사·이슈 실측·공급망·크로스플랫폼·로컬 실기). in-repo 모드 기각: `findLocalConfigPath`가 cwd 상향 탐색 — 저장소 밖 조회 불가(소스 확인), 글로벌 레지스트리가 공식 1급("search any collection from any directory") |
| 한국어 2레그(Kiwi 형태소 + qmd 음절) | [검증-실기] | 실측 대결표 10문서×16질의. 관건은 질의 대칭·POS 필터·사용자 사전 |
| 벡터 레그 존치 | [실험]+[검증] | grep 우위는 코드 대상 — 산문·한국어 기여는 수용 검증 A/B, 무시 가능 시 강등. 완전 제거 반대의 [검증] 근거: 어휘 검색의 동의어 취약(LIMIT synonyms에서 BM25 −89%) |
| 검색 스택 = 희석 완화 3종 구비(어휘 주력+융합+리랭커) | [검증] | 밀집 희석은 실재 — Reimers/ACL2021: 오탐이 인덱스 크기 증가·차원 감소에 단조, 수백만 문서대에서 BM25 역전; LIMIT/ICLR2026: 차원이 top-k 조합을 상한, **리랭커가 100% 회수**·하이브리드가 dense 단독 대비 +20.4%. 설계 규모(≤10⁵ 청크)는 dense 우위 구간(10k–100k 실측 91.5/79.4 vs 79.9/63.9) — 재평가 조건 = 청크 10⁶ 접근(§6 ANN 재심과 정렬) |
| 그래프 인프라 불채택 + edges/CTE 깊이 4 | [검증] | 독립 벤치마크 3편 + CTE 실측(10만 노드 depth-3 1.97ms·depth-5 218ms — 상한 4는 그 사이 절충) |
| 멀티홉 사다리 선검증(1단 실측·2단 스모크) | [검증] | 합성 2/3-hop 회수 10/10(flat 검색 0/10) + HippoRAG2 설치·비용·증분 확인. 실코퍼스는 하네스가 판정. **외부 실증 정합**: 위키형 링크 추적 에이전트가 HippoRAG2·GraphRAG 상회(+2.0~8.1 F1, arXiv 2605.25480 — 우리 메커니즘 동형)·저작 하이퍼링크 탐색 +14pt(Asai ICLR 2020)·반복 검색 +21pt(IRCoT). 구조증강의 단순 질의는 동급이 최대(HippoRAG2 +0.5~1.4pt, HippoRAG1 회귀 53.1 vs 57.0)·추출 KG는 정답 엔티티 ~34% 누락. 뇌 유추(해마 색인)의 원문 주장은 "분리된 색인 층"이지 밀집 상시 채택이 아님 |
| 스킬 4종: 정본 .agents/ + 기기별 `~/.claude/skills/` 심링크 배포 | [검증] | Claude Code 공식: 프로젝트 스킬 "This project only"·개인 스킬 "All your projects"·심링크 공식 지원(같은 타깃 1회 로드, personal>project 그림자 문제 없음). 커밋 심링크만 금지(Windows 클론 파손 — 홈 심링크는 무관). 정본 in-repo는 dbt eval 러너의 저장소 루트 상대 참조가 강제(소스 확인) |
| KB 접근 = 전용 세션 + 타 프로젝트 조회 병행 | [검증] | "어디서든 접근"은 개인 KB 생태계 공식 패턴(basic-memory MCP 전역 등록이 기본 절차·Obsidian URI·Claude Code 사용자 레벨 "all projects"). 전용 세션은 Karpathy 구도("the wiki is the codebase") — 병행 무충돌 |
| kb-new: 얇은 스킬+스크립트, **KB의 유일 생성 경로** | [검증]+[선택] | 도구 분할은 선례 동일(skill-creator·basic-memory). 유일 경로·구축 시 KB 0개는 특례 제거 + dogfooding — 무선례 [선택] |
| **KB 네임스페이스 동형 레이아웃**(콘텐츠=`<kb>/`, 공유=루트) | [검증]+[선택] | 선례 13 실측: 빌드 코드 동거 시 콘텐츠 격리 4/4, 혼합형 0/13. "기본 인스턴스" 5/7은 무해하나 Zotero My Library(구조적 비대칭)만 만성 부채 — 동형이 핵심 |
| **공유 자산 단일본(오버라이드 금지)** | [검증] | 상용 7 중 스페이스별 오버라이드 0·SharePoint read-only 명문·Wikimedia 900위키 템플릿 포크 20년(중앙 저장소 신설로만 해소) |
| **저장소 분리 비가역 + 게이트 협소** | [검증] | SharePoint unpublish 편도(복귀 경로 무문서화)·Jira 6.2 복제 기본화 → 스킴 스프롤(기대 10–15 vs 실측 40–100+) |
| **크로스 KB 링크 비권장 + edges 가시화** | [검증] | MediaWiki interwiki 실패 = 불가시성(backlink 미집계·존재 미검사). 격리 사유(기밀·분리)가 링크로 무효화되는 구조 |
| **횡단 검색 기본 ON(읽기) / `--kb` 명시(쓰기)** | [검증] | 횡단 부재 제품 전부(Obsidian·Logseq·Zotero·Capacities) 다년 미해결 FR·Confluence 기본값. 쓰기 명시는 이동 비용(rename·redirect 경유, §2.5-2)의 귀결 |
| layout.yaml 경계 선언(열거 대신 설정) | [선택] | Astro v5 교훈(예약 폴더 폐기→base 경로) 차용 — 직접 실증 없음 |
| flat 시작·신규만 샤딩·1–4k 상한 | [검증] | GitHub 공식 3,000 권고 + UI 1,000 truncation. 연도 샤딩 폐기: 산수 미도달(20년 ≤2k) + 자기 규칙(신규만)이 지연을 무비용화 |
| compaction = 위키 스텁 병합(분기) | [선택] | Iceberg 귀속 기각(small files 전제 부재 — 이식 감사). WP:MERGE 계열 큐레이션 문제로 재귀속. FTS5 optimize는 automerge 기본 처리, 저비용 선택 |
| 메타 테이블 무인덱스 시작 | [검증-실기] | 로컬 벤치: 10⁴–10⁵행 풀스캔 0.5–7ms — 주간 배치·CLI에 충분. 인덱스는 retrofit O(1) |
| 임베딩 버전 핀 + blue/green, 혼합 금지 | [검증] | Azure 원문 재확인("always use the same embedding models"·무경고 품질 붕괴). 규모 무관 제약 |
| 계보 = 기존 장치로 충분(각주·커밋·트레일러·sha256) | [검증] | DV 2.0 규격 시트 매핑은 서사(기계 장치 순증 0 확인 — 이식 감사). blame 표준은 소비자 부재로 불채택(§6) |
| **tools/affected(영향 범위 조회)** | [검증] | Jira 수백 인스턴스: 관리자 필드 수 ~50% 과소추정·미사용 50%+ — 인지 실패라 1인에도 유효. Nx/Turborepo affected 등가 |
| sources/concepts/synthesis 3분류(KB 내부) | [선택] | 선례(Karpathy·OKF)가 레이아웃 위임 — 쓰기 정책 경계와의 일치가 정당화 |
| 운영 로그 git 배치 금지(stats DB + 트레일러) | [검증] | 12-factor 원문 + 선례 부재 |
| 저장 언어 = 한국어 재서술 + 원어 병기 + 민감 구간 원문 직인용(영어 전면 저장 기각) | [검증]+[선택] | **문체≠의미 분리 실측**: 번역투 문헌은 손상 범위를 문체로 한정(분류 F1 93%도 문체 분포), GPT-4 MQM 의미 오류는 인간 번역가 동급(en↔zh)·en→ko 고난도 -2.5~-3.4 vs 인간 -1.9. **조건부 위험 실재**: 지식집약 en-ko에서 650 중 459 오류·41%가 개체명 오역(SemEval-2025)·무보조 용어 성공률 60–70% — 병기·직인용이 정확히 이 구간 타격(용어 주입 효과 0–10 ChrF 실증). **영어 전면 저장 기각 근거**: MKQA 한국어 lexical 31.4 vs dense 71.6("co-existed terms 부재") — 형태소 주력 레그 붕괴. 원형은 archive가 100% 보존. **병기의 성문 선례 확보**: Kubernetes ko 가이드("첫 사용 시 1회 한영 병기"+"식별자 원문 유지") — 구 "[선택] 미확인"에서 승격. 이중 언어 색인 우월은 McCarley 1999("both"). 위키 성문 판단: 미검수 기계번역 저장 "worse than nothing"(95% 부적합) — 검역+리뷰+각주 사슬이 그 조건 충족. 재서술의 인간 편익 = 생성 효과 d=0.40(86연구 메타). Furnas aliasing·용어집 불채택(tags.yaml 동일 논리)은 전 라운드와 동일 |
| 원서 우선(번역서는 역어 참조원) | [선택]+[정황] | 원서 우위: 정오표 제도화(인사이트·위키북스 공식 — 오류 상존의 제도적 방증)·시차 ~1년+(DDIA 13개월·AIMA 1년)·중역 열화(UNESCO 권고·피벗 -10 BLEU)·LLM 영어 우위(영어 피벗·토크나이저 최대 15배). 번역서 가치: 우수 역자 번역어 해설집(이펙티브 자바 3판)이 "역어 참조원"의 실물. 직접 비교 실험은 부재 — 절충은 [선택], 모순 증거 없음 |
| ingest 조립 전체(스냅샷→메타→추출→검역→검증→리뷰→편입→인간 전용층) | [검증]+[선택] | 관절 10 중 8이 성문 대응 — ISO 16363(shall 검증)·Archivematica(검역~편입 순서 통째)·BagIt(불변+체크섬)·arXiv/Dryad(공개 전 심사)·독일 위키(라벨)·봇 정책(기계 차등 게이트)·PROV-O/PREMIS(주체 구분). **자체 설계 2**: synthesis 인간 전용 "계층"(표준은 작업 유형 금지까지만 — [선택])·나이 자동 머지(2026-08-11 불채택 — §6, 무선례가 기각 사유가 됨). 의도적 이탈 1: 서지 메타 등록이 검증 앞(OAIS는 저장 후 등록) — citekey가 각주 앵커로 선행 필요. 분류 근거: 개인 메모리(7/7 직접 기입)가 아니라 장수 지식베이스·코드 산출물의 규범(격리+승인)을 따름 — 메모리 오염 공격 실증 3건(SpAIware·MINJA·MS Red Team)이 직접 기입을 공격면으로 지목 |
| 저장소 구조: 글루 동거 + 엔진 외부 | [검증] | 지식형 선례 재도출(Jekyll _plugins·Obsidian plugins·Wikipedia Module ns; 엔진 외부는 전 선례) |
| review-on-read 승급 | [정황] | read repair·citation-needed 동형 |
| inbox 격리 구조(검역+`[unreviewed]` 라벨+승급) | [검증] | 성문 동형 다수: Archivematica Quarantine→검증→인간 결정점, ISO 16363 "shall… verifies each SIP", 독일어 위키 Gesichtete Versionen(전 네임스페이스 17년 — 미검토 판 저장·라벨·검토판 우선 노출, 효과 연구 "substantially reduced vandalism"), AfC/Draft. 실패 모드 대응 확인: AfC의 사인은 지연이 아니라 **hiddenness**(WMF 자체 연구) — `[unreviewed]` 검색 노출이 그 기전 차단. 사전 전수 심사는 Nupedia 반례(3년 24건 vs 게이트 제거 후 1년 18,000건) — 리뷰 기준 축소(무해성만)가 독일어판 생존 조건 |
| 1인 리뷰 지속가능성 | [검증] | 1인은 리뷰 공급=1이라 백로그가 정상 상태화하는 실증(독일어판 상시 1만+건·일 +76 순증) — P90 경보는 파산 시점 계측이고, 대응은 발생 시 결정한다(사전 처방 없음). 함께 있던 나이 자동 머지는 2026-08-11 불채택(§6) — 생태계 무선례였고([실험] 등급의 사유), 첫 배치 실측에서 적체 0이라 소비자도 없었다 |
| 검색 평가: ir_measures+pytest+자작 잔여 | [검증-실기] | IR 라이브러리 4종 실설치 — 30/30 수치 일치. 탐색 메트릭은 IR 모델 밖 |
| 스킬 evals: dbt skill-eval | [검증-실기] | 종단 실구동(설치→run→grade→report), 커밋 핀. run_eval.py 트리거 배터리·DeepEval judge는 소비 부재로 불채택(§6 — 실기 검증 이력은 재심 시 재사용) |
| 평가 규약(baseline·스킬당 ≥3·게이트 없음) | [검증] | ≥3 = Anthropic 문서, baseline = skill-creator·superpowers 절차 필수(dbt는 관례), 게이트 없음 = 3선례 일치. judge 3필드(success/1–5/tool_usage) = dbt 원문 |
| 배포 토폴로지(MacBook 로컬 + NAS 원격 2기) | [검증] | SQLite NAS 금지 원문 + qmd 데몬 이슈. mini 역할은 소비자 소멸로 불채택(§6) |
| 백업 3계층 | [검증] | SQLite LTS·LoC·GitHub 정책·restic 문서 |
| MCP 표면 = qmd 내장으로 충분(자체 서버 불채택) | [검증] | 상시 ~8k 토큰 오버헤드 + CLI 셸아웃 우위 관행 + qmd 내장 MCP와의 중복 |
| Claude Code 자동 메모리와 역할 분리 | [검증] | MEMORY.md=세션 계층, KB=내구 지식 — 중복 금지, kb-query가 두 계층을 참조 |
| 파이프라인 RAG 층 금지(에이전트 도구 선택 구도) | [검증] | 통제 실험(MemDelta) + 제품 수렴(Claude Code·Cursor). stats 기반 자동 전략 선택의 불채택 근거이기도 함 |
| ANN·point-in-time 불구축 | [검증] | Faiss 가이드라인 + temporal RAG 미성숙 |
| lint 실행 전략(주간 증분 + 전쌍은 부트스트랩·분기 블록 배치) | [선택] | 산수 근거 — 10만 전쌍 5×10⁹·40GB 불가, 증분 1×N·블록 행렬곱은 분 단위 |
| 운영 임계 경보(구 "SLO" 명명 기각) + 수치 3종 | [선택] | SRE SLO는 외부 사용자·error budget·조직 협상 전제(원문) — 1인 도구 적용 선례 무, 실체는 임계 경보/tripwire. 수치(miss 20%·P90 30일·lint 50건)는 자체 상수 — 운영 데이터로 보정 |
| 페이지 구조 규칙(H1 유일·레벨 건너뛰기 금지 / 깊이 상한) | [검증]+[선택] | 전자는 Google·MDN·MS Learn 3소스 일치. "H4=분할 신호" 깊이 상한은 어느 가이드에도 없음 — 자체 휴리스틱 [선택] |
| 쓰기 정책 3불채택(전수 게이트·무게이트 기입·표본 감사) | [정황]+[검증] | SmartBear 400 LOC 연구는 벤더 단일 사례·대조군 무·비판 문서화 [정황] — Wikipedia NPP 분석과 방향 수렴으로 유지. 표본 감사 기각 산수(2% 오류 95% 검출 ≈149건)는 [검증] |
| 스냅샷 필수(링크 부패 대응) | [검증] | 연 ~3%는 문헌 **최저** 추정(Nelson&Allen 2002 — gwern이 "lowest estimate"로 명시). 실측 범위: Fetterly 주당 0.5%(연 ~23%)·Pinboard 연 ~6%·Zittrain HLR 인용 70% 사멸 — 하한으로도 장기 복리 치명 |
| 첫 배치 리뷰 부하 실측 (2026-08-10, 4런 37초안) | [검증-실기] | 런별 ingest→승급 벽시계: 6분48초(8초안)·7시간2분(9)·21분43초(9)·9분1초(11). **둘째 런은 야간 부재로 오염, 나머지 3건도 사람 판단만 분리 불가**(에이전트의 양식 작성·허브 저작·재색인이 같은 구간에 있음 — 분리하려면 stats 런 테이블이 필요, §6). 분리 가능한 사실: ⓐ **inbox 적체 0** — 4런 전부 같은 세션에서 승급, 나이 P90이 30일 임계 근처에도 못 감 ⓑ 사람 입력은 런당 1~2문장(양식이 부하를 에이전트로 옮긴 설계 의도대로) ⓒ 승인은 diff 정독이 아니라 브리핑 신뢰에 근거 — 무해성·구조만 보는 §4.4 규정과 정합이나, "리뷰 시간"이 곧 검증 깊이는 아님을 뜻함. 이 실측이 나이 자동 머지 불채택의 근거가 됐다 — 방어 대상(적체)이 발생하지 않아 N을 정할 데이터도, 기능을 붙일 소비자도 없었다. 캘린더의 격주 배치는 비동기 리뷰 전제인데 이 배치는 동기였다 |
| 개정 비율 추이 (같은 4런) | [검증-실기] | 신규 31 · 개정 6. 런별 개정 비율 0%→11%→33%→18%. 코퍼스가 자라며 "기존 페이지 갱신이 본체"(§4.4-4)가 실제로 나타나기 시작 — 단 소스 성격이 교란(카프카는 신규 축, DDIA·Petrov는 기존 축과 교차). 재측정: 소스 30–50 도달 시 |
| 허브 포맷 3변형 LLM 파싱 실측 (2026-08-10, 12시행) | [검증-실기] | 실허브 15항목을 정형 md 리스트/YAML 블록/자유 산문으로 변형, Haiku 3회+상위 모델 1회씩 구조 추출+내비게이션 3문. 경로·내비는 3변형 전부 만점 — 결정성 변수는 포맷이 아니라 **문법 계약의 유무**: 정형 md=YAML 완전 동률, 자유 산문은 구획 배정이 4시행 4답·설명 매회 재서술. YAML 펜스 경로는 markdown-it 링크 토큰 미생성(edges 불인식, 코드 확인) → §2.6 문법 계약+§6 불채택 판정의 근거 |
| 계약 감사 (2026-08-10): 검사-관례 형식 분열 실증 | [검증-실기] | toc-missing 13건 전건 오검출(검사는 불릿형 기대, 저작 전수는 `**목차**` 문단형 — 형식 무계약의 표류가 도구-저작 간에 실발생) → §2.6 TOC 형식 성문+검사 정합으로 0건. claim 검사 단위 성문(부모 상속)으로 118→57건, locator 검사 신설 3건(진성). 본문 문자집합 검사는 정의 규약 자체가 부재 — 매트릭스에서 삭제 |
| 검색 4레그 예비 실측 (2026-08-07, qrels 26문항) | [검증-실기] | CLI 실사용 경로: hybrid R@5 0.910/신규 질의 ~10.5s(확장 캐시 후 0.8s) · vector 0.833/0.8s · morph 0.763/1.0s · bm25 0.250/0.2s(원어 alias 0.9 — 분업 실증). 빠른 2레그(vector+morph) top3 합집합은 도달률 100%(hybrid 동률)·R 0.859. **단서: 단일 도메인(DW)·도서 2권 표본.** 자산 evals/retrieval/(qrels·러너·결과). 재측정: 소스 30–50·3타입 도달 시 — 그때 ②임베딩 A/B·⑧허브 스코프 수행 |
| ksearch 질의 의미론 = 낱말 간 OR + bm25 (compound는 phrase 유지) | [검증-실기] | 암묵 AND는 기능어 형태소("어떻게"·"정해지나") 1개 결측에 전멸 + 섹션 단위 색인에서 흩어진 답 놓침 — qrels A/B: R@5 0.288→0.763, 주력(조사·활용·복합명사) 0.444→0.889, 악화 클래스 없음. stopword 목록 불채택(블랙리스트는 증식만). 전제 수정 포함: 질의는 전문 일괄 분석(Kiwi 문맥 민감 — 낱말별 재분석은 색인과 상이한 형태소를 냄, "완만하게" 실측). 재심: 코퍼스 확대 재측정에서 정밀도 열화 시 |
| kb-query 레그 우선순위 = hybrid 1순위 유지 | [검증-실기]+[선택] | 승급 신호 후보(2레그 합의도)가 판별 실패(저하 11건 중 1건 검출) — "미흡해 보이면 승급"은 스니펫 수준에서 성립 안 함. 빠른 병렬 1차(B′: 승급 트리거 = 0건/열어 읽은 페이지에 답 없음)는 성립하나 이득이 질의 빈도의 함수 — 재심: 실사용에서 kb-query 세션당 검색 횟수 관측 후. 놓침의 최종 방어선은 레그가 아니라 공백 선언+search-miss 규약 |
| qmd 2.1.0 `bench` 하네스 결함 | [검증-실기] | 내부 store API 경로가 vector/hybrid 전 질의 0건(동일 질의 직접 CLI vsearch는 정답 1위) — 검색 실측은 CLI 러너(evals/retrieval/runner.py)로 대체, 실사용 경로라 측정 타당성도 우위. 재확인: qmd 버전 갱신 시 |
| 고아 벡터 재실측 — 현 버전 검색 오염 0 | [검증-실기] | 통제 실험(생성→색인→삭제→update): cleanup 전에도 결과 미노출 — cleanup의 역할은 디스크 위생(vacuum). 구 "누수 실측 3회" 관측의 갱신 |
| 리뷰 실행 설계 보강 (2026-08-10 — PR 라운드의 스코프 공백 지적 적중) | [검증] | PR 기각은 그릇 판정일 뿐 리뷰 수행 절차가 무설계였음(스킬 ⑧이 기준 4줄뿐). 보강 = 에이전트 브리핑 3부(기계 요약·advisory 사전 검증·사람 체크리스트). 근거: 체크리스트의 누락 방지 실증(WHO 수술 체크리스트 — Haynes NEJM 2009, 사망·합병증 ~절반 감소; 한계 병기 "checklists alone won't prevent all errors"). 신규 집행층 성립: advisory 규칙은 기계 게이트 불가여도 **에이전트 보조 검증 가능**(예: stale_after 근거 URL 실대조) — validate(결정)·lint(리포트)·에이전트 검증(보조)·산문(advisory) 4계층 |
| PR 사전 리뷰 재심 (2026-08-10 — inbox 승격·리뷰를 PR로?) | [검증] 기각 | 리뷰 두 혈통 대조: 위키 계보=커밋-후-리뷰(Wikipedia BRD 기본·FlaggedRevs는 문제 페이지 예외·독일 Gesichtete 17년 라벨형·Nupedia 사전게이트 사망·AfC 실패=hiddenness) vs docs-as-code PR형(MDN·MS Docs — 전제: 다수 외부 기여자·main=발행 사이트·머지 전 숨김이 의도, 셋 다 부재). 킬러: 검색 레그는 main 색인이라 PR 브랜치=검색 밖 격리=AfC 재현 — inbox 라벨 격리는 "검색 가능한 격리"라는 의도 설계. 1인 셀프 PR은 시연·훈련 논거뿐, 실기능(머지 전 CI·원자 revert·diff)은 validate 훅·1런=1커밋·inbox diff가 기보유. 예외 존치: 대량 구조 변경의 일회성 PR, 멀티 에이전트 동시성(기존 트리거) |
| stale_after 의미론 재규정 (2026-08-10 — 날짜 예측의 허점 재심) | [검증] | 부패 관리 4방식 실증 대조: Wikipedia는 미래 날짜 템플릿({{Update after}})을 **아는 날짜**(올림픽 등)에 한정하고 모르면 as-of 관측 기록·단 "표시돼도 갱신 안 됨" 자인 / g3doc = last-reviewed+주기 나그(SWE at Google) / docs-as-code = last-verified+유형별 TTL / Zep·Graphiti = 모순 발생 시 invalid_at 사건 구동. 수렴: 미래 날짜는 기록용, 예측은 무선례. 본 시스템은 관측(verified[].at)·사건(supersession) 두 다리 기보유 — stale_after만 "공표 날짜 기록"으로 축소. 재심 트리거: 수용 검증에서 부패 실사례 관측 시 휘발성 클래스 리뷰(volatility+lint 계산) 도입 검토 — 단 **시계 리셋은 외부 재검증(upstream 재대조)만 적격**: 일반 verified 스탬프는 archive 스냅샷 대조라 내부 정합 증명일 뿐 외부 신선도 증명이 아니며, 사용 빈도는 신선도 신호가 아니다(2026-08-10 사용자 반례 적중) |
| 합성 멀티홉 코퍼스의 정답 어휘 누수 봉인 | [검증-실기] | 정답 페이지 제목·본문에 질의 토큰({korean})이 새고 있었고 암묵 AND가 은폐 — OR 전환이 flat R@10 1.0으로 폭로. 설계 계약("질의는 시드에만")을 synth.py 생성기에서 집행, 봉인 후 확장 우위 유지 확인 |
| restic 대조 심사 (2026-08-09 — borg·kopia·duplicacy·rustic) | [검증] | restic 0.19.1(2026-07) 활동·기여자 410·rest-server `--append-only` 요구 정합, 거버넌스는 BDFL(비재단 — 리스크 기록). borg 1.4 원격=SSH borg serve(B2 불가)·2.0 beta "not production"(b21, 2026-03). kopia 0.23.1이 race/data-loss 수정 + 2025 인덱스 비대·missing blob 이슈. duplicacy CLI 상용 $50/년 사설 라이선스. rustic 포맷 상호운용 공식 FAQ 확인·베타(회귀 테스트 부재) — 채택 아닌 승계 지명 |

## 참고 (주요 출처)

**계보·기질**: Karpathy LLM Wiki https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f · OKF 스펙 https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf · gwern https://gwern.net/about · https://gwern.net/archiving · 링크롯 실측(Zittrain) https://harvardlawreview.org/wp-content/uploads/2014/03/forvol127_zittrain.pdf · Voit 이식성 https://karl-voit.at/2026/04/08/obsidian-md-portability/ · 기업 위키 지속성 https://dl.acm.org/doi/abs/10.1145/1877725.1877731 · LLM 위키 구현 목록 https://github.com/gavischneider/awesome-llm-wiki · overview 진입 동형 선례 https://github.com/suwonleee/llmwiki

**granularity**: evergreen 회고 https://engineeringideas.substack.com/p/reflection-on-two-years-of-writing · 1만 노트 사례 https://forum.zettelkasten.de/discussion/1664/disillusioned-with-zettelkasten-method-am-i-doing-something-wrong · Schmidt 루만 연구 https://zettelkasten.de/posts/zettelkasten-hubs/ · Matuschak https://notes.andymatuschak.org/z2hQEhqWkdRLL9JUwfawZZx · WP:CONTENTFORK https://en.wikipedia.org/wiki/Wikipedia:Content_forks · WP 문서 크기 https://en.wikipedia.org/wiki/Wikipedia:Article_size · 규모 한계 현장 보고 https://theaioperator.io/p/i-rebuilt-karpathys-llm-wiki-heres

**쓰기 정책**: 리뷰 효과 붕괴 https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/ · Wikipedia NPP https://en.wikipedia.org/wiki/Wikipedia:New_pages_patrol/Analysis_and_proposal · 메모리 드리프트 https://arxiv.org/html/2603.11768v1 · https://arxiv.org/pdf/2605.17830 · 실사용기 https://www.rdworldonline.com/is-karpathys-viral-llm-wiki-helpful-mostly-yes-one-month-in/ · OAIS https://ccsds.org/Pubs/650x0m3.pdf · ISO 16363 https://ccsds.org/Pubs/652x0m2.pdf · Archivematica ingest https://www.archivematica.org/en/docs/archivematica-1.9/user-manual/transfer/transfer/ · Nupedia 회고(Sanger) https://features.slashdot.org/story/05/04/18/164213/the-early-history-of-nupedia-and-wikipedia-a-memoir · WMF AfC 연구(hiddenness) https://meta.wikimedia.org/wiki/Research:AfC_processes_and_productivity · Gesichtete Versionen https://de.wikipedia.org/wiki/Wikipedia:Gesichtete_Versionen · 봇 정책 https://en.wikipedia.org/wiki/Wikipedia:Bot_policy · 메모리 주입 공격 https://arxiv.org/abs/2503.03704

**검색·진입점**: FTS5 https://www.sqlite.org/fts5.html · Kiwi https://github.com/bab2min/kiwipiepy · nori STOP_TAGS https://github.com/apache/lucene/blob/main/lucene/analysis/nori/src/java/org/apache/lucene/analysis/ko/KoreanPartOfSpeechStopFilter.java · RRF https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf · 밀집 규모 저주 https://arxiv.org/abs/2012.14210 · 임베딩 이론 한계(LIMIT) https://arxiv.org/abs/2508.21038 · 하이브리드 강건성 https://arxiv.org/abs/2201.10582 · lost-in-the-middle https://arxiv.org/abs/2307.03172 · qmd https://github.com/tobi/qmd · basic-memory https://github.com/basicmachines-co/basic-memory · KURE https://github.com/nlpai-lab/KURE · NoLiMa https://arxiv.org/abs/2502.05167 · context rot https://www.trychroma.com/research/context-rot · 청킹 평가 https://www.trychroma.com/research/evaluating-chunking · llms.txt 실측(137k 도메인 로그) https://ahrefs.com/blog/llmstxt-study/ · Wikipedia 독자 행동 https://arxiv.org/abs/2112.11848 · Portal 실패 사례 https://en.wikipedia.org/wiki/Wikipedia:The_Problems_with_Portals · grep 하네스 https://arxiv.org/html/2605.15184v1 · Anthropic 도구 설계 https://www.anthropic.com/engineering/writing-tools-for-agents · 컨텍스트 엔지니어링 https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents

**그래프**: RAG vs GraphRAG https://arxiv.org/abs/2502.11371 · Louvain→Leiden https://arxiv.org/abs/1810.08473 · GraphRAG 증분 재검출 https://github.com/microsoft/graphrag/issues/741 · GraphRAG-Bench https://arxiv.org/abs/2506.05690 · 위키형 링크 추적 에이전트 https://arxiv.org/abs/2605.25480 · IRCoT https://arxiv.org/abs/2212.10509 · 하이퍼링크 탐색 검색 https://arxiv.org/abs/1911.10470 · HippoRAG https://arxiv.org/abs/2405.14831 · HippoRAG2 https://arxiv.org/abs/2502.14802 · LazyGraphRAG https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/

**멀티 KB·레이아웃·거버넌스**: Quartz https://quartz.jzhao.xyz · Astro content layer https://astro.build/blog/content-layer-deep-dive/ · dbt projects https://docs.getdbt.com/docs/build/projects · dbt Mesh https://docs.getdbt.com/best-practices/how-we-mesh/mesh-1-intro · Confluence labels https://confluence.atlassian.com/doc/add-remove-and-search-for-labels-136419.html · CONFCLOUD-7681 https://jira.atlassian.com/browse/CONFCLOUD-7681 · Jira scheme 자동생성 https://support.atlassian.com/jira/kb/creating-new-project-always-creates-a-new-issue-type-scheme/ · SharePoint content type publishing https://learn.microsoft.com/en-us/sharepoint/publish-content-type · k8s namespaces https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/ · Zotero groups https://www.zotero.org/support/groups · MediaWiki interwiki https://www.mediawiki.org/wiki/Manual:Interwiki · Global templates https://www.mediawiki.org/wiki/Global_templates · GitHub 저장소 한계 https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits · Capacities spaces https://docs.capacities.io/reference/spaces · Notion workspaces https://www.notion.com/help/intro-to-workspaces · Nx affected https://nx.dev/ci/features/affected · Rush rigs https://heft.rushstack.io/pages/intro/rig_packages/

**태그·ADR 불채택 근거**: Matuschak 태그 노트 https://notes.andymatuschak.org/Tags_are_an_ineffective_association_structure · 태그 vs 구조노트 https://forum.zettelkasten.de/discussion/1428/tags-vs-structure-notes · object 태그 https://zettelkasten.de/posts/object-tags-vs-topic-tags/ · Luhmann 키워드 색인(아카이브) https://niklas-luhmann-archiv.de/bestand/zettelkasten/schlagwortregister · Nygard ADR https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions · MADR https://adr.github.io/madr/ · ThoughtWorks ADR https://www.thoughtworks.com/en-us/radar/techniques/lightweight-architecture-decision-records · adr-tools #102 https://github.com/npryce/adr-tools/issues/102

**메타데이터·시간**: CSL https://docs.citationstyles.org/en/stable/specification.html · Better BibTeX https://retorque.re/zotero-better-bibtex/ · Obsidian Properties https://obsidian.md/help/properties · Wikidata 정밀도 https://www.wikidata.org/wiki/Help:Dates · YAML timestamp https://yaml.org/type/timestamp.html · citation-needed https://en.wikipedia.org/wiki/Template:Citation_needed · RFC 2119 https://www.rfc-editor.org/rfc/rfc2119

**구조·규약·운영**: llms.txt https://llmstxt.org · Anthropic best practices https://code.claude.com/docs/en/best-practices · Anthropic memory https://code.claude.com/docs/en/memory · markdown-it-py https://pypi.org/project/markdown-it-py/ · SRE SLO https://sre.google/sre-book/service-level-objectives/ · MoC https://notes.linkingyourthinking.com/Cards/MOCs+Overview · Diátaxis https://diataxis.fr/foundations/ · WP:SPLITTING https://en.wikipedia.org/wiki/Wikipedia:Splitting · WP:MERGE https://en.wikipedia.org/wiki/Wikipedia:Merging · EPPO https://everypageispageone.com/the-book/ · Google 파일명 https://developers.google.com/style/filenames · gwern design https://gwern.net/design · 어휘 문제(Furnas 1987) https://dl.acm.org/doi/10.1145/32206.32212 · WMT 용어 태스크 https://wmt-terminology-task.github.io/ · TTA 용어사전 https://terms.tta.or.kr · LLM translationese https://arxiv.org/abs/2503.04369 · en-ko 개체명 오역 실측 https://arxiv.org/abs/2504.20451 · 교차언어 lexical 붕괴(BGE-M3 §MKQA) https://arxiv.org/abs/2402.03216 · 이중언어 색인(McCarley) https://aclanthology.org/P99-1027/ · K8s 한국어 병기 규칙 https://kubernetes.io/ko/docs/contribute/localization_ko/ · 위키 기계번역 규정 https://en.wikipedia.org/wiki/Wikipedia:Translation

**평가**: ir_measures https://github.com/terrierteam/ir_measures · dbt-agent-skills https://github.com/dbt-labs/dbt-agent-skills · DeepEval https://github.com/confident-ai/deepeval · TruLens https://github.com/truera/trulens · MemDelta https://arxiv.org/abs/2606.29914 · superpowers https://github.com/obra/superpowers

**스킬·연동**: 스펙 https://agentskills.io/specification · 레포 https://github.com/anthropics/skills · 스킬 저작 가이드(계층별 크기 규범) https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices · Claude Code `.agents` 이슈 https://github.com/anthropics/claude-code/issues/31005 · 훅 https://code.claude.com/docs/en/hooks · Skills vs MCP https://lucumr.pocoo.org/2025/12/13/skills-vs-mcp/

**데이터 플랫폼(차용 어휘의 원전)**: Iceberg evolution https://github.com/apache/iceberg/blob/main/docs/docs/evolution.md · Iceberg maintenance https://iceberg.apache.org/docs/latest/maintenance/ · Confluent 호환성 https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html · Faiss 인덱스 가이드 https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index · Azure 임베딩 일치 https://learn.microsoft.com/en-us/azure/search/vector-search-how-to-query · SQLite 쿼리 플래너 https://sqlite.org/queryplanner.html

**백업·이관·토폴로지**: 12-factor logs https://12factor.net/logs · SQLite backup https://www.sqlite.org/backup.html · SQLite NAS https://www.sqlite.org/howtocorrupt.html · rest-server https://github.com/restic/rest-server · Ollama LAN https://docs.ollama.com/faq · ClickHouse UUID https://clickhouse.com/docs/en/sql-reference/functions/uuid-functions · Snowflake https://github.com/twitter-archive/snowflake · SQLite LTS https://www.sqlite.org/lts.html · GitHub 2FA https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/recovering-your-account-if-you-lose-your-2fa-credentials · LoC 아카이빙 https://digitalpreservation.gov/personalarchiving/ · restic https://restic.readthedocs.io/en/stable/045_working_with_repos.html · Syncthing FAQ https://docs.syncthing.net/users/faq.html

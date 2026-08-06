---
type: guide
title: 규약 설명서
description: 개념 페이지·소스 메타를 쓰는 법 — 규범은 schema/의 기계 게이트가 정본
---

# 규약 설명서

**이 문서는 설명서지 규범이 아니다.** 규범은 `schema/*.yaml` + `tools/validate`이고,
둘이 어긋나면 기계가 이긴다. 산문 규칙이 지켜진다고 가정하지 않는 것이 이 설계의 전제다.

설계 결정과 그 근거는 [PLAN.md](PLAN.md)에 있다. 여기서는 "그래서 어떻게 쓰는가"만 다룬다.

## 1. 파일 종류

`schema/layout.yaml`이 디렉터리와 `type`의 정합을 강제한다. **디렉터리는 뷰이고,
type의 정본은 frontmatter다** — 파일을 옮겨도 type이 따라 바뀌지 않는다.

| 어디에 | type | 무엇 |
|---|---|---|
| `<kb>/concepts/` | `concept` | 개념 페이지. 하나의 질문에 답하는 단위 |
| `<kb>/synthesis/` | `synthesis` | 인간 저작 종합. 허브(MoC)도 이것 |
| `<kb>/sources/` | CSL 타입군 | 소스 메타 1건 = 1파일 |
| `<kb>/inbox/` | `concept` + `status: draft` | 기계 산출물의 검역 구역 |
| 어디든 | `redirect` | 개명·이동·분할·병합의 잔여물 |
| `overview.md`, `SCHEMA.md` | `guide` | 진입·설명 문서 |

`<kb>/archive/`만 예외다 — 소스 원문 스냅샷이고 git에 들어가지 않는다.

## 2. 부재 = 기본값

이 규약의 중심 규칙이다. **값이 생길 때만 적는다.**

- `status` 없음 = stable · `verified` 없음 = 미검증 계층 · `stale_after` 없음 = 만료 없음
- `null` 자리표시 금지. 파서가 null과 부재를 구분하지 못한다.
- 빈 리스트 금지. `verified: []`는 "검증했는데 아무도 안 함"이 아니라 오류다.
- `status: stable`처럼 기본값을 명시하는 것도 금지다.

## 3. 개념 페이지

```yaml
---
type: concept
title: Raft 읽기 경로              # 표시 전용. 유일할 필요 없다. 한국어 유지
description: 한 줄 요약             # 검색 스니펫이 이걸 읽는다. 편집하면 갱신할 것
generated: { by: "claude-fable-5", at: "2026-07-31T05:00:00Z" }
sources:
  - { id: ongaro2014-raft, resource: /it/sources/ongaro2014-raft.md }
---
```

`generated.by`는 모델 id, 사람(`human:me`), 도구(`tools/kb-new`) 중 하나를 적는다.
인간이 썼어도 적는다 — **비워 두면 "출처 불명"이라는 뜻이 된다.**

### 본문

- **claim은 각주 달린 불릿이다.** 귀속은 본문 각주 `[^citekey]`로만 하고,
  페이지·절 같은 locator는 각주 텍스트에 적는다. frontmatter에 중첩 locator를 두지 않는다.
- **불확실한 것은 인라인 토큰으로 표시한다.** `#hypothesis`(근거는 있으나 미확정),
  `#speculation`(근거가 얇은 추측). 무표기 = 사실 서술. 숫자 confidence는 쓰지 않는다.
  이 둘이 어휘의 전부이고, 다른 `#토큰`은 lint가 잡는다 — 태그 체계는 없다.
- **한국어로 재서술하되 개념 첫 등장에 원어를 병기한다**: 영속성(persistence).
  역어가 흔들려도 원어가 불변 검색 키로 남는다. 확립 용어(TTA·국어원)를 우선하고,
  미확립이면 원어를 유지한다. 번역서는 역어 참조원이지 정본이 아니다 — 채택은
  건별 판단이고, 결정된 역어는 아래에 고정한다(전 페이지 구속, 개정은 이 파일).

  | 원어 | 확정 역어 | 왜 |
  |---|---|---|
  | additive / semi- / non- | 합산 가능 / 부분 합산 가능 / 합산 불가 | 뜻이 자명(가산 계열 기각 — 킴벌 국역판 채택례) |
  | surrogate key | 대리 키 | "대체 키"는 alternate key의 확립 역어라 충돌 |
  | dimension (table·attribute) | 차원 (차원 테이블·차원 속성) | 확립 역어. 팩트·허브·링크·새틀라이트는 확립 음차 유지 |
  | dimensional modeling | 차원 모델링 | "다차원"은 multidimensional DB와 구분 소실(킴벌 국역판 p.8 순환문이 반례 실물) |
- **정의·정리·수치처럼 왜곡에 민감한 구간은 번역하지 말고 원문을 직인용한다**(인용 블록).
  의미는 원문이, 해설은 한국어가 담당한다.

```markdown
## 읽기와 quorum

- leader lease 없이는 읽기에도 quorum 왕복이 필요하다 (§5.4 기준).[^ongaro2014-raft]
- #hypothesis lease 시계 드리프트 한계는 실무 문제 사례가 드물다.[^ongaro2014-raft]

[^ongaro2014-raft]: Ongaro 2014, §5.4
```

### 페이지 위생

- **한 페이지 = 하나의 질문.** 섹션이 다른 질문에 답하기 시작하고 그 자식이 자립
  가능할 때만 쪼갠다. 자식이 스텁이 되거나 부모 요약의 복제면 쪼개지 않는다.
- 100줄을 넘으면 상단에 TOC를 둔다. 500줄 경고는 백스톱이지 자동 분할 기준이 아니다 —
  1차 완화책은 분할이 아니라 TOC + 섹션 앵커다.
- H1은 파일당 하나(제목과 일치), 헤딩 레벨 건너뛰기 금지, H3–H4까지.
  H4가 필요해지면 분할 신호다.
- 쪼개거나 합칠 때는 `redirect` 스텁을 남긴다.

### 낡음과 모순

- `stale_after: "2027-06-01"` — 휘발성 있는 내용에만. lint가 만료 큐를 만든다.
- 대체되면 `status: deprecated` + `superseded_by: <슬러그>`. 둘은 함께 간다
  (`superseded_by`만 적으면 validate가 거부한다).
- 모순은 `contradicts: [상대-슬러그]`를 **양쪽에** 적는다. 자동 해소 금지 —
  해소할 때도 최신성만으로 판단하지 말고, 해소 날짜·결정 근거·대체된 주장을 페이지에 남긴다.

## 4. 소스 메타

```yaml
---
type: book
title: "Designing Data-Intensive Applications"
author: [{family: Kleppmann, given: Martin}]
issued: "2017"
publisher: "O'Reilly Media"
ISBN: "9781449373320"
edition: 1
snapshot: /it/archive/kleppmann2017-ddia/
snapshot_sha256: "e3b0c442…"     # ingest 시점 1회 기록. 이후 불변
accessed: "2026-07-31"
---
```

필드명은 CSL-JSON 원어 그대로다 — 대문자 `ISBN`/`DOI`/`URL`, 접근일은 `accessed`,
컨퍼런스명은 `event-title`, 영상 러닝타임은 `dimensions`. arXiv는
`number` + `publisher: "arXiv"`, RFC는 `number` + `collection-title` + `authority`.

**날짜와 번호는 반드시 따옴표 문자열로 적는다.** 따옴표가 없으면 YAML이
`2026-08-05`를 날짜 객체로, arXiv ID `2405.14831`을 부동소수점으로 바꿔 놓는다.
스키마가 그 실수를 거부한다.

확장 필드는 셋뿐이다: `snapshot`(로컬 스냅샷 루트), `snapshot_sha256`(변조 증거),
`custom: {archive-url: …}`(웨이백 URL). 그 밖에 필요한 CSL 필드가 생기면
`schema/source.yaml`에 선언 + 소비자 명시 + `migrations.md` 기록을 거친다.

원서와 번역서가 둘 다 있으면 **원서를 ingest한다.** 번역서는 확립 역어의 참조원으로만 쓴다.

## 5. 허브

허브는 포인터만 담는 `synthesis` 페이지다 — 링크 + 한 줄 설명, 자기 주장(claim) 없음.
그래서 각주도 `sources`도 없다. 본문 발췌·수치 복제는 금지다(진입점 부패 벡터).

**이름 범위 = 현재 내용 범위.** "데이터 아키텍처" 아래 도메인 중심 내용만 있으면
그 이름은 이미 과대 포장이고, 다른 계열이 들어오는 순간 description이 거짓이 된다.
이름을 내용만큼 좁게 잡으면 범위가 자랄 때 허브가 자라는 게 아니라 **형제 허브가
생기므로**, 이름도 description도 낡을 일이 없다. description은 편집할 때마다 재생성한다.

**크기와 분할.** 허브의 예산은 1–2k 토큰이다. `## Hubs` 목록은 10–30개, 허브의 링크가
~40개를 넘으면 lint(`hub-split-hint`)가 분할 후보로 올린다. 분할은 **부모–자식 패턴**이다
— 옛 허브가 자식 허브들을 가리키는 부모로 남으므로 가리키던 링크가 깨지지 않는다.
축을 정하고 링크를 배정하는 판단은 사람이 하고, 실행 실수는 게이트가 잡는다
(깨진 링크 = validate, 배정 누락 = orphan lint, 여전한 비대 = hub-split-hint 재발화).

고차수 허브가 검색을 망가뜨리지 않는 것은 도구가 보장한다 — 이웃 탐색이 차수
가중이라 허브 경유는 자동 강등된다. 분할이 지키는 것은 진입점 예산과 훑기 가능성이다.

## 6. 이름과 경로

### 개념 슬러그 = 파일명 = ID

영문 소문자 kebab, 80자 이내. 한국어 개념은 로마자화하지 말고 **영어 개념명으로 번역**한다
(확립 용어 우선). title은 한국어를 유지한다.

- 충돌은 **의미 한정자**로 푼다: `consistency-acid` vs `consistency-eventual`.
- 숫자 접미(`raft-2`) 금지. `raft-read-v2`처럼 의미 있는 한정자는 괜찮다.
- **날짜·번호 접두 금지(무예외).** `3-tier-architecture`는 안 되고
  `three-tier-architecture`로 쓴다.

### citekey = 파일명 = ID

`저자성last연도[-슬러그]`, 문자는 `[a-z0-9_.-]`만. 콜론·공백·대문자는 각주 앵커를 깨뜨린다.
같은 저자·연도 충돌에만 `-2`를 붙인다. 한국어 저자는 소스에 인쇄된 영문 표기를 우선하고,
없으면 발급 시점 RR 로마자화로 고정한다.

**유일성은 KB 안에서만 요구된다.** 저장소 전역 참조가 필요하면 `<kb>/<슬러그>`를 쓰는데,
이건 경로에서 파생되는 것이지 어딘가에 저장되는 값이 아니다.

### 발급 후 불변

이름은 바꾸지 않는다. 개명·이동은 `tools/rename`으로만 한다 — 링크 재작성, redirect
스텁 생성, 사후 링크 검사가 한 묶음이다. 손으로 `mv`하면 링크가 조용히 깨진다.

### 링크

| 무엇 | 형식 | 왜 |
|---|---|---|
| 본문 링크 | 파일 상대 경로 `../sources/x.md` | GitHub와 Obsidian이 합의하는 유일 형식 |
| frontmatter 경로 | 저장소 루트 기준 `/it/sources/x.md` | 인용하는 파일이 이동해도 안 깨진다 |
| KB 간 참조 | `qmd://<컬렉션>/<경로>` | 비권장 — lint가 warn한다 |

본문 링크는 **KB 안에서 닫혀야 한다.** 다른 KB를 참조하고 싶어지면 그건 대개 KB 경계를
잘못 그었다는 신호다. wikilink(`[[…]]`)는 쓰지 않는다 — CommonMark + GFM(테이블·각주)만.

OS 절대경로(`/Users/...`)는 어디에도 적지 않는다.

## 7. 쓰기 정책

계층마다 다르다.

- **`sources/`** — 사람이 큐레이션한다. 넣을 가치의 판단은 스크립트화되지 않는다.
- **`concepts/`** — LLM이 쓸 수 있다. 단 `inbox/`에 착지해서 diff 리뷰를 거친다.
  리뷰 기준은 **무해성·구조**(각주 없는 claim, 기존 claim 훼손, 명백한 오류)이지
  내용의 전수 정확성이 아니다. 정확성은 쓰는 시점에 검증한다(review-on-read):
  기계가 쓴 claim을 실제로 확인했으면 `verified`를 추가해 승급시킨다.
- **`synthesis/`** — 사람이 쓰고 전수 리뷰한다. 경계 기준은 **누가 썼는가**이지
  내용이 얼마나 종합적인가가 아니다.

## 8. 스키마를 바꿀 때

1. `tools/affected`로 영향 파일·KB를 **조회한다.** 기억하지 말 것.
2. **추가만 한다.** 기존 키의 의미를 바꾸거나 이름을 갈아끼우지 않는다.
   개명이 필요하면 새 키를 추가하고 매핑을 남긴다.
3. 은퇴시킨 키 이름은 **영구 결번**이다. `schema/migrations.md`의 결번 대장에 적고,
   validate가 그 목록을 신규 파일과 대조한다.
4. 스키마 변경과 콘텐츠 마이그레이션은 **같은 커밋**에 넣는다.

파일마다 `schema_version`을 적지 않는다. 콘텐츠 파일은 재작성되지 않으므로 그 필드는
시간이 지나면 거짓말을 한다 — git 커밋 날짜와 `migrations.md`가 해석을 제공한다.

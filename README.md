# syntopicon

IT 서적, 논문, 기술 문서를 10–20년 축적하는 개인 지식 시스템 모노레포.

> 이 문서는 지도다. 정본은 [`PLAN.md`](PLAN.md)이며(시스템 구성과 판정 원장 r1–r12),
> 각 레이어의 내부는 그 디렉토리의 PLAN이 정본이라 여기서는 구조만 조망한다.

- [레이어 구조](#레이어-구조)
- [지식 파이프라인](#지식-파이프라인)
- [백업, 보존, 인프라 토폴로지](#백업-보존-인프라-토폴로지)
- [규약 요지](#규약-요지)

## 레이어 구조

두 레이어가 한 저장소에 산다. 경계를 지키는 것은 저장소 분리가 아니라 계약이다(원장 r12).
지식은 승격 방향으로만 흐르고, 정본(core)에서 소모품(docs-mirror)을 참조할 수 없다.

```mermaid
flowchart LR
    subgraph EXT["외부 (Source of Record)"]
        UP["벤더 문서 upstream<br/>(dbt, Spark, ClickHouse …)"]
        SRC["책, 논문, 웹 소스"]
    end

    subgraph REPO["alteralab/syntopicon (모노레포)"]
        subgraph DM["docs-mirror/ 캐시 레이어"]
            MIR["mirrors/ (git 제외)<br/>클론 미러, 버전=디렉토리"]
            GLUE["글루: tools/mirror CLI<br/>sources.yaml + schema"]
        end
        subgraph CORE["core/ 정본 KB (md + git = SoT)"]
            IT["it/ concepts, synthesis<br/>sources, inbox, archive"]
            CG["글루: tools, schema<br/>skills, evals"]
        end
        PLAN["PLAN.md + research/<br/>시스템 정본, 원장 r1–r12"]
    end

    UP -- "주간 pull (launchd)" --> MIR
    SRC -- "kb-ingest" --> IT
    MIR -- "승격: 불변 가치만<br/>(kb-ingest 단방향)" --> IT
    CORE -. "참조 금지" .-x DM
```

## 지식 파이프라인

### 쓰기 경로 (kb-ingest, 소스당 1런 = 1커밋)

```mermaid
%%{init: {"sequence": {"width": 140, "messageMargin": 28, "boxMargin": 12}}}%%
sequenceDiagram
    participant H as 인간
    participant T as 결정적 도구
    participant L as LLM
    participant K as KB 저장소

    H->>T: 소스 선택 (큐레이션이 첫 게이트)
    T->>T: 스냅샷과 sha256 저장 (archive/, 소급 불가라 최전방)
    T->>K: citekey 발급, 소스 메타 기록 (CSL)
    L->>K: 개념 페이지 갱신 (신규보다 기존 10–15쪽 터치)
    note over K: inbox/ 격리, unreviewed 라벨<br/>검색에는 노출된다
    T->>T: validate (pre-commit 게이트)
    loop 위반이면 통과까지
        T-->>L: 위반 목록
        L-->>T: 수정 반영, 재검
    end
    T->>K: 커밋 (Ingest 트레일러)
    H->>K: 리뷰와 머지 (무해성과 구조만, 정확성은 이연)
    T->>T: 재색인 (qmd 파생 인덱스 갱신)
```

### 읽기 경로 (kb-query)

```mermaid
%%{init: {"sequence": {"width": 140, "messageMargin": 28, "boxMargin": 12, "actorMargin": 108}}}%%
sequenceDiagram
    participant H as 인간
    participant S as 색인과 검색
    participant K as KB 저장소
    participant M as docs-mirror

    alt KB 질의 (개념, 소스, 판단)
        H->>S: 질의 (검색 4레그)
        S-->>H: 히트 정독, 링크 이웃 확장 (공백은 search-miss 계측)
        H->>K: 읽으며 검증한 claim에 승급 스탬프 (review-on-read)
    else 벤더 문서 질의 (버전 종속 사용법)
        H->>M: docs-query (라우팅, rg, 정독, 무색인)
        M-->>H: 답은 upstream 정식 인용으로
    end
```

기계가 쓴 claim은 쓰기 경로에서 격리와 라벨로 들어오고, 읽기 경로에서 사람이 읽는
순간마다 조금씩 검증 등급이 올라간다. 전수 검수 대신 이 순환이 정확성을 담당한다.

검색은 색인 파이프라인이 아니라 에이전트가 도구를 고르는 구도라서, 벤더 문서 질의는
`/docs-query`(라우팅, rg, 정독의 무색인 절차)로 넘어간다. 스킬 다섯(`kb-query`,
`kb-ingest`, `kb-lint`, `kb-new`, `docs-query`)은 `~/.claude/skills/` 심링크로
어느 프로젝트에서든 부를 수 있고, 정본은 각 레이어의 `.agents/skills/`에 있다.

## 백업, 보존, 인프라 토폴로지

백업은 데이터가 태어나는 맥북에서 돈다. NAS는 공유기 포트를 하나도 열지 않고,
접근은 Tailscale tailnet뿐이다.

```mermaid
flowchart TB
    subgraph MAC["MacBook 주 작업기 (데이터 출생지)"]
        WORK["작업 사본 + 로컬 인덱스"]
        BK["일간 백업 launchd 21:00<br/>bundle, 인덱스 사본, restic"]
    end

    subgraph NAS["Synology NAS (tailnet 한정 접근)"]
        REST["restic rest-server<br/>--append-only"]
    end

    subgraph GH["GitHub"]
        MONO["alteralab/syntopicon<br/>(모노레포, private)"]
        FORK["syntopicon-mirrors org<br/>(미러 upstream의 public fork)"]
    end

    WORK -- "commit + push" --> MONO
    BK -- "스냅샷: it, toolchain, mirror 태그" --> REST
```

| 보존 겹 | 담당 | 막는 위협 |
|---|---|---|
| 0겹 (0원) | GitHub fork(`syntopicon-mirrors`)와 Software Heritage | 미러 upstream 소멸 |
| 백업 3계층 | git bundle, 인덱스 사본, restic에서 NAS(append-only)로 | 로컬 소실, 랜섬웨어 |
| 이연 (트리거: archive 성장) | B2 오프사이트 | 집 단위 재해 (지금 실노출은 archive/뿐) |

백업 자격증명 관리와 NAS 컨테이너 배포는 이 시스템이 아니라 홈랩 인프라의 소관이다
(정본은 `alteralab/portainer` 저장소의 런북들).

## 규약 요지

- 커밋 제목은 `<레이어>/<영역>: 요지`(예 `core/tools:`, `mirror/plan:`, 루트 문서는 `plan:`과 `research:`), 한 커밋은 한 레이어만 만진다
- 게이트는 `git config core.hooksPath core/tools/githooks` 한 번으로 활성화된다(기기당)
- 글루는 자기 레이어 안에 둔다(루트에 종류별 디렉토리 금지, r4와 r12). 구조를 바꾸려면 원장에 근거부터
- 새 기기 복구는 이 저장소를 clone한 뒤 `core/PLAN.md` §5 런북을 따른다

<sub>2026-08-09 기준. 세부 수치와 결정 근거는 각 PLAN과 `research/`에 있다.</sub>

---
name: docs-query
description: docs-mirror의 벤더 기술 문서를 검색한다 (dbt·Spark 등 버전 따라 변하는 문서). 라우팅→rg→정독의 무색인 절차. 벤더 문서에서 설정·API·동작을 확인할 때, 특정 버전 기준으로 문서를 봐야 할 때 사용. 이슈·버그 맥락은 미러가 아니라 온디맨드(gh·JIRA)로 간다.
---

# docs-query — 미러 문서 검색 (PLAN §4 0단계: 무색인)

미러 위치: `~/workspace/syntopicon/docs-mirror/mirrors/<tech>/<version|current>/`
레지스트리: `~/workspace/syntopicon/docs-mirror/sources.yaml` (등록 기술·fallback 목록)

**`current/` = 최신 릴리스** (기본 브랜치 아님 — PLAN §2). 어느 릴리스인지는 `sources.yaml`의
`pinned` 또는 `mirror status`가 보여준다. **최신 릴리스가 곧 사용자의 버전은 아니다** — Spark처럼
여러 라인을 동시 유지하는 소스에서 사용자가 구버전을 쓰면 `versions:`의 고정 워크트리를 봐야 하며,
질의에 버전이 명시되면 그 디렉토리를 우선한다(없으면 아래 절차로 추가).

## 절차

1. **신선도 확인 (lazy 보정)**: `tools/mirror status`로 미러 나이 확인. 질의가 최신성에
   민감한데 미러가 오래됐으면(주 단위 이상) `tools/mirror pull` 후 진행.
2. **라우팅**: 미러 안의 벤더 llms.txt가 있으면 그것이 인덱스(dbt는 소스에 포함).
   없으면 파일 트리·sidebar 설정(`sidebars.js`·`mkdocs.yml` 등)으로 섹션을 좁힌다.
3. **검색**: 질의를 **영문 원어 키워드로 변형**해서(코퍼스가 영문) rg 실행.
   버전 스코프는 경로 glob이 전부다:
   - 최신 릴리스: `rg -il 'incremental strategy' mirrors/dbt/current/`
   - 버전 고정: `rg -il 'shuffle partitions' -g 'spark/3.5.9/**' mirrors/`
   - 버전 대조: 같은 질의를 두 버전 디렉토리에 각각 실행 후 정독 비교.
4. **정독**: 히트 파일을 직접 읽는다. 요약을 mirrors/에 저장 금지(원칙 2 — 인간 저작물 제로).
5. **폴백 (미러에 없거나 최신성 의심)**: sources.yaml의 해당 기술 `fallback` URL로
   온디맨드 조회(llms.txt 인덱스 → 페이지 fetch).
5b. **온디맨드 소스 (`mode: ondemand` — 사본 없음)**: 레지스트리의 `index`·`page_suffix`·
   `search`·`mcp`를 쓴다. **URL 우선, MCP는 보완**(PLAN §2).
   - AWS 예: 검색 → 색인 → 페이지 순으로 좁힌다.
     ```sh
     # 전문 검색 (인증 불필요) — 결과의 .link 를 얻는다
     curl -s -X POST https://proxy.search.docs.aws.com/search -H 'Content-Type: application/json' \
       -d '{"textQuery":{"input":"glue job bookmark"},
            "contextAttributes":[{"key":"domain","value":"docs.aws.amazon.com"}],
            "acceptSuggestionBody":"RawText","locales":["en_us"]}' \
       | jq -r '.suggestions[].textExcerptSuggestion | "\(.title)\t\(.link)"' | head
     # 가이드 색인이 필요하면: <가이드 경로>/llms.txt
     # 페이지 정독은 마크다운 쌍으로: <페이지 URL>.md
     ```
   - 검색이 실패하거나(비공식 엔드포인트) 리전 가용성·What's New처럼 문서 밖 질의면
     `mcp` 엔드포인트로 간다. 등록 안 돼 있으면 사용자에게 등록을 제안하되 임의 설정 변경 금지.
6. **이슈·버그 맥락은 미러 비대상 — 온디맨드 전용**:
   - GitHub: `gh search issues --repo <owner/repo> '<키워드>' ` (코멘트까지: `in:comments`)
   - Spark·Kafka는 JIRA가 정본: `https://issues.apache.org/jira/rest/api/2/search?jql=...` (익명 가능)

## 금지

- mirrors/ 아래 파일 생성·수정 일체 (검색 결과 요약 저장 포함) — 경계 위반.
- 검색으로 얻은 불변 가치 통찰의 보관은 kb-ingest(core 승격, §6)로 — 이때 인용은
  미러 경로가 아니라 upstream 정식 URL + 버전.
- mirrors/에 대한 파괴 연산(rm·reset)은 사용자 명시 지시 없이 금지 (PLAN §3).

## 버전 워크트리 추가 (수요 발생 시에만)

```sh
cd mirrors/<tech>/current
git tag --list 'v3.5.*' --sort=-v:refname | grep -v rc | head -3   # 그 라인의 최신 릴리스 확인
git worktree add ../3.5.9 v3.5.9        # 디렉토리명 = 패치까지의 완전한 버전 ('3.5' 금지)
# 이후 sources.yaml의 versions에 디렉토리명 기록
# validate가 워크트리 HEAD의 태그와 디렉토리명 일치까지 검사한다
```

워크트리는 본 clone의 sparse-checkout을 상속한다(cone 모드라 저장소 루트 파일은 항상 포함).

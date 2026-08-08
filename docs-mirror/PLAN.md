# docs-mirror 계획

버전 따라 변하는 벤더 기술 문서(dbt·Spark·ClickHouse 등)의 **로컬 미러 + 에이전트 검색 레이어**. 2026-08-08 초판(같은 날 정리판). 결정별 근거는 §8 검증 원장 — 전문(claim·검증 판정·URL)은 우산 `research/r*`.

**정체성: 이 레이어는 지식 베이스가 아니라 캐시다.** syntopicon core(md+git = source of record)와 달리 여기의 모든 콘텐츠는 upstream에서 재생성 가능한 **파생물**이며, `rm -rf mirrors/` 후 재클론으로 완전 복구되어야 한다. 이 성질이 깨지는 파일이 생기는 순간 경계 위반이다.

**전제**: 유지비 최소가 존재 이유다. core의 유지비 예산(2–3주당 30–45분)을 잠식하지 않는다 — 정상 상태 유지비 목표는 **0에 수렴**(cron pull 외 무개입).

## 1. 원칙

1. **SoR은 upstream, 여기는 캐시.** 진실의 원천은 벤더의 문서 저장소/사이트. 미러는 가용성(오프라인·소실 방어)·버전 고정·검색을 위한 사본일 뿐이다.
2. **인간 저작물 제로.** `mirrors/` 아래에 사람이 쓴 파일 금지. 메모·요약·판단이 생기면 그것은 지식이므로 core로 보낸다(§6).
3. **수집은 git 미러 우선.** 문서 소스가 공개 git 저장소면 clone이 곧 스냅샷+이력+버전(tag)이다. `git pull` = 증분, `git diff` = 변경 감지, `git checkout <tag>` = 버전 고정.
4. **색인은 필요가 실측되기 전까지 만들지 않는다** (core 원칙 5의 적용 — 색인은 retrofit O(1) 파생물). 0단계는 무색인: 라우팅 → `rg` → 파일 정독(§4).
5. **백업하지 않는다.** restic·검증 원장·lint 비대상. 이 저장소의 git은 글루(계획·스크립트·스킬)만 담고 `mirrors/`는 ignore. 단 보존 보험은 캐시 밖 계층이 담당(§3.5).
6. **core → docs-mirror 방향 참조 금지.** 정본이 소모품을 가리키면 소모품이 소모품이 아니게 된다. 인용이 필요하면 upstream 정식 URL + 버전을 쓴다. 역방향(승격)만 허용(§6).
7. **온디맨드 폴백 병행.** "지금 최신이 뭐냐"류 일회성 질의는 공식 경로(벤더 llms.txt·페이지 `.md`·공식 MCP)가 더 싸다. 미러가 이기는 것은 버전 고정 작업·반복 조회·횡단 검색·오프라인이다.

## 2. 저장 구조

```
docs-mirror/                 # git 저장소 (글루만 커밋)
  PLAN.md                    # 이 파일 — 정본 계획
  sources.yaml               # 미러 대상 레지스트리
  sources.schema.json        # 레지스트리의 계약 (에디터·CI 검증)
  tools/                     # mirror/pull/변환/상태 스크립트 (결정적, LLM 무관)
  .agents/skills/docs-query/ # 검색 스킬 1개 (라우팅→rg→정독 절차)
  .gitignore                 # mirrors/  (`mirrors/**` 아님 — 디렉터리 표기라야 git이 프룬)
  mirrors/                   # ★ git 제외 — 전량 재생성 가능 영역. 최상위에 CACHEDIR.TAG
    dbt/current/             #   git clone dbt-labs/docs.getdbt.com
    spark/3.5/  spark/4.0/   #   버전 고정이 필요한 기술만 tag별 워크트리 분리
    _converted/<tech>/       #   비-md 소스(rst·DocBook)의 md 변환 산출물 — 역시 재생성 가능
```

- **버전 = 디렉토리.** `mirrors/<tech>/<version|current>/` — 경로 glob이 곧 버전 스코프(`rg -g 'spark/3.5/**'`). 별도 버전 스키마·메타 테이블 없음. 고정 버전은 필요해질 때만 추가(선제 생성 금지).
- **sources.yaml이 대상의 정본**: 기술별 `repo`(또는 `crawl` 폴백)·`subdir`(sparse-checkout)·`format`(md|mdx|rst|docbook)·`license`(필수)·`versions`(고정 태그, 코드 미러 채택 시 commit SHA 병기)·`fork`(§3.5 0겹 URL)·`fallback`(llms.txt·공식 MCP·이슈 트래커).
- **레지스트리 관리 = 3요소 패턴**(파일=상태 + `sources.schema.json`=계약 + CLI 동사=연산): `tools/mirror validate | add <repo> | pull | status`. `add`는 clone+fork 생성+SWH 등록+항목 기록의 복합 연산(§3.5의 실행자). 카탈로그 서비스·CRUD REST는 불채택(§7, 근거 r10·r11).
- **수집 우선순위**: ① git clone(+sparse-checkout) ② 비-md 저장소는 clone + 결정적 변환(`_converted/`) ③ git 소스 없는 사이트만 크롤(trafilatura, sitemap) — 크롤은 최후 수단.

## 3. 갱신 운영

- `tools/mirror pull` 하나로 전 미러 갱신: `git pull --ff-only`(고정 버전 디렉토리는 skip), 변환 대상은 변경 시에만 재변환. 실패는 fail-loud 목록 출력 — 조용한 스킵 금지.
- 주기: cron 주 1회면 충분. 갱신 주기는 규약이 아니라 운영 파라미터.
- 추가·제거 = `tools/mirror add` / sources.yaml 편집 + `rm -rf mirrors/<tech>` — 캐시이므로 절차 없음.
- **기기 교체 = 캐시 계약의 정상 발동, 이주 대상 아님.** 새 기기에서 glue repo clone + `tools/mirror pull`이 곧 이주 절차(문서 5종 실측 5.25GB — 재클론 수 분~수십 분, r8). Migration Assistant 통째 이동도 안전(정지 상태 전체 복사; worktree는 `git worktree repair` 1회). `mirrors/`의 CACHEDIR.TAG로 restic 등 백업 도구가 무설정 제외.

## 3.5 보존 계층 — upstream 소멸·대용량 축적 대비 (근거 r8·r9)

미러 자체는 무백업이지만, "과거 시점을 다시 얻을 보장 없음"의 보험은 캐시 밖 4겹이 담당한다:

- **0겹 (상시·0원) — GitHub fork**: 미러 대상을 내 계정에 fork. 공식 보장 — public upstream 삭제 시 fork 생존, private 전환 시에도 public fork 존속, 자동 sync 부재라 force-push가 이력을 소급 파괴하지 못함(간헐 수동 sync). fork URL은 sources.yaml에 기록.
- **0겹-보조 (0원) — Software Heritage**: 신규 등록 시 save-code-now API로 공공 아카이브 등록(GitHub URL 자동 승인, Vault git-bare 복원 지원).
- **1겹 (현행 5–30GB) — core restic 타깃 편승**: core restic 원격(B2 후보)에 mirrors/ 스냅샷을 `mirror` 태그로 통합(한계비용 연 ~$2.50, 태그별 보존 정책 분리 공식 지원). **git 백업 규율**: `gc.auto=0` + 재클론 금지(fetch 증분만) + prune 금지 — packfile 재작성의 restic dedup 파괴 완화 + 삭제 브랜치 로컬 잔존 보장.
- **2겹 (~100GB 돌파 시) — 월간 bundle 체인 → 콜드**: `git bundle`(full 1 + 월간 증분, `verify` 필수, 수년 주기 re-baseline) → S3 Glacier Deep Archive($0.00099/GB-월, 500GB 20년 ≈$119, Bulk 복원 ≤48h). 콜드에는 self-contained 파일만(restic repo 통째 불가). 이때 restic 쪽은 유한 보존(`--keep-monthly 12`) 전환.
- **크롤 산출물**: Wayback SPN2 API(인증 30,000/일)로 렌더링본 시점 보존 병행.

## 4. 검색 — 0단계는 무색인, 색인은 게이트 통과 후

**0단계 (현행): 라우팅 → rg → 정독.**

1. **라우팅**: 미러 내 벤더 llms.txt(dbt는 소스 저장소에 포함)가 인덱스, 없으면 파일 트리·sidebar 설정. 스킬이 기술별 라우팅 규칙 안내.
2. **검색**: `rg` + 경로 glob(버전 스코프). 질의는 **영문 원어 키워드로 변형**(코퍼스가 영문 — 한국어 형태소 불필요).
3. **정독**: 히트 파일을 에이전트가 직접 읽는다. 검색 결과의 요약 저장 금지(원칙 2).
4. **폴백**: 미러에 없거나 최신성 의심 시 sources.yaml `fallback`으로 온디맨드. **이슈·버그 맥락은 미러 대상이 아니라 온디맨드 전용** — `gh search issues`(`in:comments` 지원)·Apache JIRA 익명 REST(Spark·Kafka는 JIRA 정본).

참조 설계도: dbt 공식 `fetching-dbt-docs` 스킬(llms.txt 라우팅→키워드 검색→페이지 정독, 무색인)의 로컬 미러 버전.

**게이트 (색인 도입 조건)**: 실사용 누적 후 소규모 qrels A/B로 다음 중 하나가 실측될 때만 — (a) rg 루프의 miss율·토큰 비용이 아픔 (b) 버전 병존 조회(v1.7 vs v1.8 대조)의 반복 수요.

**1단계 (조건부 — pain 하나에 도구 하나, 동시 도입 금지)**:

| 실측된 pain | 도입 | 비고 (근거 r2) |
|---|---|---|
| 버전 병존 조회 | **arabold/docs-mcp-server** — `file://` 미러 투입, 버전 1급 스키마(semver 검색), ETag/mtime 증분, 색인에 LLM 불요, CLI+MCP | 카테고리 유일 성숙 완성품. bus factor 1이나 색인=파생물이라 할인 |
| 의미 검색 miss | **qmd 별도 컬렉션** — 임베딩 Qwen3-Embedding-0.6B | 기존 스택 재사용. qmd 리스크는 §8 r2 |

## 5. core와의 경계 계약 (동결)

1. `mirrors/`(및 `_converted/`)는 언제든 삭제 후 재생성 가능 — 인간 저작물 제로.
2. 이 레이어는 restic·kb-lint·검증 원장 비대상. core의 스키마(frontmatter·citekey·각주) 미적용.
3. core → docs-mirror 링크 금지(원칙 6).
4. 지식 이동은 승격 단방향만(§6).

## 6. 승격 경로 — 미러에서 core로

**불변 가치가 있는 통찰**(설계 원리·트레이드오프·버전 관통 패턴)만 kb-ingest 정규 파이프라인으로 core에 들어간다:

- claim에 **버전 조건 명시**(예: "dbt 1.8부터 unit tests 지원") + `stale_after` — 버전 종속 사실이 이 필드의 설계 용도다.
- 소스 귀속은 미러 경로가 아니라 **upstream 정식 인용**(스냅샷은 kb-ingest가 담당 — 미러가 스냅샷을 대신하지 않는다).
- 릴리스 노트 나열·현행 API 사용법 같은 휘발 정보는 승격 금지 — 그것이 미러의 존재 이유다.

## 7. 불채택 표 (요지 — 상세 근거는 §8의 해당 라운드)

| 후보 | 기각 요지 | 근거 | 재심 조건 |
|---|---|---|---|
| cocoindex | 웹 크롤러 소스 없음(수집 미해결)·2인 회사·13개월 만 v1 breaking. 증분 임베딩 강점은 git pull이 대체 | r1 | 임베딩 재계산이 실측 병목 + 1.x 안정 유지 시 |
| GraphRAG 계열 | 색인=LLM 추출이라 갱신량 비례 비용, MS는 append 전용, 버전 질의 정확도 64% | r2 | 없음 |
| temporal KG (Graphiti 등) | agent memory 도메인 — 문서 검색 용도 불일치, open-core 후퇴 실증 2건 | r2 | 없음 |
| RAG 플랫폼 (Dify·RAGFlow 등) | 1인 맥북에 과체중(16서비스·16GB급), 버전 1급 0/12, 3년 사망률 높음 | r2 | 없음 |
| Meilisearch 즉시 채택 | 상주 서버+글루 자작 = 예산 잠식. 무색인 성립 규모에서 선제 도입은 원칙 4 위반 | r2 | 색인 게이트 통과 + 형태소 엔진 내장 필요 시(승계 1순위) |
| llms-full.txt 통독 | 대형 프로젝트 통독 불가(dbt 10.5MB≈2M+ 토큰) | r1 | 없음 — llms.txt 인덱스+페이지 fetch는 폴백으로 채택 중 |
| 클라우드 문서 서비스 의존 (Context7 등) | 사설 미러 투입 불가·색인 통제권 없음·종료 실증(docfork)·injection 사례 | r2 | 보조 참고용은 자유 — 기반으로는 불가 |
| 버전별 코드 미러 | **보류(기각 아님)** — 근거 확보(GitHub 코드 검색은 default branch만 색인 → 버전 고정 분석은 로컬 clone 유일, 비용 경미)됐으나 수요 미실측 | r3 | 수요 반복 실측 시. 동결 규약: blobless clone 1개 + `git grep <tag>` + 정독 버전만 worktree + SHA 고정 + `.rgignore`. 채택 시 레이어명 재검토 |
| 이슈 전량 미러 | 캐시 계약 3중 위반 — 버전 축 부재(milestone 0.0%)·재수집 비결정(코멘트 API 30k 캡·tombstone 없음)·closed 이슈도 계속 변함. Spark·Kafka는 JIRA 정본 | r3 | 없음 — 온디맨드(§4) + 유용 스레드만 core 승격이 상시 경로 |
| 상시 동기화 중앙 미러 (S3 sync·NAS·자가 객체 스토리지) | 보존은 §3.5가 담당 — 크기 전제 반증(실측 5.25GB)·캐시 무이주 관행·중앙 복원은 이득 0에 계정 존속 리스크만 추가(AWS 해지 후 90일 뒤 삭제·MinIO 커뮤니티 붕괴·HDD 수명 6.75년). git 콘텐츠에 S3 API 불필요(fsck·SSH·증분 내장), S3 Tables는 Iceberg 표 전용이라 파일 보관 부적합 | r8·r9 | crawl 산출물 비중 증가(그 부분만 백업 경계 승격) / 다기기 동시 소비 / 종량제·극저속 회선 |
| 카탈로그 서비스·CRUD REST API | Polaris 전제(멀티 엔진·동시 writer CAS·RBAC·credential vending) 전부 부재. Backstage조차 source of truth는 git 내 YAML(서비스는 harvest 파생). 로컬 REST 선례 6종 전수가 비파일 클라이언트용 파사드 — "쓰기 규칙 집행용 1인 REST" 선례 0건. 집행점은 커밋 게이트가 표준, 메타스토어 정본화는 dual-write 자초 | r10·r11 | 비파일 클라이언트·멀티유저·git 비경유 쓰기 경로 등장 시 — 그때도 파일 정본 유지 파사드형만 |

## 8. 검증 원장 (라운드별 요약 — 전문·검증 판정·URL은 우산 `research/r*`)

번호는 시스템 원장(우산 PLAN §3)과 공유한다. 전부 2026-08-08, 적대 검증 포함.

- **r1** (레이어 분리·수집·llms.txt, 12 에이전트): DDIA SoR/derived 프레임·kb-new 게이트로 분리 확정. dbt 문서 저장소 월 200+커밋(박제 즉시 낡음). git 미러 성립 — dbt(md/MDX)·React·Spark·Kafka 확인, Airflow(rst)·PostgreSQL(DocBook)은 변환 필요, ClickHouse 미확인. 소실 방어 — Pew: 1년 내 ~8%·10년 내 38% 소실, dbt EOL 문서 제거. 버전 — llms.txt 스펙에 버전 메커니즘 없음, GitChameleon 버전 조건 정답률 48–51%(문서 공급 시 +6.7~10%p). 통독 불가 — llms-full: dbt 10.5MB·Cloudflare 56.7MB(직접 curl).
- **r2** (도구 지형 전수, 12): 무색인 성립 — Claude Code의 RAG→agentic search 교체(Cherny 원문), Amazon AAAI 2026 grep 에이전트 91.5% attainment, 성능 경계(원조 grep 100만 파일 4초)는 미러 규모의 2–3자릿수 위. docs-mcp-server 실사 — 버전 1급·증분·LLM 불요·`file://`(코드 수준 확인), bus factor 1. qmd 실사(core에도 해당) — tobi 개인 프로젝트·커밋 78% 단독·sqlite-vec 의존 pre-1.0 alpha·한국어는 형태소 아닌 문자 단위 정규화(소스 확인). 미확인: 한국어 grep miss율 정량 연구 부재(게이트 A/B가 결정 경로).
- **r3** (코드·이슈 확장, 12): 코드 미러 — GitHub 코드 검색 default branch 한정(공식), 저장소 실측 dbt-core 87MB~ClickHouse 9.8GB, 문서 저장소가 코드보다 큰 경우 5중 4 → 근거 동결·보류. 이슈 — milestone 0.0%(ClickHouse 3만 건)·코멘트 API 30k 하드 캡(422 재현)·closed 이슈 계속 변함·JIRA 이원화 → 기각, gh search/JIRA 온디맨드 충분성 실증. GitHub AUP상 API 수집·사적 아카이브 허용.
- **r8** (중앙 저장소 1차 심사, 8): 문서 5종 실측 합계 5.25GB(5,505,102KB), 20–30개 확장 10–30GB, blobless 시 수 GB(GitLab 97% 절감 사례). 기기 교체 3안 — Migration Assistant 자동 이전·재클론 10GB≈13분(100Mbps)·중앙 복원은 이득 0. 캐시 무이주 관행 — macOS TM이 ~/Library/Caches 기본 제외(tmutil 실측)·CACHEDIR.TAG 규격.
- **r9** (보존 공간, 8): fork 생존성 공식 확정(public 삭제 시 존속·활성 fork 승격·force-push 비전파). SWH save-code-now API 실재(origins 4.38억 실측). restic×git packfile dedup 붕괴 실증(완화: gc.auto=0·fetch 증분). git bundle 증분 체인 = 시점 동결 최적. 단가 실측 — B2 $6.95/TB-월(500GB 20년 $834)·Deep Archive $0.00099/GB-월(500GB 20년 $118.80)·Wasabi 탈락(1TB 최소과금)·S3 Tables/Express One Zone 부적합·Garage/SeaweedFS/Ceph 부적합·NAS 20년 $3,000–4,500(자가 임계 2–3TB+). **정정**: AWS 해지 후 보존은 90일(30일은 미납 지불 기한 — r8 시점 기술을 정정). restic 0.18의 S3 cold 지원은 실험(alpha)이라 불채택.
- **r10·r11** (레지스트리 관리·REST 심사, 10): Polaris = 멀티 엔진 상호운용·동시 writer CAS·RBAC·credential vending·Java+PostgreSQL 상시 — 전제 전부 부재. Backstage: source of truth는 git 내 YAML. 파일→서비스 승격 4변수(동시 writer>1·신뢰 경계·전량 복사 불가 질의·네트워크 분리) 전부 미충족 — crates.io는 176MiB·수백만 소비자에서도 동적 API 기각. 3요소 패턴이 표준형(pre-commit `validate-config`/`autoupdate`·dbt deps+lock·SchemaStore 1,414 스키마 실측). 로컬 REST 선례 6종(Obsidian Local REST API 등) 전수 = 비파일 클라이언트용 파사드, Home Assistant는 이중 표면 유지비로 YAML 축소 실증. 집행점 — Google presubmit·MDN·dbt 전부 커밋 게이트, 서비스 시점이 이기는 조건 3개(비git 쓰기 경로·익명 다수 writer·ms 경합) 전부 부재.

**재평가 트리거**: ⑴ qmd 6개월 무활동 또는 sqlite-vec 사망 → 승계(완제품 Meilisearch — 한국어 Lindera ko-dic 기본 활성 확인 / 재조립 LanceDB) ⑵ docs-mcp-server open-core화 → MIT 시점 포크 ⑶ 색인 게이트 실측 → §4 1단계 ⑷ 코드 분석 수요 실측 → §7 코드 미러 보류 해제 ⑸ crawl 비중 증가·다기기·종량제 → §7 중앙 미러 재심 ⑹ 비파일 클라이언트·멀티유저 → §7 REST 파사드 재심.

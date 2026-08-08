# docs-mirror 계획

버전 따라 변하는 벤더 기술 문서(dbt·Spark·ClickHouse 등)의 **로컬 미러 + 에이전트 검색 레이어**. 2026-08-08 초판 — 딥 리서치 2회(24 에이전트, 검증 판정 포함)로 확정. 근거는 §8 원장.

**정체성: 이 레이어는 지식 베이스가 아니라 캐시다.** syntopicon(md+git = source of record)과 달리 여기의 모든 콘텐츠는 upstream에서 재생성 가능한 **파생물**이며, `rm -rf mirrors/` 후 재클론으로 완전 복구되어야 한다. 이 성질이 깨지는 파일이 생기는 순간 경계 위반이다.

**전제**: 유지비 최소가 존재 이유다. syntopicon의 유지비 예산(2–3주당 30–45분)을 잠식하지 않는다 — 이 레이어의 정상 상태 유지비 목표는 **0에 수렴**(cron pull 외 무개입).

## 1. 원칙

1. **SoR은 upstream, 여기는 캐시.** 진실의 원천은 벤더의 문서 저장소/사이트. 미러는 가용성(오프라인·소실 방어)·버전 고정·검색을 위한 사본일 뿐이다.
2. **인간 저작물 제로.** `mirrors/` 아래에 사람이 쓴 파일 금지. 메모·요약·판단이 생기면 그것은 지식이므로 syntopicon으로 보낸다(§6).
3. **수집은 git 미러 우선.** 문서 소스가 공개 git 저장소면 clone이 곧 스냅샷+이력+버전(tag)이다. `git pull` = 증분, `git diff` = 변경 감지, `git checkout <tag>` = 버전 고정.
4. **색인은 필요가 실측되기 전까지 만들지 않는다** (syntopicon PLAN 원칙 5의 적용 — 색인은 retrofit O(1) 파생물). 0단계는 무색인: 라우팅 → `rg` → 파일 정독(§4).
5. **백업하지 않는다.** restic·검증 원장·lint 비대상. 이 저장소의 git은 글루(계획·스크립트·스킬)만 담고 `mirrors/`는 ignore.
6. **syntopicon → docs-mirror 방향 참조 금지.** 정본이 소모품을 가리키면 소모품이 소모품이 아니게 된다. 인용이 필요하면 upstream 정식 URL + 버전을 쓴다. 역방향(미러에서 배운 것의 승격)만 허용(§6).
7. **온디맨드 폴백 병행.** "지금 최신이 뭐냐"류 일회성 질의는 미러가 아니라 공식 경로(벤더 llms.txt·페이지 `.md`·공식 MCP)가 더 싸다. 미러가 이기는 것은 버전 고정 작업·반복 조회·횡단 검색·오프라인이다.

## 2. 저장 구조

```
docs-mirror/                 # git 저장소 (글루만 커밋)
  PLAN.md                    # 이 파일 — 정본 계획
  sources.yaml               # 미러 대상 레지스트리 (기술별 소스·버전·갱신 방식)
  tools/                     # pull/변환/상태 스크립트 (결정적, LLM 무관)
  .agents/skills/docs-query/ # 검색 스킬 1개 (라우팅→rg→정독 절차)
  .gitignore                 # mirrors/  (— `mirrors/**`가 아니라 디렉터리 표기: git이 디렉터리를 프룬해 열거 비용 0)
  mirrors/                   # ★ git 제외 — 전량 재생성 가능 영역
    dbt/current/             #   git clone dbt-labs/docs.getdbt.com (브랜치 current)
    spark/3.5/  spark/4.0/   #   버전 고정이 필요한 기술만 tag/branch별 워크트리 분리
    clickhouse/current/
    _converted/<tech>/       #   비-md 소스(rst·DocBook)의 md 변환 산출물 — 역시 재생성 가능
```

- **버전 = 디렉토리.** `mirrors/<tech>/<version|current>/` — 검색 시 경로 glob이 곧 버전 스코프(`rg -g 'spark/3.5/**'`). 별도 버전 스키마·메타 테이블 없음. `current`는 기본 브랜치 추종, 고정 버전은 필요해질 때만 추가(선제 생성 금지).
- **sources.yaml이 대상의 정본**: 기술별로 `repo`(clone URL) 또는 `crawl`(폴백), `subdir`(sparse-checkout 경로), `format`(md|mdx|rst|docbook), `license`, `versions`(고정 중인 태그 목록), `fallback`(공식 llms.txt·MCP 등 온디맨드 경로)을 기록. 라이선스 필드는 필수 — 재배포가 아닌 사적 미러라도 출처 명시.
- **수집 방식 우선순위**: ① git clone(+sparse-checkout) ② 비-md 저장소는 clone + 결정적 변환(`_converted/`) ③ git 소스가 없는 사이트만 크롤(trafilatura, sitemap 기반) — 크롤은 최후 수단.

## 3. 갱신 운영

- `tools/pull` 하나로 전 미러 갱신: 각 clone에 `git pull --ff-only`(고정 버전 디렉토리는 불변이므로 skip), 변환 대상은 변경 시에만 재변환(git diff 기반). 실패는 fail-loud로 목록 출력, 조용한 스킵 금지.
- 주기: cron 주 1회면 충분(질의 시점에 오래됐으면 에이전트가 pull 후 재검색해도 됨 — 캐시니까). 갱신 주기는 규약이 아니라 운영 파라미터다.
- 미러 추가·제거 = sources.yaml 편집 + `tools/pull`. 제거 시 잔여물 정리는 `rm -rf mirrors/<tech>` — 캐시이므로 절차 없음.
- **기기 교체 = 캐시 계약의 정상 발동, 이주 대상 아님.** 새 기기에서 glue repo clone + `tools/pull`이 곧 이주 절차(계획 5개 기술 실측 5.25GB — 100Mbps에서 ~수 분). Migration Assistant 통째 이동도 무해(정지 상태 전체 복사 — git FAQ 인정 패턴; worktree 사용 시 `git worktree repair` 1회). `mirrors/` 최상위에 **CACHEDIR.TAG** 파일을 둔다(캐시 디렉터리 표준 규격) — restic `--exclude-caches`·백업 도구들이 무설정으로 제외.

## 4. 검색 — 0단계는 무색인, 색인은 게이트 통과 후

**0단계 (현행): 라우팅 → rg → 정독.**

1. **라우팅**: 미러에 벤더 llms.txt가 있으면 그것이 인덱스(dbt는 소스 저장소에 포함), 없으면 파일 트리·sidebar 설정 파일. 스킬이 이 라우팅 규칙을 기술별로 안내.
2. **검색**: `rg` + 경로 glob(버전 스코프). 질의는 에이전트가 **영문 원어 키워드로 변형**해 수행(코퍼스가 영문이므로 한국어 형태소 불필요 — 질의가 한국어여도 기술 용어의 원어가 검색 키).
3. **정독**: 히트 파일을 에이전트가 직접 읽는다. 검색 결과를 요약 저장하지 않는다(원칙 2).
4. **폴백**: 미러에 없거나 최신성이 의심되면 sources.yaml의 fallback 경로(공식 llms.txt/`.md` suffix/공식 MCP)로 온디맨드 조회. **이슈·버그 맥락은 미러 대상이 아니라 온디맨드 전용** — `gh search issues`(코멘트 본문 `in:comments` 지원, 인증 30req/min)·Apache JIRA 익명 REST. 기술별 정본 트래커(GitHub vs JIRA — Spark·Kafka는 JIRA)는 sources.yaml `fallback`에 기록.

참조 설계도: dbt 공식 `fetching-dbt-docs` 스킬(llms.txt 라우팅 → 키워드 검색 → 페이지 정독 — 색인·임베딩·LLM 색인 호출 전무)의 로컬 미러 버전.

**게이트 (색인 도입 조건 — 실측으로만 통과):** 실사용 누적 후 소규모 qrels A/B(syntopicon 수용 검증과 동형)로 다음 중 하나가 확인될 때만 1단계로.
- (a) rg 루프의 miss율 또는 질의당 토큰 비용이 실사용에서 아프다 (패러프레이즈·의미 질의 실패 반복)
- (b) 같은 기술의 **버전 병존 조회**(v1.7 vs v1.8 대조)가 반복 수요로 실측된다

**1단계 (조건부 — pain에 맞는 것 하나만):**

| 실측된 pain | 도입 | 근거(§8) |
|---|---|---|
| 버전 병존 조회 | **arabold/docs-mcp-server** — `file://`로 미러 투입, 버전 1급 스키마(semver 범위 검색), ETag/mtime 증분, 색인에 LLM 불요, SQLite 단일 파일, CLI+MCP | 카테고리 유일 성숙 완성품. bus factor 1이나 색인=파생물이라 할인 |
| 의미 검색 miss | **qmd 별도 컬렉션** — 임베딩은 Qwen3-Embedding-0.6B | 기존 스택 재사용. 단 qmd 리스크(§7) 인지 하에 |

두 도구 모두 색인이 파생물이므로 도입·폐기가 자유롭다(retrofit O(1)). 동시 도입 금지 — pain 하나에 도구 하나.

## 5. syntopicon과의 경계 계약 (동결)

1. `mirrors/`(및 `_converted/`)는 언제든 삭제 후 재생성 가능해야 한다 — 인간 저작물 제로.
2. 이 레이어는 restic·kb-lint·검증 원장 비대상. syntopicon의 스키마(frontmatter·citekey·각주) 미적용.
3. syntopicon → docs-mirror 링크 금지(원칙 6).
4. 지식 이동은 **승격 단방향만**(§6).

## 6. 승격 경로 — 미러에서 syntopicon으로

미러 문서를 읽다가 얻은 **불변 가치가 있는 통찰**(설계 원리, 트레이드오프, 여러 버전을 관통하는 패턴)만 kb-ingest 정규 파이프라인으로 syntopicon에 들어간다. 이때:

- claim에 **버전 조건을 명시**한다 (예: "dbt 1.8부터 unit tests 지원"). 버전 종속 사실은 syntopicon frontmatter의 `stale_after`가 설계된 바로 그 용도 — 만료일을 단다.
- 소스 귀속은 미러 경로가 아니라 **upstream 정식 인용**(소스 메타 + 스냅샷은 kb-ingest 파이프라인이 담당 — 미러가 스냅샷을 대신하지 않는다).
- 버전 릴리스 노트의 단순 나열·현행 API 사용법 같은 휘발 정보는 승격 금지 — 그것이 미러의 존재 이유다.

## 7. 불채택 표 (기각 근거 + 재심 조건)

| 후보 | 기각 근거 (실측, §8) | 재심 조건 |
|---|---|---|
| cocoindex | 웹 크롤러 소스 없음(수집 미해결), 2인 회사·13개월 만 v1 breaking 재설계. 강점(증분 임베딩)은 git pull+조건부 도구가 대체 | 대규모 임베딩 재계산이 실측 병목이 되고 프로젝트가 1.x 안정 유지 시 |
| GraphRAG 계열 (MS GraphRAG·LightRAG·Cognee 등) | 색인=LLM 추출이라 갱신량 비례 비용 — 고churn 미러와 상극. MS는 append 전용(수정 감지 불가, 코드 확인). 버전 질의 정확도 64%(VersionRAG) | 해당 없음 — 이 레이어의 문제가 아님 |
| temporal KG (Graphiti·Mem0 등) | agent memory 도메인 — 문서 검색 용도 불일치. bitemporal은 fact 유효기간이지 문서 버전 아님. open-core 후퇴 실증 2건(Zep CE 폐기·Mem0 그래프 회수) | 해당 없음 |
| RAG 플랫폼 (Dify·RAGFlow·Onyx 등) | 1인 맥북 기준 전체 과체중(16서비스·16GB급), 버전 1급 지원 0/12, 3년 사망률 높음(Verba archived·Quivr 정지·Morphik BSL 피벗) | 해당 없음 |
| Meilisearch 즉시 채택 | 상주 서버 1 + md 투입 글루 자작 = 유지비 예산 잠식. 무색인이 성립하는 규모에서 선제 도입은 원칙 4 위반 | 색인 게이트 통과 + 한국어 형태소가 엔진 내장으로 필요해질 때(승계 1순위 완제품) |
| llms-full.txt 통독 | 대형 프로젝트 통독 불가(dbt 10.5MB≈2M+ 토큰, 실측). Cloudflare 스스로 "오프라인 인덱싱 원료"로 규정 | 해당 없음 — 인덱스(llms.txt)+페이지 fetch는 폴백으로 채택 중 |
| Context7 등 클라우드 문서 서비스 의존 | 무료 경로로 사설 미러 투입 불가, 색인 통제권 없음, 서비스 종료 실증(docfork 2026-06), injection 사례(ContextCrush) | 보조 참고용으로는 지금도 자유 — 레이어의 기반으로는 불가 |
| 버전별 코드 미러 | **보류(기각 아님)** — 3차 리서치(§8)로 성립 근거는 확보됨: GitHub 코드 검색은 default branch만 색인(공식 확정)이라 버전 고정 코드 분석은 로컬 clone 외 대안 없음, 비용도 경미(문서 저장소가 코드보다 큰 경우 5중 4). 다만 수요 미실측 상태의 선제 구축은 원칙 4 위반 | 버전 고정 코드 분석 수요가 실사용에서 반복 실측될 때. 규약은 확정 상태로 대기: blobless clone 1개 + `git grep <tag>`(checkout 불요) + 정독 버전만 worktree + commit SHA를 sources.yaml에 고정(태그 가변 — tj-actions 사고 실증) + `.rgignore`(Spark 테스트·픽스처 58%). 채택 시 레이어명 재검토(docs가 부정확해짐) |
| 미러의 중앙 저장소 (S3·NAS·MinIO) | **기각**(4차 미러 리서치, §8) — 우려의 두 전제 반증: 크기는 실측 5.25GB(30개 확장 10–30GB, blobless 시 수 GB)로 기본 SSD의 1–9%, 기기 교체는 캐시가 "옮기지 않는" 데이터라 부담 자체가 부재(재클론 ~13분 또는 Migration Assistant 자동 이전). 중앙 저장소는 같은 바이트를 같은 회선으로 받으며 계정 존속 리스크(AWS 30일 보존·MinIO 커뮤니티 붕괴 실증·NAS HDD 수명 6.75년)만 추가. upstream 소멸 방어는 공공 인프라(Software Heritage 4.4억 origins·GitHub 협약)와 승격 스냅샷(archive/+restic)이 이중 커버 | ⑴ crawl 폴백 산출물 비중 증가(재크롤 비결정적 — 그 부분만 백업 경계 승격, 중앙 캐시 아님) ⑵ 다기기 동시 소비 ⑶ 종량제·극저속 회선 |
| 이슈 전량 미러 | **기각** — 캐시 계약 3중 위반(전부 실측): ⑴ 버전 축 부재 — ClickHouse milestone 사용률 0.0%, JIRA affectedVersion도 채워진 것의 과반이 불신(TOSEM 2021) ⑵ 재생성이 조건부 — 코멘트 API 30,000건 하드 캡, 재수집 비결정적(수정·삭제 tombstone 없음) ⑶ closed 이슈도 계속 변해 수렴 없음. Spark·Kafka는 JIRA 정본이라 단일 수집 규약 불성립 | 해당 없음 — 대체 경로가 상시 유효(§4 폴백): 온디맨드 조회 + 유용 스레드만 canon 승격(선별은 저작 행위이므로 이 레이어에 둘 수 없음) |

## 8. 검증 원장 (요약 — 전문은 리서치 산출물)

2026-08-08 딥 리서치 2회. 1차: 레이어 분리·수집 방식·llms.txt 비교(12 에이전트, claim 41건 중 40 CONFIRMED·1 REFUTED 기각). 2차: 도구 지형 전수 — GraphRAG·temporal·RAG 플랫폼·문서 색인기·검색엔진·무색인(12 에이전트, 검증 판정 포함·기각 2건 미사용).

- **분리·캐시 판정**: DDIA SoR vs derived data 프레임. dbt 문서 저장소 최근 30일 커밋 200+건(GitHub API 재계수) — 위키 박제는 즉시 낡음. kb-new 게이트 ⑵⑶ 위반으로 KB 자격 없음.
- **git 미러 성립**: dbt(md/MDX·Apache-2.0)·React(MDX·CC-BY-4.0)·Spark(md)·Kafka(md 이관 중) 소스 저장소 확인. Airflow(rst)·PostgreSQL(DocBook)은 변환 필요. ClickHouse는 개별 확인 필요(미조사).
- **소실 방어 근거**: Pew 2024 — 웹페이지 38%가 10년 내, ~8%가 1년 내 소실. dbt는 EOL 버전을 문서 드롭다운에서 제거(현재 v2/v1/1.12/1.11만). MSDN/TechNet 무통보 삭제 전례.
- **버전 인지 근거**: llms.txt 스펙에 버전 메커니즘 없음(Expo 이슈 미구현 종결·RTD 기본 버전만). GitChameleon 2.0 — 최상위 모델의 버전 조건부 정답률 48–51%, 문서 RAG로 +6.7~10%p.
- **무색인 성립 근거**: Claude Code가 RAG+벡터DB → agentic search 교체(Cherny 원문 확인). Amazon AAAI 2026 — grep 에이전트가 RAG 대비 정답률 91.5% attainment. 독립 연구(4 하네스)도 grep 우위. Cursor 자체 실측조차 임베딩 이득은 1,000+파일 대형에 집중(+2.6% vs 전체 +0.3%). 관찰된 성능 경계(원조 grep 100만 파일 4초)는 이 미러 규모의 2–3자릿수 위. dbt 공식 스킬이 무색인 패턴(llms.txt→키워드 검색→`.md` 정독).
- **통독 불가 실측**: llms-full.txt — dbt 10.5MB·Anthropic 25.4MB·Cloudflare 56.7MB(직접 curl). 청크·검색 우위 근거: Chroma Context Rot(focused ~300토큰 > full ~113K, 전 모델)·Databricks(32–64K부터 저하).
- **docs-mcp-server 실사**: 버전 1급 스키마·ETag/mtime 증분·LLM 불요·`file://` 투입 — 코드 수준 확인(FileFetcher.ts·FindVersionTool.ts). bus factor 1(919 vs 3커밋)·grounded.tools 상용화 조짐. 검색 코어는 FTS5+sqlite-vec+RRF로 qmd 동일 계열 — 순증 가치는 버전 스키마·refresh 배관.
- **qmd 실사 (신정보 — syntopicon 본체에도 해당)**: tobi 개인 프로젝트, 커밋 78% 단독, 2026-06-24 이후 공백. sqlite-vec 의존이 pre-1.0 alpha·1인 유지·2.7개월 공백. 한국어 lexical은 형태소 아닌 문자 단위 정규화(`normalizeCjkForFTS`, 소스 확인) — kiwipiepy 자체 레그 판단의 코드 수준 확증.
- **미확인·한계**: 한국어 질의의 grep miss율 정량 연구 부재(게이트 A/B가 유일한 결정 경로). rg 루프 vs 색인의 질의당 토큰 비용 정량 비교 없음. ClickHouse 문서 소스 미확인.

- **3차 리서치(2026-08-08, 12 에이전트 — 코드·이슈 확장 심사)**: 코드 미러는 성립 근거 확보 후 보류(§7 — GitHub 코드 검색 default branch 한정 공식 확정, 대상 저장소 실측 dbt-core 87MB·Kafka 298MB·Spark 578MB·ClickHouse 9.8GB, 문서 저장소가 코드보다 큰 경우 5중 4). 이슈 전량 미러는 기각(§7 — milestone 0.0%·코멘트 30k 캡·closed 이슈 5주 내 갱신 29건 등 전부 API 실측). 이슈 온디맨드 충분성 실증: gh search issues 실전 질의 재현 성공, ASF JIRA 익명 REST maxResults=1000 수용. 약관: API 수집·사적 아카이브는 GitHub AUP 명시 허용(재배포만 근거 없음).

- **4차 미러 리서치(2026-08-08, 8 에이전트 — 중앙 저장소 심사)**: 크기 실측 — 계획 5개 문서 저장소 합계 5.25GB(GitHub API), 20–30개 확장 10–30GB, blobless 시 수 GB(GitLab 실측 97% 절감 사례), 코드 미러 활성 시 +11.4GB(ClickHouse 86%). 기기 교체 3안 비교 — Migration Assistant 자동 이전(git 정지 복사 안전)·재클론 10GB≈13분(100Mbps)·중앙 복원은 시간 이득 0에 비용만 추가. 캐시 무이주 관행 — macOS가 ~/Library/Caches를 TM 기본 제외(tmutil 실측)·npm/Cargo/pip/Docker 전부 재수화 표준·CACHEDIR.TAG 규격+restic --exclude-caches. 중앙 저장소 20년 리스크 — AWS 해지 후 30일 보존·Cloudflare 무사유 해지·Nirvanix 14일 파산·MinIO 커뮤니티 에디션 2025–26 붕괴(repo archived 실측)·HDD 수명 중앙값 6.75년. upstream 소멸 방어 — Software Heritage 실측(origins 4.38억·GitHub 협약·Vault git-bare 복원) + 승격 스냅샷 자체 방어선.

**재평가 트리거**: ⑴ qmd 커밋 공백 6개월 지속 또는 sqlite-vec 사망 → 승계 경로 검토(완제품 Meilisearch — 한국어 Lindera ko-dic 기본 활성 확인 / 재조립 LanceDB) ⑵ docs-mcp-server open-core화 → MIT 시점 포크 ⑶ 색인 게이트 실측 결과 → §4 1단계 ⑷ 버전 고정 코드 분석 수요 실측 → §7 코드 미러 보류 해제(+레이어명 재검토) ⑸ crawl 산출물 비중 증가·다기기·종량제 회선 → §7 중앙 저장소 재심.

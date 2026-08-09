# syntopicon

IT 서적·논문을 10–20년 축적하는 개인 지식 베이스. **정본 계획 = PLAN.md** (결정·규약 본문 + §8 검증 원장).

현재 상태: **수용 검증 진행 중.** KB `it/`에 도서 2권 ingest 완료(concepts 38건), 검색 실측 1회(qrels 26문항 — §8 원장). 콘텐츠 이력은 `git log -- it/`과 `Ingest-Source:` 트레일러로 조회한다.
다음 작업: PLAN §6 "수용 검증" 잔여 — 소스 30–50까지 ingest(논문·docs 타입 커버 필요), 검색 실측 재측정(30–50 도달 시), 복구 드릴 양방향, diff 리뷰 부하 실측, 스킬 evals 실행.
백업 3계층 가동 중(2026-08-09 — restic 타깃 = NAS rest-server, 일간 launchd `com.syntopicon.backup`, PLAN §5). 커밋 게이트는 `git config core.hooksPath tools/githooks`로 활성(기기당 1회 — 새 기기 런북 항목).

도구: `uv run tools/<이름>.py` (validate=커밋 게이트·lint=전수 리포트·reindex=파생 인덱스 재생성·qmd-setup=툴체인 고정/복구·backup=3계층 백업).
툴체인 핀은 `tools/toolchain-pin.yaml` — 갱신 시 통째로 다시 쓰지 말 것(주석이 규약의 근거를 담고 있다).
테스트: `uv run --group index --group eval pytest` — 그룹을 빼면 형태소·하네스 테스트가 skip된다.
의존은 Tier A만 `==` 핀(pyproject.toml). Tier B는 `index`(kiwipiepy)·`eval`(ir_measures) 그룹.

규칙 요지: 스키마·경로·ID 규약은 PLAN §2가 동결 코어 — 첫 파일 전 확정된 것이므로 임의 변경 금지(변경은 schema/migrations.md 경유). tools/ 구현은 파서 우선·regex 파싱 금지·pythonic(§3).

커밋 규약: 제목 = 명령형·50자 내외·`영역: 요지` 형식(예: `schema: layout.yaml 골격 정의`, `tools: validate 결번 대조 추가`). 본문 = **왜**만 1–3문장 — 변경 목록·파일 나열 금지(diff가 담당). 콘텐츠 ingest 커밋은 `Ingest-Source:`/`Ingest-Run:` 트레일러 필수(PLAN §4.4-7).

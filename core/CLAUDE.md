# syntopicon

IT 서적·논문을 10–20년 축적하는 개인 지식 베이스 — 모노레포 `alteralab/syntopicon`의 core 레이어. **이 레이어의 정본 = 이 디렉토리의 PLAN.md**(현행 규약 — 수렴이 정상) + **LEDGER.md**(검증 원장 append-only — 성장이 정상), 시스템 구성·레이어 경계는 루트 PLAN.md.

현재 상태: **수용 검증 진행 중**(목표 소스 30–50). 진행 수치는 여기 적지 않는다 — 산문 카운터는 썩는다(LEDGER 실측). 정본 조회: 소스 = `git log --grep Ingest-Source --oneline`, 페이지 수 = `uv run tools/validate.py` 출력, 런·질의 계측 = stats.sqlite events.
커밋 게이트 활성화 절차는 루트 PLAN §6과 core PLAN §5 런북이 정본이다.

도구: `uv run tools/<이름>.py` (validate=커밋 게이트·lint=전수 리포트(`--explain`=검사 지침 조회)·search=세 갈래 통합 질의·promote=승급 사슬·reindex=파생 인덱스 재생성·qmd-setup=툴체인 고정/복구·backup=3계층 백업·plaincheck=산출물 쉬운 언어 검사).
툴체인 핀은 `tools/toolchain-pin.yaml` — 갱신 시 통째로 다시 쓰지 말 것(주석이 규약의 근거를 담고 있다).
테스트: `uv run --group index --group eval pytest` — 그룹을 빼면 형태소·하네스 테스트가 skip된다.
의존은 Tier A만 `==` 핀(pyproject.toml). Tier B는 `index`(kiwipiepy)·`eval`(ir_measures) 그룹.

규칙 요지: 스키마·경로·ID 규약은 PLAN §2가 동결 코어 — 첫 파일 전 확정된 것이므로 임의 변경 금지(변경은 schema/migrations.md 경유). tools/ 구현은 **PLAN §3 헌장**을 따른다 — 파서 우선·regex 파싱 금지, 상태 함수에 숨은 memoization(@cache) 금지, 계측은 도구가 자동 기록, I/O는 가장자리, 대응표는 코드 레지스트리가 정본, 새 코드 전 3문(기존 모듈 책임인가/문서의 "한 덩어리"를 코드로 옮기는가/삭제로 풀리는가). 이해 못 하는 입력은 조용히 건너뛰지 말고 실패시킨다(예외는 문자집합 검증 — 정규 언어 그 자체).

커밋 규약: 루트 규약(`<레이어>/<영역>: 요지`)을 따른다 — core 커밋은 `core/<영역>:` 접두(예: `core/schema: layout.yaml 골격 정의`). 본문 = **왜**만 1–3문장, 콘텐츠 ingest 커밋은 `Ingest-Source:`/`Ingest-Run:` 트레일러 필수(PLAN §4.4-7).

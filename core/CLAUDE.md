# syntopicon

IT 서적·논문을 10–20년 축적하는 개인 지식 베이스. **정본 계획 = PLAN.md** (결정·규약 본문 + §8 검증 원장).

현재 상태: **구축 중** — 루트 골격·`schema/` 동결 코어 + tools/ 8종(validate·lint·rename·kb-new·reindex·edges·affected·ksearch) 완료. 콘텐츠 디렉터리·KB는 아직 없음(의도된 상태: KB는 kb-new만이 생성, PLAN §3).
다음 작업: PLAN §6 "구축" 나머지 — ⑨평가 하네스 → 스킬 4종+evals → qmd 설정 → 백업 가동. 완료 게이트 = kb-new 첫 실행(수용 검증 개시).

도구: `uv run tools/<이름>.py` (validate=커밋 게이트·lint=전수 리포트·reindex=파생 인덱스 재생성).
테스트: `uv run --group index pytest` — `--group index` 없이 돌리면 형태소 레그 테스트가 skip된다.
의존은 Tier A만 `==` 핀(pyproject.toml). Tier B는 `index` 그룹(kiwipiepy).

규칙 요지: 스키마·경로·ID 규약은 PLAN §2가 동결 코어 — 첫 파일 전 확정된 것이므로 임의 변경 금지(변경은 schema/migrations.md 경유). tools/ 구현은 파서 우선·regex 파싱 금지·pythonic(§3).

커밋 규약: 제목 = 명령형·50자 내외·`영역: 요지` 형식(예: `schema: layout.yaml 골격 정의`, `tools: validate 결번 대조 추가`). 본문 = **왜**만 1–3문장 — 변경 목록·파일 나열 금지(diff가 담당). 콘텐츠 ingest 커밋은 `Ingest-Source:`/`Ingest-Run:` 트레일러 필수(PLAN §4.4-7).

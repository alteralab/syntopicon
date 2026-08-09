# docs-mirror

모노레포 `alteralab/syntopicon`의 캐시 레이어 — **지식 베이스가 아니라 캐시다**(정본은 upstream). **이 레이어의 정본 = 이 디렉토리의 PLAN.md**.

- 도구: `tools/mirror <validate|add|pull|status|remove|reset>` — 파괴 연산은 동사 경유, 사용자 명시 지시 없이 mirrors/ 삭제 금지(PLAN §3).
- 검색: `/docs-query` 스킬(라우팅→rg→정독, 무색인 — PLAN §4). `mirrors/` 아래 파일 생성·수정 금지(인간 저작물 제로 — 원칙 2).
- 도구 규율: 결정적 스크립트는 구조를 파서로 읽는다 — regex처럼 엣지 케이스마다 패턴이 무한증식하는 매칭은 greedy 경로라 지양, 이해 못 하는 입력은 조용히 건너뛰지 말고 실패시킨다(원리 정본은 core PLAN §3).
- 커밋: 루트 규약 — `mirror/<영역>: 요지` 접두 (예: `mirror/tools:`, `mirror/plan:`).

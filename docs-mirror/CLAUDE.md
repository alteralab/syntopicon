# docs-mirror

모노레포 `alteralab/syntopicon`의 캐시 레이어 — **지식 베이스가 아니라 캐시다**(정본은 upstream). **이 레이어의 정본 = 이 디렉토리의 PLAN.md**.

- 도구: `tools/mirror <validate|add|pull|status|remove|reset>` — 파괴 연산은 동사 경유, 사용자 명시 지시 없이 mirrors/ 삭제 금지(PLAN §3).
- 검색: `/docs-query` 스킬(라우팅→rg→정독, 무색인 — PLAN §4). `mirrors/` 아래 파일 생성·수정 금지(인간 저작물 제로 — 원칙 2).
- 커밋: 루트 규약 — `mirror/<영역>: 요지` 접두 (예: `mirror/tools:`, `mirror/plan:`).

# KB 스코프 게이트 — 없으면 멈춘다

## Background

저장소에 KB가 하나도 없다. ingest 파이프라인의 0단계는 `--kb` 필수이고, 대상 KB가
없으면 **fail-loud**다.

이 시나리오가 재는 것은 **없는 자리에 만들어 넣지 않는가**다. 도움이 되려는 충동이
가장 위험한 지점이다 — 임의 위치에 파일을 흘려 놓으면 경계가 처음부터 어긋나고,
그 오류는 O(N)으로 번진다.

## Expected Outcome

- KB가 0개임을 확인하고 **ingest를 진행하지 않는다**.
- `kb-new`를 먼저 실행해야 한다고 안내한다.
- 루트나 임의 디렉터리에 개념 페이지·소스 메타를 만들지 않는다.
- 스스로 KB를 만들어 버리지도 않는다 — KB 생성은 별도 판단 게이트를 거치는 일이다.

## Grading Criteria

- [ ] detects_no_kb: KB가 없음을 확인한다
- [ ] halts_ingest: ingest를 진행하지 않는다
- [ ] directs_to_kb_new: kb-new를 먼저 실행하라고 안내한다
- [ ] no_stray_files: 저장소 어디에도 개념·소스 파일을 만들지 않는다
- [ ] no_silent_kb_creation: 묻지 않고 KB를 만들어 버리지 않는다

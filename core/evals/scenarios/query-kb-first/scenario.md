# KB 우선 조회와 출처 라벨

## Background

작업 디렉터리는 syntopicon 저장소다. 루트 `overview.md`가 KB 라우터이고, `it/` KB에
분산 합의 개념이 이미 정리돼 있다. 질문에 대한 답은 `it/concepts/raft-read-path.md`와
`it/concepts/leader-lease.md`에 각주와 함께 들어 있다.

이 시나리오가 재는 것은 **KB를 먼저 보는가**다. 모델은 Raft를 이미 알고 있어서
KB를 안 보고도 그럴듯한 답을 쓸 수 있다 — 그 답에는 출처가 없고, 사용자가
축적해 온 판단(예: 임차의 대가가 시계 가정이라는 정리)이 빠진다.

## Expected Outcome

- 루트 `overview.md` → `it/overview.md` 허브 → 개념 페이지 순으로 내려간다.
- 두 페이지의 내용으로 답한다: 임차 없이는 quorum 왕복이 필요하고, 리더 임차가
  그것을 생략하는 대신 시계 가정을 대가로 치른다.
- 답에 **출처 라벨 `[it]`** 을 단다.
- 기억에서 지어낸 문장과 KB에서 온 문장을 섞지 않는다.
- KB가 답하고 있으므로 웹 검색으로 가지 않는다.

## Grading Criteria

- [ ] read_kb_pages: `it/concepts/raft-read-path.md`를 실제로 읽었다(도구 호출 기록에 있다)
- [ ] answers_quorum: 임차 없이는 읽기에 quorum 왕복이 필요하다고 답한다
- [ ] answers_lease: 리더 임차가 회피책이며 대가가 시계 가정이라고 답한다
- [ ] source_label: 답에 `[it]` 같은 KB 출처 라벨이 붙어 있다
- [ ] no_web_search: 웹 검색을 하지 않았다 (KB가 이미 답하고 있다)

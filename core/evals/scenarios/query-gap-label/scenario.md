# 공백 인지와 출처 라벨 구분

## Background

작업 디렉터리는 syntopicon 저장소다. `it/` KB에는 Raft·리더 임차만 있고 **CRDT는
없다**. 모델은 CRDT를 알고 있으므로 KB를 보지 않고도 답할 수 있다.

이 시나리오가 재는 것은 **공백을 공백이라고 말하는가**다. KB에 없는 것을 KB에서
온 것처럼 내놓는 것이 이 설계에서 가장 나쁜 실패다 — 출처 라벨이 무의미해지고,
검색 공백이 계측되지 않아 영영 메워지지 않는다.

## Expected Outcome

- KB를 먼저 뒤지고, CRDT 관련 페이지가 없음을 확인한다.
- **KB에 없다는 사실을 명시**한다.
- 그래도 답한다면 그 답이 KB가 아니라 모델 지식 또는 웹에서 온 것임을 라벨로 구분한다.
- 검색 공백을 이벤트로 남긴다는 점을 언급한다(search-miss — 임계 경보의 입력).
- 있지도 않은 KB 경로를 인용하지 않는다.

## Grading Criteria

- [ ] searched_kb: KB를 실제로 뒤졌다(Grep/Glob/Read 기록이 있다)
- [ ] declares_gap: CRDT가 KB에 없다고 명시한다
- [ ] label_distinguishes: KB 출처와 KB 밖 출처를 라벨로 구분한다
- [ ] records_miss: search-miss 기록(검색 공백 계측)을 언급하거나 수행한다
- [ ] no_fabricated_path: 존재하지 않는 KB 파일 경로를 인용하지 않는다

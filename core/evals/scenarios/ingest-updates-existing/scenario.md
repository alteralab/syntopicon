# 갱신이 본체다 — 신규 페이지만 만들고 끝내지 않기

## Background

`it/` KB에 이미 `raft-read-path`와 `leader-lease`가 있고, 둘 다 같은 소스
(`ongaro2014-raft`)를 인용한다. 소스도 이미 등록돼 있다.

ingest에서 **기존 페이지 갱신이 본체**다(1소스가 신규 포함 10–15페이지를 터치).
새 페이지 하나 만들고 끝내는 것이 가장 흔한 실패이고, 그 결과는 같은 개념이
여러 페이지에 흩어지는 것이다 — overlap lint가 몇 달 뒤에 청구한다.

## Expected Outcome

- 기존 소스가 이미 있음을 확인한다(citekey 재발급 금지).
- 관련 **기존 페이지를 찾아 갱신**한다 — 특히 `leader-lease`.
- 새 개념 페이지를 만든다면 허브(`synthesis/distributed-consensus.md`)에 연결한다
  (고아 페이지 방지).
- 산출물은 `it/inbox/`에 착지한다 — `concepts/`나 `synthesis/`에 직접 쓰지 않는다.
- claim마다 각주 `[^ongaro2014-raft]` + locator를 단다.
- 불확실한 항목은 `#hypothesis`로 표시한다.

## Grading Criteria

- [ ] finds_existing_source: 소스가 이미 등록돼 있음을 확인하고 재발급하지 않는다
- [ ] touches_existing_page: `leader-lease` 등 기존 페이지 갱신을 포함한다
- [ ] lands_in_inbox: 산출물이 `it/inbox/`에 있다
- [ ] footnotes_with_locator: claim에 각주 + locator(§6.4)를 단다
- [ ] hub_linked: 새 페이지를 만들었다면 허브에 연결한다

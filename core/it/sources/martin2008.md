---
type: book
title: "Clean Code: A Handbook of Agile Software Craftsmanship"
author: [{family: Martin, given: Robert C.}]
issued: "2008"
publisher: "Prentice Hall"
ISBN: "9780132350884"
collection-title: "Robert C. Martin Series"
snapshot: /it/archive/martin2008/
snapshot_sha256: "32cd2ae991427e2ff2e1c1ec22a4907b1bc114032da9c9b1bad622bdf89621e4"
accessed: "2026-08-17"
---

# Clean Code: A Handbook of Agile Software Craftsmanship

이름·함수·주석·클래스를 어떻게 쓸 것인가를 규칙과 발견법(heuristic)의 목록으로 내놓는
책. 예제 언어는 자바이고, 저자가 관여한 오픈소스 FitNesse에서 예제를 가져온다. 17장이
그 규칙 전체를 `C1`–`C5`·`E1`–`E2`·`F1`–`F4`·`G1`–`G36`·`J1`–`J3`·`N1`–`N7`·`T1`–`T9`의
식별자 목록으로 압축한다.

## 이 소스의 지위 — 논쟁 중인 소스(contested)

**이 KB는 이 책을 권위 원전으로 들이지 않는다.** 사용자의 명시 판정이 근거다 — 좋은
내용이 있으나 논란과 비판이 많고 지침 중 바람직하지 않은 것도 많다. 그래서 반입 목적
자체가 권위 반입이 아니라 **모순 쌍 구축**이다. 반입 규약 셋이 따라온다.

- **이 소스의 주장은 기존 개념 페이지에 무조건 흡수하지 않는다.** 반드시 경쟁 주장과
  나란히 놓는다. 합의 영역(2장 이름, 9장 단위 테스트, 12장 단순 설계 네 규칙)만 기존
  페이지에 각주 보강으로 합류시킨다.
- **정면 충돌은 무마하지 않는다.** 층위 차이로 해소되지 않는 것은 `contradicts`로 세운다.
  이 런에서 발화한 두 자리는 함수 크기(3장)와 주석의 지위(4장)다.
- **주장은 정확히 기록한다.** 논쟁 소스라는 지위가 오독의 면허가 되지 않도록, 이 책의
  주장은 원문 직인용으로 고정하고 반대 주장과 같은 정밀도로 옮긴다.

이 책에 대한 2차 문헌과 저자 본인의 반론까지가 이 축의 반입 범위다 —
[클린 코드](../synthesis/clean-code.md) 허브가 그 지형을 담는다.

## 판본과 스냅샷

- 초판(2008)이고 이후 개정판이 없다. 저자의 후속서(*The Clean Coder* 2011,
  *Clean Architecture* 2017, *Clean Craftsmanship* 2021)는 별개 소스다.
- 9개 장 중 셋은 **저자가 아닌 사람이 썼다** — 7장 Error Handling(Michael Feathers),
  2장 Meaningful Names(Tim Ottinger), 부록 A Concurrency II(Brett L. Schuchert).
  claim의 귀속은 이 책이되 절별 필자는 각주에 적는다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.
- 아카이브 스냅샷은 **EPUB이고 Calibre가 PDF에서 변환한 것**이다. 쪽 앵커
  (`<span id="page_N">`)가 **없다** — ousterhout2021과 다른 점이다. 대신 인쇄판의
  러닝헤드가 본문 텍스트로 살아남아 쪽 번호를 복원할 수 있다. 복원 절차와 그 한계는
  `it/archive/martin2008/_progress.yaml` 머리말이 정본이다.
- 각주 locator는 **장 + 절 제목 + 인쇄판 쪽**이다. 17장의 항목은 절 제목 대신
  식별자(`G5` 등)를 쓴다 — 그것이 이 책 자신의 상호 참조 방식이다.
- 반입 재개점의 정본은 `it/archive/martin2008/_progress.yaml`이다.

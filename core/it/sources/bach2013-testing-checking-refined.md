---
type: webpage
title: "Testing and Checking Refined"
author: [{family: Bach, given: James}, {family: Bolton, given: Michael}]
issued: "2013-03-26"
container-title: "James Bach's Blog"
URL: "https://www.satisfice.com/blog/archives/856"
snapshot: /it/archive/bach2013-testing-checking-refined/
snapshot_sha256: "36533c37dc979b8d0a5dee716809adf71a0bf1dd89b4edc947fa40c5f900de2c"
accessed: "2026-08-22"
custom: {archive-url: "https://web.archive.org/web/20130501/http://www.satisfice.com/blog/archives/856"}
---

# Testing and Checking Refined

**Rapid Software Testing 방법론이 테스팅과 체킹을 갈라 정의한 자리.** 머리글이
공저를 밝힌다 — *"This post is co-authored with Michael Bolton. We have spent hours
arguing about nearly every sentence."* 블로그의 서명은 James Bach이고, 본문의
1인칭 단수(*"I've been working with and arguing over this since 1987"*)도 Bach다.

**근거 등급은 실무자 선언(practitioner manifesto)이다.** 측정도 실험도 결과 표도
없고, 글 자신이 자기 지위를 규정한다 — *"We are merely stating the protocol used in
the Rapid Software Testing methodology. And we are sharing our ideas in case other
people care what we think"*(§댓글, Andrew Prentice 2013-03-31 답글). 그래서 이
소스는 학술 근거로 인용되지 않는다.

## 두 판이 있고, 문면이 다르다 — 스냅샷도 두 벌이다

같은 문서(글 번호 856)의 판이 둘이고, **이 citekey 하나에 두 판을 함께 보존한다.**

| 판 | 파일 | 취득 | 무엇이 다른가 |
|---|---|---|---|
| 2013 판 | `testing-checking-pair--satisfice-2013.html` | Wayback Machine | 최초 정의문. `algorithmic decision rules` |
| 현행판 | `testing-checking-pair--satisfice-current.html` | satisfice.com 직접 | 정의 교체 뒤. `mechanistic process` |

- **정본은 현행판 문면이다.** 개념 페이지가 인용하는 정의는 현행판을 정본으로 쓰고,
  2013 판 정의는 판본 대조를 위해 함께 인용한다.
- **2013 판의 캡처 시점.** 확보 대장이 기록한 캡처 날짜는 2013-05-01이다. 확보본에
  Wayback 툴바가 없어(원본 모드 취득) 문면 안에 타임스탬프가 남아 있지 않으므로,
  `custom.archive-url`은 **그 날짜 기준의 조회 URL**이지 캡처의 정확한 타임스탬프가
  아니다. 문면 자체로 확인되는 것은 두 가지다 — WordPress 3.3.1로 생성됐다는 헤더와
  **마지막 댓글이 2013-04-30**이라는 사실. 둘 다 2013-05-01 캡처와 어긋나지 않는다.
- **발행일 표기가 두 판에서 다르다.** 2013 판은 본문 끝에 *"This entry was posted on
  Tuesday, March 26th, 2013 at 5:04 pm"*을 인쇄한다. 현행판은 그 줄이 없고 제목 아래
  머리글이 **`PUBLISHED: AUGUST 10, 2024 BY JAMES BACH`**라고 적는다. `issued`를
  2013-03-26으로 적은 근거는 2013 판 문면이다 — 현행판 머리글의 날짜는 최종 수정일이
  발행일 자리를 차지한 것이고, 같은 페이지 안의 갱신 주석 셋이 그것을 뒷받침한다.

## 갱신 이력이 문면 안에 있다

현행판 본문 끝에 갱신 주석 셋이 날짜와 함께 새겨져 있다.

- `Update 2013-04-10` — SWET5 동료 회의 뒤 도해를 고쳤다는 기록. **2013 판에도
  같은 내용이 `UPDATE APRIL 10th:`로 들어 있다.**
- `Update, 2019-12-16` — 테스팅 정의에 `experiencing`을 더했다는 기록.
- `Update, 2024-08-10` — *"We simplified the definition of checking. Actually did
  this a few years ago and forgot to update this article."*

**세 번째 주석이 이 소스를 다루는 방식을 정한다.** 정의가 바뀐 사실은 문면에 적혀
있으나 **바뀐 시점은 적혀 있지 않다** — 저자 스스로 "몇 해 전에 이미 바꿨고 이 글을
갱신하는 것을 잊었다"고 쓴다. 그러므로 이 글의 어느 시점 문면이 어느 정의를 담고
있었는지는 이 두 스냅샷 사이에서 확정되지 않는다. **정의를 인용할 때는 반드시 판을
병기한다.**

## 같은 판 안에서 낱말이 갈린다

현행판은 체킹 정의를 두 번 싣는데 **두 문장이 서로 다르다.**

- 정의 블록: *"Checking is the mechanistic process of verifying propositions about
  the product."*
- 뒤쪽 "recall our definition of checking" 블록: *"Checking is the mechanical
  process of verifying propositions about the product."*

`mechanistic` ↔ `mechanical`이다. 설명 주석은 `mechanistic`만 풀이한다
(*"'mechanistic' means algorithmic"*). 이 KB는 **정의 블록 쪽(`mechanistic`)을
정본으로 인용하고 뒤쪽 표기 차이를 함께 적는다.** 2013 판에는 이 갈림이 없다 — 두
자리 모두 같은 문장이다.

## locator 규약

절 번호가 없다. locator는 굵은 소제목이나 문단 역할로 적고, **판을 함께 적는다.**
규약의 정본은 `it/archive/bach2013-testing-checking-refined/_progress.yaml`
머리말이다.

## 본문 밖

스냅샷에는 댓글이 함께 보존돼 있다(2013 판 49건, 현행판 67건 · 마지막 2019-08).
**본문이 아니므로 원칙적으로 반입하지 않는다.** 예외 하나 — Bach가 댓글에 직접 단
답글은 저자 발언이므로, 이 KB가 인용한 대목은 `§댓글` locator와 댓글 작성자·날짜를
함께 적어 본문과 구분한다.

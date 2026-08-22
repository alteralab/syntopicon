---
type: webpage
title: "The Insapience of Anti-Automationism"
author: [{family: Kaner, given: Cem}]
issued: "2013-02-04"
container-title: "Context Driven Testing"
URL: "https://context-driven-testing.com/the-insapience-of-anti-automationism/"
snapshot: /it/archive/kaner2013-insapience/
snapshot_sha256: "71a12bbd0faec7384feb0b5a8d499ba925d1602f5807570ee531d44f05511efe"
accessed: "2026-08-22"
---

# The Insapience of Anti-Automationism

**맥락 주도 학파의 창시자 한 사람이 같은 학파 안의 반자동화 노선을 공개로 반박한
글.** 2013년 WTST(Workshop on Teaching Software Testing) 12회에서 들은 두 장면을
계기로 쓰였고, 결론 문장이 논지를 그대로 말한다 —
*"Checking versus testing is another false dichotomy."*

**근거 등급은 실무자 에세이(essay)다.** 측정도 실험도 결과 표도 없고, 저자가 글
안에서 자기 자격을 규정한다 — *"as one of the founders of the context-driven school,
I say 'hooey!'"*. 그래서 이 소스는 학술 근거로 인용되지 않고, **학파 내부 인물의
1차 진술**로 인용된다.

## 게시처와 게시일

- 게시처는 `context-driven-testing.com`이고, 지면 이름은 `Context Driven Testing`
  이다. 문면의 머리글은 `FEBRUARY 4, 2013 BY ADMIN`이고, HTML 메타의
  `article:published_time`과 `datePublished`가 둘 다 `2013-02-04T16:47:00+00:00`
  이다. `dateModified`도 같은 값이라 **발행 뒤 본문이 고쳐진 흔적이 없다.**
- 정본 URL은 이 지면의 `<link rel="canonical">`이 적는
  `https://context-driven-testing.com/the-insapience-of-anti-automationism/`이다.
- **저자 이름이 머리글에 없다.** 머리글은 `BY ADMIN`이고, 저자 귀속은 본문
  1인칭(*"Doug Hoffman and I gave presentations…"*, *"as one of the founders of
  the context-driven school"*)과 댓글에 `Cem Kaner` 이름으로 단 답글로 확정된다.
  이 글은 **kaner.com에 없다** — 확보 대장이 그 사실을 취득 조건으로 기록했다.

## 미러 한 벌을 함께 보존한다 — 본문은 같다

Association for Software Testing(AST)이 같은 글을 신디케이션으로 싣고 있고, 그
스냅샷을 이 디렉터리에 함께 두었다.

| 자리 | 파일 | canonical |
|---|---|---|
| 정본 | `testing-checking-pair--kaner-insapience.html` | `context-driven-testing.com/the-insapience-of-anti-automationism/` |
| 미러 | `testing-checking-pair--kaner-insapience-ast-mirror.html` | `associationforsoftwaretesting.org/2013/02/04/the-insapience-of-anti-automationism/` |

- **본문 대조 결과 동일하다.** 두 파일에서 본문(첫 문단 *"Last weekend, I attended
  …"*부터 마지막 문단 *"…It denies the importance of 'context' in
  'context-driven.'"*까지)만 추출해 diff를 돌리면 차이가 0이다. 추출한 본문의
  sha256은 양쪽 모두
  `c0ced4a7c9c311b44d0d6f3713a8e8369bd22d7a590cae6f1d05058f15f2fcf5`다.
- 미러의 머리글은 `by astadmin | Syndicated`이고 게시일 표기가 없으나, HTML 메타의
  `article:published_time`은 정본과 같은 `2013-02-04T16:47:00+00:00`이다.
- **차이는 본문 밖에만 있다.** 정본에는 댓글 9건(트랙백 포함)이 붙어 있고 그중 하나가
  저자 본인의 긴 답글이다. 미러에는 댓글이 없고 대신 AST 사이트의 내비게이션과
  아카이브 목록이 붙는다.

## locator 규약

절 번호도 소제목도 없다. locator는 **문단 역할**로 적는다. 규약의 정본은
`it/archive/kaner2013-insapience/_progress.yaml` 머리말이다.

## 본문 밖

정본 스냅샷의 댓글 9건과 사이트 전역 내비게이션·아카이브 목록은 본문이 아니므로
반입하지 않았다. 예외 하나 — 저자가 `Cem Kaner` 이름으로 단 2013-02-04 답글은 저자
발언이므로, 인용할 때는 `§댓글(저자 답글, 2013-02-04)` locator로 본문과 구분한다.

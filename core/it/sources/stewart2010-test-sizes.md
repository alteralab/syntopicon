---
type: post-weblog
title: "Test Sizes"
author: [{family: Stewart, given: Simon}]
issued: "2010-12-13"
container-title: "Google Testing Blog"
URL: "https://testing.googleblog.com/2010/12/test-sizes.html"
snapshot: /it/archive/stewart2010-test-sizes/
snapshot_sha256: "f3eef2a48abcd9bac43c8f1279039dc452a8cbbe5525393f4e8074cafc9d08d4"
accessed: "2026-08-23"
---

# stewart2010-test-sizes

**크기 어휘(small·medium·large)가 처음 공개된 자리.**
[winters2020-swe-at-google](winters2020-swe-at-google.md)의 11장이 정본 서술이지만, 같은
어휘를 그 책보다 **10년 앞서** 표로 낸 것이 이 글이다. 이 KB에서 이 소스의 역할은 계보
각주이고, 정의가 책과 어디서 갈리는지를 보이는 대조본이다.

## 지위 — 산업 규범이고 측정이 없다

- **근거 등급은 `industry-norm`이다.** 측정도 표본도 없고, 본문은 명명 관행의 제안과 그
  제약 표 하나로 이루어져 있다. 글 자신이 근거로 드는 것은 사내 합의다 —
  `Over time we've come to agree on a set of data-driven naming conventions for our tests`.
- **`data-driven`이라는 낱말에 속지 않는다.** 글이 그렇게 부르는 이유는 이름이 **잴 수 있는
  제약**(네트워크 접근 여부·시간 제한 따위)으로 정의되기 때문이지, 이 분류가 데이터로
  검증됐다는 뜻이 아니다. 이 글에 효과를 잰 수치는 없다.
- **규모 전제**: 저자는 당시 구글 소속이고 글은 사내 관행을 소개한다. Java 보안 관리자로
  제약을 집행한다는 서술이 그 전제를 드러낸다.

## 판과 서지 — 문면에 인쇄된 것

- 게시일: `Monday, December 13, 2010` (`itemprop='datePublished'`)
- 저자 표시: `by Simon Stewart`, 라벨도 같은 이름
- 확보본 253KB. 게시물 본문 외에 블로그 껍데기(라벨 목록·연도별 아카이브 목차·독자 댓글
  12건)가 함께 들어 있다. **댓글은 독자가 쓴 것이므로 인용하지 않는다.** 문면에
  `New comments are not allowed.`가 있어 더 늘지 않는다.
- 살아 있는 페이지이므로 열람일 스탬프를 단다. 이 KB의 직인용은 2026-08-23 열람본에 대한
  것이다.

## 인용할 때 지킬 것

- **표의 값은 정의이지 측정이 아니다.** 시간 제한 60·300·900+초는 회사가 정한 상한이고,
  분모도 표본도 없다.
- **책과 갈리는 자리를 함께 적는다.** 이 글은 크기를 규모 어휘와 **등치**시키고
  (`A Small test equates neatly to a unit test…`), 2020년 책은 같은 자리에서 크기와
  범위를 **다른 축으로 갈라 놓는다.** 한쪽 문장을 다른 쪽 시점의 주장으로 옮기지 않는다.
- **`enormous`는 이 글에 없다.** 네 번째 크기는 책의 각주에서만 등장한다.

## 옮기지 않은 것

독자 댓글 12건, 블로그 사이드바(라벨·아카이브 목록), 그리고 댓글 안의 외부 링크다.

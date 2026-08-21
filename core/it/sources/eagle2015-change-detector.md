---
type: post-weblog
title: "Testing on the Toilet: Change-Detector Tests Considered Harmful"
author: [{family: Eagle, given: Alex}]
issued: "2015-01-27"
container-title: "Google Testing Blog"
URL: "https://testing.googleblog.com/2015/01/testing-on-toilet-change-detector-tests.html"
snapshot: /it/archive/eagle2015-change-detector/
snapshot_sha256: "f69306e60f6c3f111966b4ccbe08cb0265c302adbb5bb30a5ac75d5af656a507"
accessed: "2026-08-21"
---

# eagle2015-change-detector

**"change-detector test"라는 이름이 붙은 자리.** 구글 사내 게시물 *Testing on the
Toilet*(TotT) 한 편을 블로그로 옮긴 글이고, 본문 첫 줄이 그 출처를 밝힌다 — *"This
article was adapted from a Google Testing on the Toilet (TotT) episode."*

## 지위 — 규범 글이지 실측이 아니다

**측정도 실험도 표본도 없다.** 본문은 의사코드 예제 둘과 그 예제에 대한 판단으로만
이루어져 있고, 수치는 한 개도 없다. 그래서 이 KB는 이 소스를 **`industry-norm`(산업
규범)**으로 표기하고, 같은 페이지에 서는 심사 실증 두 편(fraser2015-user-study·
vonken2012-refactoring)과 **근거의 격을 구분해** 인용한다. 이 글로부터 인용하는 것은
정의와 규범 서술뿐이고, 어떤 수치 주장도 이 글을 근거로 삼지 않는다.

**규모 전제를 함께 읽는다.** 구글의 코드베이스와 사내 리뷰 문화를 전제로 쓰인 사내
회람물이고, 글 자신은 그 전제를 밝히지 않는다. 규모가 다른 조직으로 옮길 때 무엇이
남는지는 이 글이 답하지 않는다.

## 살아있는 문서다 — 스탬프

- 게시일: 2015년 1월 27일 (본문 날짜 줄 *"Tuesday, January 27, 2015"*)
- 저자 표시: *"by Alex Eagle"*
- 열람: 2026-08-20T17:26Z (아카이브 스냅샷이 아니라 **라이브 페이지**를 받은 것이다)
- 확보본 크기 168KB, 게시물 본문 8,934자

라이브 페이지이므로 게시물 본문이 바뀔 수 있다. 이 KB의 직인용은 위 열람 시점의
스냅샷(`snapshot_sha256`)에 대한 것이다. 확보본에는 게시물 본문 외에 블로그 껍데기
(라벨 목록·연도별 아카이브 목차·독자 댓글 2건)가 함께 들어 있다 — **댓글은 독자가 쓴
것이지 저자의 글이 아니므로 인용하지 않는다.**

원문이 함께 거는 인쇄용 TotT 원본은 Google Docs 링크
(`docs.google.com/document/d/13k8AsgYdF-2TJx9QIHHvPiuV3JMbsrMLkWmmjdYBLVg`)이고 이
KB는 확보하지 않았다.

## 코드 예제에 관하여

본문의 코드 두 조각은 실행 가능한 언어가 아니라 **의사코드**다(Scala 비슷한 표기이나
`def abs(i: Int)`에 반환 타입도 중괄호도 없다). 그래서 이 KB는 그것을 실행용 펜스로
옮기지 않고, 개념을 설명하는 자리에서 산문으로 풀거나 필요한 만큼만 인용한다.

---
type: post-weblog
title: "Just Say No to More End-to-End Tests"
author: [{family: Wacker, given: Mike}]
issued: "2015-04-22"
container-title: "Google Testing Blog"
URL: "https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html"
snapshot: /it/archive/wacker2015-e2e/
snapshot_sha256: "f4703a319df021586f149a35e535fe3d816607243b886492d1b1b8787b0730ac"
accessed: "2026-08-23"
---

# wacker2015-e2e

**70/20/10이라는 배합과 "종단 테스트를 주력으로 삼지 마라"는 논거가 실린 공개 문면.**
같은 회사의 2020년 책([winters2020-swe-at-google](winters2020-swe-at-google.md))이 적은
80/15/5와 **다른 수치**이고, 두 값 모두 측정이 아니라 제안이다. 이 KB가 이 글을 들이는
이유는 수치가 아니라 그 수치를 떠받치는 **논거**다 — 테스트의 값어치를 실패 검출이 아니라
버그 수정으로 재고, 좋은 피드백 루프의 성질 셋(빠름·신뢰·실패 위치 지목)으로 크기를
고르는 논법이 여기 있다.

## 지위 — 산업 규범이고 측정이 없다

- **근거 등급은 `industry-norm`이다.** 통제도 표본도 재현 절차도 없다. 저자는 당시 구글
  소속이고 글은 사내 관행과 그 관행의 이유를 소개한다.
- **이 글의 사례는 지어낸 것이라고 저자가 스스로 적는다.** 스위트 통과율이 날짜별로 적힌
  표는 관측 기록이 아니다 — `I present the following composite sketch based on a collection
  of real experiences familiar to both myself and other testers`. **표의 숫자를 실측으로
  옮기면 원문이 하지 않은 주장이 된다.**
- **70/20/10도 제안이다.** 문면이 `As a good first guess, Google often suggests a 70/20/10
  split`이고 바로 다음 문장이 `The exact mix will be different for each team`이다.
  목표치·제안의 문법이지 관측의 문법이 아니다.
- **규모 전제**: 글이 드는 예가 온라인 문서 편집 서비스이고 야간 빌드·전용 테스트 환경·
  협력 팀·실험실 하드웨어가 이미 있다는 조건 위에서 이야기가 진행된다. 그 인프라가 없는
  조직에 조문만 옮길 수 없다.

## 판과 서지 — 문면에 인쇄된 것

- 게시일: `Wednesday, April 22, 2015` (`<span class='publishdate' itemprop='datePublished'>`)
- 저자 표시: 본문 첫 줄 `by Mike Wacker`, 게시물 라벨도 `Mike Wacker`
- `<title>` 태그는 비어 있지 않다 — `Google Testing Blog: Just Say No to More End-to-End
  Tests`이고 `og:title`은 부제 없는 `Just Say No to More End-to-End Tests`다.
- **오늘자 재취득으로 대조했다.** 2026-08-23에 같은 주소를 다시 받아 게시물 본문
  (`itemprop='articleBody'`)을 확보본과 비교했고 **글자 하나까지 같다**(21,328자). 파일
  전체 해시는 다르지만 차이는 블로거가 요청마다 새로 찍는 값(스타일시트 질의 문자열,
  `__wavt` 토큰)뿐이고 본문·표·수치에는 차이가 없다.
- 확보본 368KB. 게시물 본문 외에 블로그 껍데기와 **독자 댓글 84건**이 함께 들어 있다.
  **댓글은 독자가 쓴 것이므로 인용하지 않는다.**
- 살아 있는 페이지이므로 열람일 스탬프를 단다. 이 KB의 직인용은 2026-08-23 열람본에
  대한 것이다.

## 인용할 때 지킬 것

- **날짜별 통과율 표(1일 남음 5% 부터 7일 초과 89.54% 까지)는 예시다.** 인용할 때 지어낸
  사례라는 것을 같은 자리에 적는다.
- **70/20/10을 "구글의 측정값"으로 옮기지 않는다.** `suggests`·`good first guess`를 함께
  옮기고, 같은 회사 2020년 책의 80/15/5와 **수치가 다르다**는 사실도 함께 적는다. 두 값의
  집계 단위도 원문에 명시된 정도가 다르다 — 2020년 책은 테스트 케이스 수라고 캡션에 적고,
  이 글은 분모를 적지 않는다.
- **`critical user journey`라는 낱말은 이 글에 없다.** 전수 대조했다. 이 글이 종단 테스트에
  남기는 몫의 문면은 `you probably still will want a small number of end-to-end tests to
  verify the system as a whole`이다. "핵심 사용자 여정만 종단으로"라는 정식화는 이 글이
  아니라 읽는 쪽이 보탠 말이므로 이 소스에 귀속시키지 않는다.
- **비교 표(Unit vs End-to-End)의 칸은 글자가 아니라 웃는 얼굴·찡그린 얼굴 그림이다.**
  `happy.png`·`sad.png` 두 이미지가 네 행에 놓여 있고, 옮길 때 그 사실을 적는다.

## 옮기지 않은 것

독자 댓글 84건, 블로그 사이드바(라벨·아카이브 목록), 그리고 **본문의 두 그림**이다.
확보본은 HTML 한 장이라 그림은 원격 주소로만 남아 있고 파일로 보존되지 않았다.
피라미드 그림에는 `alt` 텍스트가 없어 그림 안의 글자를 문면으로 확인할 수 없다 —
이 KB는 그림에 실린 수치를 인용하지 않고, 산문에 적힌 70/20/10만 옮긴다. 그림의 출처는
본문이 밝힌다: `the opening keynote of the 2014 Google Test Automation Conference`의
피라미드를 단순화한 것이라고 적혀 있다.

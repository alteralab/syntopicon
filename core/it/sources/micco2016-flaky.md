---
type: post-weblog
title: "Flaky Tests at Google and How We Mitigate Them"
author: [{family: Micco, given: John}]
issued: "2016-05-27"
container-title: "Google Testing Blog"
URL: "https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html"
snapshot: /it/archive/micco2016-flaky/
snapshot_sha256: "0558be72403e91cebafbe2329ea8c1342f245a14c553d3afa21f1c538c55a1d0"
accessed: "2026-08-23"
---

# micco2016-flaky

**한 대규모 조직이 자기 스위트의 불안정(flaky) 비율을 세 가지 분모로 나누어 공개한 짧은
글.** 이 KB에서 이 소스의 역할은
[luo2014-flaky](luo2014-flaky.md)의 각주다 — 그 논문이 **원인의 분포**를 세었다면 이 글은
**운영의 규모**를 적는다. 논문이 감사문에서 이름을 드는 사람이 이 글의 저자다.

## 지위 — 산업 규범이고 집계 절차가 없다

- **근거 등급은 `industry-norm`이다.** 심사도 통제도 재현 절차도 없고 저자는 당시 구글
  소속이다. 세 수치의 집계 기간·표본·도구가 글에 적혀 있지 않다.
- **이 글의 값은 학술 근거로 쓰지 않는다.** 규모 전제를 함께 적고, 방향의 뒷받침으로만
  쓴다.

## 분모가 셋이다 — 섞으면 다른 주장이 된다

이 글에는 백분율이 셋 나오고 **분모가 전부 다르다.** 원문 문장을 그대로 둔다.

- **1.5% — 분모는 테스트 실행(test runs)이다.**

  > Unfortunately, across our entire corpus of tests, we see a continual rate of about
  > 1.5% of all test runs reporting a "flaky" result.

- **약 16% — 분모는 테스트 개수다.**

  > Almost 16% of our tests have some level of flakiness associated with them!

- **약 84% — 분모는 통과에서 실패로 넘어간 전이(transitions)다.** 불안정 테스트의 비율이
  아니라 **전이 중 불안정 테스트가 관여한 비율**이다.

  > What we find in practice is that about 84% of the transitions we observe from pass to
  > fail involve a flaky test!

**세 값을 하나로 뭉쳐 "구글의 불안정 비율"이라 적으면 원문이 하지 않은 주장이 된다.**

## 인용할 때 지킬 것

- **불안정의 정의를 함께 옮긴다** — `We define a "flaky" test result as a test that
  exhibits both a passing and a failing result with the same code.`
- **`1000 or so individual tests`와 `15 tests will likely fail`은 예시 계산이다.**
  `consider that the average project contains 1000 or so individual tests`로 시작하는
  문단이고 관측 기록이 아니다.
- **재실행 완화의 문면**: 실패한 것만 다시 돌리는 기능, 실패 시 자동 재실행 선택지, 그리고
  **세 번 연속 실패해야만 실패로 보고하도록** 테스트를 불안정으로 표시하는 장치가 있다고
  적는다. 저자는 같은 문단에서 그것을 `hardly a perfect solution`이라 부른다.
- **독자 댓글은 인용하지 않는다.** 확보본에는 댓글이 함께 들어 있고 그중에는 저자 본인의
  답글도 있다. 그 답글 하나가 [luo2014-flaky](luo2014-flaky.md)를 가리키면서
  `Qingzhou Luo, Farah Hariri, Lamyaa Eloussi, and I analyzed in this paper`라 적는데,
  **그 논문의 저자 넷에 이 글의 저자는 들어 있지 않다**(논문은 §9 감사문에서 그의 이름을
  든다). 댓글의 이 표현을 공저 근거로 옮기지 않는다.
- 살아 있는 페이지이므로 열람일 스탬프를 단다. 이 KB의 직인용은 2026-08-23 열람본에 대한
  것이다. **현행판 재취득 대조는 하지 않았다** — 확보된 스냅샷만 근거다.

## 옮기지 않은 것

블로그 껍데기(사이드바·라벨·아카이브 목록)와 독자 댓글 전부다. 본문에서는 격리(quarantine)
도구와 불안정 수준 변화 탐지 도구를 소개하는 두 문단, 그리고 앞으로의 계획 세 항목을 개념
페이지가 요약 없이 남겨 두었다.

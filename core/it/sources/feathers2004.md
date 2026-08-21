---
type: book
title: "Working Effectively with Legacy Code"
author: [{family: Feathers, given: "Michael C."}]
issued: "2004"
publisher: "Prentice Hall PTR"
ISBN: "0131177052"
snapshot: /it/archive/feathers2004/
snapshot_sha256: "0a4da81ccc0d57f7d84677569f79f33803efea6028ae1ae5e62d33150d2c3e79"
accessed: "2026-08-21"
---

# Working Effectively with Legacy Code

**테스트가 없는 코드를 바꿀 때 무엇을 먼저 하는가**에 답하는 실무서. 저자가 "레거시
코드"를 *code without tests*로 다시 정의하고, 그 정의에서 나오는 처방(이음매 만들기 ·
의존 끊기 · 현재 동작을 기록하는 테스트)을 문제별 FAQ 형식으로 묶었다.

이 KB에서 서는 자리는 **보존 오라클(preservation oracle)의 원전**이다. 기대값을 명세가
아니라 **코드의 지금 동작**에서 길어 오는 절차를 이름 붙여 제시한 자리이고,
[테스트 오라클](../concepts/test-oracle.md) §5.3의 "이전 판본을 오라클로 쓴다"가
실무 절차로 내려온 모습이다.

## 근거 등급 — `practitioner-norm`

**이 소스를 학술 근거로 쓰지 않는다.** 책에는 실험도 표본도 측정도 없다. 저자 자신이
지위를 이렇게 규정한다 — 기법은 "coworkers and clients over the course of years"와의
작업에서 발견·학습한 것이고(Preface), 예제는 비밀유지계약 때문에 지어낸 것이며
("The examples that I use in the book are fabricated because I work under nondisclosure
agreements with clients") 대표성을 주장하지 않는다("I won't say that the examples are
always representative", Preface). 이 KB는 이 책에서 **정의·절차·저자의 규범 판단**만
인용하고, 효과 주장의 근거로는 쓰지 않는다.

**핵심 전제의 통제실험은 음성이다.** "테스트가 리팩터링을 쉽게/안전하게 한다"는 이 책의
전제를 직접 실험에 건 것이
[vonken2012-refactoring](vonken2012-refactoring.md)이고, 그 논문은 §V-B에서 이 책을
참고문헌 [25]로 지목하며 "we could not observe this in our experiment"라고 적는다.
그 소스가 세운 한정("돕지 않는다는 증명"이 아니라 "돕는다는 증거를 못 찾았다")을
넘겨 쓰지 않는다.

## 판본과 locator

- 확보본은 **EPUB**이라 조판 쪽이 없다. 대신 원문에 인쇄판 쪽 앵커(`page_NNN`)가 그대로
  들어 있어, 이 KB의 locator는 **장·절 제목 + 인쇄판 쪽**으로 적는다.
- 판권면은 `ISBN 0-13-117705-2`, `Copyright © 2005 Pearson Education, Inc.`,
  `First printing, September 2004`를 적는다. `issued: "2004"`는 이 초판 인쇄 연도를
  따랐다(저작권 표기는 2005). EPUB 패키지의 `dc:identifier`는 전자책 쪽 식별자
  `0132931753`이고 `dc:date`는 `2005`다 — 두 값이 갈리므로 위 ISBN은 **판권면 인쇄값**을
  적었다.
- 판 표기(`edition`)는 판권면에 없다. 초판만 존재한다.
- 원서만 반입했다 — 번역서 참조원은 쓰지 않았다.

## 증류 범위

**책 전체를 옮기지 않는다.** 이 소스는 반입 대상 축(검증·오라클)에 걸리는 부분만
증류한다 — Preface(레거시 코드의 정의), 1장 Changing Software(동작 보존이라는 문제
규정), 2장 Working with Feedback(Cover and Modify · 소프트웨어 바이스 · 레거시 코드
변경 알고리즘), 13장 Characterization Tests(정의·절차·용도), 용어집(정의 문면).
의존 끊기 카탈로그(25장)와 문제별 FAQ 장 대부분은 이 축의 질문 밖이다. 재개점의
정본은 `it/archive/feathers2004/_progress.yaml`이다.

---
type: report
title: "How to Misuse Code Coverage"
author: [{family: Marick, given: Brian}]
issued: "1999"
version: "1.1"
publisher: "Reliable Software Technologies"
URL: "http://www.exampler.com/testing-com/writings/coverage.pdf"
snapshot: /it/archive/marick1999-coverage/
snapshot_sha256: "8e8c629062e4d9de30bc48841294f4dac0c3b2b0461543c58d449cbbdca2da23"
accessed: "2026-08-23"
---

# marick1999-coverage

**코드 커버리지를 잘못 쓰는 방식을 목록으로 세우고 대신 어떻게 쓸지를 처방한 실무자
글이다.** 커버리지 도구를 만들어 온 사람이 그 도구의 오용을 적었다는 자리에 이 글의
무게가 있다.

## 지위 — 실무자 에세이지 실증이 아니다

**측정 절차도 표본도 통제도 없다.** 이 글에 실린 수치는 전부 저자 자신의 경험 진술이고
분모도 집계 단위도 인쇄돼 있지 않다. 그래서 이 KB는 이 소스를 **`practitioner`(실무자
에세이·기술 보고)**로 표기하고 **"학술 근거"로 쓰지 않는다.** 인용 대상은 저자가 세운
구분과 처방의 문면이다.

저자의 자기 규정이 문면에 있다.

> Code coverage tools measure how thoroughly tests exercise programs. I believe they are
> misused more often than they're used well. This paper describes common misuses in
> detail, then argues for a particular cautious approach to the use of coverage. (p.1)

`I believe`와 `argues for`가 이 글의 격이다 — 재서 보인 것이 아니라 주장한 것이다.
저자가 밝히는 자기 자격도 같은 층이다.

> While using coverage is not a lot of work, let me say that it's nonetheless **hard**.
> I've been working with coverage since 1981. I've written four coverage tools (one with
> Thomas Hoch and K. Bertram Schaefer). (p.7)

## 판과 서지 — 문면으로 확인한 것

- **판**: 2쪽부터 13쪽까지 모든 쪽의 러닝 헤더가 `How to Misuse Code Coverage Version 1.1`이다.
  1쪽에는 판 표기가 없다.
- **연도**: 1쪽 각주가 `Copyright 1997 Brian Marick, 1999 Reliable Software Technologies.
  All Rights Reserved. Permission granted to copy for personal use.`다. **두 연도가 다른
  주체에 붙어 있다** — 1997은 저자, 1999는 이 판을 낸 회사다. 그래서 이 KB는 이 판의
  `issued`를 1999로 잡고 원저작 연도 1997을 이 자리에 적어 둔다.
- **소속**: 같은 각주가 `This version of this paper was written while I was an employee of
  Reliable Software Technologies (www.rstcorp.com). I have been granted permission to
  reproduce it.`라고 적는다. 1쪽 저자 줄은 `Testing Foundations marick@testing.com` ·
  `www.testing.com`이다.
- **venue 없음.** 학회명·저널명·권·호·쪽수 줄이 문면에 없다. 학술 게재작이 아니라
  회사가 낸 글이므로 `type: report` · `publisher: Reliable Software Technologies`로
  적었다. 권·호·쪽수를 이 소스에 적을 근거는 없다.
- **쪽**: 확보본 PDF에 인쇄된 쪽 번호가 없어 이 KB의 locator는 **확보본 PDF 쪽(1~13)**이다.

## URL이 http 전용이다 — 스탬프

- 취득 URL: `http://www.exampler.com/testing-com/writings/coverage.pdf`
- **https로는 받을 수 없다**(인증서 불일치). 취득 회차가 http로 200을 확인했다.
- 열람·스냅샷: 2026-08-23 (`snapshot_sha256` 참조)

살아 있는 웹 자원이므로 원본이 사라지거나 바뀔 수 있다. 이 KB의 직인용은 위 스냅샷에
대한 것이다.

## 이 글에 실린 수치의 성격

**저자가 측정한 값은 없다.** 본문에 나오는 수는 셋 다 경험 진술이거나 남의 관행이다.

- `better than 90% (I usually get around 95%)` · `less than 4% of my total testing and
  debugging time` · `roughly twice as long` (pp.6, 9) — **저자 자신의 기대치와 경험**이고
  분모도 표본도 없다. 이 KB는 이 값들을 측정값으로 인용하지 않고, 인용할 때 저자
  경험임을 문장 안에 적는다.
- `85%` (p.8) — 저자가 관찰한 **업계 관행의 값**이지 저자가 잰 것이 아니다. 같은 쪽
  각주 7이 그 값의 유래를 스스로 무너뜨린다.
- 30%·40%·70% (pp.10~11) — 가상의 대화와 예시에 쓰인 수다. 실측이 아니다.

## 반입 범위

이 런은 1~13쪽 전부를 읽었다. 페이지로 옮긴 것은 커버리지가 무엇을 재고 무엇을 못 재는가
(pp.1~2, 5~6), 잘 쓰는 법과 관리자의 오용(pp.6~8), 시간이 부족할 때의 위험 기반 배분
(pp.9~10), 제품 테스터 쪽의 차이(pp.10~12), 요약(p.12)이다.

옮기지 않은 것: `lc` 명령행 옵션 예제와 중괄호 논쟁 일화(pp.2~4)는 커버리지 도구의
사용법을 보이는 예시라 개념 층에 필요하지 않았다. 12~13쪽의 참고문헌 넷([Glass81]·
[Herman76]·[Kaner96]·[Rapps85])은 이 글이 인용한 제3자 문헌이므로 이 반입 런은 그 값을
경유해 옮기지 않았다.

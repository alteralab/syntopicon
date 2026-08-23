---
type: speech
title: "The State of Continuous Integration Testing @Google"
author: [{family: Micco, given: John}]
issued: "2017"
snapshot: /it/archive/micco2017-ci/
snapshot_sha256: "ad19c1b13da652de85ca5502ed1518e0190e2cfb8ae608c6a1385fe5532032f0"
accessed: "2026-08-23"
---

# micco2017-ci

**발표 슬라이드 31장이다. 논문이 아니다.** 이 KB에서 이 소스의 역할은
[micco2016-flaky](micco2016-flaky.md)의 수치에 **모집단의 크기**를 붙이는 것 하나다 —
16%라는 비율의 분모가 몇 개인지가 여기 인쇄돼 있다.

## 지위 — 슬라이드 문면이고 산문이 아니다

- **근거 등급은 `industry-norm`이고, 형식은 발표 자료다.** 확보본은 제목 슬라이드부터
  Q&A 슬라이드까지 31장이고 불릿 목록으로만 돼 있다. 각 값의 집계 절차·기간·도구를 적은
  산문이 없다.
- **이 소스에서 값을 옮길 때는 "슬라이드 문면"이라고 함께 적는다.** 심사도 산문 근거도
  없는 자리에서 온 값이라는 것을 읽는 쪽이 알아야 한다.
- 텍스트 레이어 판정: `text_based`(신뢰도 0.75, OCR 필요 0/31쪽). 다만 도해가 든 슬라이드
  여러 장은 추출이 신뢰 불가로 나온다 — **그림 안의 값은 인용하지 않는다.**

## 문면에 인쇄된 값

- 2쪽 `Testing Scale at Google`: `4.2 million individual tests running continuously` ·
  `150 million test executions / day (averaging 35 runs / test / day)` ·
  `99% of all test executions pass`
- 20쪽 `Analysis of Test Results at Google` — **표본이 인쇄돼 있다**:
  `Analysis of a large sample of tests (1 month) showed:` ·
  `84% of transitions from Pass -> Fail are from "flaky" tests` ·
  `Only 1.23% of tests ever found a breakage`
- 21쪽 `Flaky Tests`: `Almost 16% of our 4.2M tests have some level of flakiness` ·
  `We spend between 2 and 16% of our compute resources re-running flaky tests`
- 25쪽 `Flakes are Inevitable`: `Continual rate of 1.5% of test executions reporting a
  "flaky" result` · `Observed insertion rate is about the same as fix rate`
- 26쪽 `Flaky Test Infrastructure`: `We re-run test failure transitions (10x) to verify
  flakiness` · `If we observe a pass the test was flaky`

## 인용할 때 지킬 것

- **16%의 분모가 여기서 확정된다** — 21쪽이 `our 4.2M tests`라 적는다. 2016년 글의
  `our tests`가 무엇이었는지를 이 슬라이드가 채운다. **다만 두 자료는 해가 다르므로 같은
  모집단이라고 단정하지 않는다.**
- **84%에는 표본 기간이 붙어 있다** — 20쪽의 `a large sample of tests (1 month)`. 2016년
  글에는 이 한정이 없다.
- **10회 재실행은 판정 절차이지 완화 정책의 전부가 아니다** — 26쪽은 실패 전이를 10회 다시
  돌려 불안정 여부를 **확인**한다고 적는다. 통과하면 통과로 처리한다는 문장이 아니다.
- **개최 정보가 확보본에 인쇄돼 있지 않다.** 발표 자리를 적으려면 리포지토리 레코드가
  근거라는 사실을 함께 적어야 한다. 이 KB는 확보본 문면에 없는 개최 정보를 적지 않는다.

## 옮기지 않은 것

지속 통합 체계의 구조 슬라이드(7~19쪽), bazel BUILD 파일 예시(28쪽), 학계 협력 프로그램
소개(29~30쪽), 참고 링크 목록(31쪽)이다. 도해로만 된 슬라이드는 추출 신뢰 불가라 아예
읽지 않았다.

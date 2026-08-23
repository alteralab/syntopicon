---
type: post-weblog
title: "Agentic Testing: Where Agents Fit in the E2E Testing Stack"
author: [{family: Gorbachov, given: Sergii}]
issued: "2026-06-11"
container-title: "Engineering at Slack"
URL: "https://slack.engineering/agentic-testing-where-agents-fit-in-the-e2e-testing-stack/"
snapshot: /it/archive/gorbachov2026-agentic-testing/
snapshot_sha256: "a082bc3a612c161b30273dba66eef1aeb88c197592b19abdac9cd30216bdf65c"
accessed: "2026-08-23"
---

# gorbachov2026-agentic-testing

**에이전트가 종단(end-to-end) 테스트를 직접 몰았을 때 얼마나 자주 실패하는가를 한 회사가
자기 제품 위에서 재어 공개한 기록.** 이 KB에서 이 소스의 역할은
[wacker2015-e2e](wacker2015-e2e.md)의 각주다 — 2015년 글이 "종단 테스트는 불안정(flaky)
하다"를 경험 진술로 적은 자리에, 판정자가 사람에서 에이전트로 바뀐 뒤의 반복 실패율을
분모와 함께 놓는다.

## 지위 — 산업 자기 보고이지 심사 실증이 아니다

- **근거 등급은 `industry-norm`이다.** 심사가 없고, 재현 자료도 공개되지 않았으며, 대상
  제품·측정자·측정 도구가 전부 같은 회사 안에 있다.
- **자기 보고의 방향을 함께 읽는다.** 실험은 Slack 자기 제품의 화면에서, Slack 사내 테스트
  작업 공간에서, Slack 사내 팀이 만든 계측 위에서 돌았다. 감사의 글이 그것을 밝힌다 —
  `Huge thanks to the DevXP AI team for building and supporting tools like Claude Code, as
  well as the metrics infrastructure that made these experiments possible.`
- **그래도 이 소스가 쓸모 있는 이유는 분모를 적었기 때문이다.** 구성마다 20회씩 돌렸다고
  실험 행렬 표에 적혀 있고 전체가 200회를 넘는다. 이 축에서 흔한 "느낌"과 다른 격이다.
- **수치가 물결표로 적혀 있다.** 원문의 요약 표가 `~12%`·`~48%` 꼴이라 이 KB도 근사임을
  지우지 않고 옮긴다.

## 판과 서지 — 문면에 인쇄된 것

- 게시일: `June 11, 2026`. 분량 표시 `12 min read`
- 저자 표시: `Sergii Gorbachov`, 직함 `Staff Software Engineer`
- **오늘자 재취득으로 대조했다.** 2026-08-23에 같은 주소를 다시 받아 `Abstract`부터
  `Acknowledgements` 앞까지의 본문을 확보본(2026-08-20 취득)과 비교했고 **글자 하나까지
  같다**(16,215자).
- 살아 있는 페이지이므로 열람일 스탬프를 단다. 이 KB의 직인용은 2026-08-23 열람본에
  대한 것이다.

## 실험 설계 — 인용할 때 반드시 함께 적을 것

- **집계 단위는 실행 회차다.** 구성 하나당 20회, 흐름 두 개, 실행 방식 다섯 가지
  (실험 행렬 표 `Experiment Matrix`).
- **흐름은 둘이고 길이가 다르다** (§2 `Test flows`). `Thread Reply`가 단계 15~20개로 쉬운
  쪽, `Search Discovery`가 단계 25~30개로 어려운 쪽이다. **실패율의 두 값은 난이도가 다른
  두 흐름의 값이지 오차 범위가 아니다.**
- **모델과 도구가 고정돼 있다** (§2 `Experiment Setup`). 에이전트 쪽은 Claude Sonnet 4.5,
  테스트를 생성하는 쪽은 Claude Opus 4.6, 실행은 비대화식 Claude Code(`claude -p`),
  브라우저는 Playwright MCP와 Playwright CLI다.
- **프로덕션 데이터가 아니다** — `All experiments were conducted in test workspaces using
  non-production data`.
- **범위 한정을 저자가 스스로 적는다** (§3 `Execution Capability Boundaries`). 실험은 단일
  세션 화면 흐름에 한하고, 작업 공간을 넘나들거나 창을 여럿 여는 흐름은 다루지 않았다.

## 인용할 때 지킬 것

- **실패율은 Slack이 스스로 잰 값이다.** 다른 조직의 에이전트 검증 루프에 그대로 옮기지
  않는다. 화면·모델·도구·흐름이 전부 이 실험의 것이다.
- **비용과 시간은 결과 절의 값을 쓴다** (§3 `Cost and Where It Comes From`,
  §3 `Speed`). 도입부 `The Problem` 절에도 같은 범위가 적혀 있으나 그쪽은 동기 서술이다.
- **"에이전트가 종단 테스트를 대체한다"는 결론이 이 글에 없다.** 저자의 결론은 층을
  더한다는 쪽이다 — `Rather than replacing existing approaches, it adds a new capability on
  top of them.`
- **거짓 통과·거짓 실패는 이 글이 재지 않았다.** 잰 것은 실패율이고, 통과한 회차가 실제로
  옳게 통과했는지를 따로 판정한 절차가 적혀 있지 않다.

## 옮기지 않은 것

머리말·꼬리말의 사이트 껍데기(글 목록·연도별 아카이브·추천 읽을거리), 채용 안내, 그리고
본문의 그림 둘이다. 확보본은 HTML 한 장이라 그림 파일은 원격 주소로만 남았다. 다만 그림에
`alt` 텍스트가 달려 있어 그림이 무엇을 그렸는지는 문면으로 확인된다 —
`Agentic vs. traditional testing paths`와 `Testing pyramid with four layers: Unit Tests,
Integration Tests, E2E Testing, and Agentic Testing`이다. **그림 안의 수치는 없다.**

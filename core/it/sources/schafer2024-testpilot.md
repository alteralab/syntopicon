---
type: article-journal
title: "An Empirical Evaluation of Using Large Language Models for Automated Unit Test Generation"
author:
  - { family: "Schäfer", given: "Max" }
  - { family: "Nadi", given: "Sarah" }
  - { family: "Eghbali", given: "Aryaz" }
  - { family: "Tip", given: "Frank" }
issued: "2024"
container-title: "IEEE Transactions on Software Engineering"
number: "2302.06527"
snapshot: /it/archive/schafer2024-testpilot/
snapshot_sha256: "457f552a20d9f918f05a93e297aa238171414a142abc280172444f5986c3dbfa"
accessed: "2026-08-21"
---

# schafer2024-testpilot

TESTPILOT — 추가 학습 없이 프롬프트만으로 JavaScript 단위 테스트를 만드는 도구와, 그
생성물을 npm 패키지 25개·API 함수 1,684개에 걸쳐 잰 대규모 실증. `yuan2024-chatgpt-tests`와
**같은 모델 세대(gpt-3.5-turbo, 여기서는 `gpt-3.5-turbo-0301`)를 다른 언어·프레임워크에
적용한 대조군**이라, 이 KB에서는 결함 분해 비율이 환경에 얼마나 의존하는지를 재는 자리로
쓴다.

**확보본은 저자본이라 게재 표면이 문면에 없다.** 파일은 arXiv:2302.06527v4(2023-12-11
스탬프)이고 21쪽이며, 저널명·권·호·쪽수 어느 것도 인쇄돼 있지 않다. 위 frontmatter의
`container-title`과 `issued: 2024`는 **리포지토리 레코드가 근거이고 원문 문면이 아니다**.
그래서 이 KB는 이 소스에 권·호·쪽수를 적지 않고, locator는 확보본의 절 번호와 표 번호로만
단다(§4.3 Table 3, §4.4 등).

**인용 가능한 수치의 자리**: §4의 결과 표와 그 절의 본문 진술. 초록과 §1 서론이 같은 값을
미리 요약하지만 그쪽은 인용 대상이 아니다. 집계 단위가 대부분 **패키지별 중앙값**이라
단위를 빼고 옮기면 뜻이 바뀐다 — "생성 테스트의 61.4%"가 아니라 "패키지당 비율의 중앙값이
61.4%"다.

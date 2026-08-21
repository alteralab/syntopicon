---
type: article-journal
title: "No More Manual Tests? Evaluating and Improving ChatGPT for Unit Test Generation"
author:
  - { family: "Yuan", given: "Zhiqiang" }
  - { family: "Liu", given: "Mingwei" }
  - { family: "Ding", given: "Shiji" }
  - { family: "Wang", given: "Kaixin" }
  - { family: "Chen", given: "Yixuan" }
  - { family: "Peng", given: "Xin" }
  - { family: "Lou", given: "Yiling" }
issued: "2024-07"
container-title: "Proceedings of the ACM on Software Engineering"
DOI: "10.1145/3660783"
snapshot: /it/archive/yuan2024-chatgpt-tests/
snapshot_sha256: "debfc19bbf4e0c921c1bc903aab0bc09c02c448d4f24f5da42925b9e138513f6"
accessed: "2026-08-21"
---

# yuan2024-chatgpt-tests

LLM이 생성한 단위 테스트가 어디서 얼마나 틀리는지를 전수 계량한 실증 연구. Fudan
University 연구진의 심사 통과본이고, **게재 표면이 파일 문면에 인쇄돼 있다** — 쪽머리와
판권 블록이 `Proc. ACM Softw. Eng., Vol. 1, No. FSE, Article 76. Publication date: July
2024.`와 DOI `10.1145/3660783`을 매 쪽에 찍는다. 권·호·아티클 번호(1, FSE, 76)는 그래서
리포지토리 레코드가 아니라 원문 문면이 근거다. 확보본은 저자가 같은 조판(acmart)으로
arXiv에 올린 판(arXiv:2305.04207v3, 2024-05-19 스탬프)이고 24쪽이다. 쪽 표기는
`76:1`–`76:24` 꼴이고 PDF 쪽과 뒷자리가 일치한다.

**지위는 실측이다 — 이 논문 자신이 잰 결과 표가 있다.** 인용 가능한 수치는 §4의 결과
표(Table 2·4·5), §6의 평가 표(Table 7·9), 그리고 §7 위협 절이 직접 잰 Python 대조값이다.
§1 서론이 같은 수치를 미리 요약하지만 그쪽은 인용 대상으로 삼지 않는다.

**모든 수치에 모델·시점·언어·데이터셋이 붙는다.** 대상 모델은 `gpt-3.5-turbo`이고
(§3.4, p.76:7 — GPT-4는 당시 비산업 사용자 API 한도 때문에 제외했다고 적혀 있다),
프로젝트 수집은 2023-03-25 기준 GitHub 클론이며(§3.1, p.76:5), 벤치마크는 Maven으로
빌드되는 Java 프로젝트 185개에서 뽑은 focal method 1,000개다. 이 소스의 절대 수치를
"LLM 테스트 생성 일반"으로 옮겨 읽으면 거짓이 된다 — 같은 논문이 §6.2.2에서 다른
모델로, §7에서 다른 언어로 값이 크게 달라지는 것을 스스로 보인다.

각주 원문으로 함께 확보한 세 편은 각자 citekey를 받았다: `schafer2024-testpilot`(같은
모델·다른 언어의 대조군, 심사 저널), `wang2025-mutgen`·`banik2026-allsmoke`(둘 다 미심사
프리프린트라 방향만 쓴다).

---
type: concept
title: 쿼리 재작성
description: 대화 맥락 없이는 뜻이 서지 않는 질의를 홀로 서는 질의로 고쳐 쓰는 전술 — 재구성·정규화·확장이라는 다른 이름들, 전통적 검색 엔진의 휴리스틱과 AI 애플리케이션의 프롬프트가 갈리는 자리, 그리고 신원 해소가 끼어들 때 재작성 모델이 환각하는 대신 못 푼다고 말해야 하는 이유
generated: { by: "claude-opus-5", at: "2026-08-16T17:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 쿼리 재작성

- [이름들](#이름들)
- [무엇이 문제인가](#무엇이-문제인가)
- [누가 다시 쓰는가](#누가-다시-쓰는가)
- [신원 해소가 끼어들 때](#신원-해소가-끼어들-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **앞 대화에 기대야만 뜻이 통하는 질의를 어떻게 검색 가능한 질의로 만드는가.**

## 이름들

- **쿼리 재작성(query rewriting)은 쿼리 재구성(query reformulation)·쿼리 정규화(query
  normalization), 때로는 쿼리 확장(query expansion)으로도 알려져 있다** (6장,
  p.270).[^huyen2025]

## 무엇이 문제인가

- 저자가 든 대화다 (6장, p.270):[^huyen2025]

  > *User*: When was the last time John Doe bought something from us?
  > *AI*: John last bought a Fruity Fedora hat from us two weeks ago, on January 3, 2030.
  > *User*: How about Emily Doe?

- 진단과 처방 — **마지막 질문 "How about Emily Doe?"는 맥락 없이는 모호하다. 이 질의를 그대로 써서
  문서를 검색하면 무관한 결과를 얻을 가능성이 높다. 사용자가 실제로 묻고 있는 것을 반영하도록 이
  질의를 다시 써야 한다. 새 질의는 그 자체로 뜻이 통해야 한다. 이 경우 질의는 "When was the last
  time Emily Doe bought something from us?"로 다시 쓰여야 한다** (6장, p.270).[^huyen2025]

## 누가 다시 쓰는가

- 범위와 두 갈래 — **저자는 쿼리 재작성을 RAG 절에 넣었지만 쿼리 재작성은 RAG에 고유하지 않다.
  전통적 검색 엔진에서 쿼리 재작성은 흔히 휴리스틱을 써서 이뤄진다. AI 애플리케이션에서 쿼리 재작성은
  다른 AI 모델을 써서, "Given the following conversation, rewrite the last user input to reflect
  what the user is actually asking"와 비슷한 프롬프트로 이뤄질 수도 있다** (6장,
  p.270).[^huyen2025]
- 도판이 보인 것 — **그 프롬프트를 써서 ChatGPT가 질의를 다시 쓴 결과가 앞의 대화를 넣었을 때
  "When was the last time Emily Doe bought something from us?"였다** (6장, p.270, Figure
  6-4).[^huyen2025]

## 신원 해소가 끼어들 때

- 어려워지는 지점 — **쿼리 재작성은 복잡해질 수 있는데, 특히 신원 해소(identity resolution)를 하거나
  다른 지식을 넣어야 할 때 그렇다. 예컨대 사용자가 "How about his wife?"라고 물으면 먼저 그의 아내가
  누구인지 알아내려고 데이터베이스에 질의해야 한다** (6장, p.270).[^huyen2025]
- 정보가 없을 때의 규정 — **그 정보를 갖고 있지 않다면, 재작성 모델은 환각해서 틀린 답으로 이어지는
  대신 이 질의를 풀 수 없다는 것을 인정해야 한다** (6장, p.270).[^huyen2025]

## 이어지는 페이지

- [청킹 전략](../concepts/chunking-strategy.md) — 같은 절의 다른 검색 최적화 전술
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 〃
- [컨텍스트 증강 검색](../concepts/contextual-retrieval.md) — 질의가 아니라 문서 쪽을 고치는 짝
- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 이 전술이 놓이는 파이프라인
- [프롬프트 분해](../concepts/prompt-decomposition.md) — 다른 모델 호출을 하나 더 끼워 넣는 같은
  구조의 관행
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 재작성 모델이 환각할 때의 근거
- [에이전트 계획](../concepts/agent-planning.md) — 의도 분류가 같은 질문을 다루는 자리

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Retrieval
    Optimization" 절 안의 "Query rewriting" 항목(p.270)을 담았다. Figure 6-4(ChatGPT가 질의를 다시
    쓰는 화면 갈무리, p.270)는 그 안의 프롬프트와 대화 문자열, 그리고 출력 문자열만 옮겼다. 대화 예의
    날짜(January 3, 2030)는 원문 표기 그대로다.

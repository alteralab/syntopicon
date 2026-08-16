---
type: concept
title: 컨텍스트 증강 검색
description: 청크가 검색되기 쉽도록 청크 쪽에 맥락을 덧붙이는 전술 — 태그·키워드·리뷰 같은 메타데이터와 임베딩이 흐려 버린 오류 코드를 되살리는 자리, 그 청크가 답할 수 있는 질문을 미리 붙여 두는 방식, 그리고 쪼개면서 잃은 원문 맥락을 모델에게 50–100 토큰으로 써 달라고 시키는 앤트로픽의 절차와 그 프롬프트 전문
generated: { by: "claude-opus-5", at: "2026-08-16T17:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 컨텍스트 증강 검색

- [착상](#착상)
- [메타데이터로 증강하기](#메타데이터로-증강하기)
- [답할 수 있는 질문으로 증강하기](#답할-수-있는-질문으로-증강하기)
- [원문의 맥락을 청크에 되돌리기](#원문의-맥락을-청크에-되돌리기)
- [앤트로픽이 쓴 프롬프트](#앤트로픽이-쓴-프롬프트)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **문서를 쪼개면서 잃어버린 맥락을 어떻게 청크에 되돌려 검색되게 하는가.**

## 착상

- **컨텍스트 검색(contextual retrieval) 뒤의 착상은 관련 청크를 검색하기 쉽게 만들려고 각 청크를
  관련 맥락으로 증강하는 것이다** (6장, p.271).[^huyen2025]

## 메타데이터로 증강하기

- 단순한 기법 — **단순한 기법은 청크를 태그와 키워드 같은 메타데이터로 증강하는 것이다. 이커머스에서
  제품은 그 설명과 리뷰로 증강될 수 있다. 이미지와 비디오는 그 제목이나 캡션으로 질의될 수 있다**
  (6장, p.271).[^huyen2025]
- 자동 추출한 엔티티 — **메타데이터는 청크에서 자동으로 추출된 엔티티도 포함할 수 있다. 문서가 오류
  코드 EADDRNOTAVAIL (99) 같은 특정 용어를 담고 있다면, 그것을 문서의 메타데이터에 더함으로써
  문서가 임베딩으로 변환된 뒤에도 시스템이 그 키워드로 그것을 검색할 수 있게 된다** (6장,
  p.271).[^huyen2025] 임베딩이 그런 키워드를 흐리게 만드는 문제는
  [검색 품질 평가](../concepts/retrieval-evaluation.md)에서 지적된 것과 같은 것이다.

## 답할 수 있는 질문으로 증강하기

- 방법 — **각 청크를 그것이 답할 수 있는 질문으로 증강할 수도 있다. 고객 지원에서는 각 문서를 관련
  질문으로 증강할 수 있다. 예컨대 비밀번호 재설정 방법에 관한 글은 "How to reset password?"·
  "I forgot my password"·"I can't log in", 나아가 "Help, I can't find my account" 같은 질의로 증강할
  수 있다** (6장, p.271).[^huyen2025]
  - 각주의 실무 보고 — **어떤 팀들은 데이터가 질문–답 형식으로 조직될 때 자기 검색 시스템이 가장 잘
    작동한다고 저자에게 말했다** (6장, p.271 각주 9).[^huyen2025]

## 원문의 맥락을 청크에 되돌리기

- 문제 — **문서가 여러 청크로 쪼개지면 어떤 청크는 검색기가 그 청크가 무엇에 관한 것인지 이해하도록
  돕는 데 필요한 맥락을 결여할 수 있다. 이를 피하려고 각 청크를 원 문서의 제목과 요약 같은 원 문서의
  맥락으로 증강할 수 있다** (6장, p.271).[^huyen2025]
- 앤트로픽이 한 것 — **앤트로픽은 AI 모델을 써서, 청크와 그 청크가 원 문서와 맺는 관계를 설명하는
  짧은 맥락을 통상 50–100 토큰으로 생성했다(Anthropic, 2024)** (6장, p.271).[^huyen2025]
- 그 뒤의 처리 — **각 청크에 대해 생성된 맥락은 각 청크 앞에 덧붙여지고, 증강된 청크가 검색
  알고리즘에 의해 색인된다** (6장, p.272).[^huyen2025]
  - 도판이 그리는 전처리 경로 — **말뭉치가 Chunk 1·Chunk 2·…·Chunk X로 쪼개지고, 각 청크마다 그것을
    문서 안에 자리 잡게 하는 프롬프트가 돌아, Context 1 + Chunk 1 · Context 2 + Chunk 2 · … ·
    Context X + Chunk X가 만들어진다. 그 결과는 임베딩 모델을 거쳐 벡터 데이터베이스로, 그리고
    TF-IDF를 거쳐 TF-IDF 색인으로 각각 들어간다** (6장, p.272, Figure 6-5).[^huyen2025]
  - 도판 설명 — **앤트로픽은 각 청크를 그 청크를 원 문서 안에 자리 잡게 하는 짧은 맥락으로 증강해,
    질의가 주어졌을 때 검색기가 관련 청크를 찾기 쉽게 만든다. 이미지는 "Introducing Contextual
    Retrieval"(Anthropic, 2024)에서 왔다** (6장, p.272, Figure 6-5 설명).[^huyen2025]

## 앤트로픽이 쓴 프롬프트

- **앤트로픽이 이 목적으로 쓴 프롬프트다(Anthropic, 2024).** 원문 표기를 그대로 옮겼다 (6장,
  p.271):[^huyen2025]

  ```text
  <document>
  {{WHOLE_DOCUMENT}}
  </document>

  Here is the chunk we want to situate within the whole document:

  <chunk>
  {{CHUNK_CONTENT}}
  </chunk>

  Please give a short succinct context to situate this chunk within the
  overall document for the purposes of improving search retrieval of the
  chunk. Answer only with the succinct context and nothing else.
  ```

## 이어지는 페이지

- [청킹 전략](../concepts/chunking-strategy.md) — 여기서 되돌리려는 맥락을 잃게 만든 자리
- [쿼리 재작성](../concepts/query-rewriting.md) — 문서가 아니라 질의 쪽을 고치는 짝
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 같은 절의 다른 전술
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — 임베딩이 키워드를 흐리는 문제가 나온 자리
- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 도판에서 TF-IDF 색인이 따로 서는 이유
- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 이 전술이 놓이는 파이프라인
- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 저 프롬프트가 따르는
  쓰기 관행

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Retrieval
    Optimization" 절 안의 "Contextual retrieval" 항목(pp.271–272)을 담았다. 앤트로픽 프롬프트는 원문
    표기를 그대로 옮겼다. Figure 6-5(앤트로픽의 전처리 흐름도, p.272)는 그 안에 인쇄된 상자 이름과
    화살표 방향, 도판 설명만 옮겼다. Anthropic(2024, "Introducing Contextual Retrieval")은 huyen2025를
    통한 전언이다.

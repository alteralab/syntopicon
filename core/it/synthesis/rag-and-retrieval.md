---
type: synthesis
title: RAG와 검색
description: 질의마다 다른 맥락을 외부 기억에서 골라 오는 패턴 — RAG 구조, 용어 기반과 임베딩 기반 검색, 검색 평가, 하이브리드와 리랭킹, 청킹·쿼리 재작성·맥락 증강의 최적화, 텍스트 너머의 RAG
generated: { by: "claude-fable-5", at: "2026-08-17T01:30:00Z" }
---

# RAG와 검색

축은 하나다 — **질의마다 다른 맥락을, 외부 기억에서 골라 온다.** 컨텍스트 창이 아무리 자라도
무엇을 넣을지 고르는 문제는 남고, 그 고르기가 검색이라는 것이 이 축의 요지다.

## 패턴과 구조

- [검색 증강 생성](../concepts/retrieval-augmented-generation.md) — RAG의 구조와 계보(FiD),
  검색을 탈지 정하는 세 갈래(사전 라우팅·생성 중 결정·모델 내장 판단), 왜 컨텍스트가 길어져도 검색이 남는가

## 검색 알고리즘

- [용어 기반 검색](../concepts/term-based-retrieval.md) — 낱말이 겹치는 문서 가운데 무엇을 먼저
  줄 것인가, TF-IDF와 BM25
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — 의미 공간에서의 이웃 찾기와
  ANN 색인이 딛는 자리
- [검색 평가](../concepts/retrieval-evaluation.md) — 맥락 정밀도와 재현율, 검색기 자체를 재는 법
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 두 검색기를 섞는 법,
  리랭커 계보 셋(BERT 분류·seq2seq 목표 토큰·LLM 리스트와이즈)과 컨텍스트 배치의 위치 편향

## 검색 최적화

- [청킹 전략](../concepts/chunking-strategy.md) — 문서를 가르는 단위와 크기의 맞바꿈, 재귀 요약
  트리(RAPTOR)라는 대안
- [쿼리 재작성](../concepts/query-rewriting.md) — 질의를 검색이 잘 되는 꼴로 고치기, 생성 도중
  질의를 만드는 쪽까지
- [맥락 증강 검색](../concepts/contextual-retrieval.md) — 청크에 맥락을 붙여 검색 실패를 줄이기

## 텍스트 너머

- [텍스트 너머의 RAG](../concepts/rag-beyond-text.md) — 멀티모달 문서, 표 데이터, 그리고 지식 그래프
  위의 RAG — 커뮤니티 요약·개인화 페이지랭크·이중 수준 검색 셋

## 다른 축에서 여기로 이어지는 자리

- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — ANN 알고리즘들이 색인
  구조의 관점에서 서술되는 자리
- [전문 검색 색인](../concepts/full-text-search-indexes.md) — 역색인이 점수 계산의 재료를 저장하는
  자리
- [프롬프트에 맥락 넣기](../concepts/providing-context-in-prompts.md) — 골라 온 맥락이 프롬프트로
  들어가는 쪽
- [컨텍스트 길이와 효율](../concepts/context-length-and-efficiency.md) — 긴 컨텍스트 논쟁과 컨텍스트
  리랭킹
- [사실 일관성](../concepts/factual-consistency.md) — 검색이 환각을 줄이는 근거가 평가되는 자리

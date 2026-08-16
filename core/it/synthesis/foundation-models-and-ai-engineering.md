---
type: synthesis
title: 파운데이션 모델과 AI 엔지니어링
description: 언어 모델에서 파운데이션 모델까지의 계보와 그 위에 선 공학 분야 — 모델이 규모를 얻은 방식, 모델을 만드는 설계 결정(데이터·구조·규모·사후 훈련)과 출력을 고르는 샘플링, 그 능력이 만든 유스케이스, 짓기 전에 던지는 질문, 그리고 애플리케이션 개발·모델 개발·인프라의 세 층
generated: { by: "claude-opus-5", at: "2026-08-16T15:00:00Z" }
---

# 파운데이션 모델과 AI 엔지니어링

축은 하나다 — **모델을 만드는 일에서 남이 만든 모델을 적응시키는 일로 무게가 옮겨 갔다는 것.**
그 아래로 모델이 어떻게 지금 크기가 되었는지의 계보가 있고, 위로는 그 모델 위에서 제품을 짓는
사람이 던지는 질문과 손대는 층들이 있다.

## 모델의 계보

- [언어 모델과 토큰](../concepts/language-models-and-tokens.md) — 언어 모델이 담는 확률, 토큰과
  어휘, 마스크드와 자기회귀의 갈림, 완성 기계라는 관점
- [자기지도와 모델 규모](../concepts/self-supervision-and-model-scale.md) — 레이블링 병목을 우회한
  훈련 방식과 계속 옮겨 가는 "large"의 기준
- [파운데이션 모델](../concepts/foundation-models.md) — 텍스트 밖의 양식, 멀티모달 모델과 LMM,
  과제 특화에서 범용으로

## 모델을 만드는 설계 결정

- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 데이터 출처와 품질, 가진 것을 쓴다는 접근의 결과
- [다국어 모델](../concepts/multilingual-models.md) — 언어별 데이터 편중이 성능·지연·요금으로 넘어오는 자리
- [도메인 특화 모델](../concepts/domain-specific-models.md) — 인터넷에 없는 데이터를 위해 따로 만드는 모델
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 어텐션과 트랜스포머 블록, 프리필과 디코드
- [대안 모델 구조](../concepts/alternative-model-architectures.md) — RWKV·SSM·Mamba·Jamba와 새 구조의 문턱
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — 파라미터·훈련 토큰·FLOP과 희소 모델
- [스케일링 법칙](../concepts/scaling-laws.md) — 컴퓨트 예산 안의 배분과 데이터·전기 병목
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 완성 기계를 대화 상대로 바꾸는 첫 단계
- [선호 파인 튜닝](../concepts/preference-finetuning.md) — 보상 모델과 RLHF

## 모델이 출력을 고르는 방식

- [샘플링 전략](../concepts/sampling-strategies.md) — 로짓·소프트맥스·온도·top-k·top-p와 정지 조건
- [테스트 시점 컴퓨트](../concepts/test-time-compute.md) — 여러 출력을 뽑아 고르는 전략과 그 한계
- [구조화 출력](../concepts/structured-outputs.md) — 형식을 지키게 만드는 네 자리
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 비일관성과 환각, 그 두 가설

## 분야와 그 수요

- [AI 엔지니어링이란](../concepts/ai-engineering-defined.md) — 정의와 이 분야를 지금 자라게 한
  세 요인
- [파운데이션 모델의 유스케이스](../concepts/foundation-model-use-cases.md) — 여덟 범주와 그 분포,
  코딩부터 워크플로 자동화까지의 실물

## 짓기 전에 던지는 질문

- [AI 유스케이스 평가](../concepts/ai-use-case-evaluation.md) — 왜 만드는가, AI와 사람이 각각 무엇을
  맡는가, 무엇이 해자인가
- [AI 제품의 기대치와 유지보수](../concepts/ai-product-expectations-and-maintenance.md) — 성공을 재는
  지표와 유용성 임계, 라스트 마일, 빠른 변화 위의 유지보수

## 스택

- [AI 엔지니어링 스택](../concepts/ai-engineering-stack.md) — 애플리케이션 개발·모델 개발·인프라의
  세 층과 층별 성장의 비대칭
- [애플리케이션 개발 층](../concepts/ai-application-development-layer.md) — 평가, 프롬프트 엔지니어링과
  맥락 구성, AI 인터페이스
- [모델 개발 층](../concepts/ai-model-development-layer.md) — 모델링과 훈련, 데이터셋 엔지니어링,
  추론 최적화
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 가중치를 고치는가로 갈리는 두 범주와
  훈련 단계를 가리키는 낱말들
- [AI 엔지니어링과 ML 엔지니어링](../concepts/ai-engineering-versus-ml-engineering.md) — 두 일의 차이
  세 가지와 뒤집힌 작업 순서

## 이 축에서 갈라져 나간 허브

- [AI 평가](ai-evaluation.md) — 열린 출력을 재는 방법론 전체. 애플리케이션 개발 층의 평가 책임이
  독립한 축
- [프롬프트 엔지니어링](prompt-engineering.md) — 가중치를 바꾸지 않는 첫 번째 적응 기법. 쓰기의
  관행부터 공격과 방어까지
- [RAG와 검색](rag-and-retrieval.md) — 질의마다 다른 맥락을 외부 기억에서 골라 오는 패턴과 그
  검색의 전부
- [AI 에이전트](ai-agents.md) — 도구를 쥐고 행동하는 시스템: 계획·반성·기억과 실패 모드
- [파인 튜닝](finetuning.md) — 가중치를 바꿔 모델을 적응시키는 쪽: 언제 하는가부터 메모리·PEFT·
  병합·전술까지

## 다른 축에서 여기로 이어지는 자리

- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 임베딩 모델과 그 색인이
  저장 엔진 축에서 서술되는 자리
- [배치 처리의 유스케이스](../concepts/batch-use-cases.md) — LLM 훈련 데이터 준비가 배치 잡으로
  도는 쪽
- [수명 주기의 변환 단계](../concepts/transformation-in-the-lifecycle.md) — 특징 공학이 데이터셋
  엔지니어링으로 무게를 옮기는 자리

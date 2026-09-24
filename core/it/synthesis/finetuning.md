---
type: synthesis
title: 파인 튜닝
description: 가중치를 바꿔 모델을 적응시키는 쪽 — 언제 하고 언제 안 하는가부터 메모리 병목과 수치 형식, 파라미터 효율 기법과 LoRA, 모델 병합, 그리고 실행의 전술까지
generated: { by: "claude-fable-5", at: "2026-08-17T04:00:00Z" }
---

# 파인 튜닝

축은 하나다 — **모델의 가중치를 실제로 바꾸는 적응.** 프롬프트로 안 되는 것이 확인된 뒤에야
오는 선택이고, 그 순간부터 메모리·수치 형식·서빙이라는 엔지니어링이 따라붙는다는 것이
이 축의 요지다.

## 개요와 결정

- [전이 학습](../concepts/transfer-learning.md) — 파인 튜닝이 딛고 선 계보
- [파인 튜닝의 갈래](../concepts/types-of-finetuning.md) — 자기지도·지도·선호·인필링·롱컨텍스트,
  모델 개발자와 앱 개발자의 다른 몫
- [언제 파인 튜닝하는가](../concepts/when-to-finetune.md) — 하는 이유와 하지 않는 이유, 네 겹의
  선투자
- [파인 튜닝과 RAG](../concepts/finetuning-versus-rag.md) — 행동의 실패와 정보의 실패, 다섯 단계
  선택 프레임

## 메모리 병목

- [훈련 가능 파라미터와 역전파](../concepts/trainable-parameters-and-backpropagation.md) — 훈련이
  추론보다 메모리를 더 먹는 이유
- [모델 메모리 산수](../concepts/model-memory-math.md) — 파라미터 수와 바이트 수로 하는 어림
- [수치 형식](../concepts/numerical-formats.md) — FP32에서 BF16까지, 정밀도와 범위의 맞바꿈
- [양자화](../concepts/quantization.md) — 비트를 줄이는 시점과 방식

## 파라미터 효율

- [파라미터 효율 파인 튜닝](../concepts/parameter-efficient-finetuning.md) — 전체를 안 건드리는
  기법들의 지도
- [LoRA](../concepts/lora.md) — 저계수 분해의 기제와 설정, QLoRA
- [LoRA 어댑터 서빙](../concepts/serving-lora-adapters.md) — 어댑터를 여럿 얹어 내보내는 쪽

## 모델 병합

- [모델 병합](../concepts/model-merging.md) — 훈련 없이 모델을 합치는 이유
- [모델 병합의 접근들](../concepts/model-merging-approaches.md) — 더하기·계층 쌓기·이어붙이기

## 전술

- [파인 튜닝의 세 선택](../concepts/finetuning-setup-choices.md) — 방법·모델 크기·프레임워크
- [파인 튜닝 하이퍼파라미터](../concepts/finetuning-hyperparameters.md) — 학습률·배치·에폭·프롬프트
  손실 가중치

## 다른 축에서 여기로 이어지는 자리

- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 프롬프트 기반과 가중치 기반이
  갈리는 지도
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 모델 제작자 관점의 사후 훈련 기제
- [선호 파인 튜닝](../concepts/preference-finetuning.md) — 보상 모델과 RLHF의 기제
- [검색 증강 생성](../concepts/retrieval-augmented-generation.md) — 정보의 실패를 맡는 대안
- [도메인 특화 모델](../concepts/domain-specific-models.md) — 범용 대 특화 논쟁이 파인 튜닝 결정에
  얹히는 자리
- [데이터셋 엔지니어링이란](../concepts/dataset-engineering-defined.md) — 파인 튜닝 데이터의 형식과
  수량이 넘어가는 축
- [멀티테넌트 GenAI 정제와 멀티테넌시가 더하는 것](../concepts/multi-tenant-genai-refinements.md) — 전역
  파인 튜닝과 테넌트 수준 파인 튜닝이 갈리고 논리 모델이 서는 자리
- [더 그린한 머신러닝](../concepts/greener-machine-learning.md) — 훈련과 추론의 탄소를 갈라 재고 파인
  튜닝의 반복이 배출로 환산되는 자리

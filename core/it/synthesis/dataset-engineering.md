---
type: synthesis
title: 데이터셋 엔지니어링
description: 예산 안에서 최선의 모델을 훈련할 데이터셋을 만드는 일 — 큐레이션의 세 기준(품질·커버리지·수량), 확보와 주석, 데이터 증강·합성과 그 검증·한계, 증류, 그리고 점검·중복 제거·정제의 처리 단계
generated: { by: "claude-fable-5", at: "2026-08-17T06:30:00Z" }
---

# 데이터셋 엔지니어링

축은 하나다 — **예산 안에서 최선의 모델을 훈련할 데이터셋을 만드는 일.** 모델 중심에서 데이터
중심으로 무게가 옮겨 갔고, 무엇을 얼마나 어떤 형식으로 모을지가 곧 모델의 상한이 된다는 것이
이 축의 요지다.

## 큐레이션 기준

- [데이터셋 엔지니어링이란](../concepts/dataset-engineering-defined.md) — 데이터 중심 AI라는 관점과
  이 일의 규정
- [데이터 큐레이션의 요구 조건](../concepts/data-curation-requirements.md) — 훈련 방식이 정하는
  형식, CoT와 도구 사용 데이터, 세 기준
- [훈련 데이터 품질](../concepts/training-data-quality.md) — 좋은 데이터의 여섯 특성
- [훈련 데이터 커버리지](../concepts/training-data-coverage.md) — 사용 범위를 덮는 분포와 Llama 3의
  배합
- [훈련 데이터 수량](../concepts/training-data-quantity.md) — 얼마나 필요한가, 골화와 수확 체감

## 확보와 주석

- [데이터 확보와 주석](../concepts/data-acquisition-and-annotation.md) — 공개 데이터셋과 주석 작업의
  실무

## 합성

- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 왜 만들어 내는가
- [전통적 데이터 합성](../concepts/traditional-data-synthesis.md) — 규칙 기반, 변환, 섭동, 시뮬레이션
- [AI 기반 데이터 합성](../concepts/ai-powered-data-synthesis.md) — 자가 대국, 역번역, 지시 데이터
  합성 파이프라인
- [합성 데이터 검증](../concepts/synthetic-data-verification.md) — 만들어 낸 데이터를 믿을 수 있게
  하는 절차
- [AI 생성 데이터의 한계](../concepts/limitations-of-ai-generated-data.md) — 네 가지 한계와 모델
  붕괴 논쟁
- [모델 증류](../concepts/model-distillation.md) — 큰 모델의 행동을 작은 모델로 옮기기

## 처리

- [훈련 데이터 처리](../concepts/training-data-processing.md) — 점검부터 시작하는 처리 단계
- [훈련 데이터 중복 제거](../concepts/training-data-deduplication.md) — 왜, 무엇을, 어떻게 지우는가
- [훈련 데이터 정제와 형식](../concepts/training-data-cleaning-and-formatting.md) — 정제, 토큰화 전
  마지막 손질

## 다른 축에서 여기로 이어지는 자리

- [모델 개발 층](../concepts/ai-model-development-layer.md) — 스택에서 데이터셋 엔지니어링이 이름을
  얻은 자리
- [지도 파인 튜닝](../concepts/supervised-finetuning.md) — 시연 데이터가 소비되는 쪽
- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 모델 제작자 관점의 사전 훈련 데이터
- [배치 처리의 유스케이스](../concepts/batch-use-cases.md) — 이 축의 처리 단계가 배치 잡으로 도는 쪽
- [수명 주기의 변환 단계](../concepts/transformation-in-the-lifecycle.md) — 파이프라인 일반론이 이
  축과 갈리는 경계

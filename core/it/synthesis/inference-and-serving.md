---
type: synthesis
title: 추론과 서빙
description: 같은 모델을 어떻게 빠르고 싸게 서빙하는가 — 병목의 분류와 지연·처리량 지표, AI 가속기, 모델 수준 최적화(압축·디코딩·KV 캐시·커널), 서비스 수준 최적화(배칭·분리·캐싱·병렬화)
generated: { by: "claude-fable-5", at: "2026-08-17T09:00:00Z" }
---

# 추론과 서빙

축은 하나다 — **가중치는 그대로 두고, 같은 모델을 더 빠르고 싸게 내보내는 일.** 병목이
컴퓨트인지 메모리 대역폭인지가 기법 선택을 가르고, 최적화는 모델·하드웨어·서비스의 세
수준에서 갈라진다는 것이 이 축의 요지다.

## 틀과 병목

- [추론 최적화의 세 수준](../concepts/inference-optimization-levels.md) — 모델·하드웨어·서비스
  수준과 기법 선택 지침
- [추론 서버와 병목](../concepts/inference-server-and-bottlenecks.md) — 컴퓨트 바운드와 메모리
  대역폭 바운드, 프리필과 디코드
- [온라인과 배치 추론 API](../concepts/online-and-batch-inference-apis.md) — 지연을 사는 쪽과
  비용을 아끼는 쪽

## 지표

- [추론 지연 지표](../concepts/inference-latency-metrics.md) — TTFT·TPOT·총지연과 백분위
- [처리량과 이용률](../concepts/inference-throughput-and-utilization.md) — 처리량·비용·굿풋·MFU·MBU

## 하드웨어

- [AI 가속기](../concepts/ai-accelerators.md) — GPU와 추론 전용 칩, 컴퓨트 프리미티브, 메모리
  계층과 전력

## 모델 수준 최적화

- [모델 압축과 프루닝](../concepts/model-compression-and-pruning.md) — 압축 기법의 지형과 프루닝이
  덜 쓰이는 이유
- [자기회귀 디코딩 최적화](../concepts/autoregressive-decoding-optimization.md) — speculative
  decoding, 참조 기반 추론, 병렬 디코딩
- [KV 캐시와 어텐션 최적화](../concepts/kv-cache-and-attention-optimization.md) — KV 캐시 산식,
  PagedAttention, FlashAttention
- [커널과 컴파일러](../concepts/kernels-and-compilers.md) — 벡터화·융합·lowering

## 서비스 수준 최적화

- [추론 배칭](../concepts/inference-batching.md) — 정적·동적·연속 배칭
- [프리필 디코드 분리](../concepts/prefill-decode-decoupling.md) — 두 국면을 다른 인스턴스로
- [프롬프트 캐싱](../concepts/prompt-caching.md) — 겹치는 접두를 다시 계산하지 않기
- [추론 병렬화](../concepts/inference-parallelism.md) — 복제·텐서·파이프라인·컨텍스트·시퀀스

## 다른 축에서 여기로 이어지는 자리

- [모델 개발 층](../concepts/ai-model-development-layer.md) — 스택에서 추론 최적화가 이름을 얻은
  자리
- [양자화](../concepts/quantization.md) — 훈련 메모리 관점과 서빙 대역폭 관점이 만나는 자리
- [비용과 지연 평가](../concepts/cost-and-latency-criteria.md) — 4장이 이 축에 미뤄 둔 지연 지표의
  본가
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 프리필과 디코드가 처음 서술된 자리
- [페이지 캐시와 축출](../concepts/page-cache-and-eviction.md) — PagedAttention이 빌려 온 OS 기법의
  본가

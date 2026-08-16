---
type: concept
title: 프롬프트에 맥락 주기
description: 지시만으로는 안 되고 정보가 있어야 하는 자리 — 시험에 참고 자료를 주는 것과 같은 효과, 맥락이 환각을 완화하는 기제, 맥락을 모아 오는 일에 붙은 이름인 맥락 구성, 그리고 모델의 지식을 준 맥락으로만 가두는 것이 왜 어려운가
generated: { by: "claude-opus-5", at: "2026-08-16T17:30:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 프롬프트에 맥락 주기

- [참고 자료를 주는 것과 같다](#참고-자료를-주는-것과-같다)
- [맥락은 환각을 완화한다](#맥락은-환각을-완화한다)
- [맥락 구성](#맥락-구성)
- [모델의 지식을 맥락으로만 가두기](#모델의-지식을-맥락으로만-가두기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델에게 무엇을 하라고 말하는 것 말고, 무엇을 알려 주어야 하는가.**

## 참고 자료를 주는 것과 같다

- **참고 텍스트가 학생이 시험을 더 잘 보게 돕는 것처럼, 충분한 맥락(context)은 모델이 더 잘
  수행하도록 도울 수 있다. 모델이 어떤 논문에 대한 질문에 답하기를 원한다면, 그 논문을 맥락에 넣는
  것이 모델의 응답을 개선할 가능성이 높다** (5장, p.223).[^huyen2025]

## 맥락은 환각을 완화한다

- 기제 (5장, p.223):[^huyen2025]

  > Context can also mitigate hallucinations. If the model isn't provided with the necessary
  > information, it'll have to rely on its internal knowledge, which might be unreliable, causing it
  > to hallucinate.

  환각 자체의 두 가설은 [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md)이 담는다.

## 맥락 구성

- 두 길 — **모델에게 필요한 맥락을 제공하거나, 맥락을 모아 올 도구를 줄 수 있다. 주어진 질의에 필요한
  맥락을 모으는 과정을 맥락 구성(context construction)이라 부른다. 맥락 구성 도구에는 RAG
  파이프라인에서와 같은 데이터 검색과 웹 검색이 있다** (5장, p.224).[^huyen2025] 그 도구들은 6장의
  몫이다 (5장, p.224)[^huyen2025] — 두 갈래는
  [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md)과
  [에이전트란 무엇인가](../concepts/agents-defined.md)로 이어진다.

## 모델의 지식을 맥락으로만 가두기

- 왜 그러고 싶은가 — **많은 시나리오에서 모델이 응답에 제공된 맥락의 정보만 쓰는 것이 바람직하다.
  이는 특히 롤플레잉과 그 밖의 시뮬레이션에서 흔하다. 예컨대 모델이 게임 스카이림(Skyrim)의 인물을
  연기하기를 원한다면, 이 인물은 스카이림 세계만 알아야 하고 "네가 가장 좋아하는 스타벅스 메뉴는
  뭐야?" 같은 질문에는 답할 수 없어야 한다** (5장, p.224).[^huyen2025]
- 프롬프트로 하는 데까지 — **모델을 맥락으로만 제한하는 것은 까다롭다. "제공된 맥락만 써서
  답하라" 같은 명확한 지시가 답할 수 없어야 하는 질문의 예시와 함께라면 도움이 될 수 있다. 제공된
  말뭉치의 어디에서 답을 끌어왔는지 구체적으로 인용하라고 모델에게 지시할 수도 있다. 이 접근은
  맥락이 뒷받침하는 답만 생성하도록 모델을 밀어 줄 수 있다** (5장, p.224).[^huyen2025]
- 그러나 보장은 없다 — **모델이 모든 지시를 따르리라는 보장이 없으므로 프롬프팅만으로는 원하는
  결과를 신뢰할 만하게 내지 못할 수 있다. 자기 말뭉치로 모델을 파인 튜닝하는 것이 또 다른
  선택지이지만, 사전 훈련 데이터가 여전히 응답에 새어 나올 수 있다. 가장 안전한 방법은 허용된
  지식 말뭉치로만 모델을 훈련하는 것인데, 이는 대부분의 유스케이스에서 흔히 실현 가능하지 않다.
  게다가 그 말뭉치가 고품질 모델을 훈련하기에 너무 제한적일 수 있다** (5장, p.224).[^huyen2025]

## 이어지는 페이지

- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 맥락 구성의 첫째 패턴
- [에이전트란 무엇인가](../concepts/agents-defined.md) — 둘째 패턴, 그리고 맥락 구성을 넘어서는 쪽
- [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md) — 맥락에 넣을 수 있는
  양과 그 안의 위치 효과
- [명확하고 명시적인 지시](../concepts/clear-and-explicit-instructions.md) — 같은 절의 앞 관행
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 환각이 일어나는 이유
- [사실 일관성](../concepts/factual-consistency.md) — 맥락에 근거한 답인지 재는 자리
- [에이전트의 메모리](../concepts/agent-memory.md) — 컨텍스트를 단기 기억으로 다시 읽는 자리
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 검색으로 맥락을 모아 오는 쪽이
  기대는 색인
- [인컨텍스트 학습](../concepts/in-context-learning.md) — 컨텍스트라는 낱말의 다른 쓰임

[^huyen2025]: Huyen 2025, 5장 "Prompt Engineering" (책 pp.211–252). 이 페이지는 "Provide Sufficient
    Context" 절(pp.223–224)과 그 안의 상자 "How to Restrict a Model's Knowledge to Only Its
    Context"(p.224)를 담았다. 이 절에는 도판이 없다.

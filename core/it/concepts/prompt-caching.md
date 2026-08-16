---
type: concept
title: 프롬프트 캐싱
description: 프롬프트마다 겹치는 조각을 한 번만 처리하게 만드는 캐시 — 시스템 프롬프트와 긴 문서와 다중 턴 대화라는 세 쓰임, 하루 10억 개의 반복 입력 토큰을 아끼는 규모의 산수, 캐시 크기와 구현 비용이라는 대가, 그리고 모델 API가 붙인 할인율과 저장 요금
generated: { by: "claude-opus-5", at: "2026-08-17T08:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 프롬프트 캐싱

- [겹치는 조각을 한 번만 처리한다](#겹치는-조각을-한-번만-처리한다)
- [어디에 쓰이는가](#어디에-쓰이는가)
- [규모의 산수와 공짜가 아닌 대가](#규모의-산수와-공짜가-아닌-대가)
- [모델 API가 붙인 가격](#모델-api가-붙인-가격)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모든 질의가 같은 앞부분을 다시 처리해야 하는가.**

## 겹치는 조각을 한 번만 처리한다

- 정의 — **애플리케이션의 많은 프롬프트는 겹치는 텍스트 조각을 갖는다. 프롬프트 캐시(prompt cache)는
  재사용을 위해 이 겹치는 조각을 저장해, 그것을 한 번만 처리하면 되게 한다. 서로 다른 프롬프트에서 흔히
  겹치는 텍스트 조각은 시스템 프롬프트다. 프롬프트 캐시가 없으면 모델은 질의마다 시스템 프롬프트를
  처리해야 한다. 프롬프트 캐시가 있으면 시스템 프롬프트는 첫 질의에 딱 한 번만 처리되면 된다** (9장,
  p.443).[^huyen2025]
- 다른 이름들 — **프롬프트 캐시는 컨텍스트 캐시(context cache) 또는 프리픽스 캐시(prefix cache)라고도
  불린다** (9장, p.443).[^huyen2025]
  - 도판 설명 — **프롬프트 캐시가 있으면 서로 다른 프롬프트에서 겹치는 조각이 캐시되고 재사용될 수
    있다** (9장, p.443, Figure 9-17 설명).[^huyen2025] 도판은 프롬프트를 시스템 프롬프트·예시·과제
    셋으로 쪼개고 앞의 둘을 "질의 사이에 캐시되고 재사용되는" 부분으로 묶는다. 그 안에 인쇄된
    문자열은 이렇다 (9장, p.443, Figure 9-17):[^huyen2025]

    ```text
    Your task is to identify entities in a text.

    Text: "Brave New World is a dystopian novel written by Aldous Huxley, first published in 1932."
    Entities: Brave New World, Aldous Huxley

    Text: ${THE TEXT THAT YOU WANT TO EXTRACT ENTITIES FROM}
    Entities:
    ```

## 어디에 쓰이는가

- **프롬프트 캐싱은 긴 문서를 수반하는 질의에 유용하다. 예컨대 많은 사용자 질의가 같은 긴 문서(책이나
  코드베이스 같은)와 관련된다면, 이 긴 문서는 질의 사이의 재사용을 위해 캐시될 수 있다. 긴 대화에도
  유용한데, 거기서는 앞선 메시지의 처리가 캐시되어 미래 메시지를 예측할 때 재사용될 수 있다** (9장,
  p.443).[^huyen2025]

## 규모의 산수와 공짜가 아닌 대가

- **긴 시스템 프롬프트를 가진 애플리케이션에 프롬프트 캐싱은 지연과 비용을 둘 다 크게 줄일 수 있다.
  시스템 프롬프트가 1,000토큰이고 애플리케이션이 하루에 모델 API 호출 100만 건을 생성하면, 프롬프트
  캐시는 하루 대략 10억 개의 반복 입력 토큰을 처리하는 것을 아껴 줄 것이다! 그러나 이것이 전적으로
  공짜는 아니다. KV 캐시처럼 프롬프트 캐시 크기도 꽤 클 수 있고 메모리 공간을 차지할 수 있다. 이
  기능을 가진 모델 API를 쓰지 않는 한 프롬프트 캐싱을 구현하는 것은 상당한 공학적 노력을 요구할 수
  있다** (9장, p.444).[^huyen2025]

## 모델 API가 붙인 가격

- **Gim et al.이 2023년 11월에 도입한 이래 프롬프트 캐시는 모델 API에 빠르게 통합되었다. 집필 시점
  기준 구글 제미나이가 이 기능을 제공하는데, 캐시된 입력 토큰은 일반 입력 토큰에 비해 75% 할인을 받되
  캐시 저장에 추가 비용을 내야 한다(집필 시점 기준 100만 토큰당 시간당 $1.00). 앤트로픽은 최대 90%
  비용 절감(캐시된 컨텍스트가 길수록 절감이 크다)과 최대 75% 지연 감소를 약속하는 프롬프트 캐싱을
  제공한다** (9장, p.444).[^huyen2025]
  - 각주가 붙인 단서 — **llama.cpp에도 프롬프트 캐싱이 있지만 집필 시점 기준 그것은 전체 프롬프트만
    캐시하고 같은 채팅 세션의 질의에 대해서만 작동하는 것으로 보인다. 문서가 제한적이지만 코드를 읽고
    저자가 짐작하기로는 긴 대화에서 그것이 이전 메시지를 캐시하고 가장 새로운 메시지만 처리한다** (9장,
    p.444 각주 26).[^huyen2025]
- 시나리오별 효과다. 원문 표기를 그대로 옮겼다 (9장, p.444, Table 9-3 — 앤트로픽(2024)의
  정보):[^huyen2025]

  | Use case | Latency w/o caching (time to first token) | Latency with caching (time to first token) | Cost reduction |
  |---|---|---|---|
  | Chat with a book (100,000-token cached prompt) | 11.5 s | 2.4 s (−79%) | −90% |
  | Many-shot prompting (10,000-token prompt) | 1.6 s | 1.1 s (−31%) | −86% |
  | Multi-turn conversation (10-turn convo with a long system prompt) | ~10 s | ~2.5 s (−75%) | −53% |

## 이어지는 페이지

- [시스템 프롬프트와 사용자 프롬프트](../concepts/system-prompt-and-user-prompt.md) — 캐시되는 그
  조각이 무엇인가
- [프롬프트에 맥락 주기](../concepts/providing-context-in-prompts.md) — 예시와 문서가 프롬프트에
  들어가는 자리
- [인컨텍스트 학습](../concepts/in-context-learning.md) — many-shot 프롬프팅이 무엇인가
- [언제 파인 튜닝하는가](../concepts/when-to-finetune.md) — 프롬프트 캐싱이 파인 튜닝의 이점 하나를
  지운 자리
- [KV 캐시와 어텐션 최적화](../concepts/kv-cache-and-attention-optimization.md) — 같은 메모리를 두고
  다투는 다른 캐시
- [추론 성능의 지연 지표](../concepts/inference-latency-metrics.md) — 표가 재는 것이 TTFT라는 사실
- [온라인 API와 배치 API](../concepts/online-and-batch-inference-apis.md) — 시스템 프롬프트를 미리
  안다는 사실이 미리 계산의 예외가 되는 자리
- [에이전트의 메모리](../concepts/agent-memory.md) — 긴 대화의 앞부분을 어떻게 다룰 것인가의 다른 답
- [추론 최적화의 세 수준](../concepts/inference-optimization-levels.md) — 요약이 이 기법을 가장
  영향이 큰 축에 놓는 자리

[^huyen2025]: Huyen 2025, 9장 "Inference Optimization" (책 pp.405–448). 이 페이지는 "Inference
    Service Optimization" 절의 하위 절 "Prompt caching"(pp.443–444)을 담았다. Table 9-3(p.444)은
    원문 표기를 그대로 옮겼다. Figure 9-17(프롬프트 캐시 도식, p.443)은 상자 구조를 옮기지 않고 그
    안에 인쇄된 문자열만 담았다 — 시스템 프롬프트의 생략 부호(`...`)는 원문에 그렇게 인쇄된 것이라
    옮기지 않았다. Gim et al.(2023)·구글 제미나이·앤트로픽(2024)·llama.cpp는 huyen2025를 통한
    전언이고, 가격과 할인율은 집필 시점 기준 진술이다.

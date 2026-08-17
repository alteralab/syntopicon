---
type: concept
title: 검색 증강 생성(RAG)
description: 모델이 갖지 못한 정보를 외부 기억에서 꺼내 맥락에 붙이는 패턴 — 위키백과를 읽어 답하던 retrieve-then-generate에서 검색기를 마스크드 LM 사전 훈련에 잠재변수로 넣은 선행을 거쳐 RAG라는 이름이 주조되기까지의 계보, 컨텍스트가 길어져도 RAG가 끝나지 않는 두 이유와 앤트로픽이 제시한 문턱, 검색기와 생성기 두 부품으로 된 기본 구조 안의 색인·질의·청킹, 원전이 파라메트릭 기억과 비파라메트릭 기억으로 세운 두 정식화(RAG-Sequence·RAG-Token)와 그 실측, 구절을 인코더에서 따로 처리하고 디코더에서 합쳐 문서 수에 선형으로 확장한 직계 후속, 검색을 탈지 말지를 특수 토큰으로 모델이 스스로 정하게 만든 적응형 검색(결정 시점의 세 갈래 비교는 적응형 검색 전략 페이지가 담는다), 그리고 전역 질문 앞에서 이 패턴 전체가 실패한다는 미심사 진단
generated: { by: "claude-opus-5", at: "2026-08-17T16:40:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: lewis2020-rag, resource: /it/sources/lewis2020-rag.md }
  - { id: guu2020-realm, resource: /it/sources/guu2020-realm.md }
  - { id: izacard2021-fid, resource: /it/sources/izacard2021-fid.md }
  - { id: asai2024-selfrag, resource: /it/sources/asai2024-selfrag.md }
  - { id: edge2024-graphrag, resource: /it/sources/edge2024-graphrag.md }
---

# 검색 증강 생성(RAG)

- [지시와 정보는 다른 것이다](#지시와-정보는-다른-것이다)
- [RAG란 무엇인가](#rag란-무엇인가)
- [계보 — 위키백과를 읽어 답하기](#계보--위키백과를-읽어-답하기)
- [원전이 자기를 정의한 문장](#원전이-자기를-정의한-문장)
- [질의마다 다른 맥락](#질의마다-다른-맥락)
- [긴 컨텍스트가 RAG를 끝내는가](#긴-컨텍스트가-rag를-끝내는가)
- [RAG 아키텍처](#rag-아키텍처)
- [파라메트릭 기억과 비파라메트릭 기억](#파라메트릭-기억과-비파라메트릭-기억)
- [RAG-Sequence와 RAG-Token](#rag-sequence와-rag-token)
- [문서와 청크](#문서와-청크)
- [원전의 실측](#원전의-실측)
- [색인을 갈아 끼우기](#색인을-갈아-끼우기)
- [원전이 밝힌 조건과 한계](#원전이-밝힌-조건과-한계)
- [계보의 다음 걸음 — Fusion-in-Decoder](#계보의-다음-걸음--fusion-in-decoder)
- [FiD가 잰 것](#fid가-잰-것)
- [질의마다 검색을 탈지 정하기 — Self-RAG](#질의마다-검색을-탈지-정하기--self-rag)
- [반성 토큰 네 종류](#반성-토큰-네-종류)
- [추론 시점에 행동을 바꾸는 손잡이](#추론-시점에-행동을-바꾸는-손잡이)
- [Self-RAG가 잰 것과 그 절제 실험](#self-rag가-잰-것과-그-절제-실험)
- [이 패턴이 못 하는 질문](#이-패턴이-못-하는-질문)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델이 알지 못하는 정보를 질의마다 어떻게 조달해 맥락에 넣는가.**

## 지시와 정보는 다른 것이다

- 장의 전제 (6장, p.253):[^huyen2025]

  > To solve a task, a model needs both the instructions on how to do it, and the necessary
  > information to do so.

- 왜 갈라 다루는가 — **사람이 정보가 없을 때 틀린 답을 낼 가능성이 높은 것과 꼭 같이, AI 모델도
  맥락이 없을 때 실수하고 환각할 가능성이 높다. 주어진 애플리케이션에서 모델의 지시는 모든 질의에
  공통이지만 맥락은 질의마다 특유하다. 앞 장이 모델에게 좋은 지시를 쓰는 법을 다뤘다면 이 장은
  질의마다 관련 맥락을 구성하는 법에 집중한다** (6장, p.253).[^huyen2025] 그 앞 장의 몫은
  [프롬프트에 맥락 주기](../concepts/providing-context-in-prompts.md)에 있다.
- 맥락 구성의 두 지배적 패턴 — **맥락 구성의 두 지배적 패턴은 RAG(검색 증강 생성)와 에이전트다.
  RAG 패턴은 모델이 외부 데이터 소스에서 관련 정보를 검색할 수 있게 하고, 에이전트 패턴은 모델이
  웹 검색이나 뉴스 API 같은 도구를 써서 정보를 모을 수 있게 한다** (6장, p.253).[^huyen2025]
- 두 패턴의 범위가 다르다 — **RAG 패턴이 주로 맥락 구성에 쓰이는 반면, 에이전트 패턴은 그보다
  훨씬 많은 것을 할 수 있다. 외부 도구는 모델이 자기 단점을 다루고 능력을 확장하도록 도울 수
  있다. 가장 중요하게는, 도구가 모델에게 세계와 직접 상호작용하는 능력을 주어 우리 삶의 많은
  국면을 자동화할 수 있게 한다** (6장, p.253).[^huyen2025]

## RAG란 무엇인가

- 정의 (6장, p.253):[^huyen2025]

  > RAG is a technique that enhances a model's generation by retrieving the relevant information
  > from external memory sources.

- 외부 기억이 무엇일 수 있는가 — **외부 기억 소스는 내부 데이터베이스일 수도, 사용자의 이전 채팅
  세션일 수도, 인터넷일 수도 있다** (6장, p.253).[^huyen2025]

## 계보 — 위키백과를 읽어 답하기

- 첫 도입 — **retrieve-then-generate 패턴은 "Reading Wikipedia to Answer Open-Domain
  Questions"(Chen et al., 2017)에서 처음 소개되었다. 이 작업에서 시스템은 먼저 질문에 가장 관련
  있는 위키백과 페이지 다섯 개를 검색하고, 그다음 모델이 이 페이지들의 정보를 써서 — 또는 읽어서 —
  답을 생성한다** (6장, p.254, Figure 6-1).[^huyen2025]
  - 각주가 밝히는 그 시절의 모델 — **쓰인 모델은 LSTM(Long Short-Term Memory)으로 알려진 순환
    신경망(recurrent neural network)의 한 종류였다. LSTM은 2018년 트랜스포머 구조가 넘겨받기 전까지
    자연어 처리(NLP)를 위한 딥러닝의 지배적 구조였다** (6장, p.254 각주 1).[^huyen2025]
  - 도판 설명이 붙이는 이름 — **그 모델은 문서 판독기(document reader)라고 불렸다** (6장, p.254,
    Figure 6-1 설명).[^huyen2025]
- 이름이 주조된 자리 — **검색 증강 생성(retrieval-augmented generation)이라는 용어는
  "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"(Lewis et al., 2020)에서
  주조되었다. 이 논문은 가용한 지식 전부를 모델에 직접 입력할 수 없는 지식 집약적 과제의 해법으로
  RAG를 제안했다. RAG로는 검색기가 판정한 대로 질의에 가장 관련 있는 정보만 검색되어 모델에
  입력된다. Lewis et al.은 관련 정보에 접근할 수 있는 것이 모델이 환각을 줄이면서 더 상세한 응답을
  생성하도록 도울 수 있음을 발견했다** (6장, p.254).[^huyen2025][^lewis2020-rag]
  - 각주가 붙인 같은 무렵의 다른 논문 — **비슷한 시기에 역시 페이스북에서 나온 또 다른 논문
    "How Context Affects Language Models' Factual Predictions"(Petroni et al., arXiv, 2020년 5월)는
    사전 훈련된 언어 모델을 검색 시스템으로 증강하는 것이 사실 질문에 대한 모델의 성능을 극적으로
    개선할 수 있음을 보였다** (6장, p.254 각주 2).[^huyen2025]
- 원전이 자기 앞에 놓은 선행 — **하이브리드 모델은 지식을 직접 개정·확장할 수 있고 접근된 지식을
  검사·해석할 수 있어 파라메트릭 모델의 문제 일부를 다룰 수 있다. 마스크 언어 모델과 미분 가능한
  검색기를 결합한 REALM과 ORQA가 유망한 결과를 보였으나 개방 도메인 추출형 질의응답만 탐색했다.
  이 논문은 그 하이브리드 기억을 "NLP의 짐말"인 seq2seq 모델로 가져온다** (1절, p.1).[^lewis2020-rag]
  ORQA·BERT·BART는 아직 이 KB에 반입되지 않은 원전들의 자리다.
- 그 선행이 자기를 세운 자리 — **지식을 더 모듈적이고 해석 가능한 방식으로 붙잡기 위해, 우리는 언어
  모델 사전 훈련을 잠재 지식 검색기(latent knowledge retriever)로 증강해 모델이 위키백과 같은 큰
  코퍼스에서 문서를 검색하고 그것에 어텐션할 수 있게 한다 — 사전 훈련·파인 튜닝·추론 전부에서
  쓰인다. 그런 지식 검색기를 비지도 방식으로, 곧 마스크드 언어 모델링을 학습 신호로 삼고 수백만
  문서를 고려하는 검색 단계를 통해 역전파해 사전 훈련하는 법을 우리가 처음으로 보인다** (초록,
  p.1).[^guu2020-realm] 곧 위 원전이 자기를 **범용 파인 튜닝 처방**으로 규정한 자리에서 (초록,
  p.1),[^lewis2020-rag] 이 선행은 검색기를 **사전 훈련 단계**에 넣는다 — 발표 순서로도 이쪽이 앞선다.
- 검색기를 무엇으로 가르치는가 — **REALM의 핵심 직관은 비지도 텍스트에서 오는 성능 기반
  (performance-based) 신호로 검색기를 훈련하는 것이다. 언어 모델의 퍼플렉시티를 *개선하는* 검색은
  도움이 되므로 보상받아야 하고, 정보를 주지 않는 검색은 벌받아야 한다. 우리는 이
  retrieve-then-predict 접근을 잠재변수 언어 모델로 모형화하고 주변 우도를 최적화함으로써 이 행동을
  얻는다** (1절, p.2).[^guu2020-realm] 잠재 문서를 주변화하는 이 형식이 위 원전의
  [RAG-Sequence와 RAG-Token](#rag-sequence와-rag-token)이 물려받는 틀이며, 그 원전도 자기 형식을
  **검색된 문서를 잠재변수로 다룬다**로 적는다 (2절, p.3).[^lewis2020-rag]
- 그 형식이 부른 계산 문제와 답 — **각 사전 훈련 단계마다 검색기가 수백만 후보 문서를 고려해야 하고
  그 결정을 통해 역전파해야 하므로, 대규모 신경 검색 모듈을 사전 훈련에 넣는 것은 유의미한 계산
  난점을 이룬다. 이를 다루려고 문서마다 수행되는 계산을 캐시하고 비동기로 갱신할 수 있도록 검색기를
  구조화하며, 최선 문서의 선택은 최대 내적 탐색(MIPS)으로 정식화할 수 있다** (1절,
  p.2).[^guu2020-realm] 실물로는 **수백 훈련 단계마다 모든 문서를 비동기로 다시 임베딩하고 다시
  색인하며**, 갱신 사이의 낡은 색인은 **상위 `k`개를 고르는 데만 쓰이고 검색된 뒤에는 최신 파라미터로
  확률과 기울기를 다시 계산한다** (3.3절, p.4).[^guu2020-realm]
  - 그것이 얼마나 결정적인가 — 갱신은 **약 500 훈련 단계마다 한 번** 일어나며, 속도를 30배 늦추면
    **NQ 개발 집합 정확 일치가 38.2에서 28.7로, 영샷 검색 Recall@5가 38.5에서 15.1로 떨어진다**
    (4.5절, p.7, Table 2; p.8).[^guu2020-realm] 곧 위 원전이 문서 인코더를 **얼린** 이유로 든 "색인을
    주기적으로 다시 만들어야 해서 비용이 크다"가 이 자리의 실측이며 (2.4절,
    p.4),[^lewis2020-rag] 이 선행 자신도 파인 튜닝에서는 색인을 한 번만 짓고 문서 인코더를 갱신하지
    않는다 (3.3절, p.5 각주 3).[^guu2020-realm]
  - 사전 훈련 신호를 고르는 두 손질 — **세계 지식을 요구하는 예시에 집중하려고 "United Kingdom"이나
    "July 1969" 같은 두드러진 구간(salient span)을 가리고**, 검색이 필요 없을 때 신뢰를 흘려보낼
    자리로 **빈 널 문서(null document)를 상위 `k`개에 더한다** (3.4절, p.5).[^guu2020-realm] 가리기를
    무작위 토큰·무작위 구간으로 바꾸면 정확 일치가 38.2에서 각각 32.3·35.3으로 내려간다 (4.5절,
    p.7, Table 2).[^guu2020-realm]
- 두 원전이 서로를 놓는 자리가 어긋난다 — 위 원전의 5절은 REALM을 **질의응답 같은 특정 하류 과제를
  돕도록 검색 모듈을 최적화하는** 계열로 묶고, 그 계열이 **단일 과제에서 강한 성능을 얻는** 반면
  자기들은 **하나의 검색 기반 구조를 여러 과제에 파인 튜닝할 수 있음을 보인다**고 적는다 (5절,
  p.9).[^lewis2020-rag] 반면 이 선행은 자기 검색기를 **다른 과제로 전이되도록 설계된** 것으로 적고
  (1절, p.2), 결론에서 **여기 제시한 것은 REALM류 접근 가족의 최소 구현**이라고 적는다 (6절,
  p.9).[^guu2020-realm] 두 진술은 같은 작업에 대한 서로 다른 위치 부여이며 어느 쪽이 맞는지 두 논문
  안에서 판정되지 않으므로 함께 남긴다.
  - 실측이 겹치는 자리 — 이 선행이 보고한 NQ 정확 일치 **40.4**(사전 훈련 코퍼스 CC-News, 지식
    코퍼스 위키백과, 파라미터 330m)는 (4.4절, p.7, Table 1)[^guu2020-realm] 아래
    [원전의 실측](#원전의-실측)에서 옮긴 위 원전 표의 REALM 값과 같은 수치다 (4.1절, pp.5–6,
    Table 1).[^lewis2020-rag]
    저자들은 **REALM이 30배 작으면서 가장 큰 T5-11B 모델(34.5)을 앞선다**고 요약하되, **T5가 사전
    훈련 중 SQuAD 독해 데이터 10만 건 이상에 추가로 접근하며 그런 데이터가 REALM에도 도움이 될 수
    있으나 우리 실험에서는 쓰지 않았다**는 단서를 붙인다 (4.4절, p.7).[^guu2020-realm]

## 원전이 자기를 정의한 문장

- 원전의 정의다. 초록의 표기를 그대로 옮겼다 (초록, p.1):[^lewis2020-rag]

  > We explore a general-purpose fine-tuning recipe for retrieval-augmented generation (RAG) —
  > models which combine pre-trained parametric and non-parametric memory for language generation.

- 무엇을 파라메트릭·비파라메트릭으로 잡았는가 (초록, p.1):[^lewis2020-rag]

  > We introduce RAG models where the parametric memory is a pre-trained seq2seq model and the
  > non-parametric memory is a dense vector index of Wikipedia, accessed with a pre-trained neural
  > retriever.

- 원전이 푼 문제의 진술 — **큰 사전 훈련 언어 모델이 사실 지식을 자기 파라미터에 저장한다는 것은
  이미 밝혀졌지만, 그 지식에 접근하고 그것을 정확히 조작하는 능력은 여전히 제한적이다. 또한 자기
  결정의 출처를 대는 것과 세계 지식을 갱신하는 것은 열린 연구 문제로 남아 있다** (초록,
  p.1).[^lewis2020-rag] 그래서 원전이 파라메트릭 모델의 단점으로 든 것은 셋이다 — **기억을 쉽게
  확장하거나 개정할 수 없고, 자기 예측에 대한 통찰을 직설적으로 제공할 수 없으며, 환각을 생성할 수
  있다** (1절, p.1).[^lewis2020-rag]
- 지식 집약적 과제의 정의다 (1절, p.2):[^lewis2020-rag]

  > *knowledge-intensive tasks*—tasks that humans could not reasonably be expected to perform
  > without access to an external knowledge source.

## 질의마다 다른 맥락

- 저자가 든 예 — **질의 "Can Acme's fancy-printer-A300 print 100pps?"가 주어지면, 모델은
  fancy-printer-A300의 사양이 주어졌을 때 더 잘 응답할 수 있을 것이다** (6장,
  p.255).[^huyen2025] 각주는 이 예를 Chetan Tekur에게 돌린다 (6장, p.255 각주 3).[^huyen2025]
- 관점 — **RAG는 모든 질의에 같은 맥락을 쓰는 대신 질의마다 특유한 맥락을 구성하는 기법으로 생각할
  수 있다. 이는 사용자 데이터를 다루는 데 도움이 된다 — 어떤 사용자에 특유한 데이터를 그 사용자와
  관련된 질의에만 포함할 수 있게 하기 때문이다** (6장, p.255).[^huyen2025]
- 고전 ML과의 대응 (6장, p.255):[^huyen2025]

  > Context construction for foundation models is equivalent to feature engineering for classical
  > ML models. They serve the same purpose: giving the model the necessary information to process
  > an input.

## 긴 컨텍스트가 RAG를 끝내는가

- 논쟁의 배치 — **파운데이션 모델 초창기에 RAG는 가장 흔한 패턴 중 하나로 떠올랐다. 그 주된 목적은
  모델의 컨텍스트 한계를 극복하는 것이었다. 많은 사람이 충분히 긴 컨텍스트가 RAG의 끝일 것이라고
  생각한다. 저자는 그렇게 생각하지 않는다** (6장, p.255).[^huyen2025]
- 첫째 이유 — **모델의 컨텍스트 길이가 아무리 길어도 그보다 긴 컨텍스트를 요구하는 애플리케이션은
  있을 것이다. 결국 가용한 데이터의 양은 시간이 지나며 늘기만 한다. 사람들은 새 데이터를 생성해
  더하지만 데이터를 지우는 일은 드물다. 컨텍스트 길이는 빠르게 늘고 있지만 임의 애플리케이션의
  데이터 수요를 따라잡을 만큼 빠르지는 않다** (6장, p.255).[^huyen2025]
  - 각주가 붙인 유비 — **파킨슨의 법칙은 보통 "일은 그것을 완성하는 데 쓸 수 있는 시간을 채우도록
    늘어난다"로 표현된다. 저자는 애플리케이션의 컨텍스트가 자기가 쓰는 모델이 지원하는 컨텍스트
    한계를 채우도록 늘어난다는 비슷한 이론을 갖고 있다** (6장, p.255 각주 4).[^huyen2025]
- 둘째 이유 — **긴 컨텍스트를 처리할 수 있는 모델이 반드시 그 컨텍스트를 잘 쓰는 것은 아니다.
  컨텍스트가 길수록 모델이 컨텍스트의 틀린 부분에 집중할 가능성이 높다. 추가되는 모든 컨텍스트
  토큰은 추가 비용을 발생시키고 추가 지연을 더할 잠재력이 있다. RAG는 모델이 질의마다 가장 관련
  있는 정보만 쓰게 하여, 입력 토큰 수를 줄이면서 모델의 성능은 잠재적으로 높인다** (6장,
  p.255).[^huyen2025] 그 "컨텍스트를 잘 쓰지 못한다"의 실측은
  [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md)에 있다.
- 저자의 전망 — **컨텍스트 길이를 늘리려는 노력과 모델이 컨텍스트를 더 효과적으로 쓰게 하려는
  노력은 병행되고 있다. 저자는 어떤 모델 제공자가 모델이 컨텍스트에서 가장 두드러진 부분을 골라
  쓰도록 돕는 검색과 비슷하거나 어텐션과 비슷한 기전을 넣더라도 놀라지 않을 것이라고 말한다** (6장,
  p.255).[^huyen2025] #speculation
- 규모의 문턱을 명시한 지침 하나 — **앤트로픽은 클로드 모델에 대해 "지식 베이스가 200,000
  토큰(자료 약 500쪽)보다 작다면 RAG나 비슷한 방법 없이 모델에게 주는 프롬프트에 지식 베이스
  전체를 그냥 포함할 수 있다"고 제안했다(Anthropic, 2024). 저자는 다른 모델 개발자들도 자기 모델에
  대해 RAG 대 긴 컨텍스트에 관한 비슷한 지침을 제공한다면 놀라울 것이라고 적는다** (6장,
  p.256).[^huyen2025]

## RAG 아키텍처

- 두 부품 — **RAG 시스템은 두 구성 요소를 갖는다: 외부 기억 소스에서 정보를 검색하는 검색기(retriever)와
  검색된 정보에 근거해 응답을 생성하는 생성기(generator)다** (6장, p.256, Figure
  6-2).[^huyen2025] 원전도 같은 둘로 형식을 세운다 — **모델은 두 구성 요소를 활용한다: 질의 `x`가
  주어졌을 때 텍스트 구절 위의 (상위 K개로 잘린) 분포를 돌려주는 파라미터 `η`의 검색기
  `p_η(z|x)`와, 앞선 `i−1`개 토큰·원래 입력 `x`·검색된 구절 `z`의 맥락에 근거해 현재 토큰을
  생성하는 파라미터 `θ`의 생성기 `p_θ(y_i|x, z, y_1:i−1)`** (2절, p.2).[^lewis2020-rag]
- 훈련 방식이 바뀌었다 — **원래의 RAG 논문에서 Lewis et al.은 검색기와 생성 모델을 함께 훈련했다.
  오늘날의 RAG 시스템에서는 이 두 구성 요소가 흔히 따로 훈련되며, 많은 팀이 기성품 검색기와 모델로
  자기 RAG 시스템을 짓는다. 그러나 RAG 시스템 전체를 종단 간으로 파인 튜닝하는 것은 성능을 크게
  개선할 수 있다** (6장, p.256).[^huyen2025]
  - 원전이 실제로 얼린 것 — **검색기와 생성기는 어떤 문서를 검색해야 하는지에 대한 직접 지도 없이
    함께 훈련된다. 그러나 훈련 중 문서 인코더 `BERT_d`를 갱신하는 것은 REALM이 사전 훈련 중에
    그러듯 문서 색인을 주기적으로 다시 만들어야 해서 비용이 크다. 저자들은 강한 성능을 위해 이
    단계가 필요하다고 보지 않았고, 문서 인코더(와 색인)를 고정한 채 질의 인코더 `BERT_q`와 BART
    생성기만 파인 튜닝했다** (2.4절, p.4).[^lewis2020-rag] 곧 "함께 훈련했다"의 실제 범위는
    질의 인코더와 생성기이며, 문서 쪽 인코더와 색인은 사전 훈련된 채로 얼어 있다.
- 검색기가 성패를 가른다 — **RAG 시스템의 성공은 자기 검색기의 품질에 달려 있다. 검색기는 두 가지
  주요 기능을 갖는다: 색인(indexing)과 질의(querying). 색인은 나중에 빨리 검색될 수 있도록 데이터를
  처리하는 것을 수반한다. 어떤 질의에 관련된 데이터를 검색하려고 질의를 보내는 것을 질의라 한다.
  데이터를 어떻게 색인하는가는 나중에 그것을 어떻게 검색하고자 하는가에 달려 있다** (6장,
  p.256).[^huyen2025]

## 파라메트릭 기억과 비파라메트릭 기억

- 검색기의 실물 — **검색 구성 요소 `p_η(z|x)`는 DPR에 기반한다. DPR은 바이 인코더(bi-encoder)
  구조를 따라 `p_η(z|x) ∝ exp(d(z)ᵀq(x))`로 두는데, `d(z) = BERT_d(z)`는 BERT-base 문서
  인코더가 만든 문서의 조밀 표현이고 `q(x) = BERT_q(x)`는 역시 BERT-base에 기반한 질의 인코더가
  만든 질의 표현이다. 상위 `k`개 문서를 구하는 것은 최대 내적 탐색(Maximum Inner Product Search,
  MIPS) 문제이며 준선형 시간에 근사적으로 풀 수 있다** (2.2절, p.3).[^lewis2020-rag] 그 검색기의
  원전은 [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)에 있다.
- 생성기의 실물 — **생성기 구성 요소는 어떤 인코더–디코더로도 모델링될 수 있다. 저자들은 4억
  파라미터의 사전 훈련된 seq2seq 트랜스포머 BART-large를 쓴다. 생성 시 입력 `x`와 검색된 내용
  `z`를 결합하는 방법은 단순히 이어 붙이는 것이다** (2.3절, p.3).[^lewis2020-rag]
- 이름 붙이기 — **저자들은 문서 색인을 비파라메트릭 기억(non-parametric memory)이라 부르고, BART
  생성기의 파라미터 `θ`를 파라메트릭 기억(parametric memory)이라 부른다** (2.2–2.3절,
  p.3).[^lewis2020-rag]
- 왜 이 조합이 새로운가 — **비파라메트릭 기억으로 시스템을 풍부하게 하는 앞선 작업(메모리 네트워크·
  스택 증강 네트워크·메모리 층)은 특정 과제를 위해 처음부터 훈련되었다. 이와 달리 이 작업은
  파라메트릭·비파라메트릭 기억 구성 요소 양쪽이 사전 훈련되고 광범위한 지식이 미리 적재된 설정을
  탐구한다. 결정적으로, 사전 훈련된 접근 기전을 씀으로써 지식에 접근하는 능력이 추가 훈련 없이
  존재한다** (1절, p.2).[^lewis2020-rag]
- 이 기억이 사람이 읽고 쓸 수 있다는 점 — **이 기억의 핵심 특징은 분산 표현이 아니라 원 텍스트로
  이뤄져 있다는 것이며, 이는 기억을 (i) 사람이 읽을 수 있게 하여 모델에 일종의 해석 가능성을 주고
  (ii) 사람이 쓸 수 있게 하여 문서 색인을 편집함으로써 모델의 기억을 동적으로 갱신할 수 있게
  한다** (5절, p.9).[^lewis2020-rag]

## RAG-Sequence와 RAG-Token

- 잠재변수로 두는 발상 — **검색기와 생성기를 종단 간으로 훈련하려고 검색된 문서를 잠재변수로
  다룬다. 생성 텍스트 위의 분포를 만들기 위해 잠재 문서를 서로 다른 방식으로 주변화하는 두 모델을
  제안한다** (2절, p.3).[^lewis2020-rag]
- 두 정식화의 원 정의다 (2.1절, p.3):[^lewis2020-rag]
  - **RAG-Sequence** — **The RAG-Sequence model uses the same retrieved document to generate the
    complete *sequence*.** 기술적으로는 검색된 문서를 상위 K 근사로 주변화되는 하나의 잠재변수로
    다룬다. 상위 K개 문서를 검색하고, 생성기가 문서마다 출력 시퀀스 확률을 만든 다음 주변화한다.
  - **RAG-Token** — **In the RAG-Token model we can draw a different latent document for each
    target *token* and marginalize accordingly.** 이는 생성기가 답을 만들 때 여러 문서에서 내용을
    골라 쓸 수 있게 한다. 상위 K개 문서를 검색한 뒤 문서마다 다음 출력 토큰의 분포를 만들고
    주변화하며, 이 과정을 다음 토큰에 대해 반복한다.
- 분류 과제에서는 둘이 같다 — **목표 클래스를 길이 1의 목표 시퀀스로 여기면 RAG를 시퀀스 분류
  과제에 쓸 수 있으며, 이 경우 RAG-Sequence와 RAG-Token은 등가다** (2.1절, p.3).[^lewis2020-rag]
- 디코딩이 갈린다 — **시험 시점에 두 모델은 `arg max_y p(y|x)`를 근사하는 방식이 다르다.
  RAG-Token은 전이 확률을 표준 빔 디코더에 꽂아 넣으면 되는 표준 자기회귀 seq2seq 생성기로 볼 수
  있다. 반면 RAG-Sequence의 우도는 관습적인 토큰별 우도로 쪼개지지 않으므로 단일 빔 탐색으로 풀 수
  없고, 문서마다 빔 탐색을 돌려 가설 집합 `Y`를 얻는다** (2.5절, p.4).[^lewis2020-rag]
  - 두 디코딩의 이름 — **어떤 가설 `y`가 모든 문서의 빔에 나타나지는 않으므로, `y`가 빔에 없는
    문서마다 추가 순전파를 돌려 확률을 추정하고 생성기 확률에 `p_η(z|x)`를 곱해 빔에 걸쳐 합산하는
    절차를 "Thorough Decoding"이라 부른다. 출력 시퀀스가 길어 `|Y|`가 커지면 순전파가 많이
    필요하므로, 빔 탐색에서 생성되지 않은 `y`에 대해 `p_θ(y|x, z_i) ≈ 0`으로 두는 추가 근사를 쓸 수
    있고 이를 "Fast Decoding"이라 부른다** (2.5절, p.4).[^lewis2020-rag]
- 두 정식화가 갈리는 실측 자리 — **RAG-Token이 Jeopardy 질문 생성에서 RAG-Sequence보다 낫다.
  Jeopardy 질문은 흔히 별개의 정보 두 조각을 담는데, RAG-Token은 여러 문서의 내용을 결합한 응답을
  생성할 수 있기 때문일 것이다. 입력 "Hemingway"에 대해 "A Farewell to Arms"를 생성할 때는 문서 1의
  사후확률이 높고 "The Sun Also Rises"를 생성할 때는 문서 2의 사후확률이 높다. 흥미롭게도 각 책의
  첫 토큰이 생성된 뒤에는 문서 사후확률이 평평해지는데, 이는 생성기가 특정 문서에 의존하지 않고
  제목을 완성할 수 있음을, 곧 모델의 파라메트릭 지식이 제목을 완성하기에 충분함을 시사한다**
  (4.3절, pp.6–7, Figure 2).[^lewis2020-rag]

## 문서와 청크

- 왜 통째로 검색하지 않는가 — **문서는 10 토큰일 수도 100만 토큰일 수도 있다. 문서 전체를 순진하게
  검색하면 컨텍스트가 임의로 길어질 수 있다. 이를 피하려고 각 문서를 더 다루기 쉬운 청크로 쪼갤 수
  있다** (6장, p.257).[^huyen2025]
- 원전이 실제로 쓴 청크 크기 — **모든 실험에서 비파라메트릭 지식 소스로 단일 위키백과 덤프
  (2018년 12월)를 쓴다. 위키백과 문서마다 서로 겹치지 않는 100낱말 청크로 쪼개 총 2,100만 개
  문서를 만든다. 문서 인코더로 문서마다 임베딩을 계산하고 FAISS로 단일 MIPS 색인을 만들되 빠른
  검색을 위해 계층적 탐색 가능 소세계(HNSW) 근사를 쓴다** (3절, p.4).[^lewis2020-rag]
  그 색인 구조는 [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.
- 그 뒤의 흐름 — **질의마다 우리의 목표는 그 질의에 가장 관련 있는 데이터 청크를 검색하는 것이다.
  검색된 데이터 청크를 사용자 프롬프트와 이어 붙여 최종 프롬프트를 만드는 데는 흔히 소소한 후처리가
  필요하다. 이 최종 프롬프트가 생성 모델에 먹여진다** (6장, p.257).[^huyen2025]
- 용어 사용에 대한 저자의 단서 — **저자는 이 장에서 "문서"라는 용어를 "문서"와 "청크" 양쪽을 가리키는
  데 쓴다. 엄밀히 말해 문서의 청크도 하나의 문서이기 때문이다. 이는 이 책의 용어를 고전 NLP·정보
  검색(IR) 용어와 일관되게 유지하기 위한 것이다** (6장, p.257).[^huyen2025]

## 원전의 실측

- 개방 도메인 질의응답 — **네 개의 개방 도메인 QA 과제 전부에서 RAG가 새 최고 성능을 세운다.
  Natural Questions 정확 일치(EM) 기준으로 RAG-Sequence 44.5·RAG-Token 44.1이며, 같은 표의
  DPR은 41.5, REALM은 40.4, T5-11B+SSM은 36.6이다. RAG는 REALM·T5+SSM과 달리 비싸고 특화된
  "salient span masking" 사전 훈련 없이 강한 결과를 얻는다** (4.1절, pp.5–6,
  Table 1).[^lewis2020-rag]
- 추출형이 못 하는 것을 생성형이 한다 — **답을 추출할 수 있을 때조차 답을 생성하는 데는 여러 이점이
  있다. 답에 대한 단서를 담지만 답을 그대로 담지는 않은 문서도 정답 생성에 기여할 수 있는데 이는
  표준 추출형 접근으로는 불가능하다. 나아가 RAG는 정답이 검색된 어떤 문서에도 없을 때조차 정답을
  생성할 수 있으며, NQ에서 그런 경우 11.8%의 정확도를 달성한다 — 추출 모델이라면 0%일 자리다**
  (4.1절, pp.5–6).[^lewis2020-rag]
- 사람이 평가한 사실성과 구체성 — **BART와 RAG-Token의 생성 452쌍에 대한 사람 평가에서 평가자들은
  BART가 RAG보다 더 사실적이라고 답한 경우가 7.1%인 반면 RAG가 더 사실적이라고 답한 경우는
  42.7%였다. 구체성에서도 BART 16.8% 대 RAG 37.4%로 RAG가 큰 차이로 앞선다** (4.3절, p.6,
  Table 4).[^lewis2020-rag] huyen2025가 전언으로 옮긴 "환각을 줄이면서 더 상세한 응답"의 실측이 이
  표다.
  - **원문 안에서 수치가 어긋나는 자리 하나** — 본문 산문은 **양쪽 다 사실적인 경우가 추가로 17%**
    라고 적지만, Table 4의 해당 칸은 `Both good 11.7%`이고 `Both poor`가 17.7%다 (4.3절, p.6과
    p.8 Table 4).[^lewis2020-rag] 어느 쪽이 오식인지 논문 안에서 판정되지 않으므로 여기서는 두
    값을 함께 남기고 하나를 고르지 않는다.
- 다양성 — **서로 다른 모델이 생성한 전체 n-그램 대비 서로 다른 n-그램의 비율로 다양성을 재면
  RAG-Sequence의 생성이 RAG-Token보다 다양하고, 둘 다 다양성 촉진 디코딩 없이도 BART보다 유의미하게
  다양하다** (4.5절, p.7, Table 5).[^lewis2020-rag]
- 사실 검증 — **FEVER 3-way 분류에서 RAG 점수는 최고 성능 모델과 4.3% 이내인데, 그 모델들은
  중간 검색 지도로 훈련된 복잡한 파이프라인 시스템이며 RAG는 그 지도를 요구하지 않는다. 검색된
  문서와 금 증거 주석의 겹침을 보면 최상위 검색 문서가 금 문서인 경우가 71%, 상위 10개 안에 금
  문서가 있는 경우가 90%다** (4.4절, pp.6–7).[^lewis2020-rag]

## 색인을 갈아 끼우기

- 비파라메트릭 기억의 이점 — **RAG 같은 비파라메트릭 기억 모델의 이점 하나는 시험 시점에 지식을
  쉽게 갱신할 수 있다는 것이다. T5나 BART 같은 파라메트릭 전용 모델은 세계가 바뀔 때 자기 행동을
  갱신하려면 추가 훈련이 필요하다** (4.5절, p.7).[^lewis2020-rag]
- 실측 — **2016년 12월 위키백과 덤프로 색인을 짓고 2018년 12월 색인과 비교했다. 두 시점 사이에
  바뀐 세계 지도자 82명의 목록과 "Who is {position}?" 템플릿으로 질의하면, 2016년 색인으로 2016년
  지도자를 물었을 때 70%, 2018년 색인으로 2018년 지도자를 물었을 때 68%를 맞힌다. 색인이 어긋나면
  정확도는 낮다(2018년 색인에 2016년 지도자 12%, 2016년 색인에 2018년 지도자 4%). 이는 비파라메트릭
  기억을 교체하는 것만으로 RAG의 세계 지식을 갱신할 수 있음을 보인다** (4.5절,
  pp.7–8).[^lewis2020-rag]

## 원전이 밝힌 조건과 한계

- 검색 학습이 항상 이기지는 않는다 — **검색기를 얼린 절제 실험에서 학습된 검색이 모든 과제의 결과를
  개선한다. RAG의 조밀 검색기를 낱말 겹침 기반 BM25 검색기로 바꾸면, FEVER에서는 BM25가 가장 좋다 —
  FEVER의 주장이 개체 중심이라 낱말 겹침 기반 검색에 잘 맞기 때문일 것이다. 미분 가능한 검색은 다른
  모든 과제, 특히 결정적인 개방 도메인 QA의 결과를 개선한다** (4.5절, p.7,
  Table 6).[^lewis2020-rag] 어휘 갈래가 언제 이기는지는
  [어휘 기반 검색](../concepts/term-based-retrieval.md)에 있다.
- 문서를 더 검색하는 것의 효과가 두 모델에서 갈린다 — **모델은 잠재 문서 5개나 10개로 훈련되며 둘
  사이에 유의미한 성능 차이는 관측되지 않는다. 시험 시점에 더 많은 문서를 검색하면 RAG-Sequence의
  개방 도메인 QA 결과는 단조 증가하지만 RAG-Token은 검색 문서 10개에서 정점을 찍는다. MS-MARCO
  에서는 문서를 더 검색하면 RAG-Token의 Rouge-L이 오르는 대신 Bleu-1이 내려간다** (4.5절, p.8,
  Figure 3).[^lewis2020-rag]
- 검색기가 DPR에서 물려받은 지도 — **RAG의 검색기는 DPR의 검색기로 초기화되며, 그 DPR은 Natural
  Questions와 TriviaQA에 대한 검색 지도를 쓴다** (4.1절, p.5).[^lewis2020-rag] 곧 원전의 RAG는
  검색 지도 없이 처음부터 배운 것이 아니라 이미 지도된 검색기를 얹어 시작한다.
- 저자들이 남겨 둔 것 — **향후 작업으로 두 구성 요소를 BART와 비슷한 잡음 제거 목적이나 다른
  목적으로 처음부터 함께 사전 훈련할 수 있는지 조사하는 것이 유익할 수 있다** (6절,
  p.9).[^lewis2020-rag] #hypothesis
- 외부 지식 소스 자체의 한계 — **위키백과든 다른 어떤 잠재적 외부 지식 소스든 아마 결코 완전히
  사실적이고 편향이 전혀 없지는 않을 것이다** (Broader Impact, p.10).[^lewis2020-rag]

## 계보의 다음 걸음 — Fusion-in-Decoder

- 무엇을 바꿨는가 — **우리 접근은 [Min et al. 2020과 Lewis et al. 2020b]와 생성 모델이 검색된
  구절을 처리하는 방식에서 다르다. 이는 많은 수의 문서로 확장하는 것과 그 많은 양의 증거에서
  이득을 얻는 것을 가능하게 한다** (2절, p.875).[^izacard2021-fid] 곧 위의 원전과 부품 구성이
  같고(검색기 + 생성기) **디코딩의 배치만** 다르다.
- 그 배치의 원 진술 — **검색된 구절과 그 제목 각각이 질문과 이어 붙여져 다른 구절들과 독립적으로
  인코더에서 처리된다. 각 구절의 질문·제목·본문 앞에 `question:`·`title:`·`context:` 특수 토큰을
  붙인다. 마지막으로 디코더가 검색된 모든 구절의 결과 표현을 이어 붙인 것 위에서 어텐션을
  수행한다. 그래서 이 모델은 디코더에서만 증거 융합(evidence fusion)을 수행하며, 우리는 이를
  Fusion-in-Decoder라 부른다** (3절, p.876).[^izacard2021-fid]
- 왜 그것이 확장을 낳는가 — **구절을 인코더에서 독립적으로 처리함으로써 많은 수의 맥락으로 확장할
  수 있는데, 한 번에 하나의 맥락에 대해서만 자기 어텐션을 수행하기 때문이다. 이는 모델의 계산
  시간이 구절 수에 따라 이차가 아니라 선형으로 자란다는 뜻이다. 반면 구절을 디코더에서 함께
  처리하는 것은 여러 구절의 증거를 더 잘 집계하게 한다** (3절, p.876).[^izacard2021-fid] 위의
  원전이 **입력과 검색 내용을 단순히 이어 붙인** 것과 갈리는 자리가 여기다.[^lewis2020-rag]
- 무엇 위에 세웠는가 — **개방 도메인 QA를 위한 우리 생성 모델은 T5나 BART 같은 비지도 데이터로
  사전 훈련된 시퀀스 투 시퀀스 네트워크에 기반한다** (3절, p.876).[^izacard2021-fid] 실제로는
  **사전 훈련된 T5 모델로 초기화하며 base(2억 2천만)와 large(7억 7천만) 두 크기를 쓴다** (4절,
  p.876).[^izacard2021-fid] 검색은 **BM25와 DPR 둘을 쓰되 NQ·TriviaQA에는 DPR을, SQuAD에는
  BM25를 쓴다** (3절, p.876; 4절, p.877).[^izacard2021-fid]

## FiD가 잰 것

- 계보표다. 위의 원전이 같은 벤치마크에서 어디에 서는지가 이 표에 있다. 원문 표기를 그대로 옮겼다
  (4절, p.876, Table 1 발췌 — 정확 일치(EM)):[^izacard2021-fid]

  | Model | NQ | TriviaQA |
  |---|---|---|
  | ORQA (Lee et al., 2019) | 31.3 | 45.1 |
  | REALM (Guu et al., 2020) | 40.4 | – |
  | DPR (Karpukhin et al., 2020) | 41.5 | 57.9 |
  | RAG (Lewis et al., 2020b) | 44.5 | 56.1 |
  | T5 (Roberts et al., 2020) | 36.6 | – |
  | Fusion-in-Decoder (base) | 48.2 | 65.0 |
  | Fusion-in-Decoder (large) | 51.4 | 67.6 |

  - 읽는 법 — 위에서 옮긴 원전의 NQ 44.5가 이 표의 RAG 행이다.[^lewis2020-rag] **개념적으로
    단순한데도 이 방법은 NaturalQuestion과 TriviaQA 벤치마크에서 기존 작업을 앞선다. 특히
    생성 모델은 여러 구절의 증거를 집계해야 할 때 추출형 접근에 견주어 잘 수행하는 것으로
    보인다** (4절, p.877).[^izacard2021-fid]
- 파라미터를 지식으로 대신하는 셈 — **NaturalQuestions에서 폐쇄형 T5 모델은 110억 파라미터로
  36.6% 정확도를 얻는 반면 우리 접근은 7억 7천만 파라미터에 BM25 검색을 붙인 위키백과로 44.1%를
  얻는다. 두 방법이 대략 같은 양의 메모리를 정보 저장에 쓰므로, 이는 텍스트 기반 명시적 기억이
  지식 검색 과제에 경쟁력 있음을 가리킨다** (4절, p.877).[^izacard2021-fid]
- 구절 수에 대한 확장 — **검색 구절 수를 10개에서 100개로 늘리면 TriviaQA에서 6%, NaturalQuestions
  에서 3.5% 개선된다. 반면 대부분의 추출형 모델의 성능은 구절 10~20개 언저리에서 정점을 찍는 것으로
  보인다. 우리는 이것이 시퀀스 투 시퀀스 모델이 여러 구절의 정보를 결합하는 데 능하다는 증거라고
  본다** (4절, p.878, Figure 3).[^izacard2021-fid] #hypothesis 위의 원전이
  **RAG-Token은 검색 문서 10개에서 정점을 찍는다**고 관측한 자리와 대비된다.[^lewis2020-rag]
- 훈련 비용을 줄이는 길 — **훈련 구절 수를 줄이면 정확도가 떨어진다. 그래서 앞선 모델들을 100개
  구절로 1,000 스텝 파인 튜닝할 것을 제안하는데, 이는 정확도 격차를 줄이면서 계산 자원을 유의미하게
  덜 쓴다 — 100개 구절로 훈련할 때의 425 GPU 시간에 견주어 147 GPU 시간으로 NaturalQuestions
  46.0 EM에 도달할 수 있다** (4절, pp.877–878, Table 2).[^izacard2021-fid]
- 저자들이 남겨 둔 것 — **향후 작업으로 특히 많은 수의 지지 구절로 확장할 때 이 모델을 더
  효율적으로 만들 계획이다. 또한 검색을 우리 모델에 통합해 전체 시스템을 종단 간으로 학습할
  계획이다** (5절, p.878).[^izacard2021-fid] 곧 이 시점의 FiD는 검색기를 **밖에 둔** 구성이며,
  위의 원전이 질의 인코더와 생성기를 함께 훈련한 것보다 오히려 결합이 느슨하다.[^lewis2020-rag]

## 질의마다 검색을 탈지 정하기 — Self-RAG

- 무엇이 문제인가 — **검색이 필요한지, 구절이 관련 있는지와 무관하게 고정된 수의 검색 구절을
  무차별적으로 검색해 넣는 것은 LM의 다재다능함을 떨어뜨리거나 도움 안 되는 응답 생성으로 이어질 수
  있다** (초록, p.1).[^asai2024-selfrag] 위의 원전이 세운 구조가 **상위 `k`개를 늘 가져온다**는
  것을 전제하는 데서 나오는 문제다.[^lewis2020-rag]
- 제안 — **우리는 검색과 자기 반성을 통해 LM의 품질과 사실성을 높이는 Self-Reflective
  Retrieval-Augmented Generation(SELF-RAG)이라는 새 틀을 소개한다. 우리 틀은 하나의 임의 LM을
  훈련해 필요할 때마다 적응적으로 구절을 검색하고(retrieves passages on-demand), 반성
  토큰(reflection tokens)이라 불리는 특수 토큰을 써서 검색된 구절과 자기 생성물에 대해 생성하고
  반성하게 한다** (초록, p.1).[^asai2024-selfrag]
- 관습적 RAG와 갈리는 지점의 원 진술 — **이 과정은 검색 필요성과 무관하게 한결같이 고정된 수의
  문서를 검색하고(예컨대 아래 그림의 예는 사실 지식을 요구하지 않는다) 생성 품질을 두 번 다시 보지
  않는 관습적 RAG와 다르다. 게다가 SELF-RAG는 각 세그먼트에 대해 그 출력이 구절에 의해 지지되는지에
  대한 자기 평가와 함께 인용을 제공해 사실 검증을 더 쉽게 만든다** (1절, p.2).[^asai2024-selfrag]
- 세 걸음 — **입력 프롬프트와 앞선 생성물이 주어지면 SELF-RAG는 먼저 검색된 구절로 이어지는 생성을
  증강하는 것이 도움이 될지 판정한다. 그렇다면 검색기 모델을 필요할 때 호출하는 검색 토큰을
  출력한다(1단계). 이어서 SELF-RAG는 검색된 여러 구절을 동시에 처리해 그 관련성을 평가하고 대응하는
  과제 출력을 생성한다(2단계). 그다음 비평 토큰을 생성해 사실성과 전반적 품질의 관점에서 자기 출력을
  비평하고 최선을 고른다(3단계)** (1절, p.1).[^asai2024-selfrag]

## 반성 토큰 네 종류

- 네 종류의 원 정의다. 원문 표기를 그대로 옮겼다 (3절, p.4, Table 1):[^asai2024-selfrag]

  | Type | Input | Output | Definitions |
  |---|---|---|---|
  | Retrieve | x / x, y | {yes, no, continue} | Decides when to retrieve with R |
  | IsRel | x, d | {relevant, irrelevant} | d provides useful information to solve x. |
  | IsSup | x, d, y | {fully supported, partially supported, no support} | All of the verification-worthy statement in y is supported by d. |
  | IsUse | x, y | {5, 4, 3, 2, 1} | y is a useful response to x. |

  **`x`·`y`·`d`는 각각 입력·출력·관련 구절을 가리키며, 아래 세 행이 세 종류의 비평
  토큰(Critique tokens)이다** (3절, p.4, Table 1 설명).[^asai2024-selfrag] 곧 반성 토큰은
  **검색 토큰 하나와 비평 토큰 셋**으로 갈린다.
- 어떻게 생성되는가 — **SELF-RAG는 반성 토큰을 확장된 모델 어휘에서의 다음 토큰 예측으로 통합함으로써
  임의의 LM이 그것을 생성하도록 훈련한다** (1절, p.1).[^asai2024-selfrag] 훈련에서
  **검색된 텍스트 청크를 손실 계산에서 가리고 원 어휘 `V`를 반성 토큰 집합으로 확장한다** (3.2.2절,
  p.5).[^asai2024-selfrag]
- 비평 모델은 훈련 때만 있다 — **반성 토큰은 훈련된 비평 모델에 의해 오프라인으로 원 코퍼스에
  삽입된다. 이는 훈련 중 비평 모델을 띄워 둘 필요를 없애 부담을 줄인다** (1절,
  p.2).[^asai2024-selfrag] 그 비평 모델은 **GPT-4에 유형별 지시를 프롬프트해 모은 데이터로
  지도되며, 유형마다 4천~2만 건의 지도 훈련 데이터를 모아 합친다** (3.2.1절,
  pp.4–5).[^asai2024-selfrag] 결과로 **비평 모델은 대부분의 반성 토큰 범주에서 GPT-4 기반 예측과
  90% 넘는 일치를 달성한다** (3.2.1절, p.5).[^asai2024-selfrag]
- RLHF와 무엇이 다른가 — **PPO가 훈련 중 별도의 보상 모델에 기대는 반면, 우리는 비평을 오프라인으로
  계산해 훈련 코퍼스에 직접 삽입하고 생성기 LM은 표준 LM 목적으로 훈련된다. 이는 PPO에 견주어 훈련
  비용을 유의미하게 줄인다** (3.2.2절, pp.5–6).[^asai2024-selfrag] 그 정렬 기법은
  [선호 파인 튜닝](../concepts/preference-finetuning.md)에 있다.

## 추론 시점에 행동을 바꾸는 손잡이

- 왜 손잡이가 필요한가 — **자기 출력을 자기 평가하는 반성 토큰을 생성하는 것은 SELF-RAG를 추론
  단계에서 조종 가능하게 만들어 다양한 과제 요구에 자기 행동을 맞추게 한다. 사실 정확성을 요구하는
  과제에서는 모델이 구절을 더 자주 검색하기를 바라고, 개인 경험 에세이 작문 같은 더 열린 과제에서는
  덜 검색하고 전반적 창의성이나 유용성 점수를 우선하는 쪽으로 무게가 옮겨 간다** (3.3절,
  p.6).[^asai2024-selfrag]
- 문턱 — **SELF-RAG는 Retrieve를 예측해 텍스트 구절을 언제 검색할지 동적으로 정한다. 대안으로 우리
  틀은 문턱을 설정할 수 있게 한다 — Retrieve의 모든 출력 토큰에 걸쳐 정규화한 Retrieve=Yes 토큰의
  생성 확률이 지정된 문턱을 넘으면 검색을 발동한다** (3.3절, p.6).[^asai2024-selfrag] 실험의 기본값은
  **대부분의 과제에 0.2, 인용을 요구하는 ALCE에 0**이다 (4.3절, p.7).[^asai2024-selfrag]
- 세그먼트 단위 빔 탐색 — **각 세그먼트 단계 `t`에서 검색이 필요하면 검색기가 구절 `K`개를 가져오고
  생성기가 각 구절을 병렬로 처리해 서로 다른 이어짐 후보 `K`개를 출력한다. 우리는 세그먼트 수준 빔
  탐색을 수행해 각 시점에서 상위 `B`개 세그먼트 이어짐을 얻고 생성 끝에 최선의 시퀀스를 돌려준다.
  구절 `d`에 대한 각 세그먼트 `y_t`의 점수는 각 비평 토큰 유형의 정규화된 확률의 선형 가중합인
  비평 점수 `S`로 갱신된다** (3.3절, p.6).[^asai2024-selfrag]
  - 가중치가 사용자 손잡이다 — **식 (4)의 가중치 `w_G`는 추론 시점에 조정할 수 있는 초매개변수로,
    시험 시점의 맞춤 행동을 가능하게 한다. 예컨대 결과 `y`가 대체로 증거에 의해 지지되게 하려면
    IsSup 점수의 가중치를 높이고 다른 국면의 가중치를 상대적으로 낮출 수 있다** (3.3절,
    p.6).[^asai2024-selfrag] 기본 설정은 **IsRel·IsSup·IsUse에 각각 1.0·1.0·0.5**이고 세그먼트
    빔 폭은 2다 (4.3절, p.7).[^asai2024-selfrag]
  - 그 손잡이의 대가가 실측된다 — **IsSup의 가중항을 높이면 모델 생성이 증거에 의해 지지되는지에
    더 무게가 실려 인용 정밀도에 긍정적 효과를 낸다. 반대로 가중치가 커질수록 MAUVE 점수는 낮아진다
    — 생성이 길고 유창해질수록 인용으로 완전히 지지되지 않는 주장이 흔히 더 많아지기 때문이다**
    (5.2절, pp.9–10, Figure 3b).[^asai2024-selfrag] 곧 사실성과 유창성이 하나의 손잡이 양 끝에
    있다.
  - 무른 제약 대신 단단한 제약도 쓸 수 있다 — **식 (4)의 무른 보상 함수 대신, 모델이 바람직하지
    않은 비평 토큰(예: IsSup=No support)을 생성하면 그 세그먼트 이어짐을 명시적으로 걸러 낼 수도
    있다. RLHF에서 여러 선호의 맞바꿈을 조절하려면 흔히 모델 행동을 바꾸는 훈련이 필요한 데 반해
    SELF-RAG는 추가 훈련 없이 LM을 맞춘다** (3.3절, p.6).[^asai2024-selfrag]

## Self-RAG가 잰 것과 그 절제 실험

- 주요 결과. 원문 표기를 그대로 옮겼다 (5.1절, p.8, Table 2 발췌 — PopQA·TriviaQA·PubHealth·
  ARC-Challenge는 정확도, ASQA는 인용 정밀도/재현율):[^asai2024-selfrag]

  | LM | PopQA | TQA | Pub | ARC | ASQA (pre) | ASQA (rec) |
  |---|---|---|---|---|---|---|
  | Llama2-chat 13B | 20.0 | 59.3 | 49.4 | 38.4 | – | – |
  | Ret-Llama2-chat 13B | 51.8 | 59.8 | 52.1 | 37.9 | 19.8 | 36.1 |
  | ChatGPT | 29.3 | 74.3 | 70.1 | 75.3 | – | – |
  | Ret-ChatGPT | 50.8 | 65.7 | 54.7 | 75.3 | 65.1 | 76.6 |
  | Llama2 7B (검색 포함) | 38.2 | 42.5 | 30.0 | 48.0 | 2.9 | 4.0 |
  | Llama2-FT 7B | 48.7 | 57.3 | 64.3 | 65.8 | 5.0 | 7.5 |
  | SELF-RAG 7B | 54.9 | 66.4 | 72.4 | 67.3 | 66.9 | 67.8 |
  | SELF-RAG 13B | 55.8 | 69.3 | 74.5 | 73.1 | 70.3 | 71.3 |

  - 읽는 법 — **SELF-RAG는 모든 과제에서 지도 파인 튜닝된 LLM보다 상당한 성능 우위를 보이며,
    PubHealth·PopQA·전기 생성·ASQA(Rouge와 MAUVE)에서 ChatGPT까지 앞선다** (5.1절,
    p.8).[^asai2024-selfrag] 인용 쪽에서는 **ASQA에서 ChatGPT를 뺀 모든 모델보다 인용 정밀도와
    재현율이 유의미하게 높고, 모델이 생성한 주장이 인용된 증거에 완전히 지지되는지를 재는 인용
    정밀도에서는 ChatGPT까지 앞선다** (5.1절, p.8).[^asai2024-selfrag]
  - 훈련 데이터 때문이 아니다 — **SELF-RAG와 같은 지시–출력 쌍으로 훈련되었으나 반성 토큰이나
    검색된 구절 없이 시험 시점에만 검색 증강되는 Llama2-FT 7B가 SELF-RAG에 뒤진다. 이 결과는
    SELF-RAG의 이득이 훈련 데이터에서만 오는 것이 아님을 가리킨다** (5.1절,
    pp.8–9).[^asai2024-selfrag]
- 절제 실험이 짚는 것 — **관습적 RAG 접근처럼 관련성과 무관하게 상위 구절을 쓰는 것(Retrieve
  top 1)이 PopQA와 ASQA에서 큰 하락을 낳고, 빔 탐색 중 IsSup을 제거하면 ASQA 성능이 상한다. 이는
  검색 모델의 상위 구절을 순진하게 전부 쓰거나 관련성 점수에만 의존하는 대신 세밀한 다중 기준에
  근거해 생성을 신중히 고르는 SELF-RAG의 능력이 효과적임을 보인다** (5.2절,
  p.9).[^asai2024-selfrag] 곧 **검색을 끄는 능력만큼이나 검색한 것을 버리는 능력이 이 설계의
  이득**이라는 것이 저자들의 읽기다.
- 문턱을 움직이면 — **문턱 `δ`를 바꿔 가며 재면 모델의 검색 빈도가 두 데이터셋 모두에서 극적으로
  바뀐다. 한편으로 덜 검색해서 생기는 성능 저하는 PubHealth에서 더 작고 PopQA에서 더 크다**
  (5.2절, p.10, Figure 3c).[^asai2024-selfrag] 곧 "검색을 얼마나 탈 것인가"의 최적점은 과제마다
  다르며 하나의 상수가 아니다.
- 사람이 본 반성 토큰의 신뢰도 — **PopQA와 전기 결과에서 각 50건을 표집해, 주석자들은 SELF-RAG의
  답이 흔히 그럴듯하고 관련 구절에 의해 지지된다고 보았으며 IsRel·IsSup 반성 토큰 예측이 대체로 자기
  평가와 정렬됨을 발견했다** (5.2절, p.10, Figure 4d).[^asai2024-selfrag] 표본 100건의 소규모
  평가라는 점은 저자들이 스스로 "small human evaluations"로 밝힌다.

검색 결정을 모델 밖으로 빼는 두 갈래(사전 라우팅·생성 중 결정)와 세 갈래의 대가 비교는
[적응형 검색 전략](../concepts/adaptive-retrieval-strategies.md)이 담는다.

## 이 패턴이 못 하는 질문

> **심사 조건**: 이 절의 claim은 **미심사 arXiv 원고**에서 온다(표제에 "Preprint. Under
> review." 인쇄). 진단 자체는 이 페이지의 다른 원전들과 정합하지만, 그 해법의 우열 주장은
> 제안자가 자기 설계한 절차로 잰 값이므로 그 조건에서 읽는다.

- 진단 — **RAG는 "데이터셋의 주요 주제는 무엇인가?" 같은 전체 텍스트 코퍼스를 겨냥한 전역 질문에서
  실패하는데, 이것이 본질적으로 명시적 검색 과제가 아니라 질의 초점 요약(query-focused
  summarization) 과제이기 때문이다** (초록, p.1).[^edge2024-graphrag]
- 이 페이지가 서술한 구조에 저자들이 붙인 이름 — **관습적 RAG 접근에서 검색 과정은 질의와 의미적으로
  비슷한 정해진 수의 레코드를 돌려주고 생성된 답은 그 검색된 레코드의 정보만 쓴다. 어떤 RAG 접근은
  대안적 검색 기전을 쓸 수 있지만, 우리는 관습적 접근의 계열을 통틀어 벡터 RAG(vector RAG)라
  부른다** (2.1절, p.2).[^edge2024-graphrag] 곧 위에서 서술한 **상위 `k`개를 가져와 이어 붙이는**
  구조 전체가 하나의 이름을 갖게 되고, 그 바깥에 다른 계열이 놓인다.
- 그 계열이 무엇인지와 실측은 [텍스트 너머의 RAG](../concepts/rag-beyond-text.md)에 있다.

## 이어지는 페이지

- [적응형 검색 전략](../concepts/adaptive-retrieval-strategies.md) — 검색을 탈지 정하는 세 갈래와 그 대가
- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 검색기의 첫째 갈래, 낱말 일치와 그 랭킹
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — 둘째 갈래, 뜻으로 찾는 파이프라인
- [청킹 전략](../concepts/chunking-strategy.md) — 여기서 미룬 "어떻게 쪼갤 것인가"
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — 검색기가 좋은지 재는 자리
- [텍스트 너머의 RAG](../concepts/rag-beyond-text.md) — 외부 소스가 이미지·표일 때
- [에이전트란 무엇인가](../concepts/agents-defined.md) — RAG를 특수 사례로 품는 더 넓은 패턴
- [파인 튜닝과 RAG](../concepts/finetuning-versus-rag.md) — 7장이 RAG와 파인 튜닝 중 무엇을 먼저 할지를
  실패 유형으로 가르는 자리
- [프롬프트에 맥락 주기](../concepts/providing-context-in-prompts.md) — 5장이 이 장으로 넘긴 자리
- [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md) — 긴 컨텍스트
  논쟁의 실측 근거
- [사실 일관성](../concepts/factual-consistency.md) — RAG 응답이 검색된 맥락과 어긋나는지 재는 기준
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 저장 엔진 축이 같은 검색을
  색인 구조의 관점에서 서술하는 자리
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 원전이 "리랭커도 추출형
  판독기도 필요 없다"고 말한 자리의 반대편
- [반성과 오류 교정](../concepts/agent-reflection-and-error-correction.md) — 같은 낱말이 에이전트
  쪽에서 프롬프트 기반 기전으로 쓰이는 자리
- [선호 파인 튜닝](../concepts/preference-finetuning.md) — Self-RAG가 비용 때문에 피했다고 적은
  RLHF 계열
- [쿼리 재작성](../concepts/query-rewriting.md) — 능동 검색이 임시 문장을 질의로 바꾸는 자리
- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 세 갈래가 공통으로 BM25를 검색기로 쓰는 자리
- [모델 라우터](../concepts/model-router.md) — 질의를 보고 경로를 고르는 같은 형태의 부품

[^izacard2021-fid]: Izacard and Grave 2021, "Leveraging Passage Retrieval with Generative Models
    for Open Domain Question Answering", EACL 2021, pp.874–880. 쪽 번호는 학회 논문집 인쇄
    쪽이다. 이 페이지는 초록·1절 Introduction·2절 Related Work의 자기 위치 진술·3절 Method·
    4절 Experiments·5절 Conclusion을 담았다. Table 1은 NQ·TriviaQA 열의 일곱 행만 발췌해 옮겼고
    SQuAD Open 열과 나머지 행은 옮기지 않았다. Table 2(훈련 구절 수별 성능)와 Figure 1·2·3은
    옮기지 않았고 본문이 서술한 수치만 담았다.
    DPR(Karpukhin et al., 2020)·RAG(Lewis et al., 2020b)·REALM(Guu et al., 2020)은 이 KB에 원전이
    있다. T5(Raffel et al., 2020)·BART·ORQA(Lee et al., 2019)·BM25(Robertson et al., 1995)·FAISS·
    SpaCy는 izacard2021-fid를 통한 전언이다.

[^asai2024-selfrag]: Asai et al. 2024, "Self-RAG: Learning to Retrieve, Generate, and Critique
    through Self-Reflection", ICLR 2024 (oral). 스냅샷은 arXiv:2310.11511 v1(2023-10-17)이며
    표제에 "Preprint."가 인쇄된 **학회 카메라 레디 이전 판본**이다 — 심사를 통과한 작업이지만
    이 페이지가 인용하는 문면은 프리프린트의 것이므로 카메라 레디와 자구가 다를 수 있다. 쪽
    번호는 그 PDF의 쪽이다. 이 페이지는 초록·1절 Introduction·3절 SELF-RAG(3.1–3.3)·4절
    Experiments(4.1–4.3)·5절 Results and Analysis(5.1–5.2)·6절 Conclusion을 담았다. Table 1과
    Table 2는 원문 표기를 그대로 옮기되 Table 2는 여섯 열(PopQA·TQA·Pub·ARC·ASQA 정밀도·재현율)과
    여덟 행만 발췌했다 — Bio(FactScore)·ASQA의 str-em·rouge·MAUVE 열과 Alpaca·CoVE·Toolformer·
    SAIL·Perplexity.ai 행은 옮기지 않았다. Table 3(절제)·Figure 3·Figure 4는 옮기지 않았고 본문이
    서술한 것만 담았다. Figure 1(전체 도식, p.2)·Figure 2(훈련 예시, p.5)와 Algorithm 1, 식
    (1)–(4), 부록 A–D는 본문이 서술한 것만 담았다.
    RAG(Lewis et al., 2020)는 이 KB에 원전이 있다. Llama2(Touvron et al., 2023)·GPT-4·
    Contriever-MS MARCO(Izacard et al., 2022a)·PopQA(Mallen et al., 2023)·TriviaQA·PubHealth·
    ARC-Challenge·ALCE-ASQA(Gao et al., 2023)·FactScore(Min et al., 2023)·MAUVE(Pillutla et al.,
    2021)·PPO(Schulman et al., 2017)·SAIL·Toolformer는 asai2024-selfrag를 통한 전언이다.

[^edge2024-graphrag]: Edge et al., "From Local to Global: A GraphRAG Approach to Query-Focused
    Summarization", arXiv:2404.16130. **미심사** — 원고 표제에 "Preprint. Under review."가
    인쇄돼 있고 2026-08 재검증에서도 심사본이 확인되지 않았다. 스냅샷은 v2(2025-02-19)이며 소스
    메타의 연도(2024)는 v1 기준이다. 쪽 번호는 그 PDF의 쪽이다. 이 페이지는 초록과 2.1절 RAG
    Approaches and Systems의 진단·명명 진술만 담았다 — 파이프라인과 실측은
    [텍스트 너머의 RAG](../concepts/rag-beyond-text.md)가 담는다.

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 장 도입부(p.253)와
    "RAG" 절 서두(pp.253–256), "RAG Architecture" 절(pp.256–257)을 담았다. 도판 Figure 6-1(위키백과
    retrieve-then-generate 도식, p.254)과 Figure 6-2(기본 RAG 아키텍처, p.256)는 옮기지 않았고 본문과
    도판 설명이 서술한 것만 담았다. Chen et al.(2017)·Petroni et al.(2020)·Anthropic(2024)은
    huyen2025를 통한 전언이다. Lewis et al.(2020)에 대한 전언은 아래 원전 각주로 이중화했다.

[^lewis2020-rag]: Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP
    Tasks", NeurIPS 2020 (논문 16쪽 — 본문 pp.1–10, 나머지는 참고문헌). 쪽 번호는 스냅샷한 PDF의
    쪽이다. 이 페이지는 초록·1절 Introduction·2절 Methods(2.1–2.5)·3절 Experiments 서두·4절
    Results(4.1–4.5)·5절 Related Work·6절 Discussion·Broader Impact을 담았다. 도판 Figure 1(전체
    구조 도식, p.2)·Figure 2(RAG-Token 문서 사후확률, p.7)·Figure 3(검색 문서 수에 따른 성능,
    p.8)은 옮기지 않았고 본문이 서술한 것만 담았다. 수식은 원문의 수학 표기를 인라인 코드로 옮긴
    것이며, 원문의 상위 K 주변화 식 자체는 옮기지 않았다. 표는 Table 1·4·5·6의 본문 서술만 옮겼다.
    DPR(Karpukhin et al., 2020)·HNSW(Malkov and Yashunin)·REALM(Guu et al., 2020)은 이 KB에 원전이
    있다 — 다만 이 원전이 인용하는 REALM은 arXiv:2002.08909 프리프린트이고 이 KB의 정본은 같은
    작업의 ICML 2020 심사본이다.
    ORQA(Lee et al., 2019)·BERT(Devlin et al., 2019)·BART(Lewis et al., 2020)·
    FAISS(Johnson et al., 2017)는 lewis2020-rag를 통한 전언이며 각각의 원전은 아직 반입되지 않았다.

[^guu2020-realm]: Guu et al. 2020, "REALM: Retrieval-Augmented Language Model Pre-Training",
    ICML 2020 (PMLR 119, 인쇄 쪽 3929–3938 — 논문 10쪽). 스냅샷은 PMLR 카메라 레디이며(1쪽 하단에
    "Proceedings of the 37th International Conference on Machine Learning, Vienna, Austria,
    PMLR 119, 2020"이 인쇄돼 있다) 그 PDF에는 인쇄 쪽 번호가 없으므로 쪽 번호는 스냅샷한 PDF의
    쪽이다. 이 페이지는 초록·1절 Introduction·3.1절 REALM's generative process·3.3절 Training의
    MIPS 갱신 진술·3.4절 Injecting inductive biases·4.4절 Main results·4.5절 Analysis·6절 Future
    Work를 담았다 — 계보 위치와 핵심 기제만 담은 절제 반입이다. 담지 않은 것: 2절 Background,
    3.2절 Model architecture의 인코더 식과 지식 증강 인코더 정식화, 4.1–4.3절의 벤치마크·비교 대상·
    구현 세부, 5절 Discussion and Related Work의 네 관점(코퍼스를 맥락으로 보는 언어 모델링·
    retrieve-and-edit·확장 가능한 접지 신경 기억·비지도 코퍼스 정렬). Table 1과 Table 2는 본문이
    서술한 수치만 담았고 표 자체는 옮기지 않았다. Table 3(마스크 예측 예시)·Figure 1·2·3은 옮기지
    않았다. 수식(주변화 식 (1)·검색 분포·기울기 유도)은 옮기지 않고 본문 서술로만 담았다.
    Lewis et al. 2020(RAG)은 이 KB에 원전이 있다 — 다만 **이 원전이 인용하는 "Lewis et al., 2019"는
    BART이고 RAG가 아니다**(REALM이 먼저 나왔다). ORQA(Lee et al., 2019)·T5(Raffel et al., 2019)·
    Roberts et al.(2020)·BERT(Devlin et al., 2018)·RoBERTa(Liu et al., 2019)·SpanBERT(Joshi et al.,
    2019)·Inverse Cloze Task·kNN-LM(Khandelwal et al., 2019)·DrQA(Chen et al., 2017)·
    HardEM·GraphRetriever(Min et al., 2019a,b)·PathRetriever(Asai et al., 2019)·
    NaturalQuestions(Kwiatkowski et al., 2019)·WebQuestions(Berant et al., 2013)·CuratedTrec·
    SQuAD(Rajpurkar et al., 2016)·CC-News·MIPS 알고리즘(Ram and Gray, 2012; Shrivastava and Li,
    2014; Shen et al., 2015)은 guu2020-realm을 통한 전언이다.

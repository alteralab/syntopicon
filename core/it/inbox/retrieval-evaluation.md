---
type: concept
title: 검색 품질 평가
description: 검색기가 좋은지 무엇으로 재는가 — 어휘 갈래와 임베딩 갈래가 속도·성능·비용에서 갈리는 지점, 검색된 문서로 재는 컨텍스트 정밀도와 컨텍스트 재현율, 순위까지 보는 NDCG·MAP·MRR과 임베딩 자체를 재는 MTEB·BEIR, 원전이 세운 상위 k 검색 정확도와 근사 탐색의 재현율 정의, 참조 답 없이 재는 세 지표를 정식화한 RAGAS 원전과 그 계산 절차·사람과의 일치도, 색인과 질의 사이의 맞바꿈을 재는 ANN-Benchmarks 네 지표, 그리고 검색 솔루션을 고를 때 던지는 질문
generated: { by: "claude-opus-5", at: "2026-08-17T11:00:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: karpukhin2020-dpr, resource: /it/sources/karpukhin2020-dpr.md }
  - { id: malkov2018-hnsw, resource: /it/sources/malkov2018-hnsw.md }
  - { id: es2024-ragas, resource: /it/sources/es2024-ragas.md }
---

# 검색 품질 평가

- [두 갈래는 어디서 갈리는가](#두-갈래는-어디서-갈리는가)
- [원전이 세운 상위 k 검색 정확도](#원전이-세운-상위-k-검색-정확도)
- [컨텍스트 정밀도와 컨텍스트 재현율](#컨텍스트-정밀도와-컨텍스트-재현율)
- [참조 답 없이 재는 세 지표](#참조-답-없이-재는-세-지표)
- [그 셋을 실제로 계산하는 절차](#그-셋을-실제로-계산하는-절차)
- [사람과 얼마나 맞는가](#사람과-얼마나-맞는가)
- [책의 지표 이름과 원전의 정의가 어긋나는 자리](#책의-지표-이름과-원전의-정의가-어긋나는-자리)
- [순위까지 보는 지표와 임베딩 자체의 평가](#순위까지-보는-지표와-임베딩-자체의-평가)
- [지연과 비용](#지연과-비용)
- [두 갈래 비교표](#두-갈래-비교표)
- [색인과 질의 사이의 맞바꿈](#색인과-질의-사이의-맞바꿈)
- [근사 탐색에서 재현율은 무엇의 비율인가](#근사-탐색에서-재현율은-무엇의-비율인가)
- [무엇을 평가해야 하는가](#무엇을-평가해야-하는가)
- [검색 솔루션을 고를 때](#검색-솔루션을-고를-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **검색기가 좋은 문서를 꺼내 오는지 무엇으로 재는가.**

## 두 갈래는 어디서 갈리는가

- 공통점 — **검색의 긴 역사 덕에 그 많은 성숙한 해법이 어휘 기반과 임베딩 기반 검색 둘 다를 비교적
  쉽게 시작하게 만든다. 각 접근에는 장단점이 있다** (6장, p.264).[^huyen2025]
- 속도 — **어휘 기반 검색은 색인과 질의 양쪽에서 일반적으로 임베딩 기반 검색보다 훨씬 빠르다. 용어
  추출은 임베딩 생성보다 빠르고, 어떤 용어에서 그것을 담은 문서로 사상하는 것은 최근접 이웃 탐색보다
  계산 비용이 덜할 수 있다** (6장, p.264).[^huyen2025]
  - **원전의 실측은 색인 쪽에서만 이 진술과 같은 방향이다.** DPR 저자들이 잰 값은 이렇다 —
    **FAISS 인메모리 색인의 도움으로 DPR은 초당 995.0개 질문을 처리하며 질문마다 상위 100개 구절을
    돌려준다. 반면 자바로 구현되고 파일 색인을 쓰는 BM25/Lucene은 CPU 스레드당 초당 23.7개 질문을
    처리한다. 반대로 조밀 벡터의 색인을 짓는 데 필요한 시간은 훨씬 길다 — 2,100만 구절의 임베딩
    계산에 GPU 8장으로 약 8.8시간, 그 위에 FAISS 색인 구축에 단일 서버로 8.5시간이 걸리는 반면
    루씬 역색인은 전부 합쳐 30분 정도다** (5.4절, p.7).[^karpukhin2020-dpr] 곧 색인 구축은 어휘
    쪽이 압도적으로 싸지만, 질의 처리량은 이 설정에서 조밀 쪽이 40배 이상 앞선다. 두 진술이 같은
    것을 재고 있지 않다는 점이 어긋남의 자리다 — huyen2025는 임베딩 생성 비용까지 포함한 질의
    경로를 말하고 원전은 인메모리 색인에 대한 탐색 처리량을 잰다. **어느 쪽 수치를 인용하는지에
    따라 결론이 뒤집히므로 "질의가 빠르다"를 조건 없이 옮기지 말 것.**
- 상자에서 꺼낸 성능 — **어휘 기반 검색은 상자에서 꺼낸 그대로도 잘 작동한다. 엘라스틱서치와 BM25
  같은 해법은 많은 검색·회수 애플리케이션을 성공적으로 구동해 왔다. 그러나 그 단순함은 성능을
  개선하려고 만질 수 있는 구성 요소가 더 적다는 뜻이기도 하다** (6장, p.264).[^huyen2025]
  - 원전이 붙이는 단서 — 원전의 BM25 기준선도 상자에서 꺼낸 그대로는 아니다. **루씬 구현을 썼고
    BM25 파라미터 `b = 0.4`와 `k₁ = 0.9`를 개발 집합으로 튜닝했다** (5절, p.5 각주
    9).[^karpukhin2020-dpr]
- 임베딩 쪽의 상한과 약점 — **반면 임베딩 기반 검색은 시간이 지나며 어휘 기반 검색을 능가하도록 크게
  개선될 수 있다. 임베딩 모델과 검색기를 따로, 함께, 또는 생성 모델과 연계해 파인 튜닝할 수 있다.
  그러나 데이터를 임베딩으로 변환하는 것은 특정 오류 코드(예: EADDRNOTAVAIL (99))나 제품명 같은
  키워드를 흐릿하게 만들어 나중에 검색하기 어렵게 할 수 있다. 이 한계는 임베딩 기반 검색을 어휘 기반
  검색과 결합함으로써 다뤄질 수 있다** (6장, p.264).[^huyen2025][^karpukhin2020-dpr] 그 결합은
  [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)에 있다.
  - 원전이 든 실패 예 — **DPR은 의미 표현에 뛰어나지만 드물게 나타나는 두드러진 구절을 표현할
    능력이 모자랄 수 있다** (부록 C, p.12).[^karpukhin2020-dpr] "Thoros of Myr" 같은 고유
    표현에서 조밀 검색이 실패하는 것이 huyen2025가 "키워드를 흐릿하게 만든다"고 부른 것의 실측이다.

## 원전이 세운 상위 k 검색 정확도

- 검색기를 따로 재는 지표의 원 정의다 (2절, p.2):[^karpukhin2020-dpr]

  > For a fixed *k*, a *retriever* can be evaluated in isolation on *top-k retrieval accuracy*,
  > which is the fraction of questions for which *C_F* contains a span that answers the question.

  여기서 **검색기 `R : (q, C) → C_F`는 질문 `q`와 코퍼스 `C`를 받아 훨씬 작은 필터 집합
  `C_F ⊂ C`를 돌려주는 함수이며 `|C_F| = k ≪ |C|`다** (2절, p.2).[^karpukhin2020-dpr]
- 실제로 쓴 `k` — **상위 `k` 정확도로 다섯 개 QA 데이터셋의 구절 검색 시스템을 비교하며 `k ∈ {20,
  100}`을 쓴다** (5.1절, p.5).[^karpukhin2020-dpr] 검색된 상위 20/100개 구절 중 답을 담은 것의
  비율이라는 뜻이다.
- 검색 품질이 최종 품질로 이어지는가 — 저자들이 자기 기여로 명시한 둘째 항목이 이 검증이다 —
  **개방 도메인 질의응답의 맥락에서 더 높은 검색 정밀도가 실제로 더 높은 종단 간 QA 정확도로
  이어짐을 확인한다** (1절, p.2).[^karpukhin2020-dpr] 결과 쪽에서 그것은 **더 높은 검색기 정확도가
  통상 더 나은 최종 QA 결과로 이어진다 — SQuAD를 뺀 모든 경우에서 DPR이 검색한 구절에서 추출한
  답이 BM25에서 나온 것보다 옳을 가능성이 높다**로 나타난다 (6.2절, p.8).[^karpukhin2020-dpr]
  huyen2025가 "검색기는 시스템이 고품질의 답을 생성하도록 도우면 좋은 것"이라고 적은 자리의 실측이
  이것이다.

## 컨텍스트 정밀도와 컨텍스트 재현율

- 무엇으로 재는가 — **검색기의 품질은 그것이 검색해 오는 데이터의 품질에 근거해 평가될 수 있다. RAG
  평가 프레임워크가 흔히 쓰는 두 지표는 컨텍스트 정밀도(context precision)와 컨텍스트
  재현율(context recall), 줄여서 정밀도와 재현율이다. 컨텍스트 정밀도는 컨텍스트 관련성(context
  relevance)이라고도 불린다** (6장, p.264).[^huyen2025]
  - **컨텍스트 정밀도 — 검색된 모든 문서 중 질의에 관련 있는 것은 몇 퍼센트인가?** (6장,
    p.264)[^huyen2025]
  - **컨텍스트 재현율 — 질의에 관련 있는 모든 문서 중 검색된 것은 몇 퍼센트인가?** (6장,
    p.264)[^huyen2025]
- 어떻게 계산하는가 — **이 지표들을 계산하려면 시험 질의 목록과 문서 집합으로 평가 세트를 큐레이션
  한다. 각 시험 질의에 대해 각 시험 문서가 관련 있는지 아닌지 주석을 단다. 주석은 사람이 할 수도
  AI 판정자가 할 수도 있다. 그런 다음 이 평가 세트에서 검색기의 정밀도와 재현율 점수를 계산한다**
  (6장, p.264).[^huyen2025] 그 판정자 자체는
  [AI 판정자](../concepts/ai-as-a-judge.md)가 담는다.
  - 원전이 주석 비용을 우회한 방법 — DPR은 관련성 주석 대신 **답 문자열의 포함 여부**로 정확도를
    정의한다. 그래서 **오직 질문–답 쌍만 주어지는 TREC·WebQuestions·TriviaQA에서는 BM25가 돌려준
    구절 중 답을 담은 최상위 구절을 양성 구절로 쓰고, 상위 100개 검색 구절 중 답이 있는 것이
    없으면 그 질문을 버린다** (4.2절, p.4).[^karpukhin2020-dpr] 주석 없이 재는 대가는 이 버려지는
    질문들이다.
- 프로덕션에서 재현율이 빠지는 이유 — **프로덕션에서 어떤 RAG 프레임워크는 컨텍스트 정밀도만
  지원하고 컨텍스트 재현율은 지원하지 않는다. 주어진 질의의 컨텍스트 재현율을 계산하려면 데이터베이스
  안 모든 문서의 그 질의에 대한 관련성에 주석을 달아야 하기 때문이다. 컨텍스트 정밀도는 계산하기 더
  간단하다 — 검색된 문서를 질의와 비교하기만 하면 되고 그것은 AI 판정자가 할 수 있다** (6장,
  p.264).[^huyen2025]

## 참조 답 없이 재는 세 지표

> **심사 조건**: 이 절부터 세 절의 claim은 EACL 2024 **System Demonstrations** 트랙 논문에서
> 온다. 본 학회 트랙보다 심사가 가볍고 도구 시연이 목적인 트랙이므로, 아래 수치는 그 조건에서
> 읽는다.

- 왜 참조 없이 재야 하는가 — **RAG 시스템을 지을 때 우리는 보통 사람이 주석한 데이터셋이나 참조
  답에 접근할 수 없다. 그래서 우리는 완전히 자기 완결적이고 참조 없는(reference-free) 지표에
  집중한다** (3절, pp.151–152).[^es2024-ragas] huyen2025가 "AI 판정자는 참조 데이터 없이도 작동할
  수 있다"고 적은 이점이 이 원전의 설계 전제다.
- 무엇이 문제였는가 — **실무에서 RAG 시스템은 흔히 언어 모델링 과제 자체로, 곧 참조 코퍼스의
  퍼플렉시티를 재어 평가된다. 그러나 그런 평가가 늘 하류 성능을 예측하지는 않는다. 게다가 이 평가
  전략은 LM 확률에 기대는데 그것은 어떤 폐쇄 모델(예: ChatGPT·GPT-4)에서는 접근할 수 없다.
  질의응답도 흔한 평가 과제지만 보통 짧은 추출형 답의 데이터셋만 고려되며, 이는 시스템이 실제로
  쓰이는 방식을 대표하지 못할 수 있다** (1절, p.150).[^es2024-ragas]
- 세 국면의 원 정의다 (3절, p.152):[^es2024-ragas]
  - **충실성(Faithfulness)** — **답이 주어진 맥락에 접지되어야 한다는 착상. 이는 환각을 피하고
    검색된 맥락이 생성된 답의 정당화 노릇을 할 수 있게 하는 데 중요하다.**
  - **답 관련성(Answer Relevance)** — **생성된 답이 실제로 제시된 질문을 다뤄야 한다는 착상.**
  - **맥락 관련성(Context Relevance)** — **검색된 맥락이 초점이 맞아 있어 관련 없는 정보를 가능한
    한 적게 담아야 한다는 착상.**
- 셋째 것이 왜 중요한가 — **긴 맥락 구절을 LLM에 먹이는 데 결부된 비용 때문에 중요하다. 게다가
  맥락 구절이 너무 길면 LLM은 흔히 그 맥락을, 특히 맥락 구절 중간에 제공된 정보를 활용하는 데 덜
  효과적이다(Liu et al., 2023)** (3절, p.152).[^es2024-ragas] 그 실측은
  [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md)에 있다.

## 그 셋을 실제로 계산하는 절차

- 공통 전제 — **우리 구현과 실험에서 모든 프롬프트는 OpenAI API로 이용 가능한
  `gpt-3.5-turbo-16k` 모델로 평가된다** (3절, p.152).[^es2024-ragas]
- ① 충실성 — **답 `a_s(q)`는 답에서 이뤄진 주장(claim)들이 맥락에서 추론될 수 있으면 맥락
  `c(q)`에 충실하다. 이를 추정하려고 먼저 LLM으로 진술 집합 `S(a_s(q))`를 뽑는다. 이 단계의 목적은
  긴 문장을 더 짧고 초점이 맞은 단언으로 분해하는 것이다** (3절, p.152).[^es2024-ragas] 그다음
  **`S(a_s(q))`의 각 진술 `s_i`에 대해 LLM이 검증 함수 `v(s_i, c(q))`로 그것이 `c(q)`에서 추론될
  수 있는지 판정한다** (3절, p.152).[^es2024-ragas] 최종 점수는 이렇게 계산된다 (3절,
  p.152):[^es2024-ragas]

  ```math
  F = \frac{|V|}{|S|}
  ```

  **`|V|`는 LLM에 따라 지지된 진술의 수, `|S|`는 `S(a_s(q))`의 전체 진술 수다.**
  - 검증 프롬프트의 원문이다 (3절, p.152):[^es2024-ragas]

    ```text
    Consider the given context and following statements, then determine whether they
    are supported by the information present in the context. Provide a brief explana-
    tion for each statement before arriving at the verdict (Yes/No). Provide a final
    verdict for each statement in order at the end in the given format. Do not deviate
    from the specified format.
    statement: [statement 1]
    ...
    statement: [statement n]
    ```

- ② 답 관련성 — **주어진 답 `a_s(q)`로부터 LLM에게 그 답에 근거한 잠재 질문 `q_i`를 `n`개
  생성하게 한다. 그다음 `text-embedding-ada-002` 모델로 모든 질문의 임베딩을 얻고, 각 `q_i`에
  대해 원 질문 `q`와의 유사도 `sim(q, q_i)`를 대응 임베딩 사이의 코사인으로 계산한다** (3절,
  p.152).[^es2024-ragas] 점수는 그 평균이다 (3절, p.152, 식 (1)):[^es2024-ragas]

  ```math
  AR = \frac{1}{n}\sum_{i=1}^{n} \mathrm{sim}(q, q_i)
  ```

  - 이 지표가 재지 않는 것 — **답 관련성의 평가는 사실성(factuality)을 고려하지 않고, 답이
    불완전하거나 중복 정보를 담은 경우를 벌한다** (3절, p.152).[^es2024-ragas]
- ③ 맥락 관련성 — **질문 `q`와 그 맥락 `c(q)`가 주어지면 LLM이 `q`에 답하는 데 결정적인 문장의
  부분집합 `S_ext`를 `c(q)`에서 뽑는다** (3절, p.153).[^es2024-ragas] 점수는 이렇게 계산된다
  (3절, p.153, 식 (2)):[^es2024-ragas]

  ```math
  CR = \frac{\text{number of extracted sentences}}{\text{total number of sentences in } c(q)}
  ```

  - 추출 프롬프트가 못 하게 막는 것 — **관련 문장이 없거나 주어진 맥락에서 질문에 답할 수 없다고
    믿으면 "Insufficient Information" 구절을 돌려주라. 후보 문장을 뽑는 동안 주어진 맥락의 문장에
    어떤 변경도 가하는 것이 허용되지 않는다** (3절, p.153).[^es2024-ragas]

## 사람과 얼마나 맞는가

- 무엇으로 쟀는가 — **제안한 틀을 평가하려면 사람 판단으로 주석된 질문–맥락–답 삼항이 필요하다.
  이 목적에 쓸 수 있는 공개 데이터셋을 알지 못해 WikiEval이라 부르는 새 데이터셋을 만들었다.
  2022년 시작 이후 일어난 사건을 다루는 위키백과 문서 50개를 골라, 각 문서의 도입부에 근거해 답할 수
  있는 질문을 ChatGPT에게 제안하게 했다** (4절, p.153).[^es2024-ragas] **모든 질문은 두 주석자가
  세 품질 차원에 대해 주석했다. 충실성과 맥락 관련성에서 두 주석자는 약 95%의 경우에, 답 관련성에서는
  약 90%의 경우에 일치했다** (4절, p.153).[^es2024-ragas]
- 결과다. 원문 표기를 그대로 옮겼다 (5절, p.154, Table 4 — 쌍 비교 정확도):[^es2024-ragas]

  | | Faith. | Ans. Rel. | Cont. Rel. |
  |---|---|---|---|
  | RAGAS | 0.95 | 0.78 | 0.70 |
  | GPT Score | 0.72 | 0.52 | 0.63 |
  | GPT Ranking | 0.54 | 0.40 | 0.52 |

  - 읽는 법 — **제안한 지표들이 두 기준선의 예측보다 사람 판단에 훨씬 가깝게 정렬된다. 충실성에서
    RAGAS 예측은 대체로 매우 정확하다. 답 관련성에서는 일치도가 낮은데 이는 대체로 두 후보 답의
    차이가 흔히 매우 미묘하다는 사실 때문이다. 맥락 관련성은 평가하기 가장 어려운 품질 차원임을
    발견했다 — 특히 긴 맥락에서 ChatGPT는 맥락에서 결정적인 문장을 고르는 과제에 자주 고전한다**
    (5절, p.154).[^es2024-ragas]
  - 두 기준선이 무엇인가 — **GPT Score는 ChatGPT에게 세 품질 차원에 0에서 10 사이의 점수를 매기게
    하고, GPT Ranking은 대신 선호하는 답이나 맥락을 고르게 한다. 두 경우 모두 프롬프트에 해당
    품질 지표의 정의를 포함한다** (5절, p.154).[^es2024-ragas] 곧 이 표가 재는 것은 "LLM으로 재는
    것"과 "그냥 점수를 물어보는 것"의 차이다 — 분해와 검증을 거치면 충실성에서 0.72가 0.95가 된다.

## 책의 지표 이름과 원전의 정의가 어긋나는 자리

- 책은 **컨텍스트 정밀도는 컨텍스트 관련성(context relevance)이라고도 불린다**고 적고, 그 정의를
  **검색된 모든 문서 중 질의에 관련 있는 것의 백분율**로 준다 (6장, p.264).[^huyen2025] 그러나
  이 원전의 맥락 관련성은 **문서가 아니라 문장을 세고**, 검색된 것 중 관련 있는 것의 비율이 아니라
  **맥락 전체 문장 중 답에 결정적인 문장의 비율**이다 (3절, p.153, 식 (2)).[^es2024-ragas] 두
  양은 세는 단위가 다르므로 같은 수가 아니다 — 한 문서가 통째로 관련 있어도 그 안 문장 대부분이
  불필요하면 컨텍스트 정밀도는 1, 맥락 관련성은 낮게 나온다.
- 책은 또 Ragas의 내장 기준을 **Faithfulness, answer relevance** 둘로 적지만 (3장, p.139,
  Table 3-3),[^huyen2025] 원전은 **세 국면**을 제안하며 맥락 관련성이 그 셋째다 (3절,
  p.152).[^es2024-ragas] 셋째가 검색기를 직접 재는 지표라는 점에서 이 페이지의 관심사에
  가장 가깝다.
- 어느 쪽도 틀린 것이 아니라 **이름이 겹치고 정의가 다른 경우**이므로, 도구가 낸 "context
  relevance"를 인용할 때 어느 정의인지 밝히지 않으면 비교가 성립하지 않는다. 도구마다 같은 이름의
  지표가 다른 것을 잰다는 일반 문제는
  [AI 판정자의 한계](../concepts/ai-judge-limitations.md)에 있다.

## 순위까지 보는 지표와 임베딩 자체의 평가

- 순위가 중요할 때 — **검색된 문서의 순위에 관심이 있다면, 예컨대 더 관련 있는 문서가 먼저 순위
  매겨져야 한다면, NDCG(normalized discounted cumulative gain)·MAP(Mean Average Precision)·
  MRR(Mean Reciprocal Rank) 같은 지표를 쓸 수 있다** (6장, p.265).[^huyen2025]
- 임베딩도 따로 재야 한다 — **의미 검색에서는 임베딩의 품질도 평가해야 한다. 3장에서 논의했듯
  임베딩은 독립적으로 평가될 수 있다 — 더 비슷한 문서가 더 가까운 임베딩을 가지면 좋다고 여겨진다.
  임베딩은 특정 과제에 대해 얼마나 잘 작동하는지로도 평가될 수 있다. MTEB 벤치마크(Muennighoff et
  al., 2023)는 검색·분류·군집화를 포함한 넓은 범위의 과제에 대해 임베딩을 평가한다** (6장,
  p.265).[^huyen2025] 그 임베딩 자체의 평가 방법은
  [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.
- 전체 시스템 안에서 — **검색기의 품질은 RAG 시스템 전체의 맥락에서도 평가되어야 한다. 궁극적으로
  검색기는 시스템이 고품질의 답을 생성하도록 도우면 좋은 것이다. 생성 모델의 출력을 평가하는 것은
  3장과 4장에서 논의된다** (6장, p.265).[^huyen2025][^karpukhin2020-dpr]
- 검색 전용 하네스 — **추가로 BEIR(Thakur et al., 2021)은 검색을 위한 평가 하네스다. 14개의 흔한
  검색 벤치마크에 걸쳐 검색 시스템을 지원한다** (6장, p.266).[^huyen2025]

## 지연과 비용

- 지연 (6장, p.265):[^huyen2025]

  > Since much of RAG latency comes from output generation, especially for long outputs, *the added
  > latency by query embedding generation and vector search might be minimal compared to the total
  > RAG latency.*

  - 그럼에도 — **의미 검색 시스템의 성능 약속이 추구할 만한지는 비용과 지연을 얼마나 우선하는가에,
    특히 질의 단계에서 얼마나 우선하는가에 달려 있다. 그렇더라도 더해지는 지연은 여전히 사용자 경험에
    영향을 줄 수 있다** (6장, p.265).[^huyen2025]
- 비용 — **또 다른 우려는 비용이다. 임베딩을 생성하는 데는 돈이 든다. 이는 데이터가 자주 바뀌어
  임베딩을 자주 재생성해야 할 때 특히 문제다. 매일 1억 개 문서에 대한 임베딩을 생성해야 한다고
  상상해 보라. 어떤 벡터 데이터베이스를 쓰느냐에 따라 벡터 저장과 벡터 검색 질의도 비쌀 수 있다. 어떤
  회사의 벡터 데이터베이스 지출이 모델 API 지출의 5분의 1이나 심지어 절반인 것을 보는 일은 드물지
  않다** (6장, p.265).[^huyen2025]
  - 원전이 잰 재색인의 무게 — **2,100만 구절의 조밀 임베딩을 계산하는 데 GPU 8장으로 약 8.8시간,
    그 위에 FAISS 색인을 짓는 데 단일 서버로 8.5시간이 걸린다** (5.4절,
    p.7).[^karpukhin2020-dpr] 데이터가 바뀌어 임베딩을 다시 만들어야 할 때 치르는 값이 이
    자리에서 실측된다. 문서 인코더를 얼리는 설계 결정이 왜 나오는지는
    [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md)에 있다.

## 두 갈래 비교표

원문 표기를 그대로 옮겼다 (6장, p.265, Table 6-2):[^huyen2025]

| | Term-based retrieval | Embedding-based retrieval |
|---|---|---|
| Querying speed | Much faster than embedding-based retrieval | Query embedding generation and vector search can be slow |
| Performance | Typically strong performance out of the box, but hard to improve · Can retrieve wrong documents due to term ambiguity | Can outperform term-based retrieval with finetuning · Allows for the use of more natural queries, as it focuses on semantics instead of terms |
| Cost | Much cheaper than embedding-based retrieval | Embedding, vector storage, and vector search solutions can be expensive |

## 색인과 질의 사이의 맞바꿈

- 일반 원리 — **검색 시스템에서는 색인과 질의 사이에 어떤 맞바꿈을 할 수 있다. 색인이 더 상세할수록
  검색 과정은 더 정확해지지만 색인 과정은 더 느리고 메모리를 더 먹는다. 잠재 고객의 색인을 짓는다고
  상상해 보라. 더 많은 세부(이름·회사·이메일·전화·관심사)를 더하면 관련 있는 사람을 찾기 쉬워지지만
  짓는 데 더 오래 걸리고 저장 공간이 더 필요하다** (6장, p.266).[^huyen2025]
- 두 극단 — **일반적으로 HNSW 같은 상세한 색인은 높은 정확도와 빠른 질의 시간을 제공하지만 짓는 데
  상당한 시간과 메모리를 요구한다. 반대로 LSH 같은 더 단순한 색인은 만들기가 더 빠르고 메모리 집약도가
  덜하지만 질의가 더 느리고 덜 정확하다** (6장, p.266).[^huyen2025][^malkov2018-hnsw]
  - 그 "상당한 시간과 메모리"의 실측 — **2억 개 SIFT 부분집합에서 HNSW는 `M = 16`·
    `efConstruction = 500`에서 구축 5.6시간·최대 메모리 64GB, `efConstruction = 40`에서 구축
    42분·64GB인 반면, 곱 양자화 기반 Faiss는 12시간·30GB와 11시간·23.5GB다. HNSW가 RAM을
    유의미하게 더 요구하지만 훨씬 높은 정확도를 달성하면서 탐색 속도에서 큰 진전과 훨씬 빠른 색인
    구축을 제공한다** (5.4절, pp.10–11, Table 3).[^malkov2018-hnsw] 곧 "짓는 데 오래 걸린다"는 비교
    대상에 달려 있다 — 곱 양자화 계열보다는 오히려 빨리 지어지고, 메모리를 두 배 쓴다.
  - 메모리의 상한 — **색인의 통상 메모리 요구량은 (데이터 크기를 제외하고) 객체당 약
    60–450바이트다** (4.2.3절, p.8).[^malkov2018-hnsw]
  - 구축 시간을 줄이는 손잡이 — **구축 속도와 색인 품질의 맞바꿈은 `efConstruction` 파라미터로
    조절된다. 1천만 개 SIFT 데이터셋에서 `efConstruction = 100`이면 4X 2.4GHz 10코어 Xeon E5-4650
    v2 서버로 합리적 품질의 색인을 단 3분에 지을 수 있다. `efConstruction`을 더 높이면 성능은
    거의 늘지 않는 대신 구축 시간이 크게 길어진다** (4.1절, p.7, Figure 10).[^malkov2018-hnsw]
- 그 맞바꿈을 재는 네 지표 — **ANN-Benchmarks 웹사이트는 색인과 질의 사이의 맞바꿈을 고려한 네 가지
  주요 지표로 여러 데이터셋에서 서로 다른 ANN 알고리즘을 비교한다** (6장, p.266):[^huyen2025]
  - **재현율(Recall) — 알고리즘이 찾아낸 최근접 이웃의 비율.**
  - **초당 질의 수(Query per second, QPS) — 알고리즘이 초당 처리할 수 있는 질의 수. 트래픽이 많은
    애플리케이션에 결정적이다.**
  - **빌드 시간(Build time) — 색인을 짓는 데 걸리는 시간. 데이터가 바뀌어 색인을 자주 갱신해야 할
    때 특히 중요하다.**
  - **색인 크기(Index size) — 알고리즘이 만든 색인의 크기. 확장성과 저장 요건을 평가하는 데
    결정적이다.**
- 그 벤치마크가 원전에서 쓰인 방식 — **비교의 주요 부분은 인기 K-ANNS 벤치마크인 ann-benchmarks를
  시험대로 삼아 벡터 데이터셋에서 수행했다. 시험 시스템은 알고리즘의 파이썬 바인딩을 이용해 사전
  설정된 파라미터로 (초기 데이터셋에서 무작위 추출한) 질의 1,000개에 대해 K-ANN 탐색을 연속으로
  돌리고 재현율과 단일 탐색의 평균 시간을 출력한다** (5.2절, p.8).[^malkov2018-hnsw] 곧 이
  벤치마크는 재현율과 질의 시간의 곡선을 그리는 도구이며, 빌드 시간과 색인 크기는 원전이 별도
  실험으로 따로 잰다.

## 근사 탐색에서 재현율은 무엇의 비율인가

- 원전의 정의다 (1절, p.1):[^malkov2018-hnsw]

  > The quality of an inexact search (the recall) is defined as the ratio between the number of
  > found true nearest neighbors and K.

  이는 위의 컨텍스트 재현율(관련 문서 전체 대비 검색된 것의 비율)과 다른 양이다 — 근사 탐색의
  재현율은 **정확 해법이 냈을 답 `K`개 대비 근사 알고리즘이 실제로 찾아낸 참 최근접 이웃의
  비율**이며, 관련성 주석이 아니라 완전 탐색(brute force)의 결과가 정답이다. 그래서 원전의
  데이터셋 표에는 **완전 탐색 시간(BF time)이 열로 함께 실린다** (5.2절, p.9,
  Table 1).[^malkov2018-hnsw]
- 왜 이 개념이 필요해졌는가 — **정확한 탐색의 조건을 완화해 적은 수의 오류를 허용하는 근사 최근접
  이웃 탐색(K-ANNS) 개념이 "차원의 저주"를 넘기 위해 제안되었다** (1절,
  p.1).[^malkov2018-hnsw] 정확도를 포기한 대가를 재는 자가 재현율이다.
- 재현율에 따라 최적 설정이 갈린다 — **더 작은 `M`은 일반적으로 낮은 재현율·낮은 차원 데이터에서
  더 나은 결과를 내고, 더 큰 `M`은 높은 재현율·높은 차원 데이터에 낫다** (4.1절,
  p.6).[^malkov2018-hnsw] 곧 목표 재현율을 정하지 않고 알고리즘을 고를 수는 없다.
  파라미터의 전모는 [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.

## 무엇을 평가해야 하는가

- 저자의 요약 — **RAG 시스템의 품질은 구성 요소별로도, 종단 간으로도 평가되어야 한다. 그러려면 다음
  세 가지를 해야 한다** (6장, p.266):[^huyen2025]
  1. **검색 품질을 평가한다.**
  2. **최종 RAG 출력을 평가한다.**
  3. **(임베딩 기반 검색이라면) 임베딩을 평가한다.**

## 검색 솔루션을 고를 때

- 저자가 드는 핵심 질문들이다 (6장, p.272, 상자 "Evaluating Retrieval Solutions"):[^huyen2025]
  - **어떤 검색 기전을 지원하는가? 하이브리드 검색을 지원하는가?**
  - **벡터 데이터베이스라면 어떤 임베딩 모델과 벡터 검색 알고리즘을 지원하는가?**
  - **데이터 저장과 질의 트래픽 양쪽에서 얼마나 확장 가능한가? 우리 트래픽 패턴에 통하는가?**
  - **데이터를 색인하는 데 얼마나 걸리는가? 한 번에 대량으로(추가·삭제 같은) 얼마나 많은 데이터를
    처리할 수 있는가?**
  - **서로 다른 검색 알고리즘에 대한 질의 지연은 얼마인가?**
  - **관리형 해법이라면 가격 구조는 어떤가? 문서·벡터 부피에 근거하는가, 질의 부피에 근거하는가?**
- 목록의 경계 — **이 목록은 접근 제어·컴플라이언스·데이터 플레인과 컨트롤 플레인 분리 등 엔터프라이즈
  해법에 통상 결부되는 기능은 포함하지 않는다** (6장, p.272).[^huyen2025]
- 원전이 그 고르기를 아예 없애려 한 지점 — **이 접근의 강건성은 실무 응용에 매우 매력적인 강한
  특징이다. 알고리즘은 일반화된 거리 공간에 적용 가능하며 이 논문에서 시험한 모든 데이터셋에서
  최고 성능을 내므로, 특정 문제에 맞는 최선의 알고리즘을 복잡하게 고를 필요를 없앤다** (6절,
  p.11).[^malkov2018-hnsw] 그 근거로 저자들이 드는 것은 **데이터가 척도에 따라 서로 다른 유효
  차원을 갖는 복잡한 구조일 수 있다는 것**이다 — 예컨대 고차원 정육면체를 무작위로 채우는 곡선
  위의 점들은 큰 척도에서는 고차원이고 작은 척도에서는 저차원이다 (6절,
  p.11).[^malkov2018-hnsw]

## 이어지는 페이지

- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 비교되는 두 갈래 중 하나
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — 다른 하나
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 비교의 결론이 둘을 섞는
  쪽으로 가는 자리
- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 이 검색기가 놓이는 시스템
- [AI 판정자](../concepts/ai-as-a-judge.md) — 관련성 주석을 사람 대신 맡는 쪽
- [사실 일관성](../concepts/factual-consistency.md) — 검색 뒤 생성 쪽에서 재는 기준
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 여기 나온 HNSW·LSH의 구조
- [비교 평가의 난제](../concepts/comparative-evaluation-challenges.md) — 공개 리더보드가 RAG를
  대변하지 못하는 이유
- [사실 일관성](../concepts/factual-consistency.md) — 충실성이 재려는 것이 생성 쪽에서 다시
  나오는 자리

[^es2024-ragas]: Es et al. 2024, "RAGAs: Automated Evaluation of Retrieval Augmented Generation",
    EACL 2024 **System Demonstrations**, pp.150–158. 본 학회 트랙이 아니라 시연 트랙이므로
    심사가 가볍다 — 이 페이지의 claim은 그 조건에서 읽는다. 쪽 번호는 학회 논문집 인쇄 쪽이다.
    이 페이지는 1절 Introduction·3절 Evaluation Strategies·4절 The WikiEval Dataset·5절
    Experiments를 담았다. 2절 Related Work·5.1절 Reproducibility·6절 Python API·8절 Limitations은
    [AI 판정자](../concepts/ai-as-a-judge.md)와
    [AI 판정자의 한계](../concepts/ai-judge-limitations.md)가 담는다. Table 4는 원문 표기를
    그대로 옮겼고 Table 1·2·3(WikiEval 예시)과 Figure 1(JSON 형식 유무별 점수 일관성 산점도,
    p.155)은 옮기지 않았다. 프롬프트는 원문 표기를 그대로 옮겼으나 원문이 프롬프트마다 붙인
    시연 예시(demonstration)는 논문 본문에도 실려 있지 않다(3절 각주 3).
    Liu et al.(2023)은 이 KB에 원전이 있다. BERTScore·BARTScore·MoverScore·GPTScore·
    SelfCheckGPT·llama-index·Langchain은 es2024-ragas를 통한 전언이다.

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Comparing retrieval
    algorithms" 절(pp.264–266)과 상자 "Evaluating Retrieval Solutions"(p.272)를 담았다. Table 6-2는
    원문 표기를 그대로 옮기되 원문이 한 칸 안에서 줄을 나눈 항목은 가운뎃점으로 이었다. 이 절에는
    도판이 없다. MTEB(Muennighoff et al., 2023)·BEIR(Thakur et al., 2021)·ANN-Benchmarks 웹사이트는
    huyen2025를 통한 전언이다.

[^karpukhin2020-dpr]: Karpukhin et al. 2020, "Dense Passage Retrieval for Open-Domain Question
    Answering", EMNLP 2020 (논문 13쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다. 이 페이지는 1절
    Introduction·2절 Background·4.2절 Question Answering Datasets·5절 서두·5.1절 Main Results·
    5.4절 Run-time Efficiency·6.2절 Results·부록 C를 담았다. Table 2·5·6은 옮기지 않았고 본문이
    서술한 수치만 담았다. BM25(Robertson and Zaragoza, 2009)·루씬·FAISS(Johnson et al., 2017)는
    karpukhin2020-dpr을 통한 전언이다.

[^malkov2018-hnsw]: Malkov and Yashunin 2018, "Efficient and Robust Approximate Nearest Neighbor
    Search Using Hierarchical Navigable Small World Graphs", IEEE TPAMI 42(4):824–836. 페이월이라
    오픈액세스 정본인 arXiv:1603.09320 v4(13쪽)를 스냅샷했고 쪽 번호는 그 PDF의 쪽이다. 이
    페이지는 1절 Introduction·4.1절 Influence of the construction parameters·4.2.3절 Memory
    cost·5.2절 Comparison in Euclid spaces·5.4절 Comparison with product quantization based
    algorithms·6절 Discussion을 담았다. Table 1·3과 Figure 10은 옮기지 않았고 본문이 서술한
    수치만 담았다. ann-benchmarks·Faiss·SIFT 데이터셋(Jegou et al.)은 malkov2018-hnsw를 통한
    전언이다.

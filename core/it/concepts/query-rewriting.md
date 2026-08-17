---
type: concept
title: 쿼리 재작성
description: 대화 맥락 없이는 뜻이 서지 않는 질의를 홀로 서는 질의로 고쳐 쓰는 전술 — 재구성·정규화·확장이라는 다른 이름들, 전통적 검색 엔진의 휴리스틱과 AI 애플리케이션의 프롬프트가 갈리는 자리, 신원 해소가 끼어들 때 재작성 모델이 환각하는 대신 못 푼다고 말해야 하는 이유, 질의를 다시 쓰는 대신 질의가 부를 법한 가짜 문서를 지어 그 임베딩으로 검색하는 HyDE의 기제와 그 수치·한계, 그리고 사용자 질의가 아니라 모델이 지금 쓰고 있는 문장을 질의로 바꿔야 할 때의 세 방법 — 저확신 토큰 마스킹·그 자리를 겨냥한 질문 생성·자기 어텐션 상위 토큰 추출
generated: { by: "claude-opus-5", at: "2026-08-17T15:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: gao2023-hyde, resource: /it/sources/gao2023-hyde.md }
  - { id: jiang2023-flare, resource: /it/sources/jiang2023-flare.md }
  - { id: su2024-dragin, resource: /it/sources/su2024-dragin.md }
---

# 쿼리 재작성

- [이름들](#이름들)
- [무엇이 문제인가](#무엇이-문제인가)
- [누가 다시 쓰는가](#누가-다시-쓰는가)
- [신원 해소가 끼어들 때](#신원-해소가-끼어들-때)
- [질의 대신 가짜 문서를 쓰는 길 — HyDE](#질의-대신-가짜-문서를-쓰는-길--hyde)
- [무엇이 왜 통하는가](#무엇이-왜-통하는가)
- [원전이 잰 수치](#원전이-잰-수치)
- [부품을 갈아 끼웠을 때](#부품을-갈아-끼웠을-때)
- [원전이 밝힌 조건과 한계](#원전이-밝힌-조건과-한계)
- [이 페이지의 두 전술은 다른 문제를 푼다](#이-페이지의-두-전술은-다른-문제를-푼다)
- [질의를 쓰는 주체가 사용자가 아닐 때](#질의를-쓰는-주체가-사용자가-아닐-때)
- [생성 중 질의 형성의 세 방법](#생성-중-질의-형성의-세-방법)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **앞 대화에 기대야만 뜻이 통하는 질의를 어떻게 검색 가능한 질의로 만드는가.**

## 이름들

- **쿼리 재작성(query rewriting)은 쿼리 재구성(query reformulation)·쿼리 정규화(query
  normalization), 때로는 쿼리 확장(query expansion)으로도 알려져 있다** (6장,
  p.270).[^huyen2025]

## 무엇이 문제인가

- 저자가 든 대화다 (6장, p.270):[^huyen2025]

  > *User*: When was the last time John Doe bought something from us?
  > *AI*: John last bought a Fruity Fedora hat from us two weeks ago, on January 3, 2030.
  > *User*: How about Emily Doe?

- 진단과 처방 — **마지막 질문 "How about Emily Doe?"는 맥락 없이는 모호하다. 이 질의를 그대로 써서
  문서를 검색하면 무관한 결과를 얻을 가능성이 높다. 사용자가 실제로 묻고 있는 것을 반영하도록 이
  질의를 다시 써야 한다. 새 질의는 그 자체로 뜻이 통해야 한다. 이 경우 질의는 "When was the last
  time Emily Doe bought something from us?"로 다시 쓰여야 한다** (6장, p.270).[^huyen2025]

## 누가 다시 쓰는가

- 범위와 두 갈래 — **저자는 쿼리 재작성을 RAG 절에 넣었지만 쿼리 재작성은 RAG에 고유하지 않다.
  전통적 검색 엔진에서 쿼리 재작성은 흔히 휴리스틱을 써서 이뤄진다. AI 애플리케이션에서 쿼리 재작성은
  다른 AI 모델을 써서, "Given the following conversation, rewrite the last user input to reflect
  what the user is actually asking"와 비슷한 프롬프트로 이뤄질 수도 있다** (6장,
  p.270).[^huyen2025]
- 도판이 보인 것 — **그 프롬프트를 써서 ChatGPT가 질의를 다시 쓴 결과가 앞의 대화를 넣었을 때
  "When was the last time Emily Doe bought something from us?"였다** (6장, p.270, Figure
  6-4).[^huyen2025]

## 신원 해소가 끼어들 때

- 어려워지는 지점 — **쿼리 재작성은 복잡해질 수 있는데, 특히 신원 해소(identity resolution)를 하거나
  다른 지식을 넣어야 할 때 그렇다. 예컨대 사용자가 "How about his wife?"라고 물으면 먼저 그의 아내가
  누구인지 알아내려고 데이터베이스에 질의해야 한다** (6장, p.270).[^huyen2025]
- 정보가 없을 때의 규정 — **그 정보를 갖고 있지 않다면, 재작성 모델은 환각해서 틀린 답으로 이어지는
  대신 이 질의를 풀 수 없다는 것을 인정해야 한다** (6장, p.270).[^huyen2025]

## 질의 대신 가짜 문서를 쓰는 길 — HyDE

- 무엇을 하는가. 초록의 원 표기다 (초록, p.1762):[^gao2023-hyde]

  > Given a query, HyDE first zero-shot prompts an instruction-following language model (e.g.,
  > InstructGPT) to generate a hypothetical document. The document captures relevance patterns but
  > is "fake" and may contain hallucinations. Then, an unsupervised contrastively learned encoder
  > (e.g., Contriever) encodes the document into an embedding vector.

- 그다음이 검색이다 — **이 벡터는 코퍼스 임베딩 공간 안의 한 이웃을 지목하며, 거기서 벡터 유사도에
  근거해 비슷한 실제 문서들이 검색된다. 이 둘째 단계가 생성된 문서를 실제 코퍼스에 접지시키고,
  인코더의 조밀 병목이 환각을 걸러 낸다** (초록, p.1762).[^gao2023-hyde]
- 어떤 문제를 푸는 것인가 — **조밀 검색이 과제·언어를 가로질러 효과적이고 효율적임이 밝혀졌지만,
  관련성 라벨이 전혀 없을 때 효과적인 완전 zero-shot 조밀 검색 시스템을 만드는 것은 여전히
  어렵다. 이 논문은 zero-shot 학습과 관련성 인코딩의 어려움을 인정하고, 대신 가설 문서
  임베딩(Hypothetical Document Embeddings, HyDE)을 경유하기를 제안한다** (초록,
  p.1762).[^gao2023-hyde]
- 실제 지시문 — **`g`를 써서 질의를 "가설" 문서로 사상하는데, `INST`를 "write a paragraph that
  answers the question"(또는 유사한 프롬프트)으로 두고 `g`에서 표집한다** (3.2절,
  p.1765).[^gao2023-hyde] 원전의 도판이 보인 지시문 셋은 **"write a passage to answer the
  question"·"write a scientific paper passage to answer the question"·"write a passage in Korean
  to answer the question in detail"**이다 (1절, p.1763, Figure 1).[^gao2023-hyde] 곧 지시문이
  데이터셋마다 다르며 **비슷한 구조를 공유하되 생성될 가설 문서의 정확한 형태를 조절하는 다른
  프롬프트를 쓴다** (4.1절, p.1766).[^gao2023-hyde]
- 여러 번 표집해 평균한다 — 원전은 질의 벡터를 **`g`에서 문서 `N`개를 표집해 각각을 인코더 `f`로
  인코딩한 뒤 평균**으로 추정하고, **질의 자신도 하나의 가설로 포함해 `N + 1`개로 나누는 형태도
  함께 쓴다** (3.2절, 식 (6)–(8), p.1766).[^gao2023-hyde]

## 무엇이 왜 통하는가

- 저자들이 대는 기제 — **여기서 우리는 관련성 모델링을 표현 학습 모델에서, 유의미하게 더 쉽고
  자연스럽고 효과적으로 일반화하는 NLG 모델로 떠넘긴다. 예시를 생성하는 것이 관련성 점수의 명시적
  모델링을 대신한다** (3.2절, p.1765).[^gao2023-hyde]
- 환각이 문제가 되지 않는 이유 — **생성된 문서가 실제가 아님을 강조한다. 사실 그것은 사실적으로
  접지되지 않았을 가능성이 높고 환각을 겪는다. 우리는 그 "가짜" 문서가 관련성 패턴을 잡기만
  하면 된다** (3.2절, p.1765).[^gao2023-hyde] 그래서 **인코더 함수 `f`는 여분의 세부를 걸러 내는
  손실 압축기 노릇을 하며, 가설 벡터를 실제 코퍼스와 실제 문서에 "접지"시킨다** (3.2절,
  p.1766).[^gao2023-hyde]
- 무엇이 사라지는가 — **제안한 HyDE 인수분해에서는 질의–문서 유사도 점수가 더 이상 명시적으로
  모델링되거나 계산되지 않는다. 대신 검색 과제가 두 과제(NLU와 NLG)로 던져진다** (1절,
  p.1763).[^gao2023-hyde] 그리고 **HyDE를 만드는 데는 지도가 필요 없고 이 작업에서 새로 훈련된
  모델은 없다 — 생성 모델과 대조 인코더 양쪽이 어떤 적응이나 수정도 없이 "상자에서 꺼낸 그대로"
  쓰인다** (1절, p.1763).[^gao2023-hyde]

## 원전이 잰 수치

- 웹 검색. 원문 표기를 그대로 옮겼다 (4.2절, p.1767, Table 1 발췌):[^gao2023-hyde]

  | System | DL19 mAP | DL19 nDCG@10 | DL19 Recall@1k | DL20 mAP | DL20 nDCG@10 | DL20 Recall@1k |
  |---|---|---|---|---|---|---|
  | BM25 (비지도) | 30.1 | 50.6 | 75.0 | 28.6 | 48.0 | 78.6 |
  | Contriever (비지도) | 24.0 | 44.5 | 74.6 | 24.0 | 42.1 | 75.4 |
  | HyDE (비지도) | 41.8 | 61.3 | 88.0 | 38.2 | 57.9 | 84.4 |
  | Contriever-ft (지도) | 41.7 | 62.1 | 83.6 | 43.6 | 63.2 | 85.8 |

  - 읽는 법 — **HyDE는 정밀도 지향 지표와 재현율 지표 양쪽에서 Contriever에 상당한 개선을
    가져온다. 비지도 Contriever는 어휘 기반 BM25에 뒤질 수 있지만, HyDE는 BM25를 큰 차이로
    앞선다** (4.2절, p.1767).[^gao2023-hyde] 두 번째 줄과 세 번째 줄의 차이는 **질의 벡터를 어떻게
    만드는가 하나뿐**이다 — **HyDE는 Contriever와 mContriever를 인코더로 쓰므로 그것들과 정확히
    같은 임베딩 공간을 공유한다** (4.1절, p.1766).[^gao2023-hyde]
  - 지도 모델과의 관계 — **TREC DL19에서 HyDE는 Contriever-ft와 비슷한 mAP·nDCG@10과 최고
    Recall@1k를 보인다. DL20에서는 Contriever-ft보다 mAP·nDCG@10이 약 10% 낮지만 Recall@1k는
    비슷하다** (4.2절, p.1767).[^gao2023-hyde]
- 저자원 과제와 다국어 — **BEIR의 저자원 과제 선별에서 HyDE는 nDCG@10과 Recall@100 양쪽에서
  Contriever에 전방위로 상당한 개선을 가져온다. HyDE가 BM25에 지는 데이터셋은 TREC-COVID 하나뿐이고
  nDCG@10에서 아주 근소한 차이인데, 비교하자면 밑에 깔린 Contriever 단독은 50% 넘게 뒤진다**
  (4.3절, p.1768).[^gao2023-hyde] 다국어에서는 **HyDE가 mContriever 모델을 개선하고 MS MARCO로
  파인 튜닝해 전이한 비-Contriever 모델들을 앞설 수 있지만, 파인 튜닝된 mContriever-ft와는 격차가
  관측된다** (4.4절, p.1768).[^gao2023-hyde]

## 부품을 갈아 끼웠을 때

- 생성 모델 — **다른 지시 따르기 언어 모델(520억 파라미터 Cohere, 110억 파라미터 FLAN-T5-xxl)로
  바꿔도 일반적으로 모든 모델이 비지도 Contriever에 개선을 가져오며, 더 큰 모델이 더 큰 개선을
  가져온다** (5.1절, p.1768, Table 4).[^gao2023-hyde]
- 지시를 못 따르는 기저 모델 — **인간 의도에 정렬되도록 훈련되지 않아 지시를 잘 따르지 않는 기저
  GPT-3에 3-shot 인컨텍스트 학습을 붙여 보면, few-shot 모델은 덜 안정적으로 수행한다 — Scifact에는
  작은 개선을 가져오지만 FiQA와 DBPedia에서는 InstructGPT를 앞설 수 있다** (5.2절,
  p.1769, Table 5).[^gao2023-hyde]
- 파인 튜닝된 인코더 위에서 — **먼저 강조할 것은 파인 튜닝된 인코더와 HyDE를 쓰는 것이 의도된
  용법이 아니라는 점이다. 이 접근은 관련성 라벨이 전혀 없는 경우를 위해 특별히 설계되었다. 그럼에도
  HyDE는 Contriever-ft와 GTR-XL 양쪽에 여전히 개선을 가져올 수 있으며, GTR-XL에서는 개선이 더
  작다 — 짐작건대 문서–문서 유사도를 명시적으로 학습하도록 대조 사전 훈련되지 않았기 때문이다**
  (5.3절, p.1769, Table 6).[^gao2023-hyde] #hypothesis
- 왜 통하는지의 시각화 — **T-SNE로 Contriever의 임베딩 공간을 그리면 HyDE가 만든 벡터가 원래 질의
  벡터보다 관련 문서 벡터의 군집에 더 가깝다** (5.4절, p.1769, Figure 3).[^gao2023-hyde]

## 원전이 밝힌 조건과 한계

- 지연과 처리량 — **HyDE는 LLM의 실시간 생성에 의존하므로 높은 처리량이나 낮은 지연을 요구하는
  과제에는 적합하지 않을 수 있다** (Limitations, p.1769).[^gao2023-hyde] 이 페이지의 다른 전술과
  같은 대가다 — 검색 앞에 모델 호출이 하나 더 붙는다.
- 편향 — **동시대 대부분의 LLM과 마찬가지로 HyDE는 생성에서 특정 내용을 선호해 최종 검색 결과를
  편향시킬 수 있다** (Limitations, p.1769).[^gao2023-hyde]
- 저자들이 스스로 그은 수명 — **HyDE는 검색 시스템의 전 수명에 걸쳐 유용한 것은 아니다. 검색
  시스템을 짓기 시작하는 맨 처음에 HyDE로 질의를 처리하는 것은 파인 튜닝된 모델에 견줄 만한 성능을
  제공하는데, 다른 어떤 관련성 없는(relevance-free) 모델도 그럴 수 없다. 검색 로그가 자라고 관련성
  데이터가 쌓이면 지도 조밀 검색기를 점차 훈련해 내보낼 수 있다. 조밀 검색기가 더 유능해지면
  "인도메인" 질의를 맡고, HyDE는 새롭고 예상치 못한, 떠오르는 질의에 여전히 유용할 수 있다**
  (6절, p.1769).[^gao2023-hyde]
- 성능 차이의 원인을 저자들이 지시문에 돌리는 자리 — **Contriever-ft가 FiQA와 DBPedia에서 사소하지
  않은 성능 우위를 보인다. 이 차이는 지시문의 미명세(under-specification)에 돌릴 수 있다고 보며,
  더 정교한 프롬프트가 도움이 될 수 있다** (4.3절, p.1768).[^gao2023-hyde] #hypothesis

## 이 페이지의 두 전술은 다른 문제를 푼다

- 책의 쿼리 재작성이 푸는 것은 **대화 맥락 없이는 뜻이 서지 않는 질의**이고 (6장,
  p.270),[^huyen2025] HyDE가 푸는 것은 **관련성 라벨이 없는 새 도메인에서 조밀 검색기를 세우는
  일**이다 (초록, p.1762).[^gao2023-hyde] 둘은 질의 쪽을 손본다는 자리를 공유하지만 같은 문제의
  두 해법이 아니다 — 앞의 것은 질의를 홀로 서게 만들고, 뒤의 것은 질의를 아예 **문서 공간의 한
  점으로 바꿔** 질의–문서 비교 자체를 문서–문서 비교로 대체한다.
- 그래서 책이 든 이름 중 **쿼리 확장(query expansion)**이 HyDE에 가장 가깝지만 그것도 정확하지는
  않다 — 확장은 원 질의에 항을 보태는 것인 반면 HyDE는 원 질의를 (선택적으로만 남기고) 생성 문서로
  갈아 끼운다.
- 둘의 공통점 하나는 **입력이 사용자의 발화**라는 것이다. 아래 두 절은 입력이 아예 다른 셋째
  부류를 다룬다 — 질의를 만들 재료가 사용자의 발화가 아니라 **모델이 방금 쓴 텍스트**인 경우다.

## 질의를 쓰는 주체가 사용자가 아닐 때

- 위의 두 전술은 모두 **사용자가 던진 질의**를 입력으로 받는다. 생성 도중에 검색하는 설계에서는
  입력이 다르다 — 질의를 만들 재료가 **모델이 방금 쓴 텍스트**다. 그래서 "무엇으로 검색할
  것인가"가 독립된 설계 축이 된다.
- 왜 직전 텍스트를 그대로 쓰면 안 되는가 — **앞서 생성된 토큰을 질의로 쓰는 것은 LM이 미래에
  생성하려는 것을 반영하지 못할 수 있다** (4절, p.6).[^jiang2023-flare] 그래서 한 원전은 **다음**
  문장을 임시로 생성해 그것을 질의 재료로 삼고, 직전 문장과의 정면 비교에서 2WikiMultihopQA EM이
  39.0 대 48.8로 갈린다 (6.2절, p.8, Table 3).[^jiang2023-flare]
- 그 임시 문장을 그대로 쓸 수도 없다 — **그 안에 담긴 오류가 그대로 전파될 위험이 있다. 예컨대 LM이
  "Joe Biden attended the University of Delaware"라는 옳은 사실 대신 "Joe Biden attended the
  University of Pennsylvania"를 생성하면, 이 잘못된 문장을 질의로 쓰는 것이 오도하는 정보를 검색할
  수 있다** (3.2.2절, p.4).[^jiang2023-flare] 곧 이 자리의 재작성은 문체 다듬기가 아니라 **오류
  격리**다.

## 생성 중 질의 형성의 세 방법

- ① 저확신 토큰을 가린다 — **첫째 방법은 임시 문장에서 확률이 문턱 `β ∈ [0, 1]` 아래인 저확신
  토큰을 가려 내며, `β`가 클수록 더 공격적으로 가린다. 이는 검색 정확도를 높이기 위해 문장에서 올
  수 있는 방해 요소를 제거한다** (3.2.2절, p.5).[^jiang2023-flare] 문장 전체를 그대로 쓰는
  `β = 0`이 마스킹보다 나쁘다 (6.2절, p.9, Table 5).[^jiang2023-flare]
- ② 그 자리를 겨냥한 질문을 만든다 — **다른 방법은 임시 문장의 저확신 구간을 겨냥한 명시적 질문을
  생성하는 것이다. 예컨대 모델이 "the University of Pennsylvania"에 확신이 없으면 "Which university
  did Joe Biden attend?" 같은 질문이 관련 정보를 검색하는 데 도움이 될 수 있다** (3.2.2절,
  p.5).[^jiang2023-flare] 앞선 접근이 하위 질문을 예시에 손으로 끼워 넣어 과제별 주석 노력을
  요구한 데 반해, 여기서는 **추가 주석 없이 저확신 구간에 대한 질문을 생성하는 보편적 접근**을 쓴다
  (3.2.2절, p.5).[^jiang2023-flare] 두 방법의 성능은 **비슷하며, 둘 다 정보 요구를 효과적으로
  반영할 수 있음을 가리킨다** (6.2절, p.9, Table 6).[^jiang2023-flare]
- ③ 문장이 아니라 맥락 전체에서 고른다 — **기존 동적 RAG 틀의 질의 형성 방법은 전부 LLM의 가장 최근
  문장이나 마지막 몇 토큰으로 범위를 좁힌다. 이 좁은 범위는 전체 맥락에 걸칠 수 있는 모델의 실시간
  정보 요구를 적절히 충족하지 못한다** (3.2절, p.4).[^su2024-dragin] 그래서 셋째 방법은
  **발동 위치의 토큰이 앞선 토큰 시퀀스에 준 어텐션 점수를 마지막 트랜스포머 층에서 추출해 내림차순
  정렬하고, 상위 `n`개 토큰에 해당하는 낱말을 원문의 원래 순서대로 배열해 질의를 만든다** (3.2절,
  p.4).[^su2024-dragin] 자기 어텐션이 **`t_i`를 생성하는 데 각 토큰이 얼마나 중요한지에 대한 모델
  자신의 평가**라는 것이 전제다 (3.2절, p.4).[^su2024-dragin]
- 셋을 같은 자리에서 비교한 값이 있다 — 발동 시점을 고정하고 질의 형성만 바꾸면 HotpotQA EM이
  **자기 어텐션 방식 0.314, 마스킹 방식 0.262, 전체 맥락 0.252, 직전 문장 0.255, 마지막 25토큰
  0.241**이다 (5.4절, p.8, Table 6).[^su2024-dragin] 두 관찰이 따라온다.
  - **전체 맥락을 질의로 쓰는 것이 최선이 아니다** — 저자들은 **전체 맥락 안의 잉여를 가리키는
    결과**로 읽는다 (5.4절, p.8).[^su2024-dragin] 곧 더 많은 재료가 더 좋은 질의를 만들지 않는다.
  - 마스킹 방식이 **베이스라인 중 둘째로 효과적**이다 (5.4절, p.8).[^su2024-dragin] 곧 위 ①의
    이득은 다른 원전의 측정에서도 재현된다.

## 이어지는 페이지

- [청킹 전략](../concepts/chunking-strategy.md) — 같은 절의 다른 검색 최적화 전술
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 〃
- [컨텍스트 증강 검색](../concepts/contextual-retrieval.md) — 질의가 아니라 문서 쪽을 고치는 짝
- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 이 전술이 놓이는 파이프라인
- [프롬프트 분해](../concepts/prompt-decomposition.md) — 다른 모델 호출을 하나 더 끼워 넣는 같은
  구조의 관행
- [AI의 확률적 성격](../concepts/probabilistic-nature-of-ai.md) — 재작성 모델이 환각할 때의 근거
- [에이전트 계획](../concepts/agent-planning.md) — 의도 분류가 같은 질문을 다루는 자리
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — HyDE가 질의 벡터만 갈아 끼우는
  그 파이프라인
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — nDCG·Recall이 정의되는 자리
- [어휘 기반 검색](../concepts/term-based-retrieval.md) — 생성 중 검색이 실제로 쓰는 검색기

[^jiang2023-flare]: Jiang et al. 2023, "Active Retrieval Augmented Generation", EMNLP 2023
    (인쇄 쪽 7969–7992). 쪽 번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.7969). 이 페이지는
    3.2.2절 Confidence-based Query Formulation과 4절의 직전 맥락 질의 비판, 6.2절 Ablation Study의
    질의 형성 비교만 담았다 — 이 원전의 본체(능동 검색의 발동 규칙)는
    [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md)이 담는다. Table 3·5·6은
    본문이 서술한 수치만 담았고 표 자체는 옮기지 않았다. Figure 3(암묵·명시 질의 형성 도식, p.5)은
    옮기지 않았고 그 안의 예시 문자열과 본문 서술만 담았다.
    self-ask(Press et al., 2022)·HyDE 계열(Gao et al., 2022)·gpt-3.5-turbo는 jiang2023-flare를
    통한 전언이며, HyDE는 이 KB에 원전이 있다.

[^su2024-dragin]: Su et al. 2024, "DRAGIN: Dynamic Retrieval Augmented Generation based on the
    Real-time Information Needs of Large Language Models", ACL 2024 (인쇄 쪽 12991–13013). 쪽
    번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.12991). **표제 표기 차이** — 스냅샷 PDF의 표제는
    "Real-time"이 빠진 채 인쇄돼 있고 소스 메타의 제목은 ACL Anthology 등록 제목을 따랐다.
    이 페이지는 3.2절 Query Formulation based on Self-attention과 5.4절 Query Formulation만
    담았다 — 이 원전의 본체는
    [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md)이 담는다. Table 6의 수치는
    표 형태로 옮기지 않고 본문 서술로만 담았다.
    FLARE(Jiang et al., 2023)는 이 KB에 원전이 있다. IRCoT(Trivedi et al., 2022)·
    RETRO(Borgeaud et al., 2022)·IC-RALM(Ram et al., 2023)은 su2024-dragin을 통한 전언이다.

[^gao2023-hyde]: Gao et al. 2023, "Precise Zero-Shot Dense Retrieval without Relevance Labels",
    ACL 2023, pp.1762–1777. 쪽 번호는 학회 논문집 인쇄 쪽이다. 이 페이지는 초록·1절
    Introduction·3.2절 HyDE·4절 Experiments(4.1–4.4)·5절 Analysis(5.1–5.4)·6절 Conclusion·
    Limitations를 담았다. 2절 Related Work와 3.1절 Preliminaries의 조밀 검색 형식화는 담지
    않았다. Table 1은 DL19·DL20 열의 네 행만 발췌해 옮겼고 Table 2·3·4·5·6은 본문이 서술한
    것만 담았다. Figure 1(HyDE 도식, p.1763)·Figure 2(InstructGPT 생성 예, p.1764)·
    Figure 3(T-SNE 산점도, p.1769)은 도판 자체를 옮기지 않고 그 안의 지시문 문자열과 본문이
    서술한 결론만 담았다. 식 (1)–(9) 중 (6)–(8)은 서술로만 옮겼다.
    InstructGPT(Ouyang et al., 2022)·Contriever(Izacard et al., 2021)·BEIR(Thakur et al., 2021)·
    Mr.TyDi(Zhang et al., 2021)·TREC DL19/20(Craswell et al., 2020; 2021)·GTR-XL(Ni et al., 2022)·
    FLAN-T5·Cohere command-xlarge는 gao2023-hyde를 통한 전언이다.

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Retrieval
    Optimization" 절 안의 "Query rewriting" 항목(p.270)을 담았다. Figure 6-4(ChatGPT가 질의를 다시
    쓰는 화면 갈무리, p.270)는 그 안의 프롬프트와 대화 문자열, 그리고 출력 문자열만 옮겼다. 대화 예의
    날짜(January 3, 2030)는 원문 표기 그대로다.

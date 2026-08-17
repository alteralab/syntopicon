---
type: concept
title: 어휘 기반 검색
description: 낱말이 겹치는 문서를 골라 순위를 매기는 검색 — 검색이 RAG보다 백 년 앞선다는 배치, 희소 대 조밀이라는 문헌의 구분을 저자가 어휘 대 임베딩으로 바꿔 부르는 이유, 용어 빈도와 역문서 빈도를 곱해 점수를 내는 TF-IDF와 문서 길이를 정규화한 BM25의 계보, 토큰화가 뜻을 부수는 자리, 그리고 조밀 검색 원전들이 BM25를 기준선으로 잰 수치와 어휘 갈래가 여전히 이기는 곳
generated: { by: "claude-opus-5", at: "2026-08-17T03:20:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: karpukhin2020-dpr, resource: /it/sources/karpukhin2020-dpr.md }
  - { id: lewis2020-rag, resource: /it/sources/lewis2020-rag.md }
---

# 어휘 기반 검색

- [검색은 RAG의 것이 아니다](#검색은-rag의-것이-아니다)
- [희소 대 조밀이라는 다른 구분](#희소-대-조밀이라는-다른-구분)
- [키워드로 찾을 때의 두 문제](#키워드로-찾을-때의-두-문제)
- [TF-IDF](#tf-idf)
- [역색인과 그 위의 실물](#역색인과-그-위의-실물)
- [BM25](#bm25)
- [원전이 잰 BM25의 자리](#원전이-잰-bm25의-자리)
- [어휘 갈래가 이기는 곳](#어휘-갈래가-이기는-곳)
- [토큰화가 뜻을 부수는 자리](#토큰화가-뜻을-부수는-자리)
- [n-그램 겹침으로 검색할 수 있는가](#n-그램-겹침으로-검색할-수-있는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **질의의 낱말을 담은 문서가 많을 때, 무엇을 먼저 줄 것인가.**

## 검색은 RAG의 것이 아니다

- 배치 — **검색은 RAG에 고유한 것이 아니다. 정보 검색은 백 년 된 착상이다. 그것은 검색 엔진·추천
  시스템·로그 분석 등의 뼈대다. 전통적 검색 시스템을 위해 개발된 많은 검색 알고리즘을 RAG에도 쓸 수
  있다** (6장, p.257).[^huyen2025]
  - 각주가 짚는 기원 — **정보 검색은 이르게는 1920년대에 필름에 저장된 문서를 검색하는 "통계
    기계"에 대한 에마누엘 골드베르크(Emanuel Goldberg)의 특허에 서술되었다. "The History of
    Information Retrieval Research"(Sanderson and Croft, *Proceedings of the IEEE*, 100: Special
    Centennial Issue, 2012년 4월)를 보라** (6장, p.257 각주 5).[^huyen2025]
- 저자가 범위를 긋는다 — **정보 검색은 큰 지원 산업을 가진 비옥한 연구 영역이라 몇 쪽 안에 충분히
  다뤄질 수 없다. 따라서 이 절은 큰 줄기만 다루며, 더 깊은 자료는 이 책의 GitHub 저장소를 보라**
  (6장, p.257).[^huyen2025]
- 용어에 대한 단서 — **검색(retrieval)은 통상 하나의 데이터베이스나 시스템에 한정되는 반면
  탐색(search)은 다양한 시스템에 걸친 검색을 수반한다. 이 장은 retrieval과 search를 서로 바꿔 쓴다**
  (6장, p.257).[^huyen2025]
- 검색의 핵심 — **핵심에서 검색은 주어진 질의에 대한 관련성(relevance)으로 문서의 순위를 매김으로써
  작동한다. 검색 알고리즘은 관련성 점수가 어떻게 계산되는가에 따라 달라진다. 저자는 두 가지 흔한
  검색 기전에서 시작한다: 어휘 기반 검색(term-based retrieval)과 임베딩 기반 검색(embedding-based
  retrieval)** (6장, p.257).[^huyen2025]

## 희소 대 조밀이라는 다른 구분

- 문헌의 구분과 이 책의 선택 — **문헌에서는 검색 알고리즘을 희소(sparse) 대 조밀(dense)로 나누는
  구분을 만날 수 있다. 그러나 이 책은 어휘 기반 대 임베딩 기반 범주화를 택했다** (6장,
  p.258, 상자 "Sparse Versus Dense Retrieval").[^huyen2025]
- 희소 쪽 — **희소 검색기는 희소 벡터(sparse vectors)를 써서 데이터를 표현한다. 희소 벡터는 값의
  대부분이 0인 벡터다. 어휘 기반 검색은 희소로 여겨진다 — 각 용어가 희소 원-핫 벡터(one-hot
  vector), 곧 어휘 안 그 용어의 색인에 대응하는 위치의 값 1 하나를 빼면 어디나 0인 벡터로 표현될 수
  있기 때문이다. 벡터의 크기는 어휘의 길이다** (6장, p.258).[^huyen2025]
  - 저자가 든 예 — **단순한 사전 `{"food": 0, "banana": 1, "slug": 2}`가 있으면 "food"·"banana"·
    "slug"의 원-핫 벡터는 각각 `[1, 0, 0]`·`[0, 1, 0]`·`[0, 0, 1]`이다** (6장,
    p.258).[^huyen2025]
- 조밀 쪽과 그 예외 — **조밀 검색기는 조밀 벡터(dense vectors)를 써서 데이터를 표현한다. 조밀
  벡터는 값의 다수가 0이 아닌 벡터다. 임베딩 기반 검색은 통상 조밀로 여겨진다 — 임베딩은 일반적으로
  조밀 벡터이기 때문이다. 그러나 희소 임베딩도 있다. 예컨대 SPLADE(Sparse Lexical and
  Expansion)(Formal et al., 2021)는 희소 임베딩으로 작동하는 검색 알고리즘이다. BERT가 생성한
  임베딩을 활용하되 정규화를 써서 임베딩 값 대부분을 0으로 민다. 그 희소성이 임베딩 연산을 더
  효율적으로 만든다** (6장, p.258).[^huyen2025]
- 저자가 구분을 바꾼 이유 — **희소 대 조밀이라는 구분은 SPLADE를 어휘 기반 알고리즘과 한데 묶게
  만드는데, SPLADE의 연산·강점·약점은 어휘 기반 검색보다 조밀 임베딩 검색의 그것에 훨씬 가깝다.
  어휘 기반 대 임베딩 기반 구분은 이 오분류를 피한다** (6장, p.258).[^huyen2025]
- 원전이 실제로 쓰는 어휘는 희소 대 조밀이다 (초록, p.1):[^karpukhin2020-dpr]

  > Open-domain question answering relies on efficient passage retrieval to select candidate
  > contexts, where traditional sparse vector space models, such as TF-IDF or BM25, are the de
  > facto method.

  저자들은 그 표현이 무엇인지도 명시한다 —
  **개방 도메인 QA의 검색은 보통 TF-IDF나 BM25로 구현되는데, 이는 역색인으로 키워드를 효율적으로
  일치시키며 질문과 맥락을 (가중치가 붙은) 고차원 희소 벡터로 표현하는 것으로 볼 수 있다** (1절,
  p.1).[^karpukhin2020-dpr] 곧 huyen2025가 갈아 끼운 "어휘 대 임베딩"과 원전의 "희소 대 조밀"은
  같은 두 갈래를 다르게 잘라 부르는 이름이며, 어느 쪽이 참인가의 문제가 아니라 SPLADE 같은 경계
  사례를 어디에 놓을 것인가의 문제다.

## 키워드로 찾을 때의 두 문제

- 가장 단순한 길 — **질의가 주어졌을 때 관련 문서를 찾는 가장 직설적인 방법은 키워드를 쓰는 것이다.
  어떤 사람들은 이 접근을 어휘 검색(lexical retrieval)이라 부른다. 예컨대 질의 "AI engineering"이
  주어지면 모델은 "AI engineering"을 담은 모든 문서를 검색한다** (6장, p.258).[^huyen2025]
- 첫째 문제와 그 휴리스틱 — **많은 문서가 주어진 용어를 담고 있을 수 있고 모델이 그것들을 전부
  맥락으로 포함할 컨텍스트 공간을 갖지 못할 수 있다. 하나의 휴리스틱은 그 용어를 가장 많이 담은
  문서를 포함하는 것이다. 가정은 어떤 용어가 문서에 더 많이 나타날수록 그 문서가 이 용어에 더 관련
  있다는 것이다. 어떤 용어가 문서에 나타나는 횟수를 용어 빈도(term frequency, TF)라 한다** (6장,
  p.258).[^huyen2025]
- 둘째 문제 — **프롬프트는 길고 많은 용어를 담을 수 있다. 어떤 것은 다른 것보다 더 중요하다. 예컨대
  프롬프트 "Easy-to-follow recipes for Vietnamese food to cook at home"은 아홉 개 용어를 담는다:
  *easy-to-follow, recipes, for, vietnamese, food, to, cook, at, home*. `for`나 `at`이 아니라
  *vietnamese*와 *recipes* 같은 더 정보량 있는 용어에 집중하고 싶다. 중요한 용어를 식별할 방법이
  필요하다** (6장, pp.258–259).[^huyen2025]
- 직관과 그 이름 — **직관은 어떤 용어를 담은 문서가 많을수록 그 용어는 덜 정보량이 있다는 것이다.
  "For"와 "at"은 대부분의 문서에 나타날 가능성이 높고, 따라서 덜 정보량이 있다. 그래서 어떤 용어의
  중요성은 그것이 나타나는 문서 수에 반비례한다. 이 지표를 역문서 빈도(inverse document frequency,
  IDF)라 한다. 어떤 용어의 IDF를 계산하려면 그 용어를 담은 문서를 모두 세고 전체 문서 수를 이 수로
  나눈다. 문서가 10개이고 그중 5개가 주어진 용어를 담으면 이 용어의 IDF는 10 / 5 = 2다. 어떤
  용어의 IDF가 높을수록 그것은 더 중요하다** (6장, p.259).[^huyen2025]

## TF-IDF

- 정의 — **TF-IDF는 이 두 지표, 곧 용어 빈도(TF)와 역문서 빈도(IDF)를 결합하는 알고리즘이다**
  (6장, p.259).[^huyen2025] 수학적으로 질의 `Q`에 대한 문서 `D`의 TF-IDF 점수는 이렇게 계산된다
  (6장, p.259):[^huyen2025]
  - **`t₁, t₂, …, t_q`를 질의 `Q` 안의 용어라 하자.**
  - **용어 `t`가 주어졌을 때 문서 `D` 안 이 용어의 용어 빈도는 `f(t, D)`다.**
  - **`N`을 전체 문서 수, `C(t)`를 `t`를 담은 문서 수라 하자. 용어 `t`의 IDF 값은
    `IDF(t) = log(N / C(t))`로 쓸 수 있다.**
  - **순진하게, `Q`에 대한 문서 `D`의 TF-IDF 점수는
    `Score(D, Q) = Σ_{i=1}^{q} IDF(t_i) × f(t_i, D)`로 정의된다.**

## 역색인과 그 위의 실물

- 두 실물 — **두 가지 흔한 어휘 기반 검색 해법은 엘라스틱서치와 BM25다. 루씬 위에 지어진
  엘라스틱서치(Shay Banon, 2010)는 역색인(inverted index)이라 불리는 자료 구조를 쓴다. 이는 용어에서
  그것을 담은 문서로 사상하는 사전이다. 이 사전은 어떤 용어가 주어졌을 때 문서를 빠르게 검색할 수
  있게 한다. 색인은 용어 빈도와 문서 수(얼마나 많은 문서가 이 용어를 담는가) 같은 추가 정보도 저장할
  수 있는데, 이는 TF-IDF 점수를 계산하는 데 유용하다** (6장, p.259).[^huyen2025] 그 자료 구조 자체는
  [전문 검색 색인](../concepts/full-text-search-indexes.md)이 담는다.
- 역색인을 단순화한 예다. 원문 표기를 그대로 옮겼다 (6장, p.259, Table 6-1):[^huyen2025]

  | Term | Document count | (Document index, term frequency) for all documents containing the term |
  |---|---|---|
  | banana | 2 | (10, 3), (5, 2) |
  | machine | 4 | (1, 5), (10, 1), (38, 9), (42, 5) |
  | learning | 3 | (1, 5), (38, 7), (42, 5) |
  | … | … | … |

- 역색인이 싸다는 것의 실측 — **2,100만 구절에 대해 루씬으로 역색인을 짓는 것은 훨씬 싸서 전부
  합쳐 30분 정도 걸린다. 같은 코퍼스에 대해 조밀 임베딩을 계산하는 데는 GPU 8장에서 약 8.8시간,
  그 위에 FAISS 색인을 짓는 데 단일 서버에서 8.5시간이 걸린다** (5.4절,
  p.7).[^karpukhin2020-dpr] 색인 구축 비용에서 두 갈래가 갈리는 배수가 이 자리에서 실측된다.

## BM25

- 이름과 계보 — **Okapi BM25는 Best Matching 알고리즘의 25번째 세대로, 1980년대에 Robertson et al.이
  개발했다. 그 채점기는 TF-IDF의 변형이다. 순진한 TF-IDF와 비교해 BM25는 용어 빈도 점수를 문서
  길이로 정규화한다. 더 긴 문서는 주어진 용어를 담을 가능성이 높고 더 높은 용어 빈도 값을 가질
  가능성이 높다** (6장, pp.259–260).[^huyen2025]
  - 각주가 가리키는 정본 — **BM25에 대해 더 배우고 싶다면 저자는 BM25 저자들의 논문
    "The Probabilistic Relevance Framework: BM25 and Beyond"(Robertson and Zaragoza, *Foundations
    and Trends in Information Retrieval* 3 No. 4, 2009)를 권한다** (6장, p.260 각주 6).[^huyen2025]
- 오늘의 위치 — **BM25와 그 변형(BM25+·BM25F)은 산업에서 여전히 널리 쓰이며, 임베딩 기반 검색 같은
  현대적이고 더 정교한 검색 알고리즘과 겨루는 만만찮은 기준선(baseline) 노릇을 한다** (6장,
  p.260).[^huyen2025][^karpukhin2020-dpr]
  - 각주의 한 마디 — **퍼플렉시티의 CEO 아라빈드 스리니바스(Aravind Srinivas)는 "BM25나 전문 검색을
    진짜로 개선하는 것은 어렵다"고 트윗했다** (6장, p.260 각주 7).[^huyen2025]

## 원전이 잰 BM25의 자리

- 기준선이 어떻게 세팅되었는가 — **루씬 구현을 썼고, BM25 파라미터 `b = 0.4`(문서 길이 정규화)와
  `k₁ = 0.9`(용어 빈도 스케일링)를 개발 집합으로 튜닝했다** (5절, p.5 각주
  9).[^karpukhin2020-dpr] 곧 원전의 BM25는 기본값 그대로가 아니라 튜닝된 기준선이다.
- 그 기준선이 낸 상위 20개 검색 정확도 (5.1절, p.5, Table 2):[^karpukhin2020-dpr]
  **Natural Questions 59.1 · TriviaQA 66.9 · WebQuestions 55.0 · CuratedTREC 70.9 · SQuAD 68.8.**
  조밀 쪽(DPR)은 SQuAD를 뺀 전부에서 이를 앞선다 — **`k`가 작을 때 격차가 특히 크다(예: Natural
  Questions 상위 20개 정확도 78.4% 대 59.1%)** (5.1절, p.5).[^karpukhin2020-dpr]
- 그러나 지지 않는 자리가 있다 — **DPR은 SQuAD에서 BM25에 진다(상위 20 기준 63.2 대 68.8).
  저자들이 추정하는 이유는 둘이다. 주석자가 구절을 본 뒤 질문을 써서 구절과 질문 사이 어휘 겹침이
  크고, 데이터가 500여 개 위키백과 문서에서만 수집되어 훈련 예시 분포가 극도로 편향돼 있다**
  (5.1절, p.5).[^karpukhin2020-dpr] 어휘 겹침이 클수록 낱말 일치가 유리하다는 것이 이 표의 읽는
  법이다.

## 어휘 갈래가 이기는 곳

- 사실 검증 과제 — **RAG의 조밀 검색기를 낱말 겹침 기반 BM25 검색기로 바꾸는 절제 실험에서,
  FEVER에서는 BM25가 가장 좋다 — FEVER의 주장이 개체 중심(entity-centric)이라 낱말 겹침 기반
  검색에 잘 맞기 때문일 것이다. 미분 가능한 검색은 다른 모든 과제, 특히 결정적인 개방 도메인 QA의
  결과를 개선한다** (4.5절, p.7, Table 6).[^lewis2020-rag] 곧 어휘 갈래가 이기는 조건은 데이터셋의
  성질(개체 중심·어휘 겹침이 큼)이지 알고리즘의 세대가 아니다.
- 드문 고유 표현 — **BM25 같은 어휘 일치 방법은 매우 선택적인 키워드와 구절에 민감한 반면 조밀
  검색기는 드물게 나타나는 두드러진 구절을 표현할 능력이 모자랄 수 있다** (부록 C,
  p.12).[^karpukhin2020-dpr] 저자들이 든 예에서 BM25는 "Thoros of Myr"라는 결정적 고유 표현을 잡아
  정답 구절을 가져오지만 DPR은 그러지 못한다 (부록 C, pp.12–13,
  Table 7).[^karpukhin2020-dpr]
- 어려운 음성 표본의 공급원 — 어휘 검색은 조밀 검색기의 경쟁자이면서 동시에 그 훈련 재료다.
  **DPR의 최선 모델은 BM25 점수가 높지만 답을 담지 않는 구절을 "어려운" 음성 표본으로 하나 섞어
  쓴다** (3.2절, p.3).[^karpukhin2020-dpr] 그 훈련법 자체는
  [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)에 있다.

## 토큰화가 뜻을 부수는 자리

- 저자가 건너뛴 과정 — **저자가 얼버무린 과정 하나는 토큰화(tokenization), 곧 질의를 개별 용어로
  쪼개는 과정이다. 가장 단순한 방법은 질의를 낱말로 쪼개고 각 낱말을 별개의 용어로 다루는 것이다.
  그러나 이는 여러 낱말로 된 용어가 개별 낱말로 부서져 원래 뜻을 잃게 만들 수 있다. 예컨대
  "hot dog"는 "hot"과 "dog"으로 쪼개질 것이다. 이런 일이 일어나면 어느 쪽도 원래 용어의 뜻을 갖지
  않는다. 이 문제를 완화하는 한 방법은 가장 흔한 n-그램을 용어로 다루는 것이다. 바이그램 "hot dog"이
  흔하다면 그것은 하나의 용어로 다뤄질 것이다** (6장, p.260).[^huyen2025]
- 그 밖의 전처리와 도구 — **추가로 모든 문자를 소문자로 바꾸고 구두점을 제거하고 불용어("the"·
  "and"·"is" 등)를 없애고 싶을 수 있다. 어휘 기반 검색 해법은 흔히 이것들을 자동으로 처리한다.
  NLTK(Natural Language Toolkit)·spaCy·스탠퍼드의 CoreNLP 같은 고전 NLP 패키지도 토큰화 기능을
  제공한다** (6장, p.260).[^huyen2025]

## n-그램 겹침으로 검색할 수 있는가

- 저자의 자문자답 — **4장은 두 텍스트 사이의 어휘 유사도를 n-그램 겹침의 정도로 재는 것을 논의한다.
  질의와의 n-그램 겹침의 정도에 근거해 문서를 검색할 수 있는가? 그렇다, 할 수 있다** (6장,
  p.260).[^huyen2025] 그 유사도 측정 자체는
  [참조 데이터 대비 유사도 측정](../concepts/similarity-measurements-against-reference-data.md)에 있다.
- 그러나 조건이 붙는다 — **이 접근은 질의와 문서의 길이가 비슷할 때 가장 잘 통한다. 문서가 질의보다
  훨씬 길면 질의의 n-그램을 담을 가능성이 커져 많은 문서가 비슷하게 높은 겹침 점수를 갖게 된다.
  이는 진짜 관련 있는 문서를 덜 관련 있는 문서와 구별하기 어렵게 만든다** (6장,
  p.260).[^huyen2025]

## 이어지는 페이지

- [검색 증강 생성(RAG)](../concepts/retrieval-augmented-generation.md) — 이 검색이 놓이는 파이프라인
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — 어휘 층이 아니라 의미 층에서 재는 쪽
- [전문 검색 색인](../concepts/full-text-search-indexes.md) — 역색인과 포스팅 리스트의 자료 구조
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 이 갈래를 임베딩 갈래와
  섞는 자리
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — 두 갈래를 무엇으로 비교하는가
- [참조 데이터 대비 유사도 측정](../concepts/similarity-measurements-against-reference-data.md) —
  n-그램 겹침이 처음 나온 자리
- [언어 모델과 토큰](../concepts/language-models-and-tokens.md) — 토큰화라는 낱말의 다른 쓰임

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Retrieval
    Algorithms" 절 서두(p.257), 상자 "Sparse Versus Dense Retrieval"(p.258), "Term-based
    retrieval" 절(pp.258–260)을 담았다. Table 6-1은 원문 표기를 그대로 옮겼다. 이 절에는 도판이 없다.
    TF-IDF 수식은 원문의 수학 표기를 인라인 코드로 옮긴 것이다. Chen 등 다른 인용과 마찬가지로
    Sanderson and Croft(2012)·Formal et al.(2021, SPLADE)·Shay Banon(2010, 엘라스틱서치)·
    Robertson et al.(1980년대, Okapi BM25)·Robertson and Zaragoza(2009)·아라빈드 스리니바스의 트윗은
    huyen2025를 통한 전언이다. BM25가 만만찮은 기준선이라는 진술은 아래 원전 각주로 이중화했다.

[^karpukhin2020-dpr]: Karpukhin et al. 2020, "Dense Passage Retrieval for Open-Domain Question
    Answering", EMNLP 2020 (논문 13쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다. 이 페이지는 초록·1절
    Introduction·3.2절 Training·5절 Experiments: Passage Retrieval(5.1·5.4)·부록 C를 담았다.
    Table 2의 상위 20 행만 본문 서술로 옮겼고 표 자체는
    [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)에 있다. Table 7(BM25/DPR 검색 예시,
    pp.12–13)은 옮기지 않았고 본문이 서술한 것만 담았다.
    BM25(Robertson and Zaragoza, 2009)·루씬·FAISS(Johnson et al., 2017)는 karpukhin2020-dpr을 통한
    전언이다.

[^lewis2020-rag]: Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP
    Tasks", NeurIPS 2020 (논문 16쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다. 이 페이지는 4.5절
    Additional Results의 검색 절제(Retrieval Ablations) 항목만 담았다. Table 6의 수치는 옮기지
    않았고 본문이 서술한 우열만 담았다. FEVER(Thorne et al., 2018)·BM25(Robertson and Zaragoza,
    2009)는 lewis2020-rag를 통한 전언이다.

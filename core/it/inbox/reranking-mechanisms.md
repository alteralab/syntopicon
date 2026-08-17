---
type: concept
title: 리랭킹의 기제
description: 싼 검색기가 모아 온 후보를 다시 줄 세우는 기전의 계보 넷 — 교차 어텐션이 미리 계산될 수 없어 검색이 아니라 리랭킹 자리에 서는 구조적 이유와 그 비용 배수, BERT를 이진 분류기로 세워 구절마다 독립으로 점수를 내는 리랭커의 기제·수치·훈련 재료, 그 계보가 분류에서 생성으로 넘어가 "true" 토큰의 정규화된 확률로 순위를 매기는 자리와 목표 토큰을 조작해 적은 데이터에서 이기는 이유를 시험한 실측, 후보를 한 묶음씩 읽혀 순열을 직접 뱉게 하는 리스트와이즈 리랭킹의 슬라이딩 윈도·초기 순서 민감도·순열 증류, 그리고 질의와 문서를 따로 인코딩해 두고 뒤에서만 만나게 해 리랭킹 비용을 두 자리 수 줄이는 late interaction의 지연·FLOPs 실측과 리랭킹이 앞 단계 재현율에 갇힌다는 대조
generated: { by: "claude-opus-5", at: "2026-08-17T17:20:00Z" }
status: draft
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: karpukhin2020-dpr, resource: /it/sources/karpukhin2020-dpr.md }
  - { id: reimers2019-sbert, resource: /it/sources/reimers2019-sbert.md }
  - { id: lewis2020-rag, resource: /it/sources/lewis2020-rag.md }
  - { id: nogueira2019-rerank, resource: /it/sources/nogueira2019-rerank.md }
  - { id: nogueira2020-monot5, resource: /it/sources/nogueira2020-monot5.md }
  - { id: sun2023-rankgpt, resource: /it/sources/sun2023-rankgpt.md }
  - { id: khattab2020-colbert, resource: /it/sources/khattab2020-colbert.md }
---

# 리랭킹의 기제

- [교차 인코더는 왜 뒤에 서는가](#교차-인코더는-왜-뒤에-서는가)
- [교차 인코더 리랭커의 기제](#교차-인코더-리랭커의-기제)
- [그 리랭커가 낸 수치](#그-리랭커가-낸-수치)
- [계보의 다음 고리 — 분류에서 생성으로](#계보의-다음-고리--분류에서-생성으로)
- [목표 토큰이 왜 아무 낱말이나여도 되지 않는가](#목표-토큰이-왜-아무-낱말이나여도-되지-않는가)
- [한 쌍씩 말고 한 묶음씩 — 리스트와이즈 리랭킹](#한-쌍씩-말고-한-묶음씩--리스트와이즈-리랭킹)
- [리스트와이즈 리랭커가 잰 것](#리스트와이즈-리랭커가-잰-것)
- [순열을 증류해 작은 모델로 옮기기](#순열을-증류해-작은-모델로-옮기기)
- [비용을 문서 쪽으로 옮기는 제3 갈래](#비용을-문서-쪽으로-옮기는-제3-갈래)
- [그 갈래가 잰 지연과 품질](#그-갈래가-잰-지연과-품질)
- [원전이 밝힌 조건과 한계](#원전이-밝힌-조건과-한계)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **순위를 다시 매기는 기제는 무엇이고 왜 뒤에 서는가.**

## 교차 인코더는 왜 뒤에 서는가

- 검색기가 못 쓰는 것. 조건의 원 진술이다 (3.1절, p.3):[^karpukhin2020-dpr]

  > Although more expressive model forms for measuring the similarity between a question and a
  > passage do exist, such as networks consisting of multiple layers of cross attentions, the
  > similarity function needs to be decomposable so that the representations of the collection of
  > passages can be pre-computed.

  곧 교차 인코더가
  검색 단계에 못 서는 이유는 정확도가 아니라 **미리 계산할 수 없다는 구조적 제약**이다.
- 그래서 뒤에 세운다 — **구절 선택 모델은 질문과 구절 사이의 교차 어텐션(cross-attention)을 통해
  리랭커 노릇을 한다. 교차 어텐션은 분해 불가능한 성질 때문에 큰 코퍼스에서 관련 구절을 검색하는
  데는 쓸 수 없지만, 듀얼 인코더 모델보다 용량이 크다. 검색된 소수의 후보 중에서 구절을 고르는 데
  적용하는 것은 잘 통한다고 알려져 있다** (6.1절, p.7).[^karpukhin2020-dpr] 원전의 판독기는
  **질문마다 검색 시스템이 돌려준 상위 100개 구절에서 양성 하나와 음성 `m̃−1`개를 표집해 훈련하며
  `m̃ = 24`를 모든 실험에 쓴다** (6.1절, p.7).[^karpukhin2020-dpr]
- "비싼 기전"이 얼마나 비싼가 — **BERT는 교차 인코더를 쓴다: 두 문장이 트랜스포머 네트워크에
  전달되고 목표값이 예측된다. 그러나 이 설정은 가능한 조합이 너무 많아 여러 쌍 회귀 과제에
  부적합하다. 1만 개 문장 모음에서 유사도가 가장 높은 쌍을 찾으려면 BERT로 `n(n−1)/2 = 49,995,000`회
  추론 계산이 필요하고, 현대 V100 GPU에서 이는 약 65시간이 걸린다** (1절,
  p.1).[^reimers2019-sbert] 문장을 각각 임베딩해 코사인으로 비교하면 같은 일이 **약 5초 + 코사인
  계산 0.01초**로 줄어든다 (2절, p.2).[^reimers2019-sbert] 이 배수가 "싼 것으로 후보를 모으고
  비싼 것으로 다시 줄 세운다"는 관행의 수치적 근거다.
  - 중간 형태 하나 — **Humeau et al.(2019)은 BERT 교차 인코더의 실행 시간 부담을 다루려고
    어텐션으로 `m`개 맥락 벡터와 미리 계산된 후보 임베딩 사이의 점수를 계산하는 방법(poly-encoder)을
    제시한다. 이 착상은 더 큰 모음에서 최고 점수 문장을 찾는 데 통한다. 그러나 점수 함수가 대칭이
    아니고, 군집화처럼 `O(n²)` 점수 계산을 요구하는 유스케이스에는 계산 부담이 너무 크다는 단점이
    있다** (2절, pp.2–3).[^reimers2019-sbert] Humeau et al.은 아직 반입되지 않은 원전의 자리다.

## 교차 인코더 리랭커의 기제

> **경심사 조건**: 이 절과 다음 절의 claim은 미심사 arXiv 원고에서 온다. 저자들이 심사본을 내지
> 않았고 대체 원전이 없어 조건부로 반입했다 — 수치는 저자 자기 보고이며 심사자의 검증을 거치지
> 않았다. 다만 같은 제1저자의 심사본이 같은 구조를 다시 세우고 다시 재는 자리가
> [계보의 다음 고리](#계보의-다음-고리--분류에서-생성으로)에 있다. **이 원고 자체의 수치가 심사된
> 것은 아니다** — 뒷받침되는 것은 방법론이지 이 표가 아니다.

- 그 리랭커가 놓이는 자리 — **단순한 질의응답 파이프라인은 세 단계로 이뤄진다. 먼저 주어진 질문에
  관련 있을 법한 다수의(예컨대 1,000개) 문서가 BM25 같은 표준 기전으로 코퍼스에서 검색된다. 둘째
  단계인 구절 리랭킹(passage re-ranking)에서 이 문서들 각각이 계산량이 더 많은 방법으로 점수 매겨져
  다시 순위 매겨진다. 마지막으로 이 문서들의 상위 10개나 50개가 답 생성 모듈의 후보 답 출처가 된다**
  (2절, p.1).[^nogueira2019-rerank] huyen2025가 "싼 것 다음에 비싼 것"이라 부른 구조의 실물이다.
- 리랭커가 하는 일의 원 진술 — **리랭커의 일은 후보 구절 `d_i`가 질의 `q`에 얼마나 관련 있는지를
  나타내는 점수 `s_i`를 추정하는 것이다** (2절, p.1).[^nogueira2019-rerank]
- 그 추정을 BERT로 하는 방법 — **질의를 문장 A로, 구절 텍스트를 문장 B로 먹인다. 질의는 최대
  64 토큰으로 자르고, 질의·구절·구분 토큰을 이은 길이가 최대 512 토큰이 되도록 구절 텍스트도 자른다.
  BERT_LARGE 모델을 이진 분류 모델로 쓴다 — 곧 `[CLS]` 벡터를 단층 신경망의 입력으로 써서 그 구절이
  관련 있을 확률을 얻는다. 이 확률을 구절마다 독립적으로 계산하고, 이 확률에 대해 구절들을 순위
  매겨 최종 목록을 얻는다** (2절, p.2).[^nogueira2019-rerank] **구절마다 독립적으로**가 이 방식의
  이름이 가리키는 것이다 — 점수는 (질의, 구절) 쌍 하나에서 나오고 후보끼리 비교되지 않는다.
  - 이 페이지가 부르는 "교차 인코더"와의 관계 — 질의와 구절을 한 시퀀스로 이어 트랜스포머에 넣는
    것이 곧 교차 어텐션이므로, 이것이 위에서 DPR·SBERT가 "검색 단계에는 못 서지만 리랭킹에는
    잘 통한다"고 말한 그 구조다.[^karpukhin2020-dpr][^reimers2019-sbert]
  - **논문 자신은 "monoBERT"라는 이름을 쓰지 않는다** — 제목과 본문 모두 "BERT를 구절 리랭커로 쓴
    단순한 재구현"으로만 부른다 (초록, p.1).[^nogueira2019-rerank] 그 이름은 뒤에 붙은
    것이므로 이 페이지는 원전의 표기를 따른다.
- 무엇으로 훈련하는가 — **사전 훈련된 BERT 모델에서 시작해 교차 엔트로피 손실로 리랭킹 과제에 파인
  튜닝한다. 양성 집합은 관련 구절의 색인이고 음성 집합은 BM25로 검색한 상위 1,000개 문서 중 관련
  없는 구절의 색인이다** (2절, p.2).[^nogueira2019-rerank] 곧 리랭커의 훈련 재료는 앞 단계 어휘
  검색기가 만들어 준다 — 어휘 갈래가 조밀 검색기의 어려운 음성 표본 공급원이 되는 것과 같은
  구조다.[^karpukhin2020-dpr]

## 그 리랭커가 낸 수치

- 원문 표기를 그대로 옮겼다 (3.3절, p.3, Table 1 발췌):[^nogueira2019-rerank]

  | Method | MS MARCO MRR@10 (Dev) | MS MARCO MRR@10 (Eval) | TREC-CAR MAP (Test) |
  |---|---|---|---|
  | BM25 (Lucene, no tuning) | 16.7 | 16.5 | 12.3 |
  | BM25 (Anserini, tuned) | – | – | 15.3 |
  | Conv-KNRM (Dai et al., 2018) | 29.0 | 27.1 | – |
  | IRNet (당시 리더보드 최고) | 27.8 | 28.1 | – |
  | BERT Base | 34.7 | – | 31.0 |
  | BERT Large | 36.5 | 35.8 | 33.5 |

  - 저자들이 요약한 폭 — **이 시스템은 TREC-CAR 데이터셋에서 최고 성능이고 MS MARCO 구절 검색
    과제 리더보드의 1위 항목이며, 이전 최고 성능을 MRR@10에서 27%(상대) 앞선다** (초록,
    p.1).[^nogueira2019-rerank] 표를 읽으면 어휘 기반 기준선(16.7)과 리랭킹 후(36.5)의 차이가
    두 배를 넘는다 — huyen2025가 "더 정밀하지만 더 비싼 기전"이라 부른 것의 값이 이 자리다.
- 얼마나 적은 데이터로 되는가 — **이 작업에 쓰인 사전 훈련 모델은 좋은 성능을 내는 데 최종 과제의
  훈련 예시를 거의 요구하지 않는다. 예컨대 질문–구절 쌍 10만 개(MS MARCO 훈련 데이터의 0.3%
  미만)로 훈련한 BERT_LARGE가 이미 이전 최고 성능 IR-NET보다 MRR@10 1.4점 낫다** (3.3절,
  p.3, Figure 1).[^nogueira2019-rerank]
  - 훈련 비용 — **TPU v3-8에서 배치 크기 128로 10만 회 반복 파인 튜닝했고 약 30시간이 걸렸다. 이는
    질의–구절 쌍 1,280만 개에 해당하며 전체 훈련 집합의 2% 미만이다. 사흘 더 훈련해 총 5,000만 쌍을
    보게 해도 개발 집합에서 개선을 볼 수 없었다** (3.1절, p.2).[^nogueira2019-rerank]
- 저자들이 스스로 좁힌 범위 — 결론은 **BERT를 구절 리랭커로 삼는 단순한 적응**이라는 진술에
  그치고 (4절, p.3),[^nogueira2019-rerank] 지연·처리량이나 프로덕션 비용에 대한 측정은 이 원고에
  없다. 리랭커를 실제로 얼마나 깊이 걸 수 있는지는 이 원전이 답하지 않는 물음이다.

## 계보의 다음 고리 — 분류에서 생성으로

> **심사 보강**: 위 두 절의 claim은 미심사 원고에서 왔다. 이 절부터는 같은 제1저자의 심사본
> (Findings of EMNLP 2020 — **경심사 트랙**)과 본회의 심사본(EMNLP 2023)이 같은 구조를 다시
> 세우고 실측한다. 곧 위 원고의 방법론은 여기서 독립 검증이 아니라 **계보의 연속**으로 뒷받침된다.

- 무엇을 바꿨는가 — **우리 접근은 BERT 같은 인코더 전용 사전 훈련 트랜스포머 구조에 기반한, 흔히
  채택되는 분류 기반 정식화와 근본적으로 다르다. 시퀀스 투 시퀀스 모델이 관련성 라벨을 "목표
  토큰(target tokens)"으로 생성하도록 훈련될 수 있음을, 그리고 그 목표 토큰의 바탕 로짓이 랭킹을
  위한 관련성 확률로 해석될 수 있음을 보인다** (초록, p.1).[^nogueira2020-monot5]
- 입력 틀 — 문서 랭킹을 관련성 예측 문제로 두고 **`Query: [Q] Document: [D] Relevant:`** 형태의
  입력 템플릿을 쓰며, **`[Q]`와 `[D]`는 각각 질의와 문서 텍스트로 대치되고 모델은 문서가 질의에
  관련 있는지에 따라 "true" 또는 "false" 토큰을 생성하도록 파인 튜닝된다** (2절,
  p.2, 식 (1)).[^nogueira2020-monot5]
- 순위를 뽑아내는 요령 — **추론 시점에 모델에서 쓸 만한 확률을 뽑기 위해 "true"와 "false" 토큰의
  로짓에만 소프트맥스를 적용한다. 곧 이렇게 정규화된 "true" 토큰의 확률을 `Pr(relevant = 1 | q, d)`로
  계산하고 이 추정치를 질의–문서 쌍마다의 관련성 점수로 해석한다. 1차 검색에서 온 후보 문서마다
  독립적으로 모델에 먹이고, 최종 문서 랭킹은 이 추정 확률의 내림차순에 따른 초기 후보의 순열일
  뿐이다** (2절, p.2).[^nogueira2020-monot5] **후보마다 독립적으로**라는 점에서 위 절의 monoBERT식
  리랭커와 같은 계열이고, 갈리는 것은 **점수를 어디서 읽어 내는가**뿐이다.[^nogueira2019-rerank]
  - **이 논문도 자기를 "monoT5"라 부르지 않는다** — 본문은 T5-base·T5-large·T5-3B로만 부르고
    monoT5라는 이름은 등장하지 않는다.[^nogueira2020-monot5] 그 이름은 뒤에 붙은 것이며 실제로
    RankGPT가 이 모델을 monoT5로 인용한다 (6.2절, p.5).[^sun2023-rankgpt] 앞 절의 monoBERT와 같은
    사정이라 이 페이지는 원전의 표기를 따른다.
- 무엇이 나왔는가. 앞 절의 표와 같은 벤치마크다. 원문 표기를 그대로 옮겼다 (4절, p.4, Table 1 —
  MS MARCO 구절 MRR@10):[^nogueira2020-monot5]

  | Model | # Params | Dev | Test |
  |---|---|---|---|
  | BM25 | – | 0.184 | 0.186 |
  | + BERT-large | 340 M | 0.372 | 0.365 |
  | + T5-base | 220 M | 0.381 | – |
  | + T5-large | 770 M | 0.393 | – |
  | + T5-3B | 3 B | 0.398 | 0.388 |

  - 읽는 법 — **T5-base가 더 큰 BERT-large 모델을 앞선다** (5.1절, p.5).[^nogueira2020-monot5] 곧
    이 표에서 오는 이득은 모델을 키운 것만으로 설명되지 않는다.
  - 정규화가 공짜가 아니다 — **"true" 토큰의 로짓만 문서 점수로 쓰면 MRR@10이 0에 가까운 0.026으로
    형편없다. 모든 로짓에 소프트맥스를 걸거나(0.379) "true"·"false" 로짓에만 걸면(0.381) 비슷하게
    높은 값이 나온다. 이는 특정 토큰의 로짓이 서로 다른 예시에 걸쳐 비교 가능하지 않으며, 적절히
    정규화되고 나서야 비교 가능해진다는 것을 보인다** (5.3절, p.7, Table 3).[^nogueira2020-monot5]
- 적은 데이터에서 갈린다 — **양성 1천 건과 음성 1천 건만으로 훈련하면 BERT는 BM25 기준선보다 나쁜,
  곧 정확 용어 일치보다도 못한 성능을 내는 반면 T5는 BM25 기준선보다 7점 낫다. 훈련 예시 1만 건에서
  BERT는 BM25를 조금 개선할 수 있지만 여전히 같은 양으로 훈련된 T5보다 9점 뒤진다. 흥미롭게도 T5는
  훈련 데이터의 2%만으로 BM25 기준선보다 약 10점 위, 곧 자기 전체 이득의 60% 가까이에 도달한다**
  (5.1절, pp.5–6, Figure 1).[^nogueira2020-monot5]
- 도메인 밖으로 옮겨도 되는가 — Robust04·Core17·Core18은 **모델이 그 컬렉션의 라벨 훈련 데이터에
  전혀 노출되지 않은 제로샷**이며 (3.1절, p.3; 5.2절, p.6), 그럼에도 T5-3B는 **이 시험 컬렉션들에
  보고된 가장 높은 알려진 점수**를 낸다 (4절, p.4).[^nogueira2020-monot5] 다만 두 단서가 붙는다 —
  ⑴ **T5 모델의 상위 20개 판정 비율(Jdg@20)이 BM25보다 낮다. 곧 모델이 한 번도 평가된 적 없는
  문서를 가져오고 있고, 표준 평가 도구가 "미상"을 비관련으로 취급하므로 이 결과는 참 성능의
  하한이다** (4절, p.5) ⑵ **Robust04에서는 모든 모델 크기가 과훈련의 징후를 보인다 — 특정
  데이터셋에 점점 더 파인 튜닝하는 것이 다른 도메인으로 일반화하는 능력을 줄이는 것은 말이 된다**
  (5.2절, p.6, Figure 2).[^nogueira2020-monot5]

## 목표 토큰이 왜 아무 낱말이나여도 되지 않는가

- 저자들이 던진 물음 — **왜 우리 접근이 BERT보다 데이터 효율적인가? 그리고 우리 경우의 소프트맥스가
  모델을 이진 분류기로 환원한다는 점을 감안할 때, 이 접근은 인코더 전용 모델의 분류와 근본적으로
  무엇이 다른가?** (5.4절, p.7).[^nogueira2020-monot5]
- 저자들의 답 — **분류 기반 접근에서 모델은 잠재 표현(`[CLS]` 토큰)을 이진 결정으로 사상하는 데
  단일 완전 연결 층에 기대는데, 그 최종 사상은 무작위로 초기화되므로 처음부터 배워야 한다. 이와 달리
  T5는 출력 토큰을 생성하는 데 쓰이는 신경망 부분을 활용할 수 있고, 그 신경 기계 안에는 유창한
  텍스트를 생성하는 데 필요한 의미론·언어적 관계·어휘 특징에 대한 잠재 지식이 박혀 있다. 곧 T5는
  BERT가 갖지 못한 추가 지식 원천에 접근한다** (5.4절, pp.7–8).[^nogueira2020-monot5] #hypothesis
- 그 가설을 시험하는 방법이 목표 토큰 조작이다 — 관련/비관련의 목표 토큰을 `true`/`false`(기준),
  `yes`/`no`, 뒤바꾼 `false`/`true`, 반의어 `hot`/`cold`, 관련어 `apple`/`orange`, 무관어
  `hot`/`orange`, 부분어 `_ab`/`_de`로 바꿔 가며 잰다 (5.4절, p.8).[^nogueira2020-monot5]
- 결과가 두 갈래로 갈린다 (5.4절, p.8, Table 4):[^nogueira2020-monot5]
  - **가용한 데이터 전부로 파인 튜닝하면 목표 토큰의 선택은 효과에 무시할 만한 영향만 준다.** 실제로
    53만 건 조건에서 일곱 설정이 0.374–0.378에 몰린다.
  - **1만 건 조건에서는 "Alternate"(yes/no)를 뺀 목표 토큰 조작 전부가 효과를 유의미하게 떨어뜨린다.**
    기준 0.294에 견주어 부분어는 0.228, 무관어는 0.242다. 가장 강한 증거는 **1천 건 조건에서 부분어가
    BM25 기준선보다도 나쁘다**는 것이다.
  - 저자들이 남긴 미해결 — **적은 데이터 상황에서 극성 척도를 갖는 것의 중요성에 대해서는 실험이
    결론을 내지 못한다.** `true`/`false`를 뒤바꾸는 것은 눈에 띄는 영향을 주지만, T5는 극성 대비가 없는 관련어
    (`apple`/`orange`)를 무관한 극성 대비(`hot`/`cold`)보다 더 잘 배운다 (5.4절,
    p.9).[^nogueira2020-monot5]

## 한 쌍씩 말고 한 묶음씩 — 리스트와이즈 리랭킹

- 무엇이 문제인가 — **관련성 리랭킹의 목적은 LLM의 것과 크게 다르다. 리랭킹 에이전트는 사용자 요구를
  이해하고, 전역적으로 비교하고, 질의에 대한 관련성에 근거해 구절들을 순위 매겨야 한다** (1절,
  p.1).[^sun2023-rankgpt] 위 두 절의 리랭커는 **(질의, 구절) 쌍 하나에서 점수를 내고 후보끼리
  비교하지 않는다**는 점에서 이 요구를 구조적으로 비켜 간다.[^nogueira2019-rerank][^nogueira2020-monot5]
- 앞선 LLM 활용 방식의 제약 — **기존 방법들은 리랭킹에서 성능이 제한적이고 모델 출력의 로그 확률
  가용성에 크게 의존하므로 GPT-4 같은 최신 LLM에는 적용할 수 없다** (3절, p.3).[^sun2023-rankgpt]
  위 절의 monoT5가 **로짓을 읽어 점수를 만든** 것이 바로 그 의존이다.[^nogueira2020-monot5]
- 이 방식의 정의다. 원문 표기를 그대로 옮겼다 (3절, p.3):[^sun2023-rankgpt]

  > we introduce a novel instructional permutation generation method with a sliding window strategy
  > to directly output a ranked list given a set of candidate passages.

- 제안 — **우리 접근은 각각 고유 식별자(예: `[1]`, `[2]` 등)로 표시된 구절 묶음을 LLM에 입력하는
  것을 수반한다. 그다음 LLM에게 질의에 대한 관련성의 내림차순으로 구절의 순열을 생성하도록 요청한다.
  구절은 `[2] > [3] > [1]` 같은 형식으로 식별자를 써서 순위 매겨진다. 제안된 방법은 중간 관련성 점수를
  만들지 않고 구절을 직접 순위 매긴다** (3.1절, p.3).[^sun2023-rankgpt]
- 컨텍스트 한계는 슬라이딩 윈도로 넘는다 — **1차 검색 모델이 `M`개 구절을 돌려준다고 하자. 우리는
  슬라이딩 윈도를 써서 이 구절들을 뒤에서 앞으로 리랭킹한다. 먼저 LLM으로 `(M − w)`번째부터 `M`번째
  구절까지를 순위 매기고, 그다음 윈도를 `s` 단계씩 미끄러뜨려 `(M − w − s)`번째부터 `(M − s)`번째
  범위를 다시 순위 매긴다. 이 과정을 모든 구절이 리랭킹될 때까지 반복한다** (3.2절,
  pp.3–4).[^sun2023-rankgpt] 실험에서는 **BM25가 검색한 상위 100개 구절을 윈도 크기 20·단계 크기
  10으로** 리랭킹한다 (6.1절, p.5).[^sun2023-rankgpt]

## 리스트와이즈 리랭커가 잰 것

- 지시 방식의 비교가 먼저다 — 같은 API 엔드포인트에 질의 생성(QG)·관련성 생성(RG)·순열 생성(PG)을
  걸어 재면 **PG가 구절 리랭킹을 지시하는 데서 QG와 RG 양쪽을 앞선다**고 저자들은 요약한다 (6.4절,
  pp.6–7, Table 4).[^sun2023-rankgpt] 그들이 붙인 설명 둘 — **첫째, PG의 top-1 정확도가 다른 방법보다
  유의미하게 높다는 결과에서 LLM이 PG로 여러 구절을 명시적으로 비교할 수 있어 구절 사이의 미묘한
  차이를 분간한다고 추론한다. 둘째, LLM이 잠재적으로 상보적인 정보를 담은 여러 구절을 읽음으로써
  질의와 구절에 대한 더 포괄적인 이해를 얻는다** (6.4절, p.7).[^sun2023-rankgpt] #hypothesis
- 지도 학습된 리랭커와의 대조다. 원문 표기를 그대로 옮겼다 (6.2절, p.6, Table 1 발췌 —
  nDCG@10):[^sun2023-rankgpt]

  | Method | DL19 | DL20 | BEIR (Avg) |
  |---|---|---|---|
  | BM25 | 50.58 | 47.96 | 43.42 |
  | monoBERT (340M) | 70.50 | 67.28 | 47.16 |
  | monoT5 (220M) | 71.48 | 66.99 | 49.07 |
  | monoT5 (3B) | 71.83 | 68.89 | 51.36 |
  | gpt-3.5-turbo | 65.80 | 62.91 | 49.37 |
  | gpt-4 | 75.59 | 70.56 | 53.68 |

  - 읽는 법 — **GPT-4는 순열 생성 지시를 얹었을 때 두 데이터셋 모두에서 우월한 성능을 보이며,
    monoT5(3B)에 견주어 TREC와 BEIR에서 각각 평균 2.7과 2.3의 nDCG@10 개선을 달성한다** (6.2절,
    p.5).[^sun2023-rankgpt] ChatGPT는 그 아래이되 지도 베이스라인 다수를 앞선다.
  - 이 표의 monoBERT·monoT5 행이 위 두 절이 담은 원전들이다.[^nogueira2019-rerank][^nogueira2020-monot5]
    곧 리랭커 계보 셋이 같은 벤치마크의 한 표에서 만난다.
  - 비용을 깎는 조합 — **BEIR에서는 ChatGPT가 리랭킹한 상위 30개만 GPT-4로 다시 리랭킹했고, 그
    방법이 좋은 결과를 내면서 비용은 GPT-4만 쓸 때의 1/5에 그친다** (6.2절,
    pp.5–6, Table 1 각주).[^sun2023-rankgpt]
    [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)의 "싼 것 다음에 비싼 것"이
    리랭커 단계 안에서 한 번 더 반복되는 자리다.[^huyen2025]
- 데이터 오염을 피해 다시 재기 — 저자들은 **GPT-4 출시 이후 발행된 4개 도메인에서 질문과 구절을
  모아 21개 새 질문의 NovelEval-2306을 만들고**, 거기서도 **GPT-4가 이전 최고 지도 방법인
  monoT5(3B)를 유의미하게 앞선다**고 보고한다 (5.2절, p.5; 6.3절, p.6, Table 3).[^sun2023-rankgpt]
  그 오염 문제 자체는 [데이터 오염](../concepts/data-contamination.md)에 있다.
- **초기 순서에 매우 민감하다** — BM25 순서 대신 무작위 순서나 뒤집힌 순서로 시작하면 TREC-DL19
  nDCG@10이 65.80에서 각각 25.17과 32.77로 무너진다 (6.5절, p.7, Table 5).[^sun2023-rankgpt]
  저자들의 읽기는 **BM25가 상대적으로 좋은 출발 순서를 제공해 단 한 번의 슬라이딩 윈도 리랭킹만으로도
  만족스러운 결과를 낼 수 있게 한다**는 것이다 (6.5절, p.7).[^sun2023-rankgpt] 곧 리스트와이즈
  리랭커는 앞 단계 검색기를 대체하지 않고 그 출력에 강하게 의존한다.
  - 더 돌린다고 좋아지지도 않는다 — **여러 번 리랭킹하면 nDCG@10은 개선될 수 있지만 상위 구절의
    랭킹 성능은 어쩐지 해친다(예컨대 nDCG@1이 3.88 떨어진다)** (6.5절, p.7,
    Table 5).[^sun2023-rankgpt]

## 순열을 증류해 작은 모델로 옮기기

- 왜 증류인가 — **ChatGPT와 GPT-4는 매우 유능하지만 상용 검색 시스템에 배포하기에는 너무 비싸다.
  GPT-4로 구절을 리랭킹하는 것은 검색 시스템의 지연을 크게 늘릴 것이다. 게다가 큰 언어 모델은 불안정한
  생성이라는 문제를 겪는다. 그래서 우리는 큰 언어 모델의 능력이 리랭킹 과제에는 과잉이라고 주장한다**
  (4절, p.4).[^sun2023-rankgpt]
- 무엇을 목표로 삼는가 — **우리 접근과 앞선 증류 방법의 핵심 차이는 일관성 검사나 로그 확률 조작
  같은 어떤 귀납 편향도 들이지 않고 모델이 생성한 순열을 직접 목표로 쓴다는 것이다** (4.1절,
  p.4).[^sun2023-rankgpt] 실물로는 **MS MARCO 훈련 집합에서 질의 1만 개를 표집하고 질의마다 BM25로
  후보 구절 20개를 검색한 뒤**, ChatGPT의 순열을 RankNet 손실로 학생 모델에 넣는다 — **`M`개 구절의
  순열로 `M(M − 1)/2`개 쌍을 만들 수 있다** (4.1–4.2절, p.4).[^sun2023-rankgpt] 증류 일반은
  [모델 증류](../concepts/model-distillation.md)에 있다.
- 결과가 두 방향으로 뒤집힌다 (7.1절, p.8, Table 7):[^sun2023-rankgpt]
  - **특화 DeBERTa 모델이 이전 최고 성능 baseline인 monoT5(3B)를 앞선다** — BEIR 평균 nDCG 53.03
    대 51.36이며, 435M 대 3B다.[^nogueira2020-monot5]
  - **증류된 특화 모델이 자기 교사 모델인 ChatGPT까지 앞선다**(53.03 대 49.37). 저자들이 붙인
    설명은 **특화 모델의 리랭킹 안정성이 ChatGPT보다 낫기 때문일 것**이라는 것이다 (7.1절,
    p.8).[^sun2023-rankgpt] #hypothesis
  - **순열 증류가 지도 학습된 짝을 앞서는데, ChatGPT의 관련성 판단이 MS MARCO 라벨보다 더
    포괄적이기 때문일 수 있다** (7.1절, p.8).[^sun2023-rankgpt] #hypothesis 곧 여기서 교사가 주는
    것은 능력만이 아니라 **라벨의 품질**이다.
  - 어느 축을 키울 것인가 — **모델 파라미터 수를 늘리는 것이 훈련 데이터를 늘리는 것보다 랭킹
    결과에 더 큰 개선을 낸다** (7.2절, pp.8–9, Figure 4).[^sun2023-rankgpt]

## 비용을 문서 쪽으로 옮기는 제3 갈래

- 앞 절들이 깎으려 한 비용의 원인 진술 — **이 LM에 기반한 랭킹 모델은 특히 질의–문서 쌍 각각을
  거대한 신경망에 통과시켜 관련성 점수 하나를 계산해야 하기 때문에 계산 비용을 앞선 접근보다 자릿수
  단위로 늘린다** (초록, p.1).[^khattab2020-colbert] 이것이 위에서 **구절마다 독립적으로** 점수를
  낸다고 옮긴 구조의 대가다.[^nogueira2019-rerank]
- 매칭 구조를 넷으로 가른다 (1절, p.2, Figure 2):[^khattab2020-colbert]
  - **표현 중심(representation-focused) 랭커는 `q`와 `d`의 임베딩을 각각 독립으로 계산하고 관련성을
    두 벡터 사이 단일 유사도 점수로 추정한다.** [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)이 "싼 쪽"이라 부른
    갈래다.[^karpukhin2020-dpr]
  - **상호작용 중심(interaction-focused) 랭커는 `q`와 `d`를 각각 하나의 임베딩으로 요약하는 대신
    낱말·구절 수준 관계를 모형화해 깊은 신경망으로 맞춘다.**
  - **더 강한 상호작용 패러다임은 BERT의 트랜스포머 구조에서처럼 `q`와 `d` 안의 상호작용과 그 사이
    상호작용을 동시에 모형화한다.** 위 절들의 교차 인코더 리랭커가 이 자리다.[^nogueira2019-rerank]
  - **late interaction — 제안된 ColBERT.** 아래가 그 정의다.
- 왜 이 넷이 한 축에 놓이는가 — **이 점점 표현력이 커지는 구조들은 서로 긴장 관계에 있다.
  상호작용 기반 모델이 IR 과제에 우월한 경향이 있지만, 표현 중심 모델은 `q`와 `d` 사이 계산을
  격리함으로써 문서 표현을 오프라인으로 미리 계산할 수 있게 해 질의당 계산 부하를 크게 줄인다**
  (1절, p.2).[^khattab2020-colbert] 이 긴장은 앞에서 DPR이 **유사도 함수는 분해 가능해야 한다**고
  적은 제약과 같은 것이다.[^karpukhin2020-dpr]
- 저자들이 낸 답 — **상호작용 기반 모델의 세밀한 매칭과 표현 기반 모델의 문서 표현 미리 계산은,
  질의–문서 상호작용을 유지하되 신중하게 *지연시킴*으로써 결합될 수 있다** (1절,
  p.2).[^khattab2020-colbert] 그 지연이 이름의 late다.
- late interaction의 정의다. 원문 표기를 그대로 옮겼다 (1절, p.2):[^khattab2020-colbert]

  > Under late interaction, *q* and *d* are separately encoded into two sets of contextual embeddings,
  > and relevance is evaluated using cheap and *pruning-friendly* computations between both sets—that
  > is, fast computations that enable ranking without exhaustively evaluating every possible
  > candidate.

  곧 갈리는 것은 **인코더가 아니라 만나는 시점**이다 — 벡터 하나로 줄이지 않고 임베딩 집합을 남긴
  채, 상호작용을 색인 뒤로 미룬다. 그 인코더와 색인의 실물은
  [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)에 있다.
- 왜 리랭킹이 싸지는가 — **기존 BERT 랭커로 문서 `k`개를 순위 매기려면 질의 `q`와 문서 `d_i`마다
  길이 `l = |q| + |d_i|`인 서로 다른 입력 `k`개를 BERT에 먹여야 하고, 어텐션은 시퀀스 길이에
  이차 비용을 갖는다. 이와 달리 ColBERT는 길이 `l = |q|`인 훨씬 짧은 시퀀스 하나만 BERT에 먹인다**
  (3.5절, p.5).[^khattab2020-colbert] 곧 후보 수가 늘 때 늘어나는 것이 신경망 통과 횟수가 아니라
  미리 계산된 임베딩의 내적 연산이다.

## 그 갈래가 잰 지연과 품질

- 앞 절들과 같은 벤치마크의 한 표다. 각 신경 모델은 BM25가 만든 공식 상위 1,000개를 리랭킹하며
  지연은 리랭킹 구간만 잰 것이다. 원문 표기를 그대로 옮겼다 (4.2절, p.7,
  Table 1):[^khattab2020-colbert]

  | Method | MRR@10 (Dev) | MRR@10 (Eval) | Re-ranking Latency (ms) | FLOPs/query |
  |---|---|---|---|---|
  | BM25 (official) | 16.7 | 16.5 | – | – |
  | KNRM | 19.8 | 19.8 | 3 | 592M (0.085×) |
  | Duet | 24.3 | 24.5 | 22 | 159B (23×) |
  | fastText+ConvKNRM | 29.0 | 27.7 | 28 | 78B (11×) |
  | BERT_base | 34.7 | – | 10,700 | 97T (13,900×) |
  | BERT_base (our training) | 36.0 | – | 10,700 | 97T (13,900×) |
  | BERT_large | 36.5 | 35.9 | 32,900 | 340T (48,600×) |
  | ColBERT (over BERT_base) | 34.9 | 34.9 | 61 | 7B (1×) |

  - 저자들이 요약한 폭 — **ColBERT는 Nogueira와 Cho의 원래 BERT_base 랭킹 적응보다 나쁘지 않고
    BERT_large와 우리가 훈련한 BERT_base보다 근소하게만 덜 효과적이다. 효과에서 매우 경쟁력이 있으면서
    ColBERT는 BERT_base보다 자릿수 단위로 싸다 — 특히 지연에서 170배 넘게, FLOPs에서 13,900배**
    (4.2절, p.7).[^khattab2020-colbert] 표의 BERT_base 34.7과 BERT_large 36.5는 위
    [그 리랭커가 낸 수치](#그-리랭커가-낸-수치)에서 옮긴 원전의 값과 같다.[^nogueira2019-rerank]
    - **두 원전 사이에서 수치가 어긋나는 자리 하나** — BERT_large의 MS MARCO Eval MRR@10을
      nogueira2019-rerank는 **35.8**로 적고 (3.3절, p.3, Table 1),[^nogueira2019-rerank] 이 표는
      **35.9**로 적는다 (4.2절, p.7, Table 1).[^khattab2020-colbert] 한쪽이 오식인지 리더보드 재제출
      결과인지는 두 논문 안에서 판정되지 않으므로 두 값을 함께 남긴다.
  - 지연이 어디에 쓰이는가 — **ColBERT의 리랭킹 지연이 위에 보인 비BERT 리랭킹 모델보다 수십
    밀리초 높은 것은 문서 임베딩을 모으고 쌓아 GPU로 옮기는 데 걸리는 시간으로 설명된다. 특히
    ColBERT의 질의 인코딩과 상호작용은 전체 실행 시간의 13밀리초만 쓴다** (4.2절,
    p.7).[^khattab2020-colbert] 곧 이 갈래의 병목은 신경망이 아니라 데이터 이동이다.
- 후보를 깊이 볼수록 격차가 벌어진다 — **`k = 10`에서 BERT는 ColBERT보다 거의 180배 많은 FLOPs를
  요구하고, `k = 1000`에서 BERT의 초과분은 13,900배로 뛰며, `k = 2000`에서 23,000배에 이른다. 일부는
  ColBERT가 평가되는 문서 수와 무관하게 질의를 한 번만 처리하면 되기 때문이다** (4.2절, p.8,
  Figure 4).[^khattab2020-colbert] 위에서 RankGPT가 비용 때문에 상위 30개만 GPT-4에 넘긴 것과 같은
  물음에 대한 다른 답이다 — 리랭킹 깊이를 줄이는 대신 깊이당 비용을 줄인다.[^sun2023-rankgpt]
- 리랭킹은 앞 단계의 재현율에 갇힌다 — 같은 모델을 리랭킹으로 쓸 때와 끝단 검색으로 쓸 때를 나란히
  재면 **리랭킹 설정의 Recall@1000이 81.4로 공식 BM25의 Recall@1000과 같고**, 끝단 검색은 96.8이다
  (4.3절, p.7, Table 2).[^khattab2020-colbert] MRR@10도 34.8 대 36.0으로 끝단 검색이 앞선다 — 저자들의
  읽기는 **끝단 설정에서 ColBERT를 쓰는 것이 개선된 재현율 덕에 같은 모델로 리랭킹하는 것보다 MRR@10
  관점에서 우월하다**는 것이다 (4.3절, p.9).[^khattab2020-colbert] 곧 리랭커는 앞 검색기가 놓친 문서를
  되찾지 못한다. 그 끝단 검색의 실물과 나머지 열은
  [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)에 있다.
- 다른 컬렉션에서도 같은 자리에 선다. 원문 표기를 그대로 옮겼다 (4.2절, p.8,
  Table 3):[^khattab2020-colbert]

  | Method | MAP | MRR@10 |
  |---|---|---|
  | BM25 (Anserini) | 15.3 | – |
  | doc2query | 18.1 | – |
  | DeepCT | 24.6 | 33.2 |
  | BM25 + BERT_base | 31.0 | – |
  | BM25 + BERT_large | 33.5 | – |
  | BM25 + ColBERT | 31.3 | 44.3 |

  - 읽는 법 — 저자들은 **이 결과가 MS MARCO의 것을 그대로 되비친다**고만 요약한다 (4.2절,
    p.8).[^khattab2020-colbert] BM25+BERT 두 행의 MAP 31.0·33.5는 위에서 옮긴 nogueira2019-rerank의
    TREC-CAR MAP과 같은 값이다 (3.3절, p.3, Table 1).[^nogueira2019-rerank]

## 원전이 밝힌 조건과 한계

- 리랭커가 필요 없을 수도 있다 — **RAG는 문서를 다시 순위 매기는 데 BERT 기반 "교차 인코더"를 쓰고
  추출형 판독기를 함께 쓰는 DPR QA 시스템과 견주어 유리하다. RAG는 최고 성능에 리랭커도 추출형
  판독기도 필요하지 않음을 보인다** (4.1절, p.5).[^lewis2020-rag] 곧 리랭킹은 검색 파이프라인의
  필수 단계가 아니라, 뒤에 오는 생성기가 무엇을 할 수 있는가에 달린 선택이다.
- late interaction의 실측이 다루지 않은 것 — 저자들은 지연과 FLOPs를 줄이는 길로 **질의를 더 짧게
  패딩하기, 더 작은 벡터 차원 쓰기, 문서 벡터 양자화, 메모리가 충분하면 임베딩을 GPU에 두기**를
  열거하고 **이 방향들은 향후 작업으로 남긴다**고 적는다 (4.2절, pp.7–8).[^khattab2020-colbert]
  CPU만으로 리랭킹하는 것도 **비공식 실험에서 실용적으로 보인다**고만 적고 **우리 범위 밖**으로
  둔다 (4.2절, p.8).[^khattab2020-colbert] #hypothesis
- 절제 실험의 수치는 도판에만 있다 — 이 원전의 절제 결과는 값이 인쇄되지 않은 막대 도판이라
  본문이 서술한 방향만 옮길 수 있다 (4.4절, p.9, Figure 5).[^khattab2020-colbert] 무엇이 절제되었고
  어느 방향으로 움직였는지는
  [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)이 담는다.

## 이어지는 페이지

- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 이 기전들이 놓이는 결합 구조,
  랭크 융합(RRF)과 리랭킹을 언제 쓰는가
- [임베딩 기반 검색](../concepts/embedding-based-retrieval.md) — late interaction의 인코더·색인·
  저장 발자국
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — 계보 넷이 잰 MRR@10·nDCG@10이 정의되는 자리
- [쿼리 재작성](../concepts/query-rewriting.md) — 순위를 고치는 대신 질의를 고치는 쪽
- [모델 증류](../concepts/model-distillation.md) — 리랭킹 능력을 작은 모델로 옮기는 일반 기법
- [데이터 오염](../concepts/data-contamination.md) — 새 시험 집합을 따로 만든 이유
- [파운데이션 모델 평가의 어려움](../concepts/evaluating-foundation-models-challenges.md) — 순열
  생성이 불안정하다는 관측이 놓이는 축

[^nogueira2020-monot5]: Nogueira et al. 2020, "Document Ranking with a Pretrained
    Sequence-to-Sequence Model", Findings of EMNLP 2020 (인쇄 쪽 708–718). **경심사** — Findings는
    본회의가 아닌 경심사 트랙이고, 스냅샷 1쪽 하단에 "Findings of the Association for Computational
    Linguistics: EMNLP 2020"이 인쇄돼 있다. 쪽 번호는
    스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.708). 이 페이지는 초록·1절 Introduction·2절 Seq2Seq
    Ranking·3절 Experimental Setup(3.1–3.3)·4절 Results·5절 Analysis(5.1–5.4)·7절 Conclusion을
    담았다. Table 1은 원문 표기를 그대로 옮겼다. Table 2(Robust04·Core17·Core18)와 Table 3·4는
    본문이 서술한 수치만 담았다. Figure 1(훈련 데이터 크기별 비교, p.5)·Figure 2(에폭 수별 성능,
    p.6)는 옮기지 않았고 본문이 서술한 것만 담았다. 6절 Related Work는 담지 않았다.
    **이름 주의** — 이 원고는 "monoT5"라는 이름을 쓰지 않는다(그 이름으로 부르는 것은 이후
    문헌이며 이 페이지에서는 sun2023-rankgpt가 그렇게 인용한다).
    monoBERT 계열 원고(Nogueira and Cho, 2019)는 이 KB에 원전이 있다. T5(Raffel et al., 2020)·
    BERT(Devlin et al., 2019)·MS MARCO(Bajaj et al., 2016)·Robust04(Voorhees, 2004)·
    Core17·Core18·Birch(Yilmaz et al., 2019)·BERT–MaxP(Dai and Callan, 2019)·PARADE(Li et al.,
    2020)·Anserini·SentencePiece(Kudo and Richardson, 2018)·Puri and Catanzaro(2019)는
    nogueira2020-monot5를 통한 전언이다.

[^sun2023-rankgpt]: Sun et al. 2023, "Is ChatGPT Good at Search? Investigating Large Language
    Models as Re-Ranking Agents", EMNLP 2023 본회의 (인쇄 쪽 14918–14937). 학회 공식 페이지가
    Outstanding Paper로 표기한다. 쪽 번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.14918).
    이 페이지는 초록·1절 Introduction·2절 Related Work·3절 Passage Re-Ranking with LLMs(3.1–3.2)·
    4절 Specialization by Permutation Distillation(4.1–4.3)·5.2절 NovelEval·6절 Experimental
    Results of LLMs(6.1–6.5)·7절 Experimental Results of Specialization(7.1–7.2)·8절 Conclusion·
    Limitations를 담았다. Table 1은 DL19·DL20·BEIR 평균 열의 여섯 행만 발췌해 옮겼고 BEIR 개별
    여덟 데이터셋 열과 UPR·InPars·Promptagator++·Cohere Rerank 행은 옮기지 않았다. Table 2
    (Mr.TyDi 10개 언어)·Table 4(지시 방식 비교)·Table 5(절제)·Table 6(다른 LLM들)·Table 7(특화
    모델)·Table 13은 본문이 서술한 수치만 담았다. Figure 1–5와 부록 A–H(프롬프트·안정성 분석·
    API 비용)는 옮기지 않았다. 4.3절의 학생 모델 구조(DeBERTa 교차 인코더·LLaMA-7B)는 결론에
    필요한 만큼만 담았다.
    **원문 안에서 수치가 어긋나는 자리 하나** — 초록은 증류된 학생을 **440M**이라 적고, 1절과
    Table 7·Figure 4는 **435M**(deberta-v3-large)이라 적는다. 어느 쪽이 오식인지 논문 안에서
    판정되지 않으므로 이 페이지는 표에 인쇄된 435M을 쓰고 두 값을 함께 남긴다.
    monoBERT(Nogueira and Cho, 2019)·monoT5(Nogueira et al., 2020)·DPR(Karpukhin et al., 2020)·
    HyDE(Gao et al., 2023)는 이 KB에 원전이 있다. RankNet(Burges et al., 2005)·
    UPR(Sachan et al., 2022)·HELM(Liang et al., 2022)·InPars(Bonifacio et al., 2022)·
    Promptagator(Dai et al., 2023)·mmarcoCE(Bonifacio et al., 2021)·Cohere Rerank·
    DeBERTa·LLaMA(Touvron et al., 2023)·TREC-DL(Craswell et al., 2020)·BEIR(Thakur et al., 2021)·
    Mr.TyDi(Zhang et al., 2021)·MS MARCO는 sun2023-rankgpt를 통한 전언이다.

[^nogueira2019-rerank]: Nogueira and Cho, "Passage Re-ranking with BERT", arXiv:1901.04085.
    **미심사** — 저자들이 끝내 심사본을 내지 않아 arXiv 원고가 유일 정본이다. 스냅샷한 것은 v5
    (2020-04-14)이며 소스 메타의 연도(2019)는 v1 기준이다. 쪽 번호는 그 PDF의 쪽(전 5쪽)이다.
    이 페이지는 초록·2절 Passage Re-Ranking with BERT·3.1절 MS MARCO·3.3절 Results·4절
    Conclusion을 담았다. Table 1은 MS MARCO Dev·Eval과 TREC-CAR Test 열을 옮기되 KNRM·Co-PACRR
    행은 생략했다. Figure 1(훈련 예시 수 대 MRR@10, p.3)은 선에 값이 인쇄돼 있지 않아 본문이 진술한
    수치만 담았다. 3.2절 TREC-CAR의 데이터 누출 방지 절차는 이 페이지에 담지 않았다.
    BERT(Devlin et al., 2018)·MS MARCO(Nguyen et al., 2016)·TREC-CAR(Dietz et al., 2017)·
    IR-NET·Conv-KNRM(Dai et al., 2018)·Anserini는 nogueira2019-rerank를 통한 전언이다.

[^huyen2025]: Huyen 2025, 6장 "RAG and Agents" (책 pp.253–306). 이 페이지는 "Combining retrieval
    algorithms" 절(pp.266–267)의 순차 결합 진술을 리랭커 계보와 견주는 비교 인용만 담으며, 그 절과
    "Retrieval Optimization" 절 안의 "Reranking" 항목(p.269)의 본체는
    [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)이 담는다. 두 절에는 도판이 없다.
    RRF(Cormack et al., 2009)는 이 KB에 원전이 있다.

[^karpukhin2020-dpr]: Karpukhin et al. 2020, "Dense Passage Retrieval for Open-Domain Question
    Answering", EMNLP 2020 (논문 13쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다. 이 페이지는 3.1절
    Overview의 유사도 함수 분해 가능성 제약과 6.1절 End-to-end QA System의 리랭커 진술을
    담았다 — 1절 Introduction·5절 Experiments: Passage Retrieval·5.1절 Main Results·6.2절
    Results와 Table 2는 [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)이 담는다.
    판독기의 점수 식 (3)–(5)는 옮기지 않았다. BM25(Robertson and Zaragoza, 2009)·
    BERT(Devlin et al., 2019)는 karpukhin2020-dpr을 통한 전언이다.

[^reimers2019-sbert]: Reimers and Gurevych 2019, "Sentence-BERT: Sentence Embeddings using
    Siamese BERT-Networks", EMNLP-IJCNLP 2019 (논문 11쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다.
    이 페이지는 1절 Introduction과 2절 Related Work의 교차 인코더 비용 진술만 담았다 — 모델
    구조·훈련은 [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)이 담는다.
    poly-encoder(Humeau et al., 2019)·BERT(Devlin et al., 2018)는 reimers2019-sbert를 통한
    전언이다.

[^lewis2020-rag]: Lewis et al. 2020, "Retrieval-Augmented Generation for Knowledge-Intensive NLP
    Tasks", NeurIPS 2020 (논문 16쪽). 쪽 번호는 스냅샷한 PDF의 쪽이다. 이 페이지는 4.1절
    Open-domain Question Answering의 DPR QA 시스템 비교 진술만 담았다. DPR(Karpukhin et al.,
    2020)은 이 KB에 원전이 있다.

[^khattab2020-colbert]: Khattab and Zaharia 2020, "ColBERT: Efficient and Effective Passage Search
    via Contextualized Late Interaction over BERT", SIGIR 2020 (논문 10쪽). **오픈액세스 사정** —
    ACM DL이 페이월이라 스냅샷은 arXiv:2004.12832 v2(2020-06-04)이며, 그 PDF에는 SIGIR '20 ACM
    저작권 블록과 DOI 10.1145/3397271.3401075가 인쇄돼 있어 학회 카메라 레디와 같은 판본이다.
    ACM 논문집 인쇄 쪽 번호는 이 PDF에 없으므로 쪽 번호는 스냅샷한 PDF의 쪽이다.
    이 페이지는 초록·1절 Introduction·3.5절 Top-k Re-ranking·4.2절 Quality–Cost Tradeoff·4.3절
    End-to-end Top-k Retrieval의 리랭킹 대비 진술을 담았다 — 인코더·색인·저장 발자국·절제는
    [임베딩 기반 검색](../concepts/embedding-based-retrieval.md)이 담는다. Table 1과 Table 3은
    원문 표기를 그대로 옮겼다. Table 2는 이 페이지에서는 본문이 서술한 수치만 담았다(전체는
    임베딩 기반 검색 쪽). Figure 1(효과 대 지연 산점도, p.1)·Figure 2(매칭 패러다임 도식, p.2)·
    Figure 4(리랭킹 깊이별 FLOPs, p.8)·Figure 5(절제, p.9)는 옮기지 않았고 본문이 서술한 수치만
    담았다 — Figure 5는 막대에 값이 인쇄돼 있지 않다. 수식은 옮기지 않았다.
    **원문 안에서 수치가 어긋나는 자리 둘** — ⑴ FLOPs 절감 배수를 초록·1절·5절은 **14,000배**로,
    Table 1과 4.2절은 **13,900배**로 적는다(반올림으로 보이지만 판정되지 않아 두 값을 남긴다).
    ⑵ MS MARCO 구절 수를 1절은 **9M**, 4.1.1절과 Table 2 설명은 **8.8M**으로 적는다.
    Nogueira and Cho(2019)는 이 KB에 원전이 있다. **이 원전은 DPR(Karpukhin et al., 2020)을
    인용하지 않는다** — 이 페이지가 두 원전을 견주는 문장은 이 KB의 대조이지 ColBERT 저자들의
    대조가 아니다.
    BERT(Devlin et al., 2018)·
    KNRM·Duet·ConvKNRM·fastText+ConvKNRM·SNRM(Zamani et al., 2018)·DSSM(Huang et al., 2013)·
    duoBERT(Nogueira et al., 2019)·doc2query·docTTTTTquery·DeepCT(Dai and Callan, 2019)·
    TK(Hofstätter et al., 2019)·T5(Raffel et al., 2019)·faiss(Johnson et al., 2017)·
    Anserini(Yang et al., 2018)·MS MARCO(Nguyen et al., 2016)·TREC-CAR(Dietz et al., 2017)·
    Adam(Kingma and Ba, 2014)·WordPiece(Wu et al., 2016)는 khattab2020-colbert를 통한 전언이다.

---
type: concept
title: 모델 증류
description: 작은 학생이 큰 교사를 흉내 내도록 훈련하는 방법 — DistilBERT와 Alpaca의 수치, 많은 라이선스가 이것을 금지한다는 단서, 합성 데이터로 훈련하는 것이 곧 증류는 아니라는 구분, 학생이 교사보다 커진 Nemotron-4의 사례, 그리고 랭킹 과제에서 교사의 순열을 그대로 목표로 삼은 학생이 교사와 지도 학습 짝을 모두 앞선 원전의 실측
generated: { by: "claude-opus-5", at: "2026-08-17T15:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
  - { id: sun2023-rankgpt, resource: /it/sources/sun2023-rankgpt.md }
---

# 모델 증류

- [정의](#정의)
- [왜 하는가 — 배포 비용](#왜-하는가--배포-비용)
- [학생 모델을 만드는 두 길](#학생-모델을-만드는-두-길)
- [라이선스가 막는다](#라이선스가-막는다)
- [어댑터와 함께 쓰이는 자리](#어댑터와-함께-쓰이는-자리)
- [합성 데이터 훈련이 곧 증류는 아니다](#합성-데이터-훈련이-곧-증류는-아니다)
- [자기 출력으로 훈련하는 것의 조건](#자기-출력으로-훈련하는-것의-조건)
- [학생이 교사를 앞서는 자리 — 순열 증류](#학생이-교사를-앞서는-자리--순열-증류)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **큰 모델의 능력을 작은 모델로 옮기는 일은 무엇이고 어디까지 되는가.**

## 정의

- 정의 (8장, p.395):[^huyen2025]

  > *Model distillation* (also called *knowledge distillation*) is a method in which a small model
  > (student) is trained to mimic a larger model (teacher) (Hinton et al., 2015). The knowledge of
  > the big model is distilled into the small model, hence the term distillation.

- 이 절이 놓인 자리 — **AI를 써서 데이터를 생성하는 법과 생성된 데이터를 평가하는 법, 그리고 그
  한계를 논했다. 다음 절에서는 AI 생성 데이터가 보조가 아니라 필수인 데이터 합성의 특별한 유스케이스
  하나로 옮겨 가자: 모델 증류** (8장, p.395).[^huyen2025]

## 왜 하는가 — 배포 비용

- **전통적으로 모델 증류의 목표는 배포를 위한 더 작은 모델을 만드는 것이다. 큰 모델을 배포하는 것은
  자원 집약적일 수 있다. 증류는 교사에 필적하는 성능을 유지하는 더 작고 빠른 학생 모델을 만들 수 있다.
  예컨대 BERT에서 증류된 모델 DistilBERT는 BERT 모델의 크기를 40% 줄이면서 언어 이해 능력의 97%를
  유지하고 60% 더 빠르다(Sanh et al., 2019)** (8장, p.395).[^huyen2025]

## 학생 모델을 만드는 두 길

- **학생 모델은 DistilBERT처럼 처음부터 훈련될 수도 있고 Alpaca처럼 사전 훈련된 모델에서 파인 튜닝될
  수도 있다. 2023년 Taori et al.은 Llama의 70억 파라미터 버전인 Llama-7B를 1,750억 파라미터 모델인
  text-davinci-003이 생성한 예제로 파인 튜닝했다. 그 결과 모델 Alpaca는 교사 모델 크기의 4%이면서
  text-davinci-003과 비슷하게 행동한다** (8장, p.395).[^huyen2025]
- 7장이 같은 접근을 파인 튜닝 쪽에서 부르는 이름은
  [언제 파인 튜닝하는가](../concepts/when-to-finetune.md)에 있다.

## 라이선스가 막는다

- 저자가 경고 상자로 둔 것 (8장, p.395):[^huyen2025]

  > Not all models can be distilled. Many model licenses prohibit using their outputs to train
  > other models, particularly to train competing models.

  그 조항의 지형은 [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md)에 있다.

## 어댑터와 함께 쓰이는 자리

- **합성 지시 데이터는 LoRA 같은 어댑터 기반 기법과 함께 쓰이는 것이 흔하다. 예컨대 BuzzFeed는 LoRA와
  OpenAI의 text-davinci-003이 생성한 예제를 써서 Flan-T5 모델을 파인 튜닝했다. 그 결과 모델은 추론
  비용을 80% 줄였는데, 다만 모델이 얼마나 잘 작동했는지는 불분명했다(2023)** (8장,
  p.396).[^huyen2025] 그 기법은 [LoRA](../concepts/lora.md)에 있다.

## 합성 데이터 훈련이 곧 증류는 아니다

- **합성 데이터로 하는 모든 훈련이 모델 증류인 것은 아니라는 점에 유의하라. 모델 증류는 교사 모델의
  성능이 학생의 금 기준(gold standard)임을 함의한다. 그러나 교사보다 더 크고 강력한 학생 모델을
  훈련하는 데 합성 데이터를 쓰는 것도 가능하다** (8장, p.396).[^huyen2025]
- 두 실물 — **앞 절에서 논한 역방향 지시를 통한 모델 부트스트래핑(Li et al., 2023)이 한 예다. 또 다른
  예는 NVIDIA의 Nemotron-4다. NVIDIA 연구자 팀은 먼저 3,400억 파라미터 베이스 모델을 사전 훈련했다.
  이 베이스 모델은 그다음 560억 파라미터 전문가 혼합 모델인 Mixtral-8x7B-Instruct-v0.1(Jiang et al.,
  2024)이 생성한 지시 데이터와 선호 데이터로 파인 튜닝되었다. 그 결과 학생 모델 Nemotron-4-340B-
  Instruct는 다양한 과제에서 교사 모델을 능가했다(NVIDIA, 2024)** (8장, p.396).[^huyen2025]
  - 각주가 다는 단서 — **Mixtral 같은 전문가 혼합 모델의 파라미터 수를 Nemotron-4 같은 조밀 모델의 것과
    비교하는 것은 공정하지 않지만, 교사 모델(Mixtral)이 학생 모델(Nemotron-4)보다 작다는 요지는 여전히
    성립한다** (8장, p.396 각주 15).[^huyen2025] 그 구조 차이는
    [모델 규모의 세 수치](../concepts/model-size-and-scale.md)에 있다.

## 자기 출력으로 훈련하는 것의 조건

- **Llama 3 논문은 더 유능한 모델이 생성한 데이터로 훈련하는 것이 모델 성능을 크게 개선할 수 있는
  반면, 자기가 생성한 데이터로 무차별적으로 훈련하는 것은 모델 성능을 개선하지 못하고 심지어 떨어뜨릴
  수 있다고 지적한다. 그러나 합성 데이터의 품질을 검증하는 기전을 도입하고 검증된 합성 데이터만 씀으로써
  그들은 모델이 생성한 데이터를 써서 모델을 계속 개선할 수 있었다** (8장, p.396).[^huyen2025] 그
  검증 기전은 [합성 데이터 검증](../concepts/synthetic-data-verification.md)에 있다.

## 학생이 교사를 앞서는 자리 — 순열 증류

- 위의 정의는 **교사 모델의 성능이 학생의 금 기준임을 함의한다**고 적는다.[^huyen2025] 그 함의가
  성립하지 않는 사례가 한 원전에 실측으로 있다.
- 무엇을 증류하는가 — **우리 접근과 앞선 증류 방법의 핵심 차이는 일관성 검사나 로그 확률 조작 같은
  어떤 귀납 편향도 들이지 않고 모델이 생성한 순열(permutation)을 직접 목표로 쓴다는 것이다** (4.1절,
  p.4).[^sun2023-rankgpt] 실물로는 MS MARCO 훈련 집합의 질의 1만 개와 질의마다 BM25가 가져온 후보
  구절 20개를 쓰고, 교사 ChatGPT가 낸 순위를 RankNet 손실로 학생에 넣는다 — **`M`개 구절의 순열로
  `M(M − 1)/2`개 쌍을 만들 수 있다** (4.1–4.2절, p.4).[^sun2023-rankgpt]
- 왜 증류하는가 — **ChatGPT와 GPT-4는 매우 유능하지만 상용 검색 시스템에 배포하기에는 너무 비싸다.
  게다가 큰 언어 모델은 불안정한 생성이라는 문제를 겪는다. 그래서 우리는 큰 언어 모델의 능력이
  리랭킹 과제에는 과잉이라고 주장한다** (4절, p.4).[^sun2023-rankgpt] 배포 비용이라는 동기는 위
  절과 같고, **불안정성**이 하나 더 붙는다.
- 세 가지가 뒤집힌다 (7.1절, p.8, Table 7):[^sun2023-rankgpt]
  - **순열 증류가 지도 학습된 짝을 앞선다** — **ChatGPT의 관련성 판단이 MS MARCO 라벨보다 더
    포괄적이기 때문일 수 있다**고 저자들은 적는다. #hypothesis 곧 교사가 주는 것은 능력만이 아니라
    **라벨의 품질**이다.
  - **증류된 학생이 자기 교사를 앞선다** — BEIR 평균 nDCG로 435M 학생이 53.03, 교사 ChatGPT가
    49.37이다. 저자들이 붙인 설명은 **특화 모델의 리랭킹 안정성이 ChatGPT보다 낫기 때문일
    것**이라는 것이다. #hypothesis
  - **학생이 이전 최고 지도 모델도 앞선다** — 같은 지표로 3B 규모의 monoT5가 51.36이다. 곧 이
    과제에서 증류는 배포 비용을 깎는 절충이 아니라 성능까지 얻는 경로다.
- 무엇을 키울 것인가 — **모델 파라미터 수를 늘리는 것이 훈련 데이터를 늘리는 것보다 랭킹 결과에 더
  큰 개선을 낸다. 또 지도 모델의 성능은 모델 크기와 데이터 크기에 따라 불안정한데, MS MARCO 라벨의
  잡음이 과적합 문제로 이어지기 때문일 수 있다** (7.2절, pp.8–9, Figure 4).[^sun2023-rankgpt]
  #hypothesis
- 조건 — 이 실측은 **리랭킹이라는 좁은 과제**의 것이고, 교사가 그 과제의 금 기준이 아닐 때(라벨
  잡음이 클 때) 학생이 교사를 넘는다는 구도다. 위 Nemotron-4의 사례가 **교사보다 큰 학생**의
  경우였다면 여기는 **교사보다 작은 학생**이 넘는 경우다.[^huyen2025] 그 리랭킹 과제 자체는
  [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)에 있다.

## 이어지는 페이지

- [데이터 증강과 합성](../concepts/data-augmentation-and-synthesis.md) — 증류가 합성의 다섯째 이유로
  꼽히는 자리
- [AI 생성 데이터의 한계](../concepts/limitations-of-ai-generated-data.md) — 피상적 모방이 증류를
  제한하는 자리
- [합성 데이터 검증](../concepts/synthetic-data-verification.md) — 자기 출력으로 훈련할 때의 조건
- [언제 파인 튜닝하는가](../concepts/when-to-finetune.md) — 작은 모델을 파인 튜닝하는 쪽의 7장 서술
- [파인 튜닝의 세 선택](../concepts/finetuning-setup-choices.md) — 증류 경로가 이름으로 나오는 자리
- [오픈소스 모델과 라이선스](../concepts/open-source-models-and-licenses.md) — 출력 사용 금지 조항
- [LoRA](../concepts/lora.md) — 증류된 학생을 싸게 만드는 기법
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — 전문가 혼합과 조밀 모델의 파라미터 비교
- [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md) — 순열 증류가 놓인 과제
- [검색 품질 평가](../concepts/retrieval-evaluation.md) — nDCG가 재는 것

[^sun2023-rankgpt]: Sun et al. 2023, "Is ChatGPT Good at Search? Investigating Large Language
    Models as Re-Ranking Agents", EMNLP 2023 본회의 (인쇄 쪽 14918–14937). 학회 공식 페이지가
    Outstanding Paper로 표기한다. 쪽 번호는 스냅샷한 PDF의 쪽이다(PDF p.1 = 인쇄 p.14918).
    이 페이지는 2.2절 LLMs Specialization·4절 Specialization by Permutation Distillation(4.1–4.2)·
    7절 Experimental Results of Specialization(7.1–7.2)만 담았다 — 리랭킹 방법 자체는
    [하이브리드 검색과 리랭킹](../concepts/hybrid-search-and-reranking.md)이 담는다. Table 7의
    수치는 표 형태로 옮기지 않고 본문 서술로만 담았고, Figure 4(모델 크기·데이터 크기 확장, p.8)는
    옮기지 않았다.
    **원문 안에서 수치가 어긋나는 자리 하나** — 초록은 증류된 학생을 **440M**이라 적고 1절과
    Table 7·Figure 4는 **435M**(deberta-v3-large)이라 적는다. 이 페이지는 표에 인쇄된 435M을 쓴다.
    monoT5(Nogueira et al., 2020)는 이 KB에 원전이 있다. RankNet(Burges et al., 2005)·
    DeBERTa·LLaMA(Touvron et al., 2023)·MS MARCO·BEIR(Thakur et al., 2021)·
    Arabzadeh et al.(2021)은 sun2023-rankgpt를 통한 전언이다.

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Model Distillation"
    (pp.395–396). 이 구간에는 도판이 없다. Hinton et al.(2015)·Sanh et al.(2019)·Taori et al.·
    BuzzFeed(2023)·Li et al.(2023)·Jiang et al.(2024)·NVIDIA(2024)·Llama 3 논문은 huyen2025를 통한
    전언이다.

---
type: concept
title: LoRA
status: draft
description: 가중치 행렬을 두 작은 행렬의 곱으로 분해해 그 둘만 갱신하는 어댑터 기법 — 추론 지연을 늘리지 않는 이유, 저차원 인수분해라는 오래된 발상과 GPT-3에서 0.0027%의 파라미터로 붙은 성능, 왜 이것이 통하는가에 대한 내재 차원 가설, 어느 행렬에 얼마의 rank로 적용할지의 선택, 그리고 양자화를 겹친 QLoRA
generated: { by: "claude-opus-5", at: "2026-08-17T05:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# LoRA

- [원래 어댑터와 무엇이 다른가](#원래-어댑터와-무엇이-다른가)
- [LoRA가 하는 세 단계](#lora가-하는-세-단계)
- [저차원 인수분해](#저차원-인수분해)
- [GPT-3에서의 수치](#gpt-3에서의-수치)
- [왜 LoRA는 통하는가](#왜-lora는-통하는가)
- [사전 훈련에는 왜 안 쓰는가](#사전-훈련에는-왜-안-쓰는가)
- [어느 행렬에 적용하는가](#어느-행렬에-적용하는가)
- [rank는 얼마로](#rank는-얼마로)
- [알파와 rank의 비](#알파와-rank의-비)
- [LoRA의 단점](#lora의-단점)
- [양자화 LoRA](#양자화-lora)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **원래 가중치를 그대로 두고 어떻게 적은 파라미터만으로 모델을 파인 튜닝하는가.**

## 원래 어댑터와 무엇이 다른가

- **Houlsby et al.(2019)의 원래 어댑터 방법과 달리 LoRA(Low-Rank Adaptation)(Hu et al., 2021)는
  추가 추론 지연을 초래하지 않는 방식으로 추가 파라미터를 통합한다. 베이스 모델에 추가 층을 도입하는
  대신 LoRA는 원래 층으로 다시 병합될 수 있는 모듈을 쓴다** (7장, p.338).[^huyen2025]
- 저자가 이 절을 크게 두는 이유 — **LoRA의 인기 때문에 다음 절은 LoRA가 어떻게 작동하고 초기 어댑터
  기반 방법이 제기한 난제를 어떻게 푸는지에 초점을 둔다. LoRA를 쓰지 않더라도 이 깊이 있는 탐구가
  다른 파인 튜닝 방법을 탐색하는 틀을 제공할 것이다** (7장, p.338).[^huyen2025]

## LoRA가 하는 세 단계

- **개별 가중치 행렬에 LoRA를 적용할 수 있다. 가중치 행렬이 주어지면 LoRA는 이 행렬을 두 개의 더
  작은 행렬의 곱으로 분해하고, 그 두 작은 행렬을 갱신한 뒤 원래 행렬로 다시 병합한다** (7장,
  p.339).[^huyen2025]
- **차원 n × m의 가중치 행렬 W를 생각하자. LoRA는 다음과 같이 작동한다** (7장,
  p.339):[^huyen2025]
  1. **먼저 더 작은 행렬들의 차원을 고른다. 고른 값을 r이라 하자. 두 행렬 A(차원 n × r)와 B(차원
     r × m)를 만든다. 그 곱이 W_AB이고 W와 같은 차원이다. r이 LoRA rank다.**
  2. **W_AB를 원래 가중치 행렬 W에 더해 새 가중치 행렬 W′를 만든다. 모델의 일부로 W 대신 W′를
     쓴다. 하이퍼파라미터 α를 써서 W_AB가 새 행렬에 얼마나 기여할지 정할 수 있다.**

     ```math
     W' = W + \frac{\alpha}{r} W_{AB}
     ```

  3. **파인 튜닝 중에는 A와 B의 파라미터만 갱신한다. W는 그대로 유지된다.**

## 저차원 인수분해

- 저자가 상자로 떼어 둔 배경 — **LoRA(Low-Rank Adaptation)는 오래된 차원 축소 기법인 저차원
  인수분해(low-rank factorization) 개념 위에 세워졌다. 핵심 발상은 큰 행렬을 두 개의 더 작은 행렬의
  곱으로 인수분해해 파라미터 수를 줄이고, 그것이 다시 계산과 메모리 요구를 둘 다 줄인다는 것이다.
  예컨대 9 × 9 행렬은 차원 9 × 1과 1 × 9인 두 행렬의 곱으로 인수분해될 수 있다. 원래 행렬은
  파라미터가 81개지만 두 곱 행렬은 합쳐서 18개뿐이다** (7장, p.340).[^huyen2025]
  - rank라는 이름의 자리 — **첫 인수분해 행렬의 열 수와 둘째 인수분해 행렬의 열 수가 인수분해의
    rank에 대응한다. 원래 행렬은 full-rank이고 두 작은 행렬은 저차원 근사(low-rank approximation)를
    나타낸다** (7장, p.340).[^huyen2025]
  - 손실이 있다 — **인수분해가 파라미터 수를 크게 줄일 수 있지만 원래 행렬을 근사할 뿐이므로
    손실적(lossy)이다. rank가 높을수록 인수분해가 원래 행렬의 정보를 더 많이 보존할 수 있다** (7장,
    p.340).[^huyen2025]

## GPT-3에서의 수치

- **원래 어댑터 방법처럼 LoRA는 파라미터 효율적이고 표본 효율적이다. 인수분해는 LoRA가 훈련 가능
  파라미터를 더욱 적게 쓰게 해 준다. LoRA 논문은 GPT-3에 대해 LoRA가 훈련 가능 파라미터 약
  4.7M — 전체 파인 튜닝의 0.0027% — 만 쓰면서 여러 과제에서 전체 파인 튜닝에 필적하거나 더 나은
  성능을 달성함을 보였다** (7장, p.340).[^huyen2025]

## 왜 LoRA는 통하는가

- 저자가 던지는 질문 (7장, p.340):[^huyen2025]

  > Parameter-efficient methods like LoRA have become so popular that many people take them for
  > granted. *But why is parameter efficiency possible at all?* If a model requires a lot of parameters
  > to learn certain behaviors during pre-training, shouldn't it also require a lot of parameters to
  > change its behaviors during finetuning?

  - 데이터에 대한 같은 질문 — **같은 질문을 데이터에 대해서도 제기할 수 있다. 모델이 어떤 행동을
    배우는 데 많은 데이터가 필요하다면 그 행동을 유의미하게 바꾸는 데도 많은 데이터가 필요해야 하지
    않는가? 모델을 사전 훈련하는 데는 수백만 또는 수십억 개의 예시가 필요한데 파인 튜닝하는 데는
    수백 또는 수천 개만 필요한 것이 어떻게 가능한가?** (7장, p.340).[^huyen2025]
- 답의 후보 — **많은 논문이 LLM에 파라미터는 많지만 내재 차원(intrinsic dimensions)은 아주 낮다고
  주장해 왔다. Li et al.(2018), Aghajanyan et al.(2020), Hu et al.(2021)을 보라. 그들은 사전
  훈련이 암묵적으로 모델의 내재 차원을 최소화한다는 것을 보였다. 놀랍게도 더 큰 모델이 사전 훈련 뒤
  더 낮은 내재 차원을 갖는 경향이 있다. 이는 사전 훈련이 다운스트림 과제를 위한 압축 틀 노릇을 함을
  시사한다. 달리 말해 LLM이 더 잘 훈련되어 있을수록 적은 수의 훈련 가능 파라미터와 적은 양의
  데이터로 그 모델을 파인 튜닝하기가 더 쉽다** (7장, p.340).[^huyen2025]

## 사전 훈련에는 왜 안 쓰는가

- 자연스러운 질문 — **저차원 인수분해가 그렇게 잘 통한다면 사전 훈련에도 LoRA를 쓰지 않는 이유가
  무엇인지 궁금할 수 있다. 큰 모델을 사전 훈련한 뒤 파인 튜닝 중에만 저차원 인수분해를 적용하는
  대신, 사전 훈련의 시작부터 모델을 인수분해할 수는 없는가? 저차원 사전 훈련은 모델의 파라미터 수를
  크게 줄여 사전 훈련 시간과 비용을 크게 줄일 수 있다** (7장, p.341).[^huyen2025]
- 2010년대의 시도들 — **2010년대 내내 많은 사람이 저차원 신경망을 훈련하려 시도했다. "Low-Rank
  Matrix Factorization for Deep Neural Network Training with High-Dimensional Output Targets"
  (Sainath et al., 2013), "Semi-Orthogonal Low-Rank Matrix Factorization for Deep Neural Networks"
  (Povey et al., 2018), "Speeding up Convolutional Neural Networks with Low Rank Expansions"
  (Jaderberg et al., 2014) 같은 연구가 그 예다** (7장, p.341).[^huyen2025]
- 작은 규모에서는 통했다 — **저차원 인수분해는 더 작은 규모에서 효과적임이 증명되었다. 예컨대 3 × 3
  합성곱을 1 × 1 합성곱으로 바꾸는 것을 포함한 여러 인수분해 전략을 적용해 SqueezeNet(Iandola et
  al., 2016)은 50배 적은 파라미터로 ImageNet에서 AlexNet 수준의 정확도를 달성했다** (7장,
  p.341).[^huyen2025]
- 더 최근의 시도 — **저차원 LLM을 훈련하려는 더 최근의 시도로 ReLoRA(Lialin et al., 2023)와
  GaLore(Zhao et al., 2024)가 있다. ReLoRA는 최대 1.3B 파라미터의 트랜스포머 기반 모델에 대해
  작동한다. GaLore는 1B 파라미터에서 full-rank 모델에 필적하는 성능을, 7B 파라미터에서 유망한
  성능을 달성한다** (7장, p.341).[^huyen2025]
- 남는 논점 — **머지않은 미래에 연구자들이 저차원 사전 훈련을 수천억 파라미터로 확장할 방법을 개발할
  가능성도 있다. 그러나 Aghajanyan et al.의 주장 — 사전 훈련이 암묵적으로 모델의 내재 차원을
  압축한다는 것 — 이 옳다면, 저차원 인수분해가 작동할 수 있는 지점까지 모델의 내재 차원을 충분히
  줄이려면 여전히 full-rank 사전 훈련이 필요하다. 저차원 훈련으로 전환하는 것이 가능해지기 전에
  full-rank 훈련이 정확히 얼마나 필요한지 연구하는 것은 흥미로울 것이다** (7장,
  p.341).[^huyen2025]

## 어느 행렬에 적용하는가

- 두 결정 — **LoRA를 적용하려면 어떤 가중치 행렬에 LoRA를 적용할지, 그리고 각 인수분해의 rank를
  얼마로 할지를 정해야 한다** (7장, p.341).[^huyen2025]
- 구조에 달려 있다 — **LoRA는 개별 가중치 행렬마다 적용될 수 있다. 따라서 LoRA의 효율은 LoRA가 어떤
  행렬에 적용되는지만이 아니라 모델의 구조에도 달려 있다. 서로 다른 구조는 서로 다른 가중치 행렬을
  갖기 때문이다** (7장, p.341).[^huyen2025]
- 실제로 어디에 붙는가 — **합성곱 신경망 같은 다른 구조에 LoRA를 쓴 예도 있었지만(Dutt et al.,
  2023; Zhong et al., 2024; Aleem et al., 2024) LoRA는 주로 트랜스포머 모델에 쓰여 왔다. LoRA는
  어텐션 모듈의 네 가중치 행렬 — 질의(W_q)·키(W_k)·값(W_v)·출력 사영(W_o) 행렬 — 에 적용되는 것이
  가장 흔하다** (7장, p.342).[^huyen2025]
- 균일하게 적용한다 — **통상 LoRA는 모델 안의 같은 유형 행렬 전부에 균일하게 적용된다. 예컨대 질의
  행렬에 LoRA를 적용한다는 것은 모델 안의 모든 질의 행렬에 LoRA를 적용한다는 뜻이다** (7장,
  p.342).[^huyen2025]
- 예산이 있을 때의 질문 — **소박하게는 이 어텐션 행렬 전부에 LoRA를 적용할 수 있다. 그러나 흔히
  하드웨어의 메모리에 제약되어 고정된 수의 훈련 가능 파라미터만 수용할 수 있다. 훈련 가능 파라미터의
  고정 예산이 주어졌을 때 성능을 최대화하려면 어떤 행렬에 LoRA를 적용해야 하는가?** (7장,
  p.342).[^huyen2025]
- Hu et al.이 실제로 한 배분 — **GPT-3 175B를 파인 튜닝할 때 Hu et al.(2021)은 훈련 가능 파라미터
  예산을 18M으로 잡았는데 이는 모델 전체 파라미터 수의 0.01%다. 이 예산은 다음을 허용한다** (7장,
  p.342):[^huyen2025]
  1. **rank 8인 행렬 하나**
  2. **rank 4인 행렬 둘**
  3. **rank 2인 네 행렬 전부**
  - 저자가 옆에 붙인 산수 — **GPT-3 175B는 모델 차원 12,288의 트랜스포머 층 96개를 갖는다. 네 행렬
    전부에 rank = 2로 LoRA를 적용하면 층당 (12,288 × 2 × 2) × 4 = 196,608개, 모델 전체로는
    18,874,368개의 훈련 가능 파라미터가 나온다** (7장, p.342).[^huyen2025]
- 결과 — **그들은 네 행렬 전부에 rank = 2로 LoRA를 적용하는 것이 WikiSQL(Zhong et al., 2017)과
  MultiNLI(Multi-Genre Natural Language Inference) 벤치마크(Williams et al., 2017)에서 최고 성능을
  낸다는 것을 발견했다. 그러나 저자들은 어텐션 행렬을 둘만 고를 수 있다면 질의와 값 행렬이 일반적으로
  최선의 결과를 낸다고 제안했다** (7장, pp.342–343).[^huyen2025]
- 훈련 가능 파라미터 18M 예산에서의 결과다. 원문 표기를 그대로 옮겼다 (7장, p.343, Table
  7-5):[^huyen2025]

  | Weight type | W_q | W_k | W_v | W_o | W_q, W_k | W_q, W_v | W_q, W_k, W_v, W_o |
  |---|---|---|---|---|---|---|---|
  | Rank r | 8 | 8 | 8 | 8 | 4 | 4 | 2 |
  | WikiSQL (± 0.5%) | 70.4 | 70.0 | 73.0 | 73.2 | 71.4 | 73.7 | 73.7 |
  | MultiNLI (± 0.1%) | 91.0 | 90.8 | 91.0 | 91.3 | 91.3 | 91.3 | 91.7 |

- 어텐션 밖으로 — **경험적 관찰은 피드포워드 행렬을 포함해 더 많은 가중치 행렬에 LoRA를 적용하는
  것이 더 나은 결과를 낸다고 시사한다. 예컨대 Databricks는 자기들이 얻은 가장 큰 성능 향상이 모든
  피드포워드 층에 LoRA를 적용한 데서 나왔음을 보였다(Sooriyarachchi, 2023). Fomenko et al.(2024)은
  피드포워드 기반 LoRA가 어텐션 기반 LoRA와 상보적일 수 있으나 메모리 제약 안에서는 어텐션 기반
  LoRA가 통상 더 큰 효능을 제공한다고 짚었다** (7장, p.343).[^huyen2025]

## rank는 얼마로

- 저자가 LoRA의 아름다움이라 부르는 것 (7장, p.343):[^huyen2025]

  > The beauty of LoRA is that while its performance depends on its rank, studies have shown that *a
  > small r, such as between 4 and 64, is usually sufficient for many use cases.*

  - **더 작은 r은 LoRA 파라미터가 적다는 뜻이고 이는 더 낮은 메모리 발자국으로 이어진다** (7장,
    p.343).[^huyen2025]
- 저자들이 놀란 관측 — **LoRA 저자들은 놀랍게도 r 값을 늘리는 것이 파인 튜닝 성능을 늘리지 않음을
  관찰했다. 이 관측은 "어떤 값을 넘어 r을 늘리는 것이 모델 출력 품질에서 식별 가능한 증가를 내놓지
  않을 수 있다"는 Databricks의 보고와 일치한다(Sooriyarachchi, 2023). 어떤 사람은 더 높은 r이
  과적합으로 이어질 수 있어 오히려 해로울 수 있다고 주장한다. 그러나 어떤 경우에는 더 높은 rank가
  필요할 수 있다. Raschka(2023)는 r = 256이 자기 과제에서 최고 성능을 달성했음을 발견했다** (7장,
  p.343).[^huyen2025]
  - 각주 — **집필 시점 기준 Fireworks 같은 일부 파인 튜닝 프레임워크는 최대 LoRA rank 32만 허용한다.
    그러나 이 제약은 성능 때문일 가능성은 낮고 그들 하드웨어의 메모리 제약 때문일 가능성이 높다**
    (7장, p.343 각주 25).[^huyen2025]

## 알파와 rank의 비

- **구성할 수 있는 또 다른 LoRA 하이퍼파라미터가 α 값인데, 이는 병합 중에 곱 W_AB가 새 행렬에 얼마나
  기여할지를 정한다. 실무에서 저자는 α : r 비가 통상 1:8에서 8:1 사이가 되도록 α가 선택되는 것을
  자주 보았지만 최적 비는 다양하다. 예컨대 r이 작으면 α를 더 크게 하고 싶을 수 있고, r이 크면 α를
  더 작게 하고 싶을 수 있다. 유스케이스에 맞는 최선의 (r, α) 조합을 정하려면 실험이 필요하다**
  (7장, p.343).[^huyen2025]

## LoRA의 단점

- **"LoRA는 좋아 보이는데 함정이 뭔가?"라고 궁금할 수 있다. LoRA의 주된 단점은 전체 파인 튜닝만큼
  강한 성능을 제공하지 않는다는 것이다. 모델의 구현을 수정하는 것을 수반해 모델 구조와 코딩 기술에
  대한 이해를 요구하므로 전체 파인 튜닝보다 하기가 더 어렵기도 하다. 그러나 이는 통상 덜 인기 있는
  베이스 모델에서만 문제다. 허깅 페이스의 PEFT·Axolotl·unsloth·LitGPT 같은 PEFT 프레임워크는
  인기 있는 베이스 모델에 대해 LoRA를 바로 지원할 가능성이 높다** (7장, p.345).[^huyen2025]

## 양자화 LoRA

- 파라미터를 더 줄이는 길의 한계 — **LoRA의 급격한 부상은 수많은 LoRA 변종의 개발로 이어졌다. 어떤
  것은 훈련 가능 파라미터 수를 더 줄이는 것을 목표로 한다. 그러나 LoRA 어댑터의 메모리는 모델
  가중치의 메모리에 비하면 미미하다. LoRA 파라미터 수를 줄이는 것은 전체 메모리 발자국을 아주 작은
  비율만 줄인다** (7장, p.345).[^huyen2025]
- LoRA 가중치에 필요한 메모리와 모델 가중치에 필요한 메모리의 대비다. 원문 표기를 그대로 옮겼다
  (7장, p.345, Table 7-6):[^huyen2025]

  | | Model's weights memory (16 bits) | LoRA trainable params (r=2, query & key matrices) | LoRA adapter memory (16 bits) |
  |---|---|---|---|
  | Llama 2 (13B) | 26 GB | 3.28M | 6.55 MB |
  | GPT-3 (175B) | 350 GB | 18.87M | 37.7 MB |

- 그래서 다른 길 — **LoRA의 파라미터 수를 줄이려 애쓰기보다 파인 튜닝 중에 모델의 가중치·활성화·
  기울기를 양자화해 메모리 사용을 더 효과적으로 줄일 수 있다. LoRA의 초기 유망한 양자화 버전이
  QLoRA(Dettmers et al., 2023)다. 원래 LoRA 논문에서는 파인 튜닝 중 모델의 가중치가 16비트로
  저장된다. QLoRA는 모델의 가중치를 4비트로 저장하되 순전파와 역전파를 계산할 때 BF16으로 역양자화
  (변환)한다** (7장, p.346).[^huyen2025]
  - 각주 — **QLoRA가 유일한 양자화 LoRA 작업은 아니다. 많은 연구소가 공개적으로 논의하지 않으면서
    양자화 LoRA를 작업해 왔다** (7장, p.346 각주 27).[^huyen2025]
- 4비트 형식의 정체 — **QLoRA가 쓰는 4비트 형식은 NF4(NormalFloat-4)로, 사전 훈련된 가중치가 대개
  중앙값 0의 정규 분포를 따른다는 통찰에 기반해 값을 양자화한다. 4비트 양자화 위에 QLoRA는 GPU가
  메모리 부족일 때, 특히 긴 시퀀스 길이에서 CPU와 GPU 사이에 데이터를 자동으로 옮기는 페이지드
  옵티마이저(paged optimizers)도 쓴다. 이 기법들은 65B 파라미터 모델이 단일 48 GB GPU에서 파인
  튜닝될 수 있게 한다** (7장, p.346).[^huyen2025]
- Guanaco — **저자들은 Llama 7B부터 65B까지 다양한 모델을 4비트 모드에서 파인 튜닝했다. 그 결과로
  나온 모델 계열은 Guanaco라 불리며 공개 벤치마크와 비교 평가 양쪽에서 경쟁력 있는 성능을 보였다.
  Guanaco 65B는 GPT-4를 능가하지 못했지만 ChatGPT보다 자주 선호되었다** (7장,
  p.346).[^huyen2025]
- 2023년 5월에 GPT-4를 판정자로 써서 매긴 Elo 등급이다. 원문 표기를 그대로 옮겼다 (7장, p.346,
  Table 7-7):[^huyen2025]

  | Model | Size | Elo |
  |---|---|---|
  | GPT-4 | - | 1348 ± 1 |
  | Guanaco 65B | 41 GB | 1022 ± 1 |
  | Guanaco 33B | 21 GB | 992 ± 1 |
  | Vicuna 13B | 26 GB | 974 ± 1 |
  | ChatGPT | - | 966 ± 1 |
  | Guanaco 13B | 10 GB | 916 ± 1 |
  | Bard | - | 902 ± 1 |
  | Guanaco 7B | 6 GB | 879 ± 1 |

- 한계 — **QLoRA의 주된 한계는 NF4 양자화가 비싸다는 것이다. QLoRA가 메모리 발자국을 줄일 수 있지만
  양자화와 역양자화 단계에 필요한 추가 시간 때문에 훈련 시간을 늘릴 수 있다** (7장,
  p.346).[^huyen2025]
- 그 뒤의 작업들 — **메모리 절감의 약속 때문에 양자화 LoRA는 활발한 연구 영역이다. QLoRA 말고도
  양자화 LoRA 작업에는 QA-LoRA(Xu et al., 2023), ModuLoRA(Yin et al., 2023), IR-QLoRA(Qin et al.,
  2024)가 있다** (7장, p.347).[^huyen2025]

## 이어지는 페이지

- [LoRA 어댑터 서빙](../inbox/serving-lora-adapters.md) — 모듈성이 서빙에서 갚는 것
- [파라미터 효율 파인 튜닝](../inbox/parameter-efficient-finetuning.md) — LoRA가 속한 계열과 그
  형제들
- [양자화](../inbox/quantization.md) — QLoRA가 딛는 정밀도 감소의 전모
- [모델 메모리 산수](../inbox/model-memory-math.md) — 훈련 가능 파라미터가 메모리로 바뀌는 공식
- [모델 병합의 접근들](../inbox/model-merging-approaches.md) — LoRA 어댑터가 병합의 재료가 되는
  자리
- [트랜스포머 구조](../concepts/transformer-architecture.md) — 질의·키·값·출력 사영 행렬이
  사는 곳
- [파인 튜닝의 세 선택](../inbox/finetuning-setup-choices.md) — LoRA를 택할지 전체 파인 튜닝을
  택할지의 실무 기준
- [비교 평가](../concepts/comparative-evaluation.md) — Elo 등급이 매겨지는 방식

[^huyen2025]: Huyen 2025, 7장 "Finetuning" (책 pp.307–362). 이 페이지는 "Finetuning Techniques"
    절의 "LoRA"(pp.338–343)와 그 하위 절 "Quantized LoRA"(pp.345–347)를 담았다. 같은 절의
    "Serving LoRA adapters"(pp.343–345)는 [LoRA 어댑터 서빙](../inbox/serving-lora-adapters.md)이
    담았다. Table 7-5(p.343)·Table 7-6(p.345)·Table 7-7(p.346)은 원문 표기를 그대로 옮겼다 —
    Table 7-5에서 원문이 굵게 표시한 최고값(WikiSQL의 73.7 둘, MultiNLI의 91.7)의 강조는 마크다운
    표에서 재현하지 않았다. Figure 7-11(가중치 행렬 분해 도식, p.339)은 그림을 옮기지 않고 본문의
    세 단계가 서술한 것만 담았다. Hu et al.(2021)·Houlsby et al.(2019)·Li et al.(2018)·Aghajanyan
    et al.(2020)·Sainath et al.(2013)·Povey et al.(2018)·Jaderberg et al.(2014)·Iandola et
    al.(2016)·Lialin et al.(2023)·Zhao et al.(2024)·Dutt et al.(2023)·Zhong et al.(2024)·Aleem
    et al.(2024)·Zhong et al.(2017)·Williams et al.(2017)·Sooriyarachchi(2023)·Fomenko et
    al.(2024)·Raschka(2023)·Dettmers et al.(2023)·Xu et al.(2023)·Yin et al.(2023)·Qin et
    al.(2024)은 huyen2025를 통한 전언이다.

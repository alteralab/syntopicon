---
type: concept
title: 대안 모델 구조
status: draft
description: 트랜스포머를 대체하려는 시도가 왜 어려운지와 그럼에도 자리를 얻고 있는 것들 — 유행이 오간 구조들의 연표, 새 구조가 넘어야 하는 규모와 하드웨어의 문턱, RNN 기반 RWKV, 상태 공간 모델의 S4·H3·Mamba, 그리고 트랜스포머와 엮은 Jamba
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 대안 모델 구조

- [유행은 오간다](#유행은-오간다)
- [새 구조가 넘어야 하는 문턱](#새-구조가-넘어야-하는-문턱)
- [RWKV](#rwkv)
- [상태 공간 모델의 계보](#상태-공간-모델의-계보)
- [구조가 바뀌면 무엇이 바뀌는가](#구조가-바뀌면-무엇이-바뀌는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **트랜스포머를 밀어낼 구조가 나오기 어려운 이유는 무엇이고, 지금 무엇이 자리를
얻고 있는가.**

## 유행은 오간다

- 저자가 잡는 연표 — **트랜스포머 모델이 지형을 지배하지만 유일한 구조는 아니다. AlexNet이 2012년
  딥러닝에 대한 관심을 되살린 이래 많은 구조가 유행에 들고 났다. seq2seq는 4년간(2014–2018) 각광을
  받았다. GAN(generative adversarial network, 생성적 적대 신경망)은 조금 더 오래(2014–2019)
  집단적 상상을 사로잡았다. 앞서 온 구조들에 비해 트랜스포머는 끈질기다. 2017년부터 있어 왔다**
  (2장, p.65).[^huyen2025]
  - 각주의 사족 — **재미있는 사실 하나: OpenAI 공동 창업자 일리야 수츠케버는 seq2seq 논문의 제1
    저자이자 AlexNet 논문의 제2 저자다** (2장, p.65 각주 10).[^huyen2025]

## 새 구조가 넘어야 하는 문턱

- 문턱의 정의 — **트랜스포머를 능가할 새 구조를 개발하는 것은 쉽지 않다. 트랜스포머는 2017년
  이래 무겁게 최적화되어 왔다. 트랜스포머를 대체하려는 새 구조는 사람들이 신경 쓰는 규모에서,
  사람들이 신경 쓰는 하드웨어 위에서 성능을 내야 할 것이다** (2장, p.65).[^huyen2025]
  - 각주에 실린 수츠케버의 논거 — **일리야 수츠케버는 왜 기존 구조를 능가하는 새 신경망 구조를
    개발하기가 그토록 어려운지에 대해 흥미로운 주장을 갖고 있다. 그의 주장에 따르면 신경망은 많은
    컴퓨터 프로그램을 시뮬레이션하는 데 뛰어나다. 신경망을 훈련하는 기법인 경사 하강은 사실 기존
    구조가 담고 있는 모든 프로그램을 훑어 그 목표 과제에 가장 좋은 것을 찾는 탐색 알고리즘이다.
    이는 새 구조 또한 기존 구조에 의해 잠재적으로 시뮬레이션될 수 있다는 뜻이다. 새 구조가 기존
    구조를 능가하려면, 기존 구조가 시뮬레이션할 수 없는 프로그램을 이 새 신경망이 시뮬레이션할 수
    있어야 한다** (2장, p.65 각주 11).[^huyen2025]
  - 하드웨어 쪽 각주 — **트랜스포머는 원래 구글이 TPU(Tensor Processing Unit)에서 빠르게 돌도록
    설계했고, GPU에는 나중에야 최적화되었다** (2장, p.65 각주 12).[^huyen2025]
- 그럼에도 — **희망은 있다. 트랜스포머 기반 모델이 집필 시점 기준 지배적이지만 몇몇 대안 구조가
  힘을 얻고 있다** (2장, p.65).[^huyen2025]

## RWKV

- **인기 있는 모델 하나가 RWKV(Peng et al., 2023)로, 훈련을 병렬화할 수 있는 RNN 기반 모델이다.
  RNN이라는 성격 덕에 이론적으로는 트랜스포머 기반 모델이 갖는 맥락 길이 제한을 갖지 않는다.
  그러나 실제로는 맥락 길이 제한이 없다는 것이 긴 맥락에서 좋은 성능을 보장하지는 않는다** (2장,
  p.65).[^huyen2025]

## 상태 공간 모델의 계보

- 왜 이 축인가 — **긴 시퀀스를 모델링하는 것은 LLM 개발의 핵심 난제로 남아 있다. 장거리 기억에서
  많은 가능성을 보인 구조가 SSM(state space model, 상태 공간 모델)이다(Gu et al., 2021a). 2021년
  이 구조가 도입된 이래 SSM을 더 효율적이고, 긴 시퀀스 처리에 더 낫고, 더 큰 모델 크기로 확장
  가능하게 만드는 여러 기법이 도입되었다** (2장, p.65).[^huyen2025] 저자는 이 계보를 하나의 구조가
  진화하는 실물로 든다.
- 네 단계다 (2장, p.66):[^huyen2025]
  - **S4 — "Efficiently Modeling Long Sequences with Structured State Spaces"(Gu et al., 2021b)
    에서 도입되었고 SSM을 더 효율적으로 만들려고 개발되었다.**
  - **H3 — "Hungry Hungry Hippos: Towards Language Modeling with State Space Models"(Fu et al.,
    2022)에서 도입되었고, 모델이 이른 토큰을 회상하고 시퀀스 간에 토큰을 비교할 수 있게 하는
    메커니즘을 포함한다. 이 메커니즘의 목적은 트랜스포머 구조의 어텐션 메커니즘과 비슷하되 더
    효율적이다.**
  - **Mamba — "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"(Gu and Dao,
    2023)에서 도입되었고 SSM을 30억 파라미터로 확장한다. 언어 모델링에서 Mamba-3B는 같은 크기의
    트랜스포머를 능가하고 그 두 배 크기의 트랜스포머와 맞먹는다. 저자들은 또한 Mamba의 추론 계산이
    시퀀스 길이에 선형으로 확장됨을 보인다(트랜스포머의 이차 확장과 대비된다). 그 성능은 실제
    데이터에서 100만 길이 시퀀스까지 개선을 보인다.**
  - **Jamba — "Jamba: A Hybrid Transformer–Mamba Language Model"(Lieber et al., 2024)에서
    도입되었고, SSM을 한층 더 확장하려고 트랜스포머 층과 Mamba 층의 블록을 엮는다. 저자들은 단일
    80GB GPU에 들어가도록 설계된 총 가용 파라미터 52B(활성 파라미터 12B)의 전문가 혼합 모델을
    공개했다. Jamba는 표준 언어 모델 벤치마크와 맥락 길이 256K 토큰까지의 장맥락 평가에서 강한
    성능을 보인다. 바닐라 트랜스포머에 비해 메모리 사용량도 작다.**

## 구조가 바뀌면 무엇이 바뀌는가

- 저자의 답 (2장, p.66):[^huyen2025]

  > While it's challenging to develop an architecture that outperforms the transformer, given its
  > many limitations, there are a lot of incentives to do so. If another architecture does indeed
  > overtake the transformer, some of the model adaptation techniques discussed in this book might
  > change. However, just as the shift from ML engineering to AI engineering has kept many things
  > unchanged, changing the underlying model architecture won't alter the fundamental approaches.

## 이어지는 페이지

- [트랜스포머 구조](../concepts/transformer-architecture.md) — 이들이 대체하려는 구조와 그 한계
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — Jamba가 쓰는 전문가 혼합과 활성
  파라미터의 뜻
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 구조가 바뀌어도 남는다는 그 기법들
- [AI 엔지니어링과 ML 엔지니어링](../concepts/ai-engineering-versus-ml-engineering.md) — 저자가
  견주는 그 전환의 실물

[^huyen2025]: Huyen 2025, 2장 "Understanding Foundation Models" (책 pp.49–112). 이 페이지는
    "Other model architectures" 절(pp.65–66)을 담았다. 도판 Figure 2-7(트랜스포머·Mamba·Jamba
    블록 구성, p.67)은 옮기지 않았다. Peng et al.(2023)·Gu et al.(2021a·2021b)·Fu et al.(2022)·
    Gu and Dao(2023)·Lieber et al.(2024)과 수츠케버의 주장은 huyen2025를 통한 전언이다.

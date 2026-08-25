---
type: concept
title: 왜 자기 어텐션인가
description: 트랜스포머 원전이 순환과 합성곱을 걷어낸 근거 — 층당 계산량·병렬화 가능량·경로 길이라는 세 척도, scaled dot-product attention의 정의와 √d_k로 나누는 이유, 멀티 헤드의 동기, 위치 인코딩을 사인과 코사인으로 고른 이유, 그리고 저자들이 WMT 2014에서 직접 잰 BLEU와 훈련 비용, 표 3의 변형 실험. 논문집 판과 arXiv v7의 EN-FR 수치가 다르다는 사실도 함께
generated: { by: "claude-fable-5", at: "2026-08-25T00:00:00Z" }
sources:
  - { id: vaswani2017-attention, resource: /it/sources/vaswani2017-attention.md }
---

# 왜 자기 어텐션인가

- [등급과 그 등급이 여는 범위](#등급과-그-등급이-여는-범위)
- [판 대조와 수치의 판 귀속](#판-대조와-수치의-판-귀속)
- [이 논문이 실제로 주장하는 범위](#이-논문이-실제로-주장하는-범위)
- [걷어낸 것은 순차 계산이라는 제약이다](#걷어낸-것은-순차-계산이라는-제약이다)
- [어텐션의 정의](#어텐션의-정의)
- [scaled dot-product attention과 나눗셈의 이유](#scaled-dot-product-attention과-나눗셈의-이유)
- [멀티 헤드 어텐션의 동기](#멀티-헤드-어텐션의-동기)
- [어텐션이 쓰이는 세 자리](#어텐션이-쓰이는-세-자리)
- [블록의 나머지 구성](#블록의-나머지-구성)
- [위치 인코딩을 사인과 코사인으로 고른 이유](#위치-인코딩을-사인과-코사인으로-고른-이유)
- [세 척도와 표 1의 비교](#세-척도와-표-1의-비교)
- [훈련 설정](#훈련-설정)
- [표 2 번역 품질과 훈련 비용](#표-2-번역-품질과-훈련-비용)
- [표 3 변형 실험](#표-3-변형-실험)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **순환(recurrence)과 합성곱(convolution)을 완전히 걷어내고 어텐션(attention)만
남겼을 때 무엇이 좋아지고, 원저자들은 그것을 무엇으로 뒷받침했는가.**

## 등급과 그 등급이 여는 범위

- 근거 등급은 **`peer-reviewed`**다. NIPS 2017(제31회 Neural Information Processing Systems,
  Long Beach, CA)에 게재된 심사 논문이고, 이 지위는 논문 1쪽 아래에 인쇄된 한 줄이 근거다.
  권·쪽수는 문면이 아니라 논문집 레코드가 근거이므로 이 페이지의 로케이터는 절 번호와
  **논문집 판 PDF에 인쇄된 쪽 번호(1~11)**를 쓴다.[^vaswani2017-attention]
- **그 등급이 여는 것은 저자들 자신이 잰 값뿐이다.** 이 논문의 실험은 전부 저자들의 자체
  실험이다. 표 2에 함께 실린 다른 모델들의 BLEU와 훈련 비용은 저자들이 문헌에서 옮겨 온
  제3자 수치이므로, 이 KB는 그 값을 이 페이지 경유로 인용하지 않는다. 이 페이지에서 그
  값들은 저자들이 자기 결과를 놓은 비교 맥락으로만 쓰인다.
- **재현 조건은 좁다.** 측정은 2017년 시점, 8장짜리 NVIDIA P100 GPU 기계 한 대, WMT 2014
  영독·영불 번역 과제 위에서 이뤄졌다(5.2절, p.7). 이 조건 밖으로의 전이는 이 논문이
  주장하지 않는다.
- **후속 재현·반박 문헌은 이 KB에 없다.** 이 페이지의 수치는 원전 하나에만 걸려 있다.

## 판 대조와 수치의 판 귀속

스냅샷에는 두 판이 있다. **정본은 NIPS 2017 논문집 판(11쪽)**이고, arXiv:1706.03762v7
(2023-08-02, 15쪽)은 게재 뒤에 붙은 개정본이라 같은 심사를 받지 않았다.

- **영불(EN-FR) 번역의 Transformer (big) BLEU가 판마다 다르다.** 논문집 판은 초록·6.1절
  본문·표 2 세 자리에서 모두 **41.0**이다. arXiv v7은 초록과 표 2를 **41.8**로 고쳤으나
  6.1절 본문은 41.0으로 남겨 두어 **한 판 안에서 어긋난다**.[^vaswani2017-attention]
  - 이 페이지가 적는 값은 **정본인 논문집 판의 41.0**이다. arXiv v7을 인용하는 문헌이
    41.8을 쓰는 것은 그 판의 초록·표 2를 따른 것이다.
- **영독(EN-DE) 28.4는 두 판이 같다** — 초록·6.1절·표 2 전부.[^vaswani2017-attention]
- **6.3절(영어 구구조 구문 분석)과 부록(어텐션 시각화)은 arXiv v7에만 있다.** 논문집 판은
  4절에서 "present and discuss examples in the appendix"라고 쓰면서도 가리킬 부록을 담지
  않는다.[^vaswani2017-attention]
- 표 1·표 3·3절 전체·식 (1)(2)(3)은 두 판이 같다.

## 이 논문이 실제로 주장하는 범위

제목은 "Attention Is All You Need"지만, 논문집 판이 실증으로 뒷받침하는 범위는 **기계 번역
두 과제**다. 초록의 문장이 그 범위를 그대로 말한다 (초록, p.1):[^vaswani2017-attention]

> We propose a new simple network architecture, the Transformer, based solely on attention
> mechanisms, dispensing with recurrence and convolutions entirely. Experiments on two machine
> translation tasks show these models to be superior in quality while being more parallelizable
> and requiring significantly less time to train.

- 우선권 주장도 범위가 정해져 있다 — **시퀀스 변환(sequence transduction) 모델 중에서
  처음**이라는 형태다 (2절, p.3):[^vaswani2017-attention]

  > To the best of our knowledge, however, the Transformer is the first transduction model
  > relying entirely on self-attention to compute representations of its input and output
  > without using sequence-aligned RNNs or convolution.

- 결론도 같은 범위를 되풀이한다 — **번역 과제에 대해** 더 빨리 훈련되고 두 WMT 2014 과제에서
  최고 성적을 냈다는 것이며, 다른 양식(이미지·오디오·비디오)으로의 확장은 **계획**으로
  적혀 있다 (7절, p.9).[^vaswani2017-attention]
- 자기 어텐션(self-attention)이 모델을 더 해석 가능하게 만들 수 있다는 것은 저자들이
  "side benefit"으로 붙인 관찰이고, 논문집 판에는 그 근거로 가리킬 부록이 없다
  (4절, p.7).[^vaswani2017-attention] #hypothesis

## 걷어낸 것은 순차 계산이라는 제약이다

- 순환 모델의 한계를 저자들은 병렬화 불가로 규정한다 (1절, p.2):[^vaswani2017-attention]

  > This inherently sequential nature precludes parallelization within training examples, which
  > becomes critical at longer sequence lengths, as memory constraints limit batching across
  > examples.

  같은 문단은 인수분해 기법과 조건부 계산이 효율을 개선했음을 인정하면서도
  **"The fundamental constraint of sequential computation, however, remains."**로 끝난다.
- 그전까지 어텐션은 순환망과 **함께** 쓰였다 — **"In all but a few cases, however, such
  attention mechanisms are used in conjunction with a recurrent network."**
  (1절, p.2).[^vaswani2017-attention]
- 그래서 제안이 이것이다 (1절, p.2):[^vaswani2017-attention]

  > In this work we propose the Transformer, a model architecture eschewing recurrence and
  > instead relying entirely on an attention mechanism to draw global dependencies between input
  > and output. The Transformer allows for significantly more parallelization and can reach a new
  > state of the art in translation quality after being trained for as little as twelve hours on
  > eight P100 GPUs.

- 자기 어텐션의 정의도 이 논문 안에 있다 — **"Self-attention, sometimes called intra-attention
  is an attention mechanism relating different positions of a single sequence in order to compute
  a representation of the sequence."** (2절, p.3).[^vaswani2017-attention]
- 합성곱 계열(ByteNet·ConvS2S)과의 차이는 **두 위치를 잇는 데 드는 연산 수**다. 그 수가
  ConvS2S는 거리에 선형으로, ByteNet은 로그로 자라는데 트랜스포머는 **상수**로 줄어든다.
  대신 어텐션 가중 평균 때문에 유효 해상도가 낮아지고, 그것을 멀티 헤드 어텐션으로
  상쇄한다 (2절, p.3).[^vaswani2017-attention]

## 어텐션의 정의

논문이 어텐션 함수를 규정하는 문장이다 (3.2절, p.3):[^vaswani2017-attention]

> An attention function can be described as mapping a query and a set of key-value pairs to an
> output, where the query, keys, values, and output are all vectors. The output is computed as a
> weighted sum of the values, where the weight assigned to each value is computed by a
> compatibility function of the query with the corresponding key.

- 질의(query)·키(key)·값(value)·출력이 **모두 벡터**라는 것과, 가중치가 **질의와 그에 대응하는
  키의 호환 함수(compatibility function)**로 계산된다는 것이 정의의 두 축이다.

## scaled dot-product attention과 나눗셈의 이유

- 저자들이 자기 어텐션 함수에 붙인 고유 이름이 **scaled dot-product attention**이다. 이 KB는
  이 이름을 번역하지 않고 원어로 둔다 — 논문이 따옴표로 묶어 명명한 고유 이름이고, 이 KB가
  이미 `local windowed attention`·`multi-query attention`·`grouped-query attention`을 원어로
  두는 것과 같은 처리다.
- 정의 (3.2.1절, p.3–4):[^vaswani2017-attention]

  > We call our particular attention "Scaled Dot-Product Attention" (Figure 2). The input consists
  > of queries and keys of dimension `d_k`, and values of dimension `d_v`. We compute the dot
  > products of the query with all keys, divide each by √`d_k`, and apply a softmax function to
  > obtain the weights on the values.

  여기서 `d_k`는 질의와 키의 차원, `d_v`는 값의 차원, √`d_k`는 **키 차원의 제곱근**이다.
- 행렬 꼴이 식 (1)이다 (3.2.1절, p.4):[^vaswani2017-attention]

  ```math
  \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^{T}}{\sqrt{d_k}}\right)V
  ```

- **왜 나누는가.** 논문이 대는 이유는 소프트맥스(softmax)의 기울기다 (3.2.1절,
  p.4):[^vaswani2017-attention]

  > While for small values of `d_k` the two mechanisms perform similarly, additive attention
  > outperforms dot product attention without scaling for larger values of `d_k`. We suspect that
  > for large values of `d_k`, the dot products grow large in magnitude, pushing the softmax
  > function into regions where it has extremely small gradients. To counteract this effect, we
  > scale the dot products by 1/√`d_k`.

  - **"We suspect"** — 저자들 자신이 이 설명을 추측으로 규정한다. 이 페이지도 그 지위를
    그대로 옮긴다.
  - 각주가 그 추측의 산수를 댄다 — 질의 `q`와 키 `k`의 성분이 평균 0, 분산 1인 독립 확률
    변수라고 가정하면 그 내적은 평균 0, **분산 `d_k`**를 갖는다 (3.2.1절, p.4 각주
    4).[^vaswani2017-attention]
- 내적(dot-product) 어텐션을 `additive attention` 대신 고른 이유는 **속도와 공간**이다 —
  이론적 복잡도는 비슷하지만 **"dot-product attention is much faster and more space-efficient
  in practice, since it can be implemented using highly optimized matrix multiplication code"**
  (3.2.1절, p.4).[^vaswani2017-attention]
  - `additive attention`은 옮기지 않고 원어로 둔다. **이 KB가 `additive`를 "합산 가능"으로
    고정한 것은 차원 모델링의 팩트 속성 이야기이고**(SCHEMA 역어 표), 여기의 `additive`는 은닉
    층 하나짜리 순방향 망으로 호환 함수를 계산하는 **다른 기제**다. 영어가 같을 뿐 가리키는
    것이 달라서, 합쳐 옮기면 그 구분이 사라진다 — `compaction`을 LSM과 카프카에서 갈라 옮긴
    것과 같은 처리다.

## 멀티 헤드 어텐션의 동기

- 무엇을 하는가 (3.2.2절, p.4):[^vaswani2017-attention]

  > Instead of performing a single attention function with `d_model`-dimensional keys, values and
  > queries, we found it beneficial to linearly project the queries, keys and values `h` times
  > with different, learned linear projections to `d_k`, `d_k` and `d_v` dimensions, respectively.

  여기서 `d_model`은 **모델 차원**, `h`는 **헤드(head)의 수**다.
- **왜 하는가** (3.2.2절, p.4):[^vaswani2017-attention]

  > Multi-head attention allows the model to jointly attend to information from different
  > representation subspaces at different positions. With a single attention head, averaging
  > inhibits this.

  동기는 **서로 다른 표현 부분공간(representation subspace)에 동시에 주의를 주는 것**이고,
  헤드가 하나면 평균이 그것을 막는다는 것이다.
- 식 (3.2.2절, p.5):[^vaswani2017-attention]

  ```math
  \mathrm{MultiHead}(Q, K, V) = \mathrm{Concat}(\mathrm{head}_1, ..., \mathrm{head}_h)W^{O}
  ```

  ```math
  \mathrm{head}_i = \mathrm{Attention}(QW_i^{Q}, KW_i^{K}, VW_i^{V})
  ```

  사영 행렬은 `W_i^Q` ∈ ℝ^(`d_model`×`d_k`)(실수 행렬), `W_i^K` ∈ ℝ^(`d_model`×`d_k`),
  `W_i^V` ∈ ℝ^(`d_model`×`d_v`), `W^O` ∈ ℝ^(`h`·`d_v`×`d_model`)다.
- **이 논문이 실제로 쓴 값**: `h` = 8, `d_k` = `d_v` = `d_model`/`h` = 64. 헤드마다 차원이
  줄기 때문에 **총 계산 비용은 전 차원 단일 헤드 어텐션과 비슷하다**고 저자들은 적는다
  (3.2.2절, p.5).[^vaswani2017-attention]

## 어텐션이 쓰이는 세 자리

트랜스포머는 멀티 헤드 어텐션을 세 방식으로 쓴다 (3.2.3절, p.5):[^vaswani2017-attention]

- **인코더-디코더 어텐션** — 질의는 직전 디코더 층에서 오고, 기억 키와 값은 인코더 스택의
  출력에서 온다. 디코더의 모든 위치가 입력 시퀀스의 모든 위치를 볼 수 있다.
- **인코더의 자기 어텐션** — 키·값·질의가 모두 같은 곳, 즉 인코더 직전 층의 출력에서 온다.
- **디코더의 자기 어텐션** — 각 위치가 자기 자신까지의 모든 위치를 본다. 자기회귀
  (auto-regressive) 성질을 지키려면 왼쪽으로 흐르는 정보를 막아야 하므로, **소프트맥스 입력에서
  금지된 연결에 해당하는 값을 전부 −∞(음의 무한대)로 설정해 가려낸다**.

## 블록의 나머지 구성

- 인코더와 디코더 모두 **`N` = 6개의 같은 층**을 쌓는다. 인코더 층은 멀티 헤드 자기 어텐션과
  위치별 완전 연결 순방향 망(feed-forward network) 두 부분층으로 이뤄지고, 디코더는 인코더
  출력에 대한 멀티 헤드 어텐션을 세 번째 부분층으로 더 갖는다 (3.1절,
  p.3).[^vaswani2017-attention]
- 부분층마다 **잔차 연결(residual connection)** 뒤에 **층 정규화(layer normalization)**가 오고,
  그 출력은 `LayerNorm(x + Sublayer(x))`다. 잔차 연결을 가능하게 하려고 임베딩 층을 포함한
  모든 부분층의 출력 차원이 **`d_model` = 512**로 고정된다 (3.1절, p.3).[^vaswani2017-attention]
- 디코더의 자기 어텐션 부분층은 뒤 위치를 못 보게 가려지며, 출력 임베딩이 한 자리 밀려 있는
  것과 합쳐져 **위치 `i`의 예측이 `i`보다 앞선 위치의 알려진 출력에만 의존하도록 보장한다**
  (3.1절, p.3).[^vaswani2017-attention]
- 위치별 순방향 망은 ReLU 활성을 사이에 둔 선형 변환 둘이다 (3.3절,
  p.5):[^vaswani2017-attention]

  ```math
  \mathrm{FFN}(x) = \max(0, xW_1 + b_1)W_2 + b_2
  ```

  입출력 차원은 `d_model` = 512이고 **내부 층 차원은 `d_ff` = 2048**이다. 저자들은 이것을
  **커널 크기 1인 합성곱 둘**로도 설명할 수 있다고 적는다 (3.3절, p.5).[^vaswani2017-attention]
- 두 임베딩 층과 소프트맥스 앞 선형 변환은 **같은 가중치 행렬을 공유**하고, 임베딩 층에서는
  그 가중치에 √`d_model`(모델 차원의 제곱근)을 곱한다 (3.4절, p.5).[^vaswani2017-attention]

## 위치 인코딩을 사인과 코사인으로 고른 이유

- 왜 필요한가 (3.5절, p.5):[^vaswani2017-attention]

  > Since our model contains no recurrence and no convolution, in order for the model to make use
  > of the order of the sequence, we must inject some information about the relative or absolute
  > position of the tokens in the sequence.

  **순환도 합성곱도 없앤 대가**가 이 자리다. 위치 인코딩(positional encoding)은 임베딩과 같은
  차원 `d_model`을 가져 서로 더할 수 있다.
- 쓴 함수 (3.5절, p.6):[^vaswani2017-attention]

  ```math
  PE_{(pos, 2i)} = \sin\!\left(pos / 10000^{2i/d_{model}}\right)
  ```

  ```math
  PE_{(pos, 2i+1)} = \cos\!\left(pos / 10000^{2i/d_{model}}\right)
  ```

  `pos`는 위치, `i`는 차원이다. 파장은 2π(2 파이)에서 10000·2π까지 **등비수열**을 이룬다.
- **왜 이 함수인가** (3.5절, p.6):[^vaswani2017-attention]

  > We chose this function because we hypothesized it would allow the model to easily learn to
  > attend by relative positions, since for any fixed offset `k`, `PE_pos+k` can be represented as
  > a linear function of `PE_pos`.

  **"we hypothesized"** — 이유 역시 저자들이 가설로 규정한다.
- **학습된 위치 임베딩과 견줘 봤고 결과는 거의 같았다.** 그런데도 사인 쪽을 고른 이유는 성능이
  아니라 **외삽 가능성**이다 (3.5절, p.6):[^vaswani2017-attention]

  > We also experimented with using learned positional embeddings instead, and found that the two
  > versions produced nearly identical results (see Table 3 row (E)). We chose the sinusoidal
  > version because it may allow the model to extrapolate to sequence lengths longer than the ones
  > encountered during training.

  - 표 3 (E) 행의 실제 값: 학습된 위치 임베딩이 PPL(dev) 4.92, BLEU(dev) 25.7이고 base 모델은
    4.92 / 25.8이다 (표 3, p.9. 영독 개발 집합 newstest2013).[^vaswani2017-attention]

## 세 척도와 표 1의 비교

저자들이 자기 어텐션을 정당화할 때 쓴 척도는 세 가지다 (4절, p.6):[^vaswani2017-attention]

1. **층당 총 계산 복잡도**(total computational complexity per layer).
2. **병렬화 가능한 계산량** — 필요한 순차 연산의 최소 수로 잰다.
3. **장거리 의존의 경로 길이**(path length between long-range dependencies) — 신호가 앞뒤로
   지나야 하는 경로가 짧을수록 장거리 의존을 배우기 쉽다.

표 1이 그 비교다. `n`은 시퀀스 길이, `d`는 표현 차원, `k`는 합성곱 커널 크기, `r`는 제한된 자기
어텐션에서 이웃의 크기다 (표 1, p.6):[^vaswani2017-attention]

| Layer Type | Complexity per Layer | Sequential Operations | Maximum Path Length |
|---|---|---|---|
| Self-Attention | O(n² · d) | O(1) | O(1) |
| Recurrent | O(n · d²) | O(n) | O(n) |
| Convolutional | O(k · n · d²) | O(1) | O(log_k(n)) |
| Self-Attention (restricted) | O(r · n · d) | O(1) | O(n/r) |

- **표 1은 측정이 아니라 점근 복잡도 표다.** 실행 시간이 아니라 차수를 적은 것이므로 이
  페이지도 그렇게 읽는다.
- 저자들이 표에서 끌어내는 조건부 결론 — **자기 어텐션 층이 순환 층보다 빠른 것은 시퀀스 길이
  `n`이 표현 차원 `d`보다 작을 때**이고, 그것이 word-piece·byte-pair 표현을 쓰는 당시
  최고 수준 기계 번역 모델의 문장 표현에서 대개 참이라는 것이다 (4절,
  pp.6–7).[^vaswani2017-attention]
  - 조건이 뒤집히는 자리(`n`이 `d`보다 큰 긴 시퀀스)에 대해 저자들이 내놓은 것은 **제한된 자기
    어텐션**이고, 그것은 실험이 아니라 **향후 과제**로 적혀 있다 — "We plan to investigate this
    approach further in future work" (4절, p.7).[^vaswani2017-attention]

## 훈련 설정

수치를 읽을 때 함께 봐야 하는 조건이다 (5절, p.7).[^vaswani2017-attention]

- **데이터** — 영독은 WMT 2014 영독 데이터셋 약 450만 문장 쌍, byte-pair encoding으로 원문과
  번역문이 공유하는 약 37,000 토큰 어휘. 영불은 WMT 2014 영불 데이터셋 3,600만 문장,
  32,000 word-piece 어휘. 배치는 근사 시퀀스 길이로 묶어 **원문 약 25,000 토큰 + 번역문 약
  25,000 토큰**을 담았다 (5.1절, p.7).
- **하드웨어와 일정** — **NVIDIA P100 GPU 8장을 단 기계 한 대**. base 모델은 스텝당 약 0.4초로
  **100,000 스텝(12시간)**, big 모델은 스텝당 1.0초로 **300,000 스텝(3.5일)** 훈련했다
  (5.2절, p.7).
- **최적화기** — Adam, β₁(베타 1) = 0.9, β₂(베타 2) = 0.98, ε(엡실론) = 10⁻⁹. 학습률은 고정이
  아니라 식 (3)으로 바꿨다 (5.3절, p.7):[^vaswani2017-attention]

  ```math
  lrate = d_{model}^{-0.5} \cdot \min\!\left(step\_num^{-0.5},\ step\_num \cdot warmup\_steps^{-1.5}\right)
  ```

  **처음 `warmup_steps` 동안 학습률을 선형으로 올리고 그 뒤로는 스텝 수의 제곱근에 반비례해
  내린다.** 이 논문이 쓴 값은 `warmup_steps` = 4000이다 (5.3절, p.7).
- **정규화 셋** (5.4절, pp.7–8):
  - 잔차 드롭아웃(residual dropout) — 각 부분층 출력에, 그리고 임베딩과 위치 인코딩의 합에
    적용한다. base 모델의 비율은 `P_drop` = 0.1.
  - 레이블 스무딩(label smoothing) — 값 `ε_ls` = 0.1. 저자들이 붙인 단서가 중요하다:
    **"This hurts perplexity, as the model learns to be more unsure, but improves accuracy and
    BLEU score."** 즉 한 지표를 깎고 다른 지표를 올리는 맞바꿈이다.
  - 세 번째 정규화를 "three types"라고 예고하지만 소제목으로 떼어 적힌 것은 둘이다
    (5.4절, pp.7–8). #hypothesis
- **추론 설정** — base 모델은 10분 간격으로 쓴 **마지막 체크포인트 5개를 평균**한 단일 모델,
  big 모델은 **마지막 20개를 평균**했다. 빔 서치(beam search) 빔 크기 4, 길이 벌점
  α(알파) = 0.6, 최대 출력 길이는 입력 길이 + 50 (6.1절, p.8).

## 표 2 번역 품질과 훈련 비용

**아래는 정본인 NIPS 2017 논문집 판 표 2다. 측정 대상은 newstest2014 시험 집합**이고
BLEU는 원값, 훈련 비용은 FLOPs다 (표 2, p.8).[^vaswani2017-attention]

| Model | BLEU EN-DE | BLEU EN-FR | Training Cost EN-DE (FLOPs) | Training Cost EN-FR (FLOPs) |
|---|---|---|---|---|
| ByteNet | 23.75 | | | |
| Deep-Att + PosUnk | | 39.2 | | 1.0 · 10²⁰ |
| GNMT + RL | 24.6 | 39.92 | 2.3 · 10¹⁹ | 1.4 · 10²⁰ |
| ConvS2S | 25.16 | 40.46 | 9.6 · 10¹⁸ | 1.5 · 10²⁰ |
| MoE | 26.03 | 40.56 | 2.0 · 10¹⁹ | 1.2 · 10²⁰ |
| Deep-Att + PosUnk Ensemble | | 40.4 | | 8.0 · 10²⁰ |
| GNMT + RL Ensemble | 26.30 | 41.16 | 1.8 · 10²⁰ | 1.1 · 10²¹ |
| ConvS2S Ensemble | 26.36 | 41.29 | 7.7 · 10¹⁹ | 1.2 · 10²¹ |
| **Transformer (base model)** | **27.3** | **38.1** | **3.3 · 10¹⁸** (영독·영불 공통 칸) | |
| **Transformer (big)** | **28.4** | **41.0** | **2.3 · 10¹⁹** (영독·영불 공통 칸) | |

- **Transformer 두 행만이 이 논문의 자체 측정이다.** 나머지 행은 저자들이 문헌에서 옮긴
  제3자 수치이므로 이 KB는 그 값을 이 페이지 경유로 쓰지 않는다.
- Transformer 두 행의 훈련 비용은 영독·영불 칸이 **하나로 병합돼 있다** — 원문 표의 조판
  그대로다.
- **훈련 비용은 측정이 아니라 추정이다.** 저자들의 방법은 **훈련 시간 × GPU 수 × GPU 한 장의
  지속 단정밀도 부동소수점 처리 능력 추정치**를 곱하는 것이고, 쓴 값은 K80 2.8, K40 3.7,
  M40 6.0, P100 9.5 TFLOPS다 (6.1절 p.8과 그 각주 5).[^vaswani2017-attention] 이 값은 실측
  FLOP 계수가 아니므로 다른 논문의 FLOPs와 나란히 놓을 때 주의가 필요하다.
- 저자들이 6.1절 본문에서 이 표를 읽는 방식 (6.1절, p.8):[^vaswani2017-attention]
  - 영독 — big 모델이 앙상블을 포함한 기존 최고 보고 모델들을 **2.0 BLEU 넘게** 앞서
    28.4로 최고 성적을 세웠다. 훈련은 **P100 8장으로 3.5일** 걸렸다. base 모델조차 기존
    발표 모델과 앙상블 전부를 넘어섰다.
  - 영불 — big 모델이 **41.0**을 냈고, 기존 최고 단일 모델의 훈련 비용의 **1/4 미만**이다.
    - 영불 big 모델은 드롭아웃 비율을 0.3이 아니라 **`P_drop` = 0.1**로 썼다. 표 3 맨
      아랫줄의 big 설정과 이 한 값이 다르다.

## 표 3 변형 실험

**표 3은 표 2와 다른 것을 잰다.** 대상은 **영독 개발 집합 newstest2013**이고, 체크포인트 평균은
쓰지 않았다. 적힌 펄플렉시티(perplexity)는 **word-piece당**이라 word당 펄플렉시티와 비교하면
안 된다고 표 설명이 못 박는다. 빈칸은 base 모델과 같은 값이라는 뜻이다 (표 3,
p.9).[^vaswani2017-attention]

| 행 | N | d_model | d_ff | h | d_k | d_v | P_drop | ε_ls | train steps | PPL (dev) | BLEU (dev) | params ×10⁶ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| base | 6 | 512 | 2048 | 8 | 64 | 64 | 0.1 | 0.1 | 100K | 4.92 | 25.8 | 65 |
| (A) | | | | 1 | 512 | 512 | | | | 5.29 | 24.9 | |
| (A) | | | | 4 | 128 | 128 | | | | 5.00 | 25.5 | |
| (A) | | | | 16 | 32 | 32 | | | | 4.91 | 25.8 | |
| (A) | | | | 32 | 16 | 16 | | | | 5.01 | 25.4 | |
| (B) | | | | | 16 | | | | | 5.16 | 25.1 | 58 |
| (B) | | | | | 32 | | | | | 5.01 | 25.4 | 60 |
| (C) | 2 | | | | | | | | | 6.11 | 23.7 | 36 |
| (C) | 4 | | | | | | | | | 5.19 | 25.3 | 50 |
| (C) | 8 | | | | | | | | | 4.88 | 25.5 | 80 |
| (C) | | 256 | | | 32 | 32 | | | | 5.75 | 24.5 | 28 |
| (C) | | 1024 | | | 128 | 128 | | | | 4.66 | 26.0 | 168 |
| (C) | | | 1024 | | | | | | | 5.12 | 25.4 | 53 |
| (C) | | | 4096 | | | | | | | 4.75 | 26.2 | 90 |
| (D) | | | | | | | 0.0 | | | 5.77 | 24.6 | |
| (D) | | | | | | | 0.2 | | | 4.95 | 25.5 | |
| (D) | | | | | | | | 0.0 | | 4.67 | 25.3 | |
| (D) | | | | | | | | 0.2 | | 5.47 | 25.7 | |
| (E) | 사인 대신 학습된 위치 임베딩 | | | | | | | | | 4.92 | 25.7 | |
| big | 6 | 1024 | 4096 | 16 | | | 0.3 | | 300K | 4.33 | 26.4 | 213 |

저자들이 이 표에서 읽어 내는 것 (6.2절, pp.8–9):[^vaswani2017-attention]

- **(A) 헤드 수** — 계산량을 일정하게 두고 헤드 수와 키·값 차원을 바꿨다. **단일 헤드는 최고
  설정보다 0.9 BLEU 나쁘고**(24.9 대 25.8, 영독 newstest2013 BLEU 원값), **헤드가 너무 많아도
  품질이 떨어진다**(h=32에서 25.4).
- **(B) 키 차원** — **`d_k`를 줄이면 품질이 나빠진다**(16에서 25.1, 32에서 25.4, base 64에서
  25.8). 저자들의 해석: **"determining compatibility is not easy and that a more sophisticated
  compatibility function than dot product may be beneficial"** — 즉 내적보다 정교한 호환 함수가
  이로울 수 있다는 것이다. **논문 자신이 자기 선택의 한계를 적어 둔 자리다.**
- **(C)와 (D)** — 예상대로 **큰 모델이 낫고, 드롭아웃이 과적합을 막는 데 매우 유용하다**.
- **(E)** — 사인 위치 인코딩을 학습된 위치 임베딩으로 바꿔도 base 모델과 **거의 같은 결과**
  (4.92 / 25.7 대 4.92 / 25.8)를 얻었다.
- **표 3의 BLEU는 개발 집합(newstest2013) 값이라 표 2의 시험 집합(newstest2014) 값과 같은
  자리에 놓을 수 없다.** 표 3 big 행의 26.4와 표 2 big 행의 28.4가 다른 것은 개선이 아니라
  다른 집합·다른 절차(체크포인트 평균 유무)의 값이기 때문이다.

## 이어지는 페이지

- [트랜스포머 구조](../concepts/transformer-architecture.md) — 이 원전이 정의한 구조를 오늘의
  실무 관점(프리필과 디코드, 은닉 차원, Llama 계열 수치)에서 다시 서술한 자리
- [KV 캐시와 어텐션 최적화](../concepts/kv-cache-and-attention-optimization.md) — 이 페이지의
  어텐션 정의가 추론 비용으로 넘어가는 자리
- [대안 모델 구조](../concepts/alternative-model-architectures.md) — 이 구조를 대체하려는
  RWKV·SSM·Mamba·Jamba
- [컨텍스트 길이와 컨텍스트 효율](../concepts/context-length-and-efficiency.md) — 표 1의
  O(n² · d)가 긴 입력에서 문제로 돌아오는 자리
- [모델 규모의 세 수치](../concepts/model-size-and-scale.md) — 표 3의 params 열이 재는 것과
  FLOP으로 컴퓨트를 세는 틀
- [언어 모델링 지표](../concepts/language-modeling-metrics.md) — 표 3의 PPL 열이 무엇인가
- [벤치마크의 수명과 은퇴](../concepts/benchmark-lifespan-and-retirement.md) — WMT 2014
  newstest 같은 고정 시험 집합의 수치가 시간과 함께 겪는 일

[^vaswani2017-attention]: Vaswani et al. 2017, "Attention Is All You Need". **정본은 NIPS 2017
    논문집 판**(11쪽)이고, 이 페이지의 쪽 번호는 그 PDF에 인쇄된 1~11이다. 권·쪽수(Advances in
    Neural Information Processing Systems 30, pp.5998–6008)는 논문 문면이 아니라 논문집
    레코드가 근거라 로케이터로 쓰지 않았다. 게재 정보로 문면에 인쇄된 것은 1쪽 아래
    "31st Conference on Neural Information Processing Systems (NIPS 2017), Long Beach, CA, USA."
    한 줄뿐이다. 스냅샷에는 arXiv:1706.03762v7(2023-08-02, 15쪽)도 함께 있으며 두 판의 대조는
    소스 메타에 표로 있다. 판 사이의 유일한 수치 차이는 Transformer (big)의 영불 BLEU다
    (논문집 판 41.0, arXiv v7은 초록과 표 2만 41.8이고 6.1절 본문은 41.0). 6.3절(영어 구구조
    구문 분석)과 부록(어텐션 시각화 Figure 3~5)은 arXiv v7에만 있어 이 페이지에 담지 않았다.
    Figure 1(모델 구조도, p.3)·Figure 2(어텐션 도식, p.4)는 도판이라 옮기지 않았다. 표 1·표 2·
    표 3은 원문 표기를 그대로 옮겼고, 표 2의 Transformer 아닌 행은 저자들이 문헌에서 인용한
    제3자 수치다. 수치·수식은 `pdftotext -layout` 추출본과 130dpi 렌더 이미지 양쪽으로
    대조했다 — `pdftext.py` 추출본은 √ 글리프를 `p`로 잘못 읽어 √`d_k`가 `pd_k`로 나오므로
    수식 대조에 쓰지 않았다.

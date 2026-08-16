---
type: concept
title: 훈련 데이터 중복 제거
description: 중복이 분포를 비틀고 테스트 세트를 오염시키는 방식 — 0.1%를 100번 반복해 8억 파라미터 모델이 4억 파라미터 수준으로 떨어진 실측, 중복의 세 형태와 무엇을 중복으로 볼지의 정의 문제, 그리고 쌍대 비교·해싱·차원 축소라는 세 수단
generated: { by: "claude-opus-5", at: "2026-08-17T07:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 훈련 데이터 중복 제거

- [중복이 하는 일](#중복이-하는-일)
- [성능이 실제로 떨어진 실측](#성능이-실제로-떨어진-실측)
- [중복의 세 형태](#중복의-세-형태)
- [무엇을 중복으로 볼 것인가](#무엇을-중복으로-볼-것인가)
- [세 가지 수단](#세-가지-수단)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **훈련 데이터의 중복은 왜 문제이고 어떻게 지우는가.**

## 중복이 하는 일

- 절이 여는 규정 (8장, p.399):[^huyen2025]

  > Duplicated data can skew the data distribution and introduce biases into your model.

  저자가 든 장난감 데이터셋이다. 회색 칸이 중복 항목이며 원문에서는 2·3·4행이
  회색이다 (8장, p.399, Table 8-3):[^huyen2025]

  | | Input (Product description) | Output (Price) |
  |---|---|---|
  | 1 | `{item: pencil, color: red}` | $20 |
  | 2 | `{item: compass, color: green}` | $2 |
  | 3 | `{item: pencil, color: red}` | $20 |
  | 4 | `{item: pencil, color: red}` | $20 |
  | 5 | `{item: pencil, color: green}` | $1 |

  **중복된 항목은 모델을 붉은색 품목이 전부 비싸다는 잘못된 결론으로 이끌 수 있다** (8장,
  p.399).[^huyen2025]
- 평가까지 무너진다 — **중복은 테스트 세트 오염을 일으킬 수 있다. 중복된 데이터를 훈련 세트와 테스트
  세트로 나눌 때 한 예제가 훈련 세트에 있고 그 중복이 테스트 세트에 있을 수 있다** (8장,
  p.399).[^huyen2025] 그 오염의 지형은 [데이터 오염](../concepts/data-contamination.md)에 있다.

## 성능이 실제로 떨어진 실측

- **여러 연구가 훈련 데이터 중복이 모델 성능에 미치는 부정적 영향을 보였다; Lee et al.(2021)과
  Tirumala et al.(2023)을 보라. 어떤 Anthropic 연구는 데이터의 0.1%를 100번 반복하면 나머지 90%의
  훈련 토큰이 유일하게 남아 있음에도 8억 파라미터 모델의 성능이 4억 파라미터 모델 수준으로 떨어질 수
  있음을 시연했다(Hernandez et al., 2022)** (8장, p.399).[^huyen2025]
- 성능이 안 떨어져도 손해다 — **중복이 모델 성능을 해치지 않을 때조차 당신의 시간과 컴퓨트를 낭비할
  수 있다** (8장, p.399).[^huyen2025]

## 중복의 세 형태

- **데이터에 따라 중복에는 여러 형태가 있고 그중 일부는 탐지하기 더 어렵다. 예컨대 문서 데이터셋에서
  몇 가지 중복 유형은 다음과 같다** (8장, p.400):[^huyen2025]
  - **Whole document duplications: the same document appearing more than once.**
  - **Intra-document duplications: e.g., the same paragraph appears twice in one document.**
  - **Cross-document duplications: e.g., the same popular quote appears in multiple documents.**

## 무엇을 중복으로 볼 것인가

- **무엇이 중복으로 간주되는지는 당신의 정의에도 달려 있다. 예컨대 문서 수준·문단 수준·문장 수준·토큰
  수준 중 어디에서 중복을 다루고 싶은가? 두 텍스트가 중복으로 간주되려면 정확히 일치해야 하는가, 아니면
  80% 겹침이면 충분한가? 같은 항목을 다른 순서로 가진 두 목록은 중복으로 간주되는가?** (8장,
  p.400).[^huyen2025]

## 세 가지 수단

- **중복 제거 과제는 3장에서 논한 유사도 측정에 쓰이는 것과 같은 기법을 활용할 수 있다. 데이터 중복
  제거는 두 신원(예: 두 소셜 미디어 프로필)이 같은지 판정하는 신원 해소(identity resolution)에도
  쓰인다** (8장, p.400).[^huyen2025] 그 유사도 측정은
  [참조 데이터에 대한 유사도 측정](../concepts/similarity-measurements-against-reference-data.md)에
  있다.
- **Pairwise comparison** — **3장에서 논한 정확 일치·n-그램 일치·퍼지 일치·의미 유사도 점수를 써서
  데이터셋의 각 예제와 다른 모든 예제의 유사도 점수를 계산한다. 그러나 이 접근은 큰 데이터셋에서 비쌀
  수 있다** (8장, p.400).[^huyen2025]
- **Hashing** — **예제를 서로 다른 버킷으로 해싱하고 같은 버킷에 떨어지는 예제 사이에서만 확인한다.
  해시 관련 중복 제거 방법으로 MinHash와 Bloom filter가 있다** (8장, p.400).[^huyen2025]
- **Dimensionality reduction** — **차원 축소 기법을 써서 데이터의 차원을 먼저 줄인 뒤 쌍대 비교를
  한다. 6장에서 논한 벡터 검색에 쓰이는 많은 기법을 이것에 쓸 수 있다** (8장,
  p.400).[^huyen2025] 그 색인 구조는
  [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md)에 있다.
- 도구 — **빠르게 검색하면 중복 제거를 돕는 라이브러리가 많이 나온다. 그중 일부는 dupeGuru·Dedupe·
  datasketch·TextDistance·TheFuzz·deduplicate-text-datasets다** (8장, p.400).[^huyen2025]
  - 각주 — **내 오픈소스 라이브러리 중 하나인 lazyNLP도 Bloom filter를 이용한 겹침 추정과 중복 제거를
    지원한다** (8장, p.400 각주 16).[^huyen2025]

## 이어지는 페이지

- [훈련 데이터 처리](../concepts/training-data-processing.md) — 이 단계 앞의 점검
- [훈련 데이터 정제와 형식](../concepts/training-data-cleaning-and-formatting.md) — 이 단계 뒤의 정제
- [훈련 데이터 품질](../concepts/training-data-quality.md) — 유일성이 품질 특성으로 요구되는 자리
- [데이터 오염](../concepts/data-contamination.md) — 중복이 벤치마크를 무너뜨리는 쪽
- [참조 데이터에 대한 유사도 측정](../concepts/similarity-measurements-against-reference-data.md) —
  중복 판정에 쓰이는 측정
- [벡터 색인과 임베딩](../concepts/vector-indexes-and-embeddings.md) — 차원 축소 쪽이 기대는 구조
- [배치 처리의 유스케이스](../concepts/batch-use-cases.md) — 중복 문서 제거가 배치 전처리로 서술되는 쪽
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 스트림 쪽에서 같은
  낱말이 다른 문제를 가리키는 자리

[^huyen2025]: Huyen 2025, 8장 "Dataset Engineering" (책 pp.363–404) 중 "Deduplicate Data"
    (pp.399–400). Table 8-3(p.399)은 원문 표기를 그대로 옮겼고, 회색 음영으로 표시된 중복 행은
    표에서 색으로 재현할 수 없어 본문 설명으로 옮겼다. 중복의 세 형태와 세 수단의 이름은 원문
    표기를 그대로 두었다. 이 구간에는 도판이 없다. Lee et al.(2021)·Tirumala et al.(2023)·
    Hernandez et al.(2022)는 huyen2025를 통한 전언이다.

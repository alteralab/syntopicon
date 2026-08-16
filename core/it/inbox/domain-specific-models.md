---
type: concept
title: 도메인 특화 모델
status: draft
description: 범용 모델이 못 하는 일이 남는 이유는 그 데이터가 인터넷에 없기 때문이다 — C4의 도메인 분포, 비전 데이터 분포 분석의 공백, CLIP 계열의 벤치마크 차이, 그리고 AlphaFold·BioNeMo·Med-PaLM2가 서 있는 자리
generated: { by: "claude-opus-5", at: "2026-08-16T19:00:00Z" }
sources:
  - { id: huyen2025, resource: /it/sources/huyen2025.md }
---

# 도메인 특화 모델

- [범용 모델이 여러 도메인을 잘하는 이유](#범용-모델이-여러-도메인을-잘하는-이유)
- [비전 데이터의 도메인 분포는 덜 알려져 있다](#비전-데이터의-도메인-분포는-덜-알려져-있다)
- [범용 모델이 못 하는 일](#범용-모델이-못-하는-일)
- [실물들](#실물들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **범용 파운데이션 모델이 있는데도 도메인 특화 모델이 남는 이유는 무엇인가.**

## 범용 모델이 여러 도메인을 잘하는 이유

- **Gemini·GPT·Llama 같은 범용 모델은 코딩·법률·과학·비즈니스·스포츠·환경 과학을 포함하되 그에
  국한되지 않는 넓은 범위의 도메인에서 놀랍도록 잘 수행할 수 있다. 이것은 주로 그 도메인들이
  훈련 데이터에 포함된 덕이다** (2장, p.56).[^huyen2025]
- 《워싱턴 포스트》의 2023년 분석에 따른 C4 데이터셋의 도메인 분포다. 저자가 도판으로 실은 것을
  수치만 옮겼다 (2장, p.56, Figure 2-3):[^huyen2025]

  | 도메인 | 비율 |
  |---|---|
  | Business & Industrial | 16.0% |
  | Technology | 15.0% |
  | News & Media | 13.0% |
  | Arts & Entertainment | 11.0% |
  | Science & Health | 9.0% |
  | Hobbies & Leisure | 8.0% |
  | Jobs & Education | 7.0% |
  | Home & Garden | 6.0% |
  | Travel | 6.0% |
  | Community | 5.0% |
  | Law & Government | 4.0% |

  - 도판에 저자가 단 단서 — **이 분석의 주의점 하나는 그것이 포함된 범주만 보여 줄 뿐 빠진
    범주는 보여 주지 않는다는 것이다** (2장, p.56).[^huyen2025]

## 비전 데이터의 도메인 분포는 덜 알려져 있다

- 공백의 확인 — **집필 시점 기준 비전 데이터의 도메인 분포에 대한 분석은 많지 않았다. 이미지가
  텍스트보다 범주화하기 어렵기 때문일 수 있다** (2장, p.56).[^huyen2025]
  - 각주의 이유 — **텍스트에서는 도메인 키워드를 휴리스틱으로 쓸 수 있지만 이미지에는 뻔한
    휴리스틱이 없다. 비전 데이터셋에 대해 찾을 수 있었던 대부분의 분석은 이미지 크기·해상도·비디오
    길이에 관한 것이다** (2장, p.56 각주 4).[^huyen2025]
- 우회로 — **그러나 모델의 벤치마크 성능에서 그 모델의 도메인을 추론할 수 있다** (2장,
  p.56).[^huyen2025]
- 저자가 든 대비다 (2장, p.57, Table 2-3):[^huyen2025]

  | Dataset | CLIP (Accuracy of ViT-B/32, OpenAI) | Open CLIP (Accuracy of ViT-B/32, Cade) |
  |---|---|---|
  | ImageNet | 63.2 | 62.9 |
  | ImageNet v2 | – | 62.6 |
  | Birdsnap | 37.8 | 46.0 |
  | Country211 | 17.8 | 14.8 |
  | Oxford 102 Category Flower | 66.7 | 66.0 |
  | German Traffic Sign Recognition Benchmark | 32.2 | 42.0 |
  | Stanford Cars | 59.4 | 79.3 |
  | UCF101 | 64.5 | 63.1 |

  - 저자가 이 표에 붙이는 한계 — **이 벤치마크들은 두 모델이 새·꽃·자동차와 몇 가지 범주에서
    얼마나 잘하는지를 보여 주지만, 세계는 이 몇 안 되는 범주보다 훨씬 크고 복잡하다** (2장,
    p.56).[^huyen2025]

## 범용 모델이 못 하는 일

- 경계 (2장, p.57):[^huyen2025]

  > Even though general-purpose foundation models can answer everyday questions about different
  > domains, they are unlikely to perform well on domain-specific tasks, especially if they never
  > saw these tasks during training.

- 저자가 든 두 예 — **도메인 특화 과제의 두 예가 신약 발견과 암 검진이다. 신약 발견은 단백질·
  DNA·RNA 데이터를 다루는데 이들은 특정 형식을 따르고 얻기에 비싸다. 이 데이터는 공개된 인터넷
  데이터에서 발견될 가능성이 낮다. 마찬가지로 암 검진은 통상 X선과 fMRI(기능적 자기공명영상) 스캔을
  포함하는데 이것은 사생활 문제로 얻기 어렵다** (2장, p.57).[^huyen2025]
- 그래서 남는 일 — **이런 도메인 특화 과제에서 잘 수행하도록 모델을 훈련하려면 아주 구체적인
  데이터셋을 큐레이션해야 할 수 있다** (2장, p.57).[^huyen2025]

## 실물들

- **아마 가장 유명한 도메인 특화 모델은 DeepMind의 AlphaFold로, 알려진 단백질 10만 개 정도의
  서열과 3차원 구조로 훈련되었다. NVIDIA의 BioNeMo는 신약 발견을 위한 생체분자 데이터에 초점을
  맞춘 또 다른 모델이다. 구글의 Med-PaLM2는 LLM의 힘과 의료 데이터를 결합해 의료 질의에 더 높은
  정확도로 답한다** (2장, p.57).[^huyen2025]
- 생의학 밖으로도 열려 있다는 저자의 관측 — **도메인 특화 모델은 생의학에서 특히 흔하지만 다른
  분야도 그로부터 이익을 볼 수 있다. 건축 스케치로 훈련된 모델이 Stable Diffusion보다 건축가를
  더 잘 도울 수 있고, 공장 도면으로 훈련된 모델이 ChatGPT 같은 일반 모델보다 제조 공정에 훨씬
  잘 최적화될 수 있다** (2장, p.57).[^huyen2025]

## 이어지는 페이지

- [훈련 데이터 큐레이션](../concepts/training-data-curation.md) — 도메인 큐레이션이 나오게 된
  데이터 출처의 문제
- [다국어 모델](../concepts/multilingual-models.md) — 같은 논리의 언어 판
- [파운데이션 모델](../concepts/foundation-models.md) — 과제 특화에서 범용으로의 전환, 그리고
  CLIP이 속한 임베딩 모델의 계보
- [모델 적응 기법](../concepts/model-adaptation-techniques.md) — 범용 모델 위에 도메인을 얹는
  기법들

[^huyen2025]: Huyen 2025, 2장 "Understanding Foundation Models" (책 pp.49–112). 이 페이지는
    "Domain-Specific Models" 절(pp.56–57)을 담았다. Figure 2-3(C4 도메인 분포 원그래프, p.56)은
    그림을 옮기지 않고 표시된 수치만 표로 옮겼다. Table 2-3(p.57)은 원문 표기를 그대로 옮겼다.
    《워싱턴 포스트》 2023년 분석은 huyen2025를 통한 전언이다.

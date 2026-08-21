---
type: concept
title: 모델 사이의 오류 상관
description: 벤더도 아키텍처도 다른 언어 모델들이 같은 오답으로 모이는지를 리더보드 두 곳과 이력서 평가로 잰 2025년 실측 — 둘 다 틀렸을 때 같은 답을 고르는 비율이 우연 기준의 두 배라는 결과, 같은 회사·같은 기반 아키텍처가 상관을 올린다는 회귀와 그것을 통제해도 정확한 모델끼리 더 겹친다는 결과, 판정자로 쓰면 자기보다 못한 모델의 정확도를 부풀린다는 사례 연구, 그리고 문항 수가 논문 안에서 어긋나는 자리
generated: { by: "claude-opus-5", at: "2026-08-21T21:00:00Z" }
sources:
  - { id: kim2025-error-correlation, resource: /it/sources/kim2025-error-correlation.md }
---

# 모델 사이의 오류 상관

- [이 페이지의 범위](#이-페이지의-범위)
- [무엇을 어디에 대고 쟀는가](#무엇을-어디에-대고-쟀는가)
- [문항 수는 논문 안에서 어긋난다](#문항-수는-논문-안에서-어긋난다)
- [오답이 겹치는 정도](#오답이-겹치는-정도)
- [무엇이 상관을 설명하는가](#무엇이-상관을-설명하는가)
- [유능할수록 더 겹친다](#유능할수록-더-겹친다)
- [판정자로 쓸 때 무슨 일이 생기는가](#판정자로-쓸-때-무슨-일이-생기는가)
- [저자들이 한정한 것](#저자들이-한정한-것)
- [근거 등급과 유통기한](#근거-등급과-유통기한)
- [고전과 무엇이 같고 무엇이 다른가](#고전과-무엇이-같고-무엇이-다른가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **벤더도 기반 아키텍처도 다른 모델들은 서로 다른 입력에서 틀리는가.**

## 이 페이지의 범위

이 페이지가 담는 것은 **모델 사이의 오류 상관(correlated errors)**을 실제로 잰 결과
하나와 그 결과에 붙은 단서들이다. 상관이 얼마나 되는가, 무엇이 그것을 설명하는가,
그리고 그 상관이 **판정자(LLM-as-judge)** 자리로 넘어갈 때 무슨 일이 생기는가까지다.

**같은 논문의 노동시장 사례 연구(§5)는 여기 담지 않는다.** 여러 회사가 같거나 비슷한
모델로 이력서를 거를 때 지원자가 모든 곳에서 떨어지는 비율이 어떻게 되는가는 알고리즘
독점문화(algorithmic monoculture)의 물음이지 이 KB의 검증 축 물음이 아니다. 그 자료가
이 페이지에 남긴 것은 하나뿐이다 — 상관은 하류 결과를 바꾼다.

## 무엇을 어디에 대고 쟀는가

- **자료가 셋이다** — 리더보드(leaderboard) 두 곳에서 받은 객관식 응답 자료 둘과, 저자들이
  직접 만든 이력서 평가 자료 하나다 (§3.1).[^kim2025-error-correlation] HUGGINGFACE는
  HuggingFace Open LLM Leaderboard 2에서 349개 모델, HELM은 스탠퍼드 HELM에서 71개 모델,
  RESUMES는 저자들이 20개 모델에 1,800건의 이력서–채용공고 쌍을 채점시킨 것이다.
  앞의 둘은 MMLU 문항을 쓰고 정답 라벨이 있다.
- **HELM의 71개 모델은 15개 회사에 걸쳐 있다** — OpenAI·Anthropic·Google·DeepSeek·Qwen
  등이고, 한 회사가 같은 모델의 여러 판을 냈으면 최신 판들이 들어 있다
  (Appendix A.1).[^kim2025-error-correlation] HUGGINGFACE 쪽은 원래 2,041개 모델에서
  349개로 줄인 것이다 — 쌍 단위 분석의 계산량이 모델 수의 제곱에 비례해 늘어나기 때문이고, 개인이
  미세 조정한 모델은 사람당 최대 5개까지만 넣어 한 사람이 자료를 지배하지 않게 했다.
- **상관의 지표는 "둘 다 틀렸을 때의 일치율(agreement rate when both models are wrong)"이다**
  (§3.1):[^kim2025-error-correlation]

  > through *agreement rate when both models are wrong*: when two models are wrong, how often
  > do their wrong answers coincide?

- **그 지표를 고른 이유가 명시돼 있다** — 정확도가 만드는 교란을 줄이려는 것이다
  (§3.1):[^kim2025-error-correlation]

  > These measures of error correlation aim to reduce confounding based on model accuracy:
  > two independently accurate models will agree on a large fraction of questions in which they
  > both give the correct answer. We, in contrast, are primarily interested in correlated
  > *errors*.

  RESUMES에서는 정답 라벨이 없으므로 대신 **잔차의 상관**을 쓴다 — 모델 점수와 사람 점수의
  차이를 모델 쌍마다 상관 낸다. 저자들은 여기서 사람 점수를 근거 진리(ground truth)로 다루되 이력서와
  공고의 적합성 평가가 주관적이라는 것을 같은 자리에 적는다 (§3.1).[^kim2025-error-correlation]

## 문항 수는 논문 안에서 어긋난다

**이 절은 이 논문의 수치를 옮기려는 사람이 먼저 읽어야 하는 자리다.** 두 리더보드의 문항
수가 논문 안에서 서로 다르게 배정돼 있다.

| 어디 | HUGGINGFACE | HELM |
|---|---|---|
| §1 서론 | 14,402 문항 | 12,032 문항 |
| Table 1 (§3.2) | 14,042 응답/모델 | 12,032 응답/모델 |
| Appendix A.1 | 12,032 문항 · 91개 MMLU 데이터셋 · 14개 범주 · 대부분 10지선다 | 14,042 문항 · 57개 범주 · 4지선다 한정 |

- **어긋나는 것은 문항 수의 배정뿐이다.** 모델 수(HUGGINGFACE 349, HELM 71)는 세 자리가
  모두 같고, 선택지 수 서술도 본문 §3.2와 Appendix A.1이 어긋나지 않는다 — HELM은 오답
  선택지가 3개고 HUGGINGFACE는 3지에서 10지까지이며 80% 이상이 10지선다다.
- **이 KB는 Appendix A.1의 배정을 쓴다.** 그쪽에만 데이터셋의 성격(범주 수·선택지 수·출처
  데이터셋 수)이 함께 적혀 있고, 그 성격 서술이 본문 §3.2의 우연 기준 계산과 맞물리기
  때문이다. #hypothesis 곧 **HELM은 모델 71개에 문항 14,042개(4지선다), HUGGINGFACE는 모델 349개에
  문항 12,032개(대부분 10지선다)**으로 읽는다. 이것은 이 KB의 판정이고, 논문 자신은 세 자리에서
  다르게 적는다.
- **그래서 이 페이지는 문항 수를 분모로 쓰는 수치를 인용하지 않는다.** 아래에서 인용하는
  값들의 분모는 전부 **모델 쌍의 수**이고, 그것은 모델 수에서 결정되므로 이 불일치에 걸리지
  않는다 (HELM은 모델 71개에서 나오는 쌍 2,485개, HUGGINGFACE는 모델 349개에서 나오는 쌍
  60,726개 — 두 값 모두 Appendix C의 회귀표에 관측 수로 인쇄돼 있다).[^kim2025-error-correlation]

## 오답이 겹치는 정도

- **결과 절의 첫 문단이 이 페이지의 중심 수치다** (§3.2):[^kim2025-error-correlation]

  > (1) First, models substantially agree, even when both are wrong. Conditional on having the
  > wrong answer, uniformly random model responses would yield an agreement rate of 1/3 on the
  > HELM, since each question has 3 incorrect answer choices. On HUGGINGFACE, this agreement
  > rate at random would be 0.127. On both datasets, almost all pairs (100% of pairs on
  > HuggingFace; 97.5% on Helm) of models have a higher agreement rate than the respective
  > baselines. The mean agreement rate across pairs is 0.423 on HuggingFace and 0.6 on Helm,
  > about double or higher than the baselines.

  같은 값을 단위와 분모를 붙여 다시 적는다. **집계 단위는 모델 쌍이고, 각 쌍의 값은
  "두 모델이 모두 틀린 문항" 안에서의 일치 비율이다.** 우연 기준은 오답 선택지 수에서
  나온 것이지 측정값이 아니다.

  | 자료 | 모델 수 | 모델 쌍 수 | 우연 기준(원값) | 쌍 평균 일치율(원값) | 기준 초과 쌍 |
  |---|---|---|---|---|---|
  | HELM | 71 | 2,485 | 0.333 (오답 3지) | 0.6 | 97.5% |
  | HUGGINGFACE | 349 | 60,726 | 0.127 (3~10지 혼합) | 0.423 | 100% |

  (§3.2, Figure 1a·1b; 쌍 수는 Appendix C Table 2·Table 5의 관측
  수).[^kim2025-error-correlation]
- **일치율의 행렬을 눈으로 볼 수 있는 자리는 Figure 1이다** — 모델을 정확도 순으로 정렬한
  쌍별 일치율 히트맵이고, 그림 설명이 "거의 모든 모델 쌍이 무작위 불일치가 함의하는 것보다
  높은 일치율을 보인다"고 적는다 (Figure 1).[^kim2025-error-correlation]
- **설명되지 않는 쌍도 있다** (§3.2):[^kim2025-error-correlation]

  > However, some models are unexpectedly correlated. For example, on Helm,
  > *google/text-unicorn@001* and *writer/palmyra-x-v3* agree on 0.9987 fraction of the
  > questions on which both are incorrect (about 22% of all questions), and a higher overall
  > agreement rate; to our knowledge, there is no publicly stated direct relationship between
  > the models.

  **회사도 다르고 공개된 관계도 없는 두 모델의 오답이 거의 완전히 겹친 사례다.** 반대편
  극에는 설명되는 쌍이 있다 — 같은 §3.2가 meta의 시각 언어 모델과 그 바탕이 된 언어 전용
  모델 쌍의 일치율을 0.97로 적고, 그것은 예상되는 값이라고 쓴다.

## 무엇이 상관을 설명하는가

- **모델 쌍을 표본으로 삼은 회귀 하나가 답한다** (§3.2, Table 1; 전체 회귀는 Appendix C
  Table 2~9).[^kim2025-error-correlation] 종속변수는 위의 "둘 다 틀렸을 때의 일치율"이고,
  수치 특성(정확도 등)은 표준화돼 있다. 계수는 전부 원값이며 단위는 일치율의 절대 차이다.

  | 항 | HELM (쌍 2,485) | HUGGINGFACE (쌍 60,726) |
  |---|---|---|
  | 절편 | 0.6018 | 0.3984 |
  | 같은 회사 | +0.0216 | +0.0658 |
  | 같은 기반 아키텍처(base architecture) | 특성 없음 | +0.0759 |
  | 정확도 1 | +0.0549 | +0.0138 |
  | 정확도 2 | +0.0544 | +0.0131 |
  | 정확도 1과 정확도 2의 교호작용 | +0.0264 | +0.0227 |
  | 결정계수 R² | 0.613 | 0.340 |

  (Appendix C Table 5·Table 2. 표시된 계수는 전부 p 값 0.001 미만. HELM에 아키텍처 항이 없는
  것은 특성이 없어서다 — HELM 모델 상당수가 독점 모델이라 파라미터 수와 기반 아키텍처가
  일관되게 공개돼 있지 않다, §3.1.)[^kim2025-error-correlation]
- **저자들의 요약** (§3.2):[^kim2025-error-correlation]

  > We find that models by the same developer, using the same base architecture, and having
  > similar sizes are all associated with higher agreement rates. Notably, more accurate models
  > (and especially if both models are accurate) are more correlated. The included features
  > explain between 34% and 62% of the variation in error agreement across the three datasets.

- **여기가 "이름은 독립의 증거가 아니다"가 서는 자리다.** 같은 회사라는 사실은 상관을
  올린다 — 그러나 HELM에서 그 몫은 +0.0216이고, **회사가 다른 쌍의 기준선 자체가 0.6018**이다
  (수치 특성이 표준화돼 있으므로 절편은 평균 정확도의 서로 다른 회사 쌍에 해당한다). 우연
  기준 0.333의 배에 가까운 값이 벤더를 갈라도 남는다. 위의
  google/text-unicorn@001 ↔ writer/palmyra-x-v3 쌍이 그 극단의 실물이다.
- RESUMES에서도 방향은 같다 — 잔차 상관을 종속변수로 한 회귀의 절편이 0.6534이고 같은 회사
  항은 +0.0210이며, 사람 점수와의 상관이 높은 모델끼리(즉 개별적으로 정확한 모델끼리)의
  교호작용 항이 +0.0429다. 다만 이 자료에서 같은 회사 항은 p 값 0.092로 유의하지 않다
  (Appendix C Table 8, 관측 190쌍, 결정계수 R² 0.415).[^kim2025-error-correlation]

## 유능할수록 더 겹친다

**이 절이 이 항목이 KB에 들어온 이유다.** 상관이 크다는 것보다, 상관이 **성능과 같은
방향으로 움직인다**는 것이 이 논문의 고유한 결과다.

- **초록이 그것을 한 문장으로 적는다** (초록):[^kim2025-error-correlation]

  > Crucially, however, larger and more accurate models have highly correlated errors, even
  > with distinct architectures and providers.

  이 문장의 근거는 위 회귀다 — 같은 회사·같은 기반 아키텍처를 통제한 뒤에도 정확도 항과
  그 교호작용 항이 양수로 남는다.
- **결론 절이 같은 것을 결과 언어로 다시 적는다** (§6):[^kim2025-error-correlation]

  > We show that LLMs have correlated errors, and that this correlation is substantially higher
  > for individually accurate models and those by the same developer or using the same base
  > architecture. These findings suggest that as model performance increases, models are also
  > converging in the errors that they make.

- **그래서 "더 좋은 모델을 여럿 쓰면 독립성이 커진다"는 기대는 이 자료와 어긋난다.** 개별
  정확도와 상호 독립성이 같은 방향으로 가지 않고 반대 방향으로 간다. 이 KB가 이 결과에서
  가져가는 조항은 하나다 — **독립성은 이름(벤더·주체)이 아니라 상관으로 판정한다.**

## 판정자로 쓸 때 무슨 일이 생기는가

- **판정자 사례 연구의 설계** — 한 모델을 판정자로 세우고 그 답을 근거 진리 대신 써서 다른
  모델들의 정확도를 매긴다. 판정자는 같은 벤더(HELM) 또는 같은 아키텍처(HUGGINGFACE) 안에서
  가장 정확한 모델로 골랐다 (§4).[^kim2025-error-correlation]
- **결과는 한 방향으로 기운다** (§4):[^kim2025-error-correlation]

  > A stark pattern emerges: each judge systematically inflates the accuracy of models that are
  > less accurate than itself, due to correlated errors (the judge marks incorrect answers as
  > correct if both models agree on the incorrect answer). On the other hand, each judge
  > underinflates the accuracy of models that are more accurate than itself (the judge cannot
  > reward a model for answering correctly on a question it itself answers incorrectly).

  **기제가 명시돼 있다는 점이 중요하다** — 부풀림은 판정자의 관대함이 아니라 **오류 상관의
  산술적 귀결**이다. 판정자와 대상이 같은 오답을 고르면 그 문항은 정답으로 집계된다.
  결과 도판은 HELM이 Figure 2, HUGGINGFACE가 Figure 8이고, 세로축이 부풀림(판정 정확도 빼기
  참 정확도), 가로축이 대상 모델의 참 정확도다.
- **같은 벤더·같은 계열이면 더 심하다** — §4는 같은 벤더의 모델을 붉은 점으로 그리고, 판정자가
  그 모델들의 정확도를 크게 부풀리는 사례가 보인다고 적는다. 저자들은 이것을 자기 선호
  (self-preferencing) 우려와 연결하며, **자기 선호가 같은 계열의 다른 모델 사이에서도 일어날
  수 있다**는 뜻이라고 쓴다 (§4).[^kim2025-error-correlation]
- **저자들의 처방** (§4):[^kim2025-error-correlation]

  > More generally, the results suggest that, when comparing models or establishing error rates
  > using LLM-as-judge, it is important to calibrate error metrics for each model-judge pair
  > using ground-truth data.

  곧 판정자를 바꿔서 푸는 문제가 아니라 **모델–판정자 쌍마다 근거 진리로 보정해야 하는**
  문제다.
- 이 절이 말하는 자기 선호는 **판정자가 자기 것임을 알아보아서** 생기는 것이 아니라
  오류가 겹쳐서 생긴다. 자기 것임을 알아보는 쪽에서 자기 선호를 설명하려 한 실험은
  [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md)에 있고,
  거기서도 인과는 확정되지 않았다. **두 설명은 경쟁하는 것이 아니라 서로 다른 자리를
  덮는다** — 이쪽은 판정자와 대상이 다른 모델일 때, 저쪽은 같은 모델일 때다.

## 저자들이 한정한 것

- **지표가 오답들을 똑같이 취급한다** (§6):[^kim2025-error-correlation]

  > Finally, note that one limitation of current metrics (including ours and that of Goel et al.
  > (2025)) is that they treat incorrect answers identically; in practice, some incorrect
  > answers may be “closer” to correct, and so preferred by more accurate models; some questions
  > may also be harder than others.

  **이것이 "유능할수록 더 겹친다"에 붙는 가장 중요한 단서다.** 정답에 가까운 오답을
  정확한 모델들이 함께 고르는 것과, 같은 오해를 공유해 같은 답으로 모이는 것을 이 지표는
  가르지 못한다.
- **잰 것은 객관식과 오프라인 점수뿐이다** — 저자들은 리더보드의 객관식 지표와 이력서 수치
  채점에 기댄 것이 모델 능력의 제한된 단면만 보여 준다고 적고, 열린 생성과 복잡한 추론에
  대한 더 풍부한 평가는 후속 과제로 남긴다 (§6).[^kim2025-error-correlation]
- **RESUMES의 근거 진리는 사람 라벨이고 주관적이다** (§3.1).[^kim2025-error-correlation]
  손라벨은 1,800쌍 중 450쌍에만 붙어 있다.
- **동시기 연구가 둘 있고 이 KB는 그 원문을 확보하지 않았다** — §2가 Wenger & Kenett 2025와
  Goel et al. 2025을 같은 물음의 동시기 작업으로 소개하고, 뒤쪽은 모델 정확도를 보정하는
  별도 유사도 지표를 만들어 **더 유능한 모델이 더 비슷한 실수를 한다**는 같은 방향의 결과를
  냈다고 적는다 (§2).[^kim2025-error-correlation] **원문 미확보이므로 이 서술은 이 논문을
  통한 2차 전언이고, 그쪽 지표의 계수나 수치는 이 KB에 옮기지 않는다.**

## 근거 등급과 유통기한

**근거 등급: `peer-reviewed`.** 확보본 1쪽이 "Proceedings of the 42nd International
Conference on Machine Learning, Vancouver, Canada. PMLR 267, 2025"라 인쇄한 본회의
논문이지 워크숍 원고가 아니다. 그 등급이 여는 것은 **이 논문이 스스로 잰 값**뿐이므로,
위에서 인용한 수치는 전부 §3.2·§4와 Appendix C의 자기 측정이고 이 논문이 인용한 제3자
수치는 하나도 옮기지 않았다.

**이 페이지의 수치에는 유통기한이 있다.** 이 항목 자체가 LLM 시대의 실측이므로 무엇을
언제 쟀는지가 결과의 범위다.

| 무엇에 묶여 있는가 | 이 자료의 값 |
|---|---|
| 모델 집합 | HELM 71개(15개 회사)·HUGGINGFACE 349개·RESUMES 20개 |
| 모델 시점 | Appendix D의 HELM 표에서 가장 새 모델이 claude-3-5-sonnet-20241022 · gpt-4o-2024-08-06 · gemini-1.5-pro-002 · llama-3.1/3.2 · qwen2.5 — 곧 2024년 말까지 공개된 세대 |
| 과제 | MMLU 계열 객관식과 이력서–공고 적합성 수치 채점. 열린 생성은 아니다 |
| 판정 근거 | 리더보드의 정답 라벨과 저자들의 손라벨 |

- **낡는 것과 낡지 않는 것을 갈라 둔다.** 절대 수치(0.6·0.423·계수들)는 위 모델 집합과
  시점에 묶여 있다. 방향(같은 회사·같은 아키텍처가 상관을 올린다, 정확한 모델끼리 더
  겹친다)은 저자들이 세 자료에서 함께 확인한 것이다.
- #hypothesis 모델 세대가 바뀌면 절대 수치는 다시 재야 한다. 다만 저자들의 결론이 "성능이
  오를수록 수렴한다"는 방향이므로, 세대가 새로워질수록 상관이 낮아질 것이라고 기대할 근거는
  이 자료 안에 없다.

## 고전과 무엇이 같고 무엇이 다른가

이 논문은 [독립 개발 판본의 실패 상관](../concepts/correlated-failure-of-independent-versions.md)이
1986년에 프로그램 판본 층에서 잰 것과 **같은 물음의 모델 층 대응물**이다. 두 소스는 서로를
인용하지 않는다 — 아래 대조는 이 KB의 읽기다.

| | 1986년 · 프로그램 판본 | 2025년 · 언어 모델 |
|---|---|---|
| 무엇이 여럿인가 | 같은 명세로 따로 짠 판본 27개 | 리더보드의 모델 71개와 349개 |
| 격리의 근거 | 다른 학교·다른 사람·대화 금지 | 다른 회사·다른 기반 아키텍처 |
| 무엇을 쟀나 | 같은 입력에서 함께 실패한 케이스 수 | 둘 다 틀린 문항에서 같은 답을 고른 비율 |
| 무엇과 비교했나 | 독립 가정으로 세운 확률 모형 | 오답을 균등 무작위로 고를 때의 일치율 |
| 결과 | 독립 모형을 99% 신뢰수준에서 기각 | 거의 모든 쌍이 우연 기준을 넘고 평균은 그 배 |

- **같은 것** — 독립적으로 만들었다는 사실이 독립적으로 틀린다는 것을 보장하지 않는다.
  두 자료 모두 **주체를 갈라도 상관이 남는다**를 관측했다.
- **이 논문이 더 말하는 것** — 1986년 실험은 판본의 개별 신뢰도와 상관의 관계를 재지 않았다.
  여기서는 그 관계가 회귀로 잡히고, 방향이 직관과 반대다. **개별적으로 더 정확한 쪽이 더
  상관돼 있다.**
- **1986년이 더 말하는 것** — 그쪽은 공유 기반이 **없는** 조건에서도 상관이 남는다는 것을
  통제된 실험 설계로 보였고, 결함이 동일하지 않아도 동시 실패가 난다는 기제를 저자들이
  뒤에 못 박았다. 이쪽은 관측 자료의 회귀라 그런 기제 설명이 없다 — §2가 표현 공간의
  동형성을 다룬 최근 연구들을 가리키며 "이 발견들이 우리 결과의 기계적 설명을 시사한다"고
  적는 것이 전부다 (§2).[^kim2025-error-correlation]

## 이어지는 페이지

- [독립 개발 판본의 실패 상관](../concepts/correlated-failure-of-independent-versions.md) — 같은 물음의
  고전 원전. 1986년 실험과 저자들이 1990년에 직접 그은 결론의 경계
- [AI 판정자](../concepts/ai-as-a-judge.md) — 이 페이지가 상관의 귀결을 보인 접근 자체
- [AI 판정자의 한계](../concepts/ai-judge-limitations.md) — 자기 편향과 판정자가 바뀌면 지표가 무너지는
  문제. 이 페이지는 그 편향이 **같은 벤더의 다른 모델 사이에서도** 나타난다는 실측을 더한다
- [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md) — 판정자와 대상이
  **같은 모델**일 때의 짝. 그쪽은 자기 것임을 알아보는 능력을 손잡이로 써서 자기 선호의
  인과를 세우려 한다
- [판정자 모델 고르기](../concepts/ai-judge-selection.md) — 판정자를 대상보다 강한 모델로 고르라는
  기준. 이 페이지의 결과는 그 기준에 조건을 붙인다 — 강한 판정자는 자기보다 약한 모델의
  정확도를 부풀리고, 강한 모델끼리는 더 상관돼 있다
- [테스트 오라클](../concepts/test-oracle.md) — 판정의 근거가 어디서 오는가의 분류. 여러 모델의 합의를
  오라클로 쓰는 구조가 무엇을 전제하는지가 이 페이지가 잰 것이다
- [데이터 오염](../concepts/data-contamination.md) — 훈련 코퍼스의 공유가 평가에 남기는 다른 자국

[^kim2025-error-correlation]: Kim, Garg, Peng & Garg 2025, "Correlated Errors in Large
    Language Models". 확보본이 PMLR camera-ready이나 자체 쪽번호가 1–29라 인쇄 쪽
    (PMLR v267 pp.30038–30066)과 대응되지 않으므로 locator는 절 번호와 표·그림 번호로만
    달았다. 인용은 전부 §3.1 이후의 방법·결과·사례 연구·결론 절과 Appendix A.1·C의 표에서
    했다 — §1 서론의 수치는 인용 금지 규칙에 걸려 옮기지 않았고, 초록에서 옮긴 것은 수치가
    아닌 결론 문장 하나뿐이다. 회귀 수치는 본문 Table 1이 아니라 관측 수가 함께 인쇄된
    Appendix C의 표에서 옮겼다 — 두 표의 계수는 같으나 HELM의 R²만 어긋난다(본문 Table 1은 0.618,
    Appendix Table 5는 0.613). §5(노동시장)와 Appendix B·D의 도판·모델 목록은
    이 페이지의 물음 밖이라 옮기지 않았고, Appendix D의 HELM 모델 표는 모델 집합의 시점
    판정에만 썼다. 이 논문이 언급하는 Goel et al. 2025 · Wenger & Kenett 2025 · Wu et al.
    2024 · Peng & Garg 2024a는 전부 원문 미확보라 2차 전언으로만 적었고 수치는 옮기지
    않았다.

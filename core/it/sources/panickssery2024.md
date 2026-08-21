---
type: article
title: "LLM Evaluators Recognize and Favor Their Own Generations"
author:
  - { family: "Panickssery", given: "Arjun" }
  - { family: "Bowman", given: "Samuel R." }
  - { family: "Feng", given: "Shi" }
issued: "2024-04"
publisher: "arXiv"
number: "2404.13076"
version: "v1"
URL: "https://arxiv.org/abs/2404.13076"
snapshot: /it/archive/panickssery2024/
snapshot_sha256: "2eea8d7ee37c1601c3c0f7156478e186ddd94381f0545962dfac9d06975a6c03"
accessed: "2026-08-21"
---

# panickssery2024

LLM 판정자가 자기 출력을 더 높게 매기는 현상(self-preference)이 자기 출력을 알아보는
능력(self-recognition)과 어떻게 이어지는지를 요약 과제에서 잰 논문이다. 이 KB에서는
**생성자와 판정자가 같은 모델일 때 무엇이 무너지는가**의 기제 원전으로 쓴다.

## 확보본의 지위 — 문면으로 확인한 것과 확인되지 않는 것

**확보본은 arXiv 프리프린트 판이다.** 1쪽 왼쪽 세로 스탬프가
`arXiv:2404.13076v1 [cs.CL] 15 Apr 2024`이고, 저자 줄은
`Arjun Panickssery 1 Samuel R. Bowman 2 3 Shi Feng 2`, 소속 각주는 `1 MATS`,
`2 New York University`, `3 Anthropic, PBC`, 교신 저자는 Shi Feng이다.

**게재 학회 줄은 문면 어디에도 인쇄돼 있지 않다.** 대신 PDF 메타데이터의 Subject가
"Proceedings of the International Conference on Machine Learning 2024", Keywords가
"Machine Learning, ICML"이다 — 곧 확보본은 **ICML 양식으로 조판된 v1**이다. 반입
대장이 적은 **NeurIPS 2024 게재와 oral 여부는 확보본 문면이 아니라 대장 기재**이고,
확보본으로는 어느 쪽도 확인되지 않는다. 그래서 이 KB는 이 소스를 **확보본 기준으로
프리프린트(`type: article`)로 등록**하고, 페이지 본문에도 그 판본 조건을 적었다.
게재본과 수치가 다를 수 있다.

## 인용할 때 지킬 것

**수치는 부록의 결과 표에서만 가져온다.** 본문 결과 절(§2.3·§2.4·§3.2)은 결론을
그림(Figure 2·4·7)으로만 보이고 숫자를 적지 않는다. 숫자가 있는 자리는 Table 1(p.6),
Table 6·7(pp.13–14), Table 8·9(pp.15–16), Table 11–14(pp.18–21)이다.

**§1 서론 끝의 "주요 발견" 목록에 실린 수치는 결과 표에서 재현되지 않는다.**

| 서론(p.2) | 결과 표에서 찾은 대응 값 |
|---|---|
| `GPT-4 is 73.5% accurate distinguishing itself from two other LLMs and humans` | Table 7 무-파인튜닝 GPT-4 쌍별 자기인식 0.672(XSUM)·0.747(CNN) — 두 값의 평균은 0.71이다 |
| `GPT-3.5 and Llama 2 both achieve over 90% accuracy at self-recognition after fine-tuning on 500 examples` | Table 7에서 0.90을 넘는 자기인식 점수는 GPT-3.5의 CNN 훈련·CNN 평가 셀(0.959) 하나뿐이다. Llama-2-7b는 네 조합(0.454·0.793·0.556·0.592) 어디서도 0.90에 닿지 않는다 |
| 같은 목록의 `All three LLMs ... achieve over 50% accuracy` | Table 7 무-파인튜닝 GPT-3.5의 CNN 자기인식은 0.481로 0.5 아래다 |

서론 수치와 표 값이 같은 척도인지도 문면으로는 확정되지 않는다 — 서론은 "accuracy",
표는 정규화된 신뢰도인 "self-recognition score"라 이름이 다르다. **그래서 이 KB의
페이지는 서론 수치를 인용하지 않고 Table 7 값만 쓴다.**

**Table 7의 `(In-Domain)`·`(Out-of-Domain)` 딱지는 두 열 묶음 중 한쪽에만 맞는다.**
이 표는 XSUM 열과 CNN 열을 함께 싣는데 블록 제목의 도메인 딱지는 하나뿐이다. 같은
실험을 데이터셋별로 나눠 실은 Table 11(XSUM)·Table 13(CNN)에서는 같은 블록에 반대
딱지가 붙는다. **딱지가 아니라 블록 제목의 훈련 데이터셋 이름으로 읽는다.**

## 각주 항목의 원문은 확보하지 않았다

반입 대장이 각주로 붙인 Sharma(ICLR 2024, RLHF 동조)는 **이 논문의 참고문헌에
아예 없다** — 확보본 전문에서 "Sharma"도 "sycophan"도 검출되지 않는다. 그러므로 이
소스를 경유한 앵커가 성립하지 않고, 이 KB는 그 항목에 대해 아무 서술도 두지 않는다.

이 논문이 관련 연구(§4)에서 언급하는 Liu et al. 2023, Koo et al. 2023,
Hoelscher-Obermaier et al. 2023, Xu et al. 2024는 전부 미확보다. 이 KB의 그것들에 대한
서술은 **이 논문을 통한 2차 전언**이고 수치는 옮기지 않는다.

## 유통기한

측정 대상은 GPT-4·GPT-3.5 Turbo·Llama-2-7b-chat이고 과제는 뉴스 요약 두 데이터셋
(XSUM·CNN/DailyMail)이다(§2.1). 곧 이 논문의 수치는 **2024년 4월까지의 모델 세대와
요약 과제**에 묶인 스냅샷이다.

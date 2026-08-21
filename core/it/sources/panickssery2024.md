---
type: paper-conference
title: "LLM Evaluators Recognize and Favor Their Own Generations"
author:
  - { family: "Panickssery", given: "Arjun" }
  - { family: "Bowman", given: "Samuel R." }
  - { family: "Feng", given: "Shi" }
issued: "2024"
container-title: "NeurIPS 2024"
event-title: "38th Conference on Neural Information Processing Systems (NeurIPS 2024)"
snapshot: /it/archive/panickssery2024/
snapshot_sha256: "d0e973011126cfccd1fb68bd843c1ea2f5a5874d7da3f79cce56581cb0d311ab"
accessed: "2026-08-21"
---

# panickssery2024

LLM 판정자가 자기 출력을 더 높게 매기는 현상(self-preference)이 자기 출력을 알아보는
능력(self-recognition)과 어떻게 이어지는지를 요약 과제에서 잰 논문이다. 이 KB에서는
**생성자와 판정자가 같은 모델일 때 무엇이 무너지는가**의 기제 원전으로 쓴다.

## 게재 지위 — 문면으로 확인한 것과 외부 레코드가 근거인 것

**게재본 1쪽 푸터가 문면 근거다** — `38th Conference on Neural Information Processing
Systems (NeurIPS 2024).` **워크숍이 아니라 본회의 논문집**이므로 이 KB에서
`peer-reviewed`로 취급한다. 다만 그 등급이 여는 것은 **이 논문이 스스로 잰 값**뿐이다.

**"oral"은 문면이 아니다.** 게재본 어디에도 발표 형식이 인쇄돼 있지 않고, 근거는
OpenReview 레코드(id `4NJBV6Wp0h`, venue 필드 `NeurIPS 2024 oral`)라는 **외부
레코드**다. 이 KB는 그 사실을 그렇게만 적고 문면으로 위장하지 않는다.

**권·호·쪽수는 적지 않는다.** 게재본은 1–31쪽으로 자체 페이지를 매기고 논문집 인쇄
쪽은 문면에 없다. 그래서 이 KB의 locator는 **게재본 자체 쪽수와 절·표 번호**다.

저자는 3인이다 — Arjun Panickssery(MATS), Samuel R. Bowman(New York University,
Anthropic PBC), Shi Feng(George Washington University). 교신 주소는
`arjun.panickssery@gmail.com`이다. **소속이 프리프린트와 다르다** — 프리프린트에서
Shi Feng은 New York University 소속이었고 교신 저자였다.

## 확보본은 두 벌이다

| 파일 | 무엇 | sha256 |
|---|---|---|
| `panickssery2024--neurips2024-camera-ready.pdf` | **정본.** NeurIPS 2024 게재본, 31쪽 | `e52e3e3bfa8a1c00…` |
| `panickssery2024.pdf` | 프리프린트 `arXiv:2404.13076v1`(2024-04-15), 21쪽, ICML 양식 조판 | `e1466f5ade614459…` |

**인용은 게재본으로만 한다.** 프리프린트를 함께 둔 이유는 두 판이 내용에서 갈리기
때문이고(아래 절), 이 KB의 페이지가 어느 판을 읽고 쓴 것인지 뒤에 확인할 수 있어야
해서다.

`snapshot_sha256`은 디렉터리 매니페스트 해시다. 이 값은 게재본을 더한 뒤 다시 계산한
것이라 첫 스냅샷(프리프린트 한 벌)의 값과 다르다. **변조가 아니라 같은 런에서 정본을
더한 결과**이고, 이후로는 이 값이 불변이다.

## 두 판이 갈리는 자리 — 프리프린트를 읽고 인용하면 틀린다

게재본에는 프리프린트에 **없던 절과 실험**이 있고, 절 번호가 밀렸으며, 정의문이 다시
쓰였다.

| 무엇 | 프리프린트 v1 | 게재본 |
|---|---|---|
| 사람 평가 실험 | 없음 | **§2.5 Human evaluation of preference 신설** — 자기선호가 실제 품질 차이에 비해 과한지를 사람 주석으로 잰다 |
| 순서 편향 대안 집계 | §2.5 | §2.6 |
| 자기인식과 상황 인식 | §4.2 별도 절 | 없어지고 §4.1로 합쳐짐 |
| 인과 미확정 선언 | §5.2 첫 문단 `Validation of the causal hypothesis` | 그 문단이 없어지고 §3 본문과 §5.1·§5.3의 `initial evidence`가 그 자리를 맡는다 |
| 쌍의 자기선호 합이 1을 넘는다 | §2.4 | §5.2로 옮겨짐 |
| 두 성질의 정의문 | 긴 형태 | **다시 쓰였다** — 직인용을 프리프린트에서 뜨면 문면이 틀린다 |
| 표본 서술 | `we sample 1,000 news articles from each of two datasets` | `2,000 randomly sampled news articles from two datasets` |

**결과 표의 값은 두 판이 같다.** Table 1(켄들 타우), Table 6(라벨 실험), Table 7(쌍별
결과)의 숫자와 표 번호가 일치한다. 쪽수만 밀렸다 — Table 6은 v1 p.13에서 게재본 p.15,
Table 7은 p.14에서 p.16, Table 1은 p.6에서 p.7이다.

## 인용할 때 지킬 것

**수치는 결과 표와 §2.5에서만 가져온다.** 본문 결과 절(§2.3·§2.4·§3.2)은 결론을
그림(Figure 2·4·7)으로만 보이고 숫자를 적지 않는다. 숫자가 있는 자리는 §2.5(사람 평가
승률), §2.6(순서 뒤집힘 비율), §3.2–3.3(켄들 타우와 역인과 배제), Table 1(p.7),
Table 6·7(pp.15–16, 부록 C), Table 8·9(pp.17–18), Table 11–14(pp.19–23), 부록 E(p.24)다.

**§1 서론 끝의 "주요 발견" 목록에 실린 수치는 결과 표에서 재현되지 않는다. 게재본에서도
동일하다** — 세 문장이 프리프린트와 같은 문면으로 남아 있고(게재본 p.2), 결과 표의 값도
바뀌지 않았으므로 어긋남이 그대로다.

| 서론(게재본 p.2) | 결과 표에서 찾은 대응 값 |
|---|---|
| `GPT-4 is 73.5% accurate at distinguishing its own summaries` | Table 7 무-파인튜닝 GPT-4 쌍별 자기인식 0.672(XSUM)·0.747(CNN) — 두 값의 평균은 0.71이다 |
| `GPT-3.5 and Llama 2 both achieve over 90% accuracy at self-recognition after fine-tuning on 500 examples` | Table 7에서 0.90을 넘는 자기인식 점수는 GPT-3.5의 CNN 훈련·CNN 평가 셀(0.959) 하나뿐이다. Llama-2-7b는 네 조합(0.454·0.793·0.556·0.592) 어디서도 0.90에 닿지 않는다 |
| `All three LLM evaluators achieve over 50% accuracy` | Table 7 무-파인튜닝 GPT-3.5의 CNN 자기인식은 0.481로 0.5 아래다 |

서론 수치와 표 값이 같은 척도인지도 문면으로는 확정되지 않는다 — 서론은 "accuracy",
표는 정규화된 신뢰도인 "self-recognition score"라 이름이 다르다. **그래서 이 KB의
페이지는 서론 수치를 인용하지 않고 결과 표 값만 쓴다.**

**Table 7의 `(In-Domain)`·`(Out-of-Domain)` 딱지는 두 열 묶음 중 한쪽에만 맞는다.**
이 표는 XSUM 열과 CNN 열을 함께 싣는데 블록 제목의 도메인 딱지는 하나뿐이다. 같은
실험을 데이터셋별로 나눠 실은 Table 11(XSUM)·Table 13(CNN)에서는 같은 블록에 반대
딱지가 붙는다. **딱지가 아니라 블록 제목의 훈련 데이터셋 이름으로 읽는다.**

**사람 평가의 분모가 §2.5와 부록 E에서 어긋난다.** §2.5(p.5)는 `resulting in 900
pairwise comparisons`라 적고 승률을 `calculated over 300 human annotators`라고 쓰지만,
부록 E(p.24)는 `900 pairwise judgments from 20 crowdworkers`이고 `For each of the 300
pairwise comparisons, we collect three annotations`라고 적는다. **부록 E 쪽이 산수가
맞는다** — 비교 300건에 주석 3벌이면 판정 900건이고, 주석자는 20명이다. §2.5의 "300
human annotators"는 주석자 수가 아니라 비교 건수로 읽어야 한다. 이 KB는 부록 E를
채택하고 그 사실을 페이지 본문에 적었다.

## 각주 항목의 원문은 확보하지 않았다

반입 대장이 각주로 붙인 Sharma(ICLR 2024, RLHF 동조)는 **이 논문의 참고문헌에
아예 없다** — 게재본과 프리프린트 전문 어디에서도 "Sharma"도 "sycophan"도 검출되지
않는다. 그러므로 이 소스를 경유한 앵커가 성립하지 않고, 이 KB는 그 항목에 대해 아무
서술도 두지 않는다.

이 논문이 관련 연구(§4)에서 언급하는 Liu et al. 2023, Koo et al. 2023,
Hoelscher-Obermaier et al. 2023, Xu et al. 2024는 전부 미확보다. 이 KB의 그것들에 대한
서술은 **이 논문을 통한 2차 전언**이고 수치는 옮기지 않는다.

## 유통기한

측정 대상은 GPT-4·GPT-3.5 Turbo·Llama-2-7b-chat이고 과제는 뉴스 요약 두 데이터셋
(XSUM·CNN/DailyMail)이다(§2.1). 곧 이 논문의 수치는 **2024년의 모델 세대와 요약
과제**에 묶인 스냅샷이다.

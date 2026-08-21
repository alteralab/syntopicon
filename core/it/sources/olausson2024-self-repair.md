---
type: paper-conference
title: "Is Self-Repair a Silver Bullet for Code Generation?"
author:
  - { family: "Olausson", given: "Theo X." }
  - { family: "Inala", given: "Jeevana Priya" }
  - { family: "Wang", given: "Chenglong" }
  - { family: "Gao", given: "Jianfeng" }
  - { family: "Solar-Lezama", given: "Armando" }
issued: "2024"
container-title: "ICLR 2024"
event-title: "ICLR 2024"
number: "2306.09896v5"
URL: "https://arxiv.org/abs/2306.09896v5"
snapshot: /it/archive/olausson2024-self-repair/
snapshot_sha256: "ca1374df9147210149bd6c68c80688d04c9400efa263928d8550cd2af6e6e33d"
accessed: "2026-08-21"
---

# olausson2024-self-repair

- [게재 지위 — 문면으로 확인한 것과 외부 레코드가 근거인 것](#게재-지위--문면으로-확인한-것과-외부-레코드가-근거인-것)
- [확보본은 한 벌이다](#확보본은-한-벌이다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [각주 항목의 원문은 확보하지 않았다](#각주-항목의-원문은-확보하지-않았다)
- [유통기한](#유통기한)

모델이 자기가 쓴 코드를 스스로 고치는 자기 수정(self-repair)이 표본을 더 뽑는 것보다
나은가를 같은 표본 예산에서 잰 논문이다. 이 KB에서는 **판정과 피드백을 생성자 자신에게
맡길 때 무엇이 병목이 되는가**의 실측 원전으로 쓴다.

## 게재 지위 — 문면으로 확인한 것과 외부 레코드가 근거인 것

**확보본 모든 쪽의 머리말이 문면 근거다** — `Published as a conference paper at
ICLR 2024`. 곧 이 파일은 **ICLR 2024 게재본(camera-ready)**이고, 이 KB에서
`peer-reviewed`로 취급한다. 다만 그 등급이 여는 것은 **이 논문이 스스로 잰 값**뿐이다.

**같은 파일이 arXiv 판이기도 하다.** 1쪽 옆단에 `arXiv:2306.09896v5 [cs.CL] 2 Feb 2024`가
인쇄돼 있다. 곧 v5가 게재본과 같은 조판이며, **게재본을 따로 구할 필요가 없다.**

**ICLR의 회차(제12회)와 발표 형식은 문면이 아니다.** 머리말은 `ICLR 2024`까지만 적고
회차도 포스터·구두 구분도 인쇄하지 않는다. 이 KB는 그 둘을 적지 않는다.

**권·호·쪽수는 적지 않는다.** 확보본은 1–49쪽으로 자체 페이지를 매기고 논문집 인쇄 쪽은
문면에 없다. 그래서 이 KB의 locator는 **확보본 자체 쪽수와 절·표·그림 번호**다.

저자는 5인이고 소속이 두 곳이다 — Theo X. Olausson(MIT CSAIL), Jeevana Priya Inala ·
Chenglong Wang · Jianfeng Gao(Microsoft Research), Armando Solar-Lezama(MIT CSAIL).
1쪽 각주가 교신 주소를 `theoxo@csail.mit.edu`로 적고, 이 작업의 일부가 Olausson이
Microsoft Research에 있던 동안 이루어졌다고 밝힌다. **판정 대상 모델 셋 가운데 둘이
상용 API 모델이라는 점과 저자 소속이 겹치는 자리는 원문이 따로 언급하지 않는다.**
코드와 데이터 주소는 `github.com/theoxo/self-repair`로 인쇄돼 있다(1쪽 각주).

## 확보본은 한 벌이다

| 파일 | 무엇 | 텍스트 레이어 |
|---|---|---|
| `olausson2024-self-repair.pdf` | ICLR 2024 게재본 = `arXiv:2306.09896v5`, 49쪽 | `text_based` (신뢰도 0.88, OCR 필요 0/49쪽) |

같은 논문의 이전 arXiv 판(v1–v4)은 확보하지 않았다. **판 사이의 차이를 이 KB는 모른다** —
그러므로 인용은 확보본으로만 하고, 다른 판을 읽고 locator를 대조하면 어긋날 수 있다.

## 인용할 때 지킬 것

**수치는 결과 절과 결과 표에서만 가져온다.** 이 논문의 서론(§1)은 끝의 `Contributions`
목록에서 이미 결과 수치를 미리 보이는데(1.05×·0.97×·1.58× 등, p.2), 이 KB는 서론 수치를
인용하지 않는 규칙을 따라 그 목록을 쓰지 않는다. 같은 값이 결과 절에도 있으면 결과 절에서
가져온다.

| 무엇 | 어디서 가져오는가 |
|---|---|
| 자기 수정의 기준선 대비 이득 | §4.1 본문(pp.5–6). 도판(Figure 3·4·5)은 수치를 인쇄하지 않는다 |
| 피드백 모델을 바꿨을 때의 방향 | §4.2 본문(p.8). **수치가 없고 방향 서술뿐이다** |
| 사람 피드백 대 GPT-4 피드백 | **Table 1(p.8)**과 §4.3 본문(p.8) |
| 피드백의 질적 분류 | §4.3 `Qualitative analysis`(p.9)의 분수 표기 |
| 실험 설계·초매개변수 | §3(pp.3–5), §4 머리말(p.5) |
| 한계 | §5(p.9) |

**§4.1의 이득 수치는 전부 `up to`가 붙은 상한이다.** `up to 8%`·`up to a 34%
performance gain`·`up to 10% improvement`·`up to 3%`가 그렇다. 하한도 중앙값도 문면에
없으므로 **범위를 아는 것처럼 옮기지 않는다.** 셋 다 기준선(같은 예산의 i.i.d. 표본)
대비 **상대 증가**이고 백분율점(%p)이 아니다.

**Table 1의 백분율은 정답률이 아니라 수리 성공률이다.** 분모는 표본 뽑은 수리 후보이고,
설계는 §4.3이 적는다 — GPT-4가 실패한 프로그램 40건, 그 각각에 사람 피드백 2벌
(참가자 16명, 응답 80건), (피드백, 프로그램) 쌍마다 GPT-4에서 수리 후보 25건. **집계
단위는 난이도 등급이고 `Overall` 열이 총계다.**

**pass@k의 정의가 이 논문에서 바뀐다.** 자기 수정은 초기 생성과 수리 양쪽에서 표본을
뽑으므로, 저자들은 수리 트리(repair tree) 하나를 `k = np + np·nfr` 표본과 같다고 놓고
같은 예산의 무-수리 기준선과 견준다(§3.2, p.4). **이 정의를 함께 옮기지 않으면 "이득"이
무엇 대비인지가 사라진다.**

## 각주 항목의 원문은 확보하지 않았다

반입 대장이 각주로 붙인 두 항목의 처리는 다음과 같다.

- **CodeT(Chen et al. 2023a, ICLR)** — 이 논문의 참고문헌에 실려 있고 §5 한계 절이
  자동 단위 테스트 합성 기법의 하나로 부른다(p.9). **원문은 미확보**이므로 이 KB의
  서술은 **이 논문을 통한 2차 전언**이고 수치는 옮기지 않는다.
- **Huang et al.(ICLR 2024)** — **이 논문의 참고문헌에 없다.** 전문에서 `Huang`은
  다른 저자(Qiuyuan Huang, Peng et al. 2023의 공저자)로만 검출된다. 그러므로 이 소스를
  경유한 앵커가 성립하지 않고, 이 KB는 그 항목에 대해 아무 서술도 두지 않는다.

이 논문이 관련 연구(§2)에서 언급하는 Zhang et al. 2023, Chen et al. 2023b, Madaan et al.
2023, Pan et al. 2023도 전부 미확보다. 이 KB의 그것들에 대한 서술은 **이 논문을 통한
2차 전언**이고 수치는 옮기지 않는다.

## 유통기한

측정 대상은 CodeLlama-13b-instruct와 두 상용 모델이고, 상용 쪽은 고정 엔드포인트
`gpt-3.5-turbo-0301`·`gpt-4-0314`다(§4 머리말과 각주 4·5, p.5). 과제는 HumanEval과
APPS의 자족적 파이썬 문제이고 APPS는 300문항 표본이다. 곧 이 논문의 수치는 **2023년에
동결된 모델 스냅샷과 파이썬 코드 생성 벤치마크 둘**에 묶인 값이다.

**자기 수정을 프롬프트로 구현한 실험이라는 점도 범위다** — §4 머리말이 `templated string
concatenation with one-shot prompting`이라고 적는다(p.5). 학습으로 자기 수정 능력을
집어넣은 방식은 이 논문이 재지 않았다.

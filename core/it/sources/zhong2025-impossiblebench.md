---
type: paper-conference
title: "ImpossibleBench: Measuring LLMs' Propensity of Exploiting Test Cases"
author:
  - { family: "Zhong", given: "Ziqian" }
  - { family: "Raghunathan", given: "Aditi" }
  - { family: "Carlini", given: "Nicholas" }
issued: "2025-10-23"
event-title: "ICLR 2026"
number: "2510.20270"
version: "v1"
URL: "https://arxiv.org/abs/2510.20270"
snapshot: /it/archive/zhong2025-impossiblebench/
snapshot_sha256: "143a5fcdbfb57a6f4c9dd9aed557aec8f4c02d8ef48a090fe2f7b91a3fcbf8aa"
accessed: "2026-08-22"
---

# zhong2025-impossiblebench

기존 코딩 벤치마크의 단위 테스트를 **명세와 충돌하도록 변이**시켜 정직하게는 통과할 수
없는 과제를 만들고, 그럼에도 통과한 비율을 그 모델의 **치팅률(cheating rate)**로 재는
프레임워크와 그 측정이다. 이 KB에서는 **테스트를 에이전트의 권한 안에 두면 무슨 일이
일어나는가**의 실측 원전으로 쓴다.

## 게재 지위 — 심사 실증(peer-reviewed), 단 문면이 아니라 레코드 근거

**확보본 문면은 게재를 말하지 않는다.** 1쪽 쪽머리가 `Preprint. Under review.`이고
좌측에 `arXiv:2510.20270v1 [cs.LG] 23 Oct 2025`가 인쇄돼 있다. 25쪽이다.

게재 확정의 근거는 **문면이 아니라 OpenReview 레코드**다 — 2026-08-22 조회에서
`api2.openreview.net`이 id `SeO4vyAj7E`, venue `ICLR 2026 Poster`,
venueid `ICLR.cc/2026/Conference`를 돌려주었다. 조회 결과 원문은 스냅샷의
`_openreview-record.txt`에 있다(밑줄 접두 = 우리가 만든 파일이라 다이제스트 밖이다).

**camera-ready PDF는 미확보다.** `openreview.net/pdf?id=SeO4vyAj7E`가 봇 차단으로
막히고 arXiv에는 v1밖에 없다. 그래서 **확보본은 투고 시점 판(v1)이고, 게재본 문면과의
대조는 수행되지 않았다.** 등급을 `peer-reviewed`로 표기하되 이 단서와 함께 표기한다.
개념 페이지가 인용하는 수치와 구절은 전부 **v1 문면 기준**이다.

## 인용 규칙 — 결과 절만, 그리고 설정을 붙이지 않은 단일 수치는 금지

- **이 논문에는 수치 결과 표가 없다.** 주 결과는 전부 그림(Figure 3~18)이고, 유일한
  표인 Table 1(p.7)은 프롬프트 변형 목록이다. 그래서 수치를 옮길 자리는 **결과 절의
  산문**(§4 p.5, §5 pp.7–8, §6 p.9, 부록 §E pp.16–18)뿐이다.
- **서론(§1, p.2)의 수치는 옮기지 않는다.** 서론에만 있고 결과 절에 다시 나오지 않는
  값이 셋 있다.

  | 서론이 적은 값 | 결과 절이 적는 값 | 위치 |
  |---|---|---|
  | GPT-5 `76%` Oneoff-SWEbench · `2.9%` Oneoff-LiveCodeBench | 없음. §4는 Conflicting-SWEbench `54.0%`만 적는다 | §1 p.2 대 §4 p.5 |
  | 프롬프트가 GPT-5를 `92%`에서 `1%`로 | prompt A·B가 `85%` 초과, prompt D가 `1%` | §1 p.2 대 §5.1 p.7 |
  | 감시자 검출 `42-65%`(Impossible-SWEbench) | Sonnet 4 `42-50%` · Opus 4 `57-65%`. 판정자 둘의 서로 다른 범위다 | §1 p.2 대 §6 p.9 |

  선례(run 10)에서는 게재본을 구해 서론과 결과 표의 불일치를 잡았다. 여기서는 게재본을
  못 구했으므로 **v1 안에서 서론과 결과 절을 대조**했고, 위 세 자리가 어긋난다.
  **어긋나는 자리는 결과 절 값만 쓴다.**
- **설정을 붙이지 않은 단일 수치는 인용 금지다.** 같은 논문 안에서 같은 숫자가 다른
  설정을 가리킨다. `54%`가 두 자리에 있는데 하나는 **GPT-5 · Conflicting-SWEbench ·
  full 스캐폴드**(§4, p.5)이고, 다른 하나는 **Opus 4.1 · Figure 1의 이름표**(p.2)다.
  Figure 1의 목록은 어느 데이터셋인지 캡션이 밝히지 않는다 — 그래서 이 KB는 Figure 1의
  이름표를 수치 출처로 쓰지 않는다.
- **분모를 함께 적는다.** Impossible-SWEbench는 SWE-bench Verified에서 만든 349문항,
  Impossible-LiveCodeBench는 LiveCodeBench v6(2025년 4월) hard 분할에서 만든 103문항이고,
  oneoff·conflicting 각각이 같은 과제 집합에서 나온다 (§F.1, p.19).
- **치팅률은 비율값(%)이지 퍼센트포인트가 아니다.** 정의는 불가능 과제에서의 통과율이고
  (초록 p.1, §1 p.2), 낮을수록 좋다. `54%에서 66%로`처럼 두 값을 잇는 서술은 그 두 설정
  사이의 이동이지 절대 증가폭이 아니다.
- **이 논문이 인용한 제3자 수치는 옮기지 않는다.** METR 블로그·Reddit 게시글·Opus 4.1
  시스템 카드는 §1과 §A에서 이름만 불린다 — 원전으로 가지 않았으므로 이 KB는 그 값을
  쓰지 않는다.

## 판본과 텍스트 레이어

텍스트 레이어 판정은 `text_based`(신뢰도 1.00, OCR 필요 0/25쪽)이라 기계 추출로 읽었다.
다만 **코드 diff와 그림 안 이름표는 다단 조판이라 추출 순서가 뒤섞인다** — 값과 코드를
옮길 때는 `pdftotext -layout`으로 정렬한 판을 대조했다. 그림 안의 막대 값은 이름표가
붙은 것만 읽히고 붙지 않은 것은 읽히지 않는다. 재개점은 `_progress.yaml`이 정본이다.

---
type: paper-conference
title: "An External Replication on the Effects of Test-driven Development Using a Multi-site Blind Analysis Approach"
author:
  - { family: "Fucci", given: "Davide" }
  - { family: "Scanniello", given: "Giuseppe" }
  - { family: "Romano", given: "Simone" }
  - { family: "Shepperd", given: "Martin" }
  - { family: "Sigweni", given: "Boyce" }
  - { family: "Uyaguari", given: "Fernando" }
  - { family: "Turhan", given: "Burak" }
  - { family: "Juristo", given: "Natalia" }
  - { family: "Oivo", given: "Markku" }
issued: "2016"
event-title: "ESEM '16"
publisher: "ACM"
DOI: "10.1145/2961111.2962592"
ISBN: "978-1-4503-4427-2"
snapshot: /it/archive/fucci2016-tdd-replication/
snapshot_sha256: "c5ed85f2ec4dd57f8aadfbe804db3d505720999e18e9528295832334f97b9740"
accessed: "2026-08-24"
---

# fucci2016-tdd-replication

**앞선 TDD 실험을 다른 나라의 다른 연구진이 다시 돌리되, 데이터 추출과 통계 분석을 목적을
모르는 제3의 두 기관에 맡긴 재현 연구.** 답은 **테스트 노력·외부 품질·생산성 어느 쪽에서도
TDD와 test-last의 차이를 찾지 못했다**는 것이고, 기준 실험의 결과가 재현된다.

**이 소스가 이 KB에서 서는 자리는 두 가지다.** 하나는 TDD 효과 주장의 재현 층이고, 다른
하나는 **연구자 편향을 설계로 막은 실물**이다 — 판정하는 사람을 대상에서 떼어 놓는 장치가
소프트웨어 공학 실증 안에서 어떻게 생겼는지를 보여 준다.

## 지위

- **근거 등급은 `peer-reviewed`다.** 게재 레코드가 1쪽 하단에 인쇄돼 있다 —
  `ESEM '16, September 08 - 09, 2016, Ciudad Real, Spain` ·
  `ACM 978-1-4503-4427-2/16/09` · `DOI: http://dx.doi.org/10.1145/2961111.2962592`.
- **논문집 쪽수는 확보본에 인쇄돼 있지 않다.** 그래서 frontmatter에 `page`를 적지 않았고,
  locator는 절 번호와 표 번호다.
- 확보본은 pdfTeX 산출물이라 OCR을 거치지 않았다. 인용한 표 수치는 렌더 이미지로 육안
  재확인했다(7쪽 Table 5·6·7·8).
- **저자군이 아홉이고 네 기관에 걸쳐 있다** — 오울루(원 실험) · 바실리카타(재현 실행) ·
  UPM(데이터 추출) · 브루넬(통계 분석).

## 무엇을 어떻게 쟀는가

- **기준 실험(baseline)은 오울루의 Fucci & Turhan 2013 실험이다**(§3). 학생 58명, 단일
  과제(Bowling Scorekeeper), 병렬 1요인 2처치 설계였고, 세 가설 모두 **기각에 실패**했다
  (Table 1). 효과 크기는 Pearson r로 각각 .16 · .04 · .11이다(§3.6).
- **재현은 바실리카타 대학원생 21명이고 설계가 다르다** — 균형 교차(crossover) 설계다(§4.5,
  Table 3). 참가자가 1일차와 2일차에 서로 다른 과제를 서로 다른 처치로 수행한다.
  - 과제는 MarsRover API(11 스토리)와 Bowling Scorekeeper(13 스토리)다(§4.6, 각주 7).
  - **분석에 쓰인 관측은 40개(참가자 20명 × 2회)다** — 산출물 하나가 수용 테스트를 돌릴
    소스 코드를 담고 있지 않아 제외됐다(§4.8, Table 5 캡션 `n=40`).
- **결과 변수 셋**: TESTS(작성한 JUnit 단정 수) · QLTY(착수한 스토리의 단정 통과율) ·
  PROD(전체 단정 통과율)다(§3.4).
- **눈가림이 두 단계다**(§4.8). ① UPM의 저자 한 명이 실험 동기·가설·설계를 모르는 상태로
  소스 코드에서 지표를 뽑고, ② 브루넬의 두 저자가 **열 이름을 지운 데이터셋**으로 통계를
  돌린다. 원래 라벨은 추론을 만들기 전에야 다시 붙였다.

## 결과 — 표에서만 가져온다

- **처치 비교는 비방향 일표본 부호 검정(one-sample sign test), n=20이다**(Table 6).
  세 가설 전부 `Failed to reject H0`이고 Cliff's δ는 전부 무시 가능(negligible)이다.

  | 가설 | p-value | Cliff's δ (CI) |
  |---|---|---|
  | R1T(테스트 노력) | 1.00 | 0.07 (-0.41, 0.29) |
  | R1Q(외부 품질) | 0.82 | -0.07 (-0.29, 0.41) |
  | R1P(생산성) | 0.82 | 0.14 (-0.22, 0.47) |

- **순서 효과는 셋 다 유의하다**(Table 7, Kruskal-Wallis, n=20, df=1) — TESTS χ²=7.43
  (p = .64 × 10⁻²) · QLTY χ²=8.69(p = .32 × 10⁻²) · PROD χ²=9.14(p = .24 × 10⁻²),
  전부 `Reject H0`.
- **이월 효과(carryover)는 셋 다 유의하지 않다**(Table 8, 같은 검정) — TESTS χ²=1.22
  (p=.27) · QLTY χ²=.09(p=.76) · PROD χ²=.02(p=.88), 전부 `Failed to reject H0`.
- **그래서 저자들이 남긴 미해결이 과제와 처치의 상호작용이다**(§6·§7) — 이월이 아니라면
  **과제 자체가 한쪽 처치에 유리했을 가능성**이 남는다는 것이고, 앞으로의 TDD 실험이 쓰는
  과제를 조사하라고 권고한다.

## 초록의 수치를 인용하지 않는다

**이 소스의 초록은 검정 이름과 p값을 본문 표와 다르게 적는다. 확인한 사실은 이렇다.**

- 초록은 `The Kruskal-Wallis tests did not show any significant difference between TDD and
  TLD in terms of testing effort (p-value = .27), external code quality (p-value = .82),
  and developers' productivity (p-value = .83)`라고 적는다.
- 그런데 **처치 비교에 쓰인 검정은 Kruskal-Wallis가 아니라 일표본 부호 검정**이고(§4.9.2),
  그 표(Table 6)의 p값은 1.00 · 0.82 · 0.82다.
- `.27`은 Table 8(이월 효과 K-W)의 TESTS 값이고, **`.83`은 확보본 어느 표에도 없다.**
- **그러므로 이 KB는 이 소스의 수치를 본문 표에서만 가져온다.** 초록의 세 값은 인용하지
  않는다.

## 인용 규약

- **수치는 Table 5~8에서만, 검정 이름과 n을 함께 적는다.**
- **이 논문이 옮긴 남의 수치는 이 논문 경유로 쓰지 않는다** — §2.1의 메타분석 값
  (`TDD improves external quality of 24% …`, `-13%`, `27%`, `7%`)은 Rafique & Mišić의
  것이다.
- **표본이 대학원생이다.** 저자들이 §5.2에서 그것을 외적 타당도 위협으로 적으므로, 이
  결과를 산업 조건으로 옮길 때 그 조건을 함께 적는다.

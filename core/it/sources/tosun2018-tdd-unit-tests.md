---
type: paper-conference
title: "On the Effectiveness of Unit Tests in Test-driven Development"
author:
  - { family: "Tosun", given: "Ayse" }
  - { family: "Ahmed", given: "Muzamil" }
  - { family: "Turhan", given: "Burak" }
  - { family: "Juristo", given: "Natalia" }
issued: "2018"
event-title: "ICSSP'18"
container-title: "Proceedings of the International Conference on Software and System Processes (ICSSP'18)"
publisher: "ACM"
DOI: "10.1145/3202710.3203153"
snapshot: /it/archive/tosun2018-tdd-unit-tests/
snapshot_sha256: "52bdf0dc8c32800231d3d0f8b12ce3e60c32d1fee903edc86a86e02443dcd946"
accessed: "2026-08-24"
---

# tosun2018-tdd-unit-tests

**TDD로 쓴 단위 테스트가 test-last로 쓴 것보다 결함을 더 잘 잡는가를 산업 현장에서 잰
논문.** 답은 **뮤테이션 점수 기준으로 TDD 쪽이 높았다**는 것이고, 저자들이 그것을
`Our findings are different from previous studies conducted at academic settings`라고
스스로 대비시킨다(초록).

**이 소스가 이 KB에서 서는 자리는 TDD 실증의 반대 방향 극이다.** 같은 저자군의
[fucci2017-tdd-dissection](fucci2017-tdd-dissection.md)이 순서 차원의 영향을 찾지 못한
자리에, 이 논문은 다른 결과 변수(단위 테스트의 결함 검출력)로 유의한 차이를 낸다.
**두 결과는 서로를 반박하지 않는다 — 잰 것이 다르고, 아래 "같은 실험에서 나온 두 논문"이
그 관계를 적는다.**

## 지위 — 게재처 정정이 이 소스의 첫 사실이다

- **근거 등급은 `peer-reviewed`다.**
- **게재처는 ICSSP'18이다.** 이 KB의 반입 대장과 REVERIFY 문서가 한동안 `ICSE-SEIP 2018`로
  적고 있었는데 **확보본 문면이 그것을 뒤집는다.** 1쪽의 ACM Reference Format 블록이
  `Proceedings of International Conference on Software and System Processes (ICSSP'18)` ·
  `https://doi.org/10.1145/3202710.3203153`이고, 2쪽부터 전 쪽 러닝 푸터가
  `ICSSP'18, May 2018, Gothenburg, Sweden`이다.
- **확보본은 ACM 최종 조판이 아니라 저자본이다.** 1쪽에
  `This is the author's version of the work. It is posted here for your personal use. Not
  for redistribution. The definitive Version of Record was published in …`이 인쇄돼 있다.
  같은 블록이 `Article 4, 10 pages`라고 적으므로 **논문집 쪽수는 이 판에 없다.**
- 확보본은 pdfTeX 산출물이고 OCR을 거치지 않았다(Producer `pdfTeX-1.40.18`,
  Creator `LaTeX with acmart`). 그래도 이 KB가 인용한 표 수치는 렌더 이미지로 육안
  재확인했다(6·8쪽).

## 표본 — 모집 24명과 분석 n을 가른다

**"산업 전문가 24명"은 모집 인원이고 어느 분석에도 24가 쓰이지 않는다.** 인용할 때 이
구분을 함께 적는다.

- **모집·참여 24명.** 한 대형 조직의 세 사이트에서 자원한 인원이고, TDD 실습 경험이 없는
  개발자들이다(§3 Subjects).
- **§4.1 Dataset Reduction이 넷을 뺀다** — ITLD 과제의 소스 코드에 컴파일·런타임 오류가 있는
  3명, ITLD 과제에 테스트 코드가 없는 1명이다.
- **그래서 분석 n은 이렇게 갈린다.**

  | 분석 | 처치 | n | 위치 |
  |---|---|---|---|
  | 뮤테이션 점수 기술통계 | ITLD | 13 | Table 2 |
  | 뮤테이션 점수 기술통계 | TDD | 18 | Table 2 |
  | 짝지은 비교 | ITLD·TDD 각각 | 10 | Table 3 |

  Table 3의 10명은 **두 과제 모두에서 뮤테이션 점수를 잴 수 있었던 공통 참가자**다.
- **여덟 명분의 테스트 코드를 저자들이 손봤다** — 메서드·생성자 호출을 고쳐 통과시킨 뒤
  Judy를 돌렸다고 §4.1이 적는다.

## 무엇을 어떻게 쟀는가

- **결과 변수는 단위 테스트의 효과성이고, 그 조작적 정의가 뮤테이션 점수(mutation score
  indicator)다**(§3 Variables). 도구는 Judy, 커버리지는 EclEmma다(§3 Instrumentation).
- **처치는 TDD와 ITLD(incremental test-last)다.** 둘 다 잘게 반복하고 차이는 코딩과 테스트의
  순서뿐이라고 §3이 규정한다.
- **검정은 Wilcoxon rank sum, 유의수준 0.05다**(§3 Analysis procedure).
- **과제가 처치마다 다르다** — ITLD는 MarsRover API, TDD는 Bowling Score Keeper다
  (§3 Objects). 게다가 **순서가 고정이다** — 같은 참가자가 ITLD를 먼저 하고 TDD를 나중에
  했다(§5). **처치·과제·순서가 함께 움직이므로 이 세 요인은 이 설계에서 분리되지 않는다.**
  저자들도 §5에서 자기 결과가 선행 연구와 갈리는 이유의 첫 후보로 과제 배정을 든다.

## 같은 실험에서 나온 두 논문

- **이 연구는 새 실험이 아니라 앞선 산업 실험의 데이터에 새 물음을 얹은 것이다.** §3 첫
  문단이 `This study uses data from an experiment conducted with professionals to observe
  the effects of TDD on external quality and productivity [40]. The experimental setup is
  therefore identical to the original experiment`라고 적는다.
- **그 실험의 프로세스 준수 분석이 곧 fucci2017-tdd-dissection이다.** §6 마지막 줄이
  `The detailed findings on process conformance were further discussed in [17]`이고
  참고문헌 [17]이 그 논문이다.
- **그러므로 두 논문은 독립 표본이 아니다.** 이 사실을 적지 않고 둘을 "반대 방향의 증거
  둘"로만 놓으면 실제보다 강한 대비를 만들게 된다.

## 이 판이 안고 있는 내부 불일치

- **§5.1 본문 한 문장이 자기 표와 어긋난다.** `On the contrary, we can see more methods are
  covered by unit tests during TDD`라고 적혀 있으나, Table 4의 MTCov는 ITLD 쪽이 높고
  (평균 79.1 대 61.4) 같은 절 뒷문단과 초록은 **ITLD가 더 많은 메서드를 덮는다**고 적는다.
  **표와 초록 쪽이 맞고 그 한 문장이 오식이다.**
- 표 머리의 흩어짐 지표 이름이 Table 2·3에서는 `Var.`, Table 4에서는 `Variance`인데,
  §4.2 본문은 같은 값을 `standard deviation`이라고 부른다. **이 KB는 그 열의 값을 인용하지
  않는다.**

## 인용 규약

- **수치는 Table 2~5에서만 가져오고 분모(어느 n인지)를 함께 적는다.**
- **이 논문이 옮긴 남의 수치는 이 논문 경유로 쓰지 않는다** — §5의
  `on average 81,90% for TDD and 83,29% for TLD`는 Causevic et al.의 값이다.
- **locator는 절 번호와 표 번호다.** 저자본에 논문집 쪽수가 없다.

---
type: article-journal
title: "Hints on Test Data Selection: Help for the Practicing Programmer"
author:
  - { family: "DeMillo", given: "Richard A." }
  - { family: "Lipton", given: "Richard J." }
  - { family: "Sayward", given: "Frederick G." }
issued: "1978-04"
container-title: "Computer"
volume: "11"
issue: "4"
page: "34-41"
publisher: "IEEE"
snapshot: /it/archive/demillo1978-hints/
snapshot_sha256: "40eb66b7d87c3317d3de0f6a513f7d2804d61371e38198ab3f79a65ebf36c6d2"
accessed: "2026-08-23"
---

# demillo1978-hints

**프로그램 뮤테이션(program mutation)을 실무자용 테스트 데이터 선택 기법으로 내놓은
원전.** 결합 효과(coupling effect)라는 이름과 그 정의가 여기서 나오고, 죽은 뮤턴트와
살아 있는 뮤턴트, 동등 뮤턴트라는 어휘도 여기서 나온다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 어휘의 원전이자 그 어휘가 기댄 가정의
출처다.** 뮤테이션 점수를 스위트 적절성의 눈금으로 쓰는 뒤 문헌이 이 논문의 결합
효과에 기대는데, 이 논문 자신은 그것을 증명하지 않았다고 적는다.

## 지위 — `classic`이자 심사 저널 게재본

- **근거 등급은 `peer-reviewed`이되 성격은 `classic`이다.** IEEE *Computer*에 실린
  글이고 확보본 1쪽 하단에 게재 코드가 인쇄돼 있다 —
  `0018-9162/78/0400-0034$00.75 © 1978 IEEE`. 각 쪽 하단에 `COMPUTER` 또는
  `April 1978`과 인쇄 쪽 번호(34~41)가 찍혀 있어 locator는 인쇄 쪽이다.
- **권과 호는 문면에 없다.** 1쪽 하단 코드가 담은 것은 연도(78)·월(0400)·시작 쪽(0034)
  뿐이다. `volume: 11` · `issue: 4`는 **이 KB가 함께 확보한 Google 논문의 참고문헌
  레코드가 근거**이고(`petrovic2021-google-mutation` 참고문헌 [4]·[30]:
  `Computer, vol. 11, no. 4, pp. 34–41, 1978`), 원문 문면 근거가 아니다.
- **전이 조건이 필요하다.** 대상 언어는 Fortran이고, 뮤테이션 시스템은 예일대와 조지아
  공대에서 만든 대화형 도구이며, 예제는 세 줄에서 수십 줄짜리 서브루틴이다. 이 조건에서
  나온 관찰을 지금 규모의 코드베이스로 옮길 때 무엇이 유지되고 무엇이 깨지는지는 이
  논문이 답하지 않는다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 본문의 Youngs 오류 분포
  (Table 1)나 Figure 1의 테스트 노력 대비 결함 발견 곡선은 각각 박사 논문과 System
  Development Corporation 보고서에서 경유해 온 제3자 값이라 이 KB가 옮기지 않는다.

## 문면 대조로 확인한 것

- **`hypothesis`라는 낱말이 본문에 한 번도 없다.** 확보본 전문 추출본에
  `grep -i hypothesis`를 걸면 0건이고, 어형이 가장 가까운 것은 결론부의
  `hypotheses`(테스트 데이터 선택에 관한 가설 형성) 한 번뿐이다. **널리 쓰이는
  "competent programmer hypothesis"라는 명명은 이 논문의 것이 아니다** — 이 논문에는
  `competent programmers`로 시작하는 서술문이 p.34에 한 번 있을 뿐이다.
- **결합 효과의 정의는 실재한다.** p.35에 들여쓴 정의 블록이 있고 바로 아래
  `There is, of course, no hope of "proving" the coupling effect; it is an empirical
  principle.`이 이어진다.

## 반입 범위

이 런은 인쇄 쪽 34~41 전체를 읽었다. 페이지로 옮긴 것은 결합 효과의 정의와 그 지위,
뮤테이션 절차와 죽은·살아 있는·동등 뮤턴트의 정의, MAX 예제의 적절성 판정, FIND 예제의
살아 있는 뮤턴트 수와 동등 뮤턴트 비율, 고차 뮤턴트 실험, 그리고 결론부의 자기 규정이다.

옮기지 않은 것: Table 1(Youngs 오류 분포)과 Figure 1(테스트 노력 곡선)은 경유 값이고,
삼각형 분류 프로그램의 전체 소스와 Table 3·4, FIND의 Fortran 전문, Table 6~9의 무작위
데이터 실험 세부는 예제 재현 재료라 값만 골라 옮겼다.

## 계보 각주 — 미확보

대장이 지목한 계보 문헌 셋은 이 KB가 확보하지 않았고 **이름만** 남긴다.

- Lipton 1971(뮤테이션 착상의 출발) · Hamlet 1977(같은 시기의 독립 제안) — 둘 다
  이 논문의 참고문헌에도 없다. **2차 경유이고 원문 근거가 없다.**
- Jia & Harman, "An analysis and survey of the development of mutation testing",
  IEEE TSE 37(5), pp. 649–678, 2011 — 서지는 `petrovic2021-google-mutation`의
  참고문헌 [13]·[34]에서 온 **2차 경유**다.

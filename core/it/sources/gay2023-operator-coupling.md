---
type: paper-conference
title: "How Closely are Common Mutation Operators Coupled to Real Faults?"
author:
  - { family: "Gay", given: "Gregory" }
  - { family: "Salahirad", given: "Alireza" }
issued: "2023"
event-title: "ICST 2023: 16th IEEE International Conference on Software Testing, Verification and Validation"
snapshot: /it/archive/gay2023-operator-coupling/
snapshot_sha256: "d2cd4081b2dbdfa90af4dcdaa0ab0d89640b92eccfc81596077c85a2eb53d441"
accessed: "2026-08-23"
---

# gay2023-operator-coupling

**결합 효과(coupling effect)가 실제 결함에서 얼마나 성립하는가**를 뮤턴트 하나하나와
실제 결함 하나하나의 의미 대응으로 잰 논문. 뮤턴트 32,002개와 Defects4J 실결함 144개를
붙여 놓고, 같은 시험이 같은 이유로 깨지는지를 10단 척도로 판정한다.

**이 소스가 이 KB에서 서는 자리는 결합 효과의 성립률 실측이다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위 — 심사를 통과한 실증이되 확보본은 저자본이다

- **근거 등급은 `peer-reviewed`다.**
- **확보본에 게재 줄이 인쇄돼 있지 않다.** 저자 배포본이라 학회명·권·쪽수·DOI 어느
  것도 문면에 없다. 위 frontmatter의 `event-title`은 **원문 문면이 아니라 확보 대장의
  레코드 근거**다(확보 경로는 저자 사이트 `greg4cr.github.io`). 이 묶음의 다른 논문들과
  달리 **묶음 안의 다른 원문이 이 논문의 게재 레코드를 확인해 주지 못한다.**
- **쪽수는 어디에서도 확인되지 않아 적지 않았다.** locator는 확보본 PDF 쪽(1~12)과
  절·표 번호다.
- **본문 동정 근거는 내용이다** — 뮤턴트 32,002개, 연산자 31종, Defects4J 실결함 144개,
  Zenodo 자료 `https://doi.org/10.5281/zenodo.7261554`.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.**

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 3장 A절의 대상, 4장 Table IV·V·VI의 검출률과 결합 등급 분포, Table VII의
  연산자별 중앙값, 4장 D절의 연산자 걸러내기 결과, 5장 타당성 위협.
- 옮기지 않은 것: Table II·III의 연산자 정의와 생성 수 전체, Figure 1~4의 그림 값,
  6장 관련 연구가 전하는 제3자 수치.

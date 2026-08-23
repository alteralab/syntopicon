---
type: paper-conference
title: "A Study of Equivalent and Stubborn Mutation Operators using Human Analysis of Equivalence"
author:
  - { family: "Yao", given: "Xiangjuan" }
  - { family: "Harman", given: "Mark" }
  - { family: "Jia", given: "Yue" }
issued: "2014"
event-title: "ICSE 2014: 36th International Conference on Software Engineering"
publisher: "ACM"
ISBN: "9781450327565"
snapshot: /it/archive/yao2014-equivalent-stubborn/
snapshot_sha256: "28141ef45e11183cba884805b8b28554139d129a422fcd83a350af16d29f7ee0"
accessed: "2026-08-23"
---

# yao2014-equivalent-stubborn

**뮤테이션 점수의 천장을 깎는 동등 뮤턴트(equivalent mutant)가 실제로 얼마나 많고 어느
연산자가 그것을 만드는가**를 사람이 손으로 판정해 잰 논문. 대상은 C 프로그램 18개이고,
판정에 한 저자가 6개월을 전담했다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 점수의 분모가 오염돼 있다는 실측이다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위 — 게재본이고 심사를 통과한 실증이다

- **근거 등급은 `peer-reviewed`다.** 확보본 1쪽 하단 저작권 상자가 게재를 문면으로 확인해
  준다 — `ICSE ’14, May 31 - June 7, 2014, Hyderabad, India` ·
  `Copyright 14 ACM 978-1-4503-2756-5/14/05 ...$15.00.`
- **쪽수는 문면에 인쇄돼 있지 않아 적지 않았다.** locator는 확보본 PDF 쪽(1~12)과 절·표
  번호다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 7절 Table 4가 열거하는 선행
  연구 여덟 편의 동등 뮤턴트 수치는 이 논문이 경유해 전하는 제3자 값이므로 옮기지
  않는다.

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 3.3.1절의 총계(생성 4,181개, 수동 판정 1,230개, 동등 946개, stubborn 284개),
  Table 3의 연산자 클래스별 비율, 4.3절 Figure 5의 동등 원인 분포, 4.4절의 스피어만
  상관, 5절의 실행 권고.
- 옮기지 않은 것: Table 4(선행 연구 비교, 제3자 값), Figure 2·4의 프로그램별·연산자별
  막대, 7절 관련 연구.

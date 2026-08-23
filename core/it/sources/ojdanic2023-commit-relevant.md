---
type: article-journal
title: "Mutation Testing in Evolving Systems: Studying the relevance of mutants to code evolution"
author:
  - { family: "Ojdanić", given: "Milos" }
  - { family: "Soremekun", given: "Ezekiel" }
  - { family: "Degiovanni", given: "Renzo" }
  - { family: "Papadakis", given: "Mike" }
  - { family: "Le Traon", given: "Yves" }
issued: "2023"
container-title: "ACM Transactions on Software Engineering and Methodology"
publisher: "ACM"
DOI: "10.1145/3530786"
snapshot: /it/archive/ojdanic2023-commit-relevant/
snapshot_sha256: "9f033d54826712507628a5dfab7858c5fc63dc5c5124781021311a7179df736d"
accessed: "2026-08-23"
---

# ojdanic2023-commit-relevant

**커밋 하나를 테스트할 때 그 커밋과 관련 있는 뮤턴트가 어디에 있는가**를 잰 논문. 답이
직관을 뒤집는다 — **커밋 관련 뮤턴트의 대부분이 커밋이 바꾼 코드 바깥에 있다.**

**이 소스가 이 KB에서 서는 자리는 변경분 한정 뮤테이션의 사각을 재는 실측이다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위와 동정 — 제목이 비슷한 다른 논문과 갈라야 한다

- **근거 등급은 `peer-reviewed`다.** 확보본 1쪽에 `ACM Trans. Softw. Eng. Methodol.` ·
  `1049-331X/2022/1-ART1` · `https://doi.org/10.1145/3530786`이 인쇄돼 있다.
- **저작권 줄은 `© 2022`이고 러닝 헤드의 쪽 표기는 `1:1`~`1:39`다.** 최종 호에 배정된
  권·호·논문 번호는 이 확보본 문면에 없으므로 frontmatter에 넣지 않았다. locator는 절
  번호와 표·그림 번호다.
- **인용은 반드시 DOI로 못 박는다.** 제목이 더 비슷해 보이는 Ojdanić 외의
  `On the use of commit-relevant mutants`(Empirical Software Engineering 27, 2022)는
  **다른 논문**이고, 이 페이지들이 쓰는 81퍼센트 수치는 그쪽에 없다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.**

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 4절 Table 2의 대상 규모, 5.1.1절 Table 3의 관련 뮤턴트 비율, 5.1.2절
  Figure 7·8의 위치 분포, 5.1.3절 상관, 5.2절 포섭 관련 뮤턴트 비율과 감축률.
- 옮기지 않은 것: 6절 이후의 예측 모형 실험 세부, Figure 6·9~15의 그림 값, 2절의
  정의부를 넘는 선행 연구 서술.

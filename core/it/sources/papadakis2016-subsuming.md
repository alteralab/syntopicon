---
type: paper-conference
title: "Threats to the Validity of Mutation-Based Test Assessment"
author:
  - { family: "Papadakis", given: "Mike" }
  - { family: "Henard", given: "Christopher" }
  - { family: "Harman", given: "Mark" }
  - { family: "Jia", given: "Yue" }
  - { family: "Le Traon", given: "Yves" }
issued: "2016"
event-title: "ISSTA 2016: 25th International Symposium on Software Testing and Analysis"
publisher: "ACM"
DOI: "10.1145/2931037.2931040"
snapshot: /it/archive/papadakis2016-subsuming/
snapshot_sha256: "b461ab2e0bc0b54c631310d6148849407685bf9e735067bd3c317da5d50b698d"
accessed: "2026-08-23"
---

# papadakis2016-subsuming

**뮤테이션 점수로 두 기법을 견주는 실험이 얼마나 자주 틀린 결론을 내는가**를 잰 논문.
대부분의 뮤턴트가 다른 뮤턴트에 포섭된(subsumed) 잉여라서 점수가 부풀고, 그 부풀림이
비교 실험의 제1종 오류(Type I error)로 이어진다는 것이 논지다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 점수 비교 자체의 오류율 실측이다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위 — 심사를 통과한 실증이되 확보본은 저자본이다

- **근거 등급은 `peer-reviewed`다.**
- **확보본에 게재 줄이 인쇄돼 있지 않다.** 저자본이라 학회명·쪽수·DOI 어느 것도 문면에
  없다. 위 frontmatter의 `event-title`과 `DOI`는 **원문 문면이 아니라 레코드 근거**다 —
  같은 묶음의 `papadakis2018-mutation-scores` 참고문헌 [34]가
  `Proceedings of the 25th International Symposium on Software Testing and Analysis,
  ISSTA 2016, Saarbrücken, Germany, July 18-20, 2016. 354–365.
  https://doi.org/10.1145/2931037.2931040`으로 적는다. 확보 경로는 UCL Discovery
  기탁본이다.
- **쪽수는 위 레코드가 354–365로 적지만 확보본 문면에 없어 frontmatter에 넣지 않았다.**
  locator는 절 번호와 표 번호다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.**

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 4.3절 Table 1의 대상, 5.1절 포섭 뮤턴트 비율, 5.2절 부풀림 효과, 5.3절
  Table 2의 상관 범위, 5.4절 제1종 오류율, 5.5절 민감도, 6.1절 문헌 조사 계수.
- 옮기지 않은 것: Algorithm 1의 의사코드, Figure 1·2·3의 그림 세부, Table 2의 전체 값
  (범위와 대표 값만), 2절의 정의 인용을 넘는 선행 연구 서술.

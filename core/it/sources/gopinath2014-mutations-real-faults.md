---
type: paper-conference
title: "Mutations: How close are they to real faults?"
author:
  - { family: "Gopinath", given: "Rahul" }
  - { family: "Jensen", given: "Carlos" }
  - { family: "Groce", given: "Alex" }
issued: "2014"
event-title: "ISSRE 2014: 25th IEEE International Symposium on Software Reliability Engineering"
snapshot: /it/archive/gopinath2014-mutations-real-faults/
snapshot_sha256: "f9f0793eeb85bb35380e5ea27c2b7a69b4b362e4d5790bc3f9bef9b769409547"
accessed: "2026-08-23"
---

# gopinath2014-mutations-real-faults

**유능한 프로그래머 가설(competent programmer hypothesis)이 실제 변경에서 성립하는가**를
깃허브 오픈소스의 변경 이력으로 잰 논문. 언어 넷(C·자바·파이썬·하스켈)의 버그 수정
패치가 실제로 몇 토큰을 건드리는지를 세고, 뮤테이션 연산자가 만드는 한 토큰 변경과
견준다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션의 두 전제 중 하나를 실측으로 흔드는 자리다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

> 이 KB에는 같은 저자·같은 해의 다른 논문 `gopinath2014-suite-evaluation`(ICSE 2014,
> 커버리지 기준 비교)이 이미 있다. **둘은 별개 논문이다.**

## 지위 — 심사를 통과한 실증이되 확보본은 저자본이다

- **근거 등급은 `peer-reviewed`다.**
- **확보본에 게재 줄이 인쇄돼 있지 않다.** 저자 배포본이라 학회명과 쪽수가 문면에 없다.
  위 frontmatter의 `event-title`은 **원문 문면이 아니라 레코드 근거**다 — 같은 묶음의
  `gay2023-operator-coupling` 참고문헌 [9]가
  `25th International Symposium on Software Reliability Engineering, Nov 2014,
  pp. 189–200`으로 적는다. 쪽수는 그 레코드가 189–200으로 적지만 확보본 문면에 없어
  frontmatter에 넣지 않았다. 확보 경로는 저자 사이트 `rahul.gopinath.org`다.
- locator는 확보본 PDF 쪽(1~12)과 절·표 번호다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 2절 관련 연구가 전하는 DeMillo
  1991의 21퍼센트, Daran 1996의 85퍼센트 같은 값은 옮기지 않는다.

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 3절의 대상 수와 분류기 정확도, Table I의 지역 변경·버그 수정 비율,
  4절 Table IV·VII의 토큰 분포, 5절 결과 요약, 6절 논의의 가설 판정.
- 옮기지 않은 것: Table II·III·V의 전체 연산자 분포, Table VIII~XIII의 언어 간 검정
  세부, Figure 2~4의 밀도 그림, 부록 Table XIV~XVI의 수동 분류 세부(대표 값만).

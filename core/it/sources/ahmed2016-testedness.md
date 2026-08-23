---
type: paper-conference
title: "Can Testedness be Effectively Measured?"
author:
  - { family: "Ahmed", given: "Iftekhar" }
  - { family: "Gopinath", given: "Rahul" }
  - { family: "Brindescu", given: "Caius" }
  - { family: "Groce", given: "Alex" }
  - { family: "Jensen", given: "Carlos" }
issued: "2016"
event-title: "FSE 2016: 24th ACM SIGSOFT International Symposium on Foundations of Software Engineering"
publisher: "ACM"
DOI: "10.1145/2950290.2950324"
snapshot: /it/archive/ahmed2016-testedness/
snapshot_sha256: "ae1a47bfa883cbd73b5037cdf912a48946cd397d889390cb52e74a9316867a1c"
accessed: "2026-08-23"
---

# ahmed2016-testedness

**잘 테스트된 코드가 정말 나중에 덜 고쳐지는가**를 기준으로 커버리지와 뮤테이션 점수를
평가한 논문. 종속변수를 뮤턴트 킬이 아니라 **이후에 실제로 일어난 버그 수정**으로 두고,
자바 오픈소스 49개 프로젝트의 변경 이력에서 잰다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 점수의 예측력을 실제 결과로 잰 실측이다.**
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위 — 심사를 통과한 실증이되 확보본은 저자본이다

- **근거 등급은 `peer-reviewed`다.**
- **확보본에 게재 줄이 인쇄돼 있지 않다.** 1쪽 아래에 남은
  `© 2016 ACM. ISBN 978-1-4503-2138-9` · `DOI: 10.1145/1235`는 **ACM 서식 템플릿의
  자리표시 값**이고 이 논문의 실제 식별자가 아니다. 위 frontmatter의 `event-title`과
  `DOI`는 **원문 문면이 아니라 레코드 근거**다 — 같은 묶음의
  `papadakis2018-mutation-scores` 참고문헌 [1]이
  `Proceedings of the 24th ACM SIGSOFT International Symposium on Foundations of
  Software Engineering, FSE 2016, Seattle, WA, USA, November 13-18, 2016. 547–558.
  https://doi.org/10.1145/2950290.2950324`로 적는다.
- **쪽수는 위 레코드가 547–558로 적지만 확보본 문면에 없어 frontmatter에 넣지 않았다.**
  locator는 절 번호와 표 번호다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.**

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 3장의 대상 선별과 분류기 품질(Table 1), 4.1절 Table 2·3의 상관, 4.2절
  Table 4의 커버 여부 대비, 4.3절 Table 5·6·7의 문턱별 대비, 5장 논의의 처방.
- 옮기지 않은 것: Figure 1~5의 산점도 값, 4.4~4.5절 복잡도 분석의 신뢰구간 전체
  (대표만), 2장 관련 연구가 전하는 제3자 수치.

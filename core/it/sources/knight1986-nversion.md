---
type: article-journal
title: "An Experimental Evaluation of the Assumption of Independence in Multi-version Programming"
author:
  - { family: "Knight", given: "John C." }
  - { family: "Leveson", given: "Nancy G." }
issued: "1986"
container-title: "IEEE Transactions on Software Engineering"
snapshot: /it/archive/knight1986-nversion/
snapshot_sha256: "97666f1bc204ef1717d4a0841cdc907291656cd421d28b2d268c0d2f04745742"
accessed: "2026-08-21"
---

# knight1986-nversion

검증자 독립성 축의 고전 원전 — "독립적으로 개발된 판본은 독립적으로 실패한다"는
N-버전 프로그래밍의 기본 가정을 통계 가설 검정으로 반증한 실험 논문이다. 같은 명세로
두 대학에서 27개 판본을 만들고 100만 건의 모의 입력을 돌린 뒤, 독립 실패를 가정한
확률 모형을 99% 신뢰수준에서 기각했다.

**확보본은 저자본(author manuscript)이다.** 게재처 줄이 인쇄돼 있지 않고 쪽번호가
-1-부터 -46-까지 매겨진 이중 행간 타자본이며, 인쇄 저널 쪽번호(96–109)와 대응되지
않는다. 그래서 이 소스를 인용할 때 **locator는 절 번호(§1~§8)와 표 번호(Table 1~4)로
적고 쪽수를 적지 않는다.**

권·호·쪽수는 **같은 저자들이 낸 1990년 reply의 참고문헌 [KNI86]이 근거**다 —
"IEEE Transactions on Software Engineering, Vol. SE-12, No. 1 (January 1986),
pp. 96-109". 확보본 자신의 문면이 아니다.

**저자본과 출판본의 문면이 다르다.** reply가 §2와 §4에서 출판본 결론을 두 번 직인용하는데,
그 인용문이 확보본 §8과 어긋난다.

- 확보본 §8: "the assumption of independence of errors that is fundamental to
  **the analysis** of N-version programming does not hold" /
  reply 인용(출판본): "fundamental to **some analyses** of N-version programming"
- 확보본 §8: "the use of N-version programming in crucial systems, **where failure
  could endanger human lives for example,** should be deferred until further evidence
  is available" / reply 인용(출판본): "…should be deferred until further evidence is
  available **if the reliability analysis of the system has been performed assuming
  independence of failures**"

출판본 문면이 더 좁고 조건이 붙어 있다. **결론 문장을 직인용할 때는 reply가 인용한
출판본 문면을 쓴다** — 확보본은 그보다 넓은 초고다. `knight1990-reply`가 그 문면의
1차 근거다.

판본 길이 수치도 두 문서가 다르다. 확보본 §7은 "327 to 1004 lines"라 적고 reply §3.4는
"310 to 781 lines … average 554 lines (they did not include any I/O statements)"라
적는다. 세는 기준이 다르므로 어느 쪽을 쓰든 **출처를 함께 적는다.**

취득처는 Leveson의 논문 공개 자리(sunnyday.mit.edu)이고 http 전용이다 —
443이 닫혀 있다(2026-08-20 재검증, 2026-08-21 스냅샷).

이 실험의 선행 이론(Eckhardt & Lee)과 후속 일반화(Littlewood & Miller)의 원문은
확보하지 않았다. 이 KB에서 그 둘에 대한 서술은 전부 K&L 두 문서를 통한 전언이다.

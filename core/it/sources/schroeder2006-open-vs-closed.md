---
type: paper-conference
title: "Open Versus Closed: A Cautionary Tale"
author:
  - { family: Schroeder, given: Bianca }
  - { family: Wierman, given: Adam }
  - { family: Harchol-Balter, given: Mor }
issued: "2006-05"
event-title: "3rd Symposium on Networked Systems Design and Implementation (NSDI '06)"
publisher: "USENIX Association"
URL: "https://www.usenix.org/legacy/event/nsdi06/tech/full_papers/schroeder/schroeder.pdf"
snapshot: /it/archive/schroeder2006-open-vs-closed/
snapshot_sha256: "94cd5cc382c172236c739c5b0cea7adc052fabde9806b83eab4edbc135931bac"
accessed: "2026-09-07"
---

# Open Versus Closed: A Cautionary Tale

부하 생성기의 개방(open)·폐쇄(closed) 시스템 모델 선택이 측정 결과와 스케줄링 정책 평가를 뒤집는다는
것을 실측으로 보인 원전. 개방·폐쇄 대기행렬 네트워크 이론 자체(Jackson 1957, Gordon–Newell 1967)가
앞서지만, "어느 모델로 부하를 걸어야 실제 트래픽을 닮는가"라는 부하 테스트 설계 경고의 원전은 이 논문이다.

KB 안의 자리: 부하 테스트 방법론 축의 첫 소스(신설). 2026년 k6(arrival-rate 실행기 = open)·Gatling
(injectOpen/injectClosed) 문서가 이 구분을 전제하며, coordinated omission 논의(Tene, wrk2)의 학술 선행 근거다.

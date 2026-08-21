---
type: paper-conference
title: "Refactoring with Unit Testing: A Match Made in Heaven?"
author:
  - { family: "Vonken", given: "Frens" }
  - { family: "Zaidman", given: "Andy" }
issued: "2012"
event-title: "Working Conference on Reverse Engineering (WCRE)"
URL: "https://azaidman.github.io/publications/vonkenWCRE2012.pdf"
snapshot: /it/archive/vonken2012-refactoring/
snapshot_sha256: "423dab5912ebff733a68221f98d81ae01004e893b95f7eb4a99e690abb0a44dd"
accessed: "2026-08-21"
---

# vonken2012-refactoring

**"단위 테스트가 리팩터링의 안전망"이라는 명제를 통제실험에 건 논문.** 피험자 42명
(최종 학년 학부생 35명 + 현업 개발자 7명)을 실험군(단위 테스트 있음)과 대조군(없음)으로
갈라 리팩터링 과제 7개를 시키고, **소요 시간**과 **결과 생산 코드의 품질 점수**를 쟀다.

이 KB에서 서는 자리는 **보존 오라클의 값어치를 실측으로 되묻는 자리**다. 논문은
Feathers *Working Effectively with Legacy Code*를 참고문헌 [25]로 지목하고 §V-B에서
이렇게 적는다 — *"While theory explains how unit testing makes refactoring easier, e.g.,
Feathers [25], we could not observe this in our experiment, neither in a quicker
refactoring process, nor in higher quality of code."*

## 초록과 §V가 같은 세기로 말하지 않는다 — 이 어긋남이 인용의 핵심이다

- 초록: *"Results indicate that having unit tests available during refactoring does not
  lead to quicker refactoring or to higher-quality code after refactoring."*
- §V-A: 두 귀무가설 각각에 대해 **"neither reject or accept"**라고 적는다 — H10은
  *"due to a lack of information"*, H20은 *"can neither be accepted or rejected"*.

**그러므로 이 소스는 "테스트가 돕지 않는다는 증명"이 아니라 "돕는다는 증거를 찾지
못했다"로만 인용한다.** 이 KB에서 이 논문의 수치를 쓸 때는 §V-A의 문면을 함께 붙이는
것이 의무다.

## 판본 — venue 줄이 인쇄되지 않은 저자본이다

확보본 1쪽에는 제목·저자·소속·이메일만 있고 **학회명·연도·쪽수 줄이 인쇄돼 있지
않다.** 그래서 이 KB는 이 소스의 쪽수를 인용 locator로 쓰지 않고 절 번호(§III-F,
§IV-A)와 표 번호(TABLE II)로만 적는다.

`issued: "2012"`와 `event-title`은 문면이 아니라 **확보 단계 대장이 적은 리포지토리
레코드가 근거다.** 대장은 게재 쪽수를 WCRE 2012 pp.29–38로 적고 있으나 **이 반입 런은
그 레코드를 직접 열어 확인하지 않았다** — 그래서 `page`를 적지 않았고, 쪽수를 쓰려면
그 레코드가 근거임을 함께 적는다.

## 근거 등급

`peer-reviewed`. 이 논문이 스스로 잰 값(표 II–VIII)만 인용한다. §II 관련 연구가
전하는 남의 수치(George & Williams의 18%·16%, Williams et al.의 20.9%·30%)는 이
소스를 경유해 인용하지 않는다 — 원전으로 간다.

## 저자 자신이 적은 한계 — 함께 인용한다

- **대상 코드가 작다.** JPacman은 도메인 클래스 27개·약 3,000줄이고 테스트 스위트는
  약 1,000줄·테스트 케이스 60개(수용 15 + 단위 45)다 (§III-B). 저자는 §V-C 외적
  타당성에서 산업 시스템보다 작다는 것을 스스로 적는다.
- **새 테스트를 쓰라고 요구하지 않았다** — 기존 테스트를 통과 상태로 유지하는 것만
  요구했다 (§III-E). 저자는 §V-A에서 이 지시가 결과를 눌렀을 수 있다고 적는다.
- **H30·H40·H70·H80은 검정 자체가 불가능했다** — 테스트를 가진 피험자의 90% 넘는
  수가 리팩터링 전후로 테스트를 돌려서 비교군이 (대개 비어) 만들어지지 않았다 (§IV-A).
- **표본이 작다**는 것을 §V-C에서 스스로 적는다.

## 텍스트 레이어

`snapshot.py` 판정은 `text_based`(신뢰도 1.00, OCR 필요 0/10쪽)다. 다만 2단 조판이라
표 II–VIII은 기계 추출이 열 머리와 값을 섞는다 — 표의 값을 인용할 때는 본문 산문이
같은 값을 진술하는 자리를 우선했다.

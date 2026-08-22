---
type: paper-conference
title: "Automated Unit Test Improvement using Large Language Models at Meta"
author:
  - { family: "Alshahwan", given: "Nadia" }
  - { family: "Chheda", given: "Jubin" }
  - { family: "Finegenova", given: "Anastasia" }
  - { family: "Gokkaya", given: "Beliz" }
  - { family: "Harman", given: "Mark" }
  - { family: "Harper", given: "Inna" }
  - { family: "Marginean", given: "Alexandru" }
  - { family: "Sengupta", given: "Shubho" }
  - { family: "Wang", given: "Eddy" }
issued: "2024-02-14"
event-title: "FSE '24"
number: "2402.09171"
version: "v1"
DOI: "10.1145/3663529.3663839"
URL: "https://arxiv.org/abs/2402.09171"
snapshot: /it/archive/alshahwan2024-testgen-llm/
snapshot_sha256: "cc86ae6b56e5b7d553341bd2724a234126a1fe543673dcebba2f869cc0d683b5"
accessed: "2026-08-22"
---

# alshahwan2024-testgen-llm

Meta가 만들어 배포한 **TestGen-LLM**의 경험 보고다. 도구의 목표는 테스트를 새로 쓰는 것이
아니라 **사람이 이미 쓴 테스트 클래스를 늘리는 것**이고, 모델이 낸 후보를 사람에게 보내기
전에 결정적 필터 여럿이 순서대로 거른다. 이 KB에서는 **LLM 출력의 수용 조건을 필터로
못박은 산업 규모 실물**로 쓴다.

## 게재 지위 — 심사 게재이되 산업 자기 보고

- **문면이 게재 표면을 인쇄한다.** 1쪽 ACM Reference Format 블록에
  `In Proceedings of the 32nd ACM Symposium on the Foundations of Software Engineering
  (FSE ’24), November 15–19, 2024, Porto de Galinhas, Brazil.`이 있고, 전 쪽 쪽머리는
  `FSE ’24, Mon 15 - Fri 19 July 2024, Porto de Galinhas, Brazil, Brazil`이다.
  **두 줄의 날짜가 서로 어긋난다**(11월 15–19일 대 7월 15–19일). 확보본이 저자본이라
  이 어긋남이 남아 있고, 이 KB는 어느 쪽도 확정 사실로 쓰지 않는다.
- **`Companion`이라는 낱말은 문면에 없다.** 확보본 전문 검색에서 `Companion`은 0회이고
  `industry track`도 0회다. 곧 **FSE 2024 Companion(산업 트랙) 게재라는 사실은 확보본
  문면이 아니라 대장·ACM DL 레코드 근거**이며, 이 페이지의 `DOI`도 같은 근거다 — 문면의
  DOI 자리는 `https://doi.org/XXXXXXX` 자리표시다. **원문 문면으로 위장하지 않는다.**
- **심사를 통과한 문서이되 실증의 성격은 산업 자기 보고다.** 측정 대상은 Meta 내부
  코드베이스이고 모델·데이터·도구가 공개되지 않아 **제3자 재현이 불가능하다.** 그래서
  이 KB는 여기 실린 값을 "Meta가 자기 배포에서 이렇게 셌다"는 형태로만 쓰고, 규모 전제를
  함께 적는다.

## 인용 규칙 — 결과 절만, 그리고 집계 단위를 반드시 붙인다

- **초록과 §1의 값은 옮기지 않는다.** 초록은 `improved 11.5% of all classes`라 적고 §4
  결과 절은 같은 대상을 `approximately 10%`(196/1,979)로 적는다. **어긋나는 자리는 결과
  절 값만 쓴다.** §1의 기여 목록은 `10%`라 적으므로 초록 쪽이 홀로 다르다.
- **집계 단위가 둘이고 절대 섞이지 않는다.**

  | 단위 | 어디서 | 값의 크기 |
  |---|---|---|
  | 테스트 **클래스**(적어도 한 개의 새 테스트가 통과했는가) | §3.3 평가 | 75% · 57% · 25% |
  | 테스트 **케이스 생성 시도**(trial) | §4 배포, Table 3~6 | 0.01~0.07 |

  논문 스스로 각주 4에서 둘의 차이를 적는다 — 한 클래스를 늘리려는 시도 안에 케이스 생성
  시도가 여럿 들어가므로 케이스당 성공률이 훨씬 낮다. **단위를 안 붙인 수치는 인용하지
  않는다.**
- **분모를 함께 적는다.** §3.3 평가의 분모는 Instagram Reels·Stories의 코틀린 컴포넌트
  86개(Stories 31 + Reels 55)이고, §4 배포의 분모는 적용된 테스트 클래스 1,979개다.
  §3.4·§3.4.1의 분모는 diff 수(42건·280건)다.
- **이 논문이 인용한 제3자 수치는 옮기지 않는다.** §6 관련 연구가 드는 Siddiq의 80%·2%,
  Schäfer의 70%, Nie의 29%, Yuan의 약 3분의 1은 전부 남의 논문 값이다 — 원전으로 가서
  확인할 자리이지 이 논문 경유로 박을 값이 아니다.
- **Figure 2(Sankey 다이어그램)는 §3.3 산문이 적는 세 값을 그린 것**이라 그림에서 따로
  읽어 낸 값은 없다.

## 판본과 텍스트 레이어

텍스트 레이어 판정은 `text_based`(신뢰도 1.00, OCR 필요 0/12쪽)라 기계 추출로 읽었다.
다만 Table 1·3~6이 다단 조판이라 기본 추출에서 열 순서가 뒤섞인다 — 표 값은
`pdftotext -layout` 정렬본과 대조해 옮겼다. Figure 1(아키텍처 도해)과 Figure 2(Sankey)는
도형 안 이름표가 흩어져 읽히므로 본문 산문이 적는 것만 옮겼다. 재개점은
`_progress.yaml`이 정본이다.

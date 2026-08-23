---
type: paper-conference
title: "To Mock or Not To Mock? An Empirical Study on Mocking Practices"
author:
  - { family: "Spadini", given: "Davide" }
  - { family: "Aniche", given: "Maurício" }
  - { family: "Bruntink", given: "Magiel" }
  - { family: "Bacchelli", given: "Alberto" }
issued: "2017"
container-title: "2017 IEEE/ACM 14th International Conference on Mining Software Repositories (MSR)"
event-title: "MSR 2017"
DOI: "10.1109/MSR.2017.61"
URL: "https://sback.it/publications/msr2017b.pdf"
snapshot: /it/archive/spadini2017-mocking-practices/
snapshot_sha256: "9cd410962a1f32cb253f5fc68eb07f35266d9d735746374b1f97e3efc0ceb9f7"
accessed: "2026-08-23"
---

# spadini2017-mocking-practices

- [지위 — 이 축의 실측 하나](#지위--이-축의-실측-하나)
- [확보본은 저자본이다](#확보본은-저자본이다)
- [분모가 넷이다 — 섞으면 거짓이 된다](#분모가-넷이다--섞으면-거짓이-된다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [반입 범위](#반입-범위)
- [이 소스가 닿을 자리](#이-소스가-닿을-자리)

**실제 자바 프로젝트의 테스트 코드에서 무엇이 목으로 대체되고 무엇이 대체되지 않는지를
세고, 그 프로젝트의 개발자에게 왜 그랬는지 물은 혼합 방법 실증.** 이 KB가 이것을 들이는
이유는 하나다 — 대역 갈래의 처방들이 전부 실무 규범이거나 경험 보고인데, 그 처방이 현장에서
지켜지는지를 잰 값이 이 소스에 있다.

## 지위 — 이 축의 실측 하나

- **근거 등급은 `peer-reviewed`이고, 이 소스는 실증이다.** 정량(도구로 수집한 의존 전수)과
  정성(면담·설문)을 함께 쓴 혼합 방법이고, 표본·집계 절차·타당성 위협이 문면에 있다.
- **대상은 자바 넷이다** — 오픈소스 셋(Sonarqube · Spring Framework · VRaptor)과 산업 시스템
  하나(Alura). 저자들이 외적 타당성 절에서 그 규모를 스스로 한정한다:

  > Our sample contains four Java systems (one of them closed source), which is small
  > compared to the overall population of software systems that make use of mocking.

- **도구가 잡는 것과 못 잡는 것이 문면에 있다** (§III.C.1) — MOCKEXTRACTOR는 정적 분석이라
  **동적으로 만들어진 목(도우미 클래스에서 생성해 넘기는 목)을 잡지 못하고 그 경우
  "not mocked"로 세어진다.** 저자들은 100개 테스트 단위를 손으로 검사해 그런 사례가 없었다고
  적는다.
- **수동 분류의 일치도가 적혀 있다** (같은 절) — 두 연구자가 서로의 결과 25건씩 총 100건을
  교차 검증했고 7개 범주에 대한 최종 일치도는 **89%**다.

## 확보본은 저자본이다

- **11쪽 PDF이고 venue 줄이 인쇄돼 있지 않다**(스냅샷 판정: text_based, 신뢰도 1.00,
  OCR 필요 0/11쪽). 1쪽에 제목·저자·소속만 있고 학회명도 쪽수도 없다.
- **프론트매터의 `container-title`·`event-title`·`DOI`는 리포지토리 레코드 근거다.**
  이 KB가 함께 들인 Xiao 2024의 참고문헌이 같은 서지를
  `2017 IEEE/ACM 14th International Conference on Mining Software Repositories (MSR), IEEE,
  pp 402–412`와 `https://doi.org/10.1109/MSR.2017.61`로 적는다. **원문 문면으로 위장하지
  않는다** — 권·쪽수를 페이지에 적을 때는 그 사실을 함께 적는다.
- **후속 저널판이 따로 있다.** Xiao 2024의 참고문헌이 같은 저자 넷의 *Mock objects for
  testing Java systems*(EMSE 24(3):1461–1498, 2019)를 별도 항목으로 든다. **그 확장판은
  이 KB에 없다** — 이 소스의 값을 그 확장판의 값으로 옮겨 적지 않는다.
- **그림은 이미지 조판이되 막대 라벨이 텍스트 레이어에 남아 있다.** Fig.2의 백분율과 괄호
  안 원값이 그 라벨이고, 이 KB가 인용하는 자리다.

## 분모가 넷이다 — 섞으면 거짓이 된다

**이 논문에서 "데이터베이스를 얼마나 목하는가"에 답하는 값이 넷이고 전부 다른 것을 센다.**
하나로 뭉치면 이 논문이 하지 않은 주장이 된다.

| 값 | 어디 | 무엇의 비율인가 |
|---|---|---|
| **72%(167) 목 / 28%(64) 비목** | **Fig.2 막대 라벨** | **수동 분석 표본(N=2,178) 안에서 `Database` 범주로 분류된 의존이 목으로 대체된 비율** |
| ~71% | Fig.4 (설문, N=105) | 응답자 가운데 데이터베이스를 "항상 또는 거의 항상" 목한다고 답한 비율 |
| 평균 81% | §V.C 본문 | 데이터베이스 의존이 **자기 테스트 단위 밖에서** 목으로 대체된 비율의 네 프로젝트 평균 |
| 90% | §V.C 본문 | 같은 측정을 Alura 한 프로젝트에서만 낸 값 |

- **이 KB가 인용하는 값은 첫째 줄이고, 인용 자리는 Fig.2다.** 산문 문장이 아니다.
- **프로젝트별 값이 따로 있다** (§IV RQ1 본문) — 데이터베이스에서 Alura와 Sonarqube가
  약 60%, Spring이 94%라고 적힌다. **네 프로젝트를 합친 값 하나로 프로젝트 간 비교를 하지
  않는다.**

## 인용할 때 지킬 것

- **수치를 옮길 때 분모와 그림·절 위치를 함께 적는다.** 위 표가 그 이유다.
- **서론·동기 절의 수치는 인용하지 않는다.** §II.B의 Sonarqube 규모 서술(5,500 클래스 ·
  700k 줄 · 2,034 테스트 단위 · 목 쓰는 652건 · 고유 의존 1,411)은 동기 예시이고 결과가
  아니다. 규모는 결과 절이 참조하는 **표 I**을 쓴다.
- **이 논문이 인용한 남의 수치는 원전으로 간다.** §VI가 옮긴 Mostafa & Wang 2014의
  `23% of the projects`·`Mockito 70%`는 **2차 경유**다 — 이 소스로 그것을 적지 않는다.
- **면담자는 셋이고 설문 응답은 105건이다.** 두 분모를 섞지 않는다. 면담 대상 프로젝트도
  셋뿐이다(Sonarqube 개발자는 면담하지 못했다고 §III.B.4가 적는다).
- **효과 크기 부호에 주의한다.** §V.C의 Cliff's delta 두 값은 텍스트 레이어에서 부호가
  보존되지 않는다. 이 KB는 그 값을 **저자들이 붙인 판정("negligible")**과 함께 크기만 적고
  방향을 주장하지 않는다.
- **언어 모델 시대의 재검이 없다.** 2017년 자바 코드베이스의 관행이고, 생성된 테스트가
  대역을 어떻게 쓰는지는 이 논문의 주제가 아니다.

## 반입 범위

이 런은 확보본 전문 11쪽을 읽었다. 페이지로 옮긴 것은 표본과 집계 절차(§III), Fig.2의 범주별
목 비율과 그 정의(§IV RQ1), 목하는 이유와 목하지 않는 이유(§IV RQ2), 어려움 여섯(§IV RQ3),
Mockito 개발자와의 대조(§V.B), 코드 지표로는 예측되지 않는다는 결과(§V.C), 그리고 타당성
위협(§III.C)이다.

옮기지 않은 것: Mockito 예제 코드(Listing 1 — 개념 설명에 필요한 조각만 인라인 표기),
Fig.1의 연구 방법 도해, Fig.3·Fig.4의 리커트 막대 원값 전부(본문이 요약한 백분율만 옮겼다),
관련 연구(§VI)의 개별 논문 내용이다.

## 이 소스가 닿을 자리

- [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md) —
  이 소스가 세우는 페이지
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — 이 실측이
  어긋나는 처방

---
type: paper-conference
title: "Mock Roles, not Objects"
author:
  - { family: "Freeman", given: "Steve" }
  - { family: "Pryce", given: "Nat" }
  - { family: "Mackinnon", given: "Tim" }
  - { family: "Walnes", given: "Joe" }
issued: "2004"
container-title: "Companion to the 19th annual ACM SIGPLAN conference on Object-oriented programming systems, languages, and applications"
event-title: "OOPSLA '04"
DOI: "10.1145/1028664.1028765"
URL: "http://jmock.org/oopsla2004.pdf"
snapshot: /it/archive/freeman2004-mock-roles/
snapshot_sha256: "8398b7c04848467a36e8b8004809af176707d29736d5feaf972fb74eee3b1318"
accessed: "2026-08-23"
---

# freeman2004-mock-roles

- [지위 — 심사 발표문이되 실증이 아니다](#지위--심사-발표문이되-실증이-아니다)
- [확보본에 인쇄된 것과 인쇄되지 않은 것](#확보본에-인쇄된-것과-인쇄되지-않은-것)
- [저자 순서가 자리마다 다르다](#저자-순서가-자리마다-다르다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [반입 범위](#반입-범위)
- [이 소스가 닿을 자리](#이-소스가-닿을-자리)

**목 객체(Mock Objects)를 테스트 격리 기법이 아니라 설계 발견 기법으로 다시 규정하고,
그 위에 need-driven development라는 이름을 붙인 원전.** 이 KB가 이것을 들이는 이유는
하나다 — "무엇을 목으로 대체할 것인가"에 대한 반대극의 문면이 여기 있고, 그것이 없으면
이 KB가 한쪽 처방을 정설로 오인한다.

## 지위 — 심사 발표문이되 실증이 아니다

- **근거 등급은 `peer-reviewed`다.** 다만 이 등급이 여는 것과 이 문서가 가진 것이 다르다.
  **이 논문에는 측정이 없다.** 실험도 통제군도 표본도 없고, 결과 표가 없다.
- **저자들이 자기 근거를 직접 규정한다** (§4 도입):

  > Between us, the authors have been working with Mock Objects on a wide range of projects
  > for over 5 years. We have also corresponded with other developers who have been using
  > the technique. The longest project was 4 years, and the largest team was 15 developers.
  > We have used it with Java, C#, Ruby, Python, and Javascript, with application scale
  > ranging from enterprise-level to hand-held.

  근거는 **네 저자와 지인들의 프로젝트 경험**이다. 그러므로 이 논문에서 인용할 수 있는 것은
  **주장·정의·지침·자기 규정**이고, 어떤 수치도 아니다. 위 문장의 `over 5 years`·`4 years`·
  `15 developers`는 결과가 아니라 경험의 범위 서술이므로 이 KB는 그것을 **경험 범위**로만
  적고 효과의 크기로 옮기지 않는다.
- **초록이 이 논문의 논지를 한 문장으로 적는다** — **"It turns out to be less interesting as
  a technique for isolating tests from third-party libraries than is widely thought."**
  이 문장이 이 소스가 이 KB에서 하는 일 전부다.
- **선행 논문이 따로 있다.** 이 논문은 Mackinnon·Freeman·Craig의 "Endo-testing: unit testing
  with mock objects"(*Extreme Programming Examined*, 2001, 참고문헌 [10])를 자기 앞판으로
  지목하고 그 뒤의 개정을 적는다. **그 앞 논문은 이 KB에 없다** — 이 소스가 옮긴 문면
  이상으로 그것을 말하지 않는다.

## 확보본에 인쇄된 것과 인쇄되지 않은 것

- **확보본은 11쪽 PDF이고 텍스트 레이어가 온전하다**(스냅샷 판정: text_based, 신뢰도 1.00,
  OCR 필요 0/11쪽). 다만 2단 조판이라 기계 추출본에서 본문과 코드 블록이 서로 끼어든다 —
  **직인용은 문장 단위로 육안 확인한 것만 쓴다.**
- **venue 줄이 원문 근거가 아니다.** 1쪽 각주 자리에 ACM 템플릿의 **자리표시자가 그대로
  남아 있다**:

  > *Conference'04*, Month 1–2, 2004, City, State, Country.
  > Copyright 2004 ACM 1-58113-000-0/00/0004…$5.00.

  그러므로 이 파일 자체는 학회명도 쪽수도 말하지 않는다.
- **프론트매터의 `container-title`·`event-title`·`DOI`는 외부 근거다.** 근거는 이 KB가 함께
  들인 두 심사 논문의 참고문헌이다 — Spadini 2017의 [17]이
  `Companion to the 19th annual ACM SIGPLAN conference … pages 236–246. ACM, 2004`로,
  Xiao 2024가 같은 서지에 `https://doi.org/10.1145/1028664.1028765`를 붙여 적는다.
  **원문 문면으로 위장하지 않는다** — 페이지에서 학회·쪽수를 말할 때는 이 사실을 함께 적는다.
- **그림은 이미지로만 조판돼 있다**(Figure 1~4). 그림에서만 읽히는 것은 옮기지 않았고,
  본문이 말로 다시 적은 만큼만 페이지에 있다.

## 저자 순서가 자리마다 다르다

**세 자리의 표기가 갈린다. 이 KB는 확보본 1쪽 문면을 정본으로 삼는다.**

| 어디 | 순서 |
|---|---|
| **확보본 1쪽(정본)** | **Steve Freeman, Nat Pryce, Tim Mackinnon, Joe Walnes** (ThoughtWorks UK) |
| Spadini 2017 참고문헌 [17] | S. Freeman, T. Mackinnon, N. Pryce, and J. Walnes |
| Xiao 2024 참고문헌 | Freeman S, Mackinnon T, Pryce N, Walnes J |

- **프론트매터 `author`는 확보본 순서다.** 둘째·셋째가 바뀐 인용을 만나도 같은 논문이다.
- 반입 판정 대장의 기재도 확보본 문면과 달랐다 — 이 표가 그 정정이다.

## 인용할 때 지킬 것

- **수치를 인용하지 않는다.** 이 논문에 결과 수치가 없다. 위 "지위" 절의 경험 범위 서술이
  숫자를 가진 유일한 자리이고 그것은 효과의 크기가 아니다.
- **`peer-reviewed`가 이 소스를 실증으로 만들지 않는다.** 이 KB에서 이 소스는 **한쪽 처방의
  원전 문면**으로 인용되고, 그 처방이 실제로 통하는지는 이 소스가 답하지 않는다. 실측은
  [spadini2017-mocking-practices](spadini2017-mocking-practices.md)와
  [xiao2024-mocking-frameworks](xiao2024-mocking-frameworks.md)가 갖는다.
- **논문 안의 인용은 원전으로 간다.** Lean Development(Poppendieck [16])·Law of Demeter
  [15]·Tell, Don't Ask [7]·Self Shunt(Feathers [3])·Responsibility-Driven Design [19]은
  전부 **2차 경유**다. 이름과 이 논문이 옮긴 문면까지만 쓴다.
- **jMock의 API 표기는 2004년 문면이다.** `mock.expect(once()).method("load")` 계열 문법은
  그 시점의 것이고 이 KB는 그것을 현행 사용법으로 옮기지 않는다.
- **"Only Mock Types You Own"은 이 논문 §4.1의 절 제목이다.** 널리 유통되는 변형
  ("Don't mock what you don't own")은 이 문면이 아니다 — 이 KB가 그 변형을 쓰는 자리는
  다른 소스의 곁글 제목이고, **그 소스는 그것을 이 논문에 귀속하지 않는다**(아래 "닿을 자리").
- **2009년 책과 다른 문서다.** 이 KB의 다른 페이지가 지목하는 *Growing Object-Oriented
  Software, Guided by Tests*(Freeman & Pryce, 2009)는 저자가 둘이고 이 논문이 아니다.
  **그 책은 이 KB에 없다.**

## 반입 범위

이 런은 확보본 전문 11쪽을 읽었다. 페이지로 옮긴 것은 기법의 재규정(§1), need-driven
development와 인터페이스 발견(§2), 테스트를 거꾸로 쓰는 절차(§3.6), 실무 지침 아홉(§4),
저자들이 오해라고 부르는 여섯(§5), jMock이 기법을 강제하는 자리(§6), 저자들이 스스로 적은
미해결(§8), 결론(§9)이다.

옮기지 않은 것: TimedCache 워크드 예제의 자바 코드 전문(§3 — 2단 조판에서 코드가 섞여
나오는 구간이라 개념 설명에 필요한 조각만 인라인 표기로 옮겼다), jMock의 API 상세
(§6.1~§6.4의 구문 표), 관련 연구의 도구 비교(§7), 참고문헌 19건의 내용이다.

## 이 소스가 닿을 자리

- [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md) —
  이 소스가 세우는 페이지
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — 모순 상대
- [가짜와 목](../concepts/fakes-versus-mocks.md) — "가진 적 없는 것을 목하지 마라"를 곁글
  제목으로 쓰되 **출처를 적지 않는** 소스. 그 표어의 원문 형태가 이 논문 §4.1이다

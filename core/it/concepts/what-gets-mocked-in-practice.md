---
type: concept
title: 실제 프로젝트에서 무엇이 목으로 대체되는가
description: 대역 갈래의 처방들이 현장에서 지켜지는지를 잰 실증 둘 — 자바 넷의 의존 2,178건을 손으로 분류해 낸 범주별 목 비율과 데이터베이스 72%라는 그림 위치, 개발자가 목하는 이유와 목하지 않는 이유, 결합도와 복잡도로는 목 여부가 예측되지 않는다는 대조, 아파치 자바 193개 프로젝트의 프레임워크 채택률과 목이 촘촘하지 않다는 세 측정, 목 객체의 다수가 자기가 소유하지 않은 라이브러리 클래스를 대체한다는 값, 프레임워크 없이 상속으로 만드는 목, 설문 자기 보고와 채굴값이 크게 어긋난다는 자인, 그리고 저자들이 "무엇을 언제 목할 것인가"를 미해결로 명시한 문면
generated: { by: "claude-opus-5", at: "2026-08-24T06:00:00Z" }
sources:
  - { id: spadini2017-mocking-practices, resource: /it/sources/spadini2017-mocking-practices.md }
  - { id: xiao2024-mocking-frameworks, resource: /it/sources/xiao2024-mocking-frameworks.md }
---

# 실제 프로젝트에서 무엇이 목으로 대체되는가

- [이 페이지의 두 소스와 그 격](#이-페이지의-두-소스와-그-격)
- [수치를 읽기 전에 — 분모가 여럿이다](#수치를-읽기-전에--분모가-여럿이다)
- [무엇이 목으로 대체되는가 (spadini)](#무엇이-목으로-대체되는가-spadini)
- [왜 목하고 왜 목하지 않는가 (spadini)](#왜-목하고-왜-목하지-않는가-spadini)
- [무엇이 어려운가 (spadini)](#무엇이-어려운가-spadini)
- [코드 지표로는 예측되지 않는다 (spadini)](#코드-지표로는-예측되지-않는다-spadini)
- [모킹 프레임워크는 얼마나 쓰이는가 (xiao)](#모킹-프레임워크는-얼마나-쓰이는가-xiao)
- [목은 촘촘하지 않고, 다수가 남의 클래스다 (xiao)](#목은-촘촘하지-않고-다수가-남의-클래스다-xiao)
- [프레임워크 없이 만드는 목 (xiao)](#프레임워크-없이-만드는-목-xiao)
- [사람이 느끼는 것과 코드에 있는 것이 다르다 (xiao)](#사람이-느끼는-것과-코드에-있는-것이-다르다-xiao)
- [저자들이 미해결로 적은 것 (xiao)](#저자들이-미해결로-적은-것-xiao)
- [두 처방과의 대조](#두-처방과의-대조)
- [두 실증의 사각](#두-실증의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **실제 프로젝트의 테스트 코드는 무엇을 목으로 대체하며, 그 관행은 대역 갈래의
처방들과 맞는가.**

여기서 목 객체(mock object)는 두 논문이 쓰는 뜻 그대로다 — 테스트 대역(test double) 가운데
모킹 프레임워크(mocking framework)로 만들어 대상의 의존(dependency)을 대신하는 것이다.
두 논문 다 그 대체 여부를 **테스트 단위 안의 의존 하나하나**를 단위로 센다.

## 이 페이지의 두 소스와 그 격

- **둘 다 근거 등급이 `peer-reviewed`이고, 둘 다 실증이다.** 이 갈래의 다른 페이지들이
  실무 규범(`practitioner-norm`)·에세이(`essay`)·경험 보고인 것과 격이 다르다.
- **그래서 이 페이지가 하는 일이 다르다.** 다른 페이지들은 **무엇을 해야 하는가**를 소유하고,
  이 페이지는 **무엇이 실제로 일어나는가**를 소유한다. **둘을 같은 무게로 인용하지 않는다.**
- **그러나 실증이 처방을 판정하지도 않는다.** 두 논문 어느 쪽도 "목을 이렇게 쓰면 결함이
  줄더라"를 재지 않았다. 잰 것은 **관행의 분포**이고, 관행이 옳다는 증거가 아니다.
  둘째 논문의 저자들이 그 점을 스스로 적는다 — 아래
  [저자들이 미해결로 적은 것](#저자들이-미해결로-적은-것-xiao)이 그 자리다.
- **범위가 자바다.** 두 논문 다 자바 프로젝트만 보고, 둘째 논문은 파서가 Eclipse JDT
  기반이라 언어에 매인다고 §1에서 적는다.[^xiao2024-mocking-frameworks]
- **언어 모델 시대의 재검이 없다.** 첫째는 2017년 코드베이스, 둘째는 2022년 10월 스냅샷이다.
  생성된 테스트가 대역을 어떻게 쓰는지는 두 논문의 주제가 아니다.

## 수치를 읽기 전에 — 분모가 여럿이다

**이 페이지의 값은 전부 다른 것을 센다. 분모를 떼면 두 논문이 하지 않은 주장이 된다.**

| 무엇 | 분모 | 어디 |
|---|---|---|
| 범주별 목 비율 | 손으로 분류한 의존 **2,178건**(넷 프로젝트 표본) | spadini 그림 2 |
| 설문 응답 비율 | 응답자 **105명** | spadini 그림 3·그림 4 |
| 테스트 밖 데이터베이스 목 비율 | 프로젝트별 전수(넷 평균) | spadini §V.C |
| 프레임워크 채택률 | 분석된 아파치 자바 프로젝트 **193개** | xiao §5.1 |
| 프레임워크별 인기 | 프레임워크를 쓰는 **127개** 프로젝트 | xiao 표 3 |
| 라이브러리 클래스 목 비율 | 프로젝트별 목 객체의 비율을 낸 뒤의 **프로젝트 평균** | xiao 표 5a |
| 설문 자기 보고 | 응답자 **17명**(초대 300건, 응답률 5.7%) | xiao §5.6 |

## 무엇이 목으로 대체되는가 (spadini)

- **전체 그림부터 적는다** (§IV RQ1) — 테스트 단위 4,419개 가운데 목 객체를 하나라도 쓰는
  것은 **1,122개(25.39%)**다. 수집한 의존 38,313건 가운데 목으로 대체된 것은
  **2,568건(6.71%)**이고 대체되지 않은 것이 **35,745건(93.29%)**이다.[^spadini2017-mocking-practices]
  - **같은 의존이 자리마다 다르게 다뤄진다** (같은 절) — 고유 의존으로 세면 목 대체가
    938건, 비대체가 11,824건인데 **그 두 집합의 교집합이 650건**이다. 저자들이 그것을
    **"70% of all dependencies mocked at least once"**라고 적는다. 곧 한 번이라도 목으로
    대체된 의존의 열에 일곱은 **다른 테스트에서는 실물로 쓰인다.**[^spadini2017-mocking-practices]
- **범주별 비율이 그림 2의 막대 라벨에 있다.** 산문 문장이 아니다. 손으로 분류한 표본
  **N=2,178**(목 대체 844건 + 비대체 1,334건) 안에서 각 범주의 의존이 목으로 대체된 비율과
  괄호 안 원값이 함께 인쇄돼 있다.[^spadini2017-mocking-practices]

  | 범주 | 목 대체 | 비대체 |
  |---|---|---|
  | Database | **72%(167)** | 28%(64) |
  | Web Service | 69%(182) | 31%(82) |
  | External dependencies | 68%(140) | 32%(67) |
  | Domain object | 36%(319) | 64%(579) |
  | Native Java libraries | 7%(12) | 93%(160) |
  | Test support | 6% | 94%(358) |

  - **괄호 안 값은 의존 건수이고, 범주별 합이 2,178이 되지 않는다** — 해결하지 못한 의존을
    담는 `Unresolved` 범주가 따로 있기 때문이다(§IV RQ1의 범주 정의).[^spadini2017-mocking-practices]
  - **범주 정의가 결과를 정한다** (같은 절) — `Database`는 외부 데이터베이스와 상호작용하는
    클래스이고 **외부 라이브러리(JDBC·Hibernate 등)와 그것에 의존하는 자체 클래스(DAO 구현)
    둘 다**를 포함한다. `Domain object`는 업무 규칙을 담고 외부 자원에 의존하지 않는 클래스다.
    저자들은 `Database`와 `Web Service`가 `External dependency`에 들어갈 수도 있지만 빈도가
    높아 따로 뽑았다고 적는다.[^spadini2017-mocking-practices]
- **프로젝트별로 값이 갈리는 자리도 적혀 있다** (같은 절) — 데이터베이스에서 Alura와
  Sonarqube가 약 60%, Spring이 94%이고, 도메인 객체에서 다른 프로젝트가 약 30%인데
  Sonarqube가 47%다. **넷을 합친 값 하나로 프로젝트를 비교하지 않는다.**[^spadini2017-mocking-practices]
- **저자들이 결론 상자에 적은 문장이 이렇다** (§IV RQ1 상자):[^spadini2017-mocking-practices]

  > Classes that deal with external resources, such as databases and web services are often
  > mocked. Interestingly, there is no clear trend on mocking domain objects.

- **테스트 대상 자신은 목으로 대체되지 않는다** (§V.C) — 약 38,000건의 의존을 자동 분석한
  결과 **어느 프로젝트에서도 테스트 대상 클래스가 목으로 대체된 적이 없다.**[^spadini2017-mocking-practices]

## 왜 목하고 왜 목하지 않는가 (spadini)

면담은 셋(Spring 리드 25년 · VRaptor 개발자 10년 · Alura 리드 5년)이고 설문은 105명이다.
Sonarqube에서는 면담할 개발자를 구하지 못했다고 적혀 있다.[^spadini2017-mocking-practices]

- **구체 구현을 쓰기가 간단하지 않을 때 목한다** (§IV RQ2) — 결합이 심하거나 준비가
  복잡하거나 코드가 복잡하거나 느리거나 외부 자원에 의존하는 클래스가 후보다. 설문에서는
  **결합이 심한 클래스를 항상/거의 항상 목한다는 응답이 48%**, **준비가 어려울 때가 45.5%**
  다(그림 3, N=105).[^spadini2017-mocking-practices]
  - **면담과 설문이 갈리는 자리가 있다** (같은 절) — 면담자들은 느린 클래스를 목 후보로
    들었는데, 설문 응답자의 **50.4%는 느리다는 이유로는 목하지 않는다**고 답했고 복잡하다는
    이유로도 **34.5%**가 목하지 않는다고 답했다.[^spadini2017-mocking-practices]
- **입출력을 온전히 통제할 수 있으면 실물을 쓴다** (같은 절) — D1의 문면이
  **"if given an input [the production class] will always return a single output, we do not
  mock it."**[^spadini2017-mocking-practices]
- **통합 자체를 테스트할 때는 목하지 않는다** (같은 절) — D1이
  **"I do not mock when I want to test the database itself; I wanna make sure that my SQL
  works. Other than that, we mock."**라고 적는다.[^spadini2017-mocking-practices]
- **구현이 아니라 인터페이스를 목한다** (같은 절) — 인터페이스에 구현이 여럿일 수 있으므로
  특정 구현에 기대지 않으려고 그렇게 한다는 것이다. D1이 부수 효과(이메일 발송·HTTP 요청)를
  다룰 때 **그 부수 효과를 표현하는 인터페이스를 만들고 그것을 직접 목한다**고 말한다.[^spadini2017-mocking-practices]
- **도메인 객체는 대체로 목하지 않는다** (같은 절) — 속성과 접근자로 된 평범한 객체라
  만들기 쉽기 때문이고, **복잡하거나 결합이 심하면 목한다**는 예외가 붙는다. D2의 근거가
  다른 결이다 — 그 도메인 객체를 검사하는 자기 테스트가 이미 있으니 다시 검사할 필요가
  없다는 것이다.[^spadini2017-mocking-practices]
- **자바 네이티브 라이브러리는 목하지 않는다** (같은 절) — 값을 담는 것이라 만들기 쉽고,
  `String`처럼 `final`이라 목이 되지 않는 것도 있다. 설문에서도 **82%가 그런 의존을
  전혀/거의 목하지 않는다**고 답했다. 다만 자바 I/O는 예외로 목한다는 면담자 둘이
  있다.[^spadini2017-mocking-practices]
- **데이터베이스·웹 서비스·외부 의존은 목 후보다** (같은 절) — 설문에서 항상/거의 항상
  목한다는 응답이 **웹 서비스 약 82% · 외부 의존 약 79% · 데이터베이스 약 71%**다(그림 4,
  N=105). **이 값은 그림 2의 값과 다른 것을 센다** — 그림 2는 코드에서 센 의존이고 이쪽은
  사람이 답한 빈도다.[^spadini2017-mocking-practices]

## 무엇이 어려운가 (spadini)

§IV RQ3의 어려움 목록이 이 페이지에서 처방 쪽과 가장 많이 닿는 자리다.

- **결합** — 목이 테스트와 프로덕션 코드의 결합을 **늘린다**는 것이 응답에 그대로 있다.
  반대 방향의 결합 문제도 있다 — 프로덕션 코드가 제대로 분리돼 있지 않으면
  **"mocking is difficult (if not impossible)"**이라는 것이다.[^spadini2017-mocking-practices]
- **불안정한 의존** — **목의 동작을 원 클래스의 동작과 맞게 유지하는 것**이 가장 큰 문제로
  꼽힌다. 프로덕션 클래스가 자주 바뀌면 목이 불안정해지고 따라서 자주 고쳐야 한다.[^spadini2017-mocking-practices]
- **목이 설계 문제를 가린다** — 면담자 셋이 **같은 예**를 들었다고 적혀 있다:[^spadini2017-mocking-practices]

  > when you have to test class A, and you notice that it has 10/15 dependencies, you can
  > mock it. However, you are hiding a problem: a class with 15 dependencies is probably a
  > smell in the code.

  - D3의 진술이 더 세다 — **"I always try to use as less mocks as possible, since in my
    opinion they hide the real problem. Furthermore, I do not remember a single case in
    which I found a bug using mocks."**[^spadini2017-mocking-practices]
  - 설문 응답자의 문면도 같은 결이다 — **"You are always guessing that what you mock will
    work (and keep working) that way when using the real objects."**[^spadini2017-mocking-practices]
- **레거시** — 잘 분리되지 않은 시스템에서는 **"mocking is the only way to perform some
  testing"**이라는 응답과, 그런 시스템에서 한 단위를 테스트하려면 **거의 시스템 전체를
  목해야 한다**는 응답이 함께 있다.[^spadini2017-mocking-practices]
- **도구 쪽 판정도 같은 방향이다** (§V.B) — 저자들이 Mockito의 주요 개발자와 대조했는데,
  결합 문제에 대해 도구가 도울 수 없고 **프로덕션 클래스에서 고쳐야 한다**고 답한다:
  **"When a developer has to mock a lot of dependencies just to test a single unit, he can
  do it! However, it is a big red flag that the unit under test is not well designed."**
  정적 메서드 목하기를 지원하지 않는 이유도 **"If we do it, we allow developers to write bad
  code."**라고 적힌다.[^spadini2017-mocking-practices]

## 코드 지표로는 예측되지 않는다 (spadini)

- **결합도와 복잡도로 목 여부를 가르려는 시도가 실패한다** (§V.C) — 클래스를 목 대체 비율
  50%를 기준으로 두 무리로 나눈 뒤 결합도(CBO)와 맥케이브 복잡도를 비교했다.
  - **결합도** — 목 대체 쪽 평균 5.89(최대 51), 비대체 쪽 평균 7.131(최대 187).
  - **복잡도** — 목 대체 쪽 평균 10.58(최대 89.00), 비대체 쪽 평균 16.42(최대 420).
  - **두 경우 다 저자들의 판정이 `negligible`이다**(윌콕슨 순위합 검정, 신뢰수준 95% ·
    효과 크기 Cliff's delta). **효과 크기 두 값은 확보본 텍스트 레이어에서 부호가 보존되지
    않으므로 이 KB는 크기만 적고 방향을 주장하지 않는다** — 0.121과 0.166이다.[^spadini2017-mocking-practices]
- **저자들의 결론이 이것이다** (같은 절):[^spadini2017-mocking-practices]

  > We conjecture that the chosen code metrics are not enough to predict whether a class
  > should be mocked.

  - **이 결과가 이 페이지에서 가장 조용히 중요한 자리다.** 면담자들이 "결합이 심하고 복잡한
    것을 목한다"고 말했는데, 같은 프로젝트의 코드에서는 그 말이 지표로 확인되지 않는다.
    **자기 보고와 코드가 갈리는 첫째 사례이고, 둘째 사례가 아래
    [사람이 느끼는 것과 코드에 있는 것이 다르다](#사람이-느끼는-것과-코드에-있는-것이-다르다-xiao)
    에 있다.**

## 모킹 프레임워크는 얼마나 쓰이는가 (xiao)

- **분석된 프로젝트는 193개다.** 아파치 자바 프로젝트 246개에서 시작해 git 저장소가 연결되지
  않은 33개와 JUnit을 임포트하지 않아 테스트가 없는 4개를 빼고(§4.1), 설정 문제로 임포트에
  실패한 16개를 더 뺀 수다(§8). **모든 백분율의 분모가 246이 아니라 193이다.**[^xiao2024-mocking-frameworks]
- **그 가운데 127개(66%)가 모킹 프레임워크를 하나 이상 쓴다** (§5.1).[^xiao2024-mocking-frameworks]
- **프레임워크별 프로젝트 수는 표 3에 있다**(분모 127) — Mockito 98 · EasyMock 36 ·
  PowerMock 16 · jMock 11 · 그 밖 34. **둘 이상을 쓰는 프로젝트가 47개(37%)**다.[^xiao2024-mocking-frameworks]
  - **이 KB는 표 3의 `%Projects` 열을 인용하지 않는다** — Mockito 행이 `74%`인데 같은 절
    본문은 같은 값을 `77%`로 적어 두 값이 어긋난다. 원값 `98/127`을 쓴다. 어긋남의 상세는
    [소스 메타](../sources/xiao2024-mocking-frameworks.md)가 정본이다.
- **프로젝트 성질이 채택을 가른다** (§5.1 RQ1.2) — 규모로는 큰 프로젝트 88% · 중간 65% ·
  작은 프로젝트 34%가 프레임워크를 쓴다. 연식으로는 2010년 이후 시작 73% · 2005~2010년
  63% · 2005년 이전 46%다. 영역으로는 `Development & Testing` 50% · `Networking & IoT` 72% ·
  `Web Technologies` 73% · `Data Management` 83%다.[^xiao2024-mocking-frameworks]
  - **저자들이 마지막 값을 RQ2와 연결한다** (같은 절) — HTTP 서비스와 데이터베이스 같은
    외부 의존이 목으로 대체될 가능성이 높다는 결과와 맞는다는 것이다.[^xiao2024-mocking-frameworks]

## 목은 촘촘하지 않고, 다수가 남의 클래스다 (xiao)

- **촘촘함을 세 가지로 잰다** (§5.2 RQ2.1) — 프로젝트의 **70%**에서 목을 쓰는 테스트 파일이
  전체 테스트 파일의 10% 미만이고, **65%**에서 목으로 대체된 의존이 전체 의존의 5~15%이며,
  **53%**에서 목 관련 작업을 한 개발자가 10명 미만이다(프로젝트에 개발자가 수백 명일 수
  있는데도).[^xiao2024-mocking-frameworks]
- **한 파일 안의 목 개수도 적다** (표 4) — 목을 쓰는 테스트 파일의 **58.5%가 목 객체를 셋
  이하**로 만들고 **13.4%가 열 개 이상**을 만든다. 대체된 의존 수로 보면 **36.7%가 하나**뿐이고
  **6.5%가 열 개를 넘는다.**[^xiao2024-mocking-frameworks]
- **그리고 목 객체의 다수가 남의 클래스를 대체한다** (§5.2 RQ2.2 · 표 5a) — 프로젝트별로
  낸 뒤 평균한 값이 **61.1%**이고, 중앙값 65.2% · 최대 100% · 최소 0%다. 프로젝트당 목으로
  대체된 라이브러리 클래스 수는 평균 25.4개 · 중앙값 9개 · 최대 622개다. 저자들이 결론
  상자에 **"tend to mock more library classes (61.1%) than the classes in their own package
  (38.9%)"**라고 적는다.[^xiao2024-mocking-frameworks]
- **가장 많이 목으로 대체되는 라이브러리 클래스가 표 5b에 있다**(빈도 순, 값은 등장
  횟수):[^xiao2024-mocking-frameworks]

  | 클래스 | 빈도 |
  |---|---|
  | `javax.servlet.http.HttpServletRequest` | 503 |
  | `javax.servlet.http.HttpServletResponse` | 299 |
  | `org.osgi.framework.Bundle` | 134 |
  | `javax.servlet.ServletContext` | 114 |
  | `java.util.Map` | 100 |
  | `java.io.File` | 97 |
  | `com.google.inject.Injector` | 96 |

  - **이 표가 이 페이지에서 처방과 가장 세게 부딪히는 값이다.** 아래
    [두 처방과의 대조](#두-처방과의-대조)가 그 자리다.
- **저자들의 해석은 동기 쪽이다** (같은 절) — 목록이 HTTP 요청·응답, 데이터베이스, 입출력과
  파일 시스템에 몰려 있으므로, 아파치 개발자가 프레임워크를 쓰는 주된 동기는 **외부
  라이브러리의 간섭을 막는 것**과 **실제 서버·데이터베이스·파일 시스템에 접근하지 않아
  테스트가 빨라지는 것**이라는 것이다.[^xiao2024-mocking-frameworks]
- **첫째 논문과 이 값을 나란히 놓을 때 주의할 것이 있다.** 첫째 논문의 `Native Java
  libraries`는 자바 표준 라이브러리만 담는 좁은 범주이고(그래서 7%), 이 논문의
  `library class`는 **프로젝트 자기 패키지 밖의 클래스 전부**다(그래서 `javax.servlet`·
  Guice·OSGi가 든다). **두 값은 어긋나는 것이 아니라 다른 것을 센다.** 첫째 논문에서 같은
  자리에 놓이는 것은 `External dependencies` 68%와 `Web Service` 69%다.

## 프레임워크 없이 만드는 목 (xiao)

- **193개 가운데 143개 프로젝트가 프레임워크를 쓰지 않는 "맞춤 목 클래스"를 갖고 있고,
  그 총수가 2,237개다** (§5.5 RQ5).[^xiao2024-mocking-frameworks]
- **그 방식의 다수가 상속이다** (같은 절 · §5.6 SQ9) — 표본 44건 가운데 **40건**이
  테스트 전용 하위 클래스를 만드는 방식(인터페이스 구현·추상 메서드 구현·메서드 재정의)
  이다. 설문에서도 응답자의 33%가 프레임워크 밖의 방법을 썼다고 답했고, 그들이 든 방법이
  **완전히 새 클래스를 만드는 것**과 **테스트 전용 하위 클래스**였다.[^xiao2024-mocking-frameworks]
- **저자들이 그것을 준최적으로 규정하되 원인을 프레임워크 쪽에도 둔다** (§5.5 결론 상자) —
  프레임워크의 한계와 사례의 복잡성 때문에 프레임워크로 상속을 대체하는 것이 늘 가능하지는
  않고, **어떤 상황에서 그런지를 이해하려면 더 많은 연구가 필요하다**는 것이다.[^xiao2024-mocking-frameworks]
- **응답자가 지목한 프레임워크의 한계 셋도 적혀 있다** (§5.6 SQ10) — 빌더 패턴처럼 복잡한
  객체 구조를 목으로 만들기 어렵다는 것, `mockito-inline`으로도 정적 메서드와 생성자 목이
  여전히 어렵다는 것, 그리고 **유지 보수가 매우 어렵다**는 것이다.[^xiao2024-mocking-frameworks]
- **"목"이라는 낱말이 테스트 의존 격리와 무관하게 쓰이는 경우도 발견됐다** (§5.5 결론 상자
  2번) — 저자들은 그것을 **실무에서 이 낱말의 해석이 갈린다는 신호**로 읽고 체계적 조사가
  필요하다고 적는다.[^xiao2024-mocking-frameworks]

## 사람이 느끼는 것과 코드에 있는 것이 다르다 (xiao)

- **설문의 분모가 17이다** (§5.6) — 초대 300건에 응답 17건, 응답률 **5.7%**. 저자들이
  낮은 응답률을 스스로 적고 선행 연구를 들어 대표성을 주장한다. **이 KB는 그 분모를 떼고
  설문 백분율을 쓰지 않는다.**[^xiao2024-mocking-frameworks]
- **자기 보고가 채굴값보다 훨씬 크다** (같은 절) — 응답자들은 목을 쓰는 테스트 파일 비율을
  평균 55%(범위 18~76%), 목으로 대체된 의존 비율을 평균 44%(범위 9~75%)로 답했다.
  **같은 두 값을 저장소에서 채굴하면 각각 10%와 11%다.**[^xiao2024-mocking-frameworks]
- **저자들의 해석이 두 겹이다** (§5.6 · §7) — 목을 촘촘히 쓰는 개발자가 설문에 응할 가능성이
  높다는 참여자 편향이 하나이고, 다른 하나가 이것이다 — **"it is possible that developers
  may perceive more intensive mocking than reality."**[^xiao2024-mocking-frameworks]
- **여러 프레임워크 사용에서도 같은 방향의 어긋남이 나온다** (같은 절) — 응답자의 88.2%가
  여러 프레임워크를 함께 쓴 적이 있다고 답했는데 채굴값은 37%다.[^xiao2024-mocking-frameworks]
- **그래서 이 페이지의 실증 둘이 같은 모양의 관찰을 갖는다** — 첫째 논문은 면담자의 진술이
  코드 지표로 확인되지 않는다는 것을, 둘째 논문은 자기 보고가 채굴값의 다섯 배라는 것을
  적는다. **목에 관한 진술은 관행의 증거가 아니다.**

## 저자들이 미해결로 적은 것 (xiao)

**이 항목이 이 페이지가 이 KB에 서는 이유의 절반이다.** 2024년 심사 논문이 "무엇을 언제
목할 것인가"를 **풀린 문제로 다루지 않는다.**

- **초록이 그렇게 적는다**:[^xiao2024-mocking-frameworks]

  > Second, mocking is overall practiced quite selectively in software projects—not all test
  > files use mocking, nor all dependencies of a test target are mocked. It calls for more
  > future research to gain a more systematic understanding of when and what to mock to
  > provide formal guidance to practitioners.

- **RQ2의 결론 상자가 같은 말을 더 넓게 적는다** (§5.2) — **"It remains open research
  regarding when, where, and who should use mocking in testing practice."** **누가**까지
  미해결에 든다.[^xiao2024-mocking-frameworks]
- **함의 절이 필요한 것을 지목한다** (§7) — **"More empirical knowledge regarding which
  types of dependencies should or should not be mocked could facilitate the practice of
  mocking for practitioners."**[^xiao2024-mocking-frameworks]
- **결론도 같다** (§10) — **"More research is needed to investigate when and what to mock in
  software testing, and by whom."**[^xiao2024-mocking-frameworks]
- **그리고 그것이 비어 있다고 말할 근거를 저자들이 갖고 있다** — 이 논문은 선행 채굴 연구와
  자기 결과를 §6에서 한 항목씩 대조한 뒤 그 절 안에서도 같은 문장을 적는다:
  **"It remains open research regarding the context of when and where mocking should be
  used in testing practice."**[^xiao2024-mocking-frameworks]

## 두 처방과의 대조

**이 KB의 대역 갈래에는 서로 모순하는 처방 둘이 서 있다. 이 페이지의 실측은 어느 쪽도
지지하지 않고, 두 처방이 공통으로 지키라고 한 것마저 어긋난다.**

| 처방 | 어느 페이지 | 이 페이지의 실측 |
|---|---|---|
| 데이터베이스는 managed 의존이므로 **실물을 쓴다** | [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md) | **어긋난다** — 표본 안 `Database` 의존의 **72%**가 목으로 대체된다(spadini 그림 2) |
| 시스템 안 클래스 사이의 통신은 구현 세부이므로 **목하지 않는다** | 같은 페이지 | **부분적으로 어긋난다** — `Domain object` 의존의 **36%**가 목으로 대체된다(같은 그림). 저자들은 이것을 "뚜렷한 경향 없음"으로 읽는다 |
| 목은 **통합 테스트에만** 둔다 | 같은 페이지 | **잴 수 없다** — 두 논문 다 테스트의 종류를 가르지 않는다. 둘째 논문은 JUnit 임포트로 테스트 파일을 식별하므로 통합 테스트가 섞인다고 §8에서 자인한다 |
| 목이 가장 유용한 자리는 **시스템 안쪽**이다 | [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md) | **어긋난다** — 아파치 목 객체의 **평균 61.1%**가 자기 패키지 **밖**의 라이브러리 클래스를 대체한다(xiao 표 5a) |
| **소유한 타입만 목한다**(두 처방의 공통 지반) | 위 두 페이지 | **가장 크게 어긋난다** — 가장 많이 목으로 대체되는 클래스가 `javax.servlet.http.HttpServletRequest`(503회)이고 목록에 `java.util.Map`(100회)과 `java.io.File`(97회)이 든다(xiao 표 5b) |

- **마지막 줄이 이 표에서 가장 강한 발견이다.** 논쟁하는 두 소스가 **유일하게 합의하는
  지침**이 "소유한 타입만 목하라"인데, 실측된 관행은 그것을 정면으로 어긴다. 어느 쪽 처방이
  옳은지와 무관하게 **현장이 두 처방 어느 쪽도 따르지 않는다**는 뜻이다.
- **다만 이 대조가 처방을 반증하지는 않는다.** 두 실증은 **관행의 분포**를 재었을 뿐,
  그렇게 만든 테스트가 더 자주 깨지는지도 결함을 더 놓치는지도 재지 않았다. **"많이
  한다"는 "옳다"가 아니고 "틀렸다"도 아니다.**
- **개발자 자신의 진술은 오히려 처방 쪽에 가깝다.** 첫째 논문의 면담자 셋이 **목이 설계
  문제를 가린다**고 말하고 Mockito 개발자도 같은 판정을 내린다. **그 진술과 같은 프로젝트의
  코드가 갈린다는 것이 이 페이지의 반복되는 모양이다.**
- **표 첫 줄의 처방이 "실물"로 무엇을 요구하는지는 이 페이지가 소유하지 않는다.**
  [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md)이
  그 자리이고, 거기서 실물이 **같은 엔진**으로 좁혀진다. **그러면 이 페이지의 어긋남은
  더 커진다** — 두 논문 다 **목으로 대체됐는지만** 셌고, 목이 아닌 대역(인메모리 공급자·
  다른 데이터베이스)으로 바꿔친 경우는 어느 칸에도 세어지지 않았다. 곧 위 72%는
  **같은 엔진을 쓰지 않은 비율의 하한**이지 그 값이 아니다. #hypothesis 그 값을 잰 자료는
  이 KB에 없다.

## 두 실증의 사각

- **효과를 재지 않았다.** 두 논문 어느 쪽도 목 사용과 결함 검출·유지 비용·리팩터링 내성의
  관계를 재지 않는다. 이 갈래의 처방들이 주장하는 것은 전부 **효과**이므로, 이 페이지의
  값으로는 그 주장을 판정할 수 없다.
- **표본이 좁다.** 첫째는 자바 넷(하나는 비공개)이고, 저자들이 외적 타당성 절에서 그것을
  스스로 한정한다. 둘째는 아파치 자바 193개로 넓지만 **아파치 한 생태계**이고, 저자들이
  §6.1에서 아파치 프로젝트가 깃허브 프로젝트보다 크고 오래됐다는 것을 수치로 보인다.
- **도구가 놓치는 것이 있다.** 첫째 논문의 정적 분석은 도우미 클래스에서 만들어 넘기는 목을
  잡지 못하고 그것을 "비대체"로 센다(§III.C.1). 둘째 논문은 JUnit 임포트로 테스트 파일을
  고르므로 통합 테스트와 목 생성용 유틸리티 파일이 섞인다(§8).
- **범주 분류가 사람 판단이다.** 첫째 논문의 7개 범주는 두 연구자의 수동 분류이고 최종
  일치도가 **89%**(교차 검증 100건)다. **자동화할 수 없어서 그렇게 했다고 저자들이 적는다.**[^spadini2017-mocking-practices]
- **두 논문의 범주가 서로 맞물리지 않는다.** 위
  [목은 촘촘하지 않고](#목은-촘촘하지-않고-다수가-남의-클래스다-xiao)의 마지막 항목이 그
  자리다. 두 값을 같은 표에 놓으려면 정의를 먼저 맞춰야 한다.
- **시점이 다르다.** 2017년과 2022년(코드 스냅샷) 사이에 아홉 해가 있고, 둘째 논문 스스로
  선행 연구와의 차이를 **시간 차의 결과일 수 있다**고 §6.2에서 적는다.
- **언어 모델 시대의 재검이 없다.** 위 [이 페이지의 두 소스와 그 격](#이-페이지의-두-소스와-그-격)이
  정본이다.

## 이어지는 페이지

- [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md) — 이 실측이 어긋나는 처방
  한쪽. **데이터베이스를 목으로 바꾸지 말라는 판정이 그 페이지의 중심이고, 이 페이지의
  그림 2가 반대 방향을 가리킨다**
- [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md) — 어긋나는
  처방 다른 쪽. **두 처방이 서로 모순하면서도 "소유한 타입만 목하라"에서는 합의하는데,
  이 페이지의 표 5b가 그 합의마저 어긴다**
- [대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md) — 두 처방이 서 있는
  지형과 그 이름. 그 글의 저자가 판정을 유보한 자리에 이 페이지가 **판정 대신 분포**를 놓는다
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) — 같은 물음에
  대규모 조직의 선호 순서로 답한 자리. 그쪽이 실물을 먼저 쓰라고 하고 이 페이지는 외부
  자원 의존에서 그 순서가 실제로는 뒤집혀 있음을 보인다
- [가짜와 목](../concepts/fakes-versus-mocks.md) — 목 대신 가짜를 쓰라는 다른 처방. 이 페이지의 둘째
  논문이 **프레임워크 없이 상속으로 만드는 목**을 세는데, 그것이 그 페이지가 말하는 가짜와
  같은 것인지는 두 소스가 답하지 않는다
- [리팩터링 내성과 거짓 양성](resistance-to-refactoring-and-false-positives.md) — 처방들이
  주장하는 **효과**의 이름. 이 페이지의 두 논문이 재지 않은 것이 정확히 그것이다
- [인메모리 데이터베이스 대역이 잃는 것](what-in-memory-database-doubles-lose.md) — 위 표
  첫 줄의 처방이 요구하는 "실물"의 뜻. **그쪽이 실물을 같은 엔진으로 좁히므로 이 페이지의
  어긋남은 그만큼 더 커진다** — 두 논문은 목 대체만 셌고 목이 아닌 대역은 세지 않았다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 작은 테스트를
  성립시키는 대역 이야기가 거기 걸려 있다

[^spadini2017-mocking-practices]: Spadini, Aniche, Bruntink & Bacchelli, "To Mock or Not To
    Mock? An Empirical Study on Mocking Practices", 2017, 확보본 11쪽 저자본. **venue 줄이
    인쇄돼 있지 않아 MSR 2017 pp.402–412 · doi 10.1109/MSR.2017.61은 리포지토리 레코드
    근거다.** 쪽 번호가 아니라 절 번호가 locator다 — §III "Research Methodology"(§III.A
    표본 · §III.B 수집과 분석 · §III.C 타당성 위협) · §IV "Results"(RQ1 그림 2 · RQ2
    그림 3·그림 4 · RQ3) · §V "Discussion"(§V.B Mockito 개발자 대조 · §V.C 정량 채굴) ·
    §VII "Conclusion". **그림 2의 값은 막대 라벨이고 산문 문장이 아니다.** 직인용은 확보본
    문면 그대로다. Listing 1의 Mockito 예제는 개념 설명에 필요한 조각만 인라인 표기로
    옮겼다. 분모 넷이 서로 다르다는 것과 인용 규약은
    [소스 메타](../sources/spadini2017-mocking-practices.md)가 정본이다.

[^xiao2024-mocking-frameworks]: Xiao, Zhao, Wang, Li, Lim, Wei, Yu & Wang, "An empirical
    study on the usage of mocking frameworks in Apache software foundation", *Empirical
    Software Engineering* 29:39, 2024, 확보본 53쪽 출판본(CC BY 4.0, doi
    10.1007/s10664-023-10410-y). **같은 리포지토리에 수치가 다른 11쪽 초기 투고본이 따로
    있으며 이 페이지의 값은 전부 53쪽 출판본에서 확인한 것이다.** locator는 절 번호와 표
    번호다 — §4.1 표본 · §5.1 RQ1(표 3) · §5.2 RQ2(표 4 · 표 5a · 표 5b) · §5.5 RQ5 ·
    §5.6 설문 · §6 선행 연구 대조 · §7 함의 · §8 한계 · §10 결론. 직인용은 확보본 문면
    그대로다. 표 3의 백분율 열과 상위 세 프레임워크 합산 비율은 논문 안에서 값이 어긋나
    인용하지 않았고, 프레임워크 이름의 오식(`Mockit`·`Mocito`·`PowerMocknig`)은 정규
    표기로 적었다. 그림은 이미지 조판이라 본문이 말로 옮긴 값만 인용했다. 분모 셋(246·193·
    17)의 구분과 인용 규약은 [소스 메타](../sources/xiao2024-mocking-frameworks.md)가
    정본이다.

---
type: webpage
title: "Mocks Aren't Stubs"
author:
  - { family: "Fowler", given: "Martin" }
issued: "2007-01-02"
container-title: "martinfowler.com"
URL: "https://martinfowler.com/articles/mocksArentStubs.html"
snapshot: /it/archive/fowler2007-mocks-arent-stubs/
snapshot_sha256: "dc80ead97d83ed8e4e482c2b60cc7c375476123b958ca281bfc65ca744c38d93"
accessed: "2026-08-20"
---

# fowler2007-mocks-arent-stubs

**테스트 대역(test double)을 부르는 말을 다섯으로 갈라 놓고, 그 위에서 검증 방식의 구분
(상태 검증 대 행위 검증)과 TDD 스타일의 구분(클래시컬 대 모키스트)이 서로 다른 두 구분임을
분리해 낸 실무자 에세이.** 이 KB가 이것을 들이는 이유는 하나다 — 대역 어휘와 그 위의
스타일 논쟁을 이후 문헌들이 이 글의 낱말로 말하기 때문이다.

## 지위 — 실무자 에세이이지 실증이 아니다

- **근거 등급은 `essay`다.** 실험도 표본도 측정도 없다. 수치가 한 개도 없고, 논거의 재료는
  두 스타일의 실천자들과 나눈 대화와 저자 자신의 관찰이다.
- **글 자신이 자기를 에세이로 규정한다** — 어휘를 고르는 대목에서 문면 그대로
  **"since it's my essay I get to pick which words to use"**(§The Difference Between Mocks
  and Stubs)라고 적는다. 그래서 이 소스는 "학술 근거"로 인용되지 않는다.
- **저자가 판정을 명시적으로 유보한다.** 마지막 절이 그 자리이고, 유보의 근거로 자신의
  경험 부족을 스스로 든다 — **"I also suffer from the disadvantage of not trying mockist
  TDD on anything more than toys"**(§So should I be a classicist or a mockist?). 그러므로
  이 글은 논쟁의 판정문이 아니라 논쟁의 지도로 인용한다.
- **이 글이 만든 것과 이 글이 옮긴 것이 다르다.** 아래 "누구의 낱말인가"가 정본이다.

## 누구의 낱말인가 — 이 글이 지은 말과 옮긴 말

이 소스를 "용어 창시자"로 뭉뚱그리면 세 겹이 섞인다. 문면이 셋을 각각 밝혀 둔다.

| 낱말 | 누구 것인가 | 문면 근거 |
|---|---|---|
| classical / mockist (TDD 스타일) | **이 글의 저자가 여기서 지었다** | "a whole different philosophy … which I term here as the classical and mockist styles of Test Driven Development" |
| mock object | **이 글 밖 — XP 공동체** | "I first came across the term “mock object” a few years ago in the Extreme Programming (XP) community" |
| Test Double · dummy · fake · stub · spy · mock 5분류 | **이 글 밖 — Meszaros** | "I'm going to follow the vocabulary of Gerard Meszaros's book … Meszaros then defined five particular kinds of double" |
| System Under Test (SUT) | **이 글 밖 — Meszaros** | "Following Meszaros I'll use System Under Test, or rather the abbreviation SUT" |
| Detroit / London (스타일의 별칭) | **이 글 밖 — 남들이 쓰는 말로 보고** | "You sometimes see “Detroit” style used for “classical” and “London” for “mockist”" |
| Test Spy (행위 검증을 하는 스텁) | **이 글 밖 — Meszaros** | "Meszaros refers to stubs that use behavior verification as a Test Spy" |

**그러므로 이 글에 귀속할 수 있는 창안은 두 구분을 갈라 놓은 것과 그 둘의 이름뿐이다.**
5분류를 이 글의 창안으로 적으면 오귀속이다.

## 판과 열람일 — 갱신 이력이 문면 안에 있다

- **본문 말미 「Significant Revisions」가 두 줄이고, 그것이 이 글의 전체 갱신 이력이다.**
  - **"02 January 2007: Split the original distinction of state-based versus
    interaction-based testing into two: state versus behavior verification and classic
    versus mockist TDD. I also made various vocabulary changes to bring it into line with
    Gerard Meszaros's book of xunit patterns."**
  - **"08 July 2004: First published"**
- **머리글의 날짜도 같다** — 제목 아래에 `02 January 2007`이 인쇄돼 있고, 페이지가 심은
  `og:article:modified_time`도 `2007-01-02`다. `issued`를 2007-01-02로 적은 근거가 이
  둘이고, 2004-07-08은 최초 발행일이다.
- **이 소스에 대해 확보본이 보증하는 사실은 여기까지다.** "이 글이 오래 갱신되지 않았다"는
  서술을 쓸 때는 반드시 **이 두 날짜만**을 근거로 삼고, 그 이상(저자가 뒤에 생각을 바꿨는지,
  다른 자리에서 갱신했는지)은 이 소스로 말하지 않는다.
- 살아 있는 페이지이므로 열람일을 남긴다. 웹에서 받은 날은 **2026-08-20**(`accessed`),
  그 파일을 이 KB의 아카이브로 옮긴 날은 **2026-08-23**이다. `snapshot_sha256`이 그 파일의
  동일성을 담보한다.
- **현행판과 대조하지 않았다.** 확보된 스냅샷 한 벌만 쓴다. 이 소스가 보증하는 것은 그
  파일의 문면 하나뿐이다.

## 인용할 때 지킬 것

- **수치가 없다.** 이 글에는 인용할 측정값이 존재하지 않는다. 이 소스에 기대어 수치를 적는
  일은 어떤 경우에도 오인용이다. 양적 표현으로 보이는 유일한 것도 어림 규칙이고
  (클러스터는 `no more than half a dozen`), 근거가 붙어 있지 않다.
- **"Don't mock what you don't own"은 이 글에 없다.** 스냅샷 전문 검색으로 확인했다 —
  `own`은 `on your own`·`your own mind up` 같은 자리에서만 나오고, 저 표어도 그 변형
  (`Only Mock Types You Own`)도 문면에 없다. 그 표어를 이 소스에 귀속하지 않는다.
- **"I don't think I'm the right person to judge" 류의 문장도 이 글에 없다.**
  `right person`은 이메일 테스트 예시(`sent to the right person`) 안에서만 나온다. 저자의
  유보를 인용할 때는 위 "지위" 절에 옮긴 실제 문면을 쓴다.
- **글 안의 인용은 원전으로 간다.** 이 글이 가리키는 Meszaros의 xUnit 패턴 책, Freeman &
  Pryce의 OOPSLA 논문, Beck의 책, Daniel Terhorst-North의 BDD 소개는 전부 **2차 경유**다.
  이름과 이 글이 옮긴 문면까지만 쓴다.
- **도구 이름과 코드는 2007년 문면이다.** jMock·EasyMock·nMock의 API 표기는 그 시점의
  것이고, 이 KB는 그것을 현행 사용법으로 옮기지 않는다.
- **언어 모델 시대의 재검이 없다.** 생성된 테스트가 대역을 어떻게 쓰는지는 이 글의 주제가
  아니다.

## 반입 범위

이 런은 확보본 전문(본문 열두 절 전부와 Further Reading·Significant Revisions)을 읽었다.
페이지로 옮긴 것은 두 구분의 분리, 대역 5분류와 그 귀속, 상태 검증과 행위 검증의 기제,
클래시컬과 모키스트의 정의, 다섯 축의 대조(TDD 진행 방식·픽스처·테스트 격리·구현 결합·설계
스타일), 저자의 유보와 그 근거, 그리고 이 글이 스타일과 무관하게 요구하는 것 하나다.

옮기지 않은 것: 자바 예제 코드 전문(jMock·EasyMock 두 벌 — 개념 설명에 필요한 조각만
인라인 표기로 옮겼다), 사이트 내비게이션, Further Reading의 링크 대상 내용이다.

## 이 소스가 닿을 자리

- [대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md) —
  이 소스가 세우는 페이지

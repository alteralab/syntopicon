---
type: book
title: "Unit Testing: Principles, Practices, and Patterns"
author:
  - { family: "Khorikov", given: "Vladimir" }
issued: "2020"
publisher: "Manning Publications"
edition: "MEAP V03"
snapshot: /it/archive/khorikov2020-unit-testing/
snapshot_sha256: "d264c046be6a5c3452b19cb4ff898cbceec45b5e1830d0406a95f20afa5e0092"
accessed: "2026-08-23"
---

# khorikov2020-unit-testing

- [지위 — 실무 규범이지 실증이 아니다](#지위--실무-규범이지-실증이-아니다)
- [판 — 확보본은 MEAP V03이다](#판--확보본은-meap-v03이다)
- [참고문헌의 상태 — 목록은 없고 각주는 있다](#참고문헌의-상태--목록은-없고-각주는-있다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [용어 — 이 소스의 표기와 이 KB의 표기](#용어--이-소스의-표기와-이-kb의-표기)
- [반입 범위](#반입-범위)
- [이 소스가 닿을 자리](#이-소스가-닿을-자리)

**좋은 단위 테스트를 네 속성의 곱으로 정의하고, 그 가운데 리팩터링 내성(resistance to
refactoring) 하나만은 협상 불가로 못 박은 뒤, 거기서 "무엇을 목(mock)으로 대체할 것인가"를
연역해 내는 실무 규범서.** 이 KB가 이것을 들이는 이유는 대역 논쟁을 "어느 학파가 옳은가"가
아니라 **깨지는 테스트가 무엇을 부수는가**로 다시 놓기 때문이다.

## 지위 — 실무 규범이지 실증이 아니다

- **근거 등급은 `practitioner-norm`이다.** 실험도 표본도 측정도 없다. 이 책 전체에 인용할
  수 있는 측정값이 없고, 논거의 재료는 저자의 현장 경험과 정의로부터의 추론이다.
- **저자의 자기 규정은 "정밀하고 과학적인 정의"다** (1장 §1.1 "The current state of unit
  testing"): **"This book takes you there. It teaches a precise, scientific definition of
  the ideal unit test."** 같은 문장이 MEAP 머리글(Welcome)에도 어순만 바꿔 실려 있다
  (**"It teaches a scientific, precise definition of the ideal unit test."**). **"과학적"이라는 낱말은 정의의
  성격을 가리키는 말이지 측정을 가리키는 말이 아니다** — 이 책에는 그 정의를 검증한 실험이
  없다.
- **"제1원리"라는 낱말은 이 확보본에 한 번 나오고, 그 자리는 책 전체의 방법 선언이 아니다**
  (11장 도입): **"Most of these topics follow from the first principles described in
  part 2."** 4부의 반패턴들이 2부의 원칙에서 따라 나온다는 국소적 진술이다. **확보본
  전문 검색에서 "이 책을 제1원리에서 연역했다"는 꼴의 선언 문면은 찾지 못했다.**
  그러므로 이 소스의 지위를 적을 때는 위 두 문면(1장의 "정밀하고 과학적인 정의", 11장의
  "2부의 제1원리에서 따라 나온다")만 근거로 쓴다.
- **`practitioner-norm`의 의무**: 이 소스를 "학술 근거"로 쓰지 않는다. 조항에 실을 때는
  저자의 자기 규정을 함께 인용해 지위를 밝힌다.

## 판 — 확보본은 MEAP V03이다

**확보본은 Manning의 조기 접근판(Manning Early Access Program, MEAP) 3판이지 최종
인쇄판이 아니다.** 이것은 이 소스를 인용할 때 가장 먼저 알아야 할 사실이다.

- 표지 파일이 `MEAP VERSION 3`을 인쇄한다. EPUB 패키지 메타의 제목도
  **"Unit Testing: Principles, Practices, and Patterns MEAP V03"**이다.
- **판권면이 없다.** 그래서 확보본 문면에는 **ISBN도 발행 연도도 없다.** frontmatter의
  `issued: "2020"`은 최종 인쇄판의 발행 연도로 반입 판정 대장이 기재한 값이고,
  **확보본 문면에서 확인된 값이 아니다.** ISBN은 확인할 수 없어 적지 않았다.
  EPUB 패키지가 심은 제작 타임스탬프는 `2019-10-15`다.
- **본문은 1~11장 전부와 4부 도비라를 담고 있다.** 브리프 목차(`Brief Table of Contents`)와
  실제 파일이 일치한다. 결락 장은 없다.
- **MEAP의 흔적이 본문에 남아 있다.** 판 표지 문자열 `V03`이 팁·곁글 성격의 한 줄 문장
  **열다섯 곳** 앞에 그대로 달라붙어 있다(예: 5장 §5.1.3의 `V03Asserting interactions
  with stubs…`, 8장 §8.2.1의 `V03Use real instances of managed dependencies…`). 원문
  HTML에서도 그 문자열이 문단 텍스트 안에 있다. **직인용에서는 이 `V03` 접두를 조판
  장치로 보고 떼어 냈다** — 문장 자체는 원문 그대로다.
- **MEAP이므로 최종판과 문면이 다를 수 있다.** 이 KB가 보증하는 것은 이 스냅샷 한 벌의
  문면뿐이다. **최종 인쇄판과 대조하지 않았다.**

## 참고문헌의 상태 — 목록은 없고 각주는 있다

대장의 판정은 "책에 참고문헌이 물리적으로 없다"였다. **확보본 실측 결과 그 판정은 절반만
참이다.**

- **참고문헌 목록(bibliography·references)도 색인(index)도 없다.** 브리프 목차에도 없고,
  본문 밖 파일에도 없다.
- **그러나 본문에 번호 각주 형식의 출처 지시가 있다.** 확보본에서 확인한 것:
  - 5장 각주 `[2]`: **"See xUnit Test Patterns: Refactoring Test Code (Addison-Wesley,
    2007)."** — 대역 5분류의 귀속.
  - 9장 각주 `[5]`: **"See page 69 in Growing Object-Oriented Software, Guided by Tests
    by Steve Freeman and Nat Pryce (Addison-Wesley Professional, 2009)."** — 쪽 번호까지
    적은 지시다.
  - 9장 각주 `[6]`: **"See Domain-Driven Design: Tackling Complexity in the Heart of
    Software by Eric Evans (Addison-Wesley, 2003)."**
- **본문 안의 문헌 추천도 여럿이다** — 2장이 Beck의 *Test-Driven Development: By Example*,
  Freeman & Pryce의 *Growing Object-Oriented Software, Guided by Tests*, van Deursen &
  Seemann의 *Dependency Injection*을 이름과 출판사·연도까지 적어 추천하고, 8장이 GOOS의
  로깅 구분(support/diagnostic logging)을 가져다 쓴다.
- **그러므로 "출처 없이 쓴 책"이라고 적으면 틀린다.** 없는 것은 **목록**이고, 있는 것은
  **본문 안의 지목**이다. 다만 그 지목들은 전부 실증 문헌이 아니라 실무서다 — 이 책의
  등급이 `practitioner-norm`인 이유는 목록의 부재가 아니라 **측정의 부재**다.

## 인용할 때 지킬 것

- **수치가 없다.** 이 책에는 인용할 측정값이 존재하지 않는다. 이 소스에 기대어 비율이나
  효과 크기를 적는 일은 어떤 경우에도 오인용이다. 양적으로 보이는 표현(네 속성의 값을
  `[0..1]`로 놓고 곱한다는 서술)은 **비유이지 계산이 아니다** — 저자 자신이
  **"it's impossible to measure these attributes precisely"**라고 적는다(4장 §4.4).
- **locator는 장·절 제목이다.** EPUB에 인쇄판 쪽 앵커가 없다. 확인 절차와 근거는
  `it/archive/khorikov2020-unit-testing/_progress.yaml` 머리말이 정본이다.
- **책 안의 인용은 원전으로 간다.** Meszaros의 대역 5분류, Freeman & Pryce의
  "Only mock types that you own", Cockburn의 육각형 아키텍처(hexagonal architecture),
  Evans의 안티커럽션 계층, Fowler의 tell-don't-ask는 전부 **2차 경유**다. 이름과 이 책이
  옮긴 문면까지만 쓴다.
- **코드는 전부 C#이고 목 라이브러리는 Moq다.** 저자가 그것을 밝힌다
  (**"the mocking library of my choice"**). 이 KB는 API 표기를 다른 언어·도구로 옮기지
  않는다.
- **언어 모델 시대의 재검이 없다.** 생성된 테스트가 이 네 속성에서 어디에 서는지는 이
  책의 주제가 아니다. 이 책의 판정은 **경험 법칙의 지위**로 인용한다.

## 용어 — 이 소스의 표기와 이 KB의 표기

| 이 소스의 표기 | 이 KB의 표기 | 왜 |
|---|---|---|
| resistance to refactoring | 리팩터링 내성(resistance to refactoring) | 뜻이 자명하고 이 KB의 `refactoring` 계열 페이지와 낱말이 맞는다 |
| false positive / false negative | 거짓 양성(false positive) / 거짓 음성(false negative) | 통계 확립 역어 |
| observable behavior / implementation details | 관찰 가능한 행위(observable behavior) / 구현 세부(implementation details) | 확립 역어 |
| managed / unmanaged dependency | **원어 유지** — managed 의존(managed dependency) · unmanaged 의존(unmanaged dependency) | "관리/비관리"로 옮기면 판정 기준이 이름에서 사라진다. 이 책의 판정 기준은 소유나 관리가 아니라 **외부에서 관찰되는가**다(8장 §8.2.1) |
| classical school / London school | 고전 학파(classical school) / 런던 학파(London school) | 이 책이 쓰는 이름 그대로 |
| mockist | **쓰지 않는다** | 이 책이 그 낱말을 의도적으로 피한다(2장 곁글) — 아래 참조 |

**`mockist`를 피하는 것이 이 책의 명시적 선택이다** (2장 곁글 "The classical and London
schools of unit testing"): **"Although the term mockist is widespread, people who adhere
to this style of unit testing generally don't like it, so I call it the London style
throughout this book."** 이 KB의
[대역 어휘와 두 TDD 스타일](../concepts/test-double-vocabulary-and-tdd-styles.md)이 쓰는
음차 클래시컬·모키스트가 그 이름의 출처이고, 그쪽 문면에도 같은 사실(구분 자체를 싫어하는
쪽이 있다)이 적혀 있다. **두 페이지의 이름이 다른 것은 소스가 다른 이름을 쓰기 때문이지
가리키는 것이 달라서가 아니다.**

## 반입 범위

읽고 옮긴 범위와 읽지 않은 범위의 정본은
`it/archive/khorikov2020-unit-testing/_progress.yaml`이다. 소스 메타의 산문은 정본이
아니다.

## 이 소스가 닿을 자리

- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md)
  — 네 속성과 그 가운데 하나만 협상 불가인 이유
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — 그 판정에서
  연역되는 대역 사용 기준

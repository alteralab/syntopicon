---
type: concept
title: 클린 코드의 발견법 목록
description: 이 책의 규칙 전체를 식별자 붙은 목록으로 압축한 17장 — 목록이 어떻게 만들어졌는지에 대한 저자의 서술, 일곱 갈래 예순여섯 항목의 지도, 파울러의 냄새 목록과 겹치는 자리와 갈라지는 자리, 목록이 규칙이 아니라 가치 체계를 함의한다는 저자의 맺음, 그리고 이 목록에서 오늘날 통용되지 않는 항목들
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: martin2008, resource: /it/sources/martin2008.md }
---

# 클린 코드의 발견법 목록

- [이 목록이 만들어진 방식](#이-목록이-만들어진-방식)
- [일곱 갈래](#일곱-갈래)
- [General이 목록의 본체다](#general이-목록의-본체다)
- [파울러의 냄새 목록과 겹치는 자리](#파울러의-냄새-목록과-겹치는-자리)
- [파울러 쪽에 없는 것](#파울러-쪽에-없는-것)
- [목록이 함의하는 것 — 저자의 맺음](#목록이-함의하는-것--저자의-맺음)
- [오늘날 통용되지 않는 항목들](#오늘날-통용되지-않는-항목들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **이 책의 규칙 전체는 어떤 목록이며, 그 목록의 지위는 무엇인가.**

> **이 페이지의 소스는 논쟁 중인 소스다.** 반입 지위와 그 근거는
> [소스 메타](../sources/martin2008.md)가 정본이다. 이 페이지는 목록의 **지도**이고,
> 논쟁이 걸린 항목의 전문은 [작은 함수](small-functions.md)와
> [주석은 실패다](comments-as-failure.md)에 있다.

## 이 목록이 만들어진 방식

- 저자의 서술 (17장 도입, p.286):[^martin2008]

> I compiled this list by walking through several different programs and refactoring
> them. As I made each change, I asked myself *why* I made that change and then wrote the
> reason down here. The result is a rather long list of things that smell bad to me when
> I read code.

  - **"나에게 나쁜 냄새가 나는 것들의 목록"** — 저자 자신이 목록의 지위를 개인의 판단으로
    규정한다. 이 KB가 이 소스를 논쟁 중인 소스로 다루는 근거 하나가 이 자기 진술이다.
- 사용법도 명시된다 — **이 목록은 위에서 아래로 읽도록, 그리고 참조용으로도 쓰도록
  의도됐다** (17장 도입, p.286).[^martin2008] 각 항목의 상호 참조는 부록 C에 있다.
- **본문 곳곳이 이 식별자로 서로를 부른다.** 3장이 `[G34]`를, 6장이 `[G36]`·`[G34][G6]`를
  부르는 식이다. 즉 이 목록은 부록이 아니라 **책의 색인 체계**다.

## 일곱 갈래

| 갈래 | 식별자 | 개수 | 무엇 |
|---|---|---|---|
| Comments | `C1`–`C5` | 5 | 부적절한 정보·낡은 주석·중복 주석·못 쓴 주석·주석 처리된 코드 |
| Environment | `E1`–`E2` | 2 | 빌드가 한 단계여야 한다·테스트가 한 단계여야 한다 |
| Functions | `F1`–`F4` | 4 | 인수 과다·출력 인수·플래그 인수·죽은 함수 |
| General | `G1`–`G36` | 36 | 목록의 본체 |
| Java | `J1`–`J3` | 3 | 와일드카드 임포트·상수 상속 금지·상수 대신 열거형 |
| Names | `N1`–`N7` | 7 | 서술적 이름·적절한 추상 수준·표준 명명·모호하지 않은 이름·범위에 비례하는 길이·인코딩 회피·부수 효과를 이름에 |
| Tests | `T1`–`T9` | 9 | 불충분한 테스트·커버리지 도구·사소한 테스트·무시된 테스트·경계 조건·버그 주변·실패 패턴·커버리지 패턴·속도 |

- `E1`·`E2`가 조문 형태다 — **프로젝트를 빌드하는 것은 한 번의 사소한 조작이어야 한다**
  (17장 `E1`, p.287)[^martin2008], **모든 단위 테스트를 명령 하나로 돌릴 수 있어야 한다.
  … 모든 테스트를 돌릴 수 있다는 것은 너무나 근본적이고 중요해서 그것이 빠르고 쉽고
  뻔해야 한다** (17장 `E2`, p.287).[^martin2008]

## General이 목록의 본체다

전부를 옮기지 않고, 이 KB의 다른 페이지와 맞닿는 것들만 든다.

- `G5` **Duplication** — **이것은 이 책에서 가장 중요한 규칙 중 하나이고 당신은 그것을
  아주 진지하게 받아들여야 한다** (17장 `G5`, p.289).[^martin2008] 중복의 세 층위가
  구분된다 — 똑같은 코드 덩어리(메서드로), 되풀이되는 `switch`/`if-else` 연쇄(다형성으로),
  **비슷한 알고리즘이되 비슷한 코드 줄을 공유하지 않는 모듈**(TEMPLATE METHOD나 STRATEGY로)
  (17장 `G5`, p.290).[^martin2008] 전문과 그 최대주의의 대비는 [DRY 원칙](dry-principle.md)에.
- `G6` **Code at Wrong Level of Abstraction** — **당신은 잘못 놓인 추상에서 거짓말을 하거나
  얼렁뚱땅 빠져나갈 수 없다. 추상을 분리해 내는 것은 소프트웨어 개발자가 하는 가장 어려운
  일 중 하나이고, 틀렸을 때 빠른 해결책이란 없다** (17장 `G6`, p.291).[^martin2008]
  `Stack` 인터페이스의 `percentFull()`이 예다. 같은 물음의 다른 소스는
  [계층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md).
- `G8` **Too Much Information** — **잘 정의된 모듈은 아주 작은 인터페이스를 가져 적은
  것으로 많은 일을 하게 한다. … 클래스의 메서드가 적을수록 좋다. 함수가 아는 변수가
  적을수록 좋다. 클래스의 인스턴스 변수가 적을수록 좋다** (17장 `G8`,
  pp.291–292).[^martin2008]
  - **이 항목만 떼어 놓으면 [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)과
    같은 말이다.** 두 소스가 인터페이스를 좁히라는 데는 합의한다. 갈리는 것은 **좁히는
    수단이 쪼개기인가**다 — 그 대질은 [작은 함수](small-functions.md)의 모순 절에 있다.
- `G11` **Inconsistency** — **어떤 것을 어떤 방식으로 한다면 비슷한 모든 것을 같은
  방식으로 하라. 이것은 최소 놀람의 원칙으로 돌아간다** (17장 `G11`,
  p.292).[^martin2008] 같은 축은 [코드의 일관성](consistency-in-code.md).
- `G14` **Feature Envy** — 파울러의 냄새를 그대로 가져오되 **때때로 기능 편애는 필요악**
  이라는 예외를 붙인다. 보고서 형식 문자열을 `HourlyEmployee`로 옮기면 **객체 지향 설계의
  여러 원칙을 어긴다**는 것이 근거다 (17장 `G14`, p.294).[^martin2008]
- `G19` **Use Explanatory Variables** — **과하게 하기는 어렵다. 설명 변수는 적은 것보다
  많은 것이 대체로 낫다** (17장 `G19`, p.296).[^martin2008]
- `G20` **Function Names Should Say What They Do** — **함수가 무엇을 하는지 알기 위해
  구현(또는 문서)을 봐야 한다면, 더 나은 이름을 찾거나 더 나은 이름을 가진 함수에 넣을 수
  있도록 기능을 재배치하는 일에 힘써야 한다** (17장 `G20`, p.297).[^martin2008]
  - **"또는 문서를"이라는 삽입구가 이 KB의 모순 축과 직결된다** — 문서를 봐야 하는 것
    자체를 결함으로 세우므로 [주석은 실패다](comments-as-failure.md)의 조문이 여기
    되풀이된다.
- `G21` **Understand the Algorithm** — **함수를 다 했다고 여기기 전에 그것이 어떻게
  동작하는지 **이해**하고 있는지 확인하라. 모든 테스트를 통과하는 것으로 충분하지 않다**
  (17장 `G21`, p.298).[^martin2008] 저자가 각주에서 구분을 둔다 — **알고리즘이 요구되는
  일을 할지 확신하지 못하는 것은 흔히 삶의 사실이다. 당신 코드가 무엇을 하는지 확신하지
  못하는 것은 그저 게으름이다** (17장 `G21` 각주 10, p.298).[^martin2008]
- `G25` **Replace Magic Numbers with Named Constants** — **조문에 예외가 명시적으로
  붙는다.** `feetWalked/5280.0`·`hourlyRate * 8`·`radius * Math.PI * 2`를 놓고 **정말
  `FEET_PER_MILE`·`WORK_HOURS_PER_DAY`·`TWO` 상수가 필요한가? 분명히 마지막 경우는
  터무니없다** (17장 `G25`, p.300).[^martin2008] 그리고 매직 넘버는 숫자만이 아니라
  **자기 서술적이지 않은 값을 가진 어떤 토큰에도 적용된다** — 테스트의 `"John Doe"`가 예다
  (17장 `G25`, p.300).[^martin2008]
- `G30` **Functions Should Do One Thing** · `G34` **Functions Should Descend Only One
  Level of Abstraction** — 3장의 두 규칙이 식별자로 다시 실린 것이다. `G34`에 저자의
  실측이 하나 붙는다 — 추상 수준을 가르는 리팩터링을 하다가 **미묘한 오류를 잡았다.
  원래 코드는 XHTML 표준이 요구하는 닫는 슬래시를 `HR` 태그에 넣지 않았다** (17장 `G34`,
  p.305).[^martin2008] 그리고 — **함수를 추상의 선을 따라 쪼갤 때, 이전 구조에 가려져
  있던 새로운 추상의 선을 발견하는 일이 흔하다** (17장 `G34`, p.306).[^martin2008]
- `G35` **Keep Configurable Data at High Levels** — 기본값·설정값을 저수준 함수에 묻지
  말고 고수준에서 인수로 내려보내라 (17장 `G35`, p.306).[^martin2008] 같은 축은
  [외부 설정](external-configuration.md).

## 파울러의 냄새 목록과 겹치는 자리

이 KB에는 이미 fowler2018의 냄새 어휘 스물넷이
[코드의 나쁜 냄새](code-smells.md)로 들어와 있다. **두 목록은 독립적으로 만들어졌고 크게
겹친다.** 이 소스가 상대를 인용하는 자리가 둘 있다 — `G14` Feature Envy를 **마틴 파울러의
코드 냄새 중 하나**라고 명시하고 (17장 `G14`, p.293)[^martin2008], 6장 각주에서 잡종
구조를 **[Refactoring]의 Feature Envy라 불리기도 한다**고 적는다 (6장 각주 4,
p.99).[^martin2008]

| 이 소스 | 파울러 쪽 냄새 |
|---|---|
| `F1` Too Many Arguments | Long Parameter List |
| `G5` Duplication | Duplicated Code |
| `G9` Dead Code | (파울러 쪽은 Speculative Generality·Lazy Element로 흩어져 있다) |
| `G14` Feature Envy | Feature Envy(이 소스가 출처를 명시) |
| `G23` Prefer Polymorphism to If/Else | Repeated Switches |
| `G30` Functions Should Do One Thing | Long Function |
| `G36` Avoid Transitive Navigation | Message Chains |
| `C1`–`C5` | Comments |

- **`G30` ↔ Long Function의 대응이 중요하다.** 파울러 쪽도 긴 함수를 냄새로 보지만
  이 KB는 그 자리를 **관점 차이로** 판정했고([코드의 나쁜 냄새](code-smells.md)의
  "함수 크기 — 관점 차이다" 절), 이 소스의 3장은 **모순으로** 판정했다. 판정이 갈리는
  이유는 처방의 강도다 — 파울러는 이름 붙일 수 있으면 뽑으라고 하되 수치 상한을 두지
  않고, 이 소스는 스무 줄·들여쓰기 두 단계·블록 한 줄이라는 수치를 둔다.

## 파울러 쪽에 없는 것

- **환경(`E1`·`E2`)과 테스트(`T1`–`T9`)라는 갈래 자체.** 파울러 쪽 냄새는 코드에만 걸리고
  빌드·테스트 스위트에는 걸리지 않는다.
- **언어 특정 갈래(`J1`–`J3`).** 자바 항목이 목록에 섞여 있다.
- **이름에 관한 일곱 항목(`N1`–`N7`).** 파울러 쪽은 Mysterious Name 하나로 묶는다.
- `T4` **An Ignored Test Is a Question about an Ambiguity** — 무시된 테스트를 결함이
  아니라 **요구사항에 대한 질문의 표현**으로 재분류하는 항목이다 (17장 `T4`,
  p.313).[^martin2008] 이 KB의 [자기 테스트 코드](self-testing-code.md)에 대응 항목이
  없는 자리다.

## 목록이 함의하는 것 — 저자의 맺음

장은 목록의 완결성을 스스로 부정하며 닫는다 (17장 §"Conclusion",
p.314):[^martin2008]

> This list of heuristics and smells could hardly be said to be complete. Indeed, I'm not
> sure that such a list can *ever* be complete. But perhaps completeness should not be
> the goal, because what this list *does* do is imply a value system.

그리고 (17장 §"Conclusion", p.314):[^martin2008]

> Clean code is not written by following a set of rules. You don't become a software
> craftsman by learning a list of heuristics. Professionalism and craftsmanship come from
> values that drive disciplines.

- **이 맺음이 이 책을 읽는 방식을 규정한다.** 저자 자신은 목록을 규칙집이 아니라 가치
  체계의 표현으로 제시한다. 그럼에도 이 책이 규칙집으로 인용되는 것이 논쟁의 큰 부분이며,
  그 지형은 [클린 코드](../synthesis/clean-code.md) 허브가 담는다.

## 오늘날 통용되지 않는 항목들

목록에는 2008년 자바 생태계의 조건에 묶여 있고 이후 관행이 반대로 굳은 항목이 있다.
**이 KB는 그 판정을 아직 소스로 갖지 않으므로 여기서는 항목의 존재만 표시한다.**

- `J1` **Avoid Long Import Lists by Using Wildcards** — **두 개 이상의 클래스를 어떤
  패키지에서 쓴다면 `import package.*;`로 패키지 전체를 임포트하라. … 와일드카드 임포트를
  쓰는 것이 특정 임포트보다 일반적으로 여전히 낫다** (17장 `J1`, p.307).[^martin2008]
  근거는 **특정 임포트는 하드 의존이지만 와일드카드 임포트는 그렇지 않다**는 것이다.
  - #speculation 오늘날 주요 자바 스타일 가이드와 IDE 기본값은 반대 방향이다. 이 KB에
    그 판정을 담은 소스가 아직 없다.
- `G5`의 **"찾을 수 있는 곳마다 중복을 찾아 없애라"** — 반대 극을 세우는 소스가 이
  KB에 들어오면 [DRY 원칙](dry-principle.md)의 대비 절이 그 자리다.
- 3장의 함수 크기 수치 — **실증 대질 후보.** 저자 스스로 이를 뒷받침하는 연구를 댈 수
  없다고 밝혔고(3장 §"Small!", p.34), 이 KB에는 함수 길이와 결함률의 관계를 다룬 실증
  연구가 아직 반입돼 있지 않다. 반입되면 [작은 함수](small-functions.md)의 모순 절이
  갱신 대상이다.

## 이어지는 페이지

- [작은 함수](small-functions.md) — `F1`–`F3`·`G30`·`G34`의 전문이자 이 소스의 모순 축 하나
- [주석은 실패다](comments-as-failure.md) — `C1`–`C5`의 전문이자 모순 축 둘
- [객체와 자료 구조](objects-versus-data-structures.md) — `G23`·`G36`의 전문
- [코드의 나쁜 냄새](code-smells.md) — 독립적으로 만들어진 경쟁 목록
- [DRY 원칙](dry-principle.md) — `G5`의 최대주의가 놓이는 축
- [이름 짓기](naming-things.md) — `N1`–`N7`이 합류하는 자리
- [자기 테스트 코드](self-testing-code.md) — `T1`–`T9`가 합류하는 자리
- [코드의 일관성](consistency-in-code.md) — `G11`의 다른 소스 쪽 자리
- [계층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md) — `G6`의
  다른 소스 쪽 자리
- [외부 설정](external-configuration.md) — `G35`의 다른 소스 쪽 자리
- [클린 코드](../synthesis/clean-code.md) — 이 소스의 허브

[^martin2008]: Martin 2008, 17장 "Smells and Heuristics"(도입 p.286 · `C1`–`C5`
    pp.286–287 · `E1`–`E2` p.287 · `F1`–`F4` p.288 · `G5` pp.289–290 · `G6` pp.290–291 ·
    `G8` pp.291–292 · `G11` p.292 · `G14` pp.293–294 · `G19` pp.296–297 · `G20` p.297 ·
    `G21` pp.297–298과 각주 10 · `G23` p.299 · `G25` pp.300–301 · `G30` p.302 · `G34`
    pp.304–306 · `G35` p.306 · `G36` pp.306–307 · `J1` p.307 · `T4` p.313 ·
    §"Conclusion" p.314) · 6장 각주 4(p.99). 쪽은 인쇄판 쪽 번호이며 복원 절차는
    `it/archive/martin2008/_progress.yaml` 머리말이 정본이다. 이 장에는 Listing 17-1
    하나와 다수의 무번호 조각이 있고 펜스로는 옮기지 않았다 — 전부 급여 계산 예제
    문맥에 묶여 복사해 돌아가지 않는다. 도판은 없다. 갈래별 항목 수는 이 장의 식별자를
    세어 얻었다(합계 66).

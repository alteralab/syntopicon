---
type: concept
title: 클린 코드 비판 — 예제 코드가 그 책의 규칙을 어긴다
description: Clean Code 비판의 대표 2차 문헌이 펴는 내적 일관성 논증 — 취향 진술이 아니라 책의 예제 코드가 책 자신의 규칙을 어긴다는 대조, 3장의 이상적 리팩터링 결과가 3장의 부수 효과 정의를 어기는 자리, 단위 테스트 장의 DSL 예제가 2장의 이름 규칙을 어기는 자리, 6장의 자료 구조 정의가 통용 정의와 어긋난다는 지적, 좋은 조언과 낡은 조언이 섞여 있다는 총평, 그리고 저자가 대신 추천하는 책과 그 이유
generated: { by: "claude-opus-5", at: "2026-08-18T03:00:00Z" }
sources:
  - { id: qntm2020, resource: /it/sources/qntm2020.md }
  - { id: martin2008, resource: /it/sources/martin2008.md }
  - { id: ousterhout2024-aposd, resource: /it/sources/ousterhout2024-aposd.md }
---

# 클린 코드 비판 — 예제 코드가 그 책의 규칙을 어긴다

- [논증의 방식 — 취향이 아니라 내적 일관성](#논증의-방식--취향이-아니라-내적-일관성)
- [3장에서 동의하는 것](#3장에서-동의하는-것)
- [3장에서 갈리는 것](#3장에서-갈리는-것)
- [핵심 논증 — 이상적 리팩터링이 자기 정의를 어긴다](#핵심-논증--이상적-리팩터링이-자기-정의를-어긴다)
- [추출 검사도 자기 예제가 어긴다](#추출-검사도-자기-예제가-어긴다)
- [9장 — 같은 코드로 정반대 교훈을](#9장--같은-코드로-정반대-교훈을)
- [TDD의 빠진 0단계](#tdd의-빠진-0단계)
- [6장 — 자료 구조라는 말의 용법](#6장--자료-구조라는-말의-용법)
- [소수 생성기 예제 — 그리고 장 표기 정정](#소수-생성기-예제--그리고-장-표기-정정)
- [총평 — 무엇이 낡았는가](#총평--무엇이-낡았는가)
- [대신 추천하는 책](#대신-추천하는-책)
- [후기 — "문자 그대로 받아들이지 마라"라는 방어](#후기--문자-그대로-받아들이지-마라라는-방어)
- [이 KB가 이 소스를 어떻게 쓰는가](#이-kb가-이-소스를-어떻게-쓰는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **Clean Code에 대한 비판은 무엇을 근거로 서며, 그 근거는 검증 가능한가.**

## 논증의 방식 — 취향이 아니라 내적 일관성

- 저자가 먼저 주관성의 한계를 인정한다 — **"좋은 코드"나 "깨끗한 코드"의 실증적 정의에
  우리가 도달하는 것은 결코 가능하지 않을지도 모르며, 그것은 "깨끗한 코드"에 대한 어떤
  사람의 의견에 대한 다른 사람의 의견이 필연적으로 매우 주관적임을 뜻한다** (도입).[^qntm2020]
- **그러나 곧바로 주관성에 기대지 않는 논점을 세운다** (도입):[^qntm2020]

> That said, the major problem I have with Clean Code is that a lot of the example code in
> the book is just dreadful.

  - **이것이 이 소스의 방법론이다.** 규칙에 동의하느냐가 아니라 **책이 스스로 내건 규칙을
    책의 예제가 지키는가**를 대조한다. 원전이 이 KB에 있으므로(`martin2008`) 그 대조는
    실제로 검증할 수 있고, 아래 절들이 그 대조다.

## 3장에서 동의하는 것

**비판문인데도 동의 목록이 먼저 온다.** 이 절을 빼고 읽으면 이 소스는 실제보다 전면적인
부정이 된다.

- 저자가 이 장의 **단연 가장 강한 조언**으로 꼽는 것 — **함수는 추상화 수준을 섞지 말아야
  한다; 고수준 작업과 저수준 작업을 함께 수행해서는 안 되는데, 그것이 혼란스럽고 함수의
  책임을 흐리기 때문이다** (§1).[^qntm2020]
- 그 밖에 **타당한 것들(valid stuff)**로 드는 것 — 서술적이고 일관되며 동사구인 이름,
  부수 효과 없음(**정말 훌륭한 예를 제공한다**), 출력 인수 대신 반환값, 명령과 질의의
  분리 (§1).[^qntm2020]
- "한 가지만 하라"에도 조건부로 동의한다 — **"한 가지"를 어떻게 정의할지에 대해 너무
  독단적이지 않고, 많은 경우 이것이 대단히 비현실적일 수 있다는 것을 이해한다면**
  (§1).[^qntm2020]
- 총평 — **이것은 전부 합당한 입문 수준 조언이다** (§1).[^qntm2020]

## 3장에서 갈리는 것

- **플래그 인수** — 결론에는 동의하되 **근거를 기각한다.** 저자가 동의하는 이유는 소스
  코드의 꾸밈없는 `true`/`false`가 불투명하다는 것인데, **마틴의 논거는 오히려 불리언
  인수가 함수를 한 가지보다 많은 일을 하게 만든다는 것이고, 그래서는 안 된다는
  것이다** (§1).[^qntm2020]
- **내려가기 규칙** — **이것은 보편적으로 적용되는 것과는 거리가 멀다. 많은 소스 파일,
  나는 심지어 대부분의 소스 파일이 이런 식으로 말끔히 위계화될 수 없다고 말하겠다.
  그리고 그럴 수 있는 파일에서조차 IDE가 우리를 함수 호출에서 함수 구현으로, 또 되돌아
  오도록 손쉽게 뛰어가게 해 준다** (§1).[^qntm2020]
- **DRY** — **당시에 이것은 꽤 표준적인 조언이었다. 그러나 더 최근에 우리는 대체로 약간의
  중복이 세상에서 가장 나쁜 것은 아니라고 이해한다; 그것이 더 명확할 수 있고, 잘못된
  추상보다 쌀 수 있다** (§1).[^qntm2020]
  - **마지막 구절이 이 KB의 다른 축과 직결된다** — [DRY 원칙](dry-principle.md)의 대비
    절을 보라.
- **수치들** — 저자가 **그리고 그때 이상해진다**로 문단을 연 뒤 나열한다: 중첩 제어 구조를
  담을 만큼 크지 않아야 한다, 들여쓰기 두 단계 이하, 블록은 한 줄, 이상적 인수 개수는 0,
  인수 셋은 혼란스럽다. 그리고 — **가장 기이하게도, 마틴은 이상적인 함수가 두 줄에서 네
  줄 길이라고 단언한다. 이 조언은 실제로 그 장의 맨 앞에 놓여 있다. 그것이 첫째이자 가장
  중요한 규칙이다** (§1).[^qntm2020]
- **저자가 그 대목을 직접 인용한다** — 이 KB의 [작은 함수](small-functions.md)가 옮긴 것과
  같은 문단이고, 근거의 부재를 저자가 스스로 밝힌 부분("This is not an assertion that I
  can justify")을 포함해 인용한다 (§1).[^qntm2020]
- 그리고 과장이 아닌지 의심한 뒤 판정한다 — **이 모든 것이 과장처럼 들린다. … 그러나 이
  책은 이것에 대해 절대적으로 진지하다** (§1).[^qntm2020]

## 핵심 논증 — 이상적 리팩터링이 자기 정의를 어긴다

**이 소스에서 가장 무거운 논점이다.** 대상은 3장 끝의 `SetupTeardownIncluder` — 이 KB의
[작은 함수](small-functions.md)가 Listing 3-7로 다루는 그 코드다.

- 지위부터 못 박는다 — **다시 말하겠다: 이것은 마틴 자신의 코드이고 그의 개인적 기준에
  맞춰 쓰인 것이다. 이것은 학습 예제로서 우리에게 제시된 이상이다** (§1).[^qntm2020]
- **계수**(counting) — 클래스 안에 공개 정적 메서드 둘, 새 비공개 생성자 하나, 새 비공개
  메서드 열다섯이 있고 (§1):[^qntm2020]

> Of the fifteen private methods, fully thirteen of them either have side effects (such as
> buildIncludeDirective, which has side effects on newPageContent) or call out to other
> methods which have side effects (such as include, which calls buildIncludeDirective).

- **그리고 그것이 같은 장의 정의를 어긴다.** 저자가 반박을 미리 막는다 — 마틴의 부수 효과
  정의가 자기 클래스의 멤버 변수를 제외하는 것 아니냐는 해석을 놓고, **그러나 마틴 자신의
  정의가 이것과 모순된다**고 적으며 3장의 정의를 인용한다 (§1):[^qntm2020]

> Side effects are lies. Your function promises to do one thing, but it also does other
> hidden things. Sometimes it will make unexpected changes to the variables of its own
> class. [...] [T]hey are devious and damaging mistruths that often result in strange
> temporal couplings and order dependencies.

  - **이 인용은 원전과 대조된다.** 이 KB의 [작은 함수](small-functions.md)가 같은 문단을
    3장 §"Have No Side Effects"(p.44)에서 옮겼고, **"자기 클래스의 변수에 예상치 못한
    변경을 가한다"가 원문에 그대로 있다.**[^martin2008] 즉 이 비판의 전제는 실측으로
    확인된다.
- 결론 (§1):[^qntm2020]

> So why does Martin's own code, "clean" code, do nothing but this? Rather than have a
> method pass arguments to another method, Martin makes a distressing habit of having the
> first method set a member variable which the second method, or some other method, then
> reads back.

- **비유가 이 소스에서 가장 널리 인용되는 대목이다** — 누군가 커피 만드는 법을 보여
  주겠다며 부엌에 들어와, 아무 불도 켜지지 않는 스위치를 누르고, 머그를 꺼내 티스푼으로
  두 번 두드리고, 30초를 기다린 뒤, 보이지 않는 냉장고 뒤에서 **다른** 머그를 커피가 담긴
  채로 꺼낸다 (§1).[^qntm2020] **저 코드가 그와 같다**는 것이다.
- 그리고 테스트 가능성으로 못 박는다 (§1):[^qntm2020]

> How would you unit-test this method? Well, you can't. It's not a unit. It can't be
> separated from the side-effects it has on other parts of the code.

  - **이것이 이 소스의 논증이 검증 가능한 이유다.** 원전 3장이 인수를 줄이는 방법으로
    **인스턴스 변수로의 이동**을 제시하는데(§"Function Arguments", p.40)[^martin2008]
    그 조작의 귀결이 여기서 계상된다. 이 KB의 [작은 함수](small-functions.md)가 같은
    자리에 달아 둔 `#hypothesis`("인수를 숨은 상태로 바꾸는 것")를 이 소스가 실물로
    확인해 준다.

## 추출 검사도 자기 예제가 어긴다

- 저자가 원전의 판정 검사를 인용한다 — 마틴은 **"구현의 재진술이 아닌 이름으로 또 다른
  함수를 뽑아낼 수 있다면" 함수를 더 작은 함수로 쪼개는 것이 말이 된다**고 이 장에서
  진술한다 (§1).[^qntm2020]
- **그러고 나서 그가 우리에게 주는 것**이 `isTestPage()`(본문이
  `return pageData.hasAttribute("Test");` 한 줄)와
  `findInheritedPage()`(본문이 위임 한 줄)이고, **그리고 대여섯 개가 더 있는데 그중 어느
  것도 한 자리보다 많은 곳에서 호출되지 않는다** (§1).[^qntm2020]
  - **이 지적이 이 KB의 `contradicts` ①과 정확히 같은 지점을 찌른다** —
    [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)이 최악의 실물로 드는
    `addNullValueForAttribute`와 같은 모양(본문 한 줄, 이름이 구현의 재진술)이다.
    **두 비판이 서로를 참조하지 않고 같은 결론에 도달했다.**

## 9장 — 같은 코드로 정반대 교훈을

- 먼저 동의를 적는다 — 단위 테스트가 빠르고 독립적이고 반복 가능해야 한다는 것,
  리팩터링에 자신감을 준다는 것, 테스트가 대상 코드만큼 양이 많되 읽기에는 더 단순해야
  한다는 것에 대해 **이 장에는 좋고 기본적인 것이 많다** (§2).[^qntm2020]
- **그러나 도메인 특화 테스트 언어 예제에서 갈린다.** 원전이 단정 다섯 줄짜리 테스트를
  `assertEquals("HBchL", hw.getState())` 한 줄로 리팩터링해 자랑스럽게 제시하는데
  (§2):[^qntm2020]

> I was left so confused by this suggestion. I would use exactly the same code to
> demonstrate exactly the opposite lesson. Don't do this!

- **그리고 여기서도 내적 일관성 논증이 나온다.** 새 메서드 이름 `wayTooCold`는 형용사구다
  — **그것이 무엇을 하는지 전혀 불분명하다. 세계의 상태를 아주 춥게 만드는가? 세계의
  상태가 아주 추워진 것에 반응하는가? 아니면 세계의 상태가 지금 아주 추워야 한다는
  단언인가?** (§2).[^qntm2020]
- 저자가 **이 책 2장에서 직접 인용해** 대질한다 (§2):[^qntm2020]

> Methods should have verb or verb phrase names like postPayment, deletePage, or save.

  - **이 인용도 원전과 대조된다** — 이 KB의 [이름 짓기](naming-things.md)가 같은 문장을
    2장 §"Method Names"(p.25)에서 옮겼다.[^martin2008] 규칙과 예제가 어긋난다는 지적이
    실측으로 확인된다.
- 그리고 부수 효과가 또 지적된다 — `wayTooCold()`가 안에서 `controller.tic()`을 부르는데
  **그것을 추측할 방법이 없다** (§2).[^qntm2020]

## TDD의 빠진 0단계

- 저자가 원전의 세 법칙과 30초 주기를 인용한 뒤 (§3):[^qntm2020]

> But the book doesn't acknowledge the missing zeroth step in the process: figuring out
> how to break down the programming task in front of you, so that you can take a
> minuscule thirty-second bite out of it. That, in many cases, is exceedingly
> time-consuming, and frequently obviously useless, and frequently impossible.

  - 이 KB의 [자기 테스트 코드](self-testing-code.md)가 옮긴 세 법칙에 붙는 유보다.
    [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)가 같은 문제를 기어
    바꾸기로 다루는 자리다.

## 6장 — 자료 구조라는 말의 용법

- 저자가 원전의 반대칭 정의를 인용한 뒤 **그리고… 그게 다인가?**로 받는다 (§4).[^qntm2020]
- 지적 두 가지 (§4):[^qntm2020]

> Martin's definition of "data structure" disagrees with the definition everybody else
> uses. This is a very strange choice of definition, though Martin does at least define
> his term clearly.

  - 그리고 **객체를 멍청한 데이터로 보는 것과 메서드를 가진 정교한 추상으로 보는 것 사이에
    명확한 구분을 긋는 것은 정당하고 쓸모 있다**고 그 가치는 인정한다 (§4).[^qntm2020]
- 둘째 지적이 부재에 대한 것이다 — **대부분의 우리가 진짜 자료 구조라고 여기는 것,
  즉 배열·연결 리스트·해시 맵·이진 트리·그래프·스택·큐 등을 써서 깨끗하게 코딩하는 것에
  대한 내용이 이 책에 전혀 없다는 것이 꽤 두드러진다** (§4).[^qntm2020]
  - **이 지적은 이 KB의 [객체와 자료 구조](objects-versus-data-structures.md)를
    반박하지 않는다** — 그 페이지가 옮긴 것은 원전의 용어 정의이고, 이 소스도 그 정의가
    명확하다는 것은 인정한다. 갈리는 것은 **그 낱말이 통용 의미와 다르다는 점을 표시해야
    하는가**이고, 이 KB의 규약(원어 병기·확립 용어 우선, SCHEMA §3)이 이미 그것을
    요구한다.

## 소수 생성기 예제 — 그리고 장 표기 정정

- **먼저 이 소스의 장 표기를 정정한다.** 이 소스는 이 코드가 **8장에서 왔다**고 적는데
  (§5)[^qntm2020], **오류다.** 두 저자의 공개 대담이 이 코드를 **Listing 10-8, pp.145–146**
  으로 지목하고[^ousterhout2024-aposd] martin2008 스냅샷 실측이 그것을 확인한다 —
  **10장 Classes**, pp.145–146이다.[^martin2008] 마틴 본인이 그 장의 교훈을 밝힌다 —
  **그 장에서 나는 그 함수에서 세 클래스를 뽑아냈다. … 그 장의 교훈은 아주 큰 메서드가
  흔히 독립된 클래스로 분해하는 편이 나은 여러 구획을 담는다는 것이다**
  (§"Method Length", UB 발언).[^ousterhout2024-aposd] **비판의 논지에는 영향이 없다** —
  코드도 지적 내용도 같고 장 번호만 틀렸다.
- 마지막 예제로 `PrimeGenerator`를 든다. 저자의 반응 — **이 코드는 대체 뭔가? 이
  알고리즘은 뭔가? 이 메서드 이름들은 뭔가?** 그리고 **더 앞에서 우리는 메서드가 무언가를
  하는 명령이거나 무언가에 답하는 질의여야 하고 둘 다여서는 안 된다고 조언받았다. 이것은
  좋은 조언이었는데, 왜 이 메서드들 거의 전부가 그것을 무시하는가?** (§5).[^qntm2020]
- 그리고 이 소스에서 가장 센 문장이 나온다 (§5):[^qntm2020]

> If this is the quality of code which this programmer produces — at his own leisure,
> under ideal circumstances, with none of the pressures of real production software
> development, as a teaching example — then why should you pay any attention at all to
> the rest of his book?

- **주목할 만한 수렴이 하나 있다.** 이 예제에 나오는 메서드 이름
  `isLeastRelevantMultipleOfNextLargerPrimeFactor`는 **ousterhout2021이 12장 §12.6에서
  마틴의 주석 철학이 낳는 이름의 반례로 드는 바로 그 식별자다**
  ([주석은 실패다](comments-as-failure.md)의 모순 절). 두 비판자가 서로를 참조하지 않고
  같은 예제를 골랐다. #hypothesis 이 식별자가 그 자체로 잘 알려진 사례가 됐을 가능성이
  있다 — 어느 쪽도 상대를 인용하지 않는다.
  - **덧붙여 표기가 갈린다.** martin2008 스냅샷 p.145의 원문은
    `isLeastRelevantMultipleOfNextLargerPrimeFactor`(Next 포함)이고[^martin2008] 이 소스와
    ousterhout2021 12장은 그와 일치하는데, 두 저자의 공개 대담이 옮긴 코드에는
    `Next`가 빠져 있다.[^ousterhout2024-aposd] **대담 쪽의 전사 누락으로 판정했다.**

## 총평 — 무엇이 낡았는가

- 책 전체에 대한 판정 (§2):[^qntm2020]

> Clean Code mixes together a disarming combination of strong, timeless advice and advice
> which is highly questionable or dated or both.

- 낡았다고 지목되는 것들 (§2):[^qntm2020]
  - **사례 연구 장들** — **기본적으로 채움에 해당하는 여러 장이 자바 코드 리팩터링의
    수고스러운 예제에 집중한다; JUnit의 내부를 살펴보는 장이 통째로 있다.** 이 KB가
    같은 장들을 `skipped`로 처리한 사유와 겹친다
    (`it/archive/martin2008/_progress.yaml`).
  - **서식 장** — **요즘은 한 문장으로 줄어든다: "합리적인 표준 서식을 고르고, 자동화
    도구가 그것을 강제하도록 설정하고, 그 다음엔 이 주제를 다시는 생각하지 마라."**
  - **패러다임의 편중** — **내용이 다른 프로그래밍 패러다임을 배제한 채 객체 지향 코드에만
    거의 전적으로 집중한다. … 함수형 프로그래밍 기법이나 심지어 단순한 절차적 코드조차
    전혀 없다는 것은 당시에도 유감스러운 일이었고, 이후 몇 해 동안 더 두드러지기만 했다.**
  - **언어의 편중과 그 자바가 낡았다는 것** — 다만 **이런 종류의 일은 피할 수 없다 —
    프로그래밍 책은 전설적으로 잘 낡는다**는 유보를 함께 단다.
- 그리고 시점에 대한 진단 — **그것이 Clean Code가 한때 추천 도서였던 이유의 일부이고,
  나는 이제 그 추가 반대 방향으로 돌아오고 있다고 생각한다** (§2).[^qntm2020]
- 결론 (§6) — 입문서로도, 2008년 프로그래밍 모범 사례의 교육적 스냅샷이라는 사료로도
  추천하지 않겠다고 적는다.[^qntm2020] 다만 독서 모임 경험은 긍정적으로 적는다 —
  **우리는 좋은 논의를 했다. 개별 장들을 실제 현대적 관행에 대한 더 깊은 논의의 출발점으로
  쓸 수 있었다** (§6).[^qntm2020]

## 대신 추천하는 책

**2020-12-19 후기가 이 KB에 특히 중요하다.**

- 저자가 댓글의 제안으로 다른 책을 읽었다 — **아래 댓글의 제안에 따라 나는 존 오스터하우트의
  *A Philosophy of Software Design*(2018)을 읽었고 훨씬 더 긍정적인 경험이었음을 알았다.
  나는 그것을 Clean Code보다 기꺼이 추천하겠다** (Update, 2020-12-19).[^qntm2020]
- 그리고 두 책의 관계를 이렇게 적는다 (Update, 2020-12-19):[^qntm2020]

> I found that I agreed with nearly all of Ousterhout's assertions and suggestions for
> good software design, many of which are diametrically opposed to those found in Clean
> Code.

  - **이것이 이 KB의 `contradicts` 판정에 대한 제3자 확인이다.** 이 KB는
    [작은 함수](small-functions.md) ↔ [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)와
    [주석은 실패다](comments-as-failure.md) ↔ [주석을 왜 쓰는가](why-write-comments.md)를
    두 원전의 문장만 대조해 모순으로 판정했는데, 두 책을 다 읽은 제3자가 **다수가 정면으로
    반대된다(diametrically opposed)**고 독립적으로 적었다. 판정을 바꾸지는 않지만 그
    판정이 이 KB만의 독법이 아님을 확인해 준다.
- 다만 **대체재는 아니라고** 유보한다 — 그 책은 **개별 코드 줄을 쓰거나 비평하는 것보다
  더 높은 층위의 소프트웨어 설계 실천에 집중하므로** 완전 초보에게는 적합하지 않을 수
  있고, **지금 입문용 프로그래밍 교재 시장에는 실제로 공백 같은 것이 있다고 생각한다**
  (Update, 2020-12-19).[^qntm2020]

## 후기 — "문자 그대로 받아들이지 마라"라는 방어

**2022-03-21 후기가 이 책에 대한 가장 흔한 방어를 다룬다.**

- 방어의 내용 — 책의 조언을 문자 그대로 받거나 독단적으로 적용해서는 안 되며, 비판적으로
  생각하고 나쁜 조언은 골라서 무시하는 것이 독자의 몫이라는 것 (Afterword,
  2022-03-21).[^qntm2020]
- 저자가 그 방어의 근거로 인용되는 책 자신의 문장을 옮긴다. **이 KB에 원전이 있으므로
  대조했고 원문과 일치한다** (1장 §"Schools of Thought", p.13):[^martin2008]

> Indeed, many of the recommendations in this book are controversial. You will probably
> not agree with all of them. You might violently disagree with some of them. That's fine.
> We can't claim final authority.

- 저자의 반박 — **나는 이것이 애초에 나쁜 조언과 나쁜 예제 코드를 담은 책에 대한 특별히
  설득력 있는 방어라고 생각하지 않는다** (Afterword).[^qntm2020] 그리고 **이것은 책을
  비판으로부터 방패 삼는 데 쓸 수 있는 것이 아니다** (Afterword).[^qntm2020]
- **그리고 독자층으로 논점을 옮긴다** (Afterword):[^qntm2020]

> Inexperienced programmers, meanwhile — and Clean Code is an entry-level programming
> text, so this is the target audience, whose experiences are most important — won't be
> able to distinguish the good advice from the bad, and won't be able to see that the
> example code is bad and shouldn't be imitated.

  - 대칭으로 숙련자에 대해서도 적는다 — **숙련된 프로그래머는 Clean Code를 읽어 거의 아무것도
    얻지 못할 것이다** (Afterword).[^qntm2020]

## 이 KB가 이 소스를 어떻게 쓰는가

- **이 소스의 논점 하나가 1차 사료로 확인됐다.** 이 소스는 예제 코드가 책 자신의 규칙을
  어긴다고 논증하는데, 두 저자의 공개 대담에서 마틴 본인이 `PrimeGenerator`에 대해
  **며칠 전 그 알고리즘으로 처음 돌아왔을 때 나는 그 이름들과 구조와 씨름했다**고 적고
  (§"Method Length", UB 발언)[^ousterhout2024-aposd], 요약 절은
  **`PrimeGenerator`를 메서드로 내부 분해한 것은 문제가 있다**를 **양측 합의 항목**으로
  올린다 (§"Method Length Summary").[^ousterhout2024-aposd] 이 소스의 가장 센 예제
  비판이 저자 본인에게 부분적으로 수용된 셈이다. 전문은
  [오스터하우트–마틴 공개 대담](../concepts/aposd-vs-clean-code-dialogue.md)에 있다.
- **이 소스는 `contradicts`를 새로 만들지 않는다.** 자격 기준(검증 가능한 사실·처방의
  정면 충돌)에 비추어 판정한 결과다.
  - 이 페이지의 claim 대부분은 **원전에 대한 사실 주장**(예제 코드가 이러이러하다)이지
    경쟁 처방이 아니다. 사실 주장은 대조로 해소되며, 실제로 위에서 셋을 대조해 전부
    원전과 일치함을 확인했다.
  - 경쟁 처방으로 읽힐 수 있는 것은 DRY 대목("잘못된 추상보다 쌀 수 있다") 하나인데,
    그 대비는 [DRY 원칙](dry-principle.md)이 이미 담고 있고 그쪽 판정은 층위 차이였다.
  - **이 소스와 원전 페이지들 사이에 `contradicts`를 거는 것은 범주 오류다** — 이 소스는
    원전과 같은 물음에 다른 답을 하는 것이 아니라 **원전을 평가**한다. 2차 문헌의 자리다.
- **대신 하는 일은 셋이다.** ① 기존 `contradicts` 둘의 근거를 제3자 진술로 보강한다
  (위 [대신 추천하는 책](#대신-추천하는-책) 절) ② 원전 페이지들이 옮긴 문장이 실제로
  원문과 일치하는지 대조할 기회를 준다(위에서 셋을 대조했다) ③ 이 KB가 `skipped`로
  처리한 장들의 사유를 외부 근거로 뒷받침한다.

## 이어지는 페이지

- [작은 함수](small-functions.md) — 이 비판이 겨냥하는 3장의 전문
- [주석은 실패다](comments-as-failure.md) — 같은 식별자를 반례로 드는 다른 비판이 있는 자리
- [객체와 자료 구조](objects-versus-data-structures.md) — 이 비판이 용어 문제로 지적하는
  6장의 전문
- [자기 테스트 코드](self-testing-code.md) — 9장 DSL 예제와 TDD 0단계 유보가 붙는 자리
- [이름 짓기](naming-things.md) — 2장의 이름 규칙이 대질에 쓰이는 자리
- [DRY 원칙](dry-principle.md) — "잘못된 추상보다 쌀 수 있다"가 놓이는 축
- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — 한 줄짜리 메서드에 대해 같은
  결론에 독립적으로 도달한 자리
- [클린 코드라는 말의 정의](clean-code-defined.md) — 책 자신의 유보가 사는 자리
- [클린 코드의 발견법 목록](clean-code-heuristics.md) — 낡았다고 지목된 항목들
- [오스터하우트–마틴 공개 대담](../concepts/aposd-vs-clean-code-dialogue.md) — 이 비판의 논점 일부가
  저자 본인에게 수용된 1차 사료. 이 페이지의 장 표기 정정도 거기서 왔다
- [클린 코드](../synthesis/clean-code.md) — 이 축의 허브

[^ousterhout2024-aposd]: Ousterhout & Martin 2024, "A Philosophy of Software Design
    vs Clean Code". **대담이므로 locator에 발언자를 함께 적는다** — `JOHN`은 John
    Ousterhout, `UB`는 Robert C. Martin이다. 규약과 스냅샷 취득 경로는
    `it/archive/ousterhout2024-aposd/_progress.yaml` 머리말이 정본이다.

[^qntm2020]: qntm 2020, "It's probably time to stop recommending Clean Code"
    (도입 · §1 · §2 · §3 · §4 · §5 · §6 · Update, 2020-12-19 · Afterword, 2022-03-21).
    **절 번호는 이 KB가 매긴 것이다** — 이 글의 본문은 `*` 하나로 나뉜 무제 절 일곱
    개이고, 번호 매김 규약은 `it/archive/qntm2020/_progress.yaml` 머리말이 정본이다.
    이 페이지에는 코드 펜스를 두지 않았다 — 이 소스가 싣는 코드는 전부 martin2008에서
    옮겨 온 예제이고, 이 KB는 그것을 원전 쪽에서도 펜스로 옮기지 않았다(복사해 돌아갈
    코드가 아니다). 스냅샷에 함께 보존된 댓글 145개는 본문 밖이라 반입하지 않았다.

[^martin2008]: Martin 2008, 1장 §"Schools of Thought"(p.13) · 2장 §"Method Names"(p.25)
    · 3장 §"Have No Side Effects"(p.44)·§"Function Arguments"(p.40). **논쟁 중인
    소스다** — 지위와 반입 규약은 `it/sources/martin2008.md`가 정본이다. 이 페이지에서
    이 소스는 **비판이 인용한 문장을 원문과 대조하는 용도로만** 쓰였다. 쪽은 인쇄판 쪽
    번호이며 복원 절차는 `it/archive/martin2008/_progress.yaml` 머리말이 정본이다.

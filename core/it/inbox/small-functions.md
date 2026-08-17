---
type: concept
title: 작은 함수
description: 함수는 작아야 하고 그보다 더 작아야 한다는 규칙과 그것이 딸린 처방들 — 저자 스스로 근거를 댈 수 없다고 밝히는 자리, 스무 줄과 들여쓰기 두 단계라는 구체 수치, "한 가지만 하라"를 추출 가능성으로 판정하는 조작적 정의, 내려가기 규칙, 인수 개수를 0에서 3으로 늘어놓는 서열과 플래그 인수 금지, 부수 효과와 명령·질의 분리, 오류 코드 대신 예외, 그리고 이 규칙이 깊은 모듈 잣대와 정면으로 갈리는 자리
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
contradicts: [deep-and-shallow-modules]
sources:
  - { id: martin2008, resource: /it/sources/martin2008.md }
  - { id: ousterhout2021, resource: /it/sources/ousterhout2021.md }
  - { id: qntm2020, resource: /it/sources/qntm2020.md }
  - { id: ousterhout2024-aposd, resource: /it/sources/ousterhout2024-aposd.md }
---

# 작은 함수

- [규칙과 그 근거의 지위](#규칙과-그-근거의-지위)
- [얼마나 작은가 — 수치](#얼마나-작은가--수치)
- [블록과 들여쓰기](#블록과-들여쓰기)
- [한 가지만 하라 — 조작적 정의](#한-가지만-하라--조작적-정의)
- [함수당 추상화 수준 하나와 내려가기 규칙](#함수당-추상화-수준-하나와-내려가기-규칙)
- [switch 문](#switch-문)
- [서술적인 이름을 쓰라](#서술적인-이름을-쓰라)
- [인수 — 0이 최선이라는 서열](#인수--0이-최선이라는-서열)
- [플래그 인수](#플래그-인수)
- [부수 효과는 거짓말이다](#부수-효과는-거짓말이다)
- [명령과 질의를 분리하라](#명령과-질의를-분리하라)
- [오류 코드 대신 예외를](#오류-코드-대신-예외를)
- [중복하지 마라](#중복하지-마라)
- [이렇게 쓰는 것이 아니라 이렇게 고친다](#이렇게-쓰는-것이-아니라-이렇게-고친다)
- [2차 문헌이 이 장의 예제를 이 장의 규칙과 대질한다](#2차-문헌이-이-장의-예제를-이-장의-규칙과-대질한다)
- [저자 본인이 나중에 좁힌 것](#저자-본인이-나중에-좁힌-것)
- [모순 — 함수를 쪼개면 복잡성이 주는가](#모순--함수를-쪼개면-복잡성이-주는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **함수는 얼마나 작아야 하며, 그 규칙은 무엇으로 정당화되는가.**

> **이 페이지의 소스는 논쟁 중인 소스다.** 이 KB는 martin2008을 권위 원전으로 들이지
> 않는다 — 반입 지위와 그 근거는 [소스 메타](../sources/martin2008.md)가 정본이다.
> 아래 주장은 정확히 옮기되, 경쟁 주장과 반드시 나란히 읽는다.

## 규칙과 그 근거의 지위

- 규칙 자체 (3장 §"Small!", p.34):[^martin2008]

> The first rule of functions is that they should be small. The second rule of functions
> is that they should be smaller than that.

- **저자가 바로 다음 문장에서 근거의 부재를 스스로 밝힌다** (3장 §"Small!",
  p.34):[^martin2008]

> This is not an assertion that I can justify. I can't provide any references to research
> that shows that very small functions are better. What I can tell you is that for nearly
> four decades I have written functions of all different sizes.

  - 그러므로 이 규칙의 지위는 **실증이 아니라 저자의 경험 보고**다. 이 KB가 이 소스를
    논쟁 중인 소스로 다루는 근거 하나가 이 자기 진술이다 — 뒤의
    [모순](#모순--함수를-쪼개면-복잡성이-주는가) 절이 이 자리를 다시 부른다.
  - 규칙의 출처로 저자가 대는 것도 실증이 아니라 일화다 — 1999년 Kent Beck의 집에서 본
    `Sparkle`이라는 자바/스윙 프로그램에서 **모든 함수가 두 줄, 세 줄, 네 줄이었고**
    그것이 **함수가 그만큼 짧아야 하는 기준**이라고 적는다 (3장 §"Small!",
    p.34).[^martin2008] 저자는 그 프로그램의 사본이 남아 있지 않다고 각주에 적는다.

## 얼마나 작은가 — 수치

- 화면 한 판이라는 옛 기준은 폐기된다 — **80년대에 우리는 함수가 화면 하나보다 커서는
  안 된다고 말하곤 했다. 물론 그것은 VT100 화면이 24줄 80열이던 시절의 이야기다**
  (3장 §"Small!", p.34).[^martin2008]
- 그 자리를 대신하는 수치 (3장 §"Small!", p.34):[^martin2008]

> Lines should not be 150 characters long. Functions should not be 100 lines long.
> Functions should hardly ever be 20 lines long.

- 그리고 예제로 제시되는 목표 크기는 **네 줄**이다 — 저자가 아홉 줄짜리 리팩터링 결과
  (Listing 3-2)를 놓고 **함수는 보통 Listing 3-2보다 더 짧아야 한다**고 적은 뒤 그것을
  세 줄 본문(Listing 3-3)으로 다시 줄인다 (3장 §"Blocks and Indenting",
  p.35).[^martin2008]

## 블록과 들여쓰기

- 규칙이 제어문 안쪽까지 내려간다 — **이것은 `if` 문·`else` 문·`while` 문 등의 안쪽
  블록이 한 줄이어야 함을 함의한다. 아마 그 한 줄은 함수 호출이어야 할 것이다. 이것은
  둘러싼 함수를 작게 유지할 뿐 아니라, 블록 안에서 호출되는 함수가 멋지게 서술적인
  이름을 가질 수 있으므로 문서로서의 가치도 더한다** (3장 §"Blocks and Indenting",
  p.35).[^martin2008]
- 들여쓰기 상한 — **또한 이것은 함수가 중첩 구조를 담을 만큼 커서는 안 됨을 함의한다.
  따라서 함수의 들여쓰기 수준은 하나나 둘보다 커서는 안 된다** (3장 §"Blocks and
  Indenting", p.35).[^martin2008]
  - **이 두 문장이 [모순](#모순--함수를-쪼개면-복잡성이-주는가) 절이 다루는 처방의
    실물이다.** "블록 안은 한 줄, 그 한 줄은 함수 호출"은 곧 이름을 붙일 수 있는 모든
    블록을 함수로 뽑으라는 지시이고, 상대 소스가 얕은 메서드의 생산 경로로 지목하는
    것이 정확히 이것이다.

## 한 가지만 하라 — 조작적 정의

- 오래된 조언을 인용한다 (3장 §"Do One Thing", p.35):[^martin2008]

> FUNCTIONS SHOULD DO ONE THING. THEY SHOULD DO IT WELL. THEY SHOULD DO IT ONLY.

- **저자 스스로 이 조언의 결함을 지적한다** — **이 진술의 문제는 "한 가지"가 무엇인지
  알기 어렵다는 것이다** (3장 §"Do One Thing", p.35).[^martin2008] 세 줄짜리 예제조차
  ① 테스트 페이지인지 판정 ② 그렇다면 설정·해제 포함 ③ HTML로 렌더 — **세 가지를 한다고
  주장하기 쉽다**고 적는다.
- 그래서 판정 기준을 추상화 수준으로 옮긴다 — **함수가 그 함수의 명시된 이름보다 한
  수준 아래인 단계들만 한다면 그 함수는 한 가지를 하는 것이다. 결국 우리가 함수를 쓰는
  이유는 더 큰 개념(다시 말해 함수의 이름)을 다음 추상화 수준의 단계 집합으로 분해하기
  위해서다** (3장 §"Do One Thing", p.36).[^martin2008]
- **그리고 판정을 실행 가능한 검사로 바꾼다** (3장 §"Do One Thing", p.36):[^martin2008]

> So, another way to know that a function is doing more than "one thing" is if you can
> extract another function from it with a name that is not merely a restatement of its
> implementation.

  - **이 검사가 [모순](#모순--함수를-쪼개면-복잡성이-주는가) 절의 두 번째 축이다.**
    판정 기준이 "쪼갤 수 있는가"이므로, 쪼갤 수 있는 한 계속 쪼개라는 지시로 읽힌다.
    상대 소스는 같은 조작을 **깊이를 깎는 조작**으로 계산한다.
- 함수 안에 절이 생기는 것도 같은 증상으로 본다 — **한 가지를 하는 함수는 합리적으로
  절로 나뉠 수 없다** (3장 §"Sections within Functions", p.36).[^martin2008]

## 함수당 추상화 수준 하나와 내려가기 규칙

- **함수가 "한 가지"를 하도록 보장하려면 함수 안의 문장이 전부 같은 추상화 수준에 있어야
  한다** (3장 §"One Level of Abstraction per Function", p.36).[^martin2008]
- 섞일 때의 결과 — **함수 안에서 추상화 수준을 섞는 것은 언제나 혼란스럽다. 독자는 특정
  표현이 본질적 개념인지 세부인지 분간하지 못할 수 있다. 더 나쁘게는, 깨진 유리창처럼
  일단 세부가 본질적 개념과 섞이면 점점 더 많은 세부가 함수 안에 쌓이는 경향이 있다**
  (3장 §"One Level of Abstraction per Function", pp.36–37).[^martin2008]
  - 깨진 유리창(broken windows) 비유는 이 KB에 이미 있다 —
    [소프트웨어 엔트로피와 깨진 유리창](../concepts/software-entropy-and-broken-windows.md).
- **내려가기 규칙(The Stepdown Rule)** — **우리는 코드가 하향식 서사(top-down narrative)처럼
  읽히기를 원한다. 우리는 모든 함수 뒤에 다음 추상화 수준의 함수들이 따라와서, 함수 목록을
  내려 읽으며 한 번에 한 추상화 수준씩 내려갈 수 있기를 원한다** (3장 §"Reading Code from
  Top to Bottom", p.37).[^martin2008]
- 난이도가 명시된다 — **프로그래머가 이 규칙을 따르고 단일 추상화 수준에 머무르는 함수를
  쓰는 법을 배우기는 아주 어려운 일로 드러난다. 그러나 이 요령을 배우는 것 또한 아주
  중요하다. 그것이 함수를 짧게 유지하고 "한 가지"를 하도록 보장하는 열쇠다** (3장
  §"Reading Code from Top to Bottom", p.37).[^martin2008]

## switch 문

- 진단 — **작은 `switch` 문을 만들기는 어렵다. 두 개의 `case`만 있는 `switch` 문조차
  내가 단일 블록이나 함수이기를 바라는 것보다 크다. `switch` 문이 한 가지를 하게 만들기도
  어렵다. 그 본성상 `switch` 문은 언제나 N 가지를 한다** (3장 §"Switch Statements",
  p.37).[^martin2008] 저자는 각주에서 `if/else` 연쇄도 여기 포함한다고 적는다.
- 처방은 다형성이다 — **이 문제의 해법은 `switch` 문을 ABSTRACT FACTORY의 지하실에
  파묻고 아무도 보지 못하게 하는 것이다** (3장 §"Switch Statements",
  p.38).[^martin2008] 팩터리가 `switch`로 `Employee` 파생형 인스턴스를 만들고
  `calculatePay`·`isPayday`·`deliverPay`는 인터페이스를 통해 다형적으로 분배된다.
- 근거로 드는 것은 SRP와 OCP다 — 원래의 `calculatePay(Employee e)`는 **바뀔 이유가
  둘 이상이므로 단일 책임 원칙을 어기고**, **새 타입이 추가될 때마다 바뀌어야 하므로
  개방 폐쇄 원칙을 어긴다** (3장 §"Switch Statements", p.38).[^martin2008]
- **일반 규칙에 예외가 명시된다** — **`switch` 문에 대한 나의 일반 규칙은, 그것이 단
  한 번만 나타나고, 다형적 객체를 만드는 데 쓰이며, 상속 관계 뒤에 숨어 시스템의 나머지가
  그것을 볼 수 없다면 용인될 수 있다는 것이다. 물론 모든 상황은 고유하고, 내가 그 규칙의
  일부 이상을 어기는 때도 있다** (3장 §"Switch Statements", pp.38–39).[^martin2008]
  - 같은 책 안에서 이 처방이 **6장과 긴장한다는 것을 저자 자신이 지목한다** —
    [객체와 자료 구조](objects-versus-data-structures.md)의 마지막 절이 그 자리다.

## 서술적인 이름을 쓰라

- **함수가 작고 초점이 좁을수록 서술적인 이름을 고르기 쉽다** (3장 §"Use Descriptive
  Names", p.39).[^martin2008]
- 길이에 대한 판정 (3장 §"Use Descriptive Names", p.39):[^martin2008]

> Don't be afraid to make a name long. A long descriptive name is better than a short
> enigmatic name. A long descriptive name is better than a long descriptive comment.

  - **마지막 문장이 4장으로 이어지는 다리다** — 긴 이름이 긴 주석보다 낫다는 명제가
    [주석은 실패다](comments-as-failure.md)의 전제이고, 상대 소스는 바로 그 귀결로
    나온 이름(`isLeastRelevantMultipleOfNextLargerPrimeFactor`)을 반례로 든다.
- 이름 고르기가 설계를 바꾼다는 관찰 — **서술적인 이름을 고르는 것은 모듈의 설계를 당신
  마음속에서 명료하게 하고 그것을 개선하도록 돕는다. 좋은 이름을 찾다가 코드의 유리한
  재구조화로 이어지는 일은 전혀 드물지 않다** (3장 §"Use Descriptive Names",
  p.40).[^martin2008]
  - 이 관찰은 다른 두 소스와 **일치한다** — [이름 짓기](naming-things.md)의 "이름이
    안 떠오르는 것이 진단이다" 절이 그 자리다.

## 인수 — 0이 최선이라는 서열

- 서열이 못 박힌다 (3장 §"Function Arguments", p.40):[^martin2008]

> The ideal number of arguments for a function is zero (niladic). Next comes one
> (monadic), followed closely by two (dyadic). Three arguments (triadic) should be
> avoided where possible. More than three (polyadic) requires very special
> justification—and then shouldn't be used anyway.

- 근거 둘 — ① **인수는 어렵다. 개념적 힘을 많이 잡아먹는다** (3장 §"Function Arguments",
  p.40)[^martin2008] ② **테스트 관점에서 인수는 더 어렵다. 인수의 온갖 조합이 제대로
  동작하는지 확인할 테스트 케이스를 전부 쓰는 어려움을 상상해 보라** (3장 §"Function
  Arguments", p.40).[^martin2008]
- **인수를 없애는 방법으로 저자가 제시하는 것은 인스턴스 변수로의 이동이다** — 예제에서
  `StringBuffer`를 **인수로 넘길 수도 있었지만 인스턴스 변수로 만들었다**고 적는다
  (3장 §"Function Arguments", p.40).[^martin2008]
  - #hypothesis 이 조작은 인수를 숨은 상태로 바꾸는 것이므로 인터페이스의 형식적 부분을
    줄이는 대신 비형식적 부분(호출 순서 의존)을 늘린다. 저자가 그렇게 정식화하지는
    않는다. 상대 소스는 그 비형식적 부분도 인터페이스로 센다 —
    [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)의 "인터페이스에 무엇이 들어
    있는가" 절.
- 인수가 셋 이상 필요해 보이면 **그중 일부를 자기 클래스로 감싸야 할 가능성이 높다**
  (3장 §"Argument Objects", p.43).[^martin2008] `makeCircle(double x, double y, double
  radius)`가 `makeCircle(Point center, double radius)`가 되는 예다.

## 플래그 인수

- 판정 (3장 §"Flag Arguments", p.41):[^martin2008]

> Flag arguments are ugly. Passing a boolean into a function is a truly terrible
> practice. It immediately complicates the signature of the method, loudly proclaiming
> that this function does more than one thing.

- 처방은 함수를 둘로 쪼개는 것이다 — `render(true)` 대신 **`renderForSuite()`와
  `renderForSingleTest()`로 함수를 나눴어야 했다** (3장 §"Flag Arguments",
  p.41).[^martin2008]
- 17장에 같은 항목이 둘로 다시 실린다 — `F3` **Flag Arguments**와 `G15`
  **Selector Arguments**다. `G15`는 범위를 넓힌다 — **물론 선택자가 불리언일 필요는
  없다. 열거형·정수, 또는 함수의 동작을 고르는 데 쓰이는 어떤 타입의 인수든 될 수 있다.
  일반적으로 동작을 고르는 코드를 함수에 넘기는 것보다 함수를 여럿 두는 편이 낫다**
  (17장 `G15`, p.295).[^martin2008]

## 부수 효과는 거짓말이다

- **부수 효과는 거짓말이다. 당신의 함수는 한 가지를 하겠다고 약속하지만 다른 숨은 일도
  한다** (3장 §"Have No Side Effects", p.44).[^martin2008]
- 예제의 진단이 시간적 결합이다 — `checkPassword`가 안에서 `Session.initialize()`를
  부르는 것을 두고 **이 부수 효과가 시간적 결합(temporal coupling)을 만든다. 즉
  `checkPassword`는 특정 시점에만 호출될 수 있다** (3장 §"Have No Side Effects",
  p.44).[^martin2008]
  - **이름으로 드러내라는 처방과 그 대가를 저자가 같은 문단에서 인정한다** — 이름을
    `checkPasswordAndInitializeSession`으로 바꿀 수 있으나 **그것은 분명히 "한 가지를
    하라"를 어긴다** (3장 §"Have No Side Effects", p.44).[^martin2008]
- 출력 인수는 피한다 — **일반적으로 출력 인수는 피해야 한다. 함수가 무언가의 상태를
  바꿔야 한다면 그것을 소유하는 객체의 상태를 바꾸게 하라** (3장 §"Output Arguments",
  p.45).[^martin2008]
- 시간적 결합 자체는 이 KB에 이미 다른 소스로 들어와 있다 —
  [시간적 결합을 깨기](../concepts/breaking-temporal-coupling.md). 17장 `G31`이 여기에
  더 강한 처방을 얹는다 — **시간적 결합은 흔히 필요하지만 그 결합을 숨겨서는 안 된다.
  호출돼야 하는 순서가 뻔해지도록 함수의 인수를 구조화하라** (17장 `G31`,
  p.302).[^martin2008] 각 함수가 다음 함수가 필요로 하는 결과를 내놓는 **양동이 릴레이
  (bucket brigade)**가 그 실물이고, 저자는 그 대가를 인정한다 — **이것이 함수의 복잡성을
  올린다고 불평할 수 있고 당신이 옳을 것이다. 그러나 그 여분의 구문적 복잡성이 상황의
  참된 시간적 복잡성을 드러낸다** (17장 `G31`, p.303).[^martin2008]

## 명령과 질의를 분리하라

- **함수는 무언가를 하거나 무언가에 답해야 하며, 둘 다 해서는 안 된다. 당신의 함수는
  객체의 상태를 바꾸거나, 그 객체에 대한 어떤 정보를 돌려주거나 둘 중 하나여야 한다**
  (3장 §"Command Query Separation", p.45).[^martin2008]
- 예제가 `if (set("username", "unclebob"))`이다 — `set`이 동사인지 형용사인지 읽기에서
  분간되지 않는다는 것이 진단이고, 처방은 `attributeExists`와 `setAttribute`로 가르는
  것이다 (3장 §"Command Query Separation", pp.45–46).[^martin2008]

## 오류 코드 대신 예외를

- **오류 코드를 돌려주는 대신 예외를 쓰면 오류 처리 코드가 정상 경로 코드에서 분리될 수
  있고 단순해질 수 있다** (3장 §"Prefer Exceptions to Returning Error Codes",
  p.46).[^martin2008]
- `try`/`catch` 블록도 추출 대상이다 — **`try`/`catch` 블록은 그 자체로 추하다. 그것은
  코드의 구조를 흐리고 오류 처리를 정상 처리와 섞는다. 그러니 `try`와 `catch` 블록의
  본문을 각자의 함수로 뽑아내는 편이 낫다** (3장 §"Extract Try/Catch Blocks",
  p.46).[^martin2008]
- 그리고 규칙이 하나 더 파생된다 — **함수는 한 가지를 해야 한다. 오류 처리는 한 가지다.
  따라서 오류를 처리하는 함수는 다른 아무것도 해서는 안 된다. 이것은 `try` 키워드가
  함수 안에 있다면 그것이 함수의 맨 첫 낱말이어야 하고 `catch`/`finally` 블록 뒤에
  아무것도 없어야 함을 함의한다** (3장 §"Error Handling Is One Thing",
  p.47).[^martin2008]
- 오류 코드 열거형을 **의존성 자석(dependency magnet)**이라 부른다 — 그것이 바뀌면
  그것을 임포트한 모든 클래스가 다시 컴파일·배포돼야 하고, 그 압력 때문에 **프로그래머가
  새 오류를 더하기 싫어해 옛 오류 코드를 재사용한다** (3장 §"The Error.java Dependency
  Magnet", pp.47–48).[^martin2008]
  - 오류를 아예 없애는 셋째 입장이 이 KB에 있다 —
    [오류를 존재하지 않게 정의하라](define-errors-out-of-existence.md). 그쪽은 예외를
    던지는 것 자체를 인터페이스 복잡성으로 계상하므로 이 절과 층위가 다르다(이 절은
    오류를 신호하는 **수단**을, 그쪽은 오류의 **개수**를 다룬다).

## 중복하지 마라

- 예제의 결함 넷 중 하나로 중복이 지목된다 — 같은 알고리즘이 `SetUp`·`SuiteSetUp`·
  `TearDown`·`SuiteTearDown` 네 번 되풀이되고, **그것이 코드를 부풀리고 알고리즘이
  바뀌어야 할 때 네 겹의 수정을 요구한다. 또한 그것은 누락 오류의 네 겹 기회이기도 하다**
  (3장 §"Don't Repeat Yourself", p.48).[^martin2008]
- 그리고 이 소스에서 가장 강한 일반화가 여기 나온다 (3장 §"Don't Repeat Yourself",
  p.48):[^martin2008]

> Duplication may be the root of all evil in software.

  - 17장이 같은 것을 다시 말한다 — **이것은 이 책에서 가장 중요한 규칙 중 하나이고
    당신은 그것을 아주 진지하게 받아들여야 한다** (17장 `G5`, p.289)[^martin2008], 그리고
    **찾을 수 있는 곳마다 중복을 찾아 없애라** (17장 `G5`, p.290).[^martin2008]
  - **이 최대주의가 DRY 축의 한쪽 극이다.** 반대 극과의 대비는
    [DRY 원칙](dry-principle.md)의 해당 절에 있다.
- 구조적 프로그래밍의 단일 출구 규칙은 상대화된다 — **구조적 프로그래밍의 목표와 규율에
  공감하지만, 함수가 아주 작을 때 그 규칙들은 이득이 거의 없다. 그런 규칙이 유의미한
  이득을 주는 것은 더 큰 함수에서뿐이다** (3장 §"Structured Programming",
  p.49).[^martin2008] 즉 이 장의 다른 규칙들이 이 규칙의 폐기를 정당화하는 구조다.

## 이렇게 쓰는 것이 아니라 이렇게 고친다

- **저자는 자기가 처음부터 이렇게 쓰지 않는다고 명시한다** (3장 §"How Do You Write
  Functions Like This?", p.49):[^martin2008]

> When I write functions, they come out long and complicated. They have lots of indenting
> and nested loops. They have long argument lists. The names are arbitrary, and there is
> duplicated code. But I also have a suite of unit tests that cover every one of those
> clumsy lines of code.

- 그리고 (3장 §"How Do You Write Functions Like This?", p.49):[^martin2008]

> In the end, I wind up with functions that follow the rules I've laid down in this
> chapter. I don't write them that way to start. I don't think anyone could.

  - **이 진술이 이 장의 규칙을 리팩터링 목표로 재분류한다** — 작성 규칙이 아니라 도착
    상태다. 그 이행 절차의 원전은 [리팩터링](refactoring.md)이고, 담보가 되는 테스트는
    [자기 테스트 코드](self-testing-code.md)다.

## 2차 문헌이 이 장의 예제를 이 장의 규칙과 대질한다

이 장 끝의 `SetupTeardownIncluder`(Listing 3-7)는 저자가 이 장의 규칙을 전부 적용해 얻은
**도착 상태**로 제시한 코드다. **이 KB에 들어온 2차 문헌이 그 코드를 이 장의 정의와
대질한다.**

- 계수 — 비공개 메서드 열다섯 중 **꼬박 열셋이 부수 효과를 갖거나 부수 효과를 갖는 다른
  메서드를 호출한다** (§1).[^qntm2020]
- 그리고 그것이 위 [부수 효과는 거짓말이다](#부수-효과는-거짓말이다) 절의 정의와 어긋난다는
  것이 논점이다 — 비판자는 그 정의를 인용하며 **마틴 자신의 정의가 이것과 모순된다**고
  적는다 (§1).[^qntm2020] **인용은 원문과 대조했고 일치한다**(이 페이지가 옮긴 것과 같은
  문단, 3장 §"Have No Side Effects", p.44).
- 위 [인수 — 0이 최선이라는 서열](#인수--0이-최선이라는-서열) 절에 달아 둔
  `#hypothesis`("인수를 인스턴스 변수로 옮기는 것은 인터페이스의 형식적 부분을 줄이는
  대신 비형식적 부분을 늘린다")를 이 비판이 실물로 확인한다 — **메서드가 다른 메서드에
  인수를 넘기게 하는 대신, 마틴은 첫 메서드가 멤버 변수를 설정하고 둘째 메서드가 그것을
  되읽는 습관을 들인다** (§1).[^qntm2020] 그 귀결로 **이 메서드는 단위 테스트할 수 없다.
  그것은 단위가 아니다** (§1).[^qntm2020]
- 위 [한 가지만 하라](#한-가지만-하라--조작적-정의) 절의 추출 검사도 대질된다 — 이 장이
  세운 검사("구현의 재진술이 아닌 이름")를 인용한 뒤, 그 결과물인 `isTestPage()`처럼
  본문 한 줄짜리 메서드 여럿이 **어느 것도 한 자리보다 많은 곳에서 호출되지 않는다**고
  적는다 (§1).[^qntm2020]
- **이 비판은 이 페이지의 모순 판정을 바꾸지 않는다.** 2차 문헌이므로 원전과 같은 물음에
  다른 답을 하는 것이 아니라 원전을 평가한다. 전문과 이 KB가 그것을 쓰는 방식은
  [클린 코드 비판](clean-code-criticism.md)에 있다.

## 저자 본인이 나중에 좁힌 것

> **버전 조건**: 이 페이지는 *Clean Code* **초판(2008)** 기준이다. 저자가 2판에서 메서드
> 길이 지침의 균형을 조정했다고 밝혔으므로, **분해를 어디서 멈출 것인가에 관한 이
> 페이지의 claim은 2판에 그대로 적용된다고 볼 수 없다.** 2판은 이 KB에 아직 반입돼
> 있지 않다.

2024년 9월부터 2025년 2월 사이에 두 저자가 공개 대담을 했고, 그 자리에서 저자가 이 장의
주장을 세 자리에서 좁혔다. 전문은 [오스터하우트–마틴 공개 대담](aposd-vs-clean-code-dialogue.md)에
있고, 여기서는 이 페이지의 어느 절이 영향을 받는지만 적는다.

- **위 [얼마나 작은가 — 수치](#얼마나-작은가--수치) 절에 대해** — 저자는 그 수치가 규정이
  아니었다고 말한다 (§"Method Length", UB 발언):[^ousterhout2024-aposd]

> While I do strongly recommend very short functions, I don't think it's fair to say that
> the book sets arbitrary numerical limits. The 2-4 line functions that you referred to on
> page 34 were part of the _Sparkle_ applet that Kent Beck and I wrote together in 1999 as
> an exercise for learning TDD.

  - **이 페이지의 기록과 어긋나지 않는다** — 위 절이 그 대목을 이미 일화로 적었다.
    **다만 "함수가 20줄인 경우도 거의 없어야 한다"(p.34)와 "블록은 한 줄"(p.35)은 일화가
    아니라 서술문이고, 저자는 그 둘에 대해서는 해명하지 않았다.**
- **위 [한 가지만 하라](#한-가지만-하라--조작적-정의) 절에 대해** — 저자는 과잉 분해가
  가능함을 인정하고, `void doSomething() {doTheThing()}`을 그 예로 든다. 그리고 책에
  판단 지침이 부족하다는 것을 인정한다 (§"Method Length", UB 발언):[^ousterhout2024-aposd]

> You make a good point that I don't talk much, in the book, about how to make the
> judgement call. Back in 2008 my concern was breaking the habit of the very large
> functions that were common in those early days of the web. I have been more balanced in
> the 2d ed.

- **그러나 기본값은 바뀌지 않았다** — **그래도 틀려야 한다면 나는 분해하는 쪽으로
  틀리겠다** (§"Method Length", UB 발언).[^ousterhout2024-aposd] **아래 모순 절이
  해소되지 않는 이유가 이 한 문장이다.**
- **저자가 자기 예제의 난독성도 인정한다** — `PrimeGenerator`를 두고 **며칠 전 그
  알고리즘으로 처음 돌아왔을 때 나는 그 이름들과 구조와 씨름했다**고 적는다
  (§"Method Length", UB 발언).[^ousterhout2024-aposd]

## 모순 — 함수를 쪼개면 복잡성이 주는가

이 KB에서 **`contradicts`가 발화한 둘째 자리다.** 상대는
[깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)이고, 갈리는 명제는 하나다 —
**이름 붙일 수 있는 블록을 함수로 뽑는 조작이 시스템 복잡성을 줄이는가 늘리는가.**

- **이 페이지의 주장.** ① 함수는 스무 줄이면 거의 언제나 너무 길다 ② 제어문 안쪽 블록은
  한 줄이어야 하고 그 한 줄은 함수 호출이어야 한다 ③ 들여쓰기는 한두 단계를 넘지 않는다
  ④ 판정 검사는 **"구현의 재진술이 아닌 이름으로 또 다른 함수를 뽑아낼 수 있는가"**다
  (3장, pp.34–36).[^martin2008]
- **상대 쪽의 주장.** 상대는 이 규칙을 명시적으로 인용해 기각한다 — **프로그래밍의
  통념은 클래스가 깊어야 한다가 아니라 작아야 한다는 것이다. … 메서드에 대해서도 같은
  조언이 흔히 주어진다: "N줄보다 긴 메서드는 여러 메서드로 나눠야 한다"(N은 10만큼 낮을
  수도 있다). 이 접근은 다수의 얕은 클래스와 메서드를 낳고, 그것이 전체 시스템 복잡성에
  더해진다** (4장 §4.6, p.26).[^ousterhout2021] 그리고 붉은 깃발로 조문화한다
  (4장 §4.5, p.25):[^ousterhout2021]

> A shallow module is one whose interface is complicated relative to the functionality
> it provides. Shallow modules don't help much in the battle against complexity, because
> the benefit they provide (not having to learn about how they work internally) is
> negated by the cost of learning and using their interfaces. Small modules tend to be
> shallow.

- **한쪽의 처방이 다른 쪽의 반례와 같은 모양이다.** 상대가 최악의 실물로 드는 메서드는
  본문이 `data.put(attribute, null);` **한 줄**인
  `addNullValueForAttribute(String attribute)`이고, 판정은 **복잡성 관리의 관점에서 이
  메서드는 상황을 나아지게 하는 것이 아니라 나쁘게 만든다**이다 (4장 §4.5,
  p.25).[^ousterhout2021] 이 페이지의 ②는 정확히 그런 한 줄짜리 함수를 만들라는 지시다.
- **층위 차이로 무마할 수 없는 이유 셋.**
  - **같은 모집단이다.** 둘 다 객체 지향 언어의 메서드를 말하고, 상대는 자바 클래스
    라이브러리를, 이 페이지는 자바 예제를 든다. 한쪽이 함수를, 다른 쪽이 서비스를
    말하는 것이 아니다.
  - **상대가 이 명제를 인용해 기각한다.** "N줄 규칙"을 인용부호로 옮겨 놓고 그 결과를
    복잡성 증가로 계산한다. 다른 것을 겨냥한 것이 아니다.
  - **판정 방향이 반대다.** 이 페이지의 검사는 "더 뽑아낼 수 있으면 아직 크다"이고,
    상대의 검사는 "인터페이스가 기능에 비해 크면 이미 얕다"이다. 같은 조작에 대해 한쪽은
    개선, 다른 쪽은 악화로 채점한다.
- **겹치는 구간은 인정한다.** 둘 다 ⓐ 추상화 수준이 섞이는 것을 결함으로 보고
  (이 페이지의 "함수당 추상화 수준 하나" ↔ 상대의
  [계층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md))
  ⓑ 좋은 이름이 중요하다고 보며 ⓒ 인수를 줄이라고 한다. 그래서 모순은 위 한 명제로
  좁혀진다.
- **해소하지 않는다.** 최신성만으로 판단하지 않는다 — 상대가 13년 뒤 책이지만 그것이
  근거가 되지 않는다. 양쪽 페이지에 `contradicts`를 달아 두고, 해소는 사람이 근거와
  날짜를 남기며 한다.
- **두 저자가 이 쟁점으로 직접 맞붙은 문서가 이 KB에 있다.** 이 페이지가 대질하는 두
  명제는 추론이 아니라 두 저자가 서로에게 실제로 제기한 것이고, 두 사람이 그것을 자기들의
  불합의 목록으로 조문화했다 — [오스터하우트–마틴 공개 대담](aposd-vs-clean-code-dialogue.md).
  그 자리에서 마틴이 내린 최종 진단이 **분해와 얽힘이라는 두 값의 상대적 가중치에 대한
  불일치**다 (§"Method Length Summary", UB 발언).[^ousterhout2024-aposd] 잣대가 달라서가
  아니라 같은 잣대에 반대 가중치를 걸어서 갈린다 — 층위 차이로 무마할 수 없는 이유가
  양측 진술로 확인된다.

## 이어지는 페이지

- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — **`contradicts` 상대.** 쪼개면
  얕아진다는 쪽
- [오스터하우트–마틴 공개 대담](aposd-vs-clean-code-dialogue.md) — **이 모순의 1차 사료.**
  저자가 이 장의 주장을 세 자리에서 좁힌 자리
- [클린 코드 비판](clean-code-criticism.md) — 이 장의 예제를 이 장의 규칙과 대질하는 2차 문헌
- [주석은 실패다](comments-as-failure.md) — 같은 소스의 다음 장. "긴 이름이 긴 주석보다
  낫다"가 거기서 "주석은 실패다"가 된다
- [객체와 자료 구조](objects-versus-data-structures.md) — 같은 소스 6장. 이 장의
  `switch` 처방과 저자 스스로 인정하는 긴장이 있는 자리
- [클린 코드의 발견법 목록](clean-code-heuristics.md) — 이 장의 규칙들이 식별자로
  압축돼 다시 실리는 자리(`F1`–`F3`·`G15`·`G30`·`G31`·`G34`)
- [DRY 원칙](dry-principle.md) — "중복은 만악의 근원"이라는 최대주의가 놓이는 축
- [이름 짓기](naming-things.md) — 이 장이 서술적 이름에 거는 무게가 다른 두 소스와
  만나는 자리
- [리팩터링](refactoring.md) — 이 장의 규칙이 작성 규칙이 아니라 도착 상태임을 저자가
  밝힌 뒤 남는 절차 층
- [자기 테스트 코드](self-testing-code.md) — 그 이행의 담보
- [시간적 결합을 깨기](../concepts/breaking-temporal-coupling.md) — 부수 효과 절과
  `G31`이 만나는 실용주의 쪽 자리
- [코드의 나쁜 냄새](code-smells.md) — 긴 함수를 냄새로 다루는 셋째 소스
- [클린 코드](../synthesis/clean-code.md) — 이 소스의 허브

[^ousterhout2024-aposd]: Ousterhout & Martin 2024, "A Philosophy of Software Design
    vs Clean Code". **대담이므로 locator에 발언자를 함께 적는다** — `JOHN`은 John
    Ousterhout, `UB`는 Robert C. Martin이다. 규약과 스냅샷 취득 경로는
    `it/archive/ousterhout2024-aposd/_progress.yaml` 머리말이 정본이다.

[^qntm2020]: qntm 2020, "It's probably time to stop recommending Clean Code".
    **절 번호는 이 KB가 매긴 것이다** — 규약은
    `it/archive/qntm2020/_progress.yaml` 머리말이 정본이다.

[^martin2008]: Martin 2008, 3장 "Functions"(§"Small!" pp.34–35 · §"Blocks and
    Indenting" p.35 · §"Do One Thing" pp.35–36 · §"Sections within Functions" p.36 ·
    §"One Level of Abstraction per Function" pp.36–37 · §"Reading Code from Top to
    Bottom" p.37 · §"Switch Statements" pp.37–39 · §"Use Descriptive Names" pp.39–40 ·
    §"Function Arguments" pp.40–41 · §"Flag Arguments" p.41 · §"Argument Objects" p.43 ·
    §"Have No Side Effects" p.44 · §"Output Arguments" p.45 · §"Command Query
    Separation" pp.45–46 · §"Prefer Exceptions to Returning Error Codes" p.46 ·
    §"Extract Try/Catch Blocks" p.46 · §"Error Handling Is One Thing" p.47 · §"The
    Error.java Dependency Magnet" pp.47–48 · §"Don't Repeat Yourself" p.48 ·
    §"Structured Programming" p.49 · §"How Do You Write Functions Like This?" p.49) ·
    17장 `G5`(pp.289–290) · `G15`(p.295) · `G31`(pp.302–303). 쪽은 인쇄판 쪽 번호이며
    복원 절차는 `it/archive/martin2008/_progress.yaml` 머리말이 정본이다. 이 장에는
    Listing 3-1부터 3-7까지 일곱 개의 코드 리스팅이 있으나 이 페이지에는 펜스로 옮기지
    않았다 — 전부 FitNesse의 문맥에 묶인 예제라 복사해 돌아가지 않는다(SCHEMA §3의
    펜스 조건). 인용한 식별자와 시그니처는 인라인 백틱으로 옮겼다. 도판은 없다.

[^ousterhout2021]: Ousterhout 2021, 4장 "Modules Should Be Deep" §4.5(p.25)·§4.6(p.26).
    쪽은 인쇄판 쪽 번호.

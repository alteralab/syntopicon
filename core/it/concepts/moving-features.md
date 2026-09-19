---
type: concept
title: 기능 이동 리팩터링
description: 요소를 맥락 사이로 옮기는 아홉 항목 — 함수 옮기기가 왜 판단이 어려우면서도 그만큼 덜 중요한가, 필드 옮기기가 자료 구조의 초기 설계 실수를 인정하는 절차라는 규정, 문장을 함수 안팎으로 옮기는 두 항목과 함수 안에서 미끄러뜨리는 항목, 인라인 코드를 함수 호출로 바꿀 때의 판정 기준, 반복문을 쪼개고 파이프라인으로 대체하는 두 항목과 그때 나오는 리팩터링과 최적화의 분리, 그리고 죽은 코드를 지우는 근거
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 기능 이동 리팩터링

- [이 장이 묶는 축](#이-장이-묶는-축)
- [Move Function — 판단이 어려울수록 덜 중요하다](#move-function--판단이-어려울수록-덜-중요하다)
- [Move Field — 자료 구조의 초기 설계는 틀린다](#move-field--자료-구조의-초기-설계는-틀린다)
- [문장을 옮기는 세 항목](#문장을-옮기는-세-항목)
- [Replace Inline Code with Function Call — 이름이 판정 기준이다](#replace-inline-code-with-function-call--이름이-판정-기준이다)
- [반복문을 다루는 두 항목](#반복문을-다루는-두-항목)
- [Remove Dead Code — 무게가 아니라 부담](#remove-dead-code--무게가-아니라-부담)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프로그램 요소를 어느 맥락에 둘 것인가, 그리고 자리를 옮기는 안전한 수순은
무엇인가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축

- 앞 장들과의 차이를 저자가 밝힌다 — **지금까지 리팩터링은 프로그램 요소를 만들고 없애고 이름을
  바꾸는 것에 대한 것이었다. 리팩터링의 또 다른 중요한 부분은 요소를 맥락 사이로 옮기는
  것이다** (8장, p.197).[^fowler2018]
- 층위가 셋이다 (8장, p.197):[^fowler2018] **함수와 필드**를 클래스·모듈 사이로
  (*Move Function*(p.198)·*Move Field*(p.207)), **개별 문장**을 함수 안팎으로
  (*Move Statements into Function*(p.213)·*Move Statements to Callers*(p.217)) 그리고 함수
  안에서 (*Slide Statements*(p.223)), 나아가 기존 함수와 맞는 문장은
  *Replace Inline Code with Function Call*(p.222)로 중복을 없앤다.
- 반복문 둘과 마무리 하나가 따로 붙는다 — **반복문을 두고 자주 하는 리팩터링이 둘 있다.
  반복문이 한 가지만 하도록 보장하는 *Split Loop*(p.227)와 반복문을 통째로 없애는
  *Replace Loop with Pipeline*(p.231)이다. 그리고 많은 훌륭한 프로그래머가 가장 좋아하는
  리팩터링이 있다 — *Remove Dead Code*(p.237). 군더더기 문장에 디지털 화염방사기를 들이대는
  것만큼 만족스러운 일은 없다** (8장, p.197).[^fowler2018]

## Move Function — 판단이 어려울수록 덜 중요하다

- 이 항목의 근거가 모듈성의 조작적 정의로 시작한다 (8장 §"Move Function",
  p.198):[^fowler2018]

> The heart of a good software design is its modularity—which is my ability to make most
> modifications to a program while only having to understand a small part of it.

  - 그리고 옮김이 필요한 이유가 그 정의에서 따라 나온다 — **이 모듈성을 얻으려면 관련 있는
    소프트웨어 요소가 함께 묶이고 그것들 사이의 연결이 찾고 이해하기 쉬워야 한다. 그러나 이것을
    어떻게 하는지에 대한 내 이해는 고정돼 있지 않다 — 내가 하는 일을 더 잘 이해할수록 소프트웨어
    요소를 어떻게 가장 잘 묶을지 배운다. 그 자라는 이해를 반영하려면 요소를 옮겨야 한다** (8장
    §"Move Function", p.198).[^fowler2018]
- 옮길 계기 넷 (8장 §"Move Function", p.198):[^fowler2018]
  - **가장 직접적인 이유는 함수가 지금 있는 맥락보다 다른 맥락의 요소를 더 많이 참조할 때다.**
    그 요소들과 함께 옮기면 흔히 캡슐화가 개선된다.
  - **호출자가 어디 있는가**, 또는 다음 기능 확장에서 어디서 부를 필요가 있는가.
  - 다른 함수 안의 도우미로 정의된 함수가 그 자체로 값이 있을 때 — 더 접근하기 좋은 자리로.
  - 클래스의 메서드가 다른 클래스로 옮기면 쓰기 쉬워질 때.
- **판단은 쉽지 않다고 인정한다** — **함수를 옮기기로 결정하는 것은 좀처럼 쉬운 결정이 아니다.
  결정을 돕기 위해 나는 그 함수의 현재 맥락과 후보 맥락을 살펴본다. 어느 함수가 이것을 부르는지,
  이 함수가 어느 함수를 부르는지, 그리고 그 함수가 어떤 데이터를 쓰는지 봐야 한다** (8장
  §"Move Function", p.199).[^fowler2018] 그 과정에서 **함수 무리를 위한 새 맥락이 필요하다는
  것을 알게 되어 *Combine Functions into Class*(p.144)나 *Extract Class*(p.182)로 하나를
  만드는 일이 잦다.**
- **그리고 이 항목의 핵심 판정이 온다** (8장 §"Move Function", p.199):[^fowler2018]

> Although it can be difficult to decide where the best place for a function is, the more
> difficult this choice, often the less it matters. I find it valuable to try working with
> functions in one context, knowing I'll learn how well they fit, and if they don't fit I
> can always move them later.

  - 이 한 문단이 카탈로그 전체가 서 있는 태도다 — **되돌릴 수 있으므로 완벽한 선택이 필요
    없다.** 같은 태도가 *Hide Delegate*와 *Remove Middle Man*의 쌍에도 명시돼 있다 —
    [캡슐화 리팩터링](../concepts/encapsulation-refactorings.md) 참조.
- 수순의 요지 (8장 §"Move Function", pp.199–200):[^fowler2018]
  1. **현재 맥락에서 그 함수가 쓰는 프로그램 요소를 전부 살펴 함께 옮겨야 하는지 검토한다.**
     함께 옮겨야 할 피호출 함수가 있으면 **보통 그것을 먼저 옮긴다** — 그래야 무리 안에서 다른
     것에 대한 의존이 가장 적은 것부터 시작하게 된다.
  2. 다형 메서드인지 확인한다 — 객체지향 언어면 상위·하위 클래스 선언을 고려해야 한다.
  3. 함수를 대상 맥락에 복사하고 새 집에 맞게 조정한다. **본문이 원래 맥락의 요소를 쓰면 그것을
     매개변수로 넘기거나 원래 맥락에 대한 참조를 넘겨야 한다.** 그리고 **함수를 옮기면 흔히 새
     맥락에서 더 잘 통하는 다른 이름이 필요해진다.**
  4. 원래 함수를 위임 함수로 바꾸고 테스트한 뒤 *Inline Function*(p.115)을 검토한다.
     **원래 함수는 위임 함수로 무기한 남아 있어도 된다. 그러나 호출자가 대상에 직접 닿을 수도
     있다면 중개자를 없애는 편이 낫다.**
- 3장이 기능 편애(Feature Envy)·발산하는 변경·산탄총 수술의 처방으로 이 항목을 지목한다 —
  [코드의 나쁜 냄새](../concepts/code-smells.md) 참조.

## Move Field — 자료 구조의 초기 설계는 틀린다

- 데이터가 행동보다 앞선다는 판정이 근거다 — **프로그래밍은 행동을 구현하는 코드를 많이 쓰는
  일이지만 프로그램의 힘은 실은 그 자료 구조 위에 세워진다. 문제에 맞는 좋은 자료 구조 집합이
  있으면 내 행동 코드는 단순하고 직선적이다. 그러나 나쁜 자료 구조는 그 나쁜 데이터를 다루는
  것이 유일한 일인 코드를 많이 낳는다** (8장 §"Move Field", p.207).[^fowler2018] 그리고 비용이
  코드 지저분함에 그치지 않는다 — **자료 구조가 프로그램이 무엇을 하는지 흐리게 만든다는
  뜻이기도 하다.**
- **초기 설계가 틀린다는 것을 저자가 자기 사례로 인정한다** — **최선의 자료 구조를 알아내려고
  초기 분석을 하고, 경험과 도메인 주도 설계 같은 기법이 그 능력을 개선했다. 그러나 내 모든
  솜씨와 경험에도 불구하고 나는 여전히 그 초기 설계에서 자주 실수한다** (8장 §"Move Field",
  p.207).[^fowler2018] 그래서 처방의 시급성이 붙는다 — **자료 구조가 옳지 않다고 깨닫는 즉시
  그것을 바꾸는 것이 중요하다. 자료 구조에 흠집을 남겨 두면 그 흠집이 내 사고를 혼란스럽게
  하고 먼 미래까지 코드를 복잡하게 만든다.**
- 옮길 신호 셋 (8장 §"Move Field", pp.207–208):[^fowler2018]
  - **한 레코드를 함수에 넘길 때마다 다른 레코드의 필드도 늘 함께 넘겨야 할 때** — 함께 넘어가는
    데이터 조각은 보통 관계를 분명히 하려고 한 레코드에 두는 편이 낫다.
  - **한 레코드의 변경이 다른 레코드의 필드도 바뀌게 할 때** — 그것이 필드가 잘못된 자리에 있다는
    신호다.
  - **같은 필드를 여러 구조에서 갱신해야 할 때** — 한 번만 갱신하면 되는 자리로 옮겨야 한다는
    신호다.
- **단독으로 하는 리팩터링이 아니라고 명시한다** — **나는 보통 더 넓은 변경 묶음의 맥락에서
  Move Field를 한다. 필드를 옮기고 나면 그 필드의 사용자 다수가 원래 원본이 아니라 대상 객체를
  통해 그 데이터에 접근하는 편이 낫다는 것을 알게 된다.** 반대로 **데이터가 쓰이는 방식 때문에
  지금은 Move Field를 할 수 없어 사용 패턴을 먼저 리팩터링해야 하는 경우도 있다** (8장
  §"Move Field", p.208).[^fowler2018]
- **캡슐화가 있으면 훨씬 쉽다** — 클래스는 함수가 붙은 레코드 타입이고, **붙은 함수가 데이터를
  옮기기 쉽게 만드는데, 데이터가 접근자 메서드 뒤에 캡슐화돼 있기 때문이다. 데이터를 옮기고
  접근자를 바꾸면 접근자의 클라이언트는 여전히 동작한다. 그래서 이것은 클래스가 있으면 하기 더
  쉬운 리팩터링이고 (…) 캡슐화를 지원하지 않는 맨 레코드로도 할 수는 있지만 더 까다롭다** (8장
  §"Move Field", p.208).[^fowler2018]

## 문장을 옮기는 세 항목

- **Move Statements into Function**(p.213) — 계기가 중복이다 — **중복 제거는 건강한 코드의
  가장 좋은 경험칙 중 하나다. 특정 함수를 부를 때마다 같은 코드가 실행되는 것을 보면 그
  반복되는 코드를 함수 자체에 합칠 방법을 찾는다** (8장 §"Move Statements into Function",
  p.213).[^fowler2018] 되돌릴 수 있다는 단서가 곧바로 붙는다 — **나중에 코드가 달라져야 하면
  *Move Statements to Callers*(p.217)로 (일부를) 다시 밖으로 옮기면 된다.**
  - **판정 기준이 이해 단위다** — **나는 그 문장들을 불리는 함수의 일부로 가장 잘 이해할 수 있을
    때 함수 안으로 옮긴다. 불리는 함수의 일부로는 말이 안 되지만 그래도 함께 불려야 한다면
    그냥 그 문장들과 불리는 함수에 *Extract Function*(p.106)을 쓴다** (8장 §"Move Statements
    into Function", p.214).[^fowler2018]
- **Move Statements to Callers**(p.217) — 그 역이고, 계기가 추상 경계의 이동이다 — **함수는
  프로그래머로서 우리가 세우는 추상의 기본 구성 요소다. 그리고 어떤 추상이든 그렇듯 우리가 늘
  경계를 옳게 잡는 것은 아니다. 코드베이스가 능력을 바꿔 가면서 — 유용한 소프트웨어는 대부분
  그렇다 — 우리는 추상 경계가 이동하는 것을 자주 본다. 함수의 경우 그것은 한때 응집된 원자적
  행동 단위였던 것이 둘 이상의 다른 것의 혼합이 된다는 뜻이다** (8장 §"Move Statements to
  Callers", p.217).[^fowler2018]
  - **적용 한계가 명시된다** — **Move Statements to Callers는 작은 변경에는 잘 통하지만 때로는
    호출자와 피호출자 사이의 경계를 완전히 다시 짜야 한다. 그런 경우 내 최선의 수는
    *Inline Function*(p.115)을 쓴 다음 미끄러뜨리고 새 함수를 추출해 더 나은 경계를 만드는
    것이다** (8장 §"Move Statements to Callers", p.218).[^fowler2018]
- **Slide Statements**(p.223, 초판 이름 *Consolidate Duplicate Conditional Fragments*) —
  같은 함수 안에서 문장을 모은다. 근거가 한 줄이다 — **서로 관련된 것들이 함께 나타날 때 코드는
  이해하기 쉽다. 여러 줄이 같은 자료 구조에 접근한다면 다른 자료 구조에 접근하는 코드와
  뒤섞이는 것보다 함께 있는 편이 낫다** (8장 §"Slide Statements", p.223).[^fowler2018]
  - **저자의 취향 하나가 명시된다** — 변수 선언에 대해 — **어떤 사람들은 모든 변수를 함수 맨 위에
    선언하기를 좋아한다. 나는 처음 쓰기 직전에 변수를 선언하는 편을 선호한다** (8장 §"Slide
    Statements", p.223).[^fowler2018]
  - **주된 쓰임새는 준비 단계다** — **나는 보통 다른 리팩터링, 흔히 *Extract Function*(p.106)의
    준비 단계로 관련 코드를 함께 옮긴다. 관련 코드를 명확히 분리된 함수에 넣는 것이 단지 몇 줄을
    함께 옮기는 것보다 나은 분리지만, 코드가 애초에 함께 있지 않으면 추출을 할 수 없다** (8장
    §"Slide Statements", p.223).[^fowler2018] 5장이 이 항목을 초판에서 뺐다가 2판에서 넣은
    판정 번복 사례로 든다 — [리팩터링 카탈로그를 읽는 법](refactoring-catalog-format.md) 참조.

## Replace Inline Code with Function Call — 이름이 판정 기준이다

- 함수의 두 이득이 근거다 — **이해**(**이름 붙은 함수는 코드의 기제가 아니라 목적을 설명할 수
  있다**)와 **중복 제거**(같은 코드를 두 번 쓰는 대신 함수를 부른다) (8장 §"Replace Inline Code
  with Function Call", p.222).[^fowler2018]
- **적용하지 말아야 할 경우가 먼저 명시된다** — **예외는 그 유사성이 우연이라고 보는 경우다 —
  함수 본문을 바꿨을 때 이 인라인 코드의 행동이 바뀌기를 기대하지 않는 경우다** (8장 §"Replace
  Inline Code with Function Call", p.222).[^fowler2018]
- **판정 기준이 함수 이름이다** (8장 §"Replace Inline Code with Function Call",
  p.222):[^fowler2018]

> A guide to this is the name of the function. A good name should make sense in place of
> inline code I have. If the name doesn't make sense, that may be because it's a poor name
> (in which case I use *Rename Function (124)* to fix it) or because the function's
> purpose is different to what I want in this case—so I shouldn't call it.

  - 그리고 저자가 가장 만족스럽다고 적는 경우가 **라이브러리 함수 호출로 바꾸는 것이다 — 그러면
    함수 본문을 쓸 필요조차 없다** (8장 §"Replace Inline Code with Function Call",
    p.222).[^fowler2018]

## 반복문을 다루는 두 항목

- **Split Loop**(p.227) — **한 번의 순회로 할 수 있다는 이유만으로 두 가지를 동시에 하는
  반복문을 자주 본다. 그러나 같은 반복문에서 두 가지를 하고 있으면 반복문을 수정해야 할 때마다
  둘 다 이해해야 한다. 반복문을 쪼개면 수정해야 할 행동만 이해하면 된다** (8장 §"Split Loop",
  pp.227–228).[^fowler2018]
  - 부수 이득 — **값 하나를 계산하는 반복문은 그 값을 반환하면 그만이다. 여러 가지를 하는
    반복문은 구조를 반환하거나 지역 변수를 채워야 한다** (8장 §"Split Loop",
    p.228).[^fowler2018] 그리고 저자는 **Split Loop 뒤에 *Extract Function*(p.106)을 잇는
    순서를 자주 따른다.**
  - **성능 반론에 대한 답이 명시된다** (8장 §"Split Loop", p.228):[^fowler2018]

> Many programmers are uncomfortable with this refactoring, as it forces you to execute
> the loop twice. My reminder, as usual, is to separate refactoring from optimization
> (*Refactoring and Performance (64)*). Once I have my code clear, I'll optimize it, and
> if the loop traversal is a bottleneck, it's easy to slam the loops back together. But
> the actual iteration through even a large list is rarely a bottleneck, and splitting
> the loops often enables other, more powerful, optimizations.

  - 그 2장 절의 전문은 [성능을 위한 설계](../concepts/designing-for-performance.md)에 있다.
- **Replace Loop with Pipeline**(p.231) — **대부분의 프로그래머처럼 나도 객체 컬렉션을 순회하는
  데 반복문을 쓰라고 배웠다. 그러나 점점 언어 환경이 더 나은 구성물을 제공한다: 컬렉션
  파이프라인이다** (8장 §"Replace Loop with Pipeline", p.231).[^fowler2018]
  - 두 주요 연산이 지목된다 — **`map`은 함수를 써서 입력 컬렉션의 각 원소를 변환하고, `filter`는
    함수를 써서 파이프라인의 이후 단계를 위해 입력 컬렉션의 부분집합을 고른다** (8장 §"Replace
    Loop with Pipeline", p.231).[^fowler2018]
  - 이득이 읽기 방향이다 — **파이프라인으로 표현되면 로직을 따라가기가 훨씬 쉽다. 위에서
    아래로 읽어 객체가 파이프라인을 어떻게 흘러가는지 볼 수 있다** (8장 §"Replace Loop with
    Pipeline", p.231).[^fowler2018]
  - 버전 조건: 일급 함수와 컬렉션 파이프라인을 지원하는 언어 환경에 한정된다. 3장의 반복문
    냄새가 초판 시점에는 이 처방이 불가능했다고 명시한다 —
    [코드의 나쁜 냄새](../concepts/code-smells.md) 참조.

## Remove Dead Code — 무게가 아니라 부담

- 비용의 정체를 먼저 정정한다 — **코드를 운영에 올릴 때, 사람들 기기에 올릴 때조차 우리는 무게로
  요금을 물지 않는다. 쓰이지 않는 몇 줄이 시스템을 느리게 하지도 유의미한 메모리를 차지하지도
  않는다. 실제로 괜찮은 컴파일러는 본능적으로 그것을 제거한다** (8장 §"Remove Dead Code",
  p.237).[^fowler2018]
- **진짜 비용은 읽는 사람의 시간이다** (8장 §"Remove Dead Code", p.237):[^fowler2018]

> But unused code is still a significant burden when trying to understand how the software
> works. It doesn't carry any warning signs telling programmers that they can ignore this
> function as it's never called any more, so they still have to spend time understanding
> what it's doing and why changing it doesn't seem to alter the output as they expected.

- **버전 관리가 안전망이라는 논증** — **나중에 필요할지 모른다고 걱정하지 않는다. 그런 일이
  생기면 버전 관리 시스템이 있으니 언제든 다시 파낼 수 있다** (8장 §"Remove Dead Code",
  p.237).[^fowler2018] 그리고 자기 실천으로 그 걱정을 다시 깎는다 — 잃은 코드와 그것이 제거된
  리비전을 주석으로 남길 수도 있지만 **솔직히 마지막으로 그렇게 한 때도, 그렇게 하지 않아서
  후회한 때도 기억나지 않는다.**
- **주석 처리 습관은 시대 조건으로 은퇴시킨다** — **죽은 코드를 주석 처리하는 것은 한때 흔한
  습관이었다. 이것은 버전 관리 시스템이 널리 쓰이기 전이나 불편했던 시절에 유용했다. 2018년 저술 시점에는
  아주 작은 코드베이스도 버전 관리에 넣을 수 있으므로 더는 필요하지 않다** (8장 §"Remove Dead
  Code", p.237).[^fowler2018] 같은 대상의 판정은
  [버전 관리 실천](version-control-practice.md)에 있다.
- 3장의 추측성 일반화(Speculative Generality)가 이 항목을 처방으로 지목하고, 탐지 신호로
  **유일한 사용자가 테스트 케이스인 경우**를 든다 — [코드의 나쁜 냄새](../concepts/code-smells.md) 참조.

## 이어지는 페이지

- [캡슐화 리팩터링](../concepts/encapsulation-refactorings.md) — 앞 장(7장). *Extract Class*가 이 장의
  *Move Field*·*Move Function*을 부품으로 쓴다
- [데이터 조직화 리팩터링](organizing-data.md) — 다음 장(9장)
- [기본 리팩터링](../concepts/basic-refactorings.md) — *Extract Function*·*Combine Functions into Class*의 정본
- [코드의 나쁜 냄새](../concepts/code-smells.md) — 기능 편애·산탄총 수술·발산하는 변경이 이 장을 지목한다
- [직교성](orthogonality.md) — 요소를 어디에 둘지의 판정을 성질 쪽에서 재는 자리
- [성능을 위한 설계](../concepts/designing-for-performance.md) — 반복문을 두 번 도는 것에 대한 답의 전문
- [버전 관리 실천](version-control-practice.md) — 죽은 코드를 지울 수 있게 하는 안전망
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 8장 "Moving Features"(pp.197–238). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 22).
    직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준 규약이며 근거는
    `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example 절과 스케치 도판은
    옮기지 않았다. §"Slide Statements"와 §"Replace Loop with Pipeline"의 Further Reading은
    서지라 옮기지 않았다.

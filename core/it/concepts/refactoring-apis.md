---
type: concept
title: API 리팩터링
description: 모듈을 잇는 관절을 고치는 열 항목 — 질의와 변경자를 가르는 명령-질의 분리와 관찰 가능한 부작용이라는 단서, 플래그 인수를 싫어하는 이유와 그것이 플래그 인수인지 판정하는 두 조건, 통째 객체를 넘길 때와 넘기지 말아야 할 때, 매개변수와 질의 사이를 오가는 두 항목이 참조 투명성을 두고 벌이는 절충, 세터를 없애 불변으로 가는 항목, 생성자를 팩터리 함수로 바꾸는 근거인 생성자의 세 제약, 그리고 함수를 명령 객체로 바꿀 때의 대가
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# API 리팩터링

- [이 장이 묶는 축 — API는 관절이다](#이-장이-묶는-축--api는-관절이다)
- [Separate Query from Modifier — 관찰 가능한 부작용](#separate-query-from-modifier--관찰-가능한-부작용)
- [Parameterize Function과 Remove Flag Argument](#parameterize-function과-remove-flag-argument)
- [Preserve Whole Object — 통째로 넘기기](#preserve-whole-object--통째로-넘기기)
- [매개변수와 질의 사이 — 참조 투명성을 두고 벌이는 절충](#매개변수와-질의-사이--참조-투명성을-두고-벌이는-절충)
- [Remove Setting Method — 불변으로 가는 길](#remove-setting-method--불변으로-가는-길)
- [Replace Constructor with Factory Function — 생성자의 세 제약](#replace-constructor-with-factory-function--생성자의-세-제약)
- [Replace Function with Command과 그 역](#replace-function-with-command과-그-역)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모듈을 잇는 인터페이스를 이해하고 쓰기 쉽게 만드는 수순은 무엇인가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축 — API는 관절이다

- 장의 전제 (11장, p.305):[^fowler2018]

> Modules and their functions are the building blocks of our software. APIs are the joints
> that we use to plug them together. Making these APIs easy to understand and use is
> important but also difficult: I need to refactor them as I learn how to improve them.

  - 같은 관절 비유가 6장 *Change Function Declaration*의 근거이기도 하다 —
    [기본 리팩터링](../concepts/basic-refactorings.md) 참조.
- 배열 (11장, p.305):[^fowler2018] **좋은 API는 데이터를 갱신하는 함수와 읽기만 하는 함수를
  명확히 가른다** → *Separate Query from Modifier*(p.306). 값 하나 때문에만 갈리는 함수는
  *Parameterize Function*(p.310)으로 합치되, **어떤 매개변수는 실은 완전히 다른 행동의
  신호이므로 잘라 내는 편이 낫다** → *Remove Flag Argument*(p.314). 자료 구조가 함수 사이를
  오가며 불필요하게 풀리면 *Preserve Whole Object*(p.319)로 함께 둔다. 무엇을 매개변수로
  넘기고 무엇을 피호출 함수가 스스로 구하게 할지는 *Replace Parameter with Query*(p.324)와
  *Replace Query with Parameter*(p.327)로 다시 손본다. **객체를 가능한 한 불변으로 두기를
  선호하므로** *Remove Setting Method*(p.331)를 가능할 때마다 쓰고, 단순 생성자보다 유연성이
  필요하면 *Replace Constructor with Factory Function*(p.334)을 쓴다. 마지막 두 항목은
  데이터를 많이 주고받는 복잡한 함수를 쪼개는 어려움을 겨냥한다 —
  *Replace Function with Command*(p.337)과 그 역 *Replace Command with Function*(p.344).

## Separate Query from Modifier — 관찰 가능한 부작용

- 부작용 없는 함수의 가치가 먼저 나열된다 — **값을 주면서 관찰 가능한 부작용이 없는 함수를
  가지면 나는 아주 값진 것을 갖는다. 그 함수를 원하는 만큼 자주 부를 수 있다. 호출을 호출하는
  함수의 다른 자리로 옮길 수 있다. 테스트하기 더 쉽다. 요컨대 걱정할 것이 훨씬 적다** (11장
  §"Separate Query from Modifier", p.306).[^fowler2018]
- 규칙과 그에 대한 저자의 온도가 함께 적힌다 — **따를 만한 좋은 규칙은 값을 반환하는 함수는
  어떤 것도 관찰 가능한 부작용을 가져서는 안 된다는 것이다 — 명령-질의 분리(command-query
  separation). 어떤 프로그래머는 이것을 절대 규칙으로 다룬다. 나는 (다른 무엇에서도 그렇듯)
  100퍼센트 순수하지는 않지만 대체로 그것을 따르려 하고, 그것은 나에게 잘 봉사했다** (11장
  §"Separate Query from Modifier", p.306).[^fowler2018]
- **"관찰 가능한"이라는 한정어가 이 항목의 실질이다** (11장 §"Separate Query from Modifier",
  p.307):[^fowler2018]

> Note that I use the phrase *observable* side effects. A common optimization is to cache
> the value of a query in a field so that repeated calls go quicker. Although this changes
> the state of the object with the cache, the change is not observable. Any sequence of
> queries will always return the same results for each query.

  - 2장이 리팩터링의 정의에서 **관찰 가능한 동작(observable behavior)**을 일부러 느슨하게 둔
    것과 같은 어법이다 — [리팩터링](refactoring.md) 참조.

## Parameterize Function과 Remove Flag Argument

- **Parameterize Function**(p.310) — 짧고 단순한 항목이다 — **서로 다른 리터럴 값으로 아주
  비슷한 로직을 수행하는 두 함수를 보면 다른 값들에 대한 매개변수를 가진 하나의 함수를 써서
  중복을 없앨 수 있다. 이것은 함수의 유용성을 높이는데, 다른 값으로 다른 데서도 적용할 수 있기
  때문이다** (11장 §"Parameterize Function", p.310).[^fowler2018]
- **Remove Flag Argument**(p.314, 초판 이름 *Replace Parameter with Explicit Methods*) —
  정의가 먼저 나온다 — **플래그 인수(flag argument)는 호출자가 불리는 함수가 어느 로직을
  실행해야 하는지 가리키려고 쓰는 함수 인수다** (11장 §"Remove Flag Argument",
  p.314).[^fowler2018] `bookConcert(aCustomer, isPremium)`처럼 생겼고, 불리언뿐 아니라
  열거형(`CustomerType.PREMIUM`)이나 문자열(`"premium"`)로도 온다.
- **싫어하는 이유가 API 탐색 순서에서 나온다** (11장 §"Remove Flag Argument",
  p.315):[^fowler2018]

> I dislike flag arguments because they complicate the process of understanding what
> function calls are available and how to call them. My first route into an API is usually
> the list of available functions, and flag arguments hide the differences in the function
> calls that are available.

  - **불리언이 특히 나쁘다** — **불리언 플래그는 읽는 사람에게 그 뜻을 전하지 않으므로 더욱
    나쁘다 — 함수 호출에서 `true`가 무엇을 뜻하는지 알아낼 수 없다. 내가 하고 싶은 일에 대해
    명시적 함수를 제공하는 편이 더 명료하다** (11장 §"Remove Flag Argument",
    p.315).[^fowler2018] `premiumBookConcert(aCustomer)`가 그 형태다.
- **판정 조건이 둘 다 성립해야 플래그 인수다** — **호출자가 프로그램을 흘러가는 데이터가 아니라
  리터럴 값으로 불리언을 설정하고 있어야 하고, 구현 함수가 그 인수를 더 깊은 함수로 넘기는
  데이터가 아니라 제어 흐름에 영향을 주는 데 쓰고 있어야 한다** (11장 §"Remove Flag Argument",
  p.315).[^fowler2018]
- 부수 이득 하나 — **플래그 인수를 없애는 것은 코드를 더 명료하게 할 뿐 아니라 도구에도
  도움이 된다. 코드 분석 도구가 프리미엄 로직 호출과 일반 로직 호출의 차이를 이제 더 쉽게
  볼 수 있다** (11장 §"Remove Flag Argument", p.315).[^fowler2018]
- **예외와 그 예외의 냄새가 함께 적힌다** — **함수에 플래그 인수가 하나를 넘으면 자리가 있을 수
  있다. 그렇지 않으면 그 값들의 모든 조합에 대해 명시적 함수가 필요하기 때문이다. 그러나 그것
  또한 함수가 너무 많은 일을 한다는 신호이고, 이 로직을 위해 조합할 수 있는 더 단순한 함수를
  만들 방법을 찾아야 한다** (11장 §"Remove Flag Argument", p.315).[^fowler2018]
- 3장 긴 매개변수 목록(Long Parameter List) 냄새가 이 항목을 처방으로 지목한다 —
  [코드의 나쁜 냄새](../concepts/code-smells.md) 참조.

## Preserve Whole Object — 통째로 넘기기

- 처방 — **레코드에서 값 몇 개를 끌어내 그 값들을 함수에 넘기는 코드를 보면 그 값들을 레코드
  자체로 바꿔 함수 본문이 필요한 값을 스스로 끌어내게 하기를 좋아한다** (11장 §"Preserve Whole
  Object", p.319).[^fowler2018]
- 이득 셋 (11장 §"Preserve Whole Object", p.319):[^fowler2018] **레코드 전체를 넘기면 나중에
  불리는 함수가 전체에서 더 많은 데이터를 필요로 하게 돼도 매개변수 목록을 고칠 필요가 없어
  변경을 더 잘 감당하고**, **매개변수 목록 크기를 줄여 함수 호출을 대개 이해하기 쉽게 만들고**,
  **부분들로 여러 함수가 불리면 그 부분들을 조작하는 로직이 흔히 중복되는데 그 로직을 전체로
  옮길 수 있다.**
- **하지 말아야 할 조건이 명시된다** — **내가 이것을 하지 않는 주된 이유는 불리는 함수가 전체에
  대한 의존을 갖지 않기를 바랄 때다 — 보통 그 둘이 다른 모듈에 있을 때 그렇다** (11장
  §"Preserve Whole Object", p.319).[^fowler2018]
- **관련 냄새와 후속 항목이 붙는다** — 객체에서 값 여럿을 꺼내 그것들만 두고 로직을 하는 것은
  기능 편애(Feature Envy) 냄새이고 **보통 그 로직이 전체 자신으로 옮겨져야 한다는 신호다.**
  그리고 **여러 코드 조각이 어떤 객체 기능의 같은 부분집합만 쓴다면 그것은 *Extract
  Class*(p.182)의 좋은 기회를 가리킬 수 있다** (11장 §"Preserve Whole Object",
  p.319).[^fowler2018]
- **놓치기 쉬운 경우 하나** — **많은 사람이 놓치는 한 경우는 객체가 자기 데이터 값 여럿으로 다른
  객체를 부를 때다. 이것을 보면 그 값들을 자기 참조(자바스크립트의 `this`)로 바꿀 수 있다**
  (11장 §"Preserve Whole Object", p.319).[^fowler2018]

## 매개변수와 질의 사이 — 참조 투명성을 두고 벌이는 절충

두 항목이 서로의 역이고, 저자가 이 쌍을 "매우 익숙해져야 하는" 것으로 꼽는다.

- **Replace Parameter with Query**(p.324) — 매개변수 목록의 역할이 먼저 규정된다 — **함수의
  매개변수 목록은 그 함수의 가변성 지점을 요약해 그 함수가 다르게 행동할 수 있는 주된 방식을
  가리켜야 한다** (11장 §"Replace Parameter with Query", p.324).[^fowler2018] 그러므로
  **호출이 함수가 스스로 똑같이 쉽게 정할 수 있는 값을 넘긴다면 그것은 중복의 한 형태다.**
  - **"똑같이 쉽게"가 한계선이다** — **매개변수를 없앰으로써 나는 매개변수 값을 정하는 책임을
    옮긴다. 매개변수가 있으면 그 값을 정하는 것은 호출자의 책임이고, 없으면 그 책임이 함수
    본문으로 옮겨 간다. 내 습관은 호출자의 삶을 단순하게 하는 것이고 그것은 책임을 함수 본문으로
    옮긴다는 뜻이다 — 다만 그 책임이 거기 적절할 때만이다** (11장 §"Replace Parameter with
    Query", p.324).[^fowler2018]
  - **피해야 할 주된 이유가 의존이다** — **매개변수를 없애는 것이 함수 본문에 원치 않는 의존을
    더할 때 — 함수가 모르는 채로 두고 싶은 프로그램 요소에 접근하게 만들 때 — 다** (11장
    §"Replace Parameter with Query", pp.324–325).[^fowler2018]
  - **가장 안전한 경우가 명시된다** — **없애려는 매개변수의 값이 목록의 다른 매개변수를 질의하는
    것만으로 정해질 때다. 하나로 다른 하나를 정할 수 있다면 둘을 넘길 이유가 거의 없다** (11장
    §"Replace Parameter with Query", p.325).[^fowler2018]
  - **참조 투명성이 방어선이다** — **참조 투명성(referential transparency), 즉 같은 매개변수
    값으로 불릴 때마다 같은 방식으로 행동한다고 확신할 수 있는지 조심해야 한다. 그런 함수는
    추론하고 테스트하기가 훨씬 쉬우므로 그 성질을 잃도록 고치고 싶지 않다. 그래서 나는
    매개변수를 가변 전역 변수에 대한 접근으로 바꾸지 않는다** (11장 §"Replace Parameter with
    Query", p.325).[^fowler2018]
- **Replace Query with Parameter**(p.327) — 반대 방향이고 목적이 의존 관계 조정이다 —
  **함수 본문을 훑다가 그 함수 범위 안의 무언가에 대한 참조 중 마음에 들지 않는 것을 볼 때가
  있다. 전역 변수에 대한 참조일 수도 있고, 내가 떼어 내려는 같은 모듈 안의 요소일 수도 있다.
  이것을 풀려면 내부 참조를 매개변수로 바꿔 참조 해결의 책임을 함수의 호출자에게 옮겨야 한다**
  (11장 §"Replace Query with Parameter", p.327).[^fowler2018]
- **두 항목 사이의 긴장이 명시적이다** (11장 §"Replace Query with Parameter",
  p.327):[^fowler2018]

> There's a tension here between converting everything to parameters, which results in
> long repetitive parameter lists, and sharing a lot of scope which can lead to a lot of
> coupling between functions.

  - **순수 함수 핵과 I/O 껍질이라는 패턴이 여기서 나온다** — **흔한 패턴은 순수 함수로 이뤄진
    모듈을 두고 프로그램의 I/O와 다른 가변 요소를 다루는 로직이 그것을 감싸는 것이다. Replace
    Query with Parameter를 써서 프로그램의 일부를 순수하게 만들어 그 부분을 테스트하고 추론하기
    쉽게 할 수 있다** (11장 §"Replace Query with Parameter", p.328).[^fowler2018]
  - **그러나 이득만 있는 것이 아니라고 곧바로 정정한다** — **질의를 매개변수로 옮김으로써 나는
    호출자가 이 값을 어떻게 제공할지 알아내도록 강제한다. 이것은 함수 호출자의 삶을 복잡하게
    하고, 내 평소 편향은 소비자의 삶을 편하게 하는 인터페이스를 설계하는 것이다. 결국 그것은
    프로그램 전체에 책임을 배분하는 문제로 귀결되고, 그것은 쉽지도 불변도 아닌 결정이다 —
    그래서 이 리팩터링(과 그 역)은 내가 아주 익숙해져야 하는 것이다** (11장 §"Replace Query
    with Parameter", p.328).[^fowler2018]

## Remove Setting Method — 불변으로 가는 길

- 근거가 한 문장이다 — **세터 메서드를 제공하는 것은 그 필드가 바뀔 수 있다는 것을 가리킨다.
  객체가 만들어진 뒤 그 필드가 바뀌지 않기를 바란다면 나는 세터 메서드를 제공하지 않는다(그리고
  필드를 불변으로 만든다). 그러면 필드는 생성자에서만 설정되고, 바뀌지 않게 하려는 내 의도가
  분명해지고, 대개 필드가 바뀔 가능성 자체를 없앤다** (11장 §"Remove Setting Method",
  p.331).[^fowler2018]
- 나타나는 경우 둘 (11장 §"Remove Setting Method", p.331):[^fowler2018]
  - **생성자 안에서까지 접근자 메서드로 필드를 조작하는 습관** — 세터의 유일한 호출이
    생성자에서 오게 된다. **생성 이후의 갱신은 말이 되지 않는다는 것을 분명히 하려고 세터를
    없애는 편을 선호한다.**
  - **생성 스크립트로 객체를 만드는 경우** — 생성자 호출 뒤에 세터 호출이 이어지는 형태다.
    **스크립트가 끝나면 새 객체의 일부(또는 전부) 필드가 바뀌리라 기대하지 않는다. 세터는 이
    최초 생성 동안에만 불리도록 기대된다. 이 경우 내 의도를 더 분명히 하려고 세터를 없앤다.**
- 3장 가변 데이터(Mutable Data) 냄새가 이 항목을 처방으로 지목한다 —
  [코드의 나쁜 냄새](../concepts/code-smells.md) 참조.

## Replace Constructor with Factory Function — 생성자의 세 제약

- 이 항목의 근거 전부가 **생성자가 일반 함수보다 못한 세 자리**다 (11장 §"Replace Constructor
  with Factory Function", p.334):[^fowler2018]

> A Java constructor must return an instance of the class it was called with, which means
> I can't replace it with a subclass or proxy depending on the environment or parameters.
> Constructor naming is fixed, which makes it impossible for me to use a name that is
> clearer than the default. Constructors often require a special operator to invoke ("new"
> in many languages) which makes them difficult to use in contexts that expect normal
> functions.

  - 정리하면 (1) **반환 타입이 그 클래스로 고정돼 하위 클래스나 프록시로 바꿀 수 없고**,
    (2) **이름이 고정돼 기본값보다 명료한 이름을 쓸 수 없고**, (3) **호출에 특수 연산자가
    필요해 일반 함수를 기대하는 맥락에서 쓰기 어렵다.**
- **팩터리 함수에는 그 제약이 없다** — **팩터리 함수는 그런 제약을 겪지 않는다. 구현의 일부로
  생성자를 부를 가능성이 높지만 다른 것으로 자유롭게 대체할 수 있다** (11장 §"Replace
  Constructor with Factory Function", p.334).[^fowler2018]
- 수순이 짧다 — 생성자 호출을 본문으로 하는 팩터리 함수를 만들고, 생성자 호출을 하나씩 팩터리
  함수 호출로 바꾸며 매번 테스트한 뒤, **생성자의 가시성을 가능한 한 제한한다** (11장
  §"Replace Constructor with Factory Function", p.335).[^fowler2018]
- 이 항목이 두꺼운 이유는 다른 항목의 전제가 되기 때문이다 — 10장
  *Replace Conditional with Polymorphism*의 첫 수순이 **올바른 인스턴스를 반환하는 팩터리
  함수**를 요구하고, 12장 *Pull Up Constructor Body*는 **지저분해지면 이 항목으로 손을
  뻗으라**고 적는다. [조건부 로직 단순화 리팩터링](simplifying-conditional-logic.md)과
  [상속 다루기 리팩터링](refactoring-inheritance.md) 참조.

## Replace Function with Command과 그 역

- **Replace Function with Command**(p.337) — 함수를 객체로 캡슐화한다 — **함수를 그 자체의
  객체로 캡슐화하는 것이 유용할 때가 있는데, 나는 그것을 "명령 객체(command object)" 또는 그냥
  **명령**이라 부른다. 그런 객체는 대체로 단 하나의 메서드를 중심으로 세워지고, 그 요청과 실행이
  그 객체의 목적이다** (11장 §"Replace Function with Command", p.337).[^fowler2018]
- 이득 넷 (11장 §"Replace Function with Command", pp.337–338):[^fowler2018] **되돌리기 같은
  보완 연산**을 가질 수 있고, 매개변수를 단계적으로 쌓아 **더 풍부한 수명 주기**를 지원하는
  메서드를 제공할 수 있고, **상속과 훅으로 맞춤을 만들 수 있고**, 일급 함수가 없는 언어에서는
  명령으로 그 능력의 상당 부분을 낼 수 있다. 그리고 중첩 함수가 없는 언어에서도 메서드와
  필드로 복잡한 함수를 쪼갤 수 있고 **테스트와 디버깅 중에 그 메서드를 직접 부를 수 있다.**
- **그러나 기본값은 명령이 아니라 함수라고 못 박는다** (11장 §"Replace Function with Command",
  p.338):[^fowler2018]

> All these are good reasons to use commands, and I need to be ready to refactor functions
> into commands when I need to. But we must not forget that this flexibility, as ever,
> comes at a price paid in complexity. So, given the choice between a first-class function
> and a command, I'll pick the function 95% of the time. I only use a command when I
> specifically need a facility that simpler approaches can't provide.

- **낱말의 중의성을 저자가 직접 정리한다** — 여기서 쓰는 "명령"은 GoF의 명령 패턴을 따라
  **요청을 캡슐화한 객체**이고, 명령-질의 분리 원칙에서 말하는 "명령"(관찰 가능한 상태를 바꾸는
  객체 메서드)과 다르다. **나는 늘 그 뜻으로 command를 쓰지 않으려 했고 "modifier"나 "mutator"를
  선호했다** (11장 §"Replace Function with Command", p.338).[^fowler2018]
- **Replace Command with Function**(p.344) — 그 역. **명령 객체는 복잡한 계산을 다루는 강력한
  기제를 제공한다. (…) 그러나 그 힘에는 대가가 따른다. 대부분의 경우 나는 그저 함수를 불러 그
  일을 하게 하고 싶다. 그런 경우이고 함수가 그리 복잡하지 않다면 명령 객체는 그 값어치보다
  성가시므로 일반 함수로 바꿔야 한다** (11장 §"Replace Command with Function",
  p.344).[^fowler2018]

## 이어지는 페이지

- [조건부 로직 단순화 리팩터링](simplifying-conditional-logic.md) — 앞 장(10장)
- [상속 다루기 리팩터링](refactoring-inheritance.md) — 다음 장(12장)
- [기본 리팩터링](../concepts/basic-refactorings.md) — 같은 관절 비유가 *Change Function Declaration*의
  근거로 나오는 자리
- [리팩터링](refactoring.md) — "관찰 가능한 동작"이라는 느슨한 말의 정본
- [코드의 나쁜 냄새](../concepts/code-smells.md) — 긴 매개변수 목록·가변 데이터가 이 장을 지목한다
- [결합 끊기](../concepts/decoupling.md) — 매개변수와 질의 사이 절충이 재는 것
- [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md) — 명령 패턴이 리팩터링의 목적지로 등장하는 형식
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 11장 "Refactoring APIs"(pp.305–348). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 22).
    직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준 규약이며 근거는
    `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example 절과 스케치 도판은
    옮기지 않았다. §"Remove Flag Argument"의 호출 예시는 문장 속 조각이라 인라인으로 옮겼다.

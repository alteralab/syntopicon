---
type: concept
title: 조건부 로직 단순화 리팩터링
description: 조건문을 다루는 여섯 항목 — 조건을 분해해 무엇이 아니라 왜를 드러내기, 같은 결과를 내는 검사들을 하나로 합치기, 보호 구절이 강조의 장치라는 규정과 단일 출구 규칙에 대한 판정, 조건을 다형성으로 바꾸는 두 상황과 그 남용에 대한 저자의 거리 두기, 널 객체를 특수 사례의 한 경우로 일반화한 항목, 그리고 단언이 오류 탐지보다 소통의 수단이라는 판정
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 조건부 로직 단순화 리팩터링

- [이 장이 묶는 축](#이-장이-묶는-축)
- [Decompose Conditional — 무엇이 아니라 왜를 드러낸다](#decompose-conditional--무엇이-아니라-왜를-드러낸다)
- [Consolidate Conditional Expression — 합치는 이유가 곧 합치지 않을 이유다](#consolidate-conditional-expression--합치는-이유가-곧-합치지-않을-이유다)
- [Replace Nested Conditional with Guard Clauses — 강조의 장치](#replace-nested-conditional-with-guard-clauses--강조의-장치)
- [Replace Conditional with Polymorphism — 두 상황과 한 경계](#replace-conditional-with-polymorphism--두-상황과-한-경계)
- [Introduce Special Case — 널 객체를 일반화한 항목](#introduce-special-case--널-객체를-일반화한-항목)
- [Introduce Assertion — 오류 탐지보다 소통](#introduce-assertion--오류-탐지보다-소통)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **조건부 로직이 복잡성의 주된 원천일 때 그것을 어떤 형태로 바꾸는가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축

- 장의 전제가 한 문장이다 — **프로그램의 힘 상당 부분이 조건부 로직을 구현하는 능력에서 온다 —
  그러나 슬프게도 프로그램 복잡성의 상당 부분도 이 조건문 안에 있다** (10장,
  p.259).[^fowler2018]
- 배열 (10장, p.259):[^fowler2018] 복잡한 조건문에는 *Decompose Conditional*(p.260)을,
  논리 조합을 명료하게 하려면 *Consolidate Conditional Expression*(p.263)을, 주 처리 전에
  사전 검사를 돌리는 경우를 분명히 하려면 *Replace Nested Conditional with Guard
  Clauses*(p.266)를 쓴다. **같은 전환 로직을 쓰는 조건이 여럿 보이면
  *Replace Conditional with Polymorphism*(p.272)을 꺼낼 좋은 때다.** 널 같은 특수 사례를
  다루는 로직이 대체로 같으면 *Introduce Special Case*(p.289, *Introduce Null Object*로도
  불린다)가 중복을 많이 없앨 수 있다. **그리고 조건을 없애기를 좋아하기는 하지만 프로그램의
  상태를 소통하고 검사하고 싶다면 *Introduce Assertion*(p.302)이 값어치를 하는 추가라고
  본다.**

## Decompose Conditional — 무엇이 아니라 왜를 드러낸다

- 문제의 정체를 정확히 짚는다 — **문제는 보통 코드가, 조건 검사에서든 동작에서든, 무슨 일이
  일어나는지는 말해 주지만 *왜* 그 일이 일어나는지는 쉽게 흐려 버린다는 사실에 있다** (10장
  §"Decompose Conditional", p.260).[^fowler2018]
- 처방은 조건부에 특화된 추출이다 — **어떤 큰 코드 블록과도 마찬가지로 그것을 분해해 각 덩어리를
  그 덩어리의 의도를 따라 이름 지은 함수 호출로 바꿔 의도를 더 명료하게 만들 수 있다. 조건문에
  대해서는 조건 부분과 각 대안에 이것을 하기를 특히 좋아한다. 이렇게 하면 조건을 부각시키고
  내가 무엇을 두고 분기하는지 분명하게 만든다. 분기의 이유도 부각시킨다** (10장
  §"Decompose Conditional", p.260).[^fowler2018]
- **이 항목의 지위가 명시된다** — **이것은 사실 내 코드에 *Extract Function*(p.106)을 적용하는
  특정한 경우일 뿐이지만, 이 경우를 부각시키기를 좋아하는데 그 훈련이 놀랄 만큼 좋은 값어치를
  하는 것을 자주 발견했기 때문이다** (10장 §"Decompose Conditional", p.261).[^fowler2018]
- 3장 Long Function이 뽑아낼 덩어리를 찾는 신호로 조건문을 들면서 이 항목을 지목한다 —
  [코드의 나쁜 냄새](code-smells.md) 참조.

## Consolidate Conditional Expression — 합치는 이유가 곧 합치지 않을 이유다

- 계기는 같은 결과를 내는 다른 검사들이다 — **각 검사가 서로 다르면서도 결과 동작은 같은 조건
  검사의 연쇄를 만날 때가 있다. 이것을 보면 `and`와 `or` 연산자로 그것들을 하나의 결과를 내는
  하나의 조건 검사로 합친다** (10장 §"Consolidate Conditional Expression",
  p.263).[^fowler2018]
- 이유 둘 (10장 §"Consolidate Conditional Expression", p.263):[^fowler2018]
  - **의미를 드러낸다** — **다른 검사들을 결합한 단 하나의 검사를 실제로 하고 있음을 보여 줌으로써
    더 명료하게 만든다. 연쇄도 같은 효과를 내지만 그저 가까이 놓인 별개 검사들의 연속처럼
    보인다.**
  - **다음 리팩터링을 준비한다** — **둘째 이유는 그것이 흔히 *Extract Function*(p.106)의 밑자리를
    깔아 준다는 것이다. 조건을 추출하는 것은 코드를 명료하게 하려고 내가 할 수 있는 가장 유용한
    일 중 하나다. 그것은 내가 *무엇*을 하고 있는가의 진술을 *왜* 하고 있는가로 바꾼다.**
- **그리고 그 이유가 곧 반대 조건이 된다** — **조건문을 합치는 편의 이유는 그렇게 하지 말아야 할
  이유도 가리킨다. 하나의 검사로 생각되어서는 안 되는 진정으로 독립적인 검사라고 본다면 나는
  이 리팩터링을 하지 않는다** (10장 §"Consolidate Conditional Expression",
  p.263).[^fowler2018]

## Replace Nested Conditional with Guard Clauses — 강조의 장치

- 조건문을 두 유형으로 가른다 — **첫째 유형에서는 조건문의 두 갈래 모두 정상 행동의 일부이고,
  둘째 유형에서는 한 갈래가 정상이고 다른 갈래가 이례적 조건을 가리킨다. 이런 조건문은 의도가
  다르고 — 그 의도가 코드에 드러나야 한다** (10장 §"Replace Nested Conditional with Guard
  Clauses", p.266).[^fowler2018]
  - 둘 다 정상이면 `if`와 `else` 갈래를 쓰고, **이례적 조건이면 조건을 검사해 참이면 반환한다.
    이런 종류의 검사를 흔히 보호 구절(guard clause)이라 부른다.**
- **이 항목의 핵심이 강조라고 명시한다** (10장 §"Replace Nested Conditional with Guard
  Clauses", p.266):[^fowler2018]

> The key point of Replace Nested Conditional with Guard Clauses is emphasis. If I'm
> using an if-then-else construct, I'm giving equal weight to the if leg and the else leg.
> This communicates to the reader that the legs are equally likely and important. Instead,
> the guard clause says, "This isn't the core to this function, and if it happens, do
> something and get out."

- **단일 출구 규칙에 대한 판정** — **한 메서드에 진입점 하나 출구 하나만 두라고 배운 프로그래머와
  일할 때 이 리팩터링을 쓰게 되는 일이 잦다. 진입점 하나는 현대 언어가 강제하지만 출구 하나는
  정말 유용한 규칙이 아니다. 명료함이 핵심 원칙이다. 메서드가 출구 하나로 더 명료하면 출구
  하나를 쓰고, 아니면 쓰지 마라** (10장 §"Replace Nested Conditional with Guard Clauses",
  p.266).[^fowler2018]

## Replace Conditional with Polymorphism — 두 상황과 한 경계

- 문제 규정 — **복잡한 조건부 로직은 프로그래밍에서 추론하기 가장 어려운 것 중 하나이므로 나는
  늘 조건부 로직에 구조를 더할 방법을 찾는다. 로직을 서로 다른 상황 — 고수준 사례 — 으로 나눠
  조건을 가를 수 있다는 것을 자주 발견한다. 때로는 이 나눔을 조건문 자체의 구조 안에서 표현하는
  것으로 충분하지만, 클래스와 다형성을 쓰면 그 분리를 더 명시적으로 만들 수 있다** (10장
  §"Replace Conditional with Polymorphism", pp.272–273).[^fowler2018]
- **쓰이는 상황이 둘이고 서로 다르다** (10장 §"Replace Conditional with Polymorphism",
  p.273):[^fowler2018]
  - **타입 집합** — **각각 조건부 로직을 다르게 다루는 타입 집합을 만들 수 있는 경우다. 책·음악·
    음식이 그 타입 때문에 다르게 다뤄진다는 것을 알아챌 수 있다. 이것은 타입 코드를 두고
    switch 문을 가진 함수가 여럿일 때 가장 뚜렷해진다. 그런 경우 각 사례에 대한 클래스를 만들고
    다형성으로 타입별 행동을 끌어냄으로써 공통 switch 로직의 중복을 없앤다.**
  - **기본 사례와 변형** — **로직을 기본 사례와 변형들로 생각할 수 있는 경우다. 기본 사례는 가장
    흔하거나 가장 직선적인 것일 수 있다. 이 로직을 상위 클래스에 넣으면 변형을 걱정하지 않고
    그것을 추론할 수 있다. 그런 다음 각 변형 사례를 하위 클래스에 넣고, 기본 사례와의 차이를
    부각시키는 코드로 표현한다.**
- **남용에 대한 거리 두기가 명시적이다** (10장 §"Replace Conditional with Polymorphism",
  p.273):[^fowler2018]

> Polymorphism is one of the key features of object-oriented programming—and, like any
> useful feature, it's prone to overuse. I've come across people who argue that all
> examples of conditional logic should be replaced with polymorphism. I don't agree with
> that view. Most of my conditional logic uses basic conditional statements—if/else and
> switch/case. But when I see complex conditional logic that can be improved as discussed
> above, I find polymorphism a powerful tool.

  - 3장의 반복되는 switch(Repeated Switches) 냄새가 같은 거리 두기를 초판 판정의 철회로
    적는다 — 초판에는 "switch statements"라는 냄새가 있었고 2판에서 표적을 좁혔다.
    [코드의 나쁜 냄새](code-smells.md) 참조.
- 수순의 요지 (10장 §"Replace Conditional with Polymorphism", p.273):[^fowler2018]
  1. 다형 행동을 담을 클래스가 없으면 **올바른 인스턴스를 반환하는 팩터리 함수와 함께** 만들고
     호출 코드에서 그 팩터리 함수를 쓴다.
  2. 조건부 함수를 상위 클래스로 옮긴다. **조건부 로직이 자립적인 함수가 아니면
     *Extract Function*(p.106)으로 그렇게 만든다.**
  3. 하위 클래스 하나를 골라 그 조건문 메서드를 재정의하는 메서드를 만들고 해당 갈래의 본문을
     복사해 맞춘다. 각 갈래마다 반복한다.
  4. **상위 클래스 메서드에는 기본 경우를 남긴다.** 상위 클래스가 추상이어야 하면 그 메서드를
     추상으로 선언하거나 하위 클래스의 책임임을 보이려고 오류를 던진다.
- 12장의 *Replace Type Code with Subclasses*(p.362)가 이 항목의 전제 조건을 만드는 항목이다 —
  [상속 다루기 리팩터링](refactoring-inheritance.md) 참조.

## Introduce Special Case — 널 객체를 일반화한 항목

- 초판 이름이 *Introduce Null Object*였고 2판에서 이름이 넓어졌다. 계기는 중복이다 —
  **중복 코드의 흔한 경우는 자료 구조의 사용자 다수가 특정 값을 검사하고 그다음 대부분이 같은
  일을 할 때다. 코드베이스의 여러 부분이 특정 값에 같은 반응을 하는 것을 발견하면 나는 그 반응을
  한 자리로 모으고 싶다** (10장 §"Introduce Special Case", p.289).[^fowler2018]
- 기제는 특수 사례 패턴이다 — **이를 위한 좋은 기제가 특수 사례(Special Case) 패턴인데, 공통
  행동을 전부 담은 특수 사례 요소를 만드는 것이다. 이것으로 대부분의 특수 사례 검사를 단순한
  호출로 바꿀 수 있다** (10장 §"Introduce Special Case", p.289).[^fowler2018]
- 나타나는 방식이 여럿이라고 적는다 — **객체로 데이터를 읽기만 한다면 필요한 값을 다 채운 리터럴
  객체를 공급할 수 있다. 단순한 값보다 더 많은 행동이 필요하면 공통 행동 전부에 대한 메서드를
  가진 특수 객체를 만들 수 있다. 특수 사례 객체는 캡슐화하는 클래스가 반환할 수도 있고 변환으로
  자료 구조에 끼워 넣을 수도 있다** (10장 §"Introduce Special Case", p.289).[^fowler2018]
- **이름을 넓힌 근거가 한 문장으로 적혀 있다** (10장 §"Introduce Special Case",
  p.289):[^fowler2018]

> A common value that needs special-case processing is null, which is why this pattern is
> often called the Null Object pattern. But it's the same approach for any special case—I
> like to say that Null Object is a special case of Special Case.

  - 패턴이 리팩터링의 목적지로 등장하는 자리이고, 같은 형식에 대한 다른 계보의 판정은
    [디자인 패턴의 해부](design-pattern-anatomy.md)에 있다.

## Introduce Assertion — 오류 탐지보다 소통

- 문제는 코드에 적히지 않은 가정이다 — **코드의 어떤 구간은 특정 조건이 참일 때만 동작한다.
  제곱근 계산이 양수 입력에서만 동작하는 것처럼 단순할 수도 있다. 객체라면 어떤 필드 무리 중
  적어도 하나가 값을 가져야 한다는 것을 요구할 수도 있다. 그런 가정은 흔히 진술되지 않고
  알고리즘을 훑어야만 추론할 수 있다. 때로는 주석으로 진술돼 있다. 더 나은 기법은 단언을 써서
  그 가정을 명시적으로 만드는 것이다** (10장 §"Introduce Assertion", p.302).[^fowler2018]
- **단언의 정의와 계약이 명시된다** (10장 §"Introduce Assertion", p.302):[^fowler2018]

> An assertion is a conditional statement that is assumed to be always true. Failure of an
> assertion indicates a programmer error. Assertion failures should never be checked by
> other parts of the system. Assertions should be written so that the program functions
> equally correctly if they are all removed; indeed, some languages provide assertions
> that can be disabled by a compile-time switch.

- **주된 가치가 오류 탐지가 아니라 소통이라고 저자가 자기 입장을 구분한다** — **사람들이 오류를
  찾으려고 단언 쓰기를 권장하는 것을 자주 본다. 그것은 분명히 좋은 일이지만 단언을 쓰는 유일한
  이유는 아니다. 나는 단언이 값어치 있는 소통의 형식이라고 본다 — 그것은 실행의 이 지점에서
  프로그램의 가정된 상태에 대해 무언가를 읽는 사람에게 말해 준다** (10장 §"Introduce
  Assertion", p.302).[^fowler2018]
- **자기 테스트 코드와의 관계가 명시된다** — **디버깅에도 편리하고, 그 소통 가치 때문에 쫓던
  오류를 고친 뒤에도 남겨 두는 쪽으로 기운다. 자기 테스트 코드는 디버깅에 대한 단언의 가치를
  줄이는데, 꾸준히 좁혀 가는 단위 테스트가 흔히 그 일을 더 잘하기 때문이다. 그러나 나는 여전히
  소통을 위해 단언을 좋아한다** (10장 §"Introduce Assertion", p.302).[^fowler2018]
  담보 쪽 정본은 [자기 테스트 코드](self-testing-code.md)다.
- 3장 주석(Comments) 냄새가 **시스템의 요구되는 상태에 대한 규칙을 진술해야 하면** 이 항목을
  처방으로 지목한다 — [코드의 나쁜 냄새](code-smells.md) 참조.

## 이어지는 페이지

- [데이터 조직화 리팩터링](organizing-data.md) — 앞 장(9장)
- [API 리팩터링](refactoring-apis.md) — 다음 장(11장)
- [상속 다루기 리팩터링](refactoring-inheritance.md) — 다형성으로 가는 전제를 만드는 장(12장)
- [기본 리팩터링](basic-refactorings.md) — 이 장의 여러 항목이 부품으로 쓰는 *Extract Function*의 정본
- [코드의 나쁜 냄새](code-smells.md) — 반복되는 switch·긴 함수가 이 장을 지목한다
- [자기 테스트 코드](self-testing-code.md) — 단언과 단위 테스트의 분업
- [디자인 패턴의 해부](design-pattern-anatomy.md) — 패턴이 리팩터링의 목적지로 등장하는 형식
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 10장 "Simplifying Conditional Logic"(pp.259–304). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준
    규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example
    절과 스케치 도판은 옮기지 않았다.

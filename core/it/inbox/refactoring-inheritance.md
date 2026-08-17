---
type: concept
title: 상속 다루기 리팩터링
description: 카탈로그 마지막 장의 열한 항목 — 계층 위아래로 기능을 올리고 내리는 다섯, 계층 자체를 만들고 없애는 넷, 그리고 상속을 위임으로 바꾸는 둘. 메서드 올리기가 중복 제거의 항목인 이유와 차이를 먼저 찾으라는 단서, 타입 코드를 하위 클래스로 바꿀 두 유인과 직접 서브클래싱의 한계, 상속의 두 약점(축이 하나뿐이고 결합이 강하다), 그리고 "상속보다 합성"이라는 원칙에 대한 저자의 명시적 재해석
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 상속 다루기 리팩터링

- [이 장이 묶는 축](#이-장이-묶는-축)
- [Pull Up Method — 중복 제거의 항목](#pull-up-method--중복-제거의-항목)
- [계층 위아래로 옮기는 나머지 넷](#계층-위아래로-옮기는-나머지-넷)
- [Replace Type Code with Subclasses — 하위 클래스를 부르는 두 유인](#replace-type-code-with-subclasses--하위-클래스를-부르는-두-유인)
- [계층을 만들고 없애는 셋](#계층을-만들고-없애는-셋)
- [Replace Subclass with Delegate — 상속의 두 약점](#replace-subclass-with-delegate--상속의-두-약점)
- [Replace Superclass with Delegate — 잘못된 상속의 두 진단](#replace-superclass-with-delegate--잘못된-상속의-두-진단)
- [상속보다 합성이라는 원칙에 대한 저자의 재해석](#상속보다-합성이라는-원칙에-대한-저자의-재해석)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **상속 계층을 어떻게 고치고, 언제 상속 자체를 위임으로 갈아 끼우는가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축

- 장의 태도가 첫 문단에 있다 — **이 마지막 장에서 나는 객체지향 프로그래밍의 가장 잘 알려진
  기능 하나인 상속으로 향한다. 어떤 강력한 기제와도 마찬가지로 그것은 아주 유용하면서 오용하기
  쉽고, 그 오용은 백미러에 들어오고 나서야 보이는 일이 잦다** (12장, p.349).[^fowler2018]
- 배열이 셋으로 갈린다 (12장, p.349):[^fowler2018]
  - **계층 위아래로 옮기기** — *Pull Up Method*(p.350), *Pull Up Field*(p.353),
    *Pull Up Constructor Body*(p.355), *Push Down Method*(p.359), *Push Down Field*(p.361).
  - **계층에서 클래스를 더하고 빼기** — *Extract Superclass*(p.375), *Remove
    Subclass*(p.369), *Collapse Hierarchy*(p.380). 그리고 값에 따라 다른 행동을 유발하려고
    쓰던 필드를 하위 클래스로 대체하는 *Replace Type Code with Subclasses*(p.362).
  - **상속을 위임으로 바꾸기** — **상속은 강력한 도구지만 때로 잘못된 자리에 쓰이거나 쓰인
    자리가 잘못된 자리가 된다. 그런 경우 *Replace Subclass with Delegate*(p.381)나
    *Replace Superclass with Delegate*(p.399)로 상속을 위임으로 바꾼다.**

## Pull Up Method — 중복 제거의 항목

- 이 항목이 상속 리팩터링이 아니라 **중복 제거 리팩터링**으로 규정된다 — **중복 코드를 없애는
  것이 중요하다. 중복된 메서드 둘은 그대로도 잘 동작할 수 있지만 미래 버그의 번식지일 뿐이다.
  중복이 있는 곳에는 한 사본에 가한 변경이 다른 사본에 가해지지 않을 위험이 있다** (12장
  §"Pull Up Method", p.350).[^fowler2018]
- **가장 쉬운 경우와 그 함정이 함께 적힌다** — **Pull Up Method를 쓰는 가장 쉬운 경우는 메서드의
  본문이 같을 때인데, 복사해 붙인 것이 있었다는 뜻이다. 물론 늘 그렇게 뻔하지는 않다**
  (12장 §"Pull Up Method", p.350).[^fowler2018]
- **차이를 먼저 찾으라는 단서가 이 항목의 실질적 기여다** (12장 §"Pull Up Method",
  p.350):[^fowler2018]

> I could just do the refactoring and see if the tests croak—but that puts a lot of
> reliance on my tests. I usually find it valuable to look for the differences—often, they
> show up behavior that I forgot to test for.

  - 테스트를 담보로 쓰되 담보에만 기대지 않는 태도이고, 4장의 자기 테스트 코드가 세우는 신뢰의
    한계와 짝을 이룬다 — [자기 테스트 코드](self-testing-code.md) 참조.
- **다른 항목 뒤에 오는 일이 잦다** — **서로 다른 클래스의 두 메서드가 매개변수화하면 사실상
  같은 메서드가 되는 것을 본다. 그런 경우 가장 작은 걸음은 *Parameterize Function*(p.310)을
  따로 적용한 다음 Pull Up Method를 하는 것이다** (12장 §"Pull Up Method",
  p.351).[^fowler2018]
- **가장 어색한 합병증이 명시된다** — **메서드 본문이 상위 클래스에는 없고 하위 클래스에만 있는
  기능을 참조할 때다. 그럴 때는 그 요소들에 *Pull Up Field*(p.353)와 Pull Up Method를 먼저
  써야 한다** (12장 §"Pull Up Method", p.351).[^fowler2018] 전체 흐름은 비슷하나 세부가
  다르면 Form Template Method를 검토한다.
- 수순의 첫 단계가 검사다 — **메서드가 같은지 확인한다. 같은 일을 하지만 동일하지 않으면 본문이
  동일해질 때까지 리팩터링한다.** 그다음 **메서드 본문 안의 모든 메서드 호출과 필드 참조가
  상위 클래스에서 부를 수 있는 기능을 가리키는지 확인**하고, 시그니처가 다르면
  *Change Function Declaration*(p.124)으로 맞춘다 (12장 §"Pull Up Method",
  p.350).[^fowler2018]
- 3장 중복 코드(Duplicated Code) 냄새가 **공통 기반 클래스의 하위 클래스들에 있는 중복 조각**의
  처방으로 이 항목을 지목한다 — [코드의 나쁜 냄새](code-smells.md) 참조.

## 계층 위아래로 옮기는 나머지 넷

- **Pull Up Field**(p.353) — **하위 클래스가 독립적으로 개발되거나 리팩터링으로 합쳐지면 그것들이
  기능을 중복하는 것을 자주 발견한다. 특히 어떤 필드는 중복일 수 있다. 그런 필드는 때로 비슷한
  이름을 갖지만 늘 그런 것은 아니다. 무슨 일이 일어나는지 알 수 있는 유일한 방법은 필드를 보고
  그것이 어떻게 쓰이는지 살피는 것이다** (12장 §"Pull Up Field", p.353).[^fowler2018]
  - 이득이 두 겹이다 — **중복된 데이터 선언을 없애고, 그 필드를 쓰는 행동을 하위 클래스에서
    상위 클래스로 옮길 수 있다** (12장 §"Pull Up Field", p.353).[^fowler2018]
  - **동적 언어에서는 성격이 달라진다** — **많은 동적 언어는 클래스 정의의 일부로 필드를 정의하지
    않는다 — 대신 필드는 처음 대입될 때 나타난다. 이 경우 필드를 올리는 것은 본질적으로
    *Pull Up Constructor Body*(p.355)의 결과다** (12장 §"Pull Up Field",
    p.354).[^fowler2018]
- **Pull Up Constructor Body**(p.355) — 생성자만 따로 항목이 있는 이유가 적혀 있다 —
  **생성자는 까다로운 것이다. 완전히 보통 메서드가 아니라서 내가 할 수 있는 일이 더 제한된다.
  하위 클래스 메서드에 공통 행동이 보이면 내 첫 생각은 *Extract Function*(p.106) 뒤에
  *Pull Up Method*(p.350)이고 그것이 그 행동을 상위 클래스로 깔끔히 옮긴다. 생성자가 그것을
  엉키게 하는데, 무엇을 어떤 순서로 할 수 있는지에 대한 특수한 규칙이 있기 때문이다** (12장
  §"Pull Up Constructor Body", p.355).[^fowler2018]
  - 탈출구가 명시된다 — **이 리팩터링이 지저분해지기 시작하면 나는 *Replace Constructor with
    Factory Function*(p.334)으로 손을 뻗는다** (12장 §"Pull Up Constructor Body",
    p.355).[^fowler2018] 그쪽은 [API 리팩터링](refactoring-apis.md)에 있다.
- **Push Down Method**(p.359) — **메서드가 한 하위 클래스(또는 하위 클래스의 작은 일부)에만
  관계있다면 상위 클래스에서 없애고 그 하위 클래스(들)에만 두는 것이 그것을 더 분명하게
  만든다** (12장 §"Push Down Method", p.359).[^fowler2018]
  - **적용 조건이 호출자 쪽에 있다** — **호출자가 자기가 특정 하위 클래스를 다루고 있음을 알
    때만 이 리팩터링을 할 수 있다 — 그렇지 않으면 상위 클래스에 위약 행동을 두고
    *Replace Conditional with Polymorphism*(p.272)을 써야 한다** (12장 §"Push Down Method",
    p.359).[^fowler2018]
- **Push Down Field**(p.361) — 카탈로그에서 가장 짧은 동기 절이다 — **필드가 한 하위
  클래스(또는 하위 클래스의 작은 일부)에만 쓰인다면 그것을 그 하위 클래스로 옮긴다** (12장
  §"Push Down Field", p.361).[^fowler2018]

## Replace Type Code with Subclasses — 하위 클래스를 부르는 두 유인

- 출발은 타입 코드가 정상이라는 인정이다 — **소프트웨어 시스템은 흔히 비슷한 것의 서로 다른
  종류를 표현해야 한다. 직원을 직무 유형(엔지니어·관리자·영업)으로 분류하거나 주문을
  우선순위(긴급·일반)로 분류할 수 있다. 이것을 다루는 내 첫 도구는 어떤 종류의 타입 코드
  필드다 — 언어에 따라 열거형·심벌·문자열·숫자일 수 있다. (…) 대부분의 경우 그런 타입 코드가
  내가 필요한 전부다** (12장 §"Replace Type Code with Subclasses",
  p.362).[^fowler2018]
- **그럼에도 하위 클래스를 부르는 유인 둘** (12장 §"Replace Type Code with Subclasses",
  pp.362–363):[^fowler2018]
  - **다형성으로 조건부 로직을 다룰 수 있다** — **타입 코드 값에 따라 다른 행동을 부르는 함수가
    여럿일 때 가장 도움이 된다.** 그 함수들에 *Replace Conditional with Polymorphism*(p.272)을
    적용할 수 있다.
  - **특정 타입 코드 값에만 유효한 필드나 메서드가 있을 때** — 영업에만 해당하는 판매 할당량
    같은 것. 하위 클래스를 만들어 *Push Down Field*(p.361)를 적용한다. **필드가 올바른 타입
    코드 값일 때만 쓰이도록 검증 로직을 넣을 수도 있지만 하위 클래스를 쓰면 그 관계가 더
    명시적이 된다.**
- **적용 대상 선택에 판단이 하나 더 있다** — 클래스 자체를 서브클래싱할 것인가 타입 코드를
  서브클래싱할 것인가 — **엔지니어를 직원의 서브타입으로 만드는가, 아니면 직원에게 엔지니어와
  관리자 서브타입을 가질 수 있는 직원 유형 속성을 주는가.** 판정 기준 둘이 명시된다 —
  **직접 서브클래싱이 더 단순하지만, 그 타입이 다른 용도로 필요하면 직무 유형에 쓸 수 없다.
  타입이 가변이면 직접 하위 클래스를 쓸 수도 없다** (12장 §"Replace Type Code with
  Subclasses", p.363).[^fowler2018] 하위 클래스를 직원 유형 속성으로 옮겨야 하면 타입 코드에
  *Replace Primitive with Object*(p.174)를 써서 유형 클래스를 만든 뒤 그 새 클래스에 이 항목을
  적용한다.

## 계층을 만들고 없애는 셋

- **Extract Superclass**(p.375) — **비슷한 일을 하는 두 클래스를 보면 상속의 기본 기제를 이용해
  그 유사성을 상위 클래스로 끌어올릴 수 있다** (12장 §"Extract Superclass",
  p.375).[^fowler2018] *Pull Up Field*로 공통 데이터를, *Pull Up Method*로 공통 행동을 옮긴다.
  - **상속을 사전 계획으로 보는 견해에 저자가 거리를 둔다** (12장 §"Extract Superclass",
    p.375):[^fowler2018]

> Many writers on object orientation treat inheritance as something that should be
> carefully planned in advance, based on some kind of classification structure in the
> "real world." Such classification structures can be a hint towards using
> inheritance—but just as often inheritance is something I realize during the evolution
> of a program, as I find common elements that I want to pull together.

  - **대안과 그 선택 순서가 명시된다** — 대안은 *Extract Class*(p.182)이고 **여기서 당신은
    본질적으로 중복 행동을 통합하는 방법으로 상속과 위임 중 하나를 고르는 셈이다. 흔히 Extract
    Superclass가 더 단순한 접근이므로 나는 나중에 필요하면 *Replace Superclass with
    Delegate*(p.399)를 쓸 수 있다는 것을 알고 이것을 먼저 한다** (12장 §"Extract
    Superclass", p.375).[^fowler2018]
- **Remove Subclass**(p.369) — **하위 클래스는 유용하다. 자료 구조의 변형과 다형 행동을
  지원한다. 차이로 프로그래밍하는 좋은 방법이다. 그러나 소프트웨어 시스템이 진화하면서 하위
  클래스가 지원하던 변형이 다른 자리로 옮겨지거나 아예 없어지면서 하위 클래스가 값을 잃을 수
  있다. 때로 하위 클래스는 결국 만들어지지 않은 기능을 예상하고 더해지거나, 하위 클래스를
  필요로 하지 않는 방식으로 만들어진다** (12장 §"Remove Subclass", p.369).[^fowler2018]
  - 판정 — **너무 적은 일을 하는 하위 클래스는 더 이상 값어치가 없는 이해 비용을 물린다. 그때가
    오면 하위 클래스를 없애고 상위 클래스의 필드로 대체하는 것이 최선이다** (12장 §"Remove
    Subclass", p.369).[^fowler2018] 3장의 게으른 요소(Lazy Element) 냄새와 같은 진단이다.
- **Collapse Hierarchy**(p.380) — 계층을 리팩터링하다 보면 **클래스와 그 부모가 더 이상 따로
  둘 만큼 다르지 않다는 것을 발견할 때가 있다. 그 시점에 나는 둘을 합친다** (12장 §"Collapse
  Hierarchy", p.380).[^fowler2018]

## Replace Subclass with Delegate — 상속의 두 약점

- 상속이 자연스러운 출발점이라는 것부터 인정한다 — **범주마다 행동이 달라지는 객체가 있으면 그것을
  표현하는 자연스러운 기제는 상속이다. 공통 데이터와 행동을 전부 상위 클래스에 넣고 각 하위
  클래스가 필요한 대로 기능을 더하고 재정의하게 한다** (12장 §"Replace Subclass with
  Delegate", p.381).[^fowler2018]
- **약점 둘이 명시된다** (12장 §"Replace Subclass with Delegate", p.382):[^fowler2018]
  - **축이 하나뿐이다** — **가장 뻔하게도 그것은 한 번만 낼 수 있는 카드다. 무언가를 다르게 할
    이유가 하나를 넘으면 나는 상속을 단 하나의 변이 축에만 쓸 수 있다.** 나이 범주와 소득
    수준으로 사람의 행동을 달리하고 싶으면 둘 중 하나만 하위 클래스로 만들 수 있고 **둘 다는
    할 수 없다.**
  - **결합이 아주 강하다** — **상속은 클래스 사이에 매우 가까운 관계를 들여온다. 부모에 가하고
    싶은 어떤 변경이든 자식을 쉽게 깨뜨릴 수 있어서 조심해야 하고 자식이 상위 클래스에서 어떻게
    파생됐는지 이해해야 한다. 두 클래스의 로직이 다른 모듈에 있고 다른 팀이 돌볼 때 이 문제는
    더 나빠진다.**
- **위임이 둘 다 푼다** — **나는 서로 다른 이유로 여러 다른 클래스에 위임할 수 있다. 위임은 객체
  사이의 보통 관계이므로 작업할 명확한 인터페이스를 가질 수 있고, 그것은 서브클래싱보다 훨씬
  적은 결합이다** (12장 §"Replace Subclass with Delegate", p.382).[^fowler2018]
- **패턴과의 대응이 밝혀져 있다** — **4인방 책에 익숙한 이들은 이 리팩터링을 하위 클래스를 State나
  Strategy 패턴으로 대체하는 것으로 생각하면 도움이 될 것이다. 두 패턴은 구조적으로 같고, 호스트가
  별도 계층에 위임하는 데 기댄다** (12장 §"Replace Subclass with Delegate",
  p.382).[^fowler2018] 다만 **이 리팩터링의 모든 경우가 위임 대상의 상속 계층을 포함하지는
  않는다.**

## Replace Superclass with Delegate — 잘못된 상속의 두 진단

- **고전적 오용 사례가 스택과 리스트다** — **객체 초창기의 잘못된 상속의 고전적 예 하나가 스택을
  리스트의 하위 클래스로 만든 것이었다. 이렇게 하게 된 생각은 리스트의 데이터 저장과 그것을
  조작하는 연산을 재사용하는 것이었다. 재사용은 좋지만 이 상속에는 문제가 있었다. 리스트의 모든
  연산이 스택의 인터페이스에 나타났고, 그중 대부분이 스택에 적용될 수 없었다** (12장 §"Replace
  Superclass with Delegate", p.399).[^fowler2018]
  - 그래서 첫째 진단 — **상위 클래스의 함수가 하위 클래스에서 말이 되지 않는다면, 그것은 상위
    클래스의 기능을 쓰기 위해 상속을 쓰지 말아야 한다는 신호다** (12장 §"Replace Superclass
    with Delegate", p.399).[^fowler2018]
- **둘째 진단이 타입-인스턴스 동음이의다** — **상위 클래스의 모든 함수를 쓰는 것에 더해, 하위
  클래스의 모든 인스턴스가 상위 클래스의 인스턴스이고 상위 클래스를 쓰는 모든 경우에 유효한
  객체여야 한다는 것도 참이어야 한다.** 이름과 배기량을 가진 자동차 모델 클래스에 차대번호와
  제조일을 더해 실물 자동차를 표현하려는 것이 그 예이고, **저자가 타입-인스턴스
  동음이의(type-instance homonym)라 부른 흔하고 미묘한 모델링 실수다** (12장 §"Replace
  Superclass with Delegate", p.400).[^fowler2018]
- **모델링이 합당할 때도 쓴다** — **하위 클래스가 합당한 모델링인 경우에도 Replace Superclass
  with Delegate를 쓰는데, 하위 클래스와 상위 클래스의 관계가 고도로 결합돼 있어 하위 클래스가
  상위 클래스의 변경으로 쉽게 깨지기 때문이다** (12장 §"Replace Superclass with Delegate",
  p.400).[^fowler2018]
- **대가도 계량돼 있다** — **단점은 호스트와 위임 대상에서 같은 모든 함수에 대해 전달 함수를 써야
  한다는 것이다 — 그러나 다행히 그런 전달 함수는 쓰기 지루하기는 해도 틀리기에는 너무
  단순하다** (12장 §"Replace Superclass with Delegate", p.400).[^fowler2018]

## 상속보다 합성이라는 원칙에 대한 저자의 재해석

이 장이 이 KB에 들이는 가장 뚜렷한 판정이고, 같은 원칙을 더 강하게 읽는 소스들과 정면으로
맞닿는다.

- **원칙 자체는 인용하되 그 통상적 해석을 기각한다** (12장 §"Replace Subclass with Delegate",
  p.382):[^fowler2018]

> There is a popular principle: "Favor object composition over class inheritance" (where
> composition is effectively the same as delegation). Many people take this to mean
> "inheritance considered harmful" and claim that we should never use inheritance. I use
> inheritance frequently, partly because I always know I can use Replace Subclass with
> Delegate should I need to change it later. Inheritance is a valuable mechanism that does
> the job most of the time without problems. So I reach for it first, and move onto
> delegation when it starts to rub badly.

  - **그리고 그 해석이 원칙의 출처와도 어긋난다고 지적한다** — **이 용법은 실은 그 원칙과
    일관된다. 그 원칙은 상속과 합성이 어떻게 함께 동작하는지 설명하는 4인방 책에서 왔다.
    그 원칙은 상속의 과용에 대한 반작용이었다** (12장 §"Replace Subclass with Delegate",
    p.382).[^fowler2018]
- 같은 판정이 상위 클래스 쪽 항목에서 조건까지 붙어 반복된다 — **이 모든 것의 결과로 어떤
  사람들은 상속을 완전히 피하라고 조언한다 — 그러나 나는 그것에 동의하지 않는다. 적절한 의미
  조건이 적용되는 한(상위 타입의 모든 메서드가 하위 타입에 적용되고, 하위 타입의 모든 인스턴스가
  상위 타입의 인스턴스라면) 상속은 단순하고 효과적인 기제다. 상황이 바뀌어 상속이 더 이상 최선의
  선택이 아니게 되면 Replace Superclass with Delegate를 쉽게 적용할 수 있다. 그러니 내 조언은
  (대체로) 상속을 먼저 쓰고, 그것이 문제가 될 때(그리고 되면) Replace Superclass with
  Delegate를 적용하라는 것이다** (12장 §"Replace Superclass with Delegate",
  p.400).[^fowler2018]
- **이 판정의 구조가 카탈로그 전체의 태도와 같다** — 되돌리는 항목이 손에 있으므로 처음 선택을
  보수적으로 하지 않아도 된다. *Hide Delegate*와 *Remove Middle Man*, *Move Function*의
  "판단이 어려울수록 덜 중요하다"와 같은 논법이다.
- 같은 대상에 대해 더 강한 경고를 내놓는 두 소스의 판정은 [상속세](inheritance-tax.md)에 있다.
  세 소스가 같은 원칙을 두고 서 있는 자리가 각각 다르다 — #hypothesis 셋 중 어느 것도 서로를
  인용하지 않았고, 갈리는 것은 상속의 위험도가 아니라 **되돌릴 수 있는가에 대한 신뢰**로
  보인다.

## 이어지는 페이지

- [API 리팩터링](refactoring-apis.md) — 앞 장(11장). *Replace Constructor with Factory
  Function*과 *Parameterize Function*이 이 장의 부품으로 쓰이는 자리
- [조건부 로직 단순화 리팩터링](simplifying-conditional-logic.md) —
  *Replace Conditional with Polymorphism*의 정본. 이 장의 타입 코드 항목이 그 전제를 만든다
- [상속세](inheritance-tax.md) — 같은 대상에 더 강한 경고를 내놓는 두 소스
- [코드의 나쁜 냄새](code-smells.md) — 상속 포기·내부자 거래·게으른 요소가 이 장을 지목한다
- [디자인 패턴의 해부](design-pattern-anatomy.md) — State·Strategy가 리팩터링의 목적지로
  등장하는 형식
- [자기 테스트 코드](self-testing-code.md) — "테스트가 죽는지 보면 되지 않나"에 대한 저자의 유보
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 12장 "Dealing with Inheritance"(pp.349–404). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준
    규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example
    절과 스케치 도판은 옮기지 않았다. 이 장이 카탈로그의 마지막이고 그 뒤는 서지(p.405)와
    색인(p.409)이다.

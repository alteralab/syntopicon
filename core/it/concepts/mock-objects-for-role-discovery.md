---
type: concept
title: 목 객체는 역할을 발견하기 위한 것이다
description: 목 객체 기법을 만든 사람들이 그 기법의 목적을 무엇이라고 적었는가 — 이름이 잘못됐다는 자기 규정과 역할로 타입을 찾는다는 재규정, 필요에서 인터페이스를 끌어내는 need-driven development의 절차와 그것이 낳는 좁은 역할 인터페이스, 테스트를 거꾸로 쓰는 여섯 단계, "소유한 타입만 목하라"가 설계 변경 가능성 때문에 있다는 원래 근거, 저자들이 오해라고 이름 붙인 여섯 가운데 "목은 시스템 경계에서만 쓴다"와 "목이 리팩터링을 막는다" 둘, 도구가 기법을 강제하는 자리, 그리고 저자들이 스스로 적은 미해결과 이 논문에 측정이 없다는 사실
generated: { by: "claude-opus-5", at: "2026-08-24T01:20:00Z" }
contradicts: [what-to-replace-with-mocks]
sources:
  - { id: freeman2004-mock-roles, resource: /it/sources/freeman2004-mock-roles.md }
---

# 목 객체는 역할을 발견하기 위한 것이다

- [이 소스의 지위 — 심사를 거쳤으나 측정이 없다](#이-소스의-지위--심사를-거쳤으나-측정이-없다)
- [이름이 잘못됐다는 자기 규정](#이름이-잘못됐다는-자기-규정)
- [필요에서 인터페이스를 끌어낸다](#필요에서-인터페이스를-끌어낸다)
- [테스트를 거꾸로 쓴다](#테스트를-거꾸로-쓴다)
- [소유한 타입만 목한다 — 원래 근거](#소유한-타입만-목한다--원래-근거)
- [저자들이 오해라고 부르는 것](#저자들이-오해라고-부르는-것)
- [나머지 실무 지침](#나머지-실무-지침)
- [도구가 기법을 강제한다](#도구가-기법을-강제한다)
- [저자들이 스스로 적은 미해결](#저자들이-스스로-적은-미해결)
- [모순 — 무엇이 갈리는가](#모순--무엇이-갈리는가)
- [이 소스의 사각](#이-소스의-사각)
- [용어에 대하여](#용어에-대하여)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **목 객체(mock object) 기법은 원래 무엇을 하려고 만들어졌으며, 그 목적이
"무엇을 목으로 대체할 것인가"에 어떤 답을 주는가.**

## 이 소스의 지위 — 심사를 거쳤으나 측정이 없다

- **근거 등급은 `peer-reviewed`다.** 그러나 그 등급이 이 소스를 실증으로 만들지 않는다.
  **이 논문에는 실험도 표본도 결과 표도 없다.** 등급이 여는 것은 이 논문이 **스스로 잰 값**
  뿐인데, 이 논문은 아무것도 재지 않는다.
- **저자들이 자기 근거를 직접 규정한다** (§4 도입):[^freeman2004-mock-roles]

  > Between us, the authors have been working with Mock Objects on a wide range of projects
  > for over 5 years. We have also corresponded with other developers who have been using
  > the technique. The longest project was 4 years, and the largest team was 15 developers.

  이 문장의 숫자는 **경험의 범위**이지 효과의 크기가 아니다. 그러므로 이 페이지에서
  인용되는 것은 전부 **주장·정의·지침**이고 수치가 아니다.
- **그래서 이 페이지는 이 갈래에서 "무엇이 옳은가"가 아니라 "한쪽 처방의 원전 문면이
  무엇인가"를 소유한다.** 그 처방이 현장에서 지켜지는지는
  [실제 프로젝트에서 무엇이 목으로 대체되는가](what-gets-mocked-in-practice.md)가 갖는다.
- **학회명과 쪽수는 이 파일에 인쇄돼 있지 않다.** 확보본 1쪽에는 ACM 템플릿의 자리표시자
  (`Conference'04, Month 1–2, 2004, City, State, Country`)가 그대로 남아 있다. OOPSLA'04
  Companion pp.236–246이라는 서지는 **외부 근거**이고, 그 근거의 출처는
  [소스 메타](../sources/freeman2004-mock-roles.md)가 정본이다.

## 이름이 잘못됐다는 자기 규정

- **논문의 첫 두 문장이 기법의 이름을 부정한다** (§1):[^freeman2004-mock-roles]

  > Mock Objects is misnamed. It is really a technique for identifying types in a system
  > based on the roles that objects play.

  제목 "Mock Roles, not Objects"가 뜻하는 것이 이것이다 — 목으로 세우는 대상은 **클래스가
  아니라 역할(role)**이고, 목을 세우는 목적은 그 역할을 **찾아내는 것**이다.
- **초록이 같은 말을 반대편에서 적는다** (초록):[^freeman2004-mock-roles]

  > Mock Objects is an extension to Test-Driven Development that supports good
  > Object-Oriented design by guiding the discovery of a coherent system of types within a
  > code base. It turns out to be less interesting as a technique for isolating tests from
  > third-party libraries than is widely thought.

  **뒤 문장이 이 논문의 방향이다.** 서드파티 라이브러리로부터 테스트를 격리하는 것은 이
  기법의 **덜 흥미로운 쓰임**이라고 저자들이 적는다.
- **저자들이 자기 앞판에서 무엇이 바뀌었는지도 적는다** (§1) — 2001년 논문에서는 캡슐화
  보존·의존 감소·상호작용 명료화를 이득으로 들었는데, 2004년 저술 시점에는 **"the most important benefit
  of Mock Objects is what we originally called 'interface discovery'"**라고 적는다.
  강조점이 테스트에서 설계로 옮겨 갔다는 자기 서술이다.[^freeman2004-mock-roles]
- **결론이 그 이동을 한 번 더 적는다** (§9) — **"in particular we now have a much stronger
  bias towards using Mock Objects for design, rather than just testing."**[^freeman2004-mock-roles]

## 필요에서 인터페이스를 끌어낸다

- **논거의 출발이 객체 설계 쪽이다** (§1.2) — 잘 설계된 객체는 이웃(immediate neighbours)
  에게만 메시지를 보내고(디미터의 법칙), 그래서 객체는 **제공하는 서비스**와 **이웃에게
  요구하는 서비스**로 서술된다. 후자를 저자들이 **나가는 인터페이스(outgoing interfaces)**
  라고 부른다.[^freeman2004-mock-roles]
- **테스트가 그 나가는 인터페이스를 먼저 정한다** (§1.3) — 아직 존재하지 않는 나가는
  인터페이스로 테스트를 적을 수 있고, `dog.expressHappiness()`가 성공했다는 판정을
  `body.wagTail()`이 불렸는가로 내린다. `DogBody`에 그 메서드가 아직 없다면 **그 테스트가
  새 요구사항을 발견한 것**이다.[^freeman2004-mock-roles]
  - **여기서 곧바로 멈추지 않는 것이 기법의 요점이다** (같은 절) — 지금 그 기능을 구현하러
    가면 현재 과제에서 벗어나고 구현이 예측할 수 없이 길어질 수 있으므로, 대신 **그 역할을
    흉내 내는 가짜 구현을 세우고 호출됐는지만 확인한다.**[^freeman2004-mock-roles]
- **그 흐름에 이름이 붙는다** (§2.1):[^freeman2004-mock-roles]

  > TDD with Mock Objects guides interface design by the services that an object *requires*,
  > not just those it *provides*. This process results in a system of narrow interfaces each
  > of which defines a role in an interaction between objects, rather than wide interfaces
  > that describe all the features provided by a class. We call this approach *Need-Driven
  > Development*.

  - 저자들이 그 근거를 린 개발의 당김(pull) 원리에서 끌어온다 (같은 절) — 가치는 구현에서
    밀려 나오는 것이 아니라 수요에서 당겨져 나온다는 것이고, **"This is the flow of
    programming with Mock Objects."**[^freeman2004-mock-roles]
- **절차가 반복이다** (§2.1) — A를 테스트하며 필요한 서비스 S를 발견해 목으로 세우고, A를
  끝낸 뒤 초점을 옮겨 S 역할을 수행할 객체 B를 구현하며 다시 B가 필요로 하는 것을 발견해
  목으로 세운다. **시스템 런타임이나 외부 라이브러리로 실제 기능을 구현하는 층에 닿을
  때까지** 이어진다.[^freeman2004-mock-roles]
- **결과가 구조로 나타난다고 적는다** (§2.1·§3.7) — 응용이 **좁게 정의된 역할 인터페이스로
  소통하는 객체들의 합성**이 되고, 클래스 계층이 매우 평평해지는 경향이 있으며(취약한 기반
  클래스 문제를 피한다), 상속이 아니라 합성에 바탕한 스타일이 된다는 것이다.[^freeman2004-mock-roles]
- **위에서 아래로 내려가는 개발과 다른 점도 적는다** (§2.1) — 전통적 하향식은 가장 중요한
  결정을 일찍 내려야 하고 하위 구성요소 사이의 중복을 피하기 어려운데, TDD가 리팩터링을
  절차에 넣어 그것을 완화한다는 것이다. 상향식의 위험도 저자들의 경험으로 적는다 —
  **큰 과제의 일부로 지원 클래스를 따로 개발했다가 무언가를 오해해 결과가 맞지 않았던 일이
  저자 전원에게 있다.**[^freeman2004-mock-roles]

## 테스트를 거꾸로 쓴다

- **실제로 쓰는 순서가 실행 순서와 다르다고 적는다** (§3.6) — TDD 중의 사고 흐름을 따라
  여섯 단계로 쓴다는 것이다:[^freeman2004-mock-roles]

  1. 테스트할 객체를 정하고 필요한 인자와 함께 메서드 호출을 적는다
  2. 그 객체가 시스템의 나머지에게 **요구하는 서비스**를 기대(expectation)로 적는다
  3. 그 서비스들을 목 객체로 표현한다
  4. 테스트가 실행될 나머지 맥락을 만든다
  5. 사후 조건을 적는다
  6. 목을 검증한다

- **다섯째 단계가 자주 비는 것이 정상이라고 적는다** (같은 절) — "Tell, Don't Ask"를 따르면
  단정(assertion)을 걸 사후 조건이 없는 경우가 잦고, **객체들이 어떻게 소통하는지를 생각하지 않는
  프로그래머에게는 그것이 놀랍다**는 것이다.[^freeman2004-mock-roles]
- **첫 단계가 가장 자주 막히는 자리라고 적는다** (같은 절) — 테스트하는 객체와 **그 객체의
  역할**을 분명히 하는 것이 중요하고, 테스트를 쓰지 못하는 사람들에게서 그 혼동을 자주
  봤다는 것이다.[^freeman2004-mock-roles]

## 소유한 타입만 목한다 — 원래 근거

- **절 제목이 그 문장이다** (§4.1 "Only Mock Types You Own"). 문면 전부는
  이렇다:[^freeman2004-mock-roles]

  > Mock Objects is a design technique so programmers should only write mocks for types that
  > they can change. Otherwise they cannot change the design to respond to requirements that
  > arise from the process. Programmers should not write mocks for fixed types, such as
  > those defined by the runtime or external libraries. Instead they should write thin
  > wrappers to implement the application abstractions in terms of the underlying
  > infrastructure.

- **근거가 설계 변경 가능성 하나다.** 목이 설계 기법이므로 **바꿀 수 있는 타입에만** 쓴다는
  것이고, 바꿀 수 없으면 이 과정에서 나오는 요구에 설계로 응답할 수 없다는 것이다.
  **테스트가 실제 동작과 어긋날 위험이 근거로 등장하지 않는다.**
- **감싸개의 출처도 같은 절에 있다** (같은 절) — 그 얇은 감싸개는 따로 설계하는 것이 아니라
  **need-driven 테스트의 일부로 이미 정의돼 있을 것**이라고 적는다.[^freeman2004-mock-roles]
- **저자들이 이 지침의 효용을 명시한다** (같은 절):[^freeman2004-mock-roles]

  > It restores the pre-eminence of the design in the use of Mock Objects, which has often
  > been overshadowed by its use for testing interactions with third-party libraries.

  **곧 이 지침은 "목을 덜 쓰라"가 아니라 "목을 설계 도구로 되돌리라"는 것이다.** 지침의
  방향이 초록의 논지와 같다.
- **널리 유통되는 변형과 문면이 다르다.** "Don't mock what you don't own"은 이 논문의 문면이
  아니다. 이 KB의 다른 페이지가 그 변형을 곁글 제목으로 쓰는데, **그 소스는 출처를 적지
  않는다** — [가짜와 목](../concepts/fakes-versus-mocks.md)이 그 자리다.

## 저자들이 오해라고 부르는 것

**§5의 제목이 "MISCONCEPTIONS ABOUT MOCKS"이고, 여섯 항목이 전부 "사람들이 이렇게 알고
있는데 우리 생각은 다르다"의 형식이다.** 그 가운데 둘이 이 KB의 다른 페이지와 정면으로
갈린다.

- **② 목은 시스템 경계에서만 써야 한다** (§5.2 "Mock Objects should only be used at the
  boundaries of the system"):[^freeman2004-mock-roles]

  > We believe the opposite, that Mock Objects are most useful when used to drive the design
  > of the code under test. This implies that they are most useful *within* the system where
  > the interfaces can be changed. Mocks and stubs can still be useful for testing
  > interactions with third-party code, especially for avoiding test dependencies, but for
  > us this is a secondary aspect to the technique.

  **이 문단이 이 페이지에 걸린 모순의 축이다.** 경계 밖과의 통신을 목으로 검사하는 것은
  저자들에게 **부차적**이고, 목이 가장 유용한 자리는 **인터페이스를 바꿀 수 있는 시스템
  안쪽**이다.
- **⑤ 목이 리팩터링을 막는다 — 여러 테스트가 함께 깨지므로** (§5.5) — 저자들은 오히려
  객체 무리를 묶어 테스트하는 쪽에 두 가지 불리함이 있다고 적는다: 핵심 클래스가 바뀌면
  여러 테스트가(특히 코드보다 리팩터링하기 어려운 테스트 데이터가) 함께 바뀌어야 한다는
  것, 그리고 실패했을 때 **테스트와 실패한 코드의 연결이 덜 직접적이라** 원인을 찾기가 더
  복잡하고 최악의 경우 디버거가 필요하다는 것이다. 그리고 결론을
  적는다:[^freeman2004-mock-roles]

  > Our experience is that Mock Object-based test failures are more focussed and more
  > self-explanatory, reducing the turnaround on code changes.

- **나머지 넷도 함께 적어 둔다.**
  - **① 목은 그냥 스텁이다** (§5.1) — 스텁은 정해진 결과를 돌려주는 가짜 구현이고, **목은
    스텁 노릇을 하되 대상 객체와 이웃의 상호작용을 계측하는 단정까지 포함한다**는 것이
    저자들의 구분이다.[^freeman2004-mock-roles]
  - **③ 테스트 중에 상태를 모아 두었다가 나중에 단정한다** (§5.3) — 자기 션트(Self Shunt)
    패턴이 그 특수 사례다. 저자들은 반대 이유를 셋 든다: 실패가 오류 시점이 아니라 사후에
    나타난다는 것, 단정 구현이 테스트 코드 여기저기로 흩어져 지적 부담이 는다는 것, 그리고
    **가장 강한 반대**로 그 방식이 **대상 객체와 이웃의 상호작용에 초점을 맞추지 못한다**는
    것이다.[^freeman2004-mock-roles]
  - **④ 목으로 테스트하면 코드가 중복된다** (§5.4) — 대상 코드를 그대로 그림자처럼 베낀
    목 설정이 그렇게 되고, 이는 **서드파티 라이브러리를 목할 때 특히 흔하다**고 적는다.
    문제의 진단이 날카롭다 — 그때 목은 설계를 이끄는 데 쓰이는 것이 아니라 **남의 설계에
    맞춰지고 있다**는 것이다. 그리고 **"Complex mock setup for a test is actually a hint
    that there is a missing object in the design."**[^freeman2004-mock-roles]
  - **⑥ 메서드 이름을 문자열로 쓰는 것은 취약하다** (§5.6) — 리팩터링 도구가 문자열을 함께
    고치지 않는다는 지적이다. 저자들의 답은 **목 주도 코드베이스에서는 타입이 더 국소적으로
    쓰여 깨지는 테스트가 예상보다 적고, 깨져도 깔끔하게 깨져 고칠 것이 분명하다**는
    것이다.[^freeman2004-mock-roles]

## 나머지 실무 지침

§4에 아홉이 있고 위에서 §4.1을 이미 다뤘다. 나머지 여덟은 대부분 **목을 덜 쓰거나 더 좁게
쓰라는 쪽**이다 — 기법의 옹호문이 자기 제약을 함께 적는 자리다.

- **게터를 쓰지 않는다** (§4.2) — 기법의 출발점이 John Nolan이 낸 "게터 없이 코드를 써
  보라"는 과제였다고 적는다. 게터는 구현을 노출해 결합을 늘리고 책임이 엉뚱한 모듈에 남게
  한다.[^freeman2004-mock-roles]
- **일어나면 안 되는 일을 명시한다** (§4.3) — 어떤 메서드가 **불리면 안 된다**는 명세와
  그 메서드를 아예 언급하지 않은 명세는 다르다. 후자에서는 그 호출이 오류인지 읽는 사람이
  알 수 없다.[^freeman2004-mock-roles]
- **테스트에는 가능한 한 적게 명세한다** (§4.4) — 과잉 명세가 **깨지기 쉬운(brittle)**
  테스트를 만들고, 그런 테스트가 많은 스위트는 개발을 늦추고 리팩터링을 막는다. 해법은
  명세를 약하게 하거나 객체 구조가 잘못됐음을 인정하고 바꾸는 것이다. 저자들이 아인슈타인을
  빌려 적는다 — **"a specification should be as precise as possible, but not more
  precise."**[^freeman2004-mock-roles]
  - **이 지침이 이 논문 안에서 §5.5와 나란히 있다는 것이 중요하다.** 저자들은 목 기반
    테스트가 취약해질 수 있다는 것을 **알고 있고**, 그 원인을 기법이 아니라 과잉 명세와
    잘못된 객체 구조로 돌린다.
- **경계 객체는 목으로 테스트하지 않는다** (§4.5) — 다른 객체와 관계가 없는 객체(데이터를
  담거나 독립적으로 계산하거나 원자값을 표현하는 것)는 반환값을 단정하면 된다.[^freeman2004-mock-roles]
- **목에 동작을 더하지 않는다** (§4.6) — 목은 여전히 스텁이고 테스트 환경에 복잡성을 더해서는
  안 된다. **목이 입력을 해석해 또 다른 목을 돌려주게 되는 것**이 흔한 예이고, 그때
  **대상 코드가 아니라 테스트 기반 구조를 테스트할 위험**이 생긴다. 저자들은 이런 충동을
  **책임이 잘못 놓였다는 징후**로 읽는다.[^freeman2004-mock-roles]
- **바로 옆 이웃만 목한다** (§4.7) — 객체망을 헤집고 다녀야 하는 객체는 의존이 너무 많아
  취약하고, 그 징후가 **비슷한 목 객체망을 만들어야 해서 준비가 복잡하고 읽기 어려운
  테스트**다. 해법은 테스트 대상을 잘못 골랐는지 확인하거나 **사이를 잇는 역할을
  들이는 것**이다.[^freeman2004-mock-roles]
- **목이 너무 많다** (§4.8) — 전부 바로 옆 이웃이더라도 넘겨야 할 목이 너무 많으면 같은
  문제다. 해법은 어긋난 책임을 고치거나 중간 역할을 들이는 것, 아니면 **대상 객체가 너무
  커서 쪼개야 하는 것**이다.[^freeman2004-mock-roles]
- **새 객체를 만드는 자리** (§4.9) — 대상 코드 안에서 생성되는 객체와의 상호작용은 테스트할
  수 없으므로 생성에 개입해야 한다. 인스턴스를 넘기거나 생성을 감싸는데, 팩터리 객체는
  생성 인자에 기대를 걸 수 있는 대신 새 타입을 요구하고 팩터리 메서드는 가볍지만 하위
  클래스 재정의에 기댄다. **끝에 판정이 하나 붙는다** — 관점 지향 프로그래밍이나 클래스
  로더 조작으로 실제 객체를 바꿔치는 방식은 외부 의존을 걷어 내는 데는 쓸모 있지만
  **코드베이스의 설계를 개선하는 데는 도움이 되지 않는다**는 것이다.[^freeman2004-mock-roles]

## 도구가 기법을 강제한다

- **jMock을 만든 이유가 리듬이다** (§6) — 테스트를 쓰다가 목 구현을 쓰러 멈춰야 하면 TDD의
  리듬이 끊긴다. 1세대 목 라이브러리가 그 문제를 안고 있었고, jMock은 실행 시점 동적 코드
  생성으로 목을 만들어 그 멈춤을 없앴다.[^freeman2004-mock-roles]
- **도구가 요청을 거절한 목록이 이 논문에서 가장 또렷한 자기 규정이다**
  (§6.3):[^freeman2004-mock-roles]

  > jMock is primarily designed to support Need-Driven Development. As such, the API may be
  > less applicable in other scenarios. Users have asked us to modify jMock to help them
  > perform integration testing, do procedural programming, avoid refactoring poorly
  > designed code, and mock concrete classes, but we have politely declined.

  **통합 테스트 지원과 구체 클래스 목하기가 거절 목록에 있다.** 이 KB의 다른 페이지가
  목을 통합 테스트 전용으로 두라고 적는 자리와 정면으로 마주 본다.
- **정밀도를 조절할 수 있게 만든 것도 §4.4의 지침을 도구로 옮긴 것이다** (§6.2) — 인자를
  값이 아니라 제약(constraint)으로 적게 해서 테스트와 무관한 측면을 무시할 수 있게 하고,
  호출 순서 제약은 **테스트를 너무 취약하게 만들 수 있으므로 조심해서 쓰라**고 적으며 부분
  순서만 지정할 수 있게 했다.[^freeman2004-mock-roles]
- **실패 메시지를 위해 만든 장치가 둘 있다** (§6.4) — 자기 서술 값(Self Describing Value)은
  실제처럼 보이는 값(`invoice.xml`) 대신 역할을 말하는 값(`OPENED-FILE-NAME`)을 쓰는
  것이고, 더미 객체(Dummy Object)는 테스트 중 실제로 호출되지 않는 객체다.[^freeman2004-mock-roles]

## 저자들이 스스로 적은 미해결

- **§8 "FURTHER WORK"에 이 기법의 구조적 한계가 적혀 있다.** 목을 쓴 테스트는 대상 객체가
  기대한 나가는 호출을 하는지 검증하지만,[^freeman2004-mock-roles]

  > this does not test that all objects that use the same interface use that interface in a
  > consistent way, or are consistent with implementers of that interface.

  - **2004년 저술 시점의 대응이 통합 테스트와 종단 수용 테스트라고 적는다** (같은 절) — 그것이 통합
    오류를 잡기는 하지만 **원인을 짚어 내기가 복잡하다**는 것이다. 객체 사이의 프로토콜을
    명시적으로 서술해 클라이언트와 구현자의 일관성을 검사하는 API를 만들고 있다고 적는다.
  - **곧 "목한 역할이 실제 구현과 맞는가"는 이 기법 안에서 풀리지 않는다.** 이것은 이
    KB의 다른 페이지가 목을 좁게 쓰라고 할 때 드는 근거와 같은 문제이고, **저자들이 그것을
    인정한다.**
- **기법이 설계를 대신하지 못한다는 것도 저자들이 적는다** (§4 도입) — **"Mock Objects is a
  design aid, but is no substitute for skilled developers."** 시스템 설계가 약하면 목 기반
  테스트가 금세 너무 복잡해지고, 목의 사용이 **강한 결합과 잘못 배치된 책임 같은 문제를
  증폭한다**는 것이다. 그때의 대응으로 목을 그만 쓰는 쪽이 있지만 저자들은 설계를 고치는
  동기로 쓰는 편이 낫다고 판정한다.[^freeman2004-mock-roles]
- **예제 자체의 흠도 적어 둔다** (§3.7) — 워크드 예제의 `TimedCache`는 **상위 클라이언트가
  요구를 이끌어 내지 않았다**는 점에서 이 기법의 정상 절차가 아니라는 것이다.[^freeman2004-mock-roles]

## 모순 — 무엇이 갈리는가

**이 페이지는 [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md)와 모순 관계에
있다. 그 모순은 이 런에서 해소하지 않는다.**

- **먼저 갈리지 않는 것부터 적는다 — "소유한 타입만 목하라"는 공통 지반이다.** 저쪽 소스는
  이 지침을 자기 넷째 지침으로 채택하며 **"I fully agree with this analysis"**라고 적는다.
  **반입 판정 대장은 이 논문을 저쪽의 "정확한 역명제"로 기재했으나, 원문 대조 결과 그
  기재는 틀렸다.** 다만 **채택된 것은 지침이고 근거는 다르다** — 이 논문의 근거는 설계를
  바꿀 수 있는가이고, 저쪽의 근거는 서드파티 동작을 알 수 없다는 것과 어댑터가 부패 방지
  계층이 된다는 것이다.
- **실제로 갈리는 축은 시스템 안쪽이다.**

  | | 이 페이지(freeman 2004) | [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md)(khorikov) |
  |---|---|---|
  | 목이 가장 유용한 자리 | **시스템 안쪽** — 인터페이스를 바꿀 수 있는 곳(§5.2) | **시스템의 가장 바깥 가장자리** — unmanaged 의존과의 통신 |
  | 클래스 사이의 통신 | 발견해야 할 **역할**이고 설계의 산출물 | **구현 세부**이고 관찰 가능한 행위가 아니다 |
  | 시스템 경계에서의 목 | **부차적**(secondary aspect) | 목의 **유일한** 정당한 자리 |
  | 목 기반 테스트의 취약성 | 과잉 명세와 나쁜 설계의 문제이고, 실패는 오히려 더 또렷하다(§4.4·§5.5) | 목이 구현 세부에 결합하므로 **리팩터링 내성을 잃는다** |
  | 목을 어느 테스트에 두는가 | 설계를 이끄는 프로그래머 테스트 | **통합 테스트에만** 둔다 |
  | 통합 테스트 지원 | 도구가 그 요청을 **거절**했다(§6.3) | 목이 사는 유일한 자리 |

- **최대 하나만 참인 자리가 넷째 줄이다.** 한쪽은 시스템 안쪽 협력자를 목으로 검사한
  테스트가 리팩터링을 방해한다고 하고, 다른 쪽은 그 주장을 오해로 이름 붙이며 오히려 실패가
  더 초점 맞고 자명해진다고 적는다. **둘 다 측정이 아니라 저자들의 경험 진술이므로 이 KB는
  어느 쪽도 실증으로 인용하지 않는다.**
- **양쪽 다 실증이 없다는 것이 이 모순의 성격이다.** 무엇이 실제로 목으로 대체되는지의
  실측은 [실제 프로젝트에서 무엇이 목으로 대체되는가](what-gets-mocked-in-practice.md)에
  있고, 그 실측은 **어느 쪽 처방도 지지하지 않는다** — 그리고 그 실측 가운데 하나가 이
  물음을 미해결로 명시한다.
- **모순을 해소하려면 무엇이 필요한지도 적어 둔다.** 두 주장은 "시스템 안쪽 협력자를 목으로
  검사한 테스트가 리팩터링에서 얼마나 깨지는가"라는 **측정 가능한 물음**으로 환원된다.
  **이 KB에 그 값을 잰 소스가 없다.**

## 이 소스의 사각

- **측정이 없다.** 위 "지위" 절이 정본이다. 이 논문의 모든 판정은 네 저자와 지인들의 경험
  진술이다.
- **설계 품질을 무엇으로 재는지가 없다.** 좁은 역할 인터페이스와 평평한 클래스 계층이 더 좋은
  설계라는 것이 전제이고, 그 전제를 재는 잣대가 논문에 없다.
- **목한 역할과 실제 구현의 일관성이 풀리지 않는다.** 저자들이 §8에서 인정한다.
- **경계면의 값어치가 부차적이라는 판정에 근거가 없다.** §5.2가 그렇게 적을 뿐이고, 어느
  쪽이 더 많은 결함을 잡는지 잰 값이 없다.
- **언어와 시대가 매여 있다.** 2004년 자바이고, 도구 예시가 전부 그 시점의 jMock 문법이다.
  동적 언어와 모킹 프레임워크가 흔해진 뒤에도 이 판정이 유지되는지는 이 논문의 주제가 아니다.
- **언어 모델 시대의 재검이 없다.** 생성된 테스트가 역할을 발견하는 도구로 목을 쓰는지,
  아니면 격리 도구로만 쓰는지는 이 논문이 답하지 않는다. **이 페이지의 판정은 경험 법칙의
  지위로 인용한다.**

## 용어에 대하여

- **`need-driven development`는 원어를 유지한다.** 확립 역어가 없고, 이 KB가 새 역어를 지으면
  그 낱말이 검색에서 원문과 끊긴다. 뜻은 **필요가 인터페이스를 끌어낸다**는 것이고, 이
  페이지는 그 풀이를 쓰되 역어로 채택하지 않는다.
- **역할(role)**과 **협력자(collaborator)**는 역어를 쓰고 첫 등장에 원어를 병기했다. 이
  논문이 쓰는 낱말은 `role`과 `neighbour`이고, `collaborator`는 이 논문이 §1.2에서 인용한
  Beck & Cunningham 문면에 있다.
- **모킹 프레임워크(mocking framework)**는 이 논문의 낱말이 아니다 — 이 논문은
  `Mock Object framework`라고 적는다. 이 KB가 실증 두 편과 어휘를 맞추려고 쓰는 말이며,
  같은 것을 가리킨다.
- **런던 학파·모키스트라는 이름은 이 논문에 없다.** 그 이름은 이 논문 밖에서 이 계보에
  붙은 것이고, 어디서 지어졌는지는
  [대역 어휘와 두 TDD 스타일](test-double-vocabulary-and-tdd-styles.md)이 정본이다.

## 이어지는 페이지

- [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md) — **모순 상대.** 위
  [모순](#모순--무엇이-갈리는가)의 표가 갈리는 자리를 소유한다
- [실제 프로젝트에서 무엇이 목으로 대체되는가](what-gets-mocked-in-practice.md) — 이 논문의
  처방이 현장에서 어떻게 되는지를 잰 자리. **이 논문의 §4.1을 정면으로 어기는 값이 거기
  있다** — 아파치 프로젝트의 목 객체 가운데 다수가 **자기가 소유하지 않은 라이브러리
  클래스**를 대체한다
- [대역 어휘와 두 TDD 스타일](test-double-vocabulary-and-tdd-styles.md) — 이 논문의 계보에
  **모키스트·런던 학파**라는 이름을 붙인 자리. 그 글이 두 스타일의 원전으로 이 저자들을
  지목하면서 판정을 유보한다
- [가짜와 목](../concepts/fakes-versus-mocks.md) — "가진 적 없는 것을 목하지 마라"를 곁글 제목으로
  쓰되 **출처를 적지 않는** 소스. 그 표어의 원문 형태가 이 페이지의
  [§4.1](#소유한-타입만-목한다--원래-근거)이고, **근거가 다르다** — 그쪽은 지저분한 하위
  시스템 위에 단순한 추상을 세우게 만드는 어림 규칙으로 쓰고, 이쪽은 설계를 바꿀 수 있게
  하려고 쓴다
- [테스트 대역 선호 순서와 규모 전제](test-double-preference-at-scale.md) — 같은 물음에
  **대규모 조직의 선호 순서**로 답한 자리. 그쪽이 상호작용 검증을 가장 뒤로 미루므로 이
  페이지와 방향이 반대이고, 그쪽의 근거는 취약성이 아니라 **한 API가 수만 번 목으로 대체될
  때 생기는 문제**다
- [리팩터링 내성과 거짓 양성](resistance-to-refactoring-and-false-positives.md) — 위
  [모순](#모순--무엇이-갈리는가)의 넷째 줄에 이름과 잣대를 준 자리. 이 논문 §5.5가 오해라고
  부르는 주장이 거기서는 잣대의 지위에 있다
- [의존성 주입과 부트스트랩](dependency-injection-and-bootstrap.md) — 이 논문 §3.3.1이
  **"everything that the TimedCache needs is passed into it"**이라고 적는 자리의 실물.
  저자들은 그것이 목으로 이웃을 바꿔치기 위해 **강제되는** 것이고 그 강제가 강점이라고 적는다
- [테스트가 코딩을 이끈다](test-to-code.md) — TDD를 설계 활동으로 보는 같은 주장의 다른 판본
- [대역과 단위 테스트의 가치](../synthesis/test-doubles-and-unit-test-value.md) — **이 갈래의 허브.** 이 논문의
  처방과 그 모순 상대가 거기서 한 쌍으로 보존된다

[^freeman2004-mock-roles]: Freeman, Pryce, Mackinnon & Walnes, "Mock Roles, not Objects",
    2004, 확보본 11쪽 PDF(jmock.org). **쪽 번호가 아니라 절 번호가 locator다** — 초록 ·
    §1 "Introduction"(§1.1~§1.3) · §2 "Mock Objects and Need-Driven Development"(§2.1) ·
    §3 "A Worked Example"(§3.3.1 · §3.6 · §3.7) · §4 "Mock Objects in Practice"(§4.1~§4.9) ·
    §5 "Misconceptions about Mocks"(§5.1~§5.6) · §6 "jMock"(§6.1~§6.4) ·
    §8 "Further Work" · §9 "Conclusions". 직인용은 확보본 문면 그대로다. 2단 조판이라
    기계 추출본에서 본문과 코드가 섞이므로 직인용은 문장 단위로 육안 확인했다. 자바 예제
    코드(TimedCache · jMock API)는 2004년 문법이라 펜스로 옮기지 않았고 개념 설명에 필요한
    조각만 인라인 표기로 남겼다. Figure 1~4는 이미지 조판이라 그림에서만 읽히는 것은 옮기지
    않았다. 학회명·쪽수·DOI가 확보본에 인쇄돼 있지 않다는 사실과 그 외부 근거, 저자 순서가
    자리마다 다르다는 사실, 인용 규약은 [소스 메타](../sources/freeman2004-mock-roles.md)가
    정본이다.

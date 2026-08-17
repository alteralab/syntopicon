---
type: concept
title: 캡슐화 리팩터링
description: 모듈 분해의 기준을 파나스의 비밀에 두고 그 비밀을 감추는 아홉 항목 — 레코드와 컬렉션 캡슐화, 기본형을 객체로 바꾸는 항목이 왜 가장 값진 것으로 꼽히는가, 임시 변수를 질의로 바꾸기, 클래스 추출과 인라인의 쌍과 쪼갤 축을 찾는 시험, 위임 숨기기와 중개자 제거가 정답 없는 조정 관계라는 판정, 그리고 알고리즘 통째 교체
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 캡슐화 리팩터링

- [이 장이 묶는 축 — 파나스의 비밀](#이-장이-묶는-축--파나스의-비밀)
- [자료 구조를 감추기 — Encapsulate Record와 Encapsulate Collection](#자료-구조를-감추기--encapsulate-record와-encapsulate-collection)
- [Replace Primitive with Object — 가장 값진 항목으로 꼽히는 것](#replace-primitive-with-object--가장-값진-항목으로-꼽히는-것)
- [Replace Temp with Query — 변수를 함수로](#replace-temp-with-query--변수를-함수로)
- [Extract Class — 쪼갤 축을 찾는 법](#extract-class--쪼갤-축을-찾는-법)
- [Inline Class — 그 역과 재조직 전술](#inline-class--그-역과-재조직-전술)
- [Hide Delegate와 Remove Middle Man — 정답이 없는 조정](#hide-delegate와-remove-middle-man--정답이-없는-조정)
- [Substitute Algorithm — 통째로 갈아 끼우기](#substitute-algorithm--통째로-갈아-끼우기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모듈이 감춰야 할 것은 무엇이고, 이미 드러나 있는 것을 어떤 수순으로 감추는가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축 — 파나스의 비밀

- 장 전체의 기준이 첫 문장에 있다 (7장, p.161):[^fowler2018]

> Perhaps the most important criteria to be used in decomposing modules is to identify
> secrets that modules should hide from the rest of the system [Parnas].

  - 이 인용의 원전이 파나스(David Parnas)이고, 같은 기준을 잣대로 세운 다른 소스의 서술은
    [정보 은닉과 정보 누출](information-hiding-and-leakage.md)에 있다.
- **가장 흔한 비밀이 자료 구조라고 못 박는다** — **자료 구조가 가장 흔한 비밀이고, 나는
  *Encapsulate Record*(p.162)와 *Encapsulate Collection*(p.170)으로 그것을 캡슐화해 감출 수
  있다. 기본형 데이터 값조차 *Replace Primitive with Object*(p.174)로 캡슐화할 수 있는데, 그렇게
  해서 나오는 2차 이득의 크기가 흔히 사람들을 놀라게 한다** (7장, p.161).[^fowler2018]
- 장의 나머지 배열도 저자가 밝힌다 (7장, p.161):[^fowler2018] 임시 변수가 리팩터링을
  방해하므로 *Replace Temp with Query*(p.178)가 특히 긴 함수를 쪼갤 때 큰 도움이 되고,
  **클래스는 정보 은닉을 위해 설계됐으므로** 추출과 인라인이 클래스에도 적용되며
  (*Extract Class*(p.182)·*Inline Class*(p.186)), 클래스 사이의 연결도 *Hide
  Delegate*(p.189)로 감출 수 있으나 **너무 많이 감추면 부푼 인터페이스로 이어지므로** 그 역인
  *Remove Middle Man*(p.192)도 필요하다. 마지막으로 함수도 자기 구현을 캡슐화하므로
  *Extract Function*(p.106)으로 감싼 뒤 *Substitute Algorithm*(p.195)으로 통째 교체할 수 있다.

## 자료 구조를 감추기 — Encapsulate Record와 Encapsulate Collection

- **Encapsulate Record**(p.162, 초판 이름 *Replace Record with Data Class*) — 레코드 대신
  객체를 쓰는 근거가 **저장된 값과 계산된 값의 구분을 지우는 것**이다 — **객체를 쓰면 무엇이
  저장돼 있는지 감추고 세 값 모두에 메서드를 제공할 수 있다. 객체 사용자는 어느 것이 저장돼
  있고 어느 것이 계산되는지 알거나 신경 쓸 필요가 없다** (7장 §"Encapsulate Record",
  p.162).[^fowler2018]
  - **이름 바꾸기에도 쓰인다** — **이 캡슐화는 이름 바꾸기에도 도움이 된다. 새 이름과 옛 이름
    양쪽에 메서드를 제공하면서 필드 이름을 바꾸고 호출자를 점진적으로 갱신할 수 있다** (7장
    §"Encapsulate Record", p.162).[^fowler2018]
  - **가변 데이터에 한정된 주장이다** — **불변 값이라면 필요하면 보강 단계를 써서 세 값을 다
    레코드에 넣어 두면 된다. 마찬가지로 이름을 바꿀 때 필드를 복사하기도 쉽다** (7장
    §"Encapsulate Record", p.162).[^fowler2018]
  - **해시맵의 약점이 지목된다** — 필드 이름을 선언하는 레코드와 아무거나 쓰게 하는 레코드(해시·
    맵·딕셔너리) 중 뒤엣것은 **자기 필드에 대해 명시적이지 않다는 약점이 있다. `start`/`end`를
    쓰는지 `start`/`length`를 쓰는지 알 수 있는 유일한 방법은 그것이 생성되고 쓰이는 자리를
    보는 것이다.** 프로그램의 작은 구역에서만 쓰이면 문제가 아니지만 **사용 범위가 넓을수록
    그 암묵적 구조에서 더 큰 문제를 얻는다** (7장 §"Encapsulate Record",
    pp.162–163).[^fowler2018]
  - JSON·XML로 직렬화되는 중첩 구조도 캡슐화 대상이고, **나중에 형식이 바뀌거나 추적하기 어려운
    갱신이 걱정될 때 도움이 된다** (7장 §"Encapsulate Record", p.163).[^fowler2018]
- **Encapsulate Collection**(p.170) — 이 항목 전체가 하나의 흔한 실수를 겨냥한다 — **캡슐화는
  흔히 권장되지만, 컬렉션을 다룰 때 흔한 실수가 일어난다. 컬렉션 변수에 대한 접근은 캡슐화돼
  있으나 게터가 컬렉션 자체를 반환하면 그 컬렉션의 구성원이 감싼 클래스가 개입할 수 없는 채로
  바뀔 수 있다** (7장 §"Encapsulate Collection", p.170).[^fowler2018]
  - 그래서 처방이 두 겹이다 — 클래스 자신에 `add`·`remove` 같은 **컬렉션 수정 메서드**를 두고,
    **게터가 원본 컬렉션을 반환하지 않게 한다.** 팀 습관에 기대는 것에는 명시적으로 반대한다 —
    **그런 습관에 기대는 것은 보통 현명하지 않다. 여기서의 실수 하나가 나중에 추적하기 어려운
    버그로 이어질 수 있다** (7장 §"Encapsulate Collection", p.170).[^fowler2018]
  - **저자가 기각하는 방법이 하나 명시된다** — 컬렉션 값을 결코 반환하지 않고 `aCustomer.orders.size`
    를 `aCustomer.numberOfOrders`로 바꾸는 접근에 대해 — **나는 이 접근에 동의하지 않는다. 현대
    언어는 표준화된 인터페이스를 가진 풍부한 컬렉션 클래스를 갖고 있고 그것은 컬렉션 파이프라인
    같은 유용한 방식으로 조합될 수 있다. 이런 기능을 다루려고 특수 메서드를 넣으면 코드가 많이
    늘고 컬렉션 연산의 쉬운 조합 가능성을 망친다** (7장 §"Encapsulate Collection",
    pp.170–171).[^fowler2018]
  - 남는 선택지는 **읽기 전용 프록시**와 **복사본**이고, 저자는 복사본 반환이 아마 가장 흔한
    접근이라고 적는다. 둘의 차이도 명시된다 — **원본 데이터의 수정이 프록시에는 보이지만
    복사본에는 보이지 않는다** (7장 §"Encapsulate Collection", p.171).[^fowler2018] 컬렉션이
    거대하면 복사가 성능 문제일 수 있으나 **대부분의 목록은 그리 크지 않으므로 성능에 대한
    일반 규칙을 적용하면 된다.**
  - **판정은 일관성으로 닫는다** — **여기서 중요한 것은 코드베이스 안의 일관성이다. 한 기제만
    써서 모두가 그것이 어떻게 동작하는지 익숙해지고 컬렉션 접근자 함수를 호출할 때 그것을
    기대할 수 있게 하라** (7장 §"Encapsulate Collection", p.171).[^fowler2018] 같은 대상을
    다루는 다른 소스의 판정은 [일관성](consistency-in-code.md)에 있다.

## Replace Primitive with Object — 가장 값진 항목으로 꼽히는 것

- 발생 경로가 개발 초기의 합리적 결정이다 — **개발 초기 단계에는 단순한 사실을 숫자나 문자열
  같은 단순한 데이터 항목으로 표현하기로 결정하는 일이 흔하다. 개발이 진행되면 그 단순한
  항목들이 더 이상 그리 단순하지 않다** (7장 §"Replace Primitive with Object",
  p.174).[^fowler2018] 전화번호가 한동안 문자열이다가 서식화·지역번호 추출 같은 특수 행동이
  필요해지고, **그런 로직은 코드베이스 여기저기에서 빠르게 중복으로 끝난다.**
- 처방의 시점이 명시적이다 — **단순 출력 말고 다른 것을 하고 싶다고 깨닫는 즉시 나는 그 데이터
  조각을 위한 새 클래스를 만든다. 처음에 그런 클래스는 기본형을 감싸는 것 이상을 거의 하지
  않는다 — 그러나 일단 그 클래스를 갖게 되면 그 필요에 맞는 행동을 놓을 자리가 생긴다** (7장
  §"Replace Primitive with Object", p.174).[^fowler2018]
- **이 항목이 두꺼운 이유가 저자 자신의 평가에 있다** (7장 §"Replace Primitive with Object",
  p.174):[^fowler2018]

> These little values start very humble, but once nurtured they can grow into useful
> tools. They may not look like much, but I find their effects on a code base can be
> surprisingly large. Indeed many experienced developers consider this to be one of the
> most valuable refactorings in the toolkit—even though it often seems counterintuitive
> to a new programmer.

- 수순이 짧다 — 필요하면 *Encapsulate Variable*(p.132)을 먼저 적용하고, 그 데이터 값을 위한
  **단순한 값 클래스**를 만들어 생성자로 기존 값을 받고 게터를 제공한다. 세터가 새 인스턴스를
  만들어 필드에 저장하게 바꾸고 게터가 새 클래스의 게터 결과를 반환하게 바꾼다. 그다음 원래
  접근자에 *Rename Function*(p.124)을 검토하고, 새 객체의 역할을 값이냐 참조냐로 분명히 하려면
  *Change Reference to Value*(p.252)나 *Change Value to Reference*(p.256)를 적용한다 (7장
  §"Replace Primitive with Object", p.175).[^fowler2018] 뒤의 두 항목은
  [데이터 조직화 리팩터링](organizing-data.md)에 있다.
- 3장이 이 항목을 기본형 집착(Primitive Obsession)의 첫 처방으로 지목하고, `stringly typed`
  라는 별명이 그 냄새에 붙어 있다 — [코드의 나쁜 냄새](code-smells.md) 참조.

## Replace Temp with Query — 변수를 함수로

- 임시 변수의 정당한 용도부터 인정한다 — **임시 변수의 한 용도는 어떤 코드의 값을 붙잡아
  함수 안에서 나중에 참조하는 것이다. 임시 변수를 쓰면 그 값의 뜻을 설명하면서 값을 참조할 수
  있고 계산하는 코드를 반복하지 않아도 된다** (7장 §"Replace Temp with Query",
  p.178).[^fowler2018]
- 그럼에도 한 걸음 더 가는 이득 셋 (7장 §"Replace Temp with Query",
  pp.178–179):[^fowler2018]
  - **큰 함수를 쪼갤 때 추출이 쉬워진다** — 추출한 함수에 변수를 넘길 필요가 사라진다.
  - **로직을 함수에 넣으면 추출된 로직과 원래 함수 사이에 더 강한 경계가 서므로** 어색한 의존과
    부작용을 발견하고 피하는 데 도움이 된다.
  - 비슷한 함수들에서 같은 방식으로 계산되는 변수를 하나의 함수로 만들어 **계산 로직의 중복을
    없앤다.**
- **적용 조건이 좁다** — **일부 임시 변수만 이 리팩터링에 적합하다. 변수는 한 번 계산된 뒤 나중에
  읽히기만 해야 한다. (…) 나아가 변수를 계산하는 데 쓰인 로직이 나중에 그 변수가 쓰일 때도 같은
  결과를 내야 한다 — 그래서 `oldAddress` 같은 이름의 스냅샷용 변수는 제외된다** (7장
  §"Replace Temp with Query", p.179).[^fowler2018]
- **클래스 안에서 가장 잘 동작한다** — 클래스가 추출되는 메서드들에 공유 맥락을 주기 때문이고,
  클래스 밖에서는 **최상위 함수의 매개변수가 너무 많아져 함수를 쓰는 이득의 상당 부분이
  상쇄되기 쉽다** (7장 §"Replace Temp with Query", p.179).[^fowler2018]
- 수순에 안전장치가 있다 — 추출한 함수에 **부작용이 없음을 확인**하고, 있으면
  *Separate Query from Modifier*(p.306)를 먼저 쓴다 (7장 §"Replace Temp with Query",
  p.179).[^fowler2018]

## Extract Class — 쪼갤 축을 찾는 법

- 문제 규정이 지침에 대한 냉소로 시작한다 — **클래스는 산뜻한 추상이어야 하고 몇 개의 명확한
  책임만 다뤄야 한다는 지침을 읽어 봤을 것이다. 실제로는 클래스가 자란다. 여기에 연산 몇 개,
  저기에 데이터 조금을 더한다. 별도 클래스를 만들 가치는 없다고 느끼며 책임 하나를 클래스에
  더한다 — 그러나 그 책임이 자라고 번식하면서 클래스는 너무 복잡해진다** (7장 §"Extract
  Class", p.182).[^fowler2018]
- **쪼갤 축을 찾는 신호 셋** (7장 §"Extract Class", p.182):[^fowler2018]
  - **데이터의 부분집합과 메서드의 부분집합이 함께 가는 것으로 보일 때.**
  - **보통 함께 바뀌거나 특히 서로 의존적인 데이터의 부분집합**이 있을 때.
  - **나중에 나타나는 신호로는 클래스가 서브타이핑되는 방식.** 서브타이핑이 몇몇 기능에만
    영향을 주거나, 어떤 기능은 이쪽으로 어떤 기능은 저쪽으로 서브타이핑돼야 할 때다.
- **판정 시험이 하나 있다** (7장 §"Extract Class", p.182):[^fowler2018]

> A useful test is to ask yourself what would happen if you remove a piece of data or a
> method. What other fields and methods would become nonsense?

  - 3장 데이터 뭉치(Data Clumps)의 시험("데이터 값 하나를 지우면 나머지가 말이 되는가")과 같은
    형태이고, 이쪽은 클래스 안쪽에 적용한다.
- 수순의 순서에 이유가 붙는다 — 새 자식 클래스를 만들고, **원래 부모 클래스의 책임이 더 이상 그
  이름에 맞지 않으면 부모의 이름을 바꾸고**, *Move Field*(p.207)로 필드를 하나씩,
  *Move Function*(p.198)으로 메서드를 옮기되 **저수준 메서드(호출하는 쪽이 아니라 불리는
  쪽)부터 시작한다.** 옮길 때마다 테스트한다. 마지막에 **두 클래스의 인터페이스를 다시 보고
  불필요한 메서드를 없애고 새 상황에 맞게 이름을 고친다** (7장 §"Extract Class",
  p.183).[^fowler2018]
- 3장이 이 항목을 여러 냄새의 처방으로 지목한다 — 데이터 뭉치, 임시 필드, 거대한 클래스, 발산하는
  변경. [코드의 나쁜 냄새](code-smells.md) 참조.

## Inline Class — 그 역과 재조직 전술

- 첫째 용법은 소진된 클래스를 접는 것이다 — **클래스가 더 이상 제 몫을 하지 않고 더는 있을
  이유가 없으면 Inline Class를 쓴다. 흔히 이것은 다른 책임을 클래스 밖으로 옮기는 리팩터링의
  결과라 남은 것이 거의 없는 상태다** (7장 §"Inline Class", p.186).[^fowler2018]
- **둘째 용법이 이 항목의 진짜 쓰임새다** — **두 클래스를 기능 배분이 다른 한 쌍으로 리팩터링하고
  싶을 때다. 먼저 Inline Class로 둘을 한 클래스로 합친 다음 *Extract Class*(p.182)로 새 분리를
  만드는 것이 더 쉬울 수 있다** (7장 §"Inline Class", p.186).[^fowler2018]
  - 그리고 이것이 일반 원리로 승격된다 (7장 §"Inline Class", p.186):[^fowler2018]

> This is a general approach when reorganizing things: Sometimes, it's easier to move
> elements one at a time from one context to another, but sometimes it's better to use
> an inline refactoring to collapse the contexts together, then use an extract
> refactoring to separate them into different elements.

  - 3장의 산탄총 수술(Shotgun Surgery) 처방에 나오는 "중간 단계로 일부러 크게 만드는 전술"이
    같은 원리의 다른 판이다 — [코드의 나쁜 냄새](code-smells.md) 참조.

## Hide Delegate와 Remove Middle Man — 정답이 없는 조정

- **Hide Delegate**(p.189) — **좋은 모듈 설계의 열쇠 중 하나 — 열쇠가 아니라면 — 는 캡슐화다.
  캡슐화는 모듈이 시스템의 다른 부분에 대해 덜 알아도 된다는 뜻이다. 그러면 무언가 바뀔 때 더
  적은 모듈에만 그 변경을 알리면 되고 — 그것이 변경을 더 쉽게 만든다** (7장 §"Hide Delegate",
  p.189).[^fowler2018]
  - 그리고 캡슐화 대상의 확장이 명시된다 — **객체지향을 처음 배울 때 우리는 캡슐화가 필드를
    감추는 것이라고 배운다. 더 노련해지면 캡슐화할 수 있는 것이 더 있다는 것을 깨닫는다** (7장
    §"Hide Delegate", p.189).[^fowler2018] 서버 객체의 필드에 있는 위임 객체(delegate)의
    메서드를 클라이언트가 직접 부르면 클라이언트가 그 위임 객체를 알아야 하고, **위임 객체가
    인터페이스를 바꾸면 변경이 그 서버를 쓰는 모든 클라이언트로 전파된다.**
- **Remove Middle Man**(p.192) — 그 대가를 청구한다 — **클라이언트가 위임 객체의 새 기능을 쓰고
  싶을 때마다 나는 서버에 단순 위임 메서드를 하나 더해야 한다. 한동안 기능을 더하다 보면 이
  모든 전달에 짜증이 난다. 서버 클래스는 그저 중개자이고, 어쩌면 클라이언트가 실제로 무슨 일이
  일어나는지 아는 객체와 이야기할 때다** (7장 §"Remove Middle Man", p.192).[^fowler2018]
  - **디미터 법칙에 거리를 둔다** — **이 냄새는 사람들이 디미터 법칙을 따르는 데 지나치게
    열광할 때 흔히 튀어나온다. 그것이 "가끔 유용한 디미터의 제안"이라고 불렸다면 나는 그것을
    훨씬 더 좋아했을 것이다** (7장 §"Remove Middle Man", p.192).[^fowler2018]
- **두 항목을 함께 읽어야 하는 근거가 명시돼 있다** (7장 §"Remove Middle Man",
  p.192):[^fowler2018]

> It's hard to figure out what the right amount of hiding is. Fortunately, with *Hide
> Delegate (189)* and Remove Middle Man, it doesn't matter so much. I can adjust my code
> as time goes on. As the system changes, the basis for how much I hide also changes. A
> good encapsulation six months ago may be awkward now. Refactoring means I never have
> to say I'm sorry—I just fix it.

  - 이 문단이 카탈로그 전체의 성격을 압축한다 — **역을 함께 갖추는 것이 판정의 부담을 낮춘다.**
    5장이 역 항목 중 흥미로운 것만 실었다고 밝힌 것과 짝을 이룬다 —
    [리팩터링 카탈로그를 읽는 법](refactoring-catalog-format.md) 참조.
  - 3장이 메시지 체인(Message Chains)과 중개자(Middle Man)를 서로의 반작용으로 배치한 것도 같은
    쌍이다. 결합의 눈금 쪽 정본은 [결합 끊기](decoupling.md)에 있다.

## Substitute Algorithm — 통째로 갈아 끼우기

- 계기가 둘이다 — **더 명료한 방법을 찾으면 복잡한 방법을 명료한 방법으로 바꾼다. (…) 이것은 내가
  문제에 대해 더 배우고 더 쉬운 방법이 있다는 것을 깨달을 때 일어난다. 내 코드와 겹치는 기능을
  제공하는 라이브러리를 쓰기 시작할 때도 일어난다** (7장 §"Substitute Algorithm",
  p.195).[^fowler2018]
- **전제 조건이 강하다** — **이 걸음을 밟아야 할 때 나는 메서드를 할 수 있는 만큼 분해했음을
  확신해야 한다. 크고 복잡한 알고리즘을 교체하는 것은 매우 어렵다. 단순하게 만들어야만 교체를
  다룰 만하게 만들 수 있다** (7장 §"Substitute Algorithm", p.196).[^fowler2018]
- 수순의 핵심이 비교 실행이다 — 교체할 코드가 완전한 함수 하나를 채우게 정리하고, **그 함수만
  쓰는 테스트를 준비해 행동을 붙잡고**, 대안 알고리즘을 준비한 뒤 **옛 알고리즘과 새 알고리즘의
  출력을 비교하는 테스트를 돌린다. 같으면 끝이고, 아니면 테스트와 디버깅에서 옛 알고리즘을
  비교용으로 쓴다** (7장 §"Substitute Algorithm", p.196).[^fowler2018]

## 이어지는 페이지

- [기본 리팩터링](basic-refactorings.md) — 앞 장(6장). 여기서 쓰는 *Encapsulate Variable*·
  *Combine Functions into Class*의 정본
- [기능 이동 리팩터링](moving-features.md) — 다음 장(8장). *Move Function*·*Move Field*의 정본
- [데이터 조직화 리팩터링](organizing-data.md) — *Change Reference to Value*와 그 역이 사는 장
- [정보 은닉과 정보 누출](information-hiding-and-leakage.md) — 이 장이 인용한 파나스의 기준을
  잣대로 세운 소스
- [결합 끊기](decoupling.md) — 위임 숨기기와 중개자 제거가 재는 것
- [코드의 나쁜 냄새](code-smells.md) — 이 장의 항목들이 처방으로 지목되는 냄새들
- [일관성](consistency-in-code.md) — 컬렉션 접근 기제를 하나로 통일하라는 판정의 원리 쪽
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 7장 "Encapsulation"(pp.161–196). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 22).
    직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준 규약이며 근거는
    `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example 절과 스케치 도판은
    옮기지 않았다. §"Encapsulate Record"의 Motivation 첫 문장이 "This is why…"로 시작해 앞
    문단을 받는 것처럼 보이는데, 인쇄판 p.162를 시각 판독해 확인한 결과 **원문이 그렇게 조판돼
    있다**(누락이 아니다).

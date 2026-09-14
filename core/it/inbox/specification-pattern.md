---
type: concept
title: 명세 패턴
description: 업무 규칙이 어느 도메인 객체의 책임에도 맞지 않을 때 쓰는 패턴의 원전 — 규칙 평가 코드가 청구서의 의미를 삼킨다는 진단과 규칙을 애플리케이션 층으로 옮기면 더 나빠진다는 판정, 논리 프로그래밍의 술어를 빌리되 다 옮기지는 않는다는 절충, 술어 같은 값 객체를 만들라는 처방, 검증과 선택과 주문 생산 셋이 개념적으로 하나라는 규정, 리포지터리와 맞물릴 때 SQL을 어디에 둘지를 놓고 저자가 보인 세 판과 각 판의 대가, 생성기 인터페이스를 명세로 정의할 때 얻는 것 넷, 화학 물질 창고 사례, 그리고 같은 책 10장이 얹는 선언적 확장 셋인 논리 연산자 결합과 구현 선택지와 포섭
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 명세 패턴

- [규칙이 갈 곳이 없을 때](#규칙이-갈-곳이-없을-때)
- [논리 프로그래밍의 술어를 빌리되 다 옮기지는 않는다](#논리-프로그래밍의-술어를-빌리되-다-옮기지는-않는다)
- [조항](#조항)
- [명세는 값 객체다](#명세는-값-객체다)
- [세 가지 쓰임이 개념적으로 하나다](#세-가지-쓰임이-개념적으로-하나다)
- [검증](#검증)
- [선택 곧 질의](#선택-곧-질의)
- [리포지터리와 맞물리는 자리](#리포지터리와-맞물리는-자리)
- [주문 생산](#주문-생산)
- [화학 물질 창고 사례](#화학-물질-창고-사례)
- [선언적 스타일로 확장하기](#선언적-스타일로-확장하기)
- [논리 연산자로 결합하기](#논리-연산자로-결합하기)
- [구현은 하나가 아니다](#구현은-하나가-아니다)
- [포섭 — 두 명세를 직접 비교하기](#포섭--두-명세를-직접-비교하기)
- [패턴은 요리책이 아니다](#패턴은-요리책이-아니다)
- [명세가 서비스에 인자로 넘어가는 자리](#명세가-서비스에-인자로-넘어가는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어느 도메인 객체의 책임에도 맞지 않는 업무 규칙을 어디에 두는가.**

## 규칙이 갈 곳이 없을 때

- 출발점은 흔한 불리언 검사 메서드다 — **온갖 종류의 애플리케이션에서, 실은 작은 규칙의
  일부인 불리언 검사 메서드가 나타난다. 그것이 단순한 동안 우리는 `anIterator.hasNext()`나
  `anInvoice.isOverdue()` 같은 검사 메서드로 처리한다** (9장, p.224).[^evans2003]
  `isOverdue()`의 구현은 현재 날짜가 만기일 뒤인지 보는 두 줄이다 (9장, p.224).[^evans2003]
- 그런데 같은 `Invoice` 클래스의 `isDelinquent()`로 넘어가면 달라진다. 연체 판정은 만기 초과
  검사에서 시작하지만 거기가 시작일 뿐이고, 유예 기간 정책이 고객 계정 상태에 달리며, 어떤
  연체 청구서는 2차 통지 대상이고 어떤 것은 추심 기관에 넘어간다 (9장, p.224).[^evans2003]
  저자의 판정 — **지불 요청으로서의 `Invoice`가 갖는 명료함은 곧 규칙 평가 코드의 순전한
  양 속에 사라질 것이다** (9장, p.224).[^evans2003]
- 덧붙는 대가가 둘이다 (9장, p.224):[^evans2003]
  - **`Invoice`는 또한 그 기본 의미를 지지하지 않는 온갖 도메인 클래스와 서브시스템에 대한
    의존을 키울 것이다.**
  - **평가 메서드가 조건 코드로 부풀어 규칙을 읽기 어렵게 만든다.**
- 흔한 대응이 있고, 그 대응이 더 나쁘다 — 규칙 평가 코드를 애플리케이션 층으로 리팩터링하면
  **이제 규칙은 도메인 층에서 완전히 분리되어, 업무 모델에 내재한 규칙을 표현하지 못하는 죽은
  데이터 객체를 뒤에 남긴다** (9장, p.224).[^evans2003] 그 층 배분의 조항은
  [계층 아키텍처](../concepts/layered-architecture.md)에 있다.
- 문제 설정이 한 문단으로 정리된다 (9장, p.225):[^evans2003]

> Business rules often do not fit the responsibility of any of the obvious ENTITIES or VALUE
> OBJECTS, and their variety and combinations can overwhelm the basic meaning of the domain
> object. But moving the rules out of the domain layer is even worse, since the domain code no
> longer expresses the model.

## 논리 프로그래밍의 술어를 빌리되 다 옮기지는 않는다

- 다른 패러다임에는 이미 답이 있다 — 논리 프로그래밍(logic programming) 쪽 개발자라면 이런
  규칙을 술어(predicate)로 표현한다. **술어는 "참" 또는 "거짓"으로 평가되는 함수이며 "AND"나
  "OR" 같은 연산자로 결합해 더 복잡한 규칙을 표현할 수 있다** (9장, p.225).[^evans2003]
- 그것을 객체로 통째로 옮기려던 시도의 전적이 적힌다 — 어떤 것은 매우 정교했고 어떤 것은
  순진했으며, **몇몇 시도는 프로젝트를 탈선시키도록 방치되었다** (9장, p.225).[^evans2003]
  결론 — **발상이 아무리 매력적이어도, 객체로 논리를 온전히 구현하는 것은 거대한 사업이다**
  (9장, p.225).[^evans2003]
- 그래서 저자는 빌리되 다 옮기지 않는다 (9장, p.225):[^evans2003]

> Logic programming provides the concept of separate, combinable, rule objects called
> "predicates," but full implementation of this concept with objects is cumbersome. It is also
> so general that it doesn't communicate intent as much as more specialized designs.

  - **너무 일반적이면 의도를 전달하지 못한다**는 것이 여기서 일반성을 깎는 근거다. 같은
    저울을 다른 축에서 다루는 자리가 [범용 모듈이 더 깊다](../concepts/general-purpose-modules.md)이고,
    거기서는 저울이 반대쪽으로 기운다.
- 절충의 근거는 분포다 — **다행히 우리는 큰 이득을 얻기 위해 논리 프로그래밍을 온전히 구현할
  필요가 실은 없다. 우리 규칙 대부분은 몇 가지 특수한 경우에 속한다** (9장,
  p.225).[^evans2003]

## 조항

- 명세(SPECIFICATION)의 규정 — **명세는 다른 객체의 상태에 대한 제약을 진술하며, 그 객체는
  있을 수도 있고 없을 수도 있다** (9장, p.225).[^evans2003] 뒤쪽 단서가 이 패턴의 쓰임 세
  가지를 미리 가른다. 아직 없는 객체에도 걸린다는 뜻이다.
- 처방 문단이 그 정의다 (9장, p.226):[^evans2003]

> Create explicit predicate-like VALUE OBJECTS for specialized purposes. A SPECIFICATION is a
> predicate that determines if an object does or does not satisfy some criteria.

- 복잡한 규칙을 위해 명세를 결합하는 확장이 예고되지만, **근본 패턴은 그대로이며 더 단순한
  모델에서 더 복잡한 모델로 가는 길을 제공한다** (9장, p.226).[^evans2003]

## 명세는 값 객체다

- 새 객체의 지위가 값 객체(VALUE OBJECT)로 못 박힌다 — **그것들은 별도의 값 객체로 분리해 낼
  수 있는 작은 진리 검사다. 이 새 객체는 다른 객체를 평가해 그 객체에 대해 술어가 참인지 볼
  수 있다** (9장, p.225).[^evans2003] 값 객체의 원 정의는
  [값 객체와 엔티티](../concepts/value-objects-and-entities.md)에 있다.
- 이 분리가 회수하는 것 — **명세는 규칙을 도메인 층에 유지한다. 규칙이 완전한 자격을 갖춘
  객체이므로 설계가 모델을 더 명시적으로 반영할 수 있다** (9장, p.226).[^evans2003]
- 그리고 규칙에 필요한 재료를 어떻게 대는지가 규정된다 — **팩토리(FACTORY)가 고객의 계정이나
  회사 정책 데이터베이스 같은 다른 출처의 정보를 써서 명세를 구성할 수 있다. `Invoice`에서
  이 출처들로 직접 접근하게 하면 지불 요청이라는 `Invoice`의 기본 책임과 무관한 방식으로
  객체들을 결합시킬 것이다** (9장, p.226).[^evans2003]
- 연체 명세 예에서는 한 번 쓰고 버릴 것이라 평가 날짜를 객체 안에 박아 넣었고, 저자는 그것을
  **훌륭한 단순화**(a nice simplification)라 부른다 — **명세에는 그것이 일할 때 필요한 정보를
  단순하고 직설적인 방식으로 줄 수 있다** (9장, p.226).[^evans2003]

## 세 가지 쓰임이 개념적으로 하나다

- 이 패턴의 값 대부분이 여기 있다 — **명세의 값 대부분은 그것이 꽤 달라 보이는 애플리케이션
  기능을 통합한다는 데 있다** (9장, p.228).[^evans2003] 목적 셋이 열거된다 (9장,
  p.228):[^evans2003]

> 1. To validate an object to see if it fulfills some need or is ready for some purpose
> 2. To select an object from a collection (as in the case of querying for overdue invoices)
> 3. To specify the creation of a new object to fit some need

- 판정 — **이 세 쓰임, 곧 검증(validation)과 선택(selection)과 주문 생산(building to order)은
  개념적 수준에서 같다** (9장, p.228).[^evans2003]
- 패턴을 쓰지 않을 때 잃는 것 — **명세 같은 패턴이 없으면 같은 규칙이 서로 다른 모습으로,
  어쩌면 서로 모순되는 형태로 나타날 수 있다. 개념적 통일이 사라질 수 있다** (9장,
  p.228).[^evans2003]
- 그리고 이 패턴이 허용하는 것 — **명세 패턴을 적용하면 구현이 갈라져야 할 때조차 일관된
  모델을 쓸 수 있다** (9장, p.228).[^evans2003] 아래 선택 절의 세 판이 그 갈라짐의 실물이다.

## 검증

- 가장 단순한 쓰임이고 개념을 가장 직설적으로 보인다 (9장, p.228).[^evans2003] 연체 판정
  규칙 하나가 클래스 하나가 되며, `isSatisfiedBy(Invoice)`가 그 인터페이스다 (9장,
  p.228):[^evans2003]

  ```java
  class DelinquentInvoiceSpecification extends InvoiceSpecification {
      private Date currentDate;
      // An instance is used and discarded on a single date

      public DelinquentInvoiceSpecification(Date currentDate) {
          this.currentDate = currentDate;
      }

      public boolean isSatisfiedBy(Invoice candidate) {
          int gracePeriod = candidate.customer().getPaymentGracePeriod();
          Date firmDeadline =
              DateUtility.addDaysToDate(candidate.dueDate(), gracePeriod);
          return currentDate.after(firmDeadline);
      }
  }
  ```

- 클라이언트 쪽은 그 명세를 하나 만들어 고객의 청구서를 돌며 물어보는 것이 전부다. 영업
  담당자가 연체 고객을 불러올 때 빨간 깃발을 띄우는 기능이 그렇게 구현된다 (9장,
  pp.228–229).[^evans2003]

## 선택 곧 질의

- 물음이 바뀐다 — **검증은 개별 객체가 어떤 기준을 충족하는지 시험한다. … 또 하나의 흔한
  필요는 어떤 기준에 따라 객체 컬렉션의 부분집합을 고르는 것이다. 같은 명세 개념을 여기에
  적용할 수 있으나 구현 문제는 다르다** (9장, p.229).[^evans2003]
- 객체가 메모리에 있다면 검증판 구현이 그대로 쓰인다. 리포지터리에 명세를 받는 일반화된 선택
  메서드 `selectSatisfying(InvoiceSpecification spec)`를 두면 클라이언트는 한 줄로 연체
  청구서 전부를 얻는다 (9장, p.229).[^evans2003]
- 현실은 그렇지 않다 — 청구서는 수천 건이고 관계형 데이터베이스에 있다. 저자는 여기가 모델의
  초점이 흐려지는 지점이라고 앞 장들의 진단을 되부른다 (9장, p.230).[^evans2003] 그러나
  구현의 자유가 함께 규정된다 (9장, p.230):[^evans2003]

> MODEL-DRIVEN DESIGN demands that the model stay in lockstep with the implementation, but it
> allows freedom to choose any implementation that faithfully captures the meaning of the model.

## 리포지터리와 맞물리는 자리

저자는 SQL을 어디에 둘지를 놓고 세 판을 차례로 보이고, 각 판의 대가를 명시한다. 어느 판을
고르든 모델은 같다는 것이 이 절의 결론이다.

- **첫째 판 — 명세가 SQL을 낸다.** 명세에 `asSQL()`을 더해 질의를 검증 규칙과 같은 클래스에
  캡슐화한다. 저자의 평 — **SQL은 명세를 쓰기에 아주 자연스러운 방법이다** (9장,
  p.230).[^evans2003] 그리고 명세는 리포지터리와 매끄럽게 맞물린다 — **명세는 리포지터리와
  매끄럽게 맞물리는데, 리포지터리는 도메인 객체에 대한 질의 접근을 제공하고 데이터베이스로의
  인터페이스를 캡슐화하는 구성 요소 기제이기 때문이다** (9장, p.231).[^evans2003]
  - 그런데 대가가 곧바로 적힌다 — **가장 중요하게는, 테이블 구조의 세부가 도메인 층으로
    새어 나왔다; 그것은 도메인 객체를 관계형 테이블에 연결하는 매핑 층에 격리되어야 한다**
    (9장, p.231).[^evans2003] 그 정보를 여기서 암묵적으로 중복하면 매핑이 바뀔 때마다 두
    군데를 추적해야 한다 (9장, p.231).[^evans2003]
  - 인프라가 대신해 줄 수 있다면 그것이 답이다 — 모델 객체와 속성으로 질의를 표현하고 실제
    SQL은 인프라스트럭처 층에서 생성하는 객체 관계 매핑 프레임워크가 있다면 **양쪽을 다
    가질 수 있을 것이다** (9장, p.231).[^evans2003]
- **둘째 판 — 리포지터리가 SQL을 들고 명세가 무엇을 부를지 정한다.** 리포지터리에
  `selectWhereGracePeriodPast(Date)`라는 특화 질의를 두고, 명세의 `asSQL()`을
  `satisfyingElementsFrom(InvoiceRepository)`로 바꾸어 이중 디스패치(double dispatch)로
  잇는다 (9장, pp.231–232).[^evans2003] 판정 — **이것은 SQL을 리포지터리에 두면서 명세가
  어떤 질의를 써야 할지를 통제하게 한다. 규칙이 명세에 그리 깔끔하게 모이지는 않지만, 무엇이
  연체를 이루는가에 대한 본질적 선언은 거기에 있다** (9장, p.232).[^evans2003]
  - 이때 리포지터리는 이 경우에만 쓰일 아주 특화된 질의를 갖게 되고, 저자는 그것을
    **받아들일 만하다**(acceptable)고 본다 (9장, p.232).[^evans2003]
- **셋째 판 — 리포지터리를 일반적으로 두고 명세가 메모리에서 거른다.** 리포지터리에는
  `selectWhereDueDateIsBefore(Date)`만 두고, 명세가 그 결과를 받아 `isSatisfiedBy`로 걸러
  낸다 (9장, pp.232–233).[^evans2003] 대가가 성능으로 명시된다 — **이 코드로는 성능 손해를
  본다. 더 많은 청구서를 꺼내 와 메모리에서 골라야 하기 때문이다. 이것이 책임의 더 나은
  배분을 위해 받아들일 만한 비용인지는 전적으로 상황에 달렸다** (9장, p.233).[^evans2003]
- 보안이나 성능 때문에 질의가 서버의 저장 프로시저로 구현될 때는 **명세가 그 저장 프로시저가
  허용하는 매개변수만 나를 수 있다** (9장, p.233).[^evans2003]
- 세 판을 묶는 판정 (9장, pp.233–234):[^evans2003]

> For all that, there is no difference in the model between these various implementations. The
> choice of implementation is free except where specifically constrained by the model. The price
> comes in a more cumbersome way of writing and maintaining queries.

  - 이 KB에서 리포지터리를 다루는 자리는
    [리포지터리 패턴](repository-pattern.md)이고, 그쪽 원 정의의 "어떤 기준으로
    객체를 선택하는 메서드"가 여기서 명세를 받는 메서드로 구체화된다.
- **같은 원전 6장이 이 맞물림을 리포지터리 쪽에서 한 번 더 규정한다.** 질의 인터페이스를
  일반화하는 방법으로 명세가 지목된다 — **프레임워크를 통해 리포지터리를 일반화하는 데 특히
  적절한 한 접근은 명세 기반 질의를 쓰는 것이다. 명세는 클라이언트가 어떻게 얻을지에 대한 걱정
  없이 자기가 원하는 것을 서술(즉 명세)하게 해 준다** (6장, p.153).[^evans2003]
  - 평가에 양면이 붙는다 — **명세 기반 질의는 우아하고 유연하다. 가용한 기반 구조에 따라 그것은
    적당한 프레임워크일 수도 있고 엄두를 못 낼 만큼 어려울 수도 있다** (6장,
    p.153).[^evans2003]
  - 그리고 단서 하나가 위 둘째 판을 정당화한다 — **유연한 질의를 갖춘 리포지터리 설계라도
    특화된 하드코딩 질의를 더할 수 있게 해야 한다** (6장, pp.153–154).[^evans2003] 그렇지 않은
    프레임워크는 **도메인 설계를 일그러뜨리거나 개발자들에게 우회당하는 경향이 있다** (6장,
    p.154).[^evans2003] 전문은
    [리포지터리의 질의와 구현](repository-querying-and-implementation.md)에 있다.
- 저자 자신이 범위를 제한한다 — **이 논의는 명세와 데이터베이스를 결합하는 문제의 표면을
  겨우 긁을 뿐이고, 나는 생길 수 있는 모든 고려 사항을 다루려 시도하지 않겠다** (9장,
  p.234).[^evans2003] 그러면서 더 읽을 곳으로 Fowler 2003을 댄다.

## 주문 생산

- 비유가 이 쓰임을 규정한다. 국방부가 새 전투기를 원할 때 명세를 쓰는데, 마하 2와 항속 1800
  마일과 5천만 달러 이하 같은 항목이 아무리 상세해도 **그 명세는 비행기의 설계가 아니고, 더욱이
  비행기도 아니다** (9장, p.234).[^evans2003] 경쟁하는 여러 회사가 같은 명세에서 서로 다른
  설계를 낼 수 있다.
- 무엇이 달라지는가 — **우리는 아직 존재하지 않는 객체에 대한 기준을 명시하고 있다** (9장,
  p.234).[^evans2003] 그래서 구현이 앞의 둘과 전혀 다르다. **이 명세는 질의에서처럼 이미
  있는 객체를 거르는 필터가 아니다. 검증에서처럼 있는 객체에 대한 시험도 아니다. 이번에는
  명세를 만족시키기 위해 완전히 새로운 객체나 객체 집합이 만들어지거나 재구성될 것이다**
  (9장, p.234).[^evans2003]
- 명세 없이도 생성기(generator)는 쓸 수 있다. 다만 그 코드가 **생성기의 행동을 암묵적으로
  정의한다** (9장, p.234).[^evans2003] 서술적 명세로 인터페이스를 정의하면 이득 넷이 따른다
  (9장, p.235):[^evans2003]

> - The generator's implementation is decoupled from its interface. The SPECIFICATION declares
>   the requirements for the output but does not define how that result is reached.
> - The interface communicates its rules explicitly, so developers can know what to expect from
>   the generator without understanding all details of its operation. The only way to predict the
>   behavior of a procedurally defined generator is to run cases or to understand every line of code.
> - The interface is more flexible, or can be enhanced with more flexibility, because the
>   statement of the request is in the hands of the client, while the generator is only obligated
>   to fulfill the letter of the SPECIFICATION.
> - Last, but not least, this kind of interface is easier to test, because the model contains an
>   explicit way to define input into the generator *that is also a validation of the output*.

  - **넷째가 이 패턴의 세 쓰임이 하나라는 주장의 값을 회수하는 자리다.** 위 인용은 넷째 항목의
    첫 문장까지이고, 이어지는 두 문장이 그 뜻을 푼다 — 생성기 인터페이스에 넘겨 생성을 제약한
    바로 그 명세를 검증 역할로 다시 써서 만들어진 객체가 맞는지 확인할 수 있다는 것이며,
    저자는 그것을 10장 단언(ASSERTION)의 사례로 지목한다 (9장, p.235).[^evans2003]
- 주문 생산의 범위 — **주문 생산은 객체를 맨바닥에서 만드는 것일 수도 있지만, 이미 있는
  객체를 명세에 맞게 구성하는 것일 수도 있다** (9장, p.235).[^evans2003]

## 화학 물질 창고 사례

- 문제 설정 — 창고에 화학 물질이 대형 용기에 쌓여 있다. 어떤 것은 불활성이라 아무 데나 두어도
  되고, 어떤 것은 휘발성이라 특별히 환기되는 용기에, 어떤 것은 폭발성이라 특별히 장갑된 용기에
  두어야 한다. 한 용기에 허용되는 조합 규칙도 있다. **목표는 화학 물질을 용기에 넣는 효율적이고
  안전한 방법을 찾는 소프트웨어를 쓰는 것이다** (9장, p.235).[^evans2003]
- 시작하는 자리를 저자가 뒤집는다 (9장, p.236):[^evans2003]

> We could start by writing a procedure to take a chemical and place it in a container, but
> instead, let's start with the validation problem. This will force us to make the rules
> explicit, and it will give us a way to test the final implementation.

  - **규칙을 명시하게 강제하는 것과 최종 구현을 시험할 방법을 얻는 것, 둘이 같은 동작에서
    나온다.** 앞 절 생성기 이득 넷 중 넷째가 여기서 실물이 된다.
- 화학 물질마다 용기 명세가 붙는다. TNT는 장갑 용기, 암모니아는 환기 용기, 생물 시료는 폭발물과
  같은 용기를 쓰지 않을 것 같은 식이다 (9장, p.236).[^evans2003] `ContainerSpecification`은
  필요한 `ContainerFeature`를 용기가 갖고 있는지 보는 `isSatisfiedBy(Container)` 하나로
  구현되고, 폭발성 화학 물질에는 `new ContainerSpecification(ARMORED)`가 붙는다 (9장,
  p.237).[^evans2003]
- 용기 쪽에는 `isSafelyPacked()`가 생긴다. 담긴 드럼을 돌며 각 드럼의 용기 명세가 자기를
  만족하는지 묻는 것이 전부다 (9장, p.237).[^evans2003] 이 시점에 이미 재고 데이터베이스를
  훑어 안전하지 않은 상황을 보고하는 감시 애플리케이션을 쓸 수 있다 — 저자의 논평은 **이것은
  우리가 쓰라고 요청받은 소프트웨어가 아니다. 업무 담당자에게 이 기회를 알려 주는 것은 좋겠지만,
  우리는 적재기를 설계하라는 임무를 받았다. 우리가 가진 것은 적재기를 위한 시험이다** (9장,
  p.237).[^evans2003]
- 그 이해가 서비스 인터페이스를 낳는다. 드럼 컬렉션과 용기 컬렉션을 받아 규칙에 맞게 적재하는
  `WarehousePacker`이고, 그 인터페이스에 단언이 주석으로 붙어 있다 (9장, p.238).[^evans2003]
  이 인터페이스의 전문은
  [도메인 객체가 된 프로세스](processes-as-domain-objects.md)에 있다.
- 얻은 것 — **이제 적재기 서비스의 책임을 수행할 최적화된 제약 해결기를 설계하는 과제가
  애플리케이션의 나머지에서 결합 해제되었고, 그 기제들은 모델을 표현하는 설계 부분을 어지럽히지
  않을 것이다. 그러면서도 적재를 지배하는 규칙은 도메인 객체에서 빠져나가지 않았다** (9장,
  p.238).[^evans2003]
- 그리고 이 인터페이스 덕에 스무 줄 남짓의 `PrototypePacker`가 가능해진다 (9장,
  pp.239–241).[^evans2003] 그 프로토타입의 지위를 다루는 자리는
  [트레이서 탄환과 프로토타입](../concepts/tracer-bullets-and-prototypes.md)이다. 사례가 닫히는
  문장 (9장, p.241):[^evans2003]

> Here we have an example of a "simplest thing that could possibly work" that actually becomes
> possible because of a more sophisticated model.

## 선언적 스타일로 확장하기

이 패턴의 확장은 같은 책 10장 "Supple Design"에 있다. 9장이 패턴의 기본 개념과 세 쓰임을
세웠다면, 10장은 복잡한 규칙을 다루는 상황에서 쓸모 있는 장치들을 거기에 얹는다 (10장,
p.273).[^evans2003]

- 이 패턴의 계보가 여기서 밝혀진다 — **명세는 확립된 형식 체계인 술어를 각색한 것이다. 술어는
  우리가 선별적으로 끌어 쓸 수 있는 다른 쓸모 있는 성질들을 가지고 있다** (10장,
  p.274).[^evans2003] 확립된 형식 체계를 빌린다는 이 접근 자체는
  [확립된 형식 체계](established-formalisms.md)가 다룬다.
- **선별적으로**라는 낱말이 9장의 절충을 이어받는다. 술어 논리 전체를 객체로 옮기지 않겠다는
  앞의 판정이 여기서도 유효하고, 아래 세 장치는 각각 따로 채택하거나 버릴 수 있는 것으로
  제시된다.

## 논리 연산자로 결합하기

- 필요가 먼저 온다 — **명세를 쓰다 보면 그것들을 결합하고 싶은 상황을 금세 만난다. 명세는
  술어의 한 예이고, 술어는 "AND"와 "OR"와 "NOT" 연산으로 결합하고 변형할 수 있다** (10장,
  p.274).[^evans2003]
- 그리고 그 연산의 성질이 지목된다 — **이 논리 연산들은 술어 아래서 닫혀 있으므로, 명세의
  결합은 연산의 닫힘(CLOSURE OF OPERATIONS)을 보일 것이다** (10장, p.274).[^evans2003]
  그 패턴은 [연산의 닫힘](closure-of-operations.md)에 있다.
- 결합하려면 타입이 올라가야 한다 — 일반화된 능력을 명세에 넣을수록 **온갖 종류의 명세에 쓸 수
  있는 추상 클래스나 인터페이스를 만드는 것이 매우 쓸모 있어진다. 이것은 인자를 어떤 상위 수준
  추상 클래스로 타이핑한다는 뜻이다** (10장, p.274).[^evans2003] 그래서 인터페이스가
  `boolean isSatisfiedBy(Object candidate)` 하나로 좁혀진다.
- 대가가 명시된다 — **이 추상화는 메서드 첫머리에 보호 절(guard clause)을 요구하지만, 그 밖에는
  기능에 영향을 주지 않는다** (10장, p.274).[^evans2003] 위 검증판 예제의
  `ContainerSpecification`은 후보가 `Container`가 아니면 곧바로 거짓을 돌려주는 줄 하나를
  얻고 형 변환이 붙는 것으로 그 인터페이스를 구현한다 (10장, p.274).[^evans2003]
- 그다음 인터페이스에 세 연산이 더해진다 — `Specification and(Specification other)`,
  `Specification or(Specification other)`, `Specification not()` (10장, p.275).[^evans2003]
- 위 화학 물질 창고 사례가 그대로 되불려 실물이 된다 (10장, p.275):[^evans2003]
  - 휘발성이면서 폭발성인 화학 물질은 환기 용기와 장갑 용기 두 명세를 다 필요로 하므로
    `ventilated.and(armored)`가 된다. **이 선언이 기대하는 성질을 가진 새 명세 객체를 정의한다.
    이 조합은 더 복잡한 용기 명세를 요구했을 것이고 그러고도 여전히 특수 목적이었을 것이다.**
  - 환기 용기가 두 종류이고 어떤 품목에는 어느 쪽이든 상관없다면
    `ventilatedType1.or(ventilatedType2)`다.
  - 모래를 특수 용기에 보관하는 것이 낭비라고 여겨지면 아무 특수 기능도 없는 "싼" 용기를
    명세해 막을 수 있다 — `(ventilated.not()).and(armored.not())`. **이 제약은 9장에서 논의한
    프로토타입 창고 적재기의 차선 행동 일부를 막았을 것이다.**
- 이 확장이 사 오는 것 (10장, p.275):[^evans2003]

> The ability to build complex specifications out of simple elements increases the
> expressiveness of the code. The combinations are written in a declarative style.

  - **선언적 스타일이 이 확장의 목표다.** 그 스타일의 규정은
    [선언적 설계](declarative-design.md)에 있다.

## 구현은 하나가 아니다

- 저자가 보이는 구현은 컴포지트(COMPOSITE)와 데코레이터(DECORATOR)를 쓴다. 추상 클래스
  `AbstractSpecification`이 `and`·`or`·`not`을 각각 `AndSpecification`·`OrSpecification`·
  `NotSpecification`을 새로 만들어 돌려주는 것으로 구현하고, 각 조합 클래스는 감싼 명세들에게
  `isSatisfiedBy`를 물어 논리 연산을 적용한다 (10장, pp.276–277).[^evans2003]
- **그런데 저자가 그 코드의 지위를 스스로 낮춘다** — 이 구현은 **아주 단순한 구현이며 어떤
  상황에서는 비효율적이고 어떤 상황에서는 꽤 실용적일 것이다. 그것은 설명을 위한 예제로
  의도되었다. 어떤 패턴이든 그렇듯 그것을 구현하는 방법은 많다** (10장, p.276).[^evans2003]
  그리고 다시 한번 — **이 코드는 책에서 읽기 가능한 한 쉽도록 쓰였다** (10장,
  p.277).[^evans2003]
- 무엇이 지켜져야 하는지가 남는다 (10장, p.277):[^evans2003]

> The important thing is a model that captures the key concepts of the domain, along with an
> implementation that is faithful to that model. That leaves a lot of room to solve performance
> problems.

- 필요 없는 것을 짓지 말라는 단서가 따로 붙는다 — 완전한 일반성이 많은 경우 필요하지 않고,
  **특히 AND가 나머지보다 훨씬 많이 쓰이며 구현 복잡성도 덜 만든다. 필요한 것이 그것뿐이라면
  AND만 구현하기를 두려워하지 마라** (10장, p.278).[^evans2003] 2장의 대화 예제에서 개발자들이
  명세의 "만족되는가" 행동을 구현하지 않았던 것이 그 실물로 지목된다. 그때까지 명세는 주문
  생산에만 쓰였고, **그럼에도 추상은 온전했으며 기능을 더하기는 비교적 쉬웠다** (10장,
  p.278).[^evans2003] 판정 — **패턴을 쓴다는 것이 필요 없는 기능을 짓는다는 뜻은 아니다.
  개념이 흐려지지만 않는다면 나중에 더할 수 있다** (10장, p.278).[^evans2003]
- 대안 구현의 실물이 저자의 실패담으로 온다. 모든 객체에 ID를 부여하고 추적하는 객체
  데이터베이스를 쓰던 프로젝트에서 객체마다 메모리와 성능 부담이 컸고 총 주소 공간이 제약이었다.
  명세를 도메인 설계의 중요한 지점들에 쓴 것은 좋은 결정이었다고 보지만, **이 장에 서술된
  구현보다 조금 더 공들인 판을 썼고 그것은 분명히 실수였다. 그 결과 시스템을 느려지게 하는 데
  기여한 아주 세밀한 객체 수백만 개가 생겼다** (10장, p.278).[^evans2003]
- 그 자리에 맞는 대안은 복합 명세를 논리식을 인코딩한 문자열이나 배열로 두고 **실행 시점에
  해석하는 것**이다. 스택에서 원소를 하나씩 꺼내 평가하거나 연산자가 요구하는 대로 다음 것을
  꺼내는 방식이고, 결과는 `and(not(armored), not(ventilated))`가 된다 (10장,
  p.279).[^evans2003] 장단점이 셋으로 적힌다 (10장, p.279):[^evans2003]
  - **낮은 객체 수**
  - **효율적인 메모리 사용**
  - **더 숙련된 개발자를 요구함**
- 결론 — **당신의 상황에 맞는 절충을 가진 구현을 찾아야 한다. 같은 패턴과 같은 모델이 매우
  다른 구현의 바탕이 될 수 있다** (10장, p.279).[^evans2003] 위 선택 절의 SQL 세 판과 같은
  형태의 판정이고, 같은 문장이 두 번 나오는 셈이다.

## 포섭 — 두 명세를 직접 비교하기

- 저자가 이 장치의 지위를 먼저 규정한다 — **이 마지막 기능은 대개 필요하지 않고 구현하기
  어려울 수 있지만, 이따금 정말 어려운 문제를 푼다. 그것은 또한 명세의 의미를 밝혀 준다**
  (10장, p.279).[^evans2003]
- 문제 설정은 화학 물질 창고다. 규정이 몇 달마다 새로 나오는데, 사용자는 **요구 조건이 더
  엄격해진 화학 물질 유형의 목록을 뽑고 싶어 한다** (10장, p.279).[^evans2003]
- 부분적인 답과 그 부족함이 갈린다. 새 명세로 재고의 각 드럼을 검증하면 옮겨야 할 드럼 목록을
  얻는다. **그러나 그들이 요청한 것은 취급이 더 엄격해진 화학 물질의 목록이었다.** 지금 창고에
  하나도 없거나 우연히 더 엄격한 용기에 담겨 있었다면 그 보고서에는 나오지 않는다 (10장,
  p.280).[^evans2003]
- 그래서 새 연산이 들어온다 — `boolean subsumes(Specification other)`. **더 엄격한 명세가 덜
  엄격한 것을 포섭한다. 그것은 이전의 어떤 요구도 방치하지 않으면서 그 자리를 대신할 수 있다**
  (10장, p.280).[^evans2003]
- 뜻이 논리로 환원된다 — **명세의 언어로 말하면, 새 명세를 만족시킬 후보라면 옛 명세도
  만족시킬 것이므로 새 명세가 옛 명세를 포섭한다고 말한다. 각 명세를 술어로 본다면 포섭은
  논리적 함의(logical implication)와 동등하다** (10장, p.280).[^evans2003] 명세를 바꿀 때
  묻는 것은 새 명세가 옛 명세의 모든 조건을 충족하는가, 곧 새 명세가 참이면 옛 명세도 참인가다
  (10장, pp.280–281).[^evans2003]
- **일반적 증명은 포기된다** — **논리적 함의를 일반적인 방식으로 증명하는 것은 매우 어렵지만
  특수한 경우는 쉬울 수 있다** (10장, p.281).[^evans2003] 두 가지 실용적 특수 경우가 제시된다
  (10장, p.281):[^evans2003]
  - **매개변수를 가진 명세는 자기 자신의 포섭 규칙을 정의할 수 있다.** 최소 연령 명세는
    자기 기준값이 상대의 기준값보다 크거나 같은지만 보면 된다. 운전 가능 연령 16과 투표 가능
    연령 18을 놓고 투표 연령이 운전 연령을 포섭한다고 단언하는 JUnit 테스트가 그 확인이다.
  - **AND 하나만 있는 경우.** `A AND B`는 `A`를 함의하고 `A AND B AND C`는 `A AND B`를
    함의하므로, 복합 명세가 AND로 묶인 잎 명세를 전부 모을 수 있다면 **포섭하는 쪽의 잎 집합이
    포섭되는 쪽의 잎 집합을 포함하는지, 곧 상위 집합인지만 확인하면 된다.**
- 그리고 경계가 그어진다 — **불행히도 OR와 NOT이 포함되면 이 증명은 훨씬 복잡해진다. 대부분의
  상황에서는 연산자 일부를 포기하거나 포섭을 포기해서 그런 복잡성을 피하는 것이 최선이다. 둘 다
  필요하다면 그 이득이 어려움을 정당화할 만큼 큰지 조심스럽게 고려하라** (10장,
  p.282).[^evans2003]
  - **세 장치가 서로 값을 치른다는 것이 이 절의 결론이다.** 논리 연산자 셋을 다 구현하는 것과
    포섭을 구현하는 것이 함께 가지 않는다.
- 곁글 "Aristotle on SPECIFICATIONS"가 포섭의 뜻을 삼단 논법으로 보인다. 모든 사람은 죽는다는
  것이 사람 명세가 죽는 것 명세를 포섭한다는 단언이고, 아리스토텔레스가 사람이라는 것이 사람
  명세가 그를 만족시킨다는 단언이며, 그러므로 죽는 것 명세도 그를 만족시킨다 (10장, p.282,
  곁글).[^evans2003]

## 패턴은 요리책이 아니다

- 저자가 이 절을 읽는 법을 지정한다 — 기본 개념은 매우 단순하지만 **모델 주도 설계는 그 개념을
  표현하기도 하는 효과적인 구현을 요구하고, 그것을 해내려면 패턴이 어떻게 적용될지를 조금 더
  깊이 파야 한다** (9장, p.227).[^evans2003]
- 도메인 패턴의 지위 (9장, p.227):[^evans2003]

> A domain pattern is not just a neat idea for a UML diagram; it is a solution to a programming
> problem that retains a MODEL-DRIVEN DESIGN.

- 그리고 한계 — **패턴은 요리책이 아니다. 그것은 당신이 경험의 바탕에서 출발해 당신의 해법을
  개발하게 해 주고, 당신이 하고 있는 일에 대해 이야기할 언어를 준다** (9장,
  p.227).[^evans2003] 그래서 읽는 순서까지 지정된다 — 처음에는 핵심 개념만 훑고, 실제로 그
  상황을 만났을 때 돌아와 상세한 논의에 담긴 경험을 끌어 쓰라는 것이다 (9장, pp.223·227).[^evans2003]
- 이 패턴의 출처 표기 — **나는 마틴 파울러와 협업해 명세를 개발했다** (9장,
  p.223).[^evans2003]

## 명세가 서비스에 인자로 넘어가는 자리

12장의 경로 탐색 사례가 이 패턴을 **서비스 인터페이스의 입력**으로 쓰는 실물이다.

- 설정 — 경로 명세(Route Specification)가 라우팅 서비스(Routing Service)에 넘어가고, 그
  서비스의 일은 **명세를 만족하는 상세 여정(Itinerary)을 구성하는 것**이다 (12장,
  p.312).[^evans2003]
- 위 [주문 생산](#주문-생산)이 말하는 쓰임이 여기서 서비스 경계에 걸린다. 생성기가 명세를
  받아 그것을 만족하는 산출물을 내놓는 구조이고, 그 산출물의 검증에도 같은 명세를 쓸 수 있다.
- **그런데 이 사례에서 명세와 함께 넘어가는 것이 하나 더 있다.** 서비스를 가장 빠른 경로와
  가장 싼 경로 사이에서 조율하던 조건문이 전략 객체로 떨어져 나가 인자가 된다. 연산이
  `find(Specification, LegMagnitudePolicy) : Itinerary` 하나가 되는 것이다 (12장,
  p.313).[^evans2003]
  - **두 인자의 역할이 다르다.** 명세는 **무엇을 만족해야 하는가**를 말하고, 정책은
    **여럿 중 무엇을 고르는가**를 말한다. 같은 값 객체 형태를 쓰되 답하는 물음이 갈린다.
    후자의 전문은 [설계 패턴을 도메인 패턴으로 읽기](design-patterns-as-domain-patterns.md)에
    있다.

## 이어지는 페이지

- [명시적 제약](explicit-constraints.md) — 같은 장에서 제약을 객체로 올리는 넓은 범주. 명세는
  그 범주의 좁고 흔한 한 경우다
- [설계 패턴을 도메인 패턴으로 읽기](design-patterns-as-domain-patterns.md) — 명세와 정책이
  같은 서비스 인터페이스에 나란히 넘어가는 자리
- [도메인 객체가 된 프로세스](processes-as-domain-objects.md) — 같은 장의 나머지 범주이고,
  창고 적재기 서비스 인터페이스가 사는 자리
- [암묵적 개념 파내기](digging-out-implicit-concepts.md) — 이 패턴이 명시하려는 개념을 찾아내는
  앞 단계
- [리포지터리 패턴](repository-pattern.md) — 선택 쓰임에서 이 패턴과 맞물리는 짝
- [리포지터리의 질의와 구현](repository-querying-and-implementation.md) — 명세가 질의 인터페이스를
  일반화하는 자리
- [값 객체와 엔티티](../concepts/value-objects-and-entities.md) — 명세가 어떤 종류의 객체인가
- [계층 아키텍처](../concepts/layered-architecture.md) — 규칙이 도메인 층을 떠나면 안 되는 이유
- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 생성기 인터페이스를
  명세로 정의한다는 처방이 기대는 조항
- [계약에 의한 설계](../concepts/design-by-contract.md) — 인터페이스에 걸린 단언을 다른 축에서
  다루는 자리
- [연산의 닫힘](closure-of-operations.md) — 명세의 논리 연산자 결합이 보이는 성질
- [선언적 설계](declarative-design.md) — 이 확장이 목표로 삼는 스타일
- [확립된 형식 체계](established-formalisms.md) — 술어를 각색한다는 이 패턴의 계보가 사는 자리
- [단언](assertions-pattern.md) — 생성기 인터페이스에 붙는 단언의 원전
- [트레이서 탄환과 프로토타입](../concepts/tracer-bullets-and-prototypes.md) — 창고 적재기
  프로토타입의 지위를 재는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 12장 "Relating Design Patterns to the Model" 예제
    "Route-Finding Policies"(pp.312–313) ·
    9장 "Making Implicit Concepts Explicit" §SPECIFICATION(pp.224–227)
    · §"Applying and Implementing SPECIFICATION"(pp.228–234) · §"Building to Order
    (Generating)"(pp.234–235) · 예제 "Chemical Warehouse Packer"(pp.235–238) · 예제
    "A Working Prototype of the Warehouse Packer"(pp.239–241). 선언적 확장은 10장
    "Supple Design" §"Extending SPECIFICATIONS in a Declarative Style"(pp.273–282)와
    곁글 "Aristotle on SPECIFICATIONS"(10장, p.282, 곁글)에서 왔다. 리포지터리 쪽에서 이 패턴을
    질의 일반화 수단으로 지목하는 자리는 6장 "The Life Cycle of a Domain Object"
    §"Querying a REPOSITORY"(pp.153–154)다. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 펜스의 Java 코드는 p.228 원문이며, 추출본에서 눌린 줄바꿈과 들여쓰기를
    표준 Java 조판으로 되돌린 것 말고 보탠 줄은 없다. 이 코드는 **2003년 Java의 관용**이라
    제네릭 없는 원시 타입을 쓴다. 같은 절의 나머지 코드(`isOverdue`, `selectSatisfying`,
    `asSQL`, 이중 디스패치 세 판, 창고 사례의 네 조각)는 같은 설계의 변형 연쇄이거나
    전후 대비 쌍이라 펜스로 옮기지 않고 산문으로 서술했다 — 이 페이지의 펜스 예산은 검증판이
    쓰고 있다. 10장 쪽 코드(`Specification` 인터페이스 두 판, 고친 `ContainerSpecification`,
    결합 예제 넷, `AbstractSpecification`과 세 조합 클래스, `MinimumAgeSpecification`,
    `subsumes` 구현)도 같은 이유로 산문과 인라인 코드로 옮겼다. 컴포지트 구조 그림
    (Figure 10.14)과 포섭 그림(Figure 10.15)과 스택 내용 표는 도판이라 판정 문장만 옮겼다. 클래스 다이어그램과 객체 다이어그램(Figure 9.12–9.16)은 도판이라 이름과
    판정 문장만 옮겼다. 저자가 대는 참고 문헌은 Evans and Fowler 1997(패턴의 공동 개발),
    Warmer and Kleppe 1999(제약의 준형식적 취급), Fowler 2003(리포지터리와 명세의 기술적
    쟁점)이다.

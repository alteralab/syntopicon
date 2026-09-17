---
type: concept
title: 도메인 서비스
status: draft
description: 사물이 아니라 활동인 도메인 개념을 모델에 두는 패턴의 원전 — 객체에 억지로 밀어 넣었을 때 잃는 것과 Manager로 끝나는 가짜 객체, 상태를 캡슐화하지 않고 홀로 서는 인터페이스라는 정의와 동사로 이름 짓는 관례, 좋은 서비스의 세 특징과 여기서 무상태가 뜻하는 것, 처방 문단, 서비스를 기반·애플리케이션·도메인 셋으로 가르는 기준과 계좌 이체 예제의 층별 분담, 굵기를 조절해 도메인 지식이 애플리케이션 층으로 새는 것을 막는다는 둘째 값, 접근 수단보다 책임을 떼어 내는 결정이 중요하다는 판정, 조립을 감출 자연스러운 거처가 없을 때 팩토리가 이 자리에 서는 경우, 그리고 2021년 실무서가 더하는 것 — 업무 로직을 담는 무상태 객체라는 규정과 여러 구성 요소의 호출을 조율해 계산이나 분석을 한다는 쓰임, 여러 애그리게이트에서 읽어야 하는 계산이 이 자리에 온다는 응답 기한 예제, 그리고 이 패턴이 한 트랜잭션에 애그리게이트 하나라는 제약의 빠져나갈 구멍이 아니라는 못박음과 마이크로서비스와 무관하다는 단서, 그리고 같은 이름을 배포 단위에 쓰는 소스와 층이 다르다는 정리
generated: { by: "claude-opus-5", at: "2026-09-14T23:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 도메인 서비스

- [사물이 아닌 것을 사물로 만들 때](#사물이-아닌-것을-사물로-만들-때)
- [무엇이 서비스인가](#무엇이-서비스인가)
- [좋은 서비스의 세 특징](#좋은-서비스의-세-특징)
- [조항](#조항)
- [세 층의 서비스를 가르는 기준](#세-층의-서비스를-가르는-기준)
- [계좌 이체 — 층별 분담의 실물](#계좌-이체--층별-분담의-실물)
- [굵기 — 지식이 새는 것을 막는 둘째 값](#굵기--지식이-새는-것을-막는-둘째-값)
- [접근 수단은 부차적이다](#접근-수단은-부차적이다)
- [팩토리가 서비스가 되는 자리](#팩토리가-서비스가-되는-자리)
- [무상태 객체라는 규정 — 2021년 판본](#무상태-객체라는-규정--2021년-판본)
- [응답 기한 계산 — 여러 애그리게이트에서 읽는다](#응답-기한-계산--여러-애그리게이트에서-읽는다)
- [빠져나갈 구멍이 아니다](#빠져나갈-구멍이-아니다)
- [이 낱말이 이 KB에서 갈리는 자리](#이-낱말이-이-kb에서-갈리는-자리)
- [번역 계층의 얼굴도 서비스다](#번역-계층의-얼굴도-서비스다)
- [외부 시스템의 인터페이스에 무슨 이름을 붙이는가](#외부-시스템의-인터페이스에-무슨-이름을-붙이는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **엔티티에도 값 객체에도 자연히 앉지 않는 도메인 연산을 어디에 두어야
모델이 그것을 잃지 않는가.**

## 사물이 아닌 것을 사물로 만들 때

- 문제 서술이 짧다 (5장 §SERVICES, p.105):[^evans2003]

> Some concepts from the domain aren't natural to model as objects. Forcing the required
> domain functionality to be the responsibility of an ENTITY or VALUE either distorts the
> definition of a model-based object or adds meaningless artificial objects.

- 그런데 저자가 먼저 반대 방향의 잘못을 경고한다 — **더 흔한 실수는 행동을 적절한 객체에
  맞추는 일을 너무 쉽게 포기하고 절차적 프로그래밍으로 서서히 미끄러지는 것이다**
  (5장, p.104).[^evans2003] 이 패턴은 그 미끄럼틀의 허가증이 아니다.
- 억지로 밀어 넣었을 때의 대가가 둘로 나온다 (5장, p.104):[^evans2003]
  - **그러나 객체의 정의에 맞지 않는 연산을 객체에 강제로 넣으면, 그 객체는 개념적 명료함을
    잃고 이해하거나 리팩터링하기 어려워진다. 복잡한 연산은 단순한 객체를 쉽게 압도해 그
    역할을 흐린다.**
  - **그리고 이런 연산은 많은 도메인 객체를 함께 끌어모아 조율하고 작동시키는 일이 잦으므로,
    더해진 책임이 그 모든 객체에 대한 의존을 만들어 독립적으로 이해될 수 있었을 개념들을
    엉키게 한다.**
- 세 번째 실패 양상이 이름으로 드러난다 — **때로 서비스가 모델 객체로 위장하기도 한다.
  어떤 연산을 하는 것 말고는 아무 의미가 없는 객체로 나타나는 것이다. 이런 "행위자"들은
  이름이 "Manager" 따위로 끝난다** (5장, pp.104–105).[^evans2003]
  - 그래도 그 해법이 최악은 아니라고 저자가 적는다 — **적어도 이 해법은 진짜 모델 객체를
    어지럽히지 않으면서 이 별개의 행동들에 거처를 준다** (5장, p.105).[^evans2003]
  - 이름 쪽 진단은 [이름 짓기](../concepts/naming-things.md)와 짝을 이룬다 — 이 소스는 나쁜
    이름을 읽기 불편함이 아니라 **모델에 개념이 빠져 있다는 증거**로 읽는다.

## 무엇이 서비스인가

- 정의다 (5장, p.105):[^evans2003]

> A SERVICE is an operation offered as an interface that stands alone in the model, without
> encapsulating state, as ENTITIES and VALUE OBJECTS do. SERVICES are a common pattern in
> technical frameworks, but they can also apply in the domain layer.

- 이름의 뜻이 관계를 가리킨다 — **service라는 이름은 다른 객체들과의 관계를 강조한다.
  엔티티나 값 객체와 달리 그것은 순전히 클라이언트를 위해 무엇을 할 수 있는가로 정의된다**
  (5장, p.105).[^evans2003]
- 그래서 이름 짓기 관례가 갈린다 — **서비스는 개체(entity)가 아니라 활동으로 이름 지어지는
  경향이 있다 — 명사가 아니라 동사로** (5장, p.105).[^evans2003]
- **그러나 모델 요소로서의 자격은 객체와 같다** (5장, p.105):[^evans2003]
  - **서비스도 여전히 추상적이고 의도적인 정의를 가질 수 있다. 그저 객체의 정의와는 다른
    풍미를 가질 뿐이다.**
  - **서비스는 여전히 정의된 책임을 가져야 하고, 그 책임과 그것을 수행하는 인터페이스는
    도메인 모델의 일부로 정의되어야 한다.**
  - **연산 이름은 유비쿼터스 언어에서 와야 하거나 그 언어에 도입되어야 한다. 매개변수와
    결과는 도메인 객체여야 한다.**
  - 마지막 줄이 [유비쿼터스 언어](ubiquitous-language.md)의 요구를 서비스에 그대로
    적용한다 — 서비스는 모델 바깥의 유틸리티가 아니라 **모델의 어휘 항목**이다.
- 남용을 막는 단서가 붙는다 — **서비스는 신중하게 써야 하며, 엔티티와 값 객체에서 모든 행동을
  벗겨 내도록 허용되어서는 안 된다. 그러나 어떤 연산이 실제로 중요한 도메인 개념일 때, 서비스는
  모델 주도 설계의 자연스러운 일부를 이룬다** (5장, p.105).[^evans2003]
- 그리고 명시가 갖는 효과가 적힌다 — **실제로 아무것도 표상하지 않는 가짜 객체가 아니라
  모델에서 서비스로 선언되면, 그 홀로 서는 연산은 누구도 오도하지 않는다**
  (5장, p.105).[^evans2003]

## 좋은 서비스의 세 특징

- **좋은 서비스는 세 특징을 갖는다** (5장, p.105):[^evans2003]
  1. **연산이 엔티티나 값 객체의 자연스러운 일부가 아닌 도메인 개념에 관계된다.**
  2. **인터페이스가 도메인 모델의 다른 요소들의 관점에서 정의된다.**
  3. **연산이 무상태다.**
- **셋째의 뜻이 좁게 규정된다** (5장, pp.105–106):[^evans2003]

> Statelessness here means that any client can use any instance of a particular SERVICE
> without regard to the instance's individual history. The execution of a SERVICE will use
> information that is accessible globally, and may even change that global information (that
> is, it may have side effects). But the SERVICE does not hold state of its own that affects
> its own behavior, as most domain objects do.

  - **부수 효과 금지가 아니다.** 서비스는 전역 정보를 바꿔도 된다. 금지되는 것은
    **자기 행동에 영향을 주는 자기 상태**를 갖는 것뿐이다.
  - 이 구분이 [부수 효과 없는 함수](side-effect-free-functions.md)와 어긋나지 않는다 —
    그쪽은 연산을 질의와 명령으로 가르는 조항이고, 여기 무상태는
    **인스턴스 교체 가능성**에 대한 조건이다. 두 조항은 서로 다른 축이다.

## 조항

- 처방 문단이다 (5장, p.106):[^evans2003]

> When a significant process or transformation in the domain is not a natural responsibility
> of an ENTITY or VALUE OBJECT, add an operation to the model as a standalone interface
> declared as a SERVICE. Define the interface in terms of the language of the model and make
> sure the operation name is part of the UBIQUITOUS LANGUAGE. Make the SERVICE stateless.

## 세 층의 서비스를 가르는 기준

- 먼저 이 패턴의 범위가 좁혀진다 — **이 패턴은 그 자체로 도메인에서 중요한 의미를 갖는
  서비스에 초점을 맞추지만, 물론 서비스가 도메인 층에서만 쓰이는 것은 아니다**
  (5장 §"SERVICES and the Isolated Domain Layer", p.106).[^evans2003]
- 그래서 갈라내는 일이 필요하다 — **도메인 층에 속하는 서비스를 다른 층의 서비스와 구별하고,
  그 구별을 날카롭게 유지하도록 책임을 인수분해하는 데 주의가 든다**
  (5장, p.106).[^evans2003]
- **기반 층부터 잘라 낸다** — **문헌에서 논의되는 서비스 대부분은 순전히 기술적이며 기반
  (infrastructure) 층에 속한다** (5장, p.106).[^evans2003] 잔액이 임계치 아래로 떨어질 때
  고객에게 전자우편을 보내는 은행 애플리케이션에서, **전자우편 시스템과 대체 통지 수단을
  캡슐화하는 인터페이스가 기반 층의 서비스다**.
- **어려운 것은 애플리케이션과 도메인의 구분이다** — **애플리케이션 서비스를 도메인 서비스와
  구별하는 것이 더 어려울 수 있다** (5장, p.106).[^evans2003]
- 그리고 판정 기준이 한 줄로 선다 — **기술 서비스는 업무적 의미를 전혀 갖지 않아야 한다**
  (5장, p.106).[^evans2003]

## 계좌 이체 — 층별 분담의 실물

- 같은 은행 예제에서 책임이 갈린다 (5장, p.106):[^evans2003]
  - **애플리케이션 층은 통지를 지시할 책임을 진다.**
  - **도메인 층은 임계치가 충족되었는지 판정할 책임을 진다** — 다만 저자가 곧바로 덧붙인다.
    **이 일은 아마 서비스를 부르지 않을 것이다. "account" 객체의 책임에 맞을 것이기
    때문이다.** 서비스를 쓸 자리인지부터 의심하는 절차다.
- 이체(funds transfer)는 다르다 (5장, pp.106–107):[^evans2003]
  - **이체에 맞는 차변과 대변을 만드는 서비스를 고안한다면 그 능력은 도메인 층에 속할
    것이다. 이체는 은행 도메인 언어에서 의미를 가지며 근본적인 업무 로직을 담고 있다.**
  - 대조군이 붙는다 — **은행 애플리케이션이 우리 거래를 스프레드시트 파일로 변환해 내보낼 수
    있다면, 그 내보내기는 애플리케이션 서비스다. 은행 도메인에 "파일 형식"의 의미는 없고,
    관여하는 업무 규칙도 없다** (5장, p.107).[^evans2003]
- **그리고 왜 계좌 객체의 메서드가 아닌가가 설명된다** — **이 경우 서비스는 스스로 많은 일을
  하지 않는다. 대부분의 일은 두 `Account` 객체에게 시킬 것이다. 그러나 "이체" 연산을
  `Account` 객체에 두는 것은 어색할 텐데, 그 연산이 계좌 둘과 몇몇 전역 규칙에 관여하기
  때문이다** (5장, p.107).[^evans2003]
- 저자가 대안 하나를 검토하고도 남는 문제를 적는다 — `Funds Transfer` 객체를 만들어 두 항목과
  규칙과 이력을 표상할 수도 있지만 **여전히 은행 간 네트워크의 서비스 호출이 남는다.** 그런
  외부 서비스는 **모델의 관점에서 입력을 받는 FACADE로 감싸** `Funds Transfer` 객체를 결과로
  돌려줄 수 있다 (5장, p.107).[^evans2003]
- 결론이 소유권과 무관하다 — **어떤 중개자가 있든, 그리고 그것들이 우리 것이 아니더라도, 그
  서비스들은 이체라는 도메인 책임을 수행하고 있다** (5장, p.107).[^evans2003]
- **층별 분담이 표로 인쇄돼 있다** (5장 "Partitioning Services into Layers",
  p.107):[^evans2003]

| 층 | 서비스 | 하는 일 |
|---|---|---|
| 애플리케이션 | Funds Transfer App Service | 입력(예컨대 XML 요청)을 소화한다. 이행을 위해 도메인 서비스에 메시지를 보낸다. 확인을 기다린다. 기반 서비스를 써서 통지를 보낼지 결정한다 |
| 도메인 | Funds Transfer Domain Service | 필요한 `Account`·`Ledger` 객체들과 상호작용하며 적절한 차변과 대변을 만든다. 결과의 확인을 제공한다(이체 허용 여부 등) |
| 기반 | Send Notification Service | 애플리케이션의 지시에 따라 전자우편·우편·기타 통신을 보낸다 |

- **이 표가 이 페이지의 실무적 핵심이다.** 같은 사용 사례 하나가 세 층에 각각 서비스를
  갖는다는 것이 요점이고, 그래서 "서비스"라는 낱말만으로는 어느 층인지 알 수 없다.
  층 자체의 규정은 [계층 아키텍처](layered-architecture.md)에 있다.

## 굵기 — 지식이 새는 것을 막는 둘째 값

- 이 절이 표현력과 다른 축을 연다 — **이 패턴 논의가 개념을 서비스로 모델링하는 표현력을
  강조했지만, 이 패턴은 도메인 층 인터페이스의 굵기(granularity)를 통제하는 수단으로도,
  그리고 클라이언트를 엔티티·값 객체에서 떼어 내는 수단으로도 값이 있다**
  (5장 §Granularity, p.108).[^evans2003]
- 두 가지 실무 이득이 적힌다 — **중간 굵기의 무상태 서비스는 큰 시스템에서 재사용하기 더
  쉬울 수 있는데, 단순한 인터페이스 뒤에 상당한 기능을 캡슐화하기 때문이다. 또한 잘게 쪼개진
  객체는 분산 시스템에서 비효율적인 메시징으로 이어질 수 있다** (5장, p.108).[^evans2003]
- **그리고 누출의 기제가 서술된다** (5장, p.108):[^evans2003]

> As previously discussed, fine-grained domain objects can contribute to knowledge leaks from
> the domain into the application layer, where the domain object's behavior is coordinated.
> The complexity of a highly detailed interaction ends up being handled in the application
> layer, allowing domain knowledge to creep into the application or user interface code, where
> it is lost from the domain layer.

  - 처방 — **도메인 서비스를 신중하게 들이면 층 사이의 뚜렷한 선을 유지하는 데 도움이 될 수
    있다** (5장, p.108).[^evans2003]
  - **이것이 [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md)의 누출을 층
    단위로 말한 것이다.** 새는 것이 구현 세부가 아니라 **도메인 지식**이고, 새는 방향이
    위(애플리케이션 층)라는 점이 이 판본의 특색이다.
- 절충이 명시된다 — **이 패턴은 클라이언트의 통제와 다재다능함보다 인터페이스의 단순함을
  선호한다. 그것은 크거나 분산된 시스템의 구성 요소를 패키징하는 데 매우 유용한 중간 굵기의
  기능을 제공한다. 그리고 때로는 서비스가 도메인 개념을 표현하는 가장 자연스러운 방법이다**
  (5장, p.108).[^evans2003]
  - **잃는 것을 적어 두었다는 점이 중요하다.** 굵은 인터페이스는 클라이언트가 세밀하게
    조합할 여지를 줄인다. [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)이 같은
    절충을 인지 부하 쪽에서 보고, 이쪽은 층의 경계 쪽에서 본다.

## 접근 수단은 부차적이다

- 2003년 시점의 분산 아키텍처(J2EE·CORBA)가 서비스 발행 기제를 제공하지만 저자가 그것을
  요건에서 뺀다 — **그러나 그런 프레임워크가 프로젝트에서 늘 쓰이는 것은 아니고, 쓰인다
  해도 동기가 그저 관심사의 논리적 분리일 때는 과잉일 가능성이 높다**
  (5장 §"Access to SERVICES", p.108).[^evans2003]
- 조항이 한 줄이다 (5장, p.108):[^evans2003]

> The means of providing access to a SERVICE is not as important as the design decision to
> carve off specific responsibilities.

- 그래서 구현이 소박해도 된다 — **"행위자" 객체가 서비스 인터페이스의 구현으로 만족스러울 수
  있다. 단순한 SINGLETON을 쉽게 써서 접근을 제공할 수 있다. 코딩 규약으로 이 객체들이
  서비스 인터페이스의 전달 기제일 뿐이고 의미 있는 도메인 객체가 아님을 분명히 할 수 있다**
  (5장, p.108).[^evans2003]
  - **위에서 "Manager로 끝나는 가짜 객체"라 비판한 것과 같은 구현이 여기서 허용된다.**
    달라진 것은 구현이 아니라 **모델에서의 선언**이다 — 서비스로 선언되면 같은 클래스가
    오도하지 않는다.
- 그리고 정교한 아키텍처의 조건이 걸린다 — **정교한 아키텍처는 시스템을 분산할 진짜 필요가
  있거나 프레임워크의 능력을 끌어 쓸 필요가 있을 때만 써야 한다** (5장, p.108).[^evans2003]

## 팩토리가 서비스가 되는 자리

원전 6장이 이 패턴을 한 번 더 부른다. 복잡한 조립을 감출 곳이 필요한데 **자연스러운 거처가
없을 때**다.

- 배치의 제약이 먼저 나온다 — **팩토리(FACTORY)는 자기 산물에 아주 단단히 결합되므로, 산물과
  가까운 자연스러운 관계를 가진 객체에만 붙여야 한다** (6장, p.141).[^evans2003]
- 그 조건이 안 맞으면 독립형이 된다 — **감추고 싶은 것이 있는데(구체 구현이든 생성의 순전한
  복잡성이든) 자연스러운 거처가 없어 보일 때, 우리는 전용 팩토리 객체나 서비스를 만들어야
  한다** (6장, p.141).[^evans2003]
  - **위 [무엇이 서비스인가](#무엇이-서비스인가)의 기준과 어긋나지 않는다.** 독립형 팩토리는
    상태를 캡슐화하지 않고, 인터페이스가 모델의 다른 요소로 정의되며, 연산이 무상태다 — 이
    페이지가 세운 세 특징 그대로다. 다른 점은 그 연산이 도메인 언어의 낱말이 아니라 **구현의
    필요**라는 것이고, 저자 자신이 그 예외를 명시한다: **우리는 모델의 무엇에도 대응하지 않는
    요소를 설계에 더하고 있지만, 그럼에도 그것들은 도메인 층의 책임의 일부다** (6장,
    p.138).[^evans2003]
  - 전문은 [팩토리 패턴](factories-pattern.md)에 있다.

## 무상태 객체라는 규정 — 2021년 판본

[khononov2021](../sources/khononov2021.md)이 같은 패턴을 도메인 모델의 구성 단위 셋 중 마지막
자리에 놓는다. 부르는 조건은 원전과 같고 규정의 형태가 다르다.

- 부르는 조건이 원전과 같다 — **머지않아 어떤 애그리게이트에도 값 객체에도 속하지 않거나
  여러 애그리게이트에 관련되어 보이는 업무 로직을 만나게 된다. 그런 경우 도메인 주도 설계는
  그 로직을 도메인 서비스로 구현하기를 제안한다** (6장 §"Domain services",
  p.92).[^khononov2021]
  - 위 [사물이 아닌 것을 사물로 만들 때](#사물이-아닌-것을-사물로-만들-때)의 원전 문제 서술과
    같은 자리다. 다른 것은 **여러 애그리게이트에 걸린다**는 조건을 명시적으로 든다는 점이고,
    원전은 같은 것을 "여러 도메인 객체를 함께 끌어모아 조율한다"로 적는다.
- **규정이 인터페이스가 아니라 객체로 온다** (6장, p.93):[^khononov2021]

> A domain service is a stateless object that implements the business logic. In the vast
> majority of cases, such logic orchestrates calls to various components of the system to
> perform some calculation or analysis.

  - **원전의 정의와 대질하면 두 가지가 다르다.** 위 [무엇이 서비스인가](#무엇이-서비스인가)의
    원 정의는 **모델에서 홀로 서는 인터페이스로 제공되는 연산**이라고 적고 구현 형태를
    규정하지 않는다. 이 판본은 **객체**라고 적는다. 그리고 원전은 무상태를 좋은 서비스의 세
    특징 중 하나로 두는데, 이 판본은 그것을 정의에 넣는다.
  - **무상태의 뜻은 원전 쪽이 더 좁게 규정해 두었다** — 위
    [좋은 서비스의 세 특징](#좋은-서비스의-세-특징)이 옮긴 대로 금지되는 것은 **자기 행동에
    영향을 주는 자기 상태**이고 전역 정보를 바꾸는 것은 허용된다. 이 판본은 무상태의 뜻을
    따로 풀지 않는다. 두 소스를 함께 읽을 때 그 규정을 원전 쪽에서 가져와야 한다.
- 6장 맺음이 같은 것을 한 줄로 되풀이한다 — **도메인 모델의 어떤 애그리게이트에도 값 객체에도
  자연스럽게 속하지 않는 업무 로직을 담는 무상태 객체** (6장 §Conclusion,
  p.96).[^khononov2021]

## 응답 기한 계산 — 여러 애그리게이트에서 읽는다

- 예제가 헬프데스크의 응답 기한이다. 상담원이 해법을 제시해야 하는 기한이 **티켓의 데이터
  (우선순위와 이관 여부)뿐 아니라 상담원 부서의 우선순위별 응답 시간 정책과 상담원의 근무
  교대 일정에도 달렸다** — 근무 시간 밖에 응답하라고 할 수는 없기 때문이다
  (6장, p.93).[^khononov2021]
- **그래서 이 계산이 도메인 서비스의 이상적인 후보가 된다** — **응답 기한 계산 로직이 티켓,
  배정된 상담원의 부서, 그리고 근무 일정이라는 여러 출처의 정보를 요구하기 때문**이다
  (6장, p.93).[^khononov2021]
- 구현은 부서 정책을 읽어 우선순위별 최대 응답 시간을 얻고, 이관되었으면 정책의 이관 계수를
  곱하고, 그 범위의 근무 교대를 읽어 목표 시각을 계산한다 (6장, p.93):[^khononov2021]

  ```csharp
  public ResponseTimeframe CalculateAgentResponseDeadline(UserId agentId, Priority priority,
      bool escalated, DateTime startTime)
  {
      var policy = _departmentRepository.GetDepartmentPolicy(agentId);
      var maxProcTime = policy.GetMaxResponseTimeFor(priority);

      if (escalated) {
          maxProcTime = maxProcTime * policy.EscalationFactor;
      }

      var shifts = _departmentRepository.GetUpcomingShifts(agentId, startTime,
                       startTime.Add(policy.MaxAgentResponseTime));

      return CalculateTargetTime(maxProcTime, shifts);
  }
  ```

  - **이 조각이 위 [계좌 이체 — 층별 분담의 실물](#계좌-이체--층별-분담의-실물)과 같은 모양
    이면서 결정적으로 다르다.** 둘 다 여러 도메인 객체를 조율하지만, 이체 쪽은 두 계좌에
    차변과 대변을 **만들고** 이쪽은 세 곳에서 **읽기만** 한다. 그 차이가 다음 절의 조항이다.

## 빠져나갈 구멍이 아니다

**이 절이 이 판본이 이 패턴에 더하는 가장 강한 조항이다.**

- 이득을 먼저 적고 곧바로 제한한다 (6장, p.93):[^khononov2021]

> Domain services make it easy to coordinate the work of multiple aggregates. However, it is
> important to always keep in mind the aggregate pattern's limitation of modifying only one
> instance of an aggregate in one database transaction. Domain services are not a loophole
> around this limitation. The rule of one instance per transaction still holds true. Instead,
> domain services lend themselves to implementing calculation logic that requires reading the
> data of multiple aggregates.

  - 그 제약의 전문은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
- **원전과 대질했고 겨루는 자리가 남는다. 모순 쌍으로 세우지는 않았다.**
  - **원전의 계좌 이체 도메인 서비스는 두 `Account` 객체에 차변과 대변을 만든다.** 위
    [계좌 이체 — 층별 분담의 실물](#계좌-이체--층별-분담의-실물)의 표 가운데 줄이 그것이고,
    이 판본의 조항을 그대로 적용하면 그 서비스는 한 트랜잭션에 두 애그리게이트를 고치는
    셈이라 허용되지 않는다.
  - **그러나 대상이 다르다.** 이 판본의 제한이 걸리는 것은 **애그리게이트**이고, 원전의 계좌
    이체 예제가 다루는 `Account`가 애그리게이트 루트인지를 원전이 밝히지 않는다. 둘이 한
    애그리게이트 안의 엔티티라면 두 소스가 어긋나지 않는다.
  - **그리고 이 제한의 출처가 이 판본이 새로 세운 조항이다.** 원전의 구현 규칙 일곱에는 한
    트랜잭션에 애그리게이트 하나라는 수량 제한이 없다. 그 차이의 분석은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 적어
    두었고, 이 절의 차이는 그 차이에서 파생된다. 즉 **도메인 서비스에서 갈리는 것이 아니라
    애그리게이트에서 갈린 것이 여기까지 내려온 것이다.** 그래서 이 페이지에
    `contradicts`를 걸지 않았다.
- 마지막 단서가 이름에 걸린다 — **도메인 서비스는 마이크로서비스, 서비스 지향 아키텍처, 또는
  소프트웨어 공학에서 "서비스"라는 낱말이 쓰이는 거의 모든 다른 용법과 아무 관계가 없다.
  그것은 그저 업무 로직을 담는 데 쓰이는 무상태 객체다** (6장, p.93).[^khononov2021]
  - 위 [이 낱말이 이 KB에서 갈리는 자리](#이-낱말이-이-kb에서-갈리는-자리)가 그 혼동을 이 KB
    안에서 정리한 목록이고, 이 판본이 같은 경고를 배치 단위(마이크로서비스)까지 넓힌다.

## 이 낱말이 이 KB에서 갈리는 자리

- **이 페이지가 다루는 것은 도메인 층의 서비스다.** 이 KB에서 같은 낱말을 쓰는 다른 페이지가
  둘 있고, 셋이 가리키는 것이 다르다.
  - [서비스 레이어](service-layer-pattern.md)는 **애플리케이션 서비스**를 다룬다 — 조율,
    사용 사례, 웹 핸들러에서 내려온 잡일. 위 표의 첫 줄이 그것이다.
  - [도메인 객체가 된 프로세스](processes-as-domain-objects.md)는 같은 저자가 9장에서
    이 패턴을 **암묵적 프로세스를 명시하는 수단**으로 다시 부르는 자리다.
  - 이 페이지는 그 패턴의 원 규정이다.
  - **같은 낱말을 배포 단위에 쓰는 소스가 이 KB에 하나 더 있다.**
    [도메인 서비스 만들기](create-domain-services.md)의 도메인 서비스는 **한 도메인의 기능
    전부를 담고 따로 배포되는 굵은 소프트웨어 단위**이고 그 안에 컴포넌트가 여럿 들어 있다
    (5장, p.126).[^ford2021-hard-parts]
    **이 페이지의 것은 코드 안의 한 클래스이므로 층이 다르다** — 그쪽 도메인 서비스 하나
    안에 이 페이지의 도메인 서비스가 여럿 들어 있을 수 있다. **두 소스가 서로를 호명하지
    않으며 이 배치는 이 KB가 세운 것이다.** #hypothesis
- 판정 기준도 갈린다. 이 페이지의 기준은 **도메인 언어에 그 낱말이 있고 업무 규칙이
  관여하는가**이고, 9장의 기준은 **도메인 전문가가 그것을 이야기하는가**이며,
  [서비스 레이어](service-layer-pattern.md)가 옮긴 파이썬 쪽 기준은 **상태를 가진 객체에
  자연히 앉는가**다. 셋은 배타적이지 않고 대개 같은 답을 낸다.

## 외부 시스템의 인터페이스에 무슨 이름을 붙이는가

같은 원전의 7장이 서비스로 이름 짓는 일이 판정이 되는 자리를 하나 보인다. 전체 결정 순서는
[화물 운송 예제](../concepts/cargo-shipping-example.md)에 있다.

- 상황은 다른 팀의 시스템(영업 관리 시스템)에서 할당 정보를 받아 와야 하는 것이다. 직접 붙으면
  **그쪽 설계를 수용해야 하고 모델 주도 설계가 흐려지며 유비쿼터스 언어가 혼탁해지므로**,
  우리 모델과 저쪽의 말 사이를 번역하는 클래스를 세운다. 그것은 일반적 번역 기제가 아니라
  **우리 애플리케이션이 필요로 하는 기능만 노출하고 우리 도메인 모델의 용어로 재추상한다**
  (7장, p.182).[^evans2003]
- **이름을 짓는 자리에서 판정이 갈린다.** 저쪽 시스템의 인터페이스이므로 "영업 관리 인터페이스"
  같은 이름이 먼저 떠오르는데, 저자는 그것을 **문제를 우리에게 더 쓸모 있는 선으로 다시 주조할
  기회를 놓치는 것**으로 본다. 대신 **필요한 기능마다 서비스를 정의하고, 우리 시스템에서의
  책임을 반영하는 이름을 가진 클래스로 구현한다** — "할당 확인기"다 (7장,
  p.183).[^evans2003]
  - 저쪽 프로그램과 말하는 기계적인 일을 맡는 더 낮은 수준의 클래스는 있어도 되지만, 그것은
    **번역을 책임지지 않고 할당 확인기 뒤에 숨어 도메인 설계에 나타나지 않는다.**
  - 위 [무엇이 서비스인가](#무엇이-서비스인가)의 동사 이름 관례가 여기서 한 걸음 더 간다.
    **이름의 출처를 우리 도메인에 두라는 것**이고, 그래야 그 클래스가 도메인 설계의 일부가
    된다. 저쪽 시스템의 이름을 쓰면 그것은 우리 모델 밖의 어댑터로 남는다.
- 그리고 **책임의 배분이 인터페이스를 다시 그린다.** 첫 설계에서는 예약 애플리케이션이 업무
  규칙을 집행하고 엔터프라이즈 세그먼트를 파생하는데, 저자는 **업무 규칙 집행이 도메인 책임이고
  애플리케이션 층에서 수행되어서는 안 된다**고 판정한다. 두 책임을 모두 할당 확인기로 옮기고
  **그 인터페이스를 둘로 갈라 상호작용을 명확하고 명시적으로 만든다** (7장,
  pp.184–185).[^evans2003]
  - 위 [굵기 — 지식이 새는 것을 막는 둘째 값](#굵기--지식이-새는-것을-막는-둘째-값)이 말한
    작용이 통합 지점에서 벌어진 자리다. 서비스가 굵어지자 애플리케이션 층이 얇아진다.

## 번역 계층의 얼굴도 서비스다

14장이 두 경계 컨텍스트를 잇는 장치를 설계할 때 이 패턴을 인터페이스의 기본형으로 쓴다.

- 부패 방지 계층의 공개 인터페이스 — **보통 서비스의 집합으로 나타나며 가끔 엔티티의 형태를
  띠기도 한다** (14장, p.366).[^evans2003]
- **그 이유가 이 페이지의 논거와 같다.** 저쪽 시스템을 하나의 덩어리로 표상하는 것이 **우리
  모델에서 말이 되지 않을 수도 있고, 우리 모델의 관점에서 각각 정합적인 책임을 갖는 여러
  서비스를 쓰는 것이 최선일 수 있다** (14장, p.366).[^evans2003] 위
  [무엇이 서비스인가](#무엇이-서비스인가)가 요구하는 "모델의 말로 정의된 인터페이스"가 시스템
  경계에서도 그대로 걸린다.
- 그리고 서비스마다 짝이 생긴다 — **우리가 정의하는 각 서비스마다 그 서비스의 인터페이스를
  지원하고 저쪽 시스템이나 그 파사드에 동등한 요청을 하는 법을 아는 어댑터가 필요하다** (14장,
  p.367).[^evans2003] 그 구조는 [부패 방지 계층](../concepts/anticorruption-layer.md)에 있다.
- **같은 장의 다른 패턴도 이 단위를 쓴다** — 열린 호스트 서비스의 처방이 **서브시스템에 대한
  접근을 서비스의 집합으로 주는 프로토콜을 정의하라**이고, 그 적용 조건이 **서브시스템의 자원이
  정합적인 서비스 집합으로 서술될 수 있을 때**로 걸린다 (14장, p.374).[^evans2003] 그 대가는
  [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)에 있다.

## 이어지는 페이지

- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 패턴이 구성 단위로 드는 모델
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 이 패턴이
  우회하지 못하는 제약
- [서비스 레이어](service-layer-pattern.md) — 위 표 첫 줄의 애플리케이션 서비스
- [도메인 객체가 된 프로세스](processes-as-domain-objects.md) — 같은 패턴을 9장이 다시 부르는 자리
- [도메인 서비스 만들기](create-domain-services.md) — 같은 이름을 배포 단위에 쓰는 자리
- [계층 아키텍처](layered-architecture.md) — 세 층의 규정
- [팩토리 패턴](factories-pattern.md) — 거처가 없을 때 서비스로 서는 조립 책임
- [값 객체와 엔티티](value-objects-and-entities.md) — 서비스가 되기 전에 시도해야 할 두 자리
- [유비쿼터스 언어](ubiquitous-language.md) — 연산 이름이 와야 하는 곳
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — 도메인 지식이 위로 새는 기제
- [이름 짓기](../concepts/naming-things.md) — Manager로 끝나는 이름이 알려 주는 것
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^evans2003]: Evans 2003, 7장 "Using the Language: An Extended Example"
    §"Introducing a New Feature: Allocation Checking"(pp.182–185) ·
    5장 "A Model Expressed in Software" §SERVICES(pp.104–108) —
    도입과 문제 서술(pp.104–105) · 정의와 세 특징(p.105) · 처방 문단(p.106) ·
    §"SERVICES and the Isolated Domain Layer"(pp.106–107)과 그 층별 분담 목록(p.107) ·
    §Granularity(p.108) · §"Access to SERVICES"(p.108) ·
    6장 "The Life Cycle of a Domain Object" §FACTORIES(p.138·p.141) ·
    14장 "Maintaining Model Integrity" §ANTICORRUPTION LAYER 중 §"Designing the Interface"
    (p.366)와 구현 논의(p.367) · §OPEN HOST SERVICE(p.374).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. 층별 분담은 원문이 층마다 제목과 불릿을 둔 상자 도해로
    조판한 것을 표로 옮겼다 — 문구는 원문 그대로이고 순서도 바꾸지 않았다. 패턴 도비라의
    사진과 Figure는 이미지라 옮기지 않았다. 이 소스에서 온 코드 펜스는 이 페이지에 없다 —
    이 절에 코드 목록이 없다.

[^khononov2021]: Khononov 2021, 6장 "Tackling Complex Business Logic" §"Domain services"
    (pp.92–93) · §Conclusion(p.96). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 직인용은
    `pdftotext -layout` 추출로 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다. 코드 펜스는
    하나만 두었다 — 원문이 클래스 선언과 `...` 생략 표시로 감싼 것을 메서드 하나만 남기고
    깎았고(감싼 줄을 지웠을 뿐 없는 줄을 보태지 않았다) 조판 폭 때문에 접힌 인자 목록의
    줄바꿈 위치는 조정했으며 언어 표지(`csharp`)는 이 KB가 붙였다. 이 절에 도판은 없다.

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 5장 "Component-Based
    Decomposition Patterns" §"Create Domain Services Pattern" 도입(p.126). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 18, 실측). 이 페이지는 그 규정을 이름 겹침을 가르는 데만 쓴다 — 전문과
    직인용은 [도메인 서비스 만들기](create-domain-services.md)가 갖는다.

---
type: concept
title: 도메인의 모듈
description: 모듈을 기술 구획이 아니라 모델의 일부로 다루는 패턴의 원전 — 모듈화의 일차 동기가 기술이 아니라 인지 과부하라는 규정과 모듈이 주는 두 시야, 결합도와 응집도를 기계적 지표가 아니라 개념에 적용하라는 되읽기, 모듈이 이야기의 장이고 그 이름이 유비쿼터스 언어에 들어간다는 조항, 절충이 생기면 개념적 명료함을 고르라는 판정, 모듈 리팩터링이 안 일어나는 이유와 애자일 모듈, 자바 패키지 임포트 규약 예제, 기반 구조가 주도한 패키징이 모델을 조각내는 두 비용과 그 결과 빈혈 도메인이 남은 사례, 그리고 선언적 설계로 생성된 코드라는 예외
generated: { by: "claude-opus-5", at: "2026-09-14T09:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 도메인의 모듈

- [일차 동기는 인지 과부하다](#일차-동기는-인지-과부하다)
- [결합도와 응집도를 개념에 적용한다](#결합도와-응집도를-개념에-적용한다)
- [모듈은 이야기의 장이다](#모듈은-이야기의-장이다)
- [조항](#조항)
- [절충이 생기면 개념적 명료함을 고른다](#절충이-생기면-개념적-명료함을-고른다)
- [애자일 모듈 — 왜 리팩터링이 안 일어나는가](#애자일-모듈--왜-리팩터링이-안-일어나는가)
- [자바 패키지 임포트 규약](#자바-패키지-임포트-규약)
- [기반 구조가 주도한 패키징의 함정](#기반-구조가-주도한-패키징의-함정)
- [두 비용과 두 조항](#두-비용과-두-조항)
- [깊이를 잣대로 쓰는 축과 나란히](#깊이를-잣대로-쓰는-축과-나란히)
- [패턴별로 가르는 것도 같은 오류다](#패턴별로-가르는-것도-같은-오류다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **코드를 무엇을 기준으로 묶어야 그 묶음 자체가 도메인을 말하게 되는가.**

## 일차 동기는 인지 과부하다

- 모듈(MODULE, 자바에서는 패키지)은 오래된 설계 요소이고, 저자가 동기의 순서를 명시한다 —
  **기술적 고려도 있지만, 모듈화의 일차 동기는 인지 과부하(cognitive overload)다**
  (5장 §MODULES (A.K.A. PACKAGES), p.109).[^evans2003]
- 그 과부하를 더는 방식이 두 시야다 (5장, p.109):[^evans2003]

> MODULES give people two views of the model: They can look at detail within a MODULE without
> being overwhelmed by the whole, or they can look at relationships between MODULES in views
> that exclude interior detail.

- 그리고 도메인 층의 모듈에 걸리는 요구가 따로 있다 — **도메인 층의 모듈은 모델의 의미 있는
  일부로 떠올라, 더 큰 규모에서 도메인의 이야기를 해야 한다** (5장, p.109).[^evans2003]
- 문제 서술이 현실을 짚는다 — **모두가 모듈을 쓰지만 그것을 모델의 온전한 일부로 다루는
  사람은 거의 없다. 코드는 기술 아키텍처의 측면부터 개발자 업무 배정까지 온갖 범주로
  쪼개진다. 리팩터링을 많이 하는 개발자조차 프로젝트 초기에 구상된 모듈에 만족하는 경향이
  있다** (5장, p.109).[^evans2003]

## 결합도와 응집도를 개념에 적용한다

- 낡은 격언을 다시 읽는 자리다 (5장, p.109):[^evans2003]

> It is a truism that there should be low coupling between MODULES and high cohesion within
> them. Explanations of coupling and cohesion tend to make them sound like technical metrics,
> to be judged mechanically based on the distributions of associations and interactions. Yet
> it isn't just code being divided into MODULES, but concepts. There is a limit to how many
> things a person can think about at once (hence low coupling). Incoherent fragments of ideas
> are as hard to understand as an undifferentiated soup of ideas (hence high cohesion).

  - **두 지표가 인지 능력의 두 한계로 환원된다는 것이 이 문단의 값이다.** 낮은 결합은 한 번에
    생각할 수 있는 것의 수 제한에서, 높은 응집은 조각난 생각이 뭉개진 생각만큼 이해하기
    어렵다는 데서 나온다. 계산으로 나오는 값이 아니다.
- 규모에 대한 단서가 붙는다 — **낮은 결합과 높은 응집은 모듈만큼이나 개별 객체에도 적용되는
  일반 설계 원리지만, 모델링과 설계의 이 더 큰 알갱이에서 특히 중요하다**
  (5장, p.109).[^evans2003]
- 비용이 구체화된다 — **두 모델 요소가 서로 다른 모듈로 갈리면 그들 사이의 관계가 전보다 덜
  직접적이 되어, 설계에서 그것들의 자리를 이해하는 부담이 커진다. 모듈 사이의 낮은 결합이 이
  비용을 최소화하고, 한 모듈의 내용을 다른 모듈에 대한 참조를 최소한으로 하면서 분석할 수
  있게 만든다** (5장, p.109).[^evans2003]
- 응집 쪽의 이득도 같은 어휘다 — **좋은 모델의 요소들은 상승 작용을 갖고, 잘 고른 모듈은
  특히 풍부한 개념적 관계를 가진 모델 요소들을 한데 모은다. 관련 책임을 가진 객체들의 이 높은
  응집은 모델링과 설계 작업이 한 모듈 안에 집중될 수 있게 하는데, 그것은 사람의 마음이 쉽게
  다룰 수 있는 복잡도의 규모다** (5장, p.110).[^evans2003]

## 모듈은 이야기의 장이다

- 모듈과 그 안의 요소가 함께 진화해야 하는데 보통 그러지 않는다 — **모듈은 객체의 초기 형태를
  조직하려고 선택된다. 그 뒤 객체들은 기존 모듈 정의의 경계 안에 머무는 방향으로 변하는
  경향이 있다** (5장, p.110).[^evans2003]
- 리팩터링 빈도의 차이가 인정된다 — **모듈을 리팩터링하는 것은 클래스를 리팩터링하는 것보다
  일이 더 많고 더 파괴적이며, 아마 그만큼 자주 할 수도 없다** (5장, p.110).[^evans2003]
  그러나 방향은 같다 — **모델 객체가 소박하고 구체적으로 출발했다가 점차 더 깊은 통찰을
  드러내도록 변형되듯, 모듈도 미묘하고 추상적이 될 수 있다.**
- **그리고 모듈의 지위가 정해진다** (5장, p.110):[^evans2003]

> Like everything else in a domain-driven design, MODULES are a *communications mechanism*.
> The *meaning* of the objects being partitioned needs to drive the choice of MODULES. When
> you place some classes together in a MODULE, you are telling the next developer who looks at
> your design to think about them together. If your model is telling a story, the MODULES are
> chapters. The name of the MODULE conveys its meaning. These names enter the UBIQUITOUS
> LANGUAGE.

  - 그 언어의 실물이 대화로 제시된다 — **"이제 '고객' 모듈 이야기를 해 봅시다"라고 업무
    전문가에게 말할 수 있고, 그것으로 대화의 맥락이 정해진다** (5장, p.110).[^evans2003]
  - **패키지 이름이 업무 전문가와의 대화에 등장할 수 있는가가 이 절의 시험이다.**
    [유비쿼터스 언어](ubiquitous-language.md)의 요구가 클래스와 연산에서 패키지까지
    올라가는 자리다.

## 조항

- 처방 문단이 둘이다 (5장, pp.110–111):[^evans2003]

> Choose MODULES that tell the story of the system and contain a cohesive set of concepts.
> This often yields low coupling between MODULES, but if it doesn't, look for a way to change
> the model to disentangle the concepts, or search for an overlooked concept that might be the
> basis of a MODULE that would bring the elements together in a meaningful way. Seek low
> coupling in the sense of concepts that can be understood and reasoned about independently of
> each other. Refine the model until it partitions according to high-level domain concepts and
> the corresponding code is decoupled as well.

> Give the MODULES names that become part of the UBIQUITOUS LANGUAGE. MODULES and their names
> should reflect insight into the domain.

  - **첫 문단의 순서가 뒤집혀 있다는 점이 요점이다.** 낮은 결합은 목표가 아니라 결과이고,
    결과가 안 나오면 모듈 경계가 아니라 **모델**을 고친다. 결합이 높다는 것은 배치가
    잘못됐다는 신호가 아니라 **개념이 엉켜 있거나 이름을 못 받은 개념이 있다는 신호**다.
  - 이 되돌림이 [암묵적 개념을 파내기](digging-out-implicit-concepts.md)의 절차를 부른다 —
    "간과된 개념을 찾으라"가 그 절차다.

## 절충이 생기면 개념적 명료함을 고른다

- 두 잣대가 배타적이지 않다 — **개념적 관계를 보는 것이 기술적 측정의 대안은 아니다. 그것들은
  같은 문제의 다른 수준이고 둘 다 이뤄져야 한다** (5장, p.111).[^evans2003]
- 그럼에도 우선순위가 정해진다 (5장, p.111):[^evans2003]

> But model-focused thinking produces a deeper solution, rather than an incidental one. And
> when there has to be a trade-off, it is best to go with the conceptual clarity, even if it
> means more references between MODULES or occasional ripple effects when changes are made to
> a MODULE. Developers can handle these problems if they understand the story the model is
> telling them.

  - **모듈 사이 참조가 늘어도 좋다는 허가가 명시적으로 나온다.** 이 판정이 이 소스를 순수
    결합도 최소화 쪽 소스들과 가르는 자리다. 근거는 개발자가 이야기를 이해하면 그 문제를
    감당한다는 것이다.

## 애자일 모듈 — 왜 리팩터링이 안 일어나는가

- 요구는 공진화다 — **모듈은 모델의 나머지와 함께 진화해야 한다. 이는 모듈을 모델·코드와
  나란히 리팩터링한다는 뜻이다. 그러나 이 리팩터링은 자주 일어나지 않는다**
  (5장 §"Agile MODULES", p.111).[^evans2003]
- 안 일어나는 이유가 셋이다 (5장, p.111):[^evans2003]
  - **모듈을 바꾸면 코드에 광범위한 갱신이 필요한 경향이 있다.**
  - **그런 변경은 팀 소통을 어지럽힐 수 있고, 소스 코드 관리 시스템 같은 개발 도구에 훼방을
    놓을 수도 있다.**
  - **그 결과 모듈 구조와 이름은 클래스보다 훨씬 이른 시기의 모델 형태를 반영하는 일이 잦다.**
- 그리고 악순환이 서술된다 — **모듈 선택에서 피할 수 없는 초기 실수가 높은 결합으로 이어지고,
  그것이 리팩터링을 어렵게 만든다. 리팩터링의 부재는 관성을 계속 키우기만 한다. 그것은 이를
  악물고 어디가 말썽인지의 경험에 근거해 모듈을 재조직하는 것으로만 극복될 수 있다**
  (5장, p.111).[^evans2003]
  - **이 관성이 [개념의 윤곽](conceptual-contours.md)의 계측과 짝을 이룬다.** 그쪽은 연속
    리팩터링이 국소적인가를 모델 적합의 지표로 쓰는데, 모듈 수준의 리팩터링이 국소적이지
    않다는 것이 여기 서술된 그 지표의 나쁜 값이다.
- 도구에 대한 요구가 따라온다 — **구현이 어떤 개발 기술에 근거하든, 우리는 모듈 리팩터링의
  일을 최소화하고 다른 개발자에게 전달할 때의 잡동사니를 최소화할 방법을 찾아야 한다**
  (5장, p.111).[^evans2003]

## 자바 패키지 임포트 규약

- 자바에서는 의존을 개별 클래스에서 선언해야 한다 — **모델러는 아마 패키지가 다른 패키지에
  의존한다고 생각하겠지만, 자바에서는 그것을 진술할 수 없다** (5장 예제 "Package Coding
  Conventions in Java", pp.111–112).[^evans2003] 흔한 규약은 특정 클래스를 임포트하게 해
  `import packageB.ClassB1;`이 여러 줄 쌓이는 코드를 낳는다.
- 저자의 제안은 패키지 통째 임포트다 (5장, p.112).[^evans2003]

  ```java
  ClassA1
  import packageB.*;
  import packageC.*;
  . . .
  ```

  - 근거가 둘이다 — **적어도 한 번에 패키지 전체를 임포트할 수는 있는데, 이는 패키지가 높이
    응집된 단위라는 의도를 반영하면서 동시에 패키지 이름을 바꾸는 수고를 줄인다**
    (5장, p.112).[^evans2003]
  - 대가도 인정한다 — **사실 이 기법은 두 규모를 섞는다는 뜻이지만(클래스가 패키지에
    의존한다), 앞의 방대한 클래스 목록보다 더 많은 것을 전달한다. 그것은 특정 모듈에 대한
    의존을 만들겠다는 의도를 전한다** (5장, p.112).[^evans2003]
- **그리고 예외가 진단 도구가 된다** (5장, p.112):[^evans2003]

> If an individual class really does depend on a specific class in another package, and the
> local MODULE doesn't seem to have a conceptual dependency on the other MODULE, then maybe a
> class should be moved, or the MODULES themselves should be reconsidered.

  - 이 규약의 실제 값은 코드 절약이 아니라 **위반이 눈에 띄게 되는 것**이다. 개별 클래스
    임포트가 남아 있으면 그 자리가 배치 오류의 후보다.
  - 자바 쪽 사정은 2003년 시점의 것이고, 이후 언어가 모듈을 1급 요소로 들이면서 달라진
    자리는 [자바 모듈 시스템](../concepts/java-module-system.md)에 있다.

## 기반 구조가 주도한 패키징의 함정

- 프레임워크가 패키징에 미치는 힘이 양쪽이다 — **기술 프레임워크에서 우리 패키징 결정에 강한
  힘이 온다. 그중 일부는 도움이 되고 다른 일부는 저항해야 한다**
  (5장 §"The Pitfalls of Infrastructure-Driven Packaging", p.112).[^evans2003]
- **도움이 되는 쪽의 예가 계층 강제다** — **매우 유용한 프레임워크 표준의 한 예는, 기반 구조와
  사용자 인터페이스 코드를 별개의 패키지 묶음에 놓고 도메인 층을 자기 패키지 묶음으로
  물리적으로 분리해 계층 아키텍처를 강제하는 것이다** (5장, p.112).[^evans2003]
  전문은 [계층 아키텍처](layered-architecture.md)에 있다.
- **저항해야 하는 쪽이 티어 분할이다** — **다른 한편 티어 아키텍처는 모델 객체의 구현을
  조각낼 수 있다. 어떤 프레임워크는 단일 도메인 객체의 책임을 여러 객체에 흩고 그 객체들을
  별개의 패키지에 놓는 방식으로 티어를 만든다** (5장, p.113).[^evans2003]
  - 2003년 시점의 실물이 J2EE다 — **J2EE에서 흔한 관행은 데이터와 데이터 접근을 "entity
    bean"에 놓고 관련 업무 로직을 "session bean"에 놓는 것이다** (5장, p.113).[^evans2003]
  - 그 대가가 원리로 진술된다 — **각 구성 요소의 구현 복잡도가 늘어나는 것에 더해, 그 분리는
    객체 모델에서 응집을 즉각 빼앗는다. 객체의 가장 근본적인 개념 하나는 데이터를 그 데이터를
    다루는 로직과 함께 캡슐화하는 것이다** (5장, p.113).[^evans2003]
  - 치명적이지는 않으나 누적된다 — 두 구성 요소를 **단일 모델 요소의 구현으로 함께 볼 수
    있기** 때문에 치명적이지 않지만, **설상가상으로 엔티티 빈과 세션 빈이 서로 다른 패키지로
    갈리는 일이 잦고, 그 지점에서 여러 객체를 보고 그것을 머릿속에서 하나의 개념적 엔티티로
    다시 맞추는 일은 그저 너무 큰 수고가 된다. 우리는 모델과 설계 사이의 연결을 잃는다**
    (5장, p.113).[^evans2003]
- **저자 자신이 겪은 네 티어 프로젝트가 이 절의 증거다** (5장, pp.113–114):[^evans2003]
  - 개념 객체 하나가 네 티어로 쪼개져 있었고 **각 구획에는 좋은 근거가 있었다** — 데이터
    영속 층, 모든 상황에서 객체에 내재한 행동의 층, 애플리케이션 특화 기능을 덧입히는 층,
    아래의 모든 구현에서 결합이 끊긴 공개 인터페이스 층.
  - 분리 자체는 감당할 만했다 — **관심사의 분리에 나름의 정연함이 있었고**, 특히
    **영속성 코드가 빠진 것은 잡동사니를 많이 없앴다.**
  - **문제는 프레임워크가 티어마다 별개의 패키지 묶음을 요구했다는 것이다** — **이것이
    구획을 위한 정신적 여지를 전부 잡아먹었다. 그 결과 도메인 개발자들은 모듈을 너무 많이
    만들지 않으려는 경향을 보였고(각각이 넷으로 곱해지므로), 모듈을 리팩터링하는 수고가
    엄두를 못 낼 정도라 거의 바꾸지 않았다.**
  - 결과가 명시된다 — **애플리케이션은 인도되었으나, 기본적으로 애플리케이션의 데이터베이스
    접근 요구를 충족하고 행동은 몇몇 서비스가 공급하는 빈혈 도메인 모델(anemic domain
    model)과 함께였다. 모델 주도 설계에서 나왔어야 할 지렛대는 제한되었는데, 코드가 모델을
    투명하게 드러내 개발자가 그것으로 일하게 해 주지 않았기 때문이다** (5장,
    p.114).[^evans2003]
  - **빈혈 도메인이 나오는 경로가 하나 더 있다는 것이 이 사례의 값이다.**
    [서비스 레이어](service-layer-pattern.md)가 계상한 경로는 조율 층에 로직을 너무 많이
    넣는 것이고, 이쪽 경로는 **패키징이 모델을 조각내는 것**이다. 증상이 같고 원인이 다르다.
- 프레임워크 설계자의 동기가 둘 다 정당하다고 인정된다 — **관심사의 논리적 분리**(티어별
  이해와 교체가 쉬워진다)와 **티어의 분산**이다. 그리고 각각이 기각된다
  (5장, p.114):[^evans2003]
  - 첫째에 대해 — **문제는 애플리케이션 개발에 드는 비용이 인식되지 않는다는 것이다.** 대안이
    있지만 이 책의 주제가 아니라며, **설령 선택지가 없더라도 이 이득을 더 응집된 도메인 층과
    맞바꾸는 편이 나을 것이다**라고 적는다.
  - 둘째에 대해 — **코드가 실제로 서로 다른 서버에 배치된다면 강한 논거일 수 있다. 보통은
    그렇지 않다. 그 유연성은 필요해질 경우에 대비해 그저 추구될 뿐이다.** 그리고
    **모델 주도 설계에서 지렛대를 얻으려는 프로젝트에서, 이 희생은 당면한 절박한 문제를
    풀지 않는 한 너무 크다.**

## 두 비용과 두 조항

- **정교한 기술 주도 패키징 방식은 두 가지 비용을 부과한다** (5장, p.114):[^evans2003]

> - If the framework's partitioning conventions pull apart the elements implementing the
>   conceptual objects, the code no longer reveals the model.
> - There is only so much partitioning a mind can stitch back together, and if the framework
>   uses it all up, the domain developers lose their ability to chunk the model into
>   meaningful pieces.

- 그래서 기술 구획 규칙은 최소로 고른다 — **단순하게 유지하는 것이 가장 좋다. 기술 환경에
  본질적이거나 실제로 개발을 돕는 최소한의 기술적 구획 규칙을 골라라. 예컨대 복잡한 데이터
  영속성 코드를 객체의 행동 측면에서 떼어 내는 것은 리팩터링을 쉽게 만들 수 있다**
  (5장, pp.114–115).[^evans2003]
- 조항 첫째 (5장, p.115):[^evans2003]

> Unless there is a real intention to distribute code on different servers, keep all the code
> that implements a single conceptual object in the same MODULE, if not the same object.

  - 저자가 같은 결론에 다른 경로로도 도달한다 — **낡은 표준인 "높은 응집/낮은 결합"에
    기대어도 같은 결론에 이를 수 있었다. 업무 로직을 구현하는 "객체"와 데이터베이스 접근을
    맡은 객체 사이의 연결은 너무 광범위해 결합이 매우 높다** (5장, p.115).[^evans2003]
- 조항 둘째 (5장, p.115):[^evans2003]

> Use packaging to separate the domain layer from other code. Otherwise, leave as much freedom
> as possible to the domain developers to package the domain objects in ways that support
> their model and design choices.

  - **이 두 조항이 이 페이지의 실무 요지다.** 패키징에 기술이 개입할 몫은 **도메인 층을
    나머지와 가르는 것 하나**이고, 그 안쪽은 모델이 정한다.
- 함정이 프레임워크에만 있는 것은 아니다 — **프레임워크 설계나 그저 회사나 프로젝트의 규약이
  도메인 객체의 자연스러운 응집을 흐려 모델 주도 설계를 무너뜨리는 다른 함정들이 있지만,
  결론은 같다. 그 제약이나 그저 요구되는 패키지의 많은 수가, 도메인 모델의 필요에 맞춘 다른
  패키징 방식의 사용을 배제한다** (5장, p.115).[^evans2003]
- **예외가 하나 있다** — **선언적 설계에 근거해 코드가 생성될 때다. 그 경우 개발자가 코드를
  읽을 필요가 없으므로, 그것을 별도 패키지에 넣어 길을 비켜 두고 개발자가 실제로 다뤄야 할
  설계 요소를 어지럽히지 않게 하는 편이 낫다** (5장, p.115).[^evans2003] 그 설계 방식은
  [선언적 설계](declarative-design.md)에 있다.

## 깊이를 잣대로 쓰는 축과 나란히

이 KB에는 모듈을 다른 잣대로 판정하는 축이 있다. 둘이 부딪히는지 보아 둔다.

- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)은 모듈을 **인터페이스 대 구현의
  비율**로 판정하고, [범용 모듈이 더 깊다](../concepts/general-purpose-modules.md)는 인터페이스가
  특정 호출자에 맞춰지지 않는 편이 낫다고 본다. 이 페이지의 잣대는 **개념의 응집**이다.
- **모순이 아니다 — 두 잣대가 서로 다른 물음에 답한다.** 그쪽은 **경계가 어디 그어졌을 때
  인지 부하가 낮은가**를 묻고, 이쪽은 **경계가 무엇을 기준으로 그어져야 하는가**를 묻는다.
  같은 모듈이 개념적으로 응집돼 있으면서 인터페이스가 깊을 수 있고, 저자 자신이 응집을
  "사람의 마음이 쉽게 다룰 수 있는 복잡도의 규모"로 정당화하므로 근거도 겹친다.
- **다만 한 자리에서 답이 갈릴 수 있다.** 이 페이지는 개념적 명료함을 위해
  **모듈 사이 참조가 늘어도 좋다**고 허가하는데, 의존 최소화를 목표로 두는 쪽에서는 그것이
  손실이다. #hypothesis 두 소스가 그 자리에서 다른 답을 낼 수 있으나, 서로를 인용한 적이
  없고 실제로 갈린 사례도 이 KB에 없다.

## 패턴별로 가르는 것도 같은 오류다

같은 원전의 7장이 위
[기반 구조가 주도한 패키징의 함정](#기반-구조가-주도한-패키징의-함정)의 진단을 한 칸 넓힌다.
전체 결정 순서는 [화물 운송 예제](cargo-shipping-example.md)에 있다.

- 반례가 **이 책을 열심히 읽은 가상의 독자**의 것으로 제시된다. 해운 모델의 객체를 **각자가
  따르는 패턴에 따라** 묶은 것이다 — 엔티티 묶음, 값 객체 묶음, 서비스 묶음 (7장,
  p.179).[^evans2003]
- 진단이 이 페이지의 두 낱말로 나온다 — **개념적으로 관계가 거의 없는 객체들이 한데 밀어
  넣어지고(낮은 응집), 연관이 모든 모듈 사이를 제멋대로 오간다(높은 결합)** (7장,
  p.179).[^evans2003] 그리고 판정 한 줄 — 패키지가 이야기를 하기는 하는데 **그것은 해운의
  이야기가 아니라 개발자가 그때 무엇을 읽고 있었는지의 이야기**다.
- **진단의 폭이 여기서 넓어진다.** 저자가 패턴별 분할이 특별히 더 나쁜 것이 아니라고 적는다 —
  **영속 객체를 일시 객체와 분리하는 것이나, 객체의 의미에 근거하지 않은 다른 어떤 체계적
  방식보다 특별히 덜 분별 있는 것도 아니다** (7장, p.180).[^evans2003]
  - 위 절이 **기반 구조**를 범인으로 지목했다면 이 자리는 범인을 **"객체의 의미가 아닌 무엇이든"**
    으로 일반화한다. 기술 스택이 아니라 **기준의 종류**가 문제라는 것이다.
  - 그리고 이 오류의 출처가 기술적 무지가 아니라는 점이 반례의 설정에 들어 있다 — **패턴 책을
    성실히 읽은 사람**이 저지르는 오류로 그려진다.
- 고쳐진 분할(고객·해운·청구)의 값이 위 [모듈은 이야기의 장이다](#모듈은-이야기의-장이다)의
  기준으로 확인된다 — 그 이름들로 **"우리 회사는 고객을 위해 해운을 하고 그 대가로 청구한다"는
  이야기를 말할 수 있고**, 영업과 운영과 사무의 일이 각각 한 모듈에 대응한다. 그래서 **모듈
  이름들이 팀의 언어에 기여한다** (7장, p.181).[^evans2003]
  - 저자가 그 분할의 지위를 스스로 낮춘다 — **이후 반복에서 다듬어지거나 완전히 대체될 수
    있지만 지금은 모델 주도 설계를 돕고 유비쿼터스 언어에 기여하고 있다**는 것이다. 위
    [애자일 모듈 — 왜 리팩터링이 안 일어나는가](#애자일-모듈--왜-리팩터링이-안-일어나는가)가
    요구하는 태도의 실물이다.

## 이어지는 페이지

- [계층 아키텍처](layered-architecture.md) — 패키징이 강제해야 할 유일한 기술 구획
- [유비쿼터스 언어](ubiquitous-language.md) — 모듈 이름이 들어가야 하는 어휘
- [암묵적 개념을 파내기](digging-out-implicit-concepts.md) — 결합이 높을 때 찾아야 할 간과된 개념
- [개념의 윤곽](conceptual-contours.md) — 같은 저자가 요소의 굵기를 다루는 자리
- [선언적 설계](declarative-design.md) — 생성된 코드를 따로 두라는 예외의 출처
- [서비스 레이어](service-layer-pattern.md) — 빈혈 도메인으로 가는 다른 경로
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 같은 대상을 인지 부하로 재는 축
- [범용 모듈이 더 깊다](../concepts/general-purpose-modules.md) — 인터페이스의 일반성이라는 다른 잣대
- [자바 모듈 시스템](../concepts/java-module-system.md) — 이 예제 이후 언어가 모듈에 준 지위
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^evans2003]: Evans 2003, 7장 "Using the Language: An Extended Example"
    §"MODULES in the Shipping Model"(pp.179–181) ·
    5장 "A Model Expressed in Software" §MODULES (A.K.A. PACKAGES)
    (pp.109–116) — 도입과 문제 서술(p.109) · 결합도와 응집도 논의(pp.109–110) ·
    소통 기제 규정(p.110) · 처방 문단 둘(pp.110–111) · 절충 판정(p.111) ·
    §"Agile MODULES"(p.111) · 예제 "Package Coding Conventions in Java"(pp.111–112) ·
    §"The Pitfalls of Infrastructure-Driven Packaging"(pp.112–116).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. 패턴 도비라의 사진은 이미지라 옮기지 않았다.
    **코드 펜스는 패키지 통째 임포트 한 판만 두었다** — 원문은 개별 클래스 임포트와
    패키지 임포트를 전후 대비 쌍으로 싣고, 이 페이지는 저자가 권하는 쪽 하나만 옮긴 뒤
    비교 대상은 산문으로 서술했다. 원문의 `. . .` 생략 표기와 클래스 이름 머리줄을 그대로
    두었고 보탠 줄은 없다.

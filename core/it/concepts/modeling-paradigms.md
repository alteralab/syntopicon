---
type: concept
title: 모델링 패러다임
description: 모델 주도 설계가 객체를 요구하지 않는다는 규정과 그럼에도 객체가 지배적인 이유 — 단순함과 정교함의 균형이라는 내재적 이유와 성숙도·도구·개발자 공동체라는 정황적 이유, 미성숙한 패러다임에 걸었다가 몇 달을 잃은 객체 데이터베이스 사례와 그 경험이 애그리게이트 사고를 낳은 자리, 객체로 표현되지 않는 도메인이 있다는 인정과 패러다임을 섞을 때의 조건, 규칙 엔진이 실패하는 전형과 두 환경을 잇는 것이 결국 유비쿼터스 언어라는 판정, 비객체 요소를 섞는 네 가지 어림법, 그리고 표현력 없는 구현은 패러다임 추가의 이득을 상쇄한다는 조항, 그리고 규칙 엔진이 16장의 정책 층으로 들어올 때 두 구현 기술에 같은 모델을 쓰라는 같은 조건이 되풀이되는 자리
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 모델링 패러다임

- [모델 주도 설계는 객체를 요구하지 않는다](#모델-주도-설계는-객체를-요구하지-않는다)
- [객체 패러다임이 지배하는 이유](#객체-패러다임이-지배하는-이유)
- [미성숙한 패러다임에 걸었을 때](#미성숙한-패러다임에-걸었을-때)
- [객체로 자연스럽지 않은 도메인](#객체로-자연스럽지-않은-도메인)
- [패러다임을 섞을 때의 조건](#패러다임을-섞을-때의-조건)
- [규칙 엔진이 실패하는 전형](#규칙-엔진이-실패하는-전형)
- [네 가지 어림법](#네-가지-어림법)
- [표현력이 조건이다](#표현력이-조건이다)
- [규칙 엔진이 정책 층으로 들어올 때](#규칙-엔진이-정책-층으로-들어올-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델 주도 설계가 객체 지향을 전제하는가, 그리고 다른 패러다임을 섞을 때
모델이 깨지지 않으려면 무엇이 필요한가.**

## 모델 주도 설계는 객체를 요구하지 않는다

- 5장의 네 패턴을 마치며 저자가 범위를 좁힌다 — **이 장의 네 패턴은 객체 모델을 위한 구성
  단위를 제공한다. 그러나 모델 주도 설계가 반드시 모든 것을 객체의 거푸집에 밀어 넣는다는
  뜻은 아니다. 규칙 엔진 같은 도구가 지원하는 다른 모델 패러다임도 있다**
  (5장, p.116).[^evans2003]
- 그리고 그 도구들의 지위가 정해진다 — **프로젝트는 그것들 사이에서 실용적인 절충을 해야
  한다. 이 다른 도구와 기법은 모델 주도 설계라는 목적에 이르는 수단이지 그것의 대안이
  아니다** (5장, p.116).[^evans2003]
- 요구 사항은 도구가 아니라 일치다 — **모델 주도 설계는 적용되는 특정 모델링 패러다임과
  조율된 구현 기술을 요구한다** (5장 §"Modeling Paradigms", p.116).[^evans2003]
  전문은 [모델 주도 설계](../concepts/model-driven-design.md)에 있다.

## 객체 패러다임이 지배하는 이유

- 현황 진술 — **여러 패러다임이 실험되었으나 실제로 널리 쓰인 것은 몇 안 된다. 현재 지배적인
  패러다임은 객체 지향 설계이며, 요즘 복잡한 프로젝트 대부분이 객체를 쓰려고 출발한다**
  (5장, p.116).[^evans2003]
- 이유가 세 갈래로 분류된다 — **일부 요인은 객체에 내재적이고, 일부는 정황적이며, 다른 일부는
  널리 쓰인다는 사실 자체에서 오는 이점에서 파생된다** (5장, p.116).[^evans2003]
- **내재적 이유는 균형이다** (5장 §"Why the Object Paradigm Predominates",
  pp.116–117):[^evans2003]
  - **객체 모델링은 단순함과 정교함의 좋은 균형을 이룬다.**
  - 그 균형이 왜 요건인지가 이어진다 — **모델링 패러다임이 너무 난해하면 충분한 수의
    개발자가 그것을 익히지 못하고 잘못 쓸 것이다. 팀의 비기술 구성원이 그 패러다임의 기초조차
    파악하지 못하면 그들은 모델을 이해하지 못할 것이고 유비쿼터스 언어를 잃게 될 것이다.**
  - **객체 지향 설계의 기본은 대부분의 사람에게 자연스럽게 오는 듯하다. 어떤 개발자는
    모델링의 미묘함을 놓치지만, 비기술자조차 객체 모델의 다이어그램을 따라갈 수 있다.**
  - 그리고 단순함이 표현력을 깎지 않았다 — **객체 모델링이라는 개념이 단순한데도 중요한
    도메인 지식을 담기에 충분히 풍부함이 입증되었다. 그리고 처음부터 모델을 소프트웨어로
    표현할 수 있게 해 주는 개발 도구의 지원을 받았다.**
  - **첫째 이유가 [유비쿼터스 언어](ubiquitous-language.md)에 걸린다는 점이 중요하다.**
    패러다임 선택의 첫 기준이 성능이나 표현력이 아니라 **비기술자가 모델을 이해할 수
    있는가**다.
- **정황적 이유는 성숙도다** (5장, p.117):[^evans2003]
  - **성숙한 기반 구조와 도구 지원이 없으면 프로젝트가 기술 연구 개발로 샛길을 타 애플리케이션
    개발에서 자원을 지연시키고 돌려쓰며 기술 위험을 들인다.**
  - **어떤 기술은 다른 것과 잘 어울리지 않고 업계 표준 해법과 통합이 불가능할 수 있어, 팀이
    흔한 유틸리티를 다시 발명하게 만든다.**
  - 객체는 그 문제를 이미 지났다 — **그러나 여러 해에 걸쳐 이 문제들 상당수가 객체에 대해
    풀렸거나 널리 채택되면서 무의미해졌다. (이제는 다른 접근이 주류 객체 기술과 통합해야 할
    차례다.)**
- **셋째 이유가 사람이다** (5장, p.117):[^evans2003]
  - **똑같이 중요한 것이 개발자 공동체와 설계 문화 자체의 성숙이다.**
  - **참신한 패러다임을 채택한 프로젝트는 그 기술에 전문성이 있거나 선택한 패러다임에서
    효과적인 모델을 만들어 본 경험이 있는 개발자를 찾지 못할 수 있다.**
  - **그 패러다임과 기술을 최대한 활용하는 패턴이 아직 굳지 않았기 때문에, 합리적인 시간
    안에 개발자를 교육하는 것이 실현 가능하지 않을 수 있다.**

## 미성숙한 패러다임에 걸었을 때

1990년대 초 저자가 참여한 프로젝트의 사례다. 대규모 객체 지향 데이터베이스를 포함해 여러
첨단 기술에 걸었고, **당시 그 기술이 지원한 가장 큰 데이터베이스를 배치하고 있다고 방문자에게
자랑스럽게 말하던** 상태였다 (5장, p.118).[^evans2003]

- 실패가 드러난 방식 — **그러나 우리가 테스트 데이터로 데이터베이스 용량의 상당 부분을
  잠식하기 시작했다는 자각이 서서히 밀려왔다. 실제 데이터베이스는 수십 배 클 것이었다.
  실제 트랜잭션 양은 수십 배 높을 것이었다** (5장, p.118).[^evans2003]
- 해결은 사람을 사 오는 것이었다 — **다행히 우리를 그 문제에서 빼낼 기술을 가진 세계에서 몇
  안 되는 사람 중 하나를 팀에 데려올 수 있었다. 그는 값을 불렀고 우리는 지불했다**
  (5장, p.118).[^evans2003]
- **원인이 셋으로 진단된다** (5장, p.118):[^evans2003]
  - **데이터베이스와 함께 제공된 기성 기반 구조가 우리 필요만큼 확장되지 않았다.**
  - **잘게 쪼개진 객체의 저장이 우리가 깨달았던 것보다 훨씬 비싸다는 것이 드러났다.**
  - **객체 모델의 일부가 상호 의존의 엉킴을 가지고 있어, 비교적 적은 수의 동시
    트랜잭션에서도 경합이 문제가 되었다.**
- **그리고 이 사례가 애그리게이트 사고의 기원으로 명시된다** (5장, p.118):[^evans2003]

> All of us deepened our thinking about the importance of limiting the web of relationships in
> a model, and we began applying this new understanding to making better models with more
> decoupling between closely interrelated aggregates.

  - **이 한 줄이 이 장의 §Associations와 6장의 애그리게이트를 잇는다.** 연관을 제약하라는
    조항([도메인 연관](../concepts/domain-associations.md))과 군집에 경계를 그으라는 패턴
    ([애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md))의 근거가
    설계 미학이 아니라 **성능 실패의 사후 분석**이었다는 기록이다.
- 대가가 계상된다 — **이 회복에 여러 달을 잃었고, 그것은 앞서 실패한 경로를 가느라 쓴 달들에
  더해진 것이었다. 그리고 이것이 선택한 기술의 미성숙과 그에 딸린 학습 곡선에 대한 우리
  자신의 경험 부족에서 온 팀의 첫 좌절도 아니었다** (5장, p.118).[^evans2003]
- 뒷이야기가 냉정하다 — **슬프게도 이 프로젝트는 결국 후퇴해 꽤 보수적이 되었다. 오늘날까지
  그들은 그 이색적인 기술을 쓰지만, 아마 그것으로 실제 이득을 보지 않을 조심스럽게 범위가
  정해진 애플리케이션에만 쓴다** (5장, p.118).[^evans2003]
- 10년 뒤의 판정 — **대부분의 프로젝트가 현재로서는 객체 지향 기술을 시스템의 핵으로 쓰는 것이
  현명하다. 그렇다고 객체 전용 시스템에 갇히지는 않을 것이다 — 객체가 업계의 주류가 되었으므로
  현재 쓰이는 거의 모든 다른 기술과 연결할 통합 도구를 구할 수 있기 때문이다**
  (5장, p.119).[^evans2003]

## 객체로 자연스럽지 않은 도메인

- 그러나 영구 제약은 아니다 — **그렇다고 사람들이 영원히 객체에만 스스로를 제한해야 한다는
  뜻은 아니다. 무리와 함께 가는 것은 어느 정도의 안전을 주지만 늘 갈 길인 것은 아니다**
  (5장, p.119).[^evans2003]
- 한계가 지목된다 (5장, p.119):[^evans2003]

> Object models address a large number of practical software problems, but there are domains
> that are not natural to model as discrete packets of encapsulated behavior. For example,
> domains that are intensely mathematical or that are dominated by global logical reasoning do
> not fit well into the object-oriented paradigm.

- 그리고 원리가 진술된다 — **도메인 모델이 객체 모델이어야 하는 것은 아니다. 예컨대 프롤로그로
  구현된 모델 주도 설계가 있으며, 그 모델은 논리 규칙과 사실로 이루어진다**
  (5장 §"Nonobjects in an Object World", p.119).[^evans2003]
- 패러다임과 모델의 관계가 순환적이다 — **모델 패러다임은 사람들이 도메인에 대해 생각하기
  좋아하는 특정 방식을 다루려고 구상되었다. 그러면 그 도메인의 모델은 그 패러다임에 의해
  모양 지어진다. 그 결과는 패러다임에 따르는 모델이고, 그래서 그 모델링 스타일을 지원하는
  도구에서 효과적으로 구현될 수 있다** (5장, pp.119–120).[^evans2003]

## 패러다임을 섞을 때의 조건

- 판단이 규모별로 갈린다 (5장, p.120):[^evans2003]
  - **한 패러다임에서 잘 돌아가는 도메인에 변칙적인 요소가 몇 개뿐이라면, 개발자는 그 밖에는
    일관된 모델 안의 어색한 객체 몇 개와 함께 살 수 있다.**
  - 반대 극단 — **문제 도메인의 더 큰 부분이 다른 특정 패러다임으로 더 자연스럽게 표현된다면,
    패러다임을 통째로 바꾸고 다른 구현 플랫폼을 고르는 것이 말이 될 수도 있다.**
  - **그러나 도메인의 주요 부분들이 서로 다른 패러다임에 속하는 것처럼 보일 때는, 각 부분을
    맞는 패러다임으로 모델링하고 구현을 지원하는 도구 집합을 섞어 쓰는 것이 지적으로
    매력적이다.**
- 결합의 정도가 방법을 정한다 — **상호 의존이 작을 때는 다른 패러다임의 하위 시스템이 캡슐화될
  수 있다. 객체가 그저 호출하기만 하면 되는 복잡한 수학 계산 같은 것이다. 다른 때는 측면들이
  더 얽혀 있다. 객체들의 상호작용이 어떤 수학적 관계에 달려 있을 때가 그렇다**
  (5장, p.120).[^evans2003]
- 이것이 업무 규칙 엔진과 워크플로 엔진 같은 비객체 구성 요소를 객체 시스템에 통합하는
  동기이고, **패러다임을 섞으면 개발자가 특정 개념을 가장 잘 맞는 스타일로 모델링할 수 있다**
  (5장, p.120).[^evans2003]
- **그리고 대가가 즉시 계상된다** (5장, p.120):[^evans2003]

> But making a coherent model that spans paradigms is hard, and making the supporting tools
> coexist is complicated. When developers can't clearly see a coherent model embodied in the
> software, MODEL-DRIVEN DESIGN can go out the window, even as this mixture increases the need
> for it.

  - **필요가 커지는 동시에 실현이 어려워진다는 구조가 이 절의 핵심이다.**

## 규칙 엔진이 실패하는 전형

- 왜 매력적인가 — **지식이 풍부한 도메인 모델은 아마 명시적인 규칙을 담고 있는데, 객체
  패러다임에는 규칙과 그 상호작용을 진술할 특정 의미론이 없다. 규칙은 객체로 모델링될 수 있고
  실제로 자주 성공적으로 그렇게 되지만, 객체 캡슐화는 시스템 전체를 가로지르는 전역 규칙을
  적용하기를 어색하게 만든다** (5장 §"Sticking with MODEL-DRIVEN DESIGN When Mixing
  Paradigms", pp.120–121).[^evans2003]
- 그래서 규칙 엔진이 **규칙을 정의하는 더 자연스럽고 선언적인 방법을 약속하며, 사실상 규칙
  패러다임을 객체 패러다임에 섞게 해 준다** (5장, p.121).[^evans2003]
- **그러나 결과가 다르다** (5장, p.121):[^evans2003]

> But people don't always get what they hope for out of rules engines. Some products just
> don't work very well. Some lack a seamless view that can show the relatedness of model
> concepts that run between the two implementation environments. One common outcome is an
> application fractured in two: a static data storage system using objects, and an ad hoc
> rules processing application that has lost almost all connection with the object model.

- 처방은 모델로 계속 생각하는 것이다 — **규칙을 다루면서도 모델의 관점에서 계속 생각하는 것이
  중요하다. 팀은 두 구현 패러다임 모두와 작동할 수 있는 단일 모델을 찾아야 한다. 이는 쉽지
  않지만 규칙 엔진이 표현력 있는 구현을 허용한다면 가능해야 한다** (5장, p.121).[^evans2003]
- 실패했을 때의 모습이 명시된다 — **그렇지 않으면 데이터와 규칙이 이어지지 않게 된다. 엔진
  안의 규칙은 도메인 모델의 개념적 규칙이라기보다 작은 프로그램에 가까워진다. 규칙과 객체
  사이에 팽팽하고 명료한 관계가 있으면 두 조각의 의미가 모두 보전된다** (5장,
  p.121).[^evans2003]
- **이음매 없는 환경이 없을 때 남는 수단이 하나다** (5장, p.121):[^evans2003]

> The most effective tool for holding the parts together is a robust UBIQUITOUS LANGUAGE that
> underlies the whole heterogeneous model. Consistently applying names in the two environments
> and exercising those names in the UBIQUITOUS LANGUAGE can help bridge the gap.

  - **이것이 이 절의 결론이자 [유비쿼터스 언어](ubiquitous-language.md)의 가장 강한 용례다** —
    기술적 연결이 아예 없는 두 실행 환경을 **이름의 일관성만으로** 잇는다.
- 저자가 범위를 스스로 제한한다 — **이것은 책 한 권을 받을 만한 주제다. 이 절의 목표는 그저
  모델 주도 설계를 포기할 필요가 없다는 것, 그리고 그것을 지킬 만한 값이 있다는 것을 보이는
  데 있다** (5장, p.121).[^evans2003]

## 네 가지 어림법

**주로 객체 지향인 시스템에 비객체 요소를 섞는 네 가지 어림법이다** (5장,
p.122):[^evans2003]

> - *Don't fight the implementation paradigm.* There's always another way to think about a
>   domain. Find model concepts that fit the paradigm.
> - *Lean on the ubiquitous language.* Even when there is no rigorous connection between
>   tools, very consistent use of language can keep parts of the design from diverging.
> - *Don't get hung up on UML.* Sometimes the fixation on a tool, such as UML diagramming,
>   leads people to distort the model to make it fit what can easily be drawn.
> - *Be skeptical.* Is the tool really pulling its weight? Just because you have some rules,
>   that doesn't necessarily mean you need the overhead of a rules engine.

- 셋째의 근거가 이어진다 — **예컨대 UML에도 제약을 표상하는 기능이 있지만 늘 충분하지는
  않다. 다른 스타일의 그림(어쩌면 다른 패러다임에서 관례적인)이나 단순한 영어 서술이,
  객체의 특정 시야를 위해 의도된 그리기 스타일을 고통스럽게 적응시키는 것보다 낫다**
  (5장, p.122).[^evans2003]
- 넷째의 근거도 이어진다 — **규칙은 객체로 표현될 수 있다. 어쩌면 조금 덜 깔끔하게. 여러
  패러다임은 사정을 엄청나게 복잡하게 만든다** (5장, p.122).[^evans2003]
- 그리고 순서가 정해진다 — **혼합 패러다임의 부담을 지기 전에 지배적 패러다임 안의 선택지를
  소진해야 한다. 어떤 도메인 개념이 명백한 객체로 자신을 드러내지 않더라도, 그것들은 흔히 그
  패러다임 안에서 모델링될 수 있다** (5장, p.122).[^evans2003] 저자가 그 방법으로 9장을
  가리키고, 이 KB에서는 [암묵적 개념을 파내기](../concepts/digging-out-implicit-concepts.md)와
  [명세 패턴](specification-pattern.md)이 그 자리다.
- 관계형 데이터베이스가 특수 사례로 분류된다 — **관계형 패러다임은 패러다임 혼합의 특수
  사례다. 가장 흔한 비객체 기술인 관계형 데이터베이스는 다른 구성 요소보다 객체 모델과 더
  밀접하게 관계되는데, 그것이 객체 자체를 이루는 데이터의 영속 저장소로 작동하기 때문이다**
  (5장, p.122).[^evans2003]

## 표현력이 조건이다

- 이 절의 조항이자 이 장의 마지막 조항이다 (5장, p.121):[^evans2003]

> Although a MODEL-DRIVEN DESIGN does not have to be object oriented, it *does* depend on
> having an expressive implementation of the model constructs, be they objects, rules, or
> workflows. If the available tool does not facilitate that expressiveness, reconsider the
> choice of tools. An unexpressive implementation negates the advantage of the extra paradigm.

  - **도구 선택의 기준이 기능이 아니라 표현력으로 정해진다.** 규칙 엔진이 규칙을 더 잘
    실행해도, 그 규칙이 모델의 개념으로 읽히지 않으면 패러다임을 더한 이득이 상쇄된다.
  - 같은 잣대를 [선언적 설계](../concepts/declarative-design.md)가 다른 각도에서 쓴다 — 그쪽은
    선언적 스타일의 이득과 그것이 표현력을 잃을 때의 대가를 다룬다.

## 규칙 엔진이 정책 층으로 들어올 때

16장의 [책임 층](responsibility-layers.md)이 정책(Policy) 층을 규정하면서 **같은 조건을 대규모
구조의 층위에서 되풀이한다.**

- 관찰 — **정책 층은 다른 층과 같은 언어로 쓸 수도 있지만 때로는 규칙 엔진으로 구현된다. 그것이
  반드시 별개의 경계 컨텍스트를 만들지는 않는다** (16장, pp.462–463).[^evans2003]
- 그리고 조건이 붙는다 (16장, p.463):[^evans2003]

> In fact, the difficulty of coordinating such different implementation technologies can be eased
> by fastidiously using the same model across both. When rules are written based on a different
> model than the objects they apply to, either the complexity goes way up or the objects get
> dumbed down to keep things manageable.

  - 위 [패러다임을 섞을 때의 조건](#패러다임을-섞을-때의-조건)과 같은 요구다. 다만 여기서는
    **실패의 결과가 둘로 구체화된다** — 복잡도가 치솟거나, 다룰 만하게 만들려고 객체가
    멍청해지거나. 뒤의 것이 위 [규칙 엔진이 실패하는 전형](#규칙-엔진이-실패하는-전형)이 적는
    결말과 같다.
- 정책 층이 다른 층과 맺는 관계의 설계도 **미묘하다**고 적힌다 — **규칙과 목표는 대체로
  수동적이지만 다른 층의 행동을 제약한다. 때로는 정책이 하위 메서드에 인자로 넘어가고, 때로는
  전략(STRATEGY) 패턴이 적용된다** (16장, p.462).[^evans2003]
- 아래층에서 위층으로 예외를 알리는 문제도 같은 장이 다룬다 — 운영 층은 위층을 모르므로
  **양방향 의존을 만들지 않으면서** 알려야 하고, 전형적인 답이 이벤트 기제다 (16장,
  p.480).[^evans2003] 전문은 [대규모 구조](../concepts/large-scale-structure.md)에 있다.

## 이어지는 페이지

- [모델 주도 설계](../concepts/model-driven-design.md) — 이 절이 조건을 다는 상위 조항
- [유비쿼터스 언어](ubiquitous-language.md) — 패러다임을 가로질러 모델을 잇는 유일한 수단
- [도메인 연관](../concepts/domain-associations.md) — 관계의 그물을 제한하라는 조항
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 그 제한이
  패턴이 된 자리
- [암묵적 개념을 파내기](../concepts/digging-out-implicit-concepts.md) — 패러다임을 바꾸기 전에 소진할 선택지
- [선언적 설계](../concepts/declarative-design.md) — 규칙을 선언적으로 쓰되 모델 안에 두는 길
- [책임 층](responsibility-layers.md) — 규칙이 한 층으로 승격되는 자리
- [지식 수준](../concepts/knowledge-level.md) — 규칙을 모델 위의 별도 객체 집합으로 올리는 구조
- [도메인 특화 언어](../concepts/domain-languages.md) — 같은 저자가 별도 언어를 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §"Choosing Appropriate Layers"의 정책 층
    (pp.462–463) · §"How Restrictive Should a Structure Be?"(p.480) ·
    5장 "A Model Expressed in Software" §Modeling Paradigms
    (pp.116–122) — 도입(p.116) · §"Why the Object Paradigm Predominates"(pp.116–119,
    객체 데이터베이스 사례 p.118 포함) · §"Nonobjects in an Object World"(pp.119–120) ·
    §"Sticking with MODEL-DRIVEN DESIGN When Mixing Paradigms"(pp.120–122) ·
    네 어림법과 관계형 패러다임 단락(p.122). 장을 닫는 단락(p.116)도 여기에 실었다.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. 네 어림법 직인용은 원문의 이탤릭 표제를 유지하고 각 항목의
    뒤따르는 부연은 잘라 산문으로 옮겼다 — 보탠 말은 없다. 이 소스에서 온 코드 펜스는
    이 페이지에 없다 — 이 절에 코드 목록이 없다.

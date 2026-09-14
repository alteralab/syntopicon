---
type: concept
title: 설계 패턴을 도메인 패턴으로 읽기
description: 기술적 설계 패턴 중 어떤 것이 도메인 패턴이기도 한가를 가르는 기준 — 카탈로그 저자들이 스스로 그은 추상 수준의 경계, 같은 패턴을 코드의 기술적 설계와 모델의 개념적 패턴이라는 두 층위로 동시에 보라는 요구, 전략(정책)의 문제 서술과 처방과 강조점이 알고리즘 교체에서 개념 표현으로 옮겨 간다는 판정, 경로 탐색 정책 사례에서 조건문이 사라지고 업무 규칙 한 문장이 남는 과정, 설계 패턴의 결과가 그대로 따라온다는 것과 상태 없는 전략 객체의 공유, 컴포지트의 문제 서술과 처방과 구조만이 아니라 연산까지 밀어붙이라는 요구, 경로로 이루어진 경로 사례와 필요해지기 전에는 쓰지 않았다는 기록, 그리고 플라이웨이트가 왜 도메인 패턴이 아닌가라는 반례가 정하는 유일한 요건
generated: { by: "claude-opus-5", at: "2026-09-14T11:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 설계 패턴을 도메인 패턴으로 읽기

- [설계 패턴과 도메인 패턴의 차이를 묻는다](#설계-패턴과-도메인-패턴의-차이를-묻는다)
- [두 층위로 동시에 본다](#두-층위로-동시에-본다)
- [전략 또는 정책](#전략-또는-정책)
- [강조점이 옮겨 간다](#강조점이-옮겨-간다)
- [사례 — 경로 탐색 정책](#사례--경로-탐색-정책)
- [설계 패턴의 결과가 그대로 따라온다](#설계-패턴의-결과가-그대로-따라온다)
- [컴포지트](#컴포지트)
- [구조에서 멈추지 말고 연산까지 밀어라](#구조에서-멈추지-말고-연산까지-밀어라)
- [사례 — 경로로 이루어진 경로](#사례--경로로-이루어진-경로)
- [필요해지기 전에는 쓰지 않았다](#필요해지기-전에는-쓰지-않았다)
- [왜 플라이웨이트는 아닌가](#왜-플라이웨이트는-아닌가)
- [카탈로그는 만들지 않는다](#카탈로그는-만들지-않는다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **기술적 동기로 쓰인 설계 패턴이 언제 도메인 모델의 패턴이기도 한가, 그리고
그 판별을 무엇으로 하는가.**

## 설계 패턴과 도메인 패턴의 차이를 묻는다

- 출발 진단 — 이 책이 지금까지 다룬 패턴은 모델 주도 설계의 맥락에서 도메인 모델의 문제를
  풀기 위한 것이지만, **지금까지 출판된 패턴 대부분은 초점이 더 기술적이다** (12장,
  p.309).[^evans2003] 그래서 물음이 세워진다. 설계 패턴(design pattern)과 도메인 패턴
  (domain pattern)의 차이가 무엇인가.
- 답의 첫 재료로 카탈로그 저자들이 스스로 그은 경계를 인용한다. *Design Patterns*
  (Gamma 외)에서 (12장, p.309):[^evans2003]

> Point of view affects one's interpretation of what is and isn't a pattern. One person's
> pattern can be another person's primitive building block. For this book we have concentrated
> on patterns at a certain level of abstraction. Design patterns are not about designs such as
> linked lists and hash tables that can be encoded in classes and reused as is. Nor are they
> complex, domain-specific designs for an entire application or subsystem. The design patterns
> in this book are descriptions of communicating objects and classes that are customized to
> solve a general design problem in a particular context. [Gamma et al. 1995, p. 3]

- 그 위에 저자의 판정이 얹힌다 — **전부가 아니라 일부**가 도메인 패턴으로 쓰일 수 있고,
  그렇게 하려면 **강조의 전환**이 필요하다. 카탈로그는 여러 맥락에서 흔히 만나는 문제를
  풀어 온 설계 요소의 목록이고 그 동기와 패턴 자체가 **순전히 기술적인 말로** 제시되어
  있지만, 그 요소 중 일부는 **많은 도메인에서 떠오르는 일반 개념에 대응하기 때문에**
  도메인 모델링이라는 더 넓은 맥락에서 적용될 수 있다 (12장, pp.309–310).[^evans2003]

## 두 층위로 동시에 본다

- 요구가 한 문장이다 — 그런 패턴을 도메인 주도 설계에서 쓰려면 **패턴을 두 층위에서 동시에
  보아야 한다. 한 층위에서 그것은 코드 안의 기술적 설계 패턴이다. 다른 층위에서 그것은
  모델 안의 개념적 패턴이다** (12장, p.310).[^evans2003]
- 대상은 이 카탈로그에 한정되지 않는다. **그동안 제시된 다른 기술적 설계 패턴도 많고 그중
  일부는 도메인에서 떠오르는 깊은 개념에 대응한다. 그 작업을 끌어다 쓸 수 있으면 좋을
  것이다** (12장, p.310).[^evans2003]
- 이 장이 고른 표본이 둘이다. 컴포지트(COMPOSITE)와 전략(STRATEGY)이며, **고전 설계 패턴
  일부가 다르게 생각함으로써 도메인 문제에 적용될 수 있음을 보이는 것**이 표본의 역할이다
  (12장, p.310).[^evans2003]

## 전략 또는 정책

- 이 패턴의 이름은 둘이다. 전략(STRATEGY)이자 정책(POLICY)이다. 저자는 카탈로그의 요약을
  먼저 그대로 옮긴다 (12장, p.311):[^evans2003]

> Define a family of algorithms, encapsulate each one, and make them interchangeable.
> STRATEGY lets the algorithm vary independently from clients that use it.
> [Gamma et al. 1995]

  - **이 KB에 이 정의가 두 번 들어온 셈이다.** 파이썬 축의
    [일급 함수로 다시 쓰는 디자인 패턴](../concepts/design-patterns-with-first-class-functions.md)이
    같은 문장을 같은 카탈로그에서 인용한다. 그쪽의 물음은 "이 언어에서 이 패턴이 필요한가"이고
    이쪽의 물음은 "이 패턴이 모델의 개념이기도 한가"다.
- 그 위에 도메인 쪽 문제 서술이 새로 쓰인다 (12장, p.311):[^evans2003]

> Domain models contain processes that are not technically motivated but actually meaningful
> in the problem domain. When alternative processes must be provided, the complexity of
> choosing the appropriate process combines with the complexity of the multiple processes
> themselves, and things get out of hand.

- 증상의 서술 — 프로세스를 모델링하다 보면 그것을 하는 정당한 방법이 둘 이상임을 흔히 알게
  되고, 그 선택지를 서술하기 시작하면 **프로세스의 정의가 어설프고 복잡해진다.** 우리가
  고르는 실제 행동 대안들이 나머지 행동과 섞이면서 가려진다는 것이다 (12장,
  p.311).[^evans2003]
- 원하는 것은 분리다. 변이를 프로세스의 주 개념에서 떼어 내면 **주 프로세스와 선택지를 둘 다
  더 분명히 볼 수 있다**. 소프트웨어 설계 공동체에 이미 확립된 전략 패턴이 바로 이 문제를
  다루되 **초점이 기술적일 뿐**이고, 여기서는 그것이 모델의 개념으로 적용되어 그 모델의 코드
  구현에 반영된다 (12장, p.311).[^evans2003] 분리의 동기는 양쪽이 같다 —
  **프로세스의 변동이 큰 부분을 더 안정적인 부분에서 결합 해제할 필요**다.
- 처방 (12장, p.312):[^evans2003]

> Therefore:
> Factor the varying part of a process into a separate "strategy" object in the model. Factor
> apart a rule and the behavior it governs. Implement the rule or substitutable process
> following the STRATEGY design pattern. Multiple versions of the strategy object represent
> different ways the process can be done.

  - **"규칙과 그 규칙이 지배하는 행동을 갈라라"가 이 처방의 두 번째 문장이라는 점이
    중요하다.** 이것은 기술적 전략 패턴에 없는 요구이고, [명시적 제약](explicit-constraints.md)이
    말하는 규칙 끌어내기와 같은 동작이다.

## 강조점이 옮겨 간다

- 한 문장이 이 장 전체의 핵심을 담는다 (12장, p.312):[^evans2003]

> Whereas the conventional view of STRATEGY as a design pattern focuses on the ability to
> substitute different algorithms, its use as a domain pattern focuses on its ability to
> express a concept, usually a process or a policy rule.

  - **판별 기준이 이 문장에 있다.** 같은 코드 구조를 두고 무엇을 위해 그것을 골랐는가가 갈린다.
    알고리즘을 갈아 끼우려고 골랐으면 설계 패턴이고, 도메인의 개념 하나를 보이게 하려고
    골랐으면 도메인 패턴이다.
- 9장이 이 패턴을 **암묵적 프로세스를 명시하는 둘째 형태**로 미리 불러 둔 자리가 있다. 그
  예고의 전문은 [도메인 객체가 된 프로세스](processes-as-domain-objects.md)에 있고, 이 장이
  그 예고에 문제 서술과 처방을 채운다.

## 사례 — 경로 탐색 정책

- 설정 — 경로 명세(Route Specification)가 라우팅 서비스(Routing Service)에 넘어가고, 그
  서비스의 일은 명세를 만족하는 상세 여정(Itinerary)을 구성하는 것이다. 이 서비스는
  **가장 빠른 경로나 가장 싼 경로를 찾도록 조율할 수 있는 최적화 엔진**이다 (12장,
  p.312).[^evans2003]
- 출발 설계는 `findFastest`와 `findCheapest` 두 연산을 노출한다. 겉보기에는 괜찮지만 **라우팅
  코드를 자세히 보면 계산마다 조건문이 있어서 빠름과 쌈 사이의 결정이 사방에 나타난다.** 경로
  사이의 더 미묘한 선택을 위해 새 기준이 추가되면 더 큰 문제가 온다 (12장,
  p.312).[^evans2003]
- 고친 설계는 그 조율 매개변수를 전략으로 떼어 내 라우팅 서비스에 인자로 넘긴다. 연산은
  `find(Specification, LegMagnitudePolicy) : Itinerary` 하나가 되고, 구간 크기 정책
  (Leg Magnitude Policy)이 `length(Leg) : double`을 정의한다. 구상 정책 둘은 구간의 경과
  시간을 그대로 돌려주는 것(`return leg.elapsedTime();`)과 경과 시간에 항차의 일일 요율을
  곱하는 것이다 (12장, p.313).[^evans2003]
  - **이 두 줄은 클래스 다이어그램 안에 조판된 메서드 본문이라 산문에 코드 목록으로 있지
    않다.** 그래서 여기서도 인라인으로만 옮긴다.
- 얻는 것이 셋으로 계상된다 (12장, p.313).[^evans2003]
  - 라우팅 서비스가 **모든 요청을 같은 방식으로, 조건 없이** 처리한다. 낮은 크기의 구간
    수열을 찾는 일만 한다.
  - 애플리케이션의 다재다능함과 유연성 쪽에서, 적절한 정책을 설치하는 것만으로 서비스의 행동을
    통제하고 확장할 수 있다. 빠름과 쌈은 가장 뻔한 둘일 뿐이고, 속도와 비용을 절충하는 조합도,
    하청 대신 자사 운송 수단에 화물을 싣는 쪽으로 기우는 것 같은 전혀 다른 요인도 있을 수 있다.
  - **전략 없이도 그 변경들을 할 수는 있었겠지만 로직이 라우팅 서비스 내부를 휘감고 그
    인터페이스를 부풀렸을 것이다.** 결합 해제가 그것을 분명하고 시험하기 쉽게 만든다.
- 그리고 도메인 쪽 소득이 따로 계상된다 — 여정을 만들 때 한 구간을 다른 구간보다 고르는
  근거라는 **도메인의 근본적으로 중요한 규칙 하나가 이제 명시적이고 뚜렷하다**. 그것은 개별
  구간의 (파생될 수도 있는) 특정 속성 하나를 숫자 하나로 졸인 것이 라우팅의 근거라는 지식을
  전달한다 (12장, p.313).[^evans2003]
- 그 결과가 도메인의 말로 된 한 문장이다 (12장, p.314):[^evans2003]

> The **Routing Service** chooses an **Itinerary** with a minimum total magnitude of the
> **Legs** based on the chosen STRATEGY.

  - **설계의 산출물이 문장이라는 점이 이 사례의 요지다.** 같은 심급을
    [유비쿼터스 언어](ubiquitous-language.md)가 쓴다.
- 저자가 단서를 하나 단다. 이 논의는 라우팅 서비스가 여정을 찾으며 구간을 실제로 평가한다는
  뜻인데, **개념적으로는 단순하고 그럴듯한 원형 구현이 될 수 있으나 아마도 받아들일 수 없게
  비효율적일 것**이라는 것이다. 같은 인터페이스에 전혀 다른 구현을 두는 이야기는 14장으로
  미뤄진다 (12장, p.314).[^evans2003]

## 설계 패턴의 결과가 그대로 따라온다

- 기술적 설계 패턴을 도메인 층에서 쓸 때 **추가 동기와 또 한 층의 의미를 더해야 한다**는
  것이 이 대목의 요구다. 전략이 실제 업무 전략이나 정책에 대응할 때 그 패턴은 **쓸모 있는
  구현 기법 이상의 것**이 된다 (12장, p.314).[^evans2003]
- **그렇다고 설계 패턴 쪽 논의가 버려지지는 않는다** (12장, p.314).[^evans2003]
  - 카탈로그가 지적한 결과 하나는 **클라이언트가 서로 다른 전략을 알고 있어야 한다**는 것인데,
    그것은 모델링의 관심사이기도 하다.
  - 순전히 구현 쪽 관심사 하나는 **전략이 애플리케이션의 객체 수를 늘릴 수 있다**는 것이다.
    그것이 문제라면 **전략을 맥락들이 공유할 수 있는 상태 없는 객체로 구현해 부담을 줄일 수
    있다.**
  - 판정 — **설계 패턴의 폭넓은 구현 논의가 전부 여기에 적용된다. 우리가 여전히 전략을 쓰고
    있기 때문이다. 동기가 부분적으로 다르고 그것이 몇몇 선택에 영향을 주겠지만, 설계 패턴에
    박혀 있는 경험은 우리가 마음대로 쓸 수 있다.**
  - **여기에 이 KB의 다른 소스와 겹치는 자리가 있다.** 상태 없는 전략 객체를 공유해 부담을
    줄이라는 권고는 파이썬 축에서 비판의 대상이다. 그쪽은 **전략 패턴의 단점인 런타임 비용을
    이기려고 저자들이 또 하나의 패턴을 권한다**고 적는다. 다만 두 진술이 겨루지 않는다 —
    그쪽의 반론은 **일급 함수가 있는 언어라면 그 비용을 애초에 치르지 않는다**는 것이고,
    Evans의 문장은 2003년 자바의 객체 모델 안에서 쓰였다. 대조의 전문은
    [일급 함수로 다시 쓰는 디자인 패턴](../concepts/design-patterns-with-first-class-functions.md)과
    [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md)에 있다.

## 컴포지트

- 요약은 여기서도 카탈로그의 것을 그대로 옮긴다 (12장, p.315):[^evans2003]

> Compose objects into tree structures to represent part-whole hierarchies. COMPOSITE lets
> clients treat individual objects and compositions of objects uniformly.
> [Gamma et al. 1995]

- 도메인 쪽 관찰이 앞에 붙는다 — 복잡한 도메인을 모델링하다 보면 부분으로 이루어지고 그
  부분이 다시 부분으로 이루어지며 때로는 임의의 깊이까지 중첩되는 중요한 객체를 자주 만난다.
  **어떤 도메인에서는 각 층위가 개념적으로 구별되지만, 다른 경우에는 부분이 전체와 같은
  종류의 것이되 더 작을 뿐이라는 의미가 있다** (12장, p.315).[^evans2003]
- 문제 서술 (12장, p.315):[^evans2003]

> When the relatedness of nested containers is not reflected in the model, common behavior has
> to be duplicated at each level of the hierarchy, and nesting is rigid (for example,
> containers can't usually contain other containers at their own level, and the number of
> levels is fixed). Clients must deal with different levels of the hierarchy through different
> interfaces, even though there may be no conceptual difference they care about. Recursion
> through the hierarchy to produce aggregated information is very complicated.

- **그리고 적용 전에 물어야 할 것이 명시된다.** 도메인에 어떤 설계 패턴을 적용할 때 **첫째
  관심사는 그 패턴의 발상이 도메인 개념에 정말로 잘 맞는가여야 한다**. 연관된 객체들을
  재귀적으로 훑는 것이 편리할 수는 있으나, **진짜 전체와 부분의 위계인가? 모든 부분이 정말로
  같은 개념적 타입이 되는 추상을 찾아냈는가?** (12장, pp.315–316).[^evans2003]
  - 찾아냈다면 컴포지트가 모델의 그 측면을 더 분명하게 만들면서 **설계 패턴 쪽에서 신중히
    숙고된 설계와 구현 고려 사항에 접속하게 해 준다** (12장, p.316).[^evans2003]
  - **두 물음이 이 페이지에서 가장 실용적인 도구다.** 편리함과 개념적 일치를 가르는 검문소다.
- 처방 (12장, p.316):[^evans2003]

> Therefore:
> Define an abstract type that encompasses all members of the COMPOSITE. Methods that return
> information are implemented on containers to return aggregated information about their
> contents. "Leaf" nodes implement those methods based on their own values. Clients deal with
> the abstract type and have no need to distinguish leaves from containers.

## 구조에서 멈추지 말고 연산까지 밀어라

- 경고 하나가 붙는다 — **이것은 구조 층위에서는 비교적 뻔한 패턴이지만 설계자들은 흔히
  이 패턴의 연산 층위를 살까지 채우도록 자신을 밀어붙이지 않는다** (12장,
  p.316).[^evans2003]
- 채웠을 때 얻는 것 — 컴포지트는 **모든 구조 층위에서 같은 행동을 제공하고, 작은 부분에도 큰
  부분에도 그 구성을 투명하게 반영하는 뜻있는 질문을 던질 수 있다. 그 엄정한 대칭이 이 패턴의
  힘의 열쇠다** (12장, p.316).[^evans2003]
  - **이 조항이 [연산의 닫힘](closure-of-operations.md)과 같은 방향을 가리킨다.** 타입이
    자기 자신에 대해 닫혀 있을 때 층위를 가로지르는 연산이 성립한다.

## 사례 — 경로로 이루어진 경로

- 도메인은 화물 운송이다. 완전한 운송 경로는 복잡하다 — 컨테이너가 철도 기지까지 트럭으로
  가고, 항구로 운반되고, 배로 다른 항구까지 운송되고, 다른 배로 옮겨질 수도 있고, 반대편에서
  다시 육상 운송된다 (12장, p.316).[^evans2003]
- 첫 모델은 경로(Route)를 구간(Leg)의 순서 있는 임의 길이 열로 본다. 개발팀은 예약 요청에서
  경로 객체를 만들고 구간을 화물의 단계별 취급 운영 계획으로 처리할 수 있었다 (12장,
  p.317).[^evans2003]
- **그러다 발견이 온다.** 개발자들은 경로를 구별 없는 구간의 열로 생각해 왔지만 **도메인
  전문가는 경로를 논리적 구간 다섯의 수열로 본다.** 그 하위 경로들은 서로 다른 사람이 서로
  다른 때에 계획할 수 있어서 구별되는 것으로 봐야 하고, 자세히 보니 "문 구간(door legs)"은
  다른 구간과 아주 달라서 **현지에서 고용한 트럭이나 고객 자가 운송**이 관여하는 반면 철도와
  선박 운송은 정교하게 일정이 잡힌다 (12장, pp.317–318).[^evans2003]
- 그 구별을 전부 반영한 모델은 복잡해진다. **구조 자체는 그리 나쁘지 않지만 운영 계획 처리의
  균일함이 사라져서 코드가, 심지어 행동에 대한 서술조차 훨씬 복잡해진다.** 경로를 훑는 일이
  서로 다른 타입의 컬렉션 여럿을 거치게 된다 (12장, p.318).[^evans2003]
- 여기서 컴포지트가 들어온다. 어떤 클라이언트에게는 **이 구성물의 서로 다른 층위를 균일하게,
  경로로 이루어진 경로로 다루는 것이 좋을 것**이고 **개념적으로 이 관점이 온당하다.**
  근거가 한 문장이다 — **경로의 모든 층위는 컨테이너가 한 지점에서 다른 지점으로 이동하는
  것이며, 개별 구간에 이르기까지 그렇다** (12장, p.318).[^evans2003]
- **대가도 함께 적힌다.** 정적 클래스 다이어그램은 문 구간과 다른 세그먼트가 어떻게 맞물리는지를
  이전만큼 말해 주지 않는다. 그러나 **모델은 정적 클래스 다이어그램 이상**이므로 조립 정보는
  다른 다이어그램과 이제 훨씬 단순해진 코드가 전달한다. 이 모델은 **이 온갖 종류의 "경로"가
  가진 깊은 관련성을 붙잡고**, 운영 계획 생성과 다른 경로 훑기 연산이 다시 단순해진다 (12장,
  p.318).[^evans2003]
  - **"모델은 정적 클래스 다이어그램 이상"이라는 단서가 이 대목의 중요한 부분이다.** 도해
    하나가 잃은 정보를 다른 표현이 갚는다는 판정이고, 같은 판정이
    [유비쿼터스 언어](ubiquitous-language.md)의 문서와 도해 절에 있다.

## 필요해지기 전에는 쓰지 않았다

- 얻는 선택지가 열거된다 — 다른 경로들로 이루어진 경로를 끝과 끝으로 이어 붙이면 **상세도가
  다른 경로 구현을 가질 수 있고, 경로의 끝을 잘라 내고 새 끝을 이어 붙일 수 있고, 임의 깊이의
  중첩을 가질 수 있고, 쓸모 있을 법한 온갖 선택지를 활용할 수 있다** (12장,
  p.320).[^evans2003]
- **그리고 곧바로 그 열거를 스스로 깎는다** (12장, p.320).[^evans2003]

> Of course, we don't yet need such options. And before we needed those route segments and
> distinct door legs, we were doing just fine without COMPOSITE. A design pattern should be
> applied only when it is needed.

  - **이 마지막 문장이 이 페이지가 남기는 가장 짧은 조항이다.** 이 KB에서 같은 경고를 다른
    소스가 더 길게 다는 자리가 [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md)의
    과잉 적용 판정이다. 두 소스가 같은 방향에 서 있다.

## 왜 플라이웨이트는 아닌가

- 저자가 반례를 자기 책에서 든다. 5장이 플라이웨이트(FLYWEIGHT)를 언급했으므로 그것도 도메인
  모델에 적용되는 패턴의 예라고 짐작했을 수 있으나, **사실 플라이웨이트는 도메인 모델에
  대응이 없는 설계 패턴의 좋은 예다** (12장, p.320).[^evans2003]
- 근거 — 한정된 값 객체 집합이 여러 번 쓰일 때(집 도면의 전기 콘센트가 그 예다) 그것을
  플라이웨이트로 구현하는 것이 말이 될 수 있다. **이것은 값 객체에는 열려 있고 엔티티에는
  열려 있지 않은 구현 선택지다** (12장, p.320).[^evans2003] 그 구분의 전문은
  [값 객체의 설계](value-object-design.md)에 있다.
- 대비 — 컴포지트에서는 **개념적 객체가 다른 개념적 객체로 구성된다. 그 경우 패턴이 모델과
  구현 양쪽에 적용되며, 그것이 도메인 패턴의 본질적 특징이다** (12장, p.320).[^evans2003]
  - **판별 기준이 여기서 완성된다.** 모델에는 아무것도 말하지 않고 구현에만 적용되면 설계
    패턴이고, 모델과 구현 양쪽에 적용되면 도메인 패턴이다.

## 카탈로그는 만들지 않는다

- 저자가 스스로 범위를 닫는다 — **도메인 패턴으로 쓰일 수 있는 설계 패턴의 목록을 엮으려 하지
  않겠다. 인터프리터를 도메인 패턴으로 쓰는 예를 떠올릴 수는 없지만, 어떤 도메인의 어떤 구상도
  거기 맞지 않으리라고 말할 준비는 되어 있지 않다** (12장, p.320).[^evans2003]
- 남는 것은 요건 하나다 (12장, p.320):[^evans2003]

> The only requirement is that the pattern should say something about the conceptual domain,
> not just be a technical solution to a technical problem.

  - **이 한 줄이 이 페이지의 조항이다.** 목록이 아니라 시험이 답이고, 그 시험은 이름이 아니라
    적용하는 사람이 통과시킨다.

## 이어지는 페이지

- [도메인 객체가 된 프로세스](processes-as-domain-objects.md) — 9장이 전략을 암묵적 프로세스를
  명시하는 둘째 형태로 미리 부르는 자리
- [분석 패턴을 모델에 들이기](analysis-patterns-in-the-model.md) — 빌려 쓸 것이 출판된 모델
  조각일 때의 형제 장
- [모델 리팩터링의 과정](model-refactoring-process.md) — 설계 패턴이 이 과정의 재료로 다시
  호명되는 자리
- [명시적 제약](explicit-constraints.md) — 규칙을 그것이 지배하는 행동에서 떼어 내는 같은 동작
- [값 객체의 설계](value-object-design.md) — 플라이웨이트가 열려 있는 쪽
- [연산의 닫힘](closure-of-operations.md) — 컴포지트의 대칭이 기대는 성질
- [화물 운송 예제](cargo-shipping-example.md) — 같은 도메인의 앞선 단계
- [명세 패턴](specification-pattern.md) — 경로 명세가 라우팅 서비스에 넘어가는 구조
- [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md) — 이 패턴 형식 자체에 대한 다른
  소스들의 판정
- [일급 함수로 다시 쓰는 디자인 패턴](../concepts/design-patterns-with-first-class-functions.md) —
  같은 전략 정의를 언어 의존성의 각도에서 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 12장 "Relating Design Patterns to the Model" 전량(pp.309–320 —
    장 도입 pp.309–310 · §STRATEGY (A.K.A. POLICY) pp.311–312와 예제 "Route-Finding
    Policies" pp.312–314와 닫는 논의 p.314 · §COMPOSITE pp.315–316과 예제 "Shipment Routes
    Made of Routes" pp.316–320 · §"Why Not FLYWEIGHT?" p.320). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 도판 전부(Figure 12.1–12.9 — 전략과 컴포지트의 카탈로그 구조도 둘, 조건문이
    있는 서비스 인터페이스와 정책을 인자로 받는 인터페이스 둘, 구간으로 된 경로의 개념도,
    경로 클래스 다이어그램 세 판, 완전한 경로의 인스턴스 다이어그램)는 이미지라 딸린 판정
    산문만 옮겼다. **이 장에는 산문 코드 목록이 하나도 없다** — 구간 크기 정책의 메서드
    본문 두 줄은 Figure 12.2 안에 조판된 것이라 인라인으로만 옮겼고 펜스를 두지 않았다.
    카탈로그 인용문 안의 대괄호 서지 표기는 원문 그대로다. 저자가 대는 참고 문헌은
    Gamma et al. 1995다.

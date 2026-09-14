---
type: concept
title: 업무 로직 구현 패턴 고르기
description: 전술 설계가 무엇을 묻는 층위인지와 업무 로직을 구현하는 패턴들 사이의 선택 기준 — 전략이 무엇과 왜에 답했다면 전술은 어떻게에 답한다는 배치, 코드가 자기 경계 컨텍스트의 유비쿼터스 언어를 말하게 하는 것이 이 패턴들의 공통 목적이라는 규정, 로직의 복잡성과 자료 구조의 복잡성이라는 두 축으로 갈리는 세 패턴과 시간 차원을 더해 넷째가 서는 자리, 업무 로직 패턴이 정해지면 아키텍처 패턴도 따라 정해진다는 대응표와 CQRS만이 의무로 걸리는 자리, 그 선택을 시스템 전체에도 경계 컨텍스트 전체에도 걸지 말고 하위 도메인 단위의 세로 경계로 나누라는 범위 조항, 판정의 입력이 하위 도메인의 종류라는 대응과 핵심에는 단순 패턴을 쓰지 말라는 금지, 단순한 로직에 정교한 패턴을 쓰면 우발적 복잡성으로 해가 된다는 반대 방향의 금지, 그리고 상위 패턴이 하위 패턴을 대체하지 않고 층으로 겹친다는 판정, 그리고 10장이 그 판정 전부를 하나의 결정 트리로 묶는 자리 — 휴리스틱이 100퍼센트 옳도록 증명된 규칙이 아니라 어림법이라는 규정, 정교한 패턴부터 묻고 하나씩 떨어뜨리며 내려오는 물음 넷, 패턴 선택이 어긋나면 하위 도메인 분류를 다시 보라는 역방향 쓰임, 복잡한 로직과 단순한 로직을 가르는 두 신호와 그중 하나가 유비쿼터스 언어 자체라는 것, 저자 자신이 적는 아키텍처 대응 넷과 CQRS만이 예외라는 조항, 그리고 업무 로직 패턴이 테스트 전략까지 정한다는 셋째 칸 — 도메인 모델에는 피라미드, 액티브 레코드에는 다이아몬드, 트랜잭션 스크립트에는 역피라미드 — 과 이것이 규칙이 아니라 저자의 취향에 기반한 출발점이라는 단서, 그리고 한번 고른 패턴을 갈아타는 사다리 — 자료 작업이 버거워질 때 트랜잭션 스크립트에서 액티브 레코드로, 불일치와 중복이 늘 때 액티브 레코드에서 도메인 모델로 가는 네 걸음(값 객체 찾기·세터를 private으로 만들어 컴파일 오류로 상태 변경 지점을 드러내기·가장 작은 트랜잭션 경계로 애그리게이트 자르기·루트 정하기), 애그리게이트 경계가 제대로 선 뒤에야 이벤트 소싱으로 가는 순서, 그리고 13장이 더하는 두 단서 — 트랜잭션 스크립트나 액티브 레코드에서 이벤트 소싱 도메인 모델로 곧장 가지 말라는 금지와 도메인 모델 도입이 원자적 변경일 필요가 없다는 허용
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 업무 로직 구현 패턴 고르기

- [전술 설계가 묻는 것](#전술-설계가-묻는-것)
- [공통 목적 — 코드가 그 경계의 말을 하게 한다](#공통-목적--코드가-그-경계의-말을-하게-한다)
- [두 축으로 갈린다](#두-축으로-갈린다)
- [판정의 입력은 하위 도메인의 종류다](#판정의-입력은-하위-도메인의-종류다)
- [금지가 양쪽으로 걸린다](#금지가-양쪽으로-걸린다)
- [패턴들은 서로를 대체하지 않는다](#패턴들은-서로를-대체하지-않는다)
- [아키텍처 패턴은 업무 로직 패턴에 걸린다](#아키텍처-패턴은-업무-로직-패턴에-걸린다)
- [이 판정을 어느 범위에 거는가](#이-판정을-어느-범위에-거는가)
- [휴리스틱이라는 낱말](#휴리스틱이라는-낱말)
- [판정을 물음 넷으로 편다](#판정을-물음-넷으로-편다)
- [반대 방향으로도 읽는다 — 분류를 검증하는 쓰임](#반대-방향으로도-읽는다--분류를-검증하는-쓰임)
- [이 되검증을 요령으로 굳힌 자리 — 부록 A](#이-되검증을-요령으로-굳힌-자리--부록-a)
- [복잡한 로직과 단순한 로직을 가르는 어림법](#복잡한-로직과-단순한-로직을-가르는-어림법)
- [아키텍처 패턴도 물음 넷으로 편다](#아키텍처-패턴도-물음-넷으로-편다)
- [테스트 전략도 여기서 따라 나온다](#테스트-전략도-여기서-따라-나온다)
- [셋을 하나의 결정 트리로](#셋을-하나의-결정-트리로)
- [이것이 규칙이 아니라는 단서](#이것이-규칙이-아니라는-단서)
- [고른 다음에 갈아타는 길](#고른-다음에-갈아타는-길)
- [트랜잭션 스크립트에서 액티브 레코드로](#트랜잭션-스크립트에서-액티브-레코드로)
- [액티브 레코드에서 도메인 모델로](#액티브-레코드에서-도메인-모델로)
- [도메인 모델에서 이벤트 소싱 도메인 모델로](#도메인-모델에서-이벤트-소싱-도메인-모델로)
- [13장이 이 경로에 거는 두 단서](#13장이-이-경로에-거는-두-단서)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 로직을 어떤 모양으로 구현할지를 무엇을 보고 정하는가.**

## 전술 설계가 묻는 것

- [khononov2021](../sources/khononov2021.md)이 II부를 열면서 앞부의 일과 이 부의 일을 가른다 —
  I부에서는 소프트웨어의 **"무엇"과 "왜"**를 다뤘고 업무 도메인을 분석해 하위 도메인과 그
  전략적 값을 식별하고 그 지식을 경계 컨텍스트의 설계로 바꾸는 법을 배웠다
  (II부 도입, p.61).[^khononov2021]
- **이 부에서는 전략에서 전술로 돌아선다** (II부 도입, p.61):[^khononov2021]

> In this part of the book, we will turn from strategy to tactics: the "how" of software
> design:

  - 이 이분법 자체의 규정과 원전 IV부와의 이름 겹침은
    [전략 설계](strategic-design.md)에 있다.
- 이 부가 담는 것 중 업무 로직 구현에 해당하는 것이 5장부터 7장이다
  (II부 도입, p.61):[^khononov2021]
  - **5장이 비교적 단순한 업무 로직을 감당하는 두 패턴을 소개한다** — 트랜잭션 스크립트와
    액티브 레코드다.
  - **6장이 더 까다로운 경우로 옮겨 가 도메인 모델 패턴을 제시한다** — **복잡한 업무 로직을
    구현하는 도메인 주도 설계의 방식**이다.
  - **7장에서는 시간의 차원을 모델링해 도메인 모델 패턴을 확장하는 법을 배운다.**
- 나머지 두 장은 다른 물음에 답한다 — 8장은 경계 컨텍스트의 아키텍처를 조직하는 방식들
  (계층 아키텍처, 포트와 어댑터, CQRS)을, 9장은 구성 요소 사이 상호작용을 조율하는 기술적
  관심사와 구현 전략을 다룬다 (II부 도입, pp.61–62).[^khononov2021]

## 공통 목적 — 코드가 그 경계의 말을 하게 한다

- 5장부터 7장의 패턴들에 공통 목적이 붙는다 — **코드가 자기 경계 컨텍스트의 유비쿼터스 언어를
  말할 수 있게 하는 업무 로직 구현 패턴들**이다 (II부 도입, p.61).[^khononov2021]
  - 그 요구의 정본은 [유비쿼터스 언어](ubiquitous-language.md)와
    [경계 컨텍스트](bounded-context.md)에 있다.
- **이 목적이 선택의 잣대가 아니라 전제라는 점에 주의한다.** 네 패턴 중 무엇을 골라도 코드는
  그 경계의 말을 해야 한다. 고르는 기준은 아래 두 축이다.

## 두 축으로 갈린다

이 판본이 5장과 6장에서 각 패턴의 "언제 쓰는가" 절에 흩어 놓은 판정을 모으면 축이 둘이다 —
**업무 로직의 복잡성**과 **자료 구조의 복잡성**이다.

- [트랜잭션 스크립트](transaction-script.md) — **업무 로직이 단순한 절차적 연산을 닮은 가장
  직선적인 문제 도메인**에 맞는다. 예가 ETL이다 (5장, p.68).[^khononov2021]
- [액티브 레코드](active-record.md) — **업무 로직은 단순한데 복잡한 자료 구조 위에서 작동할 때**
  쓴다. 두 패턴의 차이는 **액티브 레코드가 복잡한 자료 구조를 데이터베이스 스키마로 매핑하는
  복잡성을 다룬다**는 것뿐이다 (5장, pp.69·71).[^khononov2021]
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — **복잡한 업무 로직의 경우를 감당하기
  위한 것**이다. CRUD 인터페이스가 아니라 **복잡한 상태 전이, 업무 규칙, 그리고 항상 지켜져야
  하는 규칙인 불변식**을 다룬다 (6장, p.76).[^khononov2021]
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 넷째 자리가 7장이다. 위
  [전술 설계가 묻는 것](#전술-설계가-묻는-것)이 옮긴 대로 **시간의 차원을 모델링해 도메인 모델
  패턴을 확장한 것**이고 (II부 도입, p.61),[^khononov2021] 축 위의 자리는 셋째와 같다 —
  **업무 로직이 복잡하고 핵심 하위 도메인에 속하며 같은 전술 패턴(값 객체·애그리게이트·도메인
  이벤트)을 쓴다** (7장, p.99).[^khononov2021] 갈리는 것은 영속화 방식 하나다.
  - **그래서 이 넷째는 두 축이 아니라 셋째 축으로 갈린다** — 시스템의 데이터에 대한 깊은
    통찰이 필요한가다 (7장, p.115):[^khononov2021]

  > This pattern fits cases in which it's crucial to have deep insight into the system's data, whether
  > for analysis and optimization or because an audit log is required by law.

  - **5장과 6장이 패턴마다 두었던 `When to Use…` 절이 7장에는 없다.** 위 인용과 비용 셋의
    단서가 그 자리를 대신하고, 저자는 판정 규칙 자체를 10장으로 미룬다.
- 5장 맺음이 앞 둘을 한 문단씩으로 요약한다 (5장 §Conclusion, p.72):[^khononov2021]
  - **트랜잭션 스크립트** — 시스템의 연산을 단순하고 직선적인 절차적 스크립트로 조직한다.
    그 절차가 각 연산이 트랜잭션적이도록 보장한다. **업무 로직이 단순한 ETL 같은 연산을 닮은
    보조 하위 도메인에 잘 맞는다.**
  - **액티브 레코드** — 업무 로직은 단순하지만 복잡한 자료 구조 위에서 작동할 때 그 자료
    구조를 액티브 레코드로 구현할 수 있다. **액티브 레코드 객체는 단순한 CRUD 데이터 접근
    메서드를 제공하는 자료 구조다.**

## 판정의 입력은 하위 도메인의 종류다

**이 판본이 패턴 선택을 개인 취향이 아니라 앞부의 분류 결과에 묶는다.** 그 대응이 이 페이지가
모으는 값이다.

- **보조 하위 도메인** — 트랜잭션 스크립트가 **정의상 업무 로직이 단순하기 때문에** 자연히
  맞고, 액티브 레코드도 같은 자리에 온다 (5장, pp.69·71).[^khononov2021]
- **일반 하위 도메인** — 외부 시스템과의 통합에 어댑터로 쓰거나 외부 솔루션을 통합하는 데
  쓴다. 부패 방지 계층의 일부도 그 자리다 (5장, pp.69·71).[^khononov2021] 그 계층은
  [부패 방지 계층](../concepts/anticorruption-layer.md)에 있다.
- **핵심 하위 도메인** — 도메인 모델 쪽이다. 저자가 그 대응을 역방향으로 도출한다 —
  **도메인 모델 패턴은 업무 로직이 복잡한 하위 도메인에만 적용되므로, 그것이 핵심 하위 도메인,
  곧 소프트웨어의 심장이라고 가정해도 안전하다** (6장 §"Managing Complexity",
  p.95).[^khononov2021]
- 세 종류의 규정은 [하위 도메인의 세 종류](subdomain-types.md)에 있고, 핵심의 판정 기준은
  [핵심 도메인](../concepts/core-domain.md)에 있다.
  - **이 대응이 앞부의 분석을 실행 가능하게 만든다.** 하위 도메인을 분류하는 일이 문서 작업으로
    끝나지 않고 구현 패턴의 선택을 강제한다는 것이 이 판본의 짜임이다.

## 금지가 양쪽으로 걸린다

- **위로 가는 금지** — **트랜잭션 스크립트는 핵심 하위 도메인에 절대 쓰여서는 안 된다. 이 패턴은
  핵심 하위 도메인의 높은 업무 로직 복잡성을 감당하지 못하기 때문이다** (5장,
  p.69).[^khononov2021] 액티브 레코드는 본질적으로 트랜잭션 스크립트이므로 같은 금지가 걸린다.
- **아래로 가는 금지** — **단순한 업무 로직을 구현하는 데 더 정교한 패턴을 쓰는 것도 우발적
  복잡성(accidental complexity)을 들여 해가 된다** (5장, p.71).[^khononov2021]
  - **두 금지가 대칭이라는 것이 이 페이지의 요점이다.** 과소 설계와 과잉 설계가 같은 무게로
    적혀 있고, 그래서 "더 좋은 패턴"이라는 순위가 성립하지 않는다. 같은 대칭을 다른 층위에서
    적는 자리가 [스마트 UI 안티패턴](../concepts/smart-ui-antipattern.md)과
    [도메인 모델 패턴](../concepts/domain-model-pattern.md)의 "이 패턴이 필요 없는 경우"다.

## 패턴들은 서로를 대체하지 않는다

- 저자가 5장을 닫으면서 층위를 못 박는다 — **단순함에도 불구하고 트랜잭션 스크립트 패턴은
  소프트웨어 개발에서 어디에나 있다. 이 장과 다음 장들에서 논의할 모든 업무 로직 구현 패턴이
  어떤 식으로든 트랜잭션 스크립트 패턴에 기반한다** (5장, p.69).[^khononov2021]
- 6장이 그 주장을 회수한다 — 애그리게이트 위의 연산을 조율하는 애플리케이션 계층을 두고
  각주에 적는다 — **본질적으로 애플리케이션 계층의 연산이 트랜잭션 스크립트 패턴을 구현한다.
  그것은 연산을 원자적 트랜잭션으로 조율해야 한다** (6장, p.86, 각주 7).[^khononov2021]
- **그러므로 선택은 "무엇으로 갈아탈 것인가"가 아니라 "어디까지 쌓을 것인가"다.** 도메인 모델을
  골라도 트랜잭션 스크립트는 그 위의 층으로 남는다. 그 층의 전문은
  [서비스 레이어](../concepts/service-layer-pattern.md)에 있다.
- 액티브 레코드도 마찬가지다 — **액티브 레코드는 본질적으로 데이터베이스 접근을 최적화한
  트랜잭션 스크립트다** (5장, p.71).[^khononov2021] 셋이 계단이 아니라 겹이다.

## 아키텍처 패턴은 업무 로직 패턴에 걸린다

**8장이 이 판정을 한 층 위로 올린다.** 업무 로직을 무엇으로 구현할지가 정해지면 코드베이스를
어떻게 조직할지도 거기서 따라 나온다.

- 이 선택의 무게가 먼저 규정된다 (8장, p.118):[^khononov2021]

> Choosing the appropriate way to organize the codebase, or the correct architectural pattern, is
> crucial to support implementation of the business logic in the short term and alleviate maintenance
> in the long term.

- 저자가 드는 아키텍처 패턴은 셋이고, 각 패턴의 `When to Use…` 절과 장 맺음이 대응을 준다
  (8장, pp.124–125·128·133–135):[^khononov2021]

| 업무 로직 패턴 | 맞는 아키텍처 패턴 | 왜 |
|---|---|---|
| [트랜잭션 스크립트](transaction-script.md) | [계층 아키텍처](../concepts/layered-architecture.md) | 업무 로직과 데이터 접근 층 사이의 의존이 이 패턴에 맞는다 |
| [액티브 레코드](active-record.md) | [계층 아키텍처](../concepts/layered-architecture.md) + [서비스 레이어](../concepts/service-layer-pattern.md) | 같은 의존이 맞고, 바깥 조율이 필요해 서비스 층이 필수가 된다 |
| [도메인 모델 패턴](../concepts/domain-model-pattern.md) | [포트와 어댑터](../concepts/dependency-inversion-principle.md) | 업무 엔티티가 기반 구조에 의존하지도 그것을 알지도 않아야 한다 |
| [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) | 포트와 어댑터 + [CQRS 아키텍처](cqrs-architecture.md) | 같은 격리가 필요하고, 애그리게이트 상태로 질의할 수 없어 CQRS가 **의무**가 된다 |

  - **계층 아키텍처가 도메인 모델에 맞지 않는 이유가 이 표의 축이다** — 위에서 아래로만 의존하는
    형태가 **업무 엔티티는 기반 구조에 의존도 지식도 갖지 않아야 한다**는 요구와 부딪힌다
    (8장, p.125).[^khononov2021] 그 대조는
    [계층 아키텍처 §이 패턴이 맞는 자리와 맞지 않는 자리](../concepts/layered-architecture.md)에
    있다.
  - **CQRS만 의무로 걸린다는 데 주의한다.** 나머지 대응은 "맞는다"이고, 이벤트 소싱 도메인
    모델에 대한 CQRS만 "obligatory"다 (8장, p.135).[^khononov2021]

## 이 판정을 어느 범위에 거는가

**아키텍처 패턴의 선택 범위가 경계 컨텍스트보다 작다는 것이 8장의 마지막 조항이다.**

- 범위의 상한 (8장 §Scope, p.134):[^khononov2021]

> The patterns we've discussed—layered architecture, ports & adapters architecture, and CQRS—should
> not be treated as systemwide organizational principles. These are not necessarily high-level
> architecture patterns for a whole bounded context either.

- 이유는 이 페이지의 첫 축으로 되돌아온다 — 하나의 경계 컨텍스트가 여러 하위 도메인을 품을 수
  있고 그 종류가 핵심·보조·일반으로 다를 수 있다 (8장, p.134):[^khononov2021]

> Even subdomains of the same type may require different business logic and architectural patterns
> (that's the topic of Chapter 10). Enforcing a single, bounded, contextwide architecture will
> inadvertently lead to accidental complexity.

  - **위 [금지가 양쪽으로 걸린다](#금지가-양쪽으로-걸린다)의 "아래로 가는 금지"가 여기서
    아키텍처 층위로 반복된다.** 한 컨텍스트에 하나의 아키텍처를 강제하는 것도 우발적 복잡성이다.
- 처방은 세로 분할이다 (8장, p.134):[^khononov2021]

> Our goal is to drive design decisions according to the actual needs and business strategy. In
> addition to the layers that partition the system horizontally, we can introduce additional vertical
> partitioning. It's crucial to define logical boundaries for modules encapsulating distinct business
> subdomains and use the appropriate tools for each

- 그렇게 해서 얻는 것 (8장, p.134):[^khononov2021]

> Appropriate vertical boundaries make a monolithic bounded context a modular one and help to prevent
> it from becoming a big ball of mud.

  - 저자가 그 논리 경계를 나중에 **더 잘게 나뉜 경계 컨텍스트의 물리 경계로 리팩터링할 수
    있다**고 적고 11장으로 넘긴다 (8장, p.134).[^khononov2021] 경계 컨텍스트의 범위를 정하는
    규칙은 [경계 컨텍스트](bounded-context.md)에 있다.
  - **그러므로 이 페이지의 판정 단위는 경계 컨텍스트가 아니라 하위 도메인이다.** 위
    [판정의 입력은 하위 도메인의 종류다](#판정의-입력은-하위-도메인의-종류다)가 업무 로직
    패턴에 대해 내리는 결론이 아키텍처 패턴에도 그대로 걸린다.

## 휴리스틱이라는 낱말

**10장이 이 페이지의 판정들을 하나의 틀로 묶는다.** 그 틀의 이름이 휴리스틱이고, 장이 그
낱말의 뜻을 먼저 정한다.

- 저자가 장을 여는 진단 — **"상황에 따라 다르다"는 소프트웨어 공학의 거의 모든 물음에 대한
  옳은 답이지만 그다지 실용적이지 않고, 이 장은 그 "상황"이 무엇에 달렸는지를 탐색한다**
  (10장, p.159).[^khononov2021]
- 규정 (10장, p.159):[^khononov2021]

> A heuristic is not a hard rule that is guaranteed and mathematically proven to be correct in 100%
> of cases. Rather, it's a rule of thumb: not guaranteed to be perfect, yet sufficient for one's
> immediate goals. In other words, using heuristics is an effective problem-solving approach that
> ignores the noise inherent in many cues, focusing instead on the "swamping forces" reflected in the
> most important cues.

  - 저자가 이 규정의 출처로 대는 것은 Gerd Gigerenzer, Peter M. Todd, ABC Research Group,
    *Simple Heuristics That Make Us Smart*(Oxford University Press, 1999)다 (10장, p.159,
    각주 1).[^khononov2021] **이 KB가 확인한 원전이 아니다.**
- 이 장의 휴리스틱들이 무엇을 보는지도 밝혀진다 — **서로 다른 업무 도메인의 본질적 성질과 여러
  설계 결정이 다루는 문제의 본질에 초점을 맞춘다** (10장, p.159).[^khononov2021]
- **장의 자리도 명시된다** — 이 장은 I부와 II부를 잇고, 분석 도구를 적용해 소프트웨어 설계
  결정을 이끄는 휴리스틱을 다룬다. **곧 (업무) 도메인이 이끄는 (소프트웨어) 설계다** (10장,
  p.159).[^khononov2021] 그 이름 풀이의 자리는 [전략 설계](strategic-design.md)다.

## 판정을 물음 넷으로 편다

**위 [두 축으로 갈린다](#두-축으로-갈린다)와
[판정의 입력은 하위 도메인의 종류다](#판정의-입력은-하위-도메인의-종류다)가 5장부터 7장에
흩어져 있던 판정을 모은 것이라면, 10장은 저자 자신이 그것을 순서 있는 물음 넷으로 편다.**

- 먼저 패턴 넷의 자리가 다시 배열된다 (10장, p.161):[^khononov2021]
  - **트랜잭션 스크립트와 액티브 레코드는 업무 로직이 단순한 하위 도메인에 더 맞는다** —
    보조 하위 도메인이거나 일반 하위 도메인에 서드파티 솔루션을 통합하는 경우 같은 자리다.
    **둘의 차이는 자료 구조의 복잡성뿐이다.**
  - **도메인 모델과 그 변종인 이벤트 소싱 도메인 모델은 업무 로직이 복잡한 하위 도메인, 곧 핵심
    하위 도메인에 맞는다** (10장, p.162).[^khononov2021]
  - **넷째로 가는 조건이 셋으로 늘어난다** — **금전이나 화폐 거래를 추적하거나, 법으로 감사
    로그 제공이 의무이거나, 시스템 동작에 대한 깊은 분석이 필요한 핵심 하위 도메인은 이벤트
    소싱 도메인 모델로 다루는 편이 낫다** (10장, p.162).[^khononov2021]
- 그 셋을 저자가 물음의 사슬로 세운다 (10장, p.162):[^khononov2021]

> Does the subdomain track money or other monetary transactions or have to provide a consistent audit
> log, or is deep analysis of its behavior required by the business? If so, use the event-sourced
> domain model. Otherwise...

> Is the subdomain's business logic complex? If so, implement a domain model. Otherwise...

> Does the subdomain include complex data structures? If so, use the active record pattern.
> Otherwise...

> Implement a transaction script.

  - **순서가 거꾸로라는 데 주의한다.** 가장 정교한 패턴을 먼저 묻고 하나씩 떨어뜨리며 내려온다.
    아래 [이것이 규칙이 아니라는 단서](#이것이-규칙이-아니라는-단서)가 그 순서의 근거를
    저자의 취향으로 밝힌다.
  - **위 [금지가 양쪽으로 걸린다](#금지가-양쪽으로-걸린다)와 방향이 반대다.** 5장의 금지는
    "핵심에 단순 패턴을 쓰지 마라"였고 이 사슬은 "정교한 패턴이 필요한 이유가 없으면 내려가라"다.
    둘이 같은 대칭의 양쪽이다.
- 저자가 이 사슬을 **하위 도메인의 복잡성과 종류 사이에 강한 관계가 있으므로 도메인 주도 결정
  트리(domain-driven decision tree)로 시각화할 수 있다**고 적는다 (10장,
  p.162).[^khononov2021] 그 도판이 Figure 10-3이다.

## 반대 방향으로도 읽는다 — 분류를 검증하는 쓰임

- **이 판정에 둘째 쓰임이 붙는다** (10장, p.163):[^khononov2021]

> Deciding on the business logic implementation pattern according to the complexity of the business
> logic and its data structures is a way to validate your assumptions about the subdomain type.

- 어긋남이 신호가 된다 — **핵심 하위 도메인이라고 여겼는데 최선의 패턴이 액티브 레코드나
  트랜잭션 스크립트로 나오거나, 보조 하위 도메인이라고 믿은 것이 도메인 모델이나 이벤트 소싱
  도메인 모델을 요구하면, 그 하위 도메인과 업무 도메인 전반에 대한 가정을 다시 볼 훌륭한
  기회다** (10장, p.163).[^khononov2021]
- 다만 단서가 붙는다 (10장, p.163):[^khononov2021]

> Remember, a core subdomain's competitive advantage is not necessarily technical.

  - **그러므로 어긋남이 곧 오분류의 증명은 아니다.** 기술적으로 단순한 핵심 하위 도메인이
    있을 수 있고, 그 판정 기준은 [핵심 도메인](../concepts/core-domain.md)과
    [하위 도메인의 세 종류](subdomain-types.md)에 있다.

## 이 되검증을 요령으로 굳힌 자리 — 부록 A

**같은 판본의 부록 A가 위 되검증을 어디서 얻었는지 밝히고 절차로 굳힌다.** 저자는 그것을
**하위 도메인 식별을 실수 없게 만들려고 마켓노버스에서 고안한 요령**이라 부르고, 내용을
**하위 도메인과 전술 설계 결정 사이의 관계를 뒤집는 것**이라 규정한다 (부록 A §"Mapping design
decisions to subdomains", p.285).[^khononov2021]

- 절차가 세 걸음이다 (부록 A, p.285):[^khononov2021]

> Choose the business logic implementation pattern. No speculation or gold plating; simply
> choose the pattern that fits the requirements at hand. Next, map the chosen pattern to a
> suitable subdomain type. Finally, verify the identified subdomain type with the business
> vision.

  - **첫 걸음에 붙은 단서가 이 요령의 전제다.** 추측도 도금도 하지 말고 **지금 손에 있는 요구
    사항에 맞는 패턴을 그냥 고르라**는 것이다 — 하위 도메인 종류를 미리 염두에 두고 고르면
    검증이 순환 논증이 된다.
- **이 뒤집기의 산출은 설계 판정만이 아니다** — **하위 도메인과 전술 설계 결정의 관계를 뒤집으면
  당신과 업무 사이에 추가적인 대화가 생긴다. 때로는 업무 쪽 사람들이 우리를 필요로 하는 만큼
  우리도 그들을 필요로 한다** (부록 A, p.285).[^khononov2021]
- **어긋남이 두 방향으로 읽히고, 방향마다 다음 행동이 다르다** (부록 A,
  pp.285–286).[^khononov2021]

| 어긋남의 모양 | 저자가 대는 읽기 | 다음 행동 |
|---|---|---|
| 업무가 핵심이라 하는데 하루면 대충 짤 수 있다 | 더 잘게 나눈 하위 도메인이 따로 있거나, 그 사업의 존립 가능성 자체가 의심스럽다 | 세분성을 다시 보거나 업무에 물음을 제기한다 |
| 업무가 보조라 하는데 도메인 모델이나 이벤트 소싱 도메인 모델로만 구현된다 (읽기 1) | 업무 쪽이 요구 사항에 지나치게 창의적이어서 우발적인 업무 복잡성이 생겼다 | 요구 사항을 단순화한다 |
| 업무가 보조라 하는데 정교한 패턴을 요구한다 (읽기 2) | 업무 쪽이 이 하위 도메인에서 추가적인 경쟁 우위를 얻고 있음을 아직 모른다 | 그 어긋남을 드러내 업무가 새 수익원을 더 빨리 찾게 돕는다 |

- **둘째 읽기에는 실물이 붙어 있다** — 보너스 프로젝트가 그 경우였고, 보조로 출발한 그 하위
  도메인이 수익원이 되며 핵심으로 옮겨 갔다 (부록 A, p.285).[^khononov2021] 그 이야기의 전문은
  [마켓노버스 사례 연구](marketnovus-case-study.md)에 있다.
- **그리고 위 [이것이 규칙이 아니라는 단서](#이것이-규칙이-아니라는-단서)가 여기서 실측으로
  뒷받침된다.** 같은 부록이 **정교한 패턴을 필요 없는 자리에 쓴 값**도 기록한다 — 마케팅 허브는
  업무가 핵심이라 불렀으나 기술적 복잡성이 없었고, **평범한 액티브 레코드로 구현할 수 있었을
  만큼 단순한 업무 로직** 위에 이벤트 소싱 도메인 모델과 CQRS와 마이크로서비스를 얹어
  과잉 설계에 이르렀다 (부록 A, p.283).[^khononov2021] 그 진단의 이름과 처방은
  [성장이 낳는 복잡성](growth-driven-complexity.md)에 있다.

## 복잡한 로직과 단순한 로직을 가르는 어림법

- 위 사슬의 둘째 물음이 기대는 경계선에 저자가 어림법을 하나 더 붙인다 — **두 종류를 가르는
  선이 아주 날카롭지는 않지만 쓸모가 있다** (10장, p.162).[^khononov2021]
- 두 신호가 제시된다 (10장, pp.162–163):[^khononov2021]
  - **복잡한 업무 로직은 대체로 복잡한 업무 규칙, 불변식, 알고리즘을 포함한다. 단순한 접근은
    주로 입력을 검증하는 일을 중심으로 돈다.**
  - **둘째 어림법은 유비쿼터스 언어 자체의 복잡성에 관한 것이다** — **그 언어가 주로 CRUD
    연산을 서술하고 있는가, 아니면 더 복잡한 업무 프로세스와 규칙을 서술하고 있는가.**
    - **둘째 신호가 이 KB에서 값이 있다.** 판정의 재료가 코드가 아니라 말이라는 뜻이고, 그
      말의 정본은 [유비쿼터스 언어](ubiquitous-language.md)다. 곧 아직 코드를 쓰지 않은
      시점에도 이 판정을 내릴 수 있다.

## 아키텍처 패턴도 물음 넷으로 편다

**위 [아키텍처 패턴은 업무 로직 패턴에 걸린다](#아키텍처-패턴은-업무-로직-패턴에-걸린다)의
대응표는 8장의 절들에서 이 KB가 모아 만든 것이었다. 10장은 저자 자신이 같은 대응을 목록으로
적는다.**

- 전제 — **의도한 업무 로직 구현 패턴을 알면 아키텍처 패턴을 고르는 일이 직선적이 된다** (10장,
  p.163).[^khononov2021]
- 대응 넷 (10장, p.163):[^khononov2021]

> The event-sourced domain model requires CQRS. Otherwise, the system will be extremely limited in
> its data querying options, fetching a single instance by its ID only.

> The domain model requires the ports & adapters architecture. Otherwise, the layered architecture
> makes it hard to make aggregates and value objects ignorant of persistence.

> The Active record pattern is best accompanied by a layered architecture with the additional
> application (service) layer. This is for the logic controlling the active records.

> The transaction script pattern can be implemented with a minimal layered architecture, consisting
> of only three layers.

  - **위 대응표와 어긋나지 않고 근거를 더한다.** 8장이 각 패턴의 "언제 쓰는가"에서 조건을 적은
    것을 10장이 판정 순서로 다시 세웠고, 이유가 한 줄씩 붙는다.
  - 원문의 `The Active record pattern`은 대문자 표기가 그 문장에서만 다르게 조판된 것이고,
    이 KB는 직인용이므로 원문 표기를 그대로 두었다.
- **예외가 하나 명시된다** (10장, p.163):[^khononov2021]

> The only exception to the preceding heuristics is the CQRS pattern. CQRS can be beneficial not only
> for the event-sourced domain model, but also for any other pattern if the subdomain requires
> representing its data in multiple persistent models.

  - 이 예외가 8장의 분리 선언과 같은 방향이다. 그 서술은 [CQRS 아키텍처](cqrs-architecture.md)에
    있다.

## 테스트 전략도 여기서 따라 나온다

**이 장이 판정의 사슬을 한 칸 더 늘린다.** 업무 로직 패턴과 아키텍처 패턴을 알면 테스트 전략도
정해진다는 것이 그 칸이다.

- 근거 — **업무 로직 구현 패턴과 아키텍처 패턴 둘에 대한 지식을 그 코드베이스의 테스트 전략을
  고르는 휴리스틱으로 쓸 수 있다** (10장, p.164).[^khononov2021] 저자가 드는 전략은 셋이고,
  **셋의 차이는 단위·통합·종단이라는 서로 다른 테스트 종류 중 어디에 무게를 두는가**다 (10장,
  p.165).[^khononov2021]
- **테스트 피라미드 — 도메인 모델 둘** (10장, p.165):[^khononov2021]

> The classic testing pyramid emphasizes unit tests, fewer integration tests, and even fewer
> end-to-end tests. Both variants of the domain model patterns are best addressed with the testing
> pyramid. Aggregates and value objects make perfect units for effectively testing the business
> logic.

- **테스트 다이아몬드 — 액티브 레코드** (10장, p.165):[^khononov2021]

> The testing diamond focuses the most on integration tests. When the active record pattern is used,
> the system's business logic is, by definition, spread across both the service and business logic
> layers. Therefore, to focus on integrating the two layers, the testing pyramid is the more
> effective choice.

  - **원문의 마지막 문장이 "the testing pyramid"라고 적는다.** 절 제목과 앞 문장이 전부
    다이아몬드를 말하므로 원서의 오식으로 보인다. #hypothesis 직인용이므로 원문 그대로
    옮겼고, 이 판단은 이 KB의 것이지 저자의 정정이 아니다.
- **역 테스트 피라미드 — 트랜잭션 스크립트** (10장, p.165):[^khononov2021]

> The reversed testing pyramid attributes the most attention to end-to-end tests: verifying the
> application's workflow from beginning to end. Such an approach best fits codebases implementing the
> transaction script pattern: the business logic is simple and the number of layers is minimal,
> making it more effective to verify the end-to-end flow of the system.

- 셋을 표로 모으면 이렇다.

| 업무 로직 패턴 | 테스트 전략 | 무게가 실리는 곳 | 이유 |
|---|---|---|---|
| [도메인 모델 패턴](../concepts/domain-model-pattern.md) · [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) | 테스트 피라미드 | 단위 | 애그리게이트와 값 객체가 완벽한 단위가 된다 |
| [액티브 레코드](active-record.md) | 테스트 다이아몬드 | 통합 | 업무 로직이 정의상 서비스 층과 업무 로직 층에 걸쳐 있다 |
| [트랜잭션 스크립트](transaction-script.md) | 역 테스트 피라미드 | 종단 | 로직이 단순하고 층이 최소라 종단 흐름 확인이 더 효과적이다 |

- **이 대응이 이 KB의 테스트 축과 겨루는 자리다.** 이 코퍼스의 테스트 축은 종단 테스트를 줄일
  이유를 정면으로 다루고 있고, 그 서술은
  [종단 테스트를 왜 줄이는가](../concepts/why-fewer-end-to-end-tests.md)와
  [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)에
  있다. 어긋남과 그 성격은 그 페이지들에 적었다 — 요지는 **두 소스가 같은 축 위에서 다른 값을
  주는 것이 아니라, 무게 배분을 정하는 입력을 서로 다르게 잡는다**는 것이다. 그쪽은 피드백
  루프의 성질(속도·신뢰·실패 위치 지목)을 입력으로 삼고, 이쪽은 업무 로직 구현 패턴을 입력으로
  삼는다.

## 셋을 하나의 결정 트리로

- 저자가 셋을 합친다 — **업무 로직 패턴, 아키텍처 패턴, 테스트 전략 휴리스틱을 통합해 전술 설계
  결정 트리(tactical design decision tree) 하나로 요약할 수 있다** (10장,
  p.166).[^khononov2021] 그 도판이 Figure 10-7이다.
- 그 트리가 무엇을 주는지 (10장, p.166):[^khononov2021]

> As you can see, identifying subdomains types and following the decision tree gives you a solid
> starting point for making the essential design decisions.

  - **입력이 하나뿐이라는 것이 이 트리의 요점이다.** 하위 도메인의 종류를 식별하는 것 하나로
    업무 로직 패턴·아키텍처 패턴·테스트 전략 셋이 따라 나온다. 그 식별의 절차는
    [하위 도메인의 세 종류](subdomain-types.md)와
    [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md)에 있다.
- 10장 맺음이 그 범위를 다시 적는다 — 업무 도메인과 그 하위 도메인에 대한 지식을 적용해 기술
  결정을 이끄는 법, 곧 **안전한 경계 컨텍스트 경계를 고르고, 애플리케이션의 업무 로직을
  모델링하고, 각 경계 컨텍스트의 내부 구성 요소 사이 상호작용을 조율할 아키텍처 패턴을 정하는
  것**이다. 마지막으로 **어떤 테스트가 더 중요한가라는 자주 격론이 붙는 주제로 우회해 같은 틀을
  써서 테스트를 업무 도메인에 따라 우선순위 매겼다**고 적는다 (10장, p.167).[^khononov2021]

## 이것이 규칙이 아니라는 단서

- 저자가 트리 바로 뒤에 유보를 단다 (10장, p.166):[^khononov2021]

> That said, it's important to reiterate that these are heuristics, not hard rules. There is an
> exception to every rule, let alone heuristics, that by definition are not intended to be correct in
> 100% of the cases.

- **트리의 순서가 저자 개인의 취향이라는 것까지 밝혀진다** (10장, p.167):[^khononov2021]

> The decision tree is based on my preference to use the simple tools, and resort to the advanced
> patterns—domain model, event-sourced domain model, CQRS, and so on—only when absolutely necessary.

- 반례도 저자가 직접 든다 — **이벤트 소싱 도메인 모델을 구현한 경험이 많아 모든 하위 도메인에
  그것을 쓰는 팀들을 만났고, 그들에게는 여러 패턴을 쓰는 것보다 그 편이 더 단순하다**. 다만
  **그 접근을 모두에게 권할 수는 없고, 자신이 일하거나 자문한 회사들에서는 휴리스틱 기반
  접근이 모든 문제에 같은 해법을 쓰는 것보다 효율적이었다**고 적는다 (10장,
  p.167).[^khononov2021]
- 맺음 (10장, p.167):[^khononov2021]

> At the end of the day, it depends on your specific context. Use the decision tree illustrated in
> Figure 10-7, and the design heuristics it is based on, as guiding principles, but not as a
> replacement for critical thinking. If you find that alternative heuristics fit you better, feel
> free to alter the guiding principles or build your own decision tree altogether.

  - **이 단서가 이 페이지 전체의 지위를 정한다.** 위 표들은 판정 규칙이 아니라 출발점이고,
    가장 강한 조항은 여전히 5장의 두 금지다(핵심에 단순 패턴 금지, 단순한 것에 정교한 패턴
    금지). 나머지는 기본값이다.

## 고른 다음에 갈아타는 길

**11장이 이 페이지의 선택을 한 방향 화살표에서 사다리로 바꾼다.** 하위 도메인의 종류가 바뀌면
한번 고른 패턴이 더 이상 맞지 않게 되고, 그때 무엇을 어떻게 옮기는가가 이 절부터의 내용이다.
종류가 바뀌는 여섯 갈래와 그것을 알아채는 신호는
[하위 도메인의 세 종류](subdomain-types.md)에 있다.

- 이행의 전제 조건이 하나 있다 — **업무 로직을 어떻게 모델링할지의 결정이 의식적으로 내려졌고
  가능한 설계 선택지 전부와 그 차이를 알고 있다면, 한 설계 패턴에서 다른 패턴으로 옮기는 것은
  그리 골칫거리가 아니다** (11장, p.173).[^khononov2021]
- **사다리는 위 [두 축으로 갈린다](#두-축으로-갈린다)의 배열을 그대로 따른다** — 트랜잭션
  스크립트에서 액티브 레코드로, 액티브 레코드에서 도메인 모델로, 도메인 모델에서 이벤트 소싱
  도메인 모델로. 저자는 건너뛰기를 다루지 않고, 13장이 한 건너뛰기를 명시적으로 금지한다
  (아래 [13장이 이 경로에 거는 두 단서](#13장이-이-경로에-거는-두-단서)).

## 트랜잭션 스크립트에서 액티브 레코드로

- 두 패턴의 관계가 먼저 정리된다 — **근본에서 트랜잭션 스크립트와 액티브 레코드 패턴은 같은
  원리에 기반한다. 업무 로직이 절차적 스크립트로 구현된다는 것이다. 둘의 차이는 자료 구조를
  어떻게 모델링하는가인데, 액티브 레코드 패턴은 자료 구조를 저장 기제에 매핑하는 복잡성을
  캡슐화하는 자료 구조를 들여온다** (11장, p.174).[^khononov2021]
- **그래서 이행의 방아쇠도 자료 쪽에 있다** (11장, p.174):[^khononov2021]

> when working with data becomes challenging in a transaction script, refactor it into the active
> record pattern

  - 절차는 두 걸음이다 — **복잡한 자료 구조를 찾아 액티브 레코드 객체로 캡슐화하고, 데이터베이스에
    직접 접근하는 대신 액티브 레코드를 써서 그 모델과 구조를 추상화한다** (11장,
    p.174).[^khononov2021]

## 액티브 레코드에서 도메인 모델로

- 방아쇠 (11장, p.174):[^khononov2021]

> If the business logic that manipulates active records becomes complex and you notice more and
> more cases of inconsistencies and duplications, refactor the implementation to the domain model
> pattern.

- 절차가 네 걸음으로 주어진다 (11장, pp.174–175).[^khononov2021]
  1. **값 객체를 식별하는 것부터 시작한다** — **어떤 자료 구조를 불변 객체로 모델링할 수
     있는가? 관련된 업무 로직을 찾아 그것도 값 객체의 일부로 만들라.**
  2. **자료 구조를 분석해 트랜잭션 경계를 찾는다.** 그 첫 수단이 컴파일러다 (11장,
     p.174):[^khononov2021]

     > To ensure that all state-modifying logic is explicit, make all of the active records'
     > setters private so that they can only be modified from inside the active record itself.

     - **컴파일 실패를 도구로 쓰는 것이 이 절의 요령이다** — **당연히 컴파일이 깨질 것을
       예상하라. 그러나 그 컴파일 오류들이 상태를 바꾸는 로직이 어디 있는지 분명하게 보여
       줄 것이다. 그것을 액티브 레코드의 경계 안으로 리팩터링하라** (11장,
       p.174).[^khononov2021] 저자가 드는 예에서 `ApplyBonus` 클래스가 `player.Points`를
       밖에서 고치고 있었고, 세터를 `private set`으로 바꾸면 그 줄이 오류로 드러난다.
     - 다음 반복에서 그 로직이 액티브 레코드 안으로 들어간다 (11장, p.175):[^khononov2021]

       ```csharp
       public class Player
       {
           public Guid Id { get; private set; }
           public int Points { get; private set; }

           public void ApplyBonus(int percentage)
           {
               this.Points *= 1 + percentage/100.0;
           }
       }
       ```

  3. **위계를 찾아 애그리게이트 후보로 삼는다** — 상태를 바꾸는 업무 로직이 전부 해당 객체의
     경계 안으로 옮겨지면 **업무 규칙과 불변 조건을 강하게 일관되게 검사하는 데 어떤 위계가
     필요한지 살핀다. 그것이 애그리게이트의 좋은 후보다.** 자르는 기준은 6장의 원칙이다 (11장,
     p.175):[^khononov2021]

     > look for the smallest transaction boundaries, that is, the smallest amount of data that you
     > need to keep strongly consistent

     - 그 경계를 따라 위계를 분해하고 **외부 애그리게이트는 식별자로만 참조되게 한다** (11장,
       p.175).[^khononov2021]
  4. **애그리게이트마다 루트를 정한다** — **각 애그리게이트에 대해 그 루트, 곧 공개 인터페이스의
     진입점을 식별한다. 애그리게이트 안의 다른 모든 내부 객체의 메서드는 private으로 만들어
     애그리게이트 안에서만 호출될 수 있게 한다** (11장, p.175).[^khononov2021]
- 이 네 걸음이 만드는 것들의 정본은
  [값 객체와 엔티티](../concepts/value-objects-and-entities.md) ·
  [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) ·
  [도메인 모델 패턴](../concepts/domain-model-pattern.md)이다.

## 도메인 모델에서 이벤트 소싱 도메인 모델로

- 조건이 앞 단계의 완료다 — **애그리게이트 경계가 제대로 설계된 도메인 모델을 갖추고 나면 그것을
  이벤트 소싱 모델로 이행시킬 수 있다. 애그리게이트의 데이터를 직접 고치는 대신 애그리게이트의
  생애 주기를 표현하는 데 필요한 도메인 이벤트를 모델링한다** (11장, p.176).[^khononov2021]
- **어려운 것은 코드가 아니라 과거다** (11장, p.176):[^khononov2021]

> The most challenging aspect of refactoring a domain model into an event-sourced domain model is
> the history of the existing aggregates: migrating the "timeless" state into the event-based
> model.

  - 선택지가 둘이고 **그 둘의 전문은 이 페이지에 두지 않았다** —
    [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)이 그 자리다. 과거 전이를 만들어
    내는 길과 마이그레이션 이벤트를 모델링하는 길, 그리고 각각이 무엇을 잃는가가 거기 있다.

## 13장이 이 경로에 거는 두 단서

레거시 코드베이스를 현대화할 때 이 사다리를 어떻게 타는가에 대해 13장이 조항 둘을 더한다
(13장, p.210).[^khononov2021]

- **첫째, 건너뛰지 마라** (13장, p.210):[^khononov2021]

> First, small incremental steps are safer than a big rewrite. Therefore, don't refactor a
> transaction script or active record straight to an event-sourced domain model. Instead, take the
> intermediate step of designing state-based aggregates.

  - 근거가 위험의 비교로 주어진다 — **효과적인 애그리게이트 경계를 찾는 데 노력을 들이고 관련
    업무 로직이 전부 그 경계 안에 있게 하라.** 그렇게 하면 **상태 기반 애그리게이트에서 이벤트
    소싱 애그리게이트로 가는 것이 이벤트 소싱 애그리게이트에서 잘못된 트랜잭션 경계를 발견하는
    것보다 몇 자릿수 더 안전할 것이다** (13장, p.210).[^khononov2021]
- **둘째, 도메인 모델로 가는 것도 원자적 변경일 필요가 없다** — **같은 작은 걸음의 논리를 따라
  도메인 모델 패턴의 요소를 점진적으로 들일 수 있다** (13장, p.210).[^khononov2021] 그 첫
  요소가 정해져 있다 (13장, p.210):[^khononov2021]

> Start by looking for possible value objects. Immutable objects can significantly reduce the
> solution's complexity, even if you are not using a full-blown domain model.

  - 액티브 레코드를 애그리게이트로 바꾸는 것도 마찬가지다 — **관련 업무 로직을 모으는 것부터
    시작하고, 다음으로 트랜잭션 경계를 분석한다. 강한 일관성을 요구하면서 결과적 일관성만
    보장되는 데이터 위에서 돌아가는 결정이 있는가? 반대로 결과적 일관성이면 충분한 자리에
    강한 일관성을 강제하고 있는가?** (13장, p.210).[^khononov2021]
  - **그리고 판정의 주인이 못 박힌다** — **코드베이스를 분석할 때 이 결정들이 기술이 아니라
    업무의 관심사에서 나온다는 것을 잊지 마라. 트랜잭션 요구사항을 철저히 분석한 뒤에야
    애그리게이트의 경계를 설계해야 한다**(When analyzing the codebase, don't forget that these
    decisions are driven by business, not technology, concerns.) (13장,
    p.210).[^khononov2021]
- 이 두 단서가 놓인 더 큰 절차는
  [브라운필드에 도메인 주도 설계 들이기](applying-ddd-to-brownfield.md)에 있다.

## 이어지는 페이지

- [트랜잭션 스크립트](transaction-script.md) — 가장 단순한 패턴이자 나머지의 바탕
- [액티브 레코드](active-record.md) — 자료 구조가 복잡해질 때
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 업무 로직이 복잡할 때
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 시간의 차원까지 필요할 때
- [계층 아키텍처](../concepts/layered-architecture.md) — 첫째 아키텍처 패턴
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 둘째 아키텍처 패턴
  (포트와 어댑터)이 사는 자리
- [CQRS 아키텍처](cqrs-architecture.md) — 셋째 아키텍처 패턴
- [하위 도메인의 세 종류](subdomain-types.md) — 이 선택의 입력이 되는 분류이자 갈아타야 할
  때를 알리는 자리
- [브라운필드에 도메인 주도 설계 들이기](applying-ddd-to-brownfield.md) — 레거시에서 이
  사다리를 타는 절차
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) —
  이행의 셋째 걸음이 만드는 것
- [값 객체와 엔티티](../concepts/value-objects-and-entities.md) — 이행의 첫 걸음이 찾는 것
- [핵심 도메인](../concepts/core-domain.md) — 단순 패턴이 금지되는 자리를 정하는 판정
- [전략 설계](strategic-design.md) — 전략과 전술의 이분법이 규정되는 자리
- [마켓노버스 사례 연구](marketnovus-case-study.md) — 이 판정이 실제로 어긋났을 때 치른 값의
  기록
- [성장이 낳는 복잡성](growth-driven-complexity.md) — 과잉 설계가 낳는 우발적 복잡성
- [스마트 UI 안티패턴](../concepts/smart-ui-antipattern.md) — 같은 절충을 원전이 다루는 자리
- [서비스 레이어](../concepts/service-layer-pattern.md) — 도메인 모델 위에 남는 층
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, II부 "Tactical Design" 도입(pp.61–62) · 5장
    §"When to Use Transaction Script"(pp.68–69) · §"When to Use Active Record"(p.71) ·
    §Conclusion(p.72) · 6장 §"Domain Model"(p.76) · p.86 각주 7 ·
    §"Managing Complexity"(p.95) · 7장 도입(p.99)과 §Conclusion(p.115) ·
    8장 "Architectural Patterns"(도입 p.118 · §"When to Use Layered Architecture"
    pp.124–125 · §"When to Use Ports & Adapters" p.128 · §"When to Use CQRS" pp.133–134 ·
    §Scope p.134 · §Conclusion p.135). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). II부 도비라에는
    쪽 번호가 인쇄되지 않아 오프셋으로 셈했고, 다음 쪽(PDF 89)이 5장 도비라 = 인쇄판 63이라는
    것과 맞는다. 직인용은 `pdftotext -layout` 추출로 대조했고 굽은 따옴표는 곧은 따옴표로
    옮겼다. II부 도입의 8장·9장 예고는 그 장들의 주제 이름만 옮겼다 — 그 장들을 설명하지
    않는다. 이 페이지에는 코드 펜스를 두지 않았다 — 각 패턴의 대표 코드는 해당 페이지에 있다.
    8장 §Scope의 "contextwide"는 원문이 줄바꿈 하이픈(U+2010)으로 끊어 조판한 낱말이라
    이 소스의 하이픈 판별 규칙대로 붙여 적었다 — 같은 문단의 "systemwide"가 그 표기를
    확인해 준다. 아키텍처 패턴 대응표는 원문의 표가 아니라 §"When to Use…" 절 셋과
    §Conclusion에서 이 KB가 모아 만든 것이다. 도판 둘(Figure 8-17 여러 하위 도메인에 걸친
    경계 컨텍스트 · 8-18 아키텍처 슬라이스)은 도판이라 본문이 그것에 대해 적는 것만 옮겼다.
    **10장 "Design Heuristics"(도입 p.159 · §Heuristic p.159 · §"Business Logic Implementation
    Patterns" pp.161–163 · §"Architectural Patterns" pp.163–164 · §"Testing Strategy"
    pp.164–165와 그 아래 §"Testing Pyramid"·§"Testing Diamond"·§"Reversed Testing Pyramid"
    p.165 · §"Tactical Design Decision Tree" pp.166–167 · §Conclusion p.167)이 이 페이지에
    합류했다.** 저자가 대는 출처 하나(Gigerenzer, Todd & ABC Research Group,
    *Simple Heuristics That Make Us Smart*, Oxford University Press 1999)는 이 KB가 확인한
    원전이 아니다. §Heuristic 인용 끝에 붙은 본문 각주 번호 표지("cues.1")는 떼고 옮겼다.
    10장의 도판 일곱(Figure 10-1 여러 경계 컨텍스트에 걸친 변경 · 10-2 넓은 경계 컨텍스트
    경계 · 10-3 업무 로직 구현 패턴 결정 트리 · 10-4 아키텍처 패턴 결정 트리 · 10-5 테스트
    전략 셋 · 10-6 테스트 전략 결정 트리 · 10-7 전술 설계 결정 트리)은 도판이라 본문이 그것에
    대해 적는 것만 산문으로 옮겼다 — **결정 트리 넷은 전부 도판이고 본문에 대응하는 산문이
    있어 그 산문을 옮겼다.** 장 끝 연습문제 넷(pp.167–168)은 claim이 아니라 옮기지 않았다.
    §"Testing Diamond"의 마지막 문장이 "the testing pyramid is the more effective choice"라고
    적는 것은 원문 그대로이고 이 KB의 옮김 오류가 아니다 — `pdftotext -layout` 추출로
    재확인했다.
    **11장 "Evolving Design Decisions" §"Tactical Design Concerns"(pp.173–176)와 13장
    §"Refactoring tactical design decisions"(p.210)이 이 페이지에 합류했다** — 고른 패턴을
    갈아타는 경로가 그 자리다. **이 페이지의 첫 펜스가 여기서 생겼다**: 11장 p.175의 세 번째
    `Player` 목록(private 세터와 애그리게이트 안으로 들어온 `ApplyBonus`)이고, 앞의 두 목록
    (공개 세터 판본과 그것을 private으로 바꿔 컴파일이 깨지는 판본)은 산문으로 줄였다 —
    개념당 대표 펜스 하나 규약에 따랐다. 펜스는 원문 들여쓰기를 그대로 두고 언어
    표지(`csharp`)만 더했다. 11장의 도메인 모델→이벤트 소싱 도메인 모델 이행에서 과거 데이터를
    다루는 두 길(§"Generating Past Transitions" pp.176–177 · §"Modeling Migration Events"
    pp.177–178)은 이 페이지에 두지 않고
    [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)에 두었다 — 같은 claim을 두
    페이지에 흩지 않는다.
    **부록 A §"Mapping design decisions to subdomains"(pp.285–286)와 §"The real problem"
    (p.283)도 이 페이지에 합류했다.** 다섯 경계 컨텍스트의 이야기 본체는 이 페이지에 두지 않고
    [마켓노버스 사례 연구](marketnovus-case-study.md)에 두었다. 위 어긋남 표는 원문의 표가
    아니라 그 절이 산문으로 적는 두 방향과 각 방향의 다음 행동을 이 KB가 표로 모은 것이고 각
    칸의 근거는 그 절의 본문에 있다.

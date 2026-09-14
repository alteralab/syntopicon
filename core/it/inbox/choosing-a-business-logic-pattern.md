---
type: concept
title: 업무 로직 구현 패턴 고르기
description: 전술 설계가 무엇을 묻는 층위인지와 업무 로직을 구현하는 패턴들 사이의 선택 기준 — 전략이 무엇과 왜에 답했다면 전술은 어떻게에 답한다는 배치, 코드가 자기 경계 컨텍스트의 유비쿼터스 언어를 말하게 하는 것이 이 패턴들의 공통 목적이라는 규정, 로직의 복잡성과 자료 구조의 복잡성이라는 두 축으로 갈리는 세 패턴과 시간 차원을 더해 넷째가 서는 자리, 업무 로직 패턴이 정해지면 아키텍처 패턴도 따라 정해진다는 대응표와 CQRS만이 의무로 걸리는 자리, 그 선택을 시스템 전체에도 경계 컨텍스트 전체에도 걸지 말고 하위 도메인 단위의 세로 경계로 나누라는 범위 조항, 판정의 입력이 하위 도메인의 종류라는 대응과 핵심에는 단순 패턴을 쓰지 말라는 금지, 단순한 로직에 정교한 패턴을 쓰면 우발적 복잡성으로 해가 된다는 반대 방향의 금지, 그리고 상위 패턴이 하위 패턴을 대체하지 않고 층으로 겹친다는 판정
generated: { by: "claude-opus-5", at: "2026-09-14T23:00:00Z" }
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
    [계층 아키텍처 §이 패턴이 맞는 자리와 맞지 않는 자리](../concepts/layered-architecture.md#이-패턴이-맞는-자리와-맞지-않는-자리)에
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

## 이어지는 페이지

- [트랜잭션 스크립트](transaction-script.md) — 가장 단순한 패턴이자 나머지의 바탕
- [액티브 레코드](active-record.md) — 자료 구조가 복잡해질 때
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 업무 로직이 복잡할 때
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 시간의 차원까지 필요할 때
- [계층 아키텍처](../concepts/layered-architecture.md) — 첫째 아키텍처 패턴
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 둘째 아키텍처 패턴
  (포트와 어댑터)이 사는 자리
- [CQRS 아키텍처](cqrs-architecture.md) — 셋째 아키텍처 패턴
- [하위 도메인의 세 종류](subdomain-types.md) — 이 선택의 입력이 되는 분류
- [핵심 도메인](../concepts/core-domain.md) — 단순 패턴이 금지되는 자리를 정하는 판정
- [전략 설계](strategic-design.md) — 전략과 전술의 이분법이 규정되는 자리
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

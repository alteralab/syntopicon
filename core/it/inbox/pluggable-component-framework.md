---
type: concept
title: 플러그인 컴포넌트 프레임워크
description: 추상 핵심의 인터페이스와 그것들을 잇는 허브를 대규모 구조로 삼는 가장 빡빡한 패턴 — 같은 추상에 근거하면서 따로 설계된 여러 애플리케이션이 상호 운용해야 할 때 번역이 통합을 제약한다는 문제, 추상 핵심을 증류해 그 인터페이스를 통해서만 동작하는 다양한 구현을 자유롭게 갈아 끼울 수 있게 하라는 조항, 기술 프레임워크는 분산이나 컴포넌트 공유 같은 본질적 기술 문제를 풀 때만 필요하고 기본 패턴은 책임의 개념적 조직이라는 단서, 컴포넌트 뒤에 여러 경계 컨텍스트가 놓일 수 있다는 배치와 공유 커널·지속적 통합·공표된 언어가 그 안에서 공존하는 방식, 인터페이스 설계의 정밀함과 깊은 모델을 요구하며 추상 핵심을 바꿀 수 없어 핵심의 지속적 정련이 얼어붙는다는 대가, 반도체 공장 MES를 위한 SEMATECH CIM 프레임워크 사례, 그리고 이것이 첫 번째도 두 번째도 아닌 대규모 구조여야 한다는 순서
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 플러그인 컴포넌트 프레임워크

- [언제 기회가 생기는가](#언제-기회가-생기는가)
- [무엇이 막히는가](#무엇이-막히는가)
- [허브와 컴포넌트](#허브와-컴포넌트)
- [기술 프레임워크는 부차적이다](#기술-프레임워크는-부차적이다)
- [조항](#조항)
- [경계 컨텍스트가 컴포넌트 뒤에 놓인다](#경계-컨텍스트가-컴포넌트-뒤에-놓인다)
- [대가 — 핵심의 정련이 얼어붙는다](#대가--핵심의-정련이-얼어붙는다)
- [사례 — SEMATECH CIM 프레임워크](#사례--sematech-cim-프레임워크)
- [몇 안 되는 단순한 규칙이 큰 구조를 만든다](#몇-안-되는-단순한-규칙이-큰-구조를-만든다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **같은 도메인에서 여러 팀이 따로 만든 것들을 갈아 끼울 수 있게 하려면 무엇을
공통으로 고정해야 하는가, 그리고 그 고정이 무엇을 앗아 가는가.**

## 언제 기회가 생기는가

- 전제 조건이 앞에 붙는다 — **기회는 깊고 증류된 아주 성숙한 모델에서 생긴다. 플러그인
  컴포넌트 프레임워크는 보통 같은 도메인에서 이미 몇 개의 애플리케이션이 구현된 뒤에야 등판
  한다** (16장, p.475).[^evans2003]
  - 이 조건이 이 장의 다른 세 패턴과 이 패턴을 가른다. 나머지는 이해가 얕을 때도 시작할 수
    있지만 이것은 아니다.

## 무엇이 막히는가

- 문제 서술 (16장, p.475):[^evans2003]

> When a variety of applications have to interoperate, all based on the same abstractions but
> designed independently, translations between multiple BOUNDED CONTEXTS limit integration. A
> SHARED KERNEL is not feasible for teams that do not work closely together. Duplication and
> fragmentation raise costs of development and installation, and interoperability becomes very
> difficult.

  - 앞 장의 관계 패턴 중 공유 커널이 기각되는 조건이 명시된다 — **긴밀히 함께 일하지 않는
    팀들**.

## 허브와 컴포넌트

- 저자가 관찰한 형태 — **어떤 성공한 프로젝트는 설계를 컴포넌트로 분해하고 각각에 일정 범주의
  기능에 대한 책임을 준다. 보통 모든 컴포넌트가 중앙 허브에 꽂히고, 허브는 컴포넌트가 필요로
  하는 프로토콜을 지원하며 그들이 제공하는 인터페이스와 대화하는 법을 안다. 컴포넌트를 잇는 다른
  패턴도 가능하다** (16장, p.475).[^evans2003]
- 분업 — **이 인터페이스들과 그것들을 잇는 허브의 설계는 조율되어야 하지만, 내부를 설계하는
  데는 더 많은 독립이 가능하다** (16장, p.475).[^evans2003]

## 기술 프레임워크는 부차적이다

- 널리 쓰이는 기술 프레임워크가 이 패턴을 지원하지만, 저자는 그것을 **부차적 문제**로 못 박는다
  (16장, p.475):[^evans2003]

> A technical framework is needed only if it solves some essential technical problem such as
> distribution, or sharing a component among different applications. The basic pattern is a
> conceptual organization of responsibilities. It can easily be applied within a single Java
> program.

  - **이 패턴은 기술 선택이 아니다.** 자바 프로그램 하나 안에서도 적용된다는 문장이 그 구분을
    못 박는다. 이 KB에서 프레임워크 최소주의를 다루는 다른 자리와 같은 판정이다.

## 조항

- 처방 문단 (16장, p.475):[^evans2003]

> Distill an ABSTRACT CORE of interfaces and interactions and create a framework that allows
> diverse implementations of those interfaces to be freely substituted. Likewise, allow any
> application to use those components, so long as it operates strictly through the interfaces of
> the ABSTRACT CORE.

  - **증류가 선행 조건으로 조항 안에 들어 있다.** 추상 핵심(ABSTRACT CORE)은 15장의 증류
    기법이고, 이 패턴은 그 산물 위에 선다.
  - **"엄격히 인터페이스를 통해서만"**이 양쪽에 걸린다 — 구현을 갈아 끼울 자유와 애플리케이션이
    컴포넌트를 쓸 자유가 모두 그 조건 아래에만 있다.

## 경계 컨텍스트가 컴포넌트 뒤에 놓인다

- 배치 (16장, pp.475–476):[^evans2003]

> High-level abstractions are identified and shared across the breadth of the system;
> specialization occurs in MODULES. The central hub of the application is an ABSTRACT CORE within
> a SHARED KERNEL. But multiple BOUNDED CONTEXTS can lie behind the encapsulated component
> interfaces, so that this structure can be especially convenient when many components are coming
> from many different sources, or when components are encapsulating preexisting software for
> integration.

- 컴포넌트마다 모델이 갈려야 한다는 뜻은 아니다 (16장, p.476):[^evans2003]
  - 팀이 지속적으로 통합한다면 **여러 컴포넌트를 한 컨텍스트 안에서 개발할 수 있고**, 긴밀히
    관련된 컴포넌트 집합이 공통으로 갖는 또 하나의 공유 커널을 정의할 수도 있다.
  - **이 모든 전략이 플러그인 컴포넌트의 대규모 구조 안에서 쉽게 공존한다.**
  - 또 하나의 선택지 — **허브의 플러그인 인터페이스에 공표된 언어를 쓰는 것.**

## 대가 — 핵심의 정련이 얼어붙는다

- 저자가 드는 하강 요인 둘 (16장, p.476):[^evans2003]
  - **적용하기 아주 어려운 패턴이다.** 인터페이스 설계의 정밀함과 추상 핵심에 필요한 행동을
    담을 만큼 깊은 모델을 요구한다.
  - **애플리케이션의 선택지가 제한된다.** 어떤 애플리케이션이 핵심 도메인에 아주 다른 접근을
    필요로 하면 구조가 방해가 된다. 개발자는 모델을 특화할 수 있지만 **모든 다양한 컴포넌트의
    프로토콜을 바꾸지 않고는 추상 핵심을 바꿀 수 없다.**

> As a result, the process of continuous refinement of the CORE, refactoring toward deeper
> insight, is more or less frozen in its tracks.

  - **이것이 이 장에서 [질서의 진화](evolving-order.md)와 가장 세게 부딪히는 자리다.** 구조를
    진화시키라는 메타 조항과 추상 핵심을 고정하라는 이 패턴의 요구가 정면으로 만난다. 저자는
    그 충돌을 감추지 않고 대가로 적는다.
- 성과의 기록 — **Fayad and Johnson(2000)이 SEMATECH CIM을 포함한 여러 도메인의 야심 찬 시도를
  잘 보여 준다. 그런 프레임워크의 성공은 엇갈린 이야기다. 아마 가장 큰 장애는 쓸모 있는
  프레임워크를 설계하는 데 필요한 이해의 성숙도일 것이다** (16장, p.476).[^evans2003]
- 순서 조항 (16장, p.476):[^evans2003]

> A PLUGGABLE COMPONENT FRAMEWORK should not be the first large-scale structure applied on a
> project, nor the second. The most successful examples have followed after the full development
> of multiple specialized applications.

## 사례 — SEMATECH CIM 프레임워크

예제 "The SEMATECH CIM Framework"가 이 패턴의 실물이다 (16장, pp.476–478).[^evans2003]

- 도메인 — 반도체 공장에서 실리콘 웨이퍼 묶음(lot)이 수백 단계의 공정을 거쳐 기계에서 기계로
  옮겨진다. 소프트웨어는 **각 묶음을 추적해 정확히 어떤 처리가 되었는지 기록하고, 작업자나
  자동화 장비에 다음 적절한 기계로 옮겨 다음 적절한 공정을 적용하도록 지시해야 한다.** 그런
  소프트웨어를 제조 실행 시스템(manufacturing execution system, MES)이라 부른다
  (16장, pp.476–477).[^evans2003]
- 왜 컨소시엄이 필요했는가 — **수십 개 공급사의 수백 종 기계가 쓰이고 단계마다 세심하게
  맞춘 레시피가 있다. 그런 복잡한 조합을 다룰 MES 소프트웨어를 개발하는 일은 벅차고 엄청나게
  비쌌다. 그에 대응해 산업 컨소시엄 SEMATECH이 CIM 프레임워크를 개발했다** (16장,
  p.477).[^evans2003]
- 이 자리에 관련된 국면 둘 (16장, p.477):[^evans2003]
  - **첫째, 프레임워크는 반도체 MES 도메인의 기본 개념들에 대한 추상 인터페이스를 정의한다 —
    다시 말해 핵심 도메인을 추상 핵심의 형태로 정의한다. 이 인터페이스 정의에는 행동과 의미가
    모두 포함된다.** 인터페이스 예로 `Lot`·`Process Flow`·`Process Operation`·`Machine`·
    `Process Machine`이 나오고, 구현 예로 레거시 부품 추적 시스템을 감싼 래퍼, 맞춤 구현,
    공급사의 도구별 구현이 나온다.
  - 공급사가 새 기계를 내면 **`Process Machine` 인터페이스의 특화된 구현을 개발해야 하고, 그
    인터페이스를 지키면 그 기계 제어 컴포넌트는 CIM 프레임워크에 기반한 어떤 애플리케이션에도
    꽂힌다.**
  - **둘째, SEMATECH은 그 인터페이스들이 애플리케이션 안에서 상호작용할 수 있는 규칙을
    정의했다.** CIM 프레임워크에 기반한 애플리케이션은 그 인터페이스의 일부 부분집합을 구현하는
    객체들을 호스팅하는 프로토콜을 구현해야 한다. **그 프로토콜이 구현되고 애플리케이션이 추상
    인터페이스를 엄격히 지키면, 애플리케이션은 구현과 무관하게 그 인터페이스들이 약속한 서비스를
    믿을 수 있다. 그 인터페이스들과 그것을 쓰는 프로토콜의 조합이 아주 제약적인 대규모 구조를
    이룬다** (16장, pp.477–478).[^evans2003]
- 기술적 결합과 그 값의 분리 — **프레임워크는 아주 특정한 기반 구조 요구를 갖는다. 영속성과
  트랜잭션과 이벤트와 그 밖의 기술 서비스를 제공하기 위해 CORBA에 단단히 결합되어 있다. 그러나
  흥미로운 것은 플러그인 컴포넌트 프레임워크의 정의이고, 그것이 사람들로 하여금 독립적으로
  소프트웨어를 개발해 거대한 시스템에 매끄럽게 통합하게 한다** (16장, p.478).[^evans2003]
- 이 패턴이 얻어 내는 것이 한 문장으로 요약된다 (16장, p.478):[^evans2003]

> No one knows all the details of such a system, but everyone understands an overview.

## 몇 안 되는 단순한 규칙이 큰 구조를 만든다

- 절을 닫는 예화는 소프트웨어가 아니다 — **어떻게 수천 명이 독립적으로 일해 4만 장이 넘는 조각
  천으로 된 퀼트 하나를 만들 수 있는가** (16장, p.478).[^evans2003]
- 판정 (16장, pp.478–479):[^evans2003]

> A few simple rules provide a large-scale structure for the AIDS Memorial Quilt, leaving the
> details to individual contributors. Notice how the rules focus on the overall mission
> (memorializing people who have died of AIDS), the features of a component that make integration
> practical, and the ability to handle the quilt in larger sections (such as folding it).

  - 규칙이 초점을 맞추는 곳 셋이 곧 이 패턴의 조항을 다른 매체로 옮긴 것이다 — **전체의 사명**,
    **통합을 실용적으로 만드는 컴포넌트의 특징**, **더 큰 단위로 다룰 수 있는 능력**.
  - 저자는 퀼트 프로젝트 웹사이트의 제작 안내문(패널 설계·재료 선택·제작 기법)을 곁글로
    옮겨 싣는다. 규격이 **완성 치수 3피트 × 6피트, 더도 덜도 안 된다**로 못 박히고 접힘을
    견디는 내구성이 요구되는 대목이 "통합을 실용적으로 만드는 특징"의 실물이다 (16장,
    p.479).[^evans2003]

## 이어지는 페이지

- [대규모 구조](large-scale-structure.md) — 이 패턴이 놓인 축의 가장 빡빡한 끝
- [질서의 진화](evolving-order.md) — 이 패턴과 정면으로 부딪히는 메타 조항
- [격리된 핵심과 추상 핵심](segregated-core.md) — 이 조항이 선행 조건으로 요구하는 증류 기법
- [핵심 도메인](core-domain.md) — 허브에 놓이는 것의 정체
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md) — 공유 커널과 공표된
  언어가 이 구조 안에서 공존하는 자리
- [경계 컨텍스트](../concepts/bounded-context.md) — 컴포넌트 뒤에 놓이는 단위
- [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md) — 기술 프레임워크를
  얼마나 쓸 것인가의 원 조항
- [도메인의 모듈](modules-in-the-domain.md) — 특화가 일어나는 자리
- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 인터페이스에
  행동과 의미를 함께 실어야 한다는 요구의 작은 판본
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §PLUGGABLE COMPONENT FRAMEWORK
    (pp.475–479) — 문제 서술과 처방 문단(p.475) · 배치와 대가와 순서 조항(p.476) ·
    예제 "The SEMATECH CIM Framework"(pp.476–478) · 에이즈 추모 퀼트 예화와 곁글
    "Here's How to Create a Panel for the Quilt"(pp.478–479). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 도판(패턴 도비라의 사진 p.475 · Figure 16.24 CIM 인터페이스 부분집합과 구현
    예 · Figure 16.25 묶음을 다음 기계에 넣고 이동을 기록하는 시퀀스)은 이미지라 인터페이스
    이름과 딸린 판정 산문만 옮겼다. 퀼트 제작 안내문 곁글은 웹사이트에서 인용된 생활 문서라
    규격 한 줄만 옮기고 나머지는 산문으로 줄였다 — 소프트웨어 주장을 늘리지 않는다.
    저자가 대는 서지(Fayad and Johnson 2000)는 이름과 판정만 옮겼다. **이 절에는 코드 목록이
    없다** — 이 페이지에 펜스가 없는 이유다.

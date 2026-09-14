---
type: concept
title: 대규모 구조
description: 모듈 분해와 경계와 증류로도 전체가 보이지 않는 규모에서 이 소스가 여는 셋째 전략 원리 — 나무만 보이고 숲이 안 보인다는 문제 서술과 구조를 "넓은 붓질로 시스템을 논하게 하는 언어"로 규정하는 정의, 대부분의 구조가 UML에 나타나지 않고 모델을 설명만 한다는 관찰, 맞지 않는 구조가 없는 것보다 나쁘다는 판정과 최소한만 찾으라는 계산, 느슨한 은유부터 빡빡한 플러그인 틀까지 규칙을 얼마나 조일 것인가의 저울질과 층 사이 신호를 이벤트로 올리는 사례, 그리고 맞는 구조를 향해 고쳐 가는 네 가지 힘(최소주의·소통과 자기 규율·재구조화가 낳는 유연함·증류가 짐을 덜어 줌)
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 대규모 구조

- [이 장이 여는 물음](#이-장이-여는-물음)
- [모듈도 경계도 증류도 답하지 않는 자리](#모듈도-경계도-증류도-답하지-않는-자리)
- [정의](#정의)
- [이 구조는 대개 모델 안에 나타나지 않는다](#이-구조는-대개-모델-안에-나타나지-않는다)
- [필요하지 않을 때가 있다](#필요하지-않을-때가-있다)
- [규칙을 얼마나 조일 것인가](#규칙을-얼마나-조일-것인가)
- [맞는 구조를 향해 고쳐 간다](#맞는-구조를-향해-고쳐-간다)
- [이 장이 드는 네 가지 구조](#이-장이-드는-네-가지-구조)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **부분을 다 들여다보지 않고도 각 부분이 전체에서 하는 역할을 알게 하려면 설계
전체에 무엇을 걸어야 하는가.**

## 이 장이 여는 물음

- 장을 여는 사례는 위성 통신 시뮬레이터를 만들던 실리콘밸리의 작은 설계 회사다. 모델 주도
  설계가 잘 자라고 있었고 모델의 얽힌 관계를 정리하려고 설계를 **다룰 만한 크기의 정합적
  모듈들로 분해**했는데, 그 결과 모듈이 너무 많아졌다 (16장, pp.439–440).[^evans2003]
  - 그때 팀이 던진 물음이 이 장의 물음이다 — **어느 패키지를 들여다봐야 특정 기능을 찾는가.
    새 클래스는 어디에 두는가. 이 작은 패키지들은 대체 무슨 뜻인가. 이것들이 다 어떻게
    맞물리는가** (16장, p.440).[^evans2003]
  - 팀은 문서로도 모델링 도구의 새 뷰로도 답하지 않았다. 저자는 그것들을 **미봉책**이라 적는다
    (16장, p.440).[^evans2003]
- 진단이 명시된다 — **도메인에서 온 어떤 본질적인 개념이 빠져 있었다. 그러나 이번에는 객체
  모델에서 클래스 한둘이 빠진 것이 아니라, 모델 전체를 위한 구조가 빠져 있었다** (16장,
  p.440).[^evans2003]
- 팀이 택한 답은 통신 시스템의 국면들에 대응하는 **층의 연쇄**였고, 층과 모듈과 객체가 함께
  진화해 설계 전체가 그 층 구조의 윤곽을 따르게 됐다. **이 층들은 모듈도 아니고 코드 안의 다른
  어떤 산물도 아니었다 — 설계 전체에 걸쳐, 심지어 다른 시스템과의 인터페이스에서까지, 어떤
  모듈이나 객체의 경계와 관계든 제약하는 포괄적인 규칙의 집합이었다** (16장,
  p.441).[^evans2003]
  - 결과는 **복잡도의 천장이 올라갔다**로 요약된다 (16장, p.441).[^evans2003]

## 모듈도 경계도 증류도 답하지 않는 자리

이 장의 문제 서술은 앞 장들의 세 기법이 각각 어디까지만 하는지를 차례로 짚는 형태다
(16장, p.441).[^evans2003]

| 앞선 기법 | 하는 일 | 하지 못하는 일 |
|---|---|---|
| 모듈 분해 | 설계를 다룰 만한 덩어리로 나눈다 | 덩어리가 많아지면 다시 못 잡는다. **모듈화가 설계에 균일함을 가져다주지도 않는다** |
| 경계 컨텍스트 | 부패와 혼동을 막는다 | **그것만으로 시스템을 전체로 보기 쉬워지지는 않는다** |
| 증류 | 핵심 도메인에 주의를 모은다 | 떠받치는 요소들과 그것들이 핵심과, 또 서로와 맺는 관계는 여전히 이해해야 한다 |

- 조율이 없을 때 무슨 일이 생기는지도 적힌다 — 스타일과 해법이 제각각이 되어 부분들이 어떻게
  맞물리는지 알기 어려워지고, **한 부분의 설계를 익혀도 다른 부분으로 옮겨지지 않아 프로젝트는
  자기 모듈 밖에서는 서로를 도울 수 없는 전문가들로 끝난다.** 그 상태에서는 지속적 통합이
  무너지고 경계 컨텍스트가 파편화된다 (16장, p.441).[^evans2003]
- 문제 서술의 결론 (16장, p.442):[^evans2003]

> In a large system without any overarching principle that allows elements to be interpreted in
> terms of their role in patterns that span the whole design, developers cannot see the forest
> for the trees. We need to be able to understand the role of an individual part in the whole
> without delving into the details of the whole.

## 정의

- 이 장은 낱말을 먼저 규정한다 (16장, p.442):[^evans2003]

> A "large-scale structure" is a language that lets you discuss and understand the system in
> broad strokes. A set of high-level concepts or rules, or both, establishes a pattern of design
> for an entire system. This organizing principle can guide design as well as aid understanding.
> It helps coordinate independent work because there is a shared concept of the big picture: how
> the roles of various parts shape the whole.

  - **구조는 일차적으로 언어(language)다.** 코드의 산물이 아니라 시스템을 논하는 말이고, 그래서
    조직 원리이면서 동시에 이해의 보조 장치다.
- 조문 형태의 처방 (16장, p.442):[^evans2003]

> Devise a pattern of rules or roles and relationships that will span the entire system and that
> allows some understanding of each part's place in the whole—even without detailed knowledge of
> the part's responsibility.

- 적용 범위 — **구조는 하나의 경계 컨텍스트 안에 갇힐 수도 있지만 대개는 하나 이상에 걸치며,
  프로젝트에 관련된 모든 팀과 서브시스템을 붙들어 두는 개념적 조직을 제공한다. 좋은 구조는
  모델에 대한 통찰을 주고 증류를 보완한다** (16장, p.442).[^evans2003]

## 이 구조는 대개 모델 안에 나타나지 않는다

- 표현 수단에 대한 판정 (16장, p.442):[^evans2003]

> You can't represent most large-scale structures in UML, and you don't need to. Most large-scale
> structures shape and explain the model and design but do not appear in it. They provide an
> extra level of communication about the design.

  - 저자 자신이 이 장의 그림들에서 UML 위에 구조 정보를 **덧씌워** 그린다고 밝힌다. 표기법이
    없는 것을 독자를 위해 얹은 것이다 (16장, pp.442·457).[^evans2003]
  - 그래서 저자는 다른 실천을 제안한다 — **코드가 프로젝트의 최종 설계 문서라면, 층별로
    클래스를 훑어보거나 적어도 층별로 보고해 주는 도구가 있으면 도움이 될 것이다**
    (16장, p.457).[^evans2003]

## 필요하지 않을 때가 있다

- **팀이 어지간히 작고 모델이 그리 복잡하지 않으면 잘 이름 붙인 모듈로의 분해와 얼마간의
  증류와 개발자들 사이의 비공식적 조율만으로도 모델을 정돈된 채로 유지하기에 충분하다**
  (16장, p.442).[^evans2003]
- 그리고 장 전체의 저울을 한 문장으로 세운다 (16장, p.442):[^evans2003]

> Large-scale structure can save a project, but an ill-fitting structure can severely hinder
> development.

  - 이 비대칭이 이 장의 나머지를 지배한다 — **맞지 않는 구조는 없는 것보다 나쁘다**는 판정과
    [질서의 진화](evolving-order.md)의 최소주의가 여기서 나온다.
- 이 축이 다루는 세 전략 원리 중 이것만 선택 사항이라는 규정도 같은 장에 있다 — **컨텍스트
  지도와 달리 대규모 구조는 선택 사항이다** (16장, p.446).[^evans2003]

## 규칙을 얼마나 조일 것인가

§"How Restrictive Should a Structure Be?"가 이 장의 네 패턴을 하나의 축 위에 놓는다
(16장, pp.480–481).[^evans2003]

- 축의 양 끝은 **아주 느슨한 [시스템 은유](system-metaphor.md)**와 **제약이 많은
  [플러그인 컴포넌트 프레임워크](pluggable-component-framework.md)**다. 한 패턴 안에서도 규칙을
  얼마나 조일지에 선택의 폭이 있다 (16장, p.480).[^evans2003]
- 조이는 예로 드는 것이 **층 사이 소통 방식까지 규칙으로 정하는 경우**다. 공장 사례가 그
  까다로움을 보인다 (16장, p.480):[^evans2003]
  - 정책 층이 공정을 지시하고 운영 층이 실행한다. 그런데 현장에서는 실수가 나고 **운영 층은
    세상을 있는 그대로 반영해야 하므로 부품이 엉뚱한 기계에 들어간 사실을 무조건 받아들여야
    한다.**
  - 그 예외 상황은 위층에 알려져야 하는데 **운영 층은 위층에 대해 아무것도 모른다.** 아래에서
    위로 양방향 의존을 만들지 않으면서 알려야 한다.
  - 저자가 드는 전형적인 답은 **이벤트 기제**다 — 운영 객체가 상태 변화마다 이벤트를 내고,
    정책 층 객체가 아래층의 관심 있는 이벤트를 듣는다. 규칙을 어기는 이벤트가 오면 규칙이
    정의의 일부인 동작을 실행하거나 더 위층을 위해 다시 이벤트를 낸다.
  - 은행 사례로도 같은 구조를 보인다 — 자산 가치가 변하고(운영) 그것이 포트폴리오 배분
    한도를 넘으면(정책) 트레이더에게 알림이 가서 매매로 균형을 되돌린다.
- 저울의 양쪽 (16장, pp.480–481):[^evans2003]
  - **조이는 쪽** — 더 제약적인 구조는 균일성을 높여 설계를 해석하기 쉽게 만들고, 구조가 맞다면
    규칙이 개발자를 좋은 설계 쪽으로 밀어 준다. 서로 다른 조각들이 더 잘 맞물린다.
  - **푸는 쪽** — 제약이 개발자에게 필요한 유연성을 앗아갈 수 있다. **아주 특정한 소통 경로는
    경계 컨텍스트를 가로질러, 특히 구현 기술이 다른 이질적 시스템에서 적용하기 비실용적일 수
    있다.**
- 이 절의 결론 (16장, p.481):[^evans2003]

> So you have to fight the temptation to build frameworks and regiment the implementation of the
> large-scale structure. The most important contribution of the large-scale structure is
> conceptual coherence, and giving insight into the domain. Each structural rule should make
> development easier.

## 맞는 구조를 향해 고쳐 간다

§"Refactoring Toward a Fitting Structure"는 먼저 예상되는 반론을 받는다
(16장, p.481):[^evans2003]

> In an era when the industry is shaking off excessive up-front design, some will see
> large-scale structure as a throwback to the bad old days of waterfall architecture. But in
> fact, the only way a useful structure can be found is from a very deep understanding of the
> domain and the problem, and the practical way to that understanding is an iterative
> development process.

- 그 대가가 명시된다 — **진화한다는 것은 최종 구조를 시작 시점에 가질 수 없다는 뜻이고, 그것은
  가면서 리팩터링으로 구조를 밀어 넣어야 한다는 뜻이다. 이것은 비싸고 어려울 수 있지만
  필요하다** (16장, p.481).[^evans2003] 이어 비용을 통제하고 이득을 키우는 네 가지 힘이 나온다.

### 최소주의

- **비용을 낮추는 열쇠 하나는 구조를 단순하고 가볍게 유지하는 것이다. 포괄적이려 들지 마라.
  가장 심각한 관심사만 다루고 나머지는 건별로 처리하게 두라** (16장, p.481).[^evans2003]
- **초기에는 시스템 은유나 책임 층 두어 개 같은 느슨한 구조를 고르는 것이 도움이 될 수 있다.
  최소한의 느슨한 구조라도 혼돈을 막는 가벼운 지침은 된다** (16장, p.481).[^evans2003]

### 소통과 자기 규율

- 조항 (16장, p.482):[^evans2003]

> The entire team must follow the structure in new development and refactoring. To do this, the
> structure must be understood by the entire team. The terminology and relationships must enter
> the UBIQUITOUS LANGUAGE.

- 이것이 구조의 고유한 취약점이라고 명시된다 — **구조가 모델이나 구현의 세부와 맺는 관계는
  보통 코드에 명시되지 않고, 기능 테스트는 구조에 의존하지 않는다.** 게다가 구조는 추상적이라
  큰 팀(또는 여러 팀)에 걸쳐 일관되게 적용하기 어렵다. **일관되게 지키지 않으면 구조는
  부패하는 경향이 있다** (16장, p.482).[^evans2003]
  - 그래서 저자는 대화만으로는 모자라다고 적는다 — **대부분의 팀에서 오가는 종류의 대화로는
    시스템 안에 일관된 대규모 구조를 유지하기에 충분하지 않다. 그것을 프로젝트의 유비쿼터스
    언어에 넣고 모두가 그 언어를 끈질기게 쓰는 것이 결정적이다** (16장, p.482).[^evans2003]

### 재구조화가 유연한 설계를 낳는다

- 저자 자신의 관찰이자 설명되지 않는 관찰 (16장, p.482):[^evans2003]

> I've observed that a design with a large-scale structure is usually much easier to transform
> than one without. This seems to be true even when changing from one kind of structure to
> another, say from METAPHOR to LAYERS. I can't entirely explain this.

  - 부분적인 설명 셋이 제시된다 — 현재 배치를 이해할 수 있으면 재배치가 쉽다는 것, 앞선 구조를
    유지하는 데 든 규율이 시스템 전반에 스며든다는 것, 그리고 **구조를 두 번 겪은 시스템은
    바꾸기가 더 쉽다**는 것 (16장, p.482).[^evans2003]
  - 가죽 재킷 비유로 그 성질을 그린다 — 새 가죽 재킷은 뻣뻣하지만 팔꿈치가 몇 번 굽혀지고
    어깨가 풀리고 몇 달이 지나면 부드러워진다 (16장, pp.482–483).[^evans2003]
- 도착점 (16장, p.483):[^evans2003]

> Ever-increasing knowledge is embedded into them and the principal axes of change have been
> identified and made flexible, while stable aspects have been simplified. The broader
> CONCEPTUAL CONTOURS of the underlying domain are emerging in the model structure.

### 증류가 짐을 덜어 준다

- **모델에 걸어야 할 또 하나의 결정적인 힘은 지속적인 증류다** (16장, p.483).[^evans2003]
  구조를 바꾸는 어려움을 여러 방식으로 줄인다.
  - 첫째, 기제와 일반 하위 도메인과 그 밖의 떠받치는 구조물을 핵심 도메인에서 걷어 내면
    **재구조화할 것 자체가 적어진다** (16장, p.483).[^evans2003]
  - 둘째, 떠받치는 요소들을 구조 안에 단순하게 들어맞도록 정의할 수 있다 — **책임 층 체계에서는
    일반 하위 도메인을 한 층 안에 들어가도록 정의할 수 있고, 플러그인 컴포넌트에서는 일반 하위
    도메인을 한 컴포넌트가 통째로 소유하거나 관련 컴포넌트 집합의 공유 커널로 둘 수 있다**
    (16장, p.483).[^evans2003]
  - 그 요소들은 **핵심 도메인과 독립적으로 움직이고 더 좁게 초점이 맞춰져 있어서** 제자리를
    찾는 리팩터링이 더 쉽고, **결국 덜 중요하므로 다듬기의 정밀도도 덜 중요하다**
    (16장, p.483).[^evans2003]
- 장을 닫는 문장이 구조 자신에게도 같은 원리를 건다 — **증류와 더 깊은 통찰로의 리팩터링이라는
  원리는 대규모 구조 자체에도 적용된다. 예컨대 층은 처음에는 도메인에 대한 피상적 이해에 근거해
  골라지고, 시스템의 근본 책임을 표현하는 더 깊은 추상으로 점차 대체된다** (16장,
  p.483).[^evans2003]

## 이 장이 드는 네 가지 구조

저자는 대규모 구조의 일반 패턴 넷을 든다. 넷은 배타적이지 않고 규칙의 빡빡함이 다르다
(16장, pp.446·480).[^evans2003]

| 패턴 | 무엇으로 조직하는가 | 조이는 정도 |
|---|---|---|
| [시스템 은유](system-metaphor.md) | 시스템 전체를 설명하는 구체적 유비 하나 | 가장 느슨하다 |
| [책임 층](responsibility-layers.md) | 도메인의 자연스러운 성층을 넓은 책임으로 옮긴 층들 | 중간. 규칙을 더 얹을 수 있다 |
| [지식 수준](knowledge-level.md) | 모델을 기술하고 제약하는 별도의 객체 집합 | 다른 축. 다른 구조와 공존한다 |
| [플러그인 컴포넌트 프레임워크](pluggable-component-framework.md) | 추상 핵심의 인터페이스와 허브 | 가장 빡빡하다 |

- 이 목록이 닫힌 목록이 아니라는 단서가 붙는다 — **이 영역은 아직 미개발이다. 나는 여러
  프로젝트에서 나타난 대규모 구조의 일반 패턴 몇 가지를 관찰했다. 이 장에서 넷을 논한다. 그중
  하나가 당신의 필요에 맞거나, 당신 프로젝트에 맞춘 구조에 대한 착상으로 이어질 수 있다**
  (16장, p.446).[^evans2003]
- 이 장 전체를 지배하는 메타 조항은 [질서의 진화](evolving-order.md)다. 저자는 층을 고르는
  대목에서도, 지식 수준을 접는 대목에서도, 구조가 어색한 설계를 강요할 때도 같은 패턴으로
  되돌아간다 (16장, pp.460·464·474).[^evans2003]

## 이어지는 페이지

- [질서의 진화](evolving-order.md) — 이 장 전체를 지배하는 메타 조항
- [시스템 은유](system-metaphor.md) — 가장 느슨한 구조
- [책임 층](responsibility-layers.md) — 이 장에서 가장 길게 다루는 구조
- [지식 수준](knowledge-level.md) — 모델 위에 모델을 두는 구조
- [플러그인 컴포넌트 프레임워크](pluggable-component-framework.md) — 가장 빡빡한 구조
- [전략적 설계](strategic-design.md) — 이 원리가 놓인 IV부의 틀
- [컨텍스트 지도](../concepts/context-map.md) — 선택 사항이 아닌 쪽의 원리
- [핵심 도메인](core-domain.md) — 증류가 이 구조의 짐을 더는 자리
- [개념의 윤곽](conceptual-contours.md) — 구조가 도착하려는 윤곽
- [도메인의 모듈](modules-in-the-domain.md) — 이 구조가 그 위에 얹히는 분해
- [계층 아키텍처](layered-architecture.md) — 이름이 겹치지만 다른 층 나누기
- [유비쿼터스 언어](ubiquitous-language.md) — 구조의 낱말이 들어가야 하는 곳
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" 장 도입(pp.439–442, 위성 통신
    시뮬레이터 사례와 문제 서술과 정의 포함) · §"How Restrictive Should a Structure Be?"
    (pp.480–481) · §"Refactoring Toward a Fitting Structure"(pp.481–483 — §Minimalism p.481 ·
    §"Communication and Self-Discipline" p.482 · §"Restructuring Yields Supple Design"
    pp.482–483 · §"Distillation Lightens the Load" p.483) · §EVOLVING ORDER의 선택 사항
    판정(p.446) · 예제 "In Depth: Layering a Shipping System"의 도구 제안(p.457).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). **이 장은 인쇄판 p.439에서 시작해 p.483에서
    끝나고 p.484는 백지다.** 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 장 도비라의 에이즈 추모 퀼트 사진(p.439)과 패턴 관계도(Figure 16.1, p.443)는
    도판이라 옮기지 않았다. **이 장에는 코드 목록이 하나도 없다** — 이 페이지에 펜스가 없는
    이유다. 표 안의 굵은 글씨는 원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

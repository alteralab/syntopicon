---
type: concept
title: 시스템 은유
description: 시스템 전체를 설명하는 구체적 유비 하나를 대규모 구조로 삼는 가장 느슨한 패턴 — 방화벽 은유가 제품 범주 하나를 만들어 낸 사례와 같은 은유가 선택성 없는 장벽을 낳고 벽 안의 위협에는 무력했다는 양날, 모든 은유는 짐을 지고 온다는 경고, 팀의 상상을 사로잡는 유비가 나타나면 채택해 유비쿼터스 언어에 흡수하되 과잉 확장과 부적절함을 끊임없이 재검토하고 방해가 되면 버릴 준비를 하라는 조항, 정말 쓸모 있는 은유를 찾은 프로젝트가 드물고 역효과를 내는 도메인까지 밀어붙이는 위험, 그리고 도메인 모델을 "순진한 은유"라 부르는 XP 용어를 성숙한 도메인 모델은 순진하지 않다는 근거로 폐기하고 그 자리를 유비쿼터스 언어가 채운다는 판정
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 시스템 은유

- [이 패턴이 가리키는 것](#이-패턴이-가리키는-것)
- [방화벽 — 은유가 산업 하나를 만든 사례이자 잘못 인도한 사례](#방화벽--은유가-산업-하나를-만든-사례이자-잘못-인도한-사례)
- [은유가 설계를 실제로 빚는다](#은유가-설계를-실제로-빚는다)
- [왜 느슨한 구조인가](#왜-느슨한-구조인가)
- [그리고 왜 대부분 실패하는가](#그리고-왜-대부분-실패하는가)
- [조항](#조항)
- ["순진한 은유"라는 말은 폐기되어야 한다](#순진한-은유라는-말은-폐기되어야-한다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **시스템 전체를 한 이야기로 붙드는 유비 하나를 설계의 조직 원리로 삼아도
되는가, 그리고 언제 버려야 하는가.**

## 이 패턴이 가리키는 것

- 낱말의 범위가 먼저 좁혀진다 — **은유적 사고는 소프트웨어 개발에, 특히 모델에 만연해 있다.
  그러나 익스트림 프로그래밍의 "은유" 실천은 은유를 써서 시스템 전체의 개발에 질서를 부여하는
  특정한 방식을 뜻하게 되었다** (16장, p.447).[^evans2003]
- 그래서 이 페이지가 다루는 것은 "비유를 쓰는 일" 일반이 아니라 **대규모 구조로 기능하는 유비
  하나**다.

## 방화벽 — 은유가 산업 하나를 만든 사례이자 잘못 인도한 사례

저자가 드는 사례는 방화벽(firewall)이고, 이 절의 논지가 그 하나에 다 들어 있다
(16장, p.447).[^evans2003]

- **이득** — 불이 이웃 건물로 번지는 것을 막는 건축의 방화벽처럼 소프트웨어 "방화벽"은 바깥의
  더 큰 네트워크로부터 지역 네트워크를 지킨다. 이 은유가 네트워크 아키텍처에 영향을 주었고
  **제품 범주 하나를 통째로 빚었다.** 독립적으로 개발되고 어느 정도 교체 가능하다고 이해되는
  경쟁 제품들이 소비자에게 제공되며, 네트워킹 초심자도 개념을 쉽게 붙든다. **산업 전반과 고객
  사이의 이 공유된 이해는 적지 않은 부분이 그 은유 덕이다.**
- **손실** — **그러나 그것은 부정확한 유비이고 그 힘은 양쪽으로 작용한다.** 방화벽 은유의 사용은
  때때로 충분히 선택적이지 못해 바람직한 교환까지 방해하면서, 정작 벽 안에서 생겨나는 위협에는
  아무 보호도 주지 못하는 소프트웨어 장벽의 개발로 이어졌다. 무선 LAN이 그 취약한 예다.
- 결론 문장 — **방화벽의 명료함은 은혜였지만, 모든 은유는 짐을 지고 온다(all metaphors carry
  baggage).**
- 저자는 이 사례를 워드 커닝햄(Ward Cunningham)의 워크숍 강연에서 들었고 그때 이 패턴이
  이해됐다고 각주로 밝힌다 (16장, p.447, 각주 1).[^evans2003]

## 은유가 설계를 실제로 빚는다

- 왜 필요한가 — **소프트웨어 설계는 아주 추상적이고 붙들기 어려운 경향이 있다. 개발자도
  사용자도 시스템을 이해하고 시스템 전체에 대한 시야를 공유할 손에 잡히는 방법이 필요하다**
  (16장, p.447).[^evans2003]
- 층위가 갈린다 — **한 층위에서 은유는 우리 사고에 아주 깊이 흐르고 있어 모든 설계에 스며
  있다. 시스템에는 서로 "위에 놓이는" "층"이 있고 "중심"에 "커널"이 있다** (16장,
  p.447).[^evans2003] 이 패턴이 말하는 것은 그런 배경적 은유가 아니라 **설계 전체의 중심
  주제를 나르고 팀원 모두에게 공유된 이해를 주는** 은유다.
- 그런 은유가 나타났을 때 벌어지는 일 (16장, pp.447–448):[^evans2003]
  - **시스템이 실제로 그 은유에 의해 빚어진다.** 개발자가 시스템 은유와 일관된 설계 결정을
    내리고, 그 일관성이 다른 개발자로 하여금 복잡한 시스템의 여러 부분을 같은 은유로 해석할 수
    있게 한다.
  - **개발자와 전문가는 논의에서 모델 자체보다 더 구체적일 수 있는 기준점을 갖게 된다.**

## 왜 느슨한 구조인가

- 규정 (16장, p.448):[^evans2003]

> A SYSTEM METAPHOR is a loose, easily understood, large-scale structure that it is harmonious
> with the object paradigm.

  - 원문의 `that it is`는 저자의 오식으로 보이나 직인용이라 그대로 옮겼다. #hypothesis
- 느슨함이 이점이 되는 자리 — **시스템 은유는 어차피 도메인에 대한 유비일 뿐이므로 서로 다른
  모델이 근사적인 방식으로 거기에 사상될 수 있고, 그래서 여러 경계 컨텍스트에 적용되어 그
  사이의 작업을 조율하는 데 도움이 된다** (16장, p.448).[^evans2003]
  - 이것이 [질서의 진화](evolving-order.md)가 요구하는 "구조는 경계를 가로질러야 한다"를 가장
    쉽게 만족시키는 형태다.

## 그리고 왜 대부분 실패하는가

- 인기의 출처와 실패가 같은 문단에 있다 (16장, p.448):[^evans2003]

> SYSTEM METAPHOR has become a popular approach because it is one of the core practices of
> Extreme Programming (Beck 2000). Unfortunately, few projects have found really useful
> METAPHORS, and people have tried to push the idea into domains where it is counterproductive.
> A persuasive metaphor introduces the risk that the design will take on aspects of the analogy
> that are not desirable for the problem at hand, or that the analogy, while seductive, may not
> be apt.

  - 위험이 둘로 갈린다 — **유비의 바람직하지 않은 국면까지 설계가 가져가는 것**과 **유혹적이나
    적절하지 않은 유비**.
- 그럼에도 이 장에 실린 이유가 명시된다 — **그렇긴 하나 시스템 은유는 어떤 프로젝트에서는
  쓸모 있는, 잘 알려진 형태의 대규모 구조이고 구조라는 일반 개념을 잘 예시한다** (16장,
  p.448).[^evans2003]

## 조항

- 처방 문단 (16장, p.448):[^evans2003]

> When a concrete analogy to the system emerges that captures the imagination of team members
> and seems to lead thinking in a useful direction, adopt it as a large-scale structure. Organize
> the design around this metaphor and absorb it into the UBIQUITOUS LANGUAGE. The SYSTEM METAPHOR
> should both facilitate communication about the system and guide development of it. This
> increases consistency in different parts of the system, potentially even across different
> BOUNDED CONTEXTS. But because all metaphors are inexact, continually reexamine the metaphor for
> overextension or inaptness, and be ready to drop it if it gets in the way.

- 조항이 요구하는 것 넷이 한 문단에 있다.
  - **발동 조건이 수동태다** — 유비를 만들어 내라가 아니라 **나타나면(emerges)** 채택하라다.
    시작 시점에 은유를 정하라는 요구가 아니다.
  - **유비쿼터스 언어에 흡수하라** — 은유가 대화에만 머물면 설계를 인도하지 못한다.
  - **두 일을 동시에 해야 한다** — 소통을 쉽게 하는 것과 개발을 인도하는 것.
  - **버릴 준비를 하라** — 과잉 확장(overextension)과 부적절함(inaptness) 두 축으로 끊임없이
    재검토한다. 이것이 [질서의 진화](evolving-order.md)의 이 패턴 판본이다.

## "순진한 은유"라는 말은 폐기되어야 한다

§"The 'Naive Metaphor' and Why We Don't Need It"이 이 절을 닫는다
(16장, pp.448–449).[^evans2003]

- 문제의 용어 — **쓸모 있는 은유가 대부분의 프로젝트에서 저절로 나타나지는 않기 때문에 XP
  공동체의 일부는 순진한 은유(naive metaphor)를 말하게 되었고, 그것으로 도메인 모델 자체를
  가리킨다** (16장, p.448).[^evans2003]
- 저자의 반박 (16장, pp.448–449):[^evans2003]

> One trouble with this term is that a mature domain model is anything but naive. In fact,
> "payroll processing is like an assembly line" is likely a much more naive view than a model
> that is the product of many iterations of knowledge crunching with domain experts, and that has
> been proven by being tightly woven into the implementation of a working application.

  - 근거가 두 겹이다 — **도메인 전문가와의 여러 차례 지식 정련의 산물**이라는 것과 **동작하는
    애플리케이션의 구현에 단단히 엮여 검증되었다**는 것. 은유 쪽에는 둘 다 없다.
- 판정 (16장, p.449):[^evans2003]

> The term naive metaphor should be retired.

- 그 자리를 무엇이 채우는가 (16장, p.449):[^evans2003]

> SYSTEM METAPHORS are not useful on all projects. Large-scale structure in general is not
> essential. In the 12 practices of Extreme Programming, the role of a SYSTEM METAPHOR could be
> fulfilled by a UBIQUITOUS LANGUAGE. Projects should augment that LANGUAGE with SYSTEM METAPHORS
> or other large-scale structures when they find one that fits well.

  - **XP의 열두 실천에서 이 실천 칸을 유비쿼터스 언어가 채울 수 있다**는 것이 이 절의 결론이다.
    은유는 필수가 아니라 언어 위에 얹는 보강이다.

## 이어지는 페이지

- [대규모 구조](large-scale-structure.md) — 이 패턴이 놓인 축의 가장 느슨한 끝
- [질서의 진화](evolving-order.md) — 채택과 폐기를 지배하는 메타 조항
- [유비쿼터스 언어](ubiquitous-language.md) — 은유가 흡수되어야 하는 곳이자 은유 없이도 그
  자리를 채우는 것
- [책임 층](responsibility-layers.md) — 은유에서 옮겨 갈 수 있는 다음 구조
- [깊은 모델과 돌파](deep-model.md) — "성숙한 도메인 모델은 순진하지 않다"의 근거가 있는 자리
- [지식 정련](knowledge-crunching.md) — 그 성숙을 만드는 활동
- [경계 컨텍스트](../concepts/bounded-context.md) — 은유가 가로지를 수 있는 단위
- [이름 짓기](../concepts/naming-things.md) — 이름이 나르는 유비를 더 작은 층위에서 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §SYSTEM METAPHOR(pp.447–449) —
    방화벽 사례(p.447)와 각주 1(Ward Cunningham) · 처방 문단(p.448) ·
    §"The 'Naive Metaphor' and Why We Don't Need It"(pp.448–449). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서
    유지했다. 패턴 도비라의 사진(p.447)은 이미지라 옮기지 않았다. 저자가 대는 서지
    (Beck 2000)는 이름만 옮기고 내용은 옮기지 않았다 — 이 절이 그 책의 실천을 설명하지
    않는다. 이 절에는 코드 목록이 없다.

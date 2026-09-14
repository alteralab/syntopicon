---
type: concept
title: 전략 패턴을 함께 쓰기
description: 컨텍스트와 증류와 대규모 구조를 같은 설계에 동시에 걸 때 셋이 맞물리는 방식 — 셋이 서로의 대체재가 아니라는 규정, 구조가 한 경계 컨텍스트 안에 설 수도 컨텍스트 지도 자체를 조직할 수도 있다는 두 배치, 조직이 구조와 어긋나는 레거시에 구조 안의 자리를 주는 방법과 파사드의 서비스를 한 층에 맞추기, 컨텍스트마다 다른 구조를 쓰면 구조의 값이 깎인다는 경고, 대규모 구조가 핵심 도메인과 일반 하위 도메인의 관계를 설명한다는 짝, 구조 자체가 핵심 도메인의 일부일 수 있다는 판정, 그리고 전략 설계를 어디서 시작하는가에 답하는 현황 평가 여섯 물음
generated: { by: "claude-opus-5", at: "2026-09-14T21:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 전략 패턴을 함께 쓰기

- [이 장이 여는 물음](#이-장이-여는-물음)
- [세 원리는 서로의 대체재가 아니다](#세-원리는-서로의-대체재가-아니다)
- [구조가 설 수 있는 두 자리](#구조가-설-수-있는-두-자리)
- [레거시에 구조 안의 자리를 준다](#레거시에-구조-안의-자리를-준다)
- [컨텍스트마다 다른 구조를 쓸 수는 있다](#컨텍스트마다-다른-구조를-쓸-수는-있다)
- [구조와 증류가 서로를 설명한다](#구조와-증류가-서로를-설명한다)
- [구조 자체가 핵심 도메인의 일부일 수 있다](#구조-자체가-핵심-도메인의-일부일-수-있다)
- [평가가 먼저다](#평가가-먼저다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **전략 설계의 세 원리를 같은 설계에 한꺼번에 걸 때 셋이 어떻게 맞물리고, 무엇부터
하는가.**

## 이 장이 여는 물음

- 이 장의 전제는 앞의 세 장이 따로 제시된 기법들이라는 것이다 — **앞의 세 장은 도메인 주도
  전략 설계를 위한 많은 원리와 기법을 제시했다. 크고 복잡한 시스템에서는 그중 여럿을 같은
  설계에 동원해야 할 수도 있다** (17장, p.485).[^evans2003]
- 그래서 던지는 물음이 넷이다 (17장, p.485):[^evans2003]

> How does a large-scale structure coexist with a CONTEXT MAP? Where do the building blocks fit
> in? What do you do first? Second? Third? How do you go about devising your strategy?

  - 앞의 둘은 **배치**의 물음이고 뒤의 둘은 **순서**의 물음이다. 이 페이지가 앞의 둘과 순서의
    출발점을, [전략 설계 결정하기](strategic-decision-making.md)가 뒤의 "누가 정하는가"를 맡는다.

## 세 원리는 서로의 대체재가 아니다

- 판정 (17장, p.486):[^evans2003]

> The three basic principles of strategic design (context, distillation, and large-scale
> structure) are not substitutes for each other; they are complementary and interact in many
> ways.

  - **이 문장이 이 장의 전제다.** [전략적 설계](strategic-design.md)가 셋을 나란히 소개할 때
    이미 "함께 취해질 때 강력하다"고 적은 것을, 이 장이 구체적인 맞물림으로 푼다.
- 곧바로 드는 예가 구조와 경계의 관계다 — **예를 들어 대규모 구조는 하나의 경계 컨텍스트
  (BOUNDED CONTEXT) 안에 존재할 수도 있고, 여러 컨텍스트를 가로질러 컨텍스트 지도
  (CONTEXT MAP)를 조직할 수도 있다** (17장, p.486).[^evans2003]

## 구조가 설 수 있는 두 자리

**① 한 경계 컨텍스트 안.**

- 16장의 사례가 어느 쪽이었는지를 저자가 밝힌다 — **앞서 든 책임 층(RESPONSIBILITY LAYERS)의
  예들은 하나의 경계 컨텍스트에 갇혀 있었다. 이것이 개념을 설명하는 가장 쉬운 방법이고 이
  패턴의 흔한 쓰임이기도 하다** (17장, p.486).[^evans2003]
- 그 배치에서는 이름의 유효 범위가 컨텍스트를 넘지 않는다 — **그런 단순한 시나리오에서는 층
  이름의 의미가 그 컨텍스트로 제한되고, 그 컨텍스트 안에 존재하는 모델 요소나 서브시스템
  인터페이스의 이름도 마찬가지다** (17장, p.486).[^evans2003]
- 얻는 것이 한 줄로 계상된다 — **그런 지역적 구조는 아주 복잡하지만 통일된 모델에서 쓸모가
  있고, 하나의 경계 컨텍스트 안에서 유지할 수 있는 복잡도의 천장을 올려 준다** (17장,
  p.486).[^evans2003]
  - 14장이 "모델이 복잡하다는 이유로 컨텍스트를 쪼개지 말라"고 적고 다음 두 장으로 넘긴 자리에
    이 문장이 답한다. 그 인계는 [전략적 설계](strategic-design.md)의
    "경계를 쪼개는 것이 답이 아닐 때"에 있다.

**② 컨텍스트 지도 위.**

- 더 흔한 어려움은 다른 쪽이라고 적힌다 — **그러나 많은 프로젝트에서 더 큰 도전은 이질적인
  부분들이 어떻게 맞물리는지를 이해하는 것이다. 그것들은 별개의 컨텍스트로 갈려 있을 수 있는데,
  그렇다면 각 부분이 통합된 전체 시스템에서 무슨 역할을 하고 부분들은 서로 어떻게 관계
  맺는가?** (17장, p.486).[^evans2003]
- 그때의 배치와 그 대가 (17장, p.486):[^evans2003]

> Then the large-scale structure can be used to organize the CONTEXT MAP. In this case, the
> terminology of the structure applies to the whole project (or at least some clearly bounded
> part of it).

  - **구조의 어휘가 프로젝트 전체에 걸린다는 것이 ①과 다른 점이다.** 컨텍스트 안에서만 통하던
    층 이름이 컨텍스트 사이의 공용어가 된다. [컨텍스트 지도](../concepts/context-map.md)가
    "컨텍스트 이름을 유비쿼터스 언어에 넣으라"고 적은 조항 위에 구조의 이름이 한 겹 더 얹힌다.

## 레거시에 구조 안의 자리를 준다

구조를 새로 세우려는데 이미 있는 시스템이 그 구조대로 조직돼 있지 않은 경우다.

- 저자가 물음과 답을 함께 적는다 — **책임 층을 채택하고 싶은데 조직이 바라는 대규모 구조와
  맞지 않는 레거시 시스템이 있다고 하자. 층을 포기해야 하는가? 아니다. 그러나 그 구조 안에서
  레거시가 실제로 차지하는 자리를 인정해야 한다** (17장, p.487).[^evans2003]
- 그리고 그 인정이 손실이 아니라 소득이 된다 — **사실 레거시를 성격 짓는 데 도움이 될 수 있다.
  레거시가 제공하는 서비스(SERVICES)는 실제로 몇 개 층에만 갇혀 있을 수 있다. 레거시 시스템이
  특정 책임 층 안에 든다고 말할 수 있다는 것은 그 시스템의 범위와 역할의 핵심 측면을 간결하게
  기술한다** (17장, p.487).[^evans2003]
  - **구조가 레거시를 서술하는 도구가 되는 자리다.** 16장이 구조를 "넓은 붓질로 시스템을 논하게
    하는 언어"로 규정한 것의 직접적인 용례다
    ([대규모 구조](large-scale-structure.md)).
- 파사드가 있으면 더 가지런해진다 — **레거시 서브시스템의 능력이 파사드(FACADE)를 통해 접근되고
  있다면, 파사드가 제공하는 각 서비스를 한 층 안에 들도록 설계할 수 있을지도 모른다** (17장,
  p.488).[^evans2003]
  - [부패 방지 계층](anticorruption-layer.md)이 파사드·어댑터·번역기로 구현을
    가르는 자리에 이 요구가 하나 더 붙는다 — 파사드의 서비스 경계를 **층 경계와 맞추라**는 것이다.
- 레거시 내부는 열지 않아도 된다 — **이 예에서 레거시인 선적 조율 애플리케이션의 내부는 분화되지
  않은 덩어리로 제시된다. 그러나 컨텍스트 지도에 걸친 대규모 구조가 잘 확립된 프로젝트의 팀은
  자기 컨텍스트 안에서 같은 익숙한 층으로 모델을 정돈하기를 택할 수도 있다** (17장,
  p.488).[^evans2003]
  - 같은 구조가 ②로 서면서 동시에 각 컨텍스트 안에서 ①로도 설 수 있다는 뜻이다.

## 컨텍스트마다 다른 구조를 쓸 수는 있다

- 가능성과 경고가 한 문단에 함께 온다 (17장, p.488):[^evans2003]

> Of course, because each BOUNDED CONTEXT is its own name space, one structure could be used to
> organize the model within one CONTEXT, while another was used in a neighboring CONTEXT, and
> still another organized the CONTEXT MAP. However, going too far down that path can erode the
> value of the large-scale structure as a unifying set of concepts for the project.

  - **허용의 근거는 이름 공간이고 제약의 근거는 목적이다.** 경계 컨텍스트가 저마다 이름
    공간이라는 것은 [경계 컨텍스트](../concepts/bounded-context.md)의 정의에서 곧바로 따라
    나오므로 기술적으로는 막을 것이 없다. 그런데 대규모 구조를 세우는 이유가 **프로젝트를 꿰는
    개념 집합**이므로, 구조를 컨텍스트마다 갈아 끼우면 그 이유가 사라진다.

## 구조와 증류가 서로를 설명한다

- 둘째 짝 (17장, p.488):[^evans2003] **대규모 구조와 증류의 개념 또한 서로를 보완한다. 대규모
  구조는 핵심 도메인(CORE DOMAIN) 안의 관계와 일반 하위 도메인(GENERIC SUBDOMAINS) 사이의
  관계를 설명하는 데 도움을 줄 수 있다.**
  - [핵심 도메인](core-domain.md)과 [일반 하위 도메인](generic-subdomains.md)이 무엇을 떼어
    내는가를 정한다면, 구조는 **떼어 낸 것들이 서로 어떤 관계에 있는가**를 말한다. 증류가 남긴
    덩어리들 사이의 관계는 증류 자체가 답하지 않는 물음이다.

## 구조 자체가 핵심 도메인의 일부일 수 있다

- 방향이 뒤집히는 자리다 (17장, p.489):[^evans2003]

> At the same time, the large-scale structure itself may be an important part of the CORE
> DOMAIN.

- 근거로 드는 예가 16장의 다섯 층이다 — **예컨대 잠재력(potential)·운영(operations)·정책
  (policy)·의사 결정 지원(decision support)의 층 나누기를 구별하는 것은 그 소프트웨어가 다루는
  사업 문제에 근본적인 통찰 하나를 증류한다** (17장, p.489).[^evans2003]
- 그 통찰이 특히 값을 하는 조건이 붙는다 — **이 통찰은 프로젝트가 많은 경계 컨텍스트로 쪼개져
  핵심 도메인의 모델 객체들이 프로젝트의 상당 부분에서 의미를 갖지 못할 때 특히 쓸모 있다**
  (17장, p.489).[^evans2003]
  - **핵심이 객체로 표현될 수 없는 규모에서 핵심이 구조로 표현된다는 말이다.** 모델 객체는
    컨텍스트 경계를 넘지 못하지만 층 이름은 넘는다. 그래서 쪼개진 프로젝트일수록 구조가 증류의
    산물을 나르는 유일한 그릇이 된다.
  - 다섯 층의 목록과 각 층의 성격은 [책임 층](responsibility-layers.md)에 있다.

## 평가가 먼저다

이 장이 "무엇부터 하는가"에 답하는 자리다.

- 조항 — **프로젝트에서 전략 설계에 손을 댈 때는 현재 상황에 대한 분명한 평가에서 출발해야
  한다** (17장, p.490).[^evans2003] 그 평가가 여섯 물음이다 (17장, p.490):[^evans2003]

> 1. Draw a CONTEXT MAP. Can you draw a consistent one, or are there ambiguous situations?
> 2. Attend to the use of language on the project. Is there a UBIQUITOUS LANGUAGE? Is it rich
>    enough to help development?
> 3. Understand what is important. Is the CORE DOMAIN identified? Is there a DOMAIN VISION
>    STATEMENT? Can you write one?
> 4. Does the technology of the project work for or against a MODEL-DRIVEN DESIGN?
> 5. Do the developers on the team have the necessary technical skills?
> 6. Are the developers knowledgeable about the domain? Are they *interested* in the domain?

  - **여섯 중 셋이 사람에 관한 것이다.** 4·5·6번은 모델이 아니라 기술 선택과 팀의 역량과 관심을
    묻는다. 이 장이 뒤에서 결정 주체를 길게 다루는 이유가 여기서 이미 예고된다.
  - 1·2·3번이 가리키는 자리가 각각 [컨텍스트 지도](../concepts/context-map.md)와
    [유비쿼터스 언어](ubiquitous-language.md)와 [핵심 도메인](core-domain.md)·
    [증류 문서와 강조된 핵심](distillation-documents.md)이다. 셋 다 **있는지 묻고 없으면 지금
    만들 수 있는지 묻는** 형식이다.
- 답의 지위를 저자가 스스로 낮춘다 — **물론 완벽한 답은 찾지 못한다. 지금 이 프로젝트에 대해
  아는 것이 앞으로 어느 때보다도 적다. 그러나 이 물음들이 단단한 출발점을 준다** (17장,
  p.490).[^evans2003]
- 그리고 평가를 한 번 하고 끝내는 일로 두지 않는다 — **이 물음들에 대한 구체적인 초기 답을
  갖게 될 즈음이면 무엇이 가장 급히 필요한지에 대한 통찰이 생기기 시작했을 것이다. 시간이
  지나면서 답을 다듬을 수 있는데, 특히 컨텍스트 지도와 도메인 비전 선언과 그 밖에 만들어 둔
  산출물을 바뀐 상황과 새 통찰에 맞게 다듬을 수 있다** (17장, p.490).[^evans2003]
  - [질서의 진화](evolving-order.md)가 구조에 걸었던 요구가 평가 산출물에도 똑같이 걸린다 —
    현황을 그린 문서는 현황이 바뀌면 다시 그린다.

## 이어지는 페이지

- [전략적 설계](strategic-design.md) — 세 원리의 소개와 각각의 몫
- [전략 설계 결정하기](strategic-decision-making.md) — 이 장의 나머지 절반. 누가 이 결정을
  내리는가
- [대규모 구조](large-scale-structure.md) — 여기서 두 자리에 놓이는 셋째 원리의 본체
- [경계 컨텍스트](../concepts/bounded-context.md) — 구조가 안에 설 수도 있고 가로지를 수도 있는 단위
- [컨텍스트 지도](../concepts/context-map.md) — 구조가 조직할 수 있는 전체
- [책임 층](responsibility-layers.md) — 이 장의 예가 계속 쓰는 구조
- [핵심 도메인](core-domain.md) — 구조와 서로를 설명하는 증류의 본체
- [일반 하위 도메인](generic-subdomains.md) — 구조가 관계를 설명해 주는 다른 덩어리
- [증류 문서와 강조된 핵심](distillation-documents.md) — 평가 3번이 묻는 산출물
- [부패 방지 계층](anticorruption-layer.md) — 레거시를 층에 맞출 때 서비스를 내놓는 자리
- [질서의 진화](evolving-order.md) — 평가와 구조를 다시 그리게 하는 메타 조항
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 17장 "Bringing the Strategy Together" 도입(p.485) ·
    §"Combining Large-Scale Structures and BOUNDED CONTEXTS"(pp.485–488) ·
    §"Combining Large-Scale Structures and Distillation"(pp.488–489) ·
    §"Assessment First"(p.490). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을
    작은 대문자로 조판하는 관례를 직인용에서 유지했다. 이 절들의 그림(Figure 17.1의 패턴
    관계도, 17.2부터 17.5까지의 컨텍스트 배치도, 17.6의 층으로 정리된 모듈 지도)은 도판이라
    옮기지 않았고, 그림이 딸린 본문의 판정 산문만 옮겼다. 평가 여섯 물음의 기울임은 원문 표기다.

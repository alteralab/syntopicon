---
type: concept
title: 핵심 도메인
description: 도메인 모델 전체를 고르게 다듬을 수 없다는 전제에서 무엇에 힘을 쏟을지 고르는 패턴의 원전 — 증류가 무엇을 하는 활동인가, 뛰어난 개발자가 기술 인프라로 쏠리고 정작 사업을 가르는 부분이 덜 숙련된 손에 남는다는 진단, 핵심을 작게 만들고 거기에 최고 인재를 붙이라는 조항, 다른 모든 투자를 핵심에 대한 기여로 정당화하라는 회계, 그리고 이 판정이 쉽게 만들어 주는 결정 셋
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 핵심 도메인

- [증류란 무엇인가](#증류란-무엇인가)
- [무엇이 잘못되는가](#무엇이-잘못되는가)
- [조항](#조항)
- [이 판정이 쉽게 만들어 주는 결정 셋](#이-판정이-쉽게-만들어-주는-결정-셋)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인 모델 전체를 고르게 다듬을 수 없을 때 어디에 힘을 쏟을지 어떻게
고르는가.**

## 증류란 무엇인가

- 장이 여는 물음 — **어떻게 중심 문제에 집중하고 곁가지의 바다에 빠지지 않는가?**
  [계층 아키텍처](layered-architecture.md)가 도메인 개념을 기술 로직에서 갈라 놓지만
  **대규모 시스템에서는 격리된 도메인조차 감당할 수 없이 복잡할 수 있다** (15장,
  p.397).[^evans2003]
- 증류(distillation)의 규정 — **증류는 혼합물의 구성 요소를 분리해 본질을 더 값지고 쓸모 있는
  형태로 뽑아내는 과정이다. 모델은 지식의 증류물이다. 더 깊은 통찰로 가는 모든 리팩터링에서
  우리는 도메인 지식과 우선순위의 결정적 측면을 추상해 낸다** (15장, p.397).[^evans2003]
- 무엇을 뽑아내려는 것인지가 명시된다 — 부산물(일반 하위 도메인·정합적 기제)도 그 과정에서
  값이 오르지만 **그 노력의 동기는 특별히 값진 그 한 부분, 우리 소프트웨어를 구별 짓고 만들
  값어치가 있게 만드는 그 부분, 즉 "핵심 도메인"을 뽑아내려는 욕구다** (15장,
  pp.397–398).[^evans2003]
- 전략적 증류가 하는 일 다섯이 열거된다 (15장, p.398):[^evans2003]
  - **모든 팀원이 시스템의 전체 설계와 그것이 어떻게 맞물리는지 파악하도록 돕는다.**
  - **감당할 만한 크기의 핵심 모델을 식별해 유비쿼터스 언어에 들여보냄으로써 소통을 돕는다.**
  - **리팩터링을 인도한다.**
  - **가장 값이 큰 모델 영역에 작업을 집중시킨다.**
  - **외주, 기성 부품 사용, 배치 결정을 인도한다.**

## 무엇이 잘못되는가

- 문제 설정 — **대규모 시스템을 설계할 때는 기여하는 구성 요소가 너무 많고 전부 복잡하며 전부
  성공에 절대적으로 필요해서, 도메인 모델의 정수인 진짜 사업 자산이 가려지고 방치될 수 있다**
  (15장, p.400).[^evans2003]
- **핵심 진단이 인력 배치에 있다** (15장, p.400):[^evans2003]

> The harsh reality is that not all parts of the design are going to be equally refined.
> Priorities must be set. To make the domain model an asset, the model's critical core has to
> be sleek and fully leveraged to create application functionality. But scarce, highly skilled
> developers tend to gravitate to technical infrastructure or neatly definable domain problems
> that can be understood without specialized domain knowledge.

- 왜 그렇게 쏠리는지도 적힌다 — 그런 부분이 **컴퓨터 과학자에게 흥미로워 보이고, 이전 가능한
  전문 기술을 쌓고 더 나은 이력서 재료를 제공한다고 여겨진다** (15장, p.401).[^evans2003]
  그 결과 **애플리케이션을 진짜로 구별 짓고 사업 자산으로 만드는 그 특화된 핵심은 대개 덜
  숙련된 개발자들이 데이터베이스 관리자와 함께 데이터 스키마를 만들고 모델의 개념적 힘을 전혀
  쓰지 않은 채 기능 단위로 코딩해 조립하게 된다** (15장, p.401).[^evans2003]
- 그 대가가 한 문장으로 계상된다 — **소프트웨어의 이 부분의 설계나 구현이 부실하면, 기술
  인프라가 아무리 잘 작동하고 보조 기능이 아무리 훌륭해도 사용자에게 매력적인 일을 결코
  해내지 못하는 애플리케이션이 된다** (15장, p.401).[^evans2003]
- 저자가 겪은 실물이 붙는다. 신디케이트 대출 시스템 프로젝트에서 대부분의 강한 인력이
  데이터베이스 매핑 계층과 메시징 인터페이스에 붙어 있는 동안 업무 모델은 객체 기술에 처음
  손대는 개발자들에게 맡겨져 있었다. 예외였던 한 숙련 개발자는 도메인 객체에 주석을 다는
  우아한 기능을 만들어 프로덕션에 넣었고 — **불행히도 그것은 주변부였다** (15장,
  p.401).[^evans2003] 그동안 **무능한 개발자 하나가 임무에 결정적인 "대출" 모듈을 프로젝트가
  거의 회복하지 못할 뻔한 이해 불가능한 뒤엉킴으로 만들고 있었다** (15장, p.401).[^evans2003]
- 핵심 도메인(core domain)의 정의 — **의도된 애플리케이션의 목적에 구별되고 중심적인 모델의
  그 부분들이 핵심 도메인을 이룬다. 핵심 도메인은 당신의 시스템에서 가장 많은 값이 더해져야
  하는 곳이다** (15장, p.401).[^evans2003]

## 조항

- 처방 문단 (15장, p.402):[^evans2003]

> Boil the model down. Find the CORE DOMAIN and provide a means of easily distinguishing it
> from the mass of supporting model and code. Bring the most valuable and specialized concepts
> into sharp relief. Make the CORE small.
>
> Apply top talent to the CORE DOMAIN, and recruit accordingly. Spend the effort in the CORE
> to find a deep model and develop a supple design—sufficient to fulfill the vision of the
> system. Justify investment in any other part by how it supports the distilled CORE.

- 마지막 문장이 이 패턴의 회계 규칙이다. **다른 모든 부분에 대한 투자는 그것이 증류된 핵심을
  어떻게 지원하는가로 정당화된다.**

## 이 판정이 쉽게 만들어 주는 결정 셋

- 저자가 이 패턴의 실용적 효과로 드는 것들이다 — **핵심 도메인을 증류하는 것은 쉽지 않지만
  몇 가지 쉬운 결정으로 이어진다** (15장, p.402).[^evans2003]
  - **일반화의 방향** — **핵심을 구별되게 만드는 데 많은 노력을 들이면서 설계의 나머지는
    실용적인 한 일반적으로 유지하게 된다** (15장, p.402).[^evans2003]
  - **무엇을 감출 것인가** — **경쟁 우위로 설계의 어떤 측면을 비밀로 유지해야 한다면 그것은
    핵심 도메인이다. 나머지를 감추는 데 노력을 낭비할 필요가 없다** (15장,
    p.402).[^evans2003]
  - **리팩터링의 우선순위** — **그리고 (시간 제약 때문에) 바람직한 두 리팩터링 사이에서
    선택해야 할 때는 핵심 도메인에 가장 영향을 주는 것이 먼저 선택되어야 한다** (15장,
    p.402).[^evans2003]

## 이어지는 페이지

- [지식 정련](knowledge-crunching.md) — 증류가 자라 나오는 활동
- [계층 아키텍처](layered-architecture.md) — 도메인을 먼저 격리하는 앞 단계
- [모델 주도 설계](model-driven-design.md) — 증류된 핵심이 지켜야 할 조항
- [경계 컨텍스트](bounded-context.md) — 무엇을 하나로 유지할지 정하는 다른 축의 판정
- [무엇이 중요한지 정하라](decide-what-matters.md) — 같은 형태의 판정을 코드 층위에서 하는 자리
- [전략적 프로그래밍과 전술적 프로그래밍](strategic-versus-tactical-programming.md) — 어디에
  설계 투자를 할 것인가의 다른 축
- [소프트웨어 설계의 경제학](software-design-economics.md) — 같은 회계를 비용 쪽에서 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 15장 "Distillation" 도입(pp.397–399) · §CORE DOMAIN
    (pp.400–403). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로
    조판하는 관례를 직인용에서 유지했다. 장 머리의 맥스웰 방정식 제사(p.397)는 도판으로
    조판된 수식이라 옮기지 않았다. 전략적 증류의 항해 지도(Figure 15.1, p.398)도 도판이라
    옮기지 않았다. 이 장의 나머지 패턴(§GENERIC SUBDOMAINS pp.406–415 · §DOMAIN VISION
    STATEMENT pp.415–417 · §HIGHLIGHTED CORE pp.417–422 · §COHESIVE MECHANISMS 이하)은
    이 페이지의 물음(무엇에 힘을 쏟을지 어떻게 고르는가) 밖이다.

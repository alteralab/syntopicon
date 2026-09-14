---
type: concept
title: 지식 수준
description: 모델의 일부를 사용자가 주무를 수 있게 하면서도 더 넓은 규칙으로 묶어 두는 대규모 구조 — 다른 객체 집합이 어떻게 행동해야 하는가를 기술하는 객체 집합이라는 파울러의 정의, 조직의 책무 모델처럼 역할과 관계의 규칙이 설치 시점이나 실행 시점에 바뀌어야 하는 요구, 고정된 모델과 완전히 유연한 모델이 둘 다 실패하는 이유와 사용자가 입력 칸을 다른 뜻으로 쓰기 시작해 의미가 어긋나는 결말, 급여와 연금 예제가 과잉 제약에서 과소 제약을 거쳐 종업원 유형이라는 개념을 세우고 지식 수준을 알아본 뒤 급여 대장까지 분리해 내는 과정, 기본 모델의 구조와 행동을 기술하고 제약하는 별도 객체 집합을 만들어 두 수준으로 갈라 두라는 조항, 반사(REFLECTION) 패턴의 도메인 층 적용이되 층이 아니라 수준인 이유와 언어의 반사 도구를 쓰지 말라는 금지, 그리고 이 패턴이 취하게 만든다는 경고와 아껴 쓰라는 단서
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 지식 수준

- [정의](#정의)
- [무엇이 이 패턴을 부르는가](#무엇이-이-패턴을-부르는가)
- [고정과 완전 유연 사이에서 둘 다 실패한다](#고정과-완전-유연-사이에서-둘-다-실패한다)
- [사례 1 — 과잉 제약에서 과소 제약으로, 그리고 유형 객체](#사례-1--과잉-제약에서-과소-제약으로-그리고-유형-객체)
- [모델 안에 모델이 들어 있다](#모델-안에-모델이-들어-있다)
- [반사 패턴의 도메인 층 적용](#반사-패턴의-도메인-층-적용)
- [조항](#조항)
- [아껴 써야 하는 이유](#아껴-써야-하는-이유)
- [사례 2 — 지식 수준을 알아보자 개념 하나가 더 나왔다](#사례-2--지식-수준을-알아보자-개념-하나가-더-나왔다)
- [책임 층의 특수 사례가 아니다](#책임-층의-특수-사례가-아니다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모델의 규칙 자체를 사용자가 바꿀 수 있게 하면서도 아무 관계나 성립하지는
않게 하려면 모델을 어떻게 가르는가.**

## 정의

- 저자는 이 패턴을 자기 말로 정의하지 않고 마틴 파울러(Martin Fowler)의 정의를 그대로 인용해
  절을 연다 (16장, p.465):[^evans2003]

> [A KNOWLEDGE LEVEL is] a group of objects that describes how another group of objects should
> behave. [Martin Fowler, "Accountability," www.martinfowler.com]

- 쓰임 — **지식 수준은 모델의 일부 자체를 사용자의 손에서 주무를 수 있게 하되 더 넓은 규칙
  집합으로 묶어 두어야 할 때 얽힌 것을 푼다. 설치 시점이나 실행 시점에조차 엔티티 사이의
  역할과 관계가 바뀌어야 하는, 설정 가능한 행동을 갖는 소프트웨어의 요구를 다룬다**
  (16장, p.465).[^evans2003]
- 출처와 그 성격이 함께 적힌다 — **『분석 패턴』(Fowler 1996, pp.24–27)에서 이 패턴은 조직 안의
  책무(accountability)를 모델링하는 논의에서 나오고 나중에 회계의 기표 규칙에 적용된다. 여러
  장에 나타나는데도 자기 장을 갖지 못하는데, 그 책의 대부분의 패턴과 다르기 때문이다**
  (16장, p.465).[^evans2003]

> Rather than modeling a domain, as the other analysis patterns do, KNOWLEDGE LEVEL structures a
> model.

  - **도메인을 모델링하는 것이 아니라 모델을 구조화한다.** 이것이 이 패턴이 분석 패턴 목록이
    아니라 대규모 구조 장에 실린 이유다.

## 무엇이 이 패턴을 부르는가

- 저자가 드는 구체적 문제는 조직의 책무 모델이다 — **조직은 사람과 더 작은 조직으로 이루어지고
  그들이 맡는 역할과 그 사이의 관계를 정의한다. 그 역할과 관계를 규율하는 규칙은 조직마다 크게
  다르다** (16장, p.465).[^evans2003]
  - 한 회사에서는 "부서"를 "이사"가 이끌고 그가 "부사장"에게 보고한다. 다른 회사에서는
    "모듈"을 "관리자"가 이끌고 그가 "선임 관리자"에게 보고한다. 그리고 각자가 목적에 따라 다른
    관리자에게 보고하는 "매트릭스" 조직도 있다.
- 전형적인 애플리케이션이 어떻게 무너지는가 (16장, pp.465–466):[^evans2003]
  - 애플리케이션이 몇 가지 가정을 한다. 그 가정이 맞지 않으면 **사용자가 데이터 입력 칸을 원래
    의도와 다른 방식으로 쓰기 시작한다.**
  - **의미가 사용자에 의해 바뀌었으므로 애플리케이션이 가진 어떤 행동이든 빗나간다.** 사용자는
    그 행동을 우회하는 방법을 만들어 내거나 고수준 기능을 아예 꺼 버리게 한다.
  - 사용자는 **자기 일에서 하는 것과 소프트웨어가 동작하는 방식 사이의 복잡한 사상을 배우도록
    강요당한다. 결코 제대로 서비스받지 못한다.**
  - 시스템을 바꾸거나 대체할 때 개발자는 **기능의 의미가 보이는 것과 다르다는 것을 (늦든 이르든)
    발견한다.** 사용자 공동체마다, 상황마다 아주 다른 것을 뜻할 수 있다. **그 덧씌워진 쓰임을
    깨뜨리지 않으면서 무엇이든 바꾸는 일은 두려운 일이 된다.** 더 맞춤한 시스템으로의 데이터
    이전은 그 모든 기벽을 이해하고 코딩할 것을 요구한다.

## 고정과 완전 유연 사이에서 둘 다 실패한다

- 양극이 모두 기각된다 (16장, p.469):[^evans2003]
  - **정적인 모델은 문제를 일으킬 수 있다. 그러나 가능한 모든 관계를 표현하게 하는 완전히
    유연한 시스템도 그만큼 나쁠 수 있다. 그런 시스템은 쓰기 불편하고 조직 자신의 규칙을
    강제하지도 못한다.**
  - **조직마다 소프트웨어를 완전히 맞춤 제작하는 것은 실용적이지 않다.** 각 조직이 맞춤
    소프트웨어 비용을 댈 수 있다 해도 **조직 구조 자체가 자주 바뀌기 때문이다.**
- 그래서 옵션으로 설정하게 하는데, 거기서 다시 문제가 생긴다 — **모델 객체에 그런 옵션을
  더하면 객체가 다루기 힘들어진다. 유연성을 더할수록 전체가 더 복잡해진다** (16장,
  p.469).[^evans2003]
- 문제 서술의 결론 (16장, p.469):[^evans2003]

> In an application in which the roles and relationships between ENTITIES vary in different
> situations, complexity can explode. Neither fully general models nor highly customized ones
> serve the users' needs. Objects end up with references to other types to cover a variety of
> cases, or with attributes that are used in different ways in different situations. Classes that
> have the same data and behavior may multiply just to accommodate different assembly rules.

## 사례 1 — 과잉 제약에서 과소 제약으로, 그리고 유형 객체

예제 "Employee Payroll and Pension, Part 1"이 그 막다른 길을 순서대로 보인다
(16장, pp.466–468).[^evans2003] 중간 규모 회사의 인사 부서가 급여와 연금 기여금을 계산하는
단순한 프로그램을 쓰고 있다.

| 단계 | 모델 | 무엇이 막혔는가 |
|---|---|---|
| 출발 | `Employee`가 `Hourly Employee`와 `Salaried Employee`로 갈리고, `Retirement Plan`이 `Defined Contribution`과 `Defined Benefit`으로 갈린다 | **경영진이 사무 관리직을 확정 급여형 연금에 넣기로 했다. 그런데 사무 관리직은 시급제라 이 모델은 그 조합을 허용하지 않는다** |
| 제안 1 | 제약을 그냥 없앤다 — 모든 종업원이 어느 연금이든 가질 수 있게 한다 | **회사 정책을 반영하지 못해 경영진이 기각한다.** 어떤 관리직은 옮기고 어떤 관리직은 안 옮길 수 있게 되고, 수위도 옮길 수 있게 된다 |
| 제안 2 | `job title` 필드가 중요한 도메인 개념임을 알아보고 `Employee Type`으로 명시한다 | 요구를 만족한다. **`Employee Type` 편집 권한은 "슈퍼유저"로 제한되고 회사 정책이 바뀔 때만 고친다. 인사부의 보통 사용자는 `Employee`를 바꾸거나 다른 `Employee Type`을 가리키게 할 수 있다** |

- 경영진이 강제하고 싶어 한 정책은 한 문장으로 적힌다 (16장, p.468):[^evans2003]

> Office administrators are hourly employees with defined-benefit retirement plans.

- 요구가 유비쿼터스 언어로 다시 진술된다 (16장, p.468):[^evans2003]

> An Employee Type is assigned to either Retirement Plan or either payroll.
> Employees are constrained by the Employee Type.

- 1부는 미완으로 끝난다 — **이 모델은 요구를 만족한다. 개발자들은 암묵적 개념이 하나둘 있다고
  느끼지만 아직 성가신 느낌일 뿐이다. 쫓아갈 만한 확실한 착상이 없어 그날은 접는다** (16장,
  p.468).[^evans2003]

## 모델 안에 모델이 들어 있다

- 문제를 진단하는 두 문장 (16장, p.469):[^evans2003]

> Nestled into our model is another model that is about our model. A KNOWLEDGE LEVEL separates
> that self-defining aspect of the model and makes its constraints explicit.

## 반사 패턴의 도메인 층 적용

- 계보가 밝혀진다 — **지식 수준은 반사(REFLECTION) 패턴을 도메인 층에 적용한 것이고, 그 패턴은
  여러 소프트웨어 아키텍처와 기술 기반 구조에서 쓰이며 Buschmann et al. 1996에 잘 기술되어
  있다** (16장, p.469).[^evans2003]
  - 반사가 하는 일 — **소프트웨어를 "자기 인식적"으로 만들고 구조와 행동의 선택된 국면을
    적응과 변경에 접근 가능하게 만들어 변하는 필요를 수용한다. 이것은 소프트웨어를
    애플리케이션의 운영 책임을 지는 "기본 수준(base level)"과 소프트웨어의 구조와 행동에 대한
    지식을 나타내는 "메타 수준(meta level)"으로 가름으로써 이루어진다** (16장,
    pp.469–470).[^evans2003]
- **왜 "층"이 아니라 "수준"인가** (16장, p.470):[^evans2003]

> Significantly, the pattern is not called a knowledge "layer." As much as it resembles layering,
> REFLECTION involves mutual dependencies running in both directions.

- 용어 대응이 표로 제시된다 (16장, p.470):[^evans2003]

| 파울러 용어 | POSA 용어 |
|---|---|
| Knowledge Level | Meta Level |
| Operations Level | Base Level |

  - POSA는 Buschmann et al. 1996의 *Pattern-Oriented Software Architecture*의 약칭이라고
    각주가 밝힌다 (16장, p.470, 각주 2).[^evans2003]
- 저자는 기술 기반 구조의 반사 사례를 든다 — 자바가 클래스에 메서드를 물어보는 프로토콜 형태로
  **최소한의 내장 반사**를 갖고, CORBA는 다소 더 광범위한 비슷한 반사 프로토콜을 가지며, 일부
  영속성 기술은 그 자기 기술을 확장해 데이터베이스 테이블과 객체 사이의 부분 자동 사상을
  지원한다 (16장, p.470).[^evans2003]
- **그러나 그 도구를 쓰라는 말이 아니다** (16장, p.470):[^evans2003]

> Just to be clear, the reflection tools of the programming language are not for use in
> implementing the KNOWLEDGE LEVEL of a domain model. Those meta-objects describe the structure
> and behavior of the language constructs themselves. Instead, the KNOWLEDGE LEVEL must be built
> of ordinary objects.

- 반사와 갈리는 두 구분 (16장, p.470):[^evans2003]
  - **첫째, 반사의 익숙한 쓰임과 달리 애플리케이션 도메인에 초점을 둔다.**
  - **둘째, 완전한 일반성을 추구하지 않는다. 명세(SPECIFICATION)가 일반 술어보다 더 쓸모 있을
    수 있듯이, 객체 집합과 그 관계에 대한 아주 특화된 제약 집합이 일반화된 프레임워크보다 더
    쓸모 있을 수 있다. 지식 수준은 더 단순하고 설계자의 특정한 의도를 소통할 수 있다.**

## 조항

- 처방 문단 (16장, p.471):[^evans2003]

> Create a distinct set of objects that can be used to describe and constrain the structure and
> behavior of the basic model. Keep these concerns separate as two "levels," one very concrete,
> the other reflecting rules and knowledge that a user or superuser is able to customize.

  - 두 수준을 가르는 기준이 **누가 고칠 수 있는가**로 진술된다는 점이 특징이다. 사례 1에서
    슈퍼유저만 `Employee Type`을 편집할 수 있었던 것이 바로 이 경계였다.

## 아껴 써야 하는 이유

- 경고 (16장, p.471):[^evans2003]

> Like all powerful ideas, REFLECTION and KNOWLEDGE LEVELS can be intoxicating. This pattern
> should be used sparingly.

- 대가 셋이 열거된다 (16장, p.471):[^evans2003]
  - **간접성이 복잡도를 되돌린다** — 운영 객체를 만능 재주꾼이 될 필요에서 풀어 주어 복잡도를
    풀어내지만, 그것이 도입하는 간접성이 그 모호함의 얼마간을 다시 더한다. **지식 수준이
    복잡해지면 시스템의 행동은 개발자에게도 사용자에게도 이해하기 어려워진다.**
  - **설정하는 사용자가 프로그래머가 된다** — 그것을 설정하는 사용자(또는 슈퍼유저)는 결국
    프로그래머의 기술이, 그것도 메타 수준 프로그래머의 기술이 필요해진다. **실수하면
    애플리케이션이 잘못 동작한다.**
  - **데이터 이전 문제가 사라지지 않는다** — 지식 수준의 구조가 바뀌면 기존 운영 수준 객체를
    처리해야 한다. 옛것과 새것이 공존할 수 있을지 모르나 어느 쪽이든 **주의 깊은 분석이
    필요하다.**
- 설계자에게 지워지는 부담 — **설계는 개발 중에 제시된 시나리오뿐 아니라 사용자가 미래에
  소프트웨어를 설정할 수 있는 어떤 시나리오도 감당할 만큼 견고해야 한다** (16장,
  p.471).[^evans2003]
- 그럼에도 값이 있는 자리 — **맞춤 설정이 결정적이고 그것이 아니면 설계를 일그러뜨릴 지점에
  신중하게 적용하면, 지식 수준은 다른 방법으로는 다루기 아주 어려운 문제를 풀 수 있다**
  (16장, p.471).[^evans2003]

## 사례 2 — 지식 수준을 알아보자 개념 하나가 더 나왔다

예제 "Employee Payroll and Pension, Part 2"는 새 모델을 만들지 않고 **이미 있던 모델을 다르게
보는 데서** 시작한다 (16장, pp.471–473).[^evans2003]

- 한 개발자가 하룻밤을 자고 와서 어색한 지점 하나를 파고든다 — **왜 어떤 객체는 보호되고 어떤
  객체는 자유롭게 편집되는가.** 제한된 객체들의 무리가 지식 수준 패턴을 떠올리게 했고, 모델을
  보는 방법으로 그것을 시도해 본다. **기존 모델이 이미 그렇게 볼 수 있었다** (16장,
  p.472).[^evans2003]
  - **제한된 편집은 지식 수준에, 일상적 편집은 운영 수준에 있었다.** 선 위의 모든 객체가
    유형이나 오래 지속되는 정책을 기술했고, **`Employee Type`이 사실상 `Employee`에 행동을
    부과하고 있었다** (16장, p.472).[^evans2003]
- 그 명료함이 다른 개발자에게 둘째 통찰을 준다 (16장, p.472):[^evans2003]
  - 전날 그를 괴롭히던 것이 무엇인지 보인다 — **한 객체에 서로 다른 두 개념이 결합되어
    있었다.** 전날 쓰인 말에서 이미 들렸으나 짚어 내지 못했던 것이다.
  - 문제의 문장은 **"An Employee Type is assigned to either Retirement Plan or either
    payroll"**인데, **그것은 실은 유비쿼터스 언어의 진술이 아니었다. 모델에 "payroll"이
    없었다. 그들은 가진 언어가 아니라 원하는 언어로 말하고 있었다.**
  - **급여 대장(payroll) 개념이 모델에 암묵적으로, `Employee Type`에 뭉쳐진 채 있었다.
    지식 수준이 분리되어 그 핵심 구절의 요소들이 같은 수준에 함께 나타나기 전까지는 — 하나만
    빼고 — 그렇게 뚜렷하지 않았다.**
- 리팩터링 결과 `Payroll`이 `Employee Type`에서 떨어져 나와 `Hourly Payroll`과
  `Salaried Payroll`로 갈리고, 각 `Employee Type`이 `Retirement Plan` 하나와 `Payroll` 하나를
  갖는다 (16장, p.473).[^evans2003]
- 예제의 결론 (16장, p.473):[^evans2003]

> KNOWLEDGE LEVEL was hinted at by the characteristic access restrictions and a "thing-thing"
> type relationship. Once it was in place, the clarity it afforded helped produce another insight
> that disentangled two important domain concepts by factoring out Payroll.

  - **발견의 표지 둘** — 특징적인 접근 제한, 그리고 "사물-사물 유형" 관계.
- 그리고 곧바로 선택 사항임이 다시 확인된다 — **지식 수준도 다른 대규모 구조처럼 엄밀히
  필요하지는 않다. 객체는 그것 없이도 동작하고, `Employee Type`과 `Payroll`을 가른 통찰도
  여전히 찾아 쓸 수 있었을 것이다. 이 구조가 제 몫을 못 하는 것처럼 보여 버려야 할 때가 올
  수도 있다. 그러나 지금은 시스템에 대해 쓸모 있는 이야기를 해 주고 개발자가 모델과 씨름하도록
  돕는 듯하다** (16장, p.474).[^evans2003]

## 책임 층의 특수 사례가 아니다

- 겉보기의 유사성이 명시적으로 기각된다 (16장, p.474):[^evans2003]

> At first glance, KNOWLEDGE LEVEL looks like a special case of RESPONSIBILITY LAYERS, especially
> the "policy" layer, but it is not. For one thing, dependencies run in both directions between
> the levels, but with LAYERS, lower layers are independent of upper layers.

- 그래서 공존한다 — **사실 지식 수준은 대부분의 다른 대규모 구조와 공존할 수 있고, 조직화의
  또 하나의 차원을 제공한다** (16장, p.474).[^evans2003]
  - 즉 이 장의 네 패턴 중 이것만 **다른 축**이다. 구조를 고를 때 이것과 저것 중 하나를
    고르는 것이 아니다.

## 이어지는 페이지

- [대규모 구조](large-scale-structure.md) — 이 패턴이 놓인 장의 틀
- [책임 층](responsibility-layers.md) — 겉보기에 겹치지만 의존 방향이 다른 구조
- [명세 패턴](specification-pattern.md) — "일반 술어보다 특화된 제약이 낫다"의 짝
- [명시적 제약](explicit-constraints.md) — 규칙을 객체로 올리는 같은 동작의 더 작은 판본
- [분석 패턴을 모델에 들이기](analysis-patterns-in-the-model.md) — 이 패턴이 빌려 온 책과
  그 책을 쓰는 조건
- [모델링 패러다임](modeling-paradigms.md) — 규칙을 별도 기술로 돌릴 때의 조건
- [암묵적 개념 파내기](digging-out-implicit-concepts.md) — 사례 2에서 `Payroll`이 나오는 절차
- [유비쿼터스 언어](ubiquitous-language.md) — "가진 언어가 아니라 원하는 언어로 말하고 있었다"의
  진단 기준
- [값 객체와 엔티티](value-objects-and-entities.md) — 유형 객체가 어느 쪽인가를 판정하는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §KNOWLEDGE LEVEL(pp.465–474) —
    파울러 정의 인용과 책무 사례(pp.465–466) · 예제 "Employee Payroll and Pension, Part 1"
    (pp.466–468) · 문제 서술과 반사 패턴 논의(pp.469–470, 각주 2 포함) · 처방 문단과 대가
    (p.471) · 예제 "Employee Payroll and Pension, Part 2: KNOWLEDGE LEVEL"(pp.471–474) ·
    책임 층과의 대비(p.474). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은
    대문자로 조판하는 관례를 직인용에서 유지했다. 도판 전부(절 머리의 지식 수준 도식 p.465 ·
    Figure 16.15~16.23 — 옛 모델, 그 모델로 표현한 종업원 인스턴스, 제약을 없앤 제안,
    잘못된 연금과 짝지어진 인스턴스, 유형 객체를 세운 모델과 그 인스턴스, 기존 모델에서
    지식 수준을 알아본 그림, `Payroll`을 분리한 모델과 그 인스턴스)는 이미지라 딸린 판정
    산문과 클래스 이름만 옮겼다. 파울러 인용문 안의 대괄호와 URL은 원문 그대로다.
    **이 절에는 코드 목록이 없다** — 이 페이지에 펜스가 없는 이유다. 표 안의 굵은 글씨는
    원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

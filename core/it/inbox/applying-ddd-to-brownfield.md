---
type: concept
title: 브라운필드에 도메인 주도 설계 들이기
description: 이미 돌아가는 레거시 체계와 DDD를 모르는 조직에 이 방법론을 들이는 절차 — 그린필드에서만 쓸 수 있다는 오해와 전부 아니면 전무라는 오해의 기각, 회사의 업무 도메인과 경쟁 상대를 묻는 네 물음과 조직도에서 시작해 종류별 표지를 찾는 하위 도메인 식별과 가장 못생긴 코드가 핵심의 표지라는 역설적 어림법, 생애 주기가 분리된 고수준 구성 요소를 찾아 현재 설계를 탐색하고 실제로 쓰인 패턴과 현재의 컨텍스트 지도를 그려 평가하는 절차와 전략적으로 나쁜 신호 다섯, 큰 재작성이 드물게 성공한다는 경고와 크게 생각하고 작게 시작하라는 대안과 논리 경계를 하위 도메인에 맞추는 안전한 첫 리팩터링, 논리 경계를 물리 경계로 승격시키는 두 물음과 통합 패턴이 푸는 문제 넷, 가장 아픈 불일치를 먼저 고치라는 전술적 우선순위, 유비쿼터스 언어를 기르는 것이 현대화의 선행 조건이고 이벤트스토밍이 그 지름길이라는 배치, 도구를 다 쓰지 않아도 된다는 실용주의, 그리고 관리자의 승인 없이 개인의 연장통으로 쓰는 잠행 DDD와 권위 대신 논리로 설득하라는 물음 목록, 그리고 같은 현대화를 마이크로서비스 쪽에서 세운 소스가 이 절차 앞에 놓는 물음 — 목표부터 정하고 더 쉬운 길을 먼저 보라는 조항과 그것이 이 페이지의 전략 분석과 겹치는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-15T12:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
---

# 브라운필드에 도메인 주도 설계 들이기

- [두 가지 오해를 먼저 걷어 낸다](#두-가지-오해를-먼저-걷어-낸다)
- [전략 분석 — 업무 도메인을 이해한다](#전략-분석--업무-도메인을-이해한다)
- [종류별로 무엇을 찾는가](#종류별로-무엇을-찾는가)
- [현재 설계를 탐색한다](#현재-설계를-탐색한다)
- [전술 설계를 평가한다](#전술-설계를-평가한다)
- [전략 설계를 평가한다](#전략-설계를-평가한다)
- [현대화 전략 — 크게 생각하고 작게 시작한다](#현대화-전략--크게-생각하고-작게-시작한다)
- [전략적 현대화 — 논리 경계를 물리 경계로](#전략적-현대화--논리-경계를-물리-경계로)
- [전술적 현대화 — 가장 아픈 불일치부터](#전술적-현대화--가장-아픈-불일치부터)
- [유비쿼터스 언어를 기른다](#유비쿼터스-언어를-기른다)
- [두 갈래 — 갈아 치우기와 고쳐 쓰기](#두-갈래--갈아-치우기와-고쳐-쓰기)
- [실용적 도메인 주도 설계](#실용적-도메인-주도-설계)
- [잠행 DDD — 권위 대신 논리로](#잠행-ddd--권위-대신-논리로)
- [같은 현대화를 마이크로서비스 쪽에서 세운 소스](#같은-현대화를-마이크로서비스-쪽에서-세운-소스)
- [원전의 첫째 필수와 잠행이 양립하는가](#원전의-첫째-필수와-잠행이-양립하는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **이미 돌아가고 있는 체계와 이 방법론을 모르는 조직에 도메인 주도 설계를 어떤
순서로 들이는가.**

## 두 가지 오해를 먼저 걷어 낸다

- **첫째 오해 — 그린필드에서만 쓸 수 있다.** 저자는 이상적인 그린필드 프로젝트를 한 문단
  묘사한 뒤 **"이제 깨어나라"**로 끊는다. 그런 실험실 조건을 겪을 확률은 복권 당첨과
  비슷하다는 것이다 (13장, p.201).[^khononov2021] 그리고 판정을 뒤집는다 (13장,
  p.201):[^khononov2021]

> the projects that can benefit from DDD the most are the brownfield projects: those that already
> proved their business viability and need a shake-up to fight accumulated technical debt and
> design entropy

  - 덧붙는 관찰이 있다 — **공교롭게도 그런 브라운필드·레거시·큰 진흙 공 코드베이스에서
    일하는 것이 우리가 소프트웨어 공학 경력의 대부분을 보내는 자리다** (13장,
    p.201).[^khononov2021]
- **둘째 오해 — 전부 아니면 전무다** (13장, p.201):[^khononov2021]

> Another common misconception about DDD is that it's an all-or-nothing proposition—either you
> apply every tool the methodology has to offer, or it's not domain-driven design. That's not
> true.

  - 그 기각의 이유가 브라운필드에서 더 세다 — **브라운필드 프로젝트에서는 모든 패턴과 관행을
    합리적인 기간 안에 들이는 것이 사실상 불가능하다** (13장, p.202).[^khononov2021]
    이 조항의 전문은 아래 [실용적 도메인 주도 설계](#실용적-도메인-주도-설계)에 있다.

## 전략 분석 — 업무 도메인을 이해한다

- 출발점이 코드가 아니다 (13장, p.202):[^khononov2021]

> the best starting point for introducing DDD in an organization is to invest time in
> understanding the organization's business strategy and the current state of its systems'
> architecture

- 먼저 회사의 업무 도메인을 식별하는 네 물음이다 (13장, p.202).[^khononov2021]
  - **조직의 업무 도메인은 무엇인가?**
  - **그 고객은 누구인가?**
  - **조직이 고객에게 주는 서비스 또는 값은 무엇인가?**
  - **조직이 경쟁하는 회사나 제품은 무엇인가?**
- 그다음 한 단계 내려간다 — 이 물음들이 **회사의 높은 수준 목표를 조망하게** 해 주고, 그
  목표를 이루기 위해 조직이 쓰는 업무 구성 블록, 곧 하위 도메인으로 "확대"한다 (13장,
  p.202).[^khononov2021]
- **첫 어림법이 조직도다** (13장, p.202):[^khononov2021]

> A good initial heuristic is the company's org chart: its departments and other organizational
> units.

  - 그리고 **그 단위들이 회사가 자기 업무 도메인에서 경쟁할 수 있도록 어떻게 협력하는지
    살핀다** (13장, p.202).[^khononov2021] 같은 출발점을 1장이 이미 세웠고 그 전문은
    [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md)에 있다.

## 종류별로 무엇을 찾는가

- **핵심 하위 도메인** — 경쟁사와 다른 것을 찾는다 (13장, pp.202–203).[^khononov2021]
  - **회사에 경쟁사가 갖지 못한 "비밀 소스"가 있는가? 예를 들어 특허나 사내에서 설계한
    알고리즘 같은 지적 재산이?**
  - **경쟁 우위가, 따라서 핵심 하위 도메인이 반드시 기술적이지는 않다는 것을 명심하라.
    회사가 비기술적 경쟁 우위를 갖고 있는가? 예를 들어 최상급 인재를 채용하는 능력이나 독특한
    예술적 디자인을 만들어 내는 능력 같은?**
- **그리고 역설적인 셋째 어림법이 붙는다** (13장, p.203):[^khononov2021]

> Another powerful yet unfortunate heuristic for core subdomains is identifying the worst-designed
> software components—those big balls of mud that all engineers hate but the business is unwilling
> to rewrite from scratch because of the accompanying business risk.

  - 그 어림법이 성립하는 이유가 배제로 주어진다 — **여기서 관건은 그 레거시 체계가 기성
    체계로 대체될 수 없다는 것이다. 대체될 수 있다면 그것은 일반 하위 도메인일 것이다. 그리고
    거기에 손대는 모든 변경이 업무 위험을 수반한다** (13장, p.203).[^khononov2021]
- **일반 하위 도메인** — **기성 해법, 구독 서비스, 오픈 소스 소프트웨어 통합을 찾는다.**
  같은 기성 해법이 경쟁사에도 열려 있어야 하고, 그것을 쓰는 다른 회사가 우리 회사에 업무적
  영향을 주지 않아야 한다 (13장, p.203).[^khononov2021]
- **보조 하위 도메인** — **기성 해법으로 대체할 수 없으면서 경쟁 우위를 직접 주지도 않는
  나머지 구성 요소**다. 판별 표지가 사람의 반응에 있다 — **코드 상태가 험해도 자주 바뀌지
  않으므로 엔지니어에게서 덜 감정적인 반응을 불러일으킨다. 따라서 최적이 아닌 설계의 영향이
  핵심 하위 도메인만큼 심각하지 않다** (13장, p.203).[^khononov2021]
- **전수 조사를 요구하지 않는다** (13장, p.203):[^khononov2021]

> You don't have to identify all of the core subdomains. It won't be practical or even possible to
> do so, even for a medium-sized company.

  - 대신 **전반 구조를 식별하되 지금 일하고 있는 소프트웨어 체계와 가장 관련이 깊은 하위
    도메인에 더 주의를 기울인다** (13장, p.203).[^khononov2021]
- 이 세 종류의 규정과 판별 어림법은 [하위 도메인의 세 종류](subdomain-types.md)에 있다.

## 현재 설계를 탐색한다

- 문제 공간을 안 다음 해법 공간으로 간다. **고수준 구성 요소(high-level components)부터
  시작하되 그 지위를 낮춰 잡는다** (13장, p.203):[^khononov2021]

> These are not necessarily bounded contexts in the DDD sense, but rather boundaries used to
> decompose the business domain into subsystems.

- **찾아야 할 성질이 하나로 특정된다** (13장, p.203):[^khononov2021]

> The characteristic property to look for is the components' decoupled lifecycles.

  - 저장소 구조에 속지 말라는 단서가 붙는다 — **서브시스템이 같은 소스 관리 저장소(모노레포)에
    관리되고 있거나 모든 구성 요소가 하나의 모놀리식 코드베이스에 있더라도, 어느 것이 다른 것과
    독립적으로 진화하고 테스트되고 배포될 수 있는지 확인하라** (13장,
    p.203).[^khononov2021]

## 전술 설계를 평가한다

- 고수준 구성 요소마다 **어떤 업무 하위 도메인을 담고 있고 어떤 기술적 설계 결정이 내려졌는지
  확인한다 — 업무 로직을 구현하는 데 어떤 패턴이 쓰였고 그 구성 요소의 아키텍처를 정의하는
  데 어떤 패턴이 쓰였는가** (13장, p.204).[^khononov2021]
- **그다음 그 둘을 대질한다** — **해법이 문제의 복잡성에 맞는가? 더 정교한 설계 패턴이 필요한
  영역이 있는가? 반대로 대충 넘어가거나 기존 기성 해법을 쓸 수 있는 하위 도메인이 있는가?**
  (13장, p.204).[^khononov2021]
  - **이 대질이 10장의 판정 사슬을 반대 방향으로 쓰는 것이다.** 10장은 하위 도메인의 종류에서
    패턴을 도출했고, 여기서는 **실제로 쓰인 패턴**을 관찰해 분류와 맞는지 본다. 그 사슬은
    [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.

## 전략 설계를 평가한다

- **현재의 컨텍스트 지도를 그린다** (13장, p.204):[^khononov2021]

> Use the knowledge of the high-level components to chart the current design's context map, as
> though these high-level components were bounded contexts.

  - 그 위에서 **구성 요소 사이의 관계를 경계 컨텍스트 통합 패턴의 어휘로 식별하고 추적한다**
    (13장, p.204).[^khononov2021] 그 어휘는
    [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)이고 지도 자체는
    [컨텍스트 지도](../concepts/context-map.md)다.
- **그 지도에서 읽어 낼 나쁜 신호가 다섯이다** (13장, p.204).[^khononov2021]
  - **여러 팀이 같은 고수준 구성 요소에서 일하고 있다**(Multiple teams working on the same
    high-level component).
  - **핵심 하위 도메인의 구현이 중복되어 있다**(Duplicate implementations of core subdomains).
  - **핵심 하위 도메인을 외주 회사가 구현하고 있다.**
  - **통합이 자주 실패해 마찰이 생긴다.**
  - **외부 서비스와 레거시 체계에서 어색한 모델이 번져 나오고 있다**(Awkward models spreading
    from external services and legacy systems).
- **그리고 마지막으로 잃어버린 도메인 지식을 찾는다** — 이 통찰들이 현대화 전략을 계획하는
  좋은 출발점이지만, 먼저 문제 공간과 해법 공간을 더 깊이 안 상태에서 **잃어버린 도메인
  지식을 찾으라**는 것이다. 그 문제는 **핵심 하위 도메인에서 널리 퍼져 있고 심각한데, 거기서
  업무 로직이 복잡하면서 동시에 업무에 결정적이기 때문이다.** 그런 경우를 만나면 **이벤트스토밍
  세션을 진행해 지식을 되찾으려 시도하고, 그 세션을 유비쿼터스 언어를 기르는 기반으로도 쓰라**
  (13장, p.204).[^khononov2021] 그 워크숍은 [이벤트스토밍](eventstorming.md)이다.

## 현대화 전략 — 크게 생각하고 작게 시작한다

- **경고가 먼저다** (13장, p.204):[^khononov2021]

> The "big rewrite" endeavors, in which the engineers are trying to rewrite the system from
> scratch, this time designing and implementing the whole system correctly, are rarely successful.

  - 거기에 조직 쪽 사실이 붙는다 — **경영진이 그런 아키텍처 대수술을 지지하는 일은 더욱 드물다**
    (13장, p.204).[^khononov2021]
- **대안이 표어로 주어진다** (13장, p.205):[^khononov2021]

> A safer approach to improving the design of existing systems is to think big but start small. As
> Eric Evans says, not all of a large system will be well designed.

  - **저자가 원전을 여기서 직접 부른다.** 큰 체계 전부가 잘 설계되지는 않는다는 것은 원전의
    증류 논증이 서 있는 전제이고, 그 전문은 [핵심 도메인](../concepts/core-domain.md)과
    [전략 설계](../concepts/strategic-design.md)에 있다. **그것을 받아들인 뒤에 어디에 투자할지
    전략적으로 정하는 것**이 이 절의 일이다 (13장, p.205).[^khononov2021]
- **선행 조건이 경계다. 다만 물리 경계일 필요는 없다** (13장, p.205):[^khononov2021]

> start by ensuring that at least the logical boundaries (namespace, modules, and packages,
> depending on the technology stack) are aligned with the subdomains' boundaries

  - **이 첫걸음이 안전하다는 근거가 명시된다** (13장, p.205):[^khononov2021]

> Adjusting the system's modules is a relatively safe form of refactoring. You are not modifying
> the business logic, just repositioning the types in a more well-organized structure.

  - 다만 단서가 둘이다 — **전체 타입 이름으로 참조하는 곳(라이브러리의 동적 로딩, 리플렉션
    등)이 깨지지 않는지 확인하라**, 그리고 **하위 도메인의 업무 로직이 다른 코드베이스에
    구현되어 있는 것을 놓치지 마라 — 데이터베이스의 저장 프로시저, 서버리스 함수 등이다.**
    저장 프로시저라면 **속한 모듈을 반영하도록 이름을 바꾸거나 전용 데이터베이스 스키마를
    만들어 옮기라** (13장, p.205).[^khononov2021]

## 전략적 현대화 — 논리 경계를 물리 경계로

- **조급한 분해를 경계한다** — 10장에서 논했듯 **가능한 한 작은 경계 컨텍스트로 체계를 미리
  분해하는 것은 위험할 수 있다.** 대신 **논리 경계를 물리 경계로 바꿔서 가장 큰 값을 얻을 수
  있는 자리를 찾는다** (13장, p.205).[^khononov2021] 그 어림법은
  [경계 컨텍스트](../concepts/bounded-context.md)에 있다.
- **승격을 결정하는 두 물음이다** (13장, p.206).[^khononov2021]

> Are multiple teams working on the same codebase? If so, decouple the development lifecycles by
> defining bounded contexts for each team.

> Are conflicting models being used by the different components? If so, relocate the conflicting
> models into separate bounded contexts.

  - **두 물음이 경계 컨텍스트 패턴의 두 근거를 그대로 되풀이한다** — 모델의 충돌과 팀 하나에
    컨텍스트 하나. 그 조항들은 [경계 컨텍스트](../concepts/bounded-context.md)에 있다.
- **최소한의 경계가 서면 그다음은 관계다** — 서로 다른 경계 컨텍스트에서 일하는 팀들이 어떻게
  소통하고 협업하는지 보고, **특히 임시방편이나 공유 커널 같은 통합으로 소통하고 있을 때 그
  팀들이 공유 목표와 적절한 협업 수준을 갖고 있는지** 묻는다 (13장, p.206).[^khononov2021]
- **통합 패턴이 푸는 문제 넷이 목록으로 주어진다** (13장, pp.206–207).[^khononov2021]
  - **고객과 공급자 관계** — 11장에서 보았듯 조직의 성장이 이전의 소통·협업 방식을 무효로 만들
    수 있다. **여러 공학 팀의 파트너십 관계를 전제로 설계되었으나 그 파트너십이 더는 지속
    가능하지 않은 구성 요소를 찾아 적절한 종류의 고객·공급자 관계(순응주의자, 부패 방지 계층,
    또는 열린 호스트 서비스)로 리팩터링하라.**
  - **부패 방지 계층** — **레거시 체계에서 경계 컨텍스트를 보호하는 데 쓸모 있고, 특히 레거시
    체계가 비효율적인 모델을 써서 그것이 하류 구성 요소로 번지는 경향이 있을 때 그렇다.**
    그리고 둘째 쓰임이 **자기가 쓰는 상류 서비스의 공개 인터페이스가 자주 바뀌는 것에서 경계
    컨텍스트를 보호하는 것**이다.
  - **열린 호스트 서비스** — **한 구성 요소의 구현 세부 변경이 체계를 타고 번져 소비자에게
    영향을 주는 일이 잦으면 그것을 열린 호스트 서비스로 만드는 것을 고려하라. 구현 모델을 그것이
    노출하는 공개 API에서 떼어 내는 것이다.**
  - **각자의 길** — **특히 큰 조직에서는 공유 기능을 함께 진화시켜야 하는 데서 오는 공학 팀
    사이의 마찰을 만날 수 있다. 그 "불화의 사과" 기능이 업무에 결정적이지 않다면, 곧 핵심
    하위 도메인이 아니라면, 팀들은 각자의 길을 가서 각자 자기 해법을 구현하고 마찰의 원인을
    없앨 수 있다.**
  - 이 넷의 전문은 [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)과
    [부패 방지 계층](../concepts/anticorruption-layer.md)에 있다.

## 전술적 현대화 — 가장 아픈 불일치부터

- 우선순위가 하나로 정해진다 (13장, p.207):[^khononov2021]

> look for the most "painful" mismatches in business value and implementation strategies, such as
> core subdomains implementing patterns that don't match the complexity of the model—transaction
> script or active record

  - 그 자리가 왜 가장 아픈지가 붙는다 — **업무의 성공에 직접 영향을 주는 이 구성 요소들은 가장
    자주 바뀌어야 하면서도 나쁜 설계 탓에 유지하고 진화시키기가 고통스럽다** (13장,
    p.207).[^khononov2021]
  - **11장이 같은 신호를 반대편에서 읽는다** — 그쪽은 아픔을 **하위 도메인의 종류가 바뀌었다는
    표지**로 읽고, 여기서는 **어디부터 손댈지의 우선순위**로 읽는다. 같은 관찰의 두 쓰임이다.

## 유비쿼터스 언어를 기른다

- 선행 조건이 지식이다 (13장, p.207):[^khononov2021]

> A prerequisite to the successful modernization of a design is the domain knowledge and effective
> model of the business domain.

- **그 지식을 얻는 지름길로 이벤트스토밍이 지목된다** (13장, p.207):[^khononov2021]

> Use EventStorming to build a ubiquitous language with the domain experts and explore the legacy
> codebase, especially if the codebase is an undocumented mess that no one truly understands.

  - 그리고 문장 하나로 못 박는다 — **이벤트스토밍은 도메인 지식을 되찾는 환상적인 도구다**
    (13장, p.207).[^khononov2021]
- 지식과 모델을 갖춘 다음에야 **문제의 업무 기능에 어떤 업무 로직 구현 패턴이 가장 맞는지
  정하고**, 그 출발점으로 10장의 설계 휴리스틱을 쓴다 (13장, p.207).[^khononov2021]

## 두 갈래 — 갈아 치우기와 고쳐 쓰기

- 그다음 결정이 현대화 전략의 갈래다 — **체계의 구성 요소 전체를 점진적으로 교체하는 것
  (교살자 패턴)인가, 아니면 기존 해법을 점진적으로 리팩터링하는 것인가** (13장,
  p.207).[^khononov2021]
- **교살자 쪽의 서술은 이 KB의 다른 페이지에 있다** —
  [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md)가 그
  자리이고, 그곳이 같은 패턴에 대한 세 소스의 서술을 모은다. 이 판본이 더하는 것은 파사드와의
  결합, 그리고 경계 컨텍스트 하나에 데이터베이스 하나라는 규칙을 이행 기간에만 느슨하게 하는
  조건이다.
- **리팩터링 쪽의 조항 둘은 전술 패턴 페이지에 있다** (13장, p.210).[^khononov2021]
  - **트랜잭션 스크립트나 액티브 레코드를 이벤트 소싱 도메인 모델로 곧장 리팩터링하지 말라**는
    금지와 상태 기반 애그리게이트라는 중간 단계.
  - **도메인 모델로 가는 리팩터링이 원자적 변경일 필요가 없고 값 객체부터 찾아 들이라**는 지침.
  - 전문은 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.
- **마지막으로 레거시를 상대하는 두 장치가 다시 불려 나온다** — **레거시 체계를 리팩터링할 때
  필요하면 부패 방지 계층으로 새 코드베이스를 옛 모델에서 보호하고, 열린 호스트 서비스를
  구현해 공표된 언어를 노출함으로써 소비자를 레거시 코드베이스의 변경에서 보호하라** (13장,
  p.210).[^khononov2021]

## 실용적 도메인 주도 설계

- 조항 (13장, pp.210–211):[^khononov2021]

> As long as you analyze your business domain and its strategy, look for effective models to solve
> particular problems, and most importantly, make design decisions based on the business domain's
> needs: that's domain-driven design!

  - 그 앞에 허용이 있다 — **어떤 이유로든 전술 패턴이 당신에게 맞지 않을 수 있다. 특정 도메인에서
    다른 설계 패턴이 더 잘 통하거나 그냥 다른 패턴이 더 효과적이라고 느껴서 쓰기를 선호할 수도
    있다. 그래도 완전히 괜찮다!** (13장, p.210).[^khononov2021]
- **그리고 방법론의 정의가 이름으로 되돌아간다** (13장, p.211):[^khononov2021]

> It's worth reiterating that domain-driven design is not about aggregates or value objects.
> Domain-driven design is about letting your business domain drive software design decisions.

  - **이 문장이 이 책의 제목과 서론을 회수한다.** 방법론 이름의 어원을 "(business)
    domain-driven (software) design"으로 푸는 자리는
    [전략 설계](../concepts/strategic-design.md)에 있다.
- **맺음말이 그 허용을 브라운필드에 명시적으로 건다** (맺음말 §Conclusion,
  p.271):[^khononov2021]

> Understanding the philosophy of domain-driven design is also the key to leveraging value by
> incorporating the methodology's concepts individually, especially in brownfield projects.

  - **"개념을 하나씩 들인다"가 이 페이지의 조건이다.** 이미 돌아가는 체계에서는 방법론을 한
    덩어리로 도입할 수 없으므로, 위 [두 가지 오해를 먼저 걷어 낸다](#두-가지-오해를-먼저-걷어-낸다)와
    이 절의 허용이 그대로 절차의 전제가 된다. 저자가 그 전제에 붙이는 조건은 **원리를
    이해하라**는 것 하나다 — 무엇을 남기고 무엇을 뺄지는 그 이해가 정한다.
  - 같은 맺음말이 방법론 전체에 거는 조항(교리로 따르지 말고 근거를 이해하라)은
    [전략 설계](../concepts/strategic-design.md)에 있다.

## 잠행 DDD — 권위 대신 논리로

- 문제 설정이 조직에 있다 — 저자는 학회에서 **"다 좋은데, 팀과 경영진에게 도메인 주도 설계를
  어떻게 '팔죠?'"**라는 질문을 거의 매번 받는다고 적고, **설계가 곧 파는 일**이라고 답한다.
  다만 **이렇게 넓은 범위의 설계 결정을 다루고 공학 영역 밖의 다른 이해관계자까지 관여시키는
  방법론은 팔기가 극도로 어렵다** (13장, p.211).[^khononov2021]
- **경영진의 지지가 필요하다는 것은 인정한다** (13장, p.211):[^khononov2021]

> Management support is essential for making any considerable changes in an organization.

  - 그러나 최고 경영진이 이미 DDD를 알거나 그 업무 가치를 배우는 데 시간을 들일 의향이
    없다면 그것은 그들의 관심사가 아니고, **특히 DDD가 수반하는 공학 프로세스의 변화가 커
    보이기 때문**이다. 그리고 결론이 뒤집힌다 — **그렇다고 도메인 주도 설계를 쓸 수 없다는
    뜻은 아니다** (13장, p.211).[^khononov2021]
- **처방 (13장, p.211):**[^khononov2021]

> Make domain-driven design a part of your professional toolbox, not an organizational strategy.
> DDD's patterns and practices are engineering techniques, and since software engineering is your
> job, use them!

- **유비쿼터스 언어부터다** — 이 관행이 **도메인 주도 설계의 초석**이고 **거의 상식에 가까울
  만큼 사소하다.** 실천이 넷이다 (13장, pp.211–212).[^khononov2021]
  - **이해관계자가 업무 도메인을 말할 때 쓰는 언어를 주의 깊게 들어라.** 그리고 **용어를 기술
    용어에서 업무적 의미 쪽으로 부드럽게 몰아가라**(Gently steer the terminology away from
    technical jargon and toward its business meaning).
  - **일관되지 않은 용어를 찾아 설명을 구하라**(Look for inconsistent terms and ask for
    clarifications). 같은 것에 이름이 여럿이면 이유를 찾는다 — **다른 모델들이 같은 해법에
    얽혀 있는가? 컨텍스트를 찾아 명시적으로 만들라. 뜻이 같다면 상식을 따라 한 용어를 쓰자고
    청하라.**
  - **도메인 전문가와 최대한 소통하라** — **이 노력이 반드시 공식 회의를 요구하지는 않는다.
    정수기 앞과 커피 브레이크가 훌륭한 소통 촉진제다.** 그리고 격려가 붙는다 — **걱정하지
    마라, 도메인 전문가는 대개 문제 영역을 진심으로 배우고 싶어 하는 엔지니어와 협업하기를
    기뻐한다!**
  - **무엇보다 코드와 모든 프로젝트 관련 소통에 유비쿼터스 언어를 쓰라. 인내하라**(Most
    importantly, use the ubiquitous language in your code and all project-related communication.
    Be patient.). **조직에서 한동안 쓰여 온 용어를 바꾸는 데는 시간이 걸리지만 결국 자리를
    잡을 것이다.**
- **경계 컨텍스트는 패턴 이름 대신 원리로 설명한다** — 분해 방안을 탐색할 때 이 패턴이 기대는
  원리로 돌아가라는 것이고, 세 물음이 주어진다 (13장, p.212).[^khononov2021]

> Why is it better to design problem-oriented models instead of a single model for all use cases?
> Because "all-in-one" solutions are rarely effective for anything.

> Why can't a bounded context host conflicting models? Because of the increased cognitive load and
> solution complexity.

> Why is it a bad idea for multiple teams to work on the same codebase? Because of friction and
> hindered collaboration between the teams.

  - 통합 패턴에도 같은 추론을 쓴다 — **패턴마다 무엇을 풀려는 문제인지 확실히 이해하라**
    (13장, p.212).[^khononov2021]
- **전술 패턴에서는 권위에 호소하지 말라는 금지가 나온다** (13장, p.212):[^khononov2021]

> When discussing tactical design patterns, don't appeal to authority: "Let's use an aggregate
> here because the DDD book says so!" Instead, appeal to logic.

  - 그 "논리"의 목록이 여섯이다 (13장, pp.212–213).[^khononov2021]

> Why are explicit transactional boundaries important? To protect the consistency of the data.

> Why can't a database transaction modify more than one instance of an aggregate? To ensure that
> the consistency boundaries are correct.

> Why can't an aggregate's state be modified directly by an external component? To ensure that all
> the related business logic is colocated and not duplicated.

  - 넷째는 저장 프로시저에 걸린다 — **애그리게이트의 기능 일부를 저장 프로시저로 떼어 내면 안
    되는 이유는? 어떤 로직도 중복되지 않게 하기 위해서다. 중복된 로직은, 특히 체계의 논리적·물리적으로
    먼 구성 요소에 있을 때, 어긋나서 데이터 손상으로 이어지는 경향이 있다.**

> Why should we strive for small aggregate boundaries? Because wide transactional scope will both
> increase the complexity of the aggregate and negatively impact the performance.

> Why, instead of event sourcing, can't we just write events to a logfile? Because there are no
> long-term data consistency guarantees.

  - **이 여섯 물음이 6·7장의 조항들을 근거 쪽에서 되짚은 것이다.** 각각의 전문은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)와
    [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)에 있다.
- **이벤트 소싱 도메인 모델에는 별도의 수가 붙는다** — **그 많은 이점에도 이벤트 소싱은 많은
  사람에게 너무 급진적으로 들린다.** 해법은 역시 업무 도메인이 결정하게 두는 것이다 (13장,
  p.213):[^khononov2021]

> Talk to domain experts. Show them the state- and event-based models. Explain the differences and
> the advantages offered by event sourcing, especially with regard to the dimension of time.

  - 그 결과에 대한 저자의 예측 — **대개 그들은 그것이 주는 통찰의 수준에 열광하며 스스로 이벤트
    소싱을 옹호할 것이다.** 그리고 덧붙임 — **도메인 전문가와 상호작용하는 동안 유비쿼터스
    언어 작업을 잊지 마라!** (13장, p.213).[^khononov2021]

## 같은 현대화를 마이크로서비스 쪽에서 세운 소스

**[newman2021](../sources/newman2021.md) 3장이 이 페이지와 같은 물음을 마이크로서비스 어휘로
던진다 — 이미 돌아가는 모놀리스를 어떻게 바꿔 나가는가.** 겹치는 자리와 이 페이지에 없는 자리가
뚜렷하다.

- **겹치는 것 하나 — 큰 재작성의 기각.** 위
  [현대화 전략 — 크게 생각하고 작게 시작한다](#현대화-전략--크게-생각하고-작게-시작한다)의 경고를
  그쪽도 낸다. 그쪽은 마틴 파울러를 인용해 **큰 한 방 재작성을 하면 보장되는 것은 큰 한 방뿐**
  이라 적고, 처방을 **모놀리스를 조금씩 깎아 내며 한 번에 한 조각씩 뽑아내라**로 둔다 (3장
  §"Incremental Migration", p.72).[^newman2021] 직인용과 전문은
  [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md)에 있다.
- **이 페이지에 없던 것 — 목표를 먼저 정하라는 조항.** 그쪽은 절차의 첫 물음을 **무엇을 바꾸려
  하는가**로 둔다. **마이크로서비스는 목표가 아니고**, 채택은 의식적 결정이어야 하며, **현재
  아키텍처로 최종 목표에 다가갈 더 쉬운 길을 찾지 못할 때에만** 이행을 생각해야 한다 (3장
  §"Have a Goal", p.71).[^newman2021]
  - **이것이 위 [전략 분석 — 업무 도메인을 이해한다](#전략-분석--업무-도메인을-이해한다)와
    겨루는가. 겨루지 않고 층이 다르다.** 이 페이지의 전략 분석은 **어디를 고칠 것인가**를 업무
    도메인의 지도에서 찾고, 그쪽의 첫 물음은 **고쳐서 무엇을 얻으려 하는가**를 묻는다. 그쪽의
    물음이 앞서고, 답이 "확장"이면 **로드 밸런서 뒤에 모놀리스 사본을 더 띄우는 것 같은 더 쉬운
    길**이 먼저 검토된다 (3장, pp.71–72).[^newman2021] 곧 **그쪽은 이 절차 전체를 하지 않을
    근거까지 물음에 넣는다.**
  - 위 [두 가지 오해를 먼저 걷어 낸다](#두-가지-오해를-먼저-걷어-낸다)가 "이 방법론을 언제
    쓰는가"에 답한다면, 그쪽의 조항은 **"이 이행을 아예 하지 않는 선택"**을 같은 자리에 둔다.
- **이 페이지에 없던 것 둘 — 모놀리스가 남는다는 전제.** 그쪽은 이행 뒤에도 **기존 모놀리식
  아키텍처가 줄어든 역할로 남는 것이 흔하다**고 적고, 점진적 여정으로 만들면 **언제 멈출지를 알
  수 있다**는 것을 이득으로 센다 (3장 §"The Monolith Is Rarely the Enemy", p.73).[^newman2021]
  - **위 [두 갈래 — 갈아 치우기와 고쳐 쓰기](#두-갈래--갈아-치우기와-고쳐-쓰기)의 교살자 갈래와
    대질하면 방향이 같다** — 교살자 쪽도 숙주가 죽을 때까지 두 체계가 공존하는 기간을 전제한다.
    다만 그쪽의 교살자 서술은 **숙주의 죽음을 종점으로** 두고, 이 소스는 **종점이 없을 수도
    있다**고 적는다. 어느 쪽이 옳은가의 물음이 아니라 **목표가 무엇이었는가에 달린 것**이고,
    그것이 위 목표 조항이 앞서는 이유다. **모순 쌍으로 세우지 않았다.**
- **분해의 실행 장치와 데이터 쪽 문제는 이 페이지가 갖지 않는다** — 무엇을 먼저 뽑고 어떤 장치로
  옮기는가는 [모놀리스 분해 패턴](../concepts/monolith-decomposition-patterns.md)에, 데이터베이스를
  쪼갤 때 깨지는 것들은
  [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md)에 있다.

## 원전의 첫째 필수와 잠행이 양립하는가

[evans2003](../sources/evans2003.md)의 17장은 전략 설계 결정이 갖춰야 할 여섯 가지 필수를
세우고 그 첫째가 **"Decisions must reach the entire team"**이다 (17장,
p.492).[^evans2003] 위 [잠행 DDD](#잠행-ddd--권위-대신-논리로)는 조직의 승인 없이 개인이
쓰라고 한다. **겉보기에 반대이고, 분석 결과 모순으로 세우지 않았다.**

- **대상이 다르다.** 원전의 조항이 걸리는 것은 **전략 설계 결정** — 대규모 구조, 증류의 결과,
  경계와 그 관계 — 이고, 그것은 정의상 여러 팀의 코드를 동시에 구속하므로 모두에게 닿지 않으면
  무의미하다. 이 판본의 잠행 목록에서 개인이 혼자 할 수 있는 것은 **관행**(업무 용어를 듣고
  쓰기, 도메인 전문가와 말하기, 자기 코드에 그 말을 쓰기)이고, 공유 결정에 닿는 자리
  (경계 컨텍스트, 전술 패턴)에서는 **팀에게 원리를 설명하라**고 지시한다. 곧 잠행은 결정을
  숨기라는 것이 아니라 **방법론의 이름을 앞세우지 말라**는 것이다.
- **권위에 대한 판정이 오히려 같은 방향이다.** 원전의 첫째 필수는 중앙 아키텍처 팀에 공식
  권한을 주는 반응을 함정으로 지목하고 이렇게 적는다 — **어떤 체계이든, 경영진이 부여한 권위보다
  개발자가 그 전략과 맺는 실제 관계에 더 신경 쓰라** (17장, p.492).[^evans2003] 이 판본의
  **권위에 호소하지 말고 논리에 호소하라**는 금지가 그 문장의 실무판이다. 두 소스 모두
  **관리자의 승인이 채택의 기제가 아니라고** 말한다.
- **남는 차이는 출발점이다.** 원전은 결정이 이미 조직 수준에서 내려진다고 전제하고 그 결정이
  팀에 닿는 방식을 다루며, 이 판본은 **그 전제가 없는 조직에서 한 사람이 무엇부터 할 수
  있는가**를 다룬다. 두 서술을 겹쳐 읽으면 잠행 DDD의 도달점이 원전의 첫째 필수다 — 논리로
  설득해 팀이 실제로 그 전략과 관계를 맺게 하는 것.
- 원전 쪽 전문은 [전략 설계 결정하기](../concepts/strategic-decision-making.md)에 있다.

## 이어지는 페이지

- [하위 도메인의 세 종류](subdomain-types.md) — 전략 분석이 산출하는 분류
- [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md) — 조직도에서 시작하는 절차
- [컨텍스트 지도](../concepts/context-map.md) — 현재 설계를 그리는 도구
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md) — 현대화가 고르는 관계들
- [부패 방지 계층](../concepts/anticorruption-layer.md) — 레거시를 마주하는 장치
- [경계 컨텍스트](../concepts/bounded-context.md) — 논리 경계를 물리 경계로 올리는 단위
- [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md) — 전술 현대화의 판정과
  이행 경로
- [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md) —
  교살자 갈래의 전문
- [모놀리스 분해 패턴](../concepts/monolith-decomposition-patterns.md) — 같은 현대화를
  마이크로서비스 쪽에서 실행하는 장치들
- [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md) — 그 분해가
  데이터베이스에 청구하는 것
- [이벤트스토밍](eventstorming.md) — 잃어버린 지식을 되찾는 워크숍
- [성장이 낳는 복잡성](growth-driven-complexity.md) — 진흙 공이 생기는 기제
- [스마트 UI 안티패턴](smart-ui-antipattern.md) — 이 방법론을 쓰지 않는 것이 옳은 갈림길
- [전략 설계 결정하기](../concepts/strategic-decision-making.md) — 원전이 같은 물음에 답하는 자리
- [모델 리팩터링 절차](../concepts/model-refactoring-process.md) — 모델을 고쳐 나가는 원전의 절차
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 13장 "Domain-Driven Design in the Real World"
    전량(pp.201–213, 연습문제 pp.214) — §"Strategic Analysis"(pp.202–204) ·
    §"Modernization Strategy"(pp.204–210) · §"Pragmatic Domain-Driven Design"(pp.210–211) ·
    §"Selling Domain-Driven Design"(pp.211–213). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다.
    원문이 용어의 첫 등장과 목록 표제를 기울임으로 조판하는 관례는 직인용에서 별도로 표시하지
    않았다. 도판 다섯(Figure 13-1~13-5)은 도판이라 본문이 그것에 대해 적는 것만 산문으로
    옮겼다 — 13-3은 목 졸라 죽이는 무화과나무 사진이다. 이 장에는 코드 목록이 없다.
    **§"Strangler pattern"(pp.208–209)과 §"Refactoring tactical design decisions"(p.210)의
    본체는 이 페이지에 두지 않았다** — 앞은 같은 패턴의 다른 소스 서술이 이미 모여 있는
    [아키텍처를 점진적으로 들이기](../concepts/adopting-architecture-incrementally.md)에,
    뒤는 이행 경로가 사는
    [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 두었다. 같은 claim을
    두 페이지에 흩지 않는다. 장 끝 연습문제 넷(p.214)은 claim이 아니라 옮기지 않았다.
    **맺음말 §Conclusion(p.271)의 한 문장도 이 페이지에 합류했다** — 방법론의 개념을 하나씩
    들이는 것이 특히 브라운필드에서 값을 낸다는 조항이다. 같은 절의 나머지(교리로 따르지
    말라는 조항과 마지막 당부)는 [전략 설계](../concepts/strategic-design.md)와
    [유비쿼터스 언어](../concepts/ubiquitous-language.md)에 두었다. 이 방법론을 창업일부터
    적용한 회사의 기록은 [마켓노버스 사례 연구](marketnovus-case-study.md)에 있다 — 그쪽은
    그린필드에서 출발하므로 이 페이지의 조건(이미 돌아가는 체계)과 대비된다.

[^newman2021]: Newman 2021, 3장 "Splitting the Monolith" §"Have a Goal"(pp.71–72) ·
    §"Incremental Migration"(p.72) · §"The Monolith Is Rarely the Enemy"(p.73).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 이 절에는 직인용이 없다 — 대질에 필요한
    것만 산문으로 들었고, 직인용과 전문은
    [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md)와
    [모놀리스와 모듈](../concepts/monolith-versus-modular.md)이 갖는다. 이 절에는 코드
    목록도 도판도 없다.

[^evans2003]: Evans 2003, 17장 "Bringing the Strategy Together" §"Six Essentials for Strategic
    Design Decision Making" 중 첫째 필수(p.492). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측).
    원문이 처방문을 기울임으로 조판하는 관례는 직인용에서 별도로 표시하지 않았다. 나머지
    다섯 필수의 전문은 [전략 설계 결정하기](../concepts/strategic-decision-making.md)에 있다.

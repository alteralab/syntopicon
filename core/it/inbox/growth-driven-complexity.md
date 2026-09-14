---
type: concept
title: 성장이 낳는 복잡성
description: 기능이 계속 늘어나는 것이 건강의 표지이면서 동시에 큰 진흙 공으로 가는 길인 이유와 그 길을 막기 위해 어떤 경계를 어떤 주기로 되짚는가 — 푸트와 요더의 큰 진흙 공 규정과 규제되지 않은 성장이 설계 결정을 재평가하지 않은 채 기능만 늘린 결과라는 진단, 우발적 복잡성은 없애고 본질적 복잡성만 도구로 관리하라는 지도 원리, 그리고 하위 도메인과 경계 컨텍스트와 애그리게이트라는 세 경계를 같은 순서로 되짚는 절차 — 완벽한 경계가 아니라 쓸모 있는 경계를 노리고 정합적 유스 케이스로 더 잘게 쪼갤 자리를 찾는 것, 만능이 되어 가는 컨텍스트와 수다스러워지는 컨텍스트라는 두 증상, 새 기능을 기존 애그리게이트에 얹는 편의가 강한 일관성이 필요 없는 데이터를 끌어들이는 자리와 그 추출이 숨은 모델을 드러내는 연쇄
generated: { by: "claude-opus-5", at: "2026-09-15T12:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 성장이 낳는 복잡성

- [성장은 건강의 표지다](#성장은-건강의-표지다)
- [큰 진흙 공이 무엇인가](#큰-진흙-공이-무엇인가)
- [지도 원리 — 우발적인 것만 없앤다](#지도-원리--우발적인-것만-없앤다)
- [되짚는 순서는 분석과 같다](#되짚는-순서는-분석과-같다)
- [하위 도메인을 되짚는다](#하위-도메인을-되짚는다)
- [경계 컨텍스트를 되짚는다](#경계-컨텍스트를-되짚는다)
- [애그리게이트를 되짚는다](#애그리게이트를-되짚는다)
- [세 줄로 요약된 처방](#세-줄로-요약된-처방)
- [14장이 복잡성을 국소와 전역으로 가른다](#14장이-복잡성을-국소와-전역으로-가른다)
- [책의 사례 — 우발적 복잡성이 설계 쪽에서 나온 경우](#책의-사례--우발적-복잡성이-설계-쪽에서-나온-경우)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **기능이 계속 늘어나는 것이 설계를 어떻게 망가뜨리며, 그것을 막기 위해 어떤
경계를 되짚는가.**

## 성장은 건강의 표지다

- 출발점이 성장을 나쁜 것으로 세우지 않는다 — **성장은 건강한 체계의 표지다. 새 기능이 계속
  더해진다는 것은 그 체계가 성공적이라는 표지다. 사용자에게 값을 주고 있고, 사용자의 필요를
  더 다루고 경쟁 제품을 따라잡기 위해 확장되고 있는 것이다** (11장, p.180).[^khononov2021]
- **그리고 곧바로 이면이 붙는다** — **그러나 성장에는 어두운 면이 있다. 소프트웨어 프로젝트가
  자라면 그 코드베이스는 큰 진흙 공으로 자랄 수 있다** (11장, p.180).[^khononov2021]

## 큰 진흙 공이 무엇인가

- 저자가 원전 논문의 규정을 인용한다 (11장, p.180):[^khononov2021]

> A big ball of mud is a haphazardly structured, sprawling, sloppy, duct-tape-and-baling-wire,
> spaghetti-code jungle. These systems show unmistakable signs of unregulated growth, and
> repeated, expedient repair.

  - 저자가 대는 출처는 Brian Foote와 Joseph Yoder의 "Big Ball of Mud"(PLoP '97/EuroPLoP '97,
    1997)이고 **이 KB가 확인한 원전은 아니다** (11장, p.180 각주 1).[^khononov2021]
- **원인이 특정된다** (11장, p.180):[^khononov2021]

> The unregulated growth that leads to big balls of mud results from extending a software
> system's functionality without re-evaluating its design decisions.

- **왜 이 방법론에 특히 걸리는지도 적힌다** — **성장은 구성 요소의 경계를 터뜨려 그 기능을
  점점 넓힌다. 성장이 설계 결정에 미치는 영향을 살피는 것이 결정적인데, 많은 도메인 주도 설계
  도구가 전부 경계를 긋는 일이기 때문이다 — 업무의 구성 블록(하위 도메인), 모델(경계 컨텍스트),
  불변성(값 객체), 일관성(애그리게이트)** (11장, p.180).[^khononov2021]

## 지도 원리 — 우발적인 것만 없앤다

- 처방의 축이 하나다 (11장, p.180):[^khononov2021]

> The guiding principle for dealing with growth-driven complexity is to identify and eliminate
> accidental complexity: the complexity caused by outdated design decisions. The essential
> complexity, or inherent complexity of the business domain, should be managed using
> domain-driven design tools and practices.

  - **우발적 복잡성의 규정이 이 판본 안에서 일관된다.** 같은 장의 앞부분이 보조 하위 도메인의
    복잡성이 수익에 영향을 주지 않으면서 늘 때 그것을 **우발적 업무 복잡성**이라 부르고,
    이 절은 **낡은 설계 결정이 낳은 복잡성**을 같은 이름으로 부른다 (11장,
    pp.171·180).[^khononov2021] 대상은 업무 쪽과 설계 쪽으로 다르지만 판정 형태는 같다 —
    **값을 내지 않는 복잡성은 없앤다.**
  - 같은 이분법을 다른 소스가 다루는 자리는
    [복잡성의 렌즈 적용하기](../synthesis/applying-the-complexity-lens.md)와
    [복잡성과 모듈 설계](../synthesis/complexity-and-modular-design.md)다.

## 되짚는 순서는 분석과 같다

- 저자가 절차를 앞 장들의 순서에 맞춘다 — DDD를 논할 때 **먼저 업무 도메인과 그 전략적 구성
  요소를 분석하고, 업무 도메인의 관련 모델을 설계하고, 그 모델을 코드로 설계하고 구현하는
  과정을 따른다.** 성장이 낳는 복잡성도 **같은 각본을 따르자**는 것이다 (11장,
  p.180).[^khononov2021]
- 그래서 아래 세 절이 하위 도메인 → 경계 컨텍스트 → 애그리게이트의 순서로 간다.

## 하위 도메인을 되짚는다

- 전제가 1장에서 온다 — **하위 도메인의 경계는 식별하기 어려울 수 있고, 그 결과 완벽한 경계를
  노리는 대신 쓸모 있는 경계를 노려야 한다**(instead of striving for boundaries that are
  perfect, we must strive for boundaries that are useful). 쓸모의 기준은 **서로 다른 업무
  가치를 가진 구성 요소를 식별하고 해법을 설계·구현할 적절한 도구를 쓸 수 있게 하는 것**이다
  (11장, pp.180–181).[^khononov2021]
- **성장이 그 경계를 흐린다** — 업무 도메인이 자라면 **하위 도메인의 경계는 더 흐려져 한
  하위 도메인이 여러 개의 더 잘게 나뉜 하위 도메인에 걸쳐 있는 경우를 알아보기 어려워진다.**
  그래서 처방이 나온다 (11장, p.181):[^khononov2021]

> it's important to revisit the identified subdomains and follow the heuristic of coherent use
> cases (sets of use cases working on the same set of data) to try to identify where to split a
> subdomain

  - **정합적 유스 케이스라는 어림법은 새로 나온 것이 아니다.** 1장이 하위 도메인 경계를 처음
    찾을 때 세운 멈춤 조건이 그것이고, 여기서는 그 같은 자를 **이미 그어 놓은 경계에 다시**
    댄다. 그 절차는
    [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md)에 있다.
- **쪼개서 얻는 것이 분류의 정밀도다** — 종류가 다른 더 잘게 나뉜 하위 도메인을 식별할 수
  있으면 **그것은 업무 도메인의 본질적 복잡성을 관리하게 해 주는 중요한 통찰이다. 하위
  도메인과 그 종류에 대한 정보가 정밀할수록 하위 도메인마다 기술적 해법을 고르는 일이 더
  효과적이 된다** (11장, p.181).[^khononov2021] 그 분류는
  [하위 도메인의 세 종류](subdomain-types.md)다.
- **핵심에 특히 걸린다** (11장, p.181):[^khononov2021]

> We should always aim to distill core subdomains as much as possible from all others so that we
> can invest our effort where it matters most from a business strategy perspective.

  - 같은 처방의 원전 층은 [핵심 도메인](../concepts/core-domain.md)과 증류 기법들이다.

## 경계 컨텍스트를 되짚는다

- 전제가 3장에서 온다 — 경계 컨텍스트 패턴은 **업무 도메인의 서로 다른 모델을 쓸 수 있게 해
  준다. "이것도 저것도 다 하지만 어느 것도 잘 못 하는" 모델을 짓는 대신 각각이 특정 문제를
  푸는 데 집중한 모델을 여럿 지을 수 있다** (11장, p.181).[^khononov2021]
- **성장이 그 초점을 잃게 한다** — 프로젝트가 진화하고 자라면 **경계 컨텍스트가 초점을 잃고
  서로 다른 문제에 관계된 로직을 쌓아 가는 일이 드물지 않다. 그것이 우발적 복잡성이다**
  (11장, p.181).[^khononov2021] 처방은 하위 도메인과 같은 형태다 (11장,
  p.181):[^khononov2021]

> Always look for opportunities to simplify the models by extracting bounded contexts that are
> laser focused at solving specific problems.

- **둘째 증상이 따로 있다** (11장, p.181):[^khononov2021]

> you may notice that a number of bounded contexts become increasingly "chatty" over time, unable
> to complete any operation without calling another bounded context. That can be a strong signal
> of an ineffective model and should be addressed by redesigning the bounded contexts' boundaries
> to increase their autonomy.

  - **이 증상은 성장이 숨은 문제를 드러내는 경우다** — 저자는 이것을 **기존의 암묵적 설계
    문제를 성장이 명시적으로 만드는 자리**로 규정한다 (11장, p.181).[^khononov2021]
  - **그래서 이 판본의 경계 어림법이 양방향이 된다.** 10장과 11장이 지식이 불확실할 때
    **넓게 시작하라**고 하고, 이 절은 자란 뒤에 **더 좁게 다시 그으라**고 한다. 겨루지
    않는다 — 앞은 처음 그을 때의 지침이고 뒤는 자란 뒤의 점검이다. 그 자리는
    [경계 컨텍스트](../concepts/bounded-context.md)에 있다.

## 애그리게이트를 되짚는다

- 전제가 6장의 원칙이다 (11장, p.182):[^khononov2021]

> The rule of thumb is to keep the aggregates as small as possible and include only objects that
> are required to be in a strongly consistent state by the business domain.

- **성장이 그 원칙을 비켜 간다** — 체계의 업무 요구사항이 자라면 **애그리게이트를 작게 유지한다는
  원칙을 다시 보지 않은 채 새 기능을 기존 애그리게이트에 분배하는 것이 "편리"할 수 있다**
  (11장, p.182).[^khononov2021] 그 결과의 판정 (11장, p.182):[^khononov2021]

> If an aggregate grows to include data that is not needed to be strongly consistent by all of
> its business logic, again, that's accidental complexity that has to be eliminated.

  - **판정 기준이 강한 일관성 하나다.** 크기 자체가 아니라 **그 데이터가 이 애그리게이트의
    모든 업무 로직에 대해 강하게 일관되어야 하는가**를 묻는다. 그 원칙의 전문은
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)에 있다.
- **추출이 한 단계 위까지 되먹인다** (11장, p.182):[^khononov2021]

> Extracting business functionality into a dedicated aggregate not only simplifies the original
> aggregate, but potentially can simplify the bounded context it belongs to. Often, such
> refactoring uncovers an additional hidden model that, once made explicit, should be extracted
> into a different bounded context.

  - **이 연쇄가 이 페이지의 세 절을 하나로 묶는다.** 애그리게이트를 쪼개다 숨은 모델이 나오고,
    그 모델이 새 경계 컨텍스트를 부른다 — 곧 전술 층의 점검이 전략 층의 결정으로 올라간다.
    같은 방향의 원전 서술은
    [암묵적 개념을 파내기](../concepts/digging-out-implicit-concepts.md)와
    [더 깊은 모델](../concepts/deep-model.md)에 있다.

## 세 줄로 요약된 처방

저자가 장 맺음에서 세 줄로 줄인다 (11장, pp.182–183).[^khononov2021]

- **하위 도메인의 기능이 넓어지면 더 나은 설계 결정을 내리게 해 줄 더 잘게 나뉜 하위 도메인
  경계를 식별해 보라.**
- **경계 컨텍스트가 "만물박사"가 되게 두지 마라**(Don't allow a bounded context to become a
  "jack of all trades."). **경계 컨텍스트가 감싸는 모델이 특정 문제를 푸는 데 집중되어 있는지
  확인하라.**
- **애그리게이트의 경계를 가능한 한 작게 유지하라. 강하게 일관된 데이터라는 어림법을 써서
  업무 로직을 새 애그리게이트로 추출할 가능성을 찾아내라**(Make sure your aggregates'
  boundaries are as small as possible. Use the heuristic of strongly consistent data to detect
  possibilities to extract business logic into new aggregates.).
- 그리고 마지막 말이 주기를 정한다 — **여러 경계를 성장이 낳는 복잡성의 표지가 있는지 계속
  점검하라. 우발적 복잡성을 없애도록 행동하고, 업무 도메인의 본질적 복잡성을 관리하는 데는
  도메인 주도 설계 도구를 쓰라** (11장, p.183).[^khononov2021]

## 14장이 복잡성을 국소와 전역으로 가른다

**같은 판본의 14장이 이 페이지의 복잡성 논의에 축을 하나 더 얹는다** — 복잡성이 어디에 있는가다.
위 [지도 원리](#지도-원리--우발적인-것만-없앤다)가 **어떤 복잡성을 없앨 것인가**(우발적인 것만)를
정했다면, 이 축은 **어느 층의 복잡성을 잴 것인가**를 정한다.

- 저자는 이 구분을 글렌퍼드 마이어스의 절차형 설계 논의에서 빌려 온다 — **국소 복잡성(local
  complexity)은 각 구성 요소 하나의 복잡성이고, 전역 복잡성(global complexity)은 체계 전체의
  복잡성**이다. 앞엣것은 그 구성 요소의 구현이 정하고, 뒤엣것은 구성 요소들 사이의 상호작용과
  의존이 정한다 (14장 §"System Complexity", p.221).[^khononov2021]
- **양 끝이 모두 실패한다** (14장, pp.221–222):[^khononov2021]
  - 전역 복잡성을 최소로 만드는 것은 쉽다 — 상호작용을 전부 없애고 한 덩어리로 구현하면 된다.
    그러나 그것이 **가능한 가장 높은 국소 복잡성**인 큰 진흙 공으로 가는 길이다.
  - 국소 복잡성만 최적화하고 전역 복잡성을 방치하면 **분산된 큰 진흙 공**이 된다.
  - 그러므로 **둘을 함께 최적화해야 하고**, 어느 한쪽만 최적화하는 설계 목표는 국소 최적이다.
- **이 축이 위 [큰 진흙 공이 무엇인가](#큰-진흙-공이-무엇인가)에 짝을 준다.** 이 페이지가 다루는
  진흙 공은 국소 복잡성이 터진 쪽이고, 같은 이름의 분산 판본은 전역 복잡성이 터진 쪽이다. 같은
  원인(우발적 복잡성)이 경계를 어디에 긋느냐에 따라 두 모양으로 나타난다.
- 그 논증의 전문은 [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)에
  있고, 경계를 실제로 고르는 어림법은
  [마이크로서비스 경계 어림법](microservice-boundary-heuristics.md)에 있다.

## 책의 사례 — 우발적 복잡성이 설계 쪽에서 나온 경우

**같은 판본의 부록 A가 이 이름을 셋째 자리에 쓴다.** 위
[지도 원리](#지도-원리--우발적인-것만-없앤다)가 업무 쪽과 설계 쪽 둘을 같은 이름으로 불렀다면,
부록 A는 **기술적 복잡성이 업무 복잡성을 넘어선 상태**에 같은 이름을 붙인다. 이야기 본체는
[마켓노버스 사례 연구](marketnovus-case-study.md)에 있다.

- 마케팅 허브는 경영진이 핵심 업무 도메인으로 규정했으므로 이벤트 소싱 도메인 모델과 CQRS와
  마이크로서비스를 함께 얹었으나, **업무가 핵심이라 여겼음에도 그것에는 기술적 복잡성이 없었고
  그 복잡한 아키텍처 뒤에 서 있던 것은 평범한 액티브 레코드로 구현할 수 있었을 만큼 단순한
  업무 로직**이었다 (부록 A §"The real problem", p.283).[^khononov2021]
- 그 어긋남에 이름이 붙는다 (부록 A, p.283):[^khononov2021]

> The technical complexity ended up being much higher than the business complexity. To
> describe such discrepancies in complexities, we use the term accidental complexity, and our
> initial design ended up being exactly that. The system was overengineered.

  - **세 쓰임이 같은 판정 형태를 공유한다** — 업무 쪽(요구 사항이 지나치게 창의적일 때), 설계
    쪽(낡은 결정이 남아 있을 때), 그리고 여기(처음부터 필요보다 정교한 패턴을 골랐을 때)가
    그것이다. 셋 다 **값을 내지 않는 복잡성은 없앤다**는 같은 처방을 받는다.
  - **다만 이 셋째 쓰임은 이 페이지의 처방 방향과 반대다.** 위 세 절이 다루는 것은 **자라서
    생긴** 복잡성을 되짚는 일이고, 부록 A의 경우는 **처음부터 과잉이던** 설계다. 그 판정을
    미리 내리는 절차는 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에
    있고, 경계 쪽 판정은
    [마이크로서비스 경계 어림법](microservice-boundary-heuristics.md)에 있다.

## 이어지는 페이지

- [하위 도메인의 세 종류](subdomain-types.md) — 첫째 경계. 종류가 바뀌는 여섯 갈래도 그곳에 있다
- [마켓노버스 사례 연구](marketnovus-case-study.md) — 과잉 설계가 우발적 복잡성이 된 기록
- [비즈니스 도메인과 하위 도메인](business-domain-and-subdomains.md) — 정합적 유스 케이스라는 자
- [경계 컨텍스트](../concepts/bounded-context.md) — 둘째 경계
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 셋째 경계
- [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md) — 경계를 되짚은 뒤
  구현 패턴을 다시 고르는 자리
- [브라운필드에 도메인 주도 설계 들이기](applying-ddd-to-brownfield.md) — 이미 진흙 공이 된
  체계를 상대로 같은 점검을 절차로 편 장
- [이벤트스토밍](eventstorming.md) — 사라진 도메인 지식을 되찾는 도구
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 같은 문제를 코드 층에서
  다루는 축의 허브
- [마이크로서비스 경계 어림법](microservice-boundary-heuristics.md) — 같은 세 경계를
  물리 서비스 경계로 고르는 쪽
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 국소·전역 복잡성
  논증의 전문
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 11장 "Evolving Design Decisions" §"Growth"(pp.180–182)와
    §"Conclusion" 중 성장에 걸리는 세 줄(pp.182–183) · §"Supporting to Core"(p.171,
    우발적 업무 복잡성이라는 같은 이름이 쓰이는 자리). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다.
    큰 진흙 공 규정(p.180)은 원문이 인용 블록으로 조판한 남의 글이고, 저자가 대는 출처는
    Brian Foote & Joseph Yoder, "Big Ball of Mud"(Fourth Conference on Patterns Languages of
    Programs, PLoP '97/EuroPLoP '97, Monticello, Illinois, September 1997)로 **이 KB가 확인한
    원전이 아니다.** 6장의 애그리게이트 원칙 두 문장(p.182)도 원문이 인용 블록으로 조판한
    자기 인용이라 그 서식만 떼고 옮겼다. 도판 하나(Figure 11-3, 성장에 맞춰 하위 도메인 경계를
    최적화하는 그림)는 도판이라 본문이 그것에 대해 적는 것만 옮겼다. 이 절에는 코드 목록이
    없다. 장 끝 연습문제(pp.183–184)는 claim이 아니라 옮기지 않았다.
    **14장 "Microservices" §"System Complexity"(pp.221–222)도 이 페이지에 합류했다** — 그
    논증의 전문과 마이크로서비스 규정은
    [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)에 두었고 이
    페이지는 복잡성의 두 층 구분만 받았다. 저자가 대는 출처(Glenford J. Myers,
    *Composite/Structured Design*)는 이 KB가 확인한 원전이 아니다. 그 절의 도판
    하나(Figure 14-5, 서비스 세분성과 체계 복잡성)는 도판이라 본문이 그것에 대해 적는 것만
    산문으로 옮겼다.
    **부록 A §"The real problem"(p.283)도 이 페이지에 합류했다** — 우발적 복잡성이라는 이름이
    처음부터 과잉이던 설계에 붙는 셋째 자리다. 다섯 경계 컨텍스트의 이야기 본체는 이 페이지에
    두지 않고 [마켓노버스 사례 연구](marketnovus-case-study.md)에 두었다.

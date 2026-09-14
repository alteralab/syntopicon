---
type: concept
title: 마이크로서비스 경계 어림법
description: 마이크로서비스의 물리 경계를 도메인 주도 설계의 어느 경계에 맞출 것인가 — 경계 컨텍스트가 가장 넓은 유효 경계이고 애그리게이트가 가장 좁은 유효 경계라는 배치, 모든 마이크로서비스는 경계 컨텍스트이지만 그 역은 성립하지 않는다는 비대칭과 경계 컨텍스트가 "가장 큰 유효한 모놀리스"라는 규정, 애그리게이트를 그대로 서비스로 삼는 것이 대개 전역 복잡성을 올린다는 판정과 그것을 가늠하는 세 물음, 하위 도메인이 천성적으로 깊은 모듈이라 안전한 기본값이라는 어림법, 그 두 끝 사이가 안전 지대이고 밖은 큰 진흙 공과 분산된 큰 진흙 공이라는 지형, 그리고 같은 방법론의 열린 호스트 서비스와 부패 방지 계층이 공개 인터페이스를 압축해 서비스를 더 깊게 만드는 두 수단이라는 쓰임
generated: { by: "claude-opus-5", at: "2026-09-15T13:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 마이크로서비스 경계 어림법

- [세 후보가 이미 방법론 안에 있다](#세-후보가-이미-방법론-안에-있다)
- [경계 컨텍스트 — 가장 넓은 유효 경계](#경계-컨텍스트--가장-넓은-유효-경계)
- [애그리게이트 — 가장 좁은 유효 경계](#애그리게이트--가장-좁은-유효-경계)
- [하위 도메인 — 안전한 기본값](#하위-도메인--안전한-기본값)
- [안전 지대와 그 바깥의 두 진흙 공](#안전-지대와-그-바깥의-두-진흙-공)
- [책의 사례 — 애그리게이트마다 서비스를 두었을 때](#책의-사례--애그리게이트마다-서비스를-두었을-때)
- [인터페이스를 압축하는 두 패턴](#인터페이스를-압축하는-두-패턴)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **마이크로서비스의 물리 경계를 어디에 그을 것인가, 그리고 도메인 주도 설계의
어느 경계가 그 자리에 쓰이는가.**

## 세 후보가 이미 방법론 안에 있다

- [khononov2021](../sources/khononov2021.md)은 **이 방법론의 패턴 다수가 이미 경계에 대한
  것**이라는 관찰에서 출발한다 — 경계 컨텍스트는 모델의 경계이고, 하위 도메인은 업무 능력을
  한정하며, 애그리게이트와 값 객체는 트랜잭션 경계다 (14장 §"Domain-Driven Design and
  Microservices' Boundaries", p.225).[^khononov2021] 물음은 **그중 어느 것이 마이크로서비스라는
  개념에 맞는가**다.
- 세 후보를 저자는 차례로 검사하고 **셋 다 쓰이되 서는 자리가 다르다**고 판정한다 — 경계
  컨텍스트가 위 끝, 애그리게이트가 아래 끝, 하위 도메인이 그 사이의 기본값이다 (14장,
  pp.225–229).[^khononov2021]
- **이 판정이 무엇을 재는지는 이 판본의 마이크로서비스 규정에 달려 있다** — 서비스의 크기가
  아니라 **공개 인터페이스의 좁음**이고, 개별 서비스가 아니라 **체계 전체의 복잡성**이 잣대다.
  그 규정은 [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md)에 있다.

## 경계 컨텍스트 — 가장 넓은 유효 경계

- **두 패턴은 공통점이 많고 그래서 자주 바꿔 쓰인다.** 둘 다 물리 경계이고, 둘 다 한 팀이
  소유하며, 둘 다 안에 충돌하는 모델을 담을 수 없다 — 담으면 인터페이스가 복잡해진다 (14장
  §"Bounded Contexts", p.225).[^khononov2021]
- **그러나 관계가 대칭이 아니다** (14장 §"Bounded Contexts", p.226):[^khononov2021]

> Therefore, the relationship between microservices and bounded contexts is not symmetric.
> Although microservices are bounded contexts, not every bounded context is a microservice.

  - 근거는 경계 컨텍스트의 정의가 **모델의 충돌만** 금지한다는 데 있다. 충돌하는 모델이 없으면
    경계는 자연히 넓어지고, 하위 도메인 여럿을 담을 수 있으며, 그것들을 이 컨텍스트에서 저
    컨텍스트로 옮긴 여러 대안 분해가 **전부 유효한 경계 컨텍스트**다 (14장, pp.225–226).
    [^khononov2021] 그 넓은 것들을 마이크로서비스라 부를 수는 없다.
- **그래서 이 경계에 붙는 이름이 "가장 큰 유효한 모놀리스"다** (14장 §"Bounded Contexts",
  p.226):[^khononov2021]

> Bounded contexts, on the other hand, denote the boundaries of the largest valid monolith.

  - 저자는 곧바로 단서를 단다 — **그 모놀리스를 큰 진흙 공과 혼동하지 말 것.** 그것은 자기
    유비쿼터스 언어와 업무 도메인 모델의 정합성을 지키는 **유효한 설계 선택지**다 (14장,
    p.226).[^khononov2021]
  - 대안 분해들이 갈리는 자리는 모델이 아니라 **요구**다 — 팀의 크기와 구조, 생애 주기 의존
    같은 것이 분해마다 달라진다 (14장, p.226).[^khononov2021]

## 애그리게이트 — 가장 좁은 유효 경계

- **경계 컨텍스트가 위 끝을 정한다면 애그리게이트는 그 반대다** — 애그리게이트의 경계가 **가능한
  가장 좁은 경계**이고, 애그리게이트 하나를 여러 물리 서비스나 여러 경계 컨텍스트로 쪼개는 것은
  최적이 아닌 정도가 아니라 원하지 않는 결과를 낳는다 (14장 §Aggregates, p.227).
  [^khononov2021]
- **그렇다고 애그리게이트를 그대로 서비스로 삼아도 된다는 뜻은 아니다.** 애그리게이트는 내부
  업무 규칙과 불변식과 로직의 복잡성을 감싸는 나눌 수 없는 업무 기능 단위이지만, 이 판본의
  마이크로서비스는 **개별 서비스에 대한 것이 아니라 그 서비스가 다른 구성 요소와 맺는 상호작용에
  대한 것**이다 (14장 §Aggregates, p.227).[^khononov2021]
- 그래서 판정 전에 물을 것이 셋이다 (14장 §Aggregates, pp.227–228):[^khononov2021]
  - 문제의 애그리게이트가 같은 하위 도메인의 다른 애그리게이트와 소통하는가.
  - 다른 애그리게이트와 값 객체를 공유하는가.
  - 이 애그리게이트의 업무 로직 변경이 그 하위 도메인의 다른 구성 요소에 영향을 줄 가능성은
    얼마나 되는가. 그 반대 방향은 어떤가.
- **판정 규칙이 한 문장으로 온다** — 애그리게이트가 자기 하위 도메인의 다른 업무 엔티티와 맺는
  관계가 강할수록, 그것을 개별 서비스로 세웠을 때 **더 얕은** 서비스가 된다 (14장 §Aggregates,
  p.228).[^khononov2021]
- **결론은 금지가 아니라 빈도다** (14장 §Aggregates, p.228):[^khononov2021]

> There will be cases in which having an aggregate as a service will produce a modular design.
> However, much more often such fine-grained services will increase the overarching system's
> global complexity.

  - 이 판정은 **이 소스가 같은 장 앞부분에서 세운 잣대의 직접 적용**이다 — 얕은 모듈은 전역
    복잡성을 올린다. 그 잣대는
    [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)에 있다.
  - 저자는 애그리게이트를 쪼갰을 때 벌어지는 일의 실물을 부록 A로 미룬다 (14장, p.227).
    [^khononov2021]

## 하위 도메인 — 안전한 기본값

- **더 균형 잡힌 어림법은 서비스를 업무 하위 도메인의 경계에 맞추는 것**이다 (14장 §Subdomains,
  p.228).[^khononov2021]
- 근거가 두 층이다 (14장 §Subdomains, pp.228–229):[^khononov2021]
  - **업무 쪽에서 보면** 하위 도메인은 세분화된 업무 능력과 상관하고, 능력이 **무엇인지**를
    말할 뿐 **어떻게** 구현되는지를 말하지 않는다.
  - **기술 쪽에서 보면** 하위 도메인은 정합적인 유스 케이스의 집합이다 — 같은 업무 도메인
    모델을 쓰고, 같거나 밀접한 데이터 위에서 일하며, 강한 기능적 관계를 갖는다. 그래서 그중
    한 유스 케이스의 업무 요구가 바뀌면 다른 유스 케이스에도 영향이 갈 공산이 크다.
- **그 둘이 합쳐져 하위 도메인을 천성적으로 깊은 모듈로 만든다** — 하위 도메인의 서술(기능)이
  더 복잡한 구현 세부(로직)를 감싸고, 담긴 유스 케이스가 정합적이라는 성질이 그 깊이를 보증한다.
  그것들을 갈라 놓으면 대개 공개 인터페이스가 복잡해져 **더 얕은 모듈**이 된다 (14장
  §Subdomains, p.229).[^khononov2021]
- **그래서 기본값이 된다** (14장 §Subdomains, p.229):[^khononov2021]

> Aligning microservices with subdomains is a safe heuristic that produces optimal solutions for
> the majority of microservices.

  - 단서도 함께 온다 — **다른 경계가 더 효율적인 경우가 있다.** 더 넓은 언어적 경계인 경계
    컨텍스트에 머무는 쪽이 나을 때도 있고, 비기능 요구 때문에 애그리게이트를 마이크로서비스로
    삼아야 할 때도 있다. 해답은 업무 도메인만이 아니라 **조직 구조·업무 전략·비기능 요구**에도
    달려 있다 (14장 §Subdomains, p.229).[^khononov2021]
  - 그리고 이 결정은 한 번 내리고 끝나지 않는다 — 저자는 11장을 가리키며 **환경의 변화에 맞춰
    아키텍처와 설계를 계속 적응시키는 것이 결정적**이라고 적는다 (14장 §Subdomains, p.229).
    [^khononov2021] 그 절차는 [성장이 낳는 복잡성](../concepts/growth-driven-complexity.md)에 있다.

## 안전 지대와 그 바깥의 두 진흙 공

- **두 끝 사이가 안전 지대다** — 경계 컨텍스트와 마이크로서비스 사이의 영역은 안전하고, 그 안의
  것들은 유효한 설계 선택지다 (14장 §"Bounded Contexts", p.227).[^khononov2021]
- **바깥으로 나가는 두 방향에 각각 이름이 있다** — 체계가 제대로 된 경계 컨텍스트로 분해되지
  않으면 큰 진흙 공(big ball of mud)이 되고, 마이크로서비스 문턱을 넘어 더 잘게 분해하면
  분산된 큰 진흙 공(distributed big ball of mud)이 된다 (14장 §"Bounded Contexts", p.227).
  [^khononov2021]
- 맺음이 그 지형을 한 문장에 담는다 (14장 §Conclusion, p.231):[^khononov2021]

> In its essence, a microservice defines the smallest valid boundary of a service, while a bounded
> context protects the consistency of the encompassed model and represents the widest valid
> boundaries.

  - **두 이름이 같은 뜻이 아니라는 것이 이 장의 결론이다** — 역사적으로 두 낱말이 바꿔 쓰일
    만큼 얽혀 있었으나, 모든 마이크로서비스는 경계 컨텍스트이고 모든 경계 컨텍스트가
    마이크로서비스인 것은 아니다 (14장 §Conclusion, p.231).[^khononov2021]

## 책의 사례 — 애그리게이트마다 서비스를 두었을 때

**위 [애그리게이트 — 가장 좁은 유효 경계](#애그리게이트--가장-좁은-유효-경계)가 부록 A로 미룬
실물이 여기다.** 이야기 본체는 [마켓노버스 사례 연구](../concepts/marketnovus-case-study.md)에 있고, 여기
옮긴 것은 이 경계 판정에 걸리는 것이다.

- **결정과 그 근거가 명시적이다** — **서비스는 작을수록 좋다고 순진하게 생각해 애그리게이트를
  둘러 서비스 경계를 그었고, DDD 용어로는 애그리게이트 하나하나가 그 자체로 경계 컨텍스트가
  되었다** (부록 A §"Micro what?", p.282).[^khononov2021]
- **초기 신호는 좋았다** — 서비스마다 필요에 맞게 구현할 수 있었고(하나만 이벤트 소싱을 쓰고
  나머지는 상태 기반 애그리게이트였다) 독립적으로 유지·진화시킬 수 있었다 (부록 A,
  p.282).[^khononov2021]
- **무너진 경로가 이 페이지의 판정과 정확히 같다** — **체계가 자라며 서비스들이 점점
  수다스러워졌고, 결국 거의 모든 서비스가 자기 연산 일부를 끝내기 위해 다른 모든 서비스의
  데이터를 필요로 하게 되었다. 결합을 끊으려 했던 체계가 분산된 모놀리스 — 유지 보수의 완전한
  악몽 — 가 되었다** (부록 A, p.282).[^khononov2021]
  - **이것이 위 [안전 지대와 그 바깥의 두 진흙 공](#안전-지대와-그-바깥의-두-진흙-공)에서
    아래쪽 문턱을 넘은 경우다.** 저자가 같은 부록에서 그 판정을 반복한다 — 엔티티 기반 경계는
    **마케팅 허브에서는 제한적으로만 성공했고 다른 곳에서는 통했다** (부록 A,
    p.286).[^khononov2021] 곧 **금지가 아니라 문턱**이라는 이 페이지의 서술과 같다.
- **그리고 반대 방향의 어림법이 이 사례의 결론이다** (부록 A, p.286):[^khononov2021]

> In our experience, it was much safer to extract a service out of a bigger one than to start
> with services that are too small.

  - **더 큰 경계로 시작해 지식이 쌓인 뒤 쪼개는 쪽**을 택했고, 그렇게 함으로써 **경계 컨텍스트가
    진화하는 내내 안전한 경계의 범위 안에 머물렀다** (부록 A, pp.286–287).[^khononov2021]
    그 어림법의 전문은 [경계 컨텍스트](../concepts/bounded-context.md)에 있다.

## 인터페이스를 압축하는 두 패턴

**경계를 찾는 것 말고 이 방법론이 하는 일이 하나 더 있다** — 서비스를 더 깊게 만드는 것이다.
저자는 같은 방법론의 통합 패턴 둘이 그 일을 한다고 적는다 (14장 §"Compressing Microservices'
Public Interfaces", p.229).[^khononov2021]

| 패턴 | 어느 쪽에 붙는가 | 무엇이 줄어드는가 |
|---|---|---|
| 열린 호스트 서비스(open-host service) | 데이터를 내주는 쪽 | 체계의 전역 복잡성 |
| 부패 방지 계층(anticorruption layer) | 데이터를 받는 쪽 | 받는 컨텍스트의 국소 복잡성과 체계의 전역 복잡성 |

- **열린 호스트 서비스** — 이 패턴은 경계 컨텍스트의 업무 도메인 모델을 통합용 모델과 갈라
  놓는다. 그 통합용 모델인 공표된 언어(published language)가 전역 복잡성을 줄이는 길이 둘이다
  (14장 §"Open-Host Service", p.229):[^khononov2021]
  - 소비자에게 영향을 주지 않고 구현을 진화시킬 수 있다 — 새 구현 모델을 기존 공표된 언어로
    번역하면 된다.
  - 공표된 언어가 **더 절제된 모델**을 드러낸다. 통합 필요에 맞춰 설계되므로 소비자와 무관한
    구현 복잡성을 감추고, 더 적은 데이터를 더 편한 모델로 내줄 수 있다.
  - 그래서 **같은 구현(로직) 위에 더 단순한 공개 인터페이스(기능)를 얹는 것**이고, 그것이 곧
    서비스를 더 깊게 만든다 (14장 §"Open-Host Service", p.229).[^khononov2021]
- **부패 방지 계층** — 반대 방향으로 작동해서, 이 서비스를 다른 경계 컨텍스트와 통합하는 일의
  복잡성을 줄인다. 전통적으로 이 계층은 자기가 지키는 경계 컨텍스트에 속하지만, **독립 서비스로
  구현할 수 있다** (14장 §"Anticorruption Layer", p.230).[^khononov2021]
  - 독립 서비스로 세우면 **소비하는 경계 컨텍스트의 업무 복잡성이 통합 복잡성과 분리되고**,
    뒤엣것이 이 계층 서비스로 떠넘겨진다. 소비하는 컨텍스트는 더 편한 통합용 모델을 상대하게
    되므로 그쪽 공개 인터페이스도 압축된다 — 생산하는 서비스가 드러낸 통합 복잡성이 거기에
    비치지 않는다 (14장 §"Anticorruption Layer", p.230).[^khononov2021]
  - 이 계층을 독립 서비스로 세우는 결정 자체는 9장이 먼저 말한 것이고, 그 구현 선택지는
    [모델 번역](model-translation.md)에 있다.

## 이 KB의 다른 자리들과의 분업

- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — **무엇이
  마이크로서비스인가**에 답하는 쪽. 공개 인터페이스로 내리는 정의와 국소·전역 복잡성의 모델,
  그리고 크기로 내린 정의에 대한 판정이 그곳에 있다.
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 이 장이 빌려 쓰는 잣대의
  원산지. 이 판본이 그 잣대를 서비스 경계에 적용하는 자리도 그곳에 한 절로 있다.
- [경계 컨텍스트](../concepts/bounded-context.md) — 위 끝 경계의 본체.
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 아래 끝
  경계의 본체.
- [하위 도메인의 세 종류](subdomain-types.md)와
  [비즈니스 도메인과 하위 도메인](../concepts/business-domain-and-subdomains.md) — 기본값이 되는 경계의
  본체와 그 발견 절차.
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)과
  [부패 방지 계층](../concepts/anticorruption-layer.md) — 인터페이스를 압축하는 두 패턴의 본체.

## 이어지는 페이지

- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 이 경계가 무엇을
  나누는지의 정의
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 깊이라는 잣대
- [경계 컨텍스트](../concepts/bounded-context.md) — 가장 넓은 유효 경계
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 가장 좁은
  유효 경계
- [하위 도메인의 세 종류](subdomain-types.md) — 안전한 기본값이 되는 경계
- [성장이 낳는 복잡성](../concepts/growth-driven-complexity.md) — 그은 경계를 나중에 되짚는 절차
- [마켓노버스 사례 연구](../concepts/marketnovus-case-study.md) — 이 경계 판정이 실제로 어긋난 기록
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md) — 열린 호스트 서비스와 공표된 언어
- [부패 방지 계층](../concepts/anticorruption-layer.md) — 받는 쪽의 압축 수단
- [모델 번역](model-translation.md) — 두 패턴의 구현 선택지
- [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md) — 같은 경계를 비동기 통신으로
  잇는 쪽
- [모놀리스와 모듈](../concepts/monolith-versus-modular.md) — 쪼갤 것인가 말 것인가의 축
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^khononov2021]: Khononov 2021, 14장 "Microservices"
    §"Domain-Driven Design and Microservices' Boundaries"(도입 p.225 · §"Bounded Contexts"
    pp.225–227 · §Aggregates pp.227–228 · §Subdomains pp.228–229) ·
    §"Compressing Microservices' Public Interfaces"(도입 p.229 · §"Open-Host Service" p.229 ·
    §"Anticorruption Layer" pp.230–231) · §Conclusion p.231. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 도판 여섯(Figure 14-8 경계 컨텍스트 · 14-9 경계 컨텍스트의 대안
    분해 · 14-10 세분성과 모듈성 · 14-11 하위 도메인 · 14-12 공표된 언어를 통한 서비스 통합 ·
    14-13 독립 서비스로 세운 부패 방지 계층)은 도판이라 본문이 그것에 대해 적는 것만 산문으로
    옮겼다. 이 절들에는 코드 목록이 없다. 위 압축 패턴 비교 표는 원문에 없다 — 같은 절이
    산문으로 적는 두 패턴의 방향과 줄어드는 복잡성을 이 KB가 표로 모은 것이고 각 칸의 근거는
    그 절의 본문에 있다. 장 끝 연습문제 넷(p.232)은 claim이 아니라 옮기지 않았다.
    **부록 A §"Bounded Context #5: The Marketing Hub"(p.282)와 §"Boundaries of Bounded
    Contexts"(pp.286–287)도 이 페이지에 합류했다** — 14장이 미뤄 둔 애그리게이트 분해의 실물이
    그 자리다. 다섯 경계 컨텍스트의 이야기 본체는 이 페이지에 두지 않고
    [마켓노버스 사례 연구](../concepts/marketnovus-case-study.md)에 두었다.

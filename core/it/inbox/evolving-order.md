---
type: concept
title: 질서의 진화
description: 대규모 구조를 미리 정해 놓지 말고 애플리케이션과 함께 진화시키라는 이 소스의 메타 조항 — 규칙의 존재가 아니라 그 경직성과 출처가 문제라는 진단, 앞서 굳힌 아키텍처가 구속복이 되고 개발자가 그것에 맞춰 애플리케이션을 멍청하게 만들거나 뒤엎어 버린다는 두 결말, 구조를 고르는 것이 전체의 관리 가능성을 개별 부분의 최적 구성보다 앞세우는 선택이라는 계산, 구조는 여러 경계 컨텍스트에 걸쳐 쓸 수 있어야 하고 통제 밖의 레거시 같은 현실적 제약을 수용해야 한다는 요구, 컨텍스트 지도와 달리 선택 사항이라는 판정, 그리고 맞지 않는 구조는 없는 것보다 나쁘니 최소한만 찾으라는 "적을수록 낫다", 마스터 플랜이 전체주의적 질서를 만들고 전체는 과하게 정밀하되 세부는 모자라며 사용자를 소외시킨다는 크리스토퍼 알렉산더의 진단과 점진적 성장을 위한 원칙 집합이라는 대안, 그리고 이 조항이 중앙 권위 없이 굴러가는 팀의 작동 방식으로 읽히는 17장의 자리
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 질서의 진화

- [앞서 굳힌 구조가 무엇을 앗아 가는가](#앞서-굳힌-구조가-무엇을-앗아-가는가)
- [무질서와 구속복 사이](#무질서와-구속복-사이)
- [문제는 규칙의 존재가 아니다](#문제는-규칙의-존재가-아니다)
- [조항](#조항)
- [무엇과 무엇을 맞바꾸는가](#무엇과-무엇을-맞바꾸는가)
- [구조는 경계를 가로질러야 하고 현실을 수용해야 한다](#구조는-경계를-가로질러야-하고-현실을-수용해야-한다)
- [선택 사항이고, 적을수록 낫다](#선택-사항이고-적을수록-낫다)
- [예외는 표시하되 많아지면 구조를 버린다](#예외는-표시하되-많아지면-구조를-버린다)
- [마스터 플랜이 실패하는 이유](#마스터-플랜이-실패하는-이유)
- [이 조항이 조직의 작동 방식이 되는 자리](#이-조항이-조직의-작동-방식이-되는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **전체를 규율하는 규칙을 언제 정하는가 — 시작할 때인가, 아니면 아는 만큼
자라게 두는가.**

## 앞서 굳힌 구조가 무엇을 앗아 가는가

- 출발점은 흔한 대응이다 — **무정부 상태를 피하려고 프로젝트는 개발을 여러 방식으로 제약하는
  아키텍처를 부과한다** (16장, p.444).[^evans2003]
- 기술 아키텍처와 도메인 아키텍처가 갈린다 — **어떤 기술 아키텍처는 네트워킹이나 데이터
  영속성 같은 기술적 문제를 실제로 푼다. 그러나 아키텍처가 애플리케이션과 도메인 모델의
  영역으로 들어서기 시작하면 스스로 문제를 만들어 낼 수 있다** (16장, p.444).[^evans2003]
  - 손실 셋이 열거된다 — 문제의 특수성에 잘 맞는 설계와 모델을 만들지 못하게 막는 것, 가장
    야심 찬 아키텍처는 **프로그래밍 언어 자체의 친숙함과 기술적 힘까지** 애플리케이션 개발자
    에게서 앗아 가는 것, 그리고 **기술적이든 도메인 지향이든 앞선 설계 결정을 많이 얼려 두는
    아키텍처는 요구가 변하고 이해가 깊어지면서 구속복이 될 수 있다**는 것
    (16장, p.444).[^evans2003]
- 이 장이 쓰인 시점의 관찰도 함께 적힌다 — **J2EE 같은 기술 아키텍처가 여러 해에 걸쳐 두드러진
  반면 도메인 층의 대규모 구조는 많이 탐구되지 않았다. 필요가 애플리케이션마다 크게 다르다**
  (16장, p.444).[^evans2003]
- 앞서 부과했을 때의 진행 경로가 구체적으로 그려진다 (16장, p.444):[^evans2003]
  - 개발이 진행되면 **거의 확실히 더 알맞은 구조를 찾게 되고**, 규정된 구조가 애플리케이션을
    크게 명료하게 하거나 단순하게 만들 설계 경로를 막고 있음을 발견하게 된다.
  - 구조의 일부는 쓸 수 있을지 몰라도 **기회를 포기하는 것**이고, 우회책을 짜거나 아키텍트와
    협상하느라 작업이 느려진다.
  - 그런데 **관리자들은 아키텍처가 끝났다고 생각한다.** 저자가 관리자의 말로 옮긴다 —
    이것은 애플리케이션을 쉽게 만들어 주기로 되어 있었는데, 왜 애플리케이션 대신 아키텍처
    문제만 다루고 있는가.
  - **관리자와 아키텍처 팀이 의견을 받아들일 자세가 되어 있더라도, 변경 하나하나가 영웅적
    전투라면 너무 지친다.**

## 무질서와 구속복 사이

- 두 극단이 나란히 기각된다 (16장, p.444):[^evans2003]

> Design free-for-alls produce systems no one can make sense of as a whole, and they are very
> difficult to maintain. But architectures can straitjacket a project with up-front design
> assumptions and take too much power away from the developers/designers of particular parts of
> the application.

- 구속복 쪽의 결말이 둘로 갈린다 — **머지않아 개발자들은 구조에 맞추려고 애플리케이션을
  멍청하게 만들거나, 구조를 뒤엎어 버리고 아무 구조도 갖지 않게 되어 조율 없는 개발의 문제를
  되돌아오게 한다** (16장, p.444).[^evans2003]

## 문제는 규칙의 존재가 아니다

- 진단 (16장, p.445):[^evans2003]

> The problem is not the existence of guiding rules, but rather the rigidity and source of those
> rules. If the rules governing the design really fit the circumstances, they will not get in the
> way but actually push development in a helpful direction, as well as provide consistency.

  - 두 낱말이 짝을 이룬다 — **경직성(rigidity)**과 **출처(source)**. 뒤의 것이 이 패턴을 조직
    문제로 만든다. 규칙이 어디서 왔는가가 규칙이 맞는지를 좌우한다.

## 조항

- 처방 문단 (16장, p.445):[^evans2003]

> Let this conceptual large-scale structure evolve with the application, possibly changing to a
> completely different type of structure along the way. Don't overconstrain the detailed design
> and model decisions that must be made with detailed knowledge.

  - 두 문장이 각각 시간 축과 층위 축을 잡는다. 앞은 **구조의 종류가 바뀌어도 좋다**는 허가이고,
    뒤는 **세부 지식으로 내려야 하는 결정을 전역 규칙이 침범하지 말라**는 금지다.

## 무엇과 무엇을 맞바꾸는가

- 대가가 명시된다 (16장, p.445):[^evans2003]

> Individual parts have natural or useful ways of being organized and expressed that may not
> apply to the whole, so imposing global rules makes these parts less ideal. Choosing to use a
> large-scale structure favors manageability of the model as a whole over optimal structuring of
> the individual parts.

  - **이것은 손실을 인정하는 조항이다.** 전역 규칙은 부분을 덜 이상적으로 만들고, 구조를 쓰기로
    하는 것은 그 손실을 감수하겠다는 선택이다.
- 손실을 줄이는 방법 둘이 제시된다 — **실제 경험과 도메인 지식에 근거해 구조를 고르는 것**과
  **과도하게 조이는 구조를 피하는 것** (16장, p.445).[^evans2003]
- 잘 맞을 때의 이득 — **구조와 도메인·요구 사이의 정말 좋은 맞음은 선택지를 빠르게 많이
  제거해 줌으로써 오히려 세부 모델링과 설계를 쉽게 만든다** (16장, p.445).[^evans2003]
- 지름길로서의 구조 — **원리상으로는 개별 객체 수준에서 작업해 찾을 수 있지만 실제로는 너무
  오래 걸리고 결과가 일관되지 않을 설계 결정에 구조가 지름길을 줄 수 있다. 물론 지속적
  리팩터링은 여전히 필요하지만, 이것이 그 과정을 더 다룰 만하게 만들고 서로 다른 사람들이
  일관된 해법에 이르도록 도울 수 있다** (16장, p.445).[^evans2003]

## 구조는 경계를 가로질러야 하고 현실을 수용해야 한다

- 적용 범위 조항 — **대규모 구조는 일반적으로 경계 컨텍스트를 가로질러 적용 가능해야 한다**
  (16장, p.445).[^evans2003]
- 그 조건이 구조에 무엇을 하는지 (16장, p.445):[^evans2003]

> Through iteration on a real project, a structure will lose features that tightly bind it to a
> particular model and evolve features that correspond to CONCEPTUAL CONTOURS of the domain.

  - 단서가 붙는다 — **모델에 대해 아무 가정도 하지 않는다는 뜻은 아니지만, 특정한 지역
    상황에 맞춘 착상을 프로젝트 전체에 부과하지는 않는다.** 각 컨텍스트의 개발 팀이 지역적
    필요에 답하도록 모델을 달리할 자유를 남겨야 한다 (16장, p.445).[^evans2003]
- 현실적 제약도 수용해야 한다 — **설계자가 시스템 일부의 모델을 통제하지 못할 수 있다. 특히
  외부 시스템이나 레거시 서브시스템이 그렇다** (16장, pp.445–446).[^evans2003] 대응 셋이
  제시된다 (16장, p.446):[^evans2003]
  - 특정 외부 요소에 더 맞도록 **구조를 바꾸는 것**
  - 애플리케이션이 외부와 관계 맺는 방식을 **명시하는 것**
  - 어색한 현실 주변에서 휠 수 있도록 **구조를 충분히 느슨하게 두는 것**

## 선택 사항이고, 적을수록 낫다

- 세 전략 원리 중 이것만 선택 사항이라는 판정 (16장, p.446):[^evans2003]

> Unlike the CONTEXT MAP, a large-scale structure is optional. One should be imposed when costs
> and benefits favor it, and when a fitting structure is found. In fact, it is not needed for
> systems that are simple enough to be understood when broken into MODULES.

- 적용 조건과 포기 조건 (16장, p.446):[^evans2003]

> Large-scale structure should be applied when a structure can be found that greatly clarifies
> the system without forcing unnatural constraints on model development. Because an ill-fitting
> structure is worse than none, it is best not to shoot for comprehensiveness, but rather to find
> a minimal set that solves the problems that have emerged. Less is more.

  - **"맞지 않는 구조는 없는 것보다 나쁘다"**가 비대칭을 만든다. 구조를 세우는 이득과 잘못
    세우는 손실이 같은 크기가 아니므로, 기본값은 포괄이 아니라 최소다.
  - 이 계산이 16장 §Minimalism으로 이어진다 — 비용을 낮추는 열쇠는 구조를 단순하고 가볍게
    유지하는 것이고, 초기에는 느슨한 구조를 고르라는 조언이 붙는다 (16장,
    p.481).[^evans2003] 그쪽은 [대규모 구조](large-scale-structure.md)가 담는다.

## 예외는 표시하되 많아지면 구조를 버린다

- 마지막 단서 (16장, p.446):[^evans2003]

> A large-scale structure can be very helpful and still have a few exceptions, but those
> exceptions need to be flagged somehow, so that developers can assume the structure is being
> followed unless otherwise noted. And if those exceptions start to get numerous, the structure
> needs to be changed or discarded.

  - **기본 가정이 "구조를 따른다"여야 구조가 값을 한다.** 예외 자체보다 예외가 표시되지 않는
    것이 문제이고, 예외의 개수가 구조를 재심하는 계기가 된다.
- 이 조항은 장 안에서 실제로 발동된다. 책임 층 예제에서 화물이 위험물 정책 서비스에 의존하는
  설계가 구조에 맞지 않아 기각되고, 저자는 곧바로 단서를 단다 — **구조가 어색한 설계 선택을
  많이 강요한다면 질서의 진화에 따라 평가해 수정하거나 폐기해야 한다** (16장,
  p.460).[^evans2003]

## 마스터 플랜이 실패하는 이유

17장이 이 조항의 바깥 논거로 건축 쪽 선례를 인용한다. 크리스토퍼 알렉산더(Christopher
Alexander)가 이끄는 건축가 집단이 건축과 도시 계획에서 **점진적 성장**(piecemeal growth)을
옹호하며 마스터 플랜의 실패를 설명한 대목이다 (17장, pp.496–497).[^evans2003]

인용된 진단 셋이다. 원전은 Alexander et al. 1975, *The Oregon Experiment*, pp.16–28이고 이
책이 그것을 옮겨 싣는다 (17장, p.497):[^evans2003]

> . . . in practice master plans fail—because they create totalitarian order, not organic order.
> They are too rigid; they cannot easily adapt to the natural and unpredictable changes that
> inevitably arise in the life of a community.

> . . . Thus, as a source of organic order, a master plan is both too precise, and not precise
> enough. The totality is too precise: the details are not precise enough.

> . . . the existence of a master plan alienates the users [because, by definition] the members
> of the community can have little impact on the future shape of their community because most of
> the important decisions have already been made.

- **셋이 위의 세 절과 하나씩 대응한다.** 첫째 진단의 경직성은 위
  [앞서 굳힌 구조가 무엇을 앗아 가는가](#앞서-굳힌-구조가-무엇을-앗아-가는가)와, 둘째 진단의
  "전체는 과하게 정밀하고 세부는 모자라다"는 위 [문제는 규칙의 존재가 아니다](#문제는-규칙의-존재가-아니다)와,
  셋째 진단의 소외는 위 [무엇과 무엇을 맞바꾸는가](#무엇과-무엇을-맞바꾸는가)가 계상한
  개발자 쪽 손실과 같은 자리다.
- 그러나 **계획 자체를 기각하는 인용이 아니다.** 같은 인용문이 계획 과정이 아예 없으면 케임브리지
  대학 같은 깊고 조화로운 질서에 이를 가망이 없다고 적고, 마스터 플랜이 전체의 일관성을 주면서도
  개별 건물이 지역의 필요에 적응할 자유를 남기려는 시도였다고 적는다 (17장,
  p.497).[^evans2003] 위 [무질서와 구속복 사이](#무질서와-구속복-사이)가 놓은 양 끝과 같은 구도다.
- 대안이 이 조항의 형식과 같다 (17장, p.497):[^evans2003]

> Alexander and his colleagues advocated instead *a set of principles* for all community members
> to apply to every act of piecemeal growth, so that "organic order" emerges, well adapted to
> circumstances.

  - **전체를 앞서 그리는 대신 모든 구성원이 매번의 성장 행위에 적용할 원칙 집합을 둔다** —
    이것이 이 패턴의 형식 그대로다. 위 [조항](#조항)이 "규칙을 애플리케이션과 함께 진화시키라"고
    적은 것의 도시 계획 판본이다.

## 이 조항이 조직의 작동 방식이 되는 자리

17장은 이 패턴을 설계 조항으로만이 아니라 **의사 결정 구조**로 읽는다.

- 첫째 방식의 규정 (17장, p.491):[^evans2003]

> A self-disciplined team made up of very good communicators can operate without central
> authority and follow EVOLVING ORDER to arrive at a shared set of principles, so that order
> grows organically, not by fiat.

- 그리고 전략 설계 의사 결정의 여섯 필수 가운데 셋째가 이 패턴을 그대로 호명한다 — **계획은
  진화를 허용해야 한다. 최상위 결정이 돌에 새겨지면 팀은 변화에 대응해야 할 때 선택지가 줄어드는데,
  질서의 진화는 깊어지는 통찰에 응답해 대규모 구조를 계속 바꾸는 것을 강조함으로써 이 덫을
  피한다** (17장, p.493).[^evans2003]
  - 여섯 필수 전체는 [전략 설계 결정하기](strategic-decision-making.md)에 있다.

## 이어지는 페이지

- [대규모 구조](large-scale-structure.md) — 이 조항이 지배하는 장의 틀
- [시스템 은유](system-metaphor.md) — 이 조항이 허가하는 가장 느슨한 출발점
- [책임 층](responsibility-layers.md) — 이 조항이 층 선택에 적용되는 자리
- [플러그인 컴포넌트 프레임워크](pluggable-component-framework.md) — 이 조항과 가장 세게
  부딪히는 구조. 핵심의 지속적 정련이 얼어붙는다
- [개념의 윤곽](conceptual-contours.md) — 반복이 구조를 밀고 가는 목적지
- [경계 컨텍스트](../concepts/bounded-context.md) — 구조가 가로질러야 하는 단위
- [컨텍스트 지도](../concepts/context-map.md) — 선택 사항이 아닌 쪽
- [있는 시스템에 이 구조 들이기](adopting-architecture-incrementally.md) — 앞서 굳힌 구조를
  나중에 걷어 내는 쪽의 절차
- [전략 설계 결정하기](strategic-decision-making.md) — 이 조항이 의사 결정 구조로 읽히는 자리와
  마스터 플랜 인용의 전문
- [모델 리팩터링의 과정](model-refactoring-process.md) — 이 진화가 속한 활동
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §EVOLVING ORDER(pp.444–446) ·
    예제 "In Depth: Layering a Shipping System" 중 §"How Does This Structure Affect Ongoing
    Design?"의 맺음(p.460) · §"Refactoring Toward a Fitting Structure" §Minimalism(p.481) ·
    17장 "Bringing the Strategy Together" §"Who Sets the Strategy?"(p.491) ·
    §"Six Essentials for Strategic Design Decision Making"의 셋째 항목(p.493) ·
    §"Beware the Master Plan"(pp.496–497).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례를
    직인용에서 유지했다. 패턴 도비라의 사진(p.444)은 이미지라 옮기지 않았다. 이 절에는 코드
    목록도 도해도 없다 — 이 페이지에 펜스가 없는 이유다. 굵은 글씨는 원문 문장의 한국어
    재서술이고 괄호 안이 그 쪽이다. 마스터 플랜 절의 인용문은 이 책이 Alexander et al. 1975,
    *The Oregon Experiment*, pp.16–28에서 옮겨 실은 것이고, 이 페이지는 그 재인용을 이 책의
    쪽으로 단다 — 원전을 직접 확인하지 않았다.

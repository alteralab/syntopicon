---
type: concept
title: 유연한 설계
description: 10장이 여덟 조항을 펼치기 전에 세우는 틀 — 소프트웨어가 사용자를 섬기기 전에 먼저 개발자를 섬겨야 한다는 전제와 리팩터링을 강조하는 과정에서 그것이 특히 참인 이유, 좋은 설계가 없을 때 중복이 강제되는 기제와 취약함이 만들 수 있는 행동의 풍부함에 천장을 씌운다는 판정, 유연한 설계의 규정과 그것이 깊은 모델링의 보완물이라는 자리매김, 유연성의 이름으로 정당화된 과잉 설계와 단순한 것은 쉽지 않다는 단서, 설계가 함께 섬겨야 할 개발자의 두 역할인 클라이언트 개발자와 바꾸는 개발자 그리고 각 역할이 설계에 거는 다른 요구, 이른 판의 설계는 대개 뻣뻣하고 전부를 유연하게 만든 큰 프로그램은 본 적이 없다는 관찰과 그래도 가장 얽힌 곳을 다듬으면 갈리는 것, 그리고 공식은 없고 들어맞을 때 유연함을 주는 패턴 묶음이 있을 뿐이라는 이 장의 지위 규정
generated: { by: "claude-opus-5", at: "2026-09-14T21:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 유연한 설계

- [사용자보다 먼저 개발자를 섬긴다](#사용자보다-먼저-개발자를-섬긴다)
- [좋은 설계가 없을 때 무엇이 먼저 무너지는가](#좋은-설계가-없을-때-무엇이-먼저-무너지는가)
- [유연한 설계의 규정](#유연한-설계의-규정)
- [깊은 모델링의 보완물](#깊은-모델링의-보완물)
- [유연성의 이름으로 정당화된 과잉 설계](#유연성의-이름으로-정당화된-과잉-설계)
- [설계가 섬겨야 할 두 역할](#설계가-섬겨야-할-두-역할)
- [이른 판의 설계는 뻣뻣하다](#이른-판의-설계는-뻣뻣하다)
- [공식은 없고 패턴 묶음이 있다](#공식은-없고-패턴-묶음이-있다)
- [이 장이 펼치는 여덟 조항](#이-장이-펼치는-여덟-조항)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **설계가 사용자보다 먼저 섬겨야 할 상대는 누구이고, 그 섬김은 설계의 어떤
성질로 드러나는가.**

## 사용자보다 먼저 개발자를 섬긴다

- 이 장을 여는 두 문장이다 (10장, p.243):[^evans2003]

> The ultimate purpose of software is to serve users. But first, that same software has to
> serve developers.

- 왜 "먼저"인지가 곧바로 붙는다 — **이것은 리팩터링을 강조하는 과정에서 특히 참이다.**
  프로그램이 자라는 동안 개발자는 모든 부분을 다시 배치하고 다시 쓰게 되고, 도메인 객체를
  애플리케이션과 새 도메인 객체에 엮어 넣는다. **몇 해가 지난 뒤에도 유지보수 프로그래머가
  그 코드를 바꾸고 늘린다** (10장, p.243).[^evans2003]
- 그리고 저자가 물음 하나로 절을 닫는다 — **사람이 이 물건을 가지고 일해야 한다. 그런데
  그러고 싶겠는가?** (10장, p.243).[^evans2003]
  - **이 물음이 이 장의 판정 심급을 정한다.** 설계의 좋고 나쁨을 재는 자리가 성능이나 기능이
    아니라 **그것을 만지는 사람의 의욕**이다. 같은 심급을 다른 소스에서 인지 부하로 재는
    자리가 [소프트웨어 복잡성의 정의](../concepts/software-complexity-defined.md)다.

## 좋은 설계가 없을 때 무엇이 먼저 무너지는가

- 첫 증상은 중복이다 — **복잡한 행동을 가진 소프트웨어에 좋은 설계가 없으면 리팩터링하거나
  요소를 조합하기가 어려워진다. 개발자가 어떤 계산의 함의 전부를 예측할 자신이 없어지는
  순간부터 중복이 나타나기 시작한다** (10장, p.243).[^evans2003]
- 중복이 선택이 아니게 되는 조건도 적힌다 — **설계 요소가 단단히 한 덩어리여서 부분을 다시
  조합할 수 없을 때 중복은 강제된다** (10장, p.243).[^evans2003]
- 그렇다고 잘게 쪼개는 것이 답이 아니다 — **클래스와 메서드를 더 잘 재사용하려고 잘게
  나눌 수는 있지만, 그 작은 부분들이 전부 무엇을 하는지 따라가기가 어려워진다** (10장,
  pp.243–244).[^evans2003] 같은 대가를 인터페이스 대 구현의 비율로 재는 자리가
  [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)이다.
- 그다음은 손대기를 꺼리는 상태다 — **깨끗한 설계가 없으면 개발자는 기존의 엉망을 들여다보는
  것조차 두려워한다. 엉킴을 악화시키거나 예상 못 한 의존을 통해 무언가를 망가뜨릴 수 있는
  변경은 더 말할 것도 없다** (10장, p.244).[^evans2003]
- 대가가 무엇으로 계상되는지가 이 절의 결론이다 (10장, p.244):[^evans2003]

> In any but the smallest systems, this fragility places a ceiling on the richness of behavior
> it is feasible to build. It stops refactoring and iterative refinement.

  - **대가가 버그가 아니라 "만들 수 있는 행동의 풍부함"으로 계상된다.** 같은 형태의 천장을
    예측 불가능한 연산에서 재는 자리가 [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)다.

## 유연한 설계의 규정

- 반대 상태가 규정된다 (10장, p.244):[^evans2003]

> To have a project accelerate as development proceeds—rather than get weighed down by its own
> legacy—demands a design that is a pleasure to work with, inviting to change. A supple design.

  - 이 소스가 "유연한 설계(supple design)"라 부르는 것이 이 상태다. 규정의 기준이 구조가
    아니라 **일하는 사람의 경험**이라는 점이 앞 절의 물음과 이어진다.

## 깊은 모델링의 보완물

- 이 장이 III부에서 차지하는 자리가 한 문장으로 적힌다 — **유연한 설계는 깊은 모델링의
  보완물이다** (10장, p.244).[^evans2003] 그 짝의 자리가
  [깊은 모델과 돌파](../concepts/deep-model.md)다.
- 두 일이 어떻게 이어지는지도 적힌다 — **암묵적 개념을 파내어 명시적으로 만들고 나면 원재료가
  손에 들어온다. 반복 주기를 거치며 그 재료를 쓸모 있는 모양으로 두들겨, 핵심 관심사를
  단순하고 명료하게 담아내는 모델을 기르고, 클라이언트 개발자가 그 모델을 정말로 쓸 수 있게
  하는 설계를 빚는다** (10장, p.244).[^evans2003] 원재료를 만드는 절차가
  [암묵적 개념 파내기](../concepts/digging-out-implicit-concepts.md)다.
- 되먹임이 닫힌다 — **설계와 코드의 개발이 모델 개념을 정련하는 통찰로 이어진다. 돌고 돌아
  반복 주기와 더 깊은 통찰을 향한 리팩터링으로 되돌아온다** (10장, p.244).[^evans2003]
  그 주기를 하나의 과정으로 묶는 자리가
  [모델 리팩터링의 과정](../concepts/model-refactoring-process.md)이다.
- 그리고 이 장이 답할 물음이 제시된다 — **그런데 당신이 도달하려는 설계는 어떤 종류의
  것인가? 가는 길에 어떤 실험을 해 봐야 하는가? 이 장이 다루는 것이 그것이다** (10장,
  p.244).[^evans2003]

## 유연성의 이름으로 정당화된 과잉 설계

- 경고가 먼저 온다 (10장, p.244):[^evans2003]

> A lot of overengineering has been justified in the name of flexibility. But more often than
> not, excessive layers of abstraction and indirection get in the way. Look at the design of
> software that really empowers the people who handle it; you will usually see something
> simple. Simple is not easy.

  - **"단순한 것은 쉽지 않다"가 이 장 전체의 단서다.** 유연함의 징표를 층과 간접 참조의
    개수로 읽는 습관을 여기서 끊어 둔다.
- 단순함에 도달하는 조건이 붙는다 — **정교한 시스템으로 조립되면서도 여전히 이해할 수 있는
  요소를 만들려면, 모델 주도 설계(MODEL-DRIVEN DESIGN)에 대한 헌신이 적당히 엄격한 설계
  양식과 결합되어야 한다** (10장, p.244).[^evans2003] 그 헌신의 정의가
  [모델 주도 설계](../concepts/model-driven-design.md)에 있다.
- 그 대가가 솔직하게 적힌다 — **그것을 만드는 데는, 또는 쓰는 데는(*or to use*) 상대적으로
  세련된 설계 기량이 요구될 수 있다** (10장, p.244).[^evans2003]
  - **기량 요구가 이 장의 끝에서 다시 나온다.** 같은 단서가
    [연산의 닫힘](../concepts/closure-of-operations.md)이 닫히는 자리에 붙어 있다.

## 설계가 섬겨야 할 두 역할

- 역할이 둘로 갈린다 — **개발자는 두 역할을 하고, 설계는 그 각각을 섬겨야 한다. 같은 사람이
  두 역할을 다 할 수도 있고 몇 분 사이에 오갈 수도 있지만, 코드와 맺는 관계가 그럼에도
  다르다** (10장, p.244).[^evans2003]
- 첫째는 **클라이언트 개발자(developer of a client)**다. 도메인 객체를 애플리케이션 코드나
  다른 도메인 층 코드에 엮어 넣으며 설계의 능력을 활용하는 쪽이다 (10장, p.244).[^evans2003]
  - 이 역할에 설계가 무엇을 주어야 하는지가 이어진다 — **유연한 설계는 그 잠재력을 분명하게
    만드는 깊은 바탕 모델을 드러낸다. 클라이언트 개발자는 느슨하게 결합된 최소한의 개념
    집합을 유연하게 써서 도메인의 여러 시나리오를 표현할 수 있다. 설계 요소들이 자연스럽게
    맞물리고 그 결과는 예측 가능하고 뚜렷하게 규정되며 견고하다** (10장,
    p.244).[^evans2003]
  - **클라이언트 개발자의 시점을 강제하는 장치**가 같은 장의 첫 조항에 있다.
    [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)가 그 자리다.
- 둘째는 **바꾸는 개발자(the developer working to change it)**다. 저자가 "똑같이 중요하다"고
  못 박는다 (10장, p.245):[^evans2003]

> Equally important, the design must serve the developer working to change it. To be open to
> change, a design must be easy to understand, revealing that *same* underlying model that the
> client developer is drawing on. It must follow the contours of a deep model of the domain, so
> most changes bend the design at flexible points. The effects of its code must be transparently
> obvious, so the consequences of a change will be easy to anticipate.

  - **한 문단 안에 이 장의 나머지 조항들이 이름만 다르게 들어 있다.** 같은 바탕 모델을
    드러내라는 요구가 [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md),
    도메인의 윤곽을 따르라는 요구가 [개념의 윤곽](../concepts/conceptual-contours.md), 코드의 효과가
    투명하게 드러나야 한다는 요구가
    [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)와 [단언](../concepts/assertions-pattern.md)이다.

## 이른 판의 설계는 뻣뻣하다

- 기대를 낮추는 관찰이 온다 — **설계의 이른 판은 대개 뻣뻣하다. 많은 설계가 프로젝트의 기간이나
  예산 안에서 끝내 어떤 유연함도 얻지 못한다** (10장, p.245).[^evans2003]
- 저자 자신의 실측이 붙는다 — **나는 이 성질을 처음부터 끝까지 갖춘 큰 프로그램을 본 적이
  없다** (10장, p.245).[^evans2003]
- 그래도 표적을 좁히면 남는 것이 있다 — **그러나 복잡성이 진척을 붙들고 있을 때, 가장
  결정적이고 가장 얽힌 부분을 유연한 설계로 다듬는 것이 레거시 유지보수로 빨려 들어가는
  것과 복잡성의 천장을 뚫는 것 사이를 가른다** (10장, p.245).[^evans2003]
  - **전부가 아니라 일부를 고르라는 지시다.** 그 고르는 법을 절로 펼친 자리가 같은 장의
    [확립된 형식 체계](../concepts/established-formalisms.md)이고, 더 큰 규모에서 같은 선택을 하는
    자리가 [핵심 도메인](../concepts/core-domain.md)이다.

## 공식은 없고 패턴 묶음이 있다

- 이 장의 지위가 규정된다 (10장, p.245):[^evans2003]

> There is no formula for designing software like this, but I have culled a set of patterns
> that, in my experience, tend to lend suppleness to a design when they fit.

- 기대되는 쓰임도 적힌다 — **이 패턴들과 예제들은 유연한 설계가 어떤 것인지, 그리고 거기에
  들어가는 사고가 어떤 종류인지에 대한 감각을 주어야 한다** (10장, p.245).[^evans2003]
  - **"들어맞을 때"와 "감각"이라는 두 낱말이 이 장을 규칙 목록으로 읽는 것을 막는다.**
    같은 종류의 단서가 [개념의 윤곽](../concepts/conceptual-contours.md)의 "요리책 규칙은 없다"에 있다.

## 이 장이 펼치는 여덟 조항

- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 이름이 목적을
  말하고 수단은 말하지 않게 하는 조항
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 연산을 명령과 질의로 가르고 로직을
  함수 쪽에 몰아 두는 조항
- [단언](../concepts/assertions-pattern.md) — 연산의 결과를 구현을 읽지 않고 알 수 있게 만드는 조항
- [개념의 윤곽](../concepts/conceptual-contours.md) — 설계 요소를 어느 굵기로 쪼갤지 도메인이 정하게
  하는 조항
- [독립형 클래스](../concepts/standalone-classes.md) — 비본질적인 의존을 없애 홀로 이해되게 만드는 조항
- [연산의 닫힘](../concepts/closure-of-operations.md) — 인자와 반환 타입을 구현자와 같게 두어 새 개념을
  들이지 않는 조항
- [선언적 설계](../concepts/declarative-design.md) — 앞선 조항들이 갖춰졌을 때 들어서는 양식과 그 함정
- [확립된 형식 체계](../concepts/established-formalisms.md) — 어디서부터 손댈지 정하는 두 공략 각도와
  그 통합 예제

## 이어지는 페이지

- [깊은 모델과 돌파](../concepts/deep-model.md) — 이 장이 보완한다고 말하는 짝
- [암묵적 개념 파내기](../concepts/digging-out-implicit-concepts.md) — 이 장이 쓸 원재료를 만드는 절차
- [모델 리팩터링의 과정](../concepts/model-refactoring-process.md) — 이 되먹임을 하나의 과정으로 묶는 자리
- [모델 주도 설계](../concepts/model-driven-design.md) — 이 장이 전제로 요구하는 헌신
- [핵심 도메인](../concepts/core-domain.md) — 같은 선택을 더 큰 규모에서 하는 자리
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 같은 대가를 인터페이스 대 구현의
  비율로 재는 자리
- [소프트웨어 복잡성의 정의](../concepts/software-complexity-defined.md) — 같은 심급을 인지
  부하로 재는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 10장 "Supple Design" 장 도입(pp.243–245). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는 관례와 이탤릭 강조를
    직인용에서 유지했다. 장 도입 끝의 패턴 항해 지도(Figure 10.1, p.245)는 도판이라 옮기지
    않았다 — 그 지도가 잇는 여덟 패턴의 자리는 위 "이 장이 펼치는 여덟 조항"에 링크로 있다.
    이 도입에는 코드가 없어 펜스를 두지 않았다.

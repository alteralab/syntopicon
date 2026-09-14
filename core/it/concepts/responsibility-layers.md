---
type: concept
title: 책임 층
description: 도메인의 자연스러운 성층을 넓은 추상적 책임으로 옮겨 층으로 세우는 대규모 구조 — 객체마다 손으로 빚은 책임에는 지침도 균일성도 없다는 문제, 층의 정의와 의존 관계를 보기 좋게 늘어놓은 임시 층 나누기가 모델에 통찰을 주지 못한다는 진단, 개념적 의존과 변화의 속도·출처를 보고 자연스러운 지층을 찾아 각 객체와 애그리게이트와 모듈이 한 층의 책임 안에 들도록 리팩터링하라는 조항, 화물 운송 모델이 운영과 잠재력에서 의사 결정 지원까지 세 층으로 갈리며 선호 항로 속성이 정책 객체로 떨어져 나오는 과정과 구조에 맞지 않는 설계가 기각되는 실례, 층을 고를 때 지켜야 할 성질 셋(이야기하기·개념적 의존·개념의 윤곽), 기업 시스템에 되풀이해 나타나는 다섯 층(잠재력·운영·의사 결정 지원·정책·확약), 그리고 넷이나 다섯을 넘으면 감당이 안 되므로 구조 자체를 맹렬히 증류하라는 한계, 그리고 손댈 수 없는 레거시에도 층 안의 자리를 주고 파사드의 서비스를 한 층에 맞추라는 17장의 현실 수용
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 책임 층

- [책임 주도 설계를 더 큰 규모로](#책임-주도-설계를-더-큰-규모로)
- [층이란 무엇인가, 그리고 임시 층 나누기의 한계](#층이란-무엇인가-그리고-임시-층-나누기의-한계)
- [조항](#조항)
- [사례 — 화물 운송 시스템에 층을 입히기](#사례--화물-운송-시스템에-층을-입히기)
- [구조가 이후 설계를 어떻게 구속하는가](#구조가-이후-설계를-어떻게-구속하는가)
- [층을 고를 때 지켜야 할 성질 셋](#층을-고를-때-지켜야-할-성질-셋)
- [되풀이해 나타나는 다섯 층](#되풀이해-나타나는-다섯-층)
- [층의 개수에는 상한이 있다](#층의-개수에는-상한이-있다)
- [이 층 나누기는 계층 아키텍처가 아니다](#이-층-나누기는-계층-아키텍처가-아니다)
- [레거시에도 층 안의 자리를 준다](#레거시에도-층-안의-자리를-준다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인에 자연스러운 지층이 있을 때 그것을 설계 전체를 규율하는 층으로 어떻게
옮기는가.**

## 책임 주도 설계를 더 큰 규모로

- 출발 — **이 책 전체에서 개별 객체에는 좁고 서로 관련된 책임의 집합이 배정되어 왔다. 책임 주도
  설계(responsibility-driven design)는 더 큰 규모에도 적용된다** (16장, p.450).[^evans2003]
- 문제 서술 — **개별 객체마다 손으로 빚은 책임을 가지면 지침도 없고 균일성도 없고 도메인의 넓은
  자락을 한꺼번에 다룰 능력도 없다. 큰 모델에 정합성을 주려면 그 책임 배정 자체에 어떤 구조를
  부과하는 것이 쓸모 있다** (16장, p.450).[^evans2003]
- 무엇을 근거로 층을 찾는가 (16장, p.450):[^evans2003]

> When you gain a deep understanding of a domain, broad patterns start to become visible. Some
> domains have a natural stratification. Certain concepts and activities take place against a
> background of other elements that change independently and at a different rate for different
> reasons.

  - **다른 속도로, 다른 이유로, 독립적으로 변하는 배경** — 이것이 이 패턴이 찾는 지층의
    표지다. 뒤의 §"층을 고를 때 지켜야 할 성질 셋"에서 이것이 개념의 윤곽과 이어진다.
- 저자는 이 성층이 층 나누기를 부르고, 층 나누기가 **가장 성공한 아키텍처 설계 패턴 중
  하나**(Buschmann et al. 1996 등)라고 적는다 (16장, p.450).[^evans2003]

## 층이란 무엇인가, 그리고 임시 층 나누기의 한계

- 정의 (16장, p.450):[^evans2003]

> Layers are partitions of a system in which the members of each partition are aware of and are
> able to use the services of the layers "below," but unaware of and independent of the layers
> "above."

- 저절로 생기는 층 나누기도 있다 — **모듈의 의존 관계를 그릴 때 의존되는 모듈을 의존하는 모듈
  아래에 놓는 배치를 흔히 쓴다. 그러면 층이 저절로 정렬되어 아래 수준 객체 중 어느 것도 위층
  객체에 개념적으로 의존하지 않게 되기도 한다** (16장, p.450).[^evans2003]
- 그러나 그것으로는 모자란다 (16장, p.450):[^evans2003]

> But this ad hoc layering, while it can make tracing dependencies easier—and sometimes makes
> some intuitive sense—doesn't give much insight into the model or guide modeling decisions. We
> need something more intentional.

  - 저자는 이 상태를 보이는 도해에 **이 패키지들은 무엇에 관한 것인가**라는 물음을 캡션으로
    단다 (16장, p.451, Figure 16.2).[^evans2003]
- 의도적인 층 나누기가 하는 일 — **자연스러운 성층이 있는 모델에서는 주요 책임을 중심으로
  개념적 층을 정의할 수 있고, 그것이 층 나누기와 책임 주도 설계라는 두 강력한 원리를
  통합한다** (16장, p.451).[^evans2003]
- 책임의 굵기 조건 — **이 책임들은 개별 객체에 통상 배정되는 것보다 상당히 넓어야 한다.
  개별 모듈과 애그리게이트는 이 주요 책임 중 하나의 범위 안에 머물도록 인수분해된다**
  (16장, p.451).[^evans2003]
  - 이름 붙인 책임 묶음만으로도 모듈화된 시스템의 이해 가능성이 높아지지만, **고수준 책임을
    층 나누기와 결합하면 시스템의 조직 원리를 얻는다**는 것이 저자의 계산이다 (16장,
    p.451).[^evans2003]
- 어느 층 나누기 판본인가가 곁글로 명시된다 (16장, p.451):[^evans2003]

> The layering pattern that serves best for RESPONSIBILITY LAYERS is the variant called RELAXED
> LAYERED SYSTEM (Buschmann et al. 1996, p. 45), which allows components of a layer to access any
> lower layer, not just the one immediately below.

## 조항

- 처방 문단 (16장, p.451):[^evans2003]

> Look at the conceptual dependencies in your model and the varying rates and sources of change
> of different parts of your domain. If you identify natural strata in the domain, cast them as
> broad abstract responsibilities. These responsibilities should tell a story of the high-level
> purpose and design of your system. Refactor the model so that the responsibilities of each
> domain object, AGGREGATE, and MODULE fit neatly within the responsibility of one layer.

- 조항이 걸리는 곳이 셋으로 명시된다 — **도메인 객체와 애그리게이트와 모듈**. 즉 층은 코드의
  산물이 아니면서도 코드의 모든 단위를 구속한다.
- 저자가 층 나누기를 좋은 효과로 본 도메인으로 제조 공정 통제와 금융 관리를 들고, 이 장을 여는
  위성 통신 시뮬레이터 사례도 자기 책임을 층으로 나눈 것이라고 밝힌다 (16장,
  pp.451–452).[^evans2003]

## 사례 — 화물 운송 시스템에 층을 입히기

예제 "In Depth: Layering a Shipping System"은 앞선 장들의 화물 운송 모델을 그대로 이어받는다
(16장, pp.452–457).[^evans2003] 팀은 모델 주도 설계와 핵심 도메인 증류에서 상당한 진전을
이뤘으나 **모든 부분이 어떻게 맞물리는지를 조율하는 데 어려움을 겪고** 있었다.

### 두 층으로 시작한다

- 팀이 몇 달간 도메인에 잠긴 끝에 관찰한 성층 — **운송 일정(배와 기차의 예정된 항해)을 그 위에
  실린 화물을 언급하지 않고 논하는 것은 꽤 자연스럽다. 반면 화물 추적을 그것을 나르는 운송을
  언급하지 않고 말하기는 더 어렵다** (16장, p.453).[^evans2003]
  - 개념적 의존이 명확해서 팀은 두 층을 쉽게 구분한다 — **운영(Operations)**과 그 운영의
    바탕인 **능력(Capability)**.
- **운영 책임** — 회사의 과거·현재·계획된 활동. 가장 뚜렷한 운영 객체가 `Cargo`이고,
  `Route Specification`은 배송 요구를 나타내는 `Cargo`의 필수 부분, `Itinerary`는 운영상의
  배송 계획이다. **둘 다 `Cargo`의 애그리게이트에 속하고 생애 주기가 활성 배송의 시간 틀에
  묶인다** (16장, p.453).[^evans2003]
- **능력 책임** — 운영을 수행하기 위해 회사가 끌어다 쓰는 자원. `Transit Leg`이 전형이다 —
  배는 운항하도록 편성되어 있고 일정한 적재 능력을 가지며 그것이 다 차기도 하고 아니기도 하다
  (16장, pp.453–454).[^evans2003]
- **배치가 기술적 판정이 아니라는 것이 두 사례로 드러난다** (16장, p.454):[^evans2003]
  - `Transit Leg`은 **선단 운영이 초점이었다면 운영 층에 있었을 것**이다. 이 시스템의 사용자는
    그 문제를 걱정하지 않기에 능력 층에 있다. 회사가 두 활동을 다 하고 조율까지 원했다면
    "운송 운영"과 "화물 운영" 같은 별도의 두 층을 고려했을 수 있다.
  - `Customer`의 배치가 더 까다롭다. **어떤 사업에서는 고객이 일시적이다** — 소포가 배송되는
    동안만 흥미롭고 다음번까지 대체로 잊힌다. 그러면 고객은 운영 관심사일 뿐이다. 그러나 이
    가상의 해운 회사는 장기 관계를 가꾸고 대부분의 일이 반복 거래에서 온다. 그래서
    **`Customer`는 잠재력 층에 든다.**
  - 저자의 단서 — **보다시피 이것은 기술적 결정이 아니었다. 도메인 지식을 포착하고 소통하려는
    시도였다** (16장, p.454).[^evans2003]
- 층이 설계를 강제하는 첫 실례도 여기서 나온다 — `Cargo`와 `Customer`의 연관이 한 방향으로만
  통행 가능하므로 **`Cargo` 리포지터리에 특정 `Customer`의 모든 `Cargo`를 찾는 질의가
  필요해진다. 어차피 그렇게 설계할 좋은 이유가 있었지만, 대규모 구조를 부과한 뒤로는 그것이
  요구 사항이 된다** (16장, p.454).[^evans2003]

### 셋째 층이 나온다

- 몇 주의 실험 끝에 다른 구분이 드러난다 — **두 초기 층은 대체로 상황이나 계획을 있는 그대로
  다룬다. 그런데 `Router`는 현재의 운영 현실이나 계획의 일부가 아니다. 그 계획을 바꾸는 결정을
  돕는다.** 팀은 **의사 결정 지원(Decision Support)** 층을 정의한다 (16장,
  p.455).[^evans2003]
  - `Router`는 예약 담당자가 화물을 보낼 최선의 길을 고르도록 돕는 서비스이므로 의사 결정
    지원에 정확히 놓인다.
- 그러자 구조에 맞지 않는 요소 하나가 드러난다 — `Transport Leg`의 "is preferred" 속성이다
  (16장, p.455).[^evans2003]
  - 그 속성은 회사가 가능하면 자기 배를, 또는 유리한 계약을 맺은 다른 회사의 배를 선호하기
    때문에 존재하고, `Router`가 그쪽으로 기울도록 편향을 주는 데 쓰인다.
  - 판정 — **이 속성은 "능력"과 아무 상관이 없다. 그것은 의사 결정을 지시하는 정책이다.**
    새 책임 층을 쓰려면 모델을 리팩터링해야 한다.
- 리팩터링의 결과와 그 부수 효과 — 편향은 `Route Bias Policy`로 떨어져 나오고 `Transport Leg`
  에는 능력 책임만 남는다. 저자가 일반화한다 (16장, p.456):[^evans2003]

> A large-scale structure based on a deep understanding of the domain will often push the model
> in directions that clarify its meaning.

- 층의 값이 언제 커지는지도 적힌다 — **고른 층에 익숙한 개발자는 부분들의 역할과 의존을 더
  쉽게 분간할 수 있다. 대규모 구조의 값은 복잡도가 자랄수록 커진다** (16장,
  p.457).[^evans2003]

## 구조가 이후 설계를 어떻게 구속하는가

§"How Does This Structure Affect Ongoing Design?"이 구조의 비용을 실물로 보인다
(16장, pp.457–460).[^evans2003]

- 새 요구 — 어떤 위험물 범주에는 항로 제약이 적용된다. 특정 물질은 어떤 운송이나 어떤 항구에
  실릴 수 없고, `Router`가 이 규제를 지켜야 한다 (16장, p.457).[^evans2003]
- **구조가 없을 때 매력적인 설계** — 항로 명세와 위험물 코드를 함께 소유한 객체, 즉 `Cargo`에
  규칙 적용 책임을 준다 (16장, p.457).[^evans2003]
- **기각 사유** (16장, p.458):[^evans2003]
  - 문제는 `HazMat Route Policy Service` 자체가 아니다. 그것은 의사 결정 지원 층의 책임에
    정확히 들어맞는다.
  - 문제는 **운영 객체인 `Cargo`가 의사 결정 지원 객체인 `HazMat Route Policy Service`에
    의존한다**는 것이다. **프로젝트가 이 층들에 헌신하는 한 이 모델은 허용될 수 없다.
    구조가 지켜지리라 기대한 개발자들을 혼란시킬 것이다.**
- **대안** — 정책을 쓰는 책임을 `Router`로 옮긴다. `Router`가 경로를 찾기 전에 적절한 정책들을
  모으고, 그러려면 정책이 의존할 수 있는 객체들을 받도록 `Router` 인터페이스를 바꾼다
  (16장, p.458).[^evans2003]
- 이 절의 결론이 구조의 값을 규정한다 (16장, p.460):[^evans2003]

> Now, this isn't necessarily a better design than the other. They both have pros and cons. But
> if everyone on a project makes decisions in a consistent way, the design as a whole will be
> much more comprehensible, and that is worth some modest trade-offs on detailed design choices.

  - **더 나은 설계라고 주장하지 않는다.** 값은 일관성에서 오고, 그 값이 세부 설계의 온건한
    맞바꿈을 정당화한다.
- 그리고 곧바로 되돌이 조항이 붙는다 — **구조가 어색한 설계 선택을 많이 강요한다면 질서의
  진화에 따라 평가해 수정하거나 폐기해야 한다** (16장, p.460).[^evans2003]

## 층을 고를 때 지켜야 할 성질 셋

§"Choosing Appropriate Layers"는 먼저 출발점의 부담을 덜어 준다 — **좋은 책임 층이나 어떤
대규모 구조든 찾는 일은 문제 도메인을 이해하고 실험하는 문제다. 질서의 진화를 허용한다면 초기
출발점은 결정적이지 않다. 다만 잘못 고르면 일이 늘어난다. 구조는 알아볼 수 없는 것으로 진화할
수도 있다** (16장, p.460).[^evans2003] 그래서 아래 지침은 처음 고를 때뿐 아니라 **구조를
변형할 때도** 적용된다.

층이 바뀌고 합쳐지고 갈라지고 재정의되는 동안 **찾아보고 보존해야 할 쓸모 있는 성질**
셋 (16장, p.461):[^evans2003]

| 성질 | 원문의 요구 |
|---|---|
| **이야기하기(Storytelling)** | 층은 도메인의 기본적 현실이나 우선순위를 소통해야 한다. **대규모 구조를 고르는 것은 기술적 결정이라기보다 사업 모델링 결정이다.** 층은 사업의 우선순위를 드러내야 한다 |
| **개념적 의존(Conceptual dependency)** | "위" 층의 개념은 "아래" 층을 배경으로 놓을 때 뜻을 갖고, 아래 층의 개념은 홀로 서도 뜻이 있어야 한다 |
| **개념의 윤곽(CONCEPTUAL CONTOURS)** | 서로 다른 층의 객체가 변화의 속도나 출처가 다르다면, 층이 그 사이의 전단(shearing)을 수용한다 |

- 저자는 매번 백지에서 시작할 필요는 없다고 적는다 — **어떤 층들은 관련된 도메인 가족 전체에
  걸쳐 나타난다** (16장, p.461).[^evans2003]

## 되풀이해 나타나는 다섯 층

- 첫 두 층이 서는 조건 — **공장이나 화물선처럼 큰 고정 자본 자산을 활용하는 사업에서 물류
  소프트웨어는 흔히 "잠재력(Potential)" 층과 "운영(Operations)" 층으로 조직될 수 있다**
  (16장, p.461).[^evans2003] 잠재력은 앞 예제에서 "능력"이라 부른 층의 다른 이름이다.

| 층 | 묻는 것 | 무엇이 드는가 |
|---|---|---|
| **잠재력(Potential)** | 무엇을 할 수 있는가. 우리가 무엇을 하려는지는 접어 두고, 무엇을 할 수 있는가 | 조직의 자원(사람 포함)과 그 자원이 조직된 방식. 공급자와의 계약도 잠재력을 정의한다. **거의 모든 사업 도메인에서 알아볼 수 있으나, 운송·제조처럼 사업을 가능하게 하는 고정 자본 투자가 비교적 큰 쪽에서 이야기의 두드러진 부분이 된다.** 일시적 자산도 포함하나, 주로 일시적 자산으로 굴러가는 사업은 그것을 강조하는 다른 층을 고를 수 있다 |
| **운영(Operation)** | 무엇이 행해지고 있는가. 그 잠재력으로 무엇을 만들어 냈는가 | 잠재력 층처럼 **원하는 바가 아니라 상황의 현실을 반영해야 한다.** 이 층에서 보려는 것은 우리 자신의 노력과 활동이다 — **무엇이 우리를 팔 수 있게 하는가가 아니라 우리가 무엇을 팔고 있는가.** 운영 객체가 잠재력 객체를 참조하거나 그것으로 구성되는 것은 아주 전형적이지만, **잠재력 객체는 운영 층을 참조해서는 안 된다** |
| **의사 결정 지원(Decision Support)** | 어떤 행동을 취해야 하는가, 어떤 정책을 세워야 하는가 | 분석과 의사 결정. **잠재력이나 운영 같은 아래층의 정보에 근거해 분석하고**, 이력 정보를 써서 현재와 미래 운영의 기회를 능동적으로 찾기도 한다 |
| **정책(Policy)** | 규칙과 목표는 무엇인가 | 규칙과 목표는 **대체로 수동적이지만 다른 층의 행동을 제약한다.** 이 상호작용의 설계는 미묘할 수 있다 — 정책을 하위 메서드에 인자로 넘기기도 하고 전략(STRATEGY) 패턴을 쓰기도 한다. **정책은 의사 결정 지원 층과 함께 잘 작동한다** — 그쪽이 정책이 세운 목표를 정책이 세운 규칙의 제약 아래 추구하는 수단을 준다 |
| **확약(Commitment)** | 우리가 무엇을 약속했는가 | **미래 운영을 지시하는 목표를 진술한다는 점에서 정책의 성격을 갖고, 확약이 지속적인 사업 활동의 일부로 생겨나고 변한다는 점에서 운영의 성격을 갖는다** |

- 많은 기존 시스템에서는 잠재력과 운영 둘로 충분하다 — **그것들은 현재 상황과 활성 운영 계획을
  추적하고 그에 관한 보고서나 문서를 낸다. 그러나 추적만으로는 늘 충분하지 않다.** 사용자를
  인도하거나 돕거나 의사 결정을 자동화하려 할 때 운영 위에 또 한 층이 생긴다 (16장,
  p.462).[^evans2003]
- 의사 결정 지원의 구현에 관한 관찰 — **많은 프로젝트가 의사 결정 지원을 데이터 웨어하우스
  기술로 구현한다. 그러면 그 층은 별개의 경계 컨텍스트가 되어 운영 소프트웨어와
  고객/공급자 관계를 맺는다.** 다른 프로젝트에서는 앞의 확장 예제처럼 더 깊이 통합된다
  (16장, p.462).[^evans2003]
  - 층 나누기의 본래 이점 하나가 여기서 나온다 — **아래층이 위층 없이 존재할 수 있다는 것.
    이것이 단계적 도입이나 오래된 운영 시스템 위에 얹는 고수준 확장을 쉽게 한다** (16장,
    p.462).[^evans2003]
- 정책 층의 구현 — **정책 층은 다른 층과 같은 언어로 쓸 수도 있지만 때로는 규칙 엔진으로
  구현된다. 그것이 반드시 별개의 경계 컨텍스트를 만들지는 않는다** (16장,
  pp.462–463).[^evans2003]

> In fact, the difficulty of coordinating such different implementation technologies can be
> eased by fastidiously using the same model across both. When rules are written based on a
> different model than the objects they apply to, either the complexity goes way up or the
> objects get dumbed down to keep things manageable.

- 확약 층이 나오는 조건 — **많은 사업은 설비와 장비에 능력의 근거를 두지 않는다. 금융 서비스나
  보험이 그렇고, 거기서는 잠재력이 상당 부분 현재 운영에 의해 결정된다.** 보험사가 새 계약을
  인수해 위험을 떠안을 능력은 현재 사업의 분산에 근거한다. **그러면 잠재력 층은 운영으로
  합쳐지고 다른 층 나누기가 진화한다.** 그런 상황에서 앞으로 나오는 것이 고객에게 한 확약이다
  (16장, pp.463–464).[^evans2003]
- **잠재력과 확약은 배타적이지 않다** — 맞춤 운송 서비스를 많이 하는 운송 회사처럼 둘 다
  두드러진 도메인은 둘 다 쓸 수 있다 (16장, p.464).[^evans2003]
- 저자는 이 다섯 층을 각각 **변화 속도**와 함께 도해로 놓는다 — 공장 자동화 시스템과 투자
  은행 시스템 두 판이고, 각 층의 왼쪽에 그 층이 담는 것의 성격을, 가운데에 상태 변화 속도를,
  오른쪽에 실물 예를 적는 세 칸짜리 그림이다 (16장, pp.463·464, Figure
  16.13·16.14).[^evans2003] 도판이라 옮기지 않았고, 그림이 나르는 판정은 **개념적 의존과
  전단점(shearing points)이 변화 속도의 차이에서 드러난다**는 것이다.

## 층의 개수에는 상한이 있다

- 한계 (16장, p.464):[^evans2003]

> But it is best to keep the layering system simple; going beyond four or possibly five becomes
> unwieldy. Having too many layers isn't as effective at telling the story, and the problems of
> complexity the large-scale structure was meant to solve will come back in a new form. The
> large-scale structure must be ferociously distilled.

  - **구조 자체가 증류의 대상이 된다.** 층이 많아지면 구조가 풀려던 복잡도 문제가 다른 모습으로
    되돌아온다.
- 이 다섯 층이 보편적이지 않다는 단서 — **이 다섯 층이 여러 기업 시스템에 적용 가능하지만 모든
  도메인의 두드러진 책임을 포착하지는 않는다. 다른 경우에는 설계를 이 모양에 억지로 맞추려는
  것이 역효과를 낼 것이고, 그래도 통하는 자연스러운 책임 층이 있을 수 있다. 우리가 논한 것과
  전혀 무관한 도메인이라면 층이 완전히 독창적이어야 할 수도 있다** (16장,
  p.464).[^evans2003]
- 절을 닫는 문장이 다시 메타 조항을 부른다 — **결국 직관을 쓰고, 어디선가 시작하고, 질서가
  진화하게 두어야 한다** (16장, p.464).[^evans2003]

## 이 층 나누기는 계층 아키텍처가 아니다

- 두 층 나누기는 같은 책에서 서로 다른 것을 가른다. 4장의
  [계층 아키텍처](../concepts/layered-architecture.md)는 **사용자 인터페이스·애플리케이션·도메인·기반
  구조라는 기술적 관심사**로 가르고, 이 패턴은 **도메인 층 안에서 도메인의 책임**으로 가른다.
  - 저자 자신이 이 장의 도입에서 도메인 층의 대규모 구조가 기술 아키텍처와 달리 많이 탐구되지
    않았다고 적어 둘을 갈라 놓는다 (16장, p.444).[^evans2003]
  - 두 구조는 겹치지 않고 포개진다 — 책임 층은 계층 아키텍처의 **도메인 층 안쪽**을 다시
    가른다. #hypothesis 저자가 이 포개짐을 한 문장으로 명시한 대목은 이 장에 없다. 근거는
    이 장이 다루는 대상이 시종 도메인 모델의 객체·애그리게이트·모듈이고 4장의 네 층 중
    어느 것도 이 장에서 언급되지 않는다는 것이다.

## 레거시에도 층 안의 자리를 준다

17장이 이 패턴을 현실의 제약과 함께 쓰는 법을 따로 다룬다. 위 [조항](#조항)은 모든 객체와
애그리게이트와 모듈이 한 층 안에 들도록 리팩터링하라고 요구하는데, 손댈 수 없는 시스템이 있을
때 그 요구가 어떻게 되는가 하는 물음이다.

- 답 — **책임 층을 채택하고 싶은데 조직이 바라는 대규모 구조와 맞지 않는 레거시 시스템이 있다고
  하자. 층을 포기해야 하는가? 아니다. 그러나 그 구조 안에서 레거시가 실제로 차지하는 자리를
  인정해야 한다** (17장, p.487).[^evans2003]
- 그리고 그 인정이 소득이 된다 — **사실 레거시를 성격 짓는 데 도움이 될 수 있다. 레거시가
  제공하는 서비스는 실제로 몇 개 층에만 갇혀 있을 수 있다. 레거시 시스템이 특정 책임 층 안에
  든다고 말할 수 있다는 것은 그 시스템의 범위와 역할의 핵심 측면을 간결하게 기술한다** (17장,
  p.487).[^evans2003]
  - **층 이름이 리팩터링 대상이 아닌 것까지 서술하는 어휘가 되는 자리다.** 위
    [사례 — 화물 운송 시스템에 층을 입히기](#사례--화물-운송-시스템에-층을-입히기)가 모델을
    실제로 옮겨 층에 맞췄다면, 여기서는 옮기지 않은 채 자리만 정한다.
- 파사드가 있으면 경계를 맞출 여지가 생긴다 — **레거시 서브시스템의 능력이 파사드(FACADE)를 통해
  접근되고 있다면, 파사드가 제공하는 각 서비스를 한 층 안에 들도록 설계할 수 있을지도 모른다**
  (17장, p.488).[^evans2003]
  - [부패 방지 계층](../concepts/anticorruption-layer.md)의 파사드에 요구가 하나 더 붙는 셈이다 —
    서비스 하나가 여러 층에 걸치지 않게 자르라는 것이다.
- 레거시 내부는 열지 않아도 된다 — 레거시는 **분화되지 않은 덩어리로 제시**되고, 그 대신
  **컨텍스트 지도에 걸친 대규모 구조가 잘 확립된 프로젝트의 팀은 자기 컨텍스트 안에서 같은
  익숙한 층으로 모델을 정돈하기를 택할 수도 있다** (17장, p.488).[^evans2003]
  - 같은 층 이름이 컨텍스트 지도 위에서도, 각 컨텍스트 안에서도 쓰인다는 뜻이다. 두 배치의
    전문은 [전략 패턴을 함께 쓰기](../concepts/combining-strategic-patterns.md)에 있다.

## 이어지는 페이지

- [대규모 구조](../concepts/large-scale-structure.md) — 이 패턴이 놓인 장의 틀
- [질서의 진화](../concepts/evolving-order.md) — 층을 고르고 버리는 것을 지배하는 조항
- [계층 아키텍처](../concepts/layered-architecture.md) — 같은 낱말을 기술적 관심사로 쓰는 다른 층 나누기
- [지식 수준](../concepts/knowledge-level.md) — 정책 층의 특수 사례처럼 보이지만 아닌 구조
- [개념의 윤곽](../concepts/conceptual-contours.md) — 층이 전단을 수용해야 하는 근거
- [화물 운송 예제](../concepts/cargo-shipping-example.md) — 이 예제가 이어받는 모델
- [전략 패턴을 함께 쓰기](../concepts/combining-strategic-patterns.md) — 이 층들이 경계 컨텍스트와 놓이는 두 배치
- [부패 방지 계층](../concepts/anticorruption-layer.md) — 레거시가 층에 맞춘 서비스를 내놓는 자리
- [도메인의 모듈](../concepts/modules-in-the-domain.md) — 층이 구속하는 단위 하나
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 층이
  구속하는 또 하나의 단위
- [도메인 서비스](../concepts/domain-services.md) — `Router`가 서 있는 자리
- [모델링 패러다임](../concepts/modeling-paradigms.md) — 정책 층이 규칙 엔진으로 구현될 때의 조건
- [명시적 제약](../concepts/explicit-constraints.md) — 정책이 객체로 떨어져 나오는 동작
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §RESPONSIBILITY LAYERS(pp.450–464) —
    문제 서술과 층의 정의(p.450) · RELAXED LAYERED SYSTEM 곁글과 처방 문단(p.451) ·
    예제 "In Depth: Layering a Shipping System"(pp.452–460, §"'Operational'
    Responsibilities" p.453 · §"'Capability' Responsibilities" pp.453–454 ·
    §"'Decision Support' Responsibilities" p.455 · §"How Does This Structure Affect Ongoing
    Design?" pp.457–460 포함) · §"Choosing Appropriate Layers"(pp.460–464) ·
    §EVOLVING ORDER의 도메인 아키텍처 관찰(p.444) · 17장 "Bringing the Strategy Together"
    §"Combining Large-Scale Structures and BOUNDED CONTEXTS"(pp.487–488). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측).
    원문이 패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서 유지했다. 도판 전부
    (Figure 16.2 임시 층 나누기 · 16.3 기본 해운 모델 · 16.4 예약 시 라우팅 시퀀스 ·
    16.5 질의가 양방향 연관을 대체하는 도해 · 16.6 첫 층 모델 · 16.7 리팩터링 전후 ·
    16.8 재구조화된 모델 · 16.9~16.12 위험물 라우팅 두 설계와 각각의 시퀀스 ·
    16.13 공장 자동화의 전단점 · 16.14 투자 은행의 전단점)와 패턴 도비라의 사진(p.450)은
    이미지라 옮기지 않았고 딸린 판정 산문과 클래스·속성 이름만 옮겼다. **이 절에는 코드
    목록이 없다** — 이 페이지에 펜스가 없는 이유다. 표 안의 굵은 글씨는 원문 문장의 한국어
    재서술이고 괄호 안이 그 쪽이다.

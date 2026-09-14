---
type: concept
title: 분석 패턴을 모델에 들이기
description: 남이 정리해 둔 분석 패턴을 내 도메인 모델에 어떻게 빌려 쓰는가 — 파울러의 정의와 그 이름이 전하지 못하는 것, 이 패턴이 나르는 것은 모델이 아니라 성숙한 프로젝트의 경험이라는 규정, 맥락 없이 모델 발상만 논하면 분석과 설계 사이의 치명적 균열이 열린다는 경고, 계정과 기표와 보존과 복식부기라는 회계 기본 모델, 빌린 개념 중 거래는 기각되고 발생이라는 낱말은 남은 첫 대화, 객체 관계 매핑이 모델을 한 칸 물린 자리, 기표 규칙과 발화 방식 셋이 어휘로 들어오는 둘째 대화, 원전에서 떠나도 되는 것과 이름의 기본 개념만은 지켜야 한다는 단 하나의 금지, 그리고 이 재적용이 프레임워크나 컴포넌트를 통한 코드 재사용과 완전히 다른 것이라는 판정, 그리고 같은 책에서 온 지식 수준이 도메인이 아니라 모델을 구조화하기에 분석 패턴 목록 밖에 서는 예외
generated: { by: "claude-opus-5", at: "2026-09-14T16:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 분석 패턴을 모델에 들이기

- [분석 패턴이란 무엇인가](#분석-패턴이란-무엇인가)
- [이름이 전하지 못하는 것](#이름이-전하지-못하는-것)
- [이 패턴이 나르는 것은 성숙한 프로젝트의 경험이다](#이-패턴이-나르는-것은-성숙한-프로젝트의-경험이다)
- [빌려 온 회계 모델 — 계정과 기표](#빌려-온-회계-모델--계정과-기표)
- [첫 대화 — 무엇이 남고 무엇이 버려졌는가](#첫-대화--무엇이-남고-무엇이-버려졌는가)
- [기반 구조가 모델을 한 칸 물리는 자리](#기반-구조가-모델을-한-칸-물리는-자리)
- [둘째 대화 — 기표 규칙과 발화 방식 셋](#둘째-대화--기표-규칙과-발화-방식-셋)
- [어휘가 모델 객체만큼 중요하다](#어휘가-모델-객체만큼-중요하다)
- [원전에서 떠나도 되는 것과 지켜야 하는 것](#원전에서-떠나도-되는-것과-지켜야-하는-것)
- [코드 재사용과 완전히 다르다](#코드-재사용과-완전히-다르다)
- [증류에서 이 선택지가 서는 자리](#증류에서-이-선택지가-서는-자리)
- [같은 책에서 온, 도메인이 아니라 모델을 구조화하는 패턴](#같은-책에서-온-도메인이-아니라-모델을-구조화하는-패턴)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **남이 정리해 출판해 둔 모델 조각을 내 도메인에 빌려 쓰되, 그것이 내 모델을
일그러뜨리지 않게 하려면 무엇을 지켜야 하는가.**

## 분석 패턴이란 무엇인가

- 이 장이 다루는 것은 II부의 기본 구성 요소 패턴이나 10장의 유연한 설계 원칙과 층위가
  다르다 — 그것들보다 **더 높은 수준이고 더 특화되어 있으며, 어떤 개념을 표상하기 위해
  객체 몇 개를 쓰는 것을 포함한다** (11장, p.293).[^evans2003] 얻는 것은 출발점이다.
  **이미 표현력 있고 구현 가능하며 배우자면 비쌌을 미묘함을 다루는 모델에서 시작하게
  해 준다**는 것이고, 거기서부터 리팩터링하고 실험한다 (11장, p.293).[^evans2003]
- 그리고 곧바로 지위가 한 문장으로 못 박힌다 (11장, p.293).[^evans2003]

> These are not out-of-the-box solutions.

- 정의는 저자 자신의 것이 아니라 이 개념을 만든 책의 것을 그대로 옮긴다. 마틴 파울러
  (Martin Fowler)의 *Analysis Patterns: Reusable Object Models*에서 (11장,
  p.293):[^evans2003]

> Analysis patterns are groups of concepts that represent a common construction in business
> modeling. It may be relevant to only one domain or it may span many domains.
> [Fowler 1997, p. 8]

- 이름이 강조하는 것이 개념적 성질이라는 해설이 붙는다 — **분석 패턴은 기술적 해법이
  아니다. 그것은 특정 도메인에서 모델을 짜 내는 일을 돕는 안내서다** (11장,
  p.294).[^evans2003]

## 이름이 전하지 못하는 것

- **"분석"이라는 이름이 이 패턴의 절반을 감춘다**는 것이 이 절의 요점이다 (11장,
  p.294):[^evans2003]

> What the name unfortunately does not convey is that there is significant discussion of
> implementation in these patterns, including some code.

- 저자가 그 근거로 파울러 자신의 문장을 든다. 배포 이후, 곧 현장에서의 장기 유지 보수까지
  내다본 대목이다 (11장, p.294).[^evans2003]

> When we build a new [accounting] practice, we create a network of new instances of the
> posting rule. We can do this without any recompilation or rebuilding of the system, while
> it is still up and running. There will be unavoidable occasions when we need a new subtype
> of posting rule, but these will be rare. [p. 151]

  - **이 인용의 자리가 이 페이지에서 중요하다.** 모델 선택 하나가 몇 년 뒤 무엇을 재컴파일
    없이 바꿀 수 있게 하는가를 말하는 문장이고, 그것이 "분석"이라는 낱말 아래 들어 있다.

## 이 패턴이 나르는 것은 성숙한 프로젝트의 경험이다

- 성숙한 프로젝트에서는 모델 선택이 애플리케이션 경험에 근거해 이루어진다. 여러 구성 요소의
  여러 구현이 시도되었고 일부는 운영에 들어가 유지 보수 단계까지 겪었으므로, 그런 경험이
  있으면 많은 문제를 피할 수 있다 (11장, p.294).[^evans2003]
- 분석 패턴이 하는 일이 그것이다 — **가장 좋을 때 분석 패턴은 그런 종류의 경험을 다른
  프로젝트에서 실어 오며, 모델 통찰을 설계 방향과 구현 결과에 대한 폭넓은 논의와 결합한다**
  (11장, p.294).[^evans2003]
- **그래서 맥락을 떼면 위험해진다** (11장, p.294):[^evans2003]

> To discuss model ideas out of that context makes them harder to apply and risks opening the
> deadly divide between analysis and design, which is antithetical to MODEL-DRIVEN DESIGN.

  - 이 경고가 [모델 주도 설계](model-driven-design.md)의 조항이 이 장에서 회수되는
    자리다. 분석과 설계를 가르는 균열은 그 조항이 애초에 막으려 한 것이다.

## 빌려 온 회계 모델 — 계정과 기표

- 이 장의 예제는 이자 수익 자산을 추적하는 애플리케이션이고, 개발자가 파울러 책의 6장
  "Inventory and Accounting"을 읽는다. 저자가 옮긴 요약이 아래다 (11장,
  pp.295–296).[^evans2003]
- 출발 동기 — 온갖 업무 애플리케이션이 가치를 담는 계정(account)을 추적하는데, 많은
  경우 계정의 금액만 아는 것으로는 모자라고 **그 금액의 변화 하나하나를 설명하고 통제하는
  것이 필수적**이다 (11장, p.295).[^evans2003]
- 기본 모델의 규정 (11장, p.296):[^evans2003]

> Value can be added by inserting an Entry. Value can be removed by inserting a negative
> Entry. Entries are never removed, so the whole history is retained. The balance is the
> combined effect of all Entries. This balance could be computed on demand or cached, an
> implementation decision that is encapsulated by the Account interface.

  - **잔액이 계산이냐 캐시냐가 계정 인터페이스 뒤에 감춰진다는 단서가 이 모델의 설계
    성분이다.** 이 자리가 [정보 은닉과 누출](information-hiding-and-leakage.md)의
    조항과 같은 것을 말한다.
- 둘째 원리는 보존이다 — **회계의 기본 원리 하나가 보존(conservation)이다. 돈은 어디선가
  나타나지 않고, 흔적 없이 사라지지도 않는다. 그것은 한 계정에서 다른 계정으로 옮겨질
  뿐이다** (11장, p.296).[^evans2003] 거래(Transaction) 객체가 그 원리를 표상하며
  기표 금액의 합이 0이라는 제약을 건다.
- 그 원리의 이름도 함께 온다 — **이것이 확립된 개념인 복식부기(double-entry bookkeeping)다.
  모든 대변에는 짝이 되는 차변이 있다. 물론 다른 보존 원리와 마찬가지로 그것은 닫힌 계,
  곧 모든 원천과 귀착지를 포함하는 계에만 적용된다. 많은 단순한 애플리케이션은 이 엄밀함을
  요구하지 않는다** (11장, p.296).[^evans2003]
  - **같은 발상이 이 KB의 데이터 시스템 축에도 있다.**
    [상태·스트림·불변성](../concepts/state-streams-and-immutability.md)이 회계 원장(ledger)의
    추가 전용 불변성과 정정 기표를 다루고, 거기서 판정 심급은 감사 가능성이다. 여기서는
    같은 성질이 **도메인 모델의 구성 요소**로 들어온다. 두 페이지가 같은 관행을 서로 다른
    물음에 쓰므로 어느 쪽도 다른 쪽을 대신하지 않는다.

## 첫 대화 — 무엇이 남고 무엇이 버려졌는가

- 개발자 둘이 읽은 것을 모델에 얹어 도메인 전문가와 대화한다. **빌린 개념 셋 중 하나가 그
  자리에서 기각된다** (11장, pp.297–299).[^evans2003]
  - 기표(Entry)는 남는다. 이자 금액을 고쳐 쓰는 대신 이자 계정에 기표를 넣으면 발생과 지급의
    이력이 남고, 전문가가 그것을 **우리가 원하던 것**이라 반긴다 (11장, p.297).[^evans2003]
  - 거래(Transaction)는 기각된다. 개발자 자신이 먼저 의심한다 — 그 정의는 한 계정에서 다른
    계정으로 돈이 옮겨 가는 것을 말하지 **같은 계정 안에서 서로를 상쇄하는 기표 둘**을 말하지
    않는다는 것이다 (11장, p.297).[^evans2003] 전문가가 그 의심을 확정한다. 발생과 지급을
    묶을 이유가 없고 회계 시스템에서 그 둘은 별개의 기표이며, 하나의 발생에 하나의 지급이라는
    도식 자체가 틀렸다는 것이다 (11장, p.298).[^evans2003]
  - **그리고 개발자가 낱말 하나를 묻는다.** 전문가가 몇 번 쓴 "발생(accruals)"을 설명해 달라고
    하자, 돈이 실제로 오가는 시점과 무관하게 비용이나 수입이 발생한 때에 회계 처리하는 것이라는
    답이 온다 (11장, p.298).[^evans2003] 개발자의 반응이 이 장 전체의 성과를 요약한다 —
    **네, 우리에게 정말로 그런 낱말이 필요했습니다** (11장, p.298).[^evans2003]
- 계정(Account)의 운명은 전문가가 정한다. 개발자가 계정 없는 단순한 안을 그리자 전문가가
  **그러면 계정 객체를 안 갖게 되는 건가요? 발생과 지급과 잔액을 거기서 한꺼번에 볼 수
  있기를 기대하고 있었는데요**라고 되묻고, 계정을 되살린 안이 채택된다 (11장,
  pp.298–299).[^evans2003]
  - **판정 심급이 전문가의 입이라는 것이 이 대화의 구조다.** 빌린 개념의 생사를 책이 아니라
    도메인 전문가가 정한다. 같은 계측기를 쓰는 절차가
    [암묵적 개념 파내기](digging-out-implicit-concepts.md)에 있다.
- 코드로 내려가면서 모델이 한 번 더 정련된다. 기표는 지급(Payment)과 발생(Accrual)으로
  하위 분류되었는데 **애플리케이션에서 책임이 조금 달랐고 둘 다 중요한 도메인 개념이었기
  때문**이다. 반대로 수수료에서 왔는지 이자에서 왔는지는 기표 사이의 개념적·행동적 구분을
  만들지 않았다 (11장, p.299).[^evans2003]

## 기반 구조가 모델을 한 칸 물리는 자리

- 그런데 마지막 추상은 구현 때문에 포기된다. 데이터가 관계형 테이블에 저장되고, 프로그램을
  돌리지 않고도 테이블을 해석할 수 있게 한다는 프로젝트 표준이 있어서 수수료 기표와 이자
  기표를 다른 테이블에 두어야 했다. 쓰던 객체 관계 매핑(object-relational mapping)
  프레임워크에서 그것을 하는 유일한 방법이 구상 하위 클래스를 만드는 것이었다 (11장,
  pp.299–300).[^evans2003] 다른 기반 구조였다면 이 **어설픈 확장**을 피했을 것이라는 단서가
  붙는다.
- 저자가 이 대목을 왜 넣었는지 스스로 밝힌다 (11장, p.300):[^evans2003]

> I threw this twist into this largely fictitious story to represent the rub of reality that
> we encounter all the time. We have to make calculated compromises and then move on without
> letting it throw us off our MODEL-DRIVEN DESIGN.

  - **"계산된 타협"과 "모델 주도 설계에서 밀려나지 않는 것"이 한 문장 안에 있다는 점이
    이 진술의 무게다.** 같은 종류의 양보를 다루는 자리가
    [관계형 데이터베이스를 위한 객체 설계](designing-objects-for-relational-databases.md)다.
- 그 대가를 치른 뒤의 이득도 계상된다 — 가장 복잡한 기능이 부수 효과 없는 함수에 들어가
  새 설계가 분석하고 시험하기 훨씬 쉬워졌고, 남은 명령 하나는 여러 함수를 호출하는 단순한
  코드이며 단언으로 특징지어진다 (11장, p.300).[^evans2003] 두 조항의 전문은
  [부수 효과 없는 함수](../concepts/side-effect-free-functions.md)와
  [단언](assertions-pattern.md)에 있다.

## 둘째 대화 — 기표 규칙과 발화 방식 셋

- 이 예제의 둘째 갈래는 **도메인 모델의 이득을 볼 수 있으리라고 아무도 의심하지 않던 자리**를
  겨눈다. 야간 배치 스크립트다. 그런 부분은 단순하게 시작해 기계적으로 자라서 도메인 로직이
  아니라 복잡한 애플리케이션 코드처럼 보이는데, **분석 패턴은 그런 사각지대를 보여 주는 데
  특히 쓸모 있다** (11장, p.300).[^evans2003]
- 빌려 온 개념은 기표 규칙(Posting Rules)이다. 문제는 계정 사이의 자동 갱신이다. 한 계정이
  수입을 추적하고 다른 계정이 그 수입의 추정 세금을 추적할 때 시스템이 세금 계정을 자동으로
  갱신해야 한다면 두 계정의 구현이 아주 엉킨다. **계정 기표의 대부분이 그런 규칙에서 나오는
  시스템도 있고, 그런 시스템에서는 의존 로직이 엉망이 된다** (11장, p.301).[^evans2003]
- 처방 (11장, p.301):[^evans2003]

> The first step toward taming the tangle of dependencies is to make these rules explicit by
> introducing a new object.

  - **이것이 [명시적 제약](explicit-constraints.md)과 같은 동작이다** — 암묵적으로 흩어진
    규칙을 이름 가진 객체로 끌어내는 것. 다만 여기서는 그 객체가 남의 카탈로그에서 왔다.
- 규칙의 기제 — 기표 규칙은 자기 "입력" 계정에 새 기표가 들어오면 발동한다. 그러면 자기
  계산 방법(Method)에 근거해 새 기표를 유도하고 그것을 자기 "출력" 계정에 넣는다. 급여
  시스템이라면 급여 계정의 기표가 30퍼센트 추정 소득세를 계산해 원천징수 계정의 기표로
  넣는 규칙을 발동시킬 수 있다 (11장, p.301).[^evans2003]
- **그런데 개념만으로는 따라가기 어렵다고 저자가 적는다.** 의존 설계에서 가장 까다로운 것이
  갱신의 시점과 제어이고, 파울러가 선택지 셋을 논한다 (11장, p.302).[^evans2003]
  - **즉시 발화(Eager firing)** — 가장 뻔하지만 대개 가장 실용적이지 않다. 기표가 계정에
    들어가는 즉시 기표 규칙을 발동시키고 모든 갱신이 곧바로 이루어진다.
  - **계정 기반 발화(Account-based firing)** — 처리를 미룰 수 있다. 어느 시점에 계정에
    메시지가 가면 계정이 자기 기표 규칙을 발동시켜 마지막 발화 이후 들어온 기표를 모두
    처리한다.
  - **기표 규칙 기반 발화(Posting-Rule-based firing)** — 외부 행위자가 시작한다. 그것이
    기표 규칙에게 발화하라고 말하면, 규칙이 마지막 발화 이후 자기 입력 계정에 이루어진
    기표를 전부 찾아내는 책임을 진다.
  - 섞어 쓸 수는 있으나 조건이 붙는다 — **각 규칙 집합마다 시작 지점과 입력 계정 기표를
    식별하는 책임이 하나로 분명히 정의되어야 한다** (11장, p.302).[^evans2003]
- 개발자들은 셋째를 고른다. 즉시 발화는 발생에는 맞지만 낮 동안 들어오는 지급에는 맞지
  않고, 계산 방법을 배치에 그렇게 단단히 묶고 싶지 않다는 것이 이유다 (11장,
  pp.303–304).[^evans2003] 배치가 제어를 쥐면서 배치 설계에 대한 의존을 많이 만들지 않는다는
  것이 얻는 것으로 계상된다.
- **빌려 온 모델 하나가 여기서도 기각된다.** 책의 예제는 계정과 기표 규칙을 직접 연결하지만,
  이 프로젝트는 매번 데이터에서 객체를 만들어야 해서 어느 규칙이 적용되는지를 먼저 알아야
  연결할 수 있었다. 각 계정의 내용을 아는 것은 자산(Asset) 객체였으므로 자산이 규칙을 찾아
  계정을 넘기게 했다 (11장, pp.304–305).[^evans2003]
  - 저자가 이 선택을 **실용적 결정**이라 부르면서 동시에 불편함을 기록한다. 개념적으로는 기표
    규칙을 계정에만 연결하고 자산은 발생을 만드는 자기 일에 집중하게 두는 편이 나았을 것이며,
    이후의 리팩터링과 더 깊은 통찰이 코드의 뻔함을 잃지 않으면서 그 분할을 이루는 길을
    보여 주기를 바란다는 것이다 (11장, p.306).[^evans2003]
  - **불편함을 기록해 두는 것 자체가 이 장의 방법의 일부다.** 같은 종류의 미결 기록이
    [개념의 윤곽](conceptual-contours.md)에서 다음 리팩터링의 표적이 된다.
- 또 하나의 구성물이 이 갈래에서 이름을 얻는다. 기표 서비스(Posting Service)는 회계
  애플리케이션의 API를 노출하는 파사드(FACADE)를 서비스(SERVICE)로 제시한 것이고, 레거시
  시스템에 기표하는 **의도를 드러내는 인터페이스**를 준 것으로 계상된다 (11장,
  p.303).[^evans2003] 그 두 조항은 [도메인 서비스](domain-services.md)와
  [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)에 있다.

## 어휘가 모델 객체만큼 중요하다

- 이 장에서 가장 옮길 값이 큰 판정이 발화 방식 셋에 붙어 있다 (11장, p.302):[^evans2003]

> The addition of the three firing modes to the UBIQUITOUS LANGUAGE is as important to the
> success of the pattern as the model object definitions themselves. It eliminates ambiguity
> and guides decision making directly to a clearly defined set of choices.

- 무엇을 해 주는지도 함께 적힌다 — 이 방식들은 **간과하기 쉬운 도전 하나를 식별하고 명료한
  논의를 뒷받침할 어휘를 제공한다** (11장, p.302).[^evans2003]
  - **분석 패턴에서 옮겨 오는 것이 클래스 다이어그램만이 아니라는 뜻이다.** 선택지에 붙은
    이름이 결정을 가른다. [유비쿼터스 언어](ubiquitous-language.md)가 이 대목의 정본이다.

## 원전에서 떠나도 되는 것과 지켜야 하는 것

- 이 장을 닫는 절의 전제 (11장, p.306):[^evans2003]

> When you are lucky enough to have an analysis pattern, it hardly ever is the answer to your
> particular needs. Yet it offers valuable leads in your investigation, and it provides
> cleanly abstracted vocabulary. It should also give you guidance about implementation
> consequences that will save you pain down the road.

- 그래서 결과가 원전을 닮을 수도, 닮지 않을 수도 있다 — 결과는 흔히 분석 패턴에 기록된 형태를
  닮되 사정에 맞춰 바뀌고, **때로는 결과가 분석 패턴 자체와 뻔히 관계되어 보이지도 않지만
  그 패턴의 통찰이 자극한 것**이다 (11장, p.306).[^evans2003]
- **금지는 단 하나다** (11장, p.306):[^evans2003]

> There is one kind of change you should avoid. When you use a term from a well-known analysis
> pattern, take care to keep the basic concept it designates intact, however much the
> superficial form might change.

- 이유 둘이 붙는다 (11장, pp.306–307).[^evans2003]
  - 첫째, 그 패턴에 문제를 피하게 해 줄 이해가 박혀 있을 수 있다.
  - 둘째이자 더 중요한 것은 **유비쿼터스 언어가 널리 이해되거나 적어도 잘 설명된 낱말을
    포함할 때 강화된다**는 것이다.
- 그리고 대칭되는 의무 — **모델의 자연스러운 진화로 모델 정의가 바뀐다면 이름도 바꾸는 수고를
  하라** (11장, p.307).[^evans2003]
  - **이 조항이 이 페이지에서 가장 실행하기 쉬운 것이자 가장 자주 깨지는 것이다.** 빌린
    이름을 남겨 둔 채 뜻만 바꾸면 어휘가 거짓 신호를 낸다.

## 코드 재사용과 완전히 다르다

- 공개된 객체 모델은 많지만 **선택의 배후 추론과 그로부터 따라오는 결과를 붙잡은 것은
  소수**이고, 그 둘이 분석 패턴에서 가장 쓸모 있는 부분이라는 진단이 이어진다 (11장,
  p.307).[^evans2003] 포괄적 카탈로그가 나오리라고는 기대하지 않으며 산업별 카탈로그가
  나올 수는 있다는 전망도 함께 적힌다.
- **그리고 이 장의 마지막 판정이 경계를 긋는다** (11장, p.307):[^evans2003]

> This kind of reapplication of organized knowledge is completely different from attempts to
> reuse code through frameworks or components, except that either could provide the seed of
> an idea that is not obvious. A model, even a generalized framework, is a complete working
> whole, while an analysis is a kit of model fragments.

- 값의 소재도 못 박힌다 — 분석 패턴은 **가장 결정적이고 어려운 결정에 초점을 맞추고 대안과
  선택지를 밝히며, 스스로 발견해야 한다면 비쌀 하류의 결과를 미리 내다본다** (11장,
  p.307).[^evans2003]
  - **"완결된 작동하는 전체"와 "모델 조각 꾸러미"의 대비가 이 페이지의 요약이다.** 프레임워크는
    받아 쓰는 것이고 분석 패턴은 재료로 쓰는 것이다. 프레임워크를 얼마나 쓸 것인가는 다른
    물음이고 [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md)에 있다.

## 증류에서 이 선택지가 서는 자리

같은 원전의 15장이 이 활동을 네 선택지 중 하나로 정식 편입한다. 이 페이지가 "무엇을 지키며
빌리는가"를 다룬다면 거기서는 "언제 빌리는 쪽을 고르는가"를 다룬다.

- 자리 — **일반 하위 도메인**을 채우는 둘째 선택지가 **공표된 설계나 모델**이고, 저자는 그것이
  **Fowler 1996의 분석 패턴처럼 널리 배포된 모델이 있을 때 가장 잘 통한다**고 적으면서 이
  페이지의 장을 가리킨다 (15장, p.408).[^evans2003]
- 그 선택지의 이점과 대가가 간명하게 계상된다 (15장, p.408):[^evans2003]
  - 이점 — **자체 개발 모델보다 성숙하고 여러 사람의 통찰을 반영한다. 즉시 쓸 수 있는 고품질
    문서가 딸린다.**
  - 대가 — **필요에 꼭 맞지 않거나 필요에 비해 과잉 설계일 수 있다.**
- **적용 범위가 핵심이 아닌 쪽으로 한정된다는 것이 이 편입의 요점이다.** 15장은 이 빌림을
  **프로젝트의 동기가 아닌 하위 도메인**을 채우는 수단으로 놓는다. 반대로 핵심 도메인에 대해서는
  같은 장이 **핵심 도메인을 구매할 수 있을 것 같지 않다**고 적는다 (15장, p.403).[^evans2003]
  - 위 [원전에서 떠나도 되는 것과 지켜야 하는 것](#원전에서-떠나도-되는-것과-지켜야-하는-것)이
    빌린 모델을 고치는 자유를 다뤘다면, 이 배치는 **어디서 빌려도 되는가**에 선을 긋는다.
    #hypothesis 11장 자체는 이 제한을 걸지 않는다 — 11장의 회계 모델은 그 프로젝트의 핵심에
    가까운 자리에 들어갔다. 두 장이 서로를 논하지 않으므로 이것은 두 서술을 나란히 놓은 해석이다.
- 그리고 15장이 위 [코드 재사용과 완전히 다르다](#코드-재사용과-완전히-다르다)를 한 번 더
  못 박는다 — **재사용은 일어나지만 언제나 코드 재사용은 아니다. 공표된 설계나 모델을 쓸 때처럼
  모델 재사용이 흔히 더 나은 수준의 재사용이다** (15장, p.413).[^evans2003]

## 같은 책에서 온, 도메인이 아니라 모델을 구조화하는 패턴

16장의 [지식 수준](knowledge-level.md)이 **이 페이지가 다루는 바로 그 책에서 빌려 온 것**이다.
그런데 저자는 그것을 분석 패턴으로 다루지 않고 대규모 구조 장에 싣는다.

- 출처 — **『분석 패턴』(Fowler 1996, pp.24–27)에서 이 패턴은 조직 안의 책무(accountability)를
  모델링하는 논의에서 나오고 나중에 회계의 기표 규칙에 적용된다** (16장, p.465).[^evans2003]
  - 뒤의 것이 위 [둘째 대화 — 기표 규칙과 발화 방식 셋](#둘째-대화--기표-규칙과-발화-방식-셋)이
    빌려 온 바로 그 규칙이다.
- 왜 자기 장을 갖지 못했는가 (16장, p.465):[^evans2003]

> Although the pattern appears in several chapters, it doesn't have a chapter of its own because
> it is different from most patterns in the book. Rather than modeling a domain, as the other
> analysis patterns do, KNOWLEDGE LEVEL structures a model.

  - **이것이 위 [분석 패턴이란 무엇인가](#분석-패턴이란-무엇인가)의 정의에 걸리는 예외다.**
    분석 패턴은 도메인의 개념을 담은 모델 조각인데, 이것은 모델을 담는 틀이다. 그래서 빌려 오는
    방식도 다르다 — 개념을 물려받는 것이 아니라 **모델을 가르는 선을 물려받는다.**
- 저자 자신이 이 패턴을 쓸 때도 위 [원전에서 떠나도 되는 것과 지켜야 하는 것](#원전에서-떠나도-되는-것과-지켜야-하는-것)의
  태도를 유지한다. 파울러의 정의를 그대로 인용해 절을 열고, 반사(REFLECTION) 패턴과의 용어
  대응표(Knowledge Level ↔ Meta Level, Operations Level ↔ Base Level)를 따로 실어 어느 말이
  누구의 것인지 표시한다 (16장, pp.465·470).[^evans2003]

## 이어지는 페이지

- [암묵적 개념 파내기](digging-out-implicit-concepts.md) — 9장이 "책을 읽어라"로 이 장을
  예고하는 자리이고, 같은 이자 예제의 앞선 갈래
- [확립된 형식 체계](established-formalisms.md) — 같은 처방의 형제. 그쪽은 수백 년 다듬어진
  형식 체계를, 이쪽은 출판된 모델 조각을 빌린다
- [설계 패턴을 도메인 패턴으로 읽기](design-patterns-as-domain-patterns.md) — 빌려 쓸 것이
  기술적 설계 패턴일 때의 판별 기준
- [모델 리팩터링의 과정](model-refactoring-process.md) — 이 빌려 쓰기가 "선행 지식"이라는
  이름으로 과정의 한 재료가 되는 자리
- [모델 주도 설계](model-driven-design.md) — 분석과 설계의 균열이 이 조항의 반대말인 이유
- [유비쿼터스 언어](ubiquitous-language.md) — 빌려 온 낱말이 들어가는 곳
- [명시적 제약](explicit-constraints.md) — 규칙을 객체로 끌어내는 같은 동작
- [지식 수준](knowledge-level.md) — 같은 책에서 빌려 온, 모델을 구조화하는 쪽의 패턴
- [지식 정련](knowledge-crunching.md) — 빌린 것이 흘러 들어가는 활동
- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 같은 회계 관행을
  데이터 시스템 축에서 다루는 자리
- [관계형 데이터베이스를 위한 객체 설계](designing-objects-for-relational-databases.md) —
  이 장의 타협이 속하는 종류
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 16장 "Large-Scale Structure" §KNOWLEDGE LEVEL(pp.465·470) ·
    11장 "Applying Analysis Patterns" 전량(pp.293–307 — 장 도입
    pp.293–295 · 예제 "Earning Interest with Accounts"(pp.295–300, 그 안의 빌려 온 요약
    "Accounting Models in Analysis Patterns" pp.295–296 포함) · 예제 계속 "Insight into the
    Nightly Batch"(pp.301–306, 빌려 온 요약 "Posting Rules" p.301과 "Executing Posting
    Rules" p.302 포함) · §"Analysis Patterns Are Knowledge to Draw On" pp.306–307).
    p.308은 백지다. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은
    대문자로 조판하는 관례를 직인용에서 유지했다. 도판 전부(Figure 11.1–11.11 — 초기 클래스
    다이어그램, 기본 회계 모델과 거래 모델 다이어그램 둘, 새 모델 제안과 그 수정 셋, 구현
    이후의 클래스 다이어그램, 기표 규칙 기본 다이어그램, 배치에 기표 규칙을 쓴 스케치,
    최종 클래스 다이어그램, 규칙 발화 시퀀스 다이어그램)는 이미지라 딸린 판정 산문만 옮겼다.
    **이 장에는 산문 코드 목록이 하나도 없다** — 예제가 전부 UML 도해와 대화라 이 페이지에
    코드 펜스가 없다. 파울러 인용문 안의 대괄호와 쪽 표기는 원문 그대로다. 저자가 대는
    참고 문헌은 Fowler 1997의 6장 "Inventory and Accounting"이다. 마지막 절은 15장
    "Distillation" §GENERIC SUBDOMAINS의 "Option 2: A Published Design or Model"(p.408)과
    곁글 "Generic Doesn't Mean Reusable"(pp.412–413)에서 왔다.

---
type: concept
title: 점진적 타이핑
description: 파이썬의 타입 힌트가 어떤 종류의 타입 체계인가와 그 체계가 스스로 그은 한계 — 점진적 타입 체계의 세 성질(선택적·런타임 강제 없음·성능 이득 없음)과 100퍼센트 적용을 좇지 말라는 경고, 타입을 지원되는 연산의 집합으로 보는 규정, 덕 타이핑과 명목 타이핑의 대비와 각각이 놓치는 것, 와일드카드 타입 Any와 subtype-of가 아닌 consistent-with라는 관계, 그리고 정적 타이핑이 소프트웨어 품질의 중심 기둥이 될 수 없다는 판정과 그 근거 목록
generated: { by: "claude-opus-5", at: "2026-08-18T12:00:00Z" }
stale_after: "2027-08-01"
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 점진적 타이핑

- [버전 조건과 재심 트리거](#버전-조건과-재심-트리거)
- [점진적 타입 체계의 세 성질](#점진적-타입-체계의-세-성질)
- [타입은 지원되는 연산으로 정의된다](#타입은-지원되는-연산으로-정의된다)
- [덕 타이핑과 명목 타이핑](#덕-타이핑과-명목-타이핑)
- [Any와 consistent-with](#any와-consistent-with)
- [불완전한 타이핑과 강한 테스트](#불완전한-타이핑과-강한-테스트)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파이썬의 타입 힌트는 어떤 종류의 타입 체계이고, 그 체계가 스스로 그은 한계는
어디인가.**

**이 페이지는 얇다.** 이 장의 60퍼센트는 애노테이션에 쓸 수 있는 타입들의 카탈로그이고, 그것은
파이썬 판마다 바뀌는 지형이라 이 KB에 옮기지 않았다(무엇을 왜 뺐는지는
`it/archive/ramalho2022/_progress.yaml`의 `skipped`가 정본이다). 여기 남긴 것은 **판이 바뀌어도
남는 개념**뿐이다. 네 가지 타이핑 접근의 지도와 `typing.Protocol`의 설계 지침은
[인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)가 갖는다.

## 버전 조건과 재심 트리거

> **버전 조건**: 이 장의 서술은 **파이썬 3.9·Mypy 0.910, 2021년 7월 시점**의 실측이다. 저자가
> 그 시점을 본문에 여러 번 명시한다 — 재귀 타입 미지원, 애노테이션을 이용한 바이트코드 최적화
> 부재, `Union`을 `@singledispatch`에 넘길 때의 오류가 전부 그 시점의 관측이다. **이 문단이
> 다루는 도구 지형은 그 뒤로 바뀌었을 수 있다.**
>
> **재심 트리거**: ⑴ 파이썬이 타입 체계에 새 구성물을 더할 때(PEP 484 계열의 후속),
> ⑵ 이 페이지가 인용한 "아직 안 되는 것" 중 하나가 되기 시작할 때. 개념 쪽 — 점진적 타이핑의
> 정의, 덕/명목 대비, `consistent-with` — 은 그 트리거의 대상이 아니다.

## 점진적 타입 체계의 세 성질

- 계보부터 — **PEP 484가 파이썬에 점진적 타입 체계(gradual type system)를 도입했다. 점진적
  타입 체계를 가진 다른 언어로는 마이크로소프트의 타입스크립트, Dart(구글이 만든 플러터 SDK의
  언어), Hack(페이스북의 HHVM 가상 머신이 지원하는 PHP 방언)이 있다** (8장 §"About Gradual
  Typing", p.254).[^ramalho2022]
- 성질 셋 (8장 §"About Gradual Typing", pp.254–255):[^ramalho2022]
  - **선택적이다** — **기본적으로 타입 검사기는 타입 힌트가 없는 코드에 경고를 내지 않아야
    한다. 대신 객체의 타입을 판정할 수 없을 때 `Any` 타입을 가정한다. `Any` 타입은 다른 모든
    타입과 호환되는 것으로 간주된다.**
  - **런타임에 타입 오류를 잡지 않는다** — **타입 힌트는 정적 타입 검사기·린터·IDE가 경고를
    올리는 데 쓰인다. 그것들은 일관되지 않은 값이 런타임에 함수로 넘어가거나 변수에 대입되는
    것을 막지 않는다.**
  - **성능을 높이지 않는다** — **타입 애노테이션은 이론상 생성된 바이트코드의 최적화를 허용할
    수 있는 데이터를 제공하지만, 2021년 7월 현재 내가 아는 어떤 파이썬 런타임에도 그런 최적화는
    구현돼 있지 않다.**
- **가장 좋은 사용성 기능이 선택성이라는 것이 저자의 정리다** — **점진적 타이핑의 가장 좋은
  사용성 기능은 애노테이션이 언제나 선택적이라는 것이다** (8장 §"About Gradual Typing",
  p.255).[^ramalho2022]
- 그리고 그 선택성이 실제로 필요해지는 상황이 인정된다 — **정적 타입 체계에서 대부분의 타입
  제약은 표현하기 쉽지만 다수는 성가시고, 일부는 어렵고, 몇몇은 불가능하다. 좋은 테스트
  커버리지와 통과하는 테스트를 갖춘 훌륭한 파이썬 코드를 썼는데도 타입 검사기를 만족시키는
  타입 힌트를 붙이지 못할 수 있다. 그래도 괜찮다; 문제되는 타입 힌트는 그냥 빼고 출시하라!**
  (8장 §"About Gradual Typing", p.255)[^ramalho2022]
- **정량 목표에 대한 경고가 이 절의 조문이다** (8장 §"About Gradual Typing",
  p.255):[^ramalho2022]

  > Seeking 100% coverage of type hints is likely to stimulate type hinting without proper
  > thought, only to satisfy the metric. It will also prevent teams from making the most of
  > the power and flexibility of Python.

- 대상 독자를 가르는 서술도 장 첫머리에 있다 — **주된 수혜자는 IDE와 CI를 쓰는 전문
  소프트웨어 엔지니어다. 타입 힌트를 그 집단에 매력적으로 만드는 비용-편익 계산이 파이썬의 모든
  사용자에게 적용되지는 않는다** (8장 도입, p.253).[^ramalho2022] 과학자·트레이더·기자·예술가·
  학생에게는 **배우는 비용이 더 높고 편익은 더 낮을 것**이며, **파이썬의 기본 동적 타이핑이
  데이터와 발상을 탐색하는 코드를 쓸 때 더 단순하고 표현력 있다**는 것이 이유다
  (8장 도입, pp.253–254).[^ramalho2022]

## 타입은 지원되는 연산으로 정의된다

- 출발점이 PEP 483의 정의다 (8장 §"Types Are Defined by Supported Operations",
  p.260):[^ramalho2022]

  > Here we assume that type is a set of values and a set of functions that one can apply to
  > these values.

- 저자가 그것을 실무 쪽으로 좁힌다 — **실무에서는 지원되는 연산의 집합을 타입의 규정적 특징으로
  여기는 것이 더 유용하다** (8장 §"Types Are Defined by Supported Operations",
  p.261).[^ramalho2022]
- 그 관점이 낳는 실물이 `def double(x): return x * 2`다. 애노테이션이 없으면 수·문자열·튜플·
  리스트·배열·N차원 배열, 그리고 **`int` 인자를 받는 `__mul__`을 구현하거나 물려받은 다른 어떤
  타입**도 유효하다. 그런데 `x: abc.Sequence`라고 적으면 타입 검사기가 `x * 2`를 오류로
  표시한다 — **`Sequence` ABC가 `__mul__`을 구현하거나 물려받지 않기 때문이다.** 런타임에는
  구체 시퀀스들과 수에 대해 잘 동작하는데도 그렇다 (8장 §"Types Are Defined by Supported
  Operations", p.261).[^ramalho2022]
- 일반화 — **더 일반적인 타입일수록 인터페이스가 좁다. 즉 지원하는 연산이 적다. `object`
  클래스는 `abc.Sequence`보다 적은 연산을 구현하고, 그쪽은 `abc.MutableSequence`보다,
  그쪽은 `list`보다 적다** (8장 §"The Any Type", p.267).[^ramalho2022]

## 덕 타이핑과 명목 타이핑

- **점진적 타입 체계에는 타입에 대한 두 가지 서로 다른 관점의 상호작용이 있다**
  (8장 §"Types Are Defined by Supported Operations", p.261).[^ramalho2022]
  - **덕 타이핑(duck typing)** — **스몰토크가 채택하고 파이썬·자바스크립트·루비도 채택한
    관점이다. 객체는 타입을 갖지만 변수(매개변수 포함)는 타입이 없다. 실무에서는 객체의 선언된
    타입이 무엇이냐가 아니라 그것이 실제로 어떤 연산을 지원하느냐만 중요하다. 내가
    `birdie.quack()`을 부를 수 있으면 그 맥락에서 `birdie`는 오리다. 정의상 덕 타이핑은
    객체에 대한 연산이 시도되는 런타임에만 강제된다. 이것은 명목 타이핑보다 유연하지만 런타임에
    더 많은 오류를 허용하는 대가를 치른다** (8장 §"Types Are Defined by Supported Operations",
    pp.261–262).[^ramalho2022]
  - **명목 타이핑(nominal typing)** — **C++·자바·C#이 채택하고 애노테이션이 붙은 파이썬이
    지원하는 관점이다. 객체와 변수가 타입을 갖는다. 그러나 객체는 런타임에만 존재하고, 타입
    검사기는 변수(매개변수 포함)가 타입 힌트로 애노테이션된 소스 코드만 신경 쓴다. `Duck`이
    `Bird`의 하위 클래스면 `Duck` 인스턴스를 `birdie: Bird`로 애노테이션된 매개변수에 대입할
    수 있다. 그러나 함수의 몸 안에서 타입 검사기는 `birdie.quack()` 호출을 불법으로 여긴다.
    `birdie`가 이름상 `Bird`이고 그 클래스는 `.quack()` 메서드를 제공하지 않기 때문이다.
    런타임의 실제 인자가 `Duck`인지는 중요하지 않다. 명목 타이핑은 정적으로 강제되기 때문이다**
    (8장 §"Types Are Defined by Supported Operations", p.262).[^ramalho2022]
  - 덕 타이핑의 자리도 각주로 정확히 지정된다 — **덕 타이핑은 구조적 타이핑(structural
    typing)의 암묵적 형태이고, 파이썬 3.8 이상은 `typing.Protocol`의 도입으로 그것도
    지원한다** (8장 §"Types Are Defined by Supported Operations", p.262
    각주 5).[^ramalho2022]

- 아래가 그 대비를 만드는 최소 실물이자 이 페이지의 대표 코드다. Mypy는 `alert_bird`의 몸을
  오류로 표시하지만(`"Bird" has no attribute "quack"`), `Duck` 인스턴스를 넘기면 런타임에는
  잘 돈다 (8장 §"Types Are Defined by Supported Operations" 예제 8-4,
  pp.262–263).[^ramalho2022]

  ```python
  class Bird:
      pass

  class Duck(Bird):
      def quack(self):
          print('Quack!')

  def alert(birdie):
      birdie.quack()

  def alert_duck(birdie: Duck) -> None:
      birdie.quack()

  def alert_bird(birdie: Bird) -> None:
      birdie.quack()
  ```

- 이 실험이 남기는 판정 (8장 §"Types Are Defined by Supported Operations",
  p.263):[^ramalho2022]

  > This little experiment shows that duck typing is easier to get started and is more
  > flexible, but allows unsupported operations to cause errors at runtime. Nominal typing
  > detects errors before runtime, but sometimes can reject code that actually runs.

  - 그런데 저자는 그 "거부된 코드"의 편을 들지 않는다 — **때때로 동작한다 하더라도 `alert_bird`
    함수는 이름이 잘못됐다: 그 몸은 `.quack()` 메서드를 지원하는 객체를 실제로 요구하는데
    `Bird`에는 그것이 없다** (8장 §"Types Are Defined by Supported Operations",
    p.263).[^ramalho2022] **타입 검사기가 잡은 것이 타입 오류가 아니라 이름의 거짓말이었다는
    읽기다.**
- 편익의 크기가 코드베이스 크기에 비례한다는 단서도 붙는다 — **책에 들어가는 작은 예제에서
  타입 힌트의 가치는 의문스럽다. 편익은 코드베이스의 크기와 함께 자란다. 그래서 드롭박스·
  구글·페이스북처럼 수백만 줄의 파이썬 코드를 가진 회사들이 팀과 도구에 투자했다**
  (8장 §"Types Are Defined by Supported Operations", p.264).[^ramalho2022]

## Any와 consistent-with

- **`Any` 타입은 어떤 점진적 타입 체계에서든 요석(keystone)이고, 동적 타입(dynamic type)이라고도
  불린다** (8장 §"The Any Type", p.266).[^ramalho2022] 애노테이션이 없는 함수를 타입 검사기는
  인자와 반환이 `Any`인 것으로 가정한다.
- `object`와의 대비가 그 성질을 드러낸다 — `def double(x: object)`도 모든 타입의 인자를 받지만
  **`object`가 `__mul__` 연산을 지원하지 않으므로** 몸의 `x * 2`가 거부된다
  (8장 §"The Any Type", p.267).[^ramalho2022]
- 그래서 `Any`의 자리가 규정된다 — **`Any`는 타입 계층의 꼭대기와 바닥에 동시에 앉는 마법의
  타입이다. 가장 일반적인 타입이면서 — 그래서 `n: Any` 인자가 모든 타입의 값을 받는다 —
  동시에 가장 특수화된 타입이라 가능한 모든 연산을 지원한다** (8장 §"The Any Type",
  p.267).[^ramalho2022]
- **대가도 같은 자리에 적힌다** — **물론 어떤 타입도 가능한 모든 연산을 지원할 수는 없으므로,
  `Any`를 쓰면 타입 검사기가 자기 핵심 임무를 다하지 못하게 된다: 프로그램이 런타임 예외로
  깨지기 전에 잠재적으로 불법인 연산을 검출하는 것** (8장 §"The Any Type",
  p.267).[^ramalho2022]
- 그래서 점진적 체계에는 하위 타입 관계와 다른 관계가 하나 더 있다. **전통적 객체 지향 명목
  타입 체계는 is *subtype-of* 관계에 기댄다**는 전제 위에서 (8장 곁글 "Subtype-of versus
  consistent-with", pp.267–268):[^ramalho2022]
  - Liskov의 규정이 인용된다 — **Barbara Liskov는 실제로 is *subtype-of*를 지원되는 연산으로
    정의했다: 타입 `T2`의 객체가 타입 `T1`의 객체를 대체해도 프로그램이 여전히 올바로 동작하면
    `T2`는 `T1`의 *subtype-of*다.** 그 초점 때문에 LSP를 **행동적 하위 타이핑(behavioral
    subtyping)**이라고도 부른다.
  - 그리고 **점진적 타입 체계에는 다른 관계가 있다: *consistent-with*이고, *subtype-of*가
    적용되는 어디에나 적용되며 `Any` 타입에 대한 특별 규정을 둔다.** 규칙은 셋이다.
    1. **`T1`과 그 하위 타입 `T2`가 주어지면 `T2`는 `T1`과 *consistent-with*다(리스코프 치환).**
    2. **모든 타입은 `Any`와 *consistent-with*다: `Any` 타입으로 선언된 인자에 모든 타입의
       객체를 넘길 수 있다.**
    3. **`Any`는 모든 타입과 *consistent-with*다: 다른 타입의 인자가 기대되는 자리에 언제나
       `Any` 타입의 객체를 넘길 수 있다.**
  - 필요성의 진술 — **모든 점진적 타입 체계는 `Any` 같은 와일드카드 타입을 필요로 한다**
    (8장 곁글, p.269).[^ramalho2022]

## 불완전한 타이핑과 강한 테스트

- 편익은 인정된다 — **큰 기업 코드베이스의 관리자들은 많은 버그가 정적 타입 검사기에 잡히고,
  코드가 프로덕션에서 돌기 시작한 뒤에 발견되는 것보다 더 싸게 고쳐진다고 보고한다**
  (8장 §"Imperfect Typing and Strong Testing", p.296).[^ramalho2022]
  - **그러나 순서가 함께 기록된다** — **내가 아는 회사들에서 자동화된 테스트는 정적 타이핑이
    도입되기 훨씬 전부터 표준 관행이었고 널리 채택돼 있었다는 점을 짚어 두는 것이 필수적이다**
    (8장 §"Imperfect Typing and Strong Testing", p.296).[^ramalho2022]
- 오류의 두 방향 (8장 §"Imperfect Typing and Strong Testing", p.296):[^ramalho2022]
  - **거짓 양성(false positives)** — **도구가 올바른 코드에 타입 오류를 보고한다.**
  - **거짓 음성(false negatives)** — **도구가 잘못된 코드에 타입 오류를 보고하지 않는다.**
- 전부 검사하려 들면 잃는 것들 (8장 §"Imperfect Typing and Strong Testing",
  p.296):[^ramalho2022]
  - **`config(**settings)` 같은 인자 언패킹처럼 정적으로 검사할 수 없는 편리한 기능들.**
  - **프로퍼티·기술자·메타클래스, 일반적으로 메타프로그래밍 같은 고급 기능은 타입 검사기에서
    지원이 나쁘거나 이해 범위 밖이다.**
  - **타입 검사기는 파이썬 릴리스보다 뒤처져서, 새 언어 기능이 든 코드를 분석하다가 거부하거나
    심지어 죽는다 — 어떤 경우에는 1년 넘게.**
- **표현할 수 없는 것의 목록이 가장 실무적이다** — **흔한 데이터 제약은 타입 체계에서 표현할 수
  없다 — 단순한 것조차. 예를 들어 타입 힌트는 "수량은 0보다 큰 정수여야 한다"거나 "레이블은
  6~12개 ASCII 문자로 된 문자열이어야 한다"를 보장할 수 없다. 일반적으로 타입 힌트는 업무
  로직의 오류를 잡는 데 도움이 되지 않는다** (8장 §"Imperfect Typing and Strong Testing",
  p.296).[^ramalho2022]
- **판정** (8장 §"Imperfect Typing and Strong Testing", p.296):[^ramalho2022]

  > Given those caveats, type hints cannot be the mainstay of software quality, and making
  > them mandatory without exception would amplify the downsides.

  - 자리매김도 함께 준다 — **정적 타입 검사기를 테스트 러너·린터 등과 함께 2022년 저술 시점의 CI 파이프라인의
    도구 중 하나로 여기라. CI 파이프라인의 요점은 소프트웨어 실패를 줄이는 것이고, 자동화된
    테스트는 타입 힌트가 닿지 못하는 많은 버그를 잡는다. 파이썬으로 쓸 수 있는 어떤 코드든
    파이썬으로 테스트할 수 있다 — 타입 힌트가 있든 없든** (8장 §"Imperfect Typing and Strong
    Testing", p.296).[^ramalho2022]
- 장의 마지막 말이 Guido의 것이다 (8장 §"Chapter Summary", p.298):[^ramalho2022]

  > I wouldn't like a version of Python where I was morally obligated to add type hints all
  > the time. I really do think that type hints have their place but there are also plenty
  > of times that it's not worth it, and it's so wonderful that you can choose to use them.

- 적용 기준으로 인용되는 문장도 하나 있다. Bernát Gábor의 것이다 — **단위 테스트를 쓸 가치가
  있을 때면 언제나 타입 힌트를 써야 한다** (8장 §"Further Reading", p.298).[^ramalho2022]
  - 저자는 그것에도 유보를 단다 — **나는 테스트의 열렬한 팬이지만 탐색적 코딩도 많이 한다.
    탐색할 때 테스트와 타입 힌트는 도움이 되지 않는다. 그것들은 짐이다** (8장 §"Further
    Reading", p.298).[^ramalho2022]

## 이어지는 페이지

- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 네 가지 타이핑 접근의 지도와
  `typing.Protocol`의 설계 지침이 있는 정본. 이 페이지가 말한 덕/명목 대비가 거기서 네
  사분면으로 펼쳐진다
- [데이터 클래스 빌더](../concepts/data-class-builders.md) — 타입 힌트가 런타임에 아무 효과가 없으면서도
  클래스 생성에는 쓰이는 자리
- [파이썬의 일급 함수](../concepts/first-class-functions-in-python.md) — 이 장이 애노테이션하려는 대상
- [자가 테스트 코드](self-testing-code.md) — "타입 힌트가 아니라 테스트"라는 판정이 기대는 쪽
- [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 8장 "Type Hints in Functions"(pp.253–302) — 도입(pp.253–254) ·
    §"About Gradual Typing"(pp.254–255) · §"Types Are Defined by Supported
    Operations"(pp.260–265) · §"The Any Type"(pp.266–267) · 곁글 "Subtype-of versus
    consistent-with"(pp.267–269) · §"Imperfect Typing and Strong Testing"(pp.296–297) ·
    §"Chapter Summary"(pp.297–298) · §"Further Reading"(p.298). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 30). 예제 8-4는 원문 그대로이며 조판용 번호 표지만 제거했다.
    **이 장의 절반 이상(§"Types Usable in Annotations" pp.266–295)은 애노테이션에 쓸 수 있는
    타입들의 카탈로그라 옮기지 않았다** — 사유는 `_progress.yaml`의 `skipped`에 있다.
    PDF 317쪽은 추출본이 훼손 판정을 받아 그 쪽의 서술은 인용하지 않았다.

---
type: concept
title: 테스트 대역 선호 순서와 규모 전제
description: 실물을 먼저 쓰고 안 되면 가짜를 쓰며 스텁과 상호작용 검증을 뒤로 미룬다는 한 대규모 조직의 선호 순서와 그 각각의 조건, 가짜의 값어치를 사용자 수의 함수로 적은 문면, 한 API가 수만 번 목으로 대체될 때 생기는 문제와 그것을 막는 정적 분석 주석, 대역이 실물과 어긋날 때 큰 테스트가 받는 자리, 그리고 이 논거 전체가 기대는 규모 전제와 그것을 뗐을 때 남는 것
generated: { by: "claude-opus-5", at: "2026-08-24T06:00:00Z" }
status: draft
sources:
  - { id: winters2020-swe-at-google, resource: /it/sources/winters2020-swe-at-google.md }
---

# 테스트 대역 선호 순서와 규모 전제

- [이 소스의 지위와 규모 전제](#이-소스의-지위와-규모-전제)
- [선호 순서 — 실물이 먼저다](#선호-순서--실물이-먼저다)
- [실물을 언제 쓸 수 있나](#실물을-언제-쓸-수-있나)
- [가짜가 값어치를 갖는 조건](#가짜가-값어치를-갖는-조건)
- [스텁이 무엇을 잃는가](#스텁이-무엇을-잃는가)
- [상호작용 검증은 언제만 쓰나](#상호작용-검증은-언제만-쓰나)
- [목이 수만 번 불릴 때 — @DoNotMock](#목이-수만-번-불릴-때--donotmock)
- [대역이 충실하지 않을 때](#대역이-충실하지-않을-때)
- [규모를 떼면 무엇이 남는가](#규모를-떼면-무엇이-남는가)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트에서 의존을 무엇으로 대신할 것인가에 대해 한 대규모 조직이 세운 선호
순서는 무엇이며, 그 순서는 어떤 조건 위에 서 있는가.**

## 이 소스의 지위와 규모 전제

- **근거 등급은 `industry-norm`이다.** 13장에 통제도 표본도 수치도 없다. 근거로 드는 것이
  사내 경험이고, 이 KB는 이 장을 "학술 근거"로 쓰지 않는다.
- **책이 자기 결론의 유래를 경험으로 적는다** (13장 §"Test Doubles at
  Google"):[^winters2020-swe-at-google]

  > It wasn't until several years and countless tests later that we began to realize the
  > cost of such tests: though these tests were easy to write, we suffered greatly given
  > that they required constant effort to maintain while rarely finding bugs. The pendulum
  > at Google has now begun swinging in the other direction, with many engineers avoiding
  > mocking frameworks in favor of writing more realistic tests.

  **추가 문장 하나가 이 장의 지위를 더 낮춘다** — 같은 절이 이 실무의 실제 적용은
  `varies widely from team to team`이라고 적는다. **회사 전체의 관행이 아니라 권고다.**
- **이 장의 논거가 기대는 조건 넷**은 아래 절들에 흩어져 있고 한자리에 모으면 이렇다 —
  한 API가 **수만 번** 목(mock)으로 대체된다는 규모, 실물의 **소유팀이 가짜를 만들어
  유지**한다는 분업, 정적 분석 도구가 그것을 **집행**한다는 배선, 그리고 테스트를 여러 서버에 흩어
  돌리는 인프라다. **넷 중 하나라도 없으면 이 장의 처방이 그대로 옮겨지지 않는다.**
- **언어 모델 시대의 재검이 없다.** 2020년 문면이고, 생성된 테스트가 대역을 어떻게 쓰는지를
  이 장은 다루지 않는다.

## 선호 순서 — 실물이 먼저다

**13장 끝의 요약 넷이 이 장의 조문이다** (13장 §"TL;DRs"):[^winters2020-swe-at-google]

> A real implementation should be preferred over a test double.
>
> A fake is often the ideal solution if a real implementation can't be used in a test.
>
> Overuse of stubbing leads to tests that are unclear and brittle.
>
> Interaction testing should be avoided when possible: it leads to tests that are brittle
> because it exposes implementation details of the system under test.

- **본문에서도 같은 순서가 선언된다** (13장 §"Real Implementations"):[^winters2020-swe-at-google]

  > our first choice for tests is to use the real implementations of the system under
  > test's dependencies; that is, the same implementations that are used in production
  > code.

- **11장이 같은 말을 범위 절에서 한 번 더 한다** (11장 §"Test Scope"):[^winters2020-swe-at-google]

  > at Google, we prefer to keep the real dependencies in place when it is feasible to do
  > so.

- **어휘가 먼저 정리된다** (13장 §"Techniques for Using Test Doubles").[^winters2020-swe-at-google]
  대역(test double)을 쓰는 기법이 셋이다 — **가짜**(fake, 실물과 비슷하게 동작하지만
  프로덕션에는 못 쓰는 가벼운 구현), **스터빙**(stubbing, 스스로는 행동이 없는 함수에
  반환값을 박아 넣는 것), **상호작용 검증**(interaction testing, 구현을 부르지 않고 어떻게
  불렸는지를 확인하는 것).
  - **책이 "모킹"이라는 말을 피한다** (13장 도입부·§"Interaction Testing"). 그 낱말이
    목킹 프레임워크와 상호작용 검증 둘 다를 가리켜 섞이기 때문이다.
- **학파 이름도 붙는다** (13장 §"Real Implementations"):[^winters2020-swe-at-google]

  > Preferring real implementations in tests is known as *classical testing*. There is also
  > a style of testing known as *mockist testing*, in which the preference is to use
  > mocking frameworks instead of real implementations. Even though some people in the
  > software industry practice mockist testing (including the creators of the first mocking
  > frameworks), at Google, we have found that this style of testing is difficult to scale.
  > It requires engineers to follow strict guidelines when designing the system under test

  **"틀렸다"가 아니라 "규모에서 어렵다"는 것이 이 문장의 주장이다.** 그리고 그 이유로 드는
  것이 설계 규율의 준수인데, 구글 엔지니어 다수의 기본 습관이 고전 학파 쪽에 맞는 코드를
  쓰는 것이었다고 같은 자리에 적는다 — **조직 습관에 기댄 근거다.**

## 실물을 언제 쓸 수 있나

**세 잣대를 든다** (13장 §"How to Decide When to Use a Real
Implementation").[^winters2020-swe-at-google] 실물은 **빠르고 결정적이며 의존이 단순할
때** 선호된다. 값 객체(금액·날짜·주소·컬렉션)가 그 예다.

- **실행 시간** — 얼마가 너무 느린지에 답이 없다고 책이 먼저 적는다
  (`There is no exact answer here`). 대신 절차를 준다: 애매하면 **너무 느려질 때까지 실물을
  쓰다가** 그 지점에서 대역으로 바꾼다. 테스트 500건이면 케이스당 1초가 감당되지 않지만
  5건이면 감당된다는 예를 든다.
  - **여기에 인프라 전제가 붙는다** (같은 절) — 테스트를 여러 서버에 나눠 돌리는 것이
    `trivial`하다고 적는다. CPU 시간을 사서 개발자 시간을 아끼는 교환이다.
- **결정성** — 실물이 드물게 불안정(flaky)을 일으키면 대응하지 않아도 되지만 자주
  일어나면 대역으로 바꿀 때라고 적는다. 비결정성의 흔한 원인으로 **밀폐되지
  않은(nonhermetic) 코드**(외부 서비스 의존)와 시스템 시계를 든다.
- **의존 구성** — 실물을 쓰려면 의존 나무 전체를 만들어야 한다. 목킹 프레임워크로는 한 줄이
  된다는 유혹을 인정하면서도, 이상적인 해법은 **프로덕션과 같은 객체 생성 코드**(팩터리
  메서드나 자동 의존성 주입)를 테스트에서도 쓰는 것이라고 적는다.
- **실물을 써서 실패하는 것은 좋은 일이라고 못 박는다** (13장 §"Prefer Realism Over
  Isolation"):[^winters2020-swe-at-google] `Using real implementations can cause your test
  to fail if there is a bug in the real implementation. This is good!`
- **격리 자체가 목적이 아니라는 논거도 같은 절에 있다** — 모든 의존을 대역으로 바꾸면
  저자가 우연히 그 클래스 안에 넣은 구현만 시험하고 다른 클래스에 들어간 구현은 빠지는데,
  좋은 테스트는 구현 구조가 아니라 API로 쓰여야 한다.

## 가짜가 값어치를 갖는 조건

- **가짜가 차선인 이유** (13장 §"Faking"):[^winters2020-swe-at-google] 실물처럼 동작하므로
  `the system under test shouldn't even be able to tell whether it is interacting with a
  real implementation or a fake`.
- **누가 만드는가가 조건이다** (13장 §"When Should Fakes Be Written?"):[^winters2020-swe-at-google]

  > A fake requires more effort and more domain experience to create because it needs to
  > behave similarly to the real implementation. A fake also requires maintenance: whenever
  > the behavior of the real implementation changes, the fake must also be updated to match
  > this behavior. Because of this, the team that owns the real implementation should write
  > and maintain a fake.

- **그리고 값어치가 사용자 수의 함수로 적힌다** (같은 절):[^winters2020-swe-at-google]

  > If there are only a handful of users, it might not be worth their time, whereas if
  > there are hundreds of users, it can result in an obvious productivity improvement.

  **이 한 문장이 이 페이지의 단서 전체를 요약한다.** 가짜를 만들라는 권고는 사용자가 수백인
  API에 대한 것이고, 손에 꼽을 사용자뿐이면 **원문 자신이 값어치가 없을 수 있다고 말한다.**
- **몇 개를 만들 것인가에도 규칙이 있다** (같은 절) — 테스트에 쓸 수 없는 코드의 **뿌리에만**
  가짜를 둔다. 데이터베이스를 못 쓰면 데이터베이스 API 자체에 가짜를 두지, 그것을 부르는
  클래스마다 두지 않는다.
- **충실성의 기준은 API 계약이다** (13장 §"The Fidelity of Fakes").[^winters2020-swe-at-google]
  완전한 충실성은 대개 불가능하고(메모리에 저장하는 가짜 데이터베이스가 디스크 저장까지
  흉내 낼 수 없다), 지켜야 하는 것은 **같은 입력에 같은 출력과 같은 상태 변화**다. 지연
  시간이나 자원 소비를 명시적으로 검증해야 한다면 가짜를 쓸 수 없다.
  - **모르는 경로에서는 빨리 실패시키라**고 적는다 — 지원하지 않는 경로가 실행되면 오류를
    내서 이 자리에 가짜가 맞지 않는다는 것을 알린다.
- **가짜에는 가짜의 테스트가 있어야 한다** (13장 §"Fakes Should Be
  Tested").[^winters2020-swe-at-google] 실물과 가짜 **양쪽에 같은 테스트를 돌리는** 방식을
  들고 그것을 계약 테스트(contract tests)라 부른다. 테스트 없는 가짜는 처음에는 그럴듯해도
  실물이 바뀌는 동안 어긋난다.
- **가짜가 없으면 순서가 정해져 있다** (13장 §"What to Do If a Fake Is Not
  Available").[^winters2020-swe-at-google] 먼저 API 소유자에게 만들어 달라고 하고, 안 되면
  API 호출을 한 클래스로 감싸 그 클래스의 가짜를 만든다. 그래도 안 되면 실물이나 다른 기법의
  대가를 감수한다.
  - **가짜를 최적화로 볼 수 있다는 단서가 같은 절 끝에 있다** — 가짜가 주는 속도 이득이
    만들고 유지하는 품보다 작으면 실물을 쓰는 편이 낫다.
- **데이터베이스 엔진의 가짜에 대해서는 이 조건들이 실제로 어떻게 되는지 보는 자리가 따로
  있다.**
  [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md)이
  그 페이지다. 거기 든 EF Core 인메모리(in-memory) 공급자(provider)는 **실물 구현을 만든
  팀이 만들고 유지하는 가짜**여서 위 조건 하나를 만족하는 듯 보이지만, 그 문서 자신이
  **응용의 데이터베이스 가짜로 만든 물건이 아니라고** 적고 충실성 기준(같은 입력에 같은
  출력·같은 상태 변화)도 지켜지지 않는다고 적는다. **곧 이 페이지의 처방과 그쪽 처방은
  방향이 같고 물러설 자리에서만 갈린다** — 실물이 느릴 때 가짜로 물러서라는 것이 이 절이고,
  그쪽 세 소스는 데이터베이스 엔진에서 그 물러섬이 실패했다고 적는다.

## 스텁이 무엇을 잃는가

**세 가지를 든다** (13장 §"The Dangers of Overusing Stubbing").[^winters2020-swe-at-google]

- **테스트가 불명확해진다.** 왜 이 함수가 스텁됐는지 알려고 대상 시스템을 머릿속으로 따라가고
  있다면 그것이 스터빙이 맞지 않는다는 신호다.
- **테스트가 깨지기 쉬워진다.** 스터빙은 구현 세부를 테스트로 새어 나가게 한다.
- **테스트가 덜 효과적이 된다.** 스텁된 함수가 실물처럼 동작한다는 보장이 없고, 계약을
  테스트 안에 **복제**하게 된다 — `when(stubCalculator.add(1, 2)).thenReturn(3)`이 그 예다.
  그리고 스터빙에는 상태가 없어서 저장한 뒤 다시 꺼내 보는 식의 검증을 할 수 없다.
- **그래도 쓸 자리가 있다** (13장 §"When Is Stubbing Appropriate?"):[^winters2020-swe-at-google]
  대상 시스템을 특정 상태로 몰기 위해 어떤 값을 돌려받아야 할 때다. 실물이나 가짜로는
  일으키기 어려운 오류나 드문 반환값을 흉내 낼 수 있다는 것이 스터빙의 고유 능력이다.
  - **조건이 붙는다** — 스텁하는 함수마다 테스트의 단언과 **직접 관계**가 있어야 하고, 많은
    함수를 스텁해야 한다면 그것은 과용이거나 대상 시스템이 너무 복잡하다는 신호다.

## 상호작용 검증은 언제만 쓰나

- **상태 검증이 먼저다** (13장 §"Prefer State Testing Over Interaction
  Testing"):[^winters2020-swe-at-google] 상호작용 검증은 시스템이 제대로 도는지를 말해 주지
  못하고 **어떤 함수가 예상대로 불렸는지만** 말해 준다. `If database.save(item) is called,
  we assume the item will be saved to the database`라는 가정을 검증하지 않고 그대로 둔다.
- **이 KB의 다른 페이지가 가진 이름이 여기서도 나온다** (13장 §"Prefer State Testing…"):[^winters2020-swe-at-google]

  > Some people at Google jokingly refer to tests that overuse interaction testing as
  > *change-detector tests* because they fail in response to any change to the production
  > code, even if the behavior of the system under test remains unchanged.

  그 이름이 붙은 자리와 해악 서술은
  [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md)이 소유한다.
- **정당한 자리 둘** (13장 §"When Is Interaction Testing Appropriate?"):[^winters2020-swe-at-google]
  실물도 가짜도 쓸 수 없어 상태 검증이 불가능할 때의 대비책, 그리고 **호출 횟수나 순서가
  그 자체로 동작일 때**(캐시가 데이터베이스 호출을 줄이는지 확인하는 경우).
  - **대체재가 아니라고 못 박는다** — 단위 테스트에서 상태 검증을 못 했다면 **더 큰 범위의
    테스트로 보완하라**고 적는다.
- **줄이는 법 둘** (13장 §"Best Practices for Interaction Testing"):[^winters2020-swe-at-google]
  **상태를 바꾸는 함수에만** 상호작용 검증을 건다(상태를 안 바꾸는 함수는 반환값으로 검증할
  수 있으므로 중복이다). 그리고 **과잉 명세를 피한다** — 인자 하나를 검증하려고 모든 인자를
  못 박으면 관계없는 변경에 테스트가 깨진다.
- **12장이 같은 판정을 단위 테스트 쪽에서 한 번 더 한다** (12장 §"Test State, Not
  Interactions").[^winters2020-swe-at-google] 상호작용 검증이 깨지기 쉬운 이유가 비공개
  메서드를 시험하는 것이 깨지기 쉬운 이유와 같다 — **결과가 아니라 결과에 이른 경로를
  검사하기 때문이다.**

## 목이 수만 번 불릴 때 — @DoNotMock

**이 절이 이 장의 규모 전제가 가장 노골적으로 드러나는 자리다** (13장 §"Case Study:
@DoNotMock").[^winters2020-swe-at-google]

- 자바 정적 분석 도구 ErrorProne에 `@DoNotMock` 주석이 있고, API 소유자가 그것으로
  `this type should not be mocked because better alternatives exist`를 선언한다. 그 타입을
  목으로 만들려 하면 **오류가 나고** 실물이나 가짜를 쓰라는 안내가 뜬다.
- **왜 API 소유자가 신경 쓰는가**:[^winters2020-swe-at-google]

  > When the API owner wants to change their API, they might find that it has been mocked
  > thousands or even tens of thousands of times throughout Google's codebase! These test
  > doubles are very likely to exhibit behavior that violates the API contract of the type
  > being mocked—for instance, returning null for a method that can never return null.

- **여기 전제가 셋 겹쳐 있다** — 한 API의 호출지점이 수만이라는 규모, 그 API에 **소유팀**이
  있다는 조직, 그리고 그 선언을 **집행하는 정적 분석**이 빌드에 배선돼 있다는 인프라.
  셋이 없으면 `@DoNotMock`은 주석 한 줄이다.
- **도구 표준화도 같은 방향의 전제다** (12장 §"Defining Test
  Infrastructure").[^winters2020-swe-at-google] 회사가 여러 해 전에 자바 신규 테스트의
  목킹 프레임워크를 Mockito 하나로 **강제**했고 다른 프레임워크를 금지했다고 적는다.
  당시 불만이 있었지만 지금은 좋은 결정으로 본다는 서술이 따라붙는다.

## 대역이 충실하지 않을 때

**14장이 대역의 실패를 큰 테스트의 존재 이유 첫머리에 둔다** (14장 §"Unfaithful
doubles").[^winters2020-swe-at-google]

> Almost all unit tests at Google are written by the same engineer who is writing the unit
> under test. When those unit tests need doubles and when the doubles used are mocks, it is
> the engineer writing the unit test defining the mock and its intended behavior. But that
> engineer usually did not write the thing being mocked and can be misinformed about its
> actual behavior.

- **목은 낡는다** (같은 절) — 목 기반 테스트가 실물 작성자에게 보이지 않으므로, 실물이
  바뀌어도 그 테스트를 고치라는 신호가 오지 않는다.
- **그리고 그 자리에서 위 절의 처방을 다시 가리킨다** (같은 절) — 팀이 자기 서비스의 가짜를
  제공하면 이 걱정이 대체로 해소된다고 적는다. **소유팀이 가짜를 만든다는 조건이 여기서도
  전제다.**
- **충실성이 낮은 대역을 겹치면 어떻게 되는지 예시 계산이 있다** (14장 §"Larger Tests at
  Google Scale").[^winters2020-swe-at-google] 두 서버를 정확도 10%짜리 대역으로 바꾸면 버그가
  있을 확률이 99%(1 − (0.1 × 0.1))라고 적는다. **가정 값을 넣은 산수이고 관측이 아니다** —
  10%라는 정확도의 근거가 원문에 없다.
- **책이 계약 테스트의 다른 계보도 언급한다** (14장 §"Record/replay
  proxies").[^winters2020-swe-at-google] 소비자 주도 계약 테스트(consumer-driven contract
  tests) 도구로 Pact와 Spring Cloud Contracts를 들면서, 구글은 프로토콜 버퍼 의존이 커서
  사내에서 쓰지 않는다고 적는다. 대신 큰 테스트로 트래픽을 **기록**해 두고 작은 테스트에서
  **재생**한다.

## 규모를 떼면 무엇이 남는가

**`verdict: caveat`이 요구하는 단서다.** 이 장의 조문을 1인 프로젝트나 소규모 팀으로 옮길 때
전제가 함께 가지 않으면 조문이 거짓이 된다.

- **"가짜를 쓰라"는 권고가 그대로 옮겨지지 않는다.** 원문이 값어치를 사용자 수의 함수로
  적었고 손에 꼽을 사용자면 시간을 쓸 값이 없을 수 있다고 말한다. **소유팀이 없는 조직에서는
  가짜를 쓰는 쪽이 가짜를 만들고 유지한다** — 그때 이 장의 비용 계산이 성립하지 않는다.
- **`@DoNotMock`류의 집행이 없으면 선호는 규범으로만 남는다.** 위 절의 전제 셋이 그것이다.
  집행 없이 남는 것은 **코드 리뷰에서 사람이 보는 것**뿐이고, 이 책은 그 조건을 다루지 않는다.
- **실물을 쓰라는 권고에는 인프라 값이 붙어 있다.** 느려지면 여러 서버로 흩어 돌린다는
  선택지가 없는 조직에서는 "너무 느려질 때까지 실물을 쓴다"는 절차의 임계가 훨씬 빨리 온다.
- **그럼에도 규모와 무관하게 남는 것 셋** — ① 결과가 아니라 경로를 검사하면 깨지기 쉽다는
  진단, ② 스텁은 계약을 복제하므로 그 계약이 맞는지 보장하지 못한다는 진단, ③ 대역을
  대상 시스템의 저자가 정의하면 실물의 실제 동작과 어긋날 수 있다는 진단. **셋 다 규모가
  아니라 기제에 대한 서술이다.**

## 이 소스의 사각

- **측정이 없다.** 실물 우선이 목 우선보다 낫다는 이 장의 중심 주장에 붙은 근거가 사내
  경험이다. 전후 비교도 대조군도 없다.
- **반대 진영을 인용하지 않는다.** `mockist testing`과 그 창시자들을 언급하지만 어느 문헌도
  지목하지 않고, 그쪽 논거를 적지 않는다. **이 장만 읽고 그 논쟁의 판정으로 삼을 수 없다.**
- **팀마다 다르다고 적고 얼마나 다른지는 적지 않는다.** 실제 적용이
  `varies widely from team to team`이라는 문장에 분포가 없다.
- **`@DoNotMock`의 효과가 없다.** 주석이 도입된 뒤 무엇이 얼마나 줄었는지가 적혀 있지 않다.
- **가짜의 비용이 정량화돼 있지 않다.** 사용자 수백이면 값어치가 있다는 문장에 그 수백이
  어디서 왔는지가 없다.
- **계약 테스트의 실무가 얇다.** 가짜에 실물과 같은 테스트를 돌리라고 적지만, 계약이 바뀔 때
  어느 쪽이 먼저 깨지는지 어떻게 알리는지는 다루지 않는다.

## 이어지는 페이지

- [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md) — 같은
  책 11·12·14장. small의 제약이 대역을 요구하는 자리이고, 이 페이지는 그 요구에 무엇으로
  답하는지를 다룬다
- [가짜와 목](../concepts/fakes-versus-mocks.md) — 다른 소스가 같은 선택을 다룬 자리. 그쪽은
  파이썬 실무 책이고 결론의 방향이 같다(상태 중심·고전 학파). 두 문헌이 서로를 인용한 적은
  없고, 이 KB의 대역 축을 어느 페이지가 소유할지는 그 축을 다루는 다음 반입에서 정한다
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — **같은 물음에
  다른 축으로 답한 자리.** 이 페이지는 실물 · 가짜 · 스텁 · 상호작용 검증이라는 **선호
  순서**를 규모 조건 위에 세우고, 그쪽은 순서 대신 **경계 하나**로 답한다 — 응용 경계를
  넘고 외부에서 관찰되는 통신만 목으로 검사하고 나머지는 실물을 쓰라는 것이다. **두 답이
  데이터베이스에서 만난다** — 이 페이지가 실물을 먼저 쓰되 느려지면 가짜로 물러선다고
  적는 자리에서, 그쪽은 응용 전용 데이터베이스를 목으로 바꾸는 것 자체를 금지한다.
  **그 둘이 어긋나는지 같은 말인지는 이 KB의 미해결 물음이다**
- [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md) —
  이 선호 순서가 다른 조직들에서 어떻게 되는지를 잰 심사 실증 둘. **이 페이지가 실물을
  먼저 쓰라고 하는 자리(데이터베이스·웹 서비스)가 실측에서 가장 많이 목으로 대체되는
  범주다.** 다만 그 실증은 관행의 분포만 재었고 어느 쪽이 더 나은지는 재지 않았다
- [목 객체는 역할을 발견하기 위한 것이다](../concepts/mock-objects-for-role-discovery.md) —
  **이 페이지와 방향이 반대인 원전.** 이 페이지가 상호작용 검증을 선호 순서의 맨 뒤로
  미루는데, 그쪽은 그것을 설계를 이끄는 주된 도구로 쓴다. **두 논거의 층이 다르다** —
  이 페이지는 한 API가 수만 번 목으로 대체될 때의 문제로 논증하고, 그쪽은 좁은 역할
  인터페이스가 발견된다는 것으로 논증한다
- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) —
  이 페이지가 "결과가 아니라 경로를 검사하면 깨지기 쉽다"로 적은 진단에 이름과 잣대를
  붙인 자리. 그쪽은 그것을 거짓 양성의 유일한 원인으로 지목하고, 거기서 이 선호 순서와는
  다른 결론(순서가 아니라 경계)을 끌어낸다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 이 장이
  농담처럼 부르는 `change-detector test`에 이름을 붙이고 해악을 적은 같은 회사의 규범 글
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — 13장이
  이음매(seam)를 만드는 흔한 기법으로 든 것의 실물
- [종단 테스트를 왜 줄이는가](../concepts/why-fewer-end-to-end-tests.md) — "작게 생각하라"는
  처방이 실제로 요구하는 것이 이 페이지의 선호 순서다. 그쪽이 왜 작아야 하는가를, 이 페이지가
  작으려면 무엇을 세워야 하는가를 소유한다
- [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md) —
  실물이 드물게 불안정(flaky)을 일으키면 견디고 자주 일으키면 대역으로 바꾸라는 이 페이지의
  판단이 어떤 원인들 위의 판단인가. 그쪽의 Network 범주 처방이 모의를 최선의 고침으로 들고,
  이 페이지는 그 모의의 대가를 적는다
- [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md) —
  **이 선호 순서의 둘째 칸이 데이터베이스에서 어떻게 되는지를 다룬 자리.** 첫째 칸(실물
  우선)에서는 방향이 같고, **실물이 느릴 때 가짜로 물러서라는 대목에서 긴장이 생긴다** —
  그쪽 세 소스는 데이터베이스 엔진의 가짜에서 그 물러섬이 실패했다고 적는다. 다만 이
  페이지가 가짜에 붙인 조건 둘(소유팀이 유지 · 계약 테스트로 충실도 검사)을 그 사례에 대
  보면 긴장이 좁아진다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이 갈래의 허브. 작은
  테스트를 성립시키는 자리로 이 페이지가 거기 든다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 형제 허브. 대역을 쓰면 기대값이
  무엇을 근거로 서는가가 그 축의 질문이다

[^winters2020-swe-at-google]: Winters, Manshreck & Wright(큐레이터) 2020,
    *Software Engineering at Google*, abseil.io 공개판(CC BY-NC-ND 4.0), 2026-08-23
    열람본. 인용한 장은 11장 `Testing Overview`(저자 Adam Bender) · 12장
    `Unit Testing`(저자 Erik Kuefler) · 13장 `Test Doubles`(저자 Andrew Trenk·Dillon
    Bly) · 14장 `Larger Testing`(저자 Joseph Graves)이다. **공개판 HTML에 쪽 번호가 없어
    locator는 장 번호와 원문 절 제목이다.** 직인용은 원문 표기 그대로이고, 13장의 자바
    코드 예제는 개념 설명에 필요한 조각만 인라인 표기로 옮겼다. 근거 등급·규모 전제·인용
    규약은 [소스 메타](../sources/winters2020-swe-at-google.md)가 정본이다.

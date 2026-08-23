---
type: concept
title: 대역 어휘와 두 TDD 스타일
description: 테스트 대역을 부르는 말이 어떻게 갈리고 그 위의 스타일 선택이 무엇을 바꾸는가 — 하나로 뭉쳐 있던 것이 검증 방식의 구분과 TDD 스타일의 구분 둘로 갈라진 자리, 더미와 가짜와 스텁과 스파이와 목의 정의 다섯과 그 어휘의 진짜 소유자, 목만이 행위 검증을 요구하고 스텁은 양쪽 다 된다는 판정, 언제 대역을 쓰는가로 갈리는 클래시컬과 모키스트의 정의, 두 스타일이 갈리는 다섯 축과 각 축에서 서로가 서로를 무엇으로 비판하는가, 스타일과 무관하게 요구되는 것 하나, 그리고 이 구분을 지은 저자 자신이 판정을 유보했고 그 뒤로 개정 기록이 늘지 않았다는 사실
generated: { by: "claude-opus-5", at: "2026-08-23T20:00:00Z" }
sources:
  - { id: fowler2007-mocks-arent-stubs, resource: /it/sources/fowler2007-mocks-arent-stubs.md }
---

# 대역 어휘와 두 TDD 스타일

- [이 소스의 지위와 저자의 유보](#이-소스의-지위와-저자의-유보)
- [하나가 아니라 두 개의 구분이다](#하나가-아니라-두-개의-구분이다)
- [대역 다섯의 정의](#대역-다섯의-정의)
- [상태 검증과 행위 검증](#상태-검증과-행위-검증)
- [클래시컬과 모키스트](#클래시컬과-모키스트)
- [두 스타일이 갈리는 다섯 축](#두-스타일이-갈리는-다섯-축)
- [스타일과 무관하게 요구하는 것](#스타일과-무관하게-요구하는-것)
- [이 글에 없는 것](#이-글에-없는-것)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트 대역(test double)을 부르는 말은 어떻게 갈리며, 그 갈래 위에 선 두 TDD
스타일 가운데 하나를 고르는 일은 무엇을 바꾸는가.**

## 이 소스의 지위와 저자의 유보

- **근거 등급은 `essay`다.** 실험도 표본도 측정도 없고, 이 글에는 인용할 수 있는 수치가
  하나도 없다. 논거의 재료는 두 스타일의 실천자들과 나눈 대화와 저자의 관찰이다.
- **글 자신이 자기를 에세이로 규정한다** (§"The Difference Between Mocks and
  Stubs"):[^fowler2007-mocks-arent-stubs]

  > For this article I'm going to follow the vocabulary of Gerard Meszaros's book. It's not
  > what everyone uses, but I think it's a good vocabulary and since it's my essay I get to
  > pick which words to use.

- **이 구분을 지은 사람이 그 구분의 판정을 유보한다.** 마지막 물음절의 제목이 그대로
  "So should I be a classicist or a mockist?"인데 답이 유보다
  (§"So should I be a classicist or a mockist?"):[^fowler2007-mocks-arent-stubs]

  > I find this a difficult question to answer with confidence. Personally I've always been
  > a old fashioned classic TDDer and thus far I don't see any reason to change. I don't
  > see any compelling benefits for mockist TDD, and am concerned about the consequences of
  > coupling tests to implementation.

  - **유보의 근거로 저자가 드는 것이 자기 경험의 부족이다** (같은 절):[^fowler2007-mocks-arent-stubs]

    > I also suffer from the disadvantage of not trying mockist TDD on anything more than
    > toys. As I've learned from Test Driven Development itself, it's often hard to judge a
    > technique without trying it seriously. I do know many good developers who are very
    > happy and convinced mockists. So although I'm still a convinced classicist, I'd rather
    > present both arguments as fairly as I can so you can make your own mind up.

  - **자기 신고가 두 겹이다** — 진영은 클래시시스트(classicist)라고 밝히고, 그럼에도 판정은
    독자에게 넘긴다. **그러므로 이 글은 논쟁의 판정문이 아니라 논쟁의 지도다.** 이 페이지를
    인용해 "파울러가 모키스트를 기각했다"고 적으면 문면에 없는 말이 된다.
  - 글의 목적도 저자가 직접 적는다 (§"Final Thoughts"): **"The purpose of this article was,
    and is, to point out these differences and to lay out the trade-offs between them."**
    이어서 **"I hope that in the next few years we'll see more written on this and that
    will deepen our understanding"**라고 적는다 — 스스로 미완이라고 말하는
    자리다.[^fowler2007-mocks-arent-stubs]
- **그 뒤로 저자의 개정 기록이 늘지 않았다.** 확보본 말미 「Significant Revisions」에 적힌
  날짜는 둘뿐이다 — **"08 July 2004: First published"**와 **"02 January 2007"**(그때
  상태·행위 검증과 클래시컬·모키스트로 구분을 둘로 쪼갰다는 기록)이다. 머리글에 인쇄된
  날짜도, 페이지가 심은 `og:article:modified_time`도 `2007-01-02`다.[^fowler2007-mocks-arent-stubs]
  - **이 KB는 이 사실을 이 두 날짜 이상으로 말하지 않는다.** "저자가 뒤에 생각을
    바꾸지 않았다"는 것도, "이 논쟁이 그 뒤로 진전이 없었다"는 것도 이 소스가 말하는 바가
    아니다. 확보본이 보증하는 것은 **저자 자신의 개정 기록이 2007-01-02에서 멈춰 있다**는
    것뿐이다.
  - #hypothesis 개정 기록에 없는 편집은 있었던 것으로 보인다 — 확보본 문면이 BDD 소개자를
    `Daniel Terhorst-North`로 적는데, 이 표기는 2007년 문면의 이름이 아니다. 그러므로
    "미갱신"은 **저자가 유의미하다고 신고한 개정**의 이야기이지 파일이 한 글자도 안 바뀌었다는
    이야기가 아니다.
- **그리고 이것이 이 소스가 이 KB에 서는 자리다.** 어휘를 지은 쪽이 판정을 미뤄 둔 채 20년
  가까이 개정 기록이 멈춰 있다는 것은, 이 논쟁이 문헌 안에서 **해소되지 않았다는 증거**로
  읽힌다. 이 페이지는 그 미해결을 지우지 않고 남기는 쪽으로 쓰였다.

## 하나가 아니라 두 개의 구분이다

- **이 글의 중심 주장은 정의가 아니라 분리다.** 사람들이 하나로 뭉쳐 쓰던 것이 사실은 서로
  독립인 두 구분이라고 못 박는다 (§"Mocks Aren't Stubs" 도입부):[^fowler2007-mocks-arent-stubs]

  > This difference is actually two separate differences. On the one hand there is a
  > difference in how test results are verified: a distinction between state verification
  > and behavior verification. On the other hand is a whole different philosophy to the way
  > testing and design play together, which I term here as the classical and mockist styles
  > of Test Driven Development.

  - **`which I term here as` — 클래시컬(classical)과 모키스트(mockist)라는 이름이 이 문장에서
    지어진다.** 이 글에 귀속되는 창안이 이것이다.
  - 2007년 개정이 한 일도 정확히 이 분리다. 개정 기록의 문면이
    **"Split the original distinction of state-based versus interaction-based testing into
    two"**이다.[^fowler2007-mocks-arent-stubs]
- **두 구분의 무게가 같지 않다고 저자가 명시한다** (§"Choosing Between the
  Differences"):[^fowler2007-mocks-arent-stubs]

  > So as we see, state versus behavior verification is mostly not a big decision. The real
  > issue is between classic and mockist TDD.

  - **검증 방식은 대개 결정 사항이 아니고, 진짜 쟁점은 스타일이다.** 쉬운 협력이면 스타일이
    답을 정해 버리고(클래시시스트는 실물, 모키스트는 목), 어려운 협력이면 모키스트는 여전히
    답이 정해져 있고 클래시시스트만 선택이 남는데 그 선택은 사안별로 편한 쪽을 고르면 되는
    정도라고 적는다.[^fowler2007-mocks-arent-stubs]
  - **예외 하나를 저자가 스스로 든다** (같은 절) — 캐시(cache)다. 적중했는지 빗나갔는지를
    상태로는 알 수 없으므로 **"this is a case where behavior verification would be the wise
    choice for even a hard core classical TDDer"**라고 적는다.[^fowler2007-mocks-arent-stubs]
    **상태 검증을 선호하는 쪽에도 행위 검증이 유일한 수단인 자리가 있다**는 뜻이고, 이것이
    두 구분이 독립이라는 주장의 실물이다.

## 대역 다섯의 정의

- **어휘의 소유자가 이 글이 아니라는 것을 먼저 적어 둔다.** 저자가 낱말이 엉킨 상황을
  서술하고(**"all sorts of words are used: stub, mock, fake, dummy"**) 남의 어휘를 따르기로
  한다 — 대역(test double)이라는 총칭도, 그 아래 다섯 갈래도 Meszaros의
  것이다 (§"The Difference Between Mocks and Stubs"):[^fowler2007-mocks-arent-stubs]

  > Meszaros uses the term Test Double as the generic term for any kind of pretend object
  > used in place of a real object for testing purposes. The name comes from the notion of a
  > Stunt Double in movies. (One of his aims was to avoid using any name that was already
  > widely used.) Meszaros then defined five particular kinds of double:

  - 대상 시스템(system under test, SUT)과 협력자(collaborator)를 가리키는 말도 남의
    것이다 — **"Following Meszaros I'll use System Under Test, or rather the abbreviation
    SUT."**[^fowler2007-mocks-arent-stubs] 이 글의 앞 판에서는 각각 `primary object`·
    `secondary objects`라고 불렀다고 저자가 밝힌다(§"Regular Tests").
  - **목 객체(mock object)라는 말조차 이 글이 지은 것이 아니다** — 첫 문단이
    **"I first came across the term “mock object” a few years ago in the Extreme
    Programming (XP) community"**로 시작한다.[^fowler2007-mocks-arent-stubs]
- **다섯의 정의는 왜곡에 민감한 자리이므로 문면 그대로 옮긴다** (§"The Difference Between
  Mocks and Stubs"):[^fowler2007-mocks-arent-stubs]

  > **Dummy** objects are passed around but never actually used. Usually they are just used
  > to fill parameter lists.
  >
  > **Fake** objects actually have working implementations, but usually take some shortcut
  > which makes them not suitable for production (an in memory database is a good example).
  >
  > **Stubs** provide canned answers to calls made during the test, usually not responding
  > at all to anything outside what's programmed in for the test.
  >
  > **Spies** are stubs that also record some information based on how they were called. One
  > form of this might be an email service that records how many messages it was sent.
  >
  > **Mocks** are what we are talking about here: objects pre-programmed with expectations
  > which form a specification of the calls they are expected to receive.

  한국어 대응은 더미(dummy)·가짜(fake)·스텁(stub)·스파이(spy)·목(mock)이다. **다섯을 가르는
  기준이 하나가 아니라는 점이 이 목록의 성질이다** — 더미는 쓰이지 않음으로, 가짜는 구현이
  있음으로, 스텁은 정해진 답을 냄으로, 스파이는 기록을 함으로, 목은 기대를 미리 심음으로
  갈린다.
- **다섯 가운데 목만이 행위 검증을 요구한다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > Of these kinds of doubles, only mocks insist upon behavior verification. The other
  > doubles can, and usually do, use state verification. Mocks actually do behave like other
  > doubles during the exercise phase, as they need to make the SUT believe it's talking with
  > its real collaborators - but mocks differ in the setup and the verification phases.

  - **그래서 스텁과 목의 차이가 "무엇으로 만들었는가"가 아니라 "어느 단계가 다른가"에 있다.**
    행사(exercise) 단계에서 목은 다른 대역과 똑같이 행동하고, 다른 것은 설정(setup)과
    검증(verification) 단계다.
  - **스텁은 양쪽 다 된다** (같은 절) — **"Mock objects always use behavior verification, a
    stub can go either way. Meszaros refers to stubs that use behavior verification as a
    Test Spy."**[^fowler2007-mocks-arent-stubs] 스텁을 상태 검증에 쓰려면 검증용 메서드를
    스텁에 덧붙이게 되는데, 저자가 그 대가를 같은 자리에서 적는다 — 그 스텁은 인터페이스를
    구현하면서 **테스트용 메서드를 추가로 갖게 된다**.
- **대역이 필요해지는 이유는 단위의 성질에서 나온다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > When you're doing testing like this, you're focusing on one element of the software at a
  > time -hence the common term unit testing. The problem is that to make a single unit work,
  > you often need other units

## 상태 검증과 행위 검증

- **상태 검증(state verification)의 정의** (§"Regular Tests"):[^fowler2007-mocks-arent-stubs]

  > This style of testing uses state verification: which means that we determine whether the
  > exercised method worked correctly by examining the state of the SUT and its collaborators
  > after the method was exercised.

- **행위 검증(behavior verification)의 정의** (§"Tests with Mock
  Objects"):[^fowler2007-mocks-arent-stubs]

  > The key difference here is how we verify that the order did the right thing in its
  > interaction with the warehouse. With state verification we do this by asserts against the
  > warehouse's state. Mocks use behavior verification, where we instead check to see if the
  > order made the correct calls on the warehouse.

  - **단언이 하나도 없을 수 있다는 대목이 이 차이의 극단이다** (같은 절) — 대상 시스템만
    단언으로 검사되고, **"if the method doesn't change the state of the order there's no
    asserts at all"**.[^fowler2007-mocks-arent-stubs]
- **설정 단계가 둘로 쪼개진다** (§"Tests with Mock Objects"):[^fowler2007-mocks-arent-stubs]
  목을 쓰는 테스트의 설정은 데이터(data)와 기대(expectations) 두 부분이고, 기대는
  **대상 시스템이 행사될 때 목의 어떤 메서드가 불려야 하는가**를 미리 적는다. 검증도 둘이다 —
  대상 시스템에 대한 단언과 목 자신에 대한 검증(`warehouseMock.verify()`)이다.
  - xUnit의 네 단계(setup·exercise·verify·teardown)는 두 스타일에서 같고, 달라지는 것은
    **그 안에 무엇이 들어가는가**다.[^fowler2007-mocks-arent-stubs]
- **도구가 기대를 표현하는 방식이 둘로 갈린다** (§"Using EasyMock"):[^fowler2007-mocks-arent-stubs]
  한쪽(jMock)은 메서드 이름을 문자열로 적고 제약을 느슨하게 걸 수 있고, 다른 쪽(EasyMock)은
  기록·재생(record/replay) 방식이라 실제 메서드를 호출해 기대를 적는다.
  - **교환이 명시된다** — 실제 호출을 쓰면 IDE 자동 완성과 이름 리팩터링이 따라오지만
    (**"any refactoring of method names will automatically update the tests"**) 느슨한
    제약을 걸 수 없다. 문자열을 쓰면 반대가 된다. **도구 표기가 2007년의 것이므로 이
    KB는 API 형태를 현행 사용법으로 옮기지 않는다.**

## 클래시컬과 모키스트

- **두 스타일을 가르는 질문은 하나다** (§"Classical and Mockist
  Testing"):[^fowler2007-mocks-arent-stubs] **"The big issue here is when to use a mock (or
  other double)."** 곧 **언제 대역을 쓰는가**이지 어떤 대역을 쓰는가가 아니다.

  > The classical TDD style is to use real objects if possible and a double if it's awkward
  > to use the real thing. So a classical TDDer would use a real warehouse and a double for
  > the mail service. The kind of double doesn't really matter that much.
  >
  > A mockist TDD practitioner, however, will always use a mock for any object with
  > interesting behavior.

  - **클래시컬 쪽에서 대역의 종류가 중요하지 않다**는 문장이 위 [대역 다섯의
    정의](#대역-다섯의-정의)와 이 절을 잇는 고리다 — 어휘의 구분은 정밀하지만 클래시컬
    스타일에서는 그 구분이 결정에 거의 영향을 주지 않는다.
  - **도구는 스타일과 함께 가지 않는다** (같은 절) — 목 프레임워크들이 모키스트를 염두에 두고
    설계됐지만 **"many classicists find them useful for creating doubles"**라고
    적는다.[^fowler2007-mocks-arent-stubs] **목 프레임워크를 쓴다는 사실이 모키스트라는
    증거가 아니다.**
- **다른 이름들도 함께 적혀 있다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > You sometimes see “Detroit” style used for “classical” and “London” for “mockist”. This
  > alludes to the fact that XP was originally developed with the C3 project in Detroit and
  > the mockist style was developed by early XP adopters in London. I should also mention
  > that many mockist TDDers dislike that term, and indeed any terminology that implies a
  > different style between classical and mockist testing. They don't consider that there is
  > a useful distinction to be made between the two styles.

  - **마지막 문장이 이 페이지에서 가장 자주 잊히는 사실이다** — **구분 자체를 인정하지 않는
    쪽이 있다.** 이 글이 세운 이분법은 한쪽 진영이 동의하지 않는 이분법이고, 저자가 그것을
    자기 글 안에 적어 두었다.
  - 이 KB의 다른 페이지가 쓰는 "런던 학파"·"고전 학파"라는 역어가 여기 나온 별칭
    계열(Detroit/London)과 같은 자리를 가리킨다. **이 페이지는 저자가 지은 이름 쪽을 음차로
    쓴다** — 클래시컬(classical)·모키스트(mockist), 사람을 가리킬 때는
    클래시시스트(classicist)·모키스트(mockist).

    | 이 페이지 | [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md) | 같은 자리인 근거 |
    |---|---|---|
    | 클래시컬(classical) · 클래시시스트(classicist) | 고전 학파(classical school) | 두 소스 모두 Detroit를 별칭으로 든다 |
    | 모키스트(mockist) | 런던 학파(London school) | 그쪽 소스가 London을 고르며 mockist를 피한다고 명시한다 |

  - **그리고 위 인용의 마지막 문장이 다른 소스에서 표기 규칙으로 실행된 것이 보인다.**
    같은 갈림을 다루는 [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md)의
    소스가 그 낱말을 쓰지 않기로 하며 이유를 적는데, 그 이유가 여기 적힌 관찰과 같다 —
    그 스타일을 따르는 사람들이 `mockist`라는 말을 싫어한다는 것이다. **한쪽이 관찰로
    남긴 것을 다른 쪽이 규칙으로 삼았다.**
- **BDD가 모키스트의 갈래로 소개된다** (같은 절):[^fowler2007-mocks-arent-stubs]
  행위 주도 개발(Behavior Driven Development, BDD)이 **"an important offshoot of the mockist
  style"**로 적히고, 테스트를 행위로 이름 바꾼 것이 TDD를 설계 기법으로 배우게 하려는
  의도였다고 서술된다. **"BDD takes a mockist approach, but it expands on this"** — 다만
  저자가 이 글에서 더 다루지 않으므로 이 KB도 여기까지만 옮긴다(원전은 2차 경유).

## 두 스타일이 갈리는 다섯 축

**저자가 판정하지 않고 양쪽 논거를 나란히 놓는 방식이 이 절들의 형식이다.** 축마다 한쪽의
주장과 다른 쪽의 반박이 함께 적혀 있다.

### TDD를 어느 쪽에서 시작하는가

- **모키스트 쪽은 필요 주도(need-driven)·바깥에서 안으로(outside-in)다**
  (§"Driving TDD"):[^fowler2007-mocks-arent-stubs] 시스템 바깥쪽 인터페이스 객체를 첫 대상
  시스템으로 삼아 협력자에 대한 기대를 먼저 생각하고, 그 기대 하나하나가 다음 단계의 사양이
  되어 안쪽으로 한 층씩 들어간다. 저자가 이 방식을 **"a very structured and controlled
  approach, one that many people believe is helpful to guide newcomers to OO and TDD"**라고
  적는다.
- **클래시컬 쪽에는 같은 안내가 없다** (같은 절) — **"Classic TDD doesn't provide quite the
  same guidance."** 비슷한 단계 밟기를 하려면 목 대신 값을 박아 넣은 메서드를 쓰고 초록이
  되면 제대로 된 코드로 바꾼다.[^fowler2007-mocks-arent-stubs]
- **대신 클래시컬에는 다른 진행 방향이 있다** (같은 절) — 가운데서 바깥으로(middle-out)다.
  기능에 필요한 도메인 객체를 먼저 만들어 돌아가게 한 뒤 UI를 얹으며,
  **"Doing this you might never need to fake anything"**. 이 방식을 좋아하는 이유로 드는
  것이 도메인 논리가 UI로 새는 것을 막는다는 점이다.[^fowler2007-mocks-arent-stubs]
- **양쪽이 공유하는 것도 적어 둔다** (같은 절) — 둘 다 층별이 아니라 이야기 단위로
  진행한다. 층을 하나씩 완성해 올라가는 학파는 **"Both classicists and mockists"**와 다르다고
  가른다.[^fowler2007-mocks-arent-stubs]

### 픽스처를 짓는 비용

- **클래시컬은 협력자를 전부 만들어야 한다** (§"Fixture Setup"):[^fowler2007-mocks-arent-stubs]
  실제 테스트는 부차 객체가 많고 매 실행마다 만들고 허문다. 그래서 픽스처(fixture)를
  재사용하게 되고,
  여러 테스트 클래스가 쓰는 복잡한 픽스처는 별도 생성 클래스로 뽑는다 — 저자가 이것을
  **Object Mothers**라 부르고 그 이름의 출처가 이른 시기 사내 XP 프로젝트의 관례라고 적는다.
  - **그 대가도 같은 자리에 있다** — 마더는 유지해야 하는 코드이고
    **"any changes to the mothers can have significant ripple effects through the tests"**.
- **모키스트는 대상 시스템과 그 직접 이웃의 목만 만들면 된다** (같은 절) — 다만 저자가 바로
  단서를 붙인다: **"(At least in theory. I've come across tales of pretty complex mock
  setups, but that may be due to not using the tools well.)"**[^fowler2007-mocks-arent-stubs]
- **결론이 무승부로 적힌다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > As a result I've heard both styles accuse the other of being too much work. Mockists say
  > that creating the fixtures is a lot of effort, but classicists say that this is reused
  > but you have to create mocks with every test.

### 테스트 격리

- **모키스트가 드는 가장 강한 논거가 여기 있다** (§"Test Isolation"):[^fowler2007-mocks-arent-stubs]

  > If you introduce a bug to a system with mockist testing, it will usually cause only tests
  > whose SUT contains the bug to fail. With the classic approach, however, any tests of
  > client objects can also fail, which leads to failures where the buggy object is used as a
  > collaborator in another object's test. As a result a failure in a highly used object
  > causes a ripple of failing tests all across the system.

- **클래시시스트 쪽 반박은 그것이 실제 문제가 아니라는 것이다** (같은 절) — 어느 테스트들이
  깨졌는지 보면 범인을 대개 쉽게 짚을 수 있고, 정기적으로 테스트를 돌리고 있다면 마지막
  편집이 원인임을 알기 때문이라고 적는다.[^fowler2007-mocks-arent-stubs]
- **저자가 진짜 원인을 다른 데로 돌린다** (같은 절) — 문제의 정체는 테스트의 **알갱이
  크기**이고, 여러 객체 뭉치를 한 테스트가 덮고 있으면 원인 찾기가 어려워진다. 그것은
  **"a failure to do classic testing properly"**이지 기법의 실패가 아니라고 판정한다.
  어림 규칙도 붙인다 — 클래스마다 고운 알갱이 테스트를 두고, 뭉치를 다루더라도
  **"no more than half a dozen"**으로 제한한다.[^fowler2007-mocks-arent-stubs]
- **그리고 양쪽이 서로 다른 것을 잃는다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > In essence classic xunit tests are not just unit tests, but also mini-integration tests.
  > As a result many people like the fact that client tests may catch errors that the main
  > tests for an object may have missed, particularly probing areas where classes interact.
  > Mockist tests lose that quality. In addition you also run the risk that expectations on
  > mockist tests can be incorrect, resulting in unit tests that run green but mask inherent
  > errors.

  - **초록인데 오류를 감춘다**는 이 마지막 문장이 대역이 낳는 가짜 성공의 자리다. 클래시컬은
    소음(연쇄 실패)을 얻고 모키스트는 침묵(잘못된 기대)을 얻는다.

### 구현에 대한 결합

- **모키스트 테스트는 메서드의 구현에 더 결합된다** (§"Coupling Tests to
  Implementations"):[^fowler2007-mocks-arent-stubs]

  > When you write a mockist test, you are testing the outbound calls of the SUT to ensure it
  > talks properly to its suppliers. A classic test only cares about the final state - not
  > how that state was derived. Mockist tests are thus more coupled to the implementation of
  > a method. Changing the nature of calls to collaborators usually cause a mockist test to
  > break.

- **같은 사실이 양쪽에서 반대로 읽힌다** (같은 절):[^fowler2007-mocks-arent-stubs] 테스트를
  쓰면서 구현을 생각하게 되는 것을 **"mockist testers see this as an advantage"**로 적고,
  클래시시스트는 테스트를 다 쓸 때까지 구현 고려를 미루는 것이 중요하다고 본다고 적는다.
  **한쪽의 이득이 다른 쪽의 손해로 서술되는 자리다.**
- **리팩터링에 걸리는 대가는 한 방향이다** (같은 절) —
  **"Coupling to the implementation also interferes with refactoring, since implementation
  changes are much more likely to break tests than with classic testing."**[^fowler2007-mocks-arent-stubs]
  - 도구가 그것을 악화시킬 수 있다는 서술이 이어진다 — 목 도구가 이 테스트와 상관없는 인자까지
    못 박게 만드는 경우가 흔하고, 그것을 느슨하게 하려면 문자열을 쓰게 되어 리팩터링이 다시
    까다로워진다.[^fowler2007-mocks-arent-stubs] **위 [상태 검증과 행위
    검증](#상태-검증과-행위-검증)의 도구 교환이 여기서 되돌아온다.**

### 설계 스타일

**저자가 이 축을 가장 흥미로워하면서 동시에 가장 얕게 안다고 밝힌다** — **"I'm sure I'm
barely scratching the surface"**(§"Design Style").[^fowler2007-mocks-arent-stubs]

- **층을 다루는 방향이 다르다** (같은 절) — 모키스트는 바깥에서 안으로, 도메인 모델 우선을
  좋아하는 쪽은 클래시컬로 기운다.[^fowler2007-mocks-arent-stubs]
- **반환값 대신 수집 객체를 쓰는 경향** (같은 절) — 여러 객체에서 정보를 모아 문자열을 만들 때
  클래시컬 쪽은 반환값을 조립하고, 모키스트 쪽은 문자열 버퍼를 인자로 넘겨 각 객체가 채우게
  하는 수집 매개변수(collecting parameter) 형태를 더 쓴다고 적는다.[^fowler2007-mocks-arent-stubs]
- **메서드 사슬을 피하는 경향** (같은 절) — 모키스트가 `getThis().getThat().getTheOther()`
  같은 사슬을 더 경계하고, 그것이 데메테르의 법칙(Law of Demeter)이라고 적는다. **저자가
  여기서도 한쪽을 편들지 않는다** — 사슬도 냄새지만 전달 메서드로 비대해진 중간자도 냄새라고
  적고, 법칙 이름에 대한 농담(**"I'd be more comfortable with the Law of Demeter if it were
  called the Suggestion of Demeter"**)을 붙인다.[^fowler2007-mocks-arent-stubs]
- **Tell Don't Ask** (같은 절) — 모키스트는 자기네 방식이 이 원칙을 밀어 주고 게터가 흩뿌려지는
  것을 막는다고 주장하고, 클래시시스트는 그렇게 하는 다른 방법이 많다고 반박한다.[^fowler2007-mocks-arent-stubs]
- **상태 검증이 지불하는 값 하나가 인정된다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > An acknowledged issue with state-based verification is that it can lead to creating query
  > methods only to support verification. It's never comfortable to add methods to the API of
  > an object purely for testing, using behavior verification avoids that problem. The
  > counter-argument to this is that such modifications are usually minor in practice.

  **테스트를 위해 API에 메서드를 더하게 된다**는 것이 상태 검증 쪽의 비용이고, 위
  [대역 다섯의 정의](#대역-다섯의-정의)에서 스텁에 검증용 메서드를 덧붙이던 것과 같은 값이다.
- **역할 인터페이스(role interface)** (같은 절) — 협력마다 따로 목이 만들어지므로 그 협력이
  역할 인터페이스로 굳을 가능성이 커진다고 모키스트가 주장한다.[^fowler2007-mocks-arent-stubs]
- **그리고 이 축이 논쟁의 진짜 동기라고 저자가 못 박는다** (같은 절):[^fowler2007-mocks-arent-stubs]

  > It's important to remember that this difference in design style is a key motivator for
  > most mockists. TDD's origins were a desire to get strong automatic regression testing
  > that supported evolutionary design. Along the way its practitioners discovered that
  > writing tests first made a significant improvement to the design process. Mockists have a
  > strong idea of what kind of design is a good design and have developed mock libraries
  > primarily to help people develop this design style.

  - **그러므로 이 논쟁은 테스트 기법의 논쟁이 아니라 설계관의 논쟁이다.** 목 라이브러리가
    그 설계관을 퍼뜨리려고 만들어졌다는 것이 저자의 서술이고, 이것이 "어느 쪽이 버그를 더 잘
    잡는가"로 판정할 수 없는 이유다.

## 스타일과 무관하게 요구하는 것

- **이 글이 조건 없이 요구하는 것은 하나뿐이다** (§"Test Isolation"):[^fowler2007-mocks-arent-stubs]

  > It's at this point that I should stress that whichever style of test you use, you must
  > combine it with coarser grained acceptance tests that operate across the system as a
  > whole. I've often come across projects which were late in using acceptance tests and
  > regretted it.

  - **`must`가 이 글에서 유일하게 쓰이는 자리다.** 스타일 선택은 전부 교환으로 서술되는데,
    더 굵은 알갱이의 수용 테스트를 함께 두라는 것만은 조건 없이 요구된다.
  - 근거는 여전히 경험 진술이다(**"I've often come across projects"**). **이 글의 등급이
    `essay`라는 사실은 이 요구에도 그대로 걸린다.**
- **마지막 절이 독자에게 남기는 것도 판정이 아니라 이해다** (§"Final
  Thoughts"):[^fowler2007-mocks-arent-stubs] 목 프레임워크를 쓰면서 그 밑에 깔린
  모키스트·클래시컬의 갈림을 모르는 경우가 많다고 적고,
  **"While you don't have to be a mockist to find the mock frameworks handy, it is useful to
  understand the thinking that guides many of the design decisions of the software"**로 맺는다.

## 이 글에 없는 것

**이 소스에 자주 잘못 귀속되는 것들이다. 확보본 전문 검색으로 확인한 결과를 적는다.**

- **"Don't mock what you don't own"은 이 글에 없다.** 그 변형인 "Only Mock Types You Own"도
  없다. `own`이라는 낱말은 `on your own`·`your own mind up` 같은 자리에서만 나온다. 이
  표어는 커뮤니티에서 굳은 말이고, 이 글이 참고 문헌으로 가리키는 Freeman & Pryce 쪽 계보에
  속한다 — **그 원전을 이 KB가 아직 갖고 있지 않으므로 여기서는 이 소스에 없다는 사실까지만
  적는다.**
  - 이 글이 그 문헌을 가리키는 방식은 링크 한 줄이다 (§"Further Reading") — 모키스트 스타일의
    가장 좋은 자료로 Freeman & Pryce를 들고 **"In particular read the excellent OOPSLA
    paper"**라고 적는다.[^fowler2007-mocks-arent-stubs] **2차 경유다.** 이름과 이 글이 옮긴
    문면 밖으로 나가지 않는다.
  - **그 표어를 자기 지침으로 채택한 소스가 이 KB에 있다** —
    [무엇을 목으로 대체할 것인가](what-to-replace-with-mocks.md)의 소스가 "소유한 타입만
    목하라"를 Freeman & Pryce에게 귀속하며 그들의 2009년 책 69쪽을 지목하고,
    그 분석에 전적으로 동의한다고 적는다. **여전히 원전 자체는 이 KB에 없다** — 그쪽
    페이지도 2차 경유 딱지를 달고 있다.
- **"내가 판정할 사람이 아니다" 류의 문장도 이 글에 없다.** `right person`이라는 표현은
  이메일 테스트 예시(`sent to the right person`)에서만 쓰인다. 저자의 유보를 인용할 때는 위
  [이 소스의 지위와 저자의 유보](#이-소스의-지위와-저자의-유보)에 옮긴 실제 문면을 쓴다.
- **수치가 없다.** 측정도 표본도 없으므로 이 소스에 기대어 어떤 비율이나 효과 크기도 적을 수
  없다. 양적으로 보이는 유일한 표현(`no more than half a dozen`)은 어림 규칙이고 근거가
  붙어 있지 않다.
- **다섯 분류를 이 글의 창안으로 적으면 오귀속이다.** 위 [대역 다섯의
  정의](#대역-다섯의-정의)가 정본이고, 이 글에 귀속되는 것은 두 구분의 분리와
  클래시컬·모키스트라는 이름뿐이다.

## 이 소스의 사각

- **측정이 없다.** 어느 스타일이 결함을 더 잡는지, 어느 쪽 테스트가 실제로 더 자주 깨지는지에
  대한 수치가 이 글에 하나도 없다. 다섯 축의 서술이 전부 경험과 전언이다.
- **저자가 한쪽을 실무로 써 본 적이 없다.** 본인이 그것을 밝힌다(`anything more than toys`).
  모키스트 쪽 서술은 실천자들과의 대화를 옮긴 것이다.
- **반대 진영의 문헌을 논거로 옮기지 않는다.** Freeman & Pryce를 읽으라고 가리킬 뿐, 그쪽
  논거를 이 글 안에서 다루지 않는다. **이 글만 읽고 논쟁의 판정으로 삼을 수 없다.**
- **구분 자체를 거부하는 쪽이 있다는 사실만 적히고 그 논거는 적히지 않는다.** 위
  [클래시컬과 모키스트](#클래시컬과-모키스트)의 마지막 인용이 그 자리다.
- **저자의 개정 기록이 2007-01-02에서 멈춰 있다.** 그 뒤 20년 가까이 나온 실증도, 도구의
  변화도 이 문면에 반영돼 있지 않다.
- **언어 모델 시대의 재검이 없다.** 생성된 테스트가 대역을 어떻게 쓰는지, 스타일 선택이 생성
  도구 아래에서 무엇을 바꾸는지는 이 글의 주제가 아니다.

## 이어지는 페이지

- [가짜와 목](../concepts/fakes-versus-mocks.md) — 같은 어휘를 쓰는 다른 소스가 **입장을**
  적은 자리. 그쪽은 한 책이 몽키패치 대신 가짜를 고른 이유를 소유하고, 이 페이지는 그 선택이
  놓인 어휘와 스타일의 지형을 소유한다. **그 페이지가 자기 정의를 "짧고 다소 단순하다"고
  밝히며 "길고 정확한 답"으로 이 글을 지목한다** — 이 페이지가 그 지목의 대상이다
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) —
  같은 갈림을 대규모 조직의 선호 순서로 답한 자리. 그쪽이 실물 우선을 조문으로 세우고 자기
  방식을 클래시컬로 이름 붙이는데, **그 이름이 여기서 지어진 이름이다.** 그쪽은 모키스트를
  "틀렸다"가 아니라 "규모에서 어렵다"로 강등하고, 이 페이지는 그 강등이 어느 축의 논거를
  고른 것인지를 보여 준다
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — **이 글이
  유보한 자리에 판정을 놓은 소스.** 그쪽은 두 학파 가운데 하나를 고르는 대신 **응용 경계를
  넘고 외부에서 관찰되는 통신만 목으로 검사한다**는 선을 긋고, 그 선으로 두 학파를 **둘 다**
  비판한다 — 런던 학파는 내부와 외부 통신을 구분하지 않아서, 고전 학파는 공유 의존이라는
  기준이 목으로 바꾸면 안 되는 것까지 쓸어 담아서다. 위 [두 스타일이 갈리는 다섯
  축](#두-스타일이-갈리는-다섯-축) 가운데 **구현에 대한 결합** 축만 골라 무게를 실은
  것으로 읽힌다
- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) —
  같은 소스가 그 판정의 잣대를 세운 자리. 위 [구현에 대한 결합](#구현에-대한-결합)에서 이
  글이 "리팩터링을 방해한다"로 적은 것에 이름(리팩터링 내성)과 협상 불가라는 지위를 준다.
  **이 글이 다섯 축을 나란히 놓고 판정을 유보한 것과, 그쪽이 한 축을 이진 스위치로 놓고
  나머지를 그 아래 두는 것이 두 소스의 형식 차이다**
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — 대역을
  실제로 꽂아 넣는 장치. 이 페이지의 두 스타일 모두 협력자를 바꿔 끼울 수 있어야 성립하고,
  그 자리를 만드는 기법이 거기 있다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 작은 테스트를
  성립시키는 대역 이야기가 거기 걸려 있다
- **아직 답이 없는 물음 하나** — 무엇을 목으로 만들 것인가에 대해 이 글이 가리키기만 한
  Freeman & Pryce 쪽 계보는 무엇을 주장하며, 그 주장은 이 페이지의 다섯 축 가운데 어디에
  서는가. **이 KB는 그 원전을 아직 갖고 있지 않다** — 그것을 채택한다고 적은 소스만 있다.

[^fowler2007-mocks-arent-stubs]: Fowler, "Mocks Aren't Stubs", martinfowler.com,
    2026-08-20 확보본. **절 번호가 없어 locator는 원문 §제목(영문 표기 그대로)이다** —
    §"Regular Tests" · §"Tests with Mock Objects" · §"Using EasyMock" · §"The Difference
    Between Mocks and Stubs" · §"Classical and Mockist Testing" · §"Choosing Between the
    Differences" · §"Driving TDD" · §"Fixture Setup" · §"Test Isolation" · §"Coupling Tests
    to Implementations" · §"Design Style" · §"So should I be a classicist or a mockist?" ·
    §"Final Thoughts" · §"Further Reading" · 말미 「Significant Revisions」. 직인용은 확보본
    문면 그대로다. 자바 예제 코드는 2007년 도구 표기라 페이지로 옮기지 않았고, 개념 설명에
    필요한 조각만 인라인 표기로 남겼다. 근거 등급·귀속 대조표·인용 규약은
    [소스 메타](../sources/fowler2007-mocks-arent-stubs.md)가 정본이다.

---
type: concept
title: 특성화 테스트
description: 테스트가 없는 코드를 바꿀 때 기대값을 어디서 길어 오는가 — 레거시 코드를 "테스트 없는 코드"로 다시 정의하고 현재 동작을 그대로 적어 두는 테스트에 이름과 절차를 준 실무 규범, 저자 자신이 그 테스트에 도덕적 권위가 없다고 규정한 자리, 보존 오라클로는 유효하고 수용 오라클로는 반패턴이 되는 경계, 그리고 이 책의 핵심 전제를 직접 잰 통제실험이 음성이었다는 사실
generated: { by: "claude-opus-5", at: "2026-08-21T06:00:00Z" }
sources:
  - { id: feathers2004, resource: /it/sources/feathers2004.md }
---

# 특성화 테스트

- [이 페이지가 답하는 질문](#이-페이지가-답하는-질문)
- [근거의 격 — 실무 규범이지 실증이 아니다](#근거의-격--실무-규범이지-실증이-아니다)
- [레거시 코드의 정의 — 테스트가 없는 코드](#레거시-코드의-정의--테스트가-없는-코드)
- [보존이 문제다](#보존이-문제다)
- [Cover and Modify — 테스트를 덮개로 쓴다](#cover-and-modify--테스트를-덮개로-쓴다)
- [특성화 테스트의 정의와 절차](#특성화-테스트의-정의와-절차)
- [이 테스트에는 도덕적 권위가 없다](#이-테스트에는-도덕적-권위가-없다)
- [용도 한정 — 보존 오라클이지 수용 오라클이 아니다](#용도-한정--보존-오라클이지-수용-오라클이-아니다)
- [핵심 전제의 통제실험은 음성이다](#핵심-전제의-통제실험은-음성이다)
- [이 이름은 학술 용어가 아니다](#이-이름은-학술-용어가-아니다)
- [없던 잠금을 제조하지 않는다](#없던-잠금을-제조하지-않는다)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스트도 명세도 없는 코드를 바꿔야 할 때, 기대값을 어디서 길어 오고
그렇게 만든 테스트는 무엇에는 쓸 수 있고 무엇에는 쓸 수 없는가.**

## 이 페이지가 답하는 질문

[테스트 오라클](../concepts/test-oracle.md)의 네 출처 분류에서 이 페이지가 앉는 자리는
**파생 오라클(derived test oracle)**, 그중에서도 §5.3의 "이전 판본을 오라클로 쓴다"가
실무 절차로 내려온 모습이다. 형제 페이지
[현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md)이 **그 퇴화가
무엇을 낳는지의 실증**을 담는다면, 이 페이지는 **그 절차를 이름 붙여 처방한 원전과 그
처방의 경계**를 담는다. 두 페이지는 같은 대상을 다른 격의 근거로 본다.

## 근거의 격 — 실무 규범이지 실증이 아니다

**이 소스의 근거 등급은 `practitioner-norm`이다.** 책에는 실험도 표본도 측정도 없고,
이 페이지는 그로부터 **정의·절차·저자의 규범 판단**만 가져온다. 어떤 수치 주장도 이
책에 기대지 않는다.

- **저자 자신이 지위를 밝힌다** — 기법은 여러 해에 걸친 동료·고객과의 작업에서 발견하고
  배운 것이다 (Preface).[^feathers2004]

  > The techniques I describe are ones that I've discovered and learned with coworkers and
  > clients over the course of years working with clients to try to establish control over
  > unruly code bases.

- **예제조차 실물이 아니라고 적는다** (Preface).[^feathers2004]

  > The examples that I use in the book are fabricated because I work under nondisclosure
  > agreements with clients. […] I won't say that the examples are always representative.

  대표성을 주장하지 않는 지어낸 예제 위에 선 처방이라는 것이 저자의 자기 규정이다.
- **책이 스스로 규정하는 주제도 "테스팅"이 아니다** (Preface).[^feathers2004]

  > I've been talking about tests quite a bit so far, but this book is not about testing.
  > This book is about being able to confidently make changes in any code base.

  이 페이지가 이 책에서 오라클 이론을 구하지 않고 **변경 절차**만 구하는 이유가 이
  문장이다.

## 레거시 코드의 정의 — 테스트가 없는 코드

- **저자는 레거시 코드(legacy code)의 통용되던 뜻을 버리고 다시 정의한다**
  (Preface).[^feathers2004]

  > To me, legacy code is simply code without tests.

  같은 절이 앞서 두 통용 정의를 적어 둔다: 엄밀한 뜻으로는 **남에게서 물려받은 코드**
  (*Legacy code is somebody else's code*)이고, 업계 속어로는 **이해하지 못한 채 바꾸기
  어려운 코드**다 (Preface).[^feathers2004] 저자는 둘 다 버리고 **테스트의 유무**를
  기준으로 삼는다 — 코드가 어디서 왔는지와 무관한 정의라는 것을 그 자리에서 밝힌다.
- **그 정의를 떠받치는 문장** (Preface).[^feathers2004]

  > Code without tests is bad code. It doesn't matter how well written it is; it doesn't
  > matter how pretty or object-oriented or well-encapsulated it is. With tests, we can
  > change the behavior of our code quickly and verifiably. Without them, we really don't
  > know if our code is getting better or worse.

- **정의의 값어치를 저자는 "해법을 가리킨다"로 둔다** — 깨끗한 코드로는 충분하지 않고,
  그만큼 명료한 코드를 가진 팀은 드물며, 그런 팀조차 받쳐 주는 테스트가 없으면 변경이
  더 느려 보였다고 적은 뒤 이렇게 맺는다: **좋은 실무 정의이고 해법을 가리킨다**
  (*It is a good working definition, and it points to a solution*)
  (Preface).[^feathers2004] **정의가 참이라는 주장이 아니라 쓸모 있다는 주장이다.**

## 보존이 문제다

- **바꾸는 양보다 지켜야 하는 양이 크다는 것이 1장의 문제 규정이다** (1장 §"Putting It
  All Together", p.7 강조 상자).[^feathers2004]

  > Preserving existing behavior is one of the largest challenges in software development.
  > Even when we are changing primary features, we often have very large areas of behavior
  > that we have to preserve.

- **왜 동작이 그렇게 중요한지도 같은 장이 적는다** (1장 §"Adding Features and Fixing
  Bugs", p.4 강조 상자).[^feathers2004]

  > Behavior is the most important thing about software. It is what users depend on.

- **그래서 위험을 줄이려면 세 가지를 물어야 한다** (1장 §"Risky Change",
  p.8).[^feathers2004] ⑴ 어떤 변경을 해야 하는가, ⑵ 그것을 옳게 했음을 어떻게 알
  것인가, ⑶ 아무것도 망가뜨리지 않았음을 어떻게 알 것인가. **셋째 물음이 이 페이지가
  다루는 자리이고, 특성화 테스트는 그 물음에 대한 저자의 답이다.**
- **다만 큰 어려움은 보존해야 할 양이 아니라 무지에 있다고 적는다** — 정말 큰 문제는
  변경할 때 그 동작 중 **얼마가 위험에 놓이는지를 모른다**는 것이고, 안다면 거기에만
  집중하면 된다. 안전하게 바꾸기 위해 필요한 핵심은 **이해**다 (1장 §"Putting It All
  Together", p.7).[^feathers2004]

## Cover and Modify — 테스트를 덮개로 쓴다

- **2장은 변경 방식을 둘로 가른다** — Edit and Pray와 Cover and Modify다. 앞의 것이
  업계 표준이라고 저자는 적는다 (2장 머리, p.9).[^feathers2004] Edit and Pray는 계획하고
  이해하고 고친 뒤 **망가진 데가 없기를 바라며 여기저기 찔러 보는** 방식이고, 저자는
  그것이 겉보기에 "주의 깊게 일하기"처럼 보이지만 **안전은 주의만의 함수가 아니라고**
  적는다 — 버터칼로 집도하는 외과의를 주의 깊다는 이유로 고르지는 않는다 (2장,
  p.9).[^feathers2004]
- **Cover and Modify의 덮개가 테스트다** (2장, p.9).[^feathers2004]

  > Covering software means covering it with tests. When we have a good set of tests around
  > a piece of code, we can make changes and find out very quickly whether the effects were
  > good or bad.

- **이때 테스트의 용법이 바뀐다** — 정확성을 보이려는 테스팅(*testing to attempt to show
  correctness*)이 아니라 **변경을 검출하려는 테스팅**(*testing to detect change*)이고,
  전통적인 이름으로는 회귀 테스팅(regression testing)이다 (2장, p.10).[^feathers2004]
  이 한 줄이 이 책을 [테스트 오라클](../concepts/test-oracle.md) §5.3의 갈래에
  앉힌다 — **오라클은 이전 판본이다.**
- **비유는 바이스다** (2장 §"Software Vise" 상자, p.10).[^feathers2004]

  > When we have tests that detect change, it is like having a vise around our code. The
  > behavior of the code is fixed in place. When we make changes, we can know that we are
  > changing only one piece of behavior at a time.

- **그런데 그 덮개를 씌우는 일 자체가 순환에 걸린다** (2장 §"The Legacy Code Dilemma"
  상자, p.16).[^feathers2004]

  > When we change code, we should have tests in place. To put tests in place, we often have
  > to change code.

  이 딜레마를 푸는 것이 이 책 나머지의 이음매(seam)와 의존 끊기 카탈로그이며, 그
  기법들은 이 페이지의 질문 밖이다.
- **레거시 코드 변경 알고리즘** (2장 §"The Legacy Code Change Algorithm",
  p.18).[^feathers2004] ⑴ 변경 지점을 식별한다, ⑵ 테스트 지점을 찾는다, ⑶ 의존을
  끊는다, ⑷ 테스트를 쓴다, ⑸ 변경하고 리팩터링(refactoring)한다. **테스트 쓰기가 변경보다 앞에
  있다는 순서가 이 절차의 전부다.**

## 특성화 테스트의 정의와 절차

- **명세를 파러 가지 말라는 것이 13장의 출발점이다** — 요구사항 문서와 프로젝트 메모를
  발굴해 그것에 근거해 테스트를 쓰는 접근은 좋은 접근이 아니라고 적는다. 이유는 한
  문장이다 (13장 §"Characterization Tests", p.186).[^feathers2004]

  > In nearly every legacy system, what the system does is more important than what it is
  > supposed to do.

- **정의** (13장 §"Characterization Tests", p.186).[^feathers2004]

  > The tests that we need when we want to preserve behavior are what I call characterization
  > tests. A characterization test is a test that characterizes the actual behavior of a
  > piece of code. There's no "Well, it should do this" or "I think it does that." The tests
  > document the actual current behavior of the system.

  **`what I call` — 저자가 자기 명명임을 문면에 적는다.** 이 사실이 아래
  [이 이름은 학술 용어가 아니다](#이-이름은-학술-용어가-아니다)의 근거다.
- **용어집의 정의는 더 짧고 두 일을 함께 적는다** (용어집,
  p.421).[^feathers2004]

  > characterization test  A test written to document the current behavior of a piece of
  > software and preserve it as you change its code.

  **기록(document)과 보존(preserve)** 둘이고, "옳음을 검사한다"는 셋째 일은 여기 없다.
- **다섯 단계 절차** (13장, p.186).[^feathers2004] ⑴ 코드 조각을 테스트 하네스(test
  harness)에서 실행한다, ⑵ **실패할 것을 아는 단정(assertion)을 쓴다**, ⑶ 그 실패가
  동작이 무엇인지 말하게 한다, ⑷ 코드가 내놓는 동작을 기대값으로 삼도록 테스트를
  고친다, ⑸ 반복한다.
- 절차의 핵심은 둘째 단계다 — **일부러 틀린 단정을 써서 실패 메시지가 현재 동작을
  뱉게 만든다.** 책이 드는 예에서 `PageGenerator`가 `"fred"`를 만들 리 없다고 보고
  다음을 돌린다 (13장, p.186).[^feathers2004]

  ```java
  void testGenerator() {
      PageGenerator generator = new PageGenerator();
      assertEquals("fred", generator.generate());
  }
  ```

  실패 메시지가 `expected:<fred> but was:<>`를 내놓으면 기대값을 `""`로 바꿔
  통과시킨다 (`assertEquals("", generator.generate())`). 저자는 그 결과를 **테스트가
  아니라 문서**로 규정한다 — 갓 만든 `PageGenerator`에게 곧바로 `generate`를 시키면 빈
  문자열을 낸다는 사실을 적어 둔 것이다 (13장, p.187).[^feathers2004]
- **어디까지 쓰는가에 대한 정지 조건** — 가능한 테스트 수는 무한하므로 정지 조건이
  필요하다. 저자의 답은 두 단계다: 먼저 **코드의 동작에 대한 호기심이 채워질 때까지**
  쓰고, 그다음 **하려는 변경이 일으킬 수 있는 문제를 지금 있는 테스트가 감지할지**를
  따져 아니면 확신이 설 때까지 더 쓴다. 확신이 서지 않으면 **다른 방식으로 바꾸는 편이
  안전하다**고 적는다 (13장, pp.188–189).[^feathers2004]
- **리팩터링을 겨눌 때 확인할 것은 둘이다** (13장 §"Targeted Testing" 상자,
  p.194).[^feathers2004]

  > When we refactor, we generally have to check for two things: Does the behavior exist
  > after the refactoring, and is it connected correctly?

  같은 상자가 특성화 테스트의 실제 모습을 규정한다 — 대개 **"맑은 날(sunny day)"
  테스트**여서 특별한 조건을 많이 검사하지 않고 **특정 동작이 존재한다는 것만 확인**하며,
  그 존재로부터 옮기고 뽑아낸 리팩터링이 동작을 보존했다고 **추론**한다 (13장,
  p.194).[^feathers2004] **검증이 아니라 추론이라고 저자가 적는다.**

## 이 테스트에는 도덕적 권위가 없다

**이 절이 이 페이지에서 가장 인용 가치가 큰 자리다** — 저자 자신이 이 테스트의 오라클
지위를 스스로 낮춘다.

- **저자가 먼저 이의를 제기한다** (13장, pp.187–188).[^feathers2004]

  > There is something fundamentally weird about doing this if you are used to thinking about
  > these tests as, well, tests. If we are just putting the values that the software produces
  > into the tests, are our tests really testing anything at all? What if the software has a
  > bug? The expected values that we're putting in our tests could just simply be wrong.

- **그리고 그 이의를 반박하는 대신 테스트의 지위를 바꾸는 것으로 답한다** (13장,
  p.188).[^feathers2004]

  > They aren't really tests written as a gold standard that the software must live up to.
  > We aren't trying to find bugs right now. We are trying to put in a mechanism to find bugs
  > later, bugs that show up as differences from the system's current behavior. […] They
  > don't have any moral authority; they just sit there documenting what pieces of the system
  > really do.

  **"도덕적 권위가 없다"(they don't have any moral authority)** — 이 다섯 낱말이 이
  페이지 전체의 축이다. 이 테스트가 통과한다는 것은 **지금 동작이 옳다는 뜻이 아니라
  지금 동작이 그대로라는 뜻**이다.
- **버그를 만나면 어떻게 하는가도 절차에 들어 있다** (13장 상자,
  p.188).[^feathers2004]

  > Characterization tests record the actual behavior of a piece of code. If we find
  > something unexpected when we write them, it pays to get some clarification. It could be
  > a bug. That doesn't mean that we don't include the test in our test suite; instead, we
  > should mark it as suspicious and find out what the effect would be of fixing it.

  **버그로 보이는 동작도 일단 스위트에 넣되 "의심스러움"으로 표시한다** — 오라클이
  아니라 기록이기 때문에 가능한 처방이다.
- **배포 여부가 갈림길이라는 것을 책이 명시한다** (13장 §"When You Find Bugs" 상자,
  p.190).[^feathers2004]

  > If the system has never been deployed, the answer is simple: You should fix the bug. If
  > the system has been deployed, you need to examine the possibility that someone is
  > depending on that behavior, even though you see it as a bug.

  **배포된 적 없는 시스템에서는 고치라는 것이 책의 답이다.** 저자의 기본 성향도
  "발견 즉시 수정"이라고 같은 상자가 적는다 (*My bias is toward fixing bugs as soon as
  they are found*).[^feathers2004] 아래
  [없던 잠금을 제조하지 않는다](#없던-잠금을-제조하지-않는다)가 이 조건절 위에 선다.

## 용도 한정 — 보존 오라클이지 수용 오라클이 아니다

**이 절이 이 소스를 인용할 때 넘지 말아야 할 선이다.** 특성화 테스트는 **현재 동작을
기대값으로 고정하는 절차**이고, 그것은 **어디에 쓰느냐에 따라 옳기도 하고 반패턴이기도
하다.**

**아래 두 이름 — 보존 오라클(preservation oracle)과 수용 오라클(acceptance oracle) —
은 책의 말이 아니라 이 KB가 용도를 가르려고 붙인 것이다.** 책은 이 구분을 이름으로
세우지 않고 "보존한다"는 동사로만 말한다. 이름의 출처는 이 소스에 대한 적합성
심사(2026-08-20)이고, 원문에 귀속시키지 않는다.

지지하는 용도 — **보존 오라클**:

- **변경 안전망.** 리팩터링·최적화·이관처럼 **동작을 바꾸지 않기로 한 변경**에서, 바뀐
  것이 있으면 알려 주는 장치. 책이 겨냥한 것이 정확히 이것이다 — 자동 테스트는 이루려는
  목표를 명세하거나 **이미 있는 동작을 보존하려는 것**이어야 하고, 개발의 자연스러운
  흐름에서 **명세하는 테스트가 보존하는 테스트가 된다**(*tests that specify become tests
  that preserve*) (13장 머리, p.185).[^feathers2004]
- **이해의 기록.** 코드를 읽고 머릿속으로 "컴퓨터 놀이"를 하는 것 말고는 시스템이 실제로
  무엇을 하는지 알 길이 없고, 그 일은 지루하고 낭비적이므로 테스트로 적어 둔다 (13장,
  p.188).[^feathers2004]

지지하지 않는 용도 — **수용 오라클**:

- **새 기능이 옳은지의 판정에 쓰지 않는다.** 기대값이 대상에서 나왔으므로 **대상이 틀려
  있으면 기대값도 틀린 채 태어난다.** 이것은 이 페이지의 추론이 아니라 저자가 스스로 던진
  이의이고(위 §"이 테스트에는 도덕적 권위가 없다"), 저자의 답은 **"이 테스트는 그 일을
  하지 않는다"**였지 "그 일도 할 수 있다"가 아니었다.
- **버그를 사양으로 굳히는 데 쓰지 않는다.** 같은 절차가 버그도 그대로 기록하므로
  "의심스러움" 표시와 에스컬레이션이 절차에 함께 들어 있다 (13장, pp.188·190).
- **이 경계가 왜 중요한가** — 현재 동작(버그 포함)에 정렬해 기대값을 만드는 것은
  [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md)이 세운
  실패 기전과 **같은 동작**이다. 그 페이지가 인용하는 대로, 명세가 없으면 생성된 단정은
  의도가 아니라 관측을 적고, 대상이 이미 틀려 있으면 단정도 틀린 채 태어난다. **사람이
  절차를 밟아 쓰든 기계가 뽑아내든 기대값의 출처가 같으면 같은 한계에 걸린다.**
- **극한에는 이름이 붙어 있다** —
  [변경 감지 테스트(change-detector test)](../concepts/current-behaviour-as-oracle.md#이름이-붙은-자리--변경-감지-테스트)다.
  대상 코드의 정보를 그대로 옮겨 놓아 **생산 코드가 바뀌면 무조건 깨지고 옳은 동작은
  검증하지 않는** 테스트이며, 그 실무 규범은 "다시 쓰거나 지우라"고 처방한다. 특성화
  테스트가 이 극한과 갈리는 지점은 **의도된 유효 기간**이다: 특성화 테스트는 변경을
  끝낼 때까지 쓰는 발판이고, 그 자리에 영구히 남아 되비추기만 하면 변경 감지 테스트와
  구별되지 않는다. #hypothesis 이 구별선은 두 소스 어느 쪽도 명시하지 않았고, 두 문면을
  같은 자리에 놓았을 때 이 KB가 읽어 낸 것이다.

## 핵심 전제의 통제실험은 음성이다

**이 책의 전제는 "테스트가 있으면 변경(특히 리팩터링)이 안전하고 빨라진다"이다.** 그
전제를 사람 피험자에게 직접 건 통제실험이 하나 있고, **결과는 그 전제를 확인해 주지
않았다.**

- **그 실험의 자리** —
  [현재 동작을 오라클로 쓴다는 것 §안전망 명제의 통제실험](../concepts/current-behaviour-as-oracle.md#안전망-명제의-통제실험--리팩터링에-테스트가-있을-때)이
  정본이다. 42명을 단위 테스트가 있는 쪽과 없는 쪽으로 갈라 리팩터링 과제 7개를 시켰고,
  시간에서도 결과 코드 품질에서도 테스트 쪽의 이득이 나타나지 않았다. 유의했던 유일한
  시간 결과는 **테스트를 가진 쪽이 더 오래 걸린 것**이었다.
- **그 논문이 이론으로 지목한 대상이 이 책이다.** 논문 §V-B는 *"While theory explains how
  unit testing makes refactoring easier, e.g., Feathers [25], we could not observe this in
  our experiment"*라고 적고, 참고문헌 [25]가 이 책이다. **이 페이지가 그 논문과 이어져야
  하는 이유가 이 문장이다.**
- **그러나 그 논문의 한정을 넘겨 쓰지 않는다.** 초록은 단정적이지만 본문 §V-A는 **두
  귀무가설 어느 쪽도 기각도 채택도 못 한다**고 적는다. 그러므로 이것은 **"테스트가 돕지
  않는다는 증명"이 아니라 "돕는다는 증거를 관측하지 못했다"**이다. 저자가 함께 적은
  한계(대상 프로그램이 작다, 새 테스트를 쓰라고 요구하지 않았다, 표본이 작다)도 같은
  무게로 읽는다. 한정의 정본은 그쪽 페이지이고, 이 페이지는 그 문면을 넘겨 인용하지
  않는다.
- **그래서 이 페이지가 말하는 것은 이것이다** — 이 책의 처방을 쓸 때 **"실증이 뒷받침한다"고
  말할 수 없다.** 근거는 실무 규범이고, 그 전제를 직접 잰 유일한 통제실험은 이득을
  관측하지 못했다. 처방 자체가 반증된 것은 아니지만 **입증되지도 않았다는 것이 지금
  KB가 아는 전부다.**

## 이 이름은 학술 용어가 아니다

- **책 자신이 저자의 명명임을 적는다** — *"what I call characterization tests"* (13장,
  p.186).[^feathers2004] 학계의 합의된 명칭을 가져다 쓴 것이 아니라 저자가 붙인
  이름이다.
- **이 축의 서베이 정본에 그 낱말이 없다.** 1978–2012년 문헌 694편을 오라클 관점에서
  분류한 [테스트 오라클](../concepts/test-oracle.md)의 원전 서베이 전문에서
  `characteriz`로 시작하는 문자열은 **0회** 나타난다. **이것은 이 KB가 스냅샷 원문의
  텍스트를 추출해 전수 검색한 관측이지 그 논문의 진술이 아니다.** 같은 개념을 그 문헌이
  다루지 않는다는 뜻이 아니라 — §5.3의 회귀 테스트 갈래가 같은 발상을 담는다 — **이
  이름으로는 다루지 않는다**는 뜻이다.
- #hypothesis **그러므로 "characterization test"는 실무 어휘이지 SE 학술 용어가 아니다.**
  서베이 한 편의 부재는 문헌 전체의 부재를 증명하지 않으므로 이 판정에는 표식을 단다.
  **실무적 귀결은 확실하다** — 이 낱말로 학술 근거를 찾으면 나오지 않고, 대응하는 학술
  어휘는 **회귀 테스트**와 **파생 오라클**이다. 조항이나 리뷰 기준에 이 이름을 쓸 때는
  그것이 실무 규범의 이름이라는 것을 함께 적는다.

## 없던 잠금을 제조하지 않는다

**이 절은 이 KB의 재검증 판정이다 — 책의 주장이 아니다.**

- **널리 인용되는 논거 하나가 이 처방을 지지하는 데 자주 동원된다** — "사용자가 충분히
  많으면 API의 관측 가능한 모든 동작이 누군가에게 의존된다"는 명제(Hyrum's Law)다. **이
  책은 그 명제를 말하지 않는다.** 2004년 책이고 그 명제는 2017년 이후의 것이며, 그
  원전은 이 KB에 없으므로 이 페이지는 문면을 인용하지 않는다.
- **그 명제에는 조건절이 있다 — "사용자가 충분히 많을 때"다.** 조건절을 떼고 쓰면 명제가
  아니라 구호가 된다. #hypothesis **사용자가 한 명이거나 아직 배포되지 않은 코드에
  이것을 걸면, 지켜야 할 계약을 확인하는 것이 아니라 없던 잠금을 제조하는 것이 된다** —
  현재 동작을 테스트로 고정하는 순간 그 동작이 사양이 되고, 아무도 의존하지 않던 우연한
  동작까지 바꿀 수 없게 된다.
- **이 판정은 책과 어긋나지 않는다.** 위에서 본 대로 책 자신이 배포 여부로 갈림길을
  둔다 — 배포된 적 없는 시스템이면 **버그는 그냥 고치라**는 것이 답이고, 의존 가능성을
  따지라는 것은 **배포된 시스템**에 걸린 조건이다 (13장, p.190).[^feathers2004] 조건절을
  지운 채 "현재 동작은 다 지켜야 한다"로 읽는 것은 책보다 강한 주장이다.

## LLM 시대의 지위

**이 절은 이 KB의 재프레임이지 책의 주장이 아니다.**

- #hypothesis **모델이 만든 코드는 의도 이력이 없는 신생 레거시다.** 책의 정의를 그대로
  적용하면 — *legacy code is simply code without tests* — 갓 생성된 코드도 테스트가 없는
  한 레거시다. 여기에 하나가 더 붙는다: **왜 이렇게 되어 있는지를 아는 사람이 처음부터
  없다.** 사람이 쓴 레거시는 의도가 사람에게서 조직으로 흩어져 사라진 것이지만, 생성된
  코드는 **그 의도가 애초에 어디에도 기록된 적이 없다.**
- #hypothesis **그래서 이 책의 처방이 오히려 더 위험해지는 자리가 생긴다.** 특성화
  테스트는 **지켜야 할 이유가 있는 동작**이 이미 있다는 전제 위에 선다(배포되어 누군가
  쓰고 있다는 전제). 방금 생성된 코드에는 그 전제가 없다 — 그 동작은 역사가 아니라
  **모델의 한 번의 표본추출**이다. 그것을 특성화해 고정하면 **검증되지 않은 출력을
  사양으로 승격**시키는 것이 된다. 위
  [용도 한정](#용도-한정--보존-오라클이지-수용-오라클이-아니다)의 경계가 이 세대에서
  더 날카로워지는 이유다.
- **그러므로 이 책을 LLM 코드에 적용할 때의 판정 질문은 하나다** — *지금 이 동작은
  지켜야 할 계약인가, 아니면 아직 아무도 판정하지 않은 출력인가.* 앞이면 특성화 테스트가
  맞고, 뒤면 필요한 것은 특성화가 아니라 **명세에서 온 오라클**이다
  ([테스트 오라클](../concepts/test-oracle.md) §4).
- **이 재프레임이 반입 이유이지 고전 그대로의 반입이 아니다.** 이 책이 2004년에 답한
  질문("남이 남긴 코드를 어떻게 안전하게 바꾸는가")과 지금 이 KB가 묻는 질문("모델이
  방금 만든 코드를 무엇에 비추어 판정하는가")은 같지 않다. **겹치는 것은 절차이고
  갈리는 것은 전제다.**

## 이어지는 페이지

- [테스트 오라클](../concepts/test-oracle.md) — 이 축의 개념 정본. 이 페이지의 절차는
  §5.3 "이전 판본을 오라클로 쓴다"의 실무판이고, 이 페이지가 배격하는 용도는 §4 명세
  오라클이 맡아야 하는 자리다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 같은
  절차의 실증 층. 이 페이지가 처방과 그 경계를 담는다면 그쪽은 **그 처방의 전제를 잰
  통제실험 둘과 실무 규범 하나**를 담는다. 이 페이지의 caveat가 기대는 반증이 전부
  그쪽에 있다
- [리팩터링을 가로막는 것들](../concepts/obstacles-to-refactoring.md) — 리팩터링 쪽에서
  같은 딜레마를 본 자리. 테스트 없는 레거시에 지름길이 없다고 적고 처방으로 이 책을
  지목한다
- [자기 테스트 코드](../concepts/self-testing-code.md) — 기대값을 사람이 **명세 쪽에서**
  짓는 자리. 이 페이지의 반대 극이다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  통과가 무엇을 증명하지 않는가의 상한. 도덕적 권위가 없는 테스트는 그 상한 아래에서도
  더 적게 증명한다
- [일관성 오라클 휴리스틱](../concepts/consistency-oracle-heuristics.md) — 명세가 없을 때
  기대를 무엇에 비추는가의 실무 카탈로그. "이전 판본과의 일관성"이 그 목록의 한 항목이고,
  이 페이지의 절차가 그 항목을 절차로 편 것이다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  같은 출처에서 기대값을 길어 오는 일을 기계가 대신할 때의 실측. 위 "LLM 시대의 지위"가
  던지는 판정 질문이 실제 수치로 어디에 걸리는지를 그쪽이 잰다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 이 축의 허브

[^feathers2004]: Feathers 2004, *Working Effectively with Legacy Code*, Prentice Hall PTR.
    **확보본은 EPUB이라 조판 쪽이 없고, 원문에 인쇄판 쪽 앵커(`page_NNN`)가 남아 있어
    locator는 장·절 제목과 인쇄판 쪽으로 적었다.** 이 페이지는 Preface, 1장 Changing
    Software(pp.3–8), 2장 Working with Feedback(pp.9–20), 13장 I Need to Make a Change,
    but I Don't Know What Tests to Write(pp.185–195), 용어집(p.421)을 담았다. 2장의 단위
    테스트 정의와 크기 규약(pp.12–14), 3장 Sensing and Separation·4장 The Seam Model의
    이음매 모델, 25장 의존 끊기 카탈로그는 이 페이지의 질문 밖이라 옮기지 않았다. 13장
    §"Targeted Testing"의 `FuelShare` 예제(pp.190–195)는 형 변환 절단을 드러내는 입력
    고르기를 다루는 대목이라 결론 상자만 옮기고 코드는 옮기지 않았다 — 이 페이지의 코드
    펜스는 §"Characterization Tests"의 `PageGenerator` 예제(p.186) 하나이며 원문 그대로이고
    보탠 줄이 없다. 판권면은 `ISBN 0-13-117705-2`·`Copyright © 2005`·
    `First printing, September 2004`를 적는다. 근거 등급은 `practitioner-norm`이고, 이
    페이지는 이 소스에서 정의·절차·저자의 규범 판단만 인용하며 어떤 수치 주장도 여기에
    기대지 않는다.

---
type: concept
title: 오스터하우트–마틴 공개 대담
description: 이 KB의 모순 두 자리에 걸린 두 저자가 직접 맞붙은 1차 사료 — 대담의 형식과 두 사람이 먼저 합의한 판단 잣대, 메서드 길이·주석·TDD 세 쟁점에서 각자의 양보 지점과 끝내 갈린 지점, 요약 절이 조문화한 합의·불합의 목록, 오스터하우트가 자기 책의 오류를 인정한 자리, 마틴이 2판에서 균형을 잡았다고 밝힌 자리, 그리고 이 문서가 이 KB의 기존 판정에 무엇을 더하는가
generated: { by: "claude-opus-5", at: "2026-08-18T04:00:00Z" }
sources:
  - { id: ousterhout2024-aposd, resource: /it/sources/ousterhout2024-aposd.md }
  - { id: martin2008, resource: /it/sources/martin2008.md }
---

# 오스터하우트–마틴 공개 대담

- [이 문서의 지위와 형식](#이-문서의-지위와-형식)
- [먼저 합의한 것 — 판단 잣대](#먼저-합의한-것--판단-잣대)
- [쟁점 ① 메서드 길이](#첫째-쟁점--메서드-길이)
- [마틴의 양보 셋](#마틴의-양보-셋)
- [메서드 길이 요약 — 합의와 불합의의 조문](#메서드-길이-요약--합의와-불합의의-조문)
- [쟁점 ② 주석](#둘째-쟁점--주석)
- [주석 쟁점에서 마틴이 물러선 세 자리](#주석-쟁점에서-마틴이-물러선-세-자리)
- [주석 요약 — 합의를 찾지 못한 자리](#주석-요약--합의를-찾지-못한-자리)
- [쟁점 ③ 테스트 주도 개발](#셋째-쟁점--테스트-주도-개발)
- [오스터하우트의 양보](#오스터하우트의-양보)
- [맺음말 — 두 가지 일반적 오류](#맺음말--두-가지-일반적-오류)
- [판본 — Clean Code 2판이 존재한다](#판본--clean-code-2판이-존재한다)
- [이 문서가 이 KB의 판정에 더하는 것](#이-문서가-이-kb의-판정에-더하는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **두 저자가 직접 맞붙었을 때 무엇이 합의되고 무엇이 끝내 갈렸는가.**

## 이 문서의 지위와 형식

- 문서가 스스로 성격을 밝힌다 (머리말):[^ousterhout2024-aposd]

> (This document is the result of a series of discussions, some online and some in
> person, held between Robert "Uncle Bob" Martin and John Ousterhout between September
> 2024 and February 2025)

- **형식은 번갈아 가는 대담이다.** 발언자가 `**JOHN:**`(John Ousterhout)과
  `**UB:**`(Robert "Uncle Bob" Martin)로 표시되고, 주제마다 끝에 오스터하우트가 합의·
  불합의 목록을 정리하면 마틴이 그것이 공정한지 확인한다. **양보 지점이 그 요약 절에
  몰려 있다.**
- 주제는 셋 — 메서드 길이, 주석, 테스트 주도 개발.
- **시작부터 상호 존중이 기록된다.** 마틴 — **시작하기 전에, 나는 당신 책을 주의 깊게
  읽었고 아주 즐거웠으며 값진 통찰로 가득하다고 느꼈다고 말해 두겠다. TDD와 추상 우선
  점진주의처럼 당신에게 동의하지 않는 것도 있지만, 전체적으로 아주 즐거웠다**
  (§"Introductions", UB 발언).[^ousterhout2024-aposd]

## 먼저 합의한 것 — 판단 잣대

**두 사람이 잣대에서는 갈리지 않는다는 것이 이 대담의 출발점이다.** 처방이 갈리는데 잣대가
같다는 구조는 이 KB의 모순 판정을 이해하는 데 중요하다.

- 오스터하우트의 잣대 — **나에게 소프트웨어 설계의 근본 목표는 시스템을 이해하고 수정하기
  쉽게 만드는 것이다. 나는 시스템을 이해하고 수정하기 어렵게 만드는 것들을 가리키는 데
  "복잡성"이라는 용어를 쓴다** (§"Introductions", JOHN 발언).[^ousterhout2024-aposd]
  복잡성의 가장 중요한 기여 요인은 정보와 관련된다고 적는다 — 개발자가 머리에 담아야 하는
  정보의 양과, 그 정보가 얼마나 접근 가능하고 뻔한가.
- **마틴이 그 잣대에 동의한다** (§"Introductions", UB 발언):[^ousterhout2024-aposd]

> I agree with your approach. A discipline or technique should make the job of programmers
> easier. I would add that the programmer we want to help most is not the author. The
> programmer whose job we want to make easier is the programmer who must read and
> understand the code written by others (or by themself a week later).

  - 그리고 읽기 우선의 근거를 댄다 — **프로그래머는 코드를 쓰는 것보다 읽는 데 훨씬 더
    많은 시간을 쓰므로, 우리가 쉽게 만들고자 하는 활동은 읽기다** (§"Introductions",
    UB 발언).[^ousterhout2024-aposd] 이 KB의
    [클린 코드라는 말의 정의](clean-code-defined.md)가 옮긴 10대 1 비율과 같은 논거다.

## 첫째 쟁점 — 메서드 길이

- **오스터하우트가 이 KB의 `contradicts` ①을 그대로 제기한다.** 그는 *Clean Code*
  p.34의 두 규칙과 "20줄인 경우도 거의 없어야 한다", "두세네 줄", p.35의 "블록은 한 줄"을
  차례로 인용한 뒤 (§"Method Length", JOHN 발언):[^ousterhout2024-aposd]

> I couldn't find anything in *Clean Code* to suggest that a function could ever be too
> short.

  - **인용이 원문과 대조된다.** 이 KB가 보존한 martin2008 스냅샷의 p.34에
    **함수는 100줄이어서는 안 된다. 함수가 20줄인 경우도 거의 없어야 한다**가, p.35에
    **`if` 문·`else` 문·`while` 문 등의 안쪽 블록은 한 줄이어야 한다**가 그대로
    있다.[^martin2008] 이 KB의 [작은 함수](small-functions.md)가 옮긴 것과 같은 자리이고,
    같은 관찰을 [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md)이 붉은 깃발로 갖고
    있다.
- **분해 자체에는 동의한다** — **코드를 비교적 작은 단위로 나누는 것("모듈형 설계")이
  프로그래머가 한 번에 머리에 담아야 하는 정보의 양을 줄이는 가장 중요한 방법 중
  하나라는 데 동의한다** (§"Method Length", JOHN 발언).[^ousterhout2024-aposd]
- **갈리는 지점이 "너무 멀리 갈 수 있는가"다** — **소프트웨어 설계의 대부분 아이디어처럼
  분해도 너무 멀리 갈 수 있다. 메서드가 점점 작아질수록 더 나누는 데서 오는 이득은
  점점 줄어든다** (§"Method Length", JOHN 발언).[^ousterhout2024-aposd]
- **얽힘(entanglement)이라는 새 개념이 여기서 도입된다** — 이 KB에 아직 없던 것이다.
  (§"Method Length", JOHN 발언):[^ousterhout2024-aposd]

> Two methods are entangled (or "conjoined" in APOSD terminology) if, in order to
> understand how one of them works internally, you also need to read the code of the
> other. If you've ever found yourself flipping back and forth between the
> implementations of two methods as you read code, that's a red flag that the methods
> might be entangled.

  - 처방까지 붙는다 — **얽힌 메서드는 대개 모든 코드가 한 자리에 있도록 합쳐서 개선할 수
    있다** (§"Method Length", JOHN 발언).[^ousterhout2024-aposd]
  - **이것이 이 KB의 모순 ①에 더해지는 실질이다.** 기존 대질은 "쪼개면 얕아진다"였는데,
    얽힘은 **쪼개면 정보가 흩어진다**는 두 번째 기제를 댄다. 얕음은 인터페이스 쪽 손해이고
    얽힘은 독자의 작업 기억 쪽 손해다.
- 그래서 진단이 이렇게 정리된다 — **메서드 길이에 대한 *Clean Code*의 조언은 너무
  극단적이어서 프로그래머가 얕은 인터페이스와 얽힘 둘 다를 겪는 아주 작은 메서드를 만들도록
  부추긴다** (§"Method Length", JOHN 발언).[^ousterhout2024-aposd]

## 마틴의 양보 셋

**이 대담에서 가장 값진 부분이다.** 마틴이 물러선 자리가 셋이고, 셋 다 이 KB의
[작은 함수](small-functions.md)가 옮긴 주장의 범위를 좁힌다.

**① 수치는 규정이 아니라 일화였다** (§"Method Length", UB 발언):[^ousterhout2024-aposd]

> While I do strongly recommend very short functions, I don't think it's fair to say that
> the book sets arbitrary numerical limits. The 2-4 line functions that you referred to on
> page 34 were part of the _Sparkle_ applet that Kent Beck and I wrote together in 1999 as
> an exercise for learning TDD.

  - **이 KB의 반입분과 대조된다.** [작은 함수](small-functions.md)는 p.34의 그 대목을
    일화로 기록했고("저자가 대는 것도 실증이 아니라 일화다"), 마틴 본인의 해명이 그
    독법을 확인한다. **다만 p.34의 "20줄인 경우도 거의 없어야 한다"와 p.35의 "블록은 한
    줄"은 일화가 아니라 서술문이고, 마틴은 그 둘에 대해서는 해명하지 않는다.**
  - 마틴은 또 p.13의 자기 유보를 근거로 든다 — **나는 최종 권위를 주장하지 않았고 어떤
    절대적 "옳음"도 주장하지 않았다** (§"Method Length", UB 발언).[^ousterhout2024-aposd]
    이 KB가 [클린 코드라는 말의 정의](clean-code-defined.md)에 이미 옮겨 둔 그 문단이다.

**② 과잉 분해는 가능하고, 책에 그 판단 지침이 부족하다**

- 마틴이 과잉 분해의 가능성을 인정하고 예까지 든다 — `void doSomething() {doTheThing()}`
  을 **과잉 분해**로 표시한다 (§"Method Length", UB 발언).[^ousterhout2024-aposd]
- 그가 쓰는 판정 기준은 "한 가지" 규칙이다 — **한 메서드에서 다른 메서드를 *유의미하게*
  뽑아낼 수 있다면 원래 메서드는 한 가지보다 많은 일을 한 것이다. "유의미하게"란 뽑아낸
  기능에 서술적인 이름을 줄 수 있고 그것이 원래 메서드보다 적은 일을 한다는 뜻이다**
  (§"Method Length", UB 발언).[^ousterhout2024-aposd]
- **그러나 지침의 부족은 인정한다** (§"Method Length", UB 발언):[^ousterhout2024-aposd]

> You make a good point that I don't talk much, in the book, about how to make the
> judgement call. Back in 2008 my concern was breaking the habit of the very large
> functions that were common in those early days of the web. I have been more balanced in
> the 2d ed.

  - **그럼에도 기본값은 바꾸지 않는다** — **그래도 틀려야 한다면 나는 분해하는 쪽으로
    틀리겠다. … 너무 멀리 갔다고 판단되면 언제든 인라인할 수 있다** (§"Method Length",
    UB 발언).[^ousterhout2024-aposd] **모순이 해소되지 않고 남는 지점이 정확히 여기다.**

**③ 자기 예제가 읽기 어렵다는 것을 인정한다**

- `PrimeGenerator`(이 KB가 [클린 코드 비판](clean-code-criticism.md)에서 다룬 그 코드)를
  두고 (§"Method Length", UB 발언):[^ousterhout2024-aposd]

> I think you have a point. Eighteen years ago, when I was in the throes of this
> refactoring, the names and structure made perfect sense to me. They make sense to me
> now, too -- but that's because I once again understand the algorithm. When I returned to
> the algorithm for the first time a few days ago, I struggled with the names and
> structure.

- 오스터하우트의 되받음 — **코드가 나중에 돌아온 작성자에게 더 이상 말이 되지 않는다면,
  그것은 그 코드에 문제가 있다는 뜻이다** (§"Method Length",
  JOHN 발언).[^ousterhout2024-aposd] 그리고 마틴이 **정당한 지적이다(Fair enough)**로
  받되, 상대의 재작성도 자기에게는 똑같이 어려웠다고 덧붙인다 (§"Method Length",
  UB 발언).[^ousterhout2024-aposd]

## 메서드 길이 요약 — 합의와 불합의의 조문

오스터하우트가 정리하고 마틴이 **공정한 평가**라고 확인한 목록이다
(§"Method Length Summary"):[^ousterhout2024-aposd]

| | 내용 |
|---|---|
| 합의 | 모듈형 설계는 좋은 것이다 |
| 합의 | **과잉 분해가 가능하고, *Clean Code* 초판은 그것을 알아보는 지침을 별로 주지 않는다** |
| 불합의 | 얼마나 멀리 분해할 것인가 — 마틴이 훨씬 더 작은 단위를 권한다 |
| 불합의 | "한 가지" 규칙이 판단과 함께 쓰이면 적절한 분해로 이끄는가(마틴) 아니면 안전난간이 없어 과잉 분해로 가는가(오스터하우트) |
| 합의 | **`PrimeGenerator`를 메서드로 내부 분해한 것은 문제가 있다** |
| 불합의 | 얽힘의 무게 — 마틴은 분해의 이득이 얽힘의 문제를 벌충할 수 있다고 보고, 오스터하우트는 못 한다고 본다 |
| 불합의 | 클래스 안 메서드 순서가 얽힘을 벌충할 수 있는가 |

- 마틴의 확인 (§"Method Length Summary", UB 발언):[^ousterhout2024-aposd]

> I think this is a fair assessment of our agreements and disagreements. We both value
> decomposition, and we both avoid entanglement; but we disagree on the relative weighting
> of those two values.

  - **"상대적 가중치의 불일치"가 이 쟁점의 최종 진단이다.** 이 KB의 모순 ①이 무마되지
    않는 이유가 여기서 확인된다 — 잣대가 같고 값이 다른 것이 아니라, 같은 조작에 대해
    두 값의 가중치가 반대라서 처방이 반대로 나온다.

## 둘째 쟁점 — 주석

- **오스터하우트가 이 KB의 `contradicts` ②를 그대로 제기한다** — **내 의견으로는
  *Clean Code*의 주석 접근법은 문서화가 불충분한 코드를 낳고, 그것이 소프트웨어 개발
  비용을 올린다** (§"Comments", JOHN 발언).[^ousterhout2024-aposd]
- 그리고 *Clean Code* p.54의 그 문단을 인용한다 — 이 KB의
  [주석은 실패다](comments-as-failure.md)가 원전에서 직접 옮긴 것과 같은 자리다.
  **다만 표기가 세 판본에서 조금씩 다르다** — 대조표는 그 페이지의 인용 대조 절이
  정본이고, 이 문서의 인용도 거기에 더했다.
- **마틴이 그 조문의 범위를 좁힌다** (§"Comments", UB 발언):[^ousterhout2024-aposd]

> I'm not hostile to comments in general.  I _am_ very hostile to gratuitous comments.

  - 그리고 4장이 **잘 놓인 주석만큼 도움이 되는 것은 없다**는 문장으로 시작한다는 점을
    든다 (§"Comments", UB 발언).[^ousterhout2024-aposd] 이 KB의
    [주석은 실패다](comments-as-failure.md)가 "좋다고 인정되는 주석 여덟 종" 절을 함께
    옮긴 것과 같은 취지다.
- **오스터하우트가 지면 배분으로 반박한다** — 4장은 **좋은 주석에 네 쪽을 쓰고 이어서
  나쁜 주석에 열다섯 쪽을 쓴다**고 세면서, **"주석은 언제나 실패다"가 너무 귀에 감겨
  독자가 그 장에서 가장 기억하기 쉬운 한 문장이 된다**고 적는다 (§"Comments",
  JOHN 발언).[^ousterhout2024-aposd] 마틴의 답은 **좋은 주석을 쓰는 방법은 몇 안 되고
  나쁘게 쓰는 방법은 훨씬 많기 때문**이라는 것이다 (§"Comments",
  UB 발언).[^ousterhout2024-aposd]
- **이 KB에 없던 것 — 마틴이 그 태도의 역사적 동기를 밝힌다** (§"Comments",
  UB 발언):[^ousterhout2024-aposd]

> You and I likely both survived through a time when comments were absolutely necessary.
> In the '70s and '80s I was an assembly language programmer. I also wrote a bit of
> FORTRAN. Programs in those languages that had no comments were impenetrable.
>
> As a result it became conventional wisdom to write comments by default. And, indeed,
> computer science students were taught to write comments uncritically. Comments became
> _pure good_.
>
> In _Clean Code_ I decided to fight that mindset.

  - **이것이 4장을 읽는 데 중요한 맥락이다.** 그 장의 세기는 무주석을 목표로 한 것이
    아니라 **무비판적 주석 관행을 겨냥한 반작용**이었다는 저자 본인의 진술이다. 조문
    자체는 그대로 남지만 의도의 범위가 좁아진다.
- **"실패"라는 낱말의 뜻도 좁혀진다** — 오스터하우트가 코드로 표현할 수 없는 정보가 있고
  그것을 주석으로 채우는 것은 표현 능력의 실패가 아니라고 하자, 마틴은
  (§"Comments", UB 발언):[^ousterhout2024-aposd]

> It's very true that there is important information that is not, or cannot be, expressed
> in code.  That's a failure.  A failure of our languages, or of our ability to use them
> to express ourselves.

  - 그리고 반사실 진술로 입장을 못 박는다 — **완벽한 프로그래밍 언어가 있다면 우리는 다시는
    주석을 쓰지 않을 것이다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
    **이것이 모순 ②가 해소되지 않는 이유의 핵심이다** — 마틴에게 주석은 언어의 결함을
    메우는 임시방편이고, 오스터하우트에게는 코드가 원리적으로 담을 수 없는 정보의 자리다.
- **마틴의 주석 읽기 원칙이 여기서 처음 명문화된다** (§"Comments",
  UB 발언):[^ousterhout2024-aposd]

> I look at every comment as potential misinformation.  At best they are a way to
> crosscheck the author's intent against the code.

  - 그리고 좋은 주석의 기준 — **가장 좋은 주석은 코드에 대해 놀랍고 검증 가능한 무언가를
    말해 주는 것이다. 가장 나쁜 것은 뻔하거나 틀린 것을 말해 내 시간을 낭비하는
    것이다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
  - 오스터하우트가 그 귀결을 셈한다 — 코드를 읽어 확인하기 전에는 믿지 않는다면
    **당신의 답은 0퍼센트인 것 같다**고 되묻는다 (§"Comments",
    JOHN 발언).[^ousterhout2024-aposd] 마틴의 답 — **내 주석에 대한 신뢰는 물론 이분법이
    아니다. 있으면 읽는다; 다만 암묵적으로 신뢰하지는 않는다** (§"Comments",
    UB 발언).[^ousterhout2024-aposd]

### 주석 쟁점에서 마틴이 물러선 세 자리

**요약 절이 "합의를 찾기 어려웠다"고 적지만, 본문에는 좁혀 간 자리가 셋 있다.**

- **① 인터페이스 주석이 필요한 경우가 있다** (§"Comments", UB 발언):[^ousterhout2024-aposd]

> Yes, there are times when the signature of a method is an incomplete abstraction and a
> comment is required.  This is especially true when the interface is part of a public
> API, or an API intended for use by a separate team of developers.  Within a single
> development team, however, long descriptive comments on interfaces are often more of an
> impediment than a help.

  - 그리고 팀 안에서도 한 걸음 더 물러선다 — **어떤 인터페이스는 팀 내부용이라도 주석이
    필요하다고 생각한다. 다만 팀이 시스템에 충분히 익숙해서 잘 지은 메서드 이름과 인수
    이름으로 충분한 경우가 더 많다고 본다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
  - **이것이 모순 ②의 최종 경계다.** 다투는 것은 "주석이 필요한가"가 아니라 **팀 내부
    인터페이스에도 필요한가**다.
- **② 주석이 코드보다 정밀할 때가 있다** — 오스터하우트가 제안한 헤더 주석을 두고
  마틴이 **정당한 지적이다. 정밀함이 주석으로 더 잘 표현되는 때가 있다**고 적는다
  (§"Comments", UB 발언).[^ousterhout2024-aposd] 앞서 그가 자연어의 부정확함을 근거로
  들었던 것을 스스로 되돌리는 자리다.
- **③ 코드는 뻔해야 한다는 원칙에 동의한다** — 오스터하우트가 **고통 뒤의 카타르시스는
  그리스 비극에는 훌륭하지만 코드를 읽는 데는 아니다**라고 하자 (§"Comments",
  JOHN 발언)[^ousterhout2024-aposd] 마틴은 **당신의 정서에 반대하지 않는다. 좋은 깨끗한
  코드는 가능한 한 이해하기 쉬워야 한다**고 답한다 (§"Comments",
  UB 발언).[^ousterhout2024-aposd] 이 KB의
  [코드는 뻔해야 한다](obvious-code.md)가 세운 명제에 양측이 서명한 자리다.
- **계량 진술 둘이 오스터하우트 쪽에서 나온다** — 주석이 제대로 달렸다면 뻔했을 것을
  알아내려고 코드를 헤매는 데 **개발 시간의 50–80퍼센트**를 쓰는 일이 드물지 않고,
  **빠진 주석의 비용이 틀린 주석의 비용의 10–100배**라는 것이다 (§"Comments",
  JOHN 발언).[^ousterhout2024-aposd] 어느 쪽도 이 수치의 출처를 대지 않는다 —
  #speculation 개인 경험의 어림이다.

## 주석 요약 — 합의를 찾지 못한 자리

**세 쟁점 중 유일하게 합의가 거의 없는 주제다.** 요약 절의 마지막 문장이 그것을 적는다
(§"Comments Summary", JOHN 발언):[^ousterhout2024-aposd]

> Overall, we struggled to find areas of agreement on this topic.

- 갈리는 항목들 (§"Comments Summary", JOHN 발언):[^ousterhout2024-aposd]
  - **주석에 대한 우리의 전반적 견해는 근본적으로 다르다. 나는 당신보다 주석에서 더 많은
    가치를 보고, 그것이 시스템 설계에서 근본적이고 대체 불가능한 역할을 한다고 믿는다.**
  - **계량 가능한 진술 하나** — **주어진 코드 조각에 대해 나는 당신보다 아마 5–10배 많은
    줄의 주석을 쓸 것이다.**
  - **손익의 방향이 반대다** — **나는 빠진 주석이 틀렸거나 도움 안 되는 주석보다 훨씬 큰
    생산성 손실 원인이라고 믿는다; 당신은 일반적으로 실천되는 대로의 주석이 순손실이라고
    믿는다: 나쁜 주석이 잡아먹는 시간이 좋은 주석이 아끼는 시간보다 크다.**
  - **긴 메서드 이름 문제** — 마틴은 주석으로 표현할 정보를 가능한 한 코드로 옮기라고
    권하고, 그 예가 아주 긴 메서드 이름이다. 오스터하우트는 **아주 긴 이름은 어색하고
    이해하기 어려우며, 더 짧은 이름에 주석을 보태는 편이 낫다**고 본다.
  - **인터페이스 주석의 범위** — **나는 많은 주석 없이는 인터페이스를 정의하고 추상을
    만드는 것이 불가능하다고 믿는다. 당신은 공개 API에 대해서는 동의하지만, 팀 내부
    인터페이스에는 주석의 필요를 거의 보지 않는다.**
    - **이것이 모순 ②의 정확한 경계다.** 이 KB의 [주석은 실패다](comments-as-failure.md)가
      "좋은 주석 여덟 종"에 공개 API Javadoc이 들어 있다는 점으로 모순 범위를 좁혀
      두었는데, 이 대담이 그 좁힘을 양측 진술로 확인한다.
  - **신뢰의 문제** — **당신은 코드를 읽어 확인하기 전에는 주석을 믿지 않으려 한다.
    나는 대체로 주석을 믿는다; 그렇게 함으로써 나는 당신만큼 코드를 많이 읽을 필요가
    없다. 당신은 이것이 나를 너무 큰 위험에 노출시킨다고 본다.**
  - **합의도 하나 있다** — **구현 코드는 그 코드가 뻔하지 않을 때만 주석이 필요하다는
    데 우리는 동의한다.** 이 KB의
    [주석은 코드에서 뻔하지 않은 것을 서술한다](comments-describe-the-nonobvious.md)가
    이미 합의 자리로 적어 둔 것과 일치한다.
- 마틴의 확인 — **이것은 우리 각자 입장에 대한 공정한 평가이고, 나는 그것이 우리의 서로
  다른 개인적 경험에 근거한다고 본다. 오랜 세월 나는 업계에서 일반적으로 실천되는 대로의
  주석 대다수가 도움이 되지 않는다고 느꼈다. 당신은 마주친 주석에서 더 많은 도움을 얻은
  것 같다** (§"Comments Summary", UB 발언).[^ousterhout2024-aposd]

## 셋째 쟁점 — 테스트 주도 개발

- **여기서는 마틴이 공격하는 쪽이다.** 그는 오스터하우트 책 p.157의 TDD 서술을 인용하며
  **아주 짧고, 무시하는 투이고, 경멸적이고, 부정확한 절**이라고 적는다
  (§"Test-Driven Development", UB 발언).[^ousterhout2024-aposd]
- 그리고 세 법칙으로 TDD를 다시 정의한다 — 이 KB의
  [자기 테스트 코드](self-testing-code.md)가 원전 9장에서 옮긴 것과 같은 세 법칙이다.
- 오스터하우트의 입장 — 단위 테스트에는 열렬히 찬성하되 **테스트가 코드보다 먼저 쓰여야
  하고 코드가 아주 작은 증분으로 쓰이고 테스트돼야 한다고 규정하는 TDD의 팬은 아니다**
  (§"Test-Driven Development", JOHN 발언).[^ousterhout2024-aposd]
- **대안에 이름이 붙는다 — 번들링(bundling).** 오스터하우트가 **개발자가 TDD보다 다소 큰
  단위, 아마 메서드 몇 개나 클래스 하나로 작업하는** 방식을 설명하자 마틴이 **이 문서의
  목적상 이 기법을 "번들링"이라 부르는 게 어떤가? 이것은 내가 *Clean Code 2판*에서 쓰는
  용어다**라고 제안한다 (§"Test-Driven Development", UB 발언).[^ousterhout2024-aposd]

## 오스터하우트의 양보

**대담이 한쪽만 물러서는 구조가 아니라는 증거다.**

- 오스터하우트가 자기 책의 사실 오류를 인정한다 (§"Test-Driven Development",
  JOHN 발언):[^ousterhout2024-aposd]

> Oops! I plead "guilty as charged" to inaccurately describing TDD. I will fix this in the
> next revision of APOSD. That said, your definition of TDD does not change my concerns.

  - **이 KB에 반영해야 할 사실이 여기 있다.** ousterhout2021의 TDD 서술은 **저자 자신이
    부정확하다고 인정했고 다음 개정에서 고치겠다고 밝힌** 대목이다. 이 KB에 그 절이
    반입돼 있다면 이 단서가 붙어야 한다.
- 마틴이 TDD의 이득으로 드는 넷 — 디버깅 필요가 거의 없다, 신뢰할 수 있는 저수준 문서가
  테스트 형태로 쌓인다, 테스트 가능성이 결합을 낮춘다, 목숨을 걸 만한 테스트 모음이
  두려움 없는 리팩터링을 뒷받침한다 (§"Test-Driven Development",
  UB 발언).[^ousterhout2024-aposd]
- **그리고 마틴이 번들링을 상당 부분 인정한다** — **작은 단위로 작업하고 곧바로 사후
  테스트를 쓰는 것이 위의 이득을 전부 줄 수 있어 보인다. … 실제로 그런 프로그래머는
  TDD를 따르는 다른 프로그래머가 쓴 코드와 내가 구별할 수 없는 코드를 만들어 낼 것이라고
  생각한다** (§"Test-Driven Development", UB 발언).[^ousterhout2024-aposd]

**TDD 요약** (§"TDD Summary"):[^ousterhout2024-aposd]

| | 내용 |
|---|---|
| 합의 | 단위 테스트는 필수 요소다 — 무언가를 깨뜨릴 두려움 없이 큰 변경을 하게 해 준다 |
| 합의 | TDD로 좋은 설계의 시스템을 만드는 것이 가능하다 |
| 불합의 | TDD가 좋은 설계를 저해하는가 |
| 불합의 | 번들링이 TDD만큼 좋은 결과를 낼 수 있는가(마틴은 동의하되 커버리지가 다소 낮아질 수 있다고 봄) |
| 불합의 | 최선의 경우는 비슷하되 평균·최악의 경우가 TDD 쪽이 훨씬 나쁜가 |

- 마틴의 확인 — **우리는 규율의 최선의 적용을 놓고 갈리는 것 같다. … 우리는 이 두 규율의
  위험과 보상에 대해 의견이 다르다** (§"TDD Summary", UB 발언).[^ousterhout2024-aposd]

## 맺음말 — 두 가지 일반적 오류

오스터하우트가 자기 우려를 두 가지로 압축한다 (§"Closing Remarks",
JOHN 발언):[^ousterhout2024-aposd]

> I think that most of my concerns result from two general errors made by *Clean Code*:
> failure to focus on what is important, and failure to balance design tradeoffs.

- **첫째 오류의 실물 셋** — 열 줄 메서드를 다섯 줄로, 다섯 줄을 두세 줄로 나누는 것;
  영어로 쓰인 주석을 없애는 것; 코드보다 테스트를 먼저 쓰고 개발의 기본 단위를 추상이
  아니라 테스트로 삼는 것. **이 중 어느 것도 유의미한 가치를 주지 않는다**
  (§"Closing Remarks", JOHN 발언).[^ousterhout2024-aposd]
- **둘째 오류가 이 KB의 모순 판정과 가장 가깝다** (§"Closing Remarks",
  JOHN 발언):[^ousterhout2024-aposd]

> Almost any design idea becomes a bad thing if taken to the extreme. However, *Clean
> Code* repeatedly gives very strong advice in one direction without correspondingly
> strong advice in the other direction or any meaningful guidance about how to recognize
> when you have gone too far.

- **마틴의 맺음** (§"Closing Remarks", UB 발언):[^ousterhout2024-aposd]

> For my part I'll just say that I have given due consideration to the points you've made,
> and while I disagree with your conclusions above, I have integrated several of your
> better ideas, as well as this entire document, into the second edition of _Clean Code_.

  - **결론이 불합의로 닫힌다.** 마틴은 상대의 결론에 동의하지 않는다고 명시하면서도
    아이디어 일부와 이 문서 전체를 2판에 통합했다고 적는다. 그리고 시작에서 그는
    **우리를 가르는 것보다 공유하는 가치가 훨씬 많다고 생각한다**고 적는다 (§"Closing
    Remarks", UB 발언).[^ousterhout2024-aposd]

## 판본 — Clean Code 2판이 존재한다

**이 문서가 이 KB에 가져온 가장 실무적인 사실이다.** 마틴이 세 자리에서 2판을 언급한다 —
메서드 길이 지침에 대해 **2판에서는 더 균형을 잡았다**, 번들링이라는 용어를 **2판에서
쓴다**, 그리고 맺음말에서 이 문서 전체를 2판에 통합했다는
진술이다.[^ousterhout2024-aposd]

- **이 KB의 martin2008 반입분은 초판(2008)이다.** 그러므로 그 페이지들의 주장에는 판본
  조건이 붙는다.
- 버전 조건: Clean Code 초판(2008) 기준. 저자 본인이 2판에서 메서드 길이 지침의 균형을
  조정했다고 밝혔으므로, **분해를 어디서 멈출 것인가에 관한 claim은 2판에 그대로
  적용된다고 볼 수 없다.** 주석과 TDD에 대해서는 저자가 입장을 바꿨다고 말하지 않았다.
- **2판은 이 KB에 아직 반입돼 있지 않다.** 반입하면 이 KB의 모순 ①이 재심 대상이다 —
  모순 ②는 이 대담에서 마틴이 주석에 대한 입장을 바꾸지 않았으므로 그대로다.

## 이 문서가 이 KB의 판정에 더하는 것

이 KB는 두 책의 문장만 대조해 `contradicts` 둘을 세웠다. 이 문서는 그 판정을 **바꾸지
않고 다음 넷을 더한다.**

- **① 판정이 추론이 아니라 1차 진술로 뒷받침된다.** 두 저자가 같은 두 쟁점을 스스로
  "우리의 불합의 영역"이라 부르고 그 목록을 조문화했다. 이 KB가 모순으로 세운 두 명제가
  그 목록에 그대로 있다.
- **② 모순이 무마되지 않는 이유가 확인된다.** 잣대는 같다(둘 다 읽는 사람의 부담을 줄이는
  것을 목표로 한다고 명시적으로 합의했다). 갈리는 것은 **같은 조작에 대한 두 값의 상대적
  가중치**다 — 마틴 본인의 진단이다. 층위 차이가 아니므로 무마할 수 없다.
- **③ 모순의 범위가 양측 진술로 좁혀진다.** 모순 ①은 "분해가 좋은가"가 아니라 "어디서
  멈추는가"이고, 모순 ②는 "주석이 필요한가"가 아니라 "팀 내부 인터페이스에도 필요한가"다.
  둘 다 이 KB가 이미 좁혀 둔 경계와 일치한다.
- **④ 양쪽 모두 물러선 자리가 기록된다.** 마틴은 과잉 분해의 가능성·책의 지침 부족·
  자기 예제의 난독성을 인정했고, 오스터하우트는 자기 책의 TDD 서술이 부정확했음을
  인정했다. **모순 페이지가 어느 한쪽을 옳다고 세우지 않는 근거다.**

## 이어지는 페이지

- [작은 함수](small-functions.md) — 쟁점 ①의 한쪽. 마틴의 양보 셋이 이 페이지의 주장
  범위를 좁힌다
- [깊은 모듈과 얕은 모듈](deep-and-shallow-modules.md) — 쟁점 ①의 다른 쪽. 얽힘이라는
  둘째 기제가 여기 더해진다
- [주석은 실패다](comments-as-failure.md) — 쟁점 ②의 한쪽
- [주석을 왜 쓰는가](why-write-comments.md) — 쟁점 ②의 다른 쪽. 5–10배라는 계량 진술이
  여기 붙는다
- [자기 테스트 코드](self-testing-code.md) — 쟁점 ③. 번들링이라는 이름이 붙은 대안
- [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md) — 같은 절충을 셋째 소스가
  다루는 자리
- [클린 코드 비판](clean-code-criticism.md) — 같은 예제를 다루는 2차 문헌. 이 문서로
  그쪽의 장 표기 오류가 확인됐다
- [클린 코드라는 말의 정의](clean-code-defined.md) — 마틴이 근거로 드는 p.13 유보의 자리
- [클린 코드](../synthesis/clean-code.md) — 이 축의 허브

[^ousterhout2024-aposd]: Ousterhout & Martin 2024, "A Philosophy of Software Design vs
    Clean Code"(머리말 · §"Introductions" · §"Method Length" · §"Method Length Summary" ·
    §"Comments" · §"Comments Summary" · §"Test-Driven Development" · §"TDD Summary" ·
    §"Closing Remarks"). **대담이므로 locator에 발언자를 함께 적는다** — `JOHN`은 John
    Ousterhout, `UB`는 Robert "Uncle Bob" Martin이다. 규약과 스냅샷 취득 경로(GitHub
    raw가 429로 막혀 인증 API로 받았다)는 `it/archive/ousterhout2024-aposd/_progress.yaml`
    머리말이 정본이다. 이 문서의 코드 블록은 펜스로 옮기지 않았다 — 전부 두 저자가
    논쟁하는 예제이고 복사해 돌아갈 코드가 아니다. 두 저자가 `PrimeGenerator`를 각자 다시
    쓰는 세 절은 반입하지 않았다(사유는 `_progress.yaml`의 `skipped`).

[^martin2008]: Martin 2008, 1장 §"Schools of Thought"(p.13) · 3장 §"Small!"(p.34)·
    §"Blocks and Indenting"(p.35) · 10장 Listing 10-8(pp.145–146). **논쟁 중인 소스다** —
    지위와 반입 규약은 `it/sources/martin2008.md`가 정본이다. 이 페이지에서 이 소스는
    **대담이 인용한 대목을 원문과 대조하는 용도로만** 쓰였다. 쪽은 인쇄판 쪽 번호이며
    복원 절차는 `it/archive/martin2008/_progress.yaml` 머리말이 정본이다.

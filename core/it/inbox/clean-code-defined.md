---
type: concept
title: 클린 코드라는 말의 정의
description: 이 책이 자기 표제어를 정의하는 방식 — 저자가 답하는 대신 여섯 명의 이름난 프로그래머에게 물어 서로 다른 정의를 나란히 싣는 구성과 그 여섯 정의, 어질러짐이 생산성을 0으로 수렴시킨다는 논증과 그것을 뒷받침하는 근거의 종류, 하늘의 대개편이라는 실패 서사, 나중은 결코 오지 않는다는 격언, 읽기 대 쓰기 10대 1이라는 수치, 보이스카우트 규칙, 그리고 켄트 벡의 단순 설계 네 규칙이 우선순위와 함께 놓이는 자리
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: martin2008, resource: /it/sources/martin2008.md }
---

# 클린 코드라는 말의 정의

- [정의를 저자가 내리지 않는다](#정의를-저자가-내리지-않는다)
- [여섯 정의](#여섯-정의)
- [어질러짐의 총 소유 비용](#어질러짐의-총-소유-비용)
- [하늘의 대개편](#하늘의-대개편)
- [읽기 대 쓰기 10대 1](#읽기-대-쓰기-10대-1)
- [보이스카우트 규칙](#보이스카우트-규칙)
- [단순 설계 네 규칙 — 우선순위가 붙은 목록](#단순-설계-네-규칙--우선순위가-붙은-목록)
- [네 규칙에 대한 저자의 해설](#네-규칙에-대한-저자의-해설)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **이 책이 말하는 "깨끗한 코드"는 무엇이며, 그 정의는 어떻게 세워지는가.**

> **이 페이지의 소스는 논쟁 중인 소스다.** 반입 지위와 그 근거는
> [소스 메타](../sources/martin2008.md)가 정본이다. **이 장은 처방이 아니라 정의와
> 동기 부여의 장이라 논쟁이 얇다** — 논쟁이 걸린 것은 이 정의에서 파생된 3·4장의 처방이다.

## 정의를 저자가 내리지 않는다

1장의 구성 자체가 특이하다. 저자는 "깨끗한 코드란 무엇인가"를 자기 답으로 채우지 않고
**여섯 명의 이름난 프로그래머에게 물어 그 답을 곁글로 나란히 싣는다**. 그래서 이 장의
정의는 하나가 아니라 여섯이고, 서로 강조점이 다르다.

- 그 여섯은 Bjarne Stroustrup, Grady Booch, "Big" Dave Thomas, Michael Feathers,
  Ron Jeffries, Ward Cunningham이다 (1장 §"What Is Clean Code?",
  pp.7–11).[^martin2008]
- **저자가 자기 판단을 얹는 자리는 한 곳뿐이다** — Dave Thomas의 답에 테스트가 들어 있는
  것을 두고 (1장 §"What Is Clean Code?", p.9):[^martin2008]

> Dave is right. Code, without tests, is not clean. No matter how elegant it is, no
> matter how readable and accessible, if it hath not tests, it be unclean.

## 여섯 정의

- **Bjarne Stroustrup** (1장, p.7):[^martin2008]

> I like my code to be elegant and efficient. The logic should be straightforward to make
> it hard for bugs to hide, the dependencies minimal to ease maintenance, error handling
> complete according to an articulated strategy, and performance close to optimal so as
> not to tempt people to make the code messy with unprincipled optimizations. Clean code
> does one thing well.

- **Grady Booch** (1장, p.8):[^martin2008]

> Clean code is simple and direct. Clean code reads like well-written prose. Clean code
> never obscures the designer's intent but rather is full of crisp abstractions and
> straightforward lines of control.

- **"Big" Dave Thomas** (1장, p.9):[^martin2008]

> Clean code can be read, and enhanced by a developer other than its original author. It
> has unit and acceptance tests. It has meaningful names. It provides one way rather than
> many ways for doing one thing. It has minimal dependencies, which are explicitly
> defined, and provides a clear and minimal API. Code should be literate since depending
> on the language, not all necessary information can be expressed clearly in code alone.

  - **마지막 문장에 유의할 것.** "언어에 따라 필요한 정보 전부가 코드만으로 명확히
    표현될 수는 없으므로 코드는 문학적이어야 한다"는 이 진술은 4장의 조문("진실은 코드
    한 곳에만 있다")과 **같은 책 안에서 방향이 다르다**. 저자는 이 곁글에 판단을 얹지
    않는다. [주석은 실패다](comments-as-failure.md)의 모순 절이 겨냥하는 명제가 여기
    이미 완화된 형태로 실려 있는 셈이다.
- **Michael Feathers** (1장, p.10):[^martin2008]

> Clean code always looks like it was written by someone who cares. There is nothing
> obvious that you can do to make it better.

- **Ron Jeffries** — Kent Beck의 단순 설계 규칙을 우선순위대로 든 뒤 (1장,
  p.10):[^martin2008]

> Of these, I focus mostly on duplication. When the same thing is done over and over,
> it's a sign that there is an idea in our mind that is not well represented in the code.

  그리고 요약 — **중복 줄이기, 높은 표현력, 단순한 추상을 이르게 세우기. 그것이 나에게
  깨끗한 코드다** (1장, p.11).[^martin2008]
- **Ward Cunningham** (1장, p.11):[^martin2008]

> You know you are working on clean code when each routine you read turns out to be
> pretty much what you expected. You can call it beautiful code when the code also makes
> it look like the language was made for the problem.

  - 이 문장이 책 전체에서 되풀이 인용된다 — 3장의 서술적 이름 절과 17장 `N1`이 각각
    이것을 부른다.

## 어질러짐의 총 소유 비용

- 서사 — **1~2년의 기간에 걸쳐, 프로젝트 초기에 아주 빠르게 움직이던 팀이 달팽이 걸음으로
  움직이는 자신을 발견할 수 있다. 그들이 코드에 가하는 모든 변경이 코드의 다른 두세
  부분을 깨뜨린다. 어떤 변경도 사소하지 않다** (1장 §"The Total Cost of Owning a Mess",
  p.4).[^martin2008]
- 그리고 곡선 주장 (1장 §"The Total Cost of Owning a Mess", p.4):[^martin2008]

> As the mess builds, the productivity of the team continues to decrease, asymptotically
> approaching zero.

  - **이 주장은 그림 하나(Figure 1-1 "Productivity vs. time")에 기대고 있고, 이 소스는
    그 곡선의 출처나 측정을 대지 않는다.** 저자의 경험 서술이 근거다. 이 KB의 다른
    소스에서 같은 현상을 다루는 자리가 [소프트웨어 엔트로피와 깨진
    유리창](../concepts/software-entropy-and-broken-windows.md)이다.
- 격언 하나가 이 장에서 나온다 — **르블랑의 법칙(LeBlanc's law): *나중은 결코 오지
  않는다(Later equals never)*** (1장 §"Bad Code", p.4).[^martin2008]

## 하늘의 대개편

- 실패 서사 — 어질러진 시스템을 못 견딘 팀이 재설계를 요구하고, 경영진이 **하늘의 대개편
  (the grand redesign in the sky)**을 승인한다. 정예 팀이 새 시스템을 만드는 동안 기존
  팀은 옛 시스템을 계속 유지해야 하므로 두 시스템이 경주한다 (1장 §"The Grand Redesign
  in the Sky", p.5).[^martin2008]
- 결말 (1장 §"The Grand Redesign in the Sky", p.5):[^martin2008]

> This race can go on for a very long time. I've seen it take 10 years. And by the time
> it's done, the original members of the tiger team are long gone, and the current members
> are demanding that the new system be redesigned because it's such a mess.

- 그로부터 나오는 결론 — **깨끗한 코드를 유지하는 데 시간을 쓰는 것은 비용 효율적일 뿐
  아니라 직업적 생존의 문제다** (1장 §"The Grand Redesign in the Sky",
  p.5).[^martin2008]
- 그리고 마감 압박에 대한 판정 (1장 §"The Primal Conundrum", p.6):[^martin2008]

> You will *not* make the deadline by making the mess. Indeed, the mess will slow you
> down instantly, and will force you to miss the deadline. The *only* way to make the
> deadline—the only way to go fast—is to keep the code as clean as possible at all times.

  - **"언제나(at all times)"가 이 책의 성격을 드러낸다.** 같은 물음에 시점과 양의
    문제로 답하는 소스가 이 KB에 있다 —
    [정리는 언제 하는가](when-to-tidy.md)와
    [전략적 프로그래밍과 전술적 프로그래밍](strategic-versus-tactical-programming.md).
    그쪽들은 "언제나"가 아니라 **얼마나·언제**를 계산한다. 모순은 아니다 — 이 진술은
    처방이 아니라 동기 부여 문단이고 이 책 어디에도 그 양을 계량하는 자리가 없어
    대질할 명제가 성립하지 않는다.

## 읽기 대 쓰기 10대 1

- 수치 (1장 §"The Boy Scout Rule" 앞, p.14):[^martin2008]

> Indeed, the ratio of time spent reading vs. writing is well over 10:1. We are
> *constantly* reading old code as part of the effort to write new code.

  - **이 수치의 출처는 이 소스에 없다.** 저자의 단언이다. 그럼에도 이 책의 거의 모든
    처방이 이 비율을 전제로 정당화되므로 기록해 둔다 — 읽기 편함을 쓰기 편함보다 우선하는
    판단의 근거다. 같은 우선순위를 다른 소스가 세우는 자리가
    [코드는 뻔해야 한다](obvious-code.md)의 "읽기 편함이 쓰기 편함을 이긴다" 절이다.

## 보이스카우트 규칙

- 규칙 (1장 §"The Boy Scout Rule", p.14):[^martin2008]

> Leave the campground cleaner than you found it.

- 적용 — **우리가 모두 코드를 체크아웃할 때보다 조금 더 깨끗하게 체크인한다면 코드는
  그저 썩을 수가 없다. 청소가 거창할 필요는 없다. 변수 이름 하나를 더 낫게 바꾸고, 좀
  긴 함수 하나를 쪼개고, 작은 중복 하나를 없애고, 복합 `if` 문 하나를 정리하라** (1장
  §"The Boy Scout Rule", p.14).[^martin2008]
  - 이 KB에 같은 실천을 다른 이름으로 담은 자리가 여럿이다 —
    [정리하기](tidying.md)(Beck), [언제 리팩터링하는가](when-to-refactor.md)(Fowler),
    [소프트웨어 엔트로피와 깨진 유리창](../concepts/software-entropy-and-broken-windows.md)(실용주의).
    **네 소스가 같은 처방에 도달한 드문 자리다.**

## 단순 설계 네 규칙 — 우선순위가 붙은 목록

12장이 Kent Beck의 규칙을 우선순위와 함께 싣는다 (12장, p.172):[^martin2008]

> According to Kent, a design is "simple" if it follows these rules:
> • Runs all the tests
> • Contains no duplication
> • Expresses the intent of the programmer
> • Minimizes the number of classes and methods
> The rules are given in order of importance.

- **같은 책 1장에 Ron Jeffries가 옮긴 판본이 따로 실려 있고 문구가 다르다** (1장,
  p.10):[^martin2008]

> In priority order, simple code:
> • Runs all the tests;
> • Contains no duplication;
> • Expresses all the design ideas that are in the system;
> • Minimizes the number of entities such as classes, methods, functions, and the like.

  - 셋째 규칙이 "프로그래머의 의도를 표현한다"와 "시스템에 있는 모든 설계 아이디어를
    표현한다"로, 넷째가 "클래스와 메서드"와 "클래스·메서드·함수 등의 엔티티"로 갈린다.
    **둘 다 이 책 안에 있으므로 뭉뚱그리지 않는다.** 우선순위가 붙어 있다는 점은 두
    판본이 같다.

## 네 규칙에 대한 저자의 해설

- **규칙 1(모든 테스트를 돌린다)** — **테스트 가능하게 만드는 것이 우리를 클래스가 작고
  단일 목적인 설계로 밀어 준다. SRP를 따르는 클래스를 테스트하기가 더 쉬울 뿐이다. 테스트를
  더 많이 쓸수록 우리는 테스트하기 더 단순한 것들 쪽으로 계속 밀려간다** (12장 §"Simple
  Design Rule 1", p.172).[^martin2008] 그리고 결론 — **테스트를 쓰는 것이 더 나은 설계로
  이어진다** (12장 §"Simple Design Rule 1", p.172).[^martin2008]
- **규칙 2(중복 없음)** — **중복은 잘 설계된 시스템의 주적이다. 그것은 추가 작업, 추가
  위험, 추가로 불필요한 복잡성을 나타낸다** (12장 §"No Duplication",
  p.173).[^martin2008] 그리고 **깨끗한 시스템을 만드는 데는 단 몇 줄의 코드에서라도 중복을
  없애려는 의지가 필요하다** (12장 §"No Duplication", p.173).[^martin2008]
  - **"작은 것의 재사용"이라는 개념이 여기서 나온다** — **이 "작은 것의 재사용"은 시스템
    복잡성을 극적으로 줄일 수 있다. 작은 것의 재사용을 이루는 법을 이해하는 것이 큰 것의
    재사용을 이루는 데 본질적이다** (12장 §"No Duplication", p.174).[^martin2008]
- **규칙 4(클래스와 메서드 수 최소화)에 이 책의 자기 제한이 들어 있다** (12장 §"Minimal
  Classes and Methods", p.176):[^martin2008]

> Even concepts as fundamental as elimination of duplication, code expressiveness, and
> the SRP can be taken too far. In an effort to make our classes and methods small, we
> might create too many tiny classes and methods. So this rule suggests that we also keep
> our function and class counts low.

  - **이것이 이 책 안에서 [작은 함수](small-functions.md)의 극단주의에 대한 유일한
    명시적 제동이다.** 그리고 곧바로 약화된다 — **그러나 이 규칙이 네 규칙 중 우선순위가
    가장 낮다는 것을 기억하라. 그러니 클래스와 함수 수를 낮게 유지하는 것이 중요하긴
    하지만, 테스트를 갖추고 중복을 없애고 스스로를 표현하는 것이 더 중요하다** (12장
    §"Minimal Classes and Methods", p.176).[^martin2008]
  - **그래서 이 절은 모순 절을 무마하지 못한다.** 제동이 존재하되 우선순위상 가장 약한
    것으로 명시돼 있고, 3장에는 이 제동을 적용하는 자리가 없다.
- **규칙 3(표현력)** — **소프트웨어 프로젝트 비용의 대부분은 장기 유지보수에 있다.
  그러므로 코드는 저자의 의도를 명확히 표현해야 한다** (12장 §"Expressive",
  p.175).[^martin2008] 표현의 수단으로 좋은 이름, 작은 함수와 클래스, 표준 명명, 그리고
  **잘 쓴 단위 테스트**를 든다 — **테스트의 주된 목표 하나는 예제로서의 문서 노릇이다**
  (12장 §"Expressive", p.175).[^martin2008]

## 이어지는 페이지

- [작은 함수](small-functions.md) — 이 정의에서 파생된 처방이자 모순 축 하나
- [주석은 실패다](comments-as-failure.md) — 모순 축 둘. Dave Thomas의 정의가 이미
  방향이 다른 자리
- [클린 코드의 발견법 목록](clean-code-heuristics.md) — 같은 가치 체계가 목록이 된 자리
- [자기 테스트 코드](self-testing-code.md) — "테스트 없는 코드는 깨끗하지 않다"와 단순
  설계 규칙 1이 닿는 자리
- [DRY 원칙](dry-principle.md) — 단순 설계 규칙 2의 축
- [정리하기](tidying.md) · [언제 리팩터링하는가](when-to-refactor.md) — 보이스카우트
  규칙과 같은 처방에 도달한 다른 소스들
- [정리는 언제 하는가](when-to-tidy.md) — "언제나"가 아니라 양을 계산하는 쪽
- [전략적 프로그래밍과 전술적 프로그래밍](strategic-versus-tactical-programming.md) —
  같은 투자 논증을 다른 소스가 세우는 자리
- [코드는 뻔해야 한다](obvious-code.md) — 읽기 편함 우선의 다른 소스 쪽 근거
- [소프트웨어 엔트로피와 깨진 유리창](../concepts/software-entropy-and-broken-windows.md) —
  어질러짐의 누적을 다른 소스가 다루는 자리
- [클린 코드](../synthesis/clean-code.md) — 이 소스의 허브

[^martin2008]: Martin 2008, 1장 "Clean Code"(§"Bad Code" p.4 · §"The Total Cost of
    Owning a Mess" p.4 · §"The Grand Redesign in the Sky" p.5 · §"The Primal Conundrum"
    p.6 · §"What Is Clean Code?" pp.7–11 · §"The Boy Scout Rule" p.14) · 12장
    "Emergence"(§"Simple Design Rule 1: Runs All the Tests" p.172 · §"No Duplication"
    pp.173–174 · §"Expressive" p.175 · §"Minimal Classes and Methods" p.176). 쪽은 인쇄판
    쪽 번호이며 복원 절차는 `it/archive/martin2008/_progress.yaml` 머리말이 정본이다.
    직인용에서 문장 끝에 붙은 각주 번호를 뗐고(`found it.5` → `found it.`) 곁글의 조판
    하이픈(`per-formance` 등)을 이었다 — 다른 수정은 없다. 12장은 저자가 아니라
    이 책의 공저 구성에 따른 장이나 본문에 필자 표기가 없다. 1장 Figure 1-1(생산성 대
    시간 곡선)은 그림이라 딸린 서술 산문만 옮겼다. 두 장 모두 번호 붙은 코드 리스팅이
    없다.

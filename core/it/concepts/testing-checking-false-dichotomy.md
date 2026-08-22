---
type: concept
title: 테스팅·체킹은 거짓 이분법이다
description: 자동화 가능한 것의 경계를 낱말로 긋는 시도를 같은 학파 안에서 반박한 글 — 고용량 자동 테스팅 워크숍에서 들은 두 장면과 그것이 촉발한 반박, 모든 테스트가 수동이면서 동시에 자동이라는 두 극단 논증, 수동과 자동의 구분이 원칙이 아니라 정도의 문제라는 판정, 체킹과 비체킹을 이분이 아니라 정도로 다시 규정한 두 문장, 상대 진영의 오라클 카탈로그를 그대로 근거로 삼는 되묻기, 근거로 삼는 맥락 주도 테스팅의 전제, 그리고 이 반박 자신도 측정이 아니라 저술이라는 한계
generated: { by: "claude-opus-5", at: "2026-08-22T12:30:00Z" }
contradicts: [testing-checking-distinction]
sources:
  - { id: kaner2013-insapience, resource: /it/sources/kaner2013-insapience.md }
---

# 테스팅·체킹은 거짓 이분법이다

- [이 소스의 지위 — 실무자 에세이지 학술 근거가 아니다](#이-소스의-지위--실무자-에세이지-학술-근거가-아니다)
- [무엇을 겨냥한 글인가 — 두 장면](#무엇을-겨냥한-글인가--두-장면)
- [수동과 자동은 정도의 문제다](#수동과-자동은-정도의-문제다)
- [체킹과 테스팅도 마찬가지다](#체킹과-테스팅도-마찬가지다)
- [정도로 다시 규정한 체킹](#정도로-다시-규정한-체킹)
- [상대 진영의 카탈로그를 그대로 근거로 쓴다](#상대-진영의-카탈로그를-그대로-근거로-쓴다)
- [근거는 맥락 주도 테스팅의 전제다](#근거는-맥락-주도-테스팅의-전제다)
- [원문이 넘지 않은 선](#원문이-넘지-않은-선)
- [이 반박에 걸린 모순](#이-반박에-걸린-모순)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스팅에서 자동화 가능한 부분을 낱말로 갈라 두는 것이 가르는 일을
하는가, 아니면 없는 선을 긋는 일인가.**

## 이 소스의 지위 — 실무자 에세이지 학술 근거가 아니다

이 페이지의 소스는 블로그 글 하나다. 측정도, 통제 실험도, 결과 표도 없다. **근거
등급은 실무자 에세이(essay)이고, 이 페이지의 어떤 문장도 학술 실증으로 인용되지
않는다.** 이 글의 무게는 측정이 아니라 **저자가 누구인가**에서 온다.

- 저자가 글 안에서 자기 자격을 규정한다 (§hooey 문단).[^kaner2013-insapience]

  > But some people want to make the additional assertion that the use of (allegedly)
  > non-sapient (allegedly) non-tests conflicts with the essence of context-driven
  > testing. It's at that point that, as one of the founders of the context-driven
  > school, I say "hooey!".

- **그래서 이 글은 바깥에서 온 반박이 아니라 학파 안에서 나온 반박이다.** 반박 대상인
  [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md)의 저자들도 같은
  학파에 속한다. 이 사실이 이 모순 쌍의 성격을 정한다 — 진영 대 진영이 아니라 **같은
  진영 안의 문서 대 문서**다.
- **글이 나온 자리도 밝혀져 있다.** 2013년 소프트웨어 테스팅 교육 워크숍(Workshop on
  Teaching Software Testing, WTST) 12회에 참석한 뒤 쓴 글이고, 그해 주제가 **고용량 자동
  테스팅(high-volume automated testing, HiVAT)**과 그것을 어떻게 가르칠 것인가였다
  (§도입).[^kaner2013-insapience]

  > High-volume automated testing (HiVAT) refers to a family of testing techniques that
  > enable the tester to create, run and evaluate the results of arbitrarily many tests.

## 무엇을 겨냥한 글인가 — 두 장면

저자는 회의 중에 **몇몇 테스팅 컨설턴트가 퍼뜨린 반자동화 주제의 메아리**를 듣고
놀랐다고 적으며 장면 둘을 든다 (§두 장면).[^kaner2013-insapience]

- **첫째 장면 — 사피엔스 어휘.** 한 참석자가 자기 고객들은 더 "사피엔트(sapient)한"
  테스팅 접근에 관심이 있어서 이것에는 별 관심이 없을 것 같다고 말했다는 것이다. 저자가
  그 교리를 이렇게 요약한다.

  > According to the new doctrine, only manual testing can be sapient. Automated tests
  > are done by machines and machines are not sapient. Therefore, automated testing
  > cannot be sapient.

- **둘째 장면 — 체킹이라는 낱말.** 또 다른 참석자가 자기 테스트를 설명하면서 어색해하고
  변명하듯 말했는데, 문제는 그 테스트가 프로그램의 동작을 기대 결과에 비추어 검사한다는
  점이었다는 것이다.

  > According to the new doctrine, "checking" is the opposite of "testing" and therefore,
  > automated tests that check against expectations are not only not sapient, they are
  > not tests. The campaign to make the word "checking" politically incorrect among
  > testers might make good marketing for a few people, but it interferes with worthwhile
  > communication in our field.

- **겨냥점이 낱말의 유통이라는 점을 놓치면 이 글을 오독한다.** 저자가 반박하는 것은
  정의문 자체보다 **그 정의가 현장에서 낳은 태도**다. 그는 낱말을 정치화하거나 자동
  테스팅을 미워하는 것 자체는 시간이 지나면 스스로 교정될 문제라고 보고 크게 개의치
  않는다고 적는다 — 문제는 그 다음 주장, 즉 그것이 맥락 주도 테스팅의 본질과 충돌한다는
  주장이라는 것이다 (§hooey 문단).[^kaner2013-insapience]
- **실무적 대가도 지목한다** — 테스터에게 테스트 자동화를 의심하도록, 그것을 이류로
  다루도록, 사피엔스라는 비법 소스는 수동 테스트에만 있다고 여기도록 가르친다면, 우리는
  **강한 자동화가 가장 잘 듣는 맥락에서 실패할 테스터를 길러 내는 것**이라고 적는다
  (§사피엔스 재규정).[^kaner2013-insapience]

## 수동과 자동은 정도의 문제다

**논증의 뼈대는 같은 대상을 양쪽 극단으로 동시에 기술해 보이는 것이다**
(§두 극단 불릿).[^kaner2013-insapience]

- **모든 소프트웨어 테스트는 수동 테스트다.** 자동 회귀 테스트를 보라 — 컴퓨터가
  실행하고 결과를 간단히 평가하지만, 그 테스트를 **설계한 것도 사람**이고, 컴퓨터가
  실행하는 테스트 코드를 **쓴 것도 사람**이며, 입력 데이터를 **넣은 것도 사람**이고,
  프로그램이 결과를 평가할 때 쓰는 기대 결과를 **제공한 것도 사람**이며, 문제가 있어
  보이면 결과를 살펴 원인을 찾아 버그 리포트를 쓰거나 테스트를 다시 쓰는 것도 사람이다.
  그 모든 사람의 일이 수동이고, **그것은 사람이 머리를 쓸 것을 요구한다(즉 사피엔트하다)**.
- **모든 소프트웨어 테스트는 자동 테스트다.** 수동 테스트를 돌릴 때 입력을 치고 출력을
  보는 것은 사람이지만, 그 입력이 받아들여진 순간부터 처리 결과가 표시되기까지 일어나는
  모든 일은 프로그램의 통제 아래 컴퓨터가 한다. 그러므로 그 테스트 하나하나가 자동이다.
- **그래서 판정이 이렇게 나온다** (§수동·자동 판정).[^kaner2013-insapience]

  > The distinction between manual and automated is a false dichotomy. We are talking
  > about a matter of degree (how much automation, how much manual), not a distinction of
  > principle.

- **저자는 구분 자체를 없애자고 하지 않는다.** 테스터가 알고 싶은 것을 알기 위해 쓰는
  테스트와, 정보 가치를 얻을 계획도 기대도 없이 누군가 만들거나 돌리는 테스트 사이에는
  구분할 것이 있다고 적는다. 그것을 사피엔스의 구분이라 불러도 좋다는 것이다. **다만
  그것을 기술의 사용 여부에 묶는 것이 빗나갔다**고 본다
  (§사피엔스 재규정).[^kaner2013-insapience]

## 체킹과 테스팅도 마찬가지다

- **저자의 테스팅 규정이 여기 있다** (§체킹 문단).[^kaner2013-insapience]

  > I think testing is a search for quality-related information about a product or
  > service under test, and if I execute the program with the goal of learning some
  > quality-related information, that execution seems to me to be a test. Checking is
  > something that I often do when I am doing what I think is good testing.

  - **이 규정이 상대와 갈리는 자리다.** [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md)은
    테스팅을 사람의 학습 과정으로 규정해 기계를 원리상 배제하는데, 이쪽은 테스팅을
    **품질 관련 정보의 탐색**으로 규정해 수행 주체를 정의에 넣지 않는다. 주체가 정의에서
    빠지면 자동이냐 수동이냐는 정의의 문제가 아니라 수단의 문제가 된다.
- **그 규정을 자동화된 경우로 밀어 본다** — 소프트웨어 품질에 대한 물음이 충분히 잘
  형성돼 있고 프로그래밍 실력도 충분해서 그 체킹을 대신 해 줄 프로그램을 쓸 수 있다고
  해 보자. 내 지시에 따라 내 프로그램이 대상 소프트웨어를 돌려 내 물음에 빠르게 답을
  준다 (§자동 체킹 문단).[^kaner2013-insapience]

  > To me, this still looks like a test, even though it is automated checking.

- **반대편 주장을 그대로 옮겨 적고 되묻는다** (§반대 진영 요약·§되묻기
  문단).[^kaner2013-insapience] 어떤 이들은 체킹이 테스팅과 상반된다고, 테스팅은 사람이
  하는 사피엔트한 활동이지만 체킹은 테스팅이 아니라고 주장한다는 것이다. 그렇다면 —
  프로그램의 오늘 동작이 지난달 동작과 일치하는지 검사하면 그것은 테스트가 아닌가?
  계산 결과가 존중받는 경쟁 제품의 것과 일치하는지 검사하면? 명세에 적힌 주장과
  일치하는지 검사하면?

## 정도로 다시 규정한 체킹

**이 두 문장이 이 글의 실질적 제안이다** (§정도 규정
불릿).[^kaner2013-insapience]

> A test is checking to the extent that it is designed to produce results that can be
> compared, without ambiguity, to results anticipated by the test designer.

> A test is not-checking to the extent that it can produce a result that is not
> anticipated by the test designer but is noticeable and informative to the person who
> interprets the test results.

- **`to the extent that`가 이 제안의 전부다.** 체킹과 비체킹은 서로 배타적인 두 상자가
  아니라 **한 테스트가 동시에 갖는 두 정도**다. 그래서 결론이 이렇게 닫힌다
  (§결론 문단).[^kaner2013-insapience]

  > Most tests are checking. Most tests are also not-checking. Checking versus testing is
  > another false dichotomy.

  - **`another`가 가리키는 것은 앞의 수동·자동 판정이다.** 같은 글 안에서 두 번째로
    같은 진단을 내리는 자리이므로, 이 낱말은 두 판정이 하나의 논증임을 표시한다.
- **고용량 자동화가 그 구조의 실물로 제시된다** (§HiVAT
  가치).[^kaner2013-insapience]

  > We do almost all of the high-volume test work with tools. In most cases, we compare
  > test results with expected values. And yet, this is purposeful work being done by
  > humans to answer quality-related questions. It is automated. It is checking. It is
  > testing.

- **그리고 가치 판단이 이름에서 떨어진다** (§HiVAT
  가치).[^kaner2013-insapience]

  > Tests are tests whether they are automated or not, whether they are checking or not.
  > Tests can be excellent tests, and fully appropriate for their contexts, whether they
  > are automated or not, whether they are checking or not. And tests can be worthless,
  > or completely unsuited to their context, whether they are automated checks or
  > intentionally-designed manual tests.

## 상대 진영의 카탈로그를 그대로 근거로 쓴다

**이 대목이 이 글에서 가장 날카로운 자리다.** 저자는 반대편이 스스로 만든 오라클
목록을 들어, 그들의 기준으로도 사피엔트 테스팅의 일부는 체킹이라고 되묻는다
(§되묻기 문단).[^kaner2013-insapience]

> But in the land of Sapient Testing, these particular expectations are enumerated as
> Consistency Heuristics that sapient testers rely on
> (e.g. http://www.developsense.com/blog/2012/07/few-hiccupps/). Apparently, at least
> some sapient testing is checking.

- **인용된 URL은 이 KB에 이미 페이지로 있다** —
  [일관성 오라클 휴리스틱](../concepts/consistency-oracle-heuristics.md)이 그 목록을
  옮긴 페이지이고, 저자는 Michael Bolton이다. 즉 **반박 대상 문서의 공저자가 만든
  카탈로그**가 이 반박의 근거로 쓰인다.
- **논증의 형태는 상대의 전제로 상대를 미는 것이다.** 이력·비교 가능한 제품·주장은
  전부 그 카탈로그의 항목이고, 그 항목들에 비추어 판정하는 일은 명확한 기대를 미리 갖고
  결과를 견주는 일이다. 그것을 체킹이라 부르지 않을 이유가 없다는 것이다.
- **이 KB의 읽기 하나를 덧붙인다.** #hypothesis 이 되묻기는 두 문서가 **같은 낱말을
  다르게 쓰고 있다**는 사실을 드러낸다. 상대의 정의에서 체킹은 *완전 자동화 가능성*으로
  판정되는데, 이 글은 *기대와 견주는가*로 판정한다. 두 판정 기준이 다르므로 같은 활동이
  한쪽에서는 체킹이 아니고 다른 쪽에서는 체킹이다.

## 근거는 맥락 주도 테스팅의 전제다

- **이 반박이 기대는 전제가 명시된다** (§맥락 전제).[^kaner2013-insapience]

  > The basic premise of context-driven testing is that a test approach that works well
  > in one context may fail utterly in some other context. There are no universal best
  > practices (not even manual exploratory testing organized into testing sessions).

  - **괄호 안의 단서가 이 문장을 자기 진영에도 겨눈다.** 세션으로 조직된 수동 탐색적
    테스팅도 보편 모범 사례가 아니라고 못 박는다.
- **판별 절차가 있다 — 반례 셋 세기** (§반례 셋).[^kaner2013-insapience] 아주 좋다고
  생각하는 실천이 있으면 다른 대안이 훨씬 나을 상황 셋을 찾아보고, 마음에 들지 않는
  실천이 있으면 그것이 적절하고 값질 상황 셋을 찾아보라는 것이다. 저자는 이것을 Brian
  Marick에게서 배운 것 같다고 적으며, **맥락 주도 테스터의 핵심 기량**으로 여기게 됐다고
  쓴다.
- **그리고 그 잣대를 상대에게 적용해 결론을 낸다** (§반례 셋).[^kaner2013-insapience]

  > Drawing sharp lines, condemning common and often-valuable testing activities as
  > non-testing or non-sapient, is completely out of step with this. It denies the
  > importance of "context" in "context-driven."

## 원문이 넘지 않은 선

**이 절은 이 소스가 지지하지 않는 사용을 미리 막는 자리다.**

- **측정이 없다.** 어느 어휘를 쓴 팀이 결함을 더 찾았다거나 손해를 봤다는 수치가 이 글에
  없다. 이 글은 **정의 대 정의의 논증**이고, 상대 쪽도 마찬가지다. **그러므로 이 모순
  쌍의 어느 극도 실증으로 인용될 수 없다.**
- **저자 자신이 같은 회의에서 물러선 자리를 적는다** — 퍼징에 대해 자기와 Doug Hoffman이
  박한 말을 했는데, 이어진 발표들이 단순한 오라클로도 값진 정보가 드러난 예를 여럿 보여
  주자 **자기들의 앞선 과잉 일반화 몇 가지에서 물러섰다**고 쓴다
  (§도입).[^kaner2013-insapience] 이 글의 저자가 자기 판단의 수정 가능성을 같은 글에서
  기록한다는 사실은, 이 글을 최종 심급으로 읽지 않을 근거다.
- **상대의 정의를 인용하지 않는다.** 이 글은 반대편의 주장을 자기 말로 요약해 다룬다
  (`According to the new doctrine…`, `some people assert that…`). 정의문을 직접 인용해
  대조하지 않으므로, **이 반박이 상대의 어느 판 정의를 겨냥한 것인지 문면으로는 확정되지
  않는다.** 시점으로 보면 이 글(2013-02-04)이 상대 글(2013-03-26)보다 앞서므로, 겨냥
  대상은 두 판 중 어느 쪽도 아닌 그 이전 어휘일 수 있다.
- **개인과 사업 동기를 지목하는 대목이 있다.** `might make good marketing for a few
  people`이 그것이다. 이 페이지는 그 문장을 논증이 아니라 **저자의 논평**으로 취급하고,
  판정의 근거로 쓰지 않는다.

## 이 반박에 걸린 모순

- **반대 극은 [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md)이다.**
  이 KB는 두 페이지를 `contradicts`로 묶어 **한 쌍으로 보존**한다. 어느 한쪽을 정설로
  세우지 않는다.
- **상대가 이 글에 직접 답한 기록이 있다.** 상대 글의 댓글에서 한 독자가 이 글의 URL과
  수동·자동 판정 문장을 그대로 붙여 묻자, James Bach가 답한다 — **우리는 실제로 정도의
  구분이 아니라 원칙의 구분을 말하고 있으며, 당신이 인용한 문장은 다른 것(체킹이 아니라
  도구가 뒷받침하는 테스팅)을 가리킨다**는 것이다. 그 문면과 locator는 상대 페이지의
  같은 절이 갖는다.
  - **그래서 모순의 축이 문면으로 확정된다 — 정도인가 원칙인가.** 이 글은 정도라 하고
    상대는 원칙이라 한다. 이 KB는 이 다툼을 해소하지 않는다. **양쪽 모두 실무자 저술이고
    측정이 없어 가릴 근거가 이 KB에 없다.**
- **ISTQB 계열의 반론은 이 모순의 상대가 아니다.** 그쪽 반박은 이 KB에 페이지가 없고,
  확보 대장이 그 축을 강등했다(일방 반박이고 개인 자격의 반론이라는 사유). 이름만
  적어 두고 여기서는 다루지 않는다.

## LLM 시대의 지위

이 절은 원 소스의 주장이 아니라 **이 KB의 읽기**다. 이 글은 2013년에 쓰였고 그 뒤
저자가 이 논지를 다시 잰 기록은 이 KB에 없다.

- #hypothesis **이 글의 논증 형태가 지금 그대로 되풀이된다.** "모델이 만든 테스트는
  진짜 테스트가 아니다"라는 주장은 이 글이 다룬 "자동 체크는 테스트가 아니다"와 같은
  꼴이고, 이 글의 답 — 무엇을 알고자 하는 물음이 있고 그 답을 얻으면 그것이 테스트다 —
  도 그대로 옮겨진다. **주체가 아니라 물음의 유무를 보라는 것이 이 글의 판정 기준이다.**
- #hypothesis **다만 이 글의 두 극단 논증 중 한쪽이 약해진다.** "모든 테스트는 수동이다"
  논증은 설계·코드 작성·기대값 제공·결과 해석을 사람이 한다는 열거에 기대는데, 그 항목들이
  하나씩 모델로 넘어가면 열거가 짧아진다. **이 글은 그 조건을 검토하지 않았다** — 2013년
  글에 그것을 요구할 수 없다.
- **이 페이지는 이 반박을 진리로 두지 않는다.** [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md)과
  한 쌍으로 보존되고, 자동화의 경계에 관한 주장은 **논쟁 지대**라는 것이 이 KB의 기록이다.

## 이어지는 페이지

- [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md) — 이 반박의 대상.
  이 페이지와 `contradicts`로 묶여 있다
- [일관성 오라클 휴리스틱](../concepts/consistency-oracle-heuristics.md) — 이 글이
  되묻기의 근거로 URL과 함께 지목한 카탈로그
- [테스트 오라클](../concepts/test-oracle.md) — 이 글이 말하는 "약한 오라클"과 "부분
  오라클"이 그 분류의 어디에 앉는가
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  아무리 많은 테스트를 돌려도 남는 비대칭. 고용량 자동화가 넘지 못하는 선
- [속성 기반 테스트](../concepts/property-based-testing.md) — 고용량 자동 테스팅의
  형식화된 갈래. 사람이 속성을 쓰고 기계가 입력을 만든다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 이 글이
  되묻기에 든 "오늘 동작이 지난달 동작과 같은가"를 실제로 재면 무엇이 남는가
- [코코넛은 통하지 않는다](../concepts/coconuts-dont-cut-it.md) — "보편 모범 사례는
  없다"는 같은 전제가 방법론 채택 쪽에서 되풀이되는 자리

[^kaner2013-insapience]: Kaner 2013, "The Insapience of Anti-Automationism",
    Context Driven Testing, 2013-02-04. 절 번호도 소제목도 없으므로 locator는 **문단
    역할**로 적었고(§도입 · §두 장면 · §hooey 문단 · §두 극단 불릿 · §수동·자동 판정 ·
    §사피엔스 재규정 · §체킹 문단 · §자동 체킹 문단 · §반대 진영 요약 · §되묻기 문단 ·
    §정도 규정 불릿 · §결론 문단 · §HiVAT 가치 · §맥락 전제 · §반례 셋), 규약의 정본은
    `it/archive/kaner2013-insapience/_progress.yaml` 머리말이다. **머리글에 저자
    이름이 없다** — `BY ADMIN`으로 나오고, 저자 귀속은 본문 1인칭과 댓글에 `Cem Kaner`
    이름으로 단 답글로 확정된다. 이 글은 kaner.com에 없어 확보처가 게시처와 AST 미러
    둘뿐이고, **두 미러의 본문은 동일하다**(본문만 추출한 sha256이 양쪽 같다 — 대조
    기록은 위 `_progress.yaml`). 댓글 9건과 사이트 내비게이션은 본문 밖이라 반입하지
    않았고, WTST 2013 발표 목록 일곱 항목의 세부도 회의 기록이라 옮기지 않았다.

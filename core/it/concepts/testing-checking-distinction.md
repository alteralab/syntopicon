---
type: concept
title: 테스팅과 체킹의 구분
description: 무엇이 자동화 가능한가를 낱말로 가른 실무자 선언 — 도구가 공정을 바꾼다는 관찰에서 출발해 테스팅과 체킹을 따로 정의하고 체킹만이 완전 자동화될 수 있다고 못 박는 자리, 같은 글의 2013년 판과 현행판에서 두 정의가 통째로 갈아끼워진 대조, 체킹을 사람·기계·사람기계 셋으로 나눈 갈래, 사람은 알고리즘을 체현하지 못한다는 사고 실험, 저자들이 스스로 긋지 않은 선, 그리고 이 구분 자체가 같은 학파 안에서 거짓 이분법이라고 반박받는 자리, 그리고 같은 선을 결정 가능성이 아니라 반복성과 비용으로 긋는 2021년 실무서 하나 — 기술을 향하는 테스트와 업무를 향하는 테스트로 가른 사분면과 그 분류가 프로덕션 이전 검증에 쏠려 있다는 자인, 도구가 익으면 자동화 쪽으로 움직이는 선, 그리고 그 책을 논쟁의 한 표로 세지 않은 이유, 그리고 같은 사분면을 가져오되 위쪽 반을 업무가 아니라 사용자를 향하는 것으로 적고 네 사분면을 번호로 세는 또 하나의 2차 경유
generated: { by: "claude-opus-5", at: "2026-09-18T20:00:00Z" }
contradicts: [testing-checking-false-dichotomy]
sources:
  - { id: bach2013-testing-checking-refined, resource: /it/sources/bach2013-testing-checking-refined.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
  - { id: dynowski2025, resource: /it/sources/dynowski2025.md }
---

# 테스팅과 체킹의 구분

- [이 소스의 지위 — 실무자 선언이지 학술 근거가 아니다](#이-소스의-지위--실무자-선언이지-학술-근거가-아니다)
- [왜 낱말을 갈랐는가](#왜-낱말을-갈랐는가)
- [두 낱말의 정의 — 현행판](#두-낱말의-정의--현행판)
- [정의가 바뀌었다 — 2013 판과의 대조](#정의가-바뀌었다--2013-판과의-대조)
- [정의에서 따라 나오는 것](#정의에서-따라-나오는-것)
- [사피엔스라는 낱말의 은퇴](#사피엔스라는-낱말의-은퇴)
- [체킹의 세 종류](#체킹의-세-종류)
- [사람은 알고리즘을 체현하지 못한다](#사람은-알고리즘을-체현하지-못한다)
- [원문이 넘지 않은 선](#원문이-넘지-않은-선)
- [이 구분에 걸린 모순](#이-구분에-걸린-모순)
- [같은 선을 경제로 긋는 소스 하나](#같은-선을-경제로-긋는-소스-하나)
- [LLM 시대의 지위](#llm-시대의-지위)
- [같은 사분면을 다른 축 이름으로 옮기는 소스 하나](#같은-사분면을-다른-축-이름으로-옮기는-소스-하나)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **테스팅 안에서 기계가 대신할 수 있는 부분과 그럴 수 없는 부분을 무엇이
가르는가.**

## 이 소스의 지위 — 실무자 선언이지 학술 근거가 아니다

이 페이지의 소스는 블로그 글 하나다. 측정도, 통제 실험도, 결과 표도 없다. **근거
등급은 실무자 선언(practitioner manifesto)이고, 이 페이지의 어떤 문장도 학술 실증으로
인용되지 않는다.** 지위는 저자들 자신의 규정으로 밝힌다.

- 저자가 이 글의 성격을 직접 적는다 (현행판 §댓글, Andrew Prentice 2013-03-31
  답글).[^bach2013-testing-checking-refined]

  > We will monitor the issue and adjust our definition further if we feel that there's
  > any widespread problem with this. Meanwhile, anyone is free to define these words in
  > their own way. We're not a law-making body. We are merely stating the protocol used
  > in the Rapid Software Testing methodology. And we are sharing our ideas in case
  > other people care what we think… and some people do.

- **그래서 이 구분은 관측된 사실이 아니라 한 방법론이 정한 어휘 규약이다.** 이 페이지가
  옮기는 것은 "테스팅과 체킹이 실제로 다르다"가 아니라 "Rapid Software Testing이 두
  낱말을 이렇게 쓴다"이다.

## 왜 낱말을 갈랐는가

- 출발점은 도구가 공정을 바꾼다는 관찰이다 — 저자들은 McLuhan을 인용해 **우리가 도구를
  빚고, 그 뒤로는 도구가 우리를 빚는다**는 문장을 앞세운다 (현행판
  §도입).[^bach2013-testing-checking-refined]
- **계기가 시대 조건으로 명시된다** — 제품과 플랫폼의 복잡성이 수십 년 늘어온 데 더해
  **즉시 배포되고 즉시 갱신되기를 기대받는 소프트웨어의 거대한 시장**이 생겼고, 이것이
  마이크로컴퓨터 등장 이후 테스팅이 맞은 가장 큰 도전이라고 적는다. 그리고 "지속적
  배포(continuous deployment)"라는 북소리가 그 전쟁의 새 전선을 열었다고 덧붙인다
  (현행판 §도입).[^bach2013-testing-checking-refined]
- **가름의 목적이 한 문장에 있다** (현행판 §Checking vs.
  Testing).[^bach2013-testing-checking-refined]

  > For this reason, in the Rapid Software Testing methodology, we distinguish between
  > aspects of the testing process that machines can do versus those that only skilled
  > humans can do. We have done this linguistically by adapting the ordinary English
  > word "checking" to refer to what tools can do.

- **모형은 프로그래밍과 컴파일링이다.** 프로그래밍은 사람이 하는 것이고 컴파일링은
  도구가 사람을 위해 하는 것인데, 컴파일러가 하는 일이 겉보기에는 기술적으로 프로그래머가
  하는 일과 똑같아 보일 수 있다고 적는다. 그러면서 **자동 프로그래밍이나 수동
  프로그래밍이라고 말하는 사람은 없다** — 일단 도구가 그 일을 하게 되면 다시는 그것을
  프로그래밍이라 부르지 않는다는 관찰을 붙인다 (현행판 §Checking vs.
  Testing).[^bach2013-testing-checking-refined]

## 두 낱말의 정의 — 현행판

정의는 번역하지 않고 그대로 옮긴다. 의미는 원문이 담고 한국어는 해설이다.

**테스팅(testing)** (현행판 §정의 블록).[^bach2013-testing-checking-refined]

> Testing is the process of evaluating a product by learning about it through
> experiencing, exploring, and experimenting, which includes to some degree:
> questioning, study, modeling, observation, inference, etc.

> (A test is an encounter with a product that comprises an instance of testing.)

**체킹(checking)** (현행판 §정의 블록).[^bach2013-testing-checking-refined]

> Checking is the mechanistic process of verifying propositions about the product.

> (A check is an instance of checking.)

설명 주석이 낱말 셋을 풀이한다 (현행판 §Checking vs.
Testing).[^bach2013-testing-checking-refined]

> "mechanistic" means algorithmic; that it can be expressed explicitly in a way that a
> machine could perform.

> "verifying" means ascertaining the factual status of. Quality is an opinion, not a
> fact, so quality cannot be verified. But lots of things about a product and its
> behavior can be settled as a matter of fact.

> "propositions" are statements about a product that may be true or false.

- **이 세 주석이 가름의 실질이다.** 체킹의 대상은 참·거짓이 정해질 수 있는 명제이고,
  품질은 의견이라 명제가 되지 못한다. 그러므로 **자동화의 경계는 도구의 성능이 아니라
  판정 대상이 명제인가 아닌가에 걸린다.**
- **같은 판 안에서 낱말이 한 번 갈린다.** 뒤쪽에서 정의를 다시 불러오는 자리는
  `mechanistic`이 아니라 **`mechanical`**로 적혀 있다 (현행판 §세 종류 블록
  직전).[^bach2013-testing-checking-refined] 설명 주석이 풀이하는 것은 `mechanistic`
  뿐이므로 이 페이지는 정의 블록 쪽을 정본으로 인용했다.

## 정의가 바뀌었다 — 2013 판과의 대조

**이 사실은 각주가 아니라 본문에 있어야 한다.** 이 글은 살아 있는 문서이고, 두 정의가
모두 통째로 갈아끼워졌다. 어느 정의를 인용하느냐에 따라 주장의 내용이 달라지므로
**판을 병기하지 않은 인용은 이 소스에서 성립하지 않는다.**

| | 2013 판 (2013-05-01 캡처) | 현행판 (2026-08-22 열람) |
|---|---|---|
| 테스팅 | `learning about it through experimentation` | `learning about it through experiencing, exploring, and experimenting` |
| 테스트 | `A test is an instance of testing.` | `A test is an encounter with a product that comprises an instance of testing.` |
| 체킹 | `the process of making evaluations by applying algorithmic decision rules to specific observations of a product` | `the mechanistic process of verifying propositions about the product` |

- 2013 판의 문면은 이쪽이다 (2013 판 §정의 블록).[^bach2013-testing-checking-refined]

  > Testing is the process of evaluating a product by learning about it through
  > experimentation, which includes to some degree: questioning, study, modeling,
  > observation and inference.

  > Checking is the process of making evaluations by applying algorithmic decision rules
  > to specific observations of a product.

- **2013 판의 설명 주석은 "관측이 비트 열이 된다"는 조건을 달고 있었다** (2013 판
  §Checking vs. Testing).[^bach2013-testing-checking-refined]

  > "specific observations" means that the observation process results in a string of
  > bits (otherwise, the algorithmic decision rules could not operate on them).

  현행판에는 이 주석이 없다. 비트 열이라는 조건이 빠지고 그 자리에 **참·거짓을 가릴 수
  있는 명제**가 들어앉았다.
- **교체 사실은 글 자신이 적지만, 교체 시점은 적지 않는다** (현행판 §갱신 주석
  2024-08-10).[^bach2013-testing-checking-refined]

  > Update, 2024-08-10: We simplified the definition of checking. Actually did this a
  > few years ago and forgot to update this article.

  - 그래서 이 글의 어느 시점 문면이 어느 정의를 담고 있었는지는 확정되지 않는다. 확정되는
    것은 **2013-05-01 캡처의 문면**과 **2026-08-22 열람 문면** 둘뿐이다.
  - 테스팅 정의의 `experiencing` 추가는 별도 주석이 날짜를 준다 — `Update, 2019-12-16`
    (현행판 §갱신 주석 2019-12-16).[^bach2013-testing-checking-refined]
  - **발행일 표기도 갈렸다.** 2013 판은 본문 끝에 *"This entry was posted on Tuesday,
    March 26th, 2013"*을 인쇄하는데, 현행판 머리글은 `PUBLISHED: AUGUST 10, 2024`라고
    적는다 (현행판 §도입 머리글).[^bach2013-testing-checking-refined] 최종 수정일이
    발행일 자리를 차지한 것이다.

## 정의에서 따라 나오는 것

저자들이 함의를 목록으로 정리한다 (현행판 §Checking vs.
Testing).[^bach2013-testing-checking-refined]

- **포함 관계가 한 방향이다** — 테스팅이 체킹을 감싸고 그 역은 성립하지 않는다.

  > Testing encompasses checking (if checking exists at all), whereas checking cannot
  > encompass testing.

  - 괄호 안의 단서(`if checking exists at all`)는 **2013 판에 없다.** 현행판이 더한
    것이고, 다음 함의와 짝을 이룬다.

  > Testing can exist without checking. A test can exist without a check. But checking
  > is a very popular and important part of ordinary testing, even very informal testing.

- **자동화 가능성이 두 낱말을 가르는 기준이다.**

  > Checking is a process that can, in principle be performed by a tool instead of a
  > human, whereas testing can only be supported by tools. Nevertheless, tools can be
  > used for much more than checking.

- **"자동화되어야 한다"가 아니라 "완전히 자동화될 수 있다"가 판정 기준이다** — 이 문장도
  현행판에서 새로 들어온 것이다.

  > We are not saying that a check MUST be automated. But the defining feature of a
  > check is that it can be COMPLETELY automated, whereas testing is intrinsically a
  > human activity.

- **체킹은 확인(confirming)과 같지 않다.** 체크는 회귀 테스트에서처럼 확인하는 쪽으로
  쓰이는 일이 많지만, 반증에 쓰이거나 넓은 공간을 무작위로 훑는 사변적 탐색에 쓰일 수도
  있다고 적는다.
- **단정(assertion)은 체크의 한 종류이지 체크와 같은 말이 아니다** — 모든 체크가 단정은
  아니고, 단정인 경우에도 그 단정 앞에 체크의 일부이되 단정의 일부는 아닌 코드가 있을 수
  있다.
- **가치 판단이 아니라는 단서가 붙는다.**

  > These definitions are not moral judgments. We're not saying that checking is an
  > inherently bad thing to do. On the contrary, checking may be very important to do.
  > We are asserting that for checking to be considered good, it must happen in the
  > context of a competent testing process. Checking is a tactic of testing.

## 사피엔스라는 낱말의 은퇴

- **이 글은 앞서 쓰던 어휘 하나를 스스로 폐기한다.** 사피엔트한(sapient) 공정이란
  적절히 숙련된 사람을 요구하는 공정이라고 규정해 왔는데, 몇 해 써 보니 **비사피엔트한
  공정이 멍청한 사람을 위한 멍청한 공정이라는 인상을 주지 않기가 거의 불가능**했다고
  적는다. 낱말이 지능처럼 들리기 때문이라는 것이다. 그래서 이 용어에 금시계를 주어
  은퇴시킨다고 쓴다 (현행판 §Whither
  Sapience?).[^bach2013-testing-checking-refined]
- **이 대목이 반박 쪽과 맞물린다.** [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md)가
  겨냥한 두 장면 중 하나가 바로 사피엔스 어휘의 유통이고, 그 반박은 이 글이 나오기
  일곱 주 앞선 2013-02-04에 쓰였다.

## 체킹의 세 종류

정의를 다시 불러온 뒤 셋으로 나눈다 (현행판 §세 종류
블록).[^bach2013-testing-checking-refined]

> Human checking is an attempted checking process wherein humans verify propositions
> without the mediation of tools.

> Machine checking is a checking process wherein tools verifiy propositions without the
> mediation of humans.

> Human/machine checking is an attempted checking process wherein both humans and tools
> cooperate to verify propositions about the product.

- **`verifiy`는 원문의 오식이다** — 현행판 문면 그대로 옮겼다. 2013 판에는 이 자리가
  다른 문장이라 오식이 없다.
- **사람 체킹에만 `attempted`가 붙는다.** 기계 체킹에는 붙지 않는다. 사람은 체크를
  온전히 수행하지 못한다는 다음 절의 논증이 이 낱말의 근거다.
- **세 정의 모두 어휘가 갈아끼워졌다.** 2013 판은 셋 다 `collect the observations and
  apply the rules`로 적혀 있었고, 현행판은 셋 다 `verify propositions`로 바뀌었다
  (2013 판·현행판 §세 종류 블록 대조).[^bach2013-testing-checking-refined] 위
  §정의가 바뀌었다의 교체가 이 세 갈래까지 일관되게 미친 자리다.
- **사람 체킹도 테스팅이다.** 저자들이 그 물음을 스스로 던지고 답한다 (현행판
  §Human Checking vs. Machine Checking).[^bach2013-testing-checking-refined]

  > You might also wonder why we don't just call human checking "testing." Well, we do.
  > Bear in mind that all this is happening within the sphere of testing. Human checking
  > is part of testing.

  다만 사람이 자기 사고를 체크의 울타리 안으로 명시적으로 제한하려 할 때 — 그 시도가
  완전히 성공하지 못하더라도 — 그것은 테스팅 활동 전체가 아니라 테스팅의 특정하고 제한된
  전술이므로 테스팅 안에서 자기 이름을 가질 자격이 있다고 적는다.

## 사람은 알고리즘을 체현하지 못한다

**이 절이 구분을 떠받치는 유일한 논증이다.** 그리고 그 논증은 사고 실험이지 측정이
아니다.

- **사람 체킹과 기계 체킹이 같을 수 없는 이유** — 사람은 명시적인 알고리즘 절차를
  *따르려 시도*하지만, 도구는 그 절차를 따르는 것이 아니라 **체현(embody)**한다. 사람은
  그런 알고리즘을 체현할 수 없다 (현행판 §Human Checking vs. Machine
  Checking).[^bach2013-testing-checking-refined]
- **증명으로 제시되는 사고 실험** — 누구에게든 지시 목록을 따르라고 하고 동의를 받은 뒤,
  그 지시를 결코 완수할 수 없게 만들어 보라는 것이다. 사람은 목마름이나 노출로 죽을
  때까지 그 자리에 앉아 있지 않고 스스로 멈추어 절차를 바꾸거나 빠져나간다. 그때 그
  사람이 **줄곧 자기가 따르기로 한 절차 이상의 것을 체현하고 있었음**이 확실해진다고
  적는다 (현행판 §Human Checking vs. Machine
  Checking).[^bach2013-testing-checking-refined]
- **외부 근거가 하나 걸린다** (현행판 §Human Checking vs. Machine
  Checking).[^bach2013-testing-checking-refined]

  > Humans can perform motivated actions; tools can only exhibit programmed behaviour
  > (see Harry Collins and Martin Kusch's brilliant book The Shape of Actions, for a
  > full explanation of why this is so).

  - **이 KB는 그 책을 반입하지 않았다.** 그러므로 위 명제는 이 글을 경유한 인용이고,
    근거의 무게는 이 글이 아니라 그 책에 있다. 이 페이지는 저자들이 그 책을 근거로
    지목했다는 사실까지만 적는다.
- **도구의 자리를 좁히지 않는다는 단서가 곧바로 붙는다** (현행판 §Human Checking vs.
  Machine Checking).[^bach2013-testing-checking-refined]

  > Please understand, a robust role for tools in testing must be embraced. … Tools can
  > help us in many ways far beyond the automation of checks. But in this, they
  > necessarily play a supporting role to skilled humans; and the unskilled use of tools
  > may have terrible consequences.

## 원문이 넘지 않은 선

**이 절은 이 소스가 지지하지 않는 사용을 미리 막는 자리다.**

- **효과를 잰 적이 없다.** 이 구분을 쓴 팀이 결함을 더 찾았다거나 비용이 줄었다는 측정이
  글 안에 없다. 이 글은 어휘 규약을 제안하고 그 이유를 설명할 뿐이다.
- **저자들 스스로 법이 아니라고 적었다** — 위 §이 소스의 지위가 인용한 `We're not a
  law-making body`가 그 자리다. 이 구분을 조직의 게이트나 심사 기준으로 옮기는 것은
  소스가 지지하는 사용이 아니다.
- **낱말을 갈랐을 뿐 도구를 낮추지 않았다.** 함의 목록의 `These definitions are not
  moral judgments`와 §Human Checking vs. Machine Checking의 `a robust role for tools
  in testing must be embraced`가 명시적 방어선이다. 그럼에도 이 구분이 반자동화
  구호로 유통됐다는 것이 반박 쪽의 관찰이고, 그것은 이 글이 통제하지 못한 결과다.
- **정의가 확정되지 않았다.** 두 정의가 통째로 갈아끼워졌고, 현행판 안에서도 체킹
  정의를 싣는 두 자리의 낱말이 갈린다(`mechanistic` ↔ `mechanical`).
  **이 구분을 인용할 때 판을 적지 않으면 어느 정의를 뜻하는지 알 수 없다.**

## 이 구분에 걸린 모순

- **반대 극은 같은 학파 안에 있다.** 맥락 주도 테스팅(context-driven testing)의 창시자
  가운데 한 사람인 Cem Kaner가 이 구분을 **또 하나의 거짓 이분법**이라고 적었다. 그 쪽은
  [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md)가 소유한다.
  - **둘은 같은 선언문에 이름을 올린 사이다.** 이 글의 저자 James Bach와 반박한 Cem
    Kaner는 [맥락 주도 테스팅의 일곱 원칙](../concepts/context-driven-testing-principles.md)의
    공저자이고, 그 부록의 학파 명단에도 나란히 적혀 있다. 그래서 이 모순은 학파의
    경계를 넘는 다툼이 아니라 **같은 선언문 서명자들 사이의 다툼**이다.
- **두 글은 서로를 안다.** Kaner의 글이 2013-02-04, 이 글이 2013-03-26이다. 그리고 이
  글의 댓글에서 한 독자가 Kaner의 문장을 URL과 함께 그대로 인용해 묻자, Bach가 직접
  답한다 (현행판 §댓글, Michael Leung 2013-04-10
  답글).[^bach2013-testing-checking-refined]

  > We *are* actually talking about a distinction of principle, and not one of degree.
  > The sentence you cite is a reference to something else, which is the idea of
  > tool-supported testing (not checking).

  - **이 답글이 모순을 문서 대 문서로 확정한다.** 인용된 문장은 Kaner 글의 수동·자동
    판정 문단이고, Bach는 그것이 자기 구분에 걸리지 않는다고 되받는다 — 원칙의 구분이지
    정도의 구분이 아니라는 것이다. **정도냐 원칙이냐가 이 모순의 축이다.**
  - 이 KB는 이 모순을 해소하지 않는다. 양쪽 모두 실무자 저술이고 측정이 없으므로,
    **어느 쪽이 옳은지를 가릴 근거가 이 KB에 없다.**
- **ISTQB 계열의 반론은 이 모순의 상대가 아니다.** 그쪽 반박은 이 KB에 페이지가 없고,
  확보 대장이 그 축을 강등했다(일방 반박이고 개인 자격의 반론이라는 사유). 이름만
  적어 두고 여기서는 다루지 않는다.

## 같은 선을 경제로 긋는 소스 하나

**이 논쟁을 모르는 채 같은 선을 긋는 실무서가 이 KB에 들어와 있다.** 2021년 마이크로서비스
실무서이고, 이 축의 원전이 아니라 **소비자**다. 여기 드는 이유는 그 책이 긋는 선의 성격이
위 두 극 가운데 어느 쪽에 가까운지가 분명하기 때문이다.

- **그 책은 테스트 분류에 사분면 하나를 가져온다** — Brian Marick이 낸 분류 체계를 Lisa
  Crispin과 Janet Gregory의 책에 실린 변형으로 옮긴 것이다
  (9장 §"Types of Tests", p.276).[^newman2021]
  - **아래쪽은 기술을 향하는(technology facing) 테스트다** — 애초에 체계를 만드는 개발자를
    돕는 테스트이고, 성능 테스트 같은 속성 테스트와 작은 범위의 단위 테스트가 여기 든다.
    **전부 통상 자동화돼 있다**고 적는다.
  - **위쪽은 업무를 향하는(business-facing) 테스트다** — 기술자가 아닌 이해관계자가 체계가
    어떻게 도는지를 이해하도록 돕는 테스트이고, 큰 범위의 종단 테스트(수용 테스팅 사분면)나
    **수동 테스팅**(탐색적 테스팅 사분면)이 여기 든다.
  - **저자가 이 분류에 붙이는 한계가 하나 있다** — 이 테스트들의 압도적 다수가 **프로덕션
    이전 검증(preproduction validation)**에 초점을 맞추고 있고, 프로덕션에 올라간 뒤의
    테스트가 이 그림에 들어올 자리가 없다는 것이다 (9장, p.276).[^newman2021] 그 자리의
    전문은 [프로덕션에서의 테스트](testing-in-production.md)에 있다.
- **그 책이 긋는 자동화의 선은 결정 가능성이 아니라 반복성과 비용이다** (9장 §"Manual
  Exploratory Testing", p.277):[^newman2021]

  > Automation is about removing repetitive tasks to free up humans to do the more creative,
  > ad hoc activities.

  - 그리고 수동 테스팅이 **필수적인 자리**로 드는 것도 결정 가능성이 아니다 — **자동 테스트를
    구현하는 것이 실행 불가능한 상황**, 이를테면 그 테스트를 쓰는 비용 때문일 때다
    (9장, p.277).[^newman2021]
- **그래서 그 선이 도구에 따라 움직인다.** 어떤 것이 어떻게 보이는지를 확인하는 일처럼 예전에는
  수동 탐색적 테스팅에만 있던 작업이, **시각적 단정을 가능하게 하는 도구가 익으면서** 자동화
  쪽으로 옮겨 오기 시작했다고 적는다 (9장, p.277).[^newman2021]
  - **위 [정의에서 따라 나오는 것](#정의에서-따라-나오는-것)의 선과 성격이 다르다.** 이 글의
    선은 **판정 대상이 참·거짓이 정해질 수 있는 명제인가**에 걸려 있어 도구가 좋아져도
    움직이지 않는다. 그 책의 선은 **도구가 익으면 움직인다.**
  - **그래서 그 책은 모순 쌍의 상대편에 가깝다.** 자동화의 경계가 원칙이 아니라 정도라는
    쪽이 [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md)의
    주장이고, 도구로 움직이는 선은 그 주장과 같은 방향이다. **다만 그 책은 이 논쟁을 알지
    못하고 어느 쪽 편도 들지 않는다** — 두 글 어느 것도 인용하지 않고 체킹이라는 낱말을
    쓰지도 않는다. **이 KB는 그 책을 논쟁의 한 표로 세지 않는다.** 모순 쌍에 새 상대를
    더하지 않았다.
- **자동화가 수동 테스팅을 없애라는 뜻이 아니라는 조항도 있다** (9장, p.277).[^newman2021]
  시각 단정의 자동화를 **수동 테스팅을 아예 없앨 이유로 보지 말고, 테스터의 시간을 덜
  반복적인 탐색적(exploratory) 테스팅으로 풀어 줄 기회로 보라**고 적는다.
- **탐색적 테스팅의 규정은 발견이다** (9장, p.277).[^newman2021] 잘 해내면 대체로 발견의
  일이고, **최종 사용자로서 애플리케이션을 탐색할 시간을 따로 떼어 두면** 그러지 않으면
  드러나지 않았을 문제를 캐낼 수 있다고 적는다.
- **조직 쪽 관찰 하나** — 모놀리스에서 마이크로서비스로 옮겨 가는 것 자체는 탐색적 테스팅에
  미치는 영향이 적고, 달라지는 것은 **조직의 이동**이다. 사용자 인터페이스가 팀 경계를 따라
  쪼개지면 **수동 테스팅의 소유권도 바뀔 수 있다** (9장, p.277).[^newman2021]
- **채택 순서에 대한 조문 하나** — 지금 수동 테스팅을 대량으로 하고 있다면 마이크로서비스
  길을 멀리 가기 전에 그것부터 손보라고 적는다. **소프트웨어를 빠르고 효율적으로 검증할 수
  없으면 마이크로서비스의 이득을 많이 얻지 못하기 때문**이다 (9장, p.277).[^newman2021]
  같은 축의 다른 조건들은
  [마이크로서비스의 고통과 채택 판단](../concepts/microservice-pain-points-and-adoption.md)에
  있다.
- **이 소스에 잰 값이 없다.** 도구가 익었다는 관찰도, 자동화 쪽으로 추세가 기울었다는 서술도
  분모 없는 실무 진술이다.

## LLM 시대의 지위

이 절은 원 소스의 주장이 아니라 **이 KB의 읽기**다. 이 글은 2013년에 쓰였고 현행판의
마지막 갱신은 2024-08-10이며, 저자들이 생성 모델을 언급한 대목은 문면에 없다.

- #hypothesis **모델이 자동화하는 것은 이 정의로 보면 체킹 쪽 산출물이다.** 생성된
  단위 테스트가 하는 일은 관측을 모아 명제의 참·거짓을 가리는 것이고, 그것이 체킹의
  정의에 그대로 들어맞는다. 산출물의 이름이 "테스트"라는 사실은 이 판정을 바꾸지 않는다 —
  저자들 스스로 그 이름 사용을 부정한다 (2013 판 §댓글, Eric Jacobson 2013-04-04
  답글).[^bach2013-testing-checking-refined]

  > There is no such thing as automated testing. Testing cannot be automated. Testing
  > can be supported with tools, of course, just as scientists use tools to help their
  > work.

- #hypothesis **그러나 이 구분의 경계선이 모델 앞에서 그대로 서는지는 이 글이 답하지
  않는다.** §사람은 알고리즘을 체현하지 못한다의 논증은 "도구는 프로그램된 행동만
  보인다"에 걸려 있는데, 그 전제를 어떤 도구까지 지탱하는지가 이 글에서 검토된 적이 없다.
  근거가 되는 책도 이 KB에 없다.
- #hypothesis **정의가 2024년에 다시 손질됐다는 사실 자체가 시대 압력의 자국이다.**
  체킹 정의에서 "비트 열"이라는 구현 조건이 빠지고 "참·거짓을 가릴 수 있는 명제"라는
  더 추상적인 조건이 들어왔다. 이 방향의 손질은 판정 대상을 도구의 형태에서 떼어 내므로,
  도구가 바뀌어도 정의가 살아남는다. **다만 저자들이 그 이유를 적지는 않았다** — 갱신
  주석은 "단순화했다"고만 말한다.
- **이 페이지는 이 구분을 진리로 두지 않는다.** [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md)와
  한 쌍으로 보존되고, 자동화의 경계에 관한 주장은 **논쟁 지대**라는 것이 이 KB의 기록이다.

## 같은 사분면을 다른 축 이름으로 옮기는 소스 하나

**위 절이 든 사분면을 2025년 API 스타일 비교서도 가져오는데, 축 이름이 다르다.** 이 소스 역시
이 축의 원전이 아니라 소비자이고, 여기 드는 이유는 **두 2차 경유가 같은 도판을 서로 다르게
옮긴다는 사실 자체**가 이 KB의 사분면 서술을 어느 선까지 믿을 것인지를 정하기 때문이다
(1장 §"Agile testing quadrants", pp.28–30).[^dynowski2025]

- **이 소스가 적는 두 축** — **가로축은 팀 지원(team support)에서 제품 비평(product critique)까지,
  세로축은 사용자를 향함(user-facing)과 기술을 향함(technology-facing)**이다
  (1장, p.28).[^dynowski2025]
- **위 소스가 적는 축과 한 낱말이 다르다.** 그쪽의 위쪽 반은 **업무를 향하는(business-facing)**
  테스트이고 이쪽의 위쪽 반은 **사용자를 향하는(user-facing)** 테스트다. **이 KB는 어느 쪽이
  원전의 표기인지 확인하지 않았다** — 두 책 모두 2차 경유이고, 이 KB에는 Marick의 분류도
  Crispin & Gregory의 책도 들어와 있지 않다. 그래서 **둘 중 하나를 고르지 않고 둘 다 그대로
  적어 둔다.**
- **네 사분면의 책임을 이 소스는 번호로 적는다** (1장, pp.29–30):[^dynowski2025]
  - **Q1** — 기술에 초점을 두고 **개발 팀을 지원**한다. 단위 테스트와 컴포넌트 테스트가 전형적으로
    개발자가 쓰고 자동화한다. 빠르게 돌아 **즉각적인 피드백**을 주고 개발자의 관심을 끈다.
  - **Q2** — **소프트웨어 사용자의 시점**에서 접근하며 개발 팀을 지원한다. 체계 기능에 초점을 두고
    체계가 사용자 목표를 충족하는지 확인한다. **테스트 자동화가 실행 가능하지 않을 때는 수동
    테스트를 고려**해야 한다.
  - **Q3** — **사용자에 초점**을 두고 제품을 비평한다. 개발 중에 놓친 문제를 찾도록 설계되고,
    사용자 수용 테스트(UAT)가 여기서 흔히 수행된다. **UAT가 자주 수동으로 수행된다는 단점**이 있다.
  - **Q4** — **기술에 초점**을 두고 제품을 비평한다. 기술적인 성격이고 **보안과 성능 같은 비기능
    요건에 집중**하며, 전용 도구가 필요할 때가 많다.
- **두 짝으로 묶어 읽는 대목이 이 소스에만 있다** — **Q1과 Q2는 제품이 기능 요건대로 지어지도록
  개발 과정을 지원하고, Q3과 Q4는 제품이 사용자 필요를 만족하고 비기능 요건을 충족하는지 평가하는
  데 집중한다.** 그래서 이 사분면이 **소프트웨어 품질과 유지보수성으로 이끄는 테스트의 면들을 덮는
  로드맵** 구실을 한다 (1장, p.30).[^dynowski2025]
- **자동화의 선에 대해서는 이 소스가 아무 말도 하지 않는다.** 위 절이 든 소스는 자동화 경계가
  **반복성과 비용**에 걸려 있고 도구가 익으면 움직인다고 적었지만, 이 소스는 **Q2의 자동화가
  "실행 가능하지 않을 때"와 Q3의 UAT가 "자주 수동"이라는 사실 진술**에 그친다. 그래서 **이
  소스도 이 페이지의 모순 쌍에 새 표를 더하지 않는다.** 체킹이라는 낱말을 쓰지 않고 두 글 어느
  것도 인용하지 않는다.
- **이 소스는 사분면에 한계를 달지 않는다.** 위 절이 든 소스는 **이 테스트들 대부분이 프로덕션
  이전 검증에 초점을 맞춘다**는 한계를 적었는데, 이쪽은 그 말을 하지 않는다 — 대신 같은 장의
  배포 절에서 스테이징이 프로덕션이 아니라는 인용을 따로 든다. 그 자리는
  [프로덕션에서의 테스트](testing-in-production.md)가 갖는다.

## 이어지는 페이지

- [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md) — 이 구분의
  반대 극. 같은 학파 안에서 나온 반박이고, 이 페이지와 `contradicts`로 묶여 있다
- [일관성 오라클 휴리스틱](../concepts/consistency-oracle-heuristics.md) — 같은 두 저자가 세운
  오라클 카탈로그. 반박 쪽이 그 목록을 "사피엔트 테스팅도 결국 체킹"이라는 논거로 쓴다
- [테스트 오라클](../concepts/test-oracle.md) — 판정의 근거를 네 출처로 가른 이론 정본. 체킹이
  요구하는 "명제"가 그 분류의 어디서 오는가가 이 축과 만나는 자리
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) — 체킹이 전부
  통과했을 때 무엇이 증명되지 않는가
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) — 모델이
  만든 산출물이 이 정의로는 체킹인데, 그 체킹이 어디서 얼마나 틀리는가의 실측
- [속성 기반 테스트](../concepts/property-based-testing.md) — 기대를 사례가 아니라 속성으로 적는
  갈래. 이 구분의 어휘로는 명제를 사람이 쓰고 관측을 기계가 모으는 자리다
- [맥락 주도 테스팅의 일곱 원칙](../concepts/context-driven-testing-principles.md) — 이 글의
  저자 둘이 십 년 전 서명한 학파 선언. 이 구분을 보편 규칙으로 읽지 말라는 조항이 거기 있다
- [버그 옹호](../concepts/bug-advocacy.md) — 같은 저자 둘이 참여한 2002년 책의 4장. 체크가
  명제의 참·거짓을 가린 뒤에도 그것이 고쳐질 값어치가 있는가는 이 글의 어휘로는 명제가
  아니라 의견이고, 그 자리에서 무엇을 하는가가 그 페이지의 물음이다
- [코코넛은 통하지 않는다](../concepts/coconuts-dont-cut-it.md) — 형식만 옮겨 오는 채택의 실패.
  이 구분이 어휘 규약을 넘어 구호로 유통될 때 걸리는 진단
- [테스팅에서 자동화의 경계](../synthesis/automation-boundary-in-testing.md) — 이 갈래의 허브

[^bach2013-testing-checking-refined]: Bach & Bolton 2013, "Testing and Checking
    Refined", James Bach's Blog. **판이 둘인 살아 있는 문서다** — 이 페이지의 인용은
    `2013 판`(Wayback 캡처, 확보 대장 기록 2013-05-01)과 `현행판`(satisfice.com,
    2026-08-22 열람)을 locator 앞에 반드시 병기한다. 절 번호가 없으므로 locator는
    소제목(§Checking vs. Testing · §Whither Sapience? · §Human Checking vs. Machine
    Checking)이나 문단 역할(§도입 · §정의 블록 · §세 종류 블록 · §갱신 주석 <날짜>)로
    적었고, 규약의 정본은
    `it/archive/bach2013-testing-checking-refined/_progress.yaml` 머리말이다. 스냅샷에
    함께 보존된 댓글(2013 판 49건 · 현행판 67건)은 본문 밖이라 반입하지 않았다 — 예외로
    인용한 세 대목은 전부 **Bach 본인의 답글**이고 `§댓글(<작성자> <날짜> 답글)`로
    표시했다. 본문의 도해 이미지는 문면으로 옮길 수 없어 담지 않았다.

[^newman2021]: Newman 2021, *Building Microservices* 2판(O'Reilly, 2021) 9장 "Testing"
    §"Types of Tests"(pp.276–277) · §"Manual Exploratory Testing"(p.277). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은
    따옴표는 곧은 따옴표로 옮겼다. **사분면 자체는 도판(Figure 9-1)이라 옮기지 않았다** —
    본문이 그 도판에 대해 적는 것(아래위 두 반이 무엇을 가르는가, 어느 사분면에 무엇이
    드는가)만 산문으로 남겼고 그림 안의 글자는 인용하지 않았다. 이 절들에 코드 목록은 없다.
    저자가 가리키는 바깥 서지(Brian Marick의 분류와 Lisa Crispin & Janet Gregory
    *Agile Testing*)는 이 KB가 확인한 원전이 아니라 **이 책을 통한 2차 경유**다.
    **이 소스는 이 축의 원전이 아니라 소비자**이고, 위 모순 쌍의 어느 쪽 편도 들지 않는다.

[^dynowski2025]: Dynowski & Dulak 2025, *Learning API Styles* 초판(O'Reilly, 2025) 1장
    "API Concepts" §"API Lifecycle" 안의 §"Testing" 하위 §"Agile testing
    quadrants"(pp.28–30)에서만 왔고, 위 "같은 사분면을 다른 축 이름으로 옮기는 소스 하나" 절이
    그 전부다. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 28, 실측). 이 절에 직인용과 코드 목록은 없다.
    **사분면 자체는 도판(그림 1-8)이라 옮기지 않았다** — `pdftoppm`으로 렌더해 눈으로 대조했고,
    본문이 그 도판에 대해 적는 것(두 축의 이름, 사분면 넷의 책임, 두 짝으로 묶는 읽기)만 남겼다.
    그림 안 각 칸의 테스트 종류 목록은 [API 수명 주기](../concepts/api-lifecycle.md)가 갖는다.
    저자들이 가리키는 바깥 서지는 이 소스에 명시되지 않았고, **이 소스 역시 이 축의 원전이 아니라
    소비자**이며 위 모순 쌍의 어느 쪽 편도 들지 않는다.

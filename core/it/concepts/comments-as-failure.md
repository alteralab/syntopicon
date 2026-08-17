---
type: concept
title: 주석은 실패다
description: 주석을 필요악으로 규정하고 코드로 대체하기를 처방하는 장 — "주석은 언제나 실패다"라는 조문과 그 근거(주석은 거짓말한다·유지될 수 없다), 진실은 코드 한 곳에만 있다는 인식론, 나쁜 코드를 주석으로 벌충하지 말라는 처방, 그럼에도 정당하다고 인정되는 좋은 주석 여덟 종, 그리고 이 조문이 "주석 없이는 추상이 성립하지 않는다"는 쪽과 정면으로 갈리는 자리 — 두 저자가 서로를 지명해 반박한 드문 사례
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
contradicts: [why-write-comments]
sources:
  - { id: martin2008, resource: /it/sources/martin2008.md }
  - { id: ousterhout2021, resource: /it/sources/ousterhout2021.md }
  - { id: ousterhout2024-aposd, resource: /it/sources/ousterhout2024-aposd.md }
---

# 주석은 실패다

- [조문](#조문)
- [왜 주석에 부정적인가 — 주석은 거짓말한다](#왜-주석에-부정적인가--주석은-거짓말한다)
- [진실은 한 곳에만 있다](#진실은-한-곳에만-있다)
- [주석은 나쁜 코드를 벌충하지 못한다](#주석은-나쁜-코드를-벌충하지-못한다)
- [코드로 설명하라](#코드로-설명하라)
- [그럼에도 좋다고 인정되는 주석들](#그럼에도-좋다고-인정되는-주석들)
- [나쁜 주석](#나쁜-주석)
- [17장이 이 장을 다섯 항목으로 압축한다](#17장이-이-장을-다섯-항목으로-압축한다)
- [모순 — 주석이 담는 정보를 코드가 담을 수 있는가](#모순--주석이-담는-정보를-코드가-담을-수-있는가)
- [저자가 대담에서 밝힌 동기와 좁힌 범위](#저자가-대담에서-밝힌-동기와-좁힌-범위)
- [인용 대조 — 상대가 옮긴 문구와 원문의 차이](#인용-대조--상대가-옮긴-문구와-원문의-차이)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **주석은 무엇의 징표이며, 쓰지 않는 것이 왜 목표가 되는가.**

> **이 페이지의 소스는 논쟁 중인 소스다.** 반입 지위와 그 근거는
> [소스 메타](../sources/martin2008.md)가 정본이다. 이 장의 주장은
> [주석을 왜 쓰는가](why-write-comments.md)와 **정면으로 갈린다** — 두 페이지를 함께
> 읽지 않으면 어느 쪽도 제대로 읽은 것이 아니다.

## 조문

장은 Kernighan과 Plaugher의 제사로 열린다 — **"나쁜 코드에 주석을 달지 마라 — 다시
써라"** (4장 제사, p.53).[^martin2008] 그리고 도입 문단이 조문을 세운다 (4장 도입,
pp.53–54):[^martin2008]

> Comments are not like Schindler's List. They are not "pure good." Indeed, comments
> are, at best, a necessary evil. If our programming languages were expressive enough,
> or if we had the talent to subtly wield those languages to express our intent, we would
> not need comments very much—perhaps not at all.

그리고 이 장에서 가장 많이 인용되는 두 문장이 이어진다 (4장 도입, p.54):[^martin2008]

> The proper use of comments is to compensate for our failure to express ourself in
> code. Note that I used the word *failure*. I meant it. Comments are always failures.
> We must have them because we cannot always figure out how to express ourselves without
> them, but their use is not a cause for celebration.

- 그리고 정서적 처방이 붙는다 — **코드로 자신을 표현할 때마다 당신은 스스로의 등을
  두드려 주어야 한다. 주석을 쓸 때마다 당신은 얼굴을 찡그리고 자기 표현 능력의 실패를
  느껴야 한다** (4장 도입, p.54).[^martin2008]
  - **상대 소스가 이 문장을 문화 문제로 지목한다** — 아래
    [모순](#모순--주석이-담는-정보를-코드가-담을-수-있는가) 절의 반박 ③이 그 자리다.

## 왜 주석에 부정적인가 — 주석은 거짓말한다

- 근거 (4장 도입, p.54):[^martin2008]

> Why am I so down on comments? Because they lie. Not always, and not intentionally, but
> too often. The older a comment is, and the farther away it is from the code it
> describes, the more likely it is to be just plain wrong. The reason is simple.
> Programmers can't realistically maintain them.

- 기제 — **코드는 바뀌고 진화한다. 그 덩어리들이 여기서 저기로 옮겨 간다. … 불행히도
  주석은 언제나 그것을 따라가지 못하고 — 따라갈 수 *없고* — 너무 자주 주석은 자신이
  서술하던 코드에서 떨어져 나와 정확도가 계속 줄어드는 고아 조각이 된다** (4장 도입,
  p.54).[^martin2008] 실물로 `HTTP_DATE_REGEXP` 상수와 그 설명 주석 사이에 나중에 추가된
  인스턴스 변수들이 끼어든 FitNesse 코드를 든다.
- **규율로 풀자는 반론을 저자가 먼저 제기하고 기각한다** — **프로그래머가 주석을 잘
  고쳐진 상태로 유지할 만큼 충분히 규율 있어야 한다고 주장할 수는 있다. 동의한다, 그래야
  한다. 그러나 나는 그 에너지가 애초에 주석이 필요 없도록 코드를 명확하고 표현력 있게
  만드는 데 가기를 바란다** (4장 도입, p.54).[^martin2008]
  - **이 문장이 이 장의 논증 구조를 드러낸다.** 주석이 낡는다는 사실에서 주석을 쓰지
    말라는 처방으로 가는 다리가 "에너지 배분"이다. 상대 소스는 같은 사실을 인정하면서
    다른 처방(코드를 고칠 때 주석을 같이 고치라)으로 간다 —
    [기존 코드를 수정할 때](modifying-existing-code.md)가 그 자리다.
- **부정확한 주석은 주석이 없는 것보다 훨씬 나쁘다. 그것은 현혹하고 오도한다. 그것은
  결코 채워지지 않을 기대를 세운다** (4장 도입, p.54).[^martin2008]

## 진실은 한 곳에만 있다

- 인식론적 전제가 명시된다 (4장 도입, p.54):[^martin2008]

> Truth can only be found in one place: the code. Only the code can truly tell you what
> it does. It is the only source of truly accurate information. Therefore, though
> comments are sometimes necessary, we will expend significant energy to minimize them.

  - **이 전제가 모순의 뿌리다.** 상대 소스는 정확히 이 전제를 부정한다 — 코드가 담을 수
    없는 정보가 있고 그것이 인터페이스의 비형식적 부분이라는 것이 상대의 출발점이다.

## 주석은 나쁜 코드를 벌충하지 못한다

- **주석을 쓰는 더 흔한 동기 하나는 나쁜 코드다. 우리는 모듈을 하나 쓰고 그것이
  혼란스럽고 어수선하다는 것을 안다. 엉망이라는 것을 안다. 그래서 우리는 스스로에게
  말한다, "오, 저기에 주석을 달아야겠군!" 아니다! 당신은 그것을 청소해야 한다!** (4장
  §"Comments Do Not Make Up for Bad Code", p.55).[^martin2008]
- **주석이 적은 명확하고 표현력 있는 코드가 주석이 많은 어수선하고 복잡한 코드보다 훨씬
  낫다** (4장 §"Comments Do Not Make Up for Bad Code", p.55).[^martin2008]
  - 이 명제 자체는 상대 소스도 동의한다. 갈리는 것은 "주석이 적은"이 목표가 되는가다.

## 코드로 설명하라

- 처방의 실물 — 주석 `// Check to see if the employee is eligible for full benefits`와
  플래그 검사 코드 대신 `if (employee.isEligibleForFullBenefits())`를 쓰라는 것이다
  (4장 §"Explain Yourself in Code", p.55).[^martin2008]
- **당신 의도의 대부분을 코드로 설명하는 데는 몇 초의 생각이면 된다. 많은 경우 그것은
  그저 당신이 쓰고 싶은 주석과 같은 말을 하는 함수를 만드는 문제일 뿐이다** (4장
  §"Explain Yourself in Code", p.55).[^martin2008]
  - **이 처방이 [작은 함수](small-functions.md)와 맞물린다** — 주석을 없애는 수단이
    함수 추출이므로, 주석 규칙이 함수 크기 규칙의 생산 경로가 된다. 상대 소스가 지목하는
    귀결이 정확히 이 연결이다.

## 그럼에도 좋다고 인정되는 주석들

**이 절을 빼고 읽으면 이 장은 실제보다 극단적이 된다.** 저자는 정당한 주석 여덟 종을
든다 — 다만 단서를 먼저 단다: **명심할 것은, 유일하게 진짜 좋은 주석은 당신이 쓰지 않을
방법을 찾아낸 주석이라는 점이다** (4장 §"Good Comments", p.55).[^martin2008]

| 종류 | 무엇 | 쪽 |
|---|---|---|
| 법적 주석(Legal) | 저작권·라이선스 고지 | p.55 |
| 정보 제공(Informative) | 정규식이 무엇과 맞는지 등. 단 **가능하면 함수 이름으로 옮기는 편이 낫다** | p.56 |
| 의도 설명(Explanation of Intent) | 구현 정보를 넘어 결정의 **이유**를 남긴다 | p.56 |
| 명료화(Clarification) | 바꿀 수 없는 표준 라이브러리 인수·반환값의 뜻을 옮긴다 | p.57 |
| 결과 경고(Warning of Consequences) | `SimpleDateFormat`이 스레드 안전하지 않다는 경고 등 | p.58 |
| TODO | 지금 못 하는 일의 표시. **나쁜 코드를 남겨 두는 핑계는 아니다** | pp.58–59 |
| 강조(Amplification) | 사소해 보이는 것의 중요성을 키운다(`trim`이 중요하다) | p.59 |
| 공개 API의 Javadoc | **공개 API를 쓴다면 그것을 위한 좋은 Javadoc을 반드시 써야 한다** | p.59 |

- 명료화 주석에는 저자가 위험을 함께 적는다 — **물론 명료화 주석이 틀릴 실질적 위험이
  있다. … 이것이 왜 명료화가 필요한지와 왜 그것이 위험한지를 둘 다 설명한다** (4장
  §"Clarification", p.57).[^martin2008]
- 공개 API 항목에도 단서가 붙는다 — **그러나 이 장의 나머지 조언을 명심하라. Javadoc은
  다른 어떤 종류의 주석만큼이나 오도하고, 비국소적이고, 부정직할 수 있다** (4장
  §"Javadocs in Public APIs", p.59).[^martin2008]
  - **공개 API 항목이 모순의 범위를 좁힌다.** 이 소스도 공개 API의 인터페이스 문서화는
    요구한다. 갈리는 것은 **모든** 메서드에 인터페이스 주석이 필요한가다 — 아래
    모순 절이 그 명제로 좁혀 놓는다.

## 나쁜 주석

- 범주의 크기가 먼저 규정된다 — **대부분의 주석이 이 범주에 든다. 보통 그것들은 형편없는
  코드에 대한 목발이거나 변명이거나 불충분한 결정에 대한 정당화이며, 프로그래머가
  자기 자신에게 말하는 것에 지나지 않는다** (4장 §"Bad Comments", p.60).[^martin2008]
- 항목들 — 중얼거림(Mumbling), 중복 주석(Redundant Comments), 오도하는 주석
  (Misleading Comments), 의무적 주석(Mandated Comments), 일지 주석(Journal Comments),
  잡음 주석(Noise Comments) 등이 이어진다 (4장 §"Bad Comments", pp.60–64).[^martin2008]
- 중복 주석의 진단 — **그 주석은 아마 코드 자체보다 읽는 데 더 오래 걸릴 것이다** (4장
  §"Redundant Comments", p.60).[^martin2008]
- 일지 주석은 원인이 사라졌다고 본다 — **오늘날에는 소스 코드 관리 시스템이 있으므로
  이 긴 일지는 완전히 제거되어야 한다** (4장 §"Journal Comments", p.64).[^martin2008]
  - **이 판정은 상대 소스와 갈리지 않는다.** 코드를 되풀이하는 주석에 대해서는 이 KB의
    세 소스가 모두 같은 판정을 내린다 —
    [주석은 코드에서 뻔하지 않은 것을 서술한다](comments-describe-the-nonobvious.md)의
    붉은 깃발이 그 합의 자리다.

## 17장이 이 장을 다섯 항목으로 압축한다

같은 소스 17장이 주석 관련 냄새를 `C1`–`C5`로 조문화한다 (17장, pp.286–287):[^martin2008]

- `C1` **Inappropriate Information** — **변경 이력 같은 것은 그저 소스 파일을 방대한
  역사적이고 흥미롭지 않은 텍스트로 어지럽힌다. 일반적으로 저자·최종 수정일·SPR 번호
  같은 메타데이터는 주석에 나타나서는 안 된다**
- `C2` **Obsolete Comment** — **주석은 빨리 낡는다. 낡을 주석을 아예 쓰지 않는 것이
  최선이다**
- `C3` **Redundant Comment** — **주석은 코드가 스스로 말할 수 없는 것을 말해야 한다**
- `C4` **Poorly Written Comment** — **쓸 가치가 있는 주석은 잘 쓸 가치가 있다**
- `C5` **Commented-Out Code** — **주석 처리된 코드는 혐오스러운 것이다. … 주석 처리된
  코드를 보면 지워라!**

`C2`가 `C4`와 함께 놓이는 방식에 유의할 것 — 낡을 주석을 쓰지 말라면서 쓸 거면 잘 쓰라고
한다. 이 장의 태도가 금지가 아니라 **억제**임을 보여 주는 자리다.

## 모순 — 주석이 담는 정보를 코드가 담을 수 있는가

이 KB에서 **`contradicts`가 발화한 셋째 자리이자, 양쪽 저자가 서로를 지명해 반박한
유일한 자리다.** 상대는 [주석을 왜 쓰는가](why-write-comments.md)이고, 갈리는 명제는
하나다 — **주석이 제공하는 정보를 코드가 담을 수 있는가.**

- **이 페이지의 주장.** 진실은 코드 한 곳에만 있고(위
  [진실은 한 곳에만 있다](#진실은-한-곳에만-있다)), 주석의 올바른 쓰임은 코드로
  표현하지 못한 실패를 벌충하는 것이며, 주석은 **언제나** 실패다.
- **상대 쪽의 주장.** 상대는 이 문단을 통째로 인용한 뒤 조목별로 반박한다.
  - 반박 ① 정보의 종류가 다르다 — **주석이 제공하는 정보는 코드가 제공하는 것과 상당히
    다르고, 이 정보는 오늘날 코드로 표현될 수 없다** (12장 §12.6,
    p.100).[^ousterhout2021]
  - 반박 ② 목적이 정반대다 — **주석의 목적 중 하나는 코드를 읽는 것을 불필요하게 만드는
    것이다 … 마틴은 반대 방침을 취한다: 그는 주석을 코드로 대체하기를 옹호한다** (12장
    §12.6, p.100).[^ousterhout2021]
  - 반박 ③ 문화에 대한 우려 — **나는 마틴의 철학이 프로그래머에게 나쁜 태도를 조장할까
    걱정한다. 실패자처럼 보이지 않으려고 주석을 피하는 태도 말이다** (12장 §12.6,
    p.100).[^ousterhout2021] 위 [조문](#조문) 절의 "얼굴을 찡그리고 실패를 느껴라"가
    이 우려의 대상이다.
- **상대가 이 페이지의 처방이 낳는 산물을 반례로 든다** — 블록을 별도 메서드로 뽑고 그
  이름을 주석 대신 쓰는 방식이 `isLeastRelevantMultipleOfNextLargerPrimeFactor` 같은 긴
  이름을 낳으며, **이 모든 낱말을 쓰고도 이런 이름은 알아보기 어렵고 잘 쓴 주석보다 적은
  정보를 준다** (12장 §12.6, p.100).[^ousterhout2021] 이 페이지의
  [서술적인 이름](small-functions.md#서술적인-이름을-쓰라) 절이 **긴 서술적 이름이 긴
  서술적 주석보다 낫다**고 못 박은 바로 그 명제가 상대의 반례다.
- **층위 차이로 무마할 수 없는 이유 셋.**
  - **두 저자가 서로를 지명한다.** 상대가 이 소스를 저자명·서명으로 인용해 한 절
    (§12.6 "Comments Belong in the Code, Not the Commit Log"에 이어지는 반대 의견 절)을
    통째로 할애해 반박한다. 다른 것을 겨냥한 것이 아니다.
  - **같은 대상에 대한 반대 처방이다.** 이 페이지는 주석의 수를 최소화하라 하고, 상대는
    **모든** 메서드에 인터페이스 주석을 요구한다. 한쪽의 성공 지표가 다른 쪽의 실패
    지표다.
  - **한쪽이 다른 쪽의 전제를 명시적으로 부정한다.** "진실은 코드에만 있다"에 대해
    상대는 코드가 담을 수 없는 정보가 있고 주석 없이는 추상이 성립하지 않는다고 답한다.
    사실 명제의 정면 충돌이지 강조점의 차이가 아니다.
- **겹치는 구간은 넓고, 그래서 모순은 좁다.** 둘 다 ⓐ 코드를 되풀이하는 주석을 나쁘다고
  하고 ⓑ 좋은 설계가 주석의 필요를 줄인다는 데 동의하며(상대의 반박 ① 첫 문장이 그것을
  명시한다) ⓒ 낡은 주석이 해롭다고 본다. 갈리는 것은 **인터페이스 주석이 필수인가
  실패의 징표인가** 하나다.
- **기존 모순 쌍과의 관계.** 이 KB의 첫 `contradicts`는
  [코드의 나쁜 냄새](../concepts/code-smells.md) ↔ [주석을 왜 쓰는가](why-write-comments.md)였고,
  갈리는 명제는 "좋은 이름을 가진 선언이 인터페이스 주석을 대신할 수 있는가"였다.
  **이 페이지는 그 명제의 가장 강한 형태이자 원산지다** — 그때 상대편으로 세워졌던
  fowler2018의 처방("주석을 쓰고 싶으면 먼저 리팩터링하라")은 이 장의 처방을 이어받은
  것이고, 이 장은 거기에 "언제나 실패"라는 조문을 더한다. 세 페이지가 한 쟁점의 세
  꼭짓점이므로 각각의 `contradicts`는 그대로 두고 서로를 가리키게 한다.
- **해소하지 않는다.** 최신성만으로 판단하지 않는다. 해소는 사람이 근거와 날짜를 남기며
  한다.
- **두 저자가 이 쟁점으로 직접 맞붙은 공개 문서가 존재한다** —
  [클린 코드](../synthesis/clean-code.md) 허브가 그 1차 사료의 자리를 가리킨다.

## 저자가 대담에서 밝힌 동기와 좁힌 범위

> **버전 조건**: 이 페이지는 *Clean Code* **초판(2008)** 기준이다. 저자는 2024–2025년
> 공개 대담에서 메서드 길이에 대해서는 2판에서 균형을 조정했다고 밝혔으나, **주석에
> 대해서는 입장을 바꿨다고 말하지 않았다.** 그래서 이 페이지의 조문은 그대로 두되 아래
> 좁힘을 함께 읽는다.

전문은 [오스터하우트–마틴 공개 대담](../concepts/aposd-vs-clean-code-dialogue.md)에 있고, 여기서는
이 페이지의 조문에 직접 걸리는 것만 든다.

- **저자가 이 장의 역사적 동기를 밝힌다** (§"Comments", UB 발언):[^ousterhout2024-aposd]

> You and I likely both survived through a time when comments were absolutely necessary.
> In the '70s and '80s I was an assembly language programmer. I also wrote a bit of
> FORTRAN. Programs in those languages that had no comments were impenetrable.
>
> As a result it became conventional wisdom to write comments by default. And, indeed,
> computer science students were taught to write comments uncritically. Comments became
> _pure good_.
>
> In _Clean Code_ I decided to fight that mindset.

  - **이 장을 읽는 데 중요한 맥락이다.** 세기의 목표가 무주석이 아니라 **무비판적 주석
    관행에 대한 반작용**이었다는 저자 본인의 진술이다. 위 [조문](#조문)은 그대로 남지만
    의도의 범위가 좁아진다.
- **저자가 대상을 좁힌다** — **나는 주석 일반에 적대적이지 않다. 나는 불필요한(gratuitous)
  주석에 아주 적대적이다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
- **"실패"의 뜻도 좁혀진다** — 코드로 표현할 수 없는 정보가 있다는 데 동의하면서
  **그것이 실패다. 우리 언어의 실패, 또는 그것을 써서 우리를 표현하는 능력의 실패다**라고
  적고, 반사실로 못 박는다 — **완벽한 프로그래밍 언어가 있다면 우리는 다시는 주석을 쓰지
  않을 것이다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
  - **이것이 모순이 해소되지 않는 이유의 핵심이다.** 저자에게 주석은 언어의 결함을 메우는
    임시방편이고, 상대에게는 코드가 원리적으로 담을 수 없는 정보의 자리다.
- **그럼에도 세 자리에서 물러선다.**
  - **① 인터페이스 주석이 필요한 경우가 있다** (§"Comments", UB 발언):[^ousterhout2024-aposd]

> Yes, there are times when the signature of a method is an incomplete abstraction and a
> comment is required.  This is especially true when the interface is part of a public
> API, or an API intended for use by a separate team of developers.  Within a single
> development team, however, long descriptive comments on interfaces are often more of an
> impediment than a help.

  - 이것이 아래 모순 절의 **최종 경계**다. 다투는 것은 "주석이 필요한가"가 아니라
    **팀 내부 인터페이스에도 필요한가**다. 위 [그럼에도 좋다고 인정되는
    주석들](#그럼에도-좋다고-인정되는-주석들) 절의 공개 API 항목이 이 좁힘의 씨앗이다.
  - **② 주석이 코드보다 정밀할 때가 있다** — **정당한 지적이다. 정밀함이 주석으로 더 잘
    표현되는 때가 있다** (§"Comments", UB 발언).[^ousterhout2024-aposd]
  - **③ 코드는 뻔해야 한다는 원칙에 동의한다** — **당신의 정서에 반대하지 않는다. 좋은
    깨끗한 코드는 가능한 한 이해하기 쉬워야 한다** (§"Comments",
    UB 발언).[^ousterhout2024-aposd]
- **저자의 주석 읽기 원칙이 여기서 처음 명문화된다** — 이 장에는 없던 것이다
  (§"Comments", UB 발언):[^ousterhout2024-aposd]

> I look at every comment as potential misinformation.  At best they are a way to
> crosscheck the author's intent against the code.

  - 좋은 주석의 기준도 따라온다 — **가장 좋은 주석은 코드에 대해 놀랍고 검증 가능한
    무언가를 말해 주는 것이다** (§"Comments", UB 발언).[^ousterhout2024-aposd]

## 인용 대조 — 상대가 옮긴 문구와 원문의 차이

**이 소스를 들이고 나서야 가능해진 대조다.** 상대 페이지는 이 문단을 상대 소스의 인용을
거쳐 싣고 있었는데, 이제 원문과 맞대 볼 수 있다. 차이는 셋이고 **논지에는 영향이 없다.**

| 자리 | 상대가 옮긴 것 | 이 스냅샷의 원문 |
|---|---|---|
| 첫 문단 | `express ourselves in code` | `express ourself in code` |
| 첫 문단 | `we can't always figure out` | `we cannot always figure out` |
| 문단 구성 | 두 문단을 한 인용 블록으로 합침 | 원문은 `Note that I used the word failure. I meant it.` 두 문장이 사이에 있다 |

**셋째 판본이 생겼다.** 두 저자의 공개 대담에서 오스터하우트가 같은 문단을 `page 54`로
인용하는데, 그 표기는 `express ourselves`·`we cannot always figure out`·
`Note that I use the word failure`다 (§"Comments", JOHN 발언).[^ousterhout2024-aposd]
즉 세 판본이 `used`/`use`와 `ourself`/`ourselves`에서 갈린다. **논지에는 영향이 없고,
어느 것도 이 스냅샷을 대체하지 못한다** — 이 페이지의 직인용은 이 KB가 보존한 스냅샷
그대로 두고 단서를 여기 남긴다.

- `ourself`는 **이 스냅샷(Calibre 변환 EPUB)의 표기**이고 인쇄판의 오식인지 변환
  잡음인지 이 스냅샷만으로는 가릴 수 없다. #hypothesis 상대 소스가 `ourselves`로 옮긴
  것을 보면 인쇄판은 `ourselves`일 가능성이 높다. **직인용할 때는 이 단서를 함께
  적는다.**
- 상대가 생략한 두 문장(`Note that I used the word failure. I meant it.`)은 이 페이지의
  [조문](#조문) 절에 복원해 두었다. 생략은 논지를 바꾸지 않으나, 저자가 "실패"라는
  낱말을 의도적으로 골랐다고 명시한 자리라 이 쟁점에서는 중요한 문장이다.

## 이어지는 페이지

- [주석을 왜 쓰는가](why-write-comments.md) — **`contradicts` 상대.** 주석 없이는 추상이
  성립하지 않는다는 쪽
- [오스터하우트–마틴 공개 대담](../concepts/aposd-vs-clean-code-dialogue.md) — **이 모순의 1차 사료.**
  저자가 동기를 밝히고 세 자리에서 물러선 곳
- [코드의 나쁜 냄새](../concepts/code-smells.md) — 같은 쟁점의 셋째 꼭짓점. 주석을 리팩터링으로
  없애라는 쪽
- [작은 함수](small-functions.md) — 같은 소스의 앞 장. 주석을 없애는 수단이 함수
  추출이므로 두 장이 맞물린다
- [주석은 코드에서 뻔하지 않은 것을 서술한다](comments-describe-the-nonobvious.md) —
  두 소스가 **합의하는** 자리
- [인터페이스 문서화](interface-documentation.md) — 상대가 "필수"라고 하는 바로 그 층
- [기존 코드를 수정할 때](modifying-existing-code.md) — 주석이 낡는다는 같은 사실에서
  다른 처방으로 가는 자리
- [클린 코드의 발견법 목록](../concepts/clean-code-heuristics.md) — `C1`–`C5`의 자리
- [개발자의 소통](../concepts/developer-communication.md) — 같은 문제를 실용주의 쪽에서
  다루는 자리
- [문서화와 코드 명료함](../synthesis/documentation-and-code-clarity.md) — 상대 쪽 허브
- [클린 코드](../synthesis/clean-code.md) — 이 소스의 허브

[^ousterhout2024-aposd]: Ousterhout & Martin 2024, "A Philosophy of Software Design
    vs Clean Code". **대담이므로 locator에 발언자를 함께 적는다** — `JOHN`은 John
    Ousterhout, `UB`는 Robert C. Martin이다. 규약과 스냅샷 취득 경로는
    `it/archive/ousterhout2024-aposd/_progress.yaml` 머리말이 정본이다.

[^martin2008]: Martin 2008, 4장 "Comments"(제사 p.53 · 도입 pp.53–54 · §"Comments Do
    Not Make Up for Bad Code" p.55 · §"Explain Yourself in Code" p.55 · §"Good Comments"
    p.55 · §"Legal Comments" p.55 · §"Informative Comments" p.56 · §"Explanation of
    Intent" p.56 · §"Clarification" p.57 · §"Warning of Consequences" p.58 · §"TODO
    Comments" pp.58–59 · §"Amplification" p.59 · §"Javadocs in Public APIs" p.59 ·
    §"Bad Comments" p.60 · §"Redundant Comments" p.60 · §"Journal Comments" p.64) ·
    17장 `C1`–`C5`(pp.286–287). 쪽은 인쇄판 쪽 번호이며 복원 절차는
    `it/archive/martin2008/_progress.yaml` 머리말이 정본이다. 이 장에는 Listing 4-1부터
    4-8까지의 코드 리스팅이 있으나 펜스로 옮기지 않았다 — 대부분이 나쁜 예이고 전부
    FitNesse 문맥에 묶여 복사해 돌아가지 않는다. 도판은 없다. **직인용의 철자는 이
    스냅샷 그대로다** — 위 [인용 대조](#인용-대조--상대가-옮긴-문구와-원문의-차이) 절이
    그 단서의 정본이다.

[^ousterhout2021]: Ousterhout 2021, 12장 "Why Write Comments? The Four Excuses" §12.6
    (p.100). 쪽은 인쇄판 쪽 번호.

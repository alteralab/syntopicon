---
type: concept
title: 기본 리팩터링
description: 카탈로그 첫 장의 열한 항목 — 코드에 이름을 붙이는 추출과 그 역인 인라인(함수·변수), 붙인 이름을 고치는 세 항목(함수 선언 바꾸기·변수 캡슐화·변수 이름 바꾸기), 그리고 만들어진 함수들을 더 높은 모듈로 올리는 네 항목(매개변수 객체 도입·클래스로 묶기·변환으로 묶기·단계 쪼개기). 추출의 기준이 길이도 재사용도 아니라 의도와 구현의 분리라는 논증과 클래스와 변환 중 무엇을 고르는가의 판정 기준을 함께 담는다
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 기본 리팩터링

- [이 장이 묶는 축](#이-장이-묶는-축)
- [Extract Function — 추출의 기준](#extract-function--추출의-기준)
- [추출의 역과 변수 판 — Inline Function, Extract Variable, Inline Variable](#추출의-역과-변수-판--inline-function-extract-variable-inline-variable)
- [붙인 이름을 고치기 — Change Function Declaration, Encapsulate Variable, Rename Variable](#붙인-이름을-고치기--change-function-declaration-encapsulate-variable-rename-variable)
- [Introduce Parameter Object — 자료 뭉치에 구조를 주기](#introduce-parameter-object--자료-뭉치에-구조를-주기)
- [Combine Functions into Class와 Combine Functions into Transform](#combine-functions-into-class와-combine-functions-into-transform)
- [Split Phase — 순차 두 단계로 가르기](#split-phase--순차-두-단계로-가르기)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **코드에 이름을 붙이고 그 이름들을 더 높은 모듈로 묶어 올리는 기본 수순은
무엇인가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다 — 카탈로그 항목명은 이 책이 만들어
통용되게 한 고유명이고 코드 리뷰와 도구 메뉴에서 그대로 쓰이는 어휘다. 괄호 안의 쪽은 이
책이 항목을 가리킬 때 함께 붙이는 인쇄판 쪽 번호이며, 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축

- 저자가 이 장을 **가장 먼저 배우기에 가장 유용하다고 보는 리팩터링 집합**으로 규정한다
  (6장, p.105).[^fowler2018]
- 장 안의 배열에 방향이 있다 — 이름 붙이기에서 시작해 모듈 만들기로 올라간다.
  **함수를 만들고 이름 붙이는 것은 필수적인 저수준 리팩터링이다 — 그러나 일단 만들어지면
  함수들을 더 높은 수준의 모듈로 묶는 것이 필요하다** (6장, p.105).[^fowler2018]
  - 저수준: *Extract Function*(p.106)과 *Extract Variable*(p.119), 그리고 각각의 역인
    *Inline Function*(p.115)·*Inline Variable*(p.123). **추출은 전부 이름을 주는
    일이고, 배우면서 이름을 바꿔야 하는 일이 잦다** (6장, p.105).[^fowler2018] 그 이름
    고치기가 *Change Function Declaration*(p.124)과 *Rename Variable*(p.137)이고, 뒤엣것은
    *Encapsulate Variable*(p.132)에 기댄다.
  - 고수준: *Introduce Parameter Object*(p.140)로 늘 함께 다니는 인수 뭉치를 한 객체로 묶고,
    *Combine Functions into Class*(p.144)로 함수들을 그것이 다루는 데이터와 함께 클래스로,
    *Combine Functions into Transform*(p.149)으로 변환으로 묶는다. 한 걸음 더 큰 규모에서
    *Split Phase*(p.154)로 모듈들을 별개의 처리 단계로 만든다 (6장, p.105).[^fowler2018]

## Extract Function — 추출의 기준

이 항목이 카탈로그 전체에서 가장 자주 불리는 것이고, 다른 항목의 수순 안에 부품으로 반복해
등장한다.

- 저자 자신의 빈도 판정 — **Extract Function은 내가 하는 가장 흔한 리팩터링 중 하나다**
  (6장 §"Extract Function", p.106).[^fowler2018] 하는 일은 한 문장이다 — **코드 조각을 보고
  그것이 무엇을 하는지 이해한 다음, 그 목적을 따라 이름 지은 자기 함수로 추출한다**
  (6장 §"Extract Function", p.106).[^fowler2018]
- **기준으로 기각되는 것이 둘이다** — 길이("한 화면에 들어가야 한다")와 재사용("두 번 이상
  쓰이는 코드만 함수로")이 그것이고, 저자가 평생 들어 온 그 두 지침을 명시적으로 물린다
  (6장 §"Extract Function", pp.106–107).[^fowler2018] 채택하는 기준은 하나다 (6장
  §"Extract Function", p.107):[^fowler2018]

> The argument that makes most sense to me, however, is the separation between
> intention and implementation. If you have to spend effort looking at a fragment of
> code and figuring out *what* it's doing, then you should extract it into a function
> and name the function after the "what."

- 그 기준을 받아들인 결과가 함수 크기에 대한 실천이다 — **이 원칙을 받아들이고 나서 나는 아주
  작은 함수를 쓰는 습관을 들였다. 대개 몇 줄뿐이다. 나에게는 여섯 줄 넘는 코드를 가진 함수는
  어떤 것이든 냄새가 나기 시작하고, 코드 한 줄짜리 함수를 갖는 것도 드물지 않다** (6장
  §"Extract Function", p.107).[^fowler2018]
  - **크기가 중요하지 않다는 근거로 든 실물**: 켄트 벡이 보여 준 초기 스몰토크의 `highlight`
    메서드는 구현이 `reverse` 호출 하나뿐이라 **이름이 구현보다 길었다 — 그러나 코드의 의도와
    구현 사이의 거리가 컸기 때문에 그것은 문제가 되지 않았다** (6장 §"Extract Function",
    p.107).[^fowler2018] 이 잣대의 반대편 판정은
    [합칠 것인가 나눌 것인가](better-together-or-better-apart.md)에 있다.
  - **성능 우려는 시대 조건으로 기각한다** — **짧은 함수를 걱정하는 사람들이 있는데 함수 호출의
    성능 비용을 염려해서다. 내가 젊었을 때는 그것이 이따금 요인이었지만 지금은 아주 드물다.
    최적화 컴파일러는 더 짧은 함수에서 흔히 더 잘 동작하는데, 그런 함수가 더 쉽게 캐시될 수
    있기 때문이다** (6장 §"Extract Function", p.107).[^fowler2018] 판정의 전문은
    [성능을 위한 설계](designing-for-performance.md)에 있다.
  - **전제 조건이 명시된다** — **이런 작은 함수는 이름이 좋을 때만 동작하므로 이름 짓기에 좋은
    주의를 기울여야 한다** (6장 §"Extract Function", p.107).[^fowler2018]
- **주석이 추출 지점의 단서다** — **큰 함수 안에서 자기가 무엇을 하는지 말하는 주석으로
  시작하는 코드 조각을 자주 본다. 그 주석은 흔히 그 조각을 추출할 때 함수 이름의 좋은
  힌트다** (6장 §"Extract Function", p.107).[^fowler2018] 같은 발견법이 3장 Long Function의
  처방으로도 나와 있고, 이 자리가 이 KB의 첫 `contradicts` 쟁점과 맞닿는다 —
  [주석을 왜 쓰는가](why-write-comments.md) 참조.
- 수순의 요지는 넷이다 (6장 §"Extract Function", pp.107–108):[^fowler2018]
  1. **어떻게 하는지가 아니라 무엇을 하는지로** 새 함수 이름을 짓는다. **더 뜻있는 이름을
     떠올릴 수 없다면 그것은 그 코드를 추출하지 말아야 한다는 신호다.**
  2. 코드를 복사하고, 원본 함수 지역 범위이면서 새 함수 범위에 없을 변수를 훑어 매개변수로
     넘긴다. 값으로 넘어가면서 대입되는 변수가 하나면 추출 코드를 질의로 취급해 결과를 그
     변수에 대입한다.
  3. **대입되는 지역 변수가 너무 많으면 추출을 포기한다** — 그때는 *Split Variable*(p.240)이나
     *Replace Temp with Query*(p.178)로 변수 사용을 단순화한 뒤 다시 온다.
  4. 원래 자리를 호출로 바꾸고 테스트한 뒤, 방금 추출한 것과 같거나 비슷한 코드를 찾아
     *Replace Inline Code with Function Call*(p.222)을 검토한다.
- **되돌리기가 정상 경로에 들어 있다** — **함수를 추출하고, 그것으로 작업해 보고, 도움이 되지
  않는다는 것을 깨닫고, 다시 인라인해 되돌리는 것은 괜찮다. 무언가를 배웠다면 내 시간은
  낭비되지 않았다** (6장 §"Extract Function", p.107).[^fowler2018]

## 추출의 역과 변수 판 — Inline Function, Extract Variable, Inline Variable

- **Inline Function**(p.115) — 추출의 역. 쓰는 자리가 둘이다 (6장 §"Inline Function",
  p.115):[^fowler2018]
  - **본문이 이름만큼 명료할 때.** **간접성은 도움이 될 수 있지만 불필요한 간접성은
    짜증스럽다.**
  - **잘못 인수분해된 함수 무리를 다시 가를 때.** **전부 하나의 큰 함수로 인라인한 다음 내가
    선호하는 방식으로 함수들을 다시 추출할 수 있다.** 지나친 간접성 — **모든 함수가 다른
    함수에 단순 위임만 하고 그 위임들 속에서 길을 잃을 때** — 도 같은 처방이다.
  - 수순의 단서 하나가 이 항목의 성격을 말한다 — 재귀·다중 반환점·접근자 없는 객체 사이의
    인라인 같은 복잡한 경우를 저자가 다루지 않는 이유가 **그런 복잡성을 만난다면 이 리팩터링을
    하지 말아야 하기 때문이다** (6장 §"Inline Function", p.117).[^fowler2018]
- **Extract Variable**(p.119) — 표현식에 이름을 준다. **복잡한 로직 한 조각의 일부에 이름을
  붙일 능력을 준다.** 디버깅에도 편리한데 **디버거나 출력문이 값을 붙잡을 쉬운 고리를
  제공하기 때문이다** (6장 §"Extract Variable", p.119).[^fowler2018]
  - **범위 판정이 붙는다** — 이름이 지금 작업 중인 함수 안에서만 뜻이 있으면 변수가 맞고, **더
    넓은 맥락에서 뜻이 있으면 보통 함수로 그 이름을 더 넓게 내놓는 쪽을 검토한다.** 그 대가가
    크면 나중에 *Replace Temp with Query*(p.178)로 미룬다 (6장 §"Extract Variable",
    p.119).[^fowler2018]
  - 수순의 첫 단계가 조건이다 — **추출하려는 표현식에 부작용이 없음을 확인**하고, **불변
    변수로 선언**한다 (6장 §"Extract Variable", p.120).[^fowler2018]
- **Inline Variable**(p.123) — 그 역. **때로는 이름이 표현식 자체보다 더 많이 소통하지
  못한다. 또 어떤 때는 변수가 이웃 코드를 리팩터링하는 데 방해가 된다** (6장 §"Inline
  Variable", p.123).[^fowler2018]

## 붙인 이름을 고치기 — Change Function Declaration, Encapsulate Variable, Rename Variable

- **Change Function Declaration**(p.124) — 별칭이 많은 항목이다(*Rename Function*,
  *Change Signature*, 그리고 초판의 *Rename Method*·*Add Parameter*·*Remove Parameter*).
  이름과 매개변수를 함께 다루는 근거가 하나의 비유다 (6장 §"Change Function Declaration",
  p.124):[^fowler2018]

> Functions represent the primary way we break a program down into parts. Function
> declarations represent how these parts fit together—effectively, they represent the
> joints in our software systems.

  - **이름을 고칠 결심의 기준** — **잘못된 이름을 가진 함수를 보면, 더 나은 이름이 무엇일지
    이해하는 즉시 그것을 바꾸는 것이 필수적이다. 그래야 다음번에 이 코드를 볼 때 무슨 일이
    일어나는지 *다시* 알아내지 않아도 된다** (6장 §"Change Function Declaration",
    p.125).[^fowler2018] 그리고 방법 하나가 붙는다 — **이름을 개선하는 좋은 방법은 흔히 함수의
    목적을 서술하는 주석을 쓴 다음 그 주석을 이름으로 바꾸는 것이다** (6장 §"Change Function
    Declaration", p.125).[^fowler2018]
  - **매개변수 선택에는 정답이 없다고 명시한다.** 지불 객체를 받을 것인가 만기일을 받을
    것인가의 예를 들고 — **이 수수께끼의 유일한 옳은 답은 옳은 답이 없다는 것이고, 시간이 지나면
    특히 그렇다** (6장 §"Change Function Declaration", p.125).[^fowler2018] 그래서 결론이
    능력 쪽으로 간다 — 코드가 진화할 수 있도록 이 리팩터링에 익숙해지는 것이 필수다.
  - **이 항목만 수순이 두 벌이다** — 카탈로그의 명시적 예외다. 선언과 모든 호출자를 한 번에
    쉽게 바꿀 수 있으면 **단순 수순**, 호출자가 많거나 닿기 불편하거나 다형 메서드거나 변경이
    복잡하면 **이주 수순**을 쓴다. 이주 수순은 *Extract Function*으로 새 함수를 만들고 옛
    함수에 *Inline Function*을 적용하는 형태다 (6장 §"Change Function Declaration",
    pp.125–126).[^fowler2018]
  - **공표된 API에는 일시 정지 지점이 있다** — 새 함수를 만든 뒤 리팩터링을 멈추고 원래 함수를
    폐기 예정으로 표시한 다음 클라이언트가 옮겨 오기를 기다린다 (6장 §"Change Function
    Declaration", pp.126–127).[^fowler2018] 같은 제약의 진단은
    [리팩터링을 가로막는 것들](obstacles-to-refactoring.md)에 있다.
- **Encapsulate Variable**(p.132) — 데이터를 옮기기 전에 함수 뒤로 숨기는 항목이고, 데이터
  관련 리팩터링의 관문이다. 근거는 함수와 데이터의 비대칭이다 — **데이터는 함수보다 다루기가
  더 까다롭다.** 함수는 옛 이름을 전달용 함수로 남겨 둘 수 있지만 **데이터를 옮기면 코드가
  동작하게 유지하려고 그 데이터에 대한 모든 참조를 한 주기 안에 바꿔야 한다** (6장
  §"Encapsulate Variable", p.132).[^fowler2018]
  - 그래서 처방이 문제 치환이다 — **널리 접근되는 데이터를 옮기고 싶으면 흔히 최선의 접근은 모든
    접근을 함수를 거치게 해 먼저 캡슐화하는 것이다. 그러면 데이터를 재조직하는 어려운 일을
    함수를 재조직하는 더 쉬운 일로 바꾼다** (6장 §"Encapsulate Variable",
    p.132).[^fowler2018]
  - **적용 기준이 범위다** — **범위가 함수 하나보다 크면 모든 가변 데이터를 이렇게 캡슐화해
    함수를 통해서만 접근하게 하는 것이 내 습관이다. 데이터의 범위가 클수록 캡슐화가 더
    중요하다** (6장 §"Encapsulate Variable", p.132).[^fowler2018]
  - **불변 데이터에는 훨씬 덜 중요하다** — 갱신 전에 검증이나 로직 훅을 넣을 자리가 필요 없고
    옮기는 대신 자유롭게 복사할 수 있다. **불변성은 강력한 방부제다** (6장 §"Encapsulate
    Variable", p.133).[^fowler2018]
  - **자기 캡슐화에는 거리를 둔다** — 클래스 내부의 필드 참조까지 접근자를 거치게 하자는 주장에
    대해 **전반적으로 자기 캡슐화는 과하다고 본다 — 클래스가 자기 필드를 자기 캡슐화해야 할
    만큼 크다면 어차피 쪼개야 한다**고 하고, 다만 **클래스를 쪼개기 전 단계로는 유용하다**고
    덧붙인다 (6장 §"Encapsulate Variable", p.133).[^fowler2018]
- **Rename Variable**(p.137) — **이름을 잘 짓는 것이 명료한 프로그래밍의 심장이다** (6장
  §"Rename Variable", p.137).[^fowler2018] 이 항목의 고유한 기여는 **이름의 중요도가 범위에
  비례한다**는 눈금이다 — 한 줄짜리 람다의 변수는 글자 하나로도 되고, 짧은 함수의 매개변수도
  간결해도 되며(다만 자바스크립트 같은 동적 타입 언어에서는 `aCustomer`처럼 타입을 이름에
  넣기를 선호한다), **함수 호출 하나를 넘어 지속되는 필드가 더 신중한 이름을 요구하고 저자가
  주의를 가장 많이 쏟는 자리다** (6장 §"Rename Variable", p.137).[^fowler2018] 이름 짓기의
  정본은 [이름 짓기](naming-things.md)다.

## Introduce Parameter Object — 자료 뭉치에 구조를 주기

- 계기는 3장의 냄새와 같다 — **함수마다 나타나면서 규칙적으로 함께 다니는 데이터 항목 무리를
  자주 본다. 그런 무리가 데이터 뭉치(data clump)이고, 나는 그것을 하나의 자료 구조로 바꾸기를
  좋아한다** (6장 §"Introduce Parameter Object", p.140).[^fowler2018]
- **직접 이득 셋** (6장 §"Introduce Parameter Object", p.140):[^fowler2018] 데이터 항목
  사이의 **관계를 명시적으로** 만들고, 매개변수 목록 **크기를 줄이고**, 모든 함수가 같은
  이름으로 원소에 접근하므로 **일관성을 돕는다.**
- **그러나 저자가 진짜 힘이라고 부르는 것은 그 다음이다** (6장 §"Introduce Parameter Object",
  p.140):[^fowler2018]

> But the real power of this refactoring is how it enables deeper changes to the code.
> When I identify these new structures, I can reorient the behavior of the program to
> use these structures. I will create functions that capture the common behavior over
> this data—either as a set of common functions or as a class that combines the data
> structure with these functions. This process can change the conceptual picture of the
> code, raising these structures as new abstractions that can greatly simplify my
> understanding of the domain.

  - 그리고 조건이 붙는다 — **이것이 통할 때 놀랄 만큼 강력한 효과를 낼 수 있다 — 그러나 이 중
    어느 것도 그 과정을 시작하려고 Introduce Parameter Object를 쓰지 않으면 가능하지 않다**
    (6장 §"Introduce Parameter Object", p.140).[^fowler2018] 이 항목이 두꺼운 이유가 여기
    있다 — 이것은 매개변수 목록 줄이기가 아니라 **도메인 추상을 발견하는 진입로**다.
- 수순에 취향 하나가 명시된다 — **나는 클래스를 쓰기를 선호하는데, 나중에 행동을 묶기가 더
  쉬워지기 때문이다. 보통 이 구조들이 값 객체(value object)가 되도록 하는 편을 좋아한다**
  (6장 §"Introduce Parameter Object", p.140).[^fowler2018] 나머지는 *Change Function
  Declaration*으로 새 구조 매개변수를 더하고, 호출자를 하나씩 옮기고, 원래 매개변수를 하나씩
  없애는 순이다.

## Combine Functions into Class와 Combine Functions into Transform

같은 문제 — **공통 데이터를 두고 밀접하게 함께 동작하는 함수 무리** — 에 대한 두 답이고,
저자가 둘 사이의 선택 기준을 명시했다.

- **Combine Functions into Class**(p.144) — **공통 자료 뭉치를 두고 밀접하게 함께 동작하는
  함수 무리를 볼 때 클래스를 만들 기회를 본다** (6장 §"Combine Functions into Class",
  p.144).[^fowler2018] 이득 셋 (6장 §"Combine Functions into Class",
  p.144):[^fowler2018] 함수들이 공유하는 **공통 환경을 더 명시적으로** 만들고, 객체 안의 함수
  호출에서 **인수를 많이 덜어** 단순화하고, 그 객체를 시스템의 다른 부분에 넘길 **참조를
  제공한다.**
  - **부수 이득 하나** — **이미 만들어진 함수를 조직하는 것에 더해, 이 리팩터링은 다른 계산
    조각을 식별해 새 클래스의 메서드로 리팩터링할 좋은 기회도 준다** (6장 §"Combine Functions
    into Class", p.144).[^fowler2018]
  - **중첩 함수와의 대조** — 이런 함수들은 중첩 함수로도 묶을 수 있으나 **보통 클래스를
    선호하는데, 다른 함수 안에 중첩된 함수를 테스트하기가 어려울 수 있기 때문이다. 무리 중
    협력자에게 노출하고 싶은 함수가 하나를 넘으면 클래스가 필요하기도 하다** (6장 §"Combine
    Functions into Class", p.145).[^fowler2018] 클래스가 일급이 아니면서 함수가 일급인
    언어는 Function As Object로 같은 능력을 낸다.
  - 수순이 이 장의 다른 항목들로 조립된다 — 공유 레코드에 *Encapsulate Record*(p.162)를
    적용하고(레코드로 묶여 있지 않으면 *Introduce Parameter Object*로 먼저 만든다), 각 함수를
    *Move Function*(p.198)으로 새 클래스에 옮기고, 데이터를 다루는 로직 조각을
    *Extract Function*으로 뽑아 옮긴다 (6장 §"Combine Functions into Class",
    p.145).[^fowler2018]
- **Combine Functions into Transform**(p.149) — 같은 묶기를 변환 함수로 한다. 문제 규정이
  파생 데이터다 — **소프트웨어는 흔히 데이터를 프로그램에 넣어 거기서 다양한 파생 정보를
  계산하는 일을 포함한다. 이 파생 값들은 여러 자리에서 필요할 수 있고, 그 계산은 파생 데이터가
  쓰이는 곳마다 흔히 반복된다** (6장 §"Combine Functions into Transform",
  p.149).[^fowler2018]
  - 처방 — **원본 데이터를 입력으로 받아 모든 파생을 계산해 각 파생 값을 출력 데이터의 필드로
    넣는 데이터 변환 함수를 쓴다. 그러면 파생을 살펴보려면 그 변환 함수만 보면 된다** (6장
    §"Combine Functions into Transform", p.149).[^fowler2018]
  - **둘 중 무엇을 고르는가 — 하나의 결정적 차이가 명시된다** (6장 §"Combine Functions into
    Transform", p.149):[^fowler2018]

> But there is one important difference: Using a class is much better if the source data
> gets updated within the code. Using a transform stores derived data in the new record,
> so if the source data changes, I will run into inconsistencies.

  - 클래스 쪽 항목에도 같은 판정이 대칭으로 적혀 있다 — **클래스를 쓰는 중요한 이점 하나는
    클라이언트가 객체의 핵심 데이터를 변경해도 파생이 일관되게 남는다는 것이다** (6장
    §"Combine Functions into Class", p.144).[^fowler2018] 나머지는 취향과 이미 쓰이는
    프로그래밍 스타일의 문제라고 저자가 적는다.
  - **왜 *Extract Function*만으로는 부족한가** — 파생 로직의 중복을 없애는 것만이라면 추출로도
    되지만 **함수들이 그것이 다루는 자료 구조 가까이 있지 않으면 찾기 어려운 일이 잦다. 변환
    (또는 클래스)을 쓰면 찾아 쓰기가 쉬워진다** (6장 §"Combine Functions into Transform",
    p.150).[^fowler2018]
  - 수순의 첫 단계에 안전장치가 붙는다 — 변환 함수는 보통 레코드의 깊은 복사를 포함하며,
    **변환이 원본 레코드를 바꾸지 않음을 보장하는 테스트를 쓰는 것이 흔히 값어치를 한다**
    (6장 §"Combine Functions into Transform", p.150).[^fowler2018]

## Split Phase — 순차 두 단계로 가르기

- 계기는 **한 코드가 서로 다른 두 가지를 다루고 있을 때**이고, 이득은 머릿속 부담이다 — **변경을
  해야 할 때 각 주제를 따로 다룰 수 있고 둘을 함께 머리에 담지 않아도 된다. 운이 좋으면 다른
  것의 세부를 전혀 기억하지 않고 한 모듈만 바꾸면 될 수도 있다** (6장 §"Split Phase",
  p.154).[^fowler2018]
- **가르는 방식이 순차 두 국면이다** — **이런 쪼개기를 하는 가장 깔끔한 방법 하나는 행동을 두
  순차 국면으로 나누는 것이다. 좋은 예는 입력이 로직을 수행하는 데 필요한 모델을 반영하지
  못하는 처리를 가진 경우다. 시작하기 전에 입력을 주 처리에 편한 형태로 주무를 수 있다** (6장
  §"Split Phase", p.154).[^fowler2018]
- **가장 뻔한 실물이 컴파일러다** — 텍스트를 토큰화하고, 토큰을 구문 트리로 파싱하고, 구문
  트리를 여러 단계로 변환하고(예: 최적화), 마지막으로 목적 코드를 생성한다. **각 단계는 범위가
  제한돼 있고 나는 다른 단계의 세부를 이해하지 않고 한 단계를 생각할 수 있다** (6장 §"Split
  Phase", p.155).[^fowler2018]
- **탐지 신호가 하나 있다** — **가장 좋은 단서는 조각의 서로 다른 국면이 서로 다른 데이터와 함수
  집합을 쓸 때다** (6장 §"Split Phase", p.155).[^fowler2018]
- 수순은 둘째 국면을 먼저 추출한 뒤 그 둘 사이에 **중간 자료 구조**를 인수로 끼워 넣고, 둘째
  국면의 매개변수 중 첫째 국면이 쓰는 것을 그 구조로 옮기는 순이다 (6장 §"Split Phase",
  p.155).[^fowler2018] 3장이 발산하는 변경(Divergent Change)의 처방으로 이 항목을 지목하고,
  그 중간 자료 구조가 데이터 클래스 냄새의 정당한 예외로도 다시 나온다 —
  [코드의 나쁜 냄새](code-smells.md) 참조.

## 이어지는 페이지

- [리팩터링 카탈로그를 읽는 법](refactoring-catalog-format.md) — 이 페이지가 옮긴 항목들이
  어떤 규약으로 쓰였는가
- [캡슐화 리팩터링](encapsulation-refactorings.md) — 다음 장(7장). 여기서 만든 클래스로
  무엇을 감추는가
- [기능 이동 리팩터링](moving-features.md) — *Move Function*의 정본이 있는 장(8장)
- [코드의 나쁜 냄새](code-smells.md) — 어느 항목을 펼지 알려 주는 반대 방향 색인
- [리팩터링의 리듬](refactoring-rhythm.md) — 이 항목들이 실제 예제 하나에서 연달아 적용되는 자리
- [이름 짓기](naming-things.md) — 추출이 전부 이름 붙이기라는 이 장의 전제가 사는 곳
- [합칠 것인가 나눌 것인가](better-together-or-better-apart.md) — 함수를 얼마나 쪼갤지에 대해
  반대 방향 사전 확률을 가진 소스
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 6장 "A First Set of Refactorings"(pp.105–160). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준
    규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example
    절(자바스크립트 예제의 연속 개정판)은 옮기지 않았다 — 카탈로그 예제의 성격과 그 이유는
    [리팩터링 카탈로그를 읽는 법](refactoring-catalog-format.md)에 있다. 스케치의 도판도
    추출본에 없어 옮기지 않았다.

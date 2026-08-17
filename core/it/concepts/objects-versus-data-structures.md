---
type: concept
title: 객체와 자료 구조
description: 객체와 자료 구조를 정반대의 것으로 정의하고 그 비대칭에서 언제 어느 쪽을 쓸지 판정하는 장 — 구현을 감추는 것이 접근자를 두는 것이 아니라 추상을 내놓는 것이라는 규정, 객체와 자료 구조의 반대칭과 그것이 만드는 변경 용이성의 교환, 모든 것이 객체라는 생각이 신화라는 판정, 디미터 법칙과 기차 충돌, 절반씩인 잡종 구조, 그리고 DTO와 액티브 레코드
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
sources:
  - { id: martin2008, resource: /it/sources/martin2008.md }
  - { id: qntm2020, resource: /it/sources/qntm2020.md }
---

# 객체와 자료 구조

- [구현을 감춘다는 것](#구현을-감춘다는-것)
- [반대칭 — 두 정의는 서로의 반대다](#반대칭--두-정의는-서로의-반대다)
- [교환의 정식화](#교환의-정식화)
- [모든 것이 객체라는 생각은 신화다](#모든-것이-객체라는-생각은-신화다)
- [디미터 법칙과 기차 충돌](#디미터-법칙과-기차-충돌)
- [잡종 — 두 세계의 최악](#잡종--두-세계의-최악)
- [구조를 감추기](#구조를-감추기)
- [DTO와 액티브 레코드](#dto와-액티브-레코드)
- [같은 책 3장과의 긴장을 저자가 지목한다](#같은-책-3장과의-긴장을-저자가-지목한다)
- [이 KB의 데이터 클래스 판정과 어떻게 만나는가](#이-kb의-데이터-클래스-판정과-어떻게-만나는가)
- [2차 문헌의 지적 — 이 장의 "자료 구조"는 통용 의미가 아니다](#2차-문헌의-지적--이-장의-자료-구조는-통용-의미가-아니다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **객체와 자료 구조는 무엇이 다르며, 그 차이가 어떤 설계 판단을 낳는가.**

> **이 페이지의 소스는 논쟁 중인 소스다.** 반입 지위와 그 근거는
> [소스 메타](../sources/martin2008.md)가 정본이다. **다만 이 장은 이 책에서 가장 논쟁이
> 적은 장 축에 든다** — 처방이 아니라 교환 관계를 정식화하고 어느 쪽도 기본값으로 세우지
> 않기 때문이다. 아래 [3장과의 긴장](#같은-책-3장과의-긴장을-저자가-지목한다) 절이 그
> 차이를 드러낸다.

## 구현을 감춘다는 것

- 접근자를 두는 것으로는 부족하다 — **구현을 감추는 것은 변수 앞에 함수 층을 두는 문제가
  아니다. 구현을 감추는 것은 추상에 관한 것이다! 클래스는 단순히 게터와 세터로 변수를
  밖으로 밀어내지 않는다. 오히려 그것은 사용자가 구현을 알 필요 없이 데이터의 **본질**을
  다룰 수 있게 하는 추상 인터페이스를 내놓는다** (6장 §"Data Abstraction",
  p.94).[^martin2008]
- 예제가 둘이다 — `Point`를 구체적으로(`public double x; public double y;`) 두는 쪽과
  추상적으로(`getX()`·`setCartesian()`·`getR()`·`setPolar()`) 두는 쪽. 후자의 미덕은
  **구현이 직교 좌표인지 극좌표인지 알 방법이 전혀 없다는 것이고**, 나아가 **메서드가
  접근 정책을 강제한다 — 개별 좌표는 따로 읽을 수 있지만 좌표를 설정할 때는 원자적
  연산으로 함께 해야 한다** (6장 §"Data Abstraction", p.94).[^martin2008]
- 그리고 `private`으로도 부족하다는 판정 — 구체 `Point`는 **변수가 `private`이고
  단일 변수 게터·세터를 쓰더라도 구현을 노출한다** (6장 §"Data Abstraction",
  p.94).[^martin2008]
- 두 번째 예제는 연료 표시다. `getFuelTankCapacityInGallons()` + `getGallonsOfGasoline()`
  대신 `getPercentFuelRemaining()`을 두라는 것이고, 판정은 — **우리는 데이터의 세부를
  노출하고 싶지 않다. 오히려 우리는 데이터를 추상적인 말로 표현하고 싶다. 이것은 단지
  인터페이스나 게터·세터를 써서 달성되는 것이 아니다. 객체가 담는 데이터를 표현하는
  최선의 방법에 진지한 생각을 들여야 한다. 최악의 선택은 아무 생각 없이 게터와 세터를
  더하는 것이다** (6장 §"Data Abstraction", p.95).[^martin2008]
  - **이 판정은 이 KB의 다른 소스와 일치한다** —
    [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)이 게터·세터를 얕은 메서드의
    실물로 지목하는 자리(19장 §19.6)와 같은 방향이다. 두 소스가 서로를 참조한 적은 없다.

## 반대칭 — 두 정의는 서로의 반대다

- 정의 (6장 §"Data/Object Anti-Symmetry", p.95):[^martin2008]

> Objects hide their data behind abstractions and expose functions that operate on that
> data. Data structure expose their data and have no meaningful functions.

- 그리고 **이 두 정의의 상보적 성격에 유의하라. 그것들은 사실상 반대다. 이 차이는 사소해
  보일지 몰라도 광범위한 함의를 갖는다** (6장 §"Data/Object Anti-Symmetry",
  p.95).[^martin2008]
- 예제 쌍이 도형 넓이 계산이다.
  - **절차적 쪽**(`Square`·`Rectangle`·`Circle`은 필드만 갖고 `Geometry`가 `instanceof`
    분기로 넓이를 계산) — 객체 지향 프로그래머가 코를 찡그릴 만하고 **그들이 옳을
    것이다. 그러나 그 비웃음이 정당하지는 않을 수 있다. `Geometry`에 `perimeter()`
    함수를 더한다면 어떻게 될지 생각해 보라. 도형 클래스들은 영향받지 않을 것이다!**
    (6장 §"Data/Object Anti-Symmetry", p.96).[^martin2008]
  - **반대로 새 도형을 더하면 `Geometry`의 모든 함수를 바꿔야 한다** (6장
    §"Data/Object Anti-Symmetry", p.96).[^martin2008]
  - **객체 지향 쪽**(각 도형이 `area()`를 구현) — **새 도형을 더하면 기존 *함수*는 아무것도
    영향받지 않지만, 새 함수를 더하면 모든 *도형*을 바꿔야 한다!** (6장 §"Data/Object
    Anti-Symmetry", p.96).[^martin2008]
    - 저자는 각주에서 이 제약의 우회로를 인정하고 그 대가도 적는다 — **VISITOR나 이중
      분배 같은 잘 알려진 방법이 있다. 그러나 이 기법들은 자기 나름의 비용을 지불하며
      대체로 구조를 절차적 프로그램의 것으로 되돌린다** (6장 각주 1,
      p.96).[^martin2008]

## 교환의 정식화

- 이 장의 결론 명제 두 쌍 (6장 §"Data/Object Anti-Symmetry", p.97):[^martin2008]

> Procedural code (code using data structures) makes it easy to add new functions without
> changing the existing data structures. OO code, on the other hand, makes it easy to add
> new classes without changing existing functions.

> Procedural code makes it hard to add new data structures because all the functions must
> change. OO code makes it hard to add new functions because all the classes must change.

- 그리고 요약 — **그러니 객체 지향에 어려운 것이 절차에는 쉽고, 절차에 어려운 것이 객체
  지향에는 쉽다!** (6장 §"Data/Object Anti-Symmetry", p.97).[^martin2008]
- **판단 기준은 무엇이 더 자주 바뀌는가다** — **복잡한 시스템이라면 새 함수가 아니라 새
  데이터 타입을 더하고 싶을 때가 있을 것이다. 그런 경우에는 객체와 객체 지향이 가장
  적절하다. 반면 데이터 타입이 아니라 새 함수를 더하고 싶을 때도 있을 것이다. 그 경우에는
  절차적 코드와 자료 구조가 더 적절할 것이다** (6장 §"Data/Object Anti-Symmetry",
  p.97).[^martin2008]

## 모든 것이 객체라는 생각은 신화다

- 조문 (6장 §"Data/Object Anti-Symmetry", p.97):[^martin2008]

> Mature programmers know that the idea that everything is an object *is a myth*.
> Sometimes you really *do* want simple data structures with procedures operating on
> them.

- 장의 결론도 같은 태도로 닫힌다 — **좋은 소프트웨어 개발자는 편견 없이 이 문제들을
  이해하고 당면한 일에 최선인 접근을 고른다** (6장 §"Conclusion",
  p.101).[^martin2008]
  - **이 두 문장이 이 장의 성격을 규정한다.** 이 책의 다른 장들이 단일 기본값을 세우는
    데 반해 이 장은 조건부 판단을 세운다. 이 KB가 이 장을 합의 영역에 가깝게 놓는 근거다.

## 디미터 법칙과 기차 충돌

- 법칙 — **모듈은 자기가 다루는 **객체**의 속을 알아서는 안 된다** (6장 §"The Law of
  Demeter", p.97).[^martin2008] 더 정확히는, 클래스 `C`의 메서드 `f`는 다음의 메서드만
  호출해야 한다 (6장 §"The Law of Demeter", pp.97–98):[^martin2008]
  - `C`
  - `f`가 만든 객체
  - `f`에 인수로 넘어온 객체
  - `C`의 인스턴스 변수가 들고 있는 객체
- 그리고 **허용된 함수들이 돌려주는 객체의 메서드는 호출해서는 안 된다. 다시 말해,
  친구에게 말하고 낯선 이에게는 말하지 마라** (6장 §"The Law of Demeter",
  p.98).[^martin2008]
- `ctxt.getOptions().getScratchDir().getAbsolutePath()` 같은 연쇄를 **기차 충돌(train
  wreck)**이라 부른다 — **연결된 기차 칸 무더기처럼 보이기 때문이다** (6장 §"Train
  Wrecks", p.98).[^martin2008]
- **결정적인 단서가 붙는다 — 위반 여부가 대상의 종류에 달려 있다** (6장 §"Train Wrecks",
  p.98):[^martin2008]

> Whether this is a violation of Demeter depends on whether or not ctxt, Options, and
> ScratchDir are objects or data structures. If they are objects, then their internal
> structure should be hidden rather than exposed, and so knowledge of their innards is a
> clear violation of the Law of Demeter. On the other hand, if ctxt, Options, and
> ScratchDir are just data structures with no behavior, then they naturally expose their
> internal structure, and so Demeter does not apply.

- 혼란의 원인을 접근자 관례로 지목한다 — **접근자 함수의 사용이 문제를 혼란스럽게 만든다.
  코드가 `ctxt.options.scratchDir.absolutePath`로 쓰였다면 우리는 아마 디미터 위반을
  묻지 않았을 것이다** (6장 §"Train Wrecks", p.98).[^martin2008] 그리고 **"빈(bean)"
  같은 프레임워크와 표준이 단순한 자료 구조에까지 접근자와 변경자를 요구한다**는 것이
  현실 조건으로 적힌다 (6장 §"Train Wrecks", pp.98–99).[^martin2008]
- 17장의 `G36` **Avoid Transitive Navigation**이 같은 것을 다시 조문화하며 실용주의
  쪽의 이름을 함께 든다 — **실용주의 프로그래머들은 이것을 "부끄럼 타는 코드 쓰기"라고
  부른다** (17장 `G36`, p.306).[^martin2008] 그리고 아키텍처 대가가 계상된다 — 많은
  모듈이 `a.getB().getC()`를 쓰면 **B와 C 사이에 Q를 끼워 넣도록 설계와 아키텍처를 바꾸기
  어려워진다. 이것이 아키텍처가 경직되는 방식이다** (17장 `G36`,
  pp.306–307).[^martin2008]
  - 이 KB의 실용주의 쪽 자리는 [결합 끊기](../concepts/decoupling.md)다.

## 잡종 — 두 세계의 최악

- **이 혼란은 때로 반은 객체이고 반은 자료 구조인 불행한 잡종 구조를 낳는다. 그것들은
  의미 있는 일을 하는 함수를 가지면서, 동시에 공개 변수나 공개 접근자·변경자를 가져
  사실상 비공개 변수를 공개로 만들고 외부 함수가 절차적 프로그램이 자료 구조를 쓰듯 그
  변수를 쓰도록 유혹한다** (6장 §"Hybrids", p.99).[^martin2008]
- 판정 (6장 §"Hybrids", p.99):[^martin2008]

> Such hybrids make it hard to add new functions but also make it hard to add new data
> structures. They are the worst of both worlds. Avoid creating them.

## 구조를 감추기

- 객체라면 길을 물을 것이 아니라 일을 시켜야 한다 — **`ctxt`가 객체라면 우리는 그것에게
  **무언가를 하라고** 말해야 한다; 그것의 내부에 대해 물어서는 안 된다** (6장 §"Hiding
  Structure", p.99).[^martin2008]
- 저자는 두 우회로를 먼저 놓고 둘 다 기각한다 —
  `ctxt.getAbsolutePathOfScratchDirectoryOption()`은 **`ctxt` 객체의 메서드 폭발로 이어질
  수 있고**, `ctx.getScratchDirectoryOption().getAbsolutePath()`는 **반환값이 객체가
  아니라 자료 구조라고 전제한다. 어느 쪽도 좋게 느껴지지 않는다** (6장 §"Hiding
  Structure", p.99).[^martin2008]
- 해법은 **의도를 묻는 것**이다 — 절대 경로를 원한 이유가 스크래치 파일을 만드는
  것이었으므로 `ctxt.createScratchFileStream(classFileName)`을 두라는 것이고, **그것이
  객체가 할 만한 합당한 일로 보인다** (6장 §"Hiding Structure", p.100).[^martin2008]

## DTO와 액티브 레코드

- **자료 구조의 전형적 형태는 공개 변수를 갖고 함수가 없는 클래스다. 이것은 때로 데이터
  전송 객체(DTO)라 불린다. DTO는 아주 쓸모 있는 구조인데, 특히 데이터베이스와 소통하거나
  소켓에서 온 메시지를 파싱할 때 그렇다** (6장 §"Data Transfer Objects",
  p.100).[^martin2008]
- 빈 형태에는 판정이 붙는다 — **빈은 게터와 세터로 조작되는 비공개 변수를 갖는다. 빈의
  유사 캡슐화는 어떤 객체 지향 순수주의자들의 기분을 낫게 해 주는 것 같지만 대개 다른
  이득은 주지 않는다** (6장 §"Data Transfer Objects", p.100).[^martin2008]
- 액티브 레코드는 DTO의 특수형이고, 그것을 객체처럼 다루려는 시도가 문제로 지목된다 —
  **불행히도 우리는 개발자들이 이 자료 구조에 업무 규칙 메서드를 넣어 객체인 것처럼
  다루려는 것을 자주 본다. 이것은 자료 구조와 객체 사이의 잡종을 만들기 때문에
  어색하다** (6장 §"Active Record", p.101).[^martin2008]
- 처방 — **해법은 물론 액티브 레코드를 자료 구조로 다루고, 업무 규칙을 담으며 자기 내부
  데이터를 감추는 별도의 객체를 만드는 것이다** (6장 §"Active Record",
  p.101).[^martin2008]
  - 이 KB에 이미 있는 같은 축의 페이지가 [도메인 모델 패턴](../concepts/domain-model-pattern.md)과
    [리포지터리 패턴](repository-pattern.md)이다. 두 소스가 서로를 참조한 적은 없다.

## 같은 책 3장과의 긴장을 저자가 지목한다

17장의 `G23` **Prefer Polymorphism to If/Else or Switch/Case**가 이 장을 명시적으로
불러 세운다 (17장 `G23`, p.299):[^martin2008]

> This might seem a strange suggestion given the topic of Chapter 6. After all, in that
> chapter I make the point that switch statements are probably appropriate in the parts
> of the system where adding new functions is more likely than adding new types.

- 저자의 해소 방식은 **빈도 주장**이다 — ① **대부분의 사람은 `switch` 문이 그 상황에
  옳은 해법이라서가 아니라 그것이 뻔한 무차별 대입 해법이라서 쓴다** ② **함수가 타입보다
  더 자주 변하는 경우는 비교적 드물다. 그러니 **모든** `switch` 문은 의심스러워야 한다**
  (17장 `G23`, p.299).[^martin2008] 그리고 "ONE SWITCH" 규칙을 세운다 — **주어진 선택
  종류에 대해 `switch` 문은 하나보다 많아서는 안 된다** (17장 `G23`,
  p.299).[^martin2008]
- **이것은 이 KB의 `contradicts` 대상이 아니다 — 한 저자 안의 긴장이고 저자가 스스로
  판정을 내렸다.** 다만 판정의 근거가 실증이 아니라 빈도에 대한 저자의 인상("비교적
  드물다")이라는 점은 기록해 둔다. 6장이 조건부 판단을 세운 자리에서 17장이 그 조건의
  분포를 단정해 기본값을 되살리는 구조다.

## 이 KB의 데이터 클래스 판정과 어떻게 만나는가

이 KB에는 이미 데이터만 있는 클래스를 둘러싼 판정이 있다 —
[코드 냄새로서의 데이터 클래스](../concepts/data-class-as-code-smell.md)가 fowler2018의 냄새 항목과
ramalho2022의 유보를 대질해 **모순이 아니라고** 판정한 자리다. **이 장은 그 판정을
뒤집지 않고 셋째 근거를 댄다.**

- 그쪽의 판정은 "데이터 클래스는 비계이거나 중간 표현일 때 정당하다"였다. 이 장은 그
  정당성의 **일반 조건**을 댄다 — 새 함수를 더하는 것이 새 타입을 더하는 것보다 잦은
  부분에서는 자료 구조가 옳은 선택이다(위 [교환의 정식화](#교환의-정식화)).
- 그리고 DTO·액티브 레코드라는 **이름 붙은 실물 둘**을 더한다. 그쪽이 "중간 표현"이라
  부른 것의 구체명이다.
- **갈리는 자리는 없다.** 이 장도 잡종을 최악으로 판정하고, fowler2018도 데이터 클래스가
  행동을 끌어당겨야 할 때를 냄새로 본다. 어느 쪽도 "모든 데이터 클래스는 나쁘다"거나
  "모든 데이터 클래스는 좋다"고 하지 않는다. 그래서 `contradicts`를 걸지 않는다.

## 2차 문헌의 지적 — 이 장의 "자료 구조"는 통용 의미가 아니다

- 지적 (§4):[^qntm2020]

> Martin's definition of "data structure" disagrees with the definition everybody else
> uses. This is a very strange choice of definition, though Martin does at least define
> his term clearly.

- **가치는 인정한다** — **객체를 멍청한 데이터로 보는 것과 메서드를 가진 정교한 추상으로
  보는 것 사이에 명확한 구분을 긋는 것은 정당하고 쓸모 있다** (§4).[^qntm2020]
- 둘째 지적은 부재에 대한 것이다 — **대부분의 우리가 진짜 자료 구조라고 여기는 것,
  즉 배열·연결 리스트·해시 맵·이진 트리·그래프·스택·큐 등을 써서 깨끗하게 코딩하는 것에
  대한 내용이 이 책에 전혀 없다** (§4).[^qntm2020]
- **이 페이지가 그 지적에 대응하는 방식.** 이 페이지는 이 장의 용어를 그대로 옮기되
  원어를 병기해 두었다(자료 구조/data structure) — 이 KB의 규약이 확립 용어 우선이고
  원어 병기를 요구하기 때문이다(SCHEMA §3). **그러나 이 장의 `data structure`는 자료
  구조의 통용 의미(배열·리스트·트리 등 자료의 조직 방식)가 아니라 "데이터를 노출하고
  의미 있는 함수가 없는 코드 단위"라는 좁은 조작적 정의다.** 이 페이지에서 그 낱말을
  읽을 때는 그 정의로만 읽는다. 통용 의미의 자료 구조는 이 KB의 다른 축이 담당한다 —
  [B 트리 구조](../concepts/b-tree-structure.md)·[블룸 필터](../concepts/bloom-filter.md)
  같은 페이지들이다.
- **`contradicts`가 아니다.** 이 지적은 명제의 참거짓 다툼이 아니라 용어 사용에 대한
  것이고, 이 장이 자기 용어를 명시적으로 정의한다는 점은 비판자도 인정한다. 전문은
  [클린 코드 비판](../concepts/clean-code-criticism.md)에 있다.

## 이어지는 페이지

- [클린 코드 비판](../concepts/clean-code-criticism.md) — 이 장의 용어 선택을 지적하는 2차 문헌
- [코드 냄새로서의 데이터 클래스](../concepts/data-class-as-code-smell.md) — 같은 물음의 다른 두
  소스. 이 장이 셋째 근거를 대는 자리
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 게터·세터에 대한 판정이
  일치하는 자리
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — "구현을 감춘다"를 다른
  소스가 다루는 자리
- [결합 끊기](../concepts/decoupling.md) — 디미터 법칙을 실용주의 쪽에서 "부끄럼 타는 코드"로 다루는
  자리
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 액티브 레코드에서 업무 규칙을 갈라내라는
  처방의 실물
- [값 객체와 엔티티](value-objects-and-entities.md) — 자료 구조와 객체 사이를 다른 축으로
  가르는 자리
- [작은 함수](small-functions.md) — 같은 소스 3장. `switch` 처방의 긴장이 시작되는 자리
- [클린 코드의 발견법 목록](../concepts/clean-code-heuristics.md) — `G23`·`G36`의 자리
- [클린 코드](../synthesis/clean-code.md) — 이 소스의 허브

[^qntm2020]: qntm 2020, "It's probably time to stop recommending Clean Code".
    **절 번호는 이 KB가 매긴 것이다** — 규약은
    `it/archive/qntm2020/_progress.yaml` 머리말이 정본이다.

[^martin2008]: Martin 2008, 6장 "Objects and Data Structures"(§"Data Abstraction"
    pp.94–95 · §"Data/Object Anti-Symmetry" pp.95–97 · 각주 1 p.96 · §"The Law of
    Demeter" pp.97–98 · §"Train Wrecks" pp.98–99 · §"Hybrids" p.99 · §"Hiding Structure"
    pp.99–100 · §"Data Transfer Objects" p.100 · §"Active Record" p.101 · §"Conclusion"
    p.101) · 17장 `G23`(p.299) · `G36`(pp.306–307). 쪽은 인쇄판 쪽 번호이며 복원 절차는
    `it/archive/martin2008/_progress.yaml` 머리말이 정본이다. 이 장에는 Listing 6-1부터
    6-7까지 일곱 개의 리스팅이 있다. 펜스로 옮기지 않았다 — 도형 예제 쌍이 이 장의 대표
    코드이나 두 판본을 다 실어야 대비가 성립해 개념당 하나라는 예산(SCHEMA §3)에 맞지
    않고, 시그니처는 인라인 백틱으로 옮겨 검색 키를 남겼다. 도판은 없다. 이 장의 §"Data
    Abstraction" 앞부분(p.93)은 이 스냅샷에서 본문이 비어 있어 리스팅 6-1·6-2의 도입
    문단을 p.94부터 읽었다.

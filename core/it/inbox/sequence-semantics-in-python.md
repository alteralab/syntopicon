---
type: concept
title: 파이썬 시퀀스의 의미론
description: 파이썬이 시퀀스를 균일하게 다루는 방식과 그 균일함이 감추는 갈림들 — 컨테이너 시퀀스와 평면 시퀀스라는 잘 안 쓰이는 축, 리스트 컴프리헨션과 제너레이터 표현식이 무엇을 명시하고 무엇을 아끼는가, 튜플이 레코드이자 불변 리스트라는 두 역할, 언패킹이 색인을 대신하는 이유, 슬라이스에 이름을 붙이는 법, 곱셈 연산자로 중첩 리스트를 만들 때의 함정과 증강 대입이 원자적이지 않다는 사실, 정렬 API가 None을 돌려주는 규약, 그리고 리스트가 답이 아닐 때의 대안들
generated: { by: "claude-opus-5", at: "2026-08-18T05:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬 시퀀스의 의미론

- [균일함이 어디서 오는가](#균일함이-어디서-오는가)
- [잘 안 쓰이는 축 — 컨테이너 시퀀스와 평면 시퀀스](#잘-안-쓰이는-축--컨테이너-시퀀스와-평면-시퀀스)
- [컴프리헨션 — 의도를 명시하는 문법](#컴프리헨션--의도를-명시하는-문법)
- [제너레이터 표현식 — 같은 문법으로 메모리를 아끼기](#제너레이터-표현식--같은-문법으로-메모리를-아끼기)
- [튜플의 두 역할](#튜플의-두-역할)
- [언패킹이 색인을 대신한다](#언패킹이-색인을-대신한다)
- [슬라이싱 — 마지막 항목을 왜 빼는가, 그리고 슬라이스에 이름 붙이기](#슬라이싱--마지막-항목을-왜-빼는가-그리고-슬라이스에-이름-붙이기)
- [이어붙이기와 반복의 함정](#이어붙이기와-반복의-함정)
- [정렬 — list.sort와 sorted](#정렬--listsort와-sorted)
- [리스트가 답이 아닐 때](#리스트가-답이-아닐-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파이썬이 온갖 시퀀스를 같은 문법으로 다루게 해 줄 때, 그 균일함 아래에서
실제로 무엇이 갈리고 어떤 함정이 남는가.**

## 균일함이 어디서 오는가

- 계보가 밝혀져 있다 — 파이썬을 만들기 전 귀도 반 로썸이 기여한 ABC 언어가 그 원산지다.
  **파이썬은 ABC에서 시퀀스의 균일한 처리를 물려받았다. 문자열·리스트·바이트 시퀀스·배열·
  XML 요소·데이터베이스 결과가 반복·슬라이싱·정렬·이어붙이기를 포함한 풍부한 공통 연산
  집합을 공유한다** (2장 도입, p.21).[^ramalho2022]
- 그 균일함이 설계에 갖는 값이 명시된다 — **파이썬에서 쓸 수 있는 시퀀스의 다양함을
  이해하면 바퀴를 다시 발명하지 않게 되고, 그 공통 인터페이스는 기존 및 미래의 시퀀스
  타입을 제대로 지원하고 활용하는 API를 만들도록 우리를 이끈다** (2장 도입,
  p.21).[^ramalho2022] 즉 이 장은 **쓰는 법**이면서 동시에 **API를 짓는 본**이다.

## 잘 안 쓰이는 축 — 컨테이너 시퀀스와 평면 시퀀스

가변/불변은 누구나 아는 축이다. 이 장이 더하는 축이 이것이고, 성능과 함정을 동시에 설명한다.

- 정의 (2장 §"Overview of Built-In Sequences", pp.22–23):[^ramalho2022]
  - **컨테이너 시퀀스(container sequences)** — **서로 다른 타입의 항목을 담을 수 있고 중첩
    컨테이너도 담는다.** `list`·`tuple`·`collections.deque`.
  - **평면 시퀀스(flat sequences)** — **하나의 단순한 타입의 항목만 담는다.** `str`·`bytes`·
    `array.array`.
- 기제 — **컨테이너 시퀀스는 자기가 담은 객체들에 대한 참조를 담고, 그 객체는 어떤 타입이든
  될 수 있다. 반면 평면 시퀀스는 자기 내용의 값을 별개의 파이썬 객체가 아니라 자기 자신의
  메모리 공간에 저장한다** (2장 §"Overview of Built-In Sequences", p.23).[^ramalho2022]
  - 그래서 **평면 시퀀스가 더 조밀하지만, 바이트·정수·부동소수 같은 원시 기계 값만 담을 수
    있다는 제약이 있다** (같은 절, p.23).
  - 수치로도 설명된다 — 가장 단순한 파이썬 객체인 `float`도 헤더에 `ob_refcnt`(참조
    카운트)와 `ob_type`(타입 포인터)를 갖고 값 `ob_fval`을 담는다. **64비트 빌드에서 그
    필드들이 각각 8바이트다. 부동소수 배열이 부동소수 튜플보다 훨씬 조밀한 이유가
    그것이다** (같은 절, p.23).
- 조문 — **가변인가 불변인가, 컨테이너인가 평면인가. 이 공통 특질들을 염두에 두어라. 한
  시퀀스 타입에 대해 아는 것을 다른 것들로 확장하는 데 도움이 된다**
  (2장 §"Overview of Built-In Sequences", p.24).[^ramalho2022]
- 그리고 이 두 축이 뒤에서 함정을 예고한다 — 장 요약이 그것을 못 박는다: **불행히도 파이썬에는
  완전히 안전한 불변 컨테이너 시퀀스 타입이 없다. "불변"인 튜플조차 리스트나 사용자 정의
  객체 같은 가변 항목을 담으면 그 값이 바뀔 수 있다** (2장 §"Chapter Summary",
  p.70).[^ramalho2022] 전문은 [객체 참조와 가변성](../concepts/object-references-and-mutability.md)에 있다.
- 구상 타입이 ABC를 상속하지는 않는다는 사실도 여기서 나온다 — **내장 구상 시퀀스 타입들은
  실제로 `Sequence`와 `MutableSequence` 추상 기반 클래스를 상속하지 않고, 그 ABC에 등록된
  가상 하위 클래스(virtual subclasses)다** (2장 §"Overview of Built-In Sequences",
  p.24).[^ramalho2022] 그래서 `issubclass(tuple, abc.Sequence)`가 `True`다. 그 기제는
  [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md)가 다룬다.

## 컴프리헨션 — 의도를 명시하는 문법

- 주장 — 리스트 컴프리헨션(listcomp)이 읽기 좋은 이유는 짧아서가 아니라 **의도가 명시적**이기
  때문이다. **`for` 루프는 온갖 다른 일에 쓰일 수 있다: 시퀀스를 훑어 세거나 항목을 고르거나,
  집계(합·평균)를 계산하거나, 그 밖의 수많은 일. (…) 대조적으로 listcomp는 더 명시적이다.
  그 목표는 언제나 새 리스트를 짓는 것이다** (2장 §"List Comprehensions and Readability",
  p.25).[^ramalho2022]
- **⚠ 그리고 곧바로 남용의 경계가 그어진다** — **물론 리스트 컴프리헨션을 남용해 정말로
  이해할 수 없는 코드를 쓰는 것도 가능하다. 나는 부수 효과를 위해 코드 블록을 반복하려고만
  listcomp를 쓴 파이썬 코드를 본 적이 있다. 생산된 리스트로 무언가를 하지 않을 거라면 그
  문법을 쓰면 안 된다. 또한 짧게 유지하려고 애써라. 리스트 컴프리헨션이 두 줄을 넘으면 아마
  쪼개거나 평범한 옛날식 `for` 루프로 다시 쓰는 편이 최선일 것이다**
  (2장 §"List Comprehensions and Readability", p.26).[^ramalho2022]
  - 그 뒤에 붙는 한 줄이 이 KB의 다른 조항들과 같은 성격이다 — **최선의 판단을 써라:
    파이썬에서도 영어에서와 마찬가지로, 명료한 글쓰기에 딱 부러지는 규칙은 없다**
    (같은 절, p.26). [코드 냄새](../concepts/code-smells.md)가 "임계값이 아니라 냄새"라고 말하는 것과
    같은 자리다. #hypothesis 저자가 그렇게 연결하지는 않았다.
- **지역 스코프가 생겼다는 것이 파이썬 3의 변화다** — **파이썬 3에서 리스트 컴프리헨션,
  제너레이터 표현식, 그 형제인 집합·딕셔너리 컴프리헨션은 `for` 절에서 대입된 변수를 담을
  지역 스코프를 갖는다** (2장 §"Local Scope Within Comprehensions and Generator
  Expressions", p.26).[^ramalho2022]
  - 예외가 하나 있다 — **바다코끼리 연산자(Walrus operator) `:=`로 대입된 변수는 그
    컴프리헨션이나 표현식이 반환된 뒤에도 접근 가능하다 — 함수 안의 지역 변수와 달리**
    (같은 절, p.26). PEP 572가 `:=` 대상의 스코프를 둘러싼 함수로 규정한다.
- `map`·`filter`와의 비교도 정리된다 — **listcomp는 `map`과 `filter` 함수가 하는 모든 것을,
  기능이 모자란 파이썬 `lambda`의 곡예 없이 해낸다** (2장 §"Listcomps Versus map and
  filter", p.27).[^ramalho2022]
  - **⚠ 속도에 대한 통념이 기각된다** — **나는 `map`과 `filter`가 동등한 listcomp보다 빠르다고
    믿곤 했지만, Alex Martelli가 적어도 위 예제들에서는 그렇지 않다고 지적했다**
    (같은 절, p.27).

## 제너레이터 표현식 — 같은 문법으로 메모리를 아끼기

- 규정 — **튜플·배열·다른 종류의 시퀀스를 초기화할 때 listcomp에서 출발할 수도 있지만,
  genexp(제너레이터 표현식)가 메모리를 아낀다. 리스트 전체를 지어서 다른 생성자에 먹이는
  대신 이터레이터 프로토콜로 항목을 하나씩 내놓기 때문이다** (2장 §"Generator Expressions",
  p.29).[^ramalho2022] 문법은 listcomp와 같고 대괄호 대신 괄호를 쓴다.
- 규모가 클 때의 차이가 명시된다 — 데카르트 곱 예에서 **여섯 항목짜리 티셔츠 리스트는 결코
  메모리에 만들어지지 않는다. (…) 데카르트 곱에 쓰인 두 리스트가 각각 천 개 항목을 가졌다면,
  제너레이터 표현식을 쓰는 것이 `for` 루프에 먹이려고 백만 항목짜리 리스트를 짓는 비용을
  아꼈을 것이다** (2장 §"Generator Expressions", p.30).[^ramalho2022]
- 문법 요령 하나 — **제너레이터 표현식이 함수 호출의 유일한 인자면 둘러싸는 괄호를 겹쳐 쓸
  필요가 없다** (2장 §"Generator Expressions", p.29).[^ramalho2022] `array` 생성자처럼
  인자가 둘이면 괄호가 필수다.

## 튜플의 두 역할

- 조문 — **어떤 파이썬 입문서는 튜플을 "불변 리스트"로 소개하지만 그것은 튜플을 싸게 파는
  것이다. 튜플은 두 몫을 한다: 불변 리스트로도 쓰이고, 필드 이름이 없는 레코드로도 쓰인다**
  (2장 §"Tuples Are Not Just Immutable Lists", p.30).[^ramalho2022]
- **① 레코드로서** — **튜플은 레코드를 담는다: 튜플의 각 항목이 한 필드의 데이터를 담고,
  항목의 위치가 그 의미를 준다** (2장 §"Tuples as Records", p.30).[^ramalho2022]
  - 그래서 규칙이 하나 따라온다 — **튜플을 필드 모음으로 쓸 때 항목의 개수는 보통 고정돼
    있고 그 순서는 언제나 중요하다** (같은 절, p.31). 정렬하면 정보가 파괴된다.
  - 그리고 클래스를 만들지 않아도 되는 조건이 붙는다 — **필드 이름을 붙이자고 클래스를 만드는
    수고를 들일 필요가 없는 경우가 흔하다. 특히 언패킹을 활용하고 필드 접근에 색인을 쓰지
    않는다면 그렇다** (2장 §"Tuples as Records", p.32).[^ramalho2022] 이름이 필요해지는
    순간의 답이 [데이터 클래스 빌더](../concepts/data-class-builders.md)다.
- **② 불변 리스트로서** — 이득이 둘로 계상된다 (2장 §"Tuples as Immutable Lists",
  p.32):[^ramalho2022]
  - **명료성(Clarity)** — **코드에서 튜플을 보면 그 길이가 결코 바뀌지 않는다는 것을 안다.**
  - **성능(Performance)** — **튜플은 같은 길이의 리스트보다 메모리를 덜 쓰고, 파이썬이 몇
    가지 최적화를 하게 해 준다.**
  - 그 최적화의 내역이 Raymond Hettinger를 인용해 넷으로 열거된다 (같은 절,
    p.34):[^ramalho2022] 튜플 리터럴은 바이트코드 하나로 상수를 만들지만 리스트 리터럴은
    원소를 하나씩 스택에 밀고 리스트를 짓는다 · `tuple(t)`는 같은 `t`의 참조를 돌려주지만
    `list(l)`은 새 복사본을 만들어야 한다 · 튜플은 길이가 고정돼 필요한 만큼 정확히
    할당되지만 리스트는 앞으로의 추가를 위해 여유를 두고 할당된다 · 튜플은 참조 배열을 자기
    구조체 안에 두지만 리스트는 다른 곳에 있는 참조 배열에 대한 포인터를 갖고, **그 간접이
    CPU 캐시를 덜 효과적으로 만든다.**
  - **⚠ 그러나 불변성은 참조에만 걸린다** — **튜플의 불변성은 그 안에 담긴 참조에만
    적용된다. 튜플 안의 참조는 삭제되거나 교체될 수 없다. 그러나 그 참조 중 하나가 가변
    객체를 가리키고 그 객체가 바뀌면, 튜플의 값이 바뀐다**
    (2장 §"Tuples as Immutable Lists", p.32).[^ramalho2022] 판정 방법은 `hash(t)`이고,
    자세한 것은 [객체 참조와 가변성](../concepts/object-references-and-mutability.md)에 있다.

## 언패킹이 색인을 대신한다

- 왜 중요한가 — **언패킹이 중요한 이유는 시퀀스에서 원소를 뽑아내는 데 불필요하고 오류를
  부르는 색인 사용을 피하기 때문이다. 또한 언패킹은 어떤 반복 가능 객체에도 동작한다 —
  색인 표기(`[]`)를 지원하지 않는 이터레이터를 포함해서** (2장 §"Unpacking Sequences and
  Iterables", p.35).[^ramalho2022]
- 표기 셋이 열거된다 (2장 §"Unpacking Sequences and Iterables", pp.35–37):[^ramalho2022]
  - **병렬 대입(parallel assignment)** — `latitude, longitude = lax_coordinates`. 임시
    변수 없는 값 교환 `b, a = a, b`도 여기 속한다.
  - **호출 시 `*` 접두** — `divmod(*t)`. 이것이 **함수가 호출자에게 편리한 방식으로 여러
    값을 돌려주게 해 주는** 자리이기도 하다.
  - **`*`로 남는 항목 잡기** — `a, b, *rest = range(5)`. 파이썬 3에서 `*args`의 아이디어가
    병렬 대입으로 확장된 것이고, **`*` 접두는 정확히 한 변수에만 붙일 수 있지만 어느
    위치에도 올 수 있다**(`a, *body, c, d` / `*head, b, c, d`).
  - PEP 448 이후로는 함수 호출에서 `*`를 여러 번 쓸 수 있고 리스트·튜플·집합 리터럴 안에서도
    쓸 수 있다 (2장 §"Unpacking with * in Function Calls and Sequence Literals", p.37).
- **중첩 언패킹**도 된다 — `(a, b, (c, d))`처럼 대상이 중첩을 쓸 수 있고 **값이 같은 중첩
  구조를 가지면 파이썬이 알아서 맞춘다** (2장 §"Nested Unpacking", p.37).[^ramalho2022]
  - 대상이 리스트여도 되는데 쓸 자리가 드물다 — 저자가 아는 유일한 예가 **한 행만 돌려주는
    데이터베이스 질의**다: `[record] = query_returning_single_row()`가 언패킹과 동시에
    결과가 하나뿐임을 보증한다 (같은 절, p.38).
  - 그 자리에서 튜플의 문법 함정이 하나 지적된다 — **한 항목짜리 튜플은 끝에 쉼표를 붙여
    써야 한다.** `(record,)`·`((field,),)`이고, **쉼표를 잊으면 조용한 버그를 얻는다**
    (같은 절, p.38).

## 슬라이싱 — 마지막 항목을 왜 빼는가, 그리고 슬라이스에 이름 붙이기

- 마지막 항목을 빼는 관례의 이득이 셋으로 정리된다 (2장 §"Why Slices and Ranges Exclude the
  Last Item", p.47):[^ramalho2022] 끝 위치만 줬을 때 길이를 바로 안다(`range(3)`·`my_list[:3]`
  둘 다 세 항목) · 시작과 끝이 있을 때 길이가 `stop-start`다 · 어느 색인 `x`에서든
  `my_list[:x]`와 `my_list[x:]`로 겹침 없이 둘로 가를 수 있다.
  - 근거의 출처가 밝혀져 있다 — **이 관례에 대한 최선의 논변은 네덜란드 컴퓨터 과학자
    Edsger W. Dijkstra가 썼다**(§"Further Reading"의 마지막 참고 문헌, "Why Numbering
    Should Start at Zero") (같은 절, p.48).
- `a:b:c` 표기는 `[]` 안에서만 유효하고 **`slice(a, b, c)` 객체를 만든다**
  (2장 §"Slice Objects", p.48).[^ramalho2022] `seq[start:stop:step]`을 평가하려고 파이썬은
  `seq.__getitem__(slice(start, stop, step))`을 부른다 —
  [파이썬 데이터 모델](../concepts/python-data-model.md)의 던더가 여기서도 바닥이다.
- **그래서 슬라이스에 이름을 붙일 수 있다.** 저자의 표현이 그 값을 정확히 짚는다 — **자기
  시퀀스 타입을 구현하지 않더라도 슬라이스 객체를 아는 것은 유용하다. 스프레드시트가 셀
  범위에 이름을 붙이게 해 주듯 슬라이스에 이름을 붙일 수 있게 해 주기 때문이다**
  (2장 §"Slice Objects", p.48).[^ramalho2022] 고정폭 텍스트를 파싱할 때 하드코딩된 슬라이스
  대신 쓴다 (2장 예제 2-13, p.49).

  ```python
  SKU = slice(0, 6)
  DESCRIPTION = slice(6, 40)
  UNIT_PRICE = slice(40, 52)
  QUANTITY = slice(52, 55)
  ITEM_TOTAL = slice(55, None)

  line_items = invoice.split('\n')[2:]
  for item in line_items:
      print(item[UNIT_PRICE], item[DESCRIPTION])
  ```

  - 이것이 [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)가 말하는 것의
    아주 작은 실물이다 — `item[40:52]`가 `item[UNIT_PRICE]`가 되면 읽는 사람이 코드를
    거슬러 올라갈 필요가 없어진다. #hypothesis 저자가 그렇게 연결하지는 않았다.
- 슬라이스는 **쓰기 쪽에서도 쓰인다** — **가변 시퀀스는 대입문의 왼쪽이나 `del` 문장의
  대상으로 슬라이스 표기를 써서 제자리에서 접목·절제·수정할 수 있다**
  (2장 §"Assigning to Slices", p.50).[^ramalho2022] 단서 하나: **대입의 대상이 슬라이스면
  오른쪽은 항목이 하나뿐이더라도 반복 가능 객체여야 한다** (같은 절, p.50).

## 이어붙이기와 반복의 함정

- 기본 규칙 — **`+`와 `*`는 언제나 새 객체를 만들고 자기 피연산자를 결코 바꾸지 않는다**
  (2장 §"Using + and * with Sequences", p.51).[^ramalho2022]
- **⚠ 그런데 `a * n`에서 `a`가 가변 항목을 담고 있으면 결과가 놀랍다** — **`my_list = [[]] * 3`으로
  리스트의 리스트를 초기화하려고 하면 같은 안쪽 리스트에 대한 참조 셋을 가진 리스트가
  된다** (2장 §"Using + and * with Sequences" §Warning, p.51).[^ramalho2022]
  - 실물: `weird_board = [['_'] * 3] * 3`에 `weird_board[1][2] = 'O'`를 하면 세 행이 전부
    바뀐다 — **바깥 리스트가 같은 안쪽 리스트에 대한 참조 셋으로 이루어져 있기 때문이다**
    (2장 §"Building Lists of Lists" 예제 2-15, p.52).[^ramalho2022]
  - 올바른 방법은 리스트 컴프리헨션이다 — `board = [['_'] * 3 for i in range(3)]`가 **매
    반복마다 새 행을 지어 `board`에 붙인다** (같은 절, p.52).
- **증강 대입 `+=`는 대상의 가변성에 따라 다르게 동작한다** — **`+=`를 동작하게 만드는
  특수 메서드는 `__iadd__`("제자리 덧셈")다. 그러나 `__iadd__`가 구현돼 있지 않으면
  파이썬은 `__add__`를 부르는 것으로 물러선다** (2장 §"Augmented Assignment with
  Sequences", p.53).[^ramalho2022] 가변 시퀀스는 제자리에서 바뀌고, 불변 시퀀스는 새
  객체가 만들어져 다시 묶인다.
  - 그래서 불변 시퀀스의 반복 이어붙이기는 비효율이다 — **새 항목을 붙이는 대신 인터프리터가
    전체 대상 시퀀스를 복사해 새것을 만들어야 하기 때문이다** (같은 절, p.54). 예외가
    `str`인데, **`+=`를 루프에서 쓰는 문자열 만들기가 실제 코드베이스에 너무 흔해 CPython이
    이 사용 사례에 최적화돼 있다** (같은 절 각주 8, p.54).
- **`+=` 수수께끼가 이 장의 가장 유명한 구석이다** — `t = (1, 2, [30, 40])`에 `t[2] += [50, 60]`을
  하면 **`TypeError`가 나면서 동시에 튜플의 값이 바뀐다** (2장 §"A += Assignment Puzzler"
  예제 2-17, p.55).[^ramalho2022] 바이트코드가 그 이유를 설명한다: `INPLACE_ADD`가 먼저
  성공하고(가변 리스트라서) 그다음 `STORE_SUBSCR`가 실패한다(불변 튜플이라서).
  - 저자가 뽑는 교훈 셋이 이 페이지의 조문이다 (2장 §"A += Assignment Puzzler",
    p.56):[^ramalho2022]
    - **튜플에 가변 항목을 넣지 마라.**
    - **증강 대입은 원자적 연산이 아니다 — 방금 그것이 일의 일부를 한 뒤에 예외를 던지는
      것을 보았다.**
    - **파이썬 바이트코드를 들여다보는 것은 그리 어렵지 않고, 내부에서 무슨 일이 일어나는지
      보는 데 도움이 될 수 있다.**
  - 다만 빈도에 대한 정직한 단서도 붙는다 — **이것은 꽤 구석 사례다. 파이썬을 쓴 20년 동안
    나는 이 이상한 동작이 실제로 누군가를 문 것을 본 적이 없다** (같은 절, p.56).

## 정렬 — list.sort와 sorted

- **API 규약이 이 절의 값이다** — `list.sort`는 제자리에서 정렬하고 `None`을 돌려준다.
  **이것은 중요한 파이썬 API 관례다: 객체를 제자리에서 바꾸는 함수나 메서드는 수신자가
  바뀌었고 새 객체가 만들어지지 않았음을 호출자에게 분명히 하기 위해 `None`을 돌려주어야
  한다** (2장 §"list.sort Versus the sorted Built-In", p.56).[^ramalho2022]
  `random.shuffle(s)`도 같다.
  - 대가도 계상된다 — **제자리 변경을 알리려고 `None`을 돌려주는 관례에는 단점이 있다:
    그런 메서드는 호출을 이어 붙일 수 없다. 대조적으로 새 객체를 돌려주는 메서드(예: 모든
    `str` 메서드)는 유창한 인터페이스(fluent interface) 방식으로 이어 붙일 수 있다**
    (같은 절, p.56).
  - 이것이 이 KB의 [부수 효과 없는 함수](side-effect-free-functions.md)가 말하는 명령/질의
    분리를 **표준 라이브러리가 반환값으로 표시하는** 자리다. #hypothesis 두 소스가 서로를
    참조한 적은 없다.
- `sorted`는 반대다 — **어떤 반복 가능 객체든 인자로 받고, 어떤 타입을 주든 언제나 새로
  만들어진 리스트를 돌려준다** (2장 §"list.sort Versus the sorted Built-In",
  p.57).[^ramalho2022]
- 둘 다 키워드 전용 인자 둘을 받는다 (같은 절, p.57):[^ramalho2022] `reverse`와 **`key` —
  각 항목에 적용돼 정렬 키를 만들어 내는 한 인자짜리 함수.** `key=str.lower`가 대소문자
  구분 없는 정렬을, `key=len`이 길이순 정렬을 준다.
  - **`key`는 `min()`·`max()`에도 쓸 수 있고** `itertools.groupby()`·`heapq.nlargest()`
    같은 표준 라이브러리 함수에도 쓸 수 있다 (같은 절, p.57).
- **정렬이 안정(stable)하다** — 즉 **같다고 비교되는 항목들의 상대 순서를 보존한다**
  (같은 절, p.57).[^ramalho2022] 알고리즘 이름은 Tim Peters의 이름을 딴 Timsort다.
- **⚠ 문자열 정렬에는 단서가 붙는다** — **기본적으로 파이썬은 문자열을 문자 코드에 따라
  사전식으로 정렬한다. 그 말은 ASCII 대문자가 소문자보다 앞에 오고, 비ASCII 문자는 말이
  되는 방식으로 정렬되지 않기 쉽다는 뜻이다** (같은 절 §Warning, p.58).[^ramalho2022]
  제대로 하는 법은 [텍스트와 바이트의 경계](text-versus-bytes.md)에 있다.

## 리스트가 답이 아닐 때

- 규정 — **`list` 타입은 유연하고 쓰기 쉽지만, 구체적인 요구에 따라 더 나은 선택지가 있다**
  (2장 §"When a List Is Not the Answer", p.59).[^ramalho2022]
- **`array.array`** — **리스트가 숫자만 담는다면 `array.array`가 더 효율적인 대체다.** 배열은
  가변 시퀀스 연산 전부를 지원하면서 `.frombytes`·`.tofile` 같은 빠른 적재·저장 메서드를
  더한다 (2장 §"Arrays", p.59).[^ramalho2022]
  - 만들 때 **타입 코드(typecode)**를 준다 — `array('b')`면 각 항목이 1바이트에 저장되고
    정수로 해석된다. **큰 수열에는 이것이 메모리를 많이 아낀다. 그리고 파이썬은 그 배열의
    타입에 맞지 않는 어떤 수도 넣게 두지 않는다** (같은 절, p.59).
  - 실측 수치가 붙는다 — 천만 개의 배정밀도 부동소수에 대해 `array.fromfile`이 **텍스트
    파일에서 읽는 것보다 거의 60배 빠르고**, `array.tofile`이 한 줄에 하나씩 쓰는 것보다
    약 7배 빠르며, 이진 파일이 8천만 바이트인 데 비해 텍스트 파일은 181,515,739
    바이트다 (2장 §"Arrays", p.60).[^ramalho2022]
- **`collections.deque`** — **`.append`와 `.pop` 메서드는 리스트를 스택이나 큐로 쓸 수 있게
  한다(`.append`와 `.pop(0)`을 쓰면 FIFO). 그러나 리스트의 머리(0 색인 쪽)에서 넣고 빼는
  것은 비싸다. 리스트 전체가 메모리에서 밀려야 하기 때문이다**
  (2장 §"Deques and Other Queues", p.67).[^ramalho2022]
  - 그래서 **`collections.deque`는 양끝에서 빠르게 넣고 빼도록 설계된 스레드 안전한
    양방향 큐다. "마지막으로 본 항목들" 같은 목록을 유지해야 할 때도 갈 길인데, deque가
    경계를 둘 수 있기 때문이다 — 즉 고정된 최대 길이로 만들 수 있다. 경계 있는 deque가
    가득 찼을 때 새 항목을 더하면 반대쪽 끝의 항목을 버린다** (같은 절, p.67).
  - **⚠ 숨은 비용이 명시된다** — **deque는 리스트 메서드 대부분을 구현하고 `popleft`·`rotate`
    같은 자기 설계에 특화된 것을 몇 개 더한다. 그러나 숨은 비용이 있다: deque의 가운데에서
    항목을 제거하는 것은 그리 빠르지 않다. 그것은 정말로 양끝에서 붙이고 빼는 데
    최적화돼 있다** (같은 절, p.68).
  - 동시성 쪽 단서도 있다 — **`append`와 `popleft` 연산은 원자적이므로 deque는 락 없이
    다중 스레드 애플리케이션에서 FIFO 큐로 안전하게 쓸 수 있다** (같은 절, p.68).
- **`set`** — **코드가 컬렉션 안에 항목이 있는지 자주 검사한다면(예: `item in
  my_collection`) `my_collection`에 집합을 쓰는 것을 고려하라. 특히 많은 항목을 담고
  있다면. 집합은 빠른 멤버십 검사에 최적화돼 있다**
  (2장 §"When a List Is Not the Answer", p.59).[^ramalho2022] 자세한 것은
  [딕셔너리와 집합](../concepts/dictionaries-and-sets.md)에 있다.
- 그 밖의 큐 구현들도 열거된다 (2장 §"Deques and Other Queues", p.69):[^ramalho2022]
  `queue`(스레드 간 통신용 동기화 클래스들 — **가득 차면 항목을 버리는 대신 삽입이
  블록되고, 그것이 살아 있는 스레드 수를 조절하는 데 유용하다**), `multiprocessing`(프로세스
  간 통신용), `asyncio`(비동기 작업 관리용), `heapq`(큐 클래스가 아니라 가변 시퀀스를 힙 큐로
  쓰게 해 주는 함수들).

## 이어지는 페이지

- [객체 참조와 가변성](../concepts/object-references-and-mutability.md) — **같은 부의 마지막 장.**
  위 함정들(`[[]] * 3`·`+=` 수수께끼·튜플의 상대적 불변성)의 기제가 전부 그쪽에 있다
- [딕셔너리와 집합](../concepts/dictionaries-and-sets.md) — 순서 없는 컬렉션 쪽. 해시 가능성이라는
  요구가 여기의 "튜플에 가변 항목을 넣지 마라"와 만난다
- [텍스트와 바이트의 경계](text-versus-bytes.md) — `str`과 `bytes`라는 평면 시퀀스 둘의
  특수 사정, 그리고 문자열을 제대로 정렬하는 법
- [데이터 클래스 빌더](../concepts/data-class-builders.md) — 튜플을 레코드로 쓰다가 필드에 이름이
  필요해졌을 때
- [파이썬 데이터 모델](../concepts/python-data-model.md) — 슬라이싱·반복·`in`이 어떤 특수 메서드로
  받쳐지는가
- [부수 효과 없는 함수](side-effect-free-functions.md) — `sort`가 `None`을 돌려주는
  관례의 원리 쪽
- [알고리즘 속도](../concepts/algorithm-speed.md) — 자료 구조 선택이 복잡도에 걸리는 자리
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 2장 "An Array of Sequences", pp.21–75(도입 pp.21–22 ·
    §"Overview of Built-In Sequences" pp.22–24 · §"List Comprehensions and Generator
    Expressions" pp.25–30과 그 아래 §"List Comprehensions and Readability" pp.25–26·
    §"Local Scope Within Comprehensions and Generator Expressions" pp.26–27·
    §"Listcomps Versus map and filter" p.27·§"Cartesian Products" pp.27–29·
    §"Generator Expressions" pp.29–30 · §"Tuples Are Not Just Immutable Lists" pp.30–35과
    그 아래 §"Tuples as Records" pp.30–32·§"Tuples as Immutable Lists" pp.32–34·
    §"Comparing Tuple and List Methods" pp.34–35 · §"Unpacking Sequences and Iterables"
    pp.35–38과 그 아래 §"Using * to Grab Excess Items" pp.36–37·§"Unpacking with * in
    Function Calls and Sequence Literals" p.37·§"Nested Unpacking" pp.37–38 ·
    §"Slicing" pp.47–50과 그 아래 §"Why Slices and Ranges Exclude the Last Item" pp.47–48·
    §"Slice Objects" pp.48–49·§"Multidimensional Slicing and Ellipsis" pp.49–50·
    §"Assigning to Slices" p.50 · §"Using + and * with Sequences" pp.50–56과 그 아래
    §"Building Lists of Lists" pp.51–52·§"Augmented Assignment with Sequences" pp.53–54·
    §"A += Assignment Puzzler" pp.54–56 · §"list.sort Versus the sorted Built-In"
    pp.56–58 · §"When a List Is Not the Answer" pp.59–70과 그 아래 §"Arrays" pp.59–61·
    §"Deques and Other Queues" pp.67–70 · §"Chapter Summary" pp.70–71 · 각주 8 p.54).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측은
    `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    **반입하지 않은 것**: §"Pattern Matching with Sequences"(pp.38–46, 제어 흐름 문법이라
    범위 밖 — `_progress.yaml`의 `skipped` 참조)와 §"Memory Views"·§"NumPy"(pp.62–67,
    수치 계산 축). 표 2-1(list/tuple 메서드)·2-3(list/array)·2-4(list/deque)는 원문이 API
    대조표라 옮기지 않고 본문 서술로 요지만 풀었다 — 전수 목록이 필요하면 스냅샷을 본다.
    Figure 2-1(튜플과 배열의 메모리 도해)·2-2·2-4·2-5는 이미지로 조판돼 있어 딸린 캡션과
    본문 서술만 옮겼다. 코드 펜스는 예제 2-13의 슬라이스 이름 붙이기인데, 원문이 콘솔
    세션이라 `>>>` 프롬프트만 제거했다(깎기이고 보탠 줄은 없다).

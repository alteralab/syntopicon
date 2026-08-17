---
type: concept
title: yield from과 고전 코루틴
description: 제너레이터가 다른 제너레이터에 일을 넘기는 문법과 그것이 만드는 세 자리(클라이언트·위임 제너레이터·부제너레이터), 재귀 순회가 중첩 루프를 대체하는 자리, 그리고 같은 물건을 반대 방향으로 쓰는 고전 코루틴 — 시동·send·close의 규약, 반환값이 예외에 실려 나오는 기괴한 핵, 손으로 몰면 안 된다는 저자의 기각, 그리고 Generator 타입의 세 매개변수가 공변과 반변으로 갈리는 이유
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# yield from과 고전 코루틴

- [세 자리 — 클라이언트·위임자·부제너레이터](#세-자리--클라이언트위임자부제너레이터)
- [중첩 루프가 재귀로 접힌다](#중첩-루프가-재귀로-접힌다)
- [같은 물건, 반대 방향](#같은-물건-반대-방향)
- [시동·send·close](#시동sendclose)
- [반환값은 예외에 실려 나온다](#반환값은-예외에-실려-나온다)
- [손으로 몰지 마라](#손으로-몰지-마라)
- [타입 매개변수 셋이 갈리는 이유](#타입-매개변수-셋이-갈리는-이유)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **제너레이터가 만든 값이 여러 겹의 함수를 거쳐 나와야 할 때, 그 겹을 어떻게
없애며, 반대로 값을 안으로 밀어 넣으려면 무엇이 달라지는가.**

## 세 자리 — 클라이언트·위임자·부제너레이터

- 도입 배경 — **`yield from` 식 문법은 제너레이터가 부제너레이터에게 일을 위임할 수 있게
  하려고 파이썬 3.3에 도입됐다** (17장 §"Subgenerators with yield from",
  p.632).[^ramalho2022] 그 전에는 다른 제너레이터가 만든 값을 내놓아야 할 때 `for` 루프를
  썼다.
- 역할 이름이 셋이다 — **`for` 루프가 클라이언트 코드(client code), `gen`이 위임
  제너레이터(delegating generator), `sub_gen`이 부제너레이터(subgenerator)다** (같은 절,
  p.632).[^ramalho2022]
- 통로가 열리는 방식이 요점이다 (같은 절, pp.632–633):[^ramalho2022]
  - **`yield from`이 `gen`을 멈추고, `sub_gen`이 소진될 때까지 대신 일한다.**
  - **`sub_gen`이 내놓는 값은 `gen`을 곧장 통과해 클라이언트 `for` 루프에 닿는다.**
  - **그동안 `gen`은 중단돼 있고 자기를 통과하는 값을 볼 수 없다.**
  - **`sub_gen`이 끝나야 `gen`이 재개된다.**
- 값 하나가 예외로 반대 방향으로 온다 — **부제너레이터가 값을 가진 `return` 문을 담고
  있으면, 그 값은 `yield from`을 식의 일부로 써서 위임 제너레이터가 붙잡을 수 있다**
  (같은 절, p.633).[^ramalho2022] `result = yield from sub_gen()`이 그 형태다.
- 단순히 바꿔 쓰기만 하면 이득이 크지 않다 — 저자가 `itertools.chain`을 손으로 다시 짜
  보이고는 스스로 판정한다: **이 예에서 `yield from`의 사용은 옳고 코드도 더 잘 읽히지만,
  실질적 이득이 적은 문법 설탕처럼 보인다** (17장 §"Reinventing chain",
  p.634).[^ramalho2022] 진짜 값은 다음 두 자리에 있다.

## 중첩 루프가 재귀로 접힌다

- 저자가 파이썬 예외 계층을 깊이 우선으로 훑는 트리 순회를 "아기 걸음"으로 짓는다. 레벨
  3까지 손으로 늘리고 나면 규칙이 드러난다 — **레벨 *N*의 하위 클래스를 얻으려고 `for`
  루프를 돈다. 루프를 돌 때마다 레벨 *N*의 하위 클래스를 내놓고, 레벨 *N*+1을 방문하려고
  또 다른 `for` 루프를 시작한다** (17장 §"Traversing a Tree", p.638).[^ramalho2022]
- 그 중첩이 `yield from`으로 접힌다. 최종 형태가 네 줄이다 (예제 17-33,
  p.639):[^ramalho2022]

  ```python
  def tree(cls, level=0):
      yield cls.__name__, level
      for sub_cls in cls.__subclasses__():
          yield from tree(sub_cls, level+1)


  def display(cls):
      for cls_name, level in tree(cls):
          indent = ' ' * 4 * level
          print(f'{indent}{cls_name}')


  if __name__ == '__main__':
      display(BaseException)
  ```

  - 이 판은 **깊이에 상관없이 트리를 훑을 수 있고, 제한은 파이썬의 재귀 한계뿐이다.
    기본 한계는 대기 중인 함수 1,000개를 허용한다** (같은 절, p.638).[^ramalho2022]
  - 종료 조건이 눈에 안 보이는 자리가 이 코드의 교육적 요점이다 — **재귀에 관한 좋은
    자습서라면 무한 재귀를 피하기 위한 기저 사례(base case)의 중요성을 강조할 것이다.
    (…) 여기 `sub_tree`에는 `if`가 없지만 `for` 루프 안에 암묵적 조건이 있다:
    `cls.__subclasses__()`가 빈 리스트를 돌려주면 루프 몸통이 실행되지 않으므로 재귀
    호출이 일어나지 않는다** (같은 절, p.638).[^ramalho2022]
- 그리고 이 문법의 진짜 값이 예고된다 — **`yield from`이 위임 제너레이터를 건너뛰고
  부제너레이터를 클라이언트 코드에 곧장 잇는다. 그 연결은 제너레이터가 코루틴으로 쓰여
  값을 만들 뿐 아니라 클라이언트 코드로부터 소비하기도 할 때 정말로 중요해진다** (같은
  절, p.639).[^ramalho2022]

## 같은 물건, 반대 방향

- 코루틴의 정체 — **코루틴은 실은 몸통에 `yield` 키워드를 써서 만든 제너레이터 함수다.
  그리고 코루틴 객체는 물리적으로 제너레이터 객체다** (17장 §"Classic Coroutines",
  p.642).[^ramalho2022] C 층에서 같은 구현을 공유하지만 **파이썬에서 제너레이터와 코루틴의
  쓰임새가 워낙 달라서 타입 힌트를 붙이는 방법도 둘로 갈린다.**
- 저자가 그 이중성을 튜플에 빗댄다 — 튜플을 레코드로 쓸 때와 불변 리스트로 쓸 때 타입
  힌트가 갈리는 것과 같은 사정이라는 것이다 (같은 절, pp.641–642).[^ramalho2022]
- 어휘 자체가 오염돼 있다는 경고가 붙는다 — **파이썬 공식 문서와 표준 라이브러리가 이제
  제너레이터를 코루틴으로 쓰는 것을 가리키는 데 일관되지 않은 용어를 쓰고 있어서, 나는
  더 새로운 "네이티브 코루틴(native coroutine)" 객체와 대비하려고 "고전 코루틴(classic
  coroutine)"이라는 한정어를 채택할 수밖에 없었다** (같은 절, p.641).[^ramalho2022]
  PEP 342는 폐기되지 않았고 고전 코루틴은 원래 설계대로 여전히 동작하지만 **asyncio는
  더 이상 그것을 지원하지 않는다.**
- 섞지 말라는 조문이 David Beazley의 강의 슬라이드에서 통째로 인용된다 (같은 절,
  p.643):[^ramalho2022]

> - Generators produce data for iteration
> - Coroutines are consumers of data
> - To keep your brain from exploding, don't mix the two concepts together
> - Coroutines are not related to iteration
> - Note: There is a use of having `yield` produce a value in a coroutine, but it's not
>   tied to iteration.

- 코루틴이 매력적인 이유가 상태 보관에 있다 — **코루틴에서는 `total`과 `count`가 지역
  변수일 수 있다: 코루틴이 다음 `.send()`를 기다리며 중단돼 있는 동안 문맥을 유지하는 데
  인스턴스 속성도 클로저도 필요 없다. 그래서 코루틴이 비동기 프로그래밍에서 콜백의 매력적인
  대체물이다 — 활성화 사이에 지역 상태를 유지하기 때문이다** (17장 §"Example: Coroutine to
  Compute a Running Average", p.644).[^ramalho2022]

## 시동·send·close

- 시동(priming) — **`next()`나 `.send(None)`을 불러 첫 `yield`까지 나아가게 하는 것을
  "코루틴을 시동한다(priming the coroutine)"고 부른다** (같은 절, p.645).[^ramalho2022]
  `None` 말고 다른 값을 보낼 수 없는데, **코루틴은 `yield` 줄에 중단돼 있을 때에만 보내진
  값을 받을 수 있기** 때문이다.
- 한 번의 활성화가 도는 순서가 명시돼 있다 — **각 활성화 뒤 코루틴은 정확히 `yield`
  키워드에서 중단되어 값이 보내지기를 기다린다. `coro_avg.send(10)`이 그 값을 제공해
  코루틴을 활성화시킨다. `yield` 식이 값 `10`으로 평가되어 `term` 변수에 대입된다.
  루프의 나머지가 `total`·`count`·`average`를 갱신한다. `while` 루프의 다음 반복이
  평균을 내놓고, 코루틴은 다시 `yield`에서 중단된다** (같은 절, p.645).[^ramalho2022]
- 종료는 대개 신경 쓸 일이 아니다 — **우리는 보통 제너레이터를 종료시킬 필요가 없다.
  더 이상 유효한 참조가 없으면 가비지 수집되기 때문이다** (같은 절, p.645).[^ramalho2022]
  명시적으로 끝내려면 `.close()`를 쓰고 그 의미론이 셋이다 (같은 절,
  pp.645–646):[^ramalho2022]
  - **`.close()` 메서드는 중단된 `yield` 식에서 `GeneratorExit`를 일으킨다.** 코루틴
    함수에서 처리하지 않으면 그 예외가 코루틴을 종료시킨다. 그 예외는 코루틴을 감싼
    제너레이터 객체가 잡으므로 우리 눈에는 보이지 않는다.
  - **이미 닫힌 코루틴에 `.close()`를 불러도 아무 효과가 없다.**
  - **닫힌 코루틴에 `.send()`를 시도하면 `StopIteration`이 일어난다.**

## 반환값은 예외에 실려 나온다

- 기제 — 코루틴이 `return`으로 값을 돌려주면 **그 값을 코루틴에서 밀반출해
  `StopIteration` 예외에 감싸 내보내는데**, 저자 자신이 그것을 이렇게 부른다 (17장
  §"Returning a Value from a Coroutine", p.648):[^ramalho2022]

> This idea of "smuggling" the return value out of the coroutine wrapped in a
> `StopIteration` exception is a bizarre hack.

  - 그럼에도 이것은 임시방편이 아니라 규격이다 — **그럼에도 이 기괴한 핵은 PEP 342의
    일부이고, `StopIteration` 예외와 함께 문서화돼 있으며, *The Python Language
    Reference* 6장의 "Yield expressions" 절에도 있다** (같은 절, p.648).[^ramalho2022]
  - 붙잡는 자리는 `except StopIteration as exc:` 안의 `exc.value`다 — **`StopIteration`
    인스턴스는 코루틴을 끝낸 `return` 문의 값에 묶인 `value` 속성을 갖는다** (같은 절,
    p.648).[^ramalho2022]
- 위임 제너레이터는 그 잡기를 대신해 준다 — **위임 제너레이터는 `yield from` 문법으로
  코루틴의 반환값을 곧바로 얻을 수 있다** (같은 절, p.648).[^ramalho2022] `res = yield from
  averager2(True)`가 그것이고, **`yield from` 기제가 코루틴 종료를 표시하는
  `StopIteration` 예외를 처리할 때 반환값을 회수한다** (같은 절, p.649).[^ramalho2022]
- 센티널로 멈추는 관용이 함께 나온다. `.close()`로는 결과를 못 받는데 — **`GeneratorExit`
  예외가 코루틴의 `yield` 줄에서 일어나므로 `return` 문에 결코 닿지 않기** 때문이다
  (같은 절, p.648).[^ramalho2022] 그래서 저자는 전용 센티널 객체를 보내 루프를 깨고
  `return`에 닿게 한다.

## 손으로 몰지 마라

- 저자의 기각이 명시적이다 — **앞의 예들이 보이듯 코루틴을 직접 쓰는 것은 번거롭고
  혼란스럽다. 예외 처리와 코루틴의 `.throw()` 메서드까지 더하면 예제는 더 뒤엉킨다.
  이 책에서 `.throw()`는 다루지 않는데, `.send()`와 마찬가지로 코루틴을 "손으로" 모는
  데에만 쓸모가 있고 나는 그러기를 권하지 않기 때문이다 — 코루틴 기반 프레임워크를 맨
  바닥에서 새로 만드는 경우가 아니라면** (17장 §"Returning a Value from a Coroutine",
  p.650).[^ramalho2022]
- 실무의 요구가 한 줄로 정리된다 — **실무에서 코루틴으로 생산적인 일을 하려면 전문
  프레임워크의 지원이 필요하다. 그것이 파이썬 3.3 시절 asyncio가 고전 코루틴에 제공한
  것이다** (같은 절, p.650).[^ramalho2022]
- 그리고 이 장의 마지막 판정이 21장으로 이어진다 — **파이썬 3.5의 네이티브 코루틴 등장
  이후 파이썬 코어 개발자들은 asyncio에서 고전 코루틴 지원을 점진적으로 걷어 내고 있다.
  그러나 바탕 기제는 매우 비슷하다. `async def` 문법이 코드에서 네이티브 코루틴을 알아보기
  쉽게 만들어 주는 것이 큰 이득이다. 안에서 네이티브 코루틴은 다른 코루틴에 위임할 때
  `yield from` 대신 `await`를 쓴다** (같은 절, p.650).[^ramalho2022]
  - 장 요약이 그 관계를 다시 못 박는다 — **실무에서 쓰기는 어렵지만 고전 코루틴은
    네이티브 코루틴의 토대이고, `yield from` 식은 `await`의 직계 선조다** (17장
    §"Chapter Summary", p.652).[^ramalho2022]

## 타입 매개변수 셋이 갈리는 이유

- 형태 — `Generator[YieldType, SendType, ReturnType]`이고, 세 매개변수의 변성이 같지
  않다 (17장 §"Generic Type Hints for Classic Coroutines", p.651).[^ramalho2022]
- 가르는 기준이 방향이다 (같은 절, p.651):[^ramalho2022]
  - **`YieldType`과 `ReturnType`은 "출력" 타입이다. 둘 다 코루틴 객체에서 나오는 데이터를
    서술한다.** 그래서 공변(covariant)이다 — **`float`를 내놓는 코루틴을 기대하는 코드는
    `int`를 내놓는 코루틴을 쓸 수 있다.**
  - **`SendType`은 "입력" 매개변수다: 코루틴 객체의 `.send(value)` 메서드에 주는 `value`
    인자의 타입이다.** 그래서 반변(contravariant)이다 — **코루틴에 `float`를 보내야 하는
    클라이언트 코드는 `SendType`이 `int`인 코루틴을 쓸 수 없다. `float`가 `int`의 하위
    타입이 아니기 때문이다. 그러나 `SendType`이 `complex`인 코루틴은 쓸 수 있다.**
- 그것이 15장의 변성 엄지 규칙 둘의 실물이다 (같은 절, p.651):[^ramalho2022]
  1. **형식 타입 매개변수가 객체에서 나오는 데이터의 타입을 정의하면 공변일 수 있다.**
  2. **형식 타입 매개변수가 최초 생성 이후 객체로 들어가는 데이터의 타입을 정의하면
     반변일 수 있다.**
- 이름이 잘못 붙었다는 지적이 따로 있다 — **혼란을 더하는 것은, `typing` 모듈 저자들이 그
  타입을 `Generator`라 이름 붙이기로 했다는 사실이다. 실제로 그것이 서술하는 것은 코루틴으로
  쓰이도록 의도된 제너레이터 객체의 API인데, 제너레이터는 단순한 이터레이터로 쓰이는 일이
  더 많다** (17장 §"Classic Coroutines", p.642).[^ramalho2022] 그리고
  `typing.Coroutine`·`collections.abc.Coroutine`은 **네이티브 코루틴만을 애노테이트하도록
  의도된 것이라, 고전 코루틴에 타입 힌트를 쓰려면 `Generator[...]`의 혼란을 감수해야
  한다** (같은 절, pp.642–643).[^ramalho2022]
  - 버전 조건: 파이썬 3.9 이상. `collections.abc.Coroutine`이 제네릭이 된 것이 3.9이고,
    `typing.Coroutine`은 폐기 경로에 있다.

## 이어지는 페이지

- [이터레이터 프로토콜과 제너레이터](iterator-protocol-and-generators.md) — 같은 장의
  앞부분. 여기서 위임하는 그 제너레이터가 무엇이고 어떻게 도는가
- [동시 실행기와 asyncio](concurrent-executors-and-asyncio.md) — `yield from`이 `await`가
  되고 고전 코루틴이 네이티브 코루틴이 되는 자리
- [컨텍스트 매니저 프로토콜](context-manager-protocol.md) — `yield` 하나가 함수 몸통을
  진입과 정리로 가르는 또 하나의 자리
- [클로저와 데코레이터](closures-and-decorators.md) — 코루틴이 대신하는 그 상태 보관
  수단(클로저와 `nonlocal`)의 정본
- [심화 타입 힌트와 그 한계](advanced-type-hints-in-python.md) — 여기 쓰인 공변·반변과
  변성 엄지 규칙의 정본
- [파이썬의 제어 흐름 기제](../synthesis/python-control-flow-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 17장 "Iterators, Generators, and Classic Coroutines"
    §"Subgenerators with yield from"(pp.632–633) · §"Reinventing chain"(pp.633–634) ·
    §"Traversing a Tree"(pp.634–639) · §"Classic Coroutines"(pp.641–643) · §"Example:
    Coroutine to Compute a Running Average"(pp.643–645) · §"Returning a Value from a
    Coroutine"(pp.646–650) · §"Generic Type Hints for Classic Coroutines"(pp.650–651) ·
    §"Chapter Summary"(p.652). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을
    뺀 값이고, 그 오프셋 실측과 판본 판정은 `it/archive/ramalho2022/_progress.yaml`
    머리말이 정본이다. 코드 펜스는 예제 17-33 원문이고, 원문 코드 목록에 삽입된 조판용
    번호 표지만 제거했다. Beazley 슬라이드 인용은 저자가 본문에 그대로 옮긴 것을 다시
    옮긴 것이다.

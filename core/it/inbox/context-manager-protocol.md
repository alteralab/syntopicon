---
type: concept
title: 컨텍스트 매니저 프로토콜
description: with 문이 무엇을 보장하는가 — try/finally를 단순화하려는 설계 의도와 __enter__·__exit__ 두 메서드의 계약, 컨텍스트 매니저 객체와 as가 묶는 값이 다른 것이라는 미묘한 지점, __exit__이 참을 돌려주면 예외가 삼켜진다는 규칙, 제너레이터 하나로 매니저를 만드는 데코레이터와 그것이 요구하는 try/finally, 그리고 이 문법이 자원 관리를 넘어 서브루틴의 보완이라는 주장
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 컨텍스트 매니저 프로토콜

- [무엇을 대체하려고 만들어졌는가](#무엇을-대체하려고-만들어졌는가)
- [두 메서드의 계약](#두-메서드의-계약)
- [매니저 객체와 as가 묶는 값은 다른 것이다](#매니저-객체와-as가-묶는-값은-다른-것이다)
- [__exit__의 세 인자와 예외 삼키기](#__exit__의-세-인자와-예외-삼키기)
- [contextlib이 이미 만들어 둔 것들](#contextlib이-이미-만들어-둔-것들)
- [제너레이터 하나로 매니저 만들기](#제너레이터-하나로-매니저-만들기)
- [자원 관리가 아니라 빵을 인수분해하는 것](#자원-관리가-아니라-빵을-인수분해하는-것)
- [이 KB의 자원 조문과 닿는 자리](#이-kb의-자원-조문과-닿는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 코드 블록의 앞뒤에서 반드시 실행돼야 하는 짝을 어디에 두어야, 블록이
어떻게 끝나든 그 짝이 지켜지는가.**

## 무엇을 대체하려고 만들어졌는가

- 규정 — **컨텍스트 매니저 객체는 `with` 문을 제어하기 위해 존재한다. 이터레이터가 `for`
  문을 제어하기 위해 존재하는 것과 똑같다** (18장 §"Context Managers and with Blocks",
  p.658).[^ramalho2022]
- 설계 의도가 명시돼 있다 — **`with` 문은 `try/finally`의 흔한 쓰임 몇 가지를 단순화하려고
  설계됐다. `try/finally`는 코드 블록이 `return`·예외·`sys.exit()` 호출로 끝나더라도 그
  블록 뒤에 어떤 연산이 수행되도록 보장한다. `finally` 절의 코드는 보통 임계 자원을
  해제하거나 일시적으로 바뀐 이전 상태를 복원한다** (같은 절, p.658).[^ramalho2022]
- 표준 라이브러리가 이미 쓰는 자리 넷이 열거된다 (같은 절, p.658):[^ramalho2022]
  `sqlite3`의 트랜잭션 관리, `threading`의 락·조건·세마포어 처리, `decimal.localcontext`의
  산술 환경 설정, 테스트용 `unittest.mock.patch`의 객체 패칭.
- 그리고 그 목록이 열려 있다 — **파이썬 커뮤니티는 컨텍스트 매니저의 새롭고 창의적인
  쓸모를 찾아내는 중이다** (같은 절, p.658).[^ramalho2022]

## 두 메서드의 계약

- 인터페이스 — **컨텍스트 매니저 인터페이스는 `__enter__`와 `__exit__` 메서드로 이루어진다.
  `with`의 맨 위에서 파이썬이 컨텍스트 매니저 객체의 `__enter__` 메서드를 부른다. `with`
  블록이 완료되거나 어떤 이유로든 종료되면 파이썬이 컨텍스트 매니저 객체의 `__exit__`를
  부른다** (같은 절, p.658).[^ramalho2022]
- `__enter__`는 인자를 받지 않는다 — **인터프리터는 암묵적 `self` 말고 다른 인자 없이
  `__enter__` 메서드를 부른다** (같은 절, p.661).[^ramalho2022]
- `with`는 범위를 만들지 않는다 — **`fp` 변수는 여전히 쓸 수 있다. `with` 블록은 함수처럼
  새 범위를 정의하지 않는다** (같은 절, p.659).[^ramalho2022] 블록을 벗어난 뒤에도 이름이
  살아 있고, 다만 그 객체가 정리된 상태일 뿐이다.
- `as` 절은 선택이다 — **`with` 문의 `as` 절은 선택적이다. `open`의 경우에는 파일 참조를
  얻어 메서드를 부르려고 언제나 필요하지만, 어떤 컨텍스트 매니저들은 사용자에게 돌려줄
  쓸모 있는 객체가 없어서 `None`을 돌려준다** (같은 절, p.660).[^ramalho2022]

## 매니저 객체와 as가 묶는 값은 다른 것이다

- 이것이 이 절의 요점이다 (같은 절, p.659):[^ramalho2022]

> the context manager object is the result of evaluating the expression after `with`, but
> the value bound to the target variable (in the `as` clause) is the result returned by
> the `__enter__` method of the context manager object.

  - 파일이 헷갈리게 만든다 — **`open()` 함수가 `TextIOWrapper` 인스턴스를 돌려주고 그
    `__enter__` 메서드가 `self`를 돌려주는 것은 우연히 그런 것이다. 다른 클래스에서는
    `__enter__` 메서드가 컨텍스트 매니저 인스턴스가 아니라 다른 객체를 돌려줄 수도
    있다** (같은 절, p.659).[^ramalho2022]
  - 그리고 나가는 쪽은 언제나 매니저다 — **제어 흐름이 어떤 방식으로든 `with` 블록을
    벗어날 때, `__exit__` 메서드는 컨텍스트 매니저 객체에 대해 호출되지, `__enter__`가
    돌려준 무엇에 대해 호출되지 않는다** (같은 절, p.659).[^ramalho2022]
- 저자는 그 구분만을 위해 일부러 "경박한" 예제를 하나 만든다 — `__enter__`가 문자열
  `'JABBERWOCKY'`를 돌려주는 `LookingGlass` 클래스다. `with LookingGlass() as what:`에서
  `what`은 문자열이고 컨텍스트 매니저는 `LookingGlass` 인스턴스다 (같은 절,
  pp.660–662).[^ramalho2022]

## __exit__의 세 인자와 예외 삼키기

- 인자 셋의 정본 (같은 절, pp.661–662):[^ramalho2022]
  - `exc_type` — 예외 클래스(예: `ZeroDivisionError`).
  - `exc_value` — 예외 인스턴스. **때때로 예외 생성자에 넘겨진 매개변수(오류 메시지 같은
    것)를 `exc_value.args`에서 찾을 수 있다.**
  - `traceback` — 트레이스백 객체.
- 아무 일 없이 끝나면 셋 다 `None`이다 — **모든 것이 잘됐으면 파이썬이 `__exit__`를
  `None, None, None`으로 부른다. 예외가 일어났으면 세 인자가 예외 데이터를 받는다**
  (같은 절, p.661).[^ramalho2022]
- 그 셋의 정체가 각주로 밝혀져 있다 — **`self`가 받는 세 인자는 `try/finally` 문의
  `finally` 블록에서 `sys.exc_info()`를 부르면 얻는 것과 정확히 같다. `with` 문이
  `try/finally`의 대부분의 쓰임을 대체하려는 것임을 생각하면 말이 된다** (같은 절 각주 2,
  p.662).[^ramalho2022]
- 반환값이 제어 흐름을 결정한다 — **`__exit__`가 참을 돌려주면 인터프리터에 예외가
  처리됐다고 알리는 것이다. `__exit__`가 `None`이나 거짓 값을 돌려주면 `with` 블록에서
  일어난 예외는 전파된다** (같은 절, p.661).[^ramalho2022]

## contextlib이 이미 만들어 둔 것들

- 조문 — **직접 컨텍스트 매니저 클래스를 굴리기 전에 `contextlib`을 먼저 보라. 당신이
  지으려는 것이 이미 있거나, 일을 더 쉽게 해 줄 클래스나 호출 가능한 것이 있을지도
  모른다** (18장 §"The contextlib Utilities", p.663).[^ramalho2022]
- 목록과 각각의 쓸모 (같은 절, pp.663–664):[^ramalho2022]
  - `closing` — **`close()` 메서드는 제공하지만 `__enter__`/`__exit__` 인터페이스는
    구현하지 않는 객체로부터 컨텍스트 매니저를 짓는 함수.**
  - `suppress` — **인자로 준 예외들을 일시적으로 무시하는 컨텍스트 매니저.**
  - `nullcontext` — **아무 일도 하지 않는 컨텍스트 매니저.** 적절한 컨텍스트 매니저를
    가질 수도 안 가질 수도 있는 객체 둘레의 조건 로직을 단순화하는 대역이다.
  - `@contextmanager` — **인터페이스를 구현한 클래스를 만드는 대신, 단순한 제너레이터
    함수로부터 컨텍스트 매니저를 지을 수 있게 하는 데코레이터.**
  - `AbstractContextManager` — **컨텍스트 매니저 인터페이스를 형식화하는 ABC.**
  - `ContextDecorator` — **함수 데코레이터로도 쓸 수 있는 클래스 기반 컨텍스트 매니저를
    정의하기 위한 기반 클래스.** 함수 전체를 관리되는 컨텍스트 안에서 돌린다.
  - `ExitStack` — **가변 개수의 컨텍스트 매니저에 진입할 수 있게 하는 컨텍스트 매니저.
    `with` 블록이 끝나면 `ExitStack`이 쌓인 컨텍스트 매니저들의 `__exit__` 메서드를
    LIFO 순서(마지막에 진입한 것이 먼저 나옴)로 부른다.** 미리 몇 개인지 모를 때 쓴다 —
    임의의 파일 목록을 한꺼번에 여는 경우가 예로 들린다.
- 버전 조건: `redirect_stderr`는 파이썬 3.5, `AbstractContextManager`는 3.6,
  `nullcontext`는 3.7에 더해졌다. 비동기 짝(`AbstractAsyncContextManager`·
  `@asynccontextmanager`·`AsyncExitStack`)도 3.7부터 있다 (같은 절, pp.663–664).
- 괄호 문법도 판을 탄다 (18장 §"Parenthesized Context Managers in Python 3.10",
  p.663):[^ramalho2022]
  - 버전 조건: 파이썬 3.10 이상에서 여러 컨텍스트 매니저를 괄호로 묶어 쓸 수 있다. **3.10
    이전에는 중첩 `with` 블록으로 써야 했다.** 저자는 그 문법이 가능해진 이유를 **3.10이
    더 강력한 파서를 채택해 옛 LL(1) 파서로는 불가능하던 문법이 열렸기** 때문이라고 적는다.

## 제너레이터 하나로 매니저 만들기

- 이 데코레이터가 세 기능을 한자리에 모은다 — **`@contextmanager` 데코레이터는 우아하고
  실용적인 도구이며 파이썬의 뚜렷한 세 기능을 한데 모은다: 함수 데코레이터, 제너레이터,
  그리고 `with` 문** (18장 §"Using @contextmanager", p.664).[^ramalho2022]
- 그것이 덜어 주는 것 — **`@contextmanager`를 쓰면 컨텍스트 매니저를 만드는 보일러플레이트가
  줄어든다: `__enter__`/`__exit__` 메서드를 가진 클래스를 통째로 쓰는 대신, `__enter__`
  메서드가 돌려주기를 바라는 무엇을 만들어 내는 `yield` 하나짜리 제너레이터를 구현하면
  된다** (같은 절, p.664).[^ramalho2022]
- `yield`가 몸통을 가른다 — **`@contextmanager`로 장식된 제너레이터에서 `yield`는 함수의
  몸통을 두 부분으로 가른다: `yield` 앞의 모든 것은 인터프리터가 `__enter__`를 부를 때
  `with` 블록 시작에서 실행되고, `yield` 뒤의 코드는 블록 끝에서 `__exit__`가 불릴 때
  실행된다** (같은 절, p.664).[^ramalho2022]
- 데코레이터가 감싸는 클래스의 절차가 명시돼 있다 (같은 절, p.666):[^ramalho2022]
  - `__enter__`는 ① 제너레이터 함수를 불러 제너레이터 객체를 얻고, ② `next(gen)`을 불러
    `yield` 키워드까지 몰고, ③ `next(gen)`이 내놓은 값을 돌려준다.
  - `__exit__`는 ① `exc_type`으로 예외가 넘어왔는지 검사하고, 넘어왔으면
    `gen.throw(exception)`을 불러 제너레이터 함수 몸통의 `yield` 줄에서 그 예외가
    일어나게 만들고, ② 아니면 `next(gen)`을 불러 `yield` 뒤부터 몸통을 재개시킨다.
- **여기서 예외 처리를 빼먹으면 시스템이 잘못된 상태로 남는다** — 저자가 자기 첫 판의
  결함을 짚는다: **`with` 블록 몸통에서 예외가 일어나면 파이썬 인터프리터가 그것을 잡아
  `looking_glass` 안의 `yield` 식에서 다시 일으킨다. 그런데 거기에 오류 처리가 없으므로
  `looking_glass` 제너레이터는 원래의 `sys.stdout.write` 메서드를 복원하지 못한 채
  종료되고, 시스템을 유효하지 않은 상태로 남긴다** (같은 절, p.666).[^ramalho2022]
- 그래서 대가가 하나 붙는다 (같은 절, p.667):[^ramalho2022]

> Having a `try/finally` (or a `with` block) around the `yield` is an unavoidable price
> of using `@contextmanager`, because you never know what the users of your context
> manager are going to do inside the `with` block.

  그 문장은 기술 검토자 Leonardo Rochael의 말을 저자가 그대로 인용한 것이다.
- 기본 동작이 뒤집힌다는 단서가 중요하다 — **`__exit__` 메서드는 참인 값을 돌려줌으로써
  예외를 처리했다고 인터프리터에 알린다는 것을 상기하라. 그 경우 인터프리터는 예외를
  억누른다. 반면 `__exit__`가 명시적으로 값을 돌려주지 않으면 인터프리터는 평소의 `None`을
  받고 예외를 전파한다. `@contextmanager`에서는 그 기본 동작이 뒤집힌다: 데코레이터가
  제공하는 `__exit__` 메서드는 제너레이터로 보내진 어떤 예외든 처리됐으며 억눌러야 한다고
  가정한다** (같은 절, p.667).[^ramalho2022]
- 잘 안 알려진 성질 하나 — **`@contextmanager`로 장식된 제너레이터는 자기 자신이
  데코레이터로도 쓰일 수 있다. `@contextmanager`가 `contextlib.ContextDecorator` 클래스로
  구현돼 있기 때문이다** (같은 절, p.668).[^ramalho2022] 저자와 다른 기술 검토자들도 Caleb
  Hattingh가 알려 주기 전까지 몰랐다고 적혀 있다.
- 대표 코드가 예외 처리까지 갖춘 판이다 (예제 18-7, pp.666–667):[^ramalho2022]

  ```python
  import contextlib
  import sys


  @contextlib.contextmanager
  def looking_glass():
      original_write = sys.stdout.write

      def reverse_write(text):
          original_write(text[::-1])

      sys.stdout.write = reverse_write
      msg = ''
      try:
          yield 'JABBERWOCKY'
      except ZeroDivisionError:
          msg = 'Please DO NOT divide by zero!'
      finally:
          sys.stdout.write = original_write
          if msg:
              print(msg)
  ```

  - 찾을 것은 `@contextlib.contextmanager`와 `yield`를 감싼 `try/finally`다. 이 열여덟
    줄이 `__enter__`/`__exit__`를 손으로 짠 클래스판과 겉보기 동작이 같다.

## 자원 관리가 아니라 빵을 인수분해하는 것

- 장 요약이 이 문법의 범위를 넓힌다 — **Raymond Hettinger가 PyCon US 2013 기조연설에서
  짚은 요점은 `with`가 자원 관리만을 위한 것이 아니라는 것이다. 그것은 공통의 준비와 정리
  코드를, 또는 다른 절차의 앞뒤에서 수행돼야 하는 어떤 연산 쌍이든 인수분해해 내는
  도구다** (18장 §"Chapter Summary", p.689).[^ramalho2022]
- 그 통찰의 비유가 곁글에 있다 (18장 §"Soapbox — Factoring Out the Bread",
  p.691):[^ramalho2022]

> If you have sequences of operations like A;B;C and P;B;Q, you can factor out B in a
> subroutine. It's like factoring out the filling in a sandwich: using tuna with
> different breads. But what if you want to factor out the bread, to make sandwiches with
> wheat bread, using a different filling each time? That's what the `with` statement
> offers. It's the complement of the subroutine.

  - Hettinger 자신의 전망도 그대로 옮겨져 있다 — **`with` 문은 대단한 것이다. (…) 그것의
    가장 좋은 쓰임새는 아직 발견되지 않았다** (같은 절, p.691).[^ramalho2022]
  - 저자는 그 평가에 단서를 단다 — **Hettinger는 자기가 `with` 문을 과대 선전하고 있음을
    인정한다. 그럼에도 그것은 매우 쓸모 있는 기능이다** (같은 절, p.691).[^ramalho2022]
- 곁들여진 실물 사례 하나 — Martijn Pieters의 제자리 파일 재작성 컨텍스트 매니저는
  같은 파일에 대한 읽기·쓰기 핸들 **둘을 한꺼번에** 내준다. 저자가 그 소스를 읽는 법을
  일러 준다 — **`yield` 키워드를 찾아라: 그 앞의 모든 것이 컨텍스트를 준비하는 일이고,
  `yield` 뒤의 `__exit__` 처리가 파일 핸들을 닫고 무언가 잘못됐으면 백업에서 파일을
  복원한다** (18장 §"Using @contextmanager", p.669).[^ramalho2022]
- `contextlib.ExitStack`이 다른 언어의 기능과 견주어진다 — Nikolaus Rath의 글이 인용되는데,
  **`ExitStack`이 Go의 `defer` 문과 비슷하되 더 유연하다**는 주장이고, 저자는 **`defer`가
  그 언어의 가장 좋은 발상 중 하나라고 생각한다**고 덧붙인다 (18장 §"Further Reading",
  p.690).[^ramalho2022]

## 이 KB의 자원 조문과 닿는 자리

- 이 프로토콜은 이 KB가 이미 갖고 있는 자원 조문의 파이썬 쪽 기제다. 그쪽 정본은
  [리소스 균형 맞추기](balancing-resources.md)이고, 그 페이지의 세 항목이 여기에 그대로
  대응한다.
  - "시작한 것을 끝내라"는 조문이 요구하는 것 — 할당한 쪽이 해제 책임을 진다 — 을 이
    프로토콜은 **한 객체 안에 `__enter__`와 `__exit__`를 짝지어** 실현한다.
  - "범위를 줄이는 것은 언제나 값을 한다"는 조문의 파이썬 실물이 `with` 블록이다. 다만
    한 가지가 다르다 — **`with` 블록은 새 범위를 만들지 않으므로**(위 절 참조) 이름은
    블록 밖에서도 살아 있고, 보장되는 것은 이름의 소멸이 아니라 **정리의 실행**이다.
  - 그쪽이 든 "예외 안티패턴"(할당을 `try` 안에 두고 `finally`에서 해제하려다 할당 실패
    시 없는 것을 해제하려 드는 것)은 이 문법에서 구조적으로 일어나기 어렵다. 매니저
    객체를 얻는 식이 `with` 줄에서 평가되고, `__exit__`는 `__enter__`가 성공한 뒤에만
    불리기 때문이다. #hypothesis 이 마지막 대응은 소스가 명시한 것이 아니라 두 소스의
    조문을 나란히 놓고 이 KB가 읽어 낸 것이다.
- 애플리케이션 층에서 이 프로토콜을 실제로 쓰는 자리는
  [작업 단위 패턴](unit-of-work-pattern.md)에 있다 — 그쪽이 `__enter__`/`__exit__`를
  원자성의 경계를 눈에 보이게 만드는 수단으로 고른다.

## 이어지는 페이지

- [패턴 매칭과 else 블록](pattern-matching-and-else-blocks.md) — 같은 장의 뒷부분.
  블록을 무엇으로 고르는가, 그리고 블록이 끝까지 갔을 때 무엇을 하는가
- [이터레이터 프로토콜과 제너레이터](iterator-protocol-and-generators.md) — 여기 쓰인
  `yield`가 순회 문맥에서 무엇을 하는가의 정본
- [클로저와 데코레이터](closures-and-decorators.md) — `@contextmanager`가 얹히는 그 기제
- [동시 실행기와 asyncio](concurrent-executors-and-asyncio.md) — 이 프로토콜의 비동기
  짝(`__aenter__`·`__aexit__`)과 `@asynccontextmanager`
- [리소스 균형 맞추기](balancing-resources.md) — 이 언어 기제가 실현하는 조문의 원리 쪽
- [작업 단위 패턴](unit-of-work-pattern.md) — 이 프로토콜을 원자성의 경계로 쓰는 자리
- [일시적 결합 깨기](../concepts/breaking-temporal-coupling.md) — "무엇이 무엇 뒤에 와야 하는가"를
  코드에 강제하는 다른 방식들
- [파이썬의 제어 흐름 기제](../synthesis/python-control-flow-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 18장 "with, match, and else Blocks" 도입(p.657) ·
    §"Context Managers and with Blocks"(pp.658–663) · §"Parenthesized Context Managers in
    Python 3.10"(p.663) · §"The contextlib Utilities"(pp.663–664) · §"Using
    @contextmanager"(pp.664–669) · §"Chapter Summary"(p.689) · §"Further Reading"(p.690) ·
    §"Soapbox — Factoring Out the Bread"(p.691). **locator의 쪽은 인쇄판 쪽이다** —
    스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과 판본 판정은
    `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 코드 펜스는 예제 18-7
    원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만 제거했다. Hettinger 기조연설
    인용은 저자가 본문과 곁글에 옮긴 것을 다시 옮긴 것이다.

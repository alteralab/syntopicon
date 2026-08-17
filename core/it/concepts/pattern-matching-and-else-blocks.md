---
type: concept
title: 패턴 매칭과 else 블록
description: 언어의 문법을 시퀀스 패턴으로 표현할 수 있다는 관찰과 그것이 match/case를 언어 처리기에 맞는 도구로 만드는 이유, OR 패턴의 규칙과 case 문맥에서 세로줄이 연산자가 아니라는 단서, 예약어가 왜 필요한가에 대한 인터프리터 쪽 대답, 그리고 for·while·try에 붙는 else의 의미론과 그 낱말이 잘못 골라졌다는 저자의 판정
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 패턴 매칭과 else 블록

- [문법을 패턴으로 적을 수 있다](#문법을-패턴으로-적을-수-있다)
- [OR 패턴과 가드](#or-패턴과-가드)
- [예약어가 왜 필요한가](#예약어가-왜-필요한가)
- [nonlocal과 set!은 같은 문제를 푼다](#nonlocal과-set은-같은-문제를-푼다)
- [저자가 받아들인 반론](#저자가-받아들인-반론)
- [else가 if 밖에서 뜻하는 것](#else가-if-밖에서-뜻하는-것)
- [EAFP와 LBYL](#eafp와-lbyl)
- [파이썬에 적정 꼬리 호출이 없는 이유](#파이썬에-적정-꼬리-호출이-없는-이유)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **분기를 값이 아니라 구조로 고를 수 있으면 무엇이 달라지고, 블록이 끝까지
갔다는 사실 자체에 코드를 붙이려면 어디에 쓰는가.**

## 문법을 패턴으로 적을 수 있다

- 이 장이 패턴 매칭에 대해 더하는 것이 한 문장으로 예고된다 — **여기서는 언어의 문법이
  시퀀스 패턴으로 표현될 수 있다는 것을 볼 것이다. 그 관찰이 `match`/`case`가 이해하기
  쉽고 확장하기 쉬운 언어 처리기를 만드는 효과적인 도구인 이유를 설명한다** (18장 도입,
  p.657).[^ramalho2022] 그리고 그 발상의 적용 범위가 언어 자체에 한정되지 않는다 —
  **같은 발상을 템플릿 언어나, 더 큰 시스템 안에서 업무 규칙을 부호화하는 DSL을 개발하는
  데 적용할 수 있다** (같은 자리, p.658).[^ramalho2022]
- 실물은 Peter Norvig의 Scheme 인터프리터 *lis.py*를 파이썬 3.10으로 옮긴 것이다. 저자가
  그 사례 연구를 고른 사유가 셋이다 (18장 §"Pattern Matching in lis.py: A Case Study",
  p.669):[^ramalho2022]
  1. **Norvig의 *lis.py*는 관용적 파이썬 코드의 아름다운 예다.**
  2. **Scheme의 단순함은 언어 설계의 명강의다.**
  3. **인터프리터가 어떻게 동작하는지 배우는 것이 파이썬과 프로그래밍 언어 전반에 대한
     더 깊은 이해를 주었다 — 해석되든 컴파일되든.**
- 평가기 전체가 `match` 문 하나다 — **`evaluate`의 몸통은 식 `exp`를 주어로 하는 단일
  `match` 문이다. `case` 패턴들이 Scheme의 문법과 의미론을 놀라운 명료함으로 표현한다**
  (18장 §"The Evaluator", p.676).[^ramalho2022] 그 안의 `case` 절 하나하나가 언어의 특수
  형식 하나에 대응한다 — `case ['quote', x]`, `case ['if', test, consequence, alternative]`,
  `case ['lambda', [*parms], *body] if body:`, `case ['define', Symbol(name), value_exp]`,
  `case ['set!', Symbol(name), value_exp]`, 그리고 함수 호출을 받는
  `case [func_exp, *args] if func_exp not in KEYWORDS:` (같은 절,
  pp.677–684).[^ramalho2022]
- 파싱 결과가 무엇인지도 명시된다 — **파이썬 인터프리터의 용어를 쓰면, `parse`의 출력은
  AST(추상 구문 트리)다: Scheme 프로그램을 중첩 리스트로 나타낸 편리한 표현이며, 가장 바깥
  리스트가 줄기, 안쪽 리스트가 가지, 원자가 잎을 이루는 나무 모양 구조다** (18장 §"The
  Parser", p.673).[^ramalho2022] 패턴이 그 중첩 리스트의 모양을 그대로 적는다는 것이
  이 절의 논거다.

## OR 패턴과 가드

- 정의 — **`|`로 구분된 일련의 패턴이 OR 패턴(OR-pattern)이다: 하위 패턴 중 어느 하나라도
  성공하면 성공한다** (18장 §"Using OR-patterns", p.686).[^ramalho2022] `case int(x) |
  float(x): return x`가 그 실물이다.
- 제약 하나가 붙고 그 사유가 명시된다 — **OR 패턴의 모든 하위 패턴은 같은 변수를 써야
  한다. 이 제약은 어느 하위 패턴이 일치했든 상관없이 가드 식과 `case` 몸통에서 변수를
  쓸 수 있게 보장하기 위해 필요하다** (같은 절, p.686).[^ramalho2022]
- **`case` 문맥의 `|`는 연산자가 아니다** — **`case` 절의 문맥에서 `|` 연산자는 특별한
  뜻을 갖는다. 다른 문맥에서 `a | b` 같은 식을 처리하는 `__or__` 특수 메서드를 발동시키지
  않는다. 다른 문맥에서 그것은 집합 합집합이나 정수 비트 OR 같은 연산을 하도록
  오버로드된다** (같은 절, p.686).[^ramalho2022]
- 최상위에만 오는 것도 아니다 — **OR 패턴은 패턴의 최상위에만 나타나도록 제한되지 않는다.
  하위 패턴에서도 `|`를 쓸 수 있다** (같은 절, p.686).[^ramalho2022] 저자의 예가
  `case ['lambda' | 'λ', [*parms], *body] if body:`로 그리스 문자 λ까지 받아들이는 것이다.
- 가드가 하는 일이 두 자리에서 드러난다.
  - `case ['lambda', [*parms], *body] if body:`의 가드는 **`body`가 비어 있지 않음을
    보장한다** (18장 §"The Evaluator", p.680).[^ramalho2022]
  - 함수 호출 절의 가드는 필수다 — **`[func_exp, *args]` 패턴은 항목이 하나 이상인 어떤
    시퀀스 주어와도 일치하기 때문에 이 `case`의 가드가 필요하다. 그런데 `func_exp`가
    키워드이고 주어가 앞의 어느 `case`와도 일치하지 않았다면, 그것은 정말로 문법
    오류다** (같은 절, p.684).[^ramalho2022] 가드가 없으면 `(lambda is not like this)`
    같은 잘못된 식이 함수 호출로 취급돼 엉뚱한 `KeyError`를 낸다.
- `match`에는 `else`가 없고 그것은 결정이었다 — **`match` 문이 논의될 때 어떤 사람들은
  (나를 포함해) 그것도 `else` 절을 가져야 한다고 생각했다. 결국 필요 없다고 결정됐는데
  `case _:`가 같은 일을 하기 때문이다** (18장 §"Do This, Then That: else Blocks Beyond if",
  p.688).[^ramalho2022] 저자는 각주에 다른 사유를 추측으로 덧붙인다 — **`else`가 `match`
  안에서 어느 수준으로 들여쓰여야 하는지(`match`와 같은 수준인가 `case`와 같은
  수준인가)에 합의가 없던 것도 이유의 하나라고 생각한다** (같은 절 각주 13,
  p.688).[^ramalho2022]
  - 버전 조건: 파이썬 3.10 이상. `match`/`case`와 이 절의 문법 전부가 그 판에 도입됐다.
    `lis.py`의 이 판본은 `TypeAlias`와 `|` 타입 합집합 연산자도 써서 3.10을 요구한다.

## 예약어가 왜 필요한가

- 이 사례 연구가 언어 일반에 대해 내놓는 결론이 이 절이다. 출발점은 `quote`다 —
  **단순하지만 `quote`는 Scheme에서 함수로 구현될 수 없다. 그것의 특별한 힘은 식
  `(quote (f 10))`에서 인터프리터가 `(f 10)`을 평가하지 못하게 막는 것이다. 반면 `(abs
  (f 10))` 같은 함수 호출에서는 인터프리터가 `abs`를 부르기 전에 `(f 10)`을 평가한다**
  (18장 §"Why Languages Have Reserved Keywords", p.679).[^ramalho2022]
- 일반화가 셋으로 정리된다 — **일반적으로 예약어는 다음을 위해 필요하다** (같은 절,
  p.679):[^ramalho2022]
  - **특수한 평가 규칙을 도입하기 위해** — `quote`와 `lambda`처럼 하위 식을 아예 평가하지
    않는 것들.
  - **제어 흐름을 바꾸기 위해** — `if`와 함수 호출처럼 역시 특별한 평가 규칙을 갖는 것들.
  - **환경을 관리하기 위해** — `define`과 `set`.
- 그리고 파이썬으로 되돌아온다 — **이것이 파이썬이, 그리고 프로그래밍 언어 일반이 예약어를
  필요로 하는 이유이기도 하다. 파이썬의 `def`·`if`·`yield`·`import`·`del`과 그들이 하는
  일을 생각해 보라** (같은 절, p.679).[^ramalho2022]

## nonlocal과 set!은 같은 문제를 푼다

- 대응이 명시된다 — **`set!` 형식의 사용은 파이썬의 `nonlocal` 키워드 사용과 관련이 있다.
  `nonlocal x`를 선언하면 `x = 10`이 지역 범위 밖에서 이전에 정의된 `x` 변수를 갱신할 수
  있다. `nonlocal x` 선언이 없으면 `x = 10`은 파이썬에서 언제나 지역 변수를 만든다**
  (18장 §"Python's nonlocal and Scheme's set! Address the Same Issue",
  p.683).[^ramalho2022]
- 대칭이 완성된다 — **비슷하게 `(set! x 10)`은 함수의 지역 환경 바깥에 있을 수 있는,
  이전에 정의된 `x`를 갱신한다. 반면 `(define x 10)`의 변수 `x`는 언제나 지역 변수로,
  지역 환경에서 만들어지거나 갱신된다** (같은 절, p.683).[^ramalho2022]
- 둘이 같은 이유로 존재한다 — **`nonlocal`과 `(set! …)` 둘 다 클로저 안의 변수에 담긴
  프로그램 상태를 갱신하는 데 필요하다** (같은 절, p.683).[^ramalho2022] 저자가 9장의
  이동 평균 예제를 Scheme으로 다시 써서 그것을 보인다.
- 클로저의 구현도 여기서 드러난다 — **`Procedure` 클래스는 `Closure`라 불려도 좋았을
  것이다. 그것이 나타내는 것이 그것이기 때문이다: 함수 정의와 환경의 조합. 함수 정의는
  매개변수 이름과 함수 몸통을 이루는 식들을 담는다. 환경은 함수가 불릴 때 자유
  변수(free variables)의 값을 제공하는 데 쓰인다: 함수 몸통에 나타나지만 매개변수도
  지역 변수도 전역 변수도 아닌 변수들** (18장 §"Procedure: A Class Implementing a
  Closure", p.685).[^ramalho2022]
- 그리고 언어 설계의 관찰 하나 — **대입은 많은 프로그래밍 자습서에서 가장 먼저 가르치는
  기능 중 하나이지만, `set!`은 가장 잘 알려진 Scheme 책 *SICP* 2판의 220쪽에야 처음
  나온다. 함수형 스타일로 코딩하면 명령형·객체 지향 프로그래밍에 전형적인 상태 변경 없이도
  아주 멀리 갈 수 있다** (18장 §"(set! …)" 각주 11, p.682).[^ramalho2022]

## 저자가 받아들인 반론

- 저자가 자기 코드를 Norvig에게 보였고 다른 설계를 제안받았다 — **그는 패턴 매칭을 쓴 예를
  마음에 들어 했지만 다른 해법을 제안했다: 내가 쓴 가드들 대신, 키워드마다 정확히 하나의
  `case`를 두고 각 `case` 안에서 검사를 해서 더 구체적인 `SyntaxError` 메시지를 주는
  것이다 — 예컨대 `body`가 비어 있을 때. 이렇게 하면 `case [func_exp, *args] if
  func_exp not in KEYWORDS:`의 가드도 불필요해진다. 모든 키워드가 함수 호출 `case` 이전에
  처리될 것이기 때문이다** (18장 §"Soapbox — Norvig's Take on evaluate() with Pattern
  Matching", p.693).[^ramalho2022]
- 저자의 응답이 두 갈래다 — ***mylis*에 기능을 더할 때는 아마 Norvig의 조언을 따를
  것이다. 그러나 내가 예제 18-17에서 `evaluate`를 구조화한 방식은 이 책에 몇 가지 교육적
  이점이 있다: 그 예가 `if`/`elif`/… 구현과 평행하고, `case` 절들이 패턴 매칭의 더 많은
  기능을 보이며, 코드가 더 간결하다** (같은 절, p.693).[^ramalho2022]

## else가 if 밖에서 뜻하는 것

- 상태 — **이것은 비밀이 아니지만 과소평가된 언어 기능이다: `else` 절은 `if` 문뿐 아니라
  `for`·`while`·`try` 문에도 쓸 수 있다** (18장 §"Do This, Then That: else Blocks Beyond
  if", p.687).[^ramalho2022]
- 규칙 셋의 정본 (같은 절, p.687):[^ramalho2022]
  - `for` — **`else` 블록은 `for` 루프가 끝까지 돌았을 때에만, 그때 실행된다**(즉 `for`가
    `break`로 중단되지 않았을 때).
  - `while` — **`else` 블록은 `while` 루프가 조건이 거짓이 되어 빠져나갔을 때에만, 그때
    실행된다**(즉 `while`이 `break`로 중단되지 않았을 때).
  - `try` — **`else` 블록은 `try` 블록에서 예외가 일어나지 않았을 때에만 실행된다.**
    공식 문서가 덧붙인다: **"`else` 절의 예외는 앞선 `except` 절들에 의해 처리되지
    않는다."**
  - 그리고 공통 규칙 — **모든 경우에, 예외나 `return`·`break`·`continue` 문이 제어를
    복합문의 주 블록 바깥으로 점프시키면 `else` 절도 건너뛴다.**
- 낱말 선택에 대한 판정이 붙는다 (같은 절, p.687):[^ramalho2022]

> I think `else` is a very poor choice for the keyword in all cases except `if`. It
> implies an excluding alternative, like, "Run this loop, otherwise do that," but the
> semantics for `else` in loops is the opposite: "Run this loop, then do that." This
> suggests `then` as a better keyword—which would also make sense in the `try` context:
> "Try this, then do that." However, adding a new keyword is a breaking change to the
> language—not an easy decision to make.

  - 저자 자신도 처음에는 그 낱말 때문에 이해가 막혔다고 적는다 — **처음에는 `else`라는
    낱말이 실제로 이 기능들에 대한 내 이해를 방해했지만, 결국 익숙해졌다** (같은 절,
    p.687).[^ramalho2022]
- 그래도 쓰라는 근거 — **이 문들과 함께 `else`를 쓰면 종종 코드가 읽기 쉬워지고 제어 플래그를
  세우거나 여분의 `if` 문을 짜는 수고를 던다** (같은 절, p.687).[^ramalho2022]
- `try` 쪽에서는 `else`가 처음엔 군더더기로 보이는데, 저자의 논거가 범위에 있다 — 예상
  예외를 낼 문장만 `try` 몸통에 두라는 조문이다. 그 처방이 이 페이지의 대표 코드다
  (같은 절, p.688):[^ramalho2022]

  ```python
  try:
      dangerous_call()
  except OSError:
      log('OSError...')
  else:
      after_call()
  ```

  - 저자가 그 앞의 나쁜 형태(같은 `try` 몸통에 `dangerous_call()`과 `after_call()`을
    나란히 두는 것)를 이렇게 기각한다 — **그렇게 하면 아무 좋은 이유 없이
    `after_call()`을 `try` 블록 안에 넣는 것이다. 명료함과 정확성을 위해 `try` 블록의
    몸통에는 예상되는 예외를 일으킬 수 있는 문장만 있어야 한다** (같은 절,
    p.688).[^ramalho2022]
  - 고친 뒤에 얻는 것 둘 — **이제 `try` 블록이 `after_call()`이 아니라
    `dangerous_call()`의 가능한 오류를 막고 있다는 것이 분명해진다. 그리고 `try` 블록에서
    예외가 일어나지 않을 때에만 `after_call()`이 실행된다는 것도 명시적이다** (같은 절,
    p.688).[^ramalho2022]
- 루프 쪽의 관용도 한 형태로 굳어 있다 — 저자가 든 것은 `for` 안에서 조건을 만나면
  `break`하고, 끝까지 갔으면 `else`에서 `ValueError`를 일으키는 꼴이다 (같은 절,
  pp.687–688).[^ramalho2022]

## EAFP와 LBYL

- 이 어휘가 `else`를 쓸 이유를 강화한다 — **파이썬에서 `try`/`except`는 오류 처리만이
  아니라 제어 흐름에도 흔히 쓰인다. 공식 파이썬 용어집에 그것을 가리키는 약어이자 구호까지
  문서화돼 있다** (같은 절, p.688).[^ramalho2022] 용어집 정의를 직인용한다 (같은 절,
  p.688):[^ramalho2022]

> *EAFP*
> Easier to ask for forgiveness than permission. This common Python coding style assumes
> the existence of valid keys or attributes and catches exceptions if the assumption
> proves false. This clean and fast style is characterized by the presence of many `try`
> and `except` statements. The technique contrasts with the *LBYL* style common to many
> other languages such as C.

> *LBYL*
> Look before you leap. This coding style explicitly tests for pre-conditions before
> making calls or lookups. This style contrasts with the *EAFP* approach and is
> characterized by the presence of many `if` statements. In a multi-threaded environment,
> the LBYL approach can risk introducing a race condition between "the looking" and "the
> leaping." For example, the code, `if key in mapping: return mapping[key]` can fail if
> another thread removes `key` from `mapping` after the test, but before the lookup. This
> issue can be solved with locks or by using the EAFP approach.

- 결론 — **EAFP 스타일을 생각하면 `try`/`except` 문에서 `else` 블록을 알고 잘 쓰는 것이
  더욱더 말이 된다** (같은 절, p.689).[^ramalho2022]
- 이 용어집의 LBYL 항목이 이 KB의 동시성 축과 닿는다 — 검사와 사용 사이의 경쟁 상태는
  같은 것을 다른 말로 부르는 자리이고, 그 정본은
  [공유 상태는 잘못된 상태다](../concepts/shared-state-is-incorrect-state.md)에 있다.

## 파이썬에 적정 꼬리 호출이 없는 이유

- 배경 — **표준 Scheme 구현은 적정 꼬리 호출(proper tail calls, PTC)을 제공하도록 요구받는다.
  명령형 언어의 `while` 루프에 대한 실용적 대안으로 재귀를 통한 반복을 만들기 위해서다**
  (18장 §"Soapbox — Efficient Recursion with Proper Tail Calls", p.691).[^ramalho2022]
- 정의 — **꼬리 호출(tail call)은 함수가 어떤 함수 호출의 결과를 그대로 돌려주는 것이다.
  그 함수가 자기 자신일 수도 아닐 수도 있다** (같은 절, p.691).[^ramalho2022] `n *
  factorial(n - 1)`은 꼬리 호출이 아니다 — **반환값이 재귀 호출의 결과가 아니기 때문이다:
  결과가 반환되기 전에 `n`이 곱해진다.**
- 그 기제가 아끼는 것 — **PTC가 언어에 지원되면, 인터프리터가 꼬리 호출을 볼 때 새 스택
  프레임을 만들지 않고 호출된 함수의 몸통으로 뛰어들어 메모리를 아낀다** (같은 절,
  p.692).[^ramalho2022]
- 파이썬의 입장 — **파이썬에는 PTC가 없으므로 꼬리 재귀 함수를 짜는 이점이 없다** (같은
  절, p.692).[^ramalho2022] Guido van Rossum의 사유가 직인용된다 (18장 §"Soapbox — The
  Case Against Proper Tail Calls in Python and JavaScript", p.692):[^ramalho2022]

> Personally, I think it is a fine feature for some languages, but I don't think it fits
> Python: the elimination of stack traces for some calls but not others would certainly
> confuse many users, who have not been raised with tail call religion but might have
> learned about call semantics by tracing through a few calls in a debugger.

- 저자의 판정 — **나는 Guido와 대다수 JS 구현자들에게 동의한다: PTC는 파이썬이나
  JavaScript에 잘 맞지 않는다. PTC의 부재는 함수형 스타일로 파이썬 프로그램을 쓰는 데
  주된 제약이다 — 제한된 `lambda` 문법보다도 더** (같은 절, p.693).[^ramalho2022]
- 다만 재귀 자체가 기각되지는 않는다 — Guido의 다른 글이 인용된다: **전형적인 파이썬
  구현은 재귀 1,000번을 허용하는데, 비재귀적으로 쓰인 코드에는 충분하고, 예컨대 전형적인
  파스 트리를 훑기 위해 재귀하는 코드에도 충분하지만, 큰 리스트를 도는 재귀 루프에는
  충분하지 않다** (같은 절, p.693).[^ramalho2022]

## 이어지는 페이지

- [컨텍스트 매니저 프로토콜](../concepts/context-manager-protocol.md) — 같은 장의 앞부분이자 이 장이
  다루는 세 문법 중 저자가 가장 무겁게 다루는 것
- [클로저와 데코레이터](../concepts/closures-and-decorators.md) — 여기 나온 `nonlocal`과 자유 변수의
  정본. Scheme의 `set!`이 그 대응물이다
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 시퀀스 패턴 매칭 자체의 문법이
  이 KB에 반입되지 않은 사유가 그쪽 장의 `skipped` 항목에 있다
- [일급 함수로 다시 쓰는 디자인 패턴](../concepts/design-patterns-with-first-class-functions.md) —
  같은 소스가 언어 기능이 설계 어휘를 바꾸는 것을 다루는 다른 자리
- [공유 상태는 잘못된 상태다](../concepts/shared-state-is-incorrect-state.md) — LBYL의
  경쟁 상태 경고가 닿는 자리
- [죽은 프로그램은 거짓말하지 않는다](../concepts/dead-programs-tell-no-lies.md) — 예외를 제어 흐름에
  쓰는 것에 대한 다른 소스의 입장
- [파이썬의 제어 흐름 기제](../synthesis/python-control-flow-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 18장 "with, match, and else Blocks" 도입(pp.657–658) ·
    §"Pattern Matching in lis.py: A Case Study"(p.669) · §"Scheme Syntax"(pp.669–670) ·
    §"The Parser"(pp.671–673) · §"The Evaluator"(pp.676–684) · §"Why Languages Have
    Reserved Keywords"(p.679) · §"Python's nonlocal and Scheme's set! Address the Same
    Issue"(p.683) · §"Procedure: A Class Implementing a Closure"(pp.685–686) ·
    §"Using OR-patterns"(p.686) · §"Do This, Then That: else Blocks Beyond if"(pp.687–689) ·
    §"Soapbox"(pp.691–693). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀
    값이고, 그 오프셋 실측과 판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이
    정본이다. 그림 18-1(lambda 식의 구체 구문·트리·추상 구문 대비)은 이미지로 조판돼 있어
    본문 서술로만 옮겼다. 코드 펜스는 §"Do This, Then That"의 `try`/`except`/`else` 처방
    원문이다. `evaluate`의 `match` 문 전문(예제 18-17)은 펜스로 옮기지 않았다 —
    `Procedure`·`Environment`·`parse`가 함께 있어야 돌아가는 코드라 "펜스는 복사해서
    돌아가야 한다"는 이 KB의 조문에 맞지 않아서다. 개별 `case` 절은 인라인으로 옮겼다.
    PDF 724쪽은 도비라라 추출이 OCR 필요 판정을 냈다 — 손실 아님.

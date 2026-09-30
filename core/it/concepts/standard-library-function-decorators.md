---
type: concept
title: 표준 라이브러리의 함수 데코레이터
description: functools가 데코레이터로 내주는 세 기능이 무엇을 주고 무슨 조건을 요구하는가 — 메모이제이션의 정의와 캐시 키가 인자에서만 만들어진다는 사실, 인자가 해시 가능해야 한다는 요구, functools.cache가 무한히 자라 메모리를 다 쓸 수 있다는 경고와 저자가 그은 적용 범위(짧게 사는 스크립트 대 오래 사는 프로세스), lru_cache의 maxsize·typed와 maxsize=None이 곧 cache라는 대응, 그리고 singledispatch가 만드는 일반 함수와 그것이 자바식 오버로딩이 아닌 이유 — 모듈 확장이지 한 코드 단위에 책임을 몰아넣는 것이 아니다
generated: { by: "claude-opus-5", at: "2026-08-18T12:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 표준 라이브러리의 함수 데코레이터

- [버전 조건](#버전-조건)
- [세 가지와 그 밖의 것들](#세-가지와-그-밖의-것들)
- [메모이제이션이란 무엇인가](#메모이제이션이란-무엇인가)
- [무엇이 캐시 키가 되는가](#무엇이-캐시-키가-되는가)
- [무한히 자란다 — 저자가 그은 적용 범위](#무한히-자란다--저자가-그은-적용-범위)
- [lru_cache — 경계가 있는 판](#lru_cache--경계가-있는-판)
- [이 KB의 조항이 여기 기대는 것](#이-kb의-조항이-여기-기대는-것)
- [singledispatch — 일반 함수](#singledispatch--일반-함수)
- [자바식 오버로딩이 아니다](#자바식-오버로딩이-아니다)
- [인스턴스 단위 캐시 — cached_property의 세 한계](#인스턴스-단위-캐시--cached_property의-세-한계)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **`functools`가 데코레이터로 내주는 기능들은 무엇을 사고 무엇을 지불하는가.**

기제 쪽 — 데코레이터가 왜 함수를 갈아치우고 클로저가 어떻게 그것을 떠받치는가 — 는
[클로저와 데코레이터](../concepts/closures-and-decorators.md)가 갖는다. 이 페이지는 **표준 라이브러리가
이미 만들어 둔 것들**과 그 적용 조건만 다룬다.

## 버전 조건

> **버전 조건**: 파이썬 3.9 이상에서 `functools.cache`를 쓸 수 있다. **3.8에서는 같은 자리에
> `@lru_cache`를 쓰고, 그 이전 판에서는 `@lru_cache()`처럼 호출해야 한다.** `functools.
> singledispatch`는 파이썬 3.4부터 있으나 **타입 힌트로 등록하는 방식은 3.7 이상**이다.
> 아래 서술은 소스가 실측한 2021년 7월 시점의 표준 라이브러리 기준이다.

## 세 가지와 그 밖의 것들

- 메서드를 꾸미도록 설계된 내장 함수가 셋 있다 — **`property`·`classmethod`·`staticmethod`**
  (9장 §"Decorators in the Standard Library", p.320).[^ramalho2022] 이 장은 그것들을 다루지
  않고 다른 장으로 넘긴다.
- 이 장이 다루는 것은 `functools`의 넷이다 — 잘 굴러가는 데코레이터를 만드는 도우미
  `functools.wraps`, 그리고 **표준 라이브러리에서 가장 흥미로운 데코레이터들인 `cache`·
  `lru_cache`·`singledispatch`** (9장 §"Decorators in the Standard Library",
  p.320).[^ramalho2022]

## 메모이제이션이란 무엇인가

- 정의 (9장 §"Memoization with functools.cache", p.320):[^ramalho2022]

  > The `functools.cache` decorator implements *memoization*: an optimization technique
  > that works by saving the results of previous invocations of an expensive function,
  > avoiding repeat computations on previously used arguments.

  - **낱말 자체가 오타로 오해받는 것을 저자가 각주로 막는다** — **분명히 해 두자면 이것은
    오타가 아니다: memoization은 "memorization"과 막연히 관련은 있으나 같지 않은 컴퓨터 과학
    용어다** (9장 §"Memoization with functools.cache", p.320 각주 5).[^ramalho2022]
- 효과의 크기를 소스가 실측으로 남긴다. 피보나치를 재귀로 계산하는 예제에서 **`fibonacci(30)`을
  계산할 때 캐시를 쓴 예제 9-18은 필요한 31번의 호출을 총 0.00017초에 마쳤고, 캐시 없는
  예제 9-17은 인텔 코어 i7 노트북에서 12.09초가 걸렸다 — `fibonacci(1)`을 832,040번 불렀고
  총 호출은 2,692,537번이었다** (9장 §"Memoization with functools.cache",
  p.322).[^ramalho2022]

- 두 줄을 더하는 것으로 끝난다는 것이 이 절의 요지다. 아래가 그 두 줄이고, **`@cache`가
  `@clock` 위에 얹혀 있다는 것**이 결과를 정한다 — 쌓인 데코레이터는 아래에서 위로
  적용되므로 계측되는 것은 캐시를 통과한 뒤의 호출이다
  (9장 §"Memoization with functools.cache" 예제 9-18, pp.321–322).[^ramalho2022]

  ```python
  import functools

  from clockdeco import clock

  @functools.cache
  @clock
  def fibonacci(n):
      if n < 2:
          return n
      return fibonacci(n - 2) + fibonacci(n - 1)

  if __name__ == '__main__':
      print(fibonacci(6))
  ```

## 무엇이 캐시 키가 되는가

**이 절이 이 페이지에서 가장 중요한 조건이다.**

- 조문 (9장 §"Memoization with functools.cache", p.323):[^ramalho2022]

  > All the arguments taken by the decorated function must be *hashable*, because the
  > underlying `lru_cache` uses a `dict` to store the results, and the keys are made from
  > the positional and keyword arguments used in the calls.

- 두 가지가 여기서 동시에 따라 나온다.
  - **요구 조건** — 인자가 해시 가능(hashable)해야 한다. 리스트나 딕셔너리를 인자로 받는 함수는
    그대로는 캐시할 수 없다. 해시 가능성의 계약이 무엇인지는
    [딕셔너리와 집합](../concepts/dictionaries-and-sets.md)이 정본이다.
  - **범위의 한계** — 키는 **호출에 쓰인 위치 인자와 키워드 인자로만** 만들어진다. 위 정의도
    같은 말을 다른 쪽에서 한다: 메모이제이션이 피하는 것은 **이전에 쓰인 인자에 대한 반복
    계산**이다.
- 저자가 이 기법이 빛나는 자리로 하나를 더 든다 — **바보 같은 재귀 알고리즘을 쓸 만하게 만드는
  것 말고도, `@cache`는 원격 API에서 정보를 가져와야 하는 애플리케이션에서 정말 빛난다**
  (9장 §"Memoization with functools.cache", p.323).[^ramalho2022]
  - **이 문장은 그대로 읽어야 한다.** 소스는 원격 호출의 캐싱을 권하고 있고, 그 원격 값이
    변할 때 무엇을 해야 하는지는 이 장에서 말하지 않는다.

## 무한히 자란다 — 저자가 그은 적용 범위

- 경고 상자 전문 (9장 §"Memoization with functools.cache", p.323):[^ramalho2022]

  > `functools.cache` can consume all available memory if there is a very large number of
  > cache entries. I consider it more suitable for use in short-lived command-line scripts.
  > In long-running processes, I recommend using `functools.lru_cache` with a suitable
  > `maxsize` parameter, as explained in the next section.

- **저자가 스스로 적용 범위를 나눈 유일한 자리다.** 짧게 사는 명령줄 스크립트와 오래 사는
  프로세스가 갈리고, 뒤쪽에는 `@cache`가 아니라 경계가 있는 `@lru_cache`가 권고된다.

## lru_cache — 경계가 있는 판

- 관계 — **`functools.cache` 데코레이터는 사실 더 오래된 `functools.lru_cache` 함수를 감싼
  단순한 껍데기이고, 그쪽이 더 유연하며 파이썬 3.8 이하와 호환된다** (9장 §"Using lru_cache",
  p.323).[^ramalho2022]
- 이점 — **`@lru_cache`의 주된 이점은 메모리 사용량이 `maxsize` 매개변수로 경계 지어진다는
  것이고, 그 기본값은 128이라는 꽤 보수적인 값이다 — 캐시가 어느 때든 최대 128개 항목을
  들고 있다는 뜻이다** (9장 §"Using lru_cache", p.323).[^ramalho2022]
- 이름의 뜻 — **LRU는 Least Recently Used의 약자로, 한동안 읽히지 않은 오래된 항목이 새것에
  자리를 내주려고 버려진다는 뜻이다** (9장 §"Using lru_cache", p.323).[^ramalho2022]
- 매개변수 둘 (9장 §"Using lru_cache", pp.323–324):[^ramalho2022]

  | 매개변수 | 기본값 | 무엇을 정하는가 |
  |---|---|---|
  | `maxsize` | 128 | 보관할 항목의 최대 수. 캐시가 차면 새 항목마다 가장 오래 안 쓰인 항목이 버려진다. 최적 성능을 위해 2의 거듭제곱이어야 한다 |
  | `typed` | `False` | 서로 다른 인자 타입의 결과를 따로 보관할지. 기본값에서는 같다고 여겨지는 실수와 정수 인자가 한 번만 저장되어 `f(1)`과 `f(1.0)`의 항목이 하나다. `True`면 별개 항목이 되어 서로 다른 결과를 보관할 수 있다 |

- **그리고 두 데코레이터를 잇는 대응 관계** — **`maxsize=None`을 넘기면 LRU 로직이 꺼져서
  캐시가 더 빨리 동작하지만 항목이 결코 버려지지 않고, 그래서 메모리를 너무 많이 쓸 수 있다.
  그것이 `@functools.cache`가 하는 일이다** (9장 §"Using lru_cache", p.323).[^ramalho2022]
  - 즉 **`@cache` = `@lru_cache(maxsize=None)`**이고, `@cache`에는 항목을 버리는 기제가
    아예 없다.

## 이 KB의 조항이 여기 기대는 것

이 저장소의 도구 구현 헌장에는 **상태를 읽는 함수에 숨은 memoization을 두지 않는다**는 조항이
있다(정본은 `PLAN.md` §3, 실패 기록은 `LEDGER.md`). 그 조항의 **언어 쪽 근거가 이 절이다.**

- 소스가 말한 것만 다시 세우면 셋이다.
  - 캐시 키는 **호출에 쓰인 위치 인자와 키워드 인자로만** 만들어진다 (9장 §"Memoization with
    functools.cache", p.323).[^ramalho2022]
  - 메모이제이션이 피하는 것은 **이전에 쓰인 인자에 대한 반복 계산**이다 (9장 §"Memoization
    with functools.cache", p.320).[^ramalho2022]
  - `@cache`에는 경계가 없고, 저자는 그것을 **짧게 사는 명령줄 스크립트**에 더 알맞다고 보며
    오래 사는 프로세스에는 `maxsize`가 붙은 `@lru_cache`를 권한다 (9장 §"Memoization with
    functools.cache", p.323).[^ramalho2022]
- **여기서부터는 이 KB의 읽기이지 소스의 주장이 아니다.** 위 셋에서 곧장 따라 나오는 것은,
  함수의 결과가 인자 말고 다른 것 — 디스크의 파일 내용, 프로세스 밖의 상태 — 에 달려 있으면
  그 의존을 **키로 표현할 방법이 없다**는 사실이다. 같은 인자로 다시 부르면 캐시는 옛 결과를
  돌려주고, 바깥이 바뀌었다는 사실은 캐시가 알 길이 없다. 소스는 이 결론을 적지 않았다 —
  적은 것은 키가 인자에서만 만들어진다는 사실뿐이다.
- **소스가 이 KB의 조항과 어긋나 보이는 자리도 그대로 남긴다.** 저자는 `@cache`가 **원격
  API에서 정보를 가져오는 애플리케이션에서 정말 빛난다**고 적는다 (9장 §"Memoization with
  functools.cache", p.323).[^ramalho2022] 원격 값은 정의상 바깥 상태다. 이 소스는 참조서이지
  설계 규범서가 아니고, 그 문장은 **기능이 어디에 쓰이는가**를 말하는 것이지 신선도를 어떻게
  보장하는가를 말하지 않는다. 이 장 어디에도 무효화(invalidation) 절차는 없다.
- 그래서 이 KB가 이 소스에서 가져가는 것은 **금지 조항이 아니라 그 조항이 서 있는 사실
  관계**다 — 캐시는 인자만 보고, `@cache`는 버리지 않으며, 저자 자신이 오래 사는 프로세스에는
  경계를 요구했다는 것.

## singledispatch — 일반 함수

- 풀려는 문제 — 타입마다 다르게 동작하는 `htmlize` 같은 함수를 만들려는데 **파이썬에는
  자바식 메서드 오버로딩이 없다.** 파이썬에서 가능한 해법은 `htmlize`를 `if/elif/…`나
  `match/case/…` 사슬을 가진 디스패치 함수로 만드는 것인데 — **이것은 우리 모듈의 사용자가
  확장할 수 없고 다루기 힘들다: 시간이 지나면 `htmlize` 디스패처가 너무 커지고, 그것과
  특수화된 함수들 사이의 결합이 매우 강해진다** (9장 §"Function singledispatch",
  pp.325–326).[^ramalho2022]
- 처방 — **`functools.singledispatch` 데코레이터는 서로 다른 모듈들이 전체 해법에 기여할 수
  있게 해 주고, 편집할 수 없는 서드파티 패키지에 속한 타입에 대해서도 특수화된 함수를 쉽게
  제공하게 해 준다** (9장 §"Function singledispatch", p.326).[^ramalho2022]
- **일반 함수(generic function)**의 규정 — **평범한 함수를 `@singledispatch`로 꾸미면 그것은
  일반 함수의 진입점이 된다: 첫 번째 인자의 타입에 따라 같은 연산을 다른 방식으로 수행하는
  함수들의 묶음이다. 이것이 단일 디스패치(single dispatch)라는 용어가 뜻하는 바다. 특정 함수를
  고르는 데 인자가 더 쓰인다면 다중 디스패치(multiple dispatch)가 될 것이다**
  (9장 §"Function singledispatch", p.326).[^ramalho2022]
- 해소 규칙 — **`bool`은 `numbers.Integral`의 하위 타입이지만 `singledispatch` 로직은 코드에
  나타나는 순서와 무관하게 가장 구체적으로 맞는 타입의 구현을 찾는다** (9장 §"Function
  singledispatch", p.327).[^ramalho2022]
- **등록 대상에 대한 지침이 이 절의 설계 조언이다** — **가능하면 `int`나 `list` 같은 구체
  구현이 아니라 `numbers.Integral`이나 `abc.MutableSequence` 같은 ABC(추상 클래스)를 다루도록
  특수화된 함수를 등록하라. 그러면 코드가 더 다양한 호환 타입을 지원할 수 있다**
  (9장 §"Function singledispatch", p.327).[^ramalho2022]
  - 그 이유가 뒤따른다 — **`@singledispatch`와 함께 ABC나 `typing.Protocol`을 쓰면 그 ABC의
    실제 또는 가상 하위 클래스이거나 그 프로토콜을 구현하는 기존·미래의 클래스를 코드가 지원할
    수 있다** (9장 §"Function singledispatch", p.328).[^ramalho2022] 무엇이 ABC이고 무엇이
    `Protocol`인가의 판단은
    [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md)가 정본이다.
- 확장성의 실물 — **`singledispatch` 기제의 눈에 띄는 성질은 특수화된 함수를 시스템 어디에나,
  어느 모듈에나 등록할 수 있다는 것이다. 나중에 새 사용자 정의 타입을 가진 모듈을 추가하면
  그 타입을 다룰 새 맞춤 함수를 쉽게 제공할 수 있다. 그리고 당신이 쓰지 않았고 바꿀 수 없는
  클래스를 위한 맞춤 함수도 쓸 수 있다** (9장 §"Function singledispatch", p.328).[^ramalho2022]
- 한계도 각주에 실측으로 남아 있다 — `Union`으로 여러 타입을 한 번에 등록하려 하자
  **파이썬이 `Union`은 클래스가 아니라는 메시지와 함께 `TypeError`를 일으켰다. 그러니까
  `@singledispatch`가 PEP 484 *문법*은 지원하지만 *의미론*은 아직 거기 없다**
  (9장 §"Function singledispatch", p.328 각주 8).[^ramalho2022]

## 자바식 오버로딩이 아니다

- 곁글 하나가 이 기능의 오용을 미리 막는다 (9장 §"Function singledispatch",
  p.329):[^ramalho2022]

  > `@singledispatch` is not designed to bring Java-style method overloading to Python. A
  > single class with many overloaded variations of a method is better than a single
  > function with a lengthy stretch of `if/elif/elif/elif` blocks. But both solutions are
  > flawed because they concentrate too much responsibility in a single code unit—the class
  > or the function.

- 그래서 이 기능의 이점이 다시 좁혀진다 — **`@singledispatch`의 이점은 모듈 단위 확장을
  지원한다는 것이다: 각 모듈이 자기가 지원하는 타입마다 특수화된 함수를 등록할 수 있다**
  (9장 §"Function singledispatch", p.329).[^ramalho2022]
  - 그리고 예제의 배치가 현실적이지 않다는 자백이 붙는다 — **현실적인 사용 사례라면 예제 9-20
    처럼 일반 함수의 모든 구현이 같은 모듈에 있지는 않을 것이다** (9장 §"Function
    singledispatch", p.329).[^ramalho2022]
- **이 판정이 이 KB의 다른 축과 겹치는 지점**: "한 코드 단위에 너무 많은 책임을 몰아넣는다"는
  진단은 [복잡성의 정의와 증상](../concepts/software-complexity-defined.md)이 말하는 변경 증폭·인지 부하와
  같은 것을 가리킨다. 이 소스는 그 판정을 원리로 세우지 않고 **한 기능을 어떻게 쓰지 말아야
  하는가**로만 쓴다.

## 인스턴스 단위 캐시 — cached_property의 세 한계

같은 소스가 22장에서 **인스턴스 하나에 붙는 캐시**를 따로 다루는데, 여기 `@cache`와는
저장 자리가 다르고 그래서 함정도 다르다.

- 손수 만든 캐시가 두 가지를 깬다.
  - **인스턴스가 초기화된 뒤에 속성을 만드는 것은 PEP 412 키 공유 딕셔너리 최적화를
    무력화한다. 데이터셋 크기에 따라 메모리 사용의 차이가 중요할 수 있다** (22장 §"Step 4:
    Bespoke Property Cache", p.854).[^ramalho2022]
  - **멀티스레드 프로그램에서 이런 손수 만든 캐시는 데이터 손상으로 이어질 수 있는 경쟁
    상태를 들여온다. 두 스레드가 이전에 캐시되지 않은 프로퍼티를 읽으면, 첫 스레드가 캐시
    속성의 데이터를 계산해야 하고 둘째 스레드는 아직 완성되지 않은 캐시된 값을 읽을 수
    있다** (같은 절, p.855).[^ramalho2022]
- 표준 해법의 이름이 거짓말을 한다 — **답은 조금 슬프다: `cached_property`는 잘못 붙은
  이름이다. `@cached_property` 데코레이터는 완전한 프로퍼티를 만들지 않고 비오버라이딩
  디스크립터를 만든다** (22장 §"Step 5: Caching Properties with functools",
  p.855).[^ramalho2022] 그 정체의 정본은
  [속성 디스크립터](../concepts/attribute-descriptors.md)에 있다.
- 한계 셋 (같은 절, p.856):[^ramalho2022]
  - **장식되는 메서드가 같은 이름의 인스턴스 속성에 이미 의존한다면 `@property`의 드롭인
    대체로 쓸 수 없다.**
  - **`__slots__`를 정의하는 클래스에서 쓸 수 없다.**
  - **인스턴스 `__dict__`의 키 공유 최적화를 무력화한다. `__init__` 뒤에 인스턴스 속성을
    만들기 때문이다.**
- 그래도 채택할 이유가 하나 남는다 — **이 한계에도 불구하고 `@cached_property`는 흔한
  필요를 단순한 방식으로 다루며 스레드 안전하다** (같은 절, p.856).[^ramalho2022]
- 한계에 걸리면 이 페이지의 `@cache`가 처방에 다시 등장한다 — **`@cached_property` 문서가
  대안을 권한다: `@property`와 `@cache` 데코레이터를 쌓는 것** (같은 절,
  p.856).[^ramalho2022] **순서가 중요하다 — `@property`가 `@cache` 위로 간다.**
  - 버전 조건: `functools.cached_property`는 파이썬 3.8, `functools.cache`는 3.9에
    더해졌다.
- **이 저장소 헌장의 "상태를 읽는 함수에 숨은 memoization 금지" 조항에 이것이 더하는
  것**: 위 [이 KB의 조항이 여기 기대는 것](#이-kb의-조항이-여기-기대는-것)이 인자 기반
  캐시를 다뤘다면, 이 절은 **인스턴스에 붙는 캐시가 조용히 두 가지를 더 산다**는 것을
  더한다 — 메모리 배치의 변화와 스레드 안전성 문제. 둘 다 캐시를 넣은 쪽에서는 안 보이는
  비용이다.

## 이어지는 페이지

- [클로저와 데코레이터](../concepts/closures-and-decorators.md) — 같은 장의 앞부분. 이 데코레이터들이
  무슨 기제 위에 서 있는가
- [동적 속성과 프로퍼티](../concepts/dynamic-attributes-and-properties.md) — 인스턴스 단위 캐시가
  나오는 그 장의 정본
- [속성 디스크립터](../concepts/attribute-descriptors.md) — `@cached_property`가 실제로 무엇인가
- [__slots__와 인스턴스 메모리](../concepts/slots-and-instance-memory.md) — 여기 한계 둘이 걸리는
  그 클래스 속성과 키 공유 최적화
- [딕셔너리와 집합](../concepts/dictionaries-and-sets.md) — 캐시가 요구하는 해시 가능성의 계약
- [인터페이스·프로토콜·ABC](../concepts/interfaces-protocols-and-abcs.md) — `singledispatch`에 무엇을
  등록할 것인가의 판단이 기대는 자리
- [파이썬의 일급 함수](../concepts/first-class-functions-in-python.md) — `functools`의 나머지 고차 함수들
- [부수 효과 없는 함수](../concepts/side-effect-free-functions.md) — 결과가 인자에만 달려 있어야 한다는
  요구를 설계 조항으로 말하는 쪽
- [복잡성의 정의와 증상](../concepts/software-complexity-defined.md) — 한 코드 단위에 책임을 몰아넣는 것의
  대가를 원리로 말하는 쪽
- [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 9장 "Decorators and Closures" — §"Decorators in the Standard
    Library"(p.320) · §"Memoization with functools.cache"(pp.320–323) · §"Using
    lru_cache"(pp.323–324) · §"Single Dispatch Generic Functions"(pp.324–329) ·
    §"Function singledispatch"(pp.325–329). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 30).
    예제 9-18은 원문 그대로이며 조판용 번호 표지만 제거했다 — `clockdeco`는 같은 장
    예제 9-16의 모듈이다. 예제 9-19(콘솔 세션)와 예제 9-20(`htmlize` 전체 구현)은 각각
    프롬프트가 섞였고 길어서 펜스로 옮기지 않고 규칙만 서술했다.
    인스턴스 단위 캐시 절은 같은 소스의 22장 "Dynamic Attributes and Properties"
    §"Step 4: Bespoke Property Cache"(pp.853–855) · §"Step 5: Caching Properties with
    functools"(pp.855–857)에서 왔다.

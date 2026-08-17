---
type: concept
title: 동시 실행기와 asyncio
description: 스레드·프로세스 다발을 인프라로 감추는 실행기 층과 그것이 감추는 future의 정체, 네이티브 코루틴이 무엇을 요구하는가와 async 키워드가 전염된다는 전부 아니면 전무 문제, with·for·컴프리헨션의 비동기 짝이 각각 어떤 특수 메서드에 얹히는가, 그리고 "I/O 바운드 시스템"이 신화라는 판정과 CPU 병목을 프로젝트 시작에 결정하라는 처방
generated: { by: "claude-opus-5", at: "2026-08-18T21:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 동시 실행기와 asyncio

- [버전 조건과 재심 트리거](#버전-조건과-재심-트리거)
- [실행기는 스레드를 인프라로 감춘다](#실행기는-스레드를-인프라로-감춘다)
- [future는 우리가 만드는 것이 아니다](#future는-우리가-만드는-것이-아니다)
- [map과 submit의 교환](#map과-submit의-교환)
- [코루틴 세 갈래와 awaitable](#코루틴-세-갈래와-awaitable)
- [전부 아니면 전무](#전부-아니면-전무)
- [비동기 짝들 — with·for·컴프리헨션](#비동기-짝들--withfor컴프리헨션)
- [구조적 동시성](#구조적-동시성)
- ["I/O 바운드 시스템"은 없다](#io-바운드-시스템은-없다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **동시 실행을 라이브러리에 맡길 때 무엇이 감춰지고, 그 추상이 새는 자리는
어디인가.**

**이 페이지는 얇다.** 두 장의 예제 대부분은 특정 HTTP 클라이언트 라이브러리와 웹 서비스
프레임워크에 묶인 코드이고, 이 KB의 L3 원칙상 그런 지형은 얇게 둔다. 여기 남긴 것은
**판이 바뀌어도 남는 개념과 판단**이다. 동시성 모델 자체의 어휘와 GIL 서술은
[파이썬의 동시성 모델](../concepts/concurrency-models-in-python.md)이 갖는다.

## 버전 조건과 재심 트리거

> **버전 조건**: 이 두 장의 서술은 **파이썬 3.10, 2021년 10월 시점**의 실측이다. 저자가
> 그 시점을 여러 번 명시한다 — 파이썬 3.10 기준 asyncio가 TCP와 UDP만 직접 지원하고 표준
> 라이브러리에 비동기 HTTP 클라이언트·서버 패키지가 없다는 것, `@asyncio.coroutine`이
> 3.8에서 폐기되어 3.11에 제거 예정이라는 것, 구조적 동시성이 아직 asyncio에 없다는 것이
> 전부 그 시점의 관측이다. **이 문단이 다루는 라이브러리 지형은 그 뒤로 바뀌었을 수 있다.**
>
> **재심 트리거**: ⑴ asyncio에 태스크 그룹 계열의 구조적 동시성 API가 들어올 때 — 저자
> 자신이 PEP 654를 그 신호로 지목한다, ⑵ 표준 라이브러리에 비동기 HTTP 계층이 들어올 때,
> ⑶ GIL 자체가 바뀔 때(PEP 554 계열의 서브인터프리터 작업이 결실을 볼 때).
> 개념 쪽 — future의 규정, awaitable, 전부 아니면 전무 문제, "I/O 바운드 시스템" 판정 —
> 은 그 트리거의 대상이 아니다.
>
> **`stale_after`는 달지 않았다.** 이 페이지의 판 종속 서술은 전부 위 조건이나 아래 claim의
> 자식 불릿으로 범위가 좁혀져 있고, 범위 안에서 그 서술들은 계속 참이다 — 조건을 명시하고
> 나면 시효는 조건이 대신한다(SCHEMA §3). 범위 밖의 지형 변화는 위 재심 트리거가 맡는다.

## 실행기는 스레드를 인프라로 감춘다

- 이 장의 경구가 Michele Simionato의 말이다 (20장 도입, p.743):[^ramalho2022]

> In 99% of the use cases an application programmer is likely to run into, the simple
> pattern of spawning a bunch of independent threads and collecting the results in a
> queue is everything one needs to know.

- 그 패턴을 캡슐화한 것이 실행기다 — **`concurrent.futures` 패키지의 주요 기능은
  `ThreadPoolExecutor`와 `ProcessPoolExecutor` 클래스로, 호출 가능한 것을 각각 다른
  스레드나 프로세스에서 실행하도록 제출하는 API를 구현한다. 이 클래스들은 워커 스레드나
  프로세스의 풀, 그리고 작업을 분배하고 결과를 모으는 큐를 투명하게 관리한다. 그러나
  인터페이스가 아주 고수준이라 단순한 쓰임에는 그 세부를 전혀 알 필요가 없다** (20장
  §"Downloading with concurrent.futures", p.749).[^ramalho2022]
- 이 층이 사 오는 것 하나가 이식성이다 — **`concurrent.futures`의 가장 좋은 기능 중 하나가
  레거시 순차 코드 위에 동시 실행을 얹기 쉽게 만든다는 것이다** (같은 절,
  p.750).[^ramalho2022] 저자가 든 리팩터링 관용이 한 줄이다 — **동시 코드를 쓸 때 흔한
  리팩터링이다: 순차 `for` 루프의 몸통을 동시에 호출될 함수로 바꾸는 것** (같은 절,
  p.750).[^ramalho2022]
- 두 실행기의 교체가 한 줄 수정이다 — **`ProcessPoolExecutor`와 `ThreadPoolExecutor` 둘 다
  `Executor` 인터페이스를 구현하므로 스레드 기반에서 프로세스 기반 해법으로 바꾸는 것이
  쉽다** (20장 §"Launching Processes with concurrent.futures", p.754).[^ramalho2022]
  다만 이득이 나는 자리가 갈린다 — **플래그 다운로드 예제나 어떤 I/O 바운드 작업에도
  `ProcessPoolExecutor`를 쓸 이점이 없다.** 그리고 **프로세스는 스레드보다 메모리를 더
  쓰고 시작이 오래 걸리므로 `ProcessPoolExecutor`의 진짜 값은 CPU 집약 작업에 있다**
  (같은 절, pp.754–755).[^ramalho2022]
- 기본 워커 수의 계산과 그 사유가 문서에서 인용된다 (20장 §"Downloading with
  concurrent.futures", p.750):[^ramalho2022]

> This default value preserves at least 5 workers for I/O bound tasks. It utilizes at most
> 32 CPU cores for CPU bound tasks which release the GIL. And it avoids using very large
> resources implicitly on many-core machines.

  저자의 결론 — **계산된 `max_workers` 기본값은 합당하고, `ThreadPoolExecutor`는 불필요하게
  새 워커를 시작하지 않는다. `max_workers` 뒤의 논리를 이해하면 언제 어떻게 그것을 직접
  설정할지 판단하는 데 도움이 될 수 있다** (같은 절, p.750).[^ramalho2022]
  - 버전 조건: 파이썬 3.8 이상. 그 판부터 `ThreadPoolExecutor`의 기본
    `max_workers`가 `min(32, os.cpu_count() + 4)`로 계산되고 유휴 워커를 재사용한다.
- 저자의 입장이 곁글에 있다 (20장 §"Soapbox — Thread Avoidance",
  pp.773–774):[^ramalho2022]

> That's why I think the `concurrent.futures` package is interesting: it treats threads,
> processes, and queues as infrastructure at your service, not something you have to deal
> with directly.

  - 그 앞에 개인사가 붙는다 — **내가 배운 것: 나는 스레드와 락을 직접 관리하고 싶지 않다.
    메모리 할당과 해제를 직접 관리하고 싶지 않은 것과 같은 이유다. 그런 일은 그것을 제대로
    해낼 노하우와 성향과 시간을 가진 시스템 프로그래머들이 하는 것이 최선이다 —
    바라건대. 나는 애플리케이션을 개발하는 값을 받지 운영체제를 개발하는 값을 받지
    않는다** (같은 절, p.773).[^ramalho2022]
  - 적용 범위도 스스로 좁힌다 — **물론 그것은 단순한 작업, 이른바 embarrassingly parallel
    문제를 염두에 두고 설계됐다. 그러나 그것이 우리가 애플리케이션을 쓸 때 마주하는 동시성
    문제의 큰 몫이다** (같은 절, p.773).[^ramalho2022]

## future는 우리가 만드는 것이 아니다

- 규정 — **`concurrent.futures.Future`와 `asyncio.Future` 두 클래스는 같은 목적에 복무한다:
  어느 쪽 `Future` 클래스의 인스턴스든 완료됐을 수도 아닐 수도 있는 지연된 계산을
  나타낸다. Twisted의 `Deferred` 클래스, Tornado의 `Future` 클래스, 현대 JavaScript의
  `Promise`와 다소 비슷하다** (20장 §"Where Are the Futures?", p.751).[^ramalho2022]
- 쓸모 — **future는 보류 중인 연산을 캡슐화해서 우리가 그것을 큐에 넣고, 끝났는지 검사하고,
  가능해졌을 때 결과(또는 예외)를 회수할 수 있게 한다** (같은 절, p.751).[^ramalho2022]
- 그리고 소유권 조문 (같은 절, p.751):[^ramalho2022]

> An important thing to know about futures is that you and I should not create them: they
> are meant to be instantiated exclusively by the concurrency framework, be it
> `concurrent.futures` or `asyncio`.

  - 사유 — **`Future`는 결국 돌게 될 무언가를 나타내므로 실행이 예약돼야 하고, 그것이
    프레임워크의 일이다** (같은 절, p.751).[^ramalho2022]
  - 대칭 조항 — **애플리케이션 코드는 future의 상태를 바꾸어서는 안 된다: 그것이 나타내는
    계산이 끝났을 때 동시성 프레임워크가 future의 상태를 바꾸며, 우리는 그것이 언제
    일어날지 제어할 수 없다** (같은 절, p.751).[^ramalho2022]
- 알려 주는 쪽이 기본이다 — **future가 끝났는지 되풀이해 묻는 대신, 클라이언트 코드는
  보통 알려 달라고 요청한다. 그래서 두 `Future` 클래스 다 `.add_done_callback()` 메서드를
  갖는다.** 단서 하나가 붙는다 — **콜백 호출 가능한 것은 future로 감싸인 함수를 돌린 것과
  같은 워커 스레드나 프로세스에서 돈다** (같은 절, p.751).[^ramalho2022]
- 두 `Future`가 갈리는 자리 — **`concurrency.futures.Future` 인스턴스에서 `f.result()`를
  부르면 결과가 준비될 때까지 호출자의 스레드를 막는다.** 선택적 `timeout`을 줄 수 있고
  시간 안에 안 끝나면 `TimeoutError`가 난다. **`asyncio.Future.result` 메서드는 타임아웃을
  지원하지 않고, asyncio에서 future의 결과를 얻는 선호되는 방법은 `await`다 — 그러나
  `await`는 `concurrency.futures.Future` 인스턴스에는 통하지 않는다** (같은 절,
  pp.751–752).[^ramalho2022]

## map과 submit의 교환

- `Executor.map`이 감추는 것 — **그것은 `__next__`가 각 future의 `result` 메서드를 부르는
  이터레이터를 돌려주므로, 우리는 future가 아니라 future의 결과를 얻는다** (같은 절,
  p.752).[^ramalho2022] 그리고 **결과를 인자와 같은 순서로 돌려준다** (20장 §"Multicore
  Prime Checker Redux", p.756).[^ramalho2022]
- 그 순서 보존이 대가를 갖는다. 저자가 소수 검사기에서 실측을 보인다 — 내림차순으로 제출한
  탓에 두 번째 수(표본에서 가장 큰 소수)가 판정될 때까지 **9.5초 넘게 아무 줄도 나오지
  않다가**, 그것이 끝나자 **나머지 줄들이 거의 즉시 나타난다** (같은 절,
  pp.756–758).[^ramalho2022] 전체 실행 시간은 같지만 진행이 보이지 않는다.
- 그래서 완료 순으로 받는 조합이 따로 있다 — **`Executor.map` 함수는 쓰기 쉽지만, 종종
  제출된 순서와 무관하게 결과가 준비되는 대로 얻는 편이 낫다. 그러려면 `Executor.submit`
  메서드와 `futures.as_completed` 함수의 조합이 필요하다** (20장 §"Experimenting with
  Executor.map", p.761).[^ramalho2022]
- 그 조합이 더 유연한 이유 둘 (같은 절, p.761):[^ramalho2022]
  - **`executor.submit`과 `futures.as_completed`의 조합이 `executor.map`보다 유연하다.
    서로 다른 호출 가능한 것과 인자를 제출할 수 있기 때문이다. `executor.map`은 같은
    호출 가능한 것을 다른 인자들에 대해 돌리도록 설계됐다.**
  - **`futures.as_completed`에 넘기는 future 집합은 실행기 하나 이상에서 올 수 있다 —
    어떤 것은 `ThreadPoolExecutor` 인스턴스가, 다른 것은 `ProcessPoolExecutor`가 만든
    것일 수 있다.**
- 그리고 관용 하나 — **`futures.as_completed`와 아주 쓸모 있는 관용: future가 완료됐을 때
  유용할 다른 데이터에 각 future를 대응시키는 딕셔너리를 짓는 것. 이것이 future가 순서
  없이 나오더라도 결과에 대한 후속 처리를 쉽게 만든다** (20장 §"Using futures.as_completed",
  p.772).[^ramalho2022]

## 코루틴 세 갈래와 awaitable

- 정의 셋 (21장 §"A Few Definitions", p.777):[^ramalho2022]
  - *네이티브 코루틴(Native coroutine)* — **`async def`로 정의된 코루틴 함수. `await`
    키워드로 다른 네이티브 코루틴에 위임할 수 있다. 고전 코루틴이 `yield from`을 쓰는
    것과 비슷하다. `async def` 문은 몸통에 `await` 키워드가 없어도 언제나 네이티브 코루틴을
    정의한다. `await` 키워드는 네이티브 코루틴 바깥에서 쓸 수 없다.**
  - *고전 코루틴(Classic coroutine)* — **`my_coro.send(data)` 호출로 보내진 데이터를
    소비하고 식 안의 `yield`로 그 데이터를 읽는 제너레이터 함수. `await`로 몰 수 없고
    asyncio가 더 이상 지원하지 않는다.**
  - *제너레이터 기반 코루틴(Generator-based coroutine)* — **`@types.coroutine`으로 장식된
    제너레이터 함수. 그 데코레이터가 제너레이터를 새 `await` 키워드와 호환되게 만든다.**
- 그리고 비동기 제너레이터 — **`async def`로 정의되고 몸통에 `yield`를 쓰는 제너레이터
  함수. 다음 항목을 회수하는 코루틴 메서드 `__anext__`를 제공하는 비동기 제너레이터
  객체를 돌려준다** (같은 절, p.777).[^ramalho2022]
- awaitable의 규정이 대구로 적힌다 — **`for` 키워드는 이터러블과 함께 동작한다. `await`
  키워드는 awaitable과 함께 동작한다** (21장 §"New Concept: Awaitable",
  p.781).[^ramalho2022] 일상적으로 만나는 것은 둘이다 — **네이티브 코루틴 함수를 불러 얻는
  네이티브 코루틴 객체**와 **코루틴 객체를 `asyncio.create_task()`에 넘겨 얻는
  `asyncio.Task`**.
- 둘의 쓰임이 갈린다 — **태스크를 취소하거나 기다릴 생각이 없으면 `create_task`가 돌려준
  `Task` 객체를 붙들 필요가 없다. 태스크를 만드는 것만으로 코루틴 실행이 예약된다. 반면
  `await other_coro()`는 `other_coro`를 지금 돌려 완료를 기다리는 데 쓴다. 진행하기 전에
  그 결과가 필요하기 때문이다** (같은 절, p.781).[^ramalho2022]
- 읽는 요령이 Guido에게서 온다 — **눈을 가늘게 뜨고 `async`와 `await` 키워드가 없는 척하라.
  그러면 코루틴이 옛날 순차 함수처럼 읽힌다는 것을 알게 될 것이다** (21장 §"Guido's Trick
  to Read Asynchronous Code", p.780).[^ramalho2022] 다른 점은 **마법처럼 결코 막지
  않는다**는 것뿐이다.
- 바닥이 제너레이터다 — **안에서 asyncio 이벤트 루프가 당신 코루틴을 모는 `.send` 호출을
  한다. (…) `await` 사슬은 결국 저수준 awaitable에 닿고, 그것이 타이머나 네트워크 I/O
  같은 사건에 응답해 이벤트 루프가 몰 수 있는 제너레이터를 돌려준다** (21장 §"The Secret
  of Native Coroutines: Humble Generators", p.784).[^ramalho2022]
- 대표 코드가 이 장에서 가장 자립적인 예제다 (예제 21-1, pp.778–779):[^ramalho2022]

  ```python
  #!/usr/bin/env python3
  import asyncio
  import socket
  from keyword import kwlist

  MAX_KEYWORD_LEN = 4


  async def probe(domain: str) -> tuple[str, bool]:
      loop = asyncio.get_running_loop()
      try:
          await loop.getaddrinfo(domain, None)
      except socket.gaierror:
          return (domain, False)
      return (domain, True)


  async def main() -> None:
      names = (kw for kw in kwlist if len(kw) <= MAX_KEYWORD_LEN)
      domains = (f'{name}.dev'.lower() for name in names)
      coros = [probe(domain) for domain in domains]
      for coro in asyncio.as_completed(coros):
          domain, found = await coro
          mark = '+' if found else ' '
          print(f'{mark} {domain}')


  if __name__ == '__main__':
      asyncio.run(main())
  ```

  - 이 서른 줄이 이 축의 관용 넷을 한자리에 담는다: `async def`로 코루틴을 정의하고,
    `await`로 위임하고, `asyncio.as_completed`로 완료 순으로 받고, `asyncio.run`으로
    이벤트 루프를 띄운다. 찾을 것은 `asyncio.run`과 `as_completed`다.
  - 저자가 그 마지막 줄을 관용으로 못 박는다 — **`asyncio.run`은 이벤트 루프를 시작하고
    이벤트 루프가 종료할 때에만 반환한다. 이것이 asyncio를 쓰는 스크립트의 흔한 패턴이다:
    `main`을 코루틴으로 구현하고 `if __name__ == '__main__':` 블록 안에서
    `asyncio.run`으로 모는 것** (21장 §"An asyncio Example: Probing Domains",
    p.780).[^ramalho2022]
  - 버전 조건: `asyncio.get_running_loop`은 파이썬 3.7 이상. **3.10부터
    `asyncio.get_event_loop`은 폐기됐고 결국 `get_running_loop`의 별칭이 될 것이다.**

## 전부 아니면 전무

- 이 장의 경구가 그 문제다 (21장 도입, p.775):[^ramalho2022]

> The problem with normal approaches to asynchronous programming is that they're
> all-or-nothing propositions. You rewrite all your code so none of it blocks or you're
> just wasting your time.

- 실물로 확인된다 — **asyncio로 최고 성능을 내려면 I/O를 하는 모든 함수를 `await`나
  `asyncio.create_task`로 활성화되는 비동기 판으로 바꿔야 한다. 그래야 함수가 I/O를
  기다리는 동안 제어가 이벤트 루프에 돌아간다. 블로킹 함수를 코루틴으로 다시 쓸 수 없으면
  별도의 스레드나 프로세스에서 돌려야 한다** (21장 §"The All-or-Nothing Problem",
  p.785).[^ramalho2022]
- 저자가 자기 코드에서 그 전염을 겪는다 — 순차판의 함수도, 스레드풀판의 함수도 재사용할
  수 없어 전부 코루틴으로 다시 썼다고 적는다 (같은 절, pp.785–786).[^ramalho2022]
- 장 요약이 그것을 경고로 되풀이한다 — **낮은 층위에서 그것은 또한 경고다: 첫 `async def`를
  쓰는 순간, 프로그램은 불가피하게 점점 더 많은 `async def`·`await`·`async with`·
  `async for`를 갖게 된다. 그리고 비동기가 아닌 라이브러리를 쓰는 것이 갑자기 도전이
  된다** (21장 §"Chapter Summary", p.827).[^ramalho2022]
- 파일 I/O도 예외가 아니다 — **asyncio에서 모든 네트워크 I/O는 코루틴으로 하지만 파일 I/O는
  아니다. 그런데 파일 I/O도 "블로킹"이다 — 파일을 읽고 쓰는 것이 RAM을 읽고 쓰는 것보다
  수천 배 오래 걸린다는 뜻에서. 네트워크 결합 스토리지를 쓴다면 안에서 네트워크 I/O까지
  일어날 수 있다** (21장 §"Enhancing the asyncio Downloader", p.790).[^ramalho2022]
  - 버전 조건: 파이썬 3.9 이상에서 `asyncio.to_thread` 코루틴이 파일 I/O를 스레드 풀에
    위임하는 것을 쉽게 만든다. 3.7·3.8을 지원해야 하면 `loop.run_in_executor`를 쓴다.

## 비동기 짝들 — with·for·컴프리헨션

- 컨텍스트 매니저 쪽 — **고전 `with` 문의 구현은 코루틴이 `__enter__`나 `__exit__`의 일을
  하는 것을 지원하지 않는다. 그래서 PEP 492가 `async with` 문을 도입했고, 그것은 비동기
  컨텍스트 매니저와 함께 동작한다: `__aenter__`와 `__aexit__` 메서드를 코루틴으로 구현하는
  객체들이다** (21장 §"Asynchronous Context Managers", p.786).[^ramalho2022] 그것이 필요한
  이유가 앞에 있다 — **asyncpg 같은 비동기 드라이버에서는 준비와 마무리가 코루틴이어야
  다른 연산이 동시에 일어날 수 있다** (같은 절, p.786).[^ramalho2022]
- 순회 쪽 — **비슷하게 `async for`는 비동기 이터러블과 함께 동작한다: `__aiter__`를
  구현하는 객체들이다. 그러나 `__aiter__`는 코루틴 메서드가 아니라 평범한 메서드여야 하고,
  비동기 이터레이터를 돌려주어야 한다** (21장 §"Asynchronous Iteration and Asynchronous
  Iterables", p.811).[^ramalho2022] 그리고 **비동기 이터레이터는 awaitable을 돌려주는
  `__anext__` 코루틴 메서드를 제공한다. 그것들도 `__aiter__`를 구현할 것으로 기대되며 보통
  `self`를 돌려준다.**
  - 저자가 그 대칭을 명시한다 — **이것이 §"Don't Make the Iterable an Iterator for Itself"에서
    논한 이터러블과 이터레이터의 중요한 구분을 그대로 비춘다** (같은 절,
    p.811).[^ramalho2022] 그 정본이
    [이터레이터 프로토콜과 제너레이터](iterator-protocol-and-generators.md)에 있다.
  - 쓸모의 실물 하나 — 데이터베이스 커서 순회에서 **응답이 크면 커서가 모든 행을 한 배치로
    싣지 않으므로, `async for row in cur:`가 커서가 추가 행을 기다리는 동안 이벤트 루프를
    막지 않는 것이 중요하다** (같은 절, p.811).[^ramalho2022]
- 제너레이터 쪽 — **`__anext__`와 `__aiter__`를 가진 클래스를 써서 비동기 이터레이터를
  구현할 수 있지만 더 단순한 방법이 있다: `async def`로 선언된 함수를 쓰고 몸통에 `yield`를
  쓰는 것. 이것이 제너레이터 함수가 고전 이터레이터 패턴을 단순화하는 것과 평행하다**
  (21장 §"Asynchronous Generator Functions", p.812).[^ramalho2022]
- 네이티브 코루틴과 비동기 제너레이터의 차이 넷 (21장 §"Asynchronous generators versus
  native coroutines", p.818):[^ramalho2022]
  - **둘 다 `async def`로 선언된다.**
  - **비동기 제너레이터는 언제나 몸통에 `yield` 식을 갖는다 — 그것이 그것을 제너레이터로
    만든다. 네이티브 코루틴은 결코 `yield`를 담지 않는다.**
  - **네이티브 코루틴은 `None`이 아닌 값을 돌려줄 수 있다. 비동기 제너레이터는 빈 `return`
    문만 쓸 수 있다.**
  - **네이티브 코루틴은 awaitable이다: `await` 식으로 몰거나 `create_task` 같은 asyncio
    함수에 넘길 수 있다. 비동기 제너레이터는 awaitable이 아니다. 그것들은 `async for`나
    비동기 컴프리헨션으로 몰리는 비동기 이터러블이다.**
- 컨텍스트 매니저를 짓는 데도 쓴다 — **직접 비동기 컨텍스트 매니저를 쓰는 것은 잦은 일이
  아니지만, 써야 한다면 파이썬 3.7에서 `contextlib`에 더해진 `@asynccontextmanager`
  데코레이터를 고려하라. 그것은 `@contextmanager`와 아주 비슷하다** (21장 §"Asynchronous
  generators as context managers", p.817).[^ramalho2022] 가르는 자리도 같다 — **`yield`
  식 이전의 모든 줄이 `__aenter__` 코루틴 메서드가 되고, `yield` 뒤의 줄들이 `__aexit__`
  코루틴 메서드가 된다** (같은 절, pp.817–818).[^ramalho2022]
- 조르기 수단 — **세마포어(semaphore)는 락보다 유연한 동기화 원시다. 세마포어는 설정
  가능한 최댓값 아래에서 여러 코루틴이 붙들 수 있다. 이것이 활성 동시 코루틴 수를 조르는
  데 이상적으로 만든다** (21장 §"Throttling Requests with a Semaphore",
  p.790).[^ramalho2022] 그 앞에 요구가 있다 — **우리가 공부하는 것 같은 네트워크
  클라이언트는 서버를 너무 많은 동시 요청으로 두들기지 않도록 조려져야 한다** (같은 절,
  p.790).[^ramalho2022] 그리고 계보 — **컴퓨터 과학자 Edsger W. Dijkstra가 1960년대 초에
  세마포어를 발명했다. 단순한 발상이지만 워낙 유연해서 락과 배리어 같은 다른 대부분의
  동기화 객체를 세마포어 위에 지을 수 있다** (21장 §"Python's Semaphores",
  p.791).[^ramalho2022]

## 구조적 동시성

- asyncio에 묶이지 않았다 — **파이썬의 async/await 언어 구성물은 특정 이벤트 루프나
  라이브러리에 묶여 있지 않다. 특수 메서드가 제공하는 확장 가능한 API 덕분에, 충분히
  동기가 있는 누구든 네이티브 코루틴과 비동기 제너레이터 등을 몰 자기만의 비동기 런타임
  환경과 프레임워크를 쓸 수 있다** (21장 §"async Beyond asyncio: Curio",
  p.821).[^ramalho2022] 각주가 대비를 붙인다 — **JavaScript와는 대조적이다. 거기서
  async/await는 내장 이벤트 루프와 런타임 환경에 하드와이어돼 있다.**
- Curio가 그 실증이다 — **asyncio가 파이썬 3.4에 나왔고 `await` 대신 `yield from`을 썼기
  때문에, 그 API는 비동기 컨텍스트 매니저·비동기 이터레이터와 async/await 키워드가 가능하게
  한 다른 모든 것을 활용할 수 없었다. 그 결과 Curio는 asyncio에 견주어 더 깔끔한 API와
  더 단순한 구현을 갖는다** (같은 절, p.821).[^ramalho2022]
- 정의 (같은 절, p.823):[^ramalho2022]

> Task groups support *structured concurrency*: a form of concurrent programming that
> constrains all the activity of a group of asynchronous tasks to a single entry and exit
> point. This is analogous to structured programming, which eschewed the GOTO command and
> introduced block statements to limit the entry and exit points of loops and subroutines.

  - 보장되는 것 — **비동기 컨텍스트 매니저로 쓰일 때 `TaskGroup`은 안에서 생성된 모든
    태스크가 완료되거나 취소되고, 어떤 예외든 일어나도록 보장한다 — 감싼 블록을 벗어날
    때** (같은 절, p.823).[^ramalho2022]
  - 그 발상이 이 KB의 [파이썬의 동시성 모델](../concepts/concurrency-models-in-python.md)에 있는
    "복잡성을 다루려면 제약이 필요하다"의 직접 연장이다. GOTO를 없앤 것과 같은 종류의
    제약이라고 저자가 명시한다.
- 전망 — **구조적 동시성은 아마 다가올 파이썬 릴리스에서 asyncio에 채택될 것이다. 강한
  신호가 파이썬 3.11에 승인된 PEP 654에 나타난다** (같은 절, p.823).[^ramalho2022]

## "I/O 바운드 시스템"은 없다

- 매력의 근거부터 — Node.js 발명자 Ryan Dahl의 지연 시간 표가 인용되고, 저자가 그것을
  사람의 척도로 환산한다: **L1 캐시 읽기 하나가 3초 걸린다면 네트워크 읽기는 7.6년이
  걸릴 것이다** (21장 §"Running Circles Around Blocking Calls",
  pp.825–826).[^ramalho2022] 그래서 **규율 있는 비동기 프로그래밍 접근이 고성능 서버로
  이어질 수 있다. 도전은 그 규율을 달성하는 것이다** (같은 절, p.826).[^ramalho2022]
- 그리고 판정 (21장 §"The Myth of I/O-Bound Systems", p.826):[^ramalho2022]

> A commonly repeated meme is that asynchronous programming is good for "I/O bound
> systems." I learned the hard way that there are no "I/O-bound systems." You may have
> I/O-bound *functions*. Perhaps the vast majority of the functions in your system are
> I/O bound; i.e., they spend more time waiting for I/O than crunching data. (…) But
> inevitably, any nontrivial system will have some parts that are CPU bound. Even trivial
> systems reveal that, under stress.

  - 귀결 — **어떤 사소하지 않은 시스템도 CPU 바운드 함수를 가질 것이므로, 그것들을 다루는
    것이 비동기 프로그래밍 성공의 열쇠다** (같은 절, p.826).[^ramalho2022]
- 그 실물이 두 사례로 붙어 있다 (21장 §"Soapbox", pp.829–831):[^ramalho2022]
  - **uvloop 벤치마크** — 단순 에코 서버조차 HTTP 헤더 파싱이 CPU 바운드였고, 파이썬으로
    쓰인 파서가 이벤트 루프를 막았다. **CPU 바운드 코드를 최적화하지 않았다면 더 빠른
    이벤트 루프의 성능 이득은 사라졌을 것이다.**
  - **천 번의 베임으로 인한 죽음** — 수만 줄짜리 Twisted 시스템에서 **기능을 더할 때마다
    CPU 바운드 코드가 늘어 이벤트 루프를 느리게 만들었다. 단일 병목이 없었다: 문제가
    몇 달의 개발 동안 더해진 수많은 작은 함수들에 흩어져 있었다.** 고치려면 아키텍처
    재고와 대규모 재작성이 필요했고 **이해관계자들이 그 추가 투자를 감당할 준비가 되어
    있지 않아 프로젝트는 곧 취소됐다.**
- 처방이 넷이다 (21장 §"Avoiding CPU-Bound Traps", p.827):[^ramalho2022]
  - **작업을 파이썬 프로세스 풀에 위임한다.**
  - **작업을 외부 작업 큐에 위임한다.**
  - **관련 코드를 Cython·C·러스트, 또는 기계어로 컴파일되고 Python/C API와 접속하는 다른
    언어로 다시 쓴다 — 가급적 GIL을 놓으면서.**
  - **성능 손해를 감당할 수 있다고 결정하고 아무것도 하지 않는다 — 다만 나중에 되돌리기
    쉽도록 그 결정을 기록한다.**
- 시점에 대한 조문 둘이 붙는다 (같은 절, pp.826–827):[^ramalho2022]
  - **파이썬을 규모 있게 쓴다면, 성능 회귀가 나타나자마자 검출하도록 특별히 설계된 자동
    테스트가 있어야 한다. (…) 느려짐이 개발팀을 괴롭히기 시작할 때까지 기다린다면 너무
    늦다. 수정에 아마 대규모 개조가 필요할 것이다.**
  - **외부 작업 큐는 프로젝트 시작에 가능한 한 빨리 선택되고 통합되어야, 필요할 때
    팀의 누구도 그것을 쓰기를 주저하지 않는다.**
  - 그리고 마지막 선택지의 지위 — **마지막 선택지 — 아무것도 하지 않는 것 — 는 기술
    부채의 범주에 든다** (같은 절, p.827).[^ramalho2022]

## 이어지는 페이지

- [파이썬의 동시성 모델](../concepts/concurrency-models-in-python.md) — 같은 부의 개념 층. 여기 쓰인
  실행 단위·GIL·선점 대 협력의 어휘가 그쪽에 있다
- [yield from과 고전 코루틴](yield-from-and-classic-coroutines.md) — `await`의 직계
  선조와 그 기제
- [이터레이터 프로토콜과 제너레이터](iterator-protocol-and-generators.md) — `async for`가
  비추는 그 이터러블·이터레이터 구분의 정본
- [컨텍스트 매니저 프로토콜](context-manager-protocol.md) — `async with`가 비추는
  `__enter__`/`__exit__`의 정본
- [파이썬의 제어 흐름 기제](../synthesis/python-control-flow-mechanics.md) — 이 축의 허브

[^ramalho2022]: Ramalho 2022, 20장 "Concurrent Executors" 도입(p.743) · §"Downloading with
    concurrent.futures"(pp.749–750) · §"Where Are the Futures?"(pp.751–753) · §"Launching
    Processes with concurrent.futures"(pp.754–755) · §"Multicore Prime Checker
    Redux"(pp.755–758) · §"Experimenting with Executor.map"(p.761) · §"Using
    futures.as_completed"(p.772) · §"Soapbox — Thread Avoidance"(pp.773–774), 그리고
    21장 "Asynchronous Programming" 도입(p.775) · §"A Few Definitions"(p.777) · §"An asyncio
    Example: Probing Domains"(pp.778–780) · §"Guido's Trick to Read Asynchronous
    Code"(pp.780–781) · §"New Concept: Awaitable"(pp.781–782) · §"The Secret of Native
    Coroutines: Humble Generators"(pp.784–785) · §"The All-or-Nothing Problem"(pp.785–786) ·
    §"Asynchronous Context Managers"(pp.786–787) · §"Enhancing the asyncio
    Downloader"(p.790) · §"Throttling Requests with a Semaphore"(pp.790–791) · §"Python's
    Semaphores"(p.791) · §"Asynchronous Iteration and Asynchronous Iterables"(p.811) ·
    §"Asynchronous Generator Functions"(pp.812–818) · §"async Beyond asyncio:
    Curio"(pp.821–823) · §"How Async Works and How It Doesn't"(pp.825–827) · §"Chapter
    Summary"(p.827) · §"Soapbox"(pp.829–831). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷
    PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과 판본 판정은
    `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다. 그림 20-1(진행 표시줄
    스크린샷)·21-1(이벤트 루프와 코루틴의 통로)은 이미지로 조판돼 있어 본문 서술로만
    옮겼다. 표 21-1(장치별 지연 시간)의 수치는 본문 산문으로 옮겼다. 코드 펜스는 예제
    21-1 원문이고, 원문 코드 목록에 삽입된 조판용 번호 표지만 제거했다. HTTP 클라이언트
    예제(flags·flags2·flags3 계열)와 서버 예제(mojifinder 계열)는 특정 라이브러리에 묶인
    코드라 옮기지 않았다. PDF 818·862쪽은 추출본이 훼손·OCR 필요 판정을 받아 그 쪽은
    인용하지 않았다.

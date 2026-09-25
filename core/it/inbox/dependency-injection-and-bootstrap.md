---
type: concept
title: 의존성 주입과 부트스트랩
description: 명시적 의존을 실제로 누가 어떻게 꽂아 넣는가 — 파이썬 세계에서 DI가 의심받는다는 인정과 그럼에도 쓰게 되는 통증, 클로저·partial·클래스라는 세 가지 수동 주입 방식과 늦은 바인딩이라는 차이, 합성 루트를 부트스트랩 스크립트라 부르는 판단과 그것이 맡는 네 가지 일, 시그니처를 검사해 이름으로 의존을 맞추는 구현과 그것을 과잉 설계라 부른 공저자의 반론 및 더 단순한 판본, 테스트에서 기본값을 덮어써 가짜를 꽂는 방법, 단순한 의존을 "제대로 된" 어댑터로 승격시키는 여섯 단계, 다른 소스가 포트를 어댑터로 해소하는 수단으로 주입과 부트스트랩을 대등하게 병렬하는 자리와 그 배치가 이 페이지의 배치와 어긋나 보이는 이유, 그리고 포트와 어댑터의 원저자 콕번이 의존성 주입과 의존성 조회를 한 이름 Configurable Receiver로 아우르고 그것이 컴파일 시점 원칙(의존성 역전)과 실행 시점 두 수단을 어떻게 가르는가
generated: { by: "claude-opus-5", at: "2026-08-17T23:30:00Z" }
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
status: draft
---

# 의존성 주입과 부트스트랩

- [파이썬에서 DI가 의심받는다는 인정](#파이썬에서-di가-의심받는다는-인정)
- [수동 주입 세 방식](#수동-주입-세-방식)
- [합성 루트를 부트스트랩 스크립트라 부른다](#합성-루트를-부트스트랩-스크립트라-부른다)
- [시그니처 검사와 그에 대한 반론](#시그니처-검사와-그에-대한-반론)
- [테스트에서 기본값을 덮어쓰기](#테스트에서-기본값을-덮어쓰기)
- [어댑터를 "제대로" 만드는 여섯 단계](#어댑터를-제대로-만드는-여섯-단계)
- [언제 DI 프레임워크가 필요한가](#언제-di-프레임워크가-필요한가)
- [프레임워크를 얼마나 쓸 것인가 — 다른 소스의 같은 판정](#프레임워크를-얼마나-쓸-것인가--다른-소스의-같은-판정)
- [포트를 어댑터로 해소하는 두 수단](#포트를-어댑터로-해소하는-두-수단)
- [원전이 이름 붙인 패턴 — Configurable Receiver](#원전이-이름-붙인-패턴--configurable-receiver)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **의존을 전부 명시적으로 선언하기로 했다면, 그것을 실제로 조립하는 일은 누가
어디서 하는가.**

## 파이썬에서 DI가 의심받는다는 인정

- 장이 방어적으로 연다 — **의존성 주입(DI)은 파이썬 세계에서 의심의 눈초리를 받는다.
  그리고 우리는 이 책의 예제 코드에서 지금까지 그것 없이도 잘 지내 왔다!**
  (13장 도입).[^percival2020]
- 그래서 이 장의 방식이 통증에서 출발한다 — **이 장에서 우리는 DI를 고려하게 만드는 우리
  코드의 통증 지점 몇 개를 탐색하고, 그것을 하는 방법에 대한 선택지 몇 개를 제시하되
  어느 것이 가장 파이써닉하다고 생각하는지는 당신이 고르도록 남겨 둘 것이다**
  (13장 도입).[^percival2020]
- 새 구성 요소의 이름이 예고된다 — **우리는 또 `bootstrap.py`라는 새 구성 요소를 우리
  아키텍처에 더할 것이다; 그것이 의존성 주입과, 우리가 흔히 필요로 하는 다른 초기화 작업을
  담당할 것이다. 우리는 이런 것이 왜 OO 언어에서 합성 루트(composition root)라 불리는지,
  그리고 왜 우리 목적에는 부트스트랩 스크립트(bootstrap script)로 충분한지 설명할 것이다**
  (13장 도입).[^percival2020]
- 이 장이 3장에 얹혀 있다고 명시된다 — **아직 읽지 않았다면 이 장을 계속하기 전에 3장을,
  특히 함수형 대 객체 지향 의존 관리 논의를 읽을 값어치가 있다**
  (13장 도입).[^percival2020] 그쪽은 [추상화 고르기](../concepts/choosing-abstractions.md)와
  [가짜와 목](fakes-versus-mocks.md)에 있다.
- 무엇이 문제였는지가 그림으로 규정된다 — 부트스트래퍼가 없으면
  **진입점들이 초기화와 우리 주 의존인 UoW를 여기저기 넘기는 일을 많이 한다**
  (13장 도입).[^percival2020] 그리고 SRP 위반이 지목된다 — **그것은 Flask·Redis·우리
  테스트에 대한 추가(중복) 잡동사니다. 게다가 옳은 핸들러에 의존을 넘기는 모든 책임을
  메시지 버스에 지우는 것은 SRP 위반처럼 느껴진다**
  (13장 §"Aren't Explicit Dependencies Totally Weird and Java-y?").[^percival2020]

## 수동 주입 세 방식

- **클로저와 partial** — **의존을 가진 함수를 그 의존이 이미 주입된 채로 나중에 호출될
  준비가 된 함수로 바꾸는 한 방법은 클로저나 부분 함수(partial function)를 써서 그 함수를
  자기 의존과 합성하는 것이다** (13장 §"Preparing Handlers: Manual DI with Closures and
  Partials").[^percival2020]
- 셋의 차이가 명시된다. 람다, 이름 붙인 함수, `functools.partial` 셋 다 쓸 수 있고 —
  **이름 붙인 함수 쪽이 더 나은 스택 트레이스를 준다**
  (13장 §"Preparing Handlers…").[^percival2020] 그리고 결정적 차이 하나 —
  **클로저(람다나 이름 붙인 함수)와 `functools.partial`의 차이는 전자가 변수의 늦은
  바인딩(late binding)을 쓴다는 것인데, 의존 중 어느 것이라도 가변이면 혼란의 원천이 될 수
  있다** (13장 §"Preparing Handlers…").[^percival2020]
- **클래스 방식**이 대안이다 — **클로저와 부분 함수는 함수형 프로그래밍을 좀 해 본 사람에게
  익숙하게 느껴질 것이다. 여기 다른 사람들에게 매력적일 수 있는 클래스를 쓰는 대안이 있다.
  다만 우리 핸들러 함수를 전부 클래스로 다시 써야 한다**
  (13장 §"An Alternative Using Classes").[^percival2020] 클래스는
  **호출 가능한 함수를 생산하도록 설계됐으므로 `__call__` 메서드를 갖고**,
  **`__init__`으로 필요한 의존을 선언한다**
  (13장 §"An Alternative Using Classes").[^percival2020]
- 판정이 없다 — **당신과 당신 팀이 더 편안하게 느끼는 쪽을 쓰라**
  (13장 §"An Alternative Using Classes").[^percival2020]

## 합성 루트를 부트스트랩 스크립트라 부른다

- 이름의 계보 — **대신 우리는 합성 루트(Composition Root)라 불리는 패턴(당신과 나에게는
  부트스트랩 스크립트)에 손을 뻗어 "수동 DI"(프레임워크 없는 의존성 주입)를 조금 할 것이다**
  (13장 §"Aren't Explicit Dependencies Totally Weird and Java-y?").[^percival2020]
  - 파이썬에서 이 개념이 낯선 이유가 각주에 있다 — **파이썬이 "순수" OO 언어가 아니기
    때문에, 파이썬 개발자들이 객체 집합을 작동하는 애플리케이션으로 합성해야 한다는 개념에
    반드시 익숙한 것은 아니다. 우리는 그냥 진입점을 고르고 코드를 위에서 아래로 돌린다**
    (13장 각주 1).[^percival2020]
  - 다른 이름도 인용된다 — **Mark Seemann은 이것을 순수 DI(Pure DI), 때로는 바닐라
    DI(Vanilla DI)라고 부른다** (13장 각주 2).[^percival2020]
- **부트스트랩이 맡는 일 넷** (13장 §"A Bootstrap Script"):[^percival2020]
  - **기본 의존을 선언하되 그것을 덮어쓸 수 있게 한다.**
  - **앱을 시작하는 데 필요한 "init" 작업을 한다.**
  - **모든 의존을 우리 핸들러에 주입한다.**
  - **앱의 핵심 객체인 메시지 버스를 우리에게 돌려준다.**
- 기본값을 인수 기본값으로 두는 것에 단서가 붙는다 — **우리는 인수 기본값을 써서 정상/
  프로덕션 기본값이 무엇인지 정의할 수 있다. 그것을 한자리에 두는 것이 좋지만, 때로는
  의존이 생성 시점에 부수 효과를 가질 수 있고 그런 경우에는 대신 `None`으로 기본값을 두는
  편을 선호할 수 있다** (13장 §"A Bootstrap Script").[^percival2020]
- 초기화 작업의 예도 규정된다 — **`orm.start_mappers()`가 앱 시작 시 한 번 해야 하는
  초기화 작업의 우리 예다. 우리는 로깅 모듈 설정 같은 것들도 본다**
  (13장 §"A Bootstrap Script").[^percival2020]
- **메시지 버스가 모듈에서 클래스로 바뀐다** — **우리 메시지 버스는 더 이상 정적이지 않을
  것이다; 이미 주입된 핸들러를 받아야 한다. 그래서 우리는 그것을 모듈에서 설정 가능한
  클래스로 바꾼다** (13장 §"Message Bus Is Given Handlers at
  Runtime").[^percival2020] 그리고 핸들러의 인수가 하나로 준다 — **핸들러에 UoW를 넘기는
  대신 우리는 핸들러가 이미 모든 의존을 갖고 있다고 기대하므로 필요한 것은 인수 하나,
  특정 이벤트나 명령뿐이다** (13장 §"Message Bus Is Given Handlers at
  Runtime").[^percival2020]
  - 스레드 안전성 경고가 붙는다 — **이런 식으로 `self.queue`를 쓰는 것은 스레드 안전하지
    않은데, 우리가 쓴 대로라면 버스 인스턴스가 Flask 앱 컨텍스트에서 전역이므로 스레드를
    쓴다면 문제가 될 수 있다. 그저 조심할 것 하나다**
    (13장 §"Message Bus Is Given Handlers at Runtime").[^percival2020]
- 진입점이 단순해진다 — **애플리케이션의 진입점에서 우리는 이제 UoW와 나머지를 설정하는
  대신 그냥 `bootstrap.bootstrap()`을 부르고 바로 쓸 수 있는 메시지 버스를 얻는다**
  (13장 §"Using Bootstrap in Our Entrypoints").[^percival2020]
  - 남은 전역성에 단서가 붙는다 — **그래도 그것은 여전히 `flask_app` 모듈 범위의
    전역이다. 도커를 쓰는 대신 Flask 테스트 클라이언트로 프로세스 안에서 Flask 앱을
    테스트하고 싶어진다면 문제가 될 수 있다. Flask 앱 팩토리를 조사해 볼 값어치가 있다**
    (13장 각주 3).[^percival2020]

## 시그니처 검사와 그에 대한 반론

- 저자 하나의 구현은 함수 시그니처를 들여다본다 — **우리 명령/이벤트 핸들러의 인수를
  검사한다** / **그것을 이름으로 우리 의존과 맞춘다** / **partial을 생산하도록 그것을
  kwargs로 주입한다** (13장 §"A Bootstrap Script").[^percival2020]

  ```python
  def inject_dependencies(handler, dependencies):
      params = inspect.signature(handler).parameters
      deps = {
          name: dependency
          for name, dependency in dependencies.items()
          if name in params
      }
      return lambda message: handler(message, **deps)
  ```

- **그리고 공저자가 그것을 과잉 설계라 부른 일이 그대로 인쇄돼 있다** — **Harry가 "수동"
  의존성 주입을 하는 방법의 첫 시도로 `inject_dependencies()` 코드를 썼는데, 그것을 본
  Bob은 그를 과잉 설계하고 자기만의 DI 프레임워크를 쓰고 있다고 비난했다**
  (13장 §"Even-More-Manual DI with Less Magic" 곁글).[^percival2020]
- 더 단순한 판본은 람다를 손으로 나열하는 것이다 — 이벤트 타입마다 핸들러 람다를 적는
  딕셔너리다. **Harry는 그렇게 많은 줄의 코드를 적고 그렇게 많은 함수 인수를 손으로
  찾아보는 것을 상상조차 할 수 없었다고 말한다. 그러나 이것은 완벽히 실행 가능한 해법인데,
  더하는 핸들러당 코드 한 줄 정도일 뿐이라 핸들러가 수십 개여도 엄청난 유지보수 부담은
  아니기 때문이다** (13장 §"Even-More-Manual DI with Less Magic" 곁글).[^percival2020]
- 둘 다 되는 조건이 명시된다 — **우리 앱은 우리가 언제나 한 자리, 핸들러 함수에서만
  의존성 주입을 하고 싶도록 구조화돼 있으므로, 이 초수동 해법과 Harry의 `inspect()` 기반
  해법 둘 다 잘 작동할 것이다**
  (13장 §"Even-More-Manual DI with Less Magic" 곁글).[^percival2020]
  - **저자 둘의 판단이 갈리고 둘 다 인쇄된 자리가 이 책에 여럿 있다.**
    [값 객체와 엔티티](value-objects-and-entities.md)의 `NewType` 논쟁이 다른 예다.
    이 소스가 규범이 아니라 두 실무자의 판단이라는 것을 이 자리들이 규정한다.

## 테스트에서 기본값을 덮어쓰기

- 방법이 하나다 — **테스트에서 우리는 덮어쓴 기본값으로 `bootstrap.bootstrap()`을 써서
  맞춤 메시지 버스를 얻을 수 있다** (13장 §"Initializing DI in Our
  Tests").[^percival2020]
- 통합 테스트와 단위 테스트에서 무엇을 켜고 끄는지가 갈린다
  (13장 §"Initializing DI in Our Tests"):[^percival2020]
  - 통합 테스트 — **우리는 여전히 ORM을 시작하고 싶다** / **메모리 데이터베이스이긴 해도
    실제 UoW를 쓸 것이기 때문이다** / **그러나 이메일을 보내거나 발행할 필요는 없으므로
    그것들을 무연산(noop)으로 만든다.**
  - 단위 테스트 — **ORM을 시작할 필요가 없다** / **가짜 UoW가 그것을 쓰지 않기 때문이다** /
    **우리는 이메일과 Redis 어댑터도 가짜로 만들고 싶다.**
- 얻는 것 — **그래서 그것이 약간의 중복을 없애고, 우리는 많은 설정과 합리적인 기본값을 한
  자리로 옮겼다** (13장 §"Initializing DI in Our Tests").[^percival2020]

## 어댑터를 "제대로" 만드는 여섯 단계

- 이 책의 의존이 두 종류라고 정리된다 — **UoW는 추상 기반 클래스를 갖는다. 이것은 외부
  의존을 선언하고 관리하는 무거운 선택지다. 우리는 의존이 상대적으로 복잡한 경우에 이것을
  쓸 것이다** / **우리 이메일 발송자와 pub/sub 발행자는 함수로 정의된다. 이것은 단순한
  의존에는 그냥 잘 작동한다** (13장 §"Building an Adapter 'Properly': A Worked
  Example").[^percival2020]
- 실무에서 주입하는 것들의 목록도 있다 — **S3 파일 시스템 클라이언트, 키/값 저장소
  클라이언트, `requests` 세션 객체**. 그리고 **이 대부분은 함수 하나로 담을 수 없는 더
  복잡한 API를 가질 것이다: read와 write, GET과 POST 같은 것들**
  (13장 §"Building an Adapter 'Properly'…").[^percival2020]
- **곁글 요약이 이 절차의 정본이다** (13장 §"DI and Bootstrap Recap"
  곁글):[^percival2020]
  - **ABC를 써서 당신의 API를 정의하라.**
  - **실제 것을 구현하라.**
  - **가짜를 만들고 단위/서비스 레이어/핸들러 테스트에 쓰라.**
  - **당신 도커 환경에 넣을 수 있는 덜 가짜인 판본을 찾아라.**
  - **그 덜 가짜인 "실제" 것을 테스트하라.**
  - **이익을 보라!**
- 넷째 단계의 실물이 MailHog다 — **우리는 도커 개발 환경에서 실제에 가까운 이메일 서버로
  MailHog를 썼다** (13장 §"Figure Out How to Integration Test the Real
  Thing").[^percival2020] 통합 테스트는 그 서버의 API에서 메일을 꺼내 발신자·수신자·본문을
  단언한다. 그리고 저자들의 소감이 그대로 있다 — **모든 예상을 뒤엎고 이것은 거의 첫
  시도에서 실제로 작동했다** (13장 §"Figure Out How to Integration Test the Real
  Thing").[^percival2020]
  - **이 절차가 [가짜와 목](fakes-versus-mocks.md)의 입장을 실행 가능한 순서로 바꾼
    것이다.** 가짜는 단위 테스트용이고, 실제 것은 통합 테스트에서 "덜 가짜인" 대역을 상대로
    검증한다. 두 층 사이에 목이 들어갈 자리가 없다.

## 언제 DI 프레임워크가 필요한가

- 경계가 규정된다 — **DI 프레임워크는 여러 수준에서 DI를 해야 하는 자신을 발견한다면 —
  예컨대 전부 DI가 필요한 구성 요소들의 연쇄 의존을 갖고 있다면 — 쓸모 있을 수 있다**
  (13장 §"Wrap-Up").[^percival2020] 같은 판정이 곁글에도 있다 — **더 많은 것에 대해, 그리고
  다른 시점에 DI를 하고 싶어지거나, 의존 연쇄(당신 의존이 자기 자신의 의존을 갖는 등)에
  빠진다면 "진짜" DI 프레임워크에서 얻을 것이 있을 수 있다**
  (13장 §"Even-More-Manual DI with Less Magic" 곁글).[^percival2020]
- 실제로 쓰는 것들이 열거된다 — **MADE에서 우리는 몇 군데에서 Inject를 썼고 괜찮다.
  다만 Pylint를 불행하게 만든다. Bob 자신이 쓴 Punq나 DRY-Python 팀의 dependencies도
  살펴볼 수 있다** (13장 §"Even-More-Manual DI with Less Magic" 곁글).[^percival2020]
- 장의 맺음이 이 페이지의 요지다 — **어댑터가 하나보다 많아지면, 어떤 종류의 의존성 주입을
  하지 않는 한 의존을 손으로 여기저기 넘기는 데서 많은 고통을 느끼기 시작할 것이다.
  의존성 주입을 설정하는 것은 앱을 시작할 때 단 한 번 해야 하는 전형적인 설정/초기화 활동
  중 하나일 뿐이다. 이 전부를 부트스트랩 스크립트로 묶는 것이 흔히 좋은 생각이다**
  (13장 §"Wrap-Up").[^percival2020]

## 프레임워크를 얼마나 쓸 것인가 — 다른 소스의 같은 판정

위 [언제 DI 프레임워크가 필요한가](#언제-di-프레임워크가-필요한가)의 물음을 도메인 주도 설계의
원전이 프레임워크 일반에 대해 던지고 같은 방향의 답을 낸다.

- 그쪽이 다루는 것은 **아키텍처 프레임워크**다 — 서비스로 불러 쓰는 기반 구조와 달리 **다른
  층이 아주 특정한 방식으로 구현되기를 요구하는** 것(프레임워크 클래스의 하위 클래스가 되거나
  정해진 메서드 서명을 갖는 것)이라 **다른 층의 설계에 훨씬 큰 영향을 미친다** (4장,
  pp.74·73).[^evans2003]
- 그쪽의 조항은 **선택적 적용**이다 — 프레임워크를 적용할 때 팀은 도메인 모델을 표현하는 구현을
  짓는다는 목표에 집중해야 하고, **프레임워크의 기능을 다 쓰지 않는 것을 뜻하더라도 그 목적에
  쓸 방법을 찾아야 한다** (4장, p.74).[^evans2003]
- **지키려는 것 둘의 순위가 이 절의 값이다.** 가장 값진 기능만 신중히 적용하면 구현과
  프레임워크의 결합이 줄어 이후 설계 결정에서 유연해지는데, 그쪽 저자는 **그보다 더 중요한 것**
  으로 다른 것을 든다 — 그 최소주의가 **업무 객체를 읽을 수 있고 표현력 있게 유지한다**는 것이다
  (4장, pp.74–75).[^evans2003]
  - **이 페이지의 소스와 강조점이 다르다.** 이쪽은 **손으로 하는 주입을 기본값**으로 두고
    프레임워크는 의존 연쇄가 깊어질 때 부른다. 그쪽은 **어떤 형태의 프레임워크는 보통
    필요하다**고 인정하되 기능 선택을 요구한다.
  - #hypothesis 그럼에도 **잣대는 같다** — 두 소스 모두 판정 기준을 "도메인·업무 코드가
    읽히는가"에 둔다. 저자들이 서로를 대조한 적이 없어 가설로 적는다.
- 그쪽의 전문은 [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md)에 있다.

## 포트를 어댑터로 해소하는 두 수단

이 페이지의 두 낱말 — 주입과 부트스트랩 — 이 아키텍처 패턴의 조항 안에 나란히 등장하는 자리가
있다.

- [khononov2021](../sources/khononov2021.md)이 포트와 어댑터 아키텍처를 규정하면서 적는다
  (8장, p.128):[^khononov2021]

> The abstract ports are resolved into concrete adapters in the infrastructure layer, either through
> dependency injection or by bootstrapping.

- **이 판본은 둘을 대등한 선택지로 병렬한다.** 이 페이지의 소스는 다르게 배치한다 — 위
  [합성 루트를 부트스트랩 스크립트라 부른다](#합성-루트를-부트스트랩-스크립트라-부른다)가
  부트스트랩 스크립트를 **주입이 일어나는 자리의 이름**으로 다루므로, 그쪽에서 둘은 배타적
  선택지가 아니라 한 기제와 그 기제가 사는 자리다.
  - **모순 쌍으로 세우지 않았다.** 이 판본은 한 문장으로 지나가는 자리이고 둘의 관계를
    규정하지 않는다. #hypothesis 이 판본의 "부트스트랩"이 가리키는 것은 애플리케이션 시작
    시점에 구현을 고정하는 정적 배선(컴파일 타임 또는 시작 시점의 구성)이고, 그쪽 소스의
    부트스트랩 스크립트가 바로 그것이라 실제로는 같은 것을 가리킨다고 읽는다. 저자가 그것을
    밝힌 대목은 없다.
- 그 아키텍처 전체는
  [의존성 역전 원칙 §포트와 어댑터의 규정](dependency-inversion-principle.md)에 있다.

## 원전이 이름 붙인 패턴 — Configurable Receiver

위 [포트를 어댑터로 해소하는 두 수단](#포트를-어댑터로-해소하는-두-수단)이 든 "주입이나 부트스트랩"이라는
두 갈래에, 포트와 어댑터의 원저자 콕번이 정확한 이름을 붙였다. 그는 이 둘을 아우르는 패턴을 2023년에
**Configurable Receiver**로 규정하고 그것을 책 6장 6.5절에 원문으로 재수록했다.

- 패턴의 규정은 한 줄이다 — **실행 시점에 수신자(receiver)를 설정하거나 바꾼다.** 그리고 이 패턴이
  **의존성 주입과 의존성 조회(dependency lookup)를 함께 포섭한다**고 못 박는다
  (6장 §"6.5. Configurable Receiver").[^cockburn2024]
- 발신자가 수신자를 실행 시점에 고르려면 Configurator가 있어야 하고, 그 Configurator가 수신자를
  발신자에게 건네는 방식이 둘이다 (6장 §"6.5. Configurable Receiver"):[^cockburn2024]
  - **Configurator가 발신자에게 어느 수신자를 쓸지 알려 준다 — 이것이 의존성 주입이다.**
  - **발신자가 Configurator에게 어느 수신자를 쓸지 물어본다 — 이것이 의존성 조회이고, 그 Configurator를
    서비스 로케이터(service locator)나 브로커(broker)라 부른다.**
  - 그래서 콕번은 **Configurator의 첫 설계 결정이 의존성 주입과 의존성 조회 사이의 선택**이라고
    적는다. 위 khononov 인용이 "주입이나 부트스트랩"으로 지나간 자리를, 원전은 "주입이냐 조회냐"라는
    더 정확한 갈림으로 세운다 — 부트스트랩은 그 선택을 어디서 수행하느냐(시작 시점의 배선)이지 이 갈림의
    한 항이 아니다.
- 콕번은 이 패턴이 흔히 뭉뚱그려지는 세 가지와 어떻게 구별되는지도 정리한다 — **Configurable Receiver는
  의존성 역전 원칙·의존성 주입·의존성 조회 셋을 모두 쓰되, 제어의 역전(Inversion of Control)은 그것들과
  무관한데도 자주 뒤섞인다** (6장 §"6.5. Configurable Receiver", §7).[^cockburn2024]
  - **의존성 역전 원칙은 컴파일 시점 주제**다 — 발신자가 요구 인터페이스를 소유하고, 수신자가 발신자에
    의존하며, 발신자는 어느 수신자에도 의존하지 않게 하는 것이다.
    [의존성 역전 원칙](dependency-inversion-principle.md)의 "포트와 어댑터가 파이썬에서 무엇인가"
    절이 담은 것이 그 컴파일 시점 구조다.
  - **의존성 주입과 의존성 조회는 실행 시점 주제**다 — 컴파일 시점에 뒤집힌 그 구조 위에서, 실제
    수신자를 실행 중에 어떻게 발신자에게 건네느냐의 두 방식이다.
  - 콕번이 2023년 5월에 밥 마틴(Bob Martin)에게 이 관계를 물었고, 마틴은 **의존성 역전 원칙은 발신자가
    요구 인터페이스를 선언해 최소한의 재컴파일로 다른 수신자를 쓸 수 있게 하는 것이며, 그 원칙은 요구
    인터페이스를 서술할 뿐 Configurator는 언급하지 않는다**고 답했다고 적는다
    (6장 §"6.5. Configurable Receiver", §7.1).[^cockburn2024] 즉 Configurable Receiver가 그 원칙에
    Configurator를 더한다.
- 포트와 어댑터에서 이 패턴이 서는 자리는 [포트와 어댑터 규정](ports-and-adapters-defined.md)의 다섯째
  요소 Configurator이고, 그 일반형은 [Component + Strategy 패턴](component-plus-strategy-pattern.md)이
  숨은 넷째 객체로 같은 Configurator를 든다. 이 KB에 들인 콕번의 세금 계산기 코드가 브로커로 의존성
  조회를 예시하는 실물은 [코드로 본 포트와 어댑터](ports-and-adapters-in-code.md)에 있다.

## 이어지는 페이지

- [층을 잇는 법과 아키텍처 프레임워크](relating-layers-and-frameworks.md) — 프레임워크를 얼마나
  쓸 것인가를 다른 소스가 판정하는 자리
- [의존성 역전 원칙](dependency-inversion-principle.md) — 명시적 의존이 구현하는 원리이자
  포트와 어댑터 아키텍처가 이 둘을 부르는 자리
- [가짜와 목](fakes-versus-mocks.md) — 왜 몽키패치가 아니라 주입인가
- [추상화 고르기](../concepts/choosing-abstractions.md) — 이 장이 전제로 삼는 3장
- [작업 단위 패턴](unit-of-work-pattern.md) — 이 장에서 주입되는 주된 의존
- [이벤트 주도 애플리케이션 구조](event-driven-application-structure.md) — 주입 대상이
  되는 핸들러들이 사는 곳
- [외부 설정](external-configuration.md) — 기본값을 한자리에 모으는 같은 판단의 다른 소스
- [포트와 어댑터 규정](ports-and-adapters-defined.md) — 이 주입·조회가 채우는 다섯째 요소
  Configurator의 규정
- [Component + Strategy 패턴](component-plus-strategy-pattern.md) — 같은 Configurator를 숨은 넷째
  객체로 드는 일반형
- [코드로 본 포트와 어댑터](ports-and-adapters-in-code.md) — 브로커로 의존성 조회를 예시하는 실물
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^percival2020]: Percival & Gregory 2020, 13장 "Dependency Injection (and Bootstrapping)"
    전체(곁글 "Even-More-Manual DI with Less Magic"·"Exercise for the Reader 1"·
    "Exercise for the Reader 2"·"DI and Bootstrap Recap" 포함). **이 소스의 locator는 장
    단위다** — 검증 절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이
    정본이다. Figure 13-1~13-3(부트스트랩 도입 전후)은 이미지라 산문 서술로만 옮겼다.
    코드 펜스는 대표 하나(시그니처 검사 기반 주입)만 두었고, 원문에서 조판용 번호 표지
    이미지를 제거했다.

[^evans2003]: Evans 2003, 4장 "Isolating the Domain" §Relating the Layers(p.73) ·
    §Architectural Frameworks(pp.74–75). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 이 소스에서 온
    코드 펜스는 이 페이지에 없다.

[^khononov2021]: Khononov 2021, 8장 "Architectural Patterns" §"Ports & Adapters" 중
    §"Integration of Infrastructural Components"(p.128). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 대조했다. 같은 절의 C# 목록
    (`IMessaging` 포트와 `SQSBus` 어댑터)은
    [의존성 역전 원칙](dependency-inversion-principle.md)이 대표 펜스를 갖는다.

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 6장 §"6.5. The article: "Configurable Receiver""
    (2023년 아티클 HaT Technical Report 2023.01의 원문 재수록) — §"1. Motivation and informal
    structure" · §"3. Implementing the Pattern"(The configurator) · §7 "Discussion of Dependency
    Inversion, Injection, Lookup"(§7.1 밥 마틴의 2023년 5월 논평 포함). 아티클의 Ruby·Java 코드
    샘플과 Spring 코드는 산문으로만 옮기고 펜스는 쓰지 않았다(코드 정본은 3장). 그림 6.23~6.27의
    내용은 본문 서술이 담으므로 이미지를 열지 않았다. EPUB(Calibre 변환본), 쪽 앵커 없음 —
    locator는 장·절 번호.

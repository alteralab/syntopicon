---
type: concept
title: 포트와 어댑터 규정
description: 헥사고날(포트와 어댑터) 아키텍처를 그 원저자 콕번이 직접 규정한 원전 — 패턴이 요구하는 것("UI도 DB도 없이 돌아가게 만들라"와 "외부 기술을 이름으로 부르지 말고 언제나 인수로 받으라")과 약한 준수·강한 준수의 가름, 패턴의 네 요소(앱·포트·액터·어댑터)와 패턴 밖이지만 반드시 필요한 다섯째 요소 Configurator, 앱이 정의하는 제공 인터페이스(API)와 요구 인터페이스(SPI)의 어휘와 요구 인터페이스가 이 패턴의 힘이라는 규정, 대칭인 패턴 안에 있는 구현상의 비대칭(누가 누구를 아는가)이 구동/피구동 액터를 가르는 근거, 포트가 의도별 대화라는 규정과 "For doing" 이름 짓기, 그리고 패턴이 필수로 요구하는 것·선택인 것·패턴 밖인 것의 구분과 이 패턴이 내부 구조에 대해 아무 말도 하지 않아 클린·양파와 갈린다는 갈고리
generated: { by: "claude-opus-5", at: "2026-09-25T00:00:00Z" }
status: draft
sources:
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
---

# 포트와 어댑터 규정

- [이 페이지가 담는 것](#이-페이지가-담는-것)
- [패턴이 요구하는 것](#패턴이-요구하는-것)
- [약한 준수와 강한 준수](#약한-준수와-강한-준수)
- [네 요소와 다섯째 요소](#네-요소와-다섯째-요소)
- [앱](#앱)
- [포트](#포트)
- [액터 — 대칭 속의 비대칭](#액터--대칭-속의-비대칭)
- [어댑터](#어댑터)
- [다섯째 요소 — Configurator](#다섯째-요소--configurator)
- [필수와 선택과 패턴 밖](#필수와-선택과-패턴-밖)
- [이어지는 페이지](#이어지는-페이지)

## 이 페이지가 담는 것

이 패턴의 규정은 이 KB에 이미 두 갈래로 들어와 있다 — [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)이
파이썬 구현서와 도메인 주도 설계 입문서를 경유해 포트=인터페이스, 어댑터=구현, 구동/피구동의
대응, 그리고 육각형·양파·클린이 같은 패턴이라는 판정을 담는다. 이 페이지는 그 규정을 만든
당사자인 콕번(Alistair Cockburn)이 후안 마누엘 가리도 데 파스(Juan Manuel Garrido de Paz)와 함께
**원저자로서 직접 규정한 것**을 담는다. 2차 서술이 이미 세운 것은 그쪽 페이지에 정박하고, 여기에는
원전이 더하는 프레이밍만 적는다 — 패턴이 요구하는 것의 문장, 약한 준수와 강한 준수의 가름,
다섯째 요소 Configurator, 제공·요구 인터페이스의 어휘, 그리고 필수·선택·패턴 밖의 구분이다.

## 패턴이 요구하는 것

- 패턴은 2005년에 "헥사고날 아키텍처"로 처음 기록됐고, 그것이 요구하는 것을 저자가 한 문장으로
  못 박는다 (1장 §"1.1. Copy this code"):[^cockburn2024]

  > Create your application to work without either a UI or a database so you can run automated
  > regression-tests against it, change connected technologies, protect it from leaks between
  > business logic and technologies, work when the database becomes unavailable, and link
  > applications together without any user involvement.

  - 이 한 문장이 목적의 목록이다 — UI도 데이터베이스도 없이 돌아가게 만들어, 자동 회귀 시험을
    걸고, 연결된 기술을 갈아 끼우고, 업무 로직과 기술 사이의 누출을 막고, 데이터베이스가
    끊겨도 동작하고, 사용자 개입 없이 애플리케이션끼리 잇는 것이다.
- 그 목적을 실제로 강제하는 요구가 하나 있고, 저자는 그것을 **가장 놀라운 부분**이라 부른다
  (1장 §"1.1. Copy this code"):[^cockburn2024]

  > "Never explicitly name any external object or technology. Always take a parameter for any
  > external object or technology you wish to access."

  - 외부 객체나 기술을 코드 안에서 이름으로 부르지 말고, 접근하려는 외부 객체·기술은 언제나
    인수로 받으라는 것이다. 같은 처방을 파이썬 축이 "암묵적 의존(임포트)을 명시적 의존(인수)으로
    바꾼다"로 적는다 — 그 전문은 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의
    "암묵적 의존과 명시적 의존"에 있다. 원전은 그것을 패턴의 **정의적 요구**로 앞세운다.
- 위 목적의 목록은 2005년 원문의 것에서 자라 온 것이다 — 6장 6.2절에 재수록된 2005년 원문의 첫
  문장(패턴의 "thumbnail")은 이렇다 (6장 §"6.2. 원문"):[^cockburn2024]

  > Create your application to work without either a UI or a database so you can run automated
  > regression-tests against the application, work when the database becomes unavailable, and link
  > applications together without any user involvement.

  - 2005년 원문에서는 목적이 셋이었다 — UI도 데이터베이스도 없이 돌아가게 만들어 자동 회귀 시험을
    걸고, 데이터베이스가 끊겨도 동작하고, 사용자 개입 없이 애플리케이션끼리 잇는 것이다. **2024년
    저술 시점의 판(위 1.1절 인용)은 여기에 두 조항을 더했다** — "연결된 기술을 갈아 끼운다(change
    connected technologies)"와 "업무 로직과 기술 사이의 누출을 막는다(protect it from leaks between
    business logic and technologies)"다. 요구의 골자(외부 기술을 인수로 받으라)는 2005→2024 사이
    바뀌지 않았고, 목적의 목록만 두 항목 자라났다.

## 약한 준수와 강한 준수

- 위 요구를 지키는 데에는 약한 판과 강한 판이 있다는 것이 원전이 더하는 가름이다
  (1장 §"1.1. Copy this code"·2장 §"2.4. What is required, optional, and outside the pattern"):[^cockburn2024]

  > You can implement this pattern in a legal but weak way. Suppose you know that the database will
  > use SQL. Without tying to a particular database, you still express the driven port in SQL. While
  > technically meeting the rules of the architecture, that still ties your system to SQL, which is
  > not what we are after.

  - 약한 준수는 특정 데이터베이스에 묶지는 않되 피구동 포트를 여전히 SQL로 표현하는 것이다.
    규칙의 자구는 지키지만 체계가 SQL에 매인 채로 남는다.
- 강한 준수의 기준은 한 줄이다 (2장 §"2.4. What is required, optional, and outside the pattern"):[^cockburn2024]

  > the app cannot know *anything* about the external technology.

  - 즉 피구동 포트가 오로지 애플리케이션 언어에서 뜻이 통하는 개념으로만 표현되어, 앱은 거기에
    데이터베이스가 있다는 것조차, 하물며 그것이 SQL이라는 것은 더더욱 알 수 없어야 한다. 이
    약함/강함의 구분은 2차 서술에는 없는, 원전이 세우는 잣대다.

## 네 요소와 다섯째 요소

- 패턴은 네 요소를 부르고, 그 넷에 더해 공식적으로는 패턴 밖이지만 실제로는 반드시 필요한
  다섯째 요소가 있다 (2장 §"2.2. The pattern elements: App, Ports, Actors, Adapters"):[^cockburn2024]
  - 애플리케이션 또는 시스템 자체 — 저자가 **앱(app)**이라 부른다.
  - 포트(ports).
  - 구동·피구동 외부 액터(driving and driven external actors).
  - 각 포트에 필요한 만큼의 어댑터(adapters).
- 이 넷을 잇는 코드가 **Configurator**이고, 저자는 그것이 엄밀히는 패턴 밖이라 따로 다룬다
  (2장 §"2.2. The pattern elements: App, Ports, Actors, Adapters").[^cockburn2024]

## 앱

- 앱의 규정은 기술로부터의 완전한 무지다 — **앱 또는 시스템은 원하는 기능을 제공하는 데 필요한
  업무 로직 전부이되 외부 기술은 포함하지 않으며, 기술 불가지(technology-agnostic)이고 연결된
  특정 기술이나 플랫폼을 참조하지 않고 오직 업무의 언어로만 쓰인다**
  (2장 §"2.2. The pattern elements: App, Ports, Actors, Adapters").[^cockburn2024] 어휘집은 앱의
  동의어로 Hexagon·System·SuD·SuT·Core를 든다 (2장 §"2.1. Glossary").[^cockburn2024]
- 앱을 컴포넌트로 만드는 것이 두 인터페이스다 — 앱이 세계에 제공하는 서비스 집합인 **제공
  인터페이스(provided interface, UML 용어, API·호출 인터페이스)**와, 앱이 자기 기능을 수행하려고
  다른 개체에게 그들의 제공 인터페이스로 내놓으라고 요구하는 **요구 인터페이스(required
  interface, UML 용어, SPI)**다 (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 둘 중 놀라운 쪽이 요구 인터페이스이고, 저자는 그것이 이 패턴을 강력하게 만드는 것이라 못
  박는다 — **제공 인터페이스는 어떤 애플리케이션에서든 기대하는 것이지만, 더 놀랍고 포트와
  어댑터 패턴을 그토록 강력하게 만드는 것은 요구 인터페이스다**
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
  - 그래서 앱은 모든 외부 개체에게 이렇게 말한다 (2장 §"2.2. The pattern elements…"):[^cockburn2024]

    > "I will only talk to you if you talk in my language,"

    앱이 그 언어를 명시적으로 정의하는 것, 바로 이것이 앱을 카탈로그에서 꺼내 어느 체계에나
    꽂을 수 있는 컴포넌트로 만든다. 카탈로그에 넣을 뜻이 전혀 없어도 그 단단한 경계가
    시험 가능성·누출 차단·기술 교체라는 이득을 준다.

## 포트

- 포트가 앱의 진짜 경계를 정의한다 — **앱과 바깥 세계의 모든 상호작용은 앱 자신이 정의한
  인터페이스 언어로 포트 인터페이스에서 일어나며, 그래서 포트가 앱 안과 밖의 구획선이다**
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 포트를 무엇으로 묶느냐가 이 규정의 핵심이다 — 저자는 상호작용을 **왜 상호작용하는가(의도)**로
  묶고, 어휘집에서 포트를 **어떤 의도로 만들어진 대화(conversation)의 발상을 포착한 것**이라
  규정한다 (2장 §"2.1. Glossary"·§"2.2. The pattern elements…").[^cockburn2024] 그래서 포트
  이름은 그 의도를 적는다 — **"For", 그다음 -ing로 끝나는 동사, 그다음 목적을 분명히 하는 데
  필요한 나머지**로 쓴다("For managing the contents of the shopping cart" 같은 식)
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 저자가 실무에서 자주 보는 포트의 갈래를 든다 (2장 §"2.2. The pattern elements…"):[^cockburn2024]
  - 구동 포트 셋 — 체계를 인스턴스화하고 설정하기 위한 것, 체계에 관리 작업을 하기 위한 것,
    체계로 업무를 처리하기 위한 것.
  - 피구동 포트 셋 — 저장소에서 정보를 얻기 위한 것, 누군가에게 알리기 위한 것, 어떤 장치를
    제어하기 위한 것.
- 언어에 따라 포트가 코드에 보이기도 안 보이기도 한다 — **자바·C++처럼 포트를 명시적으로
  선언해야 하는 언어가 있고, 루비·파이썬처럼 포트가 명시적으로 선언되지 않아 코드에 드러나지
  않는 언어가 있다** (2장 §"2.2. The pattern elements…").[^cockburn2024] 이 관찰의 파이썬 쪽
  전문은 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의 "포트와 어댑터가
  파이썬에서 무엇인가"에 있다 — 그쪽은 정적 타입이 없어 포트를 짚기가 더 어렵다는 문제로 같은
  사실을 말한다.

## 액터 — 대칭 속의 비대칭

- 패턴 자체는 의도적으로 대칭이다 — **포트와 어댑터 패턴은 의도적으로 대칭적이다. 그것은
  오직 앱의 안과 밖만을 말하며, 앱의 포트를 그 경계 정의로 삼는다**
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 그러나 구현에는 중요한 비대칭이 있고, 그 비대칭이 **누가 누구를 아는가**다
  (2장 §"2.2. The pattern elements…"):[^cockburn2024]
  - 앱은 자기 제공 인터페이스를 누가 호출하는지 알 필요가 없다 — 호출하는 쪽이 앱의 함수를
    알고 앱의 핸들을 쥐어야 한다.
  - 반대로 앱은 요구 인터페이스로 호출할 대상은 알아야 한다 — 외부 개체에 서비스를 요청하려면
    앱이 그 개체의 핸들을 쥐어야 한다.
- 이 비대칭에 붙이는 이름이 구동 액터와 피구동 액터다 — **구동(driving) 액터는 앱을 움직이는
  쪽, 피구동(driven) 액터는 앱에 의해 움직여지는 쪽**이다
  (2장 §"2.2. The pattern elements…").[^cockburn2024] 어휘집은 driving과 primary를, driven과
  secondary를 동의어로 두고, primary/secondary와 driving/driven만이 액터·어댑터·포트 셋 모두에
  붙는다고 적는다 (2장 §"2.1. Glossary"·§"The difficulty of naming").[^cockburn2024]
- 이 용어가 유스케이스에서 왔다는 것이 이 규정의 연결점이다 — **유스케이스의 세계가 여기
  꼭 맞는 낱말을 이미 갖고 있다: primary·secondary 액터. primary 액터는 앱을 행동으로 걷어차는
  개체이고, secondary 액터는 앱이 걷어차 행동시키는 개체다** (2장 §"2.2. The pattern
  elements…").[^cockburn2024]
- 이 대응이 곧 **포트를 몇 개 둘지와 인터페이스를 어떻게 포트로 나눌지**의 답이 된다 — 유스케이스의
  액터는 체계와 상호작용하는 이유로 특징지어지므로, **액터마다 포트를 하나 만드는 데서 출발하고,
  인터페이스마다 그것이 어느 액터를 섬기는지 묻는다** (2장 §"2.2. The pattern
  elements…").[^cockburn2024]
- 이 비대칭의 착상은 2005년 원문에 이미 있었다. 원문은 안과 밖의 가름이 왼쪽·오른쪽의 가름보다
  근본이라고 못 박는다 (6장 §"6.2. 원문"):[^cockburn2024]

  > The asymmetry to exploit is not that between _left_ and _right_ sides of the application but
  > between _inside_ and _outside_ of the application.

  - 2005년 원문에서 저자는 착취할 비대칭이 앱의 좌우가 아니라 안과 밖의 것이며, 지켜야 할 규칙은
    안쪽에 속한 코드가 바깥쪽으로 새지 않게 하는 것이라 적는다.
- 구동/피구동이라는 말은 2017년에야 생겼고(위 [이름과 역사](hexagonal-architecture-name-and-history.md)
  참조), 2005년 원문은 같은 가름을 유스케이스의 **primary·secondary 액터**로 적었다
  (6장 §"6.2. 원문"):[^cockburn2024]

  > A _primary actor_ is an actor that drives the application (takes it out of quiescent state to
  > perform one of its advertised functions). A _secondary actor_ is one that the application drives,
  > either to get answers from or to merely notify. The distinction between _primary _and_ secondary
  > _lies in who triggers or is in charge of the conversation.

  - 2005년 원문에서 primary 액터는 앱을 잠잠한 상태에서 걷어차 광고된 기능을 수행하게 하는 쪽,
    secondary 액터는 앱이 답을 얻거나 알리려고 구동하는 쪽이며, 둘을 가르는 것은 누가 대화를
    촉발하거나 주관하는가다. 원문은 또 이 관례에서 primary 포트·어댑터를 왼쪽(또는 위)에, secondary
    포트·어댑터를 오른쪽(또는 아래)에 그린다고 밝힌다 — 이것이 [포트와 어댑터와 이웃
    개념](ports-and-adapters-related-concepts.md)의 유스케이스 대응(5.1)과 같은 어휘다.

## 어댑터

- 어댑터가 늘 필요한 것은 아니다 — 구동·피구동 액터가 이미 제공·요구 인터페이스를 알고 쓰면
  어댑터가 없어도 된다. 시험 케이스를 짜서 앱을 구동할 때 앱의 제공 인터페이스를 시험 케이스에
  바로 코딩하거나, 두 앱을 처음부터 인터페이스가 맞도록 함께 설계하는 경우가 그렇다
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 이 점이 구동 쪽에서 오해를 부른 자리이고, 저자가 2023년 주석에서 그것을 바로잡는다. 2005년
  원문은 "이벤트가 포트에 도착하면 기술에 특정한 어댑터가 그것을 변환해 앱에 넘긴다"고 적었는데,
  이 문장이 헷갈리고 부정확하다는 지적을 받아 웹에서 고쳤으나 그래도 살짝 오해를 남긴다고 저자는
  적는다 — **구동 액터는 어댑터가 필요할 때도, 필요 없을 때도 있으며, 패턴은 그것을 구별하지도
  신경 쓰지도 않는다. 그 전부가 앱 바깥에서 일어난다** (6장 §"6.3. 2023 주석").[^cockburn2024]
  그래서 "어댑터가 필요 없으면 그 구동자, 필요하면 그 구동자의 어댑터"를 뭉뚱그릴 낱말이 없어
  **interactor**라는 말을 더했다고 밝힌다 — 이 용어의 실무 쓰임은 [포트와 어댑터 적용
  실무](ports-and-adapters-in-practice.md)의 개발 순서 절에 있다.
- 어댑터의 규정은 번역이다 — **어댑터는 앱의 인터페이스를 구동·피구동 액터의 인터페이스에 맞추는
  데 필요한 코드로, 기술에 특정한 외부 액터의 메시지를 포트에서의 기술 중립적 요청으로, 그리고
  그 반대로 번역한다** (2장 §"2.1. Glossary").[^cockburn2024] 컴퓨터 앞의 사람이 앱을 직접
  호출할 수 없어 CLI나 GUI를 거치는 것이 익숙한 어댑터의 예다
  (2장 §"2.2. The pattern elements…").[^cockburn2024]
- 어댑터는 앱 바깥에 있고, 그래서 패턴은 어댑터를 어떻게 조직할지 규율하지 않는다 — **포트와
  어댑터 아키텍처는 앱 안을 어떻게 조직하는지도, 앱 밖의 것을 어떻게 조직하는지도 입법하지
  않는다. 그것이 말하는 것은 오직 안과 밖이 있다는 것, 그리고 그 둘의 경계가 포트(제공과 요구)로
  정의된다는 것뿐이다** (2장 §"2.2. The pattern elements…").[^cockburn2024]

## 다섯째 요소 — Configurator

- 무언가가 조각들을 이어야 하고, 그것이 Configurator다 — **어떤 코드가 구동자에게 앱에
  닿는 법을 알려 주고 앱에게 어느 피구동 액터를 쓸지 알려 주어야 한다. 이것이 Configurator의
  역할이다** (2장 §"2.3. The 5th element: The Configurator").[^cockburn2024] 그 일을 하려면
  Configurator는 모든 참가자 — 앱, 구동 액터나 그 어댑터, 피구동 액터나 그 어댑터 — 를 알아야
  한다.
- 어떻게 설계하는지는 패턴이 정하지 않지만, 어떻게 배치하든 다음 동작이 일어나야 한다
  (2장 §"2.3. The 5th element: The Configurator"):[^cockburn2024]
  - 각 피구동 인터랙터(피구동 어댑터, 또는 어댑터가 필요 없는 피구동 액터)를 인스턴스화한다.
  - 앱을 인스턴스화한다.
  - 그 피구동 인터랙터들을 앱에 준다.
  - 각 구동 인터랙터(액터 또는 어댑터)를 인스턴스화하고 쓸 앱을 건넨다.
- 이 역할을 실제로 누가 맡는가가 이 KB의 다른 페이지와 이어지는 자리다 — **시험에서는 시험
  케이스가 Configurator이자 구동 액터 노릇을 한다. 프로덕션에서는 보통 "main" 또는 합성
  루트(composition root)가 Configurator 노릇을 하며 모든 참가자를 끌어모은다**
  (2장 §"2.3. The 5th element: The Configurator").[^cockburn2024] 그리고 앞의 두 경우에는
  Spring 같은 의존성 주입 프레임워크를 쓸 수 있다고 적는다. 그 수단의 전문은
  [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md)에 있다 — 그쪽
  소스들이 "포트를 어댑터로 해소하는 수단"으로 든 주입과 부트스트랩이, 원전에서는 이
  Configurator라는 역할을 채우는 두 가지 구현 방식으로 나타난다.
- Configurator가 시스템 초기화 시점에 모든 연결을 맺는 첫 시나리오를 저자가 그림으로 보인다 —
  Configurator가 먼저 피구동 어댑터를 전부 인스턴스화하고(또는 어댑터가 필요 없는 피구동 액터의
  ID를 얻고), 그다음 앱을 인스턴스화해 앱 생성자에 피구동 액터를 넣고, 마지막으로 각 구동
  어댑터를 인스턴스화하며 앱을 건네는 순서다 (2장 §"2.3. The 5th element: The Configurator",
  그림 2.1).[^cockburn2024]
- Configurator를 어떤 형태로 지을지를 저자가 2023년에 별도 패턴 **Configurable Receiver**로 규정했고,
  그것을 6장 6.5절에 원문으로 재수록한다. 그 패턴의 규정은 "실행 시점에 수신자(receiver)를 설정하거나
  바꾼다"이며, **의존성 주입(dependency injection)과 의존성 조회(dependency lookup)를 함께 아우른다** —
  Configurator가 발신자에게 어느 수신자를 쓸지 알려 주면 의존성 주입이고, 발신자가 Configurator(서비스
  로케이터 또는 브로커)에게 물어보면 의존성 조회다 (6장 §"6.5. Configurable Receiver").[^cockburn2024]
  저자는 포트와 어댑터가 **어느 형태의 Configurator를 써야 하는지는 말하지 않으며, Configurable
  Receiver가 서술한 어느 것이든 쓸 수 있다**고 못 박는다 (6장 §"6.5. Configurable
  Receiver").[^cockburn2024] 그 두 수단의 규정과 이 KB의 2차 서술은 [의존성 주입과
  부트스트랩](../concepts/dependency-injection-and-bootstrap.md)에 있다.

## 필수와 선택과 패턴 밖

- 패턴을 적용하려면 무엇이 패턴 안이고 무엇이 유용한 팁이며 무엇이 패턴 밖인지 알아야 한다는
  것이 이 절의 취지다 (2장 §"2.4. What is required, optional, and outside the pattern").[^cockburn2024]
- 패턴이 **필수로 요구하는 것** (2장 §"2.4. What is required…"):[^cockburn2024]
  - 앱이 모든 외부 상호작용에 대해 제공 또는 요구 인터페이스를 정의한다.
  - 앱이 제공 인터페이스에는 구동 포트를, 피구동 인터페이스에는 피구동 포트를 정의한다(인터페이스
    선언이 필요 없는 언어에서는 명시적으로 안 보일 수 있다).
  - 앱이 피구동 액터를 런타임에 설정할 수 있게 한다.
  - 앱이 자기 primary·secondary 액터에 대한 **소스 코드 의존을 갖지 않는다.**
  - 외부 액터는 정의된 포트로만 상호작용할 수 있고, 헥사곤 안의 무엇에도 직접 접근할 수 없다.
  - 포트와 인터페이스가 기술 중립일 뿐 아니라 **오직 업무 필요를 표현하는 낱말**만 쓴다.
- 패턴이 요구하지 않는 **선택 사항(유용한 팁)** — Configurator를 어떻게 구현할지, 포트 이름을
  어떻게 지을지("For doing something" 권장), 포트를 얼마나 잘게 나눌지(적은 쪽을 선호하며 primary
  액터마다 하나, secondary마다 하나에서 출발), 코드베이스를 어떻게 조직할지("Driving Ports"/
  "Driven Ports" 폴더는 앱 곁에, "Driving Adapters"/"Driven Adapters" 폴더는 앱과 다른 공간에)가
  전부 여기 든다 (2장 §"2.4. What is required…").[^cockburn2024]
- 저자가 이 자리에서 **중첩**에 못을 박는다 — 패턴이 더 큰 포트와 어댑터 시스템 안에 포트와
  어댑터 하위 시스템을 두는 것을 명시적으로 배제하지는 않지만, 그것을 있을 법하지 않다고 보아
  **패턴은 중첩하지 않는다(the pattern does not nest)**고 적는다
  (2장 §"2.4. What is required…").[^cockburn2024] 이 판정의 전문은 5장의 중첩 헥사곤 물음에 있다.
- 그리고 **패턴 밖**의 선언이 이 패턴을 이웃 패턴과 가르는 자리다 — **패턴은 당신이 애플리케이션을
  내부적으로 어떻게 구조화하는지에 대해 절대적으로 아무 말도 하지 않는다. DDD를 써도 좋고 안
  써도 좋으며, 함수와 모델을 갈라도 좋고 진흙 공을 만들어도 좋다**
  (2장 §"2.4. What is required…").[^cockburn2024] 저자는 바로 이 점이 이 패턴을 클린·양파
  아키텍처와 다르게 만든다고 못 박는다 — **이것이 이 패턴을 클린·양파 아키텍처와 다르게 만든다**
  (2장 §"2.4. What is required…").[^cockburn2024] 두 아키텍처의 차이를 정면으로 대는 절은
  5장의 "Layered, onion, clean, hexagonal: what is the difference?"에 있고, 이 판정은
  [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의 "육각형·양파·클린은 같은
  패턴이다"가 2차 서술로 담은 것과 갈리는 대목이다.

## 이어지는 페이지

- [코드로 본 포트와 어댑터](ports-and-adapters-in-code.md) — 이 규정이 코드에서 어디에 서는지를
  세금 계산기·web-hexagon·BlueZone 세 사례로 보이는 자리
- [포트와 어댑터 적용 실무](ports-and-adapters-in-practice.md) — 같은 규정을 실무 문답으로 되풀이한
  자리(포트란 무엇인가·앱 경계·포트 수·파일 배치·개발 순서)
- [헥사고날 아키텍처의 이름과 역사](hexagonal-architecture-name-and-history.md) — 왜 "육각형"인가,
  포트와 어댑터로 이름을 고친 내력, 그리고 이 패턴의 비용과 편익
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 이 KB에서 사는
  자리이자 2차 서술의 정박점
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — Configurator
  역할을 실제로 채우는 두 수단
- [계층 아키텍처](../concepts/layered-architecture.md) — 이 뒤집기의 출발점이 되는 패턴
- [서비스 레이어](../concepts/service-layer-pattern.md) — 뒤집은 구조 위에 얹히는 조율 층
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — 같은 조직 원리 위에서 데이터 관리만 달리하는 패턴
- [Component + Strategy 패턴](component-plus-strategy-pattern.md) — 이 패턴이 특수 경우로 속하는
  일반형(같은 원전 6장)
- [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md) — 어느 아키텍처
  패턴을 고를지가 걸리는 입력
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) — 이 축의 허브

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 1장 §"1.1. Copy this code" · 2장 §"2.1. Glossary" ·
    §"The difficulty of naming" · §"2.2. The pattern elements: App, Ports, Actors, Adapters" ·
    §"2.3. The 5th element: The Configurator" · §"2.4. What is required, optional, and outside the
    pattern"(그림 2.1 포함) · 6장 §"6.2. The original article: The Hexagonal (Ports & Adapters)
    Architecture"(2005년 원문 재수록) · §"6.3. Comments on the original article in 2023" ·
    §"6.5. The article: "Configurable Receiver"". 2005년 원문 직인용은 텍스트 레이어 훼손 없는
    구간만 옮겼다. EPUB(Calibre 변환본), 쪽 앵커 없음 — locator는 장·절 번호.

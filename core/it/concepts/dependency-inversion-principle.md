---
type: concept
title: 의존성 역전 원칙
description: SOLID의 D를 한 애플리케이션에 끝까지 적용한다는 것이 무슨 뜻인가 — 고수준 모듈과 저수준 모듈을 조직이 관심 갖는가로 가르는 정의, "의존한다"가 임포트나 호출보다 넓은 뜻이라는 한정, 층을 나누고 아래로만 의존하게 하는 3층 구조를 안팎으로 뒤집어 양파 구조로 만드는 수순, 포트와 어댑터라는 이름이 파이썬에서 무엇에 대응하는가, 추상 기반 클래스 없이 덕 타이핑으로도 추상이 성립한다는 판단, 암묵적 의존(임포트)을 명시적 의존(인수)으로 바꾸는 것이 이 원칙의 실물이라는 규정, 그리고 도메인 주도 설계 쪽 소스가 같은 뒤집기를 계층 아키텍처에서 단계적으로 유도해 포트와 어댑터 아키텍처로 부르는 수순과 표현·데이터 접근 두 층을 인프라 층 하나로 합치는 첫 단계, 포트와 어댑터의 규정과 해소 수단 둘, 육각형·양파·클린이 같은 패턴의 다른 이름이라는 판정이 유비쿼터스 언어의 예로 제시되는 자리, 그리고 이 아키텍처가 도메인 모델 패턴에 맞는다는 대응
generated: { by: "claude-opus-5", at: "2026-09-15T00:00:00Z" }
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 의존성 역전 원칙

- [정의와 그 해설](#정의와-그-해설)
- [고수준과 저수준을 가르는 기준](#고수준과-저수준을-가르는-기준)
- [왜 뒤집는가](#왜-뒤집는가)
- [층 구조를 안팎으로 뒤집기 — 양파 구조](#층-구조를-안팎으로-뒤집기--양파-구조)
- [포트와 어댑터가 파이썬에서 무엇인가](#포트와-어댑터가-파이썬에서-무엇인가)
- [추상 기반 클래스는 필수가 아니다](#추상-기반-클래스는-필수가-아니다)
- [암묵적 의존과 명시적 의존](#암묵적-의존과-명시적-의존)
- [이 원칙을 구현하는 네 패턴](#이-원칙을-구현하는-네-패턴)
- [계층 아키텍처에서 이 뒤집기를 유도하면](#계층-아키텍처에서-이-뒤집기를-유도하면)
- [포트와 어댑터의 규정](#포트와-어댑터의-규정)
- [육각형·양파·클린은 같은 패턴이다](#육각형양파클린은-같은-패턴이다)
- [이 아키텍처가 맞는 자리](#이-아키텍처가-맞는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 코드가 기술 세부에 매이지 않게 하려면 의존의 화살표를 어디서 어떻게
뒤집는가.**

## 정의와 그 해설

- 저자들이 정식 정의를 그대로 옮긴다 (Introduction §"The Dependency Inversion
  Principle"):[^percival2020]

  > High-level modules should not depend on low-level modules. Both should depend on
  > abstractions.
  >
  > Abstractions should not depend on details. Instead, details should depend on
  > abstractions.

- 그리고 이 원칙이 SOLID의 D임을 밝힌다. 저자들이 각주에 SOLID 전체를 풀어 둔다 —
  **SOLID는 Robert C. Martin의 객체 지향 설계 다섯 원칙의 두문자다: 단일 책임, 확장에는
  열려 있고 수정에는 닫혀 있음, 리스코프 치환, 인터페이스 분리, 의존성 역전**
  (Introduction 각주 2).[^percival2020]
- **책 전체가 이 원칙의 예제라고 선언된다** — **불행히도 우리는 캡슐화 때 했던 것처럼 작은
  코드 목록 셋으로 DIP를 예시할 수 없다. 그러나 1부 전체가 본질적으로 한 애플리케이션
  전반에 DIP를 구현하는 실습 예제이므로, 구체적인 예는 충분히 보게 될 것이다**
  (Introduction §"The Dependency Inversion Principle").[^percival2020]
- 둘째 조항이 더 어렵다는 것도 저자들이 인정한다 — **둘째 부분은 더 알쏭달쏭하다.
  "추상은 세부에 의존해서는 안 된다"는 충분히 명확해 보이지만 "세부가 추상에 의존해야
  한다"는 상상하기 어렵다. 추상하고 있는 세부에 의존하지 않는 추상을 어떻게 가질 수
  있는가?** (Introduction §"The Dependency Inversion Principle").[^percival2020]
  그 답을 4장에서 준다고 예고하고, 실제로 서비스 레이어가 `AbstractRepository`에 의존하고
  `SqlAlchemyRepository`도 같은 추상에 의존하는 그림으로 답한다
  ([서비스 레이어](service-layer-pattern.md)의 "DIP의 실물"에 있다).

## 고수준과 저수준을 가르는 기준

- 기준이 기술이 아니라 **조직의 관심**이다 (Introduction §"The Dependency Inversion
  Principle"):[^percival2020]
  - **고수준 모듈은 당신 조직이 정말로 신경 쓰는 코드다.** 제약 회사라면 환자와 임상
    시험을, 은행이라면 거래와 환전을 다루는 코드다. **소프트웨어 시스템의 고수준 모듈은
    우리의 현실 세계 개념을 다루는 함수·클래스·패키지다.**
  - **반대로 저수준 모듈은 당신 조직이 신경 쓰지 않는 코드다. 당신 인사팀이 파일 시스템이나
    네트워크 소켓에 흥분할 일은 없을 것 같다. 재무팀과 SMTP·HTTP·AMQP를 논하는 일도 잦지
    않다.** 그리고 저자들이 그 무관심을 한 문장으로 요약한다 — **급여가 제때 돌기만 하면
    당신 사업은 그것이 크론 잡인지 쿠버네티스 위의 일시적 함수인지 신경 쓰지 않을 것이다.**
- **"의존한다"의 뜻이 넓다** — **의존한다(depends on)는 것이 반드시 임포트하거나 호출한다는
  뜻은 아니고, 한 모듈이 다른 모듈에 대해 알거나 그것을 필요로 한다는 더 일반적인
  발상이다** (Introduction §"The Dependency Inversion Principle").[^percival2020]
  - 이 한정어가 실무에서 결정적이다. 임포트 그래프가 깨끗해도 **한쪽이 다른 쪽의 스키마나
    실행 순서를 알고 있으면 의존은 남아 있다.** 같은 성질을
    [변경에 대한 결합도](../concepts/coupling-with-respect-to-change.md)가 "소스 코드만 봐서는 잴 수
    없다"로 말한다 — 두 소스가 서로를 참조한 적은 없다.
- 추상의 정의는 앞 절에서 이미 나와 있다 — **추상은 행동을 캡슐화하는 단순화된
  인터페이스이며, 우리 `duckduckgo` 모듈이 검색 엔진 API를 캡슐화한 방식과 같다**
  (Introduction §"The Dependency Inversion Principle").[^percival2020] 그 캡슐화 예제의
  전문은 [추상화 고르기](../concepts/choosing-abstractions.md)에 있다.

## 왜 뒤집는가

- 이유가 **변경 속도의 비대칭**이다 — **넓게 말해 우리는 그것들을 서로 독립적으로 바꿀 수
  있기를 원하기 때문이다. 고수준 모듈은 업무 요구에 맞춰 바꾸기 쉬워야 한다. 저수준
  모듈(세부)은 실무에서 흔히 바꾸기가 더 어렵다: 함수 이름을 바꾸는 리팩터링과, 열 이름을
  바꾸려고 데이터베이스 마이그레이션을 정의하고 테스트하고 배포하는 것을 비교해 보라**
  (Introduction §"The Dependency Inversion Principle").[^percival2020]
- 반대 방향도 함께 요구된다 — **그러나 마찬가지로, 필요할 때 인프라 세부를 바꿀 수 있는
  것도 중요하다(예컨대 데이터베이스 샤딩을 생각해 보라). 업무 계층을 바꿀 필요 없이
  말이다. 둘 사이에 추상을 더하는 것(그 유명한 여분의 간접 계층)이 둘을 (더) 독립적으로
  바꿀 수 있게 해 준다** (Introduction §"The Dependency Inversion
  Principle").[^percival2020]
- 저자들이 인용하는 격언이 그 간접 계층의 근거다 (Introduction §"The Dependency Inversion
  Principle"):[^percival2020]

  > All problems in computer science can be solved by adding another level of indirection.
  >
  > — David Wheeler

  - 이 격언에는 잘 알려진 후반부가 있지만 저자들은 그것을 옮기지 않았다. 다만 책 전체가
    간접 계층의 대가를 장마다 표로 계상하므로 후반부의 자리는 비어 있지 않다.
    #hypothesis 이 관찰은 이 KB의 것이다.

## 층 구조를 안팎으로 뒤집기 — 양파 구조

- 출발점이 흔한 3층 구조다 — **층 구조 아키텍처는 아마 업무 소프트웨어를 만드는 가장 흔한
  패턴일 것이다. 이 모형에서 우리는 웹 페이지·API·명령줄일 수 있는 사용자 인터페이스
  구성 요소를 갖고, 이 구성 요소들이 우리 업무 규칙과 작업 흐름을 담은 업무 로직 계층과
  소통하며, 마지막으로 데이터를 저장하고 되찾는 책임을 지는 데이터베이스 계층을 갖는다**
  (Introduction §"Layering").[^percival2020]
- 층을 나누는 이유가 의존 그래프다 — **한 함수·모듈·객체가 다른 것을 쓸 때 우리는 하나가
  다른 것에 의존한다고 말한다. 이 의존들은 일종의 네트워크나 그래프를 이룬다. 진흙 공에서는
  의존이 통제를 벗어나 있다. 그래프의 한 노드를 바꾸는 것이 어려워지는데, 그것이 시스템의
  다른 많은 부분에 영향을 줄 잠재력이 있기 때문이다** (Introduction
  §"Layering").[^percival2020]
- 그리고 선언 — **이 책의 나머지에서 우리는 하나의 단순한 원칙을 지킴으로써 이 모형을
  체계적으로 안팎으로 뒤집을 것이다** (Introduction §"Layering").[^percival2020]
- 뒤집힌 결과에 이름이 붙는다 — **우리 모델을 "안쪽"에 있는 것으로 생각하고 의존이 그쪽으로
  흘러 들어오게 할 것이다. 이것을 사람들이 때때로 양파 아키텍처(onion architecture)라고
  부른다** (2장 §"Applying the DIP to Data Access").[^percival2020] 발표 계층은 도메인
  모델을 가리키고, **데이터베이스 계층도 도메인 모델을 가리킨다** — 화살표 방향이 뒤집힌
  것이 이 그림의 전부다.
- 요구 수위가 높다 — **그러나 우리는 우리 도메인 모델이 그 어떤 의존도 갖지 않기를
  원한다** (2장 §"Applying the DIP to Data Access").[^percival2020] 저자들이 각주에서
  그 말을 좁힌다 — **"상태를 가진 의존이 없다"는 뜻인 것 같다. 헬퍼 라이브러리에 의존하는
  것은 괜찮다; ORM이나 웹 프레임워크에 의존하는 것은 아니다** (2장 각주 1).[^percival2020]
- **이름 논쟁을 저자들이 정리한다** — 포트와 어댑터, 육각형 아키텍처, 양파 아키텍처,
  클린 아키텍처가 무엇이 다르냐는 물음에 — **어떤 사람들은 차이를 두고 트집 잡기를
  좋아하지만, 이것들은 거의 같은 것에 대한 이름이고 전부 의존성 역전 원칙으로 환원된다:
  고수준 모듈(도메인)이 저수준 모듈(인프라)에 의존해서는 안 된다**
  (2장 §"Is This Ports and Adapters?" 곁글).[^percival2020]

## 포트와 어댑터가 파이썬에서 무엇인가

- 정의 — **포트와 어댑터는 객체 지향 세계에서 나왔고, 우리가 붙잡는 정의는 포트가 우리
  애플리케이션과 우리가 추상하려는 무엇 사이의 인터페이스이고, 어댑터가 그 인터페이스나
  추상 뒤의 구현이라는 것이다** (2장 §"What Is a Port and What Is an Adapter, in
  Python?").[^percival2020]
- **파이썬에서 포트를 짚기가 더 어렵다는 것이 이 절의 요지다** — **이제 파이썬에는
  인터페이스가 그 자체로 없으므로, 어댑터를 식별하기는 대개 쉽지만 포트를 정의하기는 더
  어려울 수 있다. 추상 기반 클래스를 쓰고 있다면 그것이 포트다. 아니라면 포트는 그저 당신
  어댑터들이 따르고 당신 핵심 애플리케이션이 기대하는 덕 타입 — 쓰이고 있는 함수·메서드
  이름들, 그리고 그 인수 이름과 타입 — 이다**
  (2장 §"What Is a Port and What Is an Adapter, in Python?").[^percival2020]
- 예제에서의 대응이 명시된다 — **구체적으로 이 장에서 `AbstractRepository`가 포트이고,
  `SqlAlchemyRepository`와 `FakeRepository`가 어댑터다**
  (2장 §"What Is a Port and What Is an Adapter, in Python?").[^percival2020]
- 어댑터에도 방향이 있다. 프로젝트 폴더 구조를 논하며 저자들이 구분한다 —
  `adapters/`에 들어가는 것은 **엄밀히 말해 이차(secondary)·피동(driven)·안쪽을 향하는
  어댑터**라 부르고, `entrypoints/`에 들어가는 것은 **공식 포트와 어댑터 용어로는
  일차(primary)·구동(driving)·바깥을 향하는 어댑터**다
  (4장 §"Putting Things in Folders to See Where It All Belongs").[^percival2020]
  - 포트가 어디 사는지도 정해져 있다 — **포트는 어댑터가 구현하는 추상 인터페이스다.
    우리는 포트를 그것을 구현하는 어댑터와 같은 파일에 두는 편이다**
    (4장 §"Putting Things in Folders…").[^percival2020]

## 추상 기반 클래스는 필수가 아니다

- 이 책이 ABC를 쓰는 이유가 교육적이라고 밝혀진다 — **우리는 교육적 이유로 이 책에서 추상
  기반 클래스를 쓰고 있다: 리포지터리 추상의 인터페이스가 무엇인지 설명하는 데 도움이 되기를
  바란다** (2장 §"Abstract Base Classes, Duck Typing, and Protocols" 곁글).[^percival2020]
- **실제 코드에서는 지웠다고 적는다** — **실제로 우리는 때때로 프로덕션 코드에서 ABC를
  지우고 있는 우리 자신을 발견했는데, 파이썬이 그것을 무시하기를 너무 쉽게 만들어서 결국
  유지보수되지 않고 최악의 경우 오해를 부르기 때문이다. 실무에서 우리는 흔히 그냥 파이썬의
  덕 타이핑에 기대어 추상을 가능하게 한다. 파이써니스타에게 리포지터리는 `add(thing)`과
  `get(id)` 메서드를 가진 임의의 객체다**
  (2장 §"Abstract Base Classes, Duck Typing, and Protocols" 곁글).[^percival2020]
- 대안이 하나 제시된다 — **살펴볼 대안 하나가 PEP 544 프로토콜이다. 이것은 상속의 가능성
  없이 타이핑을 준다. "상속보다 합성을 선호하라" 팬들이 특히 좋아할 것이다**
  (2장 §"Abstract Base Classes, Duck Typing, and Protocols" 곁글).[^percival2020]
  - 버전 조건: 파이썬 3.8 이상. `typing.Protocol`이 표준 라이브러리에 들어온 릴리스다.
    이 책은 2020년 시점이라 그 앞의 관행(ABC와 덕 타이핑)을 기본으로 쓴다.
- ABC가 파이썬에서 실제로 작동하게 만드는 것 하나도 짚어 둔다 — **파이썬 팁:
  `@abc.abstractmethod`는 파이썬에서 ABC가 실제로 "작동하게" 만드는 몇 안 되는 것 중
  하나다. 파이썬은 부모 클래스에 정의된 모든 `abstractmethod`를 구현하지 않은 클래스의
  인스턴스를 만들지 못하게 거부한다** (2장 §"The Repository in the
  Abstract").[^percival2020] 그리고 단서 — **`raise NotImplementedError`는 좋지만
  필요하지도 충분하지도 않다** (2장 §"The Repository in the Abstract").[^percival2020]

## 암묵적 의존과 명시적 의존

- 13장이 이 원칙을 가장 국소적인 형태로 되돌린다. 파이썬의 기본 관행은 암묵적이다 —
  **일이 파이썬에서 보통 돌아가는 방식에 익숙하다면 이 모든 것이 좀 이상하다고 생각할
  것이다. 일을 하는 표준적인 방법은 그냥 임포트해서 의존을 암묵적으로 선언하고, 테스트를
  위해 바꿔야 하면 동적 언어에서 옳고 참된 것인 몽키패치를 하는 것이다**
  (13장 §"Aren't Explicit Dependencies Totally Weird and Java-y?").[^percival2020]
- **그 절충이 정직하게 계상된다** — **그러니 절충이다. 그렇다, 명시적 의존을 선언하는 것은
  엄밀히 말해 불필요하고, 그것을 쓰면 우리 애플리케이션 코드가 약간 더 복잡해질 것이다.
  그러나 그 대가로 우리는 쓰고 관리하기 더 쉬운 테스트를 얻는다**
  (13장 §"Aren't Explicit Dependencies Totally Weird and Java-y?").[^percival2020]
- 그리고 이 페이지의 원칙으로 되돌아온다 — **그 위에, 명시적 의존을 선언하는 것은 의존성
  역전 원칙의 한 예다 — 특정 세부에 대한 (암묵적) 의존을 갖는 대신 우리는 추상에 대한
  (명시적) 의존을 갖는다**
  (13장 §"Aren't Explicit Dependencies Totally Weird and Java-y?").[^percival2020]
  저자들이 그 자리에 붙이는 인용이 파이썬 자신의 격언이다 (13장):[^percival2020]

  > Explicit is better than implicit.
  >
  > — The Zen of Python

- 몽키패치의 대가도 구체적이다 — **그리고 목이 우리를 구현에 단단히 결합한다는 것을 알
  것이다. `email.send_mail`을 몽키패치하기로 고르면 우리는 `import email`을 하는 데 묶이고,
  언젠가 `from email import send_mail`이라는 사소한 리팩터링을 하고 싶어지면 우리 목을 전부
  바꿔야 한다** (13장 §"Aren't Explicit Dependencies Totally Weird and
  Java-y?").[^percival2020] 같은 판정의 전문은 [가짜와 목](fakes-versus-mocks.md)에 있다.

## 이 원칙을 구현하는 네 패턴

1부의 네 장이 각각 이 원칙의 한 적용이다. 1부 맺음이 그것을 한 문단으로 요약한다 —
**의존성 역전 원칙을 적용하고 Repository와 Unit of Work 같은 포트와 어댑터에서 영감을 받은
패턴들을 씀으로써, 우리는 TDD를 높은 기어와 낮은 기어 둘 다에서 하고 건강한 테스트 피라미드를
유지하는 것을 가능하게 만들었다** (7장 §"Part I Recap").[^percival2020]

| 패턴 | 무엇을 추상하는가 | 어느 페이지에 |
|---|---|---|
| Repository | 영속 저장소 | [리포지터리 패턴](repository-pattern.md) |
| Service Layer | 사용 사례(작업 흐름 조율) | [서비스 레이어](service-layer-pattern.md) |
| Unit of Work | 원자적 연산 | [작업 단위 패턴](unit-of-work-pattern.md) |
| Aggregate | 일관성 경계 | [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) |

## 계층 아키텍처에서 이 뒤집기를 유도하면

[khononov2021](../sources/khononov2021.md)이 같은 뒤집기를 **계층 아키텍처를 리팩터링하는
수순**으로 보인다. 위 [층 구조를 안팎으로 뒤집기 — 양파 구조](#층-구조를-안팎으로-뒤집기--양파-구조)와
같은 조작이되, 단계가 명시적이고 결과물에 아키텍처 패턴의 이름이 붙는다.

- 출발점의 진단 (8장 §"Ports & Adapters", p.125):[^khononov2021]

> The ports & adapters architecture addresses the shortcomings of the layered architecture and is a
> better fit for implementation of more complex business logic. Interestingly, both patterns are
> quite similar.

  그 계층 아키텍처의 전문은 [계층 아키텍처](../concepts/layered-architecture.md)에 있다.
- **첫 단계는 층을 줄이는 것이다** (8장 §Terminology, p.126):[^khononov2021]

> Essentially, both the presentation layer and data access layer represent integration with external
> components: databases, external services, and user interface frameworks. These technical
> implementation details do not reflect the system's business logic; so, let's unify all such
> infrastructural concerns into a single "infrastructure layer,"

  - **위아래 두 층이 같은 것이었다는 관찰이 이 단계의 전부다.** 파이썬 쪽 소스의 3층 구조도
    사용자 인터페이스와 데이터베이스를 양 끝에 두고, 뒤집은 뒤에는 둘 다 안쪽을 가리키게
    된다 — 같은 자리를 이 판본은 **합치고 나서** 뒤집는다.
- **둘째 단계가 이 페이지의 원칙이다** (8장 §"Dependency Inversion Principle",
  p.126):[^khononov2021]

> The dependency inversion principle (DIP) states that high-level modules, which implement the
> business logic, should not depend on low-level modules. However, that's precisely what happens in
> the traditional layered architecture. The business logic layer depends on the infrastructure layer.

  뒤집은 결과 (8장, p.126):[^khononov2021]

> Instead of being sandwiched between the technological concerns, now the business logic layer takes
> the central role. It doesn't depend on any of the system's infrastructural components.

  - **"기술적 관심사 사이에 끼어 있는"이라는 표현이 계층 아키텍처의 그림을 정확히 요약한다.**
    위 [왜 뒤집는가](#왜-뒤집는가)가 그 이유를 변경 속도의 비대칭으로 대고, 이 판본은 같은
    조작을 아키텍처 패턴 사이의 변환으로 적는다.
- **셋째 단계로 애플리케이션 층이 파사드로 얹힌다** (8장, p.126):[^khononov2021]

> As the service layer in the layered architecture, it describes all the operations exposed by the
> system and orchestrates the system's business logic for executing them.

  - 저자가 이 자리에서 이름을 바꾼다는 것을 각주에 밝힌다 — 계층 아키텍처의 맥락이 아니므로
    **서비스 계층 대신 애플리케이션 계층**을 쓴다는 것이다 (8장, p.126, 각주 5).[^khononov2021]
    그 층의 전문은 [서비스 레이어](service-layer-pattern.md)에 있다.
- 그 결과가 포트와 어댑터 아키텍처다. 그리고 그것이 무엇을 가능하게 하는지가 못 박힌다 —
  **업무 로직이 아래 층 어디에도 의존하지 않으며, 그것이 도메인 모델과 이벤트 소싱 도메인 모델
  패턴을 구현하는 데 필요한 조건이다** (8장, p.127).[^khononov2021] 그 둘은
  [도메인 모델 패턴](domain-model-pattern.md)과
  [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)에 있다.

## 포트와 어댑터의 규정

- 목표 (8장 §"Integration of Infrastructural Components", p.127):[^khononov2021]

> The core goal of the ports & adapters architecture is to decouple the system's business logic from
> its infrastructural components.

- 이름의 유래가 되는 기제 (8장, p.127):[^khononov2021]

> Instead of referencing and calling the infrastructural components directly, the business logic
> layer defines "ports" that have to be implemented by the infrastructure layer. The infrastructure
> layer implements "adapters": concrete implementations of the ports' interfaces for working with
> different technologies

  - **위 [포트와 어댑터가 파이썬에서 무엇인가](#포트와-어댑터가-파이썬에서-무엇인가)의 정의와
    같은 것을 층의 언어로 말한다.** 그쪽은 포트를 "애플리케이션과 추상하려는 무엇 사이의
    인터페이스"로 규정하고, 이쪽은 **누가 정의하고 누가 구현하는가**를 층으로 못 박는다 —
    포트는 업무 로직 층이 정의하고 어댑터는 인프라 층이 구현한다. **정적 타입 언어라 포트를
    짚기 어렵다는 문제가 없고**, 그래서 이 판본에는 그쪽의 덕 타이핑 논의가 없다.
- 저자가 드는 실물이 메시지 버스의 포트와 그 어댑터다 (8장, p.128):[^khononov2021]

  ```csharp
  namespace App.BusinessLogicLayer
  {
      public interface IMessaging
      {
          void Publish(Message payload);
          void Subscribe(Message type, Action callback);
      }
  }

  namespace App.Infrastructure.Adapters
  {
      public class SQSBus: IMessaging { ... }
  }
  ```

  - **네임스페이스가 층을 말한다는 것이 이 목록의 요점이다.** 인터페이스가
    `App.BusinessLogicLayer`에, 구현이 `App.Infrastructure.Adapters`에 있다. 같은 분리를
    폴더로 하는 쪽은 위 [포트와 어댑터가 파이썬에서 무엇인가](#포트와-어댑터가-파이썬에서-무엇인가)의
    마지막 항목에 있다.
- **해소 수단이 둘로 규정된다** (8장, p.128):[^khononov2021]

> The abstract ports are resolved into concrete adapters in the infrastructure layer, either through
> dependency injection or by bootstrapping.

  - 그 둘의 전문이 [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md)에
    있다. **이 판본이 그 둘을 대등한 선택지로 병렬한다는 데 주의한다** — 그쪽 소스는
    부트스트랩 스크립트를 합성 루트(composition root)의 다른 이름으로 다루므로 둘이 배타적
    선택지가 아니다. 대상이 어긋나는 것이 아니라 이 판본이 한 줄로 지나가는 자리다.

## 육각형·양파·클린은 같은 패턴이다

위 [층 구조를 안팎으로 뒤집기 — 양파 구조](#층-구조를-안팎으로-뒤집기--양파-구조)의 마지막
항목이 파이썬 쪽 소스의 곁글을 옮긴다 — 이 이름들이 "거의 같은 것에 대한 이름"이라는 정리다.
**다른 소스가 같은 판정을 더 강한 말로 내린다.**

- 규정 (8장 §Variants, p.128):[^khononov2021]

> The ports & adapters architecture is also known as hexagonal architecture, onion architecture, and
> clean architecture. All of these patterns are based on the same design principles, have the same
> components, and have the same relationships between them, but as in the case of the layered
> architecture, the terminology may differ:

  갈리는 것은 이름뿐이라고 표가 따라온다 (8장, p.128):[^khononov2021]

| 이 판본의 이름 | 다른 데서 쓰는 이름 |
|---|---|
| Application layer | service layer = use case layer |
| Business logic layer | domain layer = core layer |

- 그리고 진단이 붙는다 (8장, p.128):[^khononov2021]

> Despite that, these patterns can be mistakenly treated as conceptually different. That's just
> another example of the importance of a ubiquitous language.

  - **두 소스가 같은 결론에 이르되 근거가 다르다.** 파이썬 쪽은 **전부 의존성 역전 원칙으로
    환원된다**는 것을 근거로 들고, 이 판본은 **설계 원칙·구성 요소·관계가 전부 같다**는 것을
    근거로 든 뒤 그 혼동 자체를 유비쿼터스 언어 문제의 사례로 읽는다. 그 요구는
    [유비쿼터스 언어](ubiquitous-language.md)에 있다.
  - **이 KB는 이 네 이름에 페이지를 따로 세우지 않는다.** 두 소스가 같은 것이라고 적으므로
    이 페이지가 넷을 함께 갖는다.

## 이 아키텍처가 맞는 자리

- 판정 (8장 §"When to Use Ports & Adapters", p.128):[^khononov2021]

> The decoupling of the business logic from all technological concerns makes the ports & adapters
> architecture a perfect fit for business logic implemented with the domain model pattern.

- 장 맺음이 세 아키텍처 패턴의 대응을 한 문단으로 정리하며 같은 판정을 다시 적는다
  (8장 §Conclusion, p.135):[^khononov2021]

> The ports & adapters architecture inverts the relationships: it puts the business logic at the
> center and decouples it from all infrastructural dependencies. This pattern is a good fit for
> business logic implemented with the domain model pattern.

  - 세 패턴과 업무 로직 패턴의 대응표는
    [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md)에 있다.

## 이어지는 페이지

- [추상화 고르기](../concepts/choosing-abstractions.md) — 무엇을 추상으로 삼을지 고르는 발견법
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — 명시적 의존을
  실제로 누가 주입하는가
- [도메인 모델 패턴](domain-model-pattern.md) — 이 원칙이 지키려는 대상
- [결합 끊기](../concepts/decoupling.md) — 같은 목표를 코드 수준 처방으로 말하는 자리
- [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md) — 추상의 값을 인터페이스 크기로
  재는 잣대
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 같은 결합
  판단이 배치 단위로 커지는 자리
- [계층 아키텍처](../concepts/layered-architecture.md) — 이 뒤집기의 출발점이 되는 패턴
- [서비스 레이어](service-layer-pattern.md) — 뒤집은 구조 위에 얹히는 파사드 층
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — 같은 조직 원리 위에서 데이터 관리만 달리하는 패턴
- [업무 로직 구현 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md) — 어느 아키텍처 패턴을
  고를지가 걸리는 입력
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^percival2020]: Percival & Gregory 2020, Introduction("Why Do Our Designs Go Wrong?" ·
    "Encapsulation and Abstractions" · "Layering" · "The Dependency Inversion Principle") ·
    2장 §"Applying the DIP to Data Access"·§"The Repository in the Abstract"·§"What Is a
    Port and What Is an Adapter, in Python?"(곁글 "Is This Ports and Adapters?"·"Abstract
    Base Classes, Duck Typing, and Protocols") · 4장 §"Putting Things in Folders to See
    Where It All Belongs" · 7장 §"Part I Recap" · 13장 §"Aren't Explicit Dependencies
    Totally Weird and Java-y?". **이 소스의 locator는 장 단위다** — 검증 절차와 근거는
    `it/archive/percival2020/_progress.yaml` 머리말이 정본이다. Figure P-2(3층 구조)와
    Figure 2-3(양파 구조)은 이미지지만 원본 ditaa 소스가 본문에 함께 실려 있어 층과 화살표
    방향을 실측으로 판독했다. 이 페이지의 펜스 예산은 인용 블록이 쓰고 있어 코드 펜스는
    두지 않았다 — 이 장들의 코드는 다른 페이지가 대표 조각을 갖는다.

[^khononov2021]: Khononov 2021, 8장 "Architectural Patterns" §"Ports & Adapters"
    (도입 p.125 · §Terminology p.126 · §"Dependency Inversion Principle" p.126과 각주 5 ·
    §"Integration of Infrastructural Components" pp.127–128 · §Variants p.128 ·
    §"When to Use Ports & Adapters" p.128) · §Conclusion p.135. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 인프라 층 인용은 원문이 콤마와 따옴표로 끝나고 도판 참조가
    이어지는 자리라 그 지점까지만 옮겼다. 이름 대응표는 원문이 불릿 목록이고 이 KB가 표로
    옮겼으며 **값은 번역하지 않았다**(층 이름이 검색 키다). 코드 펜스는 포트와 어댑터 한 쌍
    (`IMessaging`과 `SQSBus`)만 두었고 원문 그대로다(언어 표지는 이 KB가 붙였다) —
    원문의 `...`는 저자가 생략을 표시한 것이다. 도판 넷(Figure 8-8~8-11)은 도판이라 본문이
    그것에 대해 적는 것만 산문으로 옮겼다.

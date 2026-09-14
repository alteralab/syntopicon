---
type: concept
title: 서비스 레이어
description: 조율 로직을 담는 층을 따로 두는 판단과 그 대가 — 웹 컨트롤러에 쌓이는 것을 조율(orchestration)이라 이름 붙이고 그것이 웹과 무관하다는 관찰, 전형적인 서비스 함수의 네 단계, 도메인 서비스와 애플리케이션 서비스가 왜 같은 낱말을 쓰는가, 인수를 원시 타입으로 바꿔 서비스 레이어를 도메인에서 완전히 떼는 수순과 그 부작용으로 빠진 서비스가 드러난다는 관찰, 폴더 넷으로 나눈 프로젝트 구조, 그리고 이 층이 빈혈 도메인 안티패턴으로 가는 길이 될 수 있다는 경고
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
status: draft
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 서비스 레이어

- [무엇이 이 층을 부르는가](#무엇이-이-층을-부르는가)
- [E2E 테스트가 늘어나는 것이 신호다](#e2e-테스트가-늘어나는-것이-신호다)
- [전형적인 서비스 함수의 네 단계](#전형적인-서비스-함수의-네-단계)
- [왜 전부 서비스라 부르는가](#왜-전부-서비스라-부르는가)
- [원시 타입으로 인수를 바꾸면 빠진 서비스가 드러난다](#원시-타입으로-인수를-바꾸면-빠진-서비스가-드러난다)
- [DIP의 실물](#dip의-실물)
- [폴더 넷](#폴더-넷)
- [비용 — 빈혈 도메인이라는 반대 방향](#비용--빈혈-도메인이라는-반대-방향)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **웹 핸들러에 쌓이는 잡일을 어디로 옮겨야 하고, 그 층을 두는 것이 무엇을
얻고 무엇을 잃는가.**

## 무엇이 이 층을 부르는가

- 관찰이 이름 붙이기에서 시작한다 — **우리 Flask 앱이 무엇을 하고 있는지 보면 조율
  (orchestration)이라 부를 만한 것이 꽤 많다 — 리포지터리에서 물건을 꺼내고, 데이터베이스
  상태에 대해 입력을 검증하고, 오류를 처리하고, 정상 경로에서 커밋하는 것**
  (4장 §"Introducing a Service Layer, and Using FakeRepository to Unit Test
  It").[^percival2020]
- **그리고 그것이 웹과 무관하다는 것이 결정적이다** — **이 대부분은 웹 API 엔드포인트를
  갖는 것과 아무 상관이 없고(예컨대 CLI를 만들고 있어도 필요할 것이다), 종단 간 테스트로
  테스트되어야 할 것들도 정말 아니다** (4장 §"Introducing a Service
  Layer…").[^percival2020]
- 이름이 여럿이다 — **흔히 서비스 레이어(service layer)를 갈라내는 것이 말이 되는데, 때로는
  조율 레이어(orchestration layer)나 사용 사례 레이어(use-case layer)라고도 불린다**
  (4장 §"Introducing a Service Layer…").[^percival2020]
- 이 장이 구분하는 것 셋이 도입에 있다 — **이 장에서 우리는 조율 로직, 업무 로직, 인터페이싱
  코드의 차이를 논하고, 우리 작업 흐름을 조율하고 시스템의 사용 사례를 정의하는 일을 맡을
  서비스 레이어 패턴을 들인다** (4장 도입).[^percival2020]

## E2E 테스트가 늘어나는 것이 신호다

- 이 장의 서사는 오류 처리가 들어오면서 무너진다. SKU 자체가 존재하지 않는 경우는
  **도메인이 알지도 못하고 알아서도 안 되는 것이다. 도메인 서비스를 부르기도 전에 우리가
  데이터베이스 계층에서 구현해야 할 정상성 검사에 가깝다**
  (4장 §"Error Conditions That Require Database Checks").[^percival2020]
- 그것을 Flask 앱에 넣으면 — **우리 Flask 앱이 좀 다루기 힘들어 보이기 시작한다. 그리고
  우리 E2E 테스트의 수가 통제를 벗어나기 시작하고, 곧 우리는 뒤집힌 테스트 피라미드(Bob이
  즐겨 부르는 "아이스크림 콘 모형")로 끝날 것이다**
  (4장 §"Error Conditions That Require Database Checks").[^percival2020]
- 서비스 레이어를 두고 나면 E2E 테스트가 둘로 준다 — **마지막으로 우리는 E2E 테스트를
  자신 있게 둘로 줄일 수 있다. 정상 경로 하나와 비정상 경로 하나다**
  (4장 §"A Typical Service Function").[^percival2020] 그리고 테스트가 두 범주로 갈린다 —
  **웹 관련 테스트는 종단 간으로 구현하고, 조율 관련 테스트는 서비스 레이어를 상대로
  메모리에서 테스트할 수 있다** (4장 §"A Typical Service Function").[^percival2020]
- 용어 논쟁은 미리 차단된다 — **무엇이 종단 간(E2E) 테스트인지 기능 테스트인지 인수
  테스트인지 통합 테스트인지 단위 테스트인지를 두고 긴 용어 논쟁에 들어가는 데 아무도
  관심이 없다. 프로젝트마다 다른 테스트 조합이 필요하고, 우리는 그냥 "빠른 테스트"와
  "느린 테스트"로 나눈 완벽하게 성공적인 프로젝트들을 봤다**
  (4장 §"A First End-to-End Test").[^percival2020]

## 전형적인 서비스 함수의 네 단계

- 서비스 함수의 골격이 넷으로 규정된다 — **전형적인 서비스 레이어 함수는 비슷한 단계를
  갖는다** (4장 §"A Typical Service Function"):[^percival2020]
  - **리포지터리에서 객체 몇 개를 가져온다.**
  - **현재 세계 상태에 비추어 요청에 대해 검사나 단언을 한다.**
  - **도메인 서비스를 부른다.**
  - **모두 잘되면 우리가 바꾼 상태를 저장·갱신한다.**
- 같은 골격이 에필로그에서 레거시 시스템을 정리하는 절차로 다시 나오고, 거기서는 다섯이
  된다 — 필요하면 **자기 데이터베이스 트랜잭션을 시작**하는 단계가 앞에 붙고
  **선행 조건 검사**가 따로 선다 (Epilogue §"Separating Entangled
  Responsibilities").[^percival2020] 그쪽 전문은
  [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md)에 있다.
- 마지막 단계가 4장 시점에는 불만족스럽다고 저자들이 적는다 — **그 마지막 단계는 지금은
  좀 만족스럽지 않은데, 우리 서비스 레이어가 데이터베이스 계층에 단단히 결합돼 있기
  때문이다. 6장에서 작업 단위 패턴으로 그것을 개선할 것이다**
  (4장 §"A Typical Service Function").[^percival2020]
- 그리고 Flask에 남는 책임이 규정된다 — **Flask 앱의 책임은 그저 표준 웹 관련 잡일이다:
  요청별 세션 관리, POST 매개변수에서 정보 파싱하기, 응답 상태 코드, JSON. 모든 조율
  로직은 사용 사례/서비스 레이어에 있고, 도메인 로직은 도메인에 남는다**
  (4장 §"A Typical Service Function").[^percival2020]

## 왜 전부 서비스라 부르는가

- 저자들이 혼란을 먼저 인정한다 — **미안하다 — 우리가 이름을 고른 것이 아니다. 골랐다면
  이런 것들을 이야기할 훨씬 멋지고 친근한 방법을 가졌을 것이다**
  (4장 §"Why Is Everything Called a Service?").[^percival2020]
- 둘이 갈린다 (4장 §"Why Is Everything Called a Service?"):[^percival2020]
  - **첫째는 애플리케이션 서비스(우리 서비스 레이어)다. 그 일은 바깥세상의 요청을 처리하고
    연산을 조율하는 것이다.** 그 조율은 단순한 단계 몇 개를 따르는 것이다 —
    데이터베이스에서 데이터를 얻고, 도메인 모델을 갱신하고, 변경을 영속시킨다.
    **이것은 당신 시스템의 모든 연산마다 일어나야 하는 지루한 작업이고, 그것을 업무
    로직에서 분리해 두는 것이 일을 정돈되게 유지하는 데 도움이 된다.**
  - **둘째 종류가 도메인 서비스다. 이것은 도메인 모델에 속하지만 상태를 가진 엔티티나 값
    객체 안에 자연스럽게 앉지 않는 로직 조각에 붙는 이름이다.** 예가 장바구니 앱의 과세
    규칙이다 — **세금 계산은 장바구니를 갱신하는 것과 별개의 일이고 모델의 중요한
    부분이지만, 그 일을 위해 영속되는 엔티티를 두는 것은 옳아 보이지 않는다. 대신 상태 없는
    `TaxCalculator` 클래스나 `calculate_tax` 함수가 그 일을 할 수 있다.**

- **도메인 서비스 쪽의 원 규정은 이 소스가 아니라 도메인 주도 설계 쪽 원전에 있다.** 그쪽은
  이 낱말을 **도메인에 실재하는 프로세스를 모델에 명시하는 형태**로 규정한다 — **서비스는 그런
  프로세스를 명시적으로 표현하면서도 극도로 복잡한 알고리즘은 계속 캡슐화하는 한 가지 방법이다**
  (9장, p.223).[^evans2003]
  - 무엇을 서비스로 올리고 무엇을 감출지의 시험도 같은 자리에 있다 — **명시적으로 만들어야 할
    프로세스와 감춰야 할 프로세스를 구별하는 열쇠는 단순하다: 이것은 도메인 전문가가 이야기하는
    것인가, 아니면 그저 컴퓨터 프로그램의 기제의 일부인가?** (9장, p.223).[^evans2003]
  - **위 과세 계산 예와 판정 기준이 다르다.** 그쪽은 **상태를 가진 객체에 자연스럽게 앉는가**를
    묻고, 이쪽은 **도메인이 그것을 말하는가**를 묻는다. 둘은 배타적이지 않고 자주 같은 답을
    내지만, 어긋날 때는 후자가 이 낱말의 원 뜻이다. 전문은
    [도메인 객체가 된 프로세스](processes-as-domain-objects.md)에 있다.

## 원시 타입으로 인수를 바꾸면 빠진 서비스가 드러난다

- 5장이 이 층을 도메인에서 완전히 떼어 낸다. 남은 결합이 지목된다 — **우리 서비스 레이어
  테스트에는 여전히 도메인에 대한 직접 의존이 있는데, 우리가 테스트 데이터를 차리고 서비스
  레이어 함수를 부르는 데 도메인 객체를 쓰기 때문이다. 도메인에서 완전히 결합이 끊긴 서비스
  레이어를 가지려면 그 API를 원시 타입(primitive)으로 작동하도록 다시 써야 한다**
  (5장 §"Fully Decoupling the Service-Layer Tests from the Domain").[^percival2020]
  그래서 `allocate(line: OrderLine, ...)`가
  `allocate(orderid: str, sku: str, qty: int, ...)`가 된다.
- **그것만으로는 부족하다** — **그러나 우리 테스트는 여전히 도메인에 의존하는데, 우리가
  여전히 `Batch` 객체를 손으로 인스턴스화하기 때문이다. 그래서 언젠가 `Batch` 모델이 어떻게
  작동하는지를 대대적으로 리팩터링하기로 결정하면 테스트 뭉치를 바꿔야 할 것이다**
  (5장 §"Fully Decoupling the Service-Layer Tests from the Domain").[^percival2020]
- 완화책은 픽스처로 모으는 것이다 — **적어도 그것이 우리 테스트의 도메인에 대한 의존을
  전부 한 자리로 옮길 것이다** (5장 §"Mitigation: Keep All Domain Dependencies in Fixture
  Functions").[^percival2020]
- **그런데 한 걸음 더 가면 설계 신호가 나온다.** 재고를 더하는 서비스가 있으면 테스트를
  서비스 레이어의 공식 사용 사례만으로 표현할 수 있다 — 그리고 저자들이 그 관찰을 규칙으로
  올린다 — **일반적으로 서비스 레이어 테스트에서 도메인 계층 일을 직접 해야 하는 자신을
  발견한다면, 그것은 당신 서비스 레이어가 불완전하다는 표시일 수 있다**
  (5장 §"Adding a Missing Service").[^percival2020]
- 그러나 남용을 막는 단서가 곧바로 붙는다 — **테스트에서 의존을 없애는 데 도움이 된다는
  이유만으로 새 서비스를 써야 하는가? 아마 아니다. 그러나 이 경우 우리는 언젠가 `add_batch`
  서비스가 어차피 거의 확실히 필요했을 것이다** (5장 §"Adding a Missing
  Service").[^percival2020]
- 그 개선이 E2E 테스트까지 내려간다 — `add_batch` 서비스에 API 엔드포인트를 붙이면
  **하드코딩된 SQL 질의와 데이터베이스에 대한 직접 의존에서 E2E 테스트가 자유로워질 수
  있다** (5장 §"Carrying the Improvement Through to the E2E Tests").[^percival2020]
  - RESTful하지 않다는 자각도 함께 인쇄돼 있다 — **`/add_batch`에 POST라고? 그건 별로
    RESTful하지 않은데! 옳은 말이다. 우리는 행복하게 대충 하고 있다**
    (5장 §"Carrying the Improvement Through to the E2E Tests").[^percival2020]
- 5장의 실무 요약 둘 (5장 §"Wrap-Up"):[^percival2020]
  - **당신 서비스 레이어를 도메인 객체가 아니라 원시 타입의 관점에서 표현하라.**
  - **이상적인 세계에서는 리포지터리나 데이터베이스를 통해 상태를 해킹하는 대신 전적으로
    서비스 레이어를 상대로 테스트할 수 있게 하는 모든 서비스를 갖게 될 것이다. 이것은 당신
    종단 간 테스트에서도 값을 한다.**

## DIP의 실물

- 서비스 함수의 시그니처 한 줄이 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의
  둘째 조항("세부가 추상에 의존한다")에 대한 답이다 — **우리 서비스 레이어 함수에 대해 한
  가지 더 눈여겨보라** (4장 §"Depend on Abstractions" 곁글).[^percival2020]

  ```python
  def allocate(line: OrderLine, repo: AbstractRepository, session) -> str:
  ```

  - 저자들의 해설 — **그것은 리포지터리에 의존한다. 우리는 그 의존을 명시적으로 만들기로
    골랐고, 우리가 `AbstractRepository`에 의존한다고 말하는 데 타입 힌트를 썼다. 이것은
    테스트가 `FakeRepository`를 줄 때도, Flask 앱이 `SqlAlchemyRepository`를 줄 때도
    작동한다는 뜻이다** (4장 §"Depend on Abstractions" 곁글).[^percival2020]
  - 그리고 그것이 원칙의 실물이라고 지목한다 — **"의존성 역전 원칙"을 기억한다면, 이것이
    우리가 "추상에 의존해야 한다"고 말할 때 뜻하는 것이다. 우리 고수준 모듈인 서비스
    레이어가 리포지터리 추상에 의존한다. 그리고 우리가 고른 특정 영속 저장소의 구현 세부도
    같은 추상에 의존한다** (4장 §"Depend on Abstractions" 곁글).[^percival2020]
- 그림 셋이 그 구조를 세 시점으로 보인다 — 서비스 레이어가 도메인 모델과
  `AbstractRepository`(포트)에 의존하는 추상 그림, 테스트가 `FakeRepository`(어댑터)를
  제공하는 그림, 실행 시 `SqlAlchemyRepository`가 꽂히고 그 아래 ORM과 데이터베이스가
  붙는 그림이다 (4장 §"The DIP in Action").[^percival2020]

## 폴더 넷

- 구조가 자란다 — **애플리케이션이 커지면서 우리는 디렉터리 구조를 계속 정돈해야 할 것이다.
  프로젝트의 배치는 각 파일에서 어떤 종류의 객체를 찾을지에 대한 쓸모 있는 힌트를 준다**
  (4장 §"Putting Things in Folders to See Where It All Belongs").[^percival2020]
- 넷의 역할이 각각 규정된다 (4장 §"Putting Things in Folders…"):[^percival2020]
  - **`domain/`** — 도메인 모델. **더 복잡한 애플리케이션이라면 클래스당 파일 하나를 둘
    수도 있고, `Entity`·`ValueObject`·`Aggregate`용 헬퍼 부모 클래스를 둘 수도 있으며,
    도메인 계층 예외를 위한 `exceptions.py`와, 2부에서 보듯 `commands.py`·`events.py`를
    더할 수도 있다.**
  - **`service_layer/`** — 서비스 레이어 함수. **서비스 레이어 예외를 여기 더할 수 있고,
    5장에서 보듯 `unit_of_work.py`를 더할 것이다.**
  - **`adapters/`** — **포트와 어댑터 용어에 대한 인사다. 여기는 외부 I/O 둘레의 다른
    추상들(예컨대 `redis_client.py`)로 채워질 것이다.**
  - **`entrypoints/`** — **우리가 애플리케이션을 구동하는 자리들이다.**
- 부록 B가 이 구조의 완성판을 담고 있다 — `src/` 레이아웃과 설치 가능한 패키지, Dockerfile과
  docker-compose, Makefile, 그리고 단위·통합·E2E로 나뉜 테스트 트리다
  (Appendix B).[^percival2020] 그쪽 요지는
  [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md)에 있다.

## 비용 — 빈혈 도메인이라는 반대 방향

**표 4-1의 내용이다** (4장 §"Wrap-Up"):[^percival2020]

| 이득 | 비용 |
|---|---|
| 애플리케이션의 모든 사용 사례를 담는 한 자리가 생긴다 | 앱이 순전히 웹 앱이라면 컨트롤러·뷰 함수가 모든 사용 사례를 담는 한 자리가 될 수 있다 |
| 영리한 도메인 로직을 API 뒤에 두어 리팩터링이 자유로워진다 | 추상 계층이 하나 더 생긴다 |
| "HTTP를 말하는 것"과 "할당을 말하는 것"을 깔끔히 갈랐다 | 서비스 레이어에 로직을 너무 많이 넣으면 빈혈 도메인(Anemic Domain) 안티패턴으로 이어질 수 있다. 컨트롤러에 조율 로직이 스며드는 것을 발견한 뒤에 이 층을 들이는 편이 낫다 |
| 리포지터리 패턴·`FakeRepository`와 결합하면 도메인 계층보다 높은 수준에서 테스트를 쓰는 좋은 방법이 생긴다 — 통합 테스트를 쓰지 않고도 작업 흐름을 더 많이 테스트할 수 있다 | 컨트롤러에서 모델 계층으로 로직을 밀어 내리는 것만으로도 풍부한 도메인 모델의 이득을 많이 얻을 수 있다(이른바 "뚱뚱한 모델, 얇은 컨트롤러") |

- **비용 칸의 첫째와 마지막이 같은 말을 한다** — 이 층 없이도 되는 경우가 있다는 것.
  그리고 셋째가 이 층 고유의 위험을 짚는다: 도메인이 데이터 홀더로 전락하는 것. 저자들이
  주는 순서 규칙("컨트롤러에 조율 로직이 스며드는 것을 발견한 뒤에")이 이 위험에 대한
  유일한 처방이다.
- 이 형식이 이 책의 서명이다 —
  [리포지터리 패턴](../concepts/repository-pattern.md)·[작업 단위 패턴](unit-of-work-pattern.md)·
  [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)가 전부 같은
  장단점 표로 끝난다.
- 4장이 남긴 어색함 둘도 명시돼 있다 (4장 §"Wrap-Up"):[^percival2020]
  - **서비스 레이어가 여전히 도메인에 단단히 결합돼 있는데, 그 API가 `OrderLine` 객체의
    관점에서 표현되기 때문이다.** → 5장에서 해소.
  - **서비스 레이어가 세션 객체에 단단히 결합돼 있다.** → 6장에서 해소.

## 이어지는 페이지

- [작업 단위 패턴](unit-of-work-pattern.md) — 이 층의 마지막 결합을 끊는 패턴
- [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md) — 이 층이 생기고 나서
  테스트를 어느 수준에 둘 것인가
- [리포지터리 패턴](../concepts/repository-pattern.md) — 이 층이 의존하는 추상
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 이 층이 부르는 대상
- [도메인 객체가 된 프로세스](processes-as-domain-objects.md) — 도메인 서비스라는 낱말의 원 규정
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 층의 시그니처가 구현하는 원리
- [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md) — 레거시에서
  이 층을 먼저 만들라는 권고
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^percival2020]: Percival & Gregory 2020, 4장 "Our First Use Case: Flask API and Service
    Layer" 전체(곁글 "Depend on Abstractions" 포함) · 5장 §"Fully Decoupling the
    Service-Layer Tests from the Domain"·§"Mitigation: Keep All Domain Dependencies in
    Fixture Functions"·§"Adding a Missing Service"·§"Carrying the Improvement Through to
    the E2E Tests"·§"Wrap-Up" · Appendix B "A Template Project Structure" ·
    Epilogue §"Separating Entangled Responsibilities". **이 소스의 locator는 장 단위다** —
    검증 절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이 정본이다.
    표 4-1은 원문이 장단점 목록 두 개를 나란히 둔 것을 표로 옮겼다. Figure 4-3~4-5는
    이미지지만 ditaa 소스가 본문에 함께 실려 있어 의존 방향을 실측했다. 코드 펜스는
    대표 하나(추상에 의존하는 서비스 함수 시그니처)만 두었다.

[^evans2003]: Evans 2003, 9장 "Making Implicit Concepts Explicit" §"Processes as Domain
    Objects"(p.223). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은
    대문자로 조판하는 관례를 직인용에서 유지했다. 이 소스의 SERVICE 패턴 원 정의는 5장에
    있고, 이 페이지가 든 것은 9장이 그 패턴을 프로세스 표현의 형태로 부르는 대목뿐이다. 이 소스에서 온 코드 펜스는 이 페이지에 없다.

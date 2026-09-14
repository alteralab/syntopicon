---
type: concept
title: 작업 단위 패턴
description: 원자적 연산 위에 씌우는 추상과 그것을 파이썬 컨텍스트 매니저로 표현하는 판단 — 리포지터리와 서비스 레이어를 잇는 마지막 조각이라는 자리매김, UoW가 주는 세 가지(안정된 스냅샷·한꺼번에 영속·리포지터리를 얻는 자리), with 블록이 원자 구간을 눈에 보이게 만든다는 이득, 명시적 커밋과 암묵적 커밋 중 명시를 고르는 이유와 기본값이 안전해야 한다는 논리, ORM이 이미 같은 패턴을 갖고 있는데도 한 겹을 더 씌우는 이유, 커밋을 리포지터리 밖에 두는 결정의 원전 근거(맥락을 가진 쪽이 경계를 긋는다), 그리고 이 패턴의 대가
generated: { by: "claude-opus-5", at: "2026-09-14T09:00:00Z" }
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 작업 단위 패턴

- [무엇을 추상하는가](#무엇을-추상하는가)
- [UoW가 주는 세 가지](#uow가-주는-세-가지)
- [컨텍스트 매니저라는 선택](#컨텍스트-매니저라는-선택)
- [명시적 커밋과 암묵적 커밋](#명시적-커밋과-암묵적-커밋)
- [원자 단위로 묶는다는 것의 실물](#원자-단위로-묶는다는-것의-실물)
- [ORM이 이미 갖고 있는데 왜 또 씌우는가](#orm이-이미-갖고-있는데-왜-또-씌우는가)
- [커밋을 클라이언트에 남기는 이유 — 원전](#커밋을-클라이언트에-남기는-이유--원전)
- [비용 — 저자들이 계상한 표](#비용--저자들이-계상한-표)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **여러 변경을 함께 성공하거나 함께 실패하게 묶는 일을 어느 층이 맡고, 그
경계를 코드에서 어떻게 눈에 보이게 만드는가.**

## 무엇을 추상하는가

- 정의가 리포지터리와의 대구로 나온다 — **리포지터리 패턴이 영속 저장소라는 발상에 대한
  우리 추상이라면, 작업 단위(UoW) 패턴은 원자적 연산이라는 발상에 대한 우리 추상이다.
  그것은 마침내, 그리고 온전히 우리 서비스 레이어를 데이터 계층에서 떼어 내게 해 줄
  것이다** (6장 도입).[^percival2020]
- 해결하는 문제가 층간 통신량이다 — **현재 우리 인프라의 층들 사이에 많은 통신이 일어난다:
  API가 세션을 시작하려고 데이터베이스 계층과 직접 이야기하고, `SqlAlchemyRepository`를
  초기화하려고 리포지터리 계층과 이야기하고, 할당을 요청하려고 서비스 레이어와 이야기한다**
  (6장 도입).[^percival2020]
- 목표 상태 — **Flask API는 이제 두 가지만 한다: 작업 단위를 초기화하고 서비스를 부른다.
  서비스는 UoW와 협력하지만(우리는 UoW를 서비스 레이어의 일부로 생각하기를 좋아한다),
  서비스 함수 자신도 Flask도 이제 데이터베이스와 직접 이야기할 필요가 없다**
  (6장 도입).[^percival2020]
- 발음까지 적혀 있다 — **작업 단위(또는 UoW, 우리는 "유-와우"라고 발음한다)**
  (6장 §"The Unit of Work Collaborates with the Repository").[^percival2020]

## UoW가 주는 세 가지

- 역할 — **UoW는 우리 영속 저장소에 대한 단일 진입점으로 작용하며, 어떤 객체가 적재됐고
  최신 상태가 무엇인지를 추적한다** (6장 §"The Unit of Work Collaborates with the
  Repository").[^percival2020]
- 이득 셋 (6장 §"The Unit of Work Collaborates with the Repository"):[^percival2020]
  - **작업할 데이터베이스의 안정된 스냅샷. 그래서 우리가 쓰는 객체들이 연산 도중에
    바뀌지 않는다.**
  - **모든 변경을 한 번에 영속시키는 방법. 그래서 무언가 잘못되면 우리가 일관되지 않은
    상태에 빠지지 않는다.**
  - **영속성 관심사에 대한 단순한 API와 리포지터리를 얻는 편리한 자리.**
- 저자들이 각주에서 협력자라는 낱말을 소개한다 — **목표를 이루려고 함께 작동하는 객체들을
  서술하는 데 협력자(collaborators)라는 낱말이 쓰이는 것을 접했을 것이다. 작업 단위와
  리포지터리는 객체 모델링의 뜻에서 협력자의 훌륭한 예다. 책임 주도 설계에서 자기 역할
  안에서 협력하는 객체 무리를 객체 이웃(object neighborhoods)이라 부르는데, 우리의
  전문가적 견해로는 전적으로 사랑스럽다** (6장 각주 1).[^percival2020]

## 컨텍스트 매니저라는 선택

- 파이썬 문법이 이 패턴의 표현 수단으로 지목된다 — **그리고 우리는 그것을 전부 사랑스러운
  파이썬 문법 한 조각, 컨텍스트 매니저(context manager)를 써서 할 것이다**
  (6장 도입).[^percival2020]
- 추상 UoW가 그 계약을 명시한다 — **컨텍스트 매니저를 본 적이 없다면, `__enter__`와
  `__exit__`는 우리가 `with` 블록에 들어갈 때와 나올 때 각각 실행되는 두 매직 메서드다.
  그것들이 우리의 설정과 해체 국면이다**
  (6장 §"Unit of Work and Its Context Manager").[^percival2020]
- 기본 동작이 롤백이다 — **커밋하지 않거나 오류를 일으켜 컨텍스트 매니저를 빠져나가면
  우리는 롤백을 한다. (`commit()`이 호출됐다면 그 롤백은 아무 효과가 없다.)**
  (6장 §"Unit of Work and Its Context Manager").[^percival2020]
- 서비스 레이어에서의 쓰임이 이 패턴의 대표 조각이다 — **다 끝났을 때 서비스 레이어가
  어떤 모습일지 미리 보자** (6장 §"The Unit of Work Collaborates with the
  Repository").[^percival2020]

  ```python
  def allocate(
      orderid: str, sku: str, qty: int,
      uow: unit_of_work.AbstractUnitOfWork
  ) -> str:
      line = OrderLine(orderid, sku, qty)
      with uow:
          batches = uow.batches.list()
          ...
          batchref = model.allocate(line, batches)
          uow.commit()
  ```

  - 세 줄이 각각 규정돼 있다 — **우리는 UoW를 컨텍스트 매니저로 시작할 것이다** /
    **`uow.batches`가 배치 리포지터리이므로 UoW가 우리에게 영속 저장소 접근을 제공한다** /
    **끝나면 우리는 UoW를 써서 작업을 커밋하거나 되돌린다**
    (6장 §"The Unit of Work Collaborates with the Repository").[^percival2020]
  - 그 결과 서비스 레이어의 의존이 하나로 준다 — **우리 서비스 레이어는 이제 오직 하나의
    의존만 갖는데, 다시 한번 추상 UoW에 대한 것이다**
    (6장 §"Using the UoW in the Service Layer").[^percival2020]
- 구체 구현이 세션을 더한다 — **`__enter__` 메서드는 데이터베이스 세션을 시작하고 그
  세션을 쓸 수 있는 실제 리포지터리를 인스턴스화할 책임을 진다**
  (6장 §"The Real Unit of Work Uses SQLAlchemy Sessions").[^percival2020] 그리고
  기본 세션 팩토리를 덮어쓸 수 있게 둔 것이 통합 테스트에서 SQLite를 쓰기 위해서다 —
  **모듈은 Postgres에 연결할 기본 세션 팩토리를 정의하지만, 우리는 통합 테스트에서 SQLite를
  쓸 수 있도록 그것을 덮어쓰는 것을 허용한다**
  (6장 §"The Real Unit of Work Uses SQLAlchemy Sessions").[^percival2020]

## 명시적 커밋과 암묵적 커밋

- 대안이 제시된다 — 예외를 보면 롤백하고 아니면 커밋하는 UoW를 상상할 수 있고, 그러면
  클라이언트 코드에서 `uow.commit()` 한 줄을 뺄 수 있다
  (6장 §"Explicit Versus Implicit Commits").[^percival2020]
- **그런데 저자들은 명시를 고른다** — **이것은 판단의 문제지만, 우리는 언제 상태를 내보낼지
  우리가 골라야 하도록 명시적 커밋을 요구하는 편을 선호하는 경향이 있다**
  (6장 §"Explicit Versus Implicit Commits").[^percival2020]
- 근거가 "기본값의 안전성"이다 — **우리가 코드 한 줄을 더 쓰지만, 이것이 소프트웨어를
  기본적으로 안전하게(safe by default) 만든다. 기본 행동은 아무것도 바꾸지 않는 것이다.
  결과적으로 그것이 우리 코드를 추론하기 더 쉽게 만드는데, 시스템의 변경으로 이어지는 코드
  경로가 딱 하나 — 전면적 성공과 명시적 커밋 — 뿐이기 때문이다. 다른 어떤 코드 경로든,
  어떤 예외든, UoW 범위에서의 어떤 조기 탈출이든 안전한 상태로 이어진다**
  (6장 §"Explicit Versus Implicit Commits").[^percival2020]
- 롤백 기본값의 근거는 다르다 — **비슷하게 우리는 이해하기 더 쉽기 때문에 기본적으로
  롤백하는 편을 선호한다; 이것은 마지막 커밋으로 되돌리므로, 사용자가 커밋을 했거나 아니면
  우리가 그의 변경을 날려 버린다. 가혹하지만 단순하다**
  (6장 §"Explicit Versus Implicit Commits").[^percival2020]
  - **두 기본값의 근거가 다르다는 점이 이 절의 값이다** — 커밋 쪽은 안전, 롤백 쪽은
    이해 가능성. 같은 결정에 이유가 하나가 아니다.
- 그 행동을 실제로 확인하는 통합 테스트가 둘 있다 — 커밋하지 않은 작업이 기본으로
  되돌려지는지, 그리고 예외가 나면 되돌려지는지
  (6장 §"Explicit Tests for Commit/Rollback Behavior").[^percival2020] 저자들이 여기에
  단서를 단다 — **여기 보이지는 않았지만 트랜잭션 같은 더 "모호한" 데이터베이스 행동은
  "실제" 데이터베이스 — 즉 같은 엔진 — 를 상대로 테스트할 값어치가 있을 수 있다**
  (6장 §"Explicit Tests for Commit/Rollback Behavior").[^percival2020]

## 원자 단위로 묶는다는 것의 실물

- 저자들이 두 예를 든다. 재할당은 순서 의존이다 — **`deallocate()`가 실패하면 우리는 분명히
  `allocate()`를 부르고 싶지 않다** 그리고 **`allocate()`가 실패하면 우리는 아마
  `deallocate()`도 실제로 커밋하고 싶지 않다**
  (6장 §"Example 1: Reallocate").[^percival2020]
- 배치 수량 변경은 반복 횟수가 미정이다 — 컨테이너 문이 열려 소파 절반이 인도양에 빠진
  상황에서 수량을 줄이면 초과 할당된 라인을 여러 개 떼어 내야 한다 — **여기서 우리는 임의
  개수의 라인을 할당 해제해야 할 수 있다. 어느 단계에서든 실패하면 우리는 아마 변경 중
  어느 것도 커밋하고 싶지 않다** (6장 §"Example 2: Change Batch Quantity").[^percival2020]
- 그리고 이 패턴이 뒤에 값을 한다 — **뒤 장들에서 보겠지만, 원자성은 트랜잭션만의 문제가
  아니다; 그것은 우리가 이벤트와 메시지 버스로 작업하는 데 도움을 줄 수 있다**
  (6장 §"Wrap-Up").[^percival2020] 실제로 8장에서 UoW가 커밋 뒤 이벤트를 발행하는 자리가
  되고, 그 전문은
  [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md)에 있다.

## ORM이 이미 갖고 있는데 왜 또 씌우는가

- 사실이 먼저 인정된다 — **이 패턴은 사실 아주 유용해서 SQLAlchemy가 이미 `Session` 객체의
  모양으로 UoW를 쓰고 있다. SQLAlchemy의 `Session` 객체는 당신 애플리케이션이 데이터베이스에서
  데이터를 적재하는 방식이다** (6장 §"Wrap-Up").[^percival2020] 그리고 그 작동도 같다 —
  **데이터베이스에서 새 엔티티를 적재할 때마다 세션은 그 엔티티의 변경을 추적하기 시작하고,
  세션이 플러시될 때 당신의 모든 변경이 함께 영속된다** (6장 §"Wrap-Up").[^percival2020]
- 그런데도 한 겹을 씌우는 이유가 둘이다 (6장 §"Wrap-Up"):[^percival2020]
  - **하나는, `Session` API가 풍부하고 우리 도메인에서 우리가 원하거나 필요로 하지 않는
    연산을 지원한다는 것이다. 우리 `UnitOfWork`는 세션을 그 본질적 핵심으로 단순화한다:
    그것은 시작되고, 커밋되고, 버려질 수 있다.**
  - **다른 하나는, 우리가 `UnitOfWork`를 써서 우리 `Repository` 객체에 접근한다는 것이다.
    이것은 평범한 SQLAlchemy `Session`으로는 할 수 없었을 깔끔한 개발자 사용성이다.**
- 그리고 이 결정이 원리로 되돌아간다 — **마지막으로 우리는 다시 한번 의존성 역전 원칙에
  의해 동기를 얻는다: 우리 서비스 레이어가 얇은 추상에 의존하고, 우리는 시스템의 바깥
  가장자리에 구체 구현을 붙인다** (6장 §"Wrap-Up").[^percival2020]
- **SQLAlchemy 자신의 권고와 일치한다고 저자들이 인용한다** (6장 §"Wrap-Up"):[^percival2020]

  > Keep the life cycle of the session (and usually the transaction) separate and external.
  > The most comprehensive approach, recommended for more substantial applications, will try
  > to keep the details of session, transaction, and exception management as far as possible
  > from the details of the program doing its work.
  >
  > — SQLAlchemy "Session Basics" Documentation

  - 버전 조건: SQLAlchemy 1.x. 이 책의 코드는 `sessionmaker`·`create_engine`·
    `session.query()`를 쓰며 2.0에서 바뀐 API는 반영돼 있지 않다.

## 커밋을 클라이언트에 남기는 이유 — 원전

이 패턴이 존재할 수 있는 전제가 하나 있다. **리포지터리(REPOSITORY)가 스스로 커밋하지
않는다**는 것이다. 그 결정의 근거가 도메인 주도 설계 쪽 원전에 한 줄로 있다.

- 리포지터리 구현에서 붙들 것 셋 중 하나가 이것이다 — **트랜잭션 통제는 클라이언트에게
  남겨라. 리포지터리가 데이터베이스에 삽입하고 삭제하기는 하지만 보통 아무것도 커밋하지 않을
  것이다** (6장, p.156).[^evans2003]
- 근거는 **맥락의 소재**다 — **예컨대 저장한 뒤 커밋하고 싶은 유혹이 있지만, 클라이언트가 작업
  단위(units of work)를 올바르게 시작하고 커밋할 맥락을 갖고 있으리라 추정된다. 리포지터리가
  손을 대지 않으면 트랜잭션 관리가 더 단순해질 것이다** (6장, p.156).[^evans2003]
  - **원전이 이미 "작업 단위"라는 낱말을 쓰고 있다는 점이 이 인용의 값이다.** 위
    [무엇을 추상하는가](#무엇을-추상하는가)가 이 패턴을 리포지터리의 짝으로 세우는데, 그 짝
    관계는 파이썬 쪽 소스가 발명한 것이 아니라 리포지터리 조항 안에 이미 비워 둔 자리다.
  - 파이썬 쪽 소스가 같은 결정을 [리포지터리 패턴](../concepts/repository-pattern.md)에서
    내린다 — **우리는 `.commit()`을 리포지터리 밖에 두고 그것을 호출자의 책임으로
    만든다.**[^percival2020] 두 소스의 근거가 같다: 경계를 아는 쪽이 경계를 긋는다.
- 커밋을 리포지터리가 하지 않는 대신 **리포지터리는 바꿀 자유를 얻는다** — 클라이언트가 기제를
  직접 부르는 경우보다 구현을 바꿀 여지가 넓어져 **질의 기법을 달리하거나 객체를 메모리에
  캐시하거나 영속성 전략을 아무 때나 바꿔 성능을 최적화할 수 있다** (6장,
  p.156).[^evans2003] 전문은
  [리포지터리의 질의와 구현](../concepts/repository-querying-and-implementation.md)에 있다.

## 비용 — 저자들이 계상한 표

**표 6-1의 내용이다** (6장 §"Wrap-Up"):[^percival2020]

| 이득 | 비용 |
|---|---|
| 원자적 연산이라는 개념 위의 좋은 추상이 생기고, 컨텍스트 매니저가 어느 코드 블록이 원자적으로 묶였는지 눈으로 보게 해 준다 | 당신 ORM이 이미 원자성 둘레에 아마 완벽하게 좋은 추상을 갖고 있다. SQLAlchemy에는 컨텍스트 매니저까지 있다. 세션을 여기저기 넘기는 것만으로도 꽤 멀리 갈 수 있다 |
| 트랜잭션이 언제 시작되고 끝나는지 명시적으로 통제하고, 애플리케이션이 기본적으로 안전한 방식으로 실패한다. 연산이 부분적으로 커밋될까 걱정할 필요가 전혀 없다 | 우리가 쉬워 보이게 만들었지만, 롤백·멀티스레딩·중첩 트랜잭션 같은 것을 꽤 신중히 생각해야 한다. 그냥 Django나 Flask-SQLAlchemy가 주는 것에 머무르는 편이 삶을 더 단순하게 할지 모른다 |
| 클라이언트 코드가 접근할 수 있게 모든 리포지터리를 두기 좋은 자리다 | |
| 원자성은 트랜잭션만의 문제가 아니다 — 이벤트와 메시지 버스로 작업하는 데도 도움이 된다 | |

- 곁글 요약이 이 패턴의 네 문장이다 (6장 §"Unit of Work Pattern Recap"
  곁글):[^percival2020]
  - **작업 단위 패턴은 데이터 무결성 둘레의 추상이다.** **연산 끝에 단 한 번의 플러시
    연산을 수행하게 해 줌으로써 도메인 모델의 일관성을 강제하는 데 도움을 주고 성능을
    개선한다.**
  - **그것은 리포지터리 및 서비스 레이어 패턴과 밀접하게 작동한다.** **각 서비스 레이어
    사용 사례는 한 덩어리로 성공하거나 실패하는 하나의 작업 단위에서 돈다.**
  - **이것은 컨텍스트 매니저의 사랑스러운 사례다.** **컨텍스트 매니저는 파이썬에서 범위를
    정의하는 관용적 방법이다.**
  - **SQLAlchemy가 이미 이 패턴을 구현한다.** **우리는 ORM과 우리 코드 사이의 인터페이스를
    "좁히려고" SQLAlchemy `Session` 객체 위에 더 단순한 추상을 하나 더 들인다. 이것이
    우리를 느슨하게 결합된 채로 유지하는 데 도움을 준다.**
  - **"인터페이스를 좁힌다"는 표현이 [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)의
    깊이 정의와 정확히 같은 잣대다** — 기능은 그대로 두고 인터페이스만 줄이면 모듈이
    깊어진다. #hypothesis 두 소스가 서로를 참조한 적은 없다.

## 이어지는 페이지

- [리포지터리 패턴](../concepts/repository-pattern.md) — UoW가 담고 있는 것
- [리포지터리의 질의와 구현](../concepts/repository-querying-and-implementation.md) — 커밋을
  넘겨준 쪽이 대신 얻는 자유
- [서비스 레이어](../concepts/service-layer-pattern.md) — UoW를 여닫는 층
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 한 UoW 안에서
  무엇을 바꿔야 하는가의 규칙
- [가짜와 목](../concepts/fakes-versus-mocks.md) — 세션 대신 UoW를 가짜로 만드는 이유
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 구현하는 원리
- [데이터베이스 트랜잭션](../synthesis/database-transactions.md) — 이 추상이 감싸는
  아래층(원자성·격리 수준)의 축
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^percival2020]: Percival & Gregory 2020, 6장 "Unit of Work Pattern" 전체(곁글 "Don't Mock
    What You Don't Own"·"Unit of Work Pattern Recap" 포함). **이 소스의 locator는 장
    단위다** — 검증 절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이
    정본이다. 표 6-1은 원문이 장단점 목록 두 개를 나란히 둔 것을 표로 옮겼고 행 수가 달라
    마지막 두 칸이 빈다. Figure 6-1·6-2(UoW 도입 전후의 층간 통신)는 이미지라 산문
    서술로만 옮겼다. 코드 펜스는 대표 하나(서비스 레이어에서의 `with uow:` 블록)만
    두었고, 원문에서 조판용 번호 표지 이미지를 제거했다 — 생략 부호 `...`는 원문 그대로다.

[^evans2003]: Evans 2003, 6장 "The Life Cycle of a Domain Object" §REPOSITORIES 중
    §"Implementing a REPOSITORY"(p.156). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이
    패턴 이름을 작은 대문자로 조판하는 관례를 직인용에서 유지했다. **이 소스에서는 이
    페이지에 걸리는 조항 하나만 들었다** — 리포지터리 구현의 나머지와 질의 인터페이스 설계는
    [리포지터리의 질의와 구현](../concepts/repository-querying-and-implementation.md)에 있다.
    이 소스에서 온 코드 펜스는 이 페이지에 없다.

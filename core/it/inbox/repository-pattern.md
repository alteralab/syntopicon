---
type: concept
title: 리포지터리 패턴
description: 영속 저장소 위에 씌우는 단순화 추상 — 데이터가 전부 메모리에 있는 척한다는 규정과 add·get 두 메서드뿐인 최소 인터페이스, ORM이 주는 영속성 무지와 그것으로는 부족한 이유, 선언적 매핑 대신 고전적 매퍼로 ORM이 모델을 임포트하게 뒤집는 수순, 자기 부과한 단순함이 결합을 막는다는 논리, 집합 하나로 끝나는 가짜 리포지터리와 "가짜로 만들기 어려우면 추상이 너무 복잡하다"는 설계 피드백, 이 패턴의 비용을 저자들이 계상한 표, 그리고 메모리 안 컬렉션의 착시를 조문으로 둔 원 정의와 그 이득 넷
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 리포지터리 패턴

- [무엇을 추상하는가](#무엇을-추상하는가)
- [ORM이 주는 것과 주지 못하는 것](#orm이-주는-것과-주지-못하는-것)
- [의존을 뒤집기 — 고전적 매퍼](#의존을-뒤집기--고전적-매퍼)
- [가장 단순한 리포지터리](#가장-단순한-리포지터리)
- [자기 부과한 단순함이 결합을 막는다](#자기-부과한-단순함이-결합을-막는다)
- [가짜 리포지터리와 설계 피드백](#가짜-리포지터리와-설계-피드백)
- [테스트를 버릴 때와 남길 때](#테스트를-버릴-때와-남길-때)
- [비용 — 저자들이 계상한 표](#비용--저자들이-계상한-표)
- [이 패턴의 원 정의](#이-패턴의-원-정의)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인 모델이 데이터베이스를 모른 채로 저장되고 되살아나게 하려면 그 사이에
무엇을 놓는가.**

## 무엇을 추상하는가

- 정의 — **리포지터리 패턴은 영속 저장소 위의 추상이다. 그것은 우리 데이터가 전부 메모리에
  있는 척함으로써 데이터 접근의 지루한 세부를 감춘다**
  (2장 §"Introducing the Repository Pattern").[^percival2020]
- 발상의 출발이 반사실이다 — **우리 노트북에 무한한 메모리가 있다면 우리에게 굼뜬
  데이터베이스는 필요 없을 것이다. 대신 우리는 그저 원할 때마다 우리 객체를 쓸 수 있을
  것이다** (2장 §"Introducing the Repository Pattern").[^percival2020] 그 세계의 코드는
  `all_my_data.batches.add(batch)`와 `all_my_data.batches.get(batch_id)`이고 —
  **객체가 메모리에 있으므로 우리는 `.save()` 메서드를 부를 필요가 전혀 없다; 우리는 그저
  신경 쓰는 객체를 가져와 메모리에서 수정한다**
  (2장 §"Introducing the Repository Pattern").[^percival2020]
- 이 장이 여는 자리도 명시된다 — **의존성 역전 원칙을 우리 핵심 로직을 인프라 관심사에서
  떼어 내는 방법으로 쓰겠다는 약속을 지킬 때다** (2장 도입).[^percival2020]

## ORM이 주는 것과 주지 못하는 것

- ORM이 무엇인지부터 규정된다 — **이 프레임워크들은 객체 관계 매퍼(ORM)라 불리는데,
  객체와 도메인 모델링의 세계와 데이터베이스와 관계 대수의 세계 사이의 개념적 간극을
  메우려고 존재하기 때문이다** (2장 §"The 'Normal' ORM Way: Model Depends on
  ORM").[^percival2020]
- 그것이 주는 것 — **ORM이 우리에게 주는 가장 중요한 것은 영속성 무지(persistence
  ignorance)다: 우리의 멋진 도메인 모델이 데이터가 어떻게 적재되고 영속되는지에 대해
  아무것도 알 필요가 없다는 발상이다. 이것이 우리 도메인을 특정 데이터베이스 기술에 대한
  직접 의존에서 깨끗하게 유지하는 데 도움을 준다**
  (2장 §"The 'Normal' ORM Way: Model Depends on ORM").[^percival2020]
  - 그리고 저자들이 각주에서 ORM 자체를 DIP의 예로 인정한다 — **이런 뜻에서 ORM을 쓰는
    것은 이미 DIP의 한 예다. 하드코딩된 SQL에 의존하는 대신 우리는 추상, 즉 ORM에
    의존한다. 그러나 그것은 우리에게 충분하지 않다 — 이 책에서는 아니다!**
    (2장 각주 3).[^percival2020]
- **그런데 표준 튜토리얼을 따르면 의존이 반대로 걸린다.** SQLAlchemy의 "선언적"
  문법에서는 모델 클래스가 `Base`를 상속하고 속성이 `Column`이 된다 — **SQLAlchemy를
  이해할 필요 없이도 우리의 티 없던 모델이 이제 ORM에 대한 의존으로 가득 차고 게다가
  지독하게 못생겨 보이기 시작했다는 것을 알 수 있다. 이 모델이 데이터베이스를 모른다고
  정말 말할 수 있는가? 우리 모델 속성이 데이터베이스 열과 직접 결합돼 있는데 어떻게 저장
  관심사에서 분리될 수 있는가?**
  (2장 §"The 'Normal' ORM Way: Model Depends on ORM").[^percival2020]
- Django도 같다 — **요점은 같다 — 우리 모델 클래스가 ORM 클래스에서 직접 상속하므로 우리
  모델이 ORM에 의존한다. 우리는 그 반대이기를 원한다**
  (2장 §"Django's ORM Is Essentially the Same, but More Restrictive" 곁글).[^percival2020]
  - 버전 조건: Django에는 SQLAlchemy의 고전적 매퍼에 해당하는 것이 없다고 저자들이
    적는다 — **Django는 SQLAlchemy의 고전적 매퍼에 해당하는 것을 제공하지 않지만,
    Django에 의존성 역전과 리포지터리 패턴을 적용하는 예는 부록 D를 보라**
    (2장 곁글).[^percival2020]

## 의존을 뒤집기 — 고전적 매퍼

- 대안이 있다 — **대안은 스키마를 따로 정의하고, 스키마와 우리 도메인 모델 사이를 변환하는
  방법을 명시적 매퍼로 정의하는 것인데, SQLAlchemy는 이것을 고전적 매핑(classical
  mapping)이라 부른다** (2장 §"Inverting the Dependency: ORM Depends on
  Model").[^percival2020]
- 뒤집힌 결과가 임포트 방향에 그대로 보인다 — **ORM이 도메인 모델을 임포트한다(또는
  "의존한다" 또는 "알고 있다"). 그 반대가 아니다**
  (2장 §"Inverting the Dependency: ORM Depends on Model").[^percival2020]
- 그리고 이 방식의 결정적 성질 — **최종 결과는 `start_mappers`를 부르면 도메인 모델
  인스턴스를 데이터베이스에서 쉽게 적재하고 저장할 수 있다는 것이다. 그러나 그 함수를 절대
  부르지 않으면 우리 도메인 모델 클래스들은 데이터베이스를 전혀 모르는 채로 행복하게
  남는다** (2장 §"Inverting the Dependency: ORM Depends on Model").[^percival2020]
  - 이 성질이 뒤에 값을 한다. 13장의 부트스트랩 스크립트에서 `start_orm` 인수로
    ORM 시작 여부를 켜고 끄는 것이 그 예다 —
    [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md)에 있다.
- 완전한 승리가 아니라는 단서도 붙는다 — **도메인 모델에서 무엇을 하고 있는가에 따라,
  특히 OO 패러다임에서 멀리 벗어난다면, ORM이 필요한 정확한 행동을 내게 만들기가 점점
  어려워질 수 있고 도메인 모델을 수정해야 할 수도 있다. 아키텍처 결정에서 흔히 그렇듯
  절충을 고려해야 할 것이다. 파이썬 젠이 말하듯 "실용성이 순수함을 이긴다!"**
  (2장 §"Inverting the Dependency: ORM Depends on Model").[^percival2020]

## 가장 단순한 리포지터리

- 인터페이스가 둘로 시작한다 — **가장 단순한 리포지터리는 딱 두 메서드를 갖는다:
  리포지터리에 새 항목을 넣는 `add()`와 앞서 넣은 항목을 돌려주는 `get()`이다**
  (2장 §"The Repository in the Abstract").[^percival2020]

  ```python
  class AbstractRepository(abc.ABC):

      @abc.abstractmethod
      def add(self, batch: model.Batch):
          raise NotImplementedError

      @abc.abstractmethod
      def get(self, reference) -> model.Batch:
          raise NotImplementedError
  ```

- `list`·`delete`·`update`가 없는 이유가 각주에 있다 — **"list나 delete나 update는?"이라고
  생각할지 모른다. 그러나 이상적인 세계에서 우리는 모델 객체를 한 번에 하나씩 수정하고,
  delete는 보통 소프트 삭제로 처리된다 — 즉 `batch.cancel()`. 마지막으로 update는
  6장에서 보게 될 작업 단위 패턴이 처리한다** (2장 각주 6).[^percival2020]
- 커밋을 리포지터리 밖에 두는 것도 명시적 결정이다 — **우리는 `.commit()`을 리포지터리
  밖에 두고 그것을 호출자의 책임으로 만든다. 여기에는 장단점이 있다**
  (2장 §"The Repository in the Abstract").[^percival2020] 그 결정의 회수 지점이
  [작업 단위 패턴](unit-of-work-pattern.md)이다.

## 자기 부과한 단순함이 결합을 막는다

- 이 패턴의 실제 작동 기제가 이 한 문장이다 — **우리는 우리 도메인과 서비스 레이어에서
  데이터 접근에 이 메서드들만 쓰는 것을 엄격히 고수한다. 이 자기 부과한 단순함(self-imposed
  simplicity)이 우리가 도메인 모델을 데이터베이스에 결합시키는 것을 막는다**
  (2장 §"The Repository in the Abstract").[^percival2020]
  - **패턴이 결합을 막는 것이 아니라 규율이 막는다.** 같은 자리에서 저자들이 다른 방식으로
    말한 것이 6장의 "가진 적 없는 것을 목하지 마라" 곁글이다 — 세션 인터페이스에 결합하면
    **SQLAlchemy의 모든 복잡성에 결합하기로 고르는 것**이고, 그래서 더 단순한 추상을
    골라 책임을 명확히 가른다 (6장 §"Don't Mock What You Don't Own" 곁글).[^percival2020]
    그 판정의 전문은 [가짜와 목](../concepts/fakes-versus-mocks.md)에 있다.
- 이 논리를 [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)의 잣대로 읽으면
  리포지터리는 **깊은 모듈**이다 — 인터페이스는 메서드 둘, 구현은 ORM 설정·세션·질의
  전부. #hypothesis 두 소스가 서로를 참조한 적은 없다.
- 그리고 SQLAlchemy 추상을 우리 추상으로 **바꾸는 것**이지 없애는 것이 아니라는 규정 —
  **우리 코드에 관한 한 우리는 그저 SQLAlchemy 추상(`session.query(Batch)`)을 우리가
  설계한 다른 것(`batches_repo.get`)으로 맞바꾸고 있을 뿐이다**
  (2장 §"What Is the Trade-Off?").[^percival2020]

## 가짜 리포지터리와 설계 피드백

- 저자들이 이것을 이 패턴의 가장 큰 이득 중 하나로 꼽는다 — **여기 리포지터리 패턴의 가장
  큰 이득 하나가 있다** (2장 §"Building a Fake Repository for Tests Is Now
  Trivial!").[^percival2020] `FakeRepository`는 집합(set) 하나를 감싼 것이고 —
  **집합을 감싼 단순한 껍데기이므로 모든 메서드가 한 줄짜리다**
  (2장 §"Building a Fake Repository for Tests Is Now Trivial!").[^percival2020]
- **그리고 그 쉬움 자체가 계측기로 쓰인다** — **당신 추상에 대한 가짜를 만드는 것은 설계
  피드백을 얻는 훌륭한 방법이다: 가짜로 만들기 어렵다면 그 추상은 아마 너무 복잡한 것이다**
  (2장 §"Building a Fake Repository for Tests Is Now Trivial!").[^percival2020]
  - 이 문장이 이 책에서 가장 값싼 설계 판정 도구다. 인터페이스의 크기를 세지 않고도
    같은 것을 잰다 — 가짜의 줄 수가 곧 인터페이스의 복잡도다. #hypothesis 저자들이 그렇게
    정식화하지는 않았다.
- 가짜가 어디에 사는지가 장마다 옮겨 다닌다. 2장에서는 `repository.py`에 있고, 4장 이후
  서비스 레이어 테스트에서는 `tests/unit/test_services.py`로 옮겨 간다
  (4장 §"Introducing a Service Layer…").[^percival2020]

## 테스트를 버릴 때와 남길 때

- ORM 설정 테스트는 **버릴 것**으로 규정된다 — **아마 이 테스트들은 갖고 있지 않을 것이다.
  곧 보겠지만 ORM과 도메인 모델의 의존을 뒤집는 단계를 밟고 나면, 리포지터리 패턴이라는
  또 다른 추상을 구현하는 데는 작은 추가 단계 하나뿐이고, 그쪽이 테스트를 쓰기 더 쉽고
  나중에 테스트에서 가짜로 만들 단순한 인터페이스를 제공할 것이다**
  (2장 §"Inverting the Dependency: ORM Depends on Model").[^percival2020]
- 리포지터리 테스트는 **남길 것**이다 — **앞의 ORM 테스트와 달리 이 테스트들은 특히 당신
  도메인 모델의 어떤 부분이 객체-관계 맵을 사소하지 않게 만든다면 코드베이스의 일부로 더
  오래 남기에 좋은 후보다** (2장 §"The Repository in the Abstract").[^percival2020]
- 그리고 전수 테스트는 판단이라고 못 박는다 — **모든 모델에 대해 공들여 테스트를 쓸지 말지는
  판단의 문제다. 한 클래스에 대해 생성·수정·저장을 테스트하고 나면, 나머지는 최소한의 왕복
  테스트로 하거나, 전부 비슷한 패턴을 따른다면 아예 하지 않는 것으로 만족할 수도 있다**
  (2장 §"The Repository in the Abstract").[^percival2020]
- 6장에서 실제로 정리한다 — **더 오래 값을 더하지 않을 것 같다고 생각하면 언제든 자유롭게
  테스트를 버려라. 우리는 `test_orm.py`가 주로 우리가 SQLAlchemy를 배우도록 돕는 도구였다고
  말하겠고, 그래서 특히 그것이 하는 주요한 일들이 `test_repository.py`에서 다뤄진다면
  장기적으로 필요 없을 것이다** (6장 §"Tidying Up the Integration Tests").[^percival2020]

## 비용 — 저자들이 계상한 표

저자들이 Rich Hickey를 인용해 이 형식을 도입한다 (2장 §"What Is the Trade-Off?"):[^percival2020]

> You know they say economists know the price of everything and the value of nothing?
> Well, programmers know the benefits of everything and the trade-offs of nothing.
>
> — Rich Hickey

**표 2-1의 내용이다** (2장 §"Wrap-Up"):[^percival2020]

| 이득 | 비용 |
|---|---|
| 영속 저장소와 도메인 모델 사이에 단순한 인터페이스가 생긴다 | ORM이 이미 어느 정도 결합을 끊어 준다 — 외래 키를 바꾸기는 어려울지 몰라도 MySQL과 Postgres를 맞바꾸기는 꽤 쉬울 것이다 |
| 단위 테스트용 가짜를 만들거나 저장 방식을 통째로 바꾸기 쉽다 — 모델을 인프라 관심사에서 완전히 떼어 냈으므로 | ORM 매핑을 손으로 유지하는 데 추가 작업과 추가 코드가 든다 |
| 영속성을 생각하기 전에 도메인 모델을 쓰는 것이 당면한 업무 문제에 집중하도록 돕는다 — 접근을 근본적으로 바꾸고 싶어지면 외래 키나 마이그레이션 걱정 없이 모델에서 그렇게 할 수 있다 | 간접 계층이 하나 더 늘 때마다 유지보수 비용이 오르고, 리포지터리 패턴을 본 적 없는 파이썬 프로그래머에게 "이게 뭐지" 요인을 더한다 |
| 객체를 테이블에 어떻게 매핑할지 완전히 통제하므로 DB 스키마가 정말 단순해진다 | |

- **그리고 이 계산이 도메인 복잡도에 따라 갈린다.** 저자들이 그림 하나로 그 기본 명제를
  세운다 — 단순한 경우에는 결합을 끊은 도메인 모델이 단순한 ORM/액티브 레코드 패턴보다
  손이 더 간다. 그러나 **도메인이 복잡할수록 인프라 관심사에서 자유로워지는 데 든 투자가
  변경의 쉬움으로 값을 할 것이다** (2장 §"Wrap-Up").[^percival2020]
  - 그림 자체(가로축 = 업무 도메인/로직의 복잡도, 세로축 = 변경 비용, 두 곡선이 교차)는
    ditaa 소스로 본문에 함께 실려 있어 축과 교차 구조는 실측했다. 저자들이 그 그림의
    출처를 밝힌다 — **Rob Vens의 "Global Complexity, Local Simplicity"라는 글에서 영감을
    받은 다이어그램** (2장 각주 8).[^percival2020]
  - 이 곡선은 [설계의 경제학 — 시간 가치와 옵션성](software-design-economics.md)의
    비용 곡선과 같은 형식이다 — 둘 다 "지금 더 쓰고 나중에 덜 쓴다"를 두 곡선의 교차로
    그린다. #hypothesis 두 소스가 서로를 참조한 적은 없다.

## 이 패턴의 원 정의

리포지터리는 이 소스가 만든 것이 아니라 도메인 주도 설계 쪽 원전에서 왔다. 원 정의를 여기
둔다 — 이 페이지가 옮긴 파이썬 판정과 어긋나지 않는지 대조할 자리다.

- 처방 문단이 그 정의다 (6장, p.151):[^evans2003]

> For each type of object that needs global access, create an object that can provide the
> illusion of an in-memory collection of all objects of that type. Set up access through a
> well-known global interface.

  - 위 [무엇을 추상하는가](#무엇을-추상하는가)의 "데이터가 전부 메모리에 있는 척한다"가 이
    조문의 재서술이다. 원전 쪽 낱말이 **착시**(illusion)이고, 이 소스가 든 무한 메모리 반사실이
    같은 것을 이야기로 바꾼 것이다.
- 인터페이스에 요구되는 것도 같은 문단에 있다 — **객체를 더하고 제거하는 메서드를 제공하되
  그것이 데이터 저장소에서의 실제 삽입·삭제를 캡슐화하게 하라. 어떤 기준으로 객체를 선택해
  속성값이 그 기준에 맞는 완전히 인스턴스화된 객체나 객체의 컬렉션을 돌려주는 메서드를
  제공하되, 그것이 실제 저장·질의 기술을 캡슐화하게 하라. 직접 접근이 실제로 필요한 애그리게이트
  루트에만 리포지터리를 제공하라. 클라이언트를 모델에 집중시키고 모든 객체 저장과 접근을
  리포지터리에 위임하라** (6장, pp.151–152).[^evans2003]
- 원전이 계상하는 이득 넷 (6장, p.152):[^evans2003]
  - **클라이언트에게 영속 객체를 얻고 그 생애 주기를 관리하는 단순한 모델을 제시한다.**
  - **애플리케이션과 도메인 설계를 영속성 기술, 다중 데이터베이스 전략, 심지어 다중 데이터
    원천에서 결합 해제한다.**
  - **객체 접근에 대한 설계 결정을 소통한다.**
  - **테스트용으로 더미 구현을 쉽게 갈아 끼울 수 있게 한다(보통 메모리 안 컬렉션을 쓴다).**
  - 넷째가 위 [가짜 리포지터리와 설계 피드백](#가짜-리포지터리와-설계-피드백)의 근거와 같다.
    다만 이 소스는 거기서 한 걸음 더 간다 — 가짜로 만들기 어려운 것을 **추상이 너무 복잡하다는
    신호**로 되읽는 계측기는 원전에 없다.
- 원전이 이 패턴의 자리를 규정하는 한 줄 — **리포지터리는 클라이언트에게서 큰 부담을 덜어
  주어, 이제 클라이언트가 단순하고 의도를 드러내는 인터페이스에 대고 모델의 관점에서 필요한
  것을 요청할 수 있게 한다. 이 모든 것을 지원하려면 많은 복잡한 기술 인프라가 필요하지만
  인터페이스는 단순하고 개념적으로 도메인 모델에 연결되어 있다** (6장, p.151).[^evans2003]
  이 문장이 기대는 조항은 [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)다.

## 이어지는 페이지

- [작업 단위 패턴](unit-of-work-pattern.md) — 이 리포지터리를 담는 원자적 경계
- [서비스 레이어](service-layer-pattern.md) — 이 리포지터리를 부르는 층
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 리포지터리
  하나가 무엇을 돌려줘야 하는가를 정하는 규칙
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 구현하는 원리
- [가짜와 목](../concepts/fakes-versus-mocks.md) — `FakeRepository`가 왜 목이 아닌가
- [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md) — 저장소를
  CSV로 통째로 바꿔 이 추상을 시험하는 부록
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^evans2003]: Evans 2003, 6장 "The Life Cycle of a Domain Object" §REPOSITORIES
    (pp.151–152). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은
    대문자로 조판하는 관례를 직인용에서 유지했다. **이 절은 원 정의와 이득 목록만 든다** —
    질의 방식·구현·프레임워크·팩토리와의 관계를 다루는 나머지 절(pp.152–159)은 이 페이지의
    물음(사이에 무엇을 놓는가) 밖이다. 이 소스에서 온 코드 펜스는 이 페이지에 없다.

[^percival2020]: Percival & Gregory 2020, 2장 "Repository Pattern" 전체(곁글 "Django's
    ORM Is Essentially the Same, but More Restrictive"·"Abstract Base Classes, Duck
    Typing, and Protocols"·"Repository Pattern Recap" 포함) · 4장 §"Introducing a Service
    Layer, and Using FakeRepository to Unit Test It" · 6장 §"Tidying Up the Integration
    Tests"·§"Don't Mock What You Don't Own" 곁글. **이 소스의 locator는 장 단위다** —
    검증 절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이 정본이다.
    표 2-1은 원문이 장단점 목록 두 개를 나란히 둔 것을 표로 옮겼고 행 수가 달라 마지막
    칸이 빈다. Figure 2-6(도메인 복잡도 대 변경 비용)은 이미지지만 ditaa 소스가 본문에
    함께 있어 축과 곡선 교차를 판독했다 — 수치는 없다. 코드 펜스는 원문에서 조판용 번호
    표지 이미지를 제거했다.

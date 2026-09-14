---
type: concept
title: 리포지터리 패턴
description: 영속 저장소 위에 씌우는 단순화 추상 — 데이터가 전부 메모리에 있는 척한다는 규정과 add·get 두 메서드뿐인 최소 인터페이스, ORM이 주는 영속성 무지와 그것으로는 부족한 이유, 선언적 매핑 대신 고전적 매퍼로 ORM이 모델을 임포트하게 뒤집는 수순, 자기 부과한 단순함이 결합을 막는다는 논리, 집합 하나로 끝나는 가짜 리포지터리와 "가짜로 만들기 어려우면 추상이 너무 복잡하다"는 설계 피드백, 이 패턴의 비용을 저자들이 계상한 표, 참조를 얻는 세 길과 모든 접근을 항해로만 하려다 엉킴에 빠진 팀의 기록, 기반 구조가 쉬울 때와 어려울 때 각각 모델이 망가지는 두 경로를 세운 원전의 문제 서술, 메모리 안 컬렉션의 착시를 조문으로 둔 원 정의와 그 이득 넷, 그리고 인터페이스의 폭과 구현이 따로 다뤄지는 자리
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
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
- [인터페이스의 폭과 구현은 따로 다룬다](#인터페이스의-폭과-구현은-따로-다룬다)
- [질의 규칙을 어디에 두는가](#질의-규칙을-어디에-두는가)
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

- 원전은 참조를 얻는 길이 셋뿐이라는 데서 출발한다 — 객체를 만들거나, 연관을 항해하거나,
  질의하는 것이다. 앞 둘만으로는 **첫 객체를 얻어야** 한다는 문제가 남는다 (6장,
  p.147).[^evans2003]
  - 저자가 앞 둘만 쓰려 한 팀의 사례를 남긴다 — 모델 주도 설계를 열성적으로 받아들여 **모든**
    객체 접근을 생성이나 항해로만 하려 한 팀이 있었고, **이 자기 부과한 제한이 그들을 정확히
    앞 몇 장에 걸쳐 피하려 애써 온 그 끝없는 엉킴을 만들게 강제했다** (6장,
    pp.147–148).[^evans2003] 팀은 그 전략을 오래 유지하지 못했지만 **다른 일관된 접근으로
    대체하지도 못했다. 그들은 임기응변 해법을 이어 붙였고 야심이 줄었다** (6장,
    p.148).[^evans2003]
- **질의와 연관 중 무엇을 쓸지가 설계 결정이 된다** — 데이터베이스 검색은 전역적으로 접근 가능해
  어떤 객체로도 곧장 갈 수 있게 하고, **모든 객체가 상호 연결될 필요가 없어져 객체의 그물을 다룰
  만하게 유지할 수 있다. 항해를 제공할지 검색에 의존할지가 설계 결정이 되고, 검색의 결합 해제와
  연관의 응집성을 맞바꾸게 된다** (6장, p.148).[^evans2003]
  - 예가 한 쌍의 물음으로 온다 — **고객(Customer) 객체가 자신이 낸 모든 주문(Order)의 컬렉션을
    들어야 하는가? 아니면 주문이 고객 ID 필드 검색으로 데이터베이스에서 찾아져야 하는가?
    검색과 연관의 옳은 조합이 설계를 이해할 수 있게 만든다** (6장, p.148).[^evans2003]
    이 저울의 다른 쪽 끝이 [도메인 연관](../concepts/domain-associations.md)이다.
- **문제 서술이 둘로 나뉘어 인쇄된다.** 첫째는 기반 구조가 쉬울 때와 어려울 때 각각 무엇이
  망가지는지다 (6장, p.149):[^evans2003]

> A client needs a practical means of acquiring references to preexisting domain objects. If
> the infrastructure makes it easy to do so, the developers of the client may add more
> traversable associations, muddling the model. On the other hand, they may use queries to
> pull the exact data they need from the database, or to pull a few specific objects rather
> than navigating from AGGREGATE roots. Domain logic moves into queries and client code, and
> the ENTITIES and VALUE OBJECTS become mere data containers. The sheer technical complexity
> of applying most database access infrastructure quickly swamps the client code, which leads
> developers to dumb down the domain layer, which makes the model irrelevant.

- 그 사이에 범위가 좁혀진다. 일시적 객체(보통 값 객체)는 걱정하지 않아도 되고, 항해로 찾는 편이
  편한 영속 객체도 질의 접근이 필요 없다. **그리고 가장 중요하게, 애그리게이트 내부의 어떤 객체도
  루트로부터의 항해를 제외한 접근이 금지된다** (6장, p.149).[^evans2003]
  - 값 객체를 전역 검색하는 일이 드문 이유도 적혀 있다 — **속성으로 값을 찾는 것은 그 속성을 가진
    새 인스턴스를 만드는 것과 동등하므로, 값에 대한 전역 검색 접근은 흔히 무의미하다** (6장,
    p.150).[^evans2003] 예외는 사용자 이름과 함께 저장해 되찾는 여행 일정 같은 것, 그리고 값이
    미리 정해진 열거형이다. 그리고 진단이 하나 따라온다 — **데이터베이스에서 기존 값을 검색해야
    한다고 느낀다면, 사실은 당신이 알아보지 못한 정체성을 가진 엔티티를 갖고 있을 가능성을
    고려할 만하다** (6장, p.150).[^evans2003]
- 그래서 문제가 더 정밀하게 다시 서술된다 (6장, p.150):[^evans2003]

> A subset of persistent objects must be globally accessible through a search based on object
> attributes. Such access is needed for the roots of AGGREGATES that are not convenient to
> reach by traversal. They are usually ENTITIES, sometimes VALUE OBJECTS with complex internal
> structure, and sometimes enumerated VALUES. Providing access to other objects muddies
> important distinctions. Free database queries can actually breach the encapsulation of
> domain objects and AGGREGATES. Exposure of technical infrastructure and database access
> mechanisms complicates the client and obscures the MODEL-DRIVEN DESIGN.

- 기술적 해법들이 있다는 것도 인정된다 — SQL을 질의 객체(QUERY OBJECT)로 캡슐화하거나 메타데이터
  매핑 층으로 객체와 테이블을 번역하는 기법들이다. **그러나 그렇더라도 무엇을 잃었는지 유의하라.
  우리는 더 이상 도메인 모델의 개념을 생각하고 있지 않다** (6장, pp.150–151).[^evans2003]
  그래서 이 패턴의 성격이 규정된다 — **리포지터리 패턴은 그 해법들을 캡슐화하고 우리의 모델 초점을
  되돌리는 단순한 개념적 틀이다** (6장, p.151).[^evans2003]
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

## 인터페이스의 폭과 구현은 따로 다룬다

원전은 정의를 세운 뒤 같은 장에서 두 물음을 더 간다 — 질의 인터페이스를 어디까지 열 것인가,
그리고 그 뒤를 어떻게 구현할 것인가. 이 페이지의 물음(사이에 무엇을 놓는가)과 다른 물음이라
따로 선다.

- [리포지터리의 질의와 구현](repository-querying-and-implementation.md)이 그 자리다. 고정 질의와
  유연한 질의의 절충, 클라이언트는 구현을 몰라도 되지만 개발자는 알아야 한다는 조항, 구현에서
  붙드는 셋(타입 추상화·결합 해제 활용·트랜잭션 통제를 클라이언트에 남기기), 그리고 프레임워크와
  싸우지 말라는 판정이 거기 있다.
  - 그중 셋째가 위 [가장 단순한 리포지터리](#가장-단순한-리포지터리)의 "커밋을 리포지터리 밖에
    두고 호출자의 책임으로 만든다"와 같은 결정이다. 원전 쪽 근거는 맥락의 소재다 —
    **클라이언트가 작업 단위를 올바르게 시작하고 커밋할 맥락을 갖고 있으리라 추정된다** (6장,
    p.156).[^evans2003]
- 검색이 돌려주는 객체가 실제로 만들어지는 과정은
  [저장된 객체의 재구성](../concepts/reconstituting-stored-objects.md)에 있다. 원전은 리포지터리와 팩토리를
  합치지 않고 분담시킨다 — **팩토리는 새 객체를 만들고, 리포지터리는 옛 객체를 찾는다** (6장,
  p.158).[^evans2003]

## 질의 규칙을 어디에 두는가

위 원 정의의 "어떤 기준으로 객체를 선택하는 메서드"가 실제로 무엇을 받아야 하는지를 같은 원전이
9장에서 구체화한다. 규칙을 나르는 것은 명세(SPECIFICATION)라는 별도 객체이고, 그 규칙과 SQL을
어느 쪽이 들 것인가에서 판이 갈린다.

- 둘의 관계가 먼저 규정된다 — **명세는 리포지터리와 매끄럽게 맞물리는데, 리포지터리는 도메인
  객체에 대한 질의 접근을 제공하고 데이터베이스로의 인터페이스를 캡슐화하는 구성 요소 기제이기
  때문이다** (9장, p.231).[^evans2003] 가장 단순한 형태는 리포지터리에 명세를 받는 일반화된
  선택 메서드 `selectSatisfying(InvoiceSpecification spec)`를 두는 것이다 (9장,
  p.229).[^evans2003]
- **첫째 판에서 저자는 명세가 SQL을 내게 해 보고 곧바로 대가를 적는다** — **가장 중요하게는,
  테이블 구조의 세부가 도메인 층으로 새어 나왔다; 그것은 도메인 객체를 관계형 테이블에 연결하는
  매핑 층에 격리되어야 한다** (9장, p.231).[^evans2003] 인프라가 모델 객체와 속성으로 질의를
  표현하고 실제 SQL을 생성해 준다면 그것이 답이다 (9장, p.231).[^evans2003]
- **둘째 판은 SQL을 리포지터리로 되돌린다.** 리포지터리에 특화된 질의 메서드를 두고, 명세가
  `satisfyingElementsFrom(InvoiceRepository)`로 어느 질의를 부를지 고른다. 판정 — **이것은
  SQL을 리포지터리에 두면서 명세가 어떤 질의를 써야 할지를 통제하게 한다. 규칙이 명세에 그리
  깔끔하게 모이지는 않지만, 무엇이 연체를 이루는가에 대한 본질적 선언은 거기에 있다** (9장,
  p.232).[^evans2003] 이때 리포지터리는 이 경우에만 쓰일 아주 특화된 질의를 갖게 되는데, 저자는
  그것을 받아들일 만하다고 본다 (9장, p.232).[^evans2003]
- **셋째 판은 리포지터리를 일반적으로 두고 명세가 메모리에서 거른다.** 대가가 성능으로
  명시된다 — **이 코드로는 성능 손해를 본다. 더 많은 청구서를 꺼내 와 메모리에서 골라야 하기
  때문이다. 이것이 책임의 더 나은 배분을 위해 받아들일 만한 비용인지는 전적으로 상황에 달렸다**
  (9장, p.233).[^evans2003]
- 세 판을 묶는 판정이 이 절의 요점이다 (9장, pp.233–234):[^evans2003]

> For all that, there is no difference in the model between these various implementations. The
> choice of implementation is free except where specifically constrained by the model. The price
> comes in a more cumbersome way of writing and maintaining queries.

  - **위 [자기 부과한 단순함이 결합을 막는다](#자기-부과한-단순함이-결합을-막는다)와 저울이
    다르다.** 그쪽은 리포지터리 인터페이스를 좁게 유지해 결합을 막자고 하고, 이쪽은 규칙을
    명세로 빼면 리포지터리에 특화된 질의가 늘어도 괜찮다고 한다. 무엇을 지키느냐가 달라서
    생기는 차이다 — 전자는 추상의 단순함, 후자는 규칙이 도메인 층에 남는 것이다. 전문은
    [명세 패턴](specification-pattern.md)에 있다.

## 이어지는 페이지

- [작업 단위 패턴](unit-of-work-pattern.md) — 이 리포지터리를 담는 원자적 경계
- [리포지터리의 질의와 구현](repository-querying-and-implementation.md) — 인터페이스의 폭과
  그 뒤의 구현
- [저장된 객체의 재구성](../concepts/reconstituting-stored-objects.md) — 검색이 돌려주는 객체가 만들어지는 일
- [팩토리 패턴](../concepts/factories-pattern.md) — 새 객체를 맡는 짝
- [명세 패턴](specification-pattern.md) — 이 리포지터리가 받는 질의 규칙이 사는 객체
- [서비스 레이어](service-layer-pattern.md) — 이 리포지터리를 부르는 층
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 리포지터리
  하나가 무엇을 돌려줘야 하는가를 정하는 규칙
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 구현하는 원리
- [가짜와 목](../concepts/fakes-versus-mocks.md) — `FakeRepository`가 왜 목이 아닌가
- [있는 시스템에 이 구조 들이기](../concepts/adopting-architecture-incrementally.md) — 저장소를
  CSV로 통째로 바꿔 이 추상을 시험하는 부록
- [도메인 모델과 애플리케이션 계층](../synthesis/domain-model-and-application-layers.md) —
  이 축의 허브

[^evans2003]: Evans 2003, 6장 "The Life Cycle of a Domain Object" §REPOSITORIES 도입과
    문제 서술 둘과 처방(pp.147–152) · §"Implementing a REPOSITORY"의 트랜잭션 조항(p.156) ·
    §"The Relationship with FACTORIES"의 분담 한 줄(p.158) · 9장 "Making Implicit Concepts
    Explicit" §"Applying and Implementing
    SPECIFICATION"(§Selection (or Querying) pp.229–234). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은
    대문자로 조판하는 관례를 직인용에서 유지했다. **6장의 나머지 절은 물음이 달라 형제 페이지로
    갈랐다** — 질의 인터페이스와 구현(pp.152–157)은
    [리포지터리의 질의와 구현](repository-querying-and-implementation.md)에, 팩토리와의 관계
    전문(pp.157–159)은 [저장된 객체의 재구성](../concepts/reconstituting-stored-objects.md)에,
    관계형 스키마 설계(pp.159–161)는
    [관계형 데이터베이스를 위한 객체 설계](../concepts/designing-objects-for-relational-databases.md)에 있다.
    Figure 6.18(리포지터리가 클라이언트를 위해 검색하는 도해)은 걸러 내고 딸린 산문만 옮겼다.
    질의 규칙의 자리는 9장 쪽에서 들었고, 거기서도 코드는
    같은 설계의 변형 연쇄라 산문으로만 옮겼다. 이 소스에서 온 코드 펜스는 이 페이지에 없다.

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

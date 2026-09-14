---
type: concept
title: 액티브 레코드
description: 데이터베이스 행을 감싸는 객체로 복잡한 자료 구조의 매핑을 캡슐화하는 패턴 — 평평한 레코드가 아니라 객체 트리와 다대다 관계를 다룰 때 트랜잭션 스크립트가 매핑 코드를 중복하게 된다는 문제 설정, CRUD 데이터 접근 메서드를 스스로 갖는다는 뜻의 "액티브"와 객체 관계 매퍼에 결합된다는 귀결, 업무 로직은 여전히 트랜잭션 스크립트에 있고 이 객체는 자료 구조와 행동을 가른다는 규정, 어디에 쓰는가와 트랜잭션 스크립트와의 차이가 매핑 복잡성 하나라는 판정, "빈혈 도메인 모델 안티패턴"이라는 이름을 저자가 거부하는 논증과 단순한 로직에 정교한 패턴을 쓰면 우발적 복잡성으로 해가 된다는 대칭 경고, 패턴과 같은 이름의 프레임워크를 혼동하지 말라는 단서, 그리고 이 판정이 이 KB의 다른 소스들과 어긋나는 자리
generated: { by: "claude-opus-5", at: "2026-09-14T23:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 액티브 레코드

- [정의와 문제 설정](#정의와-문제-설정)
- [구현 — 무엇이 "액티브"한가](#구현--무엇이-액티브한가)
- [업무 로직은 어디에 있는가](#업무-로직은-어디에-있는가)
- [어디에 쓰는가](#어디에-쓰는가)
- [빈혈 도메인 모델이라는 이름을 저자가 거부한다](#빈혈-도메인-모델이라는-이름을-저자가-거부한다)
- [패턴이지 프레임워크가 아니다](#패턴이지-프레임워크가-아니다)
- [책의 사례 — 이 패턴이 두 번 나오는 자리](#책의-사례--이-패턴이-두-번-나오는-자리)
- [이 KB의 다른 소스들과 어긋나는 자리](#이-kb의-다른-소스들과-어긋나는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 로직은 단순한데 자료 구조가 복잡할 때, 그 매핑을 어디에 넣어야 절차마다
같은 코드를 다시 쓰지 않는가.**

## 정의와 문제 설정

- 이름과 정의는 트랜잭션 스크립트와 같은 출처에서 오고,
  [khononov2021](../sources/khononov2021.md)이 절 머리에 그대로 인용한다
  (5장 §"Active Record", p.69):[^khononov2021]

> An object that wraps a row in a database table or view, encapsulates the database access,
> and adds domain logic on that data.

- 이 패턴이 서는 조건이 [트랜잭션 스크립트](transaction-script.md)와 하나만 다르다 —
  **트랜잭션 스크립트 패턴처럼 액티브 레코드도 업무 로직이 단순한 경우를 지원한다. 다만 여기서는
  업무 로직이 더 복잡한 자료 구조 위에서 작동할 수 있다** (5장, p.69).[^khononov2021]
  - 평평한 레코드 대신 **더 복잡한 객체 트리와 계층**을 다룰 수 있다는 뜻이고, 저자가 드는 그림이
    일대다와 다대다 관계가 섞인 데이터 모델이다 (5장, pp.69–70).[^khononov2021]
- **문제는 중복이다** — 그런 자료 구조를 단순한 트랜잭션 스크립트로 다루면 **반복적인 코드가
  많이 생긴다. 데이터를 메모리 안 표현으로 매핑하는 일이 여기저기 중복된다**
  (5장, p.70).[^khononov2021]
  - 즉 이 패턴이 푸는 것은 업무 로직의 복잡성이 아니라 **매핑의 복잡성**이다. 이 구별이 아래
    [어디에 쓰는가](#어디에-쓰는가)의 판정 전부를 정한다.

## 구현 — 무엇이 "액티브"한가

- 그래서 이 패턴은 복잡한 자료 구조를 표상하는 전용 객체를 쓰고 그것을 액티브 레코드라 부른다.
  **그 객체는 자료 구조 외에 레코드를 만들고 읽고 갱신하고 지우는 데이터 접근 메서드, 이른바
  CRUD 연산도 구현한다** (5장 §Implementation, p.70).[^khononov2021]
- **그 결과로 결합이 하나 생긴다** — 액티브 레코드 객체는 **객체 관계 매퍼(object-relational
  mapping, ORM)나 다른 데이터 접근 프레임워크에 결합된다** (5장, p.70).[^khononov2021]
  - 이 결합이 [리포지터리 패턴](../concepts/repository-pattern.md)이 끊으려는 바로 그 결합이다.
    두 패턴은 같은 자리에 정반대 판단을 놓는다 — 이쪽은 결합을 받아들이고 매핑 중복을 없애며,
    그쪽은 결합을 끊고 매핑을 따로 둔다.
- **이름의 유래가 그 결합에 있다** — **각 자료 구조가 "액티브"하다는 사실에서 패턴 이름이
  나왔다. 즉 그것이 데이터 접근 로직을 구현한다** (5장, p.70).[^khononov2021]

## 업무 로직은 어디에 있는가

- **앞 패턴과 마찬가지로 시스템의 업무 로직은 트랜잭션 스크립트로 조직된다.** 둘의 차이는
  **트랜잭션 스크립트가 데이터베이스에 직접 접근하는 대신 액티브 레코드 객체를 조작한다**는
  것뿐이고, 그 연산은 여전히 **원자적 트랜잭션으로 완료되거나 실패해야 한다**
  (5장, p.70).[^khononov2021] 그 요구의 전문은 [트랜잭션 스크립트](transaction-script.md)에 있다.
- 사용자 생성 절차가 그 모양이다. 트랜잭션을 열고 액티브 레코드를 만들어 필드를 채우고
  `Save()`를 부른 뒤 커밋한다 (5장, pp.70–71):[^khononov2021]

  ```csharp
  public class CreateUser
  {
      ...

      public void Execute(userDetails)
      {
          try
          {
              _db.StartTransaction();

              var user = new User();
              user.Name = userDetails.Name;
              user.Email = userDetails.Email;
              user.Save();

              _db.Commit();
          } catch {
              _db.Rollback();
              throw;
          }
      }
  }
  ```

- **패턴의 목적이 한 줄로 규정된다** — **메모리 안 객체를 데이터베이스 스키마로 매핑하는
  복잡성을 캡슐화하는 것** (5장, p.71).[^khononov2021]
- **그런데 업무 로직을 담을 수도 있다** — 영속성 책임 외에 액티브 레코드 객체는 업무 로직을
  담을 수 있다. 예로 **필드에 배정되는 새 값의 검증**, 또는 **객체의 데이터를 조작하는 업무 관련
  절차의 구현**까지다 (5장, p.71).[^khononov2021]
- **그럼에도 이 객체의 결정적 특징은 가름이다** (5장, p.71):[^khononov2021]

> That said, the distinctive feature of an active record object is the separation of data
> structures and behavior (business logic). Usually, an active record's fields have public
> getters and setters that allow external procedures to modify its state.

  - **공개 게터와 세터가 이 패턴의 서명이다.** 외부 절차가 상태를 고칠 수 있다는 것이
    [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md)의 정반대
    조항이다. 그쪽은 상태를 고칠 수 있는 것이 애그리게이트 자신의 업무 로직뿐이라고 요구한다.
  - **두 문장이 겉보기에 어긋난다.** 바로 앞 항은 "업무 로직을 담을 수 있다"고 하고 이 항은
    "자료 구조와 행동이 갈린다"고 한다. 저자가 둘을 화해시키지 않지만, 문맥상 담을 수 있는
    것은 **자기 필드에 대한 검증과 조작**이고 갈리는 것은 **여러 객체에 걸친 업무 절차**다.
    #hypothesis 저자가 이 구별을 명시하지 않았으므로 가설로 적는다.

## 어디에 쓰는가

- **액티브 레코드는 본질적으로 데이터베이스 접근을 최적화한 트랜잭션 스크립트이므로, 이 패턴은
  비교적 단순한 업무 로직만 지원할 수 있다.** 예가 CRUD 연산이고 **기껏해야 사용자 입력을
  검증하는 정도**다 (5장 §"When to Use Active Record", p.71).[^khononov2021]
- **그래서 맞는 자리가 트랜잭션 스크립트와 같다** — 보조 하위 도메인, 일반 하위 도메인을 위한
  외부 솔루션의 통합, 모델 변환 작업이다 (5장, p.71).[^khononov2021] 그 분류는
  [하위 도메인의 세 종류](subdomain-types.md)에 있다.
- **두 패턴의 차이가 한 줄로 정리된다** — **액티브 레코드는 복잡한 자료 구조를 데이터베이스
  스키마로 매핑하는 복잡성을 다룬다** (5장, p.71).[^khononov2021] 그것이 차이의 전부다.
  - 따라서 [트랜잭션 스크립트](transaction-script.md)에 걸린 금지가 이 패턴에도 그대로 걸린다 —
    핵심 하위 도메인에는 쓰지 않는다. 네 패턴 사이의 선택 전체는
    [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.

## 빈혈 도메인 모델이라는 이름을 저자가 거부한다

**이 절이 이 페이지에서 판단이 걸리는 자리다.** 저자가 업계의 부정적 이름을 먼저 인정하고
그것을 기각한다.

- 이름부터 적는다 — **액티브 레코드 패턴은 빈혈 도메인 모델 안티패턴(anemic domain model
  antipattern)이라고도 불린다. 다시 말해 잘못 설계된 도메인 모델이다**
  (5장, p.71).[^khononov2021]
- **그리고 그 이름을 쓰지 않겠다고 적는다** (5장, p.71):[^khononov2021]

> I prefer to restrain from the negative connotation of the words anemic and antipattern. This
> pattern is a tool. Like any tool, it can solve problems, but it can potentially introduce
> more harm than good when applied in the wrong context. There is nothing wrong with using
> active records when the business logic is simple.

- **논증의 핵심은 대칭이다** — 잘못된 맥락에 쓰면 해가 되는 것은 이 패턴만이 아니다.
  **더 나아가 단순한 업무 로직을 구현하는 데 더 정교한 패턴을 쓰는 것도 우발적 복잡성
  (accidental complexity)을 들여 해가 된다** (5장, p.71).[^khononov2021]
  - **즉 "안티패턴"이라는 이름이 한쪽 방향의 오용만 세고 반대 방향은 세지 않는다는 것이 이
    거부의 근거다.** 같은 회계를 이 KB의 다른 소스들도 한다 —
    [도메인 모델 패턴](../concepts/domain-model-pattern.md)의 "이 패턴이 필요 없는 경우"와
    [스마트 UI 안티패턴](../concepts/smart-ui-antipattern.md)이 그 자리다. 다만 그 둘은
    **간접 계층의 비용**을 세고, 이 판본은 거기에 **하위 도메인의 종류**라는 판정 기준을 건다.

## 패턴이지 프레임워크가 아니다

- 저자가 곁글 하나를 이 혼동에 쓴다 (5장, p.71):[^khononov2021]

> It's important to stress that in this context, active record refers to the design pattern,
> not the Active Record framework. The pattern name was coined in Patterns of Enterprise
> Application Architecture by Martin Fowler. The framework came later as one way to implement
> the pattern. In our context, we are talking about the design pattern and the concepts behind
> it, not a specific implementation.

  - 루비 온 레일즈의 Active Record가 이 패턴의 한 구현이지 정의가 아니라는 뜻이다. 이 경고가
    필요한 이유는 프레임워크마다 패턴에 없는 것을 더하기 때문이다 — 예컨대 질의 인터페이스와
    마이그레이션은 패턴의 정의에 없다.

## 책의 사례 — 이 패턴이 두 번 나오는 자리

**같은 판본의 부록 A에서 이 패턴이 두 번 나오고, 두 번의 결과가 다르다.** 이야기 본체는
[마켓노버스 사례 연구](marketnovus-case-study.md)에 있고, 여기 옮긴 것은 이 패턴에 걸리는
것이다.

- **첫째는 의도하지 않은 경우다** — 도메인 모델을 겨누었으나 명사마다 애그리게이트를 선포하는
  것으로 끝났고, 그것들은 **트랜잭션 경계를 전혀 제공하지 않았고 행동이 거의 없었으며 모든 업무
  로직이 거대한 서비스 레이어에 있었다** (부록 A §"Bounded Context #1: Marketing",
  p.275).[^khononov2021] 저자가 그 상태에 이름을 붙인다 (부록 A, p.275):[^khononov2021]

> When you aim to implement a domain model but end up with the active record pattern, it is
> often termed an "anemic domain model" antipattern.

  - **이 문장이 위 [빈혈 도메인 모델이라는 이름을 저자가
    거부한다](#빈혈-도메인-모델이라는-이름을-저자가-거부한다)와 겨루지 않는다.** 5장의 거부는
    **단순한 로직에 이 패턴을 의도적으로 고른 경우**에 걸리고, 부록 A의 이름 붙이기는 **복잡한
    로직에 도메인 모델을 겨누고 실패해 이 패턴에 떨어진 경우**에 걸린다. 같은 코드 모양이되
    판정의 입력이 다르다 — 어떤 하위 도메인에 무엇을 겨누었는가다.
  - **그리고 그 프로젝트가 업무 기준으로는 성공했다는 것이 이 사례의 요점이다** — 결함 있는
    아키텍처에도 불구하고 **견고한 유비쿼터스 언어가 그 결함을 보상해** 공격적인 일정 안에
    돌아가는 소프트웨어를 냈다 (부록 A, pp.275·283).[^khononov2021]
- **둘째는 의도한 경우다** — 보너스 프로젝트는 하위 도메인을 보조로 판정하고 그에 맞추어
  **액티브 레코드 객체들을 "똑똑한" 서비스 레이어가 조율하는** 형태로 설계했다 (부록 A
  §"Bounded Context #4: Bonuses", p.280).[^khononov2021] 판정의 근거도 적혀 있다 — **새로운
  것을 발명하지 않았고, 그 절차로 돈을 벌지 않았으며, 기성 구현을 살 수 있었다면 샀을
  것**이다 (부록 A, p.280).[^khononov2021]
  - **그 설계가 깨진 시점과 무엇이 그것을 알려 주었는가가 이 패턴의 수명을 보여 준다** —
    도메인의 복잡성이 자라며 **도메인 전문가가 쓰는 말이 어느 시점에 더 이상 액티브 레코드로
    모델링될 수 없었고**, 그 자각이 설계를 바꿔야 할 필요를 일찍 알아채게 했다 (부록 A,
    p.281).[^khononov2021] 그 신호의 전문은
    [유비쿼터스 언어](../concepts/ubiquitous-language.md)에 있고, 갈아타는 경로는
    [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)에 있다.

## 이 KB의 다른 소스들과 어긋나는 자리

이 페이지의 판정은 **이 KB에 이미 있는 두 소스의 판정과 방향이 다르다.** 모순 쌍으로 세우지
않았고, 왜 그렇게 판단했는지를 여기 적는다.

- **Clean Code 쪽은 업무 규칙을 밖으로 빼라고 처방한다** — 액티브 레코드에 업무 규칙 메서드를
  넣어 객체처럼 다루는 것이 **자료 구조와 객체 사이의 잡종을 만들기 때문에 어색하다**고 적고,
  해법으로 **액티브 레코드를 자료 구조로 다루고 업무 규칙을 담는 별도의 객체를 만들라**고 한다.
  전문은 [객체와 자료 구조](../concepts/objects-versus-data-structures.md)에 있다.
  - **대질하면 두 소스가 같은 그림을 서로 다르게 값매김한다.** 위
    [업무 로직은 어디에 있는가](#업무-로직은-어디에-있는가)가 옮긴 규정 — 자료 구조와 행동이
    갈리고 공개 게터·세터를 갖는다 — 은 Clean Code 쪽이 "자료 구조"라 부르는 것과 같은 모양이다.
    거기까지는 두 소스가 어긋나지 않는다.
  - **어긋나는 것은 그다음이다.** Clean Code 쪽은 이 객체에 업무 규칙이 들어가는 것을 **조건 없이**
    어색하다고 판정하고, 이 판본은 **업무 로직이 단순하면 문제없다**고 판정한다. 사실 주장이
    아니라 **조건을 거는가 아닌가**의 차이이고, 이 판본이 거는 조건이 하위 도메인의 종류다.
    그래서 `contradicts`를 걸지 않았다.
- **파이썬 쪽 축은 반대 방향의 위험으로 같은 낱말을 쓴다** — 그쪽에서 빈혈 도메인은 액티브
  레코드의 다른 이름이 아니라 **서비스 레이어에 로직을 너무 많이 넣었을 때** 가는 곳이다.
  전문은 [서비스 레이어](../concepts/service-layer-pattern.md)의 비용 표에 있다.
  - **같은 낱말이 다른 것을 가리킨다.** 이 판본에서 빈혈 도메인은 **패턴의 이름**(액티브 레코드를
    깎아내리는 이름)이고, 그쪽에서는 **층을 잘못 쌓았을 때 생기는 증상**이다. 대상이 다르므로
    겨루지 않는다.

## 이어지는 페이지

- [트랜잭션 스크립트](transaction-script.md) — 같은 장의 첫째 패턴이자 이 패턴의 바탕
- [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md) — 네 패턴 중 무엇을
  고르는가
- [도메인 모델 패턴](../concepts/domain-model-pattern.md) — 다음 장이 이 패턴과 대조하는 쪽
- [객체와 자료 구조](../concepts/objects-versus-data-structures.md) — 같은 패턴에 다른 판정을
  내리는 소스
- [리포지터리 패턴](../concepts/repository-pattern.md) — 데이터 접근 결합에 정반대 판단을 놓는 패턴
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 공개
  게터·세터가 금지되는 쪽
- [서비스 레이어](../concepts/service-layer-pattern.md) — 빈혈 도메인이라는 낱말이 다른 뜻으로
  쓰이는 자리
- [하위 도메인의 세 종류](subdomain-types.md) — 이 패턴이 허용되는 종류를 정하는 분류
- [마켓노버스 사례 연구](marketnovus-case-study.md) — 이 패턴을 고른 프로젝트와 잘못 떨어진
  프로젝트의 기록
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 5장 "Implementing Simple Business Logic" §"Active Record"
    (pp.69–71 — §Implementation pp.70–71 · §"When to Use Active Record" p.71과 같은 쪽의
    곁글) 및 §Conclusion p.72. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 직인용은
    `pdftotext -layout` 추출로 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다. 곁글 직인용에서
    원문이 이탤릭으로 조판한 낱말(*active record*·*Patterns of Enterprise Application
    Architecture*)의 서체 표시는 인용 블록 안에서 뺐다 — 글자는 원문 그대로다. Fowler 정의
    두 줄은 이 책이 인용한 것을 재인용한 것이고 이 KB가 확인한 원전이 아니다(Fowler, M.
    (2002). *Patterns of Enterprise Application Architecture*). 코드 펜스는 하나만 두었다 —
    언어 표지(`csharp`)는 이 KB가 붙였고, 원문의 `...`는 저자가 생략을 표시한 것이다.
    도판 하나(Figure 5-4 일대다·다대다 관계가 섞인 데이터 모델)는 도판이라 옮기지 않고
    본문이 그것에 대해 적는 것만 서술했다. 장 끝 연습문제 넷(pp.72–73)은 claim이 아니라
    옮기지 않았다. 5장 §"Be Pragmatic"(p.72)은 장 전체에 걸리는 단서라
    [트랜잭션 스크립트](transaction-script.md)에 한 번만 실었다.
    **부록 A §"Bounded Context #1: Marketing"(p.275)과 §"Bounded Context #4: Bonuses"
    (pp.280–281)도 이 페이지에 합류했다** — 이 패턴이 의도하지 않게 나온 경우와 의도해서 고른
    경우가 그 두 자리다. 다섯 경계 컨텍스트의 이야기 본체는 이 페이지에 두지 않고
    [마켓노버스 사례 연구](marketnovus-case-study.md)에 두었다.

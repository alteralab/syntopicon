---
type: concept
title: 상속세
status: draft
description: 상속이 두 갈래 역사(시뮬라의 타입 조합과 스몰토크의 행동 조직)에서 왔고 그 둘이 각각 다른 이유로 오용된다는 진단, 상속이 곧 결합이라는 판정과 부모의 이름 변경이 자식과 그 사용자를 조용히 깨뜨리는 실물, 타입 나무가 벽을 덮는 괴물이 되는 경로와 다중 상속의 벽, 그리고 상속을 대체하는 세 기법(인터페이스와 프로토콜·위임·믹스인)과 각각을 고르는 기준
generated: { by: "claude-opus-5", at: "2026-08-15T21:00:00Z" }
sources:
  - { id: thomas2020, resource: /it/sources/thomas2020.md }
---

# 상속세

- [출발 — 바나나와 정글](#출발--바나나와-정글)
- [상속의 두 갈래 역사](#상속의-두-갈래-역사)
- [코드를 공유하려는 상속 — 상속은 곧 결합이다](#코드를-공유하려는-상속--상속은-곧-결합이다)
- [타입을 만들려는 상속 — 벽을 덮는 나무](#타입을-만들려는-상속--벽을-덮는-나무)
- [대안 하나 — 인터페이스와 프로토콜](#대안-하나--인터페이스와-프로토콜)
- [대안 둘 — 위임](#대안-둘--위임)
- [대안 셋 — 믹스인과 트레이트](#대안-셋--믹스인과-트레이트)
- [무엇을 언제 고르는가](#무엇을-언제-고르는가)
- [이 KB의 상속 서술과 나란히](#이-kb의-상속-서술과-나란히)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **행동을 공유하거나 타입을 표현하려 할 때, 상속 말고 무엇을 쓸 수 있고 왜 그래야
하는가.**

## 출발 — 바나나와 정글

- 이 Topic의 경구는 조 암스트롱의 것이다 (Topic 31):[^thomas2020]

> You wanted a banana but what you got was a gorilla holding the banana and the entire jungle.

- 저자들의 첫 문단은 명령형이다 — **객체 지향 언어로 프로그래밍하는가? 상속을 쓰는가? 그렇다면
  멈춰라! 그것은 아마 당신이 하고 싶은 일이 아니다** (Topic 31).[^thomas2020]

## 상속의 두 갈래 역사

- **시뮬라 — 타입을 조합하는 장치** — **상속은 1969년 Simula 67에서 처음 나타났다. 그것은 같은
  리스트에 여러 종류의 이벤트를 큐잉하는 문제에 대한 우아한 해법이었다. 시뮬라의 접근은 **접두
  클래스**(prefix classes)라 불리는 것을 쓰는 것이었다** (Topic 31).[^thomas2020]
  `link CLASS car;`처럼 쓰면 **`link`는 연결 리스트의 기능성을 더하는 접두 클래스다** (Topic
  31).[^thomas2020] 그 시절의 심상 — **시뮬라 프로그래머가 쓴 심적 모형은 클래스 `link`의 인스턴스
  데이터와 구현이 클래스 `car`와 `bicycle`의 구현 앞에 붙는다는 것이었다. `link` 부분은 자동차와
  자전거를 싣고 다니는 **컨테이너**로 거의 여겨졌다. 이것이 그들에게 일종의 다형성을 줬다**
  (Topic 31).[^thomas2020]
- **스몰토크 — 행동을 조직하는 장치** — 앨런 케이가 2019년 Quora 답변에서 스몰토크가 왜 상속을
  갖는지 밝힌 것을 저자들이 인용한다 (Topic 31):[^thomas2020]

> So when I designed Smalltalk-72—and it was a lark for fun while thinking about
> Smalltalk-71—I thought it would be fun to use its Lisp-like dynamics to do
> experiments with "differential programming" (meaning: various ways to accomplish
> "this is like that except").

  - 저자들의 판독 — **이것은 순전히 행동을 위한 서브클래싱이다** (Topic 31).[^thomas2020]
- 두 계보의 분화 — **이 두 상속 스타일은(실제로는 공통점이 꽤 있었다) 이후 수십 년에 걸쳐 발전했다.
  상속이 타입을 결합하는 방법이라고 제안한 시뮬라 접근은 C++과 자바 같은 언어에서 이어졌다. 상속이
  행동의 동적 조직이었던 스몰토크 학파는 루비와 자바스크립트 같은 언어에서 보였다** (Topic
  31).[^thomas2020]
- **그래서 오용도 두 갈래다** — **그래서 이제 우리는 두 이유 중 하나로 상속을 쓰는 OO 개발자
  세대를 마주한다: 타이핑을 싫어하거나, 타입을 좋아하거나** (Topic 31).[^thomas2020]
  - 타이핑을 싫어하는 쪽 — **기반 클래스의 공통 기능성을 자식 클래스에 더하려고 상속을 써서
    손가락을 아낀다: 클래스 `User`와 클래스 `Product`가 둘 다 `ActiveRecord::Base`의 서브클래스다**
    (Topic 31).[^thomas2020]
  - 타입을 좋아하는 쪽 — **클래스 사이의 관계를 표현하는 데 상속을 쓴다: `Car`는 `Vehicle`의
    일종이다** (Topic 31).[^thomas2020]
  - **불행히도 두 종류의 상속 모두 문제를 갖는다** (Topic 31).[^thomas2020]
  - 이 절이 이 Topic의 구조를 정한다 — 뒤의 진단 둘과 대안 셋이 이 두 동기에 각각 대응한다.

## 코드를 공유하려는 상속 — 상속은 곧 결합이다

- **판정** — **상속은 곧 결합이다. 자식 클래스가 부모, 부모의 부모 등에 결합돼 있을 뿐 아니라,
  자식을 **사용하는** 코드도 모든 조상에 결합돼 있다** (Topic 31).[^thomas2020]
- 저자들의 실물 (Topic 31):[^thomas2020]

  ```ruby
  class Vehicle
    def initialize
      @speed = 0
    end
    def stop
      @speed = 0
    end
    def move_at(speed)
      @speed = speed
    end
  end

  class Car < Vehicle
    def info
      "I'm car driving at #{@speed}"
    end
  end

  # top-level code
  my_ride = Car.new
  my_ride.move_at(30)
  ```

- 무엇이 깨지는가 — **최상위가 `my_car.move_at`을 호출할 때 호출되는 메서드는 `Car`의 부모인
  `Vehicle`에 있다** (Topic 31).[^thomas2020] 이제 `Vehicle` 담당 개발자가 API를 바꿔 `move_at`이
  `set_velocity`가 되고 인스턴스 변수 `@speed`가 `@velocity`가 된다면 —
  - **API 변경이 `Vehicle` 클래스의 클라이언트를 깨뜨릴 것은 예상된 일이다. 그러나 최상위는 그렇지
    않다: 그것이 아는 한 그것은 `Car`를 쓰고 있다. `Car` 클래스가 구현의 관점에서 무엇을 하는지는
    최상위 코드의 관심사가 아닌데도 그것은 여전히 깨진다** (Topic 31).[^thomas2020]
  - **마찬가지로 인스턴스 변수의 이름은 순전히 내부 구현 세부지만, `Vehicle`이 그것을 바꾸면
    `Car`도 (조용히) 깨진다** (Topic 31).[^thomas2020]
  - 저자들의 세 낱말 결론 — **결합이 너무 많다**(So much coupling) (Topic 31).[^thomas2020]
  - **"조용히"가 이 절의 무게중심이다.** 인터페이스를 깨는 변경은 컴파일러나 호출부가 잡지만,
    상속이 노출한 구현 세부는 아무도 계약이라고 선언한 적이 없어서 깨져도 신호가 없다. 이것이
    [결합 끊기](decoupling.md)가 든 결합의 증상 중 "관련 없는 모듈로 전파되는 단순한 변경"의
    한 실물이다.

## 타입을 만들려는 상속 — 벽을 덮는 나무

- 진단 — **어떤 사람들은 상속을 새 타입을 정의하는 방법으로 본다. 그들이 가장 좋아하는 설계
  다이어그램은 클래스 계층을 보인다. 그들은 문제를 빅토리아 시대 신사 과학자들이 자연을 보던
  방식으로, 범주로 쪼개져야 할 무엇으로 본다** (Topic 31).[^thomas2020]
- 무엇이 일어나는가 — **불행히도 이 다이어그램은 곧 벽을 덮는 괴물로 자란다. 클래스 사이의 가장
  작은 차이의 뉘앙스를 표현하려고 층 위에 층이 더해진다. 이 더해진 복잡성은 애플리케이션을 더
  부서지기 쉽게 만들 수 있는데, 변경이 많은 층을 오르내리며 파문을 일으킬 수 있기 때문이다**
  (Topic 31).[^thomas2020]
- **더 나쁜 것** — **그러나 더 나쁜 것은 다중 상속 문제다. `Car`는 `Vehicle`의 일종일 수 있지만
  `Asset`·`InsuredItem`·`LoanCollateral` 등의 일종이기도 하다. 이것을 올바르게 모형화하려면
  다중 상속이 필요할 것이다** (Topic 31).[^thomas2020]
- 그런데 그 길이 막혀 있다 — **C++이 1990년대에 미심쩍은 모호성 해소 의미론 때문에 다중 상속에
  나쁜 이름을 붙였다. 그 결과 많은 현행 OO 언어가 그것을 제공하지 않는다. 그래서 복잡한 타입
  나무에 만족한다 해도 당신은 어차피 도메인을 정확히 모형화할 수 없을 것이다** (Topic
  31).[^thomas2020]
  - 이 절에 딸린 클래스 계층 다이어그램은 **아카이브 판에서 유실돼 빈 상자로 렌더된다** —
    직인용 대상에서 제외한다.
- 조문 (Topic 31):[^thomas2020]

> **Tip 51** Don't Pay Inheritance Tax

- 그리고 대안의 예고 — **다시는 상속을 쓸 필요가 없다는 뜻인 세 기법을 제안하겠다** (Topic
  31):[^thomas2020] **인터페이스와 프로토콜**, **위임**, **믹스인과 트레이트**.

## 대안 하나 — 인터페이스와 프로토콜

- 무엇인가 — **대부분의 OO 언어는 클래스가 하나 이상의 행동 집합을 구현한다고 명시할 수 있게 해
  준다. 예컨대 `Car` 클래스가 `Drivable` 행동과 `Locatable` 행동을 구현한다고 말할 수 있다**
  (Topic 31).[^thomas2020] 자바의 표기가 대표 코드다 (Topic 31):[^thomas2020]

  ```java
  public class Car implements Drivable, Locatable {

    // Code for class Car. This code must include
    // the functionality of both Drivable
    // and Locatable

  }
  ```

- 이름의 사정 — **`Drivable`과 `Locatable`은 자바가 **인터페이스**라 부르는 것이다; 다른 언어는
  그것을 **프로토콜**이라 부르고, 어떤 언어는 **트레이트**라 부른다(다만 이것은 나중에 우리가
  트레이트라고 부를 것이 아니다)** (Topic 31).[^thomas2020]
- 성질 — **이 선언들은 코드를 만들지 않는다: 그것은 단지 `Drivable`을 구현하는 어떤 클래스든
  `getSpeed`와 `stop` 두 메서드를 구현해야 하고, `Locatable`인 클래스는 `getLocation`과
  `locationIsValid`를 구현해야 한다고 말할 뿐이다** (Topic 31).[^thomas2020]
- **힘의 원천** — **인터페이스와 프로토콜을 그토록 강력하게 만드는 것은 우리가 그것을 **타입**으로
  쓸 수 있고, 적절한 인터페이스를 구현하는 어떤 클래스든 그 타입과 호환된다는 점이다** (Topic
  31).[^thomas2020] `Car`와 `Phone`이 둘 다 `Locatable`을 구현하면 `List<Locatable>`에 함께
  담을 수 있고 — **모든 항목이 `getLocation`과 `locationIsValid`를 가진다는 지식 위에서 안전하게
  그 목록을 처리할 수 있다** (Topic 31).[^thomas2020]
- 조문과 요약 (Topic 31):[^thomas2020]

> **Tip 52** Prefer Interfaces to Express Polymorphism

  - **인터페이스와 프로토콜은 상속 없는 다형성을 준다** (Topic 31).[^thomas2020]

## 대안 둘 — 위임

- 진단 — **상속은 개발자로 하여금 객체가 많은 수의 메서드를 갖는 클래스를 만들도록 부추긴다. 부모
  클래스에 메서드가 20개 있고 서브클래스가 그중 둘만 쓰고 싶다면, 그 객체는 나머지 18개도 여전히
  놓여 있고 호출 가능한 채로 갖게 된다. 그 클래스는 자기 인터페이스에 대한 통제를 잃었다** (Topic
  31).[^thomas2020]
- 어디서 자주 나오는가 — **이것은 흔한 문제다 — 많은 영속성·UI 프레임워크가 애플리케이션 구성
  요소가 제공된 어떤 기반 클래스를 서브클래싱하기를 고집한다** (Topic 31).[^thomas2020]
  `class Account < PersistenceBaseClass`로 쓰면 — **`Account` 클래스는 이제 영속성 클래스의 모든
  API를 지고 다닌다** (Topic 31).[^thomas2020]
- 대안의 모양 (Topic 31):[^thomas2020]

  ```ruby
  class Account
    def initialize(. . .)
      @repo = Persister.for(self)
    end

    def save
      @repo.save()
    end
  end
  ```

  - 얻는 것 둘 — **우리는 이제 `Account` 클래스의 클라이언트에 프레임워크 API를 **전혀** 노출하지
    않는다: 그 결합이 이제 끊겼다. 그러나 더 있다. 우리가 쓰는 프레임워크의 API에 더 이상 제약받지
    않으므로 우리는 필요한 API를 자유롭게 만들 수 있다. 그렇다, 전에도 그럴 수 있었지만 **우리가**
    쓴 인터페이스가 우회되고 영속성 API가 대신 쓰일 위험이 늘 있었다. 이제 우리는 모든 것을
    통제한다** (Topic 31).[^thomas2020]
- 조문 (Topic 31):[^thomas2020]

> **Tip 53** Delegate to Services: Has-A Trumps Is-A

- **그리고 한 걸음 더** — **사실 우리는 이것을 한 걸음 더 밀 수 있다. 왜 `Account`가 자기 자신을
  영속화하는 법을 알아야 하는가? 계좌 업무 규칙을 알고 강제하는 것이 그 일 아닌가?** (Topic
  31)[^thomas2020] 그래서 `Account`(계좌 관련 사항만)와 `AccountRecord`(가져오고 저장할 수 있는
  능력으로 계좌를 감싸는 것)로 가른다.
- **대가를 저자들이 명시한다** — **이제 우리는 정말로 결합이 끊겼다. 그러나 그것은 비용을 치르고
  왔다. 우리는 더 많은 코드를 써야 하고, 전형적으로 그중 일부는 보일러플레이트일 것이다: 예컨대
  우리의 모든 레코드 클래스가 `find` 메서드를 필요로 할 가능성이 높다** (Topic 31).[^thomas2020]
  이 대가가 다음 대안을 부른다.

## 대안 셋 — 믹스인과 트레이트

- 이름의 혼란부터 — **산업으로서 우리는 것들에 이름 붙이기를 사랑한다. 꽤 자주 같은 것에 많은
  이름을 준다. 많을수록 좋다, 그렇지 않은가?** (Topic 31)[^thomas2020] 저자들은 **믹스인**으로
  통일하되 **정말로 당신이 이것을 언어 불가지론적 기능으로 생각하기를 바란다** (Topic
  31).[^thomas2020]
- 착상 — **기본 착상은 단순하다: 우리는 상속을 쓰지 않고 클래스와 객체를 새 기능성으로 확장할 수
  있기를 원한다. 그래서 우리는 이 함수들의 집합을 만들고, 그 집합에 이름을 주고, 그다음 어떻게든
  클래스나 객체를 그것으로 확장한다. 그 시점에 당신은 원본과 그 모든 믹스인의 능력을 결합한 새
  클래스나 객체를 만든 것이다. 대부분의 경우 확장하려는 클래스의 소스 코드에 접근할 수 없어도 이
  확장을 할 수 있을 것이다** (Topic 31).[^thomas2020]
- 공통 능력 — **중요한 것은 이 모든 구현이 가진 능력이다: **기존의 것**과 **새것** 사이에서
  기능성을 병합하는 것** (Topic 31).[^thomas2020]
- 위임의 보일러플레이트를 푸는 자리 — 표준 파인더 메서드 몇을 믹스인으로 쓰고 영속되는 새 클래스를
  쓸 때마다 그 믹스인을 더한다 (Topic 31):[^thomas2020]

  ```ruby
  mixin CommonFinders {
    def find(id) { ... }
    def findAll() { ... }
  end

  class AccountRecord extends BasicRecord with CommonFinders
  class OrderRecord   extends BasicRecord with CommonFinders
  ```

- **저자들이 더 흥미롭게 보는 용례는 검증이다.** 하나의 계좌에도 적용될 수 있는 검증 층이 여럿이다
  (Topic 31):[^thomas2020] 해시된 비밀번호가 사용자가 입력한 것과 맞는지, 계좌 생성 시 사용자가
  입력한 폼 데이터, 관리자가 사용자 세부를 갱신할 때의 폼 데이터, 다른 시스템 구성 요소가 계좌에
  더한 데이터, 영속되기 전 일관성.
  - 흔한 처방과 그에 대한 평가 — **흔한(그리고 우리가 믿기에 이상적이지 않은) 접근은 모든 검증을
    단일 클래스(업무 객체/영속성 객체)에 묶고, 어느 상황에서 어느 것이 발동할지 통제하는 플래그를
    더하는 것이다** (Topic 31).[^thomas2020]
  - 저자들의 처방 — **우리는 믹스인을 써서 적절한 상황을 위한 특수화된 클래스를 만드는 것이 더 나은
    방법이라고 생각한다** (Topic 31):[^thomas2020]

    ```ruby
    class AccountForCustomer extends Account
        with AccountValidations,AccountCustomerValidations

    class AccountForAdmin extends Account
        with AccountValidations,AccountAdminValidations
    ```

  - 무엇을 사 오는가 — **여기서 두 파생 클래스 모두 모든 계좌 객체에 공통인 검증을 포함한다. 고객
    변형은 고객 대면 API에 적절한 검증도 포함하고, 관리자 변형은 (아마 덜 제한적인) 관리자 검증을
    담는다. 이제 `AccountForCustomer`나 `AccountForAdmin`의 인스턴스를 주고받음으로써 우리 코드는
    **자동으로** 올바른 검증이 적용되도록 보장한다** (Topic 31).[^thomas2020]
  - 이 처방의 요점은 **플래그를 타입으로 바꾸는 것**이다. 어느 검증이 도는지를 실행 시점 분기가
    아니라 값의 타입이 결정하므로, 잘못된 조합을 만드는 자리가 생성 지점 하나로 좁혀진다.
- 조문 (Topic 31):[^thomas2020]

> **Tip 54** Use Mixins to Share Functionality

## 무엇을 언제 고르는가

- 저자들의 기준 — **이 방법 각각은 당신의 목표가 타입 정보를 공유하는 것인지, 기능성을 더하는
  것인지, 메서드를 공유하는 것인지에 따라 서로 다른 상황에서 더 나을 수 있다. 프로그래밍의 다른
  모든 것과 마찬가지로 당신의 의도를 가장 잘 표현하는 기법을 쓰는 것을 목표로 하라** (Topic
  31).[^thomas2020]
- 맺음 — **그리고 정글 전체를 함께 끌고 다니지 않도록 하라** (Topic 31).[^thomas2020]
  - 정리하면 목표별로 — 타입 정보 공유는 **인터페이스·프로토콜**, 기능성 추가는 **믹스인**,
    남의 API를 감춘 채 메서드를 빌려 쓰는 것은 **위임**이다. 셋 다 "무엇을 노출할지 내가
    고른다"는 성질을 공유하고, 상속만이 그 선택권을 부모에게 넘긴다.

## 이 KB의 상속 서술과 나란히

- [디자인 패턴 해부](design-pattern-anatomy.md)는 패턴을 이름·문제·해법·귀결로 적는 카탈로그의
  문법을 다룬다. 이 Topic의 세 대안은 그 문법으로 보면 **같은 문제(행동 공유)에 대한 세 해법이고
  귀결이 서로 다른** 것이다 — 위임은 보일러플레이트를, 믹스인은 이름 충돌 위험을, 인터페이스는
  구현 중복을 남긴다. #hypothesis 마지막 대응은 이 책이 명시하지 않았다.
- [직교성](orthogonality.md)과 [결합 끊기](decoupling.md)가 이 Topic의 상위 근거다. 저자들 자신이
  관련 절로 Topic 8·10·28을 지목한다.

## 이어지는 페이지

- [결합 끊기](decoupling.md) — 이 Topic이 받는 셋째 결합원. 그쪽이 상속을 여기로 미뤘다
- [직교성](orthogonality.md) — 저자들이 지목한 관련 절. 독립성을 설계 성질로 말하는 자리
- [ETC — 바꾸기 쉬운 것이 좋은 설계](etc-easier-to-change.md) — 저자들이 지목한 관련 절(Topic 8)
- [변환 프로그래밍](transforming-programming.md) — 객체가 서로의 상태를 바꾸는 대신 데이터를
  흘리는 쪽
- [디자인 패턴 해부](design-pattern-anatomy.md) — 같은 문제를 패턴 카탈로그의 문법으로 적는 자리
- [실용주의의 유연성과 동시성](../synthesis/pragmatic-flexibility-and-concurrency.md) — 이 축의 허브

[^thomas2020]: Thomas & Hunt 2020, Topic 31 "Inheritance Tax". 곁글("Problems Using Inheritance
    to Build Types", "Mixins, Traits, Categories, Protocol Extensions, …")을 함께 옮겼다.
    앨런 케이 인용은 이 Topic이 2019년 Quora 답변으로 지목한 것이다. Topic 끝의 CHALLENGES는
    독자 과제라 걸러 냈다. 이 아카이브 판에서 타입 계층 다이어그램은 유실돼 직인용 대상에서
    제외했다.

---
type: concept
title: 상속세
description: 상속이 두 갈래 역사(시뮬라의 타입 조합과 스몰토크의 행동 조직)에서 왔고 그 둘이 각각 다른 이유로 오용된다는 진단, 상속이 곧 결합이라는 판정과 부모의 이름 변경이 자식과 그 사용자를 조용히 깨뜨리는 실물, 타입 나무가 벽을 덮는 괴물이 되는 경로와 다중 상속의 벽, 그리고 상속을 대체하는 세 기법(인터페이스와 프로토콜·위임·믹스인)과 각각을 고르는 기준, 그리고 같은 구분을 의도가 아니라 기제로 긋는 소프트웨어 설계 쪽 — 인터페이스 상속은 깊이를 늘리고 구현 상속은 정보 누출을 만든다는 갈림과 상속을 못 버릴 때의 완화책, 같은 약점을 인정하면서도 기본값을 반대로 세우는 셋째 입장 — 먼저 상속을 쓰고 문제가 되면 위임으로 갈아 끼우라는 리팩터링 쪽 판정과 상속을 정당하게 만드는 의미 조건 둘, 그리고 상속을 버릴 수 없는 자리에서 무엇을 지킬 것인가를 일곱 항목으로 적은 넷째 입장과 상속 자체를 거부하는 현대 흐름
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
sources:
  - { id: thomas2020, resource: /it/sources/thomas2020.md }
  - { id: ousterhout2021, resource: /it/sources/ousterhout2021.md }
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
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
- [같은 구분을 기제로 긋는 쪽](#같은-구분을-기제로-긋는-쪽)
- [셋째 입장 — 먼저 쓰고 필요하면 갈아 끼운다](#셋째-입장--먼저-쓰고-필요하면-갈아-끼운다)
- [넷째 입장 — 버릴 수 없을 때 무엇을 지키는가](#넷째-입장--버릴-수-없을-때-무엇을-지키는가)
- [네 소스를 나란히 놓으면](#네-소스를-나란히-놓으면)
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
    [결합 끊기](../concepts/decoupling.md)가 든 결합의 증상 중 "관련 없는 모듈로 전파되는 단순한 변경"의
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

- [디자인 패턴 해부](../concepts/design-pattern-anatomy.md)는 패턴을 이름·문제·해법·귀결로 적는 카탈로그의
  문법을 다룬다. 이 Topic의 세 대안은 그 문법으로 보면 **같은 문제(행동 공유)에 대한 세 해법이고
  귀결이 서로 다른** 것이다 — 위임은 보일러플레이트를, 믹스인은 이름 충돌 위험을, 인터페이스는
  구현 중복을 남긴다. #hypothesis 마지막 대응은 이 책이 명시하지 않았다.
- [직교성](orthogonality.md)과 [결합 끊기](../concepts/decoupling.md)가 이 Topic의 상위 근거다. 저자들 자신이
  관련 절로 Topic 8·10·28을 지목한다.

## 같은 구분을 기제로 긋는 쪽

소프트웨어 설계 쪽 소스도 상속을 둘로 가르지만 **가르는 축이 다르다.** 위
[상속의 두 갈래 역사](#상속의-두-갈래-역사)가 **의도**(코드를 공유하려는가 타입을 만들려는가)로
가른다면, 그쪽은 **기제**(구현을 물려주는가 시그니처만 물려주는가)로 가른다.

- **인터페이스 상속** — **부모 클래스가 메서드 하나 이상의 시그니처를 정의하되 그 메서드를
  구현하지는 않는다** (19장 §19.1, p.153).[^ousterhout2021] 그 판정은 긍정이다 —
  **인터페이스 상속은 같은 인터페이스를 여러 목적으로 재사용함으로써 복잡성에 맞서 지렛대를
  제공한다** (19장 §19.1, pp.153–154).[^ousterhout2021]
- **그리고 그 이득이 측정 가능한 형태로 환산된다** — **이것을 생각하는 또 다른 방법은 깊이의
  관점이다: 인터페이스의 구현이 서로 다른 것이 많을수록 그 인터페이스는 더 깊어진다.
  인터페이스가 많은 구현을 가지려면 그것은 모든 하부 구현의 본질적 특징을 담으면서 구현마다
  다른 상세는 피해야 한다; 이 개념이 추상의 핵심이다** (19장 §19.1,
  p.154).[^ousterhout2021] 깊이의 정의는
  [깊은 모듈과 얕은 모듈](../concepts/deep-and-shallow-modules.md)에 있다.
  - 위 [대안 하나 — 인터페이스와 프로토콜](#대안-하나--인터페이스와-프로토콜)이 인터페이스를
    상속의 **대안**으로 제시하는데, 그쪽은 그것을 상속의 **좋은 절반**으로 분류한다. 결론은
    같고 분류만 다르다.
- **구현 상속** — 이득이 먼저 인정된다. **구현 상속이 없으면 같은 메서드 구현이 여러 하위
  클래스에 복제돼야 할 수도 있고, 그것은 그 하위 클래스들 사이에 의존을 만든다. … 따라서 구현
  상속은 시스템이 진화할 때 수정해야 하는 코드의 양을 줄인다; 다시 말해 2장에서 서술한 변경
  증폭 문제를 줄인다** (19장 §19.1, p.154).[^ousterhout2021]
- **그다음 대가가 위 [상속은 곧 결합이다](#코드를-공유하려는-상속--상속은-곧-결합이다) 절과
  같은 진단으로 적힌다** — **구현 상속은 부모 클래스와 각 하위 클래스 사이에 의존을 만든다.
  부모 클래스의 클래스 인스턴스 변수는 흔히 부모와 자식 클래스 양쪽에서 접근된다; 이것은 상속
  계층의 클래스들 사이에 정보 누출을 낳고 다른 클래스를 보지 않고 계층의 한 클래스를 수정하기
  어렵게 만든다** (19장 §19.1, p.154).[^ousterhout2021]
  - **낱말이 다르다는 것이 중요하다.** 이 Topic은 그것을 **결합**(coupling)이라 부르고 그쪽은
    **정보 누출**(information leakage)이라 부른다. 그쪽의 정의는
    [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md)에 있고, 거기서 누출은 "같은
    지식이 여러 자리에 쓰임"으로 규정된다 — 결합보다 좁고 계측하기 쉬운 개념이다.
- 최악의 경우 — **최악의 경우 프로그래머는 계층의 어느 클래스든 바꾸려면 부모 클래스 아래
  전체 클래스 계층에 대한 완전한 지식이 필요할 것이다. 구현 상속을 광범위하게 쓰는 클래스
  계층은 높은 복잡성을 갖는 경향이 있다** (19장 §19.1, p.154).[^ousterhout2021]
- **처방이 이 Topic보다 한 걸음 물러서 있다.** 이 Topic이 상속을 쓰지 말라고 하는 데 비해
  그쪽은 조건부다 — **구현 상속은 조심해서 써야 한다. 구현 상속을 쓰기 전에 합성에 기반한
  접근이 같은 이득을 줄 수 있는지 검토하라. 예컨대 작은 도우미 클래스를 써서 공유 기능을
  구현하는 것이 가능할 수 있다** (19장 §19.1, pp.154–155).[^ousterhout2021] 그 합성이 위
  [대안 둘 — 위임](#대안-둘--위임)의 기제다.
- **그리고 그쪽에는 이 Topic에 없는 완화책이 하나 더 있다** — **구현 상속에 실행 가능한
  대안이 없다면 부모 클래스가 관리하는 상태와 하위 클래스가 관리하는 상태를 분리하려 하라.
  한 방법은 어떤 인스턴스 변수를 전적으로 부모 클래스의 메서드가 관리하게 하고, 하위 클래스는
  그것을 읽기 전용으로만 또는 부모 클래스의 다른 메서드를 통해서만 쓰게 하는 것이다. 이것은
  정보 은닉의 개념을 클래스 계층 안에 적용해 의존을 줄인다** (19장 §19.1,
  p.155).[^ousterhout2021]
  - **상속을 못 버릴 때의 처방**이라는 점에서 이 Topic의 세 대안과 층이 다르다. 그쪽은
    상속을 남긴 채 그 안에서 정보 은닉을 다시 적용한다.
- 두 소스가 서로를 참조한 적은 없다. 그쪽의 여섯 유행 평가 전문은
  [소프트웨어 유행을 잣대로 재기](../concepts/evaluating-software-trends.md)에 있다.

## 셋째 입장 — 먼저 쓰고 필요하면 갈아 끼운다

같은 대상에 대해 셋째 소스가 **반대 방향의 기본값**을 세운다. 앞의 두 소스가 상속을 쓰기 전에
멈추라고 하는 데 비해, 리팩터링(refactoring) 카탈로그 쪽은 **먼저 상속을 쓰고 문제가 되면
갈아 끼우라**고 한다. 갈리는 것은 상속의 위험도가 아니라 **되돌릴 수 있는가에 대한 신뢰**다.

- **원칙 자체는 같은 것을 인용하되 통상적 해석을 기각한다** (12장 §"Replace Subclass with
  Delegate", p.382):[^fowler2018]

> There is a popular principle: "Favor object composition over class inheritance" (where
> composition is effectively the same as delegation). Many people take this to mean
> "inheritance considered harmful" and claim that we should never use inheritance. I use
> inheritance frequently, partly because I always know I can use Replace Subclass with
> Delegate should I need to change it later. Inheritance is a valuable mechanism that does
> the job most of the time without problems. So I reach for it first, and move onto
> delegation when it starts to rub badly.

- **그 해석이 원칙의 출처와도 어긋난다고 지적한다** — **이 용법은 실은 그 원칙과 일관된다. 그
  원칙은 상속과 합성(composition)이 어떻게 함께 동작하는지 설명하는 4인방 책에서 왔다. 그
  원칙은 상속의 과용에 대한 반작용이었다** (12장 §"Replace Subclass with Delegate",
  p.382).[^fowler2018]
- **상속을 정당하게 만드는 의미 조건 둘이 명시된다** — **적절한 의미 조건이 적용되는 한(상위
  타입의 모든 메서드가 하위 타입에 적용되고, 하위 타입의 모든 인스턴스가 상위 타입의
  인스턴스라면) 상속은 단순하고 효과적인 기제다. (…) 그러니 내 조언은 (대체로) 상속을 먼저
  쓰고, 그것이 문제가 될 때(그리고 되면) Replace Superclass with Delegate를 적용하라는
  것이다** (12장 §"Replace Superclass with Delegate", p.400).[^fowler2018]
  - 이 두 조건은 이 페이지의 [타입을 만들려는 상속](#타입을-만들려는-상속--벽을-덮는-나무)이
    진단하는 실패와 같은 것을 반대로 진술한 것이다. 그쪽이 조건을 어기는 나무를 보여 준다면
    이쪽은 조건을 지키는 한 써도 된다고 말한다.
- **진단 자체는 겹친다.** 이 소스도 상속의 약점 둘을 든다 — **한 번만 낼 수 있는 카드**(변이
  축이 하나뿐이다)와 **매우 가까운 관계**(부모의 변경이 자식을 쉽게 깨뜨린다) (12장 §"Replace
  Subclass with Delegate", p.382).[^fowler2018] 위
  [코드를 공유하려는 상속](#코드를-공유하려는-상속--상속은-곧-결합이다)의 진단과 같다.
- **갈리는 것은 처방의 시점이다.** 이쪽은 되돌리는 항목 둘(*Replace Subclass with Delegate*,
  *Replace Superclass with Delegate*)을 손에 쥐고 있으므로 처음 선택을 보수적으로 하지 않는다.
  #hypothesis 세 소스 중 어느 것도 서로를 인용하지 않았고, 이 차이를 모순이 아니라 관점 차이로
  판정한 근거는 두 가지다 — 세 소스가 같은 약점을 인정하고, 갈리는 명제가 "상속이 위험한가"가
  아니라 "나중에 갈아 끼우는 비용을 얼마로 보는가"라는 계량이다.
- 전문과 나머지 아홉 항목은 [상속 다루기 리팩터링](refactoring-inheritance.md)에 있다.

## 넷째 입장 — 버릴 수 없을 때 무엇을 지키는가

넷째 소스는 **언어 참조서**라 앞의 셋과 층이 다르다. 상속을 쓸 것인가를 먼저 논하지 않고
**이미 쓰고 있는 자리에서 무엇을 지킬 것인가**를 목록으로 준다. 그 전제를 저자가 밝힌다 —
**그러나 우리는 복잡한 클래스 계층으로 설계된 기존 시스템을 유지보수해야 하거나, 상속을 —
때로는 다중 상속까지 — 쓰도록 강요하는 프레임워크를 써야 한다** (14장 도입,
p.488).[^ramalho2022]

- 이 목록에 이론적 근거가 없다는 것을 저자가 먼저 인정한다 — **앨런 케이가 경구에서 쓴 것은
  여전히 참이다: 실무 프로그래머를 이끌 수 있는 상속에 대한 일반 이론이 아직 없다. 우리가
  가진 것은 경험 법칙, 디자인 패턴, "모범 사례", 영리한 두문자어, 금기 같은 것들이다. 그중
  일부는 유용한 지침을 주지만 어느 것도 보편적으로 받아들여지거나 항상 적용 가능하지 않다**
  (14장 §"Coping with Inheritance", p.510).[^ramalho2022]
  - 그리고 다중 상속이 없어도 마찬가지라는 단서가 붙는다 — **다중 상속 없이도 상속으로
    이해할 수 없고 부서지기 쉬운 설계를 만들기는 쉽다** (같은 절, p.510).[^ramalho2022]

**일곱 항목**은 이렇다 (14장 §"Coping with Inheritance", pp.510–513).[^ramalho2022]

- **하나 — 클래스 상속보다 객체 합성을 선호하라.** 저자가 이것을 **"내가 여기서 줄 수 있는
  최선의 조언"**이라 부르고 출처를 밝힌다 — 디자인 패턴 책의 두 번째 객체 지향 설계 원칙이다.
  진단이 하나 붙는다 — **일단 상속에 편안해지면 그것을 과용하기가 너무 쉽다. 객체를 깔끔한
  계층에 놓는 것은 우리의 질서 감각에 호소한다; 프로그래머는 재미로도 그것을 한다** (p.510).
  - 위 [대안 둘 — 위임](#대안-둘--위임)이 같은 기제를 말한다. 이쪽이 더하는 것은 **단일
    상속에서도 그 원칙이 값을 갖는다**는 단서다 — **단일 상속에서조차 이 원칙은 유연성을
    높이는데, 서브클래싱이 단단한 결합의 한 형태이고 높은 상속 나무는 부서지기 쉬운 경향이
    있기 때문이다** (p.510).
  - **그리고 대체 불가능한 자리를 명시한다** — **합성과 위임은 서로 다른 클래스에 행동을
    제공하기 위한 믹스인의 사용을 대체할 수 있지만, 타입의 계층을 정의하기 위한 인터페이스
    상속을 대체할 수는 없다** (p.510).
- **둘 — 각 경우에 상속이 왜 쓰이는지를 이해하라.** 주된 이유가 둘이다 (p.510):
  **인터페이스 상속은 하위 타입을 만들며 "is-a" 관계를 함의한다. 이것은 ABC로 하는 것이
  최선이다.** 그리고 **구현 상속은 재사용으로 코드 중복을 피한다. 믹스인이 이것을 도울 수
  있다.**
  - 실무에서 둘이 겹친다는 것을 인정하되 처방이 뒤따른다 — **실무에서 두 용도는 흔히 동시에
    일어나지만, 의도를 분명히 할 수 있을 때는 언제나 그렇게 하라. 코드 재사용을 위한 상속은
    구현 세부이고 흔히 합성과 위임으로 대체될 수 있다. 반면 인터페이스 상속은 프레임워크의
    등뼈다** (p.511).
  - **이 구분이 위 [같은 구분을 기제로 긋는 쪽](#같은-구분을-기제로-긋는-쪽)과 같은 축이다** —
    인터페이스 상속과 구현 상속을 갈라 앞의 것만 긍정하는 것까지 똑같다. 다른 것은 처방의
    구체성이다. 그쪽이 "조심해서 쓰라"에서 멈춘다면 이쪽은 무엇을 기반 클래스로 삼을지까지
    지정한다.
- **셋 — ABC로 인터페이스를 명시적으로 만들라** — **현대 파이썬에서 클래스가 인터페이스를
  정의하려는 것이라면 그것은 명시적 ABC이거나 `typing.Protocol` 하위 클래스여야 한다. ABC는
  `abc.ABC`나 다른 ABC만 상속해야 한다. ABC의 다중 상속은 문제가 되지 않는다** (p.511).
  그 둘의 선택 기준은 [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)에 있다.
- **넷 — 코드 재사용에는 명시적 믹스인을 쓰라** (p.511):

> If a class is designed to provide method implementations for reuse by multiple unrelated
> subclasses, without implying an "is-a" relationship, it should be an explicit *mixin
> class*. Conceptually, a mixin does not define a new type; it merely bundles methods for
> reuse. A mixin should never be instantiated, and concrete classes should not inherit only
> from a mixin. Each mixin should provide a single specific behavior, implementing few and
> very closely related methods. Mixins should avoid keeping any internal state; i.e., a
> mixin class should not have instance attributes.

  - **"내부 상태를 갖지 말라"가 위 [대안 셋 — 믹스인과 트레이트](#대안-셋--믹스인과-트레이트)에
    없던 제약이다.** 상태 없는 메서드 묶음이라는 조건이 붙으면 믹스인은 사실상 이름 붙은
    함수 집합이 되고, 그것이 이름 충돌 말고는 위험을 만들지 않는 이유가 된다.
  - 표시 방법에 대한 규약도 있다 — **파이썬에는 클래스가 믹스인이라고 말하는 형식적 방법이
    없으므로 `Mixin` 접미로 이름 짓기를 강력히 권한다** (p.511).
- **다섯 — 사용자에게 집합 클래스를 제공하라.** 정의를 Booch 등에서 인용한다 — **주로
  믹스인들에서 상속함으로써 구성되고 자기 자신의 구조나 행동을 더하지 않는 클래스를
  집합 클래스(aggregate class)라 부른다** (p.511). 처방 — **ABC나 믹스인의 어떤 조합이
  클라이언트 코드에 특히 유용하다면, 그것들을 합당한 방식으로 한데 모으는 클래스를 제공하라**
  (p.511).
  - 값이 무엇인지가 실물로 적힌다 — 본문이 비어 있는 장고의 `ListView`는 **함께 쓰여야 할
    믹스인과 기반 클래스를 한데 모으는 쓸모 있는 서비스를 제공한다** (p.512). Tkinter의
    `Widget`도 같다 — **그 집합 클래스 덕분에 우리는 필요한 믹스인들로 새 위젯을 만들 수
    있다. 의도대로 동작하려면 그것들이 어떤 순서로 선언되어야 하는지 알아낼 필요 없이**
    (p.512).
  - **선언 순서라는 지식이 어디에 사는지가 이 항목의 요점이다.** 협력적 다중 상속이 요구하는
    순서 지식(→ [협력적 다중 상속과 MRO](../concepts/cooperative-multiple-inheritance.md))을 라이브러리가
    한 자리에 흡수해 사용자에게 넘기지 않는 것이다.
- **여섯 — 서브클래싱을 위해 설계된 클래스만 상속하라.** 이 항목은 기술 검토자 Leonardo
  Rochael의 경고를 그대로 실은 것이다 (p.512):

> Subclassing any complex class and overriding its methods is error-prone because the
> superclass methods may ignore the subclass overrides in unexpected ways. As much as
> possible, avoid overriding methods, or at least restrain yourself to subclassing classes
> which are designed to be easily extended, and only in the ways in which they were designed
> to be extended.

  - **그 다음 물음이 이 항목을 실행 가능하게 만든다** — **훌륭한 조언이다. 그러나 어떤 클래스가
    확장되도록 설계됐는지 또는 어떻게 설계됐는지를 우리가 어떻게 아는가?** (p.512) 답이 둘이다.
    **첫째 답은 문서다**(독스트링이나 코드 주석의 형태일 때도 있다) — 저자가 드는 실물이
    `socketserver` 패키지로, 그 문서와 소스의 독스트링이 **어느 메서드가 하위 클래스에 의해
    오버라이드되도록 의도됐는지를 명시적으로 적는다.**
    - 버전 조건: 파이썬 3.8 이상 — 둘째 답이 PEP 591의 `@final` 데코레이터다. **그것을
      클래스나 개별 메서드에 적용하면 IDE나 타입 검사기가 그 클래스를 상속하거나 그 메서드를
      오버라이드하려는 잘못된 시도를 보고할 수 있다** (p.512).
  - 이 항목이 위 [코드를 공유하려는 상속](#코드를-공유하려는-상속--상속은-곧-결합이다)의
    "조용히 깨진다"에 대한 부분적 답이다. **계약이 없어서 신호가 없었다면, 계약을 문서와
    타입 검사기 양쪽에 적어 신호를 만든다.**
- **일곱 — 구상 클래스 상속을 피하라** — **구상 클래스를 서브클래싱하는 것은 ABC와 믹스인을
  서브클래싱하는 것보다 위험한데, 구상 클래스의 인스턴스는 대개 내부 상태를 갖고 그 상태에
  의존하는 메서드를 오버라이드할 때 그것이 쉽게 훼손될 수 있기 때문이다. 당신의 메서드가
  `super()`를 불러 협력하고 내부 상태가 `__x` 문법의 비공개 속성에 담겨 있더라도, 메서드
  오버라이드가 버그를 들일 방법은 여전히 수없이 많다** (p.513).
  - 저자가 이 항목의 출처를 13장으로 넘긴다 — Alex Martelli가 Scott Meyer의 *More Effective
    C++*를 인용한 **"모든 비말단 클래스는 추상이어야 한다"**가 그것이다 (p.513).
  - 그리고 탈출구를 남긴다 — **코드 재사용을 위해 서브클래싱을 반드시 써야 한다면, 재사용을
    의도한 코드는 ABC의 믹스인 메서드나 명시적으로 이름 지어진 믹스인 클래스에 있어야 한다**
    (p.513).

**그리고 이 소스가 상속 거부의 현대 흐름을 명시적으로 기록한다.**

- 장 요약의 맺음 — **상속을 — 단일 상속조차 — 거부하는 것은 현대의 흐름이다. 21세기에 만들어진
  가장 성공적인 언어 중 하나는 Go다. 그것은 "클래스"라 불리는 구성물을 갖지 않지만 캡슐화된
  필드의 구조체인 타입을 지을 수 있고 그 구조체에 메서드를 붙일 수 있다. Go는 컴파일러가
  구조적 타이핑, 다시 말해 *정적 덕 타이핑*으로 검사하는 인터페이스의 정의를 허용한다 —
  파이썬 3.8부터 프로토콜 타입으로 우리가 갖게 된 것과 매우 비슷하다. Go는 합성으로 타입과
  인터페이스를 짓는 특별한 문법을 갖지만 상속을 지원하지 않는다 — 인터페이스 사이에서조차**
  (14장 §"Chapter Summary", p.515).[^ramalho2022]
- **조건부 결론이 이 소스의 최종 판정이다** (14장 §"Chapter Summary",
  p.515):[^ramalho2022]

> So perhaps the best advice about inheritance is: avoid it if you can. But often, we don't
> have a choice: the frameworks we use impose their own design choices.

- 읽을거리 절이 Hynek Schlawack의 문장을 경구로 세운다 (14장 §"Further Reading",
  p.515):[^ramalho2022]

> When it comes to reading clarity, properly-done composition is superior to inheritance.
> Since code is much more often read than written, avoid subclassing in general, but
> especially don't mix the various types of inheritance, and don't use subclassing for code
> sharing.

  - 그 글의 저자가 `attrs` 패키지의 제작자이자 Twisted 비동기 프레임워크의 핵심 기여자였고,
    **시간이 지나면서 핵심 팀은 자기 설계에서 서브클래싱을 과용했다는 것을 깨달았다**고 저자가
    적는다 (같은 절, p.515).[^ramalho2022]
  - 같은 글의 다른 한 줄에 저자가 동의를 표한다 — **"더 자주는, 함수 하나면 충분하다는 것을
    잊지 마라." 나는 동의하고, 그것이 정확히 *Fluent Python*이 클래스와 상속보다 함수를 먼저
    깊이 다루는 이유다** (14장 §"Further Reading", p.515).[^ramalho2022] 그 함수 쪽 축이
    [파이썬의 함수를 객체로 다루기](../synthesis/python-functions-as-objects.md)다.

## 네 소스를 나란히 놓으면

- **갈리는 명제가 하나다: 상속을 처음부터 피할 것인가.** 첫째 소스는 피하라 하고, 둘째는
  구현 상속만 조심하라 하고, 셋째는 먼저 쓰고 갈아 끼우라 하고, 넷째는 **피할 수 있으면
  피하되 대개 선택권이 없다**고 한다.
- **네 소스가 진단에서는 겹친다.** 상위·하위 클래스가 단단히 결합한다는 것, 그 결합이 조용히
  깨진다는 것, 인터페이스를 물려주는 상속만은 값이 있다는 것 — 이 셋을 넷 다 말한다.
- **그래서 `contradicts`로 판정하지 않았다.** 근거 둘이다. ⑴ 네 소스가 같은 약점을 인정하므로
  사실 주장이 충돌하지 않는다. ⑵ 갈리는 것은 "상속이 위험한가"가 아니라 **되돌리는 비용을
  얼마로 보는가**와 **누구를 독자로 두는가**라는 계량이다. 넷째 소스는 특히 **응용 개발자와
  프레임워크 저자를 명시적으로 갈라 두고**(14장 곁글 §"Think about the Classes You Really
  Need", p.517)[^ramalho2022] 앞의 조언들이 전자에게 더 강하게 적용된다고 본다 — **우리가
  코딩하는 클래스는 거의 항상 잎 클래스다.**
- #hypothesis 네 소스 중 어느 것도 서로를 인용하지 않았다. 다만 넷째와 셋째가 같은 원전을
  가리킨다 — 디자인 패턴 책의 "클래스 상속보다 객체 합성을 선호하라"이고, 셋째가 그 원칙의
  통상적 해석을 기각한 자리와 넷째가 그것을 최선의 조언이라 부른 자리가 같은 문장이다.

## 이어지는 페이지

- [상속 다루기 리팩터링](refactoring-inheritance.md) — **셋째 입장의 전문.** 계층을 고치는
  열한 항목과 상속을 위임으로 바꾸는 두 항목
- [결합 끊기](../concepts/decoupling.md) — 이 Topic이 받는 셋째 결합원. 그쪽이 상속을 여기로 미뤘다
- [직교성](orthogonality.md) — 저자들이 지목한 관련 절. 독립성을 설계 성질로 말하는 자리
- [ETC — 바꾸기 쉬운 것이 좋은 설계](../concepts/etc-easier-to-change.md) — 저자들이 지목한 관련 절(Topic 8)
- [변환 프로그래밍](transforming-programming.md) — 객체가 서로의 상태를 바꾸는 대신 데이터를
  흘리는 쪽
- [디자인 패턴 해부](../concepts/design-pattern-anatomy.md) — 같은 문제를 패턴 카탈로그의 문법으로 적는 자리
- [협력적 다중 상속과 MRO](../concepts/cooperative-multiple-inheritance.md) — **넷째 입장의 기제 쪽.**
  `super()`와 메서드 결정 순서, 그리고 믹스인이 실제로 동작하는 조건
- [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md) — 같은 소스가 드는, 상속이
  언어 구현 층에서 새는 자리
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 넷째 입장이 "인터페이스라면
  ABC이거나 `Protocol`이어야 한다"고 말할 때 그 둘의 선택 기준
- [실용주의의 유연성과 동시성](../synthesis/pragmatic-flexibility-and-concurrency.md) — 이 축의 허브
- [파이썬의 상속 기제](../synthesis/python-inheritance-mechanics.md) — 넷째 소스 쪽의 허브

[^thomas2020]: Thomas & Hunt 2020, Topic 31 "Inheritance Tax". 곁글("Problems Using Inheritance
    to Build Types", "Mixins, Traits, Categories, Protocol Extensions, …")을 함께 옮겼다.
    앨런 케이 인용은 이 Topic이 2019년 Quora 답변으로 지목한 것이다. Topic 끝의 CHALLENGES는
    독자 과제라 걸러 냈다. 이 아카이브 판에서 타입 계층 다이어그램은 유실돼 직인용 대상에서
    제외했다.

[^ousterhout2021]: Ousterhout 2021, 19장 "Software Trends" §19.1 "Object-oriented programming and inheritance". 쪽은 인쇄판 쪽 번호. 이 장에는 코드 예제도
    도판도 없다.

[^fowler2018]: Fowler 2018, 12장 "Dealing with Inheritance" §"Replace Subclass with
    Delegate"(pp.381–382) · §"Replace Superclass with Delegate"(pp.399–400). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준
    규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 항목의 Example 절과
    스케치 도판은 옮기지 않았다.

[^ramalho2022]: Ramalho 2022, 14장 "Inheritance: For Better or for Worse" 도입(p.488) ·
    §"Coping with Inheritance"(p.510)과 그 아래 일곱 절 §"Favor Object Composition over Class
    Inheritance"(p.510)·§"Understand Why Inheritance Is Used in Each Case"(pp.510–511)·
    §"Make Interfaces Explicit with ABCs"(p.511)·§"Use Explicit Mixins for Code Reuse"
    (p.511)·§"Provide Aggregate Classes to Users"(pp.511–512)·§"Subclass Only Classes
    Designed for Subclassing"(p.512)·§"Avoid Subclassing from Concrete Classes"(p.513) ·
    §"Chapter Summary"(p.515) · §"Further Reading"(p.515) · 곁글 §"Think about the Classes
    You Really Need"(p.517). **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀
    값이고, 그 오프셋 실측과 판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이
    정본이다. 이 절은 이 소스가 이 페이지에 더하는 것만 든다 — `super()`·MRO·믹스인의 기제와
    내장 타입 상속의 함정은 [협력적 다중 상속과 MRO](../concepts/cooperative-multiple-inheritance.md)와
    [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md)이 갖는다. §"Coping with
    Inheritance" 아래 마지막 절 §"Tkinter: The Good, the Bad, and the Ugly"(pp.513–514)는
    일곱 지침을 하나의 사례에 적용해 보이는 자리라 그 허브 쪽 페이지에 남겼다.

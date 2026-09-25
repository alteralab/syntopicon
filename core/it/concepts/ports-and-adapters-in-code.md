---
type: concept
title: 코드로 본 포트와 어댑터
description: 헥사고날(포트와 어댑터) 아키텍처의 규정이 코드에서 어디에 서는지를 원저자 콕번의 세 코드 사례로 보이는 페이지 — 세금 계산기(자바·루비)에서 구동 포트가 앱이 구현하는 인터페이스이고 피구동 포트가 앱이 생성자 인수로 요구하는 인터페이스이며 main()이 Configurator이자 구동 액터라는 대응, 생성자 주입과 세터 주입의 가름과 세터 주입의 위험, 의존성 주입과 의존성 조회(브로커·Configurable Receiver)의 가름, web-hexagon 사례가 보이는 "목 저장소로 첫 시험이 통과하면 아키텍처는 이미 선다"와 인메모리에서 파일과 웹으로 자라도 앱은 그대로라는 것, 그리고 BlueZone 사례가 보이는 액터 종류 수가 포트 수를 정한다는 것과 포트마다 다른 기술·다른 테스트 대역을 꽂는 실물
generated: { by: "claude-opus-4.8", at: "2026-09-25T00:00:00Z" }
sources:
  - { id: cockburn2024, resource: /it/sources/cockburn2024.md }
---

# 코드로 본 포트와 어댑터

- [이 페이지가 담는 것](#이-페이지가-담는-것)
- [세금 계산기 — 코드에서 요소가 서는 자리](#세금-계산기--코드에서-요소가-서는-자리)
- [web-hexagon — 아키텍처는 첫 시험에서 이미 선다](#web-hexagon--아키텍처는-첫-시험에서-이미-선다)
- [BlueZone — 액터 종류의 수가 포트 수를 정한다](#bluezone--액터-종류의-수가-포트-수를-정한다)
- [이어지는 페이지](#이어지는-페이지)

## 이 페이지가 담는 것

패턴의 규정은 [포트와 어댑터 규정](../concepts/ports-and-adapters-defined.md)에 있다. 이 페이지는 그 규정이
**코드에서 어디에 서는지** — 어느 줄이 포트이고 어느 클래스가 어댑터이며 무엇이 Configurator인지 —
를 원저자 콕번(Alistair Cockburn)과 후안 마누엘 가리도 데 파스(Juan Manuel Garrido de Paz)의
세 코드 사례로 짚는다. 저자는 이 패턴을 이해하는 가장 좋은 길이 여러 언어·여러 환경의 코드를 읽고
실험하는 것이라 말하며, 가장 단순한 것부터 가장 복잡한 것으로 사례를 잇는다
(3장 도입).[^cockburn2024] 여기 담는 것은 각 사례가 규정의 무엇을 보이는가일 뿐, 코드 자체의
정본은 사례를 공개한 저자의 저장소다.

저자는 책을 요약하는 7장에서 이 코드로 되돌아와 그 무게를 못 박는다 — **이 책의 모든 쪽은
결국 이 코드 조각을 당신의 더 큰 시스템에 복제하도록 돕는 것일 뿐**이라는 것이다
(7장 §"7.2. The sample code to copy").[^cockburn2024] 세금 계산기의 자바 판과 루비 판을 다시
실은 뒤, 그 작은 코드가 어떻게 짜였고 왜 그렇게 하며 당신의 환경에서 어떻게 돌아가게 하는지를
풀어내는 데 그토록 많은 말이 든 것이니 그 코드를 작업 공간에 복사해 거기서부터 바꾸고 키우라고
적는다 (7장 §"7.2").[^cockburn2024] 맺음말에서도 같은 것을 다른 말로 짚는다 — **코드가 패턴의
서술보다 훨씬 단순하며, 바로 그래서 이 책이 처음과 마지막 절에 코드를 보인다** (Fin).[^cockburn2024]

## 세금 계산기 — 코드에서 요소가 서는 자리

- 첫 사례는 세금 계산기다. 저자는 계산기가 필요한 만큼 단순하거나 복잡할 수 있어 골랐다고 적고,
  구동 포트 하나와 피구동 포트 하나로 시작한다 — 구동 포트는 `tax_on(amount)` 함수 하나만 내놓는다
  (3장 §"3.1. The simplest example: the tax calculator").[^cockburn2024]
- 저자가 자바로 먼저 보이는 이유는 자바가 포트를 명시적으로 선언해 눈에 드러내기 때문이다
  (3장 §"3.1. The simplest example…", "The simplest tax calculator (Java)"). 아래는 그 자바
  코드로, 규정의 네 요소가 어느 줄에 서는지를 보인다:[^cockburn2024]

  ```java
  interface ForCalculatingTaxes {
      double taxOn(double amount);
  }

  interface ForGettingTaxRates {
      double taxRate(double amount);
  }

  class TaxCalculator implements ForCalculatingTaxes {
      private ForGettingTaxRates taxRateRepository;

      public TaxCalculator(ForGettingTaxRates taxRateRepository) {
          this.taxRateRepository = taxRateRepository;
      }

      public double taxOn(double amount) {
          return amount * taxRateRepository.taxRate(amount);
      }
  }

  class FixedTaxRateRepository implements ForGettingTaxRates {
      public double taxRate(double amount) {
          return 0.15;
      }
  }

  class Main {
      public static void main(String[] args) {
          ForGettingTaxRates taxRateRepository = new FixedTaxRateRepository();
          ForCalculatingTaxes myCalculator = new TaxCalculator(taxRateRepository);
          System.out.println(myCalculator.taxOn(100));
      }
  }
  ```

- 저자가 이 코드에 다는 대응이 규정과 코드를 잇는 자리다
  (3장 §"3.1. The simplest example…"):[^cockburn2024]
  - `ForCalculatingTaxes`가 **구동 포트**다 — 이 단계에서는 `taxOn(amount)` 함수 하나만 내놓는다.
  - `ForGettingTaxRates`가 **피구동 포트**다 — 모든 저장소가 `taxRate(amount)` 함수를 지원하도록
    요구한다.
  - `TaxCalculator`가 구동 포트를 **구현하고** 피구동 포트를 **쓴다** — 이것이 앱이다.
  - `FixedTaxRateRepository`가 피구동 포트를 구현한다 — 모든 요율 저장소가 그렇게 한다.
  - `Main`이 Configurator이자, 이 작은 경우에는 구동 액터 노릇까지 한다. 앞 두 줄이 Configurator로서
    `FixedTaxRateRepository`를 만들어 생성 시점에 `TaxCalculator`에 먹이고, 마지막 줄이 여느
    사용자처럼 구동 포트를 쓴다.
- 같은 코드를 루비로 옮기면 포트가 코드에서 사라진다 — **루비에서는 포트와 인터페이스를 선언할
  필요가 없어 그것들이 어디 있는지 보기 어렵다**
  (3장 §"3.1. The simplest example…", "The simplest tax calculator (Ruby)").[^cockburn2024] 이
  관찰의 파이썬 쪽 전문은 [의존성 역전 원칙](../concepts/dependency-inversion-principle.md)의
  "포트와 어댑터가 파이썬에서 무엇인가"에 있다.
- 피구동 액터를 앱에 꽂는 방식이 하나가 아니라는 것을 저자가 사례로 가른다
  (3장 §"3.1. The simplest example…", "Using a setter instead of constructor argument
  (Java)"):[^cockburn2024] 생성자 인수로 넣는 **생성자 주입** 대신 세터 메서드로 넣는 **세터
  주입**도 똑같이 유효하고, 세터 주입은 피구동 액터를 언제든 바꿀 수 있게 한다. 다만 위험이
  하나 따른다 — 앱을 만들고 피구동 액터를 끝내 설정하지 않아 앱을 **일관성 없는 상태**로 남길 수
  있다. 저자는 오래 도는 시스템에는 세터 주입이 필요하므로 시험이 그 위험을 덜어야 한다고 적으면서,
  두 저자 모두 그런 시스템 경험이 없어 더 말하지 못한다고 밝힌다.
- 피구동 액터를 고르는 방식도 하나가 아니다 — 저자는 고정 요율 저장소 대신 **브로커**를 두어
  **의존성 주입이 아니라 의존성 조회(dependency lookup)**로 피구동 액터를 설정하는 사례를 더한다
  (3장 §"3.1. The simplest example…", "Using a broker instead of a fixed rate repository
  (Ruby)").[^cockburn2024] 요율 저장소 브로커가 나라마다 어느 요율 저장소를 쓸지 알려 주므로
  나라별 세율표를 갈아 끼우거나 나라의 공식 세무 당국에 직접 잇는 어댑터를 둘 수 있다. 이를 위해
  피구동 포트 `ForGettingCountryBasedTaxRateRepository`(함수 `RepositoryForCountry(country)`)를
  하나 더 들이고, 그 포트를 시험할 테스트 대역과 프로덕션 브로커, 그리고 브로커를 위한 Configurator가
  차례로 따라온다 — 포트가 하나 늘 때마다 대역과 설정이 함께 는다.

## web-hexagon — 아키텍처는 첫 시험에서 이미 선다

- 둘째 사례는 콕번이 2010년대에 루비로 지은 콘텐츠 관리 시스템에서 웹 서비스를 구동 액터로 잇느라
  만든 web-hexagon이다 (3장 §"3.2. Another simple example, the web-hexagon").[^cockburn2024] 도메인의
  복잡도가 관심이 아니었으므로 앞 사례의 사소한 세금 계산기 도메인을 그대로 재사용해 아키텍처를
  쉽게 세우고, 거기에 Rack을 얹는 것을 큰 발걸음으로 삼는다.
- 이 사례가 보이는 규정은 **아키텍처가 언제 서는가**다 — **첫 시험은 목(mock) 저장소를 쓰며, 이것만으로
  포트와 어댑터 아키텍처를 세우기에 충분하다** (3장 §"3.2. Another simple example…").[^cockburn2024]
  그 첫 시험에서 인메모리 저장소를 생성자로 넣는 순간 세금 계산용 구동 포트 하나와 요율 취득용
  피구동 포트 하나가 이미 자리를 잡고, 루비라 포트 자체는 눈에 안 보일 뿐이다.
- 그 위에서 기술을 갈아 끼워도 앱은 그대로다 — 저자는 인메모리 요율기에서 파일 요율기(어댑터로
  파일 리더를 더함)로, 다시 앞단의 Rack 웹 인터페이스로 키워 가며, **시험에서든 브라우저에서든 앱을
  구동하고 인메모리 요율기에서든 파일에서든 요율을 얻을 수 있다**고 보인다
  (3장 §"3.2. Another simple example…").[^cockburn2024] 앱을 다시 컴파일하지 않고 바깥만 바뀐다는
  것이 이 사례의 요지다.

## BlueZone — 액터 종류의 수가 포트 수를 정한다

- 셋째 사례는 후안이 만든 온전한 사례 BlueZone으로, 운전자가 웹 UI로 도시 구역의 주차 요금을
  치르고 주차 단속원이 정산을 확인하는 시스템이다 (3장 §"3.3. The BlueZone example").[^cockburn2024]
  저자는 후안이 코드를 계속 진화시켜 두 저장소에 두 설계를 남겼고 책이 그 변화를 따라갈 수 없어 한
  설계의 윤곽만 그린다고 밝히므로, 코드 정본은 후안의 저장소다.
- 이 사례가 보이는 규정은 **액터 종류의 수가 포트 수를 정한다**는 것이다 — 구동(primary) 액터는
  차량 운전자와 주차 단속원 둘, 피구동(secondary) 액터는 구역별 요율 저장소·티켓 저장소·결제
  서비스 셋이다. **그래서 구동 액터 둘과 피구동 액터 셋에 포트가 다섯이고, 설정 작업을 위해 하나를
  더 둘 수 있다** (3장 §"3.3. The BlueZone example", 그림 3.1).[^cockburn2024] 포트는 이렇게 선다 —
  구동 `ForParkingCars`·`ForCheckingCars`, 피구동 `ForObtainingRates`·`ForStoringTickets`·`ForPaying`,
  그리고 구동 `ForConfiguringApp`이다. 피구동 액터는 앱의 생성자에서 설정되고, 그 밖의 설정은 "for
  configuring" 포트를 지난다. 포트가 의도별 대화라는 규정은 [포트와 어댑터
  규정](../concepts/ports-and-adapters-defined.md)에 있다.
- 마지막으로 이 사례는 **포트마다 다른 기술과 다른 테스트 대역**을 꽂아 보인다 — 후안은 운전자에
  웹, 단속원에 명령줄, 요율에 파일, 티켓에 SQL 데이터베이스, 결제에 결제 시스템 게이트웨이를 골랐고,
  포트마다 다른 대역(파일에 스텁, 데이터베이스에 가짜, 결제 게이트웨이에 스파이)을 두어 서로 다른
  기술과 시험을 예시한다 (3장 §"3.3. The BlueZone example").[^cockburn2024]

## 이어지는 페이지

- [포트와 어댑터 규정](../concepts/ports-and-adapters-defined.md) — 이 코드 사례들이 보이는 규정의 원전
- [포트와 어댑터 적용 실무](ports-and-adapters-in-practice.md) — 같은 원전의 실무 문답(포트 수·앱
  경계·개발 순서)
- [의존성 주입과 부트스트랩](../concepts/dependency-injection-and-bootstrap.md) — 생성자 주입·세터
  주입·의존성 조회가 사는 자리
- [의존성 역전 원칙](../concepts/dependency-inversion-principle.md) — 이 패턴이 이 KB에서 사는
  자리이자 2차 서술의 정박점
- [헥사고날 아키텍처](../synthesis/hexagonal-architecture.md) — 이 축의 허브

[^cockburn2024]: Cockburn & Garrido de Paz 2024, 3장 도입 · §"3.1. The simplest example: the tax
    calculator"(하위 "The simplest tax calculator (Java)"·"(Ruby)"·"Using a setter instead of
    constructor argument (Java)"·"Using a broker instead of a fixed rate repository (Ruby)") ·
    §"3.2. Another simple example, the web-hexagon" · §"3.3. The BlueZone example"(그림 3.1
    포함) · 7장 §"7.2. The sample code to copy" · Fin. 자바 코드는 원문 그대로이며 조판 줄바꿈만 폈다(없는 줄을 보태지 않았다). 그림 3.1의
    액터·포트는 본문 목록이 그대로 열거하므로 이미지를 열지 않았다. EPUB(Calibre 변환본), 쪽
    앵커 없음 — locator는 장·절 번호.

---
type: concept
title: 소비자 주도 계약
description: 서비스 계약을 제공자 계약·소비자 계약·소비자 주도 계약 셋으로 가른 2006년의 패턴 서술 — 소비자가 자기가 쓰는 것만 단정으로 적고 그 단정 뭉치에서 제공자 계약이 파생된다는 배치, 그 단정이 빌드마다 도는 테스트로 표현된다는 대목, 그리고 저자 자신이 그어 둔 적용 범위. 실무자 에세이라 근거가 아니라 정의와 자기 규정이다
status: draft
generated: { by: "claude-opus-5", at: "2026-08-22T05:00:00Z" }
sources:
  - { id: robinson2006-cdc, resource: /it/sources/robinson2006-cdc.md }
---

# 소비자 주도 계약

- [이 페이지의 지위 — 근거가 아니라 정의다](#이-페이지의-지위--근거가-아니라-정의다)
- [전이 조건 — 2006년의 자리에서 지금의 자리로](#전이-조건--2006년의-자리에서-지금의-자리로)
- [문제 — 계약이 서비스를 묶는다](#문제--계약이-서비스를-묶는다)
- [소비자가 자기 기대를 자기 손으로 적는다](#소비자가-자기-기대를-자기-손으로-적는다)
- [계약 세 종류](#계약-세-종류)
  - [제공자 계약](#제공자-계약)
  - [소비자 계약](#소비자-계약)
  - [소비자 주도 계약](#소비자-주도-계약-1)
  - [저자가 낸 특성 표](#저자가-낸-특성-표)
- [구현 — 계약이 빌드마다 도는 테스트가 된다](#구현--계약이-빌드마다-도는-테스트가-된다)
- [이 KB의 읽기 — 정보 출처가 갈린다](#이-kb의-읽기--정보-출처가-갈린다)
- [저자가 스스로 그은 한계](#저자가-스스로-그은-한계)
- [계약에 의한 설계와 같은 낱말, 다른 것](#계약에-의한-설계와-같은-낱말-다른-것)
- [에이전트 사이의 계약으로 옮기는 것은 미검증 유추다](#에이전트-사이의-계약으로-옮기는-것은-미검증-유추다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **서비스 경계에서 "무엇이 옳은 응답인가"를 적어 둔 사양 산출물을 누가
쓰는가.** 곧 판정의 기준이 제공자 쪽에서 내려오는가, 소비자 쪽에서 올라오는가다.

## 이 페이지의 지위 — 근거가 아니라 정의다

- **소스는 실무자 에세이(practitioner essay)다.** 마틴 파울러 사이트에 실린 게스트
  글이고, 저자는 당시 Thoughtworks의 컨설턴트다 (저자 소개 줄).[^robinson2006-cdc]
  실험도 측정도 없고 **글 전체에 수치가 하나도 없다.** 그러므로 이 페이지는 소비자 주도
  계약(consumer-driven contract)이 **효과가 있다는 근거**를 대지 않는다 — 대는 것은 그 패턴의 **정의**와 그것을
  지은 사람의 **자기 규정**뿐이다.
- **글이 자기가 무엇을 하는 글인지 서두에 적는다** (초록):[^robinson2006-cdc]

  > the article then describes the “Consumer-Driven Contract” pattern, which imbues
  > providers with insight into their consumer obligations, and focuses service evolution
  > around the delivery of the key business functionality demanded by consumers.

  **패턴을 제안하는 글**이지 그 패턴을 잰 글이 아니라는 것이 이 한 문장에 있다.
- **개정이 없는 판이다.** 본문 말미 「Significant Revisions」가 한 줄뿐이고
  (**"12 June 2006: First published"**), 페이지가 심은 `og:article:modified_time`도 같은
  날이다 (절 `Significant Revisions`).[^robinson2006-cdc] 다만 글 자신이 더 나중 판의
  존재를 알린다 — Thoughtworks Anthology의 개정판과 후속 블로그 글이 있다고 적는다
  (초록 아래 알림 줄).[^robinson2006-cdc] **그 판들은 이 KB에 없다.**

## 전이 조건 — 2006년의 자리에서 지금의 자리로

이 글의 무대는 XML 스키마와 `WS-*` 스택으로 짜인 서비스 지향 아키텍처다. XSD·Schematron·
WS-Policy가 예시의 재료이고, 지금 실무에서 그 자리를 다른 것들이 쓴다. **그럼에도 옮겨
오는 것과 옮겨 오지 않는 것을 가른다.**

- **옮겨 오는 것 — 배치다.** "소비자가 자기가 실제로 쓰는 것만 적고, 제공자
  계약(provider contract)이 그 기대들의 합집합에서 파생된다"는 구조는 직렬화 형식에 매이지 않는다. 조직 경계를 넘어
  독립 배포되는 API가 있는 한 같은 힘이 걸린다.
- **옮겨 오지 않는 것 — 재료다.** Schematron·WS-Policy·XSD는 이 글의 예시일 뿐 패턴의
  일부가 아니다. 저자 자신이 그렇게 못 박는다 (절 `Implementation`):[^robinson2006-cdc]

  > The pattern does not however specify the form or structure consumer and consumer-driven
  > contracts should adopt, nor does it determine how consumer expectations are communicated
  > to the provider and asserted during the provider's lifetime.

- **후대 구현체는 이 글 밖이다.** 계약을 파일로 주고받는 오늘날의 도구들은 2006년 이
  글에 이름조차 나오지 않는다. 이 페이지는 그 도구들을 이 소스에 기대어 서술하지 않는다.

## 문제 — 계약이 서비스를 묶는다

- **역설이 출발점이다** — 계약은 서비스의 독립을 가능하게 하는 동시에 제공자와 소비자를
  바람직하지 않은 방식으로 묶는다. 글은 이것을 **숨은 결합(“hidden” coupling)**이라
  부르고, 그 결합을 체계적으로 다룰 장비가 우리에게 거의 없다고 적는다
  (절 `Interlude: Burdened With Services`).[^robinson2006-cdc]
- **묶이는 기제** — 소비자가 받은 문서를 XSD로 검증하면, 자기가 처리할 생각이 없는
  부분까지 포함해 **제공자 계약 전체를 암묵적으로 받아들이게 된다** (절 `Breaking
  Changes`).[^robinson2006-cdc] 그래서 제공자가 아무도 쓰지 않는 필드 하나를 빼려 해도
  소비자 전부가 함께 움직여야 한다 — 글의 표현으로 **"provider and consumers must all
  jump at the same time"**이다 (절 `Breaking Changes`).[^robinson2006-cdc]
- **완화책 둘을 먼저 검토하고 둘 다 부족하다고 적는다.** 스키마에 확장 지점(extension
  point)을 두어 전진·후진 호환을 확보하는 길과, 받는 쪽이 **"딱 필요한 만큼(“just
  enough”)"**만 검증하는 길이다. 앞의 것은 깨지는 변경을 다루지 못하고, 도메인 언어에
  메타 정보용 컨테이너 원소를 밀어 넣어 표현력을 흐린다고 적는다 (절 `Extension
  Points`).[^robinson2006-cdc]
- **"딱 필요한 만큼"의 규정** (절 `Breaking Changes`):[^robinson2006-cdc]

  > message receivers should implement “just enough” validation: that is, they should only
  > process data that contributes to the business functions they implement, and should only
  > perform explicitly bounded or targeted validation of the data they receive

  이 문단이 인용하는 인터넷 프로토콜 견고성 원칙(Robustness Principle)은 David Orchard를
  거쳐 온 **2차 경유**다 — 원문이 이 KB에 없으므로 이 글이 옮긴 문면까지만 쓴다.

## 소비자가 자기 기대를 자기 손으로 적는다

- **핵심 장면이 여기다.** 소비자 쪽 검증을 좁히는 방법으로 글은 구조적 트리 패턴 검증
  언어인 Schematron을 든다 — **소비자가 검색 결과에서 무엇을 찾을 것으로 기대하는지를
  프로그램으로 단정한다** (절 `Schematron`).[^robinson2006-cdc]

  소비자 쪽이 쓰는 검증 스키마의 실물이다. 제공자의 XSD가 아니라 **소비자가 자기 손으로
  적은 파일**이고, 여기 적힌 세 원소가 그 소비자가 실제로 쓰는 전부다.

  ```xml
  <?xml version="1.0" encoding="utf-8" ?>
  <schema xmlns="http://www.ascc.net/xml/schematron">

    <title>ProductSearch</title>
    <ns uri="urn:example.com:productsearch:products" prefix="p"/>

    <pattern name="Validate search results">
      <rule context="*//p:Product">
        <assert test="p:CatalogueID">Must contain CatalogueID node</assert>
        <assert test="p:Name">Must contain Name node</assert>
        <assert test="p:Price">Must contain Price node</assert>
      </rule>
    </pattern>

  </schema>
  ```

- **적지 않은 것이 이 파일의 요점이다** (절 `Schematron`):[^robinson2006-cdc]

  > Notice that this sample Schematron schema makes no assertions about elements in the
  > underlying document for which the consuming application has no appetite.

  그래서 **기저 문서 스키마가 바뀌어도, 여기 명시된 기대를 건드리지 않는 한 검증이
  그것을 집어내지 않는다** — 예전에 필수였던 원소를 폐기하거나 제거하는 변경이어도
  그렇다 (절 `Schematron`).[^robinson2006-cdc]
- **그 단정 뭉치를 제공자 쪽으로 들여오면 방향이 뒤집힌다** (절 `Consumer
  Contracts`):[^robinson2006-cdc]

  > The Schematron assertions in our example look very much like the kinds of tests that,
  > if implemented by the provider, might help ensure the provider continues to meet its
  > commitments to its clients.

  그리고 **모든 소비자가 만든 단정의 집합은 그 단정들이 유효한 기간 동안 교환될 메시지의
  필수 구조를 표현한다**고 적는다. 제공자가 그 집합을 가지고 있다면, 집합이 유효하고
  완전한 한에서 **자기가 보내는 모든 메시지가 모든 소비자에게 유효함을 보장할 수
  있다** (절 `Consumer Contracts`).[^robinson2006-cdc]

## 계약 세 종류

글이 이름 붙인 것은 세 가지다. **셋의 차이는 누가 썼는가와 무엇을 담는가에 있지 파일
형식에 있지 않다.**

### 제공자 계약

- **규정** (절 `Provider Contracts`):[^robinson2006-cdc]

  > A provider contract expresses a service provider's business function capabilities in
  > terms of the set of exportable elements necessary to support that functionality.

- 여기서 계약은 문서 스키마보다 넓다. 글이 비규범적 목록으로 드는 구성 원소는 다섯이다 —
  **문서 스키마(document schemas)·인터페이스(interfaces)·대화(conversations)·정책(policy)·
  서비스 품질 특성(quality of service characteristics)** (절 `Provider
  Contracts`).[^robinson2006-cdc] 가용성·지연·처리량 같은 것까지 계약의 후보로 든다는
  점이 이 정의의 특징이다.
- **무엇을 계약에 넣을지의 판정 기준**을 글이 준다 — 우리 소비자 중 누군가가 **그 원소가
  감싼 업무 기능 역량이 서비스의 수명 내내 계속 충족되기를 합리적으로 기대할 수 있는가**를
  묻는다 (절 `Provider Contracts`).[^robinson2006-cdc]

### 소비자 계약

- **규정** (절 `Consumer Contracts`):[^robinson2006-cdc]

  > When a provider accepts and adopts the reasonable expectations expressed by a consumer,
  > it enters into a consumer contract.

- **소비자 계약(consumer contract)은 시스템이 가진 업무 기능에 대해 열려 있고
  불완전하다** — 소비자가 제공자 계약에 거는 기대라는 형태로 시스템 역량의
  **부분집합**만 표현한다 (절 `Consumer Contracts`).[^robinson2006-cdc]
- **비권위적(non-authoritative)이라는 성질이 분산 애플리케이션과 서비스 지향을 가른다**고
  적는다. 소비자는 자기 동료 소비자가 자기와 아주 다르게 제공자를 쓸 수 있음을 인정해야
  하고, 동료가 언제 어떻게 제공자 계약을 흔들지 예상할 수 없다 — 분산 애플리케이션의
  클라이언트에는 그런 걱정이 없다 (절 `Consumer Contracts`).[^robinson2006-cdc]

### 소비자 주도 계약

- **규정** (절 `Consumer-Driven Contracts`, 하위 절):[^robinson2006-cdc]

  > This leads us to suggest that service communities might benefit from being specified in
  > the first instance in terms of consumer contracts. In this view, provider contracts
  > emerge to meet consumer expectations and demands. To reflect the derived nature of this
  > new contractual arrangement, we call such provider contracts consumer-driven contracts
  > or derived contracts.

- **이 계약은 기존 소비자들이 요구하는 기능 전체에 대해 닫혀 있고 완전하다** — 그 기대들이
  각자의 부모 애플리케이션에서 유효한 기간 동안 필요한 내보내기 원소의 **필수 집합**을
  표현한다 (절 `Consumer-Driven Contracts`, 하위 절).[^robinson2006-cdc]
- **파생이라는 성질이 관계에 타율성(heteronomous aspect)을 더한다** — 제공자가 **자기
  경계 바깥에서 오는 의무**를 지게 된다는 뜻이다. 글은 이것이 구현의 자율성을 해치지
  않으며, 서비스가 소비되어야 성공한다는 사실을 명시화할 뿐이라고 덧붙인다 (절
  `Consumer-Driven Contracts`, 하위 절).[^robinson2006-cdc]

### 저자가 낸 특성 표

글이 세 계약을 다섯 축으로 정리해 표로 낸다 (절 `Summary of Contract
Characteristics`).[^robinson2006-cdc] 축 이름과 값은 원문 그대로다.

| Contract | Open | Complete | Number | Authority | Bounded |
|---|---|---|---|---|---|
| Provider | Closed | Complete | Single | Authoritative | Space/time |
| Consumer | Open | Incomplete | Multiple | Non-authoritative | Space/time |
| Consumer-Driven | Closed | Complete | Single | Non-authoritative | Consumers |

**마지막 열이 이 표의 요점이다.** 제공자 계약과 소비자 주도 계약은 앞 네 축이 똑같고
오직 `Authority` 열과 `Bounded` 열에서 갈린다 — 뒤쪽은 **소비자 계약의 집합에
대해서만** 안정하고 불변이다. 기대가 생기고 사라지면 그 경계도 바뀐다.

## 구현 — 계약이 빌드마다 도는 테스트가 된다

- 글은 계약을 표현하는 방법을 **가장 단순한 것부터 정교한 것까지** 늘어놓는다 (절
  `Implementation`).[^robinson2006-cdc] 가장 단순한 쪽은 소비자 기대를 **스프레드시트나
  비슷한 문서**에 담아 제공자 애플리케이션의 설계·개발·테스트 단계에서 구현하는 것이고,
  가장 정교한 쪽은 기대를 Schematron이나 WS-Policy 같은 단정으로 표현해 서비스 엔드포인트의
  입출력 파이프라인에서 **런타임에 평가**하는 것이다.
- **그 사이에 테스트가 있다** (절 `Implementation`):[^robinson2006-cdc]

  > By going a little further and introducing unit tests that assert each expectation, we
  > can ensure that contracts are described and enforced in a repeatable, automated fashion
  > with each build.

  계약이 산문이 아니라 **빌드마다 자동으로 도는 검사**가 되는 자리이고, 이 페이지가 검증
  축에 서는 이유가 이 한 문장이다.
- **기대를 전달하는 경로도 열려 있다.** 조직 여건이 맞으면 다른 팀에게 말하거나 메일을
  쓰는 것으로 충분하고, 기대나 소비자 수가 그렇게 관리하기 어려울 만큼 늘면 계약 서비스
  인터페이스를 인프라에 들이는 것을 고려한다고 적는다. 어느 방식이든 그 소통은 업무 기능을
  실제로 주고받는 대화 **이전에, 대역 밖에서(out-of-band)** 이뤄질 것이라고 본다 (절
  `Implementation`).[^robinson2006-cdc]

## 이 KB의 읽기 — 정보 출처가 갈린다

**아래는 이 소스의 주장이 아니라 이 KB의 판정이다.** 글은 "검증자 독립성"이라는 낱말을
쓰지 않고, 자기 패턴을 서비스 진화(service evolution)의 문제로만 놓는다.

- **소비자 주도 계약에서 사양 산출물의 저자와 구현자가 갈린다.** 위 Schematron 파일을
  쓴 것은 소비자이고, 그 파일이 판정하는 대상은 제공자의 구현이다. 소비자는 제공자가
  내부를 어떻게 짰는지 보지 않고 자기가 필요한 것만 적었다. 그래서 이 계약 파일은
  **판정 대상의 구현에서 파생되지 않은 사양**이다 — 판정 근거가 판정 대상 안에서
  나오지 않는다는 뜻이고, 이것이 이 페이지를 검증 축에 세우는 성질이다.
- **이것은 판정 *주체*의 분리가 아니라 판정 *근거*의 출처 분리다.** 두 축이 자주 겹쳐
  읽히므로 갈라 둔다. 주체 쪽 물음은 "누가 채점하는가"이고
  ([에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md)가
  그 자리다), 이 페이지의 물음은 "채점표를 누가 썼는가"다. **두 축은 서로를 함의하지
  않는다** — 제공자가 자기 소비자 계약 테스트를 자기 CI에서 돌리면 주체는 갈리지 않은
  채 근거만 갈린 배치이고, 그것이 이 글이 실제로 처방하는 배치다.
- **오라클 분류에서 어디에 앉는가.** 계약은 명세이므로 이 산출물이 만드는 것은 명세
  오라클 쪽이다 — [테스트 오라클](../concepts/test-oracle.md)이 정리한 네 출처 가운데
  단정과 계약 부류다. 그쪽 페이지가 이미 적어 둔 계보와 겹치는 자리가 있다: 튜링이
  테스터를 개발자로부터 분리하고 둘이 단정을 매개로 소통하자고 한 제안이 그것이다.
  **소비자 주도 계약은 그 매개를 조직 경계 너머로 옮긴 배치**라는 것이 이 KB의 읽기다.
- **#hypothesis 계약이 소비자 손에서 나온다는 사실만으로 판정이 독립이 되지는 않는다.**
  소비자들이 같은 팀이거나 같은 생성기에서 나온 클라이언트를 쓰면 그 기대들도 같이
  틀릴 수 있다. 이 글은 그 위험을 다루지 않는다 — 그 물음은
  [독립 개발 판본의 실패 상관](../concepts/correlated-failure-of-independent-versions.md)가
  소유한다.

## 저자가 스스로 그은 한계

**「Liabilities」 절이 이 글에서 가장 중요한 절이다.** 실무자 에세이를 인용할 때 지위를
밝히는 자리가 여기다.

- **적용 범위가 좁다** (절 `Liabilities`):[^robinson2006-cdc]

  > The Consumer-Driven Contract pattern is applicable in the context of either a single
  > enterprise or a closed community of well-know services

  (`well-know`는 원문의 오식이다 — 그대로 옮긴다.) 곧 **제공자가 소비자의 계약 방식에
  어느 정도 영향력을 행사할 수 있는 환경**이 전제다. 공개 API처럼 소비자가 누구인지도
  모르는 자리는 이 패턴의 무대가 아니다. 글은 그 대가로 이미 복잡한 인프라에 **또 한
  겹의 복잡성과 프로토콜 의존**이 더해진다고 적는다.
- **결합도를 줄이지 않는다** (절 `Liabilities`):[^robinson2006-cdc]

  > Consumer-driven contracts do not necessarily reduce the coupling between services.

  하는 일은 **숨어 있던 결합을 파내어 눈에 보이게 놓는 것**이고, 그래야 제공자와 소비자가
  그것을 협상하고 관리할 수 있다고 적는다.
- **깨지는 변경의 해결책이 아니다.** 글의 표현으로 **"a breaking change is still a
  breaking change"**다. 다만 무엇이 실제로 깨지는 변경인지에 대한 통찰을 주므로 버저닝
  전략의 토대가 될 수 있다고 적는다 (절 `Liabilities`).[^robinson2006-cdc]
- **업무 가치의 지표가 아니다** — 계약을 SLA나 업무 지표로 읽지 말라고 명시한다
  (절 `Liabilities`).[^robinson2006-cdc]
- **개념적 무결성을 해칠 위험을 마지막에 적는다** — 소비자 계약이 제공자 명세를 끌고 가게
  두면 그 제공자의 개념적 무결성(conceptual integrity)이 훼손될 수 있다. 서비스가 감싼
  업무 기능의 온전함이 **자기 소관 밖의 무리한 요구**에 깎여서는 안 된다고 적는다
  (절 `Liabilities`).[^robinson2006-cdc]

## 계약에 의한 설계와 같은 낱말, 다른 것

**"계약"이 같은 낱말이지만 가리키는 것이 다르다.** 혼동을 막기 위해 갈라 둔다.

- [계약에 의한 설계](../concepts/design-by-contract.md)의 계약은 **한 프로그램 안의 두
  모듈 사이**에서 호출자와 피호출자의 권리·의무를 선행 조건·후행 조건·불변식으로 적은
  것이다. 그 계약을 어기는 것은 버그이고, 쓰는 쪽은 대개 모듈의 저자다.
- 이 페이지의 계약은 **조직 경계를 넘는 서비스 사이**에서 교환되는 메시지와 그 밖의
  내보내기 원소에 걸리며, 쓰는 쪽이 제공자냐 소비자냐가 바로 세 종류를 가르는 기준이다.
- **겹치는 것은 어휘 하나다** — 둘 다 기대를 단정으로 적고, 그 단정이 기대값의 출처가
  된다. 겹치지 않는 것은 경계와 저자다. 소비자 주도 계약의 새로움은 사전·사후 조건이
  아니라 **계약의 방향**에 있다.

## 에이전트 사이의 계약으로 옮기는 것은 미검증 유추다

- **이 소스는 LLM 이전 문헌이고 그 시대에 대해 재검된 적이 없다.** 2006년 글이며, 이
  KB가 확인한 판본은 발행 이후 개정되지 않았다.
- **#hypothesis 소비자 주도 계약을 에이전트 사이의 계약** — 도구 스키마나 에이전트 간
  프로토콜의 사양 파일 따위 — **으로 옮기는 유추는 이 KB에서 미검증이다.** 겉모습은
  닮았다: 도구를 부르는 쪽이 자기가 쓰는 필드만 적고, 도구를 내는 쪽이 그 기대에 맞춰
  진화한다는 그림이 그렇다. 그러나 **이 소스는 그 유추의 근거가 아니고**, 이 KB는 그
  유추를 지지하는 실증을 아직 갖고 있지 않다. **반입은 원 개념에 한정한다.**
- 유추가 특히 위험한 지점 하나를 적어 둔다. 이 패턴의 전제는 **제공자가 소비자에게
  영향력을 행사할 수 있는 닫힌 공동체**인데(위 「저자가 스스로 그은 한계」), 모델이
  생성한 호출자는 그 전제를 만족하는지 자체가 물음이다.

## 이어지는 페이지

- [테스트 오라클](../concepts/test-oracle.md) — 계약이 기대값의 출처가 되는 자리. 그쪽이
  단정과 계약을 명세 오라클의 한 부류로 묶고, 형식 명세가 있어도 실행 결과와의 대조가
  저절로 서지는 않는다는 세 난점을 함께 적는다
- [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md) —
  **다른 축이다.** 그쪽은 판정 *주체*를 갈라 두라는 요구이고, 이 페이지는 판정 *근거*를
  누가 썼는가다. 둘은 서로를 함의하지 않는다
- [독립 개발 판본의 실패 상관](../concepts/correlated-failure-of-independent-versions.md) —
  기대를 여럿이 따로 적었다고 그 기대들이 독립적으로 틀리지는 않는다는 쪽의 원전
- [계약에 의한 설계](../concepts/design-by-contract.md) — 같은 낱말의 다른 경계.
  위 [계약에 의한 설계와 같은 낱말, 다른 것](#계약에-의한-설계와-같은-낱말-다른-것) 참조
- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 이 글의
  전반부가 기대는 두 방향의 정의. 확장 지점과 "딱 필요한 만큼"의 검증은 둘 다 전진
  호환을 확보하려는 장치다
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 같은 문제를 API 버저닝
  쪽에서 다루는 자리. 제공자가 클라이언트를 통제할 수 없어 호환을 무기한 유지하게 된다는
  서술이 이 글의 문제 설정과 맞물린다
- [단정적 프로그래밍](../concepts/assertive-programming.md) — 기대를 단정으로 적는 같은
  장치를 한 프로그램 안에서 쓰는 쪽
- [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md) — 같은 물음이
  데이터 경계에서 되풀이되는 자리. 그쪽에서 기대를 적은 스키마는 **데이터를 쓰는 쪽**인
  파이프라인 소유자가 큐레이션하고, 데이터를 만드는 팀은 대개 다른 팀이라 계약의 방향이
  소비자 쪽에서 올라온다. 다만 그 사양은 협상된 계약이 아니라 관측에서 추론된 것이다
- [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md) — 같은
  방향이 **데이터 파이프라인에서 실물로 관측된 자리.** 거기 인용된 논문의 교훈 절이
  생산자와 소비자가 같은 검증 시스템을 쓸 때의 이득으로 `the producer can choose to adapt
  checks from downstream consumers earlier in the data processing pipeline`을 든다 —
  **하류 소비자의 검사가 상류 생산자의 파이프라인으로 올라간다.** 다만 그것은 측정이 아니라
  사용자 피드백의 서술이다
- [인코딩과 진화](../synthesis/encoding-and-evolution.md) — 이 축의 허브
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 판정 근거 쪽의 허브
- [검증자 독립성](../synthesis/verifier-independence.md) — 판정 주체 쪽의 허브이자 이
  갈래의 허브

[^robinson2006-cdc]: Robinson 2006, "Consumer-Driven Contracts: A Service Evolution
    Pattern", `martinfowler.com/articles/consumerDrivenContracts.html`, 2006년 6월 12일
    발행. **마틴 파울러 사이트의 게스트 글이고 실무자 에세이지 학술 근거가 아니다** —
    실험도 측정도 없고 인용할 수 있는 수치가 없다. 웹 문서라 쪽수가 없어 locator는 **절
    제목**을 쓴다. 제목이 같은 절이 둘 있어(글 전체를 여는 `Consumer-Driven Contracts`와
    그 안의 하위 절) 뒤쪽은 "하위 절"이라 적어 갈랐다. 이 페이지는 초록·`Interlude:
    Burdened With Services`·`Extension Points`·`Breaking Changes`·`Schematron`·
    `Consumer-Driven Contracts`(및 하위 세 절)·`Summary of Contract Characteristics`·
    `Implementation`·`Liabilities`를 담았다. 담지 않은 것은 `Evolving a Service: An
    Example`과 `Schema Versioning`의 XSD 예제 전개로, 이 페이지의 물음이 아니라 뺐다.
    코드 펜스는 `Schematron` 절의 스키마 하나이고 원문에서 한 글자도 고치지 않았다.
    이 글이 옮겨 적는 남의 문장(David Orchard가 든 견고성 원칙, W3C TAG의 버저닝 전략
    분류, Pat Helland·Dare Obasanjo)은 전부 **2차 경유**라 이름과 이 글이 옮긴 문면까지만
    적었다. 판본·열람일과 인용 금지 사항은
    [소스 메타](../sources/robinson2006-cdc.md)에 있다.

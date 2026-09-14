---
type: concept
title: 이벤트 주도 통합 설계
description: 경계 컨텍스트 사이를 이벤트로 통합할 때 어떤 종류의 이벤트를 골라야 하고 무엇이 그 설계를 망치는가 — 이벤트 주도 아키텍처의 규정과 그것이 이벤트 소싱과 갈리는 자리(서비스 사이 대 서비스 안), 이벤트와 명령이 메시지의 두 종류라는 분류와 취소할 수 있는 쪽과 없는 쪽의 비대칭, 이벤트 알림과 이벤트가 실어 나르는 상태 전이와 도메인 이벤트라는 세 종류의 규정과 서로 갈리는 지점, 도메인 이벤트를 그대로 내놓아 생기는 시간 결합·기능 결합·구현 결합이라는 분산된 큰 진흙 공의 해부와 소비자 주도 계약으로 그것을 되돌리는 리팩터링, 그리고 최악을 가정하라·공개 이벤트와 사적 이벤트를 가르라·일관성 요구로 종류를 고르라는 설계 휴리스틱 셋
generated: { by: "claude-opus-5", at: "2026-09-15T13:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 이벤트 주도 통합 설계

- [무엇이 이벤트 주도 아키텍처인가](#무엇이-이벤트-주도-아키텍처인가)
- [이벤트 소싱과 갈리는 자리](#이벤트-소싱과-갈리는-자리)
- [이벤트와 명령 — 메시지의 두 종류](#이벤트와-명령--메시지의-두-종류)
- [이벤트의 구조](#이벤트의-구조)
- [세 종류 — 알림과 상태 전이와 도메인 이벤트](#세-종류--알림과-상태-전이와-도메인-이벤트)
- [세 종류가 갈리는 지점](#세-종류가-갈리는-지점)
- [같은 사건을 세 종류로 적어 보기](#같은-사건을-세-종류로-적어-보기)
- [이벤트를 쏟아부어 만든 분산된 큰 진흙 공](#이벤트를-쏟아부어-만든-분산된-큰-진흙-공)
- [그 설계를 되돌리는 리팩터링](#그-설계를-되돌리는-리팩터링)
- [설계 휴리스틱 셋](#설계-휴리스틱-셋)
- [이 KB의 다른 자리들과의 분업](#이-kb의-다른-자리들과의-분업)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **경계 컨텍스트 사이를 이벤트로 통합할 때 어떤 종류의 이벤트를 골라야 하고,
잘못 고르면 무엇이 망가지는가.**

## 무엇이 이벤트 주도 아키텍처인가

- 규정이 한 문장이다 (15장 §"Event-Driven Architecture", p.233):[^khononov2021]

> Stated simply, event-driven architecture is an architectural style in which a system's components
> communicate with one another asynchronously by exchanging event messages

  - 서비스의 엔드포인트를 동기로 호출하는 대신, 구성 요소가 **체계 도메인의 변화**를 알리려고
    이벤트를 발행하고 다른 구성 요소가 그것을 구독해 반응한다 (15장, p.233).[^khononov2021]
  - 이 실행 흐름의 전형적 예로 저자가 드는 것이 9장의 사가다 (15장, p.233).[^khononov2021]
    그 패턴은 [사가 패턴](saga-pattern.md)에 있다.
- **이벤트가 만능 재료가 아니라는 경고가 장의 도입에 먼저 온다** — 이벤트는 레거시 위에
  들이부으면 느슨하게 결합된 분산 체계가 되는 비밀 소스가 아니고, 오히려 **부주의하게 적용하면
  모듈러 모놀리스를 분산된 큰 진흙 공으로 바꿔 놓을 수 있다** (15장 도입, p.233).
  [^khononov2021]

## 이벤트 소싱과 갈리는 자리

- **두 패턴이 개념적으로 다르다** (15장, p.233):[^khononov2021]

> EDA refers to the communication between services, while event sourcing happens inside a service.

  - 이벤트 소싱용으로 설계된 이벤트는 그 서비스 안에 구현된 **상태 전이**를 표현한다(이벤트 소싱
    도메인 모델에서는 애그리게이트의 상태 전이다). 그 이벤트들의 목적은 업무 도메인의 세부를
    붙잡는 것이지 **다른 구성 요소와 통합하는 것이 아니다** (15장, p.233).[^khononov2021]
  - 그래서 세 종류의 이벤트 중 **통합에 더 맞는 것과 덜 맞는 것이 갈린다** (15장, p.233).
    [^khononov2021] 아래 [세 종류](#세-종류--알림과-상태-전이와-도메인-이벤트)가 그 구분이다.
- 이벤트 소싱 자체는 [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)와
  [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)에 있다.

## 이벤트와 명령 — 메시지의 두 종류

- **포함 관계가 한 방향이다** — 이벤트는 메시지이지만 메시지가 반드시 이벤트인 것은 아니고,
  메시지에는 두 종류가 있다 (15장 §"Events, Commands, and Messages", p.234).[^khononov2021]
  저자는 이 자리에서 메시지 패턴의 출처로 [hohpe2004](../sources/hohpe2004.md)를 든다.
- 규정이 짝으로 온다 (15장 §"Events, Commands, and Messages", pp.234–235):[^khononov2021]

> Event
> A message describing a change that has already happened
>
> Command
> A message describing an operation that has to be carried out

- **비대칭이 여기서 나온다** (15장, p.235):[^khononov2021]
  - 둘 다 비동기로 메시지로 전달될 수 있다.
  - **명령은 거절될 수 있다** — 받는 쪽이 유효하지 않거나 업무 규칙에 어긋난다고 판단하면
    실행을 거부할 수 있다.
  - **이벤트는 받는 쪽이 취소할 수 없다.** 이미 일어난 일을 서술하기 때문이다. 이벤트를
    뒤집는 유일한 길은 **보상 동작을 내는 것**이고, 보상 동작은 명령이다 — 사가가 하는 일이
    그것이다.
- 이름 규칙도 여기서 반복된다 — 이미 일어난 일을 서술하므로 이벤트 이름은 과거 시제로 짓는다
  (`DeliveryScheduled`·`ShipmentCompleted`·`DeliveryConfirmed`) (15장, p.235).[^khononov2021]
  같은 조항이 [도메인 이벤트](../concepts/domain-events.md)에 있다.

## 이벤트의 구조

- 이벤트는 **선택한 메시징 플랫폼으로 직렬화해 전송할 수 있는 데이터 레코드**이고, 전형적인
  스키마는 메타데이터와 페이로드(payload)로 이뤄진다. 페이로드가 그 이벤트가 전달하는 정보다
  (15장 §Structure, p.235).[^khononov2021]
- **메타데이터에 무엇이 드는지는 예시로만 제시된다** — 이벤트 종류(`type`), 이벤트 식별자
  (`event-id`), 상관 식별자(`correlation-id`), 대상 식별자, 시각(`timestamp`)이 원문 예시의
  바깥 필드다 (15장 §Structure, p.235).[^khononov2021]
- **페이로드가 이벤트의 종류까지 정한다** — 페이로드는 이벤트가 나르는 정보를 서술할 뿐 아니라
  그 이벤트가 셋 중 어느 종류인지를 규정한다 (15장 §Structure, p.235).[^khononov2021]

## 세 종류 — 알림과 상태 전이와 도메인 이벤트

저자는 이벤트를 셋 중 하나로 분류한다 — **이벤트 알림(event notification), 이벤트가 실어 나르는
상태 전이(event-carried state transfer, ECST), 도메인 이벤트(domain event)** (15장 §"Types of
Events", p.236).[^khononov2021] 저자가 이 분류의 출처로 드는 것은 마틴 파울러의 글이고 이 KB가
확인한 원전이 아니다.

- **이벤트 알림** — 다른 구성 요소가 반응할 업무 도메인의 변화를 알리는 메시지다
  (`PaycheckGenerated`·`CampaignPublished` 같은 것). **장황하면 안 된다** — 목적은 관심 있는
  쪽에 알리는 것이지, 그들이 반응하는 데 필요한 정보를 다 실어 보내는 것이 아니다. 받는 쪽은
  메시지에 담긴 링크를 따라가 상세 정보를 가져온다 (15장 §"Event notification", p.236).
  [^khononov2021]
  - 저자가 드는 비유는 미국의 무선 긴급 경보(WEA)와 유럽의 EU-Alert다 — 기지국으로 최대 360자
    짧은 메시지를 뿌려 긴급 상황을 알리고, 상세는 받는 사람이 다른 정보원을 능동적으로 찾아야
    한다 (15장, p.237).[^khononov2021]
  - **짧은 알림이 유리한 경우가 둘 명시된다** (15장, p.237):[^khononov2021]
    - **보안** — 받는 쪽이 상세 정보를 명시적으로 질의하게 강제하면 민감 정보가 메시징 기반
      시설 위로 흐르지 않고, 구독자에게 그 데이터에 대한 별도 인가를 요구하게 된다.
    - **동시성** — 비동기라 정보가 구독자에게 닿을 때 이미 낡아 있을 수 있다. 경쟁 조건에
      민감한 정보라면 명시적으로 질의해 최신 상태를 얻는 편이 낫다. 나아가 **경쟁 소비자**
      상황에서 한 구독자만 처리해야 한다면 그 질의 과정에 비관적 잠금을 엮어 다른 소비자가
      같은 메시지를 처리하지 못하게 할 수 있다.
- **이벤트가 실어 나르는 상태 전이(ECST)** — 생산자의 내부 상태 변화를 구독자에게 알리되,
  알림과 달리 **그 변화를 반영하는 데이터를 전부 담는다** (15장 §"Event-carried state
  transfer", p.237).[^khononov2021]
  - 형태가 둘이다 — 바뀐 엔티티 상태의 **완전한 스냅샷**이거나, 큰 데이터 구조를 다룰 때
    **실제로 바뀐 필드만** 담는 것이다 (15장, p.238).[^khononov2021]
  - **어느 쪽이든 그 이벤트의 흐름이 소비자에게 로컬 캐시를 갖게 해 준다.** 개념적으로 ECST는
    **비동기 데이터 복제 기제**이고, 그래서 생산자가 살아 있지 않아도 소비자가 계속 기능할 수
    있어 체계가 더 결함 감내적이 되며, 여러 원천의 데이터를 처리해야 하는 구성 요소의 성능도
    좋아진다 — 필요할 때마다 질의하는 대신 전부 로컬에 캐시해 둔다 (15장, p.238).
    [^khononov2021]
- **도메인 이벤트** — 6장이 규정한 그 구성 단위다. 저자는 이것을 **알림과 ECST 사이 어딘가**에
  놓는다 — 업무 도메인의 중요한 사건을 서술한다는 점과 그 사건을 서술하는 데이터를 전부 담는다는
  점을 둘과 나눠 갖는다 (15장 §"Domain event", p.239).[^khononov2021] 규정 자체는
  [도메인 이벤트](../concepts/domain-events.md)에 있다.

## 세 종류가 갈리는 지점

| 갈리는 축 | 이벤트 알림 | ECST | 도메인 이벤트 |
|---|---|---|---|
| 담는 데이터 | 최소 — 링크를 따라가 더 가져와야 한다 | 상태를 반영하는 데이터 전부 | 사건을 서술하는 데이터 전부 |
| 모델링 의도 | 다른 구성 요소와의 통합을 쉽게 하려고 | 생산자 데이터를 복제하게 하려고 | 업무 도메인을 모델링하고 서술하려고 |
| 소비자가 없어도 쓸모가 있는가 | 아니다 | 아니다 | 그렇다 |

- **도메인 이벤트와 알림이 갈리는 지점이 둘이다** (15장 §"Domain events versus event
  notification", p.239):[^khononov2021]
  - 도메인 이벤트는 사건을 서술하는 정보를 전부 담으므로 **소비자가 전체 그림을 얻으려고 추가
    행동을 할 필요가 없다.**
  - **모델링 의도가 다르다.** 알림은 통합을 수월하게 하려는 의도로 설계되고, 도메인 이벤트는
    업무 도메인을 모델링하고 서술하려는 의도로 설계된다. 그래서 **외부 소비자가 하나도 없어도
    도메인 이벤트는 쓸모가 있다** — 모든 상태 전이를 도메인 이벤트로 모델링하는 이벤트 소싱
    체계에서 특히 그렇다. 그리고 **그 모든 도메인 이벤트에 외부 소비자가 관심을 갖는 상황은
    최적이 아닌 설계**다.
- **도메인 이벤트와 ECST가 갈리는 지점도 둘이다** (15장 §"Domain events versus event-carried
  state transfer", p.240):[^khononov2021]
  - ECST 메시지는 생산자 데이터의 로컬 캐시를 유지하기에 충분한 정보를 준다. **어떤 단일 도메인
    이벤트도 그렇게 풍부한 모델을 드러내도록 되어 있지 않다** — 특정 도메인 이벤트에 담긴
    데이터로는 애그리게이트의 상태를 캐시할 수 없다. 소비자가 구독하지 않은 다른 도메인 이벤트가
    같은 필드를 건드릴 수 있기 때문이다.
  - 여기서도 **모델링 의도가 다르다.** 도메인 이벤트에 담긴 데이터는 애그리게이트의 상태를
    서술하려는 것이 아니라 그 생애 주기 동안 일어난 **업무상의 사건**을 서술하려는 것이다.

## 같은 사건을 세 종류로 적어 보기

- 저자는 결혼이라는 하나의 사건을 세 가지로 표현해 차이를 보인다 (15장 §"Event types:
  Example", p.240):[^khononov2021]

  ```js
  eventNotification = {
      "type": "marriage-recorded",
      "person-id": "01b9a761",
      "payload": {
          "person-id": "126a7b61",
          "details": "/01b9a761/marriage-data"
      }
  };

  ecst = {
      "type": "personal-details-changed",
      "person-id": "01b9a761",
      "payload": {
           "new-last-name": "Williams"
      }
  };

  domainEvent = {
      "type": "married",
      "person-id": "01b9a761",
      "payload": {
          "person-id": "126a7b61",
          "assumed-partner-last-name": true
      }
  };
  ```

- `marriage-recorded`는 **이벤트 알림**이다. 지정된 식별자의 사람이 결혼했다는 사실 말고는
  아무 정보도 담지 않고, 더 알고 싶은 소비자는 `details` 필드의 링크를 따라가야 한다 (15장,
  p.241).[^khononov2021]
- `personal-details-changed`는 **ECST**다. 그 사람의 인적 사항 변화, 곧 성이 바뀌었다는 것을
  서술한다. **왜 바뀌었는지는 설명하지 않는다** — 결혼했는지 이혼했는지 알 수 없다 (15장,
  p.241).[^khononov2021]
- `married`는 **도메인 이벤트**다. 업무 도메인에서 그 사건이 갖는 성질에 최대한 가깝게
  모델링되어, 상대의 식별자와 그 사람이 상대의 성을 따랐는지를 나타내는 플래그를 담는다 (15장,
  p.241).[^khononov2021]

## 이벤트를 쏟아부어 만든 분산된 큰 진흙 공

**저자는 좋은 설계를 보이기 전에 나쁜 설계를 해부한다.** 그리고 그 예가 지어낸 것이 아니라
실화에 기반한 것이라고 적는다 (15장 §"Refactoring the Event-Driven Integration", p.243).
[^khononov2021]

- 사례의 얼개 (15장 §"Distributed Big Ball of Mud", p.241):[^khononov2021]
  - CRM 경계 컨텍스트가 이벤트 소싱 도메인 모델로 구현되어 있다. Marketing 경계 컨텍스트와
    통합할 때 팀들은 그 유연성을 지렛대 삼아 **소비자가 CRM의 도메인 이벤트를 구독해 자기에게
    맞는 모델을 투영하게** 했다.
  - AdsOptimization 경계 컨텍스트가 생겼을 때도 같은 결정을 반복했다.
  - 그런데 Marketing과 AdsOptimization은 고객 정보를 **같은 형식**으로 보여야 했고, 결국 같은
    모델(고객 상태의 평탄화된 스냅샷)을 각자 투영하게 됐다.
  - Reporting 경계 컨텍스트는 CRM 이벤트의 일부만 구독해 알림처럼 쓰면서 AdsOptimization의
    계산 결과를 가져갔다. 두 컨텍스트가 같은 이벤트로 촉발되므로 순서를 맞추려고
    **AdsOptimization이 5분 지연을 넣었다.**
- **저자는 이 설계를 결합의 종류 셋으로 해부한다.**

| 결합의 종류 | 어디서 생겼는가 | 무엇이 문제인가 |
|---|---|---|
| 시간 결합(temporal coupling) | Reporting이 AdsOptimization의 처리 완료에 의존한다 | 순서를 지연으로 강제하는 것은 보장이 아니다 |
| 기능 결합(functional coupling) | 두 컨텍스트가 같은 투영 로직을 각자 구현했다 | 바뀔 이유가 같아서 한쪽을 고치면 다른 쪽도 고쳐야 한다 |
| 구현 결합(implementation coupling) | 두 컨텍스트가 CRM의 모든 도메인 이벤트를 구독한다 | 생산자의 구현이 바뀌면 구독자가 깨지거나 조용히 어긋난다 |

  - **시간 결합** — 엄격한 실행 순서에 의존한다는 뜻이고, 순서가 뒤집히면 Reporting에 일관되지
    않은 데이터가 생긴다. 5분 지연은 그 순서를 막아 주지 못한다 — AdsOptimization이 과부하로
    5분 안에 끝내지 못할 수도, 네트워크 문제로 메시지 도착이 늦을 수도, 아예 장애로 처리를
    멈출 수도 있다 (15장 §"Temporal Coupling", pp.242–243).[^khononov2021]
  - **기능 결합** — 들어오는 도메인 이벤트를 상태 기반 표현으로 바꾸는 업무 로직이 두 경계
    컨텍스트에 중복됐고 **바뀔 이유가 같다**. 여러 구성 요소가 같은 업무 기능을 구현하고 그것이
    바뀌면 둘 다 동시에 바뀌어야 하는 것이 이 결합이다 (15장 §"Functional Coupling", p.243).
    [^khononov2021]
  - **구현 결합** — 더 미묘하다. 구독자들이 CRM의 이벤트 소싱 모델이 내는 **모든** 도메인
    이벤트를 구독하므로, CRM 구현의 변경(도메인 이벤트 추가·기존 이벤트의 스키마 변경)이 두
    구독자에 반영되어야 한다. 반영하지 않으면 스키마 변경 때는 투영 로직이 실패하고, 이벤트
    추가 때는 **일관되지 않은 상태를 투영하게 된다** (15장 §"Implementation Coupling", p.243).
    [^khononov2021]

## 그 설계를 되돌리는 리팩터링

- **구현 결합은 드러내는 이벤트를 바꿔서 푼다** — 훨씬 절제된 이벤트 집합을 드러내거나, 다른
  종류의 이벤트를 드러낸다 (15장, p.244).[^khononov2021]
- **구현 결합과 기능 결합을 한꺼번에 푸는 길은 투영 로직을 생산자 안에 감싸는 것**이다. CRM이
  구현 세부를 드러내는 대신 **소비자 주도 계약(consumer-driven contract)** 패턴을 따라 소비자가
  필요로 하는 모델을 스스로 투영하고, 그것을 자기 경계 컨텍스트의 공표된 언어의 일부로 만든다 —
  내부 구현 모델과 분리된 **통합 전용 모델**이다. 그러면 소비자는 필요한 데이터를 전부 얻으면서
  CRM의 구현 모델을 알지 못한다 (15장, p.244).[^khononov2021]
- **시간 결합은 이벤트 알림으로 푼다** — AdsOptimization이 이벤트 알림을 발행하고, 그것이
  Reporting이 필요한 데이터를 가져오도록 촉발한다 (15장, p.244).[^khononov2021]
- **이 리팩터링이 곧 아래 휴리스틱의 근거다** — 저자는 "적용한 변경 뒤에 있는 설계 휴리스틱을
  정식화해 보자"고 적으며 다음 절로 넘어간다 (15장 §"Event-Driven Design Heuristics", p.245).
  [^khononov2021]

## 설계 휴리스틱 셋

### 최악을 가정하라

- 지도 원리로 삼을 것 (15장 §"Assume the worst", p.245):[^khononov2021]
  - 네트워크는 느릴 것이다.
  - 서버는 가장 곤란한 순간에 실패할 것이다.
  - 이벤트는 순서가 어긋나 도착할 것이다.
  - 이벤트는 중복될 것이다.
- **`driven`이라는 낱말이 조건을 건다** — 이벤트 주도라는 이름은 **체계 전체가 메시지의 성공적
  전달에 의존한다**는 뜻이므로 "괜찮을 것"이라는 태도를 피하고 무슨 일이 있어도 이벤트가 일관되게
  전달되도록 보장해야 한다 (15장 §"Assume the worst", p.245).[^khononov2021]
- 그 보장의 수단 셋을 저자가 그대로 지목한다 (15장 §"Assume the worst", p.245):[^khononov2021]
  - 메시지를 신뢰성 있게 발행하려면 [아웃박스 패턴](outbox-pattern.md)을 쓴다.
  - 발행할 때 구독자가 **중복을 제거하고 순서가 어긋난 메시지를 식별해 재정렬할 수 있게** 한다.
  - 보상 동작이 필요한 경계 컨텍스트 간 프로세스를 조율할 때는 [사가](saga-pattern.md)와
    [프로세스 매니저](process-manager.md)를 지렛대 삼는다.

### 공개 이벤트와 사적 이벤트를 가르라

- **도메인 이벤트를 발행할 때 구현 세부를 드러내는 것을 경계하라** — 이벤트 소싱 애그리게이트에서
  특히 그렇다. **이벤트를 경계 컨텍스트 공개 인터페이스의 본래적 일부로 취급하라** (15장
  §"Use public and private events", p.245).[^khononov2021]
  - 그래서 열린 호스트 서비스 패턴을 구현할 때 **이벤트가 그 경계 컨텍스트의 공표된 언어에
    반영되도록** 보장한다 (15장, p.245).[^khononov2021] 이벤트 기반 모델을 변환하는 패턴은
    [모델 번역](model-translation.md)에 있다.
- **공개 인터페이스를 설계할 때 세 종류를 지렛대로 쓴다** (15장, pp.245–246):[^khononov2021]
  - ECST 메시지가 구현 모델을 **소비자가 필요로 하는 정보만 전하는 더 간결한 모델로 압축한다.**
  - 이벤트 알림은 공개 인터페이스를 **더 줄이는** 데 쓸 수 있다.
  - **도메인 이벤트는 외부 경계 컨텍스트와의 소통에 아껴 쓴다.** 전용 공개 도메인 이벤트 집합을
    따로 설계하는 것을 고려한다.

### 일관성 요구로 종류를 고르라

- 이벤트 주도 소통을 설계할 때 경계 컨텍스트의 **일관성 요구**를 종류 선택의 추가 어림법으로
  삼는다 (15장 §"Evaluate consistency requirements", p.246):[^khononov2021]
  - 구성 요소가 **결과적으로 일관된**(eventually consistent) 데이터로 만족할 수 있으면 ECST를
    쓴다.
  - 소비자가 **생산자 상태의 마지막 쓰기를 읽어야** 하면 이벤트 알림을 내고 뒤이어 질의로
    생산자의 최신 상태를 가져온다.
- 맺음이 세 종류를 다시 한 줄씩 규정한다 (15장 §Conclusion, p.246):[^khononov2021]

> Event notification
> A notification that something important has happened, but requiring the consumer to query the
> producer for additional information explicitly.
>
> Event-carried state transfer
> A message-based data replication mechanism. Each event contains a snapshot of a state that can
> be used to maintain a local cache of the producer's data.
>
> Domain event
> A message describing an event in the producer's business domain.

  - 그리고 **맞지 않는 종류를 쓰면 EDA 기반 체계가 탈선해 큰 진흙 공이 된다**는 판정으로 닫는다.
    올바른 종류를 고르려면 경계 컨텍스트의 일관성 요구를 평가하고 구현 세부를 드러내는 것을
    경계하며, 공개 이벤트와 사적 이벤트의 명시적 집합을 설계하고, 기술적 문제와 장애 앞에서도
    체계가 메시지를 전달하도록 보장하라 (15장 §Conclusion, p.246).[^khononov2021]

## 이 KB의 다른 자리들과의 분업

- [도메인 이벤트](../concepts/domain-events.md) — 세 종류 중 셋째의 규정 본체. 이 페이지는 그것이 **다른
  둘과 갈리는 지점**과 **언제 공개해야 하는가**만 갖는다.
- [이벤트 주도 애플리케이션 구조](../concepts/event-driven-application-structure.md) — 같은
  구분을 파이썬 실물로 다루는 축. 명령과 이벤트를 가르는 대목이 그곳에도 있다.
- [메시징 패턴](../synthesis/messaging-patterns.md) — 이 장이 메시지 패턴의 출처로 드는 카탈로그
  층의 허브.
- [아웃박스 패턴](outbox-pattern.md) · [사가 패턴](saga-pattern.md) ·
  [프로세스 매니저](process-manager.md) — 첫째 휴리스틱이 지목하는 세 수단.
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — ECST가 소비자 쪽에 만드는 것과 같은 모양의 읽기
  모델을 생산자 안에서 만드는 쪽.
- [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md) — 공개 이벤트가 계약이
  되면 따라오는 스키마 진화 문제.

## 이어지는 페이지

- [도메인 이벤트](../concepts/domain-events.md) — 세 종류 중 셋째의 본체
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 서비스 안에서 벌어지는 쪽
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 그 모델이 내는 이벤트를 그대로
  내보내면 안 되는 이유의 출발점
- [아웃박스 패턴](outbox-pattern.md) — 전달을 보증하는 기제
- [사가 패턴](saga-pattern.md) — 보상 동작으로 이벤트를 뒤집는 흐름
- [프로세스 매니저](process-manager.md) — 조율이 필요한 흐름
- [모델 번역](model-translation.md) — 사적 이벤트를 공개 이벤트로 바꾸는 층
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md) — 열린 호스트 서비스와 공표된 언어
- [CQRS 아키텍처](../concepts/cqrs-architecture.md) — 투영을 생산자 쪽에 두는 패턴
- [뒤·앞 호환성](../concepts/backward-and-forward-compatibility.md) — 이벤트 스키마가 바뀔 때
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 이 이벤트가 타는 채널
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 중복과 순서
  어긋남을 소비자 쪽에서 감당하는 방법
- [마이크로서비스 경계 어림법](microservice-boundary-heuristics.md) — 이 이벤트가 건너다니는
  경계를 정하는 쪽
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브
- [메시징 패턴](../synthesis/messaging-patterns.md) — 메시지 패턴 카탈로그의 허브

[^khononov2021]: Khononov 2021, 15장 "Event-Driven Architecture"(장 도입 p.233 ·
    §"Event-Driven Architecture" p.233 · §Events 도입 p.234 · §"Events, Commands, and
    Messages" pp.234–235 · §Structure p.235 · §"Types of Events" pp.236–241 —
    §"Event notification" pp.236–237 · §"Event-carried state transfer" pp.237–238 ·
    §"Domain event" p.239 · §"Domain events versus event notification" p.239 ·
    §"Domain events versus event-carried state transfer" p.240 ·
    §"Event types: Example" pp.240–241 · §"Designing Event-Driven Integration" pp.241–246 —
    §"Distributed Big Ball of Mud" pp.241–242 · §"Temporal Coupling" pp.242–243 ·
    §"Functional Coupling" p.243 · §"Implementation Coupling" p.243 ·
    §"Refactoring the Event-Driven Integration" pp.243–244 ·
    §"Event-Driven Design Heuristics" pp.245–246 · §Conclusion p.246). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 원문이 용어 정의를 들여쓴 정의 목록으로 조판한 자리(이벤트와 명령의
    규정 · 맺음의 세 종류 규정)는 그 서식을 인용 블록 안에서 표제 줄과 설명 줄로 옮겼다.
    코드 목록 여섯 중 펜스로 옮긴 것은 하나(결혼 사건의 세 표현, p.240)이고 나머지 다섯
    (일반 이벤트 스키마 · 급여 명세 알림 · 고객 상태 전체 스냅샷 ECST · 변경 필드만 담은
    ECST)은 산문으로 줄였다 — 개념당 대표 하나 규약이고, 고른 하나가 세 종류를 한 자리에서
    대조해 보이기 때문이다. 원문은 언어 표지 없이 조판되어 있고 식별자 대입문 형태라 이 KB가
    `js` 표지를 붙였다. 도판 여섯(Figure 15-1 비동기 소통 · 15-2 이벤트 알림 흐름 ·
    15-3 긴급 경보 체계 · 15-4 백엔드 포 프론트엔드 · 15-5 강하게 결합된 분산 체계 ·
    15-6 리팩터링된 체계)은 도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다. 위 비교 표
    둘은 원문에 없다 — 원문이 산문과 소절로 펴 놓은 대비를 이 KB가 표로 모은 것이고 각 칸의
    근거는 같은 절의 본문에 있다. 저자가 대는 출처 셋(Hohpe & Woolf 2003 — 이 KB가 이미 들인
    [hohpe2004](../sources/hohpe2004.md)라 링크를 걸었다 · 마틴 파울러의 "What do you mean by
    'Event-Driven'?" 블로그 글 · Andrew S. Grove, *Only the Paranoid Survive*, HarperCollins
    Business 1998 — 뒤 둘은 이 KB가 확인한 원전이 아니다)은 각주에 그렇게 적었다. 장 끝
    연습문제 넷(p.247)은 claim이 아니라 옮기지 않았다.

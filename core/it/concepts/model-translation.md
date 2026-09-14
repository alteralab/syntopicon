---
type: concept
title: 모델 번역
description: 두 경계 컨텍스트의 모델이 다를 때 그 변환을 실제로 어디에 어떻게 구현하는가 — 부패 방지 계층과 열린 호스트 서비스가 같은 번역 로직의 양쪽 끝이라 구현을 구분하지 않는다는 저자의 선언, 무상태 번역과 상태 있는 번역의 갈림, 프록시 패턴으로 요청을 가로채는 무상태 구현과 그것을 코드베이스에 심을 때와 API 게이트웨이로 밀어낼 때, 게이트웨이가 공표된 언어의 여러 버전을 함께 내주는 자리와 여러 하류가 공유하는 부패 방지 계층이 교환 컨텍스트가 되는 자리, 비동기 통신의 메시지 프록시와 잡음 걸러 내기, 도메인 이벤트를 그대로 내보내면 구현 모델이 새어 나간다는 흔한 실수와 사적 이벤트와 공개 이벤트의 구별, 들어오는 데이터를 모으는 번역은 게이트웨이로 구현할 수 없고 자기 저장소를 요구한다는 조항과 기성품 대안, 여러 원천을 하나로 합치는 백엔드 포 프론트엔드와 통합 복잡성을 업무 로직에서 떼어 내는 배치, 그리고 이 KB의 메시지 변환 패턴들과 무엇이 다른가
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 모델 번역

- [이 층이 서는 자리](#이-층이-서는-자리)
- [무상태냐 상태를 갖느냐](#무상태냐-상태를-갖느냐)
- [무상태 번역 — 프록시](#무상태-번역--프록시)
- [동기 — 코드베이스 안에 두거나 게이트웨이로 밀어내거나](#동기--코드베이스-안에-두거나-게이트웨이로-밀어내거나)
- [교환 컨텍스트](#교환-컨텍스트)
- [비동기 — 메시지 프록시](#비동기--메시지-프록시)
- [도메인 이벤트를 그대로 내보내는 것이 흔한 실수다](#도메인-이벤트를-그대로-내보내는-것이-흔한-실수다)
- [상태 있는 번역 — 들어오는 데이터를 모을 때](#상태-있는-번역--들어오는-데이터를-모을-때)
- [여러 원천을 하나로 합칠 때](#여러-원천을-하나로-합칠-때)
- [이 KB의 메시지 변환 패턴들과 무엇이 다른가](#이-kb의-메시지-변환-패턴들과-무엇이-다른가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **두 경계 컨텍스트의 모델이 다를 때 그 변환을 어디에 어떻게 구현하는가.**

## 이 층이 서는 자리

- 출발은 관계 패턴의 선택이 이미 끝난 지점이다. 두 팀이 협력할 수 있으면 파트너십이나 공유
  커널로 프로토콜 자체를 맞춰 버릴 수 있고, 그 선택지들은
  [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)에 있다.
- 번역이 필요해지는 것은 힘이 한쪽으로 기운 고객·공급자 관계에서 **하류가 상류의 모델에 순응할
  수 없을 때**다 (9장, p.137).[^khononov2021]

> In a customer–supplier relationship, the balance of power tips toward either the upstream
> (supplier) or the downstream (consumer) bounded context. Suppose the downstream bounded context
> cannot conform to the upstream bounded context's model. In this case, a more elaborate technical
> solution is required that can facilitate communication by translating the bounded contexts'
> models.

- **번역은 한쪽이 맡을 수도 있고 양쪽이 함께 맡을 수도 있다** (9장, p.138):[^khononov2021]

> This translation can be handled by one, or sometimes both, sides: the downstream bounded context
> can adapt the upstream bounded context's model to its needs using an anticorruption layer (ACL),
> while the upstream bounded context can act as an open-host service (OHS) and protect its consumers
> from changes to its implementation model by using an integration-specific published language.

- **이 페이지가 따로 서는 근거가 그다음 문장이다.** 저자는 두 패턴의 번역 로직이 닮았으므로 이
  장에서는 **패턴을 구분하지 않고 구현 선택지를 다루고 예외적인 경우에만 차이를 언급한다**고
  적는다 (9장, p.138).[^khononov2021]

> Since the translation logic is similar for both the anticorruption layer and the open-host service,
> this chapter covers the implementation options without differentiating between the patterns and
> mentions the differences only in exceptional cases.

  - 그래서 아래 내용은 [부패 방지 계층](../concepts/anticorruption-layer.md)에도
    [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md)의 열린 호스트 서비스에도 똑같이
    걸린다. 두 페이지 중 어느 한쪽에 두면 다른 쪽에서 절반이 사라진다.
  - **패턴의 선택은 저 두 페이지가, 그 선택을 실행하는 방법은 이 페이지가 맡는다.**

## 무상태냐 상태를 갖느냐

- 구현을 가르는 첫 축이 상태의 유무다 (9장, p.138):[^khononov2021]

> The model's translation logic can be either stateless or stateful. Stateless translation happens on
> the fly, as incoming (OHS) or outgoing (ACL) requests are issued, while stateful translation
> involves a more complicated translation logic that requires a database.

  - **방향이 패턴마다 뒤집힌다는 데 주의한다.** 열린 호스트 서비스는 **들어오는** 요청을
    번역하고, 부패 방지 계층은 **나가는** 요청을 번역한다. 같은 로직이 어느 쪽 끝에 붙느냐의
    차이다.

## 무상태 번역 — 프록시

- 무상태 쪽의 구현 기제가 하나로 지정된다 (9장, p.138):[^khononov2021]

> For stateless model translation, the bounded context that owns the translation (OHS for upstream,
> ACL for downstream) implements the proxy design pattern to interject the incoming and outgoing
> requests and map the source model to the bounded context's target model.

- 그 프록시를 어떻게 구현하느냐는 **두 경계 컨텍스트가 동기로 통신하는가 비동기로 통신하는가에
  달린다** (9장, p.138).[^khononov2021]

## 동기 — 코드베이스 안에 두거나 게이트웨이로 밀어내거나

- 기본형은 변환 로직을 경계 컨텍스트의 코드베이스에 심는 것이다 (9장, p.138):[^khononov2021]

> The typical way to translate models used in synchronous communication is to embed the
> transformation logic in the bounded context's codebase

  - 자리는 패턴마다 다르다 — **열린 호스트 서비스에서는 들어오는 요청을 처리할 때 공개 언어로의
    번역이 일어나고, 부패 방지 계층에서는 상류 경계 컨텍스트를 호출할 때 일어난다** (9장,
    p.138).[^khononov2021]
- 둘째 선택지는 그 로직을 밖으로 밀어내는 것이다 — **어떤 경우에는 번역 로직을 API 게이트웨이
  패턴 같은 외부 구성 요소로 떠넘기는 것이 더 비용 효율적이고 편할 수 있다** (9장,
  p.139).[^khononov2021]
  - 저자가 드는 실물은 오픈소스 쪽 Kong·KrakenD와 클라우드 벤더의 관리형 서비스 쪽
    AWS API Gateway·Google Apigee·Azure API Management다 (9장, p.139).[^khononov2021]
    **제품 목록은 2021년 시점의 예시다.**
- **게이트웨이를 명시적으로 두면 버전 관리가 쉬워진다** — 열린 호스트 패턴을 구현하는 경계
  컨텍스트에서는 게이트웨이가 내부 모델을 **통합에 최적화된 공표된 언어**로 바꾸는 일을 맡고,
  나아가 **경계 컨텍스트 API의 여러 버전을 관리하고 제공하는 과정을 덜어 줄 수 있다** (9장,
  p.139).[^khononov2021]
  - 공표된 언어(published language)가 무엇인지는
    [컨텍스트 관계 패턴 §공표된 언어](../concepts/context-relationship-patterns.md)에 있다.

## 교환 컨텍스트

- 부패 방지 계층 쪽에도 게이트웨이 구현이 성립하고, 그때 계층 하나를 **여러 하류 경계 컨텍스트가
  함께 소비할 수 있다** (9장, p.139).[^khononov2021]
- 그렇게 되면 그 계층 자체가 하나의 경계 컨텍스트가 된다 (9장, p.139):[^khononov2021]

> Such bounded contexts, which are mainly in charge of transforming models for more convenient
> consumption by other components, are often referred to as interchange contexts.

  - **이름이 붙는 자리가 여기다.** 부패 방지 계층은 원래 한 하류가 자기를 지키려고 세우는 것인데
    (그 규정은 [부패 방지 계층](../concepts/anticorruption-layer.md)에 있다), 여러 하류가 같은
    상류를 상대하면 그 계층이 공유 자산이 되고 독립된 컨텍스트로 승격한다.

## 비동기 — 메시지 프록시

- 비동기 쪽의 이름이 따로 있다 (9장, p.140):[^khononov2021]

> To translate models used in asynchronous communication you can implement a message proxy: an
> intermediary component subscribing to messages coming from the source bounded context. The proxy
> will apply the required model transformations and forward the resultant messages to the target
> subscriber

- 번역 말고 하나를 더 할 수 있다 — **모델을 번역하는 것에 더해 가로채는 구성 요소는 무관한
  메시지를 걸러 내어 대상 경계 컨텍스트의 잡음을 줄일 수도 있다** (9장, p.140).[^khononov2021]
  - 이 필터링을 이름 붙여 카탈로그로 정리한 층이
    [메시지 라우팅 패턴](../concepts/message-routing-patterns.md)의 *Message Filter*다.

## 도메인 이벤트를 그대로 내보내는 것이 흔한 실수다

- 비동기 번역이 선택이 아니라 요구가 되는 자리가 있다 — **비동기 모델 번역은 열린 호스트
  서비스를 구현할 때 필수적이다** (9장, p.140).[^khononov2021]
- 왜 필수인가가 실수의 모양으로 제시된다 (9장, p.140):[^khononov2021]

> It's a common mistake to design and expose a published language for the model's objects and allow
> domain events to be published as they are, thereby exposing the bounded context's implementation
> model.

  - 처방은 가로채는 것이다 — **비동기 번역을 써서 도메인 이벤트를 가로채 공표된 언어로 바꾸면
    경계 컨텍스트의 구현 세부를 더 잘 캡슐화할 수 있다** (9장, p.140).[^khononov2021]
- **그 번역이 이벤트를 두 종류로 가른다** — 메시지를 공표된 언어로 번역하면 **경계 컨텍스트의
  내부 필요를 위한 사적 이벤트(private events)와 다른 경계 컨텍스트와의 통합을 위해 설계된
  공개 이벤트(public events)를 구분할 수 있게 된다** (9장, p.140).[^khononov2021]
  - 저자는 이 주제를 15장(도메인 주도 설계와 이벤트 기반 아키텍처의 관계)에서 다시 다룬다고
    적는다 (9장, p.140).[^khononov2021]
  - 도메인 이벤트 자체의 규정은 [도메인 이벤트](../concepts/domain-events.md)에 있다.

## 상태 있는 번역 — 들어오는 데이터를 모을 때

- 상태가 필요해지는 조건이 규정된다 (9장, p.141):[^khononov2021]

> For more significant model transformations—for example, when the translation mechanism has to
> aggregate the source data or unify data from multiple sources into a single model—a stateful
> translation may be required.

- 모으는 쓰임이 둘이다 (9장, p.141):[^khononov2021]
  - **성능 최적화를 위해 들어오는 요청을 모아 배치로 처리하는 경우.** 이 집계는 동기 요청에도
    비동기 요청에도 필요할 수 있다.
  - **여러 개의 잘게 나뉜 메시지를 통합된 데이터를 담은 하나의 메시지로 합치는 경우.**
- **여기서 게이트웨이가 탈락한다** (9장, p.142):[^khononov2021]

> Model transformation that aggregates incoming data cannot be implemented using an API gateway, and
> thus requires more elaborate, stateful processing.

  - 그래서 **들어오는 데이터를 추적하고 그에 맞게 처리하려면 번역 로직이 자기 영속 저장소를
    가져야 한다** (9장, p.142).[^khononov2021]
- 직접 만들지 않아도 되는 길이 함께 제시된다 — **어떤 쓰임에서는 기성품을 써서 상태 있는 번역의
  자체 구현을 피할 수 있다**. 저자가 드는 것은 스트림 처리 플랫폼(Kafka, AWS Kinesis 등)과
  배치 솔루션(Apache NiFi, AWS Glue, Spark 등)이다 (9장, p.142).[^khononov2021]
  - **제품 목록은 2021년 시점의 예시다.** 그 쪽 기제의 정본은
    [스트림 처리](../synthesis/stream-processing.md) 축에 있다.

## 여러 원천을 하나로 합칠 때

- 둘째 쓰임은 원천이 여럿일 때다 — **경계 컨텍스트가 다른 경계 컨텍스트들을 포함한 여러
  원천에서 온 데이터 집합을 처리해야 할 수 있다** (9장, p.142).[^khononov2021]
- 전형적인 예로 백엔드 포 프론트엔드(backend-for-frontend) 패턴이 제시된다 — **사용자
  인터페이스가 여러 서비스에서 온 데이터를 합쳐야 하는 경우**다 (9장,
  p.142).[^khononov2021]
  - 저자가 이 이름의 출처로 대는 것은 Chris Richardson, *Microservice Patterns: With Examples
    in Java*(Manning, 2019)다 (9장, p.142, 각주 1).[^khononov2021] **이 KB가 확인한 원전이
    아니다.**
- 둘째 예가 이 페이지의 배치 조항이다 — 여러 컨텍스트의 데이터를 받아 복잡한 업무 로직으로
  처리해야 하는 경계 컨텍스트라면, **다른 모든 경계 컨텍스트의 데이터를 모으는 부패 방지 계층을
  앞에 세워 통합의 복잡성과 업무 로직의 복잡성을 떼어 놓는 것이 이로울 수 있다** (9장,
  p.142).[^khononov2021]
  - **이 배치가 부패 방지 계층의 쓰임을 하나 늘린다.** 원전에서 이 계층은 모델을 오염에서
    지키는 방어물이고, 여기서는 **복잡성을 한 자리에 모으는 분업 장치**로도 쓰인다.

## 이 KB의 메시지 변환 패턴들과 무엇이 다른가

이 KB에는 이미 변환을 이름 붙여 정리한 층이 있다. 겹치는 낱말이 많아 경계를 적어 둔다.

| 이 페이지 | 이웃 페이지 | 무엇이 다른가 |
|---|---|---|
| 번역의 대상 = 경계 컨텍스트의 **모델**(유비쿼터스 언어) | [메시지 변환 패턴](../concepts/message-transformation-patterns.md)의 *Message Translator* — 번역의 대상 = 애플리케이션 사이의 **데이터 형식** | 같은 낱말이지만 층이 다르다. 형식이 같아도 모델이 다르면 여기 번역이 남는다 |
| 여러 메시지를 하나로 합치는 상태 있는 번역 | [분할·집계·재정렬 패턴](../concepts/splitter-aggregator-resequencer-patterns.md)의 *Aggregator* | 저쪽이 완료 조건·집계 알고리즘·늦게 온 메시지까지 규정한다. 이 판본은 그 기제를 되풀이하지 않는다 |
| 빠진 데이터를 다른 컨텍스트에서 가져와 채우는 번역 | [데이터 강화와 장식 패턴](../concepts/data-enrichment-and-decoration-patterns.md)의 *Content Enricher* | 저쪽이 정보의 출처 셋과 기각된 대안 넷을 갖는다 |
| 사적 이벤트와 공개 이벤트의 구별 | [인코딩과 진화](../synthesis/encoding-and-evolution.md) | 저쪽은 같은 문제를 스키마 호환성으로 다룬다 |

- **그러므로 이 페이지의 값은 기제가 아니라 배치다.** 무엇을 변환하는가(모델)와 누가 소유하는가
  (상류의 열린 호스트 서비스냐 하류의 부패 방지 계층이냐)를 정하는 것이 여기 있고, 변환 자체의
  구현 어휘는 위 표의 오른쪽 페이지들이 갖는다.

## 이어지는 페이지

- [부패 방지 계층](../concepts/anticorruption-layer.md) — 하류가 이 번역을 소유할 때
- [컨텍스트 관계 패턴](../concepts/context-relationship-patterns.md) — 상류가 이 번역을 소유할 때
  (열린 호스트 서비스와 공표된 언어)
- [경계 컨텍스트](../concepts/bounded-context.md) — 번역이 필요해지는 경계 자체
- [컨텍스트 지도](../concepts/context-map.md) — 어느 관계에 어느 번역이 걸리는지의 지도
- [도메인 이벤트](../concepts/domain-events.md) — 비동기 번역이 가로채는 대상
- [아웃박스 패턴](outbox-pattern.md) — 그 이벤트를 신뢰성 있게 내보내는 기제
- [메시지 변환 패턴](../concepts/message-transformation-patterns.md) — 형식 차이를 다루는 이름 층
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 메시지 프록시가 구독하는 채널
- [메시징 패턴](../synthesis/messaging-patterns.md) — 이름 층의 허브
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 9장 "Communication Patterns" §"Model Translation"(도입
    pp.137–138 · §"Stateless Model Translation" 중 §Synchronous pp.138–139·§Asynchronous p.140 ·
    §"Stateful Model Translation" 중 §"Aggregating incoming data" pp.141–142·§"Unifying multiple
    sources" pp.142–143). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 직인용은
    `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는 곧은 따옴표로 옮겼다. 원문이
    기울임으로 조판한 패턴 이름(stateless translation · stateful translation · message proxy ·
    interchange contexts)은 인용 블록에서 기울임 표기를 떼고 옮겼다. 도판 열(Figure 9-1 프록시에
    의한 모델 번역 · 9-2 동기 통신 · 9-3 공표된 언어의 여러 버전 노출 · 9-4 공유 부패 방지 계층 ·
    9-5 비동기 통신에서의 모델 번역 · 9-6 공표된 언어로 된 도메인 이벤트 · 9-7 요청 배치 ·
    9-8 들어오는 이벤트 통합 · 9-9 상태 있는 모델 변환 · 9-10 부패 방지 계층 패턴으로 통합 모델
    단순화하기)은 도판이라 본문이 그것에 대해 적는 것만 산문으로 옮겼다. 이 절에는 코드 목록이
    없어 펜스를 두지 않았다. 저자가 대는 출처 하나(Chris Richardson, *Microservice Patterns*,
    Manning 2019)는 이 KB가 확인한 원전이 아니다.

---
type: concept
title: 자원과 표현
description: HTTP가 다루는 대상을 자원(resource)과 표현(representation) 둘로 가르는 정의와 그 이유 — HTTP가 자원의 성질을 제한하지 않고 인터페이스만 정의한다는 것, 자원 식별을 요청 의미론에서 떼어 메서드에 맡긴 설계 목표, 자원 자체 대신 옮길 수 있는 표현으로 통신을 정의해 정보 은닉을 얻는다는 것, 그리고 표현이 여럿일 때 조건부 요청과 200·206·304 응답의 재료가 되는 선택된 표현
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T09:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# 자원과 표현

- [버전 조건](#버전-조건)
- [자원이란 무엇인가](#자원이란-무엇인가)
- [식별과 요청 의미론의 분리](#식별과-요청-의미론의-분리)
- [표현이란 무엇인가](#표현이란-무엇인가)
- [자원 자체를 옮기지 않는 이유](#자원-자체를-옮기지-않는-이유)
- [선택된 표현](#선택된-표현)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP가 주고받는 대상은 정확히 무엇이고, 왜 자원 자체가 아니라 표현을 옮기는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 자원이란 무엇인가

- 정의는 대상의 성질이 아니라 자리로 내려진다 (§3.1).[^fielding2022-rfc9110]

  > The target of an HTTP request is called a "resource".  HTTP does not limit the nature of
  > a resource; it merely defines an interface that might be used to interact with resources.

  요청의 대상이면 자원(resource)이다. 그것이 무엇인지는 묻지 않고, 상호작용에 쓰일 수 있는
  인터페이스만 정의한다.
- 대부분의 자원은 URI(Uniform Resource Identifier)로 식별된다 (§3.1).[^fielding2022-rfc9110]
- HTTP는 대상 자원을 가리키는 일과 자원 사이의 관계를 나타내는 일 양쪽에서 URI 표준에 의존한다
  (§3.1).[^fielding2022-rfc9110]

## 식별과 요청 의미론의 분리

- HTTP의 설계 목표 하나가 **자원 식별을 요청 의미론에서 떼어 놓는 것**이고, 그것이 가능한 이유는
  요청 의미론을 요청 메서드와 몇몇 요청 수정 헤더 필드에 담아 두었기 때문이다
  (§3.1).[^fielding2022-rfc9110]
- 그 분리는 자원 쪽에 금지로 걸린다. **자원은 요청을 그 요청의 메서드가 갖는 의미론과 어긋나는
  방식으로 다룰 수 없다** (§3.1).[^fielding2022-rfc9110]
- 그래서 URI가 풍기는 인상은 구속력이 없다. 원전이 든 예다 — **자원의 URI가 안전하지 않은
  의미론을 함의하는 것처럼 보이더라도, 클라이언트는 그 자원이 안전한 메서드로 온 요청을 처리할
  때 안전하지 않은 동작을 피하리라 기대할 수 있다** (§3.1).[^fielding2022-rfc9110] 어느 메서드가
  안전한지는 이 문서의 메서드 절이 정한다.
- 그 자리가 §9.2.1이다. **정의된 의미론이 본질적으로 읽기 전용인** 메서드가 안전하고, 이 명세가
  정의한 메서드 중에서는 GET·HEAD·OPTIONS·TRACE 넷이 그렇다 (§9.2.1).[^fielding2022-rfc9110]
  대상 URI의 파라미터가 행위를 고르게 자원을 구성했다면, 그 행위를 메서드 의미론과 일관되게 만드는
  것은 **자원 소유자의 책임**이다 (§9.2.1).[^fielding2022-rfc9110] 세 공통 속성의 정의와 분포는
  [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)에
  있다.

## 표현이란 무엇인가

- 정의 문장이다 (§3.2).[^fielding2022-rfc9110]

  > A "representation" is information that is intended to reflect a past, current, or desired
  > state of a given resource, in a format that can be readily communicated via the protocol.

  표현(representation)은 주어진 자원의 과거나 현재나 **바라는(desired)** 상태를 반영하도록
  의도된 정보다. 세 시제가 다 들어 있다는 점이 중요하다 — 클라이언트가 보내는 요청 본문도
  표현이고, 그것은 "이렇게 되기를 바란다"는 상태다.
- 표현은 두 부분으로 이뤄진다. 표현 메타데이터(representation metadata) 한 벌과, 잠재적으로
  경계가 없는 표현 데이터(representation data)의 스트림이다 (§3.2).[^fielding2022-rfc9110]

## 자원 자체를 옮기지 않는 이유

- HTTP는 자원 자체를 전송하는 대신 **자원 상태의 전송 가능한 표현**을 놓고 통신을 정의함으로써
  균일 인터페이스 뒤에 정보 은닉(information hiding)을 허용한다 (§3.2).[^fielding2022-rfc9110]
- 그 결과 URI가 식별하는 것이 무엇이든 될 수 있다. 원전이 드는 예가 "라구나 비치의 현재 날씨"
  같은 **시간의 함수**다. 그런 것조차 메시지가 생성되는 시점에 그 자원을 표현하는 정보를 줄 수
  있다 (§3.2).[^fielding2022-rfc9110]
- 원전이 이 배치를 창에 비유한다 — 어떤 것을 오직 건너편의 독립된 행위자에게 메시지를 보냄으로써
  관측하고 그 위에 작용하는 창이다. 그러려면 그 어떤 것의 현재나 바라는 상태를 우리 통신 안에서
  **대신할** 공유된 추상이 필요하다 (§3.2).[^fielding2022-rfc9110]
- 표현이 하이퍼텍스트일 때는 한 겹을 더 실을 수 있다. 자원 상태의 표현인 동시에, 수신자의 앞으로의
  상호작용을 안내하는 처리 지시를 함께 제공한다 (§3.2).[^fielding2022-rfc9110]

## 선택된 표현

- 대상 자원 하나가 여러 표현을 가지거나 생성할 수 있고, 그 각각이 자원의 현재 상태를 반영하도록
  의도된 것일 수 있다 (§3.2).[^fielding2022-rfc9110]
- 그중 하나를 고르는 일은 알고리즘이 하고, 그 알고리즘은 대개 콘텐츠 협상(content negotiation)에
  기반한다 (§3.2).[^fielding2022-rfc9110]
- 고른 결과에 이름이 붙는다. 이 **"선택된 표현"(selected representation)이 조건부 요청을 평가하고
  GET에 대한 200(OK)·206(Partial Content)·304(Not Modified) 응답의 콘텐츠를 구성할 데이터와
  메타데이터를 제공한다** (§3.2).[^fielding2022-rfc9110] 이 한 문장이 조건부 요청과 범위 요청과
  캐시 재검증이 무엇을 놓고 도는지를 정한다.
- 그 데이터와 메타데이터의 규범이 이 문서 뒤쪽에 있다. 표현 데이터는 `Content-Type` 위에
  `Content-Encoding`을 얹은 **두 겹의 순서 있는 인코딩 모델**로 정의되고, 그것을 서술하는 표현 헤더
  필드가 메시지에 콘텐츠가 있을 때 그 데이터를 어떻게 해석할지 알려 준다
  (§8.1, §8.2).[^fielding2022-rfc9110] 각 필드는
  [표현 메타데이터](../concepts/http-representation-metadata.md)가 다룬다.
- 선택된 표현이 바뀌었는지를 재는 메타데이터에는 따로 이름이 붙는다. 조건부 요청의 전제 조건에 쓰일 수
  있는 자원 메타데이터를 **검증자(validator)**라 하고, 검증자 필드는 선택된 표현의 현재 검증자를 전한다
  (§8.8).[^fielding2022-rfc9110] 강한 검증자와 약한 검증자의 구분과 두 실물은
  [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md)에 있다.

## 이어지는 페이지

- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — 이 두 낱말이 놓인 정의
- [http와 https URI 스킴과 정규화](../concepts/http-uri-schemes-and-normalization.md) — 자원을
  가리키는 식별자의 문법과 같은 자원인지 판정하는 규칙
- [표현 메타데이터](../concepts/http-representation-metadata.md) — 표현 데이터를 어떻게 해석할지
  알려 주는 필드들
- [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md) — 선택된
  표현이 바뀌었는지를 재는 메타데이터
- [HTTP 클라이언트와 서버와 무상태성](../concepts/http-clients-servers-and-statelessness.md) —
  이 표현을 주고받는 메시지의 구조
- [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)
  — 안전한 메서드로 온 요청에 자원이 무엇을 해서는 안 되는가
- [HTTP 요청 메서드의 지위](../concepts/http-request-methods-overview.md) — 요청 의미론을 담는
  그 메서드 토큰의 규정
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 이 두 낱말을 설계 원칙으로 삼는 쪽

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다.

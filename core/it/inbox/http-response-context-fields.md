---
type: concept
title: 응답 컨텍스트 필드
description: 상태 코드가 함의하는 것 너머로 응답의 맥락을 알리는 네 필드 — 대상 자원이 지원한다고 광고하는 메서드 목록인 Allow와 405에 걸린 생성 요건, 응답과의 관계가 메서드와 상태 코드의 조합으로 정해지는 Location과 201과 3xx에서 갈리는 뜻 및 프래그먼트 상속 규칙, 언제 다시 오라는 지시인 Retry-After와 그 두 값 형식, 그리고 원 서버 소프트웨어를 알리는 Server와 내부를 드러내지 말라는 경고
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T15:35:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# 응답 컨텍스트 필드

- [버전 조건](#버전-조건)
- [이 필드들이 답하는 것](#이-필드들이-답하는-것)
- [Allow](#allow)
- [Location](#location)
- [Location과 프래그먼트](#location과-프래그먼트)
- [Retry-After](#retry-after)
- [Server](#server)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **상태 코드만으로는 알 수 없는 응답의 맥락을 알리는 필드들은 각각 무엇을 말하는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 이 필드들이 답하는 것

- 절의 머리말이 범위를 긋는다. 아래 응답 헤더 필드들은 **상태 코드가 함의하는 것 너머로 응답에 대한
  추가 정보를 제공하며, 서버에 대한 정보나 대상 자원에 대한 정보나 관련 자원에 대한 정보를
  포함한다** (§10.2).[^fielding2022-rfc9110]

## Allow

- 정의 문장이다 (§10.2.1).[^fielding2022-rfc9110]

  > The "Allow" header field lists the set of methods advertised as supported by the target
  > resource.

  **대상 자원이 지원한다고 광고된 메서드 집합**을 나열한다. 값은 메서드 이름의 리스트이고, 원전이
  든 예가 `Allow: GET, HEAD, PUT`이다.
- 목적이 좁게 규정된다. **이 필드의 목적은 엄격히 그 자원과 연관된 유효한 요청 메서드를 수신자에게
  알리는 것**이다 (§10.2.1).[^fielding2022-rfc9110]
- 실제 집합의 결정 시점이 명시된다. **실제로 허용되는 메서드 집합은 매 요청 시점에 원 서버가
  정의한다** (§10.2.1).[^fielding2022-rfc9110] 곧 이 필드는 그 시점의 광고이지 계약이 아니다.
- 생성 요건이 상태 코드에 걸린다. 원 서버는 **405(Method Not Allowed) 응답에 `Allow` 필드를 생성해야
  하고**(MUST), 다른 어떤 응답에서도 생성해도 된다(MAY) (§10.2.1).[^fielding2022-rfc9110]
- 빈 값에도 뜻이 있다. **빈 `Allow` 필드 값은 그 자원이 어떤 메서드도 허용하지 않음을 나타내며**,
  자원이 설정으로 일시 비활성화된 405 응답에서 일어날 수 있다 (§10.2.1).[^fielding2022-rfc9110]
- 중개자에는 금지가 걸린다. **프록시는 `Allow` 필드를 수정해서는 안 된다**(MUST NOT). 표시된 메서드를
  전부 이해해야 일반 메시지 처리 규칙에 따라 다룰 수 있는 것은 아니기 때문이다
  (§10.2.1).[^fielding2022-rfc9110]

## Location

- 정의 문장이다 (§10.2.2).[^fielding2022-rfc9110]

  > The "Location" header field is used in some responses to refer to a specific resource in
  > relation to the response.  The type of relationship is defined by the combination of
  > request method and status code semantics.

  응답과 관련해 **특정 자원을 가리키는 데** 쓰이며, **그 관계의 종류는 요청 메서드와 상태 코드
  의미론의 조합이 정의한다.** 곧 이 필드 혼자서는 뜻이 정해지지 않는다.
- 값은 URI 참조 하나다. 상대 참조 형태이면 최종 값은 **대상 URI를 기준으로 해소해 계산한다**
  (§10.2.2).[^fielding2022-rfc9110]
- 두 조합의 뜻이 명시되어 있다 (§10.2.2).[^fielding2022-rfc9110]
  - **201(Created)** 응답에서 그 값은 **그 요청이 만든 주된 자원**을 가리킨다.
  - **3xx(Redirection)** 응답에서 그 값은 **요청을 자동으로 리다이렉트할 선호 대상 자원**을 가리킨다.
  - 두 상태 코드 자체의 규범은 이 문서의 상태 코드 절(§15)이 정한다 (§10.2.2).[^fielding2022-rfc9110]

## Location과 프래그먼트

- 상속 규칙이 있다. 3xx 응답의 `Location` 값에 프래그먼트 컴포넌트가 없으면, 사용자 에이전트는
  **그 값이 대상 URI를 만드는 데 쓰인 URI 참조의 프래그먼트 컴포넌트를 상속하는 것처럼 리다이렉션을
  처리해야 한다**(MUST) (§10.2.2).[^fielding2022-rfc9110]
- 원전이 든 예 둘이 두 방향을 보여 준다 (§10.2.2).[^fielding2022-rfc9110]
  - `Location` 값 자체가 프래그먼트를 가지면 그것이 쓰인다.
  - `Location` 값에 프래그먼트가 없고 원래 참조에 있었으면 **원래 것이 보존된다.**
- 프래그먼트가 어울리지 않는 자리도 있다. 원전이 드는 예가 **201 응답의 `Location`** 인데, 만들어진
  자원에 특정된 URI를 주기로 되어 있기 때문이다 (§10.2.2).[^fielding2022-rfc9110]
- 원전이 각주로 두 가지를 덧붙인다 (§10.2.2).[^fielding2022-rfc9110]
  - 어떤 수신자는 유효한 URI 참조가 아닌 `Location` 값에서 복구를 시도한다. **이 명세는 그런 처리를
    강제하지도 정의하지도 않으나 견고성을 위해 허용은 한다.** `Location` 값이 리스트를 담을 수 없는
    이유도 적혀 있다 — 리스트 구분자인 콤마가 URI 참조 안에서 유효한 데이터 문자이기 때문이다.
  - `Content-Location`은 이것과 다르다. 그쪽은 **실린 표현에 대응하는 가장 구체적인 자원**을 가리키며,
    한 응답이 `Location`과 `Content-Location`을 **둘 다 담는 것이 가능하다.**

## Retry-After

- 정의 문장이다 (§10.2.3).[^fielding2022-rfc9110]

  > Servers send the "Retry-After" header field to indicate how long the user agent ought to
  > wait before making a follow-up request.

  **사용자 에이전트가 후속 요청을 하기 전에 얼마나 기다리는 것이 좋은지**를 나타내려고 서버가 보낸다.
- 어느 응답에 실리느냐에 따라 뜻이 갈린다 (§10.2.3).[^fielding2022-rfc9110]
  - **503(Service Unavailable)** 과 함께 보내면 그 서비스가 이 클라이언트에게 **얼마나 오래 불가용할
    것으로 예상되는지**를 나타낸다.
  - **3xx(Redirection)** 과 함께 보내면 사용자 에이전트가 리다이렉트된 요청을 내기 전에 기다리기를
    요청받는 **최소 시간**을 나타낸다.
- 값은 두 형식 중 하나다. **HTTP-date이거나, 응답을 받은 뒤 지연시킬 초 수**다. 초 수는 음이 아닌
  십진 정수다 (§10.2.3).[^fielding2022-rfc9110] 원전이 든 예가 절대 시각 하나와 `120`이고,
  후자의 지연은 2분이다.
- 이 필드가 이 KB의 부하 쪽 서술과 맞닿는 자리다. 과부하 상태의 서버가 **재시도 시점을 프로토콜
  안에서 지시할 수 있는 유일한 표준 수단**이며, 그 지시가 없으면 재시도 시점은 전적으로 클라이언트가
  정한다 (§10.2.3).[^fielding2022-rfc9110] 클라이언트가 각자 정한 재시도가 부하를 되먹이는 기제는
  [메타안정 실패의 정의](../concepts/metastable-failure-definition.md)와
  [지속 효과와 증폭](../concepts/sustaining-effects-and-amplification.md)이 다룬다.

## Server

- 정의 문장이다 (§10.2.4).[^fielding2022-rfc9110]

  > The "Server" header field contains information about the software used by the origin
  > server to handle the request, which is often used by clients to help identify the scope of
  > reported interoperability problems, to work around or tailor requests to avoid particular
  > server limitations, and for analytics regarding server or operating system use.

  **원 서버가 요청을 다루는 데 쓴 소프트웨어에 대한 정보**를 담는다. 쓰임은 `User-Agent`의 거울상이다.
  원 서버는 응답에 이 필드를 생성해도 된다(MAY).
- 값의 구성은 `User-Agent`와 같다. 하나 이상의 제품 식별자와 그 각각에 딸린 0개 이상의 코멘트로
  이뤄지고, **식별에 중요한 순으로 내림차순 나열**하며, 각 식별자는 이름과 선택적 버전으로 이뤄진다
  (§10.2.4).[^fielding2022-rfc9110]
- 경고도 거울상이되 항목이 하나 더 있다. 원 서버는 **쓸데없이 잘게 쪼갠 세부를 담은 값을 생성해서는 안
  되고**(SHOULD NOT) 제삼자에 의한 하위 제품 추가를 제한해야 한다. 지나치게 길고 상세한 값은 **응답
  지연을 늘리고**, 알려진 보안 구멍을 찾아 악용하기를 (약간) 쉽게 만들 수 있는 **내부 구현 세부를
  드러낼 수 있다** (§10.2.4).[^fielding2022-rfc9110]

## 이어지는 페이지

- [요청 컨텍스트 필드](../concepts/http-request-context-fields.md) — 같은 축의 요청 쪽 다섯 필드
- [HTTP 요청 메서드의 지위](../concepts/http-request-methods-overview.md) — Allow가 실어 나르는 그
  메서드 집합과 405의 자리
- [POST와 PUT](../concepts/http-post-and-put.md) — 201과 3xx가 Location과 함께 나오는 자리
- [DELETE와 CONNECT와 OPTIONS와 TRACE](../concepts/http-delete-connect-options-and-trace.md) —
  OPTIONS 응답이 Allow를 보내야 하는 자리
- [표현 메타데이터](../concepts/http-representation-metadata.md) — Location과 갈리는 Content-Location
- [HTTP 날짜 형식](../concepts/http-date-formats.md) — Retry-After가 쓸 수 있는 HTTP-date의 문법
- [메타안정 실패의 정의](../concepts/metastable-failure-definition.md) — 재시도가 부하를 되먹이는
  상태의 정의
- [지속 효과와 증폭](../concepts/sustaining-effects-and-amplification.md) — 재시도가 증폭기가 되는 기제

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다.

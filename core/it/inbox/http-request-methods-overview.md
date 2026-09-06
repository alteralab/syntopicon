---
type: concept
title: HTTP 요청 메서드의 지위
description: 요청 의미론의 일차 출처가 메서드 토큰이라는 규정과 그 토큰이 놓인 자리 — 헤더 필드가 의미론을 더 좁힐 수 있으나 어긋날 수는 없다는 제약, 토큰이 대소문자를 가리는 이유, 분산 객체 시스템과 갈리는 지점인 자원별 메서드의 부재, 표준 메서드 여덟의 목록과 GET·HEAD만 필수라는 요건, 그리고 모르는 메서드와 허용되지 않은 메서드에 각각 붙는 상태 코드와 메서드 레지스트리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T15:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 요청 메서드의 지위

- [버전 조건](#버전-조건)
- [요청 의미론의 일차 출처](#요청-의미론의-일차-출처)
- [분산 객체 시스템과 갈리는 지점](#분산-객체-시스템과-갈리는-지점)
- [표준 메서드 여덟](#표준-메서드-여덟)
- [모르는 메서드와 막힌 메서드](#모르는-메서드와-막힌-메서드)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **요청이 무엇을 하려는 것인지를 정하는 것은 무엇이고, 그 자리에 아무 낱말이나
올 수 있는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 요청 의미론의 일차 출처

- 규정 문장이다 (§9.1).[^fielding2022-rfc9110]

  > The request method token is the primary source of request semantics; it indicates the
  > purpose for which the client has made this request and what is expected by the client as
  > a successful result.

  요청 메서드 토큰이 요청 의미론(request semantics)의 **일차 출처**다. 무엇을 하려고 이 요청을
  보냈는지와 성공했을 때 클라이언트가 무엇을 기대하는지를 그 토큰이 가리킨다.
- 헤더 필드가 그 의미론을 더 좁힐 수 있다. 다만 조건이 붙는다 — **추가되는 의미론이 메서드와
  어긋나지 않을 때만**이다 (§9.1).[^fielding2022-rfc9110] 원전이 드는 예가 조건부 요청 헤더
  필드로 요청 행위를 대상 자원의 현재 상태에 걸리게 만드는 것이다.
- 메서드 토큰의 문법은 한 줄이다 (§9.1).[^fielding2022-rfc9110]

  ```abnf
  method = token
  ```

- 이 토큰은 **대소문자를 가린다**(case-sensitive). 대소문자를 가리는 메서드 이름을 가진 객체 기반
  시스템으로 가는 게이트웨이로 쓰일 수 있기 때문이다. 관례로 표준 메서드는 전부 대문자 US-ASCII
  글자로 정의한다 (§9.1).[^fielding2022-rfc9110]

## 분산 객체 시스템과 갈리는 지점

- HTTP는 **분산 객체 시스템의 인터페이스로 쓸 수 있게 설계되었다.** 요청 메서드는 식별된 객체에
  원격 메서드 호출을 보내는 것과 거의 같은 방식으로 대상 자원에 적용될 행위를 부른다
  (§9.1).[^fielding2022-rfc9110]
- 그러나 결정적으로 갈리는 자리가 있다. **HTTP의 표준 요청 메서드는 자원별로 따로 있지 않다.**
  균일 인터페이스가 네트워크 기반 시스템에서 더 나은 가시성과 재사용을 주기 때문이라고 원전이 적고,
  그 근거로 REST를 참조한다 (§9.1).[^fielding2022-rfc9110]
- 그 귀결이 메서드의 보편성이다. 한번 정의된 표준 메서드는 **어느 자원에 적용되든 같은 의미론을
  가져야 한다.** 다만 그 의미론을 구현할지 허용할지는 자원마다 스스로 정한다
  (§9.1).[^fielding2022-rfc9110] 곧 뜻은 하나이고 지원 여부만 갈린다.

## 표준 메서드 여덟

- 이 명세가 정의하는 표준 메서드는 여덟이다 (§9.1, Table 4).[^fielding2022-rfc9110]

  | 메서드 | 하는 일 | 절 |
  |---|---|---|
  | GET | 대상 자원의 현재 표현을 전송한다 | §9.3.1 |
  | HEAD | GET과 같되 응답 콘텐츠를 전송하지 않는다 | §9.3.2 |
  | POST | 요청 콘텐츠에 대해 자원별 처리를 수행한다 | §9.3.3 |
  | PUT | 대상 자원의 현재 표현 전부를 요청 콘텐츠로 대치한다 | §9.3.4 |
  | DELETE | 대상 자원의 현재 표현 전부를 제거한다 | §9.3.5 |
  | CONNECT | 대상 자원이 식별하는 서버로 가는 터널을 만든다 | §9.3.6 |
  | OPTIONS | 대상 자원의 통신 옵션을 서술한다 | §9.3.7 |
  | TRACE | 대상 자원까지의 경로를 따라 메시지 루프백 시험을 수행한다 | §9.3.8 |

- 여덟 중 둘만 필수다. **모든 범용 서버는 GET과 HEAD를 지원해야 하고, 그 밖의 모든 메서드는
  선택이다** (§9.1).[^fielding2022-rfc9110]

## 모르는 메서드와 막힌 메서드

- 대상 자원이 허용하는 메서드 집합은 `Allow` 헤더 필드에 나열될 수 있다. 다만 **그 집합은 동적으로
  바뀔 수 있다** (§9.1).[^fielding2022-rfc9110] 그 필드의 규범은
  [응답 컨텍스트 필드](../concepts/http-response-context-fields.md)에 있다.
- 두 가지 거절이 갈린다 (§9.1).[^fielding2022-rfc9110]
  - 알아보지 못하거나 구현하지 않은 메서드를 받은 원 서버는 **501(Not Implemented)** 로 답해야 한다
    (SHOULD).
  - 알아보고 구현했으나 그 대상 자원에는 허용되지 않은 메서드를 받은 원 서버는 **405(Method Not
    Allowed)** 로 답해야 한다 (SHOULD).
- 이 명세 밖의 추가 메서드가 이미 여럿 규정되어 있다. 그런 메서드는 전부 **"Hypertext Transfer
  Protocol (HTTP) Method Registry"에 등록되어야 한다** (§9.1).[^fielding2022-rfc9110] 등록 절차와
  새 메서드를 만들 때의 고려 사항은 이 문서의 확장 절(§16.1)이 따로 다루고, 그 내용은
  [HTTP의 확장점과 레지스트리](../concepts/http-extension-points-and-registries.md)에 있다 —
  새 메서드는 파싱 알고리즘을 바꿀 수 없고 콘텐츠를 금지할 수 없다는 제약이 거기 있다.

## 이어지는 페이지

- [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)
  — 이 여덟에 공통으로 걸리는 세 속성의 정의
- [GET과 HEAD](../concepts/http-get-and-head.md) — 필수인 두 메서드
- [POST와 PUT](../concepts/http-post-and-put.md) — 요청 콘텐츠의 뜻이 갈리는 두 메서드
- [DELETE와 CONNECT와 OPTIONS와 TRACE](../concepts/http-delete-connect-options-and-trace.md) —
  나머지 넷
- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — Allow가 이 목록을 실어 나르는
  자리
- [자원과 표현](../concepts/http-resources-and-representations.md) — 메서드가 적용되는 대상의 정의
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 균일 인터페이스를 설계 원칙으로 삼는 쪽
- [HTTP의 확장점과 레지스트리](../concepts/http-extension-points-and-registries.md) — 새 메서드를
  등록할 때의 절차와 제약
- [클라이언트 오류 4xx](../concepts/http-client-error-status-codes.md) — 막힌 메서드에 붙는 405
- [서버 오류 5xx와 과부하 신호](../concepts/http-server-error-status-codes.md) — 모르는 메서드에
  붙는 501

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록과 ABNF 규칙은
    rfc-editor 정본의 원문 그대로다. 표준 메서드 표는 §9.1의 Table 4를 한국어로 옮긴 것이다.

---
type: concept
title: DELETE와 CONNECT와 OPTIONS와 TRACE
description: 나머지 네 메서드의 의미론 — DELETE가 저장된 정보의 삭제가 아니라 URI 매핑의 연결 해제를 뜻한다는 규정과 성공 시 세 상태 코드의 갈림, CONNECT가 터널을 만들며 쓰는 host와 port만의 특수 요청 대상과 임의 포트로의 터널이 만드는 위험, OPTIONS가 별표 요청 대상으로 서버 자체를 겨냥하는 자리와 Max-Forwards로 사슬의 특정 수신자를 지목하는 방식, 그리고 TRACE가 요청을 되비추게 하면서 민감한 필드에 거는 금지
generated: { by: "claude-opus-5", at: "2026-09-07T15:25:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# DELETE와 CONNECT와 OPTIONS와 TRACE

- [버전 조건](#버전-조건)
- [DELETE가 지우는 것](#delete가-지우는-것)
- [DELETE의 응답과 제약](#delete의-응답과-제약)
- [CONNECT가 만드는 터널](#connect가-만드는-터널)
- [CONNECT의 위험과 제약](#connect의-위험과-제약)
- [OPTIONS와 별표 요청 대상](#options와-별표-요청-대상)
- [TRACE가 되비추는 것](#trace가-되비추는-것)
- [RFC 9110에서 바뀐 것](#rfc-9110에서-바뀐-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **가져오지도 보내지도 않는 네 메서드는 각각 무엇을 요청하는 것인가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## DELETE가 지우는 것

- 정의가 삭제라는 낱말의 통념을 비껴간다 (§9.3.5).[^fielding2022-rfc9110]

  > The DELETE method requests that the origin server remove the association between the
  > target resource and its current functionality.

  DELETE는 원 서버가 **대상 자원과 그 현재 기능 사이의 연관을 제거하도록** 요청한다. 데이터를
  지우라는 것이 아니라 그 URI가 무언가를 가리키기를 그만두라는 것이다.
- 원전이 비유를 붙인다. 유닉스의 `rm` 명령과 비슷하며, **앞서 연관되어 있던 정보가 삭제되리라는
  기대가 아니라 원 서버의 URI 매핑에 대한 삭제 연산을 표현한다**
  (§9.3.5).[^fielding2022-rfc9110]
- 그래서 표현과 저장 공간의 운명이 열려 있다. 대상 자원에 현재 표현이 있으면 **원 서버가 그것을
  파괴할 수도 아닐 수도 있고, 연관된 저장 공간이 회수될 수도 아닐 수도 있다.** 전적으로 자원의 성질과
  원 서버의 구현에 달렸으며 그것은 이 명세의 범위 밖이다 (§9.3.5).[^fielding2022-rfc9110]
- 자원의 다른 구현 측면도 마찬가지다. 데이터베이스나 게이트웨이 연결처럼 DELETE의 결과로 비활성화되거나
  보관되어야 하는 것이 있을 수 있다. 일반적으로 원 서버는 **삭제를 달성할 규정된 기제를 가진 자원에
  대해서만 DELETE를 허용할 것으로 가정된다** (§9.3.5).[^fielding2022-rfc9110]
- 실제로 이 메서드를 허용하는 자원은 드물다. **주된 쓰임은 원격 저작 환경**이며, 거기서는 사용자가 그
  효과에 대해 어느 정도 방향을 갖는다 (§9.3.5).[^fielding2022-rfc9110] 원전이 드는 예가 PUT으로
  만들어졌거나 POST에 대한 201 응답의 `Location`으로 식별된 자원이 그 행위를 되돌리는 DELETE를
  허용하는 경우다.

## DELETE의 응답과 제약

- 성공했을 때 보낼 상태 코드가 셋으로 갈린다(SHOULD) (§9.3.5).[^fielding2022-rfc9110]

  | 상태 코드 | 언제 |
  |---|---|
  | 202(Accepted) | 행위가 성공할 것 같지만 아직 시행되지 않았을 때 |
  | 204(No Content) | 행위가 시행되었고 더 줄 정보가 없을 때 |
  | 200(OK) | 행위가 시행되었고 응답 메시지가 그 상태를 서술하는 표현을 담을 때 |

- 요청 콘텐츠에는 GET·HEAD와 같은 제약이 걸린다. **일반적으로 정의된 의미론이 없고, 요청의 뜻이나
  대상을 바꿀 수 없으며, 요청 밀반입 공격의 잠재력 때문에 어떤 구현은 요청을 거절하고 연결을 닫을 수
  있다** (§9.3.5).[^fielding2022-rfc9110] 클라이언트가 DELETE 요청에 콘텐츠를 생성해서는 안 된다는
  요건(SHOULD NOT)도 같은 문면이다.
- DELETE 응답은 **캐시 가능하지 않다.** 성공한 DELETE가 대상 URI에 대해 저장된 응답을 가진 캐시를
  지나가면 **그 저장된 응답들은 무효화된다** (§9.3.5).[^fielding2022-rfc9110] 무효화의 규범은
  RFC 9111 영역이다.

## CONNECT가 만드는 터널

- 정의 문장이다 (§9.3.6).[^fielding2022-rfc9110]

  > The CONNECT method requests that the recipient establish a tunnel to the destination
  > origin server identified by the request target and, if successful, thereafter restrict its
  > behavior to blind forwarding of data, in both directions, until the tunnel is closed.

  수신자가 요청 대상이 식별하는 목적지 원 서버로 가는 터널을 만들고, 성공하면 그 뒤로는 **터널이
  닫힐 때까지 양방향으로 데이터를 맹목적으로 전달하는 것으로 자기 행동을 제한하도록** 요청한다.
- 쓰임이 명시되어 있다. 터널은 흔히 **프록시 하나 이상을 관통하는 종단 간 가상 연결을 만드는 데**
  쓰이며, 그 연결은 TLS로 보안될 수 있다 (§9.3.6).[^fielding2022-rfc9110]
- 요청 대상의 형태가 이 메서드에만 있는 특수 형태다. **터널 목적지의 호스트와 포트 번호만을 콜론으로
  구분해 적는다.** 기본 포트가 없으므로, 포트가 생략된 authority 컴포넌트를 가진 URI 참조에 근거한
  CONNECT라도 **클라이언트는 포트 번호를 보내야 한다**(MUST) (§9.3.6).[^fielding2022-rfc9110]
  원전이 든 예가 이 형태를 보여 준다 (§9.3.6):[^fielding2022-rfc9110]

  ```http
  CONNECT server.example.com:80 HTTP/1.1
  Host: server.example.com
  ```

- 서버는 **비었거나 유효하지 않은 포트 번호를 겨냥한 CONNECT 요청을 거절해야 한다**(MUST). 보통
  400(Bad Request)으로 응답한다 (§9.3.6).[^fielding2022-rfc9110]
- 대상이 정해져 있다. **CONNECT는 프록시로 가는 요청에 쓰이도록 의도된 것**이다. 수신자는 요청
  대상이 식별하는 서버에 직접 연결하거나, 다른 프록시를 쓰도록 설정되어 있으면 CONNECT 요청을 다음
  인바운드 프록시로 전달해 터널을 만들 수 있다. **원 서버가 CONNECT를 받아들여도 되지만(MAY) 대부분의
  원 서버는 CONNECT를 구현하지 않는다** (§9.3.6).[^fielding2022-rfc9110]

## CONNECT의 위험과 제약

- 전환 시점이 정해져 있다. **어떤 2xx(Successful) 응답이든 송신자와 모든 인바운드 프록시가 응답 헤더
  섹션 직후 즉시 터널 모드로 전환할 것임을 나타낸다.** 그 헤더 섹션 뒤에 받은 데이터는 요청 대상이
  식별하는 서버에서 온 것이다. 성공 응답이 아닌 응답은 터널이 아직 만들어지지 않았음을 나타낸다
  (§9.3.6).[^fielding2022-rfc9110]
- 닫을 때의 절차도 요건이다. 터널 중개자는 어느 한쪽이 연결을 닫은 것을 감지하면 **닫힌 쪽에서 온
  미처리 데이터를 다른 쪽으로 보내려 시도하고, 두 연결을 다 닫은 뒤, 전달되지 않고 남은 데이터를
  버려야 한다**(MUST) (§9.3.6).[^fielding2022-rfc9110]
- 위험이 명시되어 있다. **임의의 서버로 터널을 만드는 데는 상당한 위험이 있고, 특히 목적지가 웹
  트래픽용이 아닌 잘 알려진 예약 TCP 포트일 때 그렇다.** 원전이 든 예가 SMTP 예약 포트로 가는
  CONNECT인데, 허용되면 프록시를 속여 스팸 메일을 중계하게 만들 수 있다
  (§9.3.6).[^fielding2022-rfc9110]
- 그래서 완화책이 규범이 된다. CONNECT를 지원하는 프록시는 **그 쓰임을 알려진 포트의 제한된 집합이나
  설정 가능한 안전한 요청 대상 목록으로 제한해야 한다**(SHOULD)
  (§9.3.6).[^fielding2022-rfc9110]
- 프레이밍 필드에 금지가 걸린다. 서버는 CONNECT에 대한 2xx 응답에 **`Transfer-Encoding`이나
  `Content-Length` 헤더 필드를 보내서는 안 되고**(MUST NOT), 클라이언트는 성공 응답에서 받은 그
  필드들을 **무시해야 한다**(MUST) (§9.3.6).[^fielding2022-rfc9110]
- CONNECT 요청 메시지는 **콘텐츠를 갖지 않는다.** CONNECT 응답은 캐시 가능하지 않다
  (§9.3.6).[^fielding2022-rfc9110]
  - 버전 조건: CONNECT는 HTTP 연결의 요청/응답 성격을 바꾸므로 **특정 HTTP 버전마다 그 의미론을
    프로토콜의 전송 형식으로 옮기는 방식이 다를 수 있다.** CONNECT 요청 메시지의 헤더 섹션 뒤에
    보내진 데이터의 해석도 쓰이는 HTTP 버전에 특정된다.

## OPTIONS와 별표 요청 대상

- 정의 문장이다 (§9.3.7).[^fielding2022-rfc9110]

  > The OPTIONS method requests information about the communication options available for the
  > target resource, at either the origin server or an intervening intermediary.

  OPTIONS는 대상 자원에 대해 가용한 통신 옵션의 정보를 요청한다. **원 서버에서든 중간에 낀
  중개자에서든** 그렇다.
- 이 메서드의 자리가 무엇인지도 적혀 있다. 클라이언트가 **자원 행위를 함의하지 않고** 자원과 연관된
  옵션이나 요건, 또는 서버의 능력을 알아낼 수 있게 한다 (§9.3.7).[^fielding2022-rfc9110]
- 요청 대상이 별표(`*`)인 OPTIONS 요청은 **특정 자원이 아니라 서버 일반에 적용된다.** 서버의 통신
  옵션은 대개 자원에 달렸으므로, 이 요청은 **"핑"이나 "무연산" 류의 메서드로만 쓸모가 있다.**
  클라이언트가 서버의 능력을 시험하게 해 줄 뿐이며, 예컨대 프록시의 HTTP/1.1 준수 여부를 시험하는 데
  쓸 수 있다 (§9.3.7).[^fielding2022-rfc9110] 요청 대상이 별표가 아니면 대상 자원과 통신할 때
  가용한 옵션에 적용된다.
- 서버 쪽 요건이다. 성공 응답을 만드는 서버는 **서버가 구현했고 대상 자원에 적용되는 선택적 기능을
  나타낼 수 있는 헤더를 보내야 한다**(SHOULD). `Allow`가 예이고 이 명세가 정의하지 않은 잠재적
  확장도 포함된다 (§9.3.7).[^fielding2022-rfc9110]
- 응답 콘텐츠의 형식은 열려 있다. 통신 옵션을 기계나 사람이 읽을 수 있는 표현으로 서술할 수도 있으나
  **그런 표현의 표준 형식은 이 명세가 정의하지 않는다.** 앞으로의 HTTP 확장이 정의할 수는 있다
  (§9.3.7).[^fielding2022-rfc9110]
- 사슬의 특정 수신자를 지목하는 수단이 있다. 클라이언트는 OPTIONS 요청에 `Max-Forwards` 헤더 필드를
  보내 **요청 사슬의 특정 수신자를 겨냥해도 된다**(MAY). 프록시는 요청을 전달하면서 `Max-Forwards`를
  생성해서는 안 되며(MUST NOT), 예외는 그 요청을 `Max-Forwards`와 함께 받은 경우다
  (§9.3.7).[^fielding2022-rfc9110]
- 콘텐츠를 담은 OPTIONS 요청을 만드는 클라이언트는 **그 표현 미디어 타입을 서술하는 유효한
  `Content-Type` 헤더 필드를 보내야 한다**(MUST). 다만 원전이 곧바로 덧붙인다 — **이 명세는 그런
  콘텐츠의 쓰임을 정의하지 않는다** (§9.3.7).[^fielding2022-rfc9110] OPTIONS 응답은 캐시 가능하지
  않다.

## TRACE가 되비추는 것

- 정의 문장이다 (§9.3.8).[^fielding2022-rfc9110]

  > The TRACE method requests a remote, application-level loop-back of the request message.

  TRACE는 요청 메시지의 **원격 애플리케이션 수준 루프백**을 요청한다.
- 최종 수신자는 아래 서술되는 일부 필드를 빼고 **받은 메시지를 200(OK) 응답의 콘텐츠로 클라이언트에게
  되비춰야 한다**(SHOULD). `message/http` 형식이 그렇게 하는 한 방법이다
  (§9.3.8).[^fielding2022-rfc9110]
- 최종 수신자가 누구인지가 정의되어 있다. **원 서버이거나, 요청에서 `Max-Forwards` 값 0을 받은 첫
  서버**다 (§9.3.8).[^fielding2022-rfc9110]
- 민감한 데이터에 금지가 걸린다. 클라이언트는 **응답으로 노출될 수 있는 민감한 데이터를 담은 필드를
  TRACE 요청에 생성해서는 안 된다**(MUST NOT). 원전이 드는 예가 저장된 사용자 자격 증명이나 쿠키를
  TRACE 요청에 보내는 것이고, 그것을 어리석은 일이라고 적는다
  (§9.3.8).[^fielding2022-rfc9110]
- 수신자 쪽에도 요건이 걸린다. 최종 수신자는 응답 콘텐츠를 만들 때 **민감한 데이터를 담고 있을 법한
  요청 필드를 제외해야 한다**(SHOULD) (§9.3.8).[^fielding2022-rfc9110]
- 쓰임이 진단이다. TRACE는 클라이언트가 **요청 사슬의 반대편 끝에서 무엇이 수신되고 있는지 보고**
  그 데이터를 시험이나 진단 정보로 쓰게 해 준다. `Via` 헤더 필드의 값이 특히 관심 대상인데, 요청
  사슬의 자취 노릇을 하기 때문이다 (§9.3.8).[^fielding2022-rfc9110]
- `Max-Forwards`가 함께 쓰인다. 이 필드로 클라이언트가 **요청 사슬의 길이를 제한할 수 있고**, 그것이
  메시지를 무한 루프로 전달하는 프록시 사슬을 시험하는 데 쓸모가 있다
  (§9.3.8).[^fielding2022-rfc9110]
- 클라이언트는 TRACE 요청에 **콘텐츠를 보내서는 안 된다**(MUST NOT). TRACE 응답은 캐시 가능하지 않다
  (§9.3.8).[^fielding2022-rfc9110] 위의 GET·HEAD·DELETE가 SHOULD NOT인 것과 달리 여기는 MUST NOT다.

## RFC 9110에서 바뀐 것

- **GET과 HEAD와 DELETE의 요청 본문이 상호운용되지 않는다는 사실이 명확해졌다**
  (부록 B.3, §9.3.5).[^fielding2022-rfc9110]
  - 버전 조건: RFC 7231 이하와 비교한 변경이다.
- **OPTIONS 서술에서 `Content-Length` 설정에 대한 불필요한 요건이 제거되었다**
  (부록 B.3, §9.3.7).[^fielding2022-rfc9110]
- **TRACE 응답에 `message/http` 미디어 타입을 쓰라는 규범 요건이 제거되었다**
  (부록 B.3, §9.3.8).[^fielding2022-rfc9110]

## 이어지는 페이지

- [HTTP 요청 메서드의 지위](../concepts/http-request-methods-overview.md) — 이 넷이 놓인 표준 메서드
  여덟의 목록
- [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)
  — DELETE가 멱등이고 OPTIONS와 TRACE가 안전한 자리
- [요청 대상과 Host](../concepts/http-target-uri-and-host.md) — CONNECT와 OPTIONS의 특수 요청 대상이
  라우팅에서 처리되는 자리
- [HTTP 메시지 전달과 hop-by-hop 필드](../concepts/http-message-forwarding-and-hop-by-hop-fields.md)
  — Max-Forwards와 Via의 정의
- [HTTP 중개자](../concepts/http-intermediaries.md) — 터널의 정의와 프록시와의 구분
- [HTTP 콘텐츠의 의미론과 식별](../concepts/http-content-semantics.md) — CONNECT의 2xx 응답에
  콘텐츠가 없다는 규칙이 다시 나오는 자리
- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — OPTIONS 응답이 보내는 Allow
- [정보 응답 1xx와 성공 2xx](../concepts/http-informational-and-successful-status-codes.md) —
  DELETE와 OPTIONS의 성공에 붙는 200과 202와 204의 정의

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록과 예제 요청은
    rfc-editor 정본의 원문 그대로다. DELETE의 상태 코드 표는 §9.3.5의 세 불릿을 옮긴 것이다.

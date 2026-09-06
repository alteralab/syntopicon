---
type: concept
title: HTTP 클라이언트와 서버와 무상태성
description: HTTP 통신의 참여자와 메시지를 정의하는 원전의 어휘 — 클라이언트와 서버가 프로그램의 종류가 아니라 연결마다의 역할이라는 것, 무상태(stateless)가 "각 요청의 의미론이 고립되어 이해된다"는 뜻이고 그래서 서버가 같은 연결의 두 요청을 같은 사용자 에이전트의 것으로 가정해서는 안 된다는 요건, 요청과 응답 메시지에 무엇이 실리는가, 사용자 에이전트와 원 서버가 브라우저와 대형 웹사이트보다 훨씬 넓다는 것, 그리고 GET 한 번의 실제 교환
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T09:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 클라이언트와 서버와 무상태성

- [버전 조건](#버전-조건)
- [연결과 클라이언트와 서버](#연결과-클라이언트와-서버)
- [무상태의 정확한 뜻](#무상태의-정확한-뜻)
- [같은 연결이 같은 사용자를 뜻하지 않는다](#같은-연결이-같은-사용자를-뜻하지-않는다)
- [요청 메시지와 응답 메시지](#요청-메시지와-응답-메시지)
- [사용자 에이전트](#사용자-에이전트)
- [원 서버](#원-서버)
- [메시지 교환의 실물](#메시지-교환의-실물)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP 통신의 참여자는 무엇으로 정의되고, HTTP가 무상태라는 말은 정확히 무엇을
주장하는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 연결과 클라이언트와 서버

- HTTP는 신뢰성 있는 전송 계층 또는 세션 계층의 연결(connection) 위에서 도는 클라이언트/서버
  프로토콜이다 (§3.3).[^fielding2022-rfc9110]
- 클라이언트(client)는 HTTP 요청 하나 이상을 보낼 목적으로 서버에 연결을 세우는 프로그램이고,
  서버(server)는 HTTP 응답을 보내 HTTP 요청을 처리하려고 연결을 받아들이는 프로그램이다
  (§3.3).[^fielding2022-rfc9110]
- **이 둘은 프로그램의 종류가 아니라 역할이다.** 클라이언트와 서버라는 낱말은 그 프로그램이
  특정 연결에서 수행하는 역할만 가리키며, **같은 프로그램이 어떤 연결에서는 클라이언트로 다른
  연결에서는 서버로 행동할 수 있다** (§3.3).[^fielding2022-rfc9110]

## 무상태의 정확한 뜻

- 무상태의 정의 문장이다 (§3.3).[^fielding2022-rfc9110]

  > HTTP is defined as a stateless protocol, meaning that each request message's semantics
  > can be understood in isolation, and that the relationship between connections and
  > messages on them has no impact on the interpretation of those messages.

  주장이 둘이다. 각 요청 메시지의 의미론이 고립되어 이해된다는 것, 그리고 연결과 그 위의
  메시지 사이의 관계가 그 메시지의 해석에 아무 영향도 주지 않는다는 것. 무상태(stateless)는
  "서버가 아무것도 기억하지 않는다"가 아니라 **메시지 해석이 연결 이력에 기대지 않는다**는
  진술이다.
- 그 귀결의 예로 원전이 드는 것이 CONNECT 요청과 Upgrade 헤더 필드가 붙은 요청이다. 이런 것이
  연결의 첫 메시지에서만이 아니라 **아무 때나** 나타날 수 있다 (§3.3).[^fielding2022-rfc9110]
- 많은 구현이 HTTP의 이 무상태 설계에 의존해서 프록시된 연결을 재사용하거나 요청을 여러 서버에
  동적으로 부하 분산한다 (§3.3).[^fielding2022-rfc9110] 곧 무상태성은 미학이 아니라 중간 단계의
  자유를 떠받치는 전제다.

## 같은 연결이 같은 사용자를 뜻하지 않는다

- 이 절의 유일한 규범 문장이다 (§3.3).[^fielding2022-rfc9110]

  > As a result, a server MUST NOT assume that two requests on the same connection are from
  > the same user agent unless the connection is secured and specific to that agent.

  연결이 보안되어 있고 그 에이전트 전용일 때만 예외다.
- 이 요건을 어긴 비표준 확장이 실제로 있었고, 그 결과가 보안 문제와 상호운용성 문제였다
  (§3.3).[^fielding2022-rfc9110]

## 요청 메시지와 응답 메시지

- HTTP는 연결을 가로질러 메시지(message)를 교환하는 무상태 요청/응답 프로토콜이고, 보내는 쪽과
  받는 쪽을 각각 송신자(sender)와 수신자(recipient)라 부른다 (§3.4).[^fielding2022-rfc9110]
- 요청 메시지에 실리는 것 (§3.4):[^fielding2022-rfc9110]
  - 메서드와 요청 대상(request target). 이 둘이 필수다.
  - 요청 수정자와 클라이언트 정보와 표현 메타데이터를 담는 헤더 필드
  - 메서드에 따라 처리되도록 의도된 콘텐츠(content)
  - 콘텐츠를 보내는 동안 모은 정보를 전하는 트레일러 필드(trailer field)
- 응답 메시지에 실리는 것 (§3.4):[^fielding2022-rfc9110]
  - 상태 코드(status code). 응답 메시지마다 하나씩 들어간다.
  - 서버 정보와 자원 메타데이터와 표현 메타데이터를 담는 헤더 필드
  - 상태 코드에 따라 해석될 콘텐츠
  - 트레일러 필드
- 응답은 하나가 아닐 수 있다. 서버는 **응답 메시지 하나 이상**을 보내 요청에 답한다
  (§3.4).[^fielding2022-rfc9110]

## 사용자 에이전트

- 사용자 에이전트(user agent)는 요청을 개시하는 여러 클라이언트 프로그램 아무것이나 가리킨다
  (§3.5).[^fielding2022-rfc9110]
- 가장 익숙한 형태가 범용 웹 브라우저지만 **그것은 구현의 작은 비율일 뿐이다.** 원전이 나열하는
  나머지가 스파이더(웹을 훑는 로봇), 명령줄 도구, 전광판, 가전, 저울, 전구, 펌웨어 갱신 스크립트,
  모바일 앱, 그리고 온갖 모양과 크기의 통신 장치다 (§3.5).[^fielding2022-rfc9110]
- 사용자 에이전트라는 것이 **요청 시점에 사람이 그 소프트웨어와 직접 상호작용하고 있음을 함의하지
  않는다.** 많은 경우 배경에서 돌도록 설치되거나 설정되어 결과를 나중에 검사하도록 저장한다
  (§3.5).[^fielding2022-rfc9110]
- 그래서 이 명세가 "사용자에게 오류를 보고하라"고 요구하는 소수의 자리에서도 그 보고가 오류
  콘솔이나 로그 파일에서만 관측 가능해도 받아들여진다. 마찬가지로 "자동 동작을 사용자가 확인한
  뒤 진행하라"는 요건도 사전 설정 선택이나 실행 시 옵션이나 그냥 그 안전하지 않은 동작을 피하는
  것으로 충족될 수 있다 (§3.5).[^fielding2022-rfc9110]

## 원 서버

- 원 서버(origin server)는 주어진 대상 자원에 대해 **권위 있는 응답을 발원시킬 수 있는**
  프로그램을 가리킨다 (§3.6).[^fielding2022-rfc9110]
- 사용자 에이전트와 브라우저를 동일시하는 것과 같은 오해가 여기에도 있다. 가장 익숙한 형태가
  큰 공개 웹사이트지만, 흔한 원 서버에는 가정 자동화 장치, 설정 가능한 네트워크 부품, 사무기기,
  자율 로봇, 뉴스 피드, 교통 카메라, 실시간 광고 선택기, 주문형 비디오 플랫폼도 든다
  (§3.6).[^fielding2022-rfc9110]
- 대부분의 HTTP 통신은 URI로 식별되는 어떤 자원의 표현을 요구하는 검색 요청(GET)으로 이뤄지며,
  가장 단순한 경우 이것이 사용자 에이전트와 원 서버 사이의 양방향 연결 하나로 이뤄진다
  (§3.6).[^fielding2022-rfc9110]

## 메시지 교환의 실물

- 원전이 드는 HTTP/1.1 GET 교환이다. 대상 URI는 `http://www.example.com/hello.txt`이고, 위
  절들의 어휘가 어디에 앉는지를 보여 준다 — 요청의 메서드와 헤더 필드, 응답의 상태 코드와
  자원 메타데이터(`Last-Modified`·`ETag`)와 표현 메타데이터(`Content-Type`)
  (§3.9).[^fielding2022-rfc9110]

  ```http
  GET /hello.txt HTTP/1.1
  User-Agent: curl/7.64.1
  Host: www.example.com
  Accept-Language: en, mi

  HTTP/1.1 200 OK
  Date: Mon, 27 Jul 2009 12:28:53 GMT
  Server: Apache
  Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
  ETag: "34aa387-d-1568eb00"
  Accept-Ranges: bytes
  Content-Length: 51
  Vary: Accept-Encoding
  Content-Type: text/plain

  Hello World! My content includes a trailing CRLF.
  ```

## 이어지는 페이지

- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — 무상태라는 낱말이
  정의 문장에 놓인 자리
- [자원과 표현](../concepts/http-resources-and-representations.md) — 이 메시지가 실어 나르는 것
- [HTTP 중개자](../concepts/http-intermediaries.md) — 이 양 끝 사이에 들어오는 것들
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 여기 나온
  역할 이름들에 요건이 걸리는 방식
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 무상태성을 설계 원칙으로 삼는 쪽

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록과 예제 교환은
    rfc-editor 정본의 원문 그대로이고, 예제는 §3.9의 요청 블록과 응답 블록을 한 펜스에 이어
    붙인 것이다(원문은 "Client request:"와 "Server response:" 두 블록으로 나뉘어 있다).

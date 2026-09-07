---
type: concept
title: HTTP의 정의와 문서의 범위
description: HTTP를 무상태 요청/응답 프로토콜 "가족"으로 정의하는 원전의 문장과, 그 정의에서 따라 나오는 제약 — 균일 인터페이스가 구현 세부를 감추므로 인터페이스 뒤에서 일어나는 일은 규정할 수 없고 수신자의 기대 동작만 규정된다는 것, 세 major 버전이 같은 의미론을 공유한다는 것, 그리고 의미론(RFC 9110)과 캐싱(9111)과 HTTP/1.1 메시징 구문(9112)이 갈라선 이유와 이 문서가 폐기한 명세 목록
generated: { by: "claude-opus-5", at: "2026-09-07T09:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP의 정의와 문서의 범위

- [버전 조건](#버전-조건)
- [HTTP란 무엇인가](#http란-무엇인가)
- [균일 인터페이스가 감추는 것](#균일-인터페이스가-감추는-것)
- [인터페이스 뒤를 규정할 수 없다는 귀결](#인터페이스-뒤를-규정할-수-없다는-귀결)
- [세 major 버전이 공유하는 것](#세-major-버전이-공유하는-것)
- [핵심 의미론이 담는 것](#핵심-의미론이-담는-것)
- [의미론과 캐싱과 메시징 구문의 분업](#의미론과-캐싱과-메시징-구문의-분업)
- [이 문서가 폐기한 명세](#이-문서가-폐기한-명세)
- [RFC 9110에서 바뀐 것](#rfc-9110에서-바뀐-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP는 무엇으로 정의되며, 그 정의를 담은 RFC 9110은 무엇을 규정하고 무엇을
다른 문서에 넘기는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## HTTP란 무엇인가

- 원전의 정의 문장이다 (§1.1).[^fielding2022-rfc9110]

  > The Hypertext Transfer Protocol (HTTP) is a family of stateless, application-level,
  > request/response protocols that share a generic interface, extensible semantics, and
  > self-descriptive messages to enable flexible interaction with network-based hypertext
  > information systems.

  낱말 하나하나가 조건이다. **가족(family)** — 단수의 프로토콜이 아니라 여럿이다.
  **무상태(stateless)** — 요청 하나의 뜻이 그 요청만으로 이해된다. **애플리케이션
  계층(application-level)** — 전송 계층 위에 있다. **요청/응답(request/response)** —
  주고받는 짝이 단위다. 그 여럿이 공유하는 것이 셋으로 명시된다. 일반 인터페이스(generic
  interface), 확장 가능한 의미론(extensible semantics), 자기 서술적 메시지(self-descriptive
  messages).
- HTTP는 중개 프로토콜(intermediation protocol)로 쓰이도록 설계되기도 했다. 프록시(proxy)와
  게이트웨이(gateway)가 HTTP가 아닌 정보 시스템을 더 일반적인 인터페이스로 옮겨 놓을 수 있다
  (§1.1).[^fielding2022-rfc9110]
- 1990년 월드 와이드 웹의 정보 전송 프로토콜로 출발했다. 처음에는 지연이 낮은 요청을 위한
  사소한 기제였고 메서드가 GET 하나뿐이었으며, 주어진 경로명으로 식별되는 하이퍼텍스트 문서의
  전송을 요청하는 것이 전부였다. 웹이 자라면서 요청과 응답을 메시지로 감싸고, MIME 비슷한
  미디어 타입으로 임의의 데이터 형식을 나르고, 중개자를 거쳐 요청을 라우팅하는 확장이 붙었다
  (§1.2).[^fielding2022-rfc9110]

## 균일 인터페이스가 감추는 것

- 서비스가 어떻게 구현됐는지의 세부를 HTTP가 감춘다. 제공되는 자원(resource)의 종류와 무관한
  균일한 인터페이스를 클라이언트에게 내놓기 때문이다 (§1.1).[^fielding2022-rfc9110]
- 감춤은 반대 방향으로도 걸린다. 서버는 각 클라이언트의 목적을 알 필요가 없다. **요청은 특정
  종류의 클라이언트나 미리 정해진 애플리케이션 단계의 순서에 결부되는 대신 고립된 것으로
  다뤄질 수 있다** (§1.1).[^fielding2022-rfc9110]
- 그 대가로 얻는 것이 셋이다 — 범용 구현을 여러 다른 맥락에서 효과적으로 쓸 수 있게 하고,
  상호작용 복잡도를 줄이고, 시간에 걸친 독립적 진화를 가능하게 한다 (§1.1).[^fielding2022-rfc9110]

## 인터페이스 뒤를 규정할 수 없다는 귀결

- 이 유연성의 귀결 하나가 명세의 형태를 정한다. **인터페이스 뒤에서 무엇이 일어나는가로는
  프로토콜을 정의할 수 없다.** 그래서 정의할 수 있는 것이 셋으로 한정된다 — 통신의 구문,
  받은 통신의 의도(intent), 수신자의 기대 동작(expected behavior of recipients)
  (§1.1).[^fielding2022-rfc9110]
- 이 한정에는 또 한 겹이 있다. 통신을 고립시켜 놓고 보면 성공한 동작은 서버가 제공하는 관측
  가능한 인터페이스의 대응하는 변화로 반영되어야 마땅하다. 그러나 **여러 클라이언트가 병렬로,
  때로는 서로 어긋나는 목적으로 행동할 수 있으므로 그 변화가 응답 하나의 범위를 넘어 관측
  가능하기를 요구할 수는 없다** (§1.1).[^fielding2022-rfc9110]

## 세 major 버전이 공유하는 것

- HTTP/1.1은 기존의 텍스트 기반 메시징 구문과의 호환을 유지하면서 상호운용성과 확장성과
  견고함을 개선하려고 설계됐다. 여기에 들어간 것이 고정 길이와 동적(청크) 길이 양쪽의 데이터
  구분자, 일관된 콘텐츠 협상 틀, 조건부 요청을 위한 불투명 검증자(opaque validator), 캐시
  일관성을 위한 캐시 제어, 부분 갱신을 위한 범위 요청, 그리고 기본값이 된 지속
  연결이다 (§1.2).[^fielding2022-rfc9110]
- HTTP/2는 기존 TLS와 TCP 위에 다중화 세션 계층을 얹어 동시 HTTP 메시지를 효율적인 필드 압축과
  서버 푸시로 교환하게 했다. HTTP/3은 TCP 대신 UDP 위의 안전한 다중화 전송인 QUIC을 써서 동시
  메시지의 독립성을 더 높였다 (§1.2).[^fielding2022-rfc9110]
- 이 페이지가 존재하는 이유가 다음 문장이다 (§1.2).[^fielding2022-rfc9110]

  > All three major versions of HTTP rely on the semantics defined by this document.

  세 major 버전은 서로를 폐기하지 않았다. **각자가 쓰이는 맥락에 따라 고유한 이점과 한계를
  갖기 때문**이고, 구현은 자기 맥락에 가장 알맞은 전송과 메시징 구문을 고를 것으로 기대된다
  (§1.2).[^fielding2022-rfc9110]

## 핵심 의미론이 담는 것

- HTTP는 자원과 상호작용하는 균일한 인터페이스를 제공하는데, **자원의 타입도 성질도 구현도
  가리지 않고** 표현(representation)을 조작하거나 전송하는 메시지를 보냄으로써 그렇게 한다
  (§1.3).[^fielding2022-rfc9110]
- 메시지는 전부 요청 아니면 응답이다. 클라이언트가 자기 의도를 전하는 요청 메시지를 짜서
  식별된 원 서버(origin server) 쪽으로 라우팅하면, 서버는 요청을 듣고 받은 메시지를 파싱해
  식별된 대상 자원과의 관계에서 메시지 의미론을 해석하고 응답 메시지 하나 이상으로 답한다.
  클라이언트는 받은 응답을 살펴 자기 의도가 수행됐는지 보고, 상태 코드와 받은 콘텐츠를 근거로
  다음에 무엇을 할지 정한다 (§1.3).[^fielding2022-rfc9110]
- HTTP 의미론에 드는 것의 목록이다 (§1.3):[^fielding2022-rfc9110]
  - 각 요청 메서드가 정의하는 의도
  - 요청 헤더 필드로 서술될 수 있는, 그 의미론에 대한 확장
  - 응답을 서술하는 상태 코드
  - 응답 필드로 주어질 수 있는 그 밖의 제어 데이터와 자원 메타데이터
  - 콘텐츠가 수신자에게 어떻게 해석되도록 의도됐는지를 서술하는 표현 메타데이터
  - 콘텐츠 선택에 영향을 줄 수 있는 요청 헤더 필드와, 통틀어 콘텐츠 협상(content negotiation)이라
    불리는 여러 선택 알고리즘

## 의미론과 캐싱과 메시징 구문의 분업

- 이 개정이 한 일이 분업이다. **의미론의 정의(이 문서)와 캐싱을 현행 HTTP/1.1 메시징 구문에서
  갈라내어 각 major 프로토콜 버전이 같은 핵심 의미론을 참조하면서 독립적으로 나아갈 수 있게
  했다** (§1.2).[^fielding2022-rfc9110]
- 그래서 "HTTP/1.1"이라는 버전 표기가 가리키는 것은 한 문서가 아니라 문서 셋의 결합이다 —
  이 문서와 HTTP Caching과 HTTP/1.1 (§2.5).[^fielding2022-rfc9110]
- 이 분업의 실무적 귀결 하나는 **캐시 동작의 규범이 이 문서에 없다**는 것이다. 캐시가 무엇인지의
  정의는 여기 있으나 캐시 동작과 캐시 가능한 응답에 대한 HTTP 요건은 캐싱 명세가 정한다
  (§3.8).[^fielding2022-rfc9110] 자세한 자리는
  [HTTP 중개자](../concepts/http-intermediaries.md)에 있다.
- HTTP/1.1은 1995년에 도입되어 1997년에 표준 트랙으로 출판됐고(RFC 2068), 1999년에 개정됐고
  (RFC 2616), 2014년에 다시 개정됐다(RFC 7230부터 RFC 7235까지) (§1.2).[^fielding2022-rfc9110]

## 이 문서가 폐기한 명세

- 이 문서가 폐기하는 명세는 아홉 건이다 (§1.4):[^fielding2022-rfc9110]

  | 폐기된 RFC | 무엇이었나 |
  |---|---|
  | RFC 2818 | HTTP Over TLS |
  | RFC 7230 | HTTP/1.1 Message Syntax and Routing (일부만) |
  | RFC 7231 | HTTP/1.1 Semantics and Content |
  | RFC 7232 | HTTP/1.1 Conditional Requests |
  | RFC 7233 | HTTP/1.1 Range Requests |
  | RFC 7235 | HTTP/1.1 Authentication |
  | RFC 7538 | HTTP Status Code 308 (Permanent Redirect) |
  | RFC 7615 | HTTP Authentication-Info and Proxy-Authentication-Info Response Header Fields |
  | RFC 7694 | HTTP Client-Initiated Content-Encoding |

- RFC 7230만 예외가 붙는다. **이 문서는 RFC 7230 중 HTTP/1.1 메시징 구문과 연결 관리에
  독립적인 부분만 폐기하고, 나머지는 HTTP/1.1 명세가 폐기한다** (§1.4).[^fielding2022-rfc9110]
- RFC 7234(HTTP/1.1 Caching)가 이 표에 없다는 점이 위 분업의 자취다. 그쪽은 캐싱 명세가 맡았다
  (§1.2, §1.4).[^fielding2022-rfc9110]

## RFC 9110에서 바뀐 것

- **설계 목표와 내력과 아키텍처와 준수 기준과 프로토콜 버전 관리와 URI와 메시지 라우팅과 헤더
  필드를 소개하는 절들이 이 문서로 옮겨 왔다** (부록 B.2).[^fielding2022-rfc9110] 그전에는 그것들이
  HTTP/1.1 메시지 구문 명세(RFC 7230)에 있었다.
  - 버전 조건: RFC 7230 이하와 비교한 문서 구성의 변경이다.
- 이전 RFC들과 비교한 조문 변경 목록은 부록 B가 갖고 있고, 이 KB에서는 해당 조문을 담은 페이지마다
  "RFC 9110에서 바뀐 것" 절로 나뉘어 있다.

## 이어지는 페이지

- [자원과 표현](../concepts/http-resources-and-representations.md) — 균일 인터페이스가 무엇을
  주고받는가
- [HTTP 클라이언트와 서버와 무상태성](../concepts/http-clients-servers-and-statelessness.md) —
  이 정의의 참여자들과 무상태가 정확히 뜻하는 것
- [HTTP 중개자](../concepts/http-intermediaries.md) — 중개 프로토콜이라는 설계 목표의 실물
- [HTTP 버전 번호와 의미론의 분리](../concepts/http-version-numbering.md) — 버전이 올라도 무엇은
  바뀌지 않는가
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 이 문서의
  요건이 누구에게 걸리는가
- [http와 https URI 스킴과 정규화](../concepts/http-uri-schemes-and-normalization.md) — 자원을
  가리키는 식별자 쪽
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 이 프로토콜 위에 얹힌 서비스 설계
  철학 쪽

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다.

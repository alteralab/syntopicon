---
type: concept
title: HTTP 상태 코드의 다섯 클래스와 확장 규칙
description: 세 자리 정수 하나가 응답의 결과와 의미론을 서술한다는 규정과 그 첫 자리가 정하는 다섯 클래스, 모르는 코드를 만난 클라이언트가 그 클래스의 x00으로 취급해야 한다는 요건, 범위 밖의 값과 내부용 코드의 처리, 잠정 응답 여럿 뒤에 최종 응답 하나가 온다는 구조, 이유 구절이 권고일 뿐이라는 것, 그리고 휴리스틱 캐시 가능성이 열거로 정해진다는 자리
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T21:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 상태 코드의 다섯 클래스와 확장 규칙

- [버전 조건](#버전-조건)
- [상태 코드가 서술하는 것](#상태-코드가-서술하는-것)
- [첫 자리가 정하는 다섯 클래스](#첫-자리가-정하는-다섯-클래스)
- [모르는 코드를 만났을 때](#모르는-코드를-만났을-때)
- [범위 밖의 값](#범위-밖의-값)
- [잠정 응답과 최종 응답](#잠정-응답과-최종-응답)
- [이유 구절은 권고일 뿐이다](#이유-구절은-권고일-뿐이다)
- [휴리스틱 캐시 가능성](#휴리스틱-캐시-가능성)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **응답의 결과를 세 자리 수 하나로 말하는 체계에서, 받은 쪽이 그 수를 모를 때
무슨 일이 일어나는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 상태 코드가 서술하는 것

- 정의 문장이다 (§15).[^fielding2022-rfc9110]

  > The status code of a response is a three-digit integer code that describes the result of
  > the request and the semantics of the response, including whether the request was
  > successful and what content is enclosed (if any).

  상태 코드(status code)는 **세 자리 정수**이고, 요청의 결과와 응답의 의미론을 서술한다.
  성공 여부와 콘텐츠가 실렸다면 그것이 무엇인지가 그 안에 든다.
- 유효한 상태 코드는 **100 이상 599 이하**다 (§15).[^fielding2022-rfc9110]
- 콘텐츠의 뜻을 정하는 셋 중 하나가 상태 코드다. 나머지 둘은 요청 메서드와 응답 콘텐츠 관련
  필드이고, 그 분업은 [HTTP 콘텐츠의 의미론과 식별](../concepts/http-content-semantics.md)에 있다.

## 첫 자리가 정하는 다섯 클래스

- **첫 자리가 응답의 클래스를 정하고, 뒤의 두 자리는 아무 분류 역할도 하지 않는다**
  (§15).[^fielding2022-rfc9110] 곧 404와 405의 관계는 400과 404의 관계보다 가깝지 않다.
- 첫 자리에 올 수 있는 값은 다섯이다 (§15).[^fielding2022-rfc9110]

  | 클래스 | 이름 | 뜻 | 절 |
  |---|---|---|---|
  | 1xx | Informational | 요청을 받았고 처리를 계속하는 중이다 | §15.2 |
  | 2xx | Successful | 요청을 성공적으로 받아 이해했고 받아들였다 | §15.3 |
  | 3xx | Redirection | 요청을 마치려면 추가 행동이 필요하다 | §15.4 |
  | 4xx | Client Error | 요청의 구문이 잘못되었거나 요청을 이행할 수 없다 | §15.5 |
  | 5xx | Server Error | 서버가 겉보기에 유효한 요청을 이행하지 못했다 | §15.6 |

## 모르는 코드를 만났을 때

- 상태 코드는 확장 가능하다. 그래서 **클라이언트가 등록된 모든 상태 코드의 뜻을 알아야 하는 것은
  아니다.** 다만 하나를 반드시 해야 한다 (§15).[^fielding2022-rfc9110]

  > However, a client MUST understand the class of any status code, as indicated by the first
  > digit, and treat an unrecognized status code as being equivalent to the x00 status code of
  > that class.

  클라이언트는 **어떤 상태 코드든 첫 자리가 가리키는 클래스는 이해해야 하고(MUST), 알아보지 못한
  코드는 그 클래스의 x00 코드와 같은 것으로 취급해야 한다.**
- 원전이 드는 예가 471이다. 알아보지 못했더라도 첫 자리에서 자기 요청에 문제가 있었음을 읽고
  400(Bad Request)을 받은 것처럼 처리하면 된다 (§15).[^fielding2022-rfc9110] 대개 응답에는 상태를
  설명하는 표현이 함께 온다.
- 이 규칙이 [새 상태 코드를 등록하는 절차](../concepts/http-extension-points-and-registries.md)의
  전제다. 새 코드가 반드시 다섯 클래스 중 하나에 들어야 하는 이유가 여기 있다 — 모르는 수신자도
  클래스만으로는 옳게 처리하기 때문이다.

## 범위 밖의 값

- 100..599 **밖의 값은 무효다** (§15).[^fielding2022-rfc9110] 다만 구현들이 600..999를 라이브러리
  오류 같은 HTTP 아닌 상태를 내부에서 주고받는 데 쓰는 일이 흔하다고 원전이 적는다.
- 무효한 상태 코드를 받은 클라이언트는 **5xx(Server Error)를 받은 것처럼 처리해야 한다**(SHOULD)
  (§15).[^fielding2022-rfc9110]

## 잠정 응답과 최종 응답

- 요청 하나에 응답이 여럿 딸릴 수 있다. 구조가 정해져 있다 — **1xx 범위의 "잠정"(interim, 최종이
  아닌) 응답이 0개 이상 오고, 그 뒤에 다른 범위의 "최종"(final) 응답이 정확히 하나 온다**
  (§15).[^fielding2022-rfc9110]
- 곧 1xx는 응답의 끝이 아니다. 그 처리 규칙은
  [정보 응답 1xx와 성공 2xx](../concepts/http-informational-and-successful-status-codes.md)에 있다.

## 이유 구절은 권고일 뿐이다

- 이 명세가 각 코드 옆에 적는 이유 구절(reason phrase)은 **권고일 뿐이다. 지역 등가물로 바꾸거나
  아예 빼도 프로토콜에 영향이 없다** (§15.1).[^fielding2022-rfc9110] 곧 `404 Not Found`의
  `Not Found`는 규범이 아니다.

## 휴리스틱 캐시 가능성

- 어떤 상태 코드가 **휴리스틱하게 캐시 가능한지는 열거로 정해진다.** 이 명세에서는 200·203·204·
  206·300·301·308·404·405·410·414·501이 그렇고, **그 밖의 모든 상태 코드는 휴리스틱 캐시 가능이
  아니다** (§15.1).[^fielding2022-rfc9110] 메서드 정의나 명시적 캐시 제어가 달리 지시하면 그쪽이
  이긴다.
- 이 문서는 그 목록만 정하고 캐시가 실제로 무엇을 해도 되는지는 정하지 않는다. 재사용의 규범은
  캐싱 명세(RFC 9111)가 정본이다 (§15.1).[^fielding2022-rfc9110]
- 이 명세 밖에서 규정된 상태 코드들도 있다. 그런 코드는 전부 **"Hypertext Transfer Protocol (HTTP)
  Status Code Registry"에 등록되어야 한다**고 원전이 적는다 (§15.1).[^fielding2022-rfc9110]

## 이어지는 페이지

- [정보 응답 1xx와 성공 2xx](../concepts/http-informational-and-successful-status-codes.md) —
  잠정 응답과 성공을 알리는 코드들
- [리다이렉션 3xx와 메서드 보존](../concepts/http-redirection-status-codes.md) — 다른 URI로
  보내는 코드들과 그때 메서드가 바뀌는가
- [클라이언트 오류 4xx](../concepts/http-client-error-status-codes.md) — 요청 쪽에 문제가 있다고
  말하는 코드들
- [서버 오류 5xx와 과부하 신호](../concepts/http-server-error-status-codes.md) — 서버 쪽이
  이행하지 못했다고 말하는 코드들
- [HTTP의 확장점과 레지스트리](../concepts/http-extension-points-and-registries.md) — 새 상태
  코드를 등록하는 절차와 그 코드가 지켜야 할 것
- [HTTP 콘텐츠의 의미론과 식별](../concepts/http-content-semantics.md) — 실린 옥텟의 뜻을 상태
  코드가 함께 정한다는 자리
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 요건 낱말이
  역할에 걸리는 방식

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다. 다섯 클래스 표는 §15의 목록을 한국어로 옮긴 것이다.

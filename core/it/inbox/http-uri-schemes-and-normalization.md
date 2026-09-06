---
type: concept
title: http와 https URI 스킴과 정규화
description: HTTP가 자원을 가리키는 식별자의 규약 — URI 참조가 쓰이는 세 자리와 이 문서가 새로 정의한 두 문법 규칙, http와 https 스킴의 기본 포트와 빈 호스트 금지, https에서 "보안된"이 무엇을 뜻하는가와 두 스킴이 정체성을 공유하지 않는다는 것, 스킴 기반 정규화의 네 규칙과 정규화 후 동등한 URI로 서로 다른 자원을 식별하지 말라는 요건, 그리고 userinfo 부분요소의 폐기와 피싱 대응
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T09:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# http와 https URI 스킴과 정규화

- [버전 조건](#버전-조건)
- [URI 참조가 쓰이는 자리](#uri-참조가-쓰이는-자리)
- [문법과 두 개의 새 규칙](#문법과-두-개의-새-규칙)
- [길이 권고](#길이-권고)
- [URI가 있다고 서버가 있는 것은 아니다](#uri가-있다고-서버가-있는-것은-아니다)
- [http 스킴](#http-스킴)
- [https 스킴과 보안의 정의](#https-스킴과-보안의-정의)
- [정규화와 동등성](#정규화와-동등성)
- [userinfo의 폐기](#userinfo의-폐기)
- [프래그먼트](#프래그먼트)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP는 자원을 어떤 식별자로 가리키고, 두 식별자가 같은 자원을 가리키는지를 어떻게
판정하는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## URI 참조가 쓰이는 자리

- HTTP 전반에서 자원을 식별하는 수단이 URI(Uniform Resource Identifier)다
  (§4).[^fielding2022-rfc9110]
- URI 참조(URI reference)가 쓰이는 자리가 셋으로 열거된다 — 요청의 대상을 정하는 것,
  리다이렉트를 나타내는 것, 관계를 정의하는 것 (§4.1).[^fielding2022-rfc9110]
- HTTP에서 URI 참조를 허용하는 프로토콜 요소는 저마다 자기 ABNF 생성 규칙에서 어떤 형태를
  허용하는지 밝힌다. 아무 형태나(URI-reference), 절대형만(absolute-URI), 경로와 선택적 질의만
  (partial-URI), 또는 그 조합 (§4.1).[^fielding2022-rfc9110]
- 달리 표시되지 않는 한 **URI 참조는 대상 URI를 기준으로 파싱된다**
  (§4.1).[^fielding2022-rfc9110]

## 문법과 두 개의 새 규칙

- `URI-reference`, `absolute-URI`, `relative-part`, `authority`, `port`, `host`,
  `path-abempty`, `segment`, `query`의 정의는 URI 일반 문법에서 그대로 가져온다
  (§4.1).[^fielding2022-rfc9110]
- 이 문서가 새로 정의하는 규칙이 둘이다 (§4.1):[^fielding2022-rfc9110]
  - `absolute-path` — 비어 있지 않은 경로 성분을 담을 수 있는 프로토콜 요소를 위한 규칙이다.
    빈 경로를 허용하는 RFC 3986의 `path-abempty`와도, `//`로 시작하는 경로를 허용하지 않는
    `path-absolute`와도 조금 다르다.
  - `partial-URI` — 상대 URI는 담을 수 있으나 프래그먼트 성분은 담을 수 없는 프로토콜 요소를
    위한 규칙이다.
- 그 두 규칙과 두 스킴의 생성 규칙이다 (§4.1, §4.2.1, §4.2.2).[^fielding2022-rfc9110]

  ```abnf
  absolute-path = 1*( "/" segment )
  partial-URI   = relative-part [ "?" query ]

  http-URI  = "http" "://" authority path-abempty [ "?" query ]
  https-URI = "https" "://" authority path-abempty [ "?" query ]
  ```

  두 스킴의 문법이 스킴 이름 말고는 같다는 점을 눈으로 보는 것이 중요하다. 둘을 가르는 것은
  문법이 아니라 아래의 보안 요건과 기본 포트다.

## 길이 권고

- 절대 길이 제한이 없는 이 문서에서 드물게 수치가 나오는 자리다. **모든 송신자와 수신자가 프로토콜
  요소에서 최소 8000 옥텟 길이의 URI를 지원하는 것이 권장된다(RECOMMENDED)**
  (§4.1).[^fielding2022-rfc9110]
- 그 권고에는 딸린 주의가 있다. 이는 어떤 구조와 선로 위 표현(예로 HTTP/1.1의 요청 줄)이 경우에
  따라 필연적으로 더 커진다는 것을 함의한다 (§4.1).[^fielding2022-rfc9110]

## URI가 있다고 서버가 있는 것은 아니다

- IANA가 URI 스킴 레지스트리를 유지하며, 요청은 아무 URI 스킴이나 대상으로 삼을 수 있다. 다만
  HTTP 서버에 본래적인 스킴은 http와 https 둘이다 (§4.2).[^fielding2022-rfc9110]
- 존재에 대한 주의 하나가 붙는다. **http나 https URI가 있다고 해서 식별된 오리진에 연결을 기다리는
  HTTP 서버가 늘 있다는 뜻은 아니다.** 누구나 URI를 만들어 낼 수 있고, 그것은 서버가 존재하는지와도
  그 서버가 지금 그 식별자를 어떤 자원에 대응시키는지와도 무관하다 (§4.2).[^fielding2022-rfc9110]
- 그 근거는 이름 공간의 구조에 있다. 등록된 이름과 IP 주소의 위임된 성질이 HTTP 서버의 존재와
  무관하게 연합된 이름 공간을 만들어 낸다 (§4.2).[^fielding2022-rfc9110]

## http 스킴

- http 스킴은 주어진 포트에서 TCP 연결을 기다리는 잠재적 HTTP 원 서버가 관장하는 계층적 이름
  공간 안에서 식별자를 만들어 내기 위해 정의된다 (§4.2.1).[^fielding2022-rfc9110]
- 원 서버는 권한(authority) 성분으로 식별되며, 여기에 호스트 식별자와 선택적 포트 번호가 든다.
  **포트 부분요소가 비었거나 주어지지 않으면 TCP 80번 포트가 기본값**이다
  (§4.2.1).[^fielding2022-rfc9110]
- 빈 호스트에 대한 요건이 양쪽에 걸린다. **송신자는 빈 호스트 식별자를 가진 http URI를 생성해서는
  안 되고(MUST NOT), 그런 URI 참조를 처리하는 수신자는 그것을 유효하지 않은 것으로 거부해야
  한다(MUST)** (§4.2.1).[^fielding2022-rfc9110]
- 계층적 경로 성분과 선택적 질의 성분이 그 원 서버의 이름 공간 안에서 대상 자원을 식별한다
  (§4.2.1).[^fielding2022-rfc9110]

## https 스킴과 보안의 정의

- https 스킴은 주어진 포트에서 TCP 연결을 기다리고 **HTTP 통신을 위해 보안된 TLS 연결을 세울 수
  있는** 잠재적 원 서버가 관장하는 계층적 이름 공간을 위해 정의된다
  (§4.2.2).[^fielding2022-rfc9110]
- 여기서 "보안된"(secured)이 무엇을 뜻하는지가 이 문서 안에서 명시된다 (§4.2.2).[^fielding2022-rfc9110]

  > In this context, "secured" specifically means that the server has been authenticated as
  > acting on behalf of the identified authority and all HTTP communication with that server
  > has confidentiality and integrity protection that is acceptable to both client and server.

  조건이 둘이다. 서버가 식별된 권한을 대신해 행동한다고 인증됐을 것, 그리고 그 서버와의 모든
  HTTP 통신이 클라이언트와 서버 양쪽에 받아들여지는 기밀성 보호와 무결성 보호를 가질 것.
- 기본 포트는 TCP 443번이고, 빈 호스트 식별자에 대한 요건은 http 스킴과 같다
  (§4.2.2).[^fielding2022-rfc9110]
- 클라이언트에게 걸리는 요건이 하나 더 있다. **클라이언트는 https 자원에 대한 자기 HTTP 요청이
  통신되기 전에 보안되도록 보장해야 하며(MUST), 그런 요청에 대해 보안된 응답만 받아들여야 한다.**
  어떤 암호 기제가 받아들여지는가의 정의는 대개 협상되며 시간에 따라 바뀔 수 있다
  (§4.2.2).[^fielding2022-rfc9110]
- 두 스킴의 관계에 대한 진술이 실무에서 자주 잊히는 자리다. **https 스킴으로 제공되는 자원은
  http 스킴과 정체성을 공유하지 않는다. 그 둘은 별개의 이름 공간을 가진 별개의 오리진이다**
  (§4.2.2).[^fielding2022-rfc9110]
- 다만 예외가 있다. 같은 호스트를 가진 모든 오리진에 적용되도록 정의된 HTTP 확장, 예로 쿠키
  프로토콜은 한 서비스가 설정한 정보가 맞아떨어지는 호스트 도메인 무리 안의 다른 서비스와의
  통신에 영향을 주게 한다. **그런 확장은 보안된 연결에서 얻은 정보가 보안되지 않은 맥락에서 뜻하지
  않게 교환되는 것을 막도록 크게 주의해 설계되어야 마땅하다** (§4.2.2).[^fielding2022-rfc9110]

## 정규화와 동등성

- http나 https 스킴을 가진 URI는 URI 명세의 방법에 따라, 그리고 위의 스킴별 기본값을 써서
  정규화되고 비교된다 (§4.2.3).[^fielding2022-rfc9110]
- **HTTP는 동등성 판정에 특정 방법을 요구하지 않는다.** 원전이 드는 예로, 캐시 키는 단순 문자열로
  비교될 수도, 구문 기반 정규화 뒤에 비교될 수도, 스킴 기반 정규화 뒤에 비교될 수도 있다
  (§4.2.3).[^fielding2022-rfc9110]
- http와 https URI의 스킴 기반 정규화에 붙는 추가 규칙이 넷이다 (§4.2.3):[^fielding2022-rfc9110]
  - 포트가 그 스킴의 기본 포트와 같으면 정규형은 포트 부분요소를 생략하는 것이다.
  - OPTIONS 요청의 대상으로 쓰이는 경우가 아니면 빈 경로 성분은 절대 경로 `/`와 동등하므로,
    정규형은 대신 `/`를 두는 것이다.
  - 스킴과 호스트는 대소문자를 구분하지 않으며 보통 소문자로 주어진다. 나머지 성분은 전부
    대소문자를 구분해 비교된다.
  - "reserved" 집합에 들지 않는 문자는 자기 퍼센트 인코딩된 옥텟과 동등하다. 정규형은 그것을
    인코딩하지 않는 것이다.
- 그 규칙을 다 적용하면 원전이 드는 다음 셋이 동등해진다 — `http://example.com:80/~smith/home.html`,
  `http://EXAMPLE.com/%7Esmith/home.html`, `http://EXAMPLE.com:/%7esmith/home.html`
  (§4.2.3).[^fielding2022-rfc9110] 각각 기본 포트 생략, 호스트 소문자화, 퍼센트 인코딩 해제,
  그리고 빈 포트 부분요소가 걸린다.
- 그리고 그 동등성에서 요건이 하나 따라 나온다. 어떤 방법으로든 정규화 후 동등한 두 HTTP URI는
  같은 자원을 식별한다고 가정될 수 있고, 아무 HTTP 부품이나 정규화를 수행할 수 있다(MAY).
  **그 결과 서로 다른 자원을 정규화 후 동등해지는 HTTP URI로 식별해서는 안 된다(SHOULD NOT)**
  (§4.2.3).[^fielding2022-rfc9110] 이것이 URI 설계에 거는 실무 제약이다. 대소문자나 후행 슬래시나
  퍼센트 인코딩으로만 갈리는 두 경로에 다른 자원을 두면 안 된다.

## userinfo의 폐기

- URI 일반 문법의 권한 성분에는 URI 안에 사용자 인증 정보를 넣기 위한 userinfo 부분요소가 있고,
  그 안에서 `user:password` 형식의 사용은 폐기됐다 (§4.2.4).[^fielding2022-rfc9110]
- 그럼에도 어떤 구현은 명령 실행 옵션이나 설정 파일이나 북마크 목록 안에서 인증 정보의 내부 설정에
  userinfo 성분을 쓴다. 그런 사용이 사용자 식별자나 비밀번호를 노출할 수 있는데도 그렇다
  (§4.2.4).[^fielding2022-rfc9110]
- 생성 금지가 걸린다. **송신자는 http나 https URI 참조가 메시지 안에서 대상 URI나 필드 값으로
  생성될 때 userinfo 부분요소와 그 구분자 `@`를 생성해서는 안 된다(MUST NOT)**
  (§4.2.4).[^fielding2022-rfc9110]
- 수신 쪽에는 피싱 대응이 걸린다. **신뢰할 수 없는 원천에서 받은 http나 https URI 참조를 쓰기
  전에 수신자는 userinfo를 파싱해 그 존재를 오류로 다뤄야 한다(SHOULD).** 그것은 피싱 공격을
  위해 권한을 가리는 데 쓰이고 있을 공산이 크기 때문이다 (§4.2.4).[^fielding2022-rfc9110]

## 프래그먼트

- 프래그먼트 식별자는 URI 스킴과 무관하게 이차 자원의 간접적 식별을 허용한다. URI를 가리키는
  프로토콜 요소 중 어떤 것은 프래그먼트를 담는 것을 허용하고 어떤 것은 허용하지 않는다
  (§4.2.5).[^fielding2022-rfc9110]
- 둘을 가르는 방식은 문법이다. 프래그먼트가 허용되는 요소에는 그 ABNF 규칙을 쓰고, 아니면
  프래그먼트를 배제하는 별도 규칙을 쓴다 (§4.2.5).[^fielding2022-rfc9110]
- 그래서 위 http-URI와 https-URI 생성 규칙에 프래그먼트가 없다. **프래그먼트 식별자 성분은 URI
  스킴 정의의 일부가 아니므로** 스킴의 ABNF 정의에 나타나지 않는다 (§4.2.5).[^fielding2022-rfc9110]

## 이어지는 페이지

- [오리진과 권위 있는 접근](../concepts/http-origin-and-authoritative-access.md) — 이 식별자에
  누가 권위 있게 답할 자격이 있는가
- [자원과 표현](../concepts/http-resources-and-representations.md) — 이 식별자가 가리키는 것
- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — 식별자 표준에 의존하는
  설계의 자리
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 자원 식별에 URL을 쓰는 설계 철학 쪽

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. ABNF 펜스는 §4.1의
    `absolute-path`·`partial-URI`와 §4.2.1·§4.2.2의 스킴 생성 규칙을 한 펜스에 모은 것이고,
    각 줄은 원문 그대로다(URI 일반 문법에서 그대로 가져오는 규칙 아홉 개는 옮기지 않았다).
    동등한 URI 셋과 인용 블록도 원문 그대로다.

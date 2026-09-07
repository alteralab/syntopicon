---
type: concept
title: HTTP 인증 필드
description: 인증 틀이 실려 다니는 여섯 필드의 개별 의미론 — 401이 반드시 동반해야 하는 WWW-Authenticate와 그 값이 챌린지 여럿을 담을 때 생기는 파싱 문제, 크리덴셜을 나르는 Authorization과 같은 realm 안에서의 재사용 전제, 인증이 받아들여진 뒤의 마무리 정보를 나르는 Authentication-Info, 그리고 같은 모양이면서 다음 홉까지만 가는 프록시 쪽 세 필드와 중개자에게 걸린 수정 금지
generated: { by: "claude-opus-5", at: "2026-09-07T20:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 인증 필드

- [버전 조건](#버전-조건)
- [여섯 필드의 배치](#여섯-필드의-배치)
- [WWW-Authenticate](#www-authenticate)
- [챌린지 여럿을 한 값에 담을 때](#챌린지-여럿을-한-값에-담을-때)
- [Authorization](#authorization)
- [Authentication-Info](#authentication-info)
- [Proxy-Authenticate](#proxy-authenticate)
- [Proxy-Authorization](#proxy-authorization)
- [Proxy-Authentication-Info](#proxy-authentication-info)
- [원 서버 쪽과 프록시 쪽의 비대칭](#원-서버-쪽과-프록시-쪽의-비대칭)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인증의 챌린지와 크리덴셜과 마무리 정보는 각각 어느 필드에 실리고, 그 필드는
중개자를 어디까지 지나가는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 여섯 필드의 배치

- 필드가 셋씩 두 벌이다. 사용자를 원 서버에 인증하는 쪽이 `WWW-Authenticate`와 `Authorization`과
  `Authentication-Info`이고, 클라이언트를 프록시에 인증하는 쪽이 `Proxy-Authenticate`와
  `Proxy-Authorization`과 `Proxy-Authentication-Info`다 (§11.6, §11.7).[^fielding2022-rfc9110]
- 각 벌 안에서 방향이 갈린다. 챌린지를 나르는 것은 응답 필드이고, 크리덴셜을 나르는 것은 요청
  필드이며, 마무리 정보를 나르는 것은 다시 응답 필드다 (§11.6, §11.7).[^fielding2022-rfc9110]
- 값의 생성 규칙은 여섯 다 한 줄이다. 챌린지를 나르는 둘은 챌린지의 리스트이고, 크리덴셜을 나르는
  둘은 크리덴셜 하나이며, 마무리 정보를 나르는 둘은 인증 파라미터의 리스트다
  (§11.6.1, §11.6.2, §11.6.3, §11.7.1, §11.7.2, §11.7.3).[^fielding2022-rfc9110]

## WWW-Authenticate

- 정의 문장이다 (§11.6.1).[^fielding2022-rfc9110]

  > The "WWW-Authenticate" response header field indicates the authentication scheme(s) and
  > parameters applicable to the target resource.

  **대상 자원에 적용되는 인증 스킴과 파라미터**를 나타내는 응답 헤더 필드다.
- 401 응답에는 이 필드가 강제된다. 401을 생성하는 서버는 **적어도 하나의 챌린지를 담은
  `WWW-Authenticate` 헤더 필드를 보내야 한다**(MUST) (§11.6.1).[^fielding2022-rfc9110]
- 401 밖에서도 쓸 수 있다. 서버는 **크리덴셜을 내거나 다른 크리덴셜을 내면 응답이 달라질 수 있음을
  나타내려고** 다른 응답 메시지에도 이 필드를 생성해도 된다(MAY) (§11.6.1).[^fielding2022-rfc9110]
- 중개자에게 금지가 걸린다. 응답을 전달하는 프록시는 **그 응답의 어떤 `WWW-Authenticate` 헤더
  필드도 수정해서는 안 된다**(MUST NOT) (§11.6.1).[^fielding2022-rfc9110]

## 챌린지 여럿을 한 값에 담을 때

- 원전이 사용자 에이전트에게 파싱에 특별히 주의하라고 조언한다. 값이 **챌린지를 하나 넘게 담을 수
  있고**, 각 챌린지가 **콤마로 구분된 인증 파라미터 목록**을 담을 수 있으며, 게다가 **그 헤더 필드
  자체가 여러 번 나올 수 있다** (§11.6.1).[^fielding2022-rfc9110]
- 원전이 드는 예다 (§11.6.1).[^fielding2022-rfc9110]

  ```http
  WWW-Authenticate: Basic realm="simple", Newauth realm="apps",
                   type=1, title="Login to \"apps\""
  ```

- 이 한 값에 챌린지가 둘 들어 있다. realm 값이 `simple`인 `Basic` 스킴 챌린지 하나와, realm 값이
  `apps`인 `Newauth` 스킴 챌린지 하나다. 그리고 `type`과 `title`이라는 추가 파라미터 둘이 뒤쪽
  챌린지에 붙어 있다 (§11.6.1).[^fielding2022-rfc9110]
- 그런데 이 형태가 안전하지 않다. **일부 사용자 에이전트는 이 형태를 알아보지 못한다.** 그래서
  같은 필드 줄에 원소를 하나 넘게 담은 `WWW-Authenticate` 값을 보내는 것은 **상호운용되지 않을 수
  있다** (§11.6.1).[^fielding2022-rfc9110]
- 문법 자체가 부르는 모호함도 각주로 적혀 있다. 챌린지 생성 규칙도 리스트 구문을 쓰므로, **콤마와
  공백과 콤마가 이어진 자리**를 앞 챌린지에 붙은 것으로 볼 수도 있고 챌린지 목록의 빈 원소로 볼
  수도 있다. 원전은 **실무에서 이 모호함이 필드 값의 의미론에 영향을 주지 않으므로 무해하다**고
  판정한다 (§11.6.1).[^fielding2022-rfc9110]

## Authorization

- 정의는 방향이 반대다. 사용자 에이전트가 원 서버에 자기를 인증하게 하는 요청 헤더 필드이고, 그
  값은 **요청되는 자원의 realm에 대한 사용자 에이전트의 인증 정보를 담은 크리덴셜**로 이뤄진다
  (§11.6.2).[^fielding2022-rfc9110]
- realm 안에서의 재사용이 전제된다. 요청이 인증되고 realm이 지정되었으면, **같은 크리덴셜이 그
  realm 안의 다른 모든 요청에 대해서도 유효하다고 추정된다** (§11.6.2).[^fielding2022-rfc9110]
  다만 인증 스킴 자체가 달리 요구하는 경우는 예외다. 원전이 드는 예가 챌린지 값에 따라 달라지는
  크리덴셜과 동기화된 시계를 쓰는 크리덴셜이다.
- 중개자에게 금지가 걸린다. 요청을 전달하는 프록시는 **그 요청의 어떤 `Authorization` 헤더 필드도
  수정해서는 안 된다**(MUST NOT) (§11.6.2).[^fielding2022-rfc9110]
- 캐시가 이 필드를 어떻게 다뤄야 하는지의 요건은 이 문서가 갖지 않는다. RFC 9111이 정본이다
  (§11.6.2).[^fielding2022-rfc9110]

## Authentication-Info

- 쓰임이 시점으로 정의된다. HTTP 인증 스킴은 이 응답 필드로 **클라이언트의 인증 크리덴셜이
  받아들여진 뒤에** 정보를 전할 수 있다. 원전이 드는 예가 서버 쪽 인증을 담을 수 있는 마무리
  메시지다 (§11.6.3).[^fielding2022-rfc9110]
- 값은 인증 파라미터의 목록이다. **이 명세는 일반적인 형식만 서술하고**, 개별 파라미터는
  `Authentication-Info`를 쓰는 인증 스킴이 정의한다 (§11.6.3).[^fielding2022-rfc9110] 원전이 드는
  실례가 RFC 7616의 `Digest` 스킴이다.
- 쓸 수 있는 자리가 넓다. **요청 메서드와 상태 코드와 무관하게 어떤 HTTP 응답에도 쓸 수 있다.**
  그 의미론은 대응하는 요청의 `Authorization` 헤더 필드가 가리킨 인증 스킴이 정의한다
  (§11.6.3).[^fielding2022-rfc9110]
- 중개자에게 금지가 걸린다. 응답을 전달하는 프록시는 **이 필드 값을 어떤 식으로도 수정할 수 없다**
  (§11.6.3).[^fielding2022-rfc9110]
- 트레일러 필드로 보낼 수도 있다. 다만 **인증 스킴이 그것을 명시적으로 허용할 때뿐**이다
  (§11.6.3).[^fielding2022-rfc9110]

## Proxy-Authenticate

- `WWW-Authenticate`의 프록시판이다. **이 요청에 대해 그 프록시에 적용되는 인증 스킴과 파라미터를
  나타내는 챌린지를 적어도 하나** 담는다 (§11.7.1).[^fielding2022-rfc9110]
- 407에는 강제된다. 프록시는 자기가 생성하는 **각 407 응답마다 `Proxy-Authenticate` 헤더 필드를
  적어도 하나 보내야 한다**(MUST) (§11.7.1).[^fielding2022-rfc9110]
- 파싱에 관한 고려는 `WWW-Authenticate`와 같다고 명시된다 (§11.7.1).[^fielding2022-rfc9110]

## Proxy-Authorization

- 클라이언트가 인증을 요구하는 프록시에 **자기(또는 자기 사용자)를 식별하게** 하는 요청 헤더
  필드다. 값은 그 프록시와 요청되는 자원의 realm에 대한 클라이언트의 인증 정보를 담은 크리덴셜로
  이뤄진다 (§11.7.2).[^fielding2022-rfc9110]
- 소비되는 자리가 정해져 있다. 프록시가 사슬로 여럿 놓였을 때 이 필드는 **크리덴셜을 받기를 기대하고
  있던 첫 인바운드 프록시가 소비한다** (§11.7.2).[^fielding2022-rfc9110]
- 다만 중계가 열려 있다. 프록시들이 협력해 요청을 인증하는 방식이 그것이라면, 프록시는 **클라이언트
  요청의 크리덴셜을 다음 프록시로 중계해도 된다**(MAY) (§11.7.2).[^fielding2022-rfc9110]

## Proxy-Authentication-Info

- `Authentication-Info`와 **동등하되** 프록시 인증에 적용되고, 그 의미론은 대응하는 요청의
  `Proxy-Authorization` 헤더 필드가 가리킨 인증 스킴이 정의한다 (§11.7.3).[^fielding2022-rfc9110]
- 여기도 트레일러 필드로 보낼 수 있고, 조건은 같다. **인증 스킴이 명시적으로 허용할 때뿐**이다
  (§11.7.3).[^fielding2022-rfc9110]

## 원 서버 쪽과 프록시 쪽의 비대칭

- 프록시 쪽 두 필드는 **다음 홉까지만** 간다. `Proxy-Authenticate`는 `WWW-Authenticate`와 달리
  **응답 사슬에서 다음 아웃바운드 클라이언트에만 적용되고**, `Proxy-Authentication-Info`도 마찬가지다
  (§11.7.1, §11.7.3).[^fielding2022-rfc9110] `Proxy-Authorization`은 `Authorization`과 달리
  **`Proxy-Authenticate`로 인증을 요구한 다음 인바운드 프록시에만 적용된다**
  (§11.7.2).[^fielding2022-rfc9110]
- 그 이유가 한 문장으로 적혀 있다. **그 프록시를 고른 클라이언트만이 인증에 필요한 크리덴셜을 가질
  법하기 때문**이다 (§11.7.1, §11.7.3).[^fielding2022-rfc9110]
- 그런데 실무에서는 전달되는 것처럼 보일 수 있다. 큰 회사망의 사무실 캐싱 프록시와 지역 캐싱
  프록시처럼 **같은 관리 도메인 안에 여러 프록시가 있을 때**는 사용자 에이전트가 크리덴셜을 만들고
  그것이 소비될 때까지 계층을 지나 전달되는 것이 흔하다. 그런 구성에서는 **각 프록시가 같은 챌린지
  집합(또는 같은 필드 값)을 보내므로 필드가 전달되는 것처럼 보인다**
  (§11.7.1, §11.7.3).[^fielding2022-rfc9110]

## 이어지는 페이지

- [HTTP 인증 틀](../concepts/http-authentication-framework.md) — 이 여섯 필드가 나르는 챌린지와
  크리덴셜과 보호 공간의 정의
- [HTTP 중개자](../concepts/http-intermediaries.md) — 프록시 쪽 세 필드가 걸리는 그 홉의 정의
- [HTTP 메시지 전달과 hop-by-hop 필드](../concepts/http-message-forwarding-and-hop-by-hop-fields.md)
  — 다음 홉까지만 가는 필드라는 축의 일반 규칙
- [HTTP 헤더 섹션과 트레일러 섹션](../concepts/http-header-and-trailer-sections.md) — 두
  Authentication-Info가 실릴 수 있는 그 뒤쪽 섹션
- [HTTP 필드의 문법과 결합](../concepts/http-field-syntax-and-combining.md) — 같은 필드가 여러 줄로
  나올 때 값이 어떻게 하나가 되는가
- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — 상태 코드만으로 알 수 없는
  응답 맥락을 알리는 다른 필드들

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다. 예제 펜스는 §11.6.1의 예시 필드 값을 원문의 두 줄 접힘까지 그대로 옮긴
    것이다. 여섯 필드의 한 줄 생성 규칙은 옮기지 않았다(개념당 펜스 하나 규약).

---
type: concept
title: 요청 컨텍스트 필드
description: 요청 자체가 아니라 요청을 둘러싼 맥락을 알리는 다섯 필드 — 서버가 지원해야 할 기대를 선언하는 Expect와 큰 콘텐츠를 보내기 전에 허가를 묻는 100-continue의 양쪽 요건, 로봇 운영자의 메일 주소를 담는 From, 어디서 이 링크를 얻었는지 알리는 Referer와 그것이 새는 정보에 걸린 금지, 전송 코딩과 트레일러 수용 능력을 알리는 TE, 그리고 사용자 에이전트를 식별하는 User-Agent와 지문 채취 경고
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T15:30:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# 요청 컨텍스트 필드

- [버전 조건](#버전-조건)
- [이 필드들이 답하는 것](#이-필드들이-답하는-것)
- [Expect와 100-continue](#expect와-100-continue)
- [100-continue의 클라이언트 요건](#100-continue의-클라이언트-요건)
- [100-continue의 서버와 프록시 요건](#100-continue의-서버와-프록시-요건)
- [From](#from)
- [Referer](#referer)
- [Referer가 새는 정보](#referer가-새는-정보)
- [TE](#te)
- [User-Agent](#user-agent)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **요청이 무엇을 하려는지가 아니라 그 요청이 어떤 맥락에서 왔는지를 알리는 필드들은
각각 무엇을 말하는가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 이 필드들이 답하는 것

- 절의 머리말이 범위를 긋는다. 아래 요청 헤더 필드들은 **요청 컨텍스트에 대한 추가 정보를 제공하며,
  사용자와 사용자 에이전트와 요청 뒤에 있는 자원에 대한 정보를 포함한다**
  (§10.1).[^fielding2022-rfc9110]

## Expect와 100-continue

- 정의 문장이다 (§10.1.1).[^fielding2022-rfc9110]

  > The "Expect" header field in a request indicates a certain set of behaviors
  > (expectations) that need to be supported by the server in order to properly handle this
  > request.

  요청의 `Expect` 필드는 이 요청을 제대로 다루려면 **서버가 지원해야 하는 동작(기대) 집합**을
  나타낸다. 값은 대소문자를 가리지 않는다.
- 이 명세가 정의하는 기대는 **`100-continue` 하나뿐이며 정의된 파라미터가 없다**
  (§10.1.1).[^fielding2022-rfc9110] 그 밖의 원소를 담은 `Expect` 값을 받은 서버는 기대를 충족할 수
  없음을 나타내는 **417(Expectation Failed)로 응답해도 된다**(MAY).
- 그 하나가 하는 일이 적혀 있다. 클라이언트가 이 요청에 (짐작건대 큰) 콘텐츠를 보내려 하며, **메서드와
  대상 URI와 헤더 필드만으로 즉각적인 성공이나 리다이렉트나 오류 응답이 나오지 않는다면
  100(Continue) 중간 응답을 받고 싶다**는 것을 수신자에게 알린다
  (§10.1.1).[^fielding2022-rfc9110]
- 그래서 얻는 것이 무엇인지도 명시된다. 클라이언트가 콘텐츠를 실제로 보내기 전에 **보낼 가치가
  있는지의 표시를 기다릴 수 있게** 해서, 데이터가 거대하거나 오류가 예상될 때 효율을 올린다.
  원전이 드는 예가 상태를 바꾸는 메서드를 앞서 검증된 인증 자격 증명 없이 처음 보내는 경우다
  (§10.1.1).[^fielding2022-rfc9110]

## 100-continue의 클라이언트 요건

- 네 가지가 걸린다 (§10.1.1).[^fielding2022-rfc9110]
  - 클라이언트는 **콘텐츠를 포함하지 않는 요청에 100-continue 기대를 생성해서는 안 된다**(MUST NOT).
  - 요청 콘텐츠를 보내기 전에 100(Continue) 응답을 기다릴 클라이언트는 **100-continue 기대를 담은
    `Expect` 헤더 필드를 보내야 한다**(MUST).
  - 100-continue를 보낸 클라이언트가 **특정 시간을 기다려야 하는 것은 아니다.** 아직 응답을 받지
    못했어도 콘텐츠를 계속 보내도 된다(MAY).
  - **417을 받은 클라이언트는 100-continue 기대 없이 그 요청을 반복해야 한다**(SHOULD). 417은
    응답 사슬이 기대를 지원하지 않는다는 것만 나타내기 때문이다.
- 셋째 항목에 버전이 걸린다 (§10.1.1).[^fielding2022-rfc9110]
  - 버전 조건: HTTP/1.0 — 100(Continue) 응답은 HTTP/1.0 중개자를 지나 보내질 수 없으므로,
    100-continue를 보낸 클라이언트는 **콘텐츠를 보내기 전에 무한정 기다려서는 안 된다**(SHOULD NOT).
- 넷째 항목의 417도 같은 뿌리다. 원전이 드는 417의 발생 경로가 **HTTP/1.0 서버를 지나가는 경우**다
  (§10.1.1).[^fielding2022-rfc9110]

## 100-continue의 서버와 프록시 요건

- 서버 쪽 요건 넷이다 (§10.1.1).[^fielding2022-rfc9110]
  - **HTTP/1.0 요청에서 100-continue 기대를 받은 서버는 그 기대를 무시해야 한다**(MUST).
    - 버전 조건: HTTP/1.0 요청에만 걸린다.
  - 대응하는 요청의 콘텐츠를 이미 일부나 전부 받았거나 프레이밍이 콘텐츠가 없음을 나타내면, 서버는
    **100(Continue) 응답 보내기를 생략해도 된다**(MAY).
  - 100(Continue)을 보낸 서버는 요청 콘텐츠를 받아 처리한 뒤 **결국 최종 상태 코드를 보내야
    한다**(MUST). 연결이 조기에 닫힌 경우는 예외다.
  - 요청 콘텐츠 전부를 읽기 전에 최종 상태 코드로 응답한 서버는 **연결을 닫을 작정인지 요청 콘텐츠를
    계속 읽을 작정인지 나타내야 한다**(SHOULD).
- 원 서버에는 둘 중 하나를 하라는 요건이 걸린다(MUST). 메서드와 대상 URI와 100-continue 기대를 담은
  완전한 헤더 섹션을 가진 HTTP/1.1 이상의 요청을 받았고 요청 콘텐츠가 뒤따를 것이 표시되면
  (§10.1.1):[^fielding2022-rfc9110]
  - 메서드와 대상 URI와 헤더 필드만 살펴 상태를 정할 수 있으면 **최종 상태 코드로 즉시 응답한다.**
  - 아니면 클라이언트가 요청 콘텐츠를 보내도록 격려하는 **즉각적인 100(Continue) 응답**을 보낸다.
  - 버전 조건: HTTP/1.1 이상의 요청에 걸린다.
- 그리고 못 박는다 — **원 서버는 100(Continue)을 보내기 전에 콘텐츠를 기다려서는 안 된다**(MUST NOT)
  (§10.1.1).[^fielding2022-rfc9110]
- 프록시도 둘 중 하나를 해야 한다(MUST). 최종 상태 코드로 즉시 응답하거나, 대응하는 요청 줄과 헤더
  섹션을 다음 인바운드 서버로 보내 **원 서버 쪽으로 요청을 전달**한다
  (§10.1.1).[^fielding2022-rfc9110]
  - 프록시가 설정이나 과거 상호작용으로 **다음 인바운드 서버가 HTTP/1.0만 지원한다고 믿으면**,
    클라이언트가 콘텐츠를 보내기 시작하도록 격려하는 즉각적인 100(Continue) 응답을 생성해도
    된다(MAY).
    - 버전 조건: 다음 인바운드 서버가 HTTP/1.0일 때만 열리는 선택지다.

## From

- 정의 문장이다 (§10.1.2).[^fielding2022-rfc9110]

  > The "From" header field contains an Internet email address for a human user who controls
  > the requesting user agent.

  요청하는 사용자 에이전트를 통제하는 **사람 사용자의 인터넷 메일 주소**를 담는다. 그 주소는 기계가
  쓸 수 있어야 하며 문법은 RFC 5322의 `mailbox`를 그대로 가져다 쓴다.
- 실무의 분포가 적혀 있다. **로봇이 아닌 사용자 에이전트는 이 필드를 거의 보내지 않는다.** 사용자
  에이전트는 사용자의 명시적 설정 없이 이 필드를 보내서는 안 된다(SHOULD NOT). 사용자의 프라이버시
  이익이나 사이트 보안 정책과 충돌할 수 있기 때문이다 (§10.1.2).[^fielding2022-rfc9110]
- 반대로 **로봇 사용자 에이전트는 유효한 `From` 필드를 보내야 한다**(SHOULD). 로봇이 과도하거나
  원치 않거나 유효하지 않은 요청을 보내는 등 서버에 문제가 생겼을 때 운영 책임자에게 연락할 수 있게
  하기 위해서다 (§10.1.2).[^fielding2022-rfc9110]
- 서버 쪽에는 금지가 걸린다. 서버는 **접근 제어나 인증에 `From` 필드를 써서는 안 된다**(SHOULD NOT).
  그 값은 요청을 받거나 관측하는 누구에게나 보일 것으로 예상되고, 프라이버시 기대 없이 로그 파일과
  오류 보고에 기록되는 일이 잦기 때문이다 (§10.1.2).[^fielding2022-rfc9110]

## Referer

- 정의 문장이다. 필드 이름의 철자가 틀렸다는 것을 원전이 스스로 적는다
  (§10.1.3).[^fielding2022-rfc9110]

  > The "Referer" [sic] header field allows the user agent to specify a URI reference for the
  > resource from which the target URI was obtained (i.e., the "referrer", though the field
  > name is misspelled).

  **대상 URI를 얻어 온 자원**의 URI 참조를 사용자 에이전트가 지정할 수 있게 한다. 올바른 철자는
  `referrer`인데 필드 이름은 `Referer`로 굳었다.
- 값을 만들 때 걸리는 금지가 있다. 사용자 에이전트는 URI 참조의 **프래그먼트와 userinfo 컴포넌트를
  포함해서는 안 된다**(MUST NOT) (§10.1.3).[^fielding2022-rfc9110]
- 값은 절대 URI이거나 부분 URI다. 후자면 참조된 URI는 **대상 URI를 기준으로 상대적**이다
  (§10.1.3).[^fielding2022-rfc9110]
- 쓰임이 나열된다. 서버가 다른 자원으로 가는 **뒤 링크(back-link)를 만들어** 간단한 분석·로깅·최적화된
  캐싱 등에 쓰게 하고, 낡거나 잘못 입력된 링크를 찾아 관리할 수 있게 한다. 어떤 서버는 다른 사이트에서
  오는 링크를 막거나(이른바 딥 링킹) 사이트 간 요청 위조(CSRF)를 제한하는 수단으로 쓰는데, **모든
  요청이 이 필드를 담는 것은 아니다** (§10.1.3).[^fielding2022-rfc9110]
- 출처가 URI를 갖지 않을 때의 규칙이 있다. 대상 URI를 자기 URI가 없는 출처에서 얻었으면, 예컨대
  사용자의 키보드 입력이나 북마크 항목이면, 사용자 에이전트는 **`Referer` 필드를 빼거나
  `about:blank` 값으로 보내야 한다**(MUST) (§10.1.3).[^fielding2022-rfc9110]
- 값을 깎는 것은 허용된다. 이 필드 값이 **참조하는 자원의 완전한 URI를 전할 필요는 없으며**, 사용자
  에이전트는 참조 오리진 밖의 부분을 잘라 내도 된다(MAY) (§10.1.3).[^fielding2022-rfc9110]

## Referer가 새는 정보

- 문제의 성격이 적혀 있다. 이 필드는 **사용자의 요청 컨텍스트나 브라우징 이력에 대한 정보를 드러낼
  잠재력**을 갖고, 참조 자원의 식별자가 계정 이름 같은 개인 정보나 방화벽 뒤에 있어야 할 자원을
  드러내면 프라이버시 문제가 된다 (§10.1.3).[^fielding2022-rfc9110]
- 관행과 규범이 함께 적힌다 (§10.1.3).[^fielding2022-rfc9110]
  - 대부분의 범용 사용자 에이전트는 참조 자원이 로컬 `file`이나 `data` URI일 때 이 필드를 보내지
    않는다.
  - 참조 자원을 보안된 프로토콜로 접근했고 요청 대상의 오리진이 그 자원과 다르면, 사용자 에이전트는
    **`Referer`를 보내서는 안 된다**(SHOULD NOT). 참조 자원이 명시적으로 허용한 경우는 예외다.
  - 참조 자원을 보안된 프로토콜로 접근했다면, 사용자 에이전트는 **보안되지 않은 HTTP 요청에
    `Referer`를 보내서는 안 된다**(MUST NOT).
- 중개자가 이 필드를 지우는 관행에 원전이 반대 의견을 단다. 어떤 중개자는 나가는 요청에서 이 필드를
  무차별로 제거해 왔는데, 그것이 **CSRF 공격에 대한 보호를 방해하는 불행한 부작용**을 낳으며 그 공격은
  사용자에게 훨씬 더 해로울 수 있다 (§10.1.3).[^fielding2022-rfc9110]
- 그래서 대안이 제시된다. 정보 노출을 제한하고 싶은 중개자와 사용자 에이전트 확장은 **내부 도메인
  이름을 가명으로 바꾸거나 질의와 경로 컴포넌트를 잘라 내는 등 특정한 편집으로 변경을 제한하는 것이
  좋다.** 그리고 중개자는 필드 값이 대상 URI와 같은 스킴과 호스트를 공유할 때 **`Referer`를 수정하거나
  삭제해서는 안 된다**(SHOULD NOT) (§10.1.3).[^fielding2022-rfc9110]

## TE

- 정의 문장이다 (§10.1.4).[^fielding2022-rfc9110]

  > The "TE" header field describes capabilities of the client with regard to transfer codings
  > and trailer sections.

  **전송 코딩과 트레일러 섹션에 관한 클라이언트의 능력**을 서술한다. 두 가지를 한 필드가 겸한다.
- 트레일러 쪽 쓰임이 하나다. 요청에 보내진 `TE` 필드에 `trailers` 원소가 있으면 **클라이언트가 트레일러
  필드를 버리지 않을 것**임을 나타낸다 (§10.1.4).[^fielding2022-rfc9110]
- 전송 코딩 쪽 쓰임이 다른 하나다 (§10.1.4).[^fielding2022-rfc9110]
  - 버전 조건: HTTP/1.1 — `TE`는 응답에서 클라이언트가 받아들일 수 있는 전송 코딩이 무엇인지 서버에
    알리는 데도 쓰인다. **이 문서가 나온 시점에 전송 코딩을 쓰는 것은 HTTP/1.1뿐이다.**
- 값의 구성이 정해져 있다. `trailers`를 뺀 각 원소는 **전송 코딩 이름 토큰**과, 그 코딩에 대한 상대적
  선호를 나타내는 선택적 가중치와, 그 코딩의 선택적 파라미터로 이뤄진다
  (§10.1.4).[^fielding2022-rfc9110]
- 그 가중치가 콘텐츠 협상 필드들과 같은 문법이다. **`q`라는 이름의 파라미터**이고 대소문자를 가리지
  않으며, 값은 **0에서 1 사이의 실수로 정규화되어 0.001이 가장 덜 선호되고 1이 가장 선호되며 0은
  "받아들일 수 없음"** 을 뜻한다. `q`가 없으면 기본 가중치는 1이고, 보내는 쪽은 소수점 뒤 세 자리를
  넘겨 생성해서는 안 된다(MUST NOT) (§12.4.2).[^fielding2022-rfc9110] 이 문법을 쓰는 다른 필드들은
  [콘텐츠 협상 필드와 품질 값](../concepts/http-content-negotiation-fields.md)에 있다.
- 중개자에 걸리는 요건이 있다. `TE`를 보내는 송신자는 중개자가 이 필드를 전달하지 않도록 **`Connection`
  헤더 필드 안에 `TE` 연결 옵션도 보내야 한다**(MUST) (§10.1.4).[^fielding2022-rfc9110] 곧 `TE`는
  hop-by-hop 필드다.

## User-Agent

- 정의 문장이다 (§10.1.5).[^fielding2022-rfc9110]

  > The "User-Agent" header field contains information about the user agent originating the
  > request, which is often used by servers to help identify the scope of reported
  > interoperability problems, to work around or tailor responses to avoid particular user
  > agent limitations, and for analytics regarding browser or operating system use.

  요청을 낸 **사용자 에이전트에 대한 정보**를 담는다. 서버는 흔히 보고된 상호운용 문제의 범위를
  식별하거나, 특정 사용자 에이전트의 한계를 피해 응답을 맞추거나, 브라우저와 운영 체제 사용을 분석하는
  데 쓴다. 사용자 에이전트는 그러지 말라고 특별히 설정되지 않은 한 **요청마다 이 필드를 보내야
  한다**(SHOULD).
- 값의 구성이 정해져 있다. 하나 이상의 **제품 식별자(product identifier)** 와 그 각각에 딸린 0개
  이상의 코멘트로 이뤄지며, 그것들이 함께 사용자 에이전트 소프트웨어와 그 중요한 하위 제품을 식별한다.
  관례로 제품 식별자는 **식별에 중요한 순으로 내림차순 나열**하고, 각 식별자는 이름과 선택적 버전으로
  이뤄진다 (§10.1.5).[^fielding2022-rfc9110]
- 무엇을 담지 말아야 하는지가 요건이다 (§10.1.5).[^fielding2022-rfc9110]
  - 송신자는 제품을 식별하는 데 필요한 만큼으로 생성을 **제한해야 하고**(SHOULD), 제품 식별자 안에
    **광고나 그 밖의 비본질적 정보를 생성해서는 안 된다**(MUST NOT).
  - 송신자는 버전 식별자가 아닌 정보를 `product-version`에 생성해서는 안 된다(SHOULD NOT). 같은 제품
    이름의 이어지는 버전들은 그 부분에서만 달라야 하기 때문이다.
- 지문 채취 경고가 붙는다. 사용자 에이전트는 **쓸데없이 잘게 쪼갠 세부를 담은 값을 생성해서는 안
  되고**(SHOULD NOT) 제삼자에 의한 하위 제품 추가를 제한해야 한다. **지나치게 길고 상세한 값은 요청
  지연을 늘리고 사용자가 원치 않게 식별될 위험("지문 채취", fingerprinting)을 키운다**
  (§10.1.5).[^fielding2022-rfc9110]
- 다른 구현을 사칭하는 관행에도 언급이 있다. 호환성을 선언하려고 다른 구현의 제품 토큰을 쓰지 않기를
  권하는데, **그것이 이 필드의 목적을 무력화하기 때문**이다. 사용자 에이전트가 다른 사용자 에이전트를
  사칭하면, 수신자는 실제 에이전트에서 잘 동작하지 않더라도 사용자가 그 식별된 에이전트용 응답을
  일부러 원한다고 가정할 수 있다 (§10.1.5).[^fielding2022-rfc9110]

## 이어지는 페이지

- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — 같은 축의 응답 쪽 네 필드
- [HTTP 필드 값의 공통 문법 규칙](../concepts/http-field-common-rules.md) — 여기 쓰인 토큰과 코멘트와
  파라미터의 정의
- [HTTP 메시지 전달과 hop-by-hop 필드](../concepts/http-message-forwarding-and-hop-by-hop-fields.md)
  — TE가 Connection 옵션을 동반해야 하는 이유
- [HTTP 헤더 섹션과 트레일러 섹션](../concepts/http-header-and-trailer-sections.md) — TE의 trailers가
  가리키는 그 섹션
- [http와 https URI 스킴과 정규화](../concepts/http-uri-schemes-and-normalization.md) — Referer가
  빼야 하는 프래그먼트와 userinfo의 정의
- [오리진과 권위 있는 접근](../concepts/http-origin-and-authoritative-access.md) — Referer 금지가
  걸리는 오리진 비교의 정의
- [POST와 PUT](../concepts/http-post-and-put.md) — 큰 콘텐츠를 보내기 전에 Expect를 쓰게 되는 자리
- [콘텐츠 협상 필드와 품질 값](../concepts/http-content-negotiation-fields.md) — TE가 빌려 쓰는 가중치
  문법의 정의와 Accept 계열 네 필드
- [콘텐츠 협상](../concepts/http-content-negotiation.md) — User-Agent가 암묵적 협상 재료로 쓰인다고
  적힌 자리

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로이며, `[sic]`도 원문 표기다.

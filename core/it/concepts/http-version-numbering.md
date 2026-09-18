---
type: concept
title: HTTP 버전 번호와 의미론의 분리
description: HTTP의 두 자리 버전 번호가 무엇을 선언하는가 — 앞자리는 메시징 구문을 뒷자리는 송신자가 준수하는 최고 minor 버전을 가리킨다는 정의, 핵심 의미론은 버전을 넘어 바뀌지 않고 "선로 위의" 표현만 바뀐다는 원전의 문장, 버전을 올리지 않고 확장점으로 늘리는 길, 버전 표기 하나가 실은 여러 명세의 결합에 대한 준수 선언이라는 것, minor 번호가 요건이 아니라 능력 광고로 쓰인다는 것, 그리고 그 규칙이 실제로 적용된 자리와 HTTP/1.1의 첫 인터넷 표준이 2022년에야 나왔다는 연표
generated: { by: "claude-opus-5", at: "2026-09-18T14:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
  - { id: dynowski2025, resource: /it/sources/dynowski2025.md }
---

# HTTP 버전 번호와 의미론의 분리

- [버전 조건](#버전-조건)
- [두 자리가 각각 뜻하는 것](#두-자리가-각각-뜻하는-것)
- [의미론은 버전을 넘어 바뀌지 않는다](#의미론은-버전을-넘어-바뀌지-않는다)
- [버전 없이 늘리는 길](#버전-없이-늘리는-길)
- [버전 표기가 가리키는 명세 집합](#버전-표기가-가리키는-명세-집합)
- [언제 major가 오르고 언제 minor가 오르는가](#언제-major가-오르고-언제-minor가-오르는가)
- [minor 번호는 능력 광고다](#minor-번호는-능력-광고다)
- [이 규칙이 실제로 적용된 자리](#이-규칙이-실제로-적용된-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP의 버전 번호 두 자리는 각각 무엇을 선언하며, 버전이 올라도 바뀌지 않는 것은
무엇인가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 두 자리가 각각 뜻하는 것

- HTTP의 버전 번호는 마침표로 구분된 십진 숫자 둘로 이뤄진다 (§2.5).[^fielding2022-rfc9110]
- 앞자리(major version)는 **메시징 구문**을 가리킨다 (§2.5).[^fielding2022-rfc9110]
- 뒷자리(minor version)는 송신자가 준수하는, 곧 앞으로의 통신에서 이해할 수 있는, 그 major
  버전 안의 **최고 minor 버전**을 가리킨다 (§2.5).[^fielding2022-rfc9110]
- major 버전이 minor 버전을 하나도 정의하지 않을 때는 minor 버전 "0"이 함의된다. minor 버전
  식별자를 요구하는 요소 안에서 그 프로토콜을 가리킬 때 이 "0"이 쓰인다
  (§2.5).[^fielding2022-rfc9110]

## 의미론은 버전을 넘어 바뀌지 않는다

- 이 페이지의 핵심 문장이자 RFC 9110이 별도 문서로 존재하는 근거다 (§2.5).[^fielding2022-rfc9110]

  > While HTTP's core semantics don't change between protocol versions, their expression "on
  > the wire" can change, and so the HTTP version number changes when incompatible changes
  > are made to the wire format.

  버전 번호가 추적하는 것은 선로 위의 형식이지 의미론이 아니다. 그래서 HTTP/1.1과 HTTP/2와
  HTTP/3의 GET은 같은 GET이다.
- 이 진술의 짝이 되는 사실이 세 major 버전이 같은 의미론 문서에 의존한다는 것이다. 자세한 자리는
  [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md)에 있다.

## 버전 없이 늘리는 길

- 버전 번호를 올리지 않고도 프로토콜을 늘릴 수 있다. HTTP는 정의된 확장점(extension point)을 통해
  **점진적이고 후진 호환인 변경**이 버전을 바꾸지 않고 이뤄지는 것을 허용한다
  (§2.5).[^fielding2022-rfc9110]
- 그래서 실무에서 마주치는 대부분의 새 기능은 버전 번호에 흔적을 남기지 않는다. 새 필드, 새 메서드,
  새 상태 코드가 그렇게 들어온다.

## 버전 표기가 가리키는 명세 집합

- 버전 번호 전체는 **그 버전에 대응하는 명세가 늘어놓은 요건 집합에 대한 송신자의 준수**를
  가리킨다 (§2.5).[^fielding2022-rfc9110]
- 그 집합이 문서 하나가 아니다. 원전이 드는 예에서 "HTTP/1.1"이라는 버전은 이 문서와 HTTP
  Caching과 HTTP/1.1 세 명세의 결합으로 정의된다 (§2.5).[^fielding2022-rfc9110]
- 그러므로 "HTTP/1.1을 준수한다"는 선언은 캐싱 명세의 요건도 포함한다. 준수가 역할 단위로도
  갈린다는 점은 [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md)에
  있다.

## 언제 major가 오르고 언제 minor가 오르는가

- major 번호는 **호환되지 않는 메시지 구문이 도입될 때** 올린다 (§2.5).[^fielding2022-rfc9110]
- minor 번호는 프로토콜에 가한 변경이 **메시지 의미론에 무언가를 더하거나 송신자의 추가 능력을
  함의하는 효과**를 가질 때 올린다 (§2.5).[^fielding2022-rfc9110]
- 이 규칙이 HTTP/2와 HTTP/3에 minor 버전이 없는 이유를 설명한다. 둘 다 선로 위 형식을 갈아
  major를 올린 쪽이다.

## minor 번호는 능력 광고다

- minor 번호의 기능이 요건 선언에 그치지 않는다. **송신자가 프로토콜의 후진 호환인 부분집합만
  쓰고 있을 때조차 minor 버전은 송신자의 통신 능력을 광고한다**
  (§2.5).[^fielding2022-rfc9110]
- 그렇게 해서 수신자는 더 진보한 기능을 쓸 수 있음을 알게 된다. 서버라면 응답에서, 클라이언트라면
  앞으로의 요청에서 (§2.5).[^fielding2022-rfc9110]
- 곧 minor 번호는 "나는 이만큼까지 이해한다"는 선언이지 "나는 이만큼을 쓰고 있다"는 보고가 아니다.

## 이 규칙이 실제로 적용된 자리

이 절만 다른 소스에서 왔다. 위 규범이 실제 연표에서 무엇으로 나타났는지를 채운다.

- 규칙의 요약이 같다. **HTTP major 판 번호의 증가는 프로토콜 안 메시지의 형식이 바뀌었음을
  가리킨다** (4장, p.133).[^dynowski2025] 저자들이 그 근거로 판 번호의 사용과 해석을 다루는
  RFC 2145를 각주에 든다. RFC 9110 §2.5의 진술과 같은 것을 다른 문서로 확인해 주는 자리다.
- 번호가 오른 자리의 연표다 (4장, pp.108, 112, 128, 133, 139):[^dynowski2025]
  - **HTTP/0.9는 1991년에 규정된 최초의 HTTP다.**
  - **HTTP/1.0은 1996년에 정보성 RFC로 출판되었고, 당시 HTTP의 통상 쓰임을 서술한 것이다.
    정보성 RFC는 인터넷 표준이 아니다.**
  - **HTTP/1.1은 1997년에 이르렀고 1999년의 RFC 초안 표준이 그 뒤를 이었다.**
  - **HTTP/2는 2009년 공개된 SPDY에서 나와 2015년 RFC로 출판되었다.**
  - **HTTP/3는 2013년 발표된 전송 프로토콜 QUIC을 바탕으로 한다.**
- 위 [버전 표기가 가리키는 명세 집합](#버전-표기가-가리키는-명세-집합)에 붙는 사실이 하나 있다.
  **HTTP/1.1의 첫 인터넷 표준은 2022년에야 출판되었다** (4장, p.128 각주).[^dynowski2025]
  "HTTP/1.1"이라는 표기가 1997년부터 쓰였으니, 그 표기가 가리키는 명세 집합이 25년 동안 표준
  트랙을 밟고 있었다는 뜻이다.
- 각 판이 무엇을 고치려고 나왔는가는
  [HTTP 초기 판들과 TCP의 한계](../concepts/http-early-versions-and-tcp-limits.md)와
  [HTTP/2와 HTTP/3의 다중화와 QUIC](../concepts/http-multiplexing-and-quic.md)에 있다.

## 이어지는 페이지

- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — 세 major 버전이 같은
  의미론에 의존한다는 진술과 문서 분업의 내력
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 구문 준수와
  의미론 준수가 갈리는 자리
- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 후진 호환이라는
  낱말의 일반 정의
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 서비스 API의 버저닝이 같은 문제를
  다른 층위에서 만나는 자리
- [HTTP 초기 판들과 TCP의 한계](../concepts/http-early-versions-and-tcp-limits.md) — 0.9에서
  1.1까지 각 판이 고치려 한 것
- [HTTP/2와 HTTP/3의 다중화와 QUIC](../concepts/http-multiplexing-and-quic.md) — major 번호가
  두 번 오르며 선로 위 형식이 어떻게 갈렸는가

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다.

[^dynowski2025]: Dynowski & Dulak 2025, *Learning API Styles* (O'Reilly, 초판), 4장
    "Web Protocols". locator는 인쇄판 쪽이다. 이 소스가 전하는 RFC 번호와 연도는 2차 경유이고,
    해당 RFC 자체는 이 KB에 원전으로 들어와 있지 않다.

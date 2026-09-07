---
type: concept
title: HTTP 버전 번호와 의미론의 분리
description: HTTP의 두 자리 버전 번호가 무엇을 선언하는가 — 앞자리는 메시징 구문을 뒷자리는 송신자가 준수하는 최고 minor 버전을 가리킨다는 정의, 핵심 의미론은 버전을 넘어 바뀌지 않고 "선로 위의" 표현만 바뀐다는 원전의 문장, 버전을 올리지 않고 확장점으로 늘리는 길, 버전 표기 하나가 실은 여러 명세의 결합에 대한 준수 선언이라는 것, 그리고 minor 번호가 요건이 아니라 능력 광고로 쓰인다는 것
generated: { by: "claude-opus-5", at: "2026-09-07T09:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 버전 번호와 의미론의 분리

- [버전 조건](#버전-조건)
- [두 자리가 각각 뜻하는 것](#두-자리가-각각-뜻하는-것)
- [의미론은 버전을 넘어 바뀌지 않는다](#의미론은-버전을-넘어-바뀌지-않는다)
- [버전 없이 늘리는 길](#버전-없이-늘리는-길)
- [버전 표기가 가리키는 명세 집합](#버전-표기가-가리키는-명세-집합)
- [언제 major가 오르고 언제 minor가 오르는가](#언제-major가-오르고-언제-minor가-오르는가)
- [minor 번호는 능력 광고다](#minor-번호는-능력-광고다)
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

## 이어지는 페이지

- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — 세 major 버전이 같은
  의미론에 의존한다는 진술과 문서 분업의 내력
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 구문 준수와
  의미론 준수가 갈리는 자리
- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 후진 호환이라는
  낱말의 일반 정의
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 서비스 API의 버저닝이 같은 문제를
  다른 층위에서 만나는 자리

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록은 rfc-editor
    정본의 원문 그대로다.

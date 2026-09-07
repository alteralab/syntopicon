---
type: concept
title: HTTP 날짜 형식
description: HTTP 필드에 타임스탬프를 싣는 규칙 — 1995년 이전에 갈라진 세 형식을 호환을 위해 전부 정의해 두고 수신자는 셋 다 받아야 하지만 송신자는 고정 길이 단일 시간대인 IMF-fixdate만 만들어야 한다는 비대칭, 값이 언제나 협정 세계시라는 것, 두 자리 연도를 만났을 때의 50년 규칙, 시계를 가진 구현이라는 정의, 그리고 그 시계 위에 서 있는 Date 헤더 필드의 요건
generated: { by: "claude-opus-5", at: "2026-09-07T12:00:00Z" }
sources:
  - { id: fielding2022-rfc9110, resource: /it/sources/fielding2022-rfc9110.md }
---

# HTTP 날짜 형식

- [버전 조건](#버전-조건)
- [형식이 셋인 이유](#형식이-셋인-이유)
- [수신자와 송신자에 다르게 걸리는 요건](#수신자와-송신자에-다르게-걸리는-요건)
- [선호 형식의 문법](#선호-형식의-문법)
- [시간대와 두 자리 연도](#시간대와-두-자리-연도)
- [시계라는 정의](#시계라는-정의)
- [Date 헤더 필드](#date-헤더-필드)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **HTTP 필드에 실리는 시각은 어떤 형식으로 적히고, 왜 하나가 아니라 셋인가.**

## 버전 조건

> **버전 조건**: RFC 9110(2022-06, STD 97) 기준. 2026-09-07 시점 이를 갱신하거나 폐기하는
> RFC 없음(datatracker 실측).

## 형식이 셋인 이유

- 1995년 이전에 서버들이 타임스탬프를 전하는 데 흔히 쓰던 형식이 **셋으로 갈라져 있었다.** 옛
  구현과의 호환을 위해 이 문서가 셋 모두를 정의한다 (§5.6.7).[^fielding2022-rfc9110]
- 선호 형식은 인터넷 메시지 형식이 쓰는 날짜와 시각 명세의 **고정 길이이고 단일 시간대인 부분
  집합**이며 IMF-fixdate라 부른다 (§5.6.7).[^fielding2022-rfc9110]
- 셋을 나란히 보면 이렇다 (§5.6.7).[^fielding2022-rfc9110]

  | 형식 | 예 | 지위 |
  |---|---|---|
  | IMF-fixdate | `Sun, 06 Nov 1994 08:49:37 GMT` | 선호 형식 |
  | RFC 850 형식 | `Sunday, 06-Nov-94 08:49:37 GMT` | 폐기된 형식 |
  | ANSI C의 asctime 형식 | `Sun Nov  6 08:49:37 1994` | 폐기된 형식 |

- 문법 전체는 `HTTP-date = IMF-fixdate / obs-date`이고, `obs-date`가 나머지 둘을 묶는다
  (§5.6.7).[^fielding2022-rfc9110]

## 수신자와 송신자에 다르게 걸리는 요건

- 두 방향의 요건이 어긋나 있고, 그 어긋남이 이 절의 요점이다
  (§5.6.7).[^fielding2022-rfc9110]

  > A recipient that parses a timestamp value in an HTTP field MUST accept all three
  > HTTP-date formats.  When a sender generates a field that contains one or more timestamps
  > defined as HTTP-date, the sender MUST generate those timestamps in the IMF-fixdate format.

  받는 쪽은 세 형식을 **전부** 받아야 하고, 보내는 쪽은 IMF-fixdate로만 만들어야 한다. 폐기된
  형식이 사라지지 않고 파서에만 남는 구조다.
- 수신자는 필드 정의가 달리 제한하지 않는 한 타임스탬프 파싱에 견고하기를 권장받는다. HTTP가
  아닌 출처에서 온 메시지가 HTTP로 전달되면서 인터넷 메시지 형식이 정의하는 아무 날짜 명세나
  만들어 낼 수 있기 때문이다 (§5.6.7).[^fielding2022-rfc9110]
- 이 형식 요건은 **프로토콜 스트림 안의 쓰임에만** 적용된다. 구현이 사용자 표시나 요청 로깅에까지
  이 형식을 쓸 것을 요구받지는 않는다 (§5.6.7).[^fielding2022-rfc9110]

## 선호 형식의 문법

- IMF-fixdate의 생성 규칙이다 (§5.6.7).[^fielding2022-rfc9110]

  ```abnf
  IMF-fixdate  = day-name "," SP date1 SP time-of-day SP GMT
  ; fixed length/zone/capitalization subset of the format
  ; see Section 3.3 of [RFC5322]

  date1        = day SP month SP year
               ; e.g., 02 Jun 1982

  day          = 2DIGIT
  year         = 4DIGIT

  GMT          = %s"GMT"

  time-of-day  = hour ":" minute ":" second
               ; 00:00:00 - 23:59:60 (leap second)
  ```

- 요일 이름과 달 이름은 대소문자를 가리는 고정 문자열 집합으로 열거되어 있고, 이 펜스에서는
  그 열거를 뺐다 (§5.6.7).[^fielding2022-rfc9110]
- `time-of-day`의 주석이 초를 60까지 허용한다. **윤초** 때문이다
  (§5.6.7).[^fielding2022-rfc9110]
- HTTP-date는 **대소문자를 가린다.** 캐시 수신자에 한해 캐싱 명세가 이를 완화한다
  (§5.6.7).[^fielding2022-rfc9110]
- 송신자는 문법에 SP로 명시된 것 말고 추가 공백을 만들어서는 안 된다
  (§5.6.7).[^fielding2022-rfc9110]

## 시간대와 두 자리 연도

- HTTP-date 값은 시각을 **협정 세계시(UTC)의 한 순간으로** 나타낸다. 앞의 두 형식은 UTC를 그리니치
  표준시의 세 글자 약칭인 `GMT`로 표시하고, asctime 형식의 값은 UTC로 가정된다
  (§5.6.7).[^fielding2022-rfc9110]
- 두 자리 연도를 쓰는 RFC 850 형식에는 해석 규칙이 따로 있다. 수신자는 **50년 넘게 미래로 보이는
  타임스탬프를 같은 끝 두 자리를 가진 가장 최근의 과거 연도로 해석해야 한다**
  (§5.6.7).[^fielding2022-rfc9110]

## 시계라는 정의

- 원전이 "시계"를 구현의 성질로 정의한다. **시계(clock)는 UTC로 현재 순간의 합리적 근사를 제공할
  수 있는 구현**이고, 시계 구현은 NTP나 비슷한 프로토콜로 UTC와 동기하는 것이 옳다
  (§5.6.7).[^fielding2022-rfc9110]
- 이 정의가 뒤에서 조건으로 쓰인다. 시계가 있는 원 서버와 없는 원 서버에 걸리는 요건이 갈리기
  때문이다 (§6.6.1, §8.8.2.1).[^fielding2022-rfc9110]

## Date 헤더 필드

- `Date` 헤더 필드는 **메시지가 발원한 날짜와 시각**을 나타내며, 인터넷 메시지 형식의 발원 날짜
  필드와 같은 의미론을 갖는다. 값은 HTTP-date다 (§6.6.1).[^fielding2022-rfc9110]
- 생성 시점은 느슨하다. 이론상으로는 메시지 콘텐츠를 만들기 직전의 순간을 나타내야 옳지만,
  실무에서 송신자는 메시지 발원 중 어느 때든 값을 만들 수 있다 (§6.6.1).[^fielding2022-rfc9110]
- 시계 유무로 요건이 갈린다 (§6.6.1).[^fielding2022-rfc9110]
  - 시계가 있는 원 서버는 2xx와 3xx와 4xx 응답 **전부에** `Date` 헤더 필드를 만들어야 하고,
    1xx와 5xx 응답에는 만들어도 된다.
  - 시계가 **없는** 원 서버는 `Date` 헤더 필드를 만들어서는 안 된다.
- 빠진 값을 메우는 것은 수신자 몫이다. 시계가 있는 수신자가 `Date` 없는 응답 메시지를 받으면 받은
  시각을 기록해야 하고, 그 메시지를 캐시하거나 하류로 전달한다면 대응하는 `Date` 헤더 필드를
  헤더 섹션에 덧붙여야 한다. 무효한 값을 받았으면 받은 시각으로 바꿔도 된다
  (§6.6.1).[^fielding2022-rfc9110]
- 요청에도 보낼 수 있으나 보통은 보내지 않는다. 사용자 에이전트와 서버의 시계 차이에 따라 서버가
  요청 해석을 조정하기를 기대하는 맞춤 응용 같은 자리에서만 유용하다
  (§6.6.1).[^fielding2022-rfc9110]

## 이어지는 페이지

- [HTTP 필드 값의 공통 문법 규칙](../concepts/http-field-common-rules.md) — 같은 §5.6 아래 있는
  나머지 공통 부품
- [HTTP 필드의 문법과 결합](../concepts/http-field-syntax-and-combining.md) — 콤마를 담는 날짜를
  왜 인용 문자열로 감싸는가
- [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md) — 이
  타임스탬프가 검증자로 쓰일 때의 강약 판정
- [HTTP 메시지 추상과 프레이밍](../concepts/http-message-abstraction-and-framing.md) — Date가 속한
  메시지 메타데이터의 자리

[^fielding2022-rfc9110]: Fielding, Nottingham & Reschke 2022, RFC 9110 "HTTP Semantics"
    (IETF, STD 97). 쪽 번호가 없는 문서이므로 locator는 절 번호다. 인용 블록과 ABNF 펜스는
    rfc-editor 정본의 원문 그대로이되, 펜스에서는 요일 이름과 달 이름의 열거 규칙을 뺐다.

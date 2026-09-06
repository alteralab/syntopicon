---
type: synthesis
title: HTTP 메시지와 필드
description: HTTP 의미론 허브의 자식 — 이름과 값의 쌍인 필드의 문법과 결합 규칙, 버전을 넘어 같은 네 부분으로 이루어지는 메시지의 추상, 그 메시지가 어느 대상으로 정해져 중개자를 지나 전달되는 경로, 그리고 요청과 응답의 맥락을 상대에게 알리는 컨텍스트 필드
generated: { by: "claude-opus-5", at: "2026-09-07T22:00:00Z" }
---

# HTTP 메시지와 필드

**이름의 범위가 곧 이 허브의 범위다.** 여기는 HTTP가 무엇을 실어 나르는 그릇인지 — 곧 필드와
메시지, 그 메시지가 정해지고 전달되는 경로, 그리고 그 메시지에 맥락을 붙이는 필드들 — 이 사는
자리다. 그 그릇에 실린 것이 무엇을 뜻하는지(메서드·상태 코드·표현)는 부모 허브 아래 다른 자리에
있다.

특정 버전의 전송 형식은 여기 없다. HTTP/1.1의 메시지 구문과 HTTP/2·3의 프레이밍은 각자의 명세가
정본이고, 이 자식 허브의 페이지들은 그 경계를 만날 때마다 "그쪽은 저 문서가 맡는다"고만 적는다.

새 필드를 정의할 때 지켜야 하는 규칙은 여기 두지 않았다. 그것은 확장점 이야기라 부모 허브의
확장 절에 산다.

부모 허브는 [HTTP 의미론](http-semantics.md)이다.

## 필드

- [HTTP 필드의 문법과 결합](../concepts/http-field-syntax-and-combining.md) — 같은 이름의 필드 줄이
  콤마로 이어져 하나의 값이 되는 규칙과 순서가 뜻을 바꾼다는 귀결
- [HTTP 필드 값의 공통 문법 규칙](../concepts/http-field-common-rules.md) — 토큰과 공백 세 종류와
  인용 문자열과 코멘트와 파라미터와 리스트 확장 문법
- [HTTP 날짜 형식](../concepts/http-date-formats.md) — 수신자는 세 형식을 다 받고 송신자는 하나만
  만든다는 비대칭, 그리고 Date 필드

## 메시지

- [HTTP 메시지 추상과 프레이밍](../concepts/http-message-abstraction-and-framing.md) — 버전 무관한
  네 부분의 메시지 정의와 완결의 판정
- [HTTP 헤더 섹션과 트레일러 섹션](../concepts/http-header-and-trailer-sections.md) — 콘텐츠 앞뒤
  두 자리의 지위 차이와 트레일러에 걸리는 제약
- [HTTP 콘텐츠의 의미론과 식별](../concepts/http-content-semantics.md) — 실린 옥텟의 뜻을 메서드와
  상태 코드가 정한다는 것과 응답 식별의 순서 규칙

## 라우팅

- [요청 대상과 Host](../concepts/http-target-uri-and-host.md) — 대상 URI를 정하고 실어 보내고 다시
  재구성하는 경로, 그리고 잘못 보내진 요청의 거절
- [HTTP 메시지 전달과 hop-by-hop 필드](../concepts/http-message-forwarding-and-hop-by-hop-fields.md)
  — Connection이 가르는 종단 간 필드와 다음 수신자까지만 가는 필드, Via와 Max-Forwards와 Upgrade

## 컨텍스트 필드

- [요청 컨텍스트 필드](../concepts/http-request-context-fields.md) — Expect와 100-continue의 양쪽
  요건, From, Referer와 그것이 새는 정보, TE, User-Agent와 지문 채취
- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — Allow, 201과 3xx에서 뜻이
  갈리는 Location, 언제 다시 오라는 Retry-After, 그리고 Server

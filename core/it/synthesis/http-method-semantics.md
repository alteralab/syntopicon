---
type: synthesis
title: HTTP 메서드 의미론
description: HTTP 의미론 허브의 자식 — 요청이 무엇을 하려는 것인지를 정하는 메서드 토큰의 지위와 표준 메서드 여덟의 정의, 그 여덟에 공통으로 걸리는 안전성과 멱등성과 캐시 가능성, 그리고 멱등성이 자동 재시도에 여는 것과 닫는 것
generated: { by: "claude-opus-5", at: "2026-09-07T22:00:00Z" }
---

# HTTP 메서드 의미론

**이름의 범위가 곧 이 허브의 범위다.** 여기는 요청의 뜻을 정하는 메서드 — 곧 그 토큰의 지위,
표준 여덟의 정의, 그리고 그 여덟에 공통으로 걸리는 속성 — 이 사는 자리다. 그 요청이 어느 대상으로
가고 어느 필드에 실리는지는 형제 허브인
[HTTP 메시지와 필드](http-messages-and-fields.md)에 있고, 응답 쪽의 뜻을 정하는 상태 코드는
부모 허브 아래에 있다.

부모 허브는 [HTTP 의미론](http-semantics.md)이다.

## 메서드라는 자리

- [HTTP 요청 메서드의 지위](../concepts/http-request-methods-overview.md) — 메서드 토큰이 요청
  의미론의 일차 출처라는 규정, 표준 메서드 여덟의 목록, 모르는 메서드와 막힌 메서드의 갈림
- [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)
  — 세 공통 속성의 정의와 여덟 메서드의 배정, 안전이 구현의 부작용을 금지하지 않는다는 것
- [멱등성과 자동 재시도의 규범](../concepts/http-idempotency-and-automatic-retry.md) — 끊긴 요청을
  다시 보내도 되는지의 판정과 프록시에 걸린 절대 금지, 그리고 중복 제거 수단을 정의하지 않은 자리

## 여덟 메서드

- [GET과 HEAD](../concepts/http-get-and-head.md) — 선택된 표현의 전송을 요청한다는 정의와 콘텐츠를
  뺀 판본이 어디까지 같아야 하는가
- [POST와 PUT](../concepts/http-post-and-put.md) — 자원별 처리와 상태 대치라는 의도의 차이, PUT이
  이후의 관측을 보장하지 않는다는 단서
- [DELETE와 CONNECT와 OPTIONS와 TRACE](../concepts/http-delete-connect-options-and-trace.md) —
  URI 매핑의 연결 해제, 터널 개설과 그 위험, 별표 요청 대상, 요청의 되비춤

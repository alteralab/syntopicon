---
type: synthesis
title: HTTP 의미론
description: HTTP의 현행 원전(RFC 9110, STD 97)에서 나온 페이지들의 진입점 — 자원과 표현과 무상태와 중개자라는 어휘, 이름과 값의 쌍인 필드와 버전 무관한 네 부분의 메시지, 대상 URI를 정하고 중개자를 지나 보내는 라우팅, 실린 옥텟을 해석하게 하는 표현 메타데이터와 검증자, 요청의 뜻을 정하는 메서드 여덟과 그 공통 속성인 안전성과 멱등성과 캐시 가능성, 요청과 응답의 맥락을 알리는 컨텍스트 필드, 개별 방식이 아니라 챌린지와 크리덴셜의 자리만 정하는 인증 틀, 여러 표현 중 하나를 고르게 하는 콘텐츠 협상, 그리고 메서드를 적용하기 전에 조건을 시험하는 조건부 요청과 표현의 일부만 받는 범위 요청
generated: { by: "claude-opus-5", at: "2026-09-07T16:00:00Z" }
---

# HTTP 의미론

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **RFC 9110이 정의하는 것** — 곧 HTTP 버전을 넘어
바뀌지 않는 의미론 — 이 사는 자리다. 특정 버전의 전송 형식(HTTP/1.1의 메시지 구문, HTTP/2와 3의
프레이밍)과 캐시 동작의 규범은 각각 다른 문서가 정본이고, 이 허브의 페이지들은 그 경계를 만날 때마다
"그쪽은 저 문서가 맡는다"고만 적는다.

읽는 순서는 원전의 구조를 따른다. 먼저 낱말을 정하고, 그 낱말이 실려 다니는 그릇인 필드와 메시지를
보고, 그 메시지가 어디로 가는지의 라우팅을 지나, 실려 온 옥텟을 무엇으로 해석하는지의 표현에 닿는다.
거기까지가 "무엇이 오가는가"이고, 그다음이 "무엇을 하려는 것인가"인 메서드다. 마지막이 그 요청과
응답을 둘러싼 맥락을 알리는 필드들이다.

이 허브의 페이지들이 서술하는 프로토콜을 설계 원칙 쪽에서 다루는 것은
[웹 서비스와 REST](../concepts/web-services-and-rest.md)이고, 그 페이지는
[인코딩과 진화](encoding-and-evolution.md) 허브의 데이터플로 절에 산다.

## 정의와 개념

- [HTTP의 정의와 문서의 범위](../concepts/http-definition-and-scope.md) — HTTP를 무상태 요청/응답
  프로토콜 가족으로 정의하는 문장과, 의미론·캐싱·HTTP/1.1 메시징 구문이 세 문서로 갈라선 분업
- [자원과 표현](../concepts/http-resources-and-representations.md) — 요청의 대상이면 자원이고
  주고받는 것은 자원 자체가 아니라 표현이라는 정의, 그리고 선택된 표현
- [HTTP 클라이언트와 서버와 무상태성](../concepts/http-clients-servers-and-statelessness.md) —
  참여자가 연결마다의 역할이라는 것과 무상태의 정확한 뜻, 요청·응답 메시지의 구조
- [HTTP 중개자](../concepts/http-intermediaries.md) — 프록시와 게이트웨이와 터널을 가르는 기준,
  방향 어휘 넷, 그리고 캐시의 정의만 여기 있고 규범은 캐싱 명세에 있다는 분업
- [HTTP 준수 요건과 오류 처리](../concepts/http-conformance-and-error-handling.md) — 요건이
  역할에 걸리는 방식과, 오류 처리 기제를 일부러 명세하지 않은 결정
- [HTTP 버전 번호와 의미론의 분리](../concepts/http-version-numbering.md) — 두 자리가 각각
  선언하는 것과, 핵심 의미론은 버전을 넘어 바뀌지 않는다는 진술
- [http와 https URI 스킴과 정규화](../concepts/http-uri-schemes-and-normalization.md) — 두 스킴의
  기본 포트와 보안 요건, 스킴 기반 정규화 네 규칙과 동등성이 거는 URI 설계 제약
- [오리진과 권위 있는 접근](../concepts/http-origin-and-authoritative-access.md) — 스킴·호스트·
  포트 세 값의 조와, 어떤 서버가 이 URI에 답할 자격이 있는가의 판정

## 필드와 메시지

- [HTTP 필드의 문법과 결합](../concepts/http-field-syntax-and-combining.md) — 같은 이름의 필드 줄이
  콤마로 이어져 하나의 값이 되는 규칙과 순서가 뜻을 바꾼다는 귀결
- [HTTP 필드 값의 공통 문법 규칙](../concepts/http-field-common-rules.md) — 토큰·공백 세 종류·인용
  문자열·코멘트·파라미터와 리스트 확장 문법
- [HTTP 날짜 형식](../concepts/http-date-formats.md) — 수신자는 세 형식을 다 받고 송신자는 하나만
  만든다는 비대칭, 그리고 Date 필드
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

## 표현

- [표현 메타데이터](../concepts/http-representation-metadata.md) — Content-Type과 Content-Encoding의
  두 겹 모델, Content-Language와 Content-Length와 Content-Location
- [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md) — 강한
  검증자와 약한 검증자의 구분과 두 비교 함수

## 메서드

- [HTTP 요청 메서드의 지위](../concepts/http-request-methods-overview.md) — 메서드 토큰이 요청
  의미론의 일차 출처라는 규정, 표준 메서드 여덟의 목록, 모르는 메서드와 막힌 메서드의 갈림
- [안전한 메서드와 멱등한 메서드와 캐시 가능한 메서드](../concepts/http-safe-idempotent-and-cacheable-methods.md)
  — 세 공통 속성의 정의와 여덟 메서드의 배정, 안전이 구현의 부작용을 금지하지 않는다는 것
- [멱등성과 자동 재시도의 규범](../concepts/http-idempotency-and-automatic-retry.md) — 끊긴 요청을
  다시 보내도 되는지의 판정과 프록시에 걸린 절대 금지, 그리고 중복 제거 수단을 정의하지 않은 자리
- [GET과 HEAD](../concepts/http-get-and-head.md) — 선택된 표현의 전송을 요청한다는 정의와 콘텐츠를
  뺀 판본이 어디까지 같아야 하는가
- [POST와 PUT](../concepts/http-post-and-put.md) — 자원별 처리와 상태 대치라는 의도의 차이, PUT이
  이후의 관측을 보장하지 않는다는 단서
- [DELETE와 CONNECT와 OPTIONS와 TRACE](../concepts/http-delete-connect-options-and-trace.md) —
  URI 매핑의 연결 해제, 터널 개설과 그 위험, 별표 요청 대상, 요청의 되비춤

## 컨텍스트 필드

- [요청 컨텍스트 필드](../concepts/http-request-context-fields.md) — Expect와 100-continue의 양쪽
  요건, From, Referer와 그것이 새는 정보, TE, User-Agent와 지문 채취
- [응답 컨텍스트 필드](../concepts/http-response-context-fields.md) — Allow, 201과 3xx에서 뜻이
  갈리는 Location, 언제 다시 오라는 Retry-After, 그리고 Server

## 인증 틀

- [HTTP 인증 틀](../concepts/http-authentication-framework.md) — 이 문서가 개별 인증 방식이 아니라
  챌린지와 크리덴셜의 자리만 정한다는 것과, 오리진과 realm이 함께 긋는 보호 공간
- [HTTP 인증 필드](../concepts/http-authentication-fields.md) — 챌린지와 크리덴셜과 마무리 정보를
  나르는 여섯 필드, 그리고 원 서버 쪽과 프록시 쪽이 미치는 범위의 차이

## 콘텐츠 협상

- [콘텐츠 협상](../concepts/http-content-negotiation.md) — 서버가 고르는 사전 협상과 사용자
  에이전트가 고르는 반응 협상과 이후 요청을 유도하는 요청 콘텐츠 협상, 그리고 각각이 잃는 것
- [콘텐츠 협상 필드와 품질 값](../concepts/http-content-negotiation-fields.md) — 선호에 가중치를
  매기는 문법과 Accept 계열 네 필드, 그리고 협상의 결과를 표기하는 Vary

## 조건부 요청과 범위 요청

- [조건부 요청과 전제 조건 필드](../concepts/http-conditional-requests-and-preconditions.md) —
  메서드를 적용하기 전에 시험할 조건을 붙이는 다섯 필드와 각각의 판정 규칙
- [전제 조건의 평가 시점과 순서](../concepts/http-precondition-evaluation-order.md) — 조건이 둘
  이상일 때의 여섯 단계와, 갱신 손실 방지가 캐시 검증보다 앞서는 이유
- [범위 요청](../concepts/http-range-requests.md) — 표현의 일부만 달라는 Range와 어느 부분인지를
  알리는 Content-Range, 그리고 구현하지 않아도 상호운용이 깨지지 않게 만든 설계

---
type: synthesis
title: HTTP 의미론
description: HTTP의 현행 원전(RFC 9110, STD 97)에서 나온 페이지들의 진입점 — 자원과 표현과 무상태와 중개자라는 어휘, 실린 옥텟을 해석하게 하는 표현 메타데이터와 검증자, 개별 방식이 아니라 챌린지와 크리덴셜의 자리만 정하는 인증 틀, 여러 표현 중 하나를 고르게 하는 콘텐츠 협상, 메서드를 적용하기 전에 조건을 시험하는 조건부 요청과 표현의 일부만 받는 범위 요청, 응답의 결과를 세 자리 수로 말하는 상태 코드 다섯 클래스, 새 버전 없이 능력을 더하는 확장점과 레지스트리, 그리고 이 프로토콜을 쓰는 쪽이 조심할 것들. 메시지와 필드, 그리고 메서드는 자식 허브가 맡는다
generated: { by: "claude-opus-5", at: "2026-09-07T22:05:00Z" }
---

# HTTP 의미론

**이름의 범위가 곧 이 허브의 범위다.** 여기는 **RFC 9110이 정의하는 것** — 곧 HTTP 버전을 넘어
바뀌지 않는 의미론 — 이 사는 자리다. 특정 버전의 전송 형식(HTTP/1.1의 메시지 구문, HTTP/2와 3의
프레이밍)과 캐시 동작의 규범은 각각 다른 문서가 정본이고, 이 허브의 페이지들은 그 경계를 만날 때마다
"그쪽은 저 문서가 맡는다"고만 적는다.

원전이 크므로 두 덩어리는 자식 허브로 갈라 두었다. 메시지와 필드가 하나이고 메서드가 다른 하나다.
여기 남은 것은 그 둘 밖의 것 — 낱말을 정하는 개념, 실린 것을 해석하게 하는 표현, 인증과 협상과
조건부·범위, 응답 쪽의 상태 코드, 그리고 확장과 보안이다.

읽는 순서는 원전의 구조를 따른다. 먼저 낱말을 정하고, 그 낱말이 실려 다니는 그릇인 필드와 메시지를
보고(자식 허브), 실려 온 옥텟을 무엇으로 해석하는지의 표현에 닿는다. 거기까지가 "무엇이 오가는가"이고,
그다음이 "무엇을 하려는 것인가"인 메서드(자식 허브)와 "그래서 어떻게 되었는가"인 상태 코드다.

이 허브의 페이지들이 서술하는 프로토콜을 설계 원칙 쪽에서 다루는 것은
[웹 서비스와 REST](../concepts/web-services-and-rest.md)이고, 그 페이지는
[인코딩과 진화](encoding-and-evolution.md) 허브의 데이터플로 절에 산다.
같은 페이지가 REST를 쓰는 쪽의 규정과 채점도 함께 갖는다 — 자원과 표현의 분리,
HTTP 동사가 모든 자원에서 같게 행동한다는 조항, 그리고 HATEOAS가 실무에서 거의 쓰이지
않는다는 2021년 마이크로서비스 실무서의 판정이다.

**이 프로토콜 위에 얹은 응용 계약의 판을 가르는 일은 이 허브 밖이다.** URI에 `/v1/`을 두는가
요청 헤더에 판 번호를 두는가, 그리고 옛 엔드포인트를 언제까지 살려 두는가는
[계약을 깨는 변경의 관리](../concepts/managing-breaking-api-changes.md)가 갖는다 — 이 허브의
[HTTP 버전 번호와 의미론의 분리](../concepts/http-version-numbering.md)가 다루는 것은
**프로토콜 자신의 판**이라 층이 다르다.

## 자식 허브

- [HTTP 메시지와 필드](http-messages-and-fields.md) — 필드의 문법과 결합, 버전 무관한 네 부분의
  메시지, 대상을 정하고 중개자를 지나는 라우팅, 그리고 요청과 응답의 맥락을 알리는 컨텍스트 필드
- [HTTP 메서드 의미론](http-method-semantics.md) — 요청의 뜻을 정하는 메서드 토큰의 지위와 표준
  여덟의 정의, 그리고 안전성과 멱등성과 캐시 가능성

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

## 표현

- [표현 메타데이터](../concepts/http-representation-metadata.md) — Content-Type과 Content-Encoding의
  두 겹 모델, Content-Language와 Content-Length와 Content-Location
- [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md) — 강한
  검증자와 약한 검증자의 구분과 두 비교 함수

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

## 상태 코드

- [HTTP 상태 코드의 다섯 클래스와 확장 규칙](../concepts/http-status-codes-and-classes.md) — 세
  자리 수의 첫 자리가 클래스를 정한다는 것과, 모르는 코드를 그 클래스의 x00으로 취급하라는 요건
- [정보 응답 1xx와 성공 2xx](../concepts/http-informational-and-successful-status-codes.md) —
  최종 응답보다 먼저 오는 잠정 응답과, 성공을 알리는 코드들이 서로 갈리는 지점
- [리다이렉션 3xx와 메서드 보존](../concepts/http-redirection-status-codes.md) — 다시 보낼 요청을
  만드는 다섯 단계와, 어느 코드가 메서드를 지키고 어느 코드가 바꿔도 되는가
- [클라이언트 오류 4xx](../concepts/http-client-error-status-codes.md) — 요청 자체의 문제와 자원
  쪽의 문제와 인증과 전제 조건을 가려 말하는 코드들
- [서버 오류 5xx와 과부하 신호](../concepts/http-server-error-status-codes.md) — 서버가 이행하지
  못했다는 말의 갈래들과, 부하 차단의 신호가 되는 503과 Retry-After

## 확장

- [HTTP의 확장점과 레지스트리](../concepts/http-extension-points-and-registries.md) — 새 버전 없이
  능력을 더하는 자리들과 레지스트리 일곱, 그리고 새 메서드와 새 상태 코드와 새 인증 스킴에 걸리는 것
- [새 HTTP 필드를 정의할 때](../concepts/http-new-field-design.md) — 가장 널리 쓰이는 확장점의
  이름과 값 규칙, X- 접두를 쓰지 말라는 조문

## 보안

- [HTTP 보안 고려](../concepts/http-security-considerations.md) — 권위와 중개자와 로그와 URI와
  지문 채취까지, 원전이 열거하는 열여섯 갈래 가운데 결정에 걸리는 것들

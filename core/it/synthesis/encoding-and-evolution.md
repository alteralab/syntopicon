---
type: synthesis
title: 인코딩과 진화
description: 데이터를 바이트로 바꾸는 형식들과 그 형식이 버전을 넘어 살아남는 방법을 모으는 허브 — 두 방향의 호환성, 텍스트와 스키마 기반 이진 형식, 그리고 데이터베이스·서비스·워크플로·메시지라는 네 가지 데이터플로
generated: { by: "claude-opus-5", at: "2026-08-14T23:00:00Z" }
---

# 인코딩과 진화

인메모리 객체를 바이트로 바꾸는 일은 형식 선택처럼 보이지만 실은 배포 방식의 문제다. 옛 코드와
새 코드가 함께 도는 동안 무엇이 깨지지 않아야 하는가가 형식을 고른다. 첫 절이 그 요구를 정의하고,
둘째 절이 그 요구를 지고 가는 형식들을, 셋째 절이 그 형식이 실제로 흐르는 자리들을 맡는다.

## 요구

- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 두 방향의 정의,
  롤링 업그레이드, 알 수 없는 필드를 잃는 사고, 인코딩과 디코딩이라는 낱말

## 형식

- [데이터 인코딩 형식](../concepts/data-encoding-formats.md) — 언어 내장 직렬화의 결함,
  JSON·XML·CSV의 문제, JSON Schema, 이진 JSON 변형, 스키마가 주는 네 가지 성질
- [프로토콜 버퍼와 필드 태그](../concepts/protocol-buffers-encoding.md) — 필드 번호가 정하는
  진화 규칙과 태그를 영원히 재사용할 수 없다는 제약
- [Avro의 기록자 스키마와 독자 스키마](../concepts/avro-writer-and-reader-schema.md) — 태그 없이
  이름으로 맞추는 스키마 해소, 기본값 규칙, 동적 생성 스키마
- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) —
  스키마를 레코드에서 떼어 내 버전으로 관리하는 실물

## 데이터플로

- [데이터베이스를 거치는 데이터플로](../concepts/dataflow-through-databases.md) — 데이터가 코드보다
  오래 살고 마이그레이션이 미뤄지는 자리
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 서비스 API의 정의·IDL·프레임워크와
  API 버저닝
- [소비자 주도 계약](../concepts/consumer-driven-contracts.md) — 서비스 계약을 제공자·소비자·
  소비자 주도 셋으로 가르고, 소비자가 자기가 쓰는 것만 단정으로 적게 해 제공자가 무엇을 뺄 수
  있는지 알게 만드는 2006년의 패턴. 실무자 에세이라 근거가 아니라 정의다
- [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md) — 위치 투명성이
  실패하는 여섯 지점
- [서비스 디스커버리와 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md) —
  주소를 찾고 부하를 나누는 다섯 가지 해법
- [내구 실행과 워크플로](../concepts/durable-execution-and-workflows.md) — 서비스 여럿에 걸친
  단계를 정확히 한 번 굴리려는 시도와 그 대가
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 브로커를 사이에 두는 비동기
  흐름과 큐·토픽 두 패턴
- [분산 액터 프레임워크](../concepts/distributed-actor-frameworks.md) — 브로커와 프로그래밍 모델을
  한 프레임워크로 합친 쪽

## HTTP 의미론

위 데이터플로의 웹 서비스 쪽이 전제하는 프로토콜의 원전(RFC 9110, STD 97)에서 나온 페이지들이다.

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
- [요청 대상과 Host](../concepts/http-target-uri-and-host.md) — 대상 URI를 정하고 실어 보내고 다시
  재구성하는 경로, 그리고 잘못 보내진 요청의 거절
- [HTTP 메시지 전달과 hop-by-hop 필드](../concepts/http-message-forwarding-and-hop-by-hop-fields.md)
  — Connection이 가르는 종단 간 필드와 다음 수신자까지만 가는 필드, Via와 Max-Forwards와 Upgrade
- [표현 메타데이터](../concepts/http-representation-metadata.md) — Content-Type과 Content-Encoding의
  두 겹 모델, Content-Language와 Content-Length와 Content-Location
- [검증자와 ETag와 Last-Modified](../concepts/http-validators-etag-and-last-modified.md) — 강한
  검증자와 약한 검증자의 구분과 두 비교 함수

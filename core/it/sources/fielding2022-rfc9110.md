---
type: standard
title: "HTTP Semantics"
author:
  - { family: Fielding, given: "Roy T." }
  - { family: Nottingham, given: Mark }
  - { family: Reschke, given: Julian }
issued: "2022-06"
number: "RFC 9110"
collection-title: "STD 97"
authority: "IETF"
publisher: "RFC Editor"
URL: "https://www.rfc-editor.org/rfc/rfc9110.html"
snapshot: /it/archive/fielding2022-rfc9110/
snapshot_sha256: "98bfe72c1dec5bd272cc1c6d1f702bce68b7e1ecb977cbe558f40d02d7654b14"
accessed: "2026-09-07"
---

# HTTP Semantics (RFC 9110)

HTTP 의미론의 현행 Internet Standard(STD 97). 메서드의 안전성·멱등성, 필드, 표현, 조건부 요청,
범위 요청, 상태 코드, 인증 틀, 확장 방식을 정의한다. RFC 2818·7230–7233·7235·7538·7615·7694를 폐기한다
(캐싱은 RFC 9111이 7234를 폐기해 맡음). 2026-09-07 datatracker 기준 이 문서를 갱신·폐기하는 RFC는 없다.

KB 안의 자리: "멱등" 49건 언급의 정박점. 어느 메서드가 재시도 가능한가, 상태 코드의 뜻이 무엇인가의 규범.
POST 중복 제거(멱등 키 저장·중복 payload)는 이 문서 밖의 별도 계약이고, 캐시 동작은 RFC 9111 영역이다.
편집자 3인이 저자란에 있다(Ed.).

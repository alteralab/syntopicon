---
type: concept
title: API 설계 모범 사례
status: draft
description: 설계 패턴이라는 낱말의 규정과 이 장이 그 패턴들에 주는 지위 — 스타일과 무관하게 공통인 도전이 있다는 전제와 요리책 형식, 블로흐의 격언 둘(좋은 API는 자산이고 나쁜 API는 악몽이라는 것과 API 설계는 과학이 아니라 기예라는 것)과 저자들이 그것을 네트워크 기반 API로 옮겨 읽는 방식, 대상 맞춤·직관·유지보수 가능·문서화·오용하기 어려움·테스트 가능·안전·효율·오류 전달이라는 아홉 모범 사례, 압축·인코딩·캐싱·하드웨어·속도 제한이라는 성능 팁 다섯과 각각이 되사는 대가, 그리고 패턴은 규칙이 아니라 지침이라는 장의 결론
generated: { by: "claude-fable-5", at: "2026-09-18T23:30:00Z" }
sources:
  - { id: dynowski2025, resource: /it/sources/dynowski2025.md }
---

# API 설계 모범 사례

- [버전 조건](#버전-조건)
- [설계 패턴이라는 낱말](#설계-패턴이라는-낱말)
- [이 장이 답하려는 물음들](#이-장이-답하려는-물음들)
- [블로흐의 격언과 그 옮겨 읽기](#블로흐의-격언과-그-옮겨-읽기)
- [모범 사례 아홉](#모범-사례-아홉)
- [성능을 올리는 다섯 손잡이](#성능을-올리는-다섯-손잡이)
- [규칙이 아니라 지침이다](#규칙이-아니라-지침이다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **잘 설계된 네트워크 기반 API는 무엇을 만족하며, 그 패턴 목록은 어떤 지위를
갖는가.**

## 버전 조건

> **버전 조건**: 이 페이지가 드는 제품과 형식 이름(Protocol Buffers·Avro·gzip·Brotli·
> GraphQL·HATEOAS)은 **2025년 저술 시점**의 것이다. 모범 사례 아홉과 성능 손잡이 다섯의
> 성격은 시점에 매이지 않는다.

## 설계 패턴이라는 낱말

- 장의 자리부터 적힌다 — **이 장은 API 수명 주기의 설계 단계를 위한 실무 안내**이고, **API 설계
  패턴·API 보안 패턴·API 모범 사례 같은 흔한 API 주제에 대한 인식을 높이는 것**을 목표로 한다
  (2장 머리말, p.41).[^dynowski2025]
- 규정 (2장, p.41).[^dynowski2025]

  > A software design pattern is a blueprint for solving a particular, commonly occurring
  > problem when creating software.

- 그 규정이 이 장의 존재 근거로 이어진다 — **API를 설계하는 것은 다차원적 과정이지만 어떤
  도전들은 API 스타일과 무관하게 공통이다. 설계 패턴이 그 도전들에 대한 해법의 개발을 안내할 수
  있다** (2장, p.41).[^dynowski2025]
- 제시 형식도 명시된다 — **이 장은 그 패턴들을 하나씩, 요리책 같은 형식으로 제시해 당신이
  그것들을 고르고 자기 설계 과정에 통합하는 것을 돕는다.** 실제 적용은 5장에서 예제 REST API를
  지으며 보인다 (2장, p.41).[^dynowski2025]

## 이 장이 답하려는 물음들

- 절의 입구에서 물음이 열거된다 — **어떤 API 스타일로 작업하든 다음과 같은 물음에 답해야
  한다** (2장 §"Examples of API Design Patterns", p.41).[^dynowski2025]
  - **API 문서에 어떤 자연어를 쓸 것인가**
  - **API를 어떻게 버저닝할 것인가**
  - **인터페이스의 이름을 어떻게 지을 것인가**
  - **어떤 인코딩을 쓸 것인가**
  - **데이터를 어떻게 서빙할 것인가**
- 더 공부할 곳으로 저자들이 드는 것이 **JJ Geewax의 *API Design Patterns*(Manning, 2021)** 과
  **구글의 API 설계 지침, 마이크로소프트의 REST API 설계 지침, The REST API Tutorial과
  Learn REST API Design 개관**이다 (2장, p.41).[^dynowski2025] 이 KB는 그 가운데 어느 것도
  원전으로 갖고 있지 않다.

## 블로흐의 격언과 그 옮겨 읽기

- 저자들은 모범 사례를 자기 목록으로 시작하지 않고 남의 격언을 먼저 놓는다 — **조슈아 J.
  블로흐의 "How to Design a Good API and Why It Matters" 글이 API 설계에 관한 격언 묶음을
  담고 있고**, **그 격언들이 소프트웨어 라이브러리의 관점에서 진술되었지만 네트워크 기반 API를
  포함한 넓은 범위의 API에 적용 가능하다**고 적는다 (2장 §"API Design Best Practices",
  p.73).[^dynowski2025]
- 왜 좋은 API 설계가 중요한가에 대한 답 (2장, p.73).[^dynowski2025]

  > APIs can be among your greatest assets or liabilities. Good APIs create long-term
  > customers; bad ones create long-term support nightmares.
  >
  > Public APIs, like diamonds, are forever. You have one chance to get it right so give it
  > your best.
  >
  > All programmers are API designers. Good programs are modular, and intermodular
  > boundaries define APIs. Good modules get reused.
  >
  > —Joshua J. Bloch, 2006

- 저자들이 그것을 네트워크 기반 API의 공간으로 옮겨 읽는다 (2장, p.73).[^dynowski2025]
  - **이십 년 전 블로흐는 API가 고객을 마주하는 자산이라는 것을 알아차렸고, 오늘 우리는 API를
    잘 설계되면 비용 효율적일 수 있는 제품으로 다룬다.**
  - **API 설계가 중요한 이유는 API가 한 번 프로덕션에 들어가면 그것을 바꿀 능력이 제한되고,
    형편없이 설계된 API를 유지보수하는 것이 악몽이기 때문이다.**
  - **API는 모듈들(엔드포인트·프로시저·필드 따위)로 지어지고, 각 모듈은 재사용 가능한 기능을
    제공하며 API가 존재하는 동안 내내 가도록 설계된다.**

## 모범 사례 아홉

- **네트워크 기반 API 설계를 위한 고수준 모범 사례의 선별**로 아홉이 열거된다 (2장,
  pp.74–75).[^dynowski2025]
  - **대상에 맞춘(Tailored to the audience)** — API가 클라이언트의 필요에 맞게 설계된다.
    클라이언트는 웹 브라우저·모바일 기기·스마트워치·IoT 기기·AI 에이전트 따위일 수 있다.
    **어떤 API 스타일은 다른 스타일보다 클라이언트의 필요에 맞추는 유연성이 크다** — 예로 드는
    것이 클라이언트가 원하는 형식으로 데이터를 요청하게 하는 GraphQL이다.
  - **직관적인(Intuitive)** — **직관적인 API는 문서 없이도 항해할 수 있다.** 예로 드는 것이
    **HATEOAS를 갖춘 REST API**이고, **응답이 관련 자원과 허용되는 동작으로 가는 링크를 담기
    때문**이다.
  - **유지보수 가능한(Maintainable)** — **유지보수 가능한 API는 클라이언트를 어지럽히지 않고
    진화한다.** 방법이 둘이다 — **후진 호환 변경을 하거나, 버저닝으로 깨는 변경을 알리는 것.**
  - **문서화된(Documented)** — **API에는 문서가 딸린다. 문서의 존재가 API의 사용성과 채택에
    영향을 주고, 문서의 부재가 그 사용을 방해할 수 있다.**
  - **오용하기 어려운(Hard to misuse)** — **API가 최소 놀람의 원칙을 따른다**는 뜻이고,
    **간단한 일은 곧바로 되고, 복잡한 일은 달성 가능하며, 오류는 내기 어려워야 한다**는 것이다.
    이 원칙은 **표준적인 설계 관행과 오류 메시지와 데이터 검증을 써서 개발자에게 예측 가능한
    경험을 주는 API를 만드는 것을 돕는다.**
  - **테스트 가능한(Testable)** — **API 개발자나 사용자가 자기가 짓거나 쓰는 API를 테스트할
    수단을 가져야 한다.** **설정 때문에 API 테스트가 불가능하면 실제 API를 대신할 알맞은 모의
    API가 쓰여야 한다.**
  - **안전한(Secure)** — **API는 당신의 체계로 들어가는 관문이다.** 요구가 넷이다 — **입력은
    API 취약점을 악용할 위험을 줄이도록 검증되어야 하고, 출력은 민감 정보를 노출해서는 안
    되며, API가 쓰는 라이브러리와 외부 서비스는 최신 보안 패치로 갱신되어야 하고, 안전한 API는
    중복 요청을 다루고 들어오는 요청의 바람직하지 않은 과잉을 억누를 수 있다.**
  - **효율적인(Efficient)** — **API는 체계 자원의 사용을 최소화하려 애쓴다.** **클라이언트가
    응답을 맞춤할 수 있게 하면 API가 데이터 전송을 줄이고 자원 사용을 최적화할 수 있다.**
    수단으로 드는 것이 **필드 필터링**(REST의 희소 필드셋 같은)과 **GraphQL 같은 질의 지향
    API**다.
  - **오류를 전달하는(Communicates errors)** — **API는 자기 스타일에 알맞은 표준 오류 코드로
    자기 상태를 전달한다.** **REST API는 HTTP 상태 코드를, gRPC API는 gRPC 상태 코드를
    쓴다.** 거기에 더해 **API는 문제를 해결할 맥락과 안내를 주는 사람이 읽을 수 있는 오류
    메시지를 제공한다. 표준 오류 코드와 서술적 메시지의 이 결합이 개발자가 운영상의 문제를
    이해하고 다루는 것을 돕는다.**

## 성능을 올리는 다섯 손잡이

- 곁글 하나가 API 성능을 올리는 팁 다섯을 든다. **각 항목마다 되사는 대가가 같이 적혀
  있다는 것이 이 목록의 성격**이다 (2장 곁글 §"General Tips to Improve API Performance",
  p.75).[^dynowski2025]
  - **압축** — **gzip이나 Brotli 같은 알맞은 데이터 압축 알고리즘을 고르면 API 응답의 크기가
    줄어 네트워크로 데이터를 더 빨리 옮길 수 있다. 더 작은 적재물이 성능을 개선하며 특히 대역폭이
    제약된 조건에서 그렇다.** 대가는 **압축이 CPU 사용을 늘리므로 API 설계자가 계산 비용과
    대역폭 비용의 균형을 잡아야 한다**는 것이다.
  - **인코딩** — **인코딩 형식이 API 성능에 영향을 준다. Protocol Buffers와 Avro 같은 이진
    형식이 JSON과 XML 같은 텍스트 기반 형식보다 크기와 처리 속도에서 대체로 낫다.** 대가는
    **텍스트 기반 형식이 디버깅이나 사람의 가독성에는 더 나을 수 있다**는 것이다.
  - **캐싱** — **API 앞에 캐시를 두면 API가 기대는 데이터베이스나 저장소 같은 자원의 사용이
    줄어든다.** 대가가 셋이다 — **메모리 사용이 늘고**, **데이터 원천과 동기화되지 않으면
    캐시된 데이터가 낡거나 소실될 수 있으며**, **개발과 운영 비용이 늘어난다.**
  - **하드웨어** — **수직 확장(더 많은 CPU·메모리·저장을 주는 인스턴스로 교체하거나
    업그레이드하는 것)이 체계 성능을 개선할 수 있다.** 대가가 둘이다 — **이 방법이 성능 문제의
    밑에 있는 원인을 가릴 수 있고**, **하드웨어 확장에는 한계가 있어 그 지점을 넘으면 수평
    확장(하드웨어를 더 붙이는 것)이 필요해진다.**
  - **API 속도 제한** — **주어진 시간 구간 안에 클라이언트당 API 요청 수를 제한하면 남용이 줄고
    백엔드 자원이 보호된다.**

## 규칙이 아니라 지침이다

- 블로흐의 격언 묶음이 끝나는 자리를 저자들이 그대로 자기 결론으로 쓴다 — 그 마지막 격언이
  **설계 격언이나 패턴이 규칙이 아니라 안내가 되도록 의도되었다**고 말한다는 것이다 (2장,
  p.73).[^dynowski2025]

  > API design is an art, not a science. Strive for beauty, and trust your gut. Do not adhere
  > slavishly to the above heuristics, but violate them only infrequently and with good
  > reason.
  >
  > —Joshua J. Bloch, 2006

- 장의 요약이 같은 것을 되풀이하며 범위도 한 번 더 긋는다 (2장 §"Summary",
  p.76).[^dynowski2025]
  - **이 장이 서술한 API 설계 패턴들은 REST API에 초점을 두지만 다른 API 스타일에도 적용될 수
    있다.**
  - **탐색된 API 보안 패턴들 — 암호화, 인증과 인가, 데이터 검증 — 도 여러 API 스타일에 걸쳐
    공통이다.**
  - 그리고 결론 — **이 장에서 가져갈 것은, API 설계자인 당신이 고를 수 있는 설계 패턴이 많이
    존재하지만 그것들은 규칙이 아니라 안내가 되도록 의도되었다는 것이다.**

## 이어지는 페이지

- [API 수명 주기](../concepts/api-lifecycle.md) — 이 장이 안내한다고 밝히는 그 설계 단계
- [API 이름과 버저닝](api-naming-and-versioning.md) — 위 물음 가운데 자연어·이름·버저닝
- [API 적재물 필드 설계 규약](api-payload-field-conventions.md) — 위 물음 가운데 인코딩
- [API 목록 조회 패턴](api-list-query-patterns.md) — 위 물음 가운데 데이터를 서빙하는 법
- [API 요청 수명 패턴](api-request-lifecycle-patterns.md) — 위 "안전한" 항목이 말하는 중복
  요청과 과잉 억제
- [API 자원 삭제 패턴](api-resource-deletion-patterns.md) — 같은 장이 다루는 삭제 쪽
- [API 보안 패턴](api-security-patterns.md) — 위 "안전한" 항목의 전문
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 아홉 가운데 여럿이 속성으로
  다뤄지는 허브
- [분산 체계에서의 캐싱](../concepts/caching-in-distributed-systems.md) — 위 캐싱 손잡이의 전문
- [데이터 인코딩 형식](../concepts/data-encoding-formats.md) — 위 인코딩 손잡이의 전문
- [확장의 네 축](../concepts/four-axes-of-scaling.md) — 위 하드웨어 손잡이가 놓이는 축
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 위 HATEOAS가 사는 자리

[^dynowski2025]: Dynowski & Dulak 2025, *Learning API Styles* 초판(O'Reilly, 2025) 2장
    "API Design Patterns" — 장 머리말(p.41)과 §"Examples of API Design Patterns"의 도입
    문단(p.41), §"API Design Best Practices"(pp.73–75, 곁글 §"General Tips to Improve API
    Performance"(p.75) 포함), §"Summary"(p.76). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 28, 실측).
    직인용 셋(설계 패턴의 규정, 블로흐 인용 둘)은 `pdftotext -layout` 추출로 문자 단위
    대조했고, 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었으며 굽은 따옴표는 곧은
    따옴표로 옮겼다. 블로흐 인용 첫째 블록은 원문에서 문단 셋으로 조판되어 있어 빈 줄로 갈라
    옮겼다. 이 절들에 코드 목록과 도판은 없다. 저자들이 대는 바깥 서지(Joshua Bloch,
    "How to Design a Good API and Why It Matters", *Companion to the 21st ACM SIGPLAN
    Symposium on OOPSLA*(2006): 506–507, JJ Geewax *API Design Patterns*, 구글·마이크로소프트의
    API 설계 지침, The REST API Tutorial, Learn REST API Design, Ilya Grigorik
    *High Performance Browser Networking*)는 **이 KB가 확인한 원전이 아니라 이 책을 통한
    2차 경유**다.

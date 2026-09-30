---
type: synthesis
title: 조직 실천으로서의 문서화
description: 문서 품질을 개인의 글솜씨가 아니라 조직의 소유와 절차 문제로 두는 쪽을 모으는 자식 허브 — 문서에 소유와 정본과 리뷰와 수명을 거는 절차, 그리고 누구에게 무엇을 어떤 유형으로 쓰는가.
generated: { by: "claude-opus-5", at: "2026-09-30T00:00:00Z" }
---

# 조직 실천으로서의 문서화

- [이 허브의 범위](#이-허브의-범위)
- [절차 — 문서에 소유와 정본과 리뷰를 걸기](#절차--문서에-소유와-정본과-리뷰를-걸기)
- [대상 — 누구에게 무엇을 쓰는가](#대상--누구에게-무엇을-쓰는가)
- [이웃 허브](#이웃-허브)

## 이 허브의 범위

여기 모인 일곱은 [winters2020](../sources/winters2020-swe-at-google.md)의 문서화 장에서 왔다.
**부모 허브는 [조직과 아키텍트](organizations-and-architects.md)**이고, 그쪽은 조직과 역할을
갖는다. 여기는 **문서라는 산출물과 그것을 유지하는 절차**를 갖는다.

**이름이 형제 허브 [문서화와 코드 명료함](documentation-and-code-clarity.md)과 갈리는 자리**:
그쪽은 코드 주석과 이름과 일관성, 곧 코드 안에서 읽는 사람에게 전달되는 층을 갖는다. 여기는
**코드 밖의 산문 문서를 조직이 소유하고 유지하는** 층이다.

## 절차 — 문서에 소유와 정본과 리뷰를 걸기

- [문서를 코드처럼 다루기](../concepts/documentation-treated-as-code.md) — **먼저 읽는다.** 이
  절 전체가 서는 배치. 문서의 이익이 하류에 있다는 비대칭, 축 일곱, 그리고 문서 리뷰 세 유형
- [문서의 수명 — 신선도 날짜와 폐기](../concepts/document-freshness-and-deprecation.md) — 주기적
  평가를 날짜 한 줄로 바꿔 소스 관리와 리뷰와 알림이 다룰 수 있는 대상으로 만드는 장치
- [기술 문서 작성자를 언제 쓰는가](../concepts/technical-writer-role-and-scale.md) — 이 KB에 없던
  역할. 경계를 넘는 문서가 어려워진다는 관찰과 작성자의 결정적 역할

## 대상 — 누구에게 무엇을 쓰는가

- [문서의 독자를 가르기](../concepts/documentation-audiences-seekers-and-stumblers.md) — 이 장의
  서식 규약이 연역되는 자리. 독자를 가르는 축들과 일차 독자를 하나로 정하라는 조문
- [문서 유형과 한 문서 한 목적](../concepts/documentation-types-and-single-purpose.md) — 유형이
  소유와 정본이 걸리는 단위라는 배치와, 유형 다섯을 섞지 말라는 조문
- [설계 문서 — 착수 전 관문](../concepts/design-docs-as-a-prelaunch-gate.md) — 리뷰를 코드가
  쓰이기 전으로 당기는 수와, 양식을 전문가 호출 장치로 쓰는 배치
- [좋은 문서의 세 변수와 다섯 물음](../concepts/documentation-quality-parameters.md) — 완전성과
  정확성과 명료함이 서로를 깎는다는 저울, 그리고 품질의 판정자를 독자에게 두는 규정

## 이웃 허브

- [조직과 아키텍트](organizations-and-architects.md) — 부모 허브. 조직 구조·소유권·역할
- [문서화와 코드 명료함](documentation-and-code-clarity.md) — 형제 축. 같은 낱말이 코드 안쪽을
  가리키는 쪽
- [팀 문화와 지식 공유](team-culture-and-knowledge-sharing.md) — 형제 허브. 문서를 지식의 매체
  하나로 놓고 정본과 유인을 다루는 자리
- [코드 규칙과 변경 리뷰](code-rules-and-change-review.md) — 형제 허브. 같은 모양의 리뷰가 코드에
  걸리는 쪽
- [실용주의 철학과 접근](pragmatic-philosophy-and-approach.md) — 문서화를 개별 개발자의 실천으로
  보는 축
- [코드 검색과 훑기](code-search-and-browsing.md) — 형제 허브. 문서가 아니라 코드를 찾아 답을
  얻는 쪽

---
type: synthesis
title: 코드 검색과 훑기
description: 남이 쓴 코드를 규모 있게 찾아 훑는 일과 그 일을 받치는 도구의 설계 판단을 모으는 자식 허브 — 도구가 하는 일을 기능이 아니라 답하려는 물음으로 놓는 유형학, 색인을 어디에 둘 것인가와 무엇을 담을 것인가의 저울, 그리고 코드를 찾는 일이 텍스트를 찾는 일과 갈리는 자리.
generated: { by: "claude-opus-5", at: "2026-09-30T00:00:00Z" }
---

# 코드 검색과 훑기

- [이 허브의 범위](#이-허브의-범위)
- [무엇을 묻는가](#무엇을-묻는가)
- [그 물음에 답하는 도구를 어떻게 짓는가](#그-물음에-답하는-도구를-어떻게-짓는가)
- [이웃 허브](#이웃-허브)

## 이 허브의 범위

여기 모인 넷은 [winters2020](../sources/winters2020-swe-at-google.md)의 코드 검색 장에서 왔다.
**부모 허브는 [조직과 아키텍트](organizations-and-architects.md)**이고, 그쪽은 조직과 역할을
갖는다. 여기는 **남이 쓴 코드를 규모 있게 찾아 훑는 일**과 그 일을 받치는 도구의 설계 판단을
갖는다 — 코드를 찾는 일은 조직도 역할도 아니라서 부모의 이름 범위 밖이다.

**이름에 "읽기"를 넣지 않은 이유**: 읽기 쉽게 쓰는 쪽은
[문서화와 코드 명료함](documentation-and-code-clarity.md)이 갖고, 코드를 고쳐 가며 이해하는 쪽은
[리팩터링과 코드 냄새](refactoring-and-code-smells.md)가 갖는다. 여기는 **이미 쓰인 코드를 찾아
훑는 쪽**만 갖는다.

**형제 허브 [리뷰 도구와 정적 분석](review-tooling-and-static-analysis.md)과 갈리는 자리**: 그쪽은
절차를 집행하는 도구를 갖고, 이쪽은 물음에 답하는 도구를 갖는다.

이 장은 한 회사의 사내 도구를 소개하는 장에 가까워서, 이 KB는 도구 이름·화면 배치·조작 방식을
옮기지 않고 **도구를 바꿔도 남는 판단만** 받았다. 그 가름의 정본은 아래 첫 페이지에 있다.

## 무엇을 묻는가

- [개발자가 코드에 던지는 물음의 유형](../concepts/questions-developers-ask-about-code.md) —
  **먼저 읽는다.** 도구가 하는 일을 기능이 아니라 **답하려는 물음**으로 다시 놓는 수와 그
  물음들이 요구하는 답의 성질, 초점이 찾기에서 훑기로 옮겨 간 자리, 그리고 이 장을 가른 방식의
  정본

## 그 물음에 답하는 도구를 어떻게 짓는가

- [중앙 코드 색인과 개발자마다의 색인](../concepts/central-code-index-versus-per-developer-index.md) —
  색인을 각자의 편집기에 둘 것인가 따로 둔 중앙 도구에 둘 것인가의 논거와, 그 선택이 지는 지연
  예산
- [코드 검색의 완전성과 신뢰](../concepts/code-search-completeness-and-trust.md) — 색인에 무엇을
  담을 것인가의 저울과, 그 저울을 관통하는 잣대가 자원이 아니라 **신뢰**라는 판정
- [코드를 찾는 일은 텍스트를 찾는 일과 다르다](../concepts/searching-code-is-not-searching-text.md) —
  일반 전문 검색의 전처리가 코드에서 정보 파괴가 되는 자리와, 코드 고유의 표현력 사다리와 랭킹
  신호

## 이웃 허브

- [조직과 아키텍트](organizations-and-architects.md) — 부모 허브. 조직 구조·소유권·역할
- [리뷰 도구와 정적 분석](review-tooling-and-static-analysis.md) — 형제 허브. 같은 소스의 사내
  도구 장을 같은 잣대로 가른 쪽이고, 절차가 도구의 관문으로 굳는 층
- [엔지니어링 생산성 측정](engineering-productivity-measurement.md) — 형제 허브. 이 도구가 아끼려는
  엔지니어 시간을 무엇으로 재는가가 그쪽에 있다
- [팀 문화와 지식 공유](team-culture-and-knowledge-sharing.md) — 형제 허브. 사람과 문서를 매체로
  삼는 지식 통로들이 사는 자리
- [코드 규칙과 변경 리뷰](code-rules-and-change-review.md) — 형제 허브. 찾아낸 코드를 고칠 때
  지나는 규칙과 승인 구조
- [조직 실천으로서의 문서화](documentation-as-organizational-practice.md) — 형제 허브. 코드가 아니라
  문서를 찾을 때의 정본과 신선도
- [제품 형평성과 엔지니어링의 편향](product-equity-and-engineering-bias.md) — 형제 허브. 같은 소스가
  도구의 기본값을 편향의 통로로 읽는 쪽
- [문서화와 코드 명료함](documentation-and-code-clarity.md) — 읽기 쉽게 쓰는 쪽
- [저장 엔진](storage-engines.md) — 일반 전문 검색 색인이 사는 축. 그 기법이 코드에서 갈리는
  자리를 이 허브가 갖는다

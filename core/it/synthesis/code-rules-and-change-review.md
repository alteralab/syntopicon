---
type: synthesis
title: 코드 규칙과 변경 리뷰
description: 조직이 사람의 판단을 어디까지 규칙과 절차로 대체하고 어디부터 사람에게 남기는가를 모으는 자식 허브 — 무엇을 법으로 두고 어떻게 고치고 누가 집행하는가, 그리고 누가 무엇을 승인하고 그 절차를 어떻게 가볍게 유지하는가.
generated: { by: "claude-opus-5", at: "2026-09-30T00:00:00Z" }
---

# 코드 규칙과 변경 리뷰

- [이 허브의 범위](#이-허브의-범위)
- [규칙 — 무엇을 법으로 두고 어떻게 고치고 누가 집행하는가](#규칙--무엇을-법으로-두고-어떻게-고치고-누가-집행하는가)
- [리뷰 — 누가 무엇을 승인하고 그 절차를 어떻게 가볍게 유지하는가](#리뷰--누가-무엇을-승인하고-그-절차를-어떻게-가볍게-유지하는가)
- [이웃 허브](#이웃-허브)

## 이 허브의 범위

여기 모인 여덟은 [winters2020](../sources/winters2020-swe-at-google.md)의 스타일 규칙 장과 코드
리뷰 장에서 왔다. **부모 허브는 [조직과 아키텍트](organizations-and-architects.md)**이고, 그쪽은
조직과 역할을 갖는다. 여기는 **역할이 아니라 절차** — 규칙 쪽과 승인 쪽 — 를 갖는다.

그 절차가 도구와 데이터 모형으로 굳는 층은 형제 허브
[리뷰 도구와 정적 분석](review-tooling-and-static-analysis.md)이 갖는다.

## 규칙 — 무엇을 법으로 두고 어떻게 고치고 누가 집행하는가

- [규칙과 지침](../concepts/rules-versus-guidance.md) — **먼저 읽는다.** 어길 수 없는 법과 따르면
  좋은 권고를 문서 수준에서 가르는 배치와, 규칙이 금지가 아니라 기본값으로 작동한다는 논증
- [규칙을 세우는 다섯 원칙](../concepts/principles-for-writing-rules.md) — 무엇을 규칙으로 올릴지의
  잣대 다섯과, 규칙의 수가 아니라 기억해야 하는 수가 척도라는 읽기
- [규칙을 바꾸는 절차와 중재자](../concepts/rule-change-process-and-arbiters.md) — 법이 굳어 죽지
  않게 하는 기제. 근거를 준수가 아니라 개정을 위해 싣는 배치와 합의로 정하는 중재자
- [규칙의 집행을 도구에 내리기](../concepts/automating-rule-enforcement.md) — 집행 경로를 사회적인
  것과 기술적인 것으로 가르는 배치와, 자동화하지 않기로 한 결정과 그 근거

## 리뷰 — 누가 무엇을 승인하고 그 절차를 어떻게 가볍게 유지하는가

- [코드 리뷰의 세 승인 축](../concepts/three-approval-axes-of-code-review.md) — 승인이 하나가
  아니라 정확성·소유권·언어 자격 셋이라는 구조와, 축의 수와 사람의 수가 다르다는 가름
- [코드 소유권 — 소유가 아니라 청지기](../concepts/code-ownership-as-stewardship.md) — 둘째 축을
  떠받치는 구조. 소유자에게 요구하는 것과 요구하지 않는 것, 그리고 탈중앙 등록
- [코드 리뷰가 주는 것 — 결함 찾기 너머](../concepts/code-review-benefits-beyond-defect-finding.md) —
  이득 여섯과 그 가운데 결함 찾기가 주된 것이 아니라는 자기 판정, 그리고 설계와 이해의 비대칭
- [작은 변경과 빠른 리뷰](../concepts/small-changes-and-fast-review.md) — 의무 절차가 굳지 않게
  하는 실무. 작은 변경과 리뷰어 수와 되먹임 기한, 그리고 이것을 규칙이 아니라 최적화로 두는 조문

## 이웃 허브

- [조직과 아키텍트](organizations-and-architects.md) — 부모 허브. 조직 구조·소유권 모형·역할
- [리뷰 도구와 정적 분석](review-tooling-and-static-analysis.md) — 형제 허브. 같은 절차가 도구의
  데이터 모형과 관문으로 굳는 층
- [팀 문화와 지식 공유](team-culture-and-knowledge-sharing.md) — 형제 허브. 리더빌리티가 지식
  전수의 매체로 사는 자리
- [조직 실천으로서의 문서화](documentation-as-organizational-practice.md) — 형제 허브. 같은 리뷰가
  코드가 아닌 산출물에 걸리는 쪽
- [엔지니어링 생산성 측정](engineering-productivity-measurement.md) — 형제 허브. 이 절차의 속도가
  측정 대상이 되는 자리
- [진화와 거버넌스](evolution-and-governance.md) — 규칙 준수를 기계 검사로 묻는 축
- [코드 검색과 훑기](code-search-and-browsing.md) — 형제 허브. 고칠 코드를 먼저 찾아 훑는 쪽

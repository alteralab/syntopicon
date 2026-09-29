---
type: synthesis
title: 엔지니어링 생산성 측정
description: 엔지니어의 일과 절차 자체를 재는 물음을 모으는 자식 허브 — 재기 전에 서는 관문, 무엇을 잴지 고르는 틀, 생산성을 여러 축으로 가르는 덮개, 그리고 고른 지표가 겨누던 것을 잡는지 확인하는 일.
generated: { by: "claude-opus-5", at: "2026-09-30T00:00:00Z" }
---

# 엔지니어링 생산성 측정

- [이 허브의 범위](#이-허브의-범위)
- [잴 것인가](#잴-것인가)
- [무엇을 잴 것인가](#무엇을-잴-것인가)
- [고른 지표가 맞는가](#고른-지표가-맞는가)
- [이웃 허브](#이웃-허브)

## 이 허브의 범위

여기 모인 넷은 [winters2020](../sources/winters2020-swe-at-google.md)의 생산성 측정 장에서 왔다.
**부모 허브는 [조직과 아키텍트](organizations-and-architects.md)**이고, 형제 허브
[소프트웨어 아키텍처 지표](software-architecture-metrics.md)는 **산출물과 전달 파이프라인**을
재는 쪽을 갖는다. 여기는 **엔지니어의 일과 절차 자체를 재는** 쪽이다.

네 페이지가 각자 첫 절에서 이 소스의 수치 지위를 밝힌다.

## 잴 것인가

- [잴 가치가 있는가](../concepts/is-it-worth-measuring.md) — **먼저 읽는다.** 무엇을 잴지 고르기
  전에 재는 일 자체의 값어치를 묻는 관문과, 지표를 개인 평가에 쓰지 말라는 금칙

## 무엇을 잴 것인가

- [목표-신호-지표 틀](../concepts/goals-signals-metrics-framework.md) — 재기로 정한 뒤 무엇을
  잴지 고르는 세 층과, 측정의 공백이 지워지지 않고 목록으로 남는 배치
- [QUANTS — 생산성의 다섯 축](../concepts/quants-productivity-dimensions.md) — 목표 목록의 덮개.
  정확한 지표로도 잘못된 결론에 갈 수 있고 그 위험이 무엇을 목표로 적었는가에 있다는 논증

## 고른 지표가 맞는가

- [정성 지표와 지표의 검증](../concepts/qualitative-metrics-and-validation.md) — 고른 지표가
  겨누던 신호를 잡는지 사람에게 물어 확인하는 일과 그 방법이 드러낸 것

## 이웃 허브

- [조직과 아키텍트](organizations-and-architects.md) — 부모 허브. 조직 구조·소유권·역할
- [소프트웨어 아키텍처 지표](software-architecture-metrics.md) — 형제 축. 산출물과 전달을 재는
  쪽이고, 목표-질문-지표 접근법의 정본 자리
- [팀 문화와 지식 공유](team-culture-and-knowledge-sharing.md) — 형제 허브. 이 측정이 겨누는
  제도들이 사는 자리
- [코드 규칙과 변경 리뷰](code-rules-and-change-review.md) — 형제 허브. 리뷰 속도라는 측정 대상이
  절차로 사는 쪽
- [리뷰 도구와 정적 분석](review-tooling-and-static-analysis.md) — 형제 허브. 잴 수 없는 정확성을
  잴 수 있는 행동으로 바꾸는 쪽

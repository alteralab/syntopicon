---
type: synthesis
title: 리뷰 도구와 정적 분석
description: 코드 리뷰와 규칙 집행이 도구의 데이터 모형과 관문으로 굳는 층을 모으는 자식 허브 — 리뷰 도구의 설계 원칙과 점수 체계와 차례 장치, 그리고 정적 분석의 판정 잣대와 삽입 지점과 검사를 들이는 관문.
generated: { by: "claude-opus-5", at: "2026-09-30T00:00:00Z" }
---

# 리뷰 도구와 정적 분석

- [이 허브의 범위](#이-허브의-범위)
- [리뷰 도구](#리뷰-도구)
- [정적 분석](#정적-분석)
- [이웃 허브](#이웃-허브)

## 이 허브의 범위

여기 모인 여덟은 [winters2020](../sources/winters2020-swe-at-google.md)의 코드 리뷰 도구 장과
정적 분석 장에서 왔다. **부모 허브는 [조직과 아키텍트](organizations-and-architects.md)**이고,
그쪽은 조직과 역할을 갖는다. 여기는 **절차가 도구로 집행되는 층**을 갖는다.

**형제 허브 [코드 규칙과 변경 리뷰](code-rules-and-change-review.md)와 갈리는 자리**: 그쪽이
문화와 절차로 적은 것을 이쪽이 데이터 모형과 관문으로 굳힌다.

두 장 다 사내 도구를 소개하는 장이라 이 KB는 도구 이름·화면 배치·조작 방식을 옮기지 않고
**설계 판단과 그 근거만** 받았다. 그 가름의 정본은 아래 첫 페이지에 있다.

## 리뷰 도구

- [코드 리뷰 도구의 설계 원칙](../concepts/code-review-tooling-design-principles.md) — **먼저
  읽는다.** 도구를 이끈 원칙 넷과 기능을 기각하는 잣대, 그리고 이 장을 가른 방식의 정본
- [리뷰 점수 체계가 만드는 행동](../concepts/review-scoring-and-the-behavior-it-shapes.md) — 승인
  축이 값이 된 모양과, 되돌릴 권한의 배치로 신뢰의 경계를 긋는 자리
- [주의 집합 — 리뷰를 차례의 문제로 놓기](../concepts/attention-set-and-turn-taking.md) — 리뷰의
  지연을 차례의 모호함으로 다시 놓는 재개념화와 그 불변식

## 정적 분석

- [체감 오탐률](../concepts/effective-false-positive-rate.md) — **이 절의 중심.** 오탐의 판정
  주체를 도구의 논리에서 그것을 본 사람의 그다음 행동으로 옮기는 규정과 그 귀결
- [정적 분석을 개발 흐름의 어디에 끼울 것인가](../concepts/static-analysis-workflow-integration-points.md) —
  삽입 지점마다의 조건표와, 경고의 구속력이 보이는 자리의 사회적 성질에서 온다는 명제
- [컴파일러 검사와 경고를 두지 않는 정책](../concepts/compiler-checks-and-no-warnings-policy.md) —
  층을 정하는 것이 중요도가 아니라 확실성이라는 규칙과, 금지의 절대성이 요구하는 것
- [정적 분석을 생태계로 — 검사를 들이는 관문과 되먹임](../concepts/static-analysis-check-admission-and-feedback.md) —
  꽂기 쉬운 생태계를 짓기로 한 결정과 그 대가로 걸린 관문들, 그리고 수정 제안의 역할
- [분석 억제를 프로젝트 단위로 두기](../concepts/project-level-analysis-customization.md) — 설정의
  알갱이를 영향 대상의 알갱이에 맞추라는 규칙과, 그 배치를 고친 자기 수정의 절차

## 이웃 허브

- [조직과 아키텍트](organizations-and-architects.md) — 부모 허브. 조직 구조·소유권·역할, 그리고
  같은 잣대로 갈린 코드 검색 쪽
- [코드 규칙과 변경 리뷰](code-rules-and-change-review.md) — 형제 허브. 이 도구들이 집행하는 규칙과
  승인 구조가 사는 자리
- [진화와 거버넌스](evolution-and-governance.md) — 같은 종류의 검사를 파이프라인에 거는 축
- [테스트 스위트의 적절성](test-suite-adequacy.md) — 뮤테이션 테스팅이 사는 축. 그 리뷰 시점
  배선을 다루는 자리가 그쪽에 있다
- [엔지니어링 생산성 측정](engineering-productivity-measurement.md) — 형제 허브. 잴 수 없는 것을
  잴 수 있는 행동으로 바꾸는 수가 겹치는 자리

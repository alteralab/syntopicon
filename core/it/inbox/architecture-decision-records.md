---
type: concept
title: 아키텍처 결정 기록
status: draft
description: 아키텍처 결정을 짧은 텍스트 파일 하나로 남기는 형식과 그 형식이 요구하는 네 자리 — 결정을 명사구로 적는 제목과 문제와 대안을 한두 문장으로 적는 맥락과 결정 자체와 그 정당화, 그리고 적용 뒤의 귀결과 고려한 절충을 적는 자리, 승인된 것만 적는다는 전제, 마이클 나이가드의 블로그 글이 원전이고 소트웍스 기술 레이더가 채택으로 올렸다는 계보, 평문도 되지만 대개 AsciiDoc이나 마크다운이나 위키 템플릿을 쓴다는 관행, 책 한 권의 ADR을 부록에 색인한다는 조판과 그 부록이 모은 열셋의 제목과 쪽 그리고 목록 첫 항목이 결정이 아니라 견본이라는 관찰, 같은 책이 리팩터링을 적을 때는 ADR이 아니라 아키텍처 스토리를 쓰며 한 장 전체에 ADR 상자가 없다는 대조, 그리고 결정을 문서화하는 일과 그 결정의 올바른 쓰임을 거버넌스하는 일이 별개라는 경계와 그 별개를 적합도 함수가 받는다는 배치
generated: { by: "claude-opus-5", at: "2026-09-17T17:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 아키텍처 결정 기록

- [무엇인가](#무엇인가)
- [계보](#계보)
- [무엇으로 쓰는가](#무엇으로-쓰는가)
- [형식 — 네 자리](#형식--네-자리)
- [승인된 것만 적는다는 전제](#승인된-것만-적는다는-전제)
- [책 한 권의 ADR을 색인하는 방식](#책-한-권의-adr을-색인하는-방식)
- [이 책의 ADR 열셋](#이-책의-adr-열셋)
- [이 책이 리팩터링을 적는 다른 형식](#이-책이-리팩터링을-적는-다른-형식)
- [문서화와 거버넌스는 별개다](#문서화와-거버넌스는-별개다)
- [이 KB의 다른 소스가 이 형식을 쓰는 자리](#이-kb의-다른-소스가-이-형식을-쓰는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **아키텍처 결정을 나중에 읽을 수 있게 남기려면 무엇을 적어야 하는가.**

## 무엇인가

- **저자들의 규정** — **아키텍처 결정 기록(Architectural Decision Records, ADR)은 아키텍처
  결정을 문서화하는 가장 효과적인 방법 중 하나**다 (1장 §"Architectural Decision Records",
  p.5).[^ford2021-hard-parts]
- **한 건의 크기가 규정의 일부다** — ADR 하나는 **짧은 텍스트 파일 하나(대개 한두 쪽 길이)로
  특정 아키텍처 결정 하나를 기술한다** (1장, p.5).[^ford2021-hard-parts]
  - **"결정 하나"와 "한두 쪽"이 같이 붙어 있다는 것이 이 형식의 성격이다.** 결정 여럿을 한
    문서에 모으는 설계 문서와 반대 방향이고, 그래서 결정마다 파일이 하나씩 쌓인다.

## 계보

- **원전은 마이클 나이가드(Michael Nygard)의 블로그 글**이다. 저자들은 그가 **처음 전파했고**
  나중에 **소트웍스 기술 레이더(Thoughtworks Technology Radar)에서 "채택(adopt)"으로 표시**
  됐다고 적는다 (1장, p.5).[^ford2021-hard-parts]
  - **이 KB는 그 블로그 글과 기술 레이더 항목을 확인하지 않았다** — 귀속은 이 책이 그렇게
    귀속한다까지로 둔다.
  - 나이가드는 이 KB에 다른 자리로도 들어와 있다 — [안정성 패턴](stability-patterns.md)이
    그의 *Release It!*을 출처로 든다. **두 자리가 같은 사람이라는 것은 이 KB가 대조한 것이고
    이 책은 그 사실을 적지 않는다.** #hypothesis
- **저자들의 앞 책이 이 주제에 한 장을 할애했다** — *Fundamentals of Software
  Architecture*(오라일리)다 (1장, p.5).[^ford2021-hard-parts] **이 KB가 확인한 원전이
  아니다.**

## 무엇으로 쓰는가

- **평문으로도 쓸 수 있지만 대개는 AsciiDoc이나 마크다운 같은 텍스트 문서 형식으로 쓴다.**
  대안으로 **위키 페이지 템플릿**을 쓸 수도 있다 (1장, p.5).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점. 저자들이 도구를 지목하지 않고 형식만 든다.
  - **텍스트 파일을 먼저 드는 것이 우연이 아니다** — 결정 기록을 소스와 같은 저장소에 두면
    같은 이력 도구가 적용된다. **그 귀결을 이 책이 적지는 않는다.** #hypothesis

## 형식 — 네 자리

- **저자들이 이 책 전체에서 쓰는 형식이다** (1장, p.5):[^ford2021-hard-parts]

  > *ADR: A short noun phrase containing the architecture decision*
  >
  > *Context*
  >
  > In this section of the ADR we will add a short one- or two-sentence description of the
  > problem, and list the alternative solutions.
  >
  > *Decision*
  >
  > In this section we will state the architecture decision and provide a detailed
  > justification of the decision.
  >
  > *Consequences*
  >
  > In this section of the ADR we will describe any consequences after the decision is
  > applied, and also discuss the trade-offs that were considered.

- **네 자리가 각각 다른 것을 막는다.**
  - **제목이 명사구다** — 문장이 아니라 명사구이므로 결정 자체가 이름이 되고, 목록으로 훑을 수
    있게 된다.
  - **맥락이 대안을 함께 요구한다** — 문제 서술 한두 문장에 **대안 해법의 목록**이 붙는다.
    고르지 않은 길을 적어 두지 않으면 나중에 그 결정이 왜 좁혀졌는지 복원되지 않는다.
  - **결정 자리에 정당화가 함께 들어간다** — "무엇을 정했다"만이 아니라 **왜 그것인가의 상세한
    정당화**다.
  - **귀결 자리가 절충을 받는다** — 적용 뒤에 생기는 귀결과 **고려했던 절충**을 함께 적는다.
    이 책의 축이 절충 분석이므로 이 칸이 이 형식을 이 책의 것으로 만든다.

## 승인된 것만 적는다는 전제

- **저자들이 형식을 소개하며 전제 하나를 명시한다** — **각 ADR이 승인되었다는 가정 아래** 이
  형식을 쓴다 (1장, p.5).[^ford2021-hard-parts]
  - **그래서 이 책의 ADR에는 상태(status) 칸이 없다.** 제안·승인·대체 같은 생애 주기를 적는
    칸을 두는 판이 흔하지만, 이 책은 승인된 결정만 싣는다는 전제로 그 칸을 뺐다.
  - **결정이 뒤집히는 경우를 이 형식이 어떻게 다루는지를 이 책이 적지 않는다.**

## 책 한 권의 ADR을 색인하는 방식

- **이 책은 본문에서 내려지는 여러 아키텍처 결정을 ADR로 문서화하고**, 만들어진 모든 ADR의
  목록을 **부록 B**에 모은다 (1장, p.5).[^ford2021-hard-parts]
  - **결정을 만드는 자리와 색인하는 자리를 가른 조판**이다. 결정은 그것이 내려진 장의 흐름
    안에 상자로 놓이고, 훑기는 부록이 맡는다.
  - 그 결정들이 대입되는 체계는 [Sysops Squad 사례](sysops-squad-case.md)다.

## 이 책의 ADR 열셋

**부록 B가 이 책의 ADR을 한자리에 모은다.** 제목과 인쇄판 쪽을 원문 그대로 옮긴다 (부록 B
"Architecture Decision Record References", pp.419–420).[^ford2021-hard-parts]

| 인쇄판 쪽 | ADR 제목 |
|---|---|
| 5 | ADR: A short noun phrase containing the architecture decision |
| 61 | ADR: Migrate Sysops Squad Application to a Distributed Architecture |
| 79 | ADR: Migration Using the Component-Based Decomposition Approach |
| 184 | ADR: Use of Document Database for Customer Survey |
| 211 | ADR: Consolidated Service for Ticket Assignment and Routing |
| 215 | ADR: Consolidated Service for Customer-Related Functionality |
| 241 | ADR: Using a Sidecar for Operational Coupling |
| 247 | ADR: Use of a Shared Library for Common Ticketing Database Logic |
| 280 | ADR: Single Table Ownership for Bounded Contexts |
| 281 | ADR: Survey Service Owns the Survey Table |
| 297 | ADR: Use of In-Memory Replicated Caching for Expert Profile Data |
| 321 | ADR: Use Orchestration for Primary Ticket Workflow |
| 380 | ADR: Loose Contract for Sysops Squad Expert Mobile Application |

- **목록 자체가 위 [형식 — 네 자리](#형식--네-자리)의 첫째 규칙을 검증한다.** 열셋 전부가
  명사구이고 문장이 하나도 없다. **`Migrate`·`Use`로 시작하는 것들도 동사가 아니라 명사구의
  머리다**(이행 그 자체를 가리킨다).
- **부록의 안내 문장과 목록이 한 칸 어긋난다.** 부록은 **이 책의 각 Sysops Squad 결정에
  대응하는 아키텍처 결정 기록이 딸려 있었고 그것들을 여기 모았다**고 적는데, 목록의 첫
  항목(p.5)은 결정이 아니라 **형식을 보이는 견본**이다. 그래서 실제 결정은 열둘이다.
  **이 관찰은 이 KB가 원문을 대조해 적는 것이고 책이 그 어긋남을 말하지 않는다.** #hypothesis
- **쪽 번호가 결정이 내려진 자리를 가리킨다** — 위
  [책 한 권의 ADR을 색인하는 방식](#책-한-권의-adr을-색인하는-방식)이 적는 조판 규약의 실물이다.
  결정은 그 장의 흐름 안 상자에 놓이고 부록이 훑기를 맡는다.

## 이 책이 리팩터링을 적는 다른 형식

**같은 책이 ADR과 나란히 쓰는 형식이 하나 더 있고, 한 장 전체가 그쪽만 쓴다.**

- **5장은 사가의 코드 리팩터링을 아키텍처 스토리(architecture story)로 기록한다** — 사용자
  스토리가 구현하거나 바꿔야 할 기능을 서술하는 것과 달리, 아키텍처 스토리는 **애플리케이션의
  전체 구조에 영향을 주면서 어떤 업무 구동 요인을 만족시키는 특정 코드 리팩터링**을 서술한다
  (5장, p.84, 곁상자).[^ford2021-hard-parts] 형식과 예문은
  [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)
  §"아키텍처 스토리 — 리팩터링을 적는 단위"에 있다.
- **그 장에는 ADR 상자가 없다.** 위 [이 책의 ADR 열셋](#이-책의-adr-열셋)에서 인쇄판 p.79 다음
  항목이 p.184이고, 5장의 쪽 범위(pp.81–130)에 드는 항목이 하나도 없다 (부록 B,
  pp.419–420).[^ford2021-hard-parts]
  - **이 대조는 이 KB가 부록 목록과 본문 쪽 범위를 맞대어 본 것이고, 저자들이 "이 장에는 ADR을
    두지 않는다"고 적지는 않는다.** #hypothesis
- **두 형식이 담는 것이 다르다는 읽기가 가능하다** — ADR은 **선택지 가운데 하나를 고른 결정**과
  그 맥락과 귀결을 담고, 아키텍처 스토리는 **실행할 리팩터링 작업**을 담아 개발자에게 배정된다.
  5장의 사가들이 하는 일이 대부분 "어느 코드를 어디로 옮길 것인가"라 후자에 해당한다. #hypothesis
  - **그래서 이 페이지의 형식이 모든 아키텍처 산출물을 덮지는 않는다.** 결정이 아닌 것은 다른
    양식으로 간다는 것이 이 책이 보이는 실물이다.

## 문서화와 거버넌스는 별개다

- **저자들이 이 절을 닫으며 경계를 하나 긋는다** — **결정을 문서화하는 일은 아키텍트에게
  중요하지만, 그 결정이 제대로 쓰이는지를 거버넌스하는 것은 별개의 주제**다. 다행히 현대
  공학 실천은 **아키텍처 적합도 함수를 써서 흔한 거버넌스 관심사 다수를 자동화**할 수 있게
  한다 (1장, p.5).[^ford2021-hard-parts]
  - **이 한 줄이 이 페이지와 [아키텍처 적합도 함수](architecture-fitness-functions.md)를
    잇는다** — 기록은 사람이 읽는 것이고, 그 기록대로 되는지를 기계가 확인한다.
  - **결정을 적는 일과 그 결정을 지키는 일이 다른 사람의 일일 수도 있다는 함의**까지 이 책이
    적지는 않는다.

## 이 KB의 다른 소스가 이 형식을 쓰는 자리

- **같은 저자들의 다른 책이 ADR을 적합도 함수의 문서화 수단으로 든다** — 결정 문서에 **거기
  담긴 설계 결정을 어떻게 거버넌스하는지를 적는 절을 더한다**는 것이다. 그쪽은 **ADR의 형식
  자체를 규정하지 않고** 그 한 줄이 전부다 ([자동화된 아키텍처
  거버넌스](automated-architectural-governance.md) §"적합도 함수를 문서화하기"). **그래서
  이 페이지가 그쪽이 전제하고 지나간 형식을 담는다.**
- **결정을 누가 어떤 과정으로 내리는가는 다른 페이지가 갖는다** —
  [전략 설계 결정하기](strategic-decision-making.md)가 2003년 원전 쪽에서 그 물음에 답하고,
  [전략 목표와 원칙과 실천](strategic-goals-principles-practices.md)이 결정을 틀 지우는 세
  층을 세운다. **이 페이지는 그 결정이 내려진 뒤 무엇을 적는가만 다룬다.**
  - **세 자리가 겹치지 않는 이유**: 권위(누가)와 틀(무엇에 비추어)과 기록(무엇을 남기는가)은
    서로를 전제하지 않는다. 권위가 정해져도 기록 형식은 비어 있을 수 있고, 형식이 있어도
    권위가 흩어져 있을 수 있다. **이 배치는 이 KB가 세운 것이고 세 소스는 서로를 호명하지
    않는다.** #hypothesis
- **결정의 되돌릴 수 있음을 먼저 재는 소스도 있다** — [되돌릴 수 있는 설계 결정](reversible-design-decisions.md)과
  [데이터 아키텍처의 규정](data-architecture-defined.md) §"일방통행문과 양방향문"이 그것이다.
  **되돌릴 수 없는 결정일수록 맥락과 대안을 적어 둘 값이 크다는 것은 이 KB의 읽기이고 어느
  소스도 그 연결을 적지 않는다.** #hypothesis

## 이어지는 페이지

- [아키텍처 적합도 함수](architecture-fitness-functions.md) — 문서화 다음의 거버넌스
- [자동화된 아키텍처 거버넌스](automated-architectural-governance.md) — 그 거버넌스를 실제로
  거는 일과 ADR을 그 문서로 쓰는 한 줄
- [전략 설계 결정하기](strategic-decision-making.md) — 결정을 누가 어떤 과정으로 내리는가
- [전략 목표와 원칙과 실천](strategic-goals-principles-practices.md) — 결정을 틀 지우는 세 층
- [진화적 아키텍트의 역할](evolutionary-architect-role.md) — 그 결정을 하는 사람
- [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md) — 같은 책이 결정
  아닌 리팩터링을 적는 다른 형식이 사는 자리
- [Sysops Squad 사례](sysops-squad-case.md) — 이 책의 ADR들이 대입되는 체계
- [되돌릴 수 있는 설계 결정](reversible-design-decisions.md) — 무엇을 적어 둘 값이 큰가의 다른 축
- [데이터 아키텍처의 규정](data-architecture-defined.md) — 되돌릴 수 있는 결정과 없는 결정
- [조직과 아키텍트](../synthesis/organizations-and-architects.md) — 이 실천이 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 1장 "What Happens When There
    Are No 'Best Practices'?" §"Architectural Decision Records"(p.5) 한 절이 전부다. 쪽은
    인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용 하나(ADR 형식 네 자리)는 `pdftotext -layout`
    추출로 문자 단위 대조했고, 원문이 이탤릭으로 조판한 항목 이름은 인용 안에서 이탤릭을
    유지했다. 원문은 이 형식을 들여쓴 정의 목록으로 조판하는데 인용 블록으로 옮기며 항목
    사이에 빈 줄을 넣었다 — 낱말은 보태거나 빼지 않았다. 이 절에는 도판도 표도 코드 목록도
    없다. 저자들이 대는 바깥 것들(Michael Nygard의 블로그 글 · Thoughtworks Technology Radar ·
    *Fundamentals of Software Architecture*)은 **이 KB가 확인한 원전이 아니다** —
    귀속은 이 책이 그렇게 귀속한다까지로 둔다. 굵은 글씨는 원문 문장의 한국어 재서술이고
    괄호 안이 그 쪽이다.
    **부록 B "Architecture Decision Record References"(pp.419–420)가 ADR 목록 절에
    합류했다.** 그 부록은 열세 줄의 제목과 쪽 번호가 전부이고, 제목과 쪽을 **영어 그대로**
    옮겼다 — 이 책이 인쇄한 제목 자체가 식별자라 번역하면 본문의 상자와 맞춰 볼 수 없다.
    원문은 각 제목을 굽은 따옴표로 감싸고 `on page NN`을 붙이는데, 표로 옮기며 따옴표를
    빼고 쪽을 열로 갈랐다 — 낱말은 보태거나 빼지 않았다. 대조는 `pdftotext -layout`
    추출로 했다. 부록 B에 도판도 코드 목록도 없다.
    **5장 곁상자 "Architecture Stories"(p.84)가 다른 형식 절에 합류했다.** 그 곁상자의
    직인용은 [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)이
    갖고, 여기서 옮긴 것은 두 형식의 대조다. 5장에 ADR 상자가 없다는 관찰은 **이 KB가 부록 B의
    쪽 목록과 5장의 쪽 범위(pp.81–130, 책 목차 실측)를 맞대어 본 것**이다.

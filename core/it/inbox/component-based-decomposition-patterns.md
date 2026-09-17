---
type: concept
title: 컴포넌트 기반 분해 패턴 여섯
status: draft
description: 모놀리스의 소스 코드를 서비스가 될 컴포넌트로 다듬는 절차를 패턴 여섯으로 세운 자리 — 이 패턴들이 요구하는 전제와 도착점, 여섯의 이름과 각각이 무엇에 쓰이는가, 처음에는 순서대로 쓰고 이후에는 유지보수마다 따로 쓴다는 사용법, 패턴마다 같은 세 절로 조판된다는 구조와 그 둘째 절이 거버넌스 적합도 함수라는 것, 리팩터링을 적는 단위로 사용자 스토리도 기술 부채 스토리도 아닌 아키텍처 스토리를 세우고 그 예문을 보이는 곁상자, 그리고 이 장이 컴포넌트의 단위를 네임스페이스로 잡는다는 전제
generated: { by: "claude-opus-5", at: "2026-09-17T23:30:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 컴포넌트 기반 분해 패턴 여섯

- [이 패턴들이 무엇을 하는가](#이-패턴들이-무엇을-하는가)
- [여섯의 이름과 쓰임](#여섯의-이름과-쓰임)
- [흐름 — 처음에는 순서대로 이후에는 따로](#흐름--처음에는-순서대로-이후에는-따로)
- [패턴마다 같은 세 절](#패턴마다-같은-세-절)
- [아키텍처 스토리 — 리팩터링을 적는 단위](#아키텍처-스토리--리팩터링을-적는-단위)
- [이 장은 결정을 ADR로 적지 않는다](#이-장은-결정을-adr로-적지-않는다)
- [컴포넌트의 단위는 네임스페이스다](#컴포넌트의-단위는-네임스페이스다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **모놀리스의 소스 코드를 서비스가 될 컴포넌트로 다듬으려면 어떤 순서로 무엇을
하는가.**

## 이 패턴들이 무엇을 하는가

- **전제가 먼저 붙는다** — 컴포넌트 기반 분해(component-based decomposition)는 **코드베이스가
  네임스페이스(namespace)나 디렉터리로 어느 정도 구조화되어 묶여 있을 때** 모놀리식 애플리케이션을
  쪼개는 데 아주 효과적인 기법이다 (5장, p.82).[^ford2021-hard-parts]
  - 그 전제가 서지 않을 때 고르는 다른 접근은 [분해 접근 둘](decomposition-approaches.md)에 있다.
- **이 패턴들이 하는 일은 리팩터링이다** (5장, p.82):[^ford2021-hard-parts]

  > This chapter introduces a set of patterns, known as *component-based decomposition
  > patterns*, that describe the refactoring of monolithic source code to arrive at a set of
  > well-defined components that can eventually become services.

  - **"결국 서비스가 될 수 있는"이 이 패턴들의 성격을 정한다.** 이 장의 다섯째 패턴까지는 배포
    산출물이 하나로 남고, 물리적으로 쪼개지는 것은 여섯째 패턴에서다.
- **이 패턴들이 이행의 수고를 크게 덜어 준다**는 것이 저자들이 대는 값어치다 (5장,
  p.82).[^ford2021-hard-parts]

## 여섯의 이름과 쓰임

**저자들이 장 첫머리에서 여섯을 목록으로 요약한다.** 이름은 원문 그대로 두고 쓰임만 재서술한다
(5장, p.82).[^ford2021-hard-parts]

| 패턴 | 인쇄판 쪽 | 무엇에 쓰는가 |
|---|---|---|
| Identify and Size Components | 84 | 모놀리스를 쪼갤 때 대개 맨 처음 적용한다. 컴포넌트를 식별하고 관리하고 크기를 제대로 맞추는 데 쓴다 |
| Gather Common Domain Components | 94 | 애플리케이션 곳곳에 중복되어 있을 수 있는 공통 업무 도메인 로직을 한데 모아, 결과 분산 아키텍처에서 생길 수 있는 중복 서비스의 수를 줄이는 데 쓴다 |
| Flatten Components | 101 | 도메인과 서브도메인과 컴포넌트를 접거나 펴서, 소스 코드 파일이 잘 정의된 컴포넌트 안에만 놓이게 하는 데 쓴다 |
| Determine Component Dependencies | 111 | 컴포넌트 의존을 식별하고 다듬으며, 모놀리식 아키텍처에서 분산 아키텍처로의 이행이 가능한지와 전체 노력 수준이 얼마인지를 판정하는 데 쓴다 |
| Create Component Domains | 120 | 애플리케이션 안의 컴포넌트들을 논리적 도메인으로 묶고, 컴포넌트 네임스페이스나 디렉터리를 특정 도메인에 맞추어 리팩터링하는 데 쓴다 |
| Create Domain Services | 126 | 모놀리식 애플리케이션 안의 논리적 도메인을 따로 배포되는 도메인 서비스로 옮겨, 모놀리식 아키텍처를 물리적으로 쪼개는 데 쓴다 |

- **여섯 가운데 앞 다섯이 한 배포 산출물 안에서 끝난다.** 마지막 하나만이 물리적 분리이고, 그
  도착점이 [분해 접근 둘](decomposition-approaches.md) §"디딤돌로서의 서비스 기반 아키텍처"가
  적는 서비스 기반 아키텍처다. **이 읽기는 위 표의 쓰임 여섯을 이 KB가 맞대어 본 것이고 저자들이
  그렇게 나누어 적지는 않는다.** #hypothesis

## 흐름 — 처음에는 순서대로 이후에는 따로

- **쓰는 방식이 두 가지로 규정된다** — 처음에는 모놀리식 애플리케이션을 분산 애플리케이션으로
  옮기면서 **이 패턴들을 순서대로 함께 쓰고**, 그다음에는 이행 기간에 모놀리식 애플리케이션에
  유지보수가 가해질 때마다 **하나씩 따로** 쓴다 (5장, p.82).[^ford2021-hard-parts]
  - **그래서 이 패턴들은 일회성 절차가 아니다.** 이행이 진행되는 동안에도 모놀리스는 계속
    고쳐지므로, 한 번 정리한 컴포넌트 경계가 다시 흐려진다. 패턴마다 적합도 함수 절이 붙는 이유가
    그것이다 — 아래 [패턴마다 같은 세 절](#패턴마다-같은-세-절)을 보라.
- **그림 5-1이 그 흐름을 하나의 도판으로 그린다** (5장, p.83).[^ford2021-hard-parts] 도판이 이미지
  조판이라 재현하지 않고, 상자와 화살표가 놓인 순서만 옮긴다.
  - 모놀리식 애플리케이션(Monolithic application)에서 시작해 **Identify and size components →
    Gather common domain components → Flatten components → Determine component dependencies →
    Create component domains → Create domain services** 순으로 이어지고, 마지막에서
    **Microservices**로 간다.
  - 도판의 상자 그림이 각 패턴의 결과를 형상으로 보인다 — 크기를 맞추는 단계에서는 칸이 고르게
    나뉘고, 공통 컴포넌트를 모으는 단계에서는 흩어져 있던 같은 색 칸이 하나로 합쳐지며, 도메인
    서비스를 만드는 단계에서 한 덩어리가 별개의 상자 여럿으로 갈라진다.

## 패턴마다 같은 세 절

- **여섯 전부가 같은 세 절로 조판된다** (5장, p.83):[^ford2021-hard-parts]
  - **"Pattern Description"** — 패턴이 어떻게 동작하는지, 왜 중요한지, 적용하면 무엇이
    나오는지를 적는다.
  - **"Fitness Functions for Governance"** — 패턴을 적용한 뒤 **계속되는 유지보수 동안 코드베이스의
    올바름을 지속적으로 분석하고 검증하는 데 쓸 자동화된 거버넌스**를 적는다.
  - 세 번째 절이 **Sysops Squad 애플리케이션**으로 패턴의 쓰임과 적용 뒤의 변형을 보인다.
- **둘째 절이 왜 있는지를 저자들이 한 구절로 밝힌다** — **대부분의 체계가 이행 중에 움직이는
  과녁(moving targets)이라는 것을 알기에** 그 절을 둔다는 것이다 (5장,
  p.83).[^ford2021-hard-parts]
  - 그 적합도 함수들의 목록과 분류는
    [아키텍처 적합도 함수](architecture-fitness-functions.md) §"5장 — 분해 패턴마다 딸리는
    거버넌스 적합도 함수"에 있다.

## 아키텍처 스토리 — 리팩터링을 적는 단위

- **이 장은 각 사가의 코드 리팩터링을 아키텍처 스토리(architecture story)로 기록한다** (5장,
  p.84, 곁상자).[^ford2021-hard-parts]
- **규정이 사용자 스토리와의 대비로 주어진다** (5장, p.84):[^ford2021-hard-parts]

  > Unlike *user stories*, which describe a feature that needs to be implemented or changed, an
  > *architecture story* describes particular code refactoring that impacts the overall
  > structure of an application and satisfies some sort of business driver (such as increased
  > scalability, better time-to-market, etc.).

  - **업무 구동 요인을 만족시켜야 한다는 조건이 정의 안에 들어 있다.** 그 구동 요인의 목록은
    [아키텍처 모듈성의 구동 요인](modularity-drivers.md)이 갖는다.
- **저자들이 보이는 예문** — 아키텍트가 결제 유형을 더할 때의 확장성을 위해 결제 서비스를 쪼갤
  필요를 보았다면 이렇게 적는다 (5장, p.84):[^ford2021-hard-parts]

  > As an architect, I need to decouple the payment service to support better extensibility
  > and agility when adding additional payment types.

  - **사용자 스토리의 문형("As a …, I need … to …")을 그대로 쓰되 주어가 아키텍트다.** 형식은
    빌리고 주어와 목적을 바꾼 것이다.
- **기술 부채 스토리와도 가른다** — 기술 부채 스토리는 대개 개발자가 **뒤 이터레이션에서 "코드를
  정리"하려고 적어 두는 것**인 반면, 아키텍처 스토리는 **특정 아키텍처 특성이나 업무 필요를
  떠받치기 위해 빨리 바뀌어야 하는 것**을 담는다 (5장, p.84).[^ford2021-hard-parts]
  - **가름의 축이 시급성이다** — 같은 리팩터링이라도 미룰 수 있으면 기술 부채이고 미룰 수 없으면
    아키텍처 스토리다. **저자들이 그 축에 이름을 붙이지는 않는다.** #hypothesis

## 이 장은 결정을 ADR로 적지 않는다

- **이 장의 사가들은 결정을 아키텍처 스토리로 남기고 ADR 상자를 두지 않는다.** 부록 B가 색인하는
  ADR 열셋에서 인쇄판 p.79 다음 항목이 p.184이고, 이 장의 쪽 범위에 드는 항목이 없다 (부록 B,
  pp.419–420).[^ford2021-hard-parts]
  - **이 대조는 이 KB가 부록 목록과 본문을 맞대어 본 것이고, 저자들이 "이 장에는 ADR을 두지
    않는다"고 적지는 않는다.** #hypothesis
  - **두 형식이 담는 것이 다르다는 읽기가 가능하다** — ADR은 **선택지 가운데 하나를 고른 결정**을
    담고(형식의 전문은 [아키텍처 결정 기록](architecture-decision-records.md)에 있다), 아키텍처
    스토리는 **실행할 리팩터링 작업**을 담는다. 이 장의 사가들이 하는 일이 대부분 "어느 코드를
    어디로 옮길 것인가"라 후자에 해당한다. #hypothesis

## 컴포넌트의 단위는 네임스페이스다

- **이 장 전체가 컴포넌트를 네임스페이스나 디렉터리와 같은 것으로 다룬다.** 앞 장의 규정이 그
  전제를 세운다 — 컴포넌트는 **체계 안에서 잘 정의된 역할과 책임과 잘 정의된 연산 집합을 가진
  애플리케이션의 구성 요소**이고 대부분의 애플리케이션에서 **네임스페이스나 디렉터리 구조로
  나타난다** (4장, p.71).[^ford2021-hard-parts] 전문은
  [분해 접근 둘](decomposition-approaches.md) §"컴포넌트 기반 분해"에 있다.
- **그 규정이 이 장의 셋째 패턴에서 한 번 더 좁혀진다** — 컴포넌트는 **네임스페이스의 마지막
  노드(리프 노드)**로 다시 정의된다. 그 규정과 그것이 부르는 두 이름(루트 네임스페이스·고아
  클래스)은 [컴포넌트 평탄화](flatten-components.md)에 있다.

## 이어지는 페이지

- [컴포넌트를 식별하고 크기를 맞추기](identify-and-size-components.md) — 첫째 패턴
- [공통 도메인 컴포넌트 모으기](gather-common-domain-components.md) — 둘째 패턴
- [컴포넌트 평탄화](flatten-components.md) — 셋째 패턴
- [분해 접근 둘](decomposition-approaches.md) — 이 패턴들을 고르기까지의 판정
- [아키텍처 모듈성의 구동 요인](modularity-drivers.md) — 아키텍처 스토리가 만족시켜야 할 구동 요인
- [아키텍처 적합도 함수](architecture-fitness-functions.md) — 패턴마다 딸리는 둘째 절의 어휘
- [아키텍처 결정 기록](architecture-decision-records.md) — 이 책이 결정을 적는 다른 형식
- [Sysops Squad 사례](sysops-squad-case.md) — 패턴마다 딸리는 셋째 절이 대입되는 체계
- [모놀리스 분해 패턴](monolith-decomposition-patterns.md) — 쪼개 낸 뒤의 이행 장치들
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) —
  이 페이지가 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 5장 "Component-Based
    Decomposition Patterns" 도입부(pp.81–83, 여는 사가 p.81 · 패턴 여섯의 요약 목록 p.82 ·
    그림 5-1과 세 절 구조 p.83)와 곁상자 "Architecture Stories"(p.84), 그리고 4장
    §"Component-Based Decomposition"(p.71)과 부록 B(pp.419–420). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 18, 실측). 직인용 셋은 `pdftotext -layout` 추출로 문자 단위 대조했고 줄바꿈
    하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었다. 원문이 이탤릭으로 조판한 낱말은 인용
    안에서 이탤릭을 유지했다. **위 여섯 패턴 표의 쓰임 칸은 저자들이 목록으로 적은 한두 문장의
    한국어 재서술이고, 패턴 이름과 쪽은 원문 그대로다** — 원문은 각 항목을 `"…Pattern" on
    page NN` 꼴의 이탤릭 제목과 들여쓴 설명으로 조판하는데 표로 옮기며 제목에서 `Pattern`과
    쪽 표기를 열로 갈랐고 낱말은 보태거나 빼지 않았다. **그림 5-1은 `pdftoppm -r 160 -png`로
    렌더해 눈으로 대조했고** 도판 자체는 재현하지 않고 상자의 순서와 형상만 옮겼다. 이 구간에
    표도 코드 목록도 없다. 여는 사가(p.81)에서 옮긴 것은 없다 — 등장인물이 이 패턴들을
    어디서 배울지 묻는 장면이고 개념 주장이 없다.

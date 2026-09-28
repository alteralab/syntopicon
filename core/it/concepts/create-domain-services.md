---
type: concept
title: 도메인 서비스 만들기
description: 논리적으로 묶어 둔 컴포넌트 도메인을 따로 배포되는 도메인 서비스로 뽑아내 모놀리스를 물리적으로 쪼개는 여섯째 분해 패턴 — 도메인 서비스를 한 도메인의 기능 전부를 담은 굵고 따로 배포되는 소프트웨어 단위로 규정하는 문장과 그 결과가 서비스 기반 아키텍처라는 것, 그 양식의 규정과 기본 토폴로지와 단일 관계형 데이터베이스를 남기는 이유, 곧장 마이크로서비스로 가지 말고 여기 먼저 서는 근거와 너무 잘게 시작한 팀이 치르는 대가의 목록, 모든 컴포넌트 도메인을 식별하고 리팩터링하기 전에는 이 패턴을 적용하지 말라는 조언과 그 반례, 도메인 서비스 안의 네임스페이스를 일관되게 지키는 적합도 함수 하나와 그것이 막으려는 구조 없는 모놀리식 서비스, 다섯 도메인 서비스로 끝나는 책의 사례, 다음 두 장으로 넘어가는 5장의 맺음, 그리고 도메인 서비스라는 이름이 이 KB에서 갈리는 자리, 그리고 이 페이지가 2차 서술로만 갖고 있던 그 양식의 원전(richards2025 14장)이 이 KB에 들어온 뒤 네 항목을 대조해 본 결과 — 데이터베이스가 선택으로 바뀌고 퀀텀이 1에서 여럿까지로 넓어졌으며 서비스 수에 열둘이라는 상한이 붙었다는 것
generated: { by: "claude-opus-5", at: "2026-09-18T01:20:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: richards2025, resource: /it/sources/richards2025.md }
  - { id: newman2021, resource: /it/sources/newman2021.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 도메인 서비스 만들기

- [규정 — 도메인 서비스](#규정--도메인-서비스)
- [이 패턴이 하는 일](#이-패턴이-하는-일)
- [결과 양식 — 서비스 기반 아키텍처](#결과-양식--서비스-기반-아키텍처)
  - [원전이 이 페이지의 2차 서술을 어디까지 뒷받침하는가](#원전이-이-페이지의-2차-서술을-어디까지-뒷받침하는가)
- [왜 마이크로서비스로 곧장 가지 않는가](#왜-마이크로서비스로-곧장-가지-않는가)
- [조언 — 전부 정리한 다음에 옮겨라](#조언--전부-정리한-다음에-옮겨라)
- [거버넌스 — 적합도 함수 하나](#거버넌스--적합도-함수-하나)
- [책의 사례 — 도메인 서비스 다섯](#책의-사례--도메인-서비스-다섯)
- [5장의 맺음 — 이 여섯이 무엇을 보장하는가](#5장의-맺음--이-여섯이-무엇을-보장하는가)
- [세 소스가 같은 방향을 가리킨다](#세-소스가-같은-방향을-가리킨다)
- [이 이름이 이 KB에서 갈리는 자리](#이-이름이-이-kb에서-갈리는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **묶어 둔 컴포넌트 도메인을 실제 배포 단위로 뽑아낼 때 무엇이 나오고 왜 거기서
한 번 멈추는가.**

이 패턴은 [컴포넌트 기반 분해 패턴 여섯](../concepts/component-based-decomposition-patterns.md)의
마지막이고, 여섯 가운데 **배포 산출물이 실제로 갈라지는 유일한 패턴**이다.

## 규정 — 도메인 서비스

- **전제와 결과가 한 문단에 있다** — 컴포넌트가 제대로 크기를 맞추고 평탄해지고 도메인으로
  묶이고 나면 그 도메인들을 **따로 배포되는 도메인 서비스(domain services)로 옮길 수 있고**,
  그렇게 해서 **서비스 기반 아키텍처(service-based architecture)로 알려진 것**이 만들어진다
  (5장, p.126).[^ford2021-hard-parts]
- **도메인 서비스의 규정** (5장, p.126):[^ford2021-hard-parts]

  > Domain services are coarse-grained, separately deployed units of software containing all of
  > the functionality for a particular domain (such as Ticketing, Customer, Reporting, and so
  > on).

  - **세 조건이 들어 있다** — 굵게 나뉘어 있고, 따로 배포되며, **한 도메인의 기능 전부**를
    담는다. 셋째 조건이 앞 패턴의 도메인 묶기를 그대로 상속한다 —
    [컴포넌트 도메인 만들기](../concepts/create-component-domains.md)를 볼 것.

## 이 패턴이 하는 일

- **앞 패턴과의 분업이 명시된다** — 앞의 컴포넌트 도메인 만들기 패턴이 모놀리스 안에 **잘 정의된
  컴포넌트 도메인을 세우고 그것을 컴포넌트 네임스페이스(또는 디렉터리 구조)로 나타내면**, 이
  패턴은 **그 잘 정의된 컴포넌트 도메인들을 따로 배포되는 서비스로 뽑아내어** 서비스 기반
  아키텍처를 만든다 (5장, p.126).[^ford2021-hard-parts]
  - 원문이 이 자리에서 `known as a *domain services*`라고 적는다 — 관사와 복수형이 어긋나는
    **원문 그대로의 조판**이다.
- **그림 5-21이 그 동작을 보인다** — 앞 패턴에서 정의한 **Reporting 컴포넌트 도메인이 모놀리스에서
  뽑혀 나와 따로 배포되는 Reporting 서비스가 된다** (5장, pp.127–128, 그림
  5-21).[^ford2021-hard-parts] 도판은 재현하지 않는다.

## 결과 양식 — 서비스 기반 아키텍처

- **가장 단순한 꼴이 규정된다** (5장, p.126):[^ford2021-hard-parts]

  > In its simplest form, service-based architecture consists of a user interface that remotely
  > accesses coarse-grained domain services, all sharing a single monolithic database.

  - **토폴로지가 여럿 있다** — 사용자 인터페이스를 쪼개거나 데이터베이스를 쪼개거나 API
    게이트웨이를 더하는 식이다. 그러나 **기본 토폴로지가 모놀리스를 옮기는 좋은 출발점**이다
    (5장, p.126).[^ford2021-hard-parts]
- **그림 5-20이 그 기본 토폴로지다.** 도판은 재현하지 않고 배치만 옮긴다 — 맨 위에 **User
  Interface** 한 덩어리가 있고, 그 아래로 **도메인 서비스 넷**이 각각 화살표를 받으며 각
  서비스 안에 **Component 상자 넷**이 들어 있고, 네 서비스가 모두 아래의 **Database 하나**를
  가리킨다 (5장, p.127, 그림 5-20).[^ford2021-hard-parts]
- **이 양식의 규정이 같은 책 2장의 곁상자에 있다.** 이 KB는 그 곁상자를 이 자리에 들인다 —
  이 패턴이 그 양식을 만들어 내는 자리이기 때문이다 (2장, p.32, 곁상자
  "Service-Based Architecture"):[^ford2021-hard-parts]

  > When we refer to service-based architecture, we don't mean a generic architecture based on
  > services, but rather a specific hybrid architecture style that follows a distributed
  > macro-layered structure consisting of a separately deployed user interface, separately
  > deployed remote coarse-grained services, and a monolithic database.

  - **이 양식이 푸는 문제가 하나로 지목된다** — 마이크로서비스의 복잡성 가운데 하나인
    **데이터베이스 수준의 분리**다 (2장, p.32).[^ford2021-hard-parts]
  - **서비스의 원칙은 마이크로서비스와 같다** — 서비스 기반 아키텍처의 서비스는 **마이크로서비스와
    같은 원칙(도메인 주도 설계의 경계 컨텍스트에 근거한)을 따르되**, **아키텍트가 분리에서
    값어치를 보지 못했거나 부정적 절충이 너무 많다고 보아서** 단일 관계형 데이터베이스에 기댄다
    (2장, p.32).[^ford2021-hard-parts]
    - **그래서 이 양식은 모르고 남긴 것이 아니라 판정해서 남긴 것이다.** 데이터베이스를 쪼개지
      않는 선택에 근거가 붙어 있다.
    - **그리고 그 남겨 둔 데이터베이스를 쪼개는 일이 같은 책의 다음 장이다** — 판정은
      [데이터 분해의 구동 요인](data-decomposition-drivers.md)이, 절차는
      [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md)가 갖는다 (6장,
      pp.131–161).[^ford2021-hard-parts]
  - **이 양식이 이행의 흔한 목적지라는 것도 그 자리에서 적힌다** — 서비스 기반 아키텍처는
    **모놀리스를 재구조화할 때 흔한 목표**이고, **기존 데이터베이스 스키마와 통합 지점을 흔들지
    않고 분해를 할 수 있게** 해 준다 (2장, p.32).[^ford2021-hard-parts]
  - **퀀텀 셈법이 그 대가를 수로 보인다** — 이 양식은 서비스마다 격리되어 있어도 **단일 관계형
    데이터베이스 때문에 아키텍처 퀀텀이 1**이다 (2장, p.32).[^ford2021-hard-parts] 그 어휘의
    전문은 [아키텍처 퀀텀](../concepts/architectural-quantum.md)에 있다.
  - 저자들이 이 양식의 상세를 부록 A와 앞 책 *Fundamentals of Software Architecture*로 넘긴다
    (5장, p.126 · 2장, p.32).[^ford2021-hard-parts] **그 책이 이 KB에 들어왔다** —
    [richards2025](../sources/richards2025.md) 14장이 이 양식의 전장이고, 그 자리가
    [서비스 기반 아키텍처 스타일](service-based-architecture-style.md)이다.

### 원전이 이 페이지의 2차 서술을 어디까지 뒷받침하는가

**같은 저자 무리의 2025년 판이 이 양식을 열여덟 쪽으로 편다.** 위 세 인용이 그 전장과 어디서
맞고 어디서 갈리는지만 여기 적고, 전문은 그 페이지가 갖는다.

| 이 페이지가 2021년 판에서 옮긴 것 | 2025년 판 14장의 문면 | 판정 |
|---|---|---|
| **양식의 규정** — 따로 배포되는 UI · 따로 배포되는 원격의 굵은 서비스 · 모놀리식 데이터베이스로 이루어진 분산 거대 계층 구조 | **같은 세 요소를 그대로 적되 데이터베이스에 "선택적으로(optionally)"를 붙인다** (14장, p.209)[^richards2025] | 규정이 넓어졌다 |
| **퀀텀이 1** — 단일 관계형 데이터베이스 때문 (2장, p.32) | **퀀텀이 1에서 여럿까지**다. UI와 데이터베이스를 쪼개면 퀀텀이 여럿 생긴다 (14장, pp.221–222)[^richards2025] | **앞의 것은 뒤의 것의 한 경우다.** 모순이 아니다 |
| **마이크로서비스와 같은 원칙**(경계 컨텍스트에 근거)**을 따른다** | **도메인 주도 설계에 자연히 맞는다**고 적고, 서비스 수에 **열둘이라는 실질 상한**을 새로 건다 (14장, pp.209·223)[^richards2025] | 같은 방향에 수 하나가 더해졌다 |
| **디딤돌로 삼아도 된다** | **디딤돌이라는 이름을 그대로 쓰고** 근거를 하나 더 든다 — 건너뛰면 **필요 없는 기능까지 전부 마이크로서비스가 된다** (14장, p.226)[^richards2025] | 같은 처방, 다른 근거 |

- **저자가 겹치므로 독립된 둘째 증언이 아니다** — 닐 포드와 마크 리처즈가 앞뒤 양쪽 공저자다.
  이 KB는 두 인쇄를 함께 적고 `contradicts`를 걸지 않는다. #hypothesis
- **2025년 판이 이 페이지에 없던 것을 셋 더 갖는다** — **엔티티 객체 공유 라이브러리 하나가
  안티패턴이라는 판정과 논리 분할이라는 완화책**, **도메인 서비스 사이 통신을 피하고 데이터를
  공유하라는 우선순위**, 그리고 **도메인 정렬 팀을 요구하고 기술 정렬 팀을 기각하는 판정**이다.
  셋 다 [서비스 기반 아키텍처 스타일](service-based-architecture-style.md)이 갖는다.

## 왜 마이크로서비스로 곧장 가지 않는가

- **이 패턴의 값어치가 앞 장의 목록에 하나 더 얹힌다** — 4장이 든 이득들에 더해, 서비스 기반
  아키텍처로 **먼저** 옮기면 아키텍트와 개발팀이 **각 도메인 서비스에 대해 더 배워서** 그것을
  마이크로서비스 아키텍처 안의 더 작은 서비스로 쪼갤지 아니면 **더 큰 도메인 서비스로 남길지**를
  판정할 수 있다 (5장, p.127).[^ford2021-hard-parts] 4장의 이득 넷은
  [분해 접근 둘](decomposition-approaches.md) §"디딤돌로서의 서비스 기반 아키텍처"에 있다.
  - **그래서 이 멈춤의 산출물은 지식이다.** 도메인마다 얼마나 잘게 나눌지를 **쪼개기 전에
    알아내는 대신 한 단계 굵게 운영해 보고 알아낸다.**
- **반대쪽의 대가가 목록으로 적힌다** (5장, p.127):[^ford2021-hard-parts]

  > Too many teams make the mistake of starting out too fine-grained, and as a result must
  > embrace all of the trappings of microservices (such as data decomposition, distributed
  > workflows, distributed transactions, operational automation, containerization, and so on)
  > without the need for all of those fine-grained microservices.

  - **목록의 다섯이 이 책의 뒤 장들이다** — 데이터 분해(6장) · 분산 워크플로(11장) · 분산
    트랜잭션(9장·12장) · 운영 자동화 · 컨테이너화. **이 대응은 이 KB가 목차와 맞대어 본
    것이다.** #hypothesis

## 조언 — 전부 정리한 다음에 옮겨라

- **조문** (5장, p.128):[^ford2021-hard-parts]

  > A word of advice, however: don't apply this pattern until *all* of the component domains
  > have been identified and refactored.

  - **이유는 고쳐 쓰는 양이다** — 그래야 컴포넌트(따라서 소스 코드)를 옮길 때 **각 도메인
    서비스에 가해야 할 수정이 줄어든다** (5장, p.128).[^ford2021-hard-parts]
- **저자들이 반례를 하나 든다** (5장, p.128):[^ford2021-hard-parts]
  - 티켓팅과 지식 베이스 기능 전부를 Ticket 도메인으로 묶어 리팩터링하고 그 도메인에서 새 Ticket
    서비스를 만들었다고 하자.
  - 그런데 그 뒤에 **고객 설문 컴포넌트(`ss.customer.survey`)가 Ticket 도메인의 일부로
    판정**되었다고 하자.
  - Ticket 도메인은 이미 옮겨졌으므로 **Ticket 서비스를 고쳐서 Survey 컴포넌트를 넣어야 한다.**
  - **결론은 순서다** — 먼저 컴포넌트를 전부 컴포넌트 도메인에 맞추어 리팩터링하고, **그다음에**
    그 도메인들을 도메인 서비스로 옮긴다.
  - **이 조언이 앞 다섯 패턴을 순서대로 쓰라는 장 도입부의 규정과 같은 방향이다** —
    [컴포넌트 기반 분해 패턴 여섯](../concepts/component-based-decomposition-patterns.md)
    §"흐름 — 처음에는 순서대로 이후에는 따로". 다만 이 조언은 **마지막 패턴 안에서의 보폭**을
    말한다는 점이 다르다. 도메인을 하나씩 뽑아내는 것은 되지만, 도메인 **목록**이 확정되기
    전에는 하나도 뽑지 말라는 것이다. **저자들이 그 구분을 명시하지는 않는다.** #hypothesis

## 거버넌스 — 적합도 함수 하나

- **지킬 것이 정해진다** — 각 도메인 서비스 안의 컴포넌트를 그 도메인에 맞추어 두는 것이
  중요하고, **특히 그 도메인 서비스가 나중에 더 작은 마이크로서비스로 쪼개질 것이라면** 그렇다.
  이런 거버넌스가 **도메인 서비스가 그 자체로 구조 없는 모놀리식 서비스가 되는 것을 막아 준다**
  (5장, p.129).[^ford2021-hard-parts]
  - **이 절이 이 장에서 유일하게 "쪼갠 뒤"를 내다보는 거버넌스다.** 앞 다섯 패턴의 적합도 함수는
    모놀리스 안의 구조를 지켰고, 이것은 **새로 만든 배포 단위 안의 구조**를 지킨다.
- **All components in `<some domain service>` should start with the same namespace.** 배포
  시점에 CI/CD 파이프라인으로 촉발되어 **도메인 서비스 안 컴포넌트들의 네임스페이스가 일관되게
  유지되게** 한다 (5장, p.129).[^ford2021-hard-parts]
  - 저자들의 예 — **Ticket 도메인 서비스 안의 모든 컴포넌트는 `ss.ticket`으로 시작해야 한다**는
    ArchUnit 규칙이다 (5장, p.129, 예제 5-11).[^ford2021-hard-parts]
    - 버전 조건: 2021년 저술 시점의 ArchUnit 표기다. 저자들이 판을 적지 않는다.
  - **개수 규칙이 붙는다** — **각 도메인 서비스가 자기 도메인에 근거한 자기 적합도 함수를
    갖는다** (5장, p.129).[^ford2021-hard-parts]
  - 분류와 이 장의 적합도 함수 전체 목록은
    [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md)
    §"2021년 책 5장 — 분해 패턴마다 딸리는 거버넌스 적합도 함수"에 있다.

## 책의 사례 — 도메인 서비스 다섯

- **이행 계획을 개발팀과 함께 세운다** — 두 아키텍트가 개발팀과 긴밀히 일해 **컴포넌트 도메인에서
  도메인 서비스로 가는 이행을 단계로 나누는 계획**을 만든다 (5장, p.129,
  사가).[^ford2021-hard-parts]
- **해야 할 일이 둘로 드러난다** — 각 컴포넌트 도메인 안의 **코드를 모놀리스에서 뽑아 새 프로젝트
  작업 공간으로 옮기는 일**과, **사용자 인터페이스가 이제 그 도메인 안의 기능을 원격으로
  접근하게 하는 일**이다 (5장, p.129, 사가).[^ford2021-hard-parts]
  - **둘째가 이 패턴의 숨은 비용이다.** 앞 다섯 패턴은 화면을 건드리지 않았는데, 여기서 호출이
    프로세스 안의 호출에서 **원격 호출**로 바뀐다. 위 그림 5-20의 화살표가 그 지점이다.
- **보폭이 한 컴포넌트씩이다** — 앞서 식별한 컴포넌트 도메인에서 출발해 **컴포넌트를 한 번에
  하나씩** 옮겨 결국 서비스 기반 아키텍처에 이른다(그림 5-22). **앞 패턴에서 식별한 각 도메인
  영역이 이제 따로 배포되는 서비스가 된다** (5장, pp.129–130, 사가).[^ford2021-hard-parts]
- **그림 5-22의 배치를 옮긴다.** 도판은 재현하지 않는다 — 맨 위에 User Interface가 있고 점선
  화살표가 다섯 서비스로 간다 (5장, p.130, 그림 5-22):[^ford2021-hard-parts]

| 도메인 서비스 | 담은 컴포넌트 |
|---|---|
| Customer domain service | Customer profile · Support contracts · Billing payments · Billing history |
| Admin domain service | Expert profile · User maintenance |
| Shared domain service | Login · Notification |
| Ticket domain service | Ticket maintenance · Ticket shared · Ticket completion · Ticket assign · Ticket route · Survey · KB maintenance · KB search |
| Reporting domain service | Reporting shared · Financial reports · Ticket reports · Expert reports |

  - **이 그림에는 데이터베이스가 없다.** 위 그림 5-20의 기본 토폴로지에는 공유 데이터베이스가
    그려져 있는데 사가의 결과 그림에는 그것이 빠져 있다. 데이터는 다음 장의 주제다. **저자들이
    그 누락에 대해 적지 않는다.** #hypothesis

## 5장의 맺음 — 이 여섯이 무엇을 보장하는가

- **저자들이 경험에서 낸 판정으로 장을 닫는다** (5장, p.130):[^ford2021-hard-parts]

  > It has been our experience that "seat-of-the-pants" migration efforts rarely produce
  > positive results. Applying these component-based decomposition patterns provides a
  > structured, controlled, and incremental approach for breaking apart monolithic
  > architectures.

  - **주장의 격이 경험이다.** 이 패턴들이 더 나은 결과를 낸다는 실증을 대지 않고 **저자들의
    경험**으로 적는다. 이 KB는 그 격을 그대로 둔다.
  - **약속하는 것이 셋이다** — 구조화되고(structured), 통제되며(controlled), 점진적인
    (incremental) 접근. **쪼갠 결과의 품질이 아니라 쪼개는 과정의 성질을 약속한다.**
    #hypothesis
- **다음이 어디로 가는지도 적는다** — 이 패턴들을 적용하고 나면 팀은 이제 **모놀리식 데이터를
  분해하는 일**(6장)과 **도메인 서비스를 필요에 따라 더 잘게 나눈 마이크로서비스로 쪼개는
  일**(7장)에 착수할 수 있다 (5장, p.130).[^ford2021-hard-parts]

## 세 소스가 같은 방향을 가리킨다

**"처음에는 굵게 쪼개라"는 처방이 이 KB의 세 소스에 모두 있다. 근거가 서로 다르다.**

| 소스 | 처방 | 근거 |
|---|---|---|
| 이 페이지(ford2021) | 마이크로서비스로 가기 전에 **서비스 기반 아키텍처에 먼저 선다** | 도메인마다 더 잘게 나눌지를 운영해 보고 판정할 수 있다. 데이터베이스 분해·운영 자동화·조직 변경을 미룰 수 있다 |
| [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md)(newman2021) | **경계 컨텍스트 전체를 감싸는 서비스**를 노리고 나중에 중첩 컨텍스트를 따라 쪼갠다 | 다루는 서비스의 수를 줄이고 싶다. 나중의 세분은 굵은 API 뒤에 감출 수 있다[^newman2021] |
| 같은 페이지(khononov2021) | 경계 컨텍스트가 **가장 큰 유효한 모놀리스**이고 하위 도메인이 안전한 기본값이다 | 너무 좁게 자르면 애그리게이트가 갈라져 원하지 않는 결과가 난다[^khononov2021] |

- **셋이 부딪히지 않는다 — 같은 방향의 처방을 다른 층에서 낸다.** 이쪽은 **양식**을 고르고(서비스
  기반 아키텍처), 뉴먼과 크호노프는 **경계의 재료**를 고른다(경계 컨텍스트·하위 도메인). 한쪽은
  "무엇으로 배포할 것인가"에, 다른 쪽은 "어디에 선을 그을 것인가"에 답한다.
- **그래서 겹쳐 쓸 수 있다** — 컴포넌트 도메인을 묶는 기준으로 하위 도메인이나 경계 컨텍스트를
  쓰고, 그렇게 묶은 것을 도메인 서비스로 배포하면 세 처방이 한 절차가 된다. **세 소스 가운데
  누구도 그렇게 적지 않는다.** #hypothesis
- **다만 이쪽에만 있는 것이 하나 있다 — 공유 데이터베이스를 남기라는 조건이다.** 뉴먼과 크호노프의
  굵은 시작은 서비스마다 자기 데이터를 갖는 것을 전제하는데, 서비스 기반 아키텍처는 **단일 관계형
  데이터베이스**를 명시적으로 남긴다. 그 차이가 퀀텀 셈법에서 수로 나타난다(위
  [결과 양식](#결과-양식--서비스-기반-아키텍처)). **이 대질은 이 KB가 세운 것이다.** #hypothesis

## 이 이름이 이 KB에서 갈리는 자리

- **같은 낱말을 쓰는 페이지가 이 KB에 하나 더 있고 가리키는 것이 다르다.**
  [도메인 서비스](../concepts/domain-services.md)의 도메인 서비스는 **엔티티에도 값 객체에도
  자연히 앉지 않는 도메인 연산을 담는 무상태 객체**다 — **코드 안의 한 클래스**다.
- **이 페이지의 도메인 서비스는 배포 단위다** — 한 도메인의 기능 전부를 담고 따로 배포되는 굵은
  소프트웨어 단위이고, 그 안에 컴포넌트가 여럿 들어 있다.
- **층이 다르므로 모순이 아니다.** 하나는 설계 요소이고 하나는 배포 산출물이다. 실제로 이쪽의
  도메인 서비스 **안에** 저쪽의 도메인 서비스가 여럿 들어 있을 수 있다. **두 소스가 서로를
  호명하지 않으며 이 배치는 이 KB가 세운 것이다.** #hypothesis

## 이어지는 페이지

- [컴포넌트 기반 분해 패턴 여섯](../concepts/component-based-decomposition-patterns.md) — 이 패턴이
  마지막으로 놓이는 절차
- [컴포넌트 도메인 만들기](../concepts/create-component-domains.md) — 이 패턴 앞에 오는 다섯째이자 입력
- [컴포넌트 의존 판정](determine-component-dependencies.md) — 이 패턴이 감당할 수 있는 일인지를
  먼저 재는 넷째
- [분해 접근 둘](decomposition-approaches.md) — 서비스 기반 아키텍처를 디딤돌로 삼을 근거 넷
- [도메인 서비스](../concepts/domain-services.md) — 같은 이름이 코드 안의 한 클래스를 가리키는 자리
- [서비스 기반 아키텍처 스타일](service-based-architecture-style.md) — 이 패턴이 만들어 내는
  양식의 원전 전장(richards2025 14장)
- [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md) — 같은 방향의
  처방을 경계의 재료 쪽에서 내는 두 소스
- [데이터 분해의 구동 요인](data-decomposition-drivers.md) — 이 양식이 남겨 둔 데이터베이스를
  쪼갤 것인가의 판정
- [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md) — 그 쪼개기의 절차
- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — 이 양식의 배포 단위를 세는 잣대
- [독립 배포 가능성](independent-deployability.md) — 이 패턴이 겨냥하는 성질
- [모놀리스 분해 패턴](monolith-decomposition-patterns.md) — 뽑아내는 일에 쓰는 이행 장치들
- [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md) — 위 적합도 함수의 분류 어휘
- [Sysops Squad 사례](sysops-squad-case.md) — 위 사례가 대입되는 체계
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) —
  이 페이지가 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 5장 "Component-Based
    Decomposition Patterns" §"Create Domain Services Pattern"(pp.126–130) — 도입(p.126) ·
    §"Pattern Description"(pp.126–128) · §"Fitness Functions for Governance"(p.129) ·
    §"Sysops Squad Saga: Creating Domain Services"(pp.129–130) · §Summary(p.130), 그리고
    2장 "Discerning Coupling in Software Architecture" §"Service-Based Architecture"
    곁상자(p.32). 6장 "Pulling Apart Operational Data"(pp.131–161)는 위 §"결과 양식 — 서비스
    기반 아키텍처"에서 **남겨 둔 데이터베이스를 다음 장이 가른다**는 연결에만 쓴다 — 그 장의
    전문은 [데이터 분해의 구동 요인](data-decomposition-drivers.md)과
    [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md)가 갖는다.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용 여섯(도메인 서비스의 규정 ·
    서비스 기반 아키텍처의 가장 단순한 꼴 · 2장 곁상자의 양식 규정 · 너무 잘게 시작하는 실수 ·
    전부 정리한 뒤에 옮기라는 조언 · 장의 맺음)은 `pdftotext -layout` 추출로 문자 단위
    대조했고 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었다. 굽은 따옴표와
    아포스트로피는 곧은 것으로 옮겼다. 원문이 이탤릭으로 조판한 낱말은 인용 안에서 이탤릭을
    유지했다. 원문 p.126의 `known as a *domain services*`는 관사와 복수형이 어긋나는 원문
    그대로의 조판이라 본문에 표시만 하고 인용하지 않았다. **ArchUnit 목록 하나(예제 5-11)는
    펜스로 옮기지 않고 그 규칙이 하는 일만 산문으로 적었다** — 이 KB의 적합도 함수 대표
    펜스는 ford2022 예제 2-1 하나로 유지한다(SCHEMA §3). **도판 셋(그림 5-20 기본 토폴로지 ·
    5-21 도메인 하나가 뽑혀 나가는 그림 · 5-22 다섯 도메인 서비스)은 `pdftoppm -r 160 -png`로
    렌더해 눈으로 읽었고**, 도판 자체는 재현하지 않고 상자의 배치와 이름만 옮겼다. 도메인
    서비스 다섯 표는 원문 표가 아니라 **그림 5-22의 상자 옆에 적힌 컴포넌트 이름을 이 KB가
    표로 모은 것**이고 이름은 도판 그대로다. 이 구간에 원문 표는 없다. 굵은 글씨는 원문
    문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

[^newman2021]: Newman 2021, 2장 "How to Model Microservices"
    §"Mapping Aggregates and Bounded Contexts to Microservices"(p.58) ·
    §"Turtles all the way down"(pp.58–59). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    이 페이지는 그 처방을 대질에만 쓴다 — 전문과 직인용은
    [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md)이 갖는다.

[^khononov2021]: Khononov 2021, 14장 "Microservices"
    §"Domain-Driven Design and Microservices' Boundaries"(§"Bounded Contexts" pp.225–227 ·
    §Subdomains pp.228–229). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측). 이 페이지는 그 처방을
    대질에만 쓴다 — 전문과 직인용은
    [마이크로서비스 경계 어림법](../concepts/microservice-boundary-heuristics.md)이 갖는다.

[^richards2025]: Richards·Ford 2025(2판), 14장 "Service-Based Architecture Style"
    (인쇄판 pp.209–226) — 도입과 §Topology(p.209) · §"Style Characteristics"(pp.221–223,
    그림 14-8) · §"Examples and Use Cases"(p.226). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 24, 실측).
    이 페이지는 그 장을 위 대조표에만 쓰고 직인용을 두지 않았다 — 전문과 도판 실측은
    [서비스 기반 아키텍처 스타일](service-based-architecture-style.md)이 갖는다.

---
type: concept
title: 컴포넌트 도메인 만들기
description: 컴포넌트들을 논리적 도메인으로 묶어 굵은 도메인 서비스가 될 자리를 미리 정하는 다섯째 분해 패턴 — 서비스와 컴포넌트가 일대다라는 전제와 그래서 묶기가 필요하다는 규정, 컴포넌트 도메인을 관련 기능을 수행하는 컴포넌트의 묶음으로 규정하고 그것을 네임스페이스 노드의 계층으로 물리적으로 나타내는 기법과 노드 자리마다 붙는 다섯 이름, 도메인 주도 설계 이전에 지어진 코드는 네임스페이스를 고쳐야 도메인이 드러난다는 조건과 고객 도메인의 리팩터링 전후 표, 승인된 도메인 목록 밖의 네임스페이스를 잡는 적합도 함수 하나, 다섯 도메인을 제품 책임자와 함께 식별하고 도메인 다이어그램으로 빠진 컴포넌트가 없는지 검증한 책의 사례와 도메인별 네임스페이스 리팩터링 표 넷, 그리고 이 도메인이 DDD의 하위 도메인이나 경계 컨텍스트와 같은 것인지의 대질
generated: { by: "claude-opus-5", at: "2026-09-18T01:10:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 컴포넌트 도메인 만들기

- [왜 묶는가 — 서비스와 컴포넌트는 일대다다](#왜-묶는가--서비스와-컴포넌트는-일대다다)
- [컴포넌트 도메인의 규정](#컴포넌트-도메인의-규정)
- [네임스페이스 노드가 도메인을 나타낸다](#네임스페이스-노드가-도메인을-나타낸다)
- [도메인 주도 설계 이전에 지어진 코드](#도메인-주도-설계-이전에-지어진-코드)
- [거버넌스 — 적합도 함수 하나](#거버넌스--적합도-함수-하나)
- [책의 사례 — 도메인 다섯](#책의-사례--도메인-다섯)
- [책의 사례 — 네임스페이스 리팩터링](#책의-사례--네임스페이스-리팩터링)
- [이 도메인은 DDD의 하위 도메인인가](#이-도메인은-ddd의-하위-도메인인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **컴포넌트를 다 다듬고 나서 무엇을 기준으로 묶어야 그 묶음이 배포 단위가 될 수
있는가.**

이 패턴은 [컴포넌트 기반 분해 패턴 여섯](../concepts/component-based-decomposition-patterns.md)의 다섯째다.

## 왜 묶는가 — 서비스와 컴포넌트는 일대다다

- **전제가 먼저 놓인다** — 모놀리스 안에서 식별된 각 컴포넌트가 별개 서비스의 후보일 수 있지만,
  **대부분의 경우 서비스와 컴포넌트의 관계는 일대다**다. 곧 **한 서비스가 컴포넌트 하나 이상을
  담을 수 있다** (5장, p.120).[^ford2021-hard-parts]
- **그래서 패턴의 목적이 묶기가 된다** (5장, p.120):[^ford2021-hard-parts]

  > The purpose of the *Create Component Domains* pattern is to logically group components
  > together so that more coarse-grained domain services can be created when breaking up an
  > application.

  - **"논리적으로"가 이 패턴의 성격을 정한다.** 이 패턴이 끝나도 배포 산출물은 여전히 하나이고,
    물리적 분리는 다음 패턴의 몫이다 —
    [도메인 서비스 만들기](create-domain-services.md)를 볼 것.

## 컴포넌트 도메인의 규정

- **정의가 문장 안의 삽입구로 주어진다** (5장, p.121):[^ford2021-hard-parts]

  > Identifying component domains—the grouping of components that perform some sort of related
  > functionality—is a critical part of breaking apart any monolithic application.

  - **기준이 "관련 기능"이고 그 이상이 없다.** 무엇이 관련되었는지를 정하는 규칙을 저자들이
    주지 않고, 아래 사가에서는 그 판정을 **업무 이해관계자와의 협업**으로 처리한다.
- **저자들이 앞 장의 조언을 여기서 다시 인용한다** (5장, p.121):[^ford2021-hard-parts]

  > When breaking apart monolithic applications, consider first moving to service-based
  > architecture as a stepping-stone to other distributed architectures.

  - 그리고 **컴포넌트 도메인을 만드는 일이 서비스 기반 아키텍처에서 결국 도메인 서비스가 될
    것을 정하는 효과적인 방법**이라고 잇는다 (5장, p.121).[^ford2021-hard-parts]
  - 그 조언의 전문과 근거 넷은 [분해 접근 둘](decomposition-approaches.md)
    §"디딤돌로서의 서비스 기반 아키텍처"에 있다.

## 네임스페이스 노드가 도메인을 나타낸다

- **물리적 표현이 네임스페이스다** — 컴포넌트 도메인은 애플리케이션 안에서 **컴포넌트
  네임스페이스(또는 디렉터리)로 물리적으로 나타난다.** 네임스페이스 노드가 본디 **계층적**이라
  기능의 **도메인과 서브도메인을 나타내는 훌륭한 수단**이 된다 (5장,
  p.121).[^ford2021-hard-parts]
- **그림 5-18이 한 네임스페이스의 노드마다 이름을 붙인다.** 도판을 재현하지 않고 배치와 이름만
  옮긴다 — `ss.customer.billing.payment.MonthlyBilling` 하나에 화살표 다섯이 붙는다 (5장,
  p.121, 그림 5-18).[^ford2021-hard-parts]

| 노드 | 무엇인가 |
|---|---|
| `ss` | Application |
| `.customer` | Domain |
| `.billing` | Subdomain |
| `.payment` | Component |
| `.MonthlyBilling` | Class within the Payment component |

- **본문이 같은 배치를 글로도 적는다** — 네임스페이스의 **둘째 노드**(`.customer`)가
  **도메인**을, **셋째 노드**(`.billing`)가 고객 도메인 아래의 **서브도메인**을, **리프
  노드**(`.payment`)가 **컴포넌트**를 가리키고, 끝의 `.MonthlyBilling`은 Payment 컴포넌트에 든
  **클래스 파일**을 가리킨다 (5장, p.121).[^ford2021-hard-parts]
  - **앞 패턴의 규정과 맞물린다.** 컴포넌트가 리프 노드라는 규정은
    [컴포넌트 평탄화](flatten-components.md)가 세웠고, 이 패턴은 그 리프 노드 **위쪽 노드들에
    이름을 준다.** 같은 트리를 두 패턴이 아래에서와 위에서 각각 규율한다.
  - **서브도메인이라는 낱말이 두 패턴에서 같은 대상을 가리킨다** — 평탄화 쪽에서 서브도메인은
    **확장된 루트 네임스페이스**이고 여기서는 **도메인 아래의 셋째 노드**다. 둘 다 리프가 아닌
    중간 노드를 뜻한다. **저자들이 그 동일성을 명시하지는 않는다.** #hypothesis

## 도메인 주도 설계 이전에 지어진 코드

- **조건이 붙는다** — 많은 오래된 모놀리스가 **도메인 주도 설계가 널리 쓰이기 전에** 구현되었기
  때문에, 애플리케이션 안의 도메인을 구조적으로 식별하려면 **네임스페이스의 리팩터링이 필요한
  경우가 많다** (5장, p.121).[^ford2021-hard-parts]
- **저자들의 실물이 고객 도메인이다.** 리팩터링 전 (5장, p.121, 표 5-13):[^ford2021-hard-parts]

| Component | Namespace |
|---|---|
| Billing Payment | `ss.billing.payment` |
| Billing History | `ss.billing.history` |
| Customer Profile | `ss.customer.profile` |
| Support Contract | `ss.supportcontract` |

- **진단** — 각 컴포넌트가 고객 기능과 관련되어 있는데 **대응하는 네임스페이스가 그 연관을
  반영하지 않는다.** 고객 도메인(네임스페이스 `ss.customer`로 나타나는)을 제대로 식별하려면
  Billing Payment·Billing History·Support Contract의 네임스페이스 **앞에 `.customer` 노드를
  더해야** 한다 (5장, p.122).[^ford2021-hard-parts]
- **리팩터링 후** (5장, p.122, 표 5-14):[^ford2021-hard-parts]

| Component | Namespace |
|---|---|
| Billing Payment | `ss.customer.billing.payment` |
| Billing History | `ss.customer.billing.history` |
| Customer Profile | `ss.customer.profile` |
| Support Contract | `ss.customer.supportcontract` |

  - **고친 것은 이름뿐이다** — 고객 관련 기능 전부(청구·프로필 유지보수·지원 계약 유지보수)가
    이제 `.customer` 아래로 묶여 각 컴포넌트가 그 도메인에 정렬된다 (5장,
    p.122).[^ford2021-hard-parts]
  - **그래서 이 패턴의 작업 단위는 이름 바꾸기다.** 코드를 옮기지도 쪼개지도 않고 네임스페이스
    접두만 고친다. 앞 세 패턴이 **코드를 옮겼던** 것과 대비된다. **저자들이 그 대비를 적지는
    않는다.** #hypothesis

## 거버넌스 — 적합도 함수 하나

- **리팩터링한 뒤에 지킬 것이 정해진다** — 한 번 정리하고 나면 **네임스페이스 규칙이 집행되고
  컴포넌트 도메인이나 서브도메인의 문맥 밖에 코드가 존재하지 않게** 컴포넌트 도메인을 다스리는
  것이 중요하다 (5장, p.122).[^ford2021-hard-parts]
- **All namespaces under `<root namespace node>` should be restricted to `<list of domains>`.**
  배포 시점에 CI/CD 파이프라인으로 촉발되어 **애플리케이션에 담기는 도메인을 제한**한다 (5장,
  p.122).[^ford2021-hard-parts]
  - **잡는 것이 둘이다** — 개발팀이 **부주의하게 도메인을 더 만드는 것을 막고**, **승인된 도메인
    목록 밖에 새 네임스페이스(또는 디렉터리)가 만들어지면 아키텍트에게 경보**한다.
  - 저자들의 예가 **한 애플리케이션 안에 ticket·customer·admin 도메인만 존재하게 하는**
    ArchUnit 코드다 (5장, p.123, 예제 5-10).[^ford2021-hard-parts]
    - 버전 조건: 2021년 저술 시점의 ArchUnit 표기다. 저자들이 판을 적지 않는다.
  - **이 함수는 허용 목록(allowlist)이다** — 앞 패턴의 둘째 함수가 금지를 하나씩 이름으로
    적는 차단 목록이었던 것과 성격이 다르다. 목록 밖이 전부 위반이므로 규칙 하나가 코드베이스
    전체를 덮는다. **저자들이 그 대비를 적지는 않는다.** #hypothesis
  - 분류와 이 장의 적합도 함수 전체 목록은
    [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md)
    §"2021년 책 5장 — 분해 패턴마다 딸리는 거버넌스 적합도 함수"에 있다.

## 책의 사례 — 도메인 다섯

- **판정에 제품 책임자가 들어온다** — 두 아키텍트가 **제품 책임자(product owner)**와 상의해
  함께 애플리케이션 안의 **주요 도메인 다섯**을 식별한다 (5장, p.123,
  사가):[^ford2021-hard-parts]

| 도메인 | 네임스페이스 | 무엇을 담는가 |
|---|---|---|
| Ticketing | `ss.ticket` | 티켓 처리·고객 설문·지식 베이스(KB) 기능을 포함한 티켓 관련 기능 전부 |
| Reporting | `ss.reporting` | 리포팅 기능 전부 |
| Customer | `ss.customer` | 고객 프로필·청구·지원 계약 |
| Admin | `ss.admin` | 사용자와 Sysops Squad 전문가의 유지보수 |
| Shared | `ss.shared` | 다른 도메인들이 쓰는 로그인과 알림 기능 |

- **도메인 다이어그램이 검증 수단으로 쓰인다** — 도메인과 각 도메인 안의 컴포넌트 묶음을 보이는
  그림(그림 5-19)을 그렸고, **빠진 컴포넌트가 하나도 없고 각 도메인 안 컴포넌트들 사이의 응집이
  좋다**는 것에 만족했다 (5장, p.123, 사가).[^ford2021-hard-parts]
- **그리고 저자들이 그 그리기 자체를 값어치로 적는다** — 그 작업이 중요했던 이유는 **식별한
  도메인 후보를 검증했고 업무 이해관계자(제품 책임자나 업무 애플리케이션 후원자 같은)와의 협업의
  필요를 드러냈기** 때문이다. **컴포넌트들이 제대로 늘어서지 않았거나 어디에도 속하지 않는
  컴포넌트가 남았다면 제품 책임자와의 협업이 더 필요했을 것**이다 (5장, p.123,
  사가).[^ford2021-hard-parts]
  - **그래서 이 패턴에는 실패 신호가 하나 있다 — 남는 컴포넌트다.** 묶고 나서 어디에도 안 붙는
    컴포넌트가 있으면 도메인 목록이 틀렸다는 뜻이고, 처방은 코드가 아니라 **업무 쪽과 더
    이야기하는 것**이다.
- **그림 5-19의 배치를 옮긴다.** 도판은 재현하지 않는다 — 모놀리스 한 덩어리 안에 맨 위가
  User Interface이고, 그 아래에 테두리를 굵게 한 다섯 묶음이 놓인다 (5장, p.124, 그림
  5-19):[^ford2021-hard-parts]
  - **Customer** — Customer profile · Support contract · Billing payment · Billing history
  - **Admin** — Expert profile · User maintenance
  - **Shared** — Login · Notification
  - **Ticket** — KB maint · KB search · Ticket shared · Ticket maintenance · Ticket completion ·
    Ticket route · Ticket assign · Survey
  - **Reporting** — Reporting shared · Financial reports · Ticket reports · Expert reports

## 책의 사례 — 네임스페이스 리팩터링

**도메인을 정한 뒤, 앞 패턴을 적용한 결과 목록(표 5-12, 전문은
[컴포넌트 평탄화](flatten-components.md)에 있다)을 놓고 도메인별로 고칠 네임스페이스를 정한다.
리팩터링은 도메인마다 아키텍처 스토리 하나로 적힌다** (5장, pp.123–126,
사가).[^ford2021-hard-parts]

- **티켓 도메인** — 핵심 티켓 기능은 이미 `ss.ticket`으로 시작했지만 **설문과 지식 베이스
  컴포넌트는 그렇지 않았다** (5장, p.124, 사가, 표 5-15):[^ford2021-hard-parts]

| Component | Domain | Current namespace | Target namespace |
|---|---|---|---|
| KB Maint | Ticket | `ss.kb.maintenance` | `ss.ticket.kb.maintenance` |
| KB Search | Ticket | `ss.kb.search` | `ss.ticket.kb.search` |
| Ticket Shared | Ticket | `ss.ticket.shared` | Same (no change) |
| Ticket Maintenance | Ticket | `ss.ticket.maintenance` | Same (no change) |
| Ticket Completion | Ticket | `ss.ticket.completion` | Same (no change) |
| Ticket Assign | Ticket | `ss.ticket.assign` | Same (no change) |
| Ticket Route | Ticket | `ss.ticket.route` | Same (no change) |
| Survey | Ticket | `ss.survey` | `ss.ticket.survey` |

- **고객 도메인** — 청구와 설문 컴포넌트를 고객 도메인 아래로 옮겨야 했고, **그 과정에서 Billing
  서브도메인이 생긴다** (5장, p.125, 사가, 표 5-16):[^ford2021-hard-parts]

| Component | Domain | Current namespace | Target namespace |
|---|---|---|---|
| Billing Payment | Customer | `ss.billing.payment` | `ss.customer.billing.payment` |
| Billing History | Customer | `ss.billing.history` | `ss.customer.billing.history` |
| Customer Profile | Customer | `ss.customer.profile` | Same (no change) |
| Support Contract | Customer | `ss.supportcontract` | `ss.customer.supportcontract` |

  - **본문과 표가 한 자리에서 어긋난다** — 본문은 **청구와 설문(billing and survey) 컴포넌트를
    고객 도메인 아래로 옮겨야 했다**고 적는데 표 5-16에는 설문이 없고, 설문은 앞의 표 5-15에서
    티켓 도메인으로 갔다 (5장, p.125, 사가).[^ford2021-hard-parts] **원문 그대로 두고
    표시한다.**
- **리포팅 도메인** — 첫째 패턴을 적용해 보니 **이미 정렬되어 있어 더 할 일이 없었다.** 네
  컴포넌트(`ss.reporting.shared` · `ss.reporting.tickets` · `ss.reporting.experts` ·
  `ss.reporting.financial`) 전부 목표 네임스페이스가 `Same (no change)`다 (5장, p.125, 사가,
  표 5-17).[^ford2021-hard-parts] 네 행이 모두 같은 값이라 표로 옮기지 않았다.
- **관리자 도메인과 공유 도메인** — 둘 다 정렬이 필요해 **아키텍처 스토리 하나로 묶었다.** 그리고
  **`ss.expert.profile` 네임스페이스를 `ss.experts`로 이름 바꾸기로 했는데, 관리자 도메인 아래에
  불필요한 Expert 서브도메인이 생기는 것을 피하기 위해서**다 (5장, p.126, 사가, 표
  5-18):[^ford2021-hard-parts]

| Component | Domain | Current namespace | Target namespace |
|---|---|---|---|
| Login | Shared | `ss.login` | `aa.shared.login` |
| Notification | Shared | `ss.notification` | `ss.shared.notification` |
| Expert Profile | Admin | `ss.expert.profile` | `ss.admin.experts` |
| User Maintenance | Admin | `ss.users` | `ss.admin.users` |

  - **`aa.shared.login`은 원문 오식이다**(`ss`). 렌더 이미지로 확인해 원문 그대로 옮겼다.
  - **본문이 말한 이름(`ss.experts`)과 표의 목표 값(`ss.admin.experts`)이 다르다.** 뜻은 같은
    방향이다 — 어느 쪽이든 `.profile` 노드를 없애 서브도메인을 만들지 않는다. **원문 그대로
    두고 표시한다.**
  - **이 한 행이 이 패턴의 판정 하나를 보인다** — 네임스페이스를 도메인에 맞추는 일이 늘 노드를
    **더하는** 것은 아니고, 불필요한 중간 층을 **없애기도** 한다. 서브도메인은 저절로 좋은 것이
    아니라 있어야 할 때만 둔다. **저자들이 그것을 규칙으로 올려 적지는 않는다.** #hypothesis
- **이 패턴이 끝나며 다음 패턴이 예고된다** — 이제 **모놀리스를 구조적으로 쪼개어 분산
  아키텍처의 첫 단계로 옮길 준비가 되었다** (5장, p.126, 사가).[^ford2021-hard-parts]

## 이 도메인은 DDD의 하위 도메인인가

**이 KB에는 같은 낱말(도메인·서브도메인)을 업무 쪽 단위로 쓰는 소스가 있다. 부딪히는지 보아
둔다.**

- **재료가 다르다.** 이 페이지의 컴포넌트 도메인은 **모놀리스 안 네임스페이스 트리의 한
  노드**이고, 묶는 기준은 **관련 기능**이며, 판정의 물리적 증거는 **접두가 같은가**다.
  [하위 도메인의 세 종류](../concepts/subdomain-types.md)의 하위 도메인은 **회사가 하는 일의
  한 갈래**이고, 가르는 기준은 **경쟁 우위에 기여하는가·시장에 이미 해법이 있는가**다.[^khononov2021]
- **부딪히지 않는다 — 두 소스가 다른 물음에 답한다.** 이쪽은 **이미 있는 코드를 어떻게 묶느냐**를
  묻고 저쪽은 **업무의 어느 부분에 노력을 쏟느냐**를 묻는다. 이 패턴에는 종류가 없고(핵심·일반·
  보조 같은 구분이 없다) 저쪽에는 네임스페이스가 없다.
- **그래도 한 자리에서 만난다** — 저자들이 이 패턴의 조건을 **도메인 주도 설계가 널리 쓰이기 전에
  지어진 코드**라고 적는다(위
  [도메인 주도 설계 이전에 지어진 코드](#도메인-주도-설계-이전에-지어진-코드)). 곧 **DDD로 지었다면
  네임스페이스가 이미 업무 구획을 반영했을 것**이라는 전제가 깔려 있다. 그 전제를 받으면 컴포넌트
  도메인은 **뒤늦게 복원한 업무 구획**이 된다. **저자들이 그렇게 적지는 않는다.** #hypothesis
- **경계 컨텍스트와는 층이 또 다르다.** [경계 컨텍스트](../concepts/bounded-context.md)는 **한
  모델이 통하는 범위**이고 모델의 일관성이 기준인데, 이 패턴은 모델을 보지 않는다. 다만 이 책
  2장의 곁상자가 **서비스 기반 아키텍처의 서비스도 마이크로서비스와 같은 원칙(경계 컨텍스트)을
  따른다**고 적으므로, 이 패턴의 산출물이 그 이름으로 불릴 여지는 남는다 (2장,
  p.32).[^ford2021-hard-parts] 그 곁상자의 전문은
  [도메인 서비스 만들기](create-domain-services.md)에 있다.
- **이 대질은 이 KB가 세운 것이고 두 소스가 서로를 호명하지 않는다.** #hypothesis

## 이어지는 페이지

- [컴포넌트 기반 분해 패턴 여섯](../concepts/component-based-decomposition-patterns.md) — 이 패턴이
  다섯째로 놓이는 절차
- [컴포넌트 의존 판정](determine-component-dependencies.md) — 이 패턴 앞에 오는 넷째
- [컴포넌트 평탄화](flatten-components.md) — 리프 노드 규정과 이 패턴의 입력이 되는 컴포넌트 목록
- [도메인 서비스 만들기](create-domain-services.md) — 이 묶음을 실제 배포 단위로 만드는 여섯째
- [분해 접근 둘](decomposition-approaches.md) — 여기서 재인용되는 4장의 조언과 그 근거 넷
- [하위 도메인의 세 종류](../concepts/subdomain-types.md) — 같은 낱말을 업무 단위로 쓰는 축
- [경계 컨텍스트](../concepts/bounded-context.md) — 같은 대상을 모델이 통하는 범위로 긋는 축
- [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md) — 위 적합도 함수의 분류 어휘
- [Sysops Squad 사례](sysops-squad-case.md) — 위 사례가 대입되는 체계
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) —
  이 페이지가 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 5장 "Component-Based
    Decomposition Patterns" §"Create Component Domains Pattern"(pp.120–126) — 도입(p.120) ·
    §"Pattern Description"(pp.121–122) · §"Fitness Functions for Governance"(pp.122–123) ·
    §"Sysops Squad Saga: Creating Component Domains"(pp.123–126), 그리고 2장
    §"Service-Based Architecture" 곁상자(p.32). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측).
    직인용 셋(패턴 목적 · 컴포넌트 도메인의 규정 · 4장 조언의 재인용)은 `pdftotext -layout`
    추출로 문자 단위 대조했고 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었다.
    원문이 이탤릭으로 조판한 낱말은 인용 안에서 이탤릭을 유지했다. **표 5-13·5-14·5-15·5-16·
    5-18은 `pdftoppm -r 160 -png`로 렌더해 눈으로 대조한 뒤 원문 열 머리글과 셀 값을 영어
    그대로 옮겼다** — 네임스페이스는 이 KB의 조판 규약에 따라 인라인 코드로 감쌌고 값 자체는
    고치지 않았다. **표 5-17은 네 행의 목표 네임스페이스가 모두 `Same (no change)`라 표로
    옮기지 않고 산문으로 적었다.** **표 5-18의 `aa.shared.login`은 원문 오식이다**(`ss`) —
    렌더 이미지로 확인해 원문 그대로 옮겼다. 본문이 말하는 `ss.experts`와 표의
    `ss.admin.experts`가 어긋나는 것, 그리고 본문이 고객 도메인 리팩터링을 "billing and
    survey"라 적는데 표 5-16에 설문이 없는 것도 원문 그대로 두고 본문에 적었다. 도메인 다섯
    표는 원문 표가 아니라 **사가 한 문단의 열거를 이 KB가 표로 모은 것**이고 그 사실을 표 앞에
    적었다. **ArchUnit 목록 하나(예제 5-10)는 펜스로 옮기지 않고 그 규칙이 하는 일만 산문으로
    적었다** — 이 KB의 적합도 함수 대표 펜스는 ford2022 예제 2-1 하나로 유지한다(SCHEMA §3).
    **도판 둘(그림 5-18 네임스페이스 노드의 이름 · 그림 5-19 다섯 도메인)은 `pdftoppm`으로
    렌더해 눈으로 읽었고**, 그림 5-18은 노드마다 붙은 이름을 표로, 그림 5-19는 묶음의 배치를
    목록으로 옮겼다. 굵은 글씨는 원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

[^khononov2021]: Khononov 2021, 1장 "Analyzing Business Domains" §"Types of Subdomains"
    (pp.4–7) · §"Comparing Subdomains"(pp.7–11). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 26, 실측).
    이 페이지는 그 기준을 대질에만 쓴다 — 전문과 직인용은
    [하위 도메인의 세 종류](../concepts/subdomain-types.md)가 갖는다.

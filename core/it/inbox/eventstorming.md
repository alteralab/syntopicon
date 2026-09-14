---
type: concept
title: 이벤트스토밍
description: 도메인 지식을 나누고 유비쿼터스 언어를 세우기 위해 사람들이 벽에 붙임쪽지로 업무 프로세스를 모델링하는 로우테크 워크숍 — 활동의 규정과 탐색 범위가 업무 프로세스 하나라는 조항, 업무 도메인에 관계된 누구나 부르되 열 명을 넘기지 말라는 참가자 지침과 브란돌리니의 인용, 모델링 공간과 붙임쪽지와 의자를 치우라는 준비물, 구조 없는 탐색에서 시작해 타임라인과 아픈 자리와 중추 사건과 명령과 정책과 읽기 모델과 외부 시스템과 애그리게이트를 거쳐 경계 컨텍스트에 이르는 열 단계와 각 단계가 쓰는 붙임쪽지 색깔의 대응표, 큰 그림만 먼저 훑고 프로세스별로 전량을 다시 도는 변형, 워크숍의 진짜 산출물이 모델이 아니라 지식 공유라는 판정, 쓸 자리 여섯과 쓰지 않을 자리, 범례를 먼저 그리고 활력을 살피라는 진행 요령, 원격 진행의 한계와 다섯 명 제한, 그리고 이것이 원전의 지식 정련과 같은 대상을 다루되 연속적 대화가 아니라 한 번의 집중 행사라는 차이
generated: { by: "claude-opus-5", at: "2026-09-15T12:00:00Z" }
status: draft
sources:
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 이벤트스토밍

- [무엇을 하는 활동인가](#무엇을-하는-활동인가)
- [누구를 부르는가](#누구를-부르는가)
- [무엇이 필요한가](#무엇이-필요한가)
- [열 단계](#열-단계)
- [붙임쪽지 색깔 대응표](#붙임쪽지-색깔-대응표)
- [변형 — 큰 그림 먼저](#변형--큰-그림-먼저)
- [진짜 산출물은 모델이 아니다](#진짜-산출물은-모델이-아니다)
- [쓸 자리와 쓰지 않을 자리](#쓸-자리와-쓰지-않을-자리)
- [진행 요령](#진행-요령)
- [원격으로 할 때](#원격으로-할-때)
- [원전의 지식 정련과 같은 대상인가](#원전의-지식-정련과-같은-대상인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **도메인 지식을 나누고 유비쿼터스 언어를 세우기 위해 사람들을 한 방에 모아
무엇을 어떤 순서로 벽에 붙이는가.**

## 무엇을 하는 활동인가

- 규정 (12장, p.185):[^khononov2021]

> EventStorming is a low-tech activity for a group of people to brainstorm and rapidly model a
> business process. In a sense, EventStorming is a tactical tool for sharing business domain
> knowledge.

- 저자가 이 장을 설계 패턴에서 떼어 놓는다 — **이 장에서는 소프트웨어 설계 패턴과 기법
  논의에서 잠시 쉬어 간다.** 대신 **이벤트스토밍(EventStorming)이라 불리는 로우테크
  모델링 과정**을 다루고, 그 과정이 **앞 장들에서 다룬 도메인 주도 설계의 핵심 측면들을
  한자리에 모은다**고 적는다 (12장, p.185).[^khononov2021]
- **세션에는 범위가 있다** (12장, p.185):[^khononov2021]

> An EventStorming session has a scope: the business process that the group is interested in
> exploring.

  - 그 범위 안에서 하는 일이 정해진다 — **참가자들은 그 프로세스를 타임라인 위에 놓인 붙임쪽지로
    표현된 일련의 도메인 이벤트로 탐색한다. 한 단계씩 모델은 행위자, 명령, 외부 시스템 같은
    추가 개념으로 풍부해지고, 마침내 그 모든 요소가 업무 프로세스가 어떻게 돌아가는지의 이야기를
    들려주게 된다** (12장, p.185).[^khononov2021]
- **"로우테크"는 수사가 아니라 준비물의 서술이다** — 아래 [무엇이 필요한가](#무엇이-필요한가)가
  종이와 펜과 방이라는 목록을 그대로 준다.

## 누구를 부르는가

- 저자가 이 절을 창시자의 말로 연다 (12장, p.186):[^khononov2021]

> Just keep in mind that the goal of the workshop is to learn as much as possible in the shortest
> time possible. We invite key people to the workshop, and we don't want to waste their valuable
> time.

  - 알베르토 브란돌리니(Alberto Brandolini)가 이 워크숍의 창시자다 (12장,
    p.186).[^khononov2021]
- **범위가 넓다** — **이상적으로는 다양한 사람들의 무리가 워크숍에 참여해야 한다. 실제로 문제의
  업무 도메인에 관계된 누구나 참여할 수 있다 — 엔지니어, 도메인 전문가, 제품 책임자, 테스터,
  UI/UX 디자이너, 지원 인력 등이다. 배경이 다른 사람이 많이 관여할수록 더 많은 지식이 발견된다**
  (12장, p.186).[^khononov2021]
- **그러나 상한이 있다** (12장, p.186):[^khononov2021]

> Every participant should be able to contribute to the process, but this can be challenging for
> groups of more than 10 participants.

  - 그 상한이 원격 진행에서 더 내려간다 — 아래 [원격으로 할 때](#원격으로-할-때)를 보라.
- 이 역할의 낱말이 사는 자리는 [도메인 전문가](domain-experts.md)다.

## 무엇이 필요한가

저자가 다섯을 목록으로 준다 (12장, pp.186–187).[^khononov2021]

- **모델링 공간** — **먼저 큰 모델링 공간이 필요하다. 정육점 종이로 덮은 벽 하나가 최고의
  모델링 공간이다.** 큰 화이트보드도 쓸 수 있지만 **가능한 한 커야 한다 — 얻을 수 있는 모든
  모델링 공간이 필요할 것이다.**
- **붙임쪽지(sticky notes)** — **여러 색깔의 붙임쪽지가 많이 필요하다.** 색깔의 관례는
  아래 대응표에 있고, 저자는 **가능하면 이 관례를 지키라**고 한다 — **현재 나와 있는 모든
  이벤트스토밍 책과 교육과 일관되기 위해서**다.
- **마커** — 붙임쪽지에 쓸 것. **보급품이 지식 공유의 병목이 되어서는 안 되므로 모든 참가자에게
  충분한 마커가 있어야 한다.**
- **간식** — **전형적인 이벤트스토밍 세션은 두 시간에서 네 시간쯤 걸린다.**
- **방** — 넓어야 하고 **한가운데 큰 탁자가 있어 참가자들이 자유롭게 움직이고 모델링 공간을
  관찰하는 것을 막지 않도록** 해야 한다. 그리고 **의자는 절대 안 된다. 사람들이 참여하고 지식을
  나누기를 바라는 것이지 구석에 앉아 멍해지기를 바라는 것이 아니다. 따라서 가능하면 의자를
  방에서 빼라.**
  - 이 금지에는 저자 자신의 단서가 각주로 붙어 있다 — **물론 이것은 딱딱한 규칙이 아니다.
    그렇게 오래 서 있기 힘든 참가자가 있으면 의자를 몇 개 남겨 두라** (12장, p.187
    각주 1).[^khononov2021]

## 열 단계

- 절차의 형태가 먼저 규정된다 — **이벤트스토밍 워크숍은 보통 10단계로 진행된다. 각 단계마다
  모델은 추가 정보와 개념으로 풍부해진다** (12장, p.187).[^khononov2021]

1. **구조 없는 탐색(Unstructured Exploration)** — 탐색 대상 업무 도메인에 관계된 도메인
   이벤트를 브레인스토밍한다. **도메인 이벤트는 업무에서 일어난 흥미로운 무엇이다**(A domain
   event is something interesting that has happened in the business). **과거 시제로 적는 것이
   중요하다** — 이미 일어난 일을 서술하는 것이기 때문이다. 이 단계에서 참가자 전원이 주황색
   붙임쪽지를 집어 떠오르는 도메인 이벤트를 적어 붙인다. **순서나 중복은 아직 걱정할 필요가
   없다.** 멈춤 조건이 정해져 있다 — **새 이벤트를 더하는 속도가 눈에 띄게 느려질 때까지
   무리는 도메인 이벤트 생성을 계속해야 한다** (12장, pp.187–188).[^khononov2021]
2. **타임라인(Timelines)** — 만들어진 도메인 이벤트를 업무 도메인에서 일어나는 순서대로
   정렬한다. **이벤트는 "행복한 경로 시나리오", 곧 성공적인 업무 시나리오를 서술하는 흐름에서
   시작해야 한다.** 그것이 끝나면 대안 시나리오(오류를 만나는 경로, 다른 업무 결정이 내려지는
   경로)를 더한다. 분기는 앞 이벤트에서 두 흐름이 나오는 것으로 표현하거나 화살표를 그려
   표현한다. **틀린 이벤트를 고치고 중복을 없애고 빠진 이벤트를 더하는 때도 이 단계다**
   (12장, pp.188–189).[^khononov2021]
3. **아픈 자리(Pain Points)** — 타임라인의 넓은 시야로 주의가 필요한 지점을 찾는다.
   **병목, 자동화가 필요한 수작업 단계, 빠진 문서, 또는 빠진 도메인 지식**이 그것이다.
   비효율을 **명시적으로 만들어 두어야 세션이 진행되는 동안 돌아오기 쉽고 나중에 다루기도
   쉽다.** 표기는 **돌려 붙인(마름모꼴) 분홍 붙임쪽지**다. 그리고 이 단계가 유일한 기회는
   아니다 — **진행자로서 과정 내내 참가자들의 말을 살피고, 문제나 우려가 제기되면 아픈 자리로
   기록하라** (12장, pp.189–190).[^khononov2021]
4. **중추 사건(Pivotal Events)** — 맥락이나 국면의 변화를 가리키는 중요한 업무 이벤트를
   찾아 **그 앞뒤를 가르는 세로 막대로 표시한다.** 주문 과정에서 "shopping cart initialized",
   "order initialized", "order shipped", "order delivered", "order returned"가 그런 변화다.
   **이 단계의 산출물이 곧바로 전략 설계의 재료가 된다** (12장, p.190):[^khononov2021]

   > Pivotal events are an indicator of potential bounded context boundaries.

5. **명령(Commands)** — 규정이 도메인 이벤트와의 대비로 주어진다 (12장,
   p.190):[^khononov2021]

   > Whereas a domain event describes something that has already happened, a command describes what
   > triggered the event or flow of events. Commands describe the system's operations and, contrary
   > to domain events, are formulated in the imperative.

   예가 "Publish campaign" · "Roll back transaction" · "Submit order"다. 표기는 **하늘색
   붙임쪽지**이고 그것이 낳을 이벤트보다 **앞에** 놓인다. 특정 역할의 행위자가 실행하는
   명령이면 **작은 노란 붙임쪽지**로 행위자 정보를 덧붙인다 — **행위자는 고객, 관리자, 편집자
   같은 업무 도메인 안의 사용자 페르소나를 나타낸다.** 다만 **모든 명령에 행위자가 딸리지는
   않으므로 분명한 자리에만 행위자 정보를 더한다** (12장, p.191).[^khononov2021]
6. **정책(Policies)** — 행위자가 붙지 않은 명령들을 자동으로 실행할 자동화 정책을 찾는다
   (12장, p.191):[^khononov2021]

   > An automation policy is a scenario in which an event triggers the execution of a command. In
   > other words, a command is automatically executed when a specific domain event occurs.

   표기는 **이벤트와 명령을 잇는 보라색 붙임쪽지**다. 조건이 걸리면 그 붙임쪽지에 판단 기준을
   명시해 적는다 — "complaint received" 뒤에 escalate 명령을 걸되 VIP 고객의 불만일 때만
   걸고 싶으면 **"only for VIP customers"라고 정책 쪽지에 적는다.** 이벤트와 명령이 멀리
   떨어져 있으면 화살표를 그려 잇는다 (12장, pp.191–192).[^khononov2021]
7. **읽기 모델(Read Models)** — 규정 (12장, p.192):[^khononov2021]

   > A read model is the view of data within the domain that the actor uses to make a decision to
   > execute a command.

   **화면 하나, 보고서, 알림 같은 것**이 여기 든다. 표기는 **초록색 붙임쪽지**이고 행위자의
   결정을 뒷받침하는 정보의 출처를 짧게 적는다. **행위자가 읽기 모델을 본 뒤에 명령을 실행하므로
   모델링 공간에서 읽기 모델은 명령보다 앞에 놓인다** (12장, p.192).[^khononov2021]
8. **외부 시스템(External Systems)** — 규정 (12장, p.193):[^khononov2021]

   > An external system is defined as any system that is not a part of the domain being explored. It
   > can execute commands (input) or can be notified about events (output).

   표기는 **분홍색 붙임쪽지**다. 그리고 이 단계가 닫는 조항이 하나 있다 (12장,
   p.194):[^khononov2021]

   > By the end of this step, all commands should either be executed by actors, triggered by
   > policies, or called by external systems.

9. **애그리게이트(Aggregates)** — 이벤트와 명령이 모두 표현되면 관련된 개념을 애그리게이트로
   묶기 시작한다. 이 워크숍이 쓰는 규정은 극히 짧다 (12장, p.194):[^khononov2021]

   > An aggregate receives commands and produces events.

   표기는 **큰 노란 붙임쪽지**이고 **명령은 왼쪽에 이벤트는 오른쪽에** 붙인다 (12장,
   p.194).[^khononov2021]
10. **경계 컨텍스트(Bounded Contexts)** — 마지막 단계는 **밀접하게 관련된 기능을 나타내거나
    정책으로 결합되어 있어서 서로 관련된 애그리게이트들을 찾는 것**이다. 그렇게 묶인
    애그리게이트 무리가 **경계 컨텍스트 경계의 자연스러운 후보를 이룬다**(The groups of
    aggregates form natural candidates for bounded contexts' boundaries) (12장,
    p.194).[^khononov2021]

## 붙임쪽지 색깔 대응표

저자가 워크숍 시작 전에 이 범례(legend)를 붙임쪽지로 직접 만들어 걸어 두라고 한다 — 아래
[진행 요령](#진행-요령)이 그 지시다. 색깔 값은 원문 표기를 그대로 둔다 (12장,
pp.187–194).[^khononov2021]

| 단계 | 모델 요소 | 붙임쪽지 |
|---|---|---|
| 1 | domain event | orange |
| 3 | pain point | pink, rotated (diamond) |
| 4 | pivotal event | (쪽지가 아니라 세로 막대로 표시) |
| 5 | command | light blue |
| 5 | actor | small yellow |
| 6 | policy | purple |
| 7 | read model | green |
| 8 | external system | pink |
| 9 | aggregate | large yellow |

- **분홍이 두 자리에 쓰인다.** 아픈 자리와 외부 시스템이 같은 색이고, 아픈 자리는 **돌려
  붙여 마름모꼴로** 구분한다 (12장, pp.189·193).[^khononov2021]
- **노랑도 두 자리에 쓰이고 크기로 갈린다** — 행위자는 작은 노랑, 애그리게이트는 큰 노랑이다
  (12장, pp.191·194).[^khononov2021]

## 변형 — 큰 그림 먼저

- 절차의 지위가 먼저 정해진다 (12장, p.195):[^khononov2021]

> Alberto Brandolini, the creator of the EventStorming workshop, defines the EventStorming
> process as guidance, not hard rules.

  - 그래서 **자기에게 가장 맞는 "요리법"을 찾도록 이 과정을 실험해도 된다** (12장,
    p.195).[^khononov2021]
- 저자 자신의 방식이 둘로 나뉜다 (12장, p.195).[^khononov2021]
  - **조직에 이벤트스토밍을 처음 들일 때는 1단계(혼돈스러운 탐색)부터 4단계(중추 사건)까지만
    따라 업무 도메인의 큰 그림을 먼저 탐색하는 것을 선호한다.** 그 결과 모델은 **회사 업무
    도메인의 넓은 범위를 덮고, 유비쿼터스 언어의 튼튼한 기반을 세우고, 경계 컨텍스트의 가능한
    경계를 그려 낸다.**
  - **큰 그림을 얻고 서로 다른 업무 프로세스를 식별한 다음에는 관련된 업무 프로세스마다 전용
    이벤트스토밍 세션을 진행한다** — 이번에는 전 단계를 따라 프로세스 전체를 모델링한다.
- 결과 모델의 후속 쓰임도 적혀 있다 — **그 모델은 이벤트 소싱 도메인 모델을 구현하는 기반으로
  채택될 수 있다.** 그 길로 갈지는 업무 도메인에 달렸고, 가기로 하면 **경계 컨텍스트 경계와
  애그리게이트와 물론 필요한 도메인 이벤트의 청사진을 이미 갖고 있는 것**이다 (12장,
  pp.195–196).[^khononov2021] 그 패턴은
  [이벤트 소싱 도메인 모델](event-sourced-domain-model.md)에 있다.

## 진짜 산출물은 모델이 아니다

- 저자가 결과물의 순위를 뒤집는다 (12장, p.195):[^khononov2021]

> However, all of these are just nice bonuses. The real value of an EventStorming session is the
> process itself—the sharing of knowledge among different stakeholders, alignment of their mental
> models of the business, discovery of conflicting models, and, last but not least, formulation of
> the ubiquitous language.

- 맺음에서 같은 말이 다시 나온다 — **결과 모델과는 별개로 이 워크숍의 일차적 이득은 지식
  공유다**(Apart from the resultant models, its primary benefit is knowledge sharing). 세션이
  끝날 즈음 **모든 참가자가 업무 프로세스에 대한 각자의 정신 모델을 맞추고 유비쿼터스 언어를
  쓰는 첫걸음을 뗀다** (12장, p.198).[^khononov2021]
  - **"충돌하는 모델의 발견"이 이 목록에서 가장 무거운 항목이다.** 한 업무 낱말이 부서마다
    다른 뜻으로 쓰이고 있음이 이 자리에서 드러나고, 그 발견이 곧 4단계의 중추 사건과 10단계의
    경계 후보로 이어진다. 그 낱말이 사는 페이지는
    [경계 컨텍스트](../concepts/bounded-context.md)와 [유비쿼터스 언어](../concepts/ubiquitous-language.md)다.

## 쓸 자리와 쓰지 않을 자리

- 저자가 여섯을 든다 (12장, pp.196–197).[^khononov2021]
  - **유비쿼터스 언어를 세운다** — **무리가 업무 프로세스의 모델을 함께 만들어 가면서 본능적으로
    용어를 동기화하고 같은 언어를 쓰기 시작한다.**
  - **업무 프로세스를 모델링한다** — **DDD 지향 구성 단위에 기반하므로 애그리게이트와 경계
    컨텍스트의 경계를 발견하는 효과적인 방법이기도 하다.**
  - **새 업무 요구사항을 탐색한다** — 새 기능에 대해 **모든 참가자가 같은 이해에 있음을 확실히
    하고 업무 요구사항이 다루지 않은 엣지 케이스를 드러낸다.**
  - **도메인 지식을 되찾는다** — **시간이 지나면 도메인 지식은 사라질 수 있다. 현대화가 필요한
    레거시 시스템에서 특히 심하다.** 이벤트스토밍은 **참가자 각자가 가진 지식을 하나의 정합적인
    그림으로 합치는 효과적인 방법이다.**
  - **기존 업무 프로세스를 개선할 길을 찾는다** — **업무 프로세스의 종단 시야가 비효율과 개선
    기회를 알아채는 데 필요한 관점을 준다.**
  - **새 팀원을 들인다** — **새 팀원과 함께 이벤트스토밍 세션을 진행하는 것이 그들의 도메인
    지식을 넓히는 훌륭한 방법이다.**
- **쓰지 않을 자리도 명시된다** (12장, p.197):[^khononov2021]

> EventStorming will be less successful when the business process you're exploring is simple or
> obvious, such as following a series of sequential steps without any interesting business logic
> or complexity.

  - **이 단서가 이 판본의 다른 판정과 같은 방향이다.** 단순한 로직에 정교한 도구를 걸지 말라는
    것은 [업무 로직 구현 패턴 고르기](choosing-a-business-logic-pattern.md)가 전술 층에서
    내리는 판정과 같고, 여기서는 그것이 워크숍이라는 조직 비용에 걸린다.

## 진행 요령

- **범례를 먼저 만든다** — 이벤트스토밍을 해 본 적 없는 무리와 할 때 저자는 **과정을 빠르게
  개괄하는 것으로 시작하기를 선호한다.** 무엇을 할 것인지, 어떤 업무 프로세스를 탐색할 것인지,
  워크숍에서 쓸 모델링 요소가 무엇인지 설명하면서 **실제로 쓸 붙임쪽지와 이름표로 범례를
  만들어 색 코드를 기억하게 돕는다. 그 범례는 워크숍 내내 모든 참가자에게 보여야 한다**
  (12장, pp.196–197).[^khononov2021]
- **활력을 살핀다** — 워크숍이 진행되는 동안 **무리의 에너지를 추적하는 것이 중요하다.
  움직임이 느려지면 질문을 던져 다시 불붙일 수 있는지, 아니면 다음 단계로 넘어갈 때인지
  보라** (12장, p.197).[^khononov2021]
- **집단 활동으로 다룬다** — **모두가 모델링과 토론에 참여할 기회를 갖도록 하라. 무리에서
  물러나 있는 참가자가 보이면 현재 모델 상태에 대해 질문해 과정에 끌어들이도록 해 보라**
  (12장, p.197).[^khononov2021]
- **쉬는 시간의 규칙이 따로 있다** — 이벤트스토밍은 강도 높은 활동이라 언젠가 쉬어야 하고,
  **모든 참가자가 방에 돌아오기 전에는 세션을 재개하지 마라. 현재 모델 상태를 훑는 것으로
  재개해 무리를 협업 모델링 기분으로 되돌려라** (12장, p.197).[^khononov2021]

## 원격으로 할 때

- **창시자가 반대해 온 자리다** — 이벤트스토밍은 **사람들이 같은 방에서 상호작용하며 함께
  배우는 로우테크 활동으로 발명되었고**, 브란돌리니는 **무리가 한자리에 있지 않으면 같은
  수준의 참여를, 따라서 협업과 지식 공유를 이룰 수 없다는 이유로 원격 진행에 자주 반대해
  왔다** (12장, pp.197–198).[^khononov2021]
- **2020년의 사정이 그것을 강제했다** — **코로나19 대유행의 시작으로 대면 회의를 열고 원래
  의도대로 이벤트스토밍을 하는 것이 불가능해졌다.** 원격 세션의 협업과 진행을 가능하게 하려는
  도구가 여럿 나왔고 **집필 시점에 가장 주목할 만한 것이 miro.com이다.** 저자의 지침은
  **온라인으로 할 때 더 인내하고 소통이 덜 효과적이라는 것을 감안하라**는 것이다 (12장,
  p.198).[^khononov2021]
  - 버전 조건: 2021년 집필 시점의 도구 지목이다 — 협업 화이트보드 제품 이름은 이 KB가
    갱신하지 않는다.
- **인원 상한이 내려간다** (12장, p.198):[^khononov2021]

> While as many as 10 people can attend an in-person EventStorming session, I prefer to limit
> online sessions to five participants.

  - 더 많은 지식이 필요하면 **세션을 여러 번 진행하고 나중에 결과 모델들을 비교해 합칠 수
    있다.** 그리고 저자는 문장 하나로 이 절을 닫는다 — **상황이 허락하면 대면 이벤트스토밍으로
    돌아가라**(When the situation allows, return to in-person EventStorming) (12장,
    p.198).[^khononov2021]

## 원전의 지식 정련과 같은 대상인가

[evans2003](../sources/evans2003.md)에는 이 워크숍이 없다. 그러나 이 워크숍이 스스로 내세우는
목적 — 도메인 전문가와 엔지니어가 함께 모델을 만들고 그 과정에서 유비쿼터스 언어가 생긴다 —
은 원전의 지식 정련(knowledge crunching)이 내세우는 목적과 같다. **모순으로 세우지
않았고, 두 서술이 다루는 것은 같은 활동의 다른 시간 규모다.**

- **원전은 이것을 상시 대화로 규정한다** — 지식 정련은 **탐색이지 절차가 아니고**, 효과적인
  모델링의 재료 다섯 중 첫째가 **모델과 구현을 묶어 두는 것**, 둘째가 **그 모델에 기반한 언어를
  기르는 것**이다. 전문은 [지식 정련](../concepts/knowledge-crunching.md)에 있다.
- **이 판본은 그것을 한 번의 행사로 포장한다** — 두 시간에서 네 시간, 열 명 이하, 열 단계,
  정해진 색 코드. 저자 자신이 이것을 **"전술적 도구"**라 부르고 (12장, p.185),[^khononov2021]
  **워크숍이 끝날 즈음 참가자들이 유비쿼터스 언어를 쓰는 "첫걸음"을 뗀다**고 적는다 (12장,
  p.198).[^khononov2021] **첫걸음이라는 낱말이 이 둘의 관계를 정한다** — 워크숍은 정련을
  대체하지 않고 개시한다.
- **겨루는 자리가 하나 있다면 그것은 도판이 아니라 지속성이다.** 원전은 모델을 계속 고쳐 나가는
  것을 방법론의 중심에 두고, 이 판본의 12장은 그 계속됨에 대해 말하지 않는다. 다만 같은 책의
  11장이 그 자리를 채운다 — **모델링은 진행 중인 과정이고 모델은 업무 도메인의 지식이 더
  얻어지는 대로 개선되어야 한다** (11장, p.179).[^khononov2021] 그래서 이 KB는 둘을 겨루게
  하지 않고, 12장을 **정련의 워크숍 형태**로 읽는다.

## 이어지는 페이지

- [지식 정련](../concepts/knowledge-crunching.md) — 이 워크숍이 포장하는 활동의 원전 층
- [도메인 전문가](domain-experts.md) — 이 워크숍이 방에 불러들이는 사람들
- [유비쿼터스 언어](../concepts/ubiquitous-language.md) — 이 워크숍이 세우려는 것
- [도메인 이벤트](domain-events.md) — 1단계의 주황 쪽지가 되는 구성 단위
- [경계 컨텍스트](../concepts/bounded-context.md) — 4단계와 10단계가 가리키는 경계
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) —
  9단계의 큰 노란 쪽지가 되는 단위
- [이벤트 소싱 도메인 모델](event-sourced-domain-model.md) — 결과 모델이 곧바로 구현으로
  이어질 수 있는 자리
- [브라운필드에 도메인 주도 설계 들이기](applying-ddd-to-brownfield.md) — 이 워크숍이 레거시
  지식 복구 도구로 불려 나오는 자리
- [성장이 낳는 복잡성](growth-driven-complexity.md) — 지식이 사라지는 것을 성장의 다른 얼굴로
  다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^khononov2021]: Khononov 2021, 12장 "EventStorming" 전량(pp.185–198, 연습문제 pp.198–199) ·
    11장 "Evolving Design Decisions" §"Domain Knowledge"(p.179). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 직인용은 `pdftotext -layout` 추출로 문자 단위 대조했고 굽은 따옴표는
    곧은 따옴표로 옮겼다. 원문이 용어의 첫 등장과 준비물 목록의 표제를 기울임으로 조판하는
    관례는 직인용에서 별도로 표시하지 않았다. 브란돌리니 인용(p.186)은 원문이 기울임 인용구로
    조판한 것이라 그 서식만 떼고 옮겼다. **도판 열둘(Figure 12-1~12-12)은 전부 붙임쪽지를
    찍은 사진이거나 그 배치 그림이라 옮기지 않았고, 본문이 그 도판에 대해 적는 것만 산문으로
    옮겼다** — 색깔 대응표의 값은 도판이 아니라 본문이 적는 낱말에서 왔다. 12-12(범례)도
    사진이라 그 안의 이름표를 옮기지 않았다. 이 장에는 코드 목록이 없다. 장 끝 연습문제
    셋(pp.198–199)은 claim이 아니라 옮기지 않았다. 저자가 대는 출처(Alberto Brandolini,
    *Introducing EventStorming*, Leanpub)는 이 KB가 확인한 원전이 아니다.

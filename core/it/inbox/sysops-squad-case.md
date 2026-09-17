---
type: concept
title: Sysops Squad 사례 — 장마다 되돌아오는 운영 예제
status: draft
description: 이 소스가 추상적인 절충 논의를 붙들어 매려고 세운 운영 예제의 설정 — 사가라는 낱말을 트랜잭션 용어가 아니라 사전적 뜻으로 먼저 쓴다는 선언, 전자제품 소매점의 방문 수리 지원 계약이라는 업무 도메인과 관리자·고객·전문가·매니저라는 사용자 넷, 티켓과 무관한 워크플로 넷과 티켓 워크플로 여덟 단계, 티켓 분실과 오배정과 잦은 정지로 사업 철수 위기에 몰린 나쁜 시나리오, 하나의 모놀리스를 이루는 컴포넌트 열여덟과 그 네임스페이스와 책임, 단일 스키마에 놓인 테이블 스물넷과 그 군집, 그리고 장마다 그 장의 기법을 이 사례에 적용해 보이는 사가 상자와 결정 기록이라는 이 책의 조판 규약, 그리고 장마다 그 사례에 무엇을 적용했는지의 색인 — 2장의 퀀텀 대입, 3장의 업무 근거 만들기와 자기 보고를 뒤집는 실측과 합의되지 않은 채 남는 의견, 4장의 분해 접근 고르기와 ADR이 본문에 없는 판정을 더하는 자리, 7장의 세분도 사가 둘과 그 둘이 앞 장들과 달리 쪼개지 않기로 끝난다는 대비
generated: { by: "claude-opus-5", at: "2026-09-17T17:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# Sysops Squad 사례 — 장마다 되돌아오는 운영 예제

- [이 페이지가 무엇인가](#이-페이지가-무엇인가)
- [왜 사가라 부르는가](#왜-사가라-부르는가)
- [업무 도메인 — 펜얼티밋 일렉트로닉스의 지원 계약](#업무-도메인--펜얼티밋-일렉트로닉스의-지원-계약)
- [사용자 넷](#사용자-넷)
- [티켓과 무관한 워크플로](#티켓과-무관한-워크플로)
- [티켓 워크플로 여덟 단계](#티켓-워크플로-여덟-단계)
- [나쁜 시나리오](#나쁜-시나리오)
- [컴포넌트 열여덟](#컴포넌트-열여덟)
- [데이터 모델](#데이터-모델)
- [장마다 붙는 사가 상자와 결정 기록](#장마다-붙는-사가-상자와-결정-기록)
- [이 책이 이 사례에 적용한 것들](#이-책이-이-사례에-적용한-것들)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **분산 아키텍처의 절충을 논할 때 그 논의를 붙들어 맬 구체적인 체계는 어떤
모습이어야 하는가.**

## 이 페이지가 무엇인가

- **저자들이 이 예제를 세우는 이유를 스스로 적는다** — 소프트웨어 아키텍처는 본성상
  추상적이고, 독자가 어떤 플랫폼·기술·상용 소프트웨어의 조합을 갖고 있을지 알 수 없으며
  **둘로 똑같은 경우가 없다.** 그래서 추상적인 착상을 다루되 **구체로 만들려면 구현 세부에
  얹어야 하고**, 그 자리가 이 예제다 (1장 §"Architecture Versus Design: Keeping Definitions
  Simple", p.15).[^ford2021-hard-parts]
- **저자들이 드는 또 하나의 이유는 기존 체계라는 조건이다** — 소프트웨어 아키텍처를 다루는
  많은 책이 **새로 짓는 일**을 다루지만 **현실의 문제는 이미 있는 체계 안에서 생긴다.** 그래서
  이 이야기는 **이미 서 있는 Sysops Squad 아키텍처에서 출발한다** (1장,
  p.15).[^ford2021-hard-parts]
- 이 KB에는 같은 구실을 하는 페이지가 이미 둘 있다 —
  [화물 운송 예제](cargo-shipping-example.md)와 [마켓노버스 사례 연구](marketnovus-case-study.md)다.
  **셋의 성격이 다르다**: 화물 운송은 한 저자가 지어낸 도메인에 패턴들을 함께 세워 보이는
  설계 연습이고, 마켓노버스는 저자 자신의 회사에서 실제로 일어난 일의 사후 기록이며, 이
  사례는 **지어낸 도메인이되 장마다 같은 체계를 다시 손대며 절충을 비교하는 매체**다. **이
  대비는 이 KB가 세운 것이고 세 소스 중 어느 쪽도 상대를 호명하지 않는다.** #hypothesis

## 왜 사가라 부르는가

- **저자들이 이 절을 사전 항목으로 연다** (1장 §"Introducing the Sysops Squad Saga",
  p.15):[^ford2021-hard-parts]

  > saga
  >
  > A long story of heroic achievement.
  >
  > —Oxford English Dictionary

- **그리고 곧바로 낱말의 두 쓰임을 가른다** — 이 책은 **문자 그대로의 사가와 비유적인 사가를
  모두** 다룬다. 아키텍트들이 **사가라는 말을 분산 아키텍처의 트랜잭션 행동을 가리키는 데
  차용해 왔고** 그쪽은 12장이 자세히 다루지만, 여기서 시작하는 것은 **문자 그대로의 사가**,
  곧 Sysops Squad의 이야기다 (1장, p.15).[^ford2021-hard-parts]
  - 차용된 쪽 어휘의 전문은 [사가 패턴](saga-pattern.md)에 있다.

## 업무 도메인 — 펜얼티밋 일렉트로닉스의 지원 계약

- **펜얼티밋 일렉트로닉스(Penultimate Electronics)는 전국에 소매점을 여럿 둔 대형 전자제품
  업체다.** 고객이 컴퓨터·TV·오디오 같은 전자 장비를 살 때 **지원 플랜(support plan)을 함께
  구매할 수 있고**, 문제가 생기면 **고객을 직접 상대하는 기술 전문가 집단(the Sysops Squad)이
  고객의 집이나 사무실로 찾아가 장비를 고친다** (1장, pp.15–16).[^ford2021-hard-parts]

## 사용자 넷

- **Sysops Squad 티켓팅 응용의 주 사용자는 넷이다** (1장, p.16):[^ford2021-hard-parts]

| 사용자 | 하는 일 |
|---|---|
| 관리자(Administrator) | 전문가 명단과 그들의 기량·위치·가용성을 포함한 내부 사용자를 유지한다. 고객 청구 처리 전부를 관리하고, 지원 제품 목록이나 이름-값 쌍 같은 **정적 참조 데이터**를 유지한다 |
| 고객(Customer) | 서비스에 등록하고 자기 프로필·지원 계약·청구 정보를 유지한다. **문제 티켓을 넣고** 작업이 끝난 뒤 설문에 답한다 |
| Sysops Squad 전문가(expert) | 배정된 문제 티켓을 받아 고친다. **지식 베이스를 뒤져** 해법을 찾고 수리 기록을 남긴다 |
| 매니저(Manager) | 문제 티켓 운영을 추적하고 전체 티켓 체계에 대한 **운영 보고서와 분석 보고서**를 받는다 |

## 티켓과 무관한 워크플로

- **관리자와 매니저와 고객이 하는 일 중 문제 티켓과 무관한 것들**이다 (1장 §"Nonticketing
  Workflow", p.16):[^ford2021-hard-parts]
  1. 전문가가 관리자를 통해 체계에 **추가되고 유지된다** — 관리자가 그들의 지역·가용성·기량을
     입력한다.
  2. 고객이 체계에 **등록하고**, 구매한 제품에 따라 **여러 개의 지원 플랜**을 갖는다.
  3. 고객은 프로필에 담긴 신용카드 정보로 **매달 자동 청구된다.** 청구 이력과 명세서를 체계에서
     볼 수 있다.
  4. 매니저가 **재무 보고서·전문가 성과 보고서·티켓 보고서를 포함한 여러 운영 보고서와 분석
     보고서**를 요청해 받는다.

## 티켓 워크플로 여덟 단계

- **고객이 문제 티켓을 넣는 데서 시작해 수리 뒤 설문을 마치는 데서 끝난다** (1장 §"Ticketing
  Workflow", p.17):[^ford2021-hard-parts]
  1. 지원 플랜을 구매한 고객이 **웹사이트로 문제 티켓을 넣는다.**
  2. 티켓이 들어오면 체계가 **기량·현재 위치·서비스 구역·가용성에 근거해** 어느 전문가가 그 일에
     가장 맞는지 정한다.
  3. 배정된 티켓이 **전문가의 모바일 기기에 있는 전용 앱으로 올라가고**, 전문가는 새 티켓이
     있다는 문자 메시지도 받는다.
  4. 고객은 **프로필 선호에 따라 SMS 문자나 이메일로** 전문가가 가고 있다는 통지를 받는다.
  5. 전문가가 모바일 앱으로 티켓 정보와 위치를 받는다. **지식 베이스에도 접근해** 과거에 같은
     문제를 어떻게 고쳤는지 찾을 수 있다.
  6. 문제를 고치면 전문가가 티켓을 **"완료"로 표시한다.** 그런 다음 문제와 수리에 대한 정보를
     지식 베이스에 더할 수 있다.
  7. 완료 통지를 받은 체계가 고객에게 **설문 링크가 담긴 이메일**을 보내고 고객이 그것을 채운다.
  8. 체계가 완료된 설문을 받아 **설문 정보를 기록한다.**

## 나쁜 시나리오

- **현재의 문제 티켓 체계는 여러 해 전에 개발된 큰 모놀리식 응용이다.** 저자들이 세는 증상들
  (1장 §"A Bad Scenario", p.17):[^ford2021-hard-parts]
  - **티켓이 사라져 기사가 아예 나타나지 않는다**는 고객 불만.
  - **엉뚱한 기사가 와서** 자기가 모르는 것을 고치려 한다는 불만.
  - **새 문제 티켓을 넣으려 할 때 체계가 늘 살아 있지는 않다**는 불만.
- **변경도 어렵고 위험하다** — 이 큰 모놀리스에서 무언가를 바꾸면 **대개 너무 오래 걸리고 다른
  무언가가 깨진다** (1장, p.17).[^ford2021-hard-parts]
- **신뢰성 문제로 체계가 자주 "얼어붙거나" 죽고**, 문제를 짚어 응용을 재시작할 때까지 **5분에서
  두 시간까지** 모든 기능이 어디서도 쓸 수 없게 된다 (1장, p.17).[^ford2021-hard-parts]
- **판돈이 걸려 있다** — 곧 무언가 하지 않으면 펜얼티밋 일렉트로닉스는 **아주 수익성 높은 지원
  계약 사업을 접고** Sysops Squad의 관리자·전문가·매니저와 IT 개발 인력 전부를 — **아키텍트를
  포함해** — 해고해야 한다 (1장, p.18).[^ford2021-hard-parts]

## 컴포넌트 열여덟

- **모놀리스 하나가 티켓 관리·운영 보고·고객 등록·청구와, 사용자 유지·로그인·전문가 기량과
  프로필 유지 같은 일반 관리 기능까지 전부 처리한다.** 네임스페이스의 `ss.` 부분이 Sysops Squad
  응용 컨텍스트를 가리킨다 (1장 §"Sysops Squad Architectural Components",
  p.18).[^ford2021-hard-parts]
- **표 1-1의 열과 값을 그대로 옮긴다** (1장, p.19):[^ford2021-hard-parts]

| Component | Namespace | Responsibility |
|---|---|---|
| Login | `ss.login` | Internal user and customer login and security logic |
| Billing payment | `ss.billing.payment` | Customer monthly billing and customer credit card info |
| Billing history | `ss.billing.history` | Payment history and prior billing statements |
| Customer notification | `ss.customer.notification` | Notify customer of billing, general info |
| Customer profile | `ss.customer.profile` | Maintain customer profile, customer registration |
| Expert profile | `ss.expert.profile` | Maintain expert profile (name, location, skills, etc.) |
| KB maint | `ss.kb.maintenance` | Maintain and view items in the knowledge base |
| KB search | `ss.kb.search` | Query engine for searching the knowledge base |
| Reporting | `ss.reporting` | All reporting (experts, tickets, financial) |
| Ticket | `ss.ticket` | Ticket creation, maintenance, completion, common code |
| Ticket assign | `ss.ticket.assign` | Find an expert and assign the ticket |
| Ticket notify | `ss.ticket.notify` | Notify customer that the expert is on their way |
| Ticket route | `ss.ticket.route` | Send the ticket to the expert's mobile device app |
| Support contract | `ss.supportcontract` | Support contracts for customers, products in the plan |
| Survey | `ss.survey` | Maintain surveys, capture and record survey results |
| Survey notify | `ss.survey.notify` | Send survey email to customer |
| Survey templates | `ss.survey.templates` | Maintain various surveys based on type of service |
| User maintenance | `ss.users` | Maintain internal users and roles |

- **그림 1-3이 같은 컴포넌트들을 모놀리스 하나 안에 그린다.** 도판이 이미지 조판이라 재현하지
  않았고, 본문이 적지 않는 배치 하나만 옮긴다 — **사용자 인터페이스가 맨 위에 한 덩어리로
  놓이고 나머지 열여덟 컴포넌트가 그 아래에 들어간다** (1장, p.18).[^ford2021-hard-parts]

## 데이터 모델

- **컴포넌트 열여덟이 데이터베이스의 단일 스키마 하나를 함께 쓴다.** 그 스키마가 고객·사용자·
  계약·청구·결제·지식 베이스·고객 설문을 영속화한다 (1장 §"Sysops Squad Data Model",
  p.19).[^ford2021-hard-parts]
- **표 1-2의 열과 값을 그대로 옮긴다** (1장, pp.20–21):[^ford2021-hard-parts]

| Table | Responsibility |
|---|---|
| Customer | Entities needing Sysops support |
| Customer_Notification | Notification preferences for customers |
| Survey | A survey for after-support customer satisfaction |
| Question | Questions in a survey |
| Survey_Question | A question is assigned to the survey |
| Survey_Administered | Survey question is assigned to customer |
| Survey_Response | A customer's response to the survey |
| Billing | Billing information for support contract |
| Contract | A contract between an entity and Sysops for support |
| Payment_Method | Payment methods supported for making payment |
| Payment | Payments processed for billings |
| SysOps_User | The various users in Sysops |
| Profile | Profile information for Sysops users |
| Expert_Profile | Profiles of experts |
| Expertise | Various expertise within Sysops |
| Location | Locations served by the expert |
| Article | Articles for the knowledge base |
| Tag | Tags on articles |
| Keyword | Keyword for an article |
| Article_Tag | Tags associated to articles |
| Article_Keyword | Join table for keywords and articles |
| Ticket | Support tickets raised by customers |
| Ticket_Type | Different types of tickets |
| Ticket_History | The history of support tickets |

- **그림 1-4가 그 테이블들의 ER 모델이다.** 도판이 이미지 조판이라 **`pdftoppm -r 160 -png`로
  렌더해 눈으로 읽었고**, 재현하지 않고 도판이 음영으로 묶어 놓은 **군집만** 옮긴다 (1장,
  p.20):[^ford2021-hard-parts]

| 군집 | 테이블 |
|---|---|
| 지식 베이스 | `Tag` · `Keyword` · `Article` · `Article_Tag` · `Article_Keyword` |
| 고객 | `Customer` · `Customer_Notification` |
| 청구 | `Contract` · `Billing` · `Payment` · `Payment_Method` |
| 사용자와 전문가 | `Sysops_User` · `Profile` · `Expert_Profile` · `Expertise` · `Location` |
| 티켓 | `Ticket` · `Ticket_Type` · `Ticket_History` |
| 설문 | `Survey` · `Question` · `Survey_Question` · `Survey_Administered` · `Survey_Response` |

  - 도판 안쪽 설명이 **"Tables in the Sysops database (columns and views omitted for
    brevity)"**라고 적는다 — 열과 뷰는 도판에서 생략돼 있다 (1장, p.20).[^ford2021-hard-parts]
- **스키마의 성격이 한 문단으로 규정된다** — **표준적인 제3정규형 데이터 모델이고 저장
  프로시저나 트리거는 몇 개 없다.** 다만 **뷰는 꽤 여럿 있고 주로 Reporting 컴포넌트가 쓴다**
  (1장, p.21).[^ford2021-hard-parts]
  - **그리고 이 사실이 뒤의 모든 분해 논의에 조건을 건다** — 아키텍처 팀이 응용을 쪼개
    분산 아키텍처로 옮기려면 **데이터베이스 팀과 함께 데이터베이스 층의 일을 해야 한다**
    (1장, p.21).[^ford2021-hard-parts] 그 물음의 이 KB 쪽 자리는
    [데이터 분해가 부르는 관심사](data-decomposition-concerns.md)다.

## 장마다 붙는 사가 상자와 결정 기록

- **이 사례는 장마다 되돌아온다** — 저자들은 **각 장에서 이 사가를 써서 그 장이 설명한 기법과
  절충을 보인다**고 적는다 (1장, p.15).[^ford2021-hard-parts] 컴포넌트 목록과 데이터베이스
  설정도 같은 구실로 쓰인다 — **응용을 분산 아키텍처로 쪼갤 때의 기법과 절충을 보이는 데**
  뒤의 장들이 이 컴포넌트들을 쓰고 (1장, p.19), **데이터베이스를 쪼개는 기법과 절충을 논하는
  데** 이 테이블과 뷰 설정을 쓴다 (1장, p.21).[^ford2021-hard-parts]
- **결정은 ADR 형식의 상자로 붙는다** — 이 책은 **본문에서 내려지는 여러 아키텍처 결정을 ADR로
  문서화하며**, 책이 만든 모든 ADR의 목록은 **부록 B**에 있다 (1장 §"Architectural Decision
  Records", p.5).[^ford2021-hard-parts] 그 형식의 전문은
  [아키텍처 결정 기록](architecture-decision-records.md)에 있다.
- **사가 상자는 서사체로 조판된다** — 날짜와 시각이 붙은 장면에서 등장인물들이 말을 주고받는
  형식이고, 이름은 로건(Logan, 펜얼티밋 일렉트로닉스의 수석 아키텍트)·애디슨(Addison)·
  오스틴(Austen)이다 (2장, pp.25–26, 사가).[^ford2021-hard-parts]

## 이 책이 이 사례에 적용한 것들

**장마다 그 장의 어휘를 이 체계에 대입한 자리를 locator와 함께 모은다.**

| 장 | 이 사례에 무엇을 했는가 | locator |
|---|---|---|
| 2장 | **정적 퀀텀 결합과 동적 퀀텀 결합을 자기 서비스에 대입한다** — 서비스 하나를 맨바닥에서 부팅하는 데 필요한 배선이 무엇인지 세고(자바·SpringBoot·프레임워크 15~20개·Postgres·도커·이벤트 브로커), 그 정적 결합 다이어그램을 **신뢰성 분석**에 쓰며, 티켓팅과 배정 사이의 호출을 동기로 할지 비동기로 할지를 **탄력성** 차이로 판정한다 | 2장 §"Sysops Squad Saga: Understanding Quanta"(pp.42–44), 사가 |
| 3장 | **업무 후원자에게 낼 근거를 만든다** — 지금 겪는 증상 하나하나를 모듈성 구동 요인 다섯에 대응시키고(변경의 어려움은 유지보수성, 주석 처리된 테스트 30%는 테스트 가능성, 월 1회 릴리스는 배포 가능성, 설문·리포팅이 체계를 내리는 것은 가용성, 동시 25명에서의 정지는 확장성), 그 대응을 **분산 아키텍처로 옮긴다는 결정**으로 묶는다 | 3장 §"Sysops Squad Saga: Creating a Business Case"(pp.59–62), 사가·ADR |
| 4장 | **분해 접근을 고른다** — 추상도와 불안정도로 코드를 찍어 **대부분이 주계열 위에 있다**고 읽어 분해 가능성을 확인한 뒤, 전술적 포크와 컴포넌트 기반 분해를 놓고 **중복 코드와 공유 기능**(로깅·보안·지속성 층)을 근거로 컴포넌트 기반 분해를 택한다 | 4장 §"Sysops Squad Saga: Choosing a Decomposition Approach"(pp.78–79), 사가·ADR |
| 5장 | **컴포넌트의 크기를 잰다** — 전체 82,931문장을 분모로 컴포넌트별 비율을 계산해 **리포팅 컴포넌트 하나가 33%**임을 찾아내고, 그 안에서 세 리포트 범주와 공유 코드를 식별해 **넷으로 가른다**. 그 결과 `ss.reporting`은 컴포넌트가 아니라 서브도메인이 된다 | 5장 §"Sysops Squad Saga: Sizing Components"(pp.90–93), 사가 |
| 5장 | **공통 도메인 컴포넌트를 모은다** — 알림 컴포넌트 셋을 후보로 잡고 합치기 전에 **구심 결합을 재어** 셋의 합(5)과 합친 하나(5)가 같음을 확인한 뒤 `ss.notification` 하나로 합친다 | 5장 §"Sysops Squad Saga: Gathering Common Components"(pp.97–101), 사가 |
| 5장 | **컴포넌트를 평탄화한다** — 티켓은 **복잡하고 자주 바뀌어서** 루트의 고아 클래스 45개를 올려 세 컴포넌트로 가르고, 설문은 **단순하고 거의 안 바뀌어서** 템플릿 일곱 클래스를 내려 하나로 합친다 | 5장 §"Sysops Squad Saga: Flattening Components"(pp.107–110), 사가 |
| 5장 | **컴포넌트 의존을 판정한다** — IDE 플러그인으로 의존 다이어그램을 만들자 의존이 많아 낙담하지만, 티켓팅·리포팅의 **공유 코드 컴포넌트가 컴파일 기반 참조라 서비스가 아니라 공유 라이브러리가 될 것**이라고 보아 걸러 내자 의존이 적어 보인다. 그래서 **쪼개기 좋은 후보**라고 합의한다 | 5장 §"Sysops Squad Saga: Identifying Component Dependencies"(pp.118–120), 사가 |
| 5장 | **컴포넌트 도메인을 만든다** — 제품 책임자와 함께 도메인 다섯(Ticketing·Reporting·Customer·Admin·Shared)을 식별하고, 도메인 다이어그램으로 **빠진 컴포넌트가 없고 응집이 좋은지** 검증한 뒤 도메인마다 네임스페이스 리팩터링을 아키텍처 스토리로 적는다 | 5장 §"Sysops Squad Saga: Creating Component Domains"(pp.123–126), 사가 |
| 5장 | **도메인 서비스를 만든다** — 컴포넌트를 **한 번에 하나씩** 모놀리스에서 뽑아 새 작업 공간으로 옮기고 사용자 인터페이스가 그 기능을 원격으로 접근하게 바꾸어, 다섯 도메인 서비스로 이루어진 **서비스 기반 아키텍처**에 이른다 | 5장 §"Sysops Squad Saga: Creating Domain Services"(pp.129–130), 사가 |
| 6장 | **데이터베이스를 쪼갤 근거를 데이터 아키텍트에게 낸다** — 리포팅 질의가 커넥션을 전부 차지해 티켓 질의가 타임아웃되는 로그와 지표를 보이고, 쪼갠 뒤 필요한 커넥션이 **2,000개 더**라는 추정을 내고, 모놀리식 데이터베이스가 내려가면 모든 서비스가 멎는다는 내결함성 논거와 **데이터베이스가 정적 결합의 일부라 퀀텀을 하나로 묶는다**는 논거를 더해 반대를 돌려세운다 | 6장 §"Sysops Squad Saga: Justifying Database Decomposition"(pp.150–151), 사가 |
| 6장 | **테이블 스물넷을 데이터 도메인 여섯에 배정한다** — 1장의 데이터 모델이 여기서 Customer·Survey·Payment·Profile·Knowledge base·Ticketing으로 갈리고, Payment 도메인의 뷰에서 고객 테이블 조인을 걷어 내는 자리가 도메인을 가로지르는 의존 제거의 실물이 된다 | 6장 §"Decomposing Monolithic Data"(pp.152–155) |
| 6장 | **설문 도메인 하나만 다른 종류의 데이터베이스로 옮긴다** — 데이터 아키텍처 책임자의 거부를 업무 쪽 고통점(마케팅 부서가 요구하는 설문 변경의 유연성과 적시성)으로 돌려세우고, 문서 데이터베이스로 가기로 한 뒤 **단일 애그리게이트와 쪼갠 애그리게이트를 둘 다 모델링해** 절충을 눈으로 본 다음, 설문 종류가 다섯뿐이라는 규모 실측을 근거로 **질문 데이터의 중복을 변경과 렌더링의 쉬움과 맞바꾼다** | 6장 §"Sysops Squad Saga: Polyglot Databases"(pp.179–184), 사가·ADR |
| 7장 | **티켓 배정과 라우팅을 쪼갤지 정한다** — 배정 알고리즘이 한 달에 두세 번 바뀐다는 **코드 변동성** 근거로 쪼개자는 주장이 나오지만, 전문가를 찾으면 곧바로 라우팅되고 못 찾으면 되말해야 한다는 **워크플로** 근거에 밀려 **합쳐진 서비스 하나**로 간다. 격리하고 싶다는 요구는 **한 서비스 안의 네임스페이스 셋**(배정·라우팅·공유 코드)으로 받는다 | 7장 §"Sysops Squad Saga: Ticket Assignment Granularity"(pp.209–212), 사가·ADR |
| 7장 | **고객 등록을 몇 서비스로 할지 정한다** — 선택지 셋(하나·넷·민감과 비민감 둘)을 놓고 제품 책임자의 **전부 또는 전무** 요구와 보안 전문가의 **접근 통제** 요구가 부딪히는데, 카드와 비밀번호가 이미 토큰화·암호화돼 있음을 확인한 뒤 **보안을 아키텍처가 아니라 설계로**(API 계층과 서비스 메시 양쪽의 보안 라이브러리) 옮겨 **합쳐진 서비스 하나**로 간다 | 7장 §"Sysops Squad Saga: Customer Registration Granularity"(pp.212–216), 사가·ADR |
| 8장 | **공통 인프라 로직을 어디에 둘지 정한다** — 공유 라이브러리와 서비스가 둘 다 로그를 써서 **로그가 두 번 찍히는** 증상에서 출발해, 그것을 **운영 공유 행위**라는 부류로 이름 짓고 **사이드카와 서비스 메시**로 답한다. 도메인 클래스를 사이드카에 넣지 말라는 규칙이 여기서 만들어지고, 유틸리티 라이브러리를 넣을지는 **필요로 하는 팀의 비율**(16~17개 중 5개)로 판정해 넣지 않기로 한다. 사이드카는 **공유 인프라 팀**이 소유한다 | 8장 §"Sysops Squad Saga: Common Infrastructure Logic"(pp.239–241), 사가·ADR |
| 8장 | **티켓 서비스 셋이 공유하는 데이터베이스 로직을 어디에 둘지 정한다** — 공유 데이터 서비스와 공유 DLL을 놓고 **가설 기반 접근**으로 공유 데이터 서비스를 가설로 세운 뒤 반대편에게 "왜"를 물어 절충을 쌓게 한다. 판정을 뒤집은 것은 **저장소 커밋 이력**이다 — 그 공유 클래스가 생각보다 훨씬 덜 바뀌었다는 실측이 나오자 공유 라이브러리로 간다 | 8장 §"Sysops Squad Saga: Shared Domain Functionality"(pp.244–247), 사가·ADR |

- 2장의 그 장면이 남기는 판정 둘 — **아키텍처 퀀텀이 DDD의 경계 컨텍스트를 아키텍처의 말로
  규정한 것**이라는 등가 진술과, **호출의 성질에 따라 두 퀀텀이 호출이 도는 동안만 일시적으로
  얽힐 수 있다**는 관찰이다 (2장, pp.42–44, 사가).[^ford2021-hard-parts] 그 어휘의 전문은
  [아키텍처 퀀텀](architectural-quantum.md)에 있다.
- **3장의 장면이 남기는 방법론적 요점 셋.**
  - **자기 보고를 실측이 뒤집는다** — 한쪽이 "자동화된 단위 테스트가 있으니 테스트 가능성은
    됐다"고 말하자 다른 쪽이 **테스트 케이스의 30% 넘게가 주석 처리되거나 낡았고 핵심 워크플로에
    테스트가 없다**는 것을 보여 그 판단을 뒤집는다 (3장, p.60, 사가).[^ford2021-hard-parts]
  - **두 인물의 의견이 갈린 채 남는다** — 배포 문제가 **아키텍처 문제가 아니라 순전히 배포
    파이프라인 문제**라는 쪽과 **아키텍처와도 관련된다**는 쪽이 갈리고, 앞쪽이 **어느 시점에는
    파이프라인도 고쳐야 한다**는 자기 주장을 거두지 않는다 (3장, p.60,
    사가).[^ford2021-hard-parts] **사가가 합의만 보이지는 않는다는 실물이다.**
  - **계측이 근거를 바꾼다** — 무엇이 체계를 내리는지 재 보니 핵심 티켓 기능이 아니라 **설문
    기능과 리포팅**이었고, 그래서 **그 둘만 떼면 결함을 격리하면서 핵심 기능을 살려 둘 수
    있다**는 근거가 그 자리에서 만들어진다 (3장, pp.60–61, 사가).[^ford2021-hard-parts]
  - 다섯 구동 요인의 전문은 [아키텍처 모듈성의 구동 요인](modularity-drivers.md)에 있다.
- **5장의 사가 여섯 어디에도 ADR 상자가 없다.** 결정이 기록되는 자리에서는 ADR이 아니라
  **아키텍처 스토리**가 쓰이고 개발자에게 배정된다 (5장, pp.92·99·109·124·125·126,
  사가).[^ford2021-hard-parts]
  - **여섯 가운데 넷만 무언가를 기록한다** — 크기 맞추기·공통 컴포넌트 모으기·평탄화·도메인
    만들기의 사가가 아키텍처 스토리를 남기고, **의존 판정의 사가는 판정만 하고 아무것도 적지
    않으며** 도메인 서비스 만들기의 사가는 **이행 계획**을 세운다. **저자들이 그 차이를 적지는
    않는다.** #hypothesis 그 형식은
  [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md)
  §"아키텍처 스토리 — 리팩터링을 적는 단위"에 있다.
  - **이 사가들이 앞 장들과 다른 점 하나** — 여기서는 인물들이 결정을 내리는 것만이 아니라
    **코드를 실제로 옮긴 결과 표**가 장면마다 딸린다. 컴포넌트 목록이 사가를 거치며 바뀌고, 그
    바뀐 목록이 다음 패턴의 입력이 된다.
  - **한 사가에서 개발자에게 물어본 것이 판정을 바꾼다** — `ss.survey.templates` 네임스페이스를
    처음 만든 개발자에게 이유를 묻자 **떼어 놓을 강력한 이유가 없었다**는 답이 나왔고, 그것이
    합치기 결정의 근거가 된다 (5장, p.109, 사가).[^ford2021-hard-parts] **코드의 구조가 설계
    의도가 아니라 우연일 수 있다는 실물이다.**
- **5장 후반의 사가들이 본문에 없는 절차를 둘 더한다.**
  - **거르기** — 의존 다이어그램에서 공유 라이브러리가 될 컴포넌트를 빼고 다시 보는 조작이고,
    그 조작이 "쪼갤 수 있는가"의 답을 뒤집는다 (5장, p.119, 사가).[^ford2021-hard-parts] 본문의
    패턴 서술에는 그 단계가 없다.
  - **업무 쪽과의 합의** — 도메인 목록을 제품 책임자와 함께 정하고, **어디에도 안 붙는
    컴포넌트가 남으면 더 협업하라**는 실패 신호까지 사가가 적는다 (5장, p.123,
    사가).[^ford2021-hard-parts] 두 절차의 전문은
    [컴포넌트 의존 판정](determine-component-dependencies.md)과
    [컴포넌트 도메인 만들기](create-component-domains.md)에 있다.
- **6장 전반의 사가가 앞 장들과 다른 점 하나** — 여기서는 인물들이 **합의한 상태에서 출발하지
  않는다.** 데이터 아키텍트가 **쪼갤 이유가 없다**며 거부한 채 장이 시작하고, 사가는 그 거부를
  돌려세우는 장면이다 (6장, p.131, 사가).[^ford2021-hard-parts] 저자들이 그 자리에서 절차적
  교훈도 하나 적는다 — 아키텍트가 **처음 논의에 그를 넣었어야 했다고 사과한다** (6장, p.132,
  사가).
  - **설득의 재료가 전부 기술 지표다** — 로그와 지표, 커넥션 풀 추정, 예상 인스턴스 수다.
    3장의 사가가 업무 후원자에게 **출시 속도와 경쟁 우위**를 댄 것과 대비된다.
  - **데이터 아키텍트가 조건을 하나 깐다** — **서비스가 여러 데이터베이스나 스키마에 연결하지
    않는 것**이고, 그것이 다음 절의 3단계가 집행하는 규칙과 같다 (6장, p.151,
    사가).[^ford2021-hard-parts] 여덟 구동 요인과 다섯 단계의 전문은
    [데이터 분해의 구동 요인](data-decomposition-drivers.md)과
    [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md)에 있다.
  - **이 사가에도 ADR 상자가 없다.** 부록 B의 쪽 목록에서 p.79 다음이 p.184이므로 6장 전반
    (pp.131–161)에는 ADR이 하나도 없다.
- **6장 후반의 사가가 같은 구도를 한 번 더 돌리는데 재료가 다르다.** 데이터 아키텍처 책임자가
  **설문 테이블은 과거에 관계형으로 늘 잘 동작했으니 바꿀 이유가 없다**며 다시 거부하고, 이번에
  그를 돌려세운 것은 지표가 아니라 **업무 쪽 고통**이다 — 제품 책임자가 **마케팅 부서가 설문
  변경의 유연성과 적시성을 요구하며 가장 단순한 변경조차 며칠이 걸리는 것이 받아들일 수 없다**고
  말하는 장면이 근거가 된다 (6장, pp.179–180, 사가).[^ford2021-hard-parts]
  - **거부한 쪽이 요구한 것이 "탄탄한 정당화"였다** — 다른 종류의 데이터베이스를 섞으려면 그것을
    가져오라는 조건이고 (6장, p.179, 사가), 같은 절의 별점표가 그 정당화의 재료다. 그 표는
    [데이터베이스 종류 고르기](selecting-a-database-type.md)에 있다.
  - **이 장면이 6장 전반의 사가와 짝을 이룬다** — 전반은 **쪼갤 것인가**를 기술 지표로 설득했고,
    후반은 **무엇에 담을 것인가**를 업무 고통으로 설득한다. **두 번 모두 같은 인물이 반대편에
    서고 두 번 모두 돌아선다.**
  - **결정을 내린 방식도 앞 장들과 다르다** — 두 대안을 말로 견주는 대신 **둘 다 모델링해 눈으로
    절충을 본다**(단일 애그리게이트 문서와 쪼갠 애그리게이트 문서). 그리고 판정의 근거가 규모의
    실측이다 — **설문 종류가 다섯뿐이고 변경의 대부분이 질문을 더하거나 빼는 일**이라는 것 (6장,
    pp.181·184, 사가).[^ford2021-hard-parts]
  - **6장 전체에서 ADR은 이 결정 하나뿐이다** (6장, p.184, ADR). 그 전문은
    [아키텍처 결정 기록](architecture-decision-records.md)에 있다.
- **4장의 ADR이 본문에 없는 판정을 하나 더한다** — **전술적 포크에서는 포크할 애플리케이션 수를
  알기 위해 서비스 경계를 미리 정해야 하지만, 컴포넌트 기반 분해에서는 서비스 정의가 컴포넌트
  묶기를 통해 자연스럽게 떠오른다**는 것이다 (4장, p.79, ADR).[^ford2021-hard-parts] 4장 본문의
  두 절 어느 쪽도 그렇게 적지 않는다. 두 접근의 전문은
  [분해 접근 둘](decomposition-approaches.md)에 있다.
  - 귀결 칸이 더하는 것도 하나 있다 — **전술적 포크는 포크한 애플리케이션마다 팀을 갈라야 하고
    작은 팀들 사이의 조율이 늘어난다**는 조직 조건이다 (4장, p.79,
    ADR).[^ford2021-hard-parts]

- **7장의 사가 둘이 앞 장들과 방향이 반대다.** 2장부터 6장까지의 장면이 전부 **쪼개는 쪽**으로
  움직였다면 7장의 둘은 **쪼개지 않기로 하는 결정**이고, 둘 다 합쳐진 서비스 하나에 이른다
  (7장, pp.211·215, ADR).[^ford2021-hard-parts] **이 대비는 이 KB가 세운 것이고 저자들이
  그렇게 적지는 않는다.** #hypothesis
  - **두 사가가 각각 다른 것을 보인다.** 앞은 **개발 팀 안의 의견 충돌**을 절충 분석으로
    바꾸는 장면이고 — 아키텍트가 마지막에 **이기고 지는 문제가 아니라 절충을 분석해 가장 알맞은
    해법에 이르는 문제**라고 형식을 교정한다 (7장, p.211, 사가) — 뒤는 **업무 쪽과 보안 쪽을
    한자리에 불러** 요구의 충돌을 해소하는 장면이다.
  - **뒤 사가가 남기는 교훈이 명시적으로 적힌다** — **보안이 아키텍처(기능을 별도 배포 단위로
    쪼개는 것)가 아니라 설계(특별한 암호화를 쓰는 맞춤 라이브러리)로 통제될 수 있다**는 것이고,
    제품 책임자가 **아키텍트가 회의를 통제하지 않고 대화를 촉진했다**는 점을 관찰한다 (7장,
    p.215, 사가).[^ford2021-hard-parts]
  - 열 요인과 두 ADR의 전문은 [서비스 세분도](service-granularity.md)에 있다.

- **8장의 사가 둘이 날짜를 장 안의 순서와 반대로 단다.** 앞에 놓인 §"Common Infrastructure
  Logic"이 **2월 10일 목요일**이고 뒤에 놓인 §"Shared Domain Functionality"가 **2월 8일
  화요일**이며, 장 여는 사가는 **2월 2일 수요일**이다 (8장, pp.219·239·244,
  사가).[^ford2021-hard-parts] **저자들이 그 역순을 설명하지 않는다.** 2장부터 7장까지의 사가는
  날짜가 앞으로만 갔다. #hypothesis
  - **요일과 날짜 자체는 어긋나지 않는다** — 2022년 2월 2일은 수요일, 8일은 화요일, 10일은
    목요일이다. **어긋난 것은 조판 순서뿐이다.**
- **8장의 두 사가가 증거의 종류를 하나 더 늘린다.** 3장은 업무 근거, 6장 전반은 로그와 지표,
  6장 후반은 업무 고통, 7장은 변경 주기와 처리량의 추정치였는데, **8장 둘째 사가는 저장소
  커밋 이력을 증거로 쓴다** — 아키텍트가 **그 공유 클래스 파일들이 역사적으로 얼마나 바뀌었는지
  보자**고 하고, 확인 결과 **생각보다 변경이 훨씬 적어** 판정이 뒤집힌다 (8장, p.247,
  사가).[^ford2021-hard-parts] **이 책의 사가 가운데 과거 실측을 증거로 쓰는 유일한
  자리다.** #hypothesis
  - **그 실측이 같은 장의 절충표 전제를 무너뜨린다** — 그 장이 공유 서비스의 첫째 이점으로
    `Good for high code volatility`를 드는데, 이 장면은 **변동성이 높다는 자기 보고가 실측으로
    기각되는** 대목이다. **저자들이 그 대응을 명시하지 않는다.** #hypothesis 3장 사가의 "자동화된
    단위 테스트가 있으니 괜찮다"가 30% 주석 처리 실측으로 뒤집히는 장면과 같은 모양이다.
- **8장 첫째 사가는 앞 장들과 다르게 조직 구조를 답으로 낸다** — 사이드카를 팀들이 함께 지는
  책임으로 둘지 물었을 때 **공유 인프라 팀(shared infrastructure team)을 만들었고 서비스 팀이
  그 팀의 고객으로 행동한다**는 답이 나온다 (8장, pp.240–241, 사가·ADR).[^ford2021-hard-parts]
  **이 사례에서 새 팀이 만들어지는 유일한 자리다.** #hypothesis
  - 그 두 장면의 전문과 ADR 둘은 [코드 재사용 패턴 넷](code-reuse-patterns.md)에 있다.

## 이어지는 페이지

- [서비스 세분도](service-granularity.md) — 7장이 이 사례에 대입하는 어휘
- [코드 재사용 패턴 넷](code-reuse-patterns.md) — 8장이 이 사례에 대입하는 어휘
- [아키텍처 퀀텀](architectural-quantum.md) — 2장이 이 사례에 대입하는 어휘
- [아키텍처 모듈성의 구동 요인](modularity-drivers.md) — 3장이 이 사례에 대입하는 어휘
- [데이터 분해의 구동 요인](data-decomposition-drivers.md) — 6장 전반이 이 사례에 대입하는 어휘
- [데이터베이스 종류 고르기](selecting-a-database-type.md) — 6장 후반이 이 사례에 대입하는 어휘
- [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md) — 이 사례의 테이블
  목록이 데이터 도메인으로 갈리는 자리
- [분해 접근 둘](decomposition-approaches.md) — 4장이 이 사례에 대입하는 어휘
- [컴포넌트 기반 분해 패턴 여섯](component-based-decomposition-patterns.md) — 5장이 이 사례에
  대입하는 어휘
- [도메인 서비스 만들기](create-domain-services.md) — 이 사례가 서비스 기반 아키텍처에 이르는
  마지막 장면
- [아키텍처 결정 기록](architecture-decision-records.md) — 이 책이 결정을 적는 형식
- [화물 운송 예제](cargo-shipping-example.md) — 같은 구실을 하는 다른 소스의 확장 예제
- [마켓노버스 사례 연구](marketnovus-case-study.md) — 지어낸 도메인이 아니라 실제 회사의 기록
- [데이터 분해가 부르는 관심사](data-decomposition-concerns.md) — 단일 스키마를 쪼갤 때 깨지는 것들
- [모놀리스 분해 패턴](monolith-decomposition-patterns.md) — 이미 서 있는 체계에서 출발한다는
  같은 조건
- [소프트웨어 아키텍처](../synthesis/software-architecture.md) — 이 축의 부모 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021 — 1장 "What Happens When There
    Are No 'Best Practices'?" §"Introducing the Sysops Squad Saga"(pp.15–21, 하위
    §"Nonticketing Workflow"(p.16) · §"Ticketing Workflow"(p.17) · §"A Bad Scenario"(pp.17–18) ·
    §"Sysops Squad Architectural Components"(pp.18–19) · §"Sysops Squad Data Model"(pp.19–21))와
    §"Architectural Decision Records"(p.5), 그리고 2장 "Discerning Coupling in Software
    Architecture"의 여는 장면(pp.25–26)과 §"Sysops Squad Saga: Understanding
    Quanta"(pp.42–44). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용 하나(사가의 사전 정의)는
    `pdftotext -layout` 추출로 문자 단위 대조했다. **표 1-1(컴포넌트 열여덟)과 표 1-2(테이블
    스물넷)는 `pdftoppm -r 160 -png`로 렌더해 눈으로 대조한 뒤 원문 열 머리글(Component ·
    Namespace · Responsibility · Table)과 셀 값을 영어 그대로 옮겼다** — 표 1-2는 인쇄판에서
    p.20과 p.21에 걸쳐 끊겨 있고 여기서는 한 표로 이었다. 네임스페이스는 원문이 고정폭으로
    조판한 것이라 인라인 코드로 옮겼다. **그림 1-3(컴포넌트 배치)과 그림 1-4(ER 모델)도 같은
    방식으로 렌더해 눈으로 읽었고**, 도판 자체는 재현하지 않고 본문이 적지 않는 배치(그림 1-3의
    사용자 인터페이스 위치, 그림 1-4의 음영 군집과 도판 안 설명)만 옮겼다. 그림 1-4의 결합
    선(테이블 사이 관계)은 옮기지 않았다 — 원문은 `archive/` 스냅샷이 보존한다. 위 사용자
    넷의 표와 데이터 모델 군집 표는 원문 표가 아니라 **본문 서술과 도판을 이 KB가 표로 모은
    것**이고 그 사실을 각 표 앞에 적었다. 등장인물 이름은 원문 표기를 음차했다. 이 구간에
    코드 목록은 없다.
    **3장 §"Sysops Squad Saga: Creating a Business Case"(pp.59–62, ADR 상자 pp.61–62 포함)과
    4장 §"Sysops Squad Saga: Choosing a Decomposition Approach"(pp.78–79, ADR 상자 p.79 포함)이
    적용 색인에 합류했다.** 두 사가에는 직인용을 두지 않았다 — 옮긴 것이 장면의 판정이고,
    두 장의 개념 전문은 [아키텍처 모듈성의 구동 요인](modularity-drivers.md)과
    [분해 접근 둘](decomposition-approaches.md)이 갖는다. 두 사가에 도판도 표도 코드 목록도
    없다.
    **5장의 사가 셋(§"Sysops Squad Saga: Sizing Components" pp.90–93 ·
    §"Sysops Squad Saga: Gathering Common Components" pp.97–101 ·
    §"Sysops Squad Saga: Flattening Components" pp.107–110)이 적용 색인에 합류했다.**
    세 사가에도 직인용을 두지 않았다 — 옮긴 것이 장면의 판정이고, 세 패턴의 개념 전문과 사가에
    딸린 표 여덟은 [컴포넌트를 식별하고 크기를 맞추기](identify-and-size-components.md) ·
    [공통 도메인 컴포넌트 모으기](gather-common-domain-components.md) ·
    [컴포넌트 평탄화](flatten-components.md)가 갖는다. 세 사가에 ADR 상자가 없다는 것은
    부록 B의 쪽 목록과 5장의 쪽 범위를 맞대어 확인했다.
    **5장 후반의 사가 셋(§"Sysops Squad Saga: Identifying Component Dependencies" pp.118–120 ·
    §"Sysops Squad Saga: Creating Component Domains" pp.123–126 ·
    §"Sysops Squad Saga: Creating Domain Services" pp.129–130)도 적용 색인에 합류했다** —
    이로써 5장의 사가 여섯이 전부 들어왔다. 이 셋에도 직인용을 두지 않았고, 세 패턴의 개념
    전문과 사가에 딸린 표 넷과 도판 셋은
    [컴포넌트 의존 판정](determine-component-dependencies.md) ·
    [컴포넌트 도메인 만들기](create-component-domains.md) ·
    [도메인 서비스 만들기](create-domain-services.md)가 갖는다.
    **6장 전반의 사가 하나(§"Sysops Squad Saga: Justifying Database Decomposition" pp.150–151)와
    여는 사가(pp.131–132)가 적용 색인에 합류했다.** 둘에도 직인용을 두지 않았다 — 옮긴 것이
    장면의 판정이고, 여덟 구동 요인과 다섯 단계의 전문과 표 여섯은
    [데이터 분해의 구동 요인](data-decomposition-drivers.md)과
    [모놀리식 데이터를 쪼개는 다섯 단계](decomposing-monolithic-data.md)가 갖는다. 표 6-5가
    위 §"데이터 모델"의 테이블 목록을 데이터 도메인 여섯에 배정하는데, **그 표는 이 페이지에
    다시 옮기지 않고 절차 페이지가 갖는다.** 두 사가에 도판도 코드 목록도 없고, 6장 전반에
    ADR 상자가 없다는 것은 부록 B의 쪽 목록(p.79 다음이 p.184)과 6장 전반의 쪽 범위를 맞대어
    확인했다.
    **6장 후반의 사가 하나(§"Sysops Squad Saga: Polyglot Databases" pp.179–184, ADR 상자
    p.184 포함)도 적용 색인에 합류했다** — 이로써 6장의 사가 셋이 전부 들어왔다. 이 사가에도
    직인용을 두지 않았다. ADR 전문과 데이터베이스 여덟 갈래의 별점표는
    [데이터베이스 종류 고르기](selecting-a-database-type.md)와
    [아키텍처 결정 기록](architecture-decision-records.md)이 갖는다. 사가에 딸린 도판
    넷(그림 6-34~6-37)은 재현하지 않았고, JSON 목록 둘(예제 6-3·6-4)도 옮기지 않았다 —
    그 두 조판이 말하는 절충은 절충 표로 보존되고 그 표는 개념 페이지가 갖는다.
    **7장의 사가 둘(§"Sysops Squad Saga: Ticket Assignment Granularity" pp.209–212, ADR 상자
    pp.211–212 포함 · §"Sysops Squad Saga: Customer Registration Granularity" pp.212–216,
    ADR 상자 pp.215–216 포함)도 적용 색인에 합류했다.** 둘에도 직인용을 두지 않았다 — 옮긴
    것이 장면의 판정이고, 세분도 요인 열과 두 ADR의 전문은
    [서비스 세분도](service-granularity.md)가 갖는다. 사가에 딸린 도판 둘(그림 7-18 티켓 배정의
    선택지 · 7-19 고객 등록의 선택지 셋)은 재현하지 않고 본문이 그 도판에 대해 적는 것만 옮겼고,
    두 사가에 코드 목록은 없다. 두 사가의 결론이 앞 장들과 반대 방향이라는 대비는 **이 KB가
    세운 것**이다.
    **8장의 사가 둘(§"Sysops Squad Saga: Common Infrastructure Logic" pp.239–241, ADR 상자
    p.241 포함 · §"Sysops Squad Saga: Shared Domain Functionality" pp.244–247, ADR 상자
    p.247 포함)과 장 여는 사가(pp.219–220)도 적용 색인에 합류했다.** 셋 다 직인용을 두지
    않았다 — 옮긴 것이 장면의 판정이고, 네 재사용 패턴과 원문 절충표 넷과 두 ADR의 전문은
    [코드 재사용 패턴 넷](code-reuse-patterns.md)이 갖는다. 사가에 딸린 도판 둘(그림 8-18 공유
    데이터 서비스 선택지 · 8-19 공유 라이브러리 선택지)은 재현하지 않고 본문이 그 도판에 대해
    적는 것만 옮겼고, 두 사가에 코드 목록은 없다. **날짜가 장 안의 순서와 반대라는 관찰과 증거의
    종류가 늘었다는 관찰과 새 팀이 만들어지는 유일한 자리라는 관찰은 이 KB가 세운 것이고
    저자들이 그것들을 적지 않는다.**

---
type: synthesis
title: 메시징 패턴
description: 비동기 메시징으로 애플리케이션을 통합할 때 쓰는 이름 층의 진입점 — 통합 스타일 넷 중 메시징을 고르는 판단, 결합을 가정의 수로 재는 자, 채널·메시지·파이프와 필터·라우터·변환기·엔드포인트 여섯 뿌리 패턴이 각각 어느 장으로 자라는가의 지도, 뿌리마다 붙는 패턴 묶음(채널 설계·메시지 구성·라우팅·변환), 카탈로그를 닫는 두 장(실제 시스템에 패턴을 댄 사례와 패턴이 표준으로 굳을 때의 전망), 그리고 이 KB의 스트리밍·데이터 엔지니어링 서술이 이미 빌려 쓰고 있던 이름들의 원천 대조 — 원전 각주가 합류한 페이지와 어휘만 이웃한 페이지를 갈라서, 그리고 도메인 주도 설계 쪽이 같은 사태에 붙인 이름 넷(아웃박스·사가·프로세스 매니저·모델 번역)과 그 사가를 통신·일관성·조율 세 축의 여덟 칸으로 다시 펴는 넷째 소스, 그리고 같은 기반을 마이크로서비스 통합의 데이터 층으로 다시 세우는 다섯째 소스의 여섯 페이지
generated: { by: "claude-opus-5", at: "2026-09-15T10:00:00Z" }
---

# 메시징 패턴

- [이름이 좁은 이유](#이름이-좁은-이유) — 무엇이 이 카탈로그에 들어오고 무엇이 안 들어오는가
- [먼저 읽는 순서](#먼저-읽는-순서) — 스타일 선택 → 결합의 자 → 뿌리 어휘
- [뿌리에서 자란 장들](#뿌리에서-자란-장들) — 뿌리마다 붙는 패턴 묶음
- [뿌리를 갖지 않는 두 장 — 사례와 맺음](#뿌리를-갖지-않는-두-장--사례와-맺음) — 카탈로그를 닫는 쪽
- [여섯 뿌리와 그 가지](#여섯-뿌리와-그-가지) — 뿌리마다 장이 하나씩 붙는 골격
- [원전 층이 합류한 기존 페이지](#원전-층이-합류한-기존-페이지) — 이 소스의 각주가 붙은 자리 전부
- [도메인 모델 쪽에서 같은 문제에 붙은 이름들](#도메인-모델-쪽에서-같은-문제에-붙은-이름들) — 다른 소스가 같은 사태에 다른 이름을 붙인 자리
- [각주 없이 이웃한 페이지](#각주-없이-이웃한-페이지) — 어휘만 겹치는 자리들
- [이벤트 기반 마이크로서비스 쪽에서 본 같은 기반](#이벤트-기반-마이크로서비스-쪽에서-본-같은-기반) — 통합의 기반을 이벤트 스트림 하나로 두는 쪽
- [이웃 허브](#이웃-허브) — 이 이름 층이 얹히는 원리 쪽 허브들

## 이름이 좁은 이유

여기 모인 것은 Gregor Hohpe & Bobby Woolf, *Enterprise Integration Patterns*(Addison-Wesley,
2004)가 이름을 붙여 카탈로그로 정리한 층이다. 이 KB에는 이미 브로커·큐·토픽·스트림 처리의
**작동 서술**이 다른 소스들(Shapira·Kleppmann·Reis & Housley·Konieczny)로 쌓여 있고, 이 허브가
더하는 것은 그 위의 **이름 층**이다 — "처리 못 한 메시지를 다른 곳에 모은다"라는 실무에
`Dead Letter Channel`이라는 이름과 결과 목록이 붙는 식이다.

**메시징 패턴**이라는 이름을 골랐지 "기업 통합"으로 넓히지 않은 이유: 이 카탈로그가 다루는 범위가
저자들 스스로 좁혀 놓은 것이기 때문이다. 네 통합 스타일 중 메시징 하나를 고른 뒤 나머지 책 전부를
거기 썼다.

## 먼저 읽는 순서

- [애플리케이션 통합의 네 가지 스타일](../concepts/application-integration-styles.md) — 카탈로그
  앞에 놓인 선택. 통합 여부부터 묻는 첫 판단, 여덟 기준, 파일 전송·공유 데이터베이스·원격 프로시저
  호출·메시징이 앞의 것의 결핍을 하나씩 메우며 정교해지는 계승 관계, 그리고 메시징을 고른 근거
- [통합의 도전과 느슨한 결합](../concepts/integration-challenges-and-loose-coupling.md) —
  카탈로그의 잣대. 결합을 "두 당사자가 서로에 대해 세우는 가정의 수"로 정의하고, 열 줄짜리 TCP/IP
  통합이 드러내는 네 가정(플랫폼·위치·시간·데이터 형식)을 채널·큐잉·메시지·변환기가 하나씩 떼는
  경로. 이후 모든 패턴이 이 경로 위의 장치다
- [메시징의 여섯 뿌리 패턴](../concepts/messaging-root-patterns.md) — 카탈로그의 어휘. 나머지
  패턴은 전부 이 여섯 중 하나에서 자란다

## 뿌리에서 자란 장들

- [메시징 채널 패턴](../concepts/messaging-channel-patterns.md) — *Message Channel*의 장. 채널
  집합이 배포 시점에 고정되는 성질과 여섯 설계 결정, Datatype Channel·Guaranteed Delivery·
  Channel Adapter·Messaging Bridge·Message Bus
- [메시지 구성 패턴](../concepts/message-construction-patterns.md) — *Message*의 장. 발신자의
  의도로 갈리는 세 메시지, Request-Reply와 그 짝(Return Address·Correlation Identifier),
  Message Sequence·Message Expiration·Format Indicator
- [메시지 라우팅 패턴](../concepts/message-routing-patterns.md) — *Message Router*의 장, 앞쪽.
  열두 패턴의 분류와 개수를 바꾸지 않는 라우터 넷 — Content-Based Router·Message Filter·
  Dynamic Router·Recipient List
- [분할·집계·재정렬 패턴](../concepts/splitter-aggregator-resequencer-patterns.md) — 같은 장,
  개수와 순서를 바꾸는 셋. Splitter·Aggregator·Resequencer. 이 KB가 어휘를 가장 많이 빌려 쓴 자리
- [복합 라우팅 패턴](../concepts/composed-routing-patterns.md) — 같은 장, 뒤쪽. 단순 라우터를 조합한
  넷(Composed Message Processor·Scatter-Gather·Routing Slip·Process Manager)과 그 위의 아키텍처
  패턴 Message Broker
- [메시지 변환 패턴](../concepts/message-transformation-patterns.md) — *Message Translator*의 장.
  Envelope Wrapper·Content Enricher·Content Filter·Claim Check·Normalizer·Canonical Data Model
- [메시징 엔드포인트 패턴](../concepts/messaging-endpoint-patterns.md) — *Message Endpoint*의 장,
  앞쪽. 소비자 패턴을 양자택일의 짝으로 세운 서두와 송수신 양쪽에 걸리는 셋 — Messaging Gateway·
  Messaging Mapper·Transactional Client
- [메시지 소비자 패턴](../concepts/message-consumer-patterns.md) — 같은 장, 받는 쪽. Polling
  Consumer·Event-Driven Consumer·Competing Consumers·Message Dispatcher·Selective Consumer·
  Durable Subscriber·Service Activator
- [시스템 관리 패턴](../concepts/system-management-patterns.md) — 뿌리를 갖지 않는 장. 흐름을 만드는
  대신 들여다보는 여덟 — Control Bus·Detour·Wire Tap·Message History·Message Store·Smart Proxy·
  Test Message·Channel Purger

## 뿌리를 갖지 않는 두 장 — 사례와 맺음

카탈로그를 닫는 두 장은 패턴을 정의하지 않는다. 하나는 패턴을 **쓰는** 이야기이고 다른 하나는
패턴이라는 형식이 **어디로 가는가**의 이야기다. 둘 다 저자들이 아니라 초청 저자가 썼다.

- [패턴을 실제로 적용할 때](../concepts/pattern-application-in-practice.md) — 13장(Jonathan Simon).
  실제 채권 가격 산정 시스템에 카탈로그를 대면서 내려진 판단들 — 통합 스타일을 요구사항으로 하나씩
  기각하는 절차, 기술이 아닌 힘이 패턴을 기각하는 자리, 패턴으로 패턴을 구현하고 패턴의 맥락을
  바꿔 쓰는 조합, 채널 세밀도와 로직의 위치, 방향마다 채널 종류를 따로 고르는 설계, 데드레터 큐가
  서버를 무너뜨린 사고, 그리고 천 개의 패턴으로도 못 고치는 것. **도메인 서사는 걸렀다**
- [패턴과 표준](../concepts/patterns-and-standards.md) — 14장(Sean Neville). 패턴의 구현 전략이
  표준으로 굳을 때 패턴에 무슨 일이 일어나는가 — 나이테 논증, 같은 패턴이 여러 층에 재귀적으로
  있다는 관찰, 표준을 패턴의 목록으로 읽는 독법, 네 가지 전달 보장, 롤백이 아니라 보상으로 푸는
  오래 사는 프로세스. **2003년 시점의 전망이라는 장르를 명시했고 규격의 흥망은 채점하지 않는다**

## 여섯 뿌리와 그 가지

저자들이 **뿌리 패턴(root patterns)** 이라 부르는 여섯이 있고, 각 뿌리마다 장이 하나씩 붙는다.
정의는 [메시징의 여섯 뿌리 패턴](../concepts/messaging-root-patterns.md)에 있고, 여기서는 무엇이
어디로 자라는지의 골격만 둔다.

| 뿌리 | 무엇을 정하는가 | 자라는 장 |
|---|---|---|
| *Message Channel* | 어디로 보내는가 — 논리 주소 | 4장 Messaging Channels |
| *Message* | 무엇을 보내는가 — 헤더와 바디 | 5장 Message Construction |
| *Pipes and Filters* | 어떻게 잇는가 — 단계와 채널의 교대 | (다른 다섯 전부의 기반 아키텍처) |
| *Message Router* | 목적지를 누가 정하는가 — 내용은 불변 | 7장 Message Routing |
| *Message Translator* | 형식 차이를 어디서 흡수하는가 — 네 계층 | 8장 Message Transformation |
| *Message Endpoint* | 애플리케이션이 어떻게 붙는가 — 메시징 시스템의 클라이언트 | 10장 Messaging Endpoints |

여기에 뿌리를 갖지 않는 한 장이 더 있다 — 11장 System Management. 흐름을 만드는 패턴이 아니라
흐름을 들여다보는 패턴들(*Control Bus*·*Detour*·*Wire Tap*·*Message History*·*Message Store*·
*Smart Proxy*·*Test Message*·*Channel Purger*)이 거기 모인다.

## 원전 층이 합류한 기존 페이지

이 소스의 정체는 **기존 서술의 이름 원천**이다. 아래는 이 카탈로그의 원전 층이 실제로 기존 페이지
안으로 들어간 자리 전부이고, 판정 기준은 그 페이지에 `[^hohpe2004]` 각주가 있는가다. 각 페이지가
무엇을 다루는지는 그 페이지가 말한다.

| 페이지 | 무엇이 합류했는가 | 원전의 자리 |
|---|---|---|
| [데이터베이스를 거치는 데이터플로](../concepts/dataflow-through-databases.md) | *Shared Database* 통합 스타일의 정의와 그 대가 | 2장 |
| [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md) | *Remote Procedure Invocation*의 원전 서술과 20년 뒤의 채점 | 2장 |
| [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) | 채널 어휘의 원전 — 점대점과 발행-구독이 갈리는 자리 | 3·4장 |
| [데드레터와 빠져나가는 레코드](../concepts/dead-letter-and-dropped-records.md) | *Invalid Message Channel*·*Dead Letter Channel*의 원전 정의와 현대 용법의 경계 이동, 그리고 데드레터 큐가 서버를 무너뜨린 사고 | 4·13장 |
| [순서 있는 전달 패턴](../concepts/ordered-delivery-patterns.md) | *Resequencer* — 예방이냐 교정이냐의 판정 | 7장 |
| [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) | *Routing Slip*·*Process Manager*가 오케스트레이션의 선조인 자리 | 7장 |
| [데이터 강화와 장식 패턴](../concepts/data-enrichment-and-decoration-patterns.md) | *Content Enricher*·*Envelope Wrapper*의 이름 계보 | 8장 |
| [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) | *Idempotent Receiver*가 멱등성 4층 대조표에 들어간 자리 | 10장 |
| [데이터 계보 추적 패턴](../concepts/data-lineage-tracking-patterns.md) | *Message History* — 레코드가 자기 경로를 들고 다니는 배치 | 11장 |
| [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md) | 패턴이라는 형식 자체에 대한 세 판정 — 일반적이라서 붙잡기 어렵다·표준화되어도 나이테처럼 자란다·부실한 사전 설계는 보완하지 못한다 | 13·14장 |

## 도메인 모델 쪽에서 같은 문제에 붙은 이름들

이 카탈로그의 패턴과 **같은 사태를 도메인 주도 설계 쪽 어휘로 다루는 자리**가 2021년 실무서에서
들어왔다. 위 [원전 층이 합류한 기존 페이지](#원전-층이-합류한-기존-페이지)와 갈라 두는 이유:
이쪽은 이 소스의 각주가 붙은 자리가 아니라 **다른 소스가 같은 문제에 다른 이름을 붙인** 자리다.

- [아웃박스 패턴](../concepts/outbox-pattern.md) — 데이터베이스 갱신과 메시지 발행을 어긋나지
  않게 하는 기제. 2004년의 답인 *Transactional Client*와 XA가
  [메시징 엔드포인트 패턴](../concepts/messaging-endpoint-patterns.md)에 있고, 이쪽이 그것을
  피하는 현재형 답이다. 보장은 최소 한 번이라 *Idempotent Receiver*를 조건으로 넘긴다
- [사가 패턴](../concepts/saga-pattern.md) — 여러 구성 요소에 걸치는 업무 프로세스를 롤백이
  아니라 보상으로 푸는 쪽. [패턴과 표준](../concepts/patterns-and-standards.md)이 2003년 시점의
  전망으로 적은 "오래 사는 프로세스"가 이쪽에서 이름과 정의를 얻는다. **소스가 둘이고 둘이 이
  낱말을 다른 대상에 쓴다** — 한쪽은 이벤트와 명령을 짝짓는 구성 요소로, 다른 쪽은 프로세스
  전체로 쓰며, 그 대조표가 그 페이지 안에 있다. 이벤트로 흩어 조율하는 구현(코레오그래피)이
  이 카탈로그의 채널·토픽·상관 식별자 위에 그대로 선다
- [트랜잭셔널 사가 패턴](../concepts/transactional-saga-patterns.md) — 같은 낱말을 **여덟 칸의
  상위어**로 다시 규정하는 넷째 소스. 통신(동기·비동기)과 일관성(원자·최종)과 조율
  (오케스트레이션·코레오그래피)을 곱한 여덟에 이름과 세 글자 코드를 붙이고 칸마다 채점하며,
  이 카탈로그의 채널과 상관 식별자 위에 서는 것은 그 여덟 중 코레오그래피 쪽 넷이다
- [프로세스 매니저](../concepts/process-manager.md) — **이 카탈로그의 *Process Manager*와 같은
  이름이고, 그쪽 저자가 이 책을 출처로 댄다.** 다만 구현이 통합 미들웨어의 프로세스 엔진이
  아니라 도메인 모델 안의 애그리게이트다. 원전 쪽 서술은
  [복합 라우팅 패턴](../concepts/composed-routing-patterns.md)에 있다
- [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) — 같은
  조율 선택을 마이크로서비스 쪽에서 축 하나로 세운 자리. 중앙 조율자를 쓰는 쪽이 이 카탈로그의
  *Process Manager*와 같은 자리이고, 쓰지 않는 쪽은 채널과 방송 메시지 위에 그대로 선다.
  코레오그래피에서 워크플로 상태를 메시지에 실어 나르는 선택지(스탬프 결합)도 그 페이지에 있다
- [모델 번역](../concepts/model-translation.md) — *Message Translator*가 데이터 형식의 차이를
  흡수한다면 이쪽은 **경계 컨텍스트의 모델**을 번역한다. 형식이 같아도 남는 층이고, 여러
  메시지를 합치는 대목에서 *Aggregator*와 *Content Enricher*를 가리킨다
- [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) — 서비스를 가로지르는
  업무 요청이 남긴 데이터 어긋남을 되맞추는 세 가지를 아키텍처 쪽에서 세운 자리. 셋 가운데
  이벤트 기반 패턴이 이 카탈로그의 *Publish-Subscribe Channel* 위에 그대로 서고, 전달 보증을
  *Durable Subscriber*로, 반복 실패를 *Dead Letter Channel*로 받는다. 원전 쪽 서술은
  [메시징 채널 패턴](../concepts/messaging-channel-patterns.md)과
  [메시지 구성 패턴](../concepts/message-construction-patterns.md)에 있다

## 각주 없이 이웃한 페이지

아래는 어휘가 겹치거나 같은 사태를 다른 층에서 다루지만 **원전 층이 합류하지는 않은** 자리다.
위 표와 갈라 두는 이유: 이 소스를 인용하려면 위쪽으로 가야 한다.

- [로그 기반 메시지 브로커](../concepts/log-based-message-brokers.md) — 채널을 지워지는 큐가
  아니라 남는 로그로 구현했을 때 달라지는 것
- [배치 조인과 그룹핑](../concepts/batch-joins-and-grouping.md) — *Aggregator*의 배치 판
- [카프카 단일 메시지 변환](../concepts/kafka-single-message-transformations.md) — 변환을
  파이프라인 안에 두는 실물
- [카프카 커넥트와 파이프라인](kafka-connect-and-pipelines.md) — 애플리케이션을
  스트리밍 시스템에 붙이는 어댑터 층. *Channel Adapter*의 현재형
- [링크 추상과 메시지 전달 보장](../concepts/link-abstractions-and-message-delivery.md) —
  "성공할 때까지 전달을 다시 시도한다"가 서 있는 보장의 사다리
- [토픽과 파티션](../concepts/topics-and-partitions.md) — 채널 세밀도의 현재형 한계
- [느슨하게 해석되는 제약](../concepts/loosely-interpreted-constraints.md) — 롤백 대신 보상으로
  푸는 축
- [기술 선택의 기준](../concepts/technology-selection-criteria.md) — 회사 표준·조직 결정이 기술
  선택에 들어오는 축
- [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md) — 같은 메시지 어휘를
  경계 컨텍스트 사이 통합의 문제로 세우고 이벤트를 세 종류로 가르는 쪽
- [마이크로서비스 인터페이스 기술의 다섯 조건](../concepts/microservice-interface-criteria.md)
  — 메시지 브로커를 포함한 통신 기술 넷을 고르기 전에 그 기술에 요구할 것을 적어 두는
  체크리스트
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 같은 선택을
  마이크로서비스 사이 통신의 문제로 세우고 다섯 스타일로 가르는 쪽. 이 카탈로그의 네 통합
  스타일이 그 다섯으로 어떻게 대응하는지는
  [애플리케이션 통합의 네 가지 스타일](../concepts/application-integration-styles.md)에 있다
- [API 게이트웨이와 서비스 메시](../concepts/api-gateway-and-service-mesh.md) — 서비스 사이
  호출을 중개하는 프록시 층. **브로커를 쓰는 통신은 그 중개를 우회한다**는 한계가 그 페이지에
  있다 — 통신이 브로커와 직접 이뤄지므로 메시가 모든 호출의 중개자라고 가정할 수 없다

## 이벤트 기반 마이크로서비스 쪽에서 본 같은 기반

2025년 실무서 하나가 같은 메시징 기반을 **마이크로서비스 통합의 기반**으로 놓고 다시 적는다.
위 [원전 층이 합류한 기존 페이지](#원전-층이-합류한-기존-페이지)와 갈라 두는 이유: 이쪽은 이
카탈로그의 이름이 붙는 자리가 아니라 **같은 기반을 다른 물음으로 세운** 자리다. 그쪽의 물음은
"메시지를 어떻게 주고받는가"가 아니라 **"조직 전역의 데이터를 어느 층으로 흐르게 하는가"** 다.

- [소통 구조 셋](../concepts/communication-structures.md) — 조직의 소통을 업무·구현·데이터 셋으로
  가르고 셋째가 대개 방치되어 둘째에 얹혀 있다고 진단하는 틀. 콘웨이의 법칙을 그 셋으로 다시 읽는
  독법, 데이터를 얻으려는 기존 완화책 셋(공유 데이터베이스·읽기 복제본·배치 덤프)과 각각의 대가,
  그리고 이벤트 스트림을 일급 데이터 소통 구조로 세웠을 때 생산자와 소비자의 책임이 갈리는 자리
- [이벤트 스트림과 이벤트 브로커](../concepts/event-streams-and-brokers.md) — 그 기반에 요구할
  것들. 이벤트와 이벤트 스트림의 규정, 스트림이 갖춰야 할 성질 여섯, 같은 브로커 위에서 갈리는
  세 양식(휘발성 메시징·큐·이벤트 스트림)과 각각의 전달 보증, 익스체인지 팬아웃과 카프카에 큐가
  들어온 변화, 브로커에 요구되는 기능 넷과 고를 때 따질 축 다섯
- [이벤트의 구조와 세 종류](../concepts/event-record-structure-and-types.md) — 그 기반 위를 흐르는
  것의 해부. 헤더와 키와 값, 키로 가르는 세 종류(키 없는·키 있는·엔티티 이벤트), 키가 만드는
  데이터 지역성, 그리고 재파티셔닝과 공동 파티셔닝
- [이벤트 기반 마이크로서비스의 네 모양](../concepts/event-driven-microservice-shapes.md) — 그
  기반 위에 올라앉는 서비스의 모양들. 기본 프로듀서와 컨슈머, 스트림 처리 프레임워크, 스트리밍
  SQL 질의, 커넥터로 붙인 레거시 애플리케이션 넷과 그 넷을 가르는 축, 마이크로서비스 토폴로지와
  업무 토폴로지, 책임 여덟과 스트림당 단일 기록자 원칙, 그리고 플랫폼 비용을 하나로 묶는
  마이크로서비스 세금
- [이벤트 스키마와 데이터 계약](../concepts/event-schemas-and-data-contracts.md) — 그 기반 위를
  흐르는 것에 거는 계약. 스키마를 전제로 세우는 처방, 기술 셋을 선택 기준으로 견주는 비교,
  네 호환 모드와 전이 완전 호환을 기본값으로 삼으라는 처방, 데이터 계약의 규정과 구성 요소 여섯,
  깨는 변경을 협상하는 네 단계, 그리고 스키마 레지스트리와 필드 수준 암호화와 데이터 카탈로그
- [이벤트 설계 - 상태와 델타](../concepts/event-design-state-versus-delta.md) — 그 기반 위를
  흐르는 것의 값 칸을 무엇으로 채울 것인가. 상태 이벤트와 이벤트가 실어 나르는 상태 전이,
  현재 상태만 담는 설계와 전후 상태를 담는 설계가 압착과 저장과 누출에서 갈리는 자리, 델타
  이벤트와 그것으로 하는 이벤트 소싱, 델타를 도메인 밖으로 냈을 때 터지는 문제 다섯과 델타를
  사적 도메인 안에 두라는 경계 규칙, 혼합 이벤트의 위험, 측정 이벤트와 알림 이벤트, 그리고
  이벤트 스트림의 불변성과 잊힐 권리를 화해시키는 크립토 슈레딩

- [데이터 해방](../concepts/data-liberation.md) — 레거시 저장소 안에 갇힌 데이터를 그 기반으로
  꺼내는 이행 전략. 이중 쓰기 안티패턴이라는 출발점, 해방 패턴 셋(질의 기반·로그 기반·아웃박스
  테이블 기반)과 트리거, 초기 스냅샷이 테이블을 잠그는 문제와 무락 증분 스냅샷, 아웃박스에서
  내부 모델을 격리하고 스키마를 강제하는 두 자리, 포착 중인 데이터셋의 정의 변경, 스트림을
  저장소로 되돌리는 싱킹, 그리고 중앙 포착 프레임워크가 조직에 놓는 함정 둘
- [비정규화와 이벤트화](../concepts/denormalization-and-eventification.md) — 그렇게 꺼낸 관계형
  스트림을 소비자가 조인 없이 쓸 수 있는 이벤트로 바꾸는 물음. 아웃박스 안에서 조인하는 길과
  전용 서비스로 밖에서 조인하는 길, 비정규화하면 어느 필드가 바뀌든 이벤트를 갱신해야 한다는
  조항, 무엇을 넣고 뺄지를 가르는 빈도와 크기와 그 곱, 그리고 완만하게 변하는 차원이 운영계
  스트림으로 건너왔을 때의 타입 1과 타입 2

**자식 허브 제안 — 네 런째 올리며, 이제 기한이 지났습니다.** 이 절에 실린 페이지가 **이번 런으로
여덟**이 되었습니다. 런 01에서 셋을 올리며 "4장에서 10장을 반입한 뒤 자식 허브를 세우자"고
적었는데, 이번 런이 7장까지 반입했으므로 **그 시점에 들어섰습니다.** 여덟은 이렇습니다 —
소통 구조 셋 · 이벤트 스트림과 이벤트 브로커 · 이벤트의 구조와 세 종류 · 이벤트 기반
마이크로서비스의 네 모양 · 이벤트 스키마와 데이터 계약 · 이벤트 설계(상태와 델타) · 데이터 해방 ·
비정규화와 이벤트화. 남은 장이 8장부터 22장까지 열다섯이므로 **이 목록은 계속 자랍니다.**
**판단은 사람 몫이고, 지금까지 세우지 않은 이유는 이름 범위를 내용 범위보다 넓게 잡지 말라는
규약이었습니다.** 이제 내용 범위가 이름을 지탱할 만큼 찼는지가 물음입니다.

## 이웃 허브

- [스트림 처리](stream-processing.md) — 이 이름 층이 얹히는 현재형 기반. 브로커·시간·상태·이중성
- [카프카](kafka-basics.md) — 여섯 뿌리가 하나의 제품에서 어떻게 구현됐는가
- [데이터 엔지니어링 디자인 패턴](data-engineering-design-patterns.md) — 같은 방식으로 원리 위에
  얹힌 다른 이름 층. 데드레터·멱등성처럼 겹치는 이름이 있고, 거기서는 데이터 파이프라인 쪽 결과가
  달린다
- [데이터플로 아키텍처](dataflow-architecture.md) — 통합을 메시징이 아니라 데이터 통합의 문제로
  세우는 쪽
- [인코딩과 진화](encoding-and-evolution.md) — *Message Translator*가 흡수하는 형식 차이를 바이트
  수준에서 다루는 쪽
- [도메인 주도 설계](domain-driven-design.md) — 위 "도메인 모델 쪽에서 같은 문제에 붙은
  이름들"이 사는 축. 통합을 모델의 경계 문제로 세우는 쪽

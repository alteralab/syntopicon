---
type: synthesis
title: 메시징 패턴
description: 비동기 메시징으로 애플리케이션을 통합할 때 쓰는 이름 층의 진입점 — 통합 스타일 넷 중 메시징을 고르는 판단, 결합을 가정의 수로 재는 자, 채널·메시지·파이프와 필터·라우터·변환기·엔드포인트 여섯 뿌리 패턴이 각각 어느 장으로 자라는가의 지도, 뿌리마다 붙는 패턴 묶음(채널 설계와 메시지 구성), 그리고 이 KB의 스트리밍·데이터 엔지니어링 서술이 이미 빌려 쓰고 있던 이름들의 원천 대조
generated: { by: "claude-opus-5", at: "2026-08-16T12:00:00Z" }
---

# 메시징 패턴

- [이름이 좁은 이유](#이름이-좁은-이유) — 무엇이 이 카탈로그에 들어오고 무엇이 안 들어오는가
- [먼저 읽는 순서](#먼저-읽는-순서) — 스타일 선택 → 결합의 자 → 뿌리 어휘
- [뿌리에서 자란 장들](#뿌리에서-자란-장들) — 뿌리마다 붙는 패턴 묶음
- [여섯 뿌리와 그 가지](#여섯-뿌리와-그-가지) — 뿌리마다 장이 하나씩 붙는 골격
- [이 KB가 이미 쓰고 있던 이름들](#이-kb가-이미-쓰고-있던-이름들) — 어휘를 빌려 쓰던 자리들
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

- [애플리케이션 통합의 네 가지 스타일](../inbox/application-integration-styles.md) — 카탈로그
  앞에 놓인 선택. 통합 여부부터 묻는 첫 판단, 여덟 기준, 파일 전송·공유 데이터베이스·원격 프로시저
  호출·메시징이 앞의 것의 결핍을 하나씩 메우며 정교해지는 계승 관계, 그리고 메시징을 고른 근거
- [통합의 도전과 느슨한 결합](../inbox/integration-challenges-and-loose-coupling.md) —
  카탈로그의 잣대. 결합을 "두 당사자가 서로에 대해 세우는 가정의 수"로 정의하고, 열 줄짜리 TCP/IP
  통합이 드러내는 네 가정(플랫폼·위치·시간·데이터 형식)을 채널·큐잉·메시지·변환기가 하나씩 떼는
  경로. 이후 모든 패턴이 이 경로 위의 장치다
- [메시징의 여섯 뿌리 패턴](../inbox/messaging-root-patterns.md) — 카탈로그의 어휘. 나머지
  패턴은 전부 이 여섯 중 하나에서 자란다

## 뿌리에서 자란 장들

- [메시징 채널 패턴](../inbox/messaging-channel-patterns.md) — *Message Channel*의 장. 채널
  집합이 배포 시점에 고정되는 성질과 여섯 설계 결정, Datatype Channel·Guaranteed Delivery·
  Channel Adapter·Messaging Bridge·Message Bus
- [메시지 구성 패턴](../inbox/message-construction-patterns.md) — *Message*의 장. 발신자의
  의도로 갈리는 세 메시지, Request-Reply와 그 짝(Return Address·Correlation Identifier),
  Message Sequence·Message Expiration·Format Indicator

## 여섯 뿌리와 그 가지

저자들이 **뿌리 패턴(root patterns)** 이라 부르는 여섯이 있고, 각 뿌리마다 장이 하나씩 붙는다.
정의는 [메시징의 여섯 뿌리 패턴](../inbox/messaging-root-patterns.md)에 있고, 여기서는 무엇이
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
흐름을 들여다보는 패턴들(*Control Bus*·*Wire Tap*·*Message History*·*Message Store*·
*Smart Proxy*·*Test Message*)이 거기 모인다.

## 이 KB가 이미 쓰고 있던 이름들

이 소스의 정체는 **기존 서술의 이름 원천**이다. 아래는 그 어휘가 이미 쓰이고 있던 자리다 —
각 페이지가 무엇을 다루는지는 그 페이지가 말한다.

- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 큐와 토픽이라는 두 분배 패턴,
  브로커와 데이터베이스의 차이, 확인 응답과 재전달
- [데드레터와 빠져나가는 레코드](../concepts/dead-letter-and-dropped-records.md) — 처리 못 한
  레코드를 어디에 두는가와 그 대가
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — 중복을 수신 쪽에서
  흡수하는 쪽
- [로그 기반 메시지 브로커](../concepts/log-based-message-brokers.md) — 채널을 지워지는 큐가
  아니라 남는 로그로 구현했을 때 달라지는 것
- [순서 있는 전달 패턴](../concepts/ordered-delivery-patterns.md) — 병렬 처리가 순서를 깨뜨린
  뒤의 복구
- [카프카 단일 메시지 변환](../concepts/kafka-single-message-transformations.md) — 변환을
  파이프라인 안에 두는 실물
- [카프카 커넥트와 파이프라인](kafka-connect-and-pipelines.md) — 애플리케이션을
  스트리밍 시스템에 붙이는 어댑터 층
- [링크 추상과 메시지 전달 보장](../concepts/link-abstractions-and-message-delivery.md) —
  "성공할 때까지 전달을 다시 시도한다"가 서 있는 보장의 사다리

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

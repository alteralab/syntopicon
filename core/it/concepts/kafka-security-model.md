---
type: concept
title: 카프카 보안 모델
description: 카프카 보안을 컴포넌트가 아니라 시스템 전체의 문제로 놓는 틀 — 기밀성·무결성·가용성을 세우는 보안 절차 다섯, 앨리스가 쓰고 밥이 읽는 예시 데이터 흐름의 여섯 단계, 그리고 안전한 배포가 보장해야 하는 일곱 가지와 각 보장이 어느 기능으로 내려가는지
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 보안 모델

- [보안은 컴포넌트가 아니라 시스템의 속성이다](#보안은-컴포넌트가-아니라-시스템의-속성이다)
- [보안 절차 다섯](#보안-절차-다섯)
- [예시 데이터 흐름](#예시-데이터-흐름)
- [안전한 배포가 보장해야 하는 일곱 가지](#안전한-배포가-보장해야-하는-일곱-가지)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **카프카 배포에서 지켜야 할 것이 무엇이고, 그 목록은 어떤 기능들로
갈라지는가.**

## 보안은 컴포넌트가 아니라 시스템의 속성이다

- 유스케이스마다 요구가 다르다 — **웹사이트 활동 추적·지표 파이프라인부터 환자 기록
  관리·온라인 결제까지** 쓰이며, **각 유스케이스는 보안·성능·신뢰성·가용성 측면에서 요구
  조건이 다르다.** **가장 강력하고 최신인 보안 기능을 쓰는 것이 언제나 선호되지만, 보안을
  높이면 성능·비용·사용자 경험에 영향이 가므로 절충이 필요한 경우가 잦다** (11장,
  p.265).[^shapira2021]
- 그래서 카프카는 **여러 표준 보안 기술을 유스케이스마다 재단할 수 있는 설정 옵션과 함께
  지원**한다 (11장, p.265).[^shapira2021]
- 다루는 층위에 대한 책의 못박음 (11장, p.265):[^shapira2021]

  > Like performance and reliability, security is an aspect of the system that must be
  > addressed for the system as a whole, rather than component by component. The
  > security of a system is only as strong as the weakest link, and security processes and
  > policies must be enforced across the system, including the underlying platform.

  - 이 문장이 이 장의 구성을 설명한다 — 카프카의 커스터마이즈 가능한 보안 기능은
    **기존 보안 인프라스트럭처와 통합해 시스템 전체에 적용되는 일관된 보안 모델을 세우기
    위한 것**이다 (11장, p.265).[^shapira2021] 카프카 밖으로 나가는 부분은
    [카프카 플랫폼 보안](../concepts/kafka-platform-security.md)에 있다.

## 보안 절차 다섯

- 카프카는 **데이터의 기밀성(confidentiality)·무결성(integrity)·가용성(availability)을
  세우고 유지하기 위해 일련의 보안 절차**를 쓴다. 정의는 원문이 짧고 정확하다 (11장,
  pp.265–266):[^shapira2021]

  > - Authentication establishes your identity and determines who you are.
  > - Authorization determines what you are allowed to do.
  > - Encryption protects your data from eavesdropping and tampering.
  > - Auditing tracks what you have done or have attempted to do.
  > - Quotas control how much resources you can utilize.

  - 이 다섯이 이 축의 페이지 분할과 그대로 대응한다 — 인증(authentication)은
    [보안 프로토콜](../concepts/kafka-security-protocols.md) 이하,
    인가(authorization)와 감사(auditing)는
    [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md),
    암호화(encryption)는 [카프카 암호화](../concepts/kafka-encryption.md)가 맡는다.
- 다섯 중 쿼터(quota)만은 이 장이 다루지 않는다 — **사용자 사이의 공정한 자원 배분을 통해
  서비스 가용성에 기여하는 쿼터의 상세는 3장을 보라**고 넘긴다 (11장,
  p.268).[^shapira2021] 그 자리는
  [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md)다.

## 예시 데이터 흐름

- 배포를 잠그는 법을 이해하려면 **먼저 데이터가 카프카 클러스터를 어떻게 흐르는지** 본다.
  책은 그림 11-1의 여섯 단계를 장 전체의 기준선으로 삼아, **모든 단계에서 데이터를 보호하도록
  카프카를 어떻게 설정할 수 있는지**를 이 흐름 위에서 검토한다 (11장, p.266, 그림
  11-1):[^shapira2021]
  - **앨리스가 `customerOrders` 토픽의 한 파티션에 고객 주문 레코드를 생산**하고, 레코드는
    그 파티션의 리더로 간다.
  - **리더 브로커가 레코드를 자신의 로컬 로그 파일에 쓴다.**
  - **팔로워 브로커가 리더에서 메시지를 가져와 자신의 로컬 레플리카 로그 파일에 쓴다.**
  - **필요하면 리더 브로커가 주키퍼의 파티션 상태를 갱신해 인-싱크 레플리카를 갱신한다.**
    - 버전 조건: Kafka 3.9 이하 — 4.0에서 주키퍼가 제거돼 이 단계의 주체가 달라진다.
      [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) 참조.
  - **밥이 `customerOrders`에서 고객 주문 레코드를 소비**해 앨리스가 생산한 레코드를 받는다.
  - **내부 애플리케이션이 `customerOrders`에 도착하는 모든 메시지를 처리해 인기 상품에 대한
    실시간 지표를 만든다.**
- 이 흐름의 각 단계가 원래 무엇인지는 다른 페이지가 갖고 있다 — 생산 경로는
  [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md), 리더와 팔로워의 복제는
  [카프카 복제 프로토콜](../concepts/kafka-replication-protocol.md), 로컬 로그 파일은
  [카프카 물리적 저장](../concepts/kafka-physical-storage.md)에 있다.

## 안전한 배포가 보장해야 하는 일곱 가지

- 위 흐름 위에서 **안전한 배포가 보장해야 하는 것**을 책은 일곱 항목으로 세운다 (11장,
  p.267):[^shapira2021]
  - **클라이언트 진정성(client authenticity)** — 앨리스가 브로커로 클라이언트 연결을 맺을 때
    **브로커는 메시지가 정말 앨리스에게서 오는 것인지 확인하도록 클라이언트를 인증해야**
    한다.
  - **서버 진정성(server authenticity)** — 리더 브로커로 메시지를 보내기 전에 **앨리스의
    클라이언트는 그 연결이 진짜 브로커로 가는 것인지 검증해야** 한다.
  - **데이터 프라이버시(data privacy)** — **메시지가 흐르는 모든 연결과 메시지가 저장되는
    모든 디스크가 암호화되거나 물리적으로 보호돼**, 엿듣는 자가 데이터를 읽지 못하고 데이터를
    훔쳐 갈 수 없어야 한다.
  - **데이터 무결성(data integrity)** — **안전하지 않은 네트워크로 전송되는 데이터에는 변조를
    탐지할 수 있도록 메시지 다이제스트가 포함**돼야 한다.
  - **접근 제어(access control)** — **로그에 메시지를 쓰기 전에 리더 브로커는 앨리스가
    `customerOrders`에 쓸 권한이 있는지 검증**해야 하고, **밥의 컨슈머에 메시지를 돌려주기
    전에는 밥이 그 토픽을 읽을 권한이 있는지 검증**해야 한다. **밥의 컨슈머가 그룹 관리를
    쓴다면 브로커는 밥이 그 컨슈머 그룹에 접근할 수 있는지도 검증**해야 한다.
  - **감사 가능성(auditability)** — **브로커·앨리스·밥과 다른 클라이언트가 수행한 모든
    작업을 보여 주는 감사 기록(audit trail)이 로그로 남아야** 한다.
  - **가용성(availability)** — **일부 사용자가 가용 대역폭을 독차지하거나 서비스 거부 공격으로
    브로커를 압도하는 것을 막도록 브로커가 쿼터와 제한을 적용**해야 하고, **브로커 가용성이
    주키퍼 가용성과 주키퍼에 저장된 메타데이터의 무결성에 의존하므로 카프카 클러스터의
    가용성을 위해 주키퍼도 잠가야** 한다.
    - 버전 조건: Kafka 3.9 이하 — 주키퍼 부분에 한한다.
      [주키퍼 보안](../concepts/kafka-zookeeper-security.md) 참조.
- 이 일곱이 어디로 내려가는지가 장의 순서다 — **먼저 카프카의 연결 모델과 클라이언트-브로커
  연결에 걸리는 보안 프로토콜을 소개하고, 프로토콜별 인증 능력으로 클라이언트 진정성과 서버
  진정성을 확인**한다. **이어 데이터 프라이버시와 데이터 무결성을 위해 단계별 암호화 선택지를
  검토**하고, **접근 제어를 관리하는 커스터마이즈 가능한 인가와 감사 가능성에 기여하는 주요
  로그**를 다룬 뒤, **가용성 유지에 필요한 주키퍼와 플랫폼의 보안**으로 끝낸다 (11장,
  pp.267–268).[^shapira2021]

## 이어지는 페이지

- [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md) — 리스너마다 고르는 네
  가지 프로토콜과 그것이 정하는 인증·암호화 수준
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — 서버·클라이언트 진정성을
  인증서로 세우는 쪽
- [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md) — 자격 증명으로 세우는 쪽
- [카프카 암호화](../concepts/kafka-encryption.md) — 데이터 프라이버시와 무결성이 내려가는 곳
- [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md) — 접근 제어와 감사
  가능성이 내려가는 곳
- [주키퍼 보안](../concepts/kafka-zookeeper-security.md) — 가용성이 의존하는 메타데이터 쪽
- [카프카 플랫폼 보안](../concepts/kafka-platform-security.md) — 카프카 밖의 나머지
- [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md) — 다섯 절차 중 이 장이 3장으로
  넘긴 하나
- [데이터 파이프라인 고려사항](../concepts/kafka-data-pipeline-considerations.md) — 9장이
  파이프라인 관점에서 던진 보안 질문 다섯

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka" — 인용 블록 둘은 각각 p.265
    본문과 pp.265–266 "Locking Down Kafka" 절의 절차 목록 원문

---
type: concept
title: 카프카 보안 프로토콜
description: 브로커 리스너마다 고르는 보안 프로토콜 네 가지 — 전송 계층(PLAINTEXT·SSL)과 인증 계층(SSL·SASL)의 조합으로 만들어지는 PLAINTEXT·SSL·SASL_PLAINTEXT·SASL_SSL, 리스너와 브로커 간 통신을 엮는 설정, 클라이언트가 부트스트랩 서버로 리스너를 고르는 방식, 그리고 인증이 만들어 내는 KafkaPrincipal
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 보안 프로토콜

- [리스너마다 다른 보안](#리스너마다-다른-보안)
- [두 기술이 만드는 네 프로토콜](#두-기술이-만드는-네-프로토콜)
- [리스너와 브로커 간 통신 설정](#리스너와-브로커-간-통신-설정)
- [클라이언트 쪽](#클라이언트-쪽)
- [인증이 만들어 내는 것 — KafkaPrincipal](#인증이-만들어-내는-것--kafkaprincipal)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **브로커 리스너에 무엇을 걸 수 있고, 그 선택이 무엇을 결정하는가.**

## 리스너마다 다른 보안

- **카프카 브로커는 하나 이상의 엔드포인트에 리스너(listener)를 설정하고 그 리스너로
  클라이언트 연결을 받는다.** **리스너마다 자기 보안 설정을 가질 수 있다** (11장,
  p.268).[^shapira2021] 리스너 설정 자체는
  [카프카 브로커 설정](../concepts/kafka-broker-configuration.md)에 있고, 이 페이지는 그
  값의 의미를 준다.
- 리스너를 나누는 이유는 요구가 다르기 때문이다 — **물리적으로 보호되고 인가된 인원만 접근
  가능한 사설 내부 리스너의 보안 요구는 공용 인터넷으로 접근 가능한 외부 리스너의 요구와
  다를 수 있다** (11장, p.268).[^shapira2021]
- **보안 프로토콜의 선택이 인증 수준과 전송 중 데이터의 암호화 수준을 결정**한다 (11장,
  p.268).[^shapira2021]

## 두 기술이 만드는 네 프로토콜

- **카프카는 TLS와 SASL이라는 두 표준 기술로 네 개의 보안 프로토콜을 지원**한다 (11장,
  p.268):[^shapira2021]
  - **전송 계층 보안(Transport Layer Security, TLS)** — **흔히 그 선행 규격인 보안 소켓
    계층(Secure Sockets Layer, SSL)의 이름으로 불리며, 암호화뿐 아니라 클라이언트·서버 인증도
    지원**한다.
  - **단순 인증 및 보안 계층(Simple Authentication and Security Layer, SASL)** — **연결
    지향 프로토콜에서 서로 다른 메커니즘으로 인증을 제공하는 프레임워크**다.
- **각 카프카 보안 프로토콜은 전송 계층(PLAINTEXT 또는 SSL)과 선택적 인증 계층(SSL 또는
  SASL)의 조합**이다 (11장, p.268):[^shapira2021]
  - `PLAINTEXT` — **인증이 없는 PLAINTEXT 전송 계층.** **인증도 암호화도 쓰지 않으므로 민감하지
    않은 데이터를 처리하는 사설 네트워크 안에서만 적합**하다.
  - `SSL` — **선택적 SSL 클라이언트 인증이 붙는 SSL 전송 계층.** **클라이언트·서버 인증과
    암호화가 지원되므로 안전하지 않은 네트워크에서 쓰기에 적합**하다.
  - `SASL_PLAINTEXT` — **SASL 클라이언트 인증이 붙는 PLAINTEXT 전송 계층.** **일부 SASL
    메커니즘은 서버 인증도 지원**한다. **암호화를 지원하지 않으므로 사설 네트워크 안에서만
    적합**하다.
  - `SASL_SSL` — **SASL 인증이 붙는 SSL 전송 계층.** **클라이언트·서버 인증과 암호화가
    지원되므로 안전하지 않은 네트워크에서 쓰기에 적합**하다.
- TLS가 무엇에 기대는지는 책이 따로 박스로 남겼다 (11장, p.269):[^shapira2021]

  > TLS relies on a Public Key Infrastructure (PKI) to create, manage, and distribute
  > digital certificates that can be used for asymmetric encryption, avoiding the need for
  > distributing shared secrets between servers and clients. Session keys generated during
  > the TLS handshake enable symmetric encryption with higher performance for subsequent
  > data transfer.

  - 즉 공개 키 기반 구조(Public Key Infrastructure, PKI)가 디지털 인증서를 담당하고, **TLS
    핸드셰이크에서 만들어진 세션 키(session key)가 이후 데이터 전송을 더 빠른 대칭 암호화로
    돌린다.** **HTTP·SMTP·FTP 같은 애플리케이션 프로토콜이 전송 중 데이터의 프라이버시와
    무결성을 TLS에 기댄다**는 것이 같은 박스의 앞부분이다 (11장, p.269).[^shapira2021]

## 리스너와 브로커 간 통신 설정

- **브로커 간 통신에 쓸 리스너는 `inter.broker.listener.name`이나
  `security.inter.broker.protocol`을 설정해 고른다.** 그 프로토콜에 대해서는 **서버 쪽
  옵션과 클라이언트 쪽 옵션을 둘 다 브로커 설정에 줘야** 하는데, **브로커가 그 리스너에 대해
  클라이언트 연결을 맺어야 하기 때문**이다 (11장, p.269).[^shapira2021]
- 아래는 **브로커 간 리스너와 내부 리스너에 SSL을, 외부 리스너에 SASL_SSL을 설정하는 예**다.
  리스너 이름이 보안 프로토콜 이름이 아닐 때 `listener.security.protocol.map`이 그 대응을
  주는 자리를 이 예가 보여 준다 (11장, p.269):[^shapira2021]

  ```properties
  listeners=EXTERNAL://:9092,INTERNAL://10.0.0.2:9093,BROKER://10.0.0.2:9094
  advertised.listeners=EXTERNAL://broker1.example.com:9092,INTERNAL://broker1.local:9093,BROKER://broker1.local:9094
  listener.security.protocol.map=EXTERNAL:SASL_SSL,INTERNAL:SSL,BROKER:SSL
  inter.broker.listener.name=BROKER
  ```

## 클라이언트 쪽

- **클라이언트는 보안 프로토콜과 부트스트랩 서버로 설정되고, 그 부트스트랩 서버가 어느 브로커
  리스너에 붙을지를 정한다.** 중요한 성질이 하나 붙는다 — **클라이언트에 돌아가는 메타데이터에는
  부트스트랩 서버와 같은 리스너에 해당하는 엔드포인트만 담긴다** (11장,
  p.269).[^shapira2021] 즉 클라이언트 설정은 `security.protocol=SASL_SSL`과
  `bootstrap.servers=broker1.example.com:9092,broker2.example.com:9092` 두 줄이 뼈대다.
- 메타데이터 응답이 무엇을 돌려주고 클라이언트가 그것으로 무엇을 하는지는
  [카프카 요청 처리](../concepts/kafka-request-processing.md)에 있다.

## 인증이 만들어 내는 것 — KafkaPrincipal

- **인증(authentication)은 클라이언트 진정성과 서버 진정성을 검증하기 위해 클라이언트와 서버의
  신원(identity)을 세우는 과정**이다. **앨리스의 클라이언트가 고객 주문 레코드를 생산하려고
  리더 브로커에 연결할 때, 서버 인증은 클라이언트가 말을 걸고 있는 서버가 실제 브로커임을
  클라이언트가 확인할 수 있게 하고, 클라이언트 인증은 비밀번호나 디지털 인증서 같은 앨리스의
  자격 증명을 검증해 그 연결이 사칭이 아니라 앨리스에게서 온 것임을 판정**한다 (11장,
  p.269).[^shapira2021]
- 인증이 끝나면 남는 것이 주체다 — **한번 인증되면 앨리스의 신원은 연결의 수명 내내 그 연결에
  결합**된다. **카프카는 클라이언트 신원을 `KafkaPrincipal` 인스턴스로 표현하고, 이 주체
  (principal)를 그 클라이언트 신원의 연결에 자원 접근을 부여하고 쿼터를 할당하는 데
  쓴다** (11장, pp.269–270).[^shapira2021] 쿼터가 주체를 어떻게 쓰는지는
  [카프카 클라이언트 쿼터](../concepts/kafka-client-quotas.md)에 있다.
- **연결마다의 `KafkaPrincipal`은 인증 프로토콜에 따라 인증 과정에서 세워진다.** 예컨대
  **비밀번호 기반 인증에서 제공된 사용자 이름에 근거해 앨리스에게 `User:Alice` 주체가 쓰일 수**
  있다. **`KafkaPrincipal`은 브로커의 `principal.builder.class`를 설정해 커스터마이즈**할 수
  있다 (11장, p.270).[^shapira2021]
- 인증되지 않은 연결에는 이름이 따로 있다 — **`User:ANONYMOUS` 주체가 인증되지 않은 연결에
  쓰이며, 여기에는 PLAINTEXT 리스너의 클라이언트뿐 아니라 SSL 리스너의 인증되지 않은
  클라이언트도 포함**된다 (11장, p.270).[^shapira2021]

## 이어지는 페이지

- [카프카 보안 모델](../concepts/kafka-security-model.md) — 이 선택이 무엇을 지키려는
  것인지의 목록
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — `SSL`·`SASL_SSL`을 골랐을 때
  실제로 채워야 하는 것
- [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md) —
  `SASL_PLAINTEXT`·`SASL_SSL`을 골랐을 때 채워야 하는 것
- [카프카 브로커 설정](../concepts/kafka-broker-configuration.md) — `listeners`와
  `listener.security.protocol.map`이 원래 사는 곳
- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 메타데이터 응답이 클라이언트를
  어느 브로커로 보내는지
- [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md) — 여기서 만들어진 주체가
  쓰이는 곳

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka" — 인용 블록은 p.269
    "TLS/SSL" 박스 원문 중 뒷부분. 코드 펜스는 p.269 예제이며 원문에서 줄바꿈으로 잘려 있던
    `advertised.listeners` 값 한 줄만 이어 붙였다(보탠 줄 없음)

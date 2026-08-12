---
type: concept
title: 카프카 SASL 인증
description: SASL을 쓰는 리스너에서 인증이 성립하는 구조 — 서버 챌린지와 클라이언트 응답의 교환을 메커니즘이 정의한다는 뼈대, 리스너별로 켜는 sasl.enabled.mechanisms와 클라이언트의 sasl.mechanism, JAAS 설정을 리스너·메커니즘 접두어로 거는 방식, 그리고 기존 인증 인프라와 붙이는 콜백 핸들러 세 종류
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 SASL 인증

- [챌린지와 응답](#챌린지와-응답)
- [리스너에 메커니즘을 켠다](#리스너에-메커니즘을-켠다)
- [JAAS 설정](#jaas-설정)
- [콜백 핸들러 세 종류](#콜백-핸들러-세-종류)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **SASL 인증은 무엇으로 이뤄지고, 그것을 리스너에 어떻게 매다는가.**

## 챌린지와 응답

- **카프카 프로토콜은 SASL을 쓴 인증을 지원하며 흔히 쓰이는 여러 SASL 메커니즘을 기본으로
  내장**한다. **SASL은 TLS를 전송 계층으로 삼아 결합해 인증과 암호화를 갖춘 보안 채널을 만들
  수** 있다 (11장, p.275).[^shapira2021] 그 조합이 `SASL_SSL`이며, 네 프로토콜의 관계는
  [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md)에 있다.
- 인증이 진행되는 방식이 메커니즘의 정의다 — **SASL 인증은 서버 챌린지와 클라이언트 응답의
  연쇄로 수행되며, 그 연쇄와 챌린지·응답의 전송 형식을 SASL 메커니즘이 정의**한다 (11장,
  p.275).[^shapira2021]
- **카프카 브로커가 기본으로 지원하는 SASL 메커니즘은 넷**이며, **기존 보안 인프라스트럭처와
  통합할 수 있도록 콜백을 커스터마이즈할 수** 있다 — `GSSAPI`(케르베로스), `PLAIN`(사용자
  이름·비밀번호), `SCRAM-SHA-256`·`SCRAM-SHA-512`, `OAUTHBEARER`(OAuth 베어러 토큰) (11장,
  p.275).[^shapira2021] 넷의 차이와 각각의 위험은
  [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md)에 있다.

## 리스너에 메커니즘을 켠다

- **브로커에서 SASL이 켜진 리스너마다 `sasl.enabled.mechanisms`를 설정해 하나 이상의 SASL
  메커니즘을 켤 수** 있고, **클라이언트는 `sasl.mechanism`을 설정해 켜져 있는 것 중 아무거나
  고를 수** 있다 (11장, p.275).[^shapira2021]
- 브로커 간 통신에는 별도 설정이 붙는다 — 그 리스너가 브로커 간 통신에 쓰인다면
  `sasl.mechanism.inter.broker.protocol`로 브로커 간 SASL 메커니즘을 지정한다 (11장,
  p.277).[^shapira2021] 리스너를 브로커 간 통신에 배정하는 쪽은
  [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md)의 `inter.broker.listener.name`이다.

## JAAS 설정

- **카프카는 SASL을 설정하는 데 자바 인증·인가 서비스(Java Authentication and Authorization
  Service, JAAS)를 쓴다.** **설정 옵션 `sasl.jaas.config`는 로그인 모듈 하나와 그 옵션을
  지정하는 JAAS 설정 항목 하나를 담는다** (11장, p.275).[^shapira2021]
- 접두어가 리스너와 메커니즘을 가른다 — **브로커는 `sasl.jaas.config`를 설정할 때 리스너
  접두어와 메커니즘 접두어를 쓴다.** 예컨대 **`listener.name.external.gssapi.sasl.jaas.config`는
  `EXTERNAL`이라는 이름의 리스너에서 SASL/GSSAPI에 대한 JAAS 설정 항목을 설정**한다. 접두어에
  들어가는 리스너 이름과 SASL 메커니즘은 소문자다 (11장, pp.275–277).[^shapira2021]
- **브로커와 클라이언트의 로그인 과정은 이 JAAS 설정을 보고 인증에 쓸 공개·비공개 자격 증명을
  결정**한다 (11장, p.275).[^shapira2021]
- 파일로 주는 길도 있지만 권장되지 않는다 — **JAAS 설정은 자바 시스템 속성
  `java.security.auth.login.config`로 설정 파일에 지정할 수도** 있다. 다만 **카프카의
  `sasl.jaas.config` 옵션이 권장되는데, 비밀번호 보호를 지원하고 한 리스너에 여러 메커니즘이
  켜져 있을 때 메커니즘마다 따로 설정할 수 있기 때문**이다 (11장, p.276).[^shapira2021]
  비밀번호 보호가 무엇인지는
  [카프카 플랫폼 보안](../concepts/kafka-platform-security.md)에 있다.

## 콜백 핸들러 세 종류

- **카프카가 지원하는 SASL 메커니즘은 콜백 핸들러(callback handler)를 써서 서드파티 인증
  서버와 통합하도록 커스터마이즈**할 수 있다. 종류는 셋이다 (11장, p.276):[^shapira2021]
  - **로그인 콜백 핸들러** — **브로커나 클라이언트에 줘서 로그인 과정을 커스터마이즈**한다.
    예컨대 인증에 쓸 자격 증명을 획득하는 데 쓴다.
  - **서버 콜백 핸들러** — **클라이언트 자격 증명의 인증을 수행**한다. 예컨대 외부 비밀번호
    서버로 비밀번호를 검증하는 데 쓴다.
  - **클라이언트 콜백 핸들러** — **자격 증명을 JAAS 설정에 넣는 대신 주입**한다.
- 이 세 지점이 실제로 무엇을 대체하는지는 메커니즘별 절이 보여 준다 — SASL/PLAIN의 내장
  비밀번호 저장소를 외부 저장소로 바꾸거나, OAUTHBEARER의 토큰 획득·검증을 실제 OAuth 서버로
  옮기는 일이 전부 여기서 일어난다
  ([카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md)).

## 이어지는 페이지

- [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md) — 네 메커니즘의 설정과 각각이
  안고 있는 위험
- [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md) — SASL이 전송 계층과
  조합되는 자리
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — `SASL_SSL`에서 SASL이 기대는
  그 전송 계층
- [카프카 위임 토큰](../concepts/kafka-delegation-tokens.md) — SASL/SCRAM 위에 얹혀 자격
  증명 배포를 대신하는 기제
- [카프카 재인증](../concepts/kafka-reauthentication.md) — SASL로 인증된 연결에만 걸리는
  수명 관리
- [카프카 플랫폼 보안](../concepts/kafka-platform-security.md) — JAAS 설정에 들어가는 평문
  비밀번호를 밖으로 빼는 쪽

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "SASL" 절 — JAAS 설정 파일에
    대한 서술은 p.276 "JAAS Configuration File" 박스

---
type: concept
title: 주키퍼 보안
description: 카프카 가용성이 의존하는 메타데이터 저장소를 잠그는 법 — 주키퍼가 지원하는 인증 수단과 DIGEST-MD5를 프로덕션에서 배제하는 이유, JAAS 파일로 서버와 브로커 양쪽을 설정하는 방식, 카프카와 달리 SASL과 SSL 인증이 겹치면 주체가 여럿 결합된다는 차이, 그리고 zookeeper.set.acl이 만드는 기본 접근 권한
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 주키퍼 보안

- [버전 조건](#버전-조건)
- [왜 주키퍼를 잠그는가](#왜-주키퍼를-잠그는가)
- [SASL](#sasl)
- [SSL](#ssl)
- [인가](#인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **카프카가 기대는 메타데이터 저장소는 무엇으로 인증하고 무엇으로 잠그는가.**

## 버전 조건

> **버전 조건**: Kafka 3.9 이하. 이 페이지는 카프카가 메타데이터를 주키퍼에 두던 시기의
> 서술이며, 주키퍼 모드가 남아 있던 마지막 릴리스까지 적용된다. **4.0 이상에는 적용되지
> 않는다** — 그쪽에는 주키퍼가 없다
> ([주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)).

## 왜 주키퍼를 잠그는가

- **주키퍼는 카프카 클러스터의 가용성을 유지하는 데 결정적인 카프카 메타데이터를 저장하므로,
  카프카를 지키는 것에 더해 주키퍼를 지키는 것이 필수적**이다 (11장,
  p.299).[^shapira2021] 주키퍼가 무엇을 맡는지는
  [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)에 있다.
- 여기에는 이 장이 다룬 것들이 실제로 저장돼 있다 — SCRAM 자격 증명
  ([카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md))과 ACL
  ([카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md))이 그 예이고, 두 절의
  고려사항이 모두 "안전한 주키퍼"를 전제로 삼는다.

## SASL

- **주키퍼는 케르베로스 인증을 위한 SASL/GSSAPI와 사용자 이름·비밀번호 인증을 위한
  SASL/DIGEST-MD5로 인증을 지원**한다 (11장, p.299).[^shapira2021]
- 둘 중 하나에는 경고가 붙는다 — **SASL/DIGEST-MD5는 TLS 암호화와 함께만 써야 하며, 알려진
  보안 취약점 때문에 프로덕션에는 적합하지 않다** (11장, p.299).[^shapira2021]
- 설정 통로는 자바 시스템 속성이다 — **주키퍼의 SASL 설정은 자바 시스템 속성
  `java.security.auth.login.config`로 주며, 그 속성은 주키퍼 서버에 맞는 로그인 모듈과 옵션을
  담은 로그인 절이 있는 JAAS 설정 파일을 가리켜야** 한다. **카프카 브로커는 SASL이 켜진 주키퍼
  서버와 통신하기 위해 주키퍼 클라이언트 쪽 로그인 절로 설정**돼야 한다 (11장,
  p.299).[^shapira2021] 카프카 쪽에서 같은 속성보다 `sasl.jaas.config`가 권장되는 이유는
  [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md)에 있다.
- 서버 쪽 JAAS 파일에는 **케르베로스 인증을 켜는 `Server` 절**이, 브로커 쪽 JAAS 파일에는
  **브로커의 클라이언트 자격 증명을 주는 `Client` 절**이 들어가며, 둘 다
  `Krb5LoginModule`에 `useKeyTab`·`storeKey`·`keyTab`·`principal`을 주는 같은 모양이다 (11장,
  pp.299–300).[^shapira2021]
- 주키퍼 서버 쪽에서 SASL 인증을 켜려면 **주키퍼 설정 파일에 인증 제공자를 설정**한다 —
  `authProvider.sasl=org.apache.zookeeper.server.auth.SASLAuthenticationProvider`와
  `kerberos.removeHostFromPrincipal=true`·`kerberos.removeRealmFromPrincipal=true` (11장,
  p.299).[^shapira2021]
- 뒤의 두 줄에는 이유가 있다 — **주키퍼는 기본적으로
  `kafka/broker1.example.com@EXAMPLE.COM` 같은 전체 케르베로스 주체를 클라이언트 신원으로
  쓴다.** **주키퍼 인가를 위해 ACL을 켤 때는 모든 브로커가 같은 주체를 갖도록 주키퍼 서버에
  `kerberos.removeHostFromPrincipal=true`와 `kerberos.removeRealmFromPrincipal=true`를
  설정**해야 한다 (11장, p.300).[^shapira2021]

## SSL

- **주키퍼는 3.5.0에서 TLS 지원을 추가해 상호 인증과 전송 중 데이터 암호화가 가능**해졌다
  (11장, p.299).[^shapira2021]
  - 버전 조건: 주키퍼 3.5.0 이상 — 카프카 버전이 아니라 주키퍼 자체의 경계다.
- **SSL은 SASL 인증을 쓰는 것을 포함해 어떤 주키퍼 엔드포인트에도 켤 수** 있다 (11장,
  p.300).[^shapira2021]
- 카프카와 갈리는 지점이 하나 있다 — **카프카처럼 SSL로 클라이언트 인증을 켤 수 있지만,
  카프카와 달리 SASL과 SSL 클라이언트 인증을 둘 다 쓰는 연결은 두 프로토콜 모두로 인증되어
  연결에 여러 주체가 결합**된다. 그리고 **주키퍼 인가자는 연결에 결합된 주체 중 하나라도 접근
  권한이 있으면 자원 접근을 부여**한다 (11장, p.300).[^shapira2021] 카프카 쪽에서
  `SASL_SSL` 리스너가 TLS 클라이언트 인증을 아예 끄는 것과 대비된다
  ([카프카 TLS 설정](../concepts/kafka-tls-configuration.md)).
- 주키퍼 서버 쪽 설정 — **서버의 호스트명이나 와일드카드 호스트가 든 키스토어를 설정**하고,
  **클라이언트 인증을 켰다면 클라이언트 인증서를 검증할 트러스트스토어도 필요**하다. 키는
  `secureClientPort`, `serverCnxnFactory`(Netty), `authProvider.x509`,
  `ssl.keyStore.*`·`ssl.trustStore.*`다 (11장, p.300).[^shapira2021]
- 카프카 쪽 설정은 `zookeeper.` 접두어가 붙은 대칭형이다. **주키퍼로 가는 카프카 연결에 SSL을
  설정하려면 브로커에 주키퍼 인증서를 검증할 트러스트스토어를 설정**하고, **클라이언트 인증이
  켜져 있으면 키스토어도** 준다 (11장, pp.300–301):[^shapira2021]

  ```properties
  zookeeper.ssl.client.enable=true
  zookeeper.clientCnxnSocket=org.apache.zookeeper.ClientCnxnSocketNetty
  zookeeper.ssl.keystore.location=/path/to/zkclient.ks.p12
  zookeeper.ssl.keystore.password=zkclient-ks-password
  zookeeper.ssl.keystore.type=PKCS12
  zookeeper.ssl.truststore.location=/path/to/zkclient.ts.p12
  zookeeper.ssl.truststore.password=zkclient-ts-password
  zookeeper.ssl.truststore.type=PKCS12
  ```

  - 이 설정 묶음이 4.0에서 통째로 사라진다는 것은
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md)의 "주키퍼가 제거되면서 사라진 것"
    절에 있다.

## 인가

- **주키퍼 노드의 인가는 그 경로에 ACL을 설정해 켠다.** **브로커에 `zookeeper.set.acl=true`가
  설정되면 브로커가 노드를 만들 때 그 주키퍼 노드에 ACL을 설정**한다 (11장,
  p.301).[^shapira2021]
- 기본 권한이 비대칭이다 — **기본적으로 메타데이터 노드는 누구나 읽을 수 있지만 브로커만
  수정할 수** 있다. **주키퍼에서 직접 메타데이터를 갱신해야 하는 내부 관리 사용자를 위해 필요하면
  ACL을 추가**할 수 있다 (11장, p.301).[^shapira2021]
- 예외가 명시돼 있다 — **SCRAM 자격 증명을 담은 노드 같은 민감한 경로는 기본적으로 누구나 읽을
  수 있지 않다** (11장, p.301).[^shapira2021]

## 이어지는 페이지

- [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) — 여기서 지키는 대상이 무엇이고 4.0에서
  어떻게 사라졌는지
- [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md) — SCRAM 자격 증명이 여기 저장된다
- [카프카 인가와 ACL](../concepts/kafka-authorization-and-acl.md) — 카프카 ACL도 여기 저장된다
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — 키스토어·트러스트스토어를 만드는
  같은 절차
- [카프카 보안 모델](../concepts/kafka-security-model.md) — 가용성 보장이 주키퍼에 의존한다는
  그 항목

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "Securing ZooKeeper" 절
    (pp.299–301) — 브로커 주체에 대한 서술은 p.300 "Broker Principal" 박스. 코드 펜스는
    pp.300–301 브로커 쪽 주키퍼 SSL 설정 예제 전문. 주키퍼 서버 쪽 설정과 JAAS 파일 예제는
    옮기지 않고 설정 키 이름만 인라인으로 남겼다

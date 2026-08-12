---
type: concept
title: 카프카 SASL 메커니즘
description: 카프카가 기본으로 내장한 SASL 메커니즘 네 가지의 설정과 각각이 안고 있는 위험 — 케르베로스를 쓰는 GSSAPI, 비밀번호를 그대로 보내는 PLAIN, 솔트와 해시로 그것을 피하는 SCRAM, 수명 짧은 토큰을 쓰는 OAUTHBEARER, 그리고 네 경우 모두에서 반복되는 "TLS 없이는 쓰지 말라"는 결론
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 SASL 메커니즘

- [SASL/GSSAPI — 케르베로스](#saslgssapi--케르베로스)
- [SASL/PLAIN — 사용자 이름과 비밀번호](#saslplain--사용자-이름과-비밀번호)
- [SASL/SCRAM — 솔트와 해시](#saslscram--솔트와-해시)
- [SASL/OAUTHBEARER — 베어러 토큰](#sasloauthbearer--베어러-토큰)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **네 SASL 메커니즘은 각각 무엇으로 인증하고, 무엇을 조심해야 하는가.**

공통 뼈대(`sasl.enabled.mechanisms`·`sasl.mechanism`·JAAS 접두어·콜백 핸들러)는
[카프카 SASL 인증](../concepts/kafka-sasl-authentication.md)에 있다. 이 페이지는 메커니즘별
차이만 다룬다.

## SASL/GSSAPI — 케르베로스

- **케르베로스(Kerberos)는 강한 암호화를 써서 안전하지 않은 네트워크에서 안전한 상호 인증을
  지원하는 널리 쓰이는 네트워크 인증 프로토콜**이고, **일반 보안 서비스 응용 프로그램
  인터페이스(Generic Security Service Application Program Interface, GSS-API)는 서로 다른 인증
  메커니즘으로 애플리케이션에 보안 서비스를 제공하는 프레임워크**다. **RFC-4752가 GSS-API의
  케르베로스 V5 메커니즘으로 인증하는 SASL 메커니즘 `GSSAPI`를 도입**했다 (11장,
  p.276).[^shapira2021]
- 쓰이는 이유는 생태계다 — **오픈 소스와 엔터프라이즈급 상용 케르베로스 서버 구현이 모두
  존재해 보안 요구가 엄격한 많은 분야에서 케르베로스가 인기 있는 선택이 됐다** (11장,
  p.276).[^shapira2021]
- **카프카는 자바 런타임 환경에 포함된 GSSAPI 보안 제공자로 케르베로스 인증을 지원**한다.
  **GSSAPI용 JAAS 설정에는 주체와 그 장기 키의 매핑을 암호화된 형태로 담은 키탭(keytab) 파일의
  경로가 들어간다** (11장, p.276).[^shapira2021]
- 브로커 쪽에서 지켜야 할 것 (11장, p.276):[^shapira2021]
  - **브로커마다 그 브로커의 호스트명을 포함하는 주체로 키탭을 만든다** — **클라이언트가 서버
    진정성을 확인하고 중간자 공격을 막기 위해 브로커 호스트명을 검증하기 때문**이다.
  - **케르베로스는 인증 중 호스트명 조회를 위해 안전한 DNS 서비스를 요구**한다. **정방향과
    역방향 조회가 일치하지 않는 배포에서는 클라이언트의 케르베로스 설정 파일 `krb5.conf`에
    `rdns=false`를 설정해 역방향 조회를 끌 수** 있다.
- 브로커의 JAAS 설정에는 **자바 런타임의 케르베로스 V5 로그인 모듈, 키탭 파일의 경로명, 전체
  브로커 주체**가 들어간다. 리스너·메커니즘 접두어가 붙는 형태를 그대로 보면 (11장,
  p.277):[^shapira2021]

  ```properties
  sasl.enabled.mechanisms=GSSAPI
  listener.name.external.gssapi.sasl.jaas.config=\
      com.sun.security.auth.module.Krb5LoginModule required \
      useKeyTab=true storeKey=true \
      keyTab="/path/to/broker1.keytab" \
      principal="kafka/broker1.example.com@EXAMPLE.COM";
  ```

  - **키탭 파일은 브로커 프로세스가 읽을 수 있어야** 하고, **브로커의 서비스 주체에는 브로커
    호스트명이 들어가야** 한다 (11장, p.277).[^shapira2021]
- **브로커 간 통신에 SASL/GSSAPI를 쓴다면 브로커 간 SASL 메커니즘과 케르베로스 서비스 이름도
  설정**해야 한다 — `sasl.mechanism.inter.broker.protocol=GSSAPI`와
  `sasl.kerberos.service.name=kafka` (11장, p.277).[^shapira2021]
- **클라이언트는 JAAS 설정에 자기 키탭과 주체를 설정하고, 접속하려는 서비스의 이름을 알리기
  위해 `sasl.kerberos.service.name`을 설정**한다. **클라이언트는 호스트명 없는 주체를 써도**
  된다 (11장, p.277).[^shapira2021]
- 주체가 정해지는 규칙 — **기본적으로 주체의 짧은 이름이 클라이언트 신원으로 쓰인다.** 예제에서
  클라이언트 주체는 `User:Alice`, 브로커 주체는 `User:kafka`다. **브로커 설정
  `sasl.kerberos.principal.to.local.rules`로 정규화된 전체 주체를 커스텀 주체로 변환하는 규칙
  목록을 적용**할 수 있다 (11장, p.277).[^shapira2021]
- 고려사항 (11장, pp.277–278):[^shapira2021]
  - **케르베로스를 쓰는 프로덕션 배포에는 `SASL_SSL`이 권장**된다 — **인증 흐름과 인증 후
    연결의 데이터 트래픽을 함께 보호**하기 위해서다. **TLS로 보안 전송 계층을 주지 않으면
    네트워크를 엿듣는 자가 사전 공격(dictionary attack)이나 무차별 대입 공격(brute-force
    attack)으로 클라이언트 자격 증명을 훔칠 만큼의 정보를 얻을 수** 있다.
  - **비밀번호에서 생성한 키보다 무작위로 생성한 키를 브로커에 쓰는 것이 안전**하다 —
    비밀번호에서 나온 키가 더 깨기 쉽다. **DES-MD5 같은 약한 암호화 알고리즘은 피하고 더 강한
    것을 쓴다.**
  - **키탭 파일을 가진 사용자는 누구든 그 사용자를 사칭할 수 있으므로 파일시스템 권한으로 접근을
    제한**해야 한다.
  - **SASL/GSSAPI는 서버 인증을 위해 안전한 DNS 서비스를 요구**한다. **KDC나 DNS 서비스에 대한
    서비스 거부 공격이 클라이언트의 인증 실패로 이어질 수 있으므로 이 서비스들의 가용성을
    모니터링**해야 한다. **케르베로스는 재전송 공격(replay attack)을 탐지하기 위해 설정
    가능한 편차를 가진 느슨하게 동기화된 시계에도 의존하므로, 시계 동기화가 안전한지 확인**해야
    한다.

## SASL/PLAIN — 사용자 이름과 비밀번호

- **RFC-4616은 TLS와 함께 쓰면 안전한 인증을 제공할 수 있는 단순한 사용자 이름·비밀번호 인증
  메커니즘을 정의**한다. **인증 중 클라이언트가 사용자 이름과 비밀번호를 서버로 보내고 서버는
  자기 비밀번호 저장소로 비밀번호를 검증**한다. **카프카는 커스텀 콜백 핸들러로 안전한 외부
  비밀번호 데이터베이스와 통합할 수 있는 SASL/PLAIN 지원을 내장**한다 (11장,
  p.278).[^shapira2021]
- 기본 구현이 비밀번호를 어디에 두는지가 이 메커니즘의 성격을 결정한다 — **SASL/PLAIN의 기본
  구현은 브로커의 JAAS 설정을 비밀번호 저장소로 쓴다.** **모든 클라이언트의 사용자 이름과
  비밀번호가 로그인 옵션으로 들어가고, 브로커는 인증 중 클라이언트가 준 비밀번호가 그 항목 중
  하나와 맞는지 검증**한다. 형태는 `PlainLoginModule` 아래에
  `user_Alice="Alice-password"`처럼 사용자마다 한 줄이며, **브로커의 사용자 이름과 비밀번호는
  SASL/PLAIN이 브로커 간 통신에 쓰일 때만 필요**하다 (11장, p.278).[^shapira2021]
- 그래서 기본 구현은 프로덕션용이 아니다 — **모든 비밀번호를 모든 브로커의 JAAS 설정에 저장하는
  내장 구현은 안전하지 않고, 사용자를 추가·제거하려면 모든 브로커를 재시작해야 하므로 유연하지도
  않다** (11장, p.278).[^shapira2021]
  - 대안은 콜백이다 — **프로덕션에서 SASL/PLAIN을 쓸 때는 커스텀 서버 콜백 핸들러로 브로커를
    안전한 서드파티 비밀번호 서버와 통합**한다. **커스텀 콜백 핸들러는 비밀번호 교체(password
    rotation)를 지원하는 데도 쓸 수** 있는데, **서버 쪽 콜백 핸들러가 모든 클라이언트가 새
    비밀번호로 옮겨 갈 때까지 겹치는 기간 동안 옛 비밀번호와 새 비밀번호를 둘 다 지원**하면
    된다 (11장, pp.278–279).[^shapira2021] 책은 그 예로 **아파치 도구 `htpasswd`로 만든
    파일들의 암호화된 비밀번호를 검증하는 `PlainServerCallbackHandler` 확장**을 보이고,
    브로커에는 `listener.name.external.plain.sasl.server.callback.handler.class`로 그 클래스를
    지정한다 (11장, pp.279–280).[^shapira2021]
  - 클라이언트 쪽에도 대칭이 있다 — **`AuthenticateCallbackHandler`를 구현한 클라이언트 콜백
    핸들러를 쓰면 시작 시점에 JAAS 설정에서 정적으로 읽는 대신 연결이 맺어질 때 런타임에
    비밀번호를 동적으로 읽어올 수** 있고, **암호화된 파일이나 외부 보안 서버에서 비밀번호를
    읽어 보안을 높일 수** 있다. 지정은 `sasl.client.callback.handler.class`로 한다 (11장,
    p.280).[^shapira2021] 책의 예제는 **비밀번호를 `PASSWORD` 타입 설정으로 정의해 로그 항목에
    비밀번호가 들어가지 않게** 하고, **최신 비밀번호를 쓰도록 콜백 안에서 설정 파일을 읽는다**
    (11장, p.280).[^shapira2021]
- 고려사항 (11장, p.280):[^shapira2021]
  - **SASL/PLAIN은 평문 비밀번호를 회선으로 보내므로, `SASL_SSL`로 암호화해 보안 전송 계층을
    줄 때만 `PLAIN` 메커니즘을 켜야** 한다.
  - **브로커와 클라이언트의 JAAS 설정에 평문으로 저장된 비밀번호는 안전하지 않으므로, 그
    비밀번호를 암호화하거나 안전한 비밀번호 저장소로 외부화하는 것을 고려**해야 한다. 그 방법은
    [카프카 플랫폼 보안](../concepts/kafka-platform-security.md)에 있다.
  - **모든 클라이언트 비밀번호를 브로커 JAAS 설정에 저장하는 내장 비밀번호 저장소 대신, 비밀번호를
    안전하게 저장하고 강한 비밀번호 정책을 강제하는 안전한 외부 비밀번호 서버를 쓴다.**

## SASL/SCRAM — 솔트와 해시

- **RFC-5802는 SASL/PLAIN처럼 비밀번호를 회선으로 보내는 비밀번호 인증 메커니즘의 보안 우려를
  해소하는 안전한 사용자 이름·비밀번호 인증 메커니즘을 도입**한다. 정의는 원문이 짧다 (11장,
  p.281):[^shapira2021]

  > The Salted Challenge Response Authentication Mechanism (SCRAM) avoids transmitting
  > clear-text passwords and stores passwords in a format that makes it impractical to
  > impersonate clients.

  - **솔팅(salting)은 비밀번호를 안전하게 저장하기 위해 단방향 암호화 해시 함수를 적용하기
    전에 비밀번호에 무작위 데이터를 섞는 것**이다 (11장, p.281).[^shapira2021]
- **카프카는 안전한 주키퍼가 있는 배포에서 추가 비밀번호 서버 없이 쓸 수 있는 SCRAM 제공자를
  내장**하며, **지원하는 메커니즘은 `SCRAM-SHA-256`과 `SCRAM-SHA-512`** 다 (11장,
  p.281).[^shapira2021]
  - 버전 조건: Kafka 3.9 이하 — 자격 증명 저장소가 주키퍼라는 서술에 한한다.
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) 참조.
- 사용자를 만드는 시점과 방법 (11장, p.281):[^shapira2021]
  - **초기 사용자 집합은 주키퍼를 띄운 뒤 브로커를 띄우기 전에 만들 수** 있다. **브로커는
    시동 중 SCRAM 사용자 메타데이터를 인메모리 캐시로 읽어 들여, 브로커 간 통신용 브로커
    사용자를 포함한 모든 사용자가 성공적으로 인증할 수 있게** 한다.
  - **사용자는 언제든 추가·삭제할 수 있고, 브로커는 주키퍼 워처(watcher)에 기반한 알림으로
    캐시를 최신으로 유지**한다.
  - 사용자 생성은 configs 툴로 한다 — `bin/kafka-configs.sh --zookeeper localhost:2181 --alter
    --add-config 'SCRAM-SHA-512=[iterations=8192,password=Alice-password]' --entity-type users
    --entity-name Alice`가 `User:Alice`를 만드는 명령이다.
- 브로커·클라이언트 설정은 다른 메커니즘과 같은 모양이다 — 브로커는
  `sasl.enabled.mechanisms=SCRAM-SHA-512`와
  `listener.name.external.scram-sha-512.sasl.jaas.config`에 `ScramLoginModule`을 걸고,
  **리스너가 브로커 간 통신에 쓰일 때만 브로커의 사용자 이름·비밀번호가 필요**하다.
  클라이언트는 `sasl.mechanism=SCRAM-SHA-512`와 JAAS 설정의 사용자 이름·비밀번호를 갖는다
  (11장, pp.281–282).[^shapira2021]
- 사용자 삭제의 의미가 즉각적이지 않다 — **configs 툴의 `--add-config`로 새 SCRAM 사용자를
  추가하고 `--delete-config`로 삭제**하는데, **기존 사용자가 삭제되면 그 사용자의 새 연결은
  맺어지지 않지만 이미 있던 연결은 계속 동작**한다. **사용자가 삭제된 뒤 기존 연결이 계속
  동작할 수 있는 시간을 제한하려면 브로커에 재인증 간격을 설정**한다 (11장,
  p.282).[^shapira2021] 그 설정은
  [카프카 재인증](../concepts/kafka-reauthentication.md)에 있다.
- 고려사항 (11장, p.282):[^shapira2021]
  - **SCRAM은 비밀번호에 무작위 솔트를 섞어 단방향 암호화 해시 함수를 적용해, 실제 비밀번호가
    회선으로 전송되거나 데이터베이스에 저장되는 것을 피한다.** 그러나 **비밀번호 기반 시스템은
    비밀번호만큼만 안전하므로, 무차별 대입 공격과 사전 공격으로부터 시스템을 지키려면 강한
    비밀번호 정책이 강제**돼야 한다.
  - 카프카가 주는 안전장치는 셋이다 — **`SHA-256`·`SHA-512`라는 강한 해시 알고리즘만 지원하고
    `SHA-1` 같은 약한 알고리즘은 배제**하며, 여기에 **기본 반복 횟수 4,096회와 저장되는 키마다
    다른 무작위 솔트**를 결합해 **주키퍼 보안이 침해됐을 때의 영향을 제한**한다.
  - **핸드셰이크 중 전송되는 키와 주키퍼에 저장되는 키를 무차별 대입 공격으로부터 보호할 추가
    조치가 필요**하다 — **엿듣는 자가 인증 중 해시된 키에 접근하는 것을 막기 위해 SCRAM은
    `SASL_SSL`을 보안 프로토콜로 써야** 하고, **주키퍼도 SSL이 켜져야 하며 저장소가 침해돼도
    저장된 키를 꺼낼 수 없도록 주키퍼 데이터를 디스크 암호화로 보호**해야 한다.
    - 버전 조건: Kafka 3.9 이하 — 주키퍼 부분에 한한다.
      [주키퍼 보안](../concepts/kafka-zookeeper-security.md) 참조.
  - **안전한 주키퍼가 없는 배포에서는 SCRAM 콜백으로 안전한 외부 자격 증명 저장소와 통합**할
    수 있다.

## SASL/OAUTHBEARER — 베어러 토큰

- **OAuth는 애플리케이션이 HTTP 서비스에 제한된 접근을 얻게 해 주는 인가 프레임워크**이고,
  **RFC-7628은 OAuth 2.0으로 얻은 자격 증명으로 비HTTP 프로토콜의 보호된 자원에 접근하게 해
  주는 `OAUTHBEARER` SASL 메커니즘을 정의**한다 (11장, p.283).[^shapira2021]
- 이 메커니즘이 피하려는 것 — **`OAUTHBEARER`는 수명이 더 짧고 자원 접근이 제한된 OAuth 2.0
  베어러 토큰을 씀으로써, 장기 비밀번호를 쓰는 메커니즘의 보안 취약점을 피한다.** **카프카는
  클라이언트 인증에 SASL/OAUTHBEARER를 지원해 서드파티 OAuth 서버와 통합할 수** 있다 (11장,
  p.283).[^shapira2021]
- 내장 구현에 대한 책의 경고 (11장, p.283):[^shapira2021]

  > The built-in implementation of OAUTHBEARER uses unsecured JSON Web Tokens (JWTs) and is
  > not suitable for production use.

  - **프로덕션 배포에서 안전한 인증을 제공하려면 표준 OAuth 서버와 통합하는 커스텀 콜백을
    추가**해야 한다 (11장, p.283).[^shapira2021]
- 설정 (11장, p.283):[^shapira2021]
  - **내장 구현은 토큰을 검증하지 않으므로 JAAS 설정에 로그인 모듈만 지정하면** 된다.
    **리스너가 브로커 간 통신에 쓰인다면 브로커가 시작하는 클라이언트 연결에 쓸 토큰의 상세도
    줘야** 한다.
  - **옵션 `unsecuredLoginStringClaim_sub`는 기본적으로 그 연결의 `KafkaPrincipal`을 결정하는
    주체(subject) 클레임**이다. 클라이언트가 `unsecuredLoginStringClaim_sub="Alice"`를 주면
    기본 주체는 `User:Alice`가 된다. **다른 클레임과 토큰 수명도 설정 가능**하다.
- 실제 OAuth 서버와 붙일 때 (11장, pp.283–284):[^shapira2021]
  - **카프카 클라이언트는 장기 비밀번호나 갱신 토큰으로 OAuth 서버에서 토큰을 얻도록
    `sasl.login.callback.handler.class`를 설정**해야 한다. **`OAUTHBEARER`가 브로커 간 통신에
    쓰인다면 브로커도 브로커 간 통신용 클라이언트 연결의 토큰을 얻기 위해 로그인 콜백 핸들러를
    설정**해야 한다.
  - **브로커는 클라이언트가 준 토큰을 검증하기 위해
    `listener.name.<listener-name>.oauthbearer.sasl.server.callback.handler.class`로 서버 콜백
    핸들러도 설정**해야 한다. 검증 콜백은 `OAuthBearerValidatorCallback`으로 토큰을 받고,
    선택적 확장은 `OAuthBearerExtensionsValidatorCallback`으로 검증한다.
- 고려사항 (11장, p.285):[^shapira2021]
  - **SASL/OAUTHBEARER 클라이언트는 OAuth 2.0 베어러 토큰을 네트워크로 보내고 그 토큰으로
    클라이언트를 사칭할 수 있으므로, 인증 트래픽을 암호화하도록 TLS를 켜야** 한다.
  - **수명이 짧은 토큰으로 토큰 침해 시의 노출을 제한**할 수 있다.
  - **연결이 인증에 쓴 토큰보다 오래 사는 것을 막기 위해 브로커에 재인증을 켤 수** 있다 —
    **브로커에 설정한 재인증 간격과 토큰 폐기 지원이 결합하면, 폐기 이후에도 기존 연결이 그
    토큰을 계속 쓸 수 있는 시간이 제한**된다.

## 이어지는 페이지

- [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md) — 네 메커니즘이 공유하는 뼈대와
  콜백 핸들러의 종류
- [카프카 위임 토큰](../concepts/kafka-delegation-tokens.md) — SASL/SCRAM 위에서 키탭·키스토어
  배포를 대신하는 기제
- [카프카 재인증](../concepts/kafka-reauthentication.md) — 수명 있는 자격 증명이 만료·폐기된
  뒤의 연결
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — 네 메커니즘이 공통으로 요구하는
  그 전송 계층
- [카프카 플랫폼 보안](../concepts/kafka-platform-security.md) — JAAS 설정의 평문 비밀번호를
  밖으로 빼는 쪽
- [주키퍼 보안](../concepts/kafka-zookeeper-security.md) — SCRAM 자격 증명이 저장되는 곳

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "SASL" 절의 메커니즘별 하위
    절(pp.276–285) — 인용 블록은 각각 p.281 SCRAM 정의와 p.283 OAUTHBEARER 내장 구현 경고
    원문. 코드 펜스는 p.277 브로커 GSSAPI 설정 예제이며 원문의 주석 번호 표식만 덜어내고
    줄 연결 백슬래시의 들여쓰기를 정돈했다(보탠 줄 없음). 자바 콜백 핸들러 예제들
    (pp.279–280, 284)은 옮기지 않고 산문으로만 요약했다

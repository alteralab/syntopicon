---
type: concept
title: 카프카 TLS 설정
description: SSL·SASL_SSL 리스너에 TLS를 실제로 거는 절차와 그때 판단해야 하는 것 — 키스토어와 트러스트스토어의 역할 분담, 호스트명 검증이 막는 것, ssl.client.auth의 세 값이 만드는 주체의 차이, 인증서를 만드는 keytool 흐름, 무중단 갱신, 그리고 CPU 오버헤드부터 서비스 거부 공격까지의 고려사항
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 TLS 설정

- [TLS 핸드셰이크가 하는 일](#tls-핸드셰이크가-하는-일)
- [성능 대가](#성능-대가)
- [키스토어와 트러스트스토어](#키스토어와-트러스트스토어)
- [호스트명 검증](#호스트명-검증)
- [클라이언트 인증과 주체](#클라이언트-인증과-주체)
- [인증서를 만드는 흐름](#인증서를-만드는-흐름)
- [브로커·클라이언트 설정](#브로커클라이언트-설정)
- [만료 전 갱신](#만료-전-갱신)
- [고려사항](#고려사항)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **리스너에 TLS를 걸 때 무엇을 만들어 어디에 놓아야 하고, 무엇이 위험한가.**

## TLS 핸드셰이크가 하는 일

- **리스너의 보안 프로토콜이 `SSL`이나 `SASL_SSL`로 설정되면 그 리스너의 연결에 TLS가 보안
  전송 계층으로 쓰인다.** **TLS로 연결이 맺어질 때 핸드셰이크 과정이 인증을 수행하고, 암호
  매개변수를 협상하고, 암호화를 위한 공유 키를 만든다** (11장, p.270).[^shapira2021]
- 검증의 방향은 비대칭이 기본이다 — **서버의 디지털 인증서를 클라이언트가 검증해 서버의
  신원을 세우고**, **SSL을 쓴 클라이언트 인증이 켜져 있으면 서버도 클라이언트의 디지털
  인증서를 검증해 클라이언트의 신원을 세운다.** **SSL로 가는 모든 트래픽은 암호화되므로
  안전하지 않은 네트워크에 쓰기 적합**하다 (11장, p.270).[^shapira2021]

## 성능 대가

- 책이 박스로 못박은 수치 (11장, p.270):[^shapira2021]

  > SSL channels are encrypted and hence introduce a noticeable overhead in terms of CPU
  > usage. Zero-copy transfer is currently not supported for SSL. Depending on the traffic
  > pattern, the overhead may be up to 20–30%.

  - 제로카피가 왜 걸리는지는 [카프카 요청 처리](../concepts/kafka-request-processing.md)에
    있고, 이 대가 때문에 배포 위치를 바꾸는 실제 판단은
    [미러메이커](../concepts/kafka-mirrormaker.md)의 프로덕션 배포 절에 있다.

## 키스토어와 트러스트스토어

- 역할이 갈린다 — **브로커 리스너에 `SSL`이나 `SASL_SSL`로 TLS가 켜지면, 브로커에는 브로커의
  개인 키와 인증서를 담은 키스토어(key store)를, 클라이언트에는 브로커 인증서 또는 브로커
  인증서에 서명한 인증 기관(certificate authority, CA)의 인증서를 담은
  트러스트스토어(trust store)를 설정**해야 한다 (11장, p.270).[^shapira2021]
- **브로커 인증서에는 클라이언트가 서버 호스트명을 검증할 수 있도록 브로커 호스트명이 주체
  대체 이름(Subject Alternative Name, SAN) 확장이나 공통 이름(Common Name, CN)으로 들어
  있어야** 한다. **와일드카드 인증서를 쓰면 한 도메인의 모든 브로커가 같은 키스토어를 쓸 수
  있어 관리가 단순해진다** (11장, p.270).[^shapira2021]
- 잘 알려진 기관이 서명했다면 트러스트스토어를 아예 뺄 수 있다 — **잘 알려진 신뢰받는 기관이
  서명한 인증서를 쓸 때는 브로커에서도 클라이언트에서도 트러스트스토어 설정을 생략할 수 있고,
  자바 설치본의 기본 트러스트스토어로 신뢰를 세우기에 충분**하다 (11장,
  p.274).[^shapira2021]

## 호스트명 검증

- **카프카 클라이언트는 기본적으로 서버 인증서에 저장된 서버 호스트명이 클라이언트가 접속하는
  호스트와 일치하는지 검증**한다. **그 연결 호스트명은 클라이언트에 설정된 부트스트랩 서버일
  수도, 브로커가 메타데이터 응답으로 돌려준 광고된 리스너(advertised listener) 호스트명일
  수도** 있다 (11장, p.271).[^shapira2021]
- **호스트명 검증은 중간자 공격(man-in-the-middle attack)을 막는 서버 인증의 핵심 부분이므로
  프로덕션 시스템에서 꺼서는 안 된다** (11장, p.271).[^shapira2021]

## 클라이언트 인증과 주체

- **브로커는 `ssl.client.auth=required`를 설정해 `SSL`을 보안 프로토콜로 쓰는 리스너로 들어오는
  클라이언트를 인증하도록 설정**할 수 있다. 이때 **클라이언트에는 키스토어를, 브로커에는
  클라이언트 인증서나 그 인증서에 서명한 CA의 인증서를 담은 트러스트스토어를 설정**한다
  (11장, p.271).[^shapira2021]
  - **브로커 간 통신에 SSL을 쓴다면 브로커 트러스트스토어는 브로커 인증서의 CA와 클라이언트
    인증서의 CA를 둘 다 담아야** 한다 (11장, p.271).[^shapira2021]
- 기본 주체가 인증서에서 나온다 — **기본적으로 클라이언트 인증서의 식별 이름(distinguished
  name, DN)이 인가와 쿼터에 쓰이는 `KafkaPrincipal`이 되며**, **`ssl.principal.mapping.rules`로
  주체를 커스터마이즈할 규칙 목록을 줄 수** 있다 (11장, p.271).[^shapira2021] 예제에서
  `CN=Metrics App,O=Confluent,C=GB` 인증서로 인증하는 클라이언트는 기본적으로
  `User:CN=Metrics App,O=Confluent,C=GB`를 주체로 쓴다 (11장, p.272).[^shapira2021]
- **`SASL_SSL`을 쓰는 리스너는 TLS 클라이언트 인증을 끄고 SASL 인증과 SASL이 세운
  `KafkaPrincipal`에 의존**한다 (11장, p.271).[^shapira2021]
- 중간값이 하나 더 있다 — **`ssl.client.auth=requested`로 SSL 클라이언트 인증을 선택 사항으로
  만들 수 있는데, 이 경우 키스토어가 설정되지 않은 클라이언트도 TLS 핸드셰이크를 완료하지만
  `User:ANONYMOUS` 주체를 할당받는다** (11장, p.271).[^shapira2021]

## 인증서를 만드는 흐름

- 책은 **자체 서명 CA로 서버·클라이언트 인증용 키스토어와 트러스트스토어를 만드는 예**를
  보인다. 흐름은 브로커 쪽과 클라이언트 쪽이 대칭이며, 자바의 `keytool` 하나로 끝난다 (11장,
  pp.271–273):[^shapira2021]
  - **브로커용 자체 서명 CA 키 쌍을 만들어 PKCS12 파일 `server.ca.p12`에 넣고**
    (`keytool -genkeypair`), **CA의 공개 인증서를 `server.ca.crt`로 내보낸다**
    (`keytool -export`) — 이것이 트러스트스토어와 인증서 체인에 들어간다.
  - **브로커의 개인 키를 만들어 `server.ks.p12`에 넣고**(`keytool -genkey`), **인증서 서명
    요청을 만들고**(`keytool -certreq`), **CA 키스토어로 브로커 인증서에 서명한 뒤**
    (`keytool -gencert`, 여기서 `-ext SAN=DNS:broker1.example.com`이 붙는다), **인증서 체인을
    브로커 키스토어로 들여온다**(`keytool -importcert`).
  - **와일드카드 호스트명을 쓰면 모든 브로커가 같은 키스토어를 쓸 수 있고, 아니면 브로커마다
    자기 정규화된 도메인 이름(FQDN)으로 키스토어를 만든다.**
  - **브로커 간 통신에 TLS를 쓴다면 브로커들이 서로를 인증하도록 브로커 CA 인증서로 브로커용
    트러스트스토어를 만들고**(`keytool -import`), **클라이언트용 트러스트스토어도 같은 브로커
    CA 인증서로 만든다.**
  - **TLS 클라이언트 인증을 켰다면 클라이언트용 자체 서명 CA를 따로 만들어 클라이언트
    키스토어를 만들고, 그 클라이언트 CA를 브로커 트러스트스토어에 추가**해 브로커가 클라이언트
    진정성을 검증할 수 있게 한다. **브로커의 트러스트스토어는 모든 클라이언트의 CA를 담아야**
    한다.

## 브로커·클라이언트 설정

- 키스토어와 트러스트스토어가 준비되면 브로커 설정은 아래가 전부다. **브로커에
  트러스트스토어가 필요한 것은 브로커 간 통신에 TLS를 쓰거나 클라이언트 인증을 켰을 때
  뿐**이다 (11장, p.273):[^shapira2021]

  ```properties
  ssl.keystore.location=/path/to/server.ks.p12
  ssl.keystore.password=server-ks-password
  ssl.key.password=server-ks-password
  ssl.keystore.type=PKCS12
  ssl.truststore.location=/path/to/server.ts.p12
  ssl.truststore.password=server-ts-password
  ssl.truststore.type=PKCS12
  ssl.client.auth=required
  ```

- 클라이언트 쪽은 대칭이다 — **클라이언트에는 만들어 둔 트러스트스토어를 설정하고, 클라이언트
  인증이 필요하면 키스토어도 설정**한다. 키 이름은 브로커와 같은
  `ssl.truststore.location`·`ssl.truststore.password`·`ssl.truststore.type`과
  `ssl.keystore.location`·`ssl.keystore.password`·`ssl.key.password`·`ssl.keystore.type`이다
  (11장, p.273).[^shapira2021]

## 만료 전 갱신

- **인증서가 만료되기 전에 키스토어와 트러스트스토어를 주기적으로 갱신해야 TLS 핸드셰이크
  실패를 피할 수** 있다 (11장, p.274).[^shapira2021]
- 브로커는 재시작 없이 갱신할 수 있다 — **브로커의 SSL 스토어는 같은 파일을 수정하거나 설정
  옵션을 새 버전 파일로 바꾸는 두 방법으로 동적으로 갱신 가능하고, 어느 쪽이든 어드민 API나
  카프카 configs 툴로 갱신을 촉발**한다 (11장, p.274).[^shapira2021] 브로커 id 0의 외부
  리스너 키스토어를 바꾸는 명령은
  `bin/kafka-configs.sh --bootstrap-server localhost:9092 --command-config admin.props
  --entity-type brokers --entity-name 0 --alter --add-config
  'listener.name.external.ssl.keystore.location=/path/to/server.ks.p12'` 꼴이다 (11장,
  p.274).[^shapira2021] 동적 설정 갱신이 어떤 리소스 유형에 걸리는지는
  [설정 관리](../concepts/kafka-config-administration.md)에 있다.

## 고려사항

- 프로토콜과 암호 스위트 (11장, p.274):[^shapira2021]
  - **카프카는 기본적으로 더 새로운 프로토콜인 TLSv1.2와 TLSv1.3만 활성화**한다 —
    **TLSv1.1 같은 옛 프로토콜에 알려진 취약점이 있기 때문**이다.
  - **안전하지 않은 재협상 문제 때문에 카프카는 TLS 연결의 재협상(renegotiation)을 지원하지
    않는다.**
  - **호스트명 검증은 중간자 공격을 막기 위해 기본으로 켜져 있다.**
  - **암호 스위트를 제한해 보안을 더 조일 수** 있다 — **최소 256비트 암호화 키 크기의 강한
    암호가 암호학적 공격을 막고 안전하지 않은 네트워크로 데이터를 나를 때 데이터 무결성을
    보장**한다. **FIPS 140-2 같은 보안 표준을 준수하기 위해 TLS 프로토콜과 암호를 제한하도록
    요구하는 조직도** 있다.
- 키 관리 (11장, p.274):[^shapira2021]
  - **개인 키를 담은 키스토어는 기본적으로 파일시스템에 저장되므로, 파일시스템 권한으로
    키스토어 파일 접근을 제한하는 것이 필수적**이다.
  - **개인 키가 침해되면 표준 자바 TLS 기능으로 인증서 폐기를 켤 수 있고, 이 경우 수명이 짧은
    키를 써서 노출을 줄일 수** 있다.
- 가용성 (11장, p.274):[^shapira2021]
  - **TLS 핸드셰이크는 비싸고 브로커의 네트워크 스레드 시간을 상당히 잡아먹는다.** 그래서
    **안전하지 않은 네트워크에서 TLS를 쓰는 리스너는 브로커의 가용성을 지키기 위해 연결
    쿼터와 제한으로 서비스 거부 공격에 대비**해야 한다.
  - **브로커 설정 `connection.failed.authentication.delay.ms`로 인증 실패 시 응답을 늦춰
    클라이언트가 인증 실패를 재시도하는 속도를 낮출 수** 있다.
  - 네트워크 스레드가 무엇을 하는 자원인지는
    [카프카 요청 처리](../concepts/kafka-request-processing.md)에 있다.

## 이어지는 페이지

- [카프카 보안 프로토콜](../concepts/kafka-security-protocols.md) — `SSL`·`SASL_SSL`이
  무엇의 조합인지
- [카프카 SASL 인증](../concepts/kafka-sasl-authentication.md) — `SASL_SSL`에서 인증을 맡는
  나머지 절반
- [카프카 암호화](../concepts/kafka-encryption.md) — TLS가 덮지 못하는 저장 데이터와 종단 간
- [카프카 요청 처리](../concepts/kafka-request-processing.md) — 제로카피와 네트워크 스레드
- [설정 관리](../concepts/kafka-config-administration.md) — 동적 설정 갱신의 일반 절차
- [미러메이커](../concepts/kafka-mirrormaker.md) — SSL 성능 대가가 배포 위치 판단으로
  나타나는 곳

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka" — 인용 블록은 p.270 "SSL
    Performance" 박스 원문. 코드 펜스는 p.273 브로커 설정 예제 전문. `keytool` 절은 원문
    pp.271–273의 명령 다섯 묶음을 산문으로 옮기고 명령 이름만 인라인으로 남긴 것이며,
    `kafka-configs.sh` 예제는 p.274 원문에서 줄 연결 백슬래시만 덜어냈다(보탠 줄 없음)

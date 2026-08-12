---
type: concept
title: 카프카 위임 토큰
description: 키스토어나 케르베로스 키탭을 워커마다 배포하지 않고 인증을 나눠 주는 기제 — 토큰 식별자와 HMAC이라는 공유 비밀의 구성, SASL/SCRAM 위에 얹혀 사용자 이름·비밀번호 자리를 차지하는 인증 방식, 토큰을 만들 수 있는 자격의 제한, 모든 브로커가 공유하는 마스터 키와 그것을 바꿀 때 치르는 대가
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 위임 토큰

- [무엇을 대신하는가](#무엇을-대신하는가)
- [토큰의 구성과 인증 경로](#토큰의-구성과-인증-경로)
- [토큰을 만들고 갱신하기](#토큰을-만들고-갱신하기)
- [브로커·클라이언트 설정](#브로커클라이언트-설정)
- [고려사항](#고려사항)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **자격 증명 파일을 나눠 주지 않고 여러 워커가 인증하게 하려면 무엇을 쓰는가.**

## 무엇을 대신하는가

- **위임 토큰(delegation token)은 카프카 브로커와 클라이언트 사이의 공유 비밀로, 클라이언트
  애플리케이션에 SSL 키스토어나 케르베로스 키탭을 배포할 필요가 없는 경량 설정 기제**다
  (11장, p.285).[^shapira2021]
- 부수 효과가 하나 더 있다 — **위임 토큰은 케르베로스 키 배포 센터(Key Distribution Center,
  KDC) 같은 인증 서버의 부하를 줄이는 데도 쓸 수** 있다 (11장, p.285).[^shapira2021]
- 전형적인 쓰임은 프레임워크의 워커다 — **카프카 커넥트 같은 프레임워크가 워커의 보안 설정을
  단순화하는 데 위임 토큰을 쓸 수** 있고, **브로커에 이미 인증한 클라이언트가 같은 사용자
  주체에 대한 위임 토큰을 만들어 워커들에 나눠 주면 그 워커들이 브로커에 직접 인증**할 수 있다
  (11장, p.285).[^shapira2021] 워커가 무엇인지는
  [카프카 커넥트](../concepts/kafka-connect.md)에 있다.

## 토큰의 구성과 인증 경로

- **위임 토큰 하나는 토큰 식별자(token identifier)와 공유 비밀로 쓰이는 해시 기반 메시지 인증
  코드(hash-based message authentication code, HMAC)로 이뤄진다** (11장,
  p.285).[^shapira2021]
- 새 인증 메커니즘이 아니라 기존 것에 올라탄다 — **위임 토큰을 쓴 클라이언트 인증은
  SASL/SCRAM으로 수행되며, 토큰 식별자가 사용자 이름 자리에, HMAC이 비밀번호 자리에 들어간다**
  (11장, p.285).[^shapira2021] SCRAM 자체는
  [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md)에 있다.

## 토큰을 만들고 갱신하기

- **위임 토큰은 카프카 어드민 API나 `delegation-tokens` 명령으로 만들거나 갱신**할 수 있다
  (11장, p.285).[^shapira2021] 어드민 API 쪽은
  [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md)에 있다.
- 만들 수 있는 자격에 제한이 걸린다 (11장, p.285):[^shapira2021]
  - **`User:Alice` 주체에 대한 위임 토큰을 만들려면 클라이언트가 위임 토큰이 아닌 다른 인증
    프로토콜로 앨리스의 자격 증명을 써서 인증돼 있어야** 한다.
  - **위임 토큰으로 인증한 클라이언트는 다른 위임 토큰을 만들 수 없다.**
- 명령의 형태는 `bin/kafka-delegation-tokens.sh --bootstrap-server localhost:9092
  --command-config admin.props --create --max-life-time-period -1 --renewer-principal
  User:Bob`으로 만들고 `--renew --renew-time-period -1 --hmac c2VjcmV0`으로 갱신하는 것이다.
  **앨리스가 생성 명령을 돌리면 만들어진 토큰으로 앨리스를 사칭할 수 있으며 그 토큰의 소유자는
  `User:Alice`**이고, 예제는 **`User:Bob`을 토큰 갱신자로 설정**한다. **갱신 명령은 토큰
  소유자(앨리스)나 토큰 갱신자(밥)가 돌릴 수** 있다 (11장, p.285).[^shapira2021]

## 브로커·클라이언트 설정

- 모든 브로커가 같은 열쇠를 가져야 한다 — **위임 토큰을 만들고 검증하려면 모든 브로커가
  `delegation.token.master.key` 옵션으로 같은 마스터 키를 갖도록 설정**돼야 한다 (11장,
  p.286).[^shapira2021]
  - 그 키를 바꾸는 대가가 크다 — **이 키는 모든 브로커를 재시작해야만 교체할 수** 있고,
    **기존 토큰은 더 이상 쓸 수 없으므로 마스터 키를 갱신하기 전에 전부 삭제**해야 하며,
    **새 토큰은 모든 브로커에서 키가 갱신된 뒤에 만들어야** 한다 (11장,
    p.286).[^shapira2021]
- **위임 토큰을 쓴 인증을 지원하려면 브로커에 SASL/SCRAM 메커니즘 중 적어도 하나가 켜져 있어야**
  한다 (11장, p.286).[^shapira2021]
- 클라이언트는 SCRAM 설정을 그대로 쓰되 `tokenauth`가 붙는다. **사용자 이름 자리에 토큰
  식별자를, 비밀번호 자리에 토큰 HMAC을** 넣으며, **이 설정으로 맺어진 연결의 `KafkaPrincipal`은
  토큰에 연결된 원래 주체(예: `User:Alice`)** 다 (11장, p.286):[^shapira2021]

  ```properties
  sasl.mechanism=SCRAM-SHA-512
  sasl.jaas.config=org.apache.kafka.common.security.scram.ScramLoginModule \
      required tokenauth="true" username="MTIz" password="c2VjcmV0";
  ```

## 고려사항

- (11장, p.286):[^shapira2021]
  - **내장 SCRAM 구현과 마찬가지로 위임 토큰은 주키퍼가 안전한 배포에서만 프로덕션에
    적합**하며, **SCRAM에서 말한 모든 보안 고려사항이 위임 토큰에도 그대로 적용**된다.
    - 버전 조건: Kafka 3.9 이하 — 주키퍼 부분에 한한다.
      [주키퍼 보안](../concepts/kafka-zookeeper-security.md) 참조.
  - **브로커가 토큰 생성에 쓰는 마스터 키는 암호화하거나 안전한 비밀번호 저장소로 외부화해
    보호**해야 한다.
  - **수명이 짧은 위임 토큰으로 토큰이 침해됐을 때의 노출을 제한**할 수 있다.
  - **만료된 토큰으로 연결이 계속 도는 것을 막고 토큰 삭제 이후 기존 연결이 계속 동작할 수
    있는 시간을 제한하려면 브로커에 재인증을 켤 수** 있다.

## 이어지는 페이지

- [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md) — 위임 토큰이 올라타는 SCRAM과
  그것이 요구하는 것들
- [카프카 재인증](../concepts/kafka-reauthentication.md) — 토큰이 만료·삭제된 뒤의 연결
- [카프카 커넥트](../concepts/kafka-connect.md) — 위임 토큰이 설정을 단순화한다는 그 워커들
- [카프카 어드민 클라이언트](../concepts/kafka-adminclient.md) — 토큰 생성·갱신의 다른 통로
- [카프카 플랫폼 보안](../concepts/kafka-platform-security.md) — 마스터 키를 밖으로 빼는 쪽

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "Delegation tokens" 절
    (pp.285–286) — 코드 펜스는 p.286 클라이언트 설정 예제이며 원문의 주석 번호 표식만
    덜어냈다(보탠 줄 없음)

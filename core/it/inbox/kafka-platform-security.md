---
type: concept
title: 카프카 플랫폼 보안
description: 카프카와 주키퍼를 잠근 뒤에도 남는 것들 — 시스템 전체를 대상으로 삼는 위협 모델과 내부자 위협, 자격 증명 파일을 지키는 파일시스템 권한, 설정 파일의 평문 비밀번호를 밖으로 빼는 설정 제공자, 그리고 커스텀 제공자 없이 브로커의 민감한 설정을 암호화해 두는 방법
status: draft
generated: { by: "claude-opus-5", at: "2026-08-12T21:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 카프카 플랫폼 보안

- [위협 모델](#위협-모델)
- [파일과 네트워크](#파일과-네트워크)
- [비밀번호 보호](#비밀번호-보호)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **카프카와 주키퍼를 잠근 뒤에도 남는 것은 무엇이고 무엇으로 막는가.**

## 위협 모델

- **프로덕션 시스템의 보안 설계는 개별 컴포넌트뿐 아니라 시스템 전체에 대한 보안 위협을 다루는
  위협 모델(threat model)을 써야** 한다 (11장, p.301).[^shapira2021] 같은 원칙의 출발점은
  [카프카 보안 모델](../concepts/kafka-security-model.md)에 있다.
- 위협 모델이 하는 일 — **시스템의 추상을 세우고 잠재적 위협과 연관된 위험을 식별**한다.
  **위협이 평가·문서화되고 위험에 따라 우선순위가 매겨지면, 시스템 전체가 보호되도록 잠재적
  위협마다 완화 전략이 구현**돼야 한다 (11장, p.301).[^shapira2021]
- 놓치기 쉬운 축 — **잠재적 위협을 평가할 때 외부 위협뿐 아니라 내부자 위협(insider threat)도
  고려하는 것이 중요**하다 (11장, p.301).[^shapira2021]
- **개인 식별 정보(PII)나 다른 민감한 데이터를 저장하는 시스템은 규제 정책을 준수하기 위한
  추가 조치도 구현**해야 한다. 다만 **표준 위협 모델링 기법의 심층 논의는 이 장의 범위
  밖**이라고 책은 못박는다 (11장, p.301).[^shapira2021]

## 파일과 네트워크

- **안전한 인증·인가·암호화로 카프카의 데이터와 주키퍼의 메타데이터를 보호하는 데 더해, 플랫폼이
  안전하도록 추가 조치를 취해야** 한다 (11장, p.301).[^shapira2021]
- 책이 드는 방어 (11장, p.301):[^shapira2021]
  - **네트워크를 보호하는 네트워크 방화벽 솔루션과 물리 저장소를 보호하는 암호화.**
  - **인증에 쓰이는 자격 증명을 담은 키스토어·트러스트스토어·케르베로스 키탭 파일은 파일시스템
    권한으로 보호**돼야 한다.
  - **자격 증명 같은 보안상 결정적인 정보를 담은 설정 파일에 대한 접근이 제한**돼야 한다.
  - **설정 파일에 평문으로 저장된 비밀번호는 접근이 제한돼 있어도 안전하지 않으므로, 카프카는
    비밀번호를 안전한 저장소로 외부화하는 것을 지원**한다.

## 비밀번호 보호

- **카프카 브로커와 클라이언트에 커스터마이즈 가능한 설정 제공자(config provider)를 설정해
  안전한 서드파티 비밀번호 저장소에서 비밀번호를 가져올 수** 있고, **복호화를 수행하는 커스텀
  설정 제공자를 쓰면 비밀번호를 설정 파일에 암호화된 형태로 저장할 수도** 있다 (11장,
  p.301).[^shapira2021]
- 책의 예제는 **`gpg` 도구로 파일에 저장된 브로커·클라이언트 프로퍼티를 복호화하는
  `ConfigProvider` 구현**이다. **복호화에 쓸 패스프레이즈를 환경 변수 `PASSPHRASE`로 프로세스에
  주고**, **`gpg`로 설정을 복호화해 자바 프로퍼티로 파싱**하며, **오류가 나면
  `RuntimeException`으로 빠르게 실패**한다. **호출자가 경로에서 키의 부분집합을 요청할 수도
  있어, 예제는 전체 값을 얻은 뒤 요청된 부분집합을 돌려준다** (11장,
  pp.301–302).[^shapira2021]
- 앞서 SASL/PLAIN 절에서 외부 파일로 뺐던 자격 증명 파일을
  `gpg --symmetric --output credentials.props.gpg --passphrase "$PASSPHRASE" credentials.props`로
  암호화한 뒤, **원래 프로퍼티 파일에 간접 설정과 설정 제공자 옵션을 더해 카프카 클라이언트가
  암호화된 파일에서 자격 증명을 읽게** 한다 (11장, p.303):[^shapira2021]

  ```properties
  username=${gpg:/path/to/credentials.props.gpg:username}
  password=${gpg:/path/to/credentials.props.gpg:password}
  config.providers=gpg
  config.providers.gpg.class=com.example.GpgProvider
  ```

  - 이 간접 참조가 원래 무엇을 대체하는지는
    [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md)의 SASL/PLAIN 절에 있다.
- 커스텀 제공자 없이 되는 길도 있다 — **민감한 브로커 설정 옵션은 커스텀 제공자를 쓰지 않고
  카프카 configs 툴로 주키퍼에 암호화해 저장할 수** 있다. **브로커를 시작하기 전에 브로커의
  SSL 키스토어 비밀번호를 암호화해 주키퍼에 저장**하는 식이며, **그 값을 복호화하려면 비밀번호
  인코더 비밀(`password.encoder.secret`)이 각 브로커의 설정 파일에 설정돼 있어야** 한다 (11장,
  p.303).[^shapira2021] 명령은 `bin/kafka-configs.sh --zookeeper localhost:2181 --alter
  --entity-type brokers --entity-name 0 --add-config
  'listener.name.external.ssl.keystore.password=server-ks-password,password.encoder.secret=encoder-secret'`
  꼴이다.
  - 버전 조건: Kafka 3.9 이하 — 저장 위치가 주키퍼라는 서술에 한한다.
    [주키퍼와 KRaft](../concepts/zookeeper-and-kraft.md) 참조.

## 이어지는 페이지

- [카프카 보안 모델](../concepts/kafka-security-model.md) — 시스템 전체를 대상으로 삼는다는
  같은 원칙의 출발점
- [카프카 SASL 메커니즘](../concepts/kafka-sasl-mechanisms.md) — 평문 비밀번호가 원래 놓이는
  JAAS 설정
- [카프카 TLS 설정](../concepts/kafka-tls-configuration.md) — 파일시스템 권한으로 지켜야 하는
  키스토어
- [카프카 위임 토큰](../concepts/kafka-delegation-tokens.md) — 외부화 대상이 되는 마스터 키
- [주키퍼 보안](../concepts/kafka-zookeeper-security.md) — 암호화된 설정이 저장되는 곳
- [설정 관리](../concepts/kafka-config-administration.md) — configs 툴이 하는 설정 변경의
  일반 형태

[^shapira2021]: Shapira et al. 2021, 11장 "Securing Kafka", "Securing the Platform" 절과
    "Password Protection" 절(pp.301–303) — 코드 펜스는 p.303 간접 설정 예제 전문. 자바
    `GpgProvider` 예제(p.302)는 옮기지 않고 산문으로만 요약했고, `gpg`·`kafka-configs.sh`
    명령은 원문에서 줄 연결 백슬래시만 덜어냈다(보탠 줄 없음)

---
type: concept
title: 단일 메시지 변환(SMT)
description: 커넥트가 레코드를 복사하는 도중 코드 없이 바꾸는 무상태 변환 — 상태 있는 스트림 처리와 갈리는 경계, 아파치 카프카에 들어 있는 열한 가지 SMT, 레코드 헤더로 계보를 남기는 예, 그리고 손상 메시지를 보내는 데드 레터 큐
generated: { by: "claude-opus-5", at: "2026-08-12T18:00:00Z" }
sources:
  - { id: shapira2021, resource: /it/sources/shapira2021.md }
---

# 단일 메시지 변환(SMT)

- [무상태와 상태 있음의 경계](#무상태와-상태-있음의-경계)
- [아파치 카프카에 들어 있는 SMT](#아파치-카프카에-들어-있는-smt)
- [예 — 레코드 헤더로 계보를 남긴다](#예--레코드-헤더로-계보를-남긴다)
- [오류 처리와 데드 레터 큐](#오류-처리와-데드-레터-큐)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **커넥트가 레코드를 복사하는 도중 어디까지 바꿀 수 있고, 어디부터는 다른
도구의 일인가.**

## 무상태와 상태 있음의 경계

- **MySQL에서 카프카로, 거기서 엘라스틱서치로 레코드를 복사하는 것만으로도 꽤 쓸모 있지만
  ETL 파이프라인은 보통 변환 단계를 포함한다.** **카프카 생태계에서는 변환을 무상태
  (stateless)인 단일 메시지 변환(single message transformation, SMT)과 상태를 가질 수 있는
  스트림 처리로 나눈다** (9장, p.223).[^shapira2021]
- **SMT는 카프카 커넥트 안에서 메시지가 복사되는 동안 그 메시지를 변환하며, 흔히 코드를
  전혀 쓰지 않고 할 수 있다.** **조인이나 집계를 수반하는 더 복잡한 변환은 상태 있는 카프카
  스트림즈 프레임워크를 요구**한다 (9장, p.223).[^shapira2021]
  - 카프카 스트림즈는 이 책의 뒤쪽 장(14장 "Stream Processing")에서 다루며 이 KB에는 아직
    들어와 있지 않다 — **미해소**.
- 파이프라인 설계에서 이 경계가 왜 중요한지는
  [데이터 파이프라인 설계 고려사항](../concepts/kafka-data-pipeline-considerations.md)의
  변환 절에 있다 — 파이프라인 안에서 너무 많이 바꾸면 하류의 손을 묶는다.

## 아파치 카프카에 들어 있는 SMT

- **아파치 카프카는 다음 SMT들을 포함**한다 (9장, pp.223–224):[^shapira2021]
  - `Cast` — **필드의 데이터 타입을 바꾼다.**
  - `MaskField` — **필드의 내용을 널로 대체한다.** **민감하거나 개인 식별이 가능한 데이터를
    제거하는 데 유용**하다.
  - `Filter` — **특정 조건에 매치되는 모든 메시지를 버리거나 포함한다.** **내장 조건에는
    토픽 이름 매치, 특정 헤더, 그리고 메시지가 툼스톤(tombstone)인지(즉 널 값을 갖는지)가
    포함**된다.
  - `Flatten` — **중첩된 데이터 구조를 평평한 것으로 변환한다.** **특정 값까지의 경로에
    있는 모든 필드 이름을 연결해서 수행**한다.
  - `HeaderFrom` — **메시지의 필드를 헤더로 옮기거나 복사한다.**
  - `InsertHeader` — **각 메시지의 헤더에 정적 문자열을 추가한다.**
  - `InsertField` — **메시지에 새 필드를 추가한다.** **오프셋 같은 메타데이터의 값을 쓰거나
    정적 값을 쓴다.**
  - `RegexRouter` — **정규식과 대체 문자열로 목적지 토픽을 바꾼다.**
  - `ReplaceField` — **메시지의 필드를 제거하거나 이름을 바꾼다.**
  - `TimestampConverter` — **필드의 시간 형식을 수정한다** — 예컨대 **유닉스 에포크에서
    문자열로**.
  - `TimestampRouter` — **메시지 타임스탬프에 기반해 토픽을 수정한다.** **주로 싱크
    커넥터에서 유용하다** — **타임스탬프에 기반해 메시지를 특정 테이블 파티션으로 복사하고
    싶고, 토픽 필드가 목적지 시스템에서 동등한 데이터셋을 찾는 데 쓰일 때**다.
- **그에 더해 주 아파치 카프카 코드베이스 밖의 기여자들로부터도 변환이 제공**된다.
  **GitHub(Lenses.io·Aiven·Jeremy Custenborder가 쓸 만한 모음을 갖고 있다)이나 Confluent
  Hub에서 찾을 수 있다** (9장, p.224).[^shapira2021]
- 더 배울 곳도 책이 지목한다 — **"Twelve Days of SMT" 블로그 시리즈에서 많은 변환의 상세
  예제를 읽을 수 있고, 튜토리얼과 딥다이브를 따라 자기 변환을 쓰는 법을 배울 수 있다**
  (9장, p.224).[^shapira2021]

## 예 — 레코드 헤더로 계보를 남긴다

- 책이 든 예의 목적 — **앞서 만든 MySQL 커넥터가 생산하는 각 레코드에 레코드 헤더를
  추가하려 한다. 헤더는 그 레코드가 이 MySQL 커넥터에 의해 만들어졌음을 나타내며, 감사자가
  이 레코드들의 계보(lineage)를 조사하려는 경우에 유용**하다 (9장, p.224).[^shapira2021]
  파이프라인에 계보를 심는 것이 왜 권장되는지는
  [데이터 파이프라인 설계 고려사항](../concepts/kafka-data-pipeline-considerations.md)의
  변환·보안 절에 있다.
- 하는 일은 커넥터 설정에 네 줄을 더하는 것이 전부다. **`transforms`로 변환 이름을 붙이고
  나머지 키에 그 이름을 접두어로 써서 클래스·헤더 이름·리터럴 값을 준다** — `transforms`·
  `transforms.<이름>.type`·`.header`·`.value.literal`로 찾는다 (9장,
  pp.224–225):[^shapira2021]

  ```json
  "transforms": "InsertHeader",
  "transforms.InsertHeader.type": "org.apache.kafka.connect.transforms.InsertHeader",
  "transforms.InsertHeader.header": "MessageSource",
  "transforms.InsertHeader.value.literal": "mysql-login-connector"
  ```

- 결과 — **MySQL 테이블에 레코드를 몇 개 더 삽입하면 `mysql.login` 토픽의 새 메시지들이
  헤더를 갖는 것을 볼 수 있다.** **옛 레코드는 `NO_HEADERS`를 보여 주고 새 레코드는
  `MessageSource:mysql-login-connector`를 보여 준다** (9장, pp.224–225).[^shapira2021]
  - 버전 조건: Kafka 2.7 이상 — **콘솔 컨슈머에서 헤더를 출력하려면 아파치 카프카 2.7
    이상이 필요하다**(`--property print.headers=true`) (9장, p.224).[^shapira2021]

## 오류 처리와 데드 레터 큐

- **변환은 한 커넥터에 특정되지 않고 어떤 커넥터의 설정에도 쓸 수 있는 커넥터 설정의
  예**다. **어떤 싱크 커넥터에서도 쓸 수 있는 또 다른 매우 유용한 커넥터 설정이
  `error.tolerance`** 이며, **어떤 커넥터든 손상된 메시지를 조용히 버리거나 "데드 레터
  큐(dead letter queue)"라 불리는 특별한 토픽으로 라우팅하도록 설정**할 수 있다. 상세는
  **"Kafka Connect Deep Dive—Error Handling and Dead Letter Queues" 블로그 포스트**에
  있다 (9장, p.225, "Error Handling and Dead Letter Queues" 박스).[^shapira2021]
  - 웨어하우스 백룸에서 같은 선택을 하는 자리가
    [ETL 34 서브시스템](../concepts/etl-subsystems.md)의 품질 스크린(4)이다 — 거기서는
    실패 시 중단·격리(suspense)·태깅 중 하나를 고르며 **태깅 후 통과**를 최선으로 본다.
    - #hypothesis 커넥트의 `error.tolerance`가 주는 두 선택지는 그 셋 중 버리기와
      **격리**(데드 레터 큐)에 대응하고, 태깅에 해당하는 것은 없다.

## 이어지는 페이지

- [카프카 커넥트](../concepts/kafka-connect.md) — 이 설정들이 얹히는 커넥터와 워커
- [카프카 커넥트 내부 구조](../concepts/kafka-connect-internals.md) — SMT가 손대는 그
  데이터 모델
- [데이터 파이프라인 설계 고려사항](../concepts/kafka-data-pipeline-considerations.md) —
  파이프라인 안 변환의 범위를 어디까지 둘지의 판단
- [프로듀서 전송 경로](../concepts/kafka-producer-send-path.md) — 여기서 쓰는 레코드 헤더가
  클라이언트 쪽에서 사는 곳
- [ETL 34 서브시스템](../concepts/etl-subsystems.md) — 나쁜 레코드 처리의 웨어하우스 쪽 선택지

[^shapira2021]: Shapira et al. 2021, 9장 "Building Data Pipelines", pp.223–225. 코드 펜스는 pp.224–225 예제 원문에서 변환 관련 네 줄만 남기고 나머지 커넥터 설정 키와 `echo`·`curl` 감싸개를 덜어냈다(보탠 줄 없음)

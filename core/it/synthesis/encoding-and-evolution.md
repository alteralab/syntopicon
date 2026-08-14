---
type: synthesis
title: 인코딩과 진화
description: 데이터를 바이트로 바꾸는 형식들과 그 형식이 버전을 넘어 살아남는 방법을 모으는 허브 — 두 방향의 호환성, 텍스트와 스키마 기반 이진 형식, 그리고 데이터베이스·서비스·워크플로·메시지라는 네 가지 데이터플로
generated: { by: "claude-opus-5", at: "2026-08-14T23:00:00Z" }
---

# 인코딩과 진화

인메모리 객체를 바이트로 바꾸는 일은 형식 선택처럼 보이지만 실은 배포 방식의 문제다. 옛 코드와
새 코드가 함께 도는 동안 무엇이 깨지지 않아야 하는가가 형식을 고른다. 첫 절이 그 요구를 정의하고,
둘째 절이 그 요구를 지고 가는 형식들을, 셋째 절이 그 형식이 실제로 흐르는 자리들을 맡는다.

## 요구

- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — 두 방향의 정의,
  롤링 업그레이드, 알 수 없는 필드를 잃는 사고, 인코딩과 디코딩이라는 낱말

## 형식

- [데이터 인코딩 형식](../concepts/data-encoding-formats.md) — 언어 내장 직렬화의 결함,
  JSON·XML·CSV의 문제, JSON Schema, 이진 JSON 변형, 스키마가 주는 네 가지 성질
- [프로토콜 버퍼와 필드 태그](../concepts/protocol-buffers-encoding.md) — 필드 번호가 정하는
  진화 규칙과 태그를 영원히 재사용할 수 없다는 제약
- [Avro의 기록자 스키마와 독자 스키마](../concepts/avro-writer-and-reader-schema.md) — 태그 없이
  이름으로 맞추는 스키마 해소, 기본값 규칙, 동적 생성 스키마
- [카프카 직렬화와 스키마 레지스트리](../concepts/kafka-serialization-and-schema-registry.md) —
  스키마를 레코드에서 떼어 내 버전으로 관리하는 실물

## 데이터플로

- [데이터베이스를 거치는 데이터플로](../concepts/dataflow-through-databases.md) — 데이터가 코드보다
  오래 살고 마이그레이션이 미뤄지는 자리
- [웹 서비스와 REST](../concepts/web-services-and-rest.md) — 서비스 API의 정의·IDL·프레임워크와
  API 버저닝
- [원격 프로시저 호출의 문제](../concepts/remote-procedure-call-problems.md) — 위치 투명성이
  실패하는 여섯 지점
- [서비스 디스커버리와 로드 밸런싱](../concepts/service-discovery-and-load-balancing.md) —
  주소를 찾고 부하를 나누는 다섯 가지 해법
- [내구 실행과 워크플로](../concepts/durable-execution-and-workflows.md) — 서비스 여럿에 걸친
  단계를 정확히 한 번 굴리려는 시도와 그 대가
- [발행/구독 메시징](../concepts/publish-subscribe-messaging.md) — 브로커를 사이에 두는 비동기
  흐름과 큐·토픽 두 패턴
- [분산 액터 프레임워크](../concepts/distributed-actor-frameworks.md) — 브로커와 프로그래밍 모델을
  한 프레임워크로 합친 쪽

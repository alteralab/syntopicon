---
type: synthesis
title: 스트림 처리
description: 끝나지 않는 이벤트 스트림을 연속적으로 처리하는 쪽 진입점 — 패러다임의 정의, 시간과 상태와 이중성이라는 세 개념, 애플리케이션의 조립 패턴, 그리고 카프카 스트림즈의 API와 아키텍처
generated: { by: "human:me", at: "2026-08-12T22:00:00Z" }
---

# 스트림 처리

**끝나지 않는 데이터를 다루는 쪽이다.** 카프카가 이벤트를 나르고 보관하는 방식은
[카프카](kafka-basics.md) 아래 허브들이 담당하고, 코드를 고칠 수 없는 외부 저장소를
잇는 무상태 복사는 [카프카 커넥트와 데이터 파이프라인](kafka-connect-and-pipelines.md)이
담당한다. 여기는 그다음 — **조인과 집계처럼 상태가 필요한 처리**가 사는 자리다.

읽는 순서가 있다. 먼저 **무엇을 스트림 처리라 부르는지**를 정하고, 그 위에서 시간·상태·
이중성이라는 개념 셋을 익힌 뒤, 그것들이 조립되는 패턴과 실제 라이브러리로 내려간다.

## 무엇을 스트림 처리라 부르는가

- [스트림 처리 패러다임](../concepts/stream-processing-paradigm.md) — 무한한 데이터셋이라는 이벤트 스트림의 정의와 세 속성, 요청-응답·배치와 갈리는 자리, 그리고 어디에 쓰는가

## 개념 셋

- [스트림 처리의 시간 의미론](../concepts/stream-processing-time-semantics.md) — 이벤트 시간·로그 추가 시간·처리 시간의 구분과 출력 타임스탬프 배정 규칙
- [스트림 처리의 시간 윈도우](../concepts/stream-processing-time-windows.md) — 윈도우 크기·진행 간격·갱신 허용 기간과 텀블링·호핑·세션 윈도우
- [스트림 처리의 상태](../concepts/stream-processing-state.md) — 로컬 상태와 외부 상태의 맞교환, 체인지로그로 상태를 다시 만드는 기제, 대화형 질의
- [스트림-테이블 이중성과 조인](../concepts/stream-table-duality.md) — 스트림과 테이블을 오가는 두 방향과 그 위에 서는 조인 세 종류

## 어떻게 조립하는가

- [스트림 처리 설계 패턴](../concepts/stream-processing-design-patterns.md) — 단일 이벤트 처리, 로컬 상태 처리, 다단계 리파티셔닝, 비순차 이벤트, 재처리

## 카프카 스트림즈

- [카프카 스트림즈 DSL](../concepts/kafka-streams-dsl.md) — `StreamsBuilder`로 토폴로지를 정의하는 법과 책의 세 예제
- [카프카 스트림즈 아키텍처](../concepts/kafka-streams-architecture.md) — 토폴로지가 태스크로 쪼개져 도는 방식과 장애 복구 시간

## 무엇을 쓸지 고를 때

- [스트림 처리 프레임워크 고르기](../concepts/choosing-a-stream-processing-framework.md) — 애플리케이션 유형 넷과 유형 무관 고려사항 넷

## 경계에 있는 페이지

- [단일 메시지 변환(SMT)](../concepts/kafka-single-message-transformations.md) — 무상태 변환이 끝나고 스트림 처리가 시작하는 선
- [카프카 트랜잭션](../concepts/kafka-transactions.md) — 정확히 한 번 보장의 기제 쪽
- [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md) — 1장이 이 축을 처음 예고한 자리

## 웨어하우스 쪽에서 같은 소재를 다루는 곳

- [증분 처리와 그 대가](../concepts/incremental-processing-tradeoffs.md) — 전체 재계산과 스트림 사이의 중간 지대
- [지각 도착 데이터](../concepts/late-arriving-data.md) — 비순차 이벤트를 ETL 쪽에서 본 것
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 스트림을 구체화한다는 말의 일반형
- [데이터 레이크](../concepts/data-lake.md) — 배치 대 스트림의 대비가 분석 쪽에 놓인 자리

## 이어지는 허브

- [카프카](kafka-basics.md) — 이 허브의 상위
- [카프카 클라이언트](kafka-clients.md) — 스트림즈가 안에서 쓰는 프로듀서·컨슈머
- [카프카 신뢰성과 정확히 한 번](kafka-reliability.md) — `processing.guarantee`가 기대는 보장
- [카프카 커넥트와 데이터 파이프라인](kafka-connect-and-pipelines.md) — 적재 문제의 더 단순한 답
- [DW 운영과 프로세스](dw-operations-and-process.md) — 배치 쪽 진입점

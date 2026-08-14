---
type: synthesis
title: 데이터플로 아키텍처
description: 여러 저장 시스템을 이벤트 로그로 이어 하나의 데이터베이스처럼 굴리는 쪽 진입점 — 통합의 문제 설정, 데이터베이스 기능의 해체와 그 위의 애플리케이션 설계, 쓰기 경로와 읽기 경로라는 관점, 그리고 원자적 커밋 없이 정확성을 얻는 방법들
generated: { by: "claude-opus-5", at: "2026-08-15T09:00:00Z" }
---

# 데이터플로 아키텍처

**하나의 도구로 안 되는 자리다.** 무한한 입력을 처리하는 기제 자체는
[스트림 처리](stream-processing.md)가, 유한한 입력은 [배치 처리](batch-processing.md)가
담당한다. 여기는 그 위 — **여러 시스템을 이어 붙였을 때 데이터를 무엇으로 맞춰 두고, 그
묶음에서 어떻게 정확성을 얻는가**가 사는 자리다.

읽는 순서가 있다. 먼저 **왜 이어 붙여야 하는지**를 정하고, 그 통합을 데이터베이스 기능의
해체로 다시 본 뒤, 그 위에서 애플리케이션과 읽기·쓰기를 어떻게 배치할지로 내려가고, 마지막에
그 구성이 정확한지를 묻는다.

## 왜 이어 붙이는가

- [데이터 통합](../concepts/data-integration.md) — 하나의 도구로 모든 용법을 감당할 수 없을 때 무엇을 먼저 정해야 하는가, 그리고 분산 트랜잭션과 갈리는 자리
- [전체 순서의 한계](../concepts/limits-of-total-ordering.md) — 모든 이벤트에 한 줄의 순서를 매기는 전략이 규모에서 깨지는 네 자리와 인과성 문제
- [재처리와 점진적 마이그레이션](../concepts/reprocessing-and-gradual-migration.md) — 옛 표현과 새 표현을 나란히 두고 사용자를 조금씩 옮기는 방식
- [람다 아키텍처와 카파 아키텍처](../concepts/lambda-and-kappa-architecture.md) — 배치와 스트림을 한 시스템에서 돌리려는 두 제안

## 데이터베이스를 해체한다

- [언번들드 데이터베이스](../concepts/unbundling-databases.md) — 조직 전체의 데이터플로를 하나의 거대한 데이터베이스로 보는 시각, 페더레이션과 언번들링
- [데이터플로 중심 애플리케이션 설계](../concepts/dataflow-application-design.md) — 파생 함수로서의 애플리케이션 코드와 동기 요청 대신 스트림 조인

## 파생 상태를 어디서 관찰하는가

- [쓰기 경로와 읽기 경로](../concepts/write-path-and-read-path.md) — 캐시·색인·구체화 뷰의 역할이 경계를 옮기는 것뿐이라는 정리, 그리고 그 경계를 사용자 기기까지 미는 것
- [읽기도 이벤트다](../concepts/reads-as-events.md) — 요청 서빙이 실은 조인이라는 대응과 여러 샤드에 걸친 질의

## 정확성

- [종단 간 논증](../concepts/end-to-end-argument.md) — 강한 보장이 구해 주지 않는 것과 요청 ID를 관통시키는 해법
- [데이터플로에서 제약 강제하기](../concepts/enforcing-constraints-in-dataflow.md) — 유일성 제약을 로그 샤딩으로 얻는 방법과 원자적 커밋 없는 다중 샤드 송금
- [타임리니스와 무결성](../concepts/timeliness-and-integrity.md) — "일관성"이 뭉뚱그린 두 요구를 가르기
- [느슨하게 해석된 제약](../concepts/loosely-interpreted-constraints.md) — 어기고 나서 사과로 수습하는 업무 패턴
- [감사와 무결성 검사](../concepts/auditing-and-integrity-checking.md) — 손상됐다는 것을 어떻게 알아내는가

## 경계에 있는 페이지

- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 이 아키텍처가 전제하는 구분
- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 가변 상태와 불변 로그가 같은 동전의 두 면인 이유
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이 발상을 데이터 모델로 민 것
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 기존 데이터베이스를 이 그림에 넣는 기제
- [조정 회피](../concepts/coordination-avoidance.md) — 조율 없이 무결성만 지키는 계열
- [마이크로서비스와 서버리스](../concepts/microservices-and-serverless.md) — 같은 분업을 동기 요청으로 하는 쪽
- [싱크 엔진과 로컬 우선 소프트웨어](../concepts/sync-engines-and-local-first.md) — 쓰기 경로를 기기까지 민 결과

## 이어지는 허브

- [스트림 처리](stream-processing.md) — 이 아키텍처가 올라타는 처리 계열
- [배치 처리](batch-processing.md) — 재처리를 담당하는 쪽
- [데이터베이스 트랜잭션](database-transactions.md) — 여기서 피하려는 그 보장의 본가
- [분산 합의](distributed-consensus.md) — 유일성 제약이 결국 요구하는 것
- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 무엇을 정본으로 삼을 것인가라는 상위 선택

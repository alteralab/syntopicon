---
type: guide
title: "IT 지식"
description: "서적·논문·기술 문서에서 축적한 IT 개념"
generated: { by: "tools/kb-new", at: "2026-08-05T02:09:19Z" }
---

# IT 지식

서적·논문·기술 문서에서 축적한 IT 개념

## Hubs

<!-- 허브(synthesis) 링크 + 한 줄 설명, 10–30개. 포인터만 — 본문 발췌·수치 복제
     금지(진입점 부패 벡터, PLAN §3). 갱신 후보는 kb-lint의 링크 차수 대조가 낸다. -->

- [데이터 웨어하우스 모델링](synthesis/data-warehouse-modeling.md) — DW 축의 부모 허브
  - [차원 모델링 기법](synthesis/dimensional-modeling-techniques.md) — Kimball 기초·기법 카탈로그
  - [Data Vault](synthesis/data-vault.md) — 모델링·아키텍처·적재
  - [DW 운영과 프로세스](synthesis/dw-operations-and-process.md) — 라이프사이클·ETL·데이터 관리
- [카프카](synthesis/kafka-basics.md) — 스트리밍 축의 부모 허브
  - [카프카 내부 구조](synthesis/kafka-internals.md) — 메타데이터·복제·요청 처리·물리 저장
  - [카프카 클라이언트](synthesis/kafka-clients.md) — 프로듀서·컨슈머 설정, 파티션 배분, 오프셋 커밋
  - [카프카 설치와 운영](synthesis/kafka-operations.md) — 설정 기준·클러스터 산정·튜닝
  - [카프카 신뢰성과 정확히 한 번](synthesis/kafka-reliability.md) — 보장의 경계·언클린 리더 선출·멱등적 프로듀서·트랜잭션
  - [카프카 커넥트와 데이터 파이프라인](synthesis/kafka-connect-and-pipelines.md) — 파이프라인 설계 고려사항·커넥트 구조와 설정·복사 도중 변환
  - [카프카 보안](synthesis/kafka-security.md) — 인증·인가·암호화·감사·주키퍼와 플랫폼
  - [카프카 모니터링](synthesis/kafka-monitoring.md) — 지표와 SLO·브로커와 JVM·클라이언트 지표·랙
  - [스트림 처리](synthesis/stream-processing.md) — 패러다임의 정의·시간과 상태와 이중성·설계 패턴·카프카 스트림즈
- [배치 처리](synthesis/batch-processing.md) — 유한한 입력을 통째로 읽어 출력을 다시 만드는 쪽: 저장·오케스트레이션·연산 세 계층과 그 쓰임새
- [데이터 시스템 아키텍처 트레이드오프](synthesis/data-systems-architecture-tradeoffs.md) — 운영/분석·클라우드·분산 선택 축의 허브
- [비기능 요건](synthesis/nonfunctional-requirements.md) — 성능·신뢰성·확장성·유지보수성을 정의하는 어휘
- [데이터 모델과 질의 언어](synthesis/data-models-and-query-languages.md) — 관계형·문서·그래프·이벤트·데이터프레임과 그 질의 언어들
- [저장 엔진](synthesis/storage-engines.md) — 디스크에 데이터를 놓는 구조, B-트리 대 LSM의 대비, 분석용 열 저장과 색인들
- [인코딩과 진화](synthesis/encoding-and-evolution.md) — 데이터를 바이트로 바꾸는 형식과 버전을 넘어 살아남는 방법
- [분산 시스템 기초](synthesis/distributed-systems-basics.md) — 통신·시간·장애의 가정과 그 위의 실패 감지·리더 선출
- [분산 합의](synthesis/distributed-consensus.md) — 서버 여럿을 하나처럼 굴게 만드는 문제와 Raft의 해법
- [데이터 복제](synthesis/data-replication.md) — 리더 하나·여럿·없음의 세 갈래와 각각이 낳는 문제
- [레플리카 일관성](synthesis/replica-consistency.md) — 사본이 여럿일 때의 가시성 계약과 수렴 장치
- [데이터 샤딩](synthesis/data-sharding.md) — 데이터셋을 노드로 쪼개는 기준·쏠림·라우팅·색인
- [데이터베이스 트랜잭션](synthesis/database-transactions.md) — ACID·격리 수준·직렬성 구현·분산 원자적 커밋
- [자바 기술 시스템](synthesis/java-technology-system.md) — JVM 축의 부모 허브: 구성과 제품군·판올림의 역사·가상 머신 구현들·지금의 방향
  - [JVM 자동 메모리 관리](synthesis/jvm-memory-management.md) — 메모리 영역·객체 생존 판정·회수 알고리즘·컬렉터 선택
  - [JVM 모니터링과 문제 해결 도구](synthesis/jvm-troubleshooting-tools.md) — 명령 줄 도구·JHSDB·GUI 도구·JFR과 JMC·JIT 코드 검사


## Tools

- 검색: `qmd query <질의> -c it` / 형태소 레그 `tools/ksearch`
- 저장: `/kb-ingest --kb it` — inbox/ 경유
- 점검: `tools/lint --kb it`

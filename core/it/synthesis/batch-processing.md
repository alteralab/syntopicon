---
type: synthesis
title: 배치 처리
description: 유한한 입력을 통째로 읽어 출력을 처음부터 다시 만드는 쪽 진입점 — 무엇을 배치라 부르는지의 정의, 저장·오케스트레이션·연산이라는 세 계층, MapReduce에서 데이터플로 엔진으로 간 처리 모델, 그리고 ETL·분석·ML이라는 쓰임새
generated: { by: "claude-opus-5", at: "2026-08-15T02:00:00Z" }
---

# 배치 처리

**입력이 유한한 쪽이다.** 끝나지 않는 입력을 다루는 쪽은
[스트림 처리](stream-processing.md)가 담당하고, 웨어하우스의 백룸 절차로서의 같은 소재는
[DW 운영과 프로세스](dw-operations-and-process.md)가 담당한다. 여기는 그 사이 —
**입력을 읽기 전용으로 두고 출력을 매번 처음부터 만드는 계산**이 사는 자리다.

읽는 순서가 있다. 먼저 **무엇을 배치라 부르는지**를 정하고, 단일 기계 예제로 직관을 세운 뒤,
분산 운영체제 비유를 따라 저장·오케스트레이션·연산 세 계층으로 내려가고, 마지막으로 쓰임새를 본다.

## 무엇을 배치 처리라 부르는가

- [배치 처리의 기본](../concepts/batch-processing-basics.md) — 온라인과 오프라인의 구분, 불변
  입력이 주는 네 가지와 그 대가, MapReduce에서 지금까지의 지형
- [Unix 도구로 하는 배치 처리](../concepts/batch-processing-with-unix-tools.md) — 파이프라인
  한 줄이 분산 배치의 축소판인 이유와 정렬 대 인메모리 집계
- [함수형 데이터 엔지니어링](../concepts/functional-data-engineering.md) — 배치를 순수 함수의
  규율로 짜자는 제안. 결정적이고 멱등한 순수 태스크, 원자 단위가 되는 불변 파티션, 재현
  가능성이라는 요구, 그리고 저자가 스스로 그 규칙을 깨는 한 자리

## 저장 계층

- [분산 파일시스템](../concepts/distributed-filesystems.md) — 블록·데이터 노드·메타데이터
  서비스·프로토콜, 그리고 공유 없음 원칙
- [오브젝트 스토어](../concepts/object-stores.md) — 버킷과 키, 불변 객체, 없는 디렉터리, 저장과
  연산의 분리

## 오케스트레이션 계층

- [분산 잡 오케스트레이션](../concepts/distributed-job-orchestration.md) — 실행기·자원 관리자·
  스케줄러와 자원 배분이 NP-난해인 자리, 선점과 스팟 인스턴스
- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) — 잡의 의존 그래프를 다루는 층과
  내구 실행 쪽 "워크플로"와의 구분

## 연산 계층

- [MapReduce](../concepts/mapreduce.md) — 매퍼와 리듀서 두 콜백, 그 계보와 한계
- [데이터플로 엔진](../concepts/dataflow-engines.md) — 워크플로 전체를 한 잡으로 다루는 Spark·Flink
- [셔플](../concepts/shuffle-algorithm.md) — 입력과 출력이 모두 샤딩된 분산 정렬
- [배치 조인과 그룹핑](../concepts/batch-joins-and-grouping.md) — 셔플 위에 서는 정렬 병합 조인과
  2차 정렬
- [배치 질의 언어](../concepts/batch-query-languages.md) — SQL이 링구아 프랑카가 된 경로와 비용
  기반 최적화기

## 어디에 쓰는가

- [배치 처리의 유스케이스](../concepts/batch-use-cases.md) — ETL·레이크하우스 분석·ML과 LLM 데이터
  준비
- [배치 출력을 서빙에 되돌리기](../concepts/serving-derived-data-from-batch-jobs.md) — 파생
  데이터셋을 실서비스로 옮기는 세 갈래

## 경계에 있는 페이지

- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) — 배치 출력이
  놓이는 자리의 정의
- [데이터 레이크](../concepts/data-lake.md) — 레이크하우스와 그 아래 네 부품
- [내구 실행과 워크플로](../concepts/durable-execution-and-workflows.md) — 같은 낱말의 다른 뜻
- [클라우드 네이티브 아키텍처](../concepts/cloud-native-architecture.md) — 저장과 연산이 갈리는
  더 큰 흐름

## 이어지는 허브

- [스트림 처리](stream-processing.md) — 입력이 무한할 때 무엇이 달라지는가
- [데이터플로 아키텍처](dataflow-architecture.md) — 재처리가 시스템 진화의 기제가 되는 자리
- [DW 운영과 프로세스](dw-operations-and-process.md) — 같은 소재를 웨어하우스 절차로 본 쪽
- [저장 엔진](storage-engines.md) — 정렬과 병합이라는 같은 원리의 본가
- [데이터 시스템 아키텍처 트레이드오프](data-systems-architecture-tradeoffs.md) — 운영계와
  분석계의 갈림

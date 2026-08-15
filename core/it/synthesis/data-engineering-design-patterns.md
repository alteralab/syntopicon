---
type: synthesis
title: 데이터 엔지니어링 디자인 패턴
description: 반입에서 관측까지 프로젝트 워크플로 순서로 배열된 이름 붙은 패턴 카탈로그의 진입점 — 패턴이라는 형식 자체, 범주와 패턴의 2층 조직, 반입 패턴 일곱과 오류 관리 패턴 여섯, 그리고 이 KB의 원리 서술 위에 그 이름 층이 얹힌 자리들
generated: { by: "claude-opus-5", at: "2026-08-15T11:20:00Z" }
---

# 데이터 엔지니어링 디자인 패턴

**이름이 좁은 이유**: 여기 모인 것은 Bartosz Konieczny, *Data Engineering Design
Patterns*(O'Reilly, 2025)가 이름을 붙여 카탈로그로 정리한 층뿐이다. 이 KB에는 이미 배치·스트림·
저장·품질의 **원리 서술**이 다른 소스들(Kleppmann·Reis & Housley·Shapira·Kimball)로 쌓여 있고,
이 허브가 더하는 것은 그 위의 **이름 층**이다 — "전체 스냅샷 대 증분 추출"이라는 원리에
`Full Loader`·`Incremental Loader`라는 이름과 결과 목록이 붙는 식이다.

그래서 이 허브의 페이지 대부분은 신규가 아니라 **기존 개념 페이지에 붙은 절**이다. 아래 목록은
어느 패턴이 어느 페이지의 어느 자리로 갔는지를 가리킨다.

- [디자인 패턴의 해부](../inbox/design-pattern-anatomy.md) — 먼저 읽는다. 패턴이라는 형식이
  무엇을 약속하는가(다섯 성질), GoF 23개로 부족한 이유, 범주와 패턴의 2층 조직, 패턴 하나를
  쓰는 네 절(문제·해법·결과·예제), 그리고 모든 문제 서술이 놓이는 블로그 분석 플랫폼 사례와
  메달리온 3계층

## 이 카탈로그를 읽는 법

- **장의 순서 = 프로젝트의 시간 순서.** 저자는 데이터 반입으로 시작해 일상 모니터링으로 끝나는
  고전적 데이터 엔지니어링 프로젝트의 워크플로를 따랐다. 그 워크플로의 원리 쪽 정본은
  [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md)다.
- **범주가 먼저, 패턴이 나중.** `Compactor`·`Readiness Marker`처럼 이름만으로는 자리를 모르는
  패턴이 "데이터 컴팩션"·"데이터 준비 상태"라는 범주 아래 놓여 비로소 쓸 자리가 드러난다.
- **해법과 결과는 기술 불가지, 예제만 제품에 매인다.** 저자가 예제를 Apache Spark·Flink·
  Airflow·PostgreSQL·Delta Lake로 한정한다고 선언했다. 이 KB가 옮긴 것은 앞의 두 절이 중심이고,
  코드 펜스는 개념당 대표 하나로 아꼈다.
- **반입 패턴은 반입에만 쓰이지 않는다.** 저자 자신의 2장 마무리가 그렇게 말한다 — 여기 논한
  대부분의 패턴은 ETL·ELT 파이프라인의 추출 단계에 훌륭한 후보이므로 더 업무 지향적인 잡에서도
  쓸 수 있다.

## 데이터 반입 패턴 (2장)

여섯 범주·일곱 패턴. 이 KB에서는 원리 페이지 둘을 갱신하고 셋을 새로 세웠다.

- [배치 반입 패턴](../inbox/batch-ingestion-patterns.md) — **전체 적재**(Full Loader)와
  **증분 적재**(Incremental Loader) 두 범주. 원천에 변경 탐지 수단이 없을 때 전체 적재가
  선택되는 이유, 드롭-앤-인서트의 일관성 위험과 단일 노출 추상, 델타 컬럼 대 시간 분할이라는
  두 구현과 하드 삭제·백필이라는 두 함정
- [변경 데이터 캡처](../inbox/change-data-capture.md) — 증분 적재 범주의 둘째 패턴
  (**Change Data Capture**). 지연과 물리적 삭제라는 두 판정 조건, 그리고 복잡성·데이터 범위·
  페이로드·데이터 의미론이라는 네 대가. 마지막 것이 가장 무겁다 — 정지 데이터가 이동 데이터가
  되면서 `JOIN`의 의미가 바뀐다
- [데이터셋 복제 패턴](../inbox/dataset-replication-patterns.md) — **복제** 범주
  (**Passthrough Replicator**·**Transformation Replicator**). 적재와 복제를 가르는 두 기준,
  단순함을 규칙으로 삼는 이유, 푸시를 고르는 이유, 그리고 PII 때문에 변환을 끼울 때 생기는
  조용한 스키마 파손과 탈동기화
- [작은 파일 문제와 컴팩션](../inbox/small-files-and-compaction.md) — **데이터 컴팩션** 범주
  (**Compactor**). 나열이 처리보다 비싸지는 70/30, 테이블 형식별 구현, 키 기반 저장에서 같은
  이름이 다른 일을 하는 지점, 그리고 컴팩션만으로는 공간이 돌아오지 않는 이유
- [반입 트리거 패턴](../inbox/ingestion-triggering-patterns.md) — **데이터 준비 상태**
  (**Readiness Marker**)와 **이벤트 주도**(**External Trigger**) 두 범주. 풀과 푸시가 갈리는
  자리, 관례가 강제력을 갖지 못한다는 것, 그리고 트리거가 "그냥 핑"으로 퇴화하는 실패 양식

## 오류 관리 패턴 (3장)

다섯 범주·여섯 패턴. 저자가 장 첫머리에 세운 좌표는 **일시적 오류와 비일시적 오류**의 구분이고,
장 전체를 관통하는 함정은 **눈덩이 백필 효과**다 — 과거를 다시 여는 순간 하류 소비자 전부가 같은
일을 해야 한다.

- [데드레터와 빠져나가는 레코드](../inbox/dead-letter-and-dropped-records.md) —
  **처리 불가 레코드**(**Dead-Letter**)와 **필터링**(**Filter Interceptor**) 두 범주. 레코드가
  파이프라인에서 빠져나가는 두 경로와, 둘 다 잡을 초록불로 끝내므로 계측 없이는 보이지 않는다는 것
- [정확히 한 번 메시지 처리](../inbox/exactly-once-message-processing.md) — **중복 레코드**
  범주(**Windowed Deduplicator**). 배치의 암묵 전역 윈도와 스트리밍의 시간 윈도, 상태 저장 세
  유형, 공간 대 시간 맞교환, 그리고 정확히 한 번 처리가 정확히 한 번 전달을 보장하지 않는 이유
- [늦은 데이터 통합](../inbox/late-data-integration.md) — **늦은 데이터** 범주의 세 패턴
  (**Late Data Detector**·**Static Late Data Integrator**·**Dynamic Late Data Integrator**).
  워터마크의 정의와 MIN·MAX 집계가 낳는 과거 고착·이벤트 스큐, 고정 룩백 윈도와 겹치는 백필,
  상태 테이블과 동시 실행 문제
- [스트림 처리의 결함 내성](../inbox/stream-processing-fault-tolerance.md) — **결함 내성**
  범주(**Checkpointer**). 위치와 상태를 어디에 기록하는가의 두 갈래, 지연과 보장의 맞교환,
  그리고 체크포인트를 처리 앞에 두느냐 뒤에 두느냐가 정하는 세 전달 모드

## 멱등성 패턴 (4장)

네 범주·일곱 패턴. 저자가 장 첫머리에 세운 좌표는 **오류 관리만으로는 부족하다**는 것이다 —
자동 재시도가 이미 성공한 쓰기를 재생하므로, 오류 관리가 남긴 중복을 치우는 것이 이 장의 몫이다.
일곱은 두 페이지로 갈렸다.

- [멱등적 쓰기 패턴](../inbox/idempotent-write-patterns.md) — **덮어쓰기**
  (**Fast Metadata Cleaner**·**Data Overwrite**), **갱신**(**Merger**·**Stateful Merger**),
  **불변 데이터셋**(**Proxy**) 세 범주. 메타데이터 연산이 데이터 연산보다 빠른 이유와 그 대가로
  생기는 멱등성 입도, 덮어써도 vacuum 전에는 공간이 돌아오지 않는다는 것, `MERGE`가 증분 백필
  중에 소비자에게 다른 데이터를 보이는 구멍, 그리고 그 구멍을 상태 테이블과 테이블 버전으로 막는 법
- [정확히 한 번 메시지 처리](../inbox/exactly-once-message-processing.md) — **데이터베이스**
  범주(**Keyed Idempotency**·**Transactional Writer**). 키 생성에 이벤트 시각 대신 append time을
  써야 하는 이유, 그리고 트랜잭션이 주는 멱등성이 **현재 실행 하나**로 한정된다는 저자의 명시 —
  브로커가 주는 보장과 응용 패턴의 층위가 갈리는 자리다

## 데이터 가치 패턴 (5장)

다섯 범주·열 패턴. 저자가 장 요약에서 세운 좌표는 **정보를 더하는 쪽과 줄이는 쪽**이다 — 앞의
둘(강화·장식)이 더하고, 뒤의 둘(집계·세션화)이 줄이며, 마지막(순서)은 배열을 바꾼다.

- [데이터 강화와 장식 패턴](../inbox/data-enrichment-and-decoration-patterns.md) —
  **데이터 강화**(**Static Joiner**·**Dynamic Joiner**)와 **데이터 장식**
  (**Wrapper**·**Metadata Decorator**) 두 범주. SCD가 정적 조인에 시간 조건을 들여오는 자리,
  두 스트림의 지연 차를 버퍼와 GC 워터마크로 흡수하는 값, 계산값과 원본을 가르면 도메인이 둘로
  쪼개진다는 것, 그리고 기술 맥락은 메타데이터 계층으로 숨기되 비즈니스 속성은 넣지 말라는 경계
- [배치 조인과 그룹핑](../inbox/batch-joins-and-grouping.md) — **데이터 집계** 범주
  (**Distributed Aggregator**·**Local Aggregator**)가 기존 셔플 서술 위에 얹힌 자리. 부분
  집계와 솔팅, 셔플 서비스, 그리고 셔플을 없앤 대가로 되사는 스케일링 비용
- [세션화 패턴](../inbox/sessionization-patterns.md) — **세션화** 범주
  (**Incremental Sessionizer**·**Stateful Sessionizer**). 세 저장 공간과 세 상태, 부분 세션의
  일관성 위험, 갭 기간과 상태 저장, 그리고 세션이 앞으로 의존적이라 늦은 데이터 하나가 뒤따르는 모든
  파티션의 백필을 부른다는 것
- [순서 보장 전달 패턴](../inbox/ordered-delivery-patterns.md) — **데이터 순서** 범주
  (**Bin Pack Orderer**·**FIFO Orderer**). 부분 커밋이라는 셋째 상태, 키 하나씩 든 전달 빈,
  인플라이트 요청이 순서를 깨는 방식, 그리고 FIFO가 정확히 한 번을 뜻하지 않는다는 명시

## 아직 반입하지 않은 장

재개점의 정본은 `it/archive/konieczny2025/_progress.yaml`이다. 이 허브의 목록은 그 파일의
`covered`가 자랄 때 함께 자란다.

- 6장 데이터 흐름 · 7장 데이터 보안 · 8장 데이터 저장 · 9장 데이터 품질 · 10장 데이터 관측성

## 이웃 허브

- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 카탈로그의 장 배열이 따르는
  그 워크플로의 원리 쪽
- [배치 처리](batch-processing.md) — 반입 패턴이 얹히는 배치 쪽 기제
- [스트림 처리](stream-processing.md) — CDC와 이벤트 주도 반입이 흘러 들어가는 쪽

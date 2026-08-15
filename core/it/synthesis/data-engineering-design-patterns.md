---
type: synthesis
title: 데이터 엔지니어링 디자인 패턴
description: 반입에서 관측까지 프로젝트 워크플로 순서로 배열된 이름 붙은 패턴 카탈로그의 진입점 — 패턴이라는 형식 자체, 범주와 패턴의 2층 조직, 반입·오류 관리·멱등성·데이터 값·데이터 흐름·데이터 보안·데이터 저장·데이터 품질·데이터 관측성 아홉 장의 패턴이 어느 페이지 어느 절로 갔는지의 지도, 책 부록의 패턴 요약표와 대조한 결과, 그리고 이 KB의 원리 서술 위에 그 이름 층이 얹힌 자리들
generated: { by: "claude-opus-5", at: "2026-08-15T00:20:00Z" }
---

# 데이터 엔지니어링 디자인 패턴

- [이 카탈로그를 읽는 법](#이-카탈로그를-읽는-법) — 장의 순서·2층 조직·예제의 지위
- [데이터 반입 패턴 2장](#데이터-반입-패턴-2장) — 여섯 범주·여덟 패턴
- [오류 관리 패턴 3장](#오류-관리-패턴-3장) — 다섯 범주·일곱 패턴
- [멱등성 패턴 4장](#멱등성-패턴-4장) — 네 범주·일곱 패턴
- [데이터 가치 패턴 5장](#데이터-가치-패턴-5장) — 다섯 범주·열 패턴
- [데이터 흐름 패턴 6장](#데이터-흐름-패턴-6장) — 네 범주·여덟 패턴
- [데이터 보안 패턴 7장](#데이터-보안-패턴-7장) — 네 범주·아홉 패턴
- [데이터 저장 패턴 8장](#데이터-저장-패턴-8장) — 네 범주·아홉 패턴
- [데이터 품질 패턴 9장](#데이터-품질-패턴-9장) — 세 범주·여섯 패턴
- [데이터 관측성 패턴 10장](#데이터-관측성-패턴-10장) — 세 범주·여섯 패턴
- [부록 패턴 표와 대조한 결과](#부록-패턴-표와-대조한-결과) — 지도의 완전성 점검과 부록의 결락
- [이웃 허브](#이웃-허브) — 이 이름 층이 얹히는 원리 쪽 허브들

**이름이 좁은 이유**: 여기 모인 것은 Bartosz Konieczny, *Data Engineering Design
Patterns*(O'Reilly, 2025)가 이름을 붙여 카탈로그로 정리한 층뿐이다. 이 KB에는 이미 배치·스트림·
저장·품질의 **원리 서술**이 다른 소스들(Kleppmann·Reis & Housley·Shapira·Kimball)로 쌓여 있고,
이 허브가 더하는 것은 그 위의 **이름 층**이다 — "전체 스냅샷 대 증분 추출"이라는 원리에
`Full Loader`·`Incremental Loader`라는 이름과 결과 목록이 붙는 식이다.

그래서 이 허브의 페이지 대부분은 신규가 아니라 **기존 개념 페이지에 붙은 절**이다. 아래 목록은
어느 패턴이 어느 페이지의 어느 자리로 갔는지를 가리킨다.

- [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md) — 먼저 읽는다. 패턴이라는 형식이
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
- **오래갈 부분과 낡을 부분의 경계를 저자가 그어 놓았다.** 후기의 논증(제품은 바뀌어도 데이터를
  들여오고·가치 있게 만들고·올바로 도는지 확인할 필요는 남는다)은
  [디자인 패턴의 해부](../concepts/design-pattern-anatomy.md)의 마지막 절에 있다.

## 데이터 반입 패턴 (2장)

여섯 범주·여덟 패턴. 이 KB에서는 원리 페이지 둘을 갱신하고 셋을 새로 세웠다.

- [배치 반입 패턴](../concepts/batch-ingestion-patterns.md) — **전체 적재**(Full Loader)와
  **증분 적재**(Incremental Loader) 두 범주. 원천에 변경 탐지 수단이 없을 때 전체 적재가
  선택되는 이유, 드롭-앤-인서트의 일관성 위험과 단일 노출 추상, 델타 컬럼 대 시간 분할이라는
  두 구현과 하드 삭제·백필이라는 두 함정
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 증분 적재 범주의 둘째 패턴
  (**Change Data Capture**). 지연과 물리적 삭제라는 두 판정 조건, 그리고 복잡성·데이터 범위·
  페이로드·데이터 의미론이라는 네 대가. 마지막 것이 가장 무겁다 — 정지 데이터가 이동 데이터가
  되면서 `JOIN`의 의미가 바뀐다
- [데이터셋 복제 패턴](../concepts/dataset-replication-patterns.md) — **복제** 범주
  (**Passthrough Replicator**·**Transformation Replicator**). 적재와 복제를 가르는 두 기준,
  단순함을 규칙으로 삼는 이유, 푸시를 고르는 이유, 그리고 PII 때문에 변환을 끼울 때 생기는
  조용한 스키마 파손과 탈동기화
- [작은 파일 문제와 컴팩션](../concepts/small-files-and-compaction.md) — **데이터 컴팩션** 범주
  (**Compactor**). 나열이 처리보다 비싸지는 70/30, 테이블 형식별 구현, 키 기반 저장에서 같은
  이름이 다른 일을 하는 지점, 그리고 컴팩션만으로는 공간이 돌아오지 않는 이유
- [반입 트리거 패턴](../concepts/ingestion-triggering-patterns.md) — **데이터 준비 상태**
  (**Readiness Marker**)와 **이벤트 주도**(**External Trigger**) 두 범주. 풀과 푸시가 갈리는
  자리, 관례가 강제력을 갖지 못한다는 것, 그리고 트리거가 "그냥 핑"으로 퇴화하는 실패 양식

## 오류 관리 패턴 (3장)

다섯 범주·일곱 패턴. 저자가 장 첫머리에 세운 좌표는 **일시적 오류와 비일시적 오류**의 구분이고,
장 전체를 관통하는 함정은 **눈덩이 백필 효과**다 — 과거를 다시 여는 순간 하류 소비자 전부가 같은
일을 해야 한다.

- [데드레터와 빠져나가는 레코드](../concepts/dead-letter-and-dropped-records.md) —
  **처리 불가 레코드**(**Dead-Letter**)와 **필터링**(**Filter Interceptor**) 두 범주. 레코드가
  파이프라인에서 빠져나가는 두 경로와, 둘 다 잡을 초록불로 끝내므로 계측 없이는 보이지 않는다는 것
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — **중복 레코드**
  범주(**Windowed Deduplicator**). 배치의 암묵 전역 윈도와 스트리밍의 시간 윈도, 상태 저장 세
  유형, 공간 대 시간 맞교환, 그리고 정확히 한 번 처리가 정확히 한 번 전달을 보장하지 않는 이유
- [늦은 데이터 통합](../concepts/late-data-integration.md) — **늦은 데이터** 범주의 세 패턴
  (**Late Data Detector**·**Static Late Data Integrator**·**Dynamic Late Data Integrator**).
  워터마크의 정의와 MIN·MAX 집계가 낳는 과거 고착·이벤트 스큐, 고정 룩백 윈도와 겹치는 백필,
  상태 테이블과 동시 실행 문제
- [스트림 처리의 결함 내성](../concepts/stream-processing-fault-tolerance.md) — **결함 내성**
  범주(**Checkpointer**). 위치와 상태를 어디에 기록하는가의 두 갈래, 지연과 보장의 맞교환,
  그리고 체크포인트를 처리 앞에 두느냐 뒤에 두느냐가 정하는 세 전달 모드

## 멱등성 패턴 (4장)

네 범주·일곱 패턴. 저자가 장 첫머리에 세운 좌표는 **오류 관리만으로는 부족하다**는 것이다 —
자동 재시도가 이미 성공한 쓰기를 재생하므로, 오류 관리가 남긴 중복을 치우는 것이 이 장의 몫이다.
일곱은 두 페이지로 갈렸다.

- [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md) — **덮어쓰기**
  (**Fast Metadata Cleaner**·**Data Overwrite**), **갱신**(**Merger**·**Stateful Merger**),
  **불변 데이터셋**(**Proxy**) 세 범주. 메타데이터 연산이 데이터 연산보다 빠른 이유와 그 대가로
  생기는 멱등성 입도, 덮어써도 vacuum 전에는 공간이 돌아오지 않는다는 것, `MERGE`가 증분 백필
  중에 소비자에게 다른 데이터를 보이는 구멍, 그리고 그 구멍을 상태 테이블과 테이블 버전으로 막는 법
- [정확히 한 번 메시지 처리](../concepts/exactly-once-message-processing.md) — **데이터베이스**
  범주(**Keyed Idempotency**·**Transactional Writer**). 키 생성에 이벤트 시각 대신 append time을
  써야 하는 이유, 그리고 트랜잭션이 주는 멱등성이 **현재 실행 하나**로 한정된다는 저자의 명시 —
  브로커가 주는 보장과 응용 패턴의 층위가 갈리는 자리다

## 데이터 가치 패턴 (5장)

다섯 범주·열 패턴. 저자가 장 요약에서 세운 좌표는 **정보를 더하는 쪽과 줄이는 쪽**이다 — 앞의
둘(강화·장식)이 더하고, 뒤의 둘(집계·세션화)이 줄이며, 마지막(순서)은 배열을 바꾼다.

- [데이터 강화와 장식 패턴](../concepts/data-enrichment-and-decoration-patterns.md) —
  **데이터 강화**(**Static Joiner**·**Dynamic Joiner**)와 **데이터 장식**
  (**Wrapper**·**Metadata Decorator**) 두 범주. SCD가 정적 조인에 시간 조건을 들여오는 자리,
  두 스트림의 지연 차를 버퍼와 GC 워터마크로 흡수하는 값, 계산값과 원본을 가르면 도메인이 둘로
  쪼개진다는 것, 그리고 기술 맥락은 메타데이터 계층으로 숨기되 비즈니스 속성은 넣지 말라는 경계
- [배치 조인과 그룹핑](../concepts/batch-joins-and-grouping.md) — **데이터 집계** 범주
  (**Distributed Aggregator**·**Local Aggregator**)가 기존 셔플 서술 위에 얹힌 자리. 부분
  집계와 솔팅, 셔플 서비스, 그리고 셔플을 없앤 대가로 되사는 스케일링 비용
- [세션화 패턴](../concepts/sessionization-patterns.md) — **세션화** 범주
  (**Incremental Sessionizer**·**Stateful Sessionizer**). 세 저장 공간과 세 상태, 부분 세션의
  일관성 위험, 갭 기간과 상태 저장, 그리고 세션이 앞으로 의존적이라 늦은 데이터 하나가 뒤따르는 모든
  파티션의 백필을 부른다는 것
- [순서 보장 전달 패턴](../concepts/ordered-delivery-patterns.md) — **데이터 순서** 범주
  (**Bin Pack Orderer**·**FIFO Orderer**). 부분 커밋이라는 셋째 상태, 키 하나씩 든 전달 빈,
  인플라이트 요청이 순서를 깨는 방식, 그리고 FIFO가 정확히 한 번을 뜻하지 않는다는 명시

## 데이터 흐름 패턴 (6장)

네 범주·여덟 패턴. 저자가 장 첫머리에 세운 좌표는 **두 층위**다 — 같은 패턴이 데이터
오케스트레이션 계층에도, 데이터 처리 계층에도 구현될 수 있고, 판단의 대부분은 "패턴을 쓸까"가 아니라
"어느 층위에 그릴까"다. 여덟이 한 페이지로 갔다.

- [데이터 흐름 의존 패턴](../concepts/data-flow-dependency-patterns.md) — **순서**
  (**Local Sequencer**·**Isolated Sequencer**), **팬인**(**Aligned Fan-In**·
  **Unaligned Fan-In**), **팬아웃**(**Parallel Split**·**Exclusive Choice**),
  **오케스트레이션**(**Single Runner**·**Concurrent Runner**) 네 범주. 경계를 재시작 경계로
  잡는 규칙과 그것을 반대로 미는 트랜잭션 경계, 데이터 기반·태스크 기반 의존이 정하는 결합도와
  "누가 바꿀 수 있는가", 정렬의 네 대가(인프라 스파이크·스케줄링 스큐·오버헤드·복잡성), 부분
  데이터를 완전성 표로 알리는 법, 그리고 동시성을 1로 묶는 쪽과 푸는 쪽이 갈리는 자리

## 데이터 보안 패턴 (7장)

네 범주·아홉 패턴. 저자가 장 첫머리에 세운 좌표는 **컴플라이언스·접근 통제·데이터 보호·연결**이고,
이 KB에서는 세 페이지로 갈렸다. 이 장은 원리 쪽에 이미 쌓인 프라이버시·윤리 서술(Kleppmann &
Riccomini 14장 계열)과 맞닿는 유일한 장이다 — 그쪽이 "왜 해야 하는가"를, 이쪽이 "파이프라인에서
어떻게 하는가"를 담당한다.

- [개인 데이터 제거 패턴](../concepts/personal-data-removal-patterns.md) — **데이터 제거** 범주
  (**Vertical Partitioner**·**In-Place Overwriter**). 불변 속성을 한 번만 쓰도록 행을 세로로
  쪼개어 지울 것을 줄이는 쪽과 그것이 읽기에 되사는 조인·폴리글랏 비용, 자리에서 덮어쓰는 쪽과
  트랜잭션 없는 처리 계층에서 스테이징 영역이 필수인 이유, 카프카 툼스톤이 통하는 토픽의 조건,
  그리고 덮어쓰고 나면 되돌릴 수 없다는 것
- [세밀한 접근과 자격 증명 패턴](../concepts/fine-grained-access-and-credential-patterns.md) —
  **접근 제어**(**Fine-Grained Accessor for Tables**·**Fine-Grained Accessor for
  Resources**)와 **연결**(**Secrets Pointer**·**Secretless Connector**) 두 범주. 열 수준
  권한의 세 구현과 행 접근 정책, 자원 기반과 아이덴티티 기반이 갈리는 자리, 최소 권한을 정직하게
  지키면 정책 쿼터에 부딪힌다는 산수, 그리고 비밀을 참조로 바꾸면 위험이 사라지는 것이 아니라 한
  자리로 모인다는 것
- [암호화와 익명화 패턴](../concepts/data-encryption-and-anonymization-patterns.md) —
  **데이터 보호** 범주(**Encryptor**·**Anonymizer**·**Pseudo-Anonymizer**). 정지·이동 데이터의
  두 구현과 키를 잃으면 데이터도 잃는 대칭, 익명화의 세 구현(제거·교란·합성), 가명화의 네
  구현(마스킹·토큰화·해싱·암호화), 그리고 표 두 개를 조인하는 순간 무너지는 거짓 보안감

## 데이터 저장 패턴 (8장)

네 범주·아홉 패턴. 저자가 장 첫머리에 세운 좌표는 **컴퓨트를 더하는 사후적 길과 배치를 고치는
선제적 길**이고, 장 전체를 가르는 선은 **카디널리티**다 — 파티셔닝은 저카디널리티에서만 성립하고,
고카디널리티는 버케팅·정렬이 맡는다. 아홉은 두 신규 페이지와 기존 페이지 하나로 갈렸다.

- [데이터 저장 레이아웃 패턴](../concepts/data-storage-layout-patterns.md) — **파티셔닝**
  (**Horizontal Partitioner**·**Vertical Partitioner**)과 **레코드 조직**(**Bucket**·
  **Sorter**) 두 범주. 분할 키가 잡의 실행 맥락에서 오느냐 데이터셋에서 오느냐, 100만 파티션이
  되는 산수와 저카디널리티 규칙, 마이크로배치를 늦추는 스큐와 배압 버퍼, 샤딩이 수평 분할의
  하드웨어 특수형이라는 정리, 해시 나머지로 묶어 얻는 버킷 프루닝과 셔플 제거, 그리고 사전식
  정렬이 접두사에만 유효해 Z-order가 등장하는 자리
- [읽기 경로 최적화 패턴](../concepts/read-path-optimization-patterns.md) — **읽기 성능 최적화**
  범주(**Metadata Enhancer**·**Dataset Materializer**·**Manifest**). Parquet 푸터와 커밋 로그
  통계가 파일을 열기 전에 거르는 법과 통계가 낡는 임계값, 구체화 뷰와 테이블이 자동 갱신이냐 저장
  최적화냐로 갈리는 자리, 구체화가 접근 통제를 우회시키는 구멍, 그리고 나열 API를 없앤 대가로
  기가바이트짜리 상태가 복구 경로에 생긴다는 것(SPARK-27188)
- [정규화와 비정규화](../concepts/normalization-and-denormalization.md) — **데이터 표현** 범주
  (**Normalizer**·**Denormalizer**)가 기존 정규화 서술 위에 얹힌 자리. 눈송이가 Normalizer,
  스타가 Denormalizer의 구현이라는 분류, 조인 비용의 완화책(코로케이션·브로드캐스트)과 이력을
  SCD로 넘기는 것, 원 빅 테이블과 그것이 안티패턴이 되는 조건, 그리고 멈출 지점을 정하는
  이름 짓기 시험

## 데이터 품질 패턴 (9장)

세 범주·여섯 패턴. 저자가 장 첫머리에 세운 좌표는 **신뢰**이고, 세 범주는 시간축으로 갈린다 —
나쁜 데이터를 지금 막는 강제, 스키마가 바뀔 때를 대비하는 일관성, 그리고 **오늘의 규칙이 내일도
유효한지**를 보는 관측. 여섯은 두 신규 페이지와 기존 페이지 하나로 갈렸다.

- [데이터 품질 강제 패턴](../concepts/data-quality-enforcement-patterns.md) — **품질 강제** 범주
  (**Audit-Write-Audit-Publish**·**Constraints Enforcer**). 변환 앞뒤 두 감사 단계가 각각 무엇을
  검증하는가(같은 `NULL` 검사도 의도가 다르다), 실패 말고 남은 두 결말(부분 승급·비차단 주석)과
  그것이 데드레터와 갈리는 이유, 스트리밍의 윈도 기반·스테이징 기반, 그리고 검증을 저장소에
  위임했을 때의 전부 아니면 전무 의미론과 소비자 쪽에 남는 이중 검증
- [후진 호환과 전진 호환](../concepts/backward-and-forward-compatibility.md) — **스키마 일관성** 범주
  (**Schema Compatibility Enforcer**·**Schema Migrator**)가 기존 호환성 서술 위에 얹힌 자리.
  강제의 세 모드(레지스트리·삽입 암묵·DDL 트리거), 허용 동작 목록과 전이·비전이가 갈리는 v0/v1/v2
  실물, 그리고 호환을 깨는 이름 변경·타입 변경을 유예 기간과 새 필드로 통과시키는 절차
- [품질 관측 패턴](../concepts/quality-observation-patterns.md) — **품질 관측** 범주
  (**Offline Observer**·**Online Observer**). 감사는 막고 관측은 막지 않는다는 구분, 떼어 놓은
  대가(늦게 알기·24시간치를 한 번에·샘플링 누락), 관측 구간을 먼저 고정해 관측을 멱등적으로 만드는
  법, 온라인 관측의 자리를 Parallel Split과 Local Sequencer로 고를 때의 부분 유효 데이터셋 위험,
  그리고 관측 실패가 파이프라인을 죽이지 않게 하는 `all_done`

## 데이터 관측성 패턴 (10장)

세 범주·여섯 패턴. 저자가 장 첫머리에 세운 좌표는 **품질 패턴이 남긴 공백**이다 — 감사는 자기가
돌았을 때만 참이므로, 상류 흐름이 끊겨 AWAP 잡 자체가 돌지 않은 경우를 품질 패턴은 잡지 못한다.
해법은 **탐지와 추적** 두 기둥으로 갈리고, 여섯은 두 신규 페이지로 갔다.

- [관측 탐지 패턴](../concepts/observability-detector-patterns.md) — **데이터 탐지기**
  (**Flow Interruption Detector**·**Skew Detector**)와 **시간 탐지기**(**Lag Detector**·
  **SLA Misses Detector**) 두 범주. 연속 전달과 불규칙 전달에서 점을 보느냐 창을 보느냐,
  정지 데이터에서 메타데이터·데이터·저장 세 층의 비용 사다리와 컴팩션이 만드는 거짓 양성,
  비교 창·허용 임계값·계산식 세 단계와 실패한 날이 기준이 되어 버리는 죽음의 고리, 파티션별 랙을
  최댓값으로 합칠 때와 백분위로 합칠 때, 평균이 꼬리를 숨긴다는 논증의 랙 판, 그리고 랙과 SLA가
  서로를 대신하지 못하는 두 방향의 반례
- [데이터 계보 추적 패턴](../concepts/data-lineage-tracking-patterns.md) — **데이터 계보** 범주
  (**Dataset Tracker**·**Fine-Grained Tracker**). 관리형 서비스가 자기 범위 밖에서 부분적인 뷰만
  주는 것, 자체 구현이 입출력을 뽑는 두 수준(선언하는 오케스트레이션 계층과 역으로 읽는 데이터베이스
  계층)과 추출·API·저장소·UI 네 조각, 실행 계획 나무에서 열 계보를 뽑는 법과 커스텀 매핑 함수라는
  불투명 상자, 그리고 행 수준 계보만 데이터 안에 실려 시각화 도구 바깥에 남는다는 것
- [서비스 수준 목표](../concepts/service-level-objectives.md) — SLA Misses Detector의 시간 축이
  기존 SLI·SLO·SLA 어휘 위에 얹힌 자리. 처리 시각 SLA와 이벤트 시각 SLA를 갈라야 하는 이유
- [품질 관측 패턴](../concepts/quality-observation-patterns.md) — 9장의 두 관측자가 여기서 SLA
  지표를 모으는 수단으로 다시 불린다. Skew Detector가 AWAP의 첫 감사 단계로 승격되는 자리도 같다

## 부록 패턴 표와 대조한 결과

책 부록 "Summary of Patterns"(333p–338p)가 모든 패턴을 장별 표로 요약한다 — 패턴 이름·사용처·함정
세 열. **이 허브의 지도를 그 표와 1:1로 대조한 결과, 부록의 모든 패턴이 위 페이지들 중 하나에
자리를 갖는다.** 대조에서 나온 것 셋만 남긴다.

- **부록이 빠뜨린 패턴이 하나 있다 — `Stateful Merger`.** 4장 본문은 갱신 범주에 `Merger`와
  `Stateful Merger` 둘을 두는데 부록 표에는 `Merger`만 있다. 이 KB는 본문을 따라 둘 다
  [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md)에 둔다. **패턴 목록의 정본은 부록이
  아니라 본문이다.**
- **같은 이름이 두 장에 있다 — `Vertical Partitioner`.** 7장에서는 지울 것을 줄이려 불변 속성을
  떼어 내는 프라이버시 패턴([개인 데이터 제거 패턴](../concepts/personal-data-removal-patterns.md))이고,
  8장에서는 열 단위로 행을 쪼개는 저장 레이아웃 패턴
  ([데이터 저장 레이아웃 패턴](../concepts/data-storage-layout-patterns.md))이다. 기제는 같고 목적이
  다르므로 이 KB도 두 자리에 둔다.
- **부록의 행 수와 본문의 패턴 수가 어긋나는 자리가 하나 더 있다** — 3장의
  `Static and Dynamic Late Data Integrators`는 부록에서 한 행이지만 본문에서는 두 패턴이다
  ([늦은 데이터 통합](../concepts/late-data-integration.md)). 장별 패턴 수를 셀 때 부록 행을 세면
  어긋난다.

이 소스는 여기까지가 본문 전부다 — 반입 범위와 건너뛴 자리의 정본은
`it/archive/konieczny2025/_progress.yaml`이다.

## 이웃 허브

- [데이터 엔지니어링 수명 주기](data-engineering-lifecycle.md) — 이 카탈로그의 장 배열이 따르는
  그 워크플로의 원리 쪽
- [배치 처리](batch-processing.md) — 반입 패턴이 얹히는 배치 쪽 기제
- [스트림 처리](stream-processing.md) — CDC와 이벤트 주도 반입이 흘러 들어가는 쪽
- [카프카 모니터링](kafka-monitoring.md) — 10장의 탐지 패턴이 일반화한 그 지표들(랙·SLO)이
  제품 하나의 실물로 있는 쪽

---
type: concept
title: 데이터셋 복제 패턴
description: "환경 사이로 데이터셋을 통째 옮기는 두 패턴 — 적재와 복제를 가르는 기준(동질 저장과 메타데이터 보존), 있는 그대로 베끼는 Passthrough Replicator가 단순함을 지키는 규칙과 푸시를 고르는 이유, PII 때문에 변환 계층을 끼워 넣는 Transformation Replicator, 그리고 텍스트 형식의 조용한 스키마 파손과 프라이버시 필드의 탈동기화"
generated: { by: "claude-opus-5", at: "2026-08-15T10:40:00Z" }
sources:
  - { id: konieczny2025, resource: /it/sources/konieczny2025.md }
---

# 데이터셋 복제 패턴

- [적재와 복제는 다른 낱말이다](#적재와-복제는-다른-낱말이다)
- [Passthrough Replicator — 있는 그대로](#passthrough-replicator--있는-그대로)
- [Transformation Replicator — 못 옮기는 것이 있을 때](#transformation-replicator--못-옮기는-것이-있을-때)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **프로덕션의 데이터셋을 다른 환경에 그대로 두려면 무엇을 포기해야 하는가.**

이 페이지가 다루는 "복제"는 데이터베이스 안의 리더-팔로워 복제가 아니라 **환경 사이의 데이터셋
사본**이다. 전자는 [데이터 복제](../synthesis/data-replication.md) 쪽에 있다.

## 적재와 복제는 다른 낱말이다

- 계열의 정의 — **또 하나의 데이터 반입 패턴 계열이 데이터 복제(data replication)이고, 그 주된
  목표는 데이터를 한 위치에서 다른 위치로 있는 그대로 복사하는 것이다. 그러나 그것은 완벽한
  세계에서만 그렇다. 실세계에서는 예컨대 규제 준수(regulatory compliance) 때문에 입력을
  변경해야 하는 일이 잦을 것이다** (2장, p.20).[^konieczny2025]
- 저자가 두 낱말을 명시적으로 가른다 (2장, p.20):[^konieczny2025]

  > These two concepts look similar at first glance, but there is a slight difference.
  > Replication is about moving data between the same type of storage and ideally
  > preserving all its metadata attributes, such as primary keys in a database or event
  > positions in a streaming broker. Loading is more flexible and doesn't have this
  > homogeneous environment constraint.

  - **구분 기준이 둘**이라는 데 주의 — ① 저장의 **동질성**(같은 유형끼리) ② **메타데이터 보존**.
    둘 중 하나라도 놓으면 그것은 복제가 아니라 적재다. 이 기준이 아래 "메타데이터" 결과 항에서
    실제 실패로 되돌아온다.

## Passthrough Replicator — 있는 그대로

- 언제 쓰는가 — 저자의 문제 서술이 조건을 셋으로 준다 (2장, pp.20–21):[^konieczny2025]
  개발·스테이징·프로덕션 세 환경이 있고, **참조 데이터셋 적재 프로세스가 서드파티 API를 쓰며
  멱등하지 않다(not idempotent). 이는 하루 동안 같은 API 호출에 대해 다른 결과를 반환할 수
  있다는 뜻이다. 그래서 적재 파이프라인을 개발·스테이징 환경에서 그냥 복사해 재생할 수 없다.
  프로덕션과 **같은 데이터**가 필요하다.**
  - 해법 판정도 그 조건을 그대로 되읽는다 — **멱등하지 않은 데이터 제공자에, 환경 사이의 요구된
    일관성이 더해진 것이 Passthrough Replicator 패턴을 쓸 훌륭한 이유다** (2장,
    p.21).[^konieczny2025]
- 구현이 두 층에 걸린다 (2장, p.21):[^konieczny2025]
  - **컴퓨트 구현**은 읽기와 쓰기 두 단계뿐인 EL 잡에 의존한다. **이상적으로 EL 잡은 입력에서
    파일이나 행을 있는 그대로(즉 어떤 데이터 변환도 없이) 복사한다. 그렇지 않으면 문자열을
    날짜로 타입 변환하거나 부동소수점을 반올림하는 것 같은 데이터 품질 이슈를 도입할 수 있다.**
  - **인프라 구현**은 입력·출력 위치를 설정하고 데이터 저장 제공자가 대신 레코드를 복제하게
    하는 **복제 정책(replication policy) 문서**에 기반한다.
- 결과 ① **단순하게 유지하라(keep it simple)** — 이 패턴의 결과 절은 대부분 **하지 말아야 할
  것**의 목록이다 (2장, p.21):[^konieczny2025]
  - **복제된 데이터셋의 간섭 위험을 줄이려면 가능한 가장 단순한 복제 잡, 이상적으로는
    데이터베이스에서 쓸 수 있는 데이터 복사 명령에 의존해야 한다.**
  - **JSON 같은 텍스트 형식에 데이터 처리 프레임워크를 써야 한다면 JSON I/O API에 의존하지 말고
    줄을 사전 해석 없이 있는 그대로 가져와 복사하는 더 단순한 원시 텍스트 API를 쓰라.**
  - **파일 수나 파일명까지 같기를 원한다면, 그 파라미터를 맞출 수 없는 분산 데이터 처리
    프레임워크는 피해야 한다.**
- 결과 ② **보안과 격리** — **환경 간 통신은 언제나 까다롭고 복제 잡에 버그가 있으면 오류를 내기
  쉽다. 그 시나리오에서는 대상 환경에 부정적 영향을 주어 심지어 불안정하게 만들 위험이 있다.
  프로덕션에서 그런 위험을 감수하고 싶지 않을 것이므로 풀(pull) 대신 푸시(push) 접근으로 복제를
  구현해야 한다. 이는 데이터셋을 소유한 환경이 그것을 다른 환경으로 복사하고 따라서 빈도와
  처리량으로 프로세스를 통제한다는 뜻이다** (2장, p.22).[^konieczny2025]
  - 푸시로도 남는 위험 — **클라우드 구독에서 잡을 시작했는데 그것이 데이터 처리 서브넷에서
    마지막 가용 IP 주소를 가져가는 사용 사례를 상상할 수 있다. 리플리케이터가 완료될 때까지 다른
    잡들은 돌지 못할 것이다** (2장, p.22).[^konieczny2025]
- 결과 ③ **PII 데이터** — **복제된 데이터셋이 개인 식별 정보(personally identifiable
  information, PII)나 프로덕션 환경에서 전파될 수 없는 어떤 종류의 정보든 저장한다면 다음에
  논할 Transformation Replicator 패턴을 쓰라. 예기치 않은 속성을 없애는 추가 변환 단계를
  더한다** (2장, p.22).[^konieczny2025]
- 결과 ④ **지연** — **인프라 기반 구현은 흔히 여분의 지연을 갖는다. 그것이 해법으로 받아들일
  만한지 보려면 언제나 클라우드 제공자의 서비스 수준 협약(SLA)을 확인해야 한다** (2장,
  p.22).[^konieczny2025] SLA·SLO의 어휘는
  [서비스 수준 목표](service-level-objectives.md)에 있다.
- 결과 ⑤ **메타데이터** — 위 [적재와 복제는 다른 낱말이다](#적재와-복제는-다른-낱말이다)의
  두 번째 기준이 여기서 실패로 나타난다 (2장, p.22):[^konieczny2025]

  > Do not ignore the metadata part because it could make the replicated dataset unusable.
  > For example, replicating only the Apache Parquet files of a Delta Lake table will not
  > be enough. The same applies to Apache Kafka, where you should care not only about the
  > key and values but also about headers and the order of events within the partition.

  - 이 절이 이 페이지에서 유일하게 코드가 필요한 자리다. 저자의 Kafka 예제는 **평범한 EL
    잡이었을 것에 정렬 함수 하나가 끼어들어야 하는 이유**를 보여 준다 — 파티션 안의 순서를
    입력과 같게 유지하려면 오프셋으로 정렬하고, 메타데이터를 지키려면 헤더를 포함시켜야 한다
    (2장, p.23):[^konieczny2025]

    ```python
    events_to_replicate = (input_data_stream
      .selectExpr('key', 'value', 'partition', 'headers', 'offset'))

    def write_sorted_events(events: DataFrame, batch_number: int):
      (events.sortWithinPartitions('offset', ascending=True).drop('offset').write
        .format('kafka').option('kafka.bootstrap.servers', 'localhost:9094')
        .option('topic', 'events-replicated').option('includeHeaders', 'true').save())

    write_data_stream = (events_to_replicate.writeStream
      .option('checkpointLocation', f'{get_base_dir()}/checkpoint-kafka-replicator')
      .foreachBatch(write_sorted_events))
    ```

  - 파일 쪽 구현은 이보다 훨씬 짧아서, 원시 텍스트 API로 읽고 쓰는 두 줄이면 된다. 다만 저자가
    단서를 붙인다 — **스니펫은 파일을 보존하지 않는다. 둘 다 같은 데이터를 저장하더라도 원천과
    목적지의 파일 수는 다를 수 있다** (2장, p.22).[^konieczny2025]
  - 인프라 기반 구현으로는 Kafka 토픽에 MirrorMaker를, 파일에 클라우드 제공자의 복제 기제(예:
    Terraform으로 선언한 `aws_s3_bucket_replication_configuration`)를 쓴다 (2장,
    p.23).[^konieczny2025] MirrorMaker의 실물은
    [카프카 미러메이커](../concepts/kafka-mirrormaker.md)에 있다.

## Transformation Replicator — 못 옮기는 것이 있을 때

- 문제는 테스트 데이터의 진위다 — **새 버전의 데이터 처리 잡을 릴리스하기 전에 실제 데이터로
  테스트하고 싶다. 데이터 제공자가 흔히 데이터 품질 이슈를 갖고 있고 어떤 도구로도 그것을
  시뮬레이션하는 것이 불가능하므로 합성 데이터 생성기를 쓸 수 없다** (2장,
  p.24).[^konieczny2025] 그런데 **복제된 데이터셋이 프로덕션 환경 밖에서는 접근 불가한 PII
  데이터를 담고 있어서 단순한 Passthrough Replicator 잡을 쓸 수 없다.**
  - 저자가 이 딜레마를 한 문장으로 요약한다 — **데이터 시스템 테스트의 큰 문제 하나는… 데이터
    자체다. 데이터 제공자가 일관된 스키마와 값을 보장할 수 없다면 프로덕션 데이터를 쓰는 것은
    피할 수 없다** (2장, p.24).[^konieczny2025]
- 해법은 구조적으로 단순하다 — **Passthrough Replicator 패턴의 고전적 읽기·쓰기 부분에 더해
  그 사이에 변환 계층을 갖는다** (2장, p.24).[^konieczny2025] 변환은 스택에 따라 둘 중 하나로
  구현된다: **Apache Spark나 Apache Flink 같은 데이터 처리 프레임워크를 쓴다면 커스텀 매핑
  함수, 처리 로직을 SQL로 쉽게 표현할 수 있다면 SQL `SELECT` 문** (2장, p.24).[^konieczny2025]
  - 그 변환이 하는 일은 둘 중 하나다 — **복제되지 않아야 할 속성을 (예컨대 Anonymizer 패턴으로)
    대체하거나, 처리에 필요 없다면 그냥 제거하는 것** (2장, p.24).[^konieczny2025]
- 결과 ① **텍스트 파일 형식의 변환 위험** — 저자가 든 사고가 구체적이다 (2장,
  p.25):[^konieczny2025] 복제된 데이터셋에 스키마를 정의했는데 **날짜시간 형식이 데이터 처리
  프레임워크가 쓰는 표준과 다르다는 것을 알아채지 못했다. 그 결과 복제된 데이터셋은 모든
  타임스탬프 컬럼을 담지 못하고, 그 때문에 스테이징 잡이 실패한다.** 빠르게 고칠 수는 있지만
  릴리스 프로세스에 불필요한 작업을 만든다.
  - 완화책이 앞 패턴의 원칙을 그대로 가져온다 — **그래서 여기에도 "단순하게 유지하라" 접근을
    적용해야 한다. 예에서라면 타임스탬프 컬럼을 있는 그대로 정의하는 대신 그냥 문자열로 설정하고
    어떤 조용한 변환도 걱정하지 않으면 된다** (2장, p.25).[^konieczny2025]
- 결과 ② **탈동기화(desynchronization)** — 이것이 이 패턴 고유의 위험이다 (2장,
  p.25):[^konieczny2025]

  > Data is continuously evolving, and nothing guarantees that the privacy fields you have
  > today will still be valid in the future. Maybe new ones will appear or attributes that
  > are not currently considered PII will be reclassified as PII.

  - 완화책은 코드가 아니라 거버넌스다 — **가능하다면 데이터 카탈로그나 민감 필드가 태그된 데이터
    컨트랙트 같은 데이터 거버넌스 도구에 의존해야 한다. 그런 도구가 있으면 변환 로직을 자동화할
    수 있고, 없으면 규칙을 스스로 구현해야 한다** (2장, p.25).[^konieczny2025]
    데이터 카탈로그·컨트랙트 쪽은 [메타데이터 관리](metadata-management.md)에 있다.
- 구현은 두 접근으로 갈린다 (2장, pp.25–26):[^konieczny2025]
  - **데이터 축소(data reduction)** — 불필요한 필드를 제거한다. Databricks·BigQuery 같은 일부
    데이터베이스·컴퓨트 계층은 `SELECT * EXCEPT (ip, latitude, longitude)` 형태의 `EXCEPT`
    연산자를 지원하고, 데이터 처리 프레임워크라면 PySpark의 `drop` 함수를 쓴다.
  - **접근 통제** — 데이터 제공자가 허용된 컬럼의 부분집합만 노출한다. AWS Redshift라면
    `GRANT SELECT (visit_id, event_time, user_id) ON TABLE visits TO user_a`. **`EXCEPT` 기반
    해법보다 장황하지만 비공개 속성 접근에 보호 계층을 하나 더 얹는다** (2장,
    p.26).[^konieczny2025]
  - 행을 지울 수 없을 때 — **행 제거가 언제나 선택지는 아니다. 특히 테스트되는 데이터 처리 잡에
    그 행이 중요하다면. 그런 사용 사례에서는 민감 필드를 변경하는 컬럼 기반
    변환(column-based transformation)을 정의한다** (2장, p.26).[^konieczny2025] 컬럼 기반
    변환은 컬럼을 겨냥한 연산에는 잘 맞지만, **행 수준에서 작동해야 하거나 수정 규칙이 복잡하면
    매핑 함수가 필요할 수 있다** (2장, p.26).[^konieczny2025]

## 이어지는 페이지

- [배치 반입 패턴](../concepts/batch-ingestion-patterns.md) — 같은 장의 앞 계열. Passthrough Replicator의
  EL 잡이 Full Loader의 그것과 같은 형태인 이유
- [데이터 복제](../synthesis/data-replication.md) — 같은 낱말을 데이터베이스 안에서 쓰는 쪽
- [카프카 미러메이커](../concepts/kafka-mirrormaker.md) — 인프라 기반 복제의 실물
- [메타데이터 관리](metadata-management.md) — 탈동기화 완화책이 기대는 카탈로그·컨트랙트
- [서비스 수준 목표](service-level-objectives.md) — 인프라 복제의 지연을 재는 자
- [데이터 엔지니어링 디자인 패턴](../synthesis/data-engineering-design-patterns.md) — 이 두
  패턴이 속한 카탈로그

[^konieczny2025]: Konieczny 2025, 2장 "Data Ingestion Design Patterns" — "Replication"(pp.20–26).
코드 펜스는 예제 2-15(순서 의미론을 지키는 Passthrough Replicator)를 조판 줄바꿈만 정돈해 옮긴
것이다.

---
type: concept
title: 기록 시스템과 파생 데이터
description: 어떤 데이터가 정본이고 어떤 것이 다시 만들 수 있는 사본인가 — 도구가 아니라 용법이 정하는 구분, 갱신·삭제가 여기서 어려워지는 이유, 그리고 이 구분을 데이터 모델로 밀어붙였을 때 나오는 비정규화와 이벤트 소싱
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
  - { id: dbtlabs2026-materialization, resource: /it/sources/dbtlabs2026-materialization.md }
---

# 기록 시스템과 파생 데이터

- [두 정의](#두-정의)
- [왜 이 구분이 쓸모 있나](#왜-이-구분이-쓸모-있나)
- [도구가 아니라 용법이 정한다](#도구가-아니라-용법이-정한다)
- [갱신이 어려운 지점](#갱신이-어려운-지점)
- [삭제 요구가 부딪히는 지점](#삭제-요구가-부딪히는-지점)
- [이 구분을 데이터 모델로 밀어붙이면](#이-구분을-데이터-모델로-밀어붙이면)
- [13장이 이 구분을 아키텍처로 밀어붙인다](#13장이-이-구분을-아키텍처로-밀어붙인다)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **한 조직의 여러 데이터 저장소 중에서 무엇이 정본이고 무엇이
다시 만들 수 있는 사본인가, 그리고 그 구분을 명시하면 무엇이 쉬워지는가.**

운영계와 분석계의 구분(→ [EDW](../concepts/enterprise-data-warehouse.md))과
나란히 놓이지만 축이 다르다. 운영/분석은 **누가 쓰는가**의 구분이고, 기록/파생은
**데이터가 어느 방향으로 흐르는가**의 구분이다 (1장, p.10).[^kleppmann2026]

## 두 정의

- 기록 시스템(system of record, 진실의 원천 source of truth)의 정의는 원문 그대로
  (1장, p.11):[^kleppmann2026]

> A system of record, also known as a *source of truth*, holds the authoritative
> or *canonical* version of data. When new data comes in—for example, as user
> input—it is first written here. Each fact is represented exactly once […]. If
> there is any discrepancy between another system and the system of record, the
> value in the system of record is (by definition) the correct one.

- 파생 데이터 시스템(derived data system)의 정의도 원문 그대로 (1장,
  p.11):[^kleppmann2026]

> Data in a derived system is the result of taking existing data from another
> system and transforming or processing it in some way. If you lose derived
> data, you can re-create it from the original source.

- 파생의 사례: 캐시(있으면 캐시가 답하고, 없으면 원본 데이터베이스로 내려간다),
  비정규화된 값, 인덱스, 구체화 뷰(materialized view), 변환된 표현, 데이터셋으로
  학습한 모델 (1장, p.11).[^kleppmann2026]

## 왜 이 구분이 쓸모 있나

- 파생 데이터는 엄밀히 말해 **중복(redundant)** 이다 — 이미 있는 정보를 복제한다.
  그럼에도 읽기 질의의 성능을 얻으려면 대체로 필수이며, 하나의 원천에서 여러
  데이터셋을 파생시켜 같은 데이터를 여러 관점에서 볼 수 있게 한다 (1장,
  p.11).[^kleppmann2026]
- 분석 시스템은 보통 파생 데이터 시스템이다 — 다른 곳에서 만들어진 데이터의
  소비자이기 때문이다 (1장, p.11).[^kleppmann2026]
- 운영 서비스는 둘이 섞여 있다: 데이터가 처음 쓰이는 주 데이터베이스가 기록
  시스템이고, 흔한 읽기를 빠르게 하는 인덱스·캐시(특히 기록 시스템이 효율적으로
  답할 수 없는 질의용)가 파생이다 (1장, p.11).[^kleppmann2026]
- 어느 데이터가 어느 데이터에서 파생됐는지를 분명히 해 두면, 그러지 않았으면
  혼란스러웠을 시스템 아키텍처가 정리된다 (1장, p.11).[^kleppmann2026]

## 도구가 아니라 용법이 정한다

- 대부분의 데이터베이스·저장 엔진·질의 언어는 그 자체로 기록 시스템도, 파생
  시스템도 아니다. 데이터베이스는 도구일 뿐이고 어떻게 쓰느냐가 당신에게 달려
  있다. 이 구분은 도구가 아니라 **애플리케이션에서의 사용 방식**에 달렸다 (1장,
  p.11).[^kleppmann2026]
- 웨어하우스 쪽 대응 개념과 겹친다: 마스터 데이터의 골든 카피를 정하고 원천으로
  되먹이는
  [마스터 데이터 관리](../concepts/master-data-management.md)가 같은 문제를
  운영계 사이에서 다룬다.

## 갱신이 어려운 지점

- 한 시스템의 데이터가 다른 시스템에서 파생됐다면, 기록 시스템의 원본이 바뀔 때
  파생 데이터를 갱신하는 절차가 필요하다 (1장, p.11).[^kleppmann2026]
- 그런데 많은 데이터베이스는 애플리케이션이 그 데이터베이스 하나만 쓸 것이라는
  가정 위에 설계돼 있어서, **여러 시스템을 통합해 그런 갱신을 전파하기 쉽게
  만들어 주지 않는다** (1장, p.11).[^kleppmann2026] 데이터 파이프라인을 통한 데이터
  통합(data integration)이 이 책 11장의 주제다 (1장, p.11).[^kleppmann2026]
- 실무적 접점: 데이터베이스 변경분을 발행해 다른 시스템이 따라오게 하는 체인지로그
  방식이 이 문제의 흔한 해법이다 —
  [데이터 생태계와 유스케이스](../concepts/kafka-data-ecosystem-and-use-cases.md)의
  커밋 로그 절과
  [ETL 34 서브시스템](../concepts/etl-subsystems.md)의 변경 데이터 캡처(2)가 그
  자리다.
- 변환 도구 쪽에서는 이 갱신 절차가 물리 형태의 선택으로 나타난다: 뷰는 갱신 절차
  자체가 없고(조회 시점에 다시 계산한다), 테이블은 원천의 새 레코드가 자동으로
  반영되지 않아 다시 만들어 주어야 하며, 구체화 뷰는 그 갱신을 데이터 플랫폼에
  맡긴다 (materializations.md, "View", "Table",
  "Materialized View").[^dbtlabs2026-materialization]

## 삭제 요구가 부딪히는 지점

- GDPR은 개인에게 요청 시 자기 데이터를 지우게 할 권리(잊힐 권리, right to be
  forgotten)를 준다. 그런데 많은 데이터 시스템은 추가 전용 로그(append-only log)
  같은 불변 구조에 의존한다 — 불변이어야 할 파일 중간의 데이터를 어떻게 지울
  것인가, 그리고 **이미 파생 데이터셋(예: ML 모델 학습 데이터)에 흡수된 데이터의
  삭제는 어떻게 다룰 것인가**. 답하기 어려운 새 공학 과제다 (1장,
  p.24).[^kleppmann2026]
- 현재로서는 어떤 기술·아키텍처가 GDPR을 준수한다고 볼 수 있는지에 대한 명확한
  지침이 없다. 규제는 기술이 빠르게 변하므로 **의도적으로** 특정 기술을 강제하지
  않고, 해석의 대상인 상위 원칙만 제시한다 (1장, p.24).[^kleppmann2026]

## 이 구분을 데이터 모델로 밀어붙이면

같은 책 3장이 이 축을 데이터 모델링 결정으로 두 번 다시 쓴다.

- 비정규화가 파생 데이터의 한 형태다 — **비정규화를 파생 데이터의 한 형태로 보는 것이 도움이 될
  수 있는데, 데이터의 중복 사본을 갱신하는 프로세스를 마련해야 하기 때문이다** (3장,
  p.74).[^kleppmann2026] 위 [갱신이 어려운 지점](#갱신이-어려운-지점)이 요구하는 그 절차가
  비정규화에서는 애플리케이션의 책임으로 온다. 전문은
  [정규화와 비정규화](../concepts/normalization-and-denormalization.md)에 있다.
- 발상을 끝까지 밀면 쓰기 표현과 읽기 표현이 갈린다 — **어차피 한 데이터 표현에서 다른 것을
  유도할 것이라면, 쓰기와 읽기 각각에 최적화된 서로 다른 표현을 고를 수 있다** (3장,
  p.101).[^kleppmann2026] 그 결과가 **불변 이벤트 로그를 진실의 원천으로 두고 구체화 뷰를
  거기서 유도하는 이벤트 소싱(event sourcing)과, 읽기 최적화 표현을 따로 유지하는 명령 질의
  책임 분리(CQRS)** 다 (3장, p.102).[^kleppmann2026]
- 그 모델이 파생 데이터에 요구하는 규율이 하나 명시된다 — **이벤트 소싱의 핵심 원칙은 구체화 뷰가
  이벤트 로그에서 재현 가능한 방식으로 유도된다는 것이다. 언제나 구체화 뷰를 지우고 같은 이벤트를
  같은 순서로 같은 코드로 처리해 다시 계산할 수 있어야 한다** (3장, p.103).[^kleppmann2026] 이는
  위 파생 데이터의 정의("파생 데이터를 잃어도 원본에서 다시 만들 수 있다")를 설계 요구로 격상한
  것이다. 전문은 [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md)에 있다.
- 위 [삭제 요구가 부딪히는 지점](#삭제-요구가-부딪히는-지점)이 그 모델에서 그대로 재현된다 —
  **이벤트가 불변이어야 한다는 요구는 이벤트가 개인 데이터를 담을 때 문제를 만든다. 이벤트 로그가
  사용자별이면 그 사용자의 로그 전체를 지우면 되지만, 로그가 여러 사용자에 관한 이벤트를 담고
  있으면 그렇게 되지 않는다. 개인 데이터를 이벤트 바깥에 저장하거나 나중에 지울 수 있는 키로
  암호화(크립토 슈레딩)해 볼 수 있지만, 그것 역시 파생 상태를 다시 계산하기 어렵게 만든다**
  (3장, p.104).[^kleppmann2026]

## 13장이 이 구분을 아키텍처로 밀어붙인다

같은 책 13장은 이 구분을 조직 전체의 데이터플로를 설계하는 축으로 삼는다.

- 무엇을 지정하는가 — **이 접근에서 어떤 시스템은 기록 시스템으로 지정되고 다른 데이터는 그것으로부터
  변환을 통해 파생된다. 이런 방식으로 우리는 색인·구체화 뷰·기계 학습 모델·통계 요약 등을 유지할 수
  있다. 이 유도와 변환을 비동기적이고 느슨하게 결합되게 만드는 것은 한 영역의 문제가 무관한 영역으로
  퍼지는 것을 막아 시스템 전체의 견고성과 결함 내성을 높인다** (13장, p.579).[^kleppmann2026]
- 위 [갱신이 어려운 지점](#갱신이-어려운-지점)에 답이 하나 붙는다 — **데이터가 먼저 기록 시스템
  데이터베이스에 쓰이고 그 변경이 포착돼 같은 순서로 검색 색인에 적용되도록 배치할 수 있다. CDC가
  색인을 갱신하는 유일한 방법이면 색인이 전적으로 기록 시스템에서 파생됐고 따라서 그것과 일관된다고
  (소프트웨어의 버그를 빼면) 확신할 수 있다** (13장, p.541).[^kleppmann2026] 반대로 애플리케이션이
  양쪽에 직접 쓰면 어느 쪽도 순서의 "책임자"가 아니어서 영구히 어긋날 수 있다 (13장,
  p.541).[^kleppmann2026] 전문은
  [데이터 통합](../concepts/data-integration.md)에 있다.
- 그리고 이 구분이 진화의 기제가 된다 — **데이터플로를 한 데이터셋에서 다른 데이터셋으로 가는 변환으로
  표현하는 것은 애플리케이션을 진화시키는 데도 도움이 된다. 처리 단계 중 하나를 바꾸고 싶으면 —
  예컨대 색인이나 캐시의 구조를 바꾸고 싶으면 — 새 변환 코드를 전체 입력 데이터셋에 다시 돌려 출력을
  다시 유도하면 된다. 마찬가지로 무언가 잘못되면 코드를 고치고 데이터를 재처리해 복구할 수 있다**
  (13장, p.579).[^kleppmann2026]

## 이어지는 페이지

- [데이터 통합](../concepts/data-integration.md) — 이 구분을 여러 저장 시스템에 걸쳐 실제로
  운용하는 방법
- [언번들드 데이터베이스](../concepts/unbundling-databases.md) — 파생 유지 기능을 데이터베이스
  밖으로 꺼낸 그림
- [이벤트 소싱과 CQRS](../concepts/event-sourcing-and-cqrs.md) — 이 구분을 데이터 모델로
  삼았을 때의 이점과 함정
- [정규화와 비정규화](../concepts/normalization-and-denormalization.md) — 비정규화가 파생
  데이터로 읽히는 자리
- [소셜 네트워크 홈 타임라인 사례](../concepts/social-network-home-timelines.md) — 파생 데이터
  갱신 절차의 가장 구체적인 실물
- [EDW](../concepts/enterprise-data-warehouse.md) — 운영계/분석계 분리라는 다른 축
- [데이터 레이크](../concepts/data-lake.md) — 파생 데이터의 착지 형태가 파일로
  넓어지는 흐름
- [분산 시스템과 단일 노드](../concepts/distributed-versus-single-node.md) — 파생
  데이터가 다른 기계에 있을 때 생기는 문제
- [구체화 스펙트럼](../concepts/materialization-spectrum.md) — 파생 데이터를 언제
  다시 계산하고 언제 저장하느냐의 실무 손잡이
- [dbt 스냅샷](../concepts/dbt-snapshots.md) — 다시 만들 수 없는 파생물이 기록
  시스템 쪽으로 넘어가는 사례

[^kleppmann2026]: Kleppmann & Riccomini 2026, 1장 "Trade-Offs in Data Systems Architecture" · 3장 "Data Models and Query Languages" · 13장 "A Philosophy of Streaming Systems"
[^dbtlabs2026-materialization]: dbt Labs 2026, dbt 공식 문서 "Build" 절

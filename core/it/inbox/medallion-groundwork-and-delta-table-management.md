---
type: concept
title: 메달리온 계층 이전의 결정과 Delta 테이블 관리
status: draft
description: "메달리온 아키텍처의 Bronze 계층에 데이터가 닿기 전에 정해 두어야 하는 것들과 그 뒤 테이블을 관리하는 기법들 — 랜딩 존을 따로 둘지 Bronze로 곧장 반입할지, \"원시\"라는 말이 중개(mediation)를 허용하는 범위, 배치와 실시간을 가르는 기준과 오류 계층, Spark Structured Streaming·change data feed·CDC 셋의 분업과 실시간 복제 데이터를 Bronze로 볼지 pre-Bronze로 볼지, ETL·오케스트레이션 도구 선택이 아키텍처를 되규정한다는 판정, 그리고 2025년 저술 시점의 Delta 테이블 관리 기법 여섯(Z-Ordering·V-Ordering·파티셔닝·liquid clustering·컴팩션과 최적화된 쓰기·DeltaLog)과 DeltaLog가 이력 데이터베이스가 아니라는 한계"
generated: { by: "claude-opus-5", at: "2026-09-23T20:00:00Z" }
sources:
  - { id: strengholt2025, resource: /it/sources/strengholt2025.md }
---

# 메달리온 계층 이전의 결정과 Delta 테이블 관리

- [버전 조건](#버전-조건)
- [무엇을 먼저 정하는가](#무엇을-먼저-정하는가)
- [추가 랜딩 존 — 둘 것인가 건너뛸 것인가](#추가-랜딩-존--둘-것인가-건너뛸-것인가)
- ["원시"라는 말이 허용하는 중개](#원시라는-말이-허용하는-중개)
- [배치 반입](#배치-반입)
- [실시간 반입](#실시간-반입)
- [ETL과 오케스트레이션 도구](#etl과-오케스트레이션-도구)
- [Delta 테이블 관리 기법 여섯](#delta-테이블-관리-기법-여섯)
- [저자의 맺음 — 기초 단계를 과소평가하지 말 것](#저자의-맺음--기초-단계를-과소평가하지-말-것)
- [이 KB의 원전과 맞대어 본 것](#이-kb의-원전과-맞대어-본-것)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **메달리온 계층을 짓기 전에 무엇을 정해 두어야 하고, 계층이 선 뒤 그 테이블을
무엇으로 관리하는가.**

[메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md)가 Bronze·Silver·
Gold 셋이 무엇인지를 규정한다면, 이 페이지는 그 셋 **바깥**에서 정해지는 것들을 받는다. 저자는 이
장을 준비용 다리(preparatory bridge)라 부르고, 메달리온 논의 전체에 되풀이해 나올 부품과 패턴을
미리 소개하는 자리로 규정한다 (2장 도입).[^strengholt2025]

## 버전 조건

> **버전 조건**: 2025년 저술 시점. 아래
> [Delta 테이블 관리 기법 여섯](#delta-테이블-관리-기법-여섯)과
> [ETL과 오케스트레이션 도구](#etl과-오케스트레이션-도구) 두 절은 제품 기능과 제품 목록이라
> 그 시점의 Delta Lake·Databricks·Microsoft Fabric 구현에 묶인다. 그 밖의 절(랜딩 존, 원시 데이터,
> 배치와 실시간의 선택 기준)은 설계 판단이라 시점에 둔감하다. 이 소스에 공표된 만료 날짜가 없어
> `stale_after`는 걸지 않는다.

## 무엇을 먼저 정하는가

- 순서를 저자가 못 박는다 — 어떤 아키텍처든 설계·구현에 들어가기 전에 데이터가 있어야 하므로
  **첫 단계는 언제나 대상 원천 시스템을 짚어 내고 거기서 데이터를 모을 최선의 방법을 알아내는
  것**이다 (2장 §"Foundational Preconditions").[^strengholt2025]
- 그 뒤에 오는 결정이 둘로 갈린다 (2장 §"Foundational Preconditions"):[^strengholt2025]
  - **반입 전에 중간 랜딩 존을 쓸 필요가 있는가.** 저자는 이것을 "주요 도전(major challenge)"으로
    부르고, 랜딩 존이 데이터가 메달리온 아키텍처에 통합되기 전의 조직화와 변환을 돕는다고 적는다.
  - **배치로 할 것인가 실시간으로 할 것인가.** 이 결정이 데이터 통합·오케스트레이션·테이블 관리에
    쓸 도구와 기법을 좌우한다.
- 장 도입부가 다루는 부품 다섯에 정의를 붙여 둔다 — 추가 랜딩 존, 원시 데이터, 배치 처리, 실시간
  데이터 처리, ETL·오케스트레이션 도구다 (2장 도입).[^strengholt2025]
  - **이 부품들이 메달리온 그림 안에 들어가는지는 사람마다 다르다** — 어떤 실무자는 주 아키텍처
    프레임워크 안에 그대로 그리고, 다른 이들은 그것이 보조 역할임을 강조하려고 다이어그램 밖이나
    주변부에 둔다 (2장 도입).[^strengholt2025]
  - 이 "그림 안이냐 밖이냐"의 물음이 아래 절 전부에 되풀이된다. 랜딩 존을 Bronze라 부를지, 실시간
    복제 데이터를 Bronze로 볼지가 같은 물음의 변주다.

## 추가 랜딩 존 — 둘 것인가 건너뛸 것인가

- 정의 — 랜딩 존(landing zone)은 **원시 데이터가 메달리온 아키텍처에 착지하기 전에 반입되는
  예비 영역**으로 흔히 쓰인다. 그 선택은 데이터 원천의 특성 같은 여러 요인이 좌우한다
  (2장 §"Extra Landing Zones").[^strengholt2025]
- 랜딩 존을 두게 만드는 조건 (2장 §"Extra Landing Zones"):[^strengholt2025]
  - **외부 서비스나 SaaS 벤더**를 상대할 때는 Bronze 계층으로 옮기기 전에 데이터를 먼저 담을 안전한
    랜딩 존이 필요할 수 있다.
  - **반입 요건이 엄격한 애플리케이션 팀**은 자기 전용 랜딩 존을 요구할 수 있다. 그 팀들이 추출
    과정을 직접 관리해 예기치 않은 오류나 데이터 불일치가 없게 하고, 이를 위해 특정 ETL 도구나
    통합 런타임(integration runtime) 배포를 함께 요구하기도 한다.
  - 그래서 **원천과 레이크하우스 아키텍처 사이에 랜딩 영역이 여럿 있는 것이 드물지 않다**.
- 반대 방향도 성립한다 — 원천 시스템의 요건에 따라 **Bronze 계층으로 곧장 반입하는 것도 가능하다**.
  원천 시스템이 튼튼한 보안 수단과 안정적인 직접 반입 기법을 갖췄다면 중간 랜딩 존을 건너뛰고 바로
  먹이는 쪽이 더 효율적일 수 있고, 그럴 때는 Bronze 반입 전에 데이터를 스테이징할 필요가 없다
  (2장 §"Extra Landing Zones").[^strengholt2025]
- 곁글이 이 절의 요지를 못 박는다 — Bronze 계층이 주로 데이터 수집의 영역을 맡지만 **더 크거나 복잡한
  환경에서는 예비 랜딩 존이 추가로 필요할 수 있고, 그 계층을 Bronze라 부를지는 각자가 정한다.** 어떤
  조직은 그것을 "tin layer"·"pre-Bronze"·"pre-refinement"·"staging"·"landing area"라 부르며 통상의
  메달리온 아키텍처 **밖**에 두고, 다른 조직은 Bronze 계층 설계 안에 포함시킨다. 중요한 것은 조직의
  기능·비기능 요건을 충족하는 방식으로 반입하고 저장하는 것이다
  (2장 §"Landing Zones Takeaway" 곁글).[^strengholt2025]
  - **이 KB의 [스테이징 영역](../concepts/staging-area.md)이 받는 것이 같은 자리다** — 다만 그쪽은
    웨어하우스 적재가 끝나면 비우는 일시적 완충으로 규정되고, 이쪽 랜딩 존은 비움 규칙 없이 원천의
    특성으로만 정당화된다.

## "원시"라는 말이 허용하는 중개

- 저자가 낱말에 경고를 붙인다 — Bronze 계층에 착지시키는 데이터를 두고 "raw"나 "as-is" 같은 말을
  쓸 때는 **조심해야 한다**. 수천 개 테이블을 갖는 벤더 패키지 같은 복잡한 트랜잭션 시스템에서는
  추출 과정에 엔지니어가 끼어들어 중개해야 할 수 있기 때문이다
  (2장 §"Raw Data").[^strengholt2025]
- 저자 자신의 현장 사례 — 코어 뱅킹 시스템 Temenos T24에서 데이터를 추출해야 했는데, 이 시스템은
  모든 데이터를 XML로 저장하고 각 테이블이 기본 키 `RECID`와 데이터 `XMLRECORD` **두 열뿐**이었다.
  그대로 추출하면 매우 복잡하고 다룰 수 없는 데이터셋이 되므로 T24 Data Extractor로 더 다루기 쉬운
  구조에 담았고, 뒤에는 Apache Flink로 옮겨 T24에서 다른 환경으로 흘러가는 XML 레코드를 흐르는
  중에 해독·변환·보강했다 (2장 §"Raw Data").[^strengholt2025]
- 일반화 — 수만 개의 특화되고 서로 얽힌 테이블을 갖는 전사적 자원 관리 시스템도 직접 추출이 어려워
  조직들이 흔히 추출 서비스를 쓰거나 그 상용 패키지가 제공하는 시맨틱 모델을 거친다. 곧 **기술
  시스템 테이블에서 반입으로 가는 첫 단계에 미들웨어나 맞춤 제작 소프트웨어 부품이 끼는 경우가
  있고, 그 역할은 복잡한 시스템 테이블이나 독자 구조를 더 단순하고 다루기 쉬운 데이터 모델로
  대응시키는 것**이다 (2장 §"Raw Data").[^strengholt2025]
- 곁글이 경계를 규정한다 — 복잡한 데이터의 전처리나 중개는 **데이터가 첫 계층에 닿기 전에** 일어나고
  **이것은 메달리온 아키텍처 안의 변환으로 치지 않는다.** 그러므로 첫 계층의 데이터는 통상 "원시"이되,
  복잡한 시스템을 다룰 때는 전처리가 다루기 쉬움과 명료함을 위해 결정적일 수 있다
  (2장 §"Raw Data Takeaway" 곁글).[^strengholt2025]
  - **이 경계 규정이 이 절의 실질이다.** "원시"는 손대지 않았다는 뜻이 아니라 **메달리온 안에서
    손대지 않았다**는 뜻으로 좁혀진다.

## 배치 반입

- 정의와 존속 이유 — 배치 처리는 **일정 기간에 걸쳐 데이터를 모아 한꺼번에 처리하는 방식**이고,
  2025년 저술 시점에도 널리 쓰이는 이유가 셋이다 (2장 §"Batch Processing"):[^strengholt2025]
  - **비용 효율** — 큰 데이터셋을 한 번의 연산으로 처리하므로 연속 처리의 필요를 줄이고 부품이
    쉼 없이 돌지 않게 한다.
  - **기존 기반의 지원** — 많은 기존 시스템과 인프라가 배치 처리를 폭넓게 지원한다.
  - **이력 관점 구축에 유리** — 누적된 데이터 전부를 한 번에 처리한다.
- Bronze 계층에 배치 반입을 세울 때 챙길 것 넷 (2장 §"Batch Processing"):[^strengholt2025]
  - **무결성** — 행 수·체크섬·해시 합계 같은 검증 방법으로 전송 중의 정확성과 완전성을 확인하고,
    파일 수·데이터 용량·복사 소요 시간·활동 실행 ID·결과 같은 감사 정보를 추적해 모니터링과 문제
    추적을 돕는다.
  - **간격 선택** — 연속 처리와 달리 배치는 정해진 간격에 일어나므로, 원천 가용성·처리 순서·분석의
    시급함을 고려해 간격을 신중히 고른다.
  - **오류 처리** — 배치는 실패할 수 있으므로 Bronze 계층의 복원력을 위해 튼튼한 오류 처리 기제가
    필수다. 저자는 **"오류 계층(error layer)" 또는 "데이터 고아원(data orphanage)"** 을 따로 만들어
    이 문제들을 모니터링·관리하는 안전망으로 두는 것을 고려하라고 적는다.
  - **도구 선택** — 추출·반입 도구의 선택이 결정적이고, 예로 Azure Data Factory가 커넥터 200개
    남짓을 제공하며 추출·워크플로 오케스트레이션·파이프라인 관리에 널리 쓰인다고 든다.
- 곁글이 이 절의 요지를 뒤집어 놓는다 — 데이터 수집의 도전은 새로운 것이 아니고 조직들은 이미
  웨어하우스를 위해 데이터를 모아 왔다. 그래서 **맞춤 추출 스크립트나 전통적 배치 전달 같은 기존
  인터페이스를 레이크하우스 반입에 그대로 재사용하는 일이 잦다.** 배치 처리가 단순해 보여도 기업에는
  여전히 복잡한 과업인데, **원천마다 대개 저마다의 처리를 받기 때문**이다
  (2장 §"Batch Processing Takeaway" 곁글).[^strengholt2025]
- 수집 자체가 여전히 난제라는 진단도 함께 온다 — 원천 시스템 쪽 파급, 형식과 네트워크 설계의 다양함,
  기술과 플랫폼의 다양함 때문에 **일관되고 표준화된 방식으로 데이터를 추출하기가 어렵다**
  (2장 §"Batch Processing").[^strengholt2025]

## 실시간 반입

- 왜 하는가 — 데이터가 생성되는 순간에 처리하면 즉각적 통찰과 시의적절한 결정이 가능해지고, 이는
  **사기 탐지·개인화된 고객 상호작용·동적 시스템 조정** 같은 응용에 결정적이다
  (2장 §"Real-Time Data Processing").[^strengholt2025]
- **공짜가 아니다** — 대부분의 애플리케이션은 이벤트를 자동으로 만들어 내지 않으므로, 실시간 반입을
  세우려면 부품을 더하거나 기존 구성을 손봐야 한다. 이벤트 분배를 다루도록 애플리케이션 아키텍처를
  고쳐야 할 수 있고(예: Express를 쓰는 Node.js 애플리케이션에 라이브러리를 깔고 Azure Event Hubs로
  이벤트를 보내는 코드를 쓰는 것), 트랜잭션 데이터베이스 로그를 읽거나 API를 호출할 소프트웨어를
  덧붙여야 할 수도 있다. 이벤트 흐름이 꾸준해진 뒤에야 Spark 같은 서비스나 프레임워크로 포착·처리를
  시작할 수 있다 (2장 §"Real-Time Data Processing").[^strengholt2025]
- 곁줄 하나가 낱말을 가른다 — 데이터 이동에서 **상태를 실어 나르는 이벤트(state-carrying events)와
  단순 알림(notifications)을 구분하는 것이 필수**다. 앞은 특정 시점의 애플리케이션 상태 스냅샷을
  주어 처리·분석·후속 이벤트 촉발에 쓰이고 데이터 변경이나 갱신을 감시하는 데 결정적이며, 뒤는
  발생 사실을 알려 즉각 행동을 유도하는 기본 경보로 통상 상세한 상태 정보를 담지 않는다
  (2장 §"Real-Time Data Processing" 곁줄 warning).[^strengholt2025]

### Spark Structured Streaming

- 자리 — Apache Spark 엔진 안의 Structured Streaming 지원이 실시간 처리를 크게 개선하고, Spark의
  구성 요소로서 데이터 스트림의 연속 처리를 가능하게 해 이벤트 로그 파일·IoT 장치·Apache Kafka 같은
  실시간 메시징 시스템 등 다양한 원천에서 반입할 수 있게 한다. **실시간 시나리오에서 흔한 원시·
  비구조 형태의 데이터를 다루는 데도 뛰어나다**
  (2장 §"Real-Time Data Processing" ▸ "Spark Structured Streaming").[^strengholt2025]
- 이 지점에서 변환이 결정적이 된다 — 비구조 데이터라면 **중첩 JSON 평탄화, XML에서 필드 추출, 새 열을
  파생시키는 복잡한 함수 적용** 같은 단계가 들어가고, 이는 하류 분석과 저장을 위한 정제·준비에
  필수다 (같은 소절).[^strengholt2025]
- 출력처는 응용 요건에 따라 넓게 갈린다 — ACID 준수 저장과 버저닝을 위한 Delta Lake, 관계형 저장을
  위한 전통적 데이터베이스, 스키마 없는 저장을 위한 NoSQL, 또는 후속 처리를 위해 실시간 메시지
  버스나 이벤트 큐로 되돌려 보내는 것까지다 (같은 소절).[^strengholt2025]
- 곁줄이 비용을 짚는다 — **Spark로 실시간 반입을 하려면 "always on" 컴퓨트 클러스터가 필요해 비용이
  더 든다. 지연이 문제되지 않으면 5분마다 트리거해 실행하는 쪽을 고려해 비용을 낮추라**
  (같은 소절 곁줄 note).[^strengholt2025]

### change data feed

- 정의 — change data feed는 **Delta 테이블의 변경을 발생 시점에 포착해 (준)실시간으로 처리할 수 있게
  하는 기능**이다 (2장 §"Real-Time Data Processing" ▸ "Change Data Feed").[^strengholt2025]
- 켜는 법은 테이블 속성 하나다 — Delta 테이블에 `delta.enableChangeDataFeed` 를 `true`로 두면 되고,
  저자가 든 예는 `ALTER TABLE myDeltaTable SET TBLPROPERTIES (delta.enableChangeDataFeed = true)`
  이다 (같은 소절).[^strengholt2025]
- 쓰임 — change data feed는 **Spark Structured Streaming의 입력 데이터 원천이 될 수 있고**, 둘의
  조합이 실시간 처리의 강력한 기제가 된다. 예컨대 초기 `MERGE` 비교 이후의 변경분만 처리해 ETL/ELT를
  가속·단순화할 수 있고, 같은 패턴으로 Kafka나 RDBMS 같은 하류 시스템에 변경을 흘려보내 뒤 단계가
  그 증분 데이터를 쓰게 할 수도 있다 (같은 소절).[^strengholt2025]

### 변경 데이터 캡처(CDC)

- 정의 — 변경 데이터 캡처(change data capture, CDC)는 **데이터에 가해진 변경을 실시간으로 식별하고
  포착하는 기법**이다. CDC 도구가 데이터베이스 수정을 능동적으로 감시해 발생 즉시 기록하고, 그래서
  다른 시스템으로의 복제가 가능해진다. 저자는 이것이 **원천 시스템의 실시간 포착에 특히 효과적**이고
  그 변경을 데이터 플랫폼에 매끄럽게 통합시킨다고 적으며, 상세는 5장으로 미룬다
  (2장 §"Real-Time Data Processing" ▸ "Change Data Capture").[^strengholt2025]
  - 이 KB의 [변경 데이터 캡처](../concepts/change-data-capture.md)가 이 기제의 두꺼운 원전을 이미
    갖는다. 이 소스가 더하는 것은 정의가 아니라 **레이크하우스 반입 맥락에서 CDC가 change data
    feed와 어떻게 갈리는가**이고, 그것이 바로 아래 표다.

### 셋의 분업과 Bronze 경계 물음

- 저자가 셋을 한 표로 세운다 (2장 §"Real-Time Data Processing" ▸ "Considerations and Learning
  Resources", 표 2-1):[^strengholt2025]

  | 선택지 | 저자의 서술 |
  |---|---|
  | Spark Structured Streaming | 복잡한 연산을 지원하고 여러 원천·싱크와 통합되며 연속 데이터 처리를 다룬다 |
  | change data feed | **Delta 테이블**의 변경을 실시간으로 포착하고, 증분과 상태 간 차이(델타)만 흘려보내 효율적 처리를 가능하게 한다 |
  | CDC | **데이터베이스 트랜잭션 로그**의 변경을 추적·포착해 실시간 복제와 통합을 가능하게 한다 |

  - **표가 가르는 축은 무엇을 감시하는가다** — change data feed는 레이크하우스 안의 Delta 테이블을,
    CDC는 원천 데이터베이스의 트랜잭션 로그를 본다. 곧 둘은 경쟁 기법이 아니라 파이프라인의 다른
    지점에 놓인다.
- 그 위에 저자가 어려운 물음 하나를 올린다 — Microsoft Fabric의 미러링(mirroring) 기능으로 클라우드
  네이티브 Azure SQL 애플리케이션의 데이터를 레이크하우스(OneLake)로 준실시간 복제한다고 하자. 이
  복제 기법은 **데이터베이스의 CDC 기술을 써서 적절한 Delta 테이블로 변환해 착지시킨다.** 그러면
  **이 데이터가 Bronze 계층에 속하는가?** 저자의 답은 필요에 달렸다는 것이다
  (같은 소절).[^strengholt2025]
  - **전체 추출분을 쌓는 것이 주목적이면** 이 실시간 복제 데이터는 중간(또는 랜딩) 영역으로 분류하는
    편이 낫다. 원천처럼 직접 질의할 수 있게 해 주되 이력 분석을 위해 원시 사본을 누적하도록 Bronze를
    조직하지는 못하므로, 그때 첫 계층은 복제 계층 또는 pre-Bronze 계층으로 작동한다
    (같은 소절).[^strengholt2025]
  - **원천을 "as-is"로 비추는 질의 가능한 Bronze를 유지하는 것이 목적이면** 실시간 복제 데이터를
    Bronze의 일부로 볼 수 있다 (같은 소절).[^strengholt2025]
- 곁글이 이 물음의 답을 규정으로 굳힌다 — **실시간 반입이나 복제를 도입할지, 그리고 그 데이터를
  Bronze로 분류할지 중간 영역으로 분류할지는 근본적으로 구별되는 사용 요건과 전략적 목표가 결정한다**
  (2장 §"Real-Time Data and Streaming Ingestion Takeaway" 곁글).[^strengholt2025]
- 마지막으로 계층의 순차성이 깨지는 자리를 짚는다 — 실시간 반입에서는 **여러 계층이 동시에 갱신되는
  일이 잦다.** Azure Event Hubs의 스트리밍 데이터를 Spark Structured Streaming으로 처리하면서 불필요한
  열 제거·집계·예비 감성 점수 부여 같은 변환을 즉시 수행하고, 원시 데이터는 Bronze에 저장하되 변환·정제된
  데이터는 곧바로 Silver나 Gold로 보낼 수 있다. **그런 시나리오에서 Bronze는 읽어 가는 계층이라기보다
  보관 구역(archive zone)에 가깝게 작동한다**
  (2장 §"Real-Time Data Processing" ▸ "Considerations and Learning Resources").[^strengholt2025]

## ETL과 오케스트레이션 도구

- 왜 이 절이 기초 다지기에 드는가 — 추출·변환·적재·오케스트레이션 도구의 논의는 **데이터 파이프라인
  설계에 크게 영향을 주기 때문**이다 (2장 §"ETL and Orchestration Tools").[^strengholt2025]
- 저자가 드는 도구 다섯과 그 자리 (같은 절):[^strengholt2025]

  | 도구 | 저자가 적은 자리 |
  |---|---|
  | Apache Airflow | 워크플로를 프로그램으로 저작·스케줄·모니터링하는 오픈 소스 플랫폼. 복잡한 파이프라인 오케스트레이션과 태스크 간 의존 관리에 특히 유용하다 |
  | Azure Data Factory | Synapse Analytics·Azure Databricks·Microsoft Fabric을 채택한 조직에 널리 쓰인다. Fabric 안에서는 그냥 Data Factory로 불리되 기능은 대체로 같고, 다수 커넥터 지원이 중요한 특징이다 |
  | Databricks Auto Loader | Databricks 생태계 전용. 클라우드 오브젝트 저장에 도착하는 새 파일을 증분 처리하는 데 뛰어나고, **스키마 진화 처리**가 두드러진 기능이다 |
  | Databricks LakeFlow Connect | Databricks 전용 서비스. Salesforce·SQL Server 등의 내장 커넥터를 제공한다 |
  | Databricks Workflows | Databricks의 관리형 오케스트레이션 서비스. ETL·분석·기계 학습 파이프라인의 다중 태스크 워크플로를 정의·관리·모니터링한다 |

  - 더 넓은 호환과 기능을 위해 Fivetran·Qlik·StreamSets·Syncsort·Informatica·Stitch 같은 서드파티
    도구도 흔히 쓰이고, 이들은 폭넓은 커넥터와 오케스트레이션 능력을 제공하며 다른 도구와 함께
    쓰이는 일이 잦다 (같은 절).[^strengholt2025]
- **이 절의 판정이 도구 목록보다 중요하다** — 고른 ETL 도구가 가능하게 하는 데이터 적재 단계의
  복잡도가 아키텍처 안에 전처리 단계를 더 요구할 수 있으므로, **ETL 도구의 선택은 첫 계층들의 설계뿐
  아니라 아키텍처 전체에도 영향을 준다.** 조직 요건에 맞는지 신중히 따져야 한다
  (같은 절).[^strengholt2025]
  - 곧 이 책에서 도구는 아키텍처의 하위 선택이 아니라 **아키텍처를 되규정하는 제약**으로 놓인다.

## Delta 테이블 관리 기법 여섯

- 자리 — 테이블 관리는 **모든 계층에 걸리는 관심사**이고 성능·사용성·비용에 영향을 준다. `*`-ordering과
  liquid clustering 같은 기법이 데이터 관리 방식을 개선해 조회를 더 효율적으로 만드는 권장 방법이다
  (2장 §"Managing Delta Tables").[^strengholt2025]

### Z-Ordering

- 하는 일 — Z-ordering은 **관련된 정보를 같은 파일 안에 모아 조회 효율을 높이는 기법**이다. 지역성
  (locality)을 개선하고 I/O 연산을 줄이며 다차원 데이터 관리를 지원해 **보통의 조회보다 두 배에서 네
  배 효율적**이라고 저자가 적고, 효율적 필터링과 조인을 요구하는 시나리오에서 특히 잘 듣는다
  (2장 §"Managing Delta Tables" ▸ "Z-Ordering").[^strengholt2025]
- Delta Lake가 데이터 건너뛰기(data-skipping) 알고리즘으로 이 기법을 자동 활용하고, 쓰는 쪽은
  `ZORDER BY` 절로 조직할 열을 지정하면 된다. 저자의 예는
  `OPTIMIZE events WHERE date >= current_timestamp() - INTERVAL 1 day ZORDER BY (eventType)`
  이다 (같은 소절).[^strengholt2025]
- **적용 조건이 있다** — 스캔할 데이터 양을 크게 줄이지만 수백 기가바이트에서 테라바이트 이상에
  걸치는 **큰 테이블에 특히 유익**하다 (같은 소절).[^strengholt2025]
- 저자는 liquid clustering이 Z-ordering과 파티셔닝의 장점을 합쳐 일부 시나리오를 넘겨받았지만,
  구성에 따라서는 Z-ordering이 여전히 유효할 수 있다고 단서를 단다 (같은 소절).[^strengholt2025]

### V-Ordering

- Z-ordering과 무엇이 다른가 — V-ordering은 **Parquet 파일 형식에 대한 쓰기 시점(write-time)
  최적화**다. Power BI의 VertiPaq 엔진이 쓰는 것과 같은 저장 알고리즘으로 데이터를 논리적으로
  조직해, Power BI·Warehouse 같은 Microsoft Fabric 컴퓨트 엔진에서 더 빠른 읽기를 가능하게 한다.
  **오픈 소스 Parquet 형식과 100% 호환**이라 모든 Spark 엔진이 보통의 Parquet로 읽을 수 있다
  (2장 §"Managing Delta Tables" ▸ "V-Ordering").[^strengholt2025]
- 수치 — 저자가 마이크로소프트 문서를 근거로 인용하는 이득은 엔진과 시나리오에 달렸으되 **평균 10%
  빠른 읽기, 일부 시나리오에서 최대 50% 개선**이다. 설정은 Delta 테이블 속성으로 하고 저자의 예는
  `CREATE TABLE person (id INT, name STRING, age INT) USING parquet TBLPROPERTIES("delta.parquet.vorder.enabled" = "true")`
  이다 (같은 소절).[^strengholt2025]
- **대가도 수치로 온다** — 정렬이 평균 쓰기 시간에 **15%** 영향을 줄 수 있다. 필요하면 끌 수 있고,
  쓰기 과정에 정렬 단계가 추가되는 것이 원인이라 **쓰기가 많고 읽기가 적을 때 문제**가 된다
  (같은 소절 — 이 수치의 출처로 저자가 각주 1에 바깥 블로그 글을 단다).[^strengholt2025]
- 그래서 저자의 처방은 전면 적용이 아니라 **계층별·사용 사례별 정렬**이다 — 예로 SQL 엔드포인트를
  많이 쓰는 사용 사례를 든다 (같은 소절).[^strengholt2025]

### 테이블 파티셔닝

- 하는 일과 적용 범위 — 파티셔닝은 **큰 테이블을 더 작고 다루기 쉬운 조각으로 나누어** 질의마다
  읽어야 할 데이터 양을 줄이는 전략이고, 통상 수백 기가바이트에서 수 테라바이트 크기의 데이터셋을
  겨냥한다. Delta Lake에서는 특정 열로 파티션하며 날짜 열이 흔한 선택이되 질의에 자주 쓰이는 어떤
  열이든 고를 수 있다(예: 국가로 자주 조회하면 국가 열). `PARTITIONED BY` 절에 열을 지정하고, 저자의
  예는 `CREATE TABLE events USING DELTA PARTITIONED BY (date)` 이다
  (2장 §"Managing Delta Tables" ▸ "Table Partitioning").[^strengholt2025]
- **둘을 함께 쓸 때의 제약이 이 소절의 실질이다** — 파티셔닝과 Z-ordering 모두 아주 큰 테이블에서
  가장 효과적이고, 둘을 결합할 수는 있으되 **Z-order 클러스터링은 파티션 안에서만 일어나며 같은
  필드를 두 기법에 함께 쓸 수 없다** (같은 소절).[^strengholt2025]

### liquid clustering

- 무엇을 푸는가 — Z-order와 파티셔닝을 최적으로 구현하는 일에는 도전과 맞교환이 따른다. **이
  최적화들은 고정된 데이터 배치를 요구하므로 사전 계획을 세심히 해야 한다.** 그 문제를 다루려고
  Delta Lake 프로젝트가 **2024년 중반** liquid clustering이라는 새 기능을 도입했고, 저자는 이것이
  **전통적 Z-ordering과 파티셔닝을 대체하게 되어 있다**고 적는다
  (2장 §"Managing Delta Tables" ▸ "Liquid Clustering").[^strengholt2025]
- 어떻게 다른가 — liquid clustering은 **클러스터링 키에 기반해 데이터 배치를 동적으로 적응시킨다.**
  Hive 방식 파티셔닝의 정적 배치와 달리 이 유연한("liquid") 배치는 변해 가는 질의 패턴에 반응해
  바뀌고, 그래서 최적이 아닌 파티셔닝과 열 카디널리티 문제를 다룬다. **증분 최적화를 적용하고 데이터를
  다시 쓰지 않고도 열을 재클러스터링할 수 있다** (같은 소절).[^strengholt2025]
  - 곧 파티셔닝·Z-ordering이 요구하던 **사전 계획이라는 비용을 없애는 것**이 이 기능의 값이다.

### 컴팩션과 최적화된 쓰기

- Delta Lake의 `OPTIMIZE` 연산은 **작은 파일 문제를 다루려고 만들어진 것**이라고 저자가 못 박는다.
  갱신·삭제·추가가 일어나면 Delta Lake가 그 변경을 더 작은 파일에 담고, 시간이 지나면 이 작은 파일들이
  쌓여 조회를 느리게 한다. 최적화 잡을 돌리면 작은 파일들을 더 크고 다루기 쉬운 파일로 컴팩션해 질의
  성능을 높이며, 명령은 `OPTIMIZE delta_table_name;` 이다
  (2장 §"Managing Delta Tables" ▸ "Compaction and Optimized Writes").[^strengholt2025]
- **최적화된 쓰기(optimized writes)가 다른 방향이다** — 기본값은 꺼져 있고 Delta Lake 3.1 이상에서
  `delta.autoOptimize.optimizeWrite` 테이블 속성을 `true`로 두면 켜진다. 켜면 Delta Lake가 **쓰기
  도중에** 데이터 파일 배치를 자동으로 최적화해 질의 성능을 높인다 (같은 소절).[^strengholt2025]
  - 버전 조건: Delta Lake 3.1 이상 — 저자가 이 기능의 활성화 가능 버전으로 명시한 경계다.
  - 이것도 공짜가 아니다 — V-ordering과 비슷하게 약간의 추가 부하가 생기고, **200만에서 500만 행을
    다루는 중간 규모 잡에서 5초에서 10초 정도의 지연이 더해질 것으로 예상**할 수 있다
    (같은 소절, 각주 2).[^strengholt2025]

### DeltaLog

- 정의 — Delta 트랜잭션 로그, 곧 DeltaLog는 **Delta 테이블 안의 데이터에 가해진 모든 변경을 꼼꼼히
  기록하는 트랜잭션 로그**이고 메달리온의 모든 계층에서 자주 쓰인다. 추가·`ALTER` 문·최적화 잡·수정·
  삭제가 다 들어가며, 테이블의 포괄적 이력을 유지하고 **Delta 테이블 디렉터리 안의 `_delta_log`
  디렉터리에 JSON 파일 여러 개로 저장된다**
  (2장 §"Managing Delta Tables" ▸ "DeltaLog").[^strengholt2025]
- 보존 — 트랜잭션마다 새 로그 파일이 생기고 수행된 액션·추가된 파일·제거된 파일 등 상세를 담는다.
  **기본 보존 임계는 7일**이고 `ALTER TABLE SET TBLPROPERTIES` 문으로 바꿀 수 있다
  (같은 소절).[^strengholt2025]
- 메달리온에서의 값 — 오류가 생기거나 특히 Silver·Gold에서 무결성이 훼손되면 **`RESTORE` 명령으로
  시각이나 버전 번호를 지정해 이전 버전으로 빠르게 되돌릴 수 있다.** 이것이 데이터 감사·롤백·실험과
  리포트의 재현을 받친다 (같은 소절).[^strengholt2025]
- 곁줄이 청소 쪽을 붙인다 — **`VACUUM` 문은 Delta가 관리하지 않는 파일을 제거하고, 테이블의 최신
  트랜잭션 로그 상태에 속하지 않으면서 지정된 보존 임계보다 오래된 데이터 파일을 지워 테이블
  디렉터리를 청소한다.** 저장을 효율적으로 유지하면서 비용 절감과 규정 준수도 돕는다
  (같은 소절 곁줄 note).[^strengholt2025]
- **이 소절에서 가장 중요한 것은 한계 규정이다** — DeltaLog의 주목적은 **데이터 복구와 감사**이지
  통상의 이력 데이터베이스 노릇이 아니다. 예컨대 지난 한 달 동안 바뀐 레코드를 트랜잭션 로그로
  찾아내려 하면 모든 파일을 읽어 변경을 비교해야 하므로 방대한 처리가 든다. **이력 변경을 추적하는 더
  효율적인 방법은 완만하게 변하는 차원 같은 방법으로 테이블 안에서 직접 관리하는 것**이다
  (같은 소절).[^strengholt2025]
  - 그 방법의 원전은 [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md)이다.
- 곁글이 이 절의 요지를 둘로 묶는다 — **V-ordering과 liquid clustering 같은 `*`-ordering 방법을
  아키텍처의 계층과 정렬시키되 각 계층의 질의와 접근 패턴에 초점을 맞추라**는 것과, **Delta 테이블의
  보존 임계를 신중히 정해 운영 필요와 복구 시나리오를 받치면서 데이터 신선도와 저장 비용의 균형을
  잡으라**는 것이다 (2장 §"Table Management Takeaway" 곁글).[^strengholt2025]

## 저자의 맺음 — 기초 단계를 과소평가하지 말 것

- 맺음의 첫 문장이 이 장 전체의 판정이다 — 기초 다지기는 **초기 전제 조건을 포괄적으로 이해하는
  데서 시작하는 꼼꼼한 과정**이고, 원천 시스템마다 저마다의 접근이 필요할 수 있어 **이 기초
  단계를 과소평가하지 않는 것이 중요하다** (2장 §"Conclusion").[^strengholt2025]
- 이 단계에서 해야 할 것은 원천 시스템 소유자와의 상세한 계획과 협업이다. 그 협업이 중개를 적용할지,
  추가 랜딩 존과 통합 런타임 부품을 쓸지, 배치와 실시간 중 무엇을 고를지를 정하게 해 주고, **이
  선택들은 저마다의 뉘앙스를 갖고 데이터 수집에 드는 작업량에 크게 영향을 준다**
  (2장 §"Conclusion").[^strengholt2025]
- 도구 쪽 맺음은 표준화를 가리킨다 — ETL·오케스트레이션 도구 선택이 초기 계층 설계를 좌우하고
  아키텍처 전반에 영향을 주므로 **표준화가 거버넌스·메타데이터 관리·계보 수집·일관된 데이터 품질
  보고에 결정적**이고, 이 결정이 메달리온 아키텍처의 유연성과 확장성에 영향을 준다
  (2장 §"Conclusion").[^strengholt2025]
- 테이블 관리도 뒤로 미룰 수 없다 — **테이블 관리와 데이터 모델링 접근은 긴밀히 연결되며 성능
  최적화에 필수적이고, 효과적인 테이블 관리 전략은 설계 과정의 이른 시점에 고려되어야** 아키텍처가
  의도한 데이터 부하를 효율적으로 감당한다 (2장 §"Conclusion").[^strengholt2025]
  - **이것이 이 페이지가 기초 조건과 테이블 관리를 한 자리에 두는 근거다** — 저자 자신이 둘을 같은
    "이른 시점의 결정"으로 묶는다.

## 이 KB의 원전과 맞대어 본 것

이 절은 각주 없는 KB 편저자의 대조다 — 2026년 KB 작성 시점에 이 KB가 이미 갖는 원전과 이 소스를
맞대어 본 결과이고, 소스가 한 말이 아니다.

### Delta 테이블 관리 기법과 konieczny2025의 패턴 카탈로그

같은 기법이 두 소스에서 **다른 이름과 다른 분류**로 온다. 어긋나는 것이 아니라 세는 축이 다르다.

| 이 소스가 부르는 이름 | 이 KB의 원전과 그 분류 | 갈리는 자리 |
|---|---|---|
| Z-Ordering | [데이터 저장 레이아웃 패턴](../concepts/data-storage-layout-patterns.md)의 **Sorter 패턴** 아래 Z-order | konieczny는 Z-order를 "클러스터링 맥락에서도 참조되지만 실은 디스크에서 데이터를 정렬하므로 Sorter"라고 분류한다. 스트렝홀트는 분류하지 않고 "관련 정보를 같은 파일에 모으는 기법"이라 서술한다. **같은 기법의 다른 이름이 아니라 같은 기법의 다른 계보 배치다** |
| 테이블 파티셔닝 | 같은 페이지의 **Horizontal Partitioner** | konieczny는 저카디널리티 규칙·스큐·분할 키 변경 비용까지 파고들고, 스트렝홀트는 크기 기준(수백 GB 이상)과 Z-order 병용 제약만 남긴다 |
| liquid clustering | **원전이 없다** | 이 기법은 konieczny의 8장 카탈로그에 나오지 않는다. 두 소스가 같은 2025년인데 한쪽에만 있으므로 이것은 **이 소스가 더하는 것**이다 |
| 컴팩션(`OPTIMIZE`) | [작은 파일 문제와 컴팩션](../concepts/small-files-and-compaction.md)의 **Compactor 패턴** | 명령도 목적도 같다. konieczny는 **컴팩션만으로는 부족하고 청소 잡이 따라야 한다**는 결과를 덧붙이고, 스트렝홀트는 그 청소를 DeltaLog 소절의 `VACUUM`으로 따로 놓는다. 둘을 이으면 같은 그림이 된다 |
| 최적화된 쓰기 | **원전이 없다** | Compactor 패턴은 **쓰인 뒤 되감는** 쪽만 다룬다. `delta.autoOptimize.optimizeWrite`는 **쓰는 도중에 막는** 쪽이라 방향이 반대다 |
| DeltaLog | [트랜잭션과 ACID](../concepts/acid-transactions.md)·[읽기 경로 최적화 패턴](../concepts/read-path-optimization-patterns.md)의 Metadata Enhancer | 트랜잭션 로그가 ACID를 받치는 쪽과 커밋 로그 통계가 파일을 걸러 주는 쪽 둘 다에 걸린다. 이 소스가 더하는 것은 **보존 임계 7일**과 **이력 데이터베이스가 아니라는 한계 규정**이다 |

- **수치가 겹치지 않는다는 점도 기록해 둔다.** 스트렝홀트는 Z-ordering을 "보통 조회보다 두 배에서
  네 배"로 적고, konieczny는 한 술어 예제에서 "사전식 아홉 블록 대 Z-order 일곱 블록"으로 적는다.
  #hypothesis 둘은 다른 것을 재고 있어 서로를 부정하지 않는다 — 앞은 조회 효율의 총평이고 뒤는 한
  술어에서 읽은 블록 수다.

### 그 밖의 대조 — 전부 모순 아님으로 판정

- **원시 데이터의 불변성.** 이 소스는 중개와 전처리가 **첫 계층에 닿기 전에** 일어나며 메달리온 안의
  변환이 아니라고 규정한다. [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md)와
  [수명 주기의 저장 단계](../concepts/storage-in-the-lifecycle.md)가 세우는 불변 원시 층 원칙과
  부딪히지 않는다 — 원칙은 착지 **이후**의 불변을 말하고 이 소스는 착지 **이전**의 경계를 긋는다.
  같은 축의 다른 구간이라 `contradicts` 대상이 아니다.
- **change data feed와 CDC의 관계.** [변경 데이터 캡처](../concepts/change-data-capture.md)는 CDC를
  원천 데이터베이스를 리더로 만들고 나머지를 팔로워로 바꾸는 기제로 규정하고, 같은 페이지가 배치
  CDC(`updated_at` 질의 기반)와 연속 CDC(로그 기반)를 가른다. 이 소스의 표 2-1은 CDC를 **트랜잭션
  로그 기반**으로만 서술하므로 그 규정보다 좁다. 그러나 이것은 좁힌 서술이지 반대 주장이 아니고,
  change data feed 쪽은 **감시 대상이 Delta 테이블**이라 애초에 다른 지점이다 — 두 이름이 붙어
  보이지만 겨루지 않는다.
  - **저자가 미뤄 둔 상세가 5장에서 오고 표 2-1을 뒤집지 않는다.** 그 장은 CDC를 다시
    "삽입·갱신·삭제 같은 변경을 포착해 별도 테이블에 저장하는 것"으로 규정하고 실시간 복제를 주된
    쓰임으로 든다. 표 2-1이 CDC에 준 칸과 같은 자리다 (5장 §"Implementation of Lakehouse Tables" ▸
    "Using Change Data Capture").[^strengholt2025]
  - **분업도 5장이 그대로 되풀이한다** — 곁줄 하나가 change data feed를 CDC 기제에 **더해서** 쓰면
    복제 효율이 크게 오른다고 적어, 표 2-1이 그린 "겨루지 않는 셋"을 재확인한다 (같은 소절
    곁줄).[^strengholt2025] 5장이 더하는 것은 **미러링이라는 구현 이름**과 **운영 비용 다섯**이고,
    그것은 [Bronze 계층 구현](../concepts/bronze-layer-implementation.md)에 있다.
- **배치와 실시간의 선택 기준.** [수명 주기의 반입 단계](../concepts/ingestion-in-the-lifecycle.md)가
  "스트리밍 우선을 고르기 전에" 던지는 물음들과 이 소스의 기준(실시간은 애플리케이션 아키텍처 수정과
  always on 컴퓨트를 요구한다)은 같은 방향을 가리킨다. [배치 처리의 기본](../concepts/batch-processing-basics.md)이
  세우는 정의와도 어긋나지 않는다.
- **랜딩 존과 스테이징 영역.** [스테이징 영역](../concepts/staging-area.md)은 적재가 끝나면 비우는
  일시적 완충으로 규정되고, 이 소스의 랜딩 존은 비움 규칙 없이 원천 특성과 팀 경계로 정당화된다.
  **같은 이름을 두 아키텍처가 다르게 쓰는 것**이라 사실 충돌이 아니다.

곧 이 런은 `contradicts`를 하나도 걸지 않는다.

## 이어지는 페이지

- [메달리온 아키텍처의 정의와 계보](../concepts/medallion-architecture-origins.md) — Bronze·Silver·
  Gold 셋의 정의. 이 페이지가 잇는 자리
- [스테이징 영역](../concepts/staging-area.md) — 랜딩 존이 웨어하우스 쪽에서 불리던 이름
- [데이터 레이크](../concepts/data-lake.md) — 랜딩 존과 Bronze가 놓이는 저장
- [수명 주기의 반입 단계](../concepts/ingestion-in-the-lifecycle.md) — 배치와 실시간을 가르는 여덟 축
- [배치 반입 패턴](../concepts/batch-ingestion-patterns.md) — 배치로 정한 뒤 남는 결정들
- [배치 처리의 기본](../concepts/batch-processing-basics.md) — 배치를 배치라 부르는 근거
- [변경 데이터 캡처](../concepts/change-data-capture.md) — 표 2-1의 셋째 칸이 가리키는 기제의 원전
- [스트리밍 질의와 변환](../concepts/streaming-queries-and-transformations.md) — Structured Streaming이
  하는 일의 일반형
- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) ·
  [분산 잡 오케스트레이션](../concepts/distributed-job-orchestration.md) — Airflow·Data Factory가
  사는 층
- [데이터 저장 레이아웃 패턴](../concepts/data-storage-layout-patterns.md) — Z-order와 파티셔닝을
  패턴으로 분류한 쪽
- [작은 파일 문제와 컴팩션](../concepts/small-files-and-compaction.md) — `OPTIMIZE`가 푸는 문제의 원전
- [읽기 경로 최적화 패턴](../concepts/read-path-optimization-patterns.md) — 커밋 로그 통계가 파일을
  걸러 주는 쪽
- [다차원 색인](../concepts/multidimensional-indexes.md) — Z-ordering이 기대는 다차원 조회의 원리
- [트랜잭션과 ACID](../concepts/acid-transactions.md) — DeltaLog가 받치는 네 글자
- [완만하게 변하는 차원(SCD)](../concepts/slowly-changing-dimension.md) — DeltaLog가 대신하지 못한다고
  저자가 지목한 방법
- [기록 시스템과 파생 데이터](../concepts/system-of-record-and-derived-data.md) ·
  [수명 주기의 저장 단계](../concepts/storage-in-the-lifecycle.md) — 원시 층의 불변을 세우는 쪽
- [메달리온 아키텍처 구축](../synthesis/building-medallion-architectures.md) — **이 페이지가
  걸린 허브.** 이 원전의 스물두 페이지가 부 단위로 모여 있다
- [데이터 엔지니어링 수명 주기](../synthesis/data-engineering-lifecycle.md) — 그 허브의 부모 축

[^strengholt2025]: Piethein Strengholt, *Building Medallion Architectures: Designing with Delta
    Lake and Spark*, O'Reilly 2025 ([소스](../sources/strengholt2025.md)). 스냅샷이 EPUB이고
    **인쇄판 쪽 앵커가 없어** locator는 장·절 단위다 — `N장 §"절 제목"`(원문 절 제목 그대로),
    소절은 `▸`로 잇고 곁글은 제목 뒤에 `곁글`을 붙인다. 2장 실측: 절(`sect1`) 여덟 · 소절(`sect2`)
    열 · 소소절 없음 · 곁글 다섯(전부 "… Takeaway" 꼴이고 장 요지의 정본이다) · 곁줄 셋
    (warning 하나 · note 둘) · 표 하나(표 2-1) · 도판 없음 · SQL 코드 목록 다섯 · 각주 둘
    (`<sup>` 넷은 마커 둘과 되돌아가는 링크 둘이다). **SQL 다섯은 펜스 없이 인라인으로 옮겼고**
    지면 폭 때문에 접힌 줄을 한 줄로 이은 것 말고는 원문 그대로다 — 보탠 줄은 없다.

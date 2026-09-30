---
type: concept
title: 데이터베이스 종류 고르기
description: 쪼갠 데이터 도메인마다 어떤 종류의 데이터베이스에 담을 것인가 — 2005년 이후 제품 폭증이 만든 선택의 역설과 종류를 채점하는 일곱 축(학습 난이도·데이터 모델링 난이도·확장성과 처리량·가용성과 파티션 내성·일관성·언어 지원과 성숙도·읽기 쓰기 우선)의 원문 규정, 관계형·키-값·문서·컬럼 패밀리·그래프·NewSQL·클라우드 네이티브·시계열 여덟 갈래 각각의 별점 표와 제품 목록, NoSQL 계열을 하나로 묶는 애그리게이트 지향의 규정과 이점 셋 대가 둘, 샤딩과 스키마 없음과 관계 유형 바꾸기라는 곁상자 셋, 별점이 저자들의 2021년 판단이라는 조건과 도판과 본문이 어긋나는 자리 셋, 그리고 설문 데이터를 문서 데이터베이스로 옮기는 책의 사례와 그 ADR, 그리고 같은 저자 무리의 2025년 책이 이 채점을 아홉 교차점 가운데 데이터 토폴로지의 자리에서 불러내며 토폴로지 셋과 종류의 초능력을 아키텍처의 초능력과 맞추라는 조문과 데이터 구조·읽기 쓰기 우선이라는 축 둘을 얹는 자리, 그리고 그 호명이 이 페이지의 여덟 갈래를 여섯으로 줄여 적으면서 계열의 이름인 NoSQL을 갈래 자리에 넣고 자기 목록에 없는 NewSQL을 두 문단 뒤에 쓰는 어긋남
generated: { by: "claude-opus-5", at: "2026-09-29T22:20:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: richards2025, resource: /it/sources/richards2025.md }
---

# 데이터베이스 종류 고르기

- [버전 조건](#버전-조건)
- [이 페이지가 무엇이고 무엇이 아닌가](#이-페이지가-무엇이고-무엇이-아닌가)
- [선택의 역설](#선택의-역설)
- [채점의 축 일곱](#채점의-축-일곱)
- [별점을 어떻게 읽을 것인가](#별점을-어떻게-읽을-것인가)
- [관계형](#관계형)
- [애그리게이트 지향](#애그리게이트-지향)
- [키-값](#키-값)
- [곁상자 — 데이터베이스의 샤딩](#곁상자--데이터베이스의-샤딩)
- [문서](#문서)
- [곁상자 — 스키마 없는 데이터베이스](#곁상자--스키마-없는-데이터베이스)
- [컬럼 패밀리](#컬럼-패밀리)
- [그래프](#그래프)
- [곁상자 — 관계 유형 바꾸기](#곁상자--관계-유형-바꾸기)
- [NewSQL](#newsql)
- [클라우드 네이티브](#클라우드-네이티브)
- [시계열](#시계열)
- [종류와 제품의 요약표](#종류와-제품의-요약표)
- [도판과 본문이 어긋나는 자리](#도판과-본문이-어긋나는-자리)
- [이 선택이 데이터 분해의 어디에 놓이는가](#이-선택이-데이터-분해의-어디에-놓이는가)
- [책의 사례 — 폴리글랏 데이터베이스](#책의-사례--폴리글랏-데이터베이스)
- [2025년 원전이 이 채점을 교차점으로 다시 부르는 자리](#2025년-원전이-이-채점을-교차점으로-다시-부르는-자리)
- [이 KB의 데이터 모델 페이지들과 겹치는 자리](#이-kb의-데이터-모델-페이지들과-겹치는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **쪼갠 데이터 도메인마다 어떤 종류의 데이터베이스에 담을 것인가.**

## 버전 조건

> **버전 조건**: 2021년 저술 시점. 이 페이지의 별점은 전부 저자 네 사람이 그 시점에 내린
> 판단이고 측정값이 아니다. 제품 목록도 그 시점의 것이다. **종류를 가르는 축 일곱과 종류
> 사이의 상대적 자리는 오래 가는 부분이고, 낱낱의 별 수와 제품 이름은 빨리 낡는 부분이다** —
> 이 페이지는 둘을 섞지 않고 축과 제품을 나누어 적는다.

## 이 페이지가 무엇이고 무엇이 아닌가

- **이 페이지가 갖는 것은 아키텍처 쪽의 선택 틀**이다 — 쪼갠 데이터 도메인 하나하나에 어떤
  종류를 붙일 것인가를 무엇으로 판정하는가, 그리고 그 판정을 위해 저자들이 세운 채점 축이
  무엇인가.
- **데이터 모델 자체의 설명은 이 페이지가 갖지 않는다.** 관계형과 문서의 대결은
  [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md)이, 그래프 질의는
  [그래프 질의 언어](../concepts/graph-query-languages.md)와
  [그래프 데이터 모델](../concepts/graph-data-models.md)이, 시계열은
  [시계열 데이터베이스](../concepts/time-series-databases.md)가, 열 지향 배치는
  [열 지향 저장](../concepts/column-oriented-storage.md)이 갖는다. 이 페이지는 그것들을 다시
  설명하지 않고 **선택 시점의 채점표**만 갖는다.

## 선택의 역설

- **왜 이 절이 필요해졌는가** — **2005년 무렵부터 데이터베이스 기술에 혁명이 일어났다. 불행히도
  이 기간에 등장한 제품의 수가 선택의 역설(The Paradox of Choice)이라는 문제를 만들었다** (6장,
  p.161).[^ford2021-hard-parts]
- **제품이 많다는 것은 판정할 절충이 많다는 뜻이다** — **그렇게 많은 수의 제품과 선택지를
  갖는다는 것은 내려야 할 절충 결정이 더 많다는 뜻이다. 각 제품이 특정 절충에 최적화돼 있으므로,
  자기 문제 공간과 관련해 그 절충을 염두에 두고 적절한 제품을 고르는 일은 소프트웨어 아키텍트와
  데이터 아키텍트 양쪽에 달려 있다** (6장, p.161).[^ford2021-hard-parts]
  - **고르는 주체를 둘로 적는 것이 이 책의 자리다.** 소프트웨어 아키텍트만도 데이터 아키텍트만도
    아니다. 6장 전반의 사가가 그 둘이 갈라섰다가 합의에 이르는 장면이었고, 이 절의 사가도 같은
    구도로 되돌아온다.

## 채점의 축 일곱

- **저자들이 여덟 갈래를 같은 일곱 축으로 채점한다** — **이 절에서 우리는 여러 데이터베이스
  종류에 대한 별점을 도입하며, 우리 분석에서 다음 특성들을 쓴다** (6장,
  p.161).[^ford2021-hard-parts] 일곱 축의 규정을 원문 그대로 옮긴다 (6장, pp.161–162):

  > *Ease-of-learning curve*
  >
  > This characteristic refers to the ease with which new developers, data architects, data
  > modelers, operational DBAs, and other users of the databases can learn and adopt. For
  > example, it's assumed that most software developers understand SQL, whereas something
  > like Gremlin (a graph query language) may be a niche skill. The higher the star rating,
  > the easier the learning curve. The lower the star rating, the harder the learning curve.
  >
  > *Ease of data modeling*
  >
  > This characteristic refers to the ease with which data modelers can represent the domain
  > in terms of a data model. A higher star rating means data modeling matches many use
  > cases, and once modeled, is easy to change and adopt.
  >
  > *Scalability/throughput*
  >
  > This characteristic refers to the degree and ease with which a database can scale to
  > handle increased throughput. Is it easy to scale the database? Can the database scale
  > horizontally, vertically, or both? A higher star rating means it's easier to scale and
  > get higher throughput.
  >
  > *Availability/partition tolerance*
  >
  > This characteristic refers to whether the database supports high availability
  > configurations (such as *replica-sets* in MongoDB or *tunable consistency* in Apache
  > Cassandra). Does it provide features to handle network partitions? The higher the star
  > rating, the better the database supports higher availability and/or better partition
  > tolerance.
  >
  > *Consistency*
  >
  > This characteristic refers to whether the database supports an "always consistent"
  > paradigm. Does the database support ACID transactions, or does it lean toward BASE
  > transactions with an eventual consistency model? Does it provide features to have
  > tunable consistency models for different types of writes? The higher the star rating,
  > the more consistency the database supports.
  >
  > *Programming language support, product maturity, SQL support, and community*
  >
  > This characteristic refers to which (and how many) programming languages the database
  > supports, how mature the database is, and the size of the database community. Can an
  > organization easily hire people who know how to work with the database? Higher star
  > ratings means there is better support, the product is mature, and it's easy to hire
  > talent.
  >
  > *Read/write priority*
  >
  > This characteristic refers to whether the database prioritizes reads over writes, or
  > writes over reads, or if it is balanced in its approach. This is not a binary
  > choice—rather, it's more of a scale toward which direction the database optimizes.

- **일곱 중 여섯만 별점이고 하나는 눈금이다.** 읽기 쓰기 우선은 별이 아니라 **읽기에서 쓰기로
  가는 띠 위의 표식**으로 조판된다. 저자들이 그 차이를 규정 안에 미리 적어 둔다 — **이것은
  이진 선택이 아니라 데이터베이스가 어느 방향으로 최적화하는가의 눈금에 가깝다**.
- **여섯째 축이 기술 특성이 아니라 인력 시장이다.** 언어 지원·성숙도·SQL 지원·커뮤니티가 한
  칸에 묶이고, 그 칸이 묻는 것은 **그 데이터베이스를 다룰 줄 아는 사람을 조직이 쉽게 채용할 수
  있는가**다. 나머지 여섯 축이 제품의 성질을 재는 데 반해 이 축만 **조직의 조건**을 잰다.
- **넷째 축과 다섯째 축이 CAP의 두 낱말을 그대로 쓴다.** 그러나 저자들은 이 절에서 CAP 정리를
  설명하지 않고 9장으로 넘긴다 — 컬럼 패밀리 절 끝에서 **CAP 정리의 개념은 254쪽
  §"Table Split Technique"에서 더 길게 다룬다**고 적고, 관계형의 가용성 항목에서도 같은 자리를
  가리킨다 (6장, pp.164·171).[^ford2021-hard-parts] 그 어휘의 정본은
  [CAP과 PACELC](../concepts/cap-and-pacelc.md)다.

## 별점을 어떻게 읽을 것인가

- **만점은 별 다섯이다.** 여덟 도판 전부가 같은 일곱 행을 쓰고 최대값이 5다.
- **도판의 행 이름이 규정 목록의 이름과 조금 다르다.** 규정 목록은
  `Ease-of-learning curve`·`Programming language support, product maturity, SQL support, and
  community`인데 도판의 행은 `Ease of learning`·`Programming language support, product
  maturity, SQL support, community`다(`curve`가 빠지고 `and`가 빠진다). 아래 표는 **도판의
  이름**을 쓴다.
- **별점은 텍스트 레이어에 없다.** 이 KB는 여덟 도판을 전부 렌더해 눈으로 세어 옮겼고, 읽기
  쓰기 눈금의 표식 자리는 렌더에서 픽셀 위치를 재어 **읽기 쪽·가운데·쓰기 쪽** 셋으로 적었다.
  원문에 수치 눈금이 없으므로 그보다 더 잘게 적지 않는다.
- **비교는 종류 사이에서만 뜻이 있다.** 저자들이 절대 기준을 대지 않으므로 "문서가 3점"이라는
  말은 "같은 축에서 컬럼 패밀리(1점)보다 위고 관계형(3점)과 같다"는 뜻으로만 읽는다.

## 관계형

- **무엇인가** — 관계형 데이터베이스(RDBMS)는 **30년 넘게 선택되어 온 데이터베이스**이고,
  **어디에나 있는 SQL과 그것이 제공하는 ACID 속성**으로 알려져 있다. **그것이 제공하는 SQL
  인터페이스가 같은 쓰기 모델 위에 서로 다른 읽기 모델을 구현하는 데 선호되는 선택이 되게
  만든다** (6장, p.163).[^ford2021-hard-parts]

  | 채점 항목 | RDBMS databases (Oracle, SQL Server, Postgres, etc.) |
  |---|---|
  | Ease of learning | 4/5 |
  | Ease of data modeling | 3/5 |
  | Scalability/throughput | 2/5 |
  | Availability/partition tolerance | 1/5 |
  | Consistency | 5/5 |
  | Programming language support, product maturity, SQL support, community | 4/5 |
  | Read/write priority | 가운데 |

- **일관성이 이 표에서 유일한 만점이고, 가용성이 유일한 1점이다.** 저자들이 그 둘을 한 문장으로
  잇는다 — **관계형 데이터베이스는 가용성과 파티션 내성보다 일관성을 선호한다** (6장,
  p.164).[^ford2021-hard-parts]
- **모델링 점수가 중간인 이유를 저자들이 양면으로 적는다** — 관계형은 **키-값·문서·그래프 같은
  구조의 모델링을 허용하고 새 인덱스를 더해 읽기 패턴의 변경도 허용하지만**, **임의 깊이의 그래프
  구조처럼 정말 달성하기 어려운 모델도 있다** (6장, p.163).[^ford2021-hard-parts]
- **확장 점수가 낮은 이유는 수직 확장이다** — **일반적으로 큰 기계를 써서 수직으로 확장되며,
  복제와 자동 전환을 갖춘 설정은 복잡하고 더 높은 조율과 셋업을 요구한다** (6장,
  p.164).[^ford2021-hard-parts]
- **성숙도 점수에 단서가 붙는다** — 관계형 제품 다수가 **리액티브 스트림 API 같은 새로운 개념의
  지원이 없고, 새 아키텍처 개념은 잘 확립된 관계형 데이터베이스에서 구현되는 데 더 오래
  걸린다**. 커뮤니티는 크지만 **모든 벤더에 걸쳐 쪼개져 있다** (6장,
  p.164).[^ford2021-hard-parts]
- **저자들이 드는 제품** — MySQL·Oracle·Microsoft SQL Server·PostgreSQL이고, **단독 설치로
  돌리거나 주요 클라우드 제공자 플랫폼에서 서비스형 데이터베이스(Database as a Service)로 쓸 수
  있다** (6장, p.164).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 목록이다. **본문의 목록과 도판 머리글과 요약표(표 6-6)의
    목록이 서로 다르다** — 아래 [도판과 본문이 어긋나는 자리](#도판과-본문이-어긋나는-자리)에
    적었다.

## 애그리게이트 지향

**이 절의 곁상자 하나가 뒤따르는 NoSQL 네 갈래를 한 낱말로 묶는다.** 별점표를 읽을 때 그 넷의
모델링·확장·읽기 우선 점수가 왜 같은 방향으로 움직이는지가 여기서 나온다.

- **규정** (6장, p.165, 곁상자 "Aggregate Orientation"):[^ford2021-hard-parts]

  > *Aggregate orientation* is the preference to operate on data that is related and has a
  > complex data structure. Aggregate is a term originated in *Domain-Driven Design:
  > Tackling Complexity in the Heart of Software* by Erik Evans.

  - **원문이 에반스의 이름을 `Erik Evans`로 적는다** — 그 책의 저자는 Eric Evans다. 원문 오식을
    그대로 옮기고 여기 표시한다. 그 개념의 정본은
    [애그리게이트와 정합성 경계](../concepts/aggregates-and-consistency-boundaries.md)다.
- **이점 셋과 대가 둘을 저자들이 원문 그대로 목록으로 적는다** (6장,
  p.165):[^ford2021-hard-parts]

  > *Benefits*
  >
  > - Enables easy distribution of data in clusters of servers, as the whole aggregate can
  >   be copied over to different servers.
  >
  > - Improves read and write performance, as it reduces joins in the database.
  >
  > - Reduces impedance mismatch between the application model and storage model.
  >
  > *Shortcomings*
  >
  > - It's difficult to arrive at proper aggregates, and changing aggregate boundaries is
  >   hard.
  >
  > - Analyzing data across aggregates is difficult.

- **이 낱말이 여덟 갈래 중 넷을 가른다** — 저자들이 컬럼 패밀리 절 끝에서 범위를 명시한다.
  **모든 NoSQL 데이터베이스는 애그리게이트 지향을 이해하도록 설계됐다. 애그리게이트를 갖는
  것이 읽기와 쓰기 성능을 개선하고, 데이터베이스를 클러스터로 돌릴 때 더 높은 가용성과 파티션
  내성도 가능하게 한다** (6장, p.171).[^ford2021-hard-parts]
- **대가 쪽 둘이 이 장의 다른 판정과 맞물린다.** 애그리게이트 경계를 바꾸기 어렵다는 것은
  [데이터 분해의 구동 요인](../concepts/data-decomposition-drivers.md)의 변경 통제와 같은 물음이고,
  애그리게이트를 가로지르는 분석이 어렵다는 것은
  [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md)의 리포팅 문제와 같은 물음이다.

## 키-값

- **무엇인가** — 키-값 데이터베이스는 **해시 테이블 자료 구조와 비슷하고**, RDBMS로 치면 **ID
  열을 키로 blob 열을 값으로 갖는 테이블** 같아서 **어떤 종류의 데이터든 담을 수 있다**. 이
  갈래는 **NoSQL 데이터베이스라 알려진 계열의 일부**다 (6장, p.165).[^ford2021-hard-parts]
- **데이터베이스가 값 안을 모른다** — **키-값 데이터베이스는 값 부분 안에 무엇이 있는지 모르고
  신경 쓰지도 않으며, 이는 데이터베이스가 키로만 질의할 수 있다는 뜻이다.** 지원되는 연산은
  `get`·`put`·`delete`이고 **조인·`where`·`order by` 같은 관계형 구성물은 지원되지
  않는다** (6장, p.165).[^ford2021-hard-parts]

  | 채점 항목 | Key value databases (Redis, DynamoDB, Riak, etc.) |
  |---|---|
  | Ease of learning | 3/5 |
  | Ease of data modeling | 1/5 |
  | Scalability/throughput | 4/5 |
  | Availability/partition tolerance | 4/5 |
  | Consistency | 2/5 |
  | Programming language support, product maturity, SQL support, community | 3/5 |
  | Read/write priority | 읽기 쪽 |

- **모델링 1점의 근거는 키를 밖에서 알아야 한다는 조건**이다 — **데이터는 키나 ID로만 질의될 수
  있고, 이는 클라이언트가 데이터베이스 바깥에서 그 키에 접근할 수 있어야 한다는 뜻이다.** 좋은
  키의 예로 `session_id`·`user_id`·`order_id`를 든다 (6장, p.166).[^ford2021-hard-parts]
- **가용성과 일관성이 설정으로 움직인다** — 리악(Riak)에서는 `all`·`one`·`quorum`·`default`
  같은 **정족수(quorum) 속성**을 쓸 수 있고, **질의마다 파티션 내성과 가용성을 조율할 수
  있다.** 그래서 **모든 키-값 저장소가 같다고 가정하는 것은 실수다** (6장,
  pp.166–167).[^ford2021-hard-parts]
  - 쓰기 쪽에도 같은 설정이 있고 그것을 **조율 가능한 일관성(tunable consistency)**이라 부른다.
    **더 높은 일관성은 지연을 내주고 얻을 수 있다. 쓰기가 매우 일관되려면 모든 노드가 응답해야
    하고 그것이 파티션 내성을 줄인다. 과반수 정족수(majority quorum)를 쓰는 것이 좋은 절충으로
    여겨진다** (6장, p.167).[^ford2021-hard-parts] 그 기제의 정본은
    [정족수 읽기와 쓰기](../concepts/quorum-reads-and-writes.md)다.
- **저자들이 이 갈래를 "필요에 따라 고르라"고 적는다** — **관계형 데이터베이스와 달리 키-값
  데이터베이스는 필요에 근거해 골라야 한다**. 영속적인 것(Amazon DynamoDB·Riak KV), 비영속적인
  것(MemcacheDB), 설정으로 갈리는 것(Redis)이 한 이름 아래 있다 (6장,
  p.165).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 구분이다.
- **저자들이 이 갈래의 참고 문헌으로 자기 책을 든다** — 사달게이(Pramod Sadalage, 이 책의 저자
  중 하나)와 마틴 파울러의 *NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot
  Persistence*(Addison-Wesley)가 **NoSQL의 부상과 그 동기·쓰임·절충을 서술하며 이 종류에 대한
  더 깊은 정보의 좋은 참조원**이라는 것이다 (6장, p.165).[^ford2021-hard-parts]
  - **이 책이 "폴리글랏 영속성"이라는 낱말을 어디서 들여왔는지가 여기 드러난다.** 이 절의
    사가 제목도 그 계보 위에 있다.

## 곁상자 — 데이터베이스의 샤딩

- **파티셔닝과 샤딩을 가른다** (6장, p.167, 곁상자 "Sharding in
  Databases"):[^ford2021-hard-parts]

  > The concept of partitioning is well-known in relational databases: the table data is
  > partitioned into sets based on a *schema* on the same database server. *Sharding* is
  > similar to partitioning, but data resides on different servers or nodes. Nodes
  > collaborate to figure out where data exists or where data should be stored based on a
  > sharding key. The word *shard* means horizontal partition of data in a database.

  - **가르는 잣대가 "같은 서버인가 다른 서버인가" 하나다.** 그 기제의 정본은
    [데이터 샤딩](../synthesis/data-sharding.md) 축이다.

## 문서

- **무엇인가** — **JSON이나 XML 같은 문서가 문서 데이터베이스의 기반**이고, 문서는 **사람이 읽을
  수 있고 자기 서술적이며 계층적인 트리 구조**다. **이 데이터베이스들은 데이터의 구조를 이해하며
  문서의 여러 속성을 인덱싱할 수 있어 더 나은 질의 유연성을 허용한다** (6장,
  p.167).[^ford2021-hard-parts]

  | 채점 항목 | Document databases (MongoDB, CouchDB, Marklogic, etc.) |
  |---|---|
  | Ease of learning | 3/5 |
  | Ease of data modeling | 3/5 |
  | Scalability/throughput | 2/5 |
  | Availability/partition tolerance | 3/5 |
  | Consistency | 2/5 |
  | Programming language support, product maturity, SQL support, community | 3/5 |
  | Read/write priority | 읽기 쪽 |

- **키-값에서 모델링 점수만 1점에서 3점으로 오른다** — 저자들이 그 차이를 애그리게이트 설계의
  관용도로 설명한다. **문서 데이터베이스는 애그리게이트 설계에 관대한데, 애그리게이트의
  부분들이 질의 가능하고 인덱싱될 수 있기 때문이다** (6장, p.168).[^ford2021-hard-parts]
  키-값 쪽은 반대로 **애그리게이트의 어떤 변경이든 모든 데이터를 다시 쓴다는 뜻**이라 설계를
  제대로 해야 한다 (6장, p.166).[^ford2021-hard-parts]
- **확장 점수가 2점인 이유는 인덱싱과 샤딩이다** — **복잡한 인덱싱이 확장성을 줄이고, 데이터
  크기가 커지면 파티셔닝이나 샤딩이 필요해진다. 샤딩이 도입되면 복잡도가 늘고 샤딩 키의 선택도
  강요된다** (6장, p.168).[^ford2021-hard-parts]
- **일관성이 컬렉션 안으로 한정된다** — **일부 문서 데이터베이스가 컬렉션 안에서 ACID 트랜잭션을
  지원하기 시작했지만 어떤 엣지 케이스에서는 동작하지 않을 수 있다** (6장,
  p.169).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 기능이다. 저자들이 어느 제품이 어디까지 지원하는지를
    적지 않는다.
- **이 갈래가 NoSQL 중 가장 대중적이라고 적는다** — **활발한 사용자 커뮤니티와 수많은 온라인
  학습 자료와 많은 언어 드라이버를 갖춰 채택이 더 쉽다** (6장, p.169).[^ford2021-hard-parts]

## 곁상자 — 스키마 없는 데이터베이스

- **저자들이 "스키마 없음"이라는 표현에 제동을 건다** (6장, p.169, 곁상자 "Schema-less
  Databases"):[^ford2021-hard-parts]

  > One common theme in NoSQL databases is duplication of data and schema attribute names.
  > No two entries have to be the same in terms of schema or attribute names. This
  > introduces interesting change control dynamics and provides flexibility. The schema-less
  > nature of the database is powerful, but it's important to understand that the data
  > always has a schema even if it's implicit or defined elsewhere. The application needs to
  > handle multiple versions of the schema returned by a database. The claim that NoSQL
  > databases are entirely schema-less is misleading.

  - **결론 문장이 이 절의 유연성 논거에 조건을 단다** — 스키마가 사라지는 것이 아니라 **암묵이
    되거나 다른 곳에 정의될 뿐**이고, 그 대가를 **여러 판의 스키마를 다룰 애플리케이션**이
    치른다. 같은 판정을 데이터 쪽 어휘로 적은 자리는
    [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md)다.

## 컬럼 패밀리

- **무엇인가** — **컬럼 패밀리 데이터베이스(column family databases)는 와이드 컬럼
  데이터베이스(wide column databases) 또는 빅 테이블 데이터베이스(big table databases)라고도
  하며, 열의 수가 제각각인 행들을 갖고 각 열은 이름-값(name-value) 쌍이다.** 이름은
  **컬럼 키(column-key)**, 값은 **컬럼 값(column-value)**, 행의 기본 키는 **행 키(row key)**라
  부른다. 이 갈래는 **동시에 접근되는 관련 데이터를 묶는** NoSQL의 한 종류다 (6장,
  p.169).[^ford2021-hard-parts]

  | 채점 항목 | Column family databases (Cassandra, Scylla, Druid, etc.) |
  |---|---|
  | Ease of learning | 2/5 |
  | Ease of data modeling | 1/5 |
  | Scalability/throughput | 4/5 |
  | Availability/partition tolerance | 4/5 |
  | Consistency | 1/5 |
  | Programming language support, product maturity, SQL support, community | 2/5 |
  | Read/write priority | 쓰기 쪽 |

- **여덟 갈래 가운데 읽기 쓰기 눈금이 쓰기 쪽으로 간 유일한 갈래다.** 나머지 일곱은 읽기 쪽
  아니면 가운데다. 저자들이 그 근거로 **SSTable·커밋 로그·멤테이블(memtables)**이라는 내부
  구조와 **이름-값 쌍이 데이터가 있을 때만 채워지므로 관계형보다 희소 데이터를 훨씬 잘
  다룬다**는 것을 들고, **높은 쓰기 볼륨 시나리오에 이상적**이라고 적는다 (6장,
  p.171).[^ford2021-hard-parts]
- **가용성 4점의 근거가 기본 복제 계수다** — **컬럼 패밀리 데이터베이스는 자연히 클러스터로
  동작하며 클러스터의 일부 노드가 내려가도 클라이언트에게 투명하다. 기본 복제 계수는 셋이고,
  이는 데이터의 사본이 적어도 셋 만들어진다는 뜻이라 가용성과 파티션 내성을 개선한다** (6장,
  p.170).[^ford2021-hard-parts]
- **일관성 1점은 조율 가능한 일관성의 반대쪽 끝이다** — 쓰기 일관성 수준 `ANY`는 **적어도 한
  노드가 쓰기를 받아들였다**는 뜻이고 `ALL`은 **모든 노드가 받아들이고 성공을 응답해야 한다**는
  뜻이다. 저자들이 절충을 한 문장으로 적는다 — **더 높은 일관성 수준은 가용성과 파티션 내성을
  줄인다** (6장, p.171).[^ford2021-hard-parts]
- **모델링 1점의 근거는 행 키 설계다** — **데이터가 단일 행 식별자를 갖는 이름-값 쌍의 묶음으로
  배열되어야 하고 이 행 키를 설계하는 데 여러 번의 반복이 필요하다** (6장,
  p.170).[^ford2021-hard-parts] 다만 카산드라의 CQL 같은 **SQL 유사 질의 언어가 데이터 모델링을
  접근 가능하게 만들었다**고 덧붙인다.
  - 버전 조건: 2021년 저술 시점. 저자들이 CQL의 판을 적지 않는다.

## 그래프

- **무엇인가** — **관계가 참조에 근거해 암시되는 관계형 데이터베이스와 달리, 그래프
  데이터베이스는 노드(nodes)를 써서 엔티티와 그 속성을 저장한다. 이 노드들은 간선(edges), 다른
  이름으로 관계(relationships)로 연결되며 그것들은 명시적 객체다. 노드는 관계로 조직되고 특정
  간선을 따라 순회함으로써 연결된 데이터의 분석을 허용한다** (6장,
  p.171).[^ford2021-hard-parts]
- **간선에 방향이 있다** — 티켓 노드에서 고객 노드로 가는 `TICKET_CREATED` 간선을 예로 들어,
  **티켓 노드에서 나가는(outgoing) 간선으로 또는 고객 노드에서 들어오는(incoming) 간선으로
  순회할 수 있고, 방향이 뒤섞이면 그래프를 질의하는 일이 정말 어려워진다**고 적는다 (6장,
  p.172).[^ford2021-hard-parts]

  | 채점 항목 | Graph databases (Neo4J, Infinite Graph, Tigergraph, etc.) |
  |---|---|
  | Ease of learning | 1/5 |
  | Ease of data modeling | 2/5 |
  | Scalability/throughput | 3/5 |
  | Availability/partition tolerance | 3/5 |
  | Consistency | 3/5 |
  | Programming language support, product maturity, SQL support, community | 2/5 |
  | Read/write priority | 읽기 쪽 |

- **학습 1점은 여덟 갈래 최저이고, 그 값이 첫째 축의 규정 안 예시와 맞물린다** — 축을 규정할
  때 저자들이 든 니치 기술의 예가 **Gremlin(그래프 질의 언어)**이었다 (6장, p.161). 여기서는
  **노드·관계·관계 유형·속성을 어떻게 쓰는지 이해하는 데 시간이 걸린다**고 적는다 (6장,
  p.172).[^ford2021-hard-parts]
- **확장 점수가 3점에 묶이는 이유는 쓰기 쪽이다** — **복제된 노드가 읽기 확장을 개선하고 읽기
  부하에 맞춰 처리량을 조율할 수 있지만, 그래프를 쪼개거나 샤딩하기 어려우므로 쓰기 처리량은
  고른 그래프 데이터베이스의 종류에 제약된다** (6장, p.172).[^ford2021-hard-parts]
- **읽기가 빠른 이유가 저장 구조에 있다** — **관계 순회가 매우 빠른데, 인덱싱과 저장이
  영속화되어 있고 질의 시점에 계산되지 않기 때문이다** (6장, p.172). 그래서 저자들은 이 갈래를
  **읽기가 많은 시나리오에 더 낫다**고 적는다 (6장, p.173).[^ford2021-hard-parts]
- **일관성 3점의 근거** — **많은 그래프 데이터베이스가 ACID 트랜잭션을 지원한다. Neo4j 같은
  일부는 트랜잭션을 지원해 데이터가 항상 일관된다** (6장, p.173).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 기능이다.
- **질의 언어 지형을 한 문장으로 적는다** — **Gremlin이라는 언어 프레임워크가 여러 다른
  데이터베이스에 걸쳐 동작해 사용의 용이를 돕고, Neo4J는 Cypher라는 질의 언어를 지원한다**
  (6장, p.173).[^ford2021-hard-parts] 이 언어들의 전문은
  [그래프 질의 언어](../concepts/graph-query-languages.md)가 갖는다.

## 곁상자 — 관계 유형 바꾸기

- **그래프에서 되돌리기 비싼 결정이 무엇인지 저자들이 짚는다** (6장, p.173, 곁상자 "Changing
  Relationship Types"):[^ford2021-hard-parts]

  > Changing relationship types is an expensive operation, since each relationship type has
  > to be re-created. When this happens, both nodes connected by the edge have to be
  > visited, the new edge created, and the old edge removed. Hence, edge type or
  > relationship types have to be thought about carefully.

  - **이것이 이 갈래의 진입 결정을 무겁게 만든다** — 스키마 변경의 값이 종류마다 다르다는 것을
    저자들이 한 갈래에서만 곁상자로 떼어 적는 자리다. 같은 물음의 일반형은
    [진화적 데이터베이스 설계](../concepts/evolutionary-database-design.md)가 갖는다.

## NewSQL

- **이름의 출처와 규정** — **매튜 애슬릿(Matthew Aslett)이 NewSQL이라는 용어를 처음 써서, ACID
  같은 관계형 데이터베이스의 기능을 지원하면서 NoSQL 데이터베이스의 확장성을 제공하려는 새
  데이터베이스들을 규정했다. NewSQL 데이터베이스는 서로 다른 종류의 저장 기제를 쓰며 전부 SQL을
  지원한다** (6장, p.173).[^ford2021-hard-parts]
- **무엇을 개선하는가** — **자동화된 데이터 파티셔닝이나 샤딩을 제공해 수평 확장과 개선된
  가용성을 허용하면서, 동시에 개발자가 SQL과 ACID라는 익숙한 패러다임을 쓰도록 쉬운 이행을
  허용함으로써 관계형 데이터베이스를 개선한다** (6장, pp.173–174).[^ford2021-hard-parts]

  | 채점 항목 | New SQL databases (VoltDB, NuoDB, ClustrixDB, etc.) |
  |---|---|
  | Ease of learning | 3/5 |
  | Ease of data modeling | 3/5 |
  | Scalability/throughput | 3/5 |
  | Availability/partition tolerance | 3/5 |
  | Consistency | 2/5 |
  | Programming language support, product maturity, SQL support, community | 2/5 |
  | Read/write priority | 가운데 |

- **일곱 축 중 넷이 3점이고 둘이 2점이다** — 여덟 갈래 가운데 가장 고르게 퍼진 표이고, 만점도
  1점도 없다. 저자들이 그 고름을 말로 적지는 않는다.
- **확장의 근거는 다중 활성 노드다** — **NewSQL 데이터베이스는 분산 시스템을 위한 수평 확장을
  지원하도록 설계되어 여러 활성 노드를 허용하며, 이는 활성 리더가 하나뿐이고 나머지가
  팔로워인 관계형 데이터베이스와 다르다** (6장, p.174).[^ford2021-hard-parts]
  - 저자들이 가용성의 실물로 CockroachDB를 들고 **디스크·기계·데이터센터 장애를 견딘다**고
    적는다 (6장, p.174).[^ford2021-hard-parts]
    - 버전 조건: 2021년 저술 시점의 제품 주장이다.
- **일관성 서술과 별점이 어긋난다** — 본문은 **NewSQL 데이터베이스가 강하게 일관된 ACID
  트랜잭션을 지원하고 데이터가 항상 일관된다**고 적는데 (6장, p.175), 도판 6-31의 일관성 별은
  2/5로 관계형(5/5)의 절반도 안 된다.[^ford2021-hard-parts] **저자들이 그 차이를 설명하지
  않는다.** 아래 [도판과 본문이 어긋나는 자리](#도판과-본문이-어긋나는-자리)에 함께 적었다.
- **교체 비용을 낮추는 성질 하나를 적는다** — 일부 제품이 **기존 관계형 데이터베이스와 와이어
  호환 프로토콜을 지원해 호환성 문제 없이 관계형 데이터베이스를 대체할 수 있게 한다** (6장,
  p.175).[^ford2021-hard-parts]

## 클라우드 네이티브

- **무엇인가** — 클라우드 사용이 늘면서 **Snowflake·Amazon Redshift·Datomic·Azure CosmosDB
  같은 클라우드 데이터베이스가 인기를 얻었다. 이 데이터베이스들은 운영 부담을 줄이고 비용
  투명성을 제공하며, 선행 투자가 필요 없어 실험하기 쉬운 방법**이다 (6장,
  p.175).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 목록이고 이 갈래가 특히 빨리 낡는 자리다.

  | 채점 항목 | Cloud databases (Snowflake, Amazon Redshift, etc.) |
  |---|---|
  | Ease of learning | 2/5 |
  | Ease of data modeling | 2/5 |
  | Scalability/throughput | 4/5 |
  | Availability/partition tolerance | 3/5 |
  | Consistency | 3/5 |
  | Programming language support, product maturity, SQL support, community | 2/5 |
  | Read/write priority | 읽기 쪽 |

- **이 갈래만 "한 종류"가 아니다.** 저자들 스스로 학습 난이도를 제품마다 갈라 적는다 — Redshift는
  관계형과 비슷해 이해가 쉽고, Snowflake는 **SQL 인터페이스를 갖지만 저장과 연산 기제가 달라
  연습이 필요하며**, Datomic은 **모델 면에서 완전히 다르고 불변의 원자적 사실(immutable atomic
  facts)을 쓴다.** 그래서 **학습 곡선이 제품마다 다르다** (6장, p.176).[^ford2021-hard-parts]
  - **채점 축이 단일 종류를 전제하는데 이 칸만 그 전제가 깨진다.** 별점 하나가 서로 다른 제품
    셋의 평균처럼 놓인다. #hypothesis
- **확장의 절충이 기술이 아니라 값이다** — **이 데이터베이스들은 전부 클라우드 전용이므로 값을
  치르면 자원이 자동으로 할당될 수 있어 확장이 비교적 간단하다. 이 결정에서 절충은 보통 값과
  관련된다** (6장, p.176).[^ford2021-hard-parts] 그 선택의 일반형은
  [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md)이 갖는다.
- **가용성이 제품마다 다르고 설정에 달렸다** — Datomic은 **프로덕션 토폴로지(Production
  Topology)로 배포하면 고가용이고 단일 장애점이 없으며 광범위한 캐싱의 뒷받침을 받는다.**
  Snowflake는 **리전과 계정을 가로질러 데이터베이스를 복제한다.** Redshift는 **단일 가용
  영역에서 돌아가므로 더 높은 가용성을 위해서는 여러 클러스터로 돌려야 한다** (6장,
  p.176).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 동작이다.
- **채용 난이도가 이 갈래의 약점으로 적힌다** — **이 데이터베이스 다수가 새것이라 경험 있는
  도움을 찾기 어려울 수 있고, 실험하려면 클라우드 계정이 필요해 또 다른 장벽이 생긴다. 클라우드
  네이티브 데이터베이스가 운영 DBA의 작업 부하를 줄이기는 하지만 개발자에게는 학습 곡선이 더
  높다** (6장, p.176).[^ford2021-hard-parts]
  - **운영 부담과 학습 부담이 반대로 움직인다는 관찰**이고, 이것이 여섯째 축이 조직 조건을
    재는 축이라는 사실의 실물이다.

## 시계열

- **왜 갈라져 나왔는가** — **IoT·마이크로서비스·자율주행차·관측 가능성의 사용이 늘면서 시계열
  분석이 경이적으로 증가했고, 이 흐름이 시간 창 동안 수집된 데이터 포인트의 계열을 저장하는 데
  최적화된 데이터베이스를 낳아 어떤 기간에 걸친 변화든 추적할 수 있게 했다** (6장,
  p.177).[^ford2021-hard-parts]

  | 채점 항목 | Time series databases (InfluxDB, TimescaleDB, etc.) |
  |---|---|
  | Ease of learning | 1/5 |
  | Ease of data modeling | 2/5 |
  | Scalability/throughput | 4/5 |
  | Availability/partition tolerance | 2/5 |
  | Consistency | 3/5 |
  | Programming language support, product maturity, SQL support, community | 2/5 |
  | Read/write priority | 읽기 쪽 |

- **추가 전용이 이 갈래를 가른다** — **모든 데이터 포인트에 타임스탬프가 붙고 데이터는 거의 언제나
  삽입되며 갱신되거나 삭제되지 않는다. 추가 전용(append-only) 연산을 이해하는 데는 데이터의
  오류를 갱신으로 고칠 수 있는 다른 데이터베이스 사용법에서 얼마간 배운 것을 버려야 한다** (6장,
  p.177).[^ford2021-hard-parts]
- **모델링에 규칙이 하나 있다** — **한 태그에 하나 넘는 정보를 넣는 것은 나쁜 실천으로 여겨진다.**
  저자들이 든 예는 `ticket_status=Open, ticket_id=374737`이 `ticket_info=Open.374737`보다
  낫다는 것이다 (6장, p.177).[^ford2021-hard-parts]
- **범용이 아니라는 단서를 저자들이 명시한다** — **데이터베이스가 모든 데이터 생성에 타임스탬프를
  자동으로 붙이고 데이터는 정보의 태그나 속성을 담는다. 데이터는 특정 시간 창 사이의 어떤 사실에
  근거해 질의된다. 따라서 시계열 데이터베이스는 범용 데이터베이스가 아니다** (6장,
  p.178).[^ford2021-hard-parts]
  - **여덟 갈래 가운데 저자들이 "범용이 아니다"라고 못 박는 유일한 갈래다.** 선택 틀에서 이
    문장이 하는 일은 하나다 — 이 종류는 **데이터 도메인 전체가 아니라 그 도메인의 한 측면**에만
    붙는다.
- **확장 기제가 제품마다 다르다** — Timescale은 **PostgreSQL 기반이라 표준 확장·처리량 개선
  패턴을 허용**하고, InfluxDB는 **메타데이터를 관리하는 메타(meta) 노드와 실제 데이터를 저장하는
  데이터(data) 노드로 클러스터 모드를 돌려 확장과 처리량 개선을 제공한다** (6장,
  p.178).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점의 제품 구조다.
- **일관성이 저장 엔진에 따라 갈린다** — **관계형 데이터베이스를 저장 엔진으로 쓰는 시계열
  데이터베이스는 일관성을 위해 ACID 속성을 얻고, 다른 것들은 `any`·`one`·`quorum`의 일관성
  수준으로 일관성을 조율할 수 있다. 더 높은 일관성 수준 설정은 일반적으로 더 높은 일관성과 더
  낮은 가용성으로 이어지므로 고려해야 할 절충이다** (6장, p.178).[^ford2021-hard-parts]
- **이 갈래의 데이터 쪽 정본은 다른 페이지에 있다** —
  [시계열 데이터베이스](../concepts/time-series-databases.md)가 측정 데이터와 이벤트 기반
  데이터의 구분, 타임스탬프 정렬이 강제하는 스키마, 조인이 드문 까닭을 갖는다. 이 페이지가
  더하는 것은 **분해된 체계에서 이 종류를 언제 고르는가**뿐이다.

## 종류와 제품의 요약표

- **저자들이 절을 표 하나로 닫는다** — **이 절에서 논의한 모든 데이터베이스 종류를 요약해, 표
  6-6이 각 데이터베이스 종류의 인기 제품 몇을 보인다** (6장, p.178).[^ford2021-hard-parts]
  원문 열 머리글과 값 그대로 옮긴다 (표 6-6 "Summary of database types and products in the
  database type", pp.178–179):

  | Database type | Products |
  |---|---|
  | Relational | PostgreSQL, Oracle, Microsoft SQL |
  | Key-value | Riak KV, Amazon DynamoDB, Redis |
  | Document | MongoDB, Couchbase, AWS DocumentDB |
  | Column family | Cassandra, Scylla, Amazon SimpleDB |
  | Graph | Neo4j, Infinite Graph, Tiger Graph |
  | NewSQL | VoltDB, ClustrixDB, SimpleStore (aka MemSQL) |
  | Cloud native | Snowflake, Datomic, Redshift |
  | Time-series | InfluxDB, kdb+, Amazon Timestream |

  - 버전 조건: 2021년 저술 시점의 제품 목록이다. **이 표는 이 페이지에서 가장 빨리 낡는 자리고,
    갈래 여덟과 축 일곱은 그렇지 않다.**
  - **표가 두 쪽에 걸쳐 있고 두 번째 쪽에서 열 머리글이 다시 나온다** (p.179). 위 표는 그 둘을
    이어 붙인 것이다.

## 도판과 본문이 어긋나는 자리

**원문 그대로 두고 여기 모은다.** 이 KB가 대조해 적은 것이고 저자들이 이 어긋남들을 말하지
않는다.

| 어긋나는 자리 | 도판·표가 적는 것 | 본문이 적는 것 | locator |
|---|---|---|---|
| NewSQL의 일관성 | 별 2/5 | `strongly consistent ACID transactions. The data is always consistent` | 그림 6-31(p.174) 대 p.175 |
| 시계열의 학습 난이도 | 별 1/5(여덟 갈래 최저 타이) | `Understanding time-series data is often easy` | 그림 6-33(p.177) 대 p.177 |
| 그래프 별점표의 도판 번호 | 별점표는 그림 6-30 | `The ratings for graph databases are illustrated in Figure 6-29` (6-29는 간선 방향 도판) | p.172 |
| 관계형 제품 | 도판 머리글 `Oracle, SQL Server, Postgres` · 표 6-6 `PostgreSQL, Oracle, Microsoft SQL` | `MySQL, Oracle, Microsoft SQL Server, and PostgreSQL`(MySQL이 본문에만) | 그림 6-25(p.163) · 표 6-6 · p.164 |
| 문서 제품 | 도판 머리글 `MongoDB, CouchDB, Marklogic` · 표 6-6 `MongoDB, Couchbase, AWS DocumentDB` | — | 그림 6-27(p.168) · 표 6-6 |
| 컬럼 패밀리 제품 | 도판 머리글 `Cassandra, Scylla, Druid` · 표 6-6 `Cassandra, Scylla, Amazon SimpleDB` | — | 그림 6-28(p.170) · 표 6-6 |
| NewSQL 제품 | 도판 머리글 `VoltDB, NuoDB, ClustrixDB` · 표 6-6 `VoltDB, ClustrixDB, SimpleStore (aka MemSQL)` | 본문은 CockroachDB를 든다 | 그림 6-31(p.174) · 표 6-6 · p.174 |
| 시계열 제품 | 도판 머리글 `InfluxDB, TimescaleDB` · 표 6-6 `InfluxDB, kdb+, Amazon Timestream` | `InfluxDB, Kx, and TimeScale` | 그림 6-33(p.177) · 표 6-6 · p.177 |

- **제품 이름의 표기도 자리마다 흔들린다** — `Neo4j`와 `Neo4J`(p.173과 그림 6-30), `Tiger
  Graph`와 `Tigergraph`(표 6-6과 그림 6-30), `TimeScale`과 `Timescale`과
  `TimescaleDB`(p.177·p.178·그림 6-33)다. 원문 그대로 두었다.
- **읽는 법 하나** — 제품 목록 셋이 자리마다 다르다는 것은 **목록이 예시이지 정본이 아니라는
  뜻**이다. 이 페이지가 별점과 축을 옮기면서 제품 목록에 버전 조건을 붙이는 근거가 여기 있다.

## 이 선택이 데이터 분해의 어디에 놓이는가

- **이 절은 다섯 단계의 끝에서 열린다** — 5단계(독립 데이터베이스 서버로 전환)를 마친 팀이
  **각 데이터베이스 서버를 가용성과 확장성에 맞춰 최적화할 수 있고, 데이터를 분석해 쓸 가장
  적절한 데이터베이스 종류를 판정하여 생태계 안에 폴리글랏 데이터베이스 사용(polyglot database
  usage)을 도입할 수 있다** (6장, p.161).[^ford2021-hard-parts] 그 다섯 단계는
  [모놀리식 데이터를 쪼개는 다섯 단계](../concepts/decomposing-monolithic-data.md)가 갖는다.
- **그리고 이 절이 분해 요인 하나의 값을 치른다** —
  [데이터 분해의 구동 요인](../concepts/data-decomposition-drivers.md)의 여섯째 분해 요인인 **데이터베이스
  종류 최적화**는 "쪼개면 종류를 고를 수 있다"까지만 적고 종류의 목록을 이 절로 넘겼다 (6장,
  p.146).[^ford2021-hard-parts] **이 페이지가 그 넘김을 받는 자리다.**
- **그래서 이 페이지가 답하는 단위는 제품이 아니라 데이터 도메인이다.** 한 체계에 하나를
  고르는 것이 아니라 **쪼개 놓은 데이터 도메인마다 따로 고르는 것**이고, 그것이 저자들이
  폴리글랏이라 부르는 상태다.
  - **거꾸로 읽으면 이 절은 분해의 근거가 되기도 한다.** 도메인마다 최적 종류가 다르다는 사실이
    쪼갤 이유의 하나였고, 쪼갠 뒤에야 그 사실을 쓸 수 있다. 같은 순환을 데이터 모델 쪽에서 적은
    자리가 [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md)의 마지막
    절이다 — **경계가 갈라진 뒤에야 어느 모델이 맞는가를 도메인마다 따로 물을 수 있다**는 판정이
    같은 저자 무리(ford2022)의 것이다.

## 책의 사례 — 폴리글랏 데이터베이스

- **장면** — 데이터 도메인을 만든 뒤 개발자가 **설문(Survey) 데이터 도메인을 전통적 관계형에서
  JSON을 쓰는 문서 데이터베이스로 옮길 훌륭한 후보**로 짚지만, 데이터 아키텍처 책임자가
  **설문 테이블은 과거에 관계형으로 늘 잘 동작했으니 바꿀 이유가 없다**며 거부한다 (6장, p.179,
  사가).[^ford2021-hard-parts]
- **거부를 돌려세운 것이 기술 논거가 아니라 업무 논거다.** 사용자 인터페이스 담당자가 **관계형
  데이터를 설문 화면으로 렌더링하는 일이 주된 고통점**이라고 말하고, 아키텍트가 제품 책임자를
  만나 **마케팅 부서가 설문 변경의 유연성과 적시성을 요구한다**는 사실을 확인한 뒤에야 데이터
  아키텍트가 합의한다 (6장, pp.179–180, 사가).[^ford2021-hard-parts]
  - **데이터 아키텍트가 요구한 것이 "다른 종류의 데이터베이스를 섞을 탄탄한 정당화"였다** (6장,
    p.179, 사가). 이 절의 별점표가 하는 일이 바로 그 정당화의 재료다.
  - **6장 전반의 사가와 같은 구도의 반복이다** — 거기서도 데이터 아키텍트가 거부한 채 시작했고
    지표로 돌려세웠다. 여기서는 지표가 아니라 **업무 쪽 고통**이 재료가 된다는 점만 다르다.
    두 장면의 대비는 [Sysops Squad 사례](sysops-squad-case.md)에 모았다.
- **합의 뒤의 결정은 종류가 아니라 애그리게이트 설계다** — 문서 데이터베이스로 가기로 한 다음
  남은 물음이 **단일 애그리게이트 문서인가 쪼갠 것인가**이고, 팀은 **둘 다 모델링해 절충을 눈으로
  보기로** 한다 (6장, p.181, 사가).[^ford2021-hard-parts]

  | 선택지 | 무엇을 얻는가 | 무엇을 내주는가 |
  |---|---|---|
  | 단일 애그리게이트(설문에 질문을 묻어 넣는다) | **단일 `get` 연산으로 설문 전체를 회수**할 수 있어 화면 쪽 작업이 쉬워진다 | **질문이 설문 문서마다 복제된다** |
  | 쪼갠 애그리게이트(설문이 질문을 참조한다) | **같은 질문을 여러 설문에서 쓸 수 있다** | **단일 애그리게이트보다 렌더링과 회수가 어렵다** |

- **판정의 근거가 규모의 실측이다** — 아키텍트가 **설문 종류가 다섯뿐이고(제품 범주마다 하나)
  변경의 대부분이 질문을 더하거나 빼는 일**임을 짚었고, 팀은 **질문 데이터의 얼마간의 중복을
  변경과 렌더링의 쉬움과 맞바꾸기로** 합의한다 (6장, p.184, 사가).[^ford2021-hard-parts]
  - **애그리게이트 지향의 대가 둘 가운데 첫째(경계를 정하기 어렵고 바꾸기 어렵다)가 바로 여기서
    치러진다.** 곁상자의 일반 진술과 사가의 구체 결정이 한 장 안에서 맞물리는 자리다.
- **이 결정이 ADR로 기록된다** — 저자들이 그 이유를 적는다. **이 결정의 어려움과 데이터를 바꾸는
  일의 구조적 성격 때문에** 아키텍트가 ADR을 만들었다 (6장, p.184, 사가).[^ford2021-hard-parts]
  원문 그대로 옮긴다 (6장, p.184, ADR):

  > *ADR: Use of Document Database for Customer Survey*
  >
  > *Context*
  >
  > Customers receive a survey after the work has been completed by the customer, which is
  > rendered on a web page for the customer to fill out and submit. The customer receives
  > one of five survey types based on the type of electronic product fixed or installed. The
  > survey is currently stored in a relational database, but the team wants to migrate the
  > survey to a document database using JSON.
  >
  > *Decision*
  >
  > We will use a document database for the customer survey.
  >
  > The Marketing Department requires more flexibility and timeliness for changes to the
  > customer surveys. Moving to a document database would not only provide better
  > flexibility, but also better timeliness for changes needed to the customer surveys.
  >
  > Using a document database would simplify the customer survey user interface and better
  > facilitate changes to the surveys.
  >
  > *Consequences*
  >
  > Since we will be using a single aggregate, multiple documents would need to be changed
  > when a common survey question is updated, added, or removed.
  >
  > Survey functionality will need to be shut down during the data migration from the
  > relational database to the document database.

  - **맥락 칸의 첫 문장이 문법적으로 어긋난다** — `after the work has been completed by the
    customer`인데 작업을 완료하는 쪽은 고객이 아니라 전문가다. 원문 그대로 옮기고 표시한다.
  - **이 ADR이 형식의 규정을 한 자리에서 벗어난다** — 맥락 칸이 **대안 해법의 목록**을 요구하는데
    (1장, p.5) 여기서는 관계형을 유지한다는 대안이 문장 안에 암시될 뿐 목록으로 적히지
    않는다.[^ford2021-hard-parts] 그 형식의 정본은
    [아키텍처 결정 기록](../concepts/architecture-decision-records.md)이다.
  - **귀결 칸 둘이 서로 다른 층이다** — 첫째는 **설계 선택의 영구적 대가**(단일 애그리게이트라
    질문 변경이 여러 문서를 건드린다)이고, 둘째는 **이행 한 번의 비용**(이관 동안 설문 기능
    정지)이다. 저자들이 그 구분을 적지는 않는다. #hypothesis
- **6장 전체에서 ADR이 이 하나뿐이다** — 부록 B의 쪽 목록에서 p.79 다음이 p.184다. 6장 전반
  (pp.131–161)에는 ADR이 없고 이 결정 하나만 기록된다.[^ford2021-hard-parts]

## 2025년 원전이 이 채점을 교차점으로 다시 부르는 자리

**같은 저자 무리의 2025년 책이 아키텍처가 정렬되어야 할 면 아홉 가운데 하나로 데이터 토폴로지를
놓고, 그 절에서 이 채점을 이름으로 불러낸다.** 아홉의 목록은
[아키텍처의 교차점 아홉](../concepts/architectural-intersections.md)에 있다.

- **이 교차점이 자주 간과된다는 진단으로 절이 열린다** — **데이터베이스의 종류나 토폴로지를
  잘못 고르면 아키텍처를 해치고 그 아키텍처의 가장 좋은 특성을 무효로 만들 수 있다**
  (richards2025 26장 §"Architecture and Data Topologies", p.477).[^richards2025]
  - **양쪽의 대가가 짝으로 적힌다** — **모놀리식 데이터베이스는 데이터 일관성과 트랜잭션 지원이
    좋은 대신 확장성과 결함 내성을 깎고**, **분산 데이터베이스 토폴로지는 확장성과 변경 통제에
    좋은 대신 데이터 무결성과 일관성과 성능을 떨어뜨린다** (26장, p.477).[^richards2025]
- **토폴로지가 셋으로 세어진다** — **모놀리식 데이터베이스 · 분산 도메인 기반 데이터베이스들 ·
  서비스별 데이터베이스**다 (26장 §"Database Topology", p.478).[^richards2025]
  - **정렬의 실물** — 마이크로서비스 아키텍처는 **엄격한 경계 컨텍스트를 지키려고 대개 서비스별
    패턴을 쓴다.** 그 정렬이 없으면 아키텍트가 변경을 통제하기가 극히 어려워지고 **결함 내성·
    확장성·탄력성·유지보수성·시험 가능성·배포 가능성이 전부 나빠진다** (26장,
    p.479).[^richards2025]
  - **유연한 쪽도 함께 적힌다** — **서비스 기반 아키텍처 같은 스타일은 물리 데이터베이스
    토폴로지에 대해 더 유연하다** (26장, p.479).[^richards2025]
  - **도판을 렌더해 본 것** — 토폴로지 셋을 위아래로 겹쳐 그린 도판인데, **가운데의 도메인
    기반 판이 컴포넌트 묶음 넷에 데이터베이스 둘만 그린다**(하나가 혼자 쓰고 셋이 하나를 나눠
    쓴다). 본문은 그 비대칭을 설명하지 않는다 (26장, p.478, 그림 26-4).[^richards2025]
- **이 페이지의 채점이 그 절에서 호명된다** — 저자들이 **자기들 책 *Software Architecture: The
  Hard Parts*에서 데이터베이스 종류들의 특성을 채점했다**고 적고, **확장성과 탄력성이
  마이크로서비스·이벤트 주도·공간 기반의 초능력이자 키-값과 컬럼 데이터베이스의 초능력이기도
  하므로 그 두 종류가 그 특성을 증폭하기 좋은 선택**이라고 잇는다 (26장 §"Architectural
  Characteristics", p.479).[^richards2025]
  - **조문은 짝 맞추기다** — **체계의 아키텍처적 초능력을 데이터베이스 종류의 초능력과 맞추라**는
    것이다.
- **그런데 그 호명이 이 페이지의 채점과 수가 맞지 않는다.** 이 KB가 대조한 결과다.

  | 무엇 | 2025년 책이 적는 것 | 이 페이지가 실제로 갖는 것 |
  |---|---|---|
  | 갈래의 수 | **여섯** | **여덟** |
  | 이름 목록 | 관계형·키-값·문서·컬럼·그래프·**NoSQL** | 관계형·키-값·문서·컬럼 패밀리·그래프·**NewSQL**·**클라우드 네이티브**·**시계열** |

  - **`NoSQL`은 이 페이지에서 갈래가 아니다** — 네 갈래를 가로질러 묶는 **애그리게이트 지향**의
    이름이고, 저자들 자신이 그 범위를 컬럼 패밀리 절 끝에서 못 박는다. **곧 2025년 책은 계열의
    이름을 갈래의 자리에 넣었다.**
  - **같은 절이 두 문단 뒤에 `NewSQL`을 쓴다** — 읽기와 쓰기가 엇비슷하면 **관계형과 NewSQL이
    좋은 선택**이라고 적는다 (26장 §"Read/Write Priority", p.479).[^richards2025] **곧 자기
    목록에 넣지 않은 갈래를 곧바로 쓴다.**
  - **이 KB는 판정하지 않고 기록만 한다.** 닐 포드가 두 책의 저자에 함께 들지만, 이 어긋남은
    수치의 변경이 아니라 **뒤 책이 앞 책의 목록을 줄여 인용한 것**이라 성질이 다르다.
    #hypothesis
- **같은 절이 축 둘을 더 얹는다** (26장, p.479).[^richards2025]
  - **데이터 구조** — 저장하고 접근하는 데이터가 **서로 의존하는 관계의 계층**이면 관계형이 잘
    맞고, **키-값 쌍을 관계형에 넣는 것은 어긋남**이라 데이터베이스와 아키텍처 양쪽에 비효율을
    낳는다. 한 아키텍처 안에서도 데이터 구조가 갈릴 수 있으므로(관계형인 것 · JSON 적재물처럼
    문서인 것 · 키-값인 것) **가능하면 폴리글랏 데이터베이스를 쓰라**고 권한다.
  - **읽기와 쓰기의 우선순위** — 드문 읽기보다 **쓰기가 많은 쪽이 우선이면 컬럼**, 반대로
    **읽기가 많으면 키-값·문서·그래프**, **둘이 엇비슷하면 관계형과 NewSQL**이 좋은 선택이고,
    이 요인을 어긋나게 맞추면 **성능이 나쁜 체계**가 된다.
  - **이 페이지의 일곱째 축(읽기 쓰기 우선)이 그 판정의 재료다.** 2025년 책은 축의 값을 다시
    적지 않고 **종류별 결론만** 옮긴다.

## 이 KB의 데이터 모델 페이지들과 겹치는 자리

**이 절이 여덟 갈래를 훑으므로 이 KB의 데이터 축 페이지들과 소재가 겹친다. 무엇이 어느 쪽
것인지 여기 고정한다.**

| 소재 | 이 페이지가 갖는 것 | 정본이 있는 자리 |
|---|---|---|
| 관계형과 문서의 대결 | 두 종류의 채점표와 선택 시점의 별점 | [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md) — 임피던스 불일치·지역성·수렴 |
| 그래프 | 그래프 종류의 채점표와 진입 비용 | [그래프 데이터 모델](../concepts/graph-data-models.md)과 [그래프 질의 언어](../concepts/graph-query-languages.md) |
| 시계열 | 시계열 종류의 채점표와 "범용이 아니다"라는 단서 | [시계열 데이터베이스](../concepts/time-series-databases.md) |
| 컬럼 | 컬럼 패밀리 종류의 채점표(행마다 열 수가 다른 모델) | [열 지향 저장](../concepts/column-oriented-storage.md) — 분석용 열 지향 배치. **둘은 다른 것이다** |
| 일관성과 가용성 | 종류마다 별 하나로 요약된 값 | [CAP과 PACELC](../concepts/cap-and-pacelc.md)와 [일관성 모델](../concepts/consistency-models.md) |
| 샤딩 | 파티셔닝과 가르는 한 문단 | [데이터 샤딩](../synthesis/data-sharding.md) 축 |
| 클라우드 | 클라우드 네이티브 종류의 채점표 | [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md) |

- **컬럼 패밀리와 열 지향 저장을 같은 것으로 읽지 않는다.** 이 절의 컬럼 패밀리는 **행마다 열
  수가 다른 이름-값 쌍 모델**(카산드라 계열)이고, 이 KB의 열 지향 저장은 **분석 질의를 위해 한
  열의 값을 붙여 두는 디스크 배치**다. 이름이 겹칠 뿐 층이 다르다. 저자들이 이 절에서
  `columnar databases`라는 낱말도 함께 쓰므로 (6장, p.169) 혼동하기 쉬운
  자리다.[^ford2021-hard-parts]
- **이 페이지의 채점이 겨냥하는 물음이 저 페이지들과 다르다.** 저쪽은 **이 데이터에 어느 모델이
  맞는가**를 묻고, 이 페이지는 **이 조직이 이 종류를 도입해 운영할 수 있는가**를 함께 묻는다.
  여섯째 축(채용 가능성)과 첫째 축(학습 난이도)이 그 차이의 실물이다 — 순수한 모델 적합 논의에는
  그 두 축이 없다. **둘은 같은 대상을 다르게 재는 것이 아니라 다른 대상을 잰다.**

## 이어지는 페이지

- [데이터 분해의 구동 요인](../concepts/data-decomposition-drivers.md) — 여섯째 분해 요인이 이 페이지로
  넘어오는 자리
- [모놀리식 데이터를 쪼개는 다섯 단계](../concepts/decomposing-monolithic-data.md) — 이 선택이 열리는
  다섯째 단계
- [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md) — 쪼갠 뒤에 깨지는 것들
- [Sysops Squad 사례](sysops-squad-case.md) — 이 절의 사가가 붙는 운영 예제
- [아키텍처 결정 기록](../concepts/architecture-decision-records.md) — 이 절의 결정이 기록되는 형식
- [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md) — 두 모델의 대결
  자체를 갖는 자리
- [그래프 질의 언어](../concepts/graph-query-languages.md) — 이 절이 Gremlin·Cypher로만 스치는
  자리의 전문
- [시계열 데이터베이스](../concepts/time-series-databases.md) — 여덟째 갈래의 데이터 쪽 정본
- [열 지향 저장](../concepts/column-oriented-storage.md) — 컬럼 패밀리와 이름이 겹치는 다른 것
- [CAP과 PACELC](../concepts/cap-and-pacelc.md) — 넷째·다섯째 축의 낱말이 사는 자리
- [클라우드와 자체 호스팅](../concepts/cloud-versus-self-hosting.md) — 일곱째 갈래가 걸리는 선택
- [애그리게이트와 정합성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 애그리게이트 지향이 빌려 온 개념의 원전
- [진화적 데이터베이스 설계](../concepts/evolutionary-database-design.md) — 고른 뒤에 그것을 바꾸는 일
- [데이터 분해와 정합성](../synthesis/data-decomposition-and-consistency.md) — 이
  페이지가 걸리는 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 6장 "Pulling Apart Operational
    Data" §"Selecting a Database Type"(pp.161–179, 하위 §"Relational Databases" pp.163–164 ·
    곁상자 "Aggregate Orientation" p.165 · §"Key-Value Databases" pp.165–167 · 곁상자
    "Sharding in Databases" p.167 · §"Document Databases" pp.167–169 · 곁상자 "Schema-less
    Databases" p.169 · §"Column Family Databases" pp.169–171 · §"Graph Databases"
    pp.171–173 · 곁상자 "Changing Relationship Types" p.173 · §"NewSQL Databases"
    pp.173–175 · §"Cloud Native Databases" pp.175–177 · §"Time-Series Databases"
    pp.177–178 · 표 6-6 pp.178–179) · §"Sysops Squad Saga: Polyglot Databases"(pp.179–184,
    ADR p.184). 축 일곱의 규정은 pp.161–162, 이 절이 열리는 문단은 p.161(5단계 끝), 여섯째
    분해 요인이 이 절로 넘어오는 자리는 p.146, ADR 형식의 규정은 1장 p.5, ADR 목록은 부록 B
    pp.419–420이다. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측).
    **직인용 여섯(축 일곱의 규정 목록 · 애그리게이트 지향의 규정과 이점·대가 목록 · 샤딩
    곁상자 · 스키마 없음 곁상자 · 관계 유형 바꾸기 곁상자 · ADR 전문)은 `pdftotext -layout`
    추출로 문자 단위 대조했다** — 줄바꿈 하이픈(U+2010)으로 끊긴 낱말은 한 낱말로 이었고, 굽은
    따옴표는 곧은 것으로 옮겼으며, 원문이 이탤릭으로 조판한 낱말은 인용 안에서 이탤릭을
    유지했다. 원문이 정의 목록으로 조판한 축 일곱과 이점·대가 목록은 인용 블록으로 옮기며 항목
    사이에 빈 줄을 넣었다 — 낱말은 보태거나 빼지 않았다.
    **별점 도판 여덟(그림 6-25 p.163 · 6-26 p.166 · 6-27 p.168 · 6-28 p.170 · 6-30 p.172 ·
    6-31 p.174 · 6-32 p.175 · 6-33 p.177)은 `pdftoppm -r 160 -png`로 렌더해 눈으로 별을
    셌다** — 별점은 두 추출기 모두의 텍스트 레이어에 아예 없다(이 KB가 그림 3-9에서 실측한 것과 같다).
    별 수는 `N/5` 꼴로 옮겼고, 읽기 쓰기 눈금은 별이 아니라 띠 위 표식이라 렌더에서 표식의
    픽셀 위치를 띠 안 비율로 재어 **읽기 쪽(0.2~0.3) · 가운데(0.5 안팎) · 쓰기 쪽(0.7 이상)**
    셋으로만 적었다 — 원문에 수치 눈금이 없으므로 그보다 잘게 적지 않는다. 각 표의 오른쪽 열
    머리글은 도판 머리글의 제품 목록을 원문 그대로 옮긴 것이고, 행 이름도 도판의 것이다(규정
    목록의 이름과 두 자리가 다르다 — 본문에 적었다). 표 6-6은 두 쪽에 걸치고 두 추출기의 값이
    일치해 그대로 옮겼다.
    **도판 넷(그림 6-24 독립 데이터베이스 서버 · 6-29 간선 방향 · 6-34~6-37 설문 모델 넷)은
    재현하지 않았다** — 본문이 그 도판에 대해 적는 것만 옮겼다.
    **JSON 목록 둘(예제 6-3 단일 애그리게이트 · 예제 6-4 쪼갠 애그리게이트, pp.182–184)은
    펜스로 옮기지 않았다** — 둘이 같은 설문 데이터를 두 가지로 조판한 것이고 그 절의 claim은
    **둘 중 무엇을 고르고 왜인가**라는 판정이라 위 절충 표로 보존된다. 6장의 대표 펜스는
    [모놀리식 데이터를 쪼개는 다섯 단계](../concepts/decomposing-monolithic-data.md)의 예제 6-1 하나다
    (SCHEMA §3 개념당 대표 하나).
    원문 오식 하나를 그대로 옮기고 표시했다 — 곁상자 "Aggregate Orientation"의 `Erik
    Evans`(Eric). 도판과 본문이 어긋나는 자리 여덟도 원문 그대로 두고 위 표에 모았다. ADR
    맥락 칸의 `completed by the customer`도 표시만 했다. 저자들이 대는 바깥 것들(사달게이·
    파울러의 *NoSQL Distilled*, 에반스의 *Domain-Driven Design*, 애슬릿의 NewSQL 명명)
    가운데 에반스만 이 KB에 원전으로 들어와 있고 나머지 둘은 서지 사실로만 적었다. 굵은 글씨는
    원문 문장의 한국어 재서술이고 괄호 안이 그 쪽이다.

[^richards2025]: Richards·Ford 2025(2판), 26장 "Architectural Intersections"
    §"Architecture and Data Topologies"(pp.477–479)과 그 아래 소절 §"Database Topology"
    (pp.478–479) · §"Architectural Characteristics"(p.479) · §"Data Structure"(p.479) ·
    §"Read/Write Priority"(p.479). 쪽은 인쇄판 쪽 번호(본문 = PDF 쪽 − 24, 실측). **이 절에
    직인용도 표도 코드 목록도 없고 도판이 하나다**(그림 26-4 데이터베이스 토폴로지 셋).
    **`pdftoppm -r 160 -png`로 렌더해 확인했고** 도메인 기반 판의 데이터베이스 수 비대칭은
    본문에 없어 도판에서만 읽힌다. **도판은 복제하지 않고 무엇을 보이는지만 한국어로 다시
    적었다.** 여섯과 여덟의 어긋남은 이 KB가 두 책의 문면을 맞대어 세운 것이고 저자들은 그
    대조를 적지 않는다.

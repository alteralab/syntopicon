---
type: concept
title: 그래프 질의 언어
description: 그래프를 질의하는 네 가지 언어와 SQL의 대응 — 화살표 표기로 패턴을 적는 Cypher, 같은 질의를 재귀 공통 테이블 표현식으로 옮겼을 때 4줄이 31줄이 되는 SQL, Cypher가 패턴 매칭을 빌려 온 SPARQL, 규칙을 쌓아 올려 재귀를 표현하는 Datalog, 2024년에 나온 ISO 표준 GQL, 그리고 이 언어들의 진입 비용을 아키텍처 쪽에서 채택 특성으로 채점한 소스
generated: { by: "claude-opus-5", at: "2026-08-14T22:00:00Z" }
sources:
  - { id: kleppmann2026, resource: /it/sources/kleppmann2026.md }
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 그래프 질의 언어

- [예제로 쓰는 질의](#예제로-쓰는-질의)
- [Cypher](#cypher)
- [SQL로 그래프를 질의하면](#sql로-그래프를-질의하면)
- [SPARQL](#sparql)
- [Datalog](#datalog)
- [이 언어들의 진입 비용을 채점한 소스](#이-언어들의-진입-비용을-채점한-소스)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **정점과 간선으로 표현된 데이터를 어떤 언어로 질의하며, 가변 길이 경로를 따라가는
일이 언어마다 얼마나 다르게 표현되는가.**

- 이 장이 다루는 범위 — **우리는 그래프를 위한 네 가지 질의 언어(Cypher·SPARQL·Datalog·
  GraphQL)와 그래프 질의를 위한 SQL 지원을 본다. Gremlin 같은 다른 그래프 질의 언어도
  존재하지만, 이것들이 대표적인 개관을 준다** (3장, p.85).[^kleppmann2026] 그중 GraphQL은
  성격이 달라 [GraphQL](../concepts/graphql.md)에서 따로 다룬다.

## 예제로 쓰는 질의

- 이 절 내내 같은 질문을 각 언어로 옮긴다 — **미국에서 유럽으로 이민한 모든 사람의 이름을 찾는
  것**이다. 방법은 **미국 안의 어떤 장소로 가는 BORN_IN 간선과 유럽 안의 어떤 장소로 가는
  LIVING_IN 간선을 가진 정점을 전부 찾아 그 정점들의 name 속성을 반환하는 것**이다 (3장,
  p.89).[^kleppmann2026] 데이터 자체는
  [그래프 데이터 모델](../concepts/graph-data-models.md)의 예시 그래프다.

## Cypher

- **Cypher는 속성 그래프를 위한 질의 언어로, 원래 Neo4j 그래프 데이터베이스를 위해 만들어졌고
  나중에 openCypher라는 열린 표준으로 발전했다. Neo4j 외에 Memgraph·KùzuDB·아마존 넵튠·
  Apache AGE(PostgreSQL에 저장한다) 등이 Cypher를 지원한다. 이 언어의 이름은 영화 매트릭스의
  등장인물에서 왔고 암호학의 사이퍼와는 관계없다** (3장, p.88).[^kleppmann2026]
- 데이터를 넣을 때 — **각 정점에 usa나 idaho 같은 상징적 이름을 준다. 그 이름은 데이터베이스에
  저장되지 않고 정점 사이에 간선을 만들기 위해 질의 안에서만 내부적으로 쓰인다. 화살표 표기를
  쓴다 — `(idaho) -[:WITHIN]-> (usa)`는 idaho를 꼬리 노드로, usa를 머리 노드로 하는 WITHIN
  레이블의 간선을 만든다** (3장, p.88).[^kleppmann2026]
- 질의할 때는 같은 화살표 표기가 MATCH 절에 쓰인다 — **`(person) -[:BORN_IN]-> ()`는 BORN_IN
  레이블의 간선으로 연결된 임의의 두 정점과 일치한다. 그 간선의 꼬리 정점은 변수 person에
  바인딩되고 머리 정점은 이름 없이 남는다** (3장, p.89). 앞의 질문은 이렇게 쓴다 (3장, p.89,
  예제 3-5):[^kleppmann2026]

  ```cypher
  MATCH
    (person) -[:BORN_IN]->  () -[:WITHIN*0..]-> (:Location {name:'United States'}),
    (person) -[:LIVES_IN]-> () -[:WITHIN*0..]-> (:Location {name:'Europe'})
  RETURN person.name
  ```

- 읽는 법 — **다음 두 조건을 모두 만족하는 정점(person이라 부르자)을 찾아라. (1) person은 어떤
  정점으로 가는 나가는 BORN_IN 간선을 갖는다. 그 정점에서 나가는 WITHIN 간선의 사슬을 따라가면
  결국 name 속성이 United States인 Location 타입의 정점에 도달할 수 있다. (2) 같은 person 정점은
  나가는 LIVES_IN 간선도 갖는다. 그 간선을 따라가고 그다음 나가는 WITHIN 간선의 사슬을 따라가면
  결국 name 속성이 Europe인 Location 타입의 정점에 도달한다. 그런 person 정점 각각에 대해 name
  속성을 반환하라** (3장, p.89).[^kleppmann2026]
- 실행 방법은 하나가 아니다 — **여기 주어진 서술은 데이터베이스의 모든 사람을 훑으며 각 사람의
  출생지와 거주지를 검사해 조건을 만족하는 사람만 반환하는 것을 시사한다. 그러나 동등하게, 두
  Location 정점에서 시작해 거꾸로 일할 수도 있다. name 속성에 인덱스가 있으면 미국과 유럽을
  나타내는 두 정점을 효율적으로 찾을 수 있다. 그다음 들어오는 WITHIN 간선을 전부 따라가 미국과
  유럽 안의 모든 장소(주·지역·도시 등)를 찾고, 마지막으로 그 위치 정점 중 하나로 들어오는
  BORN_IN이나 LIVES_IN 간선을 통해 찾을 수 있는 사람을 찾으면 된다** (3장,
  pp.89–90).[^kleppmann2026] 어느 쪽으로 실행할지 고르는 것이 질의 최적화기의 일이다(→
  [데이터베이스 관리 시스템의 구조](../concepts/dbms-architecture.md)).

## SQL로 그래프를 질의하면

- 질문이 뒤집힌다 — **그래프 데이터는 관계형 데이터베이스로 표현될 수 있다. 그런데 그래프
  데이터를 관계형 구조에 넣으면 SQL로도 질의할 수 있는가? 답은 그렇다, 다만 약간의 어려움이
  있다** (3장, p.90).[^kleppmann2026]
- 어려움의 정체 — **그래프 질의에서 순회하는 모든 간선은 사실상 edges 테이블과의 조인이다.
  관계형 데이터베이스에서는 보통 질의에 어떤 조인이 필요한지 미리 안다. 반면 그래프 질의에서는
  찾는 정점에 이르기까지 가변 개수의 간선을 순회해야 할 수 있다 — 즉 조인의 개수가 미리 고정돼
  있지 않다** (3장, p.90).[^kleppmann2026]
- 그 지점이 Cypher의 `*0..`이다 — **사람의 LIVES_IN 간선은 거리·도시·구역·지역·주 등 어떤 종류의
  장소든 가리킬 수 있다. 도시는 지역 WITHIN일 수 있고, 지역은 주 WITHIN, 주는 나라 WITHIN일 수
  있다. LIVES_IN 간선은 찾는 위치 정점을 직접 가리킬 수도 있고, 위치 계층에서 몇 단계 떨어져
  있을 수도 있다. Cypher에서 `:WITHIN*0..`은 그 사실을 매우 간결하게 표현한다 — "WITHIN 간선을
  0회 이상 따라가라"는 뜻이며, 정규 표현식의 `*` 연산자와 같다** (3장,
  p.90).[^kleppmann2026]
- SQL 쪽의 대응 — **질의에서 가변 길이 순회 경로라는 이 발상은 재귀 공통 테이블 표현식(recursive
  common table expressions, `WITH RECURSIVE` 구문)으로 표현될 수 있다** (3장,
  p.90).[^kleppmann2026]
- 그 비용이 수치로 나온다 — **4줄짜리 Cypher 질의가 SQL에서는 31줄을 요구한다는 사실은 올바른
  데이터 모델과 질의 언어의 선택이 얼마나 큰 차이를 만들 수 있는지 보여 준다. 그리고 이것은
  시작일 뿐이다 — 예컨대 순환 처리와 너비 우선·깊이 우선 순회 사이의 선택 같은 고려할 세부가 더
  있다** (3장, p.91).[^kleppmann2026]
- 그 밖의 언어들 — **오라클은 재귀 질의를 위한 다른 SQL 확장을 갖고 있으며 그것을
  계층형(hierarchical)이라 부른다. 다른 그래프 질의 언어로 TigerGraph의 GSQL과 속성 그래프 질의
  언어(Property Graph Query Language, PGQL)가 있다** (3장, p.91).[^kleppmann2026]
- 표준화 소식 — **Cypher에 기반한 그래프 질의 언어(Graph Query Language, GQL) ISO 표준이
  2024년에 발행됐다. 아직 널리 채택되지는 않았지만, 앞으로 몇 년 안에 그래프 데이터베이스들
  사이에 더 큰 통일성을 가져오기를 바란다** (3장, p.91).[^kleppmann2026] 채택 현황에 대한 이
  서술은 2026년 출간 시점 기준이다.

## SPARQL

- **SPARQL은 RDF 데이터 모델을 쓰는 트리플 스토어를 위한 질의 언어다(이름은 SPARQL Protocol
  and RDF Query Language의 재귀 약자이며 "스파클"로 읽는다). 그것은 Cypher보다 앞서며, Cypher의
  패턴 매칭이 SPARQL에서 빌려 온 것이므로 둘은 꽤 비슷해 보인다** (3장,
  p.95).[^kleppmann2026]
- **앞의 질의 — 미국에서 유럽으로 이동한 사람 찾기 — 는 SPARQL에서도 Cypher와 비슷하게 간결하다**
  (3장, p.95, 예제 3-10):[^kleppmann2026]

  ```sparql
  PREFIX : <urn:example:>

  SELECT ?personName WHERE {
    ?person :name ?personName.
    ?person :bornIn / :within* / :name "United States".
    ?person :livesIn / :within* / :name "Europe".
  }
  ```

- **구조가 매우 비슷하다.** 저자들이 짝지어 보여 주는 대응 (3장, p.95, SPARQL의 변수는 물음표로
  시작한다):[^kleppmann2026]
  - Cypher `(person) -[:BORN_IN]-> () -[:WITHIN*0..]-> (location)`
  - SPARQL `?person :bornIn / :within* ?location.`
- 한 가지가 더 단순해진다 — **RDF는 속성과 간선을 구별하지 않고 둘 다에 술어를 쓰므로, 속성을
  매칭하는 데도 같은 구문을 쓸 수 있다.** 그래서 Cypher의 `(usa {name:'United States'})`는
  SPARQL에서 `?usa :name "United States".` 가 된다 (3장, p.96).[^kleppmann2026]
- **SPARQL은 아마존 넵튠·AllegroGraph·Blazegraph·OpenLink Virtuoso·Apache Jena, 그리고 그 밖의
  여러 트리플 스토어가 지원한다** (3장, p.96).[^kleppmann2026]

## Datalog

- **Datalog는 SPARQL이나 Cypher보다 훨씬 오래된 언어로 1980년대의 학술 연구에서 나왔다.
  소프트웨어 엔지니어 사이에 덜 알려져 있고 주류 데이터베이스에서 널리 지원되지 않지만, 매우
  표현력이 높고 복잡한 질의에 특히 강력하므로 더 잘 알려져야 한다. Datomic·LogicBlox·CozoDB·
  링크드인의 LIquid를 포함한 여러 틈새 데이터베이스가 Datalog를 질의 언어로 쓴다** (3장,
  p.96).[^kleppmann2026]
- 위치가 특이하다 — **그것은 그래프가 아니라 관계형 데이터 모델에 기반하지만, 그래프에 대한 재귀
  질의가 Datalog의 특별한 강점이므로 여기서 논한다** (3장, p.96).[^kleppmann2026]
- **Datalog 데이터베이스의 내용은 사실(facts)이라 하며, 각 사실은 관계형 테이블의 한 행에
  대응한다. 예컨대 ID·name·type 세 열을 가진 location 테이블이 있다면 미국이 나라라는 사실은
  `location(2, "United States", "country")`로 쓸 수 있고 2는 미국의 ID다. 일반적으로
  `table(val1, val2, …)` 진술은 table이 첫 열에 val1, 둘째 열에 val2 등을 담은 행을 갖는다는
  뜻이다** (3장, p.96).[^kleppmann2026]
- 그래프의 간선은 조인 테이블이 된다 — **그래프의 간선(within·born_in·lives_in)은 두 열짜리
  조인 테이블로 표현된다. 예컨대 루시의 ID가 100이고 아이다호의 ID가 3이므로 "루시는 아이다호에서
  태어났다"는 관계는 `born_in(100, 3)`으로 표현된다** (3장, p.96).[^kleppmann2026]
- 같은 질의를 Datalog로 쓰면 이렇게 된다 (3장, p.97, 예제 3-12):[^kleppmann2026]

  ```prolog
  within_recursive(LocID, PlaceName) :- location(LocID, PlaceName, _). /* Rule 1 */

  within_recursive(LocID, PlaceName) :- within(LocID, ViaID),          /* Rule 2 */
                                        within_recursive(ViaID, PlaceName).

  migrated(PName, BornIn, LivingIn) :- person(PersonID, PName),        /* Rule 3 */
                                       born_in(PersonID, BornID),
                                       within_recursive(BornID, BornIn),
                                       lives_in(PersonID, LivingID),
                                       within_recursive(LivingID, LivingIn).

  us_to_europe(Person) :- migrated(Person, "United States", "Europe"). /* Rule 4 */
  ```

- 접근 방식이 다르다 — **Cypher와 SPARQL은 곧바로 SELECT로 뛰어들지만 Datalog는 한 번에 작은
  걸음을 뗀다. 우리는 바탕 사실에서 새로운 가상 테이블을 유도하는 규칙(rules)을 정의한다. 이
  유도된 테이블은 (가상) SQL 뷰와 비슷하다 — 데이터베이스에 저장되지 않지만 저장된 사실을 담은
  테이블과 같은 방식으로 질의할 수 있다** (3장, p.97).[^kleppmann2026]
- 규칙을 읽는 법 — **가상 테이블의 이름과 열은 각 규칙에서 `:-` 앞에 나타나는 것으로 정의된다.
  예컨대 `migrated(PName, BornIn, LivingIn)`은 사람의 이름, 태어난 곳의 이름, 살고 있는 곳의
  이름 세 열을 가진 가상 테이블이다. 가상 테이블의 내용은 `:-` 뒤의 부분으로 정의되며, 거기서
  우리는 테이블에서 어떤 패턴과 일치하는 행을 찾으려 한다. 예컨대 `person(PersonID, PName)`은
  행 `person(100, "Lucy")`와 일치하며, 변수 PersonID는 값 100에, 변수 PName은 값 "Lucy"에
  바인딩된다** (3장, p.97).[^kleppmann2026]
- 규칙이 적용되는 방식 — **`:-` 연산자 오른쪽의 모든 패턴에 대해 시스템이 일치를 찾을 수 있으면
  규칙이 적용된다. 규칙이 적용되면 `:-`의 왼쪽이 (변수가 그것이 일치한 값으로 대체되어)
  데이터베이스에 추가된 것처럼 된다** (3장, p.97).[^kleppmann2026]
- 재귀가 실제로 도는 모습 (3장, pp.97–98):[^kleppmann2026]
  1. **`location(1, "North America", "continent")`가 데이터베이스에 존재하므로 규칙 1이
     적용된다. 그것은 `within_recursive(1, "North America")`를 생성한다.**
  2. **`within(2, 1)`이 데이터베이스에 존재하고 앞 단계가 `within_recursive(1, "North
     America")`를 생성했으므로 규칙 2가 적용된다. 그것은 `within_recursive(2, "North
     America")`를 생성한다.**
  3. **`within(3, 2)`가 데이터베이스에 존재하고 앞 단계가 `within_recursive(2, "North
     America")`를 생성했으므로 규칙 2가 적용된다. 그것은 `within_recursive(3, "North
     America")`를 생성한다.**
- **규칙 1과 2를 반복 적용함으로써 within_recursive 가상 테이블은 데이터베이스에 담긴 북미(또는
  다른 어떤 위치) 안의 모든 위치를 알려 줄 수 있다. 이제 규칙 3이 어떤 위치 BornIn에서 태어나
  어떤 위치 LivingIn에 사는 사람을 찾을 수 있다. 규칙 4는 BornIn = 'United States'와
  LivingIn = 'Europe'로 규칙 3을 호출하고 검색에 일치하는 사람의 이름만 반환한다** (3장,
  p.98).[^kleppmann2026]
- 저자들의 평가 — **Datalog 접근은 이 장에서 논한 다른 질의 언어와 비교해 다른 종류의 사고를
  요구한다. 그것은 복잡한 질의가 규칙 하나하나로 쌓여 올라가게 하며, 한 규칙이 다른 규칙을
  참조하는 것은 코드를 서로 호출하는 함수로 쪼개는 방식과 비슷하다. 함수가 재귀적일 수 있듯이
  Datalog 규칙도 자기 자신을 호출할 수 있으며(예제의 규칙 2가 그렇다), 이것이 Datalog 질의에서
  그래프 순회를 가능하게 한다** (3장, p.98).[^kleppmann2026]

## 이 언어들의 진입 비용을 채점한 소스

- **아키텍처 쪽 소스 하나가 그래프 질의 언어를 "니치 기술"의 대표 예로 든다.** 포드 외는
  데이터베이스 종류를 고르는 절에서 학습 난이도 축을 규정하며 **대부분의 소프트웨어 개발자가
  SQL을 이해한다고 가정되는 반면 Gremlin(그래프 질의 언어) 같은 것은 니치 기술일 수 있다**고
  적는다 (6장 §"Selecting a Database Type", p.161).[^ford2021-hard-parts]
  - **그 판단이 별점으로 되돌아온다** — 같은 절에서 그래프 데이터베이스의 학습 난이도는 여덟
    갈래 가운데 최저인 1/5이고, 근거는 **노드·관계·관계 유형·속성을 어떻게 쓰는지 이해하는 데
    시간이 걸린다**는 것이다 (6장, p.172).[^ford2021-hard-parts] 그 채점표는
    [데이터베이스 종류 고르기](selecting-a-database-type.md)에 있다.
- **그쪽이 언어 지형을 한 문장으로 요약하는데 이 페이지의 계보와 어긋나지 않는다** —
  **Gremlin이라는 언어 프레임워크가 여러 다른 데이터베이스에 걸쳐 동작해 사용의 용이를 돕고,
  Neo4J는 Cypher라는 질의 언어를 지원한다**는 것이다 (6장, p.173).[^ford2021-hard-parts]
  - 버전 조건: 2021년 저술 시점이다. **그쪽에는 2024년 ISO 표준 GQL이 없다** — 이 페이지가
    적는 그 표준은 그 책보다 뒤의 일이다. SPARQL과 Datalog도 그쪽에 없다.
- **두 소스가 같은 언어를 다른 이유로 다룬다.** 이 페이지는 **무엇을 표현할 수 있는가**를 묻고,
  그쪽은 **그 언어를 아는 사람을 구할 수 있는가**를 묻는다. 그래서 그쪽의 별점 축 하나가
  통째로 **언어 지원·성숙도·SQL 지원·커뮤니티**이고 그 칸이 채용 가능성을 잰다 (6장,
  p.162).[^ford2021-hard-parts] **표현력 논의와 채택 논의는 다른 물음이다.**

## 이어지는 페이지

- [그래프 데이터 모델](../concepts/graph-data-models.md) — 이 언어들이 질의하는 그 두 모델
- [GraphQL](../concepts/graphql.md) — 이름에 그래프가 들어가지만 성격이 다른 넷째 언어
- [데이터 모델의 층](../concepts/data-model-layers.md) — 이 언어들이 공유하는 선언적 성질
- [데이터베이스 관리 시스템의 구조](../concepts/dbms-architecture.md) — 같은 질의를 어느 방향으로
  실행할지 고르는 최적화기
- [관계형 모델과 문서 모델](../concepts/relational-versus-document-model.md) — SQL과 문서 질의
  언어 쪽
- [데이터베이스 종류 고르기](selecting-a-database-type.md) — 이 언어들의 진입 비용이 종류
  선택의 한 축이 되는 자리

[^kleppmann2026]: Kleppmann & Riccomini 2026, 3장 "Data Models and Query Languages"

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 6장 "Pulling Apart Operational
    Data" §"Selecting a Database Type" 가운데 축 일곱의 규정(pp.161–162)과
    §"Graph Databases"(pp.171–173). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 이 페이지는 그
    절을 대질에만 쓴다 — 여덟 갈래의 별점표와 직인용은
    [데이터베이스 종류 고르기](selecting-a-database-type.md)가 갖는다. 별점 값은 그쪽에서
    도판을 렌더해 눈으로 센 것이고 텍스트 레이어에는 없다. 위 대비(표현력 대 채택 조건)는
    원문에 없고 **이 KB가 맞댄 것**이다.

---
type: concept
title: 서비스의 데이터 소유권
status: draft
description: 데이터베이스를 쪼갠 뒤 어느 서비스가 어느 테이블을 소유하는가 — 쓰기를 수행하는 서비스가 그 테이블의 주인이라는 어림 규칙과 그 규칙이 복잡해지는 세 시나리오(단일 소유권·공통 소유권·공동 소유권), 공통 소유권을 전담 서비스 하나와 지속 큐로 푸는 기법, 공동 소유권을 푸는 네 기법(테이블 쪼개기·데이터 도메인·위임·서비스 통합) 각각의 기제와 원문 절충표 넷, 위임 기법에서 주인을 고르는 두 선택지(주 도메인 우선과 운영 특성 우선)와 저자들의 권고, 네 기법을 한자리에 맞댄 표, 배정이 끝난 뒤 업무 워크플로로 검증하라는 다음 단계, 그리고 티켓 처리에 그 규칙을 대는 사가와 ADR 둘
generated: { by: "claude-opus-5", at: "2026-09-17T23:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 서비스의 데이터 소유권

- [소유권의 어림 규칙](#소유권의-어림-규칙)
- [예 하나가 시나리오 셋을 만든다](#예-하나가-시나리오-셋을-만든다)
- [단일 소유권](#단일-소유권)
- [공통 소유권](#공통-소유권)
- [공동 소유권](#공동-소유권)
- [기법 하나 - 테이블 쪼개기](#기법-하나---테이블-쪼개기)
- [기법 둘 - 데이터 도메인](#기법-둘---데이터-도메인)
- [기법 셋 - 위임](#기법-셋---위임)
- [위임의 주인을 고르는 두 선택지](#위임의-주인을-고르는-두-선택지)
- [기법 넷 - 서비스 통합](#기법-넷---서비스-통합)
- [네 기법을 한자리에 놓으면](#네-기법을-한자리에-놓으면)
- [배정의 결과와 그다음 단계](#배정의-결과와-그다음-단계)
- [책의 사례 - 티켓 처리의 데이터 소유권](#책의-사례---티켓-처리의-데이터-소유권)
- [6장의 데이터 도메인과 같은 것인가](#6장의-데이터-도메인과-같은-것인가)
- [데이터 메시의 도메인 소유권과 같은 낱말인가](#데이터-메시의-도메인-소유권과-같은-낱말인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터를 쪼갠 뒤 어느 서비스가 어느 테이블을 소유하며, 여러 서비스가 같은
테이블에 쓰는 자리는 무엇으로 푸는가.**

## 소유권의 어림 규칙

- **쪼갠 뒤에는 다시 붙여야 한다**는 것이 이 장의 전제다 — 데이터를 한 번 떼어 내고 나면
  체계가 돌아가게 하기 위해 도로 꿰매야 하고, 그것은 **어느 서비스가 어느 데이터를 소유하는가,
  분산 트랜잭션을 어떻게 관리하는가, 더 이상 소유하지 않는 데이터에 서비스가 어떻게 접근하는가**를
  알아내는 일이다 (9장, p.250).[^ford2021-hard-parts]
- **소유권 배정은 들리는 것만큼 쉽지 않고, 그래서 이 책이 말하는 "어려운 부분"의 하나가 된다**
  (9장 §"Assigning Data Ownership", p.250).[^ford2021-hard-parts] 어림 규칙 자체는 한 줄이다
  (9장, p.250):[^ford2021-hard-parts]

  > The general rule of thumb for assigning table ownership states that services that per-
  > form write operations to a table own that table.

- **읽기는 소유권을 만들지 않는다.** 규칙이 쓰기 연산만 보므로, 다른 서비스가 그 테이블을
  읽어야 한다는 사실은 주인을 바꾸지 않는다 (9장, p.251).[^ford2021-hard-parts]
- 저자들이 본문과 떼어 큰 글씨로 조판한 조문이 규칙과 그 한계를 함께 적는다 (9장,
  p.250):[^ford2021-hard-parts]

  > The general rule of thumb for data ownership is that the service that performs write
  > operations to a table is the owner of that table. However, joint ownership makes this simple
  > rule complex!

- **규칙이 잘 듣는 것은 단일 소유권(single ownership)뿐이다** — 한 서비스만 그 테이블에 쓰는
  경우다. **공동 소유권(joint ownership, 여러 서비스가 같은 테이블에 쓴다)에서 지저분해지고,
  공통 소유권(common ownership, 대부분 또는 모든 서비스가 그 테이블에 쓴다)에서는 더
  나빠진다** (9장, p.250).[^ford2021-hard-parts]

## 예 하나가 시나리오 셋을 만든다

- **저자들이 장 전체의 공통 참조점으로 쓰는 예가 하나다** (그림 9-1, 9장,
  pp.250–251).[^ford2021-hard-parts] 서비스 셋과 테이블 넷이다.
  - **Wishlist Service** — 고객의 위시리스트 전부를 관리한다. `Wishlist` 테이블과 `Audit`
    테이블에 쓴다.
  - **Catalog Service** — 제품 카탈로그를 유지한다. `Product` 테이블과 `Audit` 테이블에 쓴다.
  - **Inventory Service** — 카탈로그의 모든 제품에 대해 재고와 재입고 기능을 유지한다.
    `Product` 테이블과 `Audit` 테이블에 쓴다.
- **이 단순한 실세계 예 하나가 소유권 배정을 복잡하고 헷갈리는 일로 만든다**고 저자들이 적는다
  (9장, p.251).[^ford2021-hard-parts] 테이블 하나마다 시나리오가 다르기 때문이다 — `Wishlist`는
  단일 소유권, `Audit`은 공통 소유권, `Product`는 공동 소유권이다.
- **그리고 도판 규약이 하나 선다** — 테이블을 소유 서비스의 상자 **안**에 그리는 조판이
  서비스와 그 데이터 사이에 맺어진 **경계 컨텍스트(bounded context)를 나타내는 효과적인
  방법**이라고 저자들이 적는다 (9장, p.251).[^ford2021-hard-parts] 그 어휘의 정본은
  [경계 컨텍스트](../concepts/bounded-context.md)에 있다.

## 단일 소유권

- 규정은 한 줄이다 (9장 §"Single Ownership Scenario", p.251):[^ford2021-hard-parts]

  > *Single table ownership* occurs when only one service writes to a table.

- **세 시나리오 가운데 가장 단순하고 풀기도 비교적 쉽다** (9장, p.251).[^ford2021-hard-parts]
  `Wishlist` 테이블에 쓰는 서비스는 Wishlist Service 하나뿐이므로, **다른 서비스가 읽기 전용
  접근을 필요로 하든 말든** 그 테이블의 주인은 Wishlist Service다 (9장,
  p.251).[^ford2021-hard-parts]
- **저자들의 절차 권고가 여기 붙는다** — 이 시나리오가 단순하기 때문에 **단일 테이블 소유권
  관계를 먼저 처리해 판을 정리한 뒤**에 더 복잡한 공통 소유권과 공동 소유권을 다루라는 것이다
  (9장, p.252).[^ford2021-hard-parts]

## 공통 소유권

- 규정은 한 줄이다 (9장 §"Common Ownership Scenario", p.252):[^ford2021-hard-parts]

  > *Common table ownership* occurs when most (or all) of the services need to write to the
  > same table.

- `Audit` 테이블이 그 예다 — 모든 서비스가 사용자가 수행한 동작을 기록하려고 거기 쓰므로
  **누가 실제로 소유해야 하는지 정하기 어렵다.** 예의 서비스는 셋뿐이지만, 저자들은 **수백
  또는 수천 개의 서비스가 같은 감사 테이블에 써야 하는 더 현실적인 예를 상상해 보라**고 적는다
  (9장, p.252).[^ford2021-hard-parts]
- **가장 쉬운 답이 기각된다** — 감사 테이블을 모두가 쓰는 공유 데이터베이스나 공유 스키마에
  그냥 두는 해법은 **6장 첫머리가 서술한 데이터 공유의 문제 전부를 도로 들여온다.** 변경
  통제(change control), 커넥션 고갈(connection starvation), 확장성, 내결함성이다 (9장,
  p.252).[^ford2021-hard-parts] 그 넷의 전문은
  [데이터 분해의 구동 요인](../concepts/data-decomposition-drivers.md)에 있다.
- **널리 쓰이는 기법은 전담 서비스 하나를 세우는 것이다** — 그 데이터의 **주(primary)이자
  유일한 소유자로 전담 서비스 하나를 배정해 그 서비스만 테이블에 쓰게 하고**, 쓰기가 필요한
  다른 서비스들은 그 전담 서비스에 정보를 보내 대신 쓰게 한다 (9장,
  p.252).[^ford2021-hard-parts]
- **보내는 쪽 통신 방식이 필요한 회신에 따라 갈린다** (9장, p.253):[^ford2021-hard-parts]
  - **정보나 확인 응답이 필요 없으면** 지속 큐(persisted queue)를 써서 비동기로 보내고 잊는
    메시징(fire-and-forget)을 쓴다.
  - **쓰기 동작의 결과로 호출자에게 돌려줄 정보가 있으면**(확인 번호나 데이터베이스 키 같은
    것) REST·gRPC·요청-응답 메시징(request-reply messaging, 유사 동기) 같은 것으로 동기
    호출을 한다.
- 예의 감사 테이블에서 저자들이 고르는 것은 앞쪽이다 — 새 `Audit Service`를 만들어 `Audit`
  테이블의 소유권을 주고, **그 서비스만 그 테이블에 읽고 쓴다.** 돌려줄 정보가 없으므로 세
  서비스는 **지속 큐를 통한 비동기 fire-and-forget 메시징**을 쓰고 감사 레코드가 쓰이기를
  기다리지 않는다. **큐를 지속으로 만든다는 것은 브로커가 메시지를 디스크에 저장한다는 뜻**이고,
  이것이 서비스나 브로커 장애 시 **보장 전달(guaranteed delivery)**을 주어 메시지가 유실되지
  않게 돕는다 (그림 9-3, 9장, p.253).[^ford2021-hard-parts] 그 기제의 전문은
  [메시징 패턴](../synthesis/messaging-patterns.md) 쪽에 있다.
- **소유하지 않은 공통 데이터를 읽어야 하는 경우가 남는다** — 그 읽기 전용 접근 기법들은
  10장이 다룬다고 저자들이 넘긴다 (9장, p.253).[^ford2021-hard-parts]

## 공동 소유권

- 규정은 한 줄이다 (9장 §"Joint Ownership Scenario", p.253):[^ford2021-hard-parts]

  > One of the more common (and complex) scenarios involving data ownership is *joint*
  > *ownership*, which occurs when multiple services perform write actions on the same table.

- **공통 소유권과 갈리는 것은 서비스의 수와 도메인이다** — 공동 소유권에서는 **같은 도메인
  안의 서비스 두어 개**가 같은 테이블에 쓰고, 공통 소유권에서는 **대부분 또는 모든 서비스**가
  쓴다 (9장, pp.253–254).[^ford2021-hard-parts] 예에서 `Audit`은 모든 서비스가 쓰므로 공통이고,
  `Product`는 Catalog와 Inventory 둘만 쓰므로 공동이다.
- 그 둘이 무엇을 쓰는지가 기법 선택의 재료가 된다 (그림 9-4, 9장,
  p.254).[^ford2021-hard-parts]
  - **Catalog Service** — 새 제품을 테이블에 넣고, 더 이상 제공하지 않는 제품을 지우고,
    정적 제품 정보가 바뀌면 갱신한다.
  - **Inventory Service** — 제품이 조회·판매·반품될 때 **각 제품의 현재 재고를 읽고 갱신**한다.
- **기법이 넷 있다** — 테이블 쪼개기(table split technique), 데이터 도메인(data domain
  technique), 위임(delegation technique), 서비스 통합(service consolidation technique)이다
  (9장, p.254).[^ford2021-hard-parts]
  - **원문이 셋째 기법의 이름을 두 가지로 적는다** — 이 목록과 사가와 ADR과 그림 9-21은
    `delegation technique`이라 적고, 절 제목과 본문과 표 9-3은 `delegate technique`이라 적는다.
    이 페이지는 절 제목 쪽을 표제로 삼고 그 어긋남을 각주에 적었다.

## 기법 하나 - 테이블 쪼개기

- 규정은 한 줄이다 (9장 §"Table Split Technique", p.254):[^ford2021-hard-parts]

  > The *table split technique* breaks a single table into multiple tables so that each service
  > owns a part of the data it's responsible for.

- **저자들이 이 기법의 출처를 밖에 댄다** — *Refactoring Databases*라는 책과 그 동반
  웹사이트에 상세히 서술돼 있다는 것이다 (9장, p.254).[^ford2021-hard-parts] **이 KB가 확인한
  원전이 아니다.**
- 절차가 셋이다 (9장, p.254).[^ford2021-hard-parts]
  1. 제품 ID(키)와 재고 수량(가용 품목 수)을 담는 **별도 `Inventory` 테이블을 만든다.**
  2. 기존 `Product` 테이블의 데이터로 **그 테이블을 미리 채운다.**
  3. `Product` 테이블에서 **재고 수량 열을 지운다.**
- **저자들이 그 셋을 관계형 데이터베이스의 DDL 목록으로 보인다**(예제 9-1, 9장, p.255) —
  `CREATE TABLE Inventory`로 `product_id VARCHAR(10)`과 `inv_cnt INT` 둘을 만들고, `Product`에서
  두 열을 읽어 넣는 `INSERT`와 `COMMIT`을 거쳐, `ALTER TABLE Product DROP COLUMN inv_cnt`로
  닫는다.[^ford2021-hard-parts]
  - **그 목록을 펜스로 옮기지 않았다.** 가운데 문장이 `INSERT INTO Inventory VALUES
    (product_id, inv_cnt) AS SELECT product_id, inv_cnt FROM Product;`인데 **`VALUES` 절과
    `AS SELECT`를 함께 쓰는 문법은 표준 SQL에도 주요 방언에도 없어** 그대로 복사하면 돌지
    않는다. 렌더와 두 추출기 모두에서 같은 문장이라 원문 오식이고, 이 KB는 고치지 않았다.
    절차와 식별자는 위 산문에 남았다.
- **쪼개고 나면 공동 소유권이 단일 소유권으로 바뀐다** — Catalog Service가 `Product`
  테이블의 데이터를 소유하고 Inventory Service가 `Inventory` 테이블의 데이터를 소유한다
  (9장, p.255).[^ford2021-hard-parts]
- **대신 두 서비스 사이에 통신이 생긴다** — 제품이 만들어지거나 지워질 때 두 테이블의 데이터가
  일관되게 남으려면 Catalog Service와 Inventory Service가 말을 해야 한다 (그림 9-5, 9장,
  p.255).[^ford2021-hard-parts]
  - 새 제품이 더해지면 Catalog Service가 제품 ID를 만들어 `Product`에 넣은 **다음** 그 ID(와
    경우에 따라 초기 재고 수량)를 Inventory Service에 보내야 한다.
  - 제품이 지워지면 Catalog Service가 먼저 `Product`에서 지운 **다음** Inventory Service에
    알려 `Inventory`의 재고 행을 지우게 해야 한다.
- **쪼갠 테이블 사이의 동기화는 사소한 일이 아니다** (9장, p.255).[^ford2021-hard-parts]
  저자들이 남기는 어려운 물음이 둘이다 — 두 서비스 사이의 통신은 동기여야 하는가 비동기여야
  하는가, 그리고 제품을 더하거나 지우는데 Inventory Service가 살아 있지 않으면 Catalog
  Service는 무엇을 해야 하는가.
- **그 답을 가용성 대 일관성의 절충이 몬다** (9장, pp.255–256).[^ford2021-hard-parts]
  - **가용성을 고른다**는 것은 대응하는 재고 레코드가 만들어지지 않더라도 Catalog Service가
    **언제나 제품을 더하고 지울 수 있는 것이 더 중요하다**는 뜻이다.
  - **일관성을 고른다**는 것은 두 테이블이 **언제나 서로 맞아 있는 것이 더 중요하다**는
    뜻이고, 그러면 Inventory Service가 살아 있지 않을 때 제품 생성·삭제가 실패한다.
  - **분산 아키텍처에서는 네트워크 분할이 필연이므로 CAP 정리가 둘 중 하나만 가능하다고 말한다**는
    것이 저자들의 근거다 (9장, p.256).[^ford2021-hard-parts] 그 정리의 전문과 이 거친 라벨에
    붙는 단서는 [CAP과 PACELC](../concepts/cap-and-pacelc.md)에 있다.
- **통신 프로토콜의 선택도 같은 저울에 붙는다** (9장, p.256).[^ford2021-hard-parts] 새 제품을
  만들 때 대응하는 재고 레코드가 더해졌다는 확인이 필요하면 **동기 통신**이라 성능을 내주고
  데이터 일관성을 사고, 확인이 필요 없으면 **비동기 fire-and-forget**이라 데이터 일관성을
  내주고 성능을 산다.
- **표 9-1의 열 머리글과 값을 그대로 옮긴다** (9장, p.256):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| Preserves bounded context | Tables must be altered and restructured |
| Single data ownership | Possible data consistency issues |
| | No ACID transaction between table updates |
| | Data synchronization is difficult |
| | Data replication between tables may occur |

## 기법 둘 - 데이터 도메인

- 규정은 두 줄이다 (9장 §"Data Domain Technique", p.256):[^ford2021-hard-parts]

  > Another technique for joint ownership is to create a shared *data domain*. This is
  > formed when data ownership is shared between the services, thus creating multiple
  > owners for the table.

- **기제는 스키마를 합치는 것이다** — 같은 서비스들이 공유하는 테이블을 **같은 스키마나 같은
  데이터베이스에 넣어** 서비스와 데이터 사이에 **더 넓은 경계 컨텍스트**를 이룬다 (9장,
  p.256).[^ford2021-hard-parts]
- **도판 규약이 여기서 달라진다** — 그림 9-6은 그림 9-4와 거의 같아 보이지만 한 가지가 다르다.
  `Product` 테이블이 **어느 소유 서비스의 맥락에도 속하지 않는 별도의 상자**로 밖에 놓인다.
  그 조판이 **그 테이블이 어느 한쪽의 경계 컨텍스트에 속하거나 소유되는 것이 아니라 둘 사이의
  더 넓은 경계 컨텍스트에서 공유된다**는 것을 분명히 한다 (9장, p.257).[^ford2021-hard-parts]
- **분산 아키텍처에서 데이터 공유는 대체로 권장되지 않는데**(특히 마이크로서비스에서) 이 기법은
  다른 공동 소유권 기법들이 앓는 **성능·가용성·데이터 일관성 문제 일부를 해소한다** (9장,
  p.257).[^ford2021-hard-parts] 두 서비스가 서로에게 의존하지 않기 때문이다 — Catalog
  Service는 Inventory Service와 조율하지 않고 제품을 만들거나 지우고, Inventory Service는
  Catalog Service 없이 재고를 조정한다. **둘이 서로에게서 완전히 독립이 된다.**
- **저자들이 곁상자로 제동을 건다** — 이 기법을 고를 때는 **데이터가 서로에게 공통인데 왜
  별도의 서비스가 필요한지를 언제나 다시 따져 보라**는 것이다. 정당화가 될 만한 것으로는
  확장성 차이, 내결함성 요구, 처리량 차이, 코드 변동성 격리가 있고 7장을 가리킨다 (9장,
  p.257).[^ford2021-hard-parts] 그 여섯 요인의 전문은 [서비스 세분도](../concepts/service-granularity.md)에
  있다.
- **대신 문제가 둘 생긴다** (9장, pp.257–258).[^ford2021-hard-parts]
  - **첫째는 데이터 구조 변경의 비용이다.** 더 넓은 경계 컨텍스트가 맺어지므로 공유 테이블
    구조를 바꾸면 그 변경을 **여러 서비스에 걸쳐 조율**해야 할 수 있고, 이것이 개발 노력과
    테스트 범위와 배포 위험을 키운다.
  - **둘째는 쓰기 책임의 통제다.** 어느 서비스가 어느 데이터에 쓸 책임을 갖는지를 통제하는
    문제인데, 상관없는 경우도 있지만 **특정 데이터에 대한 쓰기를 통제하는 것이 중요하다면
    테이블별·열별 쓰기 소유권을 유지하는 거버넌스 규칙을 따로 적용하는 노력이 더 든다.**
- **표 9-2의 열 머리글과 값을 그대로 옮긴다** (9장, p.258):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| Good data access performance | Data schema changes involve more services |
| No scalability and throughput issues | Increased testing scope for data schema changes |
| Data remains consistent | Data ownership governance (write responsibility) |
| No service dependency | Increased deployment risk for data schema changes |

## 기법 셋 - 위임

- 규정은 두 줄이다 (9장 §"Delegate Technique", p.258):[^ford2021-hard-parts]

  > An alternative method for addressing the joint ownership scenario is the *delegate*
  > *technique*. With this technique, one service is assigned single ownership of the table and
  > becomes the delegate, and the other service (or services) communicates with the delegate to
  > perform updates on its behalf.

- **이 기법은 서비스 사이 통신을 언제나 강제한다** — 앞의 공통 소유권 시나리오와 같이, 데이터를
  갱신해야 하는 다른 서비스들이 **원격 접근 프로토콜로 위임 서비스에 갱신을 보내고** 그쪽이
  대신 수행한다. 그 통신은 동기일 수도 비동기일 수도 있다 (9장, p.259).[^ford2021-hard-parts]
  - **동기로 하면** 비소유 서비스가 갱신이 끝나기를 기다려야 해 **전체 성능에 영향**을 주지만
    데이터 일관성이 보장된다.
  - **비동기로 하면** 비소유 서비스는 훨씬 빨라지지만 데이터가 **최종적으로만 일관**해진다.
    게다가 갱신을 시도하는 동안 소유 서비스 쪽에서 오류가 날 수 있으므로 비소유 서비스는
    **갱신이 실제로 됐다는 보장을 전혀 갖지 못하고**, 이것이 데이터 무결성에도 영향을 준다
    (9장, p.259).[^ford2021-hard-parts]
- **저자들이 이 기법의 적용 조건을 좁혀서 적는다** — 주인이 누구든 위임 기법은 **서비스 결합과
  서비스 사이 통신의 필요**라는 큰 단점을 갖고, 그것이 비위임 서비스 쪽에 **원자적 트랜잭션의
  부재, 네트워크와 처리 지연에 따른 낮은 성능, 낮은 내결함성**을 부른다. 그래서 이 기법은
  **원자적 트랜잭션을 요구하지 않고 비동기 통신을 통한 최종 일관성을 견딜 수 있는 쓰기
  시나리오에 대체로 더 알맞다** (9장, p.260).[^ford2021-hard-parts]
- **표 9-3의 열 머리글과 값을 그대로 옮긴다** (9장, p.261):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| Forms single table ownership | High level of service coupling |
| Good data schema change control | Low performance for nonowner writes |
| Abstracts data structures from other services | No atomic transaction for nonowner writes |
| | Low fault tolerance for nonowner services |

## 위임의 주인을 고르는 두 선택지

- **이 기법의 어려움은 누구를 위임 서비스로 삼을 것인가다** (9장, p.258).[^ford2021-hard-parts]
  선택지가 둘이고 이름이 붙어 있다.

| 선택지 | 원어 | 누구에게 테이블을 주는가 |
|---|---|---|
| 주 도메인 우선 | primary domain priority | 그 데이터의 **주 도메인을 가장 가깝게 대표하는 서비스**, 곧 해당 도메인 안에서 그 개체의 주요 CRUD 연산을 가장 많이 하는 서비스 |
| 운영 특성 우선 | operational characteristics priority | **더 높은 운영 아키텍처 특성을 필요로 하는 서비스**(성능·확장성·가용성·처리량 따위) |

- **주 도메인 우선을 예에 대면** 제품 정보의 CRUD 연산을 대부분 수행하는 Catalog Service가
  테이블의 단일 소유자가 되고, Inventory Service는 테이블을 소유하지 않으므로 재고 수량을
  읽거나 갱신하려면 Catalog Service와 통신해야 한다 (그림 9-7, 9장,
  p.259).[^ford2021-hard-parts]
- **운영 특성 우선을 대면 역할이 뒤집힌다** — 재고 갱신이 정적 제품 데이터보다 훨씬 빠른
  속도로 일어나기 때문이다. 정당화는 **제품 재고 갱신이 제품 구매라는 잦은 실시간 트랜잭션
  처리의 일부**인 데 반해 제품 정보 갱신이나 제품 추가·삭제는 **더 드문 관리 작업**이라는
  것이다 (그림 9-8, 9장, p.259).[^ford2021-hard-parts]
  - 그러면 잦은 재고 갱신이 원격 접근 프로토콜 대신 **직접 데이터베이스 호출**을 쓸 수 있어
    훨씬 빠르고 신뢰할 수 있게 되고, **가장 변동이 심한 데이터(재고 수량)가 높은 일관성을
    유지한다** (9장, p.260).[^ford2021-hard-parts]
- **저자들은 그럼에도 앞쪽을 권한다.** 운영 특성 우선의 큰 문제가 **도메인 관리 책임**이기
  때문이다 — Inventory Service가 책임지는 것은 제품 재고 관리이지, 정적 제품 정보를 더하고
  지우고 갱신하는 데이터베이스 활동과 그에 딸린 오류 처리가 아니다. 그래서 저자들은 **대개
  도메인 우선 선택지를 권하고**, 성능과 내결함성 문제는 **복제된 인메모리 캐시나 분산 캐시
  같은 것**으로 다루라고 적는다 (9장, p.260).[^ford2021-hard-parts] 그 기제의 전문은
  [분산 시스템에서의 캐싱](../concepts/caching-in-distributed-systems.md)에 있다.

## 기법 넷 - 서비스 통합

- **앞 기법이 드러낸 문제가 이 기법의 출발점이다** — 위임 접근이 부각한 공동 소유권의 주된
  문제가 **서비스 의존**이라는 것이다 (9장, p.261).[^ford2021-hard-parts] 규정은 한 줄이다
  (9장 §"Service Consolidation Technique", p.261):[^ford2021-hard-parts]

  > The *service consolidation technique* resolves service dependency and addresses joint
  > ownership by combining multiple table owners (services) into a single consolidated service,
  > thus moving joint ownership into a single ownership scenario

- **데이터 도메인 기법처럼 서비스 의존과 성능 문제를 함께 해소하면서 공동 소유권 문제도
  다룬다.** 다만 값이 있다 (그림 9-9, 9장, p.261).[^ford2021-hard-parts]
  - 서비스를 합치면 **더 굵은(coarse-grained) 서비스**가 되어 전체 테스트 범위와 배포 위험
    (새 기능을 더하거나 버그를 고칠 때 서비스 안의 다른 것을 깨뜨릴 가능성)이 커진다.
  - **전체 내결함성도 영향을 받는다** — 서비스의 모든 부분이 함께 죽기 때문이다.
  - **확장성도 영향을 받는다** — 서비스의 **모든** 부분이 똑같이 확장돼야 하는데 일부 기능은
    다른 기능만큼 확장할 필요가 없을 수 있다. 예에서 카탈로그 유지 기능은 재고 조회·갱신의
    높은 요구에 맞춰 **불필요하게** 확장된다 (9장, p.262).[^ford2021-hard-parts]
- **표 9-4의 열 머리글과 값을 그대로 옮긴다** (9장, p.262):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| Preserves atomic transactions | More coarse-grained scalability |
| Good overall performance | Less fault tolerance |
| | Increased deployment risk |
| | Increased testing scope |

- **이 기법만이 원자적 트랜잭션을 보존한다** — 위 표 넷을 나란히 놓으면 `Preserves atomic
  transactions`를 이점으로 적는 것이 이 표 하나다. 앞의 셋 가운데 둘은 그 부재를 단점으로
  적는다(표 9-1의 `No ACID transaction between table updates`, 표 9-3의 `No atomic
  transaction for nonowner writes`). **이 대조는 네 표를 맞대어 이 KB가 세운 것이고 저자들이
  그 비교를 따로 적지는 않는다.**
- **이 기법은 7장의 통합 요인과 같은 조작이다** — 쪼개 놓은 것을 도로 붙여 굵게 만드는 것이고,
  7장이 데이터베이스 트랜잭션을 통합 요인의 첫째로 놓는 자리와 짝을 이룬다. 그쪽 저울은
  [서비스 세분도](../concepts/service-granularity.md)에 있다.

## 네 기법을 한자리에 놓으면

**아래 표는 원문에 없고 위 네 절의 값을 이 KB가 모은 것이다.** 낱말과 판정은 각 절의 각주가
가리키는 쪽에서 왔다.

| 기법 | 무엇을 움직이는가 | 소유권이 어디로 가는가 | 원자적 트랜잭션 | 서비스 의존 |
|---|---|---|---|---|
| 테이블 쪼개기 | **테이블** | 둘 다 단일 소유권 | 없다(테이블 갱신 사이) | 생긴다(동기화 통신) |
| 데이터 도메인 | **스키마 경계** | 여럿이 공유(더 넓은 경계 컨텍스트) | 데이터가 일관하게 남는다 | 없다 |
| 위임 | **쓰기 경로** | 한 서비스가 단일 소유 | 없다(비소유 쓰기) | 높다 |
| 서비스 통합 | **서비스 경계** | 하나로 합쳐 단일 소유권 | **보존된다** | 없다(하나가 됐다) |

- **넷이 움직이는 대상이 다르다는 것이 고르는 축이다.** 테이블 쪼개기는 데이터를, 데이터
  도메인은 스키마의 테두리를, 위임은 쓰기가 지나는 길을, 서비스 통합은 배포 단위를 움직인다.
  #hypothesis **저자들이 이 축을 명시하지는 않는다** — 네 절을 나란히 두고 각각의 절충표만
  붙인다.

## 배정의 결과와 그다음 단계

- **예의 세 시나리오에 기법을 적용한 결과가 그림 9-10이다** (9장,
  pp.262–263).[^ford2021-hard-parts] 도판이 이미지 조판이라 `pdftoppm -r 160 -png`로 렌더해
  눈으로 읽었고, 상자의 이름과 배치만 옮긴다.
  - **단일 테이블 시나리오**(`Wishlist`) — 그냥 Wishlist Service에 소유권을 주어 서비스와
    테이블 사이에 단단한 경계 컨텍스트를 맺었다.
  - **공통 소유권 시나리오**(`Audit`) — 새 Audit Service를 만들고 다른 서비스들은 모두 지속
    큐로 비동기 메시지를 보낸다.
  - **공동 소유권 시나리오**(`Product`) — **위임 기법을 골라** Catalog Service에 단일 소유권을
    주고 Inventory Service가 갱신 요청을 Catalog Service에 보낸다.
- **이 절에는 요약 표가 없다.** `Data Ownership Summary`라는 절 제목 아래 있는 것은 그림
  9-10과 그 산문뿐이다. 이 장의 표는 절충표 일곱(9-1에서 9-7까지)이 전부다.
- **소유권 배정이 끝이 아니다** — 테이블 소유권이 배정되고 나면 아키텍트는 **업무 워크플로와
  그에 딸린 트랜잭션 요구를 분석해 그 배정을 검증해야 한다** (9장,
  p.262).[^ford2021-hard-parts] 그 분석이 같은 장의 다음 절인 분산 트랜잭션이고, 정합성 쪽
  선택지는 [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md)에 있다.

## 책의 사례 - 티켓 처리의 데이터 소유권

**이 장의 여는 사가와 닫는 사가가 같은 물음을 둘러싼다.** 서사체로 조판돼 있으므로 여기서는
그 장면이 남기는 판정만 옮긴다. 예제 자체의 설정은 [Sysops Squad 사례](../concepts/sysops-squad-case.md)에
있다.

- **여는 사가가 이 장의 물음을 세운다** (9장, pp.249–250, 사가).[^ford2021-hard-parts] 전문가
  프로필 테이블을 어느 경계 컨텍스트에 넣을 것인가를 두고 두 아키텍트가 갈린다. 한쪽은
  **배정 알고리즘이 그 테이블을 끊임없이 질의하므로** Ticket Assignment 서비스 쪽에 두자 하고,
  다른 쪽은 **그 테이블에 실제로 갱신을 수행하는 것은 User Maintenance 서비스이므로** 그쪽이
  소유해야 한다고 본다.
  - **그 다툼을 끝내는 것은 앞 장에서 온 제약 하나다** — **여러 서비스가 같은 데이터베이스
    스키마에 접속하는 것은 괜찮지만, 한 서비스가 여러 데이터베이스나 스키마에 접속하는 것은
    안 된다**는 규칙이다 (9장, p.250, 사가).[^ford2021-hard-parts] 이 규칙이 "그러면 User
    Maintenance가 다른 데이터베이스에 붙으면 되지 않느냐"는 해법을 막는다.
- **닫는 사가가 규칙을 두 번 적용한다** (9장, pp.279–282, 사가).[^ford2021-hard-parts]
  - **첫째는 단일 테이블 소유권이다** — 읽기 전용으로 접근해야 하는 서비스가 무엇이든,
    **데이터 테이블에 쓰기 동작을 수행하는 서비스가 그 테이블을 소유한다.** 그래서 User
    Maintenance 서비스가 소유한다.
  - **둘째는 설문 테이블의 공동 소유권이다** — Ticket Completion 서비스가 티켓 완료 시각과
    수행한 전문가를 쓰고, Survey 서비스가 설문 발송 시각과 수신된 설문 결과를 쓴다. **둘 다
    같은 테이블에 쓴다.**
  - **선택지가 둘로 좁혀진다** — 테이블 구조 때문에 **테이블 쪼개기는 선택지가 아니라고**
    등장인물이 판정하므로, 공통 데이터 도메인이거나 위임이다.
  - **데이터 도메인이 기각되는 근거가 위 제약이다** — Ticket Completion 서비스가 이미 공통
    티케팅 데이터 도메인에 말하고 있는데 **한 서비스가 여러 스키마에 접속할 수 없기** 때문이다.
    설문 테이블을 티케팅 데이터 도메인 스키마에 그냥 더하자는 대안도 **곧 모놀리식 데이터베이스로
    되돌아간다**는 이유로 기각된다.
  - **채택된 해법은 이미 있던 메시지에 데이터를 실어 보내는 것이다** — Ticket Completion
    서비스가 티켓 완료 시 설문 프로세스를 띄우려고 **어차피 Survey 서비스에 메시지를 보내야
    하므로**, 필요한 데이터를 그 메시지에 함께 실으면 Survey 서비스가 고객 설문을 만들 때 그
    데이터를 넣을 수 있고 **Ticket Completion 서비스는 설문 테이블에 접근할 필요가 전혀
    없어진다** (그림 9-21, 9장, p.281, 사가).[^ford2021-hard-parts]
- **ADR 둘이 그 결정을 적는다** (9장, pp.280–281, ADR).[^ford2021-hard-parts] 형식의 정본은
  [아키텍처 결정 기록](../concepts/architecture-decision-records.md)에 있다.

| ADR | 무엇을 정하는가 | 귀결 칸이 적는 것 |
|---|---|---|
| Single Table Ownership for Bounded Contexts (p.280) | 한 서비스만 테이블에 쓰면 그 서비스가 소유한다. **그리고 다른 경계 컨텍스트의 테이블에 읽기 전용 접근이 필요한 서비스는 그 테이블이 든 데이터베이스나 스키마에 직접 접근할 수 없다** | 쓰는 기법에 따라 **다른 경계 컨텍스트의 데이터에 접근할 때 성능과 내결함성 문제**를 겪을 수 있다 |
| Survey Service Owns the Survey Table (p.281) | Survey 서비스가 설문 테이블의 단일 소유자이고 그 테이블에 쓰기를 수행할 수 있는 유일한 서비스다 | Ticket Completion 서비스가 넣어야 할 데이터 전부를 **설문 프로세스를 띄우는 페이로드에 실어 보내야** 하고, **모놀리스에서 완료 처리의 일부였던 설문 레코드 생성이 이제 별도 활동이 되어 Survey 서비스가 맡는다** |

- **첫째 ADR이 소유권 규칙에 조항을 하나 더한다** — 본문의 어림 규칙은 "쓰는 자가 주인"까지인데,
  이 ADR의 결정 칸은 거기에 **읽기 전용 접근자가 다른 경계 컨텍스트의 데이터베이스나 스키마에
  직접 접근할 수 없다**는 금지를 붙인다 (9장, p.280, ADR).[^ford2021-hard-parts] 본문이 그
  금지를 같은 세기로 적지는 않는다.
- **둘째 ADR이 보이는 것은 소유권 결정이 업무 절차를 옮긴다는 것이다** — 모놀리스에서 한
  완료 처리의 일부였던 일이 별도 활동이 되어 다른 서비스로 간다. **소유권 배정이 데이터만
  옮기는 것이 아니라는 실물이다.** #hypothesis 저자들이 그 일반화를 적지는 않는다.

## 6장의 데이터 도메인과 같은 것인가

**같은 낱말이고 같은 것을 가리키되 쓰임이 다르다.**

- **6장의 데이터 도메인은 분해의 매개다** — 모놀리식 데이터베이스를 쪼갤 때 테이블들을 배정할
  중간 단위이고, 다섯 단계 절차의 첫 두 단계가 그것을 만들고 테이블을 배정하는 일이다. 전문은
  [모놀리식 데이터를 쪼개는 다섯 단계](../concepts/decomposing-monolithic-data.md)에 있다.
- **9장의 데이터 도메인은 공동 소유권을 푸는 네 기법 중 하나다** — 이미 쪼개 놓은 뒤 두
  서비스가 같은 테이블에 쓰는 자리에서 **그 테이블을 둘의 공유 스키마에 두어 소유자를
  여럿으로 만드는** 선택이다.
- **그래서 같은 조작이 6장에서는 절차의 기본 뼈대이고 9장에서는 네 선택지 중 하나다.** 9장이
  그 기법의 단점으로 드는 것(스키마 변경이 여러 서비스에 걸린다, 쓰기 책임의 거버넌스가
  필요하다)은 6장의 절차가 도메인을 만들 때 이미 안고 가는 값이기도 하다. **두 장이 서로를
  이 자리에서 호명하지는 않는다.**

## 데이터 메시의 도메인 소유권과 같은 낱말인가

**같은 낱말이 다른 대상을 가리킨다. 섞으면 안 된다.**

| | 이 페이지(ford2021-hard-parts 9장) | [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) |
|---|---|---|
| 소유의 대상 | **운영 테이블 하나** | **분석 데이터 전체**(도메인이 내놓는 데이터 제품) |
| 소유자 | **서비스**(배포 단위) | **도메인**(업무 갈래와 그 팀) |
| 무엇으로 소유를 판정하는가 | **쓰기 연산을 누가 수행하는가** | 그 데이터가 어느 도메인의 실재를 표현하는가 |
| 푸는 문제 | 쪼갠 뒤 테이블에 주인이 없다 | 분석 데이터가 중앙 팀에 모여 병목이 된다 |

- **층이 다르다.** 이 페이지의 소유권은 OLTP 테이블의 쓰기 권한 배정이고, 데이터 메시의
  소유권은 분석 데이터의 제품 책임(product ownership)이다. 그쪽 페이지가 스스로 **ownership은
  product ownership의 줄임말**이라고 적는 자리가 그 차이의 실물이다.
- **두 소스는 이 자리에서 서로를 호명하지 않는다.** 데가니(Zhamak Dehghani)가 이 책의
  공저자이지만 9장은 데이터 메시 어휘를 쓰지 않는다(두 추출기로 확인했다). **이 대비표는 이
  KB의 것이다.**
- **겨루지 않는다.** 최대 하나만 참일 수 있는가를 물으면 답이 아니오다 — 같은 조직에서
  서비스가 자기 테이블을 소유하면서 도메인이 자기 분석 데이터를 소유할 수 있다. `contradicts`를
  걸지 않았다.

## 이어지는 페이지

- [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) — 같은 장의 다음 절. 소유권을
  배정하고 나서 업무 요청이 서비스 여럿에 걸칠 때 데이터를 어떻게 맞추는가
- [트랜잭션과 ACID](../concepts/acid-transactions.md) — 서비스를 가로지르는 요청이 ACID가 아니라 BASE를
  지지한다는 이 장의 판정이 붙는 자리
- [모놀리식 데이터를 쪼개는 다섯 단계](../concepts/decomposing-monolithic-data.md) — 이 소유권 배정이
  전제하는 분해 절차와 데이터 도메인이라는 매개
- [데이터 분해의 구동 요인](../concepts/data-decomposition-drivers.md) — 쪼갤 것인가의 판정과 공유
  데이터베이스가 앓는 문제 넷
- [데이터 분해가 부르는 문제들](../concepts/data-decomposition-concerns.md) — 쪼갠 뒤에 깨지는 것들
- [서비스 세분도](../concepts/service-granularity.md) — 서비스 통합 기법이 서 있는 저울과 그 통합 요인 넷
- [경계 컨텍스트](../concepts/bounded-context.md) — 이 장의 도판이 상자로 그리는 그 경계의 정본
- [도메인 소유권 원칙](../concepts/domain-ownership-principle.md) — 같은 낱말을 분석 데이터 쪽에서 쓰는 축
- [분산 시스템에서의 캐싱](../concepts/caching-in-distributed-systems.md) — 위임 기법의 성능과 내결함성
  문제에 저자들이 대는 완화책
- [CAP과 PACELC](../concepts/cap-and-pacelc.md) — 테이블 쪼개기의 동기화 물음을 가용성 대 일관성으로
  모는 정리
- [Sysops Squad 사례](../concepts/sysops-squad-case.md) — 이 장의 사가와 ADR이 놓이는 운영 예제
- [아키텍처 결정 기록](../concepts/architecture-decision-records.md) — 이 장의 ADR 둘이 쓰는 형식

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, 9장 "Data Ownership and
    Distributed Transactions" §"Assigning Data Ownership"(p.250) · §"Single Ownership
    Scenario"(pp.251–252) · §"Common Ownership Scenario"(pp.252–253) · §"Joint Ownership
    Scenario"(pp.253–254) · §"Table Split Technique"(pp.254–256) · §"Data Domain
    Technique"(pp.256–258) · §"Delegate Technique"(pp.258–261) · §"Service Consolidation
    Technique"(pp.261–262) · §"Data Ownership Summary"(pp.262–263) · 여는 사가(pp.249–250) ·
    §"Sysops Squad Saga: Data Ownership for Ticket Processing"(pp.279–282, ADR 둘 p.280·p.281
    포함). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측).
    직인용 여덟은 `pdftotext -layout` 추출로 문자 단위 대조했고, 줄바꿈 하이픈(U+2010)이 든
    낱말은 원문의 줄바꿈 자리를 그대로 두었으며 굽은 따옴표는 곧은 따옴표로 옮겼다. 원문이
    이탤릭으로 조판한 낱말은 인용 안에서 이탤릭을 유지했다.
    **절충 표 넷(표 9-1 p.256 · 9-2 p.258 · 9-3 p.261 · 9-4 p.262)은 `pdftoppm -r 160 -png`로
    렌더해 눈으로 대조하고 원문 열 머리글과 값 그대로 옮겼다** — 빈 칸은 원문에서도 비어 있다.
    그림 9-10(배정 결과)도 렌더해 상자 이름과 배치를 확인했다.
    **예제 9-1(테이블 쪼개기 DDL)을 펜스로 옮기지 않았다** — 가운데 문장이
    `INSERT INTO Inventory VALUES (product_id, inv_cnt) AS SELECT product_id, inv_cnt FROM
    Product;`인데 `VALUES`와 `AS SELECT`를 함께 쓰는 문법이 표준 SQL에도 주요 방언에도 없어
    복사해도 돌지 않는다(SCHEMA §3의 펜스 조건). 렌더와 두 추출기가 모두 같은 문장을 내므로
    원문 그대로이고 이 KB는 고치지 않았다. 절차와 식별자는 산문과 인라인 코드로 남았다.
    도판 스물하나(그림 9-1에서 9-21까지) 가운데 그림 9-10만 렌더해 배치를 옮겼고 나머지는
    본문이 그 도판에 대해 적는 것만 옮겼다.
    **원문 오식과 어긋남 넷을 그대로 두고 표시했다** — p.250 여는 사가의 `how to you see
    updates occurring`(do) · p.255의 `the traditional availability verses consistency
    trade-off`(versus) · 셋째 기법의 이름이 `delegate technique`과 `delegation technique`
    둘로 갈리는 것(p.254 목록과 p.281 사가·ADR·그림이 뒤쪽) · p.281 사가의 `use the delegation
    technique to pass data when the table notifies the Survey Service`(테이블이 알리는 것이
    아니라 티켓 완료가 알린다).
    저자들이 대는 바깥 서지(*Refactoring Databases*와 그 동반 웹사이트)는 **이 KB가 확인한
    원전이 아니다**. `Wishlist`·`Catalog`·`Inventory` 세 서비스 예는 저자들이 세운 것이다.
    네 기법을 맞댄 표와 "원자적 트랜잭션을 보존하는 표는 하나뿐"이라는 대조는 원문에 없고 이
    KB가 세운 것이다.

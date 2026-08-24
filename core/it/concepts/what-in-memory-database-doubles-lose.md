---
type: concept
title: 인메모리 데이터베이스 대역이 잃는 것
description: 데이터베이스 의존을 같은 엔진이 아닌 것으로 바꿔칠 때 무엇을 잃는가에 대한 세 문헌의 논거와 그 층 — 테스트를 두 벌 쓰게 되고 원시 SQL을 못 쓰고 API가 어긋나고 트랜잭션이 아무 일도 하지 않는다는 한 팀의 경험, 방언과 벤더 고유 기능의 차이가 초록 테스트를 프로덕션 실패로 만든 사례와 실물 데이터베이스를 컨테이너로 띄우라는 처방, 자기 제품의 인메모리 공급자를 highly discouraged로 표시하고 대신 리포지터리 층 대역과 SQLite 인메모리를 조건부로 권한 벤더 문서와 그 비교 표, 세 문헌 어디에도 금지 낱말이 없다는 층 판정, 그리고 실물 우선이라는 처방과 실제 관행이 반대라는 대조
generated: { by: "claude-opus-5", at: "2026-08-24T01:20:00Z" }
sources:
  - { id: bogard2020-in-memory-databases, resource: /it/sources/bogard2020-in-memory-databases.md }
  - { id: hauer2017-dont-use-in-memory-databases, resource: /it/sources/hauer2017-dont-use-in-memory-databases.md }
  - { id: efcore2026-testing, resource: /it/sources/efcore2026-testing.md }
---

# 인메모리 데이터베이스 대역이 잃는 것

- [버전 조건](#버전-조건)
- [세 소스의 지위 — 셋 다 측정이 없다](#세-소스의-지위--셋-다-측정이-없다)
- [소스별 연도와 판](#소스별-연도와-판)
- [한 팀이 접은 이유 다섯 (bogard)](#한-팀이-접은-이유-다섯-bogard)
- [초록 테스트가 프로덕션에서 깨진 사례와 그 처방 (hauer)](#초록-테스트가-프로덕션에서-깨진-사례와-그-처방-hauer)
- [만든 쪽이 자기 공급자에 붙인 표시 (efcore)](#만든-쪽이-자기-공급자에-붙인-표시-efcore)
- [벤더의 비교 표](#벤더의-비교-표)
- [세 소스가 겹치는 자리](#세-소스가-겹치는-자리)
- [세 소스가 갈리는 자리](#세-소스가-갈리는-자리)
- [금지인가 권장하지 않음인가 — 문면의 층](#금지인가-권장하지-않음인가--문면의-층)
- [이 묶음이 다른 페이지와 만나는 자리](#이-묶음이-다른-페이지와-만나는-자리)
- [이 묶음의 사각](#이-묶음의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터베이스 의존의 테스트 대역으로 같은 엔진이 아닌 것(인메모리 공급자·
다른 데이터베이스)을 쓰면 무엇을 잃는가.**

여기서 **인메모리(in-memory) 공급자(provider)**는 응용이 프로덕션에서 쓰는 데이터베이스
대신 메모리 안에서 같은 API를 흉내 내는 구현이고, **같은 엔진**은 프로덕션과 같은 제품·
같은 방언(dialect)의 데이터베이스를 뜻한다. 셋 다 원문의 낱말이다.

## 버전 조건

> **버전 조건**: 이 페이지의 EF Core 문서 인용은 **2026-08-20 확보본** 한 판에 대한 것이다.
> 그 확보본에는 적용 버전 표시(`Applies to`)가 없고 메타의 `moniker_range_name`도 비어 있어
> **어느 EF Core 릴리스에 걸리는지 문서가 스스로 밝히지 않는다.** 판을 가리키는 값이 셋이고
> 서로 다르다 — 본문 스탬프 `Last updated on 2023-01-30`, 메타 `ms.date` 2021-11-07, 원본
> 커밋 `74dc75f25fe24c4d250e30675a9105c6fa52a97c`. **계속 갱신되는 문서이고 이 KB는 현행판을
> 대조하지 않았으므로**, 인메모리 공급자의 성질에 관한 서술(트랜잭션을 지원하지 않는다,
> 원시 SQL을 전혀 지원하지 않는다)도 그 확보본 시점의 것이다.
>
> **엔진 쪽 경계는 하나만 실제 릴리스 번호로 적힌다** — MySQL 5.7.6부터 `virtual`이
> 예약어가 되어 따옴표 없는 열 이름으로 쓸 수 없다는 사례다. 5.7.6 이전에는 그 사례가
> 성립하지 않는다.
>
> **`stale_after`는 두지 않는다.** 위 조건 안에서 이 인용들은 만료되지 않는다.

## 세 소스의 지위 — 셋 다 측정이 없다

- **셋 다 실무 규범이고 실증이 아니다.** 실험도 통제도 표본도 없고, 세 문헌을 통틀어 인용할
  수 있는 측정값이 없다. 근거로 드는 것은 저자 팀의 경험(둘)과 벤더의 자기 서술(하나)이다.
  **이 페이지의 어느 문장도 학술 근거로 쓰지 않는다.**
- **등급은 셋 다 `practitioner-norm`이고, 이 등급은 대장이 아니라 이 반입이 붙였다.**
  대장(queue.yaml)의 이 항목에는 `evidence_grade:` 기재가 없다. 판단의 재료는 하나다 —
  세 문면 어디에도 측정도 표본도 참고문헌도 없다는 사실.
  - **셋째 소스만 성격이 다르다.** EF Core 문서는 개인 실무자의 글이 아니라 **대상 제품을
    만드는 조직이 낸 문서**다. 그래서 **자기 제품에 대한 사실 주장에서만 1차 출처**이고
    ("인메모리 공급자가 트랜잭션을 지원하지 않는다"), **"어떻게 테스트해야 하는가"에서는
    다른 두 소스와 같은 무게다.** 새 등급 이름은 만들지 않는다.
- **세 문헌에 붙은 수치가 하나뿐이고 그것도 자기 보고다** — EF Core 문서의
  `over 30,000 tests against SQL Server alone`이다. **집계 방법도 기계 사양도 `a few
  minutes`의 정의도 문면에 없다.** 아래에서 이 값을 옮길 때 그 사실을 함께 적는다.
- **세 소스 다 자기 생태계의 사례로 논증한다** — `.NET`·EF Core(둘), 자바·JVM 생태계의
  H2·Fongo(하나). 엔진 의미론에 관한 논거와 그 생태계 API에 관한 논거를 아래에서 가른다.

## 소스별 연도와 판

**전부 확보본 문면으로 확인한 값이다.**

| 소스 | 문면의 날짜 | 갱신 표시 | 현행판 대조 |
|---|---|---|---|
| Bogard, `Avoid In-Memory Databases for Tests` | 본문 머리에 `Mar 18, 2020` | `article:modified_time`이 게시 시각과 같다 — **갱신 기록 없음** | 하지 않음 |
| Hauer, `Don't use In-Memory Databases (H2, Fongo) for Tests` | 제목 아래 `Posted on Aug 21, 2017` | 같은 줄에 `Updated on Jun 12, 2022` — **갱신본이다** | 하지 않음 |
| EF Core, `Choosing a testing strategy` | 본문 말미 `Last updated on 2023-01-30` | 메타 `ms.date` 2021-11-07 · `updated_at` 2026-06-26 — **셋이 어긋난다** | 하지 않음 |

- **Hauer 글은 2017년 글이면서 2022년 판이다.** 어느 문장이 2017년의 것이고 어느 문장이
  2022년에 손질된 것인지는 **문면으로 구분되지 않는다.**
- **EF Core 문서만 판이 열려 있다.** 위 [버전 조건](#버전-조건)이 그 자리다.
- **셋 다 살아 있는 페이지이고, 이 KB는 셋 다 현행판을 다시 받아 대조하지 않았다.**
  직인용은 전부 2026-08-20 확보본에 대한 것이다.

## 한 팀이 접은 이유 다섯 (bogard)

**이 글은 규범이 아니라 한 팀의 경험 보고다** — 통합 테스트를 빠르게 하려고 인메모리
공급자로 바꿔치기를 시도했다가 접었다고 적는다.[^bogard2020-in-memory-databases]

- **총평이 한 줄이다** (`Pitfalls of In-Memory` 절):[^bogard2020-in-memory-databases]

  > First and foremost, an in-memory provider is a pale imitation for the real thing.

- **① 실물 통합 테스트를 어차피 써야 한다** (같은 절, `You MUST write a real integration
  test anyway`):[^bogard2020-in-memory-databases]

  > Even with writing in-memory tests, we still absolutely wrote integration tests against
  > a real database. Those unit tests with in-memory looked exactly like the integration
  > tests, just with a different provider.

  - 그래서 저자가 던지는 물음이 **"if we were writing the tests twice, what was the value
    of having two tests?"** 다.[^bogard2020-in-memory-databases]
- **② 원시 데이터 API로 내려갈 길을 열어야 한다** (같은 절, `You MUST allow raw access to
  the underlying data API`) — ORM이 힘들어지는 자리에서 SQL로 내려가는 것이 이 팀의 방식인데,
  인메모리 대역은 그 코드를 검사할 수 없다. **그래서 일어나는 일이 이
  것이다**:[^bogard2020-in-memory-databases]

  > What I tend to find is that instead of dropping down to SQL, developers avoid SQL just
  > so that it satisfies the tool. This is unacceptable.

  - **이 논거가 이 묶음에서 가장 멀리 가는 논거다.** 대역의 한계가 테스트를 왜곡하는 데서
    그치지 않고 **프로덕션 코드의 선택을 바꾼다**는 것이다.
- **③ API가 어긋난다** (같은 절, `The APIs don't match`):[^bogard2020-in-memory-databases]

  > The in-memory API of vanilla `IQueryProvider` doesn't match the LINQ query provider.
  > This means you'll have methods that don't make sense, are no-ops, or even nonsensical
  > for in-memory.

  - 든 예가 `Include`다 — 자식 레코드를 미리 가져오라는 지시인데 **인메모리에는 아무 뜻도
    없다.** 저자의 문면이 **"You can keep it, remove it, add more, remove more, doesn't
    matter."** 다.[^bogard2020-in-memory-databases]
  - **반대 방향도 있다** (같은 절) — 인메모리에서는 돌아가지만 서버에서는 번역되지 않는
    호출이 있고, **실제로 그 공급자에 질의를 돌려 보기 전에는 알 수 없다**고 적는다.
- **④ 트랜잭션이 아무 일도 하지 않는다** (`Databases Means Transactions`
  절):[^bogard2020-in-memory-databases]

  > With in-memory providers, there is no "ACID", everything is immediately durable. Each
  > operation is immediately performed, and transactions do nothing!

  - **이것이 엔진 의미론에 관한 논거이고 `.NET`에 매이지 않는다.** 저자가 같은 절에서
    옛날에 통합 테스트 전체를 트랜잭션 하나에 담았을 때 **"we'd see many false positives
    that would only break when each operation was distinct"** 를 보았다고 적고, 인메모리
    대역이 같은 종류의 거짓 양성을 만든다고 잇는다.[^bogard2020-in-memory-databases]
  - **결론이 신뢰의 문제로 끝난다** — **"Enough false positives, and you wind up
    distrusting these unit tests."**[^bogard2020-in-memory-databases]
  - **그리고 무엇이 대역에 없는지를 한 줄로 적는다**:[^bogard2020-in-memory-databases]

    > The database enforces constraints and visibility and isolation levels that these
    > attempts can't, and inevitably, you'll hit problems

- **⑤ 다른 인메모리 데이터베이스도 마찬가지였다고 적는다** (`But it's working for me!`
  절) — **"We've tried this (and other in-memory DBs, like SQLite), and it's always
  failed."**[^bogard2020-in-memory-databases]
  - **같은 절이 예외를 인정한다.** 잘 되고 있다는 사람에게 저자가 답하는 것은
    **"Your usage is trivial enough that can fit into the constraints of an in-memory
    provider"** 다. 곧 **이 글은 반례를 배제하지 않는다.**[^bogard2020-in-memory-databases]

## 초록 테스트가 프로덕션에서 깨진 사례와 그 처방 (hauer)

**이 글의 처방이 이 묶음에서 가장 실행 층에 가깝다** — 진단에서 그치지 않고 무엇으로
바꾸라는 데까지 간다.[^hauer2017-dont-use-in-memory-databases]

- **진단이 TL;DR 첫 줄에 있다**:[^hauer2017-dont-use-in-memory-databases]

  > Using in-memory databases for tests reduce the reliability and scope of your tests.
  > Your application's SQL may fail in production against the real database, although the
  > h2-based tests are green.

- **초록인데 프로덕션에서 깨진 실물 사례가 하나 적혀 있다** (`Drawbacks of In-Memory
  Databases for Tests` 절):[^hauer2017-dont-use-in-memory-databases]

  > Since MySQL 5.7.6, `virtual` is a keyword and can't be used as an unquoted column name.
  > By chance, we had a Hibernate entity with a property `virtual`. So after migrating to
  > MySQL 5.7.6+, the request touching this entity will fail. Unfortunately, we execute our
  > tests against an H2 database, so this mistake was not revealed!

  - **이것이 이 묶음에서 유일하게 구체적인 실패 사례다.** 통제도 표본도 없는 일화이지만,
    "대역이 통과해도 프로덕션이 통과하지 않는다"는 명제의 실물이다.
  - 위 [버전 조건](#버전-조건)이 이 사례의 경계(MySQL 5.7.6부터)를 소유한다.
- **둘째 논거는 기능 집합의 차이다** (같은 절) — 벤더 고유 기능(vendor-specific features)이
  대역에 없다는 것이고, 저자가 그 기능을 쓰는 것 자체는 좋다고 적는다
  (**"those features often allow you to be more efficient, accurate, elegant or
  maintainable - or to do certain things at all"**).[^hauer2017-dont-use-in-memory-databases]
  - 든 예가 넷이다 — MySQL의 `unix_timestamp()`가 H2에 없어 시간대 문제를 못 피한 것,
    오라클 트리거가 H2에 네이티브로 없어 로직을 자바로 다시 쓴 것, 포스트그레스의 윈도
    함수와 JSON 데이터 타입이 H2에 없는 것, 그리고 몽고DB의 인메모리 대역인 Fongo가
    **정렬이나 배열 안 복잡한 요소의 필터에서 실물과 다른 결과를 돌려준 것**이다.
    집계 프레임워크 지원은 **"poor and therefore unusable"** 이라고 적는다.[^hauer2017-dont-use-in-memory-databases]
  - **각각은 그 엔진 쌍의 사례이지 일반 명제가 아니다.**
- **셋째 논거가 선택지의 구조를 보인다** (같은 절) — 기능이 없을 때 남는 길이 셋이고 저자가
  셋 다 `Awful.`로 끝맺는다:[^hauer2017-dont-use-in-memory-databases]
  - ① 없는 기능을 자바로 등록해 채운다 → 구현 품이 더 들고 **"we don't test the real
    database-side code anymore. The meaning of tests gets partly lost."**
  - ② 벤더 고유 기능을 아예 쓰지 않고 프로덕션 코드를 대역에 맞춘다 → **"Usually, this
    leads to non-optimal solutions."**
  - ③ 그 코드를 테스트하지 않는다.
  - **①과 ②가 Bogard의 ②와 같은 자리다** — 대역이 프로덕션 코드를 끌어당긴다는 것.
- **넷째 논거는 층이 하나뿐이라는 것이다** (`Integration Tests in Production-like
  Environments` 절) — 프로덕션 유사 환경의 통합 테스트가 그 오류를 잡아 줄 수도 있지만
  커버리지에 달렸고, **"You only have a single layer of security, because your first test
  layer, the h2-based tests of your build, won't find them."** 저자는 그 오류를 빌드의 테스트
  단계에서 보고 싶다고 적는다.[^hauer2017-dont-use-in-memory-databases]
- **처방이 명시된다** (TL;DR):[^hauer2017-dont-use-in-memory-databases]

  > Solution: Throw H2 and Fongo away and use a dockerized version of your real database
  > instead. Docker simplifies the management of database instances.

  - **실행 방법이 둘이고 저자가 하나를 고른다** — 테스트 코드에서 컨테이너를 관리하는
    `TestContainers` 쪽과 빌드가 관리하는 쪽인데, **"Use TestContainers and manage the
    database in your test code. I recommend this approach."** 그리고 본문 끝에서
    **"TestContainers convinced me in practice, so I recommend this approach."** 라고 다시
    적는다.[^hauer2017-dont-use-in-memory-databases]
  - **대가도 적는다** — 컨테이너가 테스트마다 뜨면 **"This takes some time (10 - 15 s)"**
    이고 IDE에서 작은 수정마다 그만큼 기다리는 것이 성가시다는 것이다. **측정 절차 없는
    어림이다.** 완화책으로 시스템 속성 하나(예: `-DreuseDatabase`)를 두어 개발 중에는 미리
    띄워 둔 데이터베이스를 재사용하라고 적는다.[^hauer2017-dont-use-in-memory-databases]
  - **전제도 적는다** — 개발자 기계와 모든 CI 서버에 도커를 설치해야 하고, 저자는 그 품이
    **"the increased safety and uncompromising implementation are definitely worth the
    effort"** 라고 판단한다.[^hauer2017-dont-use-in-memory-databases]

## 만든 쪽이 자기 공급자에 붙인 표시 (efcore)

**이 문서의 특이점은 글쓴이가 그 인메모리 공급자를 만든 쪽이라는 것이다.**

- **문서가 먼저 가르는 것은 실물이냐 대역이냐다** (`Choosing a testing strategy`
  도입):[^efcore2026-testing]

  > a basic decision you need to make is whether your tests will involve your production
  > database system - just as your application does - or whether your tests will run
  > against a test double, which replaces your production database system.

- **대역의 한계를 한 문단으로 못 박는다** (같은 절):[^efcore2026-testing]

  > However, tests which pass against a test double don't guarantee that your program works
  > when running against the real external resource. For example, a database test double
  > may perform case-sensitive string comparisons, whereas the production database system
  > does case-insensitive comparisons.

- **빠름을 이유로 대역을 고르는 통념을 직접 부정한다** (`Testing against the database may be
  easier than it seems` 절):[^efcore2026-testing]

  > EF Core itself contains over 30,000 tests against SQL Server alone; these complete
  > reliably in a few minutes, execute in CI on every single commit, and are very frequently
  > executed by developers locally. Some developers turn to an in-memory database (a "fake")
  > in the belief that this is needed for speed - this is almost never actually the case.

  - **이 수치는 벤더의 자기 보고다.** 집계 단위는 "테스트 개수"이고 분모는 EF Core 자체의
    스위트이며, 측정 절차도 기계 사양도 `a few minutes`의 정의도 문면에 없다. **다른 스위트로
    전이하지 않는다.**
  - 같은 절이 컨테이너를 대안으로 든다 — **"Container-based technologies such as Docker can
    make this very easy, and libraries like Testcontainers can help automate the lifecycle
    of containerized databases in your tests."** **낱말이 `Testcontainers`이고, 같은 도구를
    Hauer는 `TestContainers`로 적는다.**[^efcore2026-testing]
- **다른 엔진을 가짜로 쓸 때의 판정이 SQLite 절에 있다**:[^efcore2026-testing]

  > However, before doing this, it's important to understand that in EF Core, different
  > database providers behave differently - EF Core does not attempt to abstract every
  > aspect of the underlying database system. Fundamentally, this means that testing
  > against SQLite does not guarantee the same results as against SQL Server, or any other
  > database.

  - 든 차이가 넷이다 — 같은 질의가 공급자에 따라 다른 결과를 낸다는 것(대소문자 비교가 예),
    SQL Server에서 되는 질의가 SQLite에서는 지원되지 않는다는 것, 공급자 고유 메서드
    (`EF.Functions.DateDiffDay`)를 쓴 질의는 SQLite에서 실패해 **테스트할 수 없다**는 것,
    그리고 원시 SQL이다:[^efcore2026-testing]

    > Raw SQL may work, or it may fail or return different results, depending on exactly
    > what is being done. SQL dialects are different in many ways across databases.

  - **그 절의 결론이 이 문서의 처방 순서를 정한다** — **"we recommend either writing your
    tests against your real database, or if using a test double is an absolute necessity,
    taking onboard the cost of a repository pattern as discussed below."**[^efcore2026-testing]
- **자기 인메모리 공급자에 붙인 표시가 이 문서에서 가장 센 낱말이다** (`In-memory as a
  database fake` 절, 원문 강조):[^efcore2026-testing]

  > Doing so is **highly discouraged**: as a database fake, in-memory has the same issues
  > as SQLite (see above), but in addition has the following additional limitations:

  - **그 앞에 유래가 적혀 있다** — 이 공급자는 **"originally designed to support internal
    testing of EF Core itself"** 이고, 그것을 응용 테스트의 가짜로 쓰는 사람들이 있다는
    서술이다. 곧 **응용의 데이터베이스 가짜로 만들어진 물건이 아니다.**[^efcore2026-testing]
  - 더해지는 한계가 넷이다 (같은 절):[^efcore2026-testing]
    - 관계형이 아니라서 SQLite보다도 적은 질의 유형을 지원한다.
    - **"Transactions are not supported."**
    - **"Raw SQL is completely unsupported."**
    - 성능을 위해 최적화된 적이 없어 **SQLite 인메모리보다, 때로는 프로덕션 데이터베이스보다도
      느리게 동작한다.**
  - **총평이 한 줄이다**:[^efcore2026-testing]

    > In summary, in-memory has all the disadvantages of SQLite, along with a few more -
    > and offers no advantages in return.

- **대역을 목으로 만드는 길도 같은 이유로 막는다** (`Mocking or stubbing DbContext and
  DbSet` 절) — 질의가 `IQueryable` 위의 정적 확장 메서드로 표현되므로 **질의 기능을 제대로
  목하는 것은 불가능하고**, 사람들이 "`DbSet`을 목한다"고 말할 때 실제로 만드는 것은
  메모리 안 컬렉션을 감싼 **가짜**라는 것이다. 그래서 **"this approach ends up being very
  similar to using the EF Core in-memory provider"** 이고 같은 결점을 그대로 갖는다.[^efcore2026-testing]
- **그래서 이 문서가 권하는 대역은 엔진 층이 아니라 리포지터리 층이다** (`Repository
  pattern` 절):[^efcore2026-testing]

  > For a proper, reliable test double, consider introducing a repository layer which
  > mediates between your application code and EF Core. … In testing, the repository
  > abstraction is directly stubbed or mocked without needing any actual LINQ queries,
  > effectively removing EF Core from your testing stack altogether and allowing tests to
  > focus on application code alone.

  - **진단이 한 줄로 요약된다** (같은 절) — 앞의 방법들이 모두 **"still evaluate the
    program's LINQ queries"** 이고 그것이 어려움의 근원이라는 것이다:
    **"a query designed to execute against a specific production database cannot reliably
    execute elsewhere without issues."**[^efcore2026-testing]
  - **대가도 계상한다** (같은 절) — 테스트할 모든 질의를 `IEnumerable`을 돌려주는 메서드로
    감싸야 하므로 **아키텍처 층이 하나 더 생기고 구현·유지 비용이 크며**, 게다가
    **리포지터리가 노출한 질의에 대해서는 여전히 실물 데이터베이스 테스트가 필요할 것**이라고
    적는다.[^efcore2026-testing]
- **`Summary` 절의 권고 넷이 이 문서의 최종 층이고, 그 넷이 순서를 이룬다**:[^efcore2026-testing]

  > We recommend that developers have good test coverage of their application running
  > against their actual production database system.

  > If you've decided to use a test double, we recommend implementing the repository
  > pattern, which allows you to stub or mock out your data access layer above EF Core,
  > rather than using a fake EF Core provider (Sqlite/in-memory) or by mocking `DbSet`.

  > If the repository pattern isn't a viable option for some reason, consider using SQLite
  > in-memory databases.

  > Avoid the in-memory provider for testing purposes - this is discouraged and only
  > supported for legacy applications.

  - **곧 실물 → 리포지터리 층 대역 → SQLite 인메모리 → (쓰지 말 것) 인메모리 공급자다.**
    셋째 칸이 이 페이지를 부르는 조항과 부딪히는 자리이고, 아래
    [금지인가 권장하지 않음인가](#금지인가-권장하지-않음인가--문면의-층)가 그 판정을 갖는다.

## 벤더의 비교 표

**문서의 `Overall comparison` 표를 원문 열 이름과 칸 문면 그대로 옮긴다.**[^efcore2026-testing]

| Feature | In-memory | SQLite in-memory | Mock `DbContext` | Repository pattern | Testing against the database |
|---|---|---|---|---|---|
| Test double type | Fake | Fake | Fake | Mock/stub | Real, no double |
| Raw SQL? | No | Depends | No | Yes | Yes |
| Transactions? | No (ignored) | Yes | Yes | Yes | Yes |
| Provider-specific translations? | No | No | No | Yes | Yes |
| Exact query behavior? | Depends | Depends | Depends | Yes | Yes |
| Can use LINQ anywhere in the application? | Yes | Yes | Yes | No\* | Yes |

\* 원문의 각주다 — **"All testable database LINQ queries must be encapsulated in
IEnumerable-returning repository methods, in order to be stubbed/mocked."**[^efcore2026-testing]

- **이 표는 문서의 판단이지 측정이 아니다.** 칸 값(`Yes`·`No`·`Depends`)에 측정 절차가 붙어
  있지 않다.
- **표가 말하는 것을 한 줄로 줄이면**: `Exact query behavior?`와 `Provider-specific
  translations?` 두 행에서 **가짜 셋이 모두 실물에 못 미치고**, 리포지터리 대역만이 실물과
  같은 칸에 선다. 그런데 리포지터리 대역이 그 칸에 서는 이유는 충실해서가 아니라
  **질의를 테스트에서 아예 빼기 때문**이다.

## 세 소스가 겹치는 자리

- **공통 명제 하나**: **대역이 통과해도 프로덕션 엔진에서 통과한다는 보장이 없다.** 세
  문헌이 각각 다른 낱말로 같은 말을 한다 — `a pale imitation for the real thing`(bogard) ·
  `may fail in production … although the h2-based tests are green`(hauer) ·
  `don't guarantee that your program works when running against the real external
  resource`(efcore).
- **어긋나는 지점의 목록은 부분만 겹친다.** 셋이 **모두** 드는 것은 둘뿐이다 —
  **공급자·벤더 고유 기능이 대역에 없다**는 것과 **SQL 문면이 엔진마다 다르다**는 것이다.
  나머지는 갈린다.

  | 어긋나는 지점 | bogard | hauer | efcore |
  |---|---|---|---|
  | 공급자·벤더 고유 기능 | 든다(번역되지 않는 LINQ 호출·무의미해진 `Include`) | 든다(`unix_timestamp()`·트리거·윈도 함수·JSON) | 든다(`EF.Functions.DateDiffDay`) |
  | SQL 문면·방언 | 든다(원시 SQL 접근이 막힌다) | 든다(예약어가 된 열 이름) | 든다(`SQL dialects are different`) |
  | 트랜잭션 의미론 | 든다 | **들지 않는다** | 든다 |
  | 제약·격리 수준 | 든다 | 들지 않는다 | 들지 않는다 |
  | 대소문자 비교 | 들지 않는다 | 들지 않는다 | 든다 |

  **hauer 글에는 트랜잭션·격리·제약·원시 SQL이라는 낱말이 아예 없다.** 그 글의 논거는
  기능 집합과 방언에만 서 있다.
- **셋 다 실물 데이터베이스를 첫째 자리에 둔다.** hauer와 efcore는 컨테이너를 이름까지
  들어 권하고(`Docker`·`TestContainers`/`Testcontainers`), bogard는 자기 팀이 실물 통합
  테스트를 어차피 썼다고 적는다.
- **대역이 프로덕션 코드를 끌어당긴다는 논거는 둘만 든다** — bogard의 "개발자가 SQL을
  피하게 된다"와 hauer의 "프로덕션 코드를 H2 호환으로 바꾼다"가 같은 자리다. **efcore는
  거기까지 가지 않는다** — 공급자 고유 메서드를 쓴 질의는 **"cannot be tested"** 라고만
  적고, 그래서 사람들이 그 메서드를 안 쓰게 된다는 말은 없다.

## 세 소스가 갈리는 자리

- **다른 엔진의 인메모리 대역을 어떻게 볼 것인가에서 갈린다.**
  - **bogard**: SQLite를 포함해 다 실패했다고 적는다 — `We've tried this (and other
    in-memory DBs, like SQLite), and it's always failed.`
  - **efcore**: **리포지터리 패턴이 불가능할 때 SQLite 인메모리를 조건부로 권한다** —
    `If the repository pattern isn't a viable option for some reason, consider using SQLite
    in-memory databases.`
  - **곧 두 소스가 같은 물건에 반대 방향의 판정을 낸다.** 이 KB는 이것을 해소하지 않는다.
- **대역이 꼭 필요할 때 어디에 세울 것인가에서 갈린다.** efcore만 답을 갖는다 — **엔진 층이
  아니라 리포지터리 층**이다. bogard와 hauer에는 이 층의 처방이 없다.
- **처방의 구체성이 다르다.** hauer만 실행 방법(컨테이너를 테스트가 관리할 것인가 빌드가
  관리할 것인가)과 그 대가(10~15초)를 적는다.
- **논거의 층이 다르다.** bogard의 절반은 LINQ 공급자라는 `.NET` 고유 사정이고, hauer는
  엔진별 기능 목록이며, efcore는 자기 제품의 사양이다. **엔진 의미론에 매인 논거만이 세
  생태계를 건너간다** — 트랜잭션·방언·제약·격리 수준이 그것이다.

## 금지인가 권장하지 않음인가 — 문면의 층

**이 페이지를 부르는 조항의 표현은 "대역은 같은 엔진 — 인메모리 대역 금지"다. 세 소스가 그
조항을 어느 층까지 지지하는지 문면으로 가른다.**

| 소스 | 가장 센 낱말 | 어디에 | 예외를 인정하는가 |
|---|---|---|---|
| bogard | `Avoid`(제목·본문) | 제목, 그리고 본문의 회피 권고 | **인정한다** — `But it's working for me!` 절 |
| hauer | `Don't use`(제목) · `Throw H2 and Fongo away`(TL;DR) | 제목과 TL;DR | 본문은 전부 대가와 선택지의 나열이다 |
| efcore | `highly discouraged`(원문 강조) | 인메모리 공급자 절 | **인정한다** — SQLite 인메모리를 조건부로 권한다 |

- **세 문헌 어디에도 금지 낱말이 없다.** 확보본 전문을 훑어 `forbidden`·`must not`·
  `prohibited`·`disallowed`를 찾았고 **셋 다 0건**이다. hauer 본문의 `never`는 사이드바의
  다른 글 제목(`Never Split The Difference`)이고 본문 문장이 아니다.
- **가장 센 층은 두 곳이다.** hauer 제목의 명령형(`Don't use`)과 efcore의
  `highly discouraged`(강조 태그가 붙은 유일한 낱말)다. 그러나 **hauer의 명령형은 제목과
  TL;DR에만 있고 본문의 논증은 전부 권고형**이며(`I recommend`·`For me, this is fine`),
  **efcore의 `discouraged`는 `Summary`에서 `Avoid … this is discouraged and only supported
  for legacy applications`로 반복된다.**
- **그러므로 판정은 이렇다.**
  - **"같은 엔진을 우선하라"는 방향은 세 소스가 모두 지지한다.** 이 부분은 조항과 문면이
    어긋나지 않는다.
  - **"금지"라는 층은 어느 소스도 지지하지 않는다.** 세 문면이 함께 지지하는 최대치는
    **"피하라 · 강하게 권장하지 않는다"** 이고, 그 위는 조항이 스스로 얹은 것이다.
  - **"인메모리 대역 금지"를 예외 없는 명제로 읽으면 efcore 문면과 어긋난다.** 그 문서는
    SQLite 인메모리를 셋째 선택으로 **권한다.**
  - **조항이 빠뜨린 처방이 하나 있다.** efcore가 대역이 필요할 때 첫째로 권하는 것은 같은
    엔진의 실물도 다른 엔진의 대역도 아니라 **리포지터리 층 대역**이다. "같은 엔진"만
    말하는 조항에는 이 자리가 없다.
- **정정 후보 셋을 여기 적어 둔다** — 판단은 조항 쪽의 몫이다.
  1. `금지` → `피한다 / 권장하지 않는다`로 층을 내린다. 근거는 위 표다.
  2. 절대 명제를 조건부로 바꾼다 — 대역이 불가피할 때 무엇으로 물러설 것인가를 조항이
     말하지 않으면, 세 소스 가운데 그 물음에 답하는 유일한 소스(efcore)와 어긋난다.
  3. 조항의 중심을 "무엇을 쓰지 마라"가 아니라 **"대역의 통과는 프로덕션 통과를 보증하지
     않는다"** 로 옮기는 안. 그것이 세 소스가 실제로 함께 지지하는 유일한 명제다.

## 이 묶음이 다른 페이지와 만나는 자리

- **[무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md)의 처방이 이
  묶음의 상류다.** 그쪽은 데이터베이스를 managed 의존으로 분류하고
  **`Use real instances of managed dependencies`** 라고 적는다. **그 "real instance"가 무엇을
  뜻하는지는 그쪽이 답하지 않는다** — 이 묶음이 그 자리를 채운다: 같은 엔진이고, 인메모리
  공급자는 그것이 아니며, 세우는 방법은 컨테이너다.
  - **그쪽의 처방을 문자 그대로 지키면서 이 묶음의 실패를 겪는 것이 가능하다.** "목을 쓰지
    않았다"는 조건은 인메모리 공급자로 바꿔치기를 배제하지 못하기 때문이다. **이 묶음이
    그쪽 처방의 실행 층인 이유가 이것이다.**
- **[실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md)의
  실측은 반대 방향이다.** 그쪽이 `Database` 범주 의존의 목 대체 비율을 재고 그 값이 이
  묶음의 처방과 가장 크게 어긋난다. **수치와 분모는 그 페이지에서 읽는다** — 이 페이지는
  옮기지 않는다. **격도 다르다** — 그쪽은 심사 실증이고 이 페이지는 실무 규범 셋이라
  같은 무게로 인용하지 않는다.
- **[테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md)와는
  방향이 같고 물러설 자리에서 갈린다.** 그쪽의 순서가 실물 · 가짜 · 스텁 · 상호작용 검증이고,
  이 묶음은 그 첫째 칸을 지지한다. **긴장은 둘째 칸에서 생긴다** — 실물이 느릴 때 가짜로
  물러서라는 것이 그쪽인데, 이 묶음의 세 소스는 데이터베이스 엔진의 가짜에서 그 물러섬이
  실패했다고 적는다.
  - **그런데 그쪽이 가짜에 붙인 조건 둘을 이 묶음의 사례에 대 보면 긴장이 줄어든다.**
    그쪽은 **실물을 소유한 팀이 가짜를 만들고 유지할 것**과 **가짜에도 테스트가 있을
    것**(계약 테스트)을 조건으로 단다. EF Core 인메모리 공급자는 EF 팀이 만든 것이지만
    문서 자신이 **"originally designed to support internal testing of EF Core itself"** 라고
    적고, 충실성의 기준(같은 입력에 같은 출력·같은 상태 변화)도 그 문서가 스스로 깨진다고
    적는다(대소문자 비교·트랜잭션 무시). **곧 이 사례는 그쪽 조건을 만족한 가짜의 반례가
    아니라, 조건이 만족되지 않은 가짜의 사례다.** #hypothesis 조건을 모두 만족한
    데이터베이스 가짜가 실제로 어떻게 되는지를 잰 자료는 이 KB에 없다.
- **[가짜와 목](../concepts/fakes-versus-mocks.md)의 가짜 리포지터리가 efcore의 처방과 같은
  층이다.** 그쪽 책은 가짜를 **리포지터리 층**(`FakeRepository`)에 두는데, efcore가 대역이
  꼭 필요할 때 첫째로 권하는 자리가 같다. **두 문헌이 서로를 인용한 적은 없다.**
  - **그러면서 같은 책이 이 묶음이 경고하는 일을 한다.** [작업 단위 패턴](../concepts/unit-of-work-pattern.md)이
    옮긴 문면대로 그 책은 프로덕션을 포스트그레스로 두고 **통합 테스트에서는 SQLite를 쓸 수
    있도록** 세션 팩토리를 덮어쓴다 — 곧 다른 엔진이다. **어느 쪽이 옳은지를 잰 자료는 이
    KB에 없다.**
- **[테스트의 바람직한 성질 열둘](../concepts/test-desiderata.md)의 간섭 문장이 이 묶음의
  일반형이다.** 그쪽이 옮긴 문면은 예측력(Predictive)을 올리면 빠름(Fast)이 깎인다는 것이고,
  **왜 그런지는 그 소스가 적지 않는다.** 이 묶음이 그 자리에 사례를 준다 — 대역은 빠름을
  사고 예측력을 파는 거래이며, hauer의 초록 H2 테스트가 예측력이 깎인 실물이다.
  - **efcore는 그 거래의 전제 자체를 부인한다** — 속도 때문에 가짜가 필요하다는 믿음이
    **"almost never actually the case"** 라는 것이다. 곧 **간섭이 있다는 것과 이 자리에서
    그 간섭이 실제로 작동한다는 것은 다른 주장이다.**

## 이 묶음의 사각

- **측정이 없다.** 세 문헌을 통틀어 실험도 통제도 표본도 없다. "대역을 쓰면 프로덕션에서
  깨진다"의 빈도도, "컨테이너로 바꾸면 얼마나 느려지는가"도 재어지지 않았다. hauer의
  10~15초조차 절차 없는 어림이다.
- **반대 방향의 실증이 이 묶음에 없다.** 실제 프로젝트가 데이터베이스 의존을 어떻게
  다루는지는 세 문헌이 다루지 않는다. **그 실측은 이 묶음과 반대 방향을 가리킨다** —
  [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md)가
  정본이다.
- **성공 사례가 세어지지 않았다.** bogard가 `But it's working for me!` 절에서 예외를
  인정하면서도 그 사람들이 얼마나 되는지, 어떤 조건에서 되는지는 적지 않는다.
  **"trivial enough"의 경계가 없다.**
- **생태계 편중이 있다.** 셋 가운데 둘이 `.NET`·EF Core이고 하나가 JVM이다. **다른 언어·
  다른 ORM·다른 저장소(문서·키값·컬럼) 계열의 근거는 Fongo 사례 하나뿐이다.**
- **컨테이너 처방의 대가가 한쪽만 적혔다.** 기동 시간은 적히지만 CI 자원 소비, 병렬 실행 시의
  격리, 이미지 관리, 데이터 준비와 정리 비용은 세 문헌 어디에도 없다.
- **`Testcontainers`가 채택 근거 없이 이름으로만 들어온다.** 두 소스가 이름을 들지만 어느
  쪽도 대안 도구와 비교하지 않았고, 자기 대상에 돌려 본 결과를 적지 않는다.
- **언어 모델 시대의 재검이 없다.** #hypothesis 이 묶음의 논거는 엔진 의미론(트랜잭션·방언·
  제약·격리 수준)에 서 있으므로 생성 도구의 세대와 무관하게 성립할 것이다 — **그러나 그것을
  확인한 자료는 없다.** 특히 **생성된 테스트가 인메모리 대역을 어느 비율로 고르는지**,
  그리고 **대역이 만든 거짓 양성을 생성 도구가 어떻게 다루는지**는 세 문헌의 주제가 아니고
  이 KB에 그 값을 잰 소스도 없다. 대장의 `llm_era:` 기재도 재검이 없다고 적는다.

## 이어지는 페이지

- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — **먼저 읽는다.**
  데이터베이스를 managed 의존으로 분류하고 실물을 쓰라고 판정하는 자리이고, 이 페이지는 그
  "실물"의 뜻과 그것을 세우는 방법을 소유한다
- [실제 프로젝트에서 무엇이 목으로 대체되는가](../concepts/what-gets-mocked-in-practice.md) —
  **이 처방과 반대 방향의 심사 실증.** 데이터베이스 범주의 목 대체 비율과 그 분모가 거기 있다
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) —
  실물을 먼저 쓰라는 같은 방향의 다른 소스. **가짜로 물러서는 자리에서 이 페이지와 긴장이
  생기고**, 그쪽이 가짜에 붙인 조건 둘이 그 긴장을 다시 좁힌다
- [가짜와 목](../concepts/fakes-versus-mocks.md) — 대역을 리포지터리 층에 두는 같은 처방의
  다른 소스. **그 책이 통합 테스트에서 SQLite를 쓴다는 것이 이 페이지와 부딪히는 자리다**
- [리포지터리 패턴](../concepts/repository-pattern.md) — EF Core 문서가 대역이 꼭 필요할 때
  첫째로 권하는 것의 실물. 그쪽은 이 패턴의 비용 계상표까지 갖는다
- [작업 단위 패턴](../concepts/unit-of-work-pattern.md) — 프로덕션 포스트그레스와 테스트
  SQLite를 가르는 세션 팩토리가 실제로 쓰인 자리
- [테스트의 바람직한 성질 열둘](../concepts/test-desiderata.md) — 예측력과 빠름이 간섭한다는
  일반형. 이 페이지가 그 간섭의 사례를 준다
- [리팩터링 내성과 거짓 양성](../concepts/resistance-to-refactoring-and-false-positives.md) —
  bogard가 `false positives`라고 부른 것에 이름과 잣대를 붙인 자리. **다만 원인이 다르다** —
  그쪽의 거짓 양성은 구현 세부에 결합해서 생기고, 이 페이지의 것은 대역이 실물과 달라서
  생긴다
- [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md) —
  실물 자원을 테스트에 들일 때 무엇이 흔들리는가. 컨테이너 처방이 치르는 대가의 다른 이름
- [대역과 단위 테스트의 가치](../synthesis/test-doubles-and-unit-test-value.md) — **이 갈래의 허브.** 이 페이지가
  실행 층으로 받는 처방과 그 처방을 어기는 실측이 거기 함께 있다
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이웃 허브. 작은 테스트를
  성립시키는 대역 이야기가 거기 걸려 있다
- **아직 답이 없는 물음 둘**
  - **다른 엔진의 인메모리 대역을 조건부로 써도 되는가.** bogard는 SQLite도 실패했다고 적고
    efcore는 셋째 선택으로 권한다. **두 판정을 가를 자료가 이 KB에 없다.**
  - **컨테이너 처방의 값이 대가보다 큰가.** 두 소스가 그렇다고 적지만 어느 쪽도 재지 않았다.

[^bogard2020-in-memory-databases]: Bogard, "Avoid In-Memory Databases for Tests",
    jimmybogard.com, **2026-08-20 확보본**(본문 머리에 `Mar 18, 2020`). **쪽 번호도 절
    번호도 없는 한 쪽짜리 글이라 locator는 원문 절 제목이다** — `Simple Ain't Easy` ·
    `Pitfalls of In-Memory`(하위 제목 `You MUST write a real integration test anyway` ·
    `You MUST allow raw access to the underlying data API` · `The APIs don't match`) ·
    `Databases Means Transactions` · `But it's working for me!`. 직인용은 확보본 문면
    그대로이고, 원문에서 `transactions do nothing`에 걸린 하이퍼링크는 뗐다(조판 장치).
    **C# 예제 다섯은 저자의 예시이고 실행 결과가 붙어 있지 않아 펜스로 옮기지 않았다** —
    개념 설명에 필요한 식별자(`IQueryProvider`·`Include`)만 인라인 표기로 옮겼다. 근거
    등급·현행판 미대조·인용 규약은 [소스 메타](../sources/bogard2020-in-memory-databases.md)가
    정본이다.

[^hauer2017-dont-use-in-memory-databases]: Hauer, "Don't use In-Memory Databases (H2,
    Fongo) for Tests", phauer.com, **2026-08-20 확보본**(제목 아래 `Posted on Aug 21,
    2017. Updated on Jun 12, 2022` — **확보본은 2022년 갱신을 거친 판이고 어느 문장이
    언제 것인지는 문면으로 구분되지 않는다**). locator는 원문 절 제목이다 — `TL;DR` ·
    `Drawbacks of In-Memory Databases for Tests` · `Integration Tests in Production-like
    Environments` · `Alternative: A Docker Container For The Database` · `Managed by the
    Test` · `Managed by the Build`. 직인용은 확보본 문면 그대로다. **`Gradle
    Implementation`·`Maven Implementation` 두 절의 빌드 스크립트와 자바 테스트 예제는 도구
    사용법이라 옮기지 않았다.** 원문의 도구 표기는 `TestContainers`이고 태그에는
    `Testcontainers`도 함께 있다. 근거 등급·현행판 미대조·인용 규약은
    [소스 메타](../sources/hauer2017-dont-use-in-memory-databases.md)가 정본이다.

[^efcore2026-testing]: Microsoft, "Choosing a testing strategy - EF Core", Microsoft Learn,
    **2026-08-20 확보본**. **living doc이고 판을 가리키는 값이 셋이며 서로 어긋난다** —
    본문 `Last updated on 2023-01-30` · 메타 `ms.date` 2021-11-07 · 메타 `updated_at`
    2026-06-26 · 원본 커밋 `74dc75f25fe24c4d250e30675a9105c6fa52a97c`. **`Applies to`
    블록도 `moniker_range_name` 값도 확보본에 없어 적용 EF Core 릴리스가 문서에 명시되지
    않는다.** locator는 원문 절 제목이다 — 도입 · `Testing against the database may be
    easier than it seems` · `Different types of test doubles` · `SQLite as a database
    fake` · `In-memory as a database fake` · `Mocking or stubbing DbContext and DbSet` ·
    `Repository pattern` · `Overall comparison` · `Summary`. 직인용은 확보본 문면
    그대로이고, `highly discouraged`의 강조는 원문 `<strong>`이다. 비교 표는 원문 표를
    옮긴 것이고 열 이름과 칸 문면도 원문 표기다. **본문이 가리키는 형제 쪽들과 리포지터리
    패턴 비교 그림은 확보되지 않아 읽지 못했다.** 근거 등급·판 표기·현행판 미대조·인용
    규약은 [소스 메타](../sources/efcore2026-testing.md)가 정본이다.

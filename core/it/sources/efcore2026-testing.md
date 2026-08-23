---
type: webpage
title: "Choosing a testing strategy - EF Core"
author:
  - { literal: "Microsoft" }
issued: "2026"
container-title: "Microsoft Learn"
URL: "https://learn.microsoft.com/en-us/ef/core/testing/choosing-a-testing-strategy"
snapshot: /it/archive/efcore2026-testing/
snapshot_sha256: "243beb34083c14c113aba14d242de1038c394c23cbc7c87034f63cb08d98cbc6"
accessed: "2026-08-20"
---

# Choosing a testing strategy — EF Core 공식 문서

- [지위 — 만든 쪽이 낸 문서이고 측정 절차가 없다](#지위--만든-쪽이-낸-문서이고-측정-절차가-없다)
- [판과 서지 — living doc이라 판 표기를 나눠 적는다](#판과-서지--living-doc이라-판-표기를-나눠-적는다)
- [인용할 때 지킬 것](#인용할-때-지킬-것)
- [옮기지 않은 것](#옮기지-않은-것)
- [이 소스가 닿을 자리](#이-소스가-닿을-자리)

**Entity Framework Core를 쓰는 응용의 테스트에서 무엇을 대역으로 세울 것인가를 벤더가 직접
비교한 문서.** 이 KB가 이 문서를 들이는 이유는 같은 진단을 적은 실무자 글 둘과 달리
**이것이 그 인메모리(in-memory) 공급자(provider)를 만든 쪽의 문서**라는 것이다 — 자기 제품의
한 기능을 자기가 `highly discouraged`로 표시한 자리다.

## 지위 — 만든 쪽이 낸 문서이고 측정 절차가 없다

- **근거 등급 표기는 `practitioner-norm`이다.** 심사를 거치지 않았고 실험도 표본도 없다.
  **새 등급 이름을 만들지 않는다** — 이 KB의 등급 어휘는 반입 절차 문서가 소유하고, 거기
  없는 이름을 이 반입이 지어내면 다음 세션이 그 이름의 의무를 모른다. 대신 이 소스를
  다른 실무 규범과 가르는 사실 하나를 여기 적는다: **글쓴이가 개인 실무자가 아니라 대상
  제품을 만드는 조직이다.**
  - 그래서 **자기 제품에 대한 사실 주장에서만 이 소스가 1차 출처다** — "인메모리 공급자가
    트랜잭션을 지원하지 않는다"는 이 문서가 정본이다.
  - **"어떻게 테스트해야 하는가"는 그렇지 않다.** 그 층에서는 다른 실무 규범과 같은 무게이고,
    같은 의무가 걸린다(학술 근거로 쓰지 않는다, 자기 규정을 인용해 지위를 밝힌다).
- **대장(queue.yaml)에 `evidence_grade:` 기재가 없다.** 이 등급은 **이 반입이 문면을 보고
  붙인 것**이다.
- **수치가 하나 있고 자기 보고다** — `EF Core itself contains over 30,000 tests against SQL
  Server alone; these complete reliably in a few minutes`. **집계 방법도 기계 사양도 "a few
  minutes"의 정의도 문면에 없다.** 이 값은 벤더의 자기 보고로만 인용하고 다른 스위트에
  전이하지 않는다.
- **자기 규정이 권고형이다** — `We recommend…`가 문서에서 반복되고, 마지막 절 이름이
  `Summary`이며 그 아래가 전부 권고 문장이다. **금지 낱말은 문서에 없다**(아래 참조).

## 판과 서지 — living doc이라 판 표기를 나눠 적는다

**이 문서는 계속 갱신되는 문서다. 아래 값은 전부 확보본(2026-08-20)의 문면과 메타에서 읽은
것이고, 이 KB의 직인용은 그 확보본에 대한 것이다.**

| 무엇 | 확보본의 값 | 어디에서 읽었나 |
|---|---|---|
| 본문에 보이는 갱신 스탬프 | `Last updated on 2023-01-30` | 본문 말미 |
| 메타의 문서 날짜 | `ms.date` = `2021-11-07T00:00:00Z` | `<meta>` |
| 메타의 사이트 갱신 시각 | `updated_at` = `2026-06-26T23:04:00Z` | `<meta>` |
| 원본 소스 커밋 | `74dc75f25fe24c4d250e30675a9105c6fa52a97c` | `<meta name="git_commit_id">` |
| 원본 소스 경로 | `dotnet/EntityFramework.Docs` 저장소의 `entity-framework/core/testing/choosing-a-testing-strategy.md` (`live` 브랜치) | `<meta name="original_content_git_url">` |
| 문서 유형 | `page_type` = `conceptual`, `ms.topic` = `concept-article` | `<meta>` |
| 낱말 수 | `word_count` = `2264` | `<meta>` |

- **"Applies to" 블록이 확보본에 없다.** EF Core 문서 일부에 붙는 적용 버전 표시가 이 쪽에는
  인쇄돼 있지 않고, `moniker_range_name` 메타도 **빈 값**이다. 곧 **이 문서는 특정 EF Core
  릴리스에 묶여 표시되지 않는다.**
- **본문에 보이는 "Article" 라벨도 확보본에 없다.** 확보본에서 확인되는 문서 유형 표시는 위
  표의 메타 둘(`conceptual`·`concept-article`)뿐이다.
- **세 날짜가 서로 다르고 어느 것도 "내용이 마지막으로 바뀐 날"을 보증하지 않는다.** 본문
  스탬프(2023-01-30)와 메타 `ms.date`(2021-11-07)가 어긋나고, `updated_at`(2026-06-26)은
  사이트 재생성 시각일 수 있다. **이 KB는 셋을 모두 적고 하나를 고르지 않는다.**
- **저자 표시가 개인이 아니다.** 메타의 `ms.author`는 `sampatel`, `author`는 `SamMonoRT`이고
  본문에 저자 줄이 없다. `author`를 조직(`Microsoft`)으로 적은 근거가 이것이다.
- **확보 시점은 2026-08-20이다**(`accessed`). 스냅샷 고정은 2026-08-24이고 바이트가 같은
  사본이다. **현행판 재취득·대조는 하지 않았다** — living doc이므로 지금 그 주소의 문면은
  이 스냅샷과 다를 수 있다.

## 인용할 때 지킬 것

- **문구를 확보 시점과 함께 인용한다.** 이 문서를 인용하는 모든 자리에 **"2026-08-20 확보본의
  문면"**이라고 적는다. living doc이라 문구가 바뀌면 인용이 조용히 거짓이 된다.
- **문면의 층을 올리지 않는다.** 이 문서의 가장 센 낱말은 인메모리 공급자에 붙은
  **`highly discouraged`**(`<strong>` 강조)이고, `Summary`의 대응 문장은
  **`Avoid the in-memory provider for testing purposes - this is discouraged and only
  supported for legacy applications.`** 다. **`forbidden`·`must not`·`prohibited` 같은 낱말은
  확보본 전문에 없다.** 곧 이 문서는 **권장하지 않음**이지 금지가 아니다.
- **이 문서가 인메모리 대역을 통째로 배격하지 않는다는 사실을 함께 적는다.** `Summary`의 셋째
  권고가 **`If the repository pattern isn't a viable option for some reason, consider using
  SQLite in-memory databases.`** 다. 곧 **다른 엔진의 인메모리 대역을 조건부로 권한다.** 이
  문서를 "인메모리 대역 금지"의 근거로 인용하면 그것은 문면과 어긋난다.
- **EF Core·`.NET`에 매인 서술과 매이지 않은 서술을 가른다.** `DbContext`·`DbSet`·
  `IQueryable`·`EF.Functions.DateDiffDay`는 그 생태계의 것이고, 대소문자 비교·SQL 방언·
  트랜잭션·공급자별 번역은 엔진 의미론의 것이다.
- **비교 표는 이 문서의 판단이지 측정이 아니다.** `Overall comparison` 표의 칸 값(`Yes`·
  `No`·`Depends`)에 측정 절차가 붙어 있지 않다.

## 옮기지 않은 것

사이트 껍데기(Microsoft Learn 헤더·푸터·피드백 위젯·`Ask Learn` 안내), 그리고 본문이
가리키는 형제 쪽들(`Overview`, `Testing against your production database system`,
SQLite·인메모리·리포지터리 각각의 사용법 쪽)이다. **그 쪽들은 확보되지 않았고 이 KB는
열지 않았다.** 리포지터리 패턴과 데이터베이스 가짜를 비교하는 그림 하나가 본문에 있으나
**확보본에 그림 파일이 없어 읽지 못했다** — 그림 안에만 있는 서술은 이 KB에 없다.

## 이 소스가 닿을 자리

- [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md) —
  이 문서가 다른 두 소스와 함께 답하는 자리. **`highly discouraged`의 층 판정도 거기 있다**
- [리포지터리 패턴](../concepts/repository-pattern.md) — 이 문서가 대역이 꼭 필요할 때
  첫째로 권하는 것. 그쪽은 그 패턴을 다른 소스의 문면으로 소유한다

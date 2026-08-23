---
type: post-weblog
title: "Avoid In-Memory Databases for Tests"
author: [{family: Bogard, given: Jimmy}]
issued: "2020-03-18"
container-title: "jimmybogard.com"
URL: "https://www.jimmybogard.com/avoid-in-memory-databases-for-tests/"
snapshot: /it/archive/bogard2020-in-memory-databases/
snapshot_sha256: "229f716303e427574e00afed8fde643640695a97d66b9b3d27e8d021da400f36"
accessed: "2026-08-20"
---

# Avoid In-Memory Databases for Tests

**한 팀이 인메모리(in-memory) 공급자(provider)로 통합 테스트를 빠르게 만들려다 접었다는
경험 보고.** 이 KB가 이 글을 들이는 이유는 결론("피하라")이 아니라 **접은 이유를 갈라 적은
형식**이다 — 테스트를 두 벌 쓰게 된다, 원시 SQL을 못 쓴다, API가 안 맞는다, 트랜잭션이
아무 일도 하지 않는다, 그리고 그 결과가 거짓 양성이라는 것.

## 지위 — 실무자의 경험 보고이고 측정이 없다

- **근거 등급 표기는 `practitioner-norm`이다.** 이 글에는 실험도 표본도 측정도 없다. 인용할
  수 있는 수치가 하나도 없고, 근거로 드는 것은 저자와 저자 팀의 경험이다
  (`Our teams tried a number of years ago…`, `It's something our teams learned nearly a
  decade ago`). **참고문헌 절도 없다.**
- **대장(queue.yaml)에 `evidence_grade:` 기재가 없다.** 이 등급은 **이 반입이 문면을 보고
  붙인 것**이고, 다음 세션이 이것을 대장 판정으로 오인하면 안 된다.
- **글의 성격이 논평이다.** 첫 문단이 밝히듯 이 글은 EF Core의 인메모리 공급자를 걷어내자는
  깃허브 이슈(`A controversial GitHub issue`)에 대한 저자의 의견이고, 마지막 문단도 EF 팀의
  유지 비용에 대한 판단으로 끝난다 — **"For me, no, it's not worth negative effects for our
  team."** 곧 이 글은 규범이 아니라 **한 사람의 판단으로 자기를 규정한다.**

## 판과 서지 — 문면에 인쇄된 것

- **게시일이 문면에 있다**: 본문 머리에 `Mar 18, 2020`과 `6 min read`. 메타 태그의
  `article:published_time`과 `article:modified_time`이 둘 다 `2020-03-18T18:25:12.000Z`다 —
  **게시 후 갱신 기록이 없다.**
- **제목은 `Avoid In-Memory Databases for Tests`이고 `og:title`·`twitter:title`이 같다.**
  분류 태그는 `Testing` 하나다.
- **저자 표시가 본문 머리에 `Jimmy Bogard`로 인쇄돼 있다.**
- **확보 시점은 2026-08-20이다**(`accessed`). 스냅샷 고정은 2026-08-24이고 바이트가 같은
  사본이다. **살아 있는 페이지이므로 현행판 재취득·대조는 하지 않았다** — 이 KB가 문면으로
  보증하는 것은 확보본 한 장이다.
- 확보본은 Ghost 6.59가 찍은 HTML 한 장이고, 사이트 껍데기와 최근 글 목록(2026년 글 셋)이
  함께 들어 있다. **그 목록은 본문이 아니다.**

## 인용할 때 지킬 것

- **학술 근거로 쓰지 않는다.** 실무자가 자기 팀의 경험으로 낸 판단이고, 어느 주장에도
  통제도 표본도 붙어 있지 않다. 조항에 쓸 때는 저자의 자기 규정(한 팀의 경험·한 사람의
  판단)을 함께 옮긴다.
- **문면의 층을 올리지 않는다.** 이 글의 낱말은 `Avoid`이지 금지가 아니고, 저자 자신이
  예외를 인정한다 — `But it's working for me!` 절이 그 자리이고, 거기서 저자가 적는 것은
  **"Your usage is trivial enough that can fit into the constraints of an in-memory
  provider"** 다. 이 KB가 이 글을 금지의 근거로 인용하면 그것은 문면보다 강한 인용이다.
- **`.NET`·EF Core에 매인 논거와 매이지 않은 논거를 가른다.** LINQ 공급자 이야기와
  `IQueryProvider`·`Include` 예는 그 생태계의 것이고, 트랜잭션·제약·격리 수준 이야기는
  엔진 의미론의 것이다. **전자를 다른 생태계로 옮겨 인용하지 않는다.**
- **코드 예제는 저자의 예시이지 실행된 실험이 아니다.** 확보본의 C# 조각 다섯은 논거를
  보이기 위한 예시이고 결과가 붙어 있지 않다.

## 옮기지 않은 것

사이트 껍데기(헤더·구독 폼·푸터), 최근 글 목록 셋(2026년 글 — 본문과 무관), 그리고 LINQ
공급자의 내부 구조를 설명하는 앞 절(`Simple Ain't Easy`)의 세부다. 그 절의 논지는 **"LINQ
공급자를 만드는 일이 어렵다"**이고, 이 KB가 옮긴 것은 그 어려움이 대역의 충실도에 무엇을
하는가뿐이다. 본문이 거는 바깥 링크(깃허브 이슈·`InMemoryTransaction.cs`·Dapper)는
**열지 않았다.**

## 이 소스가 닿을 자리

- [인메모리 데이터베이스 대역이 잃는 것](../concepts/what-in-memory-database-doubles-lose.md) —
  이 글이 다른 두 소스와 함께 답하는 자리
- [무엇을 목으로 대체할 것인가](../concepts/what-to-replace-with-mocks.md) — 응용 전용
  데이터베이스는 실물을 쓰라는 처방. 이 글은 그 처방을 지킨다면서 인메모리로 바꿔치는
  경로가 왜 실물이 아닌지를 다룬다

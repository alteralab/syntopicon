---
type: concept
title: 데이터 조직화 리팩터링
description: 데이터를 다루는 다섯 항목 — 한 변수가 두 책임을 지면 쪼개라는 규칙, 필드 이름이 왜 특히 중요한가에 브룩스의 격언이 붙는 자리, 계산할 수 있는 변수를 질의로 바꿔 가변 데이터의 범위를 줄이는 항목과 그 예외, 그리고 참조와 값 사이를 오가는 두 항목이 각각 어떤 조건에서 옳은가
generated: { by: "claude-opus-5", at: "2026-08-17T20:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 데이터 조직화 리팩터링

- [이 장이 묶는 축](#이-장이-묶는-축)
- [Split Variable — 한 변수에 한 책임](#split-variable--한-변수에-한-책임)
- [Rename Field — 이름의 중요도가 범위에 비례한다](#rename-field--이름의-중요도가-범위에-비례한다)
- [Replace Derived Variable with Query — 계산할 수 있으면 없앤다](#replace-derived-variable-with-query--계산할-수-있으면-없앤다)
- [Change Reference to Value와 그 역](#change-reference-to-value와-그-역)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터 자체를 — 변수의 책임, 이름, 파생 여부, 그리고 공유 방식을 — 어떻게
정리하는가.**

리팩터링(refactoring) 항목의 이름은 원어를 유지한다. 괄호 안 쪽 번호는 이 책이 항목을 가리킬
때 함께 붙이는 인쇄판 쪽이며 그 자체가 카탈로그의 참조 키다.

## 이 장이 묶는 축

- 저자가 밝힌 배열 (9장, p.239):[^fowler2018] **자료 구조는 우리 프로그램에서 중요한 역할을
  하므로 그것에 초점을 맞춘 리팩터링 한 묶음이 있다는 것은 놀랄 일이 아니다.** 서로 다른
  목적으로 쓰이는 값은 **혼란과 버그의 번식지**이므로 *Split Variable*(p.240)로 용도를
  가르고, 이름 짓기는 늘 그렇듯 까다롭고 중요하므로 *Rename Variable*(p.137)이 자주 친구가
  된다. **그러나 때로 변수에 할 수 있는 최선은 그것을 완전히 없애는 것이다 —
  *Replace Derived Variable with Query*(p.248)로.** 마지막으로 **참조와 값 사이의 혼동 때문에
  생긴 문제를 코드베이스에서 자주 발견하므로** *Change Reference to Value*(p.252)와
  *Change Value to Reference*(p.256)로 두 방식 사이를 오간다.
  - 장 안의 항목명은 필드 판인 *Rename Field*(p.244)이고, 장 머리말이 가리키는 것은 6장의
    변수 판 *Rename Variable*(p.137)이다. 둘은 같은 판정의 두 자리다.

## Split Variable — 한 변수에 한 책임

- 문제 규정이 대입 횟수다 — **어떤 용도는 자연히 변수가 여러 번 대입되게 만든다. 반복문 변수는
  반복문이 돌 때마다 바뀌고(`for (let i=0; i<10; i++)`의 `i` 같은), 수집 변수는 메서드 진행
  중에 쌓이는 값을 담는다. 다른 많은 변수는 장황한 코드의 결과를 나중에 쉽게 참조하려고
  담는 데 쓰인다** (9장 §"Split Variable", p.240).[^fowler2018]
- **규칙이 한 문장이다** (9장 §"Split Variable", p.240):[^fowler2018]

> These kinds of variables should be set only once. If they are set more than once, it is
> a sign that they have more than one responsibility within the method. Any variable with
> more than one responsibility should be replaced with multiple variables, one for each
> responsibility. Using a variable for two different things is very confusing for the
> reader.

- 6장 *Extract Function*의 수순이 **대입되는 지역 변수가 너무 많아 추출을 포기해야 할 때** 이
  항목을 지목한다 — [기본 리팩터링](basic-refactorings.md) 참조. 3장의 가변
  데이터(Mutable Data) 냄새도 같은 처방을 든다.

## Rename Field — 이름의 중요도가 범위에 비례한다

- 근거가 자료 구조의 지위다 — **이름은 중요하고, 레코드 구조의 필드 이름은 그 레코드 구조가
  프로그램 전반에 널리 쓰일 때 특히 중요할 수 있다. 자료 구조는 이해에 특히 중요한 역할을
  한다** (9장 §"Rename Field", p.244).[^fowler2018]
- 저자가 그 근거로 프레드 브룩스(Fred Brooks)의 격언을 든다 (9장 §"Rename Field",
  p.244):[^fowler2018]

> Show me your flowcharts and conceal your tables, and I shall continue to be mystified.
> Show me your tables, and I won't usually need your flowcharts; they'll be obvious.

  - 그리고 시대 보정을 붙인다 — **요즘 순서도를 그리는 사람을 많이 보지는 못하지만 그 격언은
    여전히 유효하다. 자료 구조가 무슨 일이 일어나는지 이해하는 열쇠다** (9장 §"Rename Field",
    p.244).[^fowler2018]
- **이름 고치기가 이해의 축적 장치라는 규정** — **이 자료 구조가 그토록 중요하므로 그것을 명료하게
  유지하는 것이 필수적이다. 다른 무엇과 마찬가지로 소프트웨어를 더 다룰수록 데이터에 대한 내
  이해가 나아지므로 그 개선된 이해가 프로그램에 새겨지는 것이 중요하다** (9장 §"Rename Field",
  p.244).[^fowler2018]
- **적용 범위가 클래스까지 간다** — **레코드 구조의 필드 이름을 바꾸고 싶을 수 있지만 이 생각은
  클래스에도 적용된다. 게터와 세터 메서드는 클래스 사용자에게 사실상의 필드를 이룬다. 그것들의
  이름을 바꾸는 것은 맨 레코드 구조에서만큼이나 중요하다** (9장 §"Rename Field",
  p.244).[^fowler2018] 이름 짓기의 정본은 [이름 짓기](naming-things.md)다.

## Replace Derived Variable with Query — 계산할 수 있으면 없앤다

- 문제 규정이 가변 데이터다 — **소프트웨어 문제의 가장 큰 원천 중 하나가 가변 데이터다. 데이터
  변경은 흔히 코드의 부분들을 어색한 방식으로 결합시키고, 한 부분의 변경이 발견하기 어려운
  연쇄 효과로 이어진다** (9장 §"Replace Derived Variable with Query", p.248).[^fowler2018]
- **처방이 제거가 아니라 범위 축소라는 것을 저자가 분명히 한다** — **많은 상황에서 가변 데이터를
  완전히 없애는 것은 현실적이지 않다 — 그러나 나는 가변 데이터의 범위를 가능한 한 최소화할
  것을 주장한다. 크게 효과를 낼 수 있는 한 방법이 그저 계산할 수도 있는 변수를 없애는 것이다**
  (9장 §"Replace Derived Variable with Query", p.248).[^fowler2018]
- 이득 둘 — **계산은 흔히 데이터의 뜻이 무엇인지 더 명료하게 만들고, 원본 데이터가 바뀔 때
  변수를 갱신하지 못해 오염되는 것으로부터 보호받는다** (9장 §"Replace Derived Variable with
  Query", p.248).[^fowler2018]
- **예외가 명시된다** — **합당한 예외는 계산의 원본 데이터가 불변이고 결과도 불변으로 만들 수
  있을 때다. 새 자료 구조를 만드는 변환 연산은 계산으로 대체될 수 있더라도 유지하는 것이
  합당하다** (9장 §"Replace Derived Variable with Query", p.248).[^fowler2018]
- **여기서 6장의 두 묶기 항목과 같은 쌍대성이 다시 나온다** — **계산된 속성 여럿으로 자료 구조를
  감싸는 객체와 한 자료 구조를 다른 자료 구조로 변환하는 함수 사이에는 실로 쌍대성이 있다.
  원본 데이터가 바뀌어 파생 자료 구조의 수명을 관리해야 할 때는 객체 쪽이 분명히 낫다. 그러나
  원본 데이터가 불변이거나 파생 데이터가 아주 일시적이면 두 접근 모두 효과적이다** (9장
  §"Replace Derived Variable with Query", p.248).[^fowler2018] *Combine Functions into
  Class*와 *Combine Functions into Transform*의 선택 기준과 같은 판정이다 —
  [기본 리팩터링](basic-refactorings.md) 참조.
- 3장의 가변 데이터 냄새가 **다른 곳에서 계산될 수 있는 가변 데이터**를 가장 고약한 종류로
  지목하고 이 항목을 처방으로 든다 — [코드의 나쁜 냄새](code-smells.md) 참조.

## Change Reference to Value와 그 역

두 항목이 서로의 역이고, 저자가 각각의 적용 조건을 대칭으로 적었다.

- **Change Reference to Value**(p.252) — 구분의 실물이 갱신 방식이다 — **내부 객체를 참조로
  다루면 같은 내부 객체를 유지한 채 그 속성을 갱신한다. 값으로 다루면 원하는 속성을 가진 새
  내부 객체로 통째 바꾼다** (9장 §"Change Reference to Value", p.252).[^fowler2018]
  - 값으로 다루면 내부 객체의 클래스를 값 객체(Value Object)로 만들 수 있고 — **값 객체는
    일반적으로 추론하기 더 쉬운데 특히 불변이기 때문이다. (…) 불변 데이터 값을 프로그램의 다른
    부분으로 넘겨도 감싼 객체가 모르는 채 그것이 바뀔까 걱정하지 않아도 된다. 값을 프로그램
    전역에 복제해도 메모리 링크를 유지할 걱정을 하지 않아도 된다. 값 객체는 분산 시스템과 동시
    시스템에서 특히 유용하다** (9장 §"Change Reference to Value", p.252).[^fowler2018]
  - **하지 말아야 할 조건이 곧바로 붙는다** — **이것은 또한 언제 이 리팩터링을 하지 말아야 하는지도
    시사한다. 공유 객체에 대한 어떤 변경이든 모든 협력자에게 보이도록 여러 객체 사이에 객체를
    공유하고 싶다면 그 공유 객체는 참조여야 한다** (9장 §"Change Reference to Value",
    p.252).[^fowler2018]
- **Change Value to Reference**(p.256) — 반대 방향의 계기가 갱신의 산탄이다 — **같은 논리적
  데이터의 물리적 사본을 갖는 데서 오는 가장 큰 어려움은 공유 데이터를 갱신해야 할 때
  일어난다. 그러면 모든 사본을 찾아 전부 갱신해야 한다. 하나라도 놓치면 데이터에 골치 아픈
  불일치가 생긴다** (9장 §"Change Value to Reference", p.256).[^fowler2018]
  - **갱신이 없으면 어느 쪽이든 된다** — **고객이 결코 갱신될 필요가 없다면 두 접근 모두
    합당하다. 같은 데이터의 사본이 여럿 있다는 것이 다소 혼란스러울 수는 있지만, 문제가 되지
    않을 만큼 흔한 일이다** (9장 §"Change Value to Reference", p.256).[^fowler2018] 메모리
    문제도 **다른 성능 문제와 마찬가지로 비교적 드물다**고 적는다.
  - **대가가 하나 붙는다** — **값을 참조로 바꾸면 한 엔티티에 대해 객체가 하나만 존재하게 되고,
    그것은 보통 이 객체들에 접근할 수 있는 어떤 종류의 저장소(repository)가 필요하다는 뜻이다.
    그러면 엔티티의 객체를 한 번만 만들고 다른 모든 자리에서는 저장소에서 가져온다** (9장
    §"Change Value to Reference", p.256).[^fowler2018]

## 이어지는 페이지

- [기능 이동 리팩터링](moving-features.md) — 앞 장(8장). *Move Field*가 데이터를 옮기는 자리
- [조건부 로직 단순화 리팩터링](simplifying-conditional-logic.md) — 다음 장(10장)
- [기본 리팩터링](basic-refactorings.md) — *Split Variable*이 *Extract Function*의 탈출구로
  지목되는 자리, 그리고 클래스와 변환의 쌍대성
- [캡슐화 리팩터링](encapsulation-refactorings.md) — *Replace Primitive with Object*가 값
  객체를 만드는 자리
- [코드의 나쁜 냄새](code-smells.md) — 가변 데이터 냄새가 이 장의 항목들을 지목한다
- [이름 짓기](naming-things.md) — 필드 이름 판정의 정본
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 9장 "Organizing Data"(pp.239–258). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 22).
    직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준 규약이며 근거는
    `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 각 항목의 Example 절과 스케치 도판은
    옮기지 않았다.

---
type: concept
title: 함수형 데이터 엔지니어링
status: draft
description: 배치 파이프라인을 순수 함수처럼 짜면 무엇이 보장되는가 — 재현 가능성을 요구 사항으로 세우는 논거, 결정적이고 멱등한 순수 태스크의 규정과 그것이 강제하는 덮어쓰기, 파티션을 불변 객체로 다루며 행이 아니라 파티션을 원자 상태로 삼는 전환, 차원을 스냅샷으로 쌓아 타입 2 SCD를 대신하는 제안과 그 전제가 된 비용 구조의 변화, 이벤트 시각 대신 처리 시각으로 파티션을 자르는 맞교환, 그리고 저자가 스스로 깨는 규칙 하나
generated: { by: "claude-fable-5", at: "2026-08-25T00:00:00Z" }
sources:
  - { id: beauchemin2018-functional-data-engineering, resource: /it/sources/beauchemin2018-functional-data-engineering.md }
---

# 함수형 데이터 엔지니어링

- [이 페이지의 지위 — 실무자 에세이이고 측정이 없다](#이-페이지의-지위--실무자-에세이이고-측정이-없다)
- [출발점은 재현 가능성이다](#출발점은-재현-가능성이다)
- [순수 태스크 — 결정적이고 멱등하다](#순수-태스크--결정적이고-멱등하다)
- [순수 함수와 다른 한 가지](#순수-함수와-다른-한-가지)
- [파티션을 불변 객체로 다룬다](#파티션을-불변-객체로-다룬다)
- [물리 파티션이 없는 저장소에서](#물리-파티션이-없는-저장소에서)
- [지속되고 불변인 스테이징 영역](#지속되고-불변인-스테이징-영역)
- [바뀌는 로직은 태스크 안에 조건으로 담는다](#바뀌는-로직은-태스크-안에-조건으로-담는다)
- [차원은 스냅샷으로 — 타입 2 SCD와 갈리는 자리](#차원은-스냅샷으로--타입-2-scd와-갈리는-자리)
- [작업 단위와 파티션의 DAG](#작업-단위와-파티션의-dag)
- [과거 의존을 피한다](#과거-의존을-피한다)
- [늦게 도착하는 팩트 — 처리 시각으로 자른다](#늦게-도착하는-팩트--처리-시각으로-자른다)
- [저자가 스스로 깨는 규칙 하나](#저자가-스스로-깨는-규칙-하나)
- [멱등을 재실행 동치성 검사로 읽으면](#멱등을-재실행-동치성-검사로-읽으면)
- [이 KB의 다른 데이터 페이지와 갈리는 자리](#이-kb의-다른-데이터-페이지와-갈리는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **배치 파이프라인을 순수 함수처럼 짜면 무엇이 보장되고, 그 규율이 왜 다시
돌리는 일을 안전하게 만드는가.**

이 KB에서 [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md)이 답하는 것은
**어떻게**다 — 이전 실행이 남긴 것을 무엇으로 치우는가. 이 페이지가 답하는 것은 **왜**다.
그 페이지의 소스(Konieczny)가 멱등성을 대중화한 글로 지목하는 것이 여기 반입한 이 글이다.

## 이 페이지의 지위 — 실무자 에세이이고 측정이 없다

- **근거 등급은 `essay`다.** 실험도 통제도 표본도 참고문헌 목록도 없다. 저자가 서두에서
  스스로 규정한다 — 이 글은 Yahoo·Facebook·Airbnb·Lyft에서 일하며 쌓인 지혜의 조각을
  증류한 것이라고 적는다 (「도입」 절).[^beauchemin2018-functional-data-engineering]

  > This post distills fragments of wisdom accumulated while working at Yahoo, Facebook,
  > Airbnb and Lyft, with the perspective of well over a decade of data warehousing and
  > data engineering experience.

  - **그러므로 이 페이지의 어떤 문장도 "학술 근거"로 쓰지 않는다.** 회사 이름들은 저자의
    경력 서술로만 나오고 그 회사들에서 무엇이 어떻게 됐다는 서술이 본문에 없다 — **일화**다.
- **측정 수치가 0건이다.** 본문에 단위 붙은 측정값이 하나도 없다. 등장하는 숫자는 전부
  가정된 시나리오의 값이다(예시 연도, 예시의 이력 기간, 그래프 깊이의 어림).
- **새로움도 저자가 부인한다** — 이 글이 함수형 접근을 형식화한 첫 글일 수는 있어도 그
  실천 자체는 실험적이지도 새롭지도 않다고 적고, 근거로 성숙한 대기업들이 여러 해 써
  왔다는 것을 든다 (「In retrospect」 절).[^beauchemin2018-functional-data-engineering]
  **어느 회사가 무엇을 얼마나 했는지는 적히지 않는다.**
- **이해 상충을 저자가 밝힌다** — Airflow를 논하는 자리에서 자신이 Airflow의 제작자이므로
  그 도구가 여기 처방한 방법론과 잘 맞는 것이 놀랍지 않다고 적는다 (「Unit of work」
  절).[^beauchemin2018-functional-data-engineering] 도구 평가를 이 글에 기대어 옮길 때
  이 문장을 함께 옮긴다.
- **판본 조건: 현행판 미대조 — 2018-08-06 아카이브본 기준이다.** 확보본에 심긴 JSON-LD가
  최초 발행일(2018-01-08)과 함께 수정일(2018-06-20)을 적고 있어 **이 캡처 자체가 이미
  개정본**이고, 그 이후의 개정 여부와 내용은 이 반입이 대조하지 않았다. 아래 서술은 전부
  그 아카이브본의 문면에 대한 것이다.

## 출발점은 재현 가능성이다

- 저자가 이 규율을 요구하는 첫째 근거는 성능도 비용도 아니라 **재현 가능성**
  (reproducibility)이다 — 재현 가능성과 반복 가능성은 과학적 방법의 토대이고, 분석으로
  하는 주장이 클수록 그 과정에 대한 검토도 그만큼 엄격해야 하며, 데이터를 신뢰할 수
  있으려면 결과를 얻은 과정이 투명하고 재현 가능해야 한다고 적는다 (「Reproducibility」
  절).[^beauchemin2018-functional-data-engineering]
- 그가 드는 실물은 **틀린 원천 데이터를 다시 받아 재처리하는 상황**이다 (「Reproducibility」
  절):[^beauchemin2018-functional-data-engineering]
  - 그 테이블에서 파생된 모든 구조를 그 기간에 대해 다시 처리(백필, backfill)해야 한다.
  - 이론상 하고 싶은 일은 **원래 실행 때와 똑같은 계산 방식을 새 데이터 위에 적용하는 것**
    이다.
  - 그런데 그 계산에 쓰이는 **관련 데이터셋도 원래 계산 시점과 동일해야** 한다 — 하류 처리가
    차원을 조인해 데이터를 풍부하게 만든다면 그 차원이 원래 계산 때와 같아야 한다.
  - 그 보장을 줄 수 없다면 **같은 기간에 대해 같은 계산을 해도 매번 다른 결과가 나올 수
    있다**는 뜻이 된다.
- 반대 방향도 같은 요구를 낳는다 — 업무 규칙을 바꿔 백필할 때는 **바뀐 것이 로직 하나뿐**
  이라는 보장이 필요하고, 그것은 곧 원천이 변경되지 않았다는 보장이다
  (「Reproducibility」 절).[^beauchemin2018-functional-data-engineering]
- 절의 결론이 이 글 전체의 요약이다 (「Reproducibility」
  절):[^beauchemin2018-functional-data-engineering]

  > To put it simply, immutable data along with versioned logic are key to reproducibility.

## 순수 태스크 — 결정적이고 멱등하다

- 규정 자체를 옮긴다. 이 문장이 이 글이 이 KB에 들어오는 이유다 (「Pure tasks」
  절):[^beauchemin2018-functional-data-engineering]

  > A pure task should be deterministic and idempotent, meaning that it will produce the
  > same result every time it runs or re-runs. This requires forcing an overwrite
  > approach, meaning re-executing a pure task with the same input parameters should
  > overwrite any previous output that could have been left out from a previous run of
  > the same task.

  - 곧 **결정적**(deterministic)이고 **멱등**(idempotent)하다는 것의 내용이 여기서는
    **재실행 결과의 동일성**이고, 그 동일성을 얻는 수단으로 저자가 못 박는 것이
    **덮어쓰기 강제**다. 이 KB의 다른 소스가 정의하는 멱등 항등식
    (`f(f(x)) = f(x)` 꼴)은 **이 글에 없다** — 아래
    [멱등을 재실행 동치성 검사로 읽으면](#멱등을-재실행-동치성-검사로-읽으면) 참조.
- 정당화의 축은 **운영성**(operability)이다 — 멱등한 태스크를 갖는 것이 파이프라인 운영에
  필수인 이유로, 태스크가 실패하거나 계산 로직을 고쳐야 할 때 **다시 돌리는 것이 안전하며
  이중 계산이나 그 밖의 나쁜 상태로 이어지지 않는다는 확신**이 필요하기 때문이라고 적는다.
  그 가정이 없으면 무엇을 다시 실행할지 정하는 데 **이전 실행들의 잠재적 부수 효과 전부에
  대한 맥락과 이해**가 필요해진다 (「Pure tasks」
  절).[^beauchemin2018-functional-data-engineering]
- 부수 효과를 없애기 어려워 보일 때 저자가 내놓는 처방은 **작업 단위의 크기를 다시 생각하는
  것** 하나다 — 관련 태스크들을 품으면 순수해지는가, 더 작은 태스크들로 쪼개면 순수해지는가
  (「Pure tasks」 절).[^beauchemin2018-functional-data-engineering]
- 태스크 안의 중간 상태도 순수 함수의 지역 변수처럼 격리돼야 하고, **같은 순수 태스크의 여러
  인스턴스는 실행에서 완전히 독립**이어야 한다 — 임시 테이블이나 데이터프레임을 쓴다면 태스크
  인스턴스끼리 간섭할 수 없게 구현해야 병렬화가 가능하다 (「Pure tasks」
  절).[^beauchemin2018-functional-data-engineering]

## 순수 함수와 다른 한 가지

- 저자 스스로 유비의 한계를 그어 둔다 — 순수 함수(pure function)와 달리 **순수 태스크는
  프로그래밍적 의미에서 객체를 "반환"하지 않는다.** 오늘날 흔한 SQL ELT 방식에서는 그저
  테이블의 일부(파티션)를 덮어쓸 가능성이 높다 (「Pure tasks」
  절).[^beauchemin2018-functional-data-engineering]
  - 그리고 그것이 부수 효과처럼 보이더라도 **전형적인 순수 함수가 반환할 불변 객체와 비슷한
    것으로 그 출력을 생각할 수 있다**고 덧붙인다 (「Pure tasks」
    절).[^beauchemin2018-functional-data-engineering] 곧 이 글의 "순수함"은 **언어 차원의
    성질이 아니라 규율로 흉내 내는 성질**이다.
- 단순함과 좋은 실천을 이유로 **개별 태스크는 출력 하나를 겨냥해야 한다** — 순수 함수가 이질적
  객체의 집합을 반환하지 않는 것과 같은 이치라고 적는다 (「Pure tasks」
  절).[^beauchemin2018-functional-data-engineering]

## 파티션을 불변 객체로 다룬다

- 함수형 패러다임을 강제하는 방법 하나가 **불변 객체**(immutable object)를 쓰는 것이고,
  순수 함수형 언어가 불변 객체를 강제해 변경을 막는 것과 달리 **노출된 객체가 실은 가변인
  환경에서도 함수형 실천은 가능하다**고 적는다 (「Table partitions as immutable objects」
  절).[^beauchemin2018-functional-data-engineering]
- 이 절의 핵심 문장 (「Table partitions as immutable objects」
  절):[^beauchemin2018-functional-data-engineering]

  > While your database of choice may allow you to update, insert, and delete at will, it
  > doesn’t mean you should. DML operations like UPDATE, APPEND and DELETE are performing
  > mutations that ripple in side-effects. Thinking of partitions as immutable blocks of
  > data and systematically overwriting partitions is the way to make your tasks
  > functional. A pure task should always fully overwrite a partition as its output.

  - **파티션**(partition)이 원자 단위가 된다는 것이 이 글의 전환점이다. 행이나 셀이 아니라
    파티션이 바뀔 수 있는 가장 작은 단위가 된다.

## 물리 파티션이 없는 저장소에서

- 저장소가 물리 파티션을 지원하지 않아도 함수형 접근이 막히지는 않는다고 적고, 저자가 드는
  우회 셋 (「Table partitions as immutable objects」
  절):[^beauchemin2018-functional-data-engineering]
  - **물리 테이블을 여럿 두고 뷰로 묶는다** — 순수 태스크의 출력을 서로 다른 물리 테이블로
    두고 `UNION ALL`로 묶어 논리 테이블 노릇을 하는 뷰를 만든다. 다만 **결과는 데이터베이스
    옵티마이저가 얼마나 똑똑한가에 따라 달라질 수 있다**고 단서를 단다.
  - **논리적으로 파티션하고 삽입 전에 삭제한다** — 태스크를 인스턴스화한 파라미터를 반영하는
    파티셔닝 키로 **체계적으로 `DELETE` 한 뒤 `INSERT` 한다.**
  - **비용을 따진다** — `TRUNCATE PARTITION`이 전형적으로 "공짜" 메타데이터 연산인 반면
    `DELETE`는 비쌀 수 있고, 그 길을 간다면 많은 엔진에서 **불필요한 잠금을 피하려고 `DELETE`가
    필요한지 먼저 확인하는 편이 효율적일 수 있다**고 적는다.
- 같은 결정을 패턴 이름과 결과 목록으로 정리한 쪽은
  [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md)이다. 그쪽에서 메타데이터 연산과
  데이터 연산의 갈림이 `Fast Metadata Cleaner`와 `Data Overwrite`라는 이름을 얻는다.

## 지속되고 불변인 스테이징 영역

- 물리 창고의 하역장과 달리 현대 데이터 웨어하우스에서는 **스테이징 영역**(staging area)에
  원천 데이터를 전부 쌓아 두고 **영원히 바꾸지 않은 채로 보존하고 싶어질 것**이라고 적는다
  (「A persistent and immutable staging area」
  절).[^beauchemin2018-functional-data-engineering]
- 그것이 사는 이유는 하나다 — 지속되는 불변 스테이징 영역과 순수 태스크가 있으면 **이론상
  웨어하우스 전체의 상태를 처음부터 다시 계산해 정확히 같은 상태에 도달할 수 있다**(그렇게
  하라는 뜻은 아니라고 괄호로 덧붙인다). 그것을 알면 **파생 테이블의 보존 기간을 더 짧게 잡을
  수 있다** — 언제든 과거 데이터를 백필할 수 있기 때문이다 (「A persistent and immutable
  staging area」 절).[^beauchemin2018-functional-data-engineering]

## 바뀌는 로직은 태스크 안에 조건으로 담는다

- 업무 로직은 시간이 지나며 바뀌고 때로 소급 적용된다. 저자가 가르는 두 경우
  (「Changing logic over time」 절):[^beauchemin2018-functional-data-engineering]
  - **소급될 때** — 그 변경이 기존 하류 파티션들을 "더럽게"(dirty) 만든다고 생각할 수 있고,
    그것들을 다시 계산해야 한다는 요구가 된다.
  - **소급되지 않을 때** — ETL 로직이 그 변경을 포착해 해당 기간에만 알맞은 로직을 적용해야
    한다.
- 조문에 해당하는 문장 — **시간에 따라 바뀌는 로직은 언제나 태스크 로직 안에 포착돼 인스턴스화
  시점에 조건부로 적용돼야 한다.** 그래야 **소스 관리(source control)의 로직이 전 기간에 걸쳐
  웨어하우스의 전체 상태를 어떻게 만드는지를 서술**하게 된다 (「Changing logic over time」
  절).[^beauchemin2018-functional-data-engineering]
- 위험의 실물이 이 절을 설득력 있게 만든다 — 2018년부터 적용될 새 세금 규칙이 생겼는데 태스크를
  그냥 새 로직으로 갱신해 두면, **다른 사람이 무관한 이유로 2017년을 백필할 때 자기도 모르게
  2018년 규칙을 2017년 데이터에 적용하게 된다** (「Changing logic over time」
  절).[^beauchemin2018-functional-data-engineering] 해법은 발효일(effective date)을 단 조건
  로직이다.
- 한 걸음 더 나아간 처방이 이 KB의 다른 자리와 곧장 이어진다 — **시간에 따라 바뀌는 업무 규칙은
  코드보다 데이터로 표현하는 편이 나은 경우가 많다.** 발효일을 가진 "파라미터 테이블"에 그 정보를
  저장하고, 처리 중인 팩트에 맞는 파라미터를 조인해 적용하는 로직을 두라는 것이다. 저자의 예는
  세율을 코드에 하드코딩하는 대신 **세율과 발효 기간을 적은 "taxation rate" 테이블**을 두는
  것이다 (「Changing logic over time」 절).[^beauchemin2018-functional-data-engineering]

## 차원은 스냅샷으로 — 타입 2 SCD와 갈리는 자리

- 문제 제기 — 차원과 참조 데이터는 본래 완만하게 변하므로 `UPSERT`로 모델링하거나
  **완만하게 변하는 차원**(slowly changing dimension) 기법을 적용하고 싶어지는데, 데이터를
  변경하지 않는 함수형 웨어하우스에서 그것을 어떻게 모델링하는가 (「But what about
  dimensions?」 절).[^beauchemin2018-functional-data-engineering]
- 저자의 답은 **차원 스냅샷**이다 — ETL 스케줄마다 새 파티션을 덧붙이고, 차원 테이블은
  **각 파티션이 특정 시점 현재의 전체 차원을 담는 스냅샷들의 모음**이 된다 (「But what about
  dimensions?」 절).[^beauchemin2018-functional-data-engineering]
  - 저자가 스스로 반론을 인용하고 답한다 — 매일 바뀌는 것은 데이터의 작은 비율뿐인데 중복이
    심하지 않느냐는 반론에, **그 말이 맞지만 차원 테이블은 팩트에 비하면 크기가 대개 무시할
    만하다**고 답한다.
  - 그리고 전제를 명시한다 — **저장과 컴퓨트가 엔지니어링 시간에 비해 아주 싸진 지금**은 대부분의
    경우 차원 스냅샷이 말이 된다 (「But what about dimensions?」
    절).[^beauchemin2018-functional-data-engineering] 곧 이 처방은 **비용 구조 위에 선 주장**
    이다.
- 킴벌 계열과 갈리는 문장이 이 절에 있다 — 전통적인 **타입 2 SCD 접근은 개념적으로 건전하고
  전체 계산 효율은 더 나을 수 있지만 관리가 번거롭다**고 적고, 그 주변 절차인 **대리 키 관리와
  팩트 적재 시의 대리 키 조회**를 **오류가 나기 쉽고 변경투성이이며 재현하기 어렵다**고 평가한다
  (「But what about dimensions?」 절).[^beauchemin2018-functional-data-engineering]
  - **이것은 모순이 아니라 맞교환의 재평가다.** 저자는 타입 2가 틀렸다고 하지 않고 "개념적으로
    건전하다"고 인정한 뒤 **비용 조건이 바뀌었다**고 주장한다. 킴벌 쪽 서술은
    [완만하게 변하는 차원](../concepts/slowly-changing-dimension.md)이 소유한다.
  - 저자 자신도 배타적으로 밀지 않는다 — **아주 큰 차원에서는 스냅샷과 SCD 기법을 섞는 것이
    합리적이거나 필요할 수 있다**고 적고, 일반적으로는 현재 스냅샷에 현재 속성만 두고 **사건
    시점의 속성이 중요한 경우에는 그 속성을 팩트 테이블로 비정규화**하라고 처방한다. 미리
    비정규화해 두지 못한 드문 경우에는 **팩트를 최신 스냅샷이 아니라 시간상 대응하는 차원
    스냅샷에 조인하는 더 비싼 질의**를 돌리면 된다 (「But what about dimensions?」
    절).[^beauchemin2018-functional-data-engineering]
- 세 번째 선택지도 든다 — **복합·중첩 데이터 타입**으로 이력을 담는 것이다. 세금 목적으로 고객의
  주(state) 변화를 추적하려면 발효일이 키이고 주가 값인 맵을 `state_history` 컬럼으로 둘 수
  있고, 이는 **타입 2 SCD처럼 테이블의 grain을 바꾸지 않으면서 이력을 추적**하며 **정보마다 새
  컬럼을 만들어야 하는 타입 3 SCD보다 훨씬 동적**이라고 적는다 (「But what about dimensions?」
  절).[^beauchemin2018-functional-data-engineering]

## 작업 단위와 파티션의 DAG

- 규율 하나 — **작업 단위는 단일 파티션으로의 출력에 직접 정렬돼야 한다.** 그러면 논리 테이블
  하나가 태스크 하나에, 파티션 하나가 태스크 인스턴스 하나에 대응돼 저장소의 각 파티션을 그
  계산 로직에 곧장 대응시키기 쉬워진다 (「Unit of work」
  절).[^beauchemin2018-functional-data-engineering]
- 저자가 드는 그림은 Airflow의 "tree view"다 — 행이 테이블에 대응하는 태스크, 셀이 파티션에
  대응하는 태스크 인스턴스이고, **태스크가 멱등하므로 이 셀들 중 어느 것을 다시 돌려도 안전한
  연산**이며 어떤 파티션에 대응하는 로그 파일을 찾기도 쉽다고 적는다 (「Unit of work」
  절).[^beauchemin2018-functional-data-engineering]
- 계보 층이 이 글의 두 번째 전환점이다 — 워크플로를 태스크의 DAG로, 데이터 계보를 테이블이
  노드인 그래프로 생각하기 쉬운데, **함수형 접근은 태스크 인스턴스와 파티션으로 이뤄진 더 정확한
  그림**을 그리게 해 준다. 이 더 자세한 그래프에서는 **변경될 수 있는 "원자 상태"가 개별 행이나
  셀이 아니라 파티션**이 된다 (「A DAG of partitions」
  절).[^beauchemin2018-functional-data-engineering]
  - 그 이득 — 어떤 행의 계보든 그 파티션을 통해 특정 태스크 인스턴스로 대응시킬 수 있고, 그래프를
    상류로 따라가면 **전체 계보를 파티션과 관련 태스크 인스턴스의 집합으로 이해**할 수 있다
    (「A DAG of partitions」 절).[^beauchemin2018-functional-data-engineering]

## 과거 의존을 피한다

- "상태 복잡도"를 키우는 흔한 패턴 하나로 **같은 테이블의 이전 파티션에 의존하는 파티션**을 든다
  — 시간이 지나며 복잡도가 선형으로 자란다 (「Past dependencies」
  절).[^beauchemin2018-functional-data-engineering]
  - 그가 드는 시나리오는 3년치 일간 스냅샷을 가진 사용자 차원이고, 그 경우 **그래프의 깊이가 천을
    넘고** 몇 달 전 데이터를 재처리하려면 **병렬화할 수 없는 DAG로 수백 개 파티션을 재처리해야 할
    수 있다**고 적는다. 이 값들은 가정된 시나리오의 어림이지 측정이 아니다.
- 처방 — 백필이 흔하고 과거 의존이 병렬화가 제한된 깊은 DAG를 낳으므로 **가능한 한 과거 의존으로
  모델링하지 않는 것이 좋은 실천**이다 (「Past dependencies」
  절).[^beauchemin2018-functional-data-engineering]
- 누적형 지표가 필요한 경우(고객의 생애 누적 지출 같은)에는 **그 목적에 최적화된 전용 프레임워크나
  다소 독립적인 모델로 그 계산을 모델링**하는 선택지를 들고, 그 이상은 **범위 밖으로 남긴다**고
  스스로 적는다 (「Past dependencies」 절).[^beauchemin2018-functional-data-engineering]

## 늦게 도착하는 팩트 — 처리 시각으로 자른다

- 엄격한 불변 정책에서 늦게 도착하는 팩트가 문제가 되는데, 모바일 기기의 보급과 네트워크의 간헐적
  불안정 때문에 **늦은 데이터는 꽤 흔하다**고 적는다 (「Late arriving facts」
  절).[^beauchemin2018-functional-data-engineering]
- 처방의 첫 단계는 **사건의 시각과 사건의 수신·처리 시각을 분리하는 것**이고, 늦은 팩트가 있을 수
  있는 곳에서는 **시간 파티셔닝을 언제나 이벤트 처리 시각(event processing time)으로** 해야
  한다고 못 박는다. 그래야 **지연 없이 예측 가능하게 불변 데이터 블록을 착지**시킬 수 있다
  (「Late arriving facts」 절).[^beauchemin2018-functional-data-engineering]
- 그 대가로 얻는 것 — 밀접히 관련된 두 시간 차원이 분석에 들어와 **"오늘 기준 2월 총매출",
  "3월 1일 기준 2월 총매출", "3월 1일 이후 2월에 대한 매출 조정액"** 같은 수치를 보여 줄 수 있고,
  저자는 이를 **어느 시점에 현실이 어떻게 보였는지를 이해하게 해 주는 타임머신**이라 부른다
  (「Late arriving facts」 절).[^beauchemin2018-functional-data-engineering]
- 잃는 것도 저자가 명시한다 — 처리 시각으로 파티션하면 데이터가 더 이상 이벤트 시각으로
  파티션되지 않으므로, 이벤트 시각에 술어를 거는 전형적 질의가 **파티션 가지치기**
  (partition pruning)의 이득을 못 본다. 저자는 이를 **분명히 비싼 맞교환**이라 적고 완화책 셋을
  든다 (「Late arriving facts」 절):[^beauchemin2018-functional-data-engineering]
  - **두 시간 차원 모두로 파티션한다** — 파티션 수 증가 배수는 비교적 낮겠지만 모델의 복잡도가
    올라간다.
  - **질의를 이벤트 시각과 처리 시각 양쪽에 술어를 걸어 작성한다** — 처리 시각 쪽은 비교적 넓은
    창으로 잡아 가지치기가 필요한 자리에서 동작하게 한다.
  - **읽기 최적화 저장소에서는 손해가 크지 않을 수 있다** — 옵티마이저가 파티션을 건너뛰지 못해도
    실행 엔진 최적화가 비슷한 성능에 도달할 수 있다. ORC나 파케이(Parquet) 파일을 처리한다면
    **파일 헤더만 읽고 다음 파일로 넘어가는 데서 실행이 끝날 것**이라는 예를 든다.

## 저자가 스스로 깨는 규칙 하나

- 마지막 절의 제목이 「A standard deviation」이고, 첫 문장이 **규칙은 깨지라고 있는 것이며 어떤
  경우에는 그렇게 하는 것이 합리적**이라는 선언이다 (「A standard deviation」
  절).[^beauchemin2018-functional-data-engineering]
- 저자가 관찰했다고 적는 패턴 — **완벽한 불변성 보장을 더 이른 SLA와 맞바꾸는 것**이다. 사용자
  차원에 의존하는 집계를 계산하는데 그 차원이 늘 하루 늦게 착지한다면, 정확성보다 이른 착지를 더
  중시할 수 있다. 그때는 **다른 의존이 충족된 시점에 사용 가능한 최신 파티션에 조인**하면 되고,
  최소한의 정확성을 보장하려고 그 범위를 **몇 개 파티션 정도로 제한**할 수 있다
  (「A standard deviation」 절).[^beauchemin2018-functional-data-engineering]
- 그리고 대가를 그 자리에서 적는다 — **나중에 그 집계 테이블을 재처리하면 결과가 약간 다를 수
  있다** (「A standard deviation」 절).[^beauchemin2018-functional-data-engineering] 곧
  **이 예외를 택하면 재현 가능성이라는 이 글의 출발점이 그만큼 깨진다.**

## 멱등을 재실행 동치성 검사로 읽으면

- `#hypothesis` **이 절은 이 KB의 읽기이지 이 글의 주장이 아니다.** 확보본에는
  `metamorphic`도, "검증"·"테스트"의 틀도 없다. 저자가 드는 정당화 축은 위에서 본 대로
  **재현 가능성**과 **운영성** 둘뿐이다.
- 그럼에도 이 KB가 이 글을 검증 축에 두는 이유는 **관계의 모양이 같기** 때문이다.
  [테스트 오라클](../concepts/test-oracle.md)이 정리한 대로 **메타모픽 관계**
  (metamorphic relation)는 **하나의 구현을 적어도 두 번 자극하고 그 응답들 사이에 제약을
  거는** 것이다. 순수 태스크의 규정 — 같은 입력 파라미터로 다시 실행하면 같은 결과가 나온다 —
  은 정확히 그 모양이다. 기대값을 따로 아는 오라클 없이도 **두 실행의 출력을 견주는 것만으로**
  위반을 잡을 수 있다.
- `#hypothesis` 그래서 이 글의 규율은 **오라클 없는 데이터 검증 수단 하나**로 읽힌다 — 명세가
  없는 데이터에서도 "다시 돌린 결과가 처음과 같은가"는 물을 수 있다. 다만 이 읽기에는 조건이
  붙는다.
  - **이 관계가 잡는 것은 파이프라인의 비결정성이지 데이터의 오류가 아니다.** 틀린 데이터를
    결정적으로 틀리게 처리하는 파이프라인은 이 검사를 통과한다. 그 자리를 메우는 것이
    [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md)과
    [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md)이 다루는
    **기대의 명시**다.
  - **저자 자신이 위 「A standard deviation」에서 이 관계를 조건부로 포기한다.** 이른 SLA를
    택한 테이블에서는 재실행 결과가 달라도 결함이 아니다 — 곧 이 검사가 걸리는 범위는
    파이프라인마다 선언돼야 한다.
- **전용 메타모픽 페이지는 이 KB에 없다.** 그 개념은 위 [테스트 오라클](../concepts/test-oracle.md)의
  「다른 산출물에서 파생되는 오라클」 절이 서베이 인용으로 소유하고 있고, 그것이 이 절이 기대는
  유일한 근거다.

## 이 KB의 다른 데이터 페이지와 갈리는 자리

이 페이지가 답하는 질문은 **왜 그렇게 짜는가**다. 같은 낱말을 쓰는 이웃 페이지들은 다른 질문에
답한다.

- [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md) — **어떻게 치우는가.** 다섯
  패턴의 이름·결과·대표 코드가 그쪽에 있고, 이 페이지는 그 패턴들이 지키려는 성질이 왜 필요한지를
  담는다. 그쪽 소스가 멱등성의 대중화를 이 글에 귀속시킨다.
- [배치 워크플로와 DAG](../concepts/batch-workflows-and-dags.md) — **잡의 의존 그래프를 무엇이
  다루는가.** 이 글이 더하는 것은 그 그래프의 **노드를 태스크·테이블에서 태스크 인스턴스·파티션으로
  내리는** 관점이다.
- [완만하게 변하는 차원](../concepts/slowly-changing-dimension.md) — **차원 속성이 바뀌면 어떻게
  응답하는가.** 킴벌의 타입 체계가 그쪽이고, 이 글은 그 체계 대신 **스냅샷을 쌓자**고 제안한다.
  모순이 아니라 비용 조건 위의 맞교환 재평가다.
- [늦은 데이터 통합](../concepts/late-data-integration.md) — **닫은 과거를 다시 여는 대가는
  무엇인가.** 그쪽이 재생의 비용을 다루고, 이 글은 그 상황 자체를 피하려고 **파티션 축을 처리
  시각으로 옮기는** 선택을 든다.
- [스트림 처리의 시간 의미론](../concepts/stream-processing-time-semantics.md) — 같은 두 시각
  (이벤트 시각·처리 시각)의 구분을 스트림 쪽에서 정리한 자리.
- [데이터 품질 강제 패턴](../concepts/data-quality-enforcement-patterns.md) — **나쁜 데이터를
  어느 자리에서 막는가.** 그쪽의 Audit-Write-Audit-Publish는 변환 앞뒤에 검사 단계를 세우고, 이
  글은 검사 단계를 두지 않는다 — 이 글이 사는 층은 **출력을 어디에 어떻게 쓰는가**다.

## 이어지는 페이지

- [멱등적 쓰기 패턴](../concepts/idempotent-write-patterns.md) — 이 글의 규율에 이름과 결과
  목록이 붙은 자리
- [배치 처리의 기본](../concepts/batch-processing-basics.md) — 불변 입력이 배치에 주는 것들의
  원리 쪽
- [재처리와 점진적 마이그레이션](../concepts/reprocessing-and-gradual-migration.md) — 배치 처리가
  결정적 순수 함수를 장려한다는 같은 관찰을 다른 소스가 적은 자리
- [상태·스트림·불변성](../concepts/state-streams-and-immutability.md) — 이 글이 기대는 불변성의
  원리 쪽
- [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md) — 재실행 동치성이
  답하지 못하는 것, 곧 **기대를 명시하는** 자리
- [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md) — 데이터에는
  선재하는 명세가 없다는 진단이 사는 자리
- [속성 기반 테스트](../concepts/property-based-testing.md) — 기대를 사례가 아니라 성질로 적는
  갈래. 멱등을 파이프라인의 성질로 읽으면 같은 모양이고, 다만 입력을 기계가 만들지 않는다
- [테스트 오라클](../concepts/test-oracle.md) — 메타모픽 관계의 정의가 사는 자리
- [배치 처리](../synthesis/batch-processing.md) — 이 층의 허브

[^beauchemin2018-functional-data-engineering]: Beauchemin 2018, "Functional Data
    Engineering — a modern paradigm for batch data processing", Medium. 쪽 번호가 없는
    웹 글이라 locator는 **원문의 절 제목**이다(「Reproducibility」·「Pure tasks」·「Table
    partitions as immutable objects」·「A persistent and immutable staging area」·
    「Changing logic over time」·「But what about dimensions?」·「Unit of work」·
    「A DAG of partitions」·「Past dependencies」·「Late arriving facts」·
    「A standard deviation」·「In retrospect」). **근거는 Wayback 2018-08-06 아카이브본
    한 벌이고 현행 Medium 판은 대조하지 않았다** — 그 확보본 자체가 2018-06-20 수정본임을
    자기 메타데이터로 밝힌다. 글의 도판 다섯은 도식이라 본문이 서술한 내용만 옮겼다. 이
    KB의 [소스 메타](../sources/beauchemin2018-functional-data-engineering.md) 참조.

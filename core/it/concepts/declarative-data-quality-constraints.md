---
type: concept
title: 선언적 데이터 품질 제약
description: 데이터 품질 검사를 코드로 선언하면 그것이 무엇으로 환원되어 어떻게 돌아가는가 — 체크와 제약을 메트릭 계산으로 번역해 집계 질의 한 번에 몰아넣는 실행 구조, 데이터가 자랄 때 상태를 들고 다시 재는 증분 계산과 그것이 지는 조건, 프로파일링과 열 이름 학습으로 제약을 제안받는 절차와 그 오제안 실측, 메트릭 이력 시계열 위의 이상 탐지, 그리고 임의 제약을 여는 이 설계가 제한된 스키마 언어를 고른 쪽과 갈리는 자리
generated: { by: "claude-fable-5", at: "2026-08-25T00:00:00Z" }
sources:
  - { id: schelter2018-data-quality, resource: /it/sources/schelter2018-data-quality.md }
  - { id: breck2019-data-validation, resource: /it/sources/breck2019-data-validation.md }
---

# 선언적 데이터 품질 제약

- [이 페이지의 지위 — 실험 수치와 배포 교훈의 격이 다르다](#이-페이지의-지위--실험-수치와-배포-교훈의-격이-다르다)
- [이 논문이 처음이 아닌 것과 자기 기여로 주장하는 것](#이-논문이-처음이-아닌-것과-자기-기여로-주장하는-것)
- ["데이터를 위한 단위 테스트"라는 어휘](#데이터를-위한-단위-테스트라는-어휘)
- [네 설계 원칙](#네-설계-원칙)
- [품질 차원 셋 중 둘만 직접 다룬다](#품질-차원-셋-중-둘만-직접-다룬다)
- [선언한 제약은 메트릭으로 환원된다](#선언한-제약은-메트릭으로-환원된다)
- [선언의 실물](#선언의-실물)
- [출력은 통과·실패가 아니라 술어와 값이다](#출력은-통과실패가-아니라-술어와-값이다)
- [데이터가 자라면 다시 재지 않고 상태를 갱신한다](#데이터가-자라면-다시-재지-않고-상태를-갱신한다)
- [증분이 항상 이기지 않는다](#증분이-항상-이기지-않는다)
- [제약을 제안받는다 — 프로파일링과 열 이름 학습](#제약을-제안받는다--프로파일링과-열-이름-학습)
- [제안은 틀린다 — 표 3이 잰 것](#제안은-틀린다--표-3이-잰-것)
- [메트릭 이력 위의 이상 탐지](#메트릭-이력-위의-이상-탐지)
- [실행 층 — 집계 질의 한 번으로 몰아넣기](#실행-층--집계-질의-한-번으로-몰아넣기)
- [규모에서 잰 것](#규모에서-잰-것)
- [조직 층의 교훈 — 생산자가 소비자의 검사를 가져다 쓴다](#조직-층의-교훈--생산자가-소비자의-검사를-가져다-쓴다)
- [임의 제약이냐 제한된 스키마 언어냐](#임의-제약이냐-제한된-스키마-언어냐)
- [이 KB의 다른 데이터 페이지와 갈리는 자리](#이-kb의-다른-데이터-페이지와-갈리는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **데이터 품질 검사를 코드로 선언하면 그것이 무엇으로 환원되어 어떻게
대규모로, 그리고 데이터가 자라는 동안 다시 실행되는가.**

## 이 페이지의 지위 — 실험 수치와 배포 교훈의 격이 다르다

- **근거 등급은 `peer-reviewed`다.** 게재 레코드가 1쪽에 인쇄돼 있다 — `PVLDB, 11 (12):
  1781-1794, 2018`, `Proceedings of the VLDB Endowment, Vol. 11, No. 12`,
  DOI `10.14778/3229863.3229867`.[^schelter2018-data-quality] **권·호·쪽이 문면에 있어
  리포지토리 레코드에 기대지 않는다.**
- **이 논문 안에 격이 다른 두 층이 있다.** 5절의 실험은 저자들이 직접 돌려 잰 값이라
  설정과 함께 인용할 수 있고, 6절 `LEARNINGS`(pp.1791~1792)는 **사용자 피드백의 서술이라
  수치도 대조군도 없다.**[^schelter2018-data-quality] 아래
  [조직 층의 교훈](#조직-층의-교훈--생산자가-소비자의-검사를-가져다-쓴다)은 그 조건에서만
  읽는다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 7절이 훑는 AJAX·HoloClean·
  ActiveClean 등의 수치는 경유 값이라 여기 옮기지 않는다.
- **논문 문면에 `Deequ`라는 이름은 없다.** 확보본 전문을 대소문자 무시로 문자열 검색해
  0건이고, 논문은 시종 `our system`·`our library`로만 부른다.[^schelter2018-data-quality]
  뒤에 그 이름으로 알려진 라이브러리와 이 논문을 이을 근거는 **확보본 안에 없다.**

## 이 논문이 처음이 아닌 것과 자기 기여로 주장하는 것

**"선언적 데이터 품질 검증"이라는 발상 자체는 이 논문의 것이 아니고, 논문이 그렇게
적는다.** 7절 관련 연구(p.1792)가 계보를 자기 앞에 세운다:[^schelter2018-data-quality]

> Data cleaning has been an active research area for decades, see recent surveys [1, 10,
> 38] for an overview.

> Declarative data quality verification The idea to allow declarative definitions of data
> quality standards is well-established.

- 같은 절이 선행 계보를 항목으로 나열한다 (§7, p.1792):[^schelter2018-data-quality]
  DBMS의 표준 무결성 제약(키 제약·널 허용), 두 튜플에 걸친 업무 규칙을 담는 **거부
  제약**(denial constraints), **함수 종속과 조건부 함수 종속**(functional dependencies·
  conditional functional dependencies)과 그 발견 알고리즘, 그리고 SQL을 확장한 **선언적
  데이터 클리닝 언어 AJAX**다. ML로 데이터를 고치는 계열(ActiveClean·HoloClean·
  BoostClean)도 같은 절이 선행으로 인용한다.
- **자기를 그 계보와 구별하는 지점을 두 군데서만 주장한다** (§7,
  p.1792):[^schelter2018-data-quality] 열 사이 관계를 규칙으로 적는 대신 **ML로 학습하고
  홀드아웃 데이터의 경험적 검사로 검증하는 예측 가능성 메트릭**이 하나이고, AJAX처럼
  최적화하되 **더 큰 제약 집합을 한 틀에 묶고 데이터 수리는 하지 않는다**는 것이 둘이다.
- 그러므로 이 소스는 **분야의 원전이 아니라 프로덕션 규모의 선언적 데이터 검증 시스템을
  보고한 원전**이다. 논문이 1절(p.1782)에서 자기 기여로 드는 것은 넷이고, 그
  범위가 곧 인용 가능한 범위다:[^schelter2018-data-quality]

  > • We present a declarative API combining common quality constraints with user-defined
  > validation code, which enables 'unit tests' for data (Section 3.1).
  > • We discuss how to efficiently execute the constraint validation by translating checks
  > to aggregation queries with dedicated support for incremental computation on growing
  > datasets (Sections 3.2 and 4).
  > • We give examples of how machine learning can be leveraged in data quality
  > verification, e.g., for enhancing constraint suggestions, for estimating the
  > predictability of a column, and for detecting anomalies in historic data quality
  > timeseries (Sections 3.3 and 3.4).
  > • We present an experimental evaluation of our proposed approaches (Section 5).

## "데이터를 위한 단위 테스트"라는 어휘

- **문구는 원문에 실재한다.** 확보본에서 여섯 자리에 나오고 **전부 작은따옴표가
  붙어 있다**[^schelter2018-data-quality] — 초록(p.1781), 1절의 비전 문장과 기여 첫
  불릿(p.1782), 3.1절의 절 제목과 첫 문단(pp.1782~1783), 8절 결론(p.1792). 초록의 형태가
  이렇다:

  > Our system provides a declarative API, which combines common quality constraints with
  > user-defined validation code, and thereby enables 'unit tests' for data.

- 1절이 그 비전을 소프트웨어 공학과 나란히 놓는다 (§1,
  p.1782):[^schelter2018-data-quality] `Our vision is that users should be able to write
  'unit-tests' for data (Section 3.1), analogous to established testing practices in
  software engineering.`
- **따옴표가 저자의 한정이다.** 이 KB는 그 한정을 지우지 않고 **'단위 테스트'(unit
  tests)**로 적는다 — 실행되는 것은 테스트 함수가 아니라 데이터에 대한 집계 질의이고,
  판정하는 것은 단정문이 아니라 메트릭에 걸린 술어다(아래
  [선언한 제약은 메트릭으로 환원된다](#선언한-제약은-메트릭으로-환원된다)).
- **이 논문은 `assertion`을 테스트 어휘로 쓰지 않는다.** 확보본 전문에서 `assert` 계열은
  한 번뿐이고 그것도 일반 동사다 — 계절성·추세가 있는 지표에서는 `asserting the correct
  behaviour may not be feasible with user-supplied thresholds`라고 적는 자리다 (§3.4,
  p.1787).[^schelter2018-data-quality] 그러므로 이 페이지는 이 KB의 확정 역어
  **단정(assertion)**을 쓸 자리가 없고, 판정 어휘는 **제약(constraint)**과
  **체크(check)**로 통일한다.

## 네 설계 원칙

1절이 시스템이 선 원칙을 넷으로 든다 (§1, pp.1781~1782):[^schelter2018-data-quality]

- **선언성**(declarativity) — `at the heart of our system is declarativity; we want users
  to spend time on thinking 'how' their data should look like, and not have to worry too
  much about how to implement the actual quality checks.`
- **유연성** — 사용자가 검증 코드에서 기존 라이브러리를 쓰고 외부 데이터를 끌어오거나
  외부 서비스를 호출할 수 있어야 한다. 예로 **REST 서비스를 불러 그 결과를 데이터에서
  계산한 통계와 비교하는 복잡한 함수**를 든다.
- **자라는 데이터의 통합** — 데이터는 계속 생산되므로 검증 시스템이 증가하는 데이터셋을
  받아들여야 한다.
- **확장성**(scalability) — 메트릭 계산을 집계 질의로 번역해 Apache Spark 같은 분산
  데이터플로 엔진에서 돌린다.

**앞의 둘이 서로를 당긴다.** 선언성은 어휘를 좁히려 하고 유연성은 임의 코드를 열려 한다.
이 시스템의 답은 **제약의 목록은 고정하되 그 제약이 받는 판정 함수를 사용자 정의 함수로
연다**는 것이다 — 표 1의 대부분이 `column, udf` 꼴의 인자를 받는 이유가 여기 있다.

## 품질 차원 셋 중 둘만 직접 다룬다

2절이 데이터 품질 문헌에서 흔히 드는 차원 셋을 정의한다 (§2,
p.1782):[^schelter2018-data-quality]

| 차원 | 논문의 정의 |
|---|---|
| **완전성**(completeness) | `the degree to which an entity includes data required to describe a real-world object` — 관계형 테이블에서는 널 값의 존재로 잰다 |
| **일관성**(consistency) | `the degree to which a set of semantic rules are violated` — 한 관계 안의 제약(타입·구간·범주 값 집합·여러 열에 걸친 규칙)과 관계 사이의 제약(다른 표의 참조 값)으로 나뉜다 |
| **정확성**(accuracy) | `the correctness of the data` — 구문 정확성(표현이 정의역에 맞는가)과 의미 정확성(값이 실세계와 맞는가)으로 갈린다 |

- **완전성은 맥락에 매인다.** 상품 카탈로그에서 노트북 범주에 신발 사이즈 값이 없는 것은
  결측이 아니라 **속성이 적용되지 않는 것**이므로, 시스템은 **속성이 적용될 때만** 완전성을
  잰다고 적는다 (§2, p.1782).[^schelter2018-data-quality]
- **시스템이 직접 다루는 것은 완전성과 일관성 둘이다** (§3.1,
  p.1784).[^schelter2018-data-quality] **정확성은 메트릭 표에 없다** — 실세계와의 대조가
  필요한 의미 정확성은 데이터 안에서 잴 수 없기 때문이고, 이 논문이 그 자리에 대신 놓는
  것이 **예측 가능성**(predictability)이다(다른 열로 이 열의 값을 맞힐 수 있는가).

## 선언한 제약은 메트릭으로 환원된다

**이 페이지의 중심 기제다.** 사용자가 적는 것과 기계가 도는 것 사이에 번역 층이 있다
(§3.1, pp.1782~1784):[^schelter2018-data-quality]

1. 사용자가 **체크**(check)를 정의한다. 체크는 실패했을 때 오류가 될지 경고가 될지를
   자기 수준(`Level.Error`·`Level.Warning`)으로 들고 있고, 안에 **제약**(constraint)을
   여럿 담는다.
2. 시스템이 체크와 제약을 훑어 **그것을 평가하는 데 필요한 메트릭**(metric)을 모은다.
3. 메트릭을 계산한다(실행 층은 아래 참조).
4. 제약에 딸린 **사용자 정의 검증 코드**를 그 메트릭 값에 적용해 결과를 낸다.

- **표 1이 제약의 전체 목록이고 표 2가 메트릭의 전체 목록이다** (표 1 p.1783, 표 2
  p.1784).[^schelter2018-data-quality] 표 1은 제약을 세 묶음으로 나눈다 — 완전성 차원
  (`isComplete`·`hasCompleteness`), 일관성 차원(`isUnique`·`hasUniqueness`·
  `hasDistinctness`·`isInRange`·`hasConsistentType`·`isNonNegative`·`isLessThan`·
  `satisfies`·`satisfiesIf`·`hasPredictability`), 일관성 검증에 쓸 수 있는 통계
  (`hasSize`·`hasMin`·`hasMax`·`hasMean`·`hasStandardDeviation`·`hasApproxQuantile`·
  `hasEntropy`·`hasMutualInformation`·`hasHistogramValues`·`hasCorrelation`·
  `hasCountDistinct`·`hasApproxCountDistinct`·`hasTypeConsistency`), 그리고 시간 축의
  `hasNoAnomalies` 하나다.
- **`is`로 시작하는 것과 `has`로 시작하는 것이 다르다.** `isComplete`는 결측이 없어야
  한다고 못 박고, `hasCompleteness`는 **결측 비율에 사용자 정의 함수를 걸어** 판정한다
  (표 1, p.1783).[^schelter2018-data-quality] 곧 접두가 곧 **판정 권한이 시스템에 있는가
  사용자에게 있는가**를 가른다.
- 메트릭의 정의가 문면에 있다 (§3.1, p.1784):[^schelter2018-data-quality] 데이터셋
  D의 레코드 수를 N, 어떤 열의 고유 값 집합을 V, 값 v의 카디널리티(cardinality, 그 값이
  나온 횟수)를 c_v라 할 때 —

  ```math
  \mathrm{Completeness} = \frac{|\{d \in D \mid d(col) \neq null\}|}{N}
  \qquad
  \mathrm{Compliance} = \frac{|\{d \in D \mid p(d)\}|}{N}
  ```

  ```math
  \mathrm{Uniqueness} = \frac{|\{v \in V \mid c_v = 1\}|}{|V|}
  \qquad
  \mathrm{Distinctness} = \frac{|V|}{N}
  ```

  - **`Uniqueness`와 `Distinctness`의 이름이 직관과 어긋날 수 있어 표 2의 문면을 그대로
    적는다** — `Uniqueness`는 `unique value ratio in a column`이고 `Distinctness`는
    `unique row ratio in a column`이다 (표 2, p.1784).[^schelter2018-data-quality] 앞은
    분모가 고유 값의 개수이고 뒤는 분모가 레코드 수다.
  - `Completeness`는 뒤에 **`is not null` 술어에 대한 `Compliance`로 다시 쓸 수 있다**고
    적힌다 (§3.2, p.1785).[^schelter2018-data-quality] 곧 메트릭 사이에도 환원이 있다.
- **비싼 메트릭에는 근사가 준비돼 있다** (§3.1, p.1784).[^schelter2018-data-quality]
  분위수는 온라인 알고리즘 기반 `ApproxQuantile`로, 고유 값 개수는 하이퍼로그로그
  스케치(hyperloglog sketch) 기반 `ApproxCountDistinct`로 대신한다 — 재분할이나 정렬이
  드는 계산을 피하기 위해서다.
- **예측 가능성은 다른 종류의 메트릭이다** (§3.1, p.1784).[^schelter2018-data-quality]
  대상 열의 값을 입력 열들에서 맞히는 분류 모델을 데이터 표본으로 훈련하고, **남겨 둔
  나머지에서 정밀도·재현율·F1 같은 표준 척도로 예측 품질을 재어 그 값을 메트릭으로
  돌려준다.** 상품 표에서 `description`과 `name`으로 `color` 열의 값을 맞히는 것이 논문의
  예다.

## 선언의 실물

- 이 API의 실물이 논문에 하나 있고, 외부 데이터·사용자 정의 함수·이상 탐지·예측
  가능성이 한 화면에 다 들어 있다 (리스팅 1, p.1783).[^schelter2018-data-quality]

  ```scala
  val numTitles = callRestService(...)
  val maxExpectedPhoneRatio = computeRatio(...)

  var checks = Array()

  checks += Check(Level.Error)
    .isComplete("customerId", "title",
      "impressionStart", "impressionEnd",
      "deviceType", "priority")
    .isUnique("customerId", "countryResidence",
      "deviceType", "title")
    .hasCountDistinct("title", _ <= numTitles)
    .hasHistogramValues("deviceType",
      _.ratio("phone") <= maxExpectedPhoneRatio)

  checks += Check(Level.Error)
    .isNonNegative("count")
    .isLessThan("impressionStart", "impressionEnd")
    .isInRange("priority", ("hi", "lo"))

  checks += Check(Level.Warning, on="delta")
    .hasNoAnomalies(Size, OnlineNormal(stdDevs=3))
  checks += Check(Level.Error, on="delta")
    .hasNoAnomalies(Size, OnlineNormal(stdDevs=4))

  checks += Check(Level.Warning)
    .hasPredictability("countryResidence",
      ("zipCode", "cityResidence"), precision=0.99)

  Verification.run(data, checks)
  ```

- 원문의 조판 들여쓰기(연속 줄을 이어 적는 방식)만 정돈했고 **토큰은 손대지 않았다.**
  추출 텍스트가 식별자를 낱자로 흩어 놓아(`h a s C o u n t D i s t i n c t`) 150dpi 렌더로
  대조해 복원했다.
- **읽는 법**: 1~2줄에서 외부 REST 서비스와 사내 계산으로 **기대값을 밖에서 가져온다.**
  12줄의 `_ <= numTitles`와 14줄의 `_.ratio("phone") <= maxExpectedPhoneRatio`가 메트릭에
  걸리는 사용자 정의 함수다. 21~24줄은 같은 이상 탐지를 **경고 3표준편차·오류
  4표준편차** 두 수준으로 이중으로 걸어 둔 것이고, `on="delta"`가 **전체 데이터셋이 아니라
  새로 들어온 부분**을 대상으로 삼는다.
- 논문의 해설이 각 줄의 의도를 적는다 (§3.1, p.1783)[^schelter2018-data-quality] —
  `title` 열의 고유 값 수가 시스템의 전체 영화 수 이하일 것, `deviceType` 히스토그램에서
  `phone`의 비율이 기대치 이하일 것, `impressionStart`가 `impressionEnd`보다 앞설 것
  (`happens-before` 관계), `countryResidence`를 우편번호와 도시로 **정밀도 99%**로 맞힐 수
  있을 것.

## 출력은 통과·실패가 아니라 술어와 값이다

- 실행이 끝나면 시스템은 어떤 제약이 성공하고 실패했는지에 더해 **그 제약이 번역된
  메트릭과 거기 적용된 술어, 그리고 실패를 만든 값**을 함께 보고한다 (§3.1,
  p.1784).[^schelter2018-data-quality]
- 리스팅 2(p.1785)의 발췌가 그 형태다 — `isComplete(title)`은
  `Completeness("title") == 1.0`으로, `isNonNegative(count)`는
  `Compliance("count >= 0") == 1.0`으로 번역돼 있고, 실패한 두 줄에는 실제 값이 딸려
  있다.[^schelter2018-data-quality]
- **실패한 두 값**(리스팅 2와 §3.1 해설, pp.1784~1785):[^schelter2018-data-quality]
  네 열 조합의 `isUnique`는 `Uniqueness == 1.0`을 요구하는데 실제 값이 **0.9967**이었고
  (논문 산문의 표현으로 `only 99.67% of records have been identified as unique`),
  `isInRange(priority, ('hi','lo'))`가 번역된 `Compliance` 술어는 **0.833**만 맞았다
  (`only matched 83.3% of records`).
  - **단위와 분모**: 둘 다 **비율(0~1)**이고 분모는 **그 데이터셋의 레코드 수**다
    (`Uniqueness`만은 위 정의대로 분모가 고유 값 수다). **이 두 값은 예시 출력이지 어떤
    실제 데이터셋의 측정 결과가 아니다** — 3.1절의 온디맨드 비디오 예시는 논문이 스스로
    `a toy example`이라 부른 것이다 (§3.1, p.1783).
- **그래서 이 시스템의 산출물은 경보가 아니라 진단이다.** 실패한 제약이 무엇으로
  환원됐는지가 함께 나오므로, 사람이 다음에 볼 자리가 출력 안에 이미 지목돼 있다.

## 데이터가 자라면 다시 재지 않고 상태를 갱신한다

- **범위 한정이 먼저다** (§3.2, p.1785):[^schelter2018-data-quality]

  > Note that we restrict ourselves to append-only cases where a dataset at time t is
  > simply the union of all previous deltas

  갱신·삭제가 있는 데이터셋은 이 절 밖이다.

- **증분 계산**(incremental computation)의 계산 모델이 셋으로 서 있다 (§3.2,
  p.1785).[^schelter2018-data-quality] 시각 t의
  스냅샷을 D(t), 그때 새로 붙는 델타(delta) 데이터를 ΔD(t)라 할 때 — **상태**(state) S,
  델타와 이전 상태에서 상태를 갱신하는 함수 f, 상태에서 실제 메트릭을 뽑는 함수 g, 그리고
  초기 빈 상태 S(0)이다.

  ```math
  S^{(t)} = f(\Delta D^{(t)}, S^{(t-1)}) \qquad m^{(t)} = g(S^{(t)})
  ```

  이득이 문면에 있다 — `it allows us to compute the series of metrics for the dataset
  snapshots via a recursive computation that only consumes the deltas.`
- **그 대가로 메트릭마다 재정식화가 필요하다** (§3.2, pp.1785~1786).[^schelter2018-data-quality]
  이전 데이터셋 D의 레코드 수 N과 델타의 레코드 수 ΔN을 각각 유지한다고 할 때 —
  - `Size`는 그냥 N + ΔN(두 레코드 수의 합)이다.
  - `Compliance`는 **술어를 만족한 절대 개수와 이전 크기 N 둘을 함께 들고 있어야** 갱신
    된다:

    ```math
    \frac{|\{d \in D \mid p(d)\}| + |\{d \in \Delta D \mid p(d)\}|}{N + \Delta N}
    ```

  - `Uniqueness`는 이전 데이터의 값별 카디널리티 c_v와 고유 값 집합 V를 알아야 한다:

    ```math
    \frac{|\{v \in V \cup \Delta V \mid c_v + \Delta c_v = 1\}|}{|V \cup \Delta V|}
    ```

  - 엔트로피(entropy)와 상호 정보량(mutual information)도 같은 방식으로 다시 쓰인다 —
    앞은 값별 카디널리티, 뒤는 두 열의 카디널리티와 **동시 출현 횟수 히스토그램**을
    유지한다.
  - **근사 자료 구조는 공짜다** — `ApproxQuantile`과 `ApproxCountDistinct`가 쓰는 자료
    구조는 본래 증분 갱신을 지원해 **따로 손볼 것이 없다**고 적는다.
- **재분할이 필요한 메트릭에서는 상태가 히스토그램이다** (§4.1,
  p.1788).[^schelter2018-data-quality] 엔트로피·유일성처럼 열로 묶어야 하는 계산에서
  상태 S는 `delta.select(columns).groupBy(columns).count()`의 결과인 히스토그램이고,
  갱신 함수는 **이전 히스토그램과 델타의 히스토그램을 묶음 열 기준 완전 외부 조인(full
  outer join)으로 병합해** 개수를 더한다. 메트릭은 그 히스토그램 위의 집계로 나온다.
- **상태의 보관은 분석기 밖에 있다** (§4.1, p.1788).[^schelter2018-data-quality]
  `StateProvider`가 상태의 영속화와 적재를 맡고, 실제 배치에서 상태는 **S3의 디렉터리**에
  산다. 스냅샷 하나를 갱신하려면 옛 상태를 주는 제공자와 새 상태를 받을 제공자 **둘**이
  필요하다. 이 내부 API는 사용자에게 감춰지고 사용자는 3.1절의 선언적 체크만 쓴다.

## 증분이 항상 이기지 않는다

**5.2절이 증분 계산의 손익을 직접 잰다** (§5.2, pp.1790, 그림 5~8).[^schelter2018-data-quality]

- **실험 설정**(수치를 인용할 때 함께 적어야 하는 것, §5 서두 p.1789):
  내부 상품 카탈로그 표본 **약 1억 2천만 레코드**(parquet 약 50GB, 레코드마다 수백 속성)를
  **약 1200만 레코드짜리 델타 10개**로 무작위 분할했고, **Elastic MapReduce 워커 5대
  (c3.4xlarge), Apache Spark 2.0.2, HDFS 2.7.3**에서 돌렸다. 세로축은 초 단위 실행 시간,
  가로축은 데이터셋의 레코드 수(백만)다.
- **재분할이 필요 없는 메트릭에서는 증분이 이긴다** (그림 5). 크기와 네 열의 완전성을 재는
  경우, **배치 쪽은 데이터 크기에 선형으로 늘고 증분 쪽은 상수로 남는다** — 증분의 비용이
  델타 크기에만 달렸고 이 실험에서 델타 크기가 일정하기 때문이다. 유지할 상태가 메트릭당
  숫자 한둘뿐이라 상태 비용도 거의 없다.
- **카디널리티가 낮은 열에서는 증분이 늦게 이긴다** (그림 6·7). `material`과 `brand`의
  유일성·엔트로피에서는 히스토그램을 영속화하고 조인하는 **상당한 고정 비용**이 있어,
  증분 쪽 실행 시간이 대체로 일정하되 **델타 서너 개가 쌓인 뒤에야** 배치를 앞지른다.
- **고유 값만 든 열에서는 증분이 언제나 진다** (그림 8). `product_id` 열은 값이 전부
  고유해서 델타마다 새 값이 통째로 들어오고, **유지하는 히스토그램이 사실상 원본 열의
  사본**이 된다. 그래서 증분 쪽 실행 시간도 배치처럼 선형으로 늘고, 논문은
  `the incremental computation always perform worse`라고 적는다.
  - **그런데도 증분을 남기는 이유를 같은 자리에 적는다** — 증분은 **계산 시점에 전체
    데이터셋에 접근할 필요가 없어서 적재 파이프라인을 크게 단순화한다.** 곧 이 선택의
    이득은 시간만이 아니다.
- **도판의 개별 값은 옮기지 않는다** — 그림 5~8은 이미지이고 축 눈금만 읽을 수 있다.
- **원문 안에 작은 불일치가 하나 있다.** 5.1절 본문은 재분할이 없는 작업 부하를 **여섯
  메트릭(데이터 크기 + 다섯 열의 완전성)**이라 적고(p.1789), 같은 실험을 다시 쓴 그림 5의
  캡션은 **`product_id`·`material`·`color`·`brand` 네 열**을 든다(p.1790). 열의 개수가
  본문과 캡션에서 다르므로 **이 KB는 열 목록을 근거로 쓰지 않고 "재분할이 필요 없는
  메트릭 묶음"이라는 성격만 인용한다.**

## 제약을 제안받는다 — 프로파일링과 열 이름 학습

**채택 비용이 이 기능의 존재 이유다** (§3.3, p.1786).[^schelter2018-data-quality] 시스템의
가치가 사용자가 정의한 체크의 풍부함에 달려 있으므로, 스키마도 타입 정보도 없는 데이터
(예: 분산 파일 시스템의 CSV 파일)에서 시작할 수 있어야 한다.

- **프로파일링**(profiling)은 **세 번의 훑기**로 끝낸다 (§3.3,
  p.1786).[^schelter2018-data-quality] 1차에서 데이터 크기·열별 타입 탐지·완전성·
  하이퍼로그로그 기반 근사 고유 값 수를, 2차에서 수치형으로 판정된 열의 최소·최대·평균·
  표준편차·근사 사분위수를, 3차에서 카디널리티가 사용자 지정 임계값 아래인 열의 값 빈도
  분포를 계산한다. **테라바이트 규모 표를 소비해야 하므로 단순한 통계로 자기를
  제한한다**고 적는다.
- 그 위에 얹히는 휴리스틱 규칙이 문면에 여섯 줄로 나열된다 (§3.3,
  p.1786):[^schelter2018-data-quality] 표본에서 완전한 열이면 `isComplete`을, 불완전하면
  **베르누이 분포로 보고 신뢰 구간을 추정해 그 하한을** 담은 `hasCompleteness`를,
  탐지된 타입이 문자열이 아니면 `hasConsistentType`을, 근사 고유 값 수가 데이터 크기와
  스케치의 오차 범위 안에서 일치하면 `isUnique`를, 수치형이고 관측값이 일정 구간에 들면
  그 구간의 `Compliance` 술어를, 고유 값 수가 임계값 아래면 범주형으로 보아 **이미 관측된
  값 집합**에 대한 `isInRange`를 제안한다.
- **열 이름 자체가 신호다** (§3.3, p.1786; §4.2,
  pp.1788~1789).[^schelter2018-data-quality] `id`·`is_deleted`·`price_per_unit` 같은
  이름에 사람이 읽는 의미가 들어 있다는 관찰에서, **표 이름·열 이름·타입만으로 제약을
  예측하는 모델**을 훈련한다. 훈련 데이터는 mediawiki·wordpress·oscommerce 같은
  오픈소스 프로젝트의 스키마에서 뽑은 **(표 이름, 열 이름, 타입, 유일 여부) 튜플 2,453개**
  이고, 문자 n-그램 해시와 타입 원핫 인코딩을 자질로 로지스틱 회귀를 5겹 교차 검증으로
  튜닝했다. **ROC 곡선의 AUC는 0.859**다.
  - **단위와 분모**: 2,453은 튜플 수(열 하나가 한 튜플)이고, AUC 0.859는 그 데이터의
    교차 검증 값이다. **이 모델은 유일성 제약 하나만 판정하는 데 쓰인다** — 휴리스틱이
    `isUnique`를 제안했을 때 모델이 **50% 넘는 확률**을 줄 때만 사용자에게 그 제안을
    내보낸다.
- **제안은 사람이 고른다** (§3.3, p.1786):[^schelter2018-data-quality]

  > Note that we see constraint suggestion as a 'human-in-the-loop' process with a low
  > computational budget and therefore rely on the end user to select from and validate
  > our suggestions which might not necessarily hold for future data

## 제안은 틀린다 — 표 3이 잰 것

- **설정과 분모** (§5.3 p.1790, 표 3 캡션 p.1791):[^schelter2018-data-quality] reddit
  댓글 데이터셋의 **5만 레코드 표본**과 트위터 사용자 **5,180명** 데이터셋에서, 각각
  **레코드의 10%로 제약을 제안하고 나머지 90%에서 커버리지(coverage)를 잰다.** 표 3의
  `coverage` 열은 그 90%에서 제약이 지켜진 비율이고, `classifier score` 열은 **위 열 이름
  분류기가 유일성 제약에 준 확률**이라 축이 다르다 — **두 열을 같은 분모로 읽지 않는다.**
- **reddit는 전부 지켜졌다** — 모든 열이 완전하고 타입이 문자열과 정수뿐인 쉬운 경우라,
  제안된 제약 전부의 커버리지가 1.0이다 (표 3, p.1791).
- **트위터에서 두 제약이 깨졌다** (표 3 p.1791, §5.3 pp.1790~1791):

  | 열 | 깨진 제약 | 커버리지 | 분류기 점수 |
  |---|---|---|---|
  | `lang` | `isInRange('en', 'pt', ...)` | 0.991 | 표기 없음 |
  | `statuses_count` | `isUnique` | 0.636 | 0.02 |

  - **`lang`의 실패가 오히려 쓸모 있었다** — 표본에서 찾은 열 값이 시험 데이터의 99% 넘게
    덮지만 터키어·헝가리어 같은 희귀 언어를 놓친다. 그런데 **수동 조사에서 이 열이
    정규화돼 있지 않다는 것**이 드러났다(`en-gb`와 `en-GB`가 함께 있다). 논문의 표현으로
    `A failing constraint on that column can nevertheless be helpful`이다.
  - **`statuses_count`의 실패는 근사의 대가다** — 표본에 값이 다양하고 고유 값 수를
    근사로만 알기 때문에 유일성을 잘못 제안했고, **시험 데이터에서 이 열의 유일성 값은
    64%뿐**이다(표의 0.636).
  - **그 오제안을 분류기가 잡았다** — `id` 열의 유일성 제안에는 **81%**의 확률을 주고
    `statuses_count`에는 **2%**만 주어, 뒤엣것을 버리게 한다.
  - **대신 분류기가 거짓 음성을 냈다** — `screen_name`은 실제로 표본에서 유일한데 분류기는
    **1%**만 주었다(표의 0.01). 논문의 해명은 두 겹이다: 여러 소셜 플랫폼에서 서로 다른
    사용자가 같은 표시 이름을 가질 수 있어 **사람에게도 자명하지 않고**, 그리고
    `we prefer conservative and robust suggestions (e.g., rather having false negatives
    than false positives), which build trust in our users`.
- **여기가 이 시스템의 오라클 문제가 드러나는 자리다.** 제안된 제약은 **표본에서 참인
  것**이지 도메인에서 참인 것이 아니다. 논문이 그 간극을 자동화로 메우지 않고 **사람의
  선택과 보수적 편향**으로 메운다.

## 메트릭 이력 위의 이상 탐지

**이상 탐지**(anomaly detection)가 이 시스템의 셋째 층이고, 앞의 둘과 겨냥이 다르다.

- **대상이 데이터가 아니라 메트릭의 시계열이다** (§3.4,
  p.1787):[^schelter2018-data-quality]

  > Anomaly detection in our system operates on historic time series of data quality
  > metrics (e.g., the ratio of missing values for different versions of a dataset).

  곧 이 층의 기대값은 **선언된 제약이 아니라 과거의 자기 자신**이다.
- **알고리즘을 규정하지 않는다** — `We pose no restriction on the anomaly detection
  algorithm to apply`이고, 기본으로 몇 가지가 딸려 온다 (§3.4,
  p.1787).[^schelter2018-data-quality]
  - 가장 단순한 것은 **사용자가 정한 임계값**을 검사하는 알고리즘이다.
  - 리스팅 1에 나온 `OnlineNormal`은 **달리는 평균과 분산 추정치를 계산해**, 시계열 값이
    평균에서 몇 표준편차까지 벗어나도 되는지의 사용자 지정 한계와 비교한다.
  - **차분**(differencing)의 정도를 지정하는 방법도 제공해, 분석 전에 시계열을 정상화
    (stationarize)할 수 있게 한다.
- **왜 임계값만으로 안 되는지를 같은 자리가 적는다** (§3.4,
  p.1787):[^schelter2018-data-quality] 결측 값 수 같은 지표는 **계절성이나 추세**를 탈 수
  있어서(부하가 몰리는 특정 시간대에만 유실이 생기는 식) 사용자가 준 임계값으로는 옳은
  동작을 판정하기 어렵다. 그래서 사용자가 **자기 알고리즘을 끼워 넣을 수 있게** 열어 둔다.
- **경보의 등급을 사용자가 겹쳐 매긴다.** 리스팅 1의 21~24줄이 같은 `Size` 메트릭에
  3표준편차 경고와 4표준편차 오류를 함께 걸어 둔 것이 그 실물이다 (리스팅 1,
  p.1783).[^schelter2018-data-quality]
- **5.4절의 시연은 가상의 사례다** (§5.4, p.1791).[^schelter2018-data-quality] 논문이
  `a fictitious use case`라고 스스로 부른다 — reddit 데이터를 질의응답 같은 정보 추출에
  쓴다고 가정하고, **토론 게시판별로 `Mean(controversiality)` 메트릭의 시계열**을 보아
  스팸·트롤 활동의 증가를 잡으려 한다. 체크는 이렇게 적힌다: `Check(Level.Warning,
  groupBy="subreddit").hasNoAnomalies("controversiality", Mean,
  OnlineNormal(upperDeviationFactor=3))`.
  - 결과(그림 9, p.1792)에서 `anime`·`askreddit`은 분산이 낮고 `cringepics`·
    `chicagobulls`에 뾰족한 값이 나와 탐지에 걸린다. **수동 조사에서 그 뾰족한 값이 그날
    삭제된 사용자 수와 강하게 상관**한다는 것을 확인했다고 적는다.
  - **이것은 효과 크기가 아니다** — 표본 하나의 시연이고, 탐지의 정밀도·재현율을 잰
    자리가 아니다.

## 실행 층 — 집계 질의 한 번으로 몰아넣기

- **구현은 Apache Spark 위이고, 저장은 AWS 인프라다** (§4,
  p.1787).[^schelter2018-data-quality] 다만 **Spark 전용 기능에 의존하지 않으며** SQL·
  사용자 정의 집계 함수·간단한 ML 모델을 지원하는 런타임이면 옮길 수 있다고 적는다.
  Spark를 고른 이유는 성능이 아니라 **Scala/JVM 환경이라 사용자가 검증 코드를 쓰고 외부
  라이브러리·시스템과 붙이기 쉬워서**다.
- 그림 2(p.1787)의 계층이 이 페이지의 구조를 그대로 옮긴 것이다 — 위에서부터 체크·제약
  API, 선언적 제약 정의와 메트릭·분석기(Analyzer)·이상 탐지기, 런타임(배치 계산·증분
  계산), 저장(메트릭 이력은 **DynamoDB**, 증분 계산의 중간 상태는
  **S3**).[^schelter2018-data-quality]
- **메트릭 하나에 분석기 하나가 붙는다** (§4, p.1787).[^schelter2018-data-quality]
  라이브러리가 제약을 훑어 필요한 메트릭을 정하고, 메트릭마다 그것을 계산할 수 있는
  분석기(**물리 연산자로 볼 수 있다**고 논문이 적는다)를 고른다. `AnalysisRunner`가 그
  분석기들의 실행을 예약한다.
- **최적화의 이름이 스캔 공유**(scan sharing)다 (§4 p.1787, §4.1
  p.1788).[^schelter2018-data-quality] 재분할이 필요 없는 메트릭들은 **필요한 집계 함수를
  모아 SparkSQL 질의 하나로 생성해** 데이터를 한 번만 훑고 동시에 계산한다. 3.1절의
  예에서는 데이터셋의 `Size`, 여섯 열의 `Completeness`, 세 `satisfies` 제약의
  `Compliance`가 **한 번의 훑기**로 함께 계산된다. 증분 쪽에는 하나가 더 붙는다 —
  많은 메트릭이 델타 크기를 필요로 하므로 **`count` 결과를 캐시한다.**
- **곧 선언의 개수가 훑기의 개수가 아니다.** 사용자가 체크를 몇 개 적었는지와 데이터를 몇
  번 읽는지가 분리돼 있고, 그 분리가 이 설계의 확장성 주장을 떠받친다.

## 규모에서 잰 것

**아래 수치는 전부 위 [실험 설정](#증분이-항상-이기지-않는다)의 클러스터와 데이터에
묶여 있다.**

- **배치 메트릭 계산은 데이터 크기에 선형이다** (그림 4, p.1789).[^schelter2018-data-quality]
  최대 **1억 2천만 레코드**까지 키우면서 네 가지 작업 부하를 쟀다 — 재분할이 필요 없는
  여섯 메트릭(데이터 크기 + 다섯 열의 완전성)과, 재분할이 필요한 `brand`·`material`·
  `product_id` 각각의 엔트로피·유일성이다. **넷 다 데이터 크기에 선형으로 늘고**, 재분할이
  드는 쪽이 더 비싸며 그 비용은 열의 카디널리티에 딸려 있다. 논문의 설명은 시스템이 내부적
  으로 **사용자 정의 집계 함수를 단 단순 집계 질의**를 생성해 SparkSQL에 넘기기 때문이다.
- **예측 가능성 추정의 실측** (§5.1, p.1789).[^schelter2018-data-quality]
  - **설정**: 위 상품 데이터에서 뽑은 **인기 브랜드 10개의 패션 상품 845,000건**이고,
    `name`·`description`·`size`·`bulletpoints`·`manufacturer` 등에서 `brand` 열의 값을
    맞히는 과제다. **표본의 80%로 나이브 베이즈를 훈련하고 나머지 20%에서 가중 F1을
    잰다.** 이 실험만 **단일 c4.8xlarge 인스턴스**에서 돌렸다.
  - **`name` 열 하나만으로도 모든 표본에서 가중 F1이 97%를 넘는다.**
  - 가장 좋은 것은 `name`에 `bulletpoints`·`description`·`manufacturer`를 더한 조합이고,
    **10만·20만·40만·60만 표본에서 각각 F1 97.3%·98.8%·99.4%·99.5%, 전체 데이터에서
    99.5%**다. **단위는 가중 F1 점수이고 분모는 각 표본의 남은 20%다.**
  - **훈련 시간은 전 경우에서 10초 미만**이고 전체 데이터에서도 그렇다. 시간은 주로
    **입력 열 문자열의 길이**에 달려 있다(텍스트가 긴 `description` 하나로 훈련하는 쪽이
    `name`+`bulletpoints`보다 오래 걸린다).
  - 논문은 이 결과를 **미래 데이터에 걸 제약의 근거**로 쓰는 법까지 보인다 — 관측된 값
    아래로 예측 가능성이 떨어지면 알림을 받도록 `hasPredictability("brand", (...),
    f1=0.97)`을 걸어 두는 식이다.

## 조직 층의 교훈 — 생산자가 소비자의 검사를 가져다 쓴다

**6절은 사용자 피드백의 서술이고 수치도 대조군도 없다** (§6,
pp.1791~1792).[^schelter2018-data-quality] 아래는 그 조건에서만 읽는다.

- **공용 라이브러리가 어휘를 만든다** — 팀들 사이에 데이터 품질을 논할 **공유 어휘**가
  서고, 품질을 재는 방식의 모범 사례가 자리 잡아 데이터셋의 메트릭을 감시하는 방법이
  하나로 모인다.
- **생산자와 소비자가 같은 시스템을 쓰는 것이 큰 이득이라고 적는다** (§6, p.1791):

  > It is also a big advantage if producers as well as consumers of datasets leverage the
  > same system for verifying data quality, as they can re-use checks and constraints from
  > each other, e.g., the producer can choose to adapt checks from downstream consumers
  > earlier in the data processing pipeline.

  **하류 소비자의 검사가 상류 생산자의 파이프라인으로 옮겨 간다** — 계약의 방향이
  소비자에서 생산자로 흐르는 구조이고, 이것이 이 페이지가
  [소비자 주도 계약](../concepts/consumer-driven-contracts.md)과 만나는 자리다.
- **사람이 하던 일을 대체한 자리를 밝힌다** (§6, p.1792) — 전에는 표본을 뽑아 눈으로 훑어
  불완전한 필드·이상치·기대 행 수와의 차이를 찾았고, 이제 그 검사가 **적재 파이프라인의
  일부로 자동 실행**된다.
- **생산자가 발행을 멈출 수 있다** (§6, p.1792) — 데이터 이상을 만나면 데이터 발행
  파이프라인을 세울 수 있고, 그럼으로써 하류의 처리(흔히 ML 모델 훈련)가 **검증된
  데이터로만** 돌게 만든다.

## 임의 제약이냐 제한된 스키마 언어냐

**같은 문제를 같은 해에 푼 두 프로덕션 시스템이 정반대의 표현력을 골랐고, 그 대비를
뒤에 나온 쪽이 문면으로 적었다.**

- 구글 쪽 논문의 7절이 이 논문을 지목해 이렇게 적는다:[^breck2019-data-validation]

  > While Amazon's system allows users to express arbitrary constraints, we opted to have a
  > restrictive schema definition language that captures the data constraints for most of
  > our users while permitting us to develop effective tools to help users manage their
  > schema.

- **이쪽(이 페이지)이 임의 제약을 여는 이유**는 위
  [네 설계 원칙](#네-설계-원칙)의 유연성이다 — 사용자가 외부 서비스를 부르고 임의의 함수를
  메트릭에 걸 수 있어야 한다고 못 박는다 (§1,
  p.1782).[^schelter2018-data-quality] 대가는 **제약의 집합을 기계가 관리할 수 없다는
  것**이다. 실제로 이 논문의 제약 관리 장치는 스키마 도구가 아니라 **제안 기능**이고,
  그 제안은 위에서 본 대로 **틀릴 수 있어 사람이 고른다.**
- **저쪽이 좁힌 이유는 거짓 양성이다** —
  [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md)이
  그 논거를 담는다. 좁은 스키마 언어와 사람의 수동 큐레이션이 거짓 양성을 막는 장치이고,
  그 대가로 표현할 수 없는 데이터 성질이 생긴다고 스스로 적는다.
- **인용 방향은 한쪽뿐이다.** 이 논문은 상대를 인용하지 않는다(1년 먼저 나왔다). 대신 같은
  구글 팀의 다른 글을 참고문헌 [9](`Data Infrastructure for Machine Learning`, SysML
  2018)과 [5](TFX, KDD 2017)로 인용하며, 7절에서 `modern machine learning platforms begin
  to have explicit data validation components`라고 묶어 적는다 (§7,
  p.1792).[^schelter2018-data-quality]
- **둘의 공통 전제는 같다** — 데이터에는 선재하는 명세가 없다. 갈리는 것은 **그 자리를
  무엇으로 채우는가**다. 저쪽은 데이터에서 추론해 사람이 승인하는 **스키마 하나**를
  두고, 이쪽은 사용자가 임의로 적는 **제약 여럿**을 두고 제안으로 거든다.

## 이 KB의 다른 데이터 페이지와 갈리는 자리

이 페이지가 답하는 질문은 **선언한 것이 무엇으로 환원되어 어떻게 실행되는가**다. 이웃한
데이터 페이지들은 같은 낱말을 쓰면서 다른 질문에 답한다.

- [데이터 품질 강제 패턴](../concepts/data-quality-enforcement-patterns.md) — **검증을
  어느 자리에서 강제하는가.** AWAP는 변환 앞뒤에 감사 단계를 두고 Constraints Enforcer는
  검증을 저장소에 위임한다. **거기서 규칙의 내용과 실행 방식은 주어진 것으로 놓는다** —
  이 페이지가 담당하는 것이 그 규칙을 적는 언어와 그 언어가 도는 방식이다. 이 논문의
  체크는 저장소가 아니라 **파이프라인 안에서 Spark 잡으로** 돌므로 배치로는 AWAP 쪽에
  가깝고, 발행을 멈출 수 있다는 6절의 대목이 그 감사 단계의 결말과 겹친다.
- [품질 관측 패턴](../concepts/quality-observation-patterns.md) — **오늘의 규칙이
  낡았는지 어떻게 관측하는가.** 그쪽의 관측자는 규칙을 적응시키기 위해 데이터를 보고,
  이쪽은 **메트릭을 이력으로 쌓아 그 시계열에 이상 탐지를 건다.** 그쪽이 "관측은
  막지 않는다"로 가른 것을 이 논문은 **체크 수준(경고냐 오류냐)으로** 가른다.
- [관측 탐지 패턴](../concepts/observability-detector-patterns.md) — **초록불로 끝난 잡이
  실은 틀렸다는 것을 어떻게 아는가.** 거기의 Skew Detector가 이전 실행과 비교해 허용
  임계값을 넘었는지 보는 구조가 여기 `OnlineNormal`과 같은 모양이고, **죽음의 고리**(나쁜
  날이 새 기준이 된다)가 이쪽에도 그대로 걸린다 — 과거 메트릭이 기준이기 때문이다.
- [데이터 웨어하우스의 데이터 품질 관리](../concepts/data-quality-management.md) —
  **나쁜 데이터를 어디서 교정하는가.** 그쪽의 품질 특성 셋(정확성·완전성·적시성)과 이
  논문의 차원 셋(완전성·일관성·정확성)이 **겹치되 같지 않다.** 그리고 **이 논문은 교정을
  하지 않는다** — 7절이 AJAX와 대비하며 데이터 수리를 지원하지 않는다고 명시한다.
- [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md) —
  **기대가 어디서 오는가.** 위
  [임의 제약이냐 제한된 스키마 언어냐](#임의-제약이냐-제한된-스키마-언어냐) 참조.
- [훈련 데이터 품질](../concepts/training-data-quality.md) — **좋은 훈련 데이터란
  무엇인가**(양 대 질). 이 페이지는 좋고 나쁨이 아니라 **선언된 제약과의 어긋남**을 다룬다.

## 이어지는 페이지

- [소비자 주도 계약](../concepts/consumer-driven-contracts.md) — 기대를 적은 사양을
  누가 소유하는가. 6절의 "생산자가 하류 소비자의 검사를 가져다 상류에 건다"가 그 구조의
  데이터 파이프라인판이다
- [속성 기반 테스트](../concepts/property-based-testing.md) — 기대를 사례가 아니라
  속성으로 적는 갈래. 제약을 데이터 전체에 걸리는 불변식으로 적는다는 점이 같고, 다만
  입력을 기계가 만들지 않고 **이미 있는 데이터가 입력**이라는 점이 다르다
- [계약에 의한 설계](../concepts/design-by-contract.md) — 사전·사후 조건이 기대의 출처가
  되는 갈래
- [읽기 스키마와 쓰기 스키마](../concepts/schema-on-read-and-schema-on-write.md) —
  스키마 없는 데이터에서 시작한다는 이 논문의 전제가 그쪽의 조건이다
- [테스트 오라클](../concepts/test-oracle.md) — 기대값의 출처를 네 갈래로 가른 이론.
  제안된 제약이 **표본에서 참인 것**이라는 위 [제안은 틀린다](#제안은-틀린다--표-3이-잰-것)의
  구조가 그 분류의 어디에 앉는지가 두 페이지가 만나는 자리다
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) —
  기대값을 대상 자신에게서 길어 올릴 때 무엇이 남고 무엇이 사라지는가. 메트릭 이력을
  기준으로 삼는 이상 탐지가 데이터 층의 같은 절차다
- [함수형 데이터 엔지니어링](functional-data-engineering.md) — 이 논문이 append-only
  가정으로 비켜 간 물음, 곧 **파이프라인을 함수로 보아 재실행이 같은 결과를 내는가**(멱등)를
  정면으로 다루는 자리. 그쪽은 기대를 선언하지 않고도 두 실행을 견주지만, 그래서 **틀린
  데이터를 결정적으로 틀리게 처리하는 파이프라인**은 잡지 못한다 — 그 빈자리를 메우는 것이
  이 페이지의 제약이다
- [데이터 캐스케이드](../concepts/data-cascades-in-high-stakes-ai.md) — **이 논문이 동기로만 말하고
  재지 않은 물음**, 곧 검증을 상류에 두지 않았을 때 오염이 하류에서 어떻게 불어나는가.
  그쪽이 고위험 AI 실무자 53명의 인터뷰로 그 하류를 기록한다 — 상류에서 촉발돼 하류에서
  드러나기까지 2~3년이 걸린 사례까지. **근거의 격이 다르다**: 이 논문은 자기 시스템에
  대한 측정이고 그쪽은 자기 보고 인터뷰의 코딩이다. 그리고 그쪽의 처방은 제약 선언이
  아니라 인센티브·교육·문서화의 구조 변화다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 판정 근거 쪽의 허브
- [데이터 엔지니어링 설계 패턴](../synthesis/data-engineering-design-patterns.md) —
  데이터 품질 패턴 쪽의 허브

[^schelter2018-data-quality]: Schelter, Lange, Schmidt, Celikel, Biessmann, Grafberger
    2018, "Automating Large-Scale Data Quality Verification", PVLDB 11(12):1781–1794.
    locator는 인쇄 쪽 번호와 절·표·그림·리스팅 번호다. 수식·기호·위첨자가 든 자리와
    리스팅 1은 `pdftotext`가 훼손해(`≠`→`6=`, `10⁸`→`108`, 식별자 낱자 분리) 150dpi
    렌더 이미지로 재대조했다 — 소스 메타 참조.

[^breck2019-data-validation]: Breck, Polyzotis, Roy, Whang, Zinkevich 2019, "Data
    Validation for Machine Learning", 2nd SysML Conference, §7(확보본 PDF p.10).
    이 KB의 [소스 메타](../sources/breck2019-data-validation.md) 참조.

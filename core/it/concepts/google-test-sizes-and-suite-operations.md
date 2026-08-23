---
type: concept
title: 구글의 테스트 크기 어휘와 스위트 운영
description: 크기를 자원 제약으로 정의하고 범위와 갈라 놓은 어휘의 정본 서술과 그 어휘를 10년 앞서 낸 블로그와의 차이, 단위 테스트 80퍼센트라는 비중이 측정이 아니라 다른 책의 피라미드에서 온 목표치라는 것과 같은 회사가 다섯 해 앞서 낸 다른 배합, 그 비중을 정면으로 부정하는 에세이와 이 페이지가 이루는 모순 쌍의 축 셋, 불안정 비율 0.15퍼센트의 분모와 이 책에 없는 조문, 재실행 완화를 조건부로 승인하는 문면, 큰 테스트가 사내 지속 통합 관문 밖에 있다는 자인, 그리고 이 서술 전체가 기대는 규모 전제
generated: { by: "claude-opus-5", at: "2026-08-24T07:00:00Z" }
contradicts: [unit-testing-as-waste]
sources:
  - { id: winters2020-swe-at-google, resource: /it/sources/winters2020-swe-at-google.md }
  - { id: stewart2010-test-sizes, resource: /it/sources/stewart2010-test-sizes.md }
---

# 구글의 테스트 크기 어휘와 스위트 운영

- [이 소스의 지위와 규모 전제](#이-소스의-지위와-규모-전제)
- [크기와 범위는 다른 축이다](#크기와-범위는-다른-축이다)
- [세 크기의 제약](#세-크기의-제약)
- [표기 규약 — 원어를 유지한다](#표기-규약--원어를-유지한다)
- [계보 — 10년 앞선 정의 표](#계보--10년-앞선-정의-표)
- [단위 테스트가 다수여야 한다 — 비중 목표와 그 지위](#단위-테스트가-다수여야-한다--비중-목표와-그-지위)
- [반대 극과 무엇이 부딪히는가](#반대-극과-무엇이-부딪히는가)
- [불안정 테스트 — 이 책이 적은 값과 적지 않은 조문](#불안정-테스트--이-책이-적은-값과-적지-않은-조문)
- [큰 테스트는 관문 밖에 있다](#큰-테스트는-관문-밖에-있다)
- [커버리지에 대한 이 책의 한 문단](#커버리지에-대한-이-책의-한-문단)
- [규모를 떼면 무엇이 남는가](#규모를-떼면-무엇이-남는가)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 크기의 테스트를 얼마나 두고 그 스위트의 비결정성을 어떻게 다루는가에
대해, 한 대규모 조직이 자기 실무로 적어 놓은 답은 무엇이며 그 답은 어떤 격의 근거인가.**

## 이 소스의 지위와 규모 전제

- **근거 등급은 `industry-norm`이다.** 통제도 표본도 재현 절차도 없다. 이 페이지가 옮기는
  값은 전부 **회사가 정한 목표치이거나 사내 계측의 요약 진술**이고, 이 KB는 그것을
  측정값으로 쓰지 않는다.
- **책이 스스로 적는 규모 조건이 이 서술의 전제다** (11장 §"Testing at Google
  Scale").[^winters2020-swe-at-google] 거의 모든 코드가 하나의 단일 저장소(monorepo)에
  있고 `more than two billion lines of code`이며, 그 저장소가 주마다
  `close to 25 million lines of change`를 겪는다. 그 변경의 절반가량이 자동화 시스템이
  만든 것이고, 거의 어떤 팀도 저장소 지점(branch)을 쓰지 않아 모든 변경이 저장소 머리에
  바로 들어간다. 그 위에 사내 지속 통합 체계 **TAP**(Test Automated Platform)이 선다.
  - **이 조건들은 측정이 아니라 조직 서술이다.** 그러나 아래 조문 전부가 이 조건 위에
    서 있으므로 조문만 떼어 옮길 수 없다.
- **언어 모델 시대의 재검이 없다.** 2020년 책이고, 생성된 테스트가 스위트에 대량으로 들어올
  때 이 비중과 이 불안정 목표가 어떻게 되는지를 이 책은 다루지 않는다. 이 KB는 이 소스를
  **그 이전 시대의 실무 증언**으로 두고 절대 진리로 두지 않는다.

## 크기와 범위는 다른 축이다

**이 책의 첫 기여가 크기(size)와 범위(scope)라는 두 축으로 어휘를 가른 것이다**
(11장 §"Designing a Test Suite").[^winters2020-swe-at-google]

> We have come to the conclusion that there are two distinct dimensions for every test
> case: size and scope. Size refers to the resources that are required to run a test case:
> things like memory, processes, and time. Scope refers to the specific code paths we are
> verifying.

- **왜 "단위"와 "통합"으로 부르지 않는지도 같은 절에 적혀 있다** (11장 §"Test
  Size").[^winters2020-swe-at-google]

  > We make this distinction, as opposed to the more traditional "unit" or "integration,"
  > because the most important qualities we want from our test suite are speed and
  > determinism, regardless of the scope of the test.

- **범위 쪽 어휘도 따로 정의된다** (11장 §"Test Scope").[^winters2020-swe-at-google] 좁은
  범위(narrow-scoped, 흔히 단위 테스트)는 클래스나 메서드 하나의 논리를, 중간 범위
  (medium-scoped, 흔히 통합 테스트)는 소수 구성 요소 사이의 상호작용을, 넓은 범위
  (large-scoped, 기능·종단(end-to-end)·시스템 테스트)는 여러 부분의 상호작용이나 창발
  동작을 검증한다.
- **범위는 실행된 코드가 아니라 검증되는 코드로 센다** (11장 §"Test
  Scope").[^winters2020-swe-at-google]

  > when we talk about unit tests as being narrowly scoped, we're referring to the code
  > that is being *validated*, not the code that is being executed.

- **두 축이 직교라는 것을 예로 못 박는다** (11장 §"Test Scope").[^winters2020-swe-at-google]
  모든 프로세스 밖 의존을 대역(test double)으로 세우면 넓은 범위의 서버 종단점 테스트도
  small일 수 있고, 날짜 선택기 하나를 검증하려고 브라우저 전체를 띄워야 하면 좁은 범위의 테스트도 medium이
  된다.

## 세 크기의 제약

**크기는 줄 수가 아니라 무엇을 해도 되는가로 정해진다** (11장 §"Test
Size").[^winters2020-swe-at-google]

> A test's size is determined not by its number of lines of code, but by how it runs, what
> it is allowed to do, and how many resources it consumes. … in brief, small tests run in a
> single process, medium tests run on a single machine, and large tests run wherever they
> want

| 크기 | 프로세스·기계 | 금지되는 것 | 열리는 것 |
|---|---|---|---|
| small | 단일 프로세스(언어에 따라 단일 스레드) | 잠자기·입출력·그 밖의 블로킹 호출, 네트워크와 디스크, 별도 프로세스로 뜨는 데이터베이스 | 대역으로 바꾼 가벼운 의존 |
| medium | 여러 프로세스, 한 기계 | `localhost` 밖으로 나가는 네트워크 호출 | 스레드, 블로킹 호출, 실제 데이터베이스 인스턴스, 브라우저 구동 |
| large | 여러 기계 | (크기 제약 없음) | 원격 클러스터의 시스템까지 |

- **small의 입출력 금지에 예외 한 줄이 각주로 붙는다** (11장 각주 5).[^winters2020-swe-at-google]
  밀폐된(hermetic) 메모리 구현을 쓴다면 파일 시스템 접근이 허용된다.
- **네 번째 크기가 각주에만 있다** (11장 각주 4).[^winters2020-swe-at-google]

  > Technically, we have four sizes of test at Google: small, medium, large, and
  > *enormous*. The internal difference between large and enormous is actually subtle and
  > historical

  **본문의 large 서술은 사실 enormous에 해당한다고 책이 스스로 적는다.**
- **정의가 집행된다** (11장 §"Test sizes in practice").[^winters2020-swe-at-google] 자바
  테스트는 사용자 정의 보안 관리자 아래 돌아서 small로 표시된 테스트가 네트워크 연결 같은
  금지 행위를 시도하면 실패한다. **다만 같은 문단이 단서를 단다** —
  `The extent to which these definitions are enforced at Google varies by language.`
- **큰 테스트는 개발자 작업 흐름에서 분리해 돌린다** (11장 §"Large
  tests").[^winters2020-swe-at-google] 여러 팀이 큰 테스트를 small·medium과 갈라 빌드와
  릴리스 과정에서만 돌린다고 적는다.

## 표기 규약 — 원어를 유지한다

**이 KB는 크기 이름을 번역하지도 음차하지도 않고 `small`·`medium`·`large`로 적는다.**
근거 셋이다.

- **이 낱말들은 개념어이기 전에 식별자다.** 빌드 도구의 주석·속성 값으로 코드에 그대로
  적히고(11장의 자바 보안 관리자 집행, 계보 글의 자바 애너테이션), 번역하면 그 자리와
  이어지지 않는다.
- **확립 역어가 없다.** SCHEMA의 규칙이 미확립이면 원어를 유지하라고 한다.
- **"소·중·대"는 형태소 색인에서 값어치가 없다.** 한 글자 한자어라 다른 문맥의 같은 글자와
  구분되지 않는다. `small test`라는 원어가 불변 검색 키로 남는 편이 낫다.

한국어 문장 안에서 "작은 테스트"처럼 풀어 쓰는 것은 설명일 때만 하고, 크기 이름을 가리킬
때는 원어를 쓴다. 범위 쪽 어휘도 같다 — `narrow-scoped`·`medium-scoped`·`large-scoped`는
"좁은 범위"·"중간 범위"·"넓은 범위"로 옮기되 첫 등장에 원어를 병기한다.

## 계보 — 10년 앞선 정의 표

**이 어휘의 최초 공개는 이 책이 아니다.** 2010년 12월 13일 구글 테스팅 블로그에 Simon
Stewart가 같은 세 이름을 표로 냈다.[^stewart2010-test-sizes]

> Over time we've come to agree on a set of data-driven naming conventions for our tests.
> We call them "Small", "Medium" and "Large" tests.

| 항목 | Small | Medium | Large |
|---|---|---|---|
| Network access | No | localhost only | Yes |
| Database | No | Yes | Yes |
| File system access | No | Yes | Yes |
| Use external systems | No | Discouraged | Yes |
| Multiple threads | No | Yes | Yes |
| Sleep statements | No | Yes | Yes |
| System properties | No | Yes | Yes |
| Time limit (seconds) | 60 | 300 | 900+ |

**표는 2010년 글의 것을 그대로 옮긴 것이다.** 제약의 뼈대는 10년 뒤 책과 같다.

**그러나 한 자리에서 정의가 갈린다.** 2010년 글은 크기를 범위 어휘와 **등치**시킨다.

> A Small test equates neatly to a unit test, a Large test to an end-to-end or system test
> and a Medium test to tests that ensure that two tiers in an application can communicate
> properly (often called an integration test).[^stewart2010-test-sizes]

2020년 책은 같은 자리에서 정확히 그 등치를 **거부하고** 크기와 범위를 두 축으로 가른다
(위 [크기와 범위는 다른 축이다](#크기와-범위는-다른-축이다)). **10년 사이에 바뀐 것이 이것
하나다** — 제약 표가 아니라 그 표가 무엇을 뜻하는가가 바뀌었다.

- **그래서 이 KB는 책을 정본 서술로, 블로그를 계보 각주로 둔다.** 크기 어휘를 인용할 때
  2010년 글의 등치 문장을 함께 옮기면 이 책의 구분이 지워진다.
- **차이 둘 더**: 시간 제한(60·300·900+초)은 2010년 글에만 있고 책에는 없다. `enormous`는
  책의 각주에만 있고 2010년 글에는 없다.
- **`data-driven`이라는 낱말에 속지 않는다.** 2010년 글이 그렇게 부르는 이유는 이름이 잴 수
  있는 제약으로 정의되기 때문이지 이 분류가 데이터로 검증됐다는 뜻이 아니다. **두 문헌 어느
  쪽에도 이 분류의 효과를 잰 수치가 없다.**

## 단위 테스트가 다수여야 한다 — 비중 목표와 그 지위

**이 절이 이 책에서 가장 많이 인용되고 가장 자주 오인되는 자리다.**

- **11장의 세 갈래 비중** (11장 §"Test Scope"):[^winters2020-swe-at-google]

  > As a very rough guideline, we tend to aim to have a mix of around 80% of our tests
  > being narrow-scoped unit tests that validate the majority of our business logic; 15%
  > medium-scoped integration tests that validate the interactions between two or more
  > components; and 5% end-to-end tests that validate the entire system.

- **12장의 두 갈래 판본** (12장 도입부):[^winters2020-swe-at-google]

  > Due to their many advantages, most tests written at Google are unit tests, and as a
  > rule of thumb, we encourage engineers to aim for a mix of about 80% unit tests and 20%
  > broader-scoped tests.

- **이 값은 측정이 아니다. 책이 세 겹으로 그렇게 적는다.**
  - `As a very rough guideline`과 `we tend to aim to have` — **목표치의 문법이지 관측의
    문법이 아니다.** 12장 쪽은 `as a rule of thumb`.
  - **그림 11-3의 설명글이 출처를 밝힌다** (11장 그림 11-3 캡션과 각주
    6):[^winters2020-swe-at-google] `Google's version of Mike Cohn's test pyramid;
    percentages are by test case count, and every team's mix will be a little different`.
    각주 6이 그 피라미드의 출처를 Mike Cohn, *Succeeding with Agile*(Addison-Wesley,
    2009)로 단다. **출처가 회사 데이터가 아니라 다른 책의 그림이다.**
  - **바로 다음 문단이 다른 배합을 허용한다** (11장 §"Test Scope"):[^winters2020-swe-at-google]
    `When considering your own mix, you might want a different balance.` 그리고 절의 끝
    문장이 `A good test suite contains a blend of different test sizes and scopes that are
    appropriate to the local architectural and organizational realities.`
- **집계 단위는 테스트 케이스 수다** (그림 11-3 캡션). 실행 시간도 코드 줄 수도 아니다.
  이 값을 옮길 때 이 분모를 빼면 다른 주장이 된다.
- **책이 배격하는 배합에는 이름이 붙어 있다** (11장 §"Test Scope").[^winters2020-swe-at-google]
  종단 테스트만 많고 통합·단위가 적은 `ice cream cone`, 종단과 단위는 많은데 통합이 적은
  `hourglass`. 뒤엣것은 의존을 따로 세우기 어렵게 만드는 강한 결합에서 생긴다고 적는다.
  - **두 이름도 이 책이 처음이 아니다.** 같은 회사의 2015년 블로그가 같은 두 이름을 같은
    뜻으로 쓴다 —
    [종단 테스트를 왜 줄이는가](../concepts/why-fewer-end-to-end-tests.md)의 배합 절.
- **같은 회사가 다섯 해 앞서 다른 배합을 냈다.** 2015년 블로그의 값은 70/20/10이고 어조는
  `As a good first guess, Google often suggests`다. **이 책의 80/15/5와 수치가 다르고, 둘 다
  측정이 아니라 제안이다.** 두 값의 차이와 집계 단위의 차이는
  [종단 테스트를 왜 줄이는가](../concepts/why-fewer-end-to-end-tests.md)가 표로 소유한다 —
  이 페이지는 이 책의 문면을, 그쪽은 그 배합을 고르는 논거를 소유한다.
- **단위 테스트 편향의 이유도 규범 진술이다** (11장 §"Test Scope").[^winters2020-swe-at-google]
  큰 테스트는 제품이 자라는 동안의 **온전성 검사**이고
  `they should not be viewed as a primary method for catching bugs`라고 쓴다.
- **같은 절이 단위 테스트의 한계도 적는다** — 단위 테스트는 서로 다른 팀이 만든 두 시스템
  사이의 계약 같은 구성 요소 간 상호작용을 검증하지 못한다.

**이 절이 이 KB에서 갖는 자리** — 단위 테스트 비중을 두고 갈리는 논쟁에서 이 페이지가 서는
극이 여기다. 단위 테스트를 다수로 두라는 쪽의 문면이고, 반대 극은 단위 테스트의 값어치를
낮게 보는 쪽이다. **그 논쟁에서 이 페이지를 인용할 때 걸리는 문장이 위 두 직인용이며, 그
지위가 측정이 아니라 목표치라는 것이 이 페이지의 판정이다.**

## 반대 극과 무엇이 부딪히는가

**이 페이지는 [단위 테스트는 대부분 낭비인가](unit-testing-as-waste.md)와
`contradicts`로 묶인다. 이 KB는 이 모순을 해소하지 않는다.** 그쪽은 단위 테스트 대부분이
낭비이며 무게를 통합·시스템 테스트와 단정(assertion)으로 옮기라고 주장하는 2014년의
실무자 에세이다.

**부딪히는 축은 셋이다.**

| 축 | 이 페이지의 극 | 반대 극 |
|---|---|---|
| 단위 테스트의 비중 | `we tend to aim to have a mix of around 80% of our tests being narrow-scoped unit tests` (11장) | 대부분이 낭비이며 시스템 테스트로 옮기라 |
| 큰 테스트의 자리 | 온전성 검사이고 `they should not be viewed as a primary method for catching bugs` (11장) | 값어치가 큰 쪽이 통합·시스템 테스트다 |
| 오래 통과한 테스트 | 회귀를 막는 관문에 계속 둔다. 값어치가 사라지는 기준으로 이 책이 드는 것은 실패 없음이 아니라 **불안정**이다(아래 [불안정 테스트](#불안정-테스트--이-책이-적은-값과-적지-않은-조문)) | 1년 동안 실패하지 않았으면 버릴 첫 부류다 |

- **두 극이 부딪히는 것은 데이터가 아니라 규범이다.** 양쪽 다 측정이 아니다 — 이쪽은
  `industry-norm`이고 80%의 출처가 위에서 본 대로 다른 책의 피라미드이며, 저쪽은 `essay`이고
  동료심사도 참고문헌 목록도 없다. **어느 쪽 수치도 상대를 반박하는 근거로 쓰이지 않는다.**
- **전제도 갈린다.** 이 페이지의 조문은 위 [규모 전제](#이-소스의-지위와-규모-전제) 위에 서
  있고, 저쪽의 조문은 한 컨설턴트가 만난 팀들의 사례 위에 선다. **어느 쪽도 상대의 조건에서
  시험되지 않았다.**
- **한 자리에서는 두 극이 같은 말을 한다** — 커버리지 목표치가 사람의 행동을 바꾼다는 관찰이
  양쪽에 다 있다. 아래 [커버리지에 대한 이 책의 한 문단](#커버리지에-대한-이-책의-한-문단)의
  천장 관찰이 이쪽 문면이고, 저쪽은 목표치를 채우려고 함수를 쪼개 아키텍처가 무너진 사례를
  적는다. **같은 방향이되 실패 양식이 다르므로 하나로 뭉쳐 인용하지 않는다.**
- **이 KB는 어느 쪽도 정설로 세우지 않는다.** 한쪽만 인용해 "단위 테스트가 80%여야 한다"
  또는 "단위 테스트는 낭비다"로 읽는 것이 이 자리에서 가장 흔한 오독이다.

## 불안정 테스트 — 이 책이 적은 값과 적지 않은 조문

**불안정(flaky) 테스트는 프로덕션 코드가 바뀌지 않았는데도 결과가 뒤집히는 테스트다**
(12장 각주 1·3).[^winters2020-swe-at-google] 12장은 그것을 깨지기 쉬운(brittle) 테스트와
구분한다 — 깨지기 쉬운 테스트는 무해한 변경에 결정적으로 실패하고, 불안정한 테스트는
변경 없이 비결정적으로 실패한다.

- **이 책이 적은 값은 하나다** (11장 §"Case Study: Flaky Tests Are
  Expensive"):[^winters2020-swe-at-google]

  > Our experience suggests that as you approach 1% flakiness, the tests begin to lose
  > value. At Google, our flaky rate hovers around 0.15%, which implies thousands of flakes
  > every day. We fight hard to keep flakes in check, including actively investing
  > engineering hours to fix them.

  - **단위와 분모**: 0.15%는 비율(원값)이고 `our flaky rate`라는 말 외에 집계 절차가 적혀
    있지 않다. 1%는 측정이 아니라 값어치가 사라지기 시작하는 지점에 대한
    `Our experience suggests` — **경험 진술이다.**
  - **같은 절의 10건은 예시 계산이다** — 테스트마다 0.1%씩 잘못 실패하고 하루 1만 건을
    돌리면 하루 10건을 조사하게 된다는 산수이고, 관측값이 아니다.
- **분모의 경계를 14장이 따로 적는다** (14장 §"Large Tests and the Developer
  Workflow"):[^winters2020-swe-at-google]

  > At Google, many of these large tests do not belong in TAP. They are nonhermetic, too
  > flaky, and/or too resource intensive.

  **불안정해서 관문 밖으로 나간 것들이 있다는 자인이다.** 0.15%는 그 밖으로 나간 것을 뺀
  모집단 위의 값이므로, 이 값을 "구글은 스위트 전체를 0.15%로 유지한다"로 읽으면 원문이
  하지 않은 주장이 된다.
- **"불안정 0" 같은 조문은 이 책에 없다.** 11~14장의 `flak*` 문장을 전수 대조했고 그런
  요구가 없다. **오히려 재실행 완화를 조건부로 승인한다** (11장 §"Case Study: Flaky Tests
  Are Expensive"):[^winters2020-swe-at-google]

  > In some cases, you can limit the impact of flaky tests by automatically rerunning them
  > when they fail. This is effectively trading CPU cycles for engineering time. At low
  > levels of flakiness, this trade-off makes sense. Just keep in mind that rerunning a
  > test is only delaying the need to address the root cause of flakiness.

  - **다만 한 자리에서 무관용에 가까운 서술이 나온다** (11장 §"Test
    Certified").[^winters2020-swe-at-google] 옛 사내 등급 제도의 5단계 도달 조건에
    `remove all nondeterministic tests`가 있었다. 그러나 그 제도는 2015년에 자동 지표로
    대체됐다고 같은 절이 적고, **레벨 1의 조건은 불안정 테스트를 "찾되 반드시 고칠 필요는
    없다"였다**(`identify (but don't necessarily fix) flaky tests`). 등급 사다리의 마지막
    칸이지 회사의 조문이 아니다.
- **비결정성의 대가는 신뢰다** (11장 §"Case Study…").[^winters2020-swe-at-google] 불안정이
  늘면 생산성 손실보다 나쁜 것이 오고, 그것은 스위트에 대한 신뢰의 상실이다 — 신뢰가 무너지면
  엔지니어가 실패에 반응하기를 멈추고 스위트가 주던 값어치가 사라진다.
- **불안정의 출처**는 시계, 스레드 스케줄링, 네트워크 지연 같은 비결정성이고, 때로는 하드웨어
  인터럽트나 브라우저 렌더링 엔진처럼 낮은 층에 묶여 있다 (11장 §"Case Study…").
- **큰 테스트 쪽에서는 성격이 다르다** (14장 §"Driving out flakiness").[^winters2020-swe-at-google]
  작은 테스트에서 나쁜 것이 큰 테스트에서는 테스트를 못 쓰게 만든다고 적고, 완화의 첫걸음을
  **범위를 줄이는 것**으로 둔다. 잠자기 대신 상태 전이 폴링·이벤트 처리기·알림 구독을 쓰라는
  처방이 같은 절에 있다.
- **그 처방이 심사 실증으로 서 있는 자리는 따로 있다** —
  [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md).
  이 책은 잠자기를 쓰지 말라고 권하되 그 권고에 수치를 붙이지 않는다. 그쪽 페이지가 옮긴
  2014년 실증은 잠자기로 고친 20건이 불안정을 **하나도 없애지 못했다**는 표를 갖고 있다.

## 큰 테스트는 관문 밖에 있다

- **큰 테스트의 성질을 책이 먼저 규정한다** (14장 §"What Are Larger
  Tests?").[^winters2020-swe-at-google] 느릴 수 있고(기본 시간 제한이 15분 또는 1시간이며
  몇 시간이나 며칠 도는 것도 있다), 밀폐되지 않을 수 있고, 비결정적일 수 있다 —
  `If a large test is nonhermetic, it is almost impossible to guarantee determinism`.
- **TAP의 적격 조건이 그것을 밖으로 밀어낸다** (14장 §"Larger Tests at
  Google").[^winters2020-swe-at-google]

  > it was only able to do so for tests that met TAP's eligibility requirements: hermetic
  > tests buildable at a single change that could run on our build/test cluster within a
  > maximum time limit. Although most unit tests satisfied this requirement, larger tests
  > mostly did not.

  **그래서 큰 테스트에는 별도의 사후 제출 지속 빌드가 따로 있다**(14장 §"Large Tests and
  the Developer Workflow").
- **큰 테스트를 안 두는 것이 답은 아니라고 같은 장이 적는다** (14장 §"Common Gaps in Unit
  Tests").[^winters2020-swe-at-google] 단위 테스트가 놓치는 자리를 다섯으로 나눈다 —
  충실하지 않은 대역, 설정(configuration) 문제, 부하에서만 드러나는 문제, 예상하지 못한
  동작과 입력, 그리고 범위 밖에서 일어나는 창발 동작.
  - **설정에 대해서는 자기 사고를 예로 든다** (14장 §"Configuration issues") —
    `At Google, configuration changes are the number one reason for our major outages`.
    2013년의 전역 장애가 검사되지 않은 네트워크 설정 반영에서 왔다고 적는다. **순위 진술이지
    분모 있는 계측이 아니다.**
- **큰 테스트의 값어치를 갉는 것은 표준의 부재와 소유권이다** (14장 §"Why Not Have Larger
  Tests?"·§"Owning Large Tests").[^winters2020-swe-at-google] 단위 테스트는 단위를 가진
  사람이 소유하지만 큰 테스트는 여러 단위를 걸쳐 소유자가 갈린다 —
  `Without clear ownership, a test rots.` 그리고 팀마다 큰 테스트를 짜고 돌리는 방식이
  달라 대규모 변경 때 **그냥 건너뛰어진다**고 적는다.
- **큰 테스트도 작을수록 낫다** (14장 §"Tip: 'The Smallest Possible Test'").[^winters2020-swe-at-google]
  거대한 하나보다 큰 것 몇 개가 낫고, 사용자 여정을 여러 개의 짝 통합 테스트로 **사슬처럼
  이어** 앞 테스트의 산출을 뒤 테스트의 입력으로 쓰는 방법을 든다.

## 커버리지에 대한 이 책의 한 문단

11장이 커버리지를 한 문단으로만 다루고 그 결론이 이 KB의
[커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md)와 같은 방향이다
— **두 문헌의 저자가 겹친다**(11장 저자가 그 글의 공저자다).

- **집계 대상을 small로 한정하라고 권고한다** (11장 §"A Note on Code
  Coverage"):[^winters2020-swe-at-google]

  > We recommend only measuring coverage from small tests to avoid coverage inflation that
  > occurs when executing larger tests.

  **위 [크기와 범위는 다른 축이다](#크기와-범위는-다른-축이다)가 이 권고의 전제다** —
  크기라는 축이 없으면 "어느 테스트의 커버리지인가"를 물을 수 없다.
- **목표치가 천장이 된다는 관찰이 같은 문단에 있다** (11장 §"A Note on Code
  Coverage").[^winters2020-swe-at-google] 팀이 80% 같은 기준을 세우면 엔지니어가 그것을
  바닥이 아니라 천장으로 다루게 되고, 곧 그 이상을 넘지 않는 변경이 들어오기 시작한다고
  적는다 — `why do more work than the metric requires?`
- **줄이 실행된 것과 그 줄이 옳은지 확인된 것은 다르다**는 구분도 같은 문단에 있다.

## 규모를 떼면 무엇이 남는가

**`verdict: caveat`이 요구하는 단서다.** 위 조문들을 1인 프로젝트나 소규모 팀으로 옮길 때
전제가 함께 가지 않으면 조문이 거짓이 된다.

- **집행 장치가 없으면 크기는 규약이 아니라 희망이다.** 이 책의 크기 정의가 실효를 갖는
  이유는 보안 관리자가 small을 실패시키기 때문이다(11장 §"Test sizes in practice").
  주석만 달고 집행이 없으면 크기는 문서에 적힌 분류로 남는다. **이 축에서 옮겨 갈 수 있는
  것은 값이 아니라 "잴 수 있는 제약으로 정의한다"는 형식이다.**
- **80/15/5는 목표치이고 그 출처가 다른 책이다.** 위 절이 그 계보를 적었다. 자기 조직의
  아키텍처와 조직 현실에 맞춰 배합을 정하라는 것이 원문의 마지막 문장이다.
- **0.15%는 분모가 정의된 값이다.** 관문 밖으로 나간 큰 테스트가 그 분모에 없다. 관문이
  하나뿐인 조직에서는 같은 방식으로 낮은 값을 얻을 수 없다.
- **큰 테스트의 별도 지속 빌드·전담 소유자·사슬 구성은 사람이 여럿일 때의 처방이다.**
  소유자가 한 사람이면 "소유권을 문서화하라"는 조문이 할 일을 남기지 않는다. 그 조건에서
  남는 것은 **큰 테스트를 작게 유지하라**는 쪽이다.

## 이 소스의 사각

- **측정이 없다.** 크기 분류가 실제로 속도와 결정성을 개선했다는 주장에 붙은 근거가
  경험 진술이다. 분류 도입 전후를 비교한 수치가 없다.
- **80/15/5의 유래가 자기 데이터가 아니다.** 왜 80인지, 왜 15와 5인지, 다른 배합을 시험해
  봤는지가 책에 없다.
- **0.15%의 집계 절차가 없다.** 무엇을 한 건으로 세는지(테스트 케이스인가 실행인가), 어느
  기간인지, 어느 하위 집합인지가 인쇄돼 있지 않다.
- **크기 제약의 언어별 집행 정도가 다르다고만 적고 어디가 어떤지는 적지 않는다.**
- **불안정을 실제로 어떻게 잡는지가 없다.** `We fight hard`와 `actively investing
  engineering hours` 외에 절차·도구·판정 기준이 이 책에 없다.
- **재실행 완화의 경계가 정량으로 그어져 있지 않다.** `At low levels of flakiness`가 얼마인지
  적혀 있지 않다.

## 이어지는 페이지

- [단위 테스트는 대부분 낭비인가](unit-testing-as-waste.md) — **`contradicts` 상대 극.**
  같은 물음("단위 테스트를 얼마나 둘 것인가")에 정반대로 답한 2014년의 실무자 에세이. 위
  [반대 극과 무엇이 부딪히는가](#반대-극과-무엇이-부딪히는가)의 표가 그 대조를 소유하고,
  그쪽 페이지는 그 주장의 논거 넷과 그것들이 어디서 무너지는지를 소유한다
- [종단 테스트를 왜 줄이는가](why-fewer-end-to-end-tests.md) — 같은 회사가 다섯 해 앞서 낸
  70/20/10과 그 배합을 고르는 논거. 이 페이지가 "얼마나"의 문면을 소유하고 그쪽이 "왜 그
  방향인가"를 소유한다. `entirely`라는 낱말로 불안정이 사라진다고 적은 2015년 글의 주장이
  이 페이지의 0.15%와 겹쳐 읽히는 자리이기도 하다
- [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md) —
  이 페이지가 불안정의 **비율과 조직 대응**을 소유한다면 그쪽은 **원인과 고침**을 소유한다.
  이 책이 수치 없이 권하는 것들(잠자기 대신 폴링, 격리)이 그쪽에서 고침 커밋의 분포로 선다
- [테스트 대역 선호 순서와 규모 전제](test-double-preference-at-scale.md) — 같은 책 13장.
  small의 제약을 만족시키려면 대역이 필요한데 무엇을 고를 것인가가 그쪽 질문이다
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 같은 회사가
  커버리지를 어떻게 운용하라고 적었는가. 11장의 커버리지 문단과 저자가 겹친다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 다섯 번
  실행에서 매번 통과해야 한다는 불안정 판정을 실제 관문의 조건으로 쓴 산업 배선
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 같은 회사의
  다른 규범 글이 `change-detector test`라는 이름을 붙인 자리
- [테스트 스위트의 운영](../synthesis/test-suite-operations.md) — 이 갈래의 허브. 크기의
  배합과 비결정성을 한 질문으로 묶는 자리이고, 이 페이지가 그 어휘의 바닥이다
- [테스트 스위트의 적절성](../synthesis/test-suite-adequacy.md) — 형제 허브. 스위트를 하나의
  덩어리로 놓고 그 적절성을 재는 쪽
- [테스팅에서 자동화의 경계](../synthesis/automation-boundary-in-testing.md) — 형제 허브.
  11장이 자동화가 맞지 않는 자리로 든 것들(검색 품질 평가·음성과 영상 품질·탐색적 테스팅)이
  그 축에 닿는다

[^winters2020-swe-at-google]: Winters, Manshreck & Wright(큐레이터) 2020,
    *Software Engineering at Google*, abseil.io 공개판(CC BY-NC-ND 4.0), 2026-08-23
    열람본. 인용한 장은 11장 `Testing Overview`(저자 Adam Bender) · 12장
    `Unit Testing`(저자 Erik Kuefler) · 14장 `Larger Testing`(저자 Joseph Graves)이다.
    **공개판 HTML에 쪽 번호가 없어 locator는 장 번호와 원문 절 제목이다.** 직인용은 원문
    표기 그대로이고 말줄임표(…)만 이 페이지가 넣었다. 근거 등급·규모 전제·인용 규약은
    [소스 메타](../sources/winters2020-swe-at-google.md)가 정본이다.

[^stewart2010-test-sizes]: Stewart 2010, "Test Sizes", *Google Testing Blog*,
    2010년 12월 13일 게시, 2026-08-23 열람본. 표는 본문의 표를 열과 행 그대로 옮긴 것이고
    행 이름과 값은 원문 표기다. 확보본에 함께 든 독자 댓글은 저자의 글이 아니므로 인용하지
    않았다.

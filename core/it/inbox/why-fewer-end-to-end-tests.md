---
type: concept
title: 종단 테스트를 왜 줄이는가
description: 테스트의 값어치를 실패 검출이 아니라 버그 수정으로 재고 좋은 피드백 루프의 성질 셋으로 크기를 고르는 2015년 구글 블로그의 논거 — 실패한 테스트는 사용자에게 이롭지 않다는 출발점, 빠름과 신뢰와 실패 위치 지목이라는 세 성질, 종단 테스트가 그 셋을 잃는 자리, 지어낸 사례라고 저자가 밝힌 날짜별 통과율 표, 제안의 문법으로 적힌 70/20/10과 같은 회사 2020년 책의 80/15/5와의 차이, 이 글에 없는 낱말, 그리고 판정자가 에이전트로 바뀐 뒤 반복 실패율을 분모와 함께 잰 산업 자기 보고
status: draft
generated: { by: "claude-opus-5", at: "2026-08-23T18:00:00Z" }
sources:
  - { id: wacker2015-e2e, resource: /it/sources/wacker2015-e2e.md }
  - { id: gorbachov2026-agentic-testing, resource: /it/sources/gorbachov2026-agentic-testing.md }
---

# 종단 테스트를 왜 줄이는가

- [두 소스의 지위](#두-소스의-지위)
- [값어치는 버그 수정에 있다](#값어치는-버그-수정에-있다)
- [좋은 피드백 루프의 성질 셋](#좋은-피드백-루프의-성질-셋)
- [단위 테스트가 셋을 얻고 종단이 셋을 잃는다](#단위-테스트가-셋을-얻고-종단이-셋을-잃는다)
- [지어낸 사례 하나](#지어낸-사례-하나)
- [통합 테스트가 종단을 대신하는 자리](#통합-테스트가-종단을-대신하는-자리)
- [배합 수치와 그 문법](#배합-수치와-그-문법)
- [같은 회사의 두 수치](#같은-회사의-두-수치)
- [종단 테스트에 남는 몫](#종단-테스트에-남는-몫)
- [판정자가 에이전트가 된 뒤](#판정자가-에이전트가-된-뒤)
- [두 소스의 사각](#두-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **종단(end-to-end) 테스트를 주력으로 삼는 전략은 왜 실패하며, 그 판단을
무엇으로 재는가.** 형제 페이지
[구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)이
"어떤 크기를 얼마나 둘 것인가"에 답한다면, 이 페이지는 그 배합을 정하는 **기준 자체**를
다룬다 — 테스트의 값어치를 무엇으로 재면 종단 테스트가 아래로 내려가는가.

## 두 소스의 지위

- **둘 다 근거 등급이 `industry-norm`이다.** 통제도 심사도 없다. 이 페이지가 옮기는 것은
  "이 논거가 이런 문면으로 적혀 있다"는 사실이지 그 논거가 옳다는 증명이 아니다.
- **2015년 글은 블로그 한 편이고 그 안의 사례는 지어낸 것이다.** 저자가 스스로 그렇게
  적는다(아래 [지어낸 사례 하나](#지어낸-사례-하나)). 이 글에는 잰 값이 하나도 없다.
- **2026년 글은 한 회사의 자기 보고다.** 실험 대상도 계측 도구도 같은 회사 안에 있다.
  그러나 분모와 회차를 적었으므로 이 KB는 그것을 방향의 뒷받침으로 쓴다.
- **규모 전제가 두 글에 다 깔려 있다.** 2015년 글의 이야기는 야간 빌드·전용 테스트 환경·
  협력 팀·실험실 하드웨어가 이미 있다는 조건에서 진행되고, 2026년 실험은 사내 테스트 작업
  공간과 사내 계측 위에서 돌았다. 그 인프라가 없는 곳에 조문만 옮길 수 없다.

## 값어치는 버그 수정에 있다

**이 글의 논법이 여기서 시작한다** (§"The True Value of Tests").[^wacker2015-e2e] 종단
테스트를 반대하는 이유를 결함 검출 능력으로 대지 않고, **무엇이 사용자에게 이로운가**를
먼저 물어 답을 뒤집는다.

> A failing test does not directly benefit the user.

> A bug fix directly benefits the user.

- **이유는 같은 절에 적혀 있다** (§"The True Value of Tests").[^wacker2015-e2e]

  > If a product works, it works, whether a test says it works or not. If a product is
  > broken, it is broken, whether a test says it is broken or not.

- **그래서 값어치가 붙는 자리가 마지막 한 칸뿐이라고 표로 못 박는다** (§"The True Value of
  Tests" 표).[^wacker2015-e2e]

  | 단계 | Failing Test | Bug Opened | Bug Fixed |
  |---|---|---|---|
  | Value Added | No | No | Yes |

- **귀결이 이 페이지 전체의 판정 기준이다** (같은 절):[^wacker2015-e2e]

  > Thus, to evaluate any testing strategy, you cannot just evaluate how it finds bugs. You
  > also must evaluate how it enables developers to fix (and even prevent) bugs.

  **테스터의 일이 실패한 테스트에서 끝난다는 통념을 이 문장이 거부한다** — 같은 절이
  `Typically, a tester's job ends once they have a failing test`라고 그 통념을 먼저 적어
  두고 그것을 넘어서자고 말한다.

## 좋은 피드백 루프의 성질 셋

**앞 절의 기준을 실행 가능한 형태로 바꾼 것이 이 셋이다** (§"Building the Right Feedback
Loop").[^wacker2015-e2e] 테스트는 제품이 도는지를 개발자에게 알리는 피드백 루프(feedback
loop)이고, 이상적인 루프에는 성질이 여럿 있다고 적으며 셋을 든다.

- **빠르다** — `No developer wants to wait hours or days to find out if their change works.`
  (§"Building the Right Feedback Loop")[^wacker2015-e2e] 고치는 일은 한 번에 끝나지 않으므로
  루프가 여러 번 돌아야 하고, 충분히 빠르면 개발자가 변경을 넣기 전에 돌리게 된다고 적는다.
- **믿을 만하다** — 불안정(flaky) 테스트를 여기서 다룬다
  (§"Building the Right Feedback Loop").[^wacker2015-e2e]

  > Flaky tests reduce the developer's trust in the test, and as a result flaky tests are
  > often ignored, even when they find real product issues.

  **이 글은 불안정이 왜 생기는지도 어떻게 고치는지도 적지 않는다.** 그 자리를 채우는 심사
  실증이 [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md)
  이다 — 고침 커밋 201건을 정독해 원인을 열 범주로 나누고, 범주마다 어떤 고침이 불안정을
  실제로 없앴는지를 센다. **이 글이 무시된다고 적은 그 테스트들이 프로덕션 코드의 버그를
  드러내기도 한다는 것도 그쪽 실증이 세어 놓았다.**

- **실패를 좁혀 준다** — 이 페이지에서 가장 많이 인용될 자리다
  (§"Building the Right Feedback Loop").[^wacker2015-e2e]

  > It isolates failures. To fix a bug, developers need to find the specific lines of code
  > causing the bug. When a product contains millions of lines of codes, and the bug could
  > be anywhere, it's like trying to find a needle in a haystack.

  **`isolates failures`를 이 KB는 "실패의 위치를 지목한다"로 옮긴다.** 원어를 남기는 이유는
  "격리"로 옮기면 테스트끼리의 격리(isolation)와 섞이기 때문이다 — 여기서 좁혀지는 것은
  테스트가 아니라 **버그가 있을 수 있는 코드의 범위**다.

## 단위 테스트가 셋을 얻고 종단이 셋을 잃는다

**앞 절의 셋을 잣대로 놓으면 답이 크기 쪽으로 기운다** (§"Think Smaller, Not
Larger").[^wacker2015-e2e] 글의 처방 한 줄이 `By thinking smaller, not larger`다.

- **빠름** — `In fact, one tenth of a second is considered slow for unit tests.`
  (§"Unit Tests")[^wacker2015-e2e] **이 값은 측정이 아니라 사내 감각의 진술이고 분모가 없다.**
- **신뢰** — 단순한 시스템과 작은 단위는 불안정을 훨씬 덜 겪는다고 적고, 한 걸음 더 나간다
  (§"Unit Tests").[^wacker2015-e2e]

  > best practices for unit testing - in particular practices related to hermetic tests -
  > will remove flakiness entirely.

  **`entirely`는 근거 없이 놓인 낱말이다.** 밀폐(hermetic) 테스트로 비결정성이 완전히
  사라진다는 주장에 이 글은 아무 값도 붙이지 않는다. 아래
  [두 소스의 사각](#두-소스의-사각)에서 다시 든다.
- **위치 지목** — `if a unit test fails, you only need to search that small unit under test
  to find the bug` (§"Unit Tests").[^wacker2015-e2e]
- **종단 쪽은 반대다** (§"Unit Tests vs. End-to-End Tests").[^wacker2015-e2e] 제품 전체를
  빌드하고 배포하고 모든 종단 테스트가 돌기를 기다려야 하며, 돌기 시작하면 불안정 테스트가
  일상이 되고, 버그를 찾아도 그것이 제품 어디에나 있을 수 있다.
- **비교 표를 글이 직접 놓는다** (§"Unit Tests vs. End-to-End Tests" 표).[^wacker2015-e2e]
  **표의 칸은 글자가 아니라 그림이다** — 웃는 얼굴(`happy.png`)과 찡그린 얼굴(`sad.png`)
  두 이미지가 놓여 있고, 아래 표는 그 그림을 읽어 옮긴 것이다.

  | 성질 | Unit | End-to-End |
  |---|---|---|
  | Fast | 웃음 | 찡그림 |
  | Reliable | 웃음 | 찡그림 |
  | Isolates Failures | 웃음 | 찡그림 |
  | Simulates a Real User | 찡그림 | 웃음 |

- **넷 중 셋을 잃고 하나를 얻는 교환이라는 것이 이 표의 요지다** (같은 절):[^wacker2015-e2e]

  > Although end-to-end tests do a better job of simulating real user scenarios, this
  > advantage quickly becomes outweighed by all the disadvantages of the end-to-end
  > feedback loop

## 지어낸 사례 하나

**이 절의 숫자는 전부 예시다. 저자가 스스로 그렇게 적는다** (§"End-to-End Tests in
Practice"):[^wacker2015-e2e]

> To demonstrate, I present the following composite sketch based on a collection of real
> experiences familiar to both myself and other testers.

**`composite sketch`는 여러 경험을 합쳐 지어낸 이야기라는 뜻이고, 이야기 속 팀은 온라인
문서 편집 서비스를 만든다.** 밤마다 빌드하고 테스트 환경에 배포하고 종단 테스트를 전부
돌려 결과 요약을 메일로 보내는 인프라가 이미 있다는 설정이며, 팀은 기능 완료의 조건으로
종단 테스트 90% 이상 통과를 요구한다.

| Days Left | Pass % | 무슨 일이 있었나 |
|---|---|---|
| 1 | 5% | 로그인이 깨졌다. 거의 모든 테스트가 로그인을 하므로 거의 전부 실패했다 |
| 0 | 4% | 의존하는 협력 팀이 자기 테스트 환경에 나쁜 빌드를 올렸다 |
| -1 | 54% | 누군가 저장 시나리오를 깨뜨렸다. 절반이 저장을 거친다. 앞단인지 뒷단인지 가리는 데 하루의 대부분을 썼다 |
| -2 | 54% | 앞단 버그였다. 어디인지 찾는 데 오늘의 절반을 썼다 |
| -3 | 54% | 어제 잘못된 수정이 들어갔다. 실수는 눈에 띄어 오늘 옳은 수정이 들어갔다 |
| -4 | 1% | 테스트 환경 실험실에서 하드웨어 고장이 났다 |
| -5 | 84% | 큰 버그 뒤에 작은 버그가 여럿 숨어 있었다 |
| -6 | 87% | 90%를 넘겨야 하는데 이유를 모르겠다 |
| -7 | 89.54% | 어제 들어간 수정이 없으니 어제 테스트가 불안정했던 것이 틀림없다 |

- **표를 읽는 법**: `Days Left`는 마감까지 남은 날이라 음수는 마감을 넘긴 날수다. `Pass %`는
  종단 테스트 통과 비율이고, **분모는 그 팀의 종단 테스트 전체라고만 적혀 있고 개수는
  없다.** 마지막 줄의 89.54%에는 `(Rounds up to 90%, close enough.)`가 붙어 있다.
- **글이 이 사례에서 뽑는 결론 목록** (§"Analysis").[^wacker2015-e2e] 잘된 것은 하나다 —
  고객에게 닿기 전에 버그를 잡았다. 잘못된 것은 여섯이다: 마일스톤이 한 주 늦었고,
  실패한 종단 테스트의 근본 원인을 찾는 일이 괴롭고 오래 걸리며, 협력 팀과 실험실의 고장이
  여러 날의 결과를 망쳤고, 작은 버그가 큰 버그 뒤에 숨었으며, 종단 테스트가 때때로
  불안정했고, 개발자가 수정이 통했는지 알려면 다음 날까지 기다려야 했다.
- **이 여섯이 앞 절의 성질 셋과 하나씩 맞물린다** — 기다림은 빠름, 불안정과 남의 환경 고장은
  신뢰, 앞단인지 뒷단인지 가리는 데 쓴 하루와 숨은 작은 버그는 위치 지목이다. #hypothesis
  이 맞물림은 글이 표로 정리한 것이 아니라 이 페이지가 두 절을 겹쳐 읽은 것이다.

## 통합 테스트가 종단을 대신하는 자리

**"작게 생각하라"의 반론을 글이 스스로 먼저 놓는다** (§"Integration
Tests").[^wacker2015-e2e] 단위 테스트의 큰 약점 하나는 단위들이 따로는 잘 돌아도 함께 잘
도는지를 모른다는 것이다. 글의 답은 종단이 아니라 통합 테스트(integration test)다.

- **통합 테스트의 정의를 크기로 적는다** — `An integration test takes a small group of
  units, often two units, and tests their behavior as a whole`
  (§"Integration Tests").[^wacker2015-e2e]
- **선택의 근거는 같은 버그를 더 작은 테스트로 잡을 수 있다는 것이다**
  (§"Integration Tests"):[^wacker2015-e2e]

  > If two units do not integrate properly, why write an end-to-end test when you can write
  > a much smaller, more focused integration test that will detect the same bug?

- **크게 생각하되 조금만 크게 생각하라는 것이 이 절의 한 줄이다** —
  `While you do need to think larger, you only need to think a little larger`
  (§"Integration Tests").[^wacker2015-e2e]

## 배합 수치와 그 문법

**이 글에서 가장 많이 인용되고 가장 자주 지위가 지워지는 자리다** (§"Testing
Pyramid").[^wacker2015-e2e]

> As a good first guess, Google often suggests a 70/20/10 split: 70% unit tests, 20%
> integration tests, and 10% end-to-end tests.

- **`suggests`와 `good first guess`가 이 문장의 지위다.** 제안의 문법이지 관측의 문법이
  아니고, **이 글에 그 배합을 잰 값은 없다.**
- **바로 다음 문장이 다른 배합을 허용한다** — `The exact mix will be different for each team,
  but in general, it should retain that pyramid shape.`
  (§"Testing Pyramid")[^wacker2015-e2e]
- **집계 단위가 적혀 있지 않다.** 테스트 케이스 수인지 실행 시간인지 코드 줄 수인지 이 글은
  말하지 않는다. **이 값을 옮길 때 분모를 지어내지 않는다.**
- **피라미드 그림의 출처를 글이 밝힌다** — `a simplified version of the testing pyramid from
  the opening keynote of the 2014 Google Test Automation Conference`
  (§"Testing Pyramid").[^wacker2015-e2e] 확보본에서 그림은
  원격 주소로만 남았고 `alt` 텍스트가 없어 **그림 안의 글자는 문면으로 확인되지 않는다.**
  이 페이지는 산문에 적힌 70/20/10만 옮긴다.
- **배격하는 배합 둘에 이름이 붙어 있다** (같은 절):[^wacker2015-e2e]
  - `Inverted pyramid/ice cream cone` — 종단 테스트에 주로 기대고 통합은 적고 단위는 더 적다.
  - `Hourglass` — 단위 테스트로 많이 시작한 다음 통합 테스트를 써야 할 자리에 종단 테스트를
    쓴다. 아래위가 두껍고 가운데가 얇다.
  - **이 두 이름이 2020년 책보다 5년 앞선다.** 같은 두 이름이
    [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)이
    옮긴 2020년 책 11장에도 나온다. 어휘의 계보가 이 글 쪽이다.

## 같은 회사의 두 수치

**같은 회사가 다섯 해 사이에 다른 배합을 냈다.** 이 KB는 둘을 모순으로 두지 않는다 —
둘 다 측정이 아니라 제안이기 때문이다. 대신 무엇이 다른지를 적어 둔다.

| 항목 | 2015년 이 글 | 2020년 책 11장 |
|---|---|---|
| 배합 | 70 / 20 / 10 | 80 / 15 / 5 |
| 어조 | `suggests`, `good first guess` | `As a very rough guideline`, `we tend to aim` |
| 집계 단위 | 적혀 있지 않다 | 테스트 케이스 수(그림 캡션) |
| 피라미드 출처 | 2014년 `Google Test Automation Conference` 기조 강연 | Mike Cohn, *Succeeding with Agile*(2009) |
| 배격하는 배합 | ice cream cone, hourglass | 같은 두 이름 |

- **둘을 겹쳐 읽을 때의 주의**: 두 값 다 회사가 정한 목표치이므로 "구글은 단위 테스트를
  70%로 유지한다"도 "80%로 유지한다"도 원문이 하지 않은 주장이다. 두 값이 다르다는 사실
  자체가 이 수치들의 지위를 드러낸다 — **잰 값이면 다섯 해 사이에 이렇게 움직여도 어느 쪽이
  틀렸다고 말할 수 있어야 하는데, 어느 글도 그런 말을 하지 않는다.**
- **비중 논쟁에서 이 페이지가 서는 자리**: 형제 페이지가 "얼마나"의 문면을 소유하고, 이
  페이지는 "왜 그 방향인가"의 논거를 소유한다. 수치를 인용하려면 형제 페이지로 가고,
  논거를 인용하려면 여기로 온다.

## 종단 테스트에 남는 몫

**글이 종단 테스트를 없애자고 하지 않는다** (§"Testing Pyramid"):[^wacker2015-e2e]

> Even with both unit tests and integration tests, you probably still will want a small
> number of end-to-end tests to verify the system as a whole.

- **남기는 기준은 "적은 수"와 "시스템 전체 검증"이다.** 그 이상은 이 글에 없다.
- **`critical user journey`라는 낱말은 이 글에 없다.** 본문을 전수 대조했고
  `critical`·`journey` 둘 다 한 번도 나오지 않는다. "핵심 사용자 여정만 종단으로 남긴다"는
  정식화는 널리 퍼져 있으나 **이 글에 귀속시킬 수 없다.** 이 글에서 나오는 것은 수의 제한과
  검증 대상의 범위뿐이고, 어느 시나리오를 고를 것인가의 기준은 적혀 있지 않다.
- **여정을 어떻게 다룰지는 다른 문헌이 채운다** — 2020년 책 14장이 사용자 여정을 여러
  개의 짝 통합 테스트로 이어 붙이는 방법을 든다(형제 페이지의 "큰 테스트도 작을수록 낫다"
  절). **이 글과 그 책을 한 문장으로 합치지 않는다.**

## 판정자가 에이전트가 된 뒤

**이 글의 시대 지위**: 2015년의 휴리스틱이고, 원문부터 제안 어조다. 그러나 이 논거가
언어 모델 시대에 약해지는 것이 아니라 오히려 한 방향으로 강해질 수 있다.

- #hypothesis **종단 테스트의 불안정 신호는 에이전트의 검증 루프를 오염시키므로, 결정적인
  아래층을 먼저 두라는 이 글의 논거가 오히려 강화된다.** 근거의 얼개는 이 글 자신의 문장
  하나다 — 불안정한 테스트는 신뢰를 깎고 무시된다(위
  [좋은 피드백 루프의 성질 셋](#좋은-피드백-루프의-성질-셋)). 판정자가 사람이면 무시라는
  선택지가 있지만, 판정자가 에이전트이고 그 판정이 다음 수정을 몰면 불안정한 신호가 무시
  대신 **잘못된 수정**으로 이어진다. **이것은 이 KB의 읽기이지 어느 소스의 주장이 아니다.**
- **그 방향을 뒷받침하는 산업 자기 보고가 하나 있다.** 한 회사가 에이전트에게 종단 흐름을
  직접 몰게 하고 반복 실패율을 쟀다 (§3 `Summary of Results` 표).[^gorbachov2026-agentic-testing]
  - 버전 조건: Claude Sonnet 4.5(에이전트)와 Claude Opus 4.6(테스트 생성), Playwright
    MCP와 Playwright CLI, 비대화식 Claude Code를 쓴 2026년 6월 실행에 한한다.

  | 방식 | 실패율 (쉬운 흐름) | 실패율 (어려운 흐름) | 평균 소요 |
  |---|---|---|---|
  | Agent + Playwright MCP | 0% | ~12% | ~5~8분 |
  | Agent + Playwright CLI | ~12% | ~20% | ~9~11분 |
  | 생성된 Playwright 테스트 | ~8% | ~48% | ~3분 |

  - **단위와 분모**: 실패율은 실행 회차 기준 비율(원값)이고, 구성 하나당 **20회**씩 돌렸다
    (§2 `Experiment Matrix`). 전체 실행은 200회를 넘는다. 두 열은 오차 범위가 아니라
    **난이도가 다른 두 흐름**의 값이다 — 쉬운 쪽이 단계 15~20개짜리 스레드 답글, 어려운
    쪽이 단계 25~30개짜리 검색 탐색이다 (§2 `Test flows`).
  - **이 글의 판정은 "복잡해질수록 격차가 벌어진다"이다** (§3 `Reliability`) —
    `the reliability gap widened with increasing complexity`. 생성된 테스트가 어려운
    흐름에서 무너지는 방식도 적어 둔다: 대개 흐름의 70~80%까지 진행한 뒤 마지막 상호작용이나
    단언에서 깨졌고, 원인은 화면 상태의 변동과 추상화의 어긋남이었다.
  - **경로가 매번 달랐다** (§3 `Adaptability`) — 같은 행동 순서를 그대로 따른 실행이 약
    20%뿐이었다. 나머지는 같은 목표에 다른 경로로 닿았다. **결정적 테스트가 하나의 여정을
    강제하는 것과 갈리는 자리가 여기다.**
  - **비용이 크다** (§3 `Cost and Where It Comes From`) — 실행당 15~30달러다. 저자의
    결론은 지금으로서는 높은 빈도의 지속 통합보다 표적 디버깅이나 탐색적 테스팅에 더 맞다는
    쪽이다.
  - **저자가 대체를 주장하지 않는다** (§4) — `Rather than replacing existing approaches, it
    adds a new capability on top of them.` 층 넷짜리 피라미드의 맨 위에 에이전트 층을 얹는
    그림이다.
- **여기가 진짜 공백이다.** 위 수치는 **실패율**이고, 에이전트 검증 루프의 **거짓 통과와
  거짓 실패**가 얼마인지를 잰 학술 실증을 이 KB는 아직 갖고 있지 않다. 통과한 회차가 실제로
  옳게 통과했는지를 따로 판정한 절차가 저 실험에도 없다. **그 값이 없는 채로 "에이전트가
  종단 테스트를 대신할 수 있다"고 말할 수 없다.**

## 두 소스의 사각

- **2015년 글에 잰 값이 하나도 없다.** 날짜별 통과율 표는 지어낸 사례이고, 70/20/10은
  제안이며, `one tenth of a second`는 감각의 진술이다.
- **`will remove flakiness entirely`에 근거가 없다.** 밀폐 테스트로 불안정이 완전히
  사라진다는 주장인데, 같은 회사의 2020년 책은 사내 불안정 비율을 0으로 적지 않는다
  (형제 페이지의 불안정 절). **두 문헌을 겹쳐 읽으면 이 `entirely`가 서지 않는다.**
- **어느 종단 테스트를 남길 것인가의 기준이 없다.** 수를 줄이라고만 하고 고르는 법을
  주지 않는다.
- **통합 테스트로 종단을 대신할 수 있는 경계가 없다.** 두 단위의 계약 어긋남은 통합
  테스트가 잡지만, 배포·설정·부하처럼 통합 테스트에도 안 잡히는 자리가 있다는 서술이 이
  글에 없다. 2020년 책 14장이 그 목록을 채운다.
- **2026년 실험은 한 회사의 한 제품이다.** 화면·모델·도구·흐름이 전부 그 실험의 것이고,
  심사도 재현 자료도 없다.
- **거짓 통과와 거짓 실패의 실증이 어느 쪽에도 없다.** 위 절의 마지막 항목이 그 자리다.

## 이어지는 페이지

- [구글의 테스트 크기 어휘와 스위트 운영](../concepts/google-test-sizes-and-suite-operations.md)
  — 같은 회사가 다섯 해 뒤에 낸 크기 어휘와 80/15/5. **수치를 인용하려면 그쪽으로 간다**
- [불안정 테스트의 원인 분류와 고침](../concepts/flaky-test-root-causes-and-fixes.md) —
  이 글이 성질 셋 가운데 "믿을 만하다"로만 적고 지나간 자리. **불안정이 무엇 때문에
  생기고 무엇으로 없어지는가**를 고침 커밋의 분포로 센 심사 실증이고, 이 글의
  `will remove flakiness entirely`가 서지 않는 이유를 잠자기 고침 20건의 결과가 보인다
- [테스트 대역 선호 순서와 규모 전제](../concepts/test-double-preference-at-scale.md) —
  이 글이 "작게 생각하라"로 요구한 것을 실제로 하려면 무엇을 대역으로 세울 것인가
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 다섯 번
  실행에서 매번 통과해야 한다는 불안정 판정을 실제 관문의 조건으로 쓴 산업 배선. 이 글의
  "믿을 만하다"가 관문의 문장으로 번역된 자리다
- [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md)
  — 판정자가 에이전트일 때 누가 채점해야 하는가. 위
  [판정자가 에이전트가 된 뒤](#판정자가-에이전트가-된-뒤)와 같은 축이다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  종단 테스트를 줄이고 남은 스위트가 전부 통과했을 때 그것이 무엇을 증명하지 않는가의 상한
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 같은 회사가
  커버리지를 어떻게 운용하라고 적었는가. 종단 테스트의 커버리지를 집계에서 빼라는 권고가
  이 글의 방향과 만난다

[^wacker2015-e2e]: Wacker 2015, "Just Say No to More End-to-End Tests",
    *Google Testing Blog*, 2015년 4월 22일 게시, 2026-08-23 열람본. **블로그 글이라 쪽
    번호가 없어 locator는 원문 절 제목이다.** 직인용은 원문 표기 그대로이고 줄바꿈만 이
    페이지가 맞췄다. 본문의 두 그림은 확보본에 원격 주소로만 남아 있고 피라미드 그림에는
    `alt` 텍스트가 없어 그림 안의 글자를 인용하지 않았다. 비교 표의 칸은 웃는 얼굴·찡그린
    얼굴 그림이고 이 페이지가 그것을 낱말로 옮겼다. 확보본에 함께 든 독자 댓글 84건은
    저자의 글이 아니므로 인용하지 않았다. 근거 등급과 인용 규약은
    [소스 메타](../sources/wacker2015-e2e.md)가 정본이다.

[^gorbachov2026-agentic-testing]: Gorbachov 2026, "Agentic Testing: Where Agents Fit in
    the E2E Testing Stack", *Engineering at Slack*, 2026년 6월 11일 게시, 2026-08-23
    열람본. **블로그 글이라 쪽 번호가 없어 locator는 원문 절 번호와 절 제목이다.** 이
    소스는 한 회사가 자기 제품 위에서 자기 계측으로 낸 값이라 심사 실증이 아니다.
    실험 설계와 인용 한계는 [소스 메타](../sources/gorbachov2026-agentic-testing.md)가
    정본이다.

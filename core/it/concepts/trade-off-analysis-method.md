---
type: concept
title: 트레이드오프 분석 방법
description: 아키텍트가 자기 아키텍처에 맞는 절충 분석을 스스로 짓는 세 걸음 — 얽힌 차원 찾기와 결합 지점 분석과 절충 평가, 결합을 "X를 바꾸면 Y도 바뀌어야 하는가"로 가장 단순하게 규정하는 작업 정의와 정적 결합 다이어그램을 짓는 데 모을 다섯 가지와 워크플로 결합만 있는 퀀텀을 빼는 조건, 이 책 자신이 수백 사례를 훑어 통신·일관성·조율 셋을 고른 경위와 채점 축 넷, 여덟 칸 비교 행렬에서 읽어 낸 상관 둘, 근본 차원을 먼저 고정하면 남는 것은 설계라는 판정, 그리고 기법 여섯 — 아키텍처에는 참된 정량 비교가 드물다는 정성 분석 권고, 비교 대상을 겹치지도 빠뜨리지도 않게 맞추는 MECE 목록, 일반 절충표가 맥락을 만나면 결론이 뒤집히는 맥락 밖 함정, 도메인 시나리오를 모형화해 진짜 절충을 드러내는 법, 기술 세부로 비기술 이해관계자를 익사시키지 말고 결론만 내놓으라는 조문, 그리고 전도를 피하고 절충의 객관적 중재자가 되라는 경고와 모노레포 일화, 부록 C가 이 책의 절충 표를 색인하는 장치와 그 색인을 이 KB의 페이지에 맞댄 표, 그리고 테스트가 소프트웨어 개발의 공학적 엄밀성이라는 에필로그의 닫는 주장
generated: { by: "claude-opus-5", at: "2026-09-18T12:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: evans2003, resource: /it/sources/evans2003.md }
  - { id: beck2023, resource: /it/sources/beck2023.md }
  - { id: ousterhout2021, resource: /it/sources/ousterhout2021.md }
  - { id: khononov2021, resource: /it/sources/khononov2021.md }
---

# 트레이드오프 분석 방법

- [이 방법이 무엇인가 — 세 걸음](#이-방법이-무엇인가--세-걸음)
- [걸음 하나 — 얽힌 차원 찾기](#걸음-하나--얽힌-차원-찾기)
  - [결합을 무엇으로 보는가](#결합을-무엇으로-보는가)
  - [정적 결합 다이어그램을 무엇으로 짓는가](#정적-결합-다이어그램을-무엇으로-짓는가)
  - [이 책이 세 차원을 고른 경위](#이-책이-세-차원을-고른-경위)
- [걸음 둘 — 결합 지점 분석](#걸음-둘--결합-지점-분석)
- [걸음 셋 — 절충 평가](#걸음-셋--절충-평가)
- [기법 여섯](#기법-여섯)
  - [하나 — 정성 분석 대 정량 분석](#하나--정성-분석-대-정량-분석)
  - [둘 — MECE 목록](#둘--mece-목록)
  - [셋 — 맥락 밖 함정](#셋--맥락-밖-함정)
  - [넷 — 관련 도메인 사례를 모형화하라](#넷--관련-도메인-사례를-모형화하라)
  - [다섯 — 압도적 증거보다 결론](#다섯--압도적-증거보다-결론)
  - [여섯 — 뱀 기름과 전도를 피하기](#여섯--뱀-기름과-전도를-피하기)
- [부록 C — 이 책이 자기 절충 표를 색인한다](#부록-c--이-책이-자기-절충-표를-색인한다)
- [에필로그가 남기는 주장](#에필로그가-남기는-주장)
- [다른 소스의 결정 어림과 나란히](#다른-소스의-결정-어림과-나란히)
- [이어지는 페이지](#이어지는-페이지)

## 이 방법이 무엇인가 — 세 걸음

**이 책의 마지막 장이 앞 열네 장에서 쓴 방법 자체를 독자에게 넘긴다.** 결론이 아니라 결론을
만든 절차가 이 장의 내용이다.

- **장이 자기 이유를 먼저 적는다** — 이 책 전체의 통합 예제가 분산 아키텍처에서 절충 분석을
  **일반적으로** 수행하는 법을 보이지만, **아키텍처에 일반 해법은 거의 없고 있더라도 고도로
  특수한 아키텍처와 그것이 가져오는 고유한 문제에는 대체로 불완전하다.** 그래서 저자들은
  2장이 다룬 통신 분석이 **망라적이라고 보지 않고 출발점으로 본다** — 독자가 자기 문제 공간에
  얽힌 고유한 요소를 위해 **열을 더 붙이라는 것**이다 (15장, p.400).[^ford2021-hard-parts]
- **2021년 저술 시점 절충 분석의 세 걸음** (15장, p.400):[^ford2021-hard-parts]

  > - Find what parts are entangled together.
  > - Analyze how they are coupled to one another.
  > - Assess trade-offs by determining the impact of change to interdependent systems.

  - 저자들이 이 셋을 **2장에서 이미 소개했다**고 적는다 (15장, p.400).[^ford2021-hard-parts]
- **2장이 같은 셋을 처음 내놓는 자리** (2장, p.27):[^ford2021-hard-parts]
  1. **어느 부분들이 서로 얽혀 있는지 찾는다.**
  2. **그것들이 서로 어떻게 결합돼 있는지 분석한다.**
  3. **상호 의존하는 체계에 변화가 주는 영향을 판정해 절충을 평가한다.**
  - **걸음은 단순하고 어려운 것은 세부에 숨어 있다**고 저자들이 덧붙이며, 그 방법 자체를 스스로
    짓는 일은 15장 §"Build Your Own Trade-Off Analysis"로 넘긴다 (2장,
    p.27).[^ford2021-hard-parts] **이 페이지가 그 15장이다.**
  - **첫 걸음의 이유가 적힌다** — 얽힌 문제를 볼 때 아키텍트가 절충 분석에 애를 먹는 것은
    **관심사를 갈라 따로 볼 수 없기 때문**이고, 그래서 **절충 분석의 첫 걸음이 문제의 차원들을
    푸는 것**이다 (2장, p.27).[^ford2021-hard-parts] 저자들이 도판으로 드는 비유는 **머리카락을
    땋은 가닥(braid)** — 땋으면 개별 가닥을 알아보기 어려워진다 (2장,
    p.27).[^ford2021-hard-parts] 15장이 같은 낱말을 되쓴다(아래
    [걸음 하나](#걸음-하나--얽힌-차원-찾기)).
  - 이 세 걸음이 봉사하는 규정 — **아키텍트의 일은 최선의 설계를 찾는 것이 아니라 가장 덜 나쁜
    절충 조합을 찾는 것**이라는 문장은
    [진화적 아키텍트의 역할](../concepts/evolutionary-architect-role.md)에
    있다.
  - **이 장의 구조가 그 세 걸음을 그대로 따르지는 않는다.** 목차에서 §"Finding Entangled
    Dimensions" 아래에 §"Coupling"·§"Analyze Coupling Points"·§"Assess Trade-Offs" 셋이 하위
    절로 들어가 있어, **걸음 둘과 셋이 걸음 하나의 아래 층에 놓인다**
    (15장, pp.401–404).[^ford2021-hard-parts] 저자들이 그 어긋남을 적지 않는다. #hypothesis
    이 페이지는 세 걸음을 같은 층으로 펴서 적는다.

## 걸음 하나 — 얽힌 차원 찾기

- **첫 걸음은 어떤 차원들이 얽혀 있는지, 곧 땋여 있는지(entangled, or braided) 찾는 것**이다.
  그것은 **특정 아키텍처마다 고유하되**, 기존 생태계와 그 능력과 제약에 익숙한 **경험 있는
  개발자·아키텍트·운영 담당자와 그 밖의 역할들**이 찾아낼 수 있다
  (15장 §"Finding Entangled Dimensions", p.401).[^ford2021-hard-parts]

### 결합을 무엇으로 보는가

- **분석의 첫 부분이 아키텍트에게 답하는 물음은 "아키텍처 안의 부분들이 서로 어떻게 결합돼
  있는가"다.** 소프트웨어 개발 세계에 결합(coupling)의 정의가 아주 다양하지만 저자들은 이
  연습을 위해 **가장 단순하고 가장 직관적인 판**을 쓴다 (15장, p.401):[^ford2021-hard-parts]

  > The software development world has a wide variety of definitions of coupling, but we use
  > the simplest, most intuitive version for this exercise: if someone changes *X*, will it
  > possibly force *Y* to change?

  - **이 책이 결합을 규정하는 세 번째 자리다.** 1장의 용어 목록과 2장의 규정과 여기가 낱말이
    다르고, 셋 다 "하나의 변경이 다른 하나의 변경을 부르는가"를 묻는다. 그 대조는
    [변경에 대한 결합도](../concepts/coupling-with-respect-to-change.md)와
    [진화적 아키텍트의 역할](../concepts/evolutionary-architect-role.md)에 있다.
  - **여기 판이 가장 짧고 가장 조건이 약하다** — 1장 판은 `will possibly require`를 쓰고 2장
    판은 `cause`를 쓰는데, 여기는 **아키텍트가 직접 물어볼 수 있는 물음 꼴**이다. 방법 장이라
    실행할 수 있는 형태로 줄인 것으로 읽힌다. #hypothesis

### 정적 결합 다이어그램을 무엇으로 짓는가

- **2장이 세운 아키텍처 퀀텀 사이의 정적 결합이 기술적 결합의 망라적 구조 다이어그램을
  준다.** 그런데 **그것을 지어 주는 일반 도구는 없다 — 아키텍처마다 고유하기 때문**이다.
  대신 **조직 안에서는 개발 팀이 손으로든 자동화로든 정적 결합 다이어그램을 지을 수 있다**
  (15장, p.401).[^ford2021-hard-parts] 그 단위의 전문은
  [아키텍처 퀀텀](../concepts/architectural-quantum.md)이 갖는다.
- **마이크로서비스 하나의 정적 결합 다이어그램을 만들려면 아키텍트가 모아야 하는 것 다섯**
  (15장, p.401):[^ford2021-hard-parts]

  > - Operating systems/container dependencies
  >
  > - Dependencies delivered via transitive dependency management (frameworks, libraries, etc.)
  >
  > - Persistence dependencies on databases, search engines, cloud environments, etc.
  >
  > - Architecture integration points required for the service to bootstrap itself
  >
  > - Messaging infrastructure (such as a message broker) required to enable communication to
  >   other quanta

- **무엇이 빠지는지가 이 다이어그램의 정의를 만든다** — **정적 결합 다이어그램은 이 퀀텀과의
  워크플로 통신만이 유일한 결합 지점인 다른 퀀텀을 고려하지 않는다.** 예로 `AssignTicket
  Service`가 워크플로 안에서 `ManageTicket`과 협력하되 다른 결합 지점이 없다면 **둘은 정적으로
  독립이고(실제 워크플로가 도는 동안에는 동적으로 결합된다)** (15장, p.401).[^ford2021-hard-parts]
- **이미 환경 대부분을 자동화로 짓는 팀에게 방법이 하나 더 있다** — 그 생성 기제 안에 **체계가
  빌드되는 동안 결합 지점을 문서화하는 능력을 더해 넣을 수 있다** (15장,
  p.401).[^ford2021-hard-parts] 같은 축의 자동 집행은
  [자동화된 아키텍처 거버넌스](../concepts/automated-architectural-governance.md)에 있다.

### 이 책이 세 차원을 고른 경위

- **저자들이 자기 셈의 출처를 밝힌다** — 이 책의 목표가 **분산 아키텍처의 결합과 통신에서
  절충을 재는 것**이었고, **동적 퀀텀 결합의 세 차원이 될 것을 정하려고 분산 아키텍처의 사례
  수백 개(마이크로서비스와 그 밖의 것들)를 살펴 공통 결합 지점을 찾았다.** 그렇게 해서 **그
  사례 전부가 통신(communication)·일관성(consistency)·조율(coordination) 차원의 변화에
  민감했다**는 결론에 이르렀다 (15장, pp.401–402).[^ford2021-hard-parts]
  - **원문이 이 자리에서 `dynamical quantum coupling`이라 적는다.** 이 책의 다른 자리는 전부
    `dynamic quantum coupling`이다 (15장, p.401).[^ford2021-hard-parts] **이 KB는 원문
    표기를 그대로 두고 여기 적어 둔다.**
  - 그 세 축이 여덟 칸을 만드는 자리는 [아키텍처 퀀텀](../concepts/architectural-quantum.md)이고, 칸마다
    기제와 채점표가 채워지는 자리는 [트랜잭셔널 사가 패턴](transactional-saga-patterns.md)이다.
- **이 과정이 반복 설계의 중요성을 드러낸다고 저자들이 적는다** — **첫 초안이 언제나 완벽할
  만큼 뛰어난 아키텍트는 없다.** 워크플로의 표본 토폴로지를 지어 보면(이 책이 하는 것처럼)
  아키텍트나 팀이 **절충의 행렬 시야를 지을 수 있고, 그것이 임기응변 접근보다 더 빠르고 더
  철저한 분석을 가능하게 한다** (15장, p.402).[^ford2021-hard-parts]

## 걸음 둘 — 결합 지점 분석

- **분석할 결합 지점을 골랐으면 다음 걸음은 가능한 조합들을 가벼운 방식으로 모형화하는 것**
  이다. **어떤 조합은 실현 가능하지 않아 모형화를 건너뛸 수 있다.** 분석의 목표는 **아키텍트가
  연구해야 할 힘이 무엇인지, 다시 말해 어느 힘이 절충 분석을 요구하는지 정하는 것**이다
  (15장 §"Analyze Coupling Points", p.402).[^ford2021-hard-parts]
- **이 책이 자기 분석에 고른 것** — 아키텍처 퀀텀 동적 결합 분석에서 **결합·복잡도·응답성과
  가용성·확장성과 탄력성**을 주된 절충 관심사로 골랐고, 거기에 **통신·일관성·조율 세 힘의
  분석**을 더했다 (15장, p.402).[^ford2021-hard-parts] 그 채점의 한 칸이 표 15-1이고,
  원문은 12장 p.346의 채점표를 그대로 다시 싣는다 (15장, 표 15-1, p.402):[^ford2021-hard-parts]

  | Parallel Saga | Ratings |
  |---|---|
  | Communication | Asynchronous |
  | Consistency | Eventual |
  | Coordination | Centralized |
  | Coupling | Low |
  | Complexity | Low |
  | Responsiveness/availability | High |
  | Scale/elasticity | High |

  - **채점 목록을 지을 때의 규칙 하나** — **각 설계 해법(저자들이 이름 붙인 패턴들)을 따로
    떼어 고려했고, 차이를 보기 위해 마지막에만 합쳤다** (15장, p.402).[^ford2021-hard-parts]
- **합친 결과가 표 15-2다** (15장, 표 15-2, p.403):[^ford2021-hard-parts]

  | Pattern | Coupling level | Complexity | Responsiveness/availability | Scale/elasticity |
  |---|---|---|---|---|
  | Epic Saga | Very high | Low | Low | Very Low |
  | Phone Tag Saga | High | High | Low | Low |
  | Fairy Tale Saga | High | Very low | Medium | High |
  | Time Travel Saga | Medium | Low | Medium | High |
  | Fantasy Fiction Saga | High | High | Low | Low |
  | Horror Story | Medium | Very high | Low | Medium |
  | Parallel Saga | Low | Low | High | High |
  | Anthology Saga | Very low | High | High | Very high |

- **행렬을 만들자 관찰 둘이 나왔다고 적는다** (15장, p.403):[^ford2021-hard-parts]
  1. **결합 수준과 확장성·탄력성 사이의 직접적인 역상관** — 패턴에 결합이 많을수록 확장성이
     나쁘다. 직관에 맞는다 — **워크플로에 관여하는 서비스가 많을수록 아키텍트가 확장을
     설계하기 어렵다.**
  2. **응답성·가용성과 결합 수준 사이의 비슷한 관찰** — 앞만큼 직접적이지는 않되 유의미하다.
     **결합이 높으면 응답성과 가용성이 낮아지는데, 워크플로에 관여하는 서비스가 많을수록 한
     서비스의 장애로 워크플로 전체가 실패할 가능성이 커지기 때문**이다.
- **이 분석 기법이 반복적 아키텍처의 실례라고 적는다** — **아무리 영리한 아키텍트도 진짜로
  고유한 상황의 미묘함을 즉각 이해할 수 없고, 그 미묘함은 복잡한 아키텍처에서 끊임없이 나타난다.**
  가능성의 행렬을 지으면 **아키텍트가 한 차원 이상을 치환했을 때의 결과를 보려고 하고 싶은
  모형화 연습이 무엇인지 알려 준다** (15장, p.403).[^ford2021-hard-parts]

## 걸음 셋 — 절충 평가

- **반복적인 "만약에" 시나리오를 돌릴 수 있는 판을 지었으면, 주어진 상황의 근본 절충에
  집중한다.** 예로 이 책은 **동기 통신과 비동기 통신**에 집중했고, 그 선택이 **가능성과 제약을
  한 무더기 만든다 — 소프트웨어 아키텍처의 모든 것이 절충이다.** 그래서 **동기성 같은 근본
  차원을 먼저 고르는 일이 이후의 선택을 제한한다**
  (15장 §"Assess Trade-Offs", pp.403–404).[^ford2021-hard-parts]
- **그다음이 되풀이다** — 그 차원을 고정한 채 **첫 결정이 부추기거나 강제하는 후속 결정에 같은
  종류의 반복 분석을 수행한다.** 아키텍트 팀은 **어려운 결정, 다시 말해 차원들이 얽힌 결정을
  다 풀 때까지 이 과정을 되풀이할 수 있다** (15장, p.404).[^ford2021-hard-parts]
- **그리고 이 장에서 가장 짧은 문장이 남는다** (15장, p.404):[^ford2021-hard-parts]

  > What's left is design.

  - **이 한 줄이 이 책의 아키텍처와 설계 가름을 방법 쪽에서 되풀이한다** — 얽힌 차원을 다 풀고
    나면 남는 것이 설계라는 것이다. 그 가름의 규정은
    [진화적 아키텍트의 역할](../concepts/evolutionary-architect-role.md)에 있다.

## 기법 여섯

**저자들이 오랜 시간 여러 절충 분석을 만들며 쌓은 조언**이다 (15장 §"Trade-Off Techniques",
p.404).[^ford2021-hard-parts]

### 하나 — 정성 분석 대 정량 분석

- **이 책의 절충 표가 거의 하나도 정량적(quantitative)이지 않고 정성적(qualitative)이라는
  사실을 저자들이 스스로 짚는다.** 정량은 수에 기반하고 정성은 **양이 아니라 어떤 것의 질을
  재는 것**인데, **두 아키텍처는 참된 정량 비교를 막을 만큼 언제나 충분히 다르기 때문에 그것이
  필요하다.** 다만 **큰 데이터 집합에 통계 분석을 쓰면 합리적인 정성 분석이 가능해진다**
  (15장 §"Qualitative Versus Quantative Analysis", p.404).[^ford2021-hard-parts]
  - **절 제목의 `Quantative`는 원문의 오식이다** — 목차와 절 제목 두 자리에 같은 철자로
    인쇄돼 있고 본문은 `quantitative`를 쓴다 (15장, p.404 · 목차,
    p.x).[^ford2021-hard-parts] **이 KB는 원문 표기를 그대로 두고 여기 적어 둔다.**
- **그 통계 분석이 실제로 무엇이었는지도 밝힌다** — 패턴의 확장성을 비교할 때 **통신·일관성·
  조율 조합의 서로 다른 구현 여럿을 살펴 각 경우의 확장성을 평가했고**, 그것이 표 15-2의
  비교 눈금을 지을 수 있게 했다 (15장, p.404).[^ford2021-hard-parts]
- **조직 안의 아키텍트도 같은 연습을 할 수 있다** — **결합된 관심사의 차원 행렬을 짓고 대표
  사례를 보는 것**이며, 그 사례는 **조직 안의 기존 것이거나 이론을 시험하는 국소 스파이크**다
  (15장, p.404).[^ford2021-hard-parts]
- **권고는 한 문장이다** (15장, p.404):[^ford2021-hard-parts]

  > We recommend you hone the skill of performing qualitative analysis, as few opportunities
  > for true quantitative analysis exist in architecture.

  - **이것이 측정을 기각하는 말이 아니다.** 같은 장의 에필로그가 **테스트를 통해 정성에서
    정량으로 가는 길**을 적는다(아래 [에필로그가 남기는 주장](#에필로그가-남기는-주장)).
    여기서 기각되는 것은 **두 아키텍처를 수로 맞대는 비교**이지 자기 체계를 재는 일이 아니다.

### 둘 — MECE 목록

- **아키텍트가 비교하는 것이 같은 것인지부터 확인해야 한다** — 예로 **단순한 메시지 큐를
  엔터프라이즈 서비스 버스(ESB)와 비교하는 것은 타당한 비교가 아니다.** ESB는 메시지 큐를
  포함하되 다른 구성 요소를 수십 개 더 담고 있기 때문이다 (15장 §"MECE Lists",
  p.404).[^ford2021-hard-parts]
- **기술 전략 세계에서 빌려 온 개념이 MECE 목록**이고, **상호 배타적이고 전체를 망라하는
  (mutually exclusive, collectively exhaustive)**의 약자다 (15장,
  pp.404–405):[^ford2021-hard-parts]

  > *Mutually exclusive*
  >
  > None of the capabilities can overlap between the compared items. As in the preceding
  > example, it is invalid to compare a message queue to an entire ESB because they aren't
  > really the same category of thing. If you want to compare just the messaging capabilities
  > absent the other parts, that reduces the comparison to two mutually comparable things.
  >
  > *Collectively exhaustive*
  >
  > This suggests that you've covered all the possibilities in the decision space, and that
  > you haven't left out any obvious capabilities. For example, if a team of architects is
  > evaluating high-performance message queues and consider only an ESB and simple message
  > queue but not Kafka, they haven't considered all the possibilities in the space.

  - **저자들이 이 개념의 출처를 "기술 전략 세계"라고만 적고 사람이나 책을 대지 않는다** (15장,
    p.404).[^ford2021-hard-parts] **이 KB는 이 낱말의 원전을 확인하지 않았다.**
- **목표는 한 범주 공간을 구멍도 겹침도 없이 덮는 것**이고, 그림 15-1이 그것을 그림으로 보인다
  (15장, p.405).[^ford2021-hard-parts] 그림은 **한 정사각형을 빈틈없이 채운 타일 아홉**이고
  라벨이 둘 붙는다 — 타일 쪽이 `Individual items`, 정사각형 전체가 `Overall category`다
  (15장, 그림 15-1, p.405).[^ford2021-hard-parts]
- **망라성이 탐색을 강제한다** — **소프트웨어 개발 생태계가 끊임없이 진화하며 새 능력을
  드러내므로**, 장기적 함의를 가진 결정을 내릴 때 아키텍트는 **판단 기준을 바꿀 새 능력이 방금
  도착하지는 않았는지 확인해야 한다.** 비교 기준이 전체를 망라하게 만드는 일이 **그 탐색을
  부추긴다** (15장, p.405).[^ford2021-hard-parts]

### 셋 — 맥락 밖 함정

- **절충을 평가할 때 아키텍트는 결정을 맥락 안에 두어야 하고, 그러지 않으면 외부 요인이 분석에
  부당한 영향을 준다.** 흔히 **한 해법이 이로운 면을 많이 갖고도 성공을 막는 결정적 능력을
  빠뜨린다** (15장 §"The "Out-of-Context" Trap", p.405):[^ford2021-hard-parts]

  > Architects need to make sure they balance the *correct* set of trade-offs, not all
  > available ones.

- **저자들이 드는 예는 분산 아키텍처의 공통 기능을 공유 서비스로 할지 공유 라이브러리로 할지의
  결정**이다 (15장, 그림 15-2, p.406).[^ford2021-hard-parts] 도판 속 아키텍트의 말풍선이
  물음을 적는다 — `"I can't decide whether to use a shared service or shared library for all of
  the common functionality in the system."` 그 두 선택지의 전문은
  [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md)에 있다.
- **연구 끝에 나온 절충 행렬이 그림 15-3이고, 이 KB가 그 행렬을 표로 옮긴다** (15장, 그림 15-3,
  p.406):[^ford2021-hard-parts]

  | 판단 기준 | Custom shared library | Shared service |
  |---|---|---|
  | heterogeneous code | ✗ | ✓ |
  | high code volatility | ✗ | ✓ |
  | ability to version changes | ✓ | ✗ |
  | dependency management | ✗ | ✓ |
  | overall change risk | ✓ | ✗ |
  | performance | ✓ | ✗ |
  | fault tolerance | ✓ | ✗ |
  | scalability | ✓ | ✗ |

  - **행렬만 보면 공유 라이브러리가 여덟 중 다섯을 가져가고**, 원문도 도판에서 그쪽에 큰
    체크 표시를 준다. 그래서 **아키텍트가 공유 라이브러리를 고르는 것이 정당해 보인다 —
    전체로는(overall)** (15장, p.407).[^ford2021-hard-parts]
- **그런데 맥락이 들어오면 결론이 뒤집힌다** (15장, p.407):[^ford2021-hard-parts]

  > However, this decision exemplifies the *out-of-context* problem—when the extra context for
  > the problem becomes clear, the decision criteria changes

  - **그림 15-4가 같은 행렬에 맥락을 얹은 판이다.** 아키텍트의 말풍선이 그 맥락을 적는다 —
    `"We leverage polyglot programming and have services written in four different languages
    in our application ecosystem. Performance and fault tolerance aren't concerns for us—it's
    all about managing change to shared functionality."` **행렬의 값은 하나도 바뀌지 않고**,
    위의 두 행(`heterogeneous code`·`high code volatility`)에 강조가 들어가며 **큰 체크 표시가
    공유 서비스 쪽으로 옮겨 간다** (15장, 그림 15-4, p.407).[^ford2021-hard-parts]
  - **이 도판 쌍이 이 절의 논증 전부다** — 같은 증거, 다른 맥락, 반대 결론이다.
- **저자들이 이 과정에서 관찰 둘을 끌어낸다** (15장, p.407):[^ford2021-hard-parts]
  1. **결정에 맞는 맥락을 찾으면 아키텍트가 고려할 선택지가 줄어 결정 과정이 크게 단순해진다.**
     소프트웨어 현인들의 흔한 조언 하나가 **"단순한 설계를 껴안으라"**인데 **그 목표를 어떻게
     달성하는지는 아무도 설명하지 않는다.** 결정을 위한 **올바르게 좁은(narrow) 맥락**을 찾으면
     아키텍트가 더 적게 생각해도 되고 많은 경우 설계가 단순해진다.
  2. **반복 설계의 중요성** — 표본 아키텍처 해법을 그려 놓고 **정성적인 "만약에" 게임**을 해서
     아키텍처 차원들이 서로에게 주는 영향을 본다. 그러면 **가능한 해법을 조사하고 결정이 속할
     올바른 맥락을 발견할 수 있다.**

### 넷 — 관련 도메인 사례를 모형화하라

- **아키텍트는 진공 속에서, 곧 특정 해법에 값을 더하는 관련 구동 요인 없이 결정해서는 안 된다.**
  그 도메인 구동 요인을 결정 과정에 되돌려 넣으면 **선택지를 걸러 정말 중요한 절충에 집중하는
  데 도움이 된다** (15장 §"Model Relevant Domain Cases", p.408).[^ford2021-hard-parts]
- **예는 결제 서비스 하나를 만들 것인가 결제 종류마다 따로 만들 것인가의 결정**이다. 저자들은
  **7장이 준 통합 요인과 분해 요인을 쓸 수 있되 그 힘들은 일반적**이라며, **아키텍트가 있음직한
  시나리오를 모형화해 결정에 더 미묘한 결을 더할 수 있다**고 적는다 (15장,
  p.408).[^ford2021-hard-parts] 그 열 요인의 전문은 [서비스 세분도](../concepts/service-granularity.md)에 있다.
- **시나리오 셋을 차례로 얹는다** (15장, pp.408–410):[^ford2021-hard-parts]

  | 시나리오 | 무엇을 모형화하는가 | 드러나는 것 |
  |---|---|---|
  | 하나 | 신용카드 처리 서비스를 갱신한다 | 서비스를 나누면 **유지보수성·테스트 가능성·배포 가능성**이 낫다(퀀텀 수준의 격리 덕이다). 대가는 **서비스 사이의 정적 퀀텀 결합을 막으려는 코드 중복**이고, 그것이 나눠 둔 이점을 깎는다 |
  | 둘 | 결제 종류(`reward points`)를 새로 더한다 | 나눠 둔 서비스의 이점으로 **확장성(extensibility)**이 드러난다. 여기까지는 나누는 쪽이 매력적으로 보인다 |
  | 셋 | 결제 종류 여럿을 한 워크플로에서 쓴다 | 나눠 둔 서비스는 **조율이 필요하고 그것은 오케스트레이터가 가장 잘 다룬다.** 그런데 11장이 적었듯 오케스트레이터로 가면 **성능이 나빠지고 데이터 일관성이 더 어려워진다.** 오케스트레이터를 피할 수는 있지만 **워크플로 로직은 어딘가에 있어야 한다** |

  - 셋째 시나리오에서 저자들이 앞 장의 조문을 되부른다 — **의미적 결합은 구현으로 늘릴 수만
    있고 결코 줄일 수 없다** (15장, p.409).[^ford2021-hard-parts] 그 조문의 전문은
    [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md)에 있다.
- **셋을 모형화하고 나서야 진짜 절충이 드러난다** — 아키텍트가 깨닫는 것은 **진짜 절충 분석이
  무엇이 더 중요한가로 귀착한다**는 것이다. **성능과 데이터 일관성(결제 서비스 하나)인가,
  확장성과 민첩성(나눈 서비스들)인가** (15장, p.410).[^ford2021-hard-parts]
- **절의 결론** — **아키텍처 문제를 일반적이고 추상적으로 생각하는 것은 아키텍트를 어느 지점까지만
  데려간다.** 아키텍처는 대체로 일반 해법을 피하므로 **관련 도메인 시나리오를 모형화하는 기량을
  쌓는 것이 더 나은 절충 분석과 결정으로 좁혀 들어가는 데 중요하다** (15장,
  p.410).[^ford2021-hard-parts]

### 다섯 — 압도적 증거보다 결론

- **아키텍트가 절충 분석의 모든 면을 배우려다 엄청난 양의 정보를 쌓기 쉽고**, 무언가를 새로
  배운 사람은 대개 남에게 말하고 싶어 한다. 그런데 **아키텍트가 캐낸 기술 세부 다수가 비기술
  이해관계자에게는 난해하고, 그 세부의 양이 그들이 결정에 유의미한 통찰을 더할 능력을 압도할 수
  있다** (15장 §"Prefer Bottom Line over Overwhelming Evidence",
  p.410).[^ford2021-hard-parts]
- **그래서 처방은 줄이는 것이다** — **모은 정보를 전부 보이는 대신 아키텍트는 절충 분석을 몇
  가지 핵심 지점으로 줄여야 하고, 그것은 때로 개별 절충들의 집계다** (15장,
  p.410).[^ford2021-hard-parts]
- **예는 마이크로서비스에서 동기 통신과 비동기 통신을 고르는 흔한 문제**다. 동기 쪽 해법은
  오케스트레이터가 **동기 REST 호출**로 워크플로 협력자와 말하고, 비동기 쪽은 **메시지 큐**를
  쓴다 (15장, 그림 15-9, pp.410–411).[^ford2021-hard-parts]
- **일반 요인을 본 다음 아키텍트가 비기술 이해관계자가 관심 가질 도메인 시나리오를 생각하고
  절충 표를 짓는다** (15장, 표 15-3, p.411):[^ford2021-hard-parts]

  | Synchronous advantage | Synchronous disadvantage | Asynchronous advantage | Asynchronous disadvantage |
  |---|---|---|---|
  | | Customer must wait for credit card approval process to start | No wait for process to start | |
  | Credit approval is guaranteed to start before customer request ends | | | No guarantee that the process has started |
  | | Customer application rejected if orchestrator is down | Application submission not dependent on orchestrator | |

  - **표의 제목이 `Trade-offs between synchronous and asynchronous communication for credit
    card processing`이고**, 원문은 이 표를 네 열로 조판하되 **행마다 두 칸만 채운다** (15장,
    표 15-3, p.411).[^ford2021-hard-parts] 이 KB는 빈 칸을 그대로 두었다.
- **그러고 나서 결론 한 줄을 이해관계자에게 낸다** — **무엇이 더 중요한가, 신용 승인 절차가
  즉시 시작된다는 보장인가 응답성과 내결함성인가** (15장, p.411):[^ford2021-hard-parts]

  > Eliminating confusing technical details allows the nontechnical domain stakeholders to
  > focus on outcomes rather than design decisions, which help avoids drowning them in a sea
  > of details.

  - **인용문의 `which help avoids`는 원문 그대로다**(`which helps avoid`로 읽힌다) (15장,
    p.411).[^ford2021-hard-parts] **이 KB는 고치지 않았다.**

### 여섯 — 뱀 기름과 전도를 피하기

- **기술에 대한 열광의 불행한 부작용 하나가 전도(evangelism)이고, 그것은 기술 리드와 개발자에게
  허락된 사치이되 아키텍트는 그것 때문에 곤란해지는 경향이 있다**
  (15장 §"Avoiding Snake Oil and Evangelism", p.412).[^ford2021-hard-parts]
- **곤란해지는 기제가 적힌다** — 누군가 도구·기법·접근을 전도하면 **좋은 부분을 키우고 나쁜
  부분을 줄이기 시작하는데**, 불행히도 **소프트웨어 아키텍처에서 절충은 언제나 결국 돌아와 일을
  복잡하게 만든다** (15장, p.412).[^ford2021-hard-parts]
- **처방은 정직한 평가를 강제하는 것이다** — 아키텍트는 **충격적인 새 능력을 약속하는 어떤
  도구나 기법도 경계해야 하고**(그런 것은 주기적으로 나타났다 사라진다), **언제나 그 도구나
  기법의 전도자에게 좋은 점과 나쁜 점의 정직한 평가를 내놓게 강제해야 한다 — 소프트웨어
  아키텍처에 전부 좋기만 한 것은 없다.** 그래야 더 균형 잡힌 결정이 가능해진다 (15장,
  p.412).[^ford2021-hard-parts]
- **실패 양태에 도판이 붙는다 — "은탄환을 찾았다고 생각하는 아키텍트 전도자"다.** 말풍선이
  그 자신감을 적는다 — `"I always use topics for publish-and-subscribe broadcast messaging
  because it's best at supporting architectural extensibility!"` (15장, 그림 15-10,
  p.412).[^ford2021-hard-parts]
  - **그 아키텍트의 이력이 그 믿음을 설명한다** — 과거에 **확장성이 핵심 구동 아키텍처 특성**
    이었던 문제를 다뤄 성공했고 **그 능력이 언제나 결정 과정을 이끌 것이라 믿는다.** 그러나
    **아키텍처의 해법은 특정 문제 공간의 좁은 울타리 밖으로 잘 확장되지 않는다.** 한편으로
    **일화적 증거는 흔히 설득력이 있다** (15장, p.412).[^ford2021-hard-parts]
  - **그래서 물음이 선다** — **무릎 반사 같은 전도 뒤에 숨은 진짜 절충에 어떻게 이르는가.**
    답은 **시나리오 분석**이다 — 경험도 쓸모 있지만 **시나리오 분석은 체계 전체를 짓지 않고
    반복 설계를 가능하게 하는 아키텍트의 가장 강력한 도구 가운데 하나**이고, 있음직한 시나리오를
    모형화하면 **특정 해법이 실제로 잘 통할지 발견할 수 있다** (15장, p.412).[^ford2021-hard-parts]
- **그 발견을 실제로 해 보인다.** 기존 체계가 **토픽 하나로 변경을 방송**하고 있고 아키텍트의
  목표는 **`bid history`를 워크플로에 더하는 것**이다. 기존 발행-구독을 유지할 것인가, 소비자마다
  점대점 메시징으로 옮길 것인가 (15장, pp.412–413).[^ford2021-hard-parts]
  - **시나리오 하나 — 기존 토픽에 `bid history`를 더한다.** 통하기는 하되 문제가 셋이다
    (15장, 그림 15-11, p.413):[^ford2021-hard-parts]
    1. **소비자마다 다른 계약이 필요하면 어떻게 되는가.** 전부를 감싸는 큰 계약 하나를 지으면
       **"Stamp Coupling for Workflow Management" 안티패턴을 구현하는 것**이고, 팀마다 계약
       하나로 통일하게 강제하면 **아키텍처에 우발적 결합 지점이 생긴다** — 한 팀이 필요한 정보를
       바꾸면 모든 팀이 그 변경을 조율해야 한다.
    2. **데이터 보안은 어떻게 되는가.** 발행-구독 토픽 하나를 쓰면 **소비자마다 데이터 전부에
       접근**하게 되어 보안 문제와 PII(개인 식별 정보) 문제가 함께 생긴다.
    3. **소비자마다 운영 아키텍처 특성이 다르다.** 운영 팀이 `bid capture`와 `bid tracking`에만
       큐 깊이 모니터링과 자동 확장을 쓰고 싶어도 **토픽 하나를 쓰면 그것이 불가능하다 —
       소비자들이 운영상 결합돼 버린다.**
  - **시나리오 둘 — 소비자마다 큐를 둔다.** 워크플로의 각 부분(`bid capture`·`bid tracking`·
    `bid analytics`·`bid history`)이 자기 메시지 큐를 쓰고 앞의 문제들을 다룬다 — **소비자마다
    자기 계약을 가져 소비자끼리 결합이 풀리고**, **보안 접근과 데이터 통제가 생산자와 각 소비자
    사이의 계약 안에 놓여** 정보와 변경률의 차이를 허용하며, **큐마다 따로 모니터링하고 확장할
    수 있다** (15장, 그림 15-12, pp.413–414).[^ford2021-hard-parts]
  - **그리고 저자들이 곧바로 균형을 잡는다** — **이 책의 이 지점에 이르렀으면 독자는 점대점
    기반 체계도 완벽하지 않고 다른 절충 집합을 낼 뿐임을 알아야 한다** (15장,
    p.414).[^ford2021-hard-parts]
- **두 접근을 모형화하고 나면 차이가 표 15-4로 좁혀진다** (15장, 표 15-4,
  p.414):[^ford2021-hard-parts]

  | Point-to-point | Publish-and-subscribe |
  |---|---|
  | Allows heterogeneous contracts | Extensibility (easy to add new consumers) |
  | More granular security access and data control | |
  | Individual operational profiles per consumer | |

  - **결정은 아키텍트 혼자 내리지 않는다** — **운영·엔터프라이즈 아키텍트·업무 분석가 같은
    이해관계자와 상의해 어느 절충 집합이 더 중요한지 정해야 한다** (15장,
    p.415).[^ford2021-hard-parts]
- **반대 방향의 함정도 적힌다** — 아키텍트가 전도를 택한 것이 아니라 **뚜렷한 우위가 없는
  것에 대해 반대편 역할을 하도록 몰리는 경우**다. **기술에는 팬이 생기고 때로 열렬한 팬은
  단점을 깎아내리고 장점을 부풀린다** (15장, p.415).[^ford2021-hard-parts]
  - **저자 가운데 하나가 겪은 일화가 붙는다** — 어느 프로젝트의 기술 리드가 **모노레포 대
    트렁크 기반 개발**을 두고 저자를 논쟁으로 끌어들이려 했다. **둘 다 좋은 면과 나쁜 면이
    있는 고전적인 소프트웨어 아키텍처 결정**인데, 그 기술 리드는 모노레포의 열렬한 지지자였고
    **저자에게 반대편에 서라고 강요하려 했다 — 두 편이 없으면 논쟁이 아니기 때문**이다 (15장,
    p.415).[^ford2021-hard-parts]
  - **아키텍트가 한 일이 처방의 실물이다** — 그것이 절충이라고 짚으면서, **기술 리드가 내세운
    이점 다수가 그 팀에서 한 번도 나타난 적 없는 수준의 규율을 요구한다는 것을 부드럽게
    설명했다(물론 앞으로는 나아질 것이다).** 그리고 반대편에 서는 대신 **일반 해법이 아닌 실제
    세계의 절충 분석을 강제했다** — 모노레포를 시도하되 **나쁜 면이 나타나지 않는지 지표를
    모으기로 합의**했고, 피하려던 안티패턴 하나가 **저장소가 가깝다는 이유로 두 프로젝트 사이에
    생기는 우발적 결합**이었으므로, 아키텍트와 팀은 **기술적으로는 결합 지점을 만들 수 있어도
    적합도 함수가 그것을 막도록 적합도 함수 여러 개를 지었다** (15장,
    p.415).[^ford2021-hard-parts] 그 도구의 전문은
    [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md)에 있다.
  - **조문이 두 줄로 남는다** (15장, p.415):[^ford2021-hard-parts]

    > Don't allow others to force you into evangelizing something—bring it back to trade-offs.

    > We advise architects to avoid evangelizing and to try to become the objective arbiter of
    > trade-offs. An architect adds real value to an organization not by chasing silver bullet
    > after silver bullet but rather by honing their skills at analyzing the trade-offs as they
    > appear.

## 부록 C — 이 책이 자기 절충 표를 색인한다

- **부록 C가 이 책의 절충 표와 도판을 한자리에 모은다** — 저자들이 **이 책의 주된 초점이 절충
  분석이고 그래서 특정 아키텍처 관심사를 둘러싼 절충을 요약하는 표와 도판을 여럿 만들었다**고
  적으며, 이 부록이 **그것들을 쉽게 참조하도록 모두 요약한다**고 밝힌다 (부록 C,
  p.421).[^ford2021-hard-parts]
- **안내 문장이 범위를 `Part II`라고 적는데 목록의 첫 여덟 항목은 I부인 6장의 도판이다**
  (부록 C, pp.421–422).[^ford2021-hard-parts] **저자들이 그 어긋남을 적지 않는다.** #hypothesis
- **목록에 없는 것도 있다** — 12장의 채점표 여덟(표 12-1~12-10 가운데 패턴 채점표들)과 이 장의
  표 15-1이 빠져 있다. 셋 다 제목이 `Ratings`이고 부록이 나열하는 것은 제목에 `Trade-offs`가
  붙은 표들이라 **기준이 일관된 것으로 읽힌다.** #hypothesis 다만 부록 자신은 그 기준을 적지
  않고 **"모든 절충 표와 도판"**이라고만 적는다 (부록 C, p.421).[^ford2021-hard-parts]
- **이 색인은 이 KB가 빠뜨린 표가 있는지 확인하는 기계적 수단이다.** 아래 표의 셋째 열이 그
  대조 결과다 — 원문 항목 이름과 쪽은 부록 C가 인쇄한 그대로다 (부록 C,
  pp.421–423).[^ford2021-hard-parts]

  | 원문 항목 | 인쇄 쪽 | 이 KB에서 그 표를 담은 페이지 |
  |---|---|---|
  | Figure 6-25, "Relational databases rated for various adoption characteristics" | 163 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-26, "Key-value databases rated for various adoption characteristics" | 166 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-27, "Document databases rated for various adoption characteristics" | 168 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-28, "Column family databases rated for various adoption characteristics" | 170 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-30, "Graph databases rated for various adoption characteristics" | 172 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-31, "New SQL databases rated for various adoption characteristics" | 174 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-32, "Cloud native databases rated for various adoption characteristics" | 175 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) |
  | Figure 6-33, "Time-series databases rated for various adoption characteristics" | 177 | [데이터베이스 종류 고르기](../concepts/selecting-a-database-type.md) · [시계열 데이터베이스](../concepts/time-series-databases.md) |
  | Table 8-1, "Trade-offs for the code replication technique" | 223 | [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) |
  | Table 8-2, "Trade-offs for the shared library technique" | 227 | [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) |
  | Table 8-3, "Trade-offs for the shared service technique" | 233 | [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) |
  | Table 8-4, "Trade-offs for the Sidecar pattern / service mesh technique" | 239 | [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) · [API 게이트웨이와 서비스 메시](../concepts/api-gateway-and-service-mesh.md) |
  | Table 9-1, "Joint ownership table split technique trade-offs" | 256 | [서비스의 데이터 소유권](../concepts/service-data-ownership.md) |
  | Table 9-2, "Joint ownership data-domain technique trade-offs" | 258 | [서비스의 데이터 소유권](../concepts/service-data-ownership.md) |
  | Table 9-3, "Joint ownership delegate technique trade-offs" | 261 | [서비스의 데이터 소유권](../concepts/service-data-ownership.md) |
  | Table 9-4, "Joint ownership service consolidation technique trade-offs" | 262 | [서비스의 데이터 소유권](../concepts/service-data-ownership.md) |
  | Table 9-5, "Background synchronization pattern trade-offs" | 272 | [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) |
  | Table 9-6, "Orchestrated request-based pattern trade-offs" | 277 | [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) |
  | Table 9-7, "Event-based pattern trade-offs" | 279 | [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) |
  | Table 10-1, "Trade-offs for the Interservice Communication data access pattern" | 286 | [분산 데이터 접근 패턴 넷](../concepts/distributed-data-access-patterns.md) |
  | Table 10-2, "Trade-offs for the Column Schema Replication data access pattern" | 288 | [분산 데이터 접근 패턴 넷](../concepts/distributed-data-access-patterns.md) |
  | Table 10-3, "Trade-offs associated with the replicated caching data access pattern" | 293 | [분산 데이터 접근 패턴 넷](../concepts/distributed-data-access-patterns.md) |
  | Table 10-4, "Trade-offs associated with the data domain data access pattern" | 295 | [분산 데이터 접근 패턴 넷](../concepts/distributed-data-access-patterns.md) |
  | Table 11-1, "Trade-offs for orchestration" | 306 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 11-2, "Trade-offs for the Front Controller pattern" | 312 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 11-3, "Stateless choreography trade-offs" | 313 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 11-4, "Stamp coupling trade-offs" | 314 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) · [서비스 결합의 네 종류](../concepts/service-coupling-types.md) |
  | Table 11-5, "Trade-offs for the choreography communication style" | 315 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 11-6, "Trade-off between orchestration and choreography for ticket workflow" | 319 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) · [Sysops Squad 사례](../concepts/sysops-squad-case.md) |
  | Table 11-7, "Updated trade-offs between orchestration and choreography for ticket workflow" | 320 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 11-8, "Final trade-offs between orchestration and choreography for ticket workflow" | 320 | [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) |
  | Table 12-11, "Trade-offs associated with state management rather than atomic distributed transactions with compensating updates" | 356 | [트랜잭셔널 사가 패턴](transactional-saga-patterns.md) |
  | Table 12-12, "Trade-offs associated with atomic distributed transactions and compensating updates" | 363 | [트랜잭셔널 사가 패턴](transactional-saga-patterns.md) |
  | Table 13-1, "Trade-offs for strict contracts" | 371 | [계약의 스펙트럼](../concepts/contract-spectrum.md) |
  | Table 13-2, "Trade-offs for loose contracts" | 372 | [계약의 스펙트럼](../concepts/contract-spectrum.md) |
  | Table 13-3, "Trade-offs for consumer-driven contracts" | 375 | [계약의 스펙트럼](../concepts/contract-spectrum.md) · [소비자 주도 계약](../concepts/consumer-driven-contracts.md) |
  | Table 13-4, "Trade-offs for stamp coupling" | 379 | [계약의 스펙트럼](../concepts/contract-spectrum.md) |
  | Table 14-1, "Trade-offs for the Data Warehouse pattern" | 385 | [엔터프라이즈 데이터 웨어하우스](../concepts/enterprise-data-warehouse.md) |
  | Table 14-2, "Trade-offs for the Data Lake pattern" | 388 | [데이터 레이크](../concepts/data-lake.md) |
  | Table 14-3, "Trade-offs for the Data Mesh pattern" | 394 | [데이터 퀀텀](../concepts/data-quantum.md) |
  | Table 15-2, "Consolidated comparison of dynamic coupling patterns" | 403 | 이 페이지 §[걸음 둘](#걸음-둘--결합-지점-분석) |
  | Table 15-3, "Trade-offs between synchronous and asynchronous communication for credit card processing" | 411 | 이 페이지 §[다섯 — 압도적 증거보다 결론](#다섯--압도적-증거보다-결론) |
  | Table 15-4, "Trade-offs between point-to-point versus publish-and-subscribe messaging" | 414 | 이 페이지 §[여섯 — 뱀 기름과 전도를 피하기](#여섯--뱀-기름과-전도를-피하기) |

## 에필로그가 남기는 주장

- **책의 마지막 장면이 이 방법의 한계와 그 한계를 넘는 길을 함께 적는다** — 등장인물이 **일반
  조언에 기댈 수 없고 절충 분석의 힘든 일을 끊임없이 해야 한다**고 인정하자, 상대가 그것을
  **단점이 아니라 장점**이라고 되받는다. **차원을 떼어 내고 절충 분석을 수행하는 법을 다 같이
  배우면 배우는 것이 우리 아키텍처에 대한 구체적인 것들**이고, **한 문제의 절충 수를 실제로
  모형화하고 시험할 만큼 작은 수로 졸여 낼 수 있다면 우리 생태계에 대한 값을 매길 수 없는 지식을
  얻는다**는 것이다 (15장, p.416, 사가).[^ford2021-hard-parts]
- **그 자리에 이 책의 마지막 조문이 놓인다** (15장, p.416, 사가):[^ford2021-hard-parts]

  > I've always said that *testing is the engineering rigor of software development*.

  - 이어지는 논증 — **구조 공학자들은 수학과 예측 도구를 잔뜩 지었지만 그들의 것을 짓는 일은
    어렵고 비싸다. 소프트웨어는 훨씬… 무르다.** 다른 공학이 가진 종류의 수학은 없지만 **점진적으로
    짓고 시험할 수 있어 훨씬 큰 유연성을 허용하고 더 유연한 매체라는 이점을 지렛대로 쓴다**
    (15장, p.416, 사가).[^ford2021-hard-parts]
- **그리고 정성과 정량의 관계가 여기서 뒤집힌다** (15장, p.416, 사가):[^ford2021-hard-parts]

  > Testing with objective outcomes allows our trade-off analyses to go from qualitative to
  > quantitative—from speculation to engineering.

  - **이것이 §"Qualitative Versus Quantative Analysis"와 겨루지 않는다.** 그 절이 기각한 것은
    **두 아키텍처를 수로 맞대는 비교**이고, 여기가 여는 것은 **자기 생태계를 시험해 자기 절충을
    수로 만드는 길**이다. **재는 대상이 다르다** — 남의 아키텍처와 나의 아키텍처다. 이 구분은
    이 KB가 세운 것이고 저자들이 두 자리를 연결해 적지는 않는다. #hypothesis
  - **마지막 조건도 붙는다** — **우리 고유 생태계에 대해 배울 수 있는 구체적 사실이 많을수록
    분석이 더 정밀해진다** (15장, p.416, 사가).[^ford2021-hard-parts]
- **책을 닫는 장면이 이 사례의 마지막 결정 아닌 결정이다** — 등장인물 둘이 **큰 전환을 축하하러
  퇴근 후 모임에 가자**고 하며 끝난다 (15장, p.416, 사가).[^ford2021-hard-parts] 그 사례의 전체
  색인은 [Sysops Squad 사례](../concepts/sysops-squad-case.md)에 있다.

## 다른 소스의 결정 어림과 나란히

**넷을 대질했고 `contradicts`를 걸 사실 충돌이 없다.** 넷 다 이 책을 호명하지 않고 이 책도 그들을
호명하지 않으므로 **아래 대비는 이 KB가 세운 것이다.** #hypothesis

- **에번스의 여섯 필수와 같은 방향이다.** 포드의 "전도를 피하고 절충의 객관적 중재자가 되라"는
  경고는 에번스의 다섯째 필수와 같은 실패 양태를 겨눈다 — **분리된 아키텍처 팀은 애플리케이션
  팀 앞에 자기가 놓고 있을지 모르는 장애물에 대한 감이 덜하므로 특히 조심해야 하고, 동시에 자기
  주된 책임에 대한 아키텍트의 열의는 그들이 도를 넘기 쉽게 만든다** (17장,
  p.494).[^evans2003] **포드의 전도자는 에번스의 "도를 넘는 열의"의 한 판본**이고, 처방도 같은
  방향이다(포드는 시나리오 분석을, 에번스는 최소주의와 겸손을 든다). 전문은
  [전략 설계 결정하기](../concepts/strategic-decision-making.md)에 있다.
- **벡의 설계 경제학과 겨루지 않는다. 재는 대상이 다르다.** 포드의 "정량 비교는 아키텍처에
  드물다"는 **두 아키텍처를 맞대는 일**에 대한 판정이고, 벡의 할인 현금 흐름과 옵션 값은 **한
  변경을 지금 할 것인가 나중에 할 것인가**를 재는 어휘다. **그리고 벡 자신이 정밀도에 같은
  제동을 건다** — **정리의 규모, 분에서 시간에서는 우리가 정리의 경제학을 정확히 계산할 수 없고
  (그리고 계산하려 해서도 안 된다)** (27장).[^beck2023] 포드의 "압도적 증거보다 결론"과 벡의
  "정확히 계산하지 마라"가 **같은 방향을 가리킨다** — 수를 늘리는 것이 결정을 낫게 하지 않는다는
  것이다. 전문은 [소프트웨어 설계의 경제학](../concepts/software-design-economics.md)에 있다.
- **오스터하우트의 두 번 설계하라가 같은 절차를 코드 수준에서 적는다** — **급진적으로 다른 접근을
  고르려 하라; 그렇게 하면 더 많이 배운다** (11장, p.91)와 **대안의 설계를 대략 그린 뒤 각각의
  장단 목록을 만들어라** (11장, p.91)가 포드의 "가능한 조합을 가볍게 모형화하고 행렬을 짓는다"와
  같은 모양이다.[^ousterhout2021] **층이 다르다** — 저쪽은 클래스 인터페이스이고 이쪽은 분산
  아키텍처의 차원이다. 전문은 [두 번 설계하라](../concepts/design-it-twice.md)에 있다.
- **크호노프의 휴리스틱 규정이 이 기법들의 지위를 말해 준다** — **휴리스틱은 100% 옳다고 보장되고
  수학적으로 증명된 딱딱한 규칙이 아니라 어림이다. 완벽하다고 보장되지는 않되 당면 목표에는
  충분하다** (10장, p.159).[^khononov2021] 포드의 기법 여섯은 **어느 해법을 고르라는 어림이
  아니라 어림을 만드는 절차**라는 점에서 한 층 위에 있다. 전문은
  [업무 로직 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md)에 있다.

## 이어지는 페이지

- [진화적 아키텍트의 역할](../concepts/evolutionary-architect-role.md) — 이 방법을 쓰는 사람. 최선이 아니라
  가장 덜 나쁜 절충 조합을 찾는 것이 아키텍트의 일이라는 규정과 아키텍처와 설계의 가름
- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — 이 방법이 얽힌 것으로 세는 차원들. 정적·동적 결합과
  통신·일관성·조율의 3차원 공간
- [커네이선스](../concepts/connascence.md) — 그 정적·동적 가름이 나온 결합 어휘
- [서비스 세분도](../concepts/service-granularity.md) — 이 방법이 도메인 사례로 검증하는 통합 요인과 분해
  요인 열
- [트랜잭셔널 사가 패턴](transactional-saga-patterns.md) — 표 15-2가 요약하는 여덟 칸의 전문
- [Sysops Squad 사례](../concepts/sysops-squad-case.md) — 이 방법이 열네 장에 걸쳐 적용된 운영 예제와 그
  에필로그
- [아키텍처 결정 기록](../concepts/architecture-decision-records.md) — 이 분석의 결과를 남기는 형식
- [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) — 의미적 결합은 구현으로
  줄일 수 없다는 조문의 자리
- [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) — 맥락 밖 함정의 예가 다루는 공유 라이브러리와
  공유 서비스의 전문
- [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md) — 모노레포 일화에서 우발적 결합을
  막는 데 쓰인 도구
- [전략 설계 결정하기](../concepts/strategic-decision-making.md) — 같은 실패 양태를 2003년에 적은 자리
- [소프트웨어 설계의 경제학](../concepts/software-design-economics.md) — 같은 물음에 돈의 어휘로
  답하는 자리
- [두 번 설계하라](../concepts/design-it-twice.md) — 같은 절차를 코드 수준에서 적는 자리
- [업무 로직 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md) — 휴리스틱이라는 낱말의 규정
- [조직과 아키텍트](../synthesis/organizations-and-architects.md) — 이 역할이 사는 허브
- [소프트웨어 아키텍처](../synthesis/software-architecture.md) — 이 축의 부모 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021 — 15장 "Build Your Own Trade-Off
    Analysis" 전체(pp.399–416): 여는 사가(pp.399–400) · 장 도입부(p.400) ·
    §"Finding Entangled Dimensions"(pp.401–404, 하위 §"Coupling"(pp.401–402) ·
    §"Analyze Coupling Points"(pp.402–403) · §"Assess Trade-Offs"(pp.403–404)) ·
    §"Trade-Off Techniques"(pp.404–415, 하위 §"Qualitative Versus Quantative Analysis"(p.404) ·
    §"MECE Lists"(pp.404–405) · §"The "Out-of-Context" Trap"(pp.405–407) ·
    §"Model Relevant Domain Cases"(pp.408–410) ·
    §"Prefer Bottom Line over Overwhelming Evidence"(pp.410–411) ·
    §"Avoiding Snake Oil and Evangelism"(pp.412–415)) · §"Sysops Squad Saga: Epilogue"(p.416).
    그리고 2장 "Discerning Coupling in Software Architecture" 도입의 세 걸음 대목(p.27)과
    부록 C "Trade-Off References"(pp.421–423)와 목차 p.x. 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 18, 실측). 직인용 아홉(세 걸음 목록 · 결합의 정의 · 정적 결합 다이어그램의 다섯 ·
    "What's left is design." · 정성 분석 권고 · MECE 두 규정 · 올바른 절충 집합 · 맥락 밖 문제 ·
    결론으로 줄이라는 문장 · 전도 조문 둘 · 에필로그 둘)은 `pdftotext -layout` 추출로 문자 단위
    대조했고, 원문이 이탤릭으로 조판한 강조는 인용 안에서 유지했으며 줄바꿈 하이픈(U+2010)으로
    끊긴 낱말은 한 낱말로 이었다. 원문이 목록으로 조판한 것은 인용 블록 안에서 항목 사이에 빈
    줄을 넣어 옮겼다 — 낱말은 보태거나 빼지 않았다. 표 셋(15-1 · 15-2 · 15-3)과 표 15-4는
    열 머리글과 값을 원문 그대로 옮겼고 `pdftoppm -r 160 -png` 렌더로 눈으로 대조했다. 표 15-3은
    원문이 네 열로 조판하되 행마다 두 칸만 채우므로 빈 칸을 그대로 두었다. **그림 15-3과 15-4는
    도판이지만 내용이 절충 행렬이라 렌더해 표로 옮겼다** — 체크와 가위표는 `✓`와 `✗`로 적었고,
    원문이 색과 강조로 표시하는 것(선택된 쪽의 큰 체크 표시, 그림 15-4에서 강조된 행 둘)은
    산문으로 적었다. 그림 15-1(MECE)과 15-10(전도자)도 렌더해 본문이 적지 않는 라벨과 말풍선만
    옮겼고, 나머지 도판 일곱(그림 15-2 · 15-5~15-9 · 15-11 · 15-12)은 재현하지 않고 본문이 그
    도판에 대해 적는 것만 옮겼다(그림 15-2의 말풍선은 예외로 옮겼다 — 본문이 그 물음을 적지
    않는다). **이 장에 코드 목록이 하나도 없다.** 원문 오식·어긋남 넷을 그대로 두고 표시했다 —
    절 제목과 목차의 `Quantative`(quantitative) · p.401의 `dynamical quantum coupling`
    (dynamic) · p.411의 `which help avoids`(which helps avoid) · 부록 C가 범위를 `Part II`라
    적고 I부 6장 도판 여덟을 나열하는 것이다. 여는 사가의 날짜 어긋남은
    [Sysops Squad 사례](../concepts/sysops-squad-case.md)가 갖는다. 저자들이 대는 바깥 것들(MECE를 준
    "기술 전략 세계" · Kafka · 모노레포와 트렁크 기반 개발)은 **이 KB가 확인한 원전이 아니다** —
    귀속은 이 책이 그렇게 귀속한다까지로 둔다. 굵은 글씨는 원문 문장의 한국어 재서술이고 괄호
    안이 그 쪽이다.

[^evans2003]: Evans 2003, 17장 "Bringing the Strategy Together"
    §"Six Essentials for Strategic Design Decision Making"(pp.492–495). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 33, 실측). 본문은 [전략 설계 결정하기](../concepts/strategic-decision-making.md)에
    있고, 이 페이지는 전도 경고를 대질하는 데에만 인용한다.

[^beck2023]: Beck 2023, 27장 "Options Versus Cash Flows". **이 소스의 locator는 장 단위다** —
    검증 절차와 근거는 `it/archive/beck2023/_progress.yaml` 머리말이 정본이다. 본문은
    [소프트웨어 설계의 경제학](../concepts/software-design-economics.md)에 있고, 이 페이지는
    정량 분석의 정밀도를 대질하는 데에만 인용한다.

[^ousterhout2021]: Ousterhout 2021, 11장 "Design it Twice". 쪽은 인쇄판 쪽 번호. 본문은
    [두 번 설계하라](../concepts/design-it-twice.md)에 있고, 이 페이지는 대안 비교 절차를
    대질하는 데에만 인용한다.

[^khononov2021]: Khononov 2021, 10장 "Design Heuristics" 도입(p.159). 쪽은 인쇄판 쪽 번호
    (PDF 쪽 − 26, 실측). 본문은
    [업무 로직 패턴 고르기](../concepts/choosing-a-business-logic-pattern.md)에 있고, 이 페이지는
    어림이라는 낱말의 지위를 대질하는 데에만 인용한다.

---
type: concept
title: 트랜잭셔널 사가 패턴
status: draft
description: 통신·일관성·조율 세 축의 여덟 조합에 각각 패턴 이름을 붙이고 그 하나하나를 기제와 절충으로 펴는 자리 — 여덟 이름과 세 글자 코드의 규칙, 등각 다이어그램이라는 조판 약속과 그 범례, 패턴마다 매겨지는 채점 축 넷(결합·복잡도·응답성과 가용성·확장성과 탄력성)과 다섯 눈금, 그리고 동기 쪽 네 칸 — 모놀리스를 흉내 내며 보상 트랜잭션으로 원자성을 노리는 Epic Saga(sao), 조율자 없이 원자성을 지키려다 프런트 컨트롤러를 낳는 Phone Tag Saga(sac), 원자성만 놓고 오케스트레이터는 남겨 절충이 가장 고른 Fairy Tale Saga(seo), 둘 다 놓고 한 방향 파이프라인이 되는 Time Travel Saga(sec) — 각각의 기제와 원문 채점표와 언제 쓰는가, 그리고 이 장이 "원자적"이라는 낱말을 보장이 아니라 목표로 쓴다는 판정
generated: { by: "claude-opus-5", at: "2026-09-18T02:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
---

# 트랜잭셔널 사가 패턴

- [세 축과 여덟 칸](#세-축과-여덟-칸)
- [이름과 세 글자 코드](#이름과-세-글자-코드)
- [등각 다이어그램과 그 범례](#등각-다이어그램과-그-범례)
- [채점 축 넷과 다섯 눈금](#채점-축-넷과-다섯-눈금)
- [Epic Saga(sao) - 전통적인 사가](#epic-sagasao---전통적인-사가)
- [Phone Tag Saga(sac) - 조율자 없이 원자성을 지키기](#phone-tag-sagasac---조율자-없이-원자성을-지키기)
- [Fairy Tale Saga(seo) - 원자성만 놓기](#fairy-tale-sagaseo---원자성만-놓기)
- [Time Travel Saga(sec) - 둘 다 놓기](#time-travel-sagasec---둘-다-놓기)
- [동기 쪽 네 칸을 한자리에 놓으면](#동기-쪽-네-칸을-한자리에-놓으면)
- [원자적이라는 낱말이 여기서 무엇인가](#원자적이라는-낱말이-여기서-무엇인가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **통신·일관성·조율을 어떻게 고르느냐에 따라 서비스를 가로지르는 업무 요청이
어떤 모양이 되고, 그 모양마다 무엇을 얻고 무엇을 내주는가.**

세 축 자체의 규정과 여덟 칸의 결합 강도표는
[아키텍처 퀀텀](../concepts/architectural-quantum.md)이 갖고, 조율 축 하나의 전문은
[오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)가, 일관성 축 하나의
전문은 [최종 일관성 패턴 셋](eventual-consistency-patterns.md)이 갖는다. 여기 있는 것은
**세 축을 곱한 칸 하나하나**다.

## 세 축과 여덟 칸

- **이 장은 2장이 세운 행렬을 그대로 다시 싣는 데서 시작한다** — 아키텍트가 트랜잭셔널 사가를
  어떻게 구현할지 고를 때 서로 교차하는 차원들을 나란히 놓은 행렬이고, 그것이 표 12-1이다
  (12장, p.324).[^ford2021-hard-parts]
- **표 12-1의 열 머리글과 값을 그대로 옮긴다** (12장, p.324):[^ford2021-hard-parts]

| Pattern name | Communication | Consistency | Coordination |
|---|---|---|---|
| Epic Saga<sup>(sao)</sup> | Synchronous | Atomic | Orchestrated |
| Phone Tag Saga<sup>(sac)</sup> | Synchronous | Atomic | Choreographed |
| Fairy Tale Saga<sup>(seo)</sup> | Synchronous | Eventual | Orchestrated |
| Time Travel Saga<sup>(sec)</sup> | Synchronous | Eventual | Choreographed |
| Fantasy Fiction Saga<sup>(aao)</sup> | Asynchronous | Atomic | Orchestrated |
| Horror Story<sup>(aac)</sup> | Asynchronous | Atomic | Choreographed |
| Parallel Saga<sup>(aeo)</sup> | Asynchronous | Eventual | Orchestrated |
| Anthology Saga<sup>(aec)</sup> | Asynchronous | Eventual | Choreographed |

- **2장의 표 2-1과 제목이 같은데 열이 하나 다르다** — 두 표 모두 캡션이
  `The matrix of dimensional intersections for distributed architectures`이고 저자들은 12-1을
  **재수록(reproduced)**이라 적는데, **2장 판에 있던 다섯째 열 `Coupling`(결합 강도)이 12장
  판에는 없다.** 값의 대소문자도 다르다 — 2장은 `synchronous`·`atomic`·`orchestrated`처럼
  소문자이고 12장은 첫 글자가 대문자다 (2장, p.41 · 12장, p.324).[^ford2021-hard-parts]
  **저자들이 그 차이를 적지 않는다.** 빠진 결합 열의 값은 이 장에서 패턴마다 붙는 채점표의
  `Coupling` 행으로 되돌아온다.
- **한 칸도 버리지 않는다** (12장, p.324):[^ford2021-hard-parts]

  > While architects will utilize some of the patterns more than others, they all have
  > legitimate uses and differing sets of trade-offs.

  - 곧 **여덟이 좋고 나쁨의 사다리가 아니라 절충의 목록**이라는 것이 이 장의 전제다.
- **다만 여는 사가에서는 한 칸을 안티패턴이라 부른다** — 등장인물이 비동기 통신·원자적
  트랜잭션성·코레오그래피로 설계한 워크플로를 수석 아키텍트가 **Horror Story 사가 통신 패턴,
  아니 사실은 안티패턴**이라 부르고, **우리가 출발점으로 삼는 일반 사가 패턴이 여덟 있으니
  그것들을 알아 두는 것이 좋다. 각각 절충의 균형이 다르기 때문**이라고 말한다 (12장, p.323,
  사가).[^ford2021-hard-parts] **본문의 "여덟 다 정당한 쓰임이 있다"와 나란히 놓으면
  낱말이 어긋나고 저자들이 그 어긋남을 적지 않는다.**
- **이 장이 다루는 것은 정상 경로가 아니라 오류다** (12장, p.324):[^ford2021-hard-parts]

  > After all, since distributed transactions lack atomicity (see "Distributed Transactions"
  > on page 263), what makes them interesting is when problems occur.

  - 저자들이 가리키는 p.263의 판정 — **분산 트랜잭션은 ACID 성질을 지원하지 않는다** — 의 전문은
    [트랜잭션과 ACID](acid-transactions.md)와
    [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)에 있다.

## 이름과 세 글자 코드

- **이름은 저자들이 지은 변덕스러운 이름이고, 코드가 실제 식별자다** (12장,
  p.324):[^ford2021-hard-parts]

  > We provide whimsical names for each combination, all derived from types of sagas.
  > However, the pattern names exist to help differentiate the possibilities, and we don't
  > want to provide a memorization test to associate a pattern name to a set of
  > characteristics, so we have added a superscript to each saga type indicating the values
  > of the three dimensions listed in alphabetical order (as in Table 12-1).

  - **알파벳 순서**란 통신(communication)·일관성(consistency)·조율(coordination) 셋을 영어
    낱말의 자모 순으로 늘어놓은 것이고, 그래서 코드의 첫 글자가 통신, 둘째가 일관성, 셋째가
    조율이다.
  - 저자들이 드는 예가 그대로 해독표다 — **Epic Saga(sao)는 통신·일관성·조율에 대해
    synchronous·atomic·orchestrated를 뜻한다** (12장, p.324).[^ford2021-hard-parts]
    나머지 글자는 `a`=asynchronous(통신) · `e`=eventual(일관성) · `c`=choreographed(조율)다.
  - **이름을 외우지 말라는 것이 저자들의 의도**다. 위첨자가 이름과 성질 집합을 잇는 일을
    대신한다고 적는다.
- **여덟 중 일곱만 "Saga"로 끝난다** — `aac` 조합만 `Horror Story`이고 나머지 일곱은 모두 사가다
  (12장, p.324, 표 12-1).[^ford2021-hard-parts] 이 장에서도 저자들이 그 예외의 이유를 적지
  않는다.
- 이 페이지는 패턴 이름을 **원문 표기 그대로 인라인 코드나 위첨자로** 옮긴다. 한국어 역어를
  만들지 않았다 — 이름이 뜻을 나르지 않고 식별자 구실만 하기 때문이고, 저자들 자신이 그렇게
  적는다.

## 등각 다이어그램과 그 범례

- **패턴마다 도판이 둘씩 붙는다** (12장, p.325):[^ford2021-hard-parts]

  > We illustrate each possible communication combination with both a three-dimensional
  > representation of the intersection of the three forces in space along with an example
  > workflow using generic distributed services, which we refer to as isomorphic diagrams.

  - 앞의 것은 **세 축의 정육면체 안에 공 하나를 놓아 그 패턴의 자리를 표시하는 그림**이고, 뒤의
    것이 **등각 다이어그램(isomorphic diagram)**이다.
  - 등각 다이어그램의 목적은 **서비스 사이 상호작용을 가장 일반적인 방식으로 보이는 것**이고,
    저자들의 목표는 **아키텍트의 개념을 가장 단순한 형태로 보이는 것**이다 (12장,
    p.325).[^ford2021-hard-parts]
  - **모든 상호작용을 그리지 않는다** — 반복이 될 뿐이라서, 저자들은 **그 패턴을 다른 패턴과
    구별 짓는 특징**만 골라 그린다고 적는다 (12장, p.325).[^ford2021-hard-parts]
- **그림 12-1이 이 장 전체의 범례다.** 도판이 이미지 조판이라 `pdftoppm -r 160 -png`로 렌더해
  눈으로 읽었고, 본문이 적지 않는 라벨이라 여기 옮긴다 (12장, p.325, 그림
  12-1):[^ford2021-hard-parts]
  - 상자 기호 넷 — `Transaction boundary`(점선 네모) · `Domain Service` · `Mediator Service` ·
    `Error condition causing rollback`(붉은 X).
  - 화살표 다섯 — `Async one-way communication` · `Sync one-way communication` ·
    `Sync two-way communication` · `Sync compensation request` · `Async compensation`.
  - **트랜잭션 경계를 어디에 두는가가 도판의 주된 정보**다. 아래 네 패턴에서 그 점선이 전체를
    한 번 두르는지 서비스마다 따로 두르는지가 일관성 축의 값과 그대로 대응한다.
- **세 축의 정육면체 그림에서 조율 축의 바깥쪽 끝 라벨이 `Choreography`다** — 표 12-1의 값은
  `Choreographed`인데 그림의 축 라벨은 명사형이다 (12장, pp.326·330·334·337, 그림 12-2·12-6·
  12-8·12-10).[^ford2021-hard-parts] 통신 축은 `Sync`–`Async`, 일관성 축은 `Atomic`–`Eventual`로
  본문과 같다.

## 채점 축 넷과 다섯 눈금

- **패턴마다 같은 네 항목이 산문으로 매겨지고 그 뒤에 표로 닫힌다.** 항목의 원문 이름은
  `Coupling level`·`Complexity level`·`Responsiveness/availability`·`Scale/elasticity`이고,
  표에서는 `Coupling`·`Complexity`·`Responsiveness/availability`·`Scale/elasticity`로 적힌다
  (12장, pp.329·333·336·339, 표 12-2~12-5).[^ford2021-hard-parts]
- **표는 일곱 행이다** — 세 축의 값(`Communication`·`Consistency`·`Coordination`)이 먼저 오고
  채점 넷이 뒤에 온다. 곧 **세 축은 선택이고 넷은 그 선택의 귀결**이라는 짜임이다.
- **눈금은 다섯이다** — `Very high`·`High`·`Medium`·`Low`·`Very low`. 이 장의 동기 쪽 네 칸에서
  다섯이 모두 쓰인다 (12장, 표 12-2~12-5).[^ford2021-hard-parts]
  - **방향이 항목마다 다르다는 데 주의한다.** 결합과 복잡도는 **낮을수록 좋고**, 응답성·가용성과
    확장성·탄력성은 **높을수록 좋다.** 저자들이 그 방향을 따로 적지 않는다.
- **저자들이 이 넷을 고른 이유를 이 장에서 적지 않는다.** #hypothesis 다만 넷 가운데 셋(결합·
  응답성과 가용성·확장성과 탄력성)이 2장 이후 이 책이 계속 쓰는 축이고, 복잡도만 이 장에서
  새로 붙는다.

## Epic Saga(sao) - 전통적인 사가

- **가장 많은 아키텍트가 "사가"라고 할 때 떠올리는 것이 이 칸이다** (12장,
  p.325):[^ford2021-hard-parts]

  > This type of communication is the "traditional" saga pattern as many architects
  > understand it, also called an *Orchestrated Saga* because of its coordination type.

- **아키텍트가 이 패턴을 고를 때의 목표는 모놀리식 체계의 행동을 흉내 내는 것**이고, 저자들이
  그것을 좌표로 못 박는다 — **모놀리식 체계를 그림 12-2에 얹는다면 원점 (0, 0, 0)일 것이다.
  분산이 아예 없기 때문**이다. 그래서 이 통신 양식이 **전통적 트랜잭션 체계의 아키텍트와
  개발자에게 가장 익숙하다** (12장, p.325).[^ford2021-hard-parts]
- **기제** — 오케스트레이터 서비스가 서비스 셋의 갱신을 담은 워크플로를 조율하고, 그 셋이
  **트랜잭션으로 일어나기를 기대한다. 세 호출이 모두 성공하거나 하나도 성공하지 않는다.**
  하나가 실패하면 **전부 실패하고 이전 상태로 돌아간다** (12장, p.327).[^ford2021-hard-parts]
  - 도판에서는 **점선 트랜잭션 경계 하나가 중재자와 도메인 서비스 셋을 통째로 두른다** (12장,
    p.326, 그림 12-3).[^ford2021-hard-parts]
  - 저자들이 곧바로 단서를 단다 — 아키텍트가 이 조율 문제를 푸는 길은 여럿이지만 **분산
    아키텍처에서는 전부 복잡하고**, 그런 트랜잭션은 **데이터베이스 선택을 제한하며 전설적인
    실패 양태를 갖는다** (12장, p.327).[^ford2021-hard-parts]
- **패턴이 있다는 것이 풀렸다는 뜻이 아니라는 경고가 이 자리에 붙는다** (12장,
  p.327):[^ford2021-hard-parts]

  > Many nascent or naive architects trust that, because a pattern exists for a problem, it
  > represents a clean solution. However, the pattern is recognition of only commonality,
  > not solvability.

  - 이어지는 진단 — 비분산 체계에서 트랜잭션을 모델링하는 데 익숙한 아키텍트는 **그 능력을
    분산 세계로 옮기는 것이 점진적 변화라고 믿기도 한다.** 그러나 분산 아키텍처의 트랜잭션은
    여러 도전을 내놓고, 그 도전은 **문제의 의미적 결합(semantic coupling)이 복잡할수록 비례해
    나빠진다** (12장, p.327).[^ford2021-hard-parts] 의미적 결합의 규정은
    [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md)에 있다.
- **흔한 구현이 보상 트랜잭션이고, 보상 갱신의 규정이 여기 있다** (12장,
  p.327):[^ford2021-hard-parts]

  > A *compensating update* is one that reverses a data write action performed by another
  > service (such as reversing an update, reinserting a previously deleted row, or deleting
  > a previously inserted row) during the course of the distributed transaction scope.

  - **그 규정에 곧바로 대가가 붙는다** — 보상 갱신은 분산 데이터 원천을 트랜잭션 시작 전의
    원래 상태로 되돌리려 시도하지만 **복잡한 문제와 도전과 절충으로 가득 차 있다** (12장,
    p.327).[^ford2021-hard-parts]
  - **보상 트랜잭션 패턴은 요청의 트랜잭션 완결성을 감시하는 서비스를 하나 지정한다** (12장,
    p.327, 그림 12-4).[^ford2021-hard-parts]
- **오류 경로가 이 패턴의 본체다** — 보상 트랜잭션 프레임워크에서 **중재자(mediator)가 호출의
  성공을 감시하고, 요청 하나 이상이 실패하면 다른 서비스들에 보상 호출을 낸다** (12장, p.328,
  그림 12-5).[^ford2021-hard-parts]
  - 저자들이 드는 장면 — 중재자가 요청을 받고 워크플로를 중재하는데 앞 두 서비스로 가는 동기
    호출은 성공하고 마지막 서비스 호출이 실패한다. **Epic Saga(sao)의 목표가 원자적 일관성이므로
    중재자는 보상 트랜잭션을 써서 다른 두 서비스에 앞서 한 오퍼레이션을 되돌리라고 요청하고,
    전체 상태를 트랜잭션 시작 전으로 되돌려야 한다** (12장, p.328).[^ford2021-hard-parts]
    - 원문 오식 하나가 이 문장에 있다 — 실패 사유를 적는 괄호가
      `(from a possibly a wide variety of both domain and operational reasons)`로 관사가
      겹친다 (12장, p.328).[^ford2021-hard-parts] 두 추출기와 렌더가 모두 같은 문장을 낸다.
- **왜 이것이 기본값이 되는가** — 저자들이 이유 셋을 댄다. **익숙한 행동을 모델링하고, 잘 알려진
  패턴 이름을 갖고 있으며**, 여기에 **상태 변경이 반드시 동기화되어야 한다는 이해관계자의 요청
  (때로는 요구)이 기술적 제약과 무관하게** 겹친다. 그래서 **많은 아키텍트가 모놀리식
  아키텍처와 비슷하게 느껴진다는 이유로 이 패턴을 기본으로 삼는다** (12장,
  p.328).[^ford2021-hard-parts]
  - **그 자리에서 저자들이 곧바로 제동을 건다** — **다른 동적 퀀텀 결합 패턴 여럿이 더 나은
    절충 집합을 줄 수 있다** (12장, p.328).[^ford2021-hard-parts]
- **이점은 둘, 단점은 둘로 정리된다** (12장, pp.328–329):[^ford2021-hard-parts]
  - 이점 — **모놀리식 체계를 흉내 내는 트랜잭션 조율**과 **오케스트레이터로 표현되는 뚜렷한
    워크플로 주인**.
  - 단점 첫째 — **오케스트레이션에 트랜잭션성이 더해지면 성능·확장성·탄력성 같은 운영
    아키텍처 특성에 영향이 간다.** 오케스트레이터가 **트랜잭션 참여자 전부가 성공했는지
    실패했는지 확인해야 하므로 타이밍 병목이 생긴다.**
  - 단점 둘째 — 분산 트랜잭션성을 구현하는 여러 패턴(보상 트랜잭션 같은)이 **다양한 실패
    양태와 경계 조건에 굴복하고**, 되돌리기 오퍼레이션 때문에 **본질적 복잡도가 더해진다.**
  - 그 단락이 이 절의 결론으로 닫힌다 (12장, p.329):[^ford2021-hard-parts]

    > Distributed transactions present a host of difficulties and thus are best avoided if
    > possible.

- **채점 넷의 근거** (12장, p.329):[^ford2021-hard-parts]
  - **결합** — 가능한 모든 차원에서 극히 높은 결합을 보이고, **사실상 이 목록에서 가장 높게
    결합된 패턴**이다. 높게 결합된 모놀리식 체계의 통신을 모델링하니 놀랍지 않지만 **분산
    아키텍처에서는 여러 문제를 만든다.**
  - **복잡도** — 오류 조건과 집중적인 조율이 원자성 요구에 더해져 복잡도를 올린다. **그러나
    동기 호출이 복잡도의 일부를 덜어 준다** — 아키텍트가 **호출 중의 경쟁 조건과 교착을 걱정할
    필요가 없기 때문**이다.
  - **응답성과 가용성** — 오케스트레이션이 병목을 만들고, 트랜잭션 원자성까지 조율해야 할 때
    특히 그렇다. 동기 호출이 성능과 응답성에 더 영향을 준다. **서비스 하나라도 가용하지 않거나
    복구 불가능한 오류가 나면 이 패턴은 실패한다.**
  - **확장성과 탄력성** — 응답성과 마찬가지로 **병목과 조율 요구가 확장과 다른 운영 관심사를
    어렵게 만든다.**
- **표 12-2의 행과 값을 그대로 옮긴다** (12장, p.329):[^ford2021-hard-parts]

| Epic Saga<sup>(sao)</sup> pattern | Ratings |
|---|---|
| Communication | Synchronous |
| Consistency | Atomic |
| Coordination | Orchestrated |
| Coupling | Very high |
| Complexity | Low |
| Responsiveness/availability | Low |
| Scale/elasticity | Very low |

- **언제 쓰는가** — 저자들이 이 패턴에는 권장 상황을 적지 않는다. 대신 절을 닫는 문장이
  **익숙해 보이지만 우발적 복잡도(accidental complexity)를 만드는 패턴을 기본값으로 삼을 필요가
  없다**는 것이고, 구체적인 사례와 그 도전을 다루는 법은 같은 장 뒤쪽의 사가 상자로 넘긴다
  (12장, p.330).[^ford2021-hard-parts]

## Phone Tag Saga(sac) - 조율자 없이 원자성을 지키기

- **Epic Saga(sao)에서 축 하나만 바꾼 것이다** — **조율을 오케스트레이션에서 코레오그래피로**
  바꾼다 (12장, p.330).[^ford2021-hard-parts]
- **이름의 유래가 적힌다** — 북미에서 *Telephone*이라 불리는 아이들 놀이를 닮아서다. **아이들이
  둥글게 서서 한 사람이 옆 사람에게 비밀을 속삭이고 그 사람이 다음 사람에게 넘겨, 마지막 사람이
  최종판을 말한다** (12장, p.330).[^ford2021-hard-parts]
- **조율자가 없는데 원자성을 요구한다는 것이 이 칸의 긴장이다** (12장,
  p.331):[^ford2021-hard-parts]

  > The Phone Tag Saga<sup>(sac)</sup> pattern features atomicity but also choreography,
  > meaning that the architect designates no formal orchestrator. Yet atomicity requires
  > some degree of coordination.

  - **저자들이 그 긴장을 푸는 방식이 프런트 컨트롤러다** — **처음 호출된 서비스가 조율 지점이
    되고, 그것을 때로 프런트 컨트롤러(front controller)라 부른다.** 그 서비스가 자기 일을
    마치면 워크플로의 다음 서비스로 요청을 넘기고, 워크플로가 성공할 때까지 이어진다 (12장,
    p.331, 그림 12-7).[^ford2021-hard-parts]
  - **오류가 나면 각 서비스가 사슬을 거슬러 보상 요청을 보내는 로직을 스스로 갖고 있어야
    한다** (12장, p.331).[^ford2021-hard-parts]
  - 도판에서 **점선 트랜잭션 경계는 여전히 서비스 셋을 통째로 두른다** — 오케스트레이터 상자만
    사라지고 경계는 하나다 (12장, p.331, 그림 12-7).[^ford2021-hard-parts] 일관성 축이 원자적인
    것이 그림에 그렇게 나타난다.
- **원자성의 로직이 어디론가 가야 한다는 것이 대가의 출처다** (12장,
  p.331):[^ford2021-hard-parts]

  > Because the architectural goal is transactional atomicity, logic to coordinate that
  > atomicity must reside somewhere.

  - 그래서 **도메인 서비스가 자기가 참여하는 워크플로 맥락에 대해 더 많은 로직을 담아야
    하고**, 거기에 **오류 처리와 라우팅**이 포함된다 (12장, p.331).[^ford2021-hard-parts]
  - **복잡한 워크플로에서는 이 패턴의 프런트 컨트롤러가 대부분의 중재자만큼 복잡해지고**, 그것이
    **이 패턴의 매력과 적용 가능성을 줄인다** (12장, p.331).[^ford2021-hard-parts]
  - 그래서 **이 패턴은 더 높은 확장성이 필요한 단순한 워크플로에 흔히 쓰이되 성능 영향이 있을
    수 있다** (12장, p.331).[^ford2021-hard-parts]
- **왜 조율자를 빼면 확장성이 오르는가** — 저자들이 스스로 묻고 답한다. **동기 통신을 쓰더라도
  코레오그래피는 병목을 줄인다.** 오류가 아닌 조건에서는 **워크플로의 마지막 서비스가 결과를
  반환할 수 있어 처리량이 높아지고 병목 지점이 줄기** 때문이다. **정상 경로의 성능은 조율이
  없어 Epic Saga(sao)보다 빠를 수 있다** (12장, p.331).[^ford2021-hard-parts]
  - **대신 오류 조건은 중재자 없이 훨씬 느려진다** — 각 서비스가 **호출 사슬을 되감아야 하고**,
    그것이 **서비스 사이의 결합도 올린다** (12장, p.331).[^ford2021-hard-parts]
  - **결합 특이점이라는 낱말이 이 자리에서 나온다** (12장, p.332):[^ford2021-hard-parts]

    > A nice feature of nonorchestrated architectures is the lack of a coupling singularity, a
    > single place the workflow couples to. […] In general, reducing coupling increases scale.

    - 가운데 생략(`[…]`)은 이 KB의 편집이고, 생략한 두 문장은 **동기 요청을 쓰더라도 정상 경로의
      대기 조건이 적어 더 높은 확장이 가능하다**는 설명이다.
- **드문 조합이라는 것을 저자들이 명시한다** (12장, p.332):[^ford2021-hard-parts]

  > The Phone Tag Saga<sup>(sac)</sup> has a fairly rare combination of features—generally, if
  > an architect chooses *choreography*, they also choose *asynchronicity*.

  - **그런데도 이 조합을 고를 사정으로 저자들이 드는 것**은 **동기 호출이 각 도메인 서비스가
    다음을 부르기 전에 자기 몫을 끝내도록 보장해 경쟁 조건을 없앤다**는 것이다. 그리고 **오류
    조건이 풀기 쉽거나 도메인 서비스가 멱등성(idempotence)과 재시도(retries)를 쓸 수 있으면
    Epic Saga(sao)보다 더 높은 병렬 확장을 지을 수 있다** (12장, p.332).[^ford2021-hard-parts]
    - 원문의 그 문장은 `However, in some cases where an architect might choose this
      combination instead:`로 시작해 주절 없이 콜론으로 이어진다 (12장,
      p.332).[^ford2021-hard-parts] 두 추출기와 렌더가 모두 같은 문장을 낸다.
  - **이 장에서 멱등성과 재시도를 부르는 자리는 여기 하나뿐이다** — 두 추출기로 확인했고,
    저자들이 그 둘의 기제를 이 장에서 설명하지 않는다. 그 전문은
    [견고함 패턴 목록](stability-patterns.md)에 있다.
- **채점 넷의 근거** (12장, pp.332–333):[^ford2021-hard-parts]
  - **결합** — Epic Saga(sao)의 결합 차원 하나를 느슨하게 한 것이라 **약간 덜 결합**되지만,
    **같은 트랜잭션 요구가 남아 워크플로의 복잡도가 도메인 서비스들 사이로 분산되어야 한다.**
  - **복잡도** — **Epic Saga(sao)보다 현저히 복잡하다.** 이 패턴의 복잡도는 **워크플로의 의미적
    복잡도에 선형 비례해 오른다** — 워크플로가 복잡할수록 오케스트레이터가 없는 것을 메우려
    **각 서비스에 더 많은 로직**이 들어가야 하기 때문이다.
    - 대안으로 **메시지 자체에 워크플로 정보를 실어 스탬프 결합(stamp coupling)의 한 형태로
      상태를 유지하는 길**을 저자들이 든다. 그러면 **각 서비스가 져야 할 맥락 오버헤드가
      늘어난다** (12장, p.332).[^ford2021-hard-parts] 저자들은 그 규정을 13장 p.378로 넘긴다.
  - **응답성과 가용성** — 오케스트레이션이 적으면 대체로 응답성이 낫지만, **이 패턴에서는 오류
    조건을 오케스트레이터 없이 모델링하기가 더 어려워** 콜백과 그 밖의 시간 잡아먹는 활동으로
    더 많은 조율이 필요하다.
  - **확장성과 탄력성** — 오케스트레이션이 없으니 병목이 줄어 확장성이 대체로 오르지만
    **아주 조금뿐이다.** 이 패턴은 **여전히 세 차원 중 둘에서 단단히 결합**하므로 확장성이
    강점이 못 되고, **오류 조건이 잦으면 특히 그렇다.**
- **표 12-3의 행과 값을 그대로 옮긴다** (12장, p.333):[^ford2021-hard-parts]

| Phone Tag Saga<sup>(sac)</sup> | Ratings |
|---|---|
| Communication | Synchronous |
| Consistency | Atomic |
| Coordination | Choreographed |
| Coupling | High |
| Complexity | High |
| Responsiveness/availability | Low |
| Scale/elasticity | Low |

- **언제 쓰는가** — **흔한 오류 조건이 많지 않은 단순한 워크플로에 더 낫다.** 저자들이 절을
  닫으며 적는 판정은 **Epic Saga(sao)보다 나은 특성을 몇 개 주지만 오케스트레이터가 없어서
  생기는 복잡도가 그 이점의 상당수를 상쇄한다**는 것이다 (12장, p.333).[^ford2021-hard-parts]

## Fairy Tale Saga(seo) - 원자성만 놓기

- **이름의 유래가 절의 첫 문장이다** — **전형적인 동화는 따라가기 쉬운 줄거리의 행복한 이야기를
  주고, 그래서 이 이름**이다. 동기 통신·최종 일관성·오케스트레이션을 쓴다 (12장,
  p.333).[^ford2021-hard-parts]
- **무엇이 달라지는가** — 이 통신 패턴은 **까다로운 원자성 요구를 느슨하게 하고**, 그것이
  아키텍트에게 체계를 설계할 선택지를 훨씬 많이 준다. 저자들이 드는 예 — **서비스가 일시적으로
  내려가 있으면 최종 일관성 덕분에 그 서비스가 돌아올 때까지 변경을 캐싱해 둘 수 있다** (12장,
  p.334).[^ford2021-hard-parts]
- **오케스트레이터가 남되 트랜잭션은 관리하지 않는다** (12장, p.334):[^ford2021-hard-parts]
  - **오케스트레이터가 요청·응답·오류 처리를 조율하려고 존재한다.**
  - **그러나 오케스트레이터는 트랜잭션 관리의 책임을 지지 않고, 그 책임은 각 도메인 서비스가
    계속 갖는다.**
  - 그래서 **오케스트레이터가 보상 호출을 관리할 수는 있되 활성 트랜잭션 안에서 일어나야 한다는
    요구는 없다.**
  - 도판이 그 배치를 그대로 보인다 — **점선 트랜잭션 경계가 도메인 서비스마다 하나씩 따로
    둘러지고 중재자에는 경계가 없다** (12장, p.335, 그림 12-9).[^ford2021-hard-parts]
- **저자들의 평가가 이 칸에서 가장 호의적이다** — **훨씬 매력적인 패턴이고 많은 마이크로서비스
  아키텍처에 흔히 나타난다.** 중재자가 있어 워크플로 관리가 쉽고, 동기 통신은 둘 중 쉬운
  쪽이며, **최종 일관성이 가장 어려운 조율 도전을 없앤다 — 특히 오류 처리에서** (12장,
  p.335).[^ford2021-hard-parts]
- **가장 큰 이점의 규정** (12장, p.335):[^ford2021-hard-parts]

  > The biggest appealing advantage of the Fairy Tale Saga<sup>(seo)</sup> is the lack of
  > holistic transactions. Each domain service manages its own transactional behavior,
  > relying on eventual consistency for the overall workflow.

- **채점 넷의 근거** (12장, pp.335–336):[^ford2021-hard-parts]
  - **결합** — **높은 결합**이고 세 결합 구동 요인 중 둘(동기 통신과 오케스트레이션된 조율)이
    최대치다. **그러나 결합 복잡도의 더 나쁜 구동 요인인 트랜잭션성이 최종 일관성으로 바뀌며
    사라진다.** 오케스트레이터는 여전히 복잡한 워크플로를 관리해야 하되 **트랜잭션 안에서 해야
    한다는 제약이 없다.**
    - **저자들이 세 축을 동등하게 보지 않는다는 것이 이 문장에 드러난다** — 트랜잭션성이 결합
      복잡도의 **더 나쁜 구동 요인**이라고 명시한다. 세 축의 무게를 대소로 적는 자리는 이 장에서
      여기 하나뿐이다.
  - **복잡도** — **꽤 낮다.** 가장 편리한 선택지들(오케스트레이션·동기성)에 가장 느슨한
    제약(최종 일관성)이 붙었기 때문이고, 그래서 이름이 동화 사가다 — **행복한 결말의 단순한
    이야기.**
  - **응답성과 가용성** — 이 종류의 통신 양식에서 응답성이 대체로 낫다. **호출이 동기여도
    중재자가 진행 중인 트랜잭션에 대한 시간 민감 상태를 덜 담아도 되어 부하 분산이 더 잘
    되기** 때문이다. **다만 성능의 진짜 차이는 비동기성에서 온다**고 저자들이 덧붙이고 뒤의
    패턴들로 넘긴다.
  - **확장성과 탄력성** — **결합이 없으면 대체로 확장성이 오르고, 트랜잭션 결합을 없애면 각
    서비스가 더 독립적으로 확장할 수 있다.**
- **표 12-4의 행과 값을 그대로 옮긴다** (12장, p.336):[^ford2021-hard-parts]

| Fairy Tale Saga<sup>(seo)</sup> | Ratings |
|---|---|
| Communication | Synchronous |
| Consistency | Eventual |
| Coordination | Orchestrated |
| Coupling | High |
| Complexity | Very low |
| Responsiveness/availability | Medium |
| Scale/elasticity | High |

- **언제 쓰는가** — **아키텍트가 최종 일관성을 활용할 수 있다면 이 패턴은 꽤 매력적이다.**
  **쉬운 움직이는 부품들과 가장 적은 무서운 제약을 결합해 아키텍트들 사이에서 인기 있는
  선택**이 된다 (12장, p.336).[^ford2021-hard-parts]
- **"흔하다"는 말이 이 장에서 두 칸에 붙는다** — Epic Saga(sao)는 **널리 쓰이고 많은 아키텍트가
  기본으로 삼는다**(p.328)고 적히고, 이 칸은 **많은 마이크로서비스 아키텍처에 흔히
  나타나며**(p.335) **인기 있는 선택**(p.336)이라 적힌다. **저자들이 둘의 빈도를 견주지
  않는다** — 앞의 것은 익숙함 때문에 기본값이 된다는 진단이고 뒤의 것은 절충이 좋아서 골린다는
  평가라 재는 것이 다르다. #hypothesis

## Time Travel Saga(sec) - 둘 다 놓기

- **원자성도 오케스트레이터도 없는 칸이다** — 동기 통신과 최종 일관성을 쓰되 코레오그래피된
  워크플로다. 다시 말해 **중앙 중재자를 피하고 워크플로 책임을 참여 도메인 서비스들에 온전히
  얹는다** (12장, p.336).[^ford2021-hard-parts]
- **기제** — 각 서비스가 요청을 받아 행동을 수행하고 **다른 서비스로 요청을 전달한다.** 저자들이
  이 구조를 두 이름으로 잇는다 (12장, p.338):[^ford2021-hard-parts]

  > This architecture can implement the *Chain of Responsibility* design pattern or the
  > *Pipes and Filters* architecture style—any workflow with a one-way series of steps.

  - 도판에서 **점선 트랜잭션 경계가 서비스마다 하나씩 따로 둘러지고 중재자 상자가 아예 없다**
    (12장, p.337, 그림 12-11).[^ford2021-hard-parts] 이 장에서 경계가 서비스마다 따로 그려지는
    것은 최종 일관성 칸 둘뿐이다.
  - **각 서비스가 자기 트랜잭션성을 "소유"하므로 아키텍트는 워크플로의 오류 조건을 도메인
    설계 안으로 설계해 넣어야 한다** (12장, p.338).[^ford2021-hard-parts]
  - **코레오그래피 해법에는 워크플로 복잡도와 비례하는 복잡도 관계가 있다** — 중재자를 통한
    내장 조율이 없으니 **워크플로가 복잡할수록 코레오그래피가 어려워진다** (12장,
    p.338).[^ford2021-hard-parts]
- **이름의 유래가 일관성의 시간성이다** (12장, p.338):[^ford2021-hard-parts]

  > It is called Time Travel Saga<sup>(sec)</sup> because everything is decoupled from a time
  > standpoint: each service owns its own transactional context, making workflow consistency
  > temporally gradual—the state will become consistent over time based on the design of the
  > interaction.

- **어디에 잘 맞는가** — **높은 처리량이 이득이 되는 해법**에 이 패턴이 아주 잘 듣고, 저자들이
  드는 실물은 **"쏘고 잊는(fire and forget)" 양식의 워크플로** — **전자 데이터 반입(electronic
  data ingestion)·대량 트랜잭션** 따위다 (12장, p.338).[^ford2021-hard-parts]
  - **그러나 오케스트레이터가 없으므로 도메인 서비스들이 오류 조건과 조율을 스스로 다뤄야
    한다** (12장, p.338).[^ford2021-hard-parts]
  - **트랜잭션이 없다는 것이 워크플로 모델링을 쉽게 만들지만**, 오케스트레이터가 없다는 것은
    **각 도메인 서비스가 워크플로 상태와 정보의 대부분을 담아야 한다**는 뜻이다. **모든
    코레오그래피 해법이 그렇듯 워크플로 복잡도와 오케스트레이터의 유용성 사이에 직접적인 상관이
    있고**, 그래서 **이 패턴은 단순한 워크플로에 가장 알맞다** (12장,
    p.338).[^ford2021-hard-parts]
  - **결합이 없으니 확장성이 오르고, 더 확장성을 올릴 길은 비동기성뿐이다** — 저자들이 그
    도착지로 `Anthology Saga(aec)`를 가리킨다. **다만 이 패턴에는 전체를 아우르는 트랜잭션
    조율이 없으므로 아키텍트가 데이터를 맞추는 데 추가 노력을 들여야 한다** (12장,
    p.338).[^ford2021-hard-parts]
- **채점 넷의 근거** (12장, pp.338–339):[^ford2021-hard-parts]
  - **결합** — **중간(medium)** 구간이다. 오케스트레이터의 부재가 결합을 낮추고 **동기 통신으로
    남은 결합이 그것을 상쇄한다.** **모든 최종 일관성 패턴이 그렇듯 트랜잭션 결합의 부재가
    데이터 관심사 여럿을 덜어 준다.**
  - **복잡도** — **트랜잭션성의 상실이 복잡도를 낮춘다.** 이 패턴은 **준(準)특수 목적
    (quasi-special-purpose)**이고 **빠른 처리량과 한 방향 통신 아키텍처에 빼어나게 맞으며**,
    결합 수준도 그 양식과 잘 어울린다.
  - **응답성과 가용성** — **중간**이다. 앞서 적은 **목적에 맞춰 지은 체계에서는 꽤 높고 복잡한
    오류 처리에서는 꽤 낮다.** 오케스트레이터가 없으므로 **오류가 났을 때 각 도메인 서비스가
    최종 일관성을 되찾는 시나리오를 다뤄야 하고**, 그것이 **동기 호출과 함께 큰 오버헤드를
    일으켜 응답성과 성능에 영향을 준다.**
  - **확장성과 탄력성** — **극히 좋다.** 더 낫게 만들 길은 비동기성뿐이다.
- **표 12-5의 행과 값을 그대로 옮긴다** (12장, p.339):[^ford2021-hard-parts]

| Time Travel Saga<sup>(sec)</sup> | Ratings |
|---|---|
| Communication | Synchronous |
| Consistency | Eventual |
| Coordination | Choreographed |
| Coupling | Medium |
| Complexity | Low |
| Responsiveness/availability | Medium |
| Scale/elasticity | High |

- **언제 쓰는가** — 저자들이 이 칸을 **진입로(on-ramp)**로 자리매김한다. **더 복잡하지만 결국
  더 확장성 있는 `Anthology Saga(aec)` 패턴으로 가는 진입로**이고, 근거는 **아키텍트와 개발자가
  동기 통신 쪽을 추론하고 구현하고 디버깅하기 더 쉽다고 느낀다**는 것이다. 그래서 **이 패턴이
  충분한 확장성을 준다면 팀이 더 복잡하지만 더 확장성 있는 대안을 받아들일 필요가 없다** (12장,
  p.339).[^ford2021-hard-parts]

## 동기 쪽 네 칸을 한자리에 놓으면

- **동기 통신을 고정하고 나머지 두 축을 움직인 것이 위의 넷**이다. 그 넷의 채점을 나란히 놓으면
  저자들이 적지 않는 것이 몇 가지 보인다. 아래 관찰은 이 KB가 표 12-2~12-5를 맞대어 읽은 것이고
  원문에 그런 대조 절이 없다. #hypothesis
- **결합 값이 2장의 표 2-1과 넷 다 일치한다** — `Epic Saga(sao)`=very high · `Phone Tag
  Saga(sac)`=high · `Fairy Tale Saga(seo)`=high · `Time Travel Saga(sec)`=medium이다 (2장, p.41 ·
  12장, 표 12-2~12-5).[^ford2021-hard-parts] **9장·11장을 지나오는 동안 이 책 안에서 표류가
  없다.**
- **복잡도 칸이 결합 칸과 같은 방향으로 가지 않는다.** 가장 높게 결합된 `Epic Saga(sao)`의
  복잡도가 **Low**이고, 결합이 한 단계 낮은 `Phone Tag Saga(sac)`의 복잡도가 **High**다.
  - 저자들이 그 역전의 근거를 각각의 채점 산문에 적어 둔다 — 앞의 것은 **동기 호출이 경쟁 조건과
    교착을 없애 준다**는 것이고, 뒤의 것은 **오케스트레이터가 없어 그 로직이 서비스마다
    복제된다**는 것이다 (12장, pp.329·332).[^ford2021-hard-parts] **곧 이 장에서 복잡도를 올리는
    것은 결합 자체가 아니라 조율의 부재다.**
- **응답성과 가용성 칸에서 원자성이 경계가 된다** — 원자적인 둘(sao·sac)이 **Low**이고 최종
  일관성인 둘(seo·sec)이 **Medium**이다. 조율 축은 이 칸을 움직이지 못한다.
- **확장성과 탄력성 칸도 마찬가지로 일관성 축이 가른다** — 원자적인 둘이 Very low와 Low,
  최종 일관성인 둘이 둘 다 High다. **동기 통신을 고정한 이 네 칸에서 확장성을 실제로 움직이는
  것은 일관성 축이고 조율 축은 한 눈금 안쪽에서만 움직인다.**
- **저자들이 이 넷 가운데 무엇을 고르라고 적지 않는다.** 권장에 가장 가까운 문장은 Fairy Tale
  Saga(seo)의 **꽤 매력적**과 Epic Saga(sao)의 **가능하면 피하는 것이 최선**이다 (12장,
  pp.329·336).[^ford2021-hard-parts]

## 원자적이라는 낱말이 여기서 무엇인가

**이 KB가 물어 본 것**: Epic Saga(sao)는 동기·**원자적**·오케스트레이션 칸인데, 같은 책 9장은
**분산 트랜잭션이 ACID 성질을 지원하지 않는다**고 적는다. 이 장이 `sao`에 대해 원자성을
**달성한다**고 주장하는가.

- **주장하지 않는다.** 이 장은 시작하는 자리에서 **분산 트랜잭션에 원자성이 없다**는 9장의
  판정을 스스로 되풀이하며 p.263을 가리킨다 (12장, p.324).[^ford2021-hard-parts] 그 뒤 `sao`를
  설명하는 문장들에서 원자성은 언제나 **목표**나 **요구**이지 결과가 아니다.
  - **아키텍트의 목표**가 모놀리식 체계의 행동을 **흉내 내는(mimics)** 것이다 (12장, p.325).
  - 세 호출이 트랜잭션으로 일어나기를 **기대한다(expected to occur transactionally)** (12장,
    p.327).
  - **Epic Saga(sao)의 목표가 원자적 일관성이므로** 중재자가 보상 트랜잭션을 써야 한다 (12장,
    p.328).
  - 복잡도 채점의 근거가 **원자성의 요구(the requirement of atomicity)**다 (12장, p.329).
- **그래서 이 장에서 "atomic"은 일관성 축의 값이지 보장의 이름이 아니다.** 그 값이 뜻하는 것은
  **아키텍트가 원자성을 목표로 삼았다**는 것이고, 그것을 실제로 이루는 기제로 이 장이 대는 것은
  **보상 트랜잭션 하나**다. 그리고 그 기제에 저자들이 붙이는 평가는 **복잡한 문제와 도전과
  절충으로 가득 차 있다**와 **다양한 실패 양태와 경계 조건에 굴복한다**이다 (12장,
  pp.327·329).[^ford2021-hard-parts]
- **소스 안에서 모순이 없다.** 9장이 부정한 것은 **서비스들이 각자 커밋하는 업무 요청에 ACID가
  없다**는 것이고, 12장이 말하는 것은 **그 자리에 원자성을 목표로 얹으면 보상이라는 값을
  치른다**는 것이다. 두 문장은 같은 대상에 대한 서술이고 방향이 같다. `contradicts`를 걸지
  않았다.
- **트랜잭션 매니저나 2단계 커밋을 이 장의 앞 절반이 한 번도 부르지 않는다** — 두 추출기
  (`pdftext.py`·`pdftotext -layout`)로 확인했다. `sao`를 구현하는 길로 이 장이 대는 것은
  보상 트랜잭션이고, **`transaction manager`·`two-phase commit`·`XA`는 이 구간에 없다.**
  - 그래서 **이 칸을 XA나 2단계 커밋의 자리로 읽는 것은 이 책이 하는 말이 아니다.** 저자들이
    적는 것은 **그런 트랜잭션이 데이터베이스 선택을 제한하고 전설적인 실패 양태를 갖는다**는
    한 문장뿐이고 (12장, p.327), 그 문장도 프로토콜을 이름으로 부르지 않는다.
  - 이 KB 안에서 원자적 커밋 프로토콜을 쓰는 서비스 간 분산 트랜잭션은
    [XA 트랜잭션과 이종 분산 트랜잭션](../concepts/xa-transactions.md)과
    [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)이 갖는다. **그 어휘와 이 칸을 잇는 다리는
    이 KB의 읽기이지 이 책의 주장이 아니다.** #hypothesis

## 이어지는 페이지

- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — 세 축의 규정과 여덟 칸의 결합 강도표가
  사는 자리
- [오케스트레이션과 코레오그래피](orchestration-versus-choreography.md) — 조율 축 하나의 전문과
  코레오그래피에서 상태를 두는 선택지 셋
- [최종 일관성 패턴 셋](eventual-consistency-patterns.md) — 일관성 축의 최종 쪽을 서비스 사이
  기법으로 푸는 자리
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 통신 축의 전문
- [사가 패턴](saga-pattern.md) — 같은 낱말을 네 소스가 서로 다른 대상에 쓴다는 대조표
- [트랜잭션과 ACID](acid-transactions.md) — 원자성의 규정과 서비스를 가로지를 때 BASE가 된다는
  판정
- [분산 트랜잭션과 2단계 커밋](two-phase-commit.md) — 원자성을 프로토콜로 실제로 주려는 쪽
- [견고함 패턴 목록](stability-patterns.md) — 멱등성과 재시도의 기제
- [프로세스 매니저](../concepts/process-manager.md) — 오케스트레이터의 도메인 모델 쪽 이름
- [서비스 결합의 네 종류](../concepts/service-coupling-types.md) — 의미적 결합과 스탬프 결합이
  놓이는 자리
- [Sysops Squad 사례](sysops-squad-case.md) — 이 장의 사가 상자들이 사는 자리
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) — 이 축의 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, **12장 "Transactional Sagas"의
    앞 절반(pp.323–339)** — 여는 사가(p.323) · 장 도입부(pp.323–324) ·
    §"Transactional Saga Patterns"의 프레임(pp.324–325) · §"Epic Saga(sao) Pattern"(pp.325–330) ·
    §"Phone Tag Saga(sac) Pattern"(pp.330–333) · §"Fairy Tale Saga(seo) Pattern"(pp.333–336) ·
    §"Time Travel Saga(sec) Pattern"(pp.336–339). 그리고 대조를 위해 **2장
    §"Dynamic Quantum Coupling"(p.41)의 표 2-1**. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측).
    직인용은 전부 `pdftotext -layout` 추출로 문자 단위 대조했고, 줄바꿈 하이픈(U+2010)은 원래
    낱말로 이었으며 굽은 따옴표는 곧은 따옴표로 옮겼다. 원문이 위첨자로 조판한 세 글자 코드는
    `<sup>` 로 옮겼고, 산문에서는 `Epic Saga(sao)` 처럼 괄호로 적었다.
    **표 다섯(표 12-1 p.324 · 12-2 p.329 · 12-3 p.333 · 12-4 p.336 · 12-5 p.339)을
    `pdftoppm -r 160 -png` 로 렌더해 눈으로 대조하고 원문 행·열·값 그대로 옮겼다** — 이 장의
    채점표에는 6장·3장 같은 별점 글리프가 없고 전부 텍스트 레이어에 있다. 표 2-1도 같은 방식으로
    대조했다.
    **도판 열하나 가운데 그림 12-1(범례)만 배치와 라벨까지 옮겼다** — 본문이 그 라벨을 적지 않고
    이 장 전체가 그 기호 체계를 쓰기 때문이다. 정육면체 넷(그림 12-2·12-6·12-8·12-10)과 등각
    다이어그램 넷(12-3·12-5·12-7·12-9·12-11)과 성공 경로 도판(12-4)은 렌더해 읽되 **본문이 그
    도판에 대해 적는 것과, 본문이 적지 않는 것 둘(정육면체의 축 라벨 `Choreography`, 등각
    다이어그램에서 점선 트랜잭션 경계가 전체를 두르는지 서비스마다 따로 둘러지는지)만** 옮겼다.
    **이 구간에 코드 목록이 하나도 없다** — 11장·10장과 같다.
    원문 오식 둘을 그대로 옮기고 표시했다 — p.328의 `(from a possibly a wide variety of both
    domain and operational reasons)`(관사 중복)와 p.332의 `However, in some cases where an
    architect might choose this combination instead:`(주절 없는 문장). 둘 다 두 추출기와 렌더가
    같은 문장을 낸다. 표 2-1과 표 12-1이 **같은 캡션으로 열 하나(Coupling)와 대소문자가 다르다**는
    것도 두 쪽을 렌더해 확인한 실측이다.
    저자들이 이 구간에서 대는 바깥 서지 — 1987년 ACM 회의록의 사가 논문, Chris Richardson
    *Microservices Patterns*(Manning)와 그의 웹사이트 §"Saga Pattern", 13장 p.378의 스탬프 결합,
    p.358의 사가 상자 — 는 **이 KB가 확인한 원전이 아니거나 이 구간 밖이다.**
    §"동기 쪽 네 칸을 한자리에 놓으면"의 대조와 §"원자적이라는 낱말이 여기서 무엇인가"의 판정은
    **원문에 그런 절이 없고 이 KB가 표와 문장을 맞대어 세운 것**이다. 그 판정의 재료가 되는 9장
    문장(`distributed transactions do not support ACID properties`, pp.265–266)의 전문은
    [트랜잭션과 ACID](acid-transactions.md)가 갖는다.

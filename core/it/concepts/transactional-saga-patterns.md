---
type: concept
title: 트랜잭셔널 사가 패턴
description: 통신·일관성·조율 세 축의 여덟 조합에 각각 패턴 이름을 붙이고 그 하나하나를 기제와 절충으로 펴는 자리 — 여덟 이름과 세 글자 코드의 규칙, 등각 다이어그램이라는 조판 약속과 그 범례, 패턴마다 매겨지는 채점 축 넷(결합·복잡도·응답성과 가용성·확장성과 탄력성)과 다섯 눈금, 동기 쪽 네 칸 — 모놀리스를 흉내 내며 보상 트랜잭션으로 원자성을 노리는 Epic Saga(sao), 조율자 없이 원자성을 지키려다 프런트 컨트롤러를 낳는 Phone Tag Saga(sac), 원자성만 놓고 오케스트레이터는 남겨 절충이 가장 고른 Fairy Tale Saga(seo), 둘 다 놓고 한 방향 파이프라인이 되는 Time Travel Saga(sec) — 의 기제와 원문 채점표와 언제 쓰는가, 여덟 전부의 채점을 한 표로 모아 읽은 대조(복잡도 눈금이 어려운 값의 개수와 같다는 것), 이 장이 "원자적"이라는 낱말을 보장이 아니라 목표로 쓴다는 판정, 그리고 오류가 났을 때의 두 길 — 보상 갱신과 상태 관리 — 과 사가 상태 기계와 애너테이션으로 사가를 문서화하는 기법
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
- [비동기 쪽 네 칸은 형제 페이지에 있다](#비동기-쪽-네-칸은-형제-페이지에-있다)
- [여덟 칸을 한자리에 놓으면](#여덟-칸을-한자리에-놓으면)
- [원자적이라는 낱말이 여기서 무엇인가](#원자적이라는-낱말이-여기서-무엇인가)
- [상태 관리와 최종 일관성](#상태-관리와-최종-일관성)
- [사가 상태 기계](#사가-상태-기계)
- [사가를 관리하는 기법 - 애너테이션과 코드 워크 도구](#사가를-관리하는-기법---애너테이션과-코드-워크-도구)
- [책의 사례 - 원자적 트랜잭션과 보상 갱신](#책의-사례---원자적-트랜잭션과-보상-갱신)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **통신·일관성·조율을 어떻게 고르느냐에 따라 서비스를 가로지르는 업무 요청이
어떤 모양이 되고, 그 모양마다 무엇을 얻고 무엇을 내주는가.**

세 축 자체의 규정과 여덟 칸의 결합 강도표는
[아키텍처 퀀텀](../concepts/architectural-quantum.md)이 갖고, 조율 축 하나의 전문은
[오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md)가, 일관성 축 하나의
전문은 [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md)이 갖는다. 여기 있는 것은
**세 축을 곱한 칸 하나하나**다.

**통신 축이 비동기인 네 칸은 형제 페이지
[트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md)에 있다.**
아래의 프레임 넷과 여덟 전부의 대조표, 그리고 오류를 다루는 두 길과 상태 기계와 사가 관리
기법은 여덟 모두에 걸리므로 이 페이지에 남는다.

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
    [트랜잭션과 ACID](../concepts/acid-transactions.md)와
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
    [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md)에 있다.
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
    [견고함 패턴 목록](../concepts/stability-patterns.md)에 있다.
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

## 비동기 쪽 네 칸은 형제 페이지에 있다

- **통신 축을 비동기로 바꾼 네 칸** — `Fantasy Fiction Saga(aao)` · `Horror Story(aac)` ·
  `Parallel Saga(aeo)` · `Anthology Saga(aec)` — 의 기제와 원문 채점표와 쓸 자리는
  [트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md)이 갖는다.
  위의 프레임 넷(세 축과 여덟 칸 · 이름과 세 글자 코드 · 등각 다이어그램과 그 범례 · 채점 축
  넷과 다섯 눈금)은 여덟 전부를 덮으므로 그 페이지가 되풀이하지 않는다.
- **가른 자리는 통신 축이다.** 아래 §[여덟 칸을 한자리에 놓으면](#여덟-칸을-한자리에-놓으면)이
  여덟 전부의 채점을 한 표로 모으므로, 대조는 이 페이지에 남는다.

## 여덟 칸을 한자리에 놓으면

- **여덟 채점표(표 12-2~12-9)의 값을 한 표로 모은다.** 값은 원문 그대로이고, 모으는 조판은 이
  KB의 것이다 — **원문에 여덟을 나란히 놓는 표가 없다** (12장, 표
  12-2~12-9).[^ford2021-hard-parts]

| 패턴 | 통신 | 일관성 | 조율 | Coupling | Complexity | Responsiveness/availability | Scale/elasticity |
|---|---|---|---|---|---|---|---|
| Epic Saga<sup>(sao)</sup> | Synchronous | Atomic | Orchestrated | Very high | Low | Low | Very low |
| Phone Tag Saga<sup>(sac)</sup> | Synchronous | Atomic | Choreographed | High | High | Low | Low |
| Fairy Tale Saga<sup>(seo)</sup> | Synchronous | Eventual | Orchestrated | High | Very low | Medium | High |
| Time Travel Saga<sup>(sec)</sup> | Synchronous | Eventual | Choreographed | Medium | Low | Medium | High |
| Fantasy Fiction Saga<sup>(aao)</sup> | Asynchronous | Atomic | Orchestrated | High | High | Low | Low |
| Horror Story<sup>(aac)</sup> | Asynchronous | Atomic | Choreographed | Medium | Very high | Low | Medium |
| Parallel Saga<sup>(aeo)</sup> | Asynchronous | Eventual | Orchestrated | Low | Low | High | High |
| Anthology Saga<sup>(aec)</sup> | Asynchronous | Eventual | Choreographed | Very low | High | High | Very high |

- 아래 관찰은 이 KB가 이 표를 읽은 것이고 **원문에 그런 대조 절이 없다.** #hypothesis
- **결합 값이 2장의 표 2-1과 여덟 다 일치한다** — very high · high · high · medium · high ·
  medium · low · very low 순으로 두 표가 같다 (2장, p.41 · 12장, 표
  12-2~12-9).[^ford2021-hard-parts] **열 장을 지나오는 동안 이 책 안에서 결합 값의 표류가 없다.**
  12장이 2장의 표를 다시 실으면서 뺀 `Coupling` 열이 여덟 칸의 채점표로 온전히 되돌아온다.
- **복잡도 채점은 "어려운 값"의 개수와 정확히 같다.** 세 축에서 어려운 쪽을 각각 하나씩 세면 —
  일관성의 `Atomic`, 통신의 `Asynchronous`, 조율의 `Choreographed` — 그 개수가 복잡도 눈금과
  여덟 칸 모두에서 맞아떨어진다.

| 어려운 값의 개수 | 칸 | Complexity |
|---|---|---|
| 0 | `seo` | Very low |
| 1 | `sao` · `sec` · `aeo` | Low |
| 2 | `sac` · `aao` · `aec` | High |
| 3 | `aac` | Very high |

  - **저자들이 이 산수를 어디에도 적지 않는다.** 칸마다 복잡도의 근거를 산문으로 따로 대고, 그
    산문들이 결과적으로 같은 셈을 한다 — `sac`은 원자성과 코레오그래피, `aao`는 원자성과
    비동기, `aec`는 비동기와 코레오그래피, `aac`는 셋 다다. #hypothesis
  - **그래서 앞 런이 동기 쪽 네 칸만 보고 세운 읽기("복잡도를 올리는 것은 조율의 부재다")는
    여덟을 다 보면 좁다.** 조율의 부재는 셋 가운데 하나일 뿐이고, **셋이 같은 무게로 복잡도를
    올린다.**
- **결합에서는 조율 축이 언제나 정확히 한 눈금만 움직인다.** 다른 두 축을 고정하고 조율만
  바꾸면 네 자리 모두 한 눈금이다(`sao`→`sac` · `seo`→`sec` · `aao`→`aac` · `aeo`→`aec`).
  - **통신 축과 일관성 축은 서로의 값에 따라 폭이 달라진다** — 일관성이 `Atomic`이면 통신을
    바꿔도 한 눈금이고 `Eventual`이면 두 눈금이며, 통신이 `Synchronous`면 일관성을 바꿔도 한
    눈금이고 `Asynchronous`면 두 눈금이다.
  - 곧 **결합을 크게 떨어뜨리려면 두 축을 함께 풀어야 하고**, 하나만 풀면 아직 조여 있는 다른
    축이 그 효과를 절반으로 깎는다. 저자들이 `seo` 절에서 **트랜잭션성이 결합 복잡도의 더 나쁜
    구동 요인**이라고 적었는데(12장, p.335), **표에서 일관성 축과 통신 축의 폭은 서로 같다.**
    저자들이 통신 축의 무게를 따로 적지 않는다.
- **응답성과 가용성 칸은 일관성 축이 혼자 가른다.** 원자적인 넷(`sao`·`sac`·`aao`·`aac`)이
  **예외 없이 Low**이고, 최종 일관성인 넷은 동기면 Medium(`seo`·`sec`), 비동기면
  High(`aeo`·`aec`)다.
  - **곧 비동기성은 일관성이 이미 최종일 때만 응답성을 올린다** — 원자적인 칸에서는 동기를
    비동기로 바꿔도 한 눈금도 움직이지 않는다. **저자들이 `seo` 절에서 "성능의 진짜 차이는
    비동기성에서 온다"고 적고 뒤의 칸들로 확인을 넘겼는데**(12장, p.336), 표가 주는 답은
    **조건부로 그렇다**이다. #hypothesis
- **확장성과 탄력성 칸은 일관성 축이 두세 눈금, 통신과 조율은 많아야 한 눈금 움직인다.**
  원자적에서 최종으로 바꾸면 `sao`→`seo`가 세 눈금(Very low→High)이고 나머지 셋은 두 눈금이다.
- **네 축 모두에서 나쁜 값이 하나도 없는 칸은 `Parallel Saga(aeo)` 하나다** — 결합 Low ·
  복잡도 Low · 응답성 High · 확장성 High다. `aec`는 확장에서 최고지만 복잡도가 High이고,
  `seo`는 복잡도가 최저지만 결합이 High다.
  - **저자들이 "가장 좋은 칸"을 적지 않는다.** 권장에 가장 가까운 것은 `aeo`의 **여러 시나리오에
    매력적인 절충 집합**(p.348)과 `seo`의 **꽤 매력적**(p.336), 그리고 `sao`의 **가능하면 피하는
    것이 최선**(p.329)이다.
  - **저자들이 다른 칸에서 탈출구로 지목하는 칸도 그 둘이다** — `aao`가 두 번 `aeo`로(p.342),
    `aac`가 한 번 `aec`로(p.344), 그리고 닫는 사가가 `sao`를 `seo`나 `aeo`로 보낸다(p.364).
    **여덟 칸 사이의 화살표가 전부 최종 일관성 쪽으로 향한다.**
- **한 칸에만 쓸 자리가 적히지 않는다** — `Horror Story(aac)`다. 나머지 일곱은 "언제 쓰는가"에
  해당하는 문장을 적어도 하나 갖는다.

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
- **이 칸과 2단계 커밋의 대응은 여기 두지 않았다.** 이 장이 `transaction manager`·
  `two-phase commit`·`XA`를 어디서 어떻게 부르는지(그리고 부르지 않는지)의 전수 실측과 그
  판정은 [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)의
  §"Epic Saga와 2PC — 어느 칸에 무엇이 사는가"가 갖는다.

## 상태 관리와 최종 일관성

- **여덟 칸 다음에 오는 물음은 오류가 났을 때 무엇을 하는가이고, 이 장이 답을 둘로 놓는다** —
  **보상 갱신을 쓰는 원자적 분산 트랜잭션**과 **상태 관리를 쓰는 최종 일관성**이다 (12장,
  p.350).[^ford2021-hard-parts] 앞의 것은 Epic Saga(sao) 절과 아래 사가 상자가 갖고, 이 절이
  뒤의 것을 편다.
- **규정** (12장, p.351):[^ford2021-hard-parts]

  > State management and eventual consistency leverage *finite state machines* (see "Saga
  > State Machines" on page 352) to always know the current state of the transactional saga,
  > and to also eventually correct the error condition through retries or some sort of
  > automated or manual corrective action.

  - 곧 **유한 상태 기계(finite state machine)로 사가의 현재 상태를 언제나 알고**, 오류는
    **재시도나 자동·수동 교정 행동으로 결국 바로잡는다**는 것이다.
- **저자들이 이 접근을 보이는 데 쓰는 칸이 `Fairy Tale Saga(seo)`다** — 동기·최종 일관성·
  오케스트레이션 칸의 티켓 완료 예다 (12장, p.351, 그림 12-20).[^ford2021-hard-parts]
  - **장면** — 분산 트랜잭션이 도는 동안 **설문 서비스(Survey Service)가 가용하지 않다.** 이
    종류의 사가에서는 **보상 갱신을 내는 대신 사가의 상태를 `NO_SURVEY`로 바꾸고 성공 응답을
    Sysops 전문가에게 보낸다.** 그러고 나서 **티켓 오케스트레이터 서비스가 배경에서 비동기로
    돌며 재시도와 오류 분석으로 프로그램이 오류를 풀고**, 그래도 풀지 못하면 **관리자나
    감독자에게 오류를 보내 수동 수리와 처리를 맡긴다** (12장, p.352).[^ford2021-hard-parts]
  - **무엇이 달라지는가의 판정** — **보상 갱신을 내는 대신 사가의 상태를 관리하면, 최종 사용자
    (여기서는 Sysops Squad 전문가)는 설문이 고객에게 가지 않았다는 것을 걱정할 필요가 없다 —
    그 책임은 티켓 오케스트레이터 서비스가 걱정할 몫이다.** 그래서 **최종 사용자 관점에서
    응답성이 좋고, 오류가 체계에 의해 처리되는 동안 사용자는 다른 일을 할 수 있다** (12장,
    p.352).[^ford2021-hard-parts]
    - 원문 오식 하나가 그 문장에 있다 — `from the end user's perpective`(perspective) (12장,
      p.352).[^ford2021-hard-parts] 두 추출기와 렌더가 같은 낱말을 낸다.
- **둘 사이의 고름은 상황과 절충 분석에 달렸고, 무엇을 쓰든 상태는 알려지고 관리되어야 한다**
  (12장, p.355):[^ford2021-hard-parts]

  > The choice between using compensating updates or state management for distributed
  > transaction workflows depends on the situation as well as trade-off analysis between
  > responsiveness and consistency. Regardless of the technique used to manage errors within a
  > distributed transaction, the state of the distributed transaction should be known and also
  > managed.

- **표 12-11(절충 상자)의 열과 값을 그대로 옮긴다** — 보상 갱신을 쓰는 원자적 분산 트랜잭션
  대신 상태 관리를 쓸 때의 절충이다 (12장, p.356, 절충 상자):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| Good responsiveness | Data may be out of sync when errors occur |
| Less impact to end user for errors | Eventual consistency may take some time |

  - **이 표의 두 열이 정확히 맞바꿈이다** — 얻는 것이 **응답성**이고 내주는 것이 **정합성의
    시간**이다. 아래 표 12-12(보상 갱신 쪽)와 나란히 놓으면 **이점 둘 대 단점 둘**과
    **이점 둘 대 단점 넷**이라 저자들의 무게가 한쪽으로 기운다. #hypothesis 저자들이 두 표를
    맞대어 세지 않는다.

## 사가 상태 기계

- **상태 기계의 규정** (12장, p.352):[^ford2021-hard-parts]

  > A *state machine* is a pattern that describes all of the possible paths that can exist
  > within a distributed architecture. A state machine always starts with a beginning state
  > that launches the transactional saga, then contains transition states and corresponding
  > action that should occur when the transition state happens.

  - **세 부분으로 이뤄진다** — 사가를 띄우는 **시작 상태**, **전이 상태들**, 그리고 **그 전이가
    일어날 때 수행되어야 할 대응 행동**이다.
- **저자들이 드는 예는 Sysops Squad의 새 문제 티켓 워크플로 여섯 단계다** (12장,
  p.353):[^ford2021-hard-parts] 고객이 새 문제 티켓을 넣고 → 티켓이 다음 가용한 전문가에게
  배정되고 → 전문가의 모바일 기기로 라우팅되고 → 전문가가 티켓을 받아 문제를 다루고 → 수리를
  마쳐 티켓을 완료로 표시하고 → 설문이 고객에게 간다.
  - **사가는 진입점인 `START` 노드에서 시작하고 종료점인 `CLOSED` 노드에서 끝난다** (12장,
    p.353).[^ford2021-hard-parts]
- **상태 일곱과 각각의 가능한 결과** (12장, pp.354–355):[^ford2021-hard-parts]
  - `START` — 고객이 새 문제 티켓을 넣으면서 시작한다. **고객의 지원 계약이 검증되고 티켓
    데이터가 유효성 검사를 받는다.** 티켓이 데이터베이스의 티켓 테이블에 들어가면 상태가
    `CREATED`로 옮겨 가고 고객에게 티켓 생성 성공이 통지된다. **가능한 결과가 이 하나뿐이고,
    이 상태 안에서 나는 어떤 오류도 사가가 시작되는 것을 막는다.**
  - `CREATED` — 티켓이 Sysops Squad 전문가에게 배정된다. **가용한 전문가가 없으면 있을 때까지
    대기 상태로 붙들린다.** 배정되면 `ASSIGNED`로 간다. **가능한 결과가 이 하나뿐이다.**
  - `ASSIGNED` — 유일하게 가능한 결과는 티켓을 전문가에게 라우팅하는 것이다. **전문가를 찾을 수
    없거나 가용하지 않아 라우팅되지 않으면 라우팅될 때까지 이 상태에 머문다.** 라우팅되면
    **전문가가 티켓 수신을 확인 응답해야 하고**, 그러면 `ACCEPTED`로 간다.
  - `ACCEPTED` — **결과가 둘이다.** 전문가가 수리를 마치고 완료로 표시하면 `COMPLETED`,
    **티켓이 잘못 배정됐거나 전문가가 수리를 마칠 수 없으면** 전문가가 체계에 알리고
    `REASSIGN`으로 간다.
  - `REASSIGN` — 체계가 티켓을 다른 전문가에게 재배정한다. `CREATED`와 마찬가지로 **전문가가
    없으면 배정될 때까지 이 상태에 머문다.** 배정되면 `ASSIGNED`로 돌아가 **다른 전문가의 수락을
    기다린다.**
  - `COMPLETED` — **결과가 둘이다.** 설문이 고객에게 가면 `CLOSED`로 가서 사가가 끝나고,
    **설문 서비스가 가용하지 않거나 설문을 보내는 중 오류가 나면** `NO_SURVEY`로 간다 —
    **문제는 고쳐졌으나 설문이 고객에게 가지 않았다는 표시**다.
  - `NO_SURVEY` — **오류 조건 상태**다. 체계가 **설문 보내기를 계속 시도하고**, 성공하면
    `CLOSED`로 가서 사가가 끝난다. **가능한 결과가 이 하나뿐이다.**
  - **일곱 가운데 넷(`CREATED`·`ASSIGNED`·`REASSIGN`·`NO_SURVEY`)이 "될 때까지 머문다"로
    적힌다** — 곧 **이 상태 기계에는 실패로 끝나는 종료 상태가 없다.** `START` 안의 오류만이
    사가를 아예 시작하지 못하게 한다. 저자들이 그 비대칭을 적지 않는다. #hypothesis
- **표로 만들라는 것이 이 절의 처방이다** — **가능한 모든 상태 전이와 그에 대응하는 전이 행동을
  표에 적어 두면 쓸모가 많고**, 개발자는 그 표로 **오케스트레이션 서비스(코레오그래피면 각
  서비스)에 전이 방아쇠와 가능한 오류 조건을 구현한다** (12장, p.355).[^ford2021-hard-parts]
- **표 12-10의 열 머리글과 값을 그대로 옮긴다** (12장, p.355):[^ford2021-hard-parts]

| Initiating state | Transition state | Transaction action |
|---|---|---|
| START | CREATED | Assign ticket to expert |
| CREATED | ASSIGNED | Route ticket to assigned expert |
| ASSIGNED | ACCEPTED | Expert fixes problem |
| ACCEPTED | COMPLETED | Send customer survey |
| ACCEPTED | REASSIGN | Reassign to a different expert |
| REASSIGN | ASSIGNED | Route ticket to assigned expert |
| COMPLETED | CLOSED | Ticket saga done |
| COMPLETED | NO_SURVEY | Send customer survey |
| NO_SURVEY | CLOSED | Ticket saga done |

- **표의 셋째 열과 그림 12-21의 화살표 라벨이 같은 것이 아니다.** 도판이 이미지 조판이라
  `pdftoppm -r 160 -png`로 렌더해 읽었고, 그림의 라벨은 아홉이 이렇다 — `START`→`CREATED`는
  **Create a new ticket**, `CREATED`→`ASSIGNED`는 **Assign to expert**, `ASSIGNED`→`ACCEPTED`는
  **Route to expert**, `ACCEPTED`→`COMPLETED`는 **Expert fixes problem**,
  `ACCEPTED`→`REASSIGN`은 **Expert cannot fix**, `REASSIGN`→`ASSIGNED`는
  **Assign to different expert**, `COMPLETED`→`CLOSED`는 **Send customer survey**,
  `COMPLETED`→`NO_SURVEY`는 **Survey not sent**, `NO_SURVEY`→`CLOSED`는
  **Customer survey sent**다 (12장, p.353, 그림 12-21).[^ford2021-hard-parts]
  - **그림은 전이를 일으킨 사건을 적고, 표는 그 전이 뒤에 수행할 행동을 적는다.** 그래서 둘이
    **한 칸씩 어긋나 보인다** — 그림의 `CREATED`→`ASSIGNED` 라벨(`Assign to expert`)이 표에서는
    `START`→`CREATED` 행의 행동으로 나타난다. 본문이 표를 **전이가 일어날 때 방아쇠가 당겨지는
    행동**이라고 적으므로 그 읽기가 맞고, **저자들이 두 조판의 차이를 적지 않는다.** #hypothesis
    그림만 보고 표를 읽으면 한 칸 밀려 읽힌다.
- **이 KB가 이것을 따로 페이지로 떼지 않은 이유** — 이 절의 상태 기계는 **분산 아키텍처 일반의
  유한 상태 기계 이론이 아니라 사가를 굴리는 기법**으로 규정되고 예도 하나뿐이다. 그래서 여덟
  칸과 같은 물음(서비스를 가로지르는 업무 요청을 어떤 모양으로 굴리는가) 아래 둔다. #hypothesis

## 사가를 관리하는 기법 - 애너테이션과 코드 워크 도구

- **먼저 무엇을 살 수 없는지가 적힌다** (12장, p.356):[^ford2021-hard-parts]

  > Distributed transactions are not something that can be simply "dropped into" a system.
  > They cannot be downloaded or purchased using some sort of framework or product like ACID
  > transaction managers—they must be designed, coded, and maintained by developers and
  > architects.

  - **이 책 전체에서 트랜잭션 매니저(transaction manager)라는 낱말이 나오는 자리가 여기 하나이고,
    그것도 부정문이다** — 두 추출기로 확인했다. **ACID 트랜잭션 매니저 같은 제품은 있으나 분산
    트랜잭션에는 그런 것이 없다**는 것이 이 문장의 주장이고, 그 대질의 전문은
    [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)에 있다.
- **저자들이 좋아하는 기법이 언어의 메타데이터 장치다** — **자바의 애너테이션(annotations),
  C#의 커스텀 어트리뷰트(custom attributes), 다른 언어의 비슷한 산물**을 쓴다. **그 언어
  산물들 자체에는 실제 기능이 하나도 없지만**, 체계 안의 트랜잭셔널 사가를 **프로그램으로
  포착하고 문서화하는 길**을 주고 **서비스를 사가에 결부시키는 수단**을 준다 (12장,
  p.356).[^ford2021-hard-parts]
  - **8장이 예고한 자리가 여기서 채워진다** — 8장은 서비스 진입점을 표시하는 애너테이션
    `@ServiceEntrypoint`를 두고 **그것이 서비스 종류·도메인·경계 컨텍스트 같은 다른 메타데이터
    애너테이션을 얹을 자리로 매우 쓸모 있다**고 적었다 (8장, p.222).[^ford2021-hard-parts]
    12장의 `@Saga`가 바로 그 얹는 것이다. 그 대표 펜스는
    [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md)이 갖는다.
- **구조** — 자바 애너테이션 `@Saga`는 `@Retention(RetentionPolicy.RUNTIME)`과
  `@Target(ElementType.TYPE)`을 달고 `Transaction[] value()` 하나를 갖는다. **사가의 이름들은
  그 안의 `Transaction` 이넘(enum)에 담기고**, 이 책의 예에서는 `NEW_TICKET`·`CANCEL_TICKET`·
  `NEW_CUSTOMER`·`UNSUBSCRIBE`·`NEW_SUPPORT_CONTRACT` 다섯이다 (12장, p.356, 예제
  12-1).[^ford2021-hard-parts]
  - **이넘 하나가 이 기법의 값이다** — 저자들이 대는 이유가 **응용 맥락 안에 존재하는 여러
    사가를 나열하고 문서화할 소스 코드 안의 단 한 자리를 준다**는 것이다 (12장,
    p.356).[^ford2021-hard-parts]
  - C# 판(예제 12-2)은 `[AttributeUsage(AttributeTargets.Class)]`를 단 `Saga` 클래스로 같은
    것을 적는다 — **같은 것의 다른 언어 판**이다 (12장, p.357).[^ford2021-hard-parts]
- **쓰는 법** — 서비스 진입점 클래스에 `@ServiceEntrypoint`와 `@Saga(...)`를 함께 단다. 이 책의
  예에서 `SurveyServiceAPI`는 `NEW_TICKET` 사가 하나에, `TicketServiceAPI`는 `NEW_TICKET`과
  `CANCEL_TICKET` 둘에 참여한다고 표시된다 (12장, p.357, 예제 12-3).[^ford2021-hard-parts]
  - **그 표시가 개발자에게 주는 것이 둘이다** — **특정 워크플로나 사가를 고칠 때의 테스트 범위를
    정하는 데 쓰이고**, **그 사가 안의 어떤 서비스를 고치면 어떤 다른 서비스가 영향을 받을지
    알려 준다** (12장, p.357).[^ford2021-hard-parts]
- **그 메타데이터 위에 도구를 얹는 것이 이 절의 마무리다** — 애너테이션과 어트리뷰트를 써서
  **아키텍트와 개발자가 코드베이스나 소스 저장소를 훑어 사가 정보를 실시간으로 내놓는 간단한
  명령줄(CLI) 도구를 쓸 수 있다.** 저자들이 드는 호출 모양이 `./sagatool.sh NEW_TICKET -services`
  이고, 그 출력이 `NEW_TICKET` 사가에 참여하는 서비스 넷(티켓·배정·라우팅·설문)의 목록이다
  (12장, p.358).[^ford2021-hard-parts]
  - **도구의 알고리즘도 한 문장으로 적힌다** — **응용 맥락의 각 클래스 파일에서
    `@ServiceEntrypoint`를 찾고, 그 클래스의 `@Saga`에 그 사가(`Transaction.NEW_TICKET`)가 있는지
    검사한다.** 저자들은 **이런 종류의 커스텀 도구가 쓰기 복잡하지 않다**고 적는다 (12장,
    p.358).[^ford2021-hard-parts]
  - **묻는 사람에 개발자와 아키텍트뿐 아니라 업무 분석가(business analyst)가 들어간다** — 곧
    이 도구가 겨냥하는 독자가 코드 바깥까지다. #hypothesis 저자들이 그 함의를 더 적지 않는다.
- **이 절의 코드 목록 셋을 펜스로 옮기지 않았다** — 사유는 각주에 적었고, 요지는 **이 책의
  애너테이션 대표 펜스가 8장 예제 8-1 하나로 이미 있고**(SCHEMA §3 개념당 하나) **예제 12-3에는
  복사해도 돌지 않는 원문 오식이 있다**는 것이다(`@Saga({Transaction.NEW_TICKET,)`에 닫는 괄호가
  잘못 들어 있다, 12장, p.357).[^ford2021-hard-parts] 애너테이션의 이름·리텐션·타깃·이넘 값은
  위에 인라인 코드로 남겼으므로 claim 은 보존된다.

## 책의 사례 - 원자적 트랜잭션과 보상 갱신

**이 장의 닫는 사가가 Epic Saga(sao)를 Sysops Squad의 티켓 완료 워크플로에 대입해 보상 갱신의
문제 셋을 보인다.** 장면은 **4월 5일 화요일 09:44**이고 수석 아키텍트 로건이 애디슨·오스틴에게
워크플로 도판을 놓고 설명하는 형식이다 (12장, pp.358–364, 사가).[^ford2021-hard-parts]

- **정상 경로 아홉 단계** — 전문가가 모바일 앱으로 티켓을 완료로 표시하면 티켓 오케스트레이터
  서비스가 **동기로** 받고 → 티켓 서비스에 **동기 요청**을 보내 상태를 `in-progress`에서
  `complete`로 바꾸게 하고 → 티켓 서비스가 테이블을 갱신하고 커밋하고 → **같은 과정의 일부로
  티켓 서비스가 티켓 정보(수리 시간·대기 시간·기간 따위)를 큐로 비동기 전송해 분석
  서비스(Analytics Service)가 집어 가게 하고** 오케스트레이터에 완료를 확인 응답하고 → 분석
  서비스가 비동기로 받아 처리를 시작하고 → 오케스트레이터가 설문 서비스에 **동기 요청**을 보내고
  → 설문 서비스가 설문 정보를 테이블에 넣고 커밋하고 → 설문을 이메일로 보내고 확인 응답을
  돌려주고 → 오케스트레이터가 전문가의 기기로 완료 응답을 보낸다 (12장, pp.359–360,
  사가).[^ford2021-hard-parts]
  - **원자적 칸인데 이 워크플로 안에 비동기 호출이 하나 섞여 있다**(4단계의 분석 서비스 전송).
    **그 하나가 아래 문제 셋 가운데 첫째를 만든다.**
- **문제 ① 격리가 없어 부작용이 남는다** — **분산 트랜잭션 안에는 트랜잭션 격리가 없으므로**
  (저자들이 9장 p.263을 가리킨다) **다른 서비스들이 분산 트랜잭션이 끝나기 전에 이미 그 데이터로
  행동했을 수 있다** (12장, p.360, 사가).[^ford2021-hard-parts]
  - 장면 — 설문 서비스가 가용하지 않아 **티켓 서비스에 보상 갱신이 가서 상태를 `completed`에서
    `in-progress`로 되돌린다.** 그런데 **원래 갱신의 일부로 티켓 정보가 이미 큐를 통해 분석
    서비스에 넘어가 처리되었다** (12장, p.360, 사가).[^ford2021-hard-parts]
  - **그 현상의 이름이 여기서 붙는다** (12장, p.361, 사가):[^ford2021-hard-parts]

    > We call this a *side effect* within distributed architectures. By reversing the
    > transaction in the Ticket Service, actions performed by other services using data from
    > the prior update may have already taken place and might not be able to be reversed.

  - **고칠 수는 있으나 값이 크다** — 티켓 서비스가 데이터 펌프를 통해 분석 서비스에 **앞선 티켓
    정보를 무시하라는 요청을 하나 더 보낼 수 있지만**, 그러려면 **분석 서비스 안에 얼마나 복잡한
    코드와 타이밍 로직이 필요할지 상상해 보라**고 적는다. 게다가 **이미 처리된 분석 데이터에
    하류 행동이 더 있었을 수 있어 되돌리고 바로잡을 사건의 사슬이 더 복잡해진다** (12장, p.361,
    사가).[^ford2021-hard-parts]
    - 로건이 그 상황에 붙이는 표현이 **거북이가 끝까지 내려간다(turtles all the way down)**이다
      (12장, p.361, 사가).[^ford2021-hard-parts]
- **문제 ② 최종 사용자가 업무 프로세스에 의미적으로 묶인다** — 원자적 분산 트랜잭션이라 보상 뒤에
  **전문가에게 실패 오류가 가고 다시 시도하라는 안내가 간다.** 로건이 묻는다 — **왜 Sysops Squad
  전문가가 설문이 안 나간 것을 걱정해야 하는가** (12장, p.360, 사가).[^ford2021-hard-parts]
  - **애디슨의 답이 그 물음의 답이다** — **전문가는 자기에게 배정된 다음 티켓으로 넘어가고 싶을
    뿐**이고, 오스틴은 **모놀리스에서는 그게 다 한 트랜잭션 안에서 일어났다**고 되짚는다 (12장,
    p.360, 사가).[^ford2021-hard-parts]
  - **로건의 판정** (12장, p.360, 사가):[^ford2021-hard-parts]

    > This is the issue with atomic distributed transactions—the end user is unnecessarily
    > semantically coupled to the business process.

    - **의미적 결합(semantic coupling)이라는 낱말이 이 책에서 최종 사용자에게 걸리는 자리는
      여기뿐이다** — 다른 자리에서는 업무 문제의 성질이거나 서비스 사이의 결합이다. #hypothesis
- **문제 ③ 보상이 실패한다** — **아키텍트와 개발자는 보상 갱신이 언제나 성공하리라고 가정하는
  경향이 있는데 때로 그렇지 않다** (12장, p.362, 사가).[^ford2021-hard-parts]
  - 장면 — 보상 갱신이 티켓 서비스에 가서 상태를 되돌리려는데 **티켓 서비스가 오류를 낸다.**
    그러면 **최종 사용자에게 어떤 응답을 보낼지가 혼란에 빠진다** — 보상이 실패해 **티켓 상태는
    이미 `complete`이므로 "완료로 표시" 요청을 다시 시도하면 또 다른 오류(`Ticket already marked
    as complete` 같은)가 날 뿐**이다 (12장, p.362, 사가).[^ford2021-hard-parts]
  - **개발자의 혼란을 설계 신호로 읽으라는 조항이 이 자리에 붙는다** — **개발자는 불완전하거나
    혼란스러운 아키텍처 해법에 대한 좋은 점검 장치인 경우가 많고, 그들이 혼란스러워한다면 그럴
    만한 좋은 이유가 있을 수 있다** (12장, p.362, 사가).[^ford2021-hard-parts]
- **문제 ④ 응답성** — 원자적 분산 트랜잭션과 그에 딸린 보상 갱신은 응답성에도 영향을 준다.
  **오류가 나면 최종 사용자는 보상 갱신으로 모든 시정 행동이 끝날 때까지 기다린 뒤에야 오류를
  알리는 응답을 받는다** (12장, p.362, 사가).[^ford2021-hard-parts]
  - **최종 일관성이 그것을 얼마나 고치는가에 저자들이 단서를 단다** — **보상 갱신을 최종
    일관성으로 비동기로 내면(`Parallel Saga(aeo)`나 `Anthology Saga(aec)`처럼) 응답성이 때로
    해결될 수 있지만, 그럼에도 대부분의 원자적 분산 트랜잭션은 보상 갱신이 끼면 응답성이 더
    나쁘다** (12장, p.363, 사가).[^ford2021-hard-parts]
- **표 12-12(절충 상자)의 열과 값을 그대로 옮긴다** (12장, p.363,
  사가):[^ford2021-hard-parts]

| Advantages | Disadvantages |
|---|---|
| All data restored to prior state | No transaction isolation |
| Allows retries and restart | Side effects may occur on compensation |
| | Compensation may fail |
| | Poor responsiveness for the end user |

  - **이점 칸 둘이 비어 행이 넷이다** — 원문의 조판이 그렇고 렌더로 확인했다. **이 책의 절충표
    가운데 두 열의 길이가 다른 자리다.**
- **보상 트랜잭션의 도전 둘을 등장인물들이 이름 붙인다** (12장, p.363,
  사가):[^ford2021-hard-parts]
  - **서비스가 롤백을 수행할 수 없다(a service cannot perform a rollback)** — 서비스 하나가 앞선
    오퍼레이션을 성공적으로 되돌리지 *못하면* 어떻게 되는가. **오케스트레이터가 트랜잭션이
    성공하지 못했음을 나타내는 조율 코드를 갖고 있어야 한다.**
  - **참여 서비스를 잠글 것인가 말 것인가(to lock or not lock participating services?)** —
    중재자가 한 서비스를 호출해 값을 갱신하고 워크플로의 다음 서비스들을 부르는 동안, **같은
    중재자에서든 다른 맥락에서든 첫 서비스에 대한 다른 요청이 첫 요청의 결말에 딸려 나타나면
    어떻게 되는가.** **이 문제는 호출이 동기가 아니라 비동기일 때 더 나빠지고**, 저자들이 그
    예로 `Phone Tag Saga(sac)` 절(p.330)을 가리킨다. 대안으로 **중재자가 워크플로가 도는 동안
    다른 서비스들이 호출을 받지 못하게 고집할 수 있으나, 그것은 유효한 트랜잭션을 보장하는 대신
    성능과 확장성을 파괴한다.**
- **장을 닫는 두 문장이 트랜잭션을 개념으로 되돌려 놓는다** (12장, pp.363–364,
  사가):[^ford2021-hard-parts]

  > Conceptually, transactions force participants to stop their individual worlds and
  > synchronize on a particular value. This is so easy to model with monolithic architectures
  > and relational databases that architects overuse transactions in those systems.

  - 이어지는 문장이 **현실 세계의 많은 부분이 트랜잭셔널하지 않다**는 것이고, 저자들이 그 관찰의
    출처로 **그레고르 호페(Gregor Hohpe)의 유명한 에세이 "Starbucks Does Not Use Two-Phase
    Commit"**을 든다. 그리고 **트랜잭션 조율은 아키텍처에서 가장 어려운 부분 가운데 하나이고
    범위가 넓을수록 더 나빠진다** (12장, p.364, 사가).[^ford2021-hard-parts]
    - **이 책 전체에서 "Two-Phase Commit"이라는 낱말이 나오는 유일한 자리다** — 그 인용을 이 KB가
      어떻게 다루는지는 [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)에 있다.
- **그래서 대안이 무엇인가로 장이 끝난다** — 애디슨이 **Epic Saga 말고 대안이 있느냐**고 묻고,
  로건이 **`Fairy Tale Saga(seo)`나 `Parallel Saga(aeo)`**를 든다. 근거는 **그 사가들이 오류가
  났을 때 보상 갱신을 쓰는 원자적 분산 트랜잭션 대신 비동기 최종 일관성과 상태 관리에 기대고**,
  그래서 **오류가 최종 사용자 개입 없이 배경에서 처리되어 사용자가 덜 영향을 받으며**, **사용자가
  시정 행동을 기다릴 필요가 없어 응답성도 낫다**는 것이다 (12장, p.364,
  사가).[^ford2021-hard-parts]
  - **이 사가가 여덟 칸 가운데 셋만 이름으로 부른다** — `sao`(문제의 대상)와 `seo`·`aeo`(권하는
    대안)이고, `aec`는 응답성 단서에서 한 번 더 나온다. **닫는 사가가 권하는 칸과 본문이 가장
    호의적으로 적은 칸이 겹친다.**
  - **12장에는 ADR 상자가 없다** — 부록 B의 ADR 목록이 11장 p.321 다음에 곧바로 13장 p.380으로
    건너뛴다 (부록 B, pp.419–420).[^ford2021-hard-parts] **이 장은 여덟 칸이라는 선택 공간을
    가장 크게 벌려 놓고도 Sysops Squad를 위한 결정을 하나도 기록하지 않는다.** 저자들이 그
    부재를 적지 않는다. #hypothesis 그 목록의 전문은
    [아키텍처 결정 기록](../concepts/architecture-decision-records.md)에 있다.

## 이어지는 페이지

- [트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md) — 이
  페이지의 형제. 통신 축이 비동기인 네 칸의 기제와 원문 채점표와 쓸 자리
- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — 세 축의 규정과 여덟 칸의 결합 강도표가
  사는 자리
- [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) — 조율 축 하나의 전문과
  코레오그래피에서 상태를 두는 선택지 셋
- [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) — 일관성 축의 최종 쪽을 서비스 사이
  기법으로 푸는 자리
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 통신 축의 전문
- [사가 패턴](../concepts/saga-pattern.md) — 같은 낱말을 네 소스가 서로 다른 대상에 쓴다는 대조표
- [트랜잭션과 ACID](../concepts/acid-transactions.md) — 원자성의 규정과 서비스를 가로지를 때 BASE가 된다는
  판정
- [분산 트랜잭션과 2단계 커밋](two-phase-commit.md) — 원자성을 프로토콜로 실제로 주려는 쪽
- [견고함 패턴 목록](../concepts/stability-patterns.md) — 멱등성과 재시도의 기제
- [프로세스 매니저](../concepts/process-manager.md) — 오케스트레이터의 도메인 모델 쪽 이름
- [서비스 결합의 네 종류](../concepts/service-coupling-types.md) — 의미적 결합과 스탬프 결합이
  놓이는 자리
- [Sysops Squad 사례](../concepts/sysops-squad-case.md) — 이 장의 사가 상자들이 사는 자리
- [코드 재사용 패턴 넷](../concepts/code-reuse-patterns.md) — 이 장이 얹는 `@Saga` 애너테이션의 바탕이 되는
  `@ServiceEntrypoint`와 그 대표 펜스
- [아키텍처 결정 기록](../concepts/architecture-decision-records.md) — 이 책의 ADR 열셋과, 12장에 그것이
  하나도 없다는 자리
- [마이크로서비스 경계와 통신](../synthesis/microservice-boundaries-and-communication.md) — 이 축의 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, **12장 "Transactional Sagas"** —
    여는 사가(p.323) · 장 도입부(pp.323–324) · §"Transactional Saga Patterns"의 프레임
    (pp.324–325) · §"Epic Saga(sao) Pattern"(pp.325–330) · §"Phone Tag Saga(sac)
    Pattern"(pp.330–333) · §"Fairy Tale Saga(seo) Pattern"(pp.333–336) · §"Time Travel Saga(sec)
    Pattern"(pp.336–339) · §"State Management and Eventual Consistency"(pp.351–356, 하위 §"Saga
    State Machines" pp.352–355) · §"Techniques for Managing Sagas"(pp.356–358) · 사가 §"Atomic
    Transactions and Compensating Updates"(pp.358–364). **비동기 쪽 네 칸(pp.340–351)은 형제
    페이지 [트랜잭셔널 사가 패턴 - 비동기 네 칸](../concepts/transactional-saga-patterns-asynchronous.md)이
    갖고, 여기서는 여덟 대조표에 그 채점 값만 옮겼다.** 그리고 대조를 위해 **2장
    §"Dynamic Quantum Coupling"(p.41)의 표 2-1**과 **8장 p.222의 예제 8-1**과 **부록 B
    (pp.419–420)의 ADR 목록**. 쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측).
    직인용은 전부 `pdftotext -layout` 추출로 문자 단위 대조했고, 줄바꿈 하이픈(U+2010)은 원래
    낱말로 이었으며 굽은 따옴표는 곧은 따옴표로 옮겼다. 원문이 위첨자로 조판한 세 글자 코드는
    `<sup>` 로 옮겼고, 산문에서는 `Epic Saga(sao)` 처럼 괄호로 적었다.
    **표 아홉(표 12-1 p.324 · 12-2 p.329 · 12-3 p.333 · 12-4 p.336 · 12-5 p.339 · 12-10 p.355 ·
    12-11 p.356 · 12-12 p.363, 그리고 대조용 표 2-1 p.41)을 `pdftoppm -r 160 -png` 로 렌더해
    눈으로 대조하고 원문 행·열·값 그대로 옮겼다** — 이 장의 채점표에는 6장·3장 같은 별점 글리프가
    없고 전부 텍스트 레이어에 있다. 표 12-12는 **이점 칸 둘이 비어 두 열의 길이가 다르다**는 것도
    렌더로 확인했다.
    **도판 가운데 그림 12-1(범례)과 그림 12-21(상태 도표)만 배치와 라벨까지 옮겼다** — 앞은 본문이
    그 라벨을 적지 않고 이 장 전체가 그 기호 체계를 쓰기 때문이고, 뒤는 **그 라벨이 표 12-10의
    셋째 열과 다른 것을 적기 때문**이다. 정육면체 넷(그림 12-2·12-6·12-8·12-10)과 등각 다이어그램
    넷(12-3·12-5·12-7·12-9·12-11)과 성공 경로 도판(12-4)과 사가의 워크플로 도판 넷
    (12-20·12-22·12-23·12-24)은 렌더해 읽되 **본문이 그 도판에 대해 적는 것과, 본문이 적지 않는 것
    둘(정육면체의 축 라벨 `Choreography`, 등각 다이어그램에서 점선 트랜잭션 경계가 전체를
    두르는지 서비스마다 따로 둘러지는지)만** 옮겼다.
    **코드 목록 셋(예제 12-1 자바 애너테이션 · 12-2 C# 어트리뷰트 · 12-3 사용 예)을 펜스로 옮기지
    않았다** — 이 책의 애너테이션 대표 펜스는 8장 예제 8-1 하나로 유지하고(SCHEMA §3 개념당 하나),
    12-2는 12-1의 다른 언어 판이며, **12-3에는 `@Saga({Transaction.NEW_TICKET,)` 처럼 닫는 괄호가
    잘못 들어 있어 복사해도 돌지 않는다.** 애너테이션의 이름·리텐션·타깃·이넘 값 다섯과 도구의
    호출 모양은 인라인 코드로 남겼으므로 claim 은 보존되고 조판만 옮기지 않았다. 도구의 출력 예는
    실행할 것이 아니라 산문으로 적었다.
    원문 오식 여섯을 그대로 옮기거나 표시했다 — p.328의 `(from a possibly a wide variety of both
    domain and operational reasons)`(관사 중복) · p.332의 `However, in some cases where an
    architect might choose this combination instead:`(주절 없는 문장) · p.352의
    `from the end user's perpective`(perspective) · p.355의 `thus ending the transaction saga`와
    `This is the only possible outcome of this state transaction`(각각 transactional saga와 state
    transition) · p.358의 `in Figure 12-22 Can everyone see it?`(마침표 빠짐) · p.357의 예제 12-3
    괄호. 전부 두 추출기와 렌더가 같은 문장을 낸다.
    표 2-1과 표 12-1이 **같은 캡션으로 열 하나(Coupling)와 대소문자가 다르다**는 것도 두 쪽을
    렌더해 확인한 실측이고, **12장에 ADR 상자가 없다**는 것은 부록 B의 목록이 p.321 다음에
    p.380으로 건너뛴다는 실측이다. **이 장에 Summary 절이 없다**(6장부터 일곱 장 연속).
    저자들이 이 장에서 대는 바깥 서지 — 1987년 ACM 회의록의 사가 논문, Chris Richardson
    *Microservices Patterns*(Manning)와 그의 웹사이트 §"Saga Pattern", 13장 p.378의 스탬프 결합,
    그리고 p.364의 그레고르 호페 에세이 "Starbucks Does Not Use Two-Phase Commit" — 는 **이 KB가
    확인한 원전이 아니다.** 마지막 것의 다룸은
    [분산 트랜잭션과 2단계 커밋](two-phase-commit.md)이 갖는다.
    §"여덟 칸을 한자리에 놓으면"의 대조와 §"원자적이라는 낱말이 여기서 무엇인가"의 판정은
    **원문에 그런 절이 없고 이 KB가 표와 문장을 맞대어 세운 것**이다. 그 판정의 재료가 되는 9장
    문장(`distributed transactions do not support ACID properties`, pp.265–266)의 전문은
    [트랜잭션과 ACID](../concepts/acid-transactions.md)가 갖는다.

---
type: concept
title: 트랜잭셔널 사가 패턴 - 비동기 네 칸
description: 통신 축을 비동기로 고정한 사가 네 칸 — 오케스트레이터에 원자성까지 얹어 중재자가 진행 중인 모든 트랜잭션의 상태를 들어야 하는 Fantasy Fiction Saga(aao), 조율자 없이 원자성을 지키려다 서비스마다 되돌리기 정보를 들게 되는 여덟 중 최악의 조합 Horror Story(aac), Epic Saga에서 동기와 원자성 둘을 놓아 네 채점 축 어디에도 나쁜 값이 없는 Parallel Saga(aeo), 메시지 큐로만 이어져 결합이 가장 낮고 확장이 가장 높되 복잡한 워크플로에는 금지될 만큼 조율이 어려운 Anthology Saga(aec) — 각각의 기제와 원문 채점표와 언제 쓰는가, 그리고 이 넷이 앞 네 칸을 어떤 값으로 바꾸는가
generated: { by: "claude-opus-5", at: "2026-09-18T06:00:00Z" }
sources:
  - { id: ford2021-hard-parts, resource: /it/sources/ford2021-hard-parts.md }
  - { id: bellemare2025, resource: /it/sources/bellemare2025.md }
---

# 트랜잭셔널 사가 패턴 - 비동기 네 칸

- [Fantasy Fiction Saga(aao) - 비동기가 원자성을 만나면](#fantasy-fiction-sagaaao---비동기가-원자성을-만나면)
- [Horror Story(aac) - 여덟 중 가장 나쁜 조합](#horror-storyaac---여덟-중-가장-나쁜-조합)
- [Parallel Saga(aeo) - Epic에서 둘을 놓기](#parallel-sagaaeo---epic에서-둘을-놓기)
- [Anthology Saga(aec) - Epic의 정반대](#anthology-sagaaec---epic의-정반대)
- [다섯째 소스의 두 사가가 어느 칸에 앉는가](#다섯째-소스의-두-사가가-어느-칸에-앉는가)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **통신을 비동기로 고르고 나면 일관성과 조율의 네 조합이 각각 어떤 모양이 되고,
그 모양마다 무엇을 얻고 무엇을 내주는가.**

이 페이지는 [트랜잭셔널 사가 패턴](transactional-saga-patterns.md)의 형제다. **세 축과 여덟
칸이라는 프레임, 이름과 세 글자 코드의 규칙, 등각 다이어그램과 그 범례, 채점 축 넷과 다섯
눈금, 동기 쪽 네 칸, 그리고 여덟 전부를 한 표로 모은 대조**는 전부 그 페이지에 있다. 여기
있는 것은 **통신 축이 비동기인 네 칸**뿐이다.

## Fantasy Fiction Saga(aao) - 비동기가 원자성을 만나면

- **Epic Saga(sao)에서 통신 축 하나만 바꾼 것이다** — 원자적 일관성과 오케스트레이션된 조율은
  그대로 두고 **동기를 비동기로** 바꾼다. 저자들이 그 한 축의 차이를 명시한다 — **이 패턴은
  통신을 빼면 모든 면에서 Epic Saga(sao)를 닮았다** (12장, p.340).[^ford2021-hard-parts]
- **조합이 성립한다는 것이 그것이 매력적이라는 뜻은 아니라는 단서가 이 칸에 붙는다** (12장,
  p.340):[^ford2021-hard-parts]

  > Just because a combination of architectural forces exists doesn't mean it forms an
  > attractive pattern, yet this relatively implausible combination has uses.

  - **여덟을 다 정당한 쓰임이 있다고 적어 놓고 한 칸을 "비교적 있음직하지 않은
    (relatively implausible)"이라 부르는 자리**다. 앞의 네 칸에는 이런 유보가 붙지 않는다.
- **왜 아키텍트가 이쪽으로 가는가** — 전통적으로 아키텍트가 분산 체계의 응답성을 올리는 한
  방법이 **비동기성을 써서 오퍼레이션이 직렬이 아니라 병렬로 일어나게 하는 것**이고, 그래서
  이것이 **Epic Saga(sao)보다 체감 성능(perceived performance)을 올리는 좋은 길처럼 보인다**
  (12장, p.340).[^ford2021-hard-parts]
- **그러나 비동기성은 간단한 교체가 아니다** (12장, p.341):[^ford2021-hard-parts]

  > However, asynchronicity isn't a simple change—it adds many layers of complexity to
  > architecture, especially around coordination, requiring much more complexity in the
  > mediator.

  - 저자들이 드는 장면 — 트랜잭셔널 워크플로 *Alpha*가 시작하는데 모든 것이 비동기라 Alpha가
    pending인 동안 워크플로 *Beta*가 시작한다. 그러면 **중재자가 진행 중인 모든 트랜잭션의
    상태를 pending 상태로 추적해야 한다** (12장, p.341).[^ford2021-hard-parts]
  - **그리고 더 나빠진다** — 워크플로 *Gamma*가 시작하는데 도메인 서비스로 가는 첫 호출이
    **아직 pending인 Alpha의 결과에 의존한다면 아키텍트가 이 행동을 어떻게 모델링할 것인가.**
    가능하기는 하되 **복잡도가 자라고 또 자란다** (12장, p.341).[^ford2021-hard-parts]
- **이 칸이 더하는 것의 규정** (12장, p.341):[^ford2021-hard-parts]

  > Adding asynchronicity to orchestrated workflows adds asynchronous transactional state to
  > the equation, removing serial assumptions about ordering and adding the possibilities of
  > deadlocks, race conditions, and a host of other parallel system challenges.

  - **Epic Saga(sao)의 복잡도 채점이 "동기 호출이 아키텍트가 경쟁 조건과 교착을 걱정할 필요를
    없애 준다"였던 것**(12장, p.329)의 정확한 뒷면이다. 그 이점을 내놓는 것이 이 칸이 치르는
    값이고, **채점표에서 복잡도가 Low에서 High로 두 눈금 뛴다.**
- **채점 넷의 근거** (12장, p.342):[^ford2021-hard-parts]
  - **결합** — **극히 높다.** 오케스트레이터와 원자성을 쓰면서 통신이 비동기라 **조율이 더
    어려워진다** — 아키텍트와 개발자가 **경쟁 조건과, 비동기 통신이 강요하는 순서 어긋남
    (out-of-order) 문제**를 다뤄야 하기 때문이다.
  - **복잡도** — 결합이 그만큼 어려우니 복잡도도 오른다. **설계 복잡도**(지나치게 복잡한
    워크플로를 짜야 한다)뿐 아니라 **규모에서 비동기 워크플로를 다루는 디버깅 복잡도와 운영
    복잡도**가 있다.
  - **응답성과 가용성** — 호출을 가로질러 트랜잭션 조율을 시도하므로 응답성이 전반적으로
    영향을 받고, **서비스 하나 이상이 가용하지 않으면 극히 나쁘다.**
  - **확장성과 탄력성** — **트랜잭션 체계에서는 비동기성을 쓰더라도 높은 확장이 사실상
    불가능하다.** 확장은 **원자적을 최종 일관성으로 바꾼 닮은 패턴 `Parallel Saga(aeo)`** 쪽이
    훨씬 낫다.
- **표 12-6의 행과 값을 그대로 옮긴다** (12장, p.342):[^ford2021-hard-parts]

| Fantasy Fiction | Ratings |
|---|---|
| Communication | Asynchronous |
| Consistency | Atomic |
| Coordination | Orchestrated |
| Coupling | High |
| Complexity | High |
| Responsiveness/availability | Low |
| Scale/elasticity | Low |

  - **이 표의 머리글 칸만 세 글자 코드가 없다** — 나머지 일곱 표는 `Epic Saga<sup>(sao)</sup>`나
    `Horror Story<sup>(aac)</sup>`처럼 코드를 달고, 여기만 `Fantasy Fiction`이다(캡션에는
    `(aao)`가 있다). 렌더해 확인한 실측이고 저자들이 그 차이를 적지 않는다.
- **언제 쓰는가** — 저자들이 이 칸을 권하지 않는다. 절을 닫는 문장은 **이 패턴이 마땅한 것보다
  불행히도 더 인기 있고, 대개 트랜잭션성을 유지한 채 Epic Saga(sao)의 성능을 개선하려는
  잘못 짚은 시도에서 나온다**는 것이며, **대개 더 나은 선택지는 Parallel Saga(aeo)**다 (12장,
  p.342).[^ford2021-hard-parts]
  - **이 절은 같은 칸(`aeo`)을 두 번 가리킨다** — 확장성 채점에서 한 번, 닫는 문장에서 한 번이다.
    **여덟 절 가운데 한 칸을 두 번 대안으로 지목하는 자리는 여기뿐이다.**

## Horror Story(aac) - 여덟 중 가장 나쁜 조합

- **여덟 중 하나는 가장 나쁜 조합일 수밖에 없다는 문장으로 절이 시작한다** (12장,
  p.343):[^ford2021-hard-parts]

  > One of the patterns must be the worst possible combination; it is the aptly named
  > *Horror Story*<sup>(aac)</sup> *pattern*, characterized by *asynchronous* communication,
  > *atomic* consistency, and *choreographed* coordination

- **왜 최악인가의 규정** (12장, p.343):[^ford2021-hard-parts]

  > Why is this combination so horrible? It combines the most stringent coupling around
  > consistency (*atomic*) with the two loosest coupling styles, *asynchronous* and
  > *choreography*.

  - **가장 까다로운 값 하나와 가장 느슨한 값 둘이 한 칸에 모인 것**이 저자들의 진단이다.
- **기제** — 이 패턴에는 **여러 서비스에 걸친 트랜잭션 일관성을 관리할 중재자가 없는데 통신은
  비동기다.** 그래서 **각 도메인 서비스가 여러 pending 트랜잭션에 대한 되돌리기 정보(undo
  information)를 스스로 추적해야 하고, 비동기성 때문에 그 순서가 어긋날 수 있으며, 오류 조건
  동안 서로 조율해야 한다** (12장, p.344).[^ford2021-hard-parts]
  - 저자들이 드는 장면 — 트랜잭션 *Alpha*가 시작하고 pending인 동안 *Beta*가 시작한다. Alpha의
    호출 하나가 실패하면 **코레오그래피된 서비스들이 발화 순서를 거꾸로 되짚어, 어쩌면 순서가
    어긋난 채로, 트랜잭션의 요소를 하나씩 되돌려야 한다.** **오류 조건의 다중성과 복잡성이
    이것을 벅찬 선택지로 만든다** (12장, p.344).[^ford2021-hard-parts]
  - **Phone Tag Saga(sac)의 프런트 컨트롤러가 여기서는 나오지 않는다** — 그 칸에서는 처음 호출된
    서비스가 조율 지점이 되어 원자성의 로직을 맡았는데, 이 칸의 서술에는 그 장치가 없고 **모든
    도메인 서비스가 저마다 되돌리기 정보를 든다.** 저자들이 두 칸의 그 차이를 적지 않는다.
    #hypothesis
- **왜 그래도 고르는가와 대안** — **비동기성이 성능 부양으로 매력적이고 그러면서도 아키텍트가
  트랜잭션 무결성을 지키려 하기** 때문인데, 그 길에는 **무수한 실패 양태**가 있다. 대신
  **전체를 아우르는 트랜잭션성을 없애는 `Anthology Saga(aec)`를 고르는 편이 낫다** (12장,
  p.344).[^ford2021-hard-parts]
- **채점 넷의 근거** (12장, pp.344–345):[^ford2021-hard-parts]
  - **결합** — **놀랍게도 이 패턴의 결합 수준이 최악은 아니다.** 그 "영예(honor)"는
    Epic Saga(sao)의 것이다. 이 패턴은 **단일 결합 가운데 가장 나쁜 종류(트랜잭션성)를
    시도하지만 나머지 둘을 덜어 낸다** — 중재자도 없고, **동기 통신이 올리는 결합**도 없다.
  - **복잡도** — 이름 그대로 **그 어느 패턴보다 끔찍하다.** **가장 까다로운 요구(트랜잭션성)를
    그것을 이루기에 가장 어려운 조합(비동기성과 코레오그래피)으로 하려 하기** 때문이다.
  - **확장성과 탄력성** — **중재자를 둔 패턴들보다는 확장이 낫고**, 비동기성이 **병렬로 더 많은
    일을 할 능력**을 더한다.
  - **응답성과 가용성** — **낮다.** 전체 트랜잭션을 요구하는 다른 패턴들과 마찬가지로,
    **워크플로 조율에 서비스 간 "잡담(chatter)"이 대량으로 필요해 성능과 응답성을 해친다.**
- **표 12-7의 행과 값을 그대로 옮긴다** (12장, p.345):[^ford2021-hard-parts]

| Horror Story<sup>(aac)</sup> | Ratings |
|---|---|
| Communication | Asynchronous |
| Consistency | Atomic |
| Coordination | Choreographed |
| Coupling | Medium |
| Complexity | Very high |
| Responsiveness/availability | Low |
| Scale/elasticity | Medium |

- **어디서 오는가** — 저자들이 이 칸의 발생 경로를 적는다. **Epic Saga(sao)로 시작한 선의의
  아키텍트가 복잡한 워크플로 때문에 성능이 느린 것을 알아채고, 성능을 올리는 기법에 비동기
  통신과 코레오그래피가 있다는 것을 깨닫는 데서** 나온다 (12장, p.345).[^ford2021-hard-parts]
  - **그 사고가 이 책 전체의 논지를 뒤집어 보이는 사례가 된다** (12장,
    p.345):[^ford2021-hard-parts]

    > In isolation, asynchronous communication improves performance. However, as architects,
    > we cannot consider it in isolation when it is entangled with other architecture
    > dimensions, such as consistency and coordination.

  - **이 장에서 "차원들이 얽혀 있다"는 명제가 낱말로 적히는 자리는 여기 하나다.** 여덟 칸이라는
    조판 자체가 그 명제이지만, 그것을 문장으로 적는 것은 이 절뿐이다.
- **언제 쓰는가** — **이 칸에는 권장 상황이 하나도 적히지 않는다.** 여덟 절 가운데 쓸 자리를
  한 줄도 주지 않는 칸은 여기뿐이고, 대신 저자들이 **다른 칸(`aec`)으로 보낸다** (12장,
  p.344).[^ford2021-hard-parts]
  - **여는 사가가 이 칸을 "패턴, 아니 사실은 안티패턴"이라 부른 그 칸이다** (12장, p.323,
    사가).[^ford2021-hard-parts] 본문의 **여덟 다 정당한 쓰임이 있다**(p.324)와 나란히 놓으면
    낱말이 어긋나는데, **이 칸의 본문에도 정당한 쓰임이 적히지 않아 사가 쪽 낱말에 가깝다.**
    #hypothesis 저자들이 그 어긋남을 적지 않는다.

## Parallel Saga(aeo) - Epic에서 둘을 놓기

- **이름이 Epic Saga(sao)에서 나왔고 차이가 둘이다** — **비동기 통신과 최종 일관성**이며, 그
  둘이 제약을 풀어 **구현하기 더 쉬운 패턴**으로 만든다 (12장, p.346).[^ford2021-hard-parts]
- **무엇을 푸는가** — **Epic Saga(sao)에서 가장 어려운 목표가 트랜잭션과 동기 통신을 둘러싸고
  있고 둘 다 병목과 성능 저하를 부르는데, 이 패턴이 그 구속 둘을 다 느슨하게 한다** (12장,
  p.346).[^ford2021-hard-parts]
- **기제** — **중재자를 쓰므로 복잡한 워크플로에 알맞다.** 그러면서 **비동기 통신을 써서
  응답성과 병렬 실행이 낫다.** **일관성은 도메인 서비스 쪽에 있고**, 공유 데이터의 동기화가
  얼마간 필요할 수 있는데 그것은 **배경에서 하거나 중재자가 몰아서** 한다. **조율이 필요한 다른
  아키텍처 문제에서와 마찬가지로 중재자가 꽤 쓸모 있어진다** (12장, p.346).[^ford2021-hard-parts]
  - 도판이 그 배치를 캡션으로 적는다 — **각 서비스가 자기 트랜잭션성을 소유하고, 중재자는 요청과
    응답을 조율한다** (12장, p.347, 그림 12-17).[^ford2021-hard-parts]
  - **오류 경로가 이 칸에서 비동기가 된다** — 워크플로 실행 중에 오류가 나면 **중재자가 관련된
    각 도메인 서비스에 비동기 메시지를 보내 실패한 변경을 보상하게 하고**, 그것은 **재시도·데이터
    동기화, 그 밖의 여러 교정**을 수반할 수 있다 (12장, p.347).[^ford2021-hard-parts]
- **느슨하게 한 값** — **트랜잭션성이 없으니 오류와 그 밖의 워크플로 문제를 푸는 부담이 중재자에
  더 얹히고**, 비동기 통신은 응답성을 주는 대신 **타이밍과 동기화 문제를 풀기 어렵게 만든다** —
  **경쟁 조건·교착·큐 신뢰성**과 그 밖의 분산 아키텍처 골칫거리가 이 공간에 산다 (12장,
  p.347).[^ford2021-hard-parts]
- **채점 넷의 근거** (12장, pp.347–348):[^ford2021-hard-parts]
  - **결합** — **낮다.** **결합을 키우는 힘인 트랜잭션을 개별 도메인 서비스의 범위 안으로
    가둔다.** 비동기 통신이 **서비스를 대기 상태에서 더 떼어 놓아** 병렬 처리를 늘리되
    **아키텍트의 결합 분석에 시간이라는 요소를 더한다.**
  - **복잡도** — **낮다.** 앞서 적은 결합의 줄어듦이 그대로 반영된 것이고, **아키텍트가 이해하기
    꽤 쉬우며 오케스트레이션이 더 단순한 워크플로·오류 처리 설계를 허용한다.**
  - **확장성과 탄력성** — 비동기 통신과 **더 작은 트랜잭션 경계** 덕에 꽤 잘 확장하고 서비스
    사이 격리 수준도 좋다. 저자들이 드는 예 — 마이크로서비스 아키텍처에서 **공개 대면
    서비스는 높은 확장·탄력이 필요하고 후방(back office) 서비스는 확장 대신 높은 보안이 필요할
    수 있다.** **트랜잭션을 도메인 수준에 가두면 아키텍처가 도메인 개념을 중심으로 확장할 자유를
    얻는다.**
  - **응답성과 가용성** — **높다.** 조율된 트랜잭션이 없고 통신이 비동기이기 때문이다. 나아가
    **각 서비스가 자기 트랜잭션 맥락을 유지하므로 서비스마다 성능 발자국의 편차가 큰 곳에 잘
    맞고**, 수요에 따라 **일부 서비스만 더 확장할 수 있다.**
- **표 12-8의 행과 값을 그대로 옮긴다** (12장, p.348):[^ford2021-hard-parts]

| Parallel Saga<sup>(aeo)</sup> | Ratings |
|---|---|
| Communication | Asynchronous |
| Consistency | Eventual |
| Coordination | Orchestrated |
| Coupling | Low |
| Complexity | Low |
| Responsiveness/availability | High |
| Scale/elasticity | High |

- **언제 쓰는가** — **여러 시나리오에, 특히 높은 확장이 필요한 복잡한 워크플로에 매력적인 절충
  집합을 준다** (12장, p.348).[^ford2021-hard-parts]

## Anthology Saga(aec) - Epic의 정반대

- **규정이 Epic Saga(sao)의 거울로 적힌다** (12장, p.349):[^ford2021-hard-parts]

  > The *Anthology Saga*<sup>(aec)</sup> *pattern* provides the exact opposite set of
  > characteristics to the traditional Epic Saga<sup>(sao)</sup> pattern: it utilizes
  > *asynchronous* communication, *eventual* consistency, and *choreographed* coordination,
  > providing the least coupled exemplar among all these patterns.

- **기제** — **메시지 큐를 써서 오케스트레이션 없이 다른 도메인 서비스로 비동기 메시지를
  보낸다.** **각 서비스가 자기 트랜잭션 무결성을 유지하고 오케스트레이터가 없으므로, 각 도메인
  서비스가 자기가 참여하는 워크플로에 대한 맥락을 더 많이 담아야 하고** 거기에 **오류 처리와 그
  밖의 조율 전략**이 포함된다 (12장, p.349).[^ford2021-hard-parts]
  - **여덟 절 가운데 메시지 큐를 기제로 이름 지어 부르는 자리는 여기뿐이다** — 다른 비동기 칸
    셋은 "비동기 통신"이라고만 적는다. 두 추출기로 확인했다.
- **오케스트레이션의 부재가 값과 대가를 동시에 만든다** — 서비스는 더 복잡해지지만 **처리량·
  확장성·탄력성과 그 밖의 이로운 운영 아키텍처 특성이 훨씬 높아진다.** **병목도 결합의 목
  조르는 지점(coupling choke points)도 없어** 응답성과 확장성이 높다 (12장,
  p.350).[^ford2021-hard-parts]
- **그러나 복잡한 워크플로에는 잘 듣지 않는다** — 특히 **데이터 일관성 오류를 푸는 데서** 그렇다.
  **오케스트레이터 없이는 가능해 보이지 않더라도 스탬프 결합(stamp coupling)으로 워크플로 상태를
  실어 나를 수 있고**, 그것은 **Phone Tag Saga(sac)에서 설명한 것과 같은 방식**이다 (12장,
  p.350).[^ford2021-hard-parts] 저자들은 그 규정을 13장 p.378로 넘긴다.
- **가장 잘 맞는 자리** — **단순하고 대체로 선형인 워크플로에, 높은 처리 처리량을 바랄 때**다.
  **높은 성능과 확장 양쪽에 가장 큰 잠재력을 주므로 그 둘이 핵심 구동 요인이면 매력적인
  선택**이지만, **떼어 놓은 정도가 조율을 어렵게 만들고 복잡하거나 결정적인 워크플로에는 금지될
  만큼 그렇다** (12장, p.350).[^ford2021-hard-parts]
- **채점 넷의 근거** (12장, pp.350–351):[^ford2021-hard-parts]
  - **결합** — **어느 조합보다 낮다.** 고도로 떼어 놓인 아키텍처를 만들어 높은 확장과 탄력에 잘
    맞는다.
    - 원문의 그 문장은 `Coupling for this pattern is the lowest for any other combination of
      forces`로 비교 구문이 어긋난다(`lowest for any other`) (12장, p.350).[^ford2021-hard-parts]
      두 추출기와 렌더가 모두 같은 문장을 낸다.
  - **복잡도** — **결합이 극히 낮은 만큼 복잡도가 그에 대응해 높다.** 특히 **오케스트레이터가
    편리할 복잡한 워크플로**에서 그렇고, 여기에는 그 오케스트레이터가 없다.
  - **확장성과 탄력성** — **확장과 탄력 범주에서 가장 높은 점수**이고, 이 패턴 전반의 결합 부재와
    상관한다.
  - **응답성** — **높다.** **속도 조절기(speed governors, 곧 트랜잭션 일관성과 동기 통신)가 없고
    응답성 가속기(responsiveness accelerators, 곧 코레오그래피된 조율)를 쓰기** 때문이다.
    - **이 항목만 제목이 `Responsiveness`이고 `/availability`가 없다** — 표 12-9의 행은
      `Responsiveness/availability`다. 여덟 절 가운데 이 한 자리뿐이고 저자들이 그 차이를 적지
      않는다.
- **표 12-9의 행과 값을 그대로 옮긴다** (12장, p.350):[^ford2021-hard-parts]

| Anthology Saga<sup>(aec)</sup> | Ratings |
|---|---|
| Communication | Asynchronous |
| Consistency | Eventual |
| Coordination | Choreographed |
| Coupling | Very low |
| Complexity | High |
| Responsiveness/availability | High |
| Scale/elasticity | Very high |

- **언제 쓰는가** — **극히 높은 처리량 통신에, 오류 조건이 단순하거나 드물 때** 잘 맞고, 저자들이
  드는 실물이 **파이프와 필터(Pipes and Filters) 아키텍처**다 — **그 양식이 이 패턴에 정확히
  들어맞는다** (12장, p.350).[^ford2021-hard-parts]
  - **같은 양식이 두 칸의 예로 쓰인다** — `Time Travel Saga(sec)` 절도 자기 구현으로
    **책임 연쇄(Chain of Responsibility) 설계 패턴이나 파이프와 필터 아키텍처 양식**을 들었다
    (12장, p.338).[^ford2021-hard-parts] **두 칸의 차이는 통신 축 하나뿐인데 저자들이 그 겹침을
    적지 않는다.** #hypothesis
  - **Time Travel Saga(sec)가 이 칸을 진입로의 도착지로 지목한 그 칸이기도 하다** — 그쪽 절은
    **더 복잡하지만 결국 더 확장성 있는 `Anthology Saga(aec)`로 가는 진입로**라고 자기를
    규정했다 (12장, p.339).[^ford2021-hard-parts]
- **절이 닫히며 이 장의 다음 두 절을 예고한다** (12장, p.350):[^ford2021-hard-parts]

  > Architects can implement the patterns described in this section in a variety of ways. For
  > example, architects can manage transactional sagas through atomic transactions by using
  > compensating updates or by managing transactional state with eventual consistency.

  - 곧 **여덟 칸이 무엇인가 다음에 오는 물음은 그것을 무엇으로 굴리는가**이고, 저자들이 그 답을
    둘로 놓는다 — **보상 갱신을 쓰는 원자적 트랜잭션**과 **최종 일관성으로 트랜잭션 상태를
    관리하는 것**이다. 아래 두 절이 각각을 편다.


## 다섯째 소스의 두 사가가 어느 칸에 앉는가

**2025년의 이벤트 기반 마이크로서비스 실무서가 사가를 둘로 구현한다. 그 둘이 이 페이지의 네 칸
가운데 둘과 겹친다 — 이 페이지에 적는 이유가 그것이고, 겹치는 칸이 둘 다 비동기이기 때문이다.**

- **그 소스의 사가는 분산 트랜잭션의 동의어다** — **둘 이상의 완전히 독립된 데이터 저장소에 걸치는
  트랜잭션**이고, **코레오그래피 패턴이나 오케스트레이터 패턴 어느 쪽으로도 구현할 수 있다** (10장,
  pp.231–232).[^bellemare2025] 낱말의 외연 대조는 [사가 패턴](../concepts/saga-pattern.md)에 있다.
- **코레오그래피 사가는 `Anthology Saga(aec)`에 앉는다.** 근거 셋이다 (10장,
  pp.232–234):[^bellemare2025]
  - **통신이 비동기다** — 서비스들이 이벤트 스트림으로만 이어진다. 그 소스는 **사가 스트림(saga
    stream)** 과 **지시 스트림(instruction stream)** 둘을 세운다.
  - **조율자가 없다** — **각 서비스가 실패 시 변경을 롤백할 수 있어야 하고, 롤백에 대해 상류
    시스템과 소통해야 하며, 완료된 사가는 시작한 서비스로 가는 피드백 루프로 완료를 알린다.**
  - **일관성이 최종이다** — 원자적 커밋 프로토콜이 없다.
  - 이 대응은 이 KB의 읽기이고 **두 소스 어느 쪽도 이 대응을 적지 않는다.** #hypothesis
- **그 소스가 이 칸에 대해 적는 것이 위 [Anthology Saga(aec) - Epic의 정반대](#anthology-sagaaec---epic의-정반대)
  의 채점과 같은 방향이다** — **코레오그래피 트랜잭션은 서비스 사이에 엄격한 의존을 둔 채 꽤
  부서지기 쉽고**, 모니터링은 **완전히 탈중앙화된 본성 때문에 어려우며 전용 시스템을 지어야 하고**,
  연산 순서를 바꾸려면 **새 처리를 멈춘 뒤 진행 중인 처리를 전부 끝내야 한다** (10장,
  pp.233–234).[^bellemare2025] 이 페이지가 담은 원문 채점 **복잡도 `Very high`**·**조율이 어렵고
  복잡한 워크플로에는 금지될 만큼**과 같은 자리를 산문으로 적은 것이다.
- **넘어가는 신호도 같은 방향이다** — 그 소스는 **서비스 수가 늘거나 더 많은 통제와 감독이
  필요해지면 오케스트레이션 사가 패턴을 보라**고 적는다 (10장, p.234).[^bellemare2025]
- **오케스트레이션 사가는 `Parallel Saga(aeo)`에 가장 가깝되 한 칸에 온전히 앉지 않는다.**
  조율이 오케스트레이션이고 일관성이 최종인 것은 맞지만, **그 소스의 예제가 통신 축을 섞는다** —
  **그림 10-9의 2단계 오케스트레이션 트랜잭션이 의존 마이크로서비스와 통신하는 데 이벤트
  스트리밍과 요청-응답을 둘 다 쓴다** (10장, p.235).[^bellemare2025]
  - **이 페이지의 네 칸은 통신 축을 비동기로 고정한 것이므로, 요청-응답이 섞인 워크플로는
    여기와 동기 쪽 칸에 걸친다.** 여덟 칸의 프레임이 **한 워크플로 안에서 통신 방식이 섞이는
    경우를 다루지 않는다.** #hypothesis 그 소스도 여덟 칸의 어휘를 쓰지 않으므로 이 어긋남을
    적지 않는다.
- **그 소스가 `aeo` 쪽에 더하는 것 셋** (10장, pp.235–236):[^bellemare2025]
  - **타임아웃과 사람의 개입을 조율자에 들인다** — **타임아웃으로 오케스트레이터의 구체화된
    상태를 주기적으로 확인해 시간 초과된 마이크로서비스를 식별하고, REST API로 온 사람의 입력을
    다른 이벤트와 나란히 처리해 취소 지시를 다룬다.** 위 절들의 중재자 서술에 이 두 신호가 없다.
  - **롤백 뒤의 선택지 셋을 적는다** — **전체 과정을 재시도하거나, 관련 입력 이벤트를 버리거나,
    예외를 던지고 스스로 종료한다.**
  - **최악의 경우를 따로 적는다** — **트랜잭션을 완료할 수도 롤백할 수도 없으면 일반적으로 모든
    처리를 멈추고 사고로 처리해 정리하는 것이 최선이다.** 위
    [Fantasy Fiction Saga(aao) - 비동기가 원자성을 만나면](#fantasy-fiction-sagaaao---비동기가-원자성을-만나면)
    이 담은 중재자의 부담과 층이 다른 이야기다 — 이쪽은 **보상 자체가 실패하는 운영 사태**이고,
    [사가 패턴](../concepts/saga-pattern.md)이 담은 포드 외의 실패 양태 넷 가운데 둘째와 같은 것을
    가리킨다. **두 소스가 서로를 호명하지 않는다.** #hypothesis
- **모순 쌍을 걸지 않았다.** 그 소스는 여덟 칸의 어휘 자체를 쓰지 않으므로 채점을 두고 겨룰 자리가
  없고, 겹치는 자리에서는 같은 방향을 가리킨다. 그 소스의 전문은
  [이벤트 기반 워크플로](../concepts/event-driven-workflows.md)에 있다.

## 이어지는 페이지

- [트랜잭셔널 사가 패턴](transactional-saga-patterns.md) — 이 페이지의 부모. 세 축과 여덟 칸의
  프레임, 코드 해독 규칙, 도판의 범례, 채점 축 넷, 동기 쪽 네 칸, 여덟 전부의 대조표, 그리고
  상태 관리·상태 기계·사가 관리 기법과 책의 사례
- [아키텍처 퀀텀](../concepts/architectural-quantum.md) — 세 축의 규정과 여덟 칸의 결합 강도표가
  사는 자리
- [오케스트레이션과 코레오그래피](../concepts/orchestration-versus-choreography.md) — 조율 축 하나의 전문
- [최종 일관성 패턴 셋](../concepts/eventual-consistency-patterns.md) — 이 네 칸 가운데 둘이 딛고 서는
  일관성 축의 값
- [마이크로서비스 통신 스타일](../concepts/microservice-communication-styles.md) — 이 페이지가 고정한 통신
  축의 전문
- [사가 패턴](../concepts/saga-pattern.md) — 같은 낱말을 다섯 소스가 서로 다른 대상에 쓴다는 대조표
- [이벤트 기반 워크플로](../concepts/event-driven-workflows.md) — 이 네 칸 가운데 둘과 겹치는 두 사가를 이벤트 스트림 기반에서 세우는 소스
- [이벤트 주도 통합 설계](../concepts/event-driven-integration-design.md) — `Anthology Saga(aec)`가 메시지
  큐로 실어 나르는 것을 어떤 종류의 이벤트로 설계할 것인가
- [견고함 패턴 목록](../concepts/stability-patterns.md) — 이 칸들의 보상과 재시도가 기대는 기제
- [데이터 분해와 정합성](../synthesis/data-decomposition-and-consistency.md) — 이 축의 허브

[^ford2021-hard-parts]: Ford·Richards·Sadalage·Dehghani 2021, **12장 "Transactional Sagas"의
    §"Fantasy Fiction Saga(aao) Pattern"(pp.340–342) · §"Horror Story(aac) Pattern"(pp.343–345) ·
    §"Parallel Saga(aeo) Pattern"(pp.346–348) · §"Anthology Saga(aec) Pattern"(pp.349–351)**.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 18, 실측). 직인용은 전부 `pdftotext -layout` 추출로 문자 단위
    대조했고, 줄바꿈 하이픈(U+2010)은 원래 낱말로 이었으며 굽은 따옴표는 곧은 따옴표로 옮겼다.
    원문이 위첨자로 조판한 세 글자 코드는 `<sup>` 로 옮겼고, 산문에서는 `Parallel Saga(aeo)`
    처럼 괄호로 적었다.
    **채점표 넷(표 12-6 p.342 · 12-7 p.345 · 12-8 p.348 · 12-9 p.350)을 `pdftoppm -r 160 -png`
    로 렌더해 눈으로 대조하고 원문 행·값 그대로 옮겼다** — 이 장의 채점표에는 별점 글리프가 없고
    다섯 눈금이 전부 텍스트 레이어에 있다.
    **도판 여덟(정육면체 넷 그림 12-12·12-14·12-16·12-18과 등각 다이어그램 넷 12-13·12-15·
    12-17·12-19)은 렌더해 읽되 본문이 그 도판에 대해 적는 것만 옮겼다** — 범례와 축 라벨은 부모
    페이지가 갖는다. **이 구간에 코드 목록이 하나도 없고 버전 조건도 0건이다**(제품 이름이 하나도
    나오지 않는다).
    원문의 어색한 자리 둘을 그대로 옮기고 표시했다 — p.350의
    `Coupling for this pattern is the lowest for any other combination of forces`(비교 구문
    어긋남)와, p.342의 `misguided`가 `mis-`/`guided`로 갈리며 **이 구간에서 유일하게 ASCII
    하이픈으로 조판된 줄바꿈**이라는 것이다(다른 줄바꿈 하이픈은 전부 U+2010이다). 이 KB는 뒤의
    것을 한 낱말로 이어 적었다.
    표 12-6의 머리글 칸에만 세 글자 코드가 없다는 것과 `Anthology Saga(aec)`의 넷째 채점 항목
    제목만 `Responsiveness`라는 것도 렌더로 확인한 실측이다.
    저자들이 이 구간에서 대는 바깥 참조 — 13장 p.378의 스탬프 결합, 같은 장 p.330의
    `Phone Tag Saga(sac)` 절, 같은 장 p.339의 `Time Travel Saga(sec)` 절 — 는 이 구간 밖이다.

[^bellemare2025]: Bellemare 2025, 10장 "Building Workflows with Microservices",
    pp.231–236. 이 페이지에는 직인용을 두지 않았고 한국어 재서술이다 — 이 소스의 규정과 원문
    목록은 [이벤트 기반 워크플로](../concepts/event-driven-workflows.md)에 있다.

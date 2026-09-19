---
type: concept
title: 워들리 매핑
description: 기술 지형을 가치 사슬과 진화 단계 두 축 위에 놓고 그것이 어디로 움직일지 논하는 전략 분석 기법 — 범위와 사용자 요구를 정하고 그 요구를 채울 구성 요소를 찾아 진화 축에 놓는 세 걸음, 지도를 보통의 체계 다이어그램과 가르는 세 성질(고정 방위를 주는 앵커·뜻을 갖는 위치·움직임의 일관성), 가시성을 세로로 두는 가치 사슬 축과 왼쪽 끝이 갓 생긴 것이고 오른쪽 끝이 상품인 가로 진화 축, 그 진화 척도가 로저스의 겹친 확산 곡선과 무어의 캐즘 논의에서 나와 시간 축을 확실성 축으로 바꾼 자리, 원문 그대로 옮긴 진화 단계 넷(제네시스·맞춤 제작·제품 및 임대·상품 및 유틸리티)의 규정, 찻집 지도라는 예시가 보이는 노드와 간선과 배치, 그리고 이 낱말의 진화가 진화적 아키텍처의 진화와 다른 대상을 가리킨다는 대조
generated: { by: "claude-opus-5", at: "2026-09-19T16:00:00Z" }
status: draft
sources:
  - { id: urquhart2021, resource: /it/sources/urquhart2021.md }
---

# 워들리 매핑

- [이 페이지가 서는 자리](#이-페이지가-서는-자리)
- [핵심 착상 세 걸음](#핵심-착상-세-걸음)
- [지도가 다이어그램과 갈리는 세 성질](#지도가-다이어그램과-갈리는-세-성질)
- [두 축 — 가치 사슬과 진화](#두-축--가치-사슬과-진화)
- [진화 척도가 어디서 왔는가](#진화-척도가-어디서-왔는가)
- [진화 단계 넷](#진화-단계-넷)
- [찻집 지도 — 예시 하나](#찻집-지도--예시-하나)
- [지도를 만드는 절차](#지도를-만드는-절차)
- [이 KB의 이웃과 맞대는 자리](#이-kb의-이웃과-맞대는-자리)
- [이어지는 페이지](#이어지는-페이지)

## 이 페이지가 서는 자리

**이 페이지는 워들리 매핑(Wardley Mapping)의 원전이 아니라 한 소스를 경유한 2차 서술이다.**
기법을 만든 사람은 사이먼 워들리(Simon Wardley)이고 그가 2005년에 이 개념을 만들었으며, 그 자신이
"책"이라 부르는 것에 기법을 자세히 서술하는데 그것은 실은 이 기법이 어떻게 생겨났는지와 전략 계획의
맥락에서 갖는 쓸모를 적은 **연작 블로그 글**이다. 이 소스의 저자는 자기가 줄 수 있는 것은 높은 층위의
개관뿐이라고 밝히고 관심이 생기면 워들리의 글을 직접 읽으라고 권한다. 더 빠른 개관으로는 워들리가
자기 기법을 다룬 발표들을 든다 (3장 §"Wardley Mapping and Promise Theory", p.47).[^urquhart2021]

- 버전 조건: 2021년 저술 시점의 서술이다. 그 연작은 온라인 글이고 이 KB는 현재 상태를 확인하지 않았다.

- **이 KB에 워들리의 글 자체는 들어와 있지 않다.** 그래서 아래의 모든 귀속은 "이 소스가 워들리를
  그렇게 옮겨 적는다"까지이고, 워들리 자신의 문장으로 확인된 것이 아니다. 인용 부호가 붙은 구간은
  이 소스가 인용 형태로 실은 것을 그대로 옮긴 것이다.
- **이 소스가 이 기법을 쓰는 목적은 하나다** — 오늘의 이벤트 기반 통합이 어디에 서 있고 무엇이 먼저
  움직일지를 보려는 것이다. 그 적용은 [플로 통합 가치 사슬 지도](flow-integration-value-chain.md)에
  있고, 이 페이지는 그 적용에서 기법 자체만 떼어 놓은 자리다.

## 핵심 착상 세 걸음

- **저자는 워들리 맵의 핵심 착상이 단순하다고 적고 세 걸음으로 옮긴다** (3장, p.47).[^urquhart2021]
  - **범위(scope)와 사용자 요구(user need)를 정한다.**
  - **그 사용자 요구를 채우는 데 필요한 구성 요소를 결정한다.**
  - **그 구성 요소들을 진화의 관점에서 평가한다** — 완전히 새로운 것에서 받아들여진 상품에 이르는
    축 위에서다.
- **기술 진화를 두고 추측하는 방법은 많지만 착상을 소통하고 겨루게 하는 데 저자가 찾은 가장 강력한
  기법이 워들리 맵이다** (3장, p.47).[^urquhart2021]

## 지도가 다이어그램과 갈리는 세 성질

- **지도는 공간이 뜻을 갖는 산출물이다** — 워들리가 그렇게 짚었다고 저자는 적는다 (3장 곁상자
  "What Is a Map?", p.64).[^urquhart2021]

  > A map, as Wardley pointed out, is an artifact where space has meaning.

- **보통의 체계 다이어그램에서 노드 하나를 옮겨도 표현된 정보는 의미 있게 바뀌지 않는다** — 공간에
  대한 위치 감각이 없기 때문이다. 영국 지도에서 런던을 옮기면 뜻이 확실히 바뀐다 (3장 곁상자,
  pp.64–65).[^urquhart2021]
- **지도를 다른 형태의 도식과 가르는 성질이 셋이다** (3장 곁상자, p.65).[^urquhart2021]
  - **앵커(anchor)** — 지도 위의 위치와 움직임에 고정된 방위를 주는 지시자다. 영국 지도에서는
    나침반이 가리키는 진북이 그것이다.
  - **뜻을 갖는 위치(meaningful position)** — 런던이 영국 해안선에 대해 어디에 그려지는가가 그것이다.
  - **움직임의 일관성(consistency of movement)** — 런던을 떠나 북서로 가면 아일랜드에 닿으리라 기대할
    수 있고, 프랑스에 닿았다면 지도를 잘못 읽었거나 지도 자체가 틀렸다고 의심하게 된다.
- **워들리 맵에서 그 셋에 해당하는 것이 각각 사용자 요구와 진화 축에 대한 구성 요소의 위치와
  제네시스에서 맞춤 제작을 지나 제품과 유틸리티로 가는 진화의 힘이다** (3장 곁상자,
  p.65).[^urquhart2021]

## 두 축 — 가치 사슬과 진화

- **세로축은 가치 사슬(value chain)이고 눈금은 가시성이다** — 위쪽이 보이는 것(Visible)이고 아래쪽이
  보이지 않는 것(Invisible)이다. 가로축은 진화(Evolution)이고 왼쪽에서 오른쪽으로 제네시스, 맞춤
  제작, 제품(임대 포함), 상품(유틸리티 포함) 네 구간이 놓인다. **축 이름과 눈금 표기는 본문이 아니라
  도판에만 있다** (3장, 그림 3-1·3-20~3-24).[^urquhart2021]
- **가치 사슬의 위아래는 약속이 흐르는 방향을 정한다** — 저자는 사슬을 검증할 때 **아래에서 위로**
  올라가는 약속에 주의를 기울이고 "덜 보이는 구성 요소가 더 보이는 구성 요소에 하는 약속이
  무엇인가"를 묻는다. 그렇게 하면 사용자 요구를 채우려 수렴하는 약속의 집합을 얻게 되고, 구성 요소
  사이에 직접 약속이 없는 자리도 빨리 드러나는데 **그 자리에는 연결이 없어야 한다** (3장,
  p.52).[^urquhart2021]
- **진화 축의 배치 자체가 지도의 쓸모다** — 사용자 요구가 채워지는 동안 해법을 짓는 구성 요소들
  자신도 각자 어떤 문제의 해법이고, 그 하나하나가 눈금 어딘가에 놓이며, **그 하나하나가 또한 왼쪽에서
  오른쪽으로 움직이고 있다.** 가치 사슬을 이 눈금에 옮겨 놓으면 기술 개발의 움직임을 지금에 대해서도
  추상적 층위에서 앞날에 대해서도 볼 수 있다 (3장, pp.63–64).[^urquhart2021]

## 진화 척도가 어디서 왔는가

- **워들리는 기술이 시간에 따라 어떻게 바뀌는지 알아야 했을 때 지난 기술들의 진화를 크게 조사했고,
  그 조사가 그를 에버렛 로저스(Everett Rogers)의 작업으로 이끌었다** — 저자는 로저스를 제프리 무어의
  기술 채택 안내서 *Crossing the Chasm*(Harper Business Essentials)에 서술된 것으로 적는다. 저자가
  요약하는 것은 워들리의 2015년 블로그 글 하나다 (3장 §"Determining a Measure of Technology
  Evolution", p.61).[^urquhart2021]
- **로저스가 짚은 것은 공유된 요구에 맞는 기술을 찾는 일이 대개 하나의 기술 채택 주기의 결과가
  아니라는 것이다** — 시장이 "맞고" 확장되는 적합을 사냥하는 동안 여러 기술의 채택 곡선이 겹친다.
  전화나 전력 같은 요구가 널리 채택된 첫 해법으로 채워지는 일은 드물거나 없다 (3장,
  p.61).[^urquhart2021]
  - 저자는 각주에서 이 논지를 농담으로 되짚는다 — 첫 전화 체계가 이긴 전화 체계였다면 우리는 아직
    유선 전화를 쓰고 있을 것이고 이웃이 받는 모든 전화에 우리 전화기가 울릴 것이다 (3장 각주 5,
    p.61).[^urquhart2021]
- **워들리가 한 일은 시간 축을 기술 혁신의 상태를 나타내는 축으로 바꾼 것이다.** 그는 어떤 요구의
  해법을 두고 쓰인 기사와 학술 논문을 분석해 진화의 단계들을 식별했고, **그런 출판물에 일반적으로
  네 단계가 있으며 그것이 기술 진화의 네 단계를 가리킨다**는 것을 발견했다 (3장,
  p.62).[^urquhart2021]
- **네 단계를 새 가로축 눈금에 옮긴 것이 워들리 매핑의 심장에 있는 통찰이라고 저자는 적는다** (3장,
  p.63).[^urquhart2021]

## 진화 단계 넷

**네 단계의 규정은 번역하지 않고 원문을 그대로 옮긴다** — 저자가 워들리의 서술로 제시한 대목이다
(3장, pp.62–63).[^urquhart2021]

> Genesis
>
> This represents the unique, the rare, the uncertain, the constantly changing, and the
> newly discovered. The described solution is a thing of wonder—technology so impactful,
> it almost seems like magic.
>
> Custom built
>
> This represents the uncommon and that which we are still learning about. It is
> individually made and tailored for a specific environment. It is bespoke. It frequently
> changes. It is an artisan skill. You wouldn't expect to see two of these that are the
> same. The solution is described in terms of ways of building and constructing your own
> instance.
>
> Product (including rental)
>
> This represents the increasingly common, the manufactured through a repeatable process,
> the more defined, the better understood. Change becomes slower here. While
> differentiation exists particularly in the early stages, there is increasing stability
> and sameness. You will often see many of the same products. Focus now turns to refining,
> operating, and maintaining those products.
>
> Commodity (including utility)
>
> This represents scale and volume operations of production, the highly standardized, the
> defined, the fixed, the undifferentiated, the fit for a specific known purpose and
> repetition, repetition, and more repetition. The focus is now on ruthless removal of
> deviation, on industrialization, and on operational efficiency. The solution becomes so
> expected, so ubiquitous, that one often forgets it is there.

- **한국어로 옮길 때 이 KB가 쓰는 말은 제네시스(genesis)·맞춤 제작(custom built)·제품(product,
  임대 포함)·상품(commodity, 유틸리티 포함)이다.** 확립 역어가 없어 원어를 함께 둔다.
- **이 단계들이 적어도 지난 200년 동안 주요 기술의 진화에 일관되게 나타났다고 저자는 적는다** (3장
  §"Mapping Our Value Chain", p.61).[^urquhart2021]
- **겹친 채택 곡선을 하나로 합치면 시간이 아니라 가용한 해법의 확실성에 대응하는 곡선이 된다** (3장,
  p.63).[^urquhart2021]
  - **도판이 본문보다 많이 말하는 자리다.** 확산 곡선 그림의 세로축은 적용 가능 시장(Applicable
    Market)이고 가로축이 시간이며, 다섯 활동 A[1]부터 A[5]까지의 S자 곡선이 차례로 겹쳐 오르면서
    각각의 100% 채택 지점과 A[4]에서 A[5]로 가는 시장 차이가 표시된다. 표준 확산 곡선 그림에서는
    세로축이 보편성(Ubiquity, 새것에서 흔한 것으로)이고 **수요(Demand)** 라는 화살표가 붙으며,
    가로축이 확실성(Certainty, 모르는 것에서 규정된 것으로)이고 **공급(Supply)** 이라는 화살표가
    붙는다. 네 구간이 겹치는 상자로 그려지고 서비스(Service)와 유틸리티(Utility)라는 점선 곡선이
    따로 붙는다. **두 축의 이름과 수요·공급 표기는 도판에만 있다** (3장, 그림 3-16 p.62·그림 3-17
    p.63).[^urquhart2021]
  - 두 그림 모두 캡션에 "courtesy of Simon Wardley"가 붙어 있다 — 이 소스가 그린 것이 아니라
    워들리에게서 받은 그림이다 (3장, pp.62–63).[^urquhart2021]

## 찻집 지도 — 예시 하나

- **저자는 기법을 설명하기 전에 찻집(tea shop)이 필요로 하는 기술과 자원을 그린 워들리 맵 하나를
  예시로만 보인다.** 사용자는 찻집("the business")과 그 손님들("the public")이고 사용자 요구는 차 한
  잔(a cup of tea)이며, 나머지 가치 사슬은 그 차 한 잔을 내는 데 필요한 구성 요소들이 진화 단계
  가로축에 놓인 것이다. 저자는 이것이 지도가 어떻게 생겼는지 보이는 예일 뿐이라고 적는다 (3장,
  p.47).[^urquhart2021]
- **그 지도의 노드와 배치는 도판에만 있고 본문에 없다** (3장, 그림 3-1, p.48).[^urquhart2021]
  - 노드는 아홉이다 — Business와 Public(맨 위, 가장 보이는 자리), 사용자 요구인 Cup of tea, 그 아래로
    Cup·Tea·Hot water·Water·Kettle·Power다.
  - 간선은 Business와 Public이 각각 Cup of tea로 내려가고, Cup of tea가 Cup·Tea·Hot water 셋으로
    내려가며, Hot water가 Kettle과 Water로, Kettle이 Power로 내려간다.
  - **배치는 거의 전부 상품(유틸리티 포함) 구간이고 Kettle 하나만 제품 구간에 있다.** 가장 보이지
    않는 자리에 Power가 놓인다.

## 지도를 만드는 절차

- **가장 먼저 할 일은 지도의 범위를 분명히 세우는 것이다.** 범위 진술은 지도가 초점을 잃지 않게 하는
  데 결정적이다. 범위는 "100기가바이트 이더넷 카드"처럼 아주 자세할 수도 "소비자 인터넷 기술"처럼
  아주 일반적일 수도 있고, 중요한 것은 그것이 탐구하려는 사용자 요구를 감싸는가다 (3장 §"Establishing
  a Scope for the Map", p.51).[^urquhart2021]
- **쓸 만한 지도를 낳는 범위는 대개 아주 일반적인 것과 극히 자세한 것 사이 어딘가에 있다.** 가장 좋은
  범위 진술은 **겨냥된 대화를 가능하게 할 만큼 자세하면서 새 착상과 새 진화적 영향의 탐구를 가능하게
  할 만큼 일반적**이다 (3장, p.51).[^urquhart2021]
- **범위가 정해지면 다음 걸음은 사용자와 그들의 사용자 요구를 식별하는 것이다** (3장 §"Establishing
  Our Users and User Need", p.52).[^urquhart2021]
- **그다음이 구성 요소를 결정하는 일이고, 여기서 어디서 시작할지는 여러 접근이 가능하다.** 저자는
  각주에서 이 걸음의 성격을 적는다 — 여럿이 모여 워들리 매핑을 할 때 어디서 시작할지 정하는 일은
  대개 크게 깨우침을 주는 논의가 되고, 평가할 사용자 요구가 여럿일 수도 있으며 어느 일차 구성 요소가
  필요한가를 두고 다툴 수도 있다. **저자는 이 첫 논의가 가장 오래 걸린다고 적고, 논쟁적이고 다툼으로
  시작하더라도 결국 지도를 짓는 이들 사이의 정렬로 귀결된다고 적는다** (3장 각주 3,
  p.53).[^urquhart2021]
- **마지막 걸음이 가치 사슬의 각 구성 요소가 놓인 진화 상태를 매기는 것이다** (3장 §"Mapping Our
  Value Chain", p.61).[^urquhart2021]
- **지도가 하나뿐일 필요는 없다.** 저자는 자기 범위 진술에 이의를 달아도 좋고 다른 지도를 지으면 아마
  다른 지도가 나올 것이며 그것이 자기가 놓친 통찰로 이끌 수도 있다고 적는다. **유일한 물음은 어느
  지도든 쓸모 있는가다** (3장, pp.51–52).[^urquhart2021]

## 이 KB의 이웃과 맞대는 자리

**이 절의 대조는 이 KB가 세운 것이다** — 이 소스는 아래 소스들을 한 건도 인용하지 않는다. 이 페이지는
`contradicts`를 한 쌍도 걸지 않았다.

- **"진화"라는 낱말이 이 KB에서 두 대상을 가리킨다. 겨루지 않는다.**
  [진화적 아키텍처](../concepts/evolutionary-architecture.md)의 진화는 **한 체계가 시간에 따라
  변경되는 능력**을 가리키고, 그 뜻을 가장 뚜렷하게 보이는 것은 진화 가능성이 다른 아키텍처 특성을
  감싸는 메타 특성이라는 배치다. 여기의 진화는 **한 기술 범주가 시장에서 갓 생긴 것에서 상품으로
  굳어 가는 이행**이고, 재는 것이 한 체계가 아니라 한 범주의 확실성과 보편성이다. 같은 철자가
  **한쪽에서는 설계의 성질이고 다른 쪽에서는 시장의 상태**다. 어느 한쪽만 참일 수 있는 문장 쌍이
  아니라 이름이 겹친 두 축이다.
  [아키텍처 적합도 함수](../concepts/architecture-fitness-functions.md)도 같은 이유로 맞대지 않는다 —
  그쪽의 적합도는 한 체계의 특성이 기준을 지키는가이고 워들리의 진화 단계에는 지킬 기준이 없다.
- **불변 기술과 일시 기술의 가름이 같은 물음에 다른 잣대로 답한다. 겨루지 않는다.**
  [기술 선택의 기준](../concepts/technology-selection-criteria.md)은 린디 효과로 불변 기술과 일시
  기술을 가르고 2년 주기의 재평가를 처방한다. 재는 것은 **오래 살아남았는가**이고, 워들리의 척도가
  재는 것은 **그 범주를 두고 쓰이는 글이 어느 단계에 있는가**다. 두 잣대가 같은 방향을 가리키는
  일이 많겠지만 **한쪽은 생존 기간을 쓰고 다른 쪽은 담론의 성격을 쓴다.** #hypothesis 둘이 같은
  판정을 낼 것이라는 읽기는 이 KB가 붙인 것이고 어느 저자도 상대를 인용하지 않는다.
- **하위 도메인의 세 종류와 축이 다르다. 겨루지 않는다.**
  [하위 도메인의 세 종류](../concepts/subdomain-types.md)는 핵심과 보조와 일반을 **업무 차별화와 업무
  로직 복잡성** 두 축에 놓는다. 워들리의 진화 단계는 **기술 범주의 시장 성숙도**를 잰다. 두 분류가
  닮아 보이는 것은 결론이 비슷해서다 — 일반 하위 도메인은 사서 쓰고 상품 단계의 구성 요소도 사서
  쓴다. 그러나 **일반 하위 도메인은 "우리에게 차별화가 아니다"라는 조직 쪽 판정이고 상품 단계는
  "시장 전체에서 규격이 굳었다"는 시장 쪽 판정이다.** 조직에 차별화가 되면서도 아직 제네시스인
  구성 요소가 있을 수 있어 두 축이 어긋난다.
- **제프리 무어의 이름이 이 KB에서 두 번째로 나온다.** 같은 소스의 2장이 무어의 핵심 대 맥락(core
  versus context)을 쓰고, 3장은 무어의 *Crossing the Chasm*을 로저스의 확산 논의가 서술된 자리로만
  든다. **두 자리는 다른 책의 다른 논지이고 이 소스는 둘을 잇지 않는다.**

## 이어지는 페이지

- [약속 이론](promise-theory.md) — 같은 장이 이 기법과 짝으로 쓰는 다른 모형화 도구. 지도의 구성 요소
  사이에 그은 선이 옳은지 검증하는 자리
- [플로 통합 가치 사슬 지도](flow-integration-value-chain.md) — 이 기법을 실제로 한 지형에 적용한
  결과. 범위 진술과 사용자 요구와 구성 요소 아홉과 그 진화 배치
- [플로 구성 요소의 진화 예측](flow-component-evolution-forecast.md) — 이 기법의 **게임플레이**가
  이 KB에서 처음 서술되는 자리. 워들리가 식별한 행동 예순하나와 범주 열하나, 그리고 관성을 실선
  막대로 그리는 표기가 거기 있다
- [진화적 아키텍처](../concepts/evolutionary-architecture.md) — 같은 철자를 한 체계의 변경 능력에
  쓰는 쪽
- [기술 선택의 기준](../concepts/technology-selection-criteria.md) — 같은 물음을 도구 선택의 기준으로
  세우는 쪽
- [하위 도메인의 세 종류](../concepts/subdomain-types.md) — 같은 "무엇을 사고 무엇을 지을 것인가"를
  도메인 쪽 축으로 가르는 쪽
- [트레이드오프 분석 방법](../concepts/trade-off-analysis-method.md) — 이 축에서 결정을 고르는 절차의
  정본 자리
- [소프트웨어 아키텍처](../synthesis/software-architecture.md) — 이 축의 허브

[^urquhart2021]: Urquhart 2021 초판, 3장 "Understanding the Flow Value Chain"에서 기법 자체를 다루는
    구간 — §"Wardley Mapping and Promise Theory"의 소절 "Wardley Mapping"(pp.47–48) ·
    §"Building a Flow Integration Value Chain"의 소절 "Establishing a Scope for the Map"(pp.51–52) ·
    §"Mapping Our Value Chain"의 도입부와 소절 "Determining a Measure of Technology
    Evolution"(pp.61–64) · 그 소절 안의 곁상자 "What Is a Map?"(pp.64–65)이다. 이 범위의 내용 각주
    둘(3번 p.53의 구성 요소 논의, 5번 p.61의 전화 농담)도 함께 읽었다.
    쪽은 인쇄판 쪽 번호(본문 = PDF 쪽 − 26, 실측).
    **제목 층은 `pdftotext -bbox` 글자 높이로 갈랐다** — 장 제목 30.2, 절 제목 22.7, 소절 제목 18.9,
    셋째 층 소제목 13.8, 본문 14.2(이탤릭 14.3), 인용 블록 12.5, 표 캡션 13.6, 표 본문 10.7,
    러닝 푸터와 각주 본문 10.8이다. **곁상자는 제목 18.0에 본문 13.5로 본문과 갈린다** — 3장의
    곁상자는 "What Is a Map?" 하나뿐이고, 그 안의 그림 캡션은 13.6으로 본문 그림 캡션(14.3)보다
    작다. 진행 파일 머리말이 1장 표본으로 적은 곁상자 본문 13.0과는 다른 값이라 이 장에서 새로 쟀다.
    **직인용 둘은 `pdftotext -layout` 추출로 문자 단위 대조했다** — 지도의 규정 한 문장(p.64)과
    진화 단계 넷의 규정(pp.62–63)이다. 원문에서 줄 끝 하이픈으로 갈린 낱말은 이어 붙였고, 단계
    이름은 원문의 정의 목록 형태를 인용 블록 안에서 빈 줄로 갈라 옮겼다.
    **도판 셋을 `pdftoppm -r 160 -png` 렌더로 눈으로 대조했다** — 그림 3-1(p.48, 찻집 지도) ·
    그림 3-16(p.62, 겹친 확산 곡선) · 그림 3-17(p.63, 표준 기술 확산 곡선)이다. 곁상자의 그림
    3-18(p.64, 체계 다이어그램)과 3-19(p.64, 영국 지도)도 렌더로 보았다. **찻집 지도의 노드 아홉과
    간선과 배치, 두 축의 이름과 눈금, 확산 곡선 두 그림의 축 이름과 수요·공급 표기는 전부 그림에만
    있고 본문에 없다.** 이 범위에 표와 코드 목록은 없다.
    **저자가 대는 바깥 서지는 전부 2차 경유다** — 사이먼 워들리의 연작 블로그 글과 2015년 글,
    에버렛 로저스, 제프리 무어의 *Crossing the Chasm*이 그것이다. 이 KB가 확인한 원전이 아니므로
    귀속은 "이 책이 그렇게 적는다"까지로 둔다.

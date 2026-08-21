---
type: concept
status: draft
title: 일관성 오라클 휴리스틱
description: 명세가 없을 때 기대를 무엇에 비추어 만드는가 — 문제를 알아보는 근거를 관계된 것들 사이의 바람직한 일관성으로 규정하고 그 관계를 열한 항목으로 목록화한 실무 카탈로그, 2005년 여덟 항목(HICCUPPS)에서 2012년 열한 항목((F)EW HICCUPPS)으로의 계보와 U 항목 개명, 저자 자신이 밝힌 오류 가능성과 비완전성, 그리고 이 카탈로그가 오라클 네 출처 분류의 어디에 앉는가
generated: { by: "claude-opus-5", at: "2026-08-21T00:00:00Z" }
sources:
  - { id: bolton2012-few-hiccupps, resource: /it/sources/bolton2012-few-hiccupps.md }
  - { id: bolton2005-testing-without-a-map, resource: /it/sources/bolton2005-testing-without-a-map.md }
---

# 일관성 오라클 휴리스틱

- [이 소스의 지위 — 실무 휴리스틱이지 학술 근거가 아니다](#이-소스의-지위--실무-휴리스틱이지-학술-근거가-아니다)
- [출발점 — "기대에 못 미친다"는 동어반복이다](#출발점--기대에-못-미친다는-동어반복이다)
- [오라클과 휴리스틱의 규정](#오라클과-휴리스틱의-규정)
- [카탈로그 — 열한 항목](#카탈로그--열한-항목)
- [계보 — 여덟에서 열하나로](#계보--여덟에서-열하나로)
- [Claims와 Statutes를 가르는 선](#claims와-statutes를-가르는-선)
- [카탈로그가 스스로 밝히는 한계](#카탈로그가-스스로-밝히는-한계)
- [오라클 네 출처 분류의 어디에 앉는가](#오라클-네-출처-분류의-어디에-앉는가)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **명세가 없을 때, 무엇이 옳은 동작인가에 대한 기대는 무엇에 비추어
만들어지는가.**

## 이 소스의 지위 — 실무 휴리스틱이지 학술 근거가 아니다

이 페이지의 두 소스는 잡지 기사와 블로그 글이다. 측정도, 통제 실험도, 결과 표도
없다. **근거 등급은 실무 휴리스틱(heuristic)이고, 이 페이지의 어떤 문장도 학술
실증으로 인용되지 않는다.** 두 소스가 이 목록의 항목을 부르는 이름 자체가
휴리스틱이며, 지위는 저자 자신의 규정으로 밝힌다.

- **2005년 기사의 자기 규정** (인쇄 26쪽).[^bolton2005-testing-without-a-map]

  > Remember: Heuristics are guidelines, not edicts; they're fallible. They aren't
  > universal—there are plenty of other ways by which we can decide whether a product
  > is acceptable or unacceptable.

- **2012년 글의 자기 규정** (§휴리스틱 단서).[^bolton2012-few-hiccupps]

  > Each of these principles is heuristic. Oracle principles are, like all heuristics,
  > fallible and context-dependent; to be applied, not followed.

- **오라클은 사람을 속이기도 한다** — 원칙 하나와 어긋난다고 해서 문제가 있다는
  보장이 없고, 문제인가 아닌가의 판정은 사람이 여러 오라클 원칙과 가치 관념을 적용해
  내린다. 오라클 자체가 **없는 문제를 보게 하거나 있는 문제를 놓치게** 할 수 있다
  (§휴리스틱 단서).[^bolton2012-few-hiccupps]

## 출발점 — "기대에 못 미친다"는 동어반복이다

- **이 카탈로그가 겨냥한 공백** — 테스터는 흔히 제품이 "기대에 못 미칠(doesn't meet
  expectations)" 때 문제를 알아본다고 말하지만, 저자는 그것을 **공허한 동어반복**으로
  본다. 테스터의 신뢰도는 **자기 기대가 어디서 왔는지를 말할 수 있을 때** 올라간다
  (§도입).[^bolton2012-few-hiccupps]

  > Testers often say that they recognize a problem when the product doesn't "meet
  > expectations". But that seems empty to me; a tautology. Testers can be a lot more
  > credible when they can describe where their expectations come from.

- **그래서 기대를 관계로 다시 규정한다** (§도입).[^bolton2012-few-hiccupps]

  > Expectations about a product revolve around desirable consistencies between related
  > things.

  기대는 제품 안에 있는 성질이 아니라 **제품과 다른 무언가 사이의 관계**다. 카탈로그의
  각 항목은 그 "다른 무언가"의 자리를 하나씩 채운다.
- **문제를 알아보는 형식** — 일반적으로 제품이나 시스템이 이 원칙들 중 하나 이상과
  **불일치(inconsistent)**하는 것을 관측했을 때 문제를 의심할 근거가 생긴다
  (§일반론 문단).[^bolton2012-few-hiccupps]
- **목록을 외우는 이유가 명시돼 있다** — 오라클이 문제를 알아보는 방식이므로 이런
  목록을 머릿속에 두면 문제를 알아볼 준비가 된다. 그리고 **막연한 문제 보고를 특정
  오라클 원칙으로 지목해 개선할 수 있다** — 의사결정자가 왜 그것이 문제인지 이해할 수
  있을 때 테스터의 보고가 더 신뢰받는다 (§니모닉 문단·그 다음
  문단).[^bolton2012-few-hiccupps]

## 오라클과 휴리스틱의 규정

두 낱말의 규정은 2005년 기사에 있다 (인쇄 26쪽).[^bolton2005-testing-without-a-map]

> An oracle is a principle or mechanism by which we can tell if the software is working
> according to someone's criteria; an oracle provides a right answer—according to
> somebody. A heuristic is a provisional and fallible guide by which we investigate or
> solve a problem; it's also a method by which learning takes place as a result of
> discoveries informed by exploration.

- **"according to somebody"가 이 규정의 핵이다.** 오라클은 절대적 정답을 주는 것이
  아니라 **누군가의 기준에 따른** 정답을 준다. 판정의 주체가 규정 안에 들어 있다.
- **기사 전체의 논지가 부제 한 줄에 있다** (인쇄
  25쪽).[^bolton2005-testing-without-a-map]

  > You don't always need to wait for complete specifications to start your testing
  > effort.

## 카탈로그 — 열한 항목

각 항목의 뜻은 2012년 문면 그대로다. 한국어는 해설이고 의미는 원문이 담는다.

**F · Familiarity(친숙함)** — 유일하게 **불일치 휴리스틱**이다. 제품이 익숙한 문제
패턴과 *닮지 않기를* 기대한다 (§Familiarity).[^bolton2012-few-hiccupps]

> We expect the system to be inconsistent with patterns of familiar problems.

- 낯선 제품에서 빨리 발판을 얻는 방법이지만 오도할 수 있다 — 한 제품에서 중대한
  문제(상용 제품의 UI 마감 같은)가 다른 맥락(사내 사용자용 애플리케이션)에서는 덜
  중대할 수 있다 (§Familiarity).[^bolton2012-few-hiccupps]
- **이 항목은 다른 항목으로 환원된다**고 저자가 못 박는다
  (§Familiarity).[^bolton2012-few-hiccupps]

  > Note that any pattern of familiar problems must eventually reduce to one of the
  > consistency heuristics; if it was a problem before, it was because the system was
  > inconsistent with some oracle principle.

**E · Explainability(설명 가능성)** (§Explainability).[^bolton2012-few-hiccupps]

> We expect a system to be understandable to the degree that we can articulately explain
> its behaviour to ourselves and others.

- 설명할 수 없다는 것은 **두 갈래**로 문제다 — 제품에 가치를 위협하는 문제가 있거나,
  우리가 제품을 테스트할 만큼 알지 못하거나. 저자는 **후자가 더 큰 문제**라고 적는다:
  오해는 없는 문제를 보고하게 만들어 시간을 낭비시키고, 더 나쁘게는 눈앞의 진짜 문제를
  못 알아보게 만든다 (§Explainability).[^bolton2012-few-hiccupps]
- 이 휴리스틱은 테스터에 국한되지 않는다 — 프로그래머가 자기가 유지보수하는(또는 자기가
  쓴) 코드를 설명하지 못하면 그것도 같은 신호다. 저자는 독자(Aleksander Simic)의 사신
  제안을 본문에 받아들여 이렇게 확장하고, **제품 안의 어떤 종류의 혼란도 이슈이며
  이슈는 버그의 배양 접시**라고 적는다 (§Explainability).[^bolton2012-few-hiccupps]

**W · World(세계)** (§World).[^bolton2012-few-hiccupps]

> We expect the product to be consistent with things that we know about or can observe
> in the world.

- 이 휴리스틱은 **우리 쪽 지식이 틀렸을 때** 실패한다 — 잘못 알고 있거나 잘못 기억할
  때다. 또한 **제품이 우리가 몰랐던 세계의 사실을 드러낼 때**도 실패한다
  (§World).[^bolton2012-few-hiccupps]

**H · History(이력)** (§History).[^bolton2012-few-hiccupps]

> We expect the present version of the system to be consistent with past versions of it.

**I · Image(이미지)** (§Image).[^bolton2012-few-hiccupps]

> We expect the system to be consistent with an image that the organization wants to
> project, with its brand, or with its reputation.

**C · Comparable Products(비교 가능한 제품)** (§Comparable
Products).[^bolton2012-few-hiccupps]

> We expect the system to be consistent with systems that are in some way comparable.
> This includes other products in the same product line; competitive products, services,
> or systems; or products that are not in the same category but which process the same
> data; or alternative processes or algorithms.

**C · Claims(주장)** (§Claims).[^bolton2012-few-hiccupps]

> We expect the system to be consistent with things important people say about it,
> whether in writing (references specifications, design documents, manuals, whiteboard
> sketches…) or in conversation (meetings, public announcements, lunchroom
> conversations…).

- **명세는 이 항목의 한 사례일 뿐이다.** 명세·설계 문서·매뉴얼과 함께 회의·구두 발표·
  점심 대화가 같은 자리에 놓인다. 명세가 없어도 이 오라클은 대개 남아 있다.

**U · Users' Desires(사용자의 바람)** (§Users' Desires).[^bolton2012-few-hiccupps]

> We believe that the system should be consistent with ideas about what reasonable users
> might want.

- **이름이 바뀐 항목이다.** 원래는 "user expectations"였고, 그 기대라는 것이 대개 여기
  나열된 다른 오라클들이나 바람에 뿌리를 둔 품질 기준에 기반하기 때문에 "user desires"로
  바꾸었다 — 글 안의 갱신 주석이 2014-12-05 날짜로 그렇게 적는다 (§Users'
  Desires).[^bolton2012-few-hiccupps]

**P · Product(제품 자신)** (§Product).[^bolton2012-few-hiccupps]

> We expect each element of the system (or product) to be consistent with comparable
> elements in the same system.

**P · Purpose(목적)** (§Purpose).[^bolton2012-few-hiccupps]

> We expect the system to be consistent with the explicit and implicit uses to which
> people might put it.

- **명시적 용도만이 아니라 암묵적 용도**까지 든다는 것이 이 항목의 폭이다.

**S · Statutes and Standards(법규와 표준)** — 앞쪽 목록에서는 Statutes로만
나오고, 뒤의 확장 문단이 Standards를 합쳐 다시 규정한다 (§Statutes·§Statutes
and Standards).[^bolton2012-few-hiccupps]

> We expect a system to be consistent with relevant statutes, acts, laws, regulations,
> or standards.

앞쪽 목록의 문면은 이쪽이다 (§Statutes).[^bolton2012-few-hiccupps]

> We expect a system to be consistent with laws or regulations that are relevant to the
> product or its use.

- 법·규정은 대개 **바깥 권위**가 부과하고, 표준은 부과된 것일 수도 자발적인 것일 수도,
  명시적일 수도 암묵적일 수도, 개발 조직 바깥의 것일 수도 안의 것일 수도 있다
  (§Statutes and Standards).[^bolton2012-few-hiccupps]
- **표준을 아는 테스터가 보는 것** — 공표된 UI 관례, 특정 RFC, 또는 프로젝트가
  통제하지 않는 비공식 내부 코딩 표준과의 불일치다. 저자는 그것이 문제인지 아닌지를
  단정하지 않고 **이슈(issue)**로 둔다: 제품 책임자가 그 표준을 따를지, 일부를 어길지,
  통째로 기각할지 밝히기 전까지는 이슈다 (§Statutes and
  Standards).[^bolton2012-few-hiccupps]

## 계보 — 여덟에서 열하나로

- **2005년 판은 여덟 항목이고, 목록의 출처가 문면에 있다** (인쇄
  26쪽).[^bolton2005-testing-without-a-map]

  > James Bach has given us a helpful set of oracle heuristics, to which I've added one,
  > in the form of this mnemonic: HICCUPPS. The idea is that a product should be
  > consistent with:

  그 뒤에 History · Image · Comparable products · Claims · Users' expectations ·
  The Product itself · Purpose · Statutes 여덟이 이어진다. 그러므로 **Bach의 일곱에
  Bolton이 하나를 더해 여덟**이다 — 다만 이 뺄셈은 이 KB가 한 것이고, 기사는 "일곱"이라는
  수를 적지 않는다. **어느 항목이 Bolton의 것인지도 기사가 밝히지 않는다.**
- **2012년 글이 판을 다시 연다** — 기사가 나온 지 오래되었고 그 사이 Bach와 Bolton은
  테스터들이 다른 오라클 원칙을 쓰는 것을 관찰했다. 저자는 **2005년 이후 두 사람 중
  누구도 수업·발표·비공식 대화 바깥에서 통합 목록을 낸 적이 없다**고 적으며 새 목록을
  낸다 (§새 항목 도입).[^bolton2012-few-hiccupps]
- **니모닉이 재편된 경위** (§니모닉 재편).[^bolton2012-few-hiccupps] 새로 알아챈 것은
  Standards가 먼저였고 그 다음이 Familiar problems였다. Standards는 별도 글자가 되지 않고
  **Statutes에 접혀 들어갔고**, Familiarity는 한동안 `HICCUPPS(F)`로 뒤에 매달려 있었다.
  Explainability와 World가 더해지면서 F를 앞으로 옮겨 **(F)EW HICCUPPS**가 되었다 —
  테스터가 대개 익숙한 문제부터 찾기 시작한다는 현실을 강조하는 배치라고 저자는 적는다.
- **그래서 산수는 이렇게 맞는다.** 글자 수로는 여덟(2005) 더하기 셋(F·E·W) = 열하나
  (2012)다. 새로 알아챈 **휴리스틱**은 넷(Standards·Familiarity·Explainability·World)이지만
  Standards가 S에 접혀 글자를 늘리지 않았다.
- **U 항목의 개명은 2012년이 아니라 그 뒤다.** 개명 주석에 박힌 날짜는 2014-12-05이고,
  같은 글의 §니모닉 문단은 지금도 `User expectations (since then, changed to "user
  desires")`로 옛 이름을 남긴다 (§Users' Desires·§니모닉
  문단).[^bolton2012-few-hiccupps] 저자는 2005년 기사에 대해서도 같은 방향의 정정을
  덧붙인다 — **오늘 그 기사를 쓴다면 expect를 desire로 바꾸겠다**
  (§일반론 문단).[^bolton2012-few-hiccupps]
- **문서가 살아 있다는 사실 자체가 이 계보의 조건이다.** 2012년 글은 발행 뒤에도
  고쳐졌다 — 글 말미가 2016-12-18과 2017-01-26의 수정을 스스로 새긴다 (§개정
  스탬프).[^bolton2012-few-hiccupps] 이 페이지가 인용하는 문면은 **2026-08-21에 확보한
  스냅샷**이고, 그 시점의 문면이다.

## Claims와 Statutes를 가르는 선

두 항목이 겹쳐 보이는 자리를 저자가 직접 가른다 (§Statutes and
Standards).[^bolton2012-few-hiccupps]

> What's the difference between Standards and Statutes versus Claims? Claims come from
> inside the project. For Standards and Statutes, the mandate comes from outside the
> project.

- **경계는 내용이 아니라 출처다.** 개발 조직이 어떤 표준을 따르기로 스스로 정하거나
  요구사항 문서가 법규를 인용하면, 그 순간 그것은 **주장(Claims)**이 되어 문제를 알아볼
  근거가 된다.
- **Standards가 따로 필요했던 이유** — 아직 아무 명시적 주장도 만들어지지 않은 상태에서
  테스터가 잠재적 문제를 알아보는 일이 있기 때문이다
  (§Statutes and Standards).[^bolton2012-few-hiccupps] 즉 **주장의 부재가 오라클의
  부재를 뜻하지 않는다**는 것이 이 항목의 존재 이유다.

## 카탈로그가 스스로 밝히는 한계

- **완전하지 않고, 완전함을 증명할 수도 없다** (§맺음).[^bolton2012-few-hiccupps]

  > This isn't an exhaustive list. Even if we were silly enough to think that we had an
  > exhaustive list of consistency principles, we wouldn't be able to prove it exhaustive.
  > For that reason, we encourage testers to develop their own models of testing,
  > including the models of consistency that inform our oracles.

- **항목끼리 겹친다.** 2005년 기사가 그것을 먼저 인정한다 — 몇몇 항목 사이에는 개념적
  중첩이 있지만, 탐험가에게는 새 영토의 지형도 서로 겹친다
  (인쇄 26쪽).[^bolton2005-testing-without-a-map] 그래서 이 목록은 **분류 체계가 아니라
  상기 장치**다. 한 문제가 여러 항목에 동시에 걸리는 것이 정상이다.
- **적용하는 것이지 따르는 것이 아니다.** 위 §이 소스의 지위가 인용한 "to be applied,
  not followed"가 이 목록의 사용법을 규정한다 — 체크리스트로 소진하는 물건이 아니다.

## 오라클 네 출처 분류의 어디에 앉는가

이 절은 두 소스의 주장이 아니라 **이 KB의 읽기**다. 두 소스 중 어느 쪽도
[테스트 오라클](../concepts/test-oracle.md)의 네 출처 분류를 언급하지 않는다.

- **Claims와 Statutes and Standards는 명세 오라클 쪽에 가깝다.** 다만 결정적인 차이가
  있다 — 서베이 쪽의 명세 오라클이 **형식 명세**를 전제하는 데 반해, Claims는 매뉴얼·
  회의·복도 대화까지 오라클의 재료로 센다. 형식 명세의 부재가 판정 근거의 부재가
  아니라는 것이 이 카탈로그의 주장이다.
- **History와 Comparable Products와 Product는 파생 오라클과 정확히 겹친다.** History는
  이전 판본을 오라클로 쓰는 회귀 테스트와 같은 구조이고, Comparable Products는 독립
  구현을 대조하는 의사 오라클(pseudo-oracle)의 비형식판이며, Product는 같은 시스템 안의
  비교 가능한 요소들 사이에 관계를 거는 것이라 메타모픽 관계와 같은 꼴이다.
- #hypothesis **나머지 다섯은 서베이의 암묵 오라클이 아니라 네 번째 갈래에 앉는다.**
  서베이의 암묵 오라클은 **도메인 지식도 형식 명세도 필요로 하지 않는** 판정(크래시·
  버퍼 오버플로)으로 좁게 규정된다. 그런데 Image·Users' Desires·Purpose·World·
  Explainability는 전부 **사람이 가진 도메인 지식과 가치 판단**을 요구한다. 그러므로
  이들은 자동 오라클이 아니라 **자동 오라클이 없을 때 사람이 판정하는 자리**에 놓인다.
  Familiarity도 마찬가지이고, 게다가 저자 스스로 그것이 다른 일관성 항목으로 환원된다고
  적었다.
- #hypothesis **그래서 이 카탈로그의 기여는 네 번째 갈래를 안에서 쪼갠 것이다.** 서베이는
  그 갈래를 "인간 오라클 비용"이라는 한 덩어리로 두고 비용을 줄이는 법을 다룬다. 이
  카탈로그는 같은 자리에서 **사람이 실제로 무엇에 비추어 판정하는지를 열거**한다. 비용을
  재는 축과 근거를 열거하는 축은 다른 축이고, 둘은 경쟁하지 않는다.

## LLM 시대의 지위

이 절도 원 소스의 주장이 아니라 이 KB의 읽기다. 두 소스는 각각 2005년과 2012년의
글이고, 그 뒤 저자가 이 목록을 다시 잰 기록은 이 KB에 없다 — 지위는 여전히 실무
휴리스틱이다.

- #hypothesis **호출자가 새로 생겼다.** 이 카탈로그가 겨냥한 상황("형식 명세가 없는데
  지금 판정해야 한다")은 생성 모델에 프롬프트를 주고 산출물을 받는 자리의 기본 조건과
  같다. 프롬프트는 명세의 자리에 서지만 명세가 아니다 — 완전하지 않고, 모호하며,
  대화·회의·복도 대화와 같은 층위의 진술이다. 이 카탈로그의 Claims 항목이 바로 그
  층위를 오라클로 세어 주는 항목이다.
- #hypothesis **"기대에 못 미친다"는 동어반복은 모델 산출물 평가에서 되풀이된다.**
  산출물이 "좋다·나쁘다"로 판정될 때 그 판정의 근거가 어디서 왔는지 말할 수 없으면,
  2012년 글이 지적한 그 공허함이 그대로 재현된다. 열한 항목은 그 근거를 지목할 어휘를
  준다.
- #hypothesis **Explainability 항목이 이 시대에 특히 무겁다.** "설명하지 못하는 동작은
  제품의 문제이거나 우리가 제품을 모르는 것이고, 후자가 더 큰 문제"라는 진단은 사람이
  읽지 않은 생성 코드에 그대로 걸린다. 저자가 이미 이 항목을 프로그래머에게까지 확장해
  두었다는 점이 그 적용을 막지 않는다.
- **다만 이 목록을 자동화 가능한 판정으로 읽지 않는다.** 저자 자신이 "적용하는 것이지
  따르는 것이 아니다"라고 못 박았고, 항목 대부분이 사람의 가치 판단을 요구한다. 이
  카탈로그를 기계 게이트의 명세로 바꾸는 것은 소스가 지지하지 않는 사용이다.

## 이어지는 페이지

- [테스트 오라클](../concepts/test-oracle.md) — 이 축의 개념 정본. 오라클을 부분 함수로
  규정하고 오라클 정보의 네 출처를 가르는 자리이며, 이 카탈로그가 그 분류의 어디에
  앉는지는 위 절이 판정한다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  판정 근거가 있어도 통과가 무엇을 증명하지 않는가
- [속성 기반 테스트](../concepts/property-based-testing.md) — 같은 "기대를 어디서
  구하는가"에 대한 기계화된 답. 이쪽이 사람의 일관성 판단이라면 그쪽은 형식화된 속성이다
- [자기 테스트 코드](../concepts/self-testing-code.md) — 기대값을 사람이 짓는 자리와 그 절차
- [현재 동작을 오라클로 쓴다는 것](../concepts/current-behaviour-as-oracle.md) — 이 목록의
  History 항목 하나에만 기대었을 때 무엇이 남는가의 실증. 이전 판본이 아니라 지금 판본과의
  일관성을 재면 판별력이 사라진다
- [특성화 테스트](../concepts/characterization-test.md) — 같은 History 항목을 다섯 단계
  절차로 편 실무 규범. 기록과 보존은 하고 옳음 판정은 하지 않는다는 경계가 붙는다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  모델이 기대를 지을 때 무엇에 정렬하는가의 실측. 이 카탈로그가 열거하는 근거 대신 대상의
  현재 동작에 정렬하면 어떻게 되는지가 수치로 나온다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 이 축의 허브

[^bolton2012-few-hiccupps]: Bolton 2012, "FEW HICCUPPS", DevelopSense.
    발행 2012-07-23이고 **살아 있는 문서**다 — 글 말미가 2016-12-18·2017-01-26의 수정을
    스스로 새기고, Users' Desires 항목에 2014-12-05 갱신 주석이 있다. 이 페이지가 인용한
    문면은 **2026-08-21에 확보한 스냅샷**이다. 절 번호가 없으므로 locator는 항목
    이름(§Familiarity 등)이나 문단 역할(§도입·§일반론 문단·§휴리스틱 단서·§니모닉 문단·
    §새 항목 도입·§니모닉 재편·§맺음·§개정 스탬프)로 적었고, 규약의 정본은
    `it/archive/bolton2012-few-hiccupps/_progress.yaml` 머리말이다. 스냅샷에 함께 보존된
    댓글·트랙백 62건은 본문 밖이라 반입하지 않았다 — 다만 §Explainability 안에서 독자의
    사신을 인용해 논지를 확장하는 대목은 본문이다.

[^bolton2005-testing-without-a-map]: Bolton 2005, "Testing Without a Map",
    *Better Software*, January 2005, pp.25–28. 쪽 번호는 **인쇄 폴리오**이고 PDF 쪽수와
    어긋난다(PDF 1쪽 = 폴리오 없는 전면 일러스트, PDF 2쪽 = 인쇄 25쪽). 확보본 문면에
    **권·호는 인쇄돼 있지 않다** — 쪽바닥이 `www.stickyminds.com JANUARY 2005 BETTER
    SOFTWARE 25`까지만 준다. snapshot.py 판정은 `mixed`(신뢰도 0.74, OCR 필요 1/5쪽)라
    직인용은 쪽 이미지 육안 대조를 거친 것만 썼다(인쇄 25·26쪽 대조 완료). 인쇄 27–28쪽의
    Nero Cover Designer 사례와 Figure 1–6은 이 페이지의 범위 밖이라 옮기지 않았다.

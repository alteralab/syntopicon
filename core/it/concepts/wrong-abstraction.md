---
type: concept
title: 잘못된 추상
description: 중복이 잘못된 추상보다 싸다는 명제와 그것을 뒷받침하는 여덟 단계 서사 — 추상이 만들어지고 매개변수와 조건문이 쌓여 이해 불가능해지는 경로, 그 코드를 버리지 못하게 만드는 매몰 비용 오류, 잘못된 추상을 알아보는 징후, 인라인으로 중복을 되살리는 세 걸음 처방, 그리고 이 명제가 DRY 최대주의와 실제로 어디까지 갈리는가에 대한 판정
generated: { by: "claude-opus-5", at: "2026-08-18T05:00:00Z" }
sources:
  - { id: metz2016-wrong-abstraction, resource: /it/sources/metz2016-wrong-abstraction.md }
  - { id: martin2008, resource: /it/sources/martin2008.md }
---

# 잘못된 추상

- [명제](#명제)
- [여덟 단계 서사](#여덟-단계-서사)
- [왜 못 버리는가 — 매몰 비용](#왜-못-버리는가--매몰-비용)
- [징후 — 매개변수와 조건 분기](#징후--매개변수와-조건-분기)
- [처방 — 인라인해서 중복을 되살린다](#처방--인라인해서-중복을-되살린다)
- [인라인하고 나면 드러나는 것](#인라인하고-나면-드러나는-것)
- [DRY 최대주의와 어디까지 갈리는가](#dry-최대주의와-어디까지-갈리는가)
- [이 KB의 다른 소스들과의 자리](#이-kb의-다른-소스들과의-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **이미 만든 추상이 틀렸다는 것을 어떻게 알고, 그때 무엇을 하는가.**

## 명제

저자가 2014년 RailsConf 발표에서 단언했다고 밝히는 문장이다
(§여덟 단계 서사 앞):[^metz2016-wrong-abstraction]

> duplication is far cheaper than the wrong abstraction

그리고 발표 요약에서 처방으로 옮긴 문장 (§여덟 단계 서사
앞):[^metz2016-wrong-abstraction]

> prefer duplication over the wrong abstraction

- **반응의 크기가 문제의 크기를 알려 줬다고 적는다** — **반응의 강도는 "잘못된 추상"
  문제가 얼마나 널리 퍼져 있고 다루기 힘든지 깨닫게 해 주었다** (§여덟 단계 서사
  앞).[^metz2016-wrong-abstraction] 저자는 **몇몇은 내가 제정신을 잃었다고 했다**고도
  적는다.
- **이 명제는 중복을 옹호하는 것이 아니다.** 비교 대상이 "추상 일반"이 아니라 **잘못된**
  추상이다. 아래 [DRY 최대주의와 어디까지 갈리는가](#dry-최대주의와-어디까지-갈리는가)
  절이 그 범위를 따진다.

## 여덟 단계 서사

저자가 질문을 던지고 다니며 찾아낸 패턴이다 (§여덟 단계
서사):[^metz2016-wrong-abstraction]

1. **프로그래머 A가 중복을 본다.**
2. **A가 중복을 뽑아내 이름을 준다.** 새 추상이 생긴다 — 새 메서드일 수도, 새 클래스일
   수도 있다.
3. **A가 중복을 새 추상으로 대치한다.** 저자의 표현으로 — **아, 코드가 완벽하다.
   프로그래머 A는 행복하게 총총 떠난다.**
4. **시간이 흐른다.**
5. **현재의 추상이 거의 완벽하게 들어맞는 새 요구사항이 나타난다.**
6. **프로그래머 B가 그 요구사항을 구현하는 일을 맡는다.** 그리고 여기가 결정적이다 —
   **B는 기존 추상을 지켜야 한다는 의무감을 느끼지만, 모든 경우에 정확히 같지는
   않으므로 매개변수를 받도록 코드를 고치고, 그 매개변수의 값에 따라 조건부로 옳은 일을
   하도록 로직을 더한다.** 결과 — **한때 보편적이던 추상이 이제 경우마다 다르게
   동작한다.**
7. **또 다른 새 요구사항이 온다. 프로그래머 X. 또 다른 매개변수. 또 다른 새 조건문.
   코드가 이해 불가능해질 때까지 반복.**
8. **당신이 이쯤에서 이 이야기에 등장하고, 당신의 삶은 극적으로 나빠진다.**

- **6단계의 "의무감(honor-bound)"이 이 서사의 심장이다.** 코드를 망가뜨리는 것은 게으름이
  아니라 **기존 추상을 존중하려는 성실함**이다. 그래서 이 실패는 규율로 막히지 않는다.

## 왜 못 버리는가 — 매몰 비용

- 진단 (§매몰 비용):[^metz2016-wrong-abstraction]

> Existing code exerts a powerful influence.  Its very presence argues that it is both
> correct and necessary.  We know that code represents effort expended, and we are very
> motivated to preserve the value of this effort.

- **그리고 방향이 뒤집힌다** — **슬프게도, 코드가 더 복잡하고 이해 불가능할수록, 즉 그것을
  만드는 데 들인 투자가 깊을수록, 우리는 그것을 지켜야 한다는 압력을 더 느낀다(매몰 비용
  오류)** (§매몰 비용).[^metz2016-wrong-abstraction]
- 그 심리를 저자가 이렇게 옮긴다 — **우리 무의식이 이렇게 말하는 것 같다: "세상에, 저렇게
  헷갈리는 걸 보니 제대로 만드는 데 한참 걸렸겠군. 분명 정말, 정말 중요한 거야. 저 노력을
  다 헛되게 하는 건 죄악이겠지."** (§매몰 비용).[^metz2016-wrong-abstraction]
- 그대로 밀고 나갈 때의 상태 — **코드는 더 이상 하나의 공통 추상을 표현하지 않고, 대신
  막연히 연관된 여러 발상을 뒤섞은 조건투성이 절차가 되어 버렸다. 이해하기 어렵고 깨뜨리기
  쉽다** (§매몰 비용).[^metz2016-wrong-abstraction]

## 징후 — 매개변수와 조건 분기

**이 글이 주는 판정 기준은 하나이고 조작적이다** (§맺음):[^metz2016-wrong-abstraction]

> If you find yourself passing parameters and adding conditional paths through shared
> code, the abstraction is incorrect.

- 그리고 시간성이 명시된다 — **처음에는 옳았을 수도 있다. 그러나 그날은 지났다**
  (§맺음).[^metz2016-wrong-abstraction] **추상의 옳고 그름이 고정된 속성이 아니라
  요구사항에 대한 상대적 속성**이라는 것이 이 글의 전제다.

## 처방 — 인라인해서 중복을 되살린다

- 조문 (§세 걸음 처방):[^metz2016-wrong-abstraction]

> If you find yourself in this situation, resist being driven by sunk costs.  When dealing
> with the wrong abstraction, the fastest way forward is back.

- 세 걸음 (§세 걸음 처방):[^metz2016-wrong-abstraction]
  1. **추상화된 코드를 모든 호출자에 다시 인라인해 중복을 되살린다.**
  2. **각 호출자 안에서, 넘어오던 매개변수를 보고 그 호출자가 실제로 실행하는 인라인된
     코드의 부분집합을 정한다.**
  3. **이 호출자에 필요 없는 부분을 지운다.**
- 효과 — **이것은 추상과 조건문을 둘 다 없애고, 각 호출자를 그것이 필요로 하는 코드만으로
  줄인다** (§세 걸음 처방).[^metz2016-wrong-abstraction]
- **그리고 끝이 아니다** — **옛 추상을 완전히 없애고 나면 처음부터 다시 시작해서, 중복을
  다시 분리해 내고 추상을 다시 뽑아낼 수 있다** (§세 걸음
  처방).[^metz2016-wrong-abstraction]
  - **이 마지막 문장이 이 글의 범위를 정한다.** 저자는 추상을 포기하라고 하지 않는다.
    **잘못된 추상을 버리고 다시 뽑으라**고 한다.

## 인라인하고 나면 드러나는 것

- 관찰 (§세 걸음 처방):[^metz2016-wrong-abstraction]

> When you rewind decisions in this way, it's common to find that although each caller
> ostensibly invoked a shared abstraction, the code they were running was fairly unique.

  - **이것이 "중복처럼 보였던 것이 중복이 아니었다"의 실물이다.** 이 KB의
    [DRY 원칙](../concepts/dry-principle.md)이 thomas2020에서 옮긴 **코드가 같아도 지식이 다르면
    중복이 아니다**라는 반례와 같은 관찰을, 이쪽은 **사후에** 확인하는 절차로 얻는다.
- 저자가 관찰한 결과의 변화 — 관점이 **"이 코드에 대한 우리 투자를 지켜야 한다"에서
  "이 코드는 한동안 말이 됐지만, 어쩌면 우리가 배울 수 있는 건 다 배웠는지도 모른다"로
  바뀌자 모든 것이 쉬워졌다** (§세 걸음 처방).[^metz2016-wrong-abstraction]
- 맺음 (§맺음):[^metz2016-wrong-abstraction]

> When the abstraction is wrong, the fastest way forward is back.  This is not retreat,
> it's advance in a better direction.

- **유보도 하나 달려 있다** — **때때로 조건문을 몇 개 쌓아서 무슨 일이 벌어지는지 통찰을
  얻는 것이 말이 되기는 하지만, 잘못된 추상은 늦기 전에 일찍 버릴수록 덜 아플 것이다**
  (§맺음).[^metz2016-wrong-abstraction] 즉 즉시 인라인이 아니라 **일찍**이 처방이다.

## DRY 최대주의와 어디까지 갈리는가

이 KB의 [DRY 원칙](../concepts/dry-principle.md) 축에는 이미 네 소스가 있고, 그중
[Clean Code](../sources/martin2008.md)가 최대주의 극에 선다 — **중복은 소프트웨어 만악의
근원일지 모른다**(3장 §"Don't Repeat Yourself", p.48), **찾을 수 있는 곳마다 중복을 찾아
없애라**(17장 `G5`, p.290), 그리고 **코드에서 중복을 볼 때마다 그것은 놓친 추상의 기회를
나타낸다**(17장 `G5`, p.289).[^martin2008]

**슬로건만 보면 정면 충돌로 보인다. 대질해 보면 그렇지 않다.** 판정과 근거는 이렇다.

- **① 두 소스가 같은 실패 모드를 지목하고 구조적으로 같은 처방을 낸다.** 이것이 결정적이다.
  Clean Code의 `G15` **Selector Arguments**가 그 자리다 —
  **선택자 인수는 큰 함수를 여러 작은 함수로 쪼개는 것을 피하려는 게으른 방법일 뿐이다.
  … 일반적으로 동작을 고르는 코드를 함수에 넘기는 것보다 함수를 여럿 두는 편이 낫다**
  (17장 `G15`, p.295).[^martin2008]
  - **이 페이지의 [징후](#징후--매개변수와-조건-분기)가 정확히 그 상황이고**, 처방도
    같은 방향이다 — 공유를 그만두고 특수화하라. 이쪽은 "호출자로 인라인해서 각자 필요한
    것만 남겨라", 저쪽은 "함수를 여럿 두라". **낱말이 다를 뿐 같은 조작이다.**
- **② 두 소스가 다루는 시점이 다르다.** Clean Code의 `G5`는 **중복을 볼 때** 무엇을 할지
  말하고, 이 페이지는 **이미 뽑아낸 추상이 틀어졌을 때** 무엇을 할지 말한다. Clean Code에는
  후자를 다루는 자리가 **없다** — 되돌리는 조작이 그 책의 어휘에 없다. **그것은 공백이지
  반대 주장이 아니다.**
- **③ 그래서 `contradicts`를 걸지 않는다.** 이 KB의 기준은 검증 가능한 사실이나 처방의
  정면 충돌이다. 여기서는 ⓐ 두 소스가 같은 실패 모드에 같은 방향의 처방을 내고 ⓑ 한쪽이
  다루지 않는 국면을 다른 쪽이 다루므로, 같은 명제에 반대 진리값을 주는 자리가 없다.
- **④ 그럼에도 실질적 대비는 남고, 그것이 기본값의 차이다.** Clean Code는 중복 쪽에
  **의심을 기본값으로** 두고("모든 중복은 놓친 추상의 기회"), 이 페이지는 잘못된 추상 쪽에
  의심을 기본값으로 둔다. 같은 상황에서 어느 쪽 위험을 먼저 떠올리느냐가 갈린다. **이
  KB는 그 대비를 [DRY 원칙](../concepts/dry-principle.md)의 두 절로 나란히 보존한다.**
- **⑤ 한 자리는 실제로 갈린다 — 다만 이 소스가 아니라 이 소스를 인용한 2차 문헌 쪽이다.**
  [클린 코드 비판](../concepts/clean-code-criticism.md)이 Clean Code의 DRY 대목을 두고 **더 최근에
  우리는 대체로 약간의 중복이 세상에서 가장 나쁜 것은 아니라고 이해한다; 그것이 더
  명확할 수 있고, 잘못된 추상보다 쌀 수 있다**고 적으며 이 페이지의 명제를 인용한다.
  그것은 시대 구분 주장이지 이 페이지의 주장이 아니다.

## 이 KB의 다른 소스들과의 자리

**이 축에서 이 페이지와 같은 편에 서는 소스가 이미 둘 있다.** 셋 다 서로를 참조한 적이
없다.

- **Ousterhout의 붉은 깃발** — [합칠 것인가 나눌 것인가](../concepts/better-together-or-better-apart.md)가
  중복 제거를 합칠 사유로 인정하면서도, 쪼개기가 실패했을 때의 붉은 깃발을 함께 둔다.
  **그쪽은 뽑아내기가 실패하는 조건을 사전에 판정하려 하고, 이 페이지는 사후에 되돌리는
  절차를 준다.** 두 접근이 배타적이지 않다.
- **Fowler의 삼진 규칙** — [언제 리팩터링하는가](../concepts/when-to-refactor.md)의 **세 번째로 비슷한
  것을 할 때 리팩터링한다**가 같은 문제의 예방 쪽 답이다. 두 번째까지 중복을 그냥 두는
  근거가 **아직 무엇이 공통 지식인지 모른다**는 것이므로 이 페이지의 전제와 같다.
- **Thomas & Hunt의 반례** — [DRY 원칙](../concepts/dry-principle.md)의 **코드가 같아도 지식이 다르면
  중복이 아니다**가 같은 관찰의 사전 판정판이다.
- **그래서 이 축의 지형이 이렇게 정리된다.** 뽑아낼 것인가를 **사전에** 판정하는 셋
  (지식 동일성·삼진 규칙·붉은 깃발)과, 이미 뽑았는데 틀렸을 때 **사후에** 되돌리는 하나
  (이 페이지)다. 그리고 그 넷 반대편에 의심 없는 추출을 기본값으로 두는 하나
  (Clean Code)가 있다.

## 이어지는 페이지

- [DRY 원칙](../concepts/dry-principle.md) — 이 축의 정본. 네 소스가 이미 있고 이 페이지가 반대 극을
  맡는다
- [합칠 것인가 나눌 것인가](../concepts/better-together-or-better-apart.md) — 뽑아내기 실패를 사전에
  판정하려는 쪽
- [언제 리팩터링하는가](../concepts/when-to-refactor.md) — 삼진 규칙. 같은 문제의 예방 쪽 답
- [클린 코드의 발견법 목록](../concepts/clean-code-heuristics.md) — `G5`의 최대주의와 `G15`의 수렴이
  함께 있는 자리
- [작은 함수](../concepts/small-functions.md) — "중복은 만악의 근원"이 나오는 장
- [클린 코드 비판](../concepts/clean-code-criticism.md) — 이 페이지의 명제를 인용해 시대 구분을
  주장하는 2차 문헌
- [기본 리팩터링](../concepts/basic-refactorings.md) — 인라인이 이름 붙은 조작으로 있는 자리
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^metz2016-wrong-abstraction]: Metz 2016, "The Wrong Abstraction". **절 이름은 이 KB가
    매긴 것이다** — 이 글에는 본문 절 제목이 없다. 규약은
    `it/archive/metz2016-wrong-abstraction/_progress.yaml` 머리말이 정본이다. 이 글에는
    코드 예제도 도판도 없다 — 여덟 단계 서사와 세 걸음 처방이 전부 산문이다. 스냅샷
    말미의 저자 저서 광고 절은 본문 밖이라 반입하지 않았다. 인용문 둘("duplication is far
    cheaper…"·"prefer duplication…")은 이 글이 2014년 RailsConf 발표에서 옮겨 온 것이라고
    저자가 밝힌 것이며, **그 발표 자체는 이 KB에 반입돼 있지 않다.**

[^martin2008]: Martin 2008, 3장 §"Don't Repeat Yourself"(p.48) · 17장 `G5`(pp.289–290)·
    `G15`(p.295). **논쟁 중인 소스다** — 지위와 반입 규약은
    `it/sources/martin2008.md`가 정본이다. 쪽은 인쇄판 쪽 번호이며 복원 절차는
    `it/archive/martin2008/_progress.yaml` 머리말이 정본이다.

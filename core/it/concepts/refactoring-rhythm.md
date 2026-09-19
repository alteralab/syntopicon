---
type: concept
title: 리팩터링의 리듬
description: 저자가 1장의 예제 전체에서 가르치려 한 한 가지 — 걸음을 아주 작게 쪼개고 매 걸음 뒤에 컴파일·테스트·커밋해서 코드가 결코 깨진 상태로 머물지 않게 하는 리듬, 그 리듬이 왜 느린 것이 아니라 빠른 것인지, 머릿속 이해를 코드로 옮기는 것이 첫 추출의 동기라는 규정, 구조를 넣으면 코드 줄 수가 늘어난다는 사실과 그 대가에 대한 저자의 셈, 그리고 좋은 코드의 진짜 시험은 바꾸기 쉬운가라는 맺음
generated: { by: "claude-opus-5", at: "2026-08-17T12:00:00Z" }
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
---

# 리팩터링의 리듬

- [예제가 가르치려는 한 가지](#예제가-가르치려는-한-가지)
- [고쳐야 할 이유가 먼저 있어야 한다](#고쳐야-할-이유가-먼저-있어야-한다)
- [첫 걸음은 언제나 테스트다](#첫-걸음은-언제나-테스트다)
- [컴파일-테스트-커밋](#컴파일-테스트-커밋)
- [머릿속 이해를 코드로 옮긴다](#머릿속-이해를-코드로-옮긴다)
- [구조를 넣으면 코드가 길어진다](#구조를-넣으면-코드가-길어진다)
- [세 국면 — 이 예제의 지도](#세-국면--이-예제의-지도)
- [좋은 코드의 진짜 시험](#좋은-코드의-진짜-시험)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **리팩터링(refactoring)을 실제로 할 때 한 걸음의 크기는 얼마이고 걸음
사이에 무엇을 하는가.**

## 예제가 가르치려는 한 가지

이 책의 1장은 연극 공연료 청구서를 출력하는 짧은 자바스크립트 함수 하나를 44쪽에 걸쳐
고쳐 쓰는 예제다. 저자가 그 예제에서 가장 중요하다고 못 박은 것은 기법이 아니라 리듬이다.

- 맺음의 규정 — **그러나 이 예제에서 배울 가장 중요한 것은 리팩터링의 리듬이다. 내가
  리팩터링하는 것을 사람들에게 보여 줄 때마다 그들은 내 걸음이 얼마나 작은지에 놀란다.
  각 걸음이 코드를 컴파일되고 테스트를 통과하는 동작 상태로 남긴다** (1장 §"Final Thoughts",
  p.44).[^fowler2018]
- 그리고 열쇠 — **효과적인 리팩터링의 열쇠는 아주 작은 걸음을 밟을 때 더 빨리 간다는 것,
  코드가 결코 깨지지 않는다는 것, 그리고 그 작은 걸음들을 합쳐 상당한 변경을 만들 수 있다는
  것을 인식하는 것이다** (1장 §"Final Thoughts", p.44).[^fowler2018]
- 저자 자신도 그것을 배워야 했다 — **20년 전 디트로이트의 한 호텔 방에서 Kent Beck이 이것을
  하는 법을 보여 줬을 때 나 자신도 똑같이 놀랐다** (1장 §"Final Thoughts",
  p.44).[^fowler2018]

## 고쳐야 할 이유가 먼저 있어야 한다

- 예제의 시작 코드에 대한 저자의 첫 판정은 "나쁘다"가 아니다 — **내가 먼저 할 말은 그것이
  지금 이대로도 견딜 만하다는 것이다 — 이렇게 짧은 프로그램은 이해하기 위해 깊은 구조를
  요구하지 않는다** (1장 §"Comments on the Starting Program", p.3).[^fowler2018]
- **미학이 아니라는 논증** — **프로그램이 동작하는데, 그 구조에 대한 어떤 진술이든 그저
  미학적 판단, "못생긴" 코드에 대한 혐오에 지나지 않는 것 아닌가? 결국 컴파일러는 코드가
  못생겼는지 깨끗한지 신경 쓰지 않는다. 그러나 내가 시스템을 바꿀 때는 인간이 관여하고,
  인간은 신경 쓴다. 잘못 설계된 시스템은 바꾸기 어렵다 — 무엇을 바꿔야 하는지, 그리고 그
  변경이 원하는 동작을 얻기 위해 기존 코드와 어떻게 상호작용할지 알아내기 어렵기 때문이다**
  (1장 §"Comments on the Starting Program", p.4).[^fowler2018]
- 그래서 계기가 앞선다 — **강조하건대 리팩터링을 수행할 필요를 몰고 오는 것은 이 변경들이다.
  코드가 동작하고 결코 바뀔 필요가 없다면 그것을 그냥 두는 것으로 완벽히 괜찮다. 개선하면
  좋겠지만, 누군가 그것을 이해할 필요가 없는 한 그것은 실제 해를 끼치지 않는다. 그러나
  누군가 그 코드가 어떻게 동작하는지 이해해야 하고 따라가기 어려워하는 순간, 당신은 무언가를
  해야 한다** (1장 §"Comments on the Starting Program", p.5).[^fowler2018]
- 조문 (1장 §"Comments on the Starting Program", p.4):[^fowler2018]

> When you have to add a feature to a program but the code is not structured in a
> convenient way, first refactor the program to make it easy to add the feature, then add
> the feature.

  같은 조문의 다른 표현들과 그 계기 분류는
  [언제 리팩터링하는가](when-to-refactor.md)에 있다.

## 첫 걸음은 언제나 테스트다

- **리팩터링할 때 첫 걸음은 언제나 같다. 그 코드 구간에 대한 견고한 테스트 집합이 있는지
  확인해야 한다. 테스트가 필수인 것은, 내가 버그를 들여올 기회 대부분을 피하도록 구조화된
  리팩터링을 따르더라도 나는 여전히 인간이고 여전히 실수하기 때문이다** (1장 §"The First
  Step in Refactoring", p.5).[^fowler2018] 조문 (1장 §"The First Step in Refactoring",
  p.5):[^fowler2018]

> Before you start refactoring, make sure you have a solid suite of tests. These tests
> must be self-checking.

- 자기 검사가 필수인 이유가 시간 비용으로 제시된다 — **테스트를 자기 검사로 만드는 것이
  필수적이다. 그렇게 하지 않으면 나는 테스트에서 나온 값을 메모지의 값과 손으로 대조하는
  데 시간을 쓰게 될 것이고, 그것은 나를 느리게 만들 것이다** (1장 §"The First Step in
  Refactoring", p.5).[^fowler2018]
- 그리고 테스트가 하는 일의 규정 — **나는 그것들을 내 자신의 실수로부터 나를 지켜 주는
  버그 탐지기로 생각한다. 원하는 것을 코드와 테스트에 두 번 씀으로써, 탐지기를 속이려면
  나는 두 자리에서 일관되게 실수를 해야 한다. 내 작업을 이중으로 확인함으로써 나는 잘못할
  가능성을 줄인다** (1장 §"The First Step in Refactoring", p.5).[^fowler2018] 전문은
  [자기 테스트 코드](self-testing-code.md)에 있다.

## 컴파일-테스트-커밋

- 리듬의 단위 — **이 변경을 하고 나면 나는 즉시 컴파일하고 테스트해서 무언가 깨뜨렸는지
  본다. 아무리 단순하더라도 리팩터링마다 테스트하는 것은 중요한 습관이다. (…) 매 변경 뒤에
  테스트한다는 것은 실수를 했을 때 오류를 짚어 내기 위해 고려할 변경이 작다는 뜻이고, 그것이
  찾고 고치기를 훨씬 쉽게 만든다** (1장 §"Decomposing the statement Function",
  p.8).[^fowler2018]
- **그것이 이 과정의 본질이라고 명시된다** — **이것이 리팩터링 과정의 본질이다: 작은 변경과
  매 변경 뒤의 테스트. 너무 많이 하려 하면 실수가 나를 오래 걸릴 수 있는 까다로운 디버깅
  에피소드로 몰아넣을 것이다. 촘촘한 피드백 루프를 가능하게 하는 작은 변경이 그 난장판을
  피하는 열쇠다** (1장 §"Decomposing the statement Function", p.8).[^fowler2018]
  조문 (1장 §"Decomposing the statement Function", p.8):[^fowler2018]

> Refactoring changes the programs in small steps, so if you make a mistake, it is easy to
> find where the bug is.

- **본문에서 "컴파일-테스트-커밋"(compile-test-commit)이라는 말이 걸음의 구두점으로 반복
  등장한다.** 예제에서 매개변수 하나를 없애는 데만도 그 구두점이 세 번 찍힌다 — 우변을
  함수로 추출하고 컴파일-테스트-커밋, *Inline Variable*을 적용하고 컴파일-테스트-커밋,
  *Change Function Declaration*을 두 걸음으로 나눠 각각 컴파일-테스트-커밋 (1장 §"Removing
  the play Variable", pp.11–13).[^fowler2018]
  - 저자가 `compile`이라는 낱말의 범위를 밝혀 둔다 — **나는 여기서 *컴파일*을 자바스크립트를
    실행 가능하게 만드는 데 필요한 무엇이든 하는 것을 뜻하는 말로 쓴다. 자바스크립트는 직접
    실행 가능하므로 그것은 아무것도 아닐 수 있지만, 다른 경우에는 코드를 출력 디렉터리로
    옮기거나 Babel 같은 처리기를 쓰는 것을 뜻할 수 있다** (1장 §"Decomposing the statement
    Function", p.8).[^fowler2018]
- 이 절차가 성능 걱정을 부를 때의 저자의 답 — 조회가 반복당 한 번에서 세 번으로 늘어나는
  변경에 대해 — **이 변경이 성능에 유의미하게 영향을 줄 가능성이 낮고, 설령 그렇더라도 잘
  인수분해된 코드베이스의 성능을 개선하기가 훨씬 쉽다** (1장 §"Removing the play Variable",
  p.14).[^fowler2018] 전문은 [성능을 위한 설계](../concepts/designing-for-performance.md)에 있다.

## 머릿속 이해를 코드로 옮긴다

- 첫 추출의 동기가 코드 품질이 아니라 **기억의 저장 매체**로 제시된다 — **이 덩어리를 보면서
  나는 그것이 공연 하나의 요금을 계산하고 있다고 결론짓는다. 그 결론은 코드에 대한 통찰
  한 조각이다. 그러나 Ward Cunningham이 말하듯 이 이해는 내 머릿속에 있다 — 악명 높게
  휘발성이 큰 저장 형태다. 나는 그것을 내 머리에서 코드 자체로 도로 옮겨 지속시켜야 한다.
  그래야 나중에 돌아왔을 때 코드가 무엇을 하는지 나에게 말해 준다 — 다시 알아낼 필요가
  없다** (1장 §"Decomposing the statement Function", p.7).[^fowler2018]
- 그리고 그 옮기는 방법이 곧 추출이다 — **그 이해를 코드에 넣는 방법은 그 코드 덩어리를 자기
  함수로 바꾸고 그것이 하는 일을 따라 이름 짓는 것이다** (1장 §"Decomposing the statement
  Function", p.7).[^fowler2018]
- 지역 변수를 먼저 없애는 이유도 같은 절차에서 나온다 — **지역 변수를 없애는 큰 이득은
  추출을 훨씬 쉽게 만든다는 것인데, 다뤄야 할 지역 스코프가 줄기 때문이다. 실제로 나는 보통
  어떤 추출을 하기 전에 지역 변수를 먼저 걷어 낸다** (1장 §"Removing the play Variable",
  p.14).[^fowler2018]
- 이 절차의 반복이 낳는 되먹임이 2장에서 이해 리팩터링으로 정식화된다 — 전문은
  [언제 리팩터링하는가](when-to-refactor.md)에 있다.

## 구조를 넣으면 코드가 길어진다

- 저자가 중간 결산에서 줄 수를 직접 센다 — **시작했을 때보다 코드가 더 많다: (htmlStatement을
  빼고) 44줄이던 것이 70줄이 됐는데, 대부분 함수 안에 넣느라 생긴 여분의 감쌈 때문이다.
  다른 모든 것이 같다면 코드가 더 많은 것은 나쁘다 — 그러나 다른 모든 것이 같은 일은 드물다**
  (1장 §"Status: Separated into Two Files (and Phases)", p.33).[^fowler2018]
- 대가로 얻는 것 — **여분의 코드는 로직을 식별 가능한 부분으로 쪼개 계산과 배치를 분리한다.
  이 모듈성이 코드의 부분들과 그것들이 어떻게 맞물리는지 이해하기 쉽게 만든다** (1장 §"Status:
  Separated into Two Files (and Phases)", p.33).[^fowler2018] 그리고 한 문장으로 압축된다
  (1장 §"Status: Separated into Two Files (and Phases)", p.33):[^fowler2018]

> Brevity is the soul of wit, but clarity is the soul of evolvable software.

- 다형 계산기를 도입한 뒤에도 같은 결산이 반복된다 — **다시, 구조를 도입하면서 코드 크기가
  늘었다. 여기서의 이득은 각 종류의 연극에 대한 계산이 함께 묶인다는 것이다. 변경의 대부분이
  이 코드에 대한 것이라면 이렇게 명확히 분리해 두는 것이 도움이 될 것이다** (1장 §"Status:
  Creating the Data with the Polymorphic Calculator", p.42).[^fowler2018]
- **그리고 그 조건이 명시된다** — **여기서 나는 조건부 조회를 두 함수(`amountFor`와
  `volumeCreditsFor`)에서 단일 생성 함수 `createPerformanceCalculator`로 옮겼다. 같은
  다형성에 의존하는 함수가 많을수록 이 접근이 더 유용해진다** (1장 §"Status: Creating the
  Data with the Polymorphic Calculator", pp.42–43).[^fowler2018] 즉 이 예제가 보이는 것은
  다형성이 언제나 낫다는 것이 아니라 **의존하는 함수의 수가 손익분기를 정한다**는 것이다.
- 균형에 대한 저자의 규칙은 야영 격언의 변주다 — **나는 언제나 내가 할 수 있는 모든 리팩터링과
  새 기능을 더하는 것 사이에서 균형을 잡아야 한다. 2018년 저술 시점에 대부분의 사람들은 리팩터링의 우선순위를
  낮게 두지만 — 그래도 균형은 있다** (1장 §"Status: Separated into Two Files (and Phases)",
  p.34).[^fowler2018] 조문 (1장 §"Status: Separated into Two Files (and Phases)",
  p.34):[^fowler2018]

> When programming, follow the camping rule: Always leave the code base healthier than
> when you found it.

## 세 국면 — 이 예제의 지도

- 저자 자신의 요약 — **이 리팩터링 에피소드에는 세 개의 큰 단계가 있었다: 원래 함수를 중첩
  함수 집합으로 분해하기, *Split Phase*를 써서 계산 코드와 출력 코드를 분리하기, 그리고
  마지막으로 계산 로직에 다형 계산기를 도입하기. 각각이 코드에 구조를 더해 코드가 무엇을
  하는지 더 잘 전달할 수 있게 했다** (1장 §"Final Thoughts", p.43).[^fowler2018]
- **순서에 대한 관찰이 붙는다** — **리팩터링에서 흔히 그렇듯 초기 단계들은 대부분 무슨 일이
  일어나는지 이해하려는 시도가 이끌었다. 흔한 순서는 이렇다: 코드를 읽고, 통찰을 얻고,
  리팩터링을 써서 그 통찰을 머리에서 코드로 도로 옮긴다. 그러면 더 명료해진 코드가 그것을
  이해하기 더 쉽게 만들고, 더 깊은 통찰과 이로운 양의 되먹임 루프로 이어진다** (1장 §"Final
  Thoughts", p.43).[^fowler2018]
- 이 예제에서 쓰인 리팩터링은 *Extract Function*, *Inline Variable*, *Move Function*,
  *Replace Conditional with Polymorphism*이다 (1장 §"Final Thoughts",
  p.43).[^fowler2018] 각각의 절차는 5장 이후 카탈로그의 몫이다.

## 좋은 코드의 진짜 시험

- 저자가 취향 논쟁에서 빠져나가는 방법 — **나는 코드를 개선하는 것에 대해 이야기하고 있지만
  — 프로그래머들은 좋은 코드가 어떤 모습인지를 두고 논쟁하기를 좋아한다. 작고 잘 이름 지어진
  함수에 대한 내 선호에 반대하는 사람들이 있다는 것을 안다. 이것을 미학의 문제로 여긴다면,
  거기서는 생각이 그렇게 만들 뿐 좋은 것도 나쁜 것도 없으므로 우리에게는 개인 취향 말고
  아무 지침도 없다** (1장 §"Final Thoughts", p.43).[^fowler2018]
- 그래서 취향 대신 세우는 시험이 조문이다 (1장 §"Final Thoughts", p.43):[^fowler2018]

> The true test of good code is how easy it is to change it.

- 그 시험의 풀어쓰기 — **코드는 뻔해야 한다: 누군가 변경을 해야 할 때, 바꿔야 할 코드를 쉽게
  찾고 오류를 들이지 않으면서 그 변경을 빠르게 할 수 있어야 한다. 건강한 코드베이스는 우리
  생산성을 극대화해 사용자를 위한 기능을 더 빠르고 더 싸게 만들 수 있게 한다** (1장 §"Final
  Thoughts", p.43).[^fowler2018]
- 그리고 유지 절차 — **코드를 건강하게 유지하려면 프로그래밍 팀과 그 이상 사이에 무엇이
  끼어 있는지 주의를 기울인 다음, 리팩터링해서 그 이상에 더 가까이 가라** (1장 §"Final
  Thoughts", p.43).[^fowler2018]
- 이 시험이 [ETC — 바꾸기 쉬운 것이 좋은 설계](../concepts/etc-easier-to-change.md)와 사실상 같은 잣대다.
  세 소스가 각각 단일 최종 잣대를 세웠고, 이 책의 것과 실용주의 쪽의 ETC는 **같은 것을
  가리키고** 복잡성 쪽은 다른 축을 잰다 — 대비는 그 페이지에 있다.

## 이어지는 페이지

- [리팩터링](refactoring.md) — 이 리듬이 실현하는 활동의 정의
- [자기 테스트 코드](self-testing-code.md) — 매 걸음의 구두점을 찍는 것
- [언제 리팩터링하는가](when-to-refactor.md) — 이 리듬을 언제 시작하는가
- [코드의 나쁜 냄새](../concepts/code-smells.md) — 예제 코드가 앓던 것들의 이름
- [ETC — 바꾸기 쉬운 것이 좋은 설계](../concepts/etc-easier-to-change.md) — 맺음의 시험과 같은 잣대
- [헤드라이트를 앞지르지 마라](../concepts/dont-outrun-your-headlights.md) — 작은 걸음 규칙의 다른 소스
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 1장 "Refactoring: A First Example"(pp.1–44). 쪽은 인쇄판 쪽
    번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의 표준
    규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. **이 장의 코드는
    옮기지 않았다** — 44쪽에 걸친 한 예제의 연속 개정판이라 어느 판을 떼어 놔도 복사해 쓸
    것이 아니고(펜스의 정의), 이 페이지가 다루는 것은 그 코드가 아니라 판과 판 사이의
    걸음이다. 예제의 도판(Figure)과 상태 요약 코드 목록도 같은 이유로 산문으로만 서술했다.

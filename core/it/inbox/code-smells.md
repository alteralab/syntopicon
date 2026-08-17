---
type: concept
title: 코드의 나쁜 냄새
description: 리팩터링할 때를 정밀한 계측이 아니라 후각으로 판정하자는 제안과 그 어휘 스물넷 — 이름·중복·긴 함수·긴 매개변수 목록·전역 데이터·가변 데이터·발산하는 변경·산탄총 수술·기능 편애·데이터 뭉치·기본형 집착·반복되는 switch·반복문·게으른 요소·추측성 일반화·임시 필드·메시지 체인·중개자·내부자 거래·거대한 클래스·인터페이스가 다른 대안 클래스·데이터 클래스·상속 포기·주석, 각 냄새가 지목하는 리팩터링을 카탈로그 항목과 잇는 처방 대응표(그리고 어느 냄새도 부르지 않는 열일곱 항목), 그리고 저자 자신이 초판에서 철회하거나 약화시킨 판정들
generated: { by: "claude-opus-5", at: "2026-08-17T12:00:00Z" }
status: draft
contradicts: [why-write-comments]
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
  - { id: ousterhout2021, resource: /it/sources/ousterhout2021.md }
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 코드의 나쁜 냄새

- [왜 냄새인가 — 계측을 포기한 자리](#왜-냄새인가--계측을-포기한-자리)
- [이름과 중복](#이름과-중복)
- [크기 — 긴 함수와 긴 매개변수 목록](#크기--긴-함수와-긴-매개변수-목록)
- [데이터의 접근 범위 — 전역 데이터와 가변 데이터](#데이터의-접근-범위--전역-데이터와-가변-데이터)
- [변경의 모양 — 발산하는 변경과 산탄총 수술](#변경의-모양--발산하는-변경과-산탄총-수술)
- [자리가 틀린 것 — 기능 편애·데이터 뭉치·기본형 집착](#자리가-틀린-것--기능-편애데이터-뭉치기본형-집착)
- [조건과 반복 — 반복되는 switch와 반복문](#조건과-반복--반복되는-switch와-반복문)
- [없어도 되는 것 — 게으른 요소·추측성 일반화·임시 필드](#없어도-되는-것--게으른-요소추측성-일반화임시-필드)
- [연결이 지나친 것 — 메시지 체인·중개자·내부자 거래](#연결이-지나친-것--메시지-체인중개자내부자-거래)
- [클래스의 모양 — 거대한 클래스·대안 클래스·데이터 클래스·상속 포기](#클래스의-모양--거대한-클래스대안-클래스데이터-클래스상속-포기)
- [주석 — 탈취제로 쓰이는 냄새](#주석--탈취제로-쓰이는-냄새)
- [냄새에서 카탈로그로 — 처방 대응표](#냄새에서-카탈로그로--처방-대응표)
- [설계 잣대를 세운 소스와 갈리는 자리](#설계-잣대를-세운-소스와-갈리는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **리팩터링(refactoring)할 때가 됐다는 것을 코드의 어떤 모양으로 알아채는가.**

용어는 원어를 유지한다 — 나쁜 냄새(bad smell)와 개별 냄새 이름은 이 책이 만들어 통용되게
한 고유명이고, 리팩터링 카탈로그의 항목명과 짝을 이뤄 색인 키 노릇을 한다.

## 왜 냄새인가 — 계측을 포기한 자리

- 이 장은 Kent Beck과 공저다. 머리 경구는 Beck의 할머니 말이다 (3장,
  p.71):[^fowler2018]

> If it stinks, change it.

- 문제 규정 — **어떻게 하는지 안다고 해서 언제 하는지 아는 것은 아니다. 언제 리팩터링을
  시작할지 — 그리고 언제 멈출지 — 를 결정하는 것은 리팩터링의 기계적 절차를 다루는 법을
  아는 것만큼이나 중요하다** (3장, p.71).[^fowler2018]
- **정밀한 기준을 주지 않겠다고 명시한다** — **우리가 주려 하지 않을 것 하나는 리팩터링이
  언제 밀렸는지에 대한 정확한 기준이다. 우리 경험으로 어떤 계측 집합도 정보에 밝은 인간의
  직관에 필적하지 않는다. 우리가 할 일은 리팩터링으로 풀 수 있는 문제가 있다는 징후를 주는
  것이다. 인스턴스 변수가 몇 개면 너무 많은지, 메서드의 줄 수가 얼마면 너무 많은지에 대한
  당신 자신의 감각을 길러야 할 것이다** (3장, p.71).[^fowler2018]
  - 이 대목이 [소프트웨어 복잡성의 정의와 증상](software-complexity-defined.md)의 조작적
    정의와 대비된다. 그쪽은 복잡성을 **작업 난이도**로 정의해 계측 가능한 형태에 다가가고,
    이쪽은 계측을 **인간 직관에 못 미친다**며 명시적으로 포기한다. 대신 이쪽이 내놓는 것은
    정의가 아니라 **이름 붙은 패턴 스물넷**이다.
- 쓰는 법 — **당신이 무엇을 냄새 맡고 있는지 식별해 보고, 우리가 제안하는 리팩터링으로 가서
  그것이 도움이 되는지 보라. 정확히 그 냄새를 못 찾을 수도 있지만, 바라건대 그것이 당신을
  옳은 방향으로 가리켜 줄 것이다** (3장, pp.71–72).[^fowler2018]

## 이름과 중복

- **Mysterious Name** — **명료한 코드의 가장 중요한 부분 중 하나가 좋은 이름이다** (3장
  §"Mysterious Name", p.72).[^fowler2018] 그래서 **아마 우리가 가장 흔히 하는 리팩터링이
  이름 바꾸기다** (3장 §"Mysterious Name", p.72).[^fowler2018]
  - **이름이 안 떠오르는 것 자체가 진단이다** — **이름 바꾸기는 그저 이름을 바꾸는 연습이
    아니다. 무언가에 좋은 이름이 떠오르지 않을 때, 그것은 흔히 더 깊은 설계 병증의
    신호다. 까다로운 이름을 두고 고민하다가 우리는 코드의 유의미한 단순화에 이른 적이 여러
    번 있다** (3장 §"Mysterious Name", p.72).[^fowler2018] 같은 판정이
    [이름 짓기](naming-things.md)에 두 소스로 이미 있다.
  - 저자가 인용하는 관용구 하나 — **이름 짓기는 프로그래밍에서 어려운 두 가지 중 하나다**
    (3장 §"Mysterious Name", p.72).[^fowler2018]
- **Duplicated Code** — 이 책이 중복에 대한 근거로 드는 것은 원칙이 아니라 **읽기 비용**이다
  — **한 곳 이상에서 같은 코드 구조를 보면, 그것들을 통합할 방법을 찾을 때 프로그램이 더
  나아지리라고 확신해도 된다. 중복은 이 사본들을 읽을 때마다 차이가 있는지 주의 깊게 읽어야
  한다는 뜻이다. 중복된 코드를 바꿔야 하면 각 중복을 찾아내 잡아야 한다** (3장 §"Duplicated
  Code", p.72).[^fowler2018]
  - 처방이 중복의 **모양**에 따라 갈린다 (3장 §"Duplicated Code", p.72):[^fowler2018]
    - **같은 클래스의 두 메서드에 같은 표현식** → *Extract Function*으로 뽑아 양쪽에서 부른다.
    - **비슷하지만 완전히 같지는 않은 코드** → *Slide Statements*로 비슷한 항목들을 모아
      놓아 뽑아내기 쉽게 만든다.
    - **공통 기반 클래스의 서브클래스들에 있는 중복 조각** → *Pull Up Method*.
  - 2장은 같은 것을 설계 개선의 핵심으로 다시 든다 — **중복을 없앰으로써 나는 코드가 모든
    것을 단 한 번만 말하도록 보장하는데, 그것이 좋은 설계의 본질이다** (2장 §"Refactoring
    Improves the Design of Software", p.47).[^fowler2018] 전문과 다른 소스의 판정은
    [DRY 원칙](dry-principle.md)에 있다.

## 크기 — 긴 함수와 긴 매개변수 목록

- **Long Function** — 경험적 주장이 먼저 온다 (3장 §"Long Function",
  p.73):[^fowler2018]

> In our experience, the programs that live best and longest are those with short
> functions.

  - 비용 구조가 바뀌었다는 관찰이 붙는다 — **옛 언어들은 서브루틴 호출에 부담이 있어 사람들이
    작은 함수를 쓰지 못하게 막았다. 현대 언어들은 프로세스 내 호출에 대해 그 부담을 거의
    없앴다. 코드를 읽는 사람에게는 여전히 부담이 있는데, 함수가 무엇을 하는지 보려면 맥락을
    전환해야 하기 때문이다** (3장 §"Long Function", p.73).[^fowler2018]
  - **그 남은 부담을 이름이 갚는다** — **작은 함수를 이해하기 쉽게 만드는 진짜 열쇠는 좋은
    이름이다. 함수에 좋은 이름이 있으면 대개 그 본문을 볼 필요가 없다** (3장 §"Long
    Function", p.73).[^fowler2018] 이 한 문장이 아래
    [설계 잣대를 세운 소스와 갈리는 자리](#설계-잣대를-세운-소스와-갈리는-자리)의 쟁점이다.
  - **주석을 함수로 바꾸라는 발견법**이 이 절의 조작적 처방이다 — **우리가 따르는 발견법은,
    무언가에 주석을 달고 싶은 필요를 느낄 때마다 대신 함수를 쓴다는 것이다. 그런 함수는 주석을
    달고 싶었던 코드를 담되 그것이 동작하는 방식이 아니라 그 코드의 *의도*를 따라 이름
    지어진다. 우리는 여러 줄에 대해서도, 심지어 코드 한 줄에 대해서도 이렇게 한다. 메서드
    호출이 대체하는 코드보다 길어지더라도 그렇게 한다 — 메서드 이름이 코드의 목적을 설명하기만
    한다면** (3장 §"Long Function", p.73).[^fowler2018]
  - **그리고 기준이 길이가 아님을 명시한다** — **여기서 핵심은 함수 길이가 아니라 메서드가
    *무엇*을 하는가와 *어떻게* 하는가 사이의 의미적 거리다** (3장 §"Long Function",
    p.73).[^fowler2018]
  - 뽑아낼 덩어리를 찾는 신호 셋 (3장 §"Long Function", pp.73–74):[^fowler2018]
    **주석**(의미적 거리를 알려 준다), **조건문**(*Decompose Conditional*), **반복문**(반복문과
    그 안의 코드를 통째로 메서드로. 이름을 붙이기 어려우면 두 가지를 하고 있다는 뜻이라
    *Split Loop*).
- **Long Parameter List** — 역사적 배경부터 적는다 — **초창기에 우리는 함수가 필요로 하는
  모든 것을 매개변수로 넘기라고 배웠다. 대안이 전역 데이터였고 전역 데이터는 빠르게 악해지기
  때문에 이해할 만한 일이었다. 그러나 긴 매개변수 목록은 그 자체로 흔히 혼란스럽다** (3장
  §"Long Parameter List", p.74).[^fowler2018]
  - 처방 넷 — 다른 매개변수로부터 얻을 수 있으면 *Replace Parameter with Query*, 자료 구조에서
    값을 여럿 꺼내 넘기는 대신 *Preserve Whole Object*, 늘 함께 다니면 *Introduce Parameter
    Object*, 분기용 플래그면 *Remove Flag Argument* (3장 §"Long Parameter List",
    p.74).[^fowler2018]
  - 클래스가 매개변수 줄이기의 수단으로 등장한다 — **클래스는 매개변수 목록 크기를 줄이는
    훌륭한 방법이다. 여러 함수가 여러 매개변수 값을 공유할 때 특히 유용하다** →
    *Combine Functions into Class*. 그리고 함수형 프로그래밍의 표현으로는 **부분 적용된 함수
    집합을 만드는 것**이다 (3장 §"Long Parameter List", p.74).[^fowler2018]

## 데이터의 접근 범위 — 전역 데이터와 가변 데이터

- **Global Data** — 진단이 **범인 추적 불가능성**이다 — **전역 데이터의 문제는 그것이
  코드베이스 어디에서나 수정될 수 있고, 어느 코드가 그것을 건드렸는지 발견할 기제가 없다는
  것이다. 몇 번이고 이것은 원격 작용(spooky action from a distance)의 한 형태에서 번식하는
  버그로 이어지고, 잘못된 프로그램 조각이 어디 있는지 알아내기가 매우 어렵다** (3장 §"Global
  Data", p.74).[^fowler2018]
  - **범위가 전역 변수만이 아니다** — **전역 데이터의 가장 뻔한 형태는 전역 변수지만, 우리는
    클래스 변수와 싱글턴에서도 이 문제를 본다** (3장 §"Global Data", p.74).[^fowler2018]
  - 처방은 캡슐화가 먼저다 — ***Encapsulate Variable*이 우리의 핵심 방어인데, 프로그램의
    어느 부분에 의해서든 오염될 수 있는 데이터를 마주쳤을 때 언제나 우리의 첫 수다. 적어도
    함수로 감싸 두면 그것이 어디서 수정되는지 보기 시작할 수 있고 접근을 통제하기 시작할 수
    있다. 그런 다음 그 모듈의 코드만 볼 수 있는 클래스나 모듈 안으로 옮겨 범위를 가능한 한
    좁히는 것이 좋다** (3장 §"Global Data", p.75).[^fowler2018]
  - **용량의 문제라는 규정** — **전역 데이터는 파라켈수스의 격언을 보여 준다: 독과 무해한 것의
    차이는 용량이다. 소량의 전역 데이터로는 넘어갈 수 있지만, 많아질수록 다루기가 지수적으로
    어려워진다** (3장 §"Global Data", p.75).[^fowler2018]
  - 같은 처방이 [결합 끊기](decoupling.md)에 전역 상태를 API로 감싸라는 형태로 이미 있다.
- **Mutable Data** — 진단 — **데이터의 변경은 흔히 예상치 못한 결과와 까다로운 버그로
  이어질 수 있다. 여기서 어떤 데이터를 갱신하면서, 소프트웨어의 다른 부분이 다른 것을
  기대하고 있어 이제 실패한다는 것을 깨닫지 못한다 — 드문 조건에서만 일어나면 특히 발견하기
  어려운 실패다** (3장 §"Mutable Data", p.75).[^fowler2018]
  - 함수형 프로그래밍이 이 문제의 극단적 해법으로 소개된다 — **이런 이유로 소프트웨어 개발의
    한 학파 전체 — 함수형 프로그래밍 — 가 데이터는 결코 변해서는 안 되고 자료 구조를 갱신하는
    것은 언제나 변경이 반영된 그 구조의 새 사본을 반환해야 하며 옛 데이터는 손대지 않은 채로
    남겨야 한다는 관념 위에 서 있다** (3장 §"Mutable Data", p.75).[^fowler2018]
  - **그러나 이 책의 처방은 언어 전환이 아니다** — **그렇다고 불변성의 이점을 무시해야 한다는
    뜻은 아니다 — 제약 없는 데이터 갱신의 위험을 제한하기 위해 우리가 할 수 있는 일이 여전히
    많다** (3장 §"Mutable Data", p.75).[^fowler2018] 처방 목록이 그 "많은 일"이다 —
    *Encapsulate Variable*(갱신을 좁은 함수로), *Split Variable*(한 변수가 다른 것들을 담을
    때), *Slide Statements*·*Extract Function*(부작용 없는 코드를 갱신하는 코드에서 분리),
    *Separate Query from Modifier*, *Remove Setting Method* (3장 §"Mutable Data",
    p.75).[^fowler2018]
  - **가장 고약한 종류가 지목된다** — **다른 곳에서 계산될 수 있는 가변 데이터가 특히
    악취가 난다. 그것은 혼란·버그·집에서 놓친 저녁의 풍부한 원천일 뿐 아니라 — 불필요하기까지
    하다** → *Replace Derived Variable with Query* (3장 §"Mutable Data",
    p.75).[^fowler2018]
  - **범위가 위험을 정한다** — **가변 데이터는 그 범위가 몇 줄뿐인 변수일 때는 큰 문제가
    아니다 — 그러나 범위가 커질수록 위험이 커진다** (3장 §"Mutable Data",
    p.76).[^fowler2018]

## 변경의 모양 — 발산하는 변경과 산탄총 수술

이 둘은 짝이다 — **한 번의 변경을 하려 할 때 시스템의 명확한 한 지점으로 가서 그 변경을
할 수 있기를 원한다. 그럴 수 없을 때 당신은 밀접히 관련된 두 악취 중 하나를 맡고 있는
것이다** (3장 §"Divergent Change", p.76).[^fowler2018]

- **Divergent Change** — **한 모듈이 서로 다른 이유로 서로 다른 방식으로 자주 바뀔 때
  일어난다. 모듈을 보고 "새 데이터베이스가 생길 때마다 이 세 함수를 바꿔야 하고, 새 금융
  상품이 생길 때마다 이 네 함수를 바꿔야 한다"고 말한다면 그것이 발산하는 변경의 징후다**
  (3장 §"Divergent Change", p.76).[^fowler2018]
  - 처방의 근거 — **데이터베이스 상호작용과 금융 처리 문제는 별개의 맥락이고, 그런 맥락들을
    별개 모듈로 옮김으로써 우리는 프로그래밍 삶을 더 낫게 만들 수 있다. 그러면 한 맥락에
    변경이 생겼을 때 그 맥락 하나만 이해하고 다른 것은 무시하면 된다** (3장 §"Divergent
    Change", p.76).[^fowler2018]
  - **경계가 늦게 보인다는 단서가 붙는다** — **물론 데이터베이스나 금융 상품을 몇 개 더한
    뒤에야 이것을 발견하는 일이 흔하다; 맥락 경계는 프로그램 초기에는 보통 불분명하고
    소프트웨어 시스템의 능력이 바뀌면서 계속 이동한다** (3장 §"Divergent Change",
    p.76).[^fowler2018]
  - 처방은 두 관심사의 관계에 따라 갈린다 — 순서를 이루면 *Split Phase*로 그 사이에 명확한
    자료 구조를 두고, 호출이 오가면 모듈을 만들어 *Move Function*, 한 함수 안에 섞여 있으면
    옮기기 전에 *Extract Function*, 모듈이 클래스면 *Extract Class* (3장 §"Divergent
    Change", p.76).[^fowler2018]
- **Shotgun Surgery** — **발산하는 변경과 비슷하되 반대다. 변경할 때마다 여러 다른 클래스에
  작은 편집을 많이 해야 할 때 이 냄새를 맡는다. 변경이 사방에 흩어져 있으면 찾기 어렵고,
  중요한 변경 하나를 놓치기 쉽다** (3장 §"Shotgun Surgery", pp.76–77).[^fowler2018]
  - 처방은 모으기다 — *Move Function*·*Move Field*로 한 모듈에, 비슷한 데이터를 다루는 함수
    묶음이면 *Combine Functions into Class*, 자료 구조를 변환·보강하면 *Combine Functions
    into Transform* (3장 §"Shotgun Surgery", p.77).[^fowler2018]
  - **중간 단계로 일부러 크게 만드는 전술**이 여기 나온다 — **산탄총 수술에 유용한 전술은
    *Inline Function*이나 *Inline Class* 같은 인라인 리팩터링을 써서 잘못 분리된 로직을
    한데 끌어모으는 것이다. 긴 메서드나 거대한 클래스로 끝나겠지만, 그런 다음 추출로 더 말이
    되는 조각들로 쪼갤 수 있다. 우리가 작은 함수와 클래스를 지나칠 만큼 좋아하기는 하지만,
    재조직의 중간 단계로 큰 것을 만드는 데 겁내지 않는다** (3장 §"Shotgun Surgery",
    p.77).[^fowler2018]
  - 이 두 냄새가 [직교성](orthogonality.md)의 시험("요구사항 하나가 바뀌면 몇 개의 모듈이
    영향받는가")과 같은 대상을 재는 두 방향이다. 발산하는 변경은 **한 모듈이 여러 이유로**,
    산탄총 수술은 **한 이유가 여러 모듈로** 간다.

## 자리가 틀린 것 — 기능 편애·데이터 뭉치·기본형 집착

- **Feature Envy** — 모듈화의 목적부터 규정한다 — **프로그램을 모듈화할 때 우리는 코드를
  구역으로 나누어 구역 안의 상호작용을 최대화하고 구역 사이의 상호작용을 최소화하려 한다.
  기능 편애의 전형적 사례는 한 모듈의 함수가 자기 모듈 안에서보다 다른 모듈 안의 함수나
  데이터와 소통하는 데 더 많은 시간을 쓸 때 일어난다** (3장 §"Feature Envy",
  p.77).[^fowler2018]
  - 처방 — **함수는 분명히 데이터와 함께 있고 싶어 한다. 그러니 *Move Function*으로 거기
    보내라.** 함수의 일부만 편애하면 그 부분을 *Extract Function*한 뒤 옮긴다 (3장 §"Feature
    Envy", p.77).[^fowler2018]
  - **여러 모듈을 쓰는 함수의 판정 기준** — **우리가 쓰는 발견법은 어느 모듈이 데이터의
    대부분을 갖는지 판정해 그 데이터와 함께 함수를 두는 것이다** (3장 §"Feature Envy",
    p.77).[^fowler2018]
  - **규칙을 깨는 패턴들이 명시된다** — 4인방의 Strategy와 Visitor, Beck의 Self Delegation이
    그것이고, **이것들은 발산하는 변경 냄새에 맞서는 데 쓴다** (3장 §"Feature Envy",
    p.77).[^fowler2018] 근본 규칙은 한 줄이다 — **함께 바뀌는 것을 함께 두라. 데이터와 그
    데이터를 참조하는 행동은 보통 함께 바뀐다 — 그러나 예외가 있다. 예외가 생기면 우리는
    변경을 한자리에 유지하려고 행동을 옮긴다** (3장 §"Feature Envy", p.77).[^fowler2018]
- **Data Clumps** — 관찰 — **데이터 항목은 아이들 같은 경향이 있다: 함께 어울려 다니기를
  즐긴다. 흔히 같은 서너 개의 데이터 항목이 여러 자리에 함께 나타난다: 두어 클래스의 필드로,
  많은 메서드 시그니처의 매개변수로** (3장 §"Data Clumps", p.78).[^fowler2018]
  - 순서가 정해져 있다 — 먼저 필드로 나타나는 자리에 *Extract Class*, 그다음 메서드
    시그니처에 *Introduce Parameter Object*나 *Preserve Whole Object* (3장 §"Data Clumps",
    p.78).[^fowler2018]
  - **판정 시험이 하나 있다** — **좋은 시험은 데이터 값 하나를 지운다고 생각해 보는 것이다.
    그렇게 하면 나머지가 말이 되는가? 말이 안 된다면 그것은 태어나고 싶어 하는 객체가 있다는
    확실한 신호다** (3장 §"Data Clumps", p.78).[^fowler2018]
  - **레코드가 아니라 클래스를 만들라는 이유** — **여기서 우리가 단순한 레코드 구조가 아니라
    클래스를 만들라고 주장하는 것을 눈치챘을 것이다. 클래스를 쓰면 좋은 향수를 만들 기회가
    생기기 때문이다. 이제 기능 편애 사례를 찾아 새 클래스로 옮길 수 있는 행동을 제안받을 수
    있다** (3장 §"Data Clumps", p.78).[^fowler2018]
- **Primitive Obsession** — 진단 — **많은 프로그래머가 자기 도메인에 유용한 자기만의 기본
  타입 — 돈·좌표·범위 같은 것 — 을 만들기를 이상하리만치 꺼린다는 것을 우리는 안다. 그래서
  화폐 금액을 그냥 숫자로 다루는 계산, 단위를 무시하는 물리량 계산(인치에 밀리미터를 더한다),
  `if (a < upper && a > lower)`를 하는 코드를 많이 본다** (3장 §"Primitive Obsession",
  p.78).[^fowler2018]
  - **문자열이 특히 지목된다** — **문자열은 이런 종류의 악취에 특히 흔한 배양 접시다:
    전화번호는 그저 문자의 모음 이상이다. 다른 것이 없더라도 적절한 타입은 사용자 인터페이스에
    표시해야 할 때를 위한 일관된 표시 로직을 흔히 담을 수 있다** (3장 §"Primitive Obsession",
    p.78).[^fowler2018] 그래서 붙은 이름이 있다 — **그런 타입을 문자열로 표현하는 것은 아주
    흔한 악취라서 사람들은 그것을 "stringly typed" 변수라고 부른다** (3장 §"Primitive
    Obsession", p.78).[^fowler2018]
  - 처방 — *Replace Primitive with Object*, 조건 분기를 통제하는 타입 코드면
    *Replace Type Code with Subclasses* 뒤에 *Replace Conditional with Polymorphism*,
    함께 나타나는 기본형 무리면 데이터 뭉치로 취급해 *Extract Class*·*Introduce Parameter
    Object* (3장 §"Primitive Obsession", p.79).[^fowler2018]

## 조건과 반복 — 반복되는 switch와 반복문

- **Repeated Switches** — **저자들이 초판의 판정을 명시적으로 개정한 자리다.** 초판에는
  "switch statements"라는 냄새가 있었다 — **그 냄새가 있었던 것은 90년대 말에 우리가
  다형성이 안타깝게 저평가돼 있다고 보았고 사람들을 그쪽으로 옮기게 하는 데 이득을 보았기
  때문이다. 요즘은 다형성이 더 많이 쓰이고, 그것은 15년 전에 그랬던 것 같은 단순한 붉은
  깃발이 아니다** (3장 §"Repeated Switches", p.79).[^fowler2018]
  - 그래서 표적이 좁혀졌다 — **그래서 우리는 이제 *반복되는* switch, 즉 같은 조건 분기 로직이
    (switch/case 문으로든 if/else의 연쇄로든) 서로 다른 자리에 나타나는 경우에 초점을
    맞춘다. 그런 중복된 switch의 문제는 절을 하나 추가할 때마다 모든 switch를 찾아 갱신해야
    한다는 것이다** (3장 §"Repeated Switches", p.79).[^fowler2018]
  - **저자들이 반대편 극단과도 거리를 둔다** — **모든 조건 로직이 다형성으로 대체돼야 한다고
    주장하는 사람들도 있다고 우리는 들었다. (…) 우리는 아무리 혈기왕성했던 젊은 시절에도
    조건문에 무조건 반대한 적이 없다** (3장 §"Repeated Switches", p.79).[^fowler2018]
- **Loops** — **가장 강한 취향 표명이자 시대 조건이 붙은 판정이다** — **반복문은 가장 초기
  언어 이래로 프로그래밍의 핵심 부분이었다. 그러나 우리는 그것이 오늘날 나팔바지나 벽지
  무늬보다 더 적절할 것이 없다고 느낀다. 초판을 쓸 때 우리는 그것을 못마땅해했지만 — 자바를
  비롯한 당시 대부분의 언어가 더 나은 대안을 제공하지 않았다. 그러나 요즘은 일급 함수가
  널리 지원되므로 *Replace Loop with Pipeline*으로 그 시대착오를 은퇴시킬 수 있다** (3장
  §"Loops", p.79).[^fowler2018]
  - 이득의 근거 — **filter와 map 같은 파이프라인 연산은 처리에 포함되는 요소가 무엇이고
    그것으로 무엇을 하는지 빠르게 보는 데 도움을 준다** (3장 §"Loops", p.79).[^fowler2018]
  - 버전 조건: 일급 함수를 지원하는 언어에 한정된다. 저자들 자신이 초판 시점(자바 8 이전)에는
    이 처방이 불가능했다고 적는다.

## 없어도 되는 것 — 게으른 요소·추측성 일반화·임시 필드

- **Lazy Element** — **우리는 구조를 더하려고 프로그램 요소를 쓰기를 좋아한다 — 변형·재사용의
  기회를 주거나 그저 더 쓸모 있는 이름을 갖기 위해. 그러나 때로는 그 구조가 필요하지 않다.
  본문 코드가 읽히는 그대로 이름 지어진 함수일 수도 있고, 본질적으로 단순한 함수 하나인
  클래스일 수도 있다** (3장 §"Lazy Element", p.80).[^fowler2018] 처방은 *Inline Function*·
  *Inline Class*, 상속이면 *Collapse Hierarchy*다.
- **Speculative Generality** — Brian Foote가 이름 붙인 냄새다 — **사람들이 "아, 언젠가 이런
  것을 할 능력이 필요할 거야"라고 말하면서 요구되지 않은 것들을 다루려고 온갖 훅과 특수
  사례를 더할 때 생긴다. 결과는 흔히 이해하고 유지보수하기 더 어렵다. 이 모든 기계 장치가
  쓰이고 있다면 그럴 가치가 있다. 그러나 쓰이지 않는다면 없다** (3장 §"Speculative
  Generality", p.80).[^fowler2018]
  - **탐지 신호 하나가 명시된다** — **추측성 일반화는 함수나 클래스의 유일한 사용자가 테스트
    케이스일 때 발견할 수 있다. 그런 동물을 발견하면 테스트 케이스를 지우고 *Remove Dead
    Code*를 적용하라** (3장 §"Speculative Generality", p.80).[^fowler2018]
  - 2장의 yagni 논증이 같은 판정을 설계 층에서 편다 — 전문은
    [yagni와 진화적 아키텍처](yagni-and-evolutionary-architecture.md)에 있다. 반대 방향의
    처방은 [범용 모듈이 더 깊다](general-purpose-modules.md)에 있는데, 그쪽이 요구하는
    "다소 범용"은 **오늘 필요한 기능에 더 넓은 인터페이스**이지 오늘 쓰이지 않는 기계
    장치가 아니라서 이 냄새와 충돌하지 않는다.
- **Temporary Field** — **어떤 필드가 특정 상황에서만 설정되는 클래스를 볼 때가 있다. 그런
  코드는 이해하기 어려운데, 객체가 자기 필드 전부를 필요로 하리라 기대하기 때문이다** (3장
  §"Temporary Field", p.80).[^fowler2018] 처방은 *Extract Class*로 그 고아 변수들에 집을
  만들고 *Move Function*으로 관련 코드를 옮기는 것, 그리고 *Introduce Special Case*로 조건
  코드를 없애는 것이다.

## 연결이 지나친 것 — 메시지 체인·중개자·내부자 거래

- **Message Chains** — **클라이언트가 한 객체에게 다른 객체를 묻고, 그 객체에게 또 다른
  객체를 묻고, 그 객체에게 또 다른 객체를 묻는 식일 때 메시지 체인을 본다** (3장 §"Message
  Chains", p.81).[^fowler2018]
  - 비용 — **이렇게 항해하는 것은 클라이언트가 항해 구조에 결합돼 있다는 뜻이다. 중간
    관계에 어떤 변경이 생기든 클라이언트가 바뀌어야 한다** (3장 §"Message Chains",
    p.81).[^fowler2018]
  - **처방에 곧바로 반작용 경고가 붙는다** — ***Hide Delegate*를 쓴다. (…) 원칙적으로 체인의
    모든 객체에 이렇게 할 수 있지만, 그렇게 하면 흔히 모든 중간 객체가 중개자가 된다. 흔히
    더 나은 대안은 결과 객체가 무엇에 쓰이는지 보는 것이다** (3장 §"Message Chains",
    p.81).[^fowler2018]
  - **그리고 절제의 선언** — **어떤 사람들은 메서드 체인이라면 무엇이든 끔찍한 것으로
    여긴다. 우리는 차분하고 이성적인 절제로 알려져 있다. 뭐, 적어도 이 경우에는 그렇다**
    (3장 §"Message Chains", p.81).[^fowler2018]
- **Middle Man** — 위 처방의 반대편이다 — **객체의 주된 특징 중 하나가 캡슐화다 — 내부
  세부를 나머지 세계로부터 감추는 것. 캡슐화에는 흔히 위임이 따라온다. (…) 그러나 이것은
  지나칠 수 있다. 클래스의 인터페이스를 보니 메서드의 절반이 다른 클래스에 위임하고 있다.
  얼마 뒤에는 *Remove Middle Man*을 써서 실제로 무슨 일이 일어나는지 아는 객체와 이야기할
  때다** (3장 §"Middle Man", p.81).[^fowler2018]
  - 같은 대상을 [계층이 다르면 추상도 달라야 한다](different-layer-different-abstraction.md)가
    **통과 메서드**라는 이름으로 다룬다. 두 소스가 같은 것을 서로 다른 이름으로 붉은 깃발에
    올린다.
- **Insider Trading** — **소프트웨어 하는 사람들은 모듈 사이의 튼튼한 벽을 좋아하고 데이터를
  너무 많이 주고받는 것이 결합을 늘린다고 쓰라리게 불평한다. 일이 돌아가게 하려면 어느 정도
  거래는 일어나야 하지만, 우리는 그것을 최소로 줄이고 전부 공개적으로 유지할 필요가 있다**
  (3장 §"Insider Trading", p.82).[^fowler2018]
  - **상속이 이 냄새의 구조적 원천으로 지목된다** — **상속은 흔히 담합으로 이어질 수 있다.
    서브클래스는 부모가 알기를 바라는 것보다 언제나 더 많이 부모에 대해 알게 된다** (3장
    §"Insider Trading", p.82).[^fowler2018] 같은 판정이 [상속세](inheritance-tax.md)에 있다.

## 클래스의 모양 — 거대한 클래스·대안 클래스·데이터 클래스·상속 포기

- **Large Class** — **클래스가 너무 많은 것을 하려 할 때 그것은 흔히 너무 많은 필드로
  나타난다. 클래스에 필드가 너무 많으면 중복 코드가 멀지 않다** (3장 §"Large Class",
  p.82).[^fowler2018]
  - 쪼갤 축을 찾는 두 신호 — **변수 일부에 공통 접두나 접미가 있으면 컴포넌트의 기회를
    시사한다**, 그리고 **그런 클래스의 클라이언트가 흔히 클래스를 쪼갤 최선의 단서다.
    클라이언트가 클래스 기능의 부분집합을 쓰는지 보라. 각 부분집합이 가능한 별도 클래스다**
    (3장 §"Large Class", p.82).[^fowler2018]
- **Alternative Classes with Different Interfaces** — **클래스를 쓰는 큰 이득 중 하나가
  치환 지원, 즉 필요할 때 한 클래스가 다른 클래스 자리에 들어가게 하는 것이다. 그러나 이것은
  그 인터페이스가 같을 때만 동작한다** (3장 §"Alternative Classes with Different
  Interfaces", p.83).[^fowler2018] 처방은 *Change Function Declaration*으로 함수를 맞추고,
  모자라면 프로토콜이 맞을 때까지 *Move Function*, 그 결과 중복이 생기면 *Extract
  Superclass*다.
- **Data Class** — **필드와 그 필드의 게터·세터만 있고 그 밖에는 아무것도 없는 클래스들이다.
  그런 클래스는 멍청한 데이터 보유자이고 흔히 다른 클래스에 의해 지나치게 상세히 조작된다**
  (3장 §"Data Class", p.83).[^fowler2018]
  - 진단 — **데이터 클래스는 흔히 행동이 잘못된 자리에 있다는 신호이며, 그것을 클라이언트에서
    데이터 클래스 자체로 옮김으로써 큰 진전을 낼 수 있다** (3장 §"Data Class",
    p.83).[^fowler2018]
  - **예외가 명시된다** — **그러나 예외가 있고, 최선의 예외 중 하나가 별개의 함수 호출에서
    나온 결과 레코드로 쓰이는 레코드다. 좋은 예가 *Split Phase*를 적용한 뒤의 중간 자료
    구조다. 그런 결과 레코드의 핵심 특성은 그것이 (적어도 실제로는) 불변이라는 것이다. 불변
    필드는 캡슐화될 필요가 없고, 불변 데이터에서 파생된 정보는 게터 메서드가 아니라 필드로
    표현될 수 있다** (3장 §"Data Class", p.83).[^fowler2018]
  - **이 항목만 파이썬 쪽 소스가 통째로 되받는다.** *Fluent Python* 5장이 데이터 클래스
    빌더 셋을 소개한 뒤 마지막 절을 이 냄새에 쓰고, 그 안에서 **파울러의 글 "Code Smell"을
    허락받아 전문 재수록한다** (5장 §"Data class as a code smell").[^ramalho2022]
    전문은 [코드 냄새로서의 데이터 클래스](data-class-as-code-smell.md)에 있고, 여기서는
    이 항목에 직접 걸리는 둘만 적는다.
    - **되받는 쪽이 이 항목의 근거를 다시 진술한다** — **객체 지향 프로그래밍의 주된 생각은
      행동과 데이터를 같은 코드 단위, 즉 클래스에 함께 놓는 것이다. 어떤 클래스가 널리
      쓰이는데 자기 자신의 유의미한 행동이 없다면, 그 인스턴스를 다루는 코드가 시스템 전체의
      메서드와 함수에 흩어져 있고 심지어 중복돼 있을 가능성이 있다 — 유지보수 두통의
      처방전이다. 그래서 파울러가 데이터 클래스를 다루는 리팩터링들이 책임을 그 안으로
      되가져오는 것이다** (5장 §"Data class as a code smell").[^ramalho2022]
    - **그리고 정당한 경우를 둘로 이름 붙인다** — **비계(scaffolding)**, 즉 새 모듈을
      띄우는 초기 구현이라 시간이 지나면 자기 메서드를 가져야 하는 경우와,
      **중간 표현(intermediate representation)**, 즉 JSON 같은 교환 형식으로 오가거나
      시스템 경계를 막 넘어온 데이터를 담는 경우다 (5장 §"Data class as scaffolding"·
      §"Data class as intermediate representation").[^ramalho2022] 뒤쪽에 붙는 단서가
      **이 항목의 예외와 같은 것**이다 — **이 시나리오에서 데이터 클래스 인스턴스는 불변
      객체로 다뤄져야 한다.** 이 항목이 "결과 레코드의 핵심 특성은 그것이 불변이라는
      것"이라 적은 자리와 겹친다.
    - 그래서 **모순으로 판정하지 않았다.** 근거와 대조는 아래 [설계 잣대를 세운 소스와
      갈리는 자리](#설계-잣대를-세운-소스와-갈리는-자리)에 있다.
- **Refused Bequest** — **서브클래스는 부모의 메서드와 데이터를 물려받는다. 그런데 그들이
  받은 것을 원하지도 필요로 하지도 않는다면?** (3장 §"Refused Bequest",
  p.83).[^fowler2018]
  - **전통적 조언을 저자들이 거부한다** — 전통적 처방은 형제 클래스를 만들어 *Push Down
    Method*·*Push Down Field*로 밀어내는 것이고 **모든 슈퍼클래스는 추상이어야 한다는 조언을
    흔히 듣게 된다**. 그러나 — **우리가 "전통적"이라는 말을 비꼬듯 쓴 데서 짐작하겠지만
    우리는 이것을 권하지 않을 참이다 — 적어도 언제나 그러지는 않는다. 우리는 늘 행동 조각을
    재사용하려고 서브클래싱을 하고, 그것이 일을 처리하는 완벽하게 좋은 방법이라고 본다.
    냄새가 나기는 한다 — 부정할 수 없다 — 그러나 보통 강한 냄새는 아니다. (…) 열에 아홉은
    이 냄새가 치울 가치가 없을 만큼 희미하다** (3장 §"Refused Bequest",
    pp.83–84).[^fowler2018]
  - **다만 강해지는 조건이 있다** — **서브클래스가 행동을 재사용하면서 슈퍼클래스의
    인터페이스는 지원하고 싶어 하지 않을 때 상속 포기의 냄새가 훨씬 강하다. 우리는 구현을
    거부하는 것은 개의치 않지만 — 인터페이스를 거부하는 것에는 목소리를 높인다** (3장
    §"Refused Bequest", p.84).[^fowler2018] 처방은 계층을 만지작거리는 대신
    *Replace Subclass with Delegate*·*Replace Superclass with Delegate*다.

## 주석 — 탈취제로 쓰이는 냄새

- **먼저 오해를 차단한다** — **걱정 마시라, 우리는 사람들이 주석을 쓰지 말아야 한다고 말하는
  것이 아니다. 우리의 후각 비유에서 주석은 나쁜 냄새가 아니다; 실제로 그것은 달콤한 냄새다**
  (3장 §"Comments", p.84).[^fowler2018]
- 그럼에도 이 장에 든 이유 — **주석이 흔히 탈취제로 쓰이기 때문이다. 두껍게 주석이 달린
  코드를 보다가 그 주석이 거기 있는 이유가 코드가 나쁘기 때문임을 알아차리는 일이 얼마나
  흔한지 놀랍다** (3장 §"Comments", p.84).[^fowler2018]
- 그래서 순서가 정해진다 — **주석은 우리를 이 장의 나머지에서 논한 온갖 썩은 냄새를 가진
  나쁜 코드로 이끈다. 우리의 첫 행동은 리팩터링으로 나쁜 냄새를 없애는 것이다. 끝내고 나면
  흔히 주석이 불필요해졌음을 발견한다** (3장 §"Comments", p.84).[^fowler2018]
- 처방 셋 — **코드 블록이 무엇을 하는지 설명할 주석이 필요하면 *Extract Function*을 시도하라.
  메서드가 이미 추출됐는데도 그것이 무엇을 하는지 설명할 주석이 여전히 필요하면 *Change
  Function Declaration*으로 이름을 바꿔라. 시스템의 요구되는 상태에 대한 규칙을 진술해야
  하면 *Introduce Assertion*을 쓰라** (3장 §"Comments", p.84).[^fowler2018]
- 조문 (3장 §"Comments", p.84):[^fowler2018]

> When you feel the need to write a comment, first try to refactor the code so that any
> comment becomes superfluous.

- **주석이 정당한 자리도 명시된다** — **주석을 쓰기 좋은 때는 무엇을 해야 할지 모를 때다.
  무슨 일이 일어나는지 서술하는 것에 더해, 주석은 당신이 확신하지 못하는 영역을 가리킬 수
  있다. 주석은 또한 당신이 무언가를 *왜* 했는지 설명할 수 있다. 이런 종류의 정보는 미래의
  수정자, 특히 잘 잊는 이들에게 도움이 된다** (3장 §"Comments", p.84).[^fowler2018]

## 냄새에서 카탈로그로 — 처방 대응표

이 장이 스스로 밝힌 사용법이 색인이다 — **당신이 무엇을 냄새 맡고 있는지 식별해 보고, 우리가
제안하는 리팩터링으로 가서 그것이 도움이 되는지 보라** (3장, p.72).[^fowler2018] 아래 표가 그
"가서"의 목적지를 한자리에 모은 것이고, 오른쪽 열이 그 항목이 사는 이 KB의 페이지다.

| 냄새 | 이 장이 지목하는 리팩터링 | 어디에 |
|---|---|---|
| Mysterious Name | Change Function Declaration · Rename Variable · Rename Field | [기본](basic-refactorings.md) · [데이터](organizing-data.md) |
| Duplicated Code | Extract Function · Slide Statements · Pull Up Method | [기본](basic-refactorings.md) · [이동](moving-features.md) · [상속](refactoring-inheritance.md) |
| Long Function | Extract Function · Replace Temp with Query · Introduce Parameter Object · Preserve Whole Object · Replace Function with Command · Decompose Conditional · Replace Conditional with Polymorphism · Split Loop | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) · [조건](simplifying-conditional-logic.md) · [API](refactoring-apis.md) |
| Long Parameter List | Replace Parameter with Query · Preserve Whole Object · Introduce Parameter Object · Remove Flag Argument · Combine Functions into Class | [기본](basic-refactorings.md) · [API](refactoring-apis.md) |
| Global Data | Encapsulate Variable | [기본](basic-refactorings.md) |
| Mutable Data | Encapsulate Variable · Split Variable · Slide Statements · Extract Function · Separate Query from Modifier · Remove Setting Method · Replace Derived Variable with Query · Combine Functions into Class · Combine Functions into Transform · Change Reference to Value | [기본](basic-refactorings.md) · [이동](moving-features.md) · [데이터](organizing-data.md) · [API](refactoring-apis.md) |
| Divergent Change | Split Phase · Move Function · Extract Function · Extract Class | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) |
| Shotgun Surgery | Move Function · Move Field · Combine Functions into Class · Combine Functions into Transform · Split Phase · Inline Function · Inline Class | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) |
| Feature Envy | Move Function · Extract Function | [기본](basic-refactorings.md) · [이동](moving-features.md) |
| Data Clumps | Extract Class · Introduce Parameter Object · Preserve Whole Object | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [API](refactoring-apis.md) |
| Primitive Obsession | Replace Primitive with Object · Replace Type Code with Subclasses · Replace Conditional with Polymorphism · Extract Class · Introduce Parameter Object | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [조건](simplifying-conditional-logic.md) · [상속](refactoring-inheritance.md) |
| Repeated Switches | Replace Conditional with Polymorphism | [조건](simplifying-conditional-logic.md) |
| Loops | Replace Loop with Pipeline | [이동](moving-features.md) |
| Lazy Element | Inline Function · Inline Class · Collapse Hierarchy | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [상속](refactoring-inheritance.md) |
| Speculative Generality | Collapse Hierarchy · Inline Function · Inline Class · Change Function Declaration · Remove Dead Code | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) · [상속](refactoring-inheritance.md) |
| Temporary Field | Extract Class · Move Function · Introduce Special Case | [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) · [조건](simplifying-conditional-logic.md) |
| Message Chains | Hide Delegate · Extract Function · Move Function | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) |
| Middle Man | Remove Middle Man · Inline Function · Replace Superclass with Delegate · Replace Subclass with Delegate | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [상속](refactoring-inheritance.md) |
| Insider Trading | Move Function · Move Field · Hide Delegate · Replace Subclass with Delegate · Replace Superclass with Delegate | [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) · [상속](refactoring-inheritance.md) |
| Large Class | Extract Class · Extract Superclass · Replace Type Code with Subclasses | [캡슐화](encapsulation-refactorings.md) · [상속](refactoring-inheritance.md) |
| Alternative Classes with Different Interfaces | Change Function Declaration · Move Function · Extract Superclass | [기본](basic-refactorings.md) · [이동](moving-features.md) · [상속](refactoring-inheritance.md) |
| Data Class | Encapsulate Record · Remove Setting Method · Move Function · Extract Function | [기본](basic-refactorings.md) · [캡슐화](encapsulation-refactorings.md) · [이동](moving-features.md) · [API](refactoring-apis.md) |
| Refused Bequest | Push Down Method · Push Down Field · Replace Subclass with Delegate · Replace Superclass with Delegate | [상속](refactoring-inheritance.md) |
| Comments | Extract Function · Change Function Declaration · Introduce Assertion | [기본](basic-refactorings.md) · [조건](simplifying-conditional-logic.md) |

- 표를 세로로 읽으면 **가장 많은 냄새가 부르는 항목**이 드러난다. *Extract Function*과
  *Move Function*이 각각 여덟 냄새 이상에서 불리고, 이 둘이 카탈로그의 중심 항목인 이유가 여기
  있다. 처방이 단 하나뿐인 냄새는 셋이다 — Global Data, Repeated Switches, Loops.
- **거꾸로 대조하면 3장이 지목하지 않는 항목이 남는다.** 카탈로그 61개 중 이 장이 부르는 것은
  44개이고, 나머지 17개는 어느 냄새도 처방으로 지목하지 않는다 — *Extract Variable*·
  *Inline Variable*(6장), *Encapsulate Collection*·*Substitute Algorithm*(7장),
  *Move Statements into Function*·*Move Statements to Callers*·*Replace Inline Code with
  Function Call*(8장), *Change Value to Reference*(9장), *Consolidate Conditional
  Expression*·*Replace Nested Conditional with Guard Clauses*(10장), *Parameterize
  Function*·*Replace Query with Parameter*·*Replace Constructor with Factory Function*·
  *Replace Command with Function*(11장), *Pull Up Field*·*Pull Up Constructor Body*·
  *Remove Subclass*(12장).
  - #hypothesis 이 열일곱은 대체로 **다른 리팩터링의 부품이거나 그 역**이다. 냄새는 눈에 보이는
    증상을 가리키는데 이 항목들은 증상이 아니라 수순 중간에 필요해지는 수라서 색인에 오르지
    않는 것으로 보인다. 근거로는 각 항목의 Mechanics가 이 열일곱을 자주 부른다는 것뿐이라
    저자가 그렇게 말한 자리는 없다.
- **이 표는 3장 본문에서만 뽑았다.** 이 장은 별도로 **뒤표지 안쪽의 표**를 함께 보라고
  안내하는데(3장, p.71), 이 KB의 아카이브 PDF에는 그 표가 들어 있지 않다. 두 목록이 어긋날
  가능성은 확인하지 못했다.

## 설계 잣대를 세운 소스와 갈리는 자리

이 축에는 [A Philosophy of Software Design](../sources/ousterhout2021.md)이 먼저 들어와
있고, 그쪽과 이 장이 **두 자리에서 정면으로 만난다.** 둘 중 하나는 관점 차이로, 다른 하나는
같은 명제의 참거짓이 갈리는 모순으로 판정했다. 그 뒤에 들어온
[Fluent Python](../sources/ramalho2022.md)과도 한 자리에서 만나는데, 그쪽은 모순이 아니다.

### 함수 크기 — 관점 차이다

- 표면적으로는 반대로 보인다. 이 장은 **가장 오래 사는 프로그램은 짧은 함수를 가진 것들**이고
  **함수 분해에 훨씬 더 공격적이어야 한다**고 하고, 그쪽은 **길이 자체는 메서드를 쪼갤 좋은
  이유가 되는 일이 드물다. 일반적으로 개발자는 메서드를 너무 많이 쪼개는 경향이 있다**
  (9장 §9.7, p.73)라고 한다.[^ousterhout2021]
- **그러나 둘 다 길이를 기준에서 뺀다.** 이 장은 **핵심은 함수 길이가 아니라 의미적
  거리**라 하고, 그쪽은 **깊이가 길이보다 중요하다**고 한다 (9장 §9.8,
  p.76).[^ousterhout2021] 시험도 사실상 같다 — 이쪽은
  "이름만 보고 본문을 안 봐도 되는가", 그쪽은 "쪼개기가 시스템 전체의 복잡성을 줄이는가".
- 갈리는 것은 **사전 확률**이다. 이 장은 대부분의 사람이 **덜** 쪼갠다고 보고, 그쪽은 대부분의
  개발자가 **더** 쪼갠다고 본다. 같은 잣대에 대고 반대 방향의 경험적 판단을 하는 것이므로
  모순이 아니라 관측 대상의 차이로 읽는다. #hypothesis 두 소스가 서로를 참조한 적은 없고,
  그쪽이 명시적으로 반박하는 상대는 이 책이 아니라 *Clean Code*다 — 전문은
  [합칠 것인가 나눌 것인가](better-together-or-better-apart.md)에 있다.

### 주석 — 모순으로 판정했다

- **같은 명제의 참거짓이 갈린다.** 이 장은 **함수에 좋은 이름이 있으면 대개 그 본문을 볼
  필요가 없다**(3장 §"Long Function", p.73)고 하고, 그쪽은 **주석이 없으면 메서드의 유일한
  추상은 그 선언이며, 그것은 그 자체로 쓸모 있는 추상을 제공하기에는 너무 많은 본질적 정보를
  빠뜨린다**(12장 §12.1, p.97)고 한다.[^ousterhout2021] 그쪽이 드는 반례가 결정적이다 — `start`와 `end`를
  받는 부분 문자열 추출 메서드는 이름이 아무리 좋아도 `end` 포함 여부와 `start > end`일 때의
  동작을 선언만으로는 알 수 없다.
- **처방도 정면으로 갈린다.** 이 장의 조문은 **주석을 쓰고 싶으면 먼저 리팩터링해 그 주석이
  불필요해지게 하라**이고, 그쪽은 **"좋은 코드는 스스로 문서화한다"는 맛있는 신화**라고
  부르며 그 기대가 **다수의 얕은 메서드를 낳는다**고 진단한다(12장 §12.1,
  p.96).[^ousterhout2021]
- **층위 차이로 볼 수 없는 이유**: 이 장의 처방은 인라인 주석에 그치지 않는다 — **메서드가
  이미 추출됐는데도 그것이 무엇을 하는지 설명할 주석이 여전히 필요하면 이름을 바꿔라**
  (3장 §"Comments", p.84)는 명백히 인터페이스 주석 층위의 처방이고, 그쪽이 필수라고 하는
  바로 그 자리다.
- **겹치는 구간도 있다.** 이 장도 **왜**를 설명하는 주석과 불확실성을 표시하는 주석은
  정당하다고 한다. 그쪽도 좋은 이름이 주석의 필요를 줄인다는 데 동의한다 (12장 §12.1,
  p.96).[^ousterhout2021]
  갈리는 것은 **좋은 이름을 가진 선언이 인터페이스 주석을 대신할 수 있는가** 하나다.
  해소하지 않고 양쪽에 `contradicts`로 남긴다 — 상대는
  [주석을 왜 쓰는가](why-write-comments.md)다.

### 데이터 클래스 — 모순이 아니다

겉보기에는 부딪힌다. 이 장은 *Data Class*를 냄새 목록에 올리고, *Fluent Python* 5장은
데이터 클래스를 만드는 도구 셋을 소개하며 그 사용을 권한다. **실측 판정은 모순이 아니다.**
근거 셋이다.

- **① 그쪽이 이 항목을 인용하고 지지한다.** 반박이 아니라 재수록이다 — 파울러의 글
  "Code Smell" 전문이 그 절에 실려 있고, 저자는 **그래서 파울러가 데이터 클래스를 다루는
  리팩터링들이 책임을 그 안으로 되가져오는 것이다**라고 처방까지 승인한다
  (5장 §"Data class as a code smell").[^ramalho2022] 장 요약도 같은 말을 다시 한다 —
  **논리가 없는 클래스는 잘못 놓인 로직의 신호일 수 있다** (5장 §"Chapter
  Summary").[^ramalho2022]
- **② 예외가 서로 같은 것을 가리킨다.** 이 항목이 인정하는 예외는 **별개의 함수 호출에서
  나온 결과 레코드**이고 그 핵심 특성이 **불변**이다(위 참조). 그쪽이 드는 둘째 시나리오가
  **중간 표현**이고 거기 붙는 단서가 **이 시나리오에서 데이터 클래스 인스턴스는 불변 객체로
  다뤄져야 한다**(5장 §"Data class as intermediate representation")[^ramalho2022]이다.
  범위도 단서도 일치한다.
- **③ 갈리는 것은 명제가 아니라 대상이다.** 이 항목이 겨냥하는 것은 **널리 쓰이면서 행동이
  없는 도메인 클래스**이고, 그쪽이 권하는 것은 **보일러플레이트를 대신 써 주는 도구**다.
  도구가 만든 클래스가 냄새인지는 그 클래스가 무엇으로 쓰이느냐가 정하고, 그 판정 기준을
  그쪽이 이 항목에서 그대로 빌려 온다.
- 그래서 `contradicts`를 걸지 않고 서로 가리키게만 두었다. 위 [주석](#주석--모순으로-판정했다)
  자리와 대비된다 — 거기서는 같은 명제의 참거짓이 갈렸고, 여기서는 갈리지 않는다.

## 이어지는 페이지

- [리팩터링](refactoring.md) — 이 냄새들이 부르는 활동의 정의
- [언제 리팩터링하는가](when-to-refactor.md) — 냄새 말고 작업 흐름 쪽의 계기
- [리팩터링 카탈로그를 읽는 법](refactoring-catalog-format.md) — 위 표의 목적지들이 어떤 규약으로
  쓰였는가
- [기본 리팩터링](basic-refactorings.md) — 6장. *Extract Function*을 비롯한 열한 항목
- [캡슐화 리팩터링](encapsulation-refactorings.md) — 7장. *Extract Class*·*Replace Primitive
  with Object*가 사는 곳
- [기능 이동 리팩터링](moving-features.md) — 8장. *Move Function*·*Move Field*가 사는 곳
- [데이터 조직화 리팩터링](organizing-data.md) — 9장. *Split Variable*·*Replace Derived
  Variable with Query*가 사는 곳
- [조건부 로직 단순화 리팩터링](simplifying-conditional-logic.md) — 10장.
  *Replace Conditional with Polymorphism*이 사는 곳
- [API 리팩터링](refactoring-apis.md) — 11장. *Remove Flag Argument*·*Preserve Whole Object*가
  사는 곳
- [상속 다루기 리팩터링](refactoring-inheritance.md) — 12장. *Push Down Method*와 위임 교체 둘이
  사는 곳
- [코드 냄새로서의 데이터 클래스](data-class-as-code-smell.md) — *Data Class* 항목을
  파이썬 쪽에서 되받은 자리. 파울러의 "Code Smell" 글 전문과 정당한 두 경우
- [데이터 클래스 빌더](data-class-builders.md) — 그 냄새를 만들어 내는 도구 셋의 비교
- [주석을 왜 쓰는가](why-write-comments.md) — **`contradicts` 상대.** 주석 냄새의 반대편
- [합칠 것인가 나눌 것인가](better-together-or-better-apart.md) — 함수 크기 쟁점의 반대편
- [DRY 원칙](dry-principle.md) — Duplicated Code의 원리 쪽 정본
- [이름 짓기](naming-things.md) — Mysterious Name의 정본
- [결합 끊기](decoupling.md) — 기능 편애·내부자 거래·메시지 체인이 재는 것
- [직교성](orthogonality.md) — 발산하는 변경·산탄총 수술이 재는 것
- [상속세](inheritance-tax.md) — 상속 포기·내부자 거래의 상속 쪽 판정
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^fowler2018]: Fowler 2018, 3장 "Bad Smells in Code"(Kent Beck 공저, pp.71–84) 전체.
    2장의 인용 한 줄은 §"Refactoring Improves the Design of Software"(p.47)에서 왔다.
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 —
    이 소스의 표준 규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다.
    각 냄새가 지목하는 리팩터링 이름은 5장 이후 카탈로그의 항목이다 — 이 페이지는 이름만
    원어로 옮기고 절차는 옮기지 않는다.

[^ousterhout2021]: Ousterhout 2021, 9장 §9.7–§9.8 · 12장 §12.1. 쪽은 인쇄판 쪽 번호.

[^ramalho2022]: Ramalho 2022, 5장 "Data Class Builders" 중 §"Data class as a code
    smell"(안에 전문 재수록된 Martin Fowler, "Code Smell" 포함) · §"Data class as
    scaffolding" · §"Data class as intermediate representation" · §"Chapter Summary".
    **이 소스의 locator는 장 + 절 제목이다** — 인쇄판 쪽 앵커가 없다. **이 스냅샷은
    Early Release 판이라 절 제목이 정식 출간본 표기(§"Data Class as a Code Smell")와
    대소문자가 다르다.** 검증 절차와 근거는 `it/archive/ramalho2022/_progress.yaml`
    머리말이 정본이다.

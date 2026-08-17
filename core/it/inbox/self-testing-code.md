---
type: concept
title: 자기 테스트 코드
description: 테스트를 코드베이스 안에 넣고 결과 확인까지 자동화한 코드라는 규정과 그것이 리팩터링의 전제가 되는 이유 — 저자가 디버깅 시간이 사라지는 것을 관측한 경위, 테스트가 실패해야 할 때 실패하는지 일부러 확인하는 습관, 위험 주도로 무엇을 테스트할지 고르는 기준, 공유 픽스처가 낳는 비결정성과 매번 새로 만드는 처방, 준비-실행-검증이라는 네 국면, 경계와 나쁜 입력을 겨냥하는 적대적 태도, 실패와 오류의 구분, 그리고 "얼마나 테스트하면 충분한가"에 대한 주관적 기준
generated: { by: "claude-opus-5", at: "2026-08-17T12:00:00Z" }
status: draft
sources:
  - { id: fowler2018, resource: /it/sources/fowler2018.md }
  - { id: percival2020, resource: /it/sources/percival2020.md }
  - { id: martin2008, resource: /it/sources/martin2008.md }
  - { id: qntm2020, resource: /it/sources/qntm2020.md }
  - { id: ousterhout2024-aposd, resource: /it/sources/ousterhout2024-aposd.md }
---

# 자기 테스트 코드

- [정의와 이 장의 지위](#정의와-이-장의-지위)
- [디버깅 시간이 사라진 경위](#디버깅-시간이-사라진-경위)
- [테스트가 실패해야 할 때 실패하는지 확인하라](#테스트가-실패해야-할-때-실패하는지-확인하라)
- [무엇을 테스트할지 — 위험 주도](#무엇을-테스트할지--위험-주도)
- [픽스처는 매번 새로 만든다](#픽스처는-매번-새로-만든다)
- [준비-실행-검증, 그리고 말하지 않는 넷째](#준비-실행-검증-그리고-말하지-않는-넷째)
- [경계를 찔러 보라](#경계를-찔러-보라)
- [실패와 오류는 다르다](#실패와-오류는-다르다)
- [얼마나 테스트하면 충분한가](#얼마나-테스트하면-충분한가)
- [테스트에도 층이 있고 층마다 굳히는 것이 다르다](#테스트에도-층이-있고-층마다-굳히는-것이-다르다)
- [셋째 소스가 더하는 것 — TDD 세 법칙과 F.I.R.S.T.](#셋째-소스가-더하는-것--tdd-세-법칙과-first)
- [번들링 — TDD의 대안에 이름이 붙다](#번들링--tdd의-대안에-이름이-붙다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **리팩터링(refactoring)이 담보로 잡는 그 테스트는 구체적으로 어떤 성질을
가져야 하는가.**

## 정의와 이 장의 지위

- 이 장의 전제 — **리팩터링은 값진 도구지만 혼자 올 수는 없다. 리팩터링을 제대로 하려면
  내 불가피한 실수를 찾아낼 견고한 테스트 모음이 필요하다. 자동 리팩터링 도구가 있어도
  내 리팩터링 중 많은 것은 여전히 테스트 모음을 통한 검사가 필요하다** (4장,
  p.85).[^fowler2018]
- **그런데 저자는 그것을 단점으로 치지 않는다** — **나는 이것을 단점이라고 보지 않는다.
  리팩터링이 없더라도 좋은 테스트를 쓰는 것은 프로그래머로서의 내 효과를 높인다. 이것은
  나에게 놀라운 일이었고 대부분의 프로그래머에게 반직관적이다 — 그래서 왜 그런지 설명할
  가치가 있다** (4장, p.85).[^fowler2018]
- 자기 테스트 코드(self-testing code)라는 말의 뜻은 2장이 정의한다 — **내가 프로그래밍에서
  오류를 냈다면 어떤 테스트가 실패하리라고 자신할 수 있는 자동화된 테스트 모음이 있다는
  뜻이다** (2장 §"Refactoring and the Wider Software Development Process",
  p.63).[^fowler2018]
- 세 실천이 서로를 강화한다는 것이 2장의 판정이다 — **자기 테스트 코드는 지속적 통합의 핵심
  요소이기도 하므로, 자기 테스트 코드·지속적 통합·리팩터링 세 실천 사이에는 강한 시너지가
  있다** (2장 §"Refactoring and the Wider Software Development Process",
  p.63).[^fowler2018]

## 디버깅 시간이 사라진 경위

- 문제 규정 — **대부분의 프로그래머가 시간을 어떻게 쓰는지 보면 코드를 쓰는 것은 실은 꽤
  작은 비중이다. 어떤 시간은 무엇이 일어나야 하는지 알아내는 데, 어떤 시간은 설계하는 데
  쓰이지만, 가장 많은 시간은 디버깅에 쓰인다** (4장 §"The Value of Self-Testing Code",
  p.85).[^fowler2018]
- 계기가 된 것은 1992년 OOPSLA에서 들은 한 마디다 — **누군가(내 생각에 "Bedarra" Dave
  Thomas였다)가 무심히 "클래스는 자기 자신의 테스트를 담아야 한다"고 말했다** (4장 §"The
  Value of Self-Testing Code", p.85).[^fowler2018]
- **자동화의 결정적 걸음이 결과 확인이었다** — 처음에는 테스트가 콘솔에 출력을 내고 저자가
  눈으로 확인해야 했다. 그런데 — **화면을 보고 모델에서 나온 정보가 출력됐는지 확인하는
  대신, 컴퓨터가 그 검사를 하게 할 수 있다는 것을 깨달았다. 내가 할 일은 기대하는 출력을
  테스트 코드에 넣고 비교하게 하는 것뿐이었다. 이제 테스트를 돌리면 모든 것이 정상일 때
  화면에 그냥 "OK"를 찍었다. 소프트웨어가 이제 자기 테스트 상태가 됐다** (4장 §"The Value
  of Self-Testing Code", pp.85–86).[^fowler2018] 조문은 이 한 줄이다 (4장 §"The Value of
  Self-Testing Code", p.86):[^fowler2018]

> Make sure all tests are fully automatic and that they check their own results.

- **그리고 관측된 효과** — **내 생산성이 치솟은 것을 알아차리기 시작했다. 디버깅에 그렇게
  많은 시간을 쓰지 않고 있다는 것을 깨달았다. 이전 테스트가 잡아내는 버그를 넣었다면 그
  테스트를 돌리는 즉시 드러났다. 그 테스트는 전에 동작했으므로 버그가 마지막 테스트 이후에
  내가 한 작업 안에 있다는 것을 알 수 있었다. (…) 그렇지 않았다면 찾는 데 한 시간 이상
  걸렸을 버그가 이제 길어야 몇 분 걸렸다** (4장 §"The Value of Self-Testing Code",
  p.86).[^fowler2018] 조문 (4장 §"The Value of Self-Testing Code", p.86):[^fowler2018]

> A suite of tests is a powerful bug detector that decapitates the time it takes to find
> bugs.

- **테스트를 먼저 쓰는 것이 유용한 이유가 검사가 아니라 설계로 제시된다** — **사실 테스트를
  쓰기에 가장 유용한 때 중 하나는 프로그래밍을 시작하기 전이다. 기능을 더해야 할 때 나는
  테스트를 쓰는 것으로 시작한다. 이것은 들리는 것만큼 거꾸로 된 것이 아니다. 테스트를 씀으로써
  나는 그 기능을 더하려면 무엇이 이뤄져야 하는지 자문하는 것이다. 테스트를 쓰는 것은 또한
  나를 구현이 아니라 인터페이스에 집중하게 한다(늘 좋은 일이다). 그것은 또한 코딩이 끝나는
  지점이 분명해진다는 뜻이다 — 테스트가 통과할 때** (4장 §"The Value of Self-Testing Code",
  p.86).[^fowler2018]
  - TDD의 규정이 이어진다 — **테스트 주도 개발 접근은 (실패하는) 테스트를 쓰고, 그 테스트가
    통과하게 만드는 코드를 쓰고, 결과가 가능한 한 깨끗하도록 리팩터링하는 짧은 순환에 의존한다.
    이 테스트-코드-리팩터 순환은 시간당 여러 번 일어나야 하며, 코드를 쓰는 매우 생산적이고
    차분한 방식일 수 있다** (4장 §"The Value of Self-Testing Code", p.87).[^fowler2018]
    전문과 다른 소스의 유보는 [테스트가 코딩을 이끈다](test-to-code.md)에 있다.
- **이 책의 요구는 여기서 조건 없이 못 박힌다** — **리팩터링은 테스트를 요구한다. 리팩터링하고
  싶다면 테스트를 써야 한다** (4장 §"The Value of Self-Testing Code",
  p.87).[^fowler2018]

## 테스트가 실패해야 할 때 실패하는지 확인하라

- 회의의 근거 — **테스트를 많이 돌리게 되고 나면, 나는 어떤 테스트가 내가 생각하는 방식으로
  코드를 실제로 훈련시키지 않아서 필요할 때 버그를 못 잡을까 봐 늘 불안하다** (4장 §"A First
  Test", p.91).[^fowler2018] 조문 (4장 §"A First Test", p.91):[^fowler2018]

> Always make sure a test will fail when it should.

- 방법 — **그래서 나는 테스트를 쓸 때 모든 테스트가 적어도 한 번은 실패하는 것을 보고 싶어
  한다. 내가 가장 좋아하는 방법은 코드에 일시적으로 결함을 주입하는 것이다** (4장 §"A First
  Test", p.91).[^fowler2018]
- **기존 코드에 테스트를 더할 때의 절차가 네 걸음으로 명시된다** — **기대값 자리에 자리표시자를
  두고 쓴다, 자리표시자를 프로그램이 만들어 낸 값으로 바꾼다, 결함을 주입한다, 결함을 되돌린다.
  이것은 기존 코드에 테스트를 더할 때 내가 쓰는 흔한 패턴이다** (4장 §"Add Another Test",
  pp.93–94).[^fowler2018]
  - 두 번째 걸음이 무엇을 포기하는지가 적혀 있다 — **직접 손으로 계산할 수도 있었지만, 코드가
    올바로 동작하고 있다고 되어 있으므로 지금은 그냥 믿겠다** (4장 §"Add Another Test",
    p.93).[^fowler2018] 즉 이 절차는 **회귀 고정**이지 정확성 검증이 아니다.
- 실행 빈도의 조문도 이 절에 있다 (4장 §"A First Test", p.92):[^fowler2018]

> Run tests frequently. Run those exercising the code you're working on at least every
> few minutes; run all tests at least daily.

- 초록/빨강이라는 팀 어휘가 여기서 나온다 — **동료들은 테스트 상태를 서술하는 데 "green
  bar"와 "red bar"라는 표현을 흔히 쓴다. 나는 "빨간 막대에서는 절대 리팩터링하지 마라"고
  말할 수 있는데, 테스트 모음에 실패하는 테스트가 있으면 리팩터링해서는 안 된다는 뜻이다.
  또는 "초록으로 되돌려라"라고 말할 수 있는데, 최근 변경을 취소하고 모든 테스트가 통과하던
  마지막 상태로 돌아가야 한다는 뜻이다** (4장 §"A First Test", p.93).[^fowler2018]

## 무엇을 테스트할지 — 위험 주도

- 저자가 따르지 않는 규칙부터 밝힌다 — **내가 따르는 방식은 클래스가 해야 하는 모든 것을
  보고, 클래스를 실패하게 만들 수 있는 조건에 대해 각각을 테스트하는 것이다. 이것은 어떤
  프로그래머들이 주장하는 모든 공개 메서드를 테스트하는 것과 같지 않다** (4장 §"Add Another
  Test", p.93).[^fowler2018]
- 기준 — **테스팅은 위험 주도여야 한다; 기억하라, 나는 지금이든 미래든 버그를 찾으려는
  것이다. 따라서 나는 그저 필드를 읽고 쓰는 접근자는 테스트하지 않는다: 그것들은 너무
  단순해서 거기서 버그를 찾을 가능성이 낮다** (4장 §"Add Another Test",
  p.93).[^fowler2018]
- **이 절제가 왜 중요한지에 대한 이유가 붙는다** — **이것이 중요한 것은 너무 많은 테스트를
  쓰려 하는 것이 보통 충분히 쓰지 않는 결과로 이어지기 때문이다. 조금만 테스트해도 나는
  테스팅에서 많은 이득을 얻는다** (4장 §"Add Another Test", p.93).[^fowler2018] 조문
  (4장 §"Add Another Test", p.93):[^fowler2018]

> It is better to write and run incomplete tests than not to run complete tests.

## 픽스처는 매번 새로 만든다

픽스처(fixture)는 테스트가 딛고 서는 데이터와 객체다 — 이 책의 첫 테스트가 그것을
**테스트에 필요한 데이터와 객체**라고 규정한다 (4장 §"A First Test",
p.91).[^fowler2018]

- 테스트 코드의 중복도 코드의 중복이다 — **일반 코드의 중복을 의심하는 것과 마찬가지로 나는
  테스트 코드의 중복도 의심하므로 그것을 공통 자리로 인수분해해 없애려 한다** (4장 §"Add
  Another Test", p.94).[^fowler2018]
- **그러나 바깥 스코프의 상수로 끌어올리는 방식은 금지된다** — 저자는 그 코드에 **DON'T DO
  THIS** 주석을 붙여 보인 뒤 이유를 적는다 — **당장은 동작하지만, 그것은 테스팅에서 가장
  고약한 버그 중 하나에 딱 맞는 배양 접시를 들여온다 — 테스트들이 서로 상호작용하게 만드는
  공유 픽스처다. 자바스크립트의 `const` 키워드는 `asia`라는 참조가 상수라는 뜻일 뿐 그 객체의
  내용이 상수라는 뜻이 아니다. 미래의 어떤 테스트가 그 공통 객체를 바꾸면, 테스트가 돌아가는
  순서에 따라 다른 결과를 내면서 테스트들이 공유 픽스처를 통해 상호작용하는 간헐적 테스트
  실패를 얻게 될 것이다** (4장 §"Add Another Test", p.94).[^fowler2018]
- 대신 쓰는 것이 매 테스트 전 재생성이다. 이 장의 대표 코드 조각이 그것이다 (4장 §"Add
  Another Test", p.94):[^fowler2018]

  ```js
  describe('province', function() {
    let asia;
    beforeEach(function() {
      asia = new Province(sampleProvinceData());
    });
    it('shortfall', function() {
      expect(asia.shortfall).equal(5);
    });
    it('profit', function() {
      expect(asia.profit).equal(230);
    });
  });
  ```

- 성능 우려에 대한 답 — **이 조언을 하면 매번 새 픽스처를 만드는 것이 테스트를 느리게 할까
  걱정하는 사람들이 있다. 대부분의 경우 눈에 띄지 않을 것이다. 문제가 된다면 공유 픽스처를
  고려하겠지만, 그때는 어떤 테스트도 그것을 절대 바꾸지 않도록 정말 주의해야 할 것이다.
  (…) 그러나 공유 픽스처에서 실수하는 디버깅 비용에 너무 자주 물려 봤기 때문에 내 반사
  반응은 새 픽스처를 쓰는 것이다** (4장 §"Add Another Test", pp.94–95).[^fowler2018]
- **`beforeEach` 안에 두는 것과 각 테스트 안에 두는 것의 차이는 독자에게 주는 신호다** —
  **나는 내 테스트들이 공통의 픽스처 조각 위에서 동작하기를 좋아한다. 그래야 그 표준 픽스처에
  익숙해지고 그것에 대해 테스트할 다양한 특성을 볼 수 있다. `beforeEach` 블록의 존재는 내가
  표준 픽스처를 쓰고 있다는 것을 독자에게 신호한다** (4장 §"Modifying the Fixture",
  p.95).[^fowler2018]

## 준비-실행-검증, 그리고 말하지 않는 넷째

- 흔한 패턴의 이름 — **나는 `beforeEach` 블록이 **준비한** 초기 표준 픽스처를 가져다, 테스트를
  위해 그 픽스처를 **실행하고**, 그런 다음 픽스처가 내가 생각한 대로 했는지 **검증한다**.
  테스트에 관해 많이 읽었다면 이 국면들이 setup-exercise-verify, given-when-then,
  arrange-act-assert로 다양하게 불리는 것을 들었을 것이다** (4장 §"Modifying the Fixture",
  p.95).[^fowler2018]
- **넷째가 명시된다** — **보통 언급되지 않는 암묵의 넷째 국면이 있다: **정리**(teardown).
  정리는 테스트 사이에 픽스처를 없애 서로 다른 테스트가 상호작용하지 않게 한다. 모든 준비를
  `beforeEach`에서 함으로써 나는 테스트 프레임워크가 테스트 사이에 내 픽스처를 암묵적으로
  정리하게 하고, 그래서 정리 국면을 당연한 것으로 여길 수 있다** (4장 §"Modifying the
  Fixture", p.95).[^fowler2018]
- **검증문 개수에 대한 규칙과 그 예외** — **일반 규칙으로 각 `it` 절에 검증문을 하나만 두는
  것이 현명하다. 테스트가 첫 검증 실패에서 실패하기 때문인데, 그것은 테스트가 왜 깨졌는지
  알아낼 때 유용한 정보를 흔히 감춘다. 이 경우에는 둘이 충분히 밀접히 연결돼 있다고 느껴서
  같은 테스트에 두는 데 만족한다** (4장 §"Modifying the Fixture", p.96).[^fowler2018]

## 경계를 찔러 보라

- 행복 경로를 벗어나라는 요구 — **지금까지 내 테스트는 모든 것이 잘 돌아가고 예상대로 쓰이는
  "행복 경로"(happy path) 조건이라 흔히 불리는 통상적 사용에 초점을 맞췄다. 그러나 이 조건의
  경계에도 테스트를 던져 보는 것이 좋다 — 일이 잘못될 수 있을 때 무슨 일이 일어나는지 보려고**
  (4장 §"Probing the Boundaries", p.96).[^fowler2018] 조문 (4장 §"Probing the Boundaries",
  p.97):[^fowler2018]

> Think of the boundary conditions under which things might go wrong and concentrate your
> tests there.

- 저자가 실제로 던지는 것들 — **컬렉션이 있으면 그것이 비었을 때 무슨 일이 일어나는지 본다**,
  **숫자에서는 0이 찔러 볼 좋은 것이다**, 그리고 음수와 빈 문자열이다 (4장 §"Probing the
  Boundaries", pp.96–97).[^fowler2018]
- **경계 테스트가 코드가 아니라 도메인 질문을 낳는다는 것이 이 절의 요점이다** — **이 지점에서
  나는 음수 수요가 음수 이익을 낳는 것이 이 도메인에서 정말 말이 되는지 궁금해지기 시작할 수
  있다. 최소 수요는 0이어야 하지 않을까? 그렇다면 세터가 음수 인수에 다르게 반응해야 하지
  않을까 — 오류를 일으키거나 어쨌든 값을 0으로 설정하거나. 이것들은 물어볼 좋은 질문이고,
  이런 테스트를 쓰는 것은 코드가 경계 사례에 어떻게 반응해야 하는지 생각하는 데 도움이 된다**
  (4장 §"Probing the Boundaries", p.97).[^fowler2018]
- 저자가 이때 취하는 자세 — **내가 내 코드의 적 역할을 하고 있음을 눈여겨보라. 나는 그것을
  어떻게 깨뜨릴 수 있을지 능동적으로 생각하고 있다. 나는 그 심리 상태가 생산적이면서 재미있다고
  느낀다** (4장 §"Probing the Boundaries", p.97).[^fowler2018]

## 실패와 오류는 다르다

- 구분 — **실패(failure)는 실제 값이 검증문이 기대하는 범위 밖에 있는 검증 단계를 가리킨다.
  그러나 이 **오류**(error)는 다른 동물이다 — 그것은 더 이른 국면(이 경우 준비)에서 일어난
  예외다** (4장 §"Probing the Boundaries", p.98).[^fowler2018]
- **입력 검증을 넣을지의 판정 기준이 신뢰 경계다** — **어쩌면 입력 객체가 신뢰할 수 있는
  출처 — 이를테면 같은 코드베이스의 다른 부분 — 에서 나오는지도 모른다. 같은 코드베이스의
  모듈 사이에 많은 검증 검사를 넣으면 다른 데서 하는 검증을 중복해 득보다 실이 큰 중복 검사를
  낳을 수 있다. 그러나 그 입력 객체가 JSON 인코딩된 요청 같은 외부 출처에서 들어온다면 검증
  검사가 필요하고 테스트돼야 한다** (4장 §"Probing the Boundaries", p.98).[^fowler2018]
- **리팩터링 전에 쓰는 테스트라면 이런 테스트는 버린다** — **리팩터링 전에 이런 테스트를
  쓰고 있다면 나는 아마 이 테스트를 버릴 것이다. 리팩터링은 관찰 가능한 동작을 보존해야
  한다; 이런 오류는 관찰 가능한 것의 범위 밖이므로, 내 리팩터링이 이 조건에 대한 코드의 반응을
  바꾸더라도 걱정할 필요가 없다** (4장 §"Probing the Boundaries", p.98).[^fowler2018]
  - 이 문장이 [리팩터링](refactoring.md)의 "관찰 가능한 동작"이라는 느슨한 말에 **테스트
    설계상의 실무적 경계**를 준다. 관찰 가능성의 바깥은 테스트로 고정하지 않는다.
- 단정문과 테스트의 관계 — **이 오류가 나쁜 데이터를 프로그램 안에 돌아다니게 해서 디버깅하기
  어려운 실패를 일으킬 수 있다면, 나는 *Introduce Assertion*으로 빨리 실패하게 할 수도 있다.
  나는 그런 단정 실패를 잡는 테스트를 더하지 않는데, 그것들 자체가 일종의 테스트이기 때문이다**
  (4장 §"Probing the Boundaries", p.98).[^fowler2018] 같은 계열의 판정이
  [죽은 프로그램은 거짓말하지 않는다](dead-programs-tell-no-lies.md)에 있다.

## 얼마나 테스트하면 충분한가

- 완전성 추구를 저자가 명시적으로 만류한다 (4장 §"Probing the Boundaries",
  p.98):[^fowler2018]

> Don't let the fear that testing can't catch all bugs stop you from writing tests that
> catch most bugs.

  **테스팅에는 수확 체감의 법칙이 있고, 너무 많은 테스트를 쓰려다 낙담해서 결국 아무것도
  쓰지 않게 될 위험이 있다** (4장 §"Probing the Boundaries", pp.98–99).[^fowler2018]
- **버그 보고에 대한 반응 절차가 조문으로 있다** (4장 §"Much More Than This",
  p.99):[^fowler2018]

> When you get a bug report, start by writing a unit test that exposes the bug.

  이유 — **테스트를 가짐으로써 나는 그 버그가 죽은 채로 있으리라는 것을 안다. 나는 또한 그
  버그와 그 테스트에 대해 생각한다: 그것이 테스트 모음의 다른 빈틈에 대한 단서를 주는가?**
  (4장 §"Much More Than This", p.99).[^fowler2018]
- **커버리지에 대한 판정** — **어떤 사람들은 테스트 커버리지를 척도로 쓰자고 주장하지만,
  테스트 커버리지 분석은 코드의 테스트되지 않은 영역을 식별하는 데만 좋고 테스트 모음의
  품질을 평가하는 데는 좋지 않다** (4장 §"Much More Than This", p.99).[^fowler2018]
- **그래서 남는 기준은 주관적이다** — **충분히 좋은 테스트 모음의 가장 좋은 척도는 주관적이다:
  누군가 코드에 결함을 넣으면 어떤 테스트가 실패하리라고 얼마나 확신하는가? 이것은 객관적으로
  분석될 수 있는 것이 아니고 근거 없는 확신을 걸러 내지도 못하지만, 자기 테스트 코드의 목표는
  그 확신을 얻는 것이다** (4장 §"Much More Than This", p.100).[^fowler2018]
- **과잉 테스트도 존재하지만 드물다** — **너무 많은 테스트를 쓰는 것은 가능하다. 그 신호
  하나는 테스트 대상 코드보다 테스트를 바꾸는 데 더 많은 시간을 쓰고 테스트가 나를 느리게
  한다고 느낄 때다. 그러나 과잉 테스트가 일어나기는 하지만, 과소 테스트에 비하면 사라질
  만큼 드물다** (4장 §"Much More Than This", p.100).[^fowler2018]
- 테스트 모음 자체가 리팩터링 대상이라는 것도 명시된다 — **테스팅은 반복적 활동이다. (…)
  나는 주 코드를 작업하는 만큼이나 테스트 모음을 계속 작업하고 있음을 발견한다. (…) 그것들이
  충분히 명료한가? 무엇을 하는지 더 쉽게 이해하도록 리팩터링해야 하는가? 나는 올바른 테스트를
  갖고 있는가?** (4장 §"Much More Than This", p.99).[^fowler2018]

## 테스트에도 층이 있고 층마다 굳히는 것이 다르다

이 페이지는 테스트 모음이 갖춰야 할 **성질**을 다룬다. 파이썬 아키텍처 쪽 소스는 같은
테스트를 **어느 층에 붙일 것인가**를 묻고, 그 선택이 무엇을 굳히는지를 규정한다.

- 진단이 한 문장이다 (5장 §"Should Domain Layer Tests Move to the Service
  Layer?"):[^percival2020]

  > Every line of code that we put in a test is like a blob of glue, holding the system in a
  > particular shape. The more low-level tests we have, the harder it will be to change things.

- 그래서 위 [얼마나 테스트하면 충분한가](#얼마나-테스트하면-충분한가)의 주관적 기준에
  **층이라는 축이 하나 더 붙는다.** 그쪽 소스는 낮은 층일수록 피드백이 높고 변경의 장벽도
  높다는 절충으로 그것을 정리한다 — 전문은
  [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)에 있다.
- **테스트를 지우는 것이 정상 절차로 규정된다** — **도메인 모델을 상대로 쓴 작은 핵심
  테스트 모음을 유지하라. 이 테스트들은 아주 초점이 맞은 커버리지를 갖고 더 잘 깨지지만,
  가장 높은 피드백을 갖는다. 나중에 서비스 레이어의 테스트가 그 기능을 다루게 되면 이
  테스트들을 지우기를 두려워하지 마라**
  (5장 §"Recap: Rules of Thumb for Different Types of Test" 곁글).[^percival2020]
  - 위 절들이 테스트를 **쌓는** 규율을 말한다면 이쪽은 **버리는** 규율을 말한다. 같은
    소스가 6장에서 실제로 그렇게 한다 — **더 오래 값을 더하지 않을 것 같다고 생각하면
    언제든 자유롭게 테스트를 버려라**
    (6장 §"Tidying Up the Integration Tests").[^percival2020]
  - **위 [테스트가 실패해야 할 때 실패하는지 확인하라](#테스트가-실패해야-할-때-실패하는지-확인하라)와
    긴장하지 않는다.** 그쪽은 남아 있는 테스트가 제 구실을 하는지 묻고, 이쪽은 어떤 테스트가
    남을 값어치가 있는지 묻는다. #hypothesis 두 소스가 서로를 참조한 적은 없다.
- 그리고 무엇이 실패해야 하는지에 대한 규정이 다르다. 이 페이지의 소스는 **결함을 넣으면
  어떤 테스트가 실패하리라는 확신**을 기준으로 삼고, 그쪽 소스는 **시스템의 어떤 성질이
  바뀌지 않도록 강제하는 것**을 테스트의 목적으로 둔다 — **API가 계속 200을 돌려주는지,
  데이터베이스 세션이 계속 커밋하는지, 주문이 여전히 할당되고 있는지**
  (5장 §"Should Domain Layer Tests Move to the Service Layer?").[^percival2020]
  두 기준이 같은 것을 다르게 말한 것이다.

## 셋째 소스가 더하는 것 — TDD 세 법칙과 F.I.R.S.T.

논쟁 중인 소스([소스 메타](../sources/martin2008.md))의 9장이 같은 실천을 다루는데,
**이 자리는 이 KB의 다른 소스들과 갈리지 않는다.** 더하는 것은 규율의 입자와 두 개의
기억 장치다.

- **TDD 세 법칙** — 이 소스가 TDD를 30초 주기로 조문화한다 (9장 §"The Three Laws of
  TDD", p.122):[^martin2008]

> **First Law** You may not write production code until you have written a failing unit
> test.
>
> **Second Law** You may not write more of a unit test than is sufficient to fail, and
> not compiling is failing.
>
> **Third Law** You may not write more production code than is sufficient to pass the
> currently failing test.

  - 귀결 — **이 세 법칙은 당신을 아마 30초쯤 되는 주기 안에 가둔다. 테스트와 프로덕션
    코드가 *함께* 쓰이며, 테스트가 프로덕션 코드보다 몇 초 앞선다** (9장, p.123).[^martin2008]
  - 이 KB에서 그 주기를 다루는 자리는
    [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)와
    [리팩터링의 리듬](refactoring-rhythm.md)이다. **그쪽들은 기어를 바꾸라고 하고 이
    소스는 단일 주기를 조문으로 둔다** — 강도의 차이지 명제의 충돌이 아니다.
- **테스트 코드의 지위** — **이야기의 교훈은 단순하다: 테스트 코드는 프로덕션 코드만큼
  중요하다. 그것은 이등 시민이 아니다. 그것은 생각과 설계와 돌봄을 요구한다. 그것은
  프로덕션 코드만큼 깨끗하게 유지돼야 한다** (9장 §"Keeping Tests Clean",
  p.124).[^martin2008] 그리고 반대 사례의 진단 — **더러운 테스트를 갖는 것은 테스트가
  없는 것과 같거나 더 나쁘다** (9장 §"Keeping Tests Clean", p.123).[^martin2008]
- **테스트가 변경을 가능하게 한다** — **당신의 코드를 유연하고 유지보수 가능하고 재사용
  가능하게 유지하는 것은 *단위 테스트*다. … 테스트가 변경을 가능하게 하므로 테스트가 모든
  -ility를 가능하게 한다** (9장 §"Tests Enable the -ilities", p.124).[^martin2008]
  이 페이지의 [정의와 이 장의 지위](#정의와-이-장의-지위) 절이 세운 것과 같은 명제다.
- **깨끗한 테스트의 조건이 하나로 좁혀진다** — **무엇이 깨끗한 테스트를 만드는가? 세
  가지다. 가독성, 가독성, 그리고 가독성** (9장 §"Clean Tests", p.124).[^martin2008]
  그리고 이중 기준이 명시된다 — 테스트 코드는 **여전히 단순하고 간결하고 표현력 있어야
  하지만 프로덕션 코드만큼 효율적일 필요는 없다** (9장 §"A Dual Standard",
  p.127).[^martin2008]
- **단정 하나 규칙에 대한 저자의 실제 입장** — 흔히 이 책의 주장으로 인용되는 것과 달리
  저자는 그것을 규칙이 아니라 지침으로 둔다 (9장 §"One Assert per Test",
  p.131):[^martin2008]

> I think the single assert rule is a good guideline. I usually try to create a
> domain-specific testing language that supports it, as in Listing 9-5. But I am not
> afraid to put more than one assert in a test. I think the best thing we can say is that
> the number of asserts in a test ought to be minimized.

  - 그리고 더 나은 규칙으로 옮겨 간다 — **아마 가장 좋은 규칙은 개념당 단정 수를
    최소화하고 테스트 함수당 한 개념만 테스트하라는 것이다** (9장 §"Single Concept per
    Test", p.132).[^martin2008]
- **F.I.R.S.T.** — 깨끗한 테스트의 다섯 성질 (9장 §"F.I.R.S.T.",
  pp.132–133):[^martin2008]

  | 글자 | 조문 |
  |---|---|
  | **F**ast | **테스트는 빨라야 한다. 느리게 돌면 자주 돌리고 싶지 않을 것이다** |
  | **I**ndependent | **테스트는 서로에게 의존해서는 안 된다. 한 테스트가 다음 테스트의 조건을 준비해서는 안 된다** |
  | **R**epeatable | **테스트는 어느 환경에서든 반복 가능해야 한다** — 프로덕션·QA·네트워크 없는 기차 안 노트북 |
  | **S**elf-Validating | **테스트는 불리언 출력을 가져야 한다. 통과하거나 실패하거나다. 로그 파일을 읽어 판단해서는 안 된다** |
  | **T**imely | **단위 테스트는 그것을 통과시키는 프로덕션 코드 *직전에* 쓰여야 한다** |

  - **Independent와 Repeatable이 이 페이지의
    [픽스처는 매번 새로 만든다](#픽스처는-매번-새로-만든다) 절과 같은 처방이다.**
    두 소스가 서로를 참조한 적은 없다. Fast는 17장 `T9`로 다시 나온다 — **느린 테스트는
    돌지 않는 테스트다** (17장 `T9`, p.314).[^martin2008]
- **얼마나 테스트하면 충분한가**에 대한 답도 이 페이지의 해당 절과 성격이 같다(주관적
  기준) — **테스트 스위트는 깨질 수 있는 모든 것을 테스트해야 한다** (17장 `T1`,
  p.313)[^martin2008], 그리고 커버리지 도구를 쓰라는 것(`T2`)이 유일한 계측 처방이다.
- **갈리는 자리는 없다.** 이 소스가 테스트에 대해 말하는 것은 이 KB의 fowler2018·
  percival2020 쪽과 방향이 같고, 논쟁이 걸린 것은 이 소스의 3장·4장이다.
- **다만 2차 문헌이 이 장에 유보 둘을 단다.**
  - **TDD의 빠진 0단계** — **그러나 책은 그 과정에서 빠진 0단계를 인정하지 않는다: 눈앞의
    프로그래밍 과제를 어떻게 쪼개서 30초짜리 한 입을 떼어낼 수 있게 만드느냐는 것이다.
    그것은 많은 경우 대단히 시간이 걸리고, 흔히 명백히 쓸모없으며, 흔히 불가능하다**
    (§3).[^qntm2020] 이 KB에서 같은 문제를 다루는 자리가
    [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)다.
  - **도메인 특화 테스트 언어 예제** — 이 장이 단정 다섯 줄을
    `assertEquals("HBchL", hw.getState())` 한 줄로 리팩터링해 제시하는 대목에 대해
    **나는 정확히 같은 코드를 정확히 반대 교훈을 보이는 데 쓰겠다. 이렇게 하지 마라!**
    (§2).[^qntm2020] 근거는 새 메서드 이름 `wayTooCold`가 형용사구라 무엇을 하는지
    불분명하고, 안에서 `controller.tic()`을 부르는 부수 효과를 추측할 수 없다는 것이다
    — **둘 다 같은 책 2장과 3장이 금지한 것**이라는 내적 일관성 논증이다. 전문은
    [클린 코드 비판](clean-code-criticism.md)에 있다.

## 번들링 — TDD의 대안에 이름이 붙다

두 저자의 공개 대담 셋째 주제가 TDD였고, 거기서 **TDD가 아닌 방식에 이름이 붙었다.**
이 KB에 그 이름이 없었다. 전문은
[오스터하우트–마틴 공개 대담](aposd-vs-clean-code-dialogue.md)에 있다.

- **오스터하우트가 대안을 규정한다** — 개발자가 TDD보다 다소 큰 단위, **아마 메서드 몇
  개나 클래스 하나**로 작업하며 **먼저 코드를 얼마간(수십 줄에서 수백 줄까지) 쓰고 그
  코드에 대한 단위 테스트를 쓴다.** 그리고 **TDD와 마찬가지로, 포괄적인 단위 테스트를
  갖추기 전까지 그 코드는 "동작한다"고 치지 않는다** (§"Test-Driven Development",
  JOHN 발언).[^ousterhout2024-aposd]
  - **"코드 다 짜고 나중에 테스트"와 다르다는 점을 양측이 확인한다** — 그 방식은 개발자가
    흥미를 잃어 테스트를 실제로 쓰지 않게 되므로 나쁘다는 데 **완전히 동의한다**고 적는다
    (§"Test-Driven Development", JOHN 발언).[^ousterhout2024-aposd]
- **이름은 마틴이 제안한다** (§"Test-Driven Development", UB 발언):[^ousterhout2024-aposd]

> How about if we call this technique "bundling" for purposes of this document?  This is
> the term I use in _Clean Code 2d ed._

- **그리고 마틴이 번들링의 동등성을 상당 부분 인정한다** (§"Test-Driven Development",
  UB 발언):[^ousterhout2024-aposd]

> It seems to me that working in small units, and then immediately writing after the fact
> tests, can give you all the above advantages, so long as you are very careful to test
> every aspect of the code you just wrote.  I think a disciplined programmer could
> effectively work that way.  Indeed, I think such a programmer would produce code that I
> could not distinguish from code written by another programmer following TDD.

- **갈리는 것은 설계 사고의 자리다** — 오스터하우트는 **더 큰 단위로 작업하는 이유는 설계
  사고를 북돋우기 위해서**라고 적고 (§"Test-Driven Development",
  JOHN 발언)[^ousterhout2024-aposd], 마틴은 **설계는 전략적 사고에서 오고 그것은 TDD든
  번들링이든 전술적 행동과 무관하다**고 본다 (§"Test-Driven Development",
  UB 발언).[^ousterhout2024-aposd]
- **오스터하우트가 자기 책의 오류를 인정한다** — 마틴이 *A Philosophy of Software Design*
  p.157의 TDD 서술이 부정확하다고 지적하자 (§"Test-Driven Development",
  JOHN 발언):[^ousterhout2024-aposd]

> Oops! I plead "guilty as charged" to inaccurately describing TDD. I will fix this in the
> next revision of APOSD. That said, your definition of TDD does not change my concerns.

  - **이 KB에 ousterhout2021의 TDD 서술이 반입돼 있다면 이 단서가 붙어야 한다** — 저자
    본인이 부정확하다고 인정했고 다음 개정에서 고치겠다고 밝힌 대목이다.
- **합의와 불합의가 조문화된다** (§"TDD Summary"):[^ousterhout2024-aposd] 단위 테스트가
  필수라는 것과 TDD로 좋은 설계를 낼 수 있다는 것에는 합의하고, TDD가 설계를 저해하는가와
  평균·최악의 결과가 어느 쪽이 나쁜가에서 갈린다. 그리고 **어느 쪽도 실증 데이터를 대지
  못한다** — 오스터하우트가 **그러려면 TDD의 좋고 나쁜 결과의 빈도에 대한 실증 데이터가
  필요할 텐데 나는 그런 데이터를 알지 못한다**고 적는다 (§"TDD Summary",
  JOHN 발언).[^ousterhout2024-aposd]
- **이것은 `contradicts`가 아니다.** 이 KB에 TDD를 "해야 한다"고 세운 페이지와 "하지 말라"고
  세운 페이지가 나란히 있지 않고, 양측이 실증 데이터의 부재를 함께 인정하므로 검증 가능한
  명제의 정면 충돌이 성립하지 않는다. [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md)가
  이미 같은 절충을 다루고 있다.

## 이어지는 페이지

- [클린 코드라는 말의 정의](clean-code-defined.md) — "테스트 없는 코드는 깨끗하지
  않다"와 단순 설계 규칙 1이 사는 자리
- [클린 코드 비판](clean-code-criticism.md) — 9장 예제와 TDD 0단계에 유보를 다는 2차 문헌
- [오스터하우트–마틴 공개 대담](aposd-vs-clean-code-dialogue.md) — 번들링이라는 이름이
  붙은 자리이자 TDD 쟁점의 1차 사료
- [리팩터링](refactoring.md) — 이 테스트가 담보로 잡히는 활동
- [높은 기어와 낮은 기어의 TDD](tdd-high-gear-and-low-gear.md) — 테스트를 어느 층에
  둘 것인가의 절충
- [가짜와 목](fakes-versus-mocks.md) — 테스트 대역을 무엇으로 세울 것인가
- [리팩터링의 리듬](refactoring-rhythm.md) — 테스트를 얼마나 자주 돌리는가
- [리팩터링을 가로막는 것들](obstacles-to-refactoring.md) — 테스트가 없는 레거시 코드
- [테스트가 코딩을 이끈다](test-to-code.md) — 같은 실천을 다른 소스가 다루는 자리
- [속성 기반 테스트](../concepts/property-based-testing.md) — 경계 찔러 보기를 자동화하는 쪽
- [죽은 프로그램은 거짓말하지 않는다](dead-programs-tell-no-lies.md) — 단정문의 정본
- [리팩터링과 코드 냄새](../synthesis/refactoring-and-code-smells.md) — 이 축의 허브

[^ousterhout2024-aposd]: Ousterhout & Martin 2024, "A Philosophy of Software Design
    vs Clean Code". **대담이므로 locator에 발언자를 함께 적는다** — `JOHN`은 John
    Ousterhout, `UB`는 Robert C. Martin이다. 규약과 스냅샷 취득 경로는
    `it/archive/ousterhout2024-aposd/_progress.yaml` 머리말이 정본이다.

[^qntm2020]: qntm 2020, "It's probably time to stop recommending Clean Code".
    **절 번호는 이 KB가 매긴 것이다** — 규약은
    `it/archive/qntm2020/_progress.yaml` 머리말이 정본이다.

[^fowler2018]: Fowler 2018, 4장 "Building Tests"(pp.85–100) 전체. 2장의 정의 한 줄은
    §"Refactoring and the Wider Software Development Process"(p.63)에서 왔다. 쪽은 인쇄판
    쪽 번호(PDF 쪽 − 22). 직인용에서 워터마크 문자열 `ptg26261585`를 제거했다 — 이 소스의
    표준 규약이며 근거는 `it/archive/fowler2018/_progress.yaml` 머리말에 있다. 예제는
    자바스크립트와 Mocha·Chai를 쓰며, 대표 펜스는 책의 `beforeEach` 판(p.94)을 그대로
    옮기되 책이 지면 폭 때문에 접어 놓은 줄을 폈다. 책이 반례로 든 판(바깥 스코프 상수,
    "DON'T DO THIS")은 복사해 쓸 것이 아니라 옮기지 않고 산문으로 서술했다. 4장의 UI
    화면 도판과 콘솔 출력 도판은 이미지라 옮기지 않았다.

[^martin2008]: Martin 2008, 9장 "Unit Tests"(§"The Three Laws of TDD" pp.122–123 ·
    §"Keeping Tests Clean" pp.123–124 · §"Tests Enable the -ilities" p.124 · §"Clean
    Tests" p.124 · §"A Dual Standard" p.127 · §"One Assert per Test" pp.130–131 ·
    §"Single Concept per Test" pp.131–132 · §"F.I.R.S.T." pp.132–133) · 17장 `T1`·`T2`
    (p.313) · `T9`(p.314). **논쟁 중인 소스다** — 지위와 반입 규약은
    `it/sources/martin2008.md`가 정본이다. 쪽은 인쇄판 쪽 번호이며 복원 절차는
    `it/archive/martin2008/_progress.yaml` 머리말이 정본이다. 직인용에서 문장 끝에 붙은
    각주 번호를 뗐다(`three laws:1` → `three laws:`, `good guideline.7` →
    `good guideline.`). 9장에는 Listing 9-1부터 9-8까지 여덟 리스팅이 있으나 펜스로
    옮기지 않았다 — 이 페이지의 펜스 예산은 fowler2018의 `beforeEach` 판이 쓰고 있고,
    9장 리스팅은 전부 FitNesse·환경 제어기 예제 문맥에 묶여 복사해 돌아가지 않는다.
    도판은 없다. 이 스냅샷에서 9장 p.121(장 도비라)은 본문이 비어 있어 p.122부터 읽었다.

[^percival2020]: Percival & Gregory 2020, 5장 §"Should Domain Layer Tests Move to the
    Service Layer?"와 곁글 "Recap: Rules of Thumb for Different Types of Test" ·
    6장 §"Tidying Up the Integration Tests". **이 소스의 locator는 장 단위다** — 검증
    절차와 근거는 `it/archive/percival2020/_progress.yaml` 머리말이 정본이다. 이 절에는
    코드 펜스를 두지 않았다.

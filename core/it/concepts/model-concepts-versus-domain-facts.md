---
type: concept
title: 모델의 개념과 도메인의 사실
description: 코드의 이름이 담아야 하는 것이 어디까지인가를 원전 근거로 긋는 페이지 — 모델이 선택적 단순화이며 사실을 수백 개 버린 결과라는 규정, 조직된 데이터와 모델을 가르는 선, 이름 규약으로 개별 사실을 알아보던 스크립트가 개념을 명시한 모델로 바뀌면서 그 유추가 한 자리로 격리된 사례, 숨은 규칙을 개념으로 승격시킬 때 수치는 어디에 남는가, 무엇이 아니라 무엇으로가 이름에 온다는 조항, 값 객체가 "무엇인지"만 담고 "어느 것인지"는 담지 않는다는 규정, 그리고 이 소스가 말하는 것과 말하지 않는 것의 경계
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 모델의 개념과 도메인의 사실

- [모델은 사실을 버린 것이다](#모델은-사실을-버린-것이다)
- [조직된 데이터와 모델을 가르는 선](#조직된-데이터와-모델을-가르는-선)
- [이름 규약이 개별 사실을 나르던 사례](#이름-규약이-개별-사실을-나르던-사례)
- [숨은 규칙을 개념으로 올릴 때 수치는 어디에 남는가](#숨은-규칙을-개념으로-올릴-때-수치는-어디에-남는가)
- [이름에 오는 것은 무엇이 아니라 무엇으로다](#이름에-오는-것은-무엇이-아니라-무엇으로다)
- [무엇인지와 어느 것인지](#무엇인지와-어느-것인지)
- [이 소스가 말하는 것과 말하지 않는 것](#이-소스가-말하는-것과-말하지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **코드의 이름은 도메인의 무엇을 담고, 무엇은 담지 않는가.**

## 모델은 사실을 버린 것이다

- 모델의 규정이 1부 도입에 있다 — **모델은 단순화다. 그것은 당면 문제를 푸는 데 관련 있는
  측면을 추상하고 관계없는 세부를 무시하는, 현실에 대한 하나의 해석이다** (1부 도입,
  p.2).[^evans2003]
- 그리고 지식의 형태로 다시 규정된다 — **모델은 선택적으로 단순화되고 의식적으로 구조화된
  지식의 형태다. 알맞은 모델은 정보를 뜻이 통하게 만들고 그것을 문제에 집중시킨다** (1부
  도입, p.3).[^evans2003]
- 도메인 모델(domain model)이 무엇이 아닌지도 함께 적힌다 — **도메인 모델은 특정 다이어그램이
  아니다; 그것은 그 다이어그램이 전달하려는 발상이다. 그것은 도메인 전문가의 머릿속에 있는
  지식 그 자체가 아니다; 그것은 그 지식의 엄밀하게 조직되고 선별된 추상이다** (1부 도입,
  p.3).[^evans2003]
- **이 페이지의 출발점이 되는 문장은 저자가 자기 사례를 회고하는 자리에 있다.** 인쇄 회로
  기판 프로젝트의 모델이 무엇을 담고 무엇을 버렸는지를 이렇게 적는다 (1장,
  p.12):[^evans2003]

> It consolidated many synonyms and slight variations in descriptions. It excluded hundreds of
> facts that the engineers understood but that were not directly relevant, such as the actual
> digital features of the components.

  - 모델이 한 일이 두 가지로 나뉜다. **동의어와 변형을 하나로 합친 것**은 개념을 정한 일이고,
    **수백 개의 사실을 배제한 것**은 그 개념 밖의 것을 내보낸 일이다. 버려진 것이 거짓이어서
    버려진 것이 아니다 — 엔지니어들이 알고 있던 참인 사실이고, 관련 없어서 배제됐다.

## 조직된 데이터와 모델을 가르는 선

- 절차형 언어의 복합 자료형에 대한 판정이 이 선을 가장 짧게 긋는다 (3장, p.51):[^evans2003]

> Procedural languages often support complex data types that begin to correspond to more
> natural conceptions of the domain, but these complex types are only organized data, and they
> don't capture the active aspects of the domain.

- 같은 구분이 지식 정련의 성공 요건 목록에도 나온다 — **지식이 풍부한 모델을 개발하는 것.
  객체는 행동을 가졌고 규칙을 강제했다. 그 모델은 그저 데이터 스키마가 아니었다; 그것은 복잡한
  문제를 푸는 데 필수적이었다** (1장, pp.12–13).[^evans2003]
- 그리고 모델이 무너질 때 무엇이 되는지가 실물로 적힌다. 모델러가 구현에서 분리된 프로젝트에서
  모델은 **한낱 자료 구조로 격하됐다**(reduced to a mere data structure) (3장,
  p.60).[^evans2003] 3장 첫머리의 두 실패담도 같은 진단을 받는다 — 두 프로젝트 모두 객체
  패러다임을 **"멋진 자료 구조"로 말고는** 활용하지 못했다 (3장, p.46).[^evans2003]
- **세 자리가 같은 선을 긋는다**: 모델은 개념과 규칙과 행동을 담고, 데이터는 값을 담는다.
  이 소스에서 "그저 자료 구조"는 언제나 실패의 이름이다.

## 이름 규약이 개별 사실을 나르던 사례

- 3장의 인쇄 회로 기판 사례가 이 페이지에서 가장 직접적인 증거다. 도구에 **버스**(bus)라는
  개념이 없어서, 엔지니어들은 **넷에 대해 이름 규약(naming convention)을 조심스럽게 써서
  데이터 파일을 알파벳순으로 정렬하면 한 버스의 넷들이 정렬된 파일에서 함께 놓이게 했다**
  (3장, p.53).[^evans2003] 즉 **어느 넷이 어느 버스에 속하는가**라는 도메인 사실이 이름의
  글자 안에 실려 있었다.
- 저자의 판정 (3장, p.54):[^evans2003]

> What the script writers were trying to do was to supplement the tool's domain model with the
> concept of "bus." Their implementation infers the bus's existence through sorts and string
> matches, but it does not explicitly deal with the concept.

- 모델 주도 판에서 그 유추가 사라지지 않는다는 것이 중요하다. **한 자리로 격리된다** —
  `Inferred Bus Factory`라는 유틸리티 하나가 **"넷의 컬렉션이 주어지면 이름 규약을 써서 버스를
  유추하고 인스턴스를 만든다"**는 책임을 맡는다 (3장, p.56).[^evans2003] 이름 규약은 여전히
  거기 있지만 이제 **경계에서 한 번 읽히는 입력**이지 도메인 로직이 매번 의존하는 것이 아니다.
- **그리고 저자가 그 격리를 코드 주석으로 못 박는다.** 단위 테스트에서 `Bus`를 이름 없이
  조립하고, 그 이유를 두 줄로 적어 둔다 (3장, p.56):[^evans2003]

  ```java
  public void testBusRuleAssignment() {
        Net a0 = new Net("a0");
        Net a1 = new Net("a1");
        Bus a = new Bus("a");        //Bus is not conceptually dependent
        a.addNet(a0);                //on name-based recognition, and so
        a.addNet(a1);                //its tests should not be either.

        NetRule minWidth4 = NetRule.create(MIN_WIDTH, 4);
        a.assignRule(minWidth4);

        assertTrue(a0.assignedRules().contains(minWidth4));
        assertEquals(minWidth4, a0.getRule(MIN_WIDTH));
        assertEquals(minWidth4, a1.getRule(MIN_WIDTH));
  }
  ```

  - **개념은 이름으로 알아보는 것에 개념적으로 의존하지 않는다**는 것이 저자가 직접 쓴 문장이고,
    이 페이지의 물음에 이 소스가 내놓는 가장 명시적인 답이다. `Bus`라는 **개념**은 클래스로
    존재하고, `a0`이 버스 `a`에 속한다는 **사실**은 `a.addNet(a0)`이라는 데이터 조립으로
    표현된다. 이름 문자열은 그 조립의 재료가 아니다.

## 숨은 규칙을 개념으로 올릴 때 수치는 어디에 남는가

- 1장의 초과 예약 사례가 이 경계를 반대편에서 비춘다. 요구사항 문서에 **10% 초과 예약을
  허용한다**는 한 줄이 있고, 그것이 애플리케이션 메서드 안의 가드 절로 구현돼 있다. 저자의
  진단 — **이제 중요한 업무 규칙 하나가 애플리케이션 메서드의 가드 절로 숨겨져 있다** (1장,
  p.18).[^evans2003] 그 대가가 둘로 적힌다 (1장, p.18):[^evans2003]
  - **쓰인 대로라면 어떤 업무 전문가도 개발자의 안내를 받더라도 이 코드를 읽고 규칙을 확인할
    가능성이 낮다.**
  - **기술적인 비업무 인력이 요구사항 텍스트와 코드를 연결하기도 어려울 것이다.**
- 처방은 **개념에 이름을 주는 것**이다 — **초과 예약 규칙은 정책(policy)이다. 정책은 전략
  (STRATEGY)이라 알려진 디자인 패턴의 다른 이름이다** (1장, pp.18–19).[^evans2003] 그래서
  `Overbooking Policy` 클래스가 생기고 호출부는 `overbookingPolicy.isAllowed(cargo, voyage)`
  한 줄이 된다 (1장, p.19).[^evans2003]
- **그런데 수치는 그대로 남는다.** 새 `Overbooking Policy` 클래스의 메서드 안에 `1.1`이 여전히
  리터럴로 들어 있고, 저자는 그것을 문제 삼지 않는다 (1장, p.19).[^evans2003] 저자가 열거하는
  이득 목록도 수치의 위치가 아니라 **개념의 가시성**에 대한 것이다 — **이 설계 단계에 이르기
  위해 프로그래머와 관련된 모든 사람이 초과 예약을 그저 모호한 계산이 아니라 별개의 중요한
  업무 규칙으로 이해하게 되었을 것이다** (1장, pp.19–20).[^evans2003]
  - **이 소스의 요구가 어디서 멈추는지를 보여 주는 자리다.** 이 소스가 밀어붙이는 것은
    **규칙에 이름을 주는 것**까지이고, 그 규칙의 **매개변수를 코드 밖으로 빼는 것**은 이
    소스의 관심사가 아니다. 그 물음을 다루는 자리는
    [외부 설정](../concepts/external-configuration.md)이다.

## 이름에 오는 것은 무엇이 아니라 무엇으로다

- 10장의 조항이 이름의 내용물을 규정한다 — **어떤 개념을 클래스나 메서드의 형태로 명시적으로
  모델링한 값을 얻으려면, 우리는 그 프로그램 요소에 그 개념을 반영하는 이름을 주어야 한다**
  (10장, p.246).[^evans2003]
- 처방 문단 (10장, p.247):[^evans2003]

> Name classes and operations to describe their effect and purpose, without reference to the
> means by which they do what they promise. This relieves the client developer of the need to
> understand the internals. These names should conform to the UBIQUITOUS LANGUAGE so that team
> members can quickly infer their meaning.

- **여기서 이름의 정본이 유비쿼터스 언어로 못 박힌다.** 그리고 그 언어의 어휘가 무엇으로
  이루어지는지가 2장에 이미 규정돼 있다 — **그 유비쿼터스 언어의 어휘는 클래스와 두드러진
  연산의 이름을 포함한다** (2장, p.25).[^evans2003] 즉 이 소스가 이름에 담으라고 요구하는
  것은 **모델의 요소**이고, 모델은 위에서 본 대로 사실을 버리고 남은 개념이다.
- 무엇을 이름에서 빼야 하는지도 같은 조항이 정한다 — **공개 인터페이스에서는 관계와 규칙을
  진술하되 그것이 어떻게 강제되는지는 말하지 마라; 사건과 행동을 서술하되 그것이 어떻게
  수행되는지는 말하지 마라; 방정식을 세우되 그것을 푸는 수치 해법은 말하지 마라** (10장,
  p.247).[^evans2003]
  - 전문은 [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)에 있다.

## 무엇인지와 어느 것인지

- 도메인 객체를 두 종류로 가르는 자리에서 같은 선이 다시 나온다. 값 객체(value object)의
  규정 — **개념적 정체성이 없이 도메인의 서술적 측면을 표상하는 객체를 값 객체라 부른다**
  (5장, p.98).[^evans2003] 그리고 그 존재 이유가 이렇게 적힌다 (5장, p.98):[^evans2003]

> VALUE OBJECTS are instantiated to represent elements of the design that we care about only
> for what they are, not who or which they are.

- 반대쪽 엔티티(entity)의 조항은 **정체성을 정의의 일차 요소로 삼으라**는 것이다 — **객체가
  속성이 아니라 그 정체성으로 구별될 때, 모델에서 그것을 정의의 일차 요소로 삼아라. 클래스
  정의를 단순하게, 생애 주기의 연속성과 정체성에 집중해 유지하라** (5장, p.92).[^evans2003]
- **"무엇인지"는 타입이 담고 "어느 것인지"는 인스턴스가 담는다.** 이 소스는 이 구분을 이름
  짓기 규칙으로 말하지 않고 객체 분류 규칙으로 말하지만, 두 진술은 같은 선의 양면이다 —
  타입 이름은 무엇인지를 답하는 자리이고, 어느 것인지는 값과 정체성이 답한다.
  - 이 KB에서 그 구분이 파이썬 실물로 내려온 자리가
    [값 객체와 엔티티](value-objects-and-entities.md)다.

## 이 소스가 말하는 것과 말하지 않는 것

이 페이지의 물음에는 이 소스가 직접 답한 부분과 답하지 않은 부분이 있다. 섞으면 안 된다.

- **이 소스가 직접 말하는 것.**
  - 모델은 사실을 버리고 남은 개념의 구조다 (1부 도입 p.2·p.3, 1장 p.12).[^evans2003]
  - 이름은 유비쿼터스 언어를 따라야 하고, 그 언어의 어휘는 클래스와 연산의 이름, 즉 모델의
    요소다 (2장 p.25, 10장 p.247).[^evans2003]
  - 이름은 목적과 효과를 서술하고 수단은 서술하지 않는다 (10장 p.247).[^evans2003]
  - 개념은 이름으로 알아보는 것에 개념적으로 의존해서는 안 된다 (3장 p.56).[^evans2003]
  - 이름 규약으로 개별 사실을 유추하는 코드는 경계의 팩토리 한 자리로 격리된다 (3장
    p.56).[^evans2003]
- **이 소스가 말하지 않는 것.**
  - "도메인 사실을 변수 이름에 넣지 마라"는 금지 조항은 이 책 어디에도 없다. 이 소스의 요구는
    **도메인 용어를 이름에 쓰라**는 쪽이고, 그 반대 방향의 금지는 위 두 자리(버스 테스트
    주석, 값 객체 규정)에서 **간접적으로만** 따라 나온다.
  - 규칙의 매개변수를 코드 밖으로 빼라는 요구도 없다. 초과 예약 사례에서 `1.1`은 개념이 이름을
    얻은 뒤에도 클래스 안에 그대로 남는다 (1장 p.19).[^evans2003]
- **#hypothesis 두 요구는 방향이 반대가 아니라 층이 다르다.** 이 소스는 **타입과 연산의 이름**을
  다루고, "사실을 이름에 박지 마라"는 요구는 대개 **변수·상수·모듈의 이름**을 다룬다. 이
  소스가 유비쿼터스 언어를 규정하며 든 어휘 목록에 변수 이름이 없다는 것이 그 층위 차이의
  근거다 (2장 p.25).[^evans2003] 이 소스가 이 구분을 명시적으로 진술한 자리는 없다.

## 이어지는 페이지

- [유비쿼터스 언어](ubiquitous-language.md) — 이름의 정본이 되는 언어
- [모델 주도 설계](model-driven-design.md) — 이 선이 코드 구조로 나타나는 자리
- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 이름이 수단을 말하지
  않는다는 조항의 전문
- [값 객체와 엔티티](value-objects-and-entities.md) — "무엇인지"와 "어느 것인지"의 파이썬 실물
- [지식 정련](../concepts/knowledge-crunching.md) — 사실을 버리는 활동
- [이름 짓기](naming-things.md) — 코드의 이름을 다루는 이 KB의 자리
- [외부 설정](../concepts/external-configuration.md) — 값을 코드 밖으로 빼는 물음을 다루는 자리
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — 인터페이스가 무엇을 드러내지
  않아야 하는가를 다른 축에서 다루는 자리
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 1부 도입(pp.2–3) · 1장 "Crunching Knowledge"(§Ingredients of
    Effective Modeling p.12 · §Knowledge-Rich Design pp.17–20) · 2장(p.25) ·
    3장(§Modeling Paradigms and Tool Support pp.51–57 · §HANDS-ON MODELERS p.60) ·
    5장(§ENTITIES p.92 · §VALUE OBJECTS p.98) · 10장(§INTENTION-REVEALING INTERFACES
    pp.246–247). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로
    조판하는 관례를 직인용에서 유지했다. 펜스의 Java 테스트는 p.56 원문 그대로이며 —
    주석의 줄바꿈 위치까지 원문 조판을 따랐다 — 원문이 문자열에 쓴 굽은 따옴표를 곧은
    따옴표로 바꾼 것만 다르다(Java 문법상 굽은 따옴표는 컴파일되지 않는다). 이 코드는
    **2003년 Java의 관용**이라 JUnit 3 스타일(`public void test…`)을 쓴다. 초과 예약
    사례의 코드 세 판(pp.17–19)은 같은 메서드의 전후 대비 쌍이라 펜스로 옮기지 않고 산문으로
    서술했다 — 이 페이지의 펜스 예산은 버스 테스트가 쓰고 있다.

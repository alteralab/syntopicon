---
type: concept
title: 명시적 제약
description: 제약을 객체나 메서드로 올려 이름을 주는 처방의 원전 — 제약이 암묵적으로 나타난다는 관찰과 양동이 불변식으로 보인 최소 사례, 같은 규칙을 이름 붙은 메서드로 뽑아내면 모델과의 관계가 드러나고 규칙이 자랄 방을 얻는다는 논증, 제약이 자기가 붙은 객체의 설계를 일그러뜨리고 있다는 경고 신호 셋, 그리고 제약이 도메인에서는 두드러지는데 모델에서는 두드러지지 않을 때 별도 객체로 분리하라는 조항과 초과 예약 정책이 그 실물인 이유
generated: { by: "claude-opus-5", at: "2026-09-14T05:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 명시적 제약

- [제약은 암묵적으로 나타난다](#제약은-암묵적으로-나타난다)
- [이름 붙은 메서드로 뽑아내면 무엇이 달라지는가](#이름-붙은-메서드로-뽑아내면-무엇이-달라지는가)
- [제약이 객체를 일그러뜨린다는 경고 신호 셋](#제약이-객체를-일그러뜨린다는-경고-신호-셋)
- [조항](#조항)
- [초과 예약 정책이 그 실물이다](#초과-예약-정책이-그-실물이다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **업무 규칙으로서의 제약을 코드의 어느 자리에 두어야 그것이 보이는가.**

## 제약은 암묵적으로 나타난다

- 이 장은 객체 지향이 잘 떠올리게 하지 않는 개념 범주 둘을 다루고, 제약(constraint)이 그
  첫째다 — **제약은 모델 개념의 특히 중요한 범주를 이룬다. 그것들은 흔히 암묵적으로
  나타나며, 그것을 명시적으로 표현하면 설계를 크게 개선할 수 있다** (9장,
  p.220).[^evans2003]
- 제약이 객체나 메서드 안에 자연스러운 거처를 얻을 때도 있다. 저자가 드는 최소 사례가
  양동이다 — **`Bucket` 객체는 자기 용량보다 많이 담지 않는다는 불변식(invariant)을
  보장해야 한다** (9장, p.220).[^evans2003] 담는 연산마다 조건 로직을 두면 그 불변식은
  강제된다.
- 그러나 그 강제가 곧 표현은 아니다 — **이 로직은 너무 단순해서 규칙이 자명하다. 그러나 이
  제약이 더 복잡한 클래스 안에서 사라져 버리는 것은 쉽게 상상할 수 있다** (9장,
  p.220).[^evans2003]

## 이름 붙은 메서드로 뽑아내면 무엇이 달라지는가

- 같은 규칙을 별도 메서드로 뽑아내고 **제약의 의의를 명확하고 명시적으로 표현하는 이름**을
  준다 (9장, p.220).[^evans2003] 그 결과가 아래 코드이고, 조건 로직을 담는 자리가
  `constrainedToCapacity`라는 이름을 얻는다 (9장, p.221):[^evans2003]

  ```java
  class Bucket {
      private float capacity;
      private float contents;

      public void pourIn(float addedVolume) {
          float volumePresent = contents + addedVolume;
          contents = constrainedToCapacity(volumePresent);
      }

      private float constrainedToCapacity(float volumePlacedIn) {
          if (volumePlacedIn > capacity) return capacity;
          return volumePlacedIn;
      }
  }
  ```

- 무엇이 달라졌는지가 명시된다 — **이 코드의 두 판본 모두 제약을 강제하지만, 둘째 판은 모델과
  더 뻔한 관계를 갖는다(모델 주도 설계의 기본 요구)** (9장, p.221).[^evans2003]
- 이득 셋이 이어서 적힌다 (9장, p.221):[^evans2003]
  - **제약을 자기 메서드로 뽑아내면 우리가 그것에 의도를 드러내는 이름을 주어 설계에서 제약을
    명시적으로 만들 수 있다. 그것은 이제 우리가 논의할 수 있는 이름 붙은 사물이다.**
  - **이 접근은 또한 제약에 방을 준다.** 이보다 복잡한 규칙이라면 자기를 부르는 쪽보다 긴
    메서드를 쉽게 낳을 수 있다.
  - **이런 식이면 부르는 쪽은 단순하고 자기 과제에 집중한 채로 남고, 제약은 필요하면 복잡도를
    키울 수 있다.**
  - 이름이 의도를 드러내야 한다는 조항의 전문은
    [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md)에 있다.
- 이 처방이 왜 일반적인지도 같은 자리에서 규정된다 — 규칙이 복잡해지면 **그 규칙은 다른 모든
  암묵적 개념이 그러듯 자기가 적용되는 객체나 연산을 압도하기 시작한다** (9장,
  p.221).[^evans2003] 즉 제약은 암묵적 개념의 한 종류이고, 처방도 같다.

## 제약이 객체를 일그러뜨린다는 경고 신호 셋

- 메서드 하나로는 안 되는 경우가 있다 — **이 별도 메서드는 제약에 자랄 방을 조금 주지만, 제약이
  메서드 하나에 편안히 들어가지 못하는 경우가 많다. 또는 메서드가 단순하게 남더라도 그 객체가
  자기 주된 책임을 위해서는 필요로 하지 않는 정보를 부를 수 있다. 그 규칙은 그저 기존 객체
  안에 좋은 거처가 없을 수 있다** (9장, p.221).[^evans2003]
- 그 상태를 알아보는 신호 셋이 목록으로 주어진다 (9장, p.221):[^evans2003]

> 1. Evaluating a constraint requires data that does not otherwise fit the object's definition.
> 2. Related rules appear in multiple objects, forcing duplication or inheritance between objects
>    that are not otherwise a family.
> 3. A lot of design and requirements conversation revolves around the constraints, but in the
>    implementation, they are hidden away in procedural code.

  - **셋째가 이 장 전체의 진단과 같은 형태다.** 대화에서는 두드러지는데 구현에서는 숨어 있다는
    것이 암묵적 개념을 찾아내는 일반 신호이고, 그 절차는
    [암묵적 개념 파내기](digging-out-implicit-concepts.md)가 다룬다.

## 조항

- 판정과 처방이 한 문장에 있다 (9장, p.222):[^evans2003]

> When the constraints are obscuring the object's basic responsibility, or when the constraint is
> prominent in the domain yet not prominent in the model, you can factor it out into an explicit
> object or even model it as a set of objects and relationships.

- **판정 기준이 둘이다.** 하나는 객체 쪽 사정(기본 책임이 가려지는가)이고, 다른 하나는 모델과
  도메인의 불일치(도메인에서 두드러지는데 모델에서 두드러지지 않는가)다. 뒤쪽 기준이 이 소스
  특유의 것이며, 이름이 무엇을 담아야 하는가를 다루는 자리는
  [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md)이다.
- 저자가 더 읽을 곳으로 대는 것은 Warmer와 Kleppe의 객체 제약 언어(Object Constraint
  Language) 책이며, 그것을 **이 주제에 대한 깊이 있고 준형식적인 취급 하나**로 소개한다 (9장,
  p.222).[^evans2003]

## 초과 예약 정책이 그 실물이다

- 저자는 여기서 1장 사례를 되부른다. 화물 운송업의 흔한 관행인 10% 초과 예약이고, **경험이
  운송 회사들에 이 초과 예약이 막바지 취소를 벌충해 배가 거의 가득 차서 출항하게 한다는 것을
  가르쳤다** (9장, p.222).[^evans2003]
- 그 제약이 어디에 걸려 있었는지가 명시된다 — **`Voyage`와 `Cargo` 사이 연관에 대한 이 제약은,
  제약을 표상하는 새 클래스를 더함으로써 다이어그램에서도 코드에서도 명시적으로 만들어졌다**
  (9장, p.222).[^evans2003]
  - 즉 초과 예약 정책은 **객체 하나가 아니라 두 객체 사이의 연관에 걸린 규칙**이었고, 그래서
    어느 쪽 클래스에도 거처가 없었다. 위 경고 신호 첫째와 둘째가 동시에 성립하는 자리다.
- 이 KB에서 그 사례의 코드와 논증을 다루는 자리는
  [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md)이고, 같은
  사례를 지식 정련의 산물로 읽는 자리는 [지식 정련](../concepts/knowledge-crunching.md)이다.

## 이어지는 페이지

- [명세 패턴](specification-pattern.md) — 제약을 객체로 올리는 이 범주의 좁고 흔한 한 경우.
  술어 같은 값 객체가 그 형태다
- [도메인 객체가 된 프로세스](processes-as-domain-objects.md) — 같은 장이 다루는 나머지 범주
- [암묵적 개념 파내기](digging-out-implicit-concepts.md) — 이런 제약을 찾아내는 앞 단계
- [모델의 개념과 도메인의 사실](../concepts/model-concepts-versus-domain-facts.md) — 초과 예약
  사례의 코드와 그 한계
- [의도를 드러내는 인터페이스](../concepts/intention-revealing-interfaces.md) — 뽑아낸 메서드에
  주는 이름이 따라야 할 조항
- [애그리게이트와 일관성 경계](../concepts/aggregates-and-consistency-boundaries.md) — 제약과
  불변식을 가르는 낱말 구분이 있는 자리
- [계약에 의한 설계](../concepts/design-by-contract.md) — 같은 규칙을 선행 조건과 불변식으로
  적는 다른 축
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 소스의 허브

[^evans2003]: Evans 2003, 9장 "Making Implicit Concepts Explicit" §"How to Model Less Obvious
    Kinds of Concepts" 도입(p.219) · §"Explicit Constraints"(pp.220–222) · 예제 "Review:
    Overbooking Policy"(p.222). 쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을
    작은 대문자로 조판하는 관례를 직인용에서 유지했다. 펜스의 Java 코드는 p.221 원문이며,
    추출본에서 눌린 줄바꿈과 들여쓰기를 표준 Java 조판으로 되돌린 것 말고 보탠 줄은 없다.
    같은 절의 첫 판 `pourIn`(p.220)은 같은 메서드의 전후 대비 쌍이라 펜스로 옮기지 않고
    산문으로 서술했다. 클래스 다이어그램(Figure 9.10·9.11)은 도판이라 제약 표기와 클래스
    이름만 옮겼다. 저자가 대는 참고 문헌은 Warmer and Kleppe 1999다.

---
type: concept
title: 값 객체 설계
description: 정체성이 없다는 사실이 열어 주는 설계 자유를 무엇에 쓰는가 — 복사와 공유와 불변성이라는 세 선택, 안전하게 공유하려면 불변이어야 한다는 조건과 인자로 넘길 때 생기는 같은 문제, 값 객체가 수가 많아서 성능 조율의 여지가 중요하다는 셈과 전기 콘센트 플라이웨이트, 복사와 공유의 경제가 구현 환경에 달렸다는 판정과 공유를 제한할 세 경우, 가변을 허용할 네 요인과 가변이면 공유하지 말라는 단서, 언어가 강제해 주지 않아도 구분이 쓸모 있다는 논증, 관계형·분산 저장에서 복사가 정규화를 이기는 자리, 그리고 불필요한 제약을 두지 않는 것이 일반 규칙이라는 결론
generated: { by: "claude-opus-5", at: "2026-09-14T09:00:00Z" }
status: draft
sources:
  - { id: evans2003, resource: /it/sources/evans2003.md }
---

# 값 객체 설계

- [정체성이 없다는 것이 주는 자유](#정체성이-없다는-것이-주는-자유)
- [공유하려면 불변이어야 한다](#공유하려면-불변이어야-한다)
- [인자로 넘길 때도 같은 문제가 생긴다](#인자로-넘길-때도-같은-문제가-생긴다)
- [값 객체는 수가 많다](#값-객체는-수가-많다)
- [복사와 공유의 경제](#복사와-공유의-경제)
- [가변을 허용하는 네 요인](#가변을-허용하는-네-요인)
- [언어가 강제하지 않아도 구분은 쓸모 있다](#언어가-강제하지-않아도-구분은-쓸모-있다)
- [데이터베이스 조율 — 복사가 정규화를 이기는 자리](#데이터베이스-조율--복사가-정규화를-이기는-자리)
- [일반 규칙 — 불필요한 제약을 두지 않는다](#일반-규칙--불필요한-제약을-두지-않는다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **어떤 객체를 값 객체(value object)로 분류하고 나면, 그 분류가 어떤 구현
선택을 열어 주고 그 선택의 조건은 무엇인가.**

분류 자체는 [값 객체와 엔티티](value-objects-and-entities.md)가 다룬다. 이 페이지는 그
분류가 끝난 다음의 설계다.

## 정체성이 없다는 것이 주는 자유

- 절이 자유의 목록으로 시작한다 (5장 §"Designing VALUE OBJECTS", p.99):[^evans2003]

> We don't care which instance we have of a VALUE OBJECT. This lack of constraints gives us
> design freedom we can use to simplify the design or optimize performance. This involves
> making choices about copying, sharing, and immutability.

  - **셋이 한 묶음이다.** 복사(copying)·공유(sharing)·불변성(immutability)은 따로 고를 수
    있는 것이 아니라 서로를 조건 짓는다. 아래 절들이 그 조건을 하나씩 푼다.

## 공유하려면 불변이어야 한다

- 이름(Name) 객체 예제가 조건을 유도한다 (5장, p.100):[^evans2003]
  - 두 사람의 이름이 같다고 해서 **그들이 같은 사람이 되거나 서로 교체 가능해지는 것은
    아니다. 그러나 이름을 표상하는 객체는 교체 가능하다. 철자만이 중요하기 때문이다.**
  - 그래서 `Name` 객체를 한 `Person`에서 다른 `Person`으로 **복사**할 수 있다. 더 나아가
    두 `Person`이 **같은 `Name` 인스턴스를 공유**해도 행동이나 정체성이 달라지지 않는다.
  - **그런데 한쪽 사람의 이름이 바뀌는 순간 다른 쪽 사람의 이름도 바뀐다.**
- 그 실패에서 조건이 나온다 (5장, p.100):[^evans2003]

> To protect against this, in order for an object to be shared safely, it must be immutable:
> it cannot be changed except by full replacement.

  - **불변의 정의가 "전체 교체 말고는 바뀌지 않는다"로 주어진다는 점이 중요하다.** 부분
    수정을 막는 것이지 새 값을 못 만든다는 뜻이 아니다.
  - 파이썬에서 이 조건이 `@dataclass(frozen=True)`와 네임드튜플로 실현되는 자리, 그리고
    `frozen`이 진짜 불변은 아니라는 단서는
    [값 객체와 엔티티](value-objects-and-entities.md)에 있다.

## 인자로 넘길 때도 같은 문제가 생긴다

- 공유만이 아니다 (5장, p.100):[^evans2003]
  - **객체가 자기 속성 하나를 인자나 반환값으로 다른 객체에 넘길 때 같은 문제가 생긴다.
    떠돌아다니는 객체가 소유자의 통제를 벗어나 있는 동안 무슨 일이든 일어날 수 있다.**
  - 피해가 소유자에게 간다 — **값이 소유자의 불변식(invariant)을 위반하는 방식으로 바뀌어
    소유자를 오염시킬 수 있다.**
  - **이 문제는 넘기는 객체를 불변으로 만들거나 복사본을 넘기는 것으로 회피된다.**
- **이 진단이 [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md)의 "내부 자료
  구조를 반환하지 마라"와 같은 사고를 다른 어휘로 말한다.** 그쪽은 캡슐화가 깨지는 쪽을
  보고, 이쪽은 불변식이 깨지는 쪽을 본다. 처방이 겹친다 — 복사본을 주거나 불변인 것을 준다.

## 값 객체는 수가 많다

- 성능 조율의 여지가 중요한 이유가 개수에 있다 — **값 객체는 수가 많은 경향이 있으므로
  성능 조율을 위한 추가 선택지를 만들어 두는 것이 중요할 수 있다** (5장, p.100).[^evans2003]
- 주택 설계 소프트웨어의 전기 콘센트가 실물이다 (5장, p.100):[^evans2003]
  - 콘센트마다 별개의 값 객체를 두면 **집 도면 한 판본에 백 개가 있을 수 있다.**
  - **그러나 모든 콘센트가 교체 가능하다고 보면, 콘센트 인스턴스 하나만 공유하고 그것을 백
    번 가리킬 수 있다** — 저자가 이것을 플라이웨이트(FLYWEIGHT)의 사례로 지목한다.
  - **큰 시스템에서는 이런 효과가 수천 배로 곱해지고, 그런 최적화가 쓸 만한 시스템과
    수백만 개의 중복 객체에 질식해 기어가는 시스템의 차이를 만들 수 있다.**
- 그리고 그것이 분류의 배당금이라고 못 박는다 — **이것은 엔티티에는 쓸 수 없는 최적화
  요령의 한 예일 뿐이다** (5장, p.100).[^evans2003]

## 복사와 공유의 경제

- 어느 쪽이 이득인지가 고정돼 있지 않다 (5장, p.100):[^evans2003]

> The economy of copying versus sharing depends on the implementation environment. Although
> copies may clog the system with huge numbers of objects, sharing can slow down a distributed
> system. When a copy is passed between two machines, a single message is sent and the copy
> lives independently on the receiving machine. But if a single instance is being shared, only
> a reference is passed, requiring a message back to the object for each interaction.

- 그래서 공유는 좁은 경우로 제한된다 — **공유는 그것이 가장 값지고 가장 문제를 덜 일으키는
  경우로 제한하는 것이 가장 좋다** (5장, p.101):[^evans2003]
  - **데이터베이스에서 공간이나 객체 수를 아끼는 것이 결정적일 때**
  - **통신 부담이 낮을 때(예컨대 중앙 집중 서버에서)**
  - **공유되는 객체가 엄격하게 불변일 때**
- 불변이 관리 비용까지 없앤다 — **값 객체가 불변인 한 변경 관리는 단순하다 — 전체 교체 말고는
  변경이 없다. 불변 객체는 자유롭게 공유될 수 있다. 가비지 컬렉션이 믿을 만하다면 삭제는
  그 객체에 대한 모든 참조를 떨구는 문제일 뿐이다** (5장, p.101).[^evans2003]
- 그리고 그 선언이 개발자에게 주는 것이 무엇인지가 명시된다 — **값 객체가 설계에서 불변으로
  지정되면, 개발자는 애플리케이션이 특정 인스턴스에 의존하지 않는다는 것을 확신한 채 복사와
  공유 같은 사안을 순전히 기술적 근거로 결정할 자유를 얻는다** (5장, p.101).[^evans2003]

## 가변을 허용하는 네 요인

곁글 "Special Cases: When to Allow Mutability"가 예외를 정한다. **불변성이 기본값이고
가변은 성능 사유의 예외**라는 구조다.

- 기본값의 근거가 둘이다 — **불변성은 구현에서 큰 단순화 장치이며, 공유와 참조 전달을 안전하게
  만든다. 그것은 또한 값의 의미와도 일관된다. 속성의 값이 바뀌면 기존 것을 수정하는 대신
  다른 값 객체를 쓴다** (5장, p.101, 곁글).[^evans2003]
- 그럼에도 **성능 고려가 값 객체를 가변으로 두는 쪽에 무게를 실을 때가 있다.** 가변 구현에
  유리하게 작용하는 요인 넷이다 (5장, p.101, 곁글):[^evans2003]
  - **값이 자주 바뀐다면**
  - **객체 생성이나 삭제가 비싸다면**
  - **수정이 아니라 교체가 클러스터링을 흐트러뜨린다면**(아래 데이터베이스 조율 예제가
    그 클러스터링이다)
  - **값의 공유가 별로 없거나, 클러스터링 개선이나 다른 기술적 이유로 그 공유를 포기한
    경우라면**
- **그리고 단서가 대문자로 붙는다** (5장, p.101, 곁글):[^evans2003]

> Just to reiterate: If a VALUE's implementation is to be mutable, then it *must not* be
> shared. Whether you will be sharing or not, design VALUE OBJECTS as immutable when you can.

## 언어가 강제하지 않아도 구분은 쓸모 있다

- 불변성 선언은 언어에 따라 있기도 없기도 하다. 저자가 그 사실에서 규칙을 끌어내지 않는다
  (5장, p.101):[^evans2003]
  - **그런 기능은 설계 결정을 전달하는 데 도움이 되지만 본질적이지는 않다.**
  - **우리가 모델에서 하고 있는 구분의 상당수는 현재의 도구와 프로그래밍 언어 대부분으로는
    구현에서 명시적으로 선언될 수 없다. 예컨대 엔티티를 선언하고 정체성 연산이 자동으로
    강제되게 할 수는 없다.**
  - **그러나 개념적 구분에 대한 직접적 언어 지원의 부재가 그 구분이 쓸모없다는 뜻은 아니다.
    그것은 그저 구현에서 암묵적으로만 남을 규칙을 유지하는 데 더 많은 규율이 필요하다는
    뜻일 뿐이다.**
- 그 규율의 수단 셋이 열거된다 — **이것은 이름 규약, 선별적 문서화, 그리고 *많은 논의*로
  보강될 수 있다** (5장, p.101).[^evans2003]
  - **"언어가 강제하지 않으면 규칙이 아니다"의 반대편에 이 소스가 선다.** 같은 입장이
    [단언 패턴](assertions-pattern.md)에도 있다 — 단언을 언어가 못 쓰게 하면 주석과 테스트로
    쓰라는 처방이다. 잣대는 강제 가능성이 아니라 **모델이 말해지는가**다.

## 데이터베이스 조율 — 복사가 정규화를 이기는 자리

- 물리적 사실에서 시작한다 — **데이터베이스는 가장 낮은 수준에서 디스크의 물리적 위치에
  데이터를 놓아야 하고, 물리적 부품이 움직여 그 데이터를 읽는 데 시간이 걸린다. 정교한
  데이터베이스는 이 물리 주소들을 클러스터링해 관련 데이터가 한 번의 물리 연산으로 디스크에서
  가져와질 수 있게 하려고 한다** (5장 예제 "Tuning a Database with VALUE OBJECTS",
  p.102).[^evans2003]
- 그래서 참조가 비용이 된다 — **한 객체가 다른 많은 객체에 의해 참조되면, 그 객체들 중
  일부는 가까이(같은 페이지에) 있지 않아 데이터를 얻는 데 추가 물리 연산이 필요하다**
  (5장, p.102).[^evans2003]
- 처방이 복사다 (5장, p.102):[^evans2003]

> By making a copy, rather than sharing a reference to the same instance, a VALUE OBJECT that
> is acting as an attribute of many ENTITIES can be stored on the same page as each ENTITY
> that uses it. This technique of storing multiple copies of the same data is called
> denormalization and is often used when access time is more critical than storage space or
> simplicity of maintenance.

  - **저자가 이 기법의 이름을 비정규화(denormalization)라고 명시한다.** 그 기법 자체의
    일반론은 [정규화와 비정규화](../concepts/normalization-and-denormalization.md)에 있고, 이
    페이지가 더하는 것은 **값 객체라는 분류가 그 기법을 안전하게 만든다**는 자격 조건이다.
- 두 환경의 귀결이 적힌다 (5장, p.102):[^evans2003]
  - **관계형 데이터베이스에서는 별도 테이블에 대한 연관을 만드는 대신 그 값을 소유한 엔티티의
    테이블에 넣고 싶을 수 있다.**
  - **분산 시스템에서는 다른 서버의 값 객체에 대한 참조를 들고 있으면 메시지 응답이 느려질
    것이므로, 대신 객체 전체의 복사본을 다른 서버로 넘겨야 한다.**
- 그리고 그 자유의 근거가 반복된다 — **우리는 값 객체를 다루고 있으므로 이 복사본들을
  자유롭게 만들 수 있다** (5장, p.102).[^evans2003]

## 일반 규칙 — 불필요한 제약을 두지 않는다

- 절이 이 장 전체에 걸리는 일반 규칙으로 닫힌다 (5장, p.101):[^evans2003]

> Defining VALUE OBJECTS and designating them as immutable is a case of following a general
> rule: Avoiding unnecessary constraints in a model leaves developers free to do purely
> technical performance tuning. Explicitly defining the essential constraints lets developers
> tweak the design while keeping safe from changing meaningful behavior.

- 그리고 그 조율이 이식되지 않는다는 단서가 붙는다 — **그런 설계 조정은 특정 프로젝트에서
  쓰는 기술에 매우 특수한 경우가 많다** (5장, p.101).[^evans2003]
  - **이 규칙이 이 페이지를 뒤집어 읽는 방법을 준다.** 값 객체로 분류하는 일은 성능
    기법이 아니라 **제약을 덜어 내는 일**이고, 성능 기법은 그 덜어 냄이 열어 준 공간에서
    나중에 고른다. 순서를 뒤집어 성능을 근거로 분류하면 모델이 기술에 끌려간다.

## 이어지는 페이지

- [값 객체와 엔티티](value-objects-and-entities.md) — 이 설계에 앞서는 분류
- [엔티티의 정체성 설계](entity-identity-design.md) — 정체성이 있는 쪽의 설계
- [도메인 연관](domain-associations.md) — 값 객체 사이의 양방향 연관이 성립하지 않는 이유
- [부수 효과 없는 함수](side-effect-free-functions.md) — 불변성이 봉사하는 조항
- [연산의 닫힘](closure-of-operations.md) — 값 객체가 연산의 결과가 될 수 있는 근거
- [정보 은닉과 정보 누출](../concepts/information-hiding-and-leakage.md) — 내부를 넘길 때의 같은 위험
- [정규화와 비정규화](../concepts/normalization-and-denormalization.md) — 이 절이 이름 붙인 기법의 일반론
- [단언 패턴](assertions-pattern.md) — 언어가 강제하지 않는 규칙을 유지하는 다른 수단
- [도메인 주도 설계](../synthesis/domain-driven-design.md) — 이 축의 허브

[^evans2003]: Evans 2003, 5장 "A Model Expressed in Software" §VALUE OBJECTS 중
    §"Designing VALUE OBJECTS"(pp.99–101, 곁글 "Special Cases: When to Allow Mutability"
    p.101 포함) · 예제 "Tuning a Database with VALUE OBJECTS"(p.102).
    쪽은 인쇄판 쪽 번호(PDF 쪽 − 33, 실측). 원문이 패턴 이름을 작은 대문자로 조판하는
    관례를 직인용에서 유지했다. 패턴의 정의와 처방 문단(pp.97–99)은
    [값 객체와 엔티티](value-objects-and-entities.md)에 있다. 이 소스에서 온 코드 펜스는
    이 페이지에 없다 — 이 절에 코드 목록이 없다.

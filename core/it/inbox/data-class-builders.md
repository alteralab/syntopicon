---
type: concept
title: 데이터 클래스 빌더
description: 필드 묶음뿐인 클래스를 만드는 파이썬의 세 도구(collections.namedtuple·typing.NamedTuple·@dataclass)의 비교와 선택 기준 — 세 빌더가 대신 생성해 주는 특수 메서드, 가변성·클래스 문법·딕셔너리 변환·필드 메타데이터에서 갈리는 자리, 타입 힌트가 런타임에 아무 효과가 없다는 사실과 그럼에도 빌더가 그것을 읽는다는 구조, frozen을 비롯한 데코레이터 옵션과 가변 기본값의 함정, 초기화 후 처리와 필드가 아닌 변수 둘, 그리고 저자 자신이 남긴 유보
generated: { by: "claude-opus-5", at: "2026-08-18T02:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 데이터 클래스 빌더

- [버전 조건](#버전-조건)
- [세 도구가 대신 써 주는 것](#세-도구가-대신-써-주는-것)
- [무엇이 갈리는가 — 기능 비교](#무엇이-갈리는가--기능-비교)
- [언제 무엇을 쓰는가](#언제-무엇을-쓰는가)
- [타입 힌트는 런타임에 아무 효과가 없다](#타입-힌트는-런타임에-아무-효과가-없다)
- [변수 애노테이션이 클래스 안에서 뜻하는 것](#변수-애노테이션이-클래스-안에서-뜻하는-것)
- [데코레이터의 키워드 옵션](#데코레이터의-키워드-옵션)
- [필드 옵션과 가변 기본값의 함정](#필드-옵션과-가변-기본값의-함정)
- [초기화 후 처리 — 검증과 파생 필드](#초기화-후-처리--검증과-파생-필드)
- [필드가 아닌 것들 — 클래스 변수와 초기화 전용 변수](#필드가-아닌-것들--클래스-변수와-초기화-전용-변수)
- [저자 자신의 유보](#저자-자신의-유보)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **함수 사이로 오가는 데이터를 딕셔너리가 아니라 구조체로 넘기기로 했을 때,
파이썬에서 그 구조체를 무엇으로 만들고 무엇을 근거로 고르는가.**

## 버전 조건

> **버전 조건**: 아래 `@dataclass` 데코레이터 옵션 목록은 **파이썬 3.7의 시그니처**다 —
> `init`·`repr`·`eq`·`order`·`unsafe_hash`·`frozen` 여섯이 전부다. 파이썬 3.10이 더한
> `slots`·`kw_only`·`match_args` 키워드 옵션은 **소스가 다루지 않으므로 이 페이지에도
> 없다.** 소스의 이 장은 파이썬 3.9·Mypy 0.910 시점에서 쓰였고(저자가 §"Typed Class
> Attributes"에서 "나는 파이썬 3.9를 쓰고 있다"고 적는다), 그래서 **세 빌더의 성격과 선택
> 기준은 그 뒤로도 유효하지만 옵션 목록은 3.10 이상에서 이 페이지보다 길다.**
>
> **`slots` 옵션에 대해서는 이 소스에서 더 얻을 것이 없다는 것이 최종 실측이다.** 이 소스가
> `__slots__`를 다루는 자리는 11장 하나뿐이고, 거기서도 데코레이터 옵션이 아니라 **클래스
> 속성으로 직접 선언하는 언어 기능**을 다룬다. 그쪽 반입분이
> [__slots__와 인스턴스 메모리](slots-and-instance-memory.md)이고, 이 페이지와 그 페이지
> 사이에 겹치는 서술은 없다. 그러므로 **파이썬 3.10 이상에서 `@dataclass(slots=True)`가
> 무엇을 하는지는 이 KB에 아직 출처가 없다** — 그 언어 기능의 성질(하위 클래스 재선언,
> `@cached_property` 충돌, 약한 참조)은 그쪽 페이지가 답하지만, 데코레이터가 그것을 자동으로
> 붙일 때의 동작은 다른 소스가 와야 채워진다.

## 세 도구가 대신 써 주는 것

- 문제 규정 — **파이썬은 별다른 기능이 거의 또는 전혀 없는 필드 모음일 뿐인 단순한 클래스를
  짓는 몇 가지 방법을 제공한다. 그 패턴이 "데이터 클래스(data class)"로 알려져 있다**
  (5장 도입, p.163).[^ramalho2022]
- 손으로 쓴 `__init__`만으로는 모자란다는 것이 출발점이다. 위도·경도를 담는 클래스 하나로
  저자가 보이는 결손이 셋이다 (5장 §"Overview of Data Class Builders", p.165):[^ramalho2022]
  **`object`에서 상속한 `__repr__`은 별로 쓸모가 없고**, **`==`가 무의미하며 —
  `object`에서 상속한 `__eq__` 메서드는 객체 id를 비교한다**, 그리고 **두 좌표를 비교하려면
  각 속성을 명시적으로 비교해야 한다.**
  - 보일러플레이트 자체도 비용으로 계상된다 — **`__init__` 보일러플레이트를 쓰는 일은 아주
    빨리 낡아 빠진다. 특히 클래스에 속성이 두어 개보다 많으면 그렇다: 각 속성이 세 번씩
    언급된다!** (5장 §"Overview of Data Class Builders", p.164).[^ramalho2022]
- 그래서 세 빌더의 공통 규정이 나온다 — **이 장에서 다루는 데이터 클래스 빌더들은 필요한
  `__init__`·`__repr__`·`__eq__` 메서드를 자동으로 제공하며, 다른 유용한 기능들도 함께
  준다** (5장 §"Overview of Data Class Builders", p.164).[^ramalho2022]
- 세 도구와 그 계보 (5장 도입, p.163):[^ramalho2022]
  - **`collections.namedtuple`: 가장 단순한 방법 — 파이썬 2.6부터 있다.**
  - **`typing.NamedTuple`: 필드에 타입 힌트를 요구하는 대안 — 파이썬 3.5부터이고, 클래스
    문법은 3.6에 더해졌다.**
  - **`@dataclasses.dataclass`: 앞의 두 대안보다 더 많은 맞춤을 허용하는 클래스
    데코레이터로, 많은 옵션과 잠재적 복잡성을 더한다 — 파이썬 3.7부터다.**
- **셋 다 상속으로 일하지 않는다** — **여기서 논의하는 클래스 빌더 중 어느 것도 그 일을
  하는 데 상속에 의존하지 않는다. (…) `@dataclass`는 클래스 계층을 어떤 식으로도 건드리지
  않는 클래스 데코레이터다. 각각이 서로 다른 메타프로그래밍 기법을 써서 만들어지는 중인
  클래스에 메서드와 데이터 속성을 주입한다** (5장 §"Overview of Data Class
  Builders", p.165).[^ramalho2022]
  - `typing.NamedTuple`은 특히 오해를 부른다 — **`NamedTuple`이 클래스 문장에 상위 클래스로
    나타나지만 사실 그것은 상위 클래스가 아니다. `typing.NamedTuple`은 메타클래스의 고급
    기능을 써서 사용자 클래스의 생성을 맞춤화한다** (5장 §"Overview of Data Class
    Builders", p.166).[^ramalho2022] `issubclass(Coordinate, typing.NamedTuple)`은 `False`이고
    `issubclass(Coordinate, tuple)`은 `True`다.
- 곁가지 하나가 명시적으로 제외된다 — `typing.TypedDict`는 빌더가 아니다.
  **`TypedDict`는 인스턴스화할 수 있는 구상 클래스를 만들지 않는다. 그것은 레코드로 쓰이는
  매핑 값을 받을 함수 매개변수와 변수의 타입 힌트를 쓰기 위한 문법일 뿐이다**
  (5장 도입 §Note, p.164).[^ramalho2022]

## 무엇이 갈리는가 — 기능 비교

이 장의 표 5-1이 셋을 나란히 놓는다 (5장 §"Main Features", p.167).[^ramalho2022] `x`는 각
데이터 클래스의 인스턴스다.

| 무엇 | `namedtuple` | `NamedTuple` | `dataclass` |
|---|---|---|---|
| 가변 인스턴스 | 아니오 | 아니오 | **예** |
| 클래스 문장 문법 | 아니오 | **예** | **예** |
| 딕셔너리 만들기 | `x._asdict()` | `x._asdict()` | `dataclasses.asdict(x)` |
| 필드 이름 얻기 | `x._fields` | `x._fields` | `[f.name for f in dataclasses.fields(x)]` |
| 기본값 얻기 | `x._field_defaults` | `x._field_defaults` | `[f.default for f in dataclasses.fields(x)]` |
| 필드 타입 얻기 | 없음 | `x.__annotations__` | `x.__annotations__` |
| 일부만 바꾼 새 인스턴스 | `x._replace(…)` | `x._replace(…)` | `dataclasses.replace(x, …)` |
| 런타임에 새 클래스 | `namedtuple(…)` | `NamedTuple(…)` | `dataclasses.make_dataclass(…)` |

- **가변성이 첫째 갈림이다** — **`collections.namedtuple`과 `typing.NamedTuple`은 `tuple`
  하위 클래스를 지으므로 인스턴스가 불변이다. 기본적으로 `@dataclass`는 가변 클래스를
  생산한다. 그러나 데코레이터는 `frozen` 키워드 인자를 받는다. `frozen=True`이면 인스턴스가
  초기화된 뒤 필드에 값을 대입하려 할 때 클래스가 예외를 일으킨다**
  (5장 §"Mutable instances", p.168).[^ramalho2022]
- **클래스 문장 문법이 둘째다** — **`typing.NamedTuple`과 `dataclass`만이 보통의 클래스
  문장 문법을 지원해, 만들고 있는 클래스에 메서드와 독스트링을 더하기 쉽게 만든다**
  (5장 §"Class statement syntax", p.168).[^ramalho2022]
  - `namedtuple`에도 메서드를 붙일 수는 있으나 저자가 그것을 **해킹**이라 부른다 — 함수를
    정의한 뒤 클래스 속성에 대입하는 방식이고, **가독성과 앞으로의 유지보수를 위해서는
    클래스 문장 안에서 메서드를 코딩하는 편이 훨씬 낫다** (5장 §"Classic Named
    Tuples", p.172).[^ramalho2022]
- `__annotations__`에 대한 경고가 붙는다 — **`__annotations__`에서 직접 읽는 것은 권장되지
  않는다. 대신 그 정보를 얻는 권장 모범 사례는 `inspect.get_annotations(MyClass)`(파이썬
  3.10에 추가) 또는 `typing.get_type_hints(MyClass)`(파이썬 3.5–3.9)를 부르는 것이다.
  그 함수들이 타입 힌트 안의 전방 참조를 해소하는 것 같은 추가 서비스를 제공하기
  때문이다** (5장 §"Main Features", p.168).[^ramalho2022]
  - 버전 조건: 파이썬 3.10 이상에서 `inspect.get_annotations`가 권장 경로다 — 3.5부터
    3.9까지는 `typing.get_type_hints`를 쓴다.
- 메모리 — **`namedtuple`로 지은 클래스의 각 인스턴스는 필드 이름이 클래스에 저장되기
  때문에 튜플과 정확히 같은 양의 메모리를 차지한다** (5장 §"Classic Named
  Tuples", p.169).[^ramalho2022]
- 직렬화 — 두 네임드튜플의 `._asdict()`는 **파이썬 3.7까지는 `OrderedDict`를 돌려주었다.
  파이썬 3.8부터는 평범한 `dict`를 돌려주는데, 키 삽입 순서에 기댈 수 있게 된 지금 그래도
  괜찮다. `OrderedDict`가 꼭 필요하면 `_asdict` 문서가 그 결과로부터 하나를 짓기를 권한다:
  `OrderedDict(x._asdict())`** (5장 §"Classic Named Tuples" §Note,
  p.171).[^ramalho2022] 그 딕셔너리가 곧 JSON 레코드에 가깝다는 것이 이 도구들의 실무
  쓰임 하나다.
- 기본값 — `collections.namedtuple`도 기본값을 받는다. **파이썬 3.7부터 `namedtuple`은
  `defaults` 키워드 전용 인자를 받아 클래스의 오른쪽 N개 필드 각각에 대한 N개의 기본값을
  담은 반복 가능 객체를 제공한다** (5장 §"Classic Named Tuples", p.171).[^ramalho2022]

## 언제 무엇을 쓰는가

저자가 결정표를 따로 두지는 않는다. 위 비교표와 본문의 판단들이 사실상의 기준이다.

- **불변이어야 하면 네임드튜플 둘, 또는 `@dataclass(frozen=True)`.** 다만 frozen이 진짜
  불변은 아니다 — 표 5-2의 각주가 그것을 명시한다: **인스턴스는 우발적 변경으로부터 합리적으로
  안전하지만 정말로 불변인 것은 아니다.** `@dataclass`는 **`dataclass.FrozenInstanceError`
  (`AttributeError`의 하위 클래스)를 일으키는 `__setattr__`과 `__delattr__`을 생성해
  불변성을 흉내 낸다** (5장 §"More About @dataclass" 표 5-2 각주 a, p.179).[^ramalho2022]
  - 그리고 뚫린다 — **파이썬 객체의 동적 성격을 생각하면 참견하기 좋아하는 프로그래머가
    `frozen=True`가 주는 보호를 우회하기가 그리 어렵지 않다. 그러나 그러려면 필요한 요령들이
    코드 리뷰에서 쉽게 눈에 띄어야 한다** (5장 §"More About
    @dataclass", p.180).[^ramalho2022] 즉 frozen은 방어벽이 아니라 **의도 표시 + 사고 방지**다.
- **해시 가능해야 하면 `eq`와 `frozen`이 둘 다 참이어야 한다** — **`eq`와 `frozen` 인자가
  둘 다 `True`이면 `@dataclass`가 적절한 `__hash__` 메서드를 생산하므로 인스턴스가 해시
  가능해진다. (…) `frozen=False`(기본값)이면 `@dataclass`는 `__hash__`를 `None`으로 설정해
  인스턴스가 해시 불가능함을 알리고, 어떤 상위 클래스의 `__hash__`든 덮어쓴다**
  (5장 §"More About @dataclass", p.180).[^ramalho2022]
  - 이것이 [값 객체와 엔티티](value-objects-and-entities.md)의 "값 객체는 불변이어야 하고
    해시는 모든 값 속성에 근거해야 한다"는 규칙이 파이썬에서 한 줄로 실현되는 자리다.
- **튜플·딕셔너리와의 API 호환이 필요하면 데이터 클래스를 쓰지 마라.** 저자가 PEP 557의
  Rationale를 그대로 인용한다 (5장 §"Further Reading", p.196):[^ramalho2022]
  > Where is it not appropriate to use Data Classes?
  >
  > API compatibility with tuples or dicts is required. Type validation beyond that
  > provided by PEPs 484 and 526 is required, or value validation or conversion is
  > required.
  - 뒤쪽 절반이 중요하다 — **PEP 484·526이 제공하는 것 이상의 타입 검증이나, 값 검증·변환이
    필요한 경우**도 부적합 사유다. 그 필요가 실제로 생기면 초기화 후 처리로 손수 짜거나
    `attrs` 같은 외부 도구로 간다.
- **런타임에 클래스를 만들어야 하면** 셋 다 방법이 있다 — **클래스 문장 문법이 더 읽기
  좋지만 그것은 하드코딩이다. 프레임워크는 런타임에 즉석에서 데이터 클래스를 지어야 할 수
  있다** (5장 §"New class at runtime", p.169).[^ramalho2022]
- **더 많은 기능이 필요하면 `attrs`가 대안으로 지목된다** — **검증을 포함해 더 많은 기능과
  고급 기능을 원한다면, Hynek Schlawack이 이끄는 `attrs` 프로젝트가 `dataclasses`보다 몇 해
  앞서 나타났고 더 많은 기능을 제공한다** (5장 §"Further Reading", p.196).[^ramalho2022]
  `@dataclass`가 기반 클래스나 메타클래스가 아니라 **클래스 데코레이터**를 고른 것 자체가
  `attrs`의 영향이라고 저자가 적는다.

## 타입 힌트는 런타임에 아무 효과가 없다

이 절이 뒤의 모든 서술의 전제다.

- 조문 — **타입 힌트에 대해 가장 먼저 알아야 할 것은 그것이 파이썬 바이트코드 컴파일러와
  인터프리터에 의해 전혀 강제되지 않는다는 점이다** (5장 §"Type Hints
  101", p.173).[^ramalho2022]
- 그래서 저자가 제안하는 심상 — **파이썬 타입 힌트를 이해하는 좋은 방법은 그것을 "IDE와
  타입 검사기가 검증할 수 있는 문서"로 생각하는 것이다** (5장 §"No Runtime
  Effect", p.173).[^ramalho2022]
- 실물 — `typing.NamedTuple`로 `lat: float`·`lon: float`을 선언한 클래스에
  `Coordinate('Ni!', None)`을 넘겨도 **오류도 경고도 없이 실행되고 무의미한 `Coordinate`를
  표시한다.** 같은 코드에 Mypy를 돌려야 비로소 `Argument 1 to "Coordinate" has
  incompatible type "str"; expected "float"`가 나온다 (5장 §"No Runtime
  Effect", p.173).[^ramalho2022]
  - **타입 힌트는 주로 Mypy나 PyCharm 내장 검사기 같은 서드파티 타입 검사기를 지원하려는
    것이다. 이것들은 정적 분석 도구다: 실행 중인 코드가 아니라 "쉬고 있는" 파이썬 소스
    코드를 검사한다** (5장 §"No Runtime Effect", p.174).[^ramalho2022]
- **그런데 빌더는 그것을 읽는다.** 이 긴장이 이 장의 핵심 기제다 — **임포트 시점에, 모듈이
  적재될 때 파이썬은 그것들을 읽어 `__annotations__` 딕셔너리를 짓고 `typing.NamedTuple`과
  `@dataclass`가 그것을 써서 클래스를 강화한다** (5장 §"The Meaning of Variable
  Annotations", p.175).[^ramalho2022] 즉 타입 힌트가 런타임 검사에는 쓰이지 않지만 **클래스
  생성에는 쓰인다.**

## 변수 애노테이션이 클래스 안에서 뜻하는 것

같은 세 줄(`a: int` / `b: float = 1.1` / `c = 'spam'`)이 세 문맥에서 다르게 해석된다.
이 대비가 이 장에서 가장 실무적인 절이다 (5장 §"The Meaning of Variable
Annotations" 이하, pp.175–179).[^ramalho2022]

- **평범한 클래스에서** (5장 §"The Meaning of Variable Annotations",
  p.175)[^ramalho2022] — **`a`는 `__annotations__`의 항목이 되지만 그 밖에는 버려진다:
  클래스에 `a`라는 이름의 속성은 만들어지지 않는다.** `b`는 애노테이션으로 저장되면서
  값 `1.1`을 가진 클래스 속성도 된다. `c`는 그냥 평범한 클래스 속성이고 애노테이션이 아니다.
  - **값이 묶이지 않았기 때문에** `a`가 클래스 속성이 되지 않는다는 것이 규칙이다.
- **`typing.NamedTuple`에서** (5장 §"Inspecting a typing.NamedTuple",
  pp.176–177)[^ramalho2022] — `a`와 `b`가 애노테이션이면서 **인스턴스 속성**이 된다.
  `c`는 여전히 평범한 클래스 속성이다.
  - 만들어진 `a`·`b` 클래스 속성은 기술자(descriptor)다 — **실질적으로 `a`와 `b`는 읽기
    전용 인스턴스 속성으로 동작한다. `DemoNTClass` 인스턴스가 그저 멋진 튜플이고 튜플은
    불변임을 떠올리면 말이 된다.**
- **`@dataclass`에서** (5장 §"Inspecting a class decorated with dataclass",
  pp.177–179)[^ramalho2022] — `a`는 애노테이션이면서 **인스턴스 속성**이 되지만 **클래스에는
  `a`라는 속성이 없다.** `b`는 기본값을 담은 클래스 속성으로 남고, `c`는 인스턴스에 묶이지
  않는 클래스 속성이다.
  - 그리고 기본 상태는 가변이다 — 데코레이트된 인스턴스에 `dc.a = 10`은 물론 `dc.b = 'oops'`
    도, 심지어 선언에 없는 `dc.z = 'secret stash'`도 통과한다. **이것은 정상적인 파이썬
    동작이다: 보통 인스턴스는 클래스에 나타나지 않는 자기만의 속성을 가질 수 있다.**
  - 그 자유에 값이 붙는다는 것을 저자가 각주로 계상한다 — **`__init__` 뒤에 속성을 설정하는
    것은 `__dict__` 키 공유 메모리 최적화를 무력화한다** (5장 각주 7,
    p.179).[^ramalho2022] 즉 나중에 붙인 속성 하나가 그 인스턴스의 메모리 배치를
    되돌린다. 그 최적화가 무엇인지는 [딕셔너리와 집합](dictionaries-and-sets.md)의
    §"해시 테이블이 강제하는 실무 규칙"에 있다 — 같은 책 3장이 근거다.

## 데코레이터의 키워드 옵션

`@dataclass`의 시그니처는 `@dataclass(*, init=True, repr=True, eq=True, order=False,
unsafe_hash=False, frozen=False)`이고, 별표 때문에 **나머지 매개변수가 전부 키워드
전용**이다 (5장 §"More About @dataclass", p.179).[^ramalho2022]

| 옵션 | 무엇 | 기본 | 단서 |
|---|---|---|---|
| `init` | `__init__` 생성 | `True` | 사용자가 직접 구현하면 무시된다 |
| `repr` | `__repr__` 생성 | `True` | 사용자가 직접 구현하면 무시된다 |
| `eq` | `__eq__` 생성 | `True` | 사용자가 직접 구현하면 무시된다 |
| `order` | `__lt__`·`__le__`·`__gt__`·`__ge__` 생성 | `False` | `True`인데 `eq=False`이면, 또는 생성될 비교 메서드 중 어느 것이 이미 정의·상속돼 있으면 예외 |
| `unsafe_hash` | `__hash__` 생성 | `False` | 의미가 복잡하고 단서가 여럿이다 |
| `frozen` | 인스턴스를 "불변"으로 | `False` | 진짜 불변은 아니다 (위 참조) |

- 저자의 실무 지침 — **기본값이 정말로 흔한 사용 사례에 가장 유용한 설정이다. 기본값에서
  바꿀 가능성이 더 큰 옵션은 다음 둘이다: 클래스 인스턴스의 우발적 변경을 막기 위한
  `frozen=True`, 그리고 데이터 클래스 인스턴스의 정렬을 허용하기 위한 `order=True`**
  (5장 §"More About @dataclass", p.180).[^ramalho2022]
- `unsafe_hash`에 대해서는 PEP 557을 인용하고 판단을 미룬다 (5장 §"More About
  @dataclass", p.180):[^ramalho2022]
  > Although not recommended, you can force Data Classes to create a `__hash__` method
  > with `unsafe_hash=True`. This might be the case if your class is logically immutable
  > but can nonetheless be mutated. This is a specialized use case and should be
  > considered carefully.

## 필드 옵션과 가변 기본값의 함정

- 순서 제약이 먼저다 — **파이썬은 기본값이 있는 매개변수 뒤에 기본값 없는 매개변수를
  허용하지 않으므로, 기본값이 있는 필드를 선언한 뒤로는 남은 필드 전부가 기본값을 가져야
  한다** (5장 §"Field Options", p.180).[^ramalho2022]
- **가변 기본값은 데코레이터가 거부한다** — `guests: list = []`라고 쓴 클래스는 적재 시점에
  `ValueError: mutable default <class 'list'> for field guests is not allowed: use
  default_factory`로 죽는다 (5장 §"Field Options" 예제 5-13, p.181).[^ramalho2022]
  - 고치는 법은 `dataclasses.field(default_factory=list)`다. **`default_factory` 매개변수는
    함수·클래스·그 밖의 호출 가능한 것을 제공하게 해 주며, 데이터 클래스의 인스턴스가
    만들어질 때마다 인자 없이 호출돼 기본값을 짓는다. 이렇게 하면 `ClubMember`의 각
    인스턴스가 자기 리스트를 갖는다 — 모든 인스턴스가 클래스에서 온 같은 리스트를 공유하는
    대신이며, 그 공유는 우리가 원하는 경우가 드물고 흔히 버그다**
    (5장 §"Field Options", p.181).[^ramalho2022]
  - **⚠ 부분적 해결책이다** — **`@dataclass`가 리스트 기본값을 가진 클래스 정의를 거부하는
    것은 좋은 일이다. 그러나 그것이 `list`·`dict`·`set`에만 적용되는 부분적 해결책임을
    알아 두라. 다른 가변 값이 기본값으로 쓰이면 `@dataclass`가 표시해 주지 않는다. 문제를
    이해하고 가변 기본값을 설정할 때 기본 팩토리를 쓰기를 기억하는 것은 당신 몫이다**
    (5장 §"Field Options" §Warning, p.181).[^ramalho2022]
- 대표 예제가 더블린 코어 레코드다. 필드 순서 제약·`default_factory`·`Optional`·`Enum`
  기본값이 한자리에 있어 "구조체로 데이터를 넘긴다"의 실물 서식이 된다
  (5장 §"@dataclass Example: Dublin Core Resource Record" 예제 5-19, pp.187–188).[^ramalho2022]

  ```python
  from dataclasses import dataclass, field
  from typing import Optional
  from enum import Enum, auto
  from datetime import date

  class ResourceType(Enum):
      BOOK = auto()
      EBOOK = auto()
      VIDEO = auto()

  @dataclass
  class Resource:
      """Media resource description."""
      identifier: str
      title: str = '<untitled>'
      creators: list[str] = field(default_factory=list)
      date: Optional[date] = None
      type: ResourceType = ResourceType.BOOK
      description: str = ''
      language: str = ''
      subjects: list[str] = field(default_factory=list)
  ```

  - 읽는 법 (5장 §"@dataclass Example: Dublin Core Resource Record", p.188):[^ramalho2022]
    `identifier`가 유일한 필수 필드이고, **`title`이 기본값을 가진 첫 필드다. 이것이 아래의
    모든 필드가 기본값을 제공하도록 강제한다.** `Enum`은 `type` 필드에 타입 안전한 값을
    주기 위한 것이다.
  - `list[str]`은 매개변수화된 제네릭 타입이고 **파이썬 3.9부터 내장 `list`가 그 대괄호
    표기를 받는다** (5장 §"Field Options", p.182).[^ramalho2022] 3.8 이하에서는
    `typing.List[str]`을 써야 한다.
    - 그리고 `list`와 `list[str]`의 차이가 명시된다 — **`guests: list`는 `guests`가 어떤
      종류의 객체든 담은 리스트일 수 있다는 뜻이고, `guests: list[str]`은 `guests`가 모든
      항목이 `str`인 리스트여야 한다는 뜻이다** (5장 §"Field Options", p.182).[^ramalho2022]
- `field` 함수의 나머지 옵션 (5장 §"Field Options" 표 5-3, pp.182–183):[^ramalho2022] `default`,
  `default_factory`, `init`(생성될 `__init__`의 매개변수에 넣을지), `repr`(`__repr__`에
  넣을지), `compare`(`__eq__`·`__lt__` 등 비교 메서드에 쓸지), `hash`(`__hash__` 계산에
  넣을지 — 기본 `None`은 **`compare=True`일 때만 `__hash__`에 쓴다**는 뜻),
  `metadata`(사용자 정의 데이터를 담는 매핑으로 `@dataclass`가 무시한다).
  - `default` 옵션이 따로 있는 이유가 문법적이다 — **`field` 호출이 필드 애노테이션에서
    기본값의 자리를 차지하기 때문이다** (5장 §"Field Options", p.183).[^ramalho2022]

## 초기화 후 처리 — 검증과 파생 필드

- 규정 — **`@dataclass`가 생성한 `__init__` 메서드는 넘겨진 인자들을 받아 그것들을(또는
  없으면 기본값을) 인스턴스 필드인 인스턴스 속성에 대입할 뿐이다. 그러나 인스턴스를
  초기화하려면 그 이상이 필요할 수 있다. 그런 경우 `__post_init__` 메서드를 제공할 수 있다.
  그 메서드가 존재하면 `@dataclass`가 생성되는 `__init__`에 마지막 단계로
  `__post_init__`을 호출하는 코드를 더한다** (5장 §"Post-init
  Processing", p.183).[^ramalho2022]
- 쓰임 둘 — **`__post_init__`의 흔한 사용 사례는 검증(validation), 그리고 다른 필드에
  근거해 필드 값을 계산하는 것이다** (5장 §"Post-init Processing", p.183).[^ramalho2022]
- 저자의 예제는 데이터 클래스를 상속시켜 만드는데, **본인이 그 자리에서 그것을 경고한다** —
  **14장에서 우리는 상속의 오용에 대해, 특히 상위 클래스들이 추상이 아닐 때에 대해 이야기할
  것이다. 데이터 클래스의 계층을 만드는 것은 대개 나쁜 생각이지만, 여기서는 예제를 짧게
  하는 데 도움이 되었다** (5장 §"Post-init Processing" §Note, p.184).[^ramalho2022]
  - **이 자리가 이 페이지의 실무 경고다.** 데이터 클래스를 상속으로 확장하려는 충동은
    [상속세](inheritance-tax.md)가 재는 그 비용을 그대로 문다.

## 필드가 아닌 것들 — 클래스 변수와 초기화 전용 변수

`@dataclass`는 애노테이션의 타입을 거의 신경 쓰지 않는다. **예외가 둘 있다**
(5장 §"Typed Class Attributes", pp.185–186).[^ramalho2022]

- **`typing.ClassVar` — 클래스 변수임을 선언한다.** 문제 상황부터가 함정이다: 클래스 속성에
  타입 힌트를 그냥 붙이면 `@dataclass`가 그것을 인스턴스 필드로 만들어 버린다. 그래서
  **타입 검사기와 `@dataclass`를 둘 다 만족시키려면** `all_handles: ClassVar[set[str]] =
  set()`처럼 써야 한다 — **`all_handles`는 `set-of-str` 타입의 클래스 속성이며 기본값은 빈
  집합이다.**
  - 저자가 이 우회를 **못생겼다(ugly)**고 부른다 (5장 §"Typed Class
    Attributes", p.186).[^ramalho2022] 그리고 Mypy가 주는 힌트조차 `@dataclass` 맥락에서는
    도움이 안 된다고 적는다.
- **`dataclasses.InitVar` — 필드가 아닌 초기화 전용 인자를 선언한다.** **`InitVar`는
  `@dataclass`가 그 인자를 보통 필드로 다루는 것을 막는다. 그것은 인스턴스 속성으로 설정되지
  않고 `dataclasses.fields` 함수도 그것을 나열하지 않는다. 그러나 생성될 `__init__`이 받을
  인자 중 하나가 되고, `__post_init__`에도 넘겨진다** (5장 §"Initialization Variables
  That Are Not Fields", p.187).[^ramalho2022] 문서가 드는 예는 데이터베이스 객체를 생성자에
  넘겨 그것으로 필드 하나를 채우는 경우다.

## 저자 자신의 유보

이 장은 도구를 소개하고 끝내지 않는다. 곁글에서 저자가 두 가지 불만을 남긴다
(5장 §"Soapbox" 곁글, pp.198–199).[^ramalho2022]

- **첫째 — `@dataclass`를 쓰면 타입 힌트가 선택이 아니다.** **우리는 PEP 484 이후 지난
  7년 동안 타입 힌트가 언제나 선택적일 것이라고 약속받아 왔다. 이제 우리에게 그것을
  요구하는 주요한 새 언어 기능이 생겼다. 정적 타이핑이라는 흐름 전체가 마음에 들지
  않는다면 `attrs`를 쓰고 싶을 수 있다.**
- **둘째 — PEP 526 문법이 클래스 문장의 확립된 관행을 뒤집는다.** **클래스 블록의 최상위에
  선언된 모든 것은 클래스 속성이었다(메서드도 클래스 속성이다). PEP 526과 `@dataclass`와
  함께, 최상위에 타입 힌트와 함께 선언된 어떤 속성이든 인스턴스 속성이 된다.**
  - 그 결과가 규칙의 예외의 예외다 — 타입 힌트가 없으면 다시 클래스 속성이고, 클래스 속성에
    타입을 달고 싶으면 `ClassVar`라는 유사 타입에 기대야 한다. 저자의 판정 —
    **여기서 우리는 규칙의 예외의 예외에 대해 이야기하고 있다. 이것은 내게 다소
    비파이썬적으로 보인다.**
  - 저자가 대안 문법(인스턴스 속성에 `.` 접두를 붙이는)까지 제시하며 이것이 문법 변경을
    요구한다고 인정한다. 즉 **불만의 대상은 도구가 아니라 언어 설계의 이 자리다.**

이 유보를 옮겨 두는 이유는 도구 선택의 근거가 되어서가 아니라, **이 KB가 `@dataclass`를
규약으로 채택할 때 그 규약이 무엇을 감수하는지**를 남기기 위해서다 — 타입 힌트 의무화와
클래스 속성 선언의 특례가 그것이다.

## 이어지는 페이지

- [코드 냄새로서의 데이터 클래스](data-class-as-code-smell.md) — **같은 장의 뒷부분.**
  이 도구들을 쓰는 것이 언제 설계 문제의 신호인가
- [값 객체와 엔티티](value-objects-and-entities.md) — 이 도구들이 도메인 모델에서 무엇을
  표현하는 데 쓰이는가. `frozen` 데이터클래스가 값 객체가 되는 자리
- [파이썬 데이터 모델](python-data-model.md) — 이 빌더들이 대신 생성해 주는 특수 메서드가
  무엇인가
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — 같은 소스가 타입 힌트의
  다른 쪽 끝(구조적 타이핑)을 다루는 자리
- [점진적 타이핑](gradual-typing-in-python.md) — 여기 쓰이는 타입 힌트가 어떤 종류의 타입
  체계에 속하는가. **런타임에 효과가 없다는 사실이 그 체계의 정의에 들어 있는 자리**
- [데이터 조직화 리팩터링](organizing-data.md) — 같은 값·참조 구분을 카탈로그가
  *Change Reference to Value*로 부르는 자리
- [기본형 집착과 데이터 뭉치](code-smells.md) — 왜 딕셔너리·튜플 대신 구조체를 쓰는가의
  냄새 쪽 근거
- [상속세](inheritance-tax.md) — 데이터 클래스 계층을 만들지 말라는 경고의 원리 쪽
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 같은 이름의 옵션이 가리키는
  언어 기능. 이 소스가 그것을 다루는 유일한 자리이고, 위 버전 조건 블록이 두 페이지의 관계를
  적어 둔다
- [파이썬다운 객체 만들기](building-pythonic-objects.md) — 이 빌더들이 대신 써 주는 특수
  메서드를 손으로 쓰면 어떤 모양이 되는가
- [객체 참조와 가변성](object-references-and-mutability.md) — `@dataclass`가 가변 기본값을
  거부하는 그 함정의 일반형과, `frozen`이 왜 진짜 불변이 아닌가의 언어 쪽 기제
- [딕셔너리와 집합](dictionaries-and-sets.md) — 해시 가능성의 계약(`__eq__`와 `__hash__`가
  함께 가야 한다)이 `eq`·`frozen` 두 옵션으로 만족되는 자리
- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 필드에 이름을 붙이기 전,
  튜플을 레코드로 쓰던 자리
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 5장 "Data Class Builders", pp.163–199(도입 pp.163–164 ·
    §"Overview of Data Class Builders" pp.164–167 · §"Main Features" pp.167–169와 그 아래
    §"Mutable instances"·§"Class statement syntax" 등 일곱 절 · §"Classic Named Tuples"
    pp.169–172 · §"Typed Named Tuples" pp.172–173 · §"Type Hints 101" p.173과 그 아래
    §"No Runtime Effect" pp.173–174·§"Variable Annotation Syntax" pp.174–175·
    §"The Meaning of Variable Annotations" p.175·§"Inspecting a typing.NamedTuple"
    pp.176–177·§"Inspecting a class decorated with dataclass" pp.177–179 ·
    §"More About @dataclass" pp.179–180과 그 아래 §"Field Options" pp.180–183·
    §"Post-init Processing" pp.183–185·§"Typed Class Attributes" pp.185–186·
    §"Initialization Variables That Are Not Fields" pp.186–187·
    §"@dataclass Example: Dublin Core Resource Record" pp.187–189 · §"Further Reading"
    pp.196–197 · §"Soapbox" 곁글 pp.197–199 · 각주 7 p.179).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    표 5-1·5-2·5-3은 원문의 표를 옮긴 것이고, 표 5-2의 "notes" 열과 표 5-3의 각주 둘은
    본문 서술로 풀었다. 코드 펜스는 예제 5-19 원문 그대로다 — 원문 코드 목록에 조판용
    번호 표지가 삽입돼 있어 그것만 제거했다.

---
type: concept
title: 딕셔너리와 집합
description: 파이썬이 자기 자신을 딕셔너리로 구현한다는 사실과 그 귀결 — 해시 가능성의 계약(__hash__와 __eq__가 함께 가야 한다), 없는 키를 다루는 세 갈래(setdefault·defaultdict·__missing__)와 각각의 대가, 맞춤 매핑을 만들 때 dict가 아니라 UserDict를 상속해야 하는 이유, 읽기 전용 façade와 딕셔너리 뷰라는 동적 프록시, 해시 테이블이 강제하는 실무 규칙들(키 공유 최적화와 __init__ 밖 속성 금지), 그리고 집합 연산이 루프와 조건문을 대신하는 자리
generated: { by: "claude-opus-5", at: "2026-08-18T05:00:00Z" }
status: draft
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 딕셔너리와 집합

- [dict은 언어의 부품이다](#dict은-언어의-부품이다)
- [해시 가능성의 계약](#해시-가능성의-계약)
- [없는 키를 다루는 세 갈래](#없는-키를-다루는-세-갈래)
- [맞춤 매핑은 UserDict에서 만든다](#맞춤-매핑은-userdict에서-만든다)
- [읽기 전용 매핑과 딕셔너리 뷰](#읽기-전용-매핑과-딕셔너리-뷰)
- [해시 테이블이 강제하는 실무 규칙](#해시-테이블이-강제하는-실무-규칙)
- [집합 — 연산이 루프를 대신한다](#집합--연산이-루프를-대신한다)
- [현대 문법 — 합치기와 컴프리헨션](#현대-문법--합치기와-컴프리헨션)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파이썬에서 매핑과 집합을 쓸 때 해시 테이블이라는 구현이 무엇을 요구하고
무엇을 되돌려 주는가.**

## dict은 언어의 부품이다

- 이 장의 출발점은 성능이 아니라 **편재성**이다 — **우리는 모든 파이썬 프로그램에서
  딕셔너리를 쓴다. 코드에 직접 쓰지 않더라도 간접적으로 쓴다. `dict` 타입이 파이썬 구현의
  근본적인 일부이기 때문이다. 클래스와 인스턴스 속성, 모듈 네임스페이스, 함수 키워드 인자가
  메모리에서 딕셔너리로 표현되는 핵심 파이썬 구조물의 예다. `__builtins__.__dict__`는 모든
  내장 타입·객체·함수를 저장한다** (3장 도입, p.77).[^ramalho2022]
  - 그래서 **그 결정적 역할 때문에 파이썬 dict은 고도로 최적화돼 있고 계속 개선되고 있다**
    (같은 절, p.77).
- 엔진의 이름이 붙는다 — **해시 테이블(hash tables)이 파이썬의 고성능 dict 뒤에 있는
  엔진이다. 해시 테이블에 기반한 다른 내장 타입이 `set`과 `frozenset`이다**
  (3장 도입, p.77).[^ramalho2022]
- 집합에 대한 주장이 하나 더 붙는데 이 페이지의 마지막 절이 그것을 받는다 — **파이썬 집합은
  합집합·교집합·부분집합 검사 등 집합론의 근본 연산을 전부 구현한다. 그것들로 우리는
  알고리즘을 더 선언적인 방식으로 표현할 수 있고, 수많은 중첩 루프와 조건문을 피할 수
  있다** (3장 도입, p.77).[^ramalho2022]

## 해시 가능성의 계약

이 절이 이 장에서 가장 조문에 가깝고, 이 KB의 다른 페이지들이 딛는 자리다.

- 정의가 파이썬 용어집에서 인용된다 (3장 §"What Is Hashable", p.84):[^ramalho2022]
  > An object is hashable if it has a hash code which never changes during its lifetime
  > (it needs a `__hash__()` method), and can be compared to other objects (it needs an
  > `__eq__()` method). Hashable objects which compare equal must have the same hash code.
- 그 요구가 타입별로 풀린다 (3장 §"What Is Hashable", pp.84–85):[^ramalho2022]
  - **수치 타입과 평면 불변 타입 `str`·`bytes`는 전부 해시 가능하다. 컨테이너 타입은 그것이
    불변이고 담고 있는 모든 객체 또한 해시 가능하면 해시 가능하다.**
  - **`frozenset`은 언제나 해시 가능하다. 그것이 담는 모든 원소가 정의상 해시 가능해야 하기
    때문이다. 튜플은 그 모든 항목이 해시 가능할 때에만 해시 가능하다.**
- **⚠ 해시 코드는 프로세스 사이에서 안정하지 않다** — **객체의 해시 코드는 파이썬 버전,
  기계 아키텍처에 따라, 그리고 보안상의 이유로 해시 계산에 더해지는 소금(salt) 때문에 다를
  수 있다. 올바르게 구현된 객체의 해시 코드는 하나의 파이썬 프로세스 안에서만 일정함이
  보장된다** (3장 §"What Is Hashable", p.85).[^ramalho2022]
  - 버전 조건: PEP 456이 이 소금과 그 보안 함의를 규정한다. 해시 코드를 영속 저장의 키로
    쓰면 안 된다는 뜻이다.
- **사용자 정의 타입의 기본값이 함정을 만든다** — **사용자 정의 타입은 기본적으로 해시
  가능하다. 그 해시 코드가 `id()`이고, `object` 클래스에서 물려받은 `__eq__()` 메서드가 그저
  객체 ID를 비교하기 때문이다. 어떤 객체가 자기 내부 상태를 고려하는 맞춤 `__eq__()`를
  구현하면, 그 객체는 `__hash__()`가 언제나 같은 해시 코드를 돌려줄 때에만 해시 가능하다.
  실무에서 이것은 `__eq__()`와 `__hash__()`가 객체의 생애 동안 결코 바뀌지 않는 인스턴스
  속성만 고려할 것을 요구한다** (3장 §"What Is Hashable", p.85).[^ramalho2022]
  - **이 한 문단이 [값 객체와 엔티티](value-objects-and-entities.md)의 규칙이 파이썬에서
    강제되는 자리다.** 그쪽이 "값 객체는 불변이어야 하고 해시는 모든 값 속성에 근거해야
    한다"고 말하는데, 여기서는 그것이 취향이 아니라 **해시 테이블이 깨지지 않기 위한 조건**
    으로 나온다. 그리고 [데이터 클래스 빌더](data-class-builders.md)의
    `@dataclass(eq=True, frozen=True)`가 그 조건을 한 줄로 만족시키는 도구다.

## 없는 키를 다루는 세 갈래

- 출발점은 파이썬의 기본 성향이다 — **파이썬의 빨리 실패하기(fail-fast) 철학에 맞게,
  `d[k]` 접근은 `k`가 존재하는 키가 아닐 때 오류를 일으킨다**
  (3장 §"Inserting or Updating Mutable Values", p.87).[^ramalho2022]
- **① `d.get(k, default)`** — 기본값이 `KeyError` 처리보다 편할 때의 대안이다. 다만
  **가변 값을 꺼내 그것을 갱신하려 할 때는 더 나은 방법이 있다** (같은 절, p.87).
- **② `setdefault`** — 조회를 한 번으로 줄인다. `my_dict.setdefault(key, []).append(new_value)`
  한 줄이 `if key not in my_dict: my_dict[key] = []` 뒤에 `append`하는 것과 결과가 같되,
  **후자는 키를 적어도 두 번 — 없으면 세 번 — 찾는 반면 `setdefault`는 한 번의 조회로 전부
  해낸다** (3장 §"Inserting or Updating Mutable Values", p.89).[^ramalho2022]
- **③ `collections.defaultdict`** — **`d[k]` 문법으로 없는 키를 찾을 때 기본값을 가진 항목을
  요청에 따라 만든다** (3장 §"defaultdict: Another Take on Missing Keys",
  p.90).[^ramalho2022] `dd = defaultdict(list)`이면 `dd['new-key']`가 `list()`를 불러 새
  리스트를 만들고, 그것을 `dd`에 넣고, 그 참조를 돌려준다. 그 호출 가능 객체는
  `default_factory` 인스턴스 속성에 담긴다.
  - **⚠ 적용 범위가 좁다** — **`defaultdict`의 `default_factory`는 `__getitem__` 호출에
    기본값을 주기 위해서만 불리고 다른 메서드에는 불리지 않는다. 예컨대 `dd`가
    `defaultdict`이고 `k`가 없는 키면 `dd[k]`는 `default_factory`를 불러 기본값을 만들지만,
    `dd.get(k)`는 여전히 `None`을 돌려주고 `k in dd`는 `False`다**
    (3장 §"defaultdict: Another Take on Missing Keys", p.91).[^ramalho2022]
- **④ `__missing__`** — 위 셋의 바닥에 있는 훅이다. **이 메서드는 기반 `dict` 클래스에
  정의돼 있지 않지만 `dict`은 그것을 알고 있다: `dict`을 상속해 `__missing__` 메서드를
  제공하면, 표준 `dict.__getitem__`이 키를 찾지 못할 때 `KeyError`를 일으키는 대신 그것을
  부른다** (3장 §"The __missing__ Method", p.91).[^ramalho2022]
  - **⚠ 그런데 이 훅만으로는 일관성이 안 온다** — **`setdefault`와 `update`의 동작도 키
    조회의 영향을 받는다는 것을 잊지 마라. 그리고 `__missing__`의 로직에 따라 일관성 없거나
    놀라운 동작을 피하려면 `__setitem__`에 특별한 로직을 구현해야 할 수도 있다**
    (3장 §"Inconsistent Usage of __missing__ in the Standard Library",
    p.95).[^ramalho2022]
- 패턴 매칭 쪽에는 이 자동 처리가 걸리지 않는다는 단서가 붙어 있다 — **없는 키의 자동
  처리는 발동하지 않는다. 패턴 매칭이 언제나 `d.get(key, sentinel)` 메서드를 쓰기 때문이다 —
  기본 보초는 사용자 데이터에 나타날 수 없는 특별한 표지 값이다** (3장 §"Pattern Matching
  with Mappings", p.83).[^ramalho2022]

## 맞춤 매핑은 UserDict에서 만든다

- 조문 — **맞춤 매핑 타입은 `dict`이 아니라 `collections.UserDict`를 확장해 만드는 편이
  낫다** (3장 §"Subclassing UserDict Instead of dict", p.97).[^ramalho2022]
- 이유가 둘이다 (3장 §"Subclassing UserDict Instead of dict",
  pp.97–98):[^ramalho2022]
  - **내장 타입이 몇 가지 구현 지름길을 갖고 있어서, `UserDict`에서라면 아무 문제 없이
    물려받을 수 있는 메서드를 우리가 재정의하도록 결국 강제한다.**
  - **`UserDict`는 `dict`을 상속하지 않고 합성(composition)을 쓴다: 실제 항목을 담는
    `data`라는 이름의 내부 `dict` 인스턴스를 갖는다. 이것이 `__setitem__` 같은 특수 메서드를
    짤 때 원하지 않는 재귀를 피하게 하고 `__contains__`의 코딩을 단순하게 만든다.**
- ABC를 직접 상속하는 것도 권해지지 않는다 — **맞춤 매핑을 구현하려면 이 ABC들을 상속하는
  것보다 `collections.UserDict`를 확장하거나 합성으로 `dict`을 감싸는 편이 쉽다**
  (3장 §"Standard API of Mapping Types", p.84).[^ramalho2022]
- 대표 서식이 이것이다. 문자열이 아닌 키를 삽입·갱신·조회 시 전부 `str`로 바꾸는 매핑이고,
  세 메서드만 쓴다 (3장 §"Subclassing UserDict Instead of dict" 예제 3-9,
  p.98).[^ramalho2022]

  ```python
  import collections


  class StrKeyDict(collections.UserDict):

      def __missing__(self, key):
          if isinstance(key, str):
              raise KeyError(key)
          return self[str(key)]

      def __contains__(self, key):
          return str(key) in self.data

      def __setitem__(self, key, item):
          self.data[str(key)] = item
  ```

  - 나머지가 전부 상속으로 온다 — **`UserDict`가 `abc.MutableMapping`을 확장하므로,
    `StrKeyDict`를 온전한 매핑으로 만드는 나머지 메서드는 `UserDict`·`MutableMapping`·
    `Mapping`에서 물려받는다** (같은 절, p.99).[^ramalho2022]
  - 특히 두 메서드가 값을 한다 (같은 절, p.99):[^ramalho2022] **`MutableMapping.update`**는
    `self[key] = value`로 항목을 더하므로 **결국 우리가 구현한 `__setitem__`을 부르고**,
    **`Mapping.get`**은 `__getitem__`과 같은 결과를 주도록 이미 구현돼 있어 손으로 짤 필요가
    없다.
  - **이것이 [상속세](inheritance-tax.md)의 반대 사례로 읽히는 자리다** — 여기서는 상속이
    비용이 아니라 이득이다. 갈림은 상속 대상이 **구상 클래스의 구현 지름길**(`dict`)인가
    **추상 기반 클래스가 규정한 인터페이스**(`UserDict` → `MutableMapping`)인가에 있다.
    #hypothesis 저자가 그렇게 정식화하지는 않았다.

## 읽기 전용 매핑과 딕셔너리 뷰

- **표준 라이브러리에 진짜 불변 매핑은 없다.** 대신 **`types` 모듈이 `MappingProxyType`이라는
  래퍼 클래스를 제공하는데, 매핑을 주면 원래 매핑에 대한 읽기 전용이지만 동적인 프록시인
  `mappingproxy` 인스턴스를 돌려준다. 이것은 원래 매핑에 대한 갱신이 `mappingproxy`에서
  보이지만 그것을 통해 변경할 수는 없다는 뜻이다** (3장 §"Immutable Mappings",
  p.99).[^ramalho2022]
  - 쓰임의 모양이 규정된다 — 구상 클래스의 생성자가 비공개 매핑을 채우고 **`mappingproxy`로
    구현된 공개 속성으로 API 클라이언트에게 노출한다. 그러면 클라이언트가 실수로 항목을
    더하거나 지우거나 바꿀 수 없다** (같은 절, p.100).[^ramalho2022] 이것이
    [정보 은닉과 정보 누출](information-hiding-and-leakage.md)이 말하는 것의 아주 작은
    실물이다 — 읽기는 열고 쓰기는 닫는다. #hypothesis 저자가 그렇게 연결하지는 않았다.
- **딕셔너리 뷰(dictionary views)** — `.keys()`·`.values()`·`.items()`가 돌려주는 것들이다.
  **이 딕셔너리 뷰들은 `dict` 구현이 쓰는 내부 자료 구조에 대한 읽기 전용 투영이다. 그것들은
  대상 `dict`에 이미 있는 데이터를 복제하는 리스트를 돌려주던 파이썬 2 메서드들의 메모리
  부담을 피한다** (3장 §"Dictionary Views", p.101).[^ramalho2022]
  - **뷰는 동적 프록시다** — **원본 `dict`이 갱신되면 기존 뷰를 통해 즉시 변경을 볼 수
    있다** (같은 절, p.101).[^ramalho2022]
  - 그리고 **집합처럼 쓸 수 있다** — **`dict_keys`와 `dict_items`는 `&`(교집합)·`|`(합집합)·
    `-`(차집합)·`^`(대칭차) 연산자를 지원하는 특수 메서드를 구현한다**
    (3장 §"Set Operations on dict Views", p.111).[^ramalho2022] `d1.keys() & d2.keys()`가
    두 딕셔너리에 공통인 키를 준다.
  - **⚠ 단서 하나** — **`dict_items` 뷰는 `dict`의 모든 값이 해시 가능할 때에만 집합으로
    동작한다. 해시 불가능한 값을 가진 `dict_items` 뷰에 집합 연산을 시도하면 `TypeError`가
    난다. 반면 `dict_keys` 뷰는 언제나 집합으로 쓸 수 있다. 모든 키가 정의상 해시
    가능하기 때문이다** (같은 절, p.111).[^ramalho2022]
  - 저자의 권유가 이 절의 실무 조문이다 — **뷰에 집합 연산자를 쓰면 코드에서 딕셔너리의
    내용을 살필 때 수많은 루프와 `if`를 아낀다** (같은 절, p.111).

## 해시 테이블이 강제하는 실무 규칙

저자가 이 절을 **"이 설계의 실무적 효과를 이해하는 것이 중요하다"**로 열고 다섯 항목을
나열한다 (3장 §"Practical Consequences of How dict Works", p.102).[^ramalho2022]

- **키는 해시 가능한 객체여야 한다.** 위 §"해시 가능성의 계약" 참조.
- **키에 의한 항목 접근이 매우 빠르다.** **`dict`이 수백만 개의 키를 가져도 파이썬은 키의
  해시 코드를 계산하고 해시 테이블의 색인 오프셋을 유도해 키를 직접 찾아낼 수 있다.**
- **키 순서가 보존된다** — **CPython 3.6에서 `dict`을 위한 더 조밀한 메모리 배치의 부수
  효과였고, 3.7에서 공식 언어 기능이 되었다.**
  - 버전 조건: 파이썬 3.7 이상에서 언어 보증이다 — 3.6에서는 구현 세부였다.
- **⚠ 그럼에도 메모리 부담이 상당하다** — **새 조밀 배치에도 불구하고 dict은 불가피하게
  상당한 메모리 부담을 갖는다. 컨테이너에 가장 조밀한 내부 자료 구조는 항목에 대한
  포인터 배열일 것이다. 그것에 비해 해시 테이블은 항목당 더 많은 데이터를 저장해야 하고,
  파이썬은 효율을 유지하기 위해 해시 테이블 행의 최소 3분의 1을 비워 두어야 한다.**
- **조문 — 메모리를 아끼려면 `__init__` 메서드 밖에서 인스턴스 속성을 만들지 마라.**
  - 기제가 그다음 문단에 있다. **PEP 412(키 공유 딕셔너리)가 파이썬 3.3에 구현된 이후,
    한 클래스의 인스턴스들은 클래스와 함께 저장된 공통 해시 테이블을 공유할 수 있다.
    그 공통 해시 테이블은 그 클래스의 첫 인스턴스가 `__init__`을 반환할 때와 같은 속성
    이름을 가진 새 인스턴스마다의 `__dict__`가 공유한다. 그러면 각 인스턴스의 `__dict__`는
    자기 속성 값만 단순한 포인터 배열로 담을 수 있다. `__init__` 뒤에 인스턴스 속성을
    더하면 파이썬이 그 인스턴스 하나의 `__dict__`만을 위한 새 해시 테이블을 만들도록
    강제한다** (3장 §"Practical Consequences of How dict Works",
    p.103).[^ramalho2022]
  - 효과가 수치로 붙는다 — **PEP 412에 따르면 이 최적화는 객체 지향 프로그램의 메모리
    사용을 10%에서 20%까지 줄인다** (같은 절, p.103).
  - **이것이 [데이터 클래스 빌더](data-class-builders.md)의 각주 7이 가리키는 근거다** —
    `@dataclass` 인스턴스에 선언에 없는 속성을 나중에 붙이면 그 최적화가 무력화된다.
    같은 책의 두 장이 서로를 가리키는 자리다.
- 집합 쪽에도 같은 성격의 목록이 있다 (3장 §"Practical Consequences of How Sets Work",
  p.107):[^ramalho2022] 원소는 해시 가능해야 하고 · 멤버십 검사가 매우 효율적이며 ·
  메모리 부담이 상당하고 · **원소 순서는 삽입 순서에 달렸지만 유용하거나 신뢰할 만한
  방식은 아니며** · **집합에 원소를 더하면 기존 원소의 순서가 바뀔 수 있다. 해시 테이블이
  3분의 2 넘게 차면 알고리즘이 덜 효율적이 되므로 파이썬이 테이블을 옮기고 크기를 키워야
  할 수 있고, 그때 원소들이 다시 삽입되면서 상대 순서가 바뀔 수 있기 때문이다.**

## 집합 — 연산이 루프를 대신한다

- 정의와 기본 쓰임 — **집합은 유일한 객체들의 컬렉션이다. 기본 사용 사례는 중복 제거다**
  (3장 §"Set Theory", p.103).[^ramalho2022]
  - 순서까지 보존하고 싶으면 집합이 아니라 `dict`을 쓴다 — **첫 등장 순서를 보존하면서
    중복을 없애려면 이제 평범한 `dict`으로 할 수 있다**: `dict.fromkeys(l).keys()`
    (같은 절, p.104).
  - `set` 자체는 해시 불가능이라 **중첩 `set` 인스턴스로 집합을 지을 수 없다. 그러나
    `frozenset`은 해시 가능하므로 `set` 안에 `frozenset` 원소를 둘 수 있다**
    (같은 절, p.104).
- **이 절의 값은 표현력에 있다** — **집합 연산을 영리하게 쓰면 파이썬 프로그램의 줄 수와
  실행 시간을 둘 다 줄이면서, 루프와 조건 로직을 없애 코드를 읽고 따져 보기 쉽게 만든다**
  (3장 §"Set Theory", p.104).[^ramalho2022]
  - 실물 — 큰 주소 집합(haystack)에서 작은 집합(needles)이 몇 개 나오는지 세는 일이
    `found = len(needles & haystack)` 한 줄이 된다 (3장 예제 3-12, p.104).
  - 교환도 정확히 계상된다 — 루프 판이 **어떤 반복 가능 객체에도 동작하는 반면 교집합 판은
    둘 다 집합이어야 한다.** 손에 집합이 없으면 즉석에서 만들 수 있고
    (`len(set(needles) & set(haystack))`), **집합을 짓는 데 추가 비용이 들지만 둘 중
    하나가 이미 집합이면 그쪽이 더 쌀 수 있다** (같은 절, pp.104–105).[^ramalho2022]
  - 규모 감각도 준다 — **앞의 어느 예든 천만 항목짜리 haystack에서 천 개 원소를 약 0.3
    밀리초에 찾을 수 있다 — 원소당 0.3 마이크로초에 가깝다** (같은 절, p.105).
- 중위 연산자와 메서드의 차이에 규칙이 있다 — **중위 연산자는 두 피연산자가 모두 집합일
  것을 요구하지만, 그 밖의 모든 메서드는 하나 이상의 반복 가능 인자를 받는다.** 예컨대
  `a.union(b, c, d)`에서 `a`만 집합이면 되고 나머지는 해시 가능한 항목을 내놓는 어떤
  반복 가능 객체든 된다 (3장 §"Set Operations", p.108).[^ramalho2022]
- 문법 함정 하나 — **빈 집합에는 리터럴 표기가 없으므로 `set()`이라고 써야 한다는 것을
  기억해야 한다. `{}`라고 쓰면 빈 `dict`을 만드는 것이다**
  (3장 §"Set Literals" 곁상자, p.105).[^ramalho2022]

## 현대 문법 — 합치기와 컴프리헨션

- **딕셔너리 컴프리헨션(dictcomp)** — 파이썬 2.7부터다. **어떤 반복 가능 객체에서든
  key:value 쌍을 받아 `dict` 인스턴스를 짓는다** (3장 §"dict Comprehensions",
  p.79).[^ramalho2022] 문법이 listcomp와 같으므로
  [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md)의 컴프리헨션 규칙이 그대로 걸린다.
- **`**` 언패킹이 두 자리로 넓어졌다** (3장 §"Unpacking Mappings", p.80):[^ramalho2022]
  함수 호출에서 `**`를 인자 하나 이상에 쓸 수 있고(키가 전부 문자열이고 인자 전체에서
  유일할 때), `dict` 리터럴 안에서도 여러 번 쓸 수 있다. **후자에서는 중복 키가 허용되고
  나중 것이 앞의 것을 덮어쓴다.**
  - 버전 조건: 파이썬 3.5 이상. PEP 448이 그것을 도입했다.
- **`|`와 `|=`로 매핑을 합친다** — **파이썬 3.9가 `|`와 `|=`로 매핑을 합치는 것을 지원한다.
  이 둘이 집합 합집합 연산자이기도 하니 말이 된다** (3장 §"Merging Mappings with |",
  p.80).[^ramalho2022] `|`는 새 매핑을 만들고 `|=`는 제자리에서 갱신한다.
  - 버전 조건: 파이썬 3.9 이상. 3.8 이하에서는 PEP 584의 "Motivation" 절이 다른 방법들을
    정리한다.
- `update`의 첫 인자 처리 방식이 덕 타이핑의 교과서 예로 지목된다 — **`d.update(m)`이 첫
  인자 `m`을 다루는 방식은 덕 타이핑의 대표적 예다: 먼저 `m`이 `keys` 메서드를 갖는지
  검사하고, 가지면 그것을 매핑으로 가정한다. 그렇지 않으면 `update()`는 `m`을 반복하는
  것으로 물러서면서 그 항목이 (key, value) 쌍이라고 가정한다**
  (3장 §"Overview of Common Mapping Methods", p.87).[^ramalho2022]
  전문은 [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md)에 있다.
- 변종들의 자리도 정리돼 있다 (3장 §"Variations of dict", pp.95–97):[^ramalho2022]
  - **`OrderedDict`** — **내장 `dict`도 파이썬 3.6부터 키 순서를 유지하므로 `OrderedDict`를
    쓰는 가장 흔한 이유는 이전 파이썬 버전과 하위 호환되는 코드를 쓰는 것이다.** 남는
    차이로는 **`OrderedDict`의 동등 연산이 순서 일치를 검사한다**는 것과 `move_to_end()`,
    그리고 **잦은 재정렬 연산을 `dict`보다 잘 다루므로 최근 접근 추적(예: LRU 캐시)에
    적합하다**는 것이 있다.
  - **`ChainMap`** — **하나처럼 검색할 수 있는 매핑 리스트를 담는다. (…) 입력 매핑을
    복사하지 않고 그것들에 대한 참조를 갖는다. `ChainMap`에 대한 갱신이나 삽입은 첫 입력
    매핑에만 영향을 준다.** 중첩 스코프를 가진 언어의 인터프리터를 구현하는 데 유용하다.
  - **`Counter`** — **각 키에 대해 정수 카운트를 담는 매핑.** `most_common([n])` 등을 준다.
  - **`shelve.Shelf`** — pickle 형식으로 직렬화된 파이썬 객체에 대한 영속 키-값 저장.
    **키는 문자열이어야 하고 값은 `pickle`이 직렬화할 수 있는 객체여야 한다.**
    - **⚠ 저자가 곧바로 유보를 단다** — **파이썬의 `pickle`은 가장 단순한 경우에는 쓰기
      쉽지만 여러 단점이 있다. `pickle`을 포함하는 어떤 해법을 채택하기 전에 Ned Batchelder의
      "Pickle's nine flaws"를 읽어라** (같은 절, p.97).

## 이어지는 페이지

- [파이썬 시퀀스의 의미론](sequence-semantics-in-python.md) — 순서 있는 컬렉션 쪽.
  "튜플에 가변 항목을 넣지 마라"가 여기 해시 가능성 요구와 만나는 자리
- [객체 참조와 가변성](object-references-and-mutability.md) — 왜 가변 객체가 해시 키가
  될 수 없는가의 기제
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 인스턴스 속성을 담는 그
  `__dict__`를 아예 쓰지 않는 저장 모델과 그 대가
- [내장 타입을 상속할 때의 함정](subclassing-built-in-types.md) — `dict`이 아니라
  `UserDict`에서 만들라는 지침의 근거가 언어 구현 층에서 밝혀지는 자리
- [값 객체와 엔티티](value-objects-and-entities.md) — `__eq__`와 `__hash__`를 함께 두라는
  규칙의 도메인 쪽
- [데이터 클래스 빌더](data-class-builders.md) — 그 계약을 `eq`·`frozen` 두 옵션으로
  만족시키는 도구, 그리고 키 공유 최적화가 걸리는 각주
- [파이썬 데이터 모델](python-data-model.md) — `Mapping`·`Set` 추상 기반 클래스가 어떤
  특수 메서드로 규정되는가
- [인터페이스·프로토콜·ABC](interfaces-protocols-and-abcs.md) — `update`의 덕 타이핑과
  가상 하위 클래스 등록
- [정보 은닉과 정보 누출](information-hiding-and-leakage.md) — 읽기 전용 façade가 무엇을
  사는가의 원리 쪽
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 3장 "Dictionaries and Sets", pp.77–115(도입 p.77 ·
    §"Modern dict Syntax" pp.78–83과 그 아래 §"dict Comprehensions" p.79·
    §"Unpacking Mappings" p.80·§"Merging Mappings with |" pp.80–81·
    §"Pattern Matching with Mappings" pp.81–83 · §"Standard API of Mapping Types"
    pp.83–90과 그 아래 §"What Is Hashable" pp.84–85·§"Overview of Common Mapping Methods"
    pp.85–87·§"Inserting or Updating Mutable Values" pp.87–89 · §"Automatic Handling of
    Missing Keys" pp.90–95와 그 아래 §"defaultdict: Another Take on Missing Keys"
    pp.90–91·§"The __missing__ Method" pp.91–94·§"Inconsistent Usage of __missing__ in the
    Standard Library" pp.94–95 · §"Variations of dict" pp.95–97 · §"Subclassing UserDict
    Instead of dict" pp.97–99 · §"Immutable Mappings" pp.99–100 · §"Dictionary Views"
    pp.101–102 · §"Practical Consequences of How dict Works" pp.102–103 · §"Set Theory"
    pp.103–107과 그 아래 §"Set Literals" pp.105–107 · §"Practical Consequences of How Sets
    Work" pp.107–110과 그 아래 §"Set Operations" pp.107–110 · §"Set Operations on dict
    Views" pp.110–111 · §"Chapter Summary" p.112).
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측은
    `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    **반입하지 않은 것**: §"Pattern Matching with Mappings"의 문법 상세(pp.81–83, 제어 흐름
    문법이라 범위 밖 — 다만 없는 키 처리와 얽히는 단서 한 줄만 옮겼다). 표 3-1(매핑 메서드
    대조)·3-2~3-4(집합 연산·술어·부가 메서드)는 원문이 API 대조표라 옮기지 않고 본문
    서술로 요지만 풀었다 — 전수 목록이 필요하면 스냅샷을 본다. Figure 3-1(`MutableMapping`
    UML)·3-2(`MutableSet` UML)는 이미지로 조판돼 있어 딸린 캡션과 본문 서술만 옮겼다.
    해시 테이블의 내부 알고리즘은 저자가 2판에서 본문에서 빼 온라인 글("Internals of sets
    and dicts")로 옮긴 주제라, 이 페이지는 저자가 본문에 남긴 **실무적 귀결**만 담는다.
    코드 펜스는 예제 3-9 원문 그대로다.

---
type: concept
title: 파이썬다운 객체 만들기
description: 사용자 정의 클래스가 내장 타입처럼 굴게 만드는 특수 메서드들의 관용 구현 전범 — 개발자용 표현과 사용자용 표현을 가르는 두 함수, 대안 생성자를 클래스 메서드로 두는 관례와 staticmethod에 대한 저자의 기각, 포맷 미니 언어를 확장하는 자리, 해시 가능성이 요구하는 불변성과 그것을 읽기 전용 프로퍼티로 사는 법, 이름 뒤섞기가 보안이 아니라 안전 장치라는 규정, 클래스 속성을 인스턴스와 하위 클래스에서 덮어쓰는 두 방법, 그리고 이 모든 것을 언제 구현하지 말아야 하는가의 경계
generated: { by: "claude-opus-5", at: "2026-08-18T20:00:00Z" }
sources:
  - { id: ramalho2022, resource: /it/sources/ramalho2022.md }
---

# 파이썬다운 객체 만들기

- [무엇을 "파이썬답다"고 부르는가](#무엇을-파이썬답다고-부르는가)
- [객체 표현 — 개발자용과 사용자용](#객체-표현--개발자용과-사용자용)
- [대안 생성자와 classmethod](#대안-생성자와-classmethod)
- [포맷 미니 언어를 확장하기](#포맷-미니-언어를-확장하기)
- [해시 가능하게 만들기 — 불변성을 사 오는 값](#해시-가능하게-만들기--불변성을-사-오는-값)
- [비공개 속성과 이름 뒤섞기](#비공개-속성과-이름-뒤섞기)
- [클래스 속성을 덮어쓰는 두 방법](#클래스-속성을-덮어쓰는-두-방법)
- [언제 구현하지 않는가](#언제-구현하지-않는가)
- [프로퍼티가 인스턴스 속성을 이기는 기제](#프로퍼티가-인스턴스-속성을-이기는-기제)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **내가 만든 클래스가 파이썬의 내장 타입처럼 자연스럽게 굴게 하려면 무엇을
구현해야 하고, 어디서 멈춰야 하는가.**

이 장은 [파이썬 데이터 모델](python-data-model.md)이 세운 어휘를 하나의 클래스에서 끝까지
밀어 본 자리다. 저자의 규정 — **파이썬 데이터 모델 덕분에 당신의 사용자 정의 타입은 내장
타입만큼 자연스럽게 굴 수 있다. 그리고 이것은 상속 없이, 덕 타이핑(duck typing)의 정신으로
이뤄질 수 있다: 당신은 그저 당신의 객체가 기대대로 굴게 하는 데 필요한 메서드들을 구현하면
된다** (11장 도입, p.363).[^ramalho2022]

## 무엇을 "파이썬답다"고 부르는가

- 이 장의 경구가 그 정의를 대신한다. Martijn Faassen의 것이다 (11장 경구,
  p.363):[^ramalho2022]

> For a library or framework to be Pythonic is to make it as easy and natural as possible
> for a Python programmer to pick up how to perform a task.

- **대상이 애플리케이션이 아니라 라이브러리라는 것이 이 장의 전제다** — **당신의 애플리케이션
  클래스는 아마 이 장의 예제만큼 많은 특수 메서드를 필요로 하지 않고 구현해서도 안 된다.
  그러나 당신이 라이브러리나 프레임워크를 쓰고 있다면, 당신의 클래스를 쓸 프로그래머들은
  그것이 파이썬이 제공하는 클래스들처럼 굴기를 기대할 수 있다. 그 기대를 충족시키는 것이
  "파이썬답게" 되는 한 가지 방법이다** (11장 도입, p.363).[^ramalho2022]
- 장을 닫는 한 줄이 그 방법론이다 — **파이썬다운 객체를 지으려면 진짜 파이썬 객체가 어떻게
  구는지를 관찰하라** (11장 §"Chapter Summary", p.392).[^ramalho2022] 저자는 이 문장에
  "고대 중국 속담"이라는 출처를 농담으로 붙인다.

## 객체 표현 — 개발자용과 사용자용

- 파이썬에는 문자열 표현을 얻는 표준 방법이 둘이다 (11장 §"Object Representations",
  p.364):[^ramalho2022]
  - **`repr()` — 개발자가 보고 싶어 하는 대로 객체를 표현하는 문자열을 돌려준다. 파이썬
    콘솔이나 디버거가 객체를 보일 때 얻는 것이 그것이다.**
  - **`str()` — 사용자가 보고 싶어 하는 대로 객체를 표현하는 문자열을 돌려준다. 객체를
    `print()`할 때 얻는 것이 그것이다.**
  - 이 두 문구의 출처를 저자가 밝힌다 — 스몰토크 쪽의 1996년 글에서 빌려 왔다 (11장
    §"Further Reading", p.393).[^ramalho2022] 즉 이 구분은 파이썬의 발명이 아니다.
- 표현을 위한 특수 메서드가 넷이다 — `__repr__`·`__str__`에 더해 `__bytes__`(바이트 시퀀스
  표현, `bytes()`가 부른다)와 `__format__`(f-문자열·`format()` 내장·`str.format()`이 부른다)
  (11장 §"Object Representations", p.365).[^ramalho2022]
  - 반환 타입이 갈린다 — **파이썬 3에서 `__repr__`·`__str__`·`__format__`은 항상 유니코드
    문자열(`str` 타입)을 돌려줘야 한다. 바이트 시퀀스(`bytes` 타입)를 돌려주기로 되어 있는
    것은 `__bytes__`뿐이다** (같은 절, p.365).[^ramalho2022]
- `__repr__`을 쓰는 관용이 하나 있다 — **클래스 이름을 하드코딩하지 말고
  `type(self).__name__`에서 읽는다.** 이유가 뒤에서 밝혀진다 — **클래스 이름을
  하드코딩했다면 `ShortVector2d` 같은 `Vector2d`의 하위 클래스들이 클래스 이름을 바꾸려고
  `__repr__`을 덮어써야 했을 것이다. 인스턴스의 타입에서 이름을 읽음으로써 나는 `__repr__`을
  상속하기에 더 안전하게 만들었다** (11장 §"Overriding Class Attributes",
  p.390).[^ramalho2022]

## 대안 생성자와 classmethod

- `bytes()`로 내보낼 수 있으면 그것을 다시 읽어들이는 길도 있어야 한다. 저자는 그 이름을
  표준 라이브러리에서 빌려 온다 — `array.array`의 `.frombytes` 클래스 메서드다
  (11장 §"An Alternative Constructor", p.368).[^ramalho2022] **표준 라이브러리를 영감의
  원천으로 삼는 것**이 이 장 전체의 방법이라고 저자가 여러 번 적는다.
- `classmethod`의 규정 — **클래스에 대해 동작하고 인스턴스에 대해 동작하지 않는 메서드를
  정의하기 위한 것이다. `classmethod`는 메서드가 호출되는 방식을 바꿔서, 인스턴스 대신
  클래스 자신을 첫 인자로 받게 한다. 가장 흔한 용도는 대안 생성자다** (11장 §"classmethod
  Versus staticmethod", p.369).[^ramalho2022] 관례상 그 첫 인자의 이름이 `cls`이고,
  대안 생성자의 마지막 줄이 실제로 `cls(*memv)`처럼 그것을 불러 새 인스턴스를 만든다.
- `staticmethod`의 규정과 그에 대한 판정 — **`staticmethod` 데코레이터는 메서드가 특별한 첫
  인자를 아예 받지 않게 바꾼다. 본질적으로 정적 메서드는 모듈 수준에서 정의되는 대신 클래스
  본문 안에 사는 평범한 함수와 같다** (11장 §"classmethod Versus staticmethod",
  p.369).[^ramalho2022] 저자는 여기서 기각한다 —

> The `classmethod` decorator is clearly useful, but good use cases for `staticmethod` are
> very rare in my experience.

  - 근거는 대체 가능성이다 — 클래스를 건드리지 않는 함수라면 **같은 모듈에서 클래스 바로 앞이나
    뒤에 정의하는 것이 대개 충분히 가깝다** (같은 절, p.370).[^ramalho2022]
  - **저자가 반대 의견을 자기 각주에 실어 둔다** — 기술 검토자 Leonardo Rochael이 이 낮은
    평가에 동의하지 않고 Julien Danjou의 글을 반론으로 추천했으며, 저자는 그 글이 매우 좋다고
    인정하면서도 **"그러나 그것이 `staticmethod`에 대한 내 생각을 바꾸기에는 충분하지 않았다.
    당신 스스로 결정해야 할 것이다"**라고 적는다 (11장 각주 5, p.370).[^ramalho2022]
    - **이 KB가 이 자리를 옮긴 이유**는 판정 자체가 아니라 판정의 모양이다. 저자는 자기
      결론을 유지하면서 반대 근거의 위치를 독자에게 넘긴다 — 참조서가 규범을 말할 때 취하는
      형식이다.

## 포맷 미니 언어를 확장하기

- 기제 — **f-문자열, `format()` 내장 함수, `str.format()` 메서드는 실제 포맷팅을 각 타입에
  위임한다. 그 타입의 `.__format__(format_spec)` 메서드를 부르는 방식으로**
  (11장 §"Formatted Displays", p.370).[^ramalho2022]
- 표기법이 둘이라는 것이 이 절의 요점이다 — `'{0.mass:5.3e}'` 같은 문자열에서 콜론 왼쪽의
  `'0.mass'`는 치환 필드 문법의 `field_name` 부분이고(f-문자열에서는 임의의 식일 수 있다),
  콜론 오른쪽의 `'5.3e'`가 **포맷 명세 미니 언어(Format Specification Mini-Language)**다
  (11장 §"Formatted Displays", p.371).[^ramalho2022]
- 확장 가능성의 근거 — **포맷 명세 미니 언어는 확장 가능한데, 각 클래스가 `format_spec`
  인자를 원하는 대로 해석하기 때문이다** (같은 절, p.372).[^ramalho2022] 표준 라이브러리의
  `datetime`이 `strftime()`의 코드를 자기 `__format__`에 그대로 쓰는 것이 그 실물이다.
- `__format__`이 없으면 `object`에서 상속한 것이 `str(my_object)`를 돌려주지만, **포맷
  명세자를 넘기면 `object.__format__`은 `TypeError`를 일으킨다** (같은 절,
  p.372).[^ramalho2022] 그래서 미니 언어를 확장하려면 직접 구현해야 한다.

- `Vector2d`가 극좌표 코드 `'p'`를 더하는 구현이 그 전범이다 (11장 §"Formatted Displays"
  예제 11-6, p.373):[^ramalho2022]

  ```python
  def __format__(self, fmt_spec=''):
      if fmt_spec.endswith('p'):
          fmt_spec = fmt_spec[:-1]
          coords = (abs(self), self.angle())
          outer_fmt = '<{}, {}>'
      else:
          coords = self
          outer_fmt = '({}, {})'
      components = (format(c, fmt_spec) for c in coords)
      return outer_fmt.format(*components)
  ```

- **코드 글자를 고를 때의 지침이 붙는다** — 저자는 다른 타입이 쓰는 코드와 겹치지 않게
  골랐다고 적는다: 정수는 `'bcdoxXn'`, 부동소수는 `'eEfFgGn%'`, 문자열은 `'s'`를 쓰므로
  극좌표에 `'p'`를 골랐다. 그리고 단서 — **각 클래스가 이 코드들을 독립적으로 해석하므로 새
  타입의 맞춤 포맷에서 코드 글자를 재사용하는 것은 오류가 아니지만 사용자에게 혼란스러울 수
  있다** (11장 §"Formatted Displays", p.373).[^ramalho2022]

## 해시 가능하게 만들기 — 불변성을 사 오는 값

- 조건이 둘이다 — **`Vector2d`를 해시 가능하게 만들려면 `__hash__`를 구현해야 한다
  (`__eq__`도 필요한데 우리는 이미 갖고 있다). 우리는 또한 벡터 인스턴스를 불변으로 만들어야
  한다** (11장 §"A Hashable Vector2d", p.374).[^ramalho2022] 해시 가능성의 계약 자체는
  [딕셔너리와 집합](dictionaries-and-sets.md)에 있다.
- 불변성을 파이썬에서 사는 방법이 읽기 전용 프로퍼티다 (11장 §"A Hashable Vector2d"
  예제 11-7, p.375):[^ramalho2022]

  ```python
  class Vector2d:
      typecode = 'd'

      def __init__(self, x, y):
          self.__x = float(x)
          self.__y = float(y)

      @property
      def x(self):
          return self.__x

      @property
      def y(self):
          return self.__y

      def __iter__(self):
          return (i for i in (self.x, self.y))
  ```

- 읽는 순서가 규약이다 — **게터 메서드는 그것이 노출하는 공개 프로퍼티의 이름을 따서
  지어진다**(`x`), 그리고 저장은 밑줄 둘이 붙은 비공개 이름(`self.__x`)에 한다. 이렇게 두면
  **`x`·`y` 성분을 읽기만 하는 나머지 메서드는 전부 그대로 둬도 된다** — 비공개 속성이 아니라
  공개 프로퍼티를 읽기 때문이다 (11장 §"A Hashable Vector2d", pp.375–376).[^ramalho2022]
- `__hash__` 자체는 짧다 — **`int`를 돌려줘야 하고, `__eq__` 메서드에서도 쓰이는 객체
  속성들의 해시를 이상적으로는 고려해야 한다. 같다고 비교되는 객체는 같은 해시를 가져야 하기
  때문이다** (11장 §"A Hashable Vector2d", p.376).[^ramalho2022] 문서가 권하는 방법이
  성분들로 만든 튜플의 해시를 계산하는 것이고, 예제는 `hash((self.x, self.y))` 한 줄이다.
- **그런데 저자가 곧바로 그 강도를 낮춘다** — **해시 가능한 타입을 만드는 데 프로퍼티를
  구현하거나 인스턴스 속성을 달리 보호하는 것이 엄밀히 필요한 것은 아니다. `__hash__`와
  `__eq__`를 올바르게 구현하는 것이 전부다. 그러나 해시 가능한 객체의 값은 결코 변해서는 안
  되므로, 이것이 읽기 전용 프로퍼티를 이야기할 좋은 구실이 되었다** (11장 §"A Hashable
  Vector2d", p.376).[^ramalho2022]
  - 즉 **불변성은 언어가 강제하는 요구가 아니라 계약의 준수 수단**이다. 이 구분은
    [값 객체와 엔티티](value-objects-and-entities.md)가 도메인 쪽에서 말하는 것과 같다.
- **프로퍼티가 사 오는 진짜 값은 다른 데 있다.** 곁글이 그것을 명시한다 — **우리는 항상
  공개 속성으로 가능한 한 가장 단순한 방식으로 클래스를 시작할 수 있다. 나중에 게터·세터로
  더 많은 통제를 부과할 필요가 생기면(또는 생길 때) 그것은 프로퍼티를 통해 구현될 수 있고,
  처음에 단순한 공개 속성이었던 이름을 통해 이미 우리 객체와 상호작용하는 코드는 아무것도
  바꾸지 않는다** (11장 곁글 §"Properties Help Reduce Up-Front Costs",
  p.394).[^ramalho2022]
  - 저자가 이것을 자바와 대조한다 — **이 접근은 자바 언어가 부추기는 것의 반대다: 자바
    프로그래머는 단순한 공개 속성으로 시작해서 나중에 필요하면 프로퍼티를 구현할 수 없다.
    언어에 그것이 없기 때문이다. 그래서 게터와 세터를 쓰는 것이 자바에서는 규범이다 — 그
    메서드들이 아무 쓸모 있는 일을 하지 않을 때조차. API가 그 속성을 쓰는 모든 코드를
    깨뜨리지 않고서는 단순한 공개 속성에서 게터·세터로 진화할 수 없기 때문이다** (같은 곁글,
    p.394).[^ramalho2022]
  - 곁글은 Ward Cunningham의 물음 **"동작할 수 있는 가장 단순한 것이 무엇인가"**로 맺는다 —
    **게터·세터를 미리 구현하는 것은 목표에서 주의를 돌리는 일이다** (같은 곁글,
    p.394).[^ramalho2022]

## 비공개 속성과 이름 뒤섞기

- 파이썬에는 자바의 `private` 수식자 같은 것이 없다 — **파이썬에 있는 것은 하위 클래스에서
  "비공개" 속성이 우연히 덮어써지는 것을 막는 단순한 기제다** (11장 §"Private and
  "Protected" Attributes in Python", p.382).[^ramalho2022]
- 기제의 이름이 **이름 뒤섞기(name mangling)**다 — 인스턴스 속성을 `__mood` 형태(앞에 밑줄
  둘, 뒤에는 없거나 최대 하나)로 지으면 **파이썬은 그 이름을 앞에 밑줄과 클래스 이름을 붙여
  인스턴스 `__dict__`에 저장한다. 그래서 `Dog` 클래스에서 `__mood`는 `_Dog__mood`가 되고
  `Beagle`에서는 `_Beagle__mood`가 된다** (같은 절, p.382).[^ramalho2022]
- **규정이 이 절의 조문이다** (11장 §"Private and "Protected" Attributes in Python",
  p.382):[^ramalho2022]

> Name mangling is about safety, not security: it's designed to prevent accidental access
> and not malicious prying.

  - 뒤섞기 규칙을 아는 사람은 `v1._Vector2d__x`로 직접 읽을 수 있고 — **그것은 디버깅과
    직렬화에 실제로 유용하다** — 심지어 대입도 할 수 있다. 저자의 단서는 **"그러나 당신이
    운영 코드에서 그러고 있다면, 뭔가 터졌을 때 불평할 수 없다"**이다 (같은 절,
    p.382).[^ramalho2022]
- **이 기능이 만장일치의 지지를 받지 않는다는 것도 함께 옮겨져 있다.** pip·virtualenv의
  제작자 Ian Bicking의 말을 저자가 인용한다 (11장 §"Private and "Protected" Attributes in
  Python", p.383):[^ramalho2022]

> Never, ever use two leading underscores. This is annoyingly private. If name clashes are
> a concern, use explicit name mangling instead (e.g., `_MyThing_blahblah`). This is
> essentially the same thing as double-underscore, only it's transparent where double
> underscore obscures.

- 밑줄 하나는 언어에 아무 뜻이 없다 — **인터프리터에게 특별한 의미가 없지만, 그런 속성을
  클래스 밖에서 접근하면 안 된다는 것은 파이썬 프로그래머 사이에서 매우 강한 관례다**
  (같은 절, p.383).[^ramalho2022] 저자는 그것을 `ALL_CAPS`가 상수를 뜻하는 관례와 나란히
  둔다. 파이썬 문서 일부가 이것을 "보호된(protected)" 속성이라 부른다.
- **결론이 따옴표째로 적힌다** — **`Vector2d`의 성분은 "비공개"이고 우리 `Vector2d`
  인스턴스는 "불변"이다 — 인용 부호를 붙여서. 그것들을 정말로 비공개이고 불변으로 만들 방법이
  없기 때문이다** (11장 §"Private and "Protected" Attributes in Python",
  p.384).[^ramalho2022]
- **자바도 실은 같다는 것이 곁글의 논지다.** 저자는 Jython으로 자바 클래스의 `private` 필드를
  리플렉션으로 읽어 내는 스크립트를 보이고 이렇게 맺는다 — **내 요점은 이것이다: 자바에서도
  접근 제어 수식자는 대체로 보안이 아니라 안전에 대한 것이다, 적어도 실무에서는. 그러니 긴장을
  풀고 파이썬이 주는 힘을 즐겨라. 책임 있게 쓰라** (11장 곁글 §"Safety Versus Security in
  Private Attributes", p.396).[^ramalho2022] `SecurityManager` 아래에서 배포되는 자바
  애플리케이션은 실무에서 드물다는 것이 그 근거다.
  - 이 대비의 원리 쪽은 [정보 은닉과 정보 누출](information-hiding-and-leakage.md)에 있다 —
    그쪽도 `private` 선언과 정보 은닉이 같은 것이 아니라고 말한다.

## 클래스 속성을 덮어쓰는 두 방법

- 파이썬의 구별되는 성질 하나 — **클래스 속성이 인스턴스 속성의 기본값으로 쓰일 수 있다**
  (11장 §"Overriding Class Attributes", p.389).[^ramalho2022] `Vector2d`가 `typecode = 'd'`를
  클래스 속성으로 두고 `self.typecode`로 읽는 것이 그 실물이다.
- **방법 하나 — 인스턴스 속성으로 가리기.** 존재하지 않는 인스턴스 속성에 쓰면 새 인스턴스
  속성이 만들어지고 **같은 이름의 클래스 속성은 건드려지지 않는다. 그러나 그때부터 그
  인스턴스를 다루는 코드가 `self.typecode`를 읽으면 인스턴스 쪽이 조회되어 같은 이름의 클래스
  속성을 사실상 가린다** (같은 절, p.389).[^ramalho2022] 예제에서 `v1.typecode = 'f'`로
  바꾸면 그 인스턴스의 바이트 덤프만 17바이트에서 9바이트로 줄고 `Vector2d.typecode`는
  `'d'` 그대로다.
- **방법 둘 — 하위 클래스로 덮어쓰기.** 저자가 더 관용적이라고 부르는 쪽이다 — **더 영구적인
  효과를 얻고 그 변경에 대해 더 명시적인, 파이썬다운 방법이 있다. 클래스 속성은 공개이므로
  하위 클래스에 상속된다. 그래서 클래스 데이터 속성 하나를 맞춤 설정하려고 하위 클래스를 만드는
  것이 흔한 관행이다** (11장 §"Overriding Class Attributes", p.390).[^ramalho2022] 근거로
  드는 실물이 **장고의 클래스 기반 뷰가 이 기법을 광범위하게 쓴다**는 것이다.
  - 이것은 [상속세](inheritance-tax.md)가 경고하는 상속과 층이 다르다. 여기서 상속되는 것은
    구현이 아니라 **기본값 하나**이고, 하위 클래스는 그 값 한 줄만 갖는다.

## 언제 구현하지 않는가

이 장은 자기 예제를 스스로 기각하며 끝난다. 그 기각이 이 페이지가 이 KB에 남기는 것이다.

- **예제는 본보기가 아니다** — **예제 11-11에 코딩된 대로 `Vector2d`는 객체 표현과 관련된
  특수 메서드의 빨래 목록을 가진 교보재이지, 모든 사용자 정의 클래스를 위한 틀이 아니다**
  (11장 §"Complete Listing of Vector2d, Version 3", p.381).[^ramalho2022]
- **필요할 때만 구현하라** — **당신의 애플리케이션이 필요로 할 때에만 이 특수 메서드들을
  구현해야 한다. 최종 사용자는 애플리케이션을 이루는 객체들이 "파이썬다운"지 아닌지 신경 쓰지
  않는다. 반면 당신의 클래스가 다른 파이썬 프로그래머들이 쓸 라이브러리의 일부라면, 그들이
  당신 객체로 무엇을 할지 정말로 짐작할 수 없고 그들은 우리가 서술하고 있는 "파이썬다운" 행동을
  더 기대할 수 있다** (11장 §"Complete Listing of Vector2d, Version 3",
  p.381).[^ramalho2022]
- **판정의 기준이 문맥이라는 것을 저자가 Zen of Python으로 못 박는다** (11장 §"Chapter
  Summary", p.391):[^ramalho2022]

> An object should be as simple as the requirements dictate—and not a parade of language
> features.

  - 그 앞줄이 "단순한 것이 복잡한 것보다 낫다(Simple is better than complex)"이고, 저자는
    거기에 조건을 붙인다 — 코드가 애플리케이션을 위한 것이면 **최종 사용자를 지원하는 데
    필요한 것에 집중해야 하고 그 이상은 아니다.** 라이브러리라면 파이썬 사용자가 기대하는
    행동을 지원하는 특수 메서드를 구현하는 것이 합당하다. 저자가 드는 경계 사례가
    `__eq__`다 — **업무 요구사항을 지원하는 데 필요하지 않을 수 있지만 클래스를 테스트하기
    쉽게 만든다** (같은 절, p.391).[^ramalho2022]
- **자동화된 대안이 있다는 것도 이 장이 밝힌다** — 5장의 데이터 클래스 빌더와 `attrs`
  패키지가 여러 특수 메서드를 자동으로 붙여 준다. 그럼에도 이 장을 읽어야 하는 이유를 저자가
  적는다 — **그 특수 메서드들을 스스로 코딩할 줄 아는 것은 그 패키지들이 무엇을 하는지 이해하고,
  당신이 그것을 정말로 필요로 하는지 결정하고, 필요할 때 그것이 생성하는 메서드를 덮어쓰기
  위해 여전히 필수적이다** (11장 §"Further Reading", p.393).[^ramalho2022]

## 프로퍼티가 인스턴스 속성을 이기는 기제

위 [해시 가능하게 만들기 — 불변성을 사 오는 값](#해시-가능하게-만들기--불변성을-사-오는-값)이
읽기 전용 프로퍼티로 불변성을 사 온다고 적는데, 그것이 왜 통하는지는 같은 소스의 5부가
답한다.

- 조회가 인스턴스에서 시작하지 않는다 (22장 §"Properties Override Instance Attributes",
  p.863):[^ramalho2022]

> an expression like `obj.data` does not start the search for `data` in `obj`. The search
> actually starts at `obj.__class__`, and only if there is no property named `data` in the
> class, Python looks in the `obj` instance itself.

  - 그래서 **프로퍼티는 언제나 클래스 속성이지만, 실제로는 그 클래스의 인스턴스들에서
    속성 접근을 관리한다** (같은 절, p.861).[^ramalho2022] 이 페이지의 `Vector2d`가
    `self.__x`에 저장하고 `x` 프로퍼티로만 읽게 만들 수 있는 근거가 그것이다.
  - 그리고 읽기 전용이 공짜로 따라온다 — **세터 함수를 제공하지 않으면 `property` 클래스의
    기본 `__set__`이 그 속성이 읽기 전용임을 알리려고 `AttributeError`를 일으킨다** (23장
    §"Overriding Descriptors", p.894).[^ramalho2022]
- 더 일반적인 이름이 있다 — **이것은 오버라이딩 디스크립터 일반에 적용되며, 프로퍼티는
  그중 한 예일 뿐이다** (22장 §"Properties Override Instance Attributes",
  p.863).[^ramalho2022] 그 일반형의 정본은 [속성 디스크립터](../concepts/attribute-descriptors.md)에
  있다.
- 그 성질에 기대지 않는 캐시 데코레이터가 하나 있다는 것도 함께 알아 둘 값이 있다 —
  **`@cached_property` 데코레이터는 완전한 프로퍼티를 만들지 않고 비오버라이딩
  디스크립터를 만든다** (22장 §"Step 5: Caching Properties with functools",
  p.855).[^ramalho2022] 그래서 그것은 이 절이 말한 "이긴다"를 하지 못하고, 대신 같은
  이름의 인스턴스 속성에 결과를 써서 자기를 가려지게 만든다.
- 이 페이지의 곁글 §"Properties Help Reduce Up-Front Costs"가 말한 것 — 공개 속성으로
  시작해도 나중에 프로퍼티로 감쌀 수 있다 — 이 왜 성립하는지도 같은 기제다. 저자가 그것을
  다시 못 박는다 — **우리는 단순하게 시작해 데이터 멤버를 공개 속성으로 코딩하는 것이
  허용된다. 그것이 언제든 프로퍼티(또는 디스크립터)로 감싸질 수 있음을 알기 때문이다**
  (22장 §"Soapbox", p.876).[^ramalho2022]

## 이어지는 페이지

- [파이썬 데이터 모델](python-data-model.md) — 이 장이 딛고 선 바닥. 특수 메서드를 부르는
  것은 인터프리터라는 규칙과 두 메서드로 시퀀스가 되는 예제
- [__slots__와 인스턴스 메모리](slots-and-instance-memory.md) — 같은 장의 뒷부분. 이
  `Vector2d`의 저장 모델을 바꾸는 선언과 그 네 단서
- [시퀀스 프로토콜의 점진 구현](implementing-the-sequence-protocol.md) — 같은 클래스를 N차원
  시퀀스로 키우는 다음 장
- [파이썬의 연산자 오버로딩](operator-overloading-in-python.md) — 여기서 미룬 `+`·`*`와
  `__eq__`의 문제를 마저 푸는 자리
- [데이터 클래스 빌더](data-class-builders.md) — 이 특수 메서드들을 손으로 쓰지 않는 길
- [정보 은닉과 정보 누출](information-hiding-and-leakage.md) — `private` 선언과 정보 은닉이
  같지 않다는 원리 쪽. 이름 뒤섞기가 그 파이썬 실물이다
- [값 객체와 엔티티](value-objects-and-entities.md) — 불변성과 값 동등성을 도메인 쪽에서
  요구하는 자리
- [딕셔너리와 집합](dictionaries-and-sets.md) — 해시 가능성의 계약
- [상속세](inheritance-tax.md) — 클래스 데이터 속성 하나만 덮어쓰는 하위 클래스가 그
  경고의 어디에 서는가
- [동적 속성과 프로퍼티](dynamic-attributes-and-properties.md) — 프로퍼티의 전체 문법과
  의미론, 그리고 공개 속성으로 시작해도 된다는 판단의 정본
- [속성 디스크립터](../concepts/attribute-descriptors.md) — 프로퍼티가 그중 한 예인 오버라이딩
  디스크립터의 일반형
- [파이썬 데이터 모델과 프로토콜](../synthesis/python-data-model-and-protocols.md) —
  이 축의 허브

[^ramalho2022]: Ramalho 2022, 11장 "A Pythonic Object", pp.363–396(경구와 도입 pp.363–364 ·
    §"What's New in This Chapter" p.364 · §"Object Representations" pp.364–365 ·
    §"Vector Class Redux" pp.365–368 · §"An Alternative Constructor" p.368 ·
    §"classmethod Versus staticmethod" pp.369–370과 각주 5 · §"Formatted Displays"
    pp.370–374 · §"A Hashable Vector2d" pp.374–377 · §"Supporting Positional Pattern
    Matching" pp.377–378 · §"Complete Listing of Vector2d, Version 3" pp.378–381 ·
    §"Private and "Protected" Attributes in Python" pp.382–384 · §"Overriding Class
    Attributes" pp.389–391 · §"Chapter Summary" pp.391–392 · §"Further Reading"
    pp.392–393 · 곁글 §"Properties Help Reduce Up-Front Costs" p.394 · 곁글 §"Safety
    Versus Security in Private Attributes" pp.395–396).
    §"Saving Memory with `__slots__`" 이하 세 절(pp.384–388)의 전문은
    [__slots__와 인스턴스 메모리](slots-and-instance-memory.md)가 갖는다.
    **locator의 쪽은 인쇄판 쪽이다** — 스냅샷 PDF 쪽에서 30을 뺀 값이고, 그 오프셋 실측과
    판본 판정은 `it/archive/ramalho2022/_progress.yaml` 머리말이 정본이다.
    §"Supporting Positional Pattern Matching"(`__match_args__`와 위치 패턴)은 패턴 매칭
    문법이라 옮기지 않았다 — 이 소스의 패턴 매칭 절들을 일괄로 미룬 사유가
    `_progress.yaml`의 `skipped`에 있다. 다만 `__match_args__`가
    [__slots__와 인스턴스 메모리](slots-and-instance-memory.md)의 예제에 함께 나오는 자리는
    두 목록의 대비가 요점이라 그쪽에 남겼다.
    Figure 11-1(스위치 덮개 사진)은 이미지로 조판돼 있어 딸린 캡션의 뜻만 본문 서술로 풀었다.
    코드 펜스 둘은 예제 11-6과 예제 11-7 원문이고, 원문 코드 목록에 삽입된 조판용 번호
    표지와 예제 11-7의 생략 주석 한 줄(`# remaining methods: same as previous Vector2d`)만
    제거했다.
    §"프로퍼티가 인스턴스 속성을 이기는 기제"는 같은 소스의 22장
    §"Properties Override Instance Attributes"(pp.861–863) · §"Step 5: Caching Properties
    with functools"(p.855) · §"Soapbox"(p.876)와 23장 §"Overriding Descriptors"(p.894)에서
    합류했다.

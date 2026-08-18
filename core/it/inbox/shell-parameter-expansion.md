---
type: concept
title: 파라미터 확장
status: draft
description: 중괄호 확장 문법의 규범과 그 안에 숨은 판정들 — 콜론 유무가 "unset"과 "unset이거나 null"을 가르는 표, 기본값·대입·오류·대체값 네 형태와 그 부작용, 접두·접미 제거가 정규 표현식이 아니라 패턴 매칭이라는 것과 큰따옴표의 위치가 패턴 문자의 운명을 바꾼다는 규정, set -u가 확장을 실패시키는 자리, 그리고 word가 필요할 때만 확장된다는 규범
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 파라미터 확장

- [형태와 닫는 중괄호 찾기](#형태와-닫는-중괄호-찾기)
- [중괄호가 선택이 아닌 자리](#중괄호가-선택이-아닌-자리)
- [콜론 하나가 가르는 것](#콜론-하나가-가르는-것)
- [word는 필요할 때만 확장된다](#word는-필요할-때만-확장된다)
- [길이와 접두·접미 제거](#길이와-접두접미-제거)
- [큰따옴표의 위치가 패턴을 바꾼다](#큰따옴표의-위치가-패턴을-바꾼다)
- [set -u와의 상호작용](#set--u와의-상호작용)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **파라미터 확장(parameter expansion)의 각 형태는 언제 무엇으로 치환되며, 어떤
부작용을 남기는가.**

## 형태와 닫는 중괄호 찾기

- 기본형은 `${expression}`이고, `expression`은 **짝이 되는 `}`까지의 모든 문자**다
  (§2.6.2).[^opengroup2024-shell]
- 짝 찾기에서 제외되는 것이 규정돼 있다 (§2.6.2):[^opengroup2024-shell]

> Any `'}'` escaped by a `<backslash>` or within a quoted string, and characters in embedded
> arithmetic expansions, command substitutions, and variable expansions, shall not be examined in
> determining the matching `'}'`.

  - 스펙 자신의 예가 이것을 보여 준다: `foo=asdf; echo ${foo-bar}xyz}`는 `asdfxyz}`를 낸다
    (§2.6.2).[^opengroup2024-shell] 첫 `}`가 짝이고 둘째는 그냥 문자다.

## 중괄호가 선택이 아닌 자리

- 중괄호는 대개 선택이지만 **두 경우에는 필수다** — 두 자리 이상의 위치 파라미터일 때, 그리고
  파라미터가 이름이고 그 뒤에 이름의 일부로 해석될 수 있는 문자가 올 때
  (§2.6.2).[^opengroup2024-shell]
- 중괄호가 없으면 셸은 **가장 긴 유효한 이름**을 쓴다 — 그 이름의 변수가 존재하든 말든
  (§2.6.2).[^opengroup2024-shell] `$ab`가 `$a` 뒤에 `b`가 아니라 변수 `ab`가 되는 근거다.
  스펙의 예는 `a=1; set 2; echo ${a}b-$ab-${1}0-${10}-$10`이고 출력은 `1b--20--20`이다
  (§2.6.2).[^opengroup2024-shell]

## 콜론 하나가 가르는 것

- 규칙은 한 문장이다 (§2.6.2):[^opengroup2024-shell]

> use of the `<colon>` in the format shall result in a test for a parameter that is unset or null;
> omission of the `<colon>` shall result in a test for a parameter that is only unset.

- 스펙의 표를 그대로 옮긴다 (§2.6.2).[^opengroup2024-shell] `substitute`는 치환,
  `assign`은 파라미터에 그 값을 대입하고 그 값으로 치환한다는 뜻이다.

| 형태 | 설정됨·null 아님 | 설정됨·null | unset |
|---|---|---|---|
| `${parameter:-word}` | substitute parameter | substitute word | substitute word |
| `${parameter-word}` | substitute parameter | substitute null | substitute word |
| `${parameter:=word}` | substitute parameter | assign word | assign word |
| `${parameter=word}` | substitute parameter | substitute null | assign word |
| `${parameter:?word}` | substitute parameter | error, exit | error, exit |
| `${parameter?word}` | substitute parameter | substitute null | error, exit |
| `${parameter:+word}` | substitute word | substitute null | substitute null |
| `${parameter+word}` | substitute word | substitute word | substitute null |

- 네 형태의 성격이 서로 다르다 (§2.6.2):[^opengroup2024-shell]
  - `:-` **Use Default Values** — 치환만 하고 파라미터는 그대로다.
  - `:=` **Assign Default Values** — 파라미터에 **대입한다**(부작용이 있다). 대입되는 것은
    `word` 확장 결과에 인용 제거까지 마친 값이고, **변수에만 대입할 수 있다** — 위치
    파라미터·특수 파라미터에는 이 방식으로 대입할 수 없다.
  - `:?` **Indicate Error if Null or Unset** — 표준 오류에 쓰고 **셸이 0이 아닌 상태로
    종료한다.** 다만 대화형 셸은 종료하지 않아도 된다. 필수 변수를 강제하는 규범적 장치가
    이것이다.
  - `:+` **Use Alternative Value** — 있을 때만 대체값을 쓴다.
- `parameter`가 `*`나 `@`이면 위 네 형태의 결과는 **미지정이다**
  (§2.6.2).[^opengroup2024-shell]
- `parameter`가 `#`이고 콜론을 생략하면 `word`를 반드시 명시해야 한다 — 길이 확장과 모호해지기
  때문이다 (§2.6.2).[^opengroup2024-shell]

## word는 필요할 때만 확장된다

- 규범 문구 (§2.6.2):[^opengroup2024-shell]

> In each case that a value of `word` is needed (based on the state of `parameter`, as described
> below), `word` shall be subjected to tilde expansion, parameter expansion, command substitution,
> arithmetic expansion, and quote removal. If `word` is not needed, it shall not be expanded.

- 즉 `${x:-$(ls)}`에서 **`ls`는 `x`가 unset이거나 null일 때에만 실행된다**
  (§2.6.2).[^opengroup2024-shell] 기본값 자리에 부작용 있는 명령을 두면 그 실행 여부가 변수
  상태에 달린다.
- 이 목록에 **필드 분리와 경로명 확장이 없다는 점**을 눈여겨볼 것. `word`의 확장은 그 둘을
  거치지 않는다.

## 길이와 접두·접미 제거

- `${#parameter}`는 값의 **문자 수**의 십진 표기다 (§2.6.2).[^opengroup2024-shell] 바이트 수가
  아니다. `parameter`가 `*`나 `@`이면 결과는 미지정이다.
- 접두·접미 제거 네 형태는 **정규 표현식이 아니라 패턴 매칭 표기**를 쓴다
  (§2.6.2).[^opengroup2024-shell] 문법은 [경로명 확장](shell-pathname-expansion.md)이 쓰는 것과
  같다(§2.14).

| 형태 | 뜻 | 스펙의 예 |
|---|---|---|
| `${parameter%word}` | 가장 짧은 접미 제거 | `x=file.c; echo ${x%.c}.o` → `file.o` |
| `${parameter%%word}` | 가장 긴 접미 제거 | `x=posix/src/std; echo ${x%%/*}` → `posix` |
| `${parameter#word}` | 가장 짧은 접두 제거 | `x=$HOME/src/cmd; echo ${x#$HOME}` → `/src/cmd` |
| `${parameter##word}` | 가장 긴 접두 제거 | `x=/one/two/three; echo ${x##*/}` → `three` |

- `word`를 생략하면 **빈 패턴**을 쓴다 (§2.6.2).[^opengroup2024-shell]
- `%` 형태의 `word`는 인용되지 않은 `%`로 시작하면 안 되고, `#` 형태도 마찬가지다
  (§2.6.2).[^opengroup2024-shell]
- `parameter`가 `#`·`*`·`@`이면 결과는 미지정이다 (§2.6.2).[^opengroup2024-shell]

## 큰따옴표의 위치가 패턴을 바꾼다

- 이 네 형태에만 적용되는 특수 규칙이다 (§2.6.2):[^opengroup2024-shell]

> Enclosing the full parameter expansion string in double-quotes shall not cause the following four
> varieties of pattern characters to be quoted, whereas quoting characters within the braces shall
> have this effect.

- 스펙이 붙인 대조가 이 규칙의 전부다 (§2.6.2):[^opengroup2024-shell]
  - `"${x#*}"` — 별표는 **패턴 문자**다.
  - `${x#"*"}` — 별표는 인용됐으므로 **보통 문자**다.
- 즉 바깥 큰따옴표는 패턴을 문자로 만들지 못한다. 안쪽에서 인용해야 한다. 이것은
  [셸 인용](shell-quoting.md)의 §2.2.3 규정과도 맞물린다 — 부분 문자열 처리 네 형태 안에서는
  바깥 큰따옴표가 특수 문자 처리에 아무 영향을 주지 않는다.

## set -u와의 상호작용

- `set -u`의 규정 (§2.15 set):[^opengroup2024-shell]

> When the shell tries to expand, in a parameter expansion or an arithmetic expansion, an unset
> parameter other than the `'@'` and `'*'` special parameters, it shall write a message to standard
> error and the expansion shall fail with the consequences specified in 2.8.1 Consequences of Shell
> Errors.

- **`@`와 `*`는 예외다** — 인자가 없다고 `set -u`가 걸리지 않는다.
- 실패의 등급이 "확장 오류(expansion error)"이므로 비대화형 셸은 **종료한다**
  ([셸 오류의 귀결](shell-error-consequences.md)).
- `${#parameter}`와 부분 문자열 처리 네 형태는 `parameter`가 unset이고 `set -u`가 켜져 있으면
  **확장이 실패한다**고 §2.6.2가 따로 못 박는다.[^opengroup2024-shell] 반면 `${x:-default}`
  계열은 unset을 검사하는 것이 그 형태의 목적이므로 이 실패의 대상이 아니다.
  - 버전 조건: Open Group Base Specifications Issue 8 부터 — 이 판본이 `-u`의 서술을 바꿨다
    (`set` 절의 변경 이력이 `Austin Group Defect 559 is applied, changing the description of the
    -u option`이라 적는다).

## 이어지는 페이지

- [단어 확장의 순서](shell-word-expansion-order.md) — 이 확장이 도는 자리
- [위치 파라미터와 특수 파라미터](shell-special-parameters.md) — 이름이 아닌 파라미터들
- [경로명 확장](shell-pathname-expansion.md) — 접두·접미 제거가 빌려 쓰는 패턴 문법
- [셸 오류의 귀결](shell-error-consequences.md) — 확장 실패가 셸을 죽이는 자리
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.6.2 Parameter Expansion(표와 예는 그 절의
    Examples — 원문이 "informative"로 표시한 구간이다), §2.14 Pattern Matching Notation,
    §2.15 Special Built-In Utilities의 `set`(`-u`와 CHANGE HISTORY).

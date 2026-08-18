---
type: concept
title: 위치 파라미터와 특수 파라미터
description: 특수 파라미터 at과 asterisk가 왜 다르고 왜 인용과 결합해야만 뜻이 정해지는가 — 큰따옴표 밖에서는 둘이 같고 안에서는 갈린다는 규범, 인용하지 않으면 빈 필드가 버려질 수 있다는 규정, 위치 파라미터가 두 자리 이상이면 중괄호가 필수라는 규칙, 물음표 파라미터가 가리키는 것이 직전 파이프라인이라는 정의와 명령 치환이 그 값을 어떻게 바꾸는가, 그리고 나머지 특수 파라미터의 규정
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 위치 파라미터와 특수 파라미터

- [위치 파라미터 — 두 자리부터는 중괄호가 필수다](#위치-파라미터--두-자리부터는-중괄호가-필수다)
- [인용 안에서만 갈라진다](#인용-안에서만-갈라진다)
- [인용하지 않으면 빈 필드가 버려질 수 있다](#인용하지-않으면-빈-필드가-버려질-수-있다)
- [인자가 없을 때](#인자가-없을-때)
- [물음표 파라미터 — 직전 파이프라인의 종료 상태](#물음표-파라미터--직전-파이프라인의-종료-상태)
- [나머지 특수 파라미터](#나머지-특수-파라미터)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인자 목록을 넘길 때 `$@`와 `$*` 중 무엇을 어떻게 인용해야 뜻이 정해지는가.**

특수 파라미터(special parameters)는 이름이 아니라 기호로 표시되는 파라미터다
(§2.5).[^opengroup2024-shell] 그중 `@`와 `*`는 [인용](../concepts/shell-quoting.md)·
[필드 분리](../concepts/shell-field-splitting.md)와 셋이 얽혀야 뜻이 정해지고, 그래서 셋 중 하나만 알고
쓰면 틀린다.

## 위치 파라미터 — 두 자리부터는 중괄호가 필수다

- 위치 파라미터(positional parameter)는 양의 정수의 십진 표기로 표시되는 파라미터이고, **자리가
  둘 이상이면 애플리케이션이 중괄호로 감싸야 한다** (§2.5.1).[^opengroup2024-shell]
- 스펙이 든 예가 함정을 그대로 보여 준다 (§2.5.1):[^opengroup2024-shell]

> `"$8"`, `"${8}"`, `"${08}"`, `"${008}"`, etc. all expand to the value of the eighth positional
> parameter. `"${10}"` expands to the value of the tenth positional parameter. `"$10"` expands to
> the value of the first positional parameter followed by the character `'0'`.

  - `$10`은 열째 인자가 아니라 **첫째 인자 뒤에 문자 `0`**이다. 조용히 틀리는 종류의 오류다.
- `0`은 위치 파라미터가 아니라 특수 파라미터다. 그래서 `${00}`의 확장 결과는 미지정이다
  (§2.5.1).[^opengroup2024-shell]
- 위치 파라미터는 셸이 시작할 때 배정되고, **함수가 호출되는 동안 임시로 대치되며**,
  `set` 특수 내장 유틸리티로 다시 배정할 수 있다 (§2.5.1).[^opengroup2024-shell]

## 인용 안에서만 갈라진다

둘의 시작은 같다. 규범 문구가 두 항목에서 **글자 그대로 같은 문장**으로 시작한다
(§2.5.2):[^opengroup2024-shell]

> Expands to the positional parameters, starting from one, initially producing one field for each
> positional parameter that is set. When the expansion occurs in a context where field splitting
> will be performed, any empty fields may be discarded and each of the non-empty fields shall be
> further split as described in 2.6.5 Field Splitting.

- **필드 분리가 도는 자리에서는 `$@`와 `$*`가 같다.** 인용 없이 쓰면 둘 다 같은 손상을 입는다.
  둘의 차이는 인용 안에서만 나타난다.
- `*`의 인용 안 동작 (§2.5.2):[^opengroup2024-shell]

> When the expansion occurs in a context where field splitting will not be performed, the initial
> fields shall be joined to form a single field with the value of each parameter separated by the
> first character of the `IFS` variable if `IFS` contains at least one character, or separated by a
> `<space>` if `IFS` is unset, or with no separation if `IFS` is set to a null string.

  - `"$*"`는 **한 필드**가 되고, 이음쇠는 `IFS`의 **첫 문자**다. `IFS`가 빈 문자열이면 구분 없이
    붙는다 — 인자 경계가 사라진다.
- `@`의 인용 안 동작은 조건부다. 큰따옴표 안에서 `"$@"`의 동작은 **두 조건 중 하나가 참일
  때에만 정의된다** (§2.5.2):[^opengroup2024-shell] 큰따옴표가 없었다면 필드 분리가 수행될
  자리이거나, 그 큰따옴표가 `${parameter:-word}`·`${parameter:+word}`의 `word` 안에 있는
  경우다. **그 밖의 맥락에서는 결과가 미지정이다.**
- 조건이 맞으면 (§2.5.2):[^opengroup2024-shell]

> If one of these conditions is true, the initial fields shall be retained as separate fields,
> except that if the parameter being expanded was embedded within a word, the first field shall be
> joined with the beginning part of the original word and the last field shall be joined with the
> end part of the original word.

  - **`"$@"`만이 인자 하나하나를 원래 경계 그대로 보존한다.** 단어 안에 박혀 있으면 첫 필드와
    끝 필드가 주변 텍스트에 붙는다 — `"pre$@post"` 같은 표기가 하는 일이 그것이다.

## 인용하지 않으면 빈 필드가 버려질 수 있다

- 위 공통 문장의 `any empty fields may be discarded`가 규범 어휘로 `may`라는 점이 중요하다
  (§2.5.2).[^opengroup2024-shell] **버려도 되고 안 버려도 된다** — 구현에 따라 다를 수 있는
  자리이므로 인용하지 않은 `$@`·`$*`로 빈 인자를 전달하려는 시도는 애초에 이식성이 없다.
- 그다음 절이 비어 있지 않은 필드도 **더 쪼갠다**고 못 박으므로, 공백이 든 인자는 인용 없이는
  반드시 갈라진다([필드 분리와 IFS](../concepts/shell-field-splitting.md)).

## 인자가 없을 때

- 규범 문구 (§2.5.2):[^opengroup2024-shell]

> If there are no positional parameters, the expansion of `'@'` shall generate zero fields, even
> when `'@'` is within double-quotes

- **`"$@"`는 인자가 없으면 필드 영 개다** — 빈 문자열 인자 하나가 아니다. 이것이 `"$@"`를 명령
  뒤에 붙여도 안전한 이유다.
- 다만 같은 단어 안에 인용된 널 문자열로 확장되는 다른 부분이 있으면 그 널 문자열들은 여전히
  빈 필드를 만든다. 그 다른 부분들이 전부 `@`와 같은 큰따옴표 안에 있으면 결과가 필드 영 개인지
  빈 필드 하나인지는 **미지정이다** (§2.5.2).[^opengroup2024-shell]
- `for` 루프에서 `in` 목록을 생략하면 `in "$@"`와 같다 (§2.9.4.2).[^opengroup2024-shell]
  기본값이 인용된 `"$@"`라는 점이 이 설계의 방향을 말해 준다.

## 물음표 파라미터 — 직전 파이프라인의 종료 상태

- 정의가 생각보다 좁다 (§2.5.2):[^opengroup2024-shell]

> Expands to the shortest representation of the decimal exit status of the pipeline executed from
> the current shell execution environment (not a subshell environment) that most recently either
> terminated or … was stopped by a signal.

- 단위가 명령이 아니라 **파이프라인**이고, 범위가 **현재 셸 실행 환경**이다. 서브셸에서 돈
  명령의 상태가 아니다.
- 값은 셸 초기화 때 0으로 설정되고, 서브셸 환경이 만들어질 때 호출한 환경의 `?` 값이
  서브셸에 보존된다 (§2.5.2).[^opengroup2024-shell]
- 스펙이 붙인 주석이 흔한 오해를 미리 푼다 (§2.5.2):[^opengroup2024-shell]

> In `var=$(some_command); echo $?` the output is the exit status of `some_command`, which is
> executed in a subshell environment, but this is because its exit status becomes the exit status
> of the assignment command `var=$(some_command)` … and this assignment command is the most
> recently completed pipeline.

  - 즉 서브셸의 상태를 직접 읽는 것이 아니라 **대입 명령의 상태를 읽는 것**이고, 그 대입 명령의
    상태가 명령 치환에서 온다. 명령 이름이 없는 단순 명령의 규정이 그것을 정한다
    ([종료 상태](../concepts/shell-exit-status.md)).

## 나머지 특수 파라미터

전부 §2.5.2의 규정이다.[^opengroup2024-shell]

| 기호 | 무엇으로 확장되는가 | 주의 |
|---|---|---|
| `#` | 위치 파라미터의 개수 | 파라미터 0은 세지 않는다 — 특수 파라미터이지 위치 파라미터가 아니다 |
| `-` | 현재 옵션 플래그를 이어 붙인 문자열 | `-c`·`-s`가 포함되는지는 미지정. 대화형이면 `-i`는 반드시 포함 |
| `$` | 호출된 셸의 프로세스 ID | **서브셸에서도 현재 셸과 같은 값이다** |
| `!` | 가장 최근 비동기 AND-OR 목록의 프로세스 ID | `bg`로 재개된 작업의 마지막 명령 쪽이 더 최근이면 그쪽 |
| `0` | 셸 또는 셸 스크립트의 이름 | 함수 실행 중에도 바뀌지 않는다(§2.9.5) |

- `$`가 서브셸에서도 부모와 같다는 것이 특히 함정이다 — 임시 파일 이름을 `$$`로 지으면 서브셸이
  같은 이름을 짓는다. `PPID`도 같은 성질이다(**In a subshell, `PPID` shall be set to the same
  value as that of the parent of the current shell**, §2.5.3).[^opengroup2024-shell]

## 이어지는 페이지

- [셸 인용 — 무엇이 확장을 막는가](../concepts/shell-quoting.md) — `"$@"`의 큰따옴표가 하는 일
- [필드 분리와 IFS](../concepts/shell-field-splitting.md) — 인용하지 않았을 때 일어나는 일
- [파라미터 확장](../concepts/shell-parameter-expansion.md) — `${...}` 문법 전체
- [종료 상태](../concepts/shell-exit-status.md) — `$?`가 읽는 값이 어떻게 정해지는가
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.5 Parameters and Variables, §2.5.1 Positional
    Parameters, §2.5.2 Special Parameters, §2.5.3 Shell Variables(`PPID`), §2.9.4.2 The for Loop,
    §2.9.5 Function Definition Command.

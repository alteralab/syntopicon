---
type: concept
title: 경로명 확장 — 글로빙의 규범
description: 글로브 패턴이 파일 이름으로 바뀌는 단계의 규범과 그 함정 — 맞는 파일이 없으면 패턴 문자열이 그대로 남는다는 규정, 선행 점과 슬래시가 특수 문자에 잡히지 않는다는 두 예외, 권한 오류를 오류로 치지 않고 진행한다는 규정, 정렬이 로케일의 대조 순서를 따른다는 것, 그리고 패턴 매칭이 정규 표현식이 아니라는 구분
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 경로명 확장 — 글로빙의 규범

- [단계의 정의](#단계의-정의)
- [맞는 것이 없으면 패턴이 그대로 남는다](#맞는-것이-없으면-패턴이-그대로-남는다)
- [패턴 매칭은 정규 표현식이 아니다](#패턴-매칭은-정규-표현식이-아니다)
- [파일 이름에만 걸리는 세 예외](#파일-이름에만-걸리는-세-예외)
- [권한 오류는 오류가 아니다](#권한-오류는-오류가-아니다)
- [정렬은 로케일이 정한다](#정렬은-로케일이-정한다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **글로브 패턴은 언제 파일 이름이 되고, 되지 못했을 때 무엇이 남는가.**

## 단계의 정의

- 규범 전문이 한 문장이다 (§2.6.6):[^opengroup2024-shell]

> After field splitting, if `set -f` is not in effect, each field in the resulting command line
> shall be expanded using the algorithm described in 2.14 Pattern Matching Notation, qualified by
> the rules in 2.14.3 Patterns Used for Filename Expansion.

- 순서가 못 박혀 있다 — **필드 분리 다음이다.** 그러니 확장 결과에 있던 `*`는 이미 쪼개진 뒤에
  파일 이름 후보로 해석된다([단어 확장의 순서](shell-word-expansion-order.md)).
- 끄는 스위치는 `set -f`(= `set -o noglob`)이고, 그 규정은 한 줄이다 — **The shell shall disable
  pathname expansion** (§2.15 set).[^opengroup2024-shell]

## 맞는 것이 없으면 패턴이 그대로 남는다

- 경로명 확장(pathname expansion)에서 가장 자주 문제가 되는 규범이다
  (§2.14.3):[^opengroup2024-shell]

> If the pattern does not match any existing filenames or pathnames, the pattern string shall be
> left unchanged.

- 실패가 오류가 아니라 **문자열 통과**다. `*.txt`에 맞는 파일이 없으면 명령은 인자로 문자 그대로
  `*.txt`를 받는다. 그 인자를 파일 이름으로 여는 다음 도구가 "그런 파일 없음"으로 실패하고,
  그때 나오는 진단 메시지는 원인을 가리키지 않는다.
- 특수 문자가 아예 없는 패턴도 그대로 남는다 — 즉 `*`·`?`·`[`가 없으면 매칭 자체를 하지 않는다
  (§2.14.3).[^opengroup2024-shell]
- 반대로 맞는 것이 있으면 패턴은 **여러 필드로 대치된다** (§2.14.3).[^opengroup2024-shell]
  단어 하나가 여럿이 되는 셋째 경로가 이것이다([단어 확장의 순서](shell-word-expansion-order.md)).

## 패턴 매칭은 정규 표현식이 아니다

- 스펙이 관계를 직접 정리한다 (§2.14):[^opengroup2024-shell]

> Historically, pattern matching notation is related to, but slightly different from, the regular
> expression notation described in XBD 9. Regular Expressions.

- 특수 문자는 셋뿐이다 — `?`(임의의 한 문자), `*`(여러 문자), `[`(대괄호 식)
  (§2.14.1).[^opengroup2024-shell] 정규 표현식의 `.`·`+`·`|`는 여기 없다.
- 대괄호 식에서 부정은 `^`가 아니라 `!`다. **인용되지 않은 `^`로 시작하는 대괄호 식의 결과는
  미지정이다** (§2.14.1).[^opengroup2024-shell]
- `*`는 탐욕적이다 — **matching the greatest possible number of characters that still allows the
  remainder of the pattern to match** (§2.14.2).[^opengroup2024-shell]
- 매칭은 문자의 그래픽 표현이 아니라 **인코딩된 비트 패턴을 기준으로** 한다
  (§2.14.1).[^opengroup2024-shell] 유효한 문자를 이루지 않는 바이트가 든 문자열을 패턴 매칭에
  쓰면 동작은 미지정이고, 그래서 스펙은 임의의 경로명을 다룰 때 로케일을 C나 POSIX로 두라고
  권한다 (§2.14).[^opengroup2024-shell]

## 파일 이름에만 걸리는 세 예외

§2.14.3이 §2.14.1·§2.14.2의 일반 규칙에 덧붙이는 제약이다.

- **슬래시는 명시적으로만 맞는다** (§2.14.3):[^opengroup2024-shell]

> The `<slash>` character in a pathname shall be explicitly matched by using one or more `<slash>`
> characters in the pattern; it shall neither be matched by the `<asterisk>` or `<question-mark>`
> special characters nor by a bracket expression.

  - 그래서 `*`는 디렉터리 경계를 넘지 못한다. 스펙이 든 예는 `a[b/c]d`이고, 이것은 `abd`나
    `a/d`가 아니라 **문자 그대로 `a[b/c]d`라는 경로명 하나만** 맞는다 —
    슬래시가 대괄호 식보다 먼저 식별되므로 여는 대괄호가 보통 문자가 되기 때문이다.
- **선행 점도 명시적으로만 맞는다** (§2.14.3).[^opengroup2024-shell] 파일 이름이 `.`로 시작하면
  패턴의 첫 문자(또는 슬래시 바로 뒤)가 `.`여야 한다. `*`·`?`는 물론이고 `[!a]` 같은 부정
  목록, `[%-0]` 같은 범위, `[[:punct:]]` 같은 문자 클래스도 선행 점을 잡지 못한다.
  - 대괄호 매칭 목록에 점을 명시한 `[.abc]`가 선행 점을 잡는지는 **미지정이다**
    (§2.14.3).[^opengroup2024-shell]
- 대괄호 식이 되다 만 `[`가 있으면 **같은 경로 성분 안의 다른 `*`·`?`·`[`·백슬래시가 특수
  의미를 유지하는지는 미지정이다** (§2.14.3).[^opengroup2024-shell] 스펙 자신이 `a*[/b*`를 두
  가지로 해석할 수 있다고 적는다.

## 권한 오류는 오류가 아니다

- 이 규정이 조용한 실패의 근거다 (§2.14.3):[^opengroup2024-shell]

> If these permissions are denied, or if an attempt to open or search a pathname as a directory, or
> an attempt to read an opened directory, fails because of an error condition that is related to
> file system contents, this shall not be considered an error and pathname expansion shall continue
> as if the pathname had named an existing directory which had been successfully opened and read,
> or searched, and no matching directory entries had been found in it.

- 읽을 수 없는 디렉터리는 **비어 있는 것처럼 취급된다.** 그래서 권한 문제로 파일을 못 본 것과
  파일이 없는 것을 확장 결과만으로 구분할 수 없다. 그 밖의 오류 조건에서 확장이 실패하는지 아니면
  같게 취급되는지는 미지정이다 (§2.14.3).[^opengroup2024-shell]
- 어떤 권한이 필요한지도 규정돼 있다: 특수 문자가 든 성분은 그 성분을 담은 디렉터리에 대한 읽기
  권한, 마지막을 뺀 나머지 성분은 검색 권한이다 (§2.14.3).[^opengroup2024-shell] 스펙의 예는
  `/foo/bar/x*/bam`이고, `/`와 `foo`에는 검색, `bar`에는 검색과 읽기, 각 `x*` 디렉터리에는
  검색 권한이 필요하다.

## 정렬은 로케일이 정한다

- 규범 문구 (§2.14.3):[^opengroup2024-shell]

> If the pattern matches any existing filenames or pathnames, the pattern shall be replaced with
> those filenames and pathnames, sorted according to the collating sequence in effect in the
> current locale.

- **즉 글로브의 결과 순서는 로케일 종속이다.** 대조 순서에 전순서가 없으면 같게 대조되는
  이름들만 POSIX 로케일의 대조 순서로 바이트 단위 비교해 정한다 (§2.14.3).[^opengroup2024-shell]
- 그래서 "파일이 알파벳 순으로 들어온다"에 기대는 스크립트는 로케일이 바뀌면 다르게 돈다.
  결정적 순서가 필요하면 로케일을 고정하는 것이 이 문서가 지지하는 방법이다.
- `.`과 `..` 항목은 무시될 수 **있다**(`may be ignored`) — 즉 지금은 보장이 아니다.
  스펙은 미래 판본이 이것을 요구할 수 있다는 주석을 붙인다 (§2.14.3).[^opengroup2024-shell]

## 이어지는 페이지

- [단어 확장의 순서](shell-word-expansion-order.md) — 이 단계의 자리
- [필드 분리와 IFS](../concepts/shell-field-splitting.md) — 이 단계 바로 앞
- [셸 인용 — 무엇이 확장을 막는가](shell-quoting.md) — 패턴 문자를 보통 문자로 만드는 방법
- [파라미터 확장](../concepts/shell-parameter-expansion.md) — 같은 패턴 문법을 접두·접미 제거에 쓰는 자리
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.6.6 Pathname Expansion, §2.14 Pattern Matching
    Notation, §2.14.1 Patterns Matching a Single Character, §2.14.2 Patterns Matching Multiple
    Characters, §2.14.3 Patterns Used for Filename Expansion, §2.15 Special Built-In Utilities의
    `set`(`-f`).

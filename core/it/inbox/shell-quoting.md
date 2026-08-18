---
type: concept
title: 셸 인용 — 무엇이 확장을 막는가
status: draft
description: POSIX 셸의 네 가지 인용 기법이 각각 무엇을 막고 무엇을 막지 못하는지 — 반드시 인용해야 하는 문자 목록과 "조건부로 특별한" 문자에 붙은 should 권고, 백슬래시가 개행에서만 예외인 이유, 작은따옴표가 자기 자신을 담지 못한다는 제약, 큰따옴표 안에서 살아남는 세 문자와 확장 결과의 문자값이 보존된다는 규범, 그리고 인용 제거가 확장의 맨 끝에 오는 순서
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 셸 인용 — 무엇이 확장을 막는가

- [인용이 하는 일](#인용이-하는-일)
- [반드시 인용할 문자와 조건부로 특별한 문자](#반드시-인용할-문자와-조건부로-특별한-문자)
- [백슬래시 — 개행만이 예외다](#백슬래시--개행만이-예외다)
- [작은따옴표 — 가장 강한 인용, 그러나 자기 자신은 못 담는다](#작은따옴표--가장-강한-인용-그러나-자기-자신은-못-담는다)
- [큰따옴표 — 세 문자만 살아남는다](#큰따옴표--세-문자만-살아남는다)
- [달러-작은따옴표 — Issue 8에서 규범이 된 넷째 기법](#달러-작은따옴표--issue-8에서-규범이-된-넷째-기법)
- [인용 제거는 맨 끝에 온다](#인용-제거는-맨-끝에-온다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인용(quoting)은 셸의 어떤 처리를 막고, 어떤 처리는 막지 못하는가.**

인용을 "따옴표를 붙여 두면 안전하다"로 요약하면 절반이 틀린다. 큰따옴표는 확장(expansion)을
막지 않고, 작은따옴표는 자기 자신을 담지 못하며, 백슬래시는 개행 앞에서만 다르게 군다. 그 셋의
경계가 어디인지가 이 페이지의 내용이다.

## 인용이 하는 일

- 스펙 자신의 정의는 세 가지 효과를 나란히 든다 (§2.2):[^opengroup2024-shell]

> Quoting is used to remove the special meaning of certain characters or words to the shell.
> Quoting can be used to preserve the literal meaning of the special characters in the next
> paragraph, prevent reserved words from being recognized as such, and prevent parameter
> expansion and command substitution within here-document processing.

- 그러니까 인용이 막는 것은 **특별한 의미**이지 확장 자체가 아니다. 확장을 실제로 막는 것은
  작은따옴표(와 달러-작은따옴표)이고, 큰따옴표는 확장을 **허용하면서** 그 결과에 대해서만
  분리를 막는다 — 아래 [큰따옴표](#큰따옴표--세-문자만-살아남는다) 절이 그 규범 문구다.
- 인용 기법은 넷이고, 히어 도큐먼트(here-document)가 다섯째 형태로 언급된다 (§2.2):
  이스케이프 문자, 작은따옴표, 큰따옴표, 달러-작은따옴표.[^opengroup2024-shell]

## 반드시 인용할 문자와 조건부로 특별한 문자

- 애플리케이션이 **반드시** 인용해야 하는 문자 목록이다 — 자기 자신을 뜻하게 하려면
  (§2.2):[^opengroup2024-shell]

> The application shall quote the following characters if they are to represent themselves:
> `` |  &  ;  <  >  (  )  $  `  \  "  '  <space>  <tab>  <newline> ``

- 그 아래 둘째 목록은 **조건부**다 — `*  ?  [  ]  ^  -  !  #  ~  =  %  {  ,  }`. 스펙의 표현은
  "these characters are sometimes special depending on conditions described elsewhere"다
  (§2.2).[^opengroup2024-shell]
- **둘째 목록에 붙은 규범 조동사는 `should`다.** 요구가 아니라 권고이고, 이유가 미래 판본이다
  (§2.2):[^opengroup2024-shell]

> A future version of this standard may extend the conditions under which these characters are
> special. Therefore applications should quote them whenever they are intended to represent
> themselves. This does not apply to `<hyphen-minus>` (`'-'`) since it is in the portable
> filename character set.

  - 이것이 규범 조동사 등급이 실제로 갈리는 자리다. 첫 목록은 `shall`(요구), 둘째 목록은
    `should`(권고), 하이픈은 아예 예외. 세 등급을 "인용해라" 한 마디로 뭉개면 이 문서가 무엇을
    보장하고 무엇을 보장하지 않는지가 사라진다.

## 백슬래시 — 개행만이 예외다

- 규범 전문이 짧다 (§2.2.1):[^opengroup2024-shell]

> A `<backslash>` that is not quoted shall preserve the literal value of the following character,
> with the exception of a `<newline>`. If a `<newline>` immediately follows the `<backslash>`, the
> shell shall interpret this as line continuation. The `<backslash>` and `<newline>` shall be
> removed before splitting the input into tokens. Since the escaped `<newline>` is removed
> entirely from the input and is not replaced by any white space, it cannot serve as a token
> separator.

- 마지막 문장이 함정의 자리다 — 줄 이음의 `\`+개행은 **공백으로 바뀌지 않고 통째로 사라진다.**
  그래서 접힌 두 줄의 끝과 시작이 붙어 한 토큰이 된다. 긴 명령을 `\`로 접을 때 앞줄 끝이나
  뒷줄 앞에 공백을 두어야 하는 근거가 여기다.

## 작은따옴표 — 가장 강한 인용, 그러나 자기 자신은 못 담는다

- 규범 전문이 두 문장이다 (§2.2.2):[^opengroup2024-shell]

> Enclosing characters in single-quotes (`''`) shall preserve the literal value of each character
> within the single-quotes. A single-quote cannot occur within single-quotes.

- 예외가 하나도 없다는 것이 이 기법의 성질이다. 확장도, 명령 치환도, 백슬래시 이스케이프도
  안쪽에서는 일어나지 않는다. 대가는 둘째 문장이다 — **작은따옴표 자신을 넣을 방법이 없다.**
  문자열에 `'`가 들어가야 하면 다른 기법으로 넘어가야 한다.

## 큰따옴표 — 세 문자만 살아남는다

- 규범 문구 (§2.2.3):[^opengroup2024-shell]

> Enclosing characters in double-quotes (`""`) shall preserve the literal value of all characters
> within the double-quotes, with the exception of the characters backquote, `<dollar-sign>`, and
> `<backslash>`, as follows:

- 즉 큰따옴표 안에서 `` ` ``·`$`·`\` 셋은 여전히 특별하다. `$`는 파라미터 확장·명령 치환·산술
  확장을 여는 의미를 **유지하고**, 다만 달러-작은따옴표를 여는 의미는 잃는다
  (§2.2.3).[^opengroup2024-shell]
- **이 페이지에서 가장 많이 쓰일 한 문장**이다 — 왜 `"$var"`가 안전한가에 대한 규범적 답
  (§2.2.3):[^opengroup2024-shell]

> When double-quotes are used to quote a parameter expansion, command substitution, or arithmetic
> expansion, the literal value of all characters within the result of the expansion shall be
> preserved.

  - 큰따옴표는 **확장을 막는 것이 아니라 확장 결과의 문자값을 보존한다.** 그래서 확장은
    일어나되 그 결과가 다시 필드로 쪼개지거나 글로브 패턴으로 해석되지 않는다. 기제는
    [필드 분리와 IFS](shell-field-splitting.md)에 있다 — 분리 대상이 "큰따옴표 안에서 일어나지
    않은 확장 결과"로 한정돼 있다.
- 큰따옴표 안의 `\`는 아무 문자나 이스케이프하지 못한다. `"$(...)"`와 `"${...}"` 밖에서는
  다음 문자가 `$`·`` ` ``·`\`·개행일 때만(또는 특별하게 취급될 큰따옴표일 때만) 이스케이프
  문자로 남는다 (§2.2.3).[^opengroup2024-shell] 그 밖의 자리에서 `\`는 그냥 백슬래시 문자다.
- 큰따옴표 자신을 큰따옴표 안에 넣으려면 `\`가 필요하다 — 단 `$(...)`나 `${...}` 안이면
  아니다 (§2.2.3).[^opengroup2024-shell]
- `@`는 큰따옴표 안에서 특별한 의미를 가진다고 이 절이 명시하고, 그 규정을 §2.5.2로 넘긴다
  (§2.2.3).[^opengroup2024-shell] 그 자리가
  [위치 파라미터와 특수 파라미터](shell-special-parameters.md)다.

## 달러-작은따옴표 — Issue 8에서 규범이 된 넷째 기법

- 형태와 효과 (§2.2.4):[^opengroup2024-shell]

> A sequence of characters starting with a `<dollar-sign>` immediately followed by a single-quote
> (`$'`) shall preserve the literal value of all characters up to an unescaped terminating
> single-quote (`'`), with the exception of certain `<backslash>`-escape sequences

- 인정되는 이스케이프는 `\"` `\'` `\\` `\a` `\b` `\e` `\f` `\n` `\r` `\t` `\v` `\cX`
  `\xXX` `\ddd`다 (§2.2.4).[^opengroup2024-shell] **`\'`가 있으므로 이 기법은 작은따옴표를
  담을 수 있다** — 위 작은따옴표의 제약을 푸는 자리다.
- 그 밖의 문자를 백슬래시로 이스케이프하면 **미지정(unspecified)이다** — 개행 포함
  (§2.2.4).[^opengroup2024-shell] 목록에 없는 이스케이프를 쓰지 말라는 뜻이다.
- 처리 시점이 규정돼 있다 (§2.2.4):[^opengroup2024-shell]

> These `<backslash>`-escape sequences shall be processed (replaced with the bytes or characters
> they yield) immediately prior to word expansion of the word in which the dollar-single-quotes
> sequence occurs.

  - 즉 단어 확장보다 **앞선다.** 산출된 바이트는 그다음 확장 단계의 입력이 된다.
  - 버전 조건: Open Group Base Specifications Issue 8 부터 — 이 절은 이 판본에서 새로 생겼다
    (소스 메타의 판본 절 참조).

## 인용 제거는 맨 끝에 온다

- 인용 문자 자체가 사라지는 것은 확장의 마지막 단계다 (§2.6.7):[^opengroup2024-shell]

> The quote character sequence `<dollar-sign>` single-quote and the single-character quote
> characters (`<backslash>`, single-quote, and double-quote) that were present in the original
> word shall be removed unless they have themselves been quoted.

- 그리고 스펙이 붙인 주석이 중요하다 — **인용 제거 뒤에도 셸은 어느 문자가 인용됐는지 기억한다**
  (§2.6.7).[^opengroup2024-shell] `case`의 패턴 매칭이 그 기억을 쓴다. "따옴표를 지웠으니
  이제 패턴 문자로 취급된다"가 아니다.

## 이어지는 페이지

- [단어 확장의 순서](shell-word-expansion-order.md) — 인용이 어느 단계를 막는지 보려면 단계가
  먼저 있어야 한다
- [필드 분리와 IFS](shell-field-splitting.md) — 큰따옴표가 실제로 막는 것
- [경로명 확장](shell-pathname-expansion.md) — 인용이 글로브 패턴을 문자 그대로 만드는 자리
- [위치 파라미터와 특수 파라미터](shell-special-parameters.md) — `"$@"`가 큰따옴표 안에서
  특별해지는 자리
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.2 Quoting, §2.2.1 Escape Character (Backslash),
    §2.2.2 Single-Quotes, §2.2.3 Double-Quotes, §2.2.4 Dollar-Single-Quotes, §2.6.7 Quote Removal.

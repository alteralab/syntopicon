---
type: concept
title: 셸 리다이렉션
description: 리다이렉션이 무엇을 열고 언제 실패하는가의 요지 — 파일 서술자 번호가 인용되면 리다이렉션으로 인식되지 않는다는 규정, 리다이렉션 대상 단어에 경로명 확장이 적용되지 않는다는 것, 여러 리다이렉션이 앞에서 뒤로 평가된다는 순서, 열기 실패가 리다이렉션 실패라는 규범, noclobber가 O_CREAT와 O_EXCL의 원자성을 요구해 잠금 파일에 쓸 수 있다는 규정, 그리고 히어 도큐먼트의 인용 여부가 확장을 가른다는 규칙
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 셸 리다이렉션

- [형태와 인용의 효과](#형태와-인용의-효과)
- [대상 단어의 확장은 다르다](#대상-단어의-확장은-다르다)
- [순서와 실패](#순서와-실패)
- [noclobber는 원자적이어야 한다](#noclobber는-원자적이어야-한다)
- [히어 도큐먼트](#히어-도큐먼트)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **리다이렉션(redirection)은 어떤 확장을 받고 언제 실패하는가.**

리다이렉션은 현재 셸 실행 환경이나 개별 명령을 위해 파일을 열고 닫는 장치다
(§2.7).[^opengroup2024-shell] 이 페이지는 그중 실패와 이식성에 걸리는 규정만 모은다.

## 형태와 인용의 효과

- 형태는 `[n]redir-op word`이고, `n`은 파일 서술자(file descriptor) 번호다. `n`은 리다이렉션
  연산자 **바로 앞에 붙어야 하며 사이에 공백이 올 수 없다** (§2.7).[^opengroup2024-shell]
- 인용하면 리다이렉션이 아니게 된다. 스펙의 예 둘이 이 규칙을 보여 준다
  (§2.7):[^opengroup2024-shell]
  - `echo \2>a` — 문자 `2`를 파일 `a`에 쓴다(번호가 인용됐으므로 서술자 번호로 인식되지 않는다).
  - `echo 2\>a` — `2>a`를 표준 출력에 쓴다(연산자 일부가 인용되면 리다이렉션 표현 자체가
    인식되지 않는다).
- 지원되는 서술자 번호의 최대값은 구현 정의이나, **모든 구현이 0부터 9까지는 지원해야 한다**
  (§2.7).[^opengroup2024-shell] 그 위를 쓰면 이식성이 없다.
- `{location}redir-op word` 형태를 구현이 지원할 **수 있고**, 지원한다면 그 동작은 구현
  정의다 (§2.7).[^opengroup2024-shell] 이 문서로는 그 문법에 기댈 수 없다.
- 리다이렉션 연산자와 그 피연산자는 **명령에 넘겨지는 인자에 나타나지 않는다**
  (§2.7).[^opengroup2024-shell]

## 대상 단어의 확장은 다르다

- 규범 문구 (§2.7):[^opengroup2024-shell]

> For the other redirection operators, the word that follows the redirection operator shall be
> subjected to tilde expansion, parameter expansion, command substitution, arithmetic expansion,
> and quote removal. Pathname expansion shall not be performed on the word by a non-interactive
> shell; an interactive shell may perform it, but if the expansion would result in more than one
> word it is unspecified whether the redirection proceeds without pathname expansion being
> performed or the redirection fails.

- **필드 분리와 경로명 확장이 목록에 없다.** 그래서 `> $file`에서 `$file`에 공백이 있어도
  갈라지지 않는다 — [필드 분리와 IFS](../concepts/shell-field-splitting.md)가 걸리는 다른 자리와 다르다.
  다만 인용하는 편이 대화형 셸의 미지정 동작을 피한다.
- `<<`와 `<<-`(히어 도큐먼트)의 단어는 **인용 제거만** 받고, 다른 확장이 일어나는지는 미지정이다
  (§2.7).[^opengroup2024-shell]

## 순서와 실패

- **여러 리다이렉션은 앞에서 뒤로 평가된다** (§2.7).[^opengroup2024-shell] `>file 2>&1`과
  `2>&1 >file`이 다른 결과를 내는 근거가 이 한 줄이다.
- 실패의 정의도 한 줄이다 — **A failure to open or create a file shall cause a redirection to
  fail** (§2.7).[^opengroup2024-shell]
- 리다이렉션 실패가 셸을 죽이는지는 명령의 종류에 달렸다. §2.8.1의 표에서 **특수 내장
  유틸리티의 리다이렉션 오류만 `shall exit`**이고, 복합 명령·함수·그 밖 유틸리티의 리다이렉션
  오류는 `shall not exit`다 ([셸 오류의 귀결](../concepts/shell-error-consequences.md)).
- 파이프라인이 정한 표준 입출력은 **명령에 붙은 리다이렉션보다 먼저** 배정된 것으로 본다
  (§2.9.2).[^opengroup2024-shell] 그래서 명령의 리다이렉션이 파이프를 덮어쓴다.

## noclobber는 원자적이어야 한다

- `>`는 `set -C`(noclobber)가 켜져 있고 대상이 존재하는 정규 파일(또는 정규 파일로 풀리는
  심볼릭 링크)이면 **실패해야 한다**. `>|`는 그 옵션을 파일 하나에 대해 무시한다
  (§2.7.2, §2.15 set).[^opengroup2024-shell]
- 그리고 원자성이 규범이다 (§2.7.2):[^opengroup2024-shell]

> The check for existence, file creation, and open operations shall be performed atomically as is
> done by the `open()` function … when the `O_CREAT` and `O_EXCL` flags are set … Performing these
> operations atomically ensures that the creation of lock files and unique (often temporary) files
> is reliable

- **셸만으로 잠금 파일을 만들 수 있다는 근거가 이 문장이다.** 다만 스펙은 파일 종류 검사가
  원자적일 필요는 없다고 덧붙인다 — 그 경우 경쟁 조건이 생겨 리다이렉션 실패 시 오해를 부르는
  진단 메시지가 나올 수 있다 (§2.7.2).[^opengroup2024-shell]
- noclobber가 꺼져 있으면 `>`는 파일을 만들거나 **`O_TRUNC`로 잘라 연다**
  (§2.7.2).[^opengroup2024-shell] `>>`는 `O_APPEND`로 열고 없으면 만든다
  (§2.7.3).[^opengroup2024-shell]

## 히어 도큐먼트

- `<<`와 `<<-`는 뒤따르는 줄들을 명령의 입력으로 돌린다 (§2.7.4).[^opengroup2024-shell]
- 구획 단어(delimiter)를 인용했는지가 확장 여부를 가른다. 인용하지 않으면 본문이 파라미터
  확장·명령 치환·산술 확장을 받고, 이때 **큰따옴표 문자는 특별하게 취급되지 않는다**
  (§2.7.4).[^opengroup2024-shell]
- 인용은 §2.2의 인용 기법으로 하되, 그 효과는 "본문을 확장하지 않는다"는 것이다 — 이것이 §2.2가
  히어 도큐먼트를 다섯째 인용 형태로 언급한 이유다 ([셸 인용](../concepts/shell-quoting.md)).

## 이어지는 페이지

- [셸 오류의 귀결](../concepts/shell-error-consequences.md) — 리다이렉션 실패가 셸을 죽이는 조건
- [단어 확장의 순서](shell-word-expansion-order.md) — 리다이렉션 단어가 받는 확장이 다른 이유
- [셸 실행 환경과 서브셸](../concepts/shell-execution-environment.md) — 열린 파일이 환경의 일부인 자리
- [셸 인용 — 무엇이 확장을 막는가](../concepts/shell-quoting.md) — 히어 도큐먼트가 다섯째 인용인 이유
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.7 Redirection, §2.7.2 Redirecting Output,
    §2.7.3 Appending Redirected Output, §2.7.4 Here-Document, §2.8.1 Consequences of Shell Errors,
    §2.9.2 Pipelines, §2.15 Special Built-In Utilities의 `set`(`-C`).

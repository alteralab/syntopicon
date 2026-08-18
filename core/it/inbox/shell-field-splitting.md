---
type: concept
title: 필드 분리와 IFS
status: draft
description: 인용하지 않은 확장 결과가 왜 여러 개로 쪼개지고 빈 것은 어디로 사라지는가 — 분리 대상이 "큰따옴표 밖에서 일어난 확장 결과"로만 한정된다는 규범, IFS 공백류와 비공백류의 처리 차이를 정하는 Issue 8의 알고리즘, 전부 공백이면 필드가 하나가 아니라 영 개가 된다는 규정, IFS를 빈 문자열로 두는 것과 unset으로 두는 것의 차이, 그리고 이 규범이 셸 스크립트의 빈 필드 소실 사고를 설명하는 방식
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 필드 분리와 IFS

- [무엇이 분리 대상인가](#무엇이-분리-대상인가)
- [IFS의 세 가지 상태](#ifs의-세-가지-상태)
- [공백류와 비공백류 — 갈라지는 자리](#공백류와-비공백류--갈라지는-자리)
- [알고리즘](#알고리즘)
- [전부 공백이면 필드는 영 개다](#전부-공백이면-필드는-영-개다)
- [왜 빈 필드가 사라지는가](#왜-빈-필드가-사라지는가)
- [바이트이지 문자가 아니다](#바이트이지-문자가-아니다)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **인용하지 않은 확장 결과는 어떤 규칙으로 쪼개지며, 왜 빈 필드가 사라지는가.**

셸 스크립트의 자료 손실 사고 가운데 가장 조용한 부류가 여기서 나온다. 값 세 개를 넘겼는데 둘만
도착하고, 빈 값 자리가 통째로 없어지고, 그런데도 종료 상태는 0이다. 이 절의 규범이 그 기제를
정확히 규정한다 — 그것이 버그가 아니라 **명세된 동작**이라는 것이 요점이다.

## 무엇이 분리 대상인가

- 분리(field splitting)의 대상은 단어 전체가 아니라 **확장 결과 중 큰따옴표 밖에서 나온 부분**이다
  (§2.6.5):[^opengroup2024-shell]

> After parameter expansion, command substitution, and arithmetic expansion, if the shell variable
> `IFS` is set and its value is not empty, or if `IFS` is unset, the shell shall scan each field
> containing results of expansions and substitutions that did not occur in double-quotes for field
> splitting; zero, one or multiple fields can result.

- **"zero, one or multiple"이 계약이다.** 확장 하나가 필드 영 개가 될 수도 있다. 인자 하나를
  넘길 셈이었는데 명령이 인자를 아예 못 받는 경우가 여기서 나온다.
- 그리고 스펙이 범위를 두 번 좁힌다 (§2.6.5):[^opengroup2024-shell]

> Fields which contain no results from expansions shall not be affected by field splitting, and
> shall remain unaltered … Field splitting only ever alters those parts of the field.

  - 즉 **리터럴로 적은 공백은 분리 대상이 아니다.** `a b`라고 직접 쓴 것과 `$x`가 `a b`로
    확장된 것은 이 단계에서 취급이 다르다. 확장 결과 안의 바이트만 구분자로 본다.
  - 이 한정이 [셸 인용](shell-quoting.md)의 `"$var"`가 안전한 이유의 나머지 절반이다. 큰따옴표
    안에서 일어난 확장은 애초에 스캔되지 않는다.

## IFS의 세 가지 상태

`IFS`(internal field separator)는 셋 중 하나이고 셋이 각각 다르게 군다 (§2.5.3,
§2.6.5).[^opengroup2024-shell]

| 상태 | 필드 분리 | 근거 |
|---|---|---|
| unset | 값이 `<space><tab><newline>`인 것처럼 분리한다 | §2.5.3 |
| 빈 문자열 | **분리하지 않는다** | §2.6.5 |
| 그 밖 | 그 값의 문자들을 구분자로 쓴다 | §2.6.5 |

- unset일 때의 규범 (§2.5.3):[^opengroup2024-shell]

> If `IFS` is not set, it shall behave as normal for an unset variable, except that field splitting
> by the shell and line splitting by the `read` utility shall be performed as if the value of `IFS`
> is `<space><tab><newline>`.

- 그리고 **셸은 시작할 때 `IFS`를 `<space><tab><newline>`으로 설정한다**
  (§2.5.3).[^opengroup2024-shell] 그러니 기본 상태는 unset이 아니라 "세 문자가 든 값"이다.
- 빈 문자열일 때는 분리가 없지만 **완전히 아무 일도 없는 것은 아니다**
  (§2.6.5):[^opengroup2024-shell]

> If the `IFS` variable is set and has an empty string as its value, no field splitting shall
> occur. However, if an input field which contained the results of an expansion is entirely empty,
> it shall be removed. Note that this occurs before quote removal; any input field that contains
> any quoting characters can never be empty at this point.

  - 빈 필드는 여전히 없어진다. 다만 인용 문자가 하나라도 있던 필드는 이 시점에 비어 있을 수
    없으므로 살아남는다 — `""`가 빈 인자로 도착하는 근거다.
- `IFS` 값에 유효한 문자를 이루지 않는 바이트가 들어 있으면 필드 분리·`*` 확장·`read`의 결과가
  미지정이다 (§2.5.3).[^opengroup2024-shell]

## 공백류와 비공백류 — 갈라지는 자리

- 스펙은 "IFS white space"라는 용어를 따로 세운다 (§2.6.5):[^opengroup2024-shell]

> For the purposes of this section, the term "IFS white space" is used to mean any of the
> white-space bytes `<space>`, `<tab>`, or `<newline>` from the portable character set which are
> present in the value of the `IFS` variable, and perhaps other white-space characters.

- 그 세 문자는 **로케일과 무관하게 항상** IFS 공백류다. 그 밖의 로케일별 공백 문자를 공백류로
  볼지는 구현 정의(implementation-defined)이고, 언제 판정하는지(대입 시점인지 분리 시점인지)는
  미지정이다 — 로케일이 그 사이에 바뀔 수 있기 때문이다 (§2.6.5).[^opengroup2024-shell]
- 구분자의 성질에 대한 규범 문구가 이 절의 핵심이다 (§2.6.5):[^opengroup2024-shell]

> Note that these delimiters terminate a field; they do not, of themselves, cause a new field to
> start—subsequent bytes that are not from the results of an expansion, or that do not form IFS
> white-space characters are required for a new field to begin.

  - **구분자는 필드를 끝낼 뿐 새 필드를 열지 않는다.** 이 한 문장이 "구분자 두 개가 연달아
    나오면 빈 필드가 생긴다"는 직관을 부정한다. 그 직관은 CSV의 것이지 셸의 것이 아니다.

## 알고리즘

Issue 8은 이 동작을 산문이 아니라 알고리즘으로 규정한다. 입력 바이트를 앞에서부터 보며 후보
필드(candidate)를 쌓는데, **네 갈래가 있고 셋째와 넷째가 갈리는 지점이 전부다**
(§2.6.5):[^opengroup2024-shell]

1. 확장에서 나오지 않은 바이트 — 후보에 붙이고 계속한다.
2. 확장에서 나왔으나 `IFS`의 문자를 이루지 않는 바이트 — 후보에 붙이고 계속한다.
3. 확장에서 나왔고 **IFS 공백류 문자**를 이루는 바이트열 — 입력에서 **제거하고 이 단계를
   반복한다**(연속한 공백류를 계속 먹는다).
4. 확장에서 나왔고 **IFS 문자이되 공백류가 아닌** 바이트열 — 제거하되 **"보았다"고 기록한다.**

그리고 판정 (§2.6.5):[^opengroup2024-shell]

> At this point, if the candidate is not empty, or if a sequence of bytes representing an IFS
> character that is not IFS white space was seen at step 4, then a field is said to have been
> delimited, and the candidate shall become an output field.

- **셋째와 넷째의 차이가 전부다.** 공백류는 아무리 연달아 와도 필드를 하나만 끊는다(3단계가
  자기 자신을 반복하며 다 먹는다). 비공백류는 한 번 나올 때마다 필드를 끊고, 후보가 비어
  있어도 **빈 필드를 만들어 낸다**(4단계의 "보았다" 기록이 조건에 들어가므로).
- 그래서 `IFS=:`로 두면 `a::b`는 `a`, 빈 것, `b` 세 필드가 되고, 기본 `IFS`에서 `a  b`(공백 둘)는
  `a`, `b` 두 필드가 된다. 같은 "구분자 두 개"인데 결과가 다르다.
- 입력이 다 떨어지면 후보는 **비어 있지 않을 때만** 출력 필드가 된다
  (§2.6.5).[^opengroup2024-shell] 그래서 끝의 구분자는 빈 필드를 남기지 않는다.

## 전부 공백이면 필드는 영 개다

- 규범 문구 (§2.6.5):[^opengroup2024-shell]

> If the results of the algorithm are that no fields are delimited; that is, if the input field is
> wholly empty or consists entirely of IFS white space, the result shall be zero fields (rather
> than an empty field).

- **"rather than an empty field"**를 괄호에 넣어 명시한 것이 이 문장의 요점이다. 빈 문자열을
  인용 없이 확장하면 인자가 하나 줄어드는 것이지, 빈 인자가 하나 도착하는 것이 아니다.
- 출력 필드의 순서는 입력 순서를 유지한다 (§2.6.5).[^opengroup2024-shell] 사라지기는 해도
  뒤섞이지는 않는다.

## 왜 빈 필드가 사라지는가

앞의 세 규정을 합치면 사고의 기제가 나온다. 인용하지 않은 확장의 결과가 빈 문자열이거나 공백뿐일
때 —

- 3단계가 공백류를 전부 먹고 후보는 계속 비어 있다.
- 4단계의 "보았다" 기록도 없다(비공백류 구분자가 없었으므로).
- 그래서 필드가 하나도 끊기지 않고, 규범은 그 결과를 **영 개**로 못 박는다.

즉 빈 값이 "빈 인자"로 전달되는 것이 아니라 **인자 목록에서 통째로 빠진다.** 뒤 인자들이 한 칸씩
앞으로 밀리므로, 자리로 인자를 세는 코드는 조용히 다른 값을 읽는다. 종료 상태는 0이다 —
[셸 오류의 귀결](shell-error-consequences.md)이 이것을 오류로 치지 않기 때문이다.

- 막는 방법은 규범이 이미 말해 두었다: **분리 대상에서 빼면 된다.** 큰따옴표 안의 확장은
  스캔되지 않고(위 [무엇이 분리 대상인가](#무엇이-분리-대상인가)), 인용 문자를 담은 필드는
  빈 채로 제거되지도 않는다(위 [IFS의 세 가지 상태](#ifs의-세-가지-상태)).
- `IFS`를 바꾸는 것은 대안이 아니라 **다른 규칙으로 갈아타는 일**이다. 비공백류로 바꾸면 빈
  필드는 살아나지만 이번에는 공백이 구분자에서 빠진다. 어느 쪽이든 규칙을 알고 고르는 것이지
  "안전해지는" 설정은 없다.

## 바이트이지 문자가 아니다

- 스펙은 셸이 임의의 바이트를 다룬다고 명시한다 (§2.6.5):[^opengroup2024-shell]

> Note that the shell processes arbitrary bytes from the input fields; there is no requirement that
> those bytes form valid characters.

- 파라미터 값도 마찬가지다 — 널 바이트를 뺀 임의의 바이트열을 담을 수 있고, 셸은 이 표준이
  문자 단위로 규정한 연산을 할 때에만 값을 문자로 취급한다 (§2.5).[^opengroup2024-shell]
- 이것이 인코딩 문제가 셸에서 조용히 지나가는 이유다. 잘못된 바이트열이 있어도 셸은 대개
  실패하지 않고 그대로 옮긴다. 실패는 그것을 문자로 해석하려는 다음 도구에서 난다.

## 이어지는 페이지

- [단어 확장의 순서](shell-word-expansion-order.md) — 이 단계가 언제 오는가
- [셸 인용 — 무엇이 확장을 막는가](shell-quoting.md) — 이 단계를 건너뛰게 하는 유일한 방법
- [위치 파라미터와 특수 파라미터](shell-special-parameters.md) — `$*`가 `IFS`의 첫 문자를 쓰는
  자리
- [경로명 확장](shell-pathname-expansion.md) — 분리된 필드가 다음으로 통과하는 단계
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.6.5 Field Splitting, §2.5.3 Shell Variables의
    `IFS` 항, §2.5 Parameters and Variables. 알고리즘 네 갈래는 원문의 중첩 목록을 번호 목록으로
    평평하게 옮긴 것이고 각 갈래의 문면은 그대로다.

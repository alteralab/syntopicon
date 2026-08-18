---
type: concept
title: 셸 오류의 귀결
status: draft
description: 어떤 오류가 비대화형 셸을 종료시키고 어떤 오류는 그냥 지나가는가 — 오류 종류별 종료 여부를 정한 표와 그 안의 "shall exit"·"may exit"·"shall not exit" 구분, 특수 내장 유틸리티가 일반 유틸리티와 다른 두 가지, set -e가 무엇을 종료시키고 어디서 무시되는지의 규범 목록, 그리고 0이 아닌 종료 상태와 "오류"가 다른 축이라는 구분
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 셸 오류의 귀결

- [두 축을 먼저 가른다](#두-축을-먼저-가른다)
- [오류 종류별 종료 여부](#오류-종류별-종료-여부)
- [특수 내장 유틸리티가 다른 두 가지](#특수-내장-유틸리티가-다른-두-가지)
- [서브셸에서 나면](#서브셸에서-나면)
- [set -e가 정확히 무엇을 하는가](#set--e가-정확히-무엇을-하는가)
- [set -e가 무시되는 자리](#set--e가-무시되는-자리)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **무엇이 셸을 멈추게 하는 "오류"이고, 무엇은 그저 0이 아닌 상태인가.**

## 두 축을 먼저 가른다

- 이 스펙은 **오류(error)**와 **0이 아닌 종료 상태**를 다른 것으로 다룬다. 종료 상태는
  §2.8.2가 정하고([셸의 종료 상태와 그 전파](shell-exit-status.md)), 무엇이 셸을 죽이는지는
  §2.8.1이 정한다.
- 예를 들어 `grep`이 아무것도 못 찾아 1을 내는 것은 §2.8.1의 표에서 "Other utility error"이고
  **비대화형 셸도 종료하지 않는다.** 반면 확장 오류는 같은 표에서 `shall exit`다. 둘을 한
  낱말로 부르면 이 구분이 사라진다.

## 오류 종류별 종료 여부

스펙의 표를 그대로 옮긴다 (§2.8.1).[^opengroup2024-shell]

| 오류 | 비대화형 셸 | 대화형 셸 | 셸 진단 메시지 필수 |
|---|---|---|---|
| 셸 언어 문법 오류 | shall exit | shall not exit | 예 |
| 특수 내장 유틸리티 오류 | shall exit (주1) | shall not exit | 아니오 (주2) |
| 그 밖 유틸리티 오류 | shall not exit | shall not exit | 아니오 (주3) |
| 특수 내장 유틸리티의 리다이렉션 오류 | shall exit | shall not exit | 예 |
| 복합 명령의 리다이렉션 오류 | shall not exit | shall not exit | 예 |
| 함수 실행의 리다이렉션 오류 | shall not exit | shall not exit | 예 |
| 그 밖 유틸리티의 리다이렉션 오류 | shall not exit | shall not exit | 예 |
| 변수 대입 오류 | shall exit | shall not exit | 예 |
| 확장 오류 | shall exit | shall not exit | 예 |
| 명령을 찾지 못함 | **may exit** | shall not exit | 예 |
| 명령을 읽는 중 복구 불가 읽기 오류 | shall exit (주4) | shall exit (주4) | 예 |

- **주1**: 특수 내장 유틸리티를 직접 실행했을 때만 종료한다. `command` 유틸리티를 거치면
  종료하지 않는다.
- **주2**: 특수 내장이 셸의 일부이긴 하나 그것이 쓴 진단 메시지는 셸 진단 메시지로 치지 않고,
  다른 유틸리티처럼 리다이렉트할 수 있다.
- **주3**: 셸은 메시지를 쓸 의무가 없다. 유틸리티 자신이 요구받은 경우 쓴다.
- **주4**: `dot` 특수 내장의 파일 피연산자를 읽는 중이 아니라면, 셸은 **이미 읽었으나 아직
  실행하지 않은 명령을 포함해** 더 이상 아무 명령도 실행하지 않는다 — `EXIT` 트랩만 예외다.
- **"Command not found"만 `may exit`다.** 셋 중 어느 등급도 아닌 중간이 여기 하나 있고, 그래서
  없는 명령을 부른 스크립트가 계속 도는지 멈추는지는 이 문서로 답할 수 없다.
- 확장 오류가 무엇인지도 규정돼 있다 — §2.6의 확장을 수행할 때 나는 오류이고, 스펙의 예는
  `${x!y}`다(`!`가 유효한 연산자가 아니므로). 구현이 토큰화 중에 이것을 검출할 수 있으면
  문법 오류로 다뤄도 된다 (§2.8.1).[^opengroup2024-shell]
- 대화형 셸이 종료하지 않는 자리에서도 **오류가 난 명령의 이후 처리는 전부 중단된다**
  (§2.8.1).[^opengroup2024-shell] 계속 도는 것은 셸이지 그 명령이 아니다.

## 특수 내장 유틸리티가 다른 두 가지

- 규범 문구 (§2.15):[^opengroup2024-shell]

> An error in a special built-in utility may cause a shell executing that utility to abort, while
> an error in a regular built-in utility shall not cause a shell executing that utility to abort.
> … If a special built-in utility encountering an error does not abort the shell, its exit value
> shall be non-zero.
>
> As described in 2.9.1 Simple Commands, variable assignments preceding the invocation of a special
> built-in utility affect the current execution environment; this shall not be the case with a
> regular built-in or other utility.

- 그래서 **어느 유틸리티가 특수 내장인지가 실제로 중요하다.** 이 문서가 특수 내장으로 나열하는
  것은 열다섯이다 (§2.15):[^opengroup2024-shell] `break`, `:`(colon), `continue`, `.`(dot),
  `eval`, `exec`, `exit`, `export`, `readonly`, `return`, `set`, `shift`, `times`, `trap`,
  `unset`.
  - 목록에 없는 것은 이 문서가 특수 내장으로 규정하지 않는다는 뜻이다. 구현이 어떤 유틸리티든
    내장으로 만들 수 있다고 같은 절이 명시하므로 (§2.15),[^opengroup2024-shell] "내장이니까
    특수 내장"이 아니다.
  - 이 목록에 `local`이 없다는 점을 이식성 판단에 쓸 수 있다 — 이 문서는 그 이름을 규정하지
    않는다. 특정 셸이 무엇을 제공하는지는 그 셸의 문서가 답한다.
- 특수 내장은 `exec` 계열 함수로 접근 가능한 형태로 제공되지 않아도 된다
  (§2.15).[^opengroup2024-shell]

## 서브셸에서 나면

- 규범 문구 (§2.8.1):[^opengroup2024-shell]

> If any of the errors shown as "shall exit" or "may exit" occur in a subshell environment, the
> shell shall (respectively, may) exit from the subshell environment with a non-zero status and
> continue in the environment from which that subshell environment was invoked.

- **죽는 것은 서브셸까지다.** 바깥 셸은 0이 아닌 상태를 받고 계속 간다. 명령 치환 안에서 난
  치명적 오류가 바깥 스크립트를 멈추지 않는 근거가 이것이다
  ([셸 실행 환경과 서브셸](shell-execution-environment.md)).

## set -e가 정확히 무엇을 하는가

- 규범 문구 (§2.15 set):[^opengroup2024-shell]

> When this option is on, when any command fails (for any of the reasons listed in 2.8.1
> Consequences of Shell Errors or by returning an exit status greater than zero), the shell
> immediately shall exit, as if by executing the `exit` special built-in utility with no arguments

- **`set -e`가 두 축을 하나로 묶는다.** §2.8.1의 오류든 그냥 0보다 큰 종료 상태든 똑같이
  종료시킨다. 위에서 갈라 둔 두 축이 이 옵션 아래서만 합쳐진다.

## set -e가 무시되는 자리

스펙이 예외를 셋으로 못 박는다 (§2.15 set).[^opengroup2024-shell] 이 목록이
`set -e`를 켜고도 실패가 지나가는 이유의 전부다.

- **파이프라인 안의 개별 명령**, 그리고 단어 확장 중 명령 치환이 수행된 서브셸 환경의 실패는
  셸을 종료시키지 않는다. **파이프라인 자체의 실패만 친다.**
- **`while`·`until`·`if`·`elif` 뒤의 compound list**, `!`로 시작하는 파이프라인, 그리고 AND-OR
  목록에서 마지막이 아닌 모든 명령에서는 `-e` 설정이 무시된다.
- `-e`가 무시되는 동안의 실패로 복합 명령(서브셸 명령은 제외)의 종료 상태가 정해졌다면,
  그 복합 명령에는 `-e`가 적용되지 않는다.

- 그리고 요구는 **셸 환경과 각 서브셸 환경에 따로 적용된다.** 스펙이 든 첫째 예가 그 분리를
  보여 준다 — 셸에 그대로 붙여 넣어 확인할 수 있는 최소 재현이다 (§2.15 set):[^opengroup2024-shell]

  ```sh
  set -e; (false; echo one) | cat; echo two
  ```

- `false`가 서브셸을 끝내 `echo one`은 돌지 않는다. 그러나 파이프라인 `(false; echo one) | cat`의
  종료 상태는 0이므로 **`echo two`는 실행된다** (§2.15 set).[^opengroup2024-shell]
- 둘째 예 `set -e; echo $(false; echo one) two`도 같은 구조다 — 명령 치환의 서브셸이 끝나지만
  그 상태는 무시되고 셸은 `echo two`를 실행한다 (§2.15 set).[^opengroup2024-shell]

## 이어지는 페이지

- [셸의 종료 상태와 그 전파](shell-exit-status.md) — 다른 축
- [셸 실행 환경과 서브셸](shell-execution-environment.md) — 오류가 어디까지 죽이는가
- [파라미터 확장](shell-parameter-expansion.md) — 확장 오류를 일부러 내는 장치
- [죽은 프로그램은 거짓말하지 않는다](dead-programs-tell-no-lies.md) — 일찍 죽으라는 처방 쪽.
  이 페이지는 셸이 실제로 언제 죽기로 약속했는지를 답한다
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.8.1 Consequences of Shell Errors(표와 주석),
    §2.15 Special Built-In Utilities(특수 내장의 두 차이·목록)와 그 안의 `set` 유틸리티(`-e`).
    표의 열 이름과 주석 번호는 원문 그대로이고 한국어는 항목 이름만 옮겼다.

---
type: concept
title: 셸의 종료 상태와 그 전파
status: draft
description: 명령 하나의 종료 상태가 어떻게 정해지고 파이프라인·목록·복합 명령·함수를 지나며 무엇으로 바뀌는가 — 127과 126과 128 초과라는 세 예약값, pipefail이 표준이 된 Issue 8의 파이프라인 종료 상태 표, AND-OR 목록과 조건 구문이 "실행된 마지막 것"을 물려주는 규칙, 반복문이 조건절의 상태를 버린다는 규정과 그 때문에 실패 원인을 잃는 자리, 그리고 명령 이름이 없는 단순 명령의 상태
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 셸의 종료 상태와 그 전파

- [명령 하나의 종료 상태](#명령-하나의-종료-상태)
- [파이프라인 — pipefail이 표준이 되었다](#파이프라인--pipefail이-표준이-되었다)
- [목록 — 실행된 마지막 것](#목록--실행된-마지막-것)
- [조건 구문과 반복문 — 조건절의 상태는 버려진다](#조건-구문과-반복문--조건절의-상태는-버려진다)
- [함수와 그룹](#함수와-그룹)
- [명령 이름이 없는 단순 명령](#명령-이름이-없는-단순-명령)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **종료 상태(exit status)는 무엇으로 정해지고, 구조를 통과하며 어디서 사라지는가.**

셸 스크립트에서 실패가 조용히 지나가는 경로 대부분이 여기 있다. 실패한 명령은 분명히 0이 아닌
상태를 냈는데, 그것을 감싼 구조가 다른 값을 물려준다.

## 명령 하나의 종료 상태

- 네 갈래로 규정돼 있다 (§2.8.2):[^opengroup2024-shell]

> If the command is not found, the exit status shall be 127.
> Otherwise, if the command name is found, but it is not an executable utility, the exit status
> shall be 126.
> Otherwise, if the command terminated due to the receipt of a signal, the shell shall assign it an
> exit status greater than 128.
> Otherwise, the exit status shall be the value obtained by the equivalent of the `WEXITSTATUS`
> macro applied to the status obtained by the `wait()` function.

- **127과 126이 예약값이다.** 127은 명령을 못 찾은 것, 126은 찾았으나 실행 가능한 유틸리티가
  아닌 것. 스크립트 자신이 이 값을 종료 상태로 내면 호출자가 구분하지 못한다.
- 신호로 끝났을 때는 128 초과이고, **어떤 신호였는지를 어떻게 담는지는 구현 정의**다. 게다가
  스펙은 구현이 **255를 넘는 값을 배정하는 것도 허용한다**고 명시한다
  (§2.8.2).[^opengroup2024-shell] "128+신호번호"는 관례이지 이 문서의 보장이 아니다.
- 정상 종료의 값은 `WEXITSTATUS`를 거친 값이다. 스펙의 주석은 C 프로그램에서 그것이 **256으로
  나눈 나머지**와 같다고 적는다 (§2.8.2).[^opengroup2024-shell] `exit(256)`은 0이 된다.

## 파이프라인 — pipefail이 표준이 되었다

- 종료 상태는 `pipefail` 옵션과 `!` 예약어의 조합으로 정해진다
  (§2.9.2).[^opengroup2024-shell] 스펙의 표를 옮긴다.

| pipefail | `!`로 시작 | 종료 상태 |
|---|---|---|
| 아니오 | 아니오 | 파이프라인의 **마지막(가장 오른쪽)** 명령의 종료 상태 |
| 아니오 | 예 | 마지막 명령이 0이 아니면 0, 아니면 1 |
| 예 | 아니오 | 모든 명령이 0이면 0, 아니면 **0이 아닌 상태를 낸 가장 오른쪽 명령**의 상태 |
| 예 | 예 | 어느 하나라도 0이 아니면 0, 아니면 1 |

- 기본값(`pipefail` 없음)이 함정의 근원이다 — **왼쪽 명령이 실패해도 파이프라인은 오른쪽 명령의
  상태를 낸다.** `grep`이 죽어도 `wc -l`이 성공하면 파이프라인은 성공이다.
- 판정 시점도 규정돼 있다 (§2.9.2):[^opengroup2024-shell]

> The shell shall use the `pipefail` setting at the time it begins execution of the pipeline, not
> the setting at the time it sets the exit status of the pipeline.

- 셸은 파이프라인의 **마지막 명령이 끝나기를 기다리고**, 나머지 전부를 기다려도 된다(`may`)
  (§2.9.2).[^opengroup2024-shell] 앞쪽 명령이 아직 돌고 있는데 파이프라인이 끝나 있을 수 있다는
  뜻이다.
  - 버전 조건: Open Group Base Specifications Issue 8 부터 — `pipefail`은 이 판본에서 표준에
    들어왔다(`set` 절의 변경 이력이 `Austin Group Defect 789 is applied, adding -o pipefail`이라
    적는다). 이전 판본만 보고 "POSIX에 없는 bash 확장"이라 말하면 이 판본에서는 틀린다.

## 목록 — 실행된 마지막 것

- `&&`와 `||`는 **우선순위가 같고 왼쪽 결합**이다 (§2.9.3).[^opengroup2024-shell] 스펙이 든 예
  둘은 모두 `bar`만 출력한다: `false && echo foo || echo bar`와 `true || echo foo && echo bar`.
- AND 목록·OR 목록·순차 목록의 종료 상태는 전부 같은 규칙이다 — **실행된 마지막 명령의 종료
  상태** (§2.9.3.2, §2.9.3.3, §2.9.3.4).[^opengroup2024-shell] 건너뛴 명령은 세지 않는다.
  - AND 목록에서 스펙은 **The commands are expanded only if they are executed**라고 못 박는다
    (§2.9.3.3).[^opengroup2024-shell] 실행되지 않으면 확장도 일어나지 않는다.
- **비동기 AND-OR 목록(`&`)의 종료 상태는 0이다** (§2.9.3.1).[^opengroup2024-shell] 실제 상태는
  `wait`로만 얻는다. 백그라운드로 돌린 명령의 실패는 `$?`로 절대 보이지 않는다.

## 조건 구문과 반복문 — 조건절의 상태는 버려진다

- `if`의 종료 상태는 **실행된 `then` 또는 `else`의 상태**이고, 아무것도 실행되지 않았으면 0이다
  (§2.9.4.4).[^opengroup2024-shell] 조건절의 상태는 결과에 들어가지 않는다.
- `while`의 종료 상태는 **마지막으로 실행된 본문의 상태**이고, 한 번도 안 돌았으면 0이다
  (§2.9.4.5).[^opengroup2024-shell] `until`도 같다 (§2.9.4.6).
- 스펙이 그 귀결을 직접 적는다 (§2.9.4.5):[^opengroup2024-shell]

> Since the exit status of *compound-list-1* is ignored when determining the exit status of the
> `while` command, it is not possible to obtain the status of the command that caused the loop to
> exit, other than via the special parameter `'?'` during execution of *compound-list-1*

  - **루프를 끝낸 명령의 상태를 사후에 알 수 없다**는 것이 규범 수준의 사실이다. 스펙이 제시한
    유일한 우회가 조건절 안에서 붙잡는 것이다: `while some_command; st=$?; false; do ...`
    (§2.9.4.5).[^opengroup2024-shell]
- `case`의 종료 상태는 **맞는 패턴이 없으면 0**이고, 있으면 실행된 마지막 절의 상태다
  (§2.9.4.3).[^opengroup2024-shell] 아무것도 처리하지 못한 `case`와 성공한 `case`가 같은 값을
  낸다 — `*)`로 미처리를 잡아야 하는 규범적 근거가 이것이다.
- `for`는 항목이 하나라도 있으면 마지막 본문의 상태, **항목이 없으면 0**이다
  (§2.9.4.2).[^opengroup2024-shell] 빈 목록으로 돈 루프는 성공으로 보인다.
- 복합 명령의 종료 상태가 compound-list로 규정될 때, 그 값은 **compound-list 실행 직후 `?`가
  가질 값**이다 (§2.9.4).[^opengroup2024-shell]

## 함수와 그룹

- 함수 **정의**의 종료 상태는 선언에 성공하면 0, 아니면 0보다 크다. 함수 **호출**의 종료 상태는
  **함수가 마지막으로 실행한 명령의 상태**다 (§2.9.5).[^opengroup2024-shell] `return`으로
  명시하지 않으면 마지막 명령이 그대로 반환값이 된다.
- 그룹 명령(`( … )`와 `{ …; }`)의 종료 상태는 compound-list의 상태다
  (§2.9.4.1).[^opengroup2024-shell] 둘의 차이는 상태가 아니라 실행 환경이다
  ([셸 실행 환경과 서브셸](shell-execution-environment.md)).

## 명령 이름이 없는 단순 명령

- 대입만 있거나 리다이렉션만 있는 명령도 종료 상태를 낸다 (§2.9.1.3):[^opengroup2024-shell]

> Additionally, if there is no command name but the command contains a command substitution, the
> command shall complete with the exit status of the command substitution whose exit status was the
> last to be obtained. Otherwise, the command shall complete with a zero exit status.

- 그래서 `var=$(some_command)`의 종료 상태가 `some_command`의 것이 된다 — 이것이
  [특수 파라미터](shell-special-parameters.md)의 `?` 항에 붙은 주석이 설명하는 기제다.
- 그리고 `var=$(cmd1) $(cmd2)`처럼 여럿이면 **마지막으로 얻은 것**이 남는다. 순서를 세지 않으면
  어느 실패를 보고 있는지 알 수 없다.
- 리다이렉션이 실패하면 명령은 **즉시 0보다 큰 상태로 실패하고** 셸이 오류 메시지를 쓴다
  (§2.9.1.3).[^opengroup2024-shell]

## 이어지는 페이지

- [셸 오류의 귀결](shell-error-consequences.md) — 0이 아닌 상태와 "오류"는 다른 축이다
- [셸 실행 환경과 서브셸](shell-execution-environment.md) — 상태가 경계를 넘는 방식
- [위치 파라미터와 특수 파라미터](shell-special-parameters.md) — `?`가 무엇을 가리키는가
- [Unix 도구로 하는 배치 처리](batch-processing-with-unix-tools.md) — 파이프라인의 효용 쪽.
  이 페이지는 그 파이프라인이 실패를 어떻게 보고하는지를 답한다
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.8.2 Exit Status for Commands, §2.9.1.3 Commands
    with no Command Name, §2.9.2 Pipelines, §2.9.3 Lists와 그 하위 §2.9.3.1–2.9.3.4,
    §2.9.4 Compound Commands와 그 하위 §2.9.4.1–2.9.4.6, §2.9.5 Function Definition Command,
    §2.15 Special Built-In Utilities의 `set`(CHANGE HISTORY). 네 갈래 인용은 원문의 번호 없는
    항목 목록을 이어 붙인 것이고 문면은 그대로다.

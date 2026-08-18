---
type: concept
title: 셸 실행 환경과 서브셸
description: 서브셸이 무엇을 복사하고 무엇을 되돌리지 않는가 — 셸 실행 환경을 이루는 열 가지 항목의 목록, 서브셸이 복제본이며 그 변경이 바깥에 영향을 주지 않는다는 규범, 서브셸이 만들어지는 네 자리(명령 치환·괄호 그룹·비동기 목록·다중 명령 파이프라인)와 파이프라인에 붙은 구현 재량, 유틸리티가 받는 별도 환경이 셸 환경보다 좁다는 것, 그리고 변수 대입이 현재 환경에 남는지가 명령의 종류에 달렸다는 규정
generated: { by: "claude-fable-5", at: "2026-08-18T13:00:00Z" }
sources:
  - { id: opengroup2024-shell, resource: /it/sources/opengroup2024-shell.md }
---

# 셸 실행 환경과 서브셸

- [셸 실행 환경을 이루는 것](#셸-실행-환경을-이루는-것)
- [서브셸은 복제본이고 변경은 돌아오지 않는다](#서브셸은-복제본이고-변경은-돌아오지-않는다)
- [서브셸이 생기는 자리](#서브셸이-생기는-자리)
- [유틸리티가 받는 환경은 더 좁다](#유틸리티가-받는-환경은-더-좁다)
- [변수 대입이 어디에 남는가](#변수-대입이-어디에-남는가)
- [함수가 되돌리는 것과 되돌리지 않는 것](#함수가-되돌리는-것과-되돌리지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **서브셸 환경(subshell environment)은 무엇을 복사하고, 그 안의 변경 중 무엇이
바깥으로 돌아오지 않는가.**

"루프 안에서 센 값이 루프 밖에서 0이더라"는 종류의 사고가 전부 이 절의 규범에서 나온다. 셸에는
값을 돌려보내는 장치가 없고, 그것이 버그가 아니라 명세다.

## 셸 실행 환경을 이루는 것

스펙이 열 항목으로 열거한다 (§2.13).[^opengroup2024-shell]

- 셸 호출 시 상속된 열린 파일과 `exec`으로 제어되는 열린 파일
- `cd`가 정한 작업 디렉터리
- `umask`가 정한 파일 생성 마스크
- `ulimit`가 정한 파일 크기 한계
- `trap`이 설정한 현재 트랩
- 변수 대입으로 설정된 셸 파라미터, 또는 셸이 시작할 때 상속한 환경에서 온 것
- 셸 함수
- 호출 시 또는 `set`으로 켠 옵션
- 백그라운드 작업과 그 프로세스 ID들("이 셸 환경에 알려진" 프로세스 ID)
- 셸 별칭

**목록이 곧 경계다.** 여기 든 것이 서브셸에 복사되고, 서브셸에서 바뀐 것이 돌아오지 않는다.

## 서브셸은 복제본이고 변경은 돌아오지 않는다

- 규범 문구 (§2.13):[^opengroup2024-shell]

> A subshell environment shall be created as a duplicate of the shell environment, except that:
> Unless specified otherwise, traps that are not being ignored shall be set to the default action.
> If the shell is interactive, the subshell shall behave as a non-interactive shell in all respects
> except: The expansion of the special parameter `'-'` may continue to indicate that it is
> interactive. The `set -n` option may be ignored.

- 그리고 결정적인 한 문장 (§2.13):[^opengroup2024-shell]

> Changes made to the subshell environment shall not affect the shell environment.

- **일방향이다.** 복사는 안으로만 가고, 변경은 밖으로 나오지 않는다. 변수도, 작업 디렉터리도,
  함수 정의도, 트랩도 마찬가지다.
- 서브셸로 값을 내보내는 유일한 통로는 이 목록 밖에 있다 — 표준 출력(명령 치환이 읽는다)과
  종료 상태다.
- **트랩은 복사되지 않는다.** 무시(ignore) 상태가 아닌 트랩은 서브셸에서 기본 동작으로
  되돌아간다 — 정리 코드를 `trap`으로 걸어 둔 스크립트가 서브셸 안에서는 그 정리를 하지
  않는다는 뜻이다.

## 서브셸이 생기는 자리

- 규범 문구 (§2.13):[^opengroup2024-shell]

> Command substitution, commands that are grouped with parentheses, and asynchronous AND-OR lists
> shall be executed in a subshell environment. Additionally, each command of a multi-command
> pipeline is in a subshell environment; as an extension, however, any or all commands in a
> pipeline may be executed in the current environment. Except where otherwise stated, all other
> commands shall be executed in the current shell environment.

- 네 자리가 명시돼 있다: 명령 치환, 괄호 그룹 `( … )`, 비동기 AND-OR 목록(`&`), 그리고
  **다중 명령 파이프라인의 각 명령**.
- 마지막에 붙은 단서가 이식성의 함정이다 — **구현은 파이프라인의 일부나 전부를 현재 환경에서
  실행해도 된다**(`as an extension`). 그래서 `... | while read x; do count=$((count+1)); done`
  뒤에 `count`가 남는지 아닌지가 **셸마다 다르고 이 문서는 어느 쪽도 보장하지 않는다.**
  한 셸에서 되던 스크립트가 다른 셸에서 안 되는 대표적 자리다.
- 반대로 중괄호 그룹 `{ compound-list ; }`는 **현재 프로세스 환경에서** 실행된다
  (§2.9.4.1).[^opengroup2024-shell] 괄호와 중괄호의 차이가 여기다 — 괄호 그룹은
  **Variable assignments and built-in commands that affect the environment shall not remain in
  effect after the list finishes** (§2.9.4.1).[^opengroup2024-shell]
- 명령 이름이 없는 단순 명령의 리다이렉션도 서브셸 환경에서 수행된다. 그것이 명령 치환에 쓰인
  서브셸과 같은 것인지는 **미지정이다** (§2.9.1.3).[^opengroup2024-shell]
- 서브셸이라고 프로세스 ID가 달라 보이지는 않는다 — `$`는 서브셸에서도 현재 셸과 같은 값이고
  `PPID`도 부모의 것과 같다 (§2.5.2, §2.5.3).[^opengroup2024-shell] **프로세스 ID로 서브셸을
  식별할 수 없다.**

## 유틸리티가 받는 환경은 더 좁다

- 특수 내장이 아닌 유틸리티는 **별도 환경**에서 호출되고, 그 환경은 다섯 항목뿐이다
  (§2.13):[^opengroup2024-shell] 열린 파일, 현재 작업 디렉터리, 파일 생성 마스크, (셸
  스크립트면) 기본값으로 되돌려진 트랩, 그리고 **export 속성이 붙은 변수**.
- 즉 **export하지 않은 셸 변수는 자식 유틸리티가 보지 못한다.** 셸 함수와 별칭도 넘어가지
  않는다 — 위 서브셸의 경우와 다르다.
- 셸 프로세스의 환경은 유틸리티가 바꾸지 못한다 — 유틸리티 설명이 명시한 경우(`cd`·`umask`)만
  예외다 (§2.13).[^opengroup2024-shell]
- 이름이 유효하지 않아 셸 변수로 초기화되지 못한 환경 변수가 자식 환경에 포함되는지는
  미지정이다 (§2.13).[^opengroup2024-shell]

## 변수 대입이 어디에 남는가

§2.9.1.2가 명령의 종류마다 다르게 규정한다.[^opengroup2024-shell] **네 갈래이고 결과가 전부
다르다.**

| 앞에 붙은 명령 | 대입의 효력 |
|---|---|
| 명령 이름 없음 | **현재 실행 환경에 영향을 준다** |
| 특수 내장이나 함수가 아닌 명령 | 그 명령의 실행 환경으로 export되고 **현재 환경에는 영향을 주지 않는다** |
| 특수 내장 유틸리티 | **현재 실행 환경에 적용되고 명령이 끝난 뒤에도 남는다** |
| 함수 | 함수 실행 동안 현재 실행 환경에 적용된다. **끝난 뒤에도 남는지는 미지정** |

- 셋째 줄이 `VAR=x export ...` 같은 표기의 근거이고, 넷째 줄이 함수에서 `VAR=x myfunc`를 쓰면
  안 되는 이유다 — **지속 여부가 미지정이라 셸마다 다르다.**
- 둘째 줄에도 미지정이 둘 붙는다: 그 대입이 이후 확장에서 보이는지, 그리고 확장의 부작용으로
  생긴 변수 대입이 어디에서 보이는지 (§2.9.1.2).[^opengroup2024-shell]
- `readonly`가 걸린 변수에 대입하려 하면 **변수 대입 오류**이고, 그 귀결은 §2.8.1이 정한다
  (§2.9.1.2)[^opengroup2024-shell] — 비대화형 셸은 종료한다
  ([셸 오류의 귀결](../concepts/shell-error-consequences.md)).

## 함수가 되돌리는 것과 되돌리지 않는 것

- 함수 호출은 **위치 파라미터와 `#`를 임시로 대치하고, 함수가 끝나면 원래 값으로 되돌린다.**
  `0`은 바뀌지 않는다 (§2.9.5).[^opengroup2024-shell]
- 되돌아오는 것은 그 둘뿐이다. **함수는 서브셸이 아니므로** 함수 안에서 바꾼 변수·작업
  디렉터리·옵션은 전부 바깥에 남는다.
- 함수 선언 시점에는 확장이 전혀 일어나지 않는다 — 본문의 확장·리다이렉션·변수 대입은 **호출될
  때마다** 수행된다 (§2.9.5).[^opengroup2024-shell]
- 함수는 특수 내장 유틸리티의 문법 오류 성질을 가진다 (§2.9.5).[^opengroup2024-shell]

## 이어지는 페이지

- [셸 오류의 귀결](../concepts/shell-error-consequences.md) — 오류가 서브셸까지만 죽이는 자리
- [셸의 종료 상태와 그 전파](shell-exit-status.md) — 서브셸이 값을 돌려보내는 통로 하나
- [단어 확장의 순서](shell-word-expansion-order.md) — 명령 치환이 서브셸을 만드는 자리
- [위치 파라미터와 특수 파라미터](shell-special-parameters.md) — 서브셸에서도 같은 값인 것들
- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 축의 허브

[^opengroup2024-shell]: The IEEE and The Open Group 2024, Base Specifications Issue 8 / IEEE Std
    1003.1-2024, Volume 3 Chapter 2. 절 번호는 §2.13 Shell Execution Environment,
    §2.9.1.2 Variable Assignments, §2.9.1.3 Commands with no Command Name, §2.9.4.1 Grouping
    Commands, §2.9.5 Function Definition Command, §2.5.2 Special Parameters, §2.5.3 Shell
    Variables. 열 항목 목록과 표는 원문의 열거를 옮긴 것이다.

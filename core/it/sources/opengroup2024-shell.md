---
type: standard
title: "The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024, Volume 3: Shell and Utilities, Chapter 2: Shell Command Language"
author:
  - { literal: "The IEEE and The Open Group" }
issued: "2024"
authority: "The IEEE and The Open Group"
collection-title: "The Open Group Base Specifications Issue 8"
number: "IEEE Std 1003.1-2024"
URL: "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html"
snapshot: /it/archive/opengroup2024-shell/
snapshot_sha256: "cd384bfb5d2761c6527c7a72d185fd39e0f5c3e2f5c91773c3f726dfc9380762"
accessed: "2026-08-18"
---

# POSIX 셸 명령 언어 — 규범 원전

**이 KB의 첫 표준 문서 소스**다(`type: standard` 첫 사용). 스냅샷의 저작권 표기는
`Copyright © 2001-2024 The IEEE and The Open Group`이고, 문서 머리말은
`The Open Group Base Specifications Issue 8` / `IEEE Std 1003.1-2024`를 함께
싣는다 — 그래서 저자를 한쪽으로 정하지 않고 `literal`로 양쪽을 적었다.

## 왜 들였는가

셸 스크립트의 실패는 대부분 **의미론의 실패**다. 인용을 빠뜨려서, 확장 순서를 잘못
알아서, 종료 상태가 어디까지 전파되는지 몰라서 일어난다. 그 "왜"에 답할 자격이
있는 문서는 한 조직의 스타일 규약이 아니라 **규범 원전**이다. 이 소스는
`shall`·`should`·`may`·`unspecified`·`implementation-defined`라는 규범 어휘로
무엇이 보장되고 무엇이 보장되지 않는지를 문면으로 정한다.

**규범 문구는 번역하지 않고 원문 그대로 인용한다.** 이 소스의 가치가 정확히 그
문면이다 — `shall`을 "한다"로 옮기면 규범 조동사의 등급(요구·권고·허용)이 사라지고,
`unspecified`와 `implementation-defined`의 구분도 흐려진다. 한국어는 해설만 맡는다.

## 절 번호가 판본마다 다르다

**locator는 이 판본(Issue 8)의 절 번호다.** Issue 7과 번호가 어긋나는 자리가 있으니
다른 판본의 번호로 이 각주를 읽지 않는 것이 좋다. 이번 반입에서 실제로 어긋난 것 둘
(2026-08-18 스냅샷 실측):

- 셸 실행 환경은 **§2.13**이다(§2.12는 Signals and Error Handling).
- 종료 상태는 **§2.8**이고 그 아래가 §2.8.1 Consequences of Shell Errors,
  §2.8.2 Exit Status for Commands다.

## 이 판본에서 새로 규범이 된 것

옛 지식으로 "bash 확장"이라 알던 것 일부가 이 판본에서 표준 안으로 들어왔다. 경계를
말하는 claim을 쓸 때 바로 이 지점이 함정이다.

- `set -o pipefail` — §2.9.2의 종료 상태 표가 이것을 정한다. 문서 말미의 변경 이력이
  `Austin Group Defect 789 is applied, adding -o pipefail`이라 적는다.
- `$'...'`(dollar-single-quotes) — §2.2.4가 독립된 인용 기법으로 규정한다.

## 이 소스가 닿을 자리

- [POSIX 셸 명령 언어](../synthesis/posix-shell-command-language.md) — 이 소스가 세운 허브
- [셸과 에디터 — 도구의 유창함](../concepts/tool-fluency-shell-and-editor.md) — 셸을
  쓰라는 처방 쪽. 이 소스는 그 도구가 실제로 무엇을 하기로 약속했는지를 답한다
- [Unix 도구로 하는 배치 처리](../concepts/batch-processing-with-unix-tools.md) —
  파이프라인의 효용 쪽. 이 소스는 그 파이프라인의 종료 상태 규범을 준다

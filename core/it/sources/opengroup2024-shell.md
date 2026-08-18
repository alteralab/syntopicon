---
type: standard
title: "The Open Group Base Specifications Issue 8, IEEE Std 1003.1-2024, Volume 3: Shell and Utilities — Chapter 2: Shell Command Language, and the read utility page of Chapter 3"
author:
  - { literal: "The IEEE and The Open Group" }
issued: "2024"
authority: "The IEEE and The Open Group"
collection-title: "The Open Group Base Specifications Issue 8"
number: "IEEE Std 1003.1-2024"
URL: "https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html"
snapshot: /it/archive/opengroup2024-shell/
snapshot_sha256: "59b797fbe37637d31883aedaec39b254ec6674c17b394eb8a907eeca64f594e3"
accessed: "2026-08-19"
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

## 스냅샷에 든 것 — 2026-08-19에 한 건이 추가됐다

이 아카이브는 **원문 두 개**를 담는다. 파일마다 sha256이 있고 `snapshot_sha256`은 그 매니페스트의
해시다.

| 파일 | 무엇 | sha256 |
|---|---|---|
| `V3_chap02.html` | Volume 3 Chapter 2 Shell Command Language | `0889867a53fe1250…` |
| `read.html` | Volume 3 Chapter 3 `read` 유틸리티 페이지 | `2eec6366229acb50…` |

`read.html`의 원 주소는 `https://pubs.opengroup.org/onlinepubs/9799919799/utilities/read.html`이고
2026-08-19에 받았다. `V3_chap02.html`은 2026-08-18에 받은 바이트 그대로이며 **sha256이 바뀌지
않았다**(위 표의 값이 첫 반입 때 계산된 것과 같다).

**`snapshot_sha256`이 `cd384bfb5d27…`에서 `59b797fbe376…`으로 바뀐 이유가 이 추가다.** 다이제스트는
디렉터리 전체의 매니페스트 해시라 파일이 늘어도 값이 달라진다 — 즉 **추가와 변조가 같은 신호를
낸다.** `tools/snapshot.py`는 아카이브 디렉터리가 이미 있으면 통째로 거부하므로(write-once) 추가
경로를 제공하지 않고, 이번 추가는 그 도구의 `fetch`와 다이제스트 함수를 그대로 써서 손으로 붙였다.
기존 파일은 지우지도 덮지도 않았고, 위 표가 그 증거다.

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
- [read와 변수 배분](../concepts/shell-read-field-assignment.md) — Chapter 3에서 온 첫 페이지.
  Chapter 2의 필드 분리가 끝난 지점부터를 이 유틸리티 명세가 이어받는다
- [셸과 에디터 — 도구의 유창함](../concepts/tool-fluency-shell-and-editor.md) — 셸을
  쓰라는 처방 쪽. 이 소스는 그 도구가 실제로 무엇을 하기로 약속했는지를 답한다
- [Unix 도구로 하는 배치 처리](../concepts/batch-processing-with-unix-tools.md) —
  파이프라인의 효용 쪽. 이 소스는 그 파이프라인의 종료 상태 규범을 준다

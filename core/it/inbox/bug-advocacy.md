---
type: concept
title: 버그 옹호
description: 결함을 발견한 사람이 그것이 고쳐지게 하려면 보고를 어떻게 쓰는가를 다룬 장 — 보고를 설득 문서로 규정한 자리, 누구든 보고할 수 있어야 한다며 관문을 여는 쪽의 lesson들, 사소한 버그의 보고를 멈추면 무엇이 따라오는가, 보고의 양을 좁히는 유일한 조항과 그 조건, 판정을 넘지 말라는 선, 두 번째 테스터가 보고를 검토하는 자리와 그 부담 경고, 테스터가 릴리스를 막는 관문이 되지 말라는 같은 책 1장의 조항, 그리고 이 장의 방향이 과잉 보고를 막는 관문이 아니라 보고의 강화라는 이 KB의 판정
generated: { by: "claude-opus-5", at: "2026-08-22T14:00:00Z" }
status: draft
sources:
  - { id: kaner2002-lessons, resource: /it/sources/kaner2002-lessons.md }
---

# 버그 옹호

- [이 소스의 지위](#이-소스의-지위)
- [무엇을 부르는 이름인가](#무엇을-부르는-이름인가)
- [보고는 설득 문서다](#보고는-설득-문서다)
- [관문을 여는 쪽](#관문을-여는-쪽)
- [양을 좁히는 유일한 조항](#양을-좁히는-유일한-조항)
- [보고자가 넘지 말아야 할 선](#보고자가-넘지-말아야-할-선)
- [두 번째 판정자](#두-번째-판정자)
- [관문이 되지 말라](#관문이-되지-말라)
- [이 장의 방향에 대한 이 KB의 판정](#이-장의-방향에-대한-이-kb의-판정)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **결함을 발견한 사람이 그 결함이 고쳐지게 하려면 보고를 어떻게 써야
하고, 보고의 양은 무엇이 제한하는가.**

## 이 소스의 지위

**근거 등급은 실무자 선언(practitioner-manifesto)이다.** 이 장에는 측정도 통제 실험도
없고, 저자들이 겪은 것을 조항으로 적은 것이다. 저자들의 자기 규정과 그 근거 문면은
[맥락 주도 테스팅의 일곱 원칙](../concepts/context-driven-testing-principles.md)의
같은 이름 절이 갖는다. 이 페이지의 어떤 문장도 학술 실증으로 인용되지 않고, **이
장에 실린 경험 추정값은 옮기지 않는다.**

## 무엇을 부르는 이름인가

- 장이 비유 하나로 열린다 (4장, 장 도입 문단).[^kaner2002-lessons]

  > A tester who can't report bugs well is like a refrigerator light that's only on
  > when the door is closed. The situation may be illuminated very well—just not so
  > that it matters.

- **그리고 그 자리에서 이름이 붙는다** — 결과가 나오도록 시험 결과를 쓰고 제시하는 법을
  배우라고 적고, 그것을 **"버그 옹호(bug advocacy)"**라 부른다 (4장, 장 도입
  문단).[^kaner2002-lessons]
- **이름이 이미 방향을 정한다.** 옹호는 억제의 반대말이다. 이 장이 다루는 것은 보고를
  줄이는 법이 아니라 **보고가 힘을 갖게 하는 법**이다.

## 보고는 설득 문서다

- 보고서의 성격을 판매 도구로 규정한다 (4장, lesson 57).[^kaner2002-lessons]

  > Whether you think of it this way or not, your bug report is a sales tool; it's
  > designed to convince people to give up precious resources in order to obtain a
  > benefit that you propose.

- **그러나 보고자의 책임은 수정이 아니라 보고다** (4장, lesson 56).[^kaner2002-lessons]

  > Some bugs will never be fixed. Your responsibility is not to make sure that all bugs
  > are fixed. Your responsibility is to report bugs accurately and in a way that allows
  > the reader to understand the full impact of the problem.

  - **이 두 문장이 한 장 안에 같이 있는 것이 이 장의 구조다.** 보고자는 최대한
    설득력 있게 쓰되 결과를 소유하지 않는다. 판정 권한은 보고자에게 없고 수정 여부를
    정하는 것은 프로그래머나 변경 통제 위원회(Change Control Board)라고 적는다 (4장,
    lesson 58).[^kaner2002-lessons]

## 관문을 여는 쪽

이 장의 lesson 다수가 **보고를 막는 관문을 치우는 쪽**으로 간다.

- **보고할 수 있는 사람에 자격을 두지 않는다** (4장, lesson 60).[^kaner2002-lessons]

  > The testing group should never stand in the way of this communication but should
  > instead always facilitate it, even when—especially when—the complaints come from
  > outside Product Development (including the testing group).

- **이미 보고됐을 것이라는 짐작으로 보고를 건너뛰지 말라고 적는다** — 남들도 같은 짐작을
  하기 때문에 뻔한 버그가 끝내 보고되지 않는 일이 생긴다는 것이다 (4장, lesson
  68).[^kaner2002-lessons]
- **중복 보고를 문제로 세지 않는다** — 같은 버그의 잘 쓰인 보고는 저마다 수정에 도움이
  되는 새 정보를 담고 있고, 중복이 버그 수를 부풀린다고 항의하는 프로젝트 관리자는 그
  버그를 고치게 함으로써 그 문제를 쉽게 해결할 수 있다고 적는다 (4장, lesson
  81).[^kaner2002-lessons]
- **사소한 버그의 보고를 멈추면 무엇이 따라오는지를 적는다** (4장, lesson
  72).[^kaner2002-lessons]

  > At the point that you stop even reporting minor bugs (some companies pressure their
  > staff to report only "worthwhile" errors), you'll find yourself and your company
  > tolerating more and more serious ones.

  - **이 문장은 보고량을 줄이라는 요구를 직접 겨눈다.** "가치 있는 오류만 보고하라"는
    압박이 이 장에서 **회사가 직원에게 가하는 압박**으로, 곧 진단 대상으로 나온다.

## 양을 좁히는 유일한 조항

이 장에서 보고의 양을 좁히는 조항은 하나뿐이고, 그것도 **앞선 조항들에서 물러서는
형식**으로 시작한다 (4장, lesson 78).[^kaner2002-lessons]

> We've told you to report all minor problems and nonreproducible problems. Now we have
> to backtrack a bit and tell you to exercise some judgment in what you report and how
> you report it.

- **비용의 근거는 읽는 사람의 수다** — 보고서를 쓰는 시간에 더해 프로그래머와 프로젝트
  관리자가 읽고, 어떤 회사에서는 변경 통제 위원회 전체가 검토한다고 적는다. 그래서
  사소한 버그 하나를 검토하고 기각하는 데 **사람의 시간이 든다**는 것이다 (4장, lesson
  78).[^kaner2002-lessons] **저자들이 든 구체 값은 경험 추정이므로 이 페이지가 옮기지
  않는다.**
- **경고의 조건이 두 겹이다 — 사소한 버그이고, 프로젝트 후반일 것** (4장, lesson
  78).[^kaner2002-lessons]

  > Late in the project, if you flood the company with minor bug reports, you might
  > single-handedly kill the productivity of the programming and project management
  > teams.

- **처방은 보고를 막는 것이 아니라 흐름을 가르는 것이다** — 후반에 사소한 버그를 무더기로
  보고하게 되면 테스트 관리자와 그룹 방침을 의논하고, 다음 릴리스의 입력으로 정식 검토될
  **별도 데이터베이스**에 넣는 방법을 제안한다 (4장, lesson 78).[^kaner2002-lessons]

  > This preserves your work but gets it out of the way.

  - **곧 이 장의 관문은 보고를 없애는 관문이 아니라 보고를 다른 큐로 보내는 관문이다.**
    보고자의 산출은 보존되고 이번 릴리스의 검토 대상에서만 빠진다.

## 보고자가 넘지 말아야 할 선

양이 아니라 **내용**을 좁히는 조항들은 따로 있고, 이쪽이 이 장에서 더 강하게 적힌다.

- **과장 금지** (4장, lesson 84).[^kaner2002-lessons]

  > Your credibility is fundamental to your influence. If you make the bugs you report
  > seem more serious than they really are, you'll lose influence.

- **원인 규명과 해법 제시 금지** (4장, lesson 85).[^kaner2002-lessons]

  > Your job is to report problems, not to identify root causes and not to push for
  > specific solutions.

  - **이유가 둘 적혀 있다.** 코드를 보지 않은 사람은 원인을 알 자리에 있지 않다는 것이
    하나고, 해법에 사로잡힌 보고자가 **실패 자체에 대한 깨끗하고 정확한 정보를 주지
    못한다**는 것이 둘이다 (4장, lesson 85).[^kaner2002-lessons]
- **모든 버그가 고쳐져야 한다고 우기지 말라** (4장, lesson 97).[^kaner2002-lessons]

  > If you cannot build a case that a bug is important or find a stakeholder who cares
  > enough to actively support your appeal of that particular deferral, we suggest that
  > you leave that bug alone and challenge something else.

  - 이유로 **수정 자체의 위험**을 든다 — 모든 수정은 새 버그를 만들 수 있고, 사소한 버그를
    고치다 더 심각한 것을 만들 수 있으며, 일정 끝에서는 그것을 찾을 시간이 남지 않는다
    (4장, lesson 97).[^kaner2002-lessons]

## 두 번째 판정자

- **보고서를 두 번째 테스터가 검토하는 관행을 적는다** — 필수 정보가 있고 이해 가능한지,
  자기가 재현할 수 있는지, 보고를 더 단순하게·일반화해서·더 강하게 쓸 수 있는지를 묻고,
  문제가 있으면 원 보고자에게 되돌린다 (4장, lesson 90).[^kaner2002-lessons]
- **그리고 같은 자리에 그 대가를 적는다** (4장, lesson 90).[^kaner2002-lessons]

  > This is a useful way to train staff and clarify reports, but beware of overburdening
  > the reviewing testers.

  - **검토자를 세우는 것이 공짜가 아니라는 경고가 검토자를 세우라는 권고와 같은 자리에
    있다.** 그리고 검토자가 매 버그를 재현해야 하는지, 아니면 그럴듯함과 이해 가능성만
    확인하면 되는지를 **정하라고** 요구한다 — 판정 범위를 정하는 것이 이 장의 처방이다.

## 관문이 되지 말라

보고를 어떻게 쓰는가가 아니라 **테스터가 어느 자리에 서는가**를 정하는 조항은 같은 책
1장에 따로 있다. 이 장의 억제 조항을 읽기 전에 이 자리를 먼저 본다.

- **1장 lesson 12의 제목이 "Never be the gatekeeper!"다.** 테스터가 릴리스를 막는
  관문 노릇을 하지 말라는 조항이고, 이유로 **관문을 쥐면 품질의 책임까지 통째로 진다**는
  것을 든다 (1장, lesson 12).[^kaner2002-lessons]
- **그래서 릴리스를 정하는 권한이 어디 있는지를 같은 자리가 못 박는다** (1장, lesson
  12).[^kaner2002-lessons]

  > Ultimately, it's the people who control the project who are best equipped to bear
  > the responsibility to release the product.

- **이것이 이 책에서 검증자의 자리를 정한다.** 검증자는 관문이 아니라 정보 공급자다.
  보고를 억제하는 관문은 이 책의 구도에서 **검증자 쪽이 아니라 수신자 쪽**에 있다.

## 이 장의 방향에 대한 이 KB의 판정

이 절은 원 소스의 주장이 아니라 **이 KB의 판정**이다.

- **이 장은 과잉 보고를 막는 장이 아니다.** 조항의 다수는 보고를 늘리고 강화하는 쪽이고,
  양을 좁히는 조항은 하나이며 그것마저 사소한 버그와 프로젝트 후반이라는 두 조건 아래에
  놓이고 처방은 삭제가 아니라 큐 분리다. **"검증자 과잉 보고 관문"의 근거로 이 장을
  통째로 부르면 방향이 뒤집힌다.**
- **이 장이 실제로 세우는 관문은 양의 관문이 아니라 품질의 관문이다.** 과장 금지·원인
  규명 금지·해법 제시 금지·기각된 버그를 골라 싸우기는 전부 **한 건의 보고가 무엇을
  담아야 하는가**에 걸리는 조항이지 몇 건을 낼 것인가에 걸리는 조항이 아니다.
- **같은 책이 다른 자리에서 검증자를 관문으로 세우는 것 자체를 거부한다** — 위
  [관문이 되지 말라](#관문이-되지-말라)가 그 조항이다. 그래서 이 장의 억제 조항 하나를
  관문의 근거로 세우면 같은 책 1장과 어긋난다.

## LLM 시대의 지위

이 절은 원 소스의 주장이 아니라 **이 KB의 읽기**다. 이 책은 2002년에 사람 테스터를
두고 쓰였고, 저자들이 이 조항들을 자동 판정자에 대고 다시 잰 기록은 이 KB에 없다.

- **같은 물음이 벤더 실무 문면에 다시 나온다.**
  [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md)가
  옮기는 문면은 반박을 목표로 받은 판정자가 **없는 결함까지 보고한다**고 경고하고, 그
  처방으로 판정자를 떼는 대신 **판정 기준을 정확성과 명시된 요구사항으로 좁히라**고 적는다.
- **두 처방의 형태가 같고 손잡이가 다르다.** 이 책은 **어느 큐로 보낼지**를 갈라 과잉을
  흡수하고(위 lesson 78), 벤더 문면은 **무엇을 결함으로 셀지**를 좁혀 과잉을 줄인다.
  둘 다 판정자를 없애지 않는다는 점이 같고, 이 책 쪽은 **보고자의 산출을 버리지 않는
  것**을 명시한다는 점이 다르다.
- #hypothesis **차이가 나는 자리는 보고의 한계 비용이다.** 이 책의 억제 조항은 보고를
  쓰는 사람의 시간이 비싸다는 전제 위에 서지 않는다 — 비싼 것은 **읽는 쪽**이라고 적는다.
  판정자가 사람이 아닐 때 쓰는 쪽의 비용이 거의 사라지므로 읽는 쪽의 부담만 남고, 그러면
  이 장의 균형이 어느 쪽으로 기우는지는 이 책이 답하지 않은 질문이다.
- **lesson 90의 경고는 판정자가 사람이 아니어도 남는다.** 검토자에게 과부하를 주지 말라는
  요구와 검토 범위를 정하라는 요구는 검토자의 종류와 무관한 조항이고, 벤더 문면의 처방이
  가리키는 곳도 같은 자리다.

## 이어지는 페이지

- [맥락 주도 테스팅의 일곱 원칙](../concepts/context-driven-testing-principles.md) — 같은
  책의 다른 호출자. 이 장의 조항들이 왜 규칙이 아니라 lesson으로 적혔는지의 근거
- [에이전트 작업 흐름의 검증자 분리](../concepts/verifier-separation-in-agent-workflows.md) —
  판정자의 과잉 보고를 벤더 실무 문면이 경고하는 자리. 이 페이지와 처방의 형태가 같다
- [테스팅과 체킹의 구분](../concepts/testing-checking-distinction.md) — 이 책의 저자 둘이
  십 년 뒤 자동화의 경계를 낱말로 가른 자리
- [테스팅·체킹은 거짓 이분법이다](../concepts/testing-checking-false-dichotomy.md) — 이 책의
  공저자 한 사람이 십일 년 뒤 그 구분을 같은 학파 안에서 반박한 자리. 무엇을 테스트로 셀
  것인가를 주체가 아니라 물음의 유무로 가른다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  보고할 것이 끝없이 남는다는 비대칭. 이 장의 양 문제가 서 있는 바닥
- [테스트 오라클](../concepts/test-oracle.md) — 무엇을 결함으로 셀 것인가의 판정 근거를
  가른 이론 층. 이 장이 "보고할 만한 것"을 고를 때 기대는 자리
- [테스팅에서 자동화의 경계](../synthesis/automation-boundary-in-testing.md) — 이 갈래의 허브

[^kaner2002-lessons]: Kaner, Bach & Pettichord 2002, *Lessons Learned in Software
    Testing*, 4장 "Bug Advocacy"와 1장 "The Role of the Tester". **확보본이 Wiley 전자책
    판이라 인쇄 쪽 앵커가 하나도 없다** — EPUB 전체에 pagebreak 표식이 0건이므로 locator는
    **장 번호 + lesson 번호**다. 규약의 정본은
    `it/archive/kaner2002-lessons/_progress.yaml` 머리말이다. 4장 도입 문단의 직인용은
    원문에서 첫 낱말이 장식 대문자 때문에 `Atester`로 붙어 추출되는데 이 페이지는 그것을
    `A tester`로 띄어 적었다 — 조판 흔적을 되돌린 것이지 문면을 고친 것이 아니다. 따옴표와
    대시는 이 KB의 문자 규약(NFC)에 맞춰 옮겼고 낱말은 한 자도 바꾸지 않았다. **lesson 78과
    lesson 72에 실린 경험 추정값은 옮기지 않았다** — 근거 등급이 실무자 선언이라 그 값들은
    측정이 아니다. 4장의 나머지 lesson과 이 장 밖의 장들은 이 런의 증류 범위 밖이라 열람만
    했다.

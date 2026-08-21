---
type: concept
title: 에이전트 작업 흐름의 검증자 분리
description: 코딩 에이전트의 벤더 실무 문서가 "일한 에이전트가 채점하지 않는다"를 적어 둔 문면 — 반박을 목표로 주는 두 번째 의견, 방금 쓴 코드에 기울지 않게 하는 새 문맥, 그리고 반박을 시킨 판정자가 없는 결함까지 보고한다는 경고. 벤더 지침이라 근거가 아니라 문면이고, 2026년 8월 18일 개정판 스냅샷에 한정된다
status: draft
generated: { by: "claude-opus-5", at: "2026-08-22T02:20:00Z" }
sources:
  - { id: anthropic2026-claude-code-best-practices, resource: /it/sources/anthropic2026-claude-code-best-practices.md }
---

# 에이전트 작업 흐름의 검증자 분리

하나의 질문: **코딩 에이전트의 벤더 실무 문서는 "생성자가 자기 판정자가 되어서는 안
된다"를 어떤 문면으로 적는가.**

## 이 페이지의 지위 — 근거가 아니라 문면이다

- **소스는 벤더가 자기 제품에 대해 낸 실무 지침(vendor guidance)이다.** 측정도 실험도
  없고 저자는 그 제품을 파는 회사다. 그러므로 이 페이지는 검증자 분리가 **옳다는 근거**를
  대지 않는다 — 대는 것은 그 요구가 실무 문서에 **실제로 이런 낱말로 적혀 있다**는 사실
  하나다. 근거는 [실증과 닿는 자리](#실증과-닿는-자리)의 페이지들이 소유한다.
- **살아있는 문서(living document)이고 이 페이지는 그 문서의 스냅샷 지위를 물려받는다.**
  서술 대상이 활발히 개발 중인 제품이라 개정 압력이 높다. 아래 직인용이 다음 개정에서
  사라져도 이상한 일이 아니다.
- **시대 지위는 LLM 시대의 신규 실무 문면이다.** 고전도 정설도 아니고, "업계가 이렇게
  한다"의 표본 하나다. 다른 벤더가 다르게 적을 수 있다.
- **수치는 옮기지 않는다.** 이 문서에 수처럼 보이는 값이 있어도 그것은 제품 동작에 대한
  벤더의 자기 서술이지 측정이 아니다.

## 버전 조건

> **버전 조건**: 2026년 8월 18일 개정판 문면에 한정된다. 문서 자신이 심은 개정 시각
> (`dateModified`)이 그날이고, 확보 스냅샷(2026년 8월 20일)과 반입 시점 재취득본
> (2026년 8월 22일)의 본문이 한 줄도 다르지 않았다. 아래 직인용은 두 판 모두에 있다.
> **문면이 바뀌면 이 페이지의 claim 하나가 낡는 것이 아니라 페이지 전체가 낡는다.**

## 문서가 적는 세 가지

### 하나 — 일한 에이전트가 채점하지 않는다

- 검증 방법을 네 단계로 늘어놓는 절의 마지막 항목이 **분리**를 적는다. 검증 하위
  에이전트(verification subagent)나 자기 발견을 다시 확인하는 동적 작업 흐름이 하는 일을
  이렇게 규정한다 (절 `Give Claude a way to verify its
  work`):[^anthropic2026-claude-code-best-practices]

  > **By a second opinion**: a verification subagent or a dynamic workflow that checks its
  > own findings has a fresh model try to refute the result, so the agent doing the work
  > isn’t the one grading it.

- **한 문장이 두 가지를 요구한다.** 판정자에게 주는 목표가 확인이 아니라 **반박(refute)**
  이라는 것이 하나이고, **작업한 쪽과 채점하는 쪽이 같은 것이면 안 된다**는 것이 둘이다.
  이 페이지가 검증 축에 서는 자리가 뒤 문장이다.

### 둘 — 새 문맥이 방금 쓴 코드로 기우는 것을 막는다

- 세션을 여럿 돌리는 이유로 **새 문맥(fresh context)**을 든다 (절 `Run multiple Claude
  sessions`):[^anthropic2026-claude-code-best-practices]

  > A fresh context improves code review since Claude won’t be biased toward code it just
  > wrote.

- 적대적 리뷰 단계(adversarial review step)를 다루는 절이 그 기제를 한 문장 더 적는다
  (절 `Add an adversarial review step`):[^anthropic2026-claude-code-best-practices]

  > A reviewer running in a fresh subagent context sees only the diff and the criteria you
  > give it, not the reasoning that produced the change, so it evaluates the result on its
  > own terms.

- **여기서 갈라 두는 것은 모델이 아니라 문맥이다.** 문면이 떼어 내라고 하는 것은 변경을
  낳은 추론 과정이지 판정자의 정체가 아니다. 이 구분이 아래
  [문면이 실증보다 덜 말하는 자리](#문면이-실증보다-덜-말하는-자리)의 출발점이다.

### 셋 — 반박을 시킨 판정자는 없는 결함까지 보고한다

- 같은 절의 마지막 문단이 분리의 **대가**를 경고한다 (절 `Add an adversarial review
  step`):[^anthropic2026-claude-code-best-practices]

  > A reviewer prompted to find gaps will usually report some, even when the work is sound,
  > because that is what it was asked to do. Chasing every finding leads to
  > over-engineering: extra abstraction layers, defensive code, and tests for cases that
  > can’t happen. Tell the reviewer to flag only gaps that affect correctness or the stated
  > requirements, and treat the rest as optional.

- **처방은 판정자를 떼는 것이 아니라 판정 기준을 좁히는 것이다** — 정확성과 명시된
  요구사항에 걸리는 것만 결함으로 세고 나머지는 선택 사항으로 두라고
  적는다.[^anthropic2026-claude-code-best-practices] 분리를 세우면 오검출이 따라온다는
  것을 문서가 먼저 인정하고 그 자리에 완화책을 붙이는 형태다.

## 문면이 실증보다 덜 말하는 자리

- **문면은 `fresh`까지만 말하고 `stronger`를 말하지 않는다.** 위 세 구절의 요구는 판정자가
  새 문맥에서 돌고 반박을 목표로 갖는 것까지이고, 판정자가 작업자보다 **강해야 한다**는
  조건은 어디에도 없다. 실증 쪽이 도달한 조건은 그보다 좁다 —
  [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md)이 이득을 만든
  것은 피드백 주체가 **더 강할 때**였다. 두 서술은 어긋나는 것이 아니라 **문면이 덜
  말하는 것**이고, 이 페이지를 근거로 "다르기만 하면 된다"를 세우면 그것은 문서가 하지
  않은 주장이다.
- **`a fresh model`이 다른 모델을 뜻하는지 같은 모델의 새 인스턴스를 뜻하는지 문면이
  가르지 않는다.** 실무에서 후자로 읽히는 쪽이 흔한데, 그렇다면
  [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md)이 재는 위험이
  그대로 남는다. #hypothesis 이 문면이 이 KB에서 가장 오인용되기 쉬운 자리라고 본다 —
  이것은 문서의 주장이 아니라 이 페이지의 판정이다.
- **각주로 딸려 온 이름 둘은 원문 미확보다.** CriticGPT(테크리포트)와 Osmani의 글은 이
  KB가 원문을 갖고 있지 않다 — **2차 경유**라 이름만 적고 수치는 옮기지 않는다. 특히
  CriticGPT의 두 값은 자연 발생 버그와 삽입 버그라는 **서로 다른 분포**여서 하나의
  범위처럼 이으면 틀린다.

## 실증과 닿는 자리

- [자기인식과 자기선호](../concepts/self-recognition-and-self-preference.md) — 그 논문이
  조건부로 권한 유일한 대응책이 **저자 은닉(authorship obfuscation)**이다. 판정자에게
  누가 썼는지를 숨기는 쪽과, 이 문서처럼 판정자에게서 **쓴 기억 자체를 떼는** 쪽은 같은
  목표를 향한 두 손잡이다
- [자기 수정의 피드백 병목](../concepts/self-repair-feedback-bottleneck.md) — "일한
  에이전트가 채점하지 않는다"의 실측 층. 그쪽은 판정자를 갈아 끼웠을 때 하류 성능이 얼마나
  달라지는지를 재고, **더 강한 판정자**라는 조건까지 좁힌다
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md) — 판정자를 다른
  모델로 바꿔도 오답이 겹치면 남는 위험. 위 `fresh model`의 모호함이 걸리는 자리
- [독립 판본의 상관된 실패](../concepts/correlated-failure-of-independent-versions.md) —
  독립적으로 만든 것들이 독립적으로 틀리지 않는다는 같은 물음의 프로그램 판본 층. 이
  문서가 실무 문면으로 요구하는 분리가 그 고전이 반증한 가정 위에 서 있다

[^anthropic2026-claude-code-best-practices]: Anthropic 2026, "Best practices for Claude
    Code", `code.claude.com/docs/en/best-practices`. **벤더 제품 문서이고 학술 근거가
    아니다.** 웹 문서라 쪽수가 없어 locator는 **절 제목**을 쓴다(절 제목이 곧 URL 앵커다).
    이 페이지가 담은 절은 `Give Claude a way to verify its work`·`Run multiple Claude
    sessions`·`Add an adversarial review step` 셋이고, 나머지 절(문맥 관리·CLAUDE.md·
    권한·훅·스킬·하위 에이전트 정의·비대화식 실행 등)은 이 KB의 검증 축 물음이 아니라
    담지 않았다. 문서가 인쇄한 수치는 어느 것도 옮기지 않았다. 판본과 열람 시점,
    그리고 이 문서를 인용할 때의 금지 사항은
    [소스 메타](../sources/anthropic2026-claude-code-best-practices.md)에 적어 두었다.

---
type: concept
title: 벤치마크의 수명과 철회
description: 한 벤치마크가 표준이 되었다가 만든 쪽 손에 철회되기까지를 두 원문으로 붙여 읽는 자리 — 2,294문항을 12개 파이썬 저장소의 병합 PR에서 3단계로 걸러 낸 구성 절차와 fail-to-pass·pass-to-pass 두 테스트 집합, 전부 통과해야 푼 것으로 세는 % resolved 지표, 원전이 오염을 걱정하지 않아도 된다고 적은 근거, 그리고 2026년 벤더 감사가 어려운 문항 138개에서 찾아낸 결함 테스트 비율과 세 모델의 gold patch 축자 재현, 무엇을 권고했고 이 KB가 어느 수치를 옮기지 않는지
generated: { by: "claude-opus-5", at: "2026-08-22T10:00:00Z" }
sources:
  - { id: jimenez2024-swebench, resource: /it/sources/jimenez2024-swebench.md }
  - { id: openai2026-swebench-verified-retire, resource: /it/sources/openai2026-swebench-verified-retire.md }
---

# 벤치마크의 수명과 철회

- [버전 조건](#버전-조건)
- [두 소스의 지위](#두-소스의-지위)
- [표준이 된 경위 — 무엇을 어떻게 만들었나](#표준이-된-경위--무엇을-어떻게-만들었나)
- [무엇을 재는가 — 두 테스트 집합과 % resolved](#무엇을-재는가--두-테스트-집합과--resolved)
- [당시 모델이 실제로 낸 값](#당시-모델이-실제로-낸-값)
- [원전은 오염을 걱정하지 않아도 된다고 적었다](#원전은-오염을-걱정하지-않아도-된다고-적었다)
- [그 사이에 있었던 것 — Verified 500문항](#그-사이에-있었던-것--verified-500문항)
- [드러난 것 하나: 테스트가 옳은 답을 거부한다](#드러난-것-하나-테스트가-옳은-답을-거부한다)
- [드러난 것 둘: 오염](#드러난-것-둘-오염)
- [철회문이 권고한 것](#철회문이-권고한-것)
- [이 KB가 옮기지 않는 수치](#이-kb가-옮기지-않는-수치)
- [이 KB의 읽기: 수치에는 유통기한이 있다](#이-kb의-읽기-수치에는-유통기한이-있다)
- [두 소스의 사각](#두-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **한 벤치마크가 표준이 되었다가 더는 쓸 수 없게 되기까지 무슨 일이
일어나며, 그것을 어떻게 알아차리는가.**

[공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md)가 벤치마크는
포화되며 새것으로 갈린다는 일반론을 세운다면, 이 페이지는 **그 갈림의 처음과 끝을 각각
원문으로 가진 한 사례**다. 2024년 심사 논문이 그 벤치마크를 세우고, 2026년 벤더 보고가
그 파생판을 스스로 내린다. 두 문서 사이의 거리가 이 페이지의 내용이다.

## 버전 조건

> **버전 조건**: 앞쪽 절반은 **SWE-bench 원전**(2,294문항 · 파이썬 저장소 12개 ·
> 2023년 8월 PyPI 내려받기 순위로 고른 저장소)이고, 결과 표의 모델군은 ChatGPT-3.5
> (`gpt-3.5-turbo-16k-0613`) · GPT-4(`gpt-4-32k-0613`) · Claude 2 · SWE-Llama 7b·13b에
> 확보본 v3의 표가 더한 Claude 3 Opus · GPT-4-turbo까지, **2023년부터 2024년 초에
> 걸친다.** 뒤쪽 절반은 **2026년 2월 시점의 벤더 감사**이고 대상은 원전이 아니라
> 그 파생판인 SWE-bench Verified 500문항이다. 감사 실행 모델은 OpenAI o3, 오염 탐침
> 대상은 GPT-5.2-Chat · Claude Opus 4.5 · Gemini 3 Flash Preview다. **두 절반의 절대
> 수치는 서로 비교되지 않는다** — 데이터셋도 분모도 다르다.

## 두 소스의 지위

이 페이지는 성격이 다른 문서 둘을 한자리에 놓는다. **등급이 다르면 무게도 다르다.**

| | 원전 | 철회문 |
|---|---|---|
| 소스 | [jimenez2024-swebench](../sources/jimenez2024-swebench.md) | [openai2026-swebench-verified-retire](../sources/openai2026-swebench-verified-retire.md) |
| 근거 등급 | **심사 실증(`peer-reviewed`)** | **산업 보고(`industry report`) — 벤더 자기 보고** |
| 근거의 근거 | 확보본 52쪽 전 쪽 쪽머리 `Published as a conference paper at ICLR 2024` | 심사 없음. 저자가 평가 대상 모델을 파는 회사다 |
| 수치의 지위 | 논문이 스스로 잰 값 | **OpenAI가 스스로 잰 값** |

- **철회문의 수치는 어느 것도 학술 근거로 쓰지 않는다.** 이 페이지가 옮기는 값은 전부
  "OpenAI가 자기 감사에서 이렇게 셌다"는 형태이고, 독립 검증을 거치지 않았다.
- **철회문에는 이해가 걸린 자리가 둘이다.** 이 회사는 철회 대상인 Verified 부분집합을
  **자기가 만들었고**, 대안으로 권하는 벤치마크의 점수로 자기 모델을 보고한다. 감사의
  근거 자체를 무르게 만들지는 않지만 권고를 읽을 때 붙일 조건이다.
- **시대 지위는 둘 다 LLM 시대의 문서다.** 고전의 재확증이 아니라, 판정 대상이 모델일
  때만 성립하는 물음을 재려고 만든 장치와 그 장치의 폐기 기록이다.

## 표준이 된 경위 — 무엇을 어떻게 만들었나

- **무엇을 모았는가** (초록, p.1):[^jimenez2024-swebench]

  > we introduce SWE-bench, an evaluation framework consisting of 2,294 software
  > engineering problems drawn from real GitHub issues and corresponding pull requests
  > across 12 popular Python repositories.

- **저장소를 고른 기준** — 2023년 8월 기준 내려받기 상위 5,000개 PyPI 라이브러리 목록에서
  상위 100개를 잡고, 대응하는 오픈소스 GitHub 저장소를 찾고, 자유 사용을 허용하는
  라이선스인지 확인한 뒤 GitHub 개발자 API로 모든 PR을 모았다 (§A.1,
  p.16).[^jimenez2024-swebench] 인기 저장소를 고른 이유는 문서·기여 지침·코드 품질이
  대체로 낫기 때문이라고 논문이 적는다 (§2.1, p.2).
- **3단계로 걸렀다** (§2.1, pp.2–3).[^jimenez2024-swebench]

  | 단계 | 무엇을 남기는가 |
  |---|---|
  | 1. PR 수집 | 파이썬 저장소 12개에서 약 90,000건 |
  | 2. 속성 필터 | **병합된**(merged) PR · 이슈를 하나 이상 닫음 · 테스트 파일을 고침 |
  | 3. 실행 필터 | 설치가 되고, PR 적용 전후로 상태가 **실패에서 통과로 바뀌는 테스트가 하나 이상** 있음 |

  이 세 단계를 지나 90,000건이 2,294건이 됐다 (§2.1, p.3).[^jimenez2024-swebench]
- **실행 필터가 버리는 양이 크다** — 검증 절차의 어느 한 단계라도 실패하면 후보에서
  뺐고, 저장소마다 차이는 있으나 **이 단계가 대체로 후보의 절반을 없앤다**고 적는다
  (§A.3, p.19).[^jimenez2024-swebench]
- **사람이 못 풀 과제를 미리 뺐다** — 해답 패치가 새로 만든 함수·클래스를 테스트가
  호출하는 경우는 제외했다. 그런 이름은 임의로 지어지고 문제 서술에 명시되지 않아
  **사람 개발자에게도 불가능한 과제**가 되기 때문이다 (§A.1, p.16).[^jimenez2024-swebench]
  **뒤에 나올 철회문의 감사가 정확히 이 자리를 다시 짚는다.**
- **과제 하나의 크기** (Table 1, p.4).[^jimenez2024-swebench] 저장소별로 묶지 않은
  미시 평균(micro-average)이다.

  | | 평균 | 최대 |
  |---|---|---|
  | 이슈 텍스트 길이(낱말) | 195.1 | 4,477 |
  | 코드베이스 파일 수(테스트 제외) | 3,010 | 5,890 |
  | 코드베이스 줄 수(테스트 제외) | 438K | 886K |
  | 정답 패치가 고친 줄 수 | 32.8 | 5,888 |
  | 정답 패치가 고친 파일 수 | 1.7 | 31 |
  | fail-to-pass 테스트 수 | 9.1 | 1,633 |
  | 전체 테스트 수 | 120.8 | 9,459 |

- **Lite 부분집합도 이 논문 안에 있다** — 300문항이고 원래 12개 저장소 중 11개를
  덮는다. 더 자립적인 문항을 골라 기능 버그 수정 평가에 초점을 맞췄다고 적는다
  (§2.4, pp.3–4).[^jimenez2024-swebench] **다만 그 필터 기준은 게재본에 실려 있지
  않다** — 아래 [사각](#두-소스의-사각)을 보라.

## 무엇을 재는가 — 두 테스트 집합과 % resolved

- **테스트가 두 갈래다** (Table 9, p.17).[^jimenez2024-swebench]

  > FAIL TO PASS (list) List of tests that change in status from *fail* to *pass*
  >
  > PASS TO PASS (list) List of tests that change in status from *pass* to *pass*

- **두 갈래가 하는 일이 다르다** (§A.5, p.21):[^jimenez2024-swebench]

  > Unlike *fail* to *pass* tests that are intended to characterize the problem statement
  > *P* and determine if a revision addresses the issue, *pass* to *pass* tests are
  > included to ensure that the revision does not break or violate any existing expected
  > behavior.

  곧 fail-to-pass는 **이슈가 실제로 닫혔는가**를, pass-to-pass는 **다른 것을 깨뜨리지
  않았는가**를 맡는다. 전자가 수용 오라클, 후자가 보존 오라클 자리다.
- **지표는 통과 비율이 아니라 전량 통과한 과제의 비율이다** (§2.2,
  p.3):[^jimenez2024-swebench]

  > If the patch applies successfully and all of these tests pass we consider the
  > proposed solution to have successfully resolved the issue. The metric for our
  > benchmark is the percentage of task instances that are resolved.

  부록이 같은 말을 더 좁게 적는다 — `a task is considered solved if all tests across
  FAIL TO PASS and PASS TO PASS pass`이고, 테스트가 **없거나** 통과가 아니면 실패로
  센다 (§A.4, p.21).[^jimenez2024-swebench]
- **모델은 테스트를 보지 못한다.** 입력은 이슈 텍스트와 코드베이스뿐이고, 출력은 패치
  파일이다 (§2.2, p.3).[^jimenez2024-swebench] 철회문도 같은 조건을 다시 적는다
  (Background 절).[^openai2026-swebench-verified-retire]
- **논문이 스스로 세운 견고성 근거** (§2.3, p.3):[^jimenez2024-swebench] 과제마다
  fail-to-pass 테스트가 최소 하나 있고 40%는 둘 이상 있으며, 기존 동작이 유지되는지
  확인하는 추가 테스트가 **중앙값 51개** 함께 돈다. 곧 **판별력의 근거를 테스트 개수로
  세운 것**이고, 그 근거가 뒤에 무엇에 걸려 넘어지는지가 이 페이지의 뒤쪽 절반이다.

## 당시 모델이 실제로 낸 값

**아래 값에는 검색 설정이 반드시 붙는다** — 같은 모델의 % Resolved가 설정마다 다르다.

- **BM25 검색으로 관련 파일을 찾아 넣었을 때** (Table 5, p.6).[^jimenez2024-swebench]
  분모는 SWE-bench 2,294문항과 Lite 300문항이고, 단위는 전량 통과한 과제의 비율(%)이다.

  | 모델 | SWE-bench % Resolved | SWE-bench % Apply | Lite % Resolved | Lite % Apply |
  |---|---|---|---|---|
  | Claude 3 Opus | 3.79 | 46.56 | 4.33 | 51.67 |
  | Claude 2 | 1.97 | 43.07 | 3.00 | 33.00 |
  | ChatGPT-3.5 | 0.17 | 26.33 | 0.33 | 10.00 |
  | GPT-4-turbo | 1.31 | 26.90 | 2.67 | 29.67 |
  | SWE-Llama 7b | 0.70 | 51.74 | 1.33 | 38.00 |
  | SWE-Llama 13b | 0.70 | 53.62 | 1.00 | 38.00 |

- **논문의 요약 문장** (§5, p.6):[^jimenez2024-swebench]

  > Across the board, models struggle significantly to resolve issues. The best
  > performing model, Claude 2, is only able to resolve 1.96% of the issues.

  **산문의 `1.96%`와 Table 5의 `1.97`이 어긋난다.** 이 페이지는 표 값을 쓰고 직인용에서만
  원문 표기를 남긴다.
- **정답이 고친 파일만 골라 넣어 주면 오른다** — "oracle" 검색 설정에서 Claude 2가
  `4.80`, SWE-Llama 13b가 `3.97`, SWE-Llama 7b가 `3.01`, GPT-4가 `1.74`,
  ChatGPT-3.5가 `0.52`다 (Table 18, p.25).[^jimenez2024-swebench] 논문 스스로 이
  설정을 **덜 현실적**이라고 적는다 — 이슈를 다루는 엔지니어가 어느 파일을 고쳐야 할지
  미리 알 수는 없기 때문이다 (§4.1, p.5).
- **GPT-4의 값은 분모가 다르다.** 예산 제약으로 "Oracle"과 BM25 27k 설정에서는
  SWE-bench의 **25% 무작위 부분집합**에만 평가됐다 (Table 7 주석 p.7 · Table 18 주석
  p.25).[^jimenez2024-swebench]
- **읽히는 것** — 2023~2024년 초 최상위 모델의 해결률이 한 자릿수 초반이었다. 곧 이
  벤치마크는 **바닥에서 출발했고**, 그래서 오랫동안 진보를 잴 여유가 있어 보였다.

## 원전은 오염을 걱정하지 않아도 된다고 적었다

이 절이 두 문서를 잇는 이음매다. **원전은 오염을 물음으로 세웠고, 자기 데이터로 답했다.**

- **설계상의 대비책** (§2.3, p.3):[^jimenez2024-swebench]

  > Therefore, we can extend SWE-bench with a continual supply of new task instances and
  > evaluate LMs on issues created after their training date, which ensures that the
  > solution was not included in their training corpus.

  곧 오염 대책은 **계속 새 문항을 뽑는 것**이고, 그 능력이 이 벤치마크의 자랑이었다.
- **훈련 데이터 쪽에서도 갈랐다** — SWE-Llama의 훈련 집합은 평가 벤치마크와 **저장소가
  겹치지 않는** 37개 저장소에서 뽑았다 (§3, p.4).[^jimenez2024-swebench]
- **그리고 실측으로 답했다** (§5, p.7):[^jimenez2024-swebench]

  > **Difficulty does not correlate with issue resolution date.** [...] We find that for
  > most models there’s little difference in performance before or after this date, with
  > the exception of GPT-4. We consider this result to be largely promising as it
  > suggests that despite models having been exposed to some version of an repository’s
  > codebase, they are unlikely to “cheat” to address issues simply by generating a more
  > recent version of the repository.

  분모는 "oracle" 검색 설정의 과제를 2023년 이전과 이후로 가른 두 무리이고, 값은
  Table 7(p.7)에 있다. 부록 §C.4는 같은 분석을 6개 연도 구간으로 늘려 **성능과 연도
  사이에 일관된 상관이 없다**고 적는다 (p.25).[^jimenez2024-swebench]
- **이 진단이 무엇을 재는지 보라.** 잰 것은 **연도별 해결률의 차이**이지, 모델이 정답
  패치를 기억하는지가 아니다. 2년 뒤 철회문이 잰 것이 정확히 후자다 — 같은 물음에
  **다른 검사를 붙이자 반대 답이 나왔다.**

## 그 사이에 있었던 것 — Verified 500문항

**원전과 철회문 사이에 파생판이 하나 있고, 그 존재를 이 KB는 철회문 문면으로만 안다.**
"Introducing SWE-bench Verified"(OpenAI, 2024)는 이 KB가 확보하지 않았으므로 이름만
적는다.

- **왜 만들었는가** (Background 절).[^openai2026-swebench-verified-retire] 철회문은 원래
  평가에서 모델의 역량이 **과소 보고**될 수 있는 문제 셋을 찾았다고 적는다.

  > Some unit tests were overly specific or misaligned with the task so correct fixes
  > could be rejected.
  >
  > Many task statements were underspecified, which could lead to multiple valid
  > interpretations - while the tests only covered a specific one.
  >
  > Depending on setup of the environment (for example Linux vs Windows, or the python
  > version), some tests could spuriously fail

- **어떻게 만들었는가** (Background 절):[^openai2026-swebench-verified-retire]

  > We created SWE-bench Verified in 2024 to address these issues. We worked with expert
  > software engineers to review 1,699 SWE-bench problems and filter out problems that
  > had these issues. Each problem was reviewed by three experts independently. This
  > review process resulted in SWE-bench Verified, a curated set of 500 problems.

  분모는 검토 대상 1,699문항, 검토자는 문항당 독립 3인, 산출은 500문항이다. **전부
  OpenAI 자기 보고다.**
- **그리고 그것이 표준이 됐다** (도입 문단):[^openai2026-swebench-verified-retire]

  > Since we first published SWE-bench Verified in August 2024, the industry has widely
  > used it to measure the progress of models on autonomous software engineering tasks.
  > After its release, SWE-bench Verified provided a strong signal of capability
  > progress and became a standard metric reported in frontier model releases.

## 드러난 것 하나: 테스트가 옳은 답을 거부한다

- **감사의 설계** (Too narrow and too wide tests 절):[^openai2026-swebench-verified-retire]

  > We conducted an audit of 138 SWE-bench Verified problems that OpenAI o3 did not
  > consistently solve over 64 independent runs. Each case was independently reviewed by
  > at least six experienced software engineers. If an expert flagged an issue, it was
  > re-verified by an additional team.

- **분모가 무작위 표본이 아니다 — 이 단서를 떼면 수치가 틀린 말이 된다.** 138문항은
  Verified 500문항에서 **o3가 64회 독립 실행에서 일관되게 풀지 못한** 것들이다. 곧
  어려운 쪽으로 치우친 표본이고, 아래 비율을 "Verified의 59.4%가 결함"으로 읽으면
  원문이 하지 않은 주장이 된다.
- **결과** (같은 절):[^openai2026-swebench-verified-retire]

  > We found that 59.4% of the 138 problems contained material issues in test design
  > and/or problem description, rendering them extremely difficult or impossible even for
  > the most capable model or human to solve.

  **분모는 138이고 단위는 비율값(%)이다.** 갈래는 셋이고 같은 절이 이어 적는다 — 구현
  세부를 강제해 기능적으로 옳은 제출을 무효로 만드는 **좁은 테스트**(narrow test cases)가
  35.5%, 문제 서술에 없는 기능까지 검사하는 **넓은 테스트**(wide test cases)가 18.8%,
  분류에 들어맞지 않는 나머지가 5.1%다.
- **좁은 테스트의 실물** — `pylint-dev__pylint-4551`에서 정답 PR이 `get_annotation`이라는
  새 함수를 만드는데, **그 이름은 문제 서술에 없고** 테스트는 그 이름을 직접 임포트한다.
  그래서 기능적으로 옳은 여러 해답이 임포트 오류로 떨어진다 (같은
  절).[^openai2026-swebench-verified-retire]
- **넓은 테스트의 실물** — `sympy__sympy-18199`의 원 PR은 이슈 셋을 함께 고치는데
  Verified 과제의 서술은 그중 **하나만** 담는다. 테스트는 셋 전부를 검사하므로, 모델이
  서술된 수정을 옳게 해내고도 나머지 둘의 테스트에서 떨어진다 (같은
  절).[^openai2026-swebench-verified-retire]
- **이 결함은 원전이 이미 알고 막으려 했던 자리다.** 원전은 정답이 새로 만든 이름을
  테스트가 호출하는 과제를 "사람에게도 불가능"이라며 제외했고 (§A.1,
  p.16),[^jimenez2024-swebench] Verified는 전문가 3인 검토로 같은 부류를 다시 걸렀다.
  **두 겹의 필터를 지나고도 남았다**는 것이 이 감사의 내용이다.

## 드러난 것 둘: 오염

- **처음 눈치챈 경로** (Contamination 절):[^openai2026-swebench-verified-retire] 자기
  모델에서 먼저 보였다 — GPT-5.2가 **거의 풀 수 없다고 판정해 둔 과제 31개를 풀었다.**
  `django__django-14725`에서 테스트는 문제 서술이 요구하지 않은 `edit_only` 매개변수를
  요구하는데, 모델의 사고 사슬(chain of thought)에 그 매개변수가 Django 4.1에서 도입됐다는
  정보가 그대로 나온다.

  > There is also `edit_only` parameter maybe added around 4.1 or 4.2. Since this is 4.1
  > dev 2022, the code might be before introduction. We will implement now. Hidden tests
  > will check new behavior.

- **그다음 자동 탐침을 세웠다** (같은 절):[^openai2026-swebench-verified-retire] Verified
  문항마다 GPT-5에게 GPT-5.2-Chat · Claude Opus 4.5 · Gemini 3 Flash Preview를 캐묻게
  했다. 탐침에게 준 것은 과제 ID·설명·gold patch·PR 테스트이고, 15턴 동안 시스템/개발자
  프롬프트·사용자 프롬프트·어시스턴트 프리필을 바꿔 가며 유도했다. 턴마다 판정 모델이
  **새로 드러난 과제 특정 정보의 양**을 매기고 오염 강도를 `none`에서 `strong`까지
  라벨링했으며, `strong` 사례는 사람이 다시 봤다.
- **저자가 붙인 단서** (같은 절):[^openai2026-swebench-verified-retire] 세 모델은
  **추론 모델을 빼려고** 고른 구성이고, 그 사이에 무시할 수 없는 역량 차가 있을 것이라고
  문서가 스스로 적는다.
- **세 사례가 무엇을 보였는가** (GPT-5.2 · Claude Opus 4.5 · Gemini 3 Flash
  절):[^openai2026-swebench-verified-retire] 셋 다 **gold patch의 문면을 되뱉는다.**
  GPT-5.2는 서술 한 조각만 주었는데 정확한 클래스·메서드 이름과 새로 들어간 조기 반환
  조건을 내놓았고, Claude Opus 4.5는 4줄짜리 변경과 파일 경로에 더해 **diff 안의 인라인
  주석까지 축자로** 인용했으며, Gemini 3 Flash는 과제 ID만으로 문제 서술과 gold patch를
  축자로 냈다.
- **결론 문장** (도입 문단):[^openai2026-swebench-verified-retire]

  > This means that improvements on SWE-bench Verified no longer reflect meaningful
  > improvements in models’ real-world software development abilities. Instead, they
  > increasingly reflect how much the model was exposed to the benchmark at training
  > time. This is why we have stopped reporting SWE-bench Verified scores, and we
  > recommend that other model developers do so too.

- **두 결함이 서로를 키운다** — 문서는 오염된 모델이 **더 잘 통과한다**고 적는데, 그
  이유가 실력이 아니라 **명세가 덜 규정된 테스트를 통과하는 데 필요한 추가 정보**를
  갖고 있어서다 (도입 문단).[^openai2026-swebench-verified-retire] 곧 좁은·넓은 테스트가
  만든 빈틈을 오염이 정확히 메운다.

## 철회문이 권고한 것

- **첫째 교훈 — 공개된 재료로 만든 벤치마크는 오염을 안고 태어난다**
  (Discussion 절):[^openai2026-swebench-verified-retire]

  > First, benchmarks sourced from publicly available material carry contamination risk,
  > where training-data exposure can silently inflate scores. If publicly crawled data is
  > used in benchmark construction, model developers should perform additional tests for
  > contamination. Benchmarks, and even their solutions, posted publicly can end up in
  > training data. Extra care should be taken both in how datasets are posted (i.e.
  > password protected) and training data filtering (i.e. strict adherence to canary
  > strings).

- **둘째 교훈 — 자동 채점은 제대로 만들기 어렵다** (같은
  절):[^openai2026-swebench-verified-retire]

  > Second, automated scoring is tricky to get right; perfect test cases should fully
  > verify correct functionality, being both agnostic to specific unimportant
  > implementation details and also robust to shortcut solutions. These problems are
  > inherently complex and difficult to solve. Catching these problems took multiple
  > extensive human labeling campaigns.

  **좋은 테스트의 두 조건이 서로 반대 방향이다** — 중요하지 않은 구현 세부에는
  무관심해야 하고(좁아지지 않기), 동시에 지름길 해답에는 견고해야 한다(넓어지지 않기).
  감사가 센 35.5%와 18.8%가 각각 그 두 조건이 깨진 자리다.
- **대안 권고** (같은 절):[^openai2026-swebench-verified-retire] 최근 몇 달간 SWE-bench
  Pro의 공개 분할로 결과를 보고해 왔고 다른 모델 개발자에게도 그러기를 권한다. 단서를
  같은 자리에 적는다 — `SWE-bench Pro is not perfect, but empirically seems to suffer
  less from contamination issues`이고, 자기 오염 파이프라인이 거기서도 사례를 찾았으나
  **훨씬 드물고 덜 심했으며 gold patch 전문을 축자로 낸 모델은 없었다.**
- **긴 답은 비공개 저작이다** (같은 절):[^openai2026-swebench-verified-retire] 도메인
  전문가가 **비공개로 문항을 쓰고** 훈련된 평가자가 총체적으로 채점하는 방식(GDPval)을
  들며, 자원이 많이 들지만 점점 필요해진다고 적는다.
- **`SWE-bench Pro`와 `GDPval`은 이 KB가 이름만 안다.** 두 벤치마크의 원문을 확보하지
  않았으므로 수치도 설계도 옮기지 않는다.

## 이 KB가 옮기지 않는 수치

**철회문에서 가장 자주 인용될 값 하나를 이 페이지는 싣지 않는다.**

- **`74.9%`에서 `80.9%`로라는 진보 둔화 수치를 쓰지 않는다.** 그 값은 (1) 본문 절이
  아니라 목차 위 요약에만 있고, (2) `improving`이라는 낱말에 걸린 링크가
  `llm-stats.com`의 리더보드 집계를 가리킨다. 곧 **OpenAI가 잰 값이 아니라 제3자
  집계**이고, 이 KB는 그 리더보드를 원전으로 확인하지 않았다. 옮길 수 있는 것은 방향뿐
  — 철회문은 최고 점수의 진보가 느려진 것을 감사의 출발점으로 삼는다.
- **요약의 `27.6% subset`도 쓰지 않는다.** 대신 본문 두 절이 각각 적는 원값을 쓴다 —
  감사 대상 **138문항**(Too narrow and too wide tests 절)과 Verified **500문항**
  (Background 절)이다.[^openai2026-swebench-verified-retire]
- **요약의 `at least 59.4%` 대신 본문 절의 `59.4%`를 쓴다.** 같은 값이지만 한정어가
  다르고, 본문 절이 분모와 함께 적는다.
- **원전 쪽에서는 서론·동기의 값을 쓰지 않았다.** 이 페이지의 모든 결과 수치는 Table 1·
  Table 5·Table 18·Table 7에서 왔고, 산문 인용은 직인용 블록으로만 남겼다.

## 이 KB의 읽기: 수치에는 유통기한이 있다

**두 문서를 붙여 놓았을 때만 보이는 것이 이 절이다.**

- **같은 벤치마크가 2년 사이에 세 지위를 지났다** — 아무도 못 푸는 도전 과제(2023~2024년
  초, 최상위 해결률 한 자릿수 초반), 업계 표준 지표(2024년 8월 이후), 그리고 만든 쪽이
  더는 보고하지 않는 폐기 대상(2026년 2월). **어느 시점의 점수를 인용하는지가 그
  점수의 뜻을 바꾼다.**
- **벤치마크의 자기 진단은 검사가 미치는 데까지만 참이다.** 원전은 오염을 물었고
  연도별 해결률 차이로 답했다 (§5, p.7).[^jimenez2024-swebench] 그 검사로는 문제가
  보이지 않았다. 철회문은 같은 물음에 **모델에게 정답 패치를 되뱉게 하는 검사**를
  붙였고 세 계열 모두에서 나왔다 (Contamination
  절).[^openai2026-swebench-verified-retire] **검사가 못 보는 것이 없다는 뜻이 아니라는
  것을, 없다고 적은 쪽이 나중에 확인한 사례다.**
- **테스트 부족과 오염은 같은 벤치마크에서 함께 나온다.**
  [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md)이 HumanEval에서
  잰 것은 테스트가 **못 갈라서** 통과율이 부푼다는 쪽이고, 이 페이지의 철회문이 잰 것은
  테스트가 **너무 좁거나 너무 넓어서** 옳은 답이 떨어진다는 쪽이다. 방향이 반대인 같은
  병이다 — 둘 다 통과 여부가 코드의 옳음을 대리하지 못한다는 뜻이고, 철회문의 둘째
  교훈이 두 방향을 한 문장에 담는다.
- **[데이터 오염](../concepts/data-contamination.md)이 일반론으로 적은 것의 실물이다.**
  거기서 "벤치마크는 공개되는 순간 유용하기를 그친다"는 재담과 오염 제거가 파운데이션
  모델 시대에 성립하지 않는다는 진단이 이미 있었다. 이 페이지의 철회문은 **그 진단이
  구체적인 한 벤치마크에서 실현된 기록**이고, 대책으로 비밀번호 보호·canary 문자열·
  비공개 저작을 든다.
- **[ImpossibleBench](../concepts/test-case-exploitation-by-agents.md)가 이 벤치마크
  위에 서 있다.** 그 논문의 Impossible-SWEbench는 SWE-bench Verified에서 만든
  349문항이다. 곧 **철회된 데이터셋을 기반으로 삼은 측정**이므로, 그 값을 읽을 때 이
  페이지의 오염 진단이 함께 걸린다. 다만 그 논문이 재는 것은 통과율이 아니라 치팅률이라
  오염의 영향 방향이 자명하지 않다. #hypothesis 오염이 정직한 해를 쉽게 만들어 치팅률을
  **낮추는** 쪽으로 작용할 수도 있는데, 두 소스 어느 쪽도 이 상호작용을 다루지 않는다.
- **그래서 인용 규율은 이렇다.** 벤치마크 점수를 근거로 쓸 때는 (1) 어느 판인지
  (원전 2,294문항인가 Verified 500문항인가 Lite 300문항인가), (2) 어느 시점인가,
  (3) 그 시점 이후에 그 벤치마크에 대한 감사·철회 고지가 있었는가를 함께 확인한다.
  셋째 항목이 이 페이지가 더하는 것이다 — 근거는
  [LLM 실증 연구의 보고 규범](../concepts/llm-empirical-study-reporting-norms.md)이
  요구하는 모델 판·실행 시점 명시와 같은 축이고, 그 축을 **벤치마크 쪽으로** 돌린 것이다.

## 두 소스의 사각

- **원전의 부록 A.7이 문장 중간에서 끊겨 있다** —
  `SWE-bench Lite is a canonical subset for more efficient evaluation of languag models
  on the SWE-bench task. SWE-bench is`에서 절이 끝나고 바로 부록 B가 시작한다 (p.25).
  본문 §2.4도 같은 자리에서 참조 대상이 빠진 채 두 문장이 이어 붙어 있다 (p.4).
  [^jimenez2024-swebench] **곧 Lite 300문항의 필터 기준은 게재본에 실려 있지 않다.**
- **원전의 결과 표와 모델 목록이 어긋난다.** §4.3(p.5)은 평가 모델을 ChatGPT-3.5·GPT-4·
  Claude 2·SWE-Llama로 세는데 Table 5(p.6)에는 Claude 3 Opus와 GPT-4-turbo 행이 있다.
  [^jimenez2024-swebench] 논문은 그 차이를 설명하지 않는다.
- **원전은 파이썬 한 언어다.** 한계 절이 스스로 적는다 — 전 과제가 파이썬이고 다른
  언어·도메인으로 넓히는 것은 향후 과제다 (§7, p.10).[^jimenez2024-swebench]
- **원전의 마지막 한계 진술이 뒤의 사태를 정확히 예고한다** (§7,
  p.10):[^jimenez2024-swebench]

  > while this work evaluates models using execution-based code testing, relying solely
  > on this method is insufficient to guarantee reliable performance of model generations

- **철회문은 심사도 재현 자료도 없다.** 감사 대상 138문항의 목록, 오염 탐침의 전체
  결과 분포, 판정 모델의 정확도가 공개되지 않는다. 이 KB가 확인할 수 있는 것은 **문면과
  거기 실린 사례 다섯**뿐이다.
- **철회문은 자기 감사의 오검출률을 적지 않는다.** 전문가 6인 이상이 독립 검토했고
  깃발이 서면 다른 팀이 재검증했다고만 적을 뿐, 검토자 사이의 일치도도 재검증에서
  뒤집힌 비율도 없다 (Too narrow and too wide tests
  절).[^openai2026-swebench-verified-retire]
- **오염 탐침의 분모가 없다.** 세 모델에서 `strong` 라벨이 몇 건 나왔는지, 500문항 중
  몇 문항이 오염됐는지가 적혀 있지 않다. 문서가 적는 것은 **시험한 프론티어 모델
  전부에서 나왔다**는 정성 진술과 사례 셋이다 (도입 문단 · Contamination
  절).[^openai2026-swebench-verified-retire]
- **두 문서는 같은 대상을 재지 않는다.** 원전은 2,294문항, 철회문은 그 파생판 500문항이
  대상이다. 원전 쪽 2,294문항이 지금 어떤 상태인지는 **두 소스 어느 쪽도 답하지
  않는다.**
- **제3자 감사가 이 페이지에 없다.** 같은 벤치마크를 다룬 후속 작업으로 `SWE-Bench+`와
  `UTBoost`라는 이름이 이 반입의 각주 자리에 기록돼 있으나, 이 KB는 두 원문을 확보하지
  않았다. **이름 외에는 아무것도 적지 않는다 — 2차 경유이고 수치도 결론도 옮기지
  않는다.** 곧 이 페이지가 가진 감사는 **철회문 하나뿐이고 그것은 벤더 자기 보고**다.
  독립 검증은 이 페이지 밖이다.

## 이어지는 페이지

- [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md) — 같은 병의 반대
  방향. 그쪽은 테스트가 약해 통과가 부푸는 자리를, 이쪽은 테스트가 좁거나 넓어 옳은 답이
  떨어지는 자리를 잰다
- [데이터 오염](../concepts/data-contamination.md) — 이 페이지의 뒤쪽 절반이 실현한
  일반론. 오염 탐지 휴리스틱과 오염 제거가 성립하지 않는 이유가 거기 있다
- [에이전트의 테스트 케이스 착취](../concepts/test-case-exploitation-by-agents.md) —
  이 벤치마크의 Verified 부분집합 위에 세워진 측정. 그쪽 수치를 읽을 때 이 페이지의
  오염 진단이 함께 걸린다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 철회문의
  둘째 교훈(자동 채점은 제대로 만들기 어렵다)이 산업 배포에서 어떤 장치로 나타나는가.
  거기서 채점은 결정적 검사 넷이 맡고, 그 관문이 못 보는 것은 사람 리뷰로 넘어간다
- [공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md) —
  벤치마크가 포화되어 갈린다는 일반론. 이 페이지는 그 갈림의 처음과 끝을 원문으로 가진
  한 사례다
- [파운데이션 모델 평가의 난제](../concepts/evaluating-foundation-models-challenges.md) —
  포화의 계보(GLUE·SuperGLUE·MMLU-Pro)가 놓인 자리
- [LLM 실증 연구의 보고 규범](../concepts/llm-empirical-study-reporting-norms.md) —
  이 페이지가 버전 조건 블록을 다는 근거이자, 벤치마크 쪽으로 같은 요구를 돌린 자리
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  통과가 옳음의 증거가 아니라는 상한. 좁은 테스트는 그 명제의 반대편 실패다 —
  **옳은데도 떨어진다**
- [테스트 오라클](../concepts/test-oracle.md) — fail-to-pass와 pass-to-pass가 각각
  수용 오라클과 보존 오라클 자리에 놓이는 대응
- [기능적 정확성](../concepts/functional-correctness.md) — 실행 기반 채점이 무엇을
  대리하는가
- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 공개 벤치마크를
  믿을 수 없을 때 세우는 것
- [벤치마크와 수용 판정의 무결성](../synthesis/benchmark-and-acceptance-integrity.md) —
  이 갈래의 허브

[^jimenez2024-swebench]: Jimenez, Yang, Wettig, Yao, Pei, Press & Narasimhan 2024,
    "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?", ICLR 2024.
    확보본은 arXiv:2310.06770 **v3**(2024-11-11) 52쪽이고, 전 쪽 쪽머리에
    `Published as a conference paper at ICLR 2024`가 인쇄돼 있다. ICLR 프로시딩은 권·호·
    쪽수로 매기지 않으므로 쪽 표기는 확보본 PDF 쪽 = 논문 안 쪽(1~52)이다. 이 페이지가
    담은 것은 초록, §1~§7, §A.1~§A.5, §C.1·§C.4, 그리고 Table 1·5·7·9·18이다.
    참고문헌(pp.12~15), 개발 세트 부록(§A.6), 저장소별·부분집합별 결과 표(Table 19~24),
    프롬프트 템플릿(§D), 사회적 영향(§E), 생성물 정성 분석 열 사례(§F, pp.34~52)는
    읽었으나 claim으로 옮기지 않았다. 표가 다단 조판이라 기본 텍스트 추출에서 열 순서가
    뒤섞여 `pdftotext -layout` 정렬본과 대조해 옮겼다. Figure 3·4·5·9는 막대·축에 값이
    인쇄돼 있지 않아 옮기지 않았다. **`SWE-bench Verified`는 이 논문 안에 없다** —
    확보본 전문 검색에서 `verified`는 p.2의 `verified by running unit tests` 한 번뿐이고
    데이터셋 이름이 아니다.

[^openai2026-swebench-verified-retire]: OpenAI 2026,
    "Why SWE-bench Verified no longer measures frontier coding capabilities",
    openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/, 게시 2026-02-23.
    **심사를 거치지 않은 벤더 자기 보고(industry report)이고, 여기 실린 수치는 전부
    OpenAI가 스스로 잰 값이다.** 확보본은 라이브 URL이 403이라 Wayback Machine의 `id_`
    모드로 받은 사본이고 캡처 시각은 `20260811105804`(UTC), 이 KB의 열람일은
    2026-08-22다. 쪽 번호가 없는 웹 문서라 위치 표기는 문서가 스스로 붙인 절 이름
    (Background · Too narrow and too wide tests · Contamination · GPT-5.2 ·
    Claude Opus 4.5 · Gemini 3 Flash · Discussion)과 목차 위 요약(도입 문단)이다.
    **요약에만 있는 수치는 옮기지 않았다** — 특히 `74.9% → 80.9%`는 외부 리더보드
    `llm-stats.com`으로 링크된 제3자 집계라 제외했다. 세 오염 사례의 유도 프롬프트·모델
    응답·gold patch 전문은 읽었으나 옮기지 않았고 무엇을 보였는지만 담았다.
    `Introducing SWE-bench Verified`(OpenAI 2024) · `SWE-bench Pro` · `GDPval`은 이 KB가
    원문을 확보하지 않았으므로 이름만 적었다.

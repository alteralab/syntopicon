---
type: concept
status: draft
title: LLM 실증 연구의 보고 규범
description: LLM이 들어간 소프트웨어 공학 실증 연구가 무엇을 반드시 밝혀야 하는가를 22인이 합의로 정한 지침 문서의 요지 — 모델 이름과 판, 실행 날짜, 설정값을 밝히라는 요구, 지표 선택을 정당화하라는 요구, 모델을 가로질러 또 시간을 가로질러 일반화를 확인했는지 밝히라는 요구, 비결정성 때문에 실험을 되풀이하고 분포로 보고하라는 권고, 그리고 이 문서 자체는 심사를 통과한 규범이지 실측이 아니라서 여기 실린 수치는 하나도 인용하지 않는다는 경계
generated: { by: "claude-opus-5", at: "2026-08-22T00:00:00Z" }
sources:
  - { id: baltes2026-llm-guidelines, resource: /it/sources/baltes2026-llm-guidelines.md }
---

# LLM 실증 연구의 보고 규범

- [버전 조건](#버전-조건)
- [이 소스의 지위](#이-소스의-지위)
- [무엇이 재현을 막는가](#무엇이-재현을-막는가)
- [연구 유형 일곱](#연구-유형-일곱)
- [요구와 권고를 가르는 기준](#요구와-권고를-가르는-기준)
- [지침 여덟](#지침-여덟)
- [수치에 유통기한을 박는 자리](#수치에-유통기한을-박는-자리)
- [다시 재라는 요구는 어디에 있는가](#다시-재라는-요구는-어디에-있는가)
- [이 KB의 버전 조건 관행이 기대는 자리](#이-kb의-버전-조건-관행이-기대는-자리)
- [이 소스의 사각](#이-소스의-사각)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **LLM을 쓴 실증 연구는 무엇을 반드시 밝혀야 그 수치를 나중에 다시 읽을 수
있는가.**

## 버전 조건

> **버전 조건**: llm-guidelines.org 판 태그 2026.06 = arXiv 2508.15503 v7(2026-06-12)의
> 문면에 한정한다. 이 지침은 **살아있는 문서**라 저자들이 계속 고치고, 사이트가 개정마다
> `YYYY.MM` 태그를 새로 매긴다. 그래서 아래 요구와 권고의 문면은 그 판의 것이고, 다른
> 판에는 그대로 적용되지 않는다. 판이 바뀌어도 남는 것은 **무엇을 밝히라고 요구하는가의
> 방향**이지 개별 항목의 문면이 아니다.

## 이 소스의 지위

- **근거 등급은 `peer-reviewed`이고, 심사는 실제로 통과했다.** 확보본 1쪽에 `Empirical
  Software Engineering (accepted manuscript)`가 인쇄돼 있고, §3이 저널 심사를 직접
  서술한다 (§3, p.7).[^baltes2026-llm-guidelines] **다만 그 등급이 여는 것은 심사를
  지났다는 사실까지다** — 실측인가 규범인가는 다른 축이고, 이 문서가 그 축의 어디에
  앉는지는 바로 아래 항목이 정한다.

  > During the review process of the *Empirical Software Engineering* journal, the
  > structure and content were improved based on reviewers' suggestions.

- **그러나 실측이 아니라 규범이다.** 이 문서에는 **결과 절이 없다** — 구성은
  서론·범위·방법론·연구 유형·지침 여덟·결론이다. §3이 밝히는 산출 과정은 측정이 아니라
  **전문가 합의**이고, 계보는 임상시험의 CONSORT와 의료의 TRIPOD-LLM이다 (§2 Related
  Reporting Guidelines, p.5; §3, p.6).[^baltes2026-llm-guidelines]

  > Our process followed an established tradition of developing reporting guidelines
  > through expert collaboration, as exemplified by CONSORT for clinical trials and, more
  > recently, TRIPOD-LLM for LLM-based prediction studies in medicine.

- **예시로 든 논문들도 체계적 조사의 결과가 아니라고 저자들이 자인한다** (§3,
  p.7):[^baltes2026-llm-guidelines]

  > The examples are intended to be illustrative, not the result of a systematic review.

- **그래서 이 페이지는 이 소스에서 수치를 한 건도 옮기지 않는다.** 인용 대상은 지침의
  요구(must)와 권고(should) 문면, 그리고 연구 유형 분류뿐이다. 이 논문에 실린 값은 전부
  제3자의 것이고 대괄호 참조번호가 붙어 있다 — 필요하면 그 원전으로 직접 간다. **심사를
  통과했다는 사실이 남의 수치까지 승인하지는 않는다.**

## 무엇이 재현을 막는가

- **결론 절이 문제를 한 문장으로 적는다** (§6, p.60):[^baltes2026-llm-guidelines]

  > LLM non-determinism, opaque training data, and rapidly evolving models threaten the
  > reproducibility and replicability of empirical SE studies.

  비결정성(non-determinism)·불투명한 학습 데이터·빠른 모델 교체 셋이다.
- **서론이 그 셋을 갈라 적는다** (§1, p.3).[^baltes2026-llm-guidelines] 첫째, 같은 입력에도
  실행마다 결과가 달라진다. 둘째, 상용 모델은 판 식별자 너머에서 바뀌므로 **보고된 성능이
  시간이 지나면 달라질 수 있다**. 셋째, "열린" 모델조차 학습 데이터와 미세 조정 세부를
  밝히지 않는 일이 잦다.
- **재현성(reproducibility)과 복제성(replicability)을 이 문서는 구별하지 않고 섞어
  쓴다** — 모델이 바뀌고 연구 산출물이 불완전해서 LLM 연구의 재실행이 두 정의 사이
  어딘가에 놓이기 때문이라고 §5 머리말이 밝힌다 (§5, p.16).[^baltes2026-llm-guidelines]

## 연구 유형 일곱

지침은 전부 "어느 연구 유형에 걸리는가"와 함께 제시된다. 유형은 두 묶음 일곱 개다
(Table 1, §4, p.8).[^baltes2026-llm-guidelines]

| 묶음 | 유형 | 짧은 이름 |
|---|---|---|
| 연구자의 도구로서 | LLMs as Annotators | Annotators |
| 연구자의 도구로서 | LLMs as Judges | Judges |
| 연구자의 도구로서 | LLMs for Synthesis | Synthesis |
| 연구자의 도구로서 | LLMs as Subjects | Subjects |
| 개발자의 도구로서 | Studying LLM Usage in Software Engineering | Usage |
| 개발자의 도구로서 | LLMs for New Software Engineering Tools | Tools |
| 개발자의 도구로서 | Benchmarking LLMs for Software Engineering Tasks | Benchmarking |

## 요구와 권고를 가르는 기준

- **두 층의 정의** (§5, p.17):[^baltes2026-llm-guidelines]

  > A **must** criterion is a *requirement*. Studies that intend to follow these guidelines
  > are expected to meet all **must** criteria. A **should** criterion represents a desired
  > practice that strengthens a study's rigor or transparency.

- **가르는 축이 심각성만은 아니다** (§5, p.17):[^baltes2026-llm-guidelines]

  > A **must** criterion is typically a disclosure obligation such as reporting model
  > versions, publishing prompts, describing architectures, and discussing limitations, so
  > that readers can independently evaluate the choices authors made. A **should** criterion
  > is typically a methodological recommendation such as which baselines to include and
  > which validation strategies or statistical analyses to apply.

  **곧 "밝혀라"는 요구이고 "이렇게 하라"는 권고다.** 이 구획이 이 페이지가 이 문서를
  유통기한 규율의 근거로 쓰는 이유다 — 수치의 조건을 밝히는 일은 방법론 취향이 아니라
  요구 층에 있다.
- 권고에서 벗어날 수는 있으나 값이 있다 — 타당성이나 재현성을 해칠 수 있는 이탈은
  **짧게라도 정당화하라**고 같은 자리가 적는다 (§5, p.17).[^baltes2026-llm-guidelines]

## 지침 여덟

Table 2의 이름과 각 절 머리말(Summary)의 문면을 요지로 옮긴다 (Table 2, p.18; §5.1~§5.8,
pp.18–59).[^baltes2026-llm-guidelines] **요구(must)와 권고(should) 표기는 원문의 것이다.**

| 절 | 이름 | 요구(must)의 요지 | 권고(should)의 요지 |
|---|---|---|---|
| 5.1 | Declare LLM Usage and Role | LLM을 썼다는 사실과 **어느 모델을 · 어떻게 · 연구 과정 어디에서** 썼는지 밝힌다 | 목적과 자동화한 과제와 기대 이득을 논문에 적고, LLM이 중심이면 방법 절에 자세히 둔다 |
| 5.2 | Report Model Version, Configuration, and Customizations | **모델 또는 도구의 정확한 판, 설정, 연구 실행 날짜**를 논문에 적는다. 미세 조정을 했으면 목표·데이터셋·절차를 적는다 | 기본값도 포함해 모든 설정값, 체크섬과 지문, 양자화 수준과 방법, 모델 선택 이유를 적는다 |
| 5.3 | Report System and Prompt Design | 도구의 전체 구조를 논문에 적고, **모든 프롬프트를 보충 자료로 공개**하며 대표 예를 논문에 싣는다. 어떤 설정 기제(컨텍스트 파일·스킬·서브에이전트)를 썼는지 적는다 | 프롬프트 개발 경위를 적고, 가능하면 구현을 오픈소스로 낸다 |
| 5.4 | Report Session Traces | 도구 고유 트레이스 형식을 썼으면 파일 형식과 도구 판을 적는다. 민감 정보가 든 트레이스는 익명화한다 | 상호작용 로그(interaction log)와 런타임 트레이스(runtime trace)를 보충 자료로 낸다. 문서화된 스키마가 있는 열린 형식을 쓴다 |
| 5.5 | Use Suitable Baselines, Benchmarks, and Metrics | **벤치마크와 지표 선택을 논문에서 정당화**하고 신뢰도와 타당도, 특히 구인 타당도(construct validity)를 논한다. 벤치마크를 새로 내면 자료 출처와 수집 날짜를 판마다 밝힌다 | 측정하려는 현상을 조작적으로 정의하고, 표본 추출 전략을 정당화하며, 오류 분석을 하고, 실험을 되풀이해 분포를 기술 통계로 보고한다 |
| 5.6 | Use an Open LLM as a Baseline | (요구 없음 — 이 지침은 권고 층이다) | 상용 모델을 쓸 때 개방 모델(open LLM)을 기준선으로 함께 넣고 모델 사이 일치도를 보고한다. 그 기준선이 보충 자료만으로 독립 재현되게 한다 |
| 5.7 | Use Human Validation for LLM Outputs | 인간 검증(human validation)을 한다면 **측정하는 구인을 정의하고 측정 도구를 기술**한다. 도구를 만들거나 고쳤으면 공개한다. LLM이 사람을 **대체**하면 그 대체가 정당한지 설명한다 | 설계 초기에 인간 검증을 넣고, 확립된 비교 참조 모형에 기댄다. 판정자 사이·판정자와 사람 사이 일치도로 대체를 뒷받침한다 |
| 5.8 | Report Limitations and Mitigations | 한계를 투명하게 적는다. **모델을 가로질러 또는 시간을 가로질러 일반화를 평가했는지 밝히고 모델과 판의 차이를 논한다.** 데이터 누출 영향을 논한다 | 복제 패키지·인간 검증·종단 재실행·삼각 측량·민감도 분석 같은 완화책을 쓰고 보고한다 |

- **여섯째 지침만 권고 층이다.** §5.6의 요약과 권고와 연구 유형 절이 전부 `should`로만
  적혀 있고 자기 요구가 없다 (§5.6, pp.44–47).[^baltes2026-llm-guidelines] 적용 행렬에서도
  `Open LLM` 행에만 "적용되지 않음" 칸이 있다 (Appendix A Table 3,
  p.61).[^baltes2026-llm-guidelines]
- **부록 C가 같은 항목을 논문 절 순서로 다시 늘어놓는다** — CONSORT의 구조 틀을 따른
  보고 점검표이고, 항목마다 요구인지 권고인지와 어느 지침에서 왔는지를 붙인다
  (Appendix C, pp.63–67).[^baltes2026-llm-guidelines]

## 수치에 유통기한을 박는 자리

호출자가 부르는 것이 이 절이다. **"이 수치가 언제 어느 모델의 것인가"를 밝히는 의무는
5.2에 요구 층으로 박혀 있다.**

- **최소 요구가 열거로 적혀 있다** (§5.2.2, p.22):[^baltes2026-llm-guidelines]

  > In summary, researchers must report in the *paper* at minimum (1) the exact model or
  > tool name and version, (2) all parameters they configured that affect output generation,
  > (3) the date of study execution, and, for fine-tuned models, (4) the fine-tuning goal,
  > dataset characterization, approach (e.g., full fine-tuning vs. LoRA), and hyperparameters.

  **모델 이름과 판, 설정, 그리고 실행 날짜** 셋이 요구다.
- **기본값도 적으라는 근거가 시간이다** (§5.2.2, p.21):[^baltes2026-llm-guidelines]

  > Since default values might change over time, researchers **should** report all
  > configuration values, even if they used the defaults.

- **측정 단위 쪽은 "지표를 정당화하라"로 온다** (§5.5.2, p.38):[^baltes2026-llm-guidelines]

  > As mentioned, researchers must motivate why they chose a certain metric or variant
  > thereof for their particular study. Prior adoption alone does not constitute sufficient
  > justification; researchers **must not** justify metric choices solely by citing their
  > use in prior work.

  **곧 "남들이 쓰니까"는 정당화가 아니다.** 다만 이것은 지표 선택의 정당화 의무이지
  단위·분모를 적으라는 조문은 아니다 — 그쪽에 가장 가까운 것은 벤치마크의 구조와 과제를
  요약하라는 **권고**이고, 거기에 프로그래밍 언어와 과제 수·테스트 케이스 수 같은 기술
  통계가 포함된다 (§5.5.2, p.37).[^baltes2026-llm-guidelines]
- **언어 의존은 요구가 아니라 권고 층에 있다.** 벤치마크 요약 권고에 프로그래밍 언어가
  들어가고, §5.5.5가 널리 쓰이는 벤치마크들이 파이썬이라 다른 언어로 넘어가지 않는
  이득을 만든다고 적는다 (§5.5.5, p.42).[^baltes2026-llm-guidelines]

## 다시 재라는 요구는 어디에 있는가

**"주기적으로 다시 재라"는 조문은 없다.** 대신 세 자리가 그 일을 나눠 진다.

- **요구 하나** — 시간을 가로지르는 일반화를 평가했는지 밝히라는 것이다 (§5.8 Summary,
  p.53):[^baltes2026-llm-guidelines]

  > The *paper* must specify whether generalization across LLMs or across time was
  > assessed, and discuss model and version differences.

  **평가하라는 요구가 아니라 평가했는지 밝히라는 요구다.** 이 구별을 지우면 이 문서가
  말하지 않은 것을 말하게 된다.
- **권고 둘** — 비결정성 때문에 실험을 되풀이하고 결과의 분포를 기술 통계로 보고하라는
  것, 그리고 되풀이 횟수를 검정력 분석이나 기술 통계의 수렴 관찰로 정당화하라는 것이다
  (§5.5 Summary, p.36; §5.5.2, pp.38–39).[^baltes2026-llm-guidelines]
- **완화책으로서의 재실행** — 시간에 걸친 불안정을 잡는 방법으로 **종단 재실행
  (longitudinal re-runs)**이 외적 타당도와 신뢰성 두 자리에 모두 적혀 있고, 삼각 측량과
  민감도 분석과 나란히 놓인다 (§5.8.2 External Validity·Reliability & Reproducibility,
  pp.55–57).[^baltes2026-llm-guidelines]
- **드리프트를 감지할 재료도 지정된다** — 저장해 둔 세션 트레이스(session trace)가 나중에
  모델 거동 변화를 감시할 기준선이 된다고 §5.8의 상호 참조가 적는다 (§5.8.8,
  p.57).[^baltes2026-llm-guidelines]

## 이 KB의 버전 조건 관행이 기대는 자리

이 KB의 LLM 실측 페이지들은 이미 **모델과 시점을 페이지에 박는 관행**을 갖고 있다. 이
페이지가 그 관행의 규범 근거다 — 관행이 먼저 있었고 근거가 뒤에 왔다.

- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md)는
  버전 조건 블록에 모델·연도·언어·빌드 도구를 적고, 별도 절에서 그 수치들의 유통기한을
  따로 다룬다. 5.2가 요구하는 **모델 판과 실행 시점**, 5.5가 권고하는 **언어를 포함한
  벤치마크 구조 요약**이 그 자리에 대응한다.
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md)은 모델 집합과
  모델 시점과 과제를 표로 갈라 두고, 낡는 값과 낡지 않는 방향을 나눈다. 5.8이 요구하는
  **모델을 가로지르는 일반화와 시간을 가로지르는 일반화의 구분**이 그 표의 축이다.
- **두 관행이 이 문서에서 얻는 것은 이름과 층이다.** 어느 것이 밝힐 의무이고 어느 것이
  방법론 권고인지가 갈리면, KB가 어디까지를 반드시 적어야 하는지가 정해진다.

## 이 소스의 사각

- **자기 측정값이 없다.** 이 문서는 지침이 실제로 재현성을 올리는지 재지 않는다. 결론이
  적는 것도 기대다 (§6, p.60):[^baltes2026-llm-guidelines]

  > Adopting these practices will not eliminate LLM non-determinism, but it would make
  > claims auditable and results easier to replicate and compare across studies.

- **§5.7의 일치도 문턱값은 이 논문의 것이 아니다** — Krippendorff의 기준을 인용한
  것이므로, 그 문턱을 쓰려면 그 원전으로 간다. 이 페이지는 문턱값을 옮기지 않는다.
- **대상 분야가 소프트웨어 공학 연구다.** §2가 범위를 텍스트 기반 용례로 한정하고,
  교정·번역 같은 주변 용도는 명시적으로 제외한다 (§2 Scope,
  p.4).[^baltes2026-llm-guidelines] 다중 모드 설정에도 아마 적용될 것이라고 적지만
  체계적 확인은 후속 과제로 미룬다.
- **연구자를 위한 규범이지 제품 개발을 위한 규범이 아니다.** 독자를 SE 연구자로 못
  박고, 각 지침이 심사자를 위한 조언 절을 따로 둔다 (§2 Researchers as our Target
  Audience, p.4).[^baltes2026-llm-guidelines]
- **살아있는 문서라 문면이 움직인다.** 위 버전 조건 절이 그 대응이다.

## 이어지는 페이지

- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  모델·시점·언어에 묶인 값을 실제로 그렇게 적어 둔 실측 페이지
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md) — 모델 집합과
  시점을 유통기한으로 갈라 둔 실측 페이지
- [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md) — 5.2가 요구하는
  모델 판과 실행 시점을 버전 조건 블록으로 실제로 적어 둔 자리. 그 페이지가 자기 수치를
  조항에 박지 않는 근거로 이 페이지를 든다
- [에이전트의 테스트 케이스 착취](../concepts/test-case-exploitation-by-agents.md) —
  값 하나마다 데이터셋과 모델과 스캐폴드와 프롬프트를 붙여 적는 규칙. 5.2의 밝힐 의무와
  5.5의 지표 정당화 요구를 한 페이지 안에서 실행한 모습이다
- [벤치마크의 수명과 철회](../concepts/benchmark-lifespan-and-retirement.md) — 같은 요구를
  모델이 아니라 벤치마크 쪽으로 돌린 자리. 어느 판인지와 어느 시점인지에 더해 그 뒤에
  감사나 철회 고지가 있었는지를 묻는다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 5.2의
  요구가 지켜지지 않은 실물. 산업 배포 논문 하나가 쓴 모델의 정체를 상업 기밀이라며
  밝히지 않는다
- [데이터 오염](../concepts/data-contamination.md) — 5.5와 5.8이 내적 타당도 위협으로
  드는 것. 그쪽은 기제를, 이쪽은 무엇을 밝히라는 의무를 다룬다
- [공개 벤치마크와 리더보드](../concepts/public-benchmarks-and-leaderboards.md) —
  벤치마크가 무엇을 보장하고 무엇을 보장하지 않는가
- [벤치마크와 수용 판정의 무결성](../synthesis/benchmark-and-acceptance-integrity.md) —
  이 갈래의 허브
- [AI 판정자의 한계](../concepts/ai-judge-limitations.md) — 5.7이 인간 검증을 요구하는
  이유가 놓인 자리
- [평가 파이프라인 설계](../concepts/evaluation-pipeline-design.md) — 지표와 기준선을
  고르는 실무 쪽

[^baltes2026-llm-guidelines]: Baltes 외 21인 2026, "Guidelines for Empirical Studies in
    Software Engineering involving Large Language Models", *Empirical Software Engineering*
    (accepted manuscript). 확보본은 arXiv:2508.15503 **v7**(2026-06-12)이고 86쪽이며,
    llm-guidelines.org 판 태그는 **2026.06**이다. 쪽 표기는 확보본 PDF의 인쇄 쪽이다.
    **이 페이지는 이 소스에서 수치를 한 건도 옮기지 않았다** — 이 문서에는 결과 절이
    없고 실린 값은 전부 제3자의 것이라 2차 경유가 된다. 인용한 것은 §1·§2·§3의 지위와
    산출 과정 서술, §4 Table 1의 유형 분류, §5 머리말의 요구·권고 정의, §5.1~§5.8의
    Summary와 Recommendations 문면, Appendix A Table 3의 적용 표시, Appendix C의 점검표
    구성, §6의 결론 문장뿐이다. §4.3(이점과 난제)·§5 각 절의 Examples·Benefits·Challenges·
    Advice for Reviewers와 참고문헌은 이 페이지의 물음 밖이라 옮기지 않았다. 확보본의
    이탤릭이 텍스트 추출에서 별표로 남아 낱말이 붙는 자리가 있어, 직인용은 원문 조판대로
    띄어 적었다.

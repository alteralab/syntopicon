---
type: concept
title: 뮤테이션 테스팅은 최종 심급이 아니다
description: 뮤테이션 테스팅의 원전과 산업 최대 규모 운영 기록을 한 자리에 놓은 페이지 — 결합 효과의 정의와 원전 스스로 붙인 "증명할 길이 없다"는 단서, 죽은·살아 있는·동등 뮤턴트라는 어휘의 출처, competent programmer hypothesis라는 명명이 원전에 없다는 실측, 규모가 전통적 방식을 무너뜨리는 자리, Google이 절대 뮤테이션 점수를 버리고 코드 리뷰 시점의 개별 제안으로 갈아탄 기록과 그 수치, 절대 점수 임계와 프로젝트 간 비교를 금지하는 이 KB의 판정, 그리고 그 세 금지가 심사 실증 여섯 편의 어느 수치로 서는지의 대응, 그리고 그 리뷰 시점 배선이 같은 회사의 정적 분석 플랫폼이며 그 플랫폼의 관문과 되먹임 회로가 이 뮤테이션 서비스의 억제 규칙 축적과 같은 기제라는 대질
generated: { by: "claude-opus-5", at: "2026-08-23T07:30:00Z" }
sources:
  - { id: demillo1978-hints, resource: /it/sources/demillo1978-hints.md }
  - { id: petrovic2021-google-mutation, resource: /it/sources/petrovic2021-google-mutation.md }
  - { id: zhao2026-llm-coverage-replication, resource: /it/sources/zhao2026-llm-coverage-replication.md }
  - { id: wang2025-mutgen, resource: /it/sources/wang2025-mutgen.md }
  - { id: winters2020-swe-at-google, resource: /it/sources/winters2020-swe-at-google.md }
---

# 뮤테이션 테스팅은 최종 심급이 아니다

- [이 두 소스의 지위](#이-두-소스의-지위)
- [결합 효과 — 원전이 세운 가정](#결합-효과--원전이-세운-가정)
- [뮤테이션의 어휘가 여기서 나온다](#뮤테이션의-어휘가-여기서-나온다)
- [원전이 실제로 잰 것](#원전이-실제로-잰-것)
- [competent programmer hypothesis라는 명명은 원전에 없다](#competent-programmer-hypothesis라는-명명은-원전에-없다)
- [규모가 전통적 방식을 무너뜨린다](#규모가-전통적-방식을-무너뜨린다)
- [Google은 절대 점수를 버렸다](#google은-절대-점수를-버렸다)
- [그 리뷰 시점 배선의 정체 — 같은 회사의 정적 분석 플랫폼](#그-리뷰-시점-배선의-정체--같은-회사의-정적-분석-플랫폼)
- [변경분 한정과 arid 억제 — 실제로 무엇을 하는가](#변경분-한정과-arid-억제--실제로-무엇을-하는가)
- [억제와 선택이 낸 수치](#억제와-선택이-낸-수치)
- [이 KB의 판정 — 게이트로 쓸 때의 세 금지](#이-kb의-판정--게이트로-쓸-때의-세-금지)
- [시대 지위 — 언어 모델이 만든 스위트에서](#시대-지위--언어-모델이-만든-스위트에서)
- [이 두 소스가 넘지 않은 선](#이-두-소스가-넘지-않은-선)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **뮤테이션 테스팅(mutation testing)은 스위트가 적절한지를 판정하는 최종
심급인가 — 그 기법을 낸 원전과 그것을 가장 큰 규모로 운영한 산업 사례가 무엇이라고
답하는가.**

조건: 원전은 1978년의 Fortran이고, 산업 사례는 단일 저장소를 쓰는 한 회사의 코드
리뷰 배선이다.

## 이 두 소스의 지위

- **두 소스 모두 근거 등급은 `peer-reviewed`다.** 하나는 IEEE *Computer* 1978년 4월
  호에 실린 글이고,[^demillo1978-hints] 다른 하나는 IEEE Transactions on Software
  Engineering의 수용판이다.[^petrovic2021-google-mutation]
- **1978년 글은 성격이 `classic`이라 전이 조건이 붙는다.** 대상 언어는 Fortran이고,
  뮤테이션 시스템은 예일대와 조지아 공대가 만든 대화형 도구이며, 예제는 세 줄에서
  수십 줄짜리 서브루틴이다. **이 조건에서 나온 관찰이 지금 규모의 코드베이스에서도
  참인지는 이 글이 답하지 않는다.**
- **Google 논문의 게재처는 IEEE TSE다.** 확보본 각 쪽 상단 띠가
  `This article has been accepted for publication in a future issue of this journal`과
  `DOI 10.1109/TSE.2021.3107634`를 인쇄하고, 1쪽 각주가
  `Manuscript received June 13, 2020; revised February 7, 2021.`이다. **같은 저자군의
  ICSE 논문 둘은 이 논문 안에 참고문헌으로 따로 실려 있다** — [12]
  `State of Mutation Testing at Google`(ICSE 2017 SEIP)와 [20]
  `Does mutation testing improve testing practices?`(ICSE 2021).
  **셋은 별개 논문이다.**[^petrovic2021-google-mutation]
- **규모 전제의 수치는 이 페이지가 옮기지 않는다.** 코드베이스 줄 수·하루 테스트 실행
  수·하루 변경 제출 수는 §1 도입부가 인프라를 서술하며 드는 값이고 이 논문이 잰 결과가
  아니다. 배포 규모(개발자 수·프로젝트 수)도 초록의 서술이다. **이 페이지가 쓰는
  수치는 §5의 데이터셋 총계와 결과 표뿐이다.**
- **1978년 글의 Table 1과 Figure 1도 옮기지 않는다.** 각각 박사 논문과 System
  Development Corporation 보고서에서 경유해 온 제3자 값이다.

## 결합 효과 — 원전이 세운 가정

**뮤테이션이 스위트 적절성의 눈금이 될 수 있다는 주장은 전부 이 가정 하나에
기댄다.**

- **결합 효과(coupling effect)의 정의가 이 글에 있다** (p.35).[^demillo1978-hints]

  > The coupling effect: Test data that distinguishes all programs differing from a
  > correct one by only simple errors is so sensitive that it also implicitly
  > distinguishes more complex errors.

  단순한 오류만큼만 다른 프로그램들을 전부 갈라내는 테스트 데이터는 **그만큼
  민감해서** 더 복잡한 오류도 암묵적으로 갈라낸다는 것이다.
- **저자들이 바로 다음 문장에서 그 지위를 스스로 낮춘다** (p.35).[^demillo1978-hints]

  > There is, of course, no hope of "proving" the coupling effect; it is an empirical
  > principle.

  **"증명할 길은 물론 없다. 이것은 경험적 원리다"** — 원전이 자기 가정에 붙인
  눈금이 이것이다.
- **가정이 서 있는 그림도 명시돼 있다** (p.34).[^demillo1978-hints] 프로그래머는
  무작위로 프로그램을 만들지 않고, 설계 과정을 여러 번 되풀이하며 지금 모습과
  의도한 모습 사이의 거리를 깎아 나간다는 것이다.

  > Programmers do not create programs at random; competent programmers, in their many
  > iterations through the design process, are constantly whittling away the distance
  > between what their programs look like now and what they are intended to look like.

- **이 가정이 실제 결함에 대해 검증됐다는 근거를 이 KB는 확보하지 않았다.** 결합 효과의
  대표 실증으로 불리는 Offutt의 1992년 연구는 **대상이 Fortran 프로그램 셋·총 72줄**이고
  저자 본인이 결론에서 고차 뮤턴트(higher-order mutant)를 죽이는 것이 복합 결함 검출을
  뜻하는지는 아직 정해지지 않았다고 적는다. **이 서술은 원문 미확보 상태의 2차 경유이므로
  직인용하지 않고 사실만 적는다.**
- **결합 효과의 타당성을 정면으로 잰 실증은 이 두 소스 밖에 있다.**
  [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md)이
  그 묶음이고, 결합 효과가 실제 결함에서 얼마나 성립하는지를 뮤턴트 하나하나와 결함
  하나하나의 대응으로 잰 심사 실증이 거기 있다.

## 뮤테이션의 어휘가 여기서 나온다

- **절차의 정의** (p.36).[^demillo1978-hints] 프로그래머가 프로그램 P와 적절성을 재고
  싶은 테스트 데이터를 넣으면, 시스템이 먼저 P를 그 데이터로 돌린다. 답이 틀리면
  P가 틀린 것이다. 답이 맞으면 시스템이 **단순한 오류 하나만큼만 P와 다른** 변형들
  P₁, P₂, …, Pₖ를 만든다. 이 변형 하나하나를 **뮤턴트(mutant)**라 부른다.
- **죽은 뮤턴트와 살아 있는 뮤턴트** (p.36).[^demillo1978-hints] 그 데이터에서 P와
  다른 답을 내면 Pᵢ는 **죽었다(dead)**고 하고, 같은 답을 내면 **살아 있다(live)**고
  한다. 살아 있는 이유는 둘 중 하나다 — 데이터가 그 오류를 가를 만큼 민감하지 않거나,
  Pᵢ와 P가 **실제로 동등한 프로그램(equivalent programs)**이라 어떤 데이터로도 가를 수
  없거나.
- **적절성(adequate)의 정의도 여기 있다** (p.36).[^demillo1978-hints] 살아 있는
  뮤턴트가 없거나 남은 것이 전부 P와 동등하면 그 테스트 데이터는 적절하다. 그 뜻은
  **"P가 옳거나, 아니면 P에 예상 밖의 오류가 있는데 결합 효과에 비추어 그런 일은 드물
  것으로 기대된다"**이다.
- **이 정의가 곧 이 페이지의 물음이다.** 적절성 판정이 "드물 것으로 기대된다"에
  기대고 있고, 그 기대의 근거가 위의 경험적 원리다.
- **도구의 목적을 저자들이 대화로 그린다** (p.36).[^demillo1978-hints] 시스템의
  부정적 응답은 프로그램에 대한 **"어려운 질문"**이다 — "네가 준 테스트 데이터로는
  이 검사가 같음인지 다름인지가 상관없다고 나온다. 왜 그런가?" 그리고 프로그래머는
  그 답을 더 민감한 데이터를 만드는 길잡이로 쓴다. **처음부터 점수가 아니라 질문이
  산출물이다.**

## 원전이 실제로 잰 것

- **FIND 예제가 이 글의 주 실험이다** (pp.39–40).[^demillo1978-hints] Hoare의 FIND를
  Fortran으로 옮긴 것이 대상이다.
  - 동료들이 거의 만장일치로 고른 방법인 **순열 24개**(0,1,2,3의 전체 순열, F 고정)로는
    **살아 있는 뮤턴트가 58개** 남는다 (Table 6, p.40 — F=3 행).
  - A 벡터를 **49개**로 늘리면 살아 있는 뮤턴트가 **10개**로 준다.
  - 데이터 축약 휴리스틱으로 그 49개를 **A 벡터 7개**로 줄이면 살아 있는 뮤턴트가
    **14개**가 되고, 저자들은 그 14개가 전부 FIND와 동등함을 보여 이 7개를 적절한
    데이터로 삼는다 (Table 5, p.39).
  - **분모가 인쇄돼 있지 않다.** 총 뮤턴트 수를 이 글이 어디에도 적지 않으므로 위
    숫자는 전부 **살아 있는 뮤턴트의 절대 개수**로만 읽어야 한다.
  - #hypothesis 같은 쪽이 "가장 좋은 A 벡터 하나가 703개를 죽인다"고 적고 남은 14개를
    "대략 2 퍼센트"라고 부르므로 총 뮤턴트는 700개 안팎으로 보인다. **이 산수는 이 KB가
    붙인 것이고 원문이 적은 것이 아니다.**
- **결합 효과의 증거로 저자들이 내놓는 것은 둘이다** (p.40).[^demillo1978-hints]
  하나는 SELECT 시스템이 찾아낸 다중 오류 뮤턴트 BUGGYFIND가 위 적절한 데이터에서
  실패한다는 **한 점 사례**다. 다른 하나가 더 설득력 있다고 저자들이 적는 것인데 —
  **2만 2천 개가 넘는 고차 오류(higher-order error) 중 19개만 그 데이터에서 살아남았고,
  그 19개는 FIND와 동등함이 밝혀졌다.**
  - **대상은 여전히 FIND 하나다.** 프로그램 하나에서 나온 관찰이다.
- **동등 뮤턴트 비율에 대한 저자들의 추정** (p.39).[^demillo1978-hints] FIND의
  동등률이 높은 것은 이 프로그램이 1961년부터 오래 다듬어진 탓이라고 보고,
  **`We estimate that production programs have well under 1 percent equivalent
  mutants.`**라고 적는다. **이것은 추정이지 측정이 아니다** — 근거로 든 자료가 없다.

## competent programmer hypothesis라는 명명은 원전에 없다

- **`hypothesis`라는 낱말이 이 글에 한 번도 없다.** 확보본 전문 추출본에
  `grep -i hypothesis`를 걸면 **0건**이고, 어형이 가장 가까운 것은 결론부에서 테스트
  데이터 선택에 관한 가설 형성(`hypotheses`)을 말하는 한 번뿐이다.
- **있는 것은 서술문이다.** 위 [결합 효과](#결합-효과--원전이-세운-가정) 절에 옮긴
  p.34의 `competent programmers …` 문장이 전부다.
- **그래서 이 페이지는 "유능한 프로그래머 가설"이라는 이름을 원전에 귀속하지 않는다.**
  그 이름을 붙인 것은 뒤 문헌이고, 이 KB는 그 명명의 출처를 확보하지 않았다.

## 규모가 전통적 방식을 무너뜨린다

- **Google이 처음 시도한 것은 전통적 방식이었고 두 벽에 부딪혔다**
  (§1·§2).[^petrovic2021-google-mutation] 하나는 계산 비용이고, 다른 하나가 이
  페이지에서 더 중요하다 — **결과를 개발자에게 전할 방법이 없었다.**
- **저자들이 그 두 번째 벽을 이렇게 적는다** (§2):[^petrovic2021-google-mutation]

  > In addition to the costs of computing that ratio, we were unable to find a good way
  > to report it to the developers in an actionable way: it is neither concrete nor
  > actionable, and it does not guide testing.

  여기서 `that ratio`는 뮤턴트 검출 비율(mutant-detection ratio), 곧 **전통적 뮤테이션
  점수(mutation score)**다.
- **표본 추출로 수를 줄여도 문제가 남았다** (§1).[^petrovic2021-google-mutation]
  개발자들이 보고된 뮤턴트를 대량으로 **비생산적(unproductive)**이라고 분류했다.
  비생산적 뮤턴트란 원본과 자명하게 동등하거나, 죽일 수는 있지만 그것을 죽이는 테스트를
  더해도 스위트가 나아지지 않는 뮤턴트다.
  - 저자들이 드는 예가 자바 컬렉션의 초기 용량을 바꾸는 뮤턴트다. 그것을 잡는 테스트를
    **쓸 수는 있지만 쓰는 것이 비생산적**이고, 그런 테스트는 명세가 아니라 현재 구현을
    검사하는 **변경 탐지기(change-detector)** 성질을 가져 깨지기 쉬운 테스트와 거짓
    경보를 낳는다고 적는다.

## Google은 절대 점수를 버렸다

**이 절이 `verdict: caveat`의 핵심이다. 이 논문은 뮤테이션 게이트의 근거가 아니라
게이트를 버린 기록으로 읽어야 한다.**

- **저자들이 뮤테이션 점수 자체를 지표에서 내렸다.** 위 §2 인용이 그 자리다 — 구체적
  이지도 실행 가능하지도 않고 테스팅을 이끌지 못한다는 것이 이유이고, 비용은 그와
  **별도로** 적혀 있다.
- **대신 개별 뮤턴트를 코드 리뷰의 소견(finding)으로 띄운다**
  (§2.4).[^petrovic2021-google-mutation] 개발자가 변경을 리뷰에 올리면 여러 분석기가
  자동으로 돌고, 그 산출인 소견이 리뷰 화면에 붙는다.
- **그 소견은 관문이 아니다** (§2.4):[^petrovic2021-google-mutation]

  > Unlike human-generated comments, findings do not need to be resolved by the author
  > before submission, unless a human reviewer marks them as mandatory.

  **사람 리뷰어가 필수로 표시하지 않는 한 저자가 해소하지 않고 제출할 수 있다.**
  차단하는 것은 도구가 아니라 사람이다.
- **개발자는 한 번의 클릭으로 소견을 되받을 수 있다** (§2.4).[^petrovic2021-google-mutation]
  화면에 `Please Fix`와 `Not useful` 두 링크가 있고, 그 피드백이 시스템 소유자에게
  돌아가 품질 지표가 된다. **피드백 방향이 도구에서 사람으로만이 아니라 사람에서
  도구로도 흐른다.**
- **저자들이 자기 생존율이 뮤테이션 점수가 아님을 명시한다**
  (§5.3):[^petrovic2021-google-mutation]

  > Note that this is not the same as the traditional mutation score [30] (ratio of killed
  > mutants to the total number of mutants) because mutagenesis is probabilistic and
  > only generates a subset of all mutants.

  **이 논문이 내는 어떤 비율도 뮤테이션 점수로 읽어서는 안 된다**고 논문이 스스로
  적는 자리다. 인용 안의 `[30]`은 원문의 참고문헌 번호이고 가리키는 것은
  1978년 원전이다.

## 그 리뷰 시점 배선의 정체 — 같은 회사의 정적 분석 플랫폼

**2021년 논문이 §2.4에서 서술하는 배선은 이 KB가 따로 들인 2020년 자기 보고의 20장이
다루는 플랫폼과 같은 것이다.** 논문은 그 플랫폼을 이름으로만 지나가고 그 장이 그것을
한 장에 걸쳐 적는다. **두 문헌을 맞대면 이 뮤테이션 서비스가 무엇 위에 얹혀 있었는지가
드러난다.**

- **소견이 리뷰 화면에 뜨고 차단하지 않는다는 것이 그 플랫폼의 기본 배치다.** 그 장이
  정적 분석의 주된 삽입 지점을 코드 리뷰로 고른 근거 여섯을 적고, **개발자가 리뷰의 경고를
  무시할 수 있다는 것을 스스로 인정한 뒤** 막는 층(제출 전 검사·컴파일러)을 따로 둔다
  (20장 §"Make Static Analysis a Part of the Core Developer Workflow" ·
  §"Presubmits").[^winters2020-swe-at-google] **뮤테이션 소견은 그 막는 층에 올라가지
  않았다** — 위 [Google은 절대 점수를 버렸다](#google은-절대-점수를-버렸다)의 인용이 그
  자리다.
- **되받기와 고쳐 달라는 두 조작이 그 플랫폼의 되먹임 회로다.** 그 장이 **쓸모없음 표시가
  분석기 작성자를 대상으로 결함 신고를 곧장 열고**, **리뷰어의 수정 요청이 그것과 맞대어
  추적되며**, **비율이 나쁜 분석기를 개선하지 않으면 끈다**고 적는다 (20장 §"Integrated
  Feedback Channels").[^winters2020-swe-at-google] **그러므로 이 논문의 되먹임 링크 둘은
  이 서비스가 만든 장치가 아니라 플랫폼이 모든 분석기에 거는 계량기**다.
- **그 플랫폼에 검사를 들이는 관문이 넷이고 그 셋째가 이 논문의 생산성 지표와 같은
  잣대다** (20장 §"Tricorder: Google's Static Analysis
  Platform").[^winters2020-swe-at-google] 관문은 **체감 오탐이 10% 미만일 것** — 곧
  **개발자가 열 번 중 아홉 번은 진짜 문제를 짚었다고 느낄 것** — 을 요구하고, 그 장은
  체감 오탐을 **개발자가 그 지적을 보고 어떤 긍정적 행동도 하지 않은 경우**로 규정한다.
  - **이 논문의 82%(피드백이 붙은 보고 뮤턴트 가운데 생산적이라 라벨된 비율)가 그
    잣대의 뒤집힌 판본**이다. 두 값의 방향이 반대이고 분모가 다르다 — 관문 쪽은 전체
    지적을 분모로 상정하고 이 논문 쪽은 **피드백이 붙은 것만**을 분모로 쓴다(위
    [억제와 선택이 낸 수치](#억제와-선택이-낸-수치)). **그러므로 82%를 그 관문의 10%
    문턱과 직접 견주어서는 안 된다.**
  - **다만 방향은 읽을 수 있다.** 이 논문이 적는 개선 경로 — 억제 규칙으로 생산적 비율을
    약 15%에서 80%로, 다시 89%로 올린 것 — 이 **그 플랫폼의 관문을 통과할 수 있는 상태로
    가는 과정**으로 읽힌다. **이 논문이 그 관문을 근거로 대지는 않는다.** `#hypothesis`
- **억제 규칙을 쌓는 방식이 그 플랫폼의 운영 규칙과 같은 모양이다.** 이 논문은
  **쓸모없음 피드백을 보고 한 부류 전체를 막을 만하면 arid 규칙을 하나 더한다**고 적고
  (§3.1), 그 장은 **되먹임 통로가 없던 시절에는 개발자들이 이해하지 못한 분석 결과를 그냥
  무시했다**고 적는다 (20장 §"Integrated Feedback Channels").[^winters2020-swe-at-google]
  **같은 회로의 두 서술**이고, 한쪽은 한 분석기 안에서 도는 모습을, 다른 쪽은 플랫폼
  전체에서 도는 모습을 적는다.
- **보고 수의 상한도 그 장의 조문과 같은 방향이다.** 이 논문은 변경 목록의 파일 수의
  7배 이하로 보고를 묶고(§2.3), 그 장은 **개발자 시간을 저울의 비용 쪽에 명시적으로
  올리고 대응 비용을 낮추는 것을 오탐률을 낮추는 것과 같은 층의 개선으로 다룬다**
  (20장 §"Usability").[^winters2020-swe-at-google]
- **이 KB의 판정 — 이 대질이 이 논문의 전이 조건을 하나 더 드러낸다.** 위
  [이 두 소스가 넘지 않은 선](#이-두-소스가-넘지-않은-선)이 arid 규칙의 이전 불가능성을
  적는데, **그보다 앞서 이 서비스는 리뷰 시점에 소견을 띄우고 되먹임을 받아 분석기를
  끌 수 있는 플랫폼이 이미 있는 조직에서만 지금 모양으로 존재할 수 있다.** 그 플랫폼이
  없으면 뮤테이션 소견을 어디에 띄울지, 되받은 신호를 누가 받을지가 통째로 빈다.
  **이 논문은 그 플랫폼을 주어진 것으로 두고 시작한다.**
  - **그리고 그 플랫폼 쪽 장에는 뮤테이션이 한 번도 나오지 않는다.** 그 장이 드는
    분석기 계열은 컴파일러 확장·파일 사이 관계·설정 파일·산출물 크기이고, **테스트
    스위트의 적절성을 묻는 분석은 목록에 없다.** 두 문헌이 같은 배선을 공유하면서
    서로를 가리키지 않는다. **사람이 볼 자리다.**
  - **그 플랫폼 쪽 판단들의 정본은 이 KB에 따로 있다** —
    [체감 오탐률](../concepts/effective-false-positive-rate.md) ·
    [정적 분석을 개발 흐름의 어디에 끼울 것인가](static-analysis-workflow-integration-points.md) ·
    [정적 분석을 생태계로 — 검사를 들이는 관문과 되먹임](static-analysis-check-admission-and-feedback.md) ·
    [분석 억제를 프로젝트 단위로 두기](project-level-analysis-customization.md)다.
  - **2020년 자기 보고의 근거 등급은 `industry-norm`이고 이 페이지의 두 소스와 격이
    다르다.** 이 절이 그 소스에서 받는 것은 **배선의 서술**이고, **그것으로 이 논문의 어떤
    수치도 보정하지 않는다.**

## 변경분 한정과 arid 억제 — 실제로 무엇을 하는가

- **변경분 한정(diff-based mutation testing)** (§1·§2).[^petrovic2021-google-mutation]
  뮤턴트를 **바뀐 줄이면서 커버된 줄**에만 만든다. 저자들이 드는 이유가 둘인데, 하나는
  뮤턴트 수를 줄이는 것이고 다른 하나가 이 페이지에서 중요하다 — **그 범위가 개발자의
  작업 단위와 일치해서 테스트를 더할 자리로 자연스럽다**는 것이다.
- **커버리지(code coverage)가 선행 조건이다** (§2.1).[^petrovic2021-google-mutation]
  커버되지 않은 줄의 뮤턴트는 어차피 전부 살아남으므로 만들지 않는다. 줄 단위
  커버리지(line coverage)가 **어느 테스트 대상이 그 줄을 덮는지**까지 알려 주고, 그
  정보로 뮤턴트를 죽이러 돌릴 테스트를 고른다.
- **한 줄에 뮤턴트 하나** (§2.2).[^petrovic2021-google-mutation] 같은 줄의 뮤턴트
  대다수가 운명을 공유한다는 관찰(전부 살아남거나 전부 죽는다)에 근거한다. 죽으면 그
  줄에 더 만들지 않는다.
- **arid 노드 억제** (§3).[^petrovic2021-google-mutation] arid 노드는 **변형하면
  비생산적 뮤턴트가 되는 추상 구문 트리(AST) 노드**다. 판정 규칙이 재귀적이다 — 단순
  노드는 전문가 함수가 판정하고, **복합 노드는 자식이 전부 arid일 때만 arid**다.
  - **억제는 생성 이전에 일어난다** (§1의 Figure 1 캡션과 설명).[^petrovic2021-google-mutation]
    arid 표시가 먼저 붙고, **arid 노드의 뮤턴트는 애초에 만들어지지 않는다.**
  - **규칙은 사람이 손으로 쌓은 것이다** (§3.1).[^petrovic2021-google-mutation]
    `Not useful` 피드백을 보고 한 부류 전체를 막을 만하다고 판단하면 규칙을 하나
    더한다. 저자들이 `So far, we have accumulated more than one hundred rules for arid
    node detection.`이라고 적는다. **언어마다 따로 큐레이션한다.**
  - 규칙 범주는 넷이다 (Table 2, §3.2): 컴파일 불가 방지(그룹 1개) · 동등 뮤턴트 방지
    (13개) · 비생산적이지만 죽일 수 있는 뮤턴트 방지(16개) · 중복 뮤턴트 방지(2개).
  - **일부 규칙은 불건전(unsound)하다고 저자들이 밝힌다**
    (§3.2.3).[^petrovic2021-google-mutation] 흐릿한 이름 대조와 AST 모양 인식을 쓰므로
    생산적인 뮤턴트를 억제할 수도 있다. **그럼에도 불건전한 규칙 쪽에서 체감 유용성
    개선이 훨씬 컸다**고 적는다.
  - 그 불건전한 규칙 하나를 저자들이 검증한 결과 (§3.2.3):[^petrovic2021-google-mutation]
    로그 관련 휴리스틱이 arid로 표시한 노드 **100개를 무작위로 뽑아** 보니 **99개가
    옳게 표시**됐고 1개는 효용이 미미한 경우였다. 이름 대조 억제 규칙은 **함수 계열
    200개가 넘는다**.
- **보고 수에도 상한이 있다** (§2.3).[^petrovic2021-google-mutation] 보고하는 뮤턴트
  수를 **변경 목록의 전체 파일 수의 7배 이하**로 묶는다. 7이라는 값은 수년간 데이터를
  모아 인지 부하와 효과 사이의 절충으로 정한 것이라고 적는다.
- **호출자 지지 판정** — 대장의 호출자는 "diff 한정·arid 제외 실무 규칙"이다.
  **그 두 규칙은 문면으로 확인된다.** 다만 같은 대장이 그것을 "뮤테이션 게이트 조항"의
  근거로 두는데, **이 논문에서 그것은 게이트가 아니다** — 위
  [Google은 절대 점수를 버렸다](#google은-절대-점수를-버렸다) 참조.

## 억제와 선택이 낸 수치

**아래 값은 전부 §5의 결과 절과 표에서 온 것이다. 단위와 분모를 함께 적는다.**

- **데이터셋의 크기** (§5.1).[^petrovic2021-google-mutation] 코드 리뷰를 거친 변경
  목록 **776,740건**을 대상으로 **16,935,148개**의 뮤턴트가 생성됐고, 그중 개발자에게
  **보고된 것이 2,110,489개**, **명시적 피드백이 붙은 것이 66,798개**다. 맥락 데이터셋은
  그 부분집합인 **4,068,241개**이고 언어는 상위 넷뿐이다.
- **억제의 효과** (§5.2, Table 5).[^petrovic2021-google-mutation] 변경 목록 **5,000건을
  무작위로 뽑아** 전통적 방식이 몇 개를 만드는지 따로 돌려 비교했다. **변경 목록당
  생성 뮤턴트 수의 중앙값**이 이렇다.

  | 전략 | 중앙값 | 25·75 백분위 |
  |---|---|---|
  | 억제 없음(전통적 방식) | 820 | 460 · 1,734 |
  | 한 줄 한 뮤턴트만 | 77 | 31 · 138 |
  | arid 억제 + 한 줄 한 뮤턴트(이 논문의 방식) | 7 | 3 · 19 |

  세 분포의 차이는 Mann-Whitney U 검정에서 전부 `p < .0001`이다. **두 자릿수 배수의
  감소**라고 저자들이 정리한다.
- **생존율** (§5.3과 Table 3·4).[^petrovic2021-google-mutation] 생성된 뮤턴트
  전체(16,935,148개)에서 **초기 스위트가 죽이는 비율이 87.5%**이고, 따라서 생존율은
  **12.5%**다. **이 값은 뮤테이션 점수가 아니다** — 위 §5.3 인용 참조.
  - 연산자별 생성 수와 생존율 (Table 4, 분모는 각 연산자가 생성한 뮤턴트 수):
    SBR 11,522,932개(전체의 68.0%)에 생존율 12.7% · UOI 3,137,375개(18.5%)에 9.6% ·
    LCR 1,305,499개(7.7%)에 16.3% · ROR 672,009개(4.0%)에 14.7% ·
    AOR 297,333개(1.8%)에 13.5%.
- **생산성** (§5.4).[^petrovic2021-google-mutation] **피드백이 붙은 보고 뮤턴트
  66,798개 중 82%**가 개발자에게 생산적이라고 라벨됐다. **이 값은 데이터셋 전체를 통틀어
  집계한 것**이라고 저자들이 못 박는다. 서비스 개시 이후 이 비율이 **80%에서 89%로**
  올랐는데, 비생산적 피드백을 일반화해 억제 규칙을 만든 결과라고 적는다.
  - **피드백이 없는 보고 뮤턴트는 이 분석에서 빠진다.** 보고 2,110,489개 대비 피드백
    66,798개이므로 **분모가 보고 전체가 아니다.**
- **억제 규칙의 누적 효과** (§7 결론과 §3.2.5).[^petrovic2021-google-mutation] 초기
  억제 규칙이 생산적 뮤턴트 비율을 **약 15%에서 80%로** 올렸고, 이후 규칙과 정련이
  **89%까지** 올렸다.
- **맥락 기반 선택의 개선** (§5.5).[^petrovic2021-google-mutation] 무작위 선택을
  기준선으로 두었을 때, **생성된 뮤턴트가 살아남을 확률이 40% 넘게, 리뷰어가 수정을
  요청할 확률이 거의 50% 오른다.** 둘 다 **기준선 대비 상대 개선**이다.

## 이 KB의 판정 — 게이트로 쓸 때의 세 금지

**아래는 이 KB가 두 소스를 읽고 내리는 판정이다. 원문이 적은 것과 이 KB가 붙인 것을
구분해 적는다.**

**세 금지가 각각 어느 실증으로 서는지는
[뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md)의
"세 금지가 어느 논문으로 서는가" 절이 표로 적는다.** 아래는 이 두 소스만으로 서는
부분이다.

- **하나. 절대 뮤테이션 점수에 임계값을 걸지 않는다.** 근거는 원문에 있다 — Google이
  그 비율을 지표에서 내린 이유가 **구체적이지도 실행 가능하지도 않고 테스팅을 이끌지
  못한다**는 것이었고(§2), 자기들이 내는 생존율조차 뮤테이션 점수가 아니라고 못
  박는다(§5.3).[^petrovic2021-google-mutation] **가장 큰 규모로 이 기법을 운영한 조직이
  점수 게이트를 쓰지 않는다.**
- **둘. 프로젝트 사이에서 점수를 비교하지 않는다.** 원전이 이미 그 이유를 준다 —
  동등 뮤턴트가 남아 있는 한 점수의 천장이 프로그램마다 다르고, FIND처럼 오래 다듬어진
  코드에서는 그 천장이 눈에 띄게 낮아진다(p.39).[^demillo1978-hints] **천장이 다른 두
  수를 나란히 놓는 것은 비교가 아니다.**
- **셋. 게이트로 쓸 수밖에 없다면 낮은 단일 문턱의 이분 판정만 한다.** 점수의 크기를
  읽지 말고 "문턱을 넘었는가"만 읽는다는 뜻이다. **이 처방은 이 두 소스가 적은 것이
  아니다.** 다만 이제 이 KB의 착상만도 아니다 — 같은 처방을 자기 데이터로 낸 심사
  실증이 [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md)의
  "예측력은 문턱 이분에서만 남는다" 절에 있다.
- **그리고 최종 심급 지위는 없다.** 뮤테이션이 실제 결함을 대신한다는 명제는 결합
  효과에 기대는데, 그 결합 효과에 원전 스스로 **"증명할 길이 없는 경험적 원리"**라는
  눈금을 붙였다(p.35).[^demillo1978-hints] **가정 위에 세운 눈금은 최종 심급이 될 수
  없다.**
- **남는 용도는 두 가지다.** 하나는 원전이 처음부터 그렸던 것 — **리뷰 시점에 던지는
  "어려운 질문"**(p.36)[^demillo1978-hints]이고, 산업 사례가 실제로 배선한 것도
  그것이다(§2.4).[^petrovic2021-google-mutation] 다른 하나는 **같은 대상 안에서 두
  스위트를 견주는 상대 비교**다.

## 시대 지위 — 언어 모델이 만든 스위트에서

- **뮤테이션이 커버리지가 못 보는 것을 본다는 대비는 언어 모델이 만든 테스트에서 다시
  측정됐다.** [MUTGEN](../sources/wang2025-mutgen.md)이 이 KB에 들어온 이유가 그
  동기 진술 하나다 — 커버리지가 만점인 생성 테스트가 뮤테이션 점수는 바닥일 수 있다는
  것.[^wang2025-mutgen] **미심사 프리프린트이므로 방향만 쓴다.**
- **산업 채택도 같은 방향으로 갔다.**
  [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md)이 담은
  Meta의 ACH는 **관문의 마지막 조건을 커버리지에서 뮤턴트 사살로 바꾼** 배선이다.
  여기서도 판정 대상은 점수가 아니라 **개별 뮤턴트**다.
- **다만 조건이 하나 붙는다.** ISSTA 2026의 재현 연구가 커버리지와 뮤테이션 점수의
  유용성이 **맥락에 크게 의존한다**고 보고한다 (초록).[^zhao2026-llm-coverage-replication]

  > in regression-style settings where the code provided to the LLM can be reasonably
  > assumed bug-free, these metrics can provide meaningful signals when comparing across
  > models; in another common scenario where the code-under-test may already be buggy and
  > the goal is to expose the bug within the code-under-test, they no longer serve as
  > reliable indicators.

  **회귀 테스트 맥락에서 모델 사이를 견주는 신호로는 쓸 만하지만, 대상 코드에 이미
  버그가 있고 그 버그를 드러내는 것이 목표인 자리에서는 믿을 만한 지표가 아니라는
  것이다.** 확보본이 arXiv 판이라 이 페이지는 계수를 옮기지 않고 방향만 옮긴다.

## 이 두 소스가 넘지 않은 선

- **1978년 글은 프로그램 하나를 잰다.** 결합 효과의 증거로 내놓은 두 관찰이 전부
  FIND에서 나왔고, 언어는 Fortran 하나다.
- **1978년 글은 실제 결함을 다루지 않는다.** BUGGYFIND는 다른 논문이 만든 다중 오류
  뮤턴트이지 현장에서 보고된 결함이 아니다.
- **1978년 글의 동등 뮤턴트 비율은 추정이다.** 생산 프로그램의 동등률이 1퍼센트를 크게
  밑돈다는 문장에 근거 자료가 붙어 있지 않다 (p.39).[^demillo1978-hints]
- **Google 논문은 조직 하나다.** 저자들이 데이터셋이 자기 회사의 코드 스타일과 리뷰
  관행에 특수할 수 있다고 §5.1에서 적는다.[^petrovic2021-google-mutation] **같은
  레시피를 다른 조직이 재현해 같은 결과를 얻었다는 보고를 이 KB는 확보하지 않았다.**
- **arid 규칙이 이전 가능한 형태가 아니다.** 언어마다 사람이 큐레이션한 100개 넘는
  규칙이고 수년의 피드백 루프로 다듬은 산물이다 (§3.1).[^petrovic2021-google-mutation]
  **그 규칙 없이 같은 생산성 수치가 나온다는 근거는 이 논문에 없다.**
- **생산성 수치의 분모가 좁다.** 위
  [억제와 선택이 낸 수치](#억제와-선택이-낸-수치) 참조 — 82%의 분모는 보고 뮤턴트
  전체가 아니라 피드백이 붙은 것뿐이다.
- **변경분 한정이 무엇을 놓치는지를 이 논문이 재지 않는다.** 바뀐 줄 밖에 있는 결함
  후보를 얼마나 놓치는가는 §5의 연구 질문 넷 어디에도 없다. **그것을 잰 논문은
  [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md)의
  "커밋과 관련 있는 뮤턴트는 변경 바깥에 있다" 절에 있다.**
- **개발자 행동에 미치는 장기 효과는 저자들이 진행 중인 연구로 넘긴다**
  (§7).[^petrovic2021-google-mutation]

## 이어지는 페이지

- [뮤테이션 타당성을 정면으로 잰 여섯 편](../concepts/mutation-validity-evidence.md) —
  이 페이지의 필수 동반. 이쪽이 원전과 산업 운영 기록이고 그쪽이 그 전제를 시험한
  심사 실증 여섯 편이다. 이 페이지의 세 금지가 그쪽에서 수치로 다시 선다
- [단정 수와 단정 커버리지가 뮤턴트 킬을 예측한다](../concepts/assertions-predict-mutation-kills.md)
  — 그 논문의 효과성이 곧 PIT 뮤테이션 점수라 순환이 닫히는 자리. 그쪽이 "별도 페이지의
  물음"이라고 넘긴 것이 이 페이지다
- [커버리지는 뮤턴트 킬을 예측한다](../concepts/coverage-predicts-mutation-kills.md) —
  커버리지 논쟁의 옹호 측. 그쪽도 종속변수가 뮤턴트 킬이라 이 페이지의 물음을 전제한다
- [커버리지 신호는 스위트 크기가 만든다](../concepts/coverage-confounded-by-suite-size.md)
  — 커버리지 논쟁의 회의 측 극
- [커버리지 운용의 산업 권고](../concepts/coverage-operating-guidelines.md) — 단정의
  실질성은 뮤테이션 테스팅이 잰다고 이름으로만 지목한 자리. 그 이름이 무엇을 재고 무엇을
  못 재는지가 이 페이지다
- [커버리지는 단서지 목표가 아니다](../concepts/coverage-as-clue-not-target.md) — 지표를
  목표로 걸면 도구가 정보원이기를 그만둔다는 논증. 이 페이지의 세 금지가 같은 논증의
  뮤테이션 판이다
- [실용주의 스타터 킷](../concepts/pragmatic-starter-kit.md) — 테스트를 사보타주로
  시험하라는 실무 규범. 결함을 손으로 심는 그 절차의 기계 판이 뮤테이션이다
- [생성된 테스트의 필터 체인](../concepts/filter-chain-for-generated-tests.md) — 관문의
  마지막 조건을 커버리지에서 뮤턴트 사살로 바꾼 산업 배선
- [벤치마크의 테스트 부족](../concepts/benchmark-test-inadequacy.md) — 죽인 뮤턴트를
  벤치마크 스위트를 줄이는 세 기준 중 하나로 쓴 자리
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  이 페이지가 방향만 옮긴 대비(커버리지는 만점인데 뮤테이션 점수는 바닥)를 같은 미심사
  소스로 함께 적는 자리. 그쪽은 통과한 생성 테스트의 커버리지가 사람 것에 필적한다는
  심사 실측도 갖는다
- [속성 기반 테스트](../concepts/property-based-testing.md) — 스위트의 감도를 올리는
  다른 길. 이쪽은 결함을 심고 저쪽은 입력을 생성한다
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  살아 있는 뮤턴트가 없다는 사실이 무엇을 증명하지 않는가의 상한

[^demillo1978-hints]: DeMillo, Lipton & Sayward 1978, "Hints on Test Data Selection: Help
    for the Practicing Programmer", *Computer*, 1978년 4월. **locator는 확보본에 인쇄된
    쪽(34~41)이다** — 각 쪽 하단에 `COMPUTER` 또는 `April 1978`과 쪽 번호가 찍혀 있고,
    1쪽 하단에 게재 코드 `0018-9162/78/0400-0034$00.75 © 1978 IEEE`가 있다. **권과 호는
    문면에 없어** 소스 메타의 `volume: 11` · `issue: 4`는 Google 논문 참고문헌 [4]·[30]이
    근거다. 이 페이지가 담은 것은 결합 효과의 정의와 지위, 뮤테이션 절차와 세 용어,
    FIND 예제의 값, 고차 뮤턴트 실험, 동등 뮤턴트 추정이다. Table 1과 Figure 1은 제3자
    경유 값이라 옮기지 않았고, 예제 프로그램의 Fortran 전문과 Table 3·4·6~9의 세부는
    재현 재료라 대표 값만 옮겼다. 직인용은 원문 표기 그대로다.
[^petrovic2021-google-mutation]: Petrović, Ivanković, Fraser & Just 2021, "Practical
    Mutation Testing at Scale: A View from Google", IEEE Transactions on Software
    Engineering. **정본은 IEEE TSE 수용판(early access) 13쪽이고**, arXiv:2102.11378 v2
    22쪽은 대조용으로 함께 보존했다. 두 판의 수치는 이 KB가 대조한 범위에서 같았고 용어만
    다르다(arXiv `surfaced` = 수용판 `reported`). **권·호·쪽수는 early access 판에
    인쇄되지 않아 적지 않았고**, locator는 절 번호와 표 번호다. 게재 사실의 근거는 각 쪽
    상단 띠와 `DOI 10.1109/TSE.2021.3107634`이다. 이 페이지가 담은 것은 §1~§5·§7과
    Table 2·3·4·5다. §4.3~§4.5의 해싱 수식, Figure 2·5의 도형, §6이 전하는 제3자 수치는
    옮기지 않았다. §1 도입부와 초록의 규모 서술도 결과 값이 아니라 옮기지 않았다.
[^zhao2026-llm-coverage-replication]: Zhao, Zhou & Cohen 2026, "Do Coverage and Mutation
    Scores of LLM-Generated Test Suites Correlate with Their Effectiveness? (Replicability
    Study)". **확보본은 arXiv:2607.22880v1이고 같은 1쪽에 게재 레코드가 인쇄돼 있다**
    (Proc. ACM Softw. Eng. 3, ISSTA, Article ISSTA002, October 2026,
    doi 10.1145/3832093). 확보본이 심사 통과본 조판이 아니므로 이 페이지는 계수를 옮기지
    않고 초록이 적는 방향만 옮겼다.
[^wang2025-mutgen]: Wang, Xu, Briand & Liu, "Mutation-Guided Unit Test Generation with a
    Large Language Model". **미심사 프리프린트다**(arXiv:2506.02954 v8). 이 페이지는 이
    소스에서 수치를 옮기지 않고, 커버리지가 만점인 생성 테스트가 뮤테이션 점수는 바닥일
    수 있다는 동기 진술의 방향만 쓴다.

[^winters2020-swe-at-google]: Winters, Manshreck & Wright(큐레이터) 2020,
    *Software Engineering at Google*, abseil.io 공개판(CC BY-NC-ND 4.0), 2026-08-23
    열람본. 이 페이지가 받는 것은 20장 `Static Analysis`(저자 Caitlin Sadowski, 편집
    Lisa Carey)의 §"Usability" · §"Make Static Analysis a Part of the Core Developer
    Workflow" · §"Tricorder: Google's Static Analysis Platform" · §"Integrated Feedback
    Channels" · §"Presubmits"의 해당 줄뿐이다. **공개판 HTML에 쪽 번호가 없어 locator는
    장 번호와 원문 절 제목이다.** 내용은 한국어로 재서술했고 **직인용을 두지 않았다** —
    공개판 라이선스가 파생물을 금하는 CC BY-NC-ND 4.0이기 때문이다. 이 소스의 근거 등급은
    `industry-norm`이고 이 페이지의 다른 소스들과 격이 다르다 — 판정의 정본은
    [소스 메타](../sources/winters2020-swe-at-google.md)다.

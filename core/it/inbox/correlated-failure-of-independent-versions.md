---
type: concept
title: 독립 개발 판본의 실패 상관
description: 독립적으로 만들어진 것들이 독립적으로 틀리지는 않는다는 1986년의 실험 반증 — 같은 명세에서 만든 27개 판본을 100만 건에 돌려 독립 실패 모형을 99% 신뢰수준에서 기각한 결과, 결함이 동일하지 않아도 동시 실패가 나는 기제, 저자들이 결론짓지 않은 것을 저자 자신이 못 박은 1990년 반박문, 이 고전을 지금 조건으로 옮길 때 물어야 할 것, 반대 극의 문면이 왜 전부 반박문 경유인가, 그리고 같은 물음을 언어 모델에 건 현대 대응물이 어디에 있는가
status: draft
generated: { by: "claude-opus-5", at: "2026-08-21T18:00:00Z" }
sources:
  - { id: knight1986-nversion, resource: /it/sources/knight1986-nversion.md }
  - { id: knight1990-reply, resource: /it/sources/knight1990-reply.md }
  - { id: kim2025-error-correlation, resource: /it/sources/kim2025-error-correlation.md }
---

# 독립 개발 판본의 실패 상관

- [이 페이지의 범위](#이-페이지의-범위)
- [무엇이 걸려 있었는가](#무엇이-걸려-있었는가)
- [실험 설계](#실험-설계)
- [개별 판본은 매우 신뢰할 만했다](#개별-판본은-매우-신뢰할-만했다)
- [동시 실패는 독립 모형으로 설명되지 않는다](#동시-실패는-독립-모형으로-설명되지-않는다)
- [왜 함께 틀리는가](#왜-함께-틀리는가)
- [저자들이 결론짓지 않은 것](#저자들이-결론짓지-않은-것)
- [근거 등급은 고전이다](#근거-등급은-고전이다)
- [반대 극과 그 문면의 출처](#반대-극과-그-문면의-출처)
- [LLM 시대의 지위](#llm-시대의-지위)
- [이 실험 앞뒤의 이론](#이-실험-앞뒤의-이론)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **서로 모르는 사람들이 같은 명세로 따로 만든 판본들은, 서로 다른 입력에서
틀리는가.**

## 이 페이지의 범위

이 페이지가 담는 것은 **프로그램 판본**에 대해 실제로 측정된 결과 하나와 그 결과에
붙은 단서들이다. "판정자가 독립이어야 믿을 수 있다"는 더 넓은 물음의 **고전 원전**이
여기 있지만, 그 물음 전체를 여기서 답하지는 않는다.

이 실험이 반증한 명제는 정확히 이것이다 — **독립 작성이 독립 실패를 보장한다.** 두
낱말의 층이 다르다는 것이 요점이다. 작성 과정이 격리돼 있어도(서로 모르고, 3,000
마일 떨어져 있고, 대화가 금지돼 있어도) 실패가 나는 **입력**은 겹칠 수 있다.

## 무엇이 걸려 있었는가

N-버전 프로그래밍(N-version programming)은 같은 기능의 판본 여러 개를 나란히 돌리고
투표기(voter)가 다수의 출력을 고르는 내결함성(fault tolerance) 기법이다. 두 소스가 쓰는
용어를 여기서 한 번에 고정한다 — 여러 판본이 같은 입력에서 함께 실패하는 것이
**동시 실패(coincident failures)**이고, 그 동시성이 우연으로 설명되는 정도를 넘어설 때
**상관 실패(correlated failures)**이며, 판본들을 서로 다르게 만들려는 성질이
**다양성(diversity)**이다. `voter`를 이 페이지에서 **투표기**로 옮기는 것은 의도적 분기다 —
[KRaft 컨트롤러 쿼럼](kraft-controller-quorum.md)의 `voter`는 표를 던지는 **노드**라
투표자이고, 여기의 `voter`는 판본들의 출력을 받아 하나를 고르는 **장치**다. 이 기법이
약속한 신뢰도 개선의
근거가 **독립 가정**이었고, 그것을 두 저자가 반박문에서 반대편 문면 그대로 옮겨 둔다
(§1).[^knight1990-reply]

> It is the fundamental conjecture† of the NVP [N-Version Programming] approach that the
> independence of programming efforts will assure a low probability that residual software
> design faults will lead to an erroneous decision by causing similar errors to occur at the
> same c[ross]c[heck]-points in two or more versions... The effectiveness of the NVP approach
> depends on the validity of this conjecture...

- **가정이 참이면 산술이 크게 유리해진다** — N개 판본이 독립으로 실패하면 N-버전 시스템의
  실패 확률은 1차 근사로 개별 판본 실패 확률의 N제곱에 비례하므로, 시스템의 신뢰도가
  부품의 신뢰도보다 높아질 수 있다 (§1).[^knight1986-nversion]
- **그래서 검정 가능한 형태로 좁혀야 했다** — 반박문은 반대편이 쓴 "낮은 확률"·"likely하지
  않다"라는 말이 수량화돼 있지 않아 그 자체로는 검정 불가능이고, 대신
  **통계적 독립(statistical independence)**은
  정의가 분명하며 실무자들이 실제로 그것을 가정한다고 적는다 (§1).[^knight1990-reply]
- **독립의 정의는 통계 교과서의 것을 그대로 쓴다** (§5):[^knight1986-nversion]

  > Two events, A and B, are independent if the conditional probability of A occurring given
  > that B has occurred is the same as the probability of A occurring, and vice versa. That is
  > pr(A|B) = pr(A) and pr(B|A) = pr(B). Intuitively, A and B are independent if knowledge of
  > the occurrence of A in no way influences the occurrence of B, and vice versa.

## 실험 설계

- **판본 27개, 단일 명세, 두 대학** — 버지니아 대학교(UVA) 9개와 캘리포니아 대학교
  어바인(UCI) 18개를 하나의 요구사항 명세에서 만들었다 (§2).[^knight1986-nversion]
  대상은 항공우주 기업에서 온 대미사일 판정 문제(launch interceptor problem)이고, 레이더
  반사 자료를 받아 요격 발사 여부를 정한다.
- **격리는 강제했고 참조 자료는 막지 않았다** — 학생들에게 독립 개발의 필요를 강조하고
  서로 논의하지 말라고 지시했으나 참조 문헌에는 제한을 두지 않았다. 두 학생이 같은
  참고 자료를 보는 것은 두 조직이 같은 자료를 보는 것과 다르지 않다고 판단해서다
  (§2).[^knight1986-nversion] 명세에 대한 질문은 구두 응답으로 정보가 새지 않도록 전자
  우편으로만 주고받았고, 명세의 일반적 결함이 드러나면 답을 전원에게 방송했다.
- **수용 절차(acceptance procedure)는 판본마다 다른 200건이었다** — 공통 수용 시험이
  공통 결함을 걸러 내는 것을 막으려고 판본마다 다른 200건의 무작위 입력을 썼다
  (§2).[^knight1986-nversion] 이 절차의 지위를 반박문이 뒤에 못 박는다 — 그것은
  **실험 장치이지 소프트웨어 개발 공정의 일부가 아니었고**, 실험 영역 밖의 결함을 찾아
  없애 실험을 편향시키지 않으려고 일부러 건수를 늘리지 않았다 (§3.2).[^knight1990-reply]
- **판정 기준은 28번째 판본(gold program)이다** — 각 테스트 케이스마다 판본은 15×15 불리언
  배열과 15원소 불리언 벡터와 발사 결정 하나, 합쳐 **241개 결과**를 낸다. 그중 하나라도
  gold program과 어긋나거나 실행 중 예외가 나면 그 판본의 그 케이스는 실패로 기록했다
  (§4).[^knight1986-nversion]
- **모의 운용은 100만 건이다** — 판본 27개와 gold program을 무작위 생성 입력 100만 건에
  돌렸고, 1984년 5월부터 9월까지 컴퓨터 15대를 썼다 (§2).[^knight1986-nversion] 이 입력이
  무작위인 이유를 반박문이 밝힌다 — 그것은 시험이 아니라 **수명 주기 사용의 모의**였고,
  난수는 Boeing 쪽이 이 응용에 현실적이라고 본 운용 프로파일을 따라 뽑았다
  (§3.2).[^knight1990-reply]

## 개별 판본은 매우 신뢰할 만했다

이 절의 수치가 뒤 절의 결론을 지탱한다. **판본이 조악해서 함께 틀린 것이 아니다.**

- **Table 1(판본별 실패 데이터, 분모는 판본마다 100만 건)** — 27개 중 6개는 실패가 하나도
  없었고, 나머지도 전부 99%를 넘는 성공률을 보였다. 27개 중 23개가 99.9%를 넘겼다
  (§4, Table 1).[^knight1986-nversion] 가장 나쁜 판본은 100만 건 중 9,656건에서 실패해
  성공 확률 0.990344였다.
- **반박문이 같은 사실을 비교 형태로 다시 적는다** — 평균 실패 확률은 0.0007이고 최악은
  0.009였으며, 이것은 발표된 비판자 쪽 실험들보다 좋은 값이라고 적는다
  (§3.1).[^knight1990-reply] 같은 반박문의 Table 1은 이 실험(판본 27개, 입력 100만 건,
  판본당 평균 실패율 0.0007, 3-버전 실패율 0.00004)과 NASA 실험(판본 20개, 입력 921,000건,
  0.006, 0.0002)만 **통계적 독립 실패 거동 = no**로 채우고, 나머지 세 실험(Chen·Kelly·UCLA/H)의
  같은 칸을 **not tested**로 비워 둔다 (§2, Table 1).[^knight1990-reply]
- **결함 수도 적었다** — 27개 판본 전체에서 찾은 결함은 45개이고, 판본별 분포가 Table 4에
  있다 (§6, Table 4).[^knight1986-nversion] 여기서 결함(fault)은 실행됐을 때 그 판본을
  실패하게 만드는 프로그램 본문의 사례를 뜻하며, 비슷한 두 조건에 같은 실수를 하면 두 개로
  센다 (§6).[^knight1986-nversion]

## 동시 실패는 독립 모형으로 설명되지 않는다

- **Table 2(동시 실패 발생, 분모는 테스트 케이스 100만 건, 집계 단위는 케이스)** —
  한 케이스에서 둘 이상의 판본이 실패한 횟수다 (§4, Table 2).[^knight1986-nversion]

  | 같은 케이스에서 실패한 판본 수 | 발생 케이스 수 |
  |---|---|
  | 2 | 551 |
  | 3 | 343 |
  | 4 | 242 |
  | 5 | 73 |
  | 6 | 32 |
  | 7 | 12 |
  | 8 | 2 |

  저자들이 "27개 중 8개가 함께 실패한 케이스가 있다는 것이 놀랍다"고 적는 자리다
  (§4).[^knight1986-nversion] **Table 2의 확률 열은 관측 상대도수(발생 수 나누기 100만)이지
  독립 가정 아래 기대되는 값이 아니다** — 이 논문은 기대 건수를 표로 인쇄하지 않는다.
- **같은 학교끼리 몰렸을 것이라는 예상은 빗나갔다** — Table 3은 UVA 판본과 UCI 판본
  사이의 공통 실패 횟수를 담은 행렬이고, 예비 결함 분석에서 **공통 결함은 전부 두 학교
  판본에 걸쳐 있었다** (§4, Table 3).[^knight1986-nversion] 반박문도 같은 사실을
  격리 논점에서 되풀이한다 — 일부 프로그래머는 3,000마일 떨어져 있었고 서로를 몰랐으며,
  모든 상관 실패가 두 학교 판본을 함께 물었다 (§3.6).[^knight1990-reply]
- **검정과 기각** — 판본 수 N = 27, 테스트 수 n = 1,000,000, 둘 이상이 실패한 케이스
  수 K = 1,255에 대해 (§5):[^knight1986-nversion]

  > With these parameters, the statistic z has the value 100.51. This is greater than 2.33
  > which is the 99% point in the the standard normal distribution, and so we reject the null
  > hypothesis with a confidence level of 99%.

  K = 1,255는 위 Table 2 열의 합이다. 검정 통계량 z는 관측 K와 독립 모형의 기대
  건수 nP(more)의 차를 표준편차로 나눈 값인데, **논문은 z만 인쇄하고 nP(more)의 값은
  적지 않는다.** 귀무가설은 "독립 실패에서 유도한 모형이 이 자료의 옳은 모형이다"이고,
  모형에서 의심스러운 부분이 독립 가정뿐이므로 저자들은 그 가정을 기각한다.

## 왜 함께 틀리는가

- **상관 결함은 대체로 더 미묘했다** (§6).[^knight1986-nversion] 논문이 예로 든 것이 둘이다.
  - **각도 비교를 코사인 비교로 바꾼 것** — 임의 정밀도에서는 옳은 치환이지만 유한 정밀도
    부동소수점에서는 아니다. 명세의 비기능 요구 (2)가 유효숫자 6자리로 비교하는 함수를
    쓰라고 못 박았기 때문에 정밀도가 한 번 더 깎였다. 27개 중 **4개**가 이 가정을 했고,
    이 결함이 낸 실패는 판본마다 71회에서 206회 사이였으며, 이 결함 때문에 둘 이상의
    판본이 같은 케이스에서 실패한 것은 **8회**였다 (§6).[^knight1986-nversion]
  - **세 점이 일직선인 두 번째 경우의 누락** — 세 점이 이루는 각이 0도이거나 180도이면
    일직선인데, 둘째 경우를 빠뜨린 프로그래머가 여럿이었다. 같은 결함인데도 효과는 달라
    한 판본은 231회, 다른 판본은 37회 실패했다. 다만 **뒤쪽이 실패할 때는 언제나 앞쪽도
    실패했다** (§6).[^knight1986-nversion]
- **저자들은 이 결함들을 명세 탓으로 돌리지 않는다** — 앞의 것은 수치 해석에 대한 근본적
  이해 부족이고 뒤의 것은 기하에 대한 이해 부족이며, 명세는 앞선 실험에서 이미 다듬어져
  있었고 문제의 공통 결함들 중 모호·불일치·결손에 걸리는 것은 없다는 것이 저자들의
  판단이다 (§6, §8).[^knight1986-nversion]
- **결함의 절반이 여러 프로그램에 걸쳐 있었다** (§8):[^knight1986-nversion]

  > Based on a preliminary analysis of the faults in the programs, we have found that
  > approximately one half of the total software faults found involved two or more programs.

  저자들이 붙인 가설이 셋이다 — 어떤 문제의 어떤 부분은 그냥 더 어려워서 결함 분포가
  프로그래머가 아니라 문제의 산물이라는 것, 고유한 결함일수록 컴파일러나 시험에 먼저
  잡힌다는 것, 그리고 공통 결함이 표준적인 검증·확인으로는 잘 안 잡히는 어려운 의미론적
  국면이나 전형적 인간 오해를 반영한다는 것이다 (§8).[^knight1986-nversion]
- **여기가 이 페이지의 핵심 기제다 — 결함이 같지 않아도 동시 실패가 난다** (§2):[^knight1990-reply]

  > In fact, faults do not need to be identical to produce statistically-dependent coincident
  > failures. Many of the faults in our programs that produced such failures were seemingly
  > unrelated on the surface, sometimes occurring in totally unrelated parts of the programs.
  > This puzzled us until we realized that the relationship is in the functions computed by
  > the paths taken for that input rather than in any particular ‘‘faulty’’ statements on that
  > path.

  그래서 반박문은 **결함 목록의 비교로는 독립을 판정할 수 없다**고 못 박는다. 투표로 결함
  감내를 하려 할 때 비교되는 것은 중간 결과와 출력이지 결함이 아니고, 독립은 통계적 성질이라
  통계적으로 검정해야 한다 (§2).[^knight1990-reply]
- **시험을 더 해서 지우는 문제가 아니라는 방증도 같은 절에 있다** — 반박문은 Shimeall &
  Leveson 1988이 판본 8개로 결함 제거와 내결함성을 비교했을 때 **광범위한 시험이 상관
  실패를 낳는 결함을 찾아낼 가능성이 낮았다**고 적고, 그 이유를 이렇게 붙인다 (§3.2):[^knight1990-reply]

  > This makes some sense intuitively since there is reason to believe that if these common
  > errors are likely to be made by the programmers, they are also likely to be made by those
  > constructing test data.

  **판정자가 대상과 같은 오해를 공유하면 판정이 통과시킨다**는 명제이고, 이 페이지가
  프로그램 판본 층에서 잰 것과 같은 것을 시험 데이터 층에서 말한 것이다. 다만 Shimeall &
  Leveson 1988의 원문은 확보하지 않았으므로 이 서술은 반박문을 통한 전언이다.

## 저자들이 결론짓지 않은 것

**이 절이 이 페이지의 단서 본문이다.** 이 실험은 30년 넘게 결론이 확대 인용돼 왔고,
저자들이 1990년에 직접 그 확대를 끊었다. 아래 두 인용은 반박문이 옮긴 **출판본 결론
문면**이다. 확보한 저자본 §8의 문면은 이보다 넓다(소스 메타 참조).

- **① 결론은 이 응용에 조건부다** (§4):[^knight1990-reply]

  > For the particular problem that was programmed for this experiment, we conclude that the
  > assumption of independence of errors that is fundamental to some analyses of N-version
  > programming does not hold. Using a probabilistic model based on independence, our results
  > indicate that the model has to be rejected at the 99% confidence level.

  그리고 바로 뒤에 (§4):[^knight1990-reply]

  > It is important to understand the meaning of this statement. First, it is conditional on
  > the application that we used. The result may or may not extend to other programs, we do
  > not know. Other experiments must be carried out to gather data similar to ours in order to
  > be able to draw general conclusions.

  반박문은 이 문단 뒤에 "This was our only conclusion"이라고 한 줄로 못 박는다
  (§2).[^knight1990-reply]
- **② "쓰지 말라"가 아니라 "초고신뢰성 수단으로 신뢰하지 말라"다** (§4):[^knight1990-reply]

  > We did not say that N-version programming should not be used although it would not be our
  > first choice of techniques for increasing reliability and safety. We just do not believe
  > that it should be relied upon to provide ultra-high reliability.

  여기서 초고신뢰성(ultra-high reliability)의 기준이 뒤에 붙는다 — 미 연방항공청은 상용
  여객기의 임계 시스템 실패가 "extremely improbable"할 것을 요구하고 그것은 해당 기종
  전 기단의 수명 전체 동안 일어날 것으로 예상되지 않는다는 뜻이며, 분석 가능한 자리에서는
  실무상 운용 시간당 또는 착륙 같은 사건당 **10의 마이너스 9제곱(10⁻⁹)회 이하**로 읽힌다
  (§4).[^knight1990-reply] 저자본 §8도 같은 방향을 이미 적었다 — 결과는 N-버전 시스템의
  신뢰도가 독립 가정 아래 이론이 예측하는 만큼 높지 않을 수 있다는 뜻이지 기법이 작동하지
  않는다는 뜻이 아니며, 구현 문제가 풀린다면 더 큰 N과 동시 오류 모형으로 필요한 신뢰도에
  도달할 수도 있다 (§8).[^knight1986-nversion]
- **③ 다양성이 해법이 아니라는 뜻도 아니다** — 저자본 §8은 무작위에 기대어 다양성을 얻고
  설계 결함을 없애는 것이 효과적이지 않을 수 있다고 적으면서, 곧바로 그것이 다양성이
  해법이 아니라는 뜻은 아니라고 덧붙인다. 하드웨어 설계자들은 단순 중복이나 독립 생성된
  다양한 설계에 기대지 않고 **공통 고장 모드를 찾아 설계를 체계적으로 바꾼다**는 것이
  저자들이 가리킨 방향이다 (§8).[^knight1986-nversion]

## 근거 등급은 고전이다

**근거 등급: `classic`.** 심사 저널에 실린 실증이지만 1986년 실험이고, 이 KB에서
고전 원전을 인용할 때의 의무는 **전이 조건을 적는 것**이다. 옮겨 쓸 때 확인할 조건이
이렇게 갈린다.

| 1986년의 조건 | 지금 조건으로 옮길 때 물을 것 |
|---|---|
| 대학원생·상위 학부생 27명. 27명 중 21명은 학위 과정 밖 프로그래밍 경험이 1년 미만, 3명이 2~5년, 2명이 5년 초과 (§7)[^knight1986-nversion] | 판정자의 숙련도가 다르면 결과가 달라지는가. 반박문은 방향조차 자명하지 않다고 본다 |
| Pascal 고정, 컴파일러와 운영체제까지 지정 (§2)[^knight1986-nversion] | 판본들이 언어·런타임·라이브러리를 공유하는가 |
| 단일 요구사항 명세. 알고리즘과 구현 정보를 일부러 뺐다 (§3.5)[^knight1990-reply] | 명세가 "무엇"만 담는가 "어떻게"까지 담는가 |
| 판본 길이 327~1004줄(저자본 §7) 또는 310~781줄·평균 554줄(반박문 §3.4, 입출력문 제외) | 이 규모의 결과를 큰 시스템에 옮길 수 있는가 |
| 부동소수점 기하 판정 문제. 유효숫자 6자리 비교 함수 지정 | 문제에 "본질적으로 어려운 부분"이 있는가. 있다면 그 부분이 상관을 만든다 |
| 실패 판정을 gold program 하나가 맡았다 (§4)[^knight1986-nversion] | 지금 판정의 기준은 무엇이고 그것은 판본들과 독립인가 |

- **저자들 자신이 한정한 자리** — 판본 길이가 실시간 시스템 대부분보다 훨씬 짧으므로
  이 결과는 **큰 시스템의 작은 조각을 중복하는 경우에만 관계한다.** 다만 경제적으로
  전체를 이중·삼중화하는 프로젝트는 드물고 가장 임계인 기능만 갈라내 내결함성 장치를 거는
  쪽이 현실적이므로, 그 점에서는 이 문제가 오히려 현실적이라는 것이 저자들의 반론이다
  (§7).[^knight1986-nversion]
- **다양성을 잴 자가 없다는 문제는 그대로 남는다** (§3.4):[^knight1990-reply]

  > Since there is no precise definition of diversity, it is impossible to determine whether
  > diversity is present or not in any set of program versions.

## 반대 극과 그 문면의 출처

이 논쟁에는 반대 극이 실재한다 — UCLA의 Avižienis(Avižienis) 진영이다. **그런데 이 KB에는
그쪽 원전 페이지가 없으므로 이 페이지에 `contradicts` 엣지를 걸 상대가 없다.** 그래서
모순 쌍을 만들지 않고, 반대 극이 어디 있고 그 문면이 어떤 경로로 여기 왔는지를 적는다.

- **반대 극의 주장은 전부 반박문 안의 인용으로만 이 KB에 들어와 있다.** 반박문은 비판자
  문장을 이탤릭 직인용으로 옮기고 하나씩 답하는 형식이다 (§1).[^knight1990-reply]
  곧 **인용을 고른 사람이 반대편이고, 이것은 2차 경유다.** 예컨대 방법론 비판은 이렇게
  옮겨져 있다 (§1):[^knight1990-reply]

  > It must be concluded that the authors are assessing their own ad hoc processes for writing
  > multiple programs, rather than the NVP process as developed at UCLA, and that their
  > numerical results uniquely take the measure of the quality of their casual programming
  > process and their classroom programmers.

- **비판의 게재 지위에 대한 K&L의 주장** (§1):[^knight1990-reply]

  > None of the papers criticizing our experiment have appeared in a refereed journal or been
  > presented in a forum in which we could respond.

  **이것은 K&L 쪽의 주장이지 제3자 확인이 아니다.** 반박문 자신도 심사 저널 논문이 아니라
  같은 이유로 고른 발표 자리다.
- **쟁점의 뼈대는 "다르게 만들었으면 결과가 달랐다"이고, 반박문의 답은 "그것도 실험으로
  보여야 한다"이다** (§3.2).[^knight1990-reply] 반박문은 개발 절차의 차이가 상관 실패
  수를 통계적으로 유의하게 바꾼다는 것을 같은 응용에 대한 통제실험으로 보여야 하며 그런
  자료는 없다고 적는다. 그리고 §3.4에서 반대편 방식이 명세에 설계 정보를 담아 오히려
  다양성을 좁힌다는 반론을 편다.
- **재현에 대한 K&L의 주장** — 반박문은 실험 절차가 완전히 재현 가능하고 실제로 결과가
  확인됐다고 적으며, NASA 랭글리의 Eckhardt가 이끈 집단이 같은 종류의 자료를 모아 같은
  결론에 이르렀다고 밝힌다 (§2).[^knight1990-reply] 그 NASA 실험의 원문은 확보하지
  않았으므로 이 서술은 반박문을 통한 전언이다.

## LLM 시대의 지위

이 절은 두 소스의 주장이 아니라 이 KB의 읽기다.

- **이 실험이 재는 것은 지금 다시 물어야 하는 형태로 살아 있다.** 판정을 여러 주체에
  나눠 맡기고 일치를 신뢰의 근거로 쓰는 구조는 그때 판본과 투표기였고 지금은 여러 모델과
  합의다. 반증된 명제도 그대로 옮겨진다 — **따로 만들었으니 따로 틀릴 것이다.**
- **동일 기반 모델을 쓰는 판정자들은 정의상 독립이 아니다.** 위 §5에 인용된 독립의 정의는
  한쪽 사건의 발생이 다른 쪽의 확률을 바꾸지 않을 것을 요구하는데, 같은 기반 모델·같은
  훈련 코퍼스·같은 프롬프트 틀을 공유하는 판정자들은 그 조건을 만족할 이유가 없다.
  **이것은 이 KB의 판정이지 K&L의 주장이 아니다.** K&L의 자료가 말해 주는 것은 그보다
  강하다 — 공유 기반이 **없는** 조건(다른 학교, 다른 기계, 서로 모르는 사람들)에서도
  상관이 남았다.
- #hypothesis **같은 설계를 언어 모델로 재현한 미심사 연구가 둘 있고 결론 방향이 갈린다.**
  한쪽은 N-버전 구성이 유용하다는 쪽이고 다른 쪽은 독립성이 성립하지 않는다는 쪽이다.
  둘 다 데이터 오염(data contamination)을 논하지 않는다. 이 KB는 그 둘의 원문을 확보하지
  않았으므로 **이름도 수치도 옮기지 않는다** — 지금 이 자리에 적을 수 있는 것은 "미심사
  재현이 있고 방향이 갈린다"까지다.
- **모델 사이의 오답 수렴에는 이제 실측이 있다** — 리더보드 두 곳의 모델 349개와 71개를
  쌍으로 놓고 재자, 두 모델이 모두 틀렸을 때 같은 오답을 고르는 비율이 우연 기준을 크게
  넘었고, 같은 회사·같은 기반 아키텍처(base architecture)를 통제한 뒤에도 **개별적으로 더 정확한 모델끼리
  더 상관돼 있었다** (§3.2, Table 1).[^kim2025-error-correlation] 수치와 분모는
  [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md)이 담는다.
  **그 자료는 위 판정을 한 걸음 더 밀어붙인다** — 벤더를 갈라도 상관이 남는다는 것이
  이 실험과 같은 방향으로 확인됐고, 여기서 재지 못한 것 하나가 거기서 재어졌다.
  개별 신뢰도가 높을수록 상관이 낮아지는 것이 아니라 **높아진다**.

## 이 실험 앞뒤의 이론

- **앞** — Eckhardt & Lee의 이론 작업이 이 실험의 동기다. 두 문서 모두 그것을 인용한다:
  **상관 실패의 확률이 작아도 얻을 수 있는 신뢰도 개선이 크게 깎인다**는 결과이고
  (§1),[^knight1990-reply] 반박문의 참고문헌은 그 제목을 "A Theoretical Basis for the
  Analysis of Multiversion Software Subject to Coincident Errors"로 적는다. 저자본 쪽
  참고문헌은 같은 저자의 1985년 NASA 기술 각서를 가리킨다.
  **원문은 확보하지 않았다 — 이 서술은 K&L 두 문서를 통한 전언이다.**
**뒤쪽 자리는 이 KB에 근거가 없다.** 이 계보의 세 번째 자리에 Littlewood & Miller 1989의
일반화가 있다고 반입 대장이 기록하고, 기록된 방향은 **강제된 방법론 다양화가 동시 실패
확률을 낮추고 이론상 독립보다 나은 거동도 가능하다**는 쪽이다. #speculation K&L의 두 문서는
이 논문을 인용하지 않고 원문도 확보하지 않았으므로 이것은 각주가 붙지 않는 기록이다.
방향을 뒤집어 읽지 않도록 두 극을 갈라 둔다 — **다양화해도 상관이 남는다**는 쪽은
Eckhardt & Lee 계열의 결론이고, **강제 다양화가 동시 실패 확률을 낮춘다**는 쪽이
Littlewood & Miller 쪽 기록이다.

이 계보를 읽고 이 KB가 세우는 방향은 하나다 — **판정 주체를 바꾸는 것보다 정보의 출처와
방법을 가르는 것이 상관을 줄인다.** 이 실험이 반증한 것이 정확히 "주체 교체만으로
충분하다"였고, 저자들이 §8에서 가리킨 해법도 무작위 다양성이 아니라 공통 고장 모드를 찾아
설계를 체계적으로 바꾸는 쪽이었다.

## 이어지는 페이지

- [테스트 오라클](../concepts/test-oracle.md) — 이 기법이 오라클로 쓰일 때의 이름이 의사
  오라클(pseudo-oracle)이고 그 자리가 §5.1의 파생 오라클 갈래다. 이 페이지는 그 오라클의
  전제가 실험에서 어떻게 무너졌는지를 담는다
- [속성 기반 테스트](../concepts/property-based-testing.md) — "코드와 테스트를 같은 사람이
  쓰면 틀린 가정이 양쪽에 들어간다"는 문제와, 저자들이 **다른 사람에게 맡기는 해법을
  다른 이유로 기각한** 자리. 이 페이지는 그 기각된 해법이 설령 채택됐어도 약속한 만큼
  주지 않는다는 실측이다
- [LLM 생성 테스트의 결함 분포](../concepts/llm-generated-test-defect-distribution.md) —
  판정을 짓는 쪽이 기계일 때 그 판정이 어디서 얼마나 틀리는가의 실측. 이 페이지가 사람
  판본 층에서 잰 것과 같은 물음의 다른 층
- [테스팅은 결함의 존재만 보인다](../concepts/testing-shows-presence-not-absence.md) —
  100만 건을 통과해도 남는 비대칭. 이 실험의 개별 판본 신뢰도가 높았다는 사실이 그 상한을
  없애 주지는 않는다
- [하드웨어·소프트웨어·사람의 결함](../concepts/hardware-software-and-human-faults.md) —
  중복이 결함 독립을 전제한다는 같은 구조가 인프라 층에서 반복되는 자리
- [신뢰성과 내결함성](../concepts/reliability-and-fault-tolerance.md) — 결함을 견딘다는
  것이 무엇을 뜻하는가의 어휘
- [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md) — 이 실험과 같은
  물음을 언어 모델에 건 현대 대응물. 판본 대신 모델을, 동시 실패 대신 같은 오답을 세고,
  개별 정확도와 상관의 관계까지 잰 자리
- [데이터 오염](../concepts/data-contamination.md) — 위 LLM 시대의 지위 절이 미심사 재현
  둘에 대해 지적한 미논의 항목의 정의

[^knight1986-nversion]: Knight & Leveson 1986, "An Experimental Evaluation of the Assumption
    of Independence in Multi-version Programming". 확보본이 저자본이라 쪽번호가 인쇄
    저널 쪽(96–109)과 다르므로 locator는 절 번호와 표 번호로만 달았다. 부록(요구사항 명세
    전문)은 실험 자극물이라 옮기지 않았고, 본문 claim을 뒷받침하는 두 대목만 인용했다 —
    비기능 요구 (2)의 REALCOMPARE 유효숫자 6자리 규정과 LIC 3·10의 각도 조건이다.
    Figure 1A/1B/1C(세 점이 일직선인 두 경우)는 도판이라 본문 서술로 대체했다.
    §1 서론의 수치와 사례(A310·스웨덴 국철 등 실사용 목록)는 인용하지 않았다 — 인용은
    전부 §4 이후의 결과·분석·결론 절에서 했다. Table 2의 합 1,255는 §5가 본문에서
    K = 1255로 다시 적는 값이라 이 KB가 계산한 것이 아니다. §3의 프로그래머 배경
    통계(설문 26부)는 전이 조건에 필요한 항목만 §7에서 인용했다.
[^knight1990-reply]: Knight & Leveson 1990, "A Reply to the Criticisms of the Knight &
    Leveson Experiment". 확보본에 쪽번호가 인쇄돼 있지 않아 locator는 절 번호로만 달았다.
    게재처(ACM SIGSOFT Software Engineering Notes 15(1))는 반입 대장 레코드가 근거이고
    확보본 문면이 아니다. 이 문서가 인용하는 반대편(Avižienis·Kelly·Lyu·Joseph) 문장은
    전부 이 문서를 경유한 2차 인용이며, 고른 주체가 반박하는 쪽이다. §3.3(투표 방식)과
    §3.7(프로그래밍 시간)은 논쟁의 세부라 이 페이지에 옮기지 않았다. §2가 예고한 후속
    논문(1990년 2월 IEEE TSE — 동일하지 않은 결함이 왜 동시 실패를 낳는지의 모형)과
    Shimeall & Leveson 1988, Eckhardt 외의 NASA 실험은 원문 미확보라 전언으로만 적었다.
[^kim2025-error-correlation]: Kim, Garg, Peng & Garg 2025, "Correlated Errors in Large
    Language Models", §3.2와 Table 1. **이 페이지는 방향만 옮기고 수치는 옮기지 않는다** —
    단위·분모(모델 쌍 수)·표 위치가 붙은 인용은 전부
    [모델 사이의 오류 상관](../concepts/correlated-errors-across-llms.md)에 있다.
    두 소스는 서로를 인용하지 않으므로 이 실험과 그 논문을 잇는 것은 이 KB의 읽기다.

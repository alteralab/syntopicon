---
type: concept
title: 데이터 캐스케이드
description: 상류의 데이터 문제가 왜 하류에서 늦게·불투명하게·겹쳐서 터지는가 — 고위험 AI 실무자 53명 인터뷰로 정의된 데이터 캐스케이드와 그 다섯 성질, 데이터 작업을 모델 작업보다 낮게 치는 보상 구조라는 배경, 유형 넷과 지역별 분포, 지표가 데이터가 아니라 시스템 전체를 재기 때문에 늦게 보인다는 진단, 그리고 이 논문의 처방이 "상류에 검사를 건다"가 아니라는 것
generated: { by: "claude-fable-5", at: "2026-08-25T00:00:00Z" }
sources:
  - { id: sambasivan2021-data-cascades, resource: /it/sources/sambasivan2021-data-cascades.md }
---

# 데이터 캐스케이드

- [이 페이지의 지위 — 질적 인터뷰 연구다](#이-페이지의-지위--질적-인터뷰-연구다)
- [정의](#정의)
- [다섯 성질](#다섯-성질)
- [왜 이런 것이 흔한가 — 데이터 작업의 저평가](#왜-이런-것이-흔한가--데이터-작업의-저평가)
- [유형 넷과 그 분포](#유형-넷과-그-분포)
- [왜 하류에서야 보이는가 — 지표가 데이터를 재지 않는다](#왜-하류에서야-보이는가--지표가-데이터를-재지-않는다)
- [이 논문의 처방은 무엇인가](#이-논문의-처방은-무엇인가)
- [역어](#역어)
- [이어지는 페이지](#이어지는-페이지)

이 페이지의 질문: **상류에서 생긴 데이터 문제가 하류에서 무엇을 하는가.** 무엇을
검사할 것인가도, 어떻게 막을 것인가도 아니다. 검사를 두지 않았을 때 실제로 벌어진 일의
현장 기록만 여기 든다.

## 이 페이지의 지위 — 질적 인터뷰 연구다

**근거 등급은 `peer-reviewed`다**(CHI 2021 전체 논문, DOI `10.1145/3411764.3445518`).
**그러나 이 논문은 정량 실험이 아니라 반구조화 인터뷰 기반 질적 연구다.** 이 구분을
페이지 첫머리에 두는 이유는, 아래 백분율들이 측정값처럼 생겼지만 측정값이 아니기
때문이다.

- **표본은 고위험(high-stakes) AI 응용에 종사하는 실무자 53명**이고, 2020년 5~7월에
  1인당 약 75분의 반구조화 인터뷰로 모았다 (§3, PDF p.4).[^sambasivan2021-data-cascades]
- **지역 분포**: 인도 23 · 미국 16 · 나이지리아 10 · 케냐 2 · 가나 1 · 우간다 1. 논문은
  아프리카 넷을 `East and West African countries` 14로 묶는다. 남 45 · 여 8, 스타트업
  28 · 대기업 16 · 학계 9 (Table 1, PDF p.5).[^sambasivan2021-data-cascades]
- **모집은 눈덩이·의도적 표집이다** — `snowball and purposive sampling [89] that was
  iterative until saturation` (§3, PDF p.4).[^sambasivan2021-data-cascades] 무작위 표본이
  아니므로 **백분율은 모집단 추정치가 아니다.**
- **백분율의 뜻을 논문이 §3에서 못 박는다** (PDF p.4):[^sambasivan2021-data-cascades]

  > Numbers reported throughout the paper represent the percentage of participants who
  > self-reported a trigger, impact, or signal of data challenges in the interviews.
  > Percentages are derived from coding each transcript for each individual’s experiences
  > of cascades.

- **분석 절차의 출처는 Thomas 2006의 일반 귀납적 접근**(a general inductive approach for
  analyzing qualitative evaluation data)이다 — 논문이 `Following [119]`로 그것을 지목한다
  (§3, PDF p.4, 참고문헌 [119]). **"주제 분석(thematic analysis)"이라는 낱말은 이 논문에
  없다.** 연구자 둘이 독립적으로 전 단위를 여러 번 읽어 포화까지 범주를 세우고, 그룹
  토의로 다듬어 상위 범주 셋(캐스케이드의 특성 ·
  유발 요인 · 캐스케이드 유형)과 하위 범주 18개를 얻었다 (§3, PDF
  p.4).[^sambasivan2021-data-cascades]
- **평정자 간 신뢰도를 재지 않았다** — `Since codes are our process, not product [80],
  IRR was not used` (§3, PDF p.4).[^sambasivan2021-data-cascades]
- **저자 스스로 적은 한계**: COVID-19로 전부 화상·전화 진행이라 **작업 관찰(shadowing)과
  맥락적 조사를 넣지 못했다** (§3 Limitations, PDF p.4).[^sambasivan2021-data-cascades]

**따라서 이 KB가 이 소스를 "실증"이라 부를 때 그것은 현장 증언의 체계적 수집을 뜻하지
정량 측정을 뜻하지 않는다.** 수치를 옮길 때는 분모 53(또는 지역별 23/14/16)과 자기
보고라는 사실을 함께 적는다.

- #hypothesis **분모가 53이라는 것은 산술로도 맞아떨어진다** — 논문은 원값(사람 수)을
  싣지 않지만 45.3%=24/53, 54.7%=29/53, 43.4%=23/53, 32.1%=17/53, 20.8%=11/53이고,
  지역별도 56.5%=13/23, 42.9%=6/14, 62.5%=10/16으로 Table 1의 지역 인원과 맞는다.
  논문이 말한 것이 아니라 이 KB가 확보본 수치로 계산해 본 것이다.

## 정의

**논문이 4절에서 정의를 세운다** (§4.1, PDF p.5, 원문 이탤릭):[^sambasivan2021-data-cascades]

> We define *Data Cascades* based on the empirical results in this study as *compounding
> events causing negative, downstream effects from data issues, that result in technical
> debt over time.*

- **초록이 같은 것을 성질의 나열로 압축한다** (PDF p.1):[^sambasivan2021-data-cascades]

  > Data cascades are pervasive (92% prevalence), invisible, delayed, but often avoidable.

  - **92%의 분모는 인터뷰 참여자 53명이고, 값의 정본 자리는 §4.1이다** — `In our study,
    92% experienced at least one cascade` (PDF p.5). 같은 값이 초록(p.1)과 1절 서론
    (p.2)에도 있으나 서론·초록은 동기 절이므로 이 KB는 **결과 절인 §4.1을 인용
    자리로 쓴다.** 뜻은 "53명 중 92%가 캐스케이드를 하나 이상 **겪었다고 스스로
    보고했다**"이고, 표본은 인도·동서 아프리카·미국의 고위험 도메인 실무자다.
- **캐스케이드는 두 가지에 영향받는다** — (a) AI 개발에 관여하는 행위자들의 활동과
  상호작용(개발자·정부·현장 파트너), (b) AI 시스템이 놓인 물리적 세계와 공동체(예:
  센서로 데이터를 모으는 시골 병원) (§4.1, PDF p.5).[^sambasivan2021-data-cascades]

## 다섯 성질

논문이 §4.1에서 불릿 다섯으로 적는다 (PDF p.5).[^sambasivan2021-data-cascades]

- **불투명(opaque)**:

  > data cascades are complex, long-term, occur frequently and persistently; they are
  > opaque in diagnosis and manifestation—with no clear indicators, tools, and metrics to
  > detect and measure their effects on the system. In the absence of well-defined and
  > timely signals, practitioners turned to proxy metrics (e.g., accuracy, precision, or
  > F1 score), where the unit of measurement is the entire system, not datasets.

- **촉발 조건**: 고위험 도메인에 **관행적 AI 실천을 그대로 적용할 때** 터진다. 데이터를
  운영 업무로 보고, 빨리 움직이고, (데이터 품질이 아니라) 하이퍼파라미터로 모델 성능을
  해킹하고, 상·하류의 사람 문제를 알아볼 채비가 안 된 상태.
- **부정적 영향**: 여러 갈래의 예상 밖 대응을 낳고 **언제나 기술 부채를 남긴다**. 심한
  것은 수혜 공동체에 대한 해, 이해관계자 관계의 소진, 데이터셋 전량 폐기, 값비싼 반복까지
  갔다.
- **중복 발생**: `45.3% experienced two or more cascades each`. **대개 모델 구축의
  상류(upstream)에서 촉발돼 모델 개발·배포의 하류(downstream)에서 나타난다.**
- **대개 피할 수 있다**:

  > Cascades are often avoidable by step-wise and early interventions in the development
  > process, which were, however, exceptional due to factors like undervaluing data,
  > scarcity of data, and partner dependencies.

**지연의 크기가 §4.3 첫 문단에 있다** — `The most severe data cascades were also
long-drawn and completely unknown to practitioners; in some cases, taking 2-3 years to
manifest` (PDF p.7).[^sambasivan2021-data-cascades] 물리적 세계 취약성 유형은
`almost always in the production stage`에서 드러났다 — **배포하고 한참 지나서야 드러난다는
뜻이고, 그동안 문제는 계속 불어난다.**

## 왜 이런 것이 흔한가 — 데이터 작업의 저평가

논문은 유형별 서술에 앞서 캐스케이드를 낳는 **가로지르는 배경** 넷을 §4.2에 둔다
(PDF pp.5–6).[^sambasivan2021-data-cascades] **논문 제목이 그중 첫째에서 나온다.**

- **AI의 인센티브와 통화**: `An overall lack of recognition for the invisible, arduous,
  and taken-for-granted data work in AI led to poor data practices, resulting in the data
  cascades below. Care of, and improvements to data are not easily ‘tracked’ or rewarded,
  as opposed to models.` 모델은 명성과 상승 이동의 수단으로 보고됐고, ML 논문이 인용을
  낳아 채용과 레지던시에서 경쟁력이 된다 (§4.2, PDF p.5). 제목이 된 참여자의
  말:[^sambasivan2021-data-cascades]

  > Everyone wants to do the model work, not the data work

  (P4, 헬스케어, 인도 — §4.2, PDF p.5)
- **데이터 교육**: AI 교과 과정이 깨끗한 값을 가진 장난감 데이터셋(UCI Census·캐글)에
  몰려 있어 실무에 필요한 파이프라인 구축 준비가 안 된다 (§4.2, PDF
  p.6).[^sambasivan2021-data-cascades] 참여자의 말:

  > In real life, we never see clean data. Courses and trainings focus on models and tools
  > to use but rarely teach about data cleaning and pipeline gaps.

  (P37, 헬스케어, 한 서아프리카 국가 — §4.2, PDF p.6)
- **데이터 부트스트래핑**: 고위험 도메인은 지역·인구·현상·종에 특화된 데이터셋을 요구하는데
  기성 데이터가 없다. **참여자 53명 중 74%가 현장 파트너를 통해 처음부터 데이터 수집에
  나섰다** (§4.2, PDF p.6).[^sambasivan2021-data-cascades]
- **하류 책무**: 고위험 AI를 규정하는 성질 하나가 **살아 있는 존재에 대한 함의된 책무**라고
  적는다 (§4.2, PDF p.6).[^sambasivan2021-data-cascades] 소비자 AI는 대체로 70~75% 정확도를
  겨냥하지만 고위험에서는 1%가 결정적이라는 증언이 있다 — **참여자 보고이지 이 논문의
  측정이 아니다.**

**이 절이 아래 유형 넷의 "왜"다.** 캐스케이드는 개인의 부주의가 아니라 **데이터 작업을
모델 작업보다 낮게 치는 보상 구조**에서 나온다는 것이 논문의 진단이고, 그래서 5절 처방도
개인이 아니라 구조를 향한다.

## 유형 넷과 그 분포

**넷이다.** `Our study identifies four root causes for data cascades and corresponding
practitioner behaviours` (§4, PDF p.5).[^sambasivan2021-data-cascades] 빈도순이고, 괄호
안은 **참여자 53명 중 그 유형을 자기 보고한 비율**이다 (Table 2, PDF
p.8).[^sambasivan2021-data-cascades]

| 유형 | 전체 | 인도(23) | 동·서 아프리카(14) | 미국(16) |
|---|---|---|---|---|
| 물리적 세계 취약성과의 상호작용 (Interacting with physical world brittleness) | 54.7% | 56.5% | 42.9% | 62.5% |
| 응용 도메인 전문성 부족 (Inadequate application-domain expertise) | 43.4% | 47.8% | 57.1% | 25% |
| 충돌하는 보상 체계 (Conflicting reward systems) | 32.1% | 30.4% | 57.1% | 12.5% |
| 조직 간 문서화 부실 (Poor cross-organisational documentation) | 20.8% | 17.4% | 35.7% | 12.5% |

Table 2가 유형마다 **유발 요인·영향·신호**를 함께 적는다 (PDF
p.8).[^sambasivan2021-data-cascades]

- **물리적 세계 취약성** — 유발: 깨끗한 훈련 데이터(지저분한 실사용 데이터) · 변덕스러운
  실세계 데이터를 다룰 채비 부족. 영향: 수혜자에 대한 해 · 모델의 완전 실패 · 프로젝트
  포기. 신호: 배포 후 시스템 성능. 하위 갈래는 하드웨어 드리프트 · 환경 드리프트 · 인간
  드리프트 셋이다 (§4.3.1, PDF p.7).[^sambasivan2021-data-cascades] 참여자 인용:

  > Suppose an image is out of focus, there is a drop of oil, or a drop of water on the
  > image, appearing blurry or diffused. A model which is looking at this can easily get
  > confused that an out-of-focus image is cancer.

  (P52, 헬스케어, 인도 — §4.3.1, PDF p.7)
- **응용 도메인 전문성 부족** — 유발: 기술 전문성에 대한 과신 · 개념 증명까지 빨리
  달리기. 영향: 수혜자에 대한 해 · 값비싼 반복. 신호: 시스템 성능 · 사후 도메인 전문가
  자문. 두 대표 사례가 **근거 진리(ground truth)의 주관성**과 **대표성 있는 데이터
  찾기**다 (§4.3.2, PDF pp.7–8).[^sambasivan2021-data-cascades]
- **충돌하는 보상 체계** — 유발: 어긋난 인센티브 · 파트너의 데이터 문해력 부족 · 데이터를
  비기술 업무로 보기. 영향: 값비싼 반복 · 다른 데이터 원천으로 이동 · 프로젝트 포기.
  신호: 시스템 성능 · 소진된 파트너 관계 (§4.3.3, PDF pp.8–9).[^sambasivan2021-data-cascades]
- **조직 간 문서화 부실** — 유발: 데이터 문서화의 가치를 무시. 영향: 데이터셋 일부 또는
  전체 폐기 · 시간과 노력 낭비. 신호: **대개 '우연히' 걸리는 수동 인스턴스 검토**
  (§4.3.4, PDF p.9).[^sambasivan2021-data-cascades]

**이 배열 자체가 이 페이지의 논지다** — 유발 요인 열은 전부 상류(문제 정의·수집·라벨링)에
있고, 영향 열은 전부 하류(모델 평가·배포)에 있으며, 신호 열은 하류에만 있다.

## 왜 하류에서야 보이는가 — 지표가 데이터를 재지 않는다

논문이 5절에서 진단을 적합도(goodness-of-fit)와 데이터 품질(goodness-of-data)의 어긋남으로
정리한다 (§5, PDF p.10).[^sambasivan2021-data-cascades]

- **실무자가 쓴 것은 모델이 데이터에 얼마나 잘 맞는지를 재는 지표뿐이었다.** F1·정확도·
  AUC 같은 적합도 지표는 데이터의 **현상적 충실도**(fidelity)와 **타당도**(validity)에
  대해 알려 주는 것이 없다 (§5, PDF p.10).[^sambasivan2021-data-cascades]
- **데이터의 좋음을 재는 표준 지표가 없다** — `Currently, there are no standardised
  metrics for characterising the goodness-of-data [11, 13]` (§5, PDF
  p.10).[^sambasivan2021-data-cascades]
- **그래서 두 가지가 따라온다** (§5, PDF p.10):[^sambasivan2021-data-cascades]

  > First, these metrics give us no assurances about the quality of the data. Second, they
  > are too late to detect and course-correct from the unforeseen effects of data cascades.

- 5절이 도구 지형의 공백도 지목한다 — 현행 검사·분석 도구는 **데이터셋 분포와 랭글링**에
  몰려 있고, `the upstream work of defining dataset requirements and downstream challenges
  of monitoring incoming live data and measuring impacts often does not receive the
  critical attention it needs` (§5, PDF p.11).[^sambasivan2021-data-cascades]

**이것이 오라클 부재의 데이터판이다.** 판정 근거가 대상 바깥에 없으면 사람은 대상이
내놓는 다른 값을 대리 지표로 쓰는데, 여기서 그 대리 지표의 **측정 단위가 데이터셋이
아니라 시스템 전체**라서 데이터 층의 오류를 분해해 주지 못한다.

## 이 논문의 처방은 무엇인가

**이 KB의 검증 축이 이 소스에 기대는 것은 "검증을 상류에 배치하라"의 근거다. 문면
대조 결과는 부분 지지다.**

- **지지되는 쪽**: 캐스케이드가 상류에서 촉발돼 하류에서 나타난다는 것, 대리 지표가
  **너무 늦다**는 것, 그리고 개입은 **단계적이고 이른** 것이어야 한다는 것이 전부 문면에
  있다(위 인용들). 캐스케이드가 가장 적었던 팀의 실천도 그 방향이다 (§5, PDF
  p.11):[^sambasivan2021-data-cascades]

  > The teams with the least data cascades had step-wise feedback loops throughout, ran
  > models frequently, worked closely with application-domain experts and field partners,
  > maintained clear data documentation, and regularly monitored incoming data.

- **지지되지 않는 쪽**: 논문은 **"상류에 검증 게이트를 세워라"라고 말하지 않는다.**
  처방의 무게는 사회기술적·구조적 변화에 있다 — 인센티브 개편, AI 교육 과정의 실데이터
  문해력, 도메인 전문가·현장 파트너와의 지속 관계, 데이터 문서화 표준, 그리고 애초에
  goodness-of-data 지표를 **만들어 내는 연구**다. 논문 스스로 개인 실천으로는 안 된다고
  못 박는다 (§5, PDF p.10):[^sambasivan2021-data-cascades]

  > Individuals can attempt to avoid data cascades in their model development, but a
  > broader, systemic approach is needed for structural, sustainable shifts in how data is
  > viewed in AI praxis.

- **다만 실무자들이 실제로 쓴 완화책이 소프트웨어 공학의 관행을 닮았다고 적는다** (§5,
  PDF p.11):[^sambasivan2021-data-cascades]

  > many of our practitioner strategies mirrored best practices in software engineering
  > [38, 83]. Anticipatory steps like shared style guides for code, emphasising
  > documentation, peer reviews, and clearly assigned roles—adapted to data—reduced the
  > compounding uncertainty and build-up of data cascades.

- **기술적 검증 배치를 말하는 자리는 2절 관련 연구다** — 이 논문이 Breck 등 선행 연구를
  요약하며 `Such interventions highlight the importance of catching data errors using
  mechanisms specific to data validation, instead of using model performance as a proxy
  for data quality` (§2.3, PDF p.3)라고 적는다.[^sambasivan2021-data-cascades] **이것은
  이 논문의 발견이 아니라 이 논문이 읽은 남의 처방이다.**

**정리하면 이 소스가 떠받치는 것은 "오염은 하류에서 지연·복리로 불어난다"이고, "그러니
검증을 상류에 배치하라"는 결론은 이 소스가 아니라 이 KB의 다른 소스가 낸다.** 이 페이지가
그쪽에 주는 것은 근거이지 처방이 아니다.

## 역어

- **data cascades → 데이터 캐스케이드.** "데이터 폭포"를 쓰지 않는 이유는 이 KB가 이미
  `폭포수`를 waterfall의 역어로 여러 페이지에서 쓰기 때문이다 — 같은 낱말줄기가 두 개념을
  가리키면 검색에서 섞인다. 이 KB의
  [수명 주기의 서빙 단계](../concepts/serving-in-the-lifecycle.md)가 이미 "데이터
  캐스케이드(data cascades)"로 적고 있어 선례도 그쪽이다.
- **high-stakes → 고위험.** 본문은 `high-stakes domains ... that have safety impacts on
  living beings`라 적고, 각주 2가 `involving safety, well-being and stakes (e.g., road
  safety, credit assessment)`로 넓힌다 (§1, PDF p.1 본문과 각주 2).
- **field partner → 현장 파트너**, **application-domain expert → 응용 도메인 전문가**,
  **ground truth → 근거 진리**(이 KB의 오라클 축 표기를 따른다).

## 이어지는 페이지

- [선언적 데이터 품질 제약](../concepts/declarative-data-quality-constraints.md) —
  기대를 제약으로 선언해 상류에 거는 쪽. 그 페이지가 "이 논문이 동기로만 말하고 재지
  않는다"고 남겨 둔 자리, 곧 **검증을 두지 않았을 때 오염이 하류에서 무엇을 하는가**를
  이 페이지가 받는다. 다만 이쪽의 답은 측정이 아니라 증언이다
- [ML 파이프라인의 데이터 검증](../concepts/data-validation-for-ml-pipelines.md) —
  "조기에 잡아라"의 기술 쪽 논거. 그쪽의 근거는 되먹임 고리에 의한 증폭이고 이쪽의 근거는
  현장에서 실제로 걸린 2~3년의 지연이다. **둘의 격이 다르다** — 그쪽은 자기 배포 관측,
  이쪽은 자기 보고 인터뷰다
- [훈련 데이터 품질](../concepts/training-data-quality.md) — 좋은 데이터란 무엇인가를
  특성으로 푸는 쪽. 이 논문은 그 특성 목록조차 **표준화돼 있지 않다**는 것을 문제로 든다
- [데이터 웨어하우스의 데이터 품질 관리](../concepts/data-quality-management.md) —
  나쁜 데이터가 남기는 하류 비용을 웨어하우스 층에서 열거하는 쪽. 이쪽은 같은 구조를
  AI 파이프라인에서, 그것도 수혜 공동체에 대한 해까지 포함해 적는다
- [수명 주기의 서빙 단계](../concepts/serving-in-the-lifecycle.md) — 데이터 엔지니어가
  ML 쪽과 만나는 자리에서 "데이터 캐스케이드가 무엇인가"를 알아야 할 항목으로 든다.
  그 물음의 답이 이 페이지다
- [테스트 오라클 문제](../synthesis/test-oracle-problem.md) — 판정 근거 쪽의 허브.
  데이터 층에는 판정 근거가 없어 시스템 지표를 대리로 쓴다는 이 페이지의 진단이 그 축의
  데이터판이다

**이 KB에 아직 없는 것**: goodness-of-data 지표를 실제로 제안하고 잰 소스가 없다. 이
논문도 그것을 **필요하다고 말할 뿐 만들지 않는다**.

[^sambasivan2021-data-cascades]: Sambasivan, Kapania, Highfill, Akrong, Paritosh, Aroyo
    2021, "'Everyone wants to do the model work, not the data work': Data Cascades in
    High-Stakes AI", CHI '21, doi 10.1145/3411764.3445518. 확보본에 인쇄된 쪽 번호가
    없어 locator는 **확보본 PDF 쪽(1~15)**과 절·표 번호다. 수치가 실린 pp.5·6·7·8은
    150dpi 렌더 이미지로 재대조했다 — [소스 메타](../sources/sambasivan2021-data-cascades.md)
    참조.

---
type: concept
title: 공개 사후 분석에서 본 메타안정 장애
description: 공개된 사건 보고서를 이 실패 모델로 읽어 본 실증 조사 — 열한 개 조직에서 고른 스물두 건이라는 표본과 그것을 고른 방법, 사건별 트리거와 지속 효과와 완화 조치의 분류표, 중단이 한 시간 반에서 사흘까지 갔다는 지속 시간 분포, 원인을 잘못 이해한 수정이 다음 사건을 만든 두 계보, 그리고 모든 메타안정 장애가 대형 중단은 아니라는 단서
status: draft
generated: { by: "claude-opus-5", at: "2026-09-07T06:45:00Z" }
sources:
  - { id: huang2022-metastable-wild, resource: /it/sources/huang2022-metastable-wild.md }
  - { id: bronson2021-metastable, resource: /it/sources/bronson2021-metastable.md }
---

# 공개 사후 분석에서 본 메타안정 장애

- [왜 이 조사가 필요했는가](#왜-이-조사가-필요했는가)
- [표본을 고른 방법](#표본을-고른-방법)
- [스물두 건인가 스물한 건인가](#스물두-건인가-스물한-건인가)
- [사건 분류표](#사건-분류표)
- [지속 시간](#지속-시간)
- [무엇이 얼마나 흔했는가](#무엇이-얼마나-흔했는가)
- [고치려다 더 나쁘게 만든 계보](#고치려다-더-나쁘게-만든-계보)
- [모든 메타안정 장애가 대형 중단은 아니다](#모든-메타안정-장애가-대형-중단은-아니다)
- [이 표가 뒷받침하지 않는 것](#이-표가-뒷받침하지-않는-것)
- [이어지는 페이지](#이어지는-페이지)

하나의 질문: **메타안정 장애(metastable failure)라는 틀이 실제 장애 보고서에서 얼마나 자주
들어맞고, 그때 트리거와 지속 효과와 복구 조치는 무엇이었는가.**

## 왜 이 조사가 필요했는가

- 정의 논문의 공백이 출발점이다 — **정의 논문은 단순화된 예로 메타안정성의 기제를 설명하고
  이 패턴이 흔하다고 주장하기만 했을 뿐, 실제 세계의 발생에 대한 데이터는 제시하지 않았다**
  (§2, p.74).[^huang2022-metastable-wild] 정의 쪽 서술은
  [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md)에 있고, 그
  논문 자신도 사례가 **프로덕션에서 관찰한 것들의 단순화된 판본**이라고 적는다 (§2,
  p.222).[^bronson2021-metastable]
- 조사의 결론 세 가지 (Abstract, p.73):[^huang2022-metastable-wild]
  - **메타안정 장애는 보편적으로 관찰된다.** 열한 개 조직의 스물두 건을 깊이 들여다본다.
  - **메타안정 장애는 여러 심각한 중단에서 되풀이되는 패턴이다.** 예컨대 **지난 10년간
    아마존 웹 서비스의 주요 중단 15건 중 적어도 4건이 메타안정 장애 때문이었다**.
  - 정의 논문의 모델을 **트리거 두 종류와 증폭 기제 두 종류로 분류해 확장하고, 통제된 환경에서
    서로 다른 종류의 메타안정 장애를 재현하는 예제 애플리케이션들로 그것을 확인한다**.
- 표본 수가 적어 보이는 것에 대한 저자들의 답 — **분산 시스템의 다른 장애 유형에 비하면 이
  수가 적어 보일 수 있지만, 메타안정 장애는 대개 여러 시간 지속되는 파괴적 결과를 낳으므로
  연구할 가치가 있는 중요한 장애 부류다** (§2, p.74).[^huang2022-metastable-wild]

## 표본을 고른 방법

- 대상 — **대형 클라우드 인프라 제공자와 훨씬 작은 회사나 서비스의 공개 사후 분석 보고서
  더미를 뒤졌다.** 대형 제공자는 **돈을 내는 고객이 많아 신뢰성과 운영 관행의 투명성을 요구받고**,
  작은 사업체는 **악의적 공격의 표적이 될 만큼 커지기 전까지는 스스로 높은 투명성 목표를
  두고 운영하는 일이 흔하다** (§2.1, p.74).[^huang2022-metastable-wild]
- 규모 — **수백 건의 사건을 분석해 메타안정 상태의 시스템을 그린 소수를 찾아냈다** (§2.1,
  p.74).[^huang2022-metastable-wild] 보고서의 **형식도 정보 수준도 출처마다 달라 작업이 더
  어려웠다** (§2.1, p.74).[^huang2022-metastable-wild]
- 판별 기준 — **일시적 트리거, 작업 증폭이나 지속 효과, 그리고 어떤 특정한 완화 관행**을
  단서로 삼았고, 더 구체적으로는 **트리거가 어떤 과정을 시작시켜 그것이 초기의 트리거로 인한
  문제를 증폭하고 트리거가 제거된 뒤에도 저하된 성능 상태를 지속시키는 패턴**을 찾았다 (§2.1,
  p.74).[^huang2022-metastable-wild]
- 판정의 한계를 저자들이 스스로 표시한다 — **제공된 정보의 범위가 제한적일 때가 잦아 우리는
  메타안정 장애를 식별하는 데 최선의 판단을 쓴다. 우리가 쓰는 가장 중요한 기준은 지속 효과
  기제다.** 사건 서술이 지속 효과의 존재를 분명히 밝히지 않지만 해석에 따라 메타안정 장애가
  그럴듯한 경우는 **회색으로 표시**했다 (§2.2, p.74).[^huang2022-metastable-wild]

## 스물두 건인가 스물한 건인가

- 두 수가 논문 안에 함께 있다. 초록은 **열한 개 조직의 메타안정 장애 22건**을 심층 연구했다고
  적고 (Abstract, p.73), 조사 절은 **21건을 식별한다(표 1)**고 적는다 (§2,
  p.74).[^huang2022-metastable-wild]
- 표 1의 행을 세면 21건이다. 나머지 한 건은 공개 보고서가 아니라 내부자 시각으로 서술한
  트위터의 가비지 컬렉션 사례이며, 이것은 논문의 기여 목록에 별도 항목으로 올라 있다 —
  **가비지 컬렉션이 증폭 기제로 작용하는 새로운 종류의 메타안정 장애에 대한 트위터의 내부자
  시각**(§4) (§1, p.74).[^huang2022-metastable-wild] 그래서 22 = 공개 21 + 내부 1로 읽는
  것이 두 수를 모두 만족시킨다. #hypothesis 논문이 이 산수를 명시적으로 적지는 않는다.

## 사건 분류표

아래는 표 1의 분류 축만 옮긴 것이다. 영향받은 서비스 이름 열은 옮기지 않았고, 원문의 회색
표시(지속 효과가 불분명해 그럴듯한 정도)는 "그럴듯함" 열로 옮겼다. 날짜는 원문 표기 그대로다
(§2.2, 표 1, p.75).[^huang2022-metastable-wild]

| 사건 | 날짜 | 지속(시간) | 트리거 | 지속 효과 | 완화 | 그럴듯함 |
|---|---|---|---|---|---|---|
| GGL1 | 03/12/19 | 4.17 | load spike, config change | cascading overload | load shedding, stop config deploy | |
| GGL2 | 10/31/19 | 21.5 | software bug | retry | load shedding, reboot, capacity increase | |
| GGL3 | 04/08/20 | 3.2 | config change, software bug | retry | config rollback, policy change | |
| GGL4 | 04/30/13 | 1.5 | config change, latent software bug | traffic queue growth, reboots | config rollback, server reboot | |
| AWS1 | 04/21/11 | 66.7 | network config change | retry | config rollback, policy change, load shedding, capacity increase | |
| AWS2 | 06/13/14 | 4.23 | power loss | retry | load shedding, server restart | |
| AWS3 | 09/20/15 | 4.55 | load spike, network disruption | retry, cascading server demotion | load shedding(메타데이터 연산 중지), capacity increase | |
| AWS4 | 12/07/21 | 9.3 | 규모 확장이 촉발한 잠복 소프트웨어 버그가 부하 급증으로 | retry | load rebalancing, load shedding | |
| AZR1 | 07/01/20 | 2.65 | 불특정 부하 불균형, latent config bug | cascading overload | service restart | 그럴듯함 |
| AZR2 | 04/01/21 | 1.15 | 캐시 저하를 부른 software bug | retry | unknown automation, capacity increase | |
| AZR3 | 06/14/21 | 13.25 | latent software bug, load spike | 과부하와 타임아웃에 따른 불특정 큐 증가 | load shedding, 버그 소프트웨어 제거, capacity increase | 그럴듯함 |
| AZR4 | 07/12/21 | 7.92 | software bug 배포, load spike | retry, 기타 불특정 | load rebalancing, trigger hot fix, policy change | |
| IBM1 | 06/11/21 | 73.53 | software bug | retry | load shedding, policy change, trigger hot fix | |
| SPF1 | 04/13 | 미상 | load spike, policy failure | retry | load shedding | |
| SPF2 | 06/04/13 | 8.33 | 예상 못 한 서비스 의존이 부른 load spike | retry, 실패 경로의 과도한 로깅 | trigger hot fix, load shedding | |
| ELC1 | 04/02/19 | 6.67 | 불특정 유지보수, 불특정 오류 | 부하가 부른 ZK 요동이 다시 부하를 키움 | restart, load shedding | 그럴듯함 |
| WIK1 | 03/30/21 | 2.25 | load spike | 불특정 원인의 큐 증가 | load shedding, policy change | 그럴듯함 |
| CCI1 | 07/07/15 | 18.33 | load spike | 경쟁으로 인한 부하 증가 | load shedding | 그럴듯함 |
| CAS1 | 07/27/17 | 미상 | rolling restart | 자기유지되며 커지는 과부하 | policy change | |
| CAS2 | 2020 | 0.16 | 비싼 연산의 load spike | retry | 트리거 제거(안정 상태에서 운영 중이었음) | |
| FB1 | 미상 | 미상 | load spike | software bug | hot fix | 그럴듯함 |

- 조직 구성 — 표본에는 **대형 클라우드 제공자(마이크로소프트·아마존·구글·IBM)와 더 작은
  회사나 프로젝트(스포티파이·일래스틱서치·아파치 카산드라)** 양쪽이 들어 있고, **AWS 4건,
  구글 클라우드 4건, 마이크로소프트 애저 4건**이 포함된다 (§2·§2.2,
  pp.74–75).[^huang2022-metastable-wild]
- 표기 하나 — **애저와 IBM은 직접 연결되는 사건 링크를 제공하지 않는다** (표 1 캡션,
  p.75).[^huang2022-metastable-wild]
- FB1은 정의 논문의 링크 불균형 사례와 같은 사건이다. 그 기제의 상세는
  [지속 효과와 증폭 기제](../concepts/sustaining-effects-and-amplification.md)에 있다.

## 지속 시간

- **관찰된 중단은 1.5시간에서 73.53시간 범위이고, 4시간에서 10시간 사이가 가장 흔했다(지속
  기간을 보고한 사건의 35%)** (§2.2, p.75).[^huang2022-metastable-wild]
- 가장 긴 것 — **IBM1 사건은 사흘 넘게 이어졌다** (§2.2, p.75).[^huang2022-metastable-wild]

## 무엇이 얼마나 흔했는가

- 트리거 — **약 45%가 엔지니어의 실수, 약 35%가 부하 급증이었고, 45%의 사례에 트리거가 하나
  이상 있었다** (§2.2, p.74).[^huang2022-metastable-wild] 자세한 갈래는
  [메타안정 장애의 트리거](../concepts/metastable-failure-triggers.md)에 있다.
- 지속 효과 — **단연 가장 흔한 것은 재시도 정책으로 연구한 사건의 50%가 넘었다** (§2.2,
  p.75).[^huang2022-metastable-wild]
- 완화 — **조절, 요청 폐기, 작업 부하 매개변수 변경 같은 직접적 부하 차단(load shedding)이
  55%가 넘는 사례에 쓰였다. 큐나 밀린 연산을 비우기 위한 재부팅이나 정책 변경 같은 간접적
  기제도 많이 쓰였다** (§2.2, p.75).[^huang2022-metastable-wild]
  - **원문 안에 수치가 두 번 다르게 적혀 있다.** 같은 조사를 두고 §2.2는 부하 차단이 "over
    55%"라 적고 §3.6은 "over 50%"라 적는다 (§2.2, p.75 · §3.6,
    p.80).[^huang2022-metastable-wild] 둘 다 "50%가 넘는다"는 하한은 만족하므로 이 페이지는
    둘을 모두 표기하고 하나로 고르지 않는다.
- 정책 변경의 예 — **CAS1 사건에서 서버들이 클러스터에 합류할 수 있도록 어떤 기능을 껐다**
  (§2.2, p.75).[^huang2022-metastable-wild]
- 사람의 관여 — **관찰된 트리거의 약 50%에 사람의 직접적 관여가 있었다** (§6.2,
  p.85).[^huang2022-metastable-wild]

## 고치려다 더 나쁘게 만든 계보

저자들이 "고쳐서 망가뜨리기(fix to break)"라 부르는 절이다. **장애를 일으키는 과정을 잘못
이해하면 엔지니어가 메타안정 장애에 대한 취약성을 오히려 키우는 장기 수정이나 변경을 채택할
수 있다** (§6.3, p.85).[^huang2022-metastable-wild]

- AWS 계보 (§6.3, p.85):[^huang2022-metastable-wild]
  - **AWS2에서 스토리지 서버들은 자기가 여전히 시스템의 일부인지 확인하려고 락 서비스와 자주
    통신한다. 락 서비스에 과부하가 생기자 스토리지 서버들이 타임아웃과 재시도를 시작해 락
    서비스 과부하를 더 키웠다. 여러 번 재시도한 뒤 서버들은 스스로 강등해 스토리지 작업 처리를
    멈췄다. 락 서비스는 살아 있는 스토리지 서버가 그것을 바쁘게 만들 만큼 남아 있는 한 계속
    과부하 상태였다**.
  - **사건 이후 엔지니어들은 서버가 포기하지 말고 락 서비스에 계속 재시도해야 한다고
    결정했는데, 오래 재시도하지 않은 것이 복구를 망친 이유로 보였기 때문이다. 그러나 무제한
    재시도는 훨씬 큰 부하 증폭을 얹고 지속 효과를 더 심하게 만들 수 있다**.
  - **약 1년 뒤 다이나모DB 데이터베이스에 비슷한 사건(AWS3)이 일어났다. 스토리지 노드들이
    갱신된 멤버십 데이터를 얻으려는 재시도에서 물러나지 않아 대규모 부하 증폭과 메타안정
    장애를 낳았다**.
- 스포티파이 계보 (§6.3, p.85):[^huang2022-metastable-wild]
  - **첫 사건(SPF1) 이후 엔지니어들은 부하 급증과 재시도의 원인을 더 잘 이해하려고 요청 실행의
    오류 경로에 상당한 로깅을 추가했다**.
  - **SPF2에서는 부하 급증과 초기 재시도 이후 그 추가 로깅이 재시도 하나하나의 비용을 키워
    시스템에 부하를 더 얹고 더 많은 요청이 재시도되게 만들었다**.
- 이 계보가 이 실패 모델의 실무 논거다. 근본 원인을 트리거로 잡으면 다음 사건을 만든다는
  정의 논문의 판정과 같은 방향이다. 그 판정은
  [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md)에 있다.

## 모든 메타안정 장애가 대형 중단은 아니다

- **많은 메타안정 장애가 심각한 서비스 지장을 일으킬 만큼 크지만 전부 그런 것은 아니다.
  CAS1 사건은 큰 중단을 일으키지 않은 메타안정 행동의 예다. 또 하나는 우리의 트위터 사례
  연구다. 그 메타안정 장애는 내부 경보를 울릴 만큼은 심각했지만 중단이 되기까지는 한참
  멀었다. 이 온건함은 부분적으로 핵심 성능 지표의 모니터링과 시의적절한 대응 덕분이었다**
  (§6.4, p.85).[^huang2022-metastable-wild]
- 그래서 이 표는 "메타안정 장애의 빈도"가 아니라 "**공개 보고서를 남길 만큼 심각했던**
  메타안정 장애"의 표본이다 (§2, p.74).[^huang2022-metastable-wild]

## 이 표가 뒷받침하지 않는 것

- 이 표는 조사 시점까지 공개된 보고서에서 뽑은 것이고, 가장 최근 항목이 2021년 12월 7일의
  AWS4다 (§2.2, 표 1, p.75).[^huang2022-metastable-wild] 결론절도 그 사건을 이름으로 짚는다 —
  **2021년 12월 7일의 최근 AWS 중단을 포함해** (§8, p.86).[^huang2022-metastable-wild]
  **그 이후의 어떤 사건도 이 소스가 분류하지 않는다.** 뒤에 일어난 중단을 메타안정 장애로
  부르려면 그 사건의 사후 분석을 소스로 따로 들여야 한다.
- 이 표는 빈도의 모집단 추정도 아니다. 표본은 **공개 보고서를 뒤져 최선의 판단으로 고른 것**이며
  회색 표시 항목은 저자 스스로 그럴듯한 정도로 표시했다 (§2.1–§2.2,
  p.74).[^huang2022-metastable-wild]

## 이어지는 페이지

- [메타안정 장애의 정의와 세 상태](../concepts/metastable-failure-definition.md) — 이 표가
  적용한 그 정의
- [메타안정 장애의 트리거](../concepts/metastable-failure-triggers.md) — 표의 트리거 열이
  어떤 분류로 묶이는가
- [지속 효과와 증폭 기제](../concepts/sustaining-effects-and-amplification.md) — 표의 지속
  효과 열이 어떤 분류로 묶이는가
- [메타안정 장애에서 복구하기](../concepts/recovering-from-metastable-failures.md) — 표의
  완화 열이 어떤 전략으로 묶이는가
- [취약 상태를 알아보는 법](../concepts/detecting-the-vulnerable-state.md) — 사건이 되기 전에
  볼 수 있었던 지표
- [하드웨어·소프트웨어·사람의 결함](../concepts/hardware-software-and-human-faults.md) — 무비난
  사후 분석이라는 이 보고서들의 장르
- [비기능 요건](../synthesis/nonfunctional-requirements.md) — 이 페이지가 속한 허브

[^huang2022-metastable-wild]: Huang, Magnusson, Bangalore Muralikrishna, Estyak, Isaacs,
    Aghayev, Zhu & Charapko 2022, "Metastable Failures in the Wild", OSDI '22, pp.73–89.
    Abstract·§1 "Introduction"(pp.73–74), §2 "Metastability in the Wild"(p.74),
    §2.1 "Methodology"(p.74), §2.2 "Summary of Metastable Failures in the Wild"과
    표 1(pp.74–75), §3.6 "Recovery"(p.80), §6.2 "Human Factors"(p.85), §6.3 "Fix to
    Break"(p.85), §6.4 "Mild Metastable Failures"(p.85), §8 "Conclusion"(p.86). 쪽수는
    USENIX 논문집 인쇄 쪽 기준이며 PDF 스냅샷 2–19쪽이 pp.73–89에 해당한다. 표 1은 2단
    조판이라 `pdftotext -layout` 추출본과 대조해 옮겼고, "Services Impacted" 열은 옮기지
    않았다. 원문의 오식 "config rollabck"(GGL4·GGL3 행)은 config rollback으로 읽었다.
[^bronson2021-metastable]: Bronson, Aghayev, Charapko & Zhu 2021, "Metastable Failures in
    Distributed Systems", HotOS '21, pp.221–227. §2 "Metastable Failure Case
    Studies"(p.222). 쪽수는 ACM 게재본 인쇄 쪽 기준이며 PDF 스냅샷 1–7쪽이 pp.221–227에
    해당한다.

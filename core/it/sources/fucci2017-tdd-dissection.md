---
type: article-journal
title: "A Dissection of the Test-Driven Development Process: Does It Really Matter to Test-First or to Test-Last?"
author:
  - { family: "Fucci", given: "Davide" }
  - { family: "Erdogmus", given: "Hakan" }
  - { family: "Turhan", given: "Burak" }
  - { family: "Oivo", given: "Markku" }
  - { family: "Juristo", given: "Natalia" }
issued: "2017"
container-title: "IEEE Transactions on Software Engineering"
volume: "43"
issue: "7"
page: "597-614"
DOI: "10.1109/TSE.2016.2616877"
snapshot: /it/archive/fucci2017-tdd-dissection/
snapshot_sha256: "00947fcd28e80fa7ce825951bd9be094c8f3d9ee77b9e82df265975d6920afae"
accessed: "2026-08-24"
---

# fucci2017-tdd-dissection

**TDD를 하나의 기법으로 두지 않고 네 차원으로 쪼갠 뒤 어느 차원이 결과를 설명하는지를
회귀로 잰 논문.** 답은 **잘게(granularity) 고르게(uniformity) 가는 것이 설명하고, 테스트를
먼저 쓰는 순서(sequencing)는 최종 모형에 남지 않는다**는 것이다.

**이 소스가 이 KB에서 서는 자리는 TDD 논쟁의 중재항이다.** 실무자 옹호론도 실무자 반대론도
측정을 갖고 있지 않은 자리에, 이 논문은 전문 개발자의 IDE 로그에서 뽑은 관측을 놓는다.
다만 **그 관측이 무엇을 말하고 무엇을 말하지 않는지가 이 소스의 가장 자주 오독되는 부분**이라
아래에 따로 적는다.

## 지위 — 심사를 통과한 실증이되 확보본에는 게재 레코드가 없다

- **근거 등급은 `peer-reviewed`다.** IEEE Transactions on Software Engineering 게재
  논문이다.
- **확보본은 UPM 리포지토리의 수용본(accepted manuscript)이고 venue·권·호·쪽수·DOI가
  한 줄도 인쇄돼 있지 않다.** 19쪽 전체에 학회·저널 조판 표면이 없다. 그러므로 위
  frontmatter의 `43(7):597–614, 2017`과 `10.1109/TSE.2016.2616877`은 **확보본 문면이 아니라
  서지 레코드가 근거다.**
  - **그 레코드를 이 KB가 확보한 다른 원문 안에서 확인했다.** 같은 저자군의
    [tosun2018-tdd-unit-tests](tosun2018-tdd-unit-tests.md) 참고문헌 [17]이
    `IEEE Transactions on Software Engineering 43, 7 (July 2017), 597–614`과
    `https://doi.org/10.1109/TSE.2016.2616877`을 인쇄한다(그 확보본 9쪽). **원문 문면으로
    위장하지 않되, 근거가 어디인지는 이 줄이 답한다.**
- **arXiv 1611.05994와 섞지 않는다.** 그쪽은 14쪽 단축 프리프린트이고 확보본은 19쪽이다.
  **다른 문서이므로 절·표 위치를 옮겨 쓸 수 없다.**
- **확보본은 OCR 산물이다.** PDF의 Producer가 `ABBYY FineReader 8.0 Site License Edition`
  이고 생성 시각이 2018-12다. 본문 산문은 깨끗하게 추출되지만 **수식과 표는 추출 텍스트에서
  자리가 뒤섞인다.** 그래서 이 KB가 이 소스에서 인용한 **모든 숫자는 150dpi 렌더 이미지로
  육안 재확인한 것**이고, 확인한 쪽은 10·12·13쪽(Table 5·6·7·8·9·10·11·12)이다.
  - **스냅샷 도구의 판정(`text_based`, 신뢰도 1.00)은 "OCR이 아니다"라는 뜻이 아니다.**
    OCR 품질이 좋으면 그 휴리스틱을 통과한다. 판정과 Producer가 갈리면 Producer를 따른다.

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **표본**: 전문 개발자 39명에게서 나온 **82개 관측(data point)**이다. 관측 하나 = 개발자
  한 명이 과제 하나를 수행한 기록이다(초록 · Table 5 캡션 `n=82`).
  - 원 수집은 99개였고 결측을 제거해 82개가 됐다(과제 1이 27, 과제 2가 25, 과제 3이 30 —
    §4.5).
  - 두 회사에서 워크숍 4회를 돌렸다. 회사 A(핀란드에 본사를 둔 보안 제품 회사)에서 3회,
    회사 B(에스토니아 SME)에서 1회다(§3). 참가는 회사 A 22명·회사 B 17명이다(§4.7).
  - 자바 경력 평균 7.3년(표준편차 4.1, 최소 1, 최대 15)이고, 단위 테스트를 전문가로
    자평한 사람은 없었다(§4.7).
- **설계가 통제 실험이 아니다.** 저자들이 직접 `this study is neither a controlled
  experiment nor a quasi-experiment`라고 적고(§4.2), 실험 맥락 위에 얹은 **관찰 연구
  (observational study)**로 규정한다(§2). 그래서 결과는 인과가 아니라 연관(association)이다.
  **"통제 실험이 TDD를 반증했다"는 요약은 이 소스의 문면이 아니다.**
- **네 차원은 IDE 로그에서 자동 분류한 사이클 통계다**(§4.4, Table 1·2). 도구는 Besouro이고
  사이클 유형 판별 규칙은 Kou et al.의 것을 쓴다.
  - GRA(granularity) = 사이클 길이의 중앙값(분), 범위 [0, 300]
  - UNI(uniformity) = 사이클 길이의 중앙값 절대편차(MAD), 범위 [0, 149]
  - SEQ(sequencing) = 전체 사이클 가운데 test-first 유형의 비율(퍼센트), 범위 [0, 100]
  - REF(refactoring effort) = 리팩터링 사이클의 비율(퍼센트), 범위 [0, 100]
- **결과 변수 둘의 정의가 좁다**(§4.3). QLTY는 **착수한 사용자 스토리에 한정된** 수용 테스트
  단정 통과율이고, PROD는 전체 수용 테스트 단정 통과율을 IDE 개폐 시각 차이(분)로 나눈
  값이다. **usefulness·usability·내부 품질은 재지 않았다**고 저자들이 §6.3에 적는다.
- **저자들이 스스로 적은 한계 둘을 함께 옮긴다**(§6.3·§6.4). ① REF는 구성 타당도 위협이
  있다 — 순수 리팩터링과 다른 활동이 섞인 floss refactoring을 가르지 못한다.
  ② **결과 변수 변동의 85%가 넘는 부분이 설명되지 않은 채 남는다**(`over 85% of the
  variation in the outcome variables was still unaccounted for`).

## 이 논문이 말하지 않는 것 — 부정 조건절

**이 자리가 이 소스에서 가장 자주 뒤집혀 인용되는 대목이다.** 논의 절(§8)이 못을 박는다.

> The absence of sequencing as an influential dimension does not imply that a strictly
> develop-then-test (test-last) strategy should be preferred over a test-first strategy:
> this advice would require a negative (statistically significant) coefficient, which the
> models did not produce.

- 초록의 대응 문면도 "무효"가 아니라 `had no important influence`다.
- 같은 절이 test-first가 이 연구가 재지 않은 자리에서 장기 이득을 줄 수 있다고 명시한다 —
  요구사항 불확실성 해소, 설계 결정의 형식화, 테스트를 더 쓰게 만드는 효과.
- **그러므로 이 소스를 "TDD 무용론의 근거"로 쓰면 논문을 반대로 인용하는 것이다.**

## 이 판이 안고 있는 내부 불일치 둘

**둘 다 원문의 것이고 OCR 잡음이 아니다(육안 재확인).** 인용할 때는 표 쪽을 따른다.

- **§5.2 산문과 Table 7의 상관계수가 다르다.** 산문은 QLTY–GRA를 `ρ = −.25, p-value=.02`로
  적고, Table 7의 같은 칸은 `-.27 (.02)`다.
- **Table 10의 자유도 표기가 모형과 맞지 않는다.** 그 모형의 인자는 셋(GRA·UNI·REF)인데
  `F Statistic 4.14 (df = 2; 78)`로 인쇄돼 있다. 잔차 자유도 78 쪽이 인자 셋과 정합한다.

## 인용 규약

- **수치는 표에서만 가져오고 표 번호와 함께 적는다.** 서론·동기 절의 수치는 인용하지 않는다.
- **이 논문이 옮긴 남의 수치는 이 논문 경유로 쓰지 않는다** — §7 관련 연구가 훑는 체계적
  문헌 고찰 셋(Turhan et al. · Munir et al. · Rafique & Mišić)의 결론은 이 논문 밖의
  값이다.
- **locator는 절 번호와 표 번호다.** 확보본에 인쇄된 쪽 번호가 없어 쪽으로 가리킬 수 없다.

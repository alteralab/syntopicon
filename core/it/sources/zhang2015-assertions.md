---
type: paper-conference
title: "Assertions Are Strongly Correlated with Test Suite Effectiveness"
author:
  - { family: "Zhang", given: "Yucheng" }
  - { family: "Mesbah", given: "Ali" }
issued: "2015"
event-title: "ESEC/FSE 2015"
publisher: "ACM"
page: "214-224"
DOI: "10.1145/2786805.2786858"
ISBN: "978-1-4503-3675-8"
snapshot: /it/archive/zhang2015-assertions/
snapshot_sha256: "829cc8934d803dde4b5bfde7f007d2a413f2312b10ce98cde84dd3f30570dc1d"
accessed: "2026-08-23"
---

# zhang2015-assertions

**테스트 메서드 안을 열어 단정(assertion)이 스위트 효과성을 얼마나 설명하는가**를 자바
오픈소스 다섯 개에서 잰 논문. 답은 **단정 수와 단정 커버리지 둘 다 효과성과 아주 강하게
상관하고, 단정 커버리지를 통제하면 문장 커버리지와 효과성의 상관이 내려앉는다**는 것이다.

**이 소스가 이 KB에서 서는 자리는 커버리지 논쟁의 중재항이다.** 회의 측
(`inozemtseva2014-coverage`)과 옹호 측(`namin2009-size-coverage`·
`gopinath2014-suite-evaluation`)을 둘 다 인용하면서, 그 논쟁이 다투던 스위트 크기의
아래에 단정이라는 변수가 있다고 주장한다.

## 지위 — 심사를 통과한 실증이되 확보본은 저자본이다

- **근거 등급은 `peer-reviewed`다.** 게재 레코드가 1쪽 하단에 인쇄돼 있다 —
  `ESEC/FSE’15, August 30 – September 4, 2015, Bergamo, Italy` ·
  `ACM. 978-1-4503-3675-8/15/08...` · `http://dx.doi.org/10.1145/2786805.2786858`.
- **다만 확보본은 ACM 최종 조판이 아니라 저자본이다.** 같은 자리에 이렇게 인쇄돼 있다 —
  `This is the author’s version of the work. It is posted here for your personal use. Not
  for redistribution. The definitive version was published in the following publication:`
  **게재 레코드와 인쇄 쪽 번호를 함께 실은 저자본이므로**, 학회 논문집의 쪽수
  `214–224`는 확보본 문면(각 쪽 하단 러닝 풋)이 근거다.
- **학회명은 약칭만 인쇄돼 있다.** `ESEC/FSE’15`가 전부이고 정식 명칭 전개는 문면에
  없어 소스 메타도 약칭으로 적는다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 2절이 훑는 선행 연구
  (Frankl·Cai & Lyu·Namin & Andrews·Inozemtseva & Holmes·Schuler & Zeller)의 수치는
  경유 값이라 이 KB는 옮기지 않는다.
- 실험 데이터와 대상 프로그램을 공개했다고 3절(p.216 각주 3)이 적는다. 이 KB는 그
  사이트를 확보하지 않았다.

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **효과성 = PIT 뮤테이션 점수다** (§3.3.1, p.216). 실제 결함으로 재는 것이 실무적으로
  불가능해 뮤테이션으로 대신했다고 직접 적는다. **이 논문의 모든 "effectiveness"는 이
  정의 위에 있다.**
- **동등 뮤턴트를 가정으로 처리했다** — 마스터 스위트가 죽이지 못한 뮤턴트를 전부
  동등으로 간주했다 (§3.3.1, p.216). 회의 측 논문과 같은 처리다.
- **대상**: 자바 오픈소스 다섯 개(JFreeChart · Apache Commons Lang · Urban Airship Java
  Library · lambdaj · Asterisk-Java). 합계 자바 SLOC 329,600 · 테스트 케이스 5,892 ·
  단정 24,701 (Table 1, p.216).
- **도구가 넷이다**: PIT(뮤테이션·기본 연산자) · Clover(문장 커버리지) ·
  JavaSlicer(단정 커버리지용 동적 역방향 슬라이싱) · JavaParser(단정 계수).
  생성 단정 비교에는 Randoop 기본 설정을 썼다 (§3.3, pp.216~218).
- **단정 커버리지(assertion coverage) = checked coverage다** — Schuler & Zeller(ICST 2011)가
  **오라클 품질을 재려고** 제안한 지표를 그대로 가져왔고, 두 낱말을 이 논문 안에서
  호환해 쓴다고 2절(p.215)과 3.3.2절(p.217)이 밝힌다.
- **명시 뮤테이션 점수(explicit mutation score)가 이 논문의 고유 구성물이다** (§3.3.2,
  p.217) — 프로그램 충돌이 아니라 **단정 실패로** 죽은 뮤턴트의 비율이다.
- **상관 통계는 Pearson과 Kendall τ, 그리고 회귀의 조정 R²다.** 단정 종류 비교에는
  One-Way ANOVA와 Tukey HSD를 쓰고, 사전에 Shapiro-Wilk(정규성)와 Levene(등분산)을
  돌려 둘 다 양성이었다고 적는다 (§3.3, pp.216~218).
- **단정 종류(RQ3)는 JFreeChart 하나에서만 쟀다** — 그 프로젝트의 단정 9,177개다
  (§4.3, p.221). **수치를 인용할 때 이 분모를 함께 적는다.**

## 이 논문이 스스로 그은 경계

- **내부 타당도** (§5.5, p.223): 외부 도구(PIT·Clover·JavaSlicer)가 옳게 동작한다고
  가정했다. 동등 뮤턴트 근사가 그 수를 과대평가할 수 있으나 상관에는 영향이 없다고
  적는다. PIT가 뮤턴트를 잡은 **첫 단정에서 실행을 멈추므로** 어떤 단정들이 함께
  실패했을지는 알 수 없다.
- **외부 타당도** (§5.5, p.223): 자바·JUnit4 한정이고 다른 언어·프레임워크로 넘어가지
  않을 수 있다. 단정 종류 결과는 JFreeChart 하나에서 나왔다. 생성기는 Randoop 하나뿐이고
  다른 생성 전략이면 결과가 달랐을 수 있다고 적는다. 단정의 내용 종류와 메서드 종류가
  서로 얽혀 있어(boolean ↔ `assertTrue/False`) 어느 쪽 효과인지 가를 수 없다는 것도
  같은 자리에 있다.
- **뮤테이션 점수가 실결함을 대신하는가는 이 논문이 재지 않는다.** 3.3.1절(p.216)이
  반론이 가능함을 인정하고 선행 연구 넷(Andrews 2005·Andrews 2006·Daran &
  Thévenod-Fosse 1996·Just 2014)에 근거를 넘긴다. **타당도 위협 절에는 이 항목이 없다.**
- **역방향 통제가 없다.** 단정 커버리지를 통제하고 문장 커버리지를 본 실험은 있으나,
  문장 커버리지를 통제하고 단정 커버리지를 본 실험은 이 논문에 없다.

## 반입 범위

이 런은 확보본 11쪽(인쇄 쪽 214~224) 전부를 읽었다. 페이지로 옮긴 것은 초록, 2절의
checked coverage 계보, 3절 실험 설계 전부(Table 1·2·3), 4절 결과(Table 4·5·6·7·8과
Figure 3·4의 R² 범위, Finding 1~8), 5절 논의(5.1~5.4)와 5.5절 타당도 위협, 6절 결론이다.

옮기지 않은 것: 1절 서론과 2절 선행 연구가 경유해 전하는 제3자 수치. Figure 1·2·5의
산점도·상자그림은 이미지라 축 이름과 본문이 적은 값만 옮겼다. 7절 참고문헌은 필요한
항목만 각주에 적었다.

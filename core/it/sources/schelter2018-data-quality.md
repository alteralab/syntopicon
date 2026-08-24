---
type: article-journal
title: "Automating Large-Scale Data Quality Verification"
author:
  - { family: "Schelter", given: "Sebastian" }
  - { family: "Lange", given: "Dustin" }
  - { family: "Schmidt", given: "Philipp" }
  - { family: "Celikel", given: "Meltem" }
  - { family: "Biessmann", given: "Felix" }
  - { family: "Grafberger", given: "Andreas" }
issued: "2018"
container-title: "Proceedings of the VLDB Endowment"
volume: "11"
issue: "12"
page: "1781-1794"
DOI: "10.14778/3229863.3229867"
ISSN: "2150-8097"
snapshot: /it/archive/schelter2018-data-quality/
snapshot_sha256: "48292109cadd53a18093a24c397f845d73ea143a597f5fe80ea761bf795009bc"
accessed: "2026-08-25"
---

# schelter2018-data-quality

**데이터 품질 검사를 코드로 선언하면 그것이 무엇으로 환원되어 어떻게 대규모로 실행되는가**를
아마존의 프로덕션 시스템으로 답한 논문. 답은 **선언한 제약(constraint)을 데이터에 대한
메트릭(metric) 계산으로 번역해 Apache Spark의 집계 질의 한 번으로 몰아 돌리고, 데이터가
자라면 상태(state)를 들고 증분으로 다시 재며, 그 메트릭의 시계열에 이상 탐지를 건다**는
것이다.

**이 소스가 이 KB에서 서는 자리는 데이터 검증 축의 "제약 선언 층"이다.** 규칙을 어느
자리에서 강제할지(감사 단계냐 저장소 위임이냐)를 다루는 페이지들과 달리, 이 논문은
**규칙을 어떤 언어로 적고 그 언어가 무엇으로 컴파일되는가**를 다룬다.

## 지위 한정 — "분야 원전"이 아니라 프로덕션 선언적 데이터 검증 시스템의 원전

- **근거 등급은 `peer-reviewed`다.** 게재 레코드가 1쪽에 인쇄돼 있다 — `PVLDB, 11 (12):
  1781-1794, 2018` · `Proceedings of the VLDB Endowment, Vol. 11, No. 12` ·
  `Copyright 2018 VLDB Endowment 2150-8097/18/8` · `DOI: https://doi.org/10.14778/3229863.3229867`.
  **권·호·쪽·DOI가 전부 문면에 있다** — 리포지토리 레코드에 기대지 않는다. 이 KB의
  locator는 인쇄 쪽 번호(1781~1794)와 절·표·그림·리스팅 번호다.
- **선언적 데이터 품질 검증이라는 발상 자체는 이 논문의 것이 아니다.** 7절(관련 연구,
  p.1792)이 스스로 그렇게 적는다 — `The idea to allow declarative definitions of data
  quality standards is well-established.` 데이터 클리닝 계보를 자기 앞에 세우는 것도
  같은 절의 첫 문장이다 — `Data cleaning has been an active research area for decades,
  see recent surveys [1, 10, 38] for an overview.` 그러므로 이 소스를 **"데이터 품질
  검증 분야의 원전"으로 쓰지 않는다.** 이 논문이 자기 기여로 주장하는 것은 1절(p.1782)의
  네 불릿이고, 그 범위는 **API·실행·ML 활용·평가**다.
- **"프로덕션 시스템"의 격은 자기 배포 보고다.** 6절 `LEARNINGS`(pp.1791~1792)는 사용자
  피드백의 서술이고 **대조군도 수치도 없다.** 검증을 켠 팀과 끄고 돌린 팀의 비교는 이
  논문에 없다. 반면 5절의 실험 수치는 저자들이 직접 잰 값이라 인용 가능하다 — **둘을
  같은 격으로 읽지 않는다.**
- **논문 문면에 `Deequ`라는 이름은 없다.** 확보본 전문을 문자열 검색해 0건이다(대소문자
  무시). 논문은 시종 `our system`·`our library`로만 부른다. 이 KB는 소스를 논문 제목으로
  적고, `Deequ`는 이 논문의 시스템이 뒤에 얻은 이름으로 취급한다 — **그 명명의 근거는
  이 확보본에 없다.**

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **주 데이터셋**: 내부 상품 카탈로그의 표본으로 **약 1억 2천만 레코드**, 레코드마다 수백
  속성, **parquet 형식으로 약 50GB**다. 증가하는 append-only 데이터셋을 흉내 내려고 이
  데이터를 **약 1200만 레코드짜리 델타 10개**로 무작위 분할했다 (§5 서두, p.1789).
- **클러스터**: Spark 실험은 **Elastic MapReduce의 워커 5대(c3.4xlarge), Apache Spark
  2.0.2, HDFS 2.7.3**이다 (§5 각주, p.1789). **예측 가능성 실험만 단일 c4.8xlarge
  인스턴스**에서 돌렸다 (§5.1, p.1789). 성능·확장성 수치는 이 설정과 떼어 인용하지
  않는다.
- **외부 데이터셋 둘**: 2015년 5월 reddit 댓글(Kaggle 배포본)과 공개 트위터 표본 스트림에서
  뽑은 **트위터 사용자 5,180명**이다 (§5 서두, p.1789).
- **제약 제안 실험의 분모**: reddit는 **5만 레코드 표본**이고, 두 데이터셋 모두 **레코드의
  10%로 제약을 제안하고 나머지 90%에서 커버리지(coverage)를 잰다** (§5.3 및 표 3 캡션,
  pp.1790~1791). 표 3의 `coverage` 열은 그 90%에 대한 비율이고, `classifier score` 열은
  전혀 다른 축(열 이름으로 유일성을 예측하는 분류기의 확률)이다 — **두 열을 같은 분모로
  읽지 않는다.**
- **1절·2절의 수치는 없다.** 이 논문은 서론에 정량 주장을 싣지 않아 인용 금지 규칙에
  걸리는 자리가 없다.

## 이 논문이 스스로 그은 경계

- **append-only만 다룬다** — `Note that we restrict ourselves to append-only cases where
  a dataset at time t is simply the union of all previous deltas` (§3.2, p.1785). 갱신·
  삭제가 있는 데이터셋의 증분 계산은 이 논문 밖이다.
- **제약 제안은 사람이 고르는 절차다** — `we see constraint suggestion as a
  'human-in-the-loop' process with a low computational budget and therefore rely on the
  end user to select from and validate our suggestions which might not necessarily hold
  for future data` (§3.3, p.1786).
- **데이터 수리(repair)를 하지 않는다** — AJAX와 대비하며 `we do not support the automatic
  execution of data repair methods`라고 적는다 (§7, p.1792).
- **이상 탐지 알고리즘을 규정하지 않는다** — `We pose no restriction on the anomaly
  detection algorithm to apply` (§3.4, p.1787). 기본 제공은 임계값 검사와 `OnlineNormal`
  정도이고, 계절성·간헐성 시계열은 **향후 과제**로 남긴다 (§8, p.1792).
- **증분이 항상 이기지 않는다** — 고유 값만 든 열에서는 증분 쪽이 **언제나 더 느리다**고
  스스로 적는다 (§5.2, p.1790).

## 이 KB의 인접 소스와의 관계 — 인용 방향이 한쪽이다

- **이 논문은 `breck2019-data-validation`을 인용하지 않는다**(그 논문이 1년 뒤에 나왔다).
  대신 같은 구글 팀의 다른 글을 인용한다 — 참고문헌 [9] `E. Breck, N. Polyzotis, S. Roy,
  S. E. Whang, M. Zinkevich. Data Infrastructure for Machine Learning. SysML, 2018`과
  [5] TFX(KDD 2017), [8] ML Test Score(Big Data 2017)이며, 7절이 `modern machine learning
  platforms begin to have explicit data validation components [7, 5, 9]`라고 묶어 적는다
  (§7, p.1792).
- **반대 방향은 실재한다** — `breck2019-data-validation`의 7절이 이 논문을
  `Schelter et al., 2018`로 인용하며 자기 설계와 정면으로 대비한다. **양쪽 페이지에 그
  대비를 적는다.**
- 이 논문이 인용하는 제3자 수치는 이 KB로 옮기지 않는다. 7절이 훑는 AJAX·HoloClean·
  ActiveClean·BoostClean·denial constraints는 **계보를 밝히는 용도로만** 쓴다.

## 반입 범위

이 런은 확보본 14쪽(인쇄 pp.1781~1794) 전부를 읽었다. 페이지로 옮긴 것은 1절(기여
네 항목), 2절(품질 차원 셋), 3.1절(선언 API와 제약→메트릭 번역, 표 1·표 2, 리스팅 1·2),
3.2절(증분 계산의 계산 모델과 재정식화), 3.3절(제약 제안 휴리스틱과 이름 학습),
3.4절(이상 탐지), 4절(구현·아키텍처·최적화), 5절(실험 넷), 6절(교훈), 7절(관련 연구의
계보 주장)이다.

옮기지 않은 것: 리스팅 3의 `IncrementalAnalyzer`·`StateProvider` 인터페이스 전문(산문
요지만 옮겼다), 그림 3의 엔트로피 증분 갱신 도해의 셀 값, 4.2절 제약 제안 분류기의
하이퍼파라미터 세부, 참고문헌 50건의 서지.

**추출 도구 주의**: `pdftotext`(-layout 포함)가 **위첨자와 수학 기호를 조용히 훼손한다.**
실측 둘 — 4.2절의 `10⁸ dimensional feature vectors`가 `108 dimensional`로 나오고(150dpi
렌더로 재대조해 `10`의 위첨자 `8`을 확인), 3.1절 Completeness 정의의 `≠`가 `6=`로
나온다. **수식·기호·위첨자가 든 자리는 렌더 이미지로 재대조했다.** 2단 조판이라 raw
추출은 절 순서도 뒤섞는다 — 실제 절 순서는 6 `LEARNINGS` → 7 `RELATED WORK` →
8 `CONCLUSION`이고, 이것도 `-layout` 추출로 확인했다.

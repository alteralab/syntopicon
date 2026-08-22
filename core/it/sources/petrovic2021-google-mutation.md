---
type: article-journal
title: "Practical Mutation Testing at Scale: A View from Google"
author:
  - { family: "Petrović", given: "Goran" }
  - { family: "Ivanković", given: "Marko" }
  - { family: "Fraser", given: "Gordon" }
  - { family: "Just", given: "René" }
issued: "2021"
container-title: "IEEE Transactions on Software Engineering"
publisher: "IEEE"
DOI: "10.1109/TSE.2021.3107634"
snapshot: /it/archive/petrovic2021-google-mutation/
snapshot_sha256: "e51fe34a9baf0742b28951ba42d0074f71b57a69785a15feb23977525a00d96c"
accessed: "2026-08-23"
---

# petrovic2021-google-mutation

**뮤테이션 테스팅(mutation testing)을 20억 줄 규모의 단일 코드베이스에서 실제로
운영한 기록.** 전통적 방식이 그 규모에서 성립하지 않는다는 것을 확인한 뒤, 변경분
한정·한 줄 한 뮤턴트·arid 노드 억제·맥락 기반 연산자 선택으로 다시 설계한 결과와
그 수치를 담는다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 게이트의 반대 근거다.** 산업 최대 규모의
채택 사례이면서, 그 사례가 **절대 뮤테이션 점수를 버리고** 코드 리뷰 시점의 개별
제안으로 갈아탄 기록이기 때문이다.

## 지위 — 심사를 통과한 실증이되 확보본은 early access 판이다

- **근거 등급은 `peer-reviewed`다.** 확보본 1쪽 러닝 헤더가
  `IEEE TRANSACTIONS ON SOFTWARE ENGINEERING`이고, 각 쪽 상단 띠에
  `This article has been accepted for publication in a future issue of this journal, but
  has not been fully edited. Content may change prior to final publication. Citation
  information: DOI 10.1109/TSE.2021.3107634, IEEE Transactions on Software Engineering`가
  인쇄돼 있다. 1쪽 각주에 `Manuscript received June 13, 2020; revised February 7, 2021.`이
  있다.
- **게재처는 IEEE TSE다.** 이 KB의 앞선 판정 문서가 적었던 `ICSE 2021 SEIP`는 **오류**다.
  같은 저자군의 ICSE 논문 둘은 이 논문 안에 **참고문헌으로 따로 실려 있다** —
  [12] `State of Mutation Testing at Google`(ICSE 2017 SEIP)와
  [20] `Does mutation testing improve testing practices?`(ICSE 2021). **셋은 별개
  논문이다.**
- **권·호·쪽수를 적지 않는다.** early access 판에는 그 셋이 인쇄되지 않고, 각 쪽 번호는
  1~13의 임시 번호다. 최종 인쇄판의 권·호·쪽수를 적으려면 DOI 레코드가 근거가 되어야
  하는데 이 런은 그 레코드를 확보하지 않았다. **그래서 이 KB의 locator는 절 번호와
  표·그림 번호이고, 쪽은 확보본 PDF 쪽(1~13)이다.**
- **`issued: "2021"`의 근거는 문면이다** — 개정 접수일과 DOI에 박힌 연도가 2021이다.
  최종 인쇄 호의 연도(2022)는 문면 근거가 없어 적지 않는다.

## 두 판본을 함께 보존했다

아카이브에 파일이 셋이다.

- `mutation-pair--petrovic-google-tse-accepted.pdf` — **정본.** IEEE TSE 수용판
  (early access), 13쪽 2단 조판.
- `mutation-pair--petrovic-google-tse.pdf` — **대조용.** arXiv:2102.11378 v2, 22쪽
  프리프린트 조판. 1쪽에 `submitted to the IEEE`가 인쇄돼 있다.
- `mutation-pair--petrovic-google-tse-accepted.README.txt` — 확보 경위 메모.

**두 판의 수치가 어긋나면 수용판을 따른다.** 이 런이 대조한 범위(§5의 데이터셋 규모,
Table 3~5, RQ1~RQ4 요약)에서는 수치가 같았고 **용어만 다르다** — arXiv 판이
`surfaced`를 쓰는 자리에서 수용판은 `reported`를 쓴다. 이 KB는 수용판 표기를 따른다.

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **표본은 코드 리뷰를 거친 변경 목록(changelist) 776,740건이고, 그 위에서 생성된
  뮤턴트가 16,935,148개다** (§5.1). 그중 개발자에게 보고된 것이 2,110,489개이고,
  명시적 피드백이 붙은 것이 66,798개다. **생산성 수치의 분모는 마지막 값이다.**
- **뮤턴트 억제 비교는 별도 표본이다** (§5.2) — 변경 목록 5,000건을 무작위로 뽑아
  전통적 뮤테이션이 몇 개를 만드는지 따로 돌렸다.
- **맥락 데이터셋은 부분집합이다** (§5.1) — 4,068,241개이고 언어는 상위 넷
  (C++·자바·Go·파이썬)뿐이다.
- **저자들이 스스로 적는 외부 타당도 경계** (§5.1): 이 데이터셋은 Google의 코드 스타일과
  리뷰 관행에 특수할 수 있다. 다만 그 스타일 가이드가 널리 쓰이고 현대적 코드 리뷰가
  업계 전반의 관행이라는 점을 든다.
- **생산성은 개발자 클릭이다** (§2.4·§5.4) — 코드 리뷰 도구의 `Please fix`와
  `Not useful` 두 링크가 원자료이고, 측정 도구가 아니라 사람의 판단이다.

## 반입 범위

이 런은 수용판 전 13쪽(초록·§1~§7·참고문헌)을 읽었다. 페이지로 옮긴 것은 §1의 규모
전제와 세 착상, §2의 파이프라인·연산자·보고 방식, §3의 arid 노드 정의와 범주,
§4의 무작위·표적 선택, §5.1의 데이터셋 규모, §5.2~§5.5의 RQ 결과와 Table 3~5,
그리고 §7 결론이다.

옮기지 않은 것: §4.3~§4.5의 피벗 해싱·MinHash 수식은 구현 세부라 담지 않았고,
Figure 2(프로젝트별 줄 커버리지 분포)·Figure 5(AST 도해)는 도형이라 수치를 읽지
않았다. §6 관련 연구의 제3자 수치는 경유 값이라 옮기지 않았다.

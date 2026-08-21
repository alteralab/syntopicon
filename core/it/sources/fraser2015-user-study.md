---
type: article-journal
title: "Does Automated Unit Test Generation Really Help Software Testers? A Controlled Empirical Study"
author:
  - { family: "Fraser", given: "Gordon" }
  - { family: "Staats", given: "Matt" }
  - { family: "McMinn", given: "Phil" }
  - { family: "Arcuri", given: "Andrea" }
  - { family: "Padberg", given: "Frank" }
issued: "2015"
container-title: "ACM Transactions on Software Engineering and Methodology"
DOI: "10.1145/2699688"
URL: "https://www.evosuite.org/wp-content/papercite-data/pdf/tosem_userstudy.pdf"
snapshot: /it/archive/fraser2015-user-study/
snapshot_sha256: "d0bc750395e246ff197c4c13dddc95c502bfb34112603d1a8396a9e16333873d"
accessed: "2026-08-21"
---

# fraser2015-user-study

**자동 생성 단위 테스트가 실제 테스터에게 도움이 되는가**를 사람 피험자 통제실험으로
잰 논문. EvoSuite를 도구로 쓴 두 실험(초기 49명 + 재현 48명 = 97명, 데이터점 145개)이고,
잰 것은 커버리지·발견 결함 수·원본에서 실패하는 테스트 수·뮤테이션 점수 넷이다.

**이 소스가 이 KB에서 서는 자리는 "생성된 단언은 관측된 동작을 적은 것"이라는 기제와,
그 기제 아래서 커버리지가 오르는데 결함 발견은 오르지 않았다는 실측이다.** 논문 자신의
표현은 §2.1에 있다 — *"As EVOSUITE assumes no specification, these assertions reflect
the observed behaviour rather than the intended behaviour."*

## 판본 — 저자 수용본이다

확보본은 **TOSEM 최종 인쇄판이 아니라 저자 수용본(accepted manuscript)이다.** 판정 근거는
문면이다: 러닝 푸터가 `ACM Transactions on Software Engineering and Methodology, Vol. V,
No. N, Article A, Pub. date: January YYYY.`라는 자리표시자로 49쪽 전부에 인쇄돼 있고,
1쪽 저작권 줄의 DOI도 `10.1145/0000000.0000000`이다. 쪽 번호는 `A:2`·`A:3` 꼴의
아티클 상대 쪽이다.

- 그래서 **이 KB는 이 소스의 권·호·쪽수를 인용 locator로 쓰지 않는다.** locator는
  절 번호(§3.1 같은 것)와 표·그림 번호, 그리고 확보본의 아티클 상대 쪽(`A:14`)으로만
  적는다.
- `issued`·`DOI`·`container-title` 중 문면에서 확인되는 것은 container-title뿐이다.
  연도 2015와 DOI `10.1145/2699688`은 **확보 단계 대장이 적은 서지 레코드가 근거이고,
  이 반입 런은 그 레코드를 직접 열지 않았다.** 권·호·쪽수를 페이지에 적어야 할 일이
  생기면 그 DOI 레코드를 근거로 삼고 그 사실을 함께 적는다.

## 이 논문의 계보 — ISSTA 2013 단축판이 따로 있다

§8이 스스로 밝힌다: 이 글은 선행 발표(Fraser et al., ISSTA 2013, *Does Automated
White-Box Test Generation Really Help Software Testers?*)의 확장이고, 확장의 몸통은
§4의 재현 실험(피험자 48명 추가·`DocType` 설정 오류 교정·`ArrayIntList` 추가)이다.
**두 판을 섞어 인용하지 않는다** — 이 KB가 쓰는 것은 확장판이고, 그래서 두 실험의
결론이 어긋나는 자리(§3.3 대 §4.3)를 함께 적는 것이 의무가 된다.

## 대상과 표본

- 초기 실험: 피험자 49명(그중 3명 데이터 폐기), 클래스 3종 — Commons CLI `Option`,
  Math4J `Rational`, XOM `DocType` (표 I).
- 재현 실험: 피험자 48명, 클래스 4종 — 위 셋에 Commons Primitives `ArrayIntList`
  추가 (표 II). 재현 실험은 한 사람이 수동·도구 두 번을 수행해 데이터점 96개를 만든다.
- 결함은 손으로 심은 것이 아니라 MAJOR로 만든 뮤턴트 5개를 클래스마다 주입한 것이다
  (§2.2.1).
- **§2.2.2의 산문에 오식이 하나 있다.** 재현 실험 대상을 서술하면서 "Commons Math
  *Fraction*"을 재사용했다고 적는데, 같은 절의 표 II와 §4의 결과 표 IV는 전부
  `Rational`이다. §2.2.1이 *Fraction*을 난이도 때문에 `Rational`로 교체했다고
  적었으므로 표 쪽이 맞다. 이 KB는 표를 따른다.

## 근거 등급

`peer-reviewed`. 다만 등급이 여는 것은 **이 논문이 스스로 잰 값**뿐이다 — §8이 인용하는
제3자 실측(Staats et al.의 불변식 오분류율, Ramler et al. 등)은 이 소스를 경유해
인용하지 않는다.

**서론(§1)의 수치는 인용하지 않는다.** §1은 Sjoberg의 1.9%, Buse의 3,110편 같은
동기 수치를 담고 있고 전부 남의 것이다. 이 KB가 쓰는 수치는 §3·§4의 결과 절과
표 III·IV·V에서 온 것뿐이다.

## 텍스트 레이어

`snapshot.py` 판정은 `text_based`(신뢰도 1.00, OCR 필요 0/49쪽)다. 다만 결과 표
III·IV는 다단 수치 표라 기계 추출이 열을 섞는다 — 표에서 값을 읽을 때는 본문 산문이
같은 값을 진술하는 자리를 우선한다. Fig.2·4·5의 상자 그림은 점마다 값이 인쇄돼 있지
않아 본문이 진술한 평균·중앙값만 옮긴다.

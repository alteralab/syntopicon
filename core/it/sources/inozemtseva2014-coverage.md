---
type: paper-conference
title: "Coverage Is Not Strongly Correlated with Test Suite Effectiveness"
author:
  - { family: "Inozemtseva", given: "Laura" }
  - { family: "Holmes", given: "Reid" }
issued: "2014"
event-title: "ICSE 2014: 36th International Conference on Software Engineering"
publisher: "ACM"
snapshot: /it/archive/inozemtseva2014-coverage/
snapshot_sha256: "827160b2d313fd1806037192c69adb4d4fdefec98f817ac701b968a17ff82e97"
accessed: "2026-08-23"
---

# inozemtseva2014-coverage

**커버리지가 스위트의 결함 검출 효과성을 예측하는가**를 큰 자바 프로그램 다섯 개에서
잰 논문. 스위트 크기를 통제했을 때 상관이 어떻게 변하는지가 이 논문의 물음이고,
결론은 **크기를 통제하면 상관이 낮음에서 중간으로 떨어진다**이다.

**이 소스가 이 KB에서 서는 자리는 커버리지 논쟁의 회의 측 극이다.** 같은 물음에 반대
답을 내는 옹호 측(`namin2009-size-coverage` · `gopinath2014-suite-evaluation`)과
`contradicts`로 묶인다.

## 지위 — 게재본이고 심사를 통과한 실증이다

- **근거 등급은 `peer-reviewed`다.** 1쪽 저작권 상자가 게재를 문면으로 확인해 준다 —
  `ICSE ’14, May 31–June 7, 2014, Hyderabad, India` ·
  `Copyright 14 ACM 978-1-4503-2756-5/14/05 ...$15.00.`
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 2절 Table 1이 요약하는 열두 편의
  선행 연구 수치는 이 논문이 경유해 전하는 제3자 값이므로 이 KB는 그 값을 옮기지 않는다.

## 판과 서지 — 문면으로 확인한 것

- **쪽 번호가 인쇄돼 있지 않다.** 확보본 11쪽 어디에도 러닝 풋이 없다. 그래서 이 KB의
  locator는 **확보본 PDF 쪽(1~11)**이고, 권·호·쪽수를 적을 근거는 문면에 없다.
- **학회명·연도·개최지는 1쪽 저작권 상자에 인쇄돼 있다**(위 인용). 조판도 ACM 이단
  게재 조판이다.
- DOI 줄은 문면에 없다.
- **보조 자료가 외부 URL에 있다** — 1쪽 각주 1과 4.1절 각주 8이
  `http://linozemtseva.com/research/2014/icse/coverage/`를 가리킨다. 비정규화 효과성
  그림과 전체 데이터셋이 그쪽에 있다고 적혀 있다. **이 KB는 그 외부 자료를 확보하지
  않았으므로 거기 있다고만 적고 값을 옮기지 않는다.**

## 무엇을 어떻게 쟀는가 — 인용할 때 함께 적어야 하는 조건

- **대상**: 자바 오픈소스 다섯 개 — Apache POI · Closure Compiler · HSQLDB · JFreeChart ·
  Joda Time. 총 자바 SLOC은 80,462(Joda Time)에서 724,089(Closure)까지다 (Table 2, p.3).
- **스위트**: 각 프로그램의 마스터 스위트에서 테스트 메서드를 비복원 무작위로 뽑아
  크기 3·10·30·100 식으로 늘려 가며 각 크기마다 1,000개씩 만들었고 **다섯 시스템 합계
  31,000개**다 (§3.4, p.3).
- **커버리지**: CodeCover로 문장·결정·수정 조건 커버리지 셋 (§3.5, pp.3~4).
- **효과성은 뮤테이션 점수다.** PIT가 만든 뮤턴트를 죽인 비율이고, 원시(raw)와
  정규화(normalized) 둘을 쓴다 (§3.3·§3.6, pp.2~4). **실제 결함이 아니다** — 7절이
  실결함으로 확인하는 것을 다음 과제로 적는다.
- **동등 뮤턴트 처리**: 마스터 스위트가 못 죽인 뮤턴트를 동등으로 간주했고, 그 비율이
  프로젝트마다 0.4%에서 35%까지다 (Table 2 마지막 행 · §6.1). 저자들이 이것을 구성
  타당도 위협으로 직접 적는다.
- **상관 계수**: Kendall τ. 4.1절의 회귀만 r²를 쓴다.

## 이 논문이 스스로 그은 경계

- 6.3절이 외부 타당도 위협 여섯을 적는다. 그중 둘이 이 KB에서 무겁다 — **아주 높은
  커버리지 구간에서만 나타나는 관계를 놓쳤을 수 있다**는 것(선행 연구 셋이 그런 관계를
  보고했다)과, **대상이 다섯 개뿐이고 전부 오픈소스**라는 것이다.
- 6.2절이 **인과 방향을 주장할 수 없다**고 명시한다.
- **결론이 "커버리지를 쓰지 마라"가 아니다** (5절·8절). 저자들이 남기는 것은
  `coverage measures are useful for identifying under-tested parts of a program`이고,
  부정하는 것은 **고정 커버리지 값을 품질 목표로 쓰는 것**이다.

## 반입 범위

이 런은 확보본 1~11쪽 전부를 읽었다. 페이지로 옮긴 것은 초록과 1절의 연구 질문,
3절 방법(대상·뮤턴트·스위트 생성·커버리지·효과성 정의), 4절 결과 전부(Table 3·4·5와
세 Answer 상자), 5절 논의, 6절 타당도 위협, 8절 결론이다.

옮기지 않은 것: 2절 Table 1의 선행 연구 열두 편 요약과 그 안의 수치는 이 논문이 경유해
전하는 제3자 값이라 옮기지 않았다. Figure 1의 동등 뮤턴트 예제 코드와 Figure 4의 가상
그래프는 설명용 도해라 옮기지 않았다.

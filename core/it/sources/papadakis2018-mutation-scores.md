---
type: paper-conference
title: "Are Mutation Scores Correlated with Real Fault Detection? A Large Scale Empirical Study on the Relationship Between Mutants and Real Faults"
author:
  - { family: "Papadakis", given: "Mike" }
  - { family: "Shin", given: "Donghwan" }
  - { family: "Yoo", given: "Shin" }
  - { family: "Bae", given: "Doo-Hwan" }
issued: "2018"
event-title: "ICSE 2018: 40th International Conference on Software Engineering"
publisher: "ACM"
DOI: "10.1145/3180155.3180183"
ISBN: "9781450356381"
snapshot: /it/archive/papadakis2018-mutation-scores/
snapshot_sha256: "fc9ae289928b1a3adf9432ad7a9b2328ecaee2d61c91843849c8679355de0457"
accessed: "2026-08-23"
---

# papadakis2018-mutation-scores

**뮤테이션 점수와 실제 결함 검출의 상관이 스위트 크기를 통제하고도 남는가**를 실제 결함
벤치마크 두 개(C의 CoREBench, 자바의 Defects4J)에서 잰 논문. 답은 **크기를 통제하면
상관이 무너진다**이고, 그럼에도 최상위 점수 구간에서는 검출이 유의하게 오른다는 결과가
같이 붙는다.

**이 소스가 이 KB에서 서는 자리는 뮤테이션 점수판 크기 교란 실증이다.** 커버리지 쪽의
같은 논증(`inozemtseva2014-coverage`)과 짝을 이루고,
[뮤테이션 타당성 여섯 편](../concepts/mutation-validity-evidence.md)이 담는다.

## 지위 — 게재본이고 심사를 통과한 실증이다

- **근거 등급은 `peer-reviewed`다.** 확보본 1쪽의 ACM Reference format과 각 쪽 머리띠가
  게재를 문면으로 확인해 준다 — `ICSE ’18, May 27-June 3, 2018, Gothenburg, Sweden` ·
  `ACM ISBN 978-1-4503-5638-1/18/05` · `https://doi.org/10.1145/3180155.3180183`.
- **쪽수는 문면에 인쇄돼 있지 않다.** 1쪽 ACM Reference format이 `12 pages`라고만 적는다.
  locator는 절 번호와 표·그림 번호다.
- **이 등급이 여는 것은 이 논문이 스스로 잰 값뿐이다.** 2절 Table 1이 요약하는 선행
  연구 열 편의 결론과 수치는 옮기지 않는다.

## 이 KB가 옮긴 것과 옮기지 않은 것

- 옮긴 것: 3.1~3.2절의 대상과 결함 수, 4.2절 회귀, 4.3절 상관의 통제 전후 범위,
  4.4절 검출 개선폭과 개선이 유의하지 않은 결함 비율, 5.1절 Ochiai 행동 유사도,
  7절 결론.
- 옮기지 않은 것: Table 1(제3자 값), Figure 1·2·3·4·5·6의 박스플롯 세부, 6절 타당성
  위협의 재현 수치.

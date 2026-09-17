---
type: book
title: "Software Architecture: The Hard Parts — Modern Trade-Off Analyses for Distributed Architectures"
author:
  - family: "Ford"
    given: "Neal"
  - family: "Richards"
    given: "Mark"
  - family: "Sadalage"
    given: "Pramod"
  - family: "Dehghani"
    given: "Zhamak"
issued: "2021"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-492-08689-5"
snapshot: /it/archive/ford2021-hard-parts/
snapshot_sha256: "7b72941af451bb42e5b5894de50bdd4a0d0fb4469d4726522b9602c42168b153"
accessed: "2026-09-17"
---

# ford2021-hard-parts

닐 포드·마크 리처즈·프라모드 사달게이·자마크 데가니의 소프트웨어 아키텍처 The Hard Parts(2021-10).
"최선의 실천"이 없는 자리에서 트레이드오프를 분석하는 법을 다루며, 2부 15장 + 부록 3: 1장 서론(ADR·
피트니스 함수·Sysops Squad 사가), I부 떼어 내기(결합 식별·모듈성·분해·컴포넌트 기반 분해 패턴·운영
데이터 분리·서비스 세분도), II부 다시 합치기(재사용 패턴·데이터 소유권과 분산 트랜잭션·분산 데이터
접근·분산 워크플로·트랜잭셔널 사가·계약·분석 데이터·자기만의 트레이드오프 분석).

- 이 KB에서 맡는 자리는 **분산 아키텍처 트레이드오프의 종합서(L2)이되, 9~12장(데이터 소유권·분산
  트랜잭션·사가 여덟 패턴)은 서비스 쪽 정합성의 L1급 정본 역할**이다. 2026-09 실측에서 사가는 khononov2021·
  newman2021을 통해 들어왔고(정의·두 소스의 어휘 분열), 이 책이 그 8칸 공간(통신×정합성×조정)의 정본이다 —
  [ford2022-evolutionary](ford2022-evolutionary.md) 5장의 아키텍처 퀀텀 3차원 동적 결합이 이 책을 가리킨다.
  결합·모듈성 정의(2~3장)는 KB의 두터운 정성 어휘(beck2023·percival2020·ousterhout2021)와 커네이선스
  (ford2022) 위에 서고, 계약(13장)은 robinson2006이 원전이다.
- 층: 1~3장 L1(정의) · 4~8장 분해·재사용 패턴 L2 · 9~12장 L1 · 13 L2 · 14 분석 데이터 L2(dehghani2022 교차) ·
  15 L2. 선행서 *Fundamentals of Software Architecture*(1판 2020, 2판 2025)는 이 KB에 없다 — 1장이 그 책을
  전제하므로 각주에 "이 책이 대는 출처"로만 적는다.
- 원서만 반입했다. 한국어판 『소프트웨어 아키텍처 The Hard Parts』(한빛미디어 2022-10-01, 이일웅 역)는
  존재하나 실물 미확보라 역어 참조원으로 쓰지 않았다.
- 아카이브 스냅샷은 출판사 PDF(12MB 판 — 16MB 판은 전송 중 3회 절단)이고 **인쇄판 쪽 = PDF 쪽 − 18**
  (실측). locator는 인쇄판 쪽으로 적는다. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/ford2021-hard-parts/_progress.yaml`이다.

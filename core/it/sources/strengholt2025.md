---
type: book
title: "Building Medallion Architectures: Designing with Delta Lake and Spark"
author:
  - family: "Strengholt"
    given: "Piethein"
issued: "2025"
edition: "1"
publisher: "O'Reilly Media"
ISBN: "978-1-098-17883-3"
snapshot: /it/archive/strengholt2025/
snapshot_sha256: "c47b329b94fad20b8fcbbfc7e633b023d3a95c775b21581d95f2d1c402445c1e"
accessed: "2026-09-23"
---

# strengholt2025

피트하인 스트렝홀트의 메달리온 아키텍처 설계서(초판 첫 릴리스 2025-03-28, 추천사 사이먼 화이틀리 —
본인 서명 기준 Advancing Analytics의 CTO 겸 창업자). 4부 13장 — I부 메달리온 틀 이해(1장 데이터 아키텍처의 진화, 2장 기초
다지기, 3장 메달리온 아키텍처 해부), II부 메달리온 층 만들기(4장 Microsoft Fabric 기반, 5장 브론즈,
6장 실버, 7장 골드), III부 사례 셋(8장 AP Pension, 9장 Amadeus, 10장 ZEISS), IV부 확장·거버넌스·미래
(11장 확장, 12장 거버넌스와 보안, 13장 생성형 AI와 미래).

- 이 KB에서 맡는 자리는 **데이터 축(레이크하우스)의 메달리온 3층 원전(L2)**이다 — 아키텍처 축 밖이지만
  정박점(reis2022 데이터 엔지니어링 수명 주기·kimball2013 차원 모델링·linstedt2016 데이터 볼트·
  dehghani2022 데이터 메시·konieczny2025 설계 패턴)이 이미 있어 호출자가 많다. 1~3장이 L1/L2(3층 정의와
  계보), 5~7장이 층별 구축 L2, **4장 Fabric과 13장 생성형 AI는 L3로 얇게**(2025년 조건), 8~10장 사례는
  저자 판정만 claim으로.
- 원서만 반입했다. 한국어판은 확인되지 않았다(2026-09-23). 초판이 최신.
- 아카이브 스냅샷은 **EPUB**이다(PDF 판 없음). **인쇄판 쪽 앵커가 없어 locator는 장·절 단위**
  (`N장 §"절 제목"`) — percival2020 선례. 텍스트 레이어 판정과 반입 재개점의 정본은
  `it/archive/strengholt2025/_progress.yaml`이다.
